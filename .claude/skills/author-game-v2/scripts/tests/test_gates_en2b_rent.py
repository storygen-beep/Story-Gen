"""EN2b (2026-09-30): a staged rent with no `amount` still charges.

The importer lets `[settings.rent]` omit `amount` when `stages` starts at total 0, so
"the obligation is charged" reads the rent from that first stage. Before, it read only
`amount`, and such a game was told its rent charges nothing. Nothing in games/ is read
or written.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from test_gates_ws5 import base_game, econ_state, pay, verdict  # noqa: E402


def rent_game(rent):
    g = base_game()
    g["canvases"] += [pay("shift", 40)]
    g["settings"] = {"rent": {"enabled": True, "due_day": "Friday", **rent}}
    return g


def test_a_staged_rent_without_amount_is_the_charge():
    g = rent_game({"stages": [{"amount": 150, "after_total_paid": 0},
                              {"amount": 200, "after_total_paid": 300}]})
    v, r = verdict(g, econ_state(), "the obligation is charged")
    assert v == "PASS", r


def test_amount_still_wins_when_given():
    g = rent_game({"amount": 100, "stages": [{"amount": 150, "after_total_paid": 100}]})
    v, r = verdict(g, econ_state(), "the obligation is charged")
    assert v == "FAIL" and any("charges 100" in d for d in r["detail"]), r
