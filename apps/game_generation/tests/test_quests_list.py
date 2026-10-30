"""`[ui] quests_layout = "list"` (first_term DECISIONS 97).

The V2 quests page drawn as short tap-to-open rows: the story cards first ("My story"),
then one row per person, ready first and soonest first, the people whose arc is finished
folded at the bottom. The cards and their words are the same as the cards layout; only
the drawing changes. Without the key the page is the cards page, byte for byte.

    pytest apps/game_generation/tests/test_quests_list.py -q
"""
import pytest

from apps.game_generation.twee_comprehensive.generators.v2 import (
    TweeComprehensiveGeneratorV2,
)
from apps.projects.services.game_graph import build_game_graph
from apps.projects.services.template_import import normalize, parse_toml, validate

from .headless import build, needs_browser, open_game

FIXTURE = "apps/game_generation/games_toml_files/engine_skill_test_fixes_2026_09_30.toml"

# A story card with a counted goal, so the closed row has a bar to draw.
STORY_CARD = """
[[quest_cards]]
text  = "Get bolder: the bar notices."
when  = [ { flag = "started", op = "is_true" } ]
goals = [ { type = "trait", subject = "player", trait = "corr", op = "gte", value = 20, label = "Reach 20 corruption" } ]
tip   = "Stay late at the bar."
"""


def _twee(raw):
    graph = build_game_graph(normalize(raw))
    return TweeComprehensiveGeneratorV2().generate(graph.project, {}, graph=graph)


def _passage(twee, name):
    return next(p for p in twee.split("\n:: ") if p.startswith(name + "\n") or p.startswith(name + " "))


# ── 1. the key, its checks, and what it leaves alone ─────────────────────────


def test_without_the_key_the_cards_page_is_untouched():
    twee = _twee(parse_toml(FIXTURE))
    page = _passage(twee, "QuestsPage")
    assert "<<renderQuestsCard _card>>" in page
    assert "QuestsListScript" not in twee and "questsRoster" not in twee


def test_the_list_replaces_only_the_page():
    raw = parse_toml(FIXTURE)
    raw["ui"]["quests_layout"] = "list"
    assert validate(normalize(raw)) == []
    twee = _twee(raw)
    page = _passage(twee, "QuestsPage")
    assert "setup.questsRoster()" in page and "<<renderQuestsCard" not in page
    # The V2 script and widget stay; the page appears once.
    assert '<<widget "renderQuestsCard">>' in twee
    assert twee.count("\n:: QuestsPage") == 1


def test_a_bad_value_and_a_v1_game_are_errors():
    raw = parse_toml(FIXTURE)
    raw["ui"]["quests_layout"] = "rows"
    assert any("quests_layout must be one of cards, list" in e for e in validate(normalize(raw)))
    raw["ui"]["quests_layout"] = "list"
    raw["project"]["quests_engine"] = "v1"
    assert any('quests_layout = "list" requires' in e for e in validate(normalize(raw)))


# ── 2. behaviour, in the real engine ─────────────────────────────────────────


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    out = tmp_path_factory.mktemp("quests_list")
    toml = out / "fixture.toml"
    text = open(FIXTURE).read().replace("\n[ui.cast_page]\n", '\n[ui]\nquests_layout = "list"\n\n[ui.cast_page]\n', 1)
    toml.write_text(text + STORY_CARD)
    return build(toml, out / "out")


def _at(g, day, hour, minute=0):
    g.js("""([d, h, m]) => { const v = SugarCube.State.variables, ts = v.game_state.time_state;
        ts.current_day = d; ts.current_hour = h; ts.current_minute = m; v.flags.started = true; }""",
         [day, hour, minute])


@needs_browser
def test_rows_start_closed_story_first(html):
    with open_game(html) as g:
        _at(g, "Monday", 12)
        g.play("QuestsPage")
        rows = g.js("""() => [...document.querySelectorAll('.quests-list details.quests-row')].map(d =>
            [d.open, d.classList.contains('quests-story-row')])""")
        assert rows == [[False, True], [False, False], [False, False]]
        assert g.js("() => document.querySelector('.quests-progress').textContent.trim()") == "5 / 20"
        names = g.js("() => [...document.querySelectorAll('.quests-name')].map(n => n.textContent)")
        assert names == ["Tobin", "Vic"]
        # The open row holds the card's text and its tip, as written.
        g.js("() => document.querySelector('.quests-story-row > summary').click()")
        body = g.js("() => document.querySelector('.quests-story-row .quests-body').innerText")
        assert "Get bolder: the bar notices." in body and "Stay late at the bar." in body
        assert g.errors == []


@needs_browser
def test_the_next_window_is_counted_from_now(html):
    with open_game(html) as g:
        nxt = "(s) => SugarCube.setup.questsNextWindow(s).mins"
        tom = [{"weekdays": [0, 1, 2, 3, 4, 5], "startTime": "14:30", "endTime": "22:00"}]
        _at(g, "Monday", 15)
        assert g.js(nxt, tom) == 0                       # open now
        _at(g, "Monday", 12)
        assert g.js(nxt, tom) == 150                     # later today
        _at(g, "Saturday", 23)
        assert g.js(nxt, tom) == 24 * 60 + 15 * 60 + 30  # Sunday is off: Monday 14:30
        assert g.js("() => SugarCube.setup.questsNextWindow([]).mins === Infinity") is True  # no rows: last


@needs_browser
def test_ready_people_sort_soonest_first_and_finished_people_fold(html):
    with open_game(html) as g:
        _at(g, "Monday", 12)
        # Stub the cards: Vic ready today, Tobin ready on Wednesday, so Vic leads though he is second in the file.
        g.js("""() => { const s = SugarCube.setup, orig = s.pickQuestsCard;
            s.lookupCanvasBySlug = slug => ({ locUuid: 'x', canvas: { scheduleParams: [
                slug === 'vic_scene' ? { weekdays: [0], startTime: '18:00', endTime: '22:00' }
                                     : { weekdays: [2], startTime: '18:00', endTime: '22:00' } ] } });
            s.pickQuestsCard = n => Object.assign({}, orig(n), { ready_canvas: n === 'vic' ? 'vic_scene' : 'tobin_scene' }); }""")
        roster = g.js("() => SugarCube.setup.questsRoster().people.map(e => [e.name, e.ready, e.now, e.line])")
        assert roster[0][:3] == ["Vic", True, False] and roster[0][3].startswith("Today 6–10 PM")
        assert roster[1][:2] == ["Tobin", True] and roster[1][3].startswith("Wed 6–10 PM")
        _at(g, "Monday", 19)
        assert g.js("() => SugarCube.setup.questsRoster().people[0].now") is True
        # A finished arc leaves the people list for the fold.
        g.js("""() => { const s = SugarCube.setup, orig = s.pickQuestsCard;
            s.pickQuestsCard = n => n === 'tobin' ? Object.assign({}, orig(n), { terminal: true }) : orig(n); }""")
        r = g.js("() => { const q = SugarCube.setup.questsRoster(); return [q.people.map(e => e.name), q.done.map(e => e.name)]; }")
        assert r == [["Vic"], ["Tobin"]]
        g.play("QuestsPage")
        assert "Finished (1)" in g.js("() => document.querySelector('.quests-done-fold').innerText")
        assert g.errors == []
