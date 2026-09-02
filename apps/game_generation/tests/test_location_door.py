"""`[locations.door]` — the importer half of the door screen (Doc 73, item 1).

A door is a THRESHOLD the player lands on instead of the room: click Ray's Room and
get a screen with *knock* on it rather than walking straight in. This file covers
only the importer — nothing reads `properties["door"]` yet, so the load-bearing test
here is the INERT one.

Two properties are load-bearing and both are asserted:

  1. **It is inert without a door.** A location that authors none must carry no
     `door` key at all, so every existing game emits byte-identical output. This
     ships into a repo with 26 built games in it, one of them public.
  2. **It cannot FAIL OPEN.** `setup.triggerConditionsSatisfied` returns TRUE for any
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

DOORED = "loc_home"  # the location under test
BARE = "loc_kitchen"  # the location that must stay untouched
CANVAS = "scene_wake_up"  # a canvas id the fixture really has

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
