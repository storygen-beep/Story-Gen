"""`[[ui.timetable]]` and `[ui] timetable_button` (first_term, R1_SYSTEM_COLLEGE_DAY.md, 2026-11-01).

Her classes as a real table: a dialog built like the people's schedule pop-up
(setup.castScheduleHtml), day chips with today picked, then one row per class: the time,
the class, the room and the lecturer. On today's rows the class on now says Now, the first
still to start says "Next · in N min", and a class already over is dimmed. Opened by
setup.openTimetable(day) from the sidebar button or any link. A game without the keys
carries none of it.

    pytest apps/game_generation/tests/test_timetable.py -q
"""
import pytest

from apps.game_generation.twee_comprehensive.generators.v2 import (
    TweeComprehensiveGeneratorV2,
)
from apps.projects.services.game_graph import build_game_graph
from apps.projects.services.template_import import normalize, parse_toml, validate

from .headless import build, needs_browser, open_game

FIXTURE = "apps/game_generation/games_toml_files/engine_skill_test_fixes_2026_09_30.toml"

ROWS = [
    {"class": "Psychology", "place": "loc_bar", "lecturer": "tobin", "weekdays": [0, 2, 4],
     "from": "08:30", "to": "10:00"},
    {"class": "Business", "place": "loc_shop", "weekdays": [0, 2], "from": "10:15", "to": "11:45"},
    {"class": "Biology", "place": "loc_club", "lecturer": "vic", "weekdays": [0], "from": "13:00", "to": "14:30"},
]

TIMETABLE_TOML = """
[[ui.timetable]]
class = "Psychology"
place = "loc_bar"
lecturer = "tobin"
weekdays = [0, 2, 4]
from = "08:30"
to = "10:00"

[[ui.timetable]]
class = "Business"
place = "loc_shop"
weekdays = [0, 2]
from = "10:15"
to = "11:45"

[[ui.timetable]]
class = "Biology"
place = "loc_club"
lecturer = "vic"
weekdays = [0]
from = "13:00"
to = "14:30"
"""


def _raw(rows=None, button=True):
    raw = parse_toml(FIXTURE)
    raw["ui"]["timetable"] = [dict(r) for r in (ROWS if rows is None else rows)]
    if button:
        raw["ui"]["timetable_button"] = True
    return raw


def _twee(raw):
    graph = build_game_graph(normalize(raw))
    return TweeComprehensiveGeneratorV2().generate(graph.project, {}, graph=graph)


def _errors(raw):
    return validate(normalize(raw))


# ── 1. the keys, their checks, and what they leave alone ─────────────────────


def test_a_game_without_the_keys_carries_none_of_it():
    twee = _twee(parse_toml(FIXTURE))
    assert "timetableHtml" not in twee and "timetableButton" not in twee and ".tt-row" not in twee


def test_the_fixture_with_a_timetable_is_clean():
    assert _errors(_raw()) == []


def test_the_rows_reach_the_page_and_the_button_the_sidebar():
    twee = _twee(_raw())
    assert 'setup.timetable = [{"class": "Psychology"' in twee
    assert '<<widget "timetableButton">>' in twee
    caption = next(p for p in twee.split("\n:: ") if p.startswith("StoryCaption"))
    assert "<<castButton>>\n<<timetableButton>>" in caption


def test_rows_without_the_button_have_the_screen_but_no_sidebar_line():
    twee = _twee(_raw(button=False))
    assert "setup.openTimetable = function" in twee
    assert "timetableButton" not in twee


@pytest.mark.parametrize(
    "mutation, fragment",
    [
        (lambda r: r[0].update(place="nowhere"), "'place' 'nowhere' is not a location id"),
        (lambda r: r[0].update(lecturer="nobody"), "'lecturer' 'nobody' is not an NPC id"),
        (lambda r: r[0].update(weekdays=[7]), "'weekdays' must be a non-empty list of 0-6"),
        (lambda r: r[0].update(weekdays=[]), "'weekdays' must be a non-empty list of 0-6"),
        (lambda r: r[0].update(**{"from": "8:30"}), "'from' must be \"HH:MM\""),
        (lambda r: r[0].update(to="08:00"), "'from' must be before 'to'"),
        (lambda r: r[0].update(**{"class": ""}), "'class' must be a non-empty string"),
        (lambda r: r[0].update(room="B12"), "unknown key 'room'"),
    ],
)
def test_a_bad_row_is_an_error(mutation, fragment):
    rows = [dict(r) for r in ROWS]
    mutation(rows)
    errs = _errors(_raw(rows))
    assert any(fragment in e for e in errs), errs


