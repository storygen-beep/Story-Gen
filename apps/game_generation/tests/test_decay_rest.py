"""EN8 — decay toward a rest point; wait after contact.

PRD_SKILL_TEST_FIXES_v2 §2 EN8 (D5 · Power). Nightly trait decay was one rule: each
night she did not see him, a decaying trait dropped by its amount, down to 0
(`Math.max(0, v - d)`, NPC and player loops alike).

Now:
  * `setup.decayToward(v, rest, d)` moves a trait toward its rest point from EITHER side
    and never crosses it. Deliberate global change (LO A): a value below 0 now rises
    toward 0 instead of snapping to it; positive values behave as before.
  * `[[npcs]] trait_rest = {trait: value}` sets his rest point (default 0).
  * `[[npcs]] decay_after_days = N` — he decays only after N days without contact.
    Contact (a canvas of his firing) records `$npcs[id].last_contact_day`. Old saves lack
    it (rule 8): undefined means "contact today" and starts the wait.
  * E20 decay warnings are two-sided: a value rising out of an lt/lte gate warns too.

Old saves (§0 rule 8): a save the pre-change build wrote has no `last_contact_day`; the
first night records it and does not decay him, and he decays on schedule after.

    pytest apps/game_generation/tests/test_decay_rest.py -q
"""
import warnings

import pytest

from apps.game_generation.twee_comprehensive.generators.v2 import (
    TweeComprehensiveGeneratorV2,
)
from apps.projects.services.game_graph import build_game_graph
from apps.projects.services.template_import import normalize, parse_toml, validate

from .headless import build, needs_browser, open_game, read_data

FIXTURE = "apps/game_generation/games_toml_files/engine_skill_test_fixes_2026_09_30.toml"


def _raw():
    return parse_toml(FIXTURE)


def _npc(raw, nid):
    return next(n for n in raw["npcs"] if n["id"] == nid)


def _validate(raw):
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        errors = validate(normalize(raw))
    return errors, [str(w.message) for w in caught]


# ── 1. the hops and the validator ────────────────────────────────────────────


def test_the_keys_reach_the_npc_and_leave_npcs_clean():
    graph = build_game_graph(normalize(_raw()))
    by = {n.name: n.ai_behavior_config for n in graph.npcs}
    assert by["Vic"]["trait_rest"] == {"trust": 20}
    assert by["Sal"]["decay_after_days"] == 2
    graph = build_game_graph(normalize(_raw()))
    twee = TweeComprehensiveGeneratorV2().generate(graph.project, {}, graph=graph)
    assert 'setup.npc_trait_rest = {"vic": {"trust": 20}};' in twee
    assert 'setup.npc_decay_after_days = {"sal": 2};' in twee
    npcs_line = next(l for l in twee.splitlines() if '"vic": {"name": "Vic"' in l)
    assert "trait_rest" not in npcs_line and "decay_after_days" not in npcs_line


def test_without_the_keys_only_the_step_is_emitted():
    raw = _raw()
    _npc(raw, "vic").pop("trait_rest")
    _npc(raw, "sal").pop("decay_after_days")
    graph = build_game_graph(normalize(raw))
    twee = TweeComprehensiveGeneratorV2().generate(graph.project, {}, graph=graph)
    assert "setup.decayToward = function" in twee  # the global change
    # the loop reads `setup.npc_trait_rest || {}` either way; the data and the wait are absent
    for piece in ("setup.npc_trait_rest =", "setup.npc_decay_after_days", "last_contact_day"):
        assert piece not in twee, piece


def test_the_fixture_is_clean():
    errors, warned = _validate(_raw())
    assert errors == [] and not any("trait_rest" in w or "decay_after_days" in w for w in warned)


@pytest.mark.parametrize(
    "edit, fragment",
    [
        (lambda r: _npc(r, "vic").update(trait_rest=5), "trait_rest must be a table"),
        (lambda r: _npc(r, "vic").update(trait_rest={"trust": "high"}), "trait_rest.trust must be a number"),
        (lambda r: _npc(r, "vic").update(trait_rest={"charm": 5}), "'vic' has no core trait 'charm'"),
        (lambda r: _npc(r, "sal").update(decay_after_days=-1), "decay_after_days must be a whole number"),
        (lambda r: _npc(r, "sal").update(decay_after_days=1.5), "decay_after_days must be a whole number"),
    ],
)
def test_misuse_is_an_error(edit, fragment):
    raw = _raw()
    edit(raw)
    errors, _ = _validate(raw)
    assert any(fragment in e for e in errors), errors


def test_inert_keys_are_warned():
    raw = _raw()
    _npc(raw, "vic")["trait_rest"]["power"] = 10          # power has no trait_decay
    _npc(raw, "tobin")["decay_after_days"] = 3            # tobin has no trait_decay
    _, warned = _validate(raw)
    assert any("trait_rest.power does nothing" in w for w in warned)
    assert any("npcs['tobin'].decay_after_days does nothing" in w for w in warned)


# ── 2. behaviour, in the real engine ─────────────────────────────────────────


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    return build(FIXTURE, tmp_path_factory.mktemp("en8") / "out")


def _nights(g, n):
    for _ in range(n):
        g.js("() => window.advanceDay()")


def _t(g, nid, key):
    return g.sv(f"npcs.{nid}.core_traits.{key}")


def _contact(g, cid="sal_chat"):
    g.js("(c) => SugarCube.setup.markCanvasTriggered(c)", cid)


