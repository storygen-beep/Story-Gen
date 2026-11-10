"""The group-2 checks (LO, 2026-11-03: fix the game-logic slips "with a check for each kind
that can come back"; "No new rules and no new content until it's done"). Each gate enforces a
rule the skill already states; the ids are the third alignment pass's rows
(~/Documents/Great_Games_Study_20260926/first_term_alignment_pass3_20261103.md).

  G75        a visit pays a meter once                the-arc.md A4d
  G74        an act pays on every way out             the-arc.md A4d · the-heat-ladder.md H5
  G8 · G13   an act pays no further than the next stage the-arc.md A4 · A4d
  A48        an act pays the meter it uses            the-heat-ladder.md "Two meters, one act"
  E95        a need falls where it says               the-meters.md M8
  J5 · J73   a deduction is gated or priced           engine.md §21
  H64 · H31  a closed activity says when it opens     the-clock.md C5 (extended)
  J37        a goal names the rung below              engine.md §47
  H48        a goal can flip                          the-voice.md
  G1         the last step opens a repeatable         the-arc.md A1 (+ lint `a set flag is read`)
  G12        an accident pays him                     the-arc.md A4d · the-heat-ladder.md H5
  G15        every stage has a way up (card places)   the-arc.md A4d
  E8         a step's gate sits above his start       the-meters.md "Whatever he keeps" 4
  F61        a no-show costs                          the-phone.md P5
  F60        ignoring a thread costs                  the-phone.md P5
  F69        a booking is read where she meets it     the-phone.md P10
  F72        the rent page can place its collector    the-economy.md · engine.md §26
  C24        nothing one-time at the shop or wardrobe the-first-hour.md F3
  C38        every card carries the met flag          the-first-hour.md, the cards' meeting flag
  C11        the skip sets what the opening sets      the-first-hour.md F1c
  B37        one asset, one block                     register.md
  J51        a refill place rolls an event            the-meters.md M8

Lints (lists, never a score): E94 a public act moves the audience · D52 the walk-in odds ride
her climb · D1 work inside a hub · F10 the rent is narrated once · F68 a thread books something
· C19 every live system is armed · G1 a set flag is read.

Fixtures are written here; nothing in games/ is read or written.
"""
import contextlib
import copy
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402

V1 = {"version": "1.0", "logic": "AND"}
BANDS = [{"min": 0, "text": "Low"}, {"min": 20, "text": "Mid"}, {"min": 40, "text": "High"}]
STATE = {"board": {"ascent_tiers": ["heat", "show"]}}


# ── fixture builders ─────────────────────────────────────────────────────────
def cond(*items):
    return dict(V1, items=list(items))


def trait(key, op, value, subject="player", npc=None):
    it = {"type": "trait", "subject": subject, "trait_key": key, "operator": op, "value": value}
    if npc:
        it["npc_id"] = npc
    return it


def flag(key, op="is_true"):
    return {"type": "flag", "subject": "player", "flag_key": key, "operator": op}


def pay(key, value=1, cap=None, **kw):
    ef = {"targetType": "player", "trait": key, "op": "add", "value": value}
    if cap is not None:
        ef["cap"] = cap
    ef.update(kw)
    return ef


def his(npc, key, value):
    return {"targetType": "npc", "npcId": npc, "trait": key, "op": "add", "value": value}


def ch(text, node=None, loc="room", eff=None, conds=None, flags=None, **kw):
    c = {"text": text}
    if node:
        c.update(targetType="node", nodeId=node)
    else:
        c.update(targetType="location", locationId=loc)
    if eff:
        c["effects"] = eff
    if conds:
        c["conditions"] = cond(*conds)
    if flags:
        c["flagEffects"] = [{"targetType": "player", "flag": f, "op": "set"} for f in flags]
    c.update(kw)
    return c


def nd(nid, choices, text="The room.", blocks=None):
    return {"id": nid, "blocks": blocks or [{"type": "paragraph", "content": text}],
            "exit_block": {"choices": choices}}


def cv(cid, nodes, **trig):
    t = {"location": "room", "is_repeatable": True}
    t.update(trig)
    return {"id": cid, "name": cid, "trigger": t, "nodes": nodes}


