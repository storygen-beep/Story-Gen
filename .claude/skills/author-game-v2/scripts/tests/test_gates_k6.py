"""The gates LO asked for on 2026-11-03 ("Any of these that can come back gets a gate"):

  a goal's end is built             a goal with `ends_in_release` N > 1 is a later release's end;
  no one is named before they're met  location descriptions and description variants are read;
  a no never raises his Want        a refusal, an exit away from him or a final no adds 0 Want;
  a booking can clear               a booking flag has an unset outside its hours_since window;
  a closed activity says when it opens  a solo scheduled activity keeps its row and its hours;
  speech is a dialog block          no quoted spoken line inside a `paragraph`.

Fixtures are written here; nothing in games/ is read or written.
"""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402

V1 = {"version": "1.0", "logic": "AND"}


def row(game, state, name):
    model, g2 = gates.build(copy.deepcopy(game))
    return next(r for r in gates.run_gates(model, g2, state) if r["gate"] == name)


def para(text, **props):
    b = {"type": "paragraph", "content": text}
    if props:
        b["props"] = props
    return b


def canvas(cid, blocks=None, choices=None, **trigger):
    trig = {"location": "room", "is_repeatable": True}
    trig.update(trigger)
    node = {"id": "n", "blocks": blocks or [para("You stand there.")]}
    if choices:
        node["exit_block"] = {"choices": choices}
    return {"id": cid, "trigger": trig, "nodes": [node]}


def game(canvases=None, **extra):
    g = {"project": {"id": "fx", "name": "fx"}, "player": {"core_traits": {"heat": 0}},
         "locations": [{"id": "room", "name": "Room", "description": "A room."}],
         "npcs": [{"id": "npc_ryan", "name": "Ryan"}],
         "canvases": canvases or [canvas("c0")]}
    g.update(extra)
    return g


def flag_cond(flag, op="is_true"):
    return {"type": "flag", "subject": "player", "flag_key": flag, "operator": op}


def hours(flag, op, v):
    return {"type": "hours_since_flag", "subject": "player", "flag_key": flag, "operator": op, "value": v}


def conds(*items):
    return dict(V1, items=list(items))


# ── 1. a goal's end is built: `ends_in_release` ─────────────────────────────
GOAL = "a goal's end is built"


def goal_state(*goals):
    return {"want": {"promise": {"goals": list(goals)}}}


def test_a_goal_ending_this_release_with_no_setter_still_fails():
    st = goal_state({"goal": "pay the rent", "ends_when": "x", "ends_flag": "rent_paid"},
                    {"goal": "last", "next": "-"})
    assert row(game(), st, GOAL)["pass_"] is False


def test_a_later_release_goal_is_skipped_and_listed():
    st = goal_state({"goal": "her name on campus", "ends_when": "x", "ends_flag": "famous",
                     "ends_in_release": 2},
                    {"goal": "last", "next": "-"})
    r = row(game(), st, GOAL)
    assert r["na"] is True
    assert any("ends in release 2" in d for d in r["detail"])


def test_release_one_is_not_a_later_release():
    st = goal_state({"goal": "pay", "ends_when": "x", "ends_flag": "paid", "ends_in_release": 1},
                    {"goal": "last", "next": "-"})
    assert row(game(), st, GOAL)["pass_"] is False


# ── 2. no one is named before they're met: descriptions ──────────────────────
NAMED = "no one is named before they're met"


def met_game(loc):
    """Zoe is met by a canvas; the place's words are the thing under test."""
    meet = canvas("meet_zoe", choices=[{"text": "Hi.", "targetType": "location", "locationId": "room",
                                        "flagEffects": [{"flag": "zoe_met", "op": "set"}]}])
    gated = canvas("later", blocks=[para("x")], conditions=conds(flag_cond("zoe_met")))
    return game([meet, gated], locations=[{"id": "room", "name": "Room", "description": "A room."}, loc],
                npcs=[{"id": "npc_zoe", "name": "Zoe"}])


