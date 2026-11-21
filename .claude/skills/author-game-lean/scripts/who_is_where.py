"""Who is where: each person, each weekday, by the hour, from their schedule rows. Read-only.

    venv/bin/python .claude/skills/author-game-lean/scripts/who_is_where.py games/<slug> [--person <npc_id>]

author-game-lean copy (LO, 2026-11-20). Copied from author-game-v2/scripts/who_is_where.py (frozen at ea8f6465),
with the only parts of v2's gates.py it needs inlined (`_TR_*`, `_tr_min`, `_tr_in_window`, `_tr_days`,
`_tr_rows_slots`, `_tr_met_only`, `_tr_where`, gates.py:13786-13870), so nothing here imports v2. Two changes:
it takes the game folder (like every lean script) instead of a slug, and the engine cites below are re-read
on 2026-11-20 (v2's said v2.py:4289-4318, which has drifted).

How the engine decides (`setup.getNpcLocation`, v2.py:4398-4425): walk the person's rows in order; skip a row
whose weekdays miss today, whose window misses now (`setup.isCurrentTimeSlot`, v2.py:4770-4790: end exclusive,
no end = start + 60 minutes, a window ending before it starts wraps past midnight), or whose `when` fails
(`setup._scheduleRowLive`, v2.py:4387). The first row left wins; none left means nowhere.

Here a row with a `when` may be live or not, so it adds its place AND lets the walk go on; a `when` that only
waits for `<x>_met` counts as an ordinary row. Each cell is every place the person CAN be in that hour,
joined by "|"; "-" is nowhere; a trailing "z" marks an activity that says asleep.
"""
import re
import sys
import tomllib
from pathlib import Path

DAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
STEP = 5
SLOTS = tuple((d, m) for d in range(7) for m in range(0, 1440, STEP))
SLEEP = re.compile(r"\b(?:asleep|sleep(?:s|ing)?|in bed|snor\w*)\b", re.I)


def minutes(s):
    try:
        h, m = str(s).split(":")[:2]
        return int(h) * 60 + int(m)
    except (ValueError, AttributeError):
        return None


def in_window(m, start, end):
    """`setup.isCurrentTimeSlot` (v2.py:4770-4790)."""
    s, e = minutes(start), minutes(end) if end else None
    if s is None:
        return False
    e = s + 60 if e is None else e
    return (m >= s or m < e) if e < s else (s <= m < e)


def weekdays(v):
    return set(v) if isinstance(v, (list, tuple)) and v else set(range(7))


def row_slots(row):
    days = weekdays(row.get("weekdays"))
    return {(d, m) for d, m in SLOTS if d in days and in_window(m, row.get("start_time"), row.get("end_time"))}


def met_only(when):
    """A `when` that only waits for `<x>_met is_true` is read as an ordinary row."""
    items = when.get("items") if isinstance(when, dict) else when
    return bool(items) and all(isinstance(i, dict) and str(i.get("flag_key", "")).endswith("_met")
                               and i.get("operator") == "is_true" for i in items)


def where(game):
    """{npc_id: {(day, minute): frozenset((place or None, activity))}}."""
    out = {}
    for n in game.get("npcs") or []:
        rows = [r for r in n.get("schedules") or [] if isinstance(r, dict)]
        if not rows or not n.get("id"):
            continue
        cover = [(row_slots(r), (r.get("location"), r.get("activity") or ""),
                  bool(r.get("when")) and not met_only(r["when"])) for r in rows]
        table = {}
        for slot in SLOTS:
            can = set()
            for slots, val, gated in cover:
                if slot in slots:
                    can.add(val)
                    if not gated:
                        break
            else:
                can.add((None, ""))
            table[slot] = frozenset(can)
        out[n["id"]] = table
    return out


def cell(table, d, h):
    vals = set()
    for m in range(0, 60, STEP):
        for place, act in table.get((d, h * 60 + m), ()):
            vals.add((place or "-") + ("z" if SLEEP.search(act or "") else ""))
    return "|".join(sorted(vals)) or "-"


def lines(game, person=None):
    out = []
    for pid, table in where(game).items():
        if person and pid != person:
            continue
        out.append(pid)
        for d, day in enumerate(DAYS):
            runs, last, start = [], None, 0
            for h in range(25):
                c = cell(table, d, h) if h < 24 else None
                if c != last:
                    if last is not None:
                        runs.append(f"{start:02d}-{h:02d} {last}")
                    last, start = c, h
            out.append(f"  {day}: " + " · ".join(runs))
    return out


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    person = None
    if "--person" in args:
        i = args.index("--person")
        person = args[i + 1] if i + 1 < len(args) else None
        del args[i:i + 2]
    if not args:
        print(__doc__)
        return 2
    path = Path(args[0])
    if path.is_dir():
        path = path / "toml_phases" / "7_final_game.toml"
    if not path.is_file():
        print(f"not found: {path}")
        return 2
    print("\n".join(lines(tomllib.loads(path.read_text(encoding="utf-8")), person)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
