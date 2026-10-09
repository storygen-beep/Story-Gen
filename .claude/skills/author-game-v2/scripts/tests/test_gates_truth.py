"""The truth gates (skill pass 2026-10-08, SKILL_CHANGES B98–B116).

first_term 0.1 passed every gate, and a read-only sweep then found 230 lines that were false at
some hour they could show. These gates check a line against who is where (first-match schedule
rows, `when` rows both ways), the minutes a screen can be read in, and which flag records what.
One pass fixture and one fail fixture per gate. Fixtures only; no game is read.
"""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402

ALL = [0, 1, 2, 3, 4, 5, 6]


def cond(*items, logic="AND"):
    return {"version": "1.0", "logic": logic, "items": list(items)}


def flag(key, op="is_true"):
    return {"type": "flag", "subject": "player", "flag_key": key, "operator": op}


def trait(key, op, value):
    return {"type": "trait", "subject": "player", "trait_key": key, "operator": op, "value": value}


def at(npc, loc, op="is_present"):
    return {"type": "npc_at_location", "npc_id": npc, "location_id": loc, "operator": op}


def tod(a, b):
    return {"type": "time_of_day", "start_time": a, "end_time": b}


def para(text, **kw):
    return dict({"type": "paragraph", "content": text}, **kw)


def say(npc, text):
    return {"type": "dialog", "content": text, "props": {"speaker": "npc", "npcId": npc}}


def group(items, *blocks):
    return {"type": "group", "conditions": cond(*items), "blocks": list(blocks)}


def leave(loc, text="Go.", **kw):
    return dict({"text": text, "targetType": "location", "locationId": loc}, **kw)


def canvas(cid, loc, blocks, choices=None, rep=True, npc=None, extra=None, nodes=None, **trig):
    t = dict({"location": loc, "is_repeatable": rep}, **trig)
    if npc:
        t["npc"] = npc
    c = {"id": cid, "trigger": t,
         "nodes": nodes or [{"id": "n1", "blocks": blocks,
                             "exit_block": {"type": "choices", "choices": choices or [leave("street")]}}]}
    c.update(extra or {})
    return c


def base_game():
    """A house (hall, kitchen, bedroom) off a street; Mum in the kitchen 07–22, asleep 22–07."""
    return {
        "time": {"starting_day": "Monday", "starting_hour": 7},
        "locations": [
            {"id": "street"},
            {"id": "hall", "entry_from": "street"},
            {"id": "kitchen", "entry_from": "hall"},
            {"id": "bedroom", "entry_from": "hall"},
            {"id": "cafe", "entry_from": "street"},
        ],
        "npcs": [{"id": "npc_mum", "name": "Mum", "role": "mom", "schedules": [
            {"location": "kitchen", "weekdays": ALL, "start_time": "07:00", "end_time": "22:00",
             "activity": "cooking"},
            {"location": "bedroom", "weekdays": ALL, "start_time": "22:00", "end_time": "07:00",
             "activity": "asleep"}]}],
        "canvases": [],
    }


def run(fn, g, state=None):
    return fn(g, state) if fn in (gates._every_person_has_a_face, gates._card_shows_real_gates) else fn(g)


def ok_of(fn, g, state=None):
    return run(fn, g, state)[0]


# ── a named person is where the line says ─────────────────────────────────────
def test_named_person_backed_by_their_own_check_passes():
    g = base_game()
    g["canvases"] = [canvas("couch", "hall", [group([at("npc_mum", "kitchen")], para("Mum's in the kitchen, humming."))])]
    assert ok_of(gates._named_person_present, g) is True


def test_named_person_true_only_some_hours_is_red():
    g = base_game()
    g["canvases"] = [canvas("couch", "hall", [para("Mum is in the kitchen, humming.")])]
    ok, _, detail = run(gates._named_person_present, g)
    assert ok is False and "Mum" in detail[0]


def test_any_npc_check_does_not_back_a_name():
    g = base_game()
    any_npc = {"type": "npc_at_location", "location_id": "kitchen", "operator": "is_present"}
    g["canvases"] = [canvas("couch", "hall", [group([any_npc], para("Mum is in the kitchen."))])]
    assert ok_of(gates._named_person_present, g) is False


