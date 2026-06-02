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
