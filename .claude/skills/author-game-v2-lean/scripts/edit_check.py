"""Check an edit to a game against the game as it was before the edit.

    python3 .claude/skills/author-game-v2-lean/scripts/edit_check.py <slug> --start   # before editing
    python3 .claude/skills/author-game-v2-lean/scripts/edit_check.py <slug>           # after editing

`--start` merges the phase files, runs v2's scoreboard and saves the result. The plain run merges
again, re-runs the scoreboard and reports only what this edit made worse, plus two checks the
scoreboard does not make (schedule presence, explicit beats). It prints CLEAN and exits 0 when
nothing got worse; otherwise it prints each red and exits 1. It can be re-run after every fix.

The scoreboard is author-game-v2's gates.py, run unchanged. Nothing here re-implements a gate.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import tomllib as _toml            # py3.11+
except ModuleNotFoundError:            # py3.10, same fallback as gates.py
    import tomli as _toml

ROOT = Path(__file__).resolve().parents[4]
GATES_PY = ROOT / ".claude/skills/author-game-v2/scripts/gates.py"
MERGE_PY = ROOT / "scripts/merge_toml_phases.py"

# Lints that report a DEFECT. Every other gates.py lint is documented there as "a LIST and never
# a gate" (an inventory for a reader), so a new entry in one of those is not a regression.
DEFECT_LINTS = ("ambient_presence", "dialogue_attribution", "adjacent_groups", "past_claim")

SENTENCE = re.compile(r"(?<=[.!?])\s+")


# ── running v2's tools ───────────────────────────────────────────────────────

def game_dir(slug: str) -> Path:
    return ROOT / "games" / slug


def merged_toml(slug: str) -> Path:
    return game_dir(slug) / "toml_phases" / "7_final_game.toml"


def merge(slug: str) -> None:
    proc = subprocess.run([sys.executable, str(MERGE_PY), "--validate", str(game_dir(slug))],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        sys.exit(f"RED  the phase files do not merge or parse:\n{proc.stdout}{proc.stderr}")


def scoreboard(slug: str) -> dict:
    proc = subprocess.run([sys.executable, str(GATES_PY), str(merged_toml(slug)), "--json"],
                          capture_output=True, text=True, env={**os.environ, "PYTHONHASHSEED": "0"})
    if proc.returncode not in (0, 1):
        sys.exit(f"RED  gates.py could not score the game:\n{proc.stderr[-2000:]}")
    return json.loads(proc.stdout)


def load(path: Path) -> dict:
    with open(path, "rb") as fh:
        return _toml.load(fh)


def explicit_regex() -> re.Pattern:
    """The frozen EXPLICIT list, imported from gates.py so this check never drifts from it."""
    spec = importlib.util.spec_from_file_location("v2_gates", GATES_PY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.EXPLICIT


# ── what this edit made worse on the scoreboard ──────────────────────────────

def gate_regressions(after: dict, before: dict) -> list[str]:
    was = {g["gate"]: g for g in before["gates"]}
    out = []
    for g in after["gates"]:
        b = was.get(g["gate"])
        failing = not g["pass_"] and not g["na"] and not g.get("parked")
        if failing and (b is None or b["pass_"] or b["na"]):
            out.append(f"gate went red: {g['gate']} — {g['headline']}")
            out += [f"    {d}" for d in g.get("detail", [])[:4]]
    return out


def _findings(lint) -> set[str]:
    items = lint.get("findings", []) if isinstance(lint, dict) else (lint or [])
    return {json.dumps(i, sort_keys=True) for i in items}


def new_defects(after: dict, before: dict) -> list[str]:
    out = []
    for name in DEFECT_LINTS:
        for f in sorted(_findings(after["lints"].get(name)) - _findings(before["lints"].get(name))):
            out.append(f"new {name}: {f[:240]}")
    return out


# ── checks the scoreboard does not make ──────────────────────────────────────

def _minutes(hhmm: str) -> int:
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def _covers(row: dict, day: int, minute: int) -> bool:
    """The engine's own test (v2.py:4149-4150, 4517): weekday against TODAY first, then the time
    window, which wraps past midnight. An overnight row on specific days therefore ends at 00:00."""
    days = row.get("weekdays")
    if days not in (None, []) and day not in days:
        return False
    st = _minutes(row["start_time"])
    en = _minutes(row["end_time"]) if row.get("end_time") else st + 60
    return (minute >= st or minute < en) if en < st else (st <= minute < en)


def schedule_problems(game: dict, before: dict) -> list[str]:
    old_rows = {n["id"]: n.get("schedules", []) for n in before.get("npcs", [])}
    out = []
    for npc in game.get("npcs", []):
        rows = npc.get("schedules", [])
        if rows == old_rows.get(npc["id"]):
            continue
        for r in rows:
            days = r.get("weekdays")
            # An end of 00:00 means "until midnight" and is the correct first half of a split.
            if r.get("end_time") and 0 < _minutes(r["end_time"]) < _minutes(r["start_time"]) \
                    and days not in (None, []) and len(set(days)) < 7:
                out.append(f"{npc['id']}: row {r['location']} {r['start_time']}-{r['end_time']} on days {days} "
                           f"wraps midnight on specific days, so the engine drops them at 00:00. "
                           f"Split it: one row to 00:00, one from 00:00 on the next weekday.")
        clashes = set()
        for day in range(7):
            for minute in range(0, 24 * 60, 15):
                places = {r["location"] for r in rows if _covers(r, day, minute)}
                if len(places) > 1:
                    clashes.add((day, tuple(sorted(places))))
        for day, places in sorted(clashes)[:3]:
            out.append(f"{npc['id']}: on day {day} two rows put them in {' and '.join(places)} at the same time")
    return out


def _text_blocks(obj):
    if isinstance(obj, dict):
        if isinstance(obj.get("content"), str) and obj.get("type") in ("paragraph", "dialog", "thought_bubble"):
            yield obj
        for v in obj.values():
            yield from _text_blocks(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _text_blocks(v)


def explicit_beat_problems(game: dict, before: dict) -> list[str]:
    """register.md:204 and :360. A block that names the body is an explicit beat: it carries 3+
    frozen-list words and its last sentence stays on the body. A block naming none is fine."""
    rx = explicit_regex()
    old = {json.dumps(c, sort_keys=True) for c in before.get("canvases", [])}
    out = []
    for c in game.get("canvases", []):
        if json.dumps(c, sort_keys=True) in old:
            continue
        for b in _text_blocks(c):
            n = len(rx.findall(b["content"]))
            if n == 0:
                continue
            if n < 3:
                out.append(f"{c['id']}: explicit beat has {n} frozen-list word(s), floor is 3: \"{b['content'][:70]}\"")
            last = SENTENCE.split(b["content"].strip())[-1]
            if not rx.search(last):
                out.append(f"{c['id']}: explicit beat ends off the body: \"{last[:70]}\"")
    return out


# ── main ─────────────────────────────────────────────────────────────────────

def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1].startswith("-"):
        sys.exit(__doc__)
    slug, start = sys.argv[1], "--start" in sys.argv[2:]
    # The snapshot lives outside the repo so it never shows in git status. It is kept after a
    # CLEAN run, so the check can be re-run after a later fix; `--start` replaces it.
    key = hashlib.sha1(str(game_dir(slug).resolve()).encode()).hexdigest()[:12]
    snap = Path(tempfile.gettempdir()) / f"edit_check_{slug}_{key}.json"
    merge(slug)

    if start:
        snapshot = {"scoreboard": scoreboard(slug), "game": load(merged_toml(slug))}
        snap.write_text(json.dumps(snapshot))
        t = snapshot["scoreboard"]["tally"]
        print(f"START  {slug}: {t['pass']} pass, {t['fail']} fail, {t['na']} n/a. Make the edit, then run without --start.")
        return 0

    if not snap.exists():
        sys.exit(f"no snapshot: run `edit_check.py {slug} --start` before editing")
    before = json.loads(snap.read_text())
    after, game = scoreboard(slug), load(merged_toml(slug))

    reds = (gate_regressions(after, before["scoreboard"]) + new_defects(after, before["scoreboard"])
            + schedule_problems(game, before["game"]) + explicit_beat_problems(game, before["game"]))
    if reds:
        print(f"RED  {slug}: {len(reds)} problem(s) this edit introduced. Fix each at its cause, then re-run.")
        for r in reds:
            print(f"  - {r}" if not r.startswith("    ") else r)
        return 1
    t = after["tally"]
    print(f"CLEAN  {slug}: nothing got worse ({t['pass']} pass, {t['fail']} fail, {t['na']} n/a).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
