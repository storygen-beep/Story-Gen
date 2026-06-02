"""authoring_state.json operations for the /author-game skill. Stdlib only."""
import json
from pathlib import Path

LEDGER_NAME = "authoring_state.json"
SCHEMA_VERSION = 1


def ledger_path(game_dir) -> Path:
    return Path(game_dir) / LEDGER_NAME


def init_ledger(game_slug: str) -> dict:
    return {
        "game_slug": game_slug,
        "schema_version": SCHEMA_VERSION,
        "book_revision": 1,
        "plan": [],
        "structure_registry": {
            "locations": [], "npcs": [], "flags": [], "schedules": []
        },
        "next_up": [],
        "decisions_log": [],
    }


def load_ledger(game_dir) -> dict:
    return json.loads(ledger_path(game_dir).read_text())


def save_ledger(game_dir, led: dict) -> None:
    ledger_path(game_dir).write_text(json.dumps(led, indent=2) + "\n")


def add_structure(led: dict, kind: str, name: str) -> dict:
    reg = led["structure_registry"]
    if kind not in reg:
        raise KeyError(f"unknown structure kind: {kind!r}")
    if name in reg[kind]:
        raise ValueError(f"{kind} {name!r} already registered")
    reg[kind].append(name)
    return led


BEAT_TYPES = {
    "npc_intro", "location_reveal", "arc_escalation",
    "cross_npc", "economic", "story_turn", "capstone",
}
BEAT_STATUSES = {"planned", "active", "authored", "validated"}


def _next_beat_id(led: dict) -> str:
    return f"beat_{len(led['plan']) + 1:04d}"


def add_beat(led, *, type, title, desc, target_phase,
             deps=None, introduces=None) -> dict:
    if type not in BEAT_TYPES:
        raise ValueError(f"invalid beat type: {type!r}")
    beat = {
        "id": _next_beat_id(led),
        "type": type,
        "title": title,
        "desc": desc,
        "status": "planned",
        "deps": list(deps or []),
        "target_phase": target_phase,
        "introduces": introduces or {"locations": [], "npcs": [], "flags": []},
        "produced_canvas_ids": [],
        "decided_at": None,
    }
    led["plan"].append(beat)
    led["next_up"].append(beat["id"])
    return beat


def get_beat(led: dict, beat_id: str) -> dict:
    for beat in led["plan"]:
        if beat["id"] == beat_id:
            return beat
    raise KeyError(f"no beat {beat_id!r}")


def mark_beat(led: dict, beat_id: str, status: str) -> dict:
    if status not in BEAT_STATUSES:
        raise ValueError(f"invalid status: {status!r}")
    beat = get_beat(led, beat_id)
    beat["status"] = status
    if status in ("authored", "validated") and beat_id in led["next_up"]:
        led["next_up"].remove(beat_id)
    return beat
