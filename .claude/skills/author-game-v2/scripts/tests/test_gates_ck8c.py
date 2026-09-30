"""CK8c (PRD v2, 2026-09-30): hour-level fixes.

  I11 · G30 "works alone" = a solo canvas live in an hour when NOBODY is scheduled in the
        room, in a room where someone is scheduled at another hour.
  H13 · a time cost is a brake when it is >= the source canvas's own schedule window.
  H12 · new gate "a need can be met every day": something that raises each need is live on
        every weekday (trigger schedule, narrowed by the place's EN3 `hours`).

Fixtures are written here; nothing in games/ is read or written.
"""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402

EVERY = [0, 1, 2, 3, 4, 5, 6]


def sched(start, end, days=EVERY):
    return [{"weekdays": days, "start_time": start, "end_time": end}]


# ── I11 ───────────────────────────────────────────────────────────────────────

def walkin(npc_rows, canvas_sched=None):
    t = {"location": "bar", "is_repeatable": True}
    if canvas_sched:
        t["schedules"] = canvas_sched
    g = {"project": {"id": "fx", "name": "fx"}, "player": {"core_traits": {}},
         "locations": [{"id": "bar"}],
         "npcs": [{"id": "npc_a", "schedules": [dict(r, location="bar") for r in npc_rows]}],
         "canvases": [{"id": "wipe", "trigger": t,
                       "nodes": [{"id": "n", "blocks": [{"type": "paragraph", "content": "You wipe."}]}]}]}
    model, g2 = gates.build(copy.deepcopy(g))
    return gates._walkin_join(model, g2)[0]


def test_a_room_that_is_never_empty_is_not_working_alone():
    assert walkin(sched("00:00", "00:00")) == []


def test_a_canvas_live_while_the_room_is_empty_qualifies():
    assert walkin(sched("18:00", "20:00"), canvas_sched=sched("09:00", "17:00")) == ["bar"]


def test_a_canvas_live_only_while_someone_is_there_does_not():
    assert walkin(sched("18:00", "20:00"), canvas_sched=sched("18:00", "20:00")) == []


def test_an_unscheduled_canvas_in_a_part_time_room_qualifies():
    assert walkin(sched("18:00", "20:00")) == ["bar"]


# ── H13 ───────────────────────────────────────────────────────────────────────

def route(minutes, hub_sched=True, on_target=False):
    ch = {"text": "Work the counter", "targetType": "node", "nodeId": "rung"}
    rung_cfg = {"locationId": "bar"}
    if on_target:
        rung_cfg["time_progression_minutes"] = minutes
    else:
        ch["time_progression_minutes"] = minutes
    hub_t = {"location": "bar", "is_repeatable": True}
    if hub_sched:
        hub_t["schedules"] = sched("18:00", "22:00")
    g = {"canvases": [
        {"id": "hub", "trigger": hub_t,
         "nodes": [{"id": "n", "exit_block": {"type": "choices", "choices": [ch]}}]},
        {"id": "rung", "nodes": [{"id": "base", "exit_block": {"type": "location",
                                                                "config": rung_cfg}}]}]}
    return gates._routes([], g)["rung"][0]


def test_a_click_that_fills_the_window_is_a_brake():
    r = route(240)
    assert r["timecap"] and r["braked"]


def test_a_short_click_is_not_a_brake():
    assert not route(60)["braked"]


def test_no_window_means_time_is_no_brake():
    assert not route(240, hub_sched=False)["braked"]


def test_time_on_the_target_exit_counts():
    assert route(240, on_target=True)["braked"]


# ── H12 ───────────────────────────────────────────────────────────────────────

def need_game(sources, hours=None, triggerless_from_daily_hub=False):
    locs = [{"id": "kitchen", **({"hours": hours} if hours else {})}, {"id": "hall"}]
    canvases = []
    for i, days in enumerate(sources):
        canvases.append({"id": f"eat_{i}", "trigger": {
            "location": "kitchen", "is_repeatable": True, "schedules": sched("12:00", "13:00", days)},
            "nodes": [{"id": "n", "exit_block": {"type": "location", "config": {
                "locationId": "kitchen",
                "effects": [{"trait": "fed", "op": "add", "value": 30}]}}}]})
    if triggerless_from_daily_hub:
        canvases += [
            {"id": "hub", "trigger": {"location": "hall", "is_repeatable": True},
             "nodes": [{"id": "n", "exit_block": {"type": "choices", "choices": [
                 {"text": "Eat", "targetType": "node", "nodeId": "snack"}]}}]},
            {"id": "snack", "nodes": [{"id": "base", "exit_block": {"type": "location", "config": {
                "locationId": "hall", "effects": [{"trait": "fed", "op": "add", "value": 10}]}}}]}]
    return {"project": {"id": "fx", "name": "fx"}, "player": {"core_traits": {"fed": 50}},
            "locations": locs, "canvases": canvases}


NEEDS = {"board": {"needs": [{"key": "fed", "decay_per_day": 20}]}}


def need_row(g, state=NEEDS):
    model, g2 = gates.build(copy.deepcopy(g))
    return next(r for r in gates.run_gates(model, g2, state)
                if r["gate"] == "a need can be met every day")


def test_a_need_with_no_sunday_source_fails():
    r = need_row(need_game([[0, 1, 2, 3, 4, 5]]))
    assert r["pass_"] is False and r["detail"] == ["`fed`: nothing that raises it is live on Sun"]


def test_a_sunday_source_fills_the_gap():
    assert need_row(need_game([[0, 1, 2, 3, 4, 5], [6]]))["pass_"] is True


def test_a_place_closed_on_sunday_shuts_its_source():
    hours = [{"weekdays": [0, 1, 2, 3, 4, 5], "open": "08:00", "close": "20:00"}]
    r = need_row(need_game([EVERY], hours=hours))
    assert r["pass_"] is False and "Sun" in r["detail"][0]


def test_a_triggerless_rung_takes_its_hubs_days():
    assert need_row(need_game([], triggerless_from_daily_hub=True))["pass_"] is True


def test_no_needs_is_na():
    assert need_row(need_game([EVERY]), {"board": {}})["na"] is True


def test_a_set_to_a_full_value_is_a_refill():
    g = need_game([EVERY])
    g["canvases"][0]["nodes"][0]["exit_block"]["config"]["effects"] = [
        {"trait": "fed", "op": "set", "value": 100}]
    assert need_row(g)["pass_"] is True
