"""E3b (World and Systems PRD) — the ignore hook for conversations.

Before this, a text she never answered cost nothing: the thread sat unread with its
buttons up for ever, and the only way to charge for silence was a canvas gated on the
cause flag, `days_since_flag` and a reply flag still false. Opt-in per conversation:

  * `ignore_after_days = N`: if no reply is sent N days after the current instance
    arrived, it closes as ignored: `$game_state.phone.conv_ignored[key]` = the day;
  * `on_ignore = {effects, flagEffects}` applies once, the shapes a reply choice carries.

With a repeatable chat the ignore is per instance, and an ignored instance re-arms the
way an answered one does (its delay counts from the ignore).

    pytest apps/game_generation/tests/test_phone_ignore_hook.py -q
"""
import pytest

from .headless import build, needs_browser, open_game, read_data

FIXTURE = "apps/game_generation/games_toml_files/engine_ws_batch2_2026_10_01.toml"


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    return build(FIXTURE, tmp_path_factory.mktemp("e3b") / "out")


def _start(g):
    g.js("() => { SugarCube.State.variables.flags.started = true; }")
    g.play("Location_loc_home")
    assert g.sv("game_state.phone.triggered_conversations.ana_ask") is not None


def _next_day(g, n=1):
    g.advance_days(n)
    g.play("Location_loc_home")


def _ana_trust(g):
    ana = g.js("() => SugarCube.setup.resolveNpcId('npc_ana')")
    return g.sv(f"npcs.{ana}.core_traits.trust")


def _thread_html(g, npc="npc_ana"):
    return g.js(
        """(npc) => { if (!jQuery('.phone-frame').length) SugarCube.setup.openPhone();
                      SugarCube.setup.openChatThread('messages', npc);
                      return jQuery('.phone-frame').html() || ''; }""",
        npc,
    )


@needs_browser
def test_an_ignored_thread_applies_its_effects_once(html):
    with open_game(html) as g:
        _start(g)
        _next_day(g, 1)
        assert g.sv("game_state.phone.conv_ignored.ana_ask") is None  # 1 day < 2
        assert g.sv("flags.ignored_ana") is not True
        _next_day(g, 1)
        assert g.sv("game_state.phone.conv_ignored.ana_ask") == 3
        assert g.sv("flags.ignored_ana") is True
        for _ in range(4):
            _next_day(g, 1)
        assert g.sv("game_state.phone.conv_ignored.ana_ask") == 3
        # ana_ask's -2 landed exactly once; every other point is one ignored
        # instance of ana_loop (-1 each)
        ignored = g.sv("game_state.phone.conv_ignored")
        loop_ignored = len([k for k in ignored if k.startswith("ana_loop")])
        assert loop_ignored >= 2
        assert _ana_trust(g) == -2 - loop_ignored
        assert g.errors == []


@needs_browser
def test_a_reply_before_day_n_applies_nothing(html):
    with open_game(html) as g:
        _start(g)
        g.js("() => SugarCube.setup.sendPhoneReply('ana_ask', 0, 1)")
        g.js("() => SugarCube.setup.sendPhoneReply('ana_loop', 0, 1)")
        assert _ana_trust(g) == 1
        _next_day(g, 5)
        assert g.sv("game_state.phone.conv_ignored.ana_ask") is None
        assert g.sv("flags.ignored_ana") is not True
        assert "No reply." not in _thread_html(g).split("Coffee tomorrow?")[1].split("You up?")[0]
        assert g.errors == []


@needs_browser
def test_an_ignored_thread_is_closed(html):
    with open_game(html) as g:
        _start(g)
        _next_day(g, 2)
        thread = _thread_html(g)
        assert "No reply." in thread
        assert 'data-conv-id="ana_ask"' not in thread  # no buttons
        # a stale click on the closed instance does nothing
        before = _ana_trust(g)
        g.js("() => SugarCube.setup.sendPhoneReply('ana_ask', 0, 1)")
        assert _ana_trust(g) == before
        assert g.sv("game_state.phone.replies.ana_ask") is None
        assert g.errors == []


@needs_browser
def test_the_ignore_is_per_instance_of_a_repeatable_chat(html):
    with open_game(html) as g:
        _start(g)
        _next_day(g, 1)  # day 2: instance 0 ignored, -1
        assert g.sv("game_state.phone.conv_ignored.ana_loop") == 2
        assert _ana_trust(g) == -1
        _next_day(g, 1)  # day 3: a day after the ignore, instance 1 arrives
        assert g.sv("game_state.phone.conv_cycle.ana_loop") == 1
        g.js("() => SugarCube.setup.sendPhoneReply('ana_loop#1', 0, 1)")
        _next_day(g, 3)  # day 6: instance 1 was answered, so it re-arms unignored
        ignored = g.sv("game_state.phone.conv_ignored")
        assert "ana_loop#1" not in ignored
        assert ignored["ana_loop"] == 2
        assert g.sv("game_state.phone.conv_cycle.ana_loop") == 2
        assert g.errors == []


@needs_browser
def test_a_one_time_chat_without_the_hook_is_unchanged(html):
    with open_game(html) as g:
        _start(g)
        _next_day(g, 10)
        assert "sal_hello" not in g.sv("game_state.phone.conv_ignored")
        assert 'data-conv-id="sal_hello"' in _thread_html(g, "npc_sal")
        assert g.errors == []


@needs_browser
def test_a_save_made_before_e3b_gets_conv_ignored_and_the_hook_fires(html):
    """The save string was written by the PRE-change engine: this fixture built at
    7d7f575 (that engine ignores `ignore_after_days` and `on_ignore`), then played
    headless: $flags.started set, Engine.play Location_loc_home twice (all chats
    delivered on day 1, none answered), then Save.serialize(). Its phone state has
    no conv_ignored."""
    with open_game(html) as g:
        assert g.load_save(read_data("e3b_pre_change_save.txt")) is True
        assert g.passage() == "Location_loc_home"
        assert g.sv("game_state.phone.conv_ignored") == {}  # backfilled
        _next_day(g, 2)
        assert g.sv("game_state.phone.conv_ignored.ana_ask") == 3
        assert g.sv("flags.ignored_ana") is True
        assert g.errors == []
