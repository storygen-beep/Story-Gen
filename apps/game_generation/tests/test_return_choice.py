"""E8c (World and Systems PRD) — a choice can use `return` too.

E8b gave a location exit `destinationType = "return"`. A choice now takes
`targetType = "return"`: the same stored place (`$game_state.return_place`, set by a
call's Answer or a launcher option) and the same fallback, the canvas's home, when that
place is closed or gone or nothing is stored.

The fixture is the batch-3 one with its three `return` exits rewritten as one-choice
`choices` exits, so the game carries `return` ONLY on choices — which also proves the
return helpers are emitted for a choice alone.

    pytest apps/game_generation/tests/test_return_choice.py -q
"""
import re

import pytest

from .headless import build, needs_browser, open_game

FIXTURE = "apps/game_generation/games_toml_files/engine_ws_batch3_2026_10_02.toml"
EXIT = re.compile(
    r'exit_block = \{ type = "location", text = "([^"]+)", '
    r'config = \{ destinationType = "return", time_progression_minutes = (\d+) \} \}')


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    d = tmp_path_factory.mktemp("return_choice")
    with open(FIXTURE, encoding="utf-8") as fh:
        text = fh.read()
    text, n = EXIT.subn(
        r'exit_block = { type = "choices", choices = [ { text = "\1", '
        r'targetType = "return", time_progression_minutes = \2 } ] }', text)
    assert n == 3 and 'destinationType = "return"' not in text
    src = d / "fixture.toml"
    src.write_text(text, encoding="utf-8")
    return build(src, d / "out")


def _start_at_gym(g):
    g.js("() => { SugarCube.State.variables.flags.started = true; }")
    g.play("Location_loc_gym")


def _answer(g):
    g.js("() => { SugarCube.setup.openPhone(); SugarCube.setup.openPhoneApp('calls'); }")
    g.js("() => jQuery('.phone-call-answer').first().trigger('click')")
    g.page.wait_for_timeout(200)


@needs_browser
def test_a_return_choice_takes_her_back_free(html):
    with open_game(html) as g:
        assert g.sv("game_state.return_place") == ""   # the default exists for a choice too
        _start_at_gym(g)
        gym = g.sv("player.current_location")
        _answer(g)
        assert g.passage() == "Canvas_dan_call_Node_talk"
        assert g.sv("game_state.return_place") == gym
        assert g.click("Hang up") == "Location_loc_gym"
        assert g.sv("player.core_traits.money") == 40  # Dan's place costs 5; never charged
        assert g.sv("game_state.return_place") == ""
        assert g.errors == []


@needs_browser
def test_a_closed_room_falls_back_to_the_home(html):
    with open_game(html) as g:
        _start_at_gym(g)
        g.js("() => { const ts = SugarCube.State.variables.game_state.time_state;"
             " ts.current_hour = 18; ts.current_minute = 55; }")
        _answer(g)
        g.click("Hang up")  # the choice's 10 minutes pass 19:00, when the gym shuts
        assert g.passage() == "Location_loc_dan"
        assert g.errors == []


@needs_browser
def test_a_gone_room_falls_back_to_the_home(html):
    with open_game(html) as g:
        _start_at_gym(g)
        _answer(g)
        g.js("() => { SugarCube.State.variables.game_state.return_place = 'loc_demolished'; }")
        assert g.click("Hang up") == "Location_loc_dan"
        assert g.errors == []


@needs_browser
def test_nothing_stored_ends_at_the_home(html):
    with open_game(html) as g:
        _start_at_gym(g)
        g.play("Location_loc_dan")
        g.play("Canvas_dan_door_Node_door")
        assert g.click("Step back") == "Location_loc_dan"
        assert g.errors == []
