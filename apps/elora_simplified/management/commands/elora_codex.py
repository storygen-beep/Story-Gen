#!/usr/bin/env python3
"""
Elora Codex: Phase‑1 LangGraph ReAct agent (read‑only)

Usage:
  python manage.py elora_codex --project-id <UUID>

Notes:
- Phase‑1 focuses on read tools through LangGraph's create_react_agent.
- Write tools and safety confirmations will be added in Phase‑2.
"""

from __future__ import annotations

import json
import textwrap
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


def _require(pkg: str, import_path: str):
    try:
        mod = __import__(import_path, fromlist=["_"])
        return mod
    except Exception as e:
        raise CommandError(
            f"Missing or incompatible dependency: {pkg}. Install and retry. Details: {e}"
        )


def _load_tooling(project_id: str):
    """Import Tool adapters and Snapshot service from the existing command file."""
    try:
        mod = __import__(
            "apps.elora_simplified.management.commands.elora_twee_comprehensive",
            fromlist=["Tools", "SnapshotService", "TinyProjectSnapshot"],
        )
        Tools = mod.Tools
        SnapshotService = mod.SnapshotService
        TinyProjectSnapshot = mod.TinyProjectSnapshot
    except Exception as e:
        raise CommandError(
            "Could not import Tools/SnapshotService from elora_twee_comprehensive.py. "
            f"Ensure that file exists and is importable. Details: {e}"
        )
    return Tools(project_id), SnapshotService(project_id), TinyProjectSnapshot


def _state_modifier(snapshot: Any, writes_enabled: bool = False) -> str:
    """Render a concise state modifier using the Tiny Project Snapshot."""
    try:
        proj_name = getattr(snapshot, "project_name", "?")
        start_id = getattr(snapshot, "starting_canvas_id", None) or "None"
        # Show a few items only
        locs = getattr(snapshot, "locations_index", [])[:5]
        canv = getattr(snapshot, "story_canvases", [])[:5]
        locs_txt = ", ".join(f"{x.get('name')}({x.get('id')[:8]})" for x in locs) or "-"
        canv_txt = ", ".join(f"{x.get('name')}({x.get('id')[:8]})" for x in canv) or "-"
    except Exception:
        proj_name, start_id, locs_txt, canv_txt = "?", "None", "-", "-"

    return textwrap.dedent(
        f"""
        You are Elora, a narrative‑first ReAct agent operating over a canvas‑centric story graph.

        Rules:
        - Never hallucinate IDs; resolve via reads first.
        - Prefer read → decide → write; keep writes minimal and idempotent.
        - One node per canvas; overwrites require confirmation (Phase‑2).
        - Trigger schedules: weekday 0–6; time HH:MM; start < end.

        Project Snapshot:
        - Name: {proj_name}; Starting Canvas: {start_id}
        - Locations: {locs_txt}
        - Recent Canvases: {canv_txt}

        Session Safety:
        - Writes are {'ENABLED' if writes_enabled else 'DISABLED'}. If disabled, treat write attempts as dry‑run previews.

        Tools (read‑only in this phase):
        - get_project: fetch meta/time settings.
        - list_locations: list by name/prefix.
        - list_story_canvases: list canvases (filterable).
        - get_story_canvas: fetch a single canvas.
        - validate_project: check readiness.

        For multi‑step tasks, outline a brief plan; do not execute planning steps.
        """
    ).strip()


