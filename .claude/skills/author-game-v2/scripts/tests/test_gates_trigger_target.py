"""A `trigger` choice, or one with no `targetType`, is an exit (leftovers L8, 2026-10-02).

The engine sends a `trigger` choice to the canvas's home, as it does a `return` one, and an
omitted `targetType` is `trigger` (the importer's default, and the engine's). Only a `node`
choice stays inside the canvas, and only its `nodeId` is followed. Several readers here
defaulted a missing `targetType` to `node`, and the L4 readers saw `trigger` as a decision, so
a bare `trigger` was counted on the menu and one carrying a stray `nodeId` was walked as a
link into the scene.

Fixtures are written here; nothing in games/ is read or written.
"""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import gates  # noqa: E402
import test_gates_nc3 as nc3  # noqa: E402
import test_gates_ws6 as ws6  # noqa: E402

LEAVE = {"text": "Head back", "targetType": "location", "locationId": "work"}
TRIGGER = {"text": "Head back", "targetType": "trigger"}
UNTYPED = {"text": "Head back"}


def _with_exit(ch):
    g = ws6.green_game()
    office = next(c for c in g["canvases"] if c["id"] == "office")
    office["nodes"][0]["exit_block"]["choices"].append(copy.deepcopy(ch))
    return g


def _scores(g, state):
    model, game = gates.build(copy.deepcopy(g))
    scored, _ = gates.score(model, game, copy.deepcopy(state))
    return {r["gate"]: (r["pass_"], r["na"], r["headline"]) for r in scored}


def test_a_trigger_or_untyped_exit_scores_like_a_location_exit():
    st = ws6.green_state()
    want = _scores(_with_exit(LEAVE), st)
    assert _scores(_with_exit(TRIGGER), st) == want
    assert _scores(_with_exit(UNTYPED), st) == want


def test_a_game_with_a_trigger_choice_still_ships(tmp_path, monkeypatch):
    b, *_ = ws6.rows(tmp_path, monkeypatch, _with_exit(TRIGGER))
    assert [n for n, ok in b.items() if ok is False] == []


def test_a_trigger_or_untyped_choice_that_acts_is_an_unwritten_act():
    for exit_choice in (TRIGGER, UNTYPED):
        ch = dict(exit_choice, effects=[{"trait": "money", "op": "add", "value": 5}])
        g = {"canvases": [{"id": "c", "trigger": {"location": "work"}, "nodes": [
            {"id": "n", "exit_block": {"choices": [ch]}}]}]}
        summary, rows = gates.lint_unwritten_act([], g)
        assert len(rows) == 1 and "+5 money" in rows[0]


def test_a_stray_node_id_on_a_trigger_or_untyped_choice_is_not_followed():
    reply = {"id": "no", "blocks": [{"type": "dialog", "content": "\"Fine. Another time.\""}],
             "exit_block": {"config": {"flagEffects": [{"flag": "said_no_once", "op": "set"}]}}}
    # As a node link this passes (a written reply that moves something); the engine never
    # goes there from a trigger choice, so it is a bare walk out, like nc3's location WALK.
    for exit_choice in (TRIGGER, UNTYPED):
        ok, _h, detail, _n = nc3.no_row(
            nc3.step(nc3.YES, dict(exit_choice, nodeId="s.no"), reply=reply))
        assert ok is False and detail