@needs_browser
def test_decay_toward_unit_cases(html):
    with open_game(html) as g:
        step = "([v, r, d]) => SugarCube.setup.decayToward(v, r, d)"
        seq = []
        v = 30
        for _ in range(4):
            v = g.js(step, [v, 0, 10]); seq.append(v)
        assert seq == [20, 10, 0, 0]
        seq, v = [], -30
        for _ in range(4):
            v = g.js(step, [v, 0, 10]); seq.append(v)
        assert seq == [-20, -10, 0, 0]
        assert g.js(step, [25, 20, 10]) == 20      # never crosses from above
        assert g.js(step, [15, 20, 10]) == 20      # never crosses from below
        assert g.js(step, [5, 0, 10]) == 0 and g.js(step, [-5, 0, 10]) == 0


@needs_browser
def test_vic_settles_at_his_rest_points(html):
    with open_game(html) as g:
        trust, grudge = [], []
        for _ in range(7):
            _nights(g, 1)
            trust.append(_t(g, "vic", "trust")); grudge.append(_t(g, "vic", "grudge"))
        assert trust == [60, 50, 40, 30, 20, 20, 20]
        assert grudge == [-20, -10, 0, 0, 0, 0, 0]
        assert g.errors == []


@needs_browser
def test_sal_waits_two_days_after_contact(html):
    with open_game(html) as g:
        _contact(g)                                           # day 1
        day = g.sv("game_state.time_state.day")
        assert g.sv("npcs.sal.last_contact_day") == day
        seen = []
        for _ in range(4):
            _nights(g, 1)
            seen.append(_t(g, "sal", "trust"))
        # night 1: saw him today (skip); night 2: 1 day apart (< 2); night 3: 2 apart -> decays
        assert seen == [50, 50, 40, 30]
        _contact(g)                                           # seeing him resets the wait
        _nights(g, 2)
        assert _t(g, "sal", "trust") == 30
        _nights(g, 1)
        assert _t(g, "sal", "trust") == 20
        assert g.errors == []


@needs_browser
def test_sal_never_met_starts_the_wait_on_the_first_night(html):
    with open_game(html) as g:
        assert g.sv("npcs.sal.last_contact_day") is None
        _nights(g, 1)
        assert _t(g, "sal", "trust") == 50                   # undefined = contact today
        assert g.sv("npcs.sal.last_contact_day") is not None
        _nights(g, 2)
        assert _t(g, "sal", "trust") == 40


@needs_browser
def test_the_player_rises_toward_zero_too(tmp_path_factory):
    anchor = 'core_traits = { energy = 100, money = 40, corr = 5, stamina = 50 }\n'
    out = tmp_path_factory.mktemp("en8_player")
    text = open(FIXTURE).read()
    assert text.count(anchor) == 1
    text = text.replace(anchor, 'core_traits = { energy = 100, money = 40, corr = -12, stamina = 50 }\n'
                                'trait_decay = { corr = 5 }\n')
    toml = out / "fixture.toml"
    toml.write_text(text)
    with open_game(build(toml, out / "out")) as g:
        seq = []
        for _ in range(4):
            _nights(g, 1)
            seq.append(g.sv("player.core_traits.corr"))
        assert seq == [-7, -2, 0, 0]
        assert g.errors == []


@needs_browser
def test_decay_warnings_are_two_sided(html):
    with open_game(html) as g:
        warn = """(t) => { const v = SugarCube.State.variables;
            v.last_day_snapshot = t.snap; v.npcs.vic.core_traits.grudge = t.now;
            return SugarCube.setup.getDecayWarnings(t.th).map(w => w.text); }"""
        rising = g.js(warn, {"snap": {"npc:vic:grudge": -12}, "now": -11,
                             "th": {"npc:vic:grudge": [{"value": -10, "op": "lte", "subject": "npc",
                                                        "npc_id": "vic", "trait_key": "grudge"}]}})
        assert rising == ["Vic Grudge rising (-11.0 today, was -12.0 yesterday). "
                          "Gate at -10 — interact today or lose it."]
        g.js("() => { SugarCube.State.variables.npcs.vic.core_traits.trust = 21; }")
        dropping = g.js("""(t) => { SugarCube.State.variables.last_day_snapshot = t.snap;
            return SugarCube.setup.getDecayWarnings(t.th).map(w => w.text); }""",
                        {"snap": {"npc:vic:trust": 25},
                         "th": {"npc:vic:trust": [{"value": 22, "subject": "npc", "npc_id": "vic",
                                                   "trait_key": "trust"}]}})
        assert dropping == ["Vic Trust dropping (21.0 today, was 25.0 yesterday). "
                            "Next gate at 22 — interact today or lose more."]
        assert g.errors == []


@needs_browser
def test_a_save_made_before_en8(html):
    """§0 rule 8. Written by the PRE-change engine (the EN7 tree, snapshotted to scratch;
    it ignores trait_rest/decay_after_days): the fixture built with it, Engine.play
    Location_loc_home, Save.serialize(). Sal has no last_contact_day in it."""
    with open_game(html) as g:
        assert g.load_save(read_data("en8_pre_change_save.txt")) is True
        assert g.sv("npcs.sal.last_contact_day") is None
        _nights(g, 1)
        assert _t(g, "sal", "trust") == 50
        _nights(g, 2)
        assert _t(g, "sal", "trust") == 40
        assert _t(g, "vic", "trust") == 40 and _t(g, "vic", "grudge") == 0
        assert g.errors == []
