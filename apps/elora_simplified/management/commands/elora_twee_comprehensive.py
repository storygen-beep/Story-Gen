#!/usr/bin/env python3
"""
Elora: Narrative-first ReAct agent for twee_comprehensive game generation.

USAGE (CLI):
  python manage.py elora_twee_comprehensive --project-id <UUID>
  # Interactive REPL opens. Type 'help' for commands, 'quit' to exit.

Design notes:
- Properly integrated with Django models used by twee_comprehensive system
- Enforces one-node-per-canvas policy for simplified story management
- Canvas-centric workflow: Canvas = Story Beat = Location Interaction
- Uses actual field names and relationships from model analysis
- Includes generation tools so agent can test its own work
- Implements full ReAct workflow with safety gates and validation
"""

from __future__ import annotations

import json
import readline  # noqa: F401  # nice CLI history if available
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Optional, Union

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

# -----------------------------
# CONFIG & MODEL DISCOVERY
# -----------------------------

DEFAULT_TWEE_COMPREHENSIVE_MODEL_MAP = {
    # Corrected model mappings based on actual twee_comprehensive system analysis
    "Project": "projects.Project",
    "Location": "world.Location",
    "StoryCanvas": "stories.StoryCanvas",
    "StoryNode": "stories.StoryNode",
    "CanvasTrigger": "stories.CanvasTrigger",
    "TriggerSchedule": "stories.TriggerSchedule",
    # Note: NodeConnection removed - enforcing one-node-per-canvas policy
    # Note: Character removed - not used in twee_comprehensive workflow
}


def get_model(alias: str):
    model_map = getattr(
        settings, "TWEE_COMPREHENSIVE_MODEL_MAP", DEFAULT_TWEE_COMPREHENSIVE_MODEL_MAP
    )
    if alias not in model_map:
        raise CommandError(f"TWEE_COMPREHENSIVE_MODEL_MAP missing alias: {alias}")
    dotted = model_map[alias]
    try:
        app_label, model_name = dotted.split(".")
    except ValueError:
        raise CommandError(
            f"Invalid TWEE_COMPREHENSIVE_MODEL_MAP target '{dotted}' for alias '{alias}'. Use 'app_label.ModelName'."
        )
    model = apps.get_model(app_label, model_name)
    if model is None:
        raise CommandError(f"Could not load model for alias '{alias}' = '{dotted}'")
    return model


# -----------------------------
# OPENAI CLIENT (tool-called)
# -----------------------------


def must_get_openai_key() -> str:
    api_key = getattr(settings, "OPENAI_API_KEY", None)
    if not api_key:
        raise CommandError("OPENAI_API_KEY is not set in Django settings.")
    return api_key


# OpenAI client for 1.0+ API
class OpenAIShim:
    def __init__(self, api_key: str):
        self.api_key = api_key
        try:
            import openai  # type: ignore
        except ImportError:
            raise CommandError(
                "openai package is not installed; pip install openai to run LLM calls."
            )

        # Create OpenAI client instance for 1.0+ API
        self.client = openai.OpenAI(
            api_key=api_key,
            timeout=30.0,  # 30 second timeout
            max_retries=2,  # Retry failed requests
        )

    def chat(
        self,
        messages: list[dict[str, str]],
        model: str = "gpt-4o-mini",  # Updated to valid OpenAI model
        temperature: float = 0.2,
        max_tokens: int = 800,
    ) -> str:
        """
        Make chat completion request using OpenAI 1.0+ API.
        """
        try:
            # Use new OpenAI 1.0+ API
            resp = self.client.chat.completions.create(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                messages=messages,
            )

            # Validate response structure
            if not resp.choices or not resp.choices[0].message.content:
                raise ValueError("Invalid response structure from OpenAI API")

            return resp.choices[0].message.content.strip()

        except Exception as e:
            # Import OpenAI exceptions for proper error handling
            import openai

            if isinstance(e, openai.AuthenticationError):
                raise CommandError(
                    "OpenAI authentication failed. Check your API key in Django settings."
                )
            elif isinstance(e, openai.RateLimitError):
                raise CommandError(
                    "OpenAI rate limit exceeded. Please wait and try again."
                )
            elif isinstance(e, openai.BadRequestError):
                raise CommandError(
                    f"OpenAI request error: {str(e)}. Check model name and parameters."
                )
            elif isinstance(e, openai.APITimeoutError):
                raise CommandError("OpenAI request timed out. Please try again.")
            else:
                raise CommandError(f"OpenAI API error: {str(e)}")


# -----------------------------
# REACT AGENT BUILDING BLOCKS
# -----------------------------


@dataclass
class TinyProjectSnapshot:
    project_id: str
    project_name: str
    starting_canvas_id: Optional[str] = None
    time_settings: dict[str, Any] = field(default_factory=dict)
    locations_index: list[dict[str, Any]] = field(default_factory=list)
    story_canvases: list[dict[str, Any]] = field(default_factory=list)
    counts: dict[str, int] = field(default_factory=dict)
    ts: float = field(default_factory=lambda: time.time())


@dataclass
class StepPlan:
    tool: str
    args: dict[str, Any]
    targets: list[str]
    expected_effect: str
    destructiveness: str  # read_only | low_write | high_write
    confidence: float
    rationale: str


@dataclass
class ToDoItem:
    kind: str  # read|write
    description: str
    tool: Optional[str] = None
    args: Optional[dict[str, Any]] = None
    check: Optional[str] = None


@dataclass
class ToDoPlan:
    title: str
    rationale: str
    items: list[ToDoItem]
    overall_check: Optional[str] = None


@dataclass
class ToolResult:
    success: bool
    data: Any = None
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    _tool_metadata: dict[str, Any] = field(default_factory=dict)


