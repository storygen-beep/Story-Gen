#!/usr/bin/env python3
"""Render-bucket guard — catch canvases that will render as a flat solo LINK
when the author almost certainly meant an NPC PORTRAIT (Lane-1 hub) or a rolling
AMBIENT (Lane-2). Run it after merge, before/after packaging.

    python .claude/skills/author-game/scripts/check_render_buckets.py \
        games/<slug>/toml_phases/7_final_game.toml

Why this exists
---------------
The location screen buckets each canvas by fields on `[canvases.trigger]`, and the
build stays GREEN whichever bucket a canvas lands in — only live-play shows the wrong
one. The trap (see `references/toml-gotchas.md` "Trigger-field placement" and
`references/lanes.md` "Runtime rendering rules"):

  * `npc = "npc_x"`          -> sets `npcId` -> renders as a clickable NPC PORTRAIT.
  * `requires_npc = "npc_x"` -> gates PRESENCE only; it NEVER sets `npcId`.

So a repeatable, manual (`trigger_mode != "random"`), non-`substitution_only` canvas
that has `requires_npc` but no `npc` drops into the flat solo-link bucket — neither a
portrait nor a random roll. That is the exact defect that shipped across every hub in
The Inheritance (fixed 2026-07-19). One signature catches BOTH twin traps:

  * a Lane-1 HUB    -> add  npc = "npc_x"
  * a Lane-2 AMBIENT -> add  trigger_mode = "random"  +  chance = 0.NN

Honest limit
------------
This flags the COMMON slip (`requires_npc` set, `npc` forgotten). It CANNOT catch a hub
authored with NEITHER field (it is mechanically identical to a real solo activity like
`activity_sleep`); those need a content read. Reported at the end as a reminder.

Exit code: 1 if anything is flagged (so it can gate a build), else 0.
"""
import sys

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:  # pragma: no cover
    sys.stderr.write(
        "check_render_buckets: needs Python 3.11+ (tomllib). Run under the project venv.\n"
    )
    sys.exit(2)


def main(argv):
    if len(argv) != 2:
        sys.stderr.write(
            "usage: check_render_buckets.py games/<slug>/toml_phases/7_final_game.toml\n"
        )
        return 2
    path = argv[1]
    with open(path, "rb") as fh:
        data = tomllib.load(fh)

    flagged = []
    for canvas in data.get("canvases", []):
        trig = canvas.get("trigger", {}) or {}
        if not trig.get("is_repeatable"):
            continue  # one-shots auto-fire; never a clickable tile
        if trig.get("substitution_only"):
            continue  # Lane-3 substitution target, correctly not a tile
        if (trig.get("trigger_mode") or "manual") == "random":
            continue  # a rolling ambient — correct bucket
        if trig.get("npc"):
            continue  # already a portrait
        if trig.get("requires_npc"):
            flagged.append(
                (
                    canvas.get("id", "<no id>"),
                    trig.get("requires_npc"),
                    trig.get("location", "<no location>"),
                )
            )

    if flagged:
        print(
            f"RENDER-BUCKET GUARD: {len(flagged)} canvas(es) render as a FLAT SOLO LINK "
            f"(requires_npc set, npc missing) — confirm each is intended:"
        )
        for cid, rn, loc in flagged:
            print(f"  - {cid}  (requires_npc={rn!r}, location={loc!r})")
        print(
            "  Fix: a Lane-1 hub needs  npc = \"<id>\"  ; a Lane-2 ambient needs  "
            "trigger_mode = \"random\" + chance.\n"
            "  (A deliberately presence-gated flat link is rare — if that's what you want, ignore.)\n"
            "  Not catchable here: a hub authored with NEITHER npc nor requires_npc reads as a\n"
            "  plain solo activity — verify by content that every present-NPC surface has npc set."
        )
        return 1

    print("RENDER-BUCKET GUARD: OK — no requires_npc-without-npc canvases.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
