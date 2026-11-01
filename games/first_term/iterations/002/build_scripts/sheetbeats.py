"""Measured beats, read verbatim from the signed scene sheets (release 1, 2026-11-01). A beat is the
blockquote under its heading: `**`node`**` on a step sheet, `**1a**` in a pool sheet. Reading them from
the sheet keeps the build and the signed text one thing; a missing heading stops the build."""
import os, re

SCENES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "sheets", "scenes")


def beat(sheet, key):
    """The blockquote after the line that starts with **`key`** or **key** in sheets/scenes/<sheet>.md."""
    lines = open(os.path.join(SCENES, sheet + ".md"), encoding="utf-8").read().splitlines()
    heads = (f"**`{key}`**", f"**{key}**")
    for i, l in enumerate(lines):
        if l.startswith(heads):
            for m in lines[i + 1:]:
                if m.startswith("> "):
                    return m[2:].strip()
                if m.startswith("**") or m.startswith("#"):
                    break
    raise KeyError(f"{sheet}: no beat under {key!r}")


def pool(sheet, n, keys="abc"):
    return [beat(sheet, f"{n}{k}") for k in keys]
