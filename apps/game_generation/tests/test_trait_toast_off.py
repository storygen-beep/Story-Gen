"""`toast = false` on a [[traits.labels]] entry keeps a bookkeeping count out of the effect toast.

The "+N" toast stays for every trait by default (D1b). A label with `toast = false` is skipped by
setup.showEffectNotification, and nothing else about the trait changes: it still moves, still
gates. The importer accepts only true or false, and writes the key to the metadata only when
false, so every existing game is unchanged.

The failure (2026-11-24): first_term_lean counts meals in a hidden trait, meals_today, so a meal
can share the three-a-day cap with eating with Mom; every meal toasted "+1 Meals today", a leak of
an internal count.

    pytest apps/game_generation/tests/test_trait_toast_off.py -q
"""
import os

import pytest

from apps.projects.services.template_import import TemplateTraitLabel

from .headless import build, needs_browser, open_game

GAME = "games/first_term_lean/toml_phases/7_final_game.toml"


def test_toast_defaults_to_true():
    assert TemplateTraitLabel(key="k", label="", toast=False).toast is False
    assert TemplateTraitLabel(key="k", label="").toast is True


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    if not os.path.exists(GAME):
        pytest.skip("first_term_lean not present")
    return build(GAME, tmp_path_factory.mktemp("toast_off") / "out")


def _toast_after(g, trait, delta):
    return g.js(
        """([t, d]) => { document.querySelectorAll('.effect-toast').forEach(e => e.remove());
            SugarCube.setup.pendingEffects = [{ type: 'trait', trait: t, delta: d }];
            SugarCube.setup.showEffectNotification();
            const e = document.querySelector('.effect-toast'); return e ? e.textContent : null; }""",
        [trait, delta],
    )


@needs_browser
def test_a_toast_off_trait_is_not_named(html):
    with open_game(html) as g:
        g.js("() => { SugarCube.setup.noToastTraits = ['meals_today']; }")
        assert _toast_after(g, "meals_today", 1) is None
        assert g.errors == []


@needs_browser
def test_every_other_trait_still_toasts(html):
    with open_game(html) as g:
        g.js("() => { SugarCube.setup.noToastTraits = ['meals_today']; }")
        text = _toast_after(g, "energy", 5)
        assert text and "+5" in text, text
        assert g.errors == []


def test_nothing_is_written_when_toast_is_left_alone():
    with open("apps/projects/services/template_import.py", encoding="utf-8") as fh:
        src = fh.read()
    assert '**({"toast": False} if tl.toast is False else {})' in src
