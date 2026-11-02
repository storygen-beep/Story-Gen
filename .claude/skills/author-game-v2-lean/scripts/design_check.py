"""Check a game's design documents (premise, Want, idea page, spine) before LO reads them.

    python3 .claude/skills/author-game-v2-lean/scripts/design_check.py <slug>

Runs author-game-v2's own `shape.py <slug>` and reports its FAIL rows, then checks what shape.py
does not, each from a logged incident:

- every person in `want.cast` has an age of 18 or over, and the Want's cast section names no minor
  (the adults-only rule; shape.py checks the ledger ages in every mode);
- the goal has no date (the-want.md:50, D8): `want.promise.goals[]` and the Want's section 3;
- nothing is written ahead of the phase: IDEA.md needs phase `want` or later, a spine page needs
  `idea` or later, a sheet needs `board` or later (SKILL.md:169, stop at every phase boundary);
- a spine page that calls itself READY or signed has `signed_by` and `signed_at` in the ledger, and
  the phase is `spine` or later only when SP1-SP7 are all signed (shape.py strict rows, --finish).

Prints CLEAN (exit 0) or RED (exit 1).
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SHAPE_PY = ROOT / ".claude/skills/author-game-v2/scripts/shape.py"
ORDER = ["want", "idea", "spine", "board", "sheets", "release"]

DATED = re.compile(
    r"\b(by|before|within|in|after)\s+(the\s+end\s+of\s+)?(day|week|month|year|term|semester)\b"
    r"|\b(day|week)\s+(\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|sixty|ninety)\b"
    r"|\b\d+\s+(days|weeks|months)\b|\bdeadline\b"
    r"|\bend\s+of\s+(her|the)\s+(first|second|third|fourth|final)\s+(year|term|semester|month)\b", re.I)
# An actual signature; a blank template line ("signed by LO: —") is not one.
SIGNED = re.compile(r"\[READY\]|signed by LO:[ \t]*[A-Za-z]", re.I)
MINOR_AGE = re.compile(r"\b(1[0-7]|[1-9])[-\s]?(year[-\s]old|yo\b)|\baged?\s+(1[0-7]|[1-9])\b", re.I)


def section(md: str, number: int) -> str:
    m = re.search(rf"^##\s*{number}\.(.*?)(?=^##\s|\Z)", md, re.M | re.S)
    return m.group(0) if m else ""


def at_least(phase: str | None, wanted: str) -> bool:
    return phase in ORDER and ORDER.index(phase) >= ORDER.index(wanted)


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1].startswith("-"):
        sys.exit(__doc__)
    slug = sys.argv[1]
    gdir = ROOT / "games" / slug
    ledger_path = gdir / "v2_state.json"
    ledger = json.loads(ledger_path.read_text()) if ledger_path.exists() else {}
    want_md = (gdir / "WANT.md").read_text() if (gdir / "WANT.md").exists() else ""
    phase, reds = ledger.get("phase"), []

    if ledger:
        proc = subprocess.run([sys.executable, str(SHAPE_PY), slug], cwd=ROOT, capture_output=True, text=True)
        reds += [f"shape.py: {l.strip()}" for l in proc.stdout.splitlines() if "FAIL" in l]
        if proc.returncode not in (0, 1) and not proc.stdout.strip():
            reds.append(f"shape.py did not run: {proc.stderr.strip()[-200:]}")

    want = ledger.get("want") or {}
    if want_md or want:
        cast = want.get("cast") or []
        if not cast:
            reds.append("want.cast is empty: record every person with an age")
        for p in cast:
            age = p.get("age") if isinstance(p, dict) else None
            if not isinstance(age, (int, float)) or age < 18:
                reds.append(f"{(p or {}).get('id')}: age {age!r}; every person is an adult, 18 or over")
        for m in MINOR_AGE.finditer(section(want_md, 5)):
            reds.append(f"WANT.md section 5 gives someone a minor's age ({m.group(0)!r}); age them up or leave them out")
        goals = (want.get("promise") or {}).get("goals") or []
        texts = [f"{g.get('goal', '')} {g.get('ends_when', '')}" for g in goals if isinstance(g, dict)]
        texts.append(section(want_md, 3))
        hits = sorted({m.group(0) for t in texts for m in DATED.finditer(t)})
        if hits:
            reds.append(f"the goal carries a date ({', '.join(hits)}). D8: the goal has no date; "
                        "a deadline belongs to what holds her (section 2), never to what she wants")

    rules = [("IDEA.md", "want", (gdir / "IDEA.md").exists()),
             ("spine/", "idea", any((gdir / "spine").glob("SP*.md")) if (gdir / "spine").exists() else False),
             ("sheets/", "board", any((gdir / "sheets").rglob("*.md")) if (gdir / "sheets").exists() else False)]
    for name, needs, exists in rules:
        if exists and not at_least(phase, needs):
            reds.append(f"{name} exists but the phase is {phase!r}; it is written only from phase '{needs}', "
                        "after LO's pick at the boundary before it")

    signed = {p.get("id"): p for p in ((ledger.get("spine") or {}).get("pages") or []) if isinstance(p, dict)}
    for page in sorted((gdir / "spine").glob("SP*.md")) if (gdir / "spine").exists() else []:
        sp = page.name.split("_")[0]
        claims = SIGNED.search(page.read_text())
        rec = signed.get(sp) or {}
        if claims and not (rec.get("signed_by") and rec.get("signed_at")):
            reds.append(f"{page.name} says READY or signed, but the ledger has no signed_by/signed_at for {sp}; only LO signs")
    if at_least(phase, "spine"):
        unsigned = [sp for sp in (f"SP{i}" for i in range(1, 8)) if not (signed.get(sp) or {}).get("signed_by")]
        if unsigned:
            reds.append(f"phase is {phase!r} but {', '.join(unsigned)} are not signed; the phase moves only after LO signs all seven")

    if reds:
        print(f"RED  {slug}: {len(reds)} problem(s).")
        for r in reds:
            print(f"  - {r}")
        return 1
    print(f"CLEAN  {slug} (phase {phase}): the design documents pass every check.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
