"""E8 (World and Systems PRD) — the phone reaching outward.

Each part is opt-in and has its own section below:

  * a dating profile's `on_match` ({effects, flagEffects}) applies once, on the first
    match, so a match can lead to a scene (before, `ps.matches` was read by nothing
    but the dating screen); and `match_condition`, which the importer checks as a v1.0
    block itself, is read by the runtime in that shape;
  * an app's `conditions` keep it off the phone while they fail: not on the home grid,
    a stale tap does nothing, and its chats are not counted unread;
  * a `custom` app renders its `passage` inside the phone (before, the importer never
    sent the field and every custom app fell to "Coming Soon"). A canvas id resolves to
    the canvas's entry passage, as a launcher option does;
  * `time_cost` (minutes) on a reply choice, a daily topic, a post action and a fast job
    spends time through advanceTime, so the day can roll; its button says "· Nm";
  * a launcher app with `anywhere = true` offers its options in any room (still never
    mid-scene); without it the room lock stands;
  * a post action's `corruption_min` reads `gate_trait` when set (before, it always read
    corruption).

    pytest apps/game_generation/tests/test_phone_outward.py -q
"""
import pytest

from .headless import build, needs_browser, open_game

FIXTURE = "apps/game_generation/games_toml_files/engine_ws_batch2_2026_10_01.toml"


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    return build(FIXTURE, tmp_path_factory.mktemp("e8") / "out")


def _start(g):
    g.js("() => { SugarCube.State.variables.flags.started = true; }")
    g.play("Location_loc_home")


def _npc_trust(g, slug):
    nid = g.js("(s) => SugarCube.setup.resolveNpcId(s)", slug)
    return g.sv(f"npcs.{nid}.core_traits.trust")


# ── on_match ─────────────────────────────────────────────────────────────────


@needs_browser
def test_a_match_applies_on_match_once(html):
    with open_game(html) as g:
        _start(g)
        g.js("() => { SugarCube.setup.openPhone(); SugarCube.setup.openPhoneApp('dates'); }")
        g.js("() => SugarCube.setup.likeProfile('kai_profile')")
        assert g.sv("game_state.phone.matches.kai_profile") is not None
        assert _npc_trust(g, "npc_kai") == 2
        assert g.sv("flags.matched_kai") is True
        g.js("() => SugarCube.setup.likeProfile('kai_profile')")  # a stale second like
        assert _npc_trust(g, "npc_kai") == 2
        assert g.errors == []


@needs_browser
def test_the_match_condition_is_read_and_a_like_is_not_a_match(html):
    with open_game(html) as g:
        _start(g)
        g.js("() => { SugarCube.setup.openPhone(); SugarCube.setup.openPhoneApp('dates'); }")
        g.js("() => SugarCube.setup.likeProfile('lee_profile')")  # needs charm >= 50
        assert g.sv("game_state.phone.matches.lee_profile") is None
        assert g.sv("game_state.phone.liked_profiles.lee_profile") is True
        assert _npc_trust(g, "npc_lee") == 0
        assert g.errors == []


# ── app conditions ───────────────────────────────────────────────────────────


@needs_browser
def test_an_app_is_on_the_phone_only_while_its_conditions_hold(html):
    with open_game(html) as g:
        _start(g)
        home = lambda: g.js("() => { SugarCube.setup.openPhone(); return jQuery('.phone-frame').html(); }")
        unread = lambda: g.js("() => SugarCube.setup.getPhoneUnreadCount()")
        assert g.sv("game_state.phone.triggered_conversations.kai_secret") is not None
        assert 'data-app-id="secret"' not in home()
        hidden_count = unread()
        g.js("() => SugarCube.setup.openPhoneApp('secret')")  # a stale tap
        assert "Our secret." not in g.js("() => jQuery('.phone-frame').html()")
        g.js("() => { SugarCube.State.variables.flags.has_secret_app = true; }")
        assert 'data-app-id="secret"' in home()
        assert unread() == hidden_count + 1
        g.js("() => SugarCube.setup.openPhoneApp('secret')")
        assert "Kai" in g.js("() => jQuery('.phone-frame').html()")  # the thread list
        assert g.errors == []


# ── the custom app ───────────────────────────────────────────────────────────


@needs_browser
def test_a_custom_app_renders_its_passage(html):
    with open_game(html) as g:
        screen = lambda app: g.js(
            "(a) => { SugarCube.setup.openPhone(); SugarCube.setup.openPhoneApp(a);"
            " return jQuery('#phone-custom-body').text(); }", app)
        assert "The till." in screen("camera")   # a canvas id, resolved at build time
        assert "Paid." in screen("notes")        # a passage name, as written
        assert "Coming Soon" not in g.js("() => jQuery('.phone-frame').text()")
        assert g.js("() => SugarCube.setup.phone_data.apps.filter(a => a.id === 'camera')[0].passage") \
            == "Canvas_pay_desk_Node_desk"
        assert g.errors == []


