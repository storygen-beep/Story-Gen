"""E7c (World and Systems PRD) — saved outfits, behind `[settings] saved_outfits = true`.

  * `$player.outfits[name] = {slot: item id or null}`, at most five;
  * the wardrobe page saves what she wears, lists each outfit with Wear and Delete;
  * Wear puts back each saved garment she still owns (equipItem keeps its conditions)
    and empties the slots the outfit left empty; a garment removed since is skipped;
  * an old save gets `outfits` from the backfill (top level of $player).

    pytest apps/game_generation/tests/test_saved_outfits.py -q
"""
import pytest

from .headless import build, needs_browser, open_game, read_data

FIXTURE = "apps/game_generation/games_toml_files/engine_ws_batch3_2026_10_02.toml"


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    return build(FIXTURE, tmp_path_factory.mktemp("outfits") / "out")


def _wardrobe(g):
    g.js("() => { SugarCube.State.variables.flags.started = true; }")
    g.play("Location_loc_home")
    g.play("WardrobePage")


def _save_as(g, name):
    g.js("(n) => { jQuery('#wardrobe-outfit-name').val(n); jQuery('.wardrobe-outfit-save').trigger('click'); }", name)
    g.page.wait_for_timeout(200)


def _button(g, cls, name):
    g.js("([c, n]) => jQuery('.' + c).filter((i, b) => decodeURIComponent(jQuery(b).data('outfit') + '') === n).trigger('click')",
         [cls, name])
    g.page.wait_for_timeout(200)


@needs_browser
def test_save_wear_and_delete_an_outfit(html):
    with open_game(html) as g:
        _wardrobe(g)
        assert g.sv("player.outfits") == {}
        _save_as(g, "Work <b>")
        work = g.sv("player.outfits")["Work <b>"]
        assert (work["top"], work["bottom"], work["dress"]) == ("blouse", "skirt", None)
        assert "Work &lt;b&gt;" in g.js("() => jQuery('.wardrobe-outfits').html()")
        g.js("() => { SugarCube.setup.unequipSlot('top'); SugarCube.setup.unequipSlot('bra'); }")
        _save_as(g, "Bare")
        _button(g, "wardrobe-outfit-wear", "Work <b>")
        assert g.sv("player.equipped.top") == "blouse" and g.sv("player.equipped.bra") == "bra"
        _button(g, "wardrobe-outfit-wear", "Bare")
        assert g.sv("player.equipped.top") is None and g.sv("player.equipped.bottom") == "skirt"
        _button(g, "wardrobe-outfit-delete", "Bare")
        assert list(g.sv("player.outfits")) == ["Work <b>"]
        assert g.errors == []


@needs_browser
def test_a_removed_garment_is_skipped_and_five_is_the_cap(html):
    with open_game(html) as g:
        _wardrobe(g)
        _save_as(g, "")                                      # unnamed: "Outfit 1"
        assert list(g.sv("player.outfits")) == ["Outfit 1"]
        g.js("() => { SugarCube.setup.removeFromWardrobe('skirt'); }")
        _button(g, "wardrobe-outfit-wear", "Outfit 1")
        assert g.sv("player.equipped.top") == "blouse" and g.sv("player.equipped.bottom") is None
        for n in range(4):
            _save_as(g, f"o{n}")
        assert len(g.sv("player.outfits")) == 5
        assert g.js("() => SugarCube.setup.saveOutfit('sixth')") is False
        assert "Five saved" in g.js("() => jQuery('.wardrobe-outfits').html()")
        assert g.errors == []


@needs_browser
def test_a_save_made_before_outfits_gets_them(html):
    """The save string was written by the PRE-change engine: this fixture without
    `saved_outfits`, built at 24b0793, then played headless: $flags.started set,
    Engine.play Location_loc_home twice, then Save.serialize(). Its $player has no
    `outfits`."""
    with open_game(html) as g:
        assert g.load_save(read_data("e7c_pre_change_save.txt")) is True
        assert g.passage() == "Location_loc_home"
        assert g.sv("player.outfits") == {}                   # backfilled on load
        g.play("WardrobePage")
        _save_as(g, "Mine")
        assert g.sv("player.outfits.Mine.top") == "blouse"
        assert g.errors == []
