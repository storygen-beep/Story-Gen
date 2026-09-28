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
