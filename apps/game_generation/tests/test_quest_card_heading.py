"""Two engine fixes from the first_term alignment check.

C3 — a quest card's optional `heading`. A card shown before the player has met the person
cannot print the person's name, so `heading` replaces the name wherever that card is listed
by person: the Quests page section heading (cards layout), the person row of the list
layout, and the cast page row (which also hides the portrait) and its schedule dialog.
A card without `heading` draws exactly as before. `heading` on a Story Goal card (no
npc_id) has no name to replace: the validator warns, as it does for `group` on an NPC card.

S15 — a dress-slot garment worn from the start (`initial = true`) takes off the top and
bottom, and a top or bottom worn from the start takes off the dress, in file order: the
same slot rule as setup.equipItem.

    pytest apps/game_generation/tests/test_quest_card_heading.py -q
"""
import json
import re
import warnings

import pytest

from apps.game_generation.twee_comprehensive.generators.v2 import (
    TweeComprehensiveGeneratorV2,
)
from apps.projects.services.game_graph import build_game_graph
from apps.projects.services.template_import import normalize, parse_toml, validate

from .headless import build, needs_browser, open_game

QUESTS_FIXTURE = "apps/game_generation/games_toml_files/engine_skill_test_fixes_2026_09_30.toml"
CLOTHING_FIXTURE = "apps/game_generation/games_toml_files/engine_ws_batch3_2026_10_02.toml"

HEADING = "Someone behind the bar"
TOBIN_CARD = 'npc_id = "tobin"\ntext   = "Tobin runs the bar."\n'


def _twee(raw):
    graph = build_game_graph(normalize(raw))
    return TweeComprehensiveGeneratorV2().generate(graph.project, {}, graph=graph)


def _quests_text(layout=None):
    text = open(QUESTS_FIXTURE).read()
    assert text.count(TOBIN_CARD) == 1
    text = text.replace(TOBIN_CARD, TOBIN_CARD + f'heading = "{HEADING}"\n', 1)
    if layout:
        text = text.replace("\n[ui.cast_page]\n", f'\n[ui]\nquests_layout = "{layout}"\n\n[ui.cast_page]\n', 1)
    return text


# ── C3: the importer ─────────────────────────────────────────────────────────


def test_heading_reaches_the_runtime_card(tmp_path):
    toml = tmp_path / "g.toml"
    toml.write_text(_quests_text())
    raw = parse_toml(str(toml))
    assert validate(normalize(raw)) == []
    twee = _twee(raw)
    assert f'"heading": "{HEADING}"' in twee
    # Only the card that carries it: Vic's card has no heading key at all.
    assert twee.count('"heading":') == 1


def test_no_heading_no_key():
    twee = _twee(parse_toml(QUESTS_FIXTURE))
    assert '"heading":' not in twee


def test_heading_on_a_story_card_warns():
    raw = parse_toml(QUESTS_FIXTURE)
    raw["quest_cards"].append({
        "text": "A story goal.",
        "heading": "Nobody",
        "when": [{"flag": "started", "op": "is_true"}],
    })
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        errors = validate(normalize(raw))
    assert errors == []
    assert any("`heading` is NPC cards only" in str(w.message) for w in caught)


# ── C3: what the player sees ─────────────────────────────────────────────────


@pytest.fixture(scope="module")
def cards_html(tmp_path_factory):
    out = tmp_path_factory.mktemp("heading_cards")
    toml = out / "fixture.toml"
    toml.write_text(_quests_text())
    return build(toml, out / "out")


@pytest.fixture(scope="module")
def list_html(tmp_path_factory):
    out = tmp_path_factory.mktemp("heading_list")
    toml = out / "fixture.toml"
    toml.write_text(_quests_text("list"))
    return build(toml, out / "out")


def _start(g):
    g.js("() => { SugarCube.State.variables.flags.started = true; }")


