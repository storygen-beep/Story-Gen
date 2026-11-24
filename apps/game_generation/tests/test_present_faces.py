"""`[ui] present_faces`: everyone present at a place shows a face, even with nothing to do.

Off by default, a face is drawn only where a repeatable canvas offers something with that person
(setup.renderNpcPortraits). With `present_faces = true`, a person whose schedule row puts them at
this place now also shows a face; a click opens NpcBusyPage, which says what their row says they're
doing ("Ryan is asleep."), or that they're busy. Only people she has met are shown, by the same
rule as the Schedules page and CastPage (a person with quest cards shows while one card's `when`
holds).

The failure (2026-11-24): in first_term_lean, from 11pm Ryan is asleep in his room; his menu shuts
for the night and his face vanished, with nothing on screen to say why.

    pytest apps/game_generation/tests/test_present_faces.py -q
"""
import os

import pytest

from .headless import build, needs_browser, open_game

GAME = "games/first_term_lean/toml_phases/7_final_game.toml"
ROOM = "Location_home_ryans_room"


def _variant(tmp_path_factory, name, on):
    out = tmp_path_factory.mktemp(name)
    text = open(GAME, encoding="utf-8").read()
    # The game turned the key on itself (P44); each variant sets it from scratch.
    text = "".join(
        line for line in text.splitlines(keepends=True) if not line.startswith("present_faces =")
    )
    if on:
        assert "\n[ui]\n" in text
        text = text.replace("\n[ui]\n", "\n[ui]\npresent_faces = true\n", 1)
    toml = out / "game.toml"
    toml.write_text(text, encoding="utf-8")
    return build(toml, out / "out")


@pytest.fixture(scope="module")
def on_html(tmp_path_factory):
    if not os.path.exists(GAME):
        pytest.skip("first_term_lean not present")
    return _variant(tmp_path_factory, "faces_on", True)


@pytest.fixture(scope="module")
def off_html(tmp_path_factory):
    if not os.path.exists(GAME):
        pytest.skip("first_term_lean not present")
    return _variant(tmp_path_factory, "faces_off", False)


def _night_in_ryans_room(g, met=True):
    g.js(
        """(met) => { const v = SugarCube.State.variables, t = v.game_state.time_state;
            t.current_day = 'Saturday'; t.current_hour = 1; t.current_minute = 30;
            v.flags.met_ryan = met; }""",
        met,
    )
    g.play(ROOM)


def _names(g):
    return g.js(
        "() => [...document.querySelectorAll('.passage .npc-portrait-name')].map(e => e.textContent.trim())"
    )


@needs_browser
def test_off_by_default_no_idle_face(off_html):
    with open_game(off_html) as g:
        _night_in_ryans_room(g)
        assert "Ryan" not in _names(g)
        assert g.errors == []


@needs_browser
def test_on_shows_the_sleeping_face_and_says_so(on_html):
    with open_game(on_html) as g:
        _night_in_ryans_room(g)
        assert "Ryan" in _names(g)
        g.js(
            """() => [...document.querySelectorAll('.passage .npc-portrait-card')]
                .find(c => c.textContent.includes('Ryan')).querySelector('a').click()"""
        )
        g.page.wait_for_timeout(200)
        assert g.passage() == "NpcBusyPage"
        text = g.js("() => document.querySelector('.passage').innerText")
        assert "Ryan is asleep." in text, text
        assert g.errors == []


@needs_browser
def test_on_hides_someone_she_has_not_met(on_html):
    with open_game(on_html) as g:
        _night_in_ryans_room(g, met=False)
        assert "Ryan" not in _names(g)
        assert g.errors == []


# ── the room cards on a menu (LO 2026-11-24: "If there is no npc portrait present it can show
# the name circle in that exact same place") ─────────────────────────────────────────────────

HALL = "Location_home_hall"


def _night_in_the_hall(g, met=True):
    g.js(
        """(met) => { const v = SugarCube.State.variables, t = v.game_state.time_state;
            t.current_day = 'Saturday'; t.current_hour = 1; t.current_minute = 30;
            v.flags.met_ryan = met; }""",
        met,
    )
    g.play(HALL)


def _card_initials(g):
    return g.js(
        """() => [...document.querySelectorAll('.passage .location-card')]
            .filter(c => c.querySelector('.nav-npc-initial'))
            .map(c => [c.querySelector('.location-card-name').textContent.trim(),
                       [...c.querySelectorAll('.nav-npc-initial')].map(e => e.textContent.trim() + ':' + e.title)])"""
    )


@needs_browser
def test_on_a_card_shows_the_letter_circle_without_a_portrait(on_html):
    with open_game(on_html) as g:
        _night_in_the_hall(g)
        cards = dict(_card_initials(g))
        assert any("Ryan" in name for name in cards), cards
        ryans = next(v for k, v in cards.items() if "Ryan" in k)
        assert ryans == ["R:Ryan"], ryans
        assert g.errors == []


@needs_browser
def test_on_a_card_hides_someone_she_has_not_met(on_html):
    with open_game(on_html) as g:
        _night_in_the_hall(g, met=False)
        assert not any("Ryan" in name for name, _ in _card_initials(g))
        assert g.errors == []


@needs_browser
def test_off_a_card_draws_no_letter_circle(off_html):
    with open_game(off_html) as g:
        _night_in_the_hall(g)
        assert g.js("() => document.querySelectorAll('.passage .nav-npc-initial').length") == 0
        assert g.errors == []
