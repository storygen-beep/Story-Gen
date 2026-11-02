"""release_check.py: what counts as a save-visible id and a live flag key."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import release_check as rc  # noqa: E402


GAME = {"canvases": [{"id": "hub_theo_bar", "nodes": [{"id": "table"}],
                      "trigger": {"conditions": {"items": [{"type": "flag", "flag_key": "theo_knows_friday"}]}}}],
        "locations": [{"id": "hotel_bar"}], "npcs": [{"id": "npc_theo"}]}


def test_ids_cover_canvases_locations_npcs_but_not_nodes():
    assert rc.save_ids(GAME) == {"canvases:hub_theo_bar", "locations:hotel_bar", "npcs:npc_theo"}


def test_flag_keys_read_conditions_and_effects():
    game = dict(GAME, extra=[{"flag": "met_theo", "op": "set"}])
    assert rc.flag_keys(game) == {"theo_knows_friday", "met_theo"}
