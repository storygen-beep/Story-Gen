import json
import uuid
from datetime import time
from typing import Any, Optional

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Exists, OuterRef

from apps.characters.models import Character
from apps.npcs.models import NPC

# ===== Model Imports (explicit; no dynamic discovery) =====
from apps.projects.models import Project
from apps.stories.models import (
    CanvasTrigger,
    StoryCanvas,
    TriggerSchedule,
)
from apps.world.models import Location

# ========= Utility helpers =========

def _uuid(val: str) -> uuid.UUID:
    try:
        return uuid.UUID(str(val))
    except Exception:
        raise CommandError(f"Not a valid UUID: {val}")


def _parse_weekdays(value: Any) -> list[int]:
    """Accepts list[int] or comma-separated string of 0..6."""
    if value is None:
        return []
    if isinstance(value, list):
        days = value
    else:
        days = [int(x.strip()) for x in str(value).split(',') if x.strip()]
    for d in days:
        if d < 0 or d > 6:
            raise CommandError("weekday must be in 0..6 (0=Monday)")
    return days


def _parse_time(val: Optional[str]) -> Optional[time]:
    if not val:
        return None
    try:
        hh, mm = (int(x) for x in val.split(":", 1))
        return time(hh, mm)
    except Exception:
        raise CommandError(f"Invalid time '{val}'. Use HH:MM (24h)")


# ========= Snapshot Service (Tiny Project Snapshot) =========
class SnapshotService:
    """
    Builds a small, schema-accurate snapshot used by the agent for grounding.
    Only uses fields defined in our backend schema and generation pipeline.
    """

    def __init__(self, project: Project):
        self.project = project

    def get(self) -> dict[str, Any]:
        proj = self.project

        # Locations index (id, name, type, parent_id)
        locations_qs = (
            Location.objects.filter(project=proj)
            .select_related("parent_location")
            .only("id", "name", "location_type", "parent_location")
            .order_by("name")
        )
        locations_index = [
            {
                "id": str(loc.id),
                "name": loc.name,
                "type": loc.location_type,
                "parent_id": str(loc.parent_location_id) if loc.parent_location_id else None,
            }
            for loc in locations_qs
        ]

        # Canvases (hot subset): sort by -is_favorite, -updated_at (if present), -node_count
        canvases_qs = (
            StoryCanvas.objects.filter(project=proj)
            .annotate(has_trigger=Exists(CanvasTrigger.objects.filter(canvas_id=OuterRef("pk"))))
            .only("id", "name", "node_count", "is_favorite")
            .order_by("-is_favorite", "-node_count", "name")[:20]
        )
        hot_canvases = [
            {
                "id": str(cv.id),
                "name": cv.name,
                "node_count": cv.node_count,
                "has_trigger": bool(getattr(cv, "has_trigger", False)),
            }
            for cv in canvases_qs
        ]

        # Main character (OneToOne with project) — may not exist yet
        main_char = None
        try:
            character = Character.objects.select_related("current_location").get(project=proj)
            main_char = {
                "id": str(character.id),
                "name": character.name,
                "location_id": str(character.current_location_id) if character.current_location_id else None,
            }
        except Character.DoesNotExist:
            main_char = None

        # Counts are project-scoped
        counts = {
            "total_canvases": StoryCanvas.objects.filter(project=proj).count(),
            "total_locations": Location.objects.filter(project=proj).count(),
            "total_npcs": NPC.objects.filter(project=proj).count(),
        }

        return {
            "project_meta": {
                "id": str(proj.id),
                "name": proj.name,
                "starting_canvas_id": str(proj.starting_canvas_id) if proj.starting_canvas_id else None,
            },
            "locations_index": locations_index,
            "main_character": main_char,
            "hot_canvases": hot_canvases,
            "counts": counts,
        }