# -----------------------------
# TOOL ADAPTERS (ORM) - CORRECTED FOR TWEE_COMPREHENSIVE
# -----------------------------


class Tools:
    """
    Deterministic, DB-backed tool adapters for twee_comprehensive system.
    Uses actual field names and relationships from model analysis.
    """

    def __init__(self, project_id: str):
        self.project_id = str(project_id)
        self.Project = get_model("Project")
        self.Location = get_model("Location")
        self.StoryCanvas = get_model("StoryCanvas")
        self.StoryNode = get_model("StoryNode")
        self.CanvasTrigger = get_model("CanvasTrigger")
        self.TriggerSchedule = get_model("TriggerSchedule")

    # ---------- READ TOOLS ----------

    def get_project(self, identifier: str) -> ToolResult:
        """Get project details with time settings"""
        try:
            if uuid_like(identifier):
                project = self.Project.objects.get(pk=identifier)
            else:
                project = self.Project.objects.get(name=identifier)

            time_settings = (
                project.get_time_settings()
                if hasattr(project, "get_time_settings")
                else {}
            )

            data = {
                "id": str(project.pk),
                "name": project.name,
                "description": project.description,
                "starting_canvas_id": (
                    str(project.starting_canvas.pk) if project.starting_canvas else None
                ),
                "time_settings": time_settings,
            }
            return ToolResult(True, data=data, _tool_metadata={"name": "get_project"})
        except self.Project.DoesNotExist:
            return ToolResult(
                False,
                errors=[f"Project not found: {identifier}"],
                _tool_metadata={"name": "get_project"},
            )

    def list_locations(self, query: Optional[str] = None) -> ToolResult:
        """List locations in project"""
        qs = self.Location.objects.filter(project_id=self.project_id)
        if query:
            qs = qs.filter(name__icontains=query)
        qs = qs.order_by("name")[:25]

        data = []
        for location in qs:
            data.append(
                {
                    "id": str(location.pk),
                    "name": location.name,
                    "description": location.description,
                    "location_type": getattr(location, "location_type", "generic"),
                }
            )
        return ToolResult(True, data=data, _tool_metadata={"name": "list_locations"})

    def get_location(self, identifier: str) -> ToolResult:
        """Get specific location details"""
        qs = self.Location.objects.filter(project_id=self.project_id)

        try:
            if uuid_like(identifier):
                location = qs.get(pk=identifier)
            else:
                location = qs.get(name=identifier)

            data = {
                "id": str(location.pk),
                "name": location.name,
                "description": location.description,
                "location_type": getattr(location, "location_type", "generic"),
            }
            return ToolResult(True, data=data, _tool_metadata={"name": "get_location"})
        except self.Location.DoesNotExist:
            return ToolResult(
                False,
                errors=[f"Location not found: {identifier}"],
                _tool_metadata={"name": "get_location"},
            )

    def list_story_canvases(
        self, query: Optional[str] = None, location_id: Optional[str] = None
    ) -> ToolResult:
        """List story canvases with trigger and content info"""
        qs = self.StoryCanvas.objects.filter(
            project_id=self.project_id, deleted_at__isnull=True
        )

        if query:
            qs = qs.filter(name__icontains=query)

        # Filter by trigger location if specified
        if location_id:
            qs = qs.filter(trigger__location_id=location_id)

        qs = (
            qs.select_related("trigger").prefetch_related("nodes").order_by("name")[:25]
        )

        data = []
        for canvas in qs:
            # Get single node content (one-node-per-canvas policy)
            node = canvas.nodes.first()
            trigger_location_id = None
            if hasattr(canvas, "trigger") and canvas.trigger:
                trigger_location_id = (
                    str(canvas.trigger.location_id)
                    if canvas.trigger.location_id
                    else None
                )

            data.append(
                {
                    "id": str(canvas.pk),
                    "name": canvas.name,
                    "trigger_location_id": trigger_location_id,
                    "has_content": node is not None,
                    "node_count": canvas.nodes.count(),
                }
            )
        return ToolResult(
            True, data=data, _tool_metadata={"name": "list_story_canvases"}
        )

    def get_story_canvas(self, identifier: str) -> ToolResult:
        """Get story canvas with full content and trigger info"""
        qs = (
            self.StoryCanvas.objects.filter(
                project_id=self.project_id, deleted_at__isnull=True
            )
            .select_related("trigger")
            .prefetch_related("nodes", "trigger__schedules")
        )

        try:
            if uuid_like(identifier):
                canvas = qs.get(pk=identifier)
            else:
                canvas = qs.get(name=identifier)

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
                    "location_id": (
                        str(canvas.trigger.location_id)
                        if canvas.trigger.location_id
                        else None
                    ),
                    "is_active": canvas.trigger.is_active,
                    "schedules": schedules,
                }

            data = {
                "id": str(canvas.pk),
                "name": canvas.name,
                "description": canvas.description,
                "node_data": node_data,
                "trigger_info": trigger_info,
            }
            return ToolResult(
                True, data=data, _tool_metadata={"name": "get_story_canvas"}
            )
        except self.StoryCanvas.DoesNotExist:
            return ToolResult(
                False,
                errors=[f"Story canvas not found: {identifier}"],
                _tool_metadata={"name": "get_story_canvas"},
            )

    # ---------- WRITE TOOLS ----------

    @transaction.atomic
    def create_location(
        self, name: str, description: str = "", location_type: str = "generic"
    ) -> ToolResult:
        """Create a new location (idempotent by project+name)"""
        # Check if already exists
        existing = self.Location.objects.filter(
            project_id=self.project_id, name=name
        ).first()
        if existing:
            return ToolResult(
                True,
                data={"id": str(existing.pk), "created": False},
                warnings=["Location already existed."],
                _tool_metadata={"name": "create_location"},
            )

        location = self.Location.objects.create(
            project_id=self.project_id,
            name=name,
            description=description,
            location_type=location_type,
        )
        return ToolResult(
            True,
            data={"id": str(location.pk), "created": True},
            _tool_metadata={"name": "create_location"},
        )

    @transaction.atomic
    def create_story_canvas(
        self,
        name: str,
        location_id: str,
        content_blocks: list[str],
        exit_config: Optional[dict[str, Any]] = None,
        description: str = "",
    ) -> ToolResult:
        """
        Create story canvas with single node and trigger (one-node-per-canvas policy).
        This creates: StoryCanvas + StoryNode + CanvasTrigger in one operation.
        """
        # Validate location exists
        try:
            location = self.Location.objects.get(
                pk=location_id, project_id=self.project_id
            )
        except self.Location.DoesNotExist:
            return ToolResult(
                False,
                errors=[f"Location not found: {location_id}"],
                _tool_metadata={"name": "create_story_canvas"},
            )

        # Check for existing canvas (one-canvas-per-name policy)
        existing = self.StoryCanvas.objects.filter(
            project_id=self.project_id, name=name, deleted_at__isnull=True
        ).first()
        if existing:
            return ToolResult(
                False,
                errors=[f"Canvas already exists: {name} (use update tool instead)"],
                _tool_metadata={"name": "create_story_canvas"},
            )

        # Default exit configuration
        if exit_config is None:
            exit_config = {
                "type": "location",
                "text": "Continue",
                "config": {"destinationType": "trigger", "time_progression_minutes": 3},
            }

        # Create canvas
        canvas = self.StoryCanvas.objects.create(
            project_id=self.project_id,
            name=name,
            description=description,
        )

        # Create single node with BlockNote content (rich format + version + preview)
        rich_blocks = [
            {
                "id": str(uuid.uuid4()),
                "type": "paragraph",
                "props": {},
                "content": block_text,
                "children": [],
            }
            for block_text in content_blocks
        ]
        preview_text = "\n".join(
            [
                str(b.get("content", "")).strip()
                for b in rich_blocks
                if str(b.get("content", "")).strip()
            ]
        )
        node_data = {
            "blocks": rich_blocks,
            "version": "2.0",
            "content": preview_text,
        }

        node = self.StoryNode.objects.create(
            canvas=canvas,
            name=name,
            node_data=node_data,
            exit_block=exit_config,
        )

        # Create trigger linking to location
        trigger = self.CanvasTrigger.objects.create(
            canvas=canvas,
            location_id=location_id,
            is_active=True,
        )

        return ToolResult(
            True,
            data={
                "canvas_id": str(canvas.pk),
                "node_id": str(node.pk),
                "trigger_id": str(trigger.pk),
                "created": True,
            },
            _tool_metadata={"name": "create_story_canvas"},
        )

    @transaction.atomic
    def update_story_content(
        self,
        canvas_id: str,
        content_blocks: list[str],
        exit_config: Optional[dict[str, Any]] = None,
    ) -> ToolResult:
        """Update the content of a canvas's single node"""
        try:
            canvas = self.StoryCanvas.objects.get(
                pk=canvas_id, project_id=self.project_id, deleted_at__isnull=True
            )
        except self.StoryCanvas.DoesNotExist:
            return ToolResult(
                False,
                errors=[f"Canvas not found: {canvas_id}"],
                _tool_metadata={"name": "update_story_content"},
            )

        # Get single node
        node = canvas.nodes.first()
        if not node:
            return ToolResult(
                False,
                errors=["Canvas has no content node to update"],
                _tool_metadata={"name": "update_story_content"},
            )

        # Update content
        rich_blocks = [
            {
                "id": str(uuid.uuid4()),
                "type": "paragraph",
                "props": {},
                "content": block_text,
                "children": [],
            }
            for block_text in content_blocks
        ]
        preview_text = "\n".join(
            [
                str(b.get("content", "")).strip()
                for b in rich_blocks
                if str(b.get("content", "")).strip()
            ]
        )
        node.node_data = {
            "blocks": rich_blocks,
            "version": "2.0",
            "content": preview_text,
        }

        if exit_config:
            node.exit_block = exit_config

        node.save()

        return ToolResult(
            True,
            data={"node_id": str(node.pk), "updated": True},
            _tool_metadata={"name": "update_story_content"},
        )

    @transaction.atomic
    def create_trigger_schedule(
        self,
        canvas_id: str,
        name: str,
        weekdays: list[int],
        start_time: str,
        end_time: Optional[str] = None,
    ) -> ToolResult:
        """Add schedule to a canvas trigger"""
        try:
            canvas = self.StoryCanvas.objects.get(
                pk=canvas_id, project_id=self.project_id, deleted_at__isnull=True
            )
        except self.StoryCanvas.DoesNotExist:
            return ToolResult(
                False,
                errors=[f"Canvas not found: {canvas_id}"],
                _tool_metadata={"name": "create_trigger_schedule"},
            )

        if not hasattr(canvas, "trigger") or not canvas.trigger:
            return ToolResult(
                False,
                errors=["Canvas has no trigger to add schedule to"],
                _tool_metadata={"name": "create_trigger_schedule"},
            )

        # Validate schedule data
        for day in weekdays:
            if not (0 <= day <= 6):
                return ToolResult(
                    False,
                    errors=[f"Invalid weekday: {day} (must be 0-6, Monday=0)"],
                    _tool_metadata={"name": "create_trigger_schedule"},
                )

        from datetime import datetime

        try:
            start_dt = datetime.strptime(start_time, "%H:%M").time()
            end_dt = datetime.strptime(end_time, "%H:%M").time() if end_time else None
        except ValueError as e:
            return ToolResult(
                False,
                errors=[f"Invalid time format: {e}"],
                _tool_metadata={"name": "create_trigger_schedule"},
            )

        schedule = self.TriggerSchedule.objects.create(
            trigger=canvas.trigger,
            name=name,
            weekdays=weekdays,
            start_time=start_dt,
            end_time=end_dt,
        )

        return ToolResult(
            True,
            data={"schedule_id": str(schedule.pk), "created": True},
            _tool_metadata={"name": "create_trigger_schedule"},
        )

    @transaction.atomic
    def set_starting_canvas(self, canvas_id: str) -> ToolResult:
        """Set the starting canvas for the project"""
        try:
            canvas = self.StoryCanvas.objects.get(
                pk=canvas_id, project_id=self.project_id, deleted_at__isnull=True
            )
        except self.StoryCanvas.DoesNotExist:
            return ToolResult(
                False,
                errors=[f"Canvas not found: {canvas_id}"],
                _tool_metadata={"name": "set_starting_canvas"},
            )

        project = self.Project.objects.get(pk=self.project_id)
        project.starting_canvas = canvas
        project.save()

        return ToolResult(
            True,
            data={"project_id": str(project.pk), "starting_canvas_id": str(canvas.pk)},
            _tool_metadata={"name": "set_starting_canvas"},
        )

    # ---------- GENERATION & VALIDATION TOOLS ----------

    def validate_project(self) -> ToolResult:
        """Validate project for twee_comprehensive generation"""
        try:
            from apps.game_generation.twee_comprehensive.services import (
                TweeComprehensiveService,
            )
        except ImportError:
            return ToolResult(
                False,
                errors=["twee_comprehensive service not available"],
                _tool_metadata={"name": "validate_project"},
            )

        try:
            project = self.Project.objects.get(pk=self.project_id)
            service = TweeComprehensiveService()
            validation_result = service.validate_project(project)

            return ToolResult(
                not validation_result["has_errors"],
                data=validation_result,
                warnings=validation_result.get("warnings", []),
                errors=validation_result.get("errors", []),
                _tool_metadata={"name": "validate_project"},
            )
        except Exception as e:
            return ToolResult(
                False,
                errors=[f"Validation failed: {str(e)}"],
                _tool_metadata={"name": "validate_project"},
            )

    def generate_game_twee(self) -> ToolResult:
        """Generate twee content using twee_comprehensive system"""
        try:
            from apps.game_generation.twee_comprehensive.services import (
                TweeComprehensiveService,
            )
        except ImportError:
            return ToolResult(
                False,
                errors=["twee_comprehensive service not available"],
                _tool_metadata={"name": "generate_game_twee"},
            )

        try:
            project = self.Project.objects.get(pk=self.project_id)
            service = TweeComprehensiveService()
            twee_content = service.generate(project, version="v1")

            return ToolResult(
                True,
                data={"twee_content": twee_content, "length": len(twee_content)},
                _tool_metadata={"name": "generate_game_twee"},
            )
        except Exception as e:
            return ToolResult(
                False,
                errors=[f"Generation failed: {str(e)}"],
                _tool_metadata={"name": "generate_game_twee"},
            )

    def preview_story_canvas(self, canvas_id: str) -> ToolResult:
        """Preview how canvas content will appear in generated game"""
        result = self.get_story_canvas(canvas_id)
        if not result.success:
            return result

        canvas_data = result.data
        node_data = canvas_data.get("node_data")

        if not node_data:
            return ToolResult(
                False,
                errors=["Canvas has no content to preview"],
                _tool_metadata={"name": "preview_story_canvas"},
            )

        # Convert BlockNote blocks to preview text
        preview_text = ""
        for block in node_data.get("content_blocks", []):
            if block.get("type") == "paragraph":
                preview_text += f"<p>{block.get('content', '')}</p>\n"
            elif block.get("type") == "heading":
                level = block.get("props", {}).get("level", 1)
                preview_text += f"<h{level}>{block.get('content', '')}</h{level}>\n"

        exit_block = node_data.get("exit_block", {})
        exit_text = exit_block.get("text", "Continue")
        time_progression = exit_block.get("config", {}).get(
            "time_progression_minutes", 3
        )

        preview_text += f"\n[[{exit_text}->NextLocation]]"
        preview_text += f"\n<!-- Time advances by {time_progression} minutes -->"

        return ToolResult(
            True,
            data={
                "canvas_name": canvas_data["name"],
                "preview_html": preview_text,
                "trigger_location": canvas_data.get("trigger_info", {}).get(
                    "location_id"
                ),
            },
            _tool_metadata={"name": "preview_story_canvas"},
        )


