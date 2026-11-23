"""How a canvas at a place reaches the player: by itself on arrival, or as a button.

Two engine facts the author-game-lean skill teaches (craft/arc.md, "How a step reaches
her") and that nothing pinned before:

  1. A NON-repeatable canvas at a location fires by itself when she walks in. The
     auto-fire selector takes only non-repeatables; `getStoryCanvasRedirect` calls it on
     entry and marks the winner fired.
  2. A button, in the room's list or in a person's portrait menu, is only ever a
     REPEATABLE canvas. Both selectors skip non-repeatables.

So a step the player chooses from a menu ("Ask about the Help Wanted sign") must be a
repeatable row gated by its own flags, and a one-time canvas is for a step that happens
to her when she arrives. first_term_lean's P21 card was first written the other way and
would have fired Tom's hiring scene on every entry to the café (2026-11-24).

If one of these tests fails, the engine changed how steps reach the player: every game
built on the lean skill's step shapes changes with it. Update craft/arc.md in the same
change, or put the filter back.

    pytest apps/game_generation/tests/test_step_shapes.py -q
"""
import copy

from apps.game_generation.tests.test_canvas_presence_and_active import (
    _canvas,
    _entry,
    _fn_body,
    _raw,
    _twee,
)

SRC = None


def _src():
    global SRC
    if SRC is None:
        SRC = _twee(_raw())
    return SRC


def test_auto_fire_takes_only_non_repeatables():
    body = _fn_body(_src(), "selectAutoFireCanvasForLocation")
    assert "if (c.isRepeatable) continue;" in body


def test_entry_fires_the_auto_fire_pick_and_marks_it():
    body = _fn_body(_src(), "getStoryCanvasRedirect")
    pick = body.index("setup.selectAutoFireCanvasForLocation(locationId)")
    assert pick < body.index("setup.markCanvasTriggered(best.id)")


def test_the_room_list_takes_only_repeatables():
    body = _fn_body(_src(), "selectSoloActivityCanvasesForLocation")
    assert "if (!c.isRepeatable) continue;" in body


def test_a_persons_menu_takes_only_repeatables():
    body = _fn_body(_src(), "selectNpcPortraitCanvasesForLocation")
    assert "if (!c.isRepeatable) continue;" in body


def test_is_repeatable_reaches_the_payload_both_ways():
    d = copy.deepcopy(_raw())
    d.setdefault("canvases", []).extend(
        [
            _canvas("step_once", is_repeatable=False),
            _canvas("step_button", is_repeatable=True),
        ]
    )
    twee = _twee(d)
    assert _entry(twee, "step_once")["isRepeatable"] is False
    assert _entry(twee, "step_button")["isRepeatable"] is True
