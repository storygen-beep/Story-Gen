"""`[ui] quests_layout = "hints"`: the Quests page as Course of Temptation's Hints page.

LO 2026-11-25: "completely aligned with the cots pages. Dont do anything extra." The page is
CoT's StoryHints passage and its <<hintlist>> widget (StoryHintWidgets.txt:7-139), drawn from
`[[story_hints]]` entries, one per CoT `setup.storyhints.db` entry:

  * an entry shows while its `when` holds (CoT's displayif);
  * its hint is the text of the LAST passed pair; none passed reads "Keep exploring!"; every
    pair passed with more than one pair is "Completed ✅", grey; a single passed pair stays
    In Progress; the text "end" is CoT's end-of-storyline line;
  * redesigned (card P80, LO 2026-11-27): "Next up", category chips kept in the save ($hintCat),
    finished storylines in a "Done (N)" fold, "New" / "Updated" tags against $hints_seen;
  * the sidebar button glows until the page is first opened ($firsttime.tutorial in CoT), then
    reads "N new" while a line has changed;
  * `[[walkthroughs]]` are CoT's *Walkthrough passages: ← Quests, Overview, Steps with the
    ✅ ➡️ 💡 ❓ 🛑 markers, a guard, and {days_until:N} day counts.

    pytest apps/game_generation/tests/test_cot_hints.py -q
"""
import os

import pytest

from apps.game_generation.twee_comprehensive.generators.v2 import (
    TweeComprehensiveGeneratorV2,
)
from apps.projects.services.game_graph import build_game_graph
from apps.projects.services.template_import import normalize, parse_toml, validate

from .headless import build, needs_browser, open_game

FIXTURE = os.path.join(os.path.dirname(__file__), "data", "cot_pages_2026_11_25.toml")
OTHER = "apps/game_generation/games_toml_files/engine_skill_test_fixes_2026_09_30.toml"
END_LINE = (
    "You have reached the end of this storyline... for now! "
    "But there may still be recurring events."
)


def _twee(raw):
    graph = build_game_graph(normalize(raw))
    return TweeComprehensiveGeneratorV2().generate(graph.project, {}, graph=graph)


def _errors(mutate):
    raw = parse_toml(FIXTURE)
    mutate(raw)
    return validate(normalize(raw))


# ── 1. the keys and their checks ─────────────────────────────────────────────


def test_the_fixture_is_valid():
    assert validate(normalize(parse_toml(FIXTURE))) == []


def test_without_the_key_nothing_of_the_hints_page_is_emitted():
    twee = _twee(parse_toml(OTHER))
    assert "setup.hintsHtml" not in twee and "story_hints" not in twee


def test_the_hints_page_replaces_the_quests_page():
    twee = _twee(parse_toml(FIXTURE))
    assert "setup.hintsHtml" in twee
    assert twee.count("\n:: QuestsPage") == 1
    assert "<<renderQuestsCard _card>>" not in twee


def test_hints_need_the_v2_engine():
    def m(raw):
        raw["project"]["quests_engine"] = "v1"

    assert any('quests_layout = "hints" requires' in e for e in _errors(m))


def test_story_hints_without_the_layout_are_an_error():
    def m(raw):
        del raw["ui"]["quests_layout"]

    errs = _errors(m)
    assert any(
        "[[story_hints]]" in e and 'quests_layout = "hints"' in e for e in errs
    ), errs
    assert any("[[walkthroughs]]" in e for e in errs), errs


def test_a_hint_entry_is_checked():
    def m(raw):
        raw["story_hints"][0]["walkthrough"] = "nope"
        raw["story_hints"][1]["hints"] = []
        raw["story_hints"][2]["category"] = ""
        raw["story_hints"][3]["title"] = "The Job"
        raw["story_hints"][0]["hints"][1]["when"] = [{"flag": "job_got", "op": "maybe"}]
        raw["story_hints"][0]["colour"] = "red"

    errs = _errors(m)
    for want in (
        "walkthrough 'nope' not found",
        "hints must list at least one",
        "category is required",
        "duplicate title 'The Job'",
        "flag condition op must be is_true/is_false",
        "unknown key 'colour'",
    ):
        assert any(want in e for e in errs), (want, errs)


def test_a_walkthrough_is_checked():
    def m(raw):
        wt = raw["walkthroughs"][0]
        wt["steps"][0]["kind"] = "maybe"
        wt["steps"][1]["text"] = ""
        wt["steps"][2]["todo_text"] = ""

    errs = _errors(m)
    for want in (
        "kind must be one of",
        "needs `text`",
        "needs `done_text` and `todo_text`",
    ):
        assert any(want in e for e in errs), (want, errs)


