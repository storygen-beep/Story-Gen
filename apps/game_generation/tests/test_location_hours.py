"""EN3 — location opening hours.

PRD_SKILL_TEST_FIXES_v2 §2 EN3 (D9b · I2). A place was always open, or locked by
`entry_conditions`; nothing could say "the shop opens 09:00-17:00 on weekdays".

Opt-in by `[[locations]] hours = [{weekdays, open, close}]` (+ `closed_text`):

  * a window is open on each listed weekday (0 = Monday; empty = every day) from `open`
    to `close`; a `close` that is not after `open` runs past midnight into the next day;
  * the room's passage is guarded (even with no entry_conditions): closed, it shows
    `closed_text` and "Closed. Opens … at …" with a way back, and she does not enter;
  * the travel card and the text link grey out with the same line
    (`setup.navDestOpenNow`); the Schedules page keeps `navDestUnlocked`;
  * she is NOT moved out when a place closes around her.

A place without `hours` builds exactly as before (golden from the pre-change engine).

Old saves (§0 rule 8): no new state — hours are static data read against the clock. A
save parked in the shop, written by the pre-change build, renders the closed screen when
loaded after hours.

    pytest apps/game_generation/tests/test_location_hours.py -q
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
CLOSED_TEXT = "The shutter's down. A paper sign: back at nine."


def _raw():
    return parse_toml(FIXTURE)


def _loc(raw, lid):
    return next(l for l in raw["locations"] if l["id"] == lid)


def _validate(raw):
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        errors = validate(normalize(raw))
    return errors, [str(w.message) for w in caught]


def _graph(raw):
    return build_game_graph(normalize(raw))


def _twee(raw=None):
    graph = _graph(raw or _raw())
    return TweeComprehensiveGeneratorV2().generate(graph.project, {}, graph=graph)


def _passages(twee):
    return {p.split("\n", 1)[0].split(" ")[0]: "\n:: " + p for p in twee.split("\n:: ")}


# ── 1. the hops ──────────────────────────────────────────────────────────────


def test_the_keys_reach_the_template_and_the_graph():
    t = normalize(_raw())
    shop = next(l for l in t.locations if l.id == "loc_shop")
    assert shop.hours == [{"weekdays": [0, 1, 2, 3, 4], "open": "09:00", "close": "17:00"}]
    assert shop.closed_text == CLOSED_TEXT
    props = {l.properties["slug"]: l.properties for l in _graph(_raw()).locations}
    assert props["loc_shop"]["hours"] == shop.hours
    assert props["loc_shop"]["closed_text"] == CLOSED_TEXT
    assert "hours" not in props["loc_bar"] and "closed_text" not in props["loc_bar"]


def test_the_fixture_is_clean():
    errors, warned = _validate(_raw())
    assert errors == [] and not any("closed" in w for w in warned), (errors, warned)


# ── 2. the validator ─────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "mutation, fragment",
    [
        (lambda l: l.update(hours={"open": "09:00"}), "hours must be a list"),
        (lambda l: l.update(hours=["09:00-17:00"]), "hours[0] must be a table"),
        (lambda l: l.update(hours=[{"open": "09:00", "close": "17:00", "days": [1]}]),
         "has unknown key(s) ['days']"),
        (lambda l: l.update(hours=[{"weekdays": [7], "open": "09:00", "close": "17:00"}]),
         "weekdays must be integers 0..6"),
        (lambda l: l.update(hours=[{"open": "9am", "close": "17:00"}]), "open must be \"HH:MM\""),
        (lambda l: l.update(hours=[{"open": "09:00", "close": "25:00"}]), "close must be \"HH:MM\""),
        (lambda l: l.update(hours=[{"open": "24:00", "close": "02:00"}]), "open must be \"HH:MM\""),
        (lambda l: l.update(hours=[{"open": "09:00", "close": "09:00"}]), "the window is empty"),
        (lambda l: l.pop("hours"), "closed_text is set but hours is not"),
        (lambda l: l.update(is_container=True), "hours on a container location does nothing"),
        (lambda l: l.update(offscreen=True), "hours on an offscreen location does nothing"),
    ],
)
def test_misuse_is_an_error(mutation, fragment):
    raw = _raw()
    mutation(_loc(raw, "loc_shop"))
    errors, _ = _validate(raw)
    assert any(fragment in e for e in errors), errors


def test_close_at_midnight_is_allowed():
    raw = _raw()
    _loc(raw, "loc_shop")["hours"] = [{"open": "18:00", "close": "24:00"}]
    assert _validate(raw)[0] == []


def _with_npc_row(raw, row):
    raw["npcs"][0]["schedules"] = [{"location": "loc_shop", **row}]
    return raw


def test_an_npc_row_only_inside_closed_hours_is_warned():
    raw = _with_npc_row(_raw(), {"weekdays": [0], "start_time": "18:00", "end_time": "20:00"})
    errors, warned = _validate(raw)
    assert errors == []
    assert any("'tobin'.schedules[0] puts it at 'loc_shop' only while" in w for w in warned)


def test_an_npc_row_on_a_closed_day_is_warned():
    raw = _with_npc_row(_raw(), {"weekdays": [5, 6], "start_time": "10:00", "end_time": "12:00"})
    assert any("only while 'loc_shop' is closed" in w for w in _validate(raw)[1])


def test_an_npc_row_that_overlaps_by_one_minute_is_not_warned():
    raw = _with_npc_row(_raw(), {"weekdays": [0], "start_time": "16:59", "end_time": "20:00"})
    assert not any("is closed" in w for w in _validate(raw)[1])


def test_a_canvas_schedule_only_inside_closed_hours_is_warned():
    raw = _raw()
    canvas = next(c for c in raw["canvases"] if c["id"] == "step_plain")
    canvas["trigger"]["location"] = "loc_shop"
    canvas["trigger"]["schedules"] = [{"weekdays": [0, 1], "start_time": "06:00",
                                       "end_time": "08:00"}]
    assert any("'step_plain'.trigger.schedules[0] puts it at 'loc_shop' only while" in w
               for w in _validate(raw)[1])


def test_the_club_is_read_across_midnight():
    """A Saturday 01:00-03:00 row at the Friday 22:00-04:00 club overlaps (not warned);
    a Friday 01:00-03:00 row does not (Friday's early hours belong to Thursday's night)."""
    raw = _raw()
    raw["npcs"][0]["schedules"] = [
        {"location": "loc_club", "weekdays": [5], "start_time": "01:00", "end_time": "03:00"},
        {"location": "loc_club", "weekdays": [4], "start_time": "01:00", "end_time": "03:00"},
    ]
    warned = [w for w in _validate(raw)[1] if "is closed" in w]
    assert len(warned) == 1 and "schedules[1]" in warned[0], warned


# ── 3. emitted only when used ────────────────────────────────────────────────


def test_a_place_without_hours_is_built_as_before():
    """§0 rule 7. The golden is the pre-change engine's Location_loc_bar and the loc_bar
    link in Location_loc_home, for this fixture (the EN2c tree, snapshotted to scratch)."""
    room, link = read_data("en3_nohours_golden.txt").split("\n=====\n")
    ps = _passages(_twee())
    assert ps["Location_loc_bar"].strip() == room
    assert link in ps["Location_loc_home"]


def test_a_game_without_hours_emits_none_of_it():
    raw = _raw()
    for l in raw["locations"]:
        l.pop("hours", None), l.pop("closed_text", None)
    twee = _twee(raw)
    for piece in ("locOpenNow", "navDestOpenNow", "locClosedReason", '"hours"'):
        assert piece not in twee, piece


def test_the_schedules_page_keeps_navDestUnlocked():
    ps = _passages(_twee())
    sched = next(v for k, v in ps.items() if k.startswith("SchedulePage"))
    assert "navDestUnlocked" in sched and "navDestOpenNow" not in sched


def test_the_travel_card_greys_when_closed():
    graph = _graph(_raw())
    gen = TweeComprehensiveGeneratorV2()
    gen.generate(graph.project, {}, graph=graph)
    shop = next(l for l in gen.locations if l.properties["slug"] == "loc_shop")
    card = gen._render_location_nav_card(shop, "./media")
    assert card.startswith('<<if !setup.navDestOpenNow("loc_shop")>><div class="location-card '
                           'location-card-locked location-card-closed">')
    assert '<<= setup.locClosedReason("loc_shop")>>' in card
    assert '<<elseif setup.navDestUnlocked("loc_shop")>><a class="location-card' in card


# ── 4. behaviour, in the real engine ─────────────────────────────────────────


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    return build(FIXTURE, tmp_path_factory.mktemp("en3") / "out")


def _at(g, day, hour, minute=0):
    g.js("""([d, h, m]) => { const t = SugarCube.State.variables.game_state.time_state;
        t.current_day = d; t.current_hour = h; t.current_minute = m; }""", [day, hour, minute])


def _open(g, slug):
    return g.js(f"() => SugarCube.setup.locOpenNow('{slug}')")


def _reason(g, slug):
    return g.js(f"() => SugarCube.setup.locClosedReason('{slug}')")


def _text(g):
    return g.js("() => document.querySelector('.passage').innerText")


@needs_browser
def test_an_open_hour_lets_her_in(html):
    with open_game(html) as g:
        _at(g, "Monday", 10)
        assert _open(g, "loc_shop") is True
        g.play("Location_loc_home")
        assert "Shop —" not in _text(g)
        g.click("Shop")
        assert g.passage() == "Location_loc_shop"
        assert g.sv("player.current_location") == "loc_shop"
        assert CLOSED_TEXT not in _text(g)
        assert g.errors == []


@needs_browser
def test_a_closed_hour_greys_the_link_and_guards_the_room(html):
    with open_game(html) as g:
        _at(g, "Monday", 20)
        assert _open(g, "loc_shop") is False
        g.play("Location_loc_home")
        text = _text(g)
        assert "Shop — Closed. Opens tomorrow at 9:00 AM." in text
        assert not g.js("() => [...document.querySelectorAll('.passage a')]"
                        ".some(a => a.textContent.trim() === 'Shop')")
        g.play("Location_loc_shop")  # a <<goto>> or an old link still lands on the guard
        text = _text(g)
        assert CLOSED_TEXT in text and "Closed. Opens tomorrow at 9:00 AM." in text
        assert "The corner shop." not in text
        assert g.sv("player.current_location") == "loc_home"
        g.click("Go back")
        assert g.passage() == "Location_loc_home"
        assert g.errors == []


@needs_browser
def test_the_travel_card_renders_the_closed_line(html):
    """The fixture has no images, so it builds text links; the card is rendered here from
    the generator's own markup through SugarCube's wikifier on the live page."""
    graph = _graph(_raw())
    gen = TweeComprehensiveGeneratorV2()
    gen.generate(graph.project, {}, graph=graph)
    shop = next(l for l in gen.locations if l.properties["slug"] == "loc_shop")
    card = gen._render_location_nav_card(shop, "./media")
    with open_game(html) as g:
        render = """(m) => { const d = document.createElement('div');
            new SugarCube.Wikifier(d, m); return {text: d.innerText,
            closed: !!d.querySelector('.location-card-closed'),
            link: !!d.querySelector('a.location-card')}; }"""
        _at(g, "Saturday", 10)
        r = g.js(render, card)
        assert r["closed"] and not r["link"]
        assert "Closed. Opens Monday at 9:00 AM." in r["text"]
        _at(g, "Tuesday", 9)
        r = g.js(render, card)
        assert r["link"] and not r["closed"]
        assert g.errors == []


@needs_browser
def test_a_weekday_it_does_not_open(html):
    with open_game(html) as g:
        _at(g, "Saturday", 10)
        assert _open(g, "loc_shop") is False
        assert _reason(g, "loc_shop") == "Closed. Opens Monday at 9:00 AM."
        _at(g, "Monday", 8, 59)
        assert _open(g, "loc_shop") is False
        assert _reason(g, "loc_shop") == "Closed. Opens at 9:00 AM."
        _at(g, "Friday", 16, 59)
        assert _open(g, "loc_shop") is True
        _at(g, "Friday", 17)
        assert _open(g, "loc_shop") is False
        assert g.errors == []


@needs_browser
def test_an_overnight_window(html):
    with open_game(html) as g:
        for day, hour, is_open in [("Friday", 23, True), ("Saturday", 2, True),
                                   ("Saturday", 3, True), ("Saturday", 4, False),
                                   ("Saturday", 5, False), ("Thursday", 23, False),
                                   ("Friday", 2, False), ("Friday", 21, False)]:
            _at(g, day, hour)
            assert _open(g, "loc_club") is is_open, (day, hour)
        _at(g, "Saturday", 5)
        assert _reason(g, "loc_club") == "Closed. Opens Friday at 10:00 PM."
        _at(g, "Friday", 21)
        assert _reason(g, "loc_club") == "Closed. Opens at 10:00 PM."
        _at(g, "Saturday", 1)
        g.play("Location_loc_club")
        assert g.sv("player.current_location") == "loc_club"
        assert g.errors == []


@needs_browser
def test_she_is_not_moved_out_when_it_closes(html):
    with open_game(html) as g:
        _at(g, "Monday", 16, 30)
        g.play("Location_loc_home")
        g.click("Shop")
        assert g.passage() == "Location_loc_shop"
        _at(g, "Monday", 17, 30)  # the clock passes closing time
        assert g.passage() == "Location_loc_shop"
        assert g.sv("player.current_location") == "loc_shop"
        assert g.errors == []


@needs_browser
def test_a_save_made_before_en3_in_a_shop_after_hours(html):
    """§0 rule 8. Written by the PRE-change engine (the EN2c tree, snapshotted to scratch;
    it ignores `hours`): the fixture built with it, the clock set to Monday 20:00, then
    Engine.play Location_loc_shop and Save.serialize() there. Loaded into the EN3 build,
    the room is re-rendered, so she sees the closed screen and a way back."""
    with open_game(html) as g:
        assert g.load_save(read_data("en3_pre_change_save.txt")) is True
        assert g.passage() == "Location_loc_shop"
        text = _text(g)
        assert CLOSED_TEXT in text and "Go back" in text
        g.click("Go back")
        assert g.passage() == "Location_loc_home"
        _at(g, "Tuesday", 10)
        g.play("Location_loc_home")
        g.click("Shop")
        assert g.passage() == "Location_loc_shop"
        assert g.errors == []