def _build_tools_wrappers(lc_tools_mod, tools, write_gate: dict[str, bool] | None = None) -> list[Any]:
    """Wrap a subset of read tools as LangChain tools.

    Each wrapper returns a JSON‑serializable dict with keys: success, data, warnings, errors.
    """
    # Prefer StructuredTool with explicit schemas; fall back to @tool if needed.
    try:
        from pydantic import BaseModel, Field  # type: ignore
        has_pydantic = True
    except Exception:
        has_pydantic = False

    ToolObjects: list[Any] = []
    write_gate = write_gate or {"enabled": False}

    if has_pydantic:
        from langchain.tools import StructuredTool  # type: ignore

        class GetProjectArgs(BaseModel):
            identifier: str = Field(..., description="Project UUID or name")

        def _get_project(identifier: str) -> dict[str, Any]:
            res = tools.get_project(identifier)
            return {
                "success": res.success,
                "data": res.data,
                "warnings": res.warnings,
                "errors": res.errors,
            }

        ToolObjects.append(
            StructuredTool.from_function(
                name="get_project",
                description="Destructiveness: read_only. Fetch project meta and time settings by id or name.",
                func=_get_project,
                args_schema=GetProjectArgs,
            )
        )

        class ListLocationsArgs(BaseModel):
            query: str | None = Field(None, description="Optional name search/prefix")

        def _list_locations(query: str | None = None) -> dict[str, Any]:
            res = tools.list_locations(query=query)
            return {
                "success": res.success,
                "data": res.data,
                "warnings": res.warnings,
                "errors": res.errors,
            }

        ToolObjects.append(
            StructuredTool.from_function(
                name="list_locations",
                description="Destructiveness: read_only. List locations (optionally filtered by name query).",
                func=_list_locations,
                args_schema=ListLocationsArgs,
            )
        )

        class ListCanvasesArgs(BaseModel):
            query: str | None = Field(None, description="Optional name search/prefix")
            location_id: str | None = Field(
                None, description="Optional filter by location UUID"
            )

        def _list_story_canvases(
            query: str | None = None, location_id: str | None = None
        ) -> dict[str, Any]:
            res = tools.list_story_canvases(query=query, location_id=location_id)
            return {
                "success": res.success,
                "data": res.data,
                "warnings": res.warnings,
                "errors": res.errors,
            }

        ToolObjects.append(
            StructuredTool.from_function(
                name="list_story_canvases",
                description="Destructiveness: read_only. List story canvases; filter by name or location.",
                func=_list_story_canvases,
                args_schema=ListCanvasesArgs,
            )
        )

        class GetCanvasArgs(BaseModel):
            identifier: str = Field(..., description="Canvas UUID or name")

        def _get_story_canvas(identifier: str) -> dict[str, Any]:
            res = tools.get_story_canvas(identifier)
            return {
                "success": res.success,
                "data": res.data,
                "warnings": res.warnings,
                "errors": res.errors,
            }

        ToolObjects.append(
            StructuredTool.from_function(
                name="get_story_canvas",
                description="Destructiveness: read_only. Get a story canvas with node and trigger details.",
                func=_get_story_canvas,
                args_schema=GetCanvasArgs,
            )
        )

        class ValidateArgs(BaseModel):
            pass

        def _validate_project() -> dict[str, Any]:
            res = tools.validate_project()
            return {
                "success": res.success,
                "data": res.data,
                "warnings": res.warnings,
                "errors": res.errors,
            }

        ToolObjects.append(
            StructuredTool.from_function(
                name="validate_project",
                description="Destructiveness: read_only. Validate project integrity for generation readiness.",
                func=_validate_project,
                args_schema=ValidateArgs,
            )
        )

        # ---------- Phase-2: write tool wrappers (guarded by write_gate) ----------

        class CreateLocationArgs(BaseModel):
            name: str = Field(..., description="Location name (unique within project)")
            description: str | None = Field(None, description="Optional description")
            location_type: str | None = Field(
                None, description="Optional location type (e.g., generic)"
            )

        def _create_location(
            name: str, description: str | None = None, location_type: str | None = None
        ) -> dict[str, Any]:
            if not write_gate.get("enabled"):
                return {
                    "success": False,
                    "data": {"preview": {"tool": "create_location", "name": name}},
                    "warnings": [
                        "Writes disabled. Use 'writes on' in REPL to enable writes."
                    ],
                    "errors": ["writes_disabled"],
                }
            res = tools.create_location(
                name=name, description=description, location_type=location_type
            )
            return {
                "success": res.success,
                "data": res.data,
                "warnings": res.warnings,
                "errors": res.errors,
            }

        ToolObjects.append(
            StructuredTool.from_function(
                name="create_location",
                description="Destructiveness: low_write. Create a new location (idempotent by project+name).",
                func=_create_location,
                args_schema=CreateLocationArgs,
            )
        )

        class CreateStoryCanvasArgs(BaseModel):
            name: str
            location_id: str
            content_blocks: list[str]
            exit_config: dict[str, Any] | None = None
            description: str | None = None

        def _create_story_canvas(
            name: str,
            location_id: str,
            content_blocks: list[str],
            exit_config: dict[str, Any] | None = None,
            description: str | None = None,
        ) -> dict[str, Any]:
            if not write_gate.get("enabled"):
                return {
                    "success": False,
                    "data": {
                        "preview": {
                            "tool": "create_story_canvas",
                            "name": name,
                            "location_id": location_id,
                        }
                    },
                    "warnings": [
                        "Writes disabled. Use 'writes on' in REPL to enable writes."
                    ],
                    "errors": ["writes_disabled"],
                }
            res = tools.create_story_canvas(
                name=name,
                location_id=location_id,
                content_blocks=content_blocks,
                exit_config=exit_config,
                description=description,
            )
            return {
                "success": res.success,
                "data": res.data,
                "warnings": res.warnings,
                "errors": res.errors,
            }

        ToolObjects.append(
            StructuredTool.from_function(
                name="create_story_canvas",
                description="Destructiveness: low_write. Create a canvas with a single node and trigger (one-node-per-canvas).",
                func=_create_story_canvas,
                args_schema=CreateStoryCanvasArgs,
            )
        )

        class UpdateStoryContentArgs(BaseModel):
            canvas_id: str
            content_blocks: list[str]
            exit_config: dict[str, Any] | None = None

        def _update_story_content(
            canvas_id: str, content_blocks: list[str], exit_config: dict[str, Any] | None = None
        ) -> dict[str, Any]:
            if not write_gate.get("enabled"):
                return {
                    "success": False,
                    "data": {
                        "preview": {"tool": "update_story_content", "canvas_id": canvas_id}
                    },
                    "warnings": [
                        "Writes disabled. Use 'writes on' in REPL to enable writes."
                    ],
                    "errors": ["writes_disabled"],
                }
            res = tools.update_story_content(
                canvas_id=canvas_id, content_blocks=content_blocks, exit_config=exit_config
            )
            return {
                "success": res.success,
                "data": res.data,
                "warnings": res.warnings,
                "errors": res.errors,
            }

        ToolObjects.append(
            StructuredTool.from_function(
                name="update_story_content",
                description="Destructiveness: low_write. Update content of a canvas's single node.",
                func=_update_story_content,
                args_schema=UpdateStoryContentArgs,
            )
        )

        class CreateTriggerScheduleArgs(BaseModel):
            canvas_id: str
            name: str
            weekdays: list[int]
            start_time: str
            end_time: str | None = None

        def _create_trigger_schedule(
            canvas_id: str,
            name: str,
            weekdays: list[int],
            start_time: str,
            end_time: str | None = None,
        ) -> dict[str, Any]:
            if not write_gate.get("enabled"):
                return {
                    "success": False,
                    "data": {
                        "preview": {
                            "tool": "create_trigger_schedule",
                            "canvas_id": canvas_id,
                            "name": name,
                        }
                    },
                    "warnings": [
                        "Writes disabled. Use 'writes on' in REPL to enable writes."
                    ],
                    "errors": ["writes_disabled"],
                }
            # Lightweight validation
            warnings: list[str] = []
            for d in weekdays:
                if d < 0 or d > 6:
                    warnings.append(f"Invalid weekday: {d}")
            if end_time and start_time >= end_time:
                warnings.append("End time should be after start time")
            res = tools.create_trigger_schedule(
                canvas_id=canvas_id,
                name=name,
                weekdays=weekdays,
                start_time=start_time,
                end_time=end_time,
            )
            return {
                "success": res.success,
                "data": res.data,
                "warnings": (res.warnings or []) + warnings,
                "errors": res.errors,
            }

        ToolObjects.append(
            StructuredTool.from_function(
                name="create_trigger_schedule",
                description="Destructiveness: low_write. Add a time-based schedule to a canvas trigger.",
                func=_create_trigger_schedule,
                args_schema=CreateTriggerScheduleArgs,
            )
        )

        class SetStartingCanvasArgs(BaseModel):
            canvas_id: str

        def _set_starting_canvas(canvas_id: str) -> dict[str, Any]:
            if not write_gate.get("enabled"):
                return {
                    "success": False,
                    "data": {
                        "preview": {"tool": "set_starting_canvas", "canvas_id": canvas_id}
                    },
                    "warnings": [
                        "Writes disabled. Use 'writes on' in REPL to enable writes."
                    ],
                    "errors": ["writes_disabled"],
                }
            res = tools.set_starting_canvas(canvas_id=canvas_id)
            return {
                "success": res.success,
                "data": res.data,
                "warnings": res.warnings,
                "errors": res.errors,
            }

        ToolObjects.append(
            StructuredTool.from_function(
                name="set_starting_canvas",
                description="Destructiveness: low_write. Set the project starting canvas (entry point).",
                func=_set_starting_canvas,
                args_schema=SetStartingCanvasArgs,
            )
        )

        return ToolObjects

    # Fallback: lightweight @tool wrappers without explicit schemas.
    from langchain.tools import tool  # type: ignore

    @tool("get_project")
    def get_project_tool(identifier: str) -> dict[str, Any]:
        """Fetch project meta and time settings by id or name."""
        res = tools.get_project(identifier)
        return {
            "success": res.success,
            "data": res.data,
            "warnings": res.warnings,
            "errors": res.errors,
        }

    @tool("list_locations")
    def list_locations_tool(query: str | None = None) -> dict[str, Any]:
        """List locations (optionally filtered by name query)."""
        res = tools.list_locations(query=query)
        return {
            "success": res.success,
            "data": res.data,
            "warnings": res.warnings,
            "errors": res.errors,
        }

    @tool("list_story_canvases")
    def list_story_canvases_tool(
        query: str | None = None, location_id: str | None = None
    ) -> dict[str, Any]:
        """List story canvases; filter by name or location."""
        res = tools.list_story_canvases(query=query, location_id=location_id)
        return {
            "success": res.success,
            "data": res.data,
            "warnings": res.warnings,
            "errors": res.errors,
        }

    @tool("get_story_canvas")
    def get_story_canvas_tool(identifier: str) -> dict[str, Any]:
        """Get a story canvas with node and trigger details."""
        res = tools.get_story_canvas(identifier)
        return {
            "success": res.success,
            "data": res.data,
            "warnings": res.warnings,
            "errors": res.errors,
        }

    @tool("validate_project")
    def validate_project_tool() -> dict[str, Any]:
        """Validate project integrity for generation readiness."""
        res = tools.validate_project()
        return {
            "success": res.success,
            "data": res.data,
            "warnings": res.warnings,
            "errors": res.errors,
        }

    return [
        get_project_tool,
        list_locations_tool,
        list_story_canvases_tool,
        get_story_canvas_tool,
        validate_project_tool,
        # Phase-2 write tools (guarded by write_gate)
        # Note: @tool wrappers don't support arg schemas; rely on docstrings.
        # If needed, prefer the Pydantic path above.
    ]


