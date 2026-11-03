"""Three checker false alarms found on first_term (two-pass alignment audit, 2026-11-03).

1. `world reachable` built its walk graph from `entry_from` and `navigation_order` only, so
   the rooms of an `is_container` building (entered at its `default_entry`, rooms naming it
   as `parent`) dropped out: first_term read 10/38 while the build linked all 38.
2. `a day-cap closes` read canvases only, so a cap flag set by a phone reply was "never set".
3. `a named person is where the line says` counted a voice or a sound through the wall or
   the door from the next room as the person being "not here".

Fixtures only; nothing in games/ is read or written.
"""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402

ALL = [0, 1, 2, 3, 4, 5, 6]


def row(g, name):
    model, g2 = gates.build(copy.deepcopy(g))
    return next(r for r in gates.run_gates(model, g2, None) if r["gate"] == name)


# ── 1. world reachable: a container building ──────────────────────────────────
def building_game():
    """A street with a home container; the hall is the default entry and names `home` as
    its parent only; the kitchen hangs off the hall; the bathroom names its parent only."""
    return {
        "project": {"id": "fx", "name": "fx", "starting_canvas": "c"},
        "locations": [
            {"id": "street", "navigation_order": ["home"]},
            {"id": "home", "entry_from": "street", "is_container": True, "default_entry": "hall"},
            {"id": "hall", "parent": "home"},
            {"id": "kitchen", "parent": "home", "entry_from": "hall"},
            {"id": "bathroom", "parent": "home"},
        ],
        "canvases": [{"id": "c", "trigger": {"location": "hall"},
                      "nodes": [{"id": "n", "blocks": [{"type": "paragraph", "content": "Here."}]}]}],
    }


def test_a_container_building_is_walked_through_its_parent():
    r = row(building_game(), "world reachable")
    assert r["pass_"] is True, r["detail"]
    assert r["headline"].startswith("5/5")


def test_a_parent_that_does_not_exist_still_strands_the_room():
    g = building_game()
    g["locations"].append({"id": "attic", "parent": "nowhere"})
    r = row(g, "world reachable")
    assert r["pass_"] is False
    assert [d.split()[0] for d in r["detail"]] == ["attic"]


def test_the_helper_links_container_entry_and_parent_both_ways():
    adj = gates._location_parent_adjacency(building_game()["locations"])
    assert "hall" in adj["home"] and "home" in adj["hall"]
    assert "bathroom" in adj["home"] and "home" in adj["bathroom"]


# ── 2. a day-cap closes: a phone reply sets the flag ──────────────────────────
def cap_game(phone):
    return {
        "project": {"id": "fx", "name": "fx", "starting_canvas": "c"},
        "locations": [{"id": "kitchen"}],
        "engine": {"daily_tick": {"flagEffects": [
            {"targetType": "player", "flag": "said_eating_out", "op": "unset"}]}},
        "canvases": [{"id": "c", "trigger": {"location": "kitchen", "is_repeatable": True},
                      "nodes": [{"id": "n", "blocks": [{"type": "paragraph", "content": "Dinner."}],
                                 "exit_block": {"type": "choices", "choices": [
                                     {"text": "Eat.", "targetType": "location", "locationId": "kitchen",
                                      "conditions": {"version": "1.0", "logic": "AND", "items": [
                                          {"type": "flag", "subject": "player",
                                           "flag_key": "said_eating_out", "operator": "is_false"}]}}]}}]}],
        "phone": phone,
    }


SETS = [{"targetType": "player", "flag": "said_eating_out", "op": "set"}]


def test_a_cap_set_by_a_phone_reply_closes():
    phone = {"conversations": [{"id": "laura_dinner", "blocks": [
        {"round": 1, "choices": [{"text": "eating out tonight", "flagEffects": SETS}]}]}]}
    r = row(cap_game(phone), "a day-cap closes")
    assert r["pass_"] is True, r["detail"]


def test_a_cap_set_by_on_ignore_closes():
    phone = {"conversations": [{"id": "laura_dinner", "ignore_after_days": 1,
                                "on_ignore": {"flagEffects": SETS}, "blocks": []}]}
    r = row(cap_game(phone), "a day-cap closes")
    assert r["pass_"] is True, r["detail"]


def test_a_cap_nothing_sets_is_still_red():
    r = row(cap_game({"conversations": []}), "a day-cap closes")
    assert r["pass_"] is False
    assert "said_eating_out" in r["detail"][0]


