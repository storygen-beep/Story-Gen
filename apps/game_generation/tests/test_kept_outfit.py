"""`remember_outfit` / `restore_outfit` (LO, 2026-11-04): she leaves a scene in what she came in.

One private slot on $player.kept_outfit: not a saved outfit, so no cap and no row on the
wardrobe page. `unless_wearing` keeps a towel out of it. A garment gone since is skipped and
its slot keeps what it holds, so a plain outfit listed before `restore_outfit` is the way out
when nothing was kept.

    pytest apps/game_generation/tests/test_kept_outfit.py -q
"""
import pytest

from apps.game_generation.twee_comprehensive.generators.v2 import TweeComprehensiveGeneratorV2

from .headless import build, needs_browser, open_game

FIXTURE = "apps/game_generation/games_toml_files/engine_ws_batch3_2026_10_02.toml"


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    return build(FIXTURE, tmp_path_factory.mktemp("kept") / "out")


def _start(g):
    g.js("() => { SugarCube.State.variables.flags.started = true; }")
    g.play("Location_loc_home")


def _into_scene(g):
    g.play("Canvas_kept_scene_Node_strip")


def test_the_emitter_needs_no_garment():
    js = TweeComprehensiveGeneratorV2._wardrobe_effect_js
    assert js("remember_outfit", "") == "setup.rememberOutfit([]);"
    assert js("remember_outfit", "", ["towel"]) == 'setup.rememberOutfit(["towel"]);'
    assert js("restore_outfit", "") == "setup.restoreOutfit();"


@needs_browser
def test_she_leaves_in_what_she_came_in(html):
    with open_game(html) as g:
        _start(g)
        before = g.js("() => JSON.stringify(SugarCube.State.variables.player.equipped)")
        assert g.sv("player.equipped.top") == "blouse"
        _into_scene(g)
        g.click("Strip")
        assert g.sv("player.equipped.top") is None and g.sv("player.equipped.bra") is None
        g.click("Get dressed")
        assert g.js("() => JSON.stringify(SugarCube.State.variables.player.equipped)") == before
        assert g.sv("player.kept_outfit") is None    # the slot empties on the way out
        assert g.errors == []


@needs_browser
def test_a_bare_slot_stays_bare(html):
    """No bra in, no bra out, though the way out lists a plain bra first."""
    with open_game(html) as g:
        _start(g)
        g.js("() => SugarCube.setup.unequipItem('bra')")
        _into_scene(g)
        g.click("Strip")
        g.click("Get dressed")
        assert g.sv("player.equipped.bra") is None
        assert g.sv("player.equipped.top") == "blouse"
        assert g.errors == []


@needs_browser
def test_a_dress_comes_back_over_the_plain_outfit(html):
    with open_game(html) as g:
        _start(g)
        g.js("() => { var s = SugarCube.setup; s.addToWardrobe('slip'); s.equipItem('slip'); s.rememberOutfit([]); s.unequipItem('slip'); s.equipItem('blouse'); s.equipItem('skirt'); s.restoreOutfit(); }")
        assert g.sv("player.equipped.dress") == "slip"
        assert g.sv("player.equipped.top") is None and g.sv("player.equipped.bottom") is None
        assert g.errors == []


@needs_browser
def test_a_towel_is_not_remembered(html):
    """She undresses in the towel: the slot keeps what she wore before it."""
    with open_game(html) as g:
        _start(g)
        g.js("() => SugarCube.setup.rememberOutfit([])")   # the blouse, before the shower
        g.js("() => { var s = SugarCube.setup; s.addToWardrobe('slip'); s.equipItem('slip'); }")
        _into_scene(g)
        g.click("Strip")
        g.click("Get dressed")
        assert g.sv("player.equipped.top") == "blouse"
        assert g.sv("player.equipped.dress") is None
        assert g.errors == []


@needs_browser
def test_nothing_kept_leaves_the_plain_outfit_on(html):
    with open_game(html) as g:
        _start(g)
        assert g.js("() => SugarCube.setup.restoreOutfit()") is False
        assert g.sv("player.equipped.top") == "blouse"
        assert g.errors == []


@needs_browser
def test_a_garment_gone_since_keeps_the_plain_one(html):
    """A worn garment taken away between the two: the plain garment stays, she is not bare."""
    with open_game(html) as g:
        _start(g)
        g.js("() => { var s = SugarCube.setup; s.addToWardrobe('slip'); s.equipItem('slip'); s.rememberOutfit([]); s.removeFromWardrobe('slip'); s.equipItem('blouse'); s.equipItem('skirt'); s.restoreOutfit(); }")
        assert g.sv("player.equipped.top") == "blouse"
        assert g.sv("player.equipped.bottom") == "skirt"
        assert g.errors == []


@needs_browser
def test_the_slot_is_private(html):
    with open_game(html) as g:
        _start(g)
        g.js("() => SugarCube.setup.rememberOutfit([])")
        assert g.js("() => Object.keys(SugarCube.State.variables.player.outfits || {}).length") == 0
        assert g.errors == []
