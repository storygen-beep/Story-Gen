"""EN4 — places hidden until found.

PRD_SKILL_TEST_FIXES_v2 §2 EN4 (D10b). Every place was listed from the start (a locked
one greyed, with its reason). Opt-in by `[[locations]] hidden_until = {flag = "..."}`:

  * while that player flag is false the place is not listed — the travel card, the text
    link, a container's child list and the Navigation page. A `door` place is hidden like
    any other (the wrap sits outside the door branch);
  * its name is withheld wherever the game prints where someone is — the Schedules page,
    guidance 📍, the cast page 📍, the quests page 📍, npc_panel — as "somewhere you
    haven't found yet";
  * when every place on a room's list can be hidden, the list's header hides with them
    (LO, 2026-09-30: the header only; the room keeps whatever exits it has).

There is no passage guard: a scene can still take her there — that is the finding.

Old saves (§0 rule 8): no new state; the flag is an ordinary player flag. A save the
pre-change build wrote shows the place hidden, then found once the flag is set.

    pytest apps/game_generation/tests/test_hidden_places.py -q
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
HIDDEN = "somewhere you haven't found yet"
DOOR = {"description": "A low door.", "options": [{"text": "Go in.", "goes_to": {"type": "enter"}}]}


def _raw():
    return parse_toml(FIXTURE)


def _loc(raw, lid):
    return next(l for l in raw["locations"] if l["id"] == lid)


def _validate(raw):
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        errors = validate(normalize(raw))
    return errors, [str(w.message) for w in caught]


def _gen(raw=None):
    graph = build_game_graph(normalize(raw or _raw()))
    gen = TweeComprehensiveGeneratorV2()
    twee = gen.generate(graph.project, {}, graph=graph)
    return gen, twee


def _passages(twee):
    return {p.split("\n", 1)[0].split(" ")[0]: "\n:: " + p for p in twee.split("\n:: ")}


def _all_hidden(raw):
    """Every place home lists is hidden until found."""
    for lid in ("loc_bar", "loc_shop", "loc_club"):
        _loc(raw, lid)["hidden_until"] = {"flag": "found_attic"}
    return raw


# ── 1. the hops ──────────────────────────────────────────────────────────────


def test_the_key_reaches_the_template_and_the_graph():
    t = normalize(_raw())
    attic = next(l for l in t.locations if l.id == "loc_attic")
    assert attic.hidden_until == {"flag": "found_attic"}
    graph = build_game_graph(t)
    props = {l.properties["slug"]: l.properties for l in graph.locations}
    assert props["loc_attic"]["hidden_until"] == {"flag": "found_attic"}
    assert "hidden_until" not in props["loc_bar"]


def test_the_fixture_is_clean():
    errors, warned = _validate(_raw())
    assert errors == [] and not any("hidden_until" in w for w in warned), (errors, warned)


# ── 2. the validator ─────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "value, fragment",
    [
        ("found_attic", "must be a table {flag"),
        ({}, None),  # empty = not hidden; nothing to report
        ({"flag": "found_attic", "when": 1}, "has unknown key(s) ['when']"),
        ({"flag": ""}, ".flag is required"),
        ({"flag": "found_cellar"}, "'found_cellar' is not a declared player flag"),
    ],
)
def test_misuse_is_an_error(value, fragment):
    raw = _raw()
    _loc(raw, "loc_attic")["hidden_until"] = value
    errors, _ = _validate(raw)
    if fragment is None:
        assert errors == [], errors
    else:
        assert any(fragment in e for e in errors), errors


def test_hidden_until_on_an_offscreen_place_is_an_error():
    raw = _raw()
    _loc(raw, "loc_attic")["offscreen"] = True
    errors, _ = _validate(raw)
    assert any("an offscreen location is never listed" in e for e in errors), errors


def test_a_room_left_with_no_way_out_is_warned():
    """Home has no entry_from (no Leave exit); once every place it lists can be hidden,
    it can end up with nothing on it."""
    errors, warned = _validate(_all_hidden(_raw()))
    assert errors == []
    assert any("location 'loc_home' has no Leave exit" in w for w in warned), warned


# ── 3. emitted only when used ────────────────────────────────────────────────


def test_a_place_without_the_key_is_built_as_before():
    """§0 rule 7. The golden (written by the engine before EN3, which EN4's pre-change
    tree matches for this place) is Location_loc_bar and its link line on home."""
    room, link = read_data("en3_nohours_golden.txt").split("\n=====\n")
    ps = _passages(_gen()[1])
    assert ps["Location_loc_bar"].strip() == room
    assert link in ps["Location_loc_home"]


def test_a_game_without_hidden_places_emits_none_of_it():
    raw = _raw()
    _loc(raw, "loc_attic").pop("hidden_until")
    twee = _gen(raw)[1]
    for piece in ("locFound", "locShownName", "LOC_HIDDEN_NAME", '"hidden_until"'):
        assert piece not in twee, piece


def test_the_card_wrap_sits_outside_the_door_branch():
    raw = _raw()
    _loc(raw, "loc_attic")["door"] = DOOR
    gen, _ = _gen(raw)
    attic = next(l for l in gen.locations if l.properties["slug"] == "loc_attic")
    card = gen._render_location_nav_card(attic, "./media")
    assert card.startswith('<<if setup.locFound("loc_attic")>><a class="location-card')
    assert card.endswith("<</if>>")
    assert 'data-passage="Door_' in card


def test_the_header_hides_only_when_every_place_can_be_hidden():
    home = _passages(_gen()[1])["Location_loc_home"]
    assert "    <strong>Available destinations:</strong><br>\n" in home
    home = _passages(_gen(_all_hidden(_raw()))[1])["Location_loc_home"]
    assert ('<<if setup.locFound("loc_bar") || setup.locFound("loc_shop") || '
            'setup.locFound("loc_club") || setup.locFound("loc_attic")>>'
            '<strong>Available destinations:</strong><br><</if>>') in home


# ── 4. behaviour, in the real engine ─────────────────────────────────────────


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    return build(FIXTURE, tmp_path_factory.mktemp("en4") / "out")


def _variant(tmp_path_factory, name, edit):
    out = tmp_path_factory.mktemp(name)
    text = edit(open(FIXTURE).read())
    toml = out / "fixture.toml"
    toml.write_text(text)
    return build(toml, out / "out")


@pytest.fixture(scope="module")
def door_html(tmp_path_factory):
    anchor = 'hidden_until = { flag = "found_attic" }\n'
    door = ('\n[locations.door]\ndescription = "A low door."\n'
            '[[locations.door.options]]\ntext = "Go in."\ngoes_to = { type = "enter" }\n')
    return _variant(tmp_path_factory, "en4_door", lambda t: t.replace(anchor, anchor + door, 1))


@pytest.fixture(scope="module")
def all_hidden_html(tmp_path_factory):
    def edit(text):
        for lid in ("loc_bar", "loc_shop", "loc_club"):
            anchor = f'id          = "{lid}"\n'
            assert text.count(anchor) == 1, lid
            text = text.replace(anchor, anchor + 'hidden_until = { flag = "found_attic" }\n')
        return text
    return _variant(tmp_path_factory, "en4_all", edit)


def _text(g):
    return g.js("() => document.querySelector('.passage').innerText")


def _links(g):
    return g.js("() => [...document.querySelectorAll('.passage a')].map(a => a.textContent.trim())")


def _find(g):
    g.js("() => { SugarCube.State.variables.flags.found_attic = true; }")


@needs_browser
def test_the_attic_is_not_listed_until_found(html):
    with open_game(html) as g:
        g.play("Location_loc_home")
        assert "Attic" not in _links(g) and "Attic" not in _text(g)
        assert "Bar" in _links(g)
        _find(g)
        g.play("Location_loc_home")
        assert "Attic" in _links(g)
        g.click("Attic")
        assert g.passage() == "Location_loc_attic"
        assert g.errors == []


@needs_browser
def test_the_name_is_withheld_until_found(html):
    """Every "where" printer goes through _locNameFromUuid (guidance, cast, quests,
    npc_panel) or reads locShownName (the Schedules page)."""
    with open_game(html) as g:
        name = "() => SugarCube.setup._locNameFromUuid('loc_attic')"
        assert g.js(name) == HIDDEN
        assert g.js("() => SugarCube.setup._locNameFromUuid('loc_bar')") == "Bar"
        g.play("SchedulePage")
        assert HIDDEN in _text(g) and "Attic" not in _text(g)
        _find(g)
        assert g.js(name) == "Attic"
        g.play("SchedulePage")
        assert "Attic" in _text(g) and HIDDEN not in _text(g)
        assert g.errors == []


CAST_WHERE = '<<set _locName to _loc ? (setup._locNameFromUuid(_loc.location) || "") : "">>'
PANEL_WHERE = ("<<set _npLocName to _npLoc ? (setup._locNameFromUuid(_npLoc.location) || "
               "_npLoc.location) : (_item.away_label || \"Away\")>>")


def test_the_cast_page_and_npc_panel_ask_locNameFromUuid():
    """The fixture has no [ui.cast_page] (it lists only characters with quest cards), so
    the headless test below evaluates the exact expressions those surfaces print."""
    src = open("apps/game_generation/twee_comprehensive/generators/v2.py").read()
    assert CAST_WHERE in src and PANEL_WHERE in src


@needs_browser
def test_where_tobin_is_reads_hidden_until_found(html):
    """Tobin is in the attic on Sunday 10:00-12:00. The cast page and npc_panel pass what
    getNpcLocation returns to _locNameFromUuid."""
    with open_game(html) as g:
        g.js("""() => { const t = SugarCube.State.variables.game_state.time_state;
            t.current_day = 'Sunday'; t.current_hour = 11; t.current_minute = 0; }""")
        loc = g.js("() => SugarCube.setup.getNpcLocation('tobin')")
        assert loc and loc["location"] == "loc_attic"
        where = ("() => { const l = SugarCube.setup.getNpcLocation('tobin');"
                 " return [SugarCube.setup._locNameFromUuid(l.location) || '',"
                 " SugarCube.setup._locNameFromUuid(l.location) || l.location]; }")
        assert g.js(where) == [HIDDEN, HIDDEN]
        _find(g)
        assert g.js(where) == ["Attic", "Attic"]
        assert g.errors == []


@needs_browser
def test_a_door_place_is_hidden_like_any_other(door_html):
    with open_game(door_html) as g:
        g.play("Location_loc_home")
        assert "Attic" not in _links(g)
        _find(g)
        g.play("Location_loc_home")
        g.click("Attic")
        assert g.passage().startswith("Door_")
        assert g.errors == []


@needs_browser
def test_the_header_goes_when_every_place_is_hidden(all_hidden_html):
    with open_game(all_hidden_html) as g:
        g.play("Location_loc_home")
        text = _text(g)
        assert "Available destinations" not in text
        assert not any(n in _links(g) for n in ("Bar", "Shop", "Club", "Attic"))
        _find(g)
        g.play("Location_loc_home")
        assert "Available destinations" in _text(g)
        assert g.errors == []


@needs_browser
def test_a_save_made_before_en4(html):
    """§0 rule 8. Written by the PRE-change engine (the EN3 tree, snapshotted to scratch;
    it ignores hidden_until): the fixture built with it, Engine.play Location_loc_home,
    Save.serialize(). Its flags carry found_attic = false (declared in the fixture)."""
    with open_game(html) as g:
        assert g.load_save(read_data("en4_pre_change_save.txt")) is True
        assert g.passage() == "Location_loc_home"
        assert g.sv("flags.found_attic") is False
        assert "Attic" not in _links(g)
        _find(g)
        g.play("Location_loc_home")
        assert "Attic" in _links(g)
        assert g.errors == []
