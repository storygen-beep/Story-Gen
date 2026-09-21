"""Regression tests for the Quests page's third goal shape — `days_since_flag`.

Why it exists. A quest-card condition could only be a FLAG (`is_true`/`is_false`) or a
TRAIT (numeric, with a live "X / Y" suffix on the bullet). Neither can say "and now a
day has to pass", which is what half of vesper's 0.2.2 cot ladder actually waits for:
every step is gated `days_since_flag … gte 1` on the step before it. The page could
therefore only say it in prose, and a wait a player cannot see is a wait they read as
a bug — measured on a real player, who sat on "◯ Wait for him to drink" and reported
the game stuck when it was counting a day and a disguise.

The canvas side has had this predicate since 0.2.2 (`days_since_flag`,
`triggerConditionsSatisfied`). This adds the SAME concept, with the same name and the
same fail-closed rule, to quest-card goals, so an author meets one idea and not two.

What is locked here:

1.  **It parses and it is optional.** A card with no days goal is byte-for-byte what it
    was before the field existed.
2.  **It is validated as its own shape.** Exactly one of `flag` / `trait` /
    `days_since_flag`; numeric op; a `value`; and a `label`, because the label is what
    renders beside the bullet.
3.  **It survives to the runtime JSON.** The serializer emits only the fields that are
    set, so a new field reaches `setup.quests_cards` only if it is carried deliberately.
4.  **The runtime reads the day the flag was set**, from `flags_meta`, and FAILS CLOSED
    when the flag or its meta is missing — the same rule as the canvas predicate, which
    exists because a flag set outside `applyFlagEffect` carries no `set_day`.
5.  **The bullet gets a live number**, so the page shows "0 / 1" and then "1 / 1".

The evaluator is JS inside a string template and this suite does not execute it, so the
last two prove the wiring the way test_npc_schedule_when.py and test_time_of_day.py do.
The behaviour is proved live in the built game by games/vesper/tests/live_the_count.py.
"""

import copy
import json
import re

import pytest

from apps.projects.services.template_import import normalize, parse_toml, validate

FIXTURE = "apps/game_generation/games_toml_files/engine_prd_phase2_2026_04_29.toml"

DAYS_GOAL = {
    "days_since_flag": "frank_home",
    "op": "gte",
    "value": 1,
    "label": "Let a day pass",
}
FLAG_GOAL = {"flag": "frank_home", "op": "is_true", "label": "Get him home"}
TRAIT_GOAL = {
    "trait": "corruption",
    "subject": "player",
    "op": "gte",
    "value": 10,
    "label": "Warm him up",
}


def _game(*goals, when=None):
    """The fixture plus one v2 quest card carrying the goals under test."""
    d = parse_toml(FIXTURE)
    d.setdefault("project", {})["quests_engine"] = "v2"
    d["quest_cards"] = [
        {
            "text": "He is home and he will not look at you.",
            "tip": "Wait a day.",
            "priority": 10,
            "when": when or [{"flag": "frank_home", "op": "is_true"}],
            "goals": [copy.deepcopy(g) for g in goals],
        }
    ]
    return d


def _card_errors(errors):
    return [e for e in errors if "quest_cards" in e]


# ── 1. parse ──────────────────────────────────────────────────────────────────

def test_days_goal_parses_onto_the_card():
    t = normalize(_game(DAYS_GOAL))
    goal = t.quests_cards[0].goals[0]
    assert goal.days_since_flag == "frank_home"
    assert goal.op == "gte"
    assert goal.value == 1
    assert goal.label == "Let a day pass"


def test_days_since_flag_defaults_to_none():
    t = normalize(_game(FLAG_GOAL))
    assert t.quests_cards[0].goals[0].days_since_flag is None


def test_an_empty_days_since_flag_is_not_a_shape():
    """Coerced to None like flag/trait, so the validator sees one clean shape."""
    t = normalize(_game({**FLAG_GOAL, "days_since_flag": ""}))
    assert t.quests_cards[0].goals[0].days_since_flag is None


# ── 2. validate ───────────────────────────────────────────────────────────────

def test_a_valid_days_goal_validates_clean():
    assert _card_errors(validate(normalize(_game(DAYS_GOAL)))) == []


def test_the_three_shapes_stay_mutually_exclusive():
    both = {**DAYS_GOAL, "flag": "frank_home", "op": "is_true"}
    errs = _card_errors(validate(normalize(_game(both))))
    assert errs, "a condition carrying two shapes at once must be rejected"
    assert any("ONLY ONE" in e or "only one" in e for e in errs)


