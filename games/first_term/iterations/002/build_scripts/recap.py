"""recap.py: a repeatable act pays across its stage's line (LO's playtest, 2026-11-09).

Every part script caps a repeatable raise of Corruption or Exhibitionism at its own stage's top
(19, 39, 59, 79), so at those numbers nothing repeatable paid and the player stood one point under
every line. The skill's rule now (the-arc.md A4d) is that the cap sits at the top of the stage
ABOVE the one the act opens in. This pass moves each such cap up one stage, in the scenes file the
build has just concatenated, so the part scripts keep their own reading ("this act belongs to
Curious") and the build ships the new rule. The daily caps per band ([engine.daily_caps]) set the
pace. The gates judge the result: `an act pays no further than the next stage`, `every stage has
a way up` and `a pay can happen`.

Only canvases the engine repeats are touched (an absent `is_repeatable` means repeatable, as the
engine and gates.py read it). One-time steps keep their caps. The file is regenerated on every
build, so the pass runs once per build and never twice on the same text.

Usage: python3 recap.py <scenes.toml>
"""
import re
import sys

try:
    import tomllib
except ModuleNotFoundError:          # the venv's python 3.10
    import tomli as tomllib

METERS = ("corruption", "exhibitionism")
STAGE_TOPS = {19: 39, 39: 59, 59: 79}   # 79 stays: nothing is gated above 80 this release (gate `meter ceiling`)

# One player raise of a climb meter with a stage-top cap, in the inline-table form tomlw.py writes.
RAISE = re.compile(
    r'(\{ targetType = "player", trait = "(?:%s)", op = "add", value = \d+(?:, clamp = (?:true|false))?, cap = )(\d+)( \})'
    % "|".join(METERS))


def main(path):
    text = open(path, encoding="utf-8").read()
    data = tomllib.loads(text)
    canvases = data.get("canvases") or []
    # Split at each top-level [[canvases]] header; chunk i+1 is canvas i (chunk 0 is the preamble).
    chunks = re.split(r"(?m)^(?=\[\[canvases\]\]\s*$)", text)
    if len(chunks) - 1 != len(canvases):
        sys.exit(f"recap.py: {len(chunks) - 1} [[canvases]] headers but {len(canvases)} canvases parsed — stopping")
    moved = 0

    def bump(m):
        nonlocal moved
        old = int(m.group(2))
        if old not in STAGE_TOPS:
            return m.group(0)
        moved += 1
        return f"{m.group(1)}{STAGE_TOPS[old]}{m.group(3)}"

    out = [chunks[0]]
    for chunk, canvas in zip(chunks[1:], canvases):
        repeats = (canvas.get("trigger") or {}).get("is_repeatable", True) is not False
        out.append(RAISE.sub(bump, chunk) if repeats else chunk)
    open(path, "w", encoding="utf-8").write("".join(out))
    print(f"recap.py: {moved} repeatable stage-top cap(s) moved up one stage")


if __name__ == "__main__":
    main(sys.argv[1])
