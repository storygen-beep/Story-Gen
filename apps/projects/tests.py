"""
Tests for template_import schema + validation.

Covers the Engine PRD 2026-04-22 additions:
  F1 — trait_words sidebar type
  F2 — entry_conditions enforced regardless of clothing_enabled
  F3 — player.trait_decay
  F4 — rent eviction_mode / eviction_flag

Schema tests (SimpleTestCase — no DB) exercise normalize() and validate() on
in-memory dicts. The EnginePRDIntegrationTests class (TransactionTestCase)
runs the full pipeline on a fixture TOML and asserts the generator emits
the expected Twee.
"""

import copy
from pathlib import Path

import tomli
from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase

from apps.projects.models import Project
from apps.projects.services.template_import import (
    create_project_from_template,
    normalize,
    validate,
)


def _base_toml():
    """Minimal valid TOML-shaped dict with a player trait and one NPC."""
    return {
        "schema_version": "0.2",
        "project": {
            "id": "test_proj",
            "title": "Test Project",
            "description": "Unit-test fixture.",
        },
        "player": {
            "id": "player",
            "name": "Maya",
            "core_traits": {"hygiene": 100, "energy": 100, "awareness": 0},
            "flag_keys": [],
        },
        "npcs": [
            {
                "id": "npc_frank",
                "name": "Frank",
                "core_traits": {"trust": 0, "arousal": 0},
                "flag_keys": [],
            }
        ],
    }


# -- F1: trait_words sidebar type --------------------------------------------


class TraitWordsSidebarTests(SimpleTestCase):
    def _with_sidebar(self, item):
        d = _base_toml()
        d["sidebar_items"] = [item]
        return d

    def test_player_trait_words_valid(self):
        item = {
            "type": "trait_words",
            "trait_owner": "player",
            "trait": "awareness",
            "bands": [
                {"min": 0, "max": 9, "text": "You keep your eyes down."},
                {"min": 10, "max": 49, "text": "Sometimes you notice."},
                {"min": 50, "max": 100, "text": "You know who's watching."},
            ],
        }
        template = normalize(self._with_sidebar(item))
        errors = validate(template)
        self.assertEqual(errors, [], f"Unexpected errors: {errors}")

    def test_npc_trait_words_valid(self):
        item = {
            "type": "trait_words",
            "trait_owner": "npc",
            "npc_id": "npc_frank",
            "trait": "trust",
            "bands": [{"min": 0, "max": 100, "text": "He nods when you walk in."}],
        }
        template = normalize(self._with_sidebar(item))
        errors = validate(template)
        self.assertEqual(errors, [], f"Unexpected errors: {errors}")

    def test_missing_bands_fails(self):
        item = {"type": "trait_words", "trait_owner": "player", "trait": "awareness"}
        template = normalize(self._with_sidebar(item))
        errors = validate(template)
        self.assertTrue(any("'bands' must be a non-empty list" in e for e in errors), errors)

    def test_missing_trait_fails(self):
        item = {
            "type": "trait_words",
            "trait_owner": "player",
            "bands": [{"min": 0, "max": 10, "text": "x"}],
        }
        template = normalize(self._with_sidebar(item))
        errors = validate(template)
        self.assertTrue(any("'trait' is required" in e for e in errors), errors)

    def test_invalid_trait_owner_fails(self):
        item = {
            "type": "trait_words",
            "trait_owner": "mayor",
            "trait": "awareness",
            "bands": [{"min": 0, "max": 10, "text": "x"}],
        }
        template = normalize(self._with_sidebar(item))
        errors = validate(template)
        self.assertTrue(any("trait_owner" in e and "mayor" in e for e in errors), errors)

    def test_npc_owner_missing_npc_id_fails(self):
        item = {
            "type": "trait_words",
            "trait_owner": "npc",
            "trait": "trust",
            "bands": [{"min": 0, "max": 10, "text": "x"}],
        }
        template = normalize(self._with_sidebar(item))
        errors = validate(template)
        self.assertTrue(any("'npc_id' is required" in e for e in errors), errors)

    def test_npc_owner_unknown_npc_id_fails(self):
        item = {
            "type": "trait_words",
            "trait_owner": "npc",
            "npc_id": "npc_ghost",
            "trait": "trust",
            "bands": [{"min": 0, "max": 10, "text": "x"}],
        }
        template = normalize(self._with_sidebar(item))
        errors = validate(template)
        self.assertTrue(any("'npc_ghost' not found" in e for e in errors), errors)

    def test_player_owner_unknown_trait_fails(self):
        item = {
            "type": "trait_words",
            "trait_owner": "player",
            "trait": "magnetism",
            "bands": [{"min": 0, "max": 10, "text": "x"}],
        }
        template = normalize(self._with_sidebar(item))
        errors = validate(template)
        self.assertTrue(
            any("'magnetism' not found in player.core_traits" in e for e in errors), errors
        )

    def test_band_min_greater_than_max_fails(self):
        item = {
            "type": "trait_words",
            "trait_owner": "player",
            "trait": "awareness",
            "bands": [{"min": 50, "max": 10, "text": "bad"}],
        }
        template = normalize(self._with_sidebar(item))
        errors = validate(template)
        self.assertTrue(any("min (50)" in e and "max (10)" in e for e in errors), errors)

    def test_band_missing_text_fails(self):
        item = {
            "type": "trait_words",
            "trait_owner": "player",
            "trait": "awareness",
            "bands": [{"min": 0, "max": 10}],
        }
        template = normalize(self._with_sidebar(item))
        errors = validate(template)
        self.assertTrue(any("missing 'text'" in e for e in errors), errors)

    def test_absent_sidebar_items_no_errors(self):
        template = normalize(_base_toml())
        errors = validate(template)
        self.assertEqual(errors, [], f"Baseline should validate cleanly: {errors}")

    def test_non_trait_words_types_untouched(self):
        d = _base_toml()
        d["sidebar_items"] = [
            {"type": "trait_bar", "trait": "hygiene", "max": 100, "label": "Hygiene"},
            {"type": "countdown", "total_days": 14, "label": "days until summer"},
        ]
        template = normalize(d)
        errors = validate(template)
        self.assertEqual(errors, [], errors)


