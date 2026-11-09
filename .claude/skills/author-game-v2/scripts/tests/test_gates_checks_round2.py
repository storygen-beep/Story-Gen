"""Checker false alarms found on first_term after the group-2 checks (2026-11-03, round 2).
LO: "No new rules and no new content until it's done", so each fix makes a check read the game
the way the skill already says, and each keeps the hit it was written for.

  1. no canvas key is discarded — `kind = "event"` under [canvases.trigger.metadata] is the
     skill's own marker (the-clock.md C5); the importer drops it on purpose and the gates read it.
  2. a named person is where the line says — a voice out of a phone is a call, not a person in
     the room; "Kayla's at her mom's tonight" says she is away, not here.
  3. an act pays on every way out — a choice into a node of ANOTHER canvas goes further; the
     screen that offers it is a decision screen, not the screen after the act.
  4. an act pays no further than the next stage — an act gated on a ladder step or a flag opens no lower
     than the exits that set that step or flag (followed back through their own waits).
  5. every stage has a way up (card places) — a goal line is live from the rung below it (the
     card's previous goal on that meter), and a building pays when a room inside it pays.
  6. the rent page can place its collector — "Mark's text came in at midnight" names him
     without putting him in front of her.

Fixtures only; nothing in games/ is read or written.
"""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402
import test_gates_ck7 as ck7  # noqa: E402
import test_gates_group2_checks as g2t  # noqa: E402
import test_gates_k7_false_alarms as k7  # noqa: E402

from test_gates_group2_checks import ch, cond, cv, flag, game, nd, pay, trait  # noqa: E402

ALL = [0, 1, 2, 3, 4, 5, 6]


def lo_row(g, name):
    model, g2 = gates.build(copy.deepcopy(g))
    return next(r for r in gates.run_gates(model, g2, None) if r["gate"] == name)


# ── 1. `kind = "event"` under [canvases.trigger.metadata] ────────────────────
DISCARD = "no canvas key is discarded"


def test_the_event_marker_is_not_a_discarded_key():
    c = ck7.canvas("desk_guy", "lecture_hall", metadata={"kind": "event"})
    r = lo_row(ck7.game([{"id": "lecture_hall"}], [c]), DISCARD)
    assert r["pass_"] is True, r
    assert not any("kind" in d for d in r["detail"]), r


def test_another_metadata_key_beside_the_marker_is_still_flagged():
    c = ck7.canvas("desk_guy", "lecture_hall", metadata={"kind": "event", "cooldown_message": "Mon 8:30"})
    r = lo_row(ck7.game([{"id": "lecture_hall"}], [c]), DISCARD)
    assert r["pass_"] is False
    assert any("`cooldown_message`" in d for d in r["detail"]) and not any("`kind`" in d for d in r["detail"])


def test_a_kind_that_is_not_the_event_marker_is_still_flagged():
    c = ck7.canvas("desk_guy", "lecture_hall", metadata={"kind": "activity"})
    r = lo_row(ck7.game([{"id": "lecture_hall"}], [c]), DISCARD)
    assert r["pass_"] is False and any("`kind` under [canvases.trigger.metadata]" in d for d in r["detail"])


# ── 2. a named person is where the line says: a phone voice, an away line ────
def kayla_game(text, kayla_room="cafe"):
    """The k7 home; Kayla is at `kayla_room` all day; the line shows in Ella's room."""
    g = k7.house_game([k7.para(text)])
    g["npcs"] = [{"id": "npc_kayla", "name": "Kayla", "schedules": [
        {"location": kayla_room, "weekdays": ALL, "start_time": "00:00", "end_time": "24:00",
         "activity": "working"}]}]
    return g


def kayla_rows(g):
    ok, _, detail = gates._named_person_present(g)
    return ok, [d for d in detail if "Kayla" in d]


def test_a_voice_from_the_phone_does_not_place_her():
    for line in ("Kayla's voice buzzes small from the phone.",
                 "Kayla's voice, small and sharp out of the phone.",
                 "Kayla's voice comes on speaker."):
        ok, rows = kayla_rows(kayla_game(line))
        assert ok is not False and not rows, (line, rows)


