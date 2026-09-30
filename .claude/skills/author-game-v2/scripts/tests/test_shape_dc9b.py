"""PRD v2 DC9b · H31: shape.py's "a step's gate can be reached". A step may declare `raises`; the
board may declare `daily_raises`. A gte/gt gate on a trait the ledger raises FAILS when the steps
before it (same person, lower n, plus SP3 dependencies, transitively) cannot reach it."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import shape  # noqa: E402

ROW = "a step's gate can be reached"


def verdict(state):
    for name, ok, head, detail in shape.check(state, False)[0]:
        if name == ROW:
            return ok, detail
    raise AssertionError("row missing")


def step(n, raises=None, gate=None):
    s = {"n": n, "canvas": f"c{n}", "where": "bar", "when": {"days": ["Mon"], "from": "18:00", "to": "20:00"}}
    if raises:
        s["raises"] = raises
    if gate:
        s["gate"] = gate
    return s


def ledger(a_steps, b_steps=None, deps=None, daily=None):
    chars = [{"id": "npc_a", "ladder": {"counter": "a_stage", "steps": a_steps}}]
    if b_steps:
        chars.append({"id": "npc_b", "ladder": {"counter": "b_stage", "steps": b_steps}})
    board = {"characters": chars}
    if daily:
        board["daily_raises"] = daily
    return {"phase": "idea", "board": board, "dependencies": deps or []}


def gate(v, op="gte"):
    return [{"trait": "nerve", "op": op, "value": v}]


def test_earlier_raises_reach_the_gate():
    ok, _ = verdict(ledger([step(1, {"nerve": 5}), step(2, {"nerve": 5}), step(3, gate=gate(10))]))
    assert ok is True


def test_short_of_the_gate_fails():
    ok, detail = verdict(ledger([step(1, {"nerve": 5}), step(2, gate=gate(10))]))
    assert ok is False and "raise nerve by 5" in detail[0]


def test_gt_needs_more_than_equal():
    ok, _ = verdict(ledger([step(1, {"nerve": 10}), step(2, gate=gate(10, "gt"))]))
    assert ok is False


def test_a_daily_raise_makes_it_reachable():
    ok, _ = verdict(ledger([step(1, {"lust": 1}), step(2, gate=gate(50))], daily={"nerve": 2}))
    assert ok is True


def test_a_dependency_counts_its_steps():
    deps = [{"from": {"npc": "npc_b", "step": 1}, "needs": {"npc": "npc_a", "step": 2}}]
    ok, _ = verdict(ledger([step(1, {"nerve": 6}), step(2, {"nerve": 6})],
                           [step(1, gate=gate(12))], deps=deps))
    assert ok is True


def test_a_trait_nothing_in_the_ledger_raises_is_not_judged():
    ok, _ = verdict(ledger([step(1, {"lust": 3}), step(2, gate=[{"trait": "money", "op": "gte", "value": 99}])]))
    assert ok is None


def test_no_raises_anywhere_is_na():
    assert verdict(ledger([step(1), step(2, gate=gate(10))]))[0] is None
