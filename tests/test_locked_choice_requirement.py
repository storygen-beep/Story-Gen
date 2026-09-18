"""A locked choice must say WHAT IT WANTS, not only that she cannot.

Why this exists. LO, playing vesper's bunker, hit a greyed rung reading

    Not on this one. Not with what she can do.

and asked the obvious question: which number, and how far off is she? The engine
already had the answer and was throwing it away. `setup.describeUnmetConditions`
(v2.py:2026) builds exactly `"Fighting 35+ (you have 12)"`, and the COST rung already
renders that style — `"Work a shift (Requires 15 Energy (you have 6))"`
(test_legacy_engine.py ChoiceCostsTests). The condition rung printed the author's
static `locked_text` and stopped, so every threshold in every game was a guess.

What is locked here:

1.  **The suffix is appended, not substituted.** The authored line is the voice and it
    stays; the requirement goes in a bracket beside it, the same shape the cost rung
    already ships.
2.  **Numbers only — never flags.** The same helper also phrases flag gates
    ("Requires: Raid done"), and a locked choice is very often gated on a hidden plot
    flag. Printing those spoils the story on a greyed tile. Trait gates are the
    numbers the player is meant to chase; flag gates stay the author's business.
3.  **NPC traits are excluded too.** `describeUnmetConditions` renders an npc-subject
    trait as a bare "Corruption 40+" with no idea whose, and the player cannot see an
    NPC's stats anyway.
4.  **Nothing else moves.** A choice with no trait gate, and a game with no locked
    choices, must build exactly as before — this ships into a repo with built games in
    it, one of them public.
5.  **Unreachable predicates stay silent.** `time_of_day` has no phrasing in the helper
    (a known gap, test_time_of_day.py:126-137), so a clock-gated choice appends
    nothing rather than a half-sentence.

Targets **v2** and the DB path used by the sibling ChoiceCostsTests fixture.

    pytest tests/test_locked_choice_requirement.py -q
"""

import copy
import re

import pytest
from django.contrib.auth import get_user_model

from apps.projects.models import Project
from apps.projects.services.template_import import (
    create_project_from_template,
    normalize,
    validate,
)

pytestmark = pytest.mark.django_db

LOC = "loc_bar"
CANVAS = "canvas_start"


def _trait(key, value, subject="player", operator="gte"):
    return {"type": "trait", "subject": subject, "trait_key": key,
            "operator": operator, "value": value}


def _template(choices):
    return {
        "schema_version": "1.0",
        "project": {
            "id": "locked_requirement_test",
            "title": "Locked Requirement Fixture",
            "description": "Minimal fixture for the locked-choice requirement suffix.",
            "starting_canvas": CANVAS,
        },
        "time": {"enabled": True, "starting_hour": 8, "starting_day": "Monday"},
        "player": {
            "id": "player",
            "name": "Test Player",
            "core_traits": {"fighting": 0, "stealth": 0, "energy": 100, "equipped_weapon": 1,
                            "bottle_held": 0},
            "flag_keys": ["raid_done"],
        },
        "locations": [{"id": LOC, "name": "The Bar", "description": "Test bar."}],
        "npcs": [],
        "canvases": [{
            "id": CANVAS,
            "name": "Start",
            "type": "scene",
            "trigger": {"location": LOC, "is_active": True,
                        "is_repeatable": True, "trigger_mode": "manual"},
            "nodes": [{
                "id": "n1",
                "name": "Start Node",
                "blocks": [{"type": "paragraph", "props": {},
                            "content": [{"type": "text", "text": "test"}]}],
                "exit_block": {"type": "choices", "choices": choices},
            }],
        }],
    }


@pytest.fixture
def build(db):
    user = get_user_model().objects.create_user(
        email="locked-requirement@example.com", password="testpass123"
    )

    def _build(choices):
        from apps.game_generation.twee_comprehensive.generators.v2 import (
            TweeComprehensiveGeneratorV2,
        )
        template = normalize(copy.deepcopy(_template(choices)))
        errors = validate(template)
        assert errors == [], f"fixture should validate clean: {errors}"
        result = create_project_from_template(template, str(user.id))
        project = Project.objects.get(id=result["project_id"])
        return TweeComprehensiveGeneratorV2().generate(project)

    return _build


PLAIN = {"text": "Leave", "targetType": "trigger", "effects": []}


def _locked(text, locked_text, items):
    return {
        "text": text,
        "targetType": "trigger",
        "show_when_locked": True,
        "locked_text": locked_text,
        "conditions": {"version": "1.0", "items": items},
        "effects": [],
    }


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
                return twee[start:j + 1]
    raise AssertionError(f"unbalanced body for {name}")


# ── 1. the suffix rides beside the authored line ─────────────────────────────

def test_locked_choice_appends_the_requirement(build):
    twee = build([PLAIN, _locked("Put him down.", "Not on this one. Not with what she can do.",
                                 [_trait("fighting", 35)])])
    assert "Not on this one. Not with what she can do.<<= setup.requirementSuffix(" in twee, (
        "the locked rung must keep the authored line and append the live requirement "
        "beside it, the way the cost rung already does"
    )


def test_the_authored_line_is_not_replaced(build):
    twee = build([PLAIN, _locked("Put him down.", "Not on this one. Not with what she can do.",
                                 [_trait("fighting", 35)])])
    assert "Not on this one. Not with what she can do." in twee


