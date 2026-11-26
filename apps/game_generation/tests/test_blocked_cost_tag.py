"""The tag on a greyed row names the cost she is short of, and never repeats a price.

LO 2026-11-26: a greyed gym row read "Work out ($5) (5 Money)", the price twice: the
author's label carries the price (lean craft/economy.md C1021) and the engine added its
own tag. The tag also always showed the FIRST cost listed, so a $5 + 20 energy row greyed
for energy said "5 Money", a false reason.

`setup.blockedCostTag(costs, label)` returns the first cost she can't pay, or '' when that
cost is money and the label already shows "$<value>". Both greyed-row renderers (the solo
row and the NPC portrait badge) go through it.

    pytest apps/game_generation/tests/test_blocked_cost_tag.py -q
"""
import inspect

import pytest

from apps.game_generation.twee_comprehensive.generators import v2

from .headless import build, needs_browser, open_game

FIXTURE = "apps/game_generation/games_toml_files/engine_skill_test_fixes_2026_09_30.toml"
WORKOUT = [{"trait": "money", "value": 5}, {"trait": "energy", "value": 20}]


def test_both_greyed_renderers_use_the_helper():
    src = inspect.getsource(v2)
    assert "setup.blockedCostTag(blocked.costs, bDisplayName)" in src
    assert "setup.blockedCostTag(activity.costs, '')" in src
    assert "blocked.costs[0]" not in src and "activity.costs[0]" not in src


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    return build(FIXTURE, tmp_path_factory.mktemp("blocked_cost_tag") / "out")


def _tag(g, money, energy, label):
    return g.js(
        """([m, e, costs, label]) => {
            const t = SugarCube.State.variables.player.core_traits;
            t.money = m; t.energy = e;
            return SugarCube.setup.blockedCostTag(costs, label); }""",
        [money, energy, WORKOUT, label],
    )


@needs_browser
def test_the_tag(html):
    with open_game(html) as g:
        # Short of money, the price is in the label: no tag, the price is the reason.
        assert _tag(g, 2, 100, "Work out ($5)") == ""
        money = _tag(g, 2, 100, "Work out")
        energy = _tag(g, 10, 5, "Work out ($5)")
        # Short of money, no price in the label: the tag says it.
        assert money.startswith("5 ") and energy != money, money
        # Short of energy only: the energy, not the first cost listed.
        assert energy.startswith("20 ") and money.split(" ", 1)[1] not in energy, energy
        # Short of both: the shown price is skipped, the energy is named.
        assert _tag(g, 2, 5, "Work out ($5)") == energy
        # Can pay all of it: no tag.
        assert _tag(g, 10, 100, "Work out ($5)") == ""
        # "$50" in a label is not the $5 price.
        assert _tag(g, 2, 100, "Work out ($50)") == money
        assert g.errors == []


# ── The greyed choice inside a scene (node choices) ─────────────────────────
# LO 2026-11-27: the gym desk's "Day pass ($5)" greyed as
# "Day pass ($5) (Requires 5 Money (you have 2))". The node-choice rung now passes its
# label to getCostBlockedMessage, which leaves out a money cost the label already shows.


def test_the_node_choice_rung_passes_its_label():
    src = inspect.getsource(v2)
    assert "setup.getCostBlockedMessage({choice_costs_js}, {_cost_label_js})" in src
    assert "<<if _costMsg>> (<<= _costMsg>>)<</if>>" in src


def _msg(g, money, energy, costs, label):
    return g.js(
        """([m, e, costs, label]) => {
            const t = SugarCube.State.variables.player.core_traits;
            t.money = m; t.energy = e;
            return SugarCube.setup.getCostBlockedMessage(costs, label); }""",
        [money, energy, costs, label],
    )


@needs_browser
def test_the_node_choice_message(html):
    day = [{"trait": "money", "value": 5}]
    with open_game(html) as g:
        # Short of money, the price is in the label: nothing added.
        assert _msg(g, 2, 100, day, "Day pass ($5)") == ""
        # Without a label it reads as before.
        before = _msg(g, 2, 100, day, None)
        assert before.startswith("Requires 5 ") and before.endswith("(you have 2)"), before
        # No price in the label: the money is still named.
        assert _msg(g, 2, 100, day, "Day pass") == before
        # "$50" is not the $5 price.
        assert _msg(g, 2, 100, day, "Day pass ($50)") == before
        # Short of money and energy, the price shown: only the energy is named.
        both = _msg(g, 2, 5, WORKOUT, "Work out ($5)")
        assert both.startswith("Requires 20 ") and "you have 5" in both and ". " not in both, both
        # The row tag still agrees.
        assert _tag(g, 2, 100, "Work out ($5)") == ""
        assert g.errors == []
