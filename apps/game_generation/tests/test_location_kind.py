"""EN10 — thoroughfare vs destination.

PRD_SKILL_TEST_FIXES_v2 §2 EN10 (D9a · H20 · CK7). A location can now say what it is:
`kind = "thoroughfare"` (she passes through it) or `"destination"` (she goes there to do
something; the default). The word is "thoroughfare", never "hub" — that already means a
character's hub canvas.

Only the field: parsed, validated, copied by both writers (only when written). Nothing in
the engine reads it — DC7 / CK7 do — so every build is byte-identical with or without it.

Old saves (§0 rule 8): no runtime state and no runtime reader, so nothing about a save
changes; the byte-identical twee below is the proof.

    pytest apps/game_generation/tests/test_location_kind.py -q
"""
import warnings

import pytest

from apps.game_generation.twee_comprehensive.generators.v2 import (
    TweeComprehensiveGeneratorV2,
)
from apps.projects.services.game_graph import build_game_graph
from apps.projects.services.template_import import normalize, parse_toml, validate

FIXTURE = "apps/game_generation/games_toml_files/engine_skill_test_fixes_2026_09_30.toml"


def _raw():
    return parse_toml(FIXTURE)


def _loc(raw, lid):
    return next(l for l in raw["locations"] if l["id"] == lid)


def _validate(raw):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return validate(normalize(raw))


def _props(raw):
    return {l.properties["slug"]: l.properties for l in build_game_graph(normalize(raw)).locations}


def test_the_fixture_is_clean():
    assert _validate(_raw()) == []


def test_the_key_reaches_the_graph_only_when_written():
    props = _props(_raw())
    assert props["loc_bar"]["kind"] == "thoroughfare"
    assert "kind" not in props["loc_home"]                 # absent = a destination
    raw = _raw()
    _loc(raw, "loc_home")["kind"] = "destination"
    assert _props(raw)["loc_home"]["kind"] == "destination"


@pytest.mark.parametrize("value", ["hub", 3, "Thoroughfare", ""])
def test_anything_but_the_two_words_is_an_error(value):
    raw = _raw()
    _loc(raw, "loc_bar")["kind"] = value
    errors = _validate(raw)
    assert any("kind must be \"thoroughfare\" or \"destination\"" in e for e in errors), errors


def test_hub_is_told_what_hub_means():
    raw = _raw()
    _loc(raw, "loc_bar")["kind"] = "hub"
    assert any("names a character's hub canvas, not a place" in e for e in _validate(raw))


def test_the_build_is_identical_with_and_without_it():
    raw = _raw()
    _loc(raw, "loc_bar").pop("kind")
    twees = []
    for r in (_raw(), raw):
        graph = build_game_graph(normalize(r))
        twees.append(TweeComprehensiveGeneratorV2().generate(graph.project, {}, graph=graph))
    assert twees[0] == twees[1]
