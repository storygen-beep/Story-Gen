"""CK4 (PRD v2, 2026-09-30): the past-claim BLOCK judges claims, not markers.

A marker (last night, this week, again, …) counts only when the same clause holds the
player's pronoun for `[settings] narration_person` and a past-tense verb. LO Q1: "again"
alone never fires. The fixture is written here; nothing in games/ is read or written.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402


def game(line, person="second", name="Mara", gated=False):
    block = {"type": "paragraph", "content": line}
    if gated:
        block = {"type": "group", "props": {
            "conditions": {"version": "1.0", "logic": "AND", "items": [
                {"type": "flag", "subject": "player", "flag_key": "came_last_night",
                 "operator": "is_true"}]},
            "blocks": [block]}}
    return {"settings": {"narration_person": person}, "player": {"name": name},
            "canvases": [{"id": "daily", "trigger": {"location": "room", "is_repeatable": True},
                          "nodes": [{"id": "n", "blocks": [block]}]}]}


def hits(line, **kw):
    return gates.lint_past_claim(game(line, **kw))[1]


def test_someone_elses_log_is_not_a_claim():
    assert hits("Delgado reads this week's log aloud.") == []


def test_her_sisters_night_is_not_a_claim():
    assert hits("Her sister moved out the last night in May.") == []


def test_you_did_this_last_night_fires():
    assert hits("You did this last night.") == ["daily [last night]: You did this last night."]


def test_again_alone_never_fires():
    assert hits("He wants you again.") == []


def test_again_inside_a_past_clause_about_her_fires():
    assert hits("You came again.")
    assert hits("He fucked you again.")


def test_first_person():
    assert hits("I slept here last night.", person="first")
    assert hits("He wants me again.", person="first") == []


def test_third_person_uses_her_name_and_she():
    assert hits("Mara went home last night.", person="third")
    assert hits("She went home last night.", person="third")
    assert hits("Delgado went home last night.", person="third") == []


def test_the_pronoun_must_be_in_the_same_clause():
    assert hits("You smile, and Delgado said it last night.") == []


def test_a_gated_line_still_does_not_fire():
    assert hits("You did this last night.", gated=True) == []


def test_the_printed_line_runs_to_160_characters():
    line = "You did this last night " + "and the rest " * 20 + "."
    got = hits(line)[0]
    assert got == "daily [last night]: " + line.strip()[:160]
