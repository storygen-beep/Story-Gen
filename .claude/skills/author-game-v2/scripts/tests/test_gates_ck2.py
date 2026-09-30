"""CK2 (PRD v2, 2026-09-30): "ends on an opening" reads the door from the release page.

`release_page.door` is read first, `board.door` second (`_declared_door`). The fixture
is written here; nothing in games/ is read or written.
"""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402

DOOR = {"canvas": "shop", "choice": "Go in the back"}
BROKEN = {"canvas": "nowhere", "choice": "Go in the back"}


def game():
    """A room with one locked door on a repeatable canvas; `dollars` rises on a
    repeatable elsewhere, so the door can open later."""
    cond = {"version": "1.0", "logic": "AND", "items": [
        {"type": "trait", "subject": "player", "trait_key": "dollars",
         "operator": "gte", "value": 50}]}
    return {
        "project": {"id": "fx", "name": "fx", "starting_canvas": "work"},
        "player": {"core_traits": {"dollars": 0}},
        "locations": [{"id": "street"}],
        "canvases": [
            {"id": "work", "trigger": {"location": "street", "is_repeatable": True},
             "nodes": [{"id": "n", "blocks": [{"type": "paragraph", "content": "You work."}],
                        "exit_block": {"type": "location", "config": {
                            "locationId": "street",
                            "effects": [{"targetType": "player", "trait": "dollars",
                                         "op": "add", "value": 10}]}}}]},
            {"id": "shop", "trigger": {"location": "street", "is_repeatable": True},
             "nodes": [{"id": "n", "blocks": [{"type": "paragraph", "content": "The shop."}],
                        "exit_block": {"type": "choices", "choices": [
                            {"text": "Go in the back", "targetType": "location",
                             "locationId": "street", "show_when_locked": True,
                             "locked_text": "Not yet.", "conditions": cond},
                            {"text": "Leave", "targetType": "location",
                             "locationId": "street"}]}}]},
        ],
    }


def row(state):
    model, g2 = gates.build(copy.deepcopy(game()))
    return next(r for r in gates.run_gates(model, g2, state) if r["gate"] == "ends on an opening")


def test_a_door_only_on_the_release_page_passes():
    r = row({"release_page": {"door": dict(DOOR)}})
    assert r["pass_"] is True, r
    assert "declared door (release_page.door): shop" in r["headline"]


def test_a_door_only_on_the_board_still_passes():
    r = row({"board": {"door": dict(DOOR)}})
    assert r["pass_"] is True, r
    assert "declared door (board.door): shop" in r["headline"]


def test_no_door_anywhere_fails_with_the_new_text():
    r = row({"board": {}, "release_page": {}})
    assert r["pass_"] is False and not r["na"]
    assert r["headline"].startswith("no door declared")
    assert "release_page.door" in r["detail"][0]


def test_the_release_page_wins_when_the_two_differ():
    r = row({"release_page": {"door": dict(DOOR)}, "board": {"door": dict(BROKEN)}})
    assert r["pass_"] is True, r


def test_a_broken_release_page_door_names_its_source():
    r = row({"release_page": {"door": dict(BROKEN)}, "board": {"door": dict(DOOR)}})
    assert r["pass_"] is False
    assert any(d.startswith("release_page.door.canvas 'nowhere'") for d in r["detail"]), r


def test_no_ledger_is_na():
    assert row(None)["na"] is True