# -- F3: player.trait_decay --------------------------------------------------


class PlayerTraitDecayTests(SimpleTestCase):
    def test_valid_player_trait_decay_parses(self):
        d = _base_toml()
        d["player"]["trait_decay"] = {"hygiene": 3}
        template = normalize(d)
        self.assertEqual(template.player.trait_decay, {"hygiene": 3.0})
        self.assertEqual(validate(template), [])

    def test_trait_decay_on_unknown_trait_fails_validation(self):
        d = _base_toml()
        d["player"]["trait_decay"] = {"charisma": 2}
        template = normalize(d)
        errors = validate(template)
        self.assertTrue(
            any("player.trait_decay key 'charisma' not found" in e for e in errors), errors
        )

    def test_negative_decay_fails_validation(self):
        d = _base_toml()
        d["player"]["trait_decay"] = {"hygiene": -1}
        template = normalize(d)
        errors = validate(template)
        self.assertTrue(
            any("player.trait_decay['hygiene'] must be >= 0" in e for e in errors), errors
        )

    def test_non_numeric_decay_raises_type_error(self):
        d = _base_toml()
        d["player"]["trait_decay"] = {"hygiene": "three"}
        with self.assertRaises(TypeError) as cm:
            normalize(d)
        self.assertIn("player.trait_decay['hygiene']", str(cm.exception))

    def test_empty_trait_decay_noop(self):
        template = normalize(_base_toml())
        self.assertEqual(template.player.trait_decay, {})
        self.assertEqual(validate(template), [])


# -- F4: rent eviction_mode --------------------------------------------------


class RentEvictionModeTests(SimpleTestCase):
    def _with_rent(self, **rent_overrides):
        d = _base_toml()
        rent = {
            "enabled": True,
            "amount": 150,
            "due_day": "Monday",
            "collector_npc": "npc_frank",
            "grace_periods": 2,
        }
        rent.update(rent_overrides)
        d["settings"] = {"rent": rent}
        return d

    def test_default_eviction_mode_is_game_end(self):
        template = normalize(self._with_rent())
        self.assertEqual(template.rent_eviction_mode, "game_end")
        self.assertEqual(template.rent_eviction_flag, "rent_evicted")
        self.assertEqual(validate(template), [])

    def test_flag_set_mode_valid(self):
        template = normalize(
            self._with_rent(eviction_mode="flag_set", eviction_flag="rent_evicted")
        )
        self.assertEqual(template.rent_eviction_mode, "flag_set")
        self.assertEqual(validate(template), [])

    def test_invalid_eviction_mode_fails(self):
        template = normalize(self._with_rent(eviction_mode="purgatory"))
        errors = validate(template)
        self.assertTrue(
            any(
                "eviction_mode must be 'game_end' or 'flag_set'" in e
                and "purgatory" in e
                for e in errors
            ),
            errors,
        )

    def test_flag_set_with_bad_flag_name_fails(self):
        template = normalize(
            self._with_rent(eviction_mode="flag_set", eviction_flag="Rent Evicted!")
        )
        errors = validate(template)
        self.assertTrue(
            any("eviction_flag must be lowercase snake_case" in e for e in errors), errors
        )

    def test_rent_disabled_ignores_eviction_mode(self):
        d = _base_toml()
        d["settings"] = {"rent": {"enabled": False, "eviction_mode": "nonsense"}}
        template = normalize(d)
        # rent.enabled=false → validate() doesn't enter the rent branch.
        self.assertEqual(validate(template), [])

    def test_template_carries_eviction_fields(self):
        template = normalize(
            self._with_rent(eviction_mode="flag_set", eviction_flag="forced_deal")
        )
        self.assertEqual(validate(template), [])
        self.assertEqual(template.rent_eviction_mode, "flag_set")
        self.assertEqual(template.rent_eviction_flag, "forced_deal")


# -- Integration: fixture TOML → generator → Twee substring assertions -------


FIXTURE_PATH = (
    Path(__file__).resolve().parent.parent
    / "game_generation"
    / "games_toml_files"
    / "engine_prd_2026_04_22.toml"
)