# ── 2. behaviour, in the real engine ─────────────────────────────────────────
# The page as redesigned (card P80, LO 2026-11-27): the same words; a "Next up" card, category
# chips, two columns, "New" / "Updated" tags, a Done fold, ← Back at the top.


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    return build(FIXTURE, tmp_path_factory.mktemp("cot_hints") / "out")


def _flags(g, **flags):
    g.js("(f) => Object.assign(SugarCube.State.variables.flags, f)", flags)


def _open(g):
    clicked = g.js(
        """() => { const a = [...document.querySelectorAll('#journal-btn-widget a')]
            .find(x => x.textContent.trim() === 'Quests');
            if (!a) return false; a.click(); return true; }"""
    )
    assert clicked
    g.page.wait_for_timeout(150)


def _entries(g):
    """{title: [category, line, done, next, tag]} for each card on the page."""
    rows = g.js(
        """() => [...document.querySelectorAll('.passage .hint-card')].map(b => [
            b.querySelector('.hint-title').textContent.trim(),
            b.querySelector('.hint-category').textContent.trim(),
            b.querySelector('.hint-line').textContent.replace(/\\s+/g, ' ').trim(),
            b.classList.contains('hint-done'),
            b.classList.contains('hint-next-card'),
            (b.querySelector('.hint-tag') || {textContent: ''}).textContent.trim()])"""
    )
    return {r[0]: r[1:] for r in rows}


def _grid(g):
    """The open cards below "Next up", in order."""
    return g.js(
        """() => [...document.querySelectorAll('.passage #hintlist .hint-card:not(.hint-done) .hint-title')]
            .map(t => t.textContent.trim())"""
    )


def _chips(g):
    return g.js(
        "() => [...document.querySelectorAll('.passage .hint-chip')].map(c => [c.textContent.trim(), c.classList.contains('active')])"
    )


def _chip(g, label):
    g.js(
        """(l) => [...document.querySelectorAll('.passage .hint-chip')]
            .find(c => c.textContent.trim() === l).click()""",
        label,
    )
    g.page.wait_for_timeout(100)


def _fold(g):
    return g.js(
        "() => (document.querySelector('.passage .hint-done-toggle') || {textContent: ''}).textContent.trim()"
    )


def _toggle_fold(g):
    g.js("() => document.querySelector('.passage .hint-done-toggle').click()")
    g.page.wait_for_timeout(100)


def _badge(g):
    return g.js(
        "() => (document.querySelector('#journal-btn-widget .nav-badge') || {textContent: ''}).textContent.trim()"
    )


@needs_browser
def test_the_ladder(html):
    with open_game(html) as g:
        _open(g)
        assert (
            g.js("() => document.querySelector('.passage .cot-page-title').textContent.trim()")
            == "Quests"
        )
        rows = _entries(g)
        assert set(rows) == {"The Job", "Free Time"}  # The Quad waits on `started`, Hidden never
        # No storyline is open, so the first open entry is "Next up".
        assert rows["The Job"][0] == "Employment 💼"
        assert rows["The Job"][1] == "Go to the bar and ask for work."
        assert rows["The Job"][3] is True
        # A single pair that passes stays open.
        assert rows["Free Time"][1] == "Visit the park." and rows["Free Time"][2] is False
        assert _grid(g) == ["Free Time"]

        _flags(g, started=True, job_got=True)
        _open(g)
        rows = _entries(g)
        assert rows["The Quad"][1] == "Keep exploring!"
        assert rows["The Quad"][3] is True  # a Storyline entry takes "Next up"
        assert rows["The Job"][1] == "Work the shifts."
        assert "Hidden" not in rows
        assert _grid(g) == ["The Job", "Free Time"]

        _flags(g, job_done=True)
        _open(g)
        assert "The Job" not in _entries(g)  # folded away
        assert _fold(g) == "▸ Done (1)"
        assert "2 open · 1 done" in g.js("() => document.querySelector('.passage .cot-head').textContent")
        _toggle_fold(g)
        assert _fold(g) == "▾ Done (1)"
        job = _entries(g)["The Job"]
        assert job[1] == END_LINE and job[2] is True
        assert "Done" in g.js(
            """() => [...document.querySelectorAll('.passage .hint-card')]
                .find(b => b.querySelector('.hint-title').textContent.trim() === 'The Job').textContent"""
        )
        assert g.errors == []


@needs_browser
def test_the_chips_and_the_done_fold(html):
    with open_game(html) as g:
        _flags(g, started=True, job_got=True, job_done=True)
        _open(g)
        assert _chips(g) == [
            ["All", True],
            ["Employment 💼", False],
            ["Campus Life 🏫", False],
            ["Storyline 📖", False],
        ]
        _chip(g, "Campus Life 🏫")
        assert _grid(g) == ["Free Time"]
        assert _fold(g) == ""  # nothing done in that category
        assert _entries(g)["The Quad"][3] is True  # "Next up" stays whatever the chip
        assert g.sv("hintCat") == "Campus Life 🏫"
        _chip(g, "Employment 💼")
        assert _grid(g) == []
        assert _fold(g) == "▸ Done (1)"
        # Kept in the game's state, so the page reopens as she left it.
        _open(g)
        assert ["Employment 💼", True] in _chips(g)
        _chip(g, "All")
        assert g.sv("hintCat") is None
        assert _grid(g) == ["Free Time"] and _fold(g) == "▸ Done (1)"
        assert g.errors == []


