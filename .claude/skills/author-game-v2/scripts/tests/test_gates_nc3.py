"""NC3 (PRD v2 phase 4 · D6, 2026-09-30): a no has content, `the-arc.md` A3.

On a `consume_on = "exit"` step, every exit that doesn't consume it carries
`retry_after_days`, is a labelled `final`, or leads to a node with text and something the no
changes. n/a on a game with no opted-in step.

Fixtures are written here; nothing in games/ is read or written.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402


def step(*choices, reply=None, opt=True):
    t = {"location": "room", "is_repeatable": False}
    if opt:
        t["consume_on"] = "exit"
    nodes = [{"id": "ask", "blocks": [{"type": "paragraph", "content": "He asks."}],
              "exit_block": {"type": "choices", "choices": list(choices)}}]
    if reply is not None:
        nodes.append(reply)
    return {"canvases": [{"id": "s", "trigger": t, "nodes": nodes}]}


YES = {"text": "Go with him", "consumes": True, "targetType": "location", "locationId": "room"}
WALK = {"text": "Walk out", "targetType": "location", "locationId": "room"}


def no_row(g):
    return gates._no_has_content(g)


def test_not_opted_in_is_na():
    assert no_row(step(YES, WALK, opt=False))[0] is None


def test_a_parked_no_passes():
    ok, head, _d, n = no_row(step(YES, {"text": "Not tonight", "retry_after_days": 3,
                                        "targetType": "location", "locationId": "room"}))
    assert ok is True and n == 1, head


def test_a_no_with_a_written_reply_that_moves_something_passes():
    reply = {"id": "no", "blocks": [{"type": "dialog", "content": "\"Fine. Another time.\""}],
             "exit_block": {"config": {"flagEffects": [{"flag": "said_no_once", "op": "set"}]}}}
    ok, _h, _d, _n = no_row(step(YES, {"text": "No.", "targetType": "node", "nodeId": "s.no"},
                                 reply=reply))
    assert ok is True


def test_a_labelled_final_no_passes():
    ok, _h, _d, _n = no_row(step(YES, {"text": "Tell him no (ends his path)", "final": True,
                                       "targetType": "location", "locationId": "room"}))
    assert ok is True


def test_a_bare_walk_out_fails():
    ok, _h, detail, _n = no_row(step(YES, WALK))
    assert ok is False and '"Walk out" (a way out) leaves with nothing' in detail[0]


def test_a_reply_that_changes_nothing_fails():
    reply = {"id": "no", "blocks": [{"type": "paragraph", "content": "He shrugs."}]}
    ok, _h, detail, _n = no_row(step(YES, {"text": "No.", "targetType": "node", "nodeId": "s.no"},
                                     reply=reply))
    assert ok is False and "(a no) changes nothing" in detail[0]


def test_an_unlabelled_final_fails():
    ok, _h, detail, _n = no_row(step(YES, {"text": "No.", "final": True,
                                           "targetType": "location", "locationId": "room"}))
    assert ok is False and "does not say it ends the path" in detail[0]


def test_the_gate_runs_in_the_scoreboard():
    import copy
    g = step(YES, WALK)
    g.update({"project": {"id": "fx", "name": "fx"}, "player": {"core_traits": {}},
              "locations": [{"id": "room"}]})
    model, g2 = gates.build(copy.deepcopy(g))
    r = next(r for r in gates.run_gates(model, g2, None) if r["gate"] == "a no has content")
    assert r["pass_"] is False