@needs_browser
def test_cards_layout_heading_replaces_the_name(cards_html):
    with open_game(cards_html) as g:
        _start(g)
        g.play("QuestsPage")
        heads = g.js("() => [...document.querySelectorAll('.quests-section h3')].map(h => h.textContent.trim())")
        # (The card's own text still says "Tobin runs the bar." — the author's words are
        # untouched; only the name the engine draws is replaced.)
        assert heads == [HEADING, "Vic"]
        assert g.errors == []


@needs_browser
def test_cast_page_heading_replaces_name_and_face(cards_html):
    with open_game(cards_html) as g:
        _start(g)
        g.play("CastPage")
        names = g.js("() => [...document.querySelectorAll('.cast-card .stats-name')].map(n => n.textContent.trim())")
        assert sorted(names) == sorted([HEADING, "Vic"])
        # The row with the heading draws no portrait image (the placeholder stands in).
        imgs = g.js("""() => [...document.querySelectorAll('.cast-card')].map(c =>
            [c.querySelector('.stats-name').textContent.trim(), !!c.querySelector('.cast-face img')])""")
        assert dict(imgs)[HEADING] is False
        roster = g.js("() => SugarCube.setup.castRoster().map(e => [e.slug, e.name, e.faceHidden])")
        assert ["tobin", HEADING, True] in roster and ["vic", "Vic", False] in roster
        assert g.errors == []


@needs_browser
def test_list_layout_heading_replaces_the_name(list_html):
    with open_game(list_html) as g:
        _start(g)
        g.play("QuestsPage")
        names = g.js("() => [...document.querySelectorAll('.quests-name')].map(n => n.textContent)")
        assert names == [HEADING, "Vic"]
        assert g.errors == []


@needs_browser
def test_without_heading_the_name_is_printed(tmp_path):
    html = build(QUESTS_FIXTURE, tmp_path / "out")
    with open_game(html) as g:
        _start(g)
        g.play("QuestsPage")
        heads = g.js("() => [...document.querySelectorAll('.quests-section h3')].map(h => h.textContent.trim())")
        assert heads == ["Tobin", "Vic"]
        g.play("CastPage")
        roster = g.js("() => SugarCube.setup.castRoster().map(e => [e.name, e.faceHidden])")
        assert sorted(roster) == [["Tobin", False], ["Vic", False]]
        assert g.errors == []


# ── S15: a dress worn from the start ─────────────────────────────────────────


def _equipped_at_start(raw):
    twee = _twee(raw)
    m = re.search(r'"equipped": (\{[^}]*\})', twee)
    assert m, "no $player.equipped in the start state"
    return json.loads(m.group(1))


def _clothing(raw, item_id):
    return next(c for c in raw["clothing"] if c["id"] == item_id)


def test_top_and_bottom_without_a_dress_are_unchanged():
    eq = _equipped_at_start(parse_toml(CLOTHING_FIXTURE))
    assert eq["top"] == "blouse" and eq["bottom"] == "skirt" and eq["dress"] is None
    assert eq["bra"] == "bra"


def test_a_dress_worn_at_start_takes_off_top_and_bottom():
    raw = parse_toml(CLOTHING_FIXTURE)
    _clothing(raw, "slip")["initial"] = True  # the slip comes after blouse and skirt
    eq = _equipped_at_start(raw)
    assert eq["dress"] == "slip"
    assert eq["top"] is None and eq["bottom"] is None
    assert eq["bra"] == "bra"  # other slots are untouched, as in equipItem


def test_a_top_after_the_dress_takes_the_dress_off():
    raw = parse_toml(CLOTHING_FIXTURE)
    slip = _clothing(raw, "slip")
    slip["initial"] = True
    # File order: slip, blouse, skirt, bra — equipItem in that order ends on blouse + skirt.
    raw["clothing"].remove(slip)
    raw["clothing"].insert(0, slip)
    eq = _equipped_at_start(raw)
    assert eq["dress"] is None
    assert eq["top"] == "blouse" and eq["bottom"] == "skirt"
