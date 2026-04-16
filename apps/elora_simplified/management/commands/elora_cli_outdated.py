#!/usr/bin/env python3
"""
Elora: narrative-first ReAct agent — single-file CLI + Django management command (DB-backed).

USAGE (CLI):
  python manage.py elora_gpt5 --project-id <UUID>
  # Interactive REPL opens. Type 'help' for commands, 'quit' to exit.

Design notes:
- Uses Django settings.OPENAI_API_KEY (no env var needed)
- Model discovery via settings.ELORA_MODEL_MAP (override in your settings.py)
- Dynamic ORM adapters inspect model fields to avoid hardcoding
- Implements Tiny Project Snapshot (TPS), Planner+, Safety Gate, Executor, Validator, Synthesizer
- Tools are minimal but representative; expand as your project grows
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

DEFAULT_ELORA_MODEL_MAP = {
    # Override these in settings.ELORA_MODEL_MAP to match your project.
    # Format: "ModelAlias": "app_label.ModelName"
    # Use the Django app label (usually the last segment of AppConfig.name)
    # rather than the full Python path.
    "Project": "projects.Project",
    "Location": "world.Location",
    "Canvas": "stories.StoryCanvas",
    "Character": "characters.Character",
    "Trigger": "stories.Trigger",
    "Schedule": "stories.Schedule",  # if schedules are separate; else handled via Trigger JSON
}


def get_model(alias: str):
    model_map = getattr(settings, "ELORA_MODEL_MAP", DEFAULT_ELORA_MODEL_MAP)
    if alias not in model_map:
        raise CommandError(f"ELORA_MODEL_MAP missing alias: {alias}")
    dotted = model_map[alias]
    try:
        app_label, model_name = dotted.split(".")
    except ValueError:
        raise CommandError(
            f"Invalid ELORA_MODEL_MAP target '{dotted}' for alias '{alias}'. Use 'app_label.ModelName'."
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


# Very small shim; you can swap with openai>=1.x or your own client
class OpenAIShim:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def chat(
        self,
        messages: list[dict[str, str]],
        model: str = "gpt-5.1-mini",
        temperature: float = 0.2,
        max_tokens: int = 800,
    ) -> str:
        """
        Replace with your real OpenAI client call. This shim is a stub interface.
        """
        try:
            import openai  # type: ignore
        except Exception:
            raise CommandError(
                "openai package is not installed; pip install openai to run LLM calls."
            )

        openai.api_key = self.api_key
        # Adjust to your org/API; below is an example that works with openai>=0.28
        resp = openai.ChatCompletion.create(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            messages=messages,
        )
        return resp["choices"][0]["message"]["content"]


# -----------------------------
# REACT AGENT BUILDING BLOCKS
# -----------------------------


@dataclass
class TinyProjectSnapshot:
    project_id: str
    project_name: str
    starting_canvas_id: Optional[str] = None
    locations_index: list[dict[str, Any]] = field(default_factory=list)
    main_characters: list[dict[str, Any]] = field(default_factory=list)
    hot_canvases: list[dict[str, Any]] = field(default_factory=list)
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
# DYNAMIC ORM HELPERS
# -----------------------------


def find_field_name(model, candidates: list[str]) -> Optional[str]:
    """
    Try to find a field on model whose name matches one of candidates (case-insensitive).
    """
    fields = {f.name.lower(): f for f in model._meta.get_fields() if hasattr(f, "name")}
    for name in candidates:
        ln = name.lower()
        if ln in fields:
            return fields[ln].name
    # Allow partial contains (e.g., 'title' vs 'name')
    for k in fields.keys():
        for cand in candidates:
            if cand.lower() in k:
                return k
    return None


def natural_key_filter(model, **kwargs):
    """
    Builds a filter dict containing only existing fields.
    """
    filt = {}
    for k, v in kwargs.items():
        if hasattr(model, k):
            filt[k] = v
    return filt


# -----------------------------
# TOOL ADAPTERS (ORM)
# -----------------------------


class Tools:
    """
    Deterministic, DB-backed tool adapters. No LLM here.
    """

    def __init__(self, project_id: str):
        self.project_id = str(project_id)
        self.Project = get_model("Project")
        self.Location = get_model("Location")
        self.Canvas = get_model("Canvas")
        self.Character = get_model("Character")
        # Triggers/Schedule are optional depending on your schema:
        try:
            self.Trigger = get_model("Trigger")
        except Exception:
            self.Trigger = None
        try:
            self.Schedule = get_model("Schedule")
        except Exception:
            self.Schedule = None

        # Discover common field names dynamically
        self._location_name = find_field_name(self.Location, ["name", "title", "label"])
        self._location_type = find_field_name(
            self.Location, ["type", "kind", "category"]
        )
        self._location_parent = find_field_name(
            self.Location, ["parent", "parent_id", "container", "container_id"]
        )
        self._location_project_fk = find_field_name(
            self.Location, ["project", "project_id"]
        )

        self._canvas_name = find_field_name(self.Canvas, ["name", "title", "label"])
        self._canvas_project_fk = find_field_name(
            self.Canvas, ["project", "project_id"]
        )
        self._canvas_location_fk = find_field_name(
            self.Canvas, ["location", "location_id"]
        )
        self._canvas_node_count = find_field_name(
            self.Canvas, ["node_count", "nodes", "node_total"]
        )
        self._canvas_has_trigger = find_field_name(
            self.Canvas, ["has_trigger", "triggered"]
        )

        self._character_name = find_field_name(self.Character, ["name"])
        self._character_role = find_field_name(self.Character, ["role", "short_role"])
        self._character_project_fk = find_field_name(
            self.Character, ["project", "project_id"]
        )

    # ---------- READS ----------

    def list_locations(self, query: Optional[str] = None) -> ToolResult:
        qs = self.Location.objects
        if self._location_project_fk:
            qs = qs.filter(**{self._location_project_fk: self.project_id})
        if query and self._location_name:
            qs = qs.filter(**{f"{self._location_name}__icontains": query})
        qs = qs.order_by(self._location_name or "id")[:25]
        data = []
        for x in qs:
            data.append(
                {
                    "id": str(x.pk),
                    "name": getattr(x, self._location_name, None),
                    "type": getattr(x, self._location_type, None),
                    "parent_id": (
                        getattr(x, self._location_parent, None)
                        if self._location_parent
                        else None
                    ),
                }
            )
        return ToolResult(True, data=data, _tool_metadata={"name": "list_locations"})

    def get_location(self, identifier: str) -> ToolResult:
        qs = self.Location.objects
        if self._location_project_fk:
            qs = qs.filter(**{self._location_project_fk: self.project_id})
        obj = None
        if uuid_like(identifier):
            obj = qs.filter(pk=identifier).first()
        if not obj and self._location_name:
            obj = qs.filter(**{self._location_name: identifier}).first()
        if not obj:
            return ToolResult(
                False,
                errors=[f"Location not found: {identifier}"],
                _tool_metadata={"name": "get_location"},
            )
        return ToolResult(
            True,
            data={
                "id": str(obj.pk),
                "name": getattr(obj, self._location_name, None),
                "type": getattr(obj, self._location_type, None),
                "parent_id": (
                    getattr(obj, self._location_parent, None)
                    if self._location_parent
                    else None
                ),
            },
            _tool_metadata={"name": "get_location"},
        )

    def list_canvases(
        self, query: Optional[str] = None, location_id: Optional[str] = None
    ) -> ToolResult:
        qs = self.Canvas.objects
        if self._canvas_project_fk:
            qs = qs.filter(**{self._canvas_project_fk: self.project_id})
        if query and self._canvas_name:
            qs = qs.filter(**{f"{self._canvas_name}__icontains": query})
        if location_id and self._canvas_location_fk:
            qs = qs.filter(**{self._canvas_location_fk: location_id})
        qs = qs.order_by(self._canvas_name or "id")[:25]
        data = []
        for x in qs:
            data.append(
                {
                    "id": str(x.pk),
                    "name": getattr(x, self._canvas_name, None),
                    "location_id": (
                        getattr(x, self._canvas_location_fk, None)
                        if self._canvas_location_fk
                        else None
                    ),
                    "node_count": getattr(x, self._canvas_node_count, None),
                    "has_trigger": getattr(x, self._canvas_has_trigger, None),
                }
            )
        return ToolResult(True, data=data, _tool_metadata={"name": "list_canvases"})

    def get_canvas(self, identifier: str) -> ToolResult:
        qs = self.Canvas.objects
        if self._canvas_project_fk:
            qs = qs.filter(**{self._canvas_project_fk: self.project_id})
        obj = None
        if uuid_like(identifier):
            obj = qs.filter(pk=identifier).first()
        if not obj and self._canvas_name:
            obj = qs.filter(**{self._canvas_name: identifier}).first()
        if not obj:
            return ToolResult(
                False,
                errors=[f"Canvas not found: {identifier}"],
                _tool_metadata={"name": "get_canvas"},
            )
        return ToolResult(
            True,
            data={
                "id": str(obj.pk),
                "name": getattr(obj, self._canvas_name, None),
                "location_id": (
                    getattr(obj, self._canvas_location_fk, None)
                    if self._canvas_location_fk
                    else None
                ),
                "node_count": getattr(obj, self._canvas_node_count, None),
                "has_trigger": getattr(obj, self._canvas_has_trigger, None),
            },
            _tool_metadata={"name": "get_canvas"},
        )

    def list_characters(self, query: Optional[str] = None) -> ToolResult:
        qs = self.Character.objects
        if self._character_project_fk:
            qs = qs.filter(**{self._character_project_fk: self.project_id})
        if query and self._character_name:
            qs = qs.filter(**{f"{self._character_name}__icontains": query})
        qs = qs.order_by(self._character_name or "id")[:25]
        data = []
        for x in qs:
            data.append(
                {
                    "id": str(x.pk),
                    "name": getattr(x, self._character_name, None),
                    "short_role": getattr(x, self._character_role, None),
                }
            )
        return ToolResult(True, data=data, _tool_metadata={"name": "list_characters"})

    # ---------- WRITES ----------

    @transaction.atomic
    def create_location(
        self, name: str, type: Optional[str] = None, parent_id: Optional[str] = None
    ) -> ToolResult:
        kwargs = {}
        if self._location_name:
            kwargs[self._location_name] = name
        if self._location_type and type is not None:
            kwargs[self._location_type] = type
        if self._location_parent and parent_id:
            kwargs[self._location_parent] = parent_id
        if self._location_project_fk:
            kwargs[self._location_project_fk] = self.project_id

        # Idempotency by natural key (project + name)
        filt = {}
        if self._location_project_fk:
            filt[self._location_project_fk] = self.project_id
        if self._location_name:
            filt[self._location_name] = name
        existing = self.Location.objects.filter(**filt).first() if filt else None
        if existing:
            return ToolResult(
                True,
                data={"id": str(existing.pk), "created": False},
                warnings=["Location already existed."],
                _tool_metadata={"name": "create_location"},
            )

        obj = self.Location.objects.create(**kwargs)
        return ToolResult(
            True,
            data={"id": str(obj.pk), "created": True},
            _tool_metadata={"name": "create_location"},
        )

    @transaction.atomic
    def create_canvas(
        self, name: str, location_id: str, narrative_intent: Optional[str] = None
    ) -> ToolResult:
        kwargs = {}
        if self._canvas_name:
            kwargs[self._canvas_name] = name
        if self._canvas_location_fk:
            kwargs[self._canvas_location_fk] = location_id
        if self._canvas_project_fk:
            kwargs[self._canvas_project_fk] = self.project_id
        # You may have a narrative/intent field; discover if present:
        canvas_intent_field = find_field_name(
            self.Canvas, ["narrative_intent", "intent", "summary"]
        )
        if canvas_intent_field and narrative_intent:
            kwargs[canvas_intent_field] = narrative_intent

        # One-node-per-canvas policy (idempotency by project+name)
        filt = {}
        if self._canvas_project_fk:
            filt[self._canvas_project_fk] = self.project_id
        if self._canvas_name:
            filt[self._canvas_name] = name
        existing = self.Canvas.objects.filter(**filt).first() if filt else None
        if existing:
            return ToolResult(
                False,
                errors=[
                    "Canvas already exists (one-node-per-canvas policy). Use an update/overwrite tool."
                ],
                _tool_metadata={"name": "create_canvas"},
            )

        obj = self.Canvas.objects.create(**kwargs)
        return ToolResult(
            True,
            data={"id": str(obj.pk), "created": True},
            _tool_metadata={"name": "create_canvas"},
        )

    # Example placeholder: you can implement bidirectional edges per your schema (edge table or M2M)
    @transaction.atomic
    def connect_locations(
        self, a_id: str, b_id: str, bidirectional: bool = True
    ) -> ToolResult:
        """
        Replace with your graph edge creation logic (e.g., LocationConnection model).
        Here we only return a normalized success stub so the validator can be wired later.
        """
        return ToolResult(
            True,
            data={"a_id": a_id, "b_id": b_id, "bidirectional": bidirectional},
            _tool_metadata={"name": "connect_locations"},
        )

    @transaction.atomic
    def add_trigger(
        self, location_id: str, schedules: list[dict[str, Any]], is_active: bool = True
    ) -> ToolResult:
        if not self.Trigger:
            return ToolResult(
                False,
                errors=["Trigger model not configured."],
                _tool_metadata={"name": "add_trigger"},
            )
        # Try common fields dynamically
        Trigger = self.Trigger
        trig_loc_fk = find_field_name(Trigger, ["location", "location_id"])
        trig_proj_fk = find_field_name(Trigger, ["project", "project_id"])
        trig_active = find_field_name(Trigger, ["is_active", "active"])
        trig_schedules = find_field_name(
            Trigger, ["schedules", "schedule", "time_windows"]
        )

        kwargs = {}
        if trig_loc_fk:
            kwargs[trig_loc_fk] = location_id
        if trig_proj_fk:
            kwargs[trig_proj_fk] = self.project_id
        if trig_active:
            kwargs[trig_active] = is_active
        if trig_schedules:
            kwargs[trig_schedules] = schedules

        obj = Trigger.objects.create(**kwargs)
        return ToolResult(
            True,
            data={"id": str(obj.pk), "created": True},
            _tool_metadata={"name": "add_trigger"},
        )


# -----------------------------
# TOOL MANIFEST
# -----------------------------

TOOL_MANIFEST: dict[str, dict[str, Any]] = {
    "list_locations": {
        "args_schema": {"query": "str?"},
        "destructiveness": "read_only",
        "docs": "List up to 25 locations in the project filtered by name (icontains).",
    },
    "get_location": {
        "args_schema": {"identifier": "str"},  # id or exact name
        "destructiveness": "read_only",
        "docs": "Resolve a location by id (UUID) or exact name.",
    },
    "list_canvases": {
        "args_schema": {"query": "str?", "location_id": "str?"},
        "destructiveness": "read_only",
        "docs": "List up to 25 canvases; optionally filter by location.",
    },
    "get_canvas": {
        "args_schema": {"identifier": "str"},
        "destructiveness": "read_only",
        "docs": "Resolve a canvas by id or exact name.",
    },
    "list_characters": {
        "args_schema": {"query": "str?"},
        "destructiveness": "read_only",
        "docs": "List up to 25 characters in the project.",
    },
    "create_location": {
        "args_schema": {"name": "str", "type": "str?", "parent_id": "str?"},
        "destructiveness": "low_write",
        "docs": "Create a location (idempotent by project+name).",
        "post_invariants": ["location_exists"],
    },
    "create_canvas": {
        "args_schema": {
            "name": "str",
            "location_id": "str",
            "narrative_intent": "str?",
        },
        "destructiveness": "low_write",
        "docs": "Create a canvas for a location (one-node-per-canvas policy).",
        "post_invariants": ["canvas_exists", "one_node_per_canvas"],
    },
    "connect_locations": {
        "args_schema": {"a_id": "str", "b_id": "str", "bidirectional": "bool?"},
        "destructiveness": "low_write",
        "docs": "Connect two locations; validator enforces bidirectional invariant.",
        "post_invariants": ["bidirectional_edge"],
    },
    "add_trigger": {
        "args_schema": {
            "location_id": "str",
            "schedules": "list",
            "is_active": "bool?",
        },
        "destructiveness": "low_write",
        "docs": "Add a trigger to a location with weekly schedules.",
        "post_invariants": ["valid_schedule"],
    },
}

# -----------------------------
# TPS LOADER (Tiny Snapshot)
# -----------------------------


class SnapshotService:
    def __init__(self, project_id: str, ttl_seconds: int = 600):
        self.project_id = str(project_id)
        self.ttl = ttl_seconds
        self._cache: Optional[TinyProjectSnapshot] = None

        self.Project = get_model("Project")
        self.Location = get_model("Location")
        self.Canvas = get_model("Canvas")
        self.Character = get_model("Character")

        # Dynamic fields
        self._project_name = find_field_name(self.Project, ["name", "title"])
        self._canvas_project_fk = find_field_name(
            self.Canvas, ["project", "project_id"]
        )
        self._canvas_name = find_field_name(self.Canvas, ["name", "title"])
        self._canvas_location_fk = find_field_name(
            self.Canvas, ["location", "location_id"]
        )
        self._canvas_node_count = find_field_name(
            self.Canvas, ["node_count", "nodes", "node_total"]
        )
        self._canvas_has_trigger = find_field_name(
            self.Canvas, ["has_trigger", "triggered"]
        )

        self._location_name = find_field_name(self.Location, ["name", "title"])
        self._location_type = find_field_name(
            self.Location, ["type", "kind", "category"]
        )
        self._location_parent = find_field_name(
            self.Location, ["parent", "parent_id", "container", "container_id"]
        )
        self._location_project_fk = find_field_name(
            self.Location, ["project", "project_id"]
        )

        self._character_name = find_field_name(self.Character, ["name"])
        self._character_role = find_field_name(self.Character, ["role", "short_role"])
        self._character_project_fk = find_field_name(
            self.Character, ["project", "project_id"]
        )

    def _is_fresh(self) -> bool:
        return self._cache is not None and (time.time() - self._cache.ts) < self.ttl

    def get(self) -> TinyProjectSnapshot:
        if self._is_fresh():
            return self._cache
        # Project
        project = self.Project.objects.filter(pk=self.project_id).first()
        if not project:
            raise CommandError(f"Project not found: {self.project_id}")
        pname = (
            getattr(project, self._project_name, f"Project {self.project_id}")
            if self._project_name
            else f"Project {self.project_id}"
        )

        # Index locations
        lqs = self.Location.objects
        if self._location_project_fk:
            lqs = lqs.filter(**{self._location_project_fk: self.project_id})
        lqs = lqs.order_by(self._location_name or "id")[:100]
        loc_index = [
            {
                "id": str(x.pk),
                "name": getattr(x, self._location_name, None),
                "type": getattr(x, self._location_type, None),
                "parent_id": (
                    getattr(x, self._location_parent, None)
                    if self._location_parent
                    else None
                ),
            }
            for x in lqs
        ]

        # Characters
        cqs = self.Character.objects
        if self._character_project_fk:
            cqs = cqs.filter(**{self._character_project_fk: self.project_id})
        cqs = cqs.order_by(self._character_name or "id")[:15]
        chars = [
            {
                "id": str(x.pk),
                "name": getattr(x, self._character_name, None),
                "short_role": getattr(x, self._character_role, None),
            }
            for x in cqs
        ]

        # Hot canvases (cheap heuristic: the 10 most recently updated / created)
        canv_qs = self.Canvas.objects
        if self._canvas_project_fk:
            canv_qs = canv_qs.filter(**{self._canvas_project_fk: self.project_id})
        try:
            canv_qs = canv_qs.order_by("-updated_at")  # if you have it
        except Exception:
            canv_qs = canv_qs.order_by("-pk")
        canv_qs = canv_qs[:10]
        hot = [
            {
                "id": str(x.pk),
                "name": getattr(x, self._canvas_name, None),
                "node_count": getattr(x, self._canvas_node_count, None),
                "has_trigger": getattr(x, self._canvas_has_trigger, None),
            }
            for x in canv_qs
        ]

        counts = {
            "total_locations": self.Location.objects.count(),
            "total_characters": self.Character.objects.count(),
            "total_canvases": self.Canvas.objects.count(),
        }

        self._cache = TinyProjectSnapshot(
            project_id=self.project_id,
            project_name=pname,
            starting_canvas_id=None,
            locations_index=loc_index,
            main_characters=chars,
            hot_canvases=hot,
            counts=counts,
        )
        return self._cache


# -----------------------------
# SAFETY, VALIDATOR, SYNTHESIZER
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
            f"I’m not fully sure about the target(s) {step.targets}. Can you confirm or clarify before I proceed?",
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
    if step.tool == "create_canvas":
        # enforce "one-node-per-canvas": already checked in adapter by blocking duplicates.
        pass
    elif step.tool == "connect_locations":
        # You can add a real check against your edge table to ensure both directions exist.
        # For now, warn to implement.
        warnings.append(
            "Validator: Ensure bidirectional edges exist in DB (implement edge checks)."
        )
    elif step.tool == "add_trigger":
        # schedule validity (weekday 0–6, start < end)
        schedules = step.args.get("schedules") or []
        for s in schedules:
            wd = s.get("weekday")
            st = s.get("start")
            en = s.get("end")
            if wd is None or wd < 0 or wd > 6:
                warnings.append(f"Invalid weekday in schedule: {s}")
            if st is None or en is None or not (st < en):
                warnings.append(f"Invalid time window (start<end) in schedule: {s}")

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
# PROMPTS (SYSTEM & PLANNER)
# -----------------------------

SYSTEM_PROMPT = """You are Elora, a narrative-first assistant for open-world interactive stories.
Operate ONLY with the platform objects: Locations, Story Canvases, Triggers, Schedules, Characters/NPCs.
Never invent unsupported objects. All changes must go through tools; never write SQL/ORM directly.