def test_a_days_goal_needs_a_numeric_op():
    errs = _card_errors(validate(normalize(_game({**DAYS_GOAL, "op": "is_true"}))))
    assert any("gte" in e for e in errs), "is_true is meaningless on a day count"


def test_a_days_goal_needs_a_value():
    bad = {k: v for k, v in DAYS_GOAL.items() if k != "value"}
    assert _card_errors(validate(normalize(_game(bad)))), "no value = no threshold"


def test_a_days_goal_needs_a_label():
    bad = {k: v for k, v in DAYS_GOAL.items() if k != "label"}
    errs = _card_errors(validate(normalize(_game(bad))))
    assert errs, "the label is what renders beside the bullet — a goal without one is blank"


def test_the_other_two_shapes_still_validate():
    assert _card_errors(validate(normalize(_game(FLAG_GOAL, TRAIT_GOAL)))) == []


# ── 3. serialize ──────────────────────────────────────────────────────────────

def _cards(d):
    from apps.projects.services.game_graph import build_game_graph

    graph = build_game_graph(normalize(d))
    return (graph.project.metadata or {}).get("quests_cards", [])


def test_the_days_goal_reaches_the_runtime_shape():
    goal = _cards(_game(DAYS_GOAL))[0]["goals"][0]
    assert goal["days_since_flag"] == "frank_home"
    assert goal["op"] == "gte"
    assert goal["value"] == 1
    assert goal["label"] == "Let a day pass"


def test_a_card_without_a_days_goal_is_unchanged():
    goal = _cards(_game(FLAG_GOAL))[0]["goals"][0]
    assert goal == {"flag": "frank_home", "op": "is_true", "label": "Get him home"}


# ── 4. emission ───────────────────────────────────────────────────────────────

def _twee(d):
    from apps.game_generation.twee_comprehensive.generators.v2 import (
        TweeComprehensiveGeneratorV2,
    )
    from apps.projects.services.game_graph import build_game_graph

    graph = build_game_graph(normalize(d))
    return TweeComprehensiveGeneratorV2().generate(graph.project, {}, graph=graph)


def _fn_body(twee, decl):
    m = re.search(decl, twee)
    assert m, f"{decl} not emitted"
    depth, start = 0, twee.index("{", m.end() - 1)
    for j in range(start, len(twee)):
        if twee[j] == "{":
            depth += 1
        elif twee[j] == "}":
            depth -= 1
            if depth == 0:
                return twee[start : j + 1]
    raise AssertionError(f"unbalanced body for {decl}")


def test_the_card_is_emitted_with_its_days_goal():
    twee = _twee(_game(DAYS_GOAL))
    m = re.search(r"setup\.quests_cards = (\[.*?\]);\n", twee, re.S)
    assert m, "setup.quests_cards not emitted"
    assert json.loads(m.group(1))[0]["goals"][0]["days_since_flag"] == "frank_home"


# ── 5. runtime wiring ─────────────────────────────────────────────────────────

def test_the_evaluator_reads_set_day_and_fails_closed():
    body = _fn_body(_twee(_game(DAYS_GOAL)), r"setup\.checkQuestsCondition = function")
    assert "days_since_flag" in body, "the goal shape the author writes is not evaluated"
    assert "flags_meta" in body and "set_day" in body, (
        "days elapsed must come from the day the flag was SET, the way the canvas "
        "predicate does — not from a counter"
    )
    assert "time_state" in body


def test_the_renderer_prints_the_day_count_beside_the_bullet():
    """The suffix used to be gated on `goal.trait`, so a days goal rendered a bare
    "◯ Let a day pass" — the number the whole feature exists for was computed and
    thrown away. Caught live on the built page, not here; pinned here."""
    body = _fn_body(_twee(_game(DAYS_GOAL)), r"setup\.renderQuestsGoalBlock = function")
    assert "days_since_flag" in body, (
        "the goal renderer ignores the days shape, so the bullet shows no 'X / Y'"
    )


def test_the_bullet_gets_a_live_day_count():
    body = _fn_body(_twee(_game(DAYS_GOAL)), r"function _readCurrentValue")
    assert "days_since_flag" in body, (
        "without this the bullet renders no 'X / Y' and the player still cannot see "
        "how long the wait is"
    )
