"""`lint · a cheat page exists` (PRD IC4, LO 2026-09-27): reported, never a gate."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402

BASICS = [
    {"id": "money", "label": "Money", "trait": "money", "value": 50, "free": True},
    {"id": "skip_day", "label": "Skip to morning", "kind": "next_day", "free": True},
    {"id": "step_now", "label": "Now", "kind": "play", "canvas": "s1", "free": True},
    {"id": "again", "label": "Again", "kind": "reopen", "flag": "said_no", "free": True},
]


def test_no_page_is_reported_not_failed():
    summary, findings = gates.lint_cheat_page({})
    assert summary.startswith("none") and findings == []


def test_all_four_basics_free_is_clean():
    summary, findings = gates.lint_cheat_page({"ui": {"cheat_page": {"grants": BASICS}}})
    assert "4 free row(s), 0 behind a code" in summary and "4 of 4" in summary
    assert findings == []


def test_a_missing_basic_and_a_sold_time_saver_are_listed():
    rows = [BASICS[0], dict(BASICS[1], free=False)]
    summary, findings = gates.lint_cheat_page({"ui": {"cheat_page": {"grants": rows}}})
    assert "1 of 4" in summary
    assert "no free 'the next step now' row" in findings
    assert any("'skip_day' (next_day) is a time-saver sold behind a code" in f for f in findings)


def test_a_coded_trait_row_is_fine():
    rows = BASICS + [{"id": "stealth", "label": "Stealth", "trait": "stealth", "value": 5}]
    summary, findings = gates.lint_cheat_page({"ui": {"cheat_page": {"grants": rows}}})
    assert "1 behind a code" in summary and findings == []
