"""E8b (World and Systems PRD) — "back to where she was".

Before this a call's accept canvas and an `anywhere` launcher scene ended at the canvas's
home, so answering a call at the gym moved her to the caller's place and charged that
place's entry costs. Now a location exit may say `destinationType = "return"`:

  * Answer on a call and a launcher option store the room she stands in
    (`$game_state.return_place`, only in a game with a `return` exit);
  * the exit goes back there, with no entry cost (it is not a move);
  * if that room is closed (its hours) or gone (not in this build), or nothing is
    stored, it falls back to the canvas's home, as before;
  * arriving at a room or the map clears the stored place.

    pytest apps/game_generation/tests/test_return_exit.py -q
"""
import pytest

from .headless import build, needs_browser, open_game, read_data

FIXTURE = "apps/game_generation/games_toml_files/engine_ws_batch3_2026_10_02.toml"


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    return build(FIXTURE, tmp_path_factory.mktemp("return") / "out")


def _start_at_gym(g):
    g.js("() => { SugarCube.State.variables.flags.started = true; }")
    g.play("Location_loc_gym")


def _money(g):
    return g.sv("player.core_traits.money")


def _answer(g):
    g.js("() => { SugarCube.setup.openPhone(); SugarCube.setup.openPhoneApp('calls'); }")
    g.js("() => jQuery('.phone-call-answer').first().trigger('click')")
    g.page.wait_for_timeout(200)


def _set_clock(g, hour, minute):
    g.js("([h, m]) => { const ts = SugarCube.State.variables.game_state.time_state;"
         " ts.current_hour = h; ts.current_minute = m; }", [hour, minute])


@needs_browser
def test_a_call_answered_at_the_gym_returns_her_to_the_gym_free(html):
    with open_game(html) as g:
        assert g.sv("game_state.return_place") == ""
        _start_at_gym(g)
        gym = g.sv("player.current_location")
        _answer(g)
        assert g.passage() == "Canvas_dan_call_Node_talk"
        assert g.sv("game_state.return_place") == gym
        assert g.click("Hang up") == "Location_loc_gym"
        assert _money(g) == 40  # Dan's place costs 5; she never went there
        assert g.sv("game_state.return_place") == ""  # cleared on arrival
        assert g.errors == []


@needs_browser
def test_a_closed_room_falls_back_to_the_home_as_before(html):
    with open_game(html) as g:
        _start_at_gym(g)
        _set_clock(g, 18, 55)  # the exit's 10 minutes pass 19:00, when the gym shuts
        _answer(g)
        assert g.click("Hang up") == "Location_loc_dan"
        assert _money(g) == 35  # the home's entry cost applies, as it did before
        assert g.errors == []


@needs_browser
def test_a_gone_room_falls_back_to_the_home(html):
    with open_game(html) as g:
        _start_at_gym(g)
        _answer(g)
        g.js("() => { SugarCube.State.variables.game_state.return_place = 'loc_demolished'; }")
        g.play("Canvas_dan_call_Node_talk")  # re-render: the link resolves at render
        assert g.click("Hang up") == "Location_loc_dan"
        assert g.errors == []


@needs_browser
def test_an_anywhere_launcher_returns_her_too(html):
    with open_game(html) as g:
        _start_at_gym(g)
        g.js("() => { SugarCube.setup.openPhone(); SugarCube.setup.openPhoneApp('taxi');"
             " jQuery('.phone-launch').first().trigger('click'); }")
        g.page.wait_for_timeout(200)
        assert g.passage() == "Canvas_dan_visit_Node_ride"
        assert g.click("Ride back") == "Location_loc_gym"
        assert _money(g) == 40
        assert g.errors == []


@needs_browser
def test_a_scene_entered_from_its_room_ends_at_its_home(html):
    with open_game(html) as g:
        _start_at_gym(g)
        g.play("Location_loc_dan")  # a real move: 5 money
        g.play("Canvas_dan_door_Node_door")
        assert g.sv("game_state.return_place") == ""
        assert g.click("Step back") == "Location_loc_dan"
        assert _money(g) == 35  # re-entering her own room is free
        assert g.errors == []


@needs_browser
def test_a_save_made_before_the_change_loads_and_returns(html):
    """The save string was written by the PRE-change engine: this fixture with its three
    `return` exits as `trigger`, built at 301f6f8, then played headless: $flags.started
    set, Engine.play Location_loc_gym twice, then Save.serialize(). Its $game_state has
    no `return_place`."""
    with open_game(html) as g:
        assert g.load_save(read_data("e8b_pre_change_save.txt")) is True
        assert g.passage() == "Location_loc_gym"
        assert g.sv("game_state.return_place") == ""  # backfilled on load
        _answer(g)
        assert g.click("Hang up") == "Location_loc_gym"
        assert _money(g) == 40
        assert g.errors == []
