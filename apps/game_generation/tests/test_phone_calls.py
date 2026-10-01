"""E8-calls (World and Systems PRD) — a real call type.

Before this the phone had no calls; the skill said to write the call as the scene a text
books. Now `[[phone.calls]]` with a `type = "calls"` app:

  * a call rings once its `trigger.conditions` hold: a ring badge on the app and the
    sidebar, and a toast — pull delivery, never a covering pop-up;
  * Answer plays the `accept` canvas (not mid-scene; the scene returns her to the
    canvas's own home); Decline applies `on_decline`;
  * left ringing for `ring_minutes` (default 60) it is missed and `on_missed` applies
    once — a missed call counts as ignored;
  * `$game_state.phone.calls[id]` holds it: {state, rang_minute, ended_minute}.

    pytest apps/game_generation/tests/test_phone_calls.py -q
"""
import pytest

from .headless import build, needs_browser, open_game, read_data

FIXTURE = "apps/game_generation/games_toml_files/engine_ws_batch2_2026_10_01.toml"


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    return build(FIXTURE, tmp_path_factory.mktemp("calls") / "out")


def _start(g):
    g.js("() => { SugarCube.State.variables.flags.started = true; }")
    g.play("Location_loc_home")


def _state(g):
    return g.sv("game_state.phone.calls.ben_rings")


def _ben_trust(g):
    ben = g.js("() => SugarCube.setup.resolveNpcId('npc_ben')")
    return g.sv(f"npcs.{ben}.core_traits.trust")


def _calls_screen(g):
    return g.js("() => { SugarCube.setup.openPhone(); SugarCube.setup.openPhoneApp('calls');"
                " return jQuery('.phone-frame').html(); }")


@needs_browser
def test_a_call_rings_with_a_badge_not_a_popup(html):
    with open_game(html) as g:
        assert g.sv("game_state.phone.calls") == {}
        _start(g)
        assert _state(g)["state"] == "ringing"
        ringing = g.js("() => SugarCube.setup.ringingCalls().length")
        assert ringing == 1
        g.js("() => { SugarCube.State.variables.game_state.phone.calls.ben_rings.state = 'declined'; }")
        without = g.js("() => SugarCube.setup.getPhoneUnreadCount()")
        g.js("() => { SugarCube.State.variables.game_state.phone.calls.ben_rings.state = 'ringing'; }")
        assert g.js("() => SugarCube.setup.getPhoneUnreadCount()") == without + 1
        home = g.js("() => { SugarCube.setup.openPhone(); return jQuery('.phone-frame').html(); }")
        calls_icon = home.split('data-app-id="calls"')[1].split("phone-app-label")[0]
        assert 'phone-app-badge">1<' in calls_icon
        assert "Ben is calling" in _calls_screen(g)
        assert g.js("() => jQuery('.phone-match-overlay, .ui-dialog:visible').length") == 0
        assert g.errors == []


@needs_browser
def test_answer_plays_the_scene(html):
    with open_game(html) as g:
        _start(g)
        _calls_screen(g)
        g.js("() => jQuery('.phone-call-answer').first().trigger('click')")
        g.page.wait_for_timeout(200)
        assert g.passage() == "Canvas_ben_call_Node_talk"
        assert _state(g)["state"] == "answered"
        assert "Ben — answered" in _calls_screen(g)
        assert g.errors == []


@needs_browser
def test_mid_scene_the_call_cannot_be_answered(html):
    with open_game(html) as g:
        _start(g)
        g.play("Canvas_pay_desk_Node_desk")
        screen = _calls_screen(g)
        assert "Answer when you are free." in screen and "phone-call-answer" not in screen
        assert g.js("() => SugarCube.setup.answerCall('ben_rings')") is False
        assert _state(g)["state"] == "ringing"
        assert g.errors == []


@needs_browser
def test_decline_applies_its_effects_once(html):
    with open_game(html) as g:
        _start(g)
        _calls_screen(g)
        g.js("() => jQuery('.phone-call-decline').first().trigger('click')")
        assert _state(g)["state"] == "declined"
        assert _ben_trust(g) == -1 and g.sv("flags.declined_ben") is True
        assert g.js("() => SugarCube.setup.declineCall('ben_rings')") is False
        assert _ben_trust(g) == -1
        assert g.errors == []


@needs_browser
def test_a_call_left_ringing_is_missed_once(html):
    with open_game(html) as g:
        _start(g)
        g.js("() => window.waitTime(59)")
        assert _state(g)["state"] == "ringing"
        g.js("() => window.waitTime(1)")  # no passage: the call screen checks the clock
        assert "Ben — missed" in _calls_screen(g)
        assert _state(g)["state"] == "missed"
        assert _ben_trust(g) == -3 and g.sv("flags.missed_ben") is True
        g.play("Location_loc_home")
        assert _ben_trust(g) == -3  # once
        assert g.js("() => SugarCube.setup.answerCall('ben_rings')") is False
        assert g.errors == []


@needs_browser
def test_a_save_made_before_calls_gets_the_call_state_and_rings(html):
    """The save string was written by the PRE-change engine: this fixture as it stood
    before calls existed, built at 54c67d0, then played headless: $flags.started set,
    Engine.play Location_loc_home twice, then Save.serialize(). Its phone state has no
    `calls` map."""
    with open_game(html) as g:
        assert g.load_save(read_data("e8calls_pre_change_save.txt")) is True
        assert g.passage() == "Location_loc_home"
        assert isinstance(g.sv("game_state.phone.calls"), dict)  # backfilled on load
        g.play("Location_loc_home")
        assert _state(g)["state"] == "ringing"  # then delivered
        assert g.errors == []