def test_a_line_deeper_in_a_scene_is_read_at_the_later_time():
    g = base_game()
    nodes = [{"id": "a", "blocks": [para("You sit down.")], "exit_block": {"type": "choices", "choices": [
                 {"text": "Wait.", "targetType": "node", "nodeId": "b", "time_progression_minutes": 120}]}},
             {"id": "b", "blocks": [para("Mum's asleep upstairs.")],
              "exit_block": {"type": "choices", "choices": [leave("street")]}}]
    g["canvases"] = [canvas("wait", "hall", [], nodes=nodes, schedules=[
        {"weekdays": ALL, "start_time": "20:00", "end_time": "21:00"}])]
    # Entered 20:00–21:00, the line is read two hours on, 22:00–23:00, while she sleeps: true.
    assert ok_of(gates._named_person_present, g) is True
    # With no time spent it is read at 20:00–21:00, while she cooks: false.
    nodes[0]["exit_block"]["choices"][0]["time_progression_minutes"] = 0
    assert ok_of(gates._named_person_present, g) is False


# ── nobody is woken ───────────────────────────────────────────────────────────
def test_a_knock_while_she_sleeps_is_red_and_a_daytime_knock_passes():
    g = base_game()
    g["locations"][3]["door"] = {"options": [{"text": "Knock.", "goes_to": {"type": "enter"}}]}
    assert ok_of(gates._nobody_is_woken, g) is False
    g["locations"][3]["door"]["options"][0]["conditions"] = cond(tod("08:00", "21:00"))
    assert ok_of(gates._nobody_is_woken, g) is True


def test_a_one_time_scene_whose_person_is_out_is_red():
    g = base_game()
    g["canvases"] = [canvas("talk", "kitchen", [say("npc_mum", "Sit.")], rep=False,
                            schedules=[{"weekdays": ALL, "start_time": "09:00", "end_time": "10:00"}])]
    assert ok_of(gates._nobody_is_woken, g) is True
    g["canvases"][0]["trigger"]["schedules"] = [{"weekdays": ALL, "start_time": "02:00", "end_time": "03:00"}]
    assert ok_of(gates._nobody_is_woken, g) is False      # she is asleep and the scene has her talking


# ── every person here has a face ──────────────────────────────────────────────
def test_every_place_with_a_face_passes_and_a_missing_one_is_red():
    g = base_game()
    g["canvases"] = [canvas("hub_mum_kitchen", "kitchen", [para("She's chopping.")], npc="npc_mum")]
    state = {"board": {"characters": [{"id": "npc_mum", "occupancy_rows": [
        {"location": "bedroom", "start_time": "22:00", "reason": "asleep"}]}]}}
    assert ok_of(gates._every_person_has_a_face, g, state) is True
    ok, _, detail = run(gates._every_person_has_a_face, g, {})
    assert ok is False and "bedroom" in detail[0]


def test_a_heat_gated_face_is_not_a_face():
    g = base_game()
    g["canvases"] = [canvas("hub_mum_kitchen", "kitchen", [para("x")], npc="npc_mum",
                            conditions=cond(trait("corruption", "gte", 40)))]
    state = {"board": {"characters": [{"id": "npc_mum", "occupancy_rows": [
        {"location": "bedroom", "start_time": "22:00", "reason": "asleep"}]}]}}
    ok, _, detail = run(gates._every_person_has_a_face, g, state)
    assert ok is False and "heat-gated" in detail[0]


# ── a past line has its event ─────────────────────────────────────────────────
def test_a_past_line_on_its_flag_passes_and_on_a_shared_meter_is_red():
    g = base_game()
    line = para("I heard you were at the party.")
    g["canvases"] = [canvas("gossip", "cafe", [group([flag("party_went")], line)])]
    assert ok_of(gates._past_line_has_event, g) is True
    raise_talk = [{"text": "Chat.", "targetType": "location", "locationId": "cafe",
                   "effects": [{"trait": "talk", "op": "add", "value": 1}]}]
    g["canvases"] = [canvas("gossip", "cafe", [group([trait("talk", "gte", 5)], line)]),
                     canvas("lunch", "cafe", [para("Lunch.")], choices=raise_talk),
                     canvas("class", "cafe", [para("Class.")], choices=raise_talk)]
    assert ok_of(gates._past_line_has_event, g) is False


# ── no one is named before they're met ────────────────────────────────────────
def test_narration_placing_someone_waits_for_their_met_flag():
    g = base_game()
    g["npcs"].append({"id": "npc_zoe", "name": "Zoe", "schedules": []})
    meet = canvas("meet_zoe", "cafe", [para("A girl waves.")], rep=False,
                  choices=[leave("street", flagEffects=[{"flag": "zoe_met", "op": "set"}])])
    g["canvases"] = [meet, canvas("class", "cafe", [para("Zoe kicks your ankle under the table.")])]
    assert ok_of(gates._named_before_met_gate, g) is False
    g["canvases"][1]["trigger"]["conditions"] = cond(flag("zoe_met"))
    assert ok_of(gates._named_before_met_gate, g) is True


