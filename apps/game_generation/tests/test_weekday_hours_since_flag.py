"""E4 (World and Systems PRD) — `weekday` and `hours_since_flag` conditions.

A canvas could ask the hour (`time_of_day`) and the days since a flag (`days_since_flag`)
but not the day of the week, and nothing finer than a day since a flag: "only on
Saturday" and "three hours after he texts" were unbuildable as conditions. Two new
condition types, in every evaluator (triggerConditionsSatisfied, describeUnmetConditions,
checkSingleCondition, formatCanvasConditions, getNextActivity, and the quest cards'
checkQuestsCondition in their own flat shape):

    { type = "weekday", weekdays = [5, 6] }                 # 0 = Monday … 6 = Sunday
    { type = "hours_since_flag", subject = "player", flag_key = "met_dan",
      operator = "gte", value = 3 }

`weekday` reuses `setup._weekdayMatches`, the schedule rows' own test. For hours,
applyFlagEffect now stores `set_minute` (day * 1440 + the minute of the day) beside
`set_day`, and the two writers that set a flag directly (the EN1 closed flag, the cheat
restore) stamp the same meta. `$flags_meta` is a top-level variable the backfill does not
reach, so a flag set before E4 has `set_day` only: it reads as set at the start of that
day (`set_day * 1440`). An old save never strands; it opens a wait early, never late.
Proven by loading a save string a pre-change build wrote (tests/data/e4_pre_change_save.txt).

    pytest apps/game_generation/tests/test_weekday_hours_since_flag.py -q
"""
import warnings
from pathlib import Path

import pytest

from apps.projects.services.template_import import (
    CONDITION_SCHEMA,
    _walk_condition_carriers,
    normalize,
    parse_toml,
    validate,
)

from .headless import build, needs_browser, open_game, read_data

FIXTURE = "apps/game_generation/games_toml_files/engine_ws_batch1_2026_10_01.toml"
V2 = Path("apps/game_generation/twee_comprehensive/generators/v2.py").read_text(
    encoding="utf-8"
)


def _fn(name, size=9000):
    return V2.split(name, 1)[1][:size]


def _errors(raw):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return validate(normalize(raw))


def _cond(*items):
    return {"canvases": [{"id": "c", "trigger": {"conditions": {
        "version": "1.0", "items": list(items)}}}]}


# ── 1. the import table ───────────────────────────────────────────────────────


def test_both_types_are_in_the_condition_table():
    assert CONDITION_SCHEMA["weekday"] == (frozenset({"weekdays"}), frozenset())
    keys, ops = CONDITION_SCHEMA["hours_since_flag"]
    assert {"flag_key", "operator", "value", "subject"} <= keys
    assert ops == frozenset({"eq", "ne", "gt", "gte", "lt", "lte"})


@pytest.mark.parametrize(
    "item, fragment",
    [
        ({"type": "weekday", "weekdays": []}, "at least one day"),
        ({"type": "weekday"}, "at least one day"),
        ({"type": "weekday", "weekdays": [7]}, "must be 0-6"),
        ({"type": "weekday", "weekdays": ["sat"]}, "must be int"),
        ({"type": "weekday", "weekdays": [5], "operator": "eq"}, "unknown key `operator`"),
        ({"type": "hours_since_flag", "subject": "player", "flag_key": "f",
          "operator": "is_true", "value": 3}, "unknown operator 'is_true'"),
        ({"type": "hours_since_flag", "flag": "f", "operator": "gte", "value": 3},
         "unknown key `flag`"),
    ],
)
def test_bad_items_are_build_errors(item, fragment):
    errs = _walk_condition_carriers(_cond(item), "")
    assert any(fragment in e for e in errs), errs


def test_good_items_are_clean():
    assert _walk_condition_carriers(_cond(
        {"type": "weekday", "weekdays": [0, 6]},
        {"type": "hours_since_flag", "subject": "player", "flag_key": "f",
         "operator": "lt", "value": 1.5}), "") == []


def test_the_fixture_is_clean():
    assert _errors(parse_toml(FIXTURE)) == []