@needs_browser
def test_the_button_glows_then_counts_what_changed(html):
    with open_game(html) as g:
        assert g.js("() => !!document.querySelector('#journal-btn-widget .glow')")
        _open(g)
        assert g.sv("hints_opened") is True
        # The first opening tags nothing.
        assert all(r[4] == "" for r in _entries(g).values())
        g.play("Location_loc_home")
        assert not g.js("() => !!document.querySelector('#journal-btn-widget .glow')")
        assert _badge(g) == ""

        _flags(g, started=True)  # The Quad appears
        g.play("Location_loc_home")
        assert _badge(g) == "1 new"
        _open(g)
        assert _entries(g)["The Quad"][4] == "New"
        g.play("Location_loc_home")
        assert _badge(g) == ""

        _flags(g, job_got=True)  # The Job's line moves on
        g.play("Location_loc_home")
        assert _badge(g) == "1 new"
        _open(g)
        rows = _entries(g)
        assert rows["The Job"][4] == "Updated" and rows["The Quad"][4] == ""
        g.play("Location_loc_home")
        assert _badge(g) == ""
        assert g.errors == []


def _walkthrough(g):
    g.js("() => document.querySelector('.passage .hints-see-here').click()")
    g.page.wait_for_timeout(150)
    return g.js("() => document.querySelector('.passage').innerText")


@needs_browser
def test_the_walkthrough(html):
    with open_game(html) as g:
        _open(g)
        assert g.js(
            """() => [...document.querySelectorAll('.passage .hint-card')]
                .find(b => b.querySelector('.hint-title').textContent.trim() === 'The Job')
                .querySelector('.hints-see-here').textContent.trim()"""
        ) == "Walkthrough →"

        # The guard: before `started` the page says only its line.
        text = _walkthrough(g)
        assert (
            g.js("() => document.querySelector('.passage .cot-page-title').textContent.trim()")
            == "Walkthrough: The Job"
        )
        assert "← Quests" in text
        assert "You haven't met them yet." in text and "Overview" not in text

        _flags(g, started=True)
        _open(g)
        text = _walkthrough(g)
        assert "Overview" in text and "Steps" in text
        assert "It will take at least 4 more days." in text  # day 1 of 5
        assert "➡️ Ask at the bar." in text
        assert (
            "Wear something nice." not in text
        )  # nothing after the first step still to do

        _flags(g, job_got=True)
        g.advance_days(3)
        _open(g)
        text = _walkthrough(g)
        assert "It will take at least 1 more day." in text
        assert "✅ You got the job." in text
        assert "💡 Wear something nice." in text
        assert "➡️ Work three shifts." in text

        g.advance_days(9)
        _open(g)
        assert "It will take at least 0 more days." in _walkthrough(g)

        g.js("() => document.querySelector('#help-backward').click()")
        g.page.wait_for_timeout(150)
        assert (
            g.js("() => document.querySelector('.passage .cot-page-title').textContent.trim()")
            == "Quests"
        )
        assert g.errors == []


@needs_browser
def test_quests_and_a_walkthrough_are_pages_with_back_at_the_top(html):
    """LO 2026-11-26: "They should have their own page." No dialog opens. P80: one ← Back, at
    the top; a walkthrough's ← Quests goes to the Quests page."""
    with open_game(html) as g:
        g.play("Location_loc_home")
        _open(g)
        assert g.passage() == "QuestsPage" and not g.js("() => SugarCube.Dialog.isOpen()")
        backs = g.js(
            "() => [...document.querySelectorAll('.passage a')].filter(a => a.textContent.trim() === '← Back')"
            ".map(a => !!a.closest('.cot-head'))"
        )
        assert backs == [True]
        g.js("() => document.querySelector('.passage .hints-see-here').click()")
        g.page.wait_for_timeout(150)
        assert g.passage() == "QuestsWalkthrough" and not g.js("() => SugarCube.Dialog.isOpen()")
        assert not g.js(
            "() => [...document.querySelectorAll('.passage a')].some(a => a.textContent.trim() === '← Back')"
        )
        g.js("() => document.querySelector('#help-backward').click()")
        g.page.wait_for_timeout(150)
        assert g.passage() == "QuestsPage"
        g.js("() => document.querySelector('.passage .cot-back').click()")
        g.page.wait_for_timeout(150)
        assert g.passage() == "Location_loc_home"
        assert g.errors == []