# -----------------------------
# TOOL MANIFEST - UPDATED FOR TWEE_COMPREHENSIVE
# -----------------------------

TOOL_MANIFEST: dict[str, dict[str, Any]] = {
    "get_project": {
        "args_schema": {"identifier": "str"},
        "destructiveness": "read_only",
        "docs": "Get project details including starting canvas and time settings.",
    },
    "list_locations": {
        "args_schema": {"query": "str?"},
        "destructiveness": "read_only",
        "docs": "List up to 25 locations in the project, optionally filtered by name.",
    },
    "get_location": {
        "args_schema": {"identifier": "str"},
        "destructiveness": "read_only",
        "docs": "Get specific location details by ID or name.",
    },
    "list_story_canvases": {
        "args_schema": {"query": "str?", "location_id": "str?"},
        "destructiveness": "read_only",
        "docs": "List story canvases, optionally filtered by location trigger.",
    },
    "get_story_canvas": {
        "args_schema": {"identifier": "str"},
        "destructiveness": "read_only",
        "docs": "Get story canvas with full content, trigger, and schedule info.",
    },
    "create_location": {
        "args_schema": {"name": "str", "description": "str?", "location_type": "str?"},
        "destructiveness": "low_write",
        "docs": "Create a new location (idempotent by project+name).",
        "post_invariants": ["location_exists"],
    },
    "create_story_canvas": {
        "args_schema": {
            "name": "str",
            "location_id": "str",
            "content_blocks": "list[str]",
            "exit_config": "dict?",
            "description": "str?",
        },
        "destructiveness": "low_write",
        "docs": "Create story canvas with single node and trigger (one-node-per-canvas policy).",
        "post_invariants": ["canvas_exists", "node_exists", "trigger_exists"],
    },
    "update_story_content": {
        "args_schema": {
            "canvas_id": "str",
            "content_blocks": "list[str]",
            "exit_config": "dict?",
        },
        "destructiveness": "low_write",
        "docs": "Update content of canvas's single node.",
        "post_invariants": ["content_updated"],
    },
    "create_trigger_schedule": {
        "args_schema": {
            "canvas_id": "str",
            "name": "str",
            "weekdays": "list[int]",
            "start_time": "str",
            "end_time": "str?",
        },
        "destructiveness": "low_write",
        "docs": "Add time-based schedule to canvas trigger (weekdays 0-6, times HH:MM).",
        "post_invariants": ["valid_schedule"],
    },
    "set_starting_canvas": {
        "args_schema": {"canvas_id": "str"},
        "destructiveness": "low_write",
        "docs": "Set the starting canvas for project entry point.",
        "post_invariants": ["starting_canvas_set"],
    },
    "validate_project": {
        "args_schema": {},
        "destructiveness": "read_only",
        "docs": "Validate project for twee_comprehensive game generation.",
    },
    "generate_game_twee": {
        "args_schema": {},
        "destructiveness": "read_only",
        "docs": "Generate playable twee content using twee_comprehensive system.",
    },
    "preview_story_canvas": {
        "args_schema": {"canvas_id": "str"},
        "destructiveness": "read_only",
        "docs": "Preview how canvas content will appear in generated game.",
    },
}