# ========= Tools (deterministic adapters; schema-correct) =========
class Tools:
    def __init__(self, project: Project):
        self.project = project

    # ----- Reads
    def list_canvases(self, with_trigger: Optional[bool] = None) -> list[dict[str, Any]]:
        qs = (
            StoryCanvas.objects.filter(project=self.project)
            .annotate(has_trigger=Exists(CanvasTrigger.objects.filter(canvas_id=OuterRef("pk"))))
            .only("id", "name", "node_count", "is_valid", "is_favorite")
            .order_by("name")
        )
        if with_trigger is True:
            qs = qs.filter(canvastrigger__isnull=False)
        elif with_trigger is False:
            qs = qs.filter(canvastrigger__isnull=True)
        out = []
        for cv in qs:
            out.append(
                {
                    "id": str(cv.id),
                    "name": cv.name,
                    "node_count": cv.node_count,
                    "is_valid": cv.is_valid,
                    "has_trigger": bool(getattr(cv, "has_trigger", False)),
                }
            )
        return out

    def get_canvas(self, canvas_id: uuid.UUID) -> dict[str, Any]:
        cv = (
            StoryCanvas.objects.select_related("project")
            .prefetch_related("nodes", "flags")
            .get(id=canvas_id, project=self.project)
        )
        trigger = getattr(cv, "trigger", None)  # OneToOne, may not exist
        return {
            "id": str(cv.id),
            "name": cv.name,
            "node_count": cv.node_count,
            "has_trigger": bool(trigger),
            "flags": [
                {"flag_name": f.flag_name, "default_value": f.default_value}
                for f in cv.flags.all()
            ],
            "nodes": [
                {"id": str(n.id), "name": n.name}  # keep it light
                for n in cv.nodes.all()
            ],
        }

    def list_locations(self, name_prefix: Optional[str] = None) -> list[dict[str, Any]]:
        qs = Location.objects.filter(project=self.project).only("id", "name", "location_type")
        if name_prefix:
            qs = qs.filter(name__istartswith=name_prefix)
        return [
            {"id": str(loc.id), "name": loc.name, "type": loc.location_type}
            for loc in qs.order_by("name")
        ]

    def list_npcs(self) -> list[dict[str, Any]]:
        return [
            {"id": str(n.id), "name": n.name, "status": n.status}
            for n in NPC.objects.filter(project=self.project).only("id", "name", "status").order_by("name")
        ]

    def get_player_character(self) -> Optional[dict[str, Any]]:
        try:
            c = Character.objects.get(project=self.project)
            return {"id": str(c.id), "name": c.name}
        except Character.DoesNotExist:
            return None

    # ----- Writes
    @transaction.atomic
    def set_starting_canvas(self, canvas_id: uuid.UUID) -> dict[str, Any]:
        cv = StoryCanvas.objects.get(id=canvas_id, project=self.project)
        self.project.starting_canvas = cv
        self.project.save(update_fields=["starting_canvas"])
        return {"ok": True, "starting_canvas_id": str(cv.id)}

    @transaction.atomic
    def add_trigger(
        self,
        canvas_id: uuid.UUID,
        *,
        location_id: Optional[uuid.UUID] = None,
        is_active: bool = True,
        is_activity: bool = False,
        is_repeatable: bool = True,
        max_triggers_per_day: Optional[int] = None,
        schedules: Optional[list[dict[str, Any]]] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        cv = StoryCanvas.objects.get(id=canvas_id, project=self.project)

        # Validate location (optional). Note: CanvasTrigger.location_id is a UUIDField, not FK.
        if location_id:
            try:
                Location.objects.get(id=location_id, project=self.project)
            except Location.DoesNotExist:
                raise CommandError("location_id does not exist in this project")

        trig, created = CanvasTrigger.objects.get_or_create(
            canvas=cv,
            defaults={
                "location_id": location_id,
                "is_active": is_active,
                "is_activity": is_activity,
                "is_repeatable": is_repeatable,
                "max_triggers_per_day": max_triggers_per_day,
                "metadata": metadata or {},
            },
        )
        if not created:
            # Patch fields on existing trigger
            update_fields = []
            if location_id is not None:
                trig.location_id = location_id
                update_fields.append("location_id")
            trig.is_active = is_active
            trig.is_activity = is_activity
            trig.is_repeatable = is_repeatable
            update_fields += ["is_active", "is_activity", "is_repeatable"]
            trig.max_triggers_per_day = max_triggers_per_day
            update_fields.append("max_triggers_per_day")
            if metadata is not None:
                trig.metadata = metadata
                update_fields.append("metadata")
            trig.save(update_fields=update_fields)

        # Replace schedules if provided
        created_schedules = []
        if schedules is not None:
            TriggerSchedule.objects.filter(trigger=trig).delete()
            for sc in schedules:
                weekdays = _parse_weekdays(sc.get("weekdays"))
                start_t = _parse_time(sc.get("start_time"))
                end_t = _parse_time(sc.get("end_time"))
                if start_t and end_t and end_t <= start_t:
                    raise CommandError("end_time must be after start_time")
                created_schedules.append(
                    TriggerSchedule.objects.create(
                        trigger=trig,
                        name=sc.get("name") or "default",
                        weekdays=weekdays,
                        start_time=start_t or time(0, 0),
                        end_time=end_t,
                    )
                )

        return {
            "ok": True,
            "trigger_id": str(trig.id),
            "created": created,
            "schedules": [
                {
                    "id": str(s.id),
                    "name": s.name,
                    "weekdays": s.weekdays,
                    "start_time": s.start_time.isoformat(),
                    "end_time": s.end_time.isoformat() if s.end_time else None,
                }
                for s in (created_schedules or TriggerSchedule.objects.filter(trigger=trig))
            ],
        }

    @transaction.atomic
    def connect_locations(
        self,
        from_location_id: uuid.UUID,
        to_location_id: uuid.UUID,
        *,
        connection_type: str = "path",
        is_bidirectional: bool = True,
        properties: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        if from_location_id == to_location_id:
            raise CommandError("from_location and to_location cannot be the same")

        try:
            src = Location.objects.get(id=from_location_id, project=self.project)
            dst = Location.objects.get(id=to_location_id, project=self.project)
        except Location.DoesNotExist:
            raise CommandError("Both locations must exist in this project")

        # New model: add entry from src to dst; add reverse if bidirectional
        src.entry_connections.add(dst)
        if is_bidirectional:
            dst.entry_connections.add(src)

        return {
            "ok": True,
            "connection": {
                "from": str(src.id),
                "to": str(dst.id),
                "type": connection_type,
                "is_bidirectional": is_bidirectional,
            },
            "created": True,
        }


# ========= Minimal Planner/Executor (optional LLM; safe fallback) =========
class SimplePlanner:
    """Very small intent router so the CLI works even without LLM packages."""

    def __init__(self, tools: Tools, snapshot: dict[str, Any]):
        self.tools = tools
        self.snapshot = snapshot

    def plan(self, user_text: str) -> tuple[str, dict[str, Any]]:
        t = user_text.strip().lower()
        # Simple patterns — prioritize read-only
        if t in {"snapshot", ":snapshot"}:
            return ("snapshot", {})
        if t.startswith("list canvases"):
            wt = None
            if " with trigger" in t:
                wt = True
            if " without trigger" in t:
                wt = False
            return ("list_canvases", {"with_trigger": wt})
        if t.startswith("list locations"):
            return ("list_locations", {})
        if t.startswith("list npcs"):
            return ("list_npcs", {})
        if t.startswith("player") or t.startswith("character"):
            return ("get_player_character", {})
        if t.startswith("set start"):
            # set start <canvas_id>
            parts = user_text.strip().split()
            if len(parts) >= 3:
                return ("set_starting_canvas", {"canvas_id": _uuid(parts[2])})
        if t.startswith("connect"):
            # connect <from_id> <to_id>
            parts = user_text.strip().split()
            if len(parts) >= 3:
                return (
                    "connect_locations",
                    {
                        "from_location_id": _uuid(parts[1]),
                        "to_location_id": _uuid(parts[2]),
                    },
                )
        if t.startswith("add trigger"):
            # add trigger <canvas_id> <location_id?> schedules='[{...}]'
            # Accept a JSON blob after schedules=
            try:
                tokens = user_text.strip().split()
                canvas_id = _uuid(tokens[2])
                location_id = None
                if len(tokens) >= 4 and not tokens[3].startswith("schedules="):
                    location_id = _uuid(tokens[3])
                schedules = None
                if "schedules=" in user_text:
                    j = user_text.split("schedules=", 1)[1].strip()
                    if j.startswith("'") or j.startswith('"'):
                        j = j[1:-1]
                    schedules = json.loads(j)
                return (
                    "add_trigger",
                    {
                        "canvas_id": canvas_id,
                        "location_id": location_id,
                        "schedules": schedules,
                    },
                )
            except Exception as e:
                raise CommandError(f"Could not parse add trigger command: {e}")
        return ("unknown", {"raw": user_text})

    def execute(self, tool_name: str, args: dict[str, Any]) -> dict[str, Any]:
        if tool_name == "snapshot":
            return self.snapshot
        if not hasattr(self.tools, tool_name):
            return {"error": f"No such tool: {tool_name}", "tool": tool_name}
        func = getattr(self.tools, tool_name)
        return func(**args)


# ========= Management Command =========
class Command(BaseCommand):
    help = (
        "Open Elora CLI for a project. Example: \n"
        "  python manage.py elora_gpt5_2 --project-id <uuid>\n\n"
        "Commands (natural-ish):\n"
        "  snapshot | :snapshot\n"
        "  list canvases [with trigger|without trigger]\n"
        "  list locations\n"
        "  list npcs\n"
        "  player  (or 'character')\n"
        "  set start <canvas_id>\n"
        "  connect <from_location_id> <to_location_id>\n"
        "  add trigger <canvas_id> [<location_id>] schedules='[{..}]'\n"
        "  :quit to exit\n"
    )

    def add_arguments(self, parser):
        parser.add_argument("--project-id", required=True, help="Project UUID")

    def handle(self, *args, **options):
        project_id = _uuid(options["--project-id"]) if "--project-id" in options else _uuid(options["project_id"])

        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise CommandError(f"Project not found: {project_id}")

        # Load snapshot once; refresh on demand in the loop if needed
        snap = SnapshotService(project).get()
        tools = Tools(project)
        planner = SimplePlanner(tools, snap)

        self.stdout.write(self.style.SUCCESS(f"Elora CLI — project: {project.name} ({project.id})"))
        self.stdout.write("Type ':quit' to exit. Type 'help' for commands.")

        while True:
            try:
                line = input("elora> ").strip()
            except (KeyboardInterrupt, EOFError):
                self.stdout.write("")
                break

            if not line:
                continue
            if line in {":q", ":quit", ":exit", "quit", "exit"}:
                break
            if line in {"help", ":help"}:
                self.stdout.write(self.help)
                continue
            if line in {":refresh", "refresh snapshot"}:
                snap = SnapshotService(project).get()
                planner.snapshot = snap
                self.stdout.write(self.style.SUCCESS("Snapshot refreshed."))
                continue

            # Plan → Execute
            try:
                tool_name, args_dict = planner.plan(line)
                if tool_name == "unknown":
                    self.stdout.write("Unrecognized command. Type 'help' for examples.")
                    continue
                result = planner.execute(tool_name, args_dict)
                self._print_result(result)
            except CommandError as ce:
                self.stdout.write(self.style.ERROR(str(ce)))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error: {e}"))

        self.stdout.write(self.style.WARNING("Goodbye."))

    # Pretty printer for dict/list results
    def _print_result(self, obj: Any, indent: int = 0):
        if isinstance(obj, dict) or isinstance(obj, list):
            self.stdout.write(json.dumps(obj, indent=2, default=str))
        else:
            self.stdout.write(str(obj))
