"""IC12: `lint · the arc ladder` (reported, never scored)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402


def step(cid, reads=None, sets=None, npc="npc_jo", active=True):
    trig = {"location": "room", "is_repeatable": False, "npc": npc}
    if not active:
        trig["is_active"] = False
    if reads:
        trig["conditions"] = {"version": "1.0", "logic": "AND", "items": [
            {"type": "flag", "subject": "player", "flag_key": reads, "operator": "is_true"}]}
    node = {"id": "base", "blocks": [{"type": "paragraph", "content": "A step."}]}
    if sets:
        node["exit_block"] = {"type": "location", "config": {
            "locationId": "room", "flagEffects": [{"targetType": "player", "flag": sets, "op": "set"}]}}
    return {"id": cid, "trigger": trig, "nodes": [node]}


def game(canvases):
    return {"locations": [{"id": "room"}], "npcs": [{"id": "npc_jo", "name": "Jo"}],
            "canvases": canvases}


def test_a_linked_chain_is_counted_end_to_end():
    g = game([step("jo_1", sets="a"), step("jo_2", reads="a", sets="b"), step("jo_3", reads="b")])
    s, rows = gates.lint_arc_ladder(g)
    assert "longest chain 3" in s and "jo_1 → jo_3" in rows[0]


def test_a_broken_link_shortens_the_chain():
    g = game([step("jo_1", sets="a"), step("jo_2", reads="x", sets="b"), step("jo_3", reads="b")])
    assert "longest gated chain 2" in gates.lint_arc_ladder(g)[1][0]


def test_switched_off_steps_are_counted():
    g = game([step("jo_1", sets="a"), step("jo_2", reads="a", active=False)])
    assert "1 switched off" in gates.lint_arc_ladder(g)[1][0]


def test_a_step_named_for_a_person_is_theirs_without_a_binding():
    g = game([step("jo_1", sets="a"), step("arc_jo_02", reads="a", npc=None)])
    assert "2 one-time step(s)" in gates.lint_arc_ladder(g)[1][0]


def test_no_person_no_output():
    assert gates.lint_arc_ladder({"npcs": [], "canvases": []}) == ("", [])