# ── 3. a named person is where the line says: heard from next door ───────────
def house_game(blocks, ryan_room="ryan_room"):
    """A home container with Ella's room and Ryan's room; Ryan is in `ryan_room` until noon
    and in the hall after, so a line placing him at no fixed spot is red unless excused."""
    return {
        "time": {"starting_day": "Monday", "starting_hour": 7},
        "locations": [
            {"id": "street"},
            {"id": "home", "entry_from": "street", "is_container": True, "default_entry": "hall"},
            {"id": "hall", "parent": "home"},
            {"id": "ella_room", "parent": "home", "entry_from": "hall"},
            {"id": "ryan_room", "parent": "home", "entry_from": "hall"},
            {"id": "cafe", "entry_from": "street"},
        ],
        "npcs": [{"id": "npc_ryan", "name": "Ryan", "schedules": [
            {"location": ryan_room, "weekdays": ALL, "start_time": "00:00", "end_time": "12:00",
             "activity": "music"},
            {"location": "hall", "weekdays": ALL, "start_time": "12:00", "end_time": "24:00",
             "activity": "music"}]}],
        "canvases": [{"id": "wall", "trigger": {"location": "ella_room", "is_repeatable": True},
                      "nodes": [{"id": "n1", "blocks": blocks, "exit_block": {"type": "choices", "choices": [
                          {"text": "Go.", "targetType": "location", "locationId": "hall"}]}}]}],
    }


def para(text):
    return {"type": "paragraph", "content": text}


def say(npc, text):
    return {"type": "dialog", "content": text, "props": {"speaker": "npc", "npcId": npc}}


def test_a_sound_through_the_wall_from_the_next_room_is_not_counted():
    g = house_game([para("Ryan's music thumps through the wall.")])
    ok, _, detail = gates._named_person_present(g)
    assert ok is True, detail
    assert detail and detail[0].startswith("heard from next door — not counted")


def test_a_voice_beside_a_hearing_line_is_not_counted():
    g = house_game([para("Through the door you hear him moving."), say("npc_ryan", "Are you up?")])
    ok, _, detail = gates._named_person_present(g)
    assert ok is True, detail
    assert any("Ryan speaks" in d and d.startswith("heard from next door") for d in detail)


def test_the_same_line_with_no_hearing_word_is_still_red():
    g = house_game([para("Ryan's music is on, loud.")])
    ok, _, _ = gates._named_person_present(g)
    assert ok is False


def test_a_hearing_line_from_a_room_not_next_door_is_still_red():
    g = house_game([para("Ryan's music thumps through the wall.")], ryan_room="cafe")
    ok, _, detail = gates._named_person_present(g)
    assert ok is False
    assert not any(d.startswith("heard from next door") for d in detail)


# ── 4. the truth gates' building is its container ─────────────────────────────
def mum_game(text, mum_room):
    """The `house_game` home with Mum in `mum_room` all day; the line shows in the hall."""
    g = house_game([para(text)])
    g["locations"].append({"id": "kitchen", "parent": "home", "entry_from": "hall"})
    g["npcs"] = [{"id": "npc_mum", "name": "Mum", "role": "mom", "schedules": [
        {"location": mum_room, "weekdays": ALL, "start_time": "00:00", "end_time": "24:00",
         "activity": "cooking"}]}]
    g["canvases"][0]["trigger"]["location"] = "hall"
    return g


def test_a_room_of_a_container_home_is_in_its_building():
    g = mum_game("", "kitchen")
    assert gates._tr_building(g, "hall") == {"home", "hall", "ella_room", "ryan_room", "kitchen"}
    assert gates._tr_building(g, "home") == gates._tr_building(g, "kitchen")


def test_mom_up_in_the_kitchen_is_here_from_the_hall():
    ok, _, detail = gates._named_person_present(mum_game("Not here. Mom's up.", "kitchen"))
    assert ok is True, detail


def test_mom_up_at_the_cafe_is_still_not_here():
    ok, _, detail = gates._named_person_present(mum_game("Not here. Mom's up.", "cafe"))
    assert ok is False
    assert "not here" in detail[0]


def test_a_district_container_with_no_default_entry_is_not_one_building():
    g = mum_game("", "kitchen")
    g["locations"] += [{"id": "town", "entry_from": "street", "is_container": True},
                       {"id": "flat", "parent": "town", "entry_from": "town", "is_container": True,
                        "default_entry": "flat_room"},
                       {"id": "flat_room", "parent": "flat"},
                       {"id": "shop", "parent": "town", "entry_from": "town"}]
    assert gates._tr_building(g, "flat_room") == {"flat", "flat_room"}
    assert "flat_room" not in gates._tr_building(g, "shop")
