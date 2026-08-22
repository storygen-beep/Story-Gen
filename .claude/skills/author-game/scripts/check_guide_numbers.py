#!/usr/bin/env python3
"""Guide-number guard — every threshold the paid guide asserts must be a REAL gate.

    python .claude/skills/author-game/scripts/check_guide_numbers.py \
        games/<slug>/toml_phases/7_final_game.toml \
        games/<slug>/guide/guide.md

Why this exists
---------------
The guide is the paid product (`references/player-guide.md`). Prose in it can be a
little loose; a NUMBER cannot. A wrong threshold is the one defect that gets
discovered by a paying customer, in the worst way: they follow the book, the gate
does not open, and they conclude the game is broken.

Nothing else catches it. The build is green either way — the guide is a separate
document the compiler never sees, and it is untracked, so no diff review covers it.

What it does
------------
1. Harvests every `trait/trait_key + operator + value` condition in the merged TOML
   (conditions, goals, quest `when`, choice gates -- anywhere they appear).
2. Scans the guide markdown for claims of the form "<word> <number>", restricted to
   words that are actually trait keys in this game, plus bolded bare numbers next to
   a known trait name.
3. Reports any claimed threshold that has no matching gate.

Honest limits
-------------
- It checks that a number EXISTS as a gate on that trait, not that the guide put it
  on the right rung. A guide that swaps two real thresholds passes. Read the routes
  chapter as well.
- It only sees numbers written next to a trait name. A number in bare prose ("about
  four heads") is invisible to it, by design -- those are estimates, not thresholds.
- Schedule times are NOT covered here; check those against `[[npcs.schedules]]`
  separately (`player-guide.md` §7 has the checklist line).

Exit codes: 0 all claims verified · 1 unverified claims found · 2 bad usage.
"""
import re
import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # py<3.11
    import tomli as tomllib


def harvest_gates(node, out):
    """Every (trait, operator, value) triple the build gates on."""
    if isinstance(node, dict):
        key = node.get("trait_key") or node.get("trait")
        op = node.get("operator") or node.get("op")
        val = node.get("value")
        # bool is an int subclass -- an `is_true` flag is not a threshold.
        if key and op and isinstance(val, (int, float)) and not isinstance(val, bool):
            out.add((str(key), str(op), float(val)))
        for child in node.values():
            harvest_gates(child, out)
    elif isinstance(node, list):
        for child in node:
            harvest_gates(child, out)


def cheat_numbers(data):
    """Caps and values from [[ui.cheat_page.grants]].

    A cheat cap is a REAL number an author will legitimately quote ("the Stealth
    code caps at 9") that is deliberately NOT a gate -- it usually sits one below
    the first `lt` window on purpose. Without this the checker reports it every
    run, and a checker that cries wolf gets ignored.
    """
    out = {}
    page = (data.get("ui") or {}).get("cheat_page") or {}
    for grant in page.get("grants") or []:
        trait = grant.get("trait")
        if not trait:
            continue
        for field in ("cap", "value"):
            v = grant.get(field)
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                out.setdefault(str(trait), set()).add(float(v))
    return out


def trait_keys(data):
    """Every trait name this game could legitimately be gated on."""
    keys = set((data.get("player") or {}).get("core_traits") or {})
    for npc in data.get("npcs") or []:
        keys |= set(npc.get("core_traits") or {})
    return keys


def claims_in(text, keys):
    """(trait, value, line-number) for every threshold the guide asserts.

    Matches `stealth 30`, `relation **21**`, `corruption 10 / 20 / 30` and the
    `**Colm's numbers:** relation 12 / 24` summary shape. Markdown emphasis and
    backticks are stripped first so `**18**` reads as 18.
    """
    found = []
    for lineno, raw in enumerate(text.splitlines(), 1):
        line = re.sub(r"[*`_]", "", raw)
        for key in keys:
            for m in re.finditer(rf"\b{re.escape(key)}\b(?!\s*(?:code|key))", line, re.I):
                tail = line[m.end():m.end() + 90]
                # a run of numbers after the trait name: "10 / 20 / 30", "under 25"
                run = re.match(r"[^0-9\n]{0,24}((?:\d+(?:\s*[/·,]\s*|\s+(?:or|and|under|to)\s+)?)+)", tail)
                if not run:
                    continue
                # Look a few chars PAST the captured run: "0-100" captures only
                # "0", because the dash is not a separator, so the range would be
                # invisible if we only inspected the capture.
                span = tail[: run.end() + 6]
                # A RANGE is a description, not a threshold: "0-100", "0 and up",
                # "25-49". Ranges live in the meters/bands tables and every game
                # has them, so matching them is pure noise.
                if re.search(r"\d\s*[-\u2013\u2014]\s*\d", span) or "and up" in tail.lower():
                    continue
                for num in re.findall(r"\d+", run.group(1)):
                    found.append((key, float(num), lineno))
    return found


def main(argv):
    if len(argv) != 3:
        print(__doc__)
        return 2
    toml_path, guide_path = Path(argv[1]), Path(argv[2])
    for p in (toml_path, guide_path):
        if not p.exists():
            print(f"not found: {p}")
            return 2

    with open(toml_path, "rb") as fh:
        data = tomllib.load(fh)

    gates = set()
    harvest_gates(data, gates)
    keys = trait_keys(data)
    by_trait = {}
    for trait, _op, val in gates:
        by_trait.setdefault(trait, set()).add(val)

    caps = cheat_numbers(data)
    claims = claims_in(guide_path.read_text(encoding="utf-8"), keys)
    # Dedupe on (trait, value) -- the same threshold is legitimately repeated.
    seen, unverified, cheat_ok = set(), [], []
    for trait, val, lineno in claims:
        if (trait, val) in seen:
            continue
        seen.add((trait, val))
        if val in by_trait.get(trait, set()):
            continue
        if val in caps.get(trait, set()):
            cheat_ok.append((trait, val))
            continue
        unverified.append((trait, val, lineno))

    print(f"{toml_path.parent.parent.name}: {len(gates)} gates on {len(by_trait)} traits")
    print(f"{guide_path.name}: {len(seen)} distinct threshold claims")
    if cheat_ok:
        pretty = ", ".join(f"{t} {v:g}" for t, v in sorted(cheat_ok))
        print(f"  ({len(cheat_ok)} matched a cheat-page cap rather than a gate: {pretty})")

    if unverified:
        print(f"\n{len(unverified)} UNVERIFIED — no such gate in the build:")
        for trait, val, lineno in sorted(unverified, key=lambda x: x[2]):
            known = sorted(by_trait.get(trait, set()))
            near = ", ".join(f"{v:g}" for v in known[:8]) or "none"
            print(f"  {guide_path.name}:{lineno}  '{trait} {val:g}'   real gates: {near}")
        print("\nFix the guide, or the number is a gate that no longer exists.")
        return 1

    print("\nALL VERIFIED — every threshold in the guide is a real gate.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
