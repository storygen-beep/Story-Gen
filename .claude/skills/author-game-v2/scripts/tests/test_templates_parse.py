"""Every TOML template loads as TOML (LO, 2026-09-28): a placeholder is quoted, never bare, so the
file an author copies is valid from the first save."""
import glob
import os

try:
    import tomllib
except ImportError:                      # py3.10
    import tomli as tomllib

TEMPLATES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                         "templates")


def test_every_toml_template_parses():
    files = sorted(glob.glob(os.path.join(TEMPLATES, "*.toml")))
    assert files
    for f in files:
        with open(f, "rb") as fh:
            tomllib.load(fh)


SHEETS = ["place", "person", "scene", "system", "opening", "decision"]


def test_every_sheet_template_is_one_page_of_slots():
    """PRD v2 DC9c · I20: six sheet templates, one page each, slots rather than example prose."""
    import re
    for name in SHEETS:
        path = os.path.join(TEMPLATES, "sheets", name + ".md")
        with open(path, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
        assert len(lines) <= 60, (name, len(lines))
        assert lines[0].startswith("# [REVIEW]"), name
        assert any("<" in l and ">" in l for l in lines), name
        # a table cell is a slot, a fixed choice or a key: never a filled sentence of prose
        for l in lines:
            if l.startswith("| ") and not set(l) <= set("|- "):
                for c in (c.strip() for c in l.strip("|").split("|")):
                    assert not re.search(r"^[A-Z][a-z]+( [a-z]+){4,}[.!?]$", c), (name, c)
