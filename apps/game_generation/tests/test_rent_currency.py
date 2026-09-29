"""EN2c — the short-pay line prints the rent currency symbol.

PRD_SKILL_TEST_FIXES_v2 §2 EN2c (I5 follow-up). RentDay_Short's grace line typed "$"
into "You have: … You need: …", the one rent screen that ignored `[settings.rent]
currency_symbol`; a game in pounds showed dollars on the screen she sees when she cannot
pay. It now sets `_cur` like the other rent pages. With the default "$" the rendered text
is unchanged.

Old saves (§0 rule 8): no new state, so nothing about a save changes; a save the
pre-change build wrote loads into a "£" build and shows "£" on the short screen.

    pytest apps/game_generation/tests/test_rent_currency.py -q
"""
import pytest

from apps.projects.services.game_graph import build_game_graph
from apps.projects.services.template_import import normalize, parse_toml
from apps.game_generation.twee_comprehensive.generators.v2 import (
    TweeComprehensiveGeneratorV2,
)

from .headless import build, needs_browser, open_game, read_data
from .test_rent_stages import FIXTURE, _rent_day, _text


def _pounds_text():
    text = open(FIXTURE).read()
    anchor = 'start_after_flag = "rent_on"\n'
    assert text.count(anchor) == 1
    return text.replace(anchor, anchor + 'currency_symbol  = "£"\n')


def _short_passage():
    graph = build_game_graph(normalize(parse_toml(FIXTURE)))
    twee = TweeComprehensiveGeneratorV2().generate(graph.project, {}, graph=graph)
    return next(p for p in twee.split("\n:: ") if p.startswith("RentDay_Short"))


def test_the_short_screen_types_no_dollar():
    short = _short_passage()
    assert "$<<print" not in short
    assert short.count("<<print _cur>>") == 2


@pytest.fixture(scope="module")
def pounds_html(tmp_path_factory):
    out = tmp_path_factory.mktemp("en2c")
    toml = out / "fixture.toml"
    toml.write_text(_pounds_text())
    return build(toml, out / "out")


@pytest.fixture(scope="module")
def dollars_html(tmp_path_factory):
    return build(FIXTURE, tmp_path_factory.mktemp("en2c_default") / "out")


def _come_up_short(g):
    _rent_day(g, money=20)
    g.click("Tell them you can't pay")
    assert g.passage() == "RentDay_Short"
    return _text(g)


@needs_browser
def test_a_game_in_pounds_is_short_in_pounds(pounds_html):
    with open_game(pounds_html) as g:
        text = _come_up_short(g)
        assert "You have: £20. You need: £100." in text
        assert "$" not in text
        assert g.errors == []


@needs_browser
def test_the_default_still_reads_dollars(dollars_html):
    with open_game(dollars_html) as g:
        assert "You have: $20. You need: $100." in _come_up_short(g)
        assert g.errors == []


@needs_browser
def test_a_save_made_before_en2c_shows_the_symbol(pounds_html):
    """§0 rule 8. The save EN2b's tests use: written by a pre-EN2c build (the EN2a tree)
    after one grace warning, parked on Location_loc_home. With that warning used, its
    next short week is the eviction screen, which prints no amount; the count is cleared
    so the test reaches the grace line it is about."""
    with open_game(pounds_html) as g:
        assert g.load_save(read_data("en2b_pre_change_save.txt")) is True
        assert g.passage() == "Location_loc_home"
        g.js("() => { SugarCube.State.variables.game_state.rent_state.warnings = 0; }")
        assert "You have: £20. You need: £100." in _come_up_short(g)
        assert g.errors == []
