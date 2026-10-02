"""The goal has no date, and its end is built (the-want.md W10, W11).

  shape.py  `a goal's words name no date` — WARN: a week, day or month in a goal's own text.
  gates.py  `a goal's end is built`      — WARN by type (a scored gate, never a --ship BLOCK):
            each goal with ends_when, except the last, names an ends_flag that some effect sets.
            n/a: no ledger, or no goal but the last can end.
  gates.py  --ship REPORT `a dated line names a built event` — lines naming a future week or day.

None of these block, so none is grandfathered. Fixtures are written here; nothing in games/ is read.
"""
import copy
import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402
import shape  # noqa: E402


def shape_row(goals, goal=None):
    st = {"want": {"promise": {"goal": goal, "goals": goals} if goal else {"goals": goals}}}
    return next((ok, d) for n, ok, h, d in shape.check(st, False)[0] if n == "a goal's words name no date")


# ── shape.py ────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("text", ["pass the week-12 review", "by week 12", "week twelve",
                                  "make rent by day 30", "three months to prove it"])
def test_a_dated_goal_warns(text):
    ok, detail = shape_row([{"goal": text}])
    assert ok == "warn" and detail


def test_an_undated_goal_passes():
    assert shape_row([{"goal": "be kept on"}, {"goal": "the full-time contract"}])[0] is True


def test_the_promise_goal_is_read_too():
    assert shape_row([], goal="the week-12 review")[0] == "warn"


def test_no_goal_is_na():
    assert shape_row([])[0] is None


# ── gates.py: a goal's end is built ─────────────────────────────────────────

def game(flag_set=None):
    eff = {"flagEffects": [{"targetType": "player", "flag": flag_set}]} if flag_set else {}
    return {"project": {"id": "fx", "name": "fx"}, "player": {"core_traits": {}},
            "locations": [{"id": "room"}],
            "canvases": [{"id": "c", "trigger": {"location": "room"},
                          "nodes": [{"id": "n", "blocks": [{"type": "paragraph", "content": "Here."}],
                                     "exit_block": {"type": "choices", "choices": [
                                         dict({"text": "Sign it", "targetType": "location",
                                               "target": "room"}, **eff)]}}]}]}


def end_row(goals, g):
    model, g2 = gates.build(copy.deepcopy(g))
    st = {"want": {"promise": {"goals": goals}}}
    return next(r for r in gates.run_gates(model, g2, st) if r["gate"] == "a goal's end is built")


GOALS = [{"goal": "be kept on", "ends_when": "the review passes", "ends_flag": "review_passed",
          "next": "the contract"},
         {"goal": "the contract", "ends_when": "he signs", "ends_flag": "contract_signed", "next": "…"},
         {"goal": "Ethan's desk", "ends_when": "she has it", "next": "…"}]


def test_an_ends_flag_nobody_sets_warns():
    r = end_row(GOALS, game("review_passed"))
    assert r["pass_"] is False and "contract_signed" in r["detail"][0]


def test_every_end_set_passes_and_the_last_goal_is_exempt():
    g = game("review_passed")
    g["canvases"][0]["nodes"][0]["exit_block"]["choices"][0]["flagEffects"].append(
        {"targetType": "player", "flag": "contract_signed"})
    assert end_row(GOALS, g)["pass_"] is True


def test_ends_when_without_ends_flag_warns():
    goals = [{"goal": "be kept on", "ends_when": "the review passes", "next": "…"}, {"goal": "last"}]
    r = end_row(goals, game())
    assert r["pass_"] is False and "ends_flag is not" in r["detail"][0]


def test_only_the_last_goal_ending_is_na():
    assert end_row([{"goal": "only", "ends_when": "x", "ends_flag": "f"}], game())["na"] is True


def test_it_is_not_a_ship_block():
    assert "a goal's end is built" not in gates.SHIP_BLOCK_GATES


# ── gates.py --ship REPORT: a dated line names a built event ────────────────

def report(text):
    g = game()
    g["canvases"][0]["nodes"][0]["blocks"][0]["content"] = text
    model, g2 = gates.build(copy.deepcopy(g))
    return gates._future_dates_row(model, g2)


def test_a_future_week_is_listed():
    name, ok, head, detail = report("I decide at week twelve.")
    assert ok is False and '"week twelve"' in detail[0]


def test_in_thirty_days_is_listed_and_a_past_duration_is_not():
    assert report("Pay me in thirty days.")[1] is False
    assert report("She hasn't called you in eight months.")[1] is True


def test_no_date_is_ok():
    assert report("Be kept on.")[1] is True