def test_a_voice_with_no_phone_still_places_her():
    ok, rows = kayla_rows(kayla_game("Kayla's voice comes from the kitchen."))
    assert ok is False and rows and "not here" in rows[0], rows


def test_at_her_moms_says_she_is_away():
    ok, rows = kayla_rows(kayla_game("Kayla's at her mom's tonight."))
    assert ok is not False and not rows, rows


def test_at_her_moms_while_her_rows_hold_her_here_is_still_red():
    ok, rows = kayla_rows(kayla_game("Kayla's at her mom's tonight.", kayla_room="ella_room"))
    assert ok is False and rows and "not out" in rows[0], rows


def test_in_the_room_while_her_rows_hold_her_away_is_still_red():
    ok, rows = kayla_rows(kayla_game("Kayla's in the doorway, grinning."))
    assert ok is False and rows, rows


# ── 3. an act pays on every way out: a choice into another canvas goes on ────
EXITS = "an act pays on every way out"


def laundry_game(further):
    """A walk-in's screen: the plain way out, and a gated button further. `further` is the
    further button's target: a node in another canvas (goes on) or a location (a way out)."""
    go_on = ch("Bend for the bottom drum.", eff=[pay("show", 1, 39)], conds=[trait("show", "gte", 20)])
    if further == "other canvas":
        go_on.update(targetType="node", nodeId="garage_hub.tease")
    return game(cv("walkin", [nd("moment", [ch("He stops in the doorway.", node="answer")]),
                              nd("answer", [ch("Load it and go."), go_on], text=g2t.EXPLICIT)]),
                cv("garage_hub", [nd("hub", [ch("Go.")]), nd("tease", [ch("Go.")])]))


def test_a_button_into_another_canvas_makes_a_decision_screen():
    r = g2t.row(laundry_game("other canvas"), EXITS)
    assert r["na"] is True and not r["detail"], r     # no act screen: nothing to judge


def test_the_same_button_as_a_way_out_is_still_red():
    r = g2t.row(laundry_game("location"), EXITS)
    assert r["pass_"] is False and "walkin#answer" in r["detail"][0], r


# ── 4. an act pays no further than the next stage: a ladder step's floor ─────
# PLAYTEST 2026-11-09: an act now pays on to the NEXT stage's top (a cap at her own top was the wall).
STAGE = "an act pays no further than the next stage"


def ladder_game(step_gate, cap=39):
    """Step 2 is set behind heat `step_gate`; the repeatable act waits on step 2 and pays heat
    capped at `cap` (39 is the Mid stage's top)."""
    step = lambda key, v: {"targetType": "player", "trait": key, "op": "set", "value": v}  # noqa: E731
    return game(cv("step_1", [nd("a", [ch("Yes.", eff=[step("ryan_step", 1)])])], is_repeatable=False),
                cv("step_2", [nd("a", [ch("Yes.", eff=[step("ryan_step", 2)])])], is_repeatable=False,
                   conditions=cond(trait("ryan_step", "eq", 1), trait("heat", "gte", step_gate))),
                cv("knocks", [nd("a", [ch("Back to your room.", eff=[pay("heat", 1, cap)])])],
                   conditions=cond(trait("ryan_step", "eq", 2))),
                player={"core_traits": {"heat": 0, "show": 0, "energy": 50, "money": 0, "ryan_step": 0}})


def test_an_act_behind_a_step_opens_at_the_steps_gate():
    assert g2t.row(ladder_game(20), STAGE)["pass_"] is True


def test_an_act_behind_a_step_set_at_zero_is_still_red():
    r = g2t.row(ladder_game(0, cap=59), STAGE)          # opens at 0: the next top is 39
    assert r["pass_"] is False and "opens at heat 0" in r["detail"][0], r


