"""`systems and connections` (World and Systems PRD, Phase 6B, 2026-10-02): a REPORT row under
`--ship` and a `lint · systems and connections` print — the cards, the infrastructure apart, and
each card's feeds / reads. No threshold. Fixtures only.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import gates  # noqa: E402
import test_gates_system_cards as sc  # noqa: E402


def test_cards_infrastructure_and_meters_are_counted_apart():
    st = sc.state_with(sc.card(feeds=["money", "nerve"], reads=["energy"]), sc.METER,
                       infrastructure=[{"name": "the clock", "kind": "clock"},
                                       {"name": "the cast page", "kind": "view"}])
    summary, rows = gates._systems_and_connections(st)
    assert summary == "1 system(s) · 2 infrastructure (clock, view) · 1 meter(s)"
    assert rows == ["shift: feeds 2 (money, nerve) · reads 1 (energy) · leads to 1"]


def test_an_empty_ledger_reports_zero():
    assert gates._systems_and_connections(None)[0].startswith("0 system(s) · 0 infrastructure")


def test_the_row_is_a_report():
    name, ok, head, _ = gates._systems_row(sc.state_with(sc.card()))
    assert name == "systems and connections" and ok is None and "never a score" in head
    assert name not in gates.SHIP_BLOCK_GATES
