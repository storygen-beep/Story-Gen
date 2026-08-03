#!/usr/bin/env python3
"""Cascade-order guard — catch scene nodes where content renders BELOW the reveal link.

    python .claude/skills/author-game/scripts/check_cascade_order.py \
        games/<slug>/toml_phases/7_final_game.toml

Why this exists
---------------
The engine draws a node's `blocks` EAGERLY, top-to-bottom, in source order
(`_convert_blocks_to_game_html`, v2.py). A `cascade` block reveals only its OWN beats
(click-to-drip); it cannot defer, hide, or reorder a SIBLING block. The one thing the
engine holds back for an unfinished cascade is the `exit_block` nav links (spliced into
the cascade's tail) — and `exit_block` is a SEPARATE node key, NOT an entry in `blocks`.

So any content block placed AFTER a `cascade` in the same node's `blocks` array renders
IMMEDIATELY, below the advance link — the `[content][link][content][link]` layout, with
prose stranded under the reveal. TWO cascades in one node splice the exit TWICE (a
duplicate nav link). The build stays GREEN; only live-play shows it. (See
`references/engine-reference.md` — the cascade contract — and `references/toml-gotchas.md`.)

The rule: a `cascade` is the LAST content block in its node — only `exit_block` may
follow it — and use ONE cascade per node. Fold a mid-scene bridge or a closing beat INTO
the cascade (its own `advance_text` beat, or a no-`advance_text` terminal beat).

Honest limit
------------
Checks TOP-LEVEL `blocks` per node (where the defect lives). It does not recurse into a
`group` block's nested blocks — a cascade buried inside a `group` with siblings after it
is rare and needs a content read.

Exit code: 1 if anything is flagged (so it can gate a build), else 0.
"""
import sys

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:  # pragma: no cover
    sys.stderr.write(
        "check_cascade_order: needs Python 3.11+ (tomllib). Run under the project venv.\n"
    )
    sys.exit(2)


def main(argv):
    if len(argv) != 2:
        sys.stderr.write(
            "usage: check_cascade_order.py games/<slug>/toml_phases/7_final_game.toml\n"
        )
        return 2
    path = argv[1]
    with open(path, "rb") as fh:
        data = tomllib.load(fh)

    flagged = []  # (canvas_id, node_id, reason)
    for canvas in data.get("canvases", []):
        cid = canvas.get("id", "<no id>")
        for node in canvas.get("nodes", []) or []:
            nid = node.get("id", "<no id>")
            blocks = node.get("blocks", []) or []
            casc_idx = [
                i for i, b in enumerate(blocks) if (b or {}).get("type") == "cascade"
            ]
            if not casc_idx:
                continue
            first = casc_idx[0]
            trailing = blocks[first + 1:]  # exit_block is a separate node key, never here
            if trailing:
                types = ", ".join((b or {}).get("type", "?") for b in trailing)
                extra = " (>1 cascade in this node)" if len(casc_idx) > 1 else ""
                flagged.append(
                    (cid, nid, f"{len(trailing)} block(s) after the cascade: [{types}]{extra}")
                )

    if flagged:
        print(
            f"CASCADE-ORDER GUARD: {len(flagged)} node(s) render CONTENT BELOW THE REVEAL LINK "
            f"(a block follows a `cascade` in `blocks`):"
        )
        for cid, nid, reason in flagged:
            print(f"  - {cid} :: node {nid}  — {reason}")
        print(
            "  Fix: a `cascade` must be the LAST content block in its node — only `exit_block` may\n"
            "  follow it — and use ONE cascade per node. Fold a mid-scene bridge or a closing beat\n"
            "  INTO the cascade (its own `advance_text` beat, or a no-`advance_text` terminal beat).\n"
            "  (`exit_block` is a separate node key, not a block — cascade-then-exit_block is CORRECT.)\n"
            "  Full contract: references/engine-reference.md (the cascade section)."
        )
        return 1

    print("CASCADE-ORDER GUARD: OK — every cascade is the last block in its node.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
