#!/usr/bin/env python3
"""who_is_where.py — the presence table the truth gates read, printed for a reader.

Usage:
    python3 scripts/who_is_where.py <game-slug>            # every person, every day, by the hour
    python3 scripts/who_is_where.py <slug> --person npc_x  # one person

Each cell is where the person CAN be in that hour, by their schedule rows: first match wins and
the weekday is today's (v2.py:4289-4318); a row with `when` counts both ways ("hall|bedroom"); a
`when` that only waits for `<x>_met` counts as an ordinary row; "-" is nowhere. A trailing "z" marks
a row whose activity says asleep. Built from gates.py `_tr_where`, the same table the gates use, so a
reader (v2-reader tests 10-11) and the scoreboard never disagree about who is home. Read only.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gates  # noqa: E402

REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))


def cell(table, d, h):
    vals = set()
    for m in range(0, 60, gates._TR_STEP):
        for place, act in table.get((d, h * 60 + m), ()):
            vals.add((place or "-") + ("z" if gates._TR_SLEEP.search(act or "") else ""))
    return "|".join(sorted(vals)) or "-"


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    who = None
    if "--person" in args:
        i = args.index("--person")
        who = args[i + 1] if i + 1 < len(args) else None
        del args[i:i + 2]
    if not args:
        print(__doc__)
        return 2
    path = args[0] if args[0].endswith(".toml") else os.path.join(
        REPO, "games", args[0], "toml_phases", "7_final_game.toml")
    if not os.path.exists(path):
        print(f"not found: {path}")
        return 2
    where = gates._tr_where(gates._load(path))
    for pid, table in where.items():
        if who and pid != who:
            continue
        print(f"\n{pid}")
        for d, day in enumerate(gates._TR_DAYS):
            runs, last, start = [], None, 0
            for h in range(25):
                c = cell(table, d, h) if h < 24 else None
                if c != last:
                    if last is not None:
                        runs.append(f"{start:02d}-{h:02d} {last}")
                    last, start = c, h
            print(f"  {day}: " + " · ".join(runs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
