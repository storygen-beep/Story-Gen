"""Regression tests for `[[npcs.schedules]] when` — a schedule row that only applies
while a story condition holds.

Why it exists. A schedule row used to keep exactly five keys (location, weekdays,
start_time, end_time, activity) and apply forever. Two things read rows with no
regard for the story: the nav-card presence badge (`getNpcsPresentAtLocation`) and
the Schedules page. So a character could not be placed somewhere only AFTER a plot
beat without leaking their face onto that location's card — and their name onto the
Schedules page — in every save that could reach it, including saves where the beat
never happened. Measured on vesper 0.2.2: Bastien, rescued to the cot, could not get
a portrait card there without appearing at the cot in 1b saves where he is, as far
as that playthrough knows, dead.

What is locked here:

1.  **It parses, and it is optional.** A row without `when` is byte-for-byte what it
    was before this field existed.
2.  **It is validated hard.** A `when` without `version = "1.0"` FAILS OPEN at
    runtime (`triggerConditionsSatisfied` returns true for any versionless block),
    so the row would always apply and the leak it was written to prevent would
    return silently. That is a build error, not a warning.
3.  **It cannot recurse.** `npc_at_location` resolves presence through
    `getNpcLocation`, which is the function evaluating the row. Inside a row's
    `when` it is rejected — directly, and through a `stage` helper that contains it.
4.  **It reaches a packaged game through BOTH write sites.** `ai_behavior_config`
    is built by hand in `game_graph.build_game_graph` (the default no-DB path) AND
    in `template_import.create_project_from_template` (`--use-db`). A key added to
    one reaches the other never, with no error anywhere — `test_npc_tags_field.py`
    records the same trap.
5.  **The runtime honours it everywhere a row is read**, through one helper.
"""

import copy
import json
import re

import pytest

from apps.projects.services.template_import import normalize, parse_toml, validate

FIXTURE = "apps/game_generation/games_toml_files/engine_prd_phase2_2026_04_29.toml"
KITCHEN = "loc_kitchen"
NPC = "npc_frank"

WHEN_RESCUED = {
    "version": "1.0",
    "logic": "AND",
    "items": [
        {"type": "flag", "subject": "player", "flag_key": "frank_home", "operator": "is_true"},
    ],
}


def _row(**extra):
    row = {
        "location": KITCHEN,
        "weekdays": [0, 1, 2, 3, 4, 5, 6],
        "start_time": "06:00",
        "end_time": "10:00",
        "activity": "coffee",
    }
    row.update(extra)
    return row


def _game(*rows, helpers=None):
    d = parse_toml(FIXTURE)
    for npc in d["npcs"]:
        if npc["id"] == NPC:
            npc["schedules"] = [copy.deepcopy(r) for r in rows]
    if helpers:
        d.setdefault("engine", {})["stage_helpers"] = helpers
    return d


def _when_errors(errors):
    return [e for e in errors if ".when" in e]


# ── 1. parse ──────────────────────────────────────────────────────────────────

def test_when_parses_onto_the_row():
    t = normalize(_game(_row(when=WHEN_RESCUED)))
    frank = next(n for n in t.npcs if n.id == NPC)
    assert frank.schedules[0].when == WHEN_RESCUED


def test_when_defaults_to_none():
    t = normalize(_game(_row()))
    frank = next(n for n in t.npcs if n.id == NPC)
    assert frank.schedules[0].when is None


def test_when_must_be_a_table():
    with pytest.raises(TypeError, match=r"when"):
        normalize(_game(_row(when="frank_home")))


# ── 2. validate ───────────────────────────────────────────────────────────────

def test_a_valid_when_validates_clean():
    assert _when_errors(validate(normalize(_game(_row(when=WHEN_RESCUED))))) == []


def test_when_without_version_is_a_build_error():
    versionless = {k: v for k, v in WHEN_RESCUED.items() if k != "version"}
    errs = _when_errors(validate(normalize(_game(_row(when=versionless)))))
    assert errs, "a versionless `when` must be rejected — it fails OPEN at runtime"
    assert any('version = "1.0"' in e for e in errs)


def test_empty_when_is_a_build_error():
    errs = _when_errors(validate(normalize(_game(_row(when={})))))
    assert errs, "an empty `when` gates nothing and must be omitted instead"


def test_npc_at_location_in_when_is_rejected():
    recursive = {
        "version": "1.0",
        "items": [{"type": "npc_at_location", "location_id": KITCHEN, "npc_id": NPC,
                   "operator": "is_present"}],
    }
    errs = _when_errors(validate(normalize(_game(_row(when=recursive)))))
    assert any("npc_at_location" in e for e in errs)


