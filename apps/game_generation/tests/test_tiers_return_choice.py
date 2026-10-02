"""E14 (World and Systems PRD) — an activity's tiers count `return` choices.

An activity's tiers are the choices on its menu node: each one lists the traits it raises,
and the trait-help modal ("where can I raise X?") shows an activity under a trait only
when one of its reachable tiers raises it. The tier reader counted `trigger` and `node`
choices only, so a `return` choice (E8c) raised nothing as far as the modal knew: on a
menu mixed with a `node` choice its effects were dropped, and an activity whose only
raising choice was a `return` one wasn't listed at all. A `return` choice now counts
exactly where a `trigger` one does: it can make a node the menu, and it is one tier with
its own effects.

    pytest apps/game_generation/tests/test_tiers_return_choice.py -q
"""
import json
import re
from pathlib import Path

import pytest

from .headless import build

FIXTURE = "apps/game_generation/games_toml_files/engine_ws_tiers_return_2026_10_02.toml"


@pytest.fixture(scope="module")
def help_data(tmp_path_factory):
    html = Path(build(FIXTURE, tmp_path_factory.mktemp("tiers") / "out")).read_text()
    start = re.search(r"setup\.help_data = ", html).end()
    return json.JSONDecoder().raw_decode(html, start)[0]


def _activity(help_data, name):
    found = [a for a in help_data["player"]["activities"] if a["name"] == name]
    assert len(found) == 1, f"{name!r} listed {len(found)} times"
    return found[0]


def _tiers(activity):
    return [sorted((e["trait"], e["value"]) for e in t["effects"]) for t in activity["tiered_effects"]]


def test_a_return_choice_is_a_tier_beside_a_node_choice(help_data):
    gym = _activity(help_data, "Gym session")
    assert _tiers(gym) == [[("fitness", 3)], [("charm", 1)]]
    assert gym["tiered_effects"][1]["conditions"] is None   # as a trigger tier
    assert "Gym session" in [a["name"] for a in help_data["trait_activities"]["charm"]]


def test_return_choices_alone_make_a_tiered_menu(help_data):
    walk = _activity(help_data, "Walk")
    assert _tiers(walk) == [[("energy", 2)], [("charm", 2)]]


def test_a_trigger_choice_is_still_a_tier(help_data):
    assert _tiers(_activity(help_data, "Sit")) == [[("charm", 1)]]
