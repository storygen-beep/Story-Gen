"""E12 (World and Systems PRD) — a refused room doesn't record a visit.

A dress code (`clothing_rules`) used to redirect from :passagestart, after SugarCube had
already made the refused room's moment and while its body still rendered — so
`current_location` and `visited_locations` named a room she was turned away from. The check
now runs in `Config.navigation.override`, before the moment exists. An `entry_conditions`
refusal already kept its writes inside the guard; it is tested here so it stays that way.

    pytest apps/game_generation/tests/test_refused_room.py -q
"""
import pytest

from .headless import build, needs_browser, open_game

FIXTURE = "apps/game_generation/games_toml_files/engine_ws_batch3_2026_10_02.toml"


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    return build(FIXTURE, tmp_path_factory.mktemp("refused") / "out")


def _id(g, slug):
    return g.js("(s) => String(SugarCube.setup.locations[s].id)", slug)


def _history(g):
    return g.js("() => SugarCube.State.history.map(m => m.title)")


def _start_at_home(g):
    g.js("() => { SugarCube.State.variables.flags.started = true; }")
    g.play("Location_loc_home")


@needs_browser
def test_a_dress_code_refusal_records_nothing(html):
    with open_game(html) as g:
        _start_at_home(g)
        g.js("() => SugarCube.setup.unequipSlot('top')")
        assert g.play("Location_loc_office") == "ClothingBlock"
        assert g.sv("player.current_location") == _id(g, "loc_home")
        assert _id(g, "loc_office") not in g.sv("game_state.visited_locations")
        assert "Location_loc_office" not in _history(g)
        assert g.sv("_clothing_block_destination") == "Location_loc_office"
        g.click("Go back")
        assert g.passage() == "Location_loc_home"
        assert g.errors == []


@needs_browser
def test_an_allowed_room_records_the_visit(html):
    with open_game(html) as g:
        _start_at_home(g)
        assert g.play("Location_loc_office") == "Location_loc_office"
        assert g.sv("player.current_location") == _id(g, "loc_office")
        assert _id(g, "loc_office") in g.sv("game_state.visited_locations")
        assert g.errors == []


@needs_browser
def test_an_entry_conditions_refusal_records_nothing(html):
    with open_game(html) as g:
        _start_at_home(g)
        assert g.play("Location_loc_club") == "Location_loc_club"   # the refusal text
        assert g.sv("player.current_location") == _id(g, "loc_home")
        assert _id(g, "loc_club") not in g.sv("game_state.visited_locations")
        assert g.errors == []
