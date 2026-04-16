#!/usr/bin/env python3
"""
Elora LangGraph: Production ReAct agent using LangGraph's create_react_agent.

USAGE (CLI):
  python manage.py elora_langgraph --project-id <UUID>
  # Interactive REPL opens. Type 'help' for commands, 'quit' to exit.

Key improvements over custom ReAct implementation:
- Uses battle-tested LangGraph create_react_agent
- Proper ReAct reasoning → action → observation loops
- Automatic tool selection and execution
- Built-in conversation history and state management
- Production-ready error handling and recovery
- Eliminates "No steps executed" errors from null tools

Architecture:
- Canvas-centric workflow: Canvas = Story Beat = Location Interaction
- One-node-per-canvas policy for simplified story management
- Uses Django ORM models directly through @tool decorators
- Integrates with twee_comprehensive game generation system
"""

from __future__ import annotations

import json
import logging
import readline  # noqa: F401  # CLI history support
import sys
import time
import traceback
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any
import yaml

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction, models

# LangGraph and LangChain imports
try:
    from langchain_core.messages import AIMessage, HumanMessage
    from langchain_core.tools import tool
    from langchain_openai import ChatOpenAI
    from langgraph.prebuilt import create_react_agent
except ImportError as e:
    print(f"❌ LangGraph dependencies not installed: {e}")
    print("Run: pip install -r requirements/ai.txt")
    sys.exit(1)


# -----------------------------
# LOGGING INFRASTRUCTURE
# -----------------------------


class EloraSessionLogger:
    """Session-based structured logger for elora_cli with comprehensive tracking."""

    def __init__(self, project_id: str, logs_dir: Path = None):
        self.project_id = project_id
        self.session_id = str(uuid.uuid4())
        self.session_start = datetime.now()

        # Setup logs directory
        if logs_dir is None:
            logs_dir = Path(__file__).parent.parent.parent / "logs"
        logs_dir.mkdir(exist_ok=True)

        # Create session log file
        timestamp = self.session_start.strftime("%Y-%m-%d_%H-%M-%S")
        self.log_file = (
            logs_dir / f"elora_cli_{timestamp}_session_{self.session_id[:8]}.log"
        )

        # Setup logger
        self.logger = logging.getLogger(f"elora_cli_{self.session_id}")
        self.logger.setLevel(logging.DEBUG)

        # Remove existing handlers to avoid duplicates
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)

        # File handler with detailed formatting
        file_handler = logging.FileHandler(self.log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)

        # Create formatter for structured logging
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(funcName)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Initialize session
        self._log_session_start()

    def _log_session_start(self):
        """Log session initialization."""
        self.logger.info("=" * 80)
        self.logger.info("ELORA CLI SESSION STARTED")
        self.logger.info("=" * 80)
        self.logger.info(f"Session ID: {self.session_id}")
        self.logger.info(f"Project ID: {self.project_id}")
        self.logger.info(f"Start Time: {self.session_start.isoformat()}")
        self.logger.info(f"Log File: {self.log_file.name}")
        self.logger.info("=" * 80)

    def log_structured(self, level: str, component: str, action: str, **kwargs):
        """Log structured data with consistent format."""
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id,
            "project_id": self.project_id,
            "component": component,
            "action": action,
            **kwargs,
        }

        message = (
            f"{component.upper()}:{action.upper()} {json.dumps(log_data, default=str)}"
        )
        getattr(self.logger, level.lower())(message)

    def log_user_input(self, user_input: str, input_type: str = "command"):
        """Log user interactions."""
        self.log_structured(
            "info", "user", "input", input=user_input, input_type=input_type
        )

    def log_tool_execution(
        self,
        tool_name: str,
        params: dict = None,
        result: dict = None,
        duration_ms: float = None,
        error: str = None,
    ):
        """Log tool execution with parameters and results."""
        log_data = {"tool_name": tool_name}
        if params:
            log_data["params"] = params
        if result:
            log_data["result"] = result
        if duration_ms:
            log_data["duration_ms"] = duration_ms
        if error:
            log_data["error"] = error

        level = "error" if error else "info"
        self.log_structured(level, "tool", "execute", **log_data)

    def log_agent_operation(
        self, operation: str, details: dict = None, duration_ms: float = None
    ):
        """Log LangGraph agent operations."""
        log_data = {"operation": operation}
        if details:
            log_data.update(details)
        if duration_ms:
            log_data["duration_ms"] = duration_ms

        self.log_structured("info", "agent", operation, **log_data)

    def log_orm_operation(
        self,
        operation: str,
        model: str,
        details: dict = None,
        duration_ms: float = None,
        error: str = None,
    ):
        """Log Django ORM operations."""
        log_data = {"operation": operation, "model": model}
        if details:
            log_data.update(details)
        if duration_ms:
            log_data["duration_ms"] = duration_ms
        if error:
            log_data["error"] = error

        level = "error" if error else "debug"
        self.log_structured(level, "orm", operation, **log_data)

    def log_command_processing(
        self, command: str, command_type: str, result: str = None, error: str = None
    ):
        """Log command processing."""
        log_data = {"command": command, "command_type": command_type}
        if result:
            log_data["result"] = result
        if error:
            log_data["error"] = error

        level = "error" if error else "info"
        self.log_structured(level, "command", "process", **log_data)

    def log_error(self, error: Exception, context: str = None, **kwargs):
        """Log errors with full context."""
        error_data = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc(),
        }
        if context:
            error_data["context"] = context
        error_data.update(kwargs)

        self.log_structured("error", "system", "error", **error_data)

    def log_performance(self, operation: str, duration_ms: float, **kwargs):
        """Log performance metrics."""
        perf_data = {"operation": operation, "duration_ms": duration_ms}
        perf_data.update(kwargs)

        level = "warning" if duration_ms > 5000 else "info"  # Warn if >5 seconds
        self.log_structured(level, "performance", "timing", **perf_data)

    def log_session_end(self, exit_reason: str = "normal"):
        """Log session completion."""
        duration = (datetime.now() - self.session_start).total_seconds()

        self.logger.info("=" * 80)
        self.logger.info("ELORA CLI SESSION ENDED")
        self.logger.info(f"Duration: {duration:.2f} seconds")
        self.logger.info(f"Exit Reason: {exit_reason}")
        self.logger.info(f"End Time: {datetime.now().isoformat()}")
        self.logger.info("=" * 80)


