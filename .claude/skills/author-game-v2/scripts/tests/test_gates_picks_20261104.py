"""LO's 27 skill answers (pass3/PICKS.md, "your picks on all 27", 2026-11-03; applied 2026-11-04).

One pass fixture and one fail fixture for every check an answer changed:

  A67       shape.py: release_page.steps and SP7's top-step row against each ladder's length
  J75 / A69 lint `which refusals are shown at all` skips a small rung (5/10/15 inside a stage)
  B51       gate `a named person is where the line says`: a walk-in's arrival is presence
  B52       lint `a person who never speaks` skips a sleeper
  B53       gate `her clothes are named exactly`: a strip is backed by the act unless the canvas
            names her clothes again later
  E22       gate `ascent tiers expand the world` skips a meter declared `"spent": true`
  F31       lint `the labels and the systems agree` never asks an ascent tier to be read elsewhere
  H63       gate `nobody is woken`: 00:00-06:00 behind a door is asleep unless the row says awake
  H65       gate `a day word fits its window` skips forward words
  J70       lint `the badge arrives before the content` reads a `_step` trait as "played this"
  J74       gate `a latch flag is cleared` no longer asks for `rent_carried` to be cleared

Fixtures are built here; nothing in games/ is read.
"""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import gates  # noqa: E402
import shape  # noqa: E402
import test_gates_truth as T  # noqa: E402
from test_gates_lo_20261103 import ASCENT, descent_game, row  # noqa: E402


# ── A67 · the release page's steps match the ladders ─────────────────────────
def _steps_state(declared):
    lad = {"counter": "jo_step", "steps": [{"n": 1, "hint": "a"}, {"n": 2, "hint": "b"}, {"n": 3, "hint": "c"}]}
    return {"phase": "spine", "board": {"characters": [{"id": "npc_jo", "name": "Jo", "ladder": lad}]},
            "release_page": {"people": ["npc_jo"], "steps": declared}}


def _steps_row(state, slug=None, root=None):
    return next(r for r in shape.check(state, True, slug, root)[0] if r[0] == shape.STEPS_MATCH)


def test_release_page_steps_that_match_the_ladder_pass():
    assert _steps_row(_steps_state({"npc_jo": 3}))[1] is True


def test_a_stale_release_page_step_count_fails():
    r = _steps_row(_steps_state({"npc_jo": 2}))
    assert r[1] is False and "release_page.steps says 2, the ladder has 3" in r[3][0]


def test_a_stale_sp7_top_step_fails(tmp_path):
    spine = tmp_path / "games" / "fx" / "spine"
    spine.mkdir(parents=True)
    page = spine / "SP7_release.md"
    page.write_text("| decision | answer |\n|---|---|\n"
                    "| people, and each one's top step | Jo 2 (the shed) · 3 steps (DECISIONS 101) |\n")
    r = _steps_row(_steps_state({"npc_jo": 3}), "fx", str(tmp_path))
    assert r[1] is False and "SP7 says top step 2" in r[3][0]
    page.write_text("| people, and each one's top step | Jo 3 (the key) · DECISIONS 101 |\n")
    assert _steps_row(_steps_state({"npc_jo": 3}), "fx", str(tmp_path))[1] is True


def test_no_steps_anywhere_is_na():
    st = _steps_state(None)
    del st["release_page"]["steps"]
    assert _steps_row(st)[1] is None


# ── J75 / A69 · a small rung may show greyed in the scene ─────────────────────
def _rung_model(value, extra=()):
    items = [{"type": "trait", "subject": "player", "trait_key": "corruption", "operator": "gte",
              "value": value}] + list(extra)
    raw = {"id": "stacks", "nodes": [
        {"id": "a", "exit_block": {"choices": [
            {"text": "Move one aisle closer.", "targetType": "node", "nodeId": "b", "show_when_locked": True,
             "locked_text": "Not yet.", "conditions": {"version": "1.0", "logic": "AND", "items": items},
             "effects": [{"targetType": "player", "trait": "corruption", "op": "add", "value": 1}]}]}},
        {"id": "b"}]}
    return [{"id": "stacks", "raw": raw}]


TIERS = {"board": {"ascent_tiers": ["corruption", "exhibitionism"]}}


def test_a_small_rung_inside_a_stage_is_skipped():
    summary, rows = gates.lint_refusal_shape(_rung_model(5), {}, TIERS)
    assert "0 in-scene" in summary and rows == []
    flag = {"type": "flag", "subject": "player", "flag_key": "stacks_today", "operator": "is_false"}
    assert gates.lint_refusal_shape(_rung_model(15, [flag]), {}, TIERS)[1] == []


