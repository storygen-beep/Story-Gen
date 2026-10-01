"""E7b (World and Systems PRD) — two wardrobe switches, both off by default.

  * `[settings] wardrobe_change_on_refusal = true`: a place's `entry_conditions` refusal
    offers "Change clothes" when the unmet part is a clothing condition (`worn_*`,
    `clothing_slot`, `clothing_item`); the wardrobe's Back re-tries the place.
  * `[settings] wardrobe_anywhere = false`: "Change clothes" (on a dress code's
    ClothingBlock, and on the refusal) shows only where she can really change — a
    wardrobe room. The default keeps the old loophole: change from anywhere.

E7d — `wardrobe_location` may be a list: every room in it gets "Change Clothes" and counts
as a wardrobe room for `wardrobe_anywhere = false`.

    pytest apps/game_generation/tests/test_wardrobe_switches.py -q
"""
import pytest

from .headless import build, needs_browser, open_game

FIXTURE = "apps/game_generation/games_toml_files/engine_ws_batch3_2026_10_02.toml"


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    return build(FIXTURE, tmp_path_factory.mktemp("switches") / "out")


@pytest.fixture(scope="module")
def html_default(tmp_path_factory):
    """The same fixture with both switches removed: today's behaviour."""
    d = tmp_path_factory.mktemp("switches_default")
    with open(FIXTURE, encoding="utf-8") as fh:
        text = fh.read()
    text = text.replace('wardrobe_change_on_refusal = true\n', '')
    text = text.replace('wardrobe_anywhere          = false\n', '')
    assert "wardrobe_anywhere" not in text.split("[[clothing]]")[0].split("[settings]")[1]
    src = d / "fixture.toml"
    src.write_text(text, encoding="utf-8")
    return build(src, d / "out")


def _at(g, place):
    g.js("() => { SugarCube.State.variables.flags.started = true; }")
    g.play(f"Location_{place}")


def _links(g):
    return g.js("() => [...document.querySelectorAll('.passage a')].map(a => a.textContent.trim())")


@needs_browser
def test_the_refusal_offers_a_change_in_the_wardrobe_room(html):
    with open_game(html) as g:
        _at(g, "loc_home")
        assert g.play("Location_loc_club") == "Location_loc_club"
        assert "Change clothes" in _links(g)          # dressed: nothing shows
        assert g.click("Change clothes") == "WardrobePage"
        assert g.sv("last_game_passage") == "Location_loc_club"
        g.js("() => SugarCube.setup.unequipSlot('top')")  # the bra shows now
        g.click("← Back")
        assert g.passage() == "Location_loc_club"
        assert g.sv("player.current_location") == g.js(
            "() => SugarCube.setup.locations.loc_club.id")
        assert g.errors == []


@needs_browser
def test_away_from_the_wardrobe_neither_page_offers_a_change(html):
    with open_game(html) as g:
        _at(g, "loc_gym")
        g.play("Location_loc_club")
        assert "Change clothes" not in _links(g) and "Go back" in _links(g)
        g.js("() => SugarCube.setup.unequipSlot('top')")
        g.play("Location_loc_office", settle=300)
        assert g.passage() == "ClothingBlock"
        assert "Change clothes" not in _links(g) and "Go back" in _links(g)
        assert g.errors == []


@needs_browser
def test_a_dress_code_offers_a_change_in_the_wardrobe_room(html):
    with open_game(html) as g:
        _at(g, "loc_home")
        g.js("() => SugarCube.setup.unequipSlot('top')")
        g.play("Location_loc_office", settle=300)
        assert g.passage() == "ClothingBlock"
        assert "Change clothes" in _links(g)
        assert g.errors == []


@needs_browser
def test_the_defaults_are_todays_behaviour(html_default):
    with open_game(html_default) as g:
        _at(g, "loc_home")
        g.play("Location_loc_club")
        assert "Change clothes" not in _links(g)       # a refusal offers Go back only
        _at(g, "loc_gym")
        g.js("() => SugarCube.setup.unequipSlot('top')")
        g.play("Location_loc_office", settle=300)
        assert g.passage() == "ClothingBlock"
        assert "Change clothes" in _links(g)            # the loophole, from anywhere
        assert g.js("() => typeof SugarCube.setup.canChangeClothesHere") == "undefined"
        assert g.errors == []


@needs_browser
def test_a_second_wardrobe_room_works_like_the_first(html):
    with open_game(html) as g:
        for room in ("loc_home", "loc_dan"):
            _at(g, room)
            assert "Change Clothes" in _links(g)
            g.play("Location_loc_club")
            assert "Change clothes" in _links(g)
        _at(g, "loc_gym")
        assert "Change Clothes" not in _links(g)
        assert g.errors == []