# -----------------------------
# TPS LOADER (CORRECTED FOR TWEE_COMPREHENSIVE)
# -----------------------------


class SnapshotService:
    def __init__(self, project_id: str, ttl_seconds: int = 600):
        self.project_id = str(project_id)
        self.ttl = ttl_seconds
        self._cache: Optional[TinyProjectSnapshot] = None

        self.Project = get_model("Project")
        self.Location = get_model("Location")
        self.StoryCanvas = get_model("StoryCanvas")

    def _is_fresh(self) -> bool:
        return self._cache is not None and (time.time() - self._cache.ts) < self.ttl

    def get(self) -> TinyProjectSnapshot:
        if self._is_fresh():
            return self._cache

        # Get project with time settings
        project = self.Project.objects.filter(pk=self.project_id).first()
        if not project:
            raise CommandError(f"Project not found: {self.project_id}")

        project_name = project.name or f"Project {self.project_id}"
        time_settings = (
            project.get_time_settings() if hasattr(project, "get_time_settings") else {}
        )
        starting_canvas_id = (
            str(project.starting_canvas.pk) if project.starting_canvas else None
        )

        # Index locations
        locations = self.Location.objects.filter(project_id=self.project_id).order_by(
            "name"
        )[:100]
        loc_index = [
            {
                "id": str(loc.pk),
                "name": loc.name,
                "description": loc.description[:100] if loc.description else "",
                "location_type": getattr(loc, "location_type", "generic"),
            }
            for loc in locations
        ]

        # Story canvases with trigger info
        canvases = (
            self.StoryCanvas.objects.filter(
                project_id=self.project_id, deleted_at__isnull=True
            )
            .select_related("trigger")
            .prefetch_related("nodes")
            .order_by("-updated_at")[:15]
        )

        canvas_list = []
        for canvas in canvases:
            trigger_location_id = None
            if hasattr(canvas, "trigger") and canvas.trigger:
                trigger_location_id = (
                    str(canvas.trigger.location_id)
                    if canvas.trigger.location_id
                    else None
                )

            canvas_list.append(
                {
                    "id": str(canvas.pk),
                    "name": canvas.name,
                    "trigger_location_id": trigger_location_id,
                    "node_count": canvas.nodes.count(),
                    "has_content": canvas.nodes.exists(),
                }
            )

        # Counts
        counts = {
            "total_locations": self.Location.objects.filter(
                project_id=self.project_id
            ).count(),
            "total_canvases": self.StoryCanvas.objects.filter(
                project_id=self.project_id, deleted_at__isnull=True
            ).count(),
        }

        self._cache = TinyProjectSnapshot(
            project_id=self.project_id,
            project_name=project_name,
            starting_canvas_id=starting_canvas_id,
            time_settings=time_settings,
            locations_index=loc_index,
            story_canvases=canvas_list,
            counts=counts,
        )
        return self._cache


