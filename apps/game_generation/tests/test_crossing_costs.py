"""EN11 — crossing costs (checked first, then built).

PRD_SKILL_TEST_FIXES_v2 §2 EN11 (D10a). The check: a parent container's `costs` alone
cannot mean "charged only when crossing areas". The only charge is the travel intercept,
which charges the DESTINATION's own entry_costs on any move to a different place and
never looks at areas: a link from outside straight to an inner room skips the
container, and walking back to a container page from its own room charges it again.
LO chose the PRD's fallback (2026-09-30).

`[[locations]] crossing_costs = {time, <trait>…}` on an area (a container): charged
once when she moves to a place inside the area from a place outside it — the container
page or any inner room, however deep. Moves inside the area pay only each room's own
costs; leaving is free. A container with a `default_entry` only redirects, so the toll is
charged on the room it lands on, once. No previous place (game start) = no toll. Entry
cost and tolls are checked together; unaffordable = TravelBlock, nothing charged.

Games without crossing_costs keep their intercept byte-identical (members_only and
the_balance both use room costs; see the CHANGELOG entry's passage diff).

Old saves (§0 rule 8): no new state — the toll reads `current_location`, which every
save has.

    pytest apps/game_generation/tests/test_crossing_costs.py -q
"""
import warnings

import pytest

from apps.game_generation.twee_comprehensive.generators.v2 import (
    TweeComprehensiveGeneratorV2,
)
from apps.projects.services.game_graph import build_game_graph
from apps.projects.services.template_import import normalize, parse_toml, validate

from .headless import build, needs_browser, open_game, read_data

FIXTURE = "apps/game_generation/games_toml_files/engine_skill_test_fixes_2026_09_30.toml"
TOLL = "crossing_costs = { time = 20 }\n"


def _raw():
    return parse_toml(FIXTURE)


def _loc(raw, lid):
    return next(l for l in raw["locations"] if l["id"] == lid)


def _validate(raw):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return validate(normalize(raw))


def _twee(raw):
    graph = build_game_graph(normalize(raw))
    return TweeComprehensiveGeneratorV2().generate(graph.project, {}, graph=graph)


# ── 1. the hops and the validator ────────────────────────────────────────────


def test_the_key_reaches_the_graph():
    props = {l.properties["slug"]: l.properties for l in build_game_graph(normalize(_raw())).locations}
    assert props["loc_mall"]["crossing_costs"] == {"time": 20}
    assert "crossing_costs" not in props["loc_mall_food"]


def test_the_fixture_is_clean():
    assert _validate(_raw()) == []


@pytest.mark.parametrize(
    "edit, fragment",
    [
        (lambda r: _loc(r, "loc_mall").update(crossing_costs=5), "crossing_costs must be a dict"),
        (lambda r: _loc(r, "loc_mall").update(crossing_costs={"time": "long"}), "crossing_costs['time'] must be a number"),
        (lambda r: _loc(r, "loc_mall").update(crossing_costs={"energy": -5}), "must not be negative"),
        (lambda r: _loc(r, "loc_bar").update(crossing_costs={"time": 5}), "crossing_costs needs is_container = true"),
    ],
)
def test_misuse_is_an_error(edit, fragment):
    raw = _raw()
    edit(raw)
    assert any(fragment in e for e in _validate(raw)), _validate(raw)


def test_without_crossing_costs_none_of_it_is_emitted():
    raw = _raw()
    _loc(raw, "loc_mall").pop("crossing_costs")
    twee = _twee(raw)
    for piece in ("crossingCostsFor", "setup.loc_parent", "loc_redirect", ":: TravelBlock"):
        assert piece not in twee, piece


# ── 2. behaviour, in the real engine ─────────────────────────────────────────


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    return build(FIXTURE, tmp_path_factory.mktemp("en11") / "out")


def _variant(tmp_path_factory, name, old, new):
    text = open(FIXTURE).read()
    assert text.count(old) == 1, old
    out = tmp_path_factory.mktemp(name)
    toml = out / "fixture.toml"
    toml.write_text(text.replace(old, new))
    return build(toml, out / "out")


def _clock(g):
    return g.js("""() => { const t = SugarCube.State.variables.game_state.time_state;
        return t.day * 1440 + t.current_hour * 60 + t.current_minute; }""")


def _trip(g, dest, settle=300):
    before = _clock(g)
    g.play(f"Location_{dest}", settle=settle)
    return _clock(g) - before


def _stand_at(g, lid):
    g.js("(l) => { SugarCube.State.variables.player.current_location = l; }", lid)


@needs_browser
def test_in_across_and_back(html):
    with open_game(html) as g:
        _stand_at(g, "loc_bar")
        assert _trip(g, "loc_mall") == 20                 # crossing into the area
        assert _trip(g, "loc_mall_food") == 0             # inside
        assert _trip(g, "loc_mall_shop") == 0             # inside, direct
        assert _trip(g, "loc_mall") == 0                  # back to the container page
        assert _trip(g, "loc_bar") == 0                   # leaving is free
        assert _trip(g, "loc_mall_food") == 20            # a direct link into an inner room
        assert g.passage() == "Location_loc_mall_food"
        assert g.errors == []


@needs_browser
def test_no_previous_place_no_toll(html):
    with open_game(html) as g:
        _stand_at(g, "")
        assert _trip(g, "loc_mall_food") == 0


@needs_browser
def test_a_redirecting_container_charges_once(tmp_path_factory):
    # A default_entry container's rooms may not name it in entry_from (an existing rule).
    text = open(FIXTURE).read().replace(TOLL, TOLL + 'default_entry  = "loc_mall_food"\n', 1)
    assert text.count('entry_from  = "loc_mall"\n') == 2
    text = text.replace('entry_from  = "loc_mall"\n', "")
    out = tmp_path_factory.mktemp("en11_default")
    (out / "fixture.toml").write_text(text)
    html = build(out / "fixture.toml", out / "out")
    with open_game(html) as g:
        _stand_at(g, "loc_bar")
        assert _trip(g, "loc_mall", settle=500) == 20
        assert g.passage() == "Location_loc_mall_food"
        assert g.errors == []


@needs_browser
def test_an_unaffordable_toll_blocks_and_charges_nothing(tmp_path_factory):
    html = _variant(tmp_path_factory, "en11_energy", TOLL, "crossing_costs = { time = 20, energy = 500 }\n")
    with open_game(html) as g:
        _stand_at(g, "loc_bar")
        energy = g.sv("player.core_traits.energy")
        assert _trip(g, "loc_mall") == 0
        assert g.passage() == "TravelBlock"
        assert g.sv("player.core_traits.energy") == energy
        assert "Requires 500 Energy" in g.js("() => document.querySelector('.passage').innerText")
        assert g.errors == []


@needs_browser
def test_a_save_made_before_en11(html):
    """§0 rule 8. Written by the PRE-change engine (the EN10 tree, snapshotted to scratch;
    it ignores crossing_costs): the fixture built with it, Engine.play Location_loc_bar
    (step_offer fires there), Save.serialize(). Its current_location is loc_bar."""
    with open_game(html) as g:
        assert g.load_save(read_data("en11_pre_change_save.txt")) is True
        assert g.sv("player.current_location") == "loc_bar"
        assert _trip(g, "loc_mall") == 20
        assert g.errors == []
