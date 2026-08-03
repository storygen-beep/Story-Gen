"""`validate_game_toml`'s reachability walker vs the `random` effect value.

⚠️ The load-bearing case is `test_a_random_range_resolves_to_its_max`. A trait effect's
value is normally a number, but the engine also accepts a range —
``value = { type = "random", min = 8, max = 14 }`` — and every sex loop in vesper uses one
(`loop_npc_pleasure += random(8,14)` against a finisher gate of 50).

The walker did `current + value` and `effect.value > 0` unguarded, so it raised
`TypeError: unsupported operand type(s) for +: 'int' and 'dict'` and then
`TypeError: '>' not supported between instances of 'dict' and 'int'`. The command has
therefore never completed a run on vesper since the loops were written — it aborted with a
traceback that reads like a crash rather than a validation failure, which is exactly the
shape of bug that gets mistaken for "the validator doesn't apply to this game".

Reachability documents that it *"assumes the player takes the best path"*, so a range
resolves to its **max**: the fastest a player can reach a gate. Resolving to min would
under-report reachability and invent trait gaps that do not exist.
"""
import pytest

from apps.game_generation.management.commands.validate_game_toml import (
    _numeric_effect_value,
)


def test_a_plain_number_passes_through():
    assert _numeric_effect_value(8) == 8
    assert _numeric_effect_value(-30) == -30
    assert _numeric_effect_value(2.5) == 2.5


def test_a_random_range_resolves_to_its_max():
    """Best-path assumption: random(8,14) advances the walker by 14, not 8."""
    assert _numeric_effect_value({"type": "random", "min": 8, "max": 14}) == 14


def test_a_random_range_without_a_max_falls_back_to_min():
    assert _numeric_effect_value({"type": "random", "min": 5}) == 5


def test_a_random_range_with_no_bounds_is_skipped_not_guessed():
    assert _numeric_effect_value({"type": "random"}) is None


@pytest.mark.parametrize("value", [
    None,
    "twelve",
    {"type": "curve", "points": [1, 2]},   # a shape this walker doesn't model
    ["a", "list"],
    {},
])
def test_unmodellable_shapes_return_none_rather_than_crash(value):
    """A walker that can't model an effect should leave the trait alone.

    Returning None makes the caller skip the effect. Raising would take the whole
    validation down over one unrecognised shape — which is the bug this replaced.
    """
    assert _numeric_effect_value(value) is None


def test_a_bool_is_not_a_trait_delta():
    """bool subclasses int, so `True` would silently add 1 to a trait."""
    assert _numeric_effect_value(True) is None
    assert _numeric_effect_value(False) is None
