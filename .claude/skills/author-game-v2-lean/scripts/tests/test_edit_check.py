"""edit_check.py rules: each fires on the logged slip and stays quiet on the correct version.
Run: venv/bin/python -m pytest .claude/skills/author-game-v2-lean/scripts/tests -q
"""
import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import edit_check as ec  # noqa: E402


def game(rows):
    return {"npcs": [{"id": "npc_theo", "schedules": rows}], "canvases": []}


BAR = {"location": "hotel_bar", "weekdays": [1, 2, 3], "start_time": "18:00", "end_time": "21:00"}


def test_friday_overnight_one_row_is_flagged():
    after = game([BAR, {"location": "hotel_bar", "weekdays": [4], "start_time": "22:00", "end_time": "02:00"}])
    assert any("wraps midnight" in p for p in ec.schedule_problems(after, game([BAR])))


def test_friday_overnight_split_at_midnight_is_clean():
    after = game([BAR, {"location": "hotel_bar", "weekdays": [4], "start_time": "22:00", "end_time": "00:00"},
                  {"location": "hotel_bar", "weekdays": [5], "start_time": "00:00", "end_time": "02:00"}])
    assert ec.schedule_problems(after, game([BAR])) == []


def test_every_day_overnight_row_is_clean():
    after = game([{"location": "club", "weekdays": [0, 1, 2, 3, 4, 5, 6], "start_time": "22:00", "end_time": "04:00"}])
    assert ec.schedule_problems(after, game([])) == []


def test_double_booking_is_flagged():
    after = game([BAR, {"location": "firm", "weekdays": [2], "start_time": "14:00", "end_time": "19:00"}])
    assert any("same time" in p for p in ec.schedule_problems(after, game([BAR])))


def test_unchanged_schedules_are_not_rechecked():
    g = game([BAR, {"location": "firm", "weekdays": [2], "start_time": "14:00", "end_time": "19:00"}])
    assert ec.schedule_problems(g, copy.deepcopy(g)) == []


def canvas(*texts):
    return {"canvases": [{"id": "watch", "nodes": [{"blocks": [{"type": "paragraph", "content": t} for t in texts]}]}],
            "npcs": []}


def test_thin_explicit_beat_is_flagged():
    probs = ec.explicit_beat_problems(canvas("He stands under the water, cock half hard."), {"canvases": []})
    assert any("floor is 3" in p for p in probs)


def test_beat_that_ends_off_the_body_is_flagged():
    text = "His cock is hard and he moans, fucking his fist. It makes you think about the house."
    assert any("ends off the body" in p for p in ec.explicit_beat_problems(canvas(text), {"canvases": []}))


def test_full_beat_with_separate_interiority_is_clean():
    beat = "His cock is hard in his fist and he moans. He thrusts once more and cums on the tiles."
    after = canvas(beat, "You shut the door and stand in the dark hall.")
    assert ec.explicit_beat_problems(after, {"canvases": []}) == []


def board(gates, lints=None):
    return {"gates": gates, "lints": lints or {}}


def g(name, ok, na=False):
    return {"gate": name, "pass_": ok, "na": na, "headline": name, "detail": []}


def test_gate_that_turns_red_is_reported_and_old_reds_are_not():
    before = board([g("residents have homes", True), g("location fill", False)])
    after = board([g("residents have homes", False), g("location fill", False)])
    out = ec.gate_regressions(after, before)
    assert len(out) == 1 and "residents have homes" in out[0]


def test_only_defect_lints_count():
    before = board([], {"past_claim": {"findings": []}, "time_cost_on_button": {"findings": []}})
    after = board([], {"past_claim": {"findings": ["x: last night"]}, "time_cost_on_button": {"findings": ["y"]}})
    out = ec.new_defects(after, before)
    assert len(out) == 1 and "past_claim" in out[0]
