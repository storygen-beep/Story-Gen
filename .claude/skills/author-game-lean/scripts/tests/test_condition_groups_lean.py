"""Nested condition groups (`{ type = "group", logic, items }`, v2.py:5405-5413) read by the lean scripts the way the
engine reads them: who_is_where, presence, the sheet, the guard and reach. Each has a planted break."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import reach  # noqa: E402
import rules  # noqa: E402
import scenes  # noqa: E402
import sheet  # noqa: E402
import who_is_where as w  # noqa: E402
from test_reach import _cond, _game, _scene  # noqa: E402


def clock(days, start, end):
    return {"type": "group", "logic": "AND", "items": [{"type": "weekday", "weekdays": days},
                                                      {"type": "time_of_day", "start_time": start, "end_time": end}]}


CAFE = {"type": "group", "logic": "OR", "items": [clock([0, 1, 2, 3, 4], "07:00", "20:56"),
                                                  clock([5, 6], "10:00", "20:56")]}


def slot(day, hh, mm=0):
    return (day, hh * 60 + mm)


# ── who_is_where ──

def test_a_group_combines_its_items_by_its_own_logic():
    s = w.when_slots({"version": "1.0", "items": [CAFE]})
    assert slot(0, 8) in s and slot(5, 11) in s
    assert slot(0, 21) not in s and slot(5, 9) not in s and slot(5, 8) not in s


def test_an_and_group_intersects_and_an_empty_or_too_deep_group_never_holds():
    assert w.item_slots(clock([0], "07:00", "08:00")) == {slot(0, 7, m) for m in range(0, 60, 5)}
    assert w.item_slots({"type": "group", "logic": "OR", "items": []}) == set()
    deep = clock([0], "07:00", "08:00")
    for _ in range(3):
        deep = {"type": "group", "logic": "AND", "items": [deep]}
    assert w.item_slots(deep) == set()  # four levels deep: false, as in the engine


def test_planted_break_flattening_the_group_would_narrow_wrongly():
    flat = {"version": "1.0", "logic": "AND", "items": CAFE["items"][0]["items"] + CAFE["items"][1]["items"]}
    assert slot(0, 8) not in w.when_slots(flat)  # ANDing both branches loses Monday 8am
    assert slot(0, 8) in w.when_slots({"version": "1.0", "items": [CAFE]})


# ── presence ──

def kitchen(trigger_cond):
    return {"npcs": [{"id": "npc_mom", "name": "Laura", "role": "Mom",
                      "schedules": [{"location": "kitchen", "start_time": "07:00", "end_time": "09:00"}]}],
            "canvases": [{"id": "k", "trigger": {"location": "kitchen", "conditions": trigger_cond},
                          "nodes": [{"id": "a", "blocks": [{"type": "dialog", "content": "Eggs?",
                                                            "props": {"speaker": "npc", "npcId": "npc_mom"}}]}]}]}


PRESENT = {"type": "npc_at_location", "npc_id": "npc_mom", "location_id": "kitchen", "operator": "is_present"}
FLAG = {"type": "flag", "flag_key": "x", "operator": "is_true"}


def test_a_presence_check_on_every_branch_counts():
    cond = {"version": "1.0", "items": [{"type": "group", "logic": "OR", "items": [
        {"type": "group", "logic": "AND", "items": [PRESENT, FLAG]}, PRESENT]}]}
    assert scenes.guaranteed(cond) == {"npc_mom"}
    assert scenes.check_presence(kitchen(cond)) == ("green", [])


def test_planted_break_a_presence_check_on_one_branch_only_is_not_a_check():
    cond = {"version": "1.0", "items": [{"type": "group", "logic": "OR", "items": [PRESENT, FLAG]}]}
    assert scenes.guaranteed(cond) == set()
    assert scenes.check_presence(kitchen(cond))[0] == "red"


# ── the sheet ──

def cafe_game():
    return {"npcs": [{"id": "npc_tom", "name": "Tom", "schedules": [
                {"location": "cafe", "weekdays": [0, 1, 2, 3, 4], "start_time": "07:00", "end_time": "21:00"},
                {"location": "cafe", "weekdays": [5, 6], "start_time": "10:00", "end_time": "21:00"}]}],
            "canvases": [{"id": "work", "trigger": {"location": "cafe", "conditions": {"version": "1.0", "items": [CAFE]}},
                          "nodes": [{"id": "a", "blocks": []}]}]}


def test_the_sheet_prints_a_grouped_clock_part_by_part():
    row = sheet.compute(cafe_game(), {"work"})["work.a"]
    assert row["clock"] == "07:00–20:56 · Mon Tue Wed Thu Fri / 10:00–20:56 · Sat Sun"  # the real minutes
    assert row["who"] == "npc_tom"  # Tom is there every minute the row can show, on each kind of day
    hand = "weekdays 07:00–20:56 / weekends 10:00–20:56"
    assert sheet.norm("clock", hand) == sheet.norm("clock", row["clock"])


def test_planted_break_a_wrong_weekend_hour_differs():
    row = sheet.compute(cafe_game(), {"work"})["work.a"]
    assert sheet.norm("clock", "weekdays 07:00–20:56 / weekends 09:00–20:56") != sheet.norm("clock", row["clock"])


def test_the_sheet_flags_and_clothes_count_only_what_every_branch_checks():
    either = {"version": "1.0", "items": [{"type": "group", "logic": "OR", "items": [
        FLAG, {"type": "clothing_item", "item_id": "apron", "operator": "equipped"}]}]}
    g = cafe_game()
    g["canvases"][0]["trigger"]["conditions"] = either
    row = sheet.compute(g, {"work"})["work.a"]
    assert row["flags"] == "none" and row["wearing"] == "any"


# ── the guard ──

def test_the_guard_reads_a_clock_group_as_a_gate():
    g = {"project": {}, "canvases": [{"id": "hire", "trigger": {"location": "cafe", "is_repeatable": False,
                                                                 "conditions": {"version": "1.0", "items": [CAFE]}},
                                      "nodes": [{"id": "ask", "blocks": []}]}]}
    does = {"hire.ask": ["a person's arc step", "a no is possible"]}
    assert not any("fires by itself" in r for r in rules.guard(does, g))
    g["canvases"][0]["trigger"]["conditions"] = {"version": "1.0", "items": [
        {"type": "group", "logic": "OR", "items": [FLAG, CAFE]}]}  # planted: a flag alone can open it any hour
    assert any("fires by itself" in r for r in rules.guard(does, g))


# ── reach ──

def test_reach_reads_a_flag_inside_a_group():
    dead = _cond({"type": "group", "logic": "AND", "items": [{"type": "flag", "flag_key": "never_set",
                                                               "operator": "is_true"}, CAFE]})
    r = reach.check(_game(_scene("start"), _scene("gate", cond=dead)))
    assert "gate" in r["scenes"] and "never_set" in r["scenes"]["gate"][0]


def test_reach_keeps_an_or_group_open_when_one_branch_can_hold():
    live = _cond({"type": "group", "logic": "OR", "items": [{"type": "flag", "flag_key": "never_set",
                                                              "operator": "is_true"}, CAFE]})
    assert "gate" not in reach.check(_game(_scene("start"), _scene("gate", cond=live)))["scenes"]


def test_reach_an_empty_group_never_opens():
    r = reach.check(_game(_scene("start"), _scene("gate", cond=_cond({"type": "group", "logic": "AND", "items": []}))))
    assert "gate" in r["scenes"]


# ── a grouped clock prints its real minutes (P10, 2026-11-24: "19:56" printed as "20:00") ──

P10_HOUR = {"type": "group", "logic": "OR", "items": [clock([0, 1, 2, 3, 4], "07:00", "19:56"), clock([5], "10:00", "19:56"),
                                                      clock([6], "10:00", "18:56")]}


def test_a_grouped_clock_prints_its_real_minutes():
    g = cafe_game()
    g["canvases"][0]["trigger"]["conditions"] = {"version": "1.0", "items": [P10_HOUR]}
    row = sheet.compute(g, {"work"})["work.a"]
    assert row["clock"] == "07:00–19:56 · Mon Tue Wed Thu Fri / 10:00–19:56 · Sat / 10:00–18:56 · Sun"
    hand = "weekdays 07:00–19:56, Sat 10:00–19:56, Sun 10:00–18:56 +0"  # the card's comma form
    assert sheet.norm("clock", hand) == sheet.norm("clock", row["clock"])
    assert sheet.norm("clock", "weekdays 07:00–19:56, Sat 10:00–19:56, Sun 10:00–19:56") != sheet.norm("clock", row["clock"])


# ── a retired canvas (is_active = false, kept for old saves) is skipped (P10's six old rows) ──

def test_a_retired_canvas_raises_nothing_and_unretiring_brings_its_checks_back():
    old = _scene("old_row", cond=_cond({"type": "flag", "flag_key": "never_set", "operator": "is_true"}), is_active=False)
    g = _game(_scene("start"), old)
    assert "old_row" not in reach.check(g)["scenes"]
    assert scenes.retired(old) and sheet.compute(g, {"old_row"}) == {}
    assert "old_row.a" not in rules.seen(g)
    old["trigger"]["is_active"] = True
    assert "old_row" in reach.check(g)["scenes"] and "old_row.a" in sheet.compute(g, {"old_row"})
    assert "old_row.a" in rules.seen(g)