Rules:
1) Read-then-act: resolve entities via Tiny Project Snapshot (TPS) or cheap list/get reads.
2) ReAct: Plan exactly one step, execute, reflect. For multi-step goals, produce a short To-Do (2–5 items).
3) Safety: For deletes/overwrites/high-impact writes, produce a dry-run preview and ask for confirmation.
4) Invariants: location connections are bidirectional; one-node-per-canvas; trigger schedules use weekday 0–6 and start<end.
5) Story-first: every write needs a short narrative intention (why it improves the story).
6) Clarity: restate the user goal in platform vocabulary; ask at most one clarifying question if required.
7) Tool discipline: match args_schema exactly. Never guess IDs—resolve by reads when needed.
"""

PLANNER_PLUS_PROMPT = """You are at planning step only (no execution).
1) Restate the user goal using TPS vocabulary.
2) Resolve entities via TPS; if ambiguous, propose exactly ONE lightweight read (list/get) to disambiguate.
3) Decide: StepPlan (single tool) OR ToDoPlan (2–5 items).
4) Prepare exact tool args per manifest. Include a short narrative intention for each write.
Output ONLY valid JSON in one of two shapes:
- {"step_plan": {...}}  OR
- {"todo_plan": {"title": "...", "rationale": "...", "items": [...], "overall_check": "...?"}}
"""

# -----------------------------
# SIMPLE LLM PLANNER (ReAct)
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
                "locations_index": tps.locations_index[:10],
                "main_characters": tps.main_characters[:10],
                "hot_canvases": tps.hot_canvases[:10],
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
            messages, model="gpt-5.1-mini", temperature=0.2, max_tokens=800
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
# EXECUTOR
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
# INTERACTIVE CLI
# -----------------------------

BANNER = r"""
   ______     __
  / ____/____/ /___  ____ _____ ___  _________  ____ _____  ___
 / __/ / ___/ / __ \/ __ `/ __ `__ \/ ___/ __ \/ __ `/ __ \/ _ \
/ /___/ /  / / /_/ / /_/ / / / / / (__  ) /_/ / /_/ / / / /  __/
\____/_/  /_/\____/\__,_/_/ /_/ /_/____/\____/\__,_/_/ /_/\___/

Elora ReAct CLI — narrative-first agent for open-world stories.
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
  quit                       Exit
"""


class Command(BaseCommand):
    help = "Run Elora ReAct agent in an interactive CLI for a given --project-id"

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
                            "counts": tps.counts,
                            "locations_index": tps.locations_index[:10],
                            "main_characters": tps.main_characters[:10],
                            "hot_canvases": tps.hot_canvases[:10],
                        },
                        indent=2,
                        ensure_ascii=False,
                    )
                )
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
# CLI HELPERS
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
