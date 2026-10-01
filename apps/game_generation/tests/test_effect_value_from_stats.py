"""E5 (World and Systems PRD) — an effect value worked out from her stats.

Before this, every amount the engine paid was a number fixed at build time (or a random
range), so a shift paid the same 70 on day 1 and day 90 while rent climbed. The new
value shape reads a player trait at the moment it applies:

    value = { type = "trait", trait = "charm", mult = 2, add = 50, min = 0, max = 100 }

    = round(charm * mult + add), held inside min / max   (mult 1 and add 0 by default)

One JS resolver, `setup.resolveEffectValue`, serves every path that reads a value at
runtime: the passage emitter (choices, beats, pre-substitution effects) emits a call to
it, and the phone reply / on_ignore, daily-chat topic, daily-tick and fast-job paths,
which used to do `Number(value)`, call it too.

    pytest apps/game_generation/tests/test_effect_value_from_stats.py -q
"""
import pytest

from .headless import build, needs_browser, open_game

FIXTURE = "apps/game_generation/games_toml_files/engine_ws_batch2_2026_10_01.toml"


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    return build(FIXTURE, tmp_path_factory.mktemp("e5") / "out")


def _player(g, trait):
    return g.sv(f"player.core_traits.{trait}")


@needs_browser
def test_the_resolver_on_every_shape(html):
    with open_game(html) as g:
        r = lambda v: g.js("(v) => SugarCube.setup.resolveEffectValue(v)", v)
        assert r(5) == 5
        assert r(-2.5) == -2.5
        assert r(None) == 0
        assert r("7") == 7
        assert r("seven") == 0
        assert r({"type": "curve"}) == 0
        assert r({"type": "random", "min": 4, "max": 4}) == 4
        assert 3 <= r({"type": "random", "min": 3, "max": 5}) <= 5
        # charm = 10
        assert r({"type": "trait", "trait": "charm"}) == 10
        assert r({"type": "trait", "trait": "charm", "mult": 2, "add": 50}) == 70
        assert r({"type": "trait", "trait": "charm", "mult": 2, "add": 50, "max": 60}) == 60
        assert r({"type": "trait", "trait": "charm", "mult": -1, "min": -3}) == -3
        assert r({"type": "trait", "trait": "charm", "mult": 0.25}) == 3  # 2.5 rounds up
        assert r({"type": "trait", "trait": "nobody"}) == 0
        assert g.errors == []


@needs_browser
def test_a_fast_job_pays_from_her_stats_and_says_so(html):
    with open_game(html) as g:
        money = _player(g, "money")
        g.js("() => { SugarCube.setup.openPhone(); SugarCube.setup.openPhoneApp('jobs'); }")
        board = g.js("() => jQuery('.phone-frame').html()")
        assert "$70" in board and "$20" in board
        g.js("() => SugarCube.setup.doFastJob('shift')")
        assert _player(g, "money") == money + 70
        g.js("() => { SugarCube.State.variables.player.core_traits.charm = 30; }")
        g.js("() => SugarCube.setup.doFastJob('flat')")
        assert _player(g, "money") == money + 90
        g.js("() => { SugarCube.State.variables.game_state.fast_jobs.cooldowns = {}; }")
        g.js("() => SugarCube.setup.doFastJob('shift')")
        assert _player(g, "money") == money + 190  # 30 * 2 + 50 = 110, held at max 100
        assert g.errors == []


@needs_browser
def test_a_choice_pays_from_her_stats_through_the_passage(html):
    with open_game(html) as g:
        g.play("Location_loc_bar")
        money = _player(g, "money")
        g.js("() => { SugarCube.State.variables.player.core_traits.charm = 20; }")
        g.play("Canvas_pay_desk_Node_desk")
        g.click("Take the pay")
        assert _player(g, "money") == money + 25
        assert g.errors == []


@needs_browser
def test_the_phone_and_the_day_roll_pay_from_her_stats(html):
    with open_game(html) as g:
        g.js("() => { SugarCube.State.variables.flags.started = true; }")
        g.play("Location_loc_home")
        g.js("() => SugarCube.setup.sendPhoneReply('sal_hello', 0, 1)")
        assert _player(g, "tips") == 5  # charm - 5
        g.js("() => SugarCube.setup.sendDailyChat('npc_sal', 'sal_photo')")
        assert _player(g, "tips") == 10  # + charm * 0.5
        g.js("() => window.advanceDay()")
        assert _player(g, "tips") == 13  # + charm, max 3
        assert g.errors == []
