"""A canvas could ask what she is wearing but never what time it is.

Measured 2026-08-29 across 27 shipped sandbox games (`~/Documents/Phone_System_Study_20260829/`):
gating content on an hour window is the field's **second most common** mechanism — 20 of the 27
games do it, behind only a meter gate at 22 — and it was the one thing in that list this engine
could not express at all. The complete condition-type family before this change:

    clothing_item  clothing_slot  corruption_level  days_since_flag  flag  item  modifier
    npc_at_location  pass  quest  stage  trait  worn_beauty  worn_corruption
    worn_exposure  worn_type

Nothing there reaches the clock. Locations and NPCs get hour windows through the SCHEDULE
primitive, but a phone conversation is not scheduled and a canvas trigger is not either, so
"only in the evening" had to be faked by setting a flag from something that does touch the
clock and gating on the flag.

⚠️ The overnight wrap is the trap this feature must not re-introduce. `setup.isCurrentTimeSlot`
has handled 22:00–06:00 correctly since the schedule primitive shipped, so the predicate
DELEGATES to it rather than parsing hours a second time — there is no second implementation to
drift from the first. These tests pin that delegation, because a copy would pass every daytime
case and silently fail every overnight one.

    pytest apps/game_generation/tests/test_time_of_day.py -q
"""
from pathlib import Path

import pytest

V2 = Path("apps/game_generation/twee_comprehensive/generators/v2.py").read_text(
    encoding="utf-8"
)


def branch_body():
    """Just the time_of_day branch, cut at its own `continue;`.

    A fixed-width slice runs on into the worn_beauty branch below it, which IS guarded
    on clothing_enabled — so a naive window makes the no-guard test fail on its
    neighbour's code rather than on its own.
    """
    after = V2.split("type === 'time_of_day'")[1]
    return after[: after.index("continue;") + len("continue;")]


# --- the predicate exists and delegates -----------------------------------------


def test_predicate_reaches_the_evaluator():
    ev = V2.split("setup.triggerConditionsSatisfied = function(conditions)")[1][:14000]
    assert "type === 'time_of_day'" in ev


def test_predicate_delegates_to_the_one_wrap_implementation():
    """The whole point. A second hour parse would pass every daytime window and fail
    every overnight one, which is exactly the class of bug that ships unnoticed."""
    branch = branch_body()
    assert "setup.isCurrentTimeSlot" in branch
    # and it must NOT be doing its own arithmetic
    assert "split(':')" not in branch, "parsing hours here duplicates the wrap"
    assert "* 60" not in branch, "computing minutes here duplicates the wrap"


def test_the_wrap_it_delegates_to_still_handles_overnight():
    """Regression guard on the borrowed behaviour, not on our own code. If someone
    simplifies isCurrentTimeSlot, this predicate breaks with it and should say so."""
    fn = V2.split("setup.isCurrentTimeSlot = function(startTime, endTime)")[1][:900]
    assert "endTotal < startTotal" in fn, "the overnight branch is gone"
    assert "currentTotal >= startTotal || currentTotal < endTotal" in fn


def test_omitted_end_time_falls_through_to_the_one_hour_default():
    """`isCurrentTimeSlot` treats a missing end as start + 60. The predicate must pass
    null rather than inventing an end of its own."""
    branch = branch_body()
    assert "it.end_time || null" in branch
    fn = V2.split("setup.isCurrentTimeSlot = function(startTime, endTime)")[1][:900]
    assert "startTotal + 60" in fn


# --- a locked door says why -----------------------------------------------------


def test_predicate_reaches_the_requirement_text():
    fm = V2.split("setup.formatCanvasConditions = function(conditions)")[1][:14000]
    assert 'item.type === "time_of_day"' in fm


def test_requirement_text_names_both_ends_of_the_window():
    fm = V2.split('item.type === "time_of_day"')[1][:600]
    assert (
        "Only between" in fm and "Only at" in fm
    ), "a window and a single hour read differently and must print differently"


# --- it is a window, not a latch ------------------------------------------------


def test_the_predicate_is_not_guarded_on_any_optional_system():
    """Unlike every worn_* predicate, this one has no `_enabled` guard to short-circuit
    on, because the clock exists in every build. If a guard appears here it is a bug:
    it would silently fail every game that did not opt into some unrelated system."""
    branch = branch_body()
    assert "_enabled" not in branch


def test_the_clock_it_reads_is_initialised_in_every_build():
    """time_state is written into $game_state unconditionally, so the predicate cannot
    throw in a build that has no schedules, no phone and no clothing.

    Asserted against a BUILT game rather than against v2.py's source. The source
    anchor this used to grep (`"time_state": {{` inside the :: Start f-string) was
    dissolved when the state skeleton became a Python dict — see
    test_save_migration.py. The behaviour never changed, only where it is written,
    and a test that reads the output cannot be broken again by that class of move."""
    from apps.game_generation.twee_comprehensive.generators.v2 import (
        TweeComprehensiveGeneratorV2,
    )
    from apps.projects.services.game_graph import build_game_graph
    from apps.projects.services.template_import import normalize, parse_toml

    fixture = "apps/game_generation/games_toml_files/engine_prd_phase2_2026_04_29.toml"
    graph = build_game_graph(normalize(parse_toml(fixture)))
    twee = TweeComprehensiveGeneratorV2().generate(graph.project, {}, graph=graph)
    init = twee.split(":: Start")[1].split('"time_state"')[1][:300]
    assert "current_hour" in init and "current_minute" in init


# --- the seam this engine has bitten us on before -------------------------------


@pytest.mark.parametrize("other", ["describeUnmetConditions", "_renderGoalGate"])
def test_known_gap_is_unchanged(other):
    """⚠️ NOT a bug this feature introduced. These two display helpers already handle no
    `worn_*` predicate; they handle no `time_of_day` either. Pinned so that whoever
    teaches them one predicate teaches them the set."""
    body = V2.split(f"setup.{other} = function")[1][:9000]
    assert "time_of_day" not in body
    assert "worn_exposure" not in body


def test_phone_triggers_run_through_the_same_evaluator():
    """The reason this feature lands on the phone for free: conversations, posts and
    profiles are all evaluated by triggerConditionsSatisfied, so the predicate reaches
    them without a line of phone-specific code. `the-phone.md` P4."""
    assert "setup.checkPhoneConversations = function()" in V2
    scan = V2.split("setup.checkPhoneConversations = function()")[1][:3000]
    assert (
        scan.count("setup.triggerConditionsSatisfied") == 3
    ), "conversations, posts and profiles should each consult the shared evaluator"