def test_a_description_naming_her_before_the_meeting_fails():
    r = row(met_game({"id": "quad", "name": "Quad", "description": "Zoe sits on the steps."}), None, NAMED)
    assert r["pass_"] is False
    assert any("location quad · description" in d for d in r["detail"])


def test_a_variant_gated_on_her_met_flag_passes():
    loc = {"id": "quad", "name": "Quad", "description": "The quad.",
           "description_variants": [{"conditions": conds(flag_cond("zoe_met")), "text": "Zoe waves."}]}
    assert row(met_game(loc), None, NAMED)["pass_"] is True


def test_an_ungated_variant_fails_and_a_false_test_is_no_proof():
    loc = {"id": "quad", "name": "Quad", "description": "The quad.",
           "description_variants": [{"conditions": conds(flag_cond("zoe_met", "is_false")),
                                     "text": "Zoe waves."}]}
    r = row(met_game(loc), None, NAMED)
    assert r["pass_"] is False
    assert any("description_variants[0]" in d for d in r["detail"])


def test_a_place_hidden_until_her_met_flag_passes():
    loc = {"id": "zoe_flat", "name": "Zoe's flat", "description": "Zoe's flat.",
           "hidden_until": {"flag": "zoe_met"}}
    assert row(met_game(loc), None, NAMED)["pass_"] is True


# ── 3. a no never raises his Want ────────────────────────────────────────────
NO_WANT = "a no never raises his Want"
WANT_UP = [{"targetType": "npc", "npcId": "npc_ryan", "trait": "want", "op": "add", "value": 5}]


def choice(text, effects=None, **kw):
    ch = {"text": text, "targetType": "location", "locationId": "room", "effects": effects or []}
    ch.update(kw)
    return ch


def test_a_refusal_that_raises_want_fails_with_canvas_and_label():
    r = row(game([canvas("hall", choices=[choice("Not tonight.", WANT_UP)])]), None, NO_WANT)
    assert r["pass_"] is False
    assert r["detail"][0].startswith('hall: "Not tonight."')


def test_an_ends_his_path_label_and_a_final_no_fail():
    for ch in (choice("\"You're my brother.\" (ends his path)", WANT_UP),
               choice("Keep it to yourself.", WANT_UP, final=True)):
        assert row(game([canvas("c", choices=[ch])]), None, NO_WANT)["pass_"] is False


def test_a_no_that_costs_warmth_passes_and_a_yes_may_raise_want():
    warm = [{"targetType": "npc", "npcId": "npc_ryan", "trait": "warmth", "op": "add", "value": -2}]
    g = game([canvas("c", choices=[choice("Walk past him.", warm), choice("Stop and talk.", WANT_UP),
                                   choice("Kiss him.", WANT_UP)])])
    r = row(g, None, NO_WANT)
    assert r["pass_"] is True, r["detail"]


def test_a_phone_reply_no_is_read_too():
    ph = {"conversations": [{"id": "t1", "npc": "npc_ryan", "blocks": [
        {"type": "reply", "choices": [{"text": "not tonight", "effects": WANT_UP}]}]}]}
    r = row(game(phone=ph), None, NO_WANT)
    assert r["pass_"] is False and r["detail"][0].startswith("phone t1")


def test_no_choice_reads_as_a_no_is_na():
    assert row(game([canvas("c", choices=[choice("Kiss him.", WANT_UP)])]), None, NO_WANT)["na"] is True


# ── 4. a booking can clear ──────────────────────────────────────────────────
BOOK = "a booking can clear"


def booking_game(*extra_canvases, phone_extra=None, engine=None):
    """A phone yes sets `x_booked`; his door reads it inside a 3-hour window."""
    convs = [{"id": "ask", "npc": "npc_ryan", "blocks": [
        {"type": "reply", "choices": [{"text": "coming", "flagEffects": [{"flag": "x_booked", "op": "set"}]}]}]}]
    convs += phone_extra or []
    door = canvas("door", conditions=conds(flag_cond("x_booked"), hours("x_booked", "lt", 3)),
                  choices=[choice("Knock.", flagEffects=[{"flag": "x_booked", "op": "unset"}])])
    g = game([door, *extra_canvases], phone={"conversations": convs})
    if engine:
        g["engine"] = engine
    return g


