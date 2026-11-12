"""trigger.random_cooldown — how long a room rests after a random canvas fires.

After a random canvas fires, `checkRandomEncounters` (v2.py) rests that room: its next
3 arrivals roll nothing. That is right for ambient events and wrong for a chance-1.0
event that must come on her first arrival of a window every day (Vesper 0.2.6's daily
test, 2026-11-12: the last test's return to the cell was eating the next morning's).
A random canvas may now set `random_cooldown = N` (a whole number >= 0); the room rests
N arrivals after THAT canvas fires. Absent, the engine's 3 is unchanged, and the
payload key `randomCooldown` is emitted only where set, so a game that authors none
builds the same canvas index it did before.

    pytest apps/game_generation/tests/test_random_cooldown.py -q
"""
import inspect

import pytest

from apps.game_generation.twee_comprehensive.generators.v2 import (
    TweeComprehensiveGeneratorV2,
)
from apps.projects.services import game_graph, template_import
from apps.projects.services.game_graph import build_game_graph
from apps.projects.services.template_import import normalize, parse_toml, validate

from .headless import build, needs_browser, open_game

FIXTURE = "apps/game_generation/games_toml_files/engine_random_cooldown_2026_11_12.toml"
PLAIN = "apps/game_generation/games_toml_files/engine_prd_phase2_2026_04_29.toml"


def _raw():
    return parse_toml(FIXTURE)


def _canvas(raw, cid):
    return next(c for c in raw["canvases"] if c["id"] == cid)


def _twee(raw=None, path=None):
    graph = build_game_graph(normalize(raw if raw is not None else parse_toml(path or FIXTURE)))
    return TweeComprehensiveGeneratorV2().generate(graph.project, {}, graph=graph)


def _errors(raw):
    return validate(normalize(raw))


# ── 1. the field route ────────────────────────────────────────────────────────


def test_random_cooldown_reaches_the_graph():
    graph = build_game_graph(normalize(_raw()))
    trig = {c.metadata.get("slug"): c.trigger for c in graph.canvases
            if getattr(c, "trigger", None) is not None}
    assert trig["random_rest"].metadata["random_cooldown"] == 0
    assert "random_cooldown" not in trig["random_control"].metadata


def test_both_writers_carry_random_cooldown():
    for mod in (game_graph, template_import):
        assert '"random_cooldown": c.trigger.random_cooldown' in inspect.getsource(mod), mod.__name__


def test_the_payload_carries_random_cooldown_only_where_set():
    twee = _twee()
    assert twee.count('"randomCooldown": 0') == 1


def test_the_engine_reads_it_and_keeps_3_as_the_default():
    twee = _twee()
    assert "cooldowns[locKey] = (typeof canvas.randomCooldown === 'number') ? canvas.randomCooldown : 3;" in twee


# ── 2. the validator ──────────────────────────────────────────────────────────


def test_the_fixture_is_clean():
    assert _errors(_raw()) == []


@pytest.mark.parametrize(
    "mutation, fragment",
    [
        (lambda r: _canvas(r, "plain_card")["trigger"].update(random_cooldown=0),
         'read only with trigger_mode = "random"'),
        (lambda r: _canvas(r, "random_rest")["trigger"].update(random_cooldown=-1),
         "must be a whole number >= 0"),
        (lambda r: _canvas(r, "random_rest")["trigger"].update(random_cooldown="none"),
         "must be a whole number >= 0"),
        (lambda r: _canvas(r, "random_rest")["trigger"].update(random_cooldown=1.5),
         "must be a whole number >= 0"),
        (lambda r: _canvas(r, "random_rest")["trigger"].update(random_cooldown=True),
         "must be a whole number >= 0"),
    ],
)
def test_misuse_is_an_error(mutation, fragment):
    raw = _raw()
    mutation(raw)
    errs = _errors(raw)
    assert any(fragment in e for e in errs), errs


def test_a_positive_rest_is_legal():
    raw = _raw()
    _canvas(raw, "random_rest")["trigger"].update(random_cooldown=5)
    assert _errors(raw) == []


# ── 3. inert without the key ──────────────────────────────────────────────────


def test_a_game_without_the_key_has_no_random_cooldown():
    assert '"randomCooldown"' not in _twee(path=PLAIN)


# ── 4. behaviour, in the real engine ─────────────────────────────────────────


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    return build(FIXTURE, tmp_path_factory.mktemp("rc") / "out")


@needs_browser
def test_random_cooldown_0_fires_on_every_arrival(html):
    with open_game(html) as g:
        for _ in range(4):
            assert g.play("Location_loc_quiet") == "Canvas_random_rest_Node_meet"
        assert g.sv("game_state.random_cooldowns.loc_quiet") == 0
        assert g.errors == []


@needs_browser
def test_without_the_key_the_room_rests_3_arrivals(html):
    with open_game(html) as g:
        assert g.play("Location_loc_busy") == "Canvas_random_control_Node_meet"
        for _ in range(3):
            assert g.play("Location_loc_busy") == "Location_loc_busy"
        assert g.play("Location_loc_busy") == "Canvas_random_control_Node_meet"
        assert g.errors == []
