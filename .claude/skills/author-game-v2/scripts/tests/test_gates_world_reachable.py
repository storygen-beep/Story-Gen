"""Gate 11 · world reachable: the rooms under a second root (2026-10-01).

the-map.md R1 tells an author to build two separate grounds as two roots joined by a travel
canvas, and gate 11 exempts the second root when it is `offscreen` or sealed. The rooms
built off that root are reached the same way, so they are exempt too: a room whose
`entry_from` chain ends at an exempt root. The fixture is written here; nothing in games/
is read or written.
"""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402


def game(town_root):
    """Two roots: `home` (the start) with a bedroom, and `town` with a bar and a back room
    off the bar. `town_root` holds the second root's own keys."""
    return {
        "project": {"id": "fx", "name": "fx", "starting_canvas": "c"},
        "locations": [
            {"id": "home"},
            {"id": "bedroom", "entry_from": "home"},
            {"id": "town", **town_root},
            {"id": "bar", "entry_from": "town"},
            {"id": "back_room", "entry_from": "bar"},
        ],
        "canvases": [{"id": "c", "trigger": {"location": "home"},
                      "nodes": [{"id": "n", "blocks": [{"type": "paragraph", "content": "Here."}]}]}],
    }


def row(g):
    model, g2 = gates.build(copy.deepcopy(g))
    return next(r for r in gates.run_gates(model, g2, None) if r["gate"] == "world reachable")


def test_rooms_under_a_sealed_second_root_are_exempt():
    r = row(game({"auto_exit": False}))
    assert r["pass_"] is True, r["detail"]


def test_rooms_under_an_offscreen_second_root_are_exempt():
    r = row(game({"offscreen": True}))
    assert r["pass_"] is True, r["detail"]


def test_a_second_root_that_is_neither_still_strands_its_rooms():
    r = row(game({}))
    assert r["pass_"] is False and not r["na"]
    assert {d.split()[0] for d in r["detail"]} == {"town", "bar", "back_room"}


def test_a_loop_or_a_missing_parent_exempts_nothing():
    g = game({"auto_exit": False})
    g["locations"] += [{"id": "a", "entry_from": "b"}, {"id": "b", "entry_from": "a"},
                       {"id": "lost", "entry_from": "nowhere"}]
    r = row(g)
    assert r["pass_"] is False and not r["na"]
    assert {d.split()[0] for d in r["detail"]} == {"a", "b", "lost"}
