"""Compare a game's signed sheets with what is built.

    python3 .claude/skills/author-game-v2-lean/scripts/sheet_check.py <slug> --start   # before building
    python3 .claude/skills/author-game-v2-lean/scripts/sheet_check.py <slug>           # after building

author-game-v2 has no sheet-versus-build check ("A sheet-versus-build diff is not built",
the-sheets.md S1). This one reads the sheets in `games/<slug>/sheets/` and checks the facts a sheet
states in a fixed place:

- status: a sheet is buildable when its title says [READY] (or [GAME-READY]) and it carries a
  "Signed by LO" line;
- scenes/<canvas_id>.md: the canvas exists; it sits at the sheet's place; it can play at the sheet's
  day and hour; its trigger reads every `trait` the gate row names; it sets every `trait` the sets
  row names; it says the HOOK's quoted line;
- people/<id>.md: at the middle of every cell of the "where he/she is" grid, the person's schedule
  puts them in that place (or nowhere, for a "—" cell);
- places/<location_id>.md: the location exists. Every location without a place sheet is listed.

With a `--start` snapshot, only what changed since the snapshot is RED: a canvas, person or place
built or changed against its sheet, a piece built from an unsigned sheet, or a new location with no
sheet. Drift that was already there is listed as "already there", for LO, not blocking. Prints
CLEAN (exit 0) or RED (exit 1).
"""
from __future__ import annotations

import hashlib
import json
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
MERGE_PY = ROOT / "scripts/merge_toml_phases.py"
DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
TIME_RANGE = re.compile(r"(\d{1,2}):(\d{2})\s*[–-]\s*(\d{1,2}):(\d{2})")
BACKTICK = re.compile(r"`([a-z_][a-z0-9_]*)`")


# ── reading the game ─────────────────────────────────────────────────────────

def game_dir(slug: str) -> Path:
    return ROOT / "games" / slug


def load_game(slug: str) -> dict:
    proc = subprocess.run([sys.executable, str(MERGE_PY), "--validate", str(game_dir(slug))],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        sys.exit(f"RED  the phase files do not merge or parse:\n{proc.stdout}{proc.stderr}")
    with open(game_dir(slug) / "toml_phases" / "7_final_game.toml", "rb") as fh:
        return _toml.load(fh)


def walk(o):
    if isinstance(o, dict):
        yield o
        for v in o.values():
            yield from walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v)


def presence(rows: list[dict], day: int, minute: int):
    """The engine's order (v2.py:4149-4150, 4517): weekday against today, then the window, which
    wraps past midnight. The first matching row wins."""
    for r in rows:
        days = r.get("weekdays")
        if days not in (None, []) and day not in days:
            continue
        st = _min(r["start_time"])
        en = _min(r["end_time"]) if r.get("end_time") else st + 60
        if ((minute >= st or minute < en) if en < st else (st <= minute < en)):
            return r.get("location")
    return None


def _min(hhmm: str) -> int:
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


# ── reading the sheets ───────────────────────────────────────────────────────

def read_sheet(path: Path) -> dict:
    text = path.read_text()
    title = text.splitlines()[0] if text else ""
    rows = {}
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.strip().startswith("|") and len(cells) >= 2 and cells[0] and not set(cells[0]) <= set("-: "):
            rows.setdefault(cells[0].lower(), cells[1:])
    return {"path": path, "text": text, "rows": rows,
            "signed": ("[READY]" in title or "[GAME-READY]" in title) and "Signed by LO" in text}


def days_in(cell: str) -> list[int]:
    """'Tue–Sat' -> [1..5]; 'Thursday' -> [3]; 'Mon' -> [0]."""
    cell = cell.lower()
    m = re.search(r"\b(mon|tue|wed|thu|fri|sat|sun)[a-z]*\s*[–-]\s*(mon|tue|wed|thu|fri|sat|sun)", cell)
    if m:
        a, b = DAYS.index(m.group(1)), DAYS.index(m.group(2))
        return list(range(a, b + 1)) if a <= b else list(range(a, 7)) + list(range(0, b + 1))
    return [DAYS.index(d) for d in re.findall(r"\b(mon|tue|wed|thu|fri|sat|sun)", cell)]