def _build_agent(project_id: str, write_gate: dict[str, bool]):
    """Construct the LangGraph ReAct agent and dependencies.

    Returns: (graph, tools_wrapped, snapshot_service)
    """
    # Dependencies
    if not getattr(settings, "OPENAI_API_KEY", None):
        raise CommandError("OPENAI_API_KEY is not set in Django settings.")

    langchain_openai = _require("langchain-openai", "langchain_openai")
    langgraph_prebuilt = _require("langgraph", "langgraph.prebuilt")
    langgraph_checkpoint = _require("langgraph", "langgraph.checkpoint.memory")

    ChatOpenAI = langchain_openai.ChatOpenAI
    create_react_agent = langgraph_prebuilt.create_react_agent
    MemorySaver = langgraph_checkpoint.MemorySaver

    tools, snapshot_svc, _ = _load_tooling(project_id)
    wrapped_tools = _build_tools_wrappers(langchain_openai, tools, write_gate)

    # Build LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=settings.OPENAI_API_KEY,
        temperature=0.2,
    )

    # Acquire snapshot for state modifier
    snapshot = snapshot_svc.get()
    modifier = _state_modifier(snapshot, writes_enabled=bool(write_gate.get("enabled")))

    # Checkpointer (in-memory for Dev)
    checkpointer = MemorySaver()

    graph = create_react_agent(
        llm=llm,
        tools=wrapped_tools,
        state_modifier=modifier,
        checkpointer=checkpointer,
    )
    return graph, wrapped_tools, snapshot_svc


