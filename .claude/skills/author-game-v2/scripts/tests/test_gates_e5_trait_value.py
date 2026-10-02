"""Pay computed from stats: the gates read `{type = "trait", …}` effect values.

The engine resolves `value = { type = "trait", trait, mult, add, min, max }` when the
effect applies, as round(trait × mult + add) held inside min / max
(`setup.resolveEffectValue`, `engine.md` §3). Before this, three readers here knew only
numbers and `{type = "random", …}`, so a stat-based pay read as nothing:

  `_effect_value_sign`  — the sign of a grant (the economy and ladder checks);
  `lint_unwritten_act`  — how a choice's effect is printed;
  `_value_mean_max`     — what a week can bring in (`_week_income`).

Fixtures are written here; nothing in games/ is read or written.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402

PAY = {"type": "trait", "trait": "charm", "mult": 2, "add": 50, "min": 0, "max": 100}


# ── _effect_value_sign ────────────────────────────────────────────────────────

def test_a_trait_value_that_can_pay_is_positive():
    assert gates._effect_value_sign(PAY) == 1
    assert gates._effect_value_sign({"type": "trait", "trait": "charm"}) == 1


def test_a_trait_value_capped_below_zero_is_negative():
    assert gates._effect_value_sign({"type": "trait", "trait": "charm",
                                     "mult": -1, "max": -5}) == -1


def test_numbers_and_ranges_read_as_before():
    assert gates._effect_value_sign(3) == 1
    assert gates._effect_value_sign({"type": "random", "min": 2, "max": 4}) == 1
    assert gates._effect_value_sign({"type": "curve"}) == 0


# ── _value_bounds / _value_mean_max ───────────────────────────────────────────

def test_the_low_bound_is_what_it_pays_at_her_starting_trait():
    assert gates._value_bounds(PAY, {"charm": 10}) == (70, 100)
    assert gates._value_bounds(PAY) == (50, 100)          # a missing trait reads 0


def test_with_no_max_a_rising_value_has_no_ceiling():
    lo, hi = gates._value_bounds({"type": "trait", "trait": "charm", "add": 5}, {"charm": 3})
    assert lo == 8 and hi == math.inf


def test_mean_is_todays_pay_for_a_trait_value_and_the_midpoint_for_a_range():
    assert gates._value_mean_max(PAY, {"charm": 10}) == (70.0, 100.0)
    assert gates._value_mean_max({"type": "random", "min": 8, "max": 14}) == (11.0, 14.0)
    assert gates._value_mean_max(30) == (30.0, 30.0)


def test_week_income_counts_a_stat_based_pay_at_her_starting_trait():
    game = {"player": {"core_traits": {"money": 0, "charm": 10}},
            "canvases": [{"id": "shift", "trigger": {"location": "bar", "max_triggers_per_day": 1},
                          "nodes": [{"id": "n", "exit_block": {"config": {"effects": [
                              {"trait": "money", "op": "add", "value": PAY}]}}}]}]}
    mean, mx, rows, uncapped = gates._week_income(game, "money")
    assert (mean, mx) == (490.0, 700.0)                   # 70 today, 100 at most, × 7 days
    assert rows == ["shift: +70 (max 100) × 7 (1/day × 7 days)"] and not uncapped


# ── lint_unwritten_act ────────────────────────────────────────────────────────

def test_the_lint_prints_a_trait_value_as_its_formula():
    assert gates._effect_value_label(PAY, "money") == "+charm×2+50 money"
    assert gates._effect_value_label({"type": "trait", "trait": "charm"}, "money") == "+charm money"
    assert gates._effect_value_label({"type": "random", "min": 2, "max": 4}, "money") == "+2..4 money"


def test_the_lint_does_not_crash_on_a_trait_value():
    game = {"canvases": [{"id": "c", "nodes": [{"id": "n", "exit_block": {"choices": [
        {"text": "Take the tips", "targetType": "location", "target": "bar",
         "effects": [{"trait": "money", "op": "add", "value": PAY}]}]}}]}]}
    summary, rows = gates.lint_unwritten_act([], game)
    assert "+charm×2+50 money" in rows[0]