def game(*canvases, **extra):
    g = {"project": {"id": "fx", "name": "fx"},
         "player": {"core_traits": {"heat": 0, "show": 0, "energy": 50, "money": 0}},
         "sidebar_items": [{"trait": "heat", "bands": BANDS}, {"trait": "show", "bands": BANDS}],
         "locations": [{"id": "room", "name": "Room"}, {"id": "park", "name": "Park"},
                       {"id": "shop", "name": "Shop"}],
         "canvases": list(canvases)}
    g.update(extra)
    return g


def row(g, name, state=STATE):
    model, g2 = gates.build(copy.deepcopy(g))
    return next(r for r in gates.run_gates(model, g2, copy.deepcopy(state)) if r["gate"] == name)


def lints(g, state=STATE):
    model, g2 = gates.build(copy.deepcopy(g))
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        gates._group2_lints(model, g2, copy.deepcopy(state))
    return out.getvalue()


EXPLICIT = ("He fucks your wet cunt hard, his cock deep, your tits bouncing, and you come on his cock "
            "with his whole team watching.")


# ── G75 · a visit pays a meter once ──────────────────────────────────────────
VISIT = "a visit pays a meter once"


def test_two_raises_on_one_path_fail():
    g = game(cv("stacks", [nd("a", [ch("Move closer.", node="b", eff=[pay("heat", 1, 19)]),
                                    ch("Go.")]),
                           nd("b", [ch("Back to your desk.", eff=[pay("heat", 1, 19)])])]))
    r = row(g, VISIT)
    assert r["pass_"] is False and "stacks" in r["detail"][0], r


def test_one_raise_per_path_passes():
    g = game(cv("stacks", [nd("a", [ch("Move closer.", node="b"), ch("Go.")]),
                           nd("b", [ch("Back to your desk.", eff=[pay("heat", 1, 19)])])]))
    assert row(g, VISIT)["pass_"] is True


def test_an_act_menu_loop_is_two_visits_not_one_chain():
    g = game(cv("menu", [nd("m", [ch("Kiss him.", node="k", eff=[pay("heat", 1, 19)]), ch("Go.")]),
                         nd("k", [ch("Again.", node="m"), ch("Go.")])]))
    assert row(g, VISIT)["pass_"] is True


# ── G74 · an act pays on every way out ───────────────────────────────────────
EXITS = "an act pays on every way out"


def act_game(plain_conds=None):
    return game(cv("lockers", [
        nd("offer", [ch("Get on your knees.", node="act"), ch("Not here.")]),
        nd("act", [ch("Wipe your mouth. Go.", eff=[pay("heat", 1, 19)], conds=[flag("act_today", "is_false")],
                      flags=["act_today"]),
                   ch("Leave him to his shower.", conds=plain_conds)], text=EXPLICIT)]))


def test_an_unpaid_exit_beside_the_paid_one_fails():
    r = row(act_game(), EXITS)
    assert r["pass_"] is False and "lockers#act" in r["detail"][0], r


def test_an_unpaid_exit_shown_only_on_a_spent_day_passes():
    r = row(act_game(plain_conds=[flag("act_today", "is_true")]), EXITS)
    assert r["pass_"] is True, r


def test_a_decision_screen_with_a_way_out_is_not_an_act_screen():
    """The entry screen: go further (pays) or run (pays 0) is the accident's shape, A4d."""
    g = game(cv("towel", [nd("hall", [ch("Walk past slowly.", eff=[pay("heat", 1, 19)]),
                                      ch("Run to your room.")])]))
    assert row(g, EXITS)["na"] is True


# ── G8 · G13 · an act pays no further than the next stage ────────────────────
# PLAYTEST 2026-11-09: an act now pays on to the NEXT stage's top (a cap at her own top was the wall).
STAGE = "an act pays no further than the next stage"


def test_a_cap_above_the_next_stage_top_fails():
    """Opens at 0 (Low): the next stage, Mid, tops out at 39."""
    g = game(cv("gym", [nd("a", [ch("Let it slip.", eff=[pay("show", 1, 59)])])]))
    r = row(g, STAGE)
    assert r["pass_"] is False and "top 39" in r["detail"][0], r


def test_a_cap_at_the_next_stage_top_passes():
    g = game(cv("gym", [nd("a", [ch("Let it slip.", eff=[pay("show", 1, 59)], conds=[trait("show", "gte", 20)])])]))
    assert row(g, STAGE)["pass_"] is True