def test_the_floor_follows_the_setters_own_wait():
    """Step 3 is set at heat 0, but only after step 2, which waits on heat 20."""
    g = ladder_game(20)
    g["canvases"].insert(2, cv("step_3", [nd("a", [ch("Yes.", eff=[
        {"targetType": "player", "trait": "ryan_step", "op": "set", "value": 3}])])], is_repeatable=False,
        conditions=cond(trait("ryan_step", "eq", 2))))
    g["canvases"][-1]["trigger"]["conditions"] = cond(trait("ryan_step", "gte", 3))
    assert g2t.row(g, STAGE)["pass_"] is True


def test_a_flag_set_only_behind_a_gate_carries_the_gate():
    g = game(cv("meet", [nd("a", [ch("Yes.", flags=["jake_number"])])], is_repeatable=False,
                conditions=cond(trait("heat", "gte", 20))),
             cv("gym", [nd("a", [ch("Let him fix your squat.", eff=[pay("heat", 1, 39)])])],
                conditions=cond(flag("jake_number"))))
    assert g2t.row(g, STAGE)["pass_"] is True


# ── 5. every stage has a way up: a card line at the rung below ───────────────
WAYUP = "every stage has a way up"
SHOW = {"board": {"ascent_tiers": ["show"]}}


def card_game(goals, home_rooms=False):
    """Show pays at the park from 0; the shop's curtain pays only from show 10, capped 19; the
    shower in the house pays from 10. Show stages: 0, 20, 40 (g2t.BANDS)."""
    g = game(cv("park_walk", [nd("a", [ch("Flash.", eff=[pay("show", 1, 39)])])], location="park"),
             cv("park_more", [nd("a", [ch("Flash.", eff=[pay("show", 1, 39)], conds=[trait("show", "gte", 20)])])],
                location="park"),
             cv("curtain", [nd("a", [ch("Leave it open.", eff=[pay("show", 1, 19)],
                                       conds=[trait("show", "gte", 10)])])], location="shop"),
             cv("shower", [nd("a", [ch("Leave the door unlocked.", eff=[pay("show", 1, 19)],
                                      conds=[trait("show", "gte", 10)])])], location="bathroom"),
             quest_cards=[{"text": "x", "goals": [
                 {"trait": "show", "op": "gte", "value": v, "label": lab} for v, lab in goals]}])
    g["locations"] += [{"id": "house", "name": "Home", "is_container": True, "default_entry": "bathroom"},
                       {"id": "bathroom", "name": "Bathroom", "parent": "house"}]
    return g


def test_a_line_is_judged_at_the_rung_below_it():
    g = card_game([(10, "Show 10: flash at the park"), (15, "Show 15: leave the curtain open at the shop")])
    r = g2t.row(g, WAYUP, SHOW)
    assert r["pass_"] is True, r["detail"][:3]


def test_a_line_with_no_rung_below_is_judged_at_the_stage_floor():
    r = g2t.row(card_game([(15, "Show 15: leave the curtain open at the shop")]), WAYUP, SHOW)
    assert r["pass_"] is False and any("shop pays nothing toward show at 0" in d for d in r["detail"]), r


def test_a_building_pays_when_a_room_in_it_pays():
    g = card_game([(10, "Show 10: flash at the park"), (20, "Reach Mid (Show 20): the shower at home")])
    r = g2t.row(g, WAYUP, SHOW)
    assert r["pass_"] is True, r["detail"][:3]


def test_a_building_where_no_room_pays_is_still_red():
    g = card_game([(5, "Show 5: flash at the park"), (10, "Show 10: the shower at home")])
    r = g2t.row(g, WAYUP, SHOW)
    assert r["pass_"] is False and any("house pays nothing toward show at 5" in d for d in r["detail"]), r


# ── 6. the rent page can place its collector: his text is not him ────────────
RENT = "the rent page can place its collector"


def test_his_text_does_not_put_him_in_front_of_her():
    g = g2t.rent_game("Mark's text came in at midnight on the dot. It's Sunday, and he wants his money.",
                      g2t.SPLIT)
    assert g2t.row(g, RENT)["pass_"] is True


def test_his_text_beside_him_in_the_room_is_still_red():
    g = g2t.rent_game("Mark's text came in at midnight. Mark is at the table now.", g2t.SPLIT)
    assert g2t.row(g, RENT)["pass_"] is False
