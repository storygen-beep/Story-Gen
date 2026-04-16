"""
Condition schema validation and evaluation for CanvasTrigger.conditions (v1.0).

Implements a strict, simple schema supporting global flags and character traits
for Player or specific NPCs. Provides validation and runtime evaluation helpers.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time
from typing import Any, Dict, List, Optional, Tuple

from django.core.exceptions import ValidationError
from django.db.models import Q

from apps.characters.models import Character
from apps.npcs.models import NPC
from apps.projects.models import Project
from apps.stories.models import CanvasTrigger, StoryCanvas


SUPPORTED_VERSION = "1.0"


@dataclass
class ConditionDetail:
    index: int
    type: str
    satisfied: bool
    reason: str = ""


def _ensure_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        v = value.strip().lower()
        if v in {"true", "1", "yes"}:
            return True
        if v in {"false", "0", "no"}:
            return False
    raise ValidationError("Expected boolean value")


def _coerce_flag_value(value: Any) -> Any:
    return value


def _compare(operator: str, left: Any, right: Any) -> bool:
    if operator == "eq":
        return left == right
    if operator == "ne":
        return left != right
    if operator == "gt":
        return left > right
    if operator == "gte":
        return left >= right
    if operator == "lt":
        return left < right
    if operator == "lte":
        return left <= right
    if operator == "in":
        if not isinstance(right, (list, tuple, set)):
            raise ValidationError("'in' operator requires array value")
        return left in right
    if operator == "not_in":
        if not isinstance(right, (list, tuple, set)):
            raise ValidationError("'not_in' operator requires array value")
        return left not in right
    if operator == "contains":
        if isinstance(left, (list, tuple, set, str)):
            return right in left
        raise ValidationError("'contains' requires string or array left operand")
    if operator == "not_contains":
        if isinstance(left, (list, tuple, set, str)):
            return right not in left
        raise ValidationError("'not_contains' requires string or array left operand")
    if operator == "exists":
        return left is not None
    if operator == "not_exists":
        return left is None
    raise ValidationError(f"Unsupported operator: {operator}")


def validate_conditions_schema(
    conditions: Dict[str, Any],
    project: Project,
) -> Dict[str, Any]:
    """Validate and normalize the v1.0 trigger conditions schema.

    Raises ValidationError on problems. Returns a cleaned copy on success.
    """
    if not isinstance(conditions, dict):
        raise ValidationError("conditions must be an object")

    cleaned: Dict[str, Any] = {}
    version = conditions.get("version")
    if version != SUPPORTED_VERSION:
        raise ValidationError("conditions.version must be '1.0'")
    cleaned["version"] = SUPPORTED_VERSION

    logic = conditions.get("logic", "AND")
    if logic not in ("AND", "OR"):
        raise ValidationError("conditions.logic must be 'AND' or 'OR'")
    cleaned["logic"] = logic

    items = conditions.get("items")
    if not isinstance(items, list) or len(items) == 0:
        raise ValidationError("conditions.items must be a non-empty array")
    if len(items) > 25:
        raise ValidationError("conditions.items exceeds maximum of 25")

    cleaned_items: List[Dict[str, Any]] = []
    for idx, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValidationError(f"conditions.items[{idx}] must be an object")
        itype = item.get("type")
        if itype not in ("flag", "trait"):
            raise ValidationError(f"conditions.items[{idx}].type must be 'flag' or 'trait'")

        if itype == "flag":
            # Per-entity flag condition (aligned with traits)
            subject = item.get("subject")
            if subject not in ("player", "npc"):
                raise ValidationError(f"items[{idx}].subject must be 'player' or 'npc'")
            character_id = item.get("character_id") if subject == "npc" else None
            if subject == "npc":
                if not character_id:
                    raise ValidationError(f"items[{idx}].character_id is required for NPC flag condition")
                # Ensure NPC exists in project
                if not NPC.objects.filter(id=character_id, project=project).exists():
                    raise ValidationError(f"items[{idx}].character_id not found in project")
            flag_key = item.get("flag_key")
            if not flag_key or not isinstance(flag_key, str):
                raise ValidationError(f"items[{idx}].flag_key is required")

            operator = item.get("operator")
            if operator not in ("exists", "is_true", "is_false"):
                raise ValidationError(f"items[{idx}].operator invalid for flag condition")

            cleaned_item = {
                "type": "flag",
                "subject": subject,
                "flag_key": flag_key,
                "operator": operator,
            }
            if subject == "npc":
                cleaned_item["character_id"] = str(character_id)
            cleaned_items.append(cleaned_item)

        elif itype == "trait":
            subject = item.get("subject")
            if subject not in ("player", "npc"):
                raise ValidationError(f"items[{idx}].subject must be 'player' or 'npc'")
            character_id = item.get("character_id") if subject == "npc" else None
            if subject == "npc":
                if not character_id:
                    raise ValidationError(f"items[{idx}].character_id is required for NPC trait condition")
                try:
                    npc = NPC.objects.get(id=character_id, project=project)
                except NPC.DoesNotExist:
                    raise ValidationError(f"items[{idx}].character_id not found in project")

            trait_key = item.get("trait_key")
            if not trait_key or not isinstance(trait_key, str):
                raise ValidationError(f"items[{idx}].trait_key is required")

            operator = item.get("operator")
            if operator not in (
                "eq",
                "ne",
                "gt",
                "gte",
                "lt",
                "lte",
                "contains",
                "not_contains",
                "exists",
                "not_exists",
            ):
                raise ValidationError(f"items[{idx}].operator invalid for trait condition")

            value = item.get("value", None)
            if operator in ("exists", "not_exists"):
                value = None

            cleaned_item = {
                "type": "trait",
                "subject": subject,
                "trait_key": trait_key,
                "operator": operator,
            }
            if subject == "npc":
                cleaned_item["character_id"] = str(character_id)
            if value is not None:
                cleaned_item["value"] = value
            cleaned_items.append(cleaned_item)

    cleaned["items"] = cleaned_items
    return cleaned


def evaluate_conditions(
    project: Project,
    conditions: Dict[str, Any],
    now: Optional[datetime] = None,
) -> Tuple[bool, List[ConditionDetail]]:
    """Evaluate validated conditions against current project state.

    Assumes schema has been validated via validate_conditions_schema.
    """
    details: List[ConditionDetail] = []
    items = conditions.get("items", [])
    logic = conditions.get("logic", "AND")

    # Resolve player character once
    try:
        player = Character.objects.get(project=project)
        player_traits = player.core_traits or {}
    except Character.DoesNotExist:
        player_traits = {}

    for idx, item in enumerate(items):
        itype = item["type"]
        try:
            if itype == "flag":
                subject = item["subject"]
                operator = item["operator"]
                flag_key = item["flag_key"]
                if subject == "player":
                    # Only existence can be reliably checked without runtime state; is_true/is_false default to False
                    player = Character.objects.filter(project=project).first()
                    keys = (player.flag_keys if player else []) or []
                    exists = flag_key in keys
                    if operator == "exists":
                        satisfied = exists
                    elif operator == "is_true":
                        satisfied = False
                    else:  # is_false
                        satisfied = False
                else:
                    npc_id = item["character_id"]
                    npc = NPC.objects.filter(id=npc_id, project=project).first()
                    keys = (npc.flag_keys if npc else []) or []
                    exists = flag_key in keys
                    if operator == "exists":
                        satisfied = exists
                    elif operator == "is_true":
                        satisfied = False
                    else:
                        satisfied = False
                details.append(ConditionDetail(idx, itype, satisfied))
            else:  # trait
                subject = item["subject"]
                operator = item["operator"]
                trait_key = item["trait_key"]
                if subject == "player":
                    left = player_traits.get(trait_key)
                else:
                    npc_id = item["character_id"]
                    try:
                        npc = NPC.objects.get(id=npc_id, project=project)
                        left = (npc.core_traits or {}).get(trait_key)
                    except NPC.DoesNotExist:
                        left = None
                value = item.get("value")
                satisfied = _compare(operator, left, value)
                details.append(ConditionDetail(idx, itype, satisfied))
        except ValidationError as e:
            details.append(ConditionDetail(idx, itype, False, reason=str(e)))

    if not details:
        return False, []

    if logic == "AND":
        overall = all(d.satisfied for d in details)
    else:
        overall = any(d.satisfied for d in details)

    return overall, details


def schedule_active_now(trigger: CanvasTrigger, now: Optional[datetime] = None) -> bool:
    """Return True if any schedule for trigger is active at 'now'. If no schedules, treat as always active."""
    if now is None:
        now = datetime.now()
    current_weekday = now.weekday()
    current_time = now.time()

    schedules = trigger.schedules.all()
    if not schedules.exists():
        return True

    for s in schedules:
        if current_weekday in (s.weekdays or []):
            if s.start_time and s.start_time <= current_time:
                if s.end_time is None or s.end_time >= current_time:
                    return True
    return False


def next_schedule_start(trigger: CanvasTrigger, after: Optional[datetime] = None, days_ahead: int = 14) -> Optional[datetime]:
    """Compute the next schedule start time after 'after'. Returns None if none found in window."""
    if after is None:
        after = datetime.now()
    from datetime import timedelta

    schedules = list(trigger.schedules.all())
    if not schedules:
        return None

    candidates: List[datetime] = []
    for days in range(days_ahead + 1):
        check_date = after.date() + timedelta(days=days)
        weekday = check_date.weekday()
        for s in schedules:
            if weekday in (s.weekdays or []):
                start_dt = datetime.combine(check_date, s.start_time)
                if start_dt > after:
                    candidates.append(start_dt)
    return min(candidates) if candidates else None
