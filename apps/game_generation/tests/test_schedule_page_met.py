"""The Schedules page names only people the player has met.

Who is listed is the quest cards' decision, as on CastPage (setup.castRoster): an NPC with
any [[quest_cards]] entry is listed only while one of those cards' `when` holds, and a card
with `heading` lists the heading, not the name. An NPC with no quest card is listed as
before. The filter sits on the SchedulePage passage, not in getNpcsWithSchedules, because the
rows must stay live for presence: a meeting needs its person there.

The failure (2026-11-24): first_term_lean's Schedules page named Tom and Chris, with their
hours, from the game's first minute, before she had met either, against its plan's "no one
is named before she meets them".

    pytest apps/game_generation/tests/test_schedule_page_met.py -q
"""
import os

import pytest

from .headless import build, needs_browser, open_game

GAME = "games/first_term_lean/toml_phases/7_final_game.toml"

pytestmark = pytest.mark.skipif(
    not os.path.exists(GAME), reason="first_term_lean not present"
)


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    return build(GAME, tmp_path_factory.mktemp("schedule_met") / "out")


def _listed(g):
    g.play("SchedulePage")
    return g.js(
        "() => [...document.querySelectorAll('.passage .npc-name')].map(h => h.innerText.trim())"
    )


def _set_flag(g, flag):
    g.js("(f) => { SugarCube.State.variables.flags[f] = true; }", flag)


@needs_browser
def test_unmet_people_are_not_named(html):
    with open_game(html) as g:
        names = _listed(g)
        assert "Tom" not in names and "Chris" not in names, names
        assert g.errors == []


@needs_browser
def test_a_person_is_named_once_met(html):
    with open_game(html) as g:
        _set_flag(g, "met_tom")
        names = _listed(g)
        assert "Tom" in names, names
        assert "Chris" not in names, names
        assert g.errors == []


def test_the_filter_sits_on_the_page_and_reads_the_quest_cards():
    with open(
        "apps/game_generation/twee_comprehensive/generators/v2.py", encoding="utf-8"
    ) as fh:
        src = fh.read()
    page = src[src.index(":: SchedulePage") :]
    page = page[: page.index("<<for _npcInfo range _npcsWithSchedules>>")]
    assert "setup.pickQuestsCard(slug)" in page
    assert "card.heading" in page
