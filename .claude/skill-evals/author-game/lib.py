"""Shared helpers for the author-game exam: load a game, walk it, and grade it.

The exam grades on the DIFF from the fixture's own baseline, never on gates.py's exit
code: the fixture already fails `location fill`, so the exit code is 1 before any task.
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import subprocess
import tomllib
from functools import lru_cache
from pathlib import Path

EVAL_DIR = Path(__file__).resolve().parent
REPO = EVAL_DIR.parents[2]
GATES_PY = REPO / ".claude/skills/author-game-v2/scripts/gates.py"
MERGE_PY = REPO / "scripts/merge_toml_phases.py"
FIXTURE = json.loads((EVAL_DIR / "fixture.json").read_text())
GAME_REL = Path("games") / FIXTURE["game"]

# gates.py and the merge script are run with the same interpreter the skill documents.
SYSTEM_PYTHON = "python3"


# ── loading ──────────────────────────────────────────────────────────────────

def load_game(toml_path: Path) -> dict:
    with open(toml_path, "rb") as fh:
        return tomllib.load(fh)


def final_toml(game_dir: Path) -> Path:
    return game_dir / "toml_phases" / "7_final_game.toml"


def merge(game_dir: Path, merge_py: Path = MERGE_PY) -> subprocess.CompletedProcess:
    return subprocess.run(
        [SYSTEM_PYTHON, str(merge_py), "--validate", str(game_dir)],
        capture_output=True, text=True,
    )


def run_gates(toml_path: Path, gates_py: Path = GATES_PY) -> dict:
    proc = subprocess.run(
        [SYSTEM_PYTHON, str(gates_py), str(toml_path), "--json"],
        capture_output=True, text=True, env={**os.environ, "PYTHONHASHSEED": "0"},
    )
    if proc.returncode not in (0, 1):
        raise RuntimeError(f"gates.py exit {proc.returncode}: {proc.stderr[-2000:]}")
    return json.loads(proc.stdout)


@lru_cache(maxsize=1)
def explicit_regex() -> re.Pattern:
    """The frozen EXPLICIT list, imported from gates.py so the exam never drifts from it."""
    spec = importlib.util.spec_from_file_location("v2_gates", GATES_PY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.EXPLICIT


# ── walking ──────────────────────────────────────────────────────────────────

def iter_dicts(obj):
    if isinstance(obj, dict):
        yield obj
        for v in obj.values():
            yield from iter_dicts(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from iter_dicts(v)


def canvases(game: dict) -> dict[str, dict]:
    return {c["id"]: c for c in game.get("canvases", [])}


def new_canvases(game: dict, base: dict) -> list[dict]:
    old = canvases(base)
    return [c for cid, c in canvases(game).items() if cid not in old]


def changed_canvases(game: dict, base: dict) -> list[dict]:
    """New canvases plus canvases whose content differs from the baseline."""
    old = canvases(base)
    out = []
    for cid, c in canvases(game).items():
        if cid not in old or json.dumps(c, sort_keys=True) != json.dumps(old[cid], sort_keys=True):
            out.append(c)
    return out


def choices(obj) -> list[dict]:
    return [d for d in iter_dicts(obj) if "text" in d and "targetType" in d]


def condition_sets(obj) -> list[dict]:
    """Every dict that holds condition items (trigger, group, choice, schedule `when`, ...)."""
    return [d for d in iter_dicts(obj) if isinstance(d.get("items"), list) and "logic" in d]


def condition_items(obj) -> list[dict]:
    return [i for cs in condition_sets(obj) for i in cs["items"] if isinstance(i, dict)]


def text_blocks(obj) -> list[dict]:
    return [d for d in iter_dicts(obj) if isinstance(d.get("content"), str) and d.get("type")]


def canvas_text(canvas: dict) -> str:
    return "\n".join(b["content"] for b in text_blocks(canvas))


def effects(obj) -> list[dict]:
    return [e for d in iter_dicts(obj) for e in d.get("effects", []) if isinstance(e, dict)]


def npc(game: dict, npc_id: str) -> dict | None:
    return next((n for n in game.get("npcs", []) if n["id"] == npc_id), None)


def to_minutes(hhmm: str) -> int:
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


# ── grading against the baseline ────────────────────────────────────────────

def _finding_keys(lint) -> set[str]:
    if isinstance(lint, dict):
        items = lint.get("findings", [])
    elif isinstance(lint, list):
        items = lint
    else:
        items = []
    return {json.dumps(i, sort_keys=True) for i in items}


def gate_regressions(after: dict, base: dict) -> list[str]:
    """Gates that passed (or were n/a) at baseline and now fail."""
    before = {g["gate"]: g for g in base["gates"]}
    out = []
    for g in after["gates"]:
        b = before.get(g["gate"])
        failing_now = not g["pass_"] and not g["na"] and not g.get("parked")
        was_ok = b is None or b["pass_"] or b["na"]
        if failing_now and was_ok:
            out.append(f"gate regressed: {g['gate']} — {g['headline']}")
    return out


def new_lint_findings(after: dict, base: dict, lint_names: list[str]) -> list[str]:
    out = []
    for name in lint_names:
        if name not in after["lints"]:
            out.append(f"lint missing from gates output: {name}")
            continue
        added = _finding_keys(after["lints"][name]) - _finding_keys(base["lints"].get(name))
        for f in sorted(added)[:5]:
            out.append(f"new {name} finding: {f[:300]}")
    return out
