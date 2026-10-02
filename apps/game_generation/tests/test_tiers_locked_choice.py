"""E15 (World and Systems PRD) — a locked choice is not shown as a way to raise a trait.

An activity's tiers are the choices on its menu node. The trait-help modal ("where can I
raise X?") skips a tier whose conditions don't hold, and lists the activity with the best
bonus among the tiers that are left. The tier reader kept a `node` tier's choice
conditions but dropped them for `trigger` and `return` tiers, so a locked choice of
either kind was listed as a way to raise the trait while she couldn't pick it. All three
now carry their choice's conditions.

    pytest apps/game_generation/tests/test_tiers_locked_choice.py -q
"""
import json
import re
from pathlib import Path

import pytest

from .headless import build, needs_browser, open_game

FIXTURE = "apps/game_generation/games_toml_files/engine_ws_tiers_locked_2026_10_02.toml"
LOCK = {"type": "trait", "subject": "player", "trait_key": "fitness", "operator": "gte", "value": 20}


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    return build(FIXTURE, tmp_path_factory.mktemp("tiers_locked") / "out")


@pytest.fixture(scope="module")
def help_data(html):
    text = Path(html).read_text()
    start = re.search(r"setup\.help_data = ", text).end()
    return json.JSONDecoder().raw_decode(text, start)[0]


def _tier_conditions(help_data, name):
    found = [a for a in help_data["player"]["activities"] if a["name"] == name]
    assert len(found) == 1, f"{name!r} listed {len(found)} times"
    return [t["conditions"] for t in found[0]["tiered_effects"]]


@pytest.mark.parametrize("name", ["Spar", "Swim", "Row"])
def test_a_trigger_or_return_tier_keeps_its_choice_conditions(help_data, name):
    locked, open_ = _tier_conditions(help_data, name)
    assert locked["items"] == [LOCK]
    assert open_ is None


def _modal_rows(game, fitness):
    """Set her fitness, open "how to increase fitness", return {activity: bonus text}."""
    return game.js(
        """(f) => {
            SugarCube.State.variables.player.core_traits.fitness = f;
            SugarCube.setup.closeTraitModal();
            SugarCube.setup.showTraitActivitiesModal('', 'fitness', 30);
            const rows = {};
            document.querySelectorAll('.trait-activity-list li').forEach(li => {
                rows[li.querySelector('.activity-name').textContent] =
                    li.querySelector('.activity-bonus').textContent.split(' ')[0];
            });
            return rows;
        }""",
        fitness,
    )


@needs_browser
def test_a_locked_choice_shows_only_once_its_condition_holds(html):
    with open_game(html) as game:
        # Locked: Spar (trigger) and Swim (return) raise nothing she can pick;
        # Row lists its open choice's +1, not the locked +5.
        assert _modal_rows(game, 10) == {"Row": "+1"}
        # Open: every locked choice now counts.
        assert _modal_rows(game, 20) == {"Spar": "+4", "Swim": "+3", "Row": "+5"}
        assert game.errors == []
