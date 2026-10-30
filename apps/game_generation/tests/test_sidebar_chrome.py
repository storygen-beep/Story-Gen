"""`[ui] sidebar_hide` and `[ui] phone_clock` (first_term DECISIONS 95).

  * `sidebar_hide = ["stats", "schedules", "flags"]` leaves those buttons out of the
    sidebar; the pages are still built. A name the engine does not know is an error.
  * `phone_clock = true` adds a clock in the top-left corner while the sidebar is
    closed on a narrow screen. Without it nothing is emitted.

    pytest apps/game_generation/tests/test_sidebar_chrome.py -q
"""
from apps.game_generation.twee_comprehensive.generators.v2 import (
    TweeComprehensiveGeneratorV2,
)
from apps.projects.services.game_graph import build_game_graph
from apps.projects.services.template_import import normalize, parse_toml, validate

FIXTURE = "apps/game_generation/games_toml_files/engine_skill_test_fixes_2026_09_30.toml"


def _twee(raw, dev=False):
    graph = build_game_graph(normalize(raw))
    return TweeComprehensiveGeneratorV2().generate(graph.project, {"dev_mode": dev}, graph=graph)


def _caption(twee):
    return next(p for p in twee.split("\n:: ") if p.startswith("StoryCaption")).split("\n\n")[0]


def test_without_the_keys_every_button_is_there():
    caption = _caption(_twee(parse_toml(FIXTURE)))
    for w in ("<<journalButton>>", "<<castButton>>", "<<statsButton>>", "<<scheduleButton>>"):
        assert w in caption
    assert "phone-clock" not in _twee(parse_toml(FIXTURE))


def test_hidden_buttons_leave_the_sidebar_but_the_pages_stay():
    raw = parse_toml(FIXTURE)
    raw["ui"]["sidebar_hide"] = ["stats", "schedules"]
    twee = _twee(raw)
    caption = _caption(twee)
    assert "<<statsButton>>" not in caption and "<<scheduleButton>>" not in caption
    assert "<<journalButton>>" in caption and "<<castButton>>" in caption
    assert "\n:: StatsPage" in twee and "\n:: SchedulePage" in twee


def test_an_unknown_button_is_an_error():
    raw = parse_toml(FIXTURE)
    raw["ui"]["sidebar_hide"] = ["stat"]
    assert any("unknown button 'stat'" in e for e in validate(normalize(raw)))
    raw["ui"]["sidebar_hide"] = "stats"
    assert any("sidebar_hide must be a list" in e for e in validate(normalize(raw)))


def test_the_phone_clock_is_emitted_only_when_asked():
    raw = parse_toml(FIXTURE)
    raw["ui"]["phone_clock"] = True
    twee = _twee(raw)
    assert "setup.updatePhoneClock" in twee and "#ui-bar.stowed ~ #phone-clock" in twee