def test_an_upper_gate_inside_the_stage_holds_it():
    g = game(cv("gym", [nd("a", [ch("Let it slip.", eff=[pay("show", 1, 79)],
                                    conds=[trait("show", "gte", 20), trait("show", "lt", 59)])])]))
    assert row(g, STAGE)["pass_"] is True


def test_an_uncapped_raise_fails():
    g = game(cv("gym", [nd("a", [ch("Let it slip.", eff=[pay("show", 1)])])]))
    r = row(g, STAGE)
    assert r["pass_"] is False and "no cap" in r["detail"][0], r


# ── A48 · an act pays the meter it uses ──────────────────────────────────────
METER = "an act pays the meter it uses"


def test_gated_on_one_meter_paying_another_fails():
    g = game(cv("party", [nd("a", [ch("Kiss Zoe.", eff=[pay("show", 1, 39)], conds=[trait("heat", "gte", 20)])])]))
    r = row(g, METER)
    assert r["pass_"] is False and "Kiss Zoe" in r["detail"][0], r


def test_paying_the_meter_it_uses_passes():
    g = game(cv("party", [nd("a", [ch("Kiss Zoe.", eff=[pay("heat", 1, 39)], conds=[trait("heat", "gte", 20)])])]))
    assert row(g, METER)["pass_"] is True


def test_a_mixed_act_paying_one_of_its_meters_passes():
    g = game(cv("party", [nd("a", [ch("Kiss Zoe.", eff=[pay("show", 1, 39)],
                                     conds=[trait("heat", "gte", 20), trait("show", "gte", 20)])])]))
    assert row(g, METER)["pass_"] is True


# ── E95 · a need falls where it says ─────────────────────────────────────────
NEED = "a need falls where it says"


def need_game(sex_costs):
    eff = [pay("hygiene", -10)] if sex_costs else None
    return game(cv("bed_sex", [nd("a", [ch("Go.", eff=eff)], text=EXPLICIT)], requires_npc="npc_a"),
                cv("party_dance", [nd("a", [ch("Go.", eff=[pay("hygiene", -5)])])]),
                player={"core_traits": {"heat": 0, "show": 0, "hygiene": 50}, "trait_decay": {"hygiene": 5}})


NEED_STATE = {"board": {"ascent_tiers": ["heat", "show"],
                        "needs": [{"key": "hygiene", "falls": "a little every night; faster after parties and sex"}]}}


def test_a_need_that_never_falls_after_sex_fails():
    r = row(need_game(sex_costs=False), NEED, NEED_STATE)
    assert r["pass_"] is False and any("names sex" in d for d in r["detail"]), r


def test_a_need_that_falls_where_it_says_passes():
    assert row(need_game(sex_costs=True), NEED, NEED_STATE)["pass_"] is True


def test_a_nightly_fall_needs_the_decay_row():
    g = need_game(sex_costs=True)
    g["player"].pop("trait_decay")
    r = row(g, NEED, NEED_STATE)
    assert r["pass_"] is False and any("trait_decay" in d for d in r["detail"]), r


# ── J5 · J73 · a deduction is gated or priced ────────────────────────────────
DEDUCT = "a deduction is gated or priced"


def test_an_ungated_deduction_fails():
    g = game(cv("gym", [nd("a", [ch("Finish your set.", eff=[pay("energy", -10)])])]))
    r = row(g, DEDUCT)
    assert r["pass_"] is False and "energy" in r["detail"][0], r


def test_a_gated_a_priced_and_a_clamped_deduction_pass():
    g = game(cv("gym", [nd("a", [ch("Finish your set.", eff=[pay("energy", -10)], conds=[trait("energy", "gte", 10)]),
                                 ch("Buy a drink.", eff=[pay("money", -5)], costs=[{"trait": "money", "amount": 5}]),
                                 ch("Rest.", eff=[pay("energy", -1, clamp=True)])])]))
    assert row(g, DEDUCT)["pass_"] is True


def test_a_phone_reply_deduction_counts():
    g = game(cv("gym", [nd("a", [ch("Go.")])]),
             phone={"conversations": [{"id": "rent", "trigger": {}, "blocks": [
                 {"type": "reply", "round": 1, "choices": [{"text": "here", "effects": [pay("money", -20)]}]}]}]})
    assert row(g, DEDUCT)["pass_"] is False