class EnginePRDIntegrationTests(TestCase):
    """Full-pipeline test: fixture TOML → DB rows → generator → Twee string.

    Each test calls self._build() which runs the pipeline once and returns
    (project, twee). Assertions check that feature-specific substrings land
    in the emitted Twee.
    """

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            email="engine-prd-test@example.com", password="testpass123"
        )
        with open(FIXTURE_PATH, "rb") as f:
            cls.toml_data = tomli.load(f)

    def _build(self):
        """Run the full pipeline once and return (project, twee_string).

        normalize() mutates its input (strips parsed-out subtables, reassigns
        nested lists, etc.), and the fixture dict is loaded once per class.
        Deep-copy so tests are independent.
        """
        template = normalize(copy.deepcopy(self.toml_data))
        errors = validate(template)
        self.assertEqual(errors, [], f"Fixture should validate clean: {errors}")

        result = create_project_from_template(template, str(self.user.id))
        project = Project.objects.get(id=result["project_id"])

        # Lazy-import the generator — it pulls in a lot of Django infra.
        from apps.game_generation.twee_comprehensive.generators.v1 import (
            TweeComprehensiveGeneratorV1,
        )

        generator = TweeComprehensiveGeneratorV1()
        twee = generator.generate(project)
        self.assertIsInstance(twee, str)
        self.assertGreater(len(twee), 1000, "Generated Twee suspiciously short")
        return project, twee

    # --- F1: trait_words --------------------------------------------------

    def test_f1_trait_words_branch_exists_in_sidebar_widget(self):
        _, twee = self._build()
        self.assertIn(
            '<<elseif _item.type is "trait_words">>',
            twee,
            "Sidebar widget missing trait_words branch",
        )

    def test_f1_trait_words_bands_serialized_into_setup(self):
        _, twee = self._build()
        # setup.sidebar_items is JSON-serialized. Our player-awareness band
        # text and Frank-trust band text must both appear in it.
        self.assertIn("You catch men watching you more often now.", twee)
        self.assertIn("Frank nods when you walk in.", twee)

    def test_f1_npc_owned_trait_words_includes_npc_id(self):
        _, twee = self._build()
        # The sidebar_items JSON must include trait_owner="npc" + npc_id.
        self.assertIn('"trait_owner": "npc"', twee)
        self.assertIn('"npc_id": "npc_frank"', twee)

    # --- F2: entry_conditions without clothing ----------------------------

    def test_f2_gated_location_emits_condition_check(self):
        _, twee = self._build()
        # Pre-PRD, this passage would have been emitted without any condition
        # check because clothing_enabled is false in the fixture. Post-PRD,
        # the passage must wrap content in triggerConditionsSatisfied().
        # Location passages are named `:: Location_<name>` where <name> is
        # location.name with spaces → underscores.
        self.assertIn(":: Location_Prologue_Café", twee)
        idx = twee.index(":: Location_Prologue_Café")
        passage = twee[idx : idx + 2000]
        self.assertIn("setup.triggerConditionsSatisfied(", passage)
        self.assertIn("summer_started", passage)

    def test_f2_non_gated_location_has_no_condition_check(self):
        _, twee = self._build()
        # loc_town_square has no entry_conditions. Its passage must NOT
        # wrap content in triggerConditionsSatisfied (regression against
        # accidentally applying the gate too broadly).
        self.assertIn(":: Location_Town_Square", twee)
        start = twee.index(":: Location_Town_Square")
        rest = twee[start + 1 :]
        next_header = rest.find("\n:: ")
        passage = rest[:next_header] if next_header != -1 else rest
        self.assertNotIn("setup.triggerConditionsSatisfied(", passage)

    # --- F3: player.trait_decay ------------------------------------------

    def test_f3_setup_player_trait_decay_emitted(self):
        _, twee = self._build()
        # The generator serializes self.player_trait_decay_config as a JSON
        # object. hygiene=3 must land in setup.player_trait_decay.
        self.assertIn("setup.player_trait_decay = ", twee)
        self.assertIn('"hygiene": 3', twee)

    def test_f3_advance_day_contains_player_decay_loop(self):
        _, twee = self._build()
        # The runtime decay loop in window.advanceDay() must be emitted.
        self.assertIn(
            "if (setup.player_trait_decay && Object.keys(setup.player_trait_decay).length > 0)",
            twee,
        )

    # --- F4: rent eviction_mode = "flag_set" -----------------------------

    def test_f4_eviction_mode_emitted_to_setup(self):
        _, twee = self._build()
        self.assertIn('setup.rent_eviction_mode = "flag_set";', twee)
        self.assertIn('setup.rent_eviction_flag = "rent_evicted";', twee)

    def test_f4_rentday_short_branches_on_eviction_mode(self):
        _, twee = self._build()
        self.assertIn(":: RentDay_Short", twee)
        idx = twee.index(":: RentDay_Short")
        passage = twee[idx : idx + 4000]
        # The fail-forward branch sets the flag and continues.
        self.assertIn('<<if setup.rent_eviction_mode is "flag_set">>', passage)
        self.assertIn("$player.flags[setup.rent_eviction_flag]", passage)
        # The hard-eviction branch is still present for game_end mode.
        self.assertIn("Engine.restart()", passage)

    def test_f4_eviction_flag_registered_on_player(self):
        project, _ = self._build()
        # Auto-registration: "rent_evicted" must be added to player.flag_keys
        # during template_import (author didn't declare it in the TOML).
        player = project.player_character
        self.assertIn("rent_evicted", player.flag_keys)
        # The author-declared flag must still be present.
        self.assertIn("summer_started", player.flag_keys)

    # --- Sanity: baseline shape of generated game ------------------------

    def test_baseline_generator_emits_start_passage(self):
        _, twee = self._build()
        self.assertIn(":: Start", twee)
        # The starting canvas id must end up as a passage.
        self.assertIn("scene_wake_up", twee)


# ═══════════════════════════════════════════════════════════════════════════
#  Engine PRD 2026-04-28 Batch 1
#  E1: flagEffects op field (set | unset | toggle)
#  E5: [engine.daily_tick] hook
# ═══════════════════════════════════════════════════════════════════════════


