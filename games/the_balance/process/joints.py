#!/usr/bin/env python3
"""How the clauses are joined — a LIST, never a score.

Run from the repo root:

    venv/bin/python games/the_balance/process/joints.py [slug]

Prints the joint composition of a game's prose next to the 25-game field corpus.
Nothing here is a pass mark. See process/README.md section 5b for what the numbers
are for and what they are not.

WHY THIS EXISTS
---------------
LO read the first build and said the writing was "very short and compressed and
several pieces of information were packed together without clear grammatical
relationships." Measuring it found one number outside the field's entire range,
and it was not the one I expected:

    but per 1,000 words     field 2.46 - 8.44 (median 4.68)     the_balance 0.14

Zero of the field's 25 games come in under 0.5. The two uses in the whole game
were both spoken by characters, so the narration ran a flat zero across 5,775
words: the narrator could never contradict itself. The coordination ratio, which
is what I first blamed, sits comfortably inside the field's range and is not a
defect.

THE TWO BASES MUST MATCH
------------------------
The field exists only as built HTML; our games exist as authored TOML. Comparing
them needs both sides extracted the same way, so the two functions below are
copied verbatim from the study that set the skill's own DASH_CEILING:

    ~/Documents/Prose_Machine_Sound_Study_20260828/measure.py:38  field_prose()
    ~/Documents/Prose_Machine_Sound_Study_20260828/measure.py:59  our_prose()

Copied rather than imported on purpose: that module runs its whole study at
import time and then raises IndexError on sys.argv.

Both sides therefore include dialogue and location descriptions. A rate over word
count survives the change of basis; anything counted per sentence does not.
"""

import html as _html
import json
import pathlib
import re
import statistics
import sys
import tomllib

FIELD_DIR = pathlib.Path.home() / "Documents/Mopoga_Twine_Sandbox_Research_20260724/gamehtml"
FIELD_SLUGS = pathlib.Path.home() / "Documents/Prose_Machine_Sound_Study_20260828/results.json"

SKIP_TAG = re.compile(r'tags="[^"]*\b(script|stylesheet|widget|init|Widget)\b', re.I)
PROSE_TYPES = ("paragraph", "dialog", "thought_bubble")

# The joints, by what they tell the reader.
#
# `but` and `yet` are deliberately in NEITHER list. They are coordinating
# conjunctions like `and`, so they do not belong with the subordinators, and
# putting them in the denominator would make the ratio a second telling of the
# `but` finding instead of an independent one. `but` gets its own line.
COORDINATION = ("and", "then", "or")          # "here is the next thing"
SUBORDINATION = (
    "because", "so", "since",                 # cause
    "though", "although", "while", "whereas",  # contrast
    "after", "before", "until", "when", "once",  # time
)

# The clause that explains the fact it is attached to. register.md's load rule L1
# bans these outright; they are counted here so that a pass which adds relationship
# words cannot quietly add glosses instead.
#
# Only the WELDED form counts. L1's own prescription is "delete the clause, or make
# it its own sentence", so a judgment standing as its own sentence — "That is the
# arrangement they have." — is the fix, not the defect. An earlier version of this
# regex counted those too and would have scored the repair as a regression.
GLOSS = re.compile(r", (which (is|was|means)|and that is the|that is the)\b", re.I)


def field_prose(path):
    """Built Twine HTML to bare prose. measure.py:38, unchanged."""
    raw = path.read_text(encoding="utf-8", errors="replace")
    parts = re.findall(r"(<tw-passagedata[^>]*>)(.*?)</tw-passagedata>", raw, re.S)
    parts = [body for head, body in parts if not SKIP_TAG.search(head)]
    cap = 1500
    if len(parts) > cap:
        step = len(parts) / cap
        parts = [parts[int(i * step)] for i in range(cap)]
    text = _html.unescape("\n".join(parts))
    text = re.sub(r"/\*.*?\*/", " ", text, flags=re.S)
    text = re.sub(r"<<.*?>>", " ", text, flags=re.S)
    text = re.sub(r"\([a-zA-Z-]{2,20}:[^)]{0,300}\)", " ", text)
    text = re.sub(r"\[img\[.*?\]\]", " ", text, flags=re.S)
    text = re.sub(r"\[\[.*?\]\]", " ", text, flags=re.S)
    text = re.sub(r"<[^>]{1,200}>", " ", text)
    text = re.sub(r"[$_][A-Za-z][A-Za-z0-9_.]*", " ", text)
    return re.sub(r"''|//|@@|\{|\}", " ", text)