# ── H64 · H31 · a closed activity says when it opens ─────────────────────────
CLOSED = "a closed activity says when it opens"
SCHED = [{"weekdays": [0, 1, 2], "start_time": "08:00", "end_time": "19:00"}]


def test_a_time_of_day_window_with_no_hours_fails():
    g = game(cv("counter", [nd("a", [ch("Go.")])],
                conditions=cond({"type": "time_of_day", "start_time": "22:00", "end_time": "02:00"})))
    r = row(g, CLOSED)
    assert r["pass_"] is False and "counter" in r["detail"][0], r


def test_a_time_of_day_window_with_its_hours_passes():
    g = game(cv("counter", [nd("a", [ch("Go.")])], show_when_blocked=True, cooldown_message="10 PM-2 AM",
                conditions=cond({"type": "time_of_day", "start_time": "22:00", "end_time": "02:00"})))
    assert row(g, CLOSED)["pass_"] is True


def test_a_windowed_event_stays_hidden():
    g = game(cv("counter", [nd("a", [ch("Go.")])], metadata={"kind": "event"},
                conditions=cond({"type": "time_of_day", "start_time": "22:00", "end_time": "02:00"})),
             cv("shift", [nd("a", [ch("Go.")])], schedules=SCHED, show_when_blocked=True,
                cooldown_message="Mon-Wed, 8 AM-7 PM"))
    assert row(g, CLOSED)["pass_"] is True


def test_a_cooldown_with_no_hour_or_day_fails():
    g = game(cv("shift", [nd("a", [ch("Go.")])], schedules=SCHED, show_when_blocked=True,
                cooldown_message="No more shifts today."))
    r = row(g, CLOSED)
    assert r["pass_"] is False and "names no hour" in r["detail"][0], r


# ── J37 · a goal names the rung below ────────────────────────────────────────
RUNG = "a goal names the rung below"


def goal_game(gate_value):
    return game(cv("stacks", [nd("a", [ch("Move one aisle closer.", eff=[pay("heat", 1, 19)],
                                          conds=[trait("heat", "gte", gate_value)])])]),
                quest_cards=[{"text": "x", "goals": [{"trait": "heat", "op": "gte", "value": 5,
                                                      "label": "Heat 5: move one aisle closer in the stacks"}]}])


def test_a_goal_naming_its_own_gate_fails():
    r = row(goal_game(5), RUNG)
    assert r["pass_"] is False and "Move one aisle closer" in r["detail"][0], r


def test_a_goal_naming_the_rung_below_passes():
    assert row(goal_game(0), RUNG)["pass_"] is True


# ── H48 · a goal can flip ────────────────────────────────────────────────────
FLIP = "a goal can flip"


def flip_game(goal):
    return game(cv("gym", [nd("a", [ch("Go.", eff=[pay("heat", 1, 79)])])]),
                quest_cards=[{"text": "x", "goals": [{"trait": "heat", "op": "gte", "value": goal, "label": "Heat"}]}])


def test_a_goal_above_every_cap_fails():
    r = row(flip_game(80), FLIP)
    assert r["pass_"] is False and "79" in r["detail"][0], r


def test_a_goal_inside_the_caps_passes():
    assert row(flip_game(60), FLIP)["pass_"] is True


# ── G1 · the last step opens a repeatable, and the lint `a set flag is read` ─
LAST = "the last step opens a repeatable"


def ladder_game(repeatable_reads):
    rep_conds = [trait("tom_step", "gte", 2)] if repeatable_reads else [flag("other")]
    return game(cv("tom_01", [nd("a", [ch("Yes.", eff=[{"targetType": "player", "trait": "tom_step", "op": "set",
                                                         "value": 1}])])], is_repeatable=False),
                cv("tom_02", [nd("a", [ch("Yes.", flags=["tom_rule"],
                                          eff=[{"targetType": "player", "trait": "tom_step", "op": "set", "value": 2}])])],
                   is_repeatable=False),
                cv("tom_loop", [nd("a", [ch("Go.")])], conditions=cond(*rep_conds)))


LADDER_STATE = {"board": {"ascent_tiers": ["heat", "show"], "characters": [
    {"id": "npc_tom", "ladder": {"counter": "tom_step", "steps": [{"n": 1, "canvas": "tom_01"},
                                                                  {"n": 2, "canvas": "tom_02"}]}}]}}


