"""LO's first_term playtest, 2026-11-09 (REPORT.md in ~/Documents/Great_Games_Study_20260926/
playtest_study_20261109/). Each check tested the easy moment; these pin the real one.

  a pay can happen                    a raise that opens at or above its own cap never pays
  the loop is open enough hours    a ladder's loop is reachable ROUTINE_HOURS_FLOOR h a week, or by invite
  a card line belongs to its person   no goal line pasted onto 3+ cards; no one named before the card waits for them
  lint · the world around her         everyday-life events and people in the places (a list, never a score)

The stage-top half of `every stage has a way up` is pinned in test_gates_way_up.py.
Fixtures are written here; nothing in games/ is read or written.
"""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import gates  # noqa: E402
from test_gates_group2_checks import EXPLICIT, STATE, ch, cv, flag, game, nd, pay, row, trait  # noqa: E402

PAY = "a pay can happen"
ROUTINE = "the loop is open enough hours"
CARD = "a card line belongs to its person"


# ── a pay can happen ─────────────────────────────────────────────────────────
def test_a_raise_that_opens_at_its_cap_never_pays():
    """first_term's couch: "Watch his game in your underwear" opens at 40 and is capped at 39."""
    g = game(cv("couch", [nd("a", [ch("Watch in your underwear.", eff=[pay("heat", 1, 39)],
                                      conds=[trait("heat", "gte", 40)])])]))
    r = row(g, PAY)
    assert r["pass_"] is False and "opens at heat 40" in r["detail"][0] and "never pay" in r["detail"][0], r


def test_a_raise_behind_a_step_set_above_its_cap_never_pays():
    """laura_alone_after: it waits on a step the game sets only at 20, and pays to 19."""
    g = game(cv("step", [nd("a", [ch("Yes.", flags=["laura_04_done"])])], is_repeatable=False,
                conditions={"version": "1.0", "logic": "AND", "items": [trait("heat", "gte", 20)]}),
             cv("after", [nd("a", [ch("Lie still.", eff=[pay("heat", 1, 19)])])],
                conditions={"version": "1.0", "logic": "AND", "items": [flag("laura_04_done")]}))
    r = row(g, PAY)
    assert r["pass_"] is False and "after" in r["detail"][0], r


def test_a_raise_under_its_cap_passes():
    g = game(cv("couch", [nd("a", [ch("Sit closer.", eff=[pay("heat", 1, 59)],
                                      conds=[trait("heat", "gte", 40)])])]))
    assert row(g, PAY)["pass_"] is True


# ── the loop is open enough hours ─────────────────────────────────────────
def routine_game(rows, call=False):
    npc = {"id": "npc_r", "name": "Ryan", "schedules": rows}
    g = game(cv("step_1", [nd("a", [ch("Yes.", flags=["r_done"])])], is_repeatable=False),
             cv("couch", [nd("a", [ch("Back to your room.")], text=EXPLICIT)], requires_npc="npc_r"),
             npcs=[npc])
    if call:
        g["phone"] = {"calls": [{"id": "come_over", "caller": "npc_r", "accept": "couch"}]}
    return g


def routine_state(loop=("couch",)):
    st = copy.deepcopy(STATE)
    st["board"]["characters"] = [{"id": "npc_r", "ladder": {"counter": "r_step", "loop": list(loop) if not
                                                            isinstance(loop, str) else loop,
                                                            "steps": [{"n": 1, "canvas": "step_1"}]}}]
    return st


WEEKEND = [{"location": "room", "weekdays": [5, 6], "start_time": "14:00", "end_time": "18:00"}]
EVENINGS = [{"location": "room", "weekdays": [0, 1, 2, 3, 4, 5, 6], "start_time": "18:00", "end_time": "21:00"}]   # 21 h (the floor is 18 since 2026-11-09)


def test_a_loop_open_one_weekend_afternoon_fails():
    """first_term: Ryan's couch, Sat/Sun 14-18 only, 8 h a week."""
    r = row(routine_game(WEEKEND), ROUTINE, routine_state())
    assert r["pass_"] is False and any("8 h a week" in d and "under 18" in d for d in r["detail"]), r


def test_a_loop_open_every_evening_passes():
    r = row(routine_game(EVENINGS), ROUTINE, routine_state())
    assert r["pass_"] is True and any("21 h a week on 7 day(s)" in d for d in r["detail"]), r


def test_a_phone_invite_counts_wherever_he_is():
    r = row(routine_game(WEEKEND, call=True), ROUTINE, routine_state())
    assert r["pass_"] is True and any("a phone invite" in d for d in r["detail"]), r


def test_a_text_thread_invite_counts_wherever_he_is():
    """the-phone.md P9: after the sex step the thread becomes the loop invite. Her reply sets a flag
    the loop's trigger waits on."""
    g = routine_game(WEEKEND)
    g["phone"] = {"conversations": [{"id": "r_invite", "npc": "npc_r", "blocks": [
        {"choices": [{"text": "Come over.", "flagEffects": [{"flag": "r_invited", "op": "set"}]}]}]}]}
    g["canvases"][1]["trigger"]["conditions"] = {"version": "1.0", "logic": "AND", "items": [flag("r_invited")]}
    r = row(g, ROUTINE, routine_state())
    assert r["pass_"] is True and any("a phone invite" in d for d in r["detail"]), r