def test_a_button_with_no_rows_is_an_error():
    errs = _errors(_raw(rows=[]))
    assert any("timetable_button = true needs at least one" in e for e in errs), errs


# ── 2. behaviour, in the real engine ─────────────────────────────────────────


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    out = tmp_path_factory.mktemp("timetable")
    toml = out / "fixture.toml"
    text = open(FIXTURE).read().replace("\n[ui.cast_page]\n", "\n[ui]\ntimetable_button = true\n\n[ui.cast_page]\n", 1)
    toml.write_text(text + TIMETABLE_TOML)
    return build(toml, out / "out")


def _at(g, day, hour, minute=0):
    g.js("""([d, h, m]) => { const ts = SugarCube.State.variables.game_state.time_state;
        ts.current_day = d; ts.current_hour = h; ts.current_minute = m; }""", [day, hour, minute])


def _rows(g):
    return g.js("""() => [...document.querySelectorAll('.tt-row')].map(li => [
        li.querySelector('.tt-class').textContent, li.querySelector('.tt-where').textContent,
        li.className.replace('tt-row', '').trim()])""")


@needs_browser
def test_today_is_picked_and_now_next_and_over_are_marked(html):
    with open_game(html) as g:
        _at(g, "Monday", 10, 50)
        g.js("() => SugarCube.setup.openTimetable()")
        assert g.js("() => document.querySelector('.tt-day[aria-pressed=\"true\"]').textContent") == "Mon"
        rows = _rows(g)
        assert [r[0] for r in rows] == ["Psychology", "Business Now", "Biology Next · in 2 h 10 min"]
        assert rows[0][2] == "is-over" and rows[1][2] == "is-now" and rows[2][2] == "is-next"
        # Room and lecturer, from the locations and the NPCs; no lecturer, no dot.
        assert rows[0][1].startswith(g.js("() => SugarCube.setup.locations.loc_bar.name") + " · ")
        assert " · " not in rows[1][1]
        assert g.errors == []


@needs_browser
def test_a_day_chip_redraws_that_day_without_now_or_next(html):
    with open_game(html) as g:
        _at(g, "Monday", 9)
        g.js("() => SugarCube.setup.openTimetable()")
        g.js("() => document.querySelector('.tt-day[data-day=\"4\"]').click()")
        assert g.js("() => document.querySelector('.tt-day[aria-pressed=\"true\"]').textContent") == "Fri"
        assert _rows(g) == [["Psychology", _rows(g)[0][1], ""]]
        g.js("() => document.querySelector('.tt-day[data-day=\"5\"]').click()")
        assert g.js("() => document.querySelector('.tt-none').textContent") == "No classes this day."
        assert g.errors == []


@needs_browser
def test_the_sidebar_button_opens_it(html):
    with open_game(html) as g:
        _at(g, "Wednesday", 7)
        g.js("() => { const a = [...document.querySelectorAll('#timetable-btn-widget a')][0]; a.click(); }")
        assert g.js("() => document.querySelector('#ui-dialog-title').textContent") == "Timetable"
        rows = _rows(g)
        assert [r[0] for r in rows] == ["Psychology Next · in 1 h 30 min", "Business"]
        assert g.errors == []


# ── 3. late_until and the button's look (first_term DECISIONS 235, 237) ─────


def test_late_until_is_accepted_and_reaches_the_page():
    rows = [dict(r) for r in ROWS]
    rows[0]["late_until"] = "09:15"
    raw = _raw(rows)
    assert _errors(raw) == []
    assert '"late_until": "09:15"' in _twee(raw)


@pytest.mark.parametrize("value, fragment", [
    ("9:15", "'late_until' must be \"HH:MM\""),
    ("08:30", "'late_until' must be after 'from'"),
    ("10:30", "no later than 'to'"),
])
def test_a_bad_late_until_is_an_error(value, fragment):
    rows = [dict(r) for r in ROWS]
    rows[0]["late_until"] = value
    errs = _errors(_raw(rows))
    assert any(fragment in e for e in errs), errs


def test_the_timetable_button_is_styled_like_the_others():
    twee = _twee(_raw())
    assert '<div id="timetable-btn-widget"><<link "Timetable">>' in twee and 'class="nav-i">🗓</span>' in twee
    for sel in ("#timetable-btn-widget, #flags-btn-widget {", "#timetable-btn-widget a,",
                "#timetable-btn-widget .nav-row {", "#timetable-btn-widget a:hover {"):
        assert sel in twee, sel
