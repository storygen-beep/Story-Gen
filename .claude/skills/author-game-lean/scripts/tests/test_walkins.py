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


# ── kind (a) fires on arrival too (LO, typed in main-lean 2026-11-26: "2nd one", "Go") ─────────────────────────

def found(cid="bridge_couple", conds=(), mpd=1, mode="random", choices=None):
    c = comes(cid, who=None, place="park", conds=conds, choices=choices if choices is not None else [
        {"text": "Watch", "flagEffects": [{"flag": "saw_bridge_couple", "op": "set"}]}, {"text": "Back up the path"}])
    c["trigger"]["trigger_mode"] = mode
    c["trigger"]["chance"] = 0.35
    if mpd is not None:
        c["trigger"]["max_triggers_per_day"] = mpd
    return c


FINDS = {"p8": {"bridge_couple.a": ("a walk-in", "she comes across something")}}


def test_a_walk_in_she_comes_across_is_green_off_the_brake():
    assert walkins.problems(planted(comes(), found()), FINDS) == []


def test_a_walk_in_she_comes_across_is_never_a_button():
    assert any("is a button" in r for r in walkins.problems(planted(comes(), found(mode="manual")), FINDS))
    old = {"p8": {"bridge_couple.a": ("a walk-in",)}}  # an older card's label, on a button at a place
    assert any("is a button" in r for r in walkins.problems(planted(found(mode="manual")), old))


def test_someone_walking_in_on_her_stays_a_substitution():
    act = found("shower", mode="manual")
    act["trigger"]["substitutions"] = [{"target_canvas_id": "shower_walk_in", "chance": 0.2}]
    target = found("shower_walk_in", mode="manual")
    target["trigger"]["substitution_only"] = True
    does = {"p8": {"shower.a": ("a walk-in",), "shower_walk_in.a": ("a walk-in",)}}
    assert walkins.problems(planted(act, target), does) == []


def test_a_walk_in_she_comes_across_is_off_the_shared_brake():
    waits = found(conds=(BRAKE,))
    assert any("on the shared brake `came_to_her_today`" in r for r in walkins.problems(planted(comes(), waits), FINDS))
    sets_it = found(choices=[{"text": t, "flagEffects": [{"flag": "came_to_her_today", "op": "set"}]} for t in "AB"])
    assert any("shared brake" in r for r in walkins.problems(planted(comes(), sets_it), FINDS))


def test_a_walk_in_she_comes_across_is_once_a_day_and_has_a_way_out():
    assert any("max_triggers_per_day = 1" in r for r in walkins.problems(planted(found(mpd=None)), FINDS))
    one = found(choices=[{"text": "Watch"}])
    assert any("1 choice(s)" in r for r in walkins.problems(planted(one), FINDS))


# ── it fits what she is doing (C2196; LO, typed in main-lean 2026-11-26: "she is working out in this scene. Why??",
# then "Go ahead.") ─────────────────────────────────────────────────────────────────────────────────────────────────

def said(canvas, line):
    canvas["nodes"][0]["blocks"] = [{"type": "group", "blocks": [{"type": "dialog", "content": line}]}]
    return canvas


def gym(rule_conds=(), sub_only=True, place="park", choices=None):
    """A 'Work out' act at the park with Tom's notes riding on it, the way C2196 builds it."""
    target = comes("tom_notes", choices=choices)
    target["trigger"]["trigger_mode"] = "manual"
    target["trigger"]["location"] = place
    if sub_only:
        target["trigger"]["substitution_only"] = True
    said(target, "Your stance is all wrong. Here.")
    act = {"id": "work_out", "trigger": {"location": "park", "trigger_mode": "manual", "substitutions": [
        {"target_canvas_id": "tom_notes", "chance": 0.65,
         "conditions": {"version": "1.0", "logic": "AND", "items": list(rule_conds)}}]},
        "nodes": [{"id": "lift", "exit_block": {"choices": [{"text": "Done"}]}}]}
    return act, target


def test_a_scene_on_arrival_that_has_her_mid_act_is_red():
    rows = walkins.problems(planted(said(comes(), "Your stance is all wrong, though. Here."), comes("cafe_ann", "npc_ann", "cafe")))
    assert any("park_tom" in r and "mid-act" in r and "C2196" in r for r in rows)


def test_a_scene_on_arrival_at_the_door_is_green():
    door = said(comes(), "He's at the gate before you're through it. You run?")
    assert walkins.problems(planted(door, comes("cafe_ann", "npc_ann", "cafe"))) == []


def test_the_same_words_riding_on_the_act_are_green():
    act, target = gym()
    assert walkins.problems(planted(comes("cafe_ann", "npc_ann", "cafe"), act, target)) == []


def test_a_scene_inside_an_act_keeps_the_brake_and_a_way_out():
    leaky = [{"text": "Hold still", "flagEffects": [{"flag": "came_to_her_today", "op": "set"}]},
             {"text": "I've got it"}]
    act, target = gym(choices=leaky)
    rows = walkins.problems(planted(comes("cafe_ann", "npc_ann", "cafe"), act, target))
    assert any("tom_notes" in r and "`I've got it`" in r and "doesn't set the brake" in r for r in rows)


def test_a_scene_inside_an_act_is_substitution_only_at_the_acts_place():
    act, target = gym(sub_only=False)
    rows = walkins.problems(planted(comes("cafe_ann", "npc_ann", "cafe"), act, target))
    assert any("tom_notes" in r and "isn't substitution_only" in r for r in rows)
    act, target = gym(place="cafe")
    rows = walkins.problems(planted(comes("cafe_ann", "npc_ann", "cafe"), act, target))
    assert any("tom_notes" in r and "trigger.location is `cafe`" in r for r in rows)


def test_someone_walking_in_on_her_off_the_brake_is_not_checked_as_coming_to_her():
    act, target = gym(sub_only=False)
    target["trigger"]["conditions"]["items"] = []  # off the brake: the housemate at the bathroom door
    assert walkins.problems(planted(comes("cafe_ann", "npc_ann", "cafe"), act, target)) == []
