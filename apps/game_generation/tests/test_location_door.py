"""`[locations.door]` — the door screen: importer plumbing AND generator emission.

A door is a THRESHOLD the player lands on instead of the room: click Ray's Room and
get a screen with *knock* on it rather than walking straight in. Doc 73 items 1-2.

Two properties are load-bearing and both are asserted:

  1. **It is inert without a door.** A location that authors none carries no `door`
     key, AND no door machinery is emitted at all — not the renderer, not the
     isRerenderSafe clause, not the payload key. Every existing game must build
     byte-identical; measured on 27 builds. This ships into a repo with 26 built
     games in it, one of them public. The first cut of the generator emitted the
     runtime unconditionally and moved every game by ~2.7 KB, which is why
     `_has_doors()` gates all three sites — the same rule the travel-friction block
     follows ("only emitted when some location declares costs").
  2. **The door screen writes NOTHING.** No <<pass>>, no effect, no flag, no
     current_location. That is what makes it legal for setup.isRerenderSafe, and what
     stops a save parked on a door re-charging on reload. Cost lives on the far side.

  3. **It cannot FAIL OPEN.** `setup.triggerConditionsSatisfied` returns TRUE for any
     conditions{} missing `version`, with no build error — so a versionless option
     would render forever and its gate would never bite. The importer must refuse it.

⚠️ THE FOUR-HOP CHAIN. Nothing in template_import.py rejects an unknown TOML key, so
a forgotten line in the dataclass, the parser, or EITHER of the two writers makes the
feature evaporate with no error anywhere. The writers are the trap:
`create_project_from_template` (DB) and `build_game_graph` (no-DB) keep near-identical
location loops, and the no-DB one is what a real build uses. v2.py:9858-9861 records
the same defect class for the two location emitters — "byte-identical copies… that is
how a change like this gets half-applied."

⚠️ Targets **v2** and the no-DB path, as test_support_url.py and test_cheat_page.py do.

Run with an explicit path — pyproject sets testpaths = ["tests"], so app suites are
not collected by a bare `pytest`:

    pytest apps/game_generation/tests/test_location_door.py -q
"""
import copy
import inspect

import pytest

from apps.projects.services import game_graph, template_import
from apps.projects.services.game_graph import build_game_graph
from apps.projects.services.template_import import normalize, parse_toml, validate

FIXTURE = "apps/game_generation/games_toml_files/engine_prd_phase2_2026_04_29.toml"

# loc_kitchen is the CHILD: the only one with a nav card to check, and the only one
# with an entry_from to leave to. loc_home is the root and never renders as a
# destination, so a door on it could not be reached from the map at all.
DOORED = "loc_kitchen"
BARE = "loc_home"
# A canvas with a TRIGGER LOCATION, so it survives _compute_included_canvases. A
# trigger-less canvas is pruned from the build and its option is dropped with a
# warning — see _door_for_payload's known-limit note.
CANVAS = "scene_advance_frank_to_1"

V1 = {
    "version": "1.0",
    "logic": "AND",
    "items": [
        {
            "type": "flag",
            "subject": "player",
            "flag_key": "ray_open",
            "operator": "is_true",
        }
    ],
}
VERSIONLESS = {"logic": "AND", "items": V1["items"]}


def _raw():
    return parse_toml(FIXTURE)


def _door(**over):
    """A well-formed door: one knock into a canvas, one shown-locked way in."""
    d = {
        "description": "The door at the back of the house.",
        "no_answer": "You knock. Nobody comes to it.",
        "options": [
            {
                "text": "Knock.",
                "conditions": V1,
                "goes_to": {"type": "canvas", "canvas_id": CANVAS},
            },
            {
                "text": "Go in.",
                "conditions": V1,
                "show_when_locked": True,
                "locked_text": "You have got as far as the handle twice.",
                "goes_to": {"type": "enter"},
            },
        ],
    }
    d.update(over)
    return d


def _with_door(door, loc_id=DOORED):
    d = _raw()
    for loc in d["locations"]:
        if loc["id"] == loc_id:
            loc["door"] = copy.deepcopy(door)
    return d


def _loc(container, loc_id):
    """A location out of a normalized template or a built graph, by slug."""
    for item in container:
        if (
            getattr(item, "id", None) == loc_id
            or (getattr(item, "properties", None) or {}).get("slug") == loc_id
        ):
            return item
    raise AssertionError(f"{loc_id} not found")


def _location_passage(loc_id):
    """The Twee passage a location is emitted at — slug-based, stable across renames."""
    return f"Location_{loc_id}"


def _door_errors(d):
    return [e for e in validate(normalize(d)) if " door" in e]


# ── 1. the four-hop chain ────────────────────────────────────────────────────


