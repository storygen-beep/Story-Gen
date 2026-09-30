"""NC5 (PRD v2 phase 4 · D8a · D8b · C2, 2026-09-30): the goal chain, in shape.py.

`want.promise` carries no date, and every `want.promise.goals[]` entry with `ends_when` names
`next`. Same batch: a malformed `board.player_start` is bad input in "a step's gate can be
reached", not a silent 0.

Fixtures are written here; nothing in games/ is read or written.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import shape  # noqa: E402
import test_shape_dc9b as dc9b  # noqa: E402

ROW = "the goal chain holds"


def verdict(promise):
    for name, ok, head, detail in shape.check({"phase": "idea", "want": {"promise": promise}}, False)[0]:
        if name == ROW:
            return ok, detail
    raise AssertionError("row missing")


def test_a_chain_of_goals_passes():
    ok, detail = verdict({"goal": "Pay the debt", "goals": [
        {"goal": "Pay the debt", "ends_when": "debt_left hits 0", "next": "Buy the flat"},
        {"goal": "Buy the flat"}]})
    assert ok is True, detail


def test_no_goal_is_na():
    assert verdict({})[0] is None


def test_a_dated_promise_fails():
    ok, detail = verdict({"goal": "Pay the debt", "date": "day 30"})
    assert ok is False and "the goal has no date" in detail[0]


def test_a_dated_goal_fails():
    ok, detail = verdict({"goal": "x", "goals": [{"goal": "Pay", "date": "Friday"}]})
    assert ok is False and '"Pay": has a date' in detail[0]


def test_a_goal_that_ends_with_no_next_fails():
    ok, detail = verdict({"goal": "x", "goals": [{"goal": "Pay the debt", "ends_when": "paid"}]})
    assert ok is False and "names the next one" in detail[0]


# ── player_start bad input ────────────────────────────────────────────────────

def test_a_player_start_that_is_not_a_table_is_bad_input():
    st = dc9b.ledger([dc9b.step(1, {"nerve": 5}), dc9b.step(2, gate=dc9b.gate(5))])
    st["board"]["player_start"] = ["nerve", 20]
    ok, detail = dc9b.verdict(st)
    assert ok is False and any("board.player_start must be a table" in d for d in detail)


def test_a_player_start_value_that_is_not_a_number_is_bad_input():
    st = dc9b.ledger([dc9b.step(1, {"nerve": 5}), dc9b.step(2, gate=dc9b.gate(5))])
    st["board"]["player_start"] = {"nerve": "twenty"}
    ok, detail = dc9b.verdict(st)
    assert ok is False and any("board.player_start.nerve is not a number" in d for d in detail)


def test_a_numeric_string_player_start_is_read():
    st = dc9b.ledger([dc9b.step(1, {"nerve": 5}), dc9b.step(2, gate=dc9b.gate(25))])
    st["board"]["player_start"] = {"nerve": "20"}
    assert dc9b.verdict(st)[0] is True
