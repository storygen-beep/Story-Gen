"""Step reachability reads a value worked out from her stats (leftovers L3, 2026-10-02).

`_ladder_earnable` asks whether a step's trait gate can be met before the step. Its two
readers — a scene's effect and `[engine.daily_tick]` — knew numbers and
`{type = "random", …}` only, so a stat-based value (`{type = "trait", …}`, resolved by
`setup.resolveEffectValue` against her core traits) was skipped and a reachable step read
as unreachable. They now read it through `_value_bounds`, as the E5 readers do.

Fixtures are written here; nothing in games/ is read or written.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402

GATE = {"type": "trait", "trait_key": "money", "subject": "player", "operator": "gte", "value": 40}


def _game(value, where="scene"):
    eff = {"trait": "money", "op": "add", "targetType": "player", "value": value}
    game = {"player": {"core_traits": {"charm": 5, "money": 0}}, "npcs": [], "canvases": [
        {"id": "step", "trigger": {"location": "office"}, "nodes": []}]}
    if where == "scene":
        game["canvases"].append({"id": "shift", "trigger": {"location": "bar", "is_repeatable": False},
                                 "nodes": [{"id": "n", "exit_block": {"config": {"effects": [eff]}}}]})
    else:
        game["engine"] = {"daily_tick": {"traitEffects": [eff]}}
    return game


def _earnable(game):
    ctx = (set(), dict(game["player"]["core_traits"]), set(), set())
    return gates._ladder_earnable(GATE, "step", "rank", 2, game, ctx)


def test_a_scene_paying_from_her_stats_can_reach_the_gate():
    # charm 5 × 10 = 50 at the start, held under max 60: one shift reaches 40.
    assert _earnable(_game({"type": "trait", "trait": "charm", "mult": 10, "max": 60})) is None


def test_a_capped_stat_value_below_the_gate_is_still_short():
    why = _earnable(_game({"type": "trait", "trait": "charm", "mult": 10, "max": 30}))
    assert why and "moves it only to 30" in why


def test_the_day_roll_paying_from_her_stats_is_a_farm():
    assert _earnable(_game({"type": "trait", "trait": "charm", "mult": 1}, where="tick")) is None


def test_random_reads_as_before():
    assert _earnable(_game({"type": "random", "min": 10, "max": 45})) is None
    assert "moves it only to 20" in _earnable(_game({"type": "random", "min": 10, "max": 20}))
