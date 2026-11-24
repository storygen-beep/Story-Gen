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