def our_prose(path, types=PROSE_TYPES, with_locations=True):
    """Merged TOML to bare prose. measure.py:59, plus the two filters this script needs.

    Walks nested containers as well as node blocks, because group and block_pool
    variants hold prose in props["blocks"] and were invisible to an earlier version
    of this walk.
    """
    game = tomllib.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    out = []

    def walk(blocks):
        for block in blocks or []:
            if not isinstance(block, dict):
                continue
            if block.get("type") in types and isinstance(block.get("content"), str):
                out.append(block["content"])
            props = block.get("props") or {}
            for beat in props.get("beats") or []:
                walk(beat.get("blocks"))
            walk(props.get("blocks") or block.get("blocks"))

    for canvas in game.get("canvases") or []:
        for node in canvas.get("nodes") or []:
            walk(node.get("blocks"))
    if with_locations:
        for loc in game.get("locations") or []:
            if isinstance(loc.get("description"), str):
                out.append(loc["description"])
    return " ".join(out)


def count(text, word):
    return len(re.findall(r"(?<![\w])" + word + r"(?![\w])", text, re.I))


def profile(text):
    words = len(text.split()) or 1
    coordination = sum(count(text, w) for w in COORDINATION)
    subordination = sum(count(text, w) for w in SUBORDINATION)
    return {
        "words": words,
        "and_1k": count(text, "and") * 1000 / words,
        "but_1k": count(text, "but") * 1000 / words,
        "ratio": coordination / max(subordination, 1),
        "gloss": len(GLOSS.findall(text)),
    }


def field_profiles():
    """The same 25 games the skill's writing thresholds were measured over."""
    slugs = json.loads(FIELD_SLUGS.read_text())["field"].keys()
    out = {}
    for slug in sorted(slugs):
        path = FIELD_DIR / f"{slug}.html"
        if not path.exists():
            continue
        text = field_prose(path)
        if len(text.split()) < 500:
            continue
        out[slug] = profile(text)
    return out


def band(values):
    lo, hi = min(values), max(values)
    return lo, statistics.median(values), hi


def main():
    slug = sys.argv[1] if len(sys.argv) > 1 else "the_balance"
    merged = pathlib.Path(f"games/{slug}/toml_phases/7_final_game.toml")
    if not merged.exists():
        sys.exit(f"no merged TOML at {merged} — run merge_toml_phases.py first")

    if not FIELD_DIR.exists():
        sys.exit(
            f"field corpus missing at {FIELD_DIR}\n"
            "It lives outside the repo. Without it these numbers have nothing to sit against."
        )

    field = field_profiles()
    and_lo, and_mid, and_hi = band([g["and_1k"] for g in field.values()])
    but_lo, but_mid, but_hi = band([g["but_1k"] for g in field.values()])
    rat_lo, rat_mid, rat_hi = band([g["ratio"] for g in field.values()])

    whole = profile(our_prose(merged))
    narration = profile(our_prose(merged, types=("paragraph", "thought_bubble")))

    def verdict(value, lo, hi):
        if value < lo:
            return "BELOW THE FIELD MINIMUM"
        if value > hi:
            return "ABOVE THE FIELD MAXIMUM"
        return "inside"

    print(f"\n  joints — {slug}, {whole['words']:,} words on the study's basis")
    print(f"  {'':34}{'field, 25 games':>26}")
    print(
        f"  and per 1,000 words    {whole['and_1k']:7.1f}"
        f"   {and_lo:6.1f} - {and_hi:5.1f} (median {and_mid:4.1f})   {verdict(whole['and_1k'], and_lo, and_hi)}"
    )
    print(
        f"  but per 1,000 words    {whole['but_1k']:7.2f}"
        f"   {but_lo:6.2f} - {but_hi:5.2f} (median {but_mid:4.2f})   {verdict(whole['but_1k'], but_lo, but_hi)}"
    )
    print(
        f"  coordination:subord.   {whole['ratio']:7.2f}"
        f"   {rat_lo:6.2f} - {rat_hi:5.2f} (median {rat_mid:4.2f})   {verdict(whole['ratio'], rat_lo, rat_hi)}"
    )
    print(f"  gloss (, which is / that is the)  {whole['gloss']:3d}   register.md L1 bans these — this must never rise")

    print(f"\n  narration alone — {narration['words']:,} words, no speech")
    print(f"    but per 1,000 words  {narration['but_1k']:6.2f}   `but` at zero means the narrator never turns a thought")
    print(f"    and per 1,000 words  {narration['and_1k']:6.1f}")

    others = [g for g in ("vesper", "vesper_two") if pathlib.Path(f"games/{g}/toml_phases/7_final_game.toml").exists()]
    if others:
        print("\n  the house, same basis")
        for other in others:
            p = profile(our_prose(f"games/{other}/toml_phases/7_final_game.toml"))
            print(f"    {other:12} but {p['but_1k']:5.2f}/1k   and {p['and_1k']:5.1f}/1k   ratio {p['ratio']:4.2f}:1")

    print("\n  A LIST, NEVER A SCORE. Short sentences, fragments, and `and` joining a real")
    print("  sequence are not defects — our coordination ratio sits inside the field's range.")
    print("  The number that left the distribution is `but`. See process/README.md section 5b.\n")


if __name__ == "__main__":
    main()