def test_a_door_survives_normalize_onto_the_dataclass():
    """Hop 1+2 — the dataclass field and the parse line."""
    t = normalize(_with_door(_door()))
    assert _loc(t.locations, DOORED).door["options"][0]["text"] == "Knock."


def test_a_door_reaches_the_graph_path():
    """Hop 4, and the one that matters: build_game_graph is what a real build calls.
    A door written only to the DB path parses, validates, and never reaches the
    generator."""
    graph = build_game_graph(normalize(_with_door(_door())))
    props = _loc(graph.locations, DOORED).properties
    assert props["door"]["no_answer"] == "You knock. Nobody comes to it."
    assert len(props["door"]["options"]) == 2


def test_the_conditions_reach_the_writer_verbatim():
    """No re-shaping in the importer — the generator gets the authored block, the
    same way entry_conditions and description_variants do."""
    graph = build_game_graph(normalize(_with_door(_door())))
    opt = _loc(graph.locations, DOORED).properties["door"]["options"][0]
    assert opt["conditions"]["version"] == "1.0"
    assert opt["conditions"]["items"][0]["flag_key"] == "ray_open"


def test_both_writers_carry_the_door():
    """Hop 3+4 together. The two location loops are near-identical copies and the
    whole point of this test is that they cannot drift apart silently."""
    for mod in (game_graph, template_import):
        src = inspect.getsource(mod)
        assert (
            'loc.properties["door"] = l.door' in src
        ), f"{mod.__name__} does not write the door into loc.properties"


# ── 2. inert without a door ─────────────────────────────────────────────────


def test_a_location_with_no_door_carries_no_door_key():
    """The installed-base guarantee. Not `{}` — absent, like every other optional
    field, so no existing game's output can move by a byte."""
    graph = build_game_graph(normalize(_raw()))
    for loc in graph.locations:
        assert "door" not in (loc.properties or {})


def test_a_doored_location_does_not_touch_its_neighbours():
    graph = build_game_graph(normalize(_with_door(_door())))
    assert "door" not in (_loc(graph.locations, BARE).properties or {})


def test_the_unmodified_fixture_raises_no_door_errors():
    assert _door_errors(_raw()) == []


def test_a_well_formed_door_raises_no_errors():
    assert _door_errors(_with_door(_door())) == []


# ── 3. it cannot fail open ──────────────────────────────────────────────────


def test_versionless_option_conditions_are_refused():
    """V3. The whole reason this check exists: a conditions{} without `version`
    evaluates TRUE forever, with no build error, so the option would never be gated."""
    errs = _door_errors(
        _with_door(
            _door(
                options=[
                    {
                        "text": "Knock.",
                        "conditions": VERSIONLESS,
                        "goes_to": {"type": "enter"},
                    },
                ]
            )
        )
    )
    assert len(errs) == 1 and 'version = "1.0"' in errs[0] and DOORED in errs[0]


def test_versionless_door_variant_conditions_are_refused():
    errs = _door_errors(
        _with_door(
            _door(
                description_variants=[
                    {"conditions": VERSIONLESS, "text": "The door is shut."},
                ]
            )
        )
    )
    assert len(errs) == 1 and 'version = "1.0"' in errs[0]


def test_an_option_may_omit_conditions_entirely():
    """Omitted is not the same defect as versionless — an always-available option is
    legitimate, and refusing it would push authors toward the fail-open form."""
    assert (
        _door_errors(
            _with_door(
                _door(
                    options=[
                        {"text": "Go in.", "goes_to": {"type": "enter"}},
                    ]
                )
            )
        )
        == []
    )


# ── 4. the rest of the contract, one defect at a time ───────────────────────


@pytest.mark.parametrize(
    "door,fragment",
    [
        # V1
        ({"description": "A door."}, "has no options"),
        ({"description": "A door.", "options": []}, "has no options"),
        # V2
        ({"options": ["not a table"]}, "must be a table"),
        ({"options": [{"text": "  ", "goes_to": {"type": "enter"}}]}, "has no text"),
        # V4
        (
            {"options": [{"text": "Go.", "goes_to": {"type": "teleport"}}]},
            "not one of 'enter', 'canvas'",
        ),
        # V5
        (
            {"options": [{"text": "Go.", "goes_to": {"type": "canvas"}}]},
            "needs a canvas_id",
        ),
        (
            {
                "options": [
                    {"text": "Go.", "goes_to": {"type": "canvas", "canvas_id": "nope"}}
                ]
            },
            "not found in canvases",
        ),
        # V6
        (
            {
                "options": [
                    {
                        "text": "Go.",
                        "conditions": V1,
                        "show_when_locked": True,
                        "goes_to": {"type": "enter"},
                    }
                ]
            },
            "must say why",
        ),
    ],
)
def test_one_malformed_door_yields_exactly_one_error(door, fragment):
    errs = _door_errors(_with_door(door))
    assert len(errs) == 1, errs
    assert fragment in errs[0]
    assert DOORED in errs[0]


