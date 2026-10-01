"""E7a (World and Systems PRD) — a scene can take clothes off her.

Before this `wardrobeEffects` knew only `add` and `equip`: no scene could take a garment
off her or out of the wardrobe, and an unknown action or a missing item emitted nothing at
all. Now:

  * `unequip` takes a worn garment off (it stays in the wardrobe);
  * `remove` takes it off and out of the wardrobe (`setup.removeFromWardrobe`);
  * all three emitters (a choice, the loop-back link beat, a node exit's config) share
    one helper, so they cannot disagree;
  * the importer rejects an unknown `action` and an `item_id` that is missing or not a
    declared `[[clothing]]` item.

    pytest apps/game_generation/tests/test_wardrobe_effects.py -q
"""
import pytest

from apps.game_generation.twee_comprehensive.generators.v2 import TweeComprehensiveGeneratorV2

from .headless import build, needs_browser, open_game

FIXTURE = "apps/game_generation/games_toml_files/engine_ws_batch3_2026_10_02.toml"


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    return build(FIXTURE, tmp_path_factory.mktemp("wardrobe") / "out")


def _start(g):
    g.js("() => { SugarCube.State.variables.flags.started = true; }")
    g.play("Location_loc_home")
    g.play("Canvas_strip_scene_Node_ask")


def test_one_helper_for_every_action():
    js = TweeComprehensiveGeneratorV2._wardrobe_effect_js
    # add and equip emit exactly what they emitted before the helper existed
    assert js("add", "slip") == 'setup.addToWardrobe("slip");'
    assert js("equip", "slip") == 'setup.addToWardrobe("slip"); setup.equipItem("slip");'
    assert js("unequip", "slip") == 'setup.unequipItem("slip");'
    assert js("remove", "slip") == 'setup.removeFromWardrobe("slip");'
    assert js("grant", "slip") == "" and js("add", "") == ""


@needs_browser
def test_unequip_takes_it_off_and_remove_takes_it_away(html):
    with open_game(html) as g:
        _start(g)
        assert g.sv("player.equipped.top") == "blouse"
        assert g.click("Lose the blouse") == "Canvas_strip_scene_Node_gone"
        assert g.sv("player.equipped.top") is None
        assert "blouse" in g.sv("player.wardrobe")       # unequip keeps it
        assert g.sv("player.equipped.bottom") is None    # the exit removed the skirt
        assert "skirt" not in g.sv("player.wardrobe")
        assert g.sv("player.equipped.bra") == "bra"      # nothing else touched
        assert g.errors == []


@needs_browser
def test_equip_still_works_and_remove_of_an_unowned_garment_is_nothing(html):
    with open_game(html) as g:
        _start(g)
        g.click("Wear the slip")
        assert g.sv("player.equipped.dress") == "slip"
        assert g.sv("player.equipped.top") is None
        assert g.js("() => SugarCube.setup.removeFromWardrobe('skirt')") is False  # already gone
        assert g.js("() => SugarCube.setup.unequipItem('blouse')") is False         # not worn
        assert g.errors == []