# -----------------------------
# SAFETY, VALIDATOR, SYNTHESIZER (UPDATED)
# -----------------------------

TAU_LOW = 0.60  # ask if confidence below
TAU_HIGH = 0.80  # proceed if >= (read-only always proceeds)


def safety_gate(step: StepPlan) -> tuple[str, Optional[str]]:
    """
    Returns ("proceed" | "ask" | "confirm", preview_message?)
    """
    if step.destructiveness == "read_only":
        return "proceed", None
    if step.confidence < TAU_LOW:
        return (
            "ask",
            f"I'm not fully sure about the target(s) {step.targets}. Can you confirm or clarify before I proceed?",
        )
    if step.destructiveness == "high_write":
        preview = f"High-impact change planned: {step.tool} on {step.targets} with args {redact(step.args)}"
        return "confirm", preview
    # low_write but not super confident
    if step.confidence < TAU_HIGH:
        return (
            "ask",
            f"About to {step.tool} on {step.targets}. Confirm this is correct?",
        )
    return "proceed", None


def validate_result(step: StepPlan, result: ToolResult) -> ToolResult:
    if not result.success:
        return result
    warnings = list(result.warnings)

    # Invariant checks by tool
    if step.tool == "create_story_canvas":
        # Ensure canvas created with exactly one node and trigger
        data = result.data or {}
        if (
            not data.get("canvas_id")
            or not data.get("node_id")
            or not data.get("trigger_id")
        ):
            warnings.append(
                "Canvas creation should include canvas, node, and trigger IDs"
            )

    elif step.tool == "create_trigger_schedule":
        # Validate schedule parameters
        weekdays = step.args.get("weekdays", [])
        start_time = step.args.get("start_time")
        end_time = step.args.get("end_time")

        for day in weekdays:
            if not (0 <= day <= 6):
                warnings.append(f"Invalid weekday: {day} (should be 0-6)")

        if end_time and start_time >= end_time:
            warnings.append("End time should be after start time")

    elif step.tool == "update_story_content":
        # Ensure content blocks are reasonable
        content_blocks = step.args.get("content_blocks", [])
        if not content_blocks:
            warnings.append("Updated content is empty")

    result.warnings = warnings
    return result