def test_a_stage_gate_or_an_undeclared_tier_is_still_listed():
    assert gates.lint_refusal_shape(_rung_model(20), {}, TIERS)[1]                      # a stage, not a rung
    assert gates.lint_refusal_shape(_rung_model(5), {}, {"board": {}})[1]              # no tiers declared
    assert gates.lint_refusal_shape(_rung_model(5), {})[1]                             # no ledger at all


# ── B51 · a walk-in's arrival is presence for the walker ─────────────────────
def _walkin_game(bound):
    g = T.base_game()
    trig = {"substitution_only": True}
    if bound:
        trig["npc"] = "npc_mum"
    g["canvases"] = [T.canvas("walkin_hall", "hall", [T.para("The door opens."), T.say("npc_mum", "Oh. Sorry.")],
                              **trig)]
    return g


def test_a_walker_speaks_on_their_walk_in():
    assert T.ok_of(gates._named_person_present, _walkin_game(bound=False)) in (True, None)


def test_the_same_line_off_a_walk_in_is_still_red():
    g = _walkin_game(bound=False)
    del g["canvases"][0]["trigger"]["substitution_only"]
    ok, _, detail = T.run(gates._named_person_present, g)
    assert ok is False and "Mum speaks" in detail[0]


# ── B52 · a sleeper is exempt from "a present person speaks" ──────────────────
def test_a_sleeping_bound_person_is_not_listed_as_mute():
    g = {"npcs": [{"id": "npc_jo", "name": "Jo"}], "canvases": [
        {"id": "bed", "trigger": {"location": "room", "is_repeatable": True, "npc": "npc_jo"},
         "nodes": [{"id": "a", "blocks": [{"type": "paragraph", "content": "Jo is asleep on his back, snoring."}]}]}]}
    s, rows = gates.lint_person_never_speaks(g)
    assert rows == [] and "0 of 1" in s
    g["canvases"][0]["nodes"][0]["blocks"][0]["content"] = "Jo looks up from his book."
    assert gates.lint_person_never_speaks(g)[1] == ["bed: npc_jo never speaks"]


# ── B53 · a strip inside an act is backed by the act ─────────────────────────
def _strip_game(later_text):
    g = T.base_game()
    g["clothing"] = [{"id": "top", "slot": "top", "name": "Top"}]
    nodes = [{"id": "a", "blocks": [T.para("You pull your top off over your head.")],
              "exit_block": {"type": "choices", "choices": [
                  {"text": "Go on.", "targetType": "node", "nodeId": "b"}]}},
             {"id": "b", "blocks": [T.para(later_text)],
              "exit_block": {"type": "choices", "choices": [T.leave("street")]}}]
    g["canvases"] = [T.canvas("dare", "kitchen", [], nodes=nodes)]
    return g


def test_a_strip_the_canvas_never_contradicts_is_backed_by_the_act():
    assert T.ok_of(gates._clothes_named_exactly, _strip_game("He stares at your tits.")) is True


def test_a_strip_followed_by_her_clothes_again_needs_the_garment_moved():
    g = _strip_game("You straighten your top and leave.")
    ok, _, detail = T.run(gates._clothes_named_exactly, g)
    assert ok is False and "screen b" in detail[0]
    g["canvases"][0]["nodes"][0]["exit_block"]["choices"][0]["wardrobeEffects"] = [
        {"item_id": "top", "action": "unequip"}]
    assert T.ok_of(gates._clothes_named_exactly, g) is True


def test_an_exit_naming_her_clothes_counts_too():
    g = _strip_game("He stares.")
    g["canvases"][0]["nodes"][1]["exit_block"]["choices"] = [T.leave("street", "Pull your top back on and go.")]
    assert T.ok_of(gates._clothes_named_exactly, g) is False


# ── E22 · a spent meter is not a descent ─────────────────────────────────────
def test_a_meter_declared_spent_is_skipped():
    st = {"board": {"ascent_tiers": ["heat"], "needs": [{"key": "energy"}],
                    "meters": [{"id": "grade", "key": "grade", "kind": "ambient", "spent": True}]}}
    assert row(descent_game(), st, ASCENT)["pass_"] is True


def test_the_same_meter_without_spent_still_fails():
    st = {"board": {"ascent_tiers": ["heat"], "needs": [{"key": "energy"}],
                    "meters": [{"id": "grade", "key": "grade", "kind": "ambient"}]}}
    r = row(descent_game(), st, ASCENT)
    assert r["pass_"] is False and any(d.startswith("grade is") for d in r["detail"])


