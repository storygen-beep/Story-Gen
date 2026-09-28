"""G34b `every hub is met first`: group meetings and the forced opening count as met (LO, 2026-09-28)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402


def say(npc):
    return {"type": "dialog", "content": "Hey.", "props": {"speaker": "npc", "npcId": npc}}


NARR = {"type": "paragraph", "content": "The room is quiet."}


def sets(flag, loc="room"):
    return {"type": "location",
            "config": {"locationId": loc,
                       "flagEffects": [{"targetType": "player", "flag": flag, "op": "set"}]}}


def to(loc="room"):
    return {"type": "location", "config": {"locationId": loc}}


def hub(cid, npc, flag=None):
    t = {"location": "room", "is_repeatable": True, "npc": npc}
    if flag:
        t["conditions"] = {"version": "1.0", "logic": "AND", "items": [
            {"type": "flag", "subject": "player", "flag_key": flag, "operator": "is_true"}]}
    return {"id": cid, "trigger": t, "nodes": [{"id": "base", "blocks": [say(npc)]}]}


def scene(cid, nodes):
    return {"id": cid, "trigger": {"location": "room", "is_repeatable": False}, "nodes": nodes}


def game(canvases, start=None):
    g = {"canvases": canvases, "project": {}}
    if start:
        g["project"]["starting_canvas"] = start
    return g


def test_a_group_scene_on_one_flag_meets_everyone_it_names():
    g = game([scene("meet_crew", [{"id": "a", "blocks": [say("npc_a"), say("npc_b")],
                                   "exit_block": sets("met_crew")}]),
              hub("hub_a", "npc_a", "met_crew"), hub("hub_b", "npc_b", "met_crew")])
    met, cast, _owners, cold = gates._fh_cast_met(g)
    assert met == ["npc_a", "npc_b"] and cast == ["npc_a", "npc_b"] and cold == []


def test_a_flag_set_by_a_scene_that_names_nobody_meets_nobody():
    g = game([scene("arrive", [{"id": "a", "blocks": [NARR], "exit_block": sets("doors_open")}]),
              hub("hub_a", "npc_a", "doors_open"), hub("hub_b", "npc_b", "doors_open")])
    met, cast, _owners, _cold = gates._fh_cast_met(g)
    assert met == [] and cast == ["npc_a", "npc_b"]


def test_a_group_flag_does_not_meet_someone_the_scene_leaves_out():
    g = game([scene("meet_crew", [{"id": "a", "blocks": [say("npc_a")], "exit_block": sets("met_crew")}]),
              hub("hub_a", "npc_a", "met_crew"), hub("hub_b", "npc_b", "met_crew")])
    met, _cast, _owners, _cold = gates._fh_cast_met(g)
    assert met == ["npc_a"]


def test_a_line_on_the_forced_opening_meets_them_and_their_hub_needs_no_gate():
    g = game([scene("opening", [{"id": "a", "blocks": [say("npc_c")], "exit_block": to()}]),
              hub("hub_c", "npc_c")], start="opening")
    met, _cast, _owners, cold = gates._fh_cast_met(g)
    assert met == ["npc_c"] and cold == []


def test_a_line_on_a_branch_of_the_opening_is_not_forced():
    opening = scene("opening", [
        {"id": "a", "blocks": [NARR],
         "exit_block": {"type": "choices", "choices": [
             {"text": "Go in", "targetType": "node", "nodeId": "b"},
             {"text": "Leave", "targetType": "location", "locationId": "room"}]}},
        {"id": "b", "blocks": [say("npc_c")], "exit_block": to()}])
    met, _cast, _owners, cold = gates._fh_cast_met(game([opening, hub("hub_c", "npc_c")], start="opening"))
    assert met == [] and cold == [("npc_c", ["hub_c"])]


def test_an_ungated_hub_for_someone_the_opening_never_names_is_still_cold():
    g = game([scene("opening", [{"id": "a", "blocks": [say("npc_c")], "exit_block": to()}]),
              hub("hub_d", "npc_d")], start="opening")
    met, _cast, _owners, cold = gates._fh_cast_met(g)
    assert met == [] and cold == [("npc_d", ["hub_d"])]