def test_npc_at_location_through_a_stage_helper_is_rejected():
    helpers = [{
        "name": "frank_about",
        "conditions": {"version": "1.0", "items": [
            {"type": "npc_at_location", "location_id": KITCHEN, "operator": "is_present"},
        ]},
    }]
    via_stage = {
        "version": "1.0",
        "items": [{"type": "stage", "helper": "frank_about", "operator": "is_true"}],
    }
    errs = _when_errors(validate(normalize(_game(_row(when=via_stage), helpers=helpers))))
    assert any("npc_at_location" in e for e in errs)


# ── 3. both write sites ───────────────────────────────────────────────────────

def test_no_db_path_carries_when():
    from apps.projects.services.game_graph import build_game_graph

    graph = build_game_graph(normalize(_game(_row(when=WHEN_RESCUED))))
    frank = next(n for n in graph.npcs if n.ai_behavior_config.get("schedules"))
    assert frank.ai_behavior_config["schedules"][0]["when"] == WHEN_RESCUED, (
        "`when` did not survive the no-DB path — game_graph.py builds the schedule "
        "dict by hand and must carry it alongside template_import.py"
    )


def test_no_db_path_omits_when_when_unused():
    from apps.projects.services.game_graph import build_game_graph

    graph = build_game_graph(normalize(_game(_row())))
    frank = next(n for n in graph.npcs if n.ai_behavior_config.get("schedules"))
    assert "when" not in frank.ai_behavior_config["schedules"][0]


@pytest.mark.django_db
def test_db_path_carries_when():
    from django.contrib.auth import get_user_model

    from apps.npcs.models import NPC as NPCModel
    from apps.projects.services.template_import import create_project_from_template

    user = get_user_model().objects.create_user(
        email="schedule-when@example.com", password="testpass123"
    )
    t = normalize(_game(_row(when=WHEN_RESCUED), _row(start_time="12:00", end_time="14:00")))
    result = create_project_from_template(t, str(user.id))
    rows = NPCModel.objects.get(project_id=result["project_id"], name="Frank") \
        .ai_behavior_config["schedules"]
    assert rows[0]["when"] == WHEN_RESCUED
    assert "when" not in rows[1]


# ── 4. emission ───────────────────────────────────────────────────────────────

def _twee(d):
    from apps.game_generation.twee_comprehensive.generators.v2 import (
        TweeComprehensiveGeneratorV2,
    )
    from apps.projects.services.game_graph import build_game_graph

    graph = build_game_graph(normalize(d))
    return TweeComprehensiveGeneratorV2().generate(graph.project, {}, graph=graph)


def _npc_schedules(twee):
    m = re.search(r"setup\.npcSchedules = (\{.*?\});\n", twee, re.S)
    assert m, "setup.npcSchedules not emitted"
    return json.loads(m.group(1))


def _fn_body(twee, name):
    m = re.search(r"setup\.%s = function\([^)]*\) \{" % re.escape(name), twee)
    assert m, f"{name} not emitted"
    depth, start = 0, m.end() - 1
    for j in range(start, len(twee)):
        if twee[j] == "{":
            depth += 1
        elif twee[j] == "}":
            depth -= 1
            if depth == 0:
                return twee[start : j + 1]
    raise AssertionError(f"unbalanced body for {name}")


def test_when_is_emitted_only_where_authored():
    twee = _twee(_game(_row(when=WHEN_RESCUED), _row(start_time="12:00", end_time="14:00")))
    rows = _npc_schedules(twee)[NPC]
    assert rows[0]["when"] == WHEN_RESCUED
    assert "when" not in rows[1], "an unconditioned row must emit exactly as before"


# ── 5. runtime ────────────────────────────────────────────────────────────────
# The evaluator is JS inside a string template and the Python suite does not execute
# it, so these prove the wiring, the way test_time_of_day.py does. The behaviour is
# proved live in the built game (see the vesper ledger, rev 225).

def test_one_helper_decides_whether_a_row_is_live():
    body = _fn_body(_twee(_game(_row())), "_scheduleRowLive")
    assert "triggerConditionsSatisfied" in body
    assert "when" in body


@pytest.mark.parametrize("reader", [
    "getNpcLocation",            # presence: nav badge, portraits, npc_at_location all go through it
    "getNpcDaySchedule",
    "getNpcAllSchedulesSorted",  # the Schedules page rows
    "getNpcsWithSchedules",      # the Schedules page roster
])
def test_every_row_reader_consults_the_helper(reader):
    assert "_scheduleRowLive" in _fn_body(_twee(_game(_row())), reader)
