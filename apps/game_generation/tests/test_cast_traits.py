"""EN7 — the men's numbers on their page.

PRD_SKILL_TEST_FIXES_v2 §2 EN7 (D1 · D5 · J6). The cast page ([ui.cast_page]) showed a
man's name, relationship, tags, where he is and his next step — never a number.

Opt-in:
  * `[ui.cast_page] show_traits = [...]` — the traits every card shows;
  * `[[npcs]] show_traits = [...]` — added for that man only (a Power only the boss has);
  * `[ui.cast_page] trait_bands = {trait = [{min, max, text}]}` — a word beside the number
    (`setup.traitBand`; min and max may each be left off).

A row is the trait's one name (EN5 `setup.traitLabel`), the number and the word. A trait
marked `hidden` never shows, nor one the man does not have. The Stats page already uses
labels and honours `hidden` since EN5.

A cast page without `show_traits` is emitted exactly as before (golden from the
pre-change engine).

Old saves (§0 rule 8): no new state. A save the pre-change build wrote shows both men's
numbers on the cast page.

    pytest apps/game_generation/tests/test_cast_traits.py -q
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


def _raw():
    return parse_toml(FIXTURE)


def _npc(raw, nid):
    return next(n for n in raw["npcs"] if n["id"] == nid)


def _validate(raw):
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        errors = validate(normalize(raw))
    return errors, [str(w.message) for w in caught]


def _twee(raw):
    graph = build_game_graph(normalize(raw))
    return TweeComprehensiveGeneratorV2().generate(graph.project, {}, graph=graph)


def _passage(twee, name):
    return next("\n:: " + p for p in twee.split("\n:: ") if p.split("\n", 1)[0].split(" ")[0] == name)


def _bare(raw):
    """The fixture with every EN7 key taken out."""
    raw["ui"]["cast_page"].pop("show_traits")
    raw["ui"]["cast_page"].pop("trait_bands")
    _npc(raw, "vic").pop("show_traits")
    return raw


# ── 1. the hops and the validator ────────────────────────────────────────────


def test_the_keys_reach_the_metadata_and_the_npc():
    graph = build_game_graph(normalize(_raw()))
    cp = graph.project.metadata["cast_page"]
    assert cp["show_traits"] == ["trust"]
    assert cp["trait_bands"]["trust"][0] == {"max": 19, "text": "Wary"}
    vic = next(n for n in graph.npcs if n.name == "Vic")
    assert vic.ai_behavior_config["show_traits"] == ["power"]


def test_without_the_keys_nothing_new_is_written():
    graph = build_game_graph(normalize(_bare(_raw())))
    assert "show_traits" not in graph.project.metadata["cast_page"]
    assert "trait_bands" not in graph.project.metadata["cast_page"]
    assert all("show_traits" not in (n.ai_behavior_config or {}) for n in graph.npcs)


def test_the_fixture_is_clean():
    errors, warned = _validate(_raw())
    assert errors == [] and not any("show_traits" in w or "trait_bands" in w for w in warned)


@pytest.mark.parametrize(
    "edit, fragment",
    [
        (lambda r: r["ui"]["cast_page"].update(show_traits="trust"), "show_traits must be a list"),
        (lambda r: r["ui"]["cast_page"].update(show_traits=["charm"]), "no character has a core trait 'charm'"),
        (lambda r: _npc(r, "tobin").update(show_traits=["power"]), "'tobin' has no core trait 'power'"),
        (lambda r: r["ui"]["cast_page"].update(trait_bands=[1]), "trait_bands must be a table"),
        (lambda r: r["ui"]["cast_page"]["trait_bands"].update(trust={"max": 3}), "must be a list of"),
        (lambda r: r["ui"]["cast_page"]["trait_bands"]["trust"].append("x"), "must be a table {min, max, text}"),
        (lambda r: r["ui"]["cast_page"]["trait_bands"]["trust"].append({"min": 1}), "].text is required"),
        (lambda r: r["ui"]["cast_page"]["trait_bands"]["trust"].append({"min": "a", "text": "x"}), ".min must be a number"),
        (lambda r: r["ui"]["cast_page"]["trait_bands"]["trust"].append({"min": 9, "max": 3, "text": "x"}), "min 9 is above max 3"),
        (lambda r: r["ui"]["cast_page"]["trait_bands"]["trust"].append({"at": 3, "text": "x"}), "unknown key(s) ['at']"),
    ],
)
def test_misuse_is_an_error(edit, fragment):
    raw = _raw()
    edit(raw)
    errors, _ = _validate(raw)
    assert any(fragment in e for e in errors), errors


def test_a_band_nothing_shows_is_warned():
    raw = _raw()
    raw["ui"]["cast_page"]["trait_bands"]["power"] = [{"text": "Big"}]
    _npc(raw, "vic").pop("show_traits")
    assert any("trait_bands.power: no show_traits list names 'power'" in w for w in _validate(raw)[1])


def test_a_hidden_trait_in_a_list_is_warned():
    raw = _raw()
    raw["traits"]["labels"].append({"key": "trust", "hidden": True})
    assert any("names 'trust', which [[traits.labels]] marks hidden" in w for w in _validate(raw)[1])


def test_npc_show_traits_without_a_cast_page_is_warned():
    raw = _raw()
    raw["ui"].pop("cast_page")
    assert any("show_traits does nothing: there is no [ui.cast_page]" in w for w in _validate(raw)[1])


# ── 2. emitted only when used ────────────────────────────────────────────────


def test_a_cast_page_without_show_traits_is_emitted_as_before():
    """§0 rule 7. The golden is the CastPage passage the engine BEFORE EN7 (the EN5 tree,
    snapshotted to scratch; it ignores these keys) generated for this fixture."""
    twee = _twee(_bare(_raw()))
    assert _passage(twee, "CastPage").strip() == read_data("en7_castpage_golden.txt")
    for piece in ("castTraitRows", "traitBand", "cast_show_traits", "cast-traits"):
        assert piece not in twee, piece


# ── 3. behaviour, in the real engine ─────────────────────────────────────────


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    return build(FIXTURE, tmp_path_factory.mktemp("en7") / "out")


def _variant(tmp_path_factory, name, edit):
    out = tmp_path_factory.mktemp(name)
    toml = out / "fixture.toml"
    toml.write_text(edit(open(FIXTURE).read()))
    return build(toml, out / "out")


@pytest.fixture(scope="module")
def trust_hidden_html(tmp_path_factory):
    add = '\n[[traits.labels]]\nkey    = "trust"\nhidden = true\n'
    anchor = '[[traits.labels]]\nkey     = "stamina"\nin_dump = false\n'
    return _variant(tmp_path_factory, "en7_hidden", lambda t: t.replace(anchor, anchor + add, 1))


@pytest.fixture(scope="module")
def trust_labelled_html(tmp_path_factory):
    add = '\n[[traits.labels]]\nkey   = "trust"\nlabel = "Faith"\n'
    anchor = '[[traits.labels]]\nkey     = "stamina"\nin_dump = false\n'
    return _variant(tmp_path_factory, "en7_label", lambda t: t.replace(anchor, anchor + add, 1))


def _cards(g):
    g.js("() => { SugarCube.State.variables.flags.started = true; }")
    g.play("CastPage")
    return g.js("""() => Object.fromEntries([...document.querySelectorAll('.cast-card')].map(c =>
        [c.querySelector('.stats-name').innerText.trim(),
         [...c.querySelectorAll('.cast-trait')].map(t => t.innerText.replace(/\\s+/g, ' ').trim())]))""")


@needs_browser
def test_two_men_one_with_an_extra_power_trait(html):
    with open_game(html) as g:
        cards = _cards(g)
        assert cards["Tobin"] == ["Trust 10 · Wary"]
        assert cards["Vic"] == ["Trust 70 · Yours", "Power 30"]
        assert g.errors == []


@needs_browser
def test_the_band_moves_with_the_number(html):
    with open_game(html) as g:
        g.js("() => { SugarCube.State.variables.npcs.tobin.core_traits.trust = 35; }")
        assert _cards(g)["Tobin"] == ["Trust 35 · Warming"]


@needs_browser
def test_a_hidden_trait_never_shows(trust_hidden_html):
    with open_game(trust_hidden_html) as g:
        cards = _cards(g)
        assert cards["Tobin"] == [] and cards["Vic"] == ["Power 30"]
        g.play("StatsPage")
        assert "Trust" not in g.js("() => document.querySelector('.passage').innerText")
        assert g.errors == []


@needs_browser
def test_the_name_is_the_label(trust_labelled_html):
    with open_game(trust_labelled_html) as g:
        assert _cards(g)["Vic"] == ["Faith 70 · Yours", "Power 30"]
        g.play("StatsPage")
        assert "Faith" in g.js("() => document.querySelector('.passage').innerText")


@needs_browser
def test_trait_band_edges(html):
    with open_game(html) as g:
        band = "([k, v]) => SugarCube.setup.traitBand(k, v)"
        assert g.js(band, ["trust", -5]) == "Wary"     # max only
        assert g.js(band, ["trust", 19]) == "Wary"
        assert g.js(band, ["trust", 20]) == "Warming"
        assert g.js(band, ["trust", 999]) == "Yours"   # min only
        assert g.js(band, ["power", 30]) == ""         # no bands for power


@needs_browser
def test_a_save_made_before_en7(html):
    """§0 rule 8. Written by the PRE-change engine (the EN5 tree, snapshotted to scratch;
    it ignores show_traits/trait_bands): the fixture built with it, `started` set,
    Engine.play Location_loc_home (step_plain fires there), Save.serialize()."""
    with open_game(html) as g:
        assert g.load_save(read_data("en7_pre_change_save.txt")) is True
        assert g.passage() == "Canvas_step_plain_Node_only"
        g.play("CastPage")
        cards = g.js("() => [...document.querySelectorAll('.cast-trait')].map(t => t.innerText.replace(/\\s+/g, ' ').trim())")
        assert cards == ["Trust 10 · Wary", "Trust 70 · Yours", "Power 30"]
        assert g.errors == []