def test_a_booking_cleared_only_inside_its_window_fails():
    r = row(booking_game(), None, BOOK)
    assert r["pass_"] is False
    assert "`x_booked`" in r["detail"][0] and "door inside that window" in r["detail"][0]


def test_a_no_show_thread_on_gte_clears_it():
    noshow = {"id": "noshow", "npc": "npc_ryan",
              "trigger": {"conditions": conds(flag_cond("x_booked"), hours("x_booked", "gte", 3))},
              "on_ignore": {"flagEffects": [{"flag": "x_booked", "op": "unset"}]}, "blocks": []}
    assert row(booking_game(phone_extra=[noshow]), None, BOOK)["pass_"] is True


def test_the_daily_tick_and_the_engine_cleared_list_pass():
    tick = {"daily_tick": {"flagEffects": [{"flag": "x_booked", "op": "unset"}]}}
    assert row(booking_game(engine=tick), None, BOOK)["pass_"] is True
    assert "rent_short" in gates.ENGINE_CLEARED_FLAGS


def test_a_timestamp_and_a_scene_record_are_not_bookings():
    # read only through hours_since: a cooldown stamp; set by a scene, never unset: a record.
    stamp = canvas("stamp", conditions=conds(hours("door_seen", "lt", 20)),
                   choices=[choice("Look.", flagEffects=[{"flag": "door_seen", "op": "set"}])])
    rec = canvas("rec", conditions=conds(flag_cond("opening_done"), hours("opening_done", "lt", 12)),
                 choices=[choice("Go.", flagEffects=[{"flag": "opening_done", "op": "set"}])])
    assert row(game([stamp, rec]), None, BOOK)["na"] is True


# ── 5. a closed activity says when it opens ─────────────────────────────────
CLOSED = "a closed activity says when it opens"
SCHED = [{"weekdays": [0, 1, 2, 3, 4], "start_time": "08:00", "end_time": "12:00"}]


def test_a_solo_activity_without_its_hours_fails():
    g = game([canvas("shift", schedules=SCHED, show_when_blocked=True)])
    r = row(g, None, CLOSED)
    assert r["pass_"] is False and "a cooldown_message" in r["detail"][0]


def test_hours_under_metadata_are_named_dead():
    g = game([canvas("shift", schedules=SCHED, metadata={"show_when_blocked": True,
                                                          "cooldown_message": "mornings"})])
    r = row(g, None, CLOSED)
    assert r["pass_"] is False and "metadata" in r["detail"][0]


def test_a_solo_activity_with_its_hours_passes_and_people_and_random_events_are_skipped():
    g = game([canvas("shift", schedules=SCHED, show_when_blocked=True, cooldown_message="mornings"),
              canvas("his", schedules=SCHED, npc="npc_ryan"),
              canvas("event", schedules=SCHED, trigger_mode="random", chance=0.25)])
    assert row(g, None, CLOSED)["pass_"] is True
    assert row(game([canvas("his", schedules=SCHED, npc="npc_ryan")]), None, CLOSED)["na"] is True


# ── 6. speech is a dialog block ─────────────────────────────────────────────
SPEECH = "speech is a dialog block"


def test_a_quoted_line_in_a_paragraph_fails_with_its_count():
    g = game([canvas("c", blocks=[para('He leans in. "Come here, @player." Then: "Now, please."'),
                                  para('"Yes." You nod.')])])
    r = row(g, None, SPEECH)
    assert r["pass_"] is False
    assert r["detail"][0].startswith("c: 2 quoted line(s)")


def test_a_dialog_block_and_a_not_speech_paragraph_pass():
    g = game([canvas("c", blocks=[{"type": "dialog", "content": "Come here, @player.",
                                   "props": {"speaker": "npc_ryan"}},
                                  para('The sign says "Staff Only Beyond This Door".', not_speech=True),
                                  para('One word: "Fine." Then nothing.')])])
    assert row(g, None, SPEECH)["pass_"] is True
