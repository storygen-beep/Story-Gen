"""The walk-in floor counts walk-in rules on a door-only canvas a solo activity jumps into (first_term DECISIONS 257:
"Keep watching." on channel 5 goes on to tv_still_watching, where the walk-ins roll). Fixtures only."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402


def test_rules_on_the_canvas_she_keeps_going_into_count_for_the_room():
    tv = {"id": "living_tv", "trigger": {"location": "lr"}, "nodes": [{"id": "adult", "exit_block": {"choices": [
        {"text": "Keep watching.", "targetType": "node", "nodeId": "still_watching.still"}]}}]}
    still = {"id": "still_watching", "trigger": {"location": "lr", "substitution_only": True,
                                                  "substitutions": [{"target_canvas_id": "walkin_a"}, {"target_canvas_id": "walkin_b"}]}}
    elsewhere = {"id": "far", "trigger": {"location": "kitchen", "substitution_only": True, "substitutions": [{"target_canvas_id": "x"}]}}
    game = {"canvases": [tv, still, elsewhere]}
    assert gates._continued_subs(tv, game, "lr") == 2
    tv["nodes"][0]["exit_block"]["choices"][0]["nodeId"] = "far.still"
    assert gates._continued_subs(tv, game, "lr") == 0      # a door-only canvas in another room does not count