@pytest.mark.parametrize(
    "goal, fragment",
    [
        ({"hours_since_flag": "met_dan", "op": "is_true", "value": 3, "label": "x"},
         "hours_since_flag condition op must be"),
        ({"hours_since_flag": "met_dan", "op": "gte", "label": "x"}, "requires numeric value"),
        ({"hours_since_flag": "met_dan", "op": "gte", "value": 3}, "must have a `label`"),
        ({"weekday": [9], "label": "x"}, "must be 0-6"),
        ({"weekday": [5]}, "weekday goal item must have a `label`"),
        ({"weekday": [5], "op": "eq", "label": "x"}, "weekday condition takes no op"),
        ({"weekday": [5], "flag": "met_dan", "op": "is_true", "label": "x"}, "ONLY ONE"),
    ],
)
def test_quest_card_shapes_are_validated(goal, fragment):
    raw = parse_toml(FIXTURE)
    raw["quest_cards"][0]["goals"] = [goal]
    errs = _errors(raw)
    assert any(fragment in e for e in errs), errs


def test_quest_card_shapes_reach_the_runtime_json():
    from apps.game_generation.twee_comprehensive.generators.v2 import (
        TweeComprehensiveGeneratorV2,
    )
    from apps.projects.services.game_graph import build_game_graph

    graph = build_game_graph(normalize(parse_toml(FIXTURE)))
    twee = TweeComprehensiveGeneratorV2().generate(graph.project, {}, graph=graph)
    assert '"hours_since_flag": "met_dan"' in twee
    assert '"weekday": [5]' in twee


# ── 2. every evaluator has them ───────────────────────────────────────────────


def test_the_main_evaluator_has_both_branches():
    ev = _fn("setup.triggerConditionsSatisfied = function(conditions)", 16000)
    assert "type === 'weekday'" in ev and "setup._weekdayMatches(" in ev
    assert "type === 'hours_since_flag'" in ev and "setup.hoursSinceFlag(it)" in ev


def test_the_other_readers_have_them():
    assert "it.type === 'weekday'" in _fn("setup.describeUnmetConditions = function")
    single = _fn("setup.checkSingleCondition = function(item)", 800)
    assert "'weekday'" in single and "'hours_since_flag'" in single
    fmt = _fn("setup.formatCanvasConditions = function(conditions)", 12000)
    assert 'item.type === "weekday"' in fmt and 'item.type === "hours_since_flag"' in fmt
    assert "timeConditionsNotMet: true" in _fn("setup.getNextActivity = function(npcId)", 14000)
    quests = _fn("setup.checkQuestsCondition = function(item)", 2500)
    assert "item.hours_since_flag" in quests and "Array.isArray(item.weekday)" in quests


def test_every_flag_writer_stamps_the_minute():
    afe = _fn("window.applyFlagEffect = function", 2500)
    assert afe.count("setup.flagMetaNow()") == 2  # set and toggle
    assert "set_day: currentDay" not in afe
    assert "State.variables.flags_meta[closedFlag] = setup.flagMetaNow();" in V2
    assert "sv.flags_meta[key] = setup.flagMetaNow();" in V2  # the cheat restore


def test_the_fallback_is_the_start_of_the_set_day():
    fn = _fn("setup.flagSetMinute = function(meta)", 400)
    assert "meta.set_minute" in fn and "meta.set_day * 1440" in fn


# ── 3. behaviour, in the real engine ─────────────────────────────────────────


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    return build(FIXTURE, tmp_path_factory.mktemp("e4") / "out")


def _gate(g, cid):
    return g.js("(id) => SugarCube.setup.triggerConditionsSatisfied("
                "SugarCube.setup.getCanvasById(id).conditions)", cid)


def _clock(g, day=None, hour=None, weekday=None):
    g.js("""([d, h, w]) => { const ts = SugarCube.State.variables.game_state.time_state;
            if (d !== null) ts.day = d; if (h !== null) ts.current_hour = h;
            if (w !== null) ts.current_day = w; }""", [day, hour, weekday])