def _toml_with_choice_flag_effect(op=None, flag="test_flag"):
    """Minimal TOML with one canvas → one node → one choice → one flagEffect.

    If `op` is None, the flagEffect dict has no 'op' key (back-compat path).
    If `op` is set, it's added to the flagEffect dict.
    """
    d = _base_toml()
    d["player"]["flag_keys"] = [flag]
    fe = {"targetType": "player", "flag": flag}
    if op is not None:
        fe["op"] = op
    d["starting_canvas"] = "test_canvas"
    d["canvases"] = [
        {
            "id": "test_canvas",
            "name": "Test Canvas",
            "description": "x",
            "nodes": [
                {
                    "id": "n1",
                    "name": "Node 1",
                    "blocks": [{"type": "paragraph", "content": "x"}],
                    "exit_block": {
                        "type": "choices",
                        "choices": [
                            {
                                "text": "Continue",
                                "targetType": "trigger",
                                "flagEffects": [fe],
                            }
                        ],
                    },
                }
            ],
        }
    ]
    return d


# -- E1: schema parse of flagEffect.op ---------------------------------------


class FlagEffectOpSchemaTests(SimpleTestCase):
    def _first_choice_flag_effect(self, template):
        return template.canvases[0].nodes[0].exit_block.choices[0].flagEffects[0]

    def test_default_op_is_set(self):
        template = normalize(_toml_with_choice_flag_effect(op=None))
        self.assertEqual(self._first_choice_flag_effect(template).op, "set")

    def test_op_unset_parses(self):
        template = normalize(_toml_with_choice_flag_effect(op="unset"))
        self.assertEqual(self._first_choice_flag_effect(template).op, "unset")

    def test_op_toggle_parses(self):
        template = normalize(_toml_with_choice_flag_effect(op="toggle"))
        self.assertEqual(self._first_choice_flag_effect(template).op, "toggle")


# -- E5: schema parse of [engine.daily_tick] ---------------------------------


def _toml_with_daily_tick(flag_effects):
    d = _base_toml()
    flat_keys = []
    for fe in flag_effects:
        if fe.get("targetType", "player") == "player" and fe.get("flag"):
            flat_keys.append(fe["flag"])
    d["player"]["flag_keys"] = list(set(d["player"].get("flag_keys", []) + flat_keys))
    d["engine"] = {"daily_tick": {"flagEffects": flag_effects}}
    return d


class DailyTickSchemaTests(SimpleTestCase):
    def test_absent_daily_tick_is_none(self):
        template = normalize(_base_toml())
        self.assertIsNone(getattr(template, "daily_tick", None))

    def test_daily_tick_parses_with_unset_op(self):
        template = normalize(
            _toml_with_daily_tick(
                [
                    {"targetType": "player", "flag": "talked_to_frank_today", "op": "unset"},
                    {"targetType": "player", "flag": "watched_ryan_today", "op": "unset"},
                ]
            )
        )
        self.assertIsNotNone(template.daily_tick)
        self.assertEqual(len(template.daily_tick.flagEffects), 2)
        self.assertEqual(
            [(fe.flag, fe.op) for fe in template.daily_tick.flagEffects],
            [("talked_to_frank_today", "unset"), ("watched_ryan_today", "unset")],
        )

    def test_daily_tick_with_no_flag_effects_is_empty(self):
        template = normalize(_toml_with_daily_tick([]))
        # Dict was present but empty → daily_tick exists with no effects.
        self.assertIsNotNone(template.daily_tick)
        self.assertEqual(template.daily_tick.flagEffects, [])


# -- E1 + E5: integration via the full pipeline ------------------------------