def _format_tools_manifest(wrapped_tools: list[Any]) -> list[dict[str, str]]:
    out = []
    for t in wrapped_tools:
        try:
            out.append({"name": t.name, "description": t.description})
        except Exception:
            out.append({"name": str(getattr(t, "name", "?")), "description": "-"})
    return out


def _print_help():
    msg = """
Commands:
  help            Show this help
  tools           Show available tools (read‑only in Phase‑1)
  writes on|off   Toggle guarded writes (Phase‑2)
  tps             Show tiny project snapshot summary
  run <text>      Ask the agent to act (read‑only)
  validate        Validate project via direct adapter
  generate        Generate twee content via direct adapter
  quit            Exit
"""
    print(textwrap.dedent(msg).strip())


class Command(BaseCommand):
    help = "Run Elora Codex (Phase‑1) — LangGraph ReAct agent with read‑only tools"

    def add_arguments(self, parser):
        parser.add_argument("--project-id", required=True, help="Project UUID")

    def handle(self, *args, **options):
        project_id = options["project_id"]

        # Write gate (default off for safety); toggle via REPL
        write_gate: dict[str, bool] = {"enabled": False}

        # Build agent and deps
        graph, wrapped_tools, snapshot_svc = _build_agent(project_id, write_gate)

        # Also keep direct adapters for validate/generate commands
        tools, _, _ = _load_tooling(project_id)

        print(
            "Elora Codex — Phase‑2 (LangGraph ReAct, reads + guarded writes). Type 'help' to begin."
        )

        while True:
            try:
                raw = input("elora-codex> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nBye.")
                return

            if not raw:
                continue

            cmd, *rest = raw.split(" ", 1)
            arg = rest[0].strip() if rest else ""

            if cmd in {"quit", "exit"}:
                print("Bye.")
                return
            if cmd == "help":
                _print_help()
                continue
            if cmd == "tools":
                print(json.dumps(_format_tools_manifest(wrapped_tools), indent=2))
                continue
            if cmd == "writes":
                if arg.lower() in {"on", "enable", "enabled"}:
                    write_gate["enabled"] = True
                    # Rebuild agent to refresh state modifier context
                    graph, wrapped_tools, snapshot_svc = _build_agent(
                        project_id, write_gate
                    )
                    print("Writes ENABLED for this session. Use responsibly.")
                    continue
                if arg.lower() in {"off", "disable", "disabled"}:
                    write_gate["enabled"] = False
                    graph, wrapped_tools, snapshot_svc = _build_agent(
                        project_id, write_gate
                    )
                    print("Writes DISABLED for this session.")
                    continue
                print(
                    f"Writes are {'ENABLED' if write_gate['enabled'] else 'DISABLED'}. Use 'writes on' or 'writes off'."
                )
                continue
            if cmd == "tps":
                tps = snapshot_svc.get()
                summary = {
                    "project_name": getattr(tps, "project_name", None),
                    "starting_canvas_id": getattr(tps, "starting_canvas_id", None),
                    "counts": getattr(tps, "counts", {}),
                    "locations_index": getattr(tps, "locations_index", [])[:5],
                    "story_canvases": getattr(tps, "story_canvases", [])[:5],
                }
                print(json.dumps(summary, indent=2))
                continue
            if cmd == "validate":
                res = tools.validate_project()
                if res.success:
                    print("✅ Valid project")
                    print(json.dumps(res.data or {}, indent=2))
                else:
                    print("❌ Validation failed")
                    if res.errors:
                        print("Errors:", "; ".join(res.errors))
                    if res.warnings:
                        print("Warnings:", "; ".join(res.warnings))
                continue
            if cmd == "generate":
                res = tools.generate_game_twee()
                if res.success:
                    print("✅ Generated twee")
                    print(json.dumps(res.data or {}, indent=2))
                else:
                    print("❌ Generation failed")
                    if res.errors:
                        print("Errors:", "; ".join(res.errors))
                continue

            if cmd == "run":
                if not arg:
                    print("Usage: run <text>")
                    continue
                # Refresh modifier when snapshot changes
                tps = snapshot_svc.get()
                # Invoke LangGraph agent
                try:
                    result = graph.invoke(
                        {"messages": [("user", arg)]},
                        config={"configurable": {"thread_id": f"proj:{project_id}"}},
                    )
                except Exception as e:
                    raise CommandError(f"Agent invocation failed: {e}")

                # Extract last assistant message if present
                try:
                    messages = result.get("messages") or []
                    final_text = None
                    if messages:
                        last = messages[-1]
                        # Support for different msg types
                        final_text = getattr(last, "content", None)
                        if isinstance(final_text, list):
                            # LC often wraps content parts; join text entries
                            final_text = "\n".join(
                                x.get("text", "") if isinstance(x, dict) else str(x)
                                for x in final_text
                            ).strip()
                    if not final_text:
                        final_text = json.dumps(result, indent=2)[:2000]
                except Exception:
                    final_text = json.dumps(result, indent=2)[:2000]
                print(final_text)
                continue

            # Unknown command
            print("Unknown command. Type 'help' for options.")