def timing_decorator(logger: EloraSessionLogger, operation_name: str):
    """Decorator to time and log operations."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration_ms = (time.time() - start_time) * 1000
                logger.log_performance(
                    operation_name, duration_ms, function=func.__name__, success=True
                )
                return result
            except Exception as e:
                duration_ms = (time.time() - start_time) * 1000
                logger.log_error(e, context=f"{operation_name}:{func.__name__}")
                logger.log_performance(
                    operation_name, duration_ms, function=func.__name__, success=False
                )
                raise

        return wrapper

    return decorator


# -----------------------------
# CONFIG & MODEL DISCOVERY
# -----------------------------

DEFAULT_MODEL_MAP = {
    "Project": "projects.Project",
    "Location": "world.Location",
    "StoryCanvas": "stories.StoryCanvas",
    "StoryNode": "stories.StoryNode",
    "CanvasTrigger": "stories.CanvasTrigger",
    "TriggerSchedule": "stories.TriggerSchedule",
}


def get_models_for_agent(
    model_map: dict[str, str], logger: EloraSessionLogger = None
) -> dict[str, Any]:
    """Load Django models dynamically for the agent."""
    if logger:
        logger.log_structured(
            "info", "config", "model_loading_start", model_count=len(model_map)
        )

    models = {}
    for alias, model_path in model_map.items():
        start_time = time.time()
        try:
            app_label, model_name = model_path.split(".")
            model = apps.get_model(app_label, model_name)
            models[alias] = model

            if logger:
                duration_ms = (time.time() - start_time) * 1000
                logger.log_structured(
                    "debug",
                    "config",
                    "model_loaded",
                    alias=alias,
                    model_path=model_path,
                    duration_ms=duration_ms,
                )
        except (ValueError, LookupError) as e:
            error_msg = f"Could not load model {model_path}: {e}"
            print(f"⚠️  Warning: {error_msg}")

            if logger:
                logger.log_structured(
                    "warning",
                    "config",
                    "model_load_failed",
                    alias=alias,
                    model_path=model_path,
                    error=str(e),
                )

    if logger:
        logger.log_structured(
            "info",
            "config",
            "model_loading_complete",
            loaded_count=len(models),
            total_count=len(model_map),
        )

    return models


def must_get_openai_key(logger: EloraSessionLogger = None) -> str:
    """Get OpenAI API key from environment."""
    if logger:
        logger.log_structured("debug", "config", "openai_key_check")

    key = getattr(settings, "OPENAI_API_KEY", None)
    if not key:
        error_msg = (
            "OPENAI_API_KEY environment variable required. "
            "Set it in your .env file or environment."
        )
        if logger:
            logger.log_structured(
                "error", "config", "openai_key_missing", error=error_msg
            )
        raise CommandError(error_msg)

    if logger:
        logger.log_structured(
            "info",
            "config",
            "openai_key_found",
            key_length=len(key),
            key_prefix=key[:10] + "...",
        )

    return key


def uuid_like(s: str) -> bool:
    """Check if string looks like a UUID."""
    try:
        uuid.UUID(str(s))
        return True
    except Exception:
        return False


def convert_simple_to_rich_format(simple_blocks: list) -> list:
    """Convert content blocks to BlockNote-like format (Phase 1 constraints).

    Allowed types: "paragraph" and "heading" only.
    - Preserves existing rich blocks when possible.
    - Ensures every block has an id, type, props, content, and children=[]
    - For headings, enforces props.level ∈ {1,2,3} (defaults to 2 if missing/invalid)
    - Unsupported types are downgraded to paragraph
    """
    if not simple_blocks:
        return []

    def _sanitize_props(block_type: str, src: dict) -> dict:
        props = src.get("props", {}) if isinstance(src.get("props"), dict) else {}

        if block_type == "heading":
            # Accept level from either props.level or top-level level
            level = props.get("level")
            if level is None:
                level = src.get("level")
            try:
                level = int(level) if level is not None else None
            except Exception:
                level = None
            if level not in {1, 2, 3}:
                level = 2
            props = {**props, "level": level}
        else:
            # Paragraphs do not require any props
            props = {k: v for k, v in props.items() if k in {}}

        return props

    def _allowed_type(t: str) -> str:
        return t if t in {"paragraph", "heading"} else "paragraph"

    rich_blocks: list[dict] = []
    for block in simple_blocks:
        if not isinstance(block, dict):
            continue

        block_type = _allowed_type(block.get("type", "paragraph"))
        content = block.get("content", "")
        block_id = block.get("id") or str(uuid.uuid4())
        props = _sanitize_props(block_type, block)

        rich_blocks.append(
            {
                "id": str(block_id),
                "type": block_type,
                "props": props,
                "content": content if isinstance(content, str) else str(content),
                "children": [],  # Phase 1: no nested content
            }
        )

    return rich_blocks


# -----------------------------
# DYNAMIC COMMAND LOADER
# -----------------------------


class CommandLoader:
    """Load and manage dynamic slash commands from markdown files."""

    def __init__(self, commands_dir: Path | str):
        self.commands_dir = Path(commands_dir)
        self._commands: dict[str, dict] = {}
        self._last_scan = 0

    def scan_commands(self) -> dict[str, dict]:
        """Scan commands directory and load command files."""
        if not self.commands_dir.exists():
            return {}

        commands = {}

        for md_file in self.commands_dir.glob("*.md"):
            if md_file.name.startswith(".") or md_file.name == "README.md":
                continue

            try:
                command_name = md_file.stem.lower()
                content = md_file.read_text(encoding="utf-8").strip()

                # Parse frontmatter if present
                description = ""
                prompt_content = content

                if content.startswith("---"):
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        try:
                            frontmatter = yaml.safe_load(parts[1])
                            description = frontmatter.get("description", "")
                            prompt_content = parts[2].strip()
                        except yaml.YAMLError:
                            # If YAML parsing fails, treat entire content as prompt
                            pass

                commands[command_name] = {
                    "description": description,
                    "content": prompt_content,
                    "file": str(md_file),
                }

            except Exception as e:
                print(f"⚠️  Warning: Could not load command {md_file.name}: {e}")

        return commands

    def get_commands(self) -> dict[str, dict]:
        """Get all available commands, scanning directory if needed."""
        # Simple approach: scan every time (could add caching later)
        self._commands = self.scan_commands()
        return self._commands

    def get_command(self, name: str) -> str | None:
        """Get command content by name."""
        commands = self.get_commands()
        command = commands.get(name.lower())
        return command["content"] if command else None

    def list_commands(self) -> list[tuple[str, str]]:
        """List all commands with their descriptions."""
        commands = self.get_commands()
        return [(name, cmd["description"]) for name, cmd in commands.items()]


# -----------------------------
# LANGGRAPH TOOLS (Django Integration)
# -----------------------------


class EloraTools:
    """Django-integrated tools for LangGraph ReAct agent."""

    def __init__(
        self, project_id: str, models: dict[str, Any], logger: EloraSessionLogger = None
    ):
        self.project_id = project_id
        self.models = models
        self.logger = logger

        if self.logger:
            self.logger.log_structured(
                "info",
                "tools",
                "init_start",
                project_id=project_id,
                available_models=list(models.keys()),
            )

        # Validate project exists
        start_time = time.time()
        try:
            self.project = self.models["Project"].objects.get(pk=project_id)

            if self.logger:
                duration_ms = (time.time() - start_time) * 1000
                self.logger.log_orm_operation(
                    "get",
                    "Project",
                    details={
                        "project_id": project_id,
                        "project_name": getattr(self.project, "name", "Unknown"),
                    },
                    duration_ms=duration_ms,
                )
                self.logger.log_structured(
                    "info",
                    "tools",
                    "init_success",
                    project_name=getattr(self.project, "name", "Unknown"),
                )
        except self.models["Project"].DoesNotExist:
            if self.logger:
                duration_ms = (time.time() - start_time) * 1000
                self.logger.log_orm_operation(
                    "get",
                    "Project",
                    details={"project_id": project_id},
                    duration_ms=duration_ms,
                    error="Project not found",
                )
            raise CommandError(f"Project {project_id} not found")

    def _log_tool_call(
        self,
        tool_name: str,
        params: dict = None,
        result: dict = None,
        duration_ms: float = None,
        error: str = None,
    ):
        """Helper to log tool calls."""
        if self.logger:
            self.logger.log_tool_execution(
                tool_name, params, result, duration_ms, error
            )

    def list_locations(self, query: str = "") -> dict:
        """List locations in the project, optionally filtered by name."""
        start_time = time.time()
        params = {"query": query}

        try:
            locations = (
                self.models["Location"]
                .objects.filter(project_id=self.project_id)
                .order_by("created_at")
            )

            if query.strip():
                locations = locations.filter(name__icontains=query.strip())

            locations = locations[:25]  # Limit results

            data = []
            for loc in locations:
                data.append(
                    {
                        "id": str(loc.pk),
                        "name": loc.name,
                        "description": loc.description,
                        "location_type": loc.location_type,
                        "is_container": bool(getattr(loc, "is_container", False)),
                        "parent_location_id": (
                            str(loc.parent_location_id)
                            if getattr(loc, "parent_location_id", None)
                            else None
                        ),
                    }
                )

            result = {
                "success": True,
                "count": len(data),
                "locations": data,
                "query": query,
            }
            duration_ms = (time.time() - start_time) * 1000

            self._log_tool_call("list_locations", params, result, duration_ms)

            if self.logger:
                self.logger.log_orm_operation(
                    "filter",
                    "Location",
                    details={
                        "project_id": self.project_id,
                        "query": query,
                        "count": len(data),
                    },
                    duration_ms=duration_ms,
                )

            return result

        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            error_str = str(e)
            self._log_tool_call("list_locations", params, None, duration_ms, error_str)

            if self.logger:
                self.logger.log_orm_operation(
                    "filter",
                    "Location",
                    details={"project_id": self.project_id, "query": query},
                    duration_ms=duration_ms,
                    error=error_str,
                )
            raise

    def get_location(self, identifier: str) -> dict:
        """Get specific location details by ID or name."""
        try:
            if uuid_like(identifier):
                location = self.models["Location"].objects.get(
                    pk=identifier, project_id=self.project_id
                )
            else:
                location = self.models["Location"].objects.get(
                    name=identifier, project_id=self.project_id
                )

            return {
                "success": True,
                "location": {
                    "id": str(location.pk),
                    "name": location.name,
                    "description": location.description,
                    "location_type": location.location_type,
                    "canvas_x": location.canvas_x,
                    "canvas_y": location.canvas_y,
                },
            }
        except self.models["Location"].DoesNotExist:
            return {"success": False, "error": f"Location not found: {identifier}"}

    @transaction.atomic
    def set_entry_from(self, location_id: str, entry_from_id: str) -> dict:
        """Set the single location this can be entered from (with navigation rule enforcement)."""
        try:
            location = self.models["Location"].objects.get(
                id=location_id, project_id=self.project_id
            )

            entry_from = None
            if entry_from_id:
                entry_from = self.models["Location"].objects.get(
                    id=entry_from_id, project_id=self.project_id
                )

                # Rule 1: Container default entry enforcement (ONLY for inside locations)
                if entry_from.is_container and entry_from.default_entry_location:
                    # Check if this is an INSIDE connection (same parent) or OUTSIDE (different parent)
                    is_inside_connection = (location.parent_location == entry_from)

                    if is_inside_connection and entry_from.default_entry_location != location:
                        return {
                            "success": False,
                            "error": f"Cannot set direct entry from container '{entry_from.name}' for inside location. "
                            f"Inside locations must go through its default entry: '{entry_from.default_entry_location.name}'",
                        }
                    # Outside connections are allowed even if container has default_entry

                # Rule 4: Container boundary respect (except for default entries)
                if (
                    location.parent_location
                    and entry_from.parent_location != location.parent_location
                ):
                    # Exception: This location is a default entry for its parent container
                    is_default_entry = (
                        location.parent_location.default_entry_location == location
                    )
                    if not is_default_entry:
                        from_container = (
                            entry_from.parent_location.name
                            if entry_from.parent_location
                            else "root"
                        )
                        to_container = location.parent_location.name
                        return {
                            "success": False,
                            "error": f"Cannot create cross-container connection "
                            f"from '{entry_from.name}' (in '{from_container}') "
                            f"to '{location.name}' (in '{to_container}') "
                            f"unless '{location.name}' is the default entry for its container",
                        }

            # Test the change with Django model validation before saving
            old_entry_from = location.entry_from
            location.entry_from = entry_from
            try:
                location.full_clean()  # This will run our model validation rules
            except Exception as e:
                location.entry_from = old_entry_from  # Revert the change
                return {
                    "success": False,
                    "error": f"Navigation rule violation: {str(e)}",
                }

            location.save()

            return {
                "success": True,
                "location_id": str(location.id),
                "entry_from_id": str(entry_from.id) if entry_from else None,
                "message": f"Set entry for '{location.name}' from '{entry_from.name if entry_from else 'None'}'",
            }
        except self.models["Location"].DoesNotExist:
            return {"success": False, "error": "One or both locations not found"}

    @transaction.atomic
    def add_entry_connection(self, from_location_id: str, to_location_id: str) -> dict:
        """Add entry connection between locations (with navigation rule enforcement)."""
        # Use the rule-enforced set_entry_from method
        return self.set_entry_from(to_location_id, from_location_id)

    @transaction.atomic
    def remove_entry_connection(
        self, from_location_id: str, to_location_id: str
    ) -> dict:
        """Remove entry connection between locations (simplified navigation system)."""
        try:
            to_location = self.models["Location"].objects.get(
                id=to_location_id, project_id=self.project_id
            )

            # In simplified system, removing connection means removing the entry_from reference
            if (
                to_location.entry_from
                and str(to_location.entry_from.id) == from_location_id
            ):
                from_location_name = to_location.entry_from.name
                to_location.entry_from = None
                to_location.full_clean()  # Validate before saving
                to_location.save()
                return {
                    "success": True,
                    "from_location_id": from_location_id,
                    "to_location_id": to_location_id,
                    "message": f"Removed entry from '{from_location_name}' to '{to_location.name}'",
                }
            else:
                return {
                    "success": False,
                    "error": f"No entry connection exists from {from_location_id} to {to_location_id}",
                }
        except self.models["Location"].DoesNotExist:
            return {"success": False, "error": "Location not found"}

    @transaction.atomic
    def set_default_entry_location(
        self, container_id: str, entry_location_id: str
    ) -> dict:
        """Set default entry location for a container."""
        try:
            container = self.models["Location"].objects.get(
                id=container_id, project_id=self.project_id
            )
            entry_location = self.models["Location"].objects.get(
                id=entry_location_id, project_id=self.project_id
            )

            # Ensure the container is actually a container
            if not container.is_container:
                container.is_container = True
                container.save()

            # Debug logging for nesting validation
            if self.logger:
                self.logger.log_structured(
                    "debug",
                    "world_designer",
                    "default_entry_validation",
                    container_name=container.name,
                    container_id=str(container.id),
                    entry_name=entry_location.name,
                    entry_id=str(entry_location.id),
                    entry_parent_id=(
                        str(entry_location.parent_location.id)
                        if entry_location.parent_location
                        else None
                    ),
                    entry_parent_name=(
                        entry_location.parent_location.name
                        if entry_location.parent_location
                        else None
                    ),
                    validation_result=entry_location.parent_location == container,
                )

            # Ensure the entry location is actually inside the container
            if entry_location.parent_location != container:
                # Provide helpful error message with suggestion
                current_parent = (
                    entry_location.parent_location.name
                    if entry_location.parent_location
                    else "None"
                )
                suggestion = f' Try using nest operation first: {{"op": "nest", "data": {{"child": "{entry_location.name}", "parent": "{container.name}"}}}}'
                return {
                    "success": False,
                    "error": f"Entry location '{entry_location.name}' is not inside container '{container.name}'. Current parent: {current_parent}.{suggestion}",
                }

            # Clear entry_from for the default entry location (default entries should not have entry_from)
            if entry_location.entry_from is not None:
                if self.logger:
                    self.logger.log_structured(
                        "info",
                        "world_designer",
                        "clear_entry_from",
                        location=entry_location.name,
                        old_entry_from=entry_location.entry_from.name,
                        reason="default_entry_location",
                    )

                entry_location.entry_from = None
                entry_location.full_clean()  # Validate before saving
                entry_location.save()

            # Clear any existing entry_from relationships pointing to this container
            # since the container now has a default entry
            locations_entering_container = (
                self.models["Location"]
                .objects.filter(project_id=self.project_id, entry_from=container)
                .exclude(id=entry_location.id)
            )

            for loc in locations_entering_container:
                if self.logger:
                    self.logger.log_structured(
                        "info",
                        "world_designer",
                        "clear_container_entry",
                        location=loc.name,
                        container=container.name,
                        reason="container_has_default_entry",
                    )
                loc.entry_from = None
                loc.full_clean()  # Validate before saving
                loc.save()

            # Now set the default entry location (after fixing entry_from)
            container.default_entry_location = entry_location
            container.full_clean()  # Validate before saving
            container.save()

            return {
                "success": True,
                "container_id": str(container.id),
                "entry_location_id": str(entry_location.id),
                "message": f"Set default entry for '{container.name}' to '{entry_location.name}' (cleared conflicting entry_from relationships)",
            }
        except self.models["Location"].DoesNotExist:
            return {"success": False, "error": "Container or entry location not found"}

    @transaction.atomic
    def create_location(
        self, name: str, description: str = "", location_type: str = "generic"
    ) -> dict:
        """Create a new location (idempotent by project+name)."""
        # Check if already exists
        existing = (
            self.models["Location"]
            .objects.filter(project_id=self.project_id, name=name)
            .first()
        )

        if existing:
            return {
                "success": True,
                "created": False,
                "location_id": str(existing.pk),
                "message": f"Location '{name}' already exists",
            }

        location = self.models["Location"].objects.create(
            project_id=self.project_id,
            name=name,
            description=description,
            location_type=location_type,
        )

        return {
            "success": True,
            "created": True,
            "location_id": str(location.pk),
            "message": f"Created location '{name}'",
        }

    def get_world_graph(self) -> dict:
        """Build a read-only snapshot of the world graph for this project.

        Returns:
            dict with keys:
              - nodes: [{id, name, is_container, parent_id, entry_from_id}]
              - entry_connections: {from_id: [to_id, ...]} (reverse of entry_from)
              - containers: {container_id: [child_id, ...]}
              - components: [[location_id, ...], ...] (based on entry connections)
              - stats: counts summary
        """
        Location = self.models.get("Location")
        if not Location:
            return {"success": False, "error": "Location model unavailable"}

        # Locations with entry_from relationships
        locations = list(
            Location.objects.filter(project_id=self.project_id).select_related(
                "entry_from"
            )
        )
        nodes = [
            {
                "id": str(l.id),
                "name": l.name,
                "is_container": bool(getattr(l, "is_container", False)),
                "parent_id": (
                    str(l.parent_location_id)
                    if getattr(l, "parent_location_id", None)
                    else None
                ),
                "entry_from_id": str(l.entry_from.id) if l.entry_from else None,
            }
            for l in locations
        ]

        # Build entry connections (reverse of entry_from)
        entry_connections: dict[str, list] = {}
        for l in locations:
            if l.entry_from:
                from_id = str(l.entry_from.id)
                to_id = str(l.id)
                if from_id not in entry_connections:
                    entry_connections[from_id] = []
                entry_connections[from_id].append(to_id)

        # Containers → children
        containers: dict[str, list] = {}
        for l in locations:
            if getattr(l, "parent_location_id", None):
                pid = str(l.parent_location_id)
                containers.setdefault(pid, []).append(str(l.id))

        # Components (based on entry connections - undirected connectivity)
        adj: dict[str, set] = {str(l.id): set() for l in locations}
        for from_id, to_ids in entry_connections.items():
            for to_id in to_ids:
                adj[from_id].add(to_id)
                adj[to_id].add(from_id)  # undirected for components

        seen = set()
        components: list[list[str]] = []
        for node_id in adj.keys():
            if node_id in seen:
                continue
            stack = [node_id]
            comp = []
            while stack:
                nid = stack.pop()
                if nid in seen:
                    continue
                seen.add(nid)
                comp.append(nid)
                stack.extend([n for n in adj[nid] if n not in seen])
            components.append(comp)

        # Calculate total connections count
        total_entry_connections = sum(
            len(to_ids) for to_ids in entry_connections.values()
        )

        return {
            "success": True,
            "nodes": nodes,
            "entry_connections": entry_connections,
            "containers": containers,
            "components": components,
            "stats": {
                "locations": len(nodes),
                "entry_connections": total_entry_connections,
                "containers": len(containers),
                "components": len(components),
            },
        }

    def list_story_canvases(self, query: str = "", location_id: str = "") -> dict:
        """List story canvases, optionally filtered."""
        canvases = (
            self.models["StoryCanvas"]
            .objects.filter(project_id=self.project_id)
            .prefetch_related("nodes", "trigger__schedules")
            .order_by("created_at")
        )

        if query.strip():
            canvases = canvases.filter(name__icontains=query.strip())

        if location_id.strip():
            canvases = canvases.filter(trigger__location_id=location_id.strip())

        canvases = canvases[:25]  # Limit results

        data = []
        for canvas in canvases:
            trigger_location = None
            if hasattr(canvas, "trigger") and canvas.trigger:
                if canvas.trigger.location_id:
                    try:
                        loc = self.models["Location"].objects.get(
                            pk=canvas.trigger.location_id
                        )
                        trigger_location = {"id": str(loc.pk), "name": loc.name}
                    except self.models["Location"].DoesNotExist:
                        pass

            data.append(
                {
                    "id": str(canvas.pk),
                    "name": canvas.name,
                    "description": canvas.description,
                    "trigger_location": trigger_location,
                    "node_count": canvas.nodes.count(),
                }
            )

        return {
            "success": True,
            "count": len(data),
            "canvases": data,
            "filters": {"query": query, "location_id": location_id},
        }

    def get_story_canvas(self, identifier: str) -> dict:
        """Get story canvas with full content."""
        try:
            if uuid_like(identifier):
                canvas = self.models["StoryCanvas"].objects.get(
                    pk=identifier, project_id=self.project_id
                )
            else:
                canvas = self.models["StoryCanvas"].objects.get(
                    name=identifier, project_id=self.project_id
                )

            # Get single node (one-node-per-canvas policy)
            node = canvas.nodes.first()
            node_data = None
            if node:
                node_data = {
                    "id": str(node.pk),
                    "name": node.name,
                    "content_blocks": (
                        node.node_data.get("blocks", []) if node.node_data else []
                    ),
                    "exit_block": node.exit_block,
                }

            # Get trigger info
            trigger_info = None
            if hasattr(canvas, "trigger") and canvas.trigger:
                trigger_location = None
                if canvas.trigger.location_id:
                    try:
                        loc = self.models["Location"].objects.get(
                            pk=canvas.trigger.location_id
                        )
                        trigger_location = {"id": str(loc.pk), "name": loc.name}
                    except self.models["Location"].DoesNotExist:
                        pass

                schedules = []
                for schedule in canvas.trigger.schedules.all():
                    schedules.append(
                        {
                            "id": str(schedule.pk),
                            "name": schedule.name,
                            "weekdays": schedule.weekdays,
                            "start_time": schedule.start_time.strftime("%H:%M"),
                            "end_time": (
                                schedule.end_time.strftime("%H:%M")
                                if schedule.end_time
                                else None
                            ),
                        }
                    )

                trigger_info = {
                    "location": trigger_location,
                    "is_active": canvas.trigger.is_active,
                    "schedules": schedules,
                }

            return {
                "success": True,
                "canvas": {
                    "id": str(canvas.pk),
                    "name": canvas.name,
                    "description": canvas.description,
                    "node_data": node_data,
                    "trigger_info": trigger_info,
                },
            }
        except self.models["StoryCanvas"].DoesNotExist:
            return {"success": False, "error": f"Story canvas not found: {identifier}"}

    @transaction.atomic
    def create_story_canvas(
        self,
        name: str,
        location_id: str,
        content_blocks: list,
        description: str = "",
        schedules: list | None = None,
    ) -> dict:
        """Create story canvas with single node and trigger (one-node-per-canvas policy)."""
        # Validate location exists
        try:
            location = self.models["Location"].objects.get(
                pk=location_id, project_id=self.project_id
            )
        except self.models["Location"].DoesNotExist:
            return {"success": False, "error": f"Location not found: {location_id}"}

        # Check if canvas already exists with this name
        existing = (
            self.models["StoryCanvas"]
            .objects.filter(project_id=self.project_id, name=name)
            .first()
        )

        if existing:
            return {"success": False, "error": f"Canvas '{name}' already exists"}

        # Create canvas
        canvas = self.models["StoryCanvas"].objects.create(
            project_id=self.project_id,
            name=name,
            description=description,
        )

        # Create single node (one-node-per-canvas policy)
        # Convert simple format to rich editor format
        rich_content_blocks = convert_simple_to_rich_format(content_blocks)

        # Build BlockNote-compliant node_data (versioned + preview content)
        # Backend expects version "2.0" to treat blocks as canonical format.
        preview_text = "\n".join(
            [
                str(b.get("content", "")).strip()
                for b in rich_content_blocks
                if str(b.get("content", "")).strip()
            ]
        )
        node_data = {
            "blocks": rich_content_blocks,
            "version": "2.0",
            "content": preview_text,
        }
        node = self.models["StoryNode"].objects.create(
            canvas=canvas,
            name=f"{name} Content",
            node_data=node_data,
            exit_block={
                "type": "location",
                "text": "Continue",
                "config": {
                    "destinationType": "trigger",
                    "time_progression_minutes": 3,
                },
            },
        )

        # Create trigger
        trigger = self.models["CanvasTrigger"].objects.create(
            canvas=canvas,
            location_id=location_id,
            is_active=True,
        )

        # Optionally create schedules for the trigger (atomic with canvas + trigger)
        created_schedules = []
        if schedules:
            # Import locally to avoid module import side-effects at load time
            from apps.stories.services.scheduling import (
                TriggerScheduleService,
            )

            created = TriggerScheduleService.create_multiple_schedules(
                trigger_id=trigger.id, schedules_data=schedules
            )

            # Normalize response shape
            for sched in created:
                created_schedules.append(
                    {
                        "id": str(sched.id),
                        "name": sched.name,
                        "weekdays": sched.weekdays,
                        "start_time": sched.start_time.strftime("%H:%M"),
                        "end_time": (
                            sched.end_time.strftime("%H:%M") if sched.end_time else None
                        ),
                    }
                )

        return {
            "success": True,
            "created": True,
            "canvas_id": str(canvas.pk),
            "node_id": str(node.pk),
            "trigger_id": str(trigger.pk),
            "schedules": created_schedules,
            "message": f"Created canvas '{name}' triggered by '{location.name}'",
        }

    def generate_game_twee(self) -> dict:
        """Generate twee content using twee_comprehensive system."""
        try:
            from apps.game_generation.twee_comprehensive.services import (
                TweeComprehensiveService,
            )

            service = TweeComprehensiveService()
            twee_content = service.generate(self.project, version="v1")

            return {
                "success": True,
                "twee_length": len(twee_content),
                "message": f"Generated {len(twee_content):,} characters of twee content",
            }
        except Exception as e:
            return {"success": False, "error": f"Generation failed: {str(e)}"}

    def validate_project(self) -> dict:
        """Validate project for generation."""
        try:
            # Basic validation checks
            location_count = (
                self.models["Location"]
                .objects.filter(project_id=self.project_id)
                .count()
            )
            canvas_count = (
                self.models["StoryCanvas"]
                .objects.filter(project_id=self.project_id)
                .count()
            )

            issues = []
            if location_count == 0:
                issues.append("No locations defined")
            if canvas_count == 0:
                issues.append("No story canvases defined")

            return {
                "success": len(issues) == 0,
                "stats": {
                    "locations": location_count,
                    "canvases": canvas_count,
                },
                "issues": issues,
                "message": (
                    "Project valid for generation"
                    if not issues
                    else f"{len(issues)} issues found"
                ),
            }
        except Exception as e:
            return {"success": False, "error": f"Validation failed: {str(e)}"}

    def validate_world_graph(self) -> dict:
        """Minimal world graph validation: isolates and basic stats (simplified navigation system).

        - Info: single location with zero entry connections
        - Error: isolated locations when total_locations >= 2
        """
        Location = self.models.get("Location")
        if not Location:
            return {"success": False, "error": "Location model unavailable"}

        locations = list(
            Location.objects.filter(project_id=self.project_id).select_related(
                "entry_from"
            )
        )
        location_ids = {str(l.id) for l in locations}

        issues = []

        if len(locations) == 0:
            return {
                "success": True,
                "stats": {"locations": 0, "entry_connections": 0},
                "issues": [
                    {
                        "severity": "info",
                        "code": "NO_LOCATIONS",
                        "message": "No locations in project",
                    }
                ],
            }

        # Count connections for isolation detection
        degree = {lid: 0 for lid in location_ids}
        total_entry_connections = 0

        for l in locations:
            # In simplified system, count entry_from connections
            if l.entry_from:
                total_entry_connections += 1
                degree[str(l.id)] += 1  # This location has an incoming connection
                degree[
                    str(l.entry_from.id)
                ] += 1  # The source location has an outgoing connection

        if len(locations) == 1 and total_entry_connections == 0:
            issues.append(
                {
                    "severity": "info",
                    "code": "FIRST_LOCATION_UNCONNECTED",
                    "message": "Single unconnected location (bootstrap is OK)",
                }
            )
        elif len(locations) >= 2:
            isolated = [lid for lid, d in degree.items() if d == 0]
            if isolated:
                # Fetch names for clarity
                name_index = {str(l.id): l.name for l in locations}
                readable = ", ".join([name_index.get(lid, lid) for lid in isolated])
                issues.append(
                    {
                        "severity": "error",
                        "code": "ISOLATED_NODE",
                        "message": f"Isolated locations with no entry connections: {readable}",
                    }
                )

        return {
            "success": True,
            "stats": {
                "locations": len(locations),
                "entry_connections": total_entry_connections,
            },
            "issues": issues,
        }

    def validate_navigation_rules(self) -> dict:
        """Validate navigation consistency rules for containers and default entries."""
        Location = self.models.get("Location")
        if not Location:
            return {"success": False, "error": "Location model unavailable"}

        locations = list(
            Location.objects.filter(project_id=self.project_id).select_related(
                "entry_from", "parent_location", "default_entry_location"
            )
        )
        issues = []

        for loc in locations:
            # Check Rule 1: Container default entry bypass violations (ONLY for inside locations)
            if loc.is_container and loc.default_entry_location:
                # Find INSIDE locations that enter directly from this container (bypassing default entry)
                bypass_entries = [
                    l
                    for l in locations
                    if l.entry_from == loc
                    and l != loc.default_entry_location
                    and l.parent_location == loc  # ONLY check inside locations
                ]

                if bypass_entries:
                    bypass_names = [l.name for l in bypass_entries]
                    issues.append(
                        {
                            "severity": "error",
                            "code": "CONTAINER_BYPASS",
                            "message": f"Container '{loc.name}' has default entry '{loc.default_entry_location.name}' "
                            f"but these INSIDE locations bypass it: {bypass_names}",
                            "container": loc.name,
                            "default_entry": loc.default_entry_location.name,
                            "bypass_locations": bypass_names,
                        }
                    )

            # Check Rule 3: Default entry consistency
            if (
                loc.parent_location
                and hasattr(loc.parent_location, "default_entry_location")
                and loc.parent_location.default_entry_location == loc
            ):
                if loc.entry_from != loc.parent_location:
                    expected_from = (
                        loc.parent_location.name if loc.parent_location else "None"
                    )
                    actual_from = loc.entry_from.name if loc.entry_from else "None"
                    issues.append(
                        {
                            "severity": "error",
                            "code": "DEFAULT_ENTRY_MISMATCH",
                            "message": f"'{loc.name}' is default entry for '{loc.parent_location.name}' "
                            f"but has entry_from={actual_from} instead of {expected_from}",
                            "location": loc.name,
                            "container": loc.parent_location.name,
                            "expected_entry_from": expected_from,
                            "actual_entry_from": actual_from,
                        }
                    )

            # Check Rule 4: Container boundary violations
            if (
                loc.entry_from
                and loc.parent_location
                and loc.entry_from.parent_location != loc.parent_location
            ):
                # Exception: This location is a default entry for its parent container
                is_default_entry = (
                    hasattr(loc.parent_location, "default_entry_location")
                    and loc.parent_location.default_entry_location == loc
                )

                if not is_default_entry:
                    from_container = (
                        loc.entry_from.parent_location.name
                        if loc.entry_from.parent_location
                        else "root"
                    )
                    to_container = loc.parent_location.name
                    issues.append(
                        {
                            "severity": "warning",
                            "code": "CROSS_CONTAINER_CONNECTION",
                            "message": f"Cross-container connection from '{loc.entry_from.name}' "
                            f"(in '{from_container}') to '{loc.name}' (in '{to_container}')",
                            "from_location": loc.entry_from.name,
                            "from_container": from_container,
                            "to_location": loc.name,
                            "to_container": to_container,
                        }
                    )

        return {
            "success": True,
            "rules_checked": [
                "container_bypass",
                "default_entry_consistency",
                "container_boundaries",
            ],
            "issues": issues,
            "stats": {
                "total_locations": len(locations),
                "containers_with_default_entry": len(
                    [
                        l
                        for l in locations
                        if l.is_container and l.default_entry_location
                    ]
                ),
                "cross_container_connections": len(
                    [i for i in issues if i["code"] == "CROSS_CONTAINER_CONNECTION"]
                ),
                "rule_violations": len([i for i in issues if i["severity"] == "error"]),
            },
        }

    @transaction.atomic
    def make_container(self, location_id: str, is_container: bool = True) -> dict:
        """Mark/unmark a location as a container within this project."""
        Location = self.models.get("Location")
        if not Location:
            return {"success": False, "error": "Location model unavailable"}

        try:
            loc = Location.objects.get(pk=location_id, project_id=self.project_id)
        except Location.DoesNotExist:
            return {"success": False, "error": f"Location not found: {location_id}"}

        loc.is_container = bool(is_container)
        loc.save(
            update_fields=["is_container", "updated_at"]
        )  # clean() called in save()
        return {
            "success": True,
            "location_id": str(loc.id),
            "is_container": loc.is_container,
            "message": (
                "Marked as container" if loc.is_container else "Unset container"
            ),
        }

    @transaction.atomic
    def nest_location(
        self,
        location_id: str,
        container_id: str,
        relative_x: float | None = None,
        relative_y: float | None = None,
    ) -> dict:
        """Nest a location into a container (set parent_location and relative pos).

        - Validates both entities belong to the same project
        - Ensures container.is_container is True (auto-sets if needed)
        - Sets relative_x/relative_y (defaults to current canvas_x/y)
        """
        Location = self.models.get("Location")
        if not Location:
            return {"success": False, "error": "Location model unavailable"}

        if location_id == container_id:
            return {"success": False, "error": "Location cannot be nested into itself"}

        try:
            loc = Location.objects.get(pk=location_id, project_id=self.project_id)
            container = Location.objects.get(
                pk=container_id, project_id=self.project_id
            )
        except Location.DoesNotExist:
            return {
                "success": False,
                "error": "Both location and container must exist in this project",
            }

        # Ensure container status
        if not container.is_container:
            container.is_container = True
            container.save(
                update_fields=["is_container", "updated_at"]
            )  # triggers clean()

        # Default relative position to current absolute if not provided
        rx = loc.canvas_x if relative_x is None else relative_x
        ry = loc.canvas_y if relative_y is None else relative_y

        # Apply nesting
        loc.parent_location = container
        loc.relative_x = rx
        loc.relative_y = ry
        loc.save()  # clean() recalculates hierarchy_level and validates

        # Debug logging for nest operation
        if self.logger:
            self.logger.log_structured(
                "debug",
                "world_designer",
                "nest_operation_completed",
                location_name=loc.name,
                location_id=str(loc.id),
                container_name=container.name,
                container_id=str(container.id),
                parent_set_to=(
                    str(loc.parent_location.id) if loc.parent_location else None
                ),
                parent_name=loc.parent_location.name if loc.parent_location else None,
                hierarchy_level=loc.hierarchy_level,
            )

        # Validation check: Ensure the nesting actually worked
        loc.refresh_from_db()  # Reload from database to ensure we have the latest state
        if loc.parent_location != container:
            return {
                "success": False,
                "error": f"Nest operation failed: {loc.name} parent_location is {loc.parent_location.name if loc.parent_location else 'None'}, expected {container.name}",
            }

        return {
            "success": True,
            "location_id": str(loc.id),
            "container_id": str(container.id),
            "relative_x": loc.relative_x,
            "relative_y": loc.relative_y,
            "hierarchy_level": loc.hierarchy_level,
            "message": f"Nested '{loc.name}' into '{container.name}'",
        }

    @transaction.atomic
    def smart_place_room(
        self,
        container_identifier: str,
        room_name: str,
        room_description: str = "",
        preferred_hubs: list[str] | None = None,
        auto_create_hub: bool = False,
        bidirectional: bool = True,
    ) -> dict:
        """Smartly place a room inside a container: ensure container, nest, and connect via entry connections.

        Steps:
        - Resolve container by UUID or name (exact match)
        - Ensure container.is_container = True
        - Create or get room (idempotent by name within project)
        - Choose an interior hub under/near the container using heuristics:
            1) preferred_hubs name match (case-insensitive contains)
            2) hub keywords among children: ["living room", "hallway", "lobby", "foyer", "main hall", "town square"]
            3) most-connected child (by degree)
          If none and auto_create_hub is True: create "Hallway" under container.
          If still none: return needs_input for agent to ask the user.
        - Nest the room under the container
        - Ensure entry connections hub ↔ room (bidirectional by default)
        - Ensure entry connections container ↔ hub exists (bidirectional by default)
        - Validate world graph and include issues
        """
        Location = self.models.get("Location")
        if not Location:
            return {"success": False, "error": "Required models unavailable"}

        # Resolve container
        try:
            if uuid_like(container_identifier):
                container = Location.objects.get(
                    pk=container_identifier, project_id=self.project_id
                )
            else:
                container = Location.objects.get(
                    name=container_identifier, project_id=self.project_id
                )
        except Location.DoesNotExist:
            return {
                "success": False,
                "error": f"Container not found: {container_identifier}",
            }

        # Ensure container flag
        if not container.is_container:
            container.is_container = True
            container.save(update_fields=["is_container", "updated_at"])

        # Create/get room idempotently
        room = Location.objects.filter(
            project_id=self.project_id, name=room_name
        ).first()
        created_room = False
        if not room:
            room = Location.objects.create(
                project_id=self.project_id,
                name=room_name,
                description=room_description,
                location_type="residential",
            )
            created_room = True

        # Helper: degree map
        # Degree via simplified navigation (count destinations from each location)
        all_locs = list(
            Location.objects.filter(project_id=self.project_id).select_related(
                "entry_from"
            )
        )
        degree: dict[str, int] = {}
        for l in all_locs:
            degree[str(l.id)] = 0

        # Count outgoing connections (locations that can be entered from each location)
        for l in all_locs:
            if l.entry_from:
                from_id = str(l.entry_from.id)
                degree[from_id] = degree.get(from_id, 0) + 1

        # Find children of container
        children = list(
            Location.objects.filter(
                project_id=self.project_id, parent_location=container
            )
        )

        # Prefer explicit preferred_hubs
        hub = None
        hub_candidates = [c for c in children]
        if preferred_hubs:
            ph_lower = [p.lower() for p in preferred_hubs]
            for child in hub_candidates:
                nm = (child.name or "").lower()
                if any(p in nm for p in ph_lower):
                    hub = child
                    break

        # Keyword-based selection if not found
        if not hub:
            keywords = [
                "living room",
                "hallway",
                "lobby",
                "foyer",
                "main hall",
                "town square",
            ]
            for kw in keywords:
                for child in hub_candidates:
                    if kw in (child.name or "").lower():
                        hub = child
                        break
                if hub:
                    break

        # Most connected child fallback
        if not hub and hub_candidates:
            hub = max(hub_candidates, key=lambda x: degree.get(str(x.id), 0))

        # Optionally create a simple hub if none exists
        created_hub = False
        if not hub and auto_create_hub:
            hub = Location.objects.create(
                project_id=self.project_id,
                name="Hallway",
                description="A central corridor connecting rooms.",
                location_type="residential",
                parent_location=container,
                relative_x=0.0,
                relative_y=0.0,
            )
            created_hub = True

        if not hub:
            return {
                "success": False,
                "needs_input": True,
                "error": f"No interior hub found for container '{container.name}'.",
                "suggestion": "Specify an interior hub (e.g., Living Room/Hallway), or set auto_create_hub=true.",
                "room_id": str(room.id),
                "container_id": str(container.id),
            }

        # Nest room under container (preserve or set)
        if room.parent_location_id != container.id:
            room.parent_location = container
            # keep relative position defaulting to current absolute
            room.relative_x = room.canvas_x
            room.relative_y = room.canvas_y
            room.save()

        # In simplified navigation: set entry_from for unidirectional connections
        # Room can be entered from hub
        if not room.entry_from:
            room.entry_from = hub
            room.save(update_fields=["entry_from", "updated_at"])

        # If hub doesn't have entry_from set, set it to container
        if not hub.entry_from:
            hub.entry_from = container
            hub.save(update_fields=["entry_from", "updated_at"])

        # Validate graph and return
        validation = self.validate_world_graph()

        return {
            "success": True,
            "created_room": created_room,
            "created_hub": created_hub,
            "container_id": str(container.id),
            "hub_id": str(hub.id),
            "room_id": str(room.id),
            "issues": validation.get("issues", []),
            "message": f"Placed '{room.name}' inside '{container.name}' via hub '{hub.name}'.",
        }

    @transaction.atomic
    def delete_location(self, location_id: str, cascade: bool = True, dry_run: bool = False, force: bool = False) -> dict:
        """Delete a location and handle all dependencies safely.

        Args:
            location_id: UUID or name of location to delete
            cascade: If True, delete child locations (default: True)
            dry_run: If True, return what would be deleted without actually deleting
            force: If True, allow deletion of starting locations and other protected items

        Returns:
            dict: Success status, affected items, and messages
        """
        start_time = time.time()
        Location = self.models.get("Location")
        StoryCanvasTrigger = self.models.get("StoryCanvasTrigger")

        if not Location:
            return {"success": False, "error": "Location model unavailable"}

        try:
            # Resolve location by ID or name
            if uuid_like(location_id):
                location = Location.objects.get(pk=location_id, project_id=self.project_id)
            else:
                location = Location.objects.get(name=location_id, project_id=self.project_id)

        except Location.DoesNotExist:
            return {"success": False, "error": f"Location not found: {location_id}"}

        # Collect what will be affected
        affected_items = {
            "location": {"id": str(location.id), "name": location.name},
            "child_locations": [],
            "cleared_entry_connections": [],
            "cleared_default_entries": [],
            "affected_story_canvases": []
        }

        # Check for protection (starting locations, etc.)
        if location.is_starting_location and not force:
            return {
                "success": False,
                "error": f"Cannot delete starting location '{location.name}' without force=True"
            }

        # Find child locations (will be cascade deleted if cascade=True)
        child_locations = list(Location.objects.filter(
            parent_location=location, project_id=self.project_id
        ))

        if child_locations and not cascade:
            child_names = [loc.name for loc in child_locations]
            return {
                "success": False,
                "error": f"Location '{location.name}' has child locations: {child_names}. Use cascade=True to delete them."
            }

        for child in child_locations:
            affected_items["child_locations"].append({
                "id": str(child.id), "name": child.name
            })

        # Find locations that have entry_from pointing to this location
        entry_referencing_locations = list(Location.objects.filter(
            entry_from=location, project_id=self.project_id
        ))

        for entry_loc in entry_referencing_locations:
            affected_items["cleared_entry_connections"].append({
                "id": str(entry_loc.id),
                "name": entry_loc.name,
                "type": "entry_from"
            })

        # Find containers that have this as default_entry_location
        default_entry_containers = list(Location.objects.filter(
            default_entry_location=location, project_id=self.project_id
        ))

        for container in default_entry_containers:
            affected_items["cleared_default_entries"].append({
                "id": str(container.id),
                "name": container.name,
                "type": "default_entry"
            })

        # Find story canvas triggers at this location
        if StoryCanvasTrigger:
            story_triggers = list(StoryCanvasTrigger.objects.filter(
                location_id=location.id
            ))

            for trigger in story_triggers:
                affected_items["affected_story_canvases"].append({
                    "trigger_id": str(trigger.id),
                    "canvas_id": str(trigger.canvas_id)
                })

        # If dry_run, return what would be affected
        if dry_run:
            return {
                "success": True,
                "dry_run": True,
                "affected_items": affected_items,
                "message": f"Dry run: Would delete location '{location.name}' and {len(affected_items['child_locations'])} child locations"
            }

        # Perform the actual deletion
        try:
            # Clear entry_from references pointing to this location
            for entry_loc in entry_referencing_locations:
                entry_loc.entry_from = None
                entry_loc.save(update_fields=["entry_from"])

            # Clear default_entry_location references pointing to this location
            for container in default_entry_containers:
                container.default_entry_location = None
                container.save(update_fields=["default_entry_location"])

            # Clear story canvas triggers
            if StoryCanvasTrigger:
                for trigger in story_triggers:
                    trigger.location_id = None
                    trigger.save(update_fields=["location_id"])

            # Delete the location (child locations will cascade automatically)
            location.delete()

            # Log the operation
            if self.logger:
                duration_ms = (time.time() - start_time) * 1000
                self.logger.log_structured(
                    "info", "tools", "delete_location",
                    location_name=location.name,
                    children_deleted=len(child_locations),
                    connections_cleared=len(entry_referencing_locations) + len(default_entry_containers),
                    duration_ms=duration_ms
                )

            return {
                "success": True,
                "affected_items": affected_items,
                "message": f"Deleted location '{location.name}' and {len(child_locations)} child locations"
            }

        except Exception as e:
            if self.logger:
                duration_ms = (time.time() - start_time) * 1000
                self.logger.log_structured(
                    "error", "tools", "delete_location_failed",
                    location_name=location.name,
                    error=str(e),
                    duration_ms=duration_ms
                )
            return {
                "success": False,
                "error": f"Failed to delete location '{location.name}': {str(e)}"
            }

    @transaction.atomic
    def clear_all_connections(self, location_id: str, dry_run: bool = False) -> dict:
        """Clear all navigation connections for a location.

        Args:
            location_id: UUID or name of location to clear connections for
            dry_run: If True, return what would be cleared without actually clearing

        Returns:
            dict: Success status and details of cleared connections
        """
        start_time = time.time()
        Location = self.models.get("Location")

        if not Location:
            return {"success": False, "error": "Location model unavailable"}

        try:
            # Resolve location by ID or name
            if uuid_like(location_id):
                location = Location.objects.get(pk=location_id, project_id=self.project_id)
            else:
                location = Location.objects.get(name=location_id, project_id=self.project_id)

        except Location.DoesNotExist:
            return {"success": False, "error": f"Location not found: {location_id}"}

        # Collect what will be cleared
        cleared_connections = []

        # Check current entry_from
        if location.entry_from:
            cleared_connections.append({
                "type": "entry_from",
                "from": location.entry_from.name,
                "to": location.name
            })

        # Check if this location is used as entry_from by others
        locations_entering_from_here = list(Location.objects.filter(
            entry_from=location, project_id=self.project_id
        ))

        for loc in locations_entering_from_here:
            cleared_connections.append({
                "type": "clear_entry_from",
                "from": location.name,
                "to": loc.name
            })

        # Check if this location is a default_entry for containers
        if location.default_for_container.exists():
            for container in location.default_for_container.all():
                if container.project_id == self.project_id:
                    cleared_connections.append({
                        "type": "default_entry",
                        "container": container.name,
                        "entry": location.name
                    })

        # Check if this location has a default_entry_location
        if location.default_entry_location:
            cleared_connections.append({
                "type": "clear_default_entry",
                "container": location.name,
                "entry": location.default_entry_location.name
            })

        # If dry_run, return what would be cleared
        if dry_run:
            return {
                "success": True,
                "dry_run": True,
                "cleared_connections": cleared_connections,
                "message": f"Dry run: Would clear {len(cleared_connections)} connections for '{location.name}'"
            }

        # Perform the actual clearing
        try:
            # Clear this location's entry_from
            if location.entry_from:
                location.entry_from = None
                location.save(update_fields=["entry_from"])

            # Clear entry_from references pointing to this location
            for loc in locations_entering_from_here:
                loc.entry_from = None
                loc.save(update_fields=["entry_from"])

            # Clear default_entry references (both ways)
            if location.default_entry_location:
                location.default_entry_location = None
                location.save(update_fields=["default_entry_location"])

            for container in location.default_for_container.filter(project_id=self.project_id):
                container.default_entry_location = None
                container.save(update_fields=["default_entry_location"])

            # Log the operation
            if self.logger:
                duration_ms = (time.time() - start_time) * 1000
                self.logger.log_structured(
                    "info", "tools", "clear_all_connections",
                    location_name=location.name,
                    connections_cleared=len(cleared_connections),
                    duration_ms=duration_ms
                )

            return {
                "success": True,
                "cleared_connections": cleared_connections,
                "message": f"Cleared {len(cleared_connections)} connections for '{location.name}'"
            }

        except Exception as e:
            if self.logger:
                duration_ms = (time.time() - start_time) * 1000
                self.logger.log_structured(
                    "error", "tools", "clear_all_connections_failed",
                    location_name=location.name,
                    error=str(e),
                    duration_ms=duration_ms
                )
            return {
                "success": False,
                "error": f"Failed to clear connections for '{location.name}': {str(e)}"
            }


# -----------------------------
# WORLD DESIGNER - Unified Batch Operations
# -----------------------------


class WorldDesigner:
    """Unified world designer with declarative batch operations for atomic world building."""

    # Class-level session cache to persist entity IDs across operations
    _session_cache = {}
    _cache_timestamp = {}
    CACHE_TIMEOUT_MINUTES = 30  # How long to keep session cache

    def __init__(
        self, project_id: str, models: dict[str, Any], logger: EloraSessionLogger = None
    ):
        self.project_id = project_id
        self.models = models
        self.logger = logger
        self.elora_tools = EloraTools(project_id, models, logger)
        self.id_map = {}  # Track created entities for current batch

        # Initialize session cache for this project if not exists
        if self.project_id not in self._session_cache:
            self._session_cache[self.project_id] = {}
            self._cache_timestamp[self.project_id] = time.time()

        if self.logger:
            self.logger.log_structured(
                "info", "world_designer", "init", project_id=project_id
            )

    @transaction.atomic
    def execute_operations(self, operations: list[dict]) -> dict:
        """Execute batch world operations atomically.

        All operations succeed together or all fail together.
        Supports @ references to entities created in the same batch.
        """
        start_time = time.time()
        results = []
        self.id_map = {}  # Reset for each batch

        if self.logger:
            self.logger.log_structured(
                "info",
                "world_designer",
                "execute_operations_start",
                operations_count=len(operations),
            )

        try:
            for i, op in enumerate(operations):
                op_start_time = time.time()

                if self.logger:
                    self.logger.log_structured(
                        "debug",
                        "world_designer",
                        "operation_start",
                        operation_index=i,
                        operation=op,
                    )

                result = self._execute_single_operation(op)
                results.append(result)

                # Check if this operation failed - if so, rollback entire batch
                if not result.get("success", False):
                    failed_op_error = result.get("error", "Unknown operation failure")
                    raise Exception(f"Operation {i+1} failed: {failed_op_error}")

                if self.logger:
                    op_duration_ms = (time.time() - op_start_time) * 1000
                    success = result.get("success", False)
                    level = "info" if success else "warning"
                    self.logger.log_structured(
                        level,
                        "world_designer",
                        "operation_complete",
                        operation_index=i,
                        success=success,
                        duration_ms=op_duration_ms,
                    )

            duration_ms = (time.time() - start_time) * 1000
            success_result = {
                "success": True,
                "results": results,
                "created_ids": self.id_map,
                "operations_count": len(operations),
                "message": f"Successfully executed {len(operations)} operations",
            }

            if self.logger:
                self.logger.log_structured(
                    "info",
                    "world_designer",
                    "execute_operations_success",
                    operations_count=len(operations),
                    duration_ms=duration_ms,
                    created_ids_count=len(self.id_map),
                )

            return success_result

        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            error_result = {
                "success": False,
                "error": str(e),
                "failed_at_operation": i,
                "failed_operation": op,
                "partial_results": results[:i],
                "message": f"Failed at operation {i}: {str(e)}",
            }

            if self.logger:
                self.logger.log_error(
                    e,
                    context="world_designer_execute_operations",
                    failed_at_operation=i,
                    failed_operation=op,
                )
                self.logger.log_structured(
                    "error",
                    "world_designer",
                    "execute_operations_failed",
                    operations_count=len(operations),
                    failed_at_operation=i,
                    duration_ms=duration_ms,
                )

            return error_result

    def _execute_single_operation(self, op: dict) -> dict:
        """Route operation to appropriate handler."""
        op_type = op.get("op")

        handlers = {
            # Read operations
            "get": self._handle_get,
            "list": self._handle_list,
            "search": self._handle_search,
            "validate": self._handle_validate,
            # Write operations
            "create": self._handle_create,
            "nest": self._handle_nest,
            "place_in_container": self._handle_place_in_container,
            "create_from_template": self._handle_template,
            # Navigation operations (new LLM-friendly names)
            "set_entry_from": self._handle_set_entry_from,
            "clear_entry_from": self._handle_clear_entry_from,
            "set_default_entry": self._handle_set_default_entry,
            # Legacy navigation operations (deprecated but still work)
            "set_exit": self._handle_set_exit,  # Legacy: use "set_entry_from" instead
            "add_entry": self._handle_add_entry,  # Legacy: use "set_entry_from" instead
            "remove_entry": self._handle_remove_entry,  # Legacy: use "clear_entry_from" instead
            # Update/Delete (not fully implemented)
            "update": self._handle_update,
            "delete": self._handle_delete,
        }

        handler = handlers.get(op_type)
        if not handler:
            available_ops = ", ".join(handlers.keys())
            error_msg = f"Unknown operation type: '{op_type}'. Available operations: {available_ops}"
            if self.logger:
                self.logger.log_structured(
                    "error",
                    "world_designer",
                    "unknown_operation",
                    operation_type=op_type,
                    available_operations=list(handlers.keys()),
                )
            raise ValueError(error_msg)

        try:
            result = handler(op)

            # Log successful operations for debugging
            if self.logger and result.get("success", True):
                self.logger.log_structured(
                    "debug",
                    "world_designer",
                    "operation_success",
                    operation_type=op_type,
                    operation=op,
                )
            return result
        except Exception as e:
            # Add context to errors for better debugging
            if self.logger:
                self.logger.log_structured(
                    "error",
                    "world_designer",
                    "operation_error",
                    operation_type=op_type,
                    operation=op,
                    error=str(e),
                )
            # Re-raise with more context
            raise ValueError(f"Failed to execute {op_type} operation: {str(e)}") from e

    def _handle_create(self, op: dict) -> dict:
        """Handle creation operations for locations, containers, and canvases."""
        entity_type = op.get("type")
        data = op.get("data", {})

        # Resolve references in data
        data = self._resolve_references_in_dict(data)

        if entity_type == "location":
            result = self.elora_tools.create_location(
                name=data.get("name"),
                description=data.get("description", ""),
                location_type=data.get("location_type", "generic"),
            )
            if result.get("success"):
                location_name = data["name"]
                location_id = result["location_id"]

                # Add to current batch map
                self.id_map[location_name] = location_id

                # Add to session cache for cross-operation reference
                self._session_cache[self.project_id][location_name] = location_id
                self._cache_timestamp[self.project_id] = time.time()

                if self.logger:
                    self.logger.log_structured(
                        "info",
                        "world_designer",
                        "location_created",
                        name=location_name,
                        id=location_id,
                    )
            return result

        elif entity_type == "container":
            # Create location and mark as container
            result = self.elora_tools.create_location(
                name=data.get("name"),
                description=data.get("description", ""),
                location_type=data.get("container_type", "district"),
            )
            if result.get("success"):
                container_name = data["name"]
                container_id = result["location_id"]

                # Add to current batch map
                self.id_map[container_name] = container_id

                # Add to session cache for cross-operation reference
                self._session_cache[self.project_id][container_name] = container_id
                self._cache_timestamp[self.project_id] = time.time()

                # Mark as container
                self.elora_tools.make_container(container_id, True)

                if self.logger:
                    self.logger.log_structured(
                        "info",
                        "world_designer",
                        "container_created",
                        name=container_name,
                        id=container_id,
                    )

                # Auto-create interior hub if specified
                if data.get("auto_hub"):
                    hub_name = data.get("hub_name", f"{data['name']} Main Area")
                    hub_result = self.elora_tools.create_location(
                        name=hub_name,
                        description="Central hub area",
                        location_type="hub",
                    )
                    if hub_result.get("success"):
                        hub_id = hub_result["location_id"]
                        self.id_map[hub_name] = hub_id
                        self.elora_tools.nest_location(hub_id, loc_id)
                        # Set up bidirectional entry connections between container and hub
                        self.elora_tools.add_entry_connection(loc_id, hub_id)
                        self.elora_tools.add_entry_connection(hub_id, loc_id)
                        # Set hub as default entry for the container
                        self.elora_tools.set_default_entry_location(loc_id, hub_id)
                        result["hub_created"] = hub_name
                        result["hub_id"] = hub_id
            return result

        elif entity_type == "canvas":
            # Handle story canvas creation
            location_id = self._resolve_reference(data.get("location", ""))
            result = self.elora_tools.create_story_canvas(
                name=data.get("name"),
                location_id=location_id,
                content_blocks=data.get("content_blocks", []),
                description=data.get("description", ""),
                schedules=data.get("schedules"),
            )
            if result.get("success"):
                self.id_map[data["name"]] = result["canvas_id"]
            return result

        else:
            raise ValueError(f"Unknown entity type: {entity_type}")

    def _handle_nest(self, op: dict) -> dict:
        """Handle nesting operations (parent-child relationships)."""
        data = op.get("data", {})

        child_id = self._resolve_reference(data.get("child"))
        parent_id = self._resolve_reference(data.get("parent"))

        return self.elora_tools.nest_location(
            location_id=child_id,
            container_id=parent_id,
            relative_x=data.get("relative_x"),
            relative_y=data.get("relative_y"),
        )

    def _handle_place_in_container(self, op: dict) -> dict:
        """Handle smart placement of room in container."""
        data = op.get("data", {})

        container_ref = self._resolve_reference(data.get("container"))
        room_ref = self._resolve_reference(data.get("room"))

        # Get room name for smart_place_room
        room_name = data.get("room_name")
        if not room_name and room_ref in self.id_map.values():
            # Find the name from id_map
            for name, id_val in self.id_map.items():
                if id_val == room_ref:
                    room_name = name
                    break

        if not room_name:
            room_name = f"Room_{room_ref[:8]}"

        return self.elora_tools.smart_place_room(
            container_identifier=container_ref,
            room_name=room_name,
            room_description=data.get("description", ""),
            preferred_hubs=data.get("preferred_hubs"),
            auto_create_hub=data.get("auto_create_hub", False),
            bidirectional=data.get("bidirectional", True),
        )

    def _handle_get(self, op: dict) -> dict:
        """Handle get operations for single entities."""
        entity_type = op.get("type")
        identifier = op.get("id") or op.get("identifier") or op.get("name")

        # Resolve reference if needed
        if identifier:
            identifier = self._resolve_reference(identifier)

        if entity_type == "location":
            return self.elora_tools.get_location(identifier)
        elif entity_type == "canvas":
            return self.elora_tools.get_story_canvas(identifier)
        elif entity_type == "connection":
            return self.elora_tools.get_connection(identifier)
        elif entity_type == "neighbors":
            return self.elora_tools.get_neighbors(identifier)
        else:
            raise ValueError(f"Unknown entity type for get: {entity_type}")

    def _handle_list(self, op: dict) -> dict:
        """Handle list operations for multiple entities."""
        entity_type = op.get("type")

        if entity_type == "locations":
            query = op.get("query", "")
            return self.elora_tools.list_locations(query)
        elif entity_type == "canvases":
            query = op.get("query", "")
            location_id = op.get("location_id", "")
            if location_id:
                location_id = self._resolve_reference(location_id)
            return self.elora_tools.list_story_canvases(query, location_id)
        elif entity_type == "connections":
            location_id = op.get("location_id", "")
            if location_id:
                location_id = self._resolve_reference(location_id)
            return self.elora_tools.list_connections(location_id)
        else:
            raise ValueError(f"Unknown entity type for list: {entity_type}")

    def _handle_search(self, op: dict) -> dict:
        """Handle search operations with fuzzy matching."""
        query = op.get("query", "")
        entity_type = op.get("type", "any")

        # For now, use list with query as search
        # Could be enhanced with fuzzy matching in the future
        if entity_type == "locations" or entity_type == "any":
            return self.elora_tools.list_locations(query)
        elif entity_type == "canvases":
            return self.elora_tools.list_story_canvases(query)
        else:
            return {
                "success": False,
                "error": f"Search not implemented for type: {entity_type}",
            }

    def _handle_validate(self, op: dict) -> dict:
        """Handle validation operations."""
        target = op.get("target", "project")

        if target == "project":
            return self.elora_tools.validate_project()
        elif target == "world_graph" or target == "graph":
            return self.elora_tools.validate_world_graph()
        elif target == "navigation_rules" or target == "navigation":
            return self.elora_tools.validate_navigation_rules()
        else:
            raise ValueError(
                f"Unknown validation target: {target}. Valid targets: project, world_graph, navigation_rules"
            )

    def _handle_update(self, op: dict) -> dict:
        """Handle update operations (not fully implemented yet)."""
        # This would update existing entities
        return {"success": False, "error": "Update operations not yet implemented"}

    def _handle_delete(self, op: dict) -> dict:
        """Handle delete operations for locations and connections."""
        target_type = op.get("type", "location")
        data = op.get("data", {})

        if target_type == "location":
            # Delete a location with optional parameters
            location_id = self._resolve_reference(data.get("location") or data.get("id"))
            if not location_id:
                return {"success": False, "error": "Missing required 'location' or 'id' field"}

            cascade = data.get("cascade", True)  # Default to cascade delete
            dry_run = data.get("dry_run", False)
            force = data.get("force", False)

            return self.elora_tools.delete_location(
                location_id=location_id,
                cascade=cascade,
                dry_run=dry_run,
                force=force
            )

        elif target_type == "connections":
            # Clear all connections for a location
            location_id = self._resolve_reference(data.get("location") or data.get("id"))
            if not location_id:
                return {"success": False, "error": "Missing required 'location' or 'id' field"}

            dry_run = data.get("dry_run", False)

            return self.elora_tools.clear_all_connections(
                location_id=location_id,
                dry_run=dry_run
            )

        else:
            return {
                "success": False,
                "error": f"Unknown delete type: '{target_type}'. Supported types: 'location', 'connections'"
            }

    def _handle_template(self, op: dict) -> dict:
        """Expand and execute template operations."""
        template_name = op.get("template")
        variant = op.get("variant", "small")
        params = op.get("params", {})

        # Get template operations
        template_ops = self._get_template_operations(template_name, variant, params)

        # Execute all template operations
        results = []
        for template_op in template_ops:
            result = self._execute_single_operation(template_op)
            results.append(result)

        return {
            "template": template_name,
            "variant": variant,
            "operations_executed": len(results),
            "results": results,
        }

    def _get_template_operations(
        self, template: str, variant: str, params: dict
    ) -> list[dict]:
        """Get operations for a template."""
        if template == "neighborhood":
            return self._generate_neighborhood_ops(
                params.get("name", "Neighborhood"), variant, params
            )
        elif template == "building":
            return self._generate_building_ops(
                params.get("name", "Building"), params.get("building_type", "house")
            )
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_neighborhood_ops(
        self, name: str, size: str, params: dict
    ) -> list[dict]:
        """Generate operations for a neighborhood template."""
        ops = []

        # Create container with auto hub
        ops.append(
            {
                "op": "create",
                "type": "container",
                "data": {
                    "name": name,
                    "container_type": "neighborhood",
                    "auto_hub": True,
                    "hub_name": f"{name} Main Street",
                },
            }
        )

        # Add houses based on size
        house_count = {"small": 3, "medium": 6, "large": 10}.get(size, 3)
        for i in range(1, house_count + 1):
            house_name = f"{name} House {i}"
            ops.append(
                {
                    "op": "create",
                    "type": "location",
                    "data": {
                        "name": house_name,
                        "location_type": "residential",
                        "description": f"A cozy house in {name}",
                    },
                }
            )
            # Place house in neighborhood
            ops.append(
                {
                    "op": "place_in_container",
                    "data": {
                        "container": f"@{name}",
                        "room": f"@{house_name}",
                        "room_name": house_name,
                        "preferred_hubs": [f"{name} Main Street"],
                        "auto_create_hub": False,
                    },
                }
            )

        # Connect to existing location if specified (using entry/exit connections)
        if params.get("connect_to"):
            # Add bidirectional entry connections between neighborhood and target location
            ops.append(
                {
                    "op": "add_entry",
                    "data": {"from": f"@{name}", "to": params["connect_to"]},
                }
            )
            ops.append(
                {
                    "op": "add_entry",
                    "data": {"from": params["connect_to"], "to": f"@{name}"},
                }
            )

        return ops

    def _generate_building_ops(self, name: str, building_type: str) -> list[dict]:
        """Generate operations for a building template."""
        ops = []

        # Create building container
        ops.append(
            {
                "op": "create",
                "type": "container",
                "data": {
                    "name": name,
                    "container_type": "building",
                    "auto_hub": True,
                    "hub_name": "Hallway" if building_type == "house" else "Entrance",
                },
            }
        )

        # Add rooms based on building type
        if building_type == "house":
            rooms = ["Living Room", "Kitchen", "Bedroom", "Bathroom"]
        elif building_type == "shop":
            rooms = ["Storefront", "Storage Room", "Office"]
        elif building_type == "inn":
            rooms = ["Common Room", "Kitchen", "Guest Room 1", "Guest Room 2"]
        else:
            rooms = ["Main Room"]

        for room in rooms:
            room_full_name = f"{name} {room}"
            ops.append(
                {
                    "op": "create",
                    "type": "location",
                    "data": {
                        "name": room_full_name,
                        "location_type": "interior",
                        "description": f"{room} in {name}",
                    },
                }
            )
            ops.append(
                {
                    "op": "place_in_container",
                    "data": {
                        "container": f"@{name}",
                        "room": f"@{room_full_name}",
                        "room_name": room_full_name,
                        "auto_create_hub": False,
                    },
                }
            )

        return ops

    def _handle_set_exit(self, op: dict) -> dict:
        """Handle setting entry_from connection (simplified navigation system)."""
        data = op.get("data", {})

        from_location_id = self._resolve_reference(data.get("from"))
        to_location_id = self._resolve_reference(data.get("to"))

        return self.elora_tools.set_entry_from(to_location_id, from_location_id)

    def _handle_add_entry(self, op: dict) -> dict:
        """Handle adding entry connection between locations."""
        data = op.get("data", {})

        from_location_id = self._resolve_reference(data.get("from"))
        to_location_id = self._resolve_reference(data.get("to"))

        return self.elora_tools.add_entry_connection(from_location_id, to_location_id)

    def _handle_remove_entry(self, op: dict) -> dict:
        """Handle removing entry connection between locations."""
        data = op.get("data", {})

        from_location_id = self._resolve_reference(data.get("from"))
        to_location_id = self._resolve_reference(data.get("to"))

        return self.elora_tools.remove_entry_connection(
            from_location_id, to_location_id
        )

    def _handle_set_default_entry(self, op: dict) -> dict:
        """Handle setting default entry location for a container."""
        data = op.get("data", {})

        container_id = self._resolve_reference(data.get("container"))
        entry_location_id = self._resolve_reference(data.get("entry"))

        return self.elora_tools.set_default_entry_location(
            container_id, entry_location_id
        )

    def _handle_set_entry_from(self, op: dict) -> dict:
        """Handle setting entry_from connection (LLM-friendly naming)."""
        data = op.get("data", {})

        location_id = self._resolve_reference(data.get("location"))
        from_location_id = self._resolve_reference(data.get("from"))

        return self.elora_tools.set_entry_from(location_id, from_location_id)

    def _handle_clear_entry_from(self, op: dict) -> dict:
        """Handle clearing entry_from connection (LLM-friendly naming)."""
        data = op.get("data", {})

        location_id = self._resolve_reference(data.get("location"))

        return self.elora_tools.set_entry_from(location_id, None)

    def _is_valid_uuid(self, value: str) -> bool:
        """Check if a string is a valid UUID."""
        try:
            uuid.UUID(str(value))
            return True
        except (ValueError, TypeError):
            return False

    def _clean_expired_cache(self):
        """Clean expired entries from session cache."""
        current_time = time.time()
        timeout_seconds = self.CACHE_TIMEOUT_MINUTES * 60

        for project_id in list(self._cache_timestamp.keys()):
            if current_time - self._cache_timestamp[project_id] > timeout_seconds:
                if project_id in self._session_cache:
                    del self._session_cache[project_id]
                del self._cache_timestamp[project_id]

    def _resolve_reference(self, ref: str) -> str:
        """Convert references to UUIDs - supports UUIDs, @names, and plain names."""
        if not ref:
            return ref

        # Clean expired cache entries
        self._clean_expired_cache()

        # Remove @ prefix if present
        lookup_name = ref[1:] if ref.startswith("@") else ref

        # Check if it's already a valid UUID
        if self._is_valid_uuid(ref):
            return ref

        # Check if it's in the current batch's created entities
        if lookup_name in self.id_map:
            return self.id_map[lookup_name]

        # Check session cache for recently created entities (fallback for separate calls)
        session_cache = self._session_cache.get(self.project_id, {})
        if lookup_name in session_cache:
            cached_id = session_cache[lookup_name]
            if self.logger:
                self.logger.log_structured(
                    "info",
                    "world_designer",
                    "reference_resolved_from_cache",
                    reference=ref,
                    resolved_id=cached_id,
                )
            return cached_id

        # Try to find existing location by name
        locations = self.elora_tools.list_locations(lookup_name)
        if locations.get("locations") and len(locations["locations"]) > 0:
            # Look for exact match first
            for loc in locations["locations"]:
                if loc["name"] == lookup_name:
                    return loc["id"]
            # If no exact match, use first result
            return locations["locations"][0]["id"]

        # Provide helpful error message
        raise ValueError(
            f"Could not resolve reference '{ref}'. "
            f"Expected: UUID, location name, or @name reference. "
            f"Location '{lookup_name}' not found in project."
        )

    def _resolve_references_in_dict(self, data: dict, skip_fields=None) -> dict:
        """Recursively resolve all references in a dictionary, except for specified fields."""
        if skip_fields is None:
            # These fields contain literal values, not references
            skip_fields = {
                "name",
                "description",
                "location_type",
                "container_type",
                "connection_type",
                "template",
                "variant",
                "line_style",
                "line_color",
                "arrow_style",
            }

        resolved = {}
        for key, value in data.items():
            if key in skip_fields:
                # Don't resolve references for these fields - they're literal values
                resolved[key] = value
            elif isinstance(value, str):
                resolved[key] = self._resolve_reference(value)
            elif isinstance(value, dict):
                resolved[key] = self._resolve_references_in_dict(value, skip_fields)
            elif isinstance(value, list):
                resolved[key] = [
                    self._resolve_reference(v) if isinstance(v, str) else v
                    for v in value
                ]
            else:
                resolved[key] = value
        return resolved


# -----------------------------
# TOOL DECORATORS FOR LANGGRAPH
# -----------------------------


def create_tools(
    project_id: str, models: dict[str, Any], logger: EloraSessionLogger = None
) -> list:
    """Create LangChain tools for the ReAct agent."""

    # Create tools instance
    tools_instance = EloraTools(project_id, models, logger)

    @tool
    def list_locations(query: str = "") -> dict:
        """List locations in the project, optionally filtered by name.

        Args:
            query: Optional search query to filter locations by name

        Returns:
            Dictionary with success status, count, and list of locations
        """
        return tools_instance.list_locations(query)

    @tool
    def get_location(identifier: str) -> dict:
        """Get specific location details by ID or name.

        Args:
            identifier: Location ID (UUID) or name to search for

        Returns:
            Dictionary with location details or error message
        """
        return tools_instance.get_location(identifier)

    @tool
    def create_location(
        name: str, description: str = "", location_type: str = "generic"
    ) -> dict:
        """Create a new location in the project.

        Args:
            name: Location name (must be unique within project)
            description: Optional description of the location
            location_type: Type of location (generic, residential, commercial, etc.)

        Returns:
            Dictionary with creation status and location ID
        """
        return tools_instance.create_location(name, description, location_type)

    @tool
    def list_story_canvases(query: str = "", location_id: str = "") -> dict:
        """List story canvases, optionally filtered by query or location.

        Args:
            query: Optional search query to filter canvases by name
            location_id: Optional location ID to filter canvases by trigger location

        Returns:
            Dictionary with success status, count, and list of canvases
        """
        return tools_instance.list_story_canvases(query, location_id)

    @tool
    def get_story_canvas(identifier: str) -> dict:
        """Get story canvas with full content, trigger, and schedule info.

        Args:
            identifier: Canvas ID (UUID) or name to search for

        Returns:
            Dictionary with canvas details including content blocks and triggers
        """
        return tools_instance.get_story_canvas(identifier)

    @tool
    def create_story_canvas(
        name: str,
        location_id: str,
        content_blocks: list,
        description: str = "",
        schedules: list | None = None,
    ) -> dict:
        """Create story canvas with single node, location trigger, and optional schedules.

        Args:
            name: Canvas name (must be unique within project)
            location_id: UUID of location that triggers this canvas
            content_blocks: List of blocks with allowed types only:
                - paragraph: {"type": "paragraph", "content": "..."}
                - heading: {"type": "heading", "content": "...", "props": {"level": 1|2|3}}
                The system will convert simple blocks to rich format and enforce heading level.
            description: Optional canvas description
            schedules: Optional list of schedules to attach to the trigger. Each item must include:
                - name: str
                - weekdays: list[int] where 0=Monday .. 6=Sunday
                - start_time: "HH:MM" format (e.g., "09:00")
                - end_time: Optional "HH:MM" format (e.g., "18:00", must be after start_time)

        Returns:
            Dictionary with creation status, canvas ID, node ID, trigger ID, and created schedules
        """
        return tools_instance.create_story_canvas(
            name, location_id, content_blocks, description, schedules
        )

    @tool
    def generate_game_twee() -> dict:
        """Generate twee content for the entire project using twee_comprehensive system.

        Returns:
            Dictionary with generation status and twee content length
        """
        return tools_instance.generate_game_twee()

    @tool
    def validate_project() -> dict:
        """Validate project readiness for game generation.

        Returns:
            Dictionary with validation status, statistics, and any issues found
        """
        return tools_instance.validate_project()

    @tool
    def validate_world_graph() -> dict:
        """Validate world graph for basic issues (isolates, cross-project edges)."""
        return tools_instance.validate_world_graph()

    @tool
    def validate_navigation_rules() -> dict:
        """Validate navigation consistency rules (container defaults, entry_from consistency)."""
        return tools_instance.validate_navigation_rules()

    @tool
    def get_world_graph() -> dict:
        """Get a read-only snapshot of the world graph (nodes, edges, degrees, containers, components)."""
        return tools_instance.get_world_graph()

    @tool
    def make_container(location_id: str, is_container: bool = True) -> dict:
        """Mark or unmark a location as a container."""
        return tools_instance.make_container(location_id, is_container)

    @tool
    def nest_location(
        location_id: str,
        container_id: str,
        relative_x: float | None = None,
        relative_y: float | None = None,
    ) -> dict:
        """Nest a location into a container and set relative position."""
        return tools_instance.nest_location(
            location_id, container_id, relative_x, relative_y
        )

    @tool
    def smart_place_room(
        container_identifier: str,
        room_name: str,
        room_description: str = "",
        preferred_hubs: list[str] | None = None,
        auto_create_hub: bool = False,
        bidirectional: bool = True,
    ) -> dict:
        """Place a room inside a container: ensure container, nest, connect via one-way entry_from.

        Args:
            container_identifier: Container UUID or exact name
            room_name: Name of the room to create or use
            room_description: Optional description for room creation
            preferred_hubs: Optional list of hub names to prefer (case-insensitive contains)
            auto_create_hub: If True, creates a 'Hallway' hub if none found
            bidirectional: Deprecated/ignored in single-inbound model. Kept for compatibility; no reverse links are created.

        Returns:
            Dictionary with created/selected container, hub, room IDs and validation issues
        """
        return tools_instance.smart_place_room(
            container_identifier,
            room_name,
            room_description,
            preferred_hubs,
            auto_create_hub,
            bidirectional,
        )

    @tool
    def execute_world_operations(operations: list[dict]) -> dict:
        """Execute ANY world operations - read, write, validate - all in one tool.

        IMPORTANT: This tool requires ONE parameter named 'operations' containing a list of operation dictionaries.

        This is the UNIVERSAL tool for ALL world-related tasks.
        Supports batching, @ references, and atomic execution for writes.

        Parameter structure:
        - operations: List of operation dictionaries (REQUIRED parameter name)
          Each operation dict contains: "op" (operation type) and additional fields

        READ Operations:
        - get: Get single entity {"op": "get", "type": "location", "id": "name-or-uuid"}
        - list: List entities {"op": "list", "type": "locations", "query": "optional"}
        - search: Search with fuzzy match {"op": "search", "query": "term", "type": "locations"}
        - validate: Check world {"op": "validate", "target": "world_graph|navigation_rules"}

        WRITE Operations:
        - create: Create entities {"op": "create", "type": "location|container|canvas", "data": {...}}
        - nest: Parent-child {"op": "nest", "data": {"child": "@Room", "parent": "@Building"}}
        - place_in_container: Smart placement {"op": "place_in_container", "data": {...}}
        - create_from_template: Use templates {"op": "create_from_template", "template": "neighborhood", ...}

        NAVIGATION Operations (single-inbound model):
        - set_entry_from: Set one-way entry_from {"op": "set_entry_from", "data": {"location": "@Room", "from": "@Hub"}}
          NOTES: Do not set entry_from on default entry locations; INSIDE locations cannot bypass container's default entry; OUTSIDE locations CAN connect to containers with default entries.
        - clear_entry_from: Remove entry_from {"op": "clear_entry_from", "data": {"location": "@Room"}}
        - set_default_entry: Set automatic container entry {"op": "set_default_entry", "data": {"container": "@House", "entry": "@LivingRoom"}}
          NOTE: Default entry locations must not have entry_from

        DELETE Operations:
        - delete location: Remove location and handle dependencies {"op": "delete", "type": "location", "data": {"location": "Park", "cascade": true, "dry_run": false, "force": false}}
          Options: cascade (delete children), dry_run (preview only), force (allow protected locations)
        - delete connections: Clear all navigation connections {"op": "delete", "type": "connections", "data": {"location": "Kitchen", "dry_run": false}}
          Clears entry_from, outgoing connections, and default_entry relationships

        LEGACY NAVIGATION (Deprecated - prefer names above):
        - set_exit/add_entry/remove_entry: Deprecated aliases for set_entry_from/clear_entry_from

        NAVIGATION LOGIC EXPLANATION:
        1. Default Entry: Containers with default entries are entered automatically through that location
           - Player enters "Home" → automatically goes to "Living Room" (if Living Room is default entry)
           - Default entries don't need entry_from relationships (automatic routing)
           - Containers with default entries cannot be entered via entry_from from other locations

        2. Direct Entry: Locations without default entries use entry_from for explicit connections
           - Used for direct location-to-location navigation
           - Cannot point to containers that have default entries

        3. Container Structure: Locations are nested in containers but navigation is separate
           - nest: Creates parent-child hierarchy (where things are)
           - entry_from/default_entry: Controls how players move between locations

        Examples (showing parameter name):
        # Mixed read and write operations
        operations=[{"op": "list", "type": "locations"},
                   {"op": "create", "type": "location", "data": {"name": "Park"}},
                   {"op": "get", "type": "neighbors", "id": "@Park"}]

        # Create neighborhood from template
        operations=[{"op": "create_from_template", "template": "neighborhood",
                    "variant": "small", "params": {"name": "Riverside"}}]

        # Discovery then creation with navigation (one-way)
        operations=[{"op": "search", "query": "Main", "type": "locations"},
                   {"op": "create", "type": "location", "data": {"name": "Park"}},
                   {"op": "set_entry_from", "data": {"location": "Main Street", "from": "@Park"}}]

        Args:
            operations: List of operation dictionaries (parameter name MUST be 'operations')

        Returns:
            Dictionary with success status, results, and any created IDs
        """
        designer = WorldDesigner(project_id, models, logger)
        return designer.execute_operations(operations)

    # Return list of tool functions
    # NOTE: ALL world operations now handled by execute_world_operations
    return [
        # UNIVERSAL WORLD TOOL - handles ALL world operations (read/write/validate)
        execute_world_operations,
        # Story/Canvas tools (kept separate as they're narrative-focused)
        create_story_canvas,
        # Game generation tool (final output)
        generate_game_twee,
        # All individual world tools REMOVED to avoid confusion
        # The execute_world_operations tool now handles:
        # - list_locations           → {"op": "list", "type": "locations"}
        # - get_location             → {"op": "get", "type": "location", "id": "..."}
        # - create_location          → {"op": "create", "type": "location", "data": {...}}
        # - smart_place_room         → {"op": "place_in_container", "data": {...}}
        # - make_container           → {"op": "create", "type": "container", "data": {...}}
        # - nest_location            → {"op": "nest", "data": {...}}
        # - set_entry_from           → {"op": "set_entry_from", "data": {"location": "...", "from": "..."}}
        # - add_entry_connection     → {"op": "set_entry_from", "data": {"location": "...", "from": "..."}}
        # - remove_entry_connection  → {"op": "clear_entry_from", "data": {"location": "..."}}
        # - set_default_entry        → {"op": "set_default_entry", "data": {"container": "...", "entry": "..."}}
        # - validate_project         → {"op": "validate", "target": "project"}
        # - validate_world_graph     → {"op": "validate", "target": "world_graph"}
        # - And more with templates, search, batch operations, etc.
    ]


# -----------------------------
# LANGGRAPH REACT AGENT
# -----------------------------


class EloraReActAgent:
    """LangGraph-powered ReAct agent for story creation."""

    def __init__(
        self,
        project_id: str,
        api_key: str,
        models: dict[str, Any],
        logger: EloraSessionLogger = None,
    ):
        self.project_id = project_id
        self.models = models
        self.logger = logger

        if self.logger:
            self.logger.log_structured(
                "info",
                "agent",
                "init_start",
                model_name="gpt-4o-mini",
                project_id=project_id,
            )

        # Create OpenAI model
        start_time = time.time()
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=api_key,
            temperature=0.2,
            max_tokens=1000,
        )

        if self.logger:
            duration_ms = (time.time() - start_time) * 1000
            self.logger.log_structured(
                "info", "agent", "llm_created", duration_ms=duration_ms
            )

        # Create tools
        start_time = time.time()
        self.tools = create_tools(project_id, models, logger)

        if self.logger:
            duration_ms = (time.time() - start_time) * 1000
            self.logger.log_structured(
                "info",
                "agent",
                "tools_created",
                tool_count=len(self.tools),
                duration_ms=duration_ms,
            )

        # Create ReAct agent using LangGraph
        start_time = time.time()
        self.agent = create_react_agent(
            model=self.llm, tools=self.tools, state_modifier=self._get_system_prompt()
        )

        if self.logger:
            duration_ms = (time.time() - start_time) * 1000
            self.logger.log_structured(
                "info", "agent", "react_agent_created", duration_ms=duration_ms
            )

    def _get_system_prompt(self) -> str:
        """Get comprehensive system prompt from modular components."""
        # Fix: Use correct path - need to go up 3 levels from commands/elora_cli.py to elora_simplified/
        prompts_dir = Path(__file__).parent.parent.parent / "prompts"

        try:
            from ...prompts.prompt_builder import PromptBuilder

            builder = PromptBuilder(prompts_dir)
            return builder.load_all_modules()
        except Exception as e:
            # Log the failure and raise error instead of falling back
            if self.logger:
                self.logger.log_structured(
                    "error", "prompt", "modular_load_failed",
                    error=str(e), prompts_dir=str(prompts_dir)
                )

            raise RuntimeError(
                f"Failed to load modular prompt system: {e}\n"
                f"Prompts directory: {prompts_dir}\n"
                f"Directory exists: {prompts_dir.exists()}"
            )

    def run(self, user_input: str, base_messages: list | None = None):
        """Execute ReAct loop for user input.

        Args:
            user_input: The primary user prompt
            base_messages: Optional list of prior messages to include (conversation state)
        Returns:
            Tuple of (final_text_response, final_message_obj)
        """
        start_time = time.time()

        if self.logger:
            self.logger.log_agent_operation(
                "run_start",
                details={
                    "user_input": user_input,
                    "base_messages_count": len(base_messages or []),
                },
            )

        try:
            # Create message and invoke agent
            messages = list(base_messages or [])
            messages.append(HumanMessage(content=user_input))

            if self.logger:
                self.logger.log_agent_operation(
                    "invoking_agent", details={"total_messages": len(messages)}
                )

            # Stream updates to show tool calls in real-time
            full_response = None
            for chunk in self.agent.stream(
                {"messages": messages}, stream_mode="updates"
            ):
                # Display tool calls as they happen
                self._display_tool_call(chunk)

                # Keep the last chunk as our final response
                full_response = chunk

            # Extract final response from the last chunk
            if full_response and "agent" in full_response:
                agent_data = full_response["agent"]
                if "messages" in agent_data and agent_data["messages"]:
                    final_message = agent_data["messages"][-1]
                    if hasattr(final_message, "content"):
                        result_text = final_message.content
                        result_message = final_message
                    else:
                        result_text = str(final_message)
                        result_message = final_message
                else:
                    # Fallback if no messages in agent data
                    result_text = "✅ Task completed"
                    result_message = AIMessage(content=result_text)
            else:
                # Fallback if no agent data
                result_text = "✅ Task completed"
                result_message = AIMessage(content=result_text)

            duration_ms = (time.time() - start_time) * 1000

            if self.logger:
                self.logger.log_agent_operation(
                    "run_success",
                    details={
                        "response_length": len(result_text),
                        "response_type": type(result_message).__name__,
                    },
                    duration_ms=duration_ms,
                )

            return result_text, result_message

        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            err = f"❌ Error: {str(e)}"

            if self.logger:
                self.logger.log_error(e, context="agent_run")
                self.logger.log_agent_operation(
                    "run_error", details={"error": str(e)}, duration_ms=duration_ms
                )

            return err, AIMessage(content=err)

    def _display_tool_call(self, chunk):
        """Display tool calls in real-time with a simple 2-line format.

        Enhanced to handle various chunk structures from LangGraph streaming.
        """
        try:
            # Handle different chunk structures from LangGraph streaming
            if not isinstance(chunk, dict):
                return

            # Look for agent or tools node updates (broadened from just "agent")
            for node_name, node_data in chunk.items():
                # Process various node types that might contain tool calls
                if node_name in [
                    "agent",
                    "tools",
                    "__start__",
                    "__end__",
                ] or isinstance(node_data, dict):
                    # Check for AI messages with tool calls
                    messages = node_data.get("messages", [])
                    for msg in messages:
                        if hasattr(msg, "tool_calls") and msg.tool_calls:
                            for tool_call in msg.tool_calls:
                                tool_name = tool_call.get("name", "unknown")
                                args = tool_call.get("args", {})

                                # Format key parameters (limit to 2-3 key ones)
                                param_parts = []
                                for key, value in list(args.items())[:3]:
                                    if isinstance(value, str) and len(value) > 30:
                                        value = value[:27] + "..."
                                    param_parts.append(f'{key}="{value}"')

                                params_str = ", ".join(param_parts)
                                if params_str:
                                    params_str = f" → {params_str}"

                                print(f"🔧 Tool: {tool_name}{params_str}")

                # Handle tool execution results (enhanced for broader coverage)
                if node_name == "tools" or "tool" in node_name.lower():
                    # Check for tool execution results
                    messages = node_data.get("messages", [])
                    for msg in messages:
                        if hasattr(msg, "content") and hasattr(msg, "tool_call_id"):
                            # This is a tool result message
                            content = msg.content

                            # Try to parse the result for a summary
                            status_icon = "✅"
                            result_summary = "Success"

                            try:
                                # Try to parse JSON result for better summary
                                if isinstance(content, str) and content.startswith("{"):
                                    import json

                                    result_data = json.loads(content)

                                    # Look for common result patterns
                                    # Check for success field first (handles {"success": false, "error": "..."} pattern)
                                    if (
                                        "success" in result_data
                                        and not result_data["success"]
                                    ):
                                        status_icon = "❌"
                                        result_summary = f"Error: {result_data.get('error', 'Operation failed')}"
                                    elif "error" in result_data:
                                        status_icon = "❌"
                                        result_summary = (
                                            f"Error: {result_data['error']}"
                                        )
                                    elif "count" in result_data:
                                        result_summary = f"{result_data['count']} items"
                                    elif "id" in result_data:
                                        result_summary = (
                                            f"ID: {str(result_data['id'])[:8]}..."
                                        )
                                    elif "status" in result_data:
                                        result_summary = result_data["status"]
                                    else:
                                        # Generic success with item count if available
                                        if (
                                            isinstance(result_data, dict)
                                            and len(result_data) > 0
                                        ):
                                            result_summary = "Success"
                                        else:
                                            result_summary = "No data"

                                elif isinstance(content, str):
                                    # Simple string result
                                    if (
                                        "error" in content.lower()
                                        or "failed" in content.lower()
                                    ):
                                        status_icon = "❌"
                                        result_summary = content[:200] + (
                                            "..." if len(content) > 200 else ""
                                        )
                                    else:
                                        result_summary = content[:200] + (
                                            "..." if len(content) > 200 else ""
                                        )

                            except (json.JSONDecodeError, KeyError, AttributeError):
                                # Fallback to simple string truncation
                                if isinstance(content, str):
                                    result_summary = content[:200] + (
                                        "..." if len(content) > 200 else ""
                                    )

                            print(f"   └─ Status: {status_icon} {result_summary}")

            # Optional debug logging for chunk structures (helps diagnose missing tool calls)
            if (
                self.logger
                and hasattr(self, "_debug_tool_calls")
                and self._debug_tool_calls
            ):
                self.logger.log_structured(
                    "debug",
                    "tool_display",
                    "chunk_structure",
                    chunk_keys=list(chunk.keys()),
                    chunk_types={k: type(v).__name__ for k, v in chunk.items()},
                )

        except Exception as e:
            # Don't let display errors break the agent flow
            if self.logger:
                self.logger.log_error(e, context="tool_display")


# -----------------------------
# DJANGO MANAGEMENT COMMAND
# -----------------------------


class Command(BaseCommand):
    help = (
        "Elora LangGraph: Production ReAct agent using LangGraph's create_react_agent"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--project-id",
            type=str,
            required=True,
            help="UUID of the project to work with",
        )

    def handle(self, *args, **options):
        project_id = options["project_id"]

        # Initialize session logger first
        session_logger = EloraSessionLogger(project_id)
        session_logger.log_structured(
            "info",
            "command",
            "handle_start",
            project_id=project_id,
            args=args,
            options=options,
        )

        exit_reason = "normal"
        try:
            # Validate UUID format
            if not uuid_like(project_id):
                session_logger.log_structured(
                    "error", "command", "invalid_uuid", project_id=project_id
                )
                raise CommandError("--project-id must be a valid UUID")

            session_logger.log_structured(
                "info", "command", "uuid_validated", project_id=project_id
            )

            # Get OpenAI API key
            api_key = must_get_openai_key(session_logger)

            # Load Django models
            models = get_models_for_agent(DEFAULT_MODEL_MAP, session_logger)

            # Create ReAct agent
            try:
                agent = EloraReActAgent(project_id, api_key, models, session_logger)
                self.stdout.write("✅ LangGraph ReAct agent initialized successfully")
                session_logger.log_structured("info", "command", "agent_initialized")
            except Exception as e:
                session_logger.log_error(e, context="agent_initialization")
                raise CommandError(f"Failed to initialize agent: {e}")

            # Initialize command loader
            start_time = time.time()
            commands_dir = Path(__file__).parent.parent.parent / "commands"
            command_loader = CommandLoader(commands_dir)

            duration_ms = (time.time() - start_time) * 1000
            session_logger.log_structured(
                "info",
                "command",
                "command_loader_initialized",
                commands_dir=str(commands_dir),
                duration_ms=duration_ms,
            )

            # Interactive CLI loop
            self.stdout.write(
                self.style.SUCCESS(
                    "\n🎭 Elora LangGraph - Powered by create_react_agent\n"
                    "Canvas-centric story creation with true ReAct reasoning\n"
                    "Type 'help' for commands, 'quit' to exit\n"
                )
            )

            session_logger.log_structured("info", "command", "cli_loop_start")

            # Conversation history for the session (user + assistant + any prior context)
            session_messages: list = []

            while True:
                try:
                    user_input = input("elora> ").strip()
                    session_logger.log_user_input(user_input, "interactive")
                except (EOFError, KeyboardInterrupt):
                    exit_reason = "user_interrupt"
                    session_logger.log_structured("info", "command", "user_interrupt")
                    self.stdout.write("\n👋 Goodbye!")
                    break

                if not user_input:
                    session_logger.log_user_input("", "empty_input")
                    continue

                # Initialize command variables
                cmd = ""
                arg = None

                # Slash command routing: only /help and /quit|/exit are local.
                if user_input.startswith("/"):
                    parts = user_input[1:].strip().split()
                    cmd = parts[0].lower() if parts else ""
                    arg = parts[1].lower() if len(parts) > 1 else None

                    session_logger.log_command_processing(
                        user_input, "slash_command", result=f"command={cmd}, arg={arg}"
                    )

                    # Check for dynamic commands first
                    dynamic_command_content = command_loader.get_command(cmd)
                    if dynamic_command_content:
                        session_logger.log_command_processing(cmd, "dynamic_command")
                        self.stdout.write(f"\n🎭 Activating {cmd} mode...")

                        final_text, final_msg = agent.run(
                            dynamic_command_content, base_messages=session_messages
                        )
                        self.stdout.write(f"\n{final_text}\n")

                        # Persist the command and response
                        session_messages.append(
                            HumanMessage(content=dynamic_command_content)
                        )
                        session_messages.append(final_msg)

                        session_logger.log_command_processing(
                            cmd, "dynamic_command", result="completed"
                        )
                        continue

                # Map /caps on|off to explicit instructions sent to LLM immediately
                if cmd == "caps":
                    if arg in {"on", "enable", "enabled"}:
                        self.stdout.write(f"\n🤔 Processing: {user_input}")
                        transformed = (
                            "From now on, respond ONLY IN UPPERCASE. Do not use lowercase letters. "
                            "Acknowledge with OK IN UPPERCASE."
                        )
                        final_text, final_msg = agent.run(
                            transformed, base_messages=session_messages
                        )
                        self.stdout.write(f"\n{final_text}\n")
                        # Persist the transformed instruction and the model's reply
                        session_messages.append(HumanMessage(content=transformed))
                        session_messages.append(final_msg)
                        continue
                    elif arg in {"off", "disable", "disabled"}:
                        self.stdout.write(f"\n🤔 Processing: {user_input}")
                        transformed = "Resume normal casing. Do not force ALL CAPS."
                        final_text, final_msg = agent.run(
                            transformed, base_messages=session_messages
                        )
                        self.stdout.write(f"\n{final_text}\n")
                        session_messages.append(HumanMessage(content=transformed))
                        session_messages.append(final_msg)
                        continue
                    # fall through for unknown args to be treated verbatim

                if cmd in {"help"}:
                    help_text = [
                        "Built-in Commands:",
                        "  help - Show this help message",
                        "  quit/exit - Exit the CLI",
                        "  caps on/off - Toggle uppercase mode",
                    ]

                    # Add dynamic commands
                    dynamic_commands = command_loader.list_commands()
                    if dynamic_commands:
                        help_text.append("\nDynamic Commands:")
                        for cmd_name, cmd_desc in dynamic_commands:
                            desc_text = f" - {cmd_desc}" if cmd_desc else ""
                            help_text.append(f"  {cmd_name}{desc_text}")

                    help_text.extend(
                        [
                            "\nNotes:",
                            "  Lines starting with '/' (slash) are sent to the agent verbatim,",
                            "  except for built-in commands which are handled locally.",
                            "\nSlash Examples:",
                            "  /caps on — From now on, respond ONLY IN UPPERCASE. Do not use lowercase letters.",
                            "             Acknowledge with OK IN UPPERCASE.",
                            "  /caps off — Resume normal casing. Do not force ALL CAPS.",
                        ]
                    )

                    self.stdout.write("\n".join(help_text))
                    continue
                if cmd in {"quit", "exit"}:
                    exit_reason = "user_command"
                    session_logger.log_command_processing(cmd, "exit_command")
                    self.stdout.write("👋 Goodbye!")
                    break

                if user_input.lower() in {"quit", "exit"}:
                    exit_reason = "user_command"
                    session_logger.log_command_processing(user_input, "exit_command")
                    self.stdout.write("👋 Goodbye!")
                    break

                if user_input.lower() == "help":
                    help_text = [
                        "Built-in Commands:",
                        "  help - Show this help message",
                        "  quit/exit - Exit the CLI",
                        "  caps on/off - Toggle uppercase mode",
                    ]

                    # Add dynamic commands
                    dynamic_commands = command_loader.list_commands()
                    if dynamic_commands:
                        help_text.append("\nDynamic Commands:")
                        for cmd_name, cmd_desc in dynamic_commands:
                            desc_text = f" - {cmd_desc}" if cmd_desc else ""
                            help_text.append(f"  /{cmd_name}{desc_text}")

                    help_text.extend(
                        [
                            "\nNotes:",
                            "  Lines starting with '/' (slash) are sent to the agent verbatim,",
                            "  except for built-in commands which are handled locally.",
                            "\nSlash Examples:",
                            "  /caps on — From now on, respond ONLY IN UPPERCASE. Do not use lowercase letters.",
                            "             Acknowledge with OK IN UPPERCASE.",
                            "  /caps off — Resume normal casing. Do not force ALL CAPS.",
                            "\nExample requests:",
                            "  'create a canvas where Jake meets Linda in the living room'",
                            "  'list all locations'",
                            "  'create a beach location for vacation scenes'",
                            "  'generate the game and validate it'",
                            "\nThe agent will automatically reason about your request,",
                            "find or create necessary resources, and complete the task.",
                        ]
                    )

                    self.stdout.write("\n".join(help_text))
                    continue

                # Execute ReAct loop
                session_logger.log_command_processing(user_input, "user_query")
                self.stdout.write(f"\n🤔 Processing: {user_input}")

                final_text, final_msg = agent.run(
                    user_input, base_messages=session_messages
                )
                self.stdout.write(f"\n{final_text}\n")

                # Persist full turn into session history
                session_messages.append(HumanMessage(content=user_input))
                session_messages.append(final_msg)

                session_logger.log_command_processing(
                    user_input, "user_query", result="completed"
                )

        except Exception as e:
            exit_reason = "error"
            session_logger.log_error(e, context="main_command_loop")
            raise
        finally:
            # Always log session end
            session_logger.log_session_end(exit_reason)
