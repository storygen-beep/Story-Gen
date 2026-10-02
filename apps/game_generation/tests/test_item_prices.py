"""E10 (World and Systems PRD) — item prices.

`[[items]]` get `price`, `money_trait` (default money) and `conditions` (v1.0, what
gates buying). `setup.buyInventoryItem` buys one when `setup.itemBuyBlock` says nothing
stands in the way: a price, the conditions, enough of the money trait, room in the stack.

    pytest apps/game_generation/tests/test_item_prices.py -q
"""
import pytest

from .headless import build, needs_browser, open_game

FIXTURE = "apps/game_generation/games_toml_files/engine_ws_batch3_2026_10_02.toml"


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    return build(FIXTURE, tmp_path_factory.mktemp("items") / "out")


def _buy(g, item):
    return g.js("(i) => SugarCube.setup.buyInventoryItem(i)", item)


def _block(g, item):
    return g.js("(i) => SugarCube.setup.itemBuyBlock(i)", item)


@needs_browser
def test_a_priced_item_is_bought_with_money_until_the_stack_is_full(html):
    with open_game(html) as g:
        g.play("Location_loc_home")
        assert _buy(g, "coffee") is True and _buy(g, "coffee") is True
        assert g.sv("player.core_traits.money") == 32
        assert g.sv("game_state.inventory.coffee") == 2
        assert _block(g, "coffee") == "You cannot carry more."
        assert _buy(g, "coffee") is False and g.sv("player.core_traits.money") == 32
        assert _block(g, "pebble") == "Not for sale."
        g.js("() => { SugarCube.State.variables.player.core_traits.money = 1; }")
        g.js("() => { SugarCube.State.variables.game_state.inventory = {}; }")
        assert _block(g, "coffee").startswith("Not enough")
        assert g.errors == []


@needs_browser
def test_conditions_gate_buying_and_money_trait_pays(html):
    with open_game(html) as g:
        g.play("Location_loc_home")
        assert _block(g, "pass_card").startswith("Needs")
        assert _buy(g, "pass_card") is False
        g.js("() => { SugarCube.State.variables.flags.card_ok = true; }")
        assert _buy(g, "pass_card") is True
        assert g.sv("player.core_traits.charm") == 7
        assert g.sv("player.core_traits.money") == 40
        assert g.errors == []