# ── a latch flag is cleared ───────────────────────────────────────────────────
def test_a_flag_driving_a_row_must_clear_daily():
    g = base_game()
    g["npcs"][0]["schedules"].insert(0, {"location": "hall", "weekdays": ALL, "start_time": "23:00",
                                         "end_time": "02:00", "activity": "waiting up",
                                         "when": cond(flag("came_home_late"))})
    assert ok_of(gates._latch_flag_cleared, g) is False
    g["engine"] = {"daily_tick": {"flagEffects": [{"flag": "came_home_late", "op": "unset"}]}}
    assert ok_of(gates._latch_flag_cleared, g) is True


# ── a repeat doesn't say it's the first time ──────────────────────────────────
def test_an_arrival_line_on_a_repeat_needs_a_flag():
    g = base_game()
    g["canvases"] = [canvas("hub", "cafe", [para("You walk in and the bell rings.")])]
    assert ok_of(gates._repeat_not_first, g) is False
    g["canvases"][0]["nodes"][0]["blocks"] = [group([flag("cafe_first", "is_false")],
                                                    para("You walk in and the bell rings."))]
    assert ok_of(gates._repeat_not_first, g) is True


# ── a button does something ───────────────────────────────────────────────────
def test_a_hub_exit_back_to_its_own_room_is_red():
    g = base_game()
    g["canvases"] = [canvas("hub_mum", "kitchen", [para("x")], npc="npc_mum",
                            choices=[leave("kitchen", "Leave her to it.")])]
    assert ok_of(gates._button_does_something, g) is False
    g["canvases"][0]["nodes"][0]["exit_block"]["choices"] = [leave("hall", "Leave her to it.")]
    assert ok_of(gates._button_does_something, g) is True


def test_get_dressed_must_move_a_garment():
    g = base_game()
    g["canvases"] = [canvas("mirror", "bedroom", [para("x")], choices=[leave("hall", "Get dressed.")])]
    assert ok_of(gates._button_does_something, g) is False
    g["canvases"][0]["nodes"][0]["exit_block"]["choices"][0]["wardrobeEffects"] = [
        {"action": "equip", "item_id": "jeans"}]
    assert ok_of(gates._button_does_something, g) is True


# ── a clock bucket has a catch-all ────────────────────────────────────────────
def test_minutes_spent_before_clock_buckets_can_strand_her():
    g = base_game()
    buckets = [dict(leave("street", "Go home."), conditions=cond(tod("20:00", "21:00"))),
               dict(leave("street", "Go home."), conditions=cond(tod("21:00", "22:00")))]
    nodes = [{"id": "a", "blocks": [para("x")], "exit_block": {"type": "choices", "choices": [
                 {"text": "Stay.", "targetType": "node", "nodeId": "b", "time_progression_minutes": 30}]}},
             {"id": "b", "blocks": [para("y")], "exit_block": {"type": "choices", "choices": buckets}}]
    g["canvases"] = [canvas("party", "cafe", [], nodes=nodes,
                            schedules=[{"weekdays": ALL, "start_time": "20:00", "end_time": "22:00"}])]
    ok, _, detail = run(gates._clock_bucket_catch_all, g)
    assert ok is False and "22:00" in detail[0]
    buckets.append(leave("street", "Go home."))
    assert ok_of(gates._clock_bucket_catch_all, g) is True


# ── her clothes are named exactly · one garment per slot ──────────────────────
def test_exposure_alone_does_not_back_underwear_and_a_slot_does():
    g = base_game()
    g["clothing"] = [{"id": "bra", "slot": "bra"}]
    expo = {"type": "worn_exposure", "operator": "eq", "value": 1}
    g["canvases"] = [canvas("mirror", "bedroom", [group([expo], para("You're in your underwear."))])]
    assert ok_of(gates._clothes_named_exactly, g) is False
    slot = {"type": "clothing_slot", "slot": "top", "operator": "empty"}
    g["canvases"][0]["nodes"][0]["blocks"] = [group([expo, slot], para("You're in your underwear."))]
    assert ok_of(gates._clothes_named_exactly, g) is True


def test_two_initial_garments_in_one_slot_are_red():
    g = base_game()
    g["clothing"] = [{"id": "shirt", "slot": "dress", "initial": True},
                     {"id": "towel", "slot": "dress", "initial": True}]
    ok, _, detail = run(gates._one_garment_per_slot, g)
    assert ok is False and "towel" in detail[0]
    g["clothing"][1]["initial"] = False
    assert ok_of(gates._one_garment_per_slot, g) is True


