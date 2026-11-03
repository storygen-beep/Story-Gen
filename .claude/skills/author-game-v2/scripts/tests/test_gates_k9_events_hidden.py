"""LO, 2026-11-03: "Hours go only on activities she chooses. Events that happen to her stay hidden."

  `a closed activity says when it opens` — a canvas marked `[canvases.trigger.metadata] kind = "event"`
      is skipped (it needs no hours), and fails if it sets `show_when_blocked` (it lists its hours).

Fixtures are written here; nothing in games/ is read or written.
"""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402

GATE = "a closed activity says when it opens"
SCHED = [{"weekdays": [0, 2, 4], "start_time": "08:30", "end_time": "08:45"}]


def row(game):
    model, g2 = gates.build(copy.deepcopy(game))
    return next(r for r in gates.run_gates(model, g2, {}) if r["gate"] == GATE)


def game(*canvases):
    return {"project": {"id": "fx", "name": "fx"}, "locations": [{"id": "hall"}],
            "canvases": [{"id": cid, "name": cid, "trigger": trig, "nodes": [
                {"id": "n", "blocks": [{"type": "paragraph", "content": "The hall."}],
                 "exit_block": {"choices": [{"text": "Go.", "targetType": "location", "locationId": "hall"}]}}]}
                for cid, trig in canvases]}


def activity(**extra):
    t = {"location": "hall", "is_repeatable": True, "schedules": SCHED,
         "show_when_blocked": True, "cooldown_message": "mornings"}
    t.update(extra)
    return t


def event(**extra):
    t = {"location": "hall", "is_repeatable": True, "schedules": SCHED, "metadata": {"kind": "event"}}
    t.update(extra)
    return t


def test_an_event_with_no_hours_passes():
    r = row(game(("attend", activity()), ("guy_beside_you", event())))
    assert r["pass_"] is True, r


def test_an_event_needs_no_cooldown_line():
    """Without the mark, the same canvas fails for missing hours; with it, it is skipped."""
    bare = {"location": "hall", "is_repeatable": True, "schedules": SCHED}
    assert row(game(("guy_beside_you", bare)))["pass_"] is False
    assert row(game(("attend", activity()), ("guy_beside_you", event())))["pass_"] is True


def test_an_event_that_lists_its_hours_fails():
    r = row(game(("attend", activity()),
                 ("guy_beside_you", event(show_when_blocked=True, cooldown_message="Mon, Wed, Fri"))))
    assert r["pass_"] is False, r
    assert any("guy_beside_you" in d and "event" in d for d in r["detail"]), r["detail"]