def test_a_ladder_that_ends_on_nothing_fails():
    r = row(ladder_game(False), LAST, LADDER_STATE)
    assert r["pass_"] is False and "npc_tom" in r["detail"][0], r


def test_a_ladder_that_ends_on_a_repeatable_passes():
    assert row(ladder_game(True), LAST, LADDER_STATE)["pass_"] is True


def test_the_lint_lists_a_flag_nothing_reads():
    out = lints(ladder_game(False), LADDER_STATE)
    assert "lint · a set flag is read" in out and "tom_rule" in out, out


# ── G12 · an accident pays him ───────────────────────────────────────────────
ACCIDENT = "an accident pays him"
NPCS = [{"id": "npc_ryan", "name": "Ryan", "core_traits": {"want": 0}}]


def accident_game(raise_him):
    eff = [his("npc_ryan", "want", 2)] if raise_him else None
    return game(cv("towel", [nd("a", [ch("Walk past slowly.", eff=eff), ch("Run.")])], trigger_mode="random",
                   conditions=cond({"type": "npc_at_location", "npc_id": "npc_ryan", "location_id": "room",
                                    "operator": "is_present"})), npcs=NPCS)


def test_an_accident_that_raises_nothing_fails():
    r = row(accident_game(False), ACCIDENT)
    assert r["pass_"] is False and "towel" in r["detail"][0], r


def test_an_accident_that_raises_him_passes():
    assert row(accident_game(True), ACCIDENT)["pass_"] is True


# ── G15 · every stage has a way up: a card names a place that does not pay ──
WAYUP = "every stage has a way up"


def wayup_game(card_place):
    return game(cv("park_walk", [nd("a", [ch("Flash.", eff=[pay("show", 1, 39)])])], location="park"),
                cv("park_more", [nd("a", [ch("Flash.", eff=[pay("show", 1, 39)], conds=[trait("show", "gte", 20)])])],
                   location="park"),
                cv("shop_try", [nd("a", [ch("Go.", eff=[pay("show", 1, 39)], conds=[trait("show", "gte", 20)])])],
                   location="shop"),
                quest_cards=[{"text": "x", "goals": [{"trait": "show", "op": "gte", "value": 20,
                                                      "label": f"Reach Mid (Show 20): the {card_place}"}]}])


def test_a_card_naming_a_place_that_pays_nothing_there_fails():
    r = row(wayup_game("shop"), WAYUP, {"board": {"ascent_tiers": ["show"]}})
    assert r["pass_"] is False and any("shop pays nothing" in d for d in r["detail"]), r


def test_a_card_naming_a_paying_place_passes():
    r = row(wayup_game("park"), WAYUP, {"board": {"ascent_tiers": ["show"]}})
    assert r["pass_"] is True, r


# ── E8 · a step's gate sits above his start ──────────────────────────────────
START = "a step's gate sits above his start"


def start_game(start):
    return game(cv("ryan_02", [nd("a", [ch("Go.")])], is_repeatable=False,
                   conditions=cond(trait("want", "gte", 10, subject="npc", npc="npc_ryan"))),
                npcs=[{"id": "npc_ryan", "name": "Ryan", "core_traits": {"want": start}}])


def test_a_gate_met_at_the_start_fails():
    r = row(start_game(20), START)
    assert r["pass_"] is False and "starts at 20" in r["detail"][0], r


def test_a_gate_above_the_start_passes():
    assert row(start_game(0), START)["pass_"] is True


def test_a_step_that_pays_past_the_next_gate_fails():
    g = game(cv("s1", [nd("a", [ch("Go.", eff=[his("npc_ryan", "want", 25)])])], is_repeatable=False,
                conditions=cond(trait("want", "gte", 5, subject="npc", npc="npc_ryan"))),
             cv("s2", [nd("a", [ch("Go.")])], is_repeatable=False,
                conditions=cond(trait("want", "gte", 20, subject="npc", npc="npc_ryan"))),
             npcs=[{"id": "npc_ryan", "name": "Ryan", "core_traits": {"want": 0}}])
    r = row(g, START)
    assert r["pass_"] is False and "already meets" in r["detail"][0], r


# ── F61 · F60 · F69 · the phone's bookings ───────────────────────────────────
def thread(tid, replies, trig=None, **kw):
    d = {"id": tid, "npc": "npc_jake", "trigger": {"conditions": cond(*(trig or []))},
         "blocks": [{"type": "message", "sender": "npc", "content": "sat?"},
                    {"type": "reply", "round": 1, "choices": replies}]}
    d.update(kw)
    return d


