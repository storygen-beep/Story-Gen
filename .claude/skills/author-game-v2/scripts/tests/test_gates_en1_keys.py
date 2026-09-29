"""EN1 (2026-09-30): `consume_on` and `retry_after_days` are [canvases.trigger] keys.

"no canvas key is discarded" knows every trigger key, so one written a table too high
is told to move down instead of being called a key nothing reads. Nothing in games/ is
read or written.
"""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402


def game(canvas_extra=None, trigger_extra=None):
    step = {"id": "step", "trigger": {"location": "room_a", "is_repeatable": False,
                                      **(trigger_extra or {})},
            "nodes": [{"id": "n", "blocks": [{"type": "paragraph", "content": "He asks."}]}]}
    step.update(canvas_extra or {})
    return {"project": {"id": "fx", "name": "fx"}, "player": {"core_traits": {"money": 10}},
            "locations": [{"id": "room_a"}], "canvases": [step]}


def discarded_row(g):
    model, g2 = gates.build(copy.deepcopy(g))
    results, _ = gates.score(model, g2)
    return next(r for r in results if r["gate"] == "no canvas key is discarded")


def test_the_keys_in_their_table_are_not_flagged():
    r = discarded_row(game(trigger_extra={"consume_on": "exit", "retry_after_days": 2}))
    assert r["pass_"] is True


def test_the_keys_one_table_too_high_are_told_to_move_down():
    r = discarded_row(game(canvas_extra={"consume_on": "exit", "retry_after_days": 2}))
    assert r["pass_"] is False
    text = " ".join(r.get("detail") or [])
    assert "`consume_on`" in text and "move it one level down" in text
    assert "`retry_after_days`" in text