def midpoint(cell: str):
    m = TIME_RANGE.search(cell)
    if not m:
        return None
    st, en = int(m.group(1)) * 60 + int(m.group(2)), int(m.group(3)) * 60 + int(m.group(4))
    if en <= st:
        en += 24 * 60
    return ((st + en) // 2) % (24 * 60)


def place_id(cell: str, locations: list[dict]):
    """The location a sheet cell names: its id, or its display name as a whole word (longest wins)."""
    low = cell.lower()
    hits = [l for l in locations if l["id"] in low.replace(" ", "_")
            or re.search(r"\b" + re.escape(l.get("name", "").lower()) + r"\b", low)]
    return max(hits, key=lambda l: len(l.get("name", "")))["id"] if hits else None


# ── the checks ───────────────────────────────────────────────────────────────

def check_scene(sheet: dict, canvas: dict | None, locations: list[dict]) -> list[str]:
    cid = sheet["path"].stem
    if canvas is None:
        return [f"scene {cid}: no canvas with this id"]
    out, rows, trig = [], sheet["rows"], canvas.get("trigger", {})
    where = " ".join(rows.get("where · when", []))
    want_place = place_id(where.split("·")[0], locations) if where else None
    if want_place and trig.get("location") != want_place:
        out.append(f"scene {cid}: built at {trig.get('location')}, the sheet says {want_place}")
    days, mid = days_in(where), midpoint(where)
    if days and mid is not None:
        rows_ = [dict(r, location="here") for r in (trig.get("schedules") or [])]
        if rows_ and presence(rows_, days[0], mid) != "here":
            out.append(f"scene {cid}: cannot play when the sheet says ({where.strip()})")
    reads = {i.get("trait_key") or i.get("flag_key") for i in walk(trig) if isinstance(i, dict)}
    for key in BACKTICK.findall(" ".join(rows.get("gate", []))):
        if key not in reads:
            out.append(f"scene {cid}: the sheet's gate names `{key}`, the trigger never reads it")
    sets = {d.get("trait") or d.get("flag") for d in walk(canvas) if isinstance(d, dict) and ("op" in d)}
    for key in BACKTICK.findall(" ".join(rows.get("sets", []))):
        if key not in sets:
            out.append(f"scene {cid}: the sheet's sets row names `{key}`, nothing in the canvas sets it")
    hook = re.findall(r"[\"“]([^\"”]{8,})[\"”]", " ".join(rows.get("hook", [])))
    text = " ".join(d["content"] for d in walk(canvas) if isinstance(d.get("content"), str)).lower()
    for line in hook:
        if line.lower().rstrip(".") not in text:
            out.append(f"scene {cid}: the HOOK line is not in the canvas: \"{line}\"")
    return out


def check_person(sheet: dict, npc: dict | None, locations: list[dict]) -> list[str]:
    pid = sheet["path"].stem
    if npc is None:
        return [f"person {pid}: no NPC with this id"]
    out, lines = [], sheet["text"].splitlines()
    head = next((i for i, l in enumerate(lines) if l.strip().lower().startswith("| place")), None)
    if head is None:
        return []
    cols = [c.strip() for c in lines[head].strip().strip("|").split("|")][1:]
    for line in lines[head + 2:]:
        if not line.strip().startswith("|"):
            break
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        place = place_id(cells[0], locations)
        for col, cell in zip(cols, cells[1:]):
            mid = midpoint(cell)
            for day in days_in(col):
                if mid is None:
                    continue
                got = presence(npc.get("schedules", []), day, mid)
                if got != place:
                    out.append(f"person {pid}: {DAYS[day].title()} {mid // 60:02d}:{mid % 60:02d} the grid says "
                               f"{place}, the schedule puts them at {got}")
    return out


def run_checks(slug: str, game: dict) -> dict:
    """{key: [problems]} where key is 'scene:<id>', 'person:<id>', 'place:<id>' or 'unsheeted:<id>'."""
    sheets_dir = game_dir(slug) / "sheets"
    locs, out = game.get("locations", []), {}
    canvases = {c["id"]: c for c in game.get("canvases", [])}
    npcs = {n["id"]: n for n in game.get("npcs", [])}
    status = {}
    for path in sorted(sheets_dir.glob("scenes/*.md")):
        s = read_sheet(path)
        status[f"scene:{path.stem}"] = s["signed"]
        out[f"scene:{path.stem}"] = check_scene(s, canvases.get(path.stem), locs)
    for path in sorted(sheets_dir.glob("people/*.md")):
        s = read_sheet(path)
        npc = npcs.get(path.stem) or npcs.get(f"npc_{path.stem}")
        status[f"person:{path.stem}"] = s["signed"]
        out[f"person:{path.stem}"] = check_person(s, npc, locs)
    placed = set()
    for path in sorted(sheets_dir.glob("places/*.md")):
        s = read_sheet(path)
        placed.add(path.stem)
        status[f"place:{path.stem}"] = s["signed"]
        out[f"place:{path.stem}"] = [] if any(l["id"] == path.stem for l in locs) else [f"place {path.stem}: no location with this id"]
    for l in locs:
        if l["id"] not in placed:
            out[f"unsheeted:{l['id']}"] = [f"location {l['id']} has no place sheet"]
    return {"problems": out, "signed": status, "pieces": _fingerprints(game)}


def _fingerprints(game: dict) -> dict:
    fp = {}
    for c in game.get("canvases", []):
        fp[f"scene:{c['id']}"] = hashlib.sha1(json.dumps(c, sort_keys=True).encode()).hexdigest()
    for n in game.get("npcs", []):
        h = hashlib.sha1(json.dumps(n.get("schedules", []), sort_keys=True).encode()).hexdigest()
        fp[f"person:{n['id']}"] = fp[f"person:{n['id'].removeprefix('npc_')}"] = h
    for l in game.get("locations", []):
        fp[f"place:{l['id']}"] = fp[f"unsheeted:{l['id']}"] = "exists"
    return fp


def snapshot_path(slug: str) -> Path:
    key = hashlib.sha1(str(game_dir(slug).resolve()).encode()).hexdigest()[:12]
    return Path(tempfile.gettempdir()) / f"sheet_check_{slug}_{key}.json"


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1].startswith("-"):
        sys.exit(__doc__)
    slug = sys.argv[1]
    result = run_checks(slug, load_game(slug))
    snap = snapshot_path(slug)
    if "--start" in sys.argv[2:]:
        snap.write_text(json.dumps(result))
        unsigned = sorted(k for k, ok in result["signed"].items() if not ok)
        print(f"START  {slug}: {len(result['signed'])} sheets, {len(unsigned)} not signed"
              + (f" ({', '.join(unsigned)})" if unsigned else "") + ".")
        return 0

    before = json.loads(snap.read_text()) if snap.exists() else None
    reds, old = [], []
    for key, probs in result["problems"].items():
        changed = before is None or before["pieces"].get(key) != result["pieces"].get(key)
        if probs and changed:
            reds += probs
        elif probs:
            old += probs
        if changed and before is not None and result["pieces"].get(key) and result["signed"].get(key) is False:
            reds.append(f"{key} was built or changed, but its sheet is not [READY] and signed by LO")
    if before is None:
        print("(no --start snapshot: every mismatch is shown as RED)")
    if reds:
        print(f"RED  {slug}: {len(reds)} mismatch(es) between the signed sheets and the build.")
        for r in reds:
            print(f"  - {r}")
    if old:
        print(f"already there before this change ({len(old)}; for LO, not blocking):")
        for r in old[:12]:
            print(f"  - {r}")
    if not reds:
        print(f"CLEAN  {slug}: what this change built matches its signed sheets.")
    return 1 if reds else 0


if __name__ == "__main__":
    raise SystemExit(main())