@needs_browser
def test_weekday_opens_on_its_day_only(html):
    with open_game(html) as g:
        assert _gate(g, "sat_only") is False  # Monday
        _clock(g, weekday="Saturday")
        assert _gate(g, "sat_only") is True
        assert g.js("() => SugarCube.setup.formatCanvasConditions("
                    "SugarCube.setup.getCanvasById('sat_only').conditions)") == "Required: Only on Saturday"
        assert g.js("() => SugarCube.setup.describeUnmetConditions("
                    "SugarCube.setup.getCanvasById('sat_only').conditions)") == ""
        _clock(g, weekday="Sunday")
        assert g.js("() => SugarCube.setup.describeUnmetConditions("
                    "SugarCube.setup.getCanvasById('sat_only').conditions)") == "Only on Saturday"
        assert g.errors == []


@needs_browser
def test_hours_since_flag_counts_hours_across_midnight(html):
    with open_game(html) as g:
        assert _gate(g, "after_dan") is False  # flag not set: fails closed
        g.js("() => window.applyFlagEffect('player', null, 'met_dan', 'set')")  # day 1, 18:00
        assert g.sv("flags_meta.met_dan") == {"set_day": 1, "set_minute": 1 * 1440 + 18 * 60}
        _clock(g, hour=20)
        assert _gate(g, "after_dan") is False
        assert g.js("() => SugarCube.setup.formatCanvasConditions("
                    "SugarCube.setup.getCanvasById('after_dan').conditions)") == "Required: Wait 1 more hour"
        _clock(g, hour=21)
        assert _gate(g, "after_dan") is True
        _clock(g, day=2, hour=0)
        assert g.js("() => SugarCube.setup.hoursSinceFlag("
                    "{flag_key: 'met_dan', subject: 'player'})") == 6
        assert g.errors == []


@needs_browser
def test_an_npc_flag_has_its_own_time(html):
    with open_game(html) as g:
        g.js("() => window.applyFlagEffect('npc', 'npc_dan', 'kissed', 'set')")
        _clock(g, hour=23)
        item = {"type": "hours_since_flag", "subject": "npc", "npc_id": "npc_dan",
                "flag_key": "kissed", "operator": "gte", "value": 5}
        assert g.js("(it) => SugarCube.setup.triggerConditionsSatisfied("
                    "{version: '1.0', items: [it]})", item) is True
        assert g.js("(it) => SugarCube.setup.checkSingleCondition(it)", item) is True
        assert g.errors == []


@needs_browser
def test_quest_cards_read_both_gates(html):
    with open_game(html) as g:
        q = "(it) => SugarCube.setup.checkQuestsCondition(it)"
        hours = {"hours_since_flag": "met_dan", "op": "gte", "value": 3}
        assert g.js(q, hours) is False
        g.js("() => window.applyFlagEffect('player', null, 'met_dan', 'set')")
        _clock(g, hour=21)
        assert g.js(q, hours) is True
        assert g.js(q, {"weekday": [5]}) is False
        _clock(g, weekday="Saturday")
        assert g.js(q, {"weekday": [5]}) is True
        assert g.errors == []


@needs_browser
def test_a_save_made_before_e4_reads_its_flags_from_the_start_of_their_day(html):
    """The save string was written by the PRE-change engine: `git archive` of the
    commit before E4 (d2ac5b4), this fixture minus its E4 gates (sat_only, after_dan,
    card_wait; that importer rejects the new types), then played headless: $flags.started
    set, Engine.play Location_loc_home, applyFlagEffect('player', null, 'met_dan', 'set')
    at day 1 18:00, Engine.play Location_loc_home, then Save.serialize(). Its
    $flags_meta.met_dan is {set_day: 1}, with no set_minute."""
    with open_game(html) as g:
        assert g.load_save(read_data("e4_pre_change_save.txt")) is True
        assert g.sv("flags_meta.met_dan") == {"set_day": 1}
        # read as set at 00:00 on day 1, so at 18:00 she is 18 hours on: never stranded
        assert g.js("() => SugarCube.setup.hoursSinceFlag("
                    "{flag_key: 'met_dan', subject: 'player'})") == 18
        assert _gate(g, "after_dan") is True
        # setting it again writes the minute
        g.js("() => window.applyFlagEffect('player', null, 'met_dan', 'set')")
        assert g.sv("flags_meta.met_dan.set_minute") == 1 * 1440 + 18 * 60
        assert _gate(g, "after_dan") is False
        assert g.errors == []
