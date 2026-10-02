"""E3 (World and Systems PRD) — repeatable chats.

Before this, a phone conversation was delivered once (`triggered_conversations[id]`
was a latch) and its replies were keyed by the conversation id, so the only way to
text "free tonight?" twice was to author a second conversation, and a repeat invite
after sex could not exist. Opt-in per conversation:

  * `repeat_after_days = N`: once the current instance is answered (a reply sent; for a
    chat with no reply block, read) and N days have passed since it arrived or was
    answered, it arrives again while its trigger still holds;
  * `max_repeats = M` caps the re-arrivals.

`$game_state.phone.conv_cycle[id]` is the current instance. Instance 0 keeps the plain
id as its key in `replies` / `read_conversations`, so a one-time chat and a save
written before E3 behave exactly as before; instance n uses "id#n". The thread view
renders past instances as history (their chosen replies, no buttons), so an old
instance never holds up a later one.

    pytest apps/game_generation/tests/test_repeatable_chats.py -q
"""
import pytest

from .headless import build, needs_browser, open_game, read_data

FIXTURE = "apps/game_generation/games_toml_files/engine_ws_batch1_2026_10_01.toml"


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    return build(FIXTURE, tmp_path_factory.mktemp("e3") / "out")


def _start(g):
    """Deliver the chats: `started` holds them all."""
    g.js("() => { SugarCube.State.variables.flags.started = true; }")
    g.play("Location_loc_home")
    assert g.sv("game_state.phone.triggered_conversations.dan_invite") is not None


def _next_day(g, n=1):
    g.advance_days(n)
    g.play("Location_loc_home")


def _reply(g, key, choice=0, rnd=1):
    g.js("([k, c, r]) => SugarCube.setup.sendPhoneReply(k, c, r)", [key, choice, rnd])


def _thread_html(g, npc="npc_dan"):
    return g.js(
        """(npc) => { if (!jQuery('.phone-frame').length) SugarCube.setup.openPhone();
                      SugarCube.setup.openChatThread('messages', npc);
                      return jQuery('.phone-frame').html() || ''; }""",
        npc,
    )


@needs_browser
def test_an_unanswered_chat_does_not_come_back(html):
    with open_game(html) as g:
        _start(g)
        _next_day(g, 5)
        assert g.sv("game_state.phone.conv_cycle.dan_invite") is None
        assert g.errors == []


@needs_browser
def test_an_answered_chat_comes_back_after_its_days(html):
    with open_game(html) as g:
        _start(g)
        _reply(g, "dan_invite", 0)
        _next_day(g, 1)
        assert g.sv("game_state.phone.conv_cycle.dan_invite") is None  # 1 day < 2
        _next_day(g, 1)
        assert g.sv("game_state.phone.conv_cycle.dan_invite") == 1
        assert g.js("() => SugarCube.setup.convCurrentKey('dan_invite')") == "dan_invite#1"
        assert g.js("() => SugarCube.setup.getPhoneUnreadCount()") >= 1
        # the first instance is history; the new one has its own buttons
        thread = _thread_html(g)
        assert thread.count("Free tonight?") == 2
        assert thread.count("Noted.") == 1
        assert 'data-conv-id="dan_invite#1"' in thread
        assert 'data-conv-id="dan_invite"' not in thread
        # answering the new instance is its own reply, with its own effects
        _reply(g, "dan_invite#1", 1)
        assert g.sv("game_state.phone.replies")["dan_invite#1"] == [{"round": 1, "choice": 1}]
        assert g.sv("game_state.phone.replies")["dan_invite"] == [{"round": 1, "choice": 0}]
        thread = _thread_html(g)
        assert thread.count("Noted.") == 2
        assert "phone-reply-btn" not in thread  # both instances answered
        assert g.errors == []


@needs_browser
def test_each_answer_applies_its_effects(html):
    with open_game(html) as g:
        _start(g)
        dan = g.js("() => SugarCube.setup.resolveNpcId('npc_dan')")
        _reply(g, "dan_invite", 0)
        _next_day(g, 2)
        _reply(g, "dan_invite#1", 0)
        assert g.sv(f"npcs.{dan}.core_traits.trust") == 2
        assert g.errors == []


@needs_browser
def test_max_repeats_caps_the_returns(html):
    with open_game(html) as g:
        _start(g)
        for n in range(3):
            _reply(g, g.js("() => SugarCube.setup.convCurrentKey('dan_invite')"), 0)
            _next_day(g, 2)
        assert g.sv("game_state.phone.conv_cycle.dan_invite") == 2  # max_repeats = 2
        assert g.errors == []


@needs_browser
def test_a_chat_with_no_reply_comes_back_once_read(html):
    with open_game(html) as g:
        _start(g)
        _next_day(g, 3)
        assert g.sv("game_state.phone.conv_cycle.dan_note") is None  # unread
        g.js("() => SugarCube.setup.markConversationRead('dan_note')")
        _next_day(g, 1)
        assert g.sv("game_state.phone.conv_cycle.dan_note") == 1
        assert g.errors == []


@needs_browser
def test_the_trigger_still_has_to_hold(html):
    with open_game(html) as g:
        _start(g)
        _reply(g, "dan_invite", 0)
        g.js("() => { SugarCube.State.variables.flags.started = false; }")
        _next_day(g, 3)
        assert g.sv("game_state.phone.conv_cycle.dan_invite") is None
        assert g.errors == []


@needs_browser
def test_a_one_time_chat_is_unchanged(html):
    with open_game(html) as g:
        _start(g)
        _reply(g, "sal_hello", 0)
        _next_day(g, 10)
        assert g.sv("game_state.phone.conv_cycle.sal_hello") is None
        assert g.js("() => SugarCube.setup.convCurrentKey('sal_hello')") == "sal_hello"
        assert _thread_html(g, "npc_sal").count("Hey you.") == 1
        assert g.errors == []


@needs_browser
def test_a_save_made_before_e3_gets_conv_cycle_and_keeps_its_answer(html):
    """The save string was written by the PRE-change engine: `git archive` of the
    commit before E3 (9707f2d), this fixture built with it (that engine ignores
    `repeat_after_days` and `max_repeats`), then played headless: $flags.started set,
    Engine.play Location_loc_home (all three chats delivered on day 1),
    sendPhoneReply('dan_invite', 0, 1), Engine.play Location_loc_home, then
    Save.serialize(). Its phone state has no conv_cycle."""
    with open_game(html) as g:
        assert g.load_save(read_data("e3_pre_change_save.txt")) is True
        assert g.passage() == "Location_loc_home"
        assert g.sv("game_state.phone.conv_cycle") == {}  # backfilled
        assert g.sv("game_state.phone.replies.dan_invite") == [{"round": 1, "choice": 0}]
        _next_day(g, 2)
        assert g.sv("game_state.phone.conv_cycle.dan_invite") == 1
        thread = _thread_html(g)
        assert thread.count("Free tonight?") == 2
        assert 'data-conv-id="dan_invite#1"' in thread
        assert g.errors == []
