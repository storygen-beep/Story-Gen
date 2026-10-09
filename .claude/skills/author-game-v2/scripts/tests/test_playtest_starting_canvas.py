"""playtest.py enters the starting canvas (B68, skill pass 2026-10-08).

The game's starting canvas is emitted as `StartingCanvas_<id>_Node_<node>`; every other canvas as
`Canvas_<id>_Node_<node>`. `play` and `reach_step` used to build only the second, so an opening
step whose counter moves past the first screen could never be reached. A fake page stands in for
the browser: it answers `Story.has` from a set of passage names.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import playtest  # noqa: E402


class FakePage:
    def __init__(self, names):
        self.names = set(names)

    def evaluate(self, _js, name):
        return name in self.names


def test_an_ordinary_canvas_keeps_its_name():
    page = FakePage({"Canvas_cafe_Node_base"})
    assert playtest.passage_name(page, "cafe", "base") == "Canvas_cafe_Node_base"


def test_the_starting_canvas_is_found_under_its_own_prefix():
    page = FakePage({"StartingCanvas_opening_Node_wake"})
    assert playtest.passage_name(page, "opening", "wake") == "StartingCanvas_opening_Node_wake"


def test_an_unknown_canvas_falls_back_to_the_plain_name():
    assert playtest.passage_name(FakePage(set()), "nope", "base") == "Canvas_nope_Node_base"
