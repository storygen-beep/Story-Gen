"""IC11: `a scene ends on nothing` and `a person who never speaks` (reported lints)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402


def game(canvases):
    return {"npcs": [{"id": "npc_jo", "name": "Jo"}], "canvases": canvases}


def canvas(cid, rep, nodes, npc="npc_jo"):
    return {"id": cid, "trigger": {"location": "room", "is_repeatable": rep, "npc": npc},
            "nodes": nodes}


SAY = {"type": "dialog", "content": "Hey.", "props": {"speaker": "npc", "npcId": "npc_jo"}}
NARR = {"type": "paragraph", "content": "He looks at you."}
CHOICE = {"type": "choices", "choices": [{"text": "Stay", "targetType": "node", "nodeId": "b"}]}


def test_one_time_scene_with_no_choice_is_listed():
    s, rows = gates.lint_scene_ends_on_nothing(game([canvas("meet", False, [{"id": "a", "blocks": [NARR]}])]))
    assert "1 of 1" in s and rows[0].startswith("meet:")


def test_a_choice_anywhere_clears_it():
    g = game([canvas("meet", False, [{"id": "a", "blocks": [NARR], "exit_block": CHOICE},
                                      {"id": "b", "blocks": [NARR]}])])
    s, rows = gates.lint_scene_ends_on_nothing(g)
    assert "0 of 1" in s and rows == []


def test_repeatable_scenes_are_not_this_lints():
    assert gates.lint_scene_ends_on_nothing(game([canvas("hub", True, [{"id": "a", "blocks": [NARR]}])])) == ("", [])


def test_a_bound_person_who_never_speaks_is_listed():
    s, rows = gates.lint_person_never_speaks(game([canvas("hub", True, [{"id": "a", "blocks": [NARR]}])]))
    assert "1 of 1" in s and rows == ["hub: npc_jo never speaks"]


def test_one_line_from_that_person_clears_it():
    s, rows = gates.lint_person_never_speaks(game([canvas("hub", True, [{"id": "a", "blocks": [NARR, SAY]}])]))
    assert "0 of 1" in s and rows == []


def test_one_time_scenes_belong_to_the_other_lint():
    assert gates.lint_person_never_speaks(game([canvas("meet", False, [{"id": "a", "blocks": [NARR]}])])) == ("", [])
