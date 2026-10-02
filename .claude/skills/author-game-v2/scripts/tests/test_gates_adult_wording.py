"""Gate `adult wording` (the-voice.md "Adult wording"): the banned school words.

Whole words or phrases, case-blind, wherever a player reads. A WARN by LO's call: it is a
scored gate, so under --ship it shows inside "every other gate" and never blocks.
n/a policy: a game with no player-facing text has nothing to judge.

Fixtures are written here; nothing in games/ is read or written.
"""
import copy
import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402


def game_with(text, label="Go on", loc_name="The Lounge"):
    return {"project": {"id": "fx", "name": "fx"}, "player": {"core_traits": {}},
            "locations": [{"id": "room", "name": loc_name}],
            "canvases": [{"id": "c", "trigger": {"location": "room"},
                          "nodes": [{"id": "n",
                                     "blocks": [{"type": "paragraph", "content": text}],
                                     "exit_block": {"type": "choices", "choices": [
                                         {"text": label, "targetType": "location",
                                          "target": "room"}]}}]}]}


def row(game):
    model, g2 = gates.build(copy.deepcopy(game))
    return next(r for r in gates.run_gates(model, g2, {}) if r["gate"] == "adult wording")


def test_eighteen_is_not_teen():
    r = row(game_with("She turned eighteen last spring and moved into the dorm."))
    assert r["pass_"] is True, r


def test_a_homeroom_line_warns():
    r = row(game_with("You remember homeroom, and you hated it."))
    assert r["pass_"] is False and not r["na"]
    assert any('"homeroom"' in d for d in r["detail"]), r["detail"]


@pytest.mark.parametrize("text", ["after school", "High School", "a school-uniform", "grade 10",
                                  "the teen", "a teenager", "class president", "junior high"])
def test_every_listed_phrase_warns(text):
    assert row(game_with(f"It was {text}, again."))["pass_"] is False


@pytest.mark.parametrize("text", ["a promise", "grade 8", "a freshman seminar",
                                  "a sophomore", "the high schoolers' café"])
def test_near_misses_and_college_words_pass(text):
    # "high schoolers" is not the phrase "high school" — whole words only.
    assert row(game_with(f"It was {text}, again."))["pass_"] is True


def test_a_choice_label_and_a_room_name_are_read():
    assert row(game_with("Fine.", label="Skip detention"))["pass_"] is False
    assert row(game_with("Fine.", loc_name="Homeroom"))["pass_"] is False


def test_no_player_text_is_na():
    g = {"project": {"id": "fx", "name": "fx"}, "player": {"core_traits": {}},
         "locations": [{"id": "room"}],
         "canvases": [{"id": "c", "trigger": {"location": "room"}, "nodes": [{"id": "n"}]}]}
    assert row(g)["na"] is True


def test_it_is_not_a_ship_block():
    assert "adult wording" not in gates.SHIP_BLOCK_GATES