# ── time_cost ────────────────────────────────────────────────────────────────


def _clock(g):
    ts = g.sv("game_state.time_state")
    return ts["day"], ts["current_hour"], ts.get("current_minute", 0)


def _minutes(g):
    d, h, m = _clock(g)
    return (d * 24 + h) * 60 + m


@needs_browser
def test_each_phone_action_spends_its_time(html):
    with open_game(html) as g:
        _start(g)
        t0 = _minutes(g)
        g.js("() => SugarCube.setup.sendPhoneReply('ana_ask', 0, 1)")       # 20
        assert _minutes(g) == t0 + 20
        g.js("() => SugarCube.setup.sendDailyChat('npc_sal', 'sal_call')")   # 30
        assert _minutes(g) == t0 + 50
        g.js("() => SugarCube.setup.sendSocialPost('feed', 0)")             # 15
        assert _minutes(g) == t0 + 65
        assert g.sv("player.core_traits.followers") == 1
        g.js("() => SugarCube.setup.sendPhoneReply('sal_hello', 0, 1)")     # no time_cost
        assert _minutes(g) == t0 + 65
        assert g.errors == []


@needs_browser
def test_a_long_shift_rolls_the_day(html):
    with open_game(html) as g:
        day, hour, _ = _clock(g)
        assert hour == 18
        tips = g.sv("player.core_traits.tips")
        g.js("() => SugarCube.setup.doFastJob('night_shift')")              # 420 = 7h
        assert _clock(g)[:2] == (day + 1, 1)
        assert g.sv("player.core_traits.tips") == tips + 3  # the daily tick ran
        assert g.errors == []


@needs_browser
def test_a_timed_action_says_so_on_its_button(html):
    with open_game(html) as g:
        _start(g)
        g.js("() => { SugarCube.setup.openPhone(); SugarCube.setup.openPhoneApp('jobs'); }")
        board = g.js("() => jQuery('.phone-frame').text()")
        assert "$1 · 420m" in board
        g.js("() => { SugarCube.setup.openPhone(); SugarCube.setup.openPhoneApp('feed'); }")
        assert "Selfie · 15m" in g.js("() => jQuery('.phone-frame').text()")
        thread = g.js("""() => { SugarCube.setup.openPhone();
                                SugarCube.setup.openChatThread('messages', 'npc_ana');
                                return jQuery('.phone-frame').text(); }""")
        assert "Sure. · 20m" in thread and "Can't. · " not in thread
        assert g.errors == []


# ── the anywhere launcher ────────────────────────────────────────────────────


def _launcher(g, app):
    return g.js("(a) => { SugarCube.setup.openPhone(); SugarCube.setup.openPhoneApp(a);"
                " return jQuery('.phone-launcher').html(); }", app)


@needs_browser
def test_an_anywhere_launcher_plays_from_another_room(html):
    with open_game(html) as g:
        _start(g)  # at loc_home; pay_desk lives at loc_bar
        assert "Not here" in _launcher(g, "door")
        taxi = _launcher(g, "taxi")
        assert "phone-launch" in taxi and "Not here" not in taxi
        g.js("() => jQuery('.phone-launch').first().trigger('click')")
        g.page.wait_for_timeout(200)
        assert g.passage() == "Canvas_pay_desk_Node_desk"
        # mid-scene is still not a place
        assert "Not here" in _launcher(g, "taxi")
        assert g.errors == []


# ── the post action's gate trait ─────────────────────────────────────────────


@needs_browser
def test_a_post_action_gate_reads_its_gate_trait(html):
    with open_game(html) as g:
        _start(g)
        feed = g.js("() => { SugarCube.setup.openPhone(); SugarCube.setup.openPhoneApp('feed');"
                    " return jQuery('.phone-post-composer').html(); }")
        assert 'data-action-idx="1"' in feed      # Tease: charm 10 >= 5
        assert "🔒 Bare" in feed                  # Bare: corruption 0 < 5
        g.js("() => SugarCube.setup.sendSocialPost('feed', 1)")
        assert g.sv("player.core_traits.followers") == 2
        g.js("() => SugarCube.setup.sendSocialPost('feed', 2)")  # a stale tap on the lock
        assert g.sv("player.core_traits.followers") == 2
        assert g.errors == []
