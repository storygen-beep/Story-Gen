"""first_term's reach fixes, 2026-11-09 (DECISIONS 214-218; SKILL_NOTEBOOK N37).

  the loop is open enough hours   the floor is 18 (the top games' low end); a hub loop counts only the
                                  hours its explicit screens can be reached, past a time-gated button
  a walk-in can happen            a substitution rule that reads a person where their rows never put
                                  them, in the rule's own hours, can never fire
  ladders move forward            a step's `when_also` is checked on its own days and hours

Fixtures are written here; nothing in games/ is read or written.
"""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import gates  # noqa: E402
from test_gates_group2_checks import EXPLICIT, STATE, ch, cv, game, nd, row  # noqa: E402
from test_gates_playtest_20261109 import routine_state  # noqa: E402

ROUTINE = "the loop is open enough hours"
WALKIN = "a walk-in can happen"
TOD = lambda a, b: {"type": "time_of_day", "start_time": a, "end_time": b}
WD = lambda *d: {"type": "weekday", "weekdays": list(d)}
AT = lambda npc, loc: {"type": "npc_at_location", "npc_id": npc, "location_id": loc, "operator": "is_present"}
V1 = lambda *items: {"version": "1.0", "logic": "AND", "items": list(items)}


def test_the_floor_is_the_top_games_low_end():
    assert gates.ROUTINE_HOURS_FLOOR == 18


# ── the loop is open enough hours: the act's own button ─────────────────────
def hub_game(button_items):
    """A hub he is in every evening 18-22 (28 h a week), and the act behind one button."""
    npc = {"id": "npc_r", "name": "Ryan", "schedules": [
        {"location": "room", "weekdays": [0, 1, 2, 3, 4, 5, 6], "start_time": "18:00", "end_time": "22:00"}]}
    hub = cv("hub", [nd("a", [ch("Wait for him.", node="act", conds=button_items), ch("Go.")]),
                     nd("act", [ch("Back to your room.")], text=EXPLICIT)], requires_npc="npc_r")
    return game(cv("step_1", [nd("a", [ch("Yes.", flags=["r_done"])])], is_repeatable=False), hub, npcs=[npc])


def test_a_hub_loop_behind_a_quarter_hour_button_fails():
    """first_term: Jake's gym act sat behind a 16:30-16:45 button inside a 4-hour gym screen."""
    r = row(hub_game([TOD("18:00", "18:15")]), ROUTINE, routine_state(("hub",)))
    assert r["pass_"] is False and any("1.8 h a week" in d for d in r["detail"]), r


def test_a_hub_loop_open_all_evening_passes():
    r = row(hub_game([]), ROUTINE, routine_state(("hub",)))
    assert r["pass_"] is True and any("28 h a week on 7 day(s)" in d for d in r["detail"]), r


# ── a walk-in can happen ────────────────────────────────────────────────────
def walkin_game(rule_items):
    npc = {"id": "npc_l", "name": "Laura", "schedules": [
        {"location": "kitchen", "weekdays": [6], "start_time": "18:00", "end_time": "21:30"}]}
    host = cv("living_tv", [nd("a", [ch("Get up.")])])
    host["trigger"]["substitutions"] = [{"target_canvas_id": "walkin_tv_laura", "chance": 0.25,
                                         "conditions": V1(*rule_items)}]
    walk = cv("walkin_tv_laura", [nd("a", [ch("Turn it off.")])], substitution_only=True)
    return game(host, walk, npcs=[npc])


def test_a_walkin_reading_her_after_her_row_ends_fails():
    """first_term: Laura's Sunday channel 5 read her in the kitchen 21:30-21:58 once her row ended 21:30."""
    r = row(walkin_game([AT("npc_l", "kitchen"), WD(6), TOD("21:30", "21:58")]), WALKIN)
    assert r["pass_"] is False and any("walkin_tv_laura" in d and "never fire" in d for d in r["detail"]), r


def test_a_walkin_inside_her_row_passes():
    r = row(walkin_game([AT("npc_l", "kitchen"), WD(6), TOD("20:30", "21:28")]), WALKIN)
    assert r["pass_"] is True, r


def test_a_walkin_on_the_wrong_day_fails():
    r = row(walkin_game([AT("npc_l", "kitchen"), WD(2), TOD("20:30", "21:28")]), WALKIN)
    assert r["pass_"] is False, r


def test_no_walkin_naming_a_person_is_not_judged():
    r = row(walkin_game([WD(6), TOD("20:30", "21:28")]), WALKIN)
    assert r["na"] is True, r


# ── ladders move forward: the second window ─────────────────────────────────
def test_step_windows_keep_each_window_on_its_own_days():
    st = {"when": {"days": ["Mon", "Tue"], "from": "20:30", "to": "22:00"},
          "when_also": {"days": ["Wed"], "from": "22:00", "to": "00:00"}}
    assert gates._step_windows(st, "20:30", "22:00") == [([0, 1], "20:30", "22:00"), ([2], "22:00", "00:00")]


def test_step_windows_without_a_second_window():
    st = {"when": {"days": ["Thu"], "from": "18:00", "to": "19:30"}}
    assert gates._step_windows(st, "18:00", "19:30") == [([3], "18:00", "19:30")]


# ── lint · the world around her: random-scene depth (2026-11-10) ─────────────
def test_random_depth_lists_a_place_where_one_scene_fires():
    npc = {"id": "npc_l", "name": "Laura", "schedules": [
        {"location": "room", "weekdays": [0], "start_time": "18:00", "end_time": "20:00"}]}
    one = cv("ev_a", [nd("a", [ch("Go.")])], trigger_mode="random", chance=0.3, requires_npc="npc_l")
    g = game(one, npcs=[npc])
    rows = gates.lint_random_depth(gates.build(copy.deepcopy(g))[1])
    assert rows and rows[0].startswith("room:") and "only one can fire in 100%" in rows[0], rows


def test_random_depth_counts_two_scenes_at_once():
    npc = {"id": "npc_l", "name": "Laura", "schedules": [
        {"location": "room", "weekdays": [0], "start_time": "18:00", "end_time": "20:00"}]}
    a = cv("ev_a", [nd("a", [ch("Go.")])], trigger_mode="random", chance=0.3, requires_npc="npc_l")
    b = cv("ev_b", [nd("a", [ch("Go.")])], trigger_mode="random", chance=0.3, requires_npc="npc_l")
    rows = gates.lint_random_depth(gates.build(copy.deepcopy(game(a, b, npcs=[npc])))[1])
    assert rows and "median 2" in rows[0] and "in 0%" in rows[0], rows
