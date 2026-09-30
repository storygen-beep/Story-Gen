"""Shared harness for engine behaviour tests: build to scratch, drive the real game.

Every engine item of PRD_SKILL_TEST_FIXES_v2 phase 1 is proven the same way:

  1. build a checked-in fixture through the DEFAULT path — `package_from_toml`, no-DB,
     `--output <tmp> --no-prune` — never into games/<slug>/output/;
  2. open the compiled index.html in headless Chromium and ask the engine itself
     (`SugarCube.setup.*`, `SugarCube.State.variables`) — state, never a rendered label;
  3. for the old-save half (§0 rule 8), load a save string that a build made BEFORE
     the change actually wrote (`tests/data/*_pre_change_save.txt`) through
     `Save.deserialize`, which is SugarCube's real load path — onLoad, then the
     :passagestart backfill.

Skipped where tweego or Playwright's Chromium is absent. Not collected by pytest
(no `test_` prefix); import it from a test module.
"""
import os
import shutil
from contextlib import contextmanager

import pytest
from django.core.management import call_command

DATA = os.path.join(os.path.dirname(__file__), "data")

try:
    from playwright.sync_api import sync_playwright
except ImportError:  # pragma: no cover - environment without playwright
    sync_playwright = None

needs_browser = pytest.mark.skipif(
    sync_playwright is None or shutil.which("tweego") is None,
    reason="headless tests need playwright + tweego",
)


def build(toml_path, out_dir):
    """package_from_toml, default no-DB path, to a scratch dir. Returns index.html."""
    call_command(
        "package_from_toml",
        file=str(toml_path),
        output=str(out_dir),
        no_prune=True,
        stdout=open(os.devnull, "w"),
    )
    return os.path.join(str(out_dir), "index.html")


def read_data(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as fh:
        return fh.read().strip()


class Game:
    """A thin handle on one open page. Every read goes through the engine."""

    def __init__(self, page):
        self.page = page
        self.errors = []
        page.on("pageerror", lambda e: self.errors.append(str(e)))

    def js(self, expr, arg=None):
        return self.page.evaluate(expr, arg)

    def play(self, passage, settle=150):
        self.js("(p) => SugarCube.Engine.play(p)", passage)
        self.page.wait_for_timeout(settle)
        return self.passage()

    def passage(self):
        return self.js("() => SugarCube.State.passage")

    def sv(self, path):
        """A value under State.variables by dotted path, JSON round-tripped."""
        return self.js(
            """(p) => { let v = SugarCube.State.variables;
                for (const k of p.split('.')) { if (v == null) return null; v = v[k]; }
                return v === undefined ? null : JSON.parse(JSON.stringify(v)); }""",
            path,
        )

    def click(self, text, settle=150):
        """Click the passage link whose visible text is exactly `text`."""
        clicked = self.js(
            """(t) => { const a = [...document.querySelectorAll('.passage a')]
                .find(x => x.textContent.trim() === t);
                if (!a) return false; a.click(); return true; }""",
            text,
        )
        assert clicked, f"no link {text!r} on {self.passage()}"
        self.page.wait_for_timeout(settle)
        return self.passage()

    def advance_days(self, n):
        """Move the absolute day counter the way the engine's day roll does."""
        self.js("(n) => { SugarCube.State.variables.game_state.time_state.day += n; }", n)

    def load_save(self, save_string):
        ok = self.js(
            "(s) => { const r = SugarCube.Save.deserialize(s); return r !== null; }",
            save_string,
        )
        self.page.wait_for_timeout(250)
        return ok


@contextmanager
def open_game(html):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page()
            game = Game(page)
            page.goto("file://" + os.path.abspath(html))
            page.wait_for_function(
                "() => window.SugarCube && SugarCube.State && document.querySelector('.passage')"
            )
            yield game
        finally:
            browser.close()
