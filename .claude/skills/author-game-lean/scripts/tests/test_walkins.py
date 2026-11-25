"""walkins.py: check.py's `walkins` check, the scenes that come to her (craft/walk-ins.md). Planted dict games;
nothing in games/ is read. LO, typed in main-lean 2026-11-26: "Yes", "One is fine for now"."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import check  # noqa: E402
import walkins  # noqa: E402

BRAKE = {"type": "flag", "subject": "player", "flag_key": "came_to_her_today", "operator": "is_false"}


def comes(cid="park_tom", who="npc_tom", place="park", conds=(BRAKE,), choices=None):
    choices = choices if choices is not None else [
        {"text": "Stop and talk", "flagEffects": [{"flag": "came_to_her_today", "op": "set"}]},
        {"text": "Keep walking", "flagEffects": [{"flag": "came_to_her_today", "op": "set"}]}]
    trigger = {"location": place, "trigger_mode": "random", "chance": 0.3,
               "conditions": {"version": "1.0", "logic": "AND", "items": list(conds)}}
    if who:
        trigger["requires_npc"] = who
    return {"id": cid, "trigger": trigger, "nodes": [{"id": "a", "exit_block": {"choices": choices}}]}


def planted(*canvases, tick=("came_to_her_today",)):
    return {"canvases": list(canvases),
            "npcs": [{"id": "npc_tom", "schedules": [{"location": "park"}]},
                     {"id": "npc_ann", "schedules": [{"location": "cafe"}]},
                     {"id": "npc_bro", "schedules": [{"location": "bro_room"}]}],
            "locations": [{"id": "home"}, {"id": "her_room", "parent": "home"}, {"id": "bro_room", "parent": "home"},
                          {"id": "hall", "parent": "home"}, {"id": "park"}, {"id": "cafe"}],
            "engine": {"daily_tick": {"flagEffects": [{"targetType": "player", "flag": f, "op": "unset"}
                                                      for f in tick]}}}


def test_a_scene_that_comes_to_her_by_the_rules_is_green():
    assert walkins.problems(planted(comes(), comes("cafe_ann", "npc_ann", "cafe"))) == []


def test_a_button_is_not_checked():
    manual = comes(who=None, conds=())
    manual["trigger"]["trigger_mode"] = "manual"
    assert walkins.problems(planted(manual)) == []


def test_it_names_a_person_whose_rows_reach_the_place():
    assert any("with no person" in r for r in walkins.problems(planted(comes(who=None))))
    assert any("no schedule row at `park`" in r for r in walkins.problems(planted(comes(who="npc_ann"))))


def test_the_brake_is_a_flag_the_daily_tick_clears():
    assert any("no one-a-day brake" in r for r in walkins.problems(planted(comes(), tick=())))
    assert any("no one-a-day brake" in r for r in walkins.problems(planted(comes(conds=()))))


def test_every_way_out_sets_the_brake():
    leaky = comes(choices=[{"text": "Talk", "flagEffects": [{"flag": "came_to_her_today", "op": "set"}]},
                           {"text": "Walk on"}])
    assert any("`Walk on`" in r and "doesn't set the brake" in r for r in walkins.problems(planted(leaky)))


def test_one_brake_for_the_whole_game():
    other = dict(BRAKE, flag_key="ann_today")
    ann = comes("cafe_ann", "npc_ann", "cafe", conds=(other,),
                choices=[{"text": t, "flagEffects": [{"flag": "ann_today", "op": "set"}]} for t in ("A", "B")])
    rows = walkins.problems(planted(comes(), ann, tick=("came_to_her_today", "ann_today")))
    assert any("different flags" in r for r in rows)


def test_there_is_always_a_way_out():
    one = comes(choices=[{"text": "Talk", "flagEffects": [{"flag": "came_to_her_today", "op": "set"}]}])
    assert any("1 choice(s)" in r for r in walkins.problems(planted(one)))


def test_a_story_moment_never_waits_behind_a_chance():
    does = {"p9": {"park_tom.a": ("a walk-in", "a person's arc step")}}
    assert any("p9: park_tom.a" in r for r in walkins.problems(planted(comes()), does))
    assert walkins.problems(planted(comes()), {"p9": {"park_tom.a": ("a walk-in",)}}) == []


def test_a_retired_scene_is_skipped():
    old = comes(who=None)
    old["trigger"]["is_active"] = "false"
    assert walkins.problems(planted(old)) == []


def test_check_runs_it():
    assert "walkins" in check.CHECKS
    assert check.check_walkins(None, planted(comes(who=None)))[0] == check.RED
    assert check.check_walkins(None, None)[0] == check.INCOMPLETE


# ── from next door (P49, LO, typed in main-lean 2026-11-26: "Go with your picks") ───────────────────────────────

def knock(there="bro_room", who="npc_bro"):
    near = {"type": "npc_at_location", "npc_id": who, "location_id": there, "operator": "is_present"}
    return comes("bro_knocks", who=None, place="her_room", conds=(BRAKE, near))


def test_a_person_may_come_to_her_from_an_adjoining_place():
    assert walkins.problems(planted(knock())) == []  # a sibling room
    hub = planted(knock(there="home"))
    hub["npcs"][2]["schedules"].append({"location": "home"})
    assert walkins.problems(hub) == []  # the area's hub


def test_next_door_must_adjoin_and_hold_their_row():
    far = planted(knock(there="park", who="npc_tom"))
    assert any("doesn't adjoin `her_room`" in r for r in walkins.problems(far))
    norow = planted(knock(there="hall"))
    assert any("no schedule row at `hall`" in r for r in walkins.problems(norow))


def test_requires_npc_at_her_place_without_their_row_points_at_the_next_door_form():
    rows = walkins.problems(planted(comes("bro_knocks", who="npc_bro", place="her_room")))
    assert any("no schedule row at `her_room`" in r and "npc_at_location" in r for r in rows)


def test_neither_form_is_red():
    assert any("with no person" in r for r in walkins.problems(planted(comes(who=None))))