def test_a_choice_with_no_trait_gate_gets_no_suffix(build):
    """A flag-only lock is plot, and plot is the author's line alone."""
    twee = build([PLAIN, _locked("Go down.", "Not until the raid is done.",
                                 [{"type": "flag", "subject": "player",
                                   "flag_key": "raid_done", "operator": "is_true"}])])
    assert "Not until the raid is done.<<= setup.requirementSuffix(" not in twee, (
        "a flag-gated lock must not carry a requirement suffix — it would name a hidden "
        "story flag on a greyed tile"
    )


def test_a_game_with_no_locked_choices_is_unchanged(build):
    twee = build([PLAIN])
    assert "requirementSuffix(" not in twee.split("setup.requirementSuffix = function")[-1], (
        "no locked choice authored, so no call site may be emitted"
    )


# ── 2. the helper: numbers only ──────────────────────────────────────────────

def test_the_helper_is_emitted(build):
    body = _fn_body(build([PLAIN]), "requirementSuffix")
    assert "describeUnmetTraits" in body, "the suffix must go through the traits-only helper"


def test_the_traits_helper_keeps_only_player_trait_items(build):
    body = _fn_body(build([PLAIN]), "describeUnmetTraits")
    assert "'trait'" in body or '"trait"' in body, "it must filter on the trait type"
    assert "npc" in body, "npc-subject traits must be excluded — the player cannot see them"
    assert "describeUnmetConditions" in body, (
        "phrasing must be reused, not duplicated — one wording for locks and costs"
    )


def test_the_helper_is_emitted_even_with_no_locked_choices(build):
    """It is two small functions and it lives beside describeUnmetConditions, which is
    already unconditional. Gating it would be a second emission site to keep in step."""
    twee = build([PLAIN])
    assert "setup.describeUnmetTraits = function" in twee
    assert "setup.requirementSuffix = function" in twee


def test_an_enum_trait_gate_gets_no_suffix(build):
    """Found in live play, not in review. vesper's emitter rung is gated
    `equipped_weapon eq 2` (1 = drain, 2 = emitter) and rendered

        The emitter is empty, or she is carrying the drain instead.
        (Equipped_weapon exactly 2 (you have 1))

    — an internal loadout key, underscore and all, on screen. `eq`/`ne` on a trait is
    a state check, not a threshold the player can train towards, and the authored line
    already says it better. Only magnitude comparisons earn a bracket."""
    twee = build([PLAIN, _locked("Put the field on him.",
                                 "The emitter is empty, or she is carrying the drain instead.",
                                 [_trait("equipped_weapon", 2, operator="eq")])])
    assert "carrying the drain instead.<<= setup.requirementSuffix(" not in twee
    assert "Equipped_weapon" not in twee


def test_a_mixed_gate_names_only_the_threshold(build):
    """The emitter rung in the wild carries both shapes. The number is worth saying;
    the loadout check is not."""
    twee = build([PLAIN, _locked("Put the field on him.", "Not with what she is carrying.",
                                 [_trait("equipped_weapon", 2, operator="eq"),
                                  _trait("stealth", 30)])])
    assert "Not with what she is carrying.<<= setup.requirementSuffix(" in twee
    body = _fn_body(twee, "describeUnmetTraits")
    assert "REQUIREMENT_OPS" in body, "the operator filter must be the helper's, not the emitter's alone"


def test_a_boolean_worn_as_a_trait_gets_no_suffix(build):
    """The second leak the live audit found, after the loadout enum. `bottle_held gte 1`
    is a bottle in her coat; `bunker_stealth_used lt 1` is the one quiet pass, unspent;
    `emitter_broken lt 1` is the weapon, working. None is a number she can train, and
    naming one puts an internal key on a greyed tile. Measured across vesper's 36 locked
    trait gates the split is exact — under 2 is always possession or run-state, 2 or more
    is always a meter."""
    twee = build([PLAIN, _locked("Drink with him.", "He pours his own.",
                                 [_trait("bottle_held", 1)])])
    assert "He pours his own.<<= setup.requirementSuffix(" not in twee
    assert "Bottle_held" not in twee


def test_a_meter_threshold_still_gets_its_suffix(build):
    twee = build([PLAIN, _locked("Slip past.", "Not that quiet.", [_trait("stealth", 2)])])
    assert "Not that quiet.<<= setup.requirementSuffix(" in twee, (
        "2 is the floor, not an exclusion — the rule must not swallow a real low gate"
    )


def test_the_trait_label_loses_its_underscores(build):
    """These strings are read by the player now, not only by a shopper. the_balance gates
    on `crowd_standing` and orientation on `nerve`; one of those should not render with a
    key's punctuation in it. The flag branch has always done this."""
    body = _fn_body(build([PLAIN]), "describeUnmetConditions")
    assert "replace(/_/g, ' ')" in body.split("} else if (it.type === 'flag')")[0], (
        "the TRAIT branch must strip underscores, not just the flag branch"
    )


# ── 3. it does not disturb what already worked ───────────────────────────────

def test_the_cost_rung_is_untouched(build):
    twee = build([
        {"text": "Work a shift", "targetType": "trigger", "effects": [],
         "costs": [{"trait": "energy", "value": 15}]},
    ])
    assert "Work a shift (<<= setup.getCostBlockedMessage(" in twee, (
        "the cost rung keeps its own shape; this change is the CONDITION tier only"
    )


def test_a_clock_gated_choice_appends_nothing_visible(build):
    """`time_of_day` has no phrasing in describeUnmetConditions (a known gap), so the
    helper returns "" and the bracket never opens. Better a silent suffix than
    'Requires: ' with nothing after it."""
    twee = build([PLAIN, _locked("Down.", "Two of them on the slab.",
                                 [{"type": "time_of_day", "start_time": "00:00",
                                   "end_time": "20:00"}])])
    assert "Two of them on the slab.<<= setup.requirementSuffix(" not in twee