def synthesize_user_message(
    user_goal: str,
    step: Optional[StepPlan],
    result: Optional[ToolResult],
    todo_left: Optional[int] = None,
) -> str:
    msg = []
    msg.append(f"**Goal:** {user_goal}")
    if step:
        msg.append(
            f"**Action:** {step.tool} → targets {', '.join(step.targets) or '-'}"
        )
        msg.append(f"**Rationale (narrative):** {step.rationale}")
    if result:
        if result.success:
            msg.append("**Result:** Success.")
            if result.data:
                # Show key results
                if isinstance(result.data, dict):
                    key_info = []
                    for key in ["id", "canvas_id", "node_id", "created", "updated"]:
                        if key in result.data:
                            key_info.append(f"{key}: {result.data[key]}")
                    if key_info:
                        msg.append(f"**Details:** {', '.join(key_info)}")
        else:
            msg.append("**Result:** Failed.")
        if result.warnings:
            msg.append(f"**Warnings:** {', '.join(result.warnings)}")
        if result.errors:
            msg.append(f"**Errors:** {', '.join(result.errors)}")
    if todo_left:
        msg.append(f"**Next:** {todo_left} step(s) remain in the plan. Proceed?")
    return "\n".join(msg)


def redact(args: dict[str, Any]) -> dict[str, Any]:
    # Small helper to avoid printing long blobs or secrets
    out = {}
    for k, v in args.items():
        if isinstance(v, str) and len(v) > 200:
            out[k] = v[:200] + "…"
        elif isinstance(v, list) and len(v) > 5:
            out[k] = v[:5] + [f"... and {len(v)-5} more items"]
        else:
            out[k] = v
    return out


def uuid_like(s: str) -> bool:
    try:
        uuid.UUID(str(s))
        return True
    except Exception:
        return False


# -----------------------------
# PROMPTS (UPDATED FOR CANVAS-CENTRIC WORKFLOW)
# -----------------------------

SYSTEM_PROMPT = """You are Elora, a narrative-first assistant for twee_comprehensive interactive story generation.

Core Workflow: Project → Locations → Story Canvases (one story beat each) → Game Generation

Key Concepts:
- Canvas = Story Beat: Each canvas contains exactly one piece of content (one-node-per-canvas policy)
- Location-Based Triggers: Canvases activate when player visits specific locations
- Time-Based Schedules: Optional time windows for canvas availability
- BlockNote Content: Story content uses structured blocks format
- Exit Configuration: Each canvas specifies time progression and destination

Canvas Structure:
- Name: Short descriptive title
- Content Blocks: List of text paragraphs in BlockNote format
- Exit Block: {"type": "location", "text": "Continue", "config": {"time_progression_minutes": 3}}
- Trigger: Links canvas to specific location
- Schedules: Optional time windows (weekdays 0-6, times HH:MM)

Story Flow: Location A → Canvas A → Location B → Canvas B (location-to-location navigation)

Rules:
1) Canvas-centric thinking: Each canvas is one complete story interaction
2) One node per canvas: Never try to create multiple nodes or connections
3) Location triggers: All canvases must be triggered by visiting a location
4) Time progression: Each canvas advances game time (default 3 minutes)
5) BlockNote format: Content must be structured as blocks list
6) Validation ready: Always ensure project can generate twee games

Available Operations:
- World Building: create_location, list_locations, get_location
- Story Creation: create_story_canvas, update_story_content, get_story_canvas
- Scheduling: create_trigger_schedule with weekdays and time windows
- Project Setup: set_starting_canvas for entry point
- Testing: validate_project, generate_game_twee, preview_story_canvas

Never invent unsupported fields or relationships. All operations go through validated tools only.
"""

PLANNER_PLUS_PROMPT = """You are at planning step only (no execution).
1) Restate the user goal using canvas-centric vocabulary (Location → Canvas → Story Beat)
2) Use TPS to understand current project state and identify what needs to be created
3) Decide: StepPlan (single tool) OR ToDoPlan (2–5 items for complex stories)
4) For story content, use BlockNote blocks format: [{"type": "paragraph", "content": "text"}]
5) Include narrative intention for each write operation

Output ONLY valid JSON in one of two shapes:
- {"step_plan": {...}}  OR
- {"todo_plan": {"title": "...", "rationale": "...", "items": [...], "overall_check": "...?"}}
"""


# -----------------------------
# SIMPLE LLM PLANNER (ReAct) - UNCHANGED
# -----------------------------


