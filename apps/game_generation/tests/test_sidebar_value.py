"""EN9 — sidebar "Label: N · word".

PRD_SKILL_TEST_FIXES_v2 §2 EN9 (D4). No sidebar type printed a trait as "Corruption: 12
· Curious": `trait_bar` always draws the bar and `trait_words` prints the band word only.

`[[sidebar_items]] type = "trait_words"` gains `show_value = true`: one line, "Label: N ·
<band word>", or "Label: N" when no band matches. The label is the item's `label`, else
the trait's one name (EN5 `setup.traitLabel`). Without `show_value` the widget is
byte-identical to the pre-change engine's.

Old saves (§0 rule 8): no new state; a save the pre-change build wrote shows the line.

    pytest apps/game_generation/tests/test_sidebar_value.py -q
"""
import warnings

import pytest

from apps.game_generation.twee_comprehensive.generators.v2 import (
    TweeComprehensiveGeneratorV2,
)
from apps.projects.services.game_graph import build_game_graph
from apps.projects.services.template_import import normalize, parse_toml, validate

from .headless import build, needs_browser, open_game, read_data

FIXTURE = "apps/game_generation/games_toml_files/engine_skill_test_fixes_2026_09_30.toml"
ITEM = 'show_value = true\nbands      = [ { min = 0, max = 9, text = "Clean" }'


def _raw():
    return parse_toml(FIXTURE)


def _item(raw):
    return next(i for i in raw["sidebar_items"] if i.get("show_value"))


def _validate(raw):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return validate(normalize(raw))


def test_the_fixture_is_clean():
    assert _validate(_raw()) == []


def test_show_value_must_be_a_bool():
    raw = _raw()
    _item(raw)["show_value"] = "true"
    assert any("'show_value' must be true or false" in e for e in _validate(raw))


def test_without_show_value_the_widget_is_as_before():
    """§0 rule 7. The golden is the TimeWidgets passage (it holds sidebarItems) the engine
    BEFORE EN9 (the EN8 tree, snapshotted to scratch; it ignores show_value) generated."""
    raw = _raw()
    _item(raw).pop("show_value")
    graph = build_game_graph(normalize(raw))
    twee = TweeComprehensiveGeneratorV2().generate(graph.project, {}, graph=graph)
    widgets = next("\n:: " + p for p in twee.split("\n:: ") if p.startswith("TimeWidgets"))
    assert widgets.strip() == read_data("en9_timewidgets_golden.txt")


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    return build(FIXTURE, tmp_path_factory.mktemp("en9") / "out")


def _variant(tmp_path_factory, name, old, new):
    text = open(FIXTURE).read()
    assert text.count(old) == 1
    out = tmp_path_factory.mktemp(name)
    toml = out / "fixture.toml"
    toml.write_text(text.replace(old, new))
    return build(toml, out / "out")


def _line(g, corr=None):
    if corr is not None:
        g.js("(v) => { SugarCube.State.variables.player.core_traits.corr = v; }", corr)
    g.play("Location_loc_home")
    return g.js("() => [...document.querySelectorAll('.trait-words-value')]"
                ".map(e => e.innerText.replace(/\\s+/g, ' ').trim())")


@needs_browser
def test_label_number_and_word(html):
    with open_game(html) as g:
        assert _line(g) == ["Corruption: 5 · Clean"]
        assert _line(g, 12) == ["Corruption: 12 · Curious"]
        assert _line(g, 50) == ["Corruption: 50"]        # no band matches
        assert g.errors == []


@needs_browser
def test_an_authored_label_wins(tmp_path_factory):
    html = _variant(tmp_path_factory, "en9_label", ITEM, 'label = "Heat"\n' + ITEM)
    with open_game(html) as g:
        assert _line(g, 12) == ["Heat: 12 · Curious"]


@needs_browser
def test_an_npc_owned_item(tmp_path_factory):
    old = 'trait      = "corr"\n' + ITEM
    new = 'trait      = "trust"\ntrait_owner = "npc"\nnpc_id     = "vic"\n' + ITEM
    html = _variant(tmp_path_factory, "en9_npc", old, new)
    with open_game(html) as g:
        assert _line(g) == ["Trust: 70"]
        assert g.errors == []


@needs_browser
def test_a_save_made_before_en9(html):
    """§0 rule 8. Written by the PRE-change engine (the EN8 tree, snapshotted to scratch):
    the fixture built with it, Engine.play Location_loc_home, Save.serialize()."""
    with open_game(html) as g:
        assert g.load_save(read_data("en9_pre_change_save.txt")) is True
        assert g.passage() == "Location_loc_home"
        assert _line(g, 12) == ["Corruption: 12 · Curious"]
        assert g.errors == []
