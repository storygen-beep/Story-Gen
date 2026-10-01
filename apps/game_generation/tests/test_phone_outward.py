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
    the canvas's entry passage, as a launcher option does.

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