def test_a_ladder_with_no_loop_declared_fails():
    r = row(routine_game(EVENINGS), ROUTINE, routine_state(loop=()))
    assert r["pass_"] is False and "names no loop" in r["detail"][0], r


def test_a_loop_declared_none_is_not_judged():
    r = row(routine_game(EVENINGS), ROUTINE, routine_state(loop="none: he is her boss, it stays a tease"))
    assert r["na"] is True, r


def test_a_loop_that_is_not_explicit_fails():
    g = routine_game(EVENINGS)
    g["canvases"][1]["nodes"][0]["blocks"] = [{"type": "paragraph", "content": "You watch TV."}]
    r = row(g, ROUTINE, routine_state())
    assert r["pass_"] is False and any("no explicit beat" in d for d in r["detail"]), r


# ── a card line belongs to its person ────────────────────────────────────────
def card(npc, label, when=None, tip=""):
    return {"npc_id": npc, "text": "x", "tip": tip, "when": when or [],
            "goals": [{"type": "trait", "subject": "player", "trait": "heat", "op": "gte", "value": 20,
                       "label": label}]}


PEOPLE = [{"id": "npc_a", "name": "Ryan"}, {"id": "npc_b", "name": "Zoe"}, {"id": "npc_c", "name": "Jake"}]
MET = cv("meet", [nd("a", [ch("Hi.", flags=["a_met", "b_met", "c_met"])])], is_repeatable=False)


def test_one_list_pasted_onto_three_cards_fails():
    line = "Heat 20: stay and look: the park couple, the library stacks, a door left open"
    g = game(MET, npcs=PEOPLE, quest_cards=[card("npc_a", line), card("npc_b", line), card("npc_c", line)])
    r = row(g, CARD)
    assert r["pass_"] is False and "pasted onto 3 people's cards" in r["detail"][0], r


def test_a_card_naming_someone_unmet_fails():
    g = game(MET, npcs=PEOPLE, quest_cards=[card("npc_a", "Heat 60: get on the couch with him, pull Jake into the gym")])
    r = row(g, CARD)
    assert r["pass_"] is False and any("names Jake with no `c_met`" in d for d in r["detail"]), r


def test_own_lines_and_a_met_wait_pass():
    g = game(MET, npcs=PEOPLE, quest_cards=[
        card("npc_a", "Ryan's Lust 10: sit with him through the whole match on Sunday"),
        card("npc_b", "Zoe's Lust 10: come to her Friday party and stay past midnight, Jake too",
             when=[{"flag": "c_met", "op": "is_true"}])])
    r = row(g, CARD)
    assert r["pass_"] is True, r
    assert any("2 of 2 goal lines are her own meter target" in d for d in r["detail"]), r


# ── lint · the world around her ──────────────────────────────────────────────
def test_the_world_lint_counts_everyday_events_and_empty_places():
    g = game(cv("rain", [nd("a", [ch("Run for the bus.")], text="It starts to rain on the walk home.")],
                trigger_mode="random"),
             cv("towel", [nd("a", [ch("Go.")], text=EXPLICIT)], trigger_mode="random"),
             npcs=[{"id": "npc_a", "name": "Ryan",
                    "schedules": [{"location": "room", "weekdays": [0, 1, 2, 3, 4, 5, 6],
                                   "start_time": "08:00", "end_time": "24:00"}]}])
    model, g2 = gates.build(copy.deepcopy(g))
    summary, rows = gates.lint_world_life(model, g2)
    assert "1 of 2 events are everyday life" in summary, summary
    assert "park: nobody named can be here in any waking hour" in rows and not any(r.startswith("room:") for r in rows)


# ── lint · a loop names its hour (study 7_routine_time) ──────────────────────
def test_a_loop_act_that_names_the_dark_is_listed():
    g = routine_game(EVENINGS)
    g["canvases"][1]["nodes"][0]["blocks"] = [{"type": "paragraph", "content": "His room is dark. " + EXPLICIT}]
    model, g2 = gates.build(copy.deepcopy(g))
    summary, rows = gates.lint_loop_names_its_hour(model, g2, routine_state())
    assert "1 of 1" in summary and "names dark" in rows[0], (summary, rows)


def test_a_time_free_loop_act_is_not_listed():
    model, g2 = gates.build(copy.deepcopy(routine_game(EVENINGS)))
    summary, rows = gates.lint_loop_names_its_hour(model, g2, routine_state())
    assert rows == [] and "0 of 1" in summary, (summary, rows)


# ── lint · the climb's pace (study 10_pace) ─────────────────────────────────
def pace_game(caps):
    g = game()
    g["engine"] = {"daily_caps": {"heat": {"bands": [{"below": b, "cap": c} for b, c in caps]}}}
    return g


def test_a_one_a_day_band_makes_a_twenty_day_stage():
    summary, rows = gates.lint_climb_pace(pace_game([(20, 3), (40, 2), (101, 1)]), STATE)
    assert "heat 6.7 / 10 / 60" in summary, summary
    assert any(r.startswith("heat 40-99: 60 days at 1 a day") for r in rows), rows


def test_a_pace_of_two_or_three_a_day_lists_nothing():
    summary, rows = gates.lint_climb_pace(pace_game([(20, 3), (40, 2), (101, 5)]), STATE)
    assert rows == [], rows
