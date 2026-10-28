"""`every stage has a way up` (the-arc.md A4d, 2026-10-13).

first_term shipped a Good Girl stage with nothing that paid Corruption: the park couple
paid only from 20 (the choice into the watching screen was gated), touching herself was
gated at 20, and the only bridge was a drink's +20 boost. These fixtures pin each part of
the reading: the path inside a canvas, the cap, the drink, and a step counter that only a
higher stage can set.

Fixtures are written here; nothing in games/ is read or written.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402

STATE = {"board": {"ascent_tiers": ["corruption"]}}
BANDS = [{"min": 0, "max": 19, "text": "Good Girl"},
         {"min": 20, "max": 39, "text": "Curious"},
         {"min": 40, "max": 59, "text": "Bold"}]


def cond(*items):
    return {"version": "1.0", "logic": "AND", "items": list(items)}


def corr(op, v):
    return {"type": "trait", "subject": "player", "trait_key": "corruption", "operator": op, "value": v}


def raise_(v, cap=None):
    ef = {"targetType": "player", "trait": "corruption", "op": "add", "value": v}
    if cap is not None:
        ef["cap"] = cap
    return ef


def park(run_pays=False, watch_gate=20):
    """The park's shape: one screen, a run exit and a choice into the watching screen."""
    run = {"text": "Run.", "targetType": "location", "locationId": "park"}
    if run_pays:
        run = {"text": "Look a second longer.", "targetType": "location", "locationId": "park",
               "effects": [raise_(1, cap=19)]}
    return {
        "id": "park_couple",
        "trigger": {"location": "park", "is_repeatable": True, "max_triggers_per_day": 1},
        "nodes": [
            {"id": "sound", "exit_block": {"choices": [
                run,
                {"text": "Stay and watch.", "targetType": "node", "nodeId": "watch",
                 "conditions": cond(corr("gte", watch_gate))},
            ]}},
            {"id": "watch", "exit_block": {"choices": [
                {"text": "Leave.", "targetType": "location", "locationId": "park",
                 "effects": [raise_(1, cap=39)]},
            ]}},
        ],
    }


def game(*canvases, extra=None):
    g = {"sidebar_items": [{"type": "trait_words", "trait": "corruption", "bands": BANDS}],
         "player": {"core_traits": {"corruption": 0}},
         "canvases": list(canvases)}
    # A gate at 40 somewhere, so Good Girl and Curious are both below the highest gate.
    g["canvases"].append({"id": "bold_door", "trigger": {"location": "park", "is_repeatable": False,
                                                         "conditions": cond(corr("gte", 40))},
                          "nodes": [{"id": "a"}]})
    g.update(extra or {})
    return g


def head_detail(g):
    ok, head, detail, n = gates._stage_way_up(g, STATE)
    return ok, head, "\n".join(detail), n


def test_a_stage_whose_only_exit_is_run_is_a_wall():
    ok, head, detail, n = head_detail(game(park()))
    assert ok is False
    assert "Good Girl (0–19)" in head
    assert "Curious" not in head          # watching pays at 20, so Curious has a way up
    assert n == 2


def test_the_choice_on_the_path_gates_the_raise():
    """The park shape: the +1 sits on the watching screen's exit, behind a choice at 20,
    so it does not count at 0 even though the canvas trigger asks for nothing."""
    _ok, _h, detail, _n = head_detail(game(park()))
    good_girl = next(l for l in detail.splitlines() if "Good Girl" in l)
    assert "0 repeatable act(s) pay sober" in good_girl


def test_a_linger_button_at_stage_one_opens_it():
    ok, head, detail, _n = head_detail(game(park(run_pays=True)))
    assert ok is True, head
    assert "park_couple +1" in detail


def test_a_raise_capped_below_the_floor_does_not_count():
    # The linger button pays only to 19, so at Curious (20) only the watching exit counts.
    _ok, _h, detail, _n = head_detail(game(park(run_pays=True, watch_gate=99)))
    curious = next(l for l in detail.splitlines() if "Curious" in l)
    assert "0 repeatable act(s)" in curious


def test_a_raise_open_only_with_a_drink_is_still_a_wall():
    drink = {"id": "kitchen_wine", "trigger": {"location": "kitchen", "is_repeatable": True},
             "nodes": [{"id": "w", "exit_block": {"choices": [
                 {"text": "Have a glass.", "targetType": "location", "locationId": "kitchen",
                  "modifier_effects": [{"key": "drinks_boost", "duration_hours": 3,
                                        "trait_offsets": {"corruption": 20}}]}]}}]}
    ok, head, detail, _n = head_detail(game(park(), drink))
    assert ok is False and "Good Girl" in head
    assert "only while a drink's boost is on: park_couple +1" in detail


def test_a_step_counter_only_a_higher_stage_sets_is_not_open():
    """A repeatable after a ladder (`ryan_step = 8`) is open at 0 on its own trigger, but
    the only exit that sets the counter needs 40 — so it does not pay at Good Girl."""
    step = {"id": "step_8", "trigger": {"location": "room", "is_repeatable": False,
                                        "conditions": cond(corr("gte", 40))},
            "nodes": [{"id": "s", "exit_block": {"choices": [
                {"text": "Yes.", "targetType": "location", "locationId": "room",
                 "effects": [{"targetType": "player", "trait": "ryan_step", "op": "set", "value": 8}]}]}}]}
    after = {"id": "knocks", "trigger": {"location": "room", "is_repeatable": True,
                                         "max_triggers_per_day": 1,
                                         "conditions": cond({"type": "trait", "subject": "player",
                                                             "trait_key": "ryan_step",
                                                             "operator": "eq", "value": 8})},
             "nodes": [{"id": "k", "exit_block": {"choices": [
                 {"text": "Kiss him.", "targetType": "location", "locationId": "room",
                  "effects": [raise_(1, cap=59)]}]}}]}
    g = game(park(), step, after,
             extra={"player": {"core_traits": {"corruption": 0, "ryan_step": 0}}})
    ok, head, detail, _n = head_detail(g)
    assert ok is False and "Good Girl" in head
    good_girl = next(l for l in detail.splitlines() if "Good Girl" in l)
    assert "knocks" not in good_girl


def test_no_stages_is_not_judged():
    g = {"canvases": [], "player": {"core_traits": {}}}
    ok, head, _d, n = gates._stage_way_up(g, {"board": {}})
    assert ok is None and n == 0