# ── F31 · an ascent tier is fed everywhere by design ─────────────────────────
def _fed_everywhere(tiers):
    meter = {"id": "c", "kind": "sourced", "key": "corruption", "fed_at": ["a", "b"], "labels": ["x"]}
    model = [{"loc": "a", "sets": {"corruption"}, "reads": {"corruption"}, "raw": {}},
             {"loc": "b", "sets": {"corruption"}, "reads": {"corruption"}, "raw": {}}]
    board = {"meters": [meter], "locations": [{"id": "a", "labels": ["x"]}, {"id": "b", "labels": ["x"]}]}
    if tiers:
        board["ascent_tiers"] = ["corruption"]
    return gates.lint_labels_and_systems(model, "fx", {"board": board})[1]


def test_an_ascent_tier_is_not_asked_to_be_read_elsewhere():
    assert not any("read in no room outside" in f for f in _fed_everywhere(tiers=True))


def test_an_ordinary_sourced_meter_still_is():
    assert any("read in no room outside" in f for f in _fed_everywhere(tiers=False))


# ── H63 · the night behind a door is asleep unless the row says awake ─────────
def _night_game(activity):
    g = T.base_game()
    g["npcs"].append({"id": "npc_bro", "name": "Bro", "schedules": [
        {"location": "bedroom", "weekdays": T.ALL, "start_time": "22:00", "end_time": "07:00",
         "activity": activity}]})
    g["npcs"][0]["schedules"][1]["location"] = "kitchen"        # Mum sleeps elsewhere in this fixture
    g["locations"][3]["door"] = {"options": [{"text": "Knock.", "goes_to": {"type": "enter"}}]}
    return g


def test_a_night_row_behind_a_door_is_asleep_after_midnight():
    ok, _, detail = T.run(gates._nobody_is_woken, _night_game("in his room for the night"))
    assert ok is False and any("Bro is asleep inside at" in d and "00:" in d for d in detail)


def test_a_night_row_that_says_awake_passes():
    assert T.ok_of(gates._nobody_is_woken, _night_game("awake, gaming")) is True


def test_a_room_with_no_door_is_not_read_as_asleep():
    g = _night_game("in his room for the night")
    del g["locations"][3]["door"]
    g["canvases"] = [T.canvas("chat", "bedroom", [T.say("npc_bro", "Can't sleep either?")],
                              schedules=[{"weekdays": T.ALL, "start_time": "01:00", "end_time": "02:00"}])]
    assert T.ok_of(gates._nobody_is_woken, g) is True


# ── H65 · a forward word is skipped ──────────────────────────────────────────
def _late(text):
    g = T.base_game()
    g["canvases"] = [T.canvas("bed", "bedroom", [T.para(text)],
                              schedules=[{"weekdays": T.ALL, "start_time": "22:00", "end_time": "23:00"}])]
    return g


def test_forward_words_are_skipped():
    for text in ("I'll still be here in the morning.", "It will be dry by morning.",
                 "Tomorrow morning. Don't be late."):
        assert T.ok_of(gates._day_word_fits, _late(text)) is not False, text


def test_a_morning_said_at_night_is_still_red():
    assert T.ok_of(gates._day_word_fits, _late("Good morning, sunshine.")) is False


# ── J70 · a `_step` terminal reads as "played this" ──────────────────────────
def _badge(trait):
    raw = {"trigger": {"conditions": {"version": "1.0", "items": [
        {"type": "trait", "npc_id": "npc_jo", "trait_key": "warmth", "operator": "gte", "value": 40}]}}}
    game = {"quest_cards": [{"npc_id": "npc_jo", "terminal": True,
                             "when": [{"trait": trait, "op": "gte", "value": 4}]}]}
    return gates.lint_badge_before_content([{"raw": raw}], game)[1]


def test_a_step_counter_terminal_has_no_badge_finding():
    assert _badge("jo_step") == []


def test_a_meter_terminal_on_another_meter_is_still_listed():
    assert any("[badge] jo" in f for f in _badge("power"))


# ── J74 · rent_carried is a record, not a latch ──────────────────────────────
def test_reading_rent_carried_is_not_a_latch():
    g = T.base_game()
    g["canvases"] = [T.canvas("vance", "hall", [T.group([T.flag("rent_carried")], T.para("You were short once."))])]
    assert T.ok_of(gates._latch_flag_cleared, copy.deepcopy(g)) is None
