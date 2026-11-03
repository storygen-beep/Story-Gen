"""CK2 (PRD v2, 2026-09-30): the declared door is read from the release page first.

`release_page.door` is read first, `board.door` second (`_declared_door`). Since S12 b
(LO, 2026-11-03) `ends on an opening` no longer reads the door — it reads the quest cards
(test_gates_ws5.py, test_gates_lo_20261103.py) — but `the door can be seen again` and the ladder
check still read a declared door through `_declared_door`, so its precedence is kept here.
Nothing in games/ is read or written.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402

DOOR = {"canvas": "shop", "choice": "Go in the back"}
BROKEN = {"canvas": "nowhere", "choice": "Go in the back"}


def test_a_door_only_on_the_release_page_is_read():
    assert gates._declared_door({"release_page": {"door": dict(DOOR)}}) == DOOR


def test_a_door_only_on_the_board_is_still_read():
    assert gates._declared_door({"board": {"door": dict(DOOR)}}) == DOOR


def test_the_release_page_wins_when_the_two_differ():
    st = {"release_page": {"door": dict(DOOR)}, "board": {"door": dict(BROKEN)}}
    assert gates._declared_door(st) == DOOR


def test_no_door_anywhere_is_none():
    assert gates._declared_door({"board": {}, "release_page": {}}) is None
    assert gates._declared_door(None) is None