NOSHOW_TRIG = [flag("date_booked"), {"type": "hours_since_flag", "subject": "player", "flag_key": "date_booked",
                                     "operator": "gte", "value": 72}]
UNSET = [{"targetType": "player", "flag": "date_booked", "op": "unset"}]
COST = [his("npc_jake", "want", -5)]


def phone_game(*threads, date_reads=True):
    rd = [flag("date_booked")] if date_reads else [flag("other")]
    return game(cv("date", [nd("a", [ch("Go.", conds=rd)])]), phone={"conversations": list(threads)})


def test_a_free_no_show_fails():
    g = phone_game(thread("noshow", [{"text": "sorry", "flagEffects": UNSET}], NOSHOW_TRIG,
                          ignore_after_days=1, on_ignore={"flagEffects": UNSET}))
    r = row(g, "a no-show costs")
    assert r["pass_"] is False and "noshow" in r["detail"][0], r


def test_a_no_show_that_costs_passes():
    g = phone_game(thread("noshow", [{"text": "sorry", "flagEffects": UNSET, "effects": COST}], NOSHOW_TRIG,
                          ignore_after_days=1, on_ignore={"flagEffects": UNSET, "effects": COST}))
    assert row(g, "a no-show costs")["pass_"] is True


def booking(**kw):
    return thread("date", [{"text": "yes", "flagEffects": [{"targetType": "player", "flag": "date_booked",
                                                            "op": "set"}]}, {"text": "no"}], **kw)


def test_a_booking_thread_with_no_ignore_cost_fails():
    r = row(phone_game(booking()), "ignoring a thread costs")
    assert r["pass_"] is False and "date" in r["detail"][0], r


def test_a_booking_thread_that_costs_when_ignored_passes():
    g = phone_game(booking(ignore_after_days=1, on_ignore={"effects": COST}))
    assert row(g, "ignoring a thread costs")["pass_"] is True


def test_a_booking_only_its_no_show_reads_fails():
    r = row(phone_game(booking(), date_reads=False), "a booking is read where she meets it")
    assert r["pass_"] is False and "date_booked" in r["detail"][0], r


def test_a_booking_a_canvas_reads_passes():
    assert row(phone_game(booking()), "a booking is read where she meets it")["pass_"] is True


# ── F72 · the rent page can place its collector ──────────────────────────────
RENT = "the rent page can place its collector"


def rent_game(scene, rows):
    return game(cv("x", [nd("a", [ch("Go.")])]),
                npcs=[{"id": "npc_mark", "name": "Mark", "schedules": rows}],
                settings={"rent": {"enabled": True, "due_day": "Sunday", "collector_npc": "npc_mark",
                                   "text": {"scene": scene}}})


SPLIT = [{"location": "bedroom", "weekdays": [6], "start_time": "00:00", "end_time": "08:00"},
         {"location": "kitchen", "weekdays": [6], "start_time": "08:00", "end_time": "00:00"}]


def test_a_rent_scene_that_places_him_fails():
    r = row(rent_game("Mark is at the kitchen table with an envelope.", SPLIT), RENT)
    assert r["pass_"] is False and "Mark" in r["detail"][0], r


def test_a_rent_scene_without_him_passes():
    assert row(rent_game("The envelope is on the table.", SPLIT), RENT)["pass_"] is True


# ── C24 · nothing one-time at the shop or wardrobe ───────────────────────────
SHOP = "nothing one-time at the shop or wardrobe"


def test_a_one_time_canvas_in_the_shop_room_fails():
    g = game(cv("job_ask", [nd("a", [ch("Go.")])], location="shop", is_repeatable=False),
             settings={"shop_location": "shop"})
    r = row(g, SHOP)
    assert r["pass_"] is False and "job_ask" in r["detail"][0], r


def test_a_repeatable_in_the_shop_room_passes():
    g = game(cv("browse", [nd("a", [ch("Go.")])], location="shop"), settings={"wardrobe_location": ["shop"]})
    assert row(g, SHOP)["pass_"] is True


# ── C38 · every card carries the met flag ────────────────────────────────────
MET = "every card carries the met flag"