def test_show_when_locked_falls_back_to_the_locations_blocked_message():
    """V6's escape hatch — the lock is declared once, on the location."""
    d = _with_door(
        _door(
            options=[
                {
                    "text": "Go in.",
                    "conditions": V1,
                    "show_when_locked": True,
                    "goes_to": {"type": "enter"},
                },
            ]
        )
    )
    for loc in d["locations"]:
        if loc["id"] == DOORED:
            loc["blocked_message"] = "The door's shut and the light's off."
    assert _door_errors(d) == []


@pytest.mark.parametrize(
    "key,value,fragment",
    [
        ("auto_exit", False, "transit stop"),
        ("offscreen", True, "offscreen"),
        ("is_container", True, "container"),
    ],
)
def test_a_door_needs_a_nav_card_to_hang_off(key, value, fragment):
    """V7/V8 — three location kinds render no nav card, so a door on one is authored
    and unreachable, which is the defect this whole PRD exists to stop shipping."""
    d = _with_door(_door())
    for loc in d["locations"]:
        if loc["id"] == DOORED:
            loc[key] = value
    errs = _door_errors(d)
    assert any(fragment in e for e in errs), errs


# ── 5. validate() accumulates, it does not raise ────────────────────────────


def test_validate_returns_strings_and_never_raises():
    """The house convention: normalize() raises, validate() accumulates. A malformed
    door must not blow up the --validate path."""
    for door in (
        {"options": ["junk"]},
        {"options": [{"goes_to": "junk"}]},
        {"options": [{"text": "x", "conditions": "junk"}]},
    ):
        errs = _door_errors(_with_door(door))
        assert errs and all(isinstance(e, str) for e in errs)


# ── 6. the generator (Doc 73 item 2) ────────────────────────────────────────


def _build(d):
    from apps.game_generation.twee_comprehensive.generators.v2 import (
        TweeComprehensiveGeneratorV2,
    )

    graph = build_game_graph(normalize(d))
    return TweeComprehensiveGeneratorV2().generate(graph.project, {}, graph=graph)


def _setup_locations(twee):
    import json
    import re

    m = re.search(r"setup\.locations = (\{.*?\});", twee, re.S)
    assert m, "setup.locations not emitted"
    return json.loads(m.group(1))


def test_a_doorless_game_emits_no_door_machinery_at_all():
    """The installed-base guarantee, and the one this feature got wrong first: an
    unconditionally-emitted runtime moved all 26 built games by ~2.7 KB for nothing."""
    twee = _build(_raw())
    assert ":: Door_" not in twee
    assert "renderDoorOptions" not in twee
    assert 'title.indexOf("Door_")' not in twee
    for loc in _setup_locations(twee).values():
        assert "door" not in loc


def test_a_door_emits_exactly_one_threshold_passage():
    twee = _build(_with_door(_door()))
    assert twee.count(f":: Door_{DOORED}") == 1
    assert "setup.renderDoorOptions = function" in twee


def test_the_threshold_writes_nothing():
    """Load-bearing, not tidy. A committed post-render state is only sound if
    re-running the passage body is a no-op — otherwise every reload re-applies it."""
    twee = _build(_with_door(_door()))
    body = twee[twee.index(f":: Door_{DOORED}") :]
    body = body[: body.index("\n:: ")] if "\n:: " in body else body
    for forbidden in (
        "<<pass",
        "current_location",
        "visited_locations",
        "<<set $",
        "advanceTime",
    ):
        assert forbidden not in body, f"{forbidden!r} in the door passage"


def test_the_threshold_is_rerender_safe():
    twee = _build(_with_door(_door()))
    assert 'if (title.indexOf("Door_") === 0) return true;' in twee


def test_the_threshold_is_not_in_passage_to_location():
    """What keeps a door FREE by construction: the travel-cost intercept and the
    clothing check both key off this map, and neither may see a threshold."""
    import json
    import re

    twee = _build(_with_door(_door()))
    m = re.search(r"setup\.passage_to_location = (\{.*?\});", twee, re.S)
    assert m
    assert not [k for k in json.loads(m.group(1)) if k.startswith("Door_")]


def _with_images(d):
    """Force the nav grid: it renders cards only when some destination has an image
    defined (found or missing), else it falls back to text links."""
    for loc in d["locations"]:
        loc["image"] = f"locations/{loc['id']}.jpg"
    return d


