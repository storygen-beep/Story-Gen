"""A choice can use `targetType = "return"` (leftovers L4, 2026-10-02).

The engine resolves a `return` choice on the click: back to the room she was in, or the
canvas's home when none is stored (`engine.md` §13). It is an exit, like a `location`
choice, and its `nodeId` (if one is left on it) is never followed. The readers here that
split exits from decisions and from node-to-node routing used to see only `location` as an
exit, so a `return` was counted as a decision, and one carrying a stray `nodeId` was walked
as a link into the scene.

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
RETURN = {"text": "Head back", "targetType": "return"}


def _with_exit(ch):
    g = ws6.green_game()
    office = next(c for c in g["canvases"] if c["id"] == "office")
    office["nodes"][0]["exit_block"]["choices"].append(copy.deepcopy(ch))
    return g


def _scores(g, state):
    model, game = gates.build(copy.deepcopy(g))
    scored, _ = gates.score(model, game, copy.deepcopy(state))
    return {r["gate"]: (r["pass_"], r["na"], r["headline"]) for r in scored}


def test_a_return_exit_scores_like_a_location_exit():
    st = ws6.green_state()
    assert _scores(_with_exit(RETURN), st) == _scores(_with_exit(LEAVE), st)


def test_a_game_with_a_return_choice_still_ships(tmp_path, monkeypatch):
    b, *_ = ws6.rows(tmp_path, monkeypatch, _with_exit(RETURN))
    assert [n for n, ok in b.items() if ok is False] == []


def test_a_return_choice_that_acts_is_an_unwritten_act():
    ch = dict(RETURN, effects=[{"trait": "money", "op": "add", "value": 5}])
    g = {"canvases": [{"id": "c", "trigger": {"location": "work"}, "nodes": [
        {"id": "n", "exit_block": {"choices": [ch]}}]}]}
    summary, rows = gates.lint_unwritten_act([], g)
    assert len(rows) == 1 and "+5 money" in rows[0]


def test_a_bare_return_is_a_walk_out_and_a_stray_node_id_is_not_followed():
    reply = {"id": "no", "blocks": [{"type": "dialog", "content": "\"Fine. Another time.\""}],
             "exit_block": {"config": {"flagEffects": [{"flag": "said_no_once", "op": "set"}]}}}
    # As a node link this would pass (a written reply that moves something); as `return` the
    # engine never goes there, so it is a bare walk out, like nc3's location WALK.
    ok, _h, detail, _n = nc3.no_row(nc3.step(nc3.YES, dict(RETURN, nodeId="s.no"), reply=reply))
    assert ok is False and detail
    assert nc3.no_row(nc3.step(nc3.YES, RETURN))[0] is False