def met_game(pointer_when):
    return game(cv("hale_meet", [nd("a", [ch("Go.", flags=["hale_met"])])], is_repeatable=False),
                quest_cards=[{"npc_id": "npc_hale", "heading": "Your lecturer", "text": "x", "when": pointer_when},
                             {"npc_id": "npc_hale", "text": "y", "when": [{"flag": "hale_met", "op": "is_true"}]}])


def test_a_pointer_card_without_the_met_flag_fails():
    r = row(met_game([{"flag": "opening_done", "op": "is_true"}]), MET)
    assert r["pass_"] is False and "Your lecturer" in r["detail"][0], r


def test_every_card_with_the_met_flag_passes():
    assert row(met_game([{"flag": "hale_met", "op": "is_false"}]), MET)["pass_"] is True


# ── C11 · the skip sets what the opening sets ────────────────────────────────
SKIP = "the skip sets what the opening sets"


def opening_game(skip_flags):
    return game(cv("opening", [
        nd("wake", [ch("Skip the opening.", node="skip_card", flags=["rent_starts"]),
                    ch("Get up.", node="breakfast", flags=["rent_starts"])]),
        nd("breakfast", [ch("For the grades.", node="card", flags=["for_grades"]),
                         ch("For fun.", node="card", flags=["for_fun"])]),
        nd("skip_card", [ch("Go.", flags=skip_flags)]),
        nd("card", [ch("Go.", flags=["opening_done"])])], is_repeatable=False),
        project={"id": "fx", "name": "fx", "starting_canvas": "opening"})


def test_a_skip_that_misses_a_branch_fails():
    r = row(opening_game(["opening_done"]), SKIP)
    assert r["pass_"] is False and any("breakfast" in d for d in r["detail"]), r


def test_a_skip_that_misses_an_always_flag_fails():
    r = row(opening_game(["for_grades"]), SKIP)
    assert r["pass_"] is False and any("opening_done" in d for d in r["detail"]), r


def test_a_skip_that_takes_one_branch_passes():
    assert row(opening_game(["opening_done", "for_grades"]), SKIP)["pass_"] is True


# ── B37 · one asset, one block ───────────────────────────────────────────────
ASSET = "one asset, one block"


def media(pool):
    return [{"type": "video", "props": {"pool_dir": pool}}, {"type": "paragraph", "content": "x"}]


def test_one_pool_in_two_blocks_fails():
    g = game(cv("a", [nd("n", [ch("Go.")], blocks=media("sex/towel_t4"))]),
             cv("b", [nd("n", [ch("Go.")], blocks=media("sex/towel_t4"))]))
    r = row(g, ASSET)
    assert r["pass_"] is False and "sex/towel_t4" in r["detail"][0], r


def test_each_block_its_own_pool_passes():
    g = game(cv("a", [nd("n", [ch("Go.")], blocks=media("sex/towel_a_t4"))]),
             cv("b", [nd("n", [ch("Go.")], blocks=media("sex/towel_b_t4"))]))
    assert row(g, ASSET)["pass_"] is True


# ── J51 · a refill place rolls an event ──────────────────────────────────────
REFILL = "a refill place rolls an event"
REFILL_STATE = {"board": {"ascent_tiers": ["heat", "show"], "needs": [{"key": "hygiene"}]}}


def refill_game(subs):
    t = {"substitutions": [{"target_canvas_id": "walkin", "chance": 0.25}]} if subs else {}
    return game(cv("wash", [nd("a", [ch("Go.", eff=[pay("hygiene", 15)])])], **t),
                cv("walkin", [nd("a", [ch("Go.")])], substitution_only=True))


def test_a_refill_with_no_event_fails():
    r = row(refill_game(False), REFILL, REFILL_STATE)
    assert r["pass_"] is False and "wash" in r["detail"][0], r


def test_a_refill_that_rolls_a_walk_in_passes():
    assert row(refill_game(True), REFILL, REFILL_STATE)["pass_"] is True


# ── the group-2 lints ────────────────────────────────────────────────────────
def test_lint_a_public_act_moves_the_audience():
    st = {"board": {"ascent_tiers": ["heat"], "meters": [{"id": "campus_talk", "key": "campus_talk"}]}}
    g = game(cv("quad", [nd("a", [ch("Go.", eff=[pay("heat", 1, 19)])], text=EXPLICIT)]))
    assert "lint · a public act moves the audience" in lints(g, st)
    g2 = game(cv("quad", [nd("a", [ch("Go.", eff=[pay("campus_talk", 1)])], text=EXPLICIT)]))
    assert "a public act moves the audience" not in lints(g2, st)