class FlagOpAndDailyTickIntegrationTests(TestCase):
    """Full-pipeline tests for E1 + E5. Build the existing fixture once,
    optionally mutated, and grep the generated Twee.
    """

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            email="batch1-test@example.com", password="testpass123"
        )
        with open(FIXTURE_PATH, "rb") as f:
            cls.toml_data = tomli.load(f)

    def _build(self, mutator=None):
        toml_data = copy.deepcopy(self.toml_data)
        if mutator is not None:
            mutator(toml_data)
        template = normalize(toml_data)
        errors = validate(template)
        self.assertEqual(errors, [], f"Fixture should validate clean: {errors}")
        result = create_project_from_template(template, str(self.user.id))
        project = Project.objects.get(id=result["project_id"])
        from apps.game_generation.twee_comprehensive.generators.v1 import (
            TweeComprehensiveGeneratorV1,
        )
        generator = TweeComprehensiveGeneratorV1()
        twee = generator.generate(project)
        self.assertIsInstance(twee, str)
        return project, twee

    # --- E1 runtime function signature + branching ----------------------

    def test_e1_apply_flag_effect_signature_has_op_param(self):
        _, twee = self._build()
        self.assertIn(
            "window.applyFlagEffect = function(targetType, npcId, flag, op)",
            twee,
        )

    def test_e1_apply_flag_effect_has_unset_branch(self):
        _, twee = self._build()
        self.assertIn("'unset'", twee)
        # The unset branch must assign false (not delete-from-dict, per
        # 2026-04-29 design decision).
        self.assertRegex(twee, r"op\s*===?\s*['\"]unset['\"]")

    def test_e1_apply_flag_effect_has_toggle_branch(self):
        _, twee = self._build()
        self.assertRegex(twee, r"op\s*===?\s*['\"]toggle['\"]")

    def test_e1_apply_and_notify_flag_signature_has_op_param(self):
        _, twee = self._build()
        self.assertIn(
            "setup.applyAndNotifyFlag = function(targetType, npcId, flag, op)",
            twee,
        )

    # --- E1 emit-site threading -----------------------------------------

    def test_e1_default_emit_passes_set_op_arg(self):
        """The fixture's location-config flagEffect has no `op` field —
        the generated twee should pass "set" as the 4th arg."""
        _, twee = self._build()
        # `_get_flag_effects_for_node` (v1.py:9060 path) emits the call.
        # The fixture's exit_block is a 'location' type with summer_started.
        self.assertRegex(
            twee,
            r'setup\.applyAndNotifyFlag\(\s*"player"\s*,\s*null\s*,\s*"summer_started"\s*,\s*"set"\s*\)',
        )

    def test_e1_unset_op_threads_to_emit(self):
        """Mutate the fixture so the location-config flagEffect declares
        op = 'unset'; the generated twee should emit "unset" as 4th arg."""

        def mutate(d):
            # The fixture has exit_block on canvases[0].nodes[0]
            fe = d["canvases"][0]["nodes"][0]["exit_block"]["config"]["flagEffects"][0]
            fe["op"] = "unset"

        _, twee = self._build(mutator=mutate)
        self.assertRegex(
            twee,
            r'setup\.applyAndNotifyFlag\(\s*"player"\s*,\s*null\s*,\s*"summer_started"\s*,\s*"unset"\s*\)',
        )

    # --- E5 daily_tick emission + hook ----------------------------------

    def test_e5_setup_daily_tick_absent_when_unset(self):
        """Baseline fixture has no [engine.daily_tick]; setup.daily_tick
        should still be defined (as a sentinel) so JS doesn't NPE — but
        with empty flagEffects."""
        _, twee = self._build()
        # Either undefined-guard or empty struct — accept either pattern.
        # We commit to: always emit `setup.daily_tick = {...}` with empty
        # flagEffects when no config provided.
        self.assertIn("setup.daily_tick = ", twee)

    def test_e5_setup_daily_tick_with_flag_effects(self):
        def mutate(d):
            d["player"]["flag_keys"] = list(d["player"].get("flag_keys", [])) + [
                "talked_to_frank_today"
            ]
            d["engine"] = {
                "daily_tick": {
                    "flagEffects": [
                        {
                            "targetType": "player",
                            "flag": "talked_to_frank_today",
                            "op": "unset",
                        }
                    ]
                }
            }

        _, twee = self._build(mutator=mutate)
        self.assertIn("setup.daily_tick = ", twee)
        self.assertIn("talked_to_frank_today", twee)

    def test_e5_advance_day_loops_over_daily_tick(self):
        """The advanceDay() body must contain a loop that consumes
        setup.daily_tick.flagEffects and calls window.applyFlagEffect.
        Fires regardless of whether the user provided a config — empty
        config means the loop body just iterates 0 times."""
        _, twee = self._build()
        # The loop is keyed off `setup.daily_tick`.
        self.assertIn("setup.daily_tick", twee)
        # Slice the advanceDay body: from its definition to the next
        # top-level `window.X = function()` (which is updateTimeDisplay).
        idx = twee.index("window.advanceDay = function()")
        end = twee.find("window.updateTimeDisplay", idx + 1)
        body = twee[idx:end] if end != -1 else twee[idx:]
        self.assertIn("setup.daily_tick", body)
        self.assertIn("applyFlagEffect", body)


# ═══════════════════════════════════════════════════════════════════════════
#  Engine PRD 2026-04-28 Batch 2
#  E7: counter increment shorthand + <<inc>>/<<dec>> widgets
#  E6: per-choice text_variants
#  E4: stage_helpers (named composite gates)
# ═══════════════════════════════════════════════════════════════════════════


def _toml_with_choice_inc(inc=None):
    """Minimal TOML with one canvas → one node → one choice → optional inc."""
    d = _base_toml()
    d["player"]["core_traits"]["lean_count"] = 0
    d["starting_canvas"] = "test_canvas"
    choice = {
        "text": "Lean by the desk.",
        "targetType": "trigger",
    }
    if inc is not None:
        choice["inc"] = inc
    d["canvases"] = [
        {
            "id": "test_canvas",
            "name": "Test",
            "description": "x",
            "nodes": [
                {
                    "id": "n1",
                    "name": "N1",
                    "blocks": [{"type": "paragraph", "content": "x"}],
                    "exit_block": {
                        "type": "choices",
                        "choices": [choice],
                    },
                }
            ],
        }
    ]
    return d


# -- E7: schema + parse-time expansion of `inc` ------------------------------


class IncShorthandSchemaTests(SimpleTestCase):
    def _first_choice(self, template):
        return template.canvases[0].nodes[0].exit_block.choices[0]

    def test_default_inc_is_empty(self):
        template = normalize(_toml_with_choice_inc(inc=None))
        ch = self._first_choice(template)
        # No effects expanded from inc; effects list should be empty.
        self.assertEqual(ch.effects, [])

    def test_inc_string_form_expands_to_add_one(self):
        template = normalize(_toml_with_choice_inc(inc=["lean_count"]))
        ch = self._first_choice(template)
        self.assertEqual(len(ch.effects), 1)
        eff = ch.effects[0]
        self.assertEqual(eff.targetType, "player")
        self.assertEqual(eff.trait, "lean_count")
        self.assertEqual(eff.op, "add")
        self.assertEqual(eff.value, 1)

    def test_inc_dict_form_expands_with_explicit_step(self):
        template = normalize(
            _toml_with_choice_inc(inc=[{"counter": "lean_count", "by": 3}])
        )
        ch = self._first_choice(template)
        self.assertEqual(len(ch.effects), 1)
        self.assertEqual(ch.effects[0].value, 3)

    def test_inc_coexists_with_explicit_effects(self):
        d = _toml_with_choice_inc(inc=["lean_count"])
        d["canvases"][0]["nodes"][0]["exit_block"]["choices"][0]["effects"] = [
            {
                "targetType": "player",
                "trait": "energy",
                "op": "add",
                "value": -5,
            }
        ]
        template = normalize(d)
        ch = self._first_choice(template)
        self.assertEqual(len(ch.effects), 2)
        traits = sorted(e.trait for e in ch.effects)
        self.assertEqual(traits, ["energy", "lean_count"])


