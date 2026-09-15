#!/usr/bin/env python3
"""Where an @token reaches the player unresolved — a LIST, never a score.

Run from the repo root:

    venv/bin/python games/the_balance/process/tokens.py [slug]

WHY THIS EXISTS
---------------
The generator swaps `@gil` for a character's display name, but only on the surfaces
that call `_resolve_at_references` (v2.py:14936) or its runtime twin
`setup.resolveAtRefs` (v2.py:3421). Everywhere else the raw `@gil` reaches the screen.

The first build of this game shipped seven of those. The worst was the character
creation screen — literally the first screen — reading "@gil's son, twenty, a senior
at your college", and `locations[nate_room].name = "@nate's Room"`, which prints on
nine separate surfaces.

WHY NOT JUST USE gates.py
-------------------------
`lint_unresolved_tokens` (gates.py:1269) exists and reports most of them, but it
scans a hardcoded list of eight (section, field) pairs, **top-level arrays only, one
level deep**, and drops any value that is not a `str` (gates.py:1292). That last line
silently kills every list-valued field, which is exactly where three of this game's
leaks were hiding: `npcs[].tags` and `npcs[].relationship_options`. It also never
looks at `traits` at all.

Fixing that lint is a skill edit, which this game does not do (process/README.md §0).
So the game carries its own, and this one walks the tree recursively at any depth,
through strings and through lists of strings.

⚠️ THE TOKENS ARE NOT THE BUG. `npc_gil` and `npc_nate` are `customizable = true`
(1_metadata_and_locations.toml:200, :271) — the player can rename them, and the
listbox at v2.py:9418 lets them change the relationship too. That is why the prose
uses tokens and must keep using them. A leak is fixed by rewriting the text so it
needs neither the name nor the relationship, never by hardcoding "Gil".
"""

import pathlib
import re
import sys
import tomllib

TOKEN = re.compile(r"@(\w+(?:\.\w+)?)")

# Surfaces where the generator actually calls a resolver. Taken from the call sites
# in v2.py, NOT from gates.py's header comment, which names four and is missing
# seven (door description, description_variants, door option text and locked_text,
# npc role, and the nine runtime phone/emotion surfaces).
#
# Paths below are normalised: every list index becomes "[]".
RESOLVED_EXACT = {
    "locations[].description",                  # v2.py:10035
    "locations[].blocked_message",              # v2.py:9910  — see the caveat below
    "locations[].description_variants[].text",  # v2.py:10059
    "npcs[].role",                              # v2.py:15571
}

# ⚠️ blocked_message is HALF-resolved and is listed above as resolved on purpose.
# The location passage resolves it (v2.py:9910) but the copy baked into
# setup.locations (v2.py:1020) is raw, and navDestBlockedReason (v2.py:5032) prints
# that raw string onto the nav card. This game has no @ in any blocked_message.
# Do not add one.


def resolved(path):
    """Does the generator resolve tokens at this normalised key path?"""
    if path in RESOLVED_EXACT:
        return True
    # Canvas block prose and choice labels: v2.py:15483 and :13546. Blocks nest
    # through `blocks[]` and `props.blocks[]`, so match on the tail, not the shape.
    if path.startswith("canvases[].nodes[]"):
        if path.endswith(".content"):
            return True
        if path.endswith(".text") and ("choices[]" in path or "exit_block" in path):
            return True
    # Doors: description v2.py:9992, option text :12635, option locked_text :12637.
    if path.startswith("locations[].properties.door"):
        return path.endswith((".description", ".text", ".locked_text"))
    # The phone resolves at runtime instead: v2.py:2267, :2543, :2607, :2615, :2643.
    if path.startswith("phone."):
        return path.endswith((".content", ".text", ".notify",
                              ".player_message", ".npc_response"))
    # story_arc emotion ranges, v2.py:6617.
    if path.startswith("story_arc.") and path.endswith(".description"):
        return True
    return False


def never_rendered(path, ctx):
    """Keys the generator never emits, so a token there is a source-only untruth."""
    if path == "canvases[].description":
        return "canvas description is never emitted by the generator"
    # npcs[].description reaches only the CustomizeCharacters screen, and only for
    # NPCs with customizable = true (filter at v2.py:9372). For everyone else the
    # field is popped from the payload at v2.py:1056 and renders nowhere.
    if path == "npcs[].description" and not ctx.get("customizable"):
        return f"{ctx.get('id', 'npc')} is not customizable — description is dropped at v2.py:1056"
    return None


def walk(node, path="", ctx=None, out=None):
    """Depth-first over the parsed TOML, normalising list indices to '[]'."""
    out = [] if out is None else out
    ctx = ctx or {}
    if isinstance(node, dict):
        # Carry the owning NPC's identity down, so never_rendered() can consult it.
        if "customizable" in node or ("id" in node and "relationship_options" in node):
            ctx = {**ctx, "id": node.get("id"), "customizable": node.get("customizable")}
        for key, value in node.items():
            walk(value, f"{path}.{key}" if path else key, ctx, out)
    elif isinstance(node, list):
        for item in node:
            walk(item, f"{path}[]", ctx, out)
    elif isinstance(node, str):
        for match in TOKEN.finditer(node):
            out.append((path, match.group(0), node, ctx))
    return out


def main():
    slug = sys.argv[1] if len(sys.argv) > 1 else "the_balance"
    merged = pathlib.Path(f"games/{slug}/toml_phases/7_final_game.toml")
    if not merged.exists():
        sys.exit(f"no merged TOML at {merged} — run merge_toml_phases.py first")

    game = tomllib.loads(merged.read_text(encoding="utf-8"))
    # `@player` is resolved everywhere the NPC tokens are, and it is not a character
    # slug, so it is checked by the same rules rather than excluded.
    hits = walk(game)

    leaks, dead, fine = [], [], []
    for path, token, text, ctx in hits:
        if resolved(path):
            fine.append((path, token))
            continue
        why = never_rendered(path, ctx)
        (dead if why else leaks).append((path, token, text, why))

    print(f"\n  tokens — {slug}")
    print(f"  {len(hits)} @token(s): {len(fine)} on resolving surfaces, "
          f"{len(dead)} on keys that never render, {len(leaks)} LEAKING\n")

    if leaks:
        print("  LEAKS — the player reads the @ sign")
        for path, token, text, _ in sorted(leaks):
            excerpt = text if len(text) <= 64 else text[:61] + "…"
            print(f"    {token:8} {path}")
            print(f"             {excerpt}")
        print()
    else:
        print("  no leaks — every token sits on a surface the engine resolves\n")

    if dead:
        print("  never rendered — not a player defect, but the source says something untrue")
        for path, token, _, why in sorted(dead):
            print(f"    {token:8} {path}   ({why})")
        print()

    print("  A LIST, NEVER A SCORE. A token is right in prose and wrong in a label:")
    print("  Gil and Nate are renameable, so prose MUST use the token. A leaking key is")
    print("  fixed by rewriting the text to need neither the name nor the relationship.")
    print("  See process/README.md §5c.\n")
    return 1 if leaks else 0


if __name__ == "__main__":
    sys.exit(main())
