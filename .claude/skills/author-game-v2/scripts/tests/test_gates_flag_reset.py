"""Fixtures for the lint `a flag that never resets` (LO, 2026-09-27). orientation's
`dues_paid_week` is the real case: set on payment, read is_false, never unset — so the
dues are paid once per save. Minimal game dicts; nothing in games/ is read or written.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402


def game(tick=None, extra_unset=None):
    g = {"canvases": [
        {"id": "pay", "nodes": [{"id": "n", "exit_block": {"config": {"flagEffects": [
            {"targetType": "player", "flag": "dues_paid_week", "op": "set"},
            {"targetType": "player", "flag": "met_simone", "op": "set"},
            {"targetType": "player", "flag": "went_up_today", "op": "set"}]}}}]},
    ], "engine": {"daily_tick": {"flagEffects": [
        {"targetType": "player", "flag": "went_up_today", "op": "unset"}] + (tick or [])}}}
    if extra_unset:
        g["canvases"].append({"id": "monday", "nodes": [{"id": "n", "exit_block": {"choices": [
            {"text": "x", "flagEffects": [{"flag": extra_unset, "op": "unset"}]}]}}]})
    return g


def test_week_flag_set_and_never_unset_is_listed():
    summary, found = gates.lint_flag_never_resets(game(), None)
    assert found == ["dues_paid_week"]
    assert "1 of 2" in summary


def test_cleared_in_the_daily_tick_passes():
    tick = [{"targetType": "player", "flag": "dues_paid_week", "op": "unset"}]
    summary, found = gates.lint_flag_never_resets(game(tick=tick), None)
    assert found == [] and "all 2" in summary


def test_cleared_by_a_choice_anywhere_passes():
    _, found = gates.lint_flag_never_resets(game(extra_unset="dues_paid_week"), None)
    assert found == []


def test_plain_flags_are_not_candidates_but_declared_ones_are():
    _, found = gates.lint_flag_never_resets(game(), {"board": {"resetting_flags": ["met_simone"]}})
    assert found == ["dues_paid_week", "met_simone"]


def test_no_candidates_prints_nothing():
    assert gates.lint_flag_never_resets({"canvases": []}, None) == ("", [])