class Planner:
    def __init__(self, llm: OpenAIShim, tool_manifest: dict[str, Any]):
        self.llm = llm
        self.tool_manifest = tool_manifest

    def plan(
        self,
        user_goal: str,
        tps: TinyProjectSnapshot,
        last_tool: Optional[ToolResult] = None,
    ) -> Union[StepPlan, ToDoPlan, str]:
        """Return StepPlan | ToDoPlan | 'ask:<question>'"""
        manifest_summary = self._manifest_to_text()
        tps_text = json.dumps(
            {
                "project_name": tps.project_name,
                "starting_canvas_id": tps.starting_canvas_id,
                "time_settings": tps.time_settings,
                "locations_index": tps.locations_index[:10],
                "story_canvases": tps.story_canvases[:10],
                "counts": tps.counts,
            },
            ensure_ascii=False,
        )

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_goal},
            {
                "role": "assistant",
                "content": f"(Tool Manifest Summary)\n{manifest_summary}",
            },
            {"role": "assistant", "content": f"(Tiny Project Snapshot)\n{tps_text}"},
            {"role": "assistant", "content": PLANNER_PLUS_PROMPT},
        ]
        content = self.llm.chat(
            messages, model="gpt-4o-mini", temperature=0.2, max_tokens=800
        )

        # The model should output JSON; parse carefully
        parsed = try_parse_json(content.strip())
        if not parsed:
            # If the model asked a clarifying Q, bubble up
            if "?" in content:
                return f"ask:{content.strip()}"
            return f"ask:I need a small clarification to proceed: {content[:200]}"

        if "step_plan" in parsed:
            sp = parsed["step_plan"]
            return StepPlan(
                tool=sp["tool"],
                args=sp.get("args", {}),
                targets=sp.get("targets", []),
                expected_effect=sp.get("expected_effect", ""),
                destructiveness=sp.get("destructiveness", "read_only"),
                confidence=float(sp.get("confidence", 0.7)),
                rationale=sp.get("rationale", ""),
            )
        if "todo_plan" in parsed:
            tp = parsed["todo_plan"]
            items = []
            for it in tp.get("items", []):
                items.append(
                    ToDoItem(
                        kind=it.get("kind", "read"),
                        description=it.get("description", ""),
                        tool=it.get("tool"),
                        args=it.get("args"),
                        check=it.get("check"),
                    )
                )
            return ToDoPlan(
                title=tp.get("title", "Plan"),
                rationale=tp.get("rationale", ""),
                items=items,
                overall_check=tp.get("overall_check"),
            )
        return "ask:I could not form a valid plan. Please clarify."

    def _manifest_to_text(self) -> str:
        lines = []
        for name, meta in self.tool_manifest.items():
            lines.append(
                f"- {name} [{meta.get('destructiveness','read_only')}]: {meta.get('docs','')}"
            )
            lines.append(f"  args: {meta.get('args_schema')}")
        return "\n".join(lines)


def try_parse_json(txt: str) -> Optional[dict[str, Any]]:
    try:
        return json.loads(txt)
    except Exception:
        return None


# -----------------------------
# EXECUTOR - UNCHANGED
# -----------------------------


class Executor:
    def __init__(self, tools: Tools):
        self.tools = tools

    def execute_step(self, step: StepPlan) -> ToolResult:
        fn = getattr(self.tools, step.tool, None)
        if not fn:
            return ToolResult(False, errors=[f"Unknown tool: {step.tool}"])
        return fn(**step.args)


# -----------------------------
# INTERACTIVE CLI - UNCHANGED STRUCTURE
# -----------------------------

BANNER = r"""
   ______     __
  / ____/____/ /___  ________ _
 / __/ / ___/ / __ \/ ___/ __ `/
/ /___/ /  / / /_/ / /  / /_/ /
\____/_/  /_/\____/_/   \__,_/

Twee Comprehensive ReAct CLI — canvas-centric story building.
Type 'help' for commands, 'quit' to exit.
"""

HELP = """
Commands:
  help                       Show this help
  plan <text>                Plan without executing (shows StepPlan/ToDo)
  run <text>                 Plan + execute one step (or first ToDo item)
  todo <text>                Plan a multi-step ToDo and ask to run
  tools                      Show tool manifest
  tps                        Show tiny project snapshot (summary)
  generate                   Generate twee game content
  validate                   Validate project for generation
  quit                       Exit

Canvas-Centric Concepts:
  Canvas = Story Beat        Each canvas is one complete story interaction
  Location Triggers          Canvases activate when player visits locations
  One Node Per Canvas        Each canvas contains exactly one content node
  BlockNote Content         Story text uses structured blocks format
"""


