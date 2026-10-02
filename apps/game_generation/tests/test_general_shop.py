"""E10 (World and Systems PRD) — a general shop, `[[shops]]`.

A shop has a location and a stock of priced `[[items]]`; the room's screen shows it as
its own section, one row per item: a Buy link, or the reason she cannot (the item's
conditions, her money, a full stack, "Sold out."). A `limit` on a stock entry is how many
the shop ever sells; its sales live in `$game_state.shops[shop][item]` (backfilled).

    pytest apps/game_generation/tests/test_general_shop.py -q
"""
import pytest

from .headless import build, needs_browser, open_game, read_data

FIXTURE = "apps/game_generation/games_toml_files/engine_ws_batch3_2026_10_02.toml"


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    return build(FIXTURE, tmp_path_factory.mktemp("shop") / "out")


def _shop(g):
    return g.js("() => (jQuery('.passage .general-shop').text() || '')")


def _buy_coffee(g):
    g.js("() => jQuery('.general-shop-buy[data-item=\"coffee\"]').first().trigger('click')")
    g.page.wait_for_timeout(250)


@needs_browser
def test_the_shop_is_its_own_section_in_its_room_only(html):
    with open_game(html) as g:
        g.play("Location_loc_home")
        assert _shop(g) == ""
        g.play("Location_loc_gym")
        text = _shop(g)
        assert "Corner shop" in text and "Coffee" in text and "(3 left)" in text
        assert "Pass card" in text and "Needs" in text          # its conditions, no link
        assert g.js("() => jQuery('.general-shop-buy[data-item=\"pass_card\"]').length") == 0
        assert g.errors == []


@needs_browser
def test_buying_charges_and_counts_down_to_sold_out(html):
    with open_game(html) as g:
        g.play("Location_loc_gym")
        _buy_coffee(g)
        assert g.passage() == "Location_loc_gym"
        assert g.sv("player.core_traits.money") == 36
        assert g.sv("game_state.inventory.coffee") == 1
        assert g.sv("game_state.shops") == {"corner_shop": {"coffee": 1}}
        assert "(2 left)" in _shop(g)
        _buy_coffee(g)
        g.js("() => { SugarCube.State.variables.game_state.inventory = {}; }")  # drink them
        g.play("Location_loc_gym")
        _buy_coffee(g)
        assert g.sv("game_state.shops.corner_shop.coffee") == 3
        assert "Sold out." in _shop(g)
        assert g.js("() => SugarCube.setup.buyFromShop('corner_shop', 'coffee')") is False
        assert g.sv("player.core_traits.money") == 28
        assert g.errors == []


@needs_browser
def test_a_save_made_before_shops_loads_and_buys(html):
    """The save string was written by the PRE-change engine: this fixture without
    `[[shops]]`, built at b6edf38, then played headless: $flags.started set,
    Engine.play Location_loc_home twice, then Save.serialize(). Its $game_state has no
    `shops`."""
    with open_game(html) as g:
        assert g.load_save(read_data("e10b_pre_change_save.txt")) is True
        assert g.passage() == "Location_loc_home"
        assert g.sv("game_state.shops") == {}                  # backfilled on load
        g.play("Location_loc_gym")
        _buy_coffee(g)
        assert g.sv("game_state.shops.corner_shop.coffee") == 1
        assert g.errors == []