# -- E7 integration: widgets + emit -----------------------------------------


class IncWidgetIntegrationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            email="batch2-e7-test@example.com", password="testpass123"
        )
        with open(FIXTURE_PATH, "rb") as f:
            cls.toml_data = tomli.load(f)

    def _build(self, mutator=None):
        toml_data = copy.deepcopy(self.toml_data)
        if mutator is not None:
            mutator(toml_data)
        template = normalize(toml_data)
        errors = validate(template)
        self.assertEqual(errors, [], f"Should validate clean: {errors}")
        result = create_project_from_template(template, str(self.user.id))
        project = Project.objects.get(id=result["project_id"])
        from apps.game_generation.twee_comprehensive.generators.v1 import (
            TweeComprehensiveGeneratorV1,
        )
        twee = TweeComprehensiveGeneratorV1().generate(project)
        return project, twee

    def test_e7_inc_widget_is_emitted(self):
        _, twee = self._build()
        self.assertIn('<<widget "inc">>', twee)
        # The widget must call applyAndNotifyTrait with op=add.
        idx = twee.index('<<widget "inc">>')
        widget = twee[idx : idx + 500]
        self.assertIn("applyAndNotifyTrait", widget)
        self.assertIn('"add"', widget)

    def test_e7_dec_widget_is_emitted(self):
        _, twee = self._build()
        self.assertIn('<<widget "dec">>', twee)
        idx = twee.index('<<widget "dec">>')
        widget = twee[idx : idx + 500]
        self.assertIn("applyAndNotifyTrait", widget)

    def test_e7_inc_shorthand_emits_trait_effect_call(self):
        """A choice with `inc = ["counter_x"]` should produce a passage
        body containing setup.applyAndNotifyTrait(..., "counter_x", "add", 1.0, ...)."""

        # Inject an `inc` shorthand into the fixture's exit_block as a
        # choices-type variant, since the fixture uses location-type by default.
        # We inject a brand-new canvas with a choice using `inc`.
        def mutate(d):
            d["player"]["core_traits"]["lean_count"] = 0
            d["canvases"].append(
                {
                    "id": "inc_test_canvas",
                    "name": "Inc Test",
                    "description": "x",
                    "trigger": {"location": "loc_home"},
                    "nodes": [
                        {
                            "id": "n1",
                            "name": "N1",
                            "blocks": [{"type": "paragraph", "content": "x"}],
                            "exit_block": {
                                "type": "choices",
                                "choices": [
                                    {
                                        "text": "Lean.",
                                        "targetType": "trigger",
                                        "inc": ["lean_count"],
                                    }
                                ],
                            },
                        }
                    ],
                }
            )

        _, twee = self._build(mutator=mutate)
        # The expanded effect should call applyAndNotifyTrait on lean_count
        # with op=add, value=1.
        self.assertRegex(
            twee,
            r'setup\.applyAndNotifyTrait\(\s*"player"\s*,\s*null\s*,\s*"lean_count"\s*,\s*"add"\s*,\s*1(?:\.0)?\s*,',
        )


# -- E6: per-choice text_variants -------------------------------------------


def _toml_with_text_variants(variants=None, base_text="Sit at the table."):
    """Minimal TOML with one canvas → one node → one choice with optional variants."""
    d = _base_toml()
    d["player"]["core_traits"]["corruption"] = 0
    d["starting_canvas"] = "test_canvas"
    choice = {
        "text": base_text,
        "targetType": "trigger",
    }
    if variants is not None:
        choice["text_variants"] = variants
    d["canvases"] = [
        {
            "id": "test_canvas",
            "name": "Test",
            "description": "x",
            "nodes": [
                {
                    "id": "n1",
                    "name": "N1",
                    "blocks": [{"type": "paragraph", "content": "x"}],
                    "exit_block": {
                        "type": "choices",
                        "choices": [choice],
                    },
                }
            ],
        }
    ]
    return d


class TextVariantsSchemaTests(SimpleTestCase):
    def _first_choice(self, template):
        return template.canvases[0].nodes[0].exit_block.choices[0]

    def test_default_text_variants_is_empty(self):
        template = normalize(_toml_with_text_variants(variants=None))
        self.assertEqual(self._first_choice(template).text_variants, [])

    def test_text_variants_parses_with_conditions(self):
        variants = [
            {
                "text": "Sit at the table — claim it.",
                "conditions": {
                    "version": "1.0",
                    "items": [
                        {
                            "type": "trait",
                            "subject": "player",
                            "trait_key": "corruption",
                            "operator": "gte",
                            "value": 75,
                        }
                    ],
                },
            }
        ]
        template = normalize(_toml_with_text_variants(variants=variants))
        ch = self._first_choice(template)
        self.assertEqual(len(ch.text_variants), 1)
        self.assertEqual(ch.text_variants[0]["text"], "Sit at the table — claim it.")
        self.assertEqual(
            ch.text_variants[0]["conditions"]["items"][0]["trait_key"], "corruption"
        )

    def test_existing_fixture_validates_clean_without_text_variants(self):
        # Sanity: the engine_prd_2026_04_22 fixture has no text_variants
        # anywhere; ensure E6 schema additions don't break its load.
        with open(FIXTURE_PATH, "rb") as f:
            data = tomli.load(f)
        template = normalize(data)
        self.assertEqual(validate(template), [])


class TextVariantsIntegrationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            email="batch2-e6-test@example.com", password="testpass123"
        )
        with open(FIXTURE_PATH, "rb") as f:
            cls.toml_data = tomli.load(f)

    def _build(self, mutator=None):
        toml_data = copy.deepcopy(self.toml_data)
        if mutator is not None:
            mutator(toml_data)
        template = normalize(toml_data)
        errors = validate(template)
        self.assertEqual(errors, [], f"Should validate clean: {errors}")
        result = create_project_from_template(template, str(self.user.id))
        project = Project.objects.get(id=result["project_id"])
        from apps.game_generation.twee_comprehensive.generators.v1 import (
            TweeComprehensiveGeneratorV1,
        )
        twee = TweeComprehensiveGeneratorV1().generate(project)
        return project, twee

    def _inject_choice_with_variants(self, d, variants, base_text="Continue."):
        d["player"]["core_traits"]["corruption"] = 0
        d["canvases"].append(
            {
                "id": "tv_test_canvas",
                "name": "TV Test",
                "description": "x",
                "trigger": {"location": "loc_home"},
                "nodes": [
                    {
                        "id": "tv1",
                        "name": "TV1",
                        "blocks": [{"type": "paragraph", "content": "x"}],
                        "exit_block": {
                            "type": "choices",
                            "choices": [
                                {
                                    "text": base_text,
                                    "targetType": "trigger",
                                    "text_variants": variants,
                                }
                            ],
                        },
                    }
                ],
            }
        )

    def test_e6_no_variants_emits_static_link_label(self):
        """Back-compat: a choice without text_variants emits the existing
        <<link "static text" "target">> form."""
        _, twee = self._build()
        # The fixture's exit_block is location-type, so choice <<link>> output
        # comes from elsewhere — just confirm no <<set _cv to>> pollution
        # appears for any pre-existing choice.
        self.assertNotIn("<<set _cv to", twee)

    def test_e6_variants_emit_branching_label_resolution(self):
        """A choice with text_variants emits a <<set _cv to>> chain that
        resolves the label at runtime via triggerConditionsSatisfied."""

        def mutate(d):
            self._inject_choice_with_variants(
                d,
                variants=[
                    {
                        "text": "Sit — claim it.",
                        "conditions": {
                            "version": "1.0",
                            "items": [
                                {
                                    "type": "trait",
                                    "subject": "player",
                                    "trait_key": "corruption",
                                    "operator": "gte",
                                    "value": 75,
                                }
                            ],
                        },
                    }
                ],
                base_text="Sit at the table.",
            )

        _, twee = self._build(mutator=mutate)
        # The pre-link <<set _cv to "base">> must appear.
        self.assertIn('<<set _cv to "Sit at the table."', twee)
        # The variant's conditional update must appear too.
        self.assertIn('<<set _cv to "Sit — claim it.', twee)
        # The link must use the variable form.
        self.assertRegex(twee, r"<<link\s+_cv\b")
        # Variant condition is wired to triggerConditionsSatisfied.
        self.assertRegex(
            twee,
            r"<<if\s+setup\.triggerConditionsSatisfied\(.*corruption.*?\)>>"
            r"<<set _cv to",
        )

    def test_e6_multiple_variants_emit_elseif_chain(self):
        """First-match-wins: emit <<if>> then <<elseif>> for additional variants."""

        def mutate(d):
            self._inject_choice_with_variants(
                d,
                variants=[
                    {
                        "text": "Saturated text.",
                        "conditions": {
                            "version": "1.0",
                            "items": [
                                {
                                    "type": "trait",
                                    "subject": "player",
                                    "trait_key": "corruption",
                                    "operator": "gte",
                                    "value": 75,
                                }
                            ],
                        },
                    },
                    {
                        "text": "Mid text.",
                        "conditions": {
                            "version": "1.0",
                            "items": [
                                {
                                    "type": "trait",
                                    "subject": "player",
                                    "trait_key": "corruption",
                                    "operator": "gte",
                                    "value": 50,
                                }
                            ],
                        },
                    },
                ],
            )

        _, twee = self._build(mutator=mutate)
        # Find the slice for the injected choice and assert the elseif chain.
        # Pattern: <<set _cv to "base">>\n<<if ...>><<set _cv to "saturated">>\n<<elseif ...>><<set _cv to "mid">>...
        idx = twee.find('<<set _cv to "Continue."')
        self.assertGreater(idx, -1, "Pre-link <<set _cv>> not found")
        body = twee[idx : idx + 2000]
        self.assertIn("<<if", body)
        self.assertIn("<<elseif", body)
        self.assertIn("Saturated text.", body)
        self.assertIn("Mid text.", body)


# -- E4: stage_helpers (named composite gates) ------------------------------


def _toml_with_stage_helpers(helpers=None):
    """Minimal TOML with optional [[engine.stage_helpers]] block."""
    d = _base_toml()
    d["player"]["core_traits"]["corruption"] = 0
    if helpers is not None:
        d["engine"] = {"stage_helpers": helpers}
    return d