class Command(BaseCommand):
    help = "Run Elora ReAct agent for twee_comprehensive game generation"

    def add_arguments(self, parser):
        parser.add_argument(
            "--project-id", required=True, help="UUID of the project to work on"
        )

    def handle(self, *args, **options):
        project_id = options["project_id"]
        # Validate UUID-ish
        if not uuid_like(project_id):
            raise CommandError("--project-id must be a UUID")

        # LLM
        api_key = must_get_openai_key()
        llm = OpenAIShim(api_key)

        # Services
        snapshot_svc = SnapshotService(project_id)
        tools = Tools(project_id)
        planner = Planner(llm, TOOL_MANIFEST)
        executor = Executor(tools)

        # State
        print(BANNER)
        while True:
            try:
                raw = input("elora> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nBye.")
                return

            if not raw:
                continue
            if raw.lower() in {"quit", "exit"}:
                print("Bye.")
                return
            if raw.lower() == "help":
                print(HELP)
                continue
            if raw.lower() == "tools":
                print(json.dumps(TOOL_MANIFEST, indent=2))
                continue
            if raw.lower() == "tps":
                tps = snapshot_svc.get()
                print(
                    json.dumps(
                        {
                            "project_name": tps.project_name,
                            "starting_canvas_id": tps.starting_canvas_id,
                            "time_settings": tps.time_settings,
                            "counts": tps.counts,
                            "locations_index": tps.locations_index[:5],
                            "story_canvases": tps.story_canvases[:5],
                        },
                        indent=2,
                        ensure_ascii=False,
                    )
                )
                continue
            if raw.lower() == "generate":
                print("Generating twee game content...")
                result = tools.generate_game_twee()
                if result.success:
                    twee_length = result.data.get("length", 0)
                    print(f"✅ Generated {twee_length:,} characters of twee content")
                    print("Use 'validate' to check for issues")
                else:
                    print(f"❌ Generation failed: {'; '.join(result.errors)}")
                continue
            if raw.lower() == "validate":
                print("Validating project for generation...")
                result = tools.validate_project()
                if result.success:
                    stats = result.data.get("stats", {})
                    print("✅ Project valid for generation")
                    print(f"Stats: {json.dumps(stats, indent=2)}")
                else:
                    print(f"❌ Validation failed: {'; '.join(result.errors)}")
                    if result.warnings:
                        print(f"⚠️  Warnings: {'; '.join(result.warnings)}")
                continue

            cmd, *rest = raw.split(" ", 1)
            arg = rest[0].strip() if rest else ""

            if cmd == "plan":
                if not arg:
                    print("Usage: plan <text>")
                    continue
                tps = snapshot_svc.get()
                plan = planner.plan(arg, tps)
                print(format_plan(plan))
                continue

            if cmd in {"run", "todo"}:
                if not arg:
                    print(f"Usage: {cmd} <text>")
                    continue
                tps = snapshot_svc.get()
                plan = planner.plan(arg, tps)
                if isinstance(plan, str) and plan.startswith("ask:"):
                    print(plan[4:])
                    continue

                if isinstance(plan, StepPlan):
                    decision, preview = safety_gate(plan)
                    if decision == "ask":
                        print(preview or "Need confirmation. Proceed? (y/n)")
                        if not yesno():
                            print("Cancelled.")
                            continue
                    elif decision == "confirm":
                        print("DRY-RUN PREVIEW:")
                        print(preview)
                        print("Proceed? (y/n)")
                        if not yesno():
                            print("Cancelled.")
                            continue

                    res = executor.execute_step(plan)
                    res = validate_result(plan, res)
                    print(synthesize_user_message(arg, plan, res))
                    # Diff-refresh TPS if write succeeded
                    if res.success and plan.destructiveness != "read_only":
                        snapshot_svc._cache = None
                    continue

                if isinstance(plan, ToDoPlan):
                    print("To-Do Plan:")
                    print(format_plan(plan))
                    if cmd == "todo":
                        print("Run the first item now? (y/n)")
                        if not yesno():
                            continue
                    # Execute first writable/read item safely
                    executed_any = False
                    for idx, item in enumerate(plan.items, start=1):
                        if not item.tool:
                            # read-only non-tool description? skip or implement a read tool
                            continue
                        # transform ToDoItem -> StepPlan for execution
                        step = StepPlan(
                            tool=item.tool,
                            args=item.args or {},
                            targets=[],
                            expected_effect=item.description,
                            destructiveness=TOOL_MANIFEST.get(item.tool, {}).get(
                                "destructiveness", "read_only"
                            ),
                            confidence=0.75,
                            rationale=plan.rationale,
                        )
                        decision, preview = safety_gate(step)
                        if decision == "ask":
                            print(preview or f"About to run step {idx}. Proceed? (y/n)")
                            if not yesno():
                                print("Cancelled.")
                                break
                        elif decision == "confirm":
                            print("DRY-RUN PREVIEW:")
                            print(preview)
                            print(f"Proceed with step {idx}? (y/n)")
                            if not yesno():
                                print("Cancelled.")
                                break

                        res = executor.execute_step(step)
                        res = validate_result(step, res)
                        left = len(plan.items) - idx
                        print(synthesize_user_message(arg, step, res, todo_left=left))
                        if not res.success:
                            print("Stopping due to failure.")
                            break
                        executed_any = True
                        # Refresh TPS on writes
                        if step.destructiveness != "read_only":
                            snapshot_svc._cache = None
                    if not executed_any:
                        print("No steps executed.")
                    continue

                print("Could not form a plan. Try rephrasing.")
                continue

            print("Unknown command. Type 'help'.")


# -----------------------------
# CLI HELPERS - UNCHANGED
# -----------------------------


def format_plan(plan: Union[StepPlan, ToDoPlan, str]) -> str:
    if isinstance(plan, StepPlan):
        return json.dumps(
            {
                "step_plan": {
                    "tool": plan.tool,
                    "args": plan.args,
                    "targets": plan.targets,
                    "expected_effect": plan.expected_effect,
                    "destructiveness": plan.destructiveness,
                    "confidence": plan.confidence,
                    "rationale": plan.rationale,
                }
            },
            indent=2,
            ensure_ascii=False,
        )
    if isinstance(plan, ToDoPlan):
        return json.dumps(
            {
                "todo_plan": {
                    "title": plan.title,
                    "rationale": plan.rationale,
                    "items": [it.__dict__ for it in plan.items],
                    "overall_check": plan.overall_check,
                }
            },
            indent=2,
            ensure_ascii=False,
        )
    if isinstance(plan, str):
        return plan
    return "<?>"


def yesno() -> bool:
    try:
        s = input("[y/n]> ").strip().lower()
        return s in {"y", "yes"}
    except (EOFError, KeyboardInterrupt):
        return False
