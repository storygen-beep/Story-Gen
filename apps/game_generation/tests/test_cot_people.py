"""`[ui] people_page = "cot"`: the People page as Course of Temptation's People dialog.

LO 2026-11-25 chose "CoT's shape only": the layout and behaviour of CoT's Social passage
(Social.txt, SocialWidgets.txt) and its View Person dialog (DisplayNPC.txt,
DisplayNPCWidgets.txt), filled from systems the game already has. What is checked here:

  * the sidebar button reads "People (N)", N = the people at her place now;
  * 📍 People Here lists everyone present, met or not; a stranger by `stranger_name`;
  * a tab is built only when some person is filed under it (`people_tab`), in CoT's order,
    and shows CoT's empty line while nobody in it is known yet;
  * the 🔎 search (a stranger matches by `stranger_name` only), the sort links, paging at
    16 a page with "Page x/y";
  * the View Person dialog: "???" and "??" for a stranger with CoT's "You're not sure who
    this is."; for a known person the name, initials, role · relationship and their meters;
    "💬 Talk to …" when she is with them and a Talk row is there, "💭 … again" once used today.

    pytest apps/game_generation/tests/test_cot_people.py -q
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


def _twee(raw):
    graph = build_game_graph(normalize(raw))
    return TweeComprehensiveGeneratorV2().generate(graph.project, {}, graph=graph)


def _errors(mutate):
    raw = parse_toml(FIXTURE)
    mutate(raw)
    return validate(normalize(raw))


# ── 1. the keys and their checks ─────────────────────────────────────────────


def test_without_the_key_the_cast_page_is_untouched():
    twee = _twee(parse_toml(OTHER))
    assert "setup.peopleOpen" not in twee
    assert '<<link "The Cast" "CastPage">>' in twee


def test_the_people_dialog_replaces_the_cast_page():
    twee = _twee(parse_toml(FIXTURE))
    assert "setup.peopleOpen" in twee
    assert twee.count("\n:: CastPage") == 1
    assert (
        "setup.castRoster()"
        not in twee.split("\n:: CastPage", 1)[1].split("\n:: ", 1)[0]
    )


def test_the_people_keys_are_checked():
    def bad_value(raw):
        raw["ui"]["people_page"] = "yes"

    assert any("people_page must be" in e for e in _errors(bad_value))

    def no_cast_page(raw):
        del raw["ui"]["cast_page"]

    assert any(
        'people_page = "cot" requires [ui.cast_page]' in e
        for e in _errors(no_cast_page)
    )

    def bad_tab(raw):
        raw["npcs"][0]["people_tab"] = "family"

    assert any("people_tab must be one of" in e for e in _errors(bad_tab))

    def keys_without_page(raw):
        del raw["ui"]["people_page"]

    errs = _errors(keys_without_page)
    assert any("stranger_name" in e and 'people_page = "cot"' in e for e in errs), errs


# ── 2. behaviour, in the real engine ─────────────────────────────────────────


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    return build(FIXTURE, tmp_path_factory.mktemp("cot_people") / "out")


def _at(g, place, **flags):
    g.js("(f) => Object.assign(SugarCube.State.variables.flags, f)", flags)
    g.play(place)


def _button(g):
    return g.js("() => document.querySelector('#cast-btn-widget a').textContent.trim()")


def _open(g):
    g.js("() => document.querySelector('#cast-btn-widget a').click()")
    g.page.wait_for_timeout(150)


def _names(g):
    return g.js(
        "() => [...document.querySelectorAll('.passage .view-people-person-name a')]"
        ".map(a => a.textContent.trim())"
    )


def _tabs(g):
    return g.js(
        "() => [...document.querySelectorAll('.passage .tabgroup-button')]"
        ".map(b => b.querySelector('.tabgroup-button-emoji').textContent + ' '"
        " + b.querySelector('.tabgroup-button-label').textContent)"
    )


def _tab(g, label):
    g.js(
        """(l) => [...document.querySelectorAll('.passage .tabgroup-button')]
            .find(b => b.querySelector('.tabgroup-button-label').textContent.trim() === l).click()""",
        label,
    )
    g.page.wait_for_timeout(100)


def _body(g):
    return g.js("() => document.querySelector('.passage').innerText")


def _link(g, text):
    g.js(
        """(t) => [...document.querySelectorAll('.passage a')]
            .find(a => a.textContent.trim() === t).click()""",
        text,
    )
    g.page.wait_for_timeout(150)


def _search(g, text):
    g.js(
        """(t) => { const i = document.querySelector('.passage .social-search-input input');
            i.value = t; i.dispatchEvent(new Event('input', { bubbles: true })); }""",
        text,
    )
    g.page.wait_for_timeout(400)  # CoT's 250 ms debounce


@needs_browser
def test_the_button_counts_the_people_here(html):
    with open_game(html) as g:
        _at(g, "Location_loc_home", started=True)
        assert _button(g) == "People (19)"
        _at(g, "Location_loc_bar")
        assert _button(g) == "People (1)"
        assert g.errors == []


@needs_browser
def test_people_here_lists_a_stranger_by_stranger_name(html):
    with open_game(html) as g:
        _at(g, "Location_loc_home", started=True)
        _open(g)
        assert (
            g.js("() => document.querySelector('.passage .cot-page-title').textContent.trim()")
            == "People"
        )
        names = _names(g)
        assert names[:2] == ["guy by the window", "Laura"], names
        assert "Zed" not in names
        text = _body(g)
        assert "People nearby:" in text and "Click a person to see more." in text
        # The niche line is the role, and a stranger has none.
        niches = g.js(
            "() => [...document.querySelectorAll('.passage .view-people-person')].slice(0, 2)"
            ".map(p => (p.querySelector('.view-people-person-niche') || {textContent: ''}).textContent.trim())"
        )
        assert niches == ["", "Mom"]
        assert g.errors == []


@needs_browser
def test_a_stranger_is_three_question_marks(html):
    with open_game(html) as g:
        _at(g, "Location_loc_home", started=True)
        _open(g)
        _link(g, "guy by the window")
        assert (
            g.js("() => document.querySelector('.passage .cot-page-title').textContent.trim()")
            == "View Person"
        )
        assert (
            g.js(
                "() => document.querySelector('.npc-display-avatar').textContent.trim()"
            )
            == "??"
        )
        assert (
            g.js(
                "() => document.querySelector('.npc-display-fullname').textContent.trim()"
            )
            == "???"
        )
        text = _body(g)
        assert "A guy by the window." in text
        assert "You're not sure who this is." in text
        assert "Neighbour" not in text and "Zed" not in text
        # Back to the people list.
        g.js("() => document.querySelector('#view-people-backward').click()")
        g.page.wait_for_timeout(150)
        assert (
            g.js("() => document.querySelector('.passage .cot-page-title').textContent.trim()")
            == "People"
        )
        assert g.errors == []


@needs_browser
def test_tabs_in_cots_order_with_cots_empty_lines(html):
    with open_game(html) as g:
        _at(g, "Location_loc_home", started=True)
        _open(g)
        assert _tabs(g) == [
            "📍 People Here",
            "😊 Friends",
            "👋 Acquaintances",
            "🎭 Special",
        ]
        _tab(g, "Friends")
        assert "You have no friends. Ouch!" in _body(g)
        _tab(g, "Special")
        assert _names(g) == ["Laura"]
        assert "People who fill a particular niche in the story of your life:" in _body(
            g
        )
        g.js("() => SugarCube.Dialog.close()")
        _at(g, "Location_loc_home", met_tom=True)
        _open(g)
        _tab(g, "Friends")
        assert _names(g) == ["Tom Baker"]
        assert "Friends:" in _body(g)
        assert g.errors == []


@needs_browser
def test_search_and_sort(html):
    with open_game(html) as g:
        _at(g, "Location_loc_home", started=True)
        _open(g)
        assert "Filter Options" in _body(g)
        g.js(
            "() => document.querySelector('.passage .shop-filter-toolbar-header-minrestore a').click()"
        )
        g.page.wait_for_timeout(100)
        _search(g, "window")
        assert _names(g) == ["guy by the window"]
        _search(g, "zed")  # a stranger matches by the stranger name only
        assert _names(g) == []
        assert (
            "There is no one in this category with your current filters applied."
            in _body(g)
        )
        _link(g, "Clear all filters")
        assert len(_names(g)) == 16

        _link(g, "Sort by name (z -> a)")
        assert _names(g)[0] == "Laura"
        _link(g, "Sort by want (high → low)")
        assert _names(g)[0] == "guy by the window"  # 90
        _link(g, "Sort by want (low → high)")
        assert _names(g)[0] == "Laura"  # 0
        _link(g, "Sort by relevance")
        assert _names(g)[:2] == ["guy by the window", "Laura"]
        assert g.errors == []


@needs_browser
def test_paging_past_sixteen(html):
    with open_game(html) as g:
        _at(g, "Location_loc_home", started=True)
        _open(g)
        assert len(_names(g)) == 16
        assert "Page 1/2" in _body(g)
        assert not g.js("() => !!document.querySelector('#view-people-page-backward')")
        g.js("() => document.querySelector('#view-people-page-forward').click()")
        g.page.wait_for_timeout(100)
        assert _names(g) == ["Extra 15", "Extra 16", "Extra 17"]
        assert "Page 2/2" in _body(g)
        assert not g.js("() => !!document.querySelector('#view-people-page-forward')")
        assert g.errors == []


@needs_browser
def test_a_known_person_and_the_talk_action(html):
    with open_game(html) as g:
        _at(g, "Location_loc_bar", started=True, met_tom=True)
        _open(g)
        _link(g, "Tom Baker")
        assert (
            g.js(
                "() => document.querySelector('.npc-display-avatar').textContent.trim()"
            )
            == "TB"
        )
        text = _body(g)
        assert "Tom Baker" in text and "Bartender · Runs the bar." in text
        assert "Want" in text and "Warmth" in text
        assert "Actions" in text
        assert "He is behind the counter all day." in text  # the card's tip
        _link(g, "💬 Talk to Tom Baker")
        assert not g.js("() => SugarCube.Dialog.isOpen()")
        assert "Tom nods." in g.js("() => document.querySelector('.passage').innerText")
        g.play("Location_loc_bar")
        _open(g)
        _link(g, "Tom Baker")
        assert "💭 Talk to Tom Baker again" in _body(g)
        assert g.errors == []


@needs_browser
def test_no_talk_away_from_them(html):
    with open_game(html) as g:
        _at(g, "Location_loc_home", started=True, met_tom=True)
        _open(g)
        _tab(g, "Friends")
        _link(g, "Tom Baker")
        assert "Talk to" not in _body(g)
        assert g.errors == []


# ── pages, not dialogs (LO 2026-11-26: "They should have their own page. This design can be
# ported into that page. And a schedule modal in the people's page should work like before.") ──


@needs_browser
def test_people_and_view_person_are_pages_with_back_to_the_game(html):
    with open_game(html) as g:
        _at(g, "Location_loc_bar", started=True, met_tom=True)
        _open(g)
        assert g.passage() == "CastPage"
        assert not g.js("() => SugarCube.Dialog.isOpen()")
        _link(g, "Tom Baker")
        assert g.passage() == "PersonPage"
        assert not g.js("() => SugarCube.Dialog.isOpen()")
        # ◀ goes back to the list, on the same tab; ← Back from either page goes to the game.
        g.js("() => document.querySelector('#view-people-backward').click()")
        g.page.wait_for_timeout(150)
        assert g.passage() == "CastPage"
        _link(g, "Tom Baker")
        _link(g, "← Back")
        assert g.passage() == "Location_loc_bar"
        assert g.errors == []


@needs_browser
def test_the_schedule_is_the_old_pop_up(html):
    with open_game(html) as g:
        _at(g, "Location_loc_bar", started=True, met_tom=True)
        _open(g)
        _link(g, "Tom Baker")
        assert "people-accordion" not in g.js("() => document.querySelector('.passage').innerHTML")
        _link(g, "🗓 Schedule")
        assert g.js("() => SugarCube.Dialog.isOpen()")
        title = g.js("() => document.querySelector('#ui-dialog-title').textContent.trim()")
        assert title.endswith("Schedule"), title
        assert g.js("() => !!document.querySelector('#ui-dialog-body .tt-day, #ui-dialog-body [data-day]')")
        assert g.passage() == "PersonPage"
        assert g.errors == []