def test_lint_the_walk_in_odds_ride_her_climb():
    flat = game(cv("shower", [nd("a", [ch("Go.")])], substitutions=[{"target_canvas_id": "w", "chance": 0.25}]),
                cv("w", [nd("a", [ch("Go.")])], substitution_only=True))
    assert "lint · the walk-in odds ride her climb" in lints(flat)
    banded = game(cv("shower", [nd("a", [ch("Go.")])], substitutions=[
        {"target_canvas_id": "w", "chance": 0.1, "conditions": cond(trait("heat", "lt", 20))},
        {"target_canvas_id": "w", "chance": 0.4, "conditions": cond(trait("heat", "gte", 20))}]),
        cv("w", [nd("a", [ch("Go.")])], substitution_only=True))
    assert "walk-in odds" not in lints(banded)


def test_lint_work_inside_a_hub():
    g = game(cv("hub_laura", [nd("a", [ch("Study.", eff=[pay("grade_psych", 1)])])], npc="npc_laura"),
             player={"core_traits": {"heat": 0, "show": 0, "grade_psych": 0}})
    assert "lint · work inside a hub" in lints(g)


def test_lint_the_rent_is_narrated_once():
    g = game(cv("sunday", [nd("a", [ch("Go.")], text="He licks his thumb and counts it again.")]),
             settings={"rent": {"enabled": True}})
    assert "lint · the rent is narrated once" in lints(g)


def test_lint_a_thread_books_something():
    g = game(cv("x", [nd("a", [ch("Go.")])]),
             phone={"conversations": [thread("chat", [{"text": "lol", "effects": [his("npc_jake", "want", 1)]}])]})
    assert "lint · a thread books something" in lints(g)


def test_lint_every_live_system_is_armed():
    st = {"board": {"ascent_tiers": ["heat"], "systems": [{"id": "parties", "name": "Parties"},
                                                          {"id": "college", "name": "College"}]}}
    g = game(cv("opening", [nd("a", [ch("Go.")], text="College starts Monday.")], is_repeatable=False),
             project={"id": "fx", "name": "fx", "starting_canvas": "opening"})
    out = lints(g, st)
    assert "lint · every live system is armed" in out and "parties" in out and "college:" not in out, out


def test_lint_work_inside_a_hub_lists_a_chore():
    g = game(cv("hub_mark", [nd("a", [ch("Do your laundry.", node="l")]),
                             nd("l", [ch("Done.", costs=[{"trait": "energy", "value": 5}],
                                         time_progression_minutes=30)])], npc="npc_mark"))
    out = lints(g)
    assert "lint · work inside a hub" in out and "a chore" in out, out


def test_deduction_on_a_meter_read_below_zero_is_left_alone():
    """Pass 4 (2026-11-04): cafe_name falls on purpose; a step reads it at lte -5, so no clamp."""
    import copy
    g = {"project": {"id": "fx", "name": "fx"}, "locations": [{"id": "cafe"}],
         "player": {"core_traits": {"cafe_name": 0}},
         "canvases": [
             {"id": "shift", "trigger": {"location": "cafe", "is_repeatable": True}, "nodes": [
                 {"id": "n", "blocks": [{"type": "paragraph", "content": "A shift."}],
                  "exit_block": {"choices": [{"text": "Clock out.", "targetType": "location", "locationId": "cafe",
                                              "effects": [{"targetType": "player", "trait": "cafe_name", "op": "add",
                                                           "value": -1, "clamp": False}]}]}}]},
             {"id": "tom3", "trigger": {"location": "cafe", "is_repeatable": False, "conditions": {
                 "version": "1.0", "logic": "AND", "items": [{"type": "trait", "subject": "player",
                 "trait_key": "cafe_name", "operator": "lte", "value": -5}]}},
              "nodes": [{"id": "n", "blocks": [{"type": "paragraph", "content": "Tom."}]}]}]}
    model, g2 = gates.build(copy.deepcopy(g))
    r = next(r for r in gates.run_gates(model, g2, {}) if r["gate"] == "a deduction is gated or priced")
    assert not r["detail"] and "below 0" not in r["headline"], r