_STAGE_HELPER_FRANK_2 = {
    "name": "frank_stage_2",
    "description": "Tease tier",
    "conditions": {
        "version": "1.0",
        "logic": "AND",
        "items": [
            {
                "type": "trait",
                "subject": "player",
                "trait_key": "corruption",
                "operator": "gte",
                "value": 25,
            }
        ],
    },
}


class StageHelpersSchemaTests(SimpleTestCase):
    def test_absent_stage_helpers_is_empty_list(self):
        template = normalize(_toml_with_stage_helpers(helpers=None))
        self.assertEqual(template.stage_helpers, [])

    def test_two_helpers_parse_with_all_fields(self):
        helper2 = dict(_STAGE_HELPER_FRANK_2)
        helper2 = {**helper2, "name": "frank_stage_3", "description": "Crack tier"}
        template = normalize(
            _toml_with_stage_helpers(helpers=[_STAGE_HELPER_FRANK_2, helper2])
        )
        self.assertEqual(len(template.stage_helpers), 2)
        names = [sh.name for sh in template.stage_helpers]
        self.assertEqual(names, ["frank_stage_2", "frank_stage_3"])
        self.assertEqual(template.stage_helpers[0].description, "Tease tier")
        self.assertIn("items", template.stage_helpers[0].conditions)

    def test_duplicate_names_fail_validation(self):
        template = normalize(
            _toml_with_stage_helpers(
                helpers=[_STAGE_HELPER_FRANK_2, dict(_STAGE_HELPER_FRANK_2)]
            )
        )
        errors = validate(template)
        self.assertTrue(
            any(
                "stage_helpers" in e and "frank_stage_2" in e and "duplicate" in e.lower()
                for e in errors
            ),
            errors,
        )

    def test_empty_name_fails_validation(self):
        bad = {**_STAGE_HELPER_FRANK_2, "name": ""}
        template = normalize(_toml_with_stage_helpers(helpers=[bad]))
        errors = validate(template)
        self.assertTrue(
            any("stage_helpers" in e and "name" in e for e in errors), errors
        )

    def test_helper_referencing_helper_fails_validation(self):
        # A helper whose conditions contain a `type=stage` item must be rejected
        # — recursion is deferred per PRD §E4 acceptance criterion 2.
        nested = {
            "name": "frank_stage_2_nested",
            "conditions": {
                "version": "1.0",
                "items": [
                    {"type": "stage", "helper": "some_other", "operator": "is_true"}
                ],
            },
        }
        template = normalize(_toml_with_stage_helpers(helpers=[nested]))
        errors = validate(template)
        self.assertTrue(
            any(
                "stage_helpers" in e and "stage" in e.lower() and "primitive" in e.lower()
                for e in errors
            ),
            errors,
        )


class StageHelpersIntegrationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            email="batch2-e4-test@example.com", password="testpass123"
        )
        with open(FIXTURE_PATH, "rb") as f:
            cls.toml_data = tomli.load(f)

    def _build(self, mutator=None):
        toml_data = copy.deepcopy(self.toml_data)
        if mutator is not None:
            mutator(toml_data)
        template = normalize(toml_data)
        errors = validate(template)
        self.assertEqual(errors, [], f"Should validate clean: {errors}")
        result = create_project_from_template(template, str(self.user.id))
        project = Project.objects.get(id=result["project_id"])
        from apps.game_generation.twee_comprehensive.generators.v1 import (
            TweeComprehensiveGeneratorV1,
        )
        twee = TweeComprehensiveGeneratorV1().generate(project)
        return project, twee

    def test_e4_setup_stage_helpers_emitted_when_configured(self):
        def mutate(d):
            d["engine"] = {"stage_helpers": [_STAGE_HELPER_FRANK_2]}

        _, twee = self._build(mutator=mutate)
        self.assertIn("setup.stage_helpers = ", twee)
        self.assertIn("frank_stage_2", twee)

    def test_e4_setup_stage_helpers_map_build_emitted(self):
        def mutate(d):
            d["engine"] = {"stage_helpers": [_STAGE_HELPER_FRANK_2]}

        _, twee = self._build(mutator=mutate)
        self.assertIn("setup.stage_helpers_map", twee)

    def test_e4_trigger_conditions_satisfied_has_stage_branch(self):
        _, twee = self._build()
        # The condition evaluator gains a new branch dispatching on type === 'stage'.
        self.assertRegex(twee, r"type\s*===?\s*['\"]stage['\"]")

    def test_e4_canvas_trigger_can_use_stage_helper(self):
        """A canvas trigger can gate on a named stage helper."""

        def mutate(d):
            d["engine"] = {"stage_helpers": [_STAGE_HELPER_FRANK_2]}
            d["canvases"].append(
                {
                    "id": "stage_test_canvas",
                    "name": "Stage Test",
                    "description": "x",
                    "trigger": {
                        "location": "loc_home",
                        "conditions": {
                            "version": "1.0",
                            "items": [
                                {
                                    "type": "stage",
                                    "helper": "frank_stage_2",
                                    "operator": "is_true",
                                }
                            ],
                        },
                    },
                    "nodes": [
                        {
                            "id": "n1",
                            "name": "N1",
                            "blocks": [{"type": "paragraph", "content": "x"}],
                            "exit_block": {
                                "type": "location",
                                "text": "ok",
                                "config": {
                                    "destinationType": "specific",
                                    "locationId": "loc_home",
                                },
                            },
                        }
                    ],
                }
            )

        _, twee = self._build(mutator=mutate)
        # Verify the trigger condition got serialized into the runtime
        # (the JSON shape includes the helper reference verbatim).
        self.assertIn('"helper": "frank_stage_2"', twee)
