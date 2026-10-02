"""E13 (World and Systems PRD) — a room she can't afford to enter doesn't record a visit.

The entry-cost check used to redirect to TravelBlock from :passagestart, after SugarCube had
already made the refused room's moment and while its body still rendered — so
`current_location` and `visited_locations` named a room she never paid for, and because the
cost is charged only on a move to a DIFFERENT room, her next try to enter it was free. The
check now runs in `Config.navigation.override`, before the moment exists; the charge itself
stays in :passagestart. The fixture is also a clothing game, so the override here is chained
onto the dress-code one (E12's tests cover that half).

    pytest apps/game_generation/tests/test_unaffordable_room.py -q
"""
import pytest

from .headless import build, needs_browser, open_game

# loc_dan costs 5 money and 20 minutes to enter.
FIXTURE = "apps/game_generation/games_toml_files/engine_ws_batch3_2026_10_02.toml"


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    return build(FIXTURE, tmp_path_factory.mktemp("unaffordable") / "out")


def _id(g, slug):
    return g.js("(s) => String(SugarCube.setup.locations[s].id)", slug)


def _history(g):
    return g.js("() => SugarCube.State.history.map(m => m.title)")


def _minutes(g):
    return g.js(
        "() => { const t = SugarCube.State.variables.game_state.time_state;"
        " return t.day * 1440 + t.current_hour * 60 + t.current_minute; }"
    )


def _start_at_home(g, money):
    g.js("() => { SugarCube.State.variables.flags.started = true; }")
    g.play("Location_loc_home")
    g.js("(m) => { SugarCube.State.variables.player.core_traits.money = m; }", money)


@needs_browser
def test_an_unaffordable_entry_records_nothing(html):
    with open_game(html) as g:
        _start_at_home(g, money=2)
        before = _minutes(g)
        assert g.play("Location_loc_dan") == "TravelBlock"
        assert g.sv("player.current_location") == _id(g, "loc_home")
        assert _id(g, "loc_dan") not in g.sv("game_state.visited_locations")
        assert "Location_loc_dan" not in _history(g)
        assert g.sv("player.core_traits.money") == 2
        assert _minutes(g) == before
        assert g.sv("_travel_block_destination") == "Location_loc_dan"
        g.click("Go back")
        assert g.passage() == "Location_loc_home"
        assert g.errors == []


@needs_browser
def test_a_second_try_is_still_charged(html):
    with open_game(html) as g:
        _start_at_home(g, money=2)
        assert g.play("Location_loc_dan") == "TravelBlock"
        assert g.play("Location_loc_dan") == "TravelBlock"   # still refused, not waved in
        g.click("Go back")
        g.js("() => { SugarCube.State.variables.player.core_traits.money = 40; }")
        before = _minutes(g)
        assert g.play("Location_loc_dan") == "Location_loc_dan"
        assert g.sv("player.core_traits.money") == 35          # the refusal didn't make it free
        assert _minutes(g) == before + 20
        assert g.errors == []


@needs_browser
def test_an_affordable_entry_is_charged_once(html):
    with open_game(html) as g:
        _start_at_home(g, money=40)
        before = _minutes(g)
        assert g.play("Location_loc_dan") == "Location_loc_dan"
        assert g.sv("player.current_location") == _id(g, "loc_dan")
        assert _id(g, "loc_dan") in g.sv("game_state.visited_locations")
        assert g.sv("player.core_traits.money") == 35
        assert _minutes(g) == before + 20
        assert g.play("Location_loc_dan") == "Location_loc_dan"   # re-entry is free
        assert g.sv("player.core_traits.money") == 35
        assert g.errors == []