# ── a card shows the real gates ───────────────────────────────────────────────
def test_a_goal_on_the_step_counter_is_red_and_a_meter_goal_passes():
    g = base_game()
    g["canvases"] = [canvas("mum_02", "kitchen", [para("x")], rep=False,
                            conditions=cond(trait("mum_step", "eq", 1), trait("corruption", "gte", 20)))]
    card = {"npc_id": "npc_mum", "text": "Mum.", "ready_canvas": "mum_02",
            "goals": [{"type": "trait", "trait": "mum_step", "op": "gte", "value": 2, "label": "Talk to Mum"}]}
    g["quest_cards"] = [card]
    ok, _, detail = run(gates._card_shows_real_gates, g)
    assert ok is False and len(detail) == 2          # the counter goal, and corruption is hidden
    card["goals"] = [{"type": "trait", "trait": "corruption", "op": "gte", "value": 20, "label": "Curious"}]
    assert ok_of(gates._card_shows_real_gates, g) is True


# ── a phone line is true ──────────────────────────────────────────────────────
def test_a_follow_up_needs_after_round():
    g = base_game()
    blocks = [{"type": "message", "sender": "npc", "content": "dinner?"},
              {"type": "reply", "round": 1, "choices": [{"text": "yes"}, {"text": "no"}]},
              {"type": "message", "sender": "npc", "round": 2, "content": "six then"}]
    g["phone"] = {"conversations": [{"id": "dinner", "npc": "npc_mum", "blocks": blocks}]}
    assert ok_of(gates._phone_line_true, g) is False
    blocks[2] = {"type": "message", "sender": "npc", "after_round": 1, "after_choice": 0, "content": "six then"}
    assert ok_of(gates._phone_line_true, g) is True


def test_a_call_from_someone_asleep_is_red():
    g = base_game()
    g["phone"] = {"calls": [{"id": "late", "caller": "npc_mum",
                             "trigger": {"conditions": cond(tod("23:00", "00:00"))}}]}
    assert ok_of(gates._phone_line_true, g) is False
    g["phone"]["calls"][0]["trigger"]["conditions"] = cond(tod("19:00", "20:00"))
    assert ok_of(gates._phone_line_true, g) is True


# ── one pool, one place · the phone owns posting ─────────────────────────────
def test_a_pool_pasted_into_two_canvases_is_red():
    pool = {"type": "block_pool", "blocks": [para("She looks up."), para("She smiles.")]}
    g = base_game()
    g["canvases"] = [canvas("a", "kitchen", [copy.deepcopy(pool)]), canvas("b", "hall", [copy.deepcopy(pool)])]
    assert ok_of(gates._one_pool_one_place, g) is False
    g["canvases"].pop()
    assert ok_of(gates._one_pool_one_place, g) is True


def test_a_room_selfie_beside_a_phone_feed_is_red():
    g = base_game()
    g["phone"] = {"apps": [{"id": "feed", "type": "social_feed", "post_actions": [
        {"label": "Post a selfie", "counter_trait": "followers"}]}]}
    g["canvases"] = [canvas("mirror", "bedroom", [para("x")], choices=[leave("hall", "Post it.")])]
    assert ok_of(gates._phone_owns_posting, g) is False
    g["canvases"][0]["nodes"][0]["exit_block"]["choices"] = [leave("hall", "Fix your hair.")]
    assert ok_of(gates._phone_owns_posting, g) is True


# ── a day word fits its window ────────────────────────────────────────────────
def test_this_morning_at_night_is_red():
    g = base_game()
    g["canvases"] = [canvas("bed", "bedroom", [para("This morning was a mess.")],
                            schedules=[{"weekdays": ALL, "start_time": "20:00", "end_time": "23:00"}])]
    assert ok_of(gates._day_word_fits, g) is False
    g["canvases"][0]["trigger"]["schedules"] = [{"weekdays": ALL, "start_time": "08:00", "end_time": "11:00"}]
    assert ok_of(gates._day_word_fits, g) is True


# ── registration ─────────────────────────────────────────────────────────────
def test_the_nine_block_rows_are_registered_and_dated():
    block = {n for n, _f, _a, rule in gates._TRUTH_GATES if rule}
    assert len(block) == 9 and block <= set(gates.SHIP_BLOCK_GATES)
    assert all(gates.SHIP_SINCE[r][0] == gates.TRUTH_SINCE for _n, _f, _a, r in gates._TRUTH_GATES if r)


def test_a_legacy_rerun_reports_not_checked():
    g = base_game()
    g["canvases"] = [canvas("couch", "hall", [para("Mum is in the kitchen.")])]
    gates._LEGACY_RULES.add("named_present")
    try:
        ok, head, _ = gates._truth_run("a named person is where the line says", g, {})
    finally:
        gates._LEGACY_RULES.discard("named_present")
    assert ok is True and "not checked before" in head