@pytest.mark.parametrize("mode", ["text", "grid"])
def test_the_nav_points_at_the_door_and_never_greys_it_out(mode):
    """You can knock at a door you may not enter, so the destination must stay
    clickable and must never take the `navDestUnlocked` fork — the branch that would
    render it as an inert <div>. Asserted in BOTH nav modes, because the grid and the
    text list are separate renderers and only one of them is exercised by a fixture
    with no images."""
    d = _with_door(_door())
    if mode == "grid":
        d = _with_images(d)
    twee = _build(d)
    assert f"Door_{DOORED}" in twee
    # no lock fork for a door location, in either renderer
    assert f'setup.navDestUnlocked("{DOORED}")' not in twee
    # and the room itself is no longer a navigable destination
    assert f'data-passage="Location_{DOORED}"' not in twee
    assert f"[[Kitchen->Location_{DOORED}]]" not in twee
    if mode == "grid":
        assert f'data-passage="Door_{DOORED}"' in twee
    else:
        assert f"->Door_{DOORED}]]" in twee


def test_the_door_card_keeps_the_presence_badges():
    """The locked card drops them (v2.py's `indicators` sits only in the open branch),
    and knowing someone is in there is exactly why a player would knock."""
    twee = _build(_with_images(_with_door(_door())))
    card = twee[twee.index(f'data-passage="Door_{DOORED}"') :]
    card = card[: card.index("</a>")]
    assert "getNpcsPresentAtLocation" in card


def test_a_locked_location_without_a_door_still_greys_out():
    """The vesper guarantee. All 11 of its locked locations are story gates, not
    doors, and every one must keep rendering exactly as it does today."""
    d = _raw()
    for loc in d["locations"]:
        if loc["id"] == DOORED:
            loc["entry_conditions"] = V1
            loc["blocked_message"] = "The door's shut and the light's off."
    twee = _build(d)
    assert "location-card-locked" in twee
    assert ":: Door_" not in twee


def test_option_targets_are_resolved_at_generation_time():
    """The runtime never has to know how a passage is named."""
    twee = _build(_with_door(_door()))
    opts = _setup_locations(twee)[DOORED]["door"]["options"]
    by_text = {o["text"]: o for o in opts}
    assert by_text["Knock."]["passage"].startswith("Canvas_")
    assert by_text["Go in."]["passage"] == f"Location_{DOORED}"


def test_the_locations_blocked_message_rides_along_as_the_fallback():
    """The lock stays declared once, on the location — V6's escape hatch, resolved."""
    d = _with_door(
        _door(
            options=[
                {
                    "text": "Go in.",
                    "conditions": V1,
                    "show_when_locked": True,
                    "goes_to": {"type": "enter"},
                },
            ]
        )
    )
    for loc in d["locations"]:
        if loc["id"] == DOORED:
            loc["blocked_message"] = "The door's shut and the light's off."
    door = _setup_locations(_build(d))[DOORED]["door"]
    assert door["blocked_message"] == "The door's shut and the light's off."


def test_the_door_prose_is_the_rooms_own_variant_chain():
    """One slot, shared with _render_location_description — two copies is how half a
    change ships (v2.py's own note on the two location emitters)."""
    twee = _build(
        _with_door(
            _door(
                description_variants=[
                    {
                        "conditions": V1,
                        "text": "The door is shut and the light is off.",
                    },
                ]
            )
        )
    )
    body = twee[twee.index(f":: Door_{DOORED}") :]
    body = body[: body.index("\n:: ")]
    assert "<<if setup.triggerConditionsSatisfied(" in body
    assert "<<else>><p>The door at the back of the house.</p><</if>>" in body


def test_the_threshold_carries_a_way_back():
    """53 of 54 field door screens do. A threshold you cannot leave is a trap."""
    twee = _build(_with_door(_door()))
    body = twee[twee.index(f":: Door_{DOORED}") :]
    body = body[: body.index("\n:: ")]
    assert f"[[Leave->{_location_passage(BARE)}]]" in body


def test_the_navigation_screen_cannot_walk_past_the_door():
    """The bypass this feature shipped with first. `:: Navigation` is a second,
    engine-generated list of every location, and it linked straight into the room —
    so a player could reach Ray's bedroom without ever seeing his door. Every
    engine-generated way IN now goes through _location_entry_passage."""
    twee = _build(_with_door(_door()))
    nav = twee[twee.index("\n:: Navigation") :]
    nav = nav[: nav.index("\n:: ", 1)]
    assert f"Door_{DOORED}" in nav
    assert f"[[Kitchen->Location_{DOORED}]]" not in nav


def test_back_to_your_current_location_still_goes_to_the_room():
    """The one link that must NOT be redirected: she is already inside, and bouncing
    her onto her own threshold would be a loop, not a door."""
    twee = _build(_with_door(_door()))
    nav = twee[twee.index("\n:: Navigation") :]
    nav = nav[: nav.index("\n:: ", 1)]
    if "Back to" in nav:
        assert f"[[Back to Kitchen->Location_{DOORED}]]" in nav
