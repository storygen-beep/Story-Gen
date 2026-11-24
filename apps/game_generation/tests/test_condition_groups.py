"""A nested `group` item in a conditions table: different hours on different days on one row.

    { type = "group", logic = "OR", items = [
        { type = "group", logic = "AND", items = [ weekday Mon-Fri, time_of_day 07:00-20:56 ] },
        { type = "group", logic = "AND", items = [ weekday Sat-Sun, time_of_day 10:00-20:56 ] } ] }

The engine evaluates a group's items under its own logic (setup.triggerConditionsSatisfied), and
fails closed: an empty group, or one nested deeper than 3, is false. setup.onlyTheClockShut counts
a group made only of clock items (weekday, time_of_day, ...) as the clock, so a row gated by one
greys out of hours with its cooldown_message instead of hiding. The importer accepts `group` with
`logic` and `items` only, and refuses an empty or over-deep one.

The failure (2026-11-24): first_term_lean's café work had to be live weekdays from 7am and weekends
from 10am. One flat AND/OR list can't say that, so the game needed a row per day kind, and a
weekend menu showed each work button twice: the live weekend row and the greyed weekday twin.

    pytest apps/game_generation/tests/test_condition_groups.py -q
"""
import os

import pytest

from apps.projects.services.template_import import _validate_condition_block_schema

from .headless import build, needs_browser, open_game

GAME = "games/first_term_lean/toml_phases/7_final_game.toml"

WEEK = {"type": "weekday", "weekdays": [0, 1, 2, 3, 4]}
WEEKEND = {"type": "weekday", "weekdays": [5, 6]}


def _tod(start, end):
    return {"type": "time_of_day", "start_time": start, "end_time": end}


CAFE = {
    "type": "group",
    "logic": "OR",
    "items": [
        {"type": "group", "logic": "AND", "items": [WEEK, _tod("07:00", "20:56")]},
        {"type": "group", "logic": "AND", "items": [WEEKEND, _tod("10:00", "20:56")]},
    ],
}
FLAG_ON = {
    "type": "flag",
    "subject": "player",
    "flag_key": "grp_test",
    "operator": "is_true",
}


def _cond(*items, logic="AND"):
    return {"version": "1.0", "logic": logic, "items": list(items)}


# ── the importer ─────────────────────────────────────────────────────────────


def test_a_group_is_accepted():
    assert _validate_condition_block_schema(_cond(FLAG_ON, CAFE), "t") == []


def test_an_empty_group_is_refused():
    errs = _validate_condition_block_schema(_cond({"type": "group", "items": []}), "t")
    assert any("needs items" in e for e in errs), errs


def test_a_group_too_deep_is_refused():
    deep = {"type": "group", "items": [WEEK]}
    for _ in range(3):
        deep = {"type": "group", "items": [deep]}
    errs = _validate_condition_block_schema(_cond(deep), "t")
    assert any("nest at most" in e for e in errs), errs


def test_a_bad_key_or_logic_in_a_group_is_refused():
    errs = _validate_condition_block_schema(
        _cond({"type": "group", "logic": "XOR", "items": [WEEK], "when": 1}), "t"
    )
    assert any("unknown key `when`" in e for e in errs), errs
    assert any("logic must be" in e for e in errs), errs


def test_an_item_inside_a_group_is_still_checked():
    errs = _validate_condition_block_schema(
        _cond({"type": "group", "items": [{"type": "nonsense"}]}), "t"
    )
    assert any("unknown condition type 'nonsense'" in e for e in errs), errs


# ── the engine, in the real game ─────────────────────────────────────────────


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    if not os.path.exists(GAME):
        pytest.skip("first_term_lean not present")
    return build(GAME, tmp_path_factory.mktemp("cond_groups") / "out")


def _at(g, day, hour, minute=0):
    g.js(
        """([d, h, m]) => { const t = SugarCube.State.variables.game_state.time_state;
            t.current_day = d; t.current_hour = h; t.current_minute = m; }""",
        [day, hour, minute],
    )


def _holds(g, cond):
    return g.js("(c) => SugarCube.setup.triggerConditionsSatisfied(c)", cond)


def _clock_only(g, cond):
    return g.js(
        "(c) => SugarCube.setup.onlyTheClockShut({ conditions: c, isActive: true })",
        cond,
    )


@needs_browser
def test_one_row_holds_both_day_kinds(html):
    with open_game(html) as g:
        cases = [
            ("Monday", 8, True),
            ("Monday", 21, False),
            ("Saturday", 9, False),
            ("Saturday", 11, True),
            ("Sunday", 20, True),
        ]
        for day, hour, want in cases:
            _at(g, day, hour)
            assert _holds(g, _cond(CAFE)) is want, (day, hour)
        assert g.errors == []


@needs_browser
def test_a_clock_group_greys_and_a_flag_hides(html):
    with open_game(html) as g:
        _at(g, "Saturday", 9)
        g.js("() => { SugarCube.State.variables.flags.grp_test = true; }")
        assert _clock_only(g, _cond(FLAG_ON, CAFE)) is True
        g.js("() => { SugarCube.State.variables.flags.grp_test = false; }")
        assert _clock_only(g, _cond(FLAG_ON, CAFE)) is False
        assert g.errors == []


@needs_browser
def test_a_group_fails_closed(html):
    with open_game(html) as g:
        _at(g, "Monday", 8)
        assert _holds(g, _cond({"type": "group", "items": []})) is False
        deep = {"type": "group", "items": [WEEK]}
        for _ in range(3):
            deep = {"type": "group", "items": [deep]}
        assert _holds(g, _cond(deep)) is False
        shallow = {"type": "group", "items": [{"type": "group", "items": [WEEK]}]}
        assert _holds(g, _cond(shallow)) is True
        assert g.errors == []


@needs_browser
def test_a_flat_or_still_works(html):
    with open_game(html) as g:
        _at(g, "Saturday", 9)
        assert _holds(g, _cond(WEEK, _tod("08:00", "10:00"), logic="OR")) is True
        assert g.errors == []
