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
        # The fail-forward branch sets the flag via the canonical helper —
        # 2026-05-06 consolidation retired direct $player.flags writes; all
        # player-flag mutations now go through setup.applyAndNotifyFlag so
        # writes land in the canonical $flags store + queue UI notification.
        self.assertIn('<<if setup.rent_eviction_mode is "flag_set">>', passage)
        self.assertIn(
            "setup.applyAndNotifyFlag('player', null, setup.rent_eviction_flag, 'set')",
            passage,
        )
        self.assertNotIn("$player.flags[setup.rent_eviction_flag]", passage)
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

    def test_stage_helper_with_or_logic_fails_validation(self):
        """OR-restriction (2026-05-03): OR in helpers produces awkward
        Path A/B rendering in the Pattern 2 goal block. Author should
        refactor to separate transition canvases per RTS pattern."""
        bad = {
            "name": "test_or_helper",
            "description": "Test OR rejection",
            "conditions": {
                "version": "1.0",
                "logic": "OR",
                "items": [
                    {"type": "flag", "subject": "player", "flag_key": "a", "operator": "is_true"},
                    {"type": "flag", "subject": "player", "flag_key": "b", "operator": "is_true"},
                ],
            },
        }
        template = normalize(_toml_with_stage_helpers(helpers=[bad]))
        errors = validate(template)
        self.assertTrue(
            any("OR-logic is not allowed in stage_helpers" in e for e in errors),
            f"Expected OR-logic rejection error, got: {errors}",
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


# -- arc_stages: per-NPC stage display registry (E9/E10/E11 foundation) ------


_FRANK_ARC_STAGES = ["Suspicious", "Warm", "Restrict", "Tease", "Cracked"]


def _toml_with_arc_stages(arc_stages=None, player_trait_decay=None):
    """Minimal TOML where the single NPC may declare arc_stages."""
    d = _base_toml()
    if arc_stages is not None:
        d["npcs"][0]["arc_stages"] = arc_stages
    if player_trait_decay is not None:
        d["player"]["trait_decay"] = player_trait_decay
    return d


class ArcStagesSchemaTests(SimpleTestCase):
    def test_absent_arc_stages_is_empty_list(self):
        template = normalize(_toml_with_arc_stages(arc_stages=None))
        self.assertEqual(template.npcs[0].arc_stages, [])
        # Empty list also validates clean — treated as no stage chain.
        self.assertEqual(validate(template), [])

    def test_explicit_empty_list_validates_clean(self):
        template = normalize(_toml_with_arc_stages(arc_stages=[]))
        self.assertEqual(template.npcs[0].arc_stages, [])
        self.assertEqual(validate(template), [])

    def test_full_chain_parses_in_order(self):
        template = normalize(_toml_with_arc_stages(arc_stages=_FRANK_ARC_STAGES))
        self.assertEqual(template.npcs[0].arc_stages, _FRANK_ARC_STAGES)
        self.assertEqual(validate(template), [])

    def test_non_list_raises_type_error(self):
        with self.assertRaises(TypeError) as ctx:
            normalize(_toml_with_arc_stages(arc_stages="Suspicious"))
        self.assertIn("arc_stages must be a list", str(ctx.exception))

    def test_non_string_element_raises_type_error(self):
        with self.assertRaises(TypeError) as ctx:
            normalize(_toml_with_arc_stages(arc_stages=["Suspicious", 2, "Warm"]))
        self.assertIn("arc_stages[1]", str(ctx.exception))
        self.assertIn("must be a string", str(ctx.exception))

    def test_player_trait_decay_collision_fails_validation(self):
        # An NPC with arc_stages cannot have its <slug>_stage trait listed in
        # player.trait_decay — decay bypasses applyAndNotifyTrait, which is
        # where E9 hooks the advancement log. The validator catches it.
        d = _toml_with_arc_stages(
            arc_stages=_FRANK_ARC_STAGES,
            player_trait_decay={"npc_frank_stage": 0.5},
        )
        # The collision trait must exist in core_traits so trait_decay
        # validation reaches the arc_stages check (otherwise the missing-trait
        # error fires first).
        d["player"]["core_traits"]["npc_frank_stage"] = 0
        template = normalize(d)
        errors = validate(template)
        self.assertTrue(
            any(
                "npc_frank" in e
                and "arc_stages" in e
                and "trait_decay" in e
                and "npc_frank_stage" in e
                for e in errors
            ),
            f"Expected collision error, got: {errors}",
        )


class ArcStagesIntegrationTests(TestCase):
    """Full pipeline: TOML → DB → generator → Twee. Verifies that the
    slug-keyed registry lands in the runtime as setup.npc_arc_stages."""

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            email="arc-stages-test@example.com", password="testpass123"
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

    def test_no_arc_stages_emits_empty_registry(self):
        # Fixture has no arc_stages on any NPC by default.
        _, twee = self._build()
        self.assertIn("setup.npc_arc_stages = ", twee)
        # Empty object emitted when no NPC declares stages.
        self.assertIn("setup.npc_arc_stages = {};", twee)

    def test_frank_arc_stages_emitted_in_registry(self):
        def mutate(d):
            for n in d.get("npcs", []):
                if n.get("id") == "npc_frank":
                    n["arc_stages"] = _FRANK_ARC_STAGES
                    break

        _, twee = self._build(mutator=mutate)
        # Slug-keyed entry must appear with all five labels in order.
        self.assertIn("setup.npc_arc_stages = ", twee)
        self.assertIn('"npc_frank"', twee)
        for label in _FRANK_ARC_STAGES:
            self.assertIn(f'"{label}"', twee)
        # Spot-check that the registry contains the slug pointing at the chain.
        # Pattern: "npc_frank": ["Suspicious", "Warm", ...]
        self.assertRegex(
            twee,
            r'"npc_frank"\s*:\s*\[\s*"Suspicious"\s*,\s*"Warm"\s*,\s*"Restrict"',
        )


# -- E11: stage_label sidebar item -------------------------------------------


def _toml_with_stage_label(item, arc_stages=None):
    """Minimal TOML with one sidebar_items entry; Frank gets arc_stages
    unless explicitly set to empty."""
    d = _base_toml()
    d["npcs"][0]["arc_stages"] = (
        _FRANK_ARC_STAGES if arc_stages is None else arc_stages
    )
    d["sidebar_items"] = [item]
    return d


class StageLabelSidebarSchemaTests(SimpleTestCase):
    def test_minimal_valid_stage_label(self):
        item = {"type": "stage_label", "npc_id": "npc_frank"}
        template = normalize(_toml_with_stage_label(item))
        self.assertEqual(validate(template), [])

    def test_stage_label_with_prefix(self):
        item = {"type": "stage_label", "npc_id": "npc_frank", "prefix": "Stepdad"}
        template = normalize(_toml_with_stage_label(item))
        self.assertEqual(validate(template), [])

    def test_missing_npc_id_fails(self):
        item = {"type": "stage_label"}
        template = normalize(_toml_with_stage_label(item))
        errors = validate(template)
        self.assertTrue(
            any("stage_label" in e and "npc_id" in e and "required" in e for e in errors),
            errors,
        )

    def test_unknown_npc_id_fails(self):
        item = {"type": "stage_label", "npc_id": "npc_ghost"}
        template = normalize(_toml_with_stage_label(item))
        errors = validate(template)
        self.assertTrue(
            any(
                "stage_label" in e and "npc_ghost" in e and "not found" in e
                for e in errors
            ),
            errors,
        )

    def test_npc_without_arc_stages_fails(self):
        item = {"type": "stage_label", "npc_id": "npc_frank"}
        # Force arc_stages empty — npc_frank has no stage chain.
        template = normalize(_toml_with_stage_label(item, arc_stages=[]))
        errors = validate(template)
        self.assertTrue(
            any(
                "stage_label" in e and "arc_stages" in e and "npc_frank" in e
                for e in errors
            ),
            errors,
        )

    def test_non_string_prefix_fails(self):
        item = {"type": "stage_label", "npc_id": "npc_frank", "prefix": 7}
        template = normalize(_toml_with_stage_label(item))
        errors = validate(template)
        self.assertTrue(
            any("stage_label" in e and "prefix" in e and "string" in e for e in errors),
            errors,
        )


class StageLabelSidebarIntegrationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            email="stage-label-test@example.com", password="testpass123"
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

    def test_stage_label_branch_emitted_when_configured(self):
        def mutate(d):
            for n in d.get("npcs", []):
                if n.get("id") == "npc_frank":
                    n["arc_stages"] = _FRANK_ARC_STAGES
                    break
            d.setdefault("sidebar_items", []).append({
                "type": "stage_label",
                "npc_id": "npc_frank",
                "prefix": "Frank",
            })

        _, twee = self._build(mutator=mutate)
        # Render block must be present in the sidebar widget.
        self.assertIn('_item.type is "stage_label"', twee)
        # Trait name derivation visible in the emitted Twee.
        self.assertIn('_slNpcId + "_stage"', twee)
        # Out-of-range clamp uses Math.min against arc_stages.length - 1.
        self.assertRegex(twee, r"Math\.min\(Number\(_slRawStage\),\s*_slStages\.length\s*-\s*1\)")

    def test_stage_label_render_block_present_even_without_item(self):
        # The widget's elseif branch is part of the static widget definition,
        # so it ships even when no stage_label item is configured. This keeps
        # authoring forward-compatible: adding a stage_label later doesn't
        # require a regenerate.
        _, twee = self._build()
        self.assertIn('_item.type is "stage_label"', twee)


# -- E9: stage-flag stalled-progress detection -------------------------------


def _toml_with_story_arc_hints(hints_overrides=None, arc_stages=None):
    """Minimal TOML with [story_arc] + [story_arc.hints]. Frank gets
    arc_stages by default so the stalled-detection paths engage."""
    d = _base_toml()
    d["npcs"][0]["arc_stages"] = (
        _FRANK_ARC_STAGES if arc_stages is None else arc_stages
    )
    base_hints = {
        "stuck_threshold_minutes": 30,
        "hint_style": "observation",
        "templates": [],
    }
    if hints_overrides:
        base_hints.update(hints_overrides)
    d["story_arc"] = {"version": "1.0", "hints": base_hints}
    return d


class StageStallSchemaTests(SimpleTestCase):
    def test_defaults_when_fields_omitted(self):
        template = normalize(_toml_with_story_arc_hints())
        self.assertIsNotNone(template.story_arc)
        self.assertIsNotNone(template.story_arc.hints)
        self.assertEqual(template.story_arc.hints.stuck_threshold_days, 7)
        self.assertEqual(template.story_arc.hints.stage_stall_message, "")

    def test_custom_threshold_and_message_parse(self):
        template = normalize(_toml_with_story_arc_hints(hints_overrides={
            "stuck_threshold_days": 14,
            "stage_stall_message": "Maya feels herself standing still.",
        }))
        self.assertEqual(template.story_arc.hints.stuck_threshold_days, 14)
        self.assertEqual(
            template.story_arc.hints.stage_stall_message,
            "Maya feels herself standing still.",
        )

    def test_legacy_minutes_still_supported_alongside_days(self):
        # stuck_threshold_minutes is unrelated to E9 but lives on the same
        # dataclass — confirm the existing field doesn't regress.
        template = normalize(_toml_with_story_arc_hints(hints_overrides={
            "stuck_threshold_minutes": 60,
            "stuck_threshold_days": 5,
        }))
        self.assertEqual(template.story_arc.hints.stuck_threshold_minutes, 60)
        self.assertEqual(template.story_arc.hints.stuck_threshold_days, 5)


class StageStallIntegrationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            email="stage-stall-test@example.com", password="testpass123"
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

    def test_stage_advancement_log_initialized_in_game_state(self):
        _, twee = self._build()
        # The init lives in $game_state setup at the Start passage.
        self.assertIn('"stage_advancement_log": {}', twee)

    def test_advancement_log_hook_in_apply_and_notify_trait(self):
        # The regex + registry check sits inside applyAndNotifyTrait.
        _, twee = self._build()
        self.assertRegex(twee, r"/\^\(\[a-z_\]\+\)_stage\$/\.exec\(trait\)")
        # Hook is gated on positive delta + registry membership.
        self.assertIn("delta > 0 && setup.npc_arc_stages", twee)
        self.assertIn("stage_advancement_log[stageMatch[1]]", twee)

    def test_stage_progression_stalled_block_emitted(self):
        _, twee = self._build()
        # detectStoryPosition adds the stalled flag and the OR-with-not-complete
        # guard. Both must be visible in the emitted runtime.
        self.assertIn("result.stage_progression_stalled", twee)
        self.assertRegex(twee, r"completed_nodes\.length\s*<\s*totalNodes\s*\|\|\s*totalNodes\s*===\s*0")

    def test_stage_stall_hint_branch_in_generate_narrative_hint(self):
        _, twee = self._build()
        # The new top branch in generateNarrativeHint sets hint_type "stage_stall"
        # and reads custom message with generic fallback.
        self.assertIn('"stage_stall"', twee)
        self.assertIn("Days are slipping past", twee)
        # Custom message comes from arc.hints.stage_stall_message.
        self.assertIn("hints.stage_stall_message", twee)

    def test_custom_stall_message_reaches_runtime(self):
        # Author-provided stage_stall_message round-trips into setup.story_arc.hints.
        def mutate(d):
            for n in d.get("npcs", []):
                if n.get("id") == "npc_frank":
                    n["arc_stages"] = _FRANK_ARC_STAGES
                    break
            d.setdefault("story_arc", {}).setdefault("hints", {})
            d["story_arc"]["hints"]["stage_stall_message"] = (
                "Maya feels the days slip past her."
            )
            d["story_arc"]["hints"]["stuck_threshold_days"] = 5

        _, twee = self._build(mutator=mutate)
        self.assertIn("Maya feels the days slip past her.", twee)
        # Threshold must round-trip — default is 7, custom is 5.
        self.assertIn('"stuck_threshold_days": 5', twee)

    def test_hidden_npcs_excluded_from_stall_check(self):
        # Hidden NPCs shouldn't contribute to stall detection — the runtime
        # filters them out via npc.hidden_from_ui.
        _, twee = self._build()
        self.assertIn("npc.hidden_from_ui", twee)


# -- E10: stage-gated hint pool + template consumer --------------------------


def _toml_with_hint_template(template_dict, arc_stages=None):
    """Build TOML with a single hint template + Frank arc_stages by default."""
    d = _base_toml()
    d["npcs"][0]["arc_stages"] = (
        _FRANK_ARC_STAGES if arc_stages is None else arc_stages
    )
    d["story_arc"] = {
        "version": "1.0",
        "hints": {
            "stuck_threshold_minutes": 30,
            "hint_style": "observation",
            "templates": [template_dict],
        },
    }
    return d


class StageGatedHintSchemaTests(SimpleTestCase):
    def test_full_stage_gate_triple_validates(self):
        tpl = {
            "text": "Frank's started warming up.",
            "condition": {
                "stage_npc": "npc_frank",
                "stage_op": "eq",
                "stage_value": 1,
            },
        }
        template = normalize(_toml_with_hint_template(tpl))
        errors = validate(template)
        self.assertEqual(errors, [], f"Should validate clean: {errors}")
        # npc_id defaults to stage_npc when not explicitly set on the template.
        self.assertEqual(template.story_arc.hints.templates[0].npc_id, "npc_frank")

    def test_partial_triple_fails_validation(self):
        # stage_npc + stage_op without stage_value
        tpl = {
            "text": "Hint.",
            "condition": {"stage_npc": "npc_frank", "stage_op": "gte"},
        }
        template = normalize(_toml_with_hint_template(tpl))
        errors = validate(template)
        self.assertTrue(
            any("must all be set together" in e for e in errors), errors
        )

    def test_invalid_stage_op_fails(self):
        tpl = {
            "text": "Hint.",
            "condition": {
                "stage_npc": "npc_frank",
                "stage_op": "BETWEEN",
                "stage_value": 1,
            },
        }
        template = normalize(_toml_with_hint_template(tpl))
        errors = validate(template)
        self.assertTrue(
            any("stage_op must be one of" in e for e in errors), errors
        )

    def test_unknown_stage_npc_fails(self):
        tpl = {
            "text": "Hint.",
            "condition": {
                "stage_npc": "npc_ghost",
                "stage_op": "eq",
                "stage_value": 0,
            },
        }
        template = normalize(_toml_with_hint_template(tpl))
        errors = validate(template)
        self.assertTrue(
            any("npc_ghost" in e and "not found" in e for e in errors), errors
        )

    def test_stage_npc_without_arc_stages_fails(self):
        tpl = {
            "text": "Hint.",
            "condition": {
                "stage_npc": "npc_frank",
                "stage_op": "eq",
                "stage_value": 0,
            },
        }
        # NPC exists but has no arc_stages.
        template = normalize(_toml_with_hint_template(tpl, arc_stages=[]))
        errors = validate(template)
        self.assertTrue(
            any("npc_frank" in e and "without arc_stages" in e for e in errors),
            errors,
        )

    def test_stage_value_out_of_range_fails(self):
        tpl = {
            "text": "Hint.",
            "condition": {
                "stage_npc": "npc_frank",
                "stage_op": "eq",
                "stage_value": 99,
            },
        }
        template = normalize(_toml_with_hint_template(tpl))
        errors = validate(template)
        self.assertTrue(
            any("out of range" in e and "0..4" in e for e in errors), errors
        )

    def test_explicit_npc_id_overrides_default(self):
        tpl = {
            "text": "Hint.",
            "npc_id": "npc_frank",
            "condition": {"missing_flag": "frank_caught"},
        }
        template = normalize(_toml_with_hint_template(tpl))
        errors = validate(template)
        self.assertEqual(errors, [], f"Should validate clean: {errors}")
        self.assertEqual(template.story_arc.hints.templates[0].npc_id, "npc_frank")

    def test_unknown_npc_id_routing_fails(self):
        tpl = {
            "text": "Hint.",
            "npc_id": "npc_ghost",
            "condition": {"missing_flag": "x_flag"},
        }
        template = normalize(_toml_with_hint_template(tpl))
        errors = validate(template)
        self.assertTrue(
            any("npc_id" in e and "npc_ghost" in e for e in errors), errors
        )


class StageGatedHintIntegrationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            email="stage-gated-hint-test@example.com", password="testpass123"
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

    def _add_frank_stage_chain_and_hint(self, d, hint_text="Stage 1 hint."):
        for n in d.get("npcs", []):
            if n.get("id") == "npc_frank":
                n["arc_stages"] = _FRANK_ARC_STAGES
                break
        d.setdefault("story_arc", {}).setdefault("hints", {})
        d["story_arc"]["hints"].setdefault("templates", []).append({
            "text": hint_text,
            "condition": {
                "stage_npc": "npc_frank",
                "stage_op": "eq",
                "stage_value": 1,
            },
        })

    def test_runtime_helpers_emitted(self):
        # Both consumer functions and the slug-resolver must be present
        # in the runtime, regardless of whether a hint template is configured.
        _, twee = self._build()
        self.assertIn("setup.getStageHintForNPC = function", twee)
        self.assertIn("setup.npcSlugForId = function", twee)

    def test_get_next_activity_short_circuits_on_stage_hint(self):
        # The early-return block at the top of getNextActivity uses isStageHint.
        _, twee = self._build()
        self.assertIn("setup.getStageHintForNPC(slug)", twee)
        self.assertIn("isStageHint: true", twee)

    def test_quests_page_renders_stage_hint_directly(self):
        _, twee = self._build()
        # Quests cards: picker resolves which template fires per NPC, widget
        # renders the narrative line + (Pattern 2) auto-rendered 🎯 goal block.
        self.assertIn("setup.getStageHintForNPC(_slug)", twee)
        self.assertIn("<<renderStageHint _hint>>", twee)
        # Pattern 2 restored — goal block engine must be present.
        self.assertIn("setup.computeHintGoal", twee)
        # Pattern 3 (per-NPC activity list) remains EXCLUDED.
        self.assertNotIn("setup.computeActivityList", twee)

    def test_sidebar_hint_extracts_stage_hint_first(self):
        _, twee = self._build()
        # The new branch lives at the top of the per-source loop.
        self.assertIn("next.isStageHint && next.stageHint && next.stageHint.text", twee)

    def test_template_normalized_to_condition_items(self):
        # When a stage-gate triple is authored, condition_items must contain
        # a regular trait condition on <slug>_stage that checkSingleCondition
        # can evaluate without a new branch.
        def mutate(d):
            self._add_frank_stage_chain_and_hint(d, "Numbers warmth, Stage 1.")

        _, twee = self._build(mutator=mutate)
        # The normalized condition_items list must show in the runtime JSON.
        self.assertIn('"trait_key": "npc_frank_stage"', twee)
        self.assertIn('"operator": "eq"', twee)
        self.assertIn('"value": 1', twee)
        self.assertIn('"npc_id": "npc_frank"', twee)
        self.assertIn("Numbers warmth, Stage 1.", twee)

    def test_missing_flag_normalizes_to_is_false_condition(self):
        # A missing_flag condition becomes a flag/is_false predicate so the
        # existing checkSingleCondition handles it.
        def mutate(d):
            for n in d.get("npcs", []):
                if n.get("id") == "npc_frank":
                    n["arc_stages"] = _FRANK_ARC_STAGES
                    break
            d.setdefault("story_arc", {}).setdefault("hints", {})
            d["story_arc"]["hints"].setdefault("templates", []).append({
                "text": "He hasn't caught you yet.",
                "npc_id": "npc_frank",
                "condition": {"missing_flag": "frank_caught"},
            })

        _, twee = self._build(mutator=mutate)
        self.assertIn('"flag_key": "frank_caught"', twee)
        self.assertIn('"operator": "is_false"', twee)


# -- Narrative-priority picker (2026-05-01) ----------------------------------


class HintPriorityPickerTests(StageGatedHintIntegrationTests):
    """Picker rule: (priority desc, condition_items.length desc, file-order asc).

    Verifies the field round-trips through loader → serializer → runtime,
    that the runtime sort comparator is shipped, and that the linter warns
    on undecidable ties (same npc_id + stage_value + priority + items count).
    """

    def test_priority_field_loads_and_serializes(self):
        # Default templates serialize with priority = 0 (no field on TOML).
        def add_default(d):
            self._add_frank_stage_chain_and_hint(d, "Default Frank line.")

        _, twee = self._build(mutator=add_default)
        self.assertIn('"priority": 0', twee)

    def test_explicit_priority_flows_through(self):
        def add_with_priority(d):
            self._add_frank_stage_chain_and_hint(d, "Crisis Frank line.")
            # Bump the lone hint's priority and add a missing_flag distinguisher.
            d["story_arc"]["hints"]["templates"][0]["priority"] = 10
            d["story_arc"]["hints"]["templates"][0]["condition"]["missing_flag"] = "first_rent_paid"

        _, twee = self._build(mutator=add_with_priority)
        self.assertIn('"priority": 10', twee)

    def test_picker_sorts_candidates_in_runtime_js(self):
        _, twee = self._build()
        # The picker should collect candidates and sort by the comparator.
        self.assertIn("candidates.push", twee)
        self.assertIn("candidates.sort", twee)
        self.assertIn("priority || 0", twee)

    def test_global_hints_dedupe_by_goal_key(self):
        _, twee = self._build()
        # getGlobalHints groups by missing_flag || missing_trait || file index.
        self.assertIn("missing_flag", twee)
        self.assertIn("missing_trait", twee)
        # Goal-key grouping pattern + per-group sort.
        self.assertIn("groupOrder", twee)

    def test_linter_warns_on_undecidable_tie(self):
        import warnings as _w

        def add_tied_pair(d):
            # Two templates targeting Frank Stage 1 with identical priority
            # (default 0) and identical condition_items count (1 — the stage
            # gate). File order would silently win — linter should warn.
            # _add_frank_stage_chain_and_hint adds a hint with stage_value=1.
            self._add_frank_stage_chain_and_hint(d, "First Frank line.")
            d["story_arc"]["hints"]["templates"].append({
                "text": "Second Frank line.",
                "npc_id": "npc_frank",
                "condition": {"stage_npc": "npc_frank", "stage_op": "eq", "stage_value": 1},
            })

        with _w.catch_warnings(record=True) as caught:
            _w.simplefilter("always")
            self._build(mutator=add_tied_pair)
        tie_warnings = [
            str(w.message) for w in caught
            if "undecidable picker tie" in str(w.message)
        ]
        self.assertTrue(
            tie_warnings,
            "Expected a HINT LINTER WARN about an undecidable picker tie",
        )


# -- Tips page (game-level mechanics surface, 2026-05-01) --------------------


class TipsPageTests(StageGatedHintIntegrationTests):
    """[ui.tips_page] is opt-in: when authored, engine ships a setup.tips_page
    runtime object + emits a :: TipsPage passage + the sidebar shows a
    💡 Tips button. When absent, none of those appear."""

    def test_tips_page_emitted_when_authored(self):
        def add_tips(d):
            d.setdefault("ui", {})["tips_page"] = {
                "title": "Tips",
                "content": "<h3>Trust</h3><p>Decays 1.0/day if ignored.</p>",
            }

        _, twee = self._build(mutator=add_tips)
        # Runtime ship line + page passage + the authored content body.
        self.assertIn("setup.tips_page = ", twee)
        self.assertIn(":: TipsPage", twee)
        self.assertIn("Decays 1.0/day if ignored", twee)

    def test_tips_page_skipped_when_absent(self):
        # Default fixture has no [ui.tips_page] block.
        _, twee = self._build()
        # Ship line still present (empty object) — graceful no-op.
        self.assertIn("setup.tips_page = ", twee)
        # Sidebar widget body has the conditional guard.
        self.assertIn("setup.tips_page && setup.tips_page.content", twee)

    def test_quests_button_relabeled_to_quests(self):
        _, twee = self._build()
        # Pre-2026-05-01 the button said "📖 Guide" (misleading — pointed at
        # QuestsPage). Now reads "📋 Quests"; old label must be gone from
        # the sidebar widget.
        self.assertIn('"📋 Quests"', twee)
        self.assertNotIn('"📖 Guide"', twee)

    def test_tips_button_widget_invoked_in_sidebar(self):
        _, twee = self._build()
        # StoryCaption (one of dev/non-dev branches gets emitted per build) must
        # invoke the new widget alongside the other sidebar buttons.
        self.assertIn("<<tipsButton>>", twee)
        # Widget definition itself must exist.
        self.assertIn('<<widget "tipsButton">>', twee)


# -- E9+E10+E11 fixture-driven smoke test ------------------------------------


PHASE2_FIXTURE_PATH = (
    Path(__file__).resolve().parent.parent
    / "game_generation"
    / "games_toml_files"
    / "engine_prd_phase2_2026_04_29.toml"
)


class Phase2IntegrationSmokeTest(TestCase):
    """End-to-end check on the Phase 2 didactic fixture. If this breaks, the
    fixture and the engine code drifted apart — fix one or the other."""

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            email="phase2-smoke-test@example.com", password="testpass123"
        )

    def test_phase2_fixture_builds_clean_with_all_three_features(self):
        with open(PHASE2_FIXTURE_PATH, "rb") as f:
            toml_data = tomli.load(f)
        template = normalize(toml_data)
        errors = validate(template)
        self.assertEqual(errors, [], f"Phase 2 fixture should validate clean: {errors}")
        result = create_project_from_template(template, str(self.user.id))
        project = Project.objects.get(id=result["project_id"])
        from apps.game_generation.twee_comprehensive.generators.v1 import (
            TweeComprehensiveGeneratorV1,
        )
        twee = TweeComprehensiveGeneratorV1().generate(project)

        # Foundation: arc_stages registry shipped with all five labels.
        self.assertIn('"npc_frank"', twee)
        for label in ["Suspicious", "Warm", "Restrict", "Tease", "Cracked"]:
            self.assertIn(f'"{label}"', twee)

        # E11: stage_label sidebar branch present.
        self.assertIn('_item.type is "stage_label"', twee)

        # E9: advancement-log hook + custom stall message + threshold round-trip.
        self.assertIn("stage_advancement_log", twee)
        self.assertIn("Days are slipping past. Maya feels herself", twee)
        self.assertIn('"stuck_threshold_days": 7', twee)

        # E10: template consumer + per-stage normalized condition_items.
        self.assertIn("setup.getStageHintForNPC", twee)
        # The three template texts must each appear in the runtime — that's
        # the most distinctive signal. (Counting trait_key occurrences is
        # noisy because canvas trigger conditions also reference the stage
        # trait; we don't depend on that count here.)
        self.assertIn("Try talking to Frank in the kitchen", twee)
        self.assertIn("Frank's started warming up", twee)
        self.assertIn("Things have shifted. The chores are the new way", twee)
        self.assertIn('"npc_id": "npc_frank"', twee)
        # The normalized trait condition lands at minimum 3× — once per
        # hint template. (Canvas triggers add more; we just want the
        # template-emission path to be present.)
        self.assertGreaterEqual(twee.count('"trait_key": "npc_frank_stage"'), 3)

        # Pattern 3 (2026-05-01): QuestsPage routes stage hints directly via
        # setup.getStageHintForNPC (not through getNextActivity). The earlier
        # `<<elseif _next.isStageHint>>` branches were removed when activity
        # lists replaced the per-source single-next-activity rendering.
        self.assertIn("setup.getStageHintForNPC(_slug)", twee)
        self.assertIn("<<renderStageHint _hint>>", twee)


# -- Pattern 2 (2026-05-01): label registries + tip + auto_goal -------------


def _toml_with_labels(trait_labels=None, flag_labels=None):
    """Minimal TOML with optional [[traits.labels]] / [[flags.labels]] blocks."""
    d = _base_toml()
    if trait_labels is not None:
        d["traits"] = {"labels": trait_labels}
    if flag_labels is not None:
        d["flags"] = {"labels": flag_labels}
    return d


class Pattern2LabelRegistryTests(SimpleTestCase):
    def test_absent_label_registries_are_empty_lists(self):
        template = normalize(_toml_with_labels())
        self.assertEqual(template.trait_labels, [])
        self.assertEqual(template.flag_labels, [])

    def test_trait_label_parses_with_all_fields(self):
        template = normalize(
            _toml_with_labels(
                trait_labels=[
                    {"key": "frank_bookkeeping_count", "label": "Bookkeeping",
                     "verb": "do", "unit": "session"}
                ]
            )
        )
        self.assertEqual(len(template.trait_labels), 1)
        tl = template.trait_labels[0]
        self.assertEqual(tl.key, "frank_bookkeeping_count")
        self.assertEqual(tl.label, "Bookkeeping")
        self.assertEqual(tl.verb, "do")
        self.assertEqual(tl.unit, "session")

    def test_flag_label_parses(self):
        template = normalize(
            _toml_with_labels(
                flag_labels=[{"key": "group_settled_in", "label": "Settled in"}]
            )
        )
        self.assertEqual(len(template.flag_labels), 1)
        self.assertEqual(template.flag_labels[0].key, "group_settled_in")
        self.assertEqual(template.flag_labels[0].label, "Settled in")

    def test_duplicate_trait_label_keys_fail_validation(self):
        template = normalize(
            _toml_with_labels(
                trait_labels=[
                    {"key": "trust", "label": "Trust"},
                    {"key": "trust", "label": "Different"},
                ]
            )
        )
        errors = validate(template)
        self.assertTrue(
            any("traits.labels" in e and "duplicate" in e.lower() for e in errors),
            errors,
        )

    def test_missing_label_field_fails_validation(self):
        template = normalize(
            _toml_with_labels(trait_labels=[{"key": "trust", "label": ""}])
        )
        errors = validate(template)
        self.assertTrue(
            any("traits.labels" in e and "label" in e for e in errors), errors
        )

    def test_serializer_emits_tip_and_auto_goal(self):
        from apps.projects.services.template_import import _serialize_hint_template, TemplateHintTemplate, TemplateHintCondition
        t = TemplateHintTemplate(
            text="He's looser at the table now.",
            tip="Each Bookkeeping pays $8.",
            auto_goal=True,
            npc_id="npc_frank",
            condition=TemplateHintCondition(
                stage_npc="npc_frank", stage_op="eq", stage_value=0
            ),
        )
        out = _serialize_hint_template(t)
        self.assertEqual(out["tip"], "Each Bookkeeping pays $8.")
        self.assertTrue(out["auto_goal"])
        self.assertEqual(out["text"], "He's looser at the table now.")

    def test_auto_goal_defaults_true_when_omitted_in_toml(self):
        d = _base_toml()
        d["story_arc"] = {
            "version": "1.0",
            "hints": {
                "stuck_threshold_minutes": 30,
                "templates": [
                    {"text": "test", "npc_id": "npc_frank"}
                ],
            },
        }
        template = normalize(d)
        self.assertTrue(template.story_arc.hints.templates[0].auto_goal)


class Pattern2RuntimeMetadataTests(TestCase):
    """Test that label registries flow through create_project_from_template."""

    def test_label_registries_persist_to_project_metadata(self):
        from apps.projects.services.template_import import create_project_from_template
        from apps.authentication.models import User
        from apps.projects.models import Project

        d = _toml_with_labels(
            trait_labels=[
                {"key": "frank_bookkeeping_count", "label": "Bookkeeping", "verb": "do"}
            ],
            flag_labels=[{"key": "group_settled_in", "label": "Settled in"}],
        )
        template = normalize(d)
        owner = User.objects.create_user(
            username="p2_runtime", email="p2r@test", password="x"
        )
        result = create_project_from_template(template, owner_id=str(owner.id))
        proj = Project.objects.get(id=result["project_id"])
        self.assertEqual(
            proj.metadata["trait_labels"]["frank_bookkeeping_count"]["verb"], "do"
        )


# =============================================================================
# S7 (linkreplace cascade) + S8 (thought bubble) — engine primitives
# =============================================================================
# Authored 2026-05-06 with the bedroom-anchor pilot rewrite. Doctrine source:
# docs 21 + 22 (RTS Brother + cross-NPC mechanism audits, 40 surfaces verified
# live in doc 22 §11). Pattern D (top-of-cascade gate, then linear) is the
# dominant family-arc shape; Pattern E (gate at hub button, pure linear) is
# dominant in peer/career. Per-beat effects fire on click — verified live in
# MarcusParkDate where <<MakeBoyfriend>> ran on Accept (loyalty 0 → 100).


class S7CascadeNormalizationTests(SimpleTestCase):
    """Schema-side: cascade block normalization via _normalize_block_list."""

    def _norm_one(self, block_dict):
        """Helper: normalize a single block, return the safe dict."""
        from apps.projects.services.template_import import _normalize_block_list

        out = _normalize_block_list([block_dict])
        self.assertEqual(len(out), 1, "Block was dropped during normalization")
        return out[0]

    def test_cascade_normalizes_with_id_at_props_level(self):
        block = {
            "type": "cascade",
            "props": {
                "id": "test_cascade_a",
                "beats": [
                    {"blocks": [{"type": "paragraph", "content": "Beat 0."}]},
                    {"advance_text": "Continue", "blocks": [{"type": "paragraph", "content": "Beat 1."}]},
                ],
            },
        }
        safe = self._norm_one(block)
        self.assertEqual(safe["type"], "cascade")
        self.assertEqual(safe["props"]["id"], "test_cascade_a")
        self.assertEqual(len(safe["props"]["beats"]), 2)
        self.assertEqual(safe["props"]["beats"][0]["advance_text"], "")
        self.assertEqual(safe["props"]["beats"][1]["advance_text"], "Continue")

    def test_cascade_reads_beats_from_top_level_or_props(self):
        """Replays the 2026-05-03 4-place bug class for cascade."""
        # Form A: beats at top level
        a = {
            "type": "cascade",
            "props": {"id": "ta"},
            "beats": [{"blocks": [{"type": "paragraph", "content": "A"}]}],
        }
        # Form B: beats inside props
        b = {
            "type": "cascade",
            "props": {
                "id": "tb",
                "beats": [{"blocks": [{"type": "paragraph", "content": "B"}]}],
            },
        }
        safe_a = self._norm_one(a)
        safe_b = self._norm_one(b)
        self.assertEqual(len(safe_a["props"]["beats"]), 1)
        self.assertEqual(len(safe_b["props"]["beats"]), 1)
        self.assertEqual(safe_a["props"]["beats"][0]["blocks"][0]["content"], "A")
        self.assertEqual(safe_b["props"]["beats"][0]["blocks"][0]["content"], "B")

    def test_cascade_with_zero_beats_normalizes_to_empty(self):
        block = {"type": "cascade", "props": {"id": "empty", "beats": []}}
        safe = self._norm_one(block)
        self.assertEqual(safe["props"]["beats"], [])

    def test_cascade_beat_passes_through_effects_and_conditions(self):
        block = {
            "type": "cascade",
            "props": {
                "id": "with_fx",
                "beats": [
                    {"blocks": [{"type": "paragraph", "content": "open"}]},
                    {
                        "advance_text": "Cross to him.",
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
                        "effects": [
                            {"targetType": "player", "trait": "corruption", "op": "add", "value": 1}
                        ],
                        "show_when_locked": True,
                        "locked_text": "Hesitate.",
                        "blocks": [{"type": "paragraph", "content": "deeper"}],
                    },
                ],
            },
        }
        safe = self._norm_one(block)
        beat1 = safe["props"]["beats"][1]
        self.assertEqual(beat1["advance_text"], "Cross to him.")
        self.assertIsInstance(beat1["conditions"], dict)
        self.assertEqual(beat1["conditions"]["items"][0]["value"], 25)
        self.assertEqual(beat1["effects"][0]["trait"], "corruption")
        self.assertTrue(beat1["show_when_locked"])
        self.assertEqual(beat1["locked_text"], "Hesitate.")

    def test_cascade_beat_blocks_recursively_normalize(self):
        """Beat blocks should be normalized through the same recursion (group/pool/thought_bubble all valid inside)."""
        block = {
            "type": "cascade",
            "props": {
                "id": "rec",
                "beats": [
                    {
                        "blocks": [
                            {"type": "paragraph", "content": "p1"},
                            {"type": "thought_bubble", "props": {"speaker": "npc_frank"}, "content": "She came."},
                            {
                                "type": "group",
                                "props": {
                                    "conditions": {"version": "1.0", "logic": "AND", "items": []},
                                    "blocks": [{"type": "paragraph", "content": "inner"}],
                                },
                            },
                        ]
                    }
                ],
            },
        }
        safe = self._norm_one(block)
        beat0_blocks = safe["props"]["beats"][0]["blocks"]
        self.assertEqual(len(beat0_blocks), 3)
        self.assertEqual(beat0_blocks[0]["type"], "paragraph")
        self.assertEqual(beat0_blocks[1]["type"], "thought_bubble")
        self.assertEqual(beat0_blocks[2]["type"], "group")
        # Group recursively normalized its inner blocks
        self.assertEqual(beat0_blocks[2]["props"]["blocks"][0]["content"], "inner")


class NestedGroupNormalizationTests(SimpleTestCase):
    """Schema-side: group-inside-group survives _normalize_block_list.

    Regression for the 2026-05-17 fix: the old same-type-skip rule emptied
    any group whose children were sub-groups (→ renderer "No content").
    The Ryan/Jake E8 canvases use exactly this shape (a stage gate wrapping
    flag-gated sub-branch groups).
    """

    def _norm(self, blocks):
        from apps.projects.services.template_import import _normalize_block_list

        return _normalize_block_list(blocks)

    def test_group_inside_group_is_preserved(self):
        """A stage group wrapping two flag-gated sub-branch groups keeps both
        sub-groups AND their leaf grandchildren (the Ryan Stage-0 shape)."""
        stage = {
            "type": "group",
            "props": {
                "conditions": {"version": "1.0", "logic": "AND", "items": [
                    {"type": "trait", "subject": "player",
                     "trait_key": "npc_ryan_stage", "operator": "eq", "value": 0},
                ]},
                "blocks": [
                    {"type": "group", "props": {
                        "conditions": {"version": "1.0", "logic": "AND", "items": [
                            {"type": "flag", "subject": "player",
                             "flag_key": "ryan_help_tier_open", "operator": "is_false"},
                        ]},
                        "blocks": [
                            {"type": "paragraph", "content": "first-time prose"},
                            {"type": "dialog", "props": {"speaker": "npc",
                             "npcId": "npc_ryan"}, "content": "Need somethin'?"},
                        ],
                    }},
                    {"type": "group", "props": {
                        "conditions": {"version": "1.0", "logic": "AND", "items": [
                            {"type": "flag", "subject": "player",
                             "flag_key": "ryan_help_tier_open", "operator": "is_true"},
                        ]},
                        "blocks": [
                            {"type": "paragraph", "content": "default prose"},
                        ],
                    }},
                ],
            },
        }
        out = self._norm([stage])
        self.assertEqual(len(out), 1)
        inner = out[0]["props"]["blocks"]
        # Both sub-branch groups survive (was [] under the old skip rule).
        self.assertEqual(len(inner), 2, "nested sub-groups were dropped")
        self.assertEqual(inner[0]["type"], "group")
        self.assertEqual(inner[1]["type"], "group")
        # Grandchildren leaves intact.
        self.assertEqual(
            inner[0]["props"]["blocks"][0]["content"], "first-time prose")
        self.assertEqual(
            inner[0]["props"]["blocks"][1]["content"], "Need somethin'?")
        self.assertEqual(
            inner[1]["props"]["blocks"][0]["content"], "default prose")

    def test_mixed_flat_and_nested_children_all_survive(self):
        """A group with [paragraph, group, group] keeps the flat leaf too."""
        g = {
            "type": "group",
            "props": {
                "conditions": {"version": "1.0", "logic": "AND", "items": [
                    {"type": "trait", "subject": "player",
                     "trait_key": "x", "operator": "eq", "value": 1}]},
                "blocks": [
                    {"type": "paragraph", "content": "lead"},
                    {"type": "group", "props": {"conditions": {
                        "version": "1.0", "logic": "AND", "items": [
                            {"type": "flag", "subject": "player",
                             "flag_key": "f", "operator": "is_true"}]},
                        "blocks": [{"type": "paragraph", "content": "a"}]}},
                    {"type": "group", "props": {"conditions": {
                        "version": "1.0", "logic": "AND", "items": [
                            {"type": "flag", "subject": "player",
                             "flag_key": "f", "operator": "is_false"}]},
                        "blocks": [{"type": "paragraph", "content": "b"}]}},
                ],
            },
        }
        inner = self._norm([g])[0]["props"]["blocks"]
        self.assertEqual([b["type"] for b in inner],
                         ["paragraph", "group", "group"])
        self.assertEqual(inner[0]["content"], "lead")

    def test_three_level_group_nest_survives_within_cap(self):
        """group→group→group (depth 3) survives; max_depth=4 is the ceiling."""
        leaf = {"type": "paragraph", "content": "deep"}

        def grp(child):
            return {"type": "group", "props": {
                "conditions": {"version": "1.0", "logic": "AND", "items": [
                    {"type": "flag", "subject": "player",
                     "flag_key": "f", "operator": "is_true"}]},
                "blocks": [child]}}

        out = self._norm([grp(grp(grp(leaf)))])
        l1 = out[0]["props"]["blocks"]
        self.assertEqual(l1[0]["type"], "group")
        l2 = l1[0]["props"]["blocks"]
        self.assertEqual(l2[0]["type"], "group")
        l3 = l2[0]["props"]["blocks"]
        self.assertEqual(l3[0]["content"], "deep")

    def test_depth_cap_truncates_pathological_nesting(self):
        """Nesting deeper than max_depth (4) is truncated, not infinite."""
        from apps.projects.services.template_import import _normalize_block_list

        def grp(child):
            return {"type": "group", "props": {
                "conditions": {"version": "1.0", "logic": "AND", "items": [
                    {"type": "flag", "subject": "player",
                     "flag_key": "f", "operator": "is_true"}]},
                "blocks": [child]}}

        deep = {"type": "paragraph", "content": "x"}
        for _ in range(8):  # 8 levels — well past the depth-4 ceiling
            deep = grp(deep)
        out = _normalize_block_list([deep])  # must not raise / recurse forever
        # Walk down; the chain terminates (empty blocks) at the cap.
        node = out[0]
        depth = 0
        while node.get("type") == "group":
            kids = node["props"].get("blocks", [])
            if not kids:
                break
            node = kids[0]
            depth += 1
            self.assertLessEqual(depth, 4, "nesting exceeded max_depth")


class S8ThoughtBubbleNormalizationTests(SimpleTestCase):
    """Schema-side: thought_bubble normalizes as a leaf block (no recursion)."""

    def test_thought_bubble_preserves_speaker_and_content(self):
        from apps.projects.services.template_import import _normalize_block_list

        out = _normalize_block_list(
            [
                {
                    "type": "thought_bubble",
                    "props": {"speaker": "npc_frank"},
                    "content": "She came.",
                }
            ]
        )
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["type"], "thought_bubble")
        self.assertEqual(out[0]["props"]["speaker"], "npc_frank")
        self.assertEqual(out[0]["content"], "She came.")


class S7CascadeGeneratorTests(SimpleTestCase):
    """Generator-side: _render_cascade emits correct SugarCube markup.

    Calls _render_cascade directly on a generator instance with synthetic
    cascade blocks. Avoids the full pipeline so tests stay fast and focused.
    """

    def setUp(self):
        from apps.game_generation.twee_comprehensive.generators.v1 import (
            TweeComprehensiveGeneratorV1,
        )

        self.gen = TweeComprehensiveGeneratorV1()
        # Minimal slug map / npc map so dialog speaker resolution doesn't 500
        self.gen.npc_slug_map = {"npc_frank": "uuid-frank"}
        self.gen.npc_map = {"uuid-frank": {"name": "Frank", "portrait": ""}}
        self.gen.clothing_enabled = False

    def _make_cascade(self, beats):
        return {"type": "cascade", "props": {"id": "test_c", "beats": beats}}

    def test_emits_linkreplace_per_beat(self):
        """Each non-opening beat with advance_text emits a <<linkreplace ...>>."""
        cascade = self._make_cascade([
            {"blocks": [{"type": "paragraph", "content": "open"}]},
            {"advance_text": "Push the door open.", "blocks": [{"type": "paragraph", "content": "second"}]},
            {"advance_text": "Close the door.", "blocks": [{"type": "paragraph", "content": "third"}]},
        ])
        out = self.gen._render_cascade(cascade)
        self.assertIn('<<linkreplace "Push the door open.">>', out)
        self.assertIn('<<linkreplace "Close the door.">>', out)
        # Beat 0 renders unconditionally — its prose appears with no link wrapper.
        self.assertIn("<p>open</p>", out)
        # Cascade ID namespacing
        self.assertIn('id="cascade-test_c-beat-0"', out)
        self.assertIn('id="cascade-test_c-beat-1"', out)

    def test_beat_effects_fire_inside_linkreplace_body(self):
        """Per-beat-effects contract — effects must appear INSIDE <<linkreplace>>...<</linkreplace>>."""
        cascade = self._make_cascade([
            {"blocks": [{"type": "paragraph", "content": "open"}]},
            {
                "advance_text": "Close the door.",
                "effects": [
                    {"targetType": "npc", "npcId": "npc_frank", "trait": "arousal", "op": "add", "value": 2}
                ],
                "blocks": [{"type": "paragraph", "content": "second"}],
            },
        ])
        out = self.gen._render_cascade(cascade)
        # Locate the linkreplace open + close
        lr_open = out.find('<<linkreplace "Close the door.">>')
        lr_close = out.find('<</linkreplace>>', lr_open)
        self.assertGreater(lr_open, -1, "linkreplace not emitted")
        self.assertGreater(lr_close, lr_open, "linkreplace not closed")
        body = out[lr_open:lr_close]
        # The effect script must appear INSIDE the linkreplace body.
        self.assertIn("setup.applyAndNotifyTrait", body)
        self.assertIn('"arousal"', body)
        self.assertIn("2.0", body)  # value (float-cast)
        self.assertIn("setup.showEffectNotification", body)

    def test_conditional_beat_emits_trigger_conditions_wrapper(self):
        """Gated beats wrap the linkreplace in <<if setup.triggerConditionsSatisfied(...)>>."""
        cascade = self._make_cascade([
            {"blocks": [{"type": "paragraph", "content": "open"}]},
            {
                "advance_text": "Cross to him.",
                "conditions": {
                    "version": "1.0",
                    "logic": "AND",
                    "items": [
                        {"type": "trait", "subject": "player", "trait_key": "corruption", "operator": "gte", "value": 25}
                    ],
                },
                "blocks": [{"type": "paragraph", "content": "deeper"}],
            },
        ])
        out = self.gen._render_cascade(cascade)
        self.assertIn("setup.triggerConditionsSatisfied(", out)
        self.assertIn('"trait_key": "corruption"', out)
        self.assertIn('<<if setup.triggerConditionsSatisfied', out)
        self.assertIn('<</if>>', out)

    def test_show_when_locked_emits_else_branch_with_locked_sibling(self):
        cascade = self._make_cascade([
            {"blocks": [{"type": "paragraph", "content": "open"}]},
            {
                "advance_text": "Cross to him.",
                "conditions": {
                    "version": "1.0",
                    "logic": "AND",
                    "items": [
                        {"type": "trait", "subject": "player", "trait_key": "corruption", "operator": "gte", "value": 25}
                    ],
                },
                "show_when_locked": True,
                "locked_text": "Hesitate at the door.",
                "blocks": [{"type": "paragraph", "content": "deeper"}],
            },
        ])
        out = self.gen._render_cascade(cascade)
        self.assertIn('<<else>>', out)
        self.assertIn('Hesitate at the door.', out)
        self.assertIn('class="locked-choice"', out)

    def test_terminal_beat_renders_inline_no_linkreplace(self):
        """Last beat with no advance_text renders blocks inline, no link wrapper."""
        cascade = self._make_cascade([
            {"blocks": [{"type": "paragraph", "content": "open"}]},
            {"advance_text": "Continue.", "blocks": [{"type": "paragraph", "content": "middle"}]},
            {"blocks": [{"type": "paragraph", "content": "terminal"}]},
        ])
        out = self.gen._render_cascade(cascade)
        # Terminal beat content appears
        self.assertIn("<p>terminal</p>", out)
        # But without its own linkreplace wrapper (only 1 linkreplace for the middle beat)
        self.assertEqual(out.count("<<linkreplace"), 1)

    def test_zero_beat_cascade_returns_empty(self):
        cascade = {"type": "cascade", "props": {"id": "empty", "beats": []}}
        self.assertEqual(self.gen._render_cascade(cascade), "")

    def test_thought_bubble_inside_cascade_renders(self):
        cascade = self._make_cascade([
            {
                "blocks": [
                    {"type": "paragraph", "content": "She closes it."},
                    {"type": "thought_bubble", "props": {"speaker": "npc_frank"}, "content": "She came."},
                ]
            },
        ])
        out = self.gen._render_cascade(cascade)
        self.assertIn('class="thought-bubble thought-bubble-npc"', out)
        self.assertIn("💭", out)
        self.assertIn("Frank is thinking", out)
        self.assertIn("She came.", out)


class S8ThoughtBubbleGeneratorTests(SimpleTestCase):
    """Generator-side: thought_bubble dispatches separately from dialog."""

    def setUp(self):
        from apps.game_generation.twee_comprehensive.generators.v1 import (
            TweeComprehensiveGeneratorV1,
        )

        self.gen = TweeComprehensiveGeneratorV1()
        self.gen.npc_slug_map = {"npc_frank": "uuid-frank"}
        self.gen.npc_map = {"uuid-frank": {"name": "Frank", "portrait": ""}}

    def test_npc_thought_bubble_emits_thought_class_and_glyph(self):
        out = self.gen._convert_blocks_to_game_html(
            [{"type": "thought_bubble", "props": {"speaker": "npc_frank"}, "content": "She came."}]
        )
        self.assertIn('class="thought-bubble thought-bubble-npc"', out)
        self.assertIn("💭", out)
        self.assertIn("Frank is thinking", out)

    def test_player_thought_bubble_uses_player_class(self):
        out = self.gen._convert_blocks_to_game_html(
            [{"type": "thought_bubble", "props": {"speaker": "player"}, "content": "I shouldn't be here."}]
        )
        self.assertIn('class="thought-bubble thought-bubble-player"', out)
        self.assertIn("You are thinking", out)
        self.assertIn("I shouldn't be here.", out)


# =============================================================================
# S4 — Threshold notifications on locked actions
# =============================================================================
# Authored 2026-05-06 alongside the bedroom-anchor pilot wiring. RTS source:
# doc 13 §7.4 + doc 22 §11 (NotifyCorruption-style threshold publishing).
# Locked choice / locked cascade-beat sibling renders as a button that fires
# a warning toast publishing the threshold in-character on click.
#
# NB (2026-05-06): An S3 walkthrough-counter discovery pass briefly shipped
# alongside S4 but was reverted same-day — duplicated the auto-rendered goal
# block (Pattern 2, `setup.computeHintGoal`). See git history if revisiting.


class S4ChoiceLockedTextThresholdSchemaTests(SimpleTestCase):
    """S4: schema round-trip for the locked_text_threshold field on choices."""

    def test_choice_locked_text_threshold_round_trips(self):
        """Set field on raw choice dict — round-trips through the parser."""
        from apps.projects.services.template_import import TemplateChoice, _require_str

        # Direct construction
        ch = TemplateChoice(
            text="Cross to him.",
            show_when_locked=True,
            locked_text="Hesitate at the door.",
            locked_text_threshold="I'd need 25 corruption — no clearer way to put it.",
        )
        self.assertEqual(
            ch.locked_text_threshold,
            "I'd need 25 corruption — no clearer way to put it.",
        )

    def test_choice_without_threshold_defaults_to_empty(self):
        from apps.projects.services.template_import import TemplateChoice
        ch = TemplateChoice(text="x")
        self.assertEqual(ch.locked_text_threshold, "")


class S4CascadeBeatLockedTextThresholdNormalizationTests(SimpleTestCase):
    """S4: schema round-trip for the locked_text_threshold field on cascade beats."""

    def test_beat_locked_text_threshold_normalizes(self):
        from apps.projects.services.template_import import _normalize_block_list

        block = {
            "type": "cascade",
            "props": {
                "id": "test_c",
                "beats": [
                    {"blocks": [{"type": "paragraph", "content": "open"}]},
                    {
                        "advance_text": "Cross to him.",
                        "conditions": {
                            "version": "1.0",
                            "logic": "AND",
                            "items": [
                                {"type": "trait", "subject": "player", "trait_key": "corruption", "operator": "gte", "value": 25}
                            ],
                        },
                        "show_when_locked": True,
                        "locked_text": "Hesitate at the door.",
                        "locked_text_threshold": "Need 25 corruption.",
                        "blocks": [{"type": "paragraph", "content": "deep"}],
                    },
                ],
            },
        }
        out = _normalize_block_list([block])
        self.assertEqual(len(out), 1)
        beat1 = out[0]["props"]["beats"][1]
        self.assertEqual(beat1["locked_text_threshold"], "Need 25 corruption.")

    def test_beat_without_threshold_defaults_to_empty_string(self):
        from apps.projects.services.template_import import _normalize_block_list
        block = {
            "type": "cascade",
            "props": {"id": "x", "beats": [{"blocks": [{"type": "paragraph", "content": "p"}]}]},
        }
        out = _normalize_block_list([block])
        self.assertEqual(out[0]["props"]["beats"][0]["locked_text_threshold"], "")


class S4GeneratorEmitsThresholdNotificationTests(SimpleTestCase):
    """S4: generator emits queueGatedNotification + showEffectNotification
    inside the locked sibling button when locked_text_threshold is set."""

    def setUp(self):
        from apps.game_generation.twee_comprehensive.generators.v1 import (
            TweeComprehensiveGeneratorV1,
        )
        self.gen = TweeComprehensiveGeneratorV1()
        self.gen.npc_slug_map = {"npc_frank": "uuid-frank"}
        self.gen.npc_map = {"uuid-frank": {"name": "Frank", "portrait": ""}}
        self.gen.clothing_enabled = False

    def test_cascade_beat_with_threshold_emits_notify_button(self):
        cascade = {"type": "cascade", "props": {"id": "tc", "beats": [
            {"blocks": [{"type": "paragraph", "content": "open"}]},
            {
                "advance_text": "Cross to him.",
                "conditions": {"version": "1.0", "logic": "AND", "items": [
                    {"type": "trait", "subject": "player", "trait_key": "corruption", "operator": "gte", "value": 25}
                ]},
                "show_when_locked": True,
                "locked_text": "Hesitate at the door.",
                "locked_text_threshold": "Need 25 corruption.",
                "blocks": [{"type": "paragraph", "content": "deep"}],
            },
        ]}}
        out = self.gen._render_cascade(cascade)
        # The locked sibling now wraps the label in a <<button>> macro.
        self.assertIn('<<button "Hesitate at the door.">>', out)
        self.assertIn('queueGatedNotification("Need 25 corruption.")', out)
        self.assertIn('setup.showEffectNotification()', out)
        # The plain static span should NOT be the rendering when threshold set
        # — verify by absence of the static-only pattern (just label inside span
        # with no button child).
        self.assertNotIn(
            '<span class="locked-choice" title="Hesitate at the door.">Hesitate at the door.</span>',
            out,
        )

    def test_cascade_beat_without_threshold_falls_back_to_static_span(self):
        cascade = {"type": "cascade", "props": {"id": "tc", "beats": [
            {"blocks": [{"type": "paragraph", "content": "open"}]},
            {
                "advance_text": "Cross to him.",
                "conditions": {"version": "1.0", "logic": "AND", "items": [
                    {"type": "trait", "subject": "player", "trait_key": "corruption", "operator": "gte", "value": 25}
                ]},
                "show_when_locked": True,
                "locked_text": "Hesitate at the door.",
                # No locked_text_threshold
                "blocks": [{"type": "paragraph", "content": "deep"}],
            },
        ]}}
        out = self.gen._render_cascade(cascade)
        # Static span — not the button form.
        self.assertNotIn('queueGatedNotification', out)
        self.assertIn('class="locked-choice"', out)
        self.assertIn('Hesitate at the door.', out)


# =============================================================================
# E17 — Per-hint ready_text override for Pattern 2 ready-frame
# =============================================================================
# Authored 2026-05-06. Lets authors replace the engine-default ready-frame text
# ("All gates cleared. Visit X to seal the moment.") with in-character prose
# per-NPC-per-stage. Engine reads template's ready_text via setup._getReadyHintForNPC.


class E17ReadyTextSchemaTests(SimpleTestCase):
    """Schema round-trip for the ready_text field on hint templates."""

    def test_hint_with_ready_text_round_trips(self):
        from apps.projects.services.template_import import (
            TemplateHintTemplate,
            TemplateHintCondition,
            _serialize_hint_template,
        )

        cond = TemplateHintCondition(
            stage_npc="npc_frank", stage_op="eq", stage_value=3
        )
        tpl = TemplateHintTemplate(
            condition=cond,
            text="He needs me in the office.",
            tip="Office evenings.",
            npc_id="npc_frank",
            auto_goal=True,
            ready_text="Office, after seven. Tonight he'll move the line.",
        )
        out = _serialize_hint_template(tpl)
        self.assertEqual(
            out["ready_text"],
            "Office, after seven. Tonight he'll move the line.",
        )
        self.assertEqual(out["text"], "He needs me in the office.")
        self.assertEqual(out["tip"], "Office evenings.")

    def test_hint_without_ready_text_defaults_empty(self):
        from apps.projects.services.template_import import (
            TemplateHintTemplate,
            _serialize_hint_template,
        )

        tpl = TemplateHintTemplate(text="x", npc_id="npc_y")
        out = _serialize_hint_template(tpl)
        self.assertEqual(out["ready_text"], "")


class E17ReadyTextEngineEmissionTests(TestCase):
    """E17: the engine emits per-template ready_text into the runtime story_arc
    JSON, and setup._getReadyHintForNPC reads it as the override. Verify the
    JSON shape carries the field through + the JS function body references it.
    Uses an in-memory minimal TOML (not a fixture) to keep the test focused."""

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            email="e17-ready-text-test@example.com", password="testpass123"
        )

    def _build_with_ready_text(self):
        """Build a minimal project with a single hint that has ready_text."""
        d = copy.deepcopy(_base_toml())
        d["story_arc"] = {
            "version": "1.0",
            "summary": "test",
            "hints": {
                "stuck_threshold_minutes": 30,
                "hint_style": "observation",
                "templates": [
                    {
                        "text": "He needs me in the office after seven now.",
                        "tip": "Frank's office, weekday evenings.",
                        "ready_text": "Office, after seven. Tonight he'll move the line.",
                        "npc_id": "npc_frank",
                        "auto_goal": True,
                        "condition": {
                            "stage_npc": "npc_frank",
                            "stage_op": "eq",
                            "stage_value": 3,
                        },
                    }
                ],
            },
        }
        # NPC needs npc_frank trait declared (per condition lookup)
        d["player"]["core_traits"]["npc_frank_stage"] = 0
        template = normalize(d)
        result = create_project_from_template(template, str(self.user.id))
        project = Project.objects.get(id=result["project_id"])
        from apps.game_generation.twee_comprehensive.generators.v1 import (
            TweeComprehensiveGeneratorV1,
        )
        gen = TweeComprehensiveGeneratorV1()
        return gen.generate(project)

    def test_ready_text_serialized_into_twee(self):
        twee = self._build_with_ready_text()
        # Author-supplied ready_text must appear in the generated twee
        # (HTML-encoded apostrophe in the JSON string).
        self.assertIn(
            "Office, after seven. Tonight he",
            twee,
            "ready_text override missing from generated twee",
        )
        self.assertIn("move the line", twee)

    def test_engine_synthesizer_reads_ready_text_field(self):
        """The setup._getReadyHintForNPC body must reference tpl.ready_text
        for the override to actually take effect at runtime."""
        twee = self._build_with_ready_text()
        self.assertIn("tpl.ready_text", twee)

    def test_engine_default_fallback_kept_in_synthesizer(self):
        """Backward-compat — the existing default string + fallback path must
        remain so NPCs without ready_text overrides keep working."""
        twee = self._build_with_ready_text()
        # Look for the OR-fallback expression: readyText || ("All gates cleared. ...")
        self.assertIn("All gates cleared. Visit", twee)


# -- arc_closure_flag: terminal-stage flag-resolved Ready / ✓ Complete frame -
#
# 2026-05-10. Adds a third closure pattern alongside the existing two:
#   • next-stage helper exists → engine walks `_findStageSetterCanvas` (legacy)
#   • arc_complete=true → renders ✓ badge unconditionally (2026-05-09)
#   • arc_closure_flag="<flag>" → engine looks up the flag's setter canvas via
#     `_findFlagSetterCanvas` and renders 🔓 Ready (📍+🕒) while the flag is
#     unset, then ✓ Arc complete once the flag flips true.
# Mutex with arc_complete (validated). Lets terminal-stage hints reflect the
# actual consummation moment instead of firing closure on stage entry.
# Doctrine: location/time stay out of narrative copy (text/tip/ready_text);
# the auto-rendered goal block carries them. See plan
# `lets-plan-a-game-wobbly-snail.md` (2026-05-10) and
# memory: `feedback_hint_narrative_no_time_or_location`.


class ArcClosureFlagSchemaTests(SimpleTestCase):
    """Schema round-trip + mutex validation for arc_closure_flag."""

    def test_arc_closure_flag_round_trips(self):
        from apps.projects.services.template_import import (
            TemplateHintTemplate,
            TemplateHintCondition,
            _serialize_hint_template,
        )

        cond = TemplateHintCondition(
            stage_npc="npc_frank", stage_op="eq", stage_value=4
        )
        tpl = TemplateHintTemplate(
            condition=cond,
            text="Upstairs now.",
            npc_id="npc_frank",
            auto_goal=False,
            arc_closure_flag="frank_bedroom_first_done",
        )
        out = _serialize_hint_template(tpl)
        self.assertEqual(out["arc_closure_flag"], "frank_bedroom_first_done")
        self.assertFalse(out["arc_complete"])
        self.assertEqual(out["text"], "Upstairs now.")

    def test_arc_closure_flag_default_empty(self):
        from apps.projects.services.template_import import (
            TemplateHintTemplate,
            _serialize_hint_template,
        )

        tpl = TemplateHintTemplate(text="x", npc_id="npc_y")
        out = _serialize_hint_template(tpl)
        self.assertEqual(out["arc_closure_flag"], "")

    def test_arc_complete_and_arc_closure_flag_mutex_rejected(self):
        d = copy.deepcopy(_base_toml())
        d["npcs"][0]["arc_stages"] = ["s0", "s1"]
        d["player"]["core_traits"]["npc_frank_stage"] = 0
        d["story_arc"] = {
            "version": "1.0",
            "summary": "test",
            "hints": {
                "stuck_threshold_minutes": 30,
                "hint_style": "observation",
                "templates": [
                    {
                        "text": "Both set — should error.",
                        "npc_id": "npc_frank",
                        "auto_goal": False,
                        "arc_complete": True,
                        "arc_closure_flag": "some_flag",
                        "condition": {
                            "stage_npc": "npc_frank",
                            "stage_op": "eq",
                            "stage_value": 1,
                        },
                    }
                ],
            },
        }
        template = normalize(d)
        errors = validate(template)
        # Look for the mutex error message
        joined = " | ".join(errors)
        self.assertIn("arc_complete", joined)
        self.assertIn("arc_closure_flag", joined)
        self.assertIn("mutually exclusive", joined)


class ArcClosureFlagEngineEmissionTests(TestCase):
    """The engine emits arc_closure_flag into the runtime story_arc JSON,
    setup.computeHintGoal references it for the Ready/Complete bifurcation,
    setup._isHintReady references it for the ready_text swap, and
    setup.getStageHintForNPC passes it through on the picker return."""

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            email="arc-closure-flag-test@example.com", password="testpass123"
        )

    def _build_with_arc_closure_flag(self):
        d = copy.deepcopy(_base_toml())
        d["npcs"][0]["arc_stages"] = ["s0", "s1"]
        d["npcs"][0]["flag_keys"] = []
        d["player"]["core_traits"]["npc_frank_stage"] = 0
        d["player"]["flag_keys"] = ["frank_bedroom_first_done"]
        d["story_arc"] = {
            "version": "1.0",
            "summary": "test",
            "hints": {
                "stuck_threshold_minutes": 30,
                "hint_style": "observation",
                "templates": [
                    {
                        "text": "Upstairs now.",
                        "ready_text": "He'll be in his bedroom tonight.",
                        "npc_id": "npc_frank",
                        "auto_goal": False,
                        "arc_closure_flag": "frank_bedroom_first_done",
                        "condition": {
                            "stage_npc": "npc_frank",
                            "stage_op": "eq",
                            "stage_value": 1,
                        },
                    },
                ],
            },
        }
        template = normalize(d)
        result = create_project_from_template(template, str(self.user.id))
        project = Project.objects.get(id=result["project_id"])
        from apps.game_generation.twee_comprehensive.generators.v1 import (
            TweeComprehensiveGeneratorV1,
        )
        gen = TweeComprehensiveGeneratorV1()
        return gen.generate(project)

    def test_arc_closure_flag_serialized_into_twee(self):
        twee = self._build_with_arc_closure_flag()
        # Field name + value both present in the runtime JSON
        self.assertIn("arc_closure_flag", twee)
        self.assertIn("frank_bedroom_first_done", twee)

    def test_compute_hint_goal_branches_on_arc_closure_flag(self):
        twee = self._build_with_arc_closure_flag()
        # Engine reads the field
        self.assertIn("hintObj.arc_closure_flag", twee)
        # Engine resolves the flag via the setter-canvas helper
        self.assertIn("_findFlagSetterCanvas", twee)
        # Both Ready frame and ✓ Arc complete frame remain emitted
        self.assertIn("Ready", twee)
        self.assertIn("Arc complete", twee)

    def test_is_hint_ready_branches_on_arc_closure_flag(self):
        twee = self._build_with_arc_closure_flag()
        # _isHintReady has a closure-flag short-circuit BEFORE auto_goal check
        # (so closure templates with auto_goal=false still get ready_text swap)
        body = twee[twee.find("setup._isHintReady"):]
        cf_idx = body.find("arc_closure_flag")
        ag_idx = body.find("auto_goal === false")
        self.assertGreater(cf_idx, -1, "arc_closure_flag check missing from _isHintReady")
        self.assertGreater(ag_idx, -1, "auto_goal check missing from _isHintReady")
        self.assertLess(cf_idx, ag_idx, "arc_closure_flag must be checked before auto_goal short-circuit")

    def test_get_stage_hint_for_npc_passes_through_arc_closure_flag(self):
        twee = self._build_with_arc_closure_flag()
        # picker.return must include the field — look in the whole twee
        # for the pattern `arc_closure_flag:` (object-literal syntax).
        self.assertIn("arc_closure_flag:", twee)
        # And the picker reads from `picked.arc_closure_flag`
        self.assertIn("picked.arc_closure_flag", twee)


# -- Engine regression: priority-aware NPC portrait selection at locations ---
#
# Bug context (2026-05-06): when two repeatable manual canvases for the same
# NPC at the same location were simultaneously valid (e.g., a tier-2 surface
# and a tier-3 surface gated by a stage flag), setup.renderNpcPortraits picked
# the FIRST canvas in canvasList declaration order — ignoring `priority`.
# Authors who relied on `priority` to disambiguate (per the field's documented
# semantics) were silently routed to the lower-priority canvas. The fix adds
# priority-aware per-NPC dedup to both renderNpcPortraits (portrait grid at
# location) and getNpcsWithCanvasesAtLocation (NPC badges in navigation).
#
# These tests guard against regression of the priority-sort logic in the
# emitted engine code. They use the shared fixture (engine_prd_2026_04_22.toml)
# since the engine functions are invariant across fixtures — what we verify is
# that the generator emits the new sort logic into the engine init block.


class LocationPortraitPrioritySelectionTests(TestCase):
    """Regression tests for priority-aware canvas dedup in setup.renderNpcPortraits
    and setup.getNpcsWithCanvasesAtLocation (v1.py:3577 + 3384)."""

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            email="portrait-priority-test@example.com", password="testpass123"
        )
        with open(FIXTURE_PATH, "rb") as f:
            cls.toml_data = tomli.load(f)

    def _build(self):
        template = normalize(copy.deepcopy(self.toml_data))
        errors = validate(template)
        self.assertEqual(errors, [], f"Fixture should validate clean: {errors}")
        result = create_project_from_template(template, str(self.user.id))
        project = Project.objects.get(id=result["project_id"])
        from apps.game_generation.twee_comprehensive.generators.v1 import (
            TweeComprehensiveGeneratorV1,
        )
        generator = TweeComprehensiveGeneratorV1()
        return generator.generate(project)

    def test_render_npc_portraits_buckets_by_affordability(self):
        """The dedup must collect ALL valid canvases per NPC into
        affordable + blocked buckets before picking the highest priority,
        rather than first-in-canvasList-wins. Post-2026-05-07 refactor:
        affordable bucketing lives in setup.selectNpcPortraitCanvasesForLocation
        (shared with the NEW badge), blocked bucketing stays inline in the
        renderer."""
        twee = self._build()
        # Affordable bucket lives in the shared helper now
        helper_idx = twee.index("setup.selectNpcPortraitCanvasesForLocation = function")
        helper_body = twee[helper_idx : helper_idx + 2000]
        self.assertIn("npcAffordable", helper_body,
            "selectNpcPortraitCanvasesForLocation missing affordable bucket")
        self.assertIn(".push(c)", helper_body,
            "selectNpcPortraitCanvasesForLocation should push canvases into the bucket")
        # Blocked bucket stays in the renderer (only it needs the greyed-out path)
        renderer_idx = twee.index("setup.renderNpcPortraits = function")
        renderer_body = twee[renderer_idx : renderer_idx + 4000]
        self.assertIn("npcBlockedAll", renderer_body,
            "renderNpcPortraits missing blocked bucket (greyed portraits)")
        # Renderer must call the shared helper for the affordable picks
        self.assertIn("setup.selectNpcPortraitCanvasesForLocation(locationId)", renderer_body,
            "renderNpcPortraits must delegate affordable selection to the shared helper")

    def test_render_npc_portraits_picks_highest_priority_per_npc(self):
        """After bucketing, the per-NPC pick must be priority-desc — the
        comparator declaration sortByPriorityDesc must be present and used to
        sort each NPC's bucket before head-pick."""
        twee = self._build()
        idx = twee.index("setup.renderNpcPortraits = function")
        body = twee[idx : idx + 4000]
        self.assertIn("sortByPriorityDesc", body)
        # Comparator body — the standard engine convention for desc sort
        self.assertIn("(b.priority || 0) - (a.priority || 0)", body)

    def test_get_npcs_with_canvases_at_location_sorts_by_priority(self):
        """getNpcsWithCanvasesAtLocation must sort selectCanvasByPriority's
        return value by priority desc before per-NPC dedup, so navigation
        badges match the canvas the player will actually reach when they
        click into the location."""
        twee = self._build()
        idx = twee.index("setup.getNpcsWithCanvasesAtLocation = function")
        body = twee[idx : idx + 1500]
        self.assertIn("availableCanvases.sort", body)
        self.assertIn("(b.priority || 0) - (a.priority || 0)", body)

    def test_priority_sort_comparator_appears_four_times(self):
        """Exact count: the desc-priority comparator must appear in exactly
        four engine functions post-2026-05-07 NEW-badge truth-matching refactor —
            1. setup.selectCanvasByPriority (existing — replay-mode head pick)
            2. setup.getNpcsWithCanvasesAtLocation (nav badge sort)
            3. setup.renderNpcPortraits (blocked-bucket sort — affordable
               sort moved into the shared helper below)
            4. setup.selectNpcPortraitCanvasesForLocation (NEW — shared
               affordable-bucket sort, used by both the renderer and the
               NEW badge)
        Drift in this count means the priority-aware dedup got removed or
        duplicated. Further consolidation refactors must update this."""
        twee = self._build()
        count = twee.count("(b.priority || 0) - (a.priority || 0)")
        self.assertEqual(
            count,
            4,
            f"Expected exactly 4 priority-desc comparators in emitted engine, found {count}",
        )


# -- Engine: dual player-flag-store consolidation onto $flags ---------------
#
# Bug context (2026-05-06): the engine had two separate player-flag stores —
# $flags (canonical, what triggerConditionsSatisfied reads, what every canvas-
# effect helper writes) and $player.flags (vestigial, populated only at game
# init + by ONE legacy direct-Twee-write at the rent eviction passage).
# The dev sidebar displayed BOTH stores, which made debugging impossible —
# someone reading the dev panel could see "frank_restrict_declared = false"
# under "Player Flags" while the engine had it as true under "Story Flags."
# The fix: retire $player.flags. Move per-key defaults to $flags init.
# Replace the rent eviction direct write with the canonical helper. Remove
# the duplicate sidebar section. Add a one-time save-migration block on
# :passagestart for backward-compat with in-progress saves.


class PlayerFlagStoreConsolidationTests(TestCase):
    """Regression tests for the $player.flags retirement (2026-05-06).

    Verifies the Start passage shape, the rent eviction helper call, the
    sidebar single-flag-list, and the migration block in :passagestart.
    All emission-level — same approach as other tests in this file."""

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            email="flag-consolidation-test@example.com", password="testpass123"
        )
        with open(FIXTURE_PATH, "rb") as f:
            cls.toml_data = tomli.load(f)

    def _build(self):
        template = normalize(copy.deepcopy(self.toml_data))
        errors = validate(template)
        self.assertEqual(errors, [], f"Fixture should validate clean: {errors}")
        result = create_project_from_template(template, str(self.user.id))
        project = Project.objects.get(id=result["project_id"])
        from apps.game_generation.twee_comprehensive.generators.v1 import (
            TweeComprehensiveGeneratorV1,
        )
        generator = TweeComprehensiveGeneratorV1()
        return generator.generate(project)

    def _start_passage(self, twee: str) -> str:
        """Slice out the :: Start passage body for shape assertions."""
        idx = twee.index(":: Start")
        rest = twee[idx + 1 :]
        nxt = rest.find("\n:: ")
        return rest[:nxt] if nxt != -1 else rest

    def test_start_passage_does_not_create_player_flags(self):
        """$player init no longer carries a `flags` property — retired in
        favor of the canonical top-level $flags store."""
        twee = self._build()
        start = self._start_passage(twee)
        # The $player set block must not contain a "flags": key. Look for
        # the literal substring used in the init JSON shape.
        self.assertIn("<<set $player = {", start)
        # Find the $player set block
        player_idx = start.index("<<set $player = {")
        player_close = start.index("}>>", player_idx)
        player_block = start[player_idx:player_close + 3]
        self.assertNotIn('"flags":', player_block,
            "$player init should no longer create a flags property")

    def test_start_passage_initializes_flags_with_registered_keys(self):
        """$flags init must include every registered player flag key with
        default false, plus the engine metadata keys (game_started,
        debug_mode). Smoke-check via known TLS flag keys."""
        twee = self._build()
        start = self._start_passage(twee)
        # Find the $flags set block
        idx = start.index("<<set $flags = {")
        close = start.index("}>>", idx)
        flags_block = start[idx:close + 3]
        # Engine metadata keys
        self.assertIn('"game_started": true', flags_block)
        self.assertIn('"debug_mode":', flags_block)
        # A representative registered flag from the engine_prd fixture
        # (the EnginePRDIntegrationTests confirm this fixture has registered
        # flag keys including rent-related ones).
        self.assertIn('"rent_evicted": false', flags_block)

    def test_no_direct_player_flags_writes_in_engine_emission(self):
        """No engine code path should write to $player.flags directly. All
        flag mutations must go through setup.applyAndNotifyFlag /
        applyFlagEffect, which target the canonical $flags store."""
        twee = self._build()
        # The migration block deletes sv.player.flags — that's a removal,
        # not a mutation. Strip it out before scanning so the test catches
        # only "real" writes.
        # Pattern that would match a direct write: $player.flags[...] = ...
        # or $player.flags[...] to ... (Twee macro)
        self.assertNotIn("$player.flags[", twee,
            "No direct $player.flags writes allowed — use setup.applyAndNotifyFlag")
        self.assertNotIn("set $player.flags", twee,
            "No <<set $player.flags...>> Twee macros — retired pattern")

    def test_dev_sidebar_renders_only_one_flag_section(self):
        """FlagsPage must show ONE flag list (Story Flags reading $flags),
        not two. The pre-fix duplicate "Player Flags" section reading
        $player.flags was the diagnostic trap."""
        twee = self._build()
        # FlagsPage passage
        self.assertIn(":: FlagsPage", twee)
        idx = twee.index(":: FlagsPage")
        nxt = twee.index("\n:: ", idx + 1)
        page = twee[idx:nxt]
        self.assertIn("Story Flags", page)
        self.assertNotIn("Player Flags", page,
            "FlagsPage should not contain a duplicate Player Flags section")
        # The trait-panel widget must also read $flags, not $player.flags
        widget_idx = twee.index('id="flags-widget"')
        widget_end = twee.index("</div>", widget_idx + 200)
        widget = twee[widget_idx:widget_end]
        self.assertNotIn("$player.flags", widget)
        self.assertIn("$flags", widget)

    def test_rent_eviction_uses_canonical_helper(self):
        """Rent eviction was the only legacy direct-Twee-write site. After
        consolidation it must use setup.applyAndNotifyFlag like every other
        canvas-effect path."""
        twee = self._build()
        idx = twee.index(":: RentDay_Short")
        nxt = twee.index("\n:: ", idx + 1)
        passage = twee[idx:nxt]
        self.assertIn(
            "setup.applyAndNotifyFlag('player', null, setup.rent_eviction_flag, 'set')",
            passage,
        )

    def test_save_migration_block_in_passagestart_handler(self):
        """In-progress saves made before the consolidation have $player.flags
        populated. The :passagestart hook copies any TRUE values into $flags
        and deletes the legacy property. Idempotent (delete makes the guard
        fail on subsequent runs)."""
        twee = self._build()
        # Locate the :passagestart hook (InfoPageNav script passage)
        hook_idx = twee.index("$(document).on(':passagestart'")
        hook_end = twee.index("});", hook_idx)
        hook = twee[hook_idx:hook_end]
        # Migration must read sv.player.flags, copy to sv.flags, and delete
        self.assertIn("sv.player.flags", hook,
            "Migration block must reference sv.player.flags")
        self.assertIn("delete sv.player.flags", hook,
            "Migration block must delete sv.player.flags after copy")
        self.assertIn("sv.flags[lk] = true", hook,
            "Migration block must write TRUE values to sv.flags")


# -- Engine: runtime "no exits satisfied" diagnostic --------------------------
#
# When a canvas's exit_block has all-conditional choices and zero conditions
# evaluate true at runtime, the engine emits three layered behaviors:
#  (1) console.warn with canvas slug + choices + state snapshot (always)
#  (2) Visible red diagnostic banner with per-choice / per-condition ✓✗
#      (only when $flags.debug_mode is true)
#  (3) [[Continue->return_target]] fallback link (preserved)
#
# Bug context: scene_office_after_crack hit a dead-end on 2026-05-06 when
# Frank.corruption ≥ 25 + frank_office_first_sex_done = false. The pre-fix
# fallback was silent ("No available choices / Continue") and took several
# rounds of console paste-back to identify the trap. This diagnostic makes
# the next dead-end loud + actionable at runtime.


class EngineNoExitsDiagnosticTests(TestCase):
    """Regression tests for the runtime no-exits diagnostic emission
    (v1.py:10072+, 2026-05-06).

    Uses an in-memory minimal TOML built around _base_toml() with a single
    canvas whose exit_block has TWO choices, BOTH conditional. This is the
    shape that triggers the diagnostic at runtime when conditions don't
    cover the full state space."""

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            email="no-exits-diag-test@example.com", password="testpass123"
        )

    def _build_with_all_conditional_canvas(self):
        """Build a minimal project with one canvas whose exit_block has
        only-conditional choices — the shape that triggers the diagnostic."""
        d = copy.deepcopy(_base_toml())
        d["project"]["starting_canvas"] = "test_canvas_all_conditional"
        d["player"]["flag_keys"] = ["test_flag_a", "test_flag_b"]
        d["locations"] = [
            {"id": "loc_test", "name": "Test Location", "description": "test"}
        ]
        d["canvases"] = [
            {
                "id": "test_canvas_all_conditional",
                "name": "Test Canvas — All Conditional",
                "trigger": {
                    "location": "loc_test",
                    "is_repeatable": True,
                    "priority": 5,
                    "is_active": True,
                },
                "nodes": [
                    {
                        "id": "base",
                        "name": "Test node",
                        "blocks": [
                            {"type": "paragraph", "content": "Test content."}
                        ],
                        "exit_block": {
                            "type": "choices",
                            "choices": [
                                {
                                    "text": "Path A — needs flag A.",
                                    "targetType": "trigger",
                                    "time_progression_minutes": 5,
                                    "conditions": {
                                        "version": "1.0",
                                        "logic": "AND",
                                        "items": [
                                            {
                                                "type": "flag",
                                                "subject": "player",
                                                "flag_key": "test_flag_a",
                                                "operator": "is_true",
                                            }
                                        ],
                                    },
                                },
                                {
                                    "text": "Path B — needs flag B.",
                                    "targetType": "trigger",
                                    "time_progression_minutes": 5,
                                    "conditions": {
                                        "version": "1.0",
                                        "logic": "AND",
                                        "items": [
                                            {
                                                "type": "flag",
                                                "subject": "player",
                                                "flag_key": "test_flag_b",
                                                "operator": "is_true",
                                            }
                                        ],
                                    },
                                },
                            ],
                        },
                    }
                ],
            }
        ]
        template = normalize(d)
        errors = validate(template)
        self.assertEqual(errors, [], f"In-memory TOML should validate: {errors}")
        result = create_project_from_template(template, str(self.user.id))
        project = Project.objects.get(id=result["project_id"])
        from apps.game_generation.twee_comprehensive.generators.v1 import (
            TweeComprehensiveGeneratorV1,
        )
        generator = TweeComprehensiveGeneratorV1()
        return generator.generate(project)

    def test_console_warn_emitted_for_all_conditional_canvas(self):
        """When a canvas's exit_block has all-conditional choices, the engine
        must emit a console.warn block to surface dead-ends to anyone with
        DevTools open — including production players (the warn is NOT gated
        on debug_mode, only the visible banner is)."""
        twee = self._build_with_all_conditional_canvas()
        self.assertIn("[engine] no exit choices satisfied", twee,
            "console.warn block must be emitted for all-conditional canvas")
        # The warn payload must include canvas slug + state snapshot
        self.assertIn('canvas: "test_canvas_all_conditional"', twee)
        self.assertIn("flags: State.variables.flags", twee)
        self.assertIn("player_traits: (State.variables.player || {}).core_traits", twee)

    def test_dev_mode_diagnostic_banner_gated_on_flags_debug_mode(self):
        """The visible red diagnostic banner must be wrapped in
        <<if $flags.debug_mode>> so production players never see it. The
        banner walks each condition via setup.triggerConditionsSatisfied
        for per-item ✓/✗ rendering."""
        twee = self._build_with_all_conditional_canvas()
        # CSS class used in stylesheet + once per all-conditional canvas
        diag_class_count = twee.count("engine-diag-no-exits")
        self.assertGreaterEqual(diag_class_count, 2,
            f"Expected ≥2 engine-diag-no-exits refs (stylesheet + canvas div), found {diag_class_count}")
        # Banner must be debug_mode-gated
        self.assertIn("<<if $flags.debug_mode>>", twee)
        # Per-item eval pattern: wrap each condition item in a single-item
        # AND group + call triggerConditionsSatisfied to get pass/fail
        self.assertIn('<<set _single to {version: "1.0", logic: "AND", items: [_it]}>>', twee)
        self.assertIn("<<set _ok to setup.triggerConditionsSatisfied(_single)>>", twee)
        # Pass/fail CSS classes must be referenced inline
        self.assertIn("engine-diag-pass", twee)
        self.assertIn("engine-diag-fail", twee)

    def test_continue_fallback_link_preserved(self):
        """The original [[Continue->return_target]] fallback must remain so
        players are never softlocked when no exit choices satisfy. The
        diagnostic is additive — it doesn't replace the recovery path."""
        twee = self._build_with_all_conditional_canvas()
        idx = twee.index("[engine] no exit choices satisfied")
        slice_after = twee[idx : idx + 4000]
        self.assertIn("No available choices", slice_after)
        self.assertIn("[[Continue->", slice_after,
            "Continue fallback link must be preserved alongside the diagnostic")

    def test_per_canvas_diag_data_carries_choice_text_and_conditions(self):
        """The window._engineNoExitsDiag_<slug> JS variable must carry each
        choice's text and full conditions structure so console.warn + the
        dev banner can introspect them. Verifies JSON injection works."""
        twee = self._build_with_all_conditional_canvas()
        # Slug-suffixed JS global must be assigned
        self.assertIn("window._engineNoExitsDiag_test_canvas_all_conditional", twee)
        # The diag JSON must include both choice texts + their conditions
        # (we constructed two choices with distinctive text)
        self.assertIn("Path A — needs flag A.", twee)
        self.assertIn("Path B — needs flag B.", twee)
        self.assertIn("test_flag_a", twee)
        self.assertIn("test_flag_b", twee)
        # And the JSON shape (text + conditions keys)
        self.assertIn('"text":', twee)
        self.assertIn('"conditions":', twee)


class CascadeExitRoutingTests(TestCase):
    """Regression tests for cascade-aware exit routing
    (v1.py:_render_cascade_tail + _generate_canvas_node_passages, 2026-05-07).

    When a node body contains a multi-beat cascade (one with at least one
    `advance_text` beat), the engine must route the exit-block links INTO
    the deepest advance-beat's <<linkreplace>> body, hidden until the player
    clicks through the cascade. Per RTS Pattern E doctrine. Without this,
    exits render at the passage tail alongside the cascade's first advance
    link — players bypass the cascade and skip the entire emotional beat."""

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            email="cascade-exit-routing-test@example.com", password="testpass123"
        )

    def _build_with_node_body(self, body_blocks, exit_choices=None,
                              starting_canvas="test_canvas_cascade_routing"):
        """Build a minimal project with one canvas, one node containing the
        given body blocks + optional exit choices."""
        if exit_choices is None:
            exit_choices = [
                {"text": "Exit A", "targetType": "trigger",
                 "time_progression_minutes": 5},
                {"text": "Exit B", "targetType": "trigger",
                 "time_progression_minutes": 5},
            ]
        d = copy.deepcopy(_base_toml())
        d["project"]["starting_canvas"] = starting_canvas
        d["player"]["flag_keys"] = ["test_flag_a", "test_flag_b"]
        d["locations"] = [
            {"id": "loc_test", "name": "Test Location", "description": "test"}
        ]
        d["canvases"] = [
            {
                "id": starting_canvas,
                "name": "Cascade Routing Test",
                "trigger": {
                    "location": "loc_test",
                    "is_repeatable": True,
                    "priority": 5,
                    "is_active": True,
                },
                "nodes": [
                    {
                        "id": "base",
                        "name": "Test node",
                        "blocks": body_blocks,
                        "exit_block": {
                            "type": "choices",
                            "choices": exit_choices,
                        },
                    }
                ],
            }
        ]
        template = normalize(d)
        errors = validate(template)
        self.assertEqual(errors, [], f"In-memory TOML should validate: {errors}")
        result = create_project_from_template(template, str(self.user.id))
        project = Project.objects.get(id=result["project_id"])
        from apps.game_generation.twee_comprehensive.generators.v1 import (
            TweeComprehensiveGeneratorV1,
        )
        generator = TweeComprehensiveGeneratorV1()
        return generator.generate(project)

    def _multi_beat_cascade(self, cascade_id="test_cascade_3beat"):
        """Cascade with Beat 0 + Beat 1 advance + Beat 2 terminal."""
        return {
            "type": "cascade",
            "props": {
                "id": cascade_id,
                "beats": [
                    {"blocks": [{"type": "paragraph",
                                 "content": "Beat 0 prose here."}]},
                    {"advance_text": "Continue",
                     "blocks": [{"type": "paragraph",
                                 "content": "Beat 1 prose here."}]},
                    {"blocks": [{"type": "paragraph",
                                 "content": "Beat 2 terminal prose."}]},
                ],
            },
        }

    def test_exits_injected_inside_last_advance_linkreplace(self):
        """Cascade with advance_text → exits land INSIDE the linkreplace body,
        not at the passage tail. The player must click the advance link to
        reveal the exits — preserving the cascade's emotional pacing."""
        twee = self._build_with_node_body([self._multi_beat_cascade()])
        # Find the linkreplace and the exit links — exit must be between
        # <<linkreplace "Continue">> and <</linkreplace>>
        lr_open = twee.find('<<linkreplace "Continue">>')
        self.assertGreater(lr_open, 0,
            "Multi-beat cascade must emit <<linkreplace 'Continue'>>")
        lr_close = twee.find("<</linkreplace>>", lr_open)
        self.assertGreater(lr_close, lr_open,
            "<<linkreplace>> must have a matching close")
        exit_a = twee.find('<<link "Exit A"', lr_open)
        self.assertGreater(exit_a, 0, "Exit A link must be present")
        self.assertLess(exit_a, lr_close,
            "Exit A must be INSIDE the linkreplace body, not after it")
        exit_b = twee.find('<<link "Exit B"', lr_open)
        self.assertGreater(exit_b, 0, "Exit B link must be present")
        self.assertLess(exit_b, lr_close,
            "Exit B must be INSIDE the linkreplace body, not after it")

    def test_exits_emitted_at_tail_for_non_cascade_node(self):
        """Plain-paragraph node body → exits emit at passage tail as before.
        No cascade → no sentinel → no routing path activated. The fix is
        scoped to cascade-bearing nodes only."""
        twee = self._build_with_node_body([
            {"type": "paragraph", "content": "Just plain prose, no cascade."}
        ])
        self.assertNotIn("__CASCADE_EXIT_INJECT__", twee,
            "Sentinel must NEVER appear in rendered output")
        self.assertIn('<<link "Exit A"', twee)
        self.assertIn('<<link "Exit B"', twee)
        # Exits should be inside the passage's <<nobr>> block (no cascade
        # routing happened, so the passage_body emits at tail as today)
        nobr_open = twee.find("<<nobr>>")
        self.assertGreater(nobr_open, 0)
        exit_a = twee.find('<<link "Exit A"', nobr_open)
        self.assertGreater(exit_a, nobr_open)

    def test_exits_emitted_at_tail_for_single_beat_cascade(self):
        """Cascade with only Beat 0 (no advance_text anywhere) is a degenerate
        case — last_advance_idx == -1 → no sentinel planted → exits emit at
        passage tail as before. No regression."""
        single_beat_cascade = {
            "type": "cascade",
            "props": {
                "id": "test_singlebeat",
                "beats": [
                    {"blocks": [{"type": "paragraph",
                                 "content": "Only Beat 0, no advances."}]},
                ],
            },
        }
        twee = self._build_with_node_body([single_beat_cascade])
        self.assertNotIn("__CASCADE_EXIT_INJECT__", twee,
            "Single-beat cascade must NOT plant the sentinel")
        # No <<linkreplace>> emitted (no advance beats)
        self.assertNotIn("<<linkreplace ", twee)
        # Exits emitted at tail
        self.assertIn('<<link "Exit A"', twee)
        self.assertIn('<<link "Exit B"', twee)

    def test_no_exits_diagnostic_travels_with_exits_into_cascade(self):
        """When a cascade-bearing node has all-conditional exits that fail
        under fresh state, the no-exits runtime diagnostic must travel WITH
        the exits into the cascade body — fires after click-through, not on
        initial render. Confirms the diagnostic emission isn't lost during
        the sentinel substitution."""
        all_conditional_exits = [
            {
                "text": "Path A — needs flag A.",
                "targetType": "trigger",
                "time_progression_minutes": 5,
                "conditions": {
                    "version": "1.0", "logic": "AND",
                    "items": [
                        {"type": "flag", "subject": "player",
                         "flag_key": "test_flag_a", "operator": "is_true"}
                    ],
                },
            },
            {
                "text": "Path B — needs flag B.",
                "targetType": "trigger",
                "time_progression_minutes": 5,
                "conditions": {
                    "version": "1.0", "logic": "AND",
                    "items": [
                        {"type": "flag", "subject": "player",
                         "flag_key": "test_flag_b", "operator": "is_true"}
                    ],
                },
            },
        ]
        twee = self._build_with_node_body(
            [self._multi_beat_cascade()],
            exit_choices=all_conditional_exits,
        )
        # No-exits diagnostic must be inside the linkreplace body
        lr_open = twee.find('<<linkreplace "Continue">>')
        lr_close = twee.find("<</linkreplace>>", lr_open)
        warn_pos = twee.find("[engine] no exit choices satisfied")
        self.assertGreater(warn_pos, lr_open,
            "Diagnostic must be inside the cascade's linkreplace body")
        self.assertLess(warn_pos, lr_close,
            "Diagnostic must be inside the cascade, not at passage tail")
        # Continue fallback also routed inside
        continue_pos = twee.find("[[Continue->", lr_open)
        self.assertGreater(continue_pos, lr_open)
        self.assertLess(continue_pos, lr_close)

    def test_sentinel_string_never_leaks_to_rendered_twee(self):
        """The sentinel string must NEVER appear in the rendered Twee output.
        If it does, the substitution failed for some path and that path will
        ship a literal HTML comment containing our internal marker — visible
        to anyone who view-sources the page."""
        twee = self._build_with_node_body([self._multi_beat_cascade()])
        self.assertNotIn("__CASCADE_EXIT_INJECT__", twee,
            "Sentinel string leaked into rendered output — substitution failed")


class CascadePatternCExitRoutingTests(TestCase):
    """P7 audit fix tests (2026-05-12) — Pattern C cascade exit-routing.

    When a cascade has any beat with non-empty `conditions` (gated beat),
    the cascade plants the SAFE sentinel instead of the STANDARD one. The
    substitution branch in _generate_canvas_node_passages must:
    - Detect SAFE sentinel anywhere in node_content
    - Strip both SAFE + STANDARD sentinels (no splice)
    - Keep passage_body INTACT so exits render at passage bottom

    Reason: a runtime gate failure terminates the cascade. With sentinel
    inside the gated linkreplace body, gate-fail = sentinel never renders =
    exits never appear. Bottom-of-passage exit fallback prevents stuck players.

    RTS-aligned: scenes with mid-cascade gates render exits at passage bottom
    (RTS PeepBrotherSex pattern, doc 21 Pattern C / doc 28 §LANE 2 🟡 #2)."""

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            email="cascade-pattern-c-test@example.com", password="testpass123"
        )

    def _build_with_node_body(self, body_blocks, exit_choices=None,
                              starting_canvas="test_canvas_pattern_c"):
        """Build a minimal project with one canvas, one node containing the
        given body blocks + optional exit choices."""
        if exit_choices is None:
            exit_choices = [
                {"text": "Exit A", "targetType": "trigger",
                 "time_progression_minutes": 5},
                {"text": "Exit B", "targetType": "trigger",
                 "time_progression_minutes": 5},
            ]
        d = copy.deepcopy(_base_toml())
        d["project"]["starting_canvas"] = starting_canvas
        d["player"]["flag_keys"] = ["test_flag"]
        d["locations"] = [
            {"id": "loc_test", "name": "Test Location", "description": "test"}
        ]
        d["canvases"] = [
            {
                "id": starting_canvas,
                "name": "Pattern C Test",
                "trigger": {
                    "location": "loc_test",
                    "is_repeatable": True,
                    "priority": 5,
                    "is_active": True,
                },
                "nodes": [
                    {
                        "id": "base",
                        "name": "Test node",
                        "blocks": body_blocks,
                        "exit_block": {
                            "type": "choices",
                            "choices": exit_choices,
                        },
                    }
                ],
            }
        ]
        template = normalize(d)
        errors = validate(template)
        self.assertEqual(errors, [], f"Validation errors: {errors}")
        result = create_project_from_template(template, str(self.user.id))
        project = Project.objects.get(id=result["project_id"])
        from apps.game_generation.twee_comprehensive.generators.v1 import (
            TweeComprehensiveGeneratorV1,
        )
        generator = TweeComprehensiveGeneratorV1()
        return generator.generate(project)

    def _gated_cascade(self):
        """Cascade with one gated beat (Beat 2). Beat 1 is unconditional advance,
        Beat 2 is gated, Beat 3 is terminal. last_advance_idx = 2 (the gated beat)."""
        return {
            "type": "cascade",
            "props": {
                "id": "test_pattern_c_cascade",
                "beats": [
                    # Beat 0 — opens
                    {"blocks": [
                        {"type": "paragraph", "content": "Setup beat opens."}
                    ]},
                    # Beat 1 — unconditional advance
                    {"advance_text": "Advance one.", "blocks": [
                        {"type": "paragraph", "content": "Beat 1 prose."}
                    ]},
                    # Beat 2 — GATED on test_flag (last_advance_idx)
                    {
                        "advance_text": "Advance two.",
                        "conditions": {
                            "version": "1.0",
                            "logic": "AND",
                            "items": [
                                {"type": "flag", "subject": "player",
                                 "flag_key": "test_flag", "operator": "is_true"},
                            ],
                        },
                        "show_when_locked": True,
                        "locked_text": "Wait for the right moment.",
                        "locked_text_threshold": "I'd want to be different first.",
                        "blocks": [
                            {"type": "paragraph", "content": "Beat 2 gated prose."}
                        ],
                    },
                    # Beat 3 — terminal (no advance)
                    {"blocks": [
                        {"type": "paragraph", "content": "Terminal beat closes."}
                    ]},
                ],
            },
        }

    def _ungated_cascade(self):
        """Cascade with NO gated beats — should plant STANDARD sentinel."""
        return {
            "type": "cascade",
            "props": {
                "id": "test_ungated_cascade",
                "beats": [
                    {"blocks": [{"type": "paragraph", "content": "Open."}]},
                    {"advance_text": "Advance.", "blocks": [
                        {"type": "paragraph", "content": "Mid."}
                    ]},
                    {"blocks": [{"type": "paragraph", "content": "End."}]},
                ],
            },
        }

    def test_pattern_c_cascade_uses_safe_sentinel_path(self):
        """Cascade with a gated beat: substitution should NOT splice (no inline
        exits inside cascade) AND passage_body should remain so exits render at
        passage bottom."""
        twee = self._build_with_node_body([self._gated_cascade()])

        # Both sentinels stripped from output
        self.assertNotIn("__CASCADE_EXIT_INJECT_SAFE__", twee,
            "SAFE sentinel leaked into rendered output")
        self.assertNotIn("__CASCADE_EXIT_INJECT__", twee,
            "STANDARD sentinel leaked into rendered output")

        # Exit choices DO appear at passage bottom (passage_body kept intact)
        self.assertIn("Exit A", twee, "Exit A missing — passage_body cleared incorrectly")
        self.assertIn("Exit B", twee, "Exit B missing — passage_body cleared incorrectly")

        # Locked-sibling button rendered for gate-fail UX
        self.assertIn("Wait for the right moment.", twee,
            "Locked sibling label missing")
        self.assertIn("queueGatedNotification", twee,
            "Locked sibling threshold-notification helper not invoked")

    def test_ungated_cascade_keeps_standard_inline_splice(self):
        """Regression — ungated cascade should still use STANDARD sentinel
        (exits spliced inside cascade body, passage_body cleared). This is the
        existing pre-P7 behavior; P7 fix must not break it."""
        twee = self._build_with_node_body([self._ungated_cascade()])

        # No raw sentinels in output (substitution succeeded for STANDARD)
        self.assertNotIn("__CASCADE_EXIT_INJECT__", twee,
            "STANDARD sentinel leaked — splice failed")

        # Exits present (spliced inside cascade)
        self.assertIn("Exit A", twee)
        self.assertIn("Exit B", twee)

    def test_mixed_node_body_safe_takes_precedence(self):
        """Multi-cascade node body: one cascade gated, one not. SAFE sentinel
        from the gated cascade should take precedence — both sentinels stripped,
        passage_body kept intact (bottom exits)."""
        twee = self._build_with_node_body([
            self._ungated_cascade(),
            self._gated_cascade(),
        ])

        # Both sentinels gone
        self.assertNotIn("__CASCADE_EXIT_INJECT_SAFE__", twee)
        self.assertNotIn("__CASCADE_EXIT_INJECT__", twee)

        # Exits at passage bottom (kept intact via SAFE-precedence path)
        self.assertIn("Exit A", twee)
        self.assertIn("Exit B", twee)


class LocationNewBadgeTruthMatchingTests(TestCase):
    """Regression tests for the NEW badge truth-matching refactor
    (v1.py:locationHasNewCanvases, 2026-05-07).

    Before the refactor, the badge fired for any unvisited canvas in
    selectCanvasByPriority's output — which diverged from what the
    location page actually routes to (auto-fire / NPC portrait / solo
    activity). The fix extracts the three routing-path selections into
    pure helpers and rebuilds the badge to ask the same questions the
    renderers do, so the badge can't promise content the player can't
    reach from the location screen at the current state."""

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            email="new-badge-truth-test@example.com", password="testpass123"
        )

    def _build_minimal(self):
        """Build a minimal project just to get the engine JS emitted —
        the badge logic lives in the engine setup script, not in any
        canvas-specific code, so a one-canvas project is enough to inspect
        the helper definitions."""
        d = copy.deepcopy(_base_toml())
        d["project"]["starting_canvas"] = "test_canvas"
        d["locations"] = [
            {"id": "loc_test", "name": "Test", "description": "test"}
        ]
        d["canvases"] = [
            {
                "id": "test_canvas",
                "name": "Test",
                "trigger": {
                    "location": "loc_test",
                    "is_repeatable": True,
                    "priority": 5,
                    "is_active": True,
                },
                "nodes": [
                    {
                        "id": "base",
                        "name": "Test",
                        "blocks": [{"type": "paragraph", "content": "."}],
                        "exit_block": {
                            "type": "choices",
                            "choices": [
                                {"text": "Out", "targetType": "trigger",
                                 "time_progression_minutes": 5},
                            ],
                        },
                    }
                ],
            }
        ]
        template = normalize(d)
        errors = validate(template)
        self.assertEqual(errors, [], f"In-memory TOML should validate: {errors}")
        result = create_project_from_template(template, str(self.user.id))
        project = Project.objects.get(id=result["project_id"])
        from apps.game_generation.twee_comprehensive.generators.v1 import (
            TweeComprehensiveGeneratorV1,
        )
        generator = TweeComprehensiveGeneratorV1()
        return generator.generate(project)

    def test_three_pure_selectors_defined(self):
        """The three pure-selection helpers must exist in the emitted engine.
        These are the single source of truth for what content the location
        page will actually deliver via each routing path."""
        twee = self._build_minimal()
        self.assertIn("setup.selectAutoFireCanvasForLocation = function", twee,
            "Auto-fire selector helper missing")
        self.assertIn("setup.selectNpcPortraitCanvasesForLocation = function", twee,
            "NPC portrait selector helper missing")
        self.assertIn("setup.selectSoloActivityCanvasesForLocation = function", twee,
            "Solo activity selector helper missing")

    def test_badge_uses_all_three_selectors(self):
        """The badge function must consult all three routing paths to decide
        whether unvisited content is reachable. Without this, the badge
        re-diverges from what the renderers route to."""
        twee = self._build_minimal()
        idx = twee.index("setup.locationHasNewCanvases = function")
        body = twee[idx : idx + 2000]
        self.assertIn("setup.selectAutoFireCanvasForLocation(locationId)", body,
            "Badge must consult auto-fire path")
        self.assertIn("setup.selectNpcPortraitCanvasesForLocation(locationId)", body,
            "Badge must consult NPC portrait path")
        self.assertIn("setup.selectSoloActivityCanvasesForLocation(locationId)", body,
            "Badge must consult solo activity path")
        # And it must guard each pick with isCanvasNew — otherwise the badge
        # would fire for any reachable canvas, visited or not.
        self.assertGreaterEqual(body.count("setup.isCanvasNew"), 3,
            "Badge must call isCanvasNew on each routing path's pick")

    def test_badge_no_longer_uses_selectCanvasByPriority(self):
        """selectCanvasByPriority's tier-progression logic returned multiple
        canvases (lowest unvisited per activity-name group), which fired
        NEW for any of them — even when the actual NPC-portrait click would
        route to a different (already-visited) canvas. The new badge must
        NOT use selectCanvasByPriority. Other call sites (e.g.
        getNpcsWithCanvasesAtLocation) keep using it — that's fine."""
        twee = self._build_minimal()
        idx = twee.index("setup.locationHasNewCanvases = function")
        end = twee.index("};", idx)
        body = twee[idx : end + 2]
        self.assertNotIn("selectCanvasByPriority", body,
            "Badge must not call selectCanvasByPriority — was the source of the truth-mismatch")

    def test_npc_portrait_selector_excludes_cost_blocked(self):
        """Cost-blocked portraits route to a cost-gate passage, not playable
        content. They must NOT contribute to NEW. The selector body must
        exclude them via checkCostsAffordable."""
        twee = self._build_minimal()
        idx = twee.index("setup.selectNpcPortraitCanvasesForLocation = function")
        body = twee[idx : idx + 2000]
        self.assertIn("checkCostsAffordable", body,
            "NPC portrait selector must exclude cost-blocked picks")

    def test_solo_activity_selector_excludes_cost_blocked_and_cooldown(self):
        """Same rationale for solo: blocked + cooldown picks lead to gates,
        not playable content. Selector must filter both."""
        twee = self._build_minimal()
        idx = twee.index("setup.selectSoloActivityCanvasesForLocation = function")
        body = twee[idx : idx + 2000]
        self.assertIn("checkCostsAffordable", body,
            "Solo selector must exclude cost-blocked picks")
        self.assertIn("canTriggerActivity", body,
            "Solo selector must exclude cooldown-blocked picks via canTriggerActivity")

    def test_renderers_delegate_to_shared_selectors(self):
        """All three renderers must delegate their selection step to the
        shared helpers. Without this guarantee, the helpers and the
        renderers can drift, re-introducing the badge mismatch."""
        twee = self._build_minimal()
        # getStoryCanvasRedirect → selectAutoFireCanvasForLocation
        idx = twee.index("setup.getStoryCanvasRedirect = function")
        end = twee.index("};", idx)
        body = twee[idx : end + 2]
        self.assertIn("setup.selectAutoFireCanvasForLocation(locationId)", body,
            "getStoryCanvasRedirect must use the shared auto-fire selector")
        # renderNpcPortraits → selectNpcPortraitCanvasesForLocation
        idx = twee.index("setup.renderNpcPortraits = function")
        body = twee[idx : idx + 4000]
        self.assertIn("setup.selectNpcPortraitCanvasesForLocation(locationId)", body,
            "renderNpcPortraits must use the shared NPC portrait selector")
        # renderSoloActivities → selectSoloActivityCanvasesForLocation
        idx = twee.index("setup.renderSoloActivities = function")
        body = twee[idx : idx + 3000]
        self.assertIn("setup.selectSoloActivityCanvasesForLocation(locationId)", body,
            "renderSoloActivities must use the shared solo selector")


class RandomRangeEffectValueTests(SimpleTestCase):
    """Engine extension: effect.value accepts either a static number (current
    behavior, byte-equivalent) or a random-range dict
    ``{type: "random", min: N, max: M}`` that emits an inclusive integer-random
    JS expression.

    Source spec: ``28th_april_TLS_Phase2_Redesign/23_Location_Menu_Sex_Loop_Hybrid.md`` §6
    (sex-loop hub per-action pleasure mutations need varied per-play deltas
    per the Shady Deals design lift).

    Helper: ``v1.py:_resolve_effect_value(val)`` — used by all 4 emit sites
    (cascade beat path + choice-effect path + inline trait-effect helper).
    """

    def setUp(self):
        from apps.game_generation.twee_comprehensive.generators.v1 import (
            TweeComprehensiveGeneratorV1,
        )

        self.gen = TweeComprehensiveGeneratorV1()
        # Minimal stubs so dialog/effect resolution doesn't 500 in cascade tests
        self.gen.npc_slug_map = {"npc_frank": "uuid-frank"}
        self.gen.npc_map = {"uuid-frank": {"name": "Frank", "portrait": ""}}
        self.gen.clothing_enabled = False

    # ── Helper unit tests (1-6 + 10): _resolve_effect_value ────────────────

    def test_1_static_numeric_value_unchanged(self):
        """value=5 still emits "5.0" — backwards-compat guarantee."""
        self.assertEqual(self.gen._resolve_effect_value(5), "5.0")
        self.assertEqual(self.gen._resolve_effect_value(0), "0.0")
        self.assertEqual(self.gen._resolve_effect_value(-3), "-3.0")
        self.assertEqual(self.gen._resolve_effect_value(2.5), "2.5")

    def test_2_random_range_emits_math_random_expression(self):
        """value={random, min=3, max=5} → (Math.floor(Math.random()*3)+3).
        Span = max - min + 1 = 3 (inclusive)."""
        out = self.gen._resolve_effect_value({"type": "random", "min": 3, "max": 5})
        self.assertEqual(out, "(Math.floor(Math.random() * 3) + 3)")

    def test_3_random_range_min_equals_max_emits_constant_expression(self):
        """Edge case: min == max yields span=1, expression always evaluates to min.
        Degenerate but valid (author may write {5,5} as a placeholder)."""
        out = self.gen._resolve_effect_value({"type": "random", "min": 5, "max": 5})
        self.assertEqual(out, "(Math.floor(Math.random() * 1) + 5)")

    def test_4_invalid_value_dict_type_raises(self):
        """Unknown random type (e.g. 'gaussian') raises ValueError."""
        with self.assertRaises(ValueError) as ctx:
            self.gen._resolve_effect_value({"type": "gaussian", "min": 0, "max": 1})
        self.assertIn("'gaussian'", str(ctx.exception))

    def test_5_random_range_missing_min_raises(self):
        """Missing min field → ValueError."""
        with self.assertRaises(ValueError) as ctx:
            self.gen._resolve_effect_value({"type": "random", "max": 5})
        self.assertIn("min", str(ctx.exception).lower())

    def test_6_random_range_min_greater_than_max_raises(self):
        """min > max is an authoring error → ValueError."""
        with self.assertRaises(ValueError) as ctx:
            self.gen._resolve_effect_value({"type": "random", "min": 10, "max": 3})
        self.assertIn("min", str(ctx.exception).lower())
        self.assertIn("max", str(ctx.exception).lower())

    def test_10_bool_value_raises(self):
        """Python isinstance(True, int) is True — without an explicit bool guard,
        value=true would silently emit "1.0". The helper rejects bools so authoring
        mistakes surface as render errors."""
        with self.assertRaises(ValueError) as ctx_t:
            self.gen._resolve_effect_value(True)
        self.assertIn("bool", str(ctx_t.exception).lower())
        with self.assertRaises(ValueError) as ctx_f:
            self.gen._resolve_effect_value(False)
        self.assertIn("bool", str(ctx_f.exception).lower())

    # ── Integration tests (7-9): real render paths use the helper ─────────

    def test_7_random_range_in_cascade_beat_effect(self):
        """Full cascade-with-random-beat-effect via _render_cascade — confirms
        the helper hooks up at the cascade emit path (lines 10076 + 10141)."""
        cascade = {
            "type": "cascade",
            "props": {
                "id": "test_random_cascade",
                "beats": [
                    {"blocks": [{"type": "paragraph", "content": "open"}]},
                    {
                        "advance_text": "Push.",
                        "effects": [
                            {
                                "targetType": "player",
                                "trait": "loop_npc_pleasure",
                                "op": "add",
                                "value": {"type": "random", "min": 3, "max": 5},
                            }
                        ],
                        "blocks": [{"type": "paragraph", "content": "second"}],
                    },
                ],
            },
        }
        out = self.gen._render_cascade(cascade)
        # Locate the linkreplace body
        lr_open = out.find('<<linkreplace "Push.">>')
        lr_close = out.find('<</linkreplace>>', lr_open)
        self.assertGreater(lr_open, -1, "linkreplace not emitted")
        body = out[lr_open:lr_close]
        # Helper output appears INSIDE the linkreplace body
        self.assertIn("setup.applyAndNotifyTrait", body)
        self.assertIn('"loop_npc_pleasure"', body)
        self.assertIn("(Math.floor(Math.random() * 3) + 3)", body)

    def test_8_emit_sites_count_matches_plan(self):
        """The plan asserts exactly 4 emit sites use _resolve_effect_value(val).
        This static-source test catches the 'missed an emit site' regression.
        If a future change adds another applyAndNotifyTrait emission with a raw
        float(val) instead of going through the helper, this test fires."""
        from apps.game_generation.twee_comprehensive.generators import v1 as v1_module
        import inspect
        src = inspect.getsource(v1_module)
        helper_call_count = src.count("self._resolve_effect_value(val)")
        # 4 emission sites + the helper definition (whose docstring also references it):
        # we count inside applyAndNotifyTrait emit contexts, NOT the helper def itself.
        # Tightest assertion: count of "applyAndNotifyTrait(...{self._resolve_effect_value(val)}..."
        import re
        emit_pattern = re.compile(
            r"applyAndNotifyTrait\([^)]*\{self\._resolve_effect_value\(val\)\}",
            re.DOTALL,
        )
        emit_count = len(emit_pattern.findall(src))
        self.assertEqual(
            emit_count, 4,
            f"Expected exactly 4 emit sites using _resolve_effect_value(val); "
            f"found {emit_count}. Either an emit site lost the helper (regression) "
            f"or a new emit site was added without the helper (regression)."
        )
        # Sanity: zero raw float(val) emissions remain
        raw_pattern = re.compile(
            r"applyAndNotifyTrait\([^)]*\{float\(val\)\}",
            re.DOTALL,
        )
        raw_count = len(raw_pattern.findall(src))
        self.assertEqual(
            raw_count, 0,
            f"Found {raw_count} raw 'float(val)' applyAndNotifyTrait emissions; "
            f"all should go through _resolve_effect_value(val)."
        )

    def test_9_random_range_composes_with_clamp_and_cap(self):
        """Effect with random-range value + clamp + cap emits all three correctly.
        clamp/cap parameters are unaffected by the value swap — they're emitted
        alongside the helper-resolved expression in the same applyAndNotifyTrait call."""
        effects = [
            {
                "targetType": "player",
                "trait": "loop_npc_pleasure",
                "op": "add",
                "value": {"type": "random", "min": 3, "max": 5},
                "clamp": True,
                "cap": 50,
            }
        ]
        out = self.gen._emit_trait_effects_inline(effects, context="test_9")
        # Random-range expression emitted
        self.assertIn("(Math.floor(Math.random() * 3) + 3)", out)
        # Clamp + cap emitted alongside, unchanged
        self.assertIn(", true, 50)", out)
        # Full call shape preserved
        self.assertIn(
            'setup.applyAndNotifyTrait("player", null, "loop_npc_pleasure", "add", '
            '(Math.floor(Math.random() * 3) + 3), true, 50)',
            out,
        )


# ─── PRD 25 — Lane 3 dispatcher substitution ─────────────────────────────────
#
# Schema round-trip + validator + engine emission tests for the substitutions
# field on TemplateTrigger. See plan `lets-plan-a-game-wobbly-snail.md` Pass 5
# and `28th_april_TLS_Phase2_Redesign/25_Lane_3_Dispatcher_Substitution_PRD.md`.


def _toml_with_substitutions(rules=None, substitution_only=False, target_canvas_extra=None):
    """Build a minimal TOML dict with two canvases:
       - parent_canvas: has the substitutions trigger
       - target_canvas: the substitution target (matches rule's target_canvas_id)
    """
    if rules is None:
        rules = [{"target_canvas_id": "target_canvas", "chance": 0.5}]
    target = {
        "id": "target_canvas",
        "name": "Substitution Target",
        "description": "x",
        "trigger": {
            "location": "loc_test",
            "is_repeatable": True,
            "priority": 5,
            "is_active": True,
            "substitution_only": substitution_only,
        },
        "nodes": [
            {
                "id": "base",
                "name": "Target node",
                "blocks": [{"type": "paragraph", "content": "Substituted content."}],
                "exit_block": {"type": "location", "config": {"destinationType": "trigger"}},
            }
        ],
    }
    if target_canvas_extra:
        target.update(target_canvas_extra)
    d = _base_toml()
    d["project"]["starting_canvas"] = "parent_canvas"
    d["locations"] = [
        {"id": "loc_test", "name": "Test Location", "description": "test"}
    ]
    d["canvases"] = [
        {
            "id": "parent_canvas",
            "name": "Parent Canvas",
            "description": "x",
            "trigger": {
                "location": "loc_test",
                "is_repeatable": True,
                "priority": 5,
                "is_active": True,
                "substitutions": rules,
            },
            "nodes": [
                {
                    "id": "base",
                    "name": "Parent node",
                    "blocks": [{"type": "paragraph", "content": "Parent content."}],
                    "exit_block": {"type": "location", "config": {"destinationType": "trigger"}},
                }
            ],
        },
        target,
    ]
    return d


class SubstitutionsRoundTripTests(SimpleTestCase):
    """PRD 25 §4 — schema round-trip for substitutions + substitution_only fields."""

    def test_substitution_round_trips(self):
        """Parser preserves target_canvas_id, chance, conditions on each rule."""
        rules = [
            {
                "target_canvas_id": "target_canvas",
                "chance": 0.33,
                "conditions": {
                    "version": "1.0",
                    "logic": "AND",
                    "items": [
                        {"type": "flag", "subject": "player",
                         "flag_key": "frank_caught", "operator": "is_true"}
                    ],
                },
            }
        ]
        d = _toml_with_substitutions(rules=rules)
        template = normalize(d)
        parent = next(c for c in template.canvases if c.id == "parent_canvas")
        self.assertEqual(len(parent.trigger.substitutions), 1)
        rule = parent.trigger.substitutions[0]
        self.assertEqual(rule["target_canvas_id"], "target_canvas")
        self.assertEqual(rule["chance"], 0.33)
        self.assertIsNotNone(rule["conditions"])
        self.assertEqual(rule["conditions"]["items"][0]["flag_key"], "frank_caught")

    def test_substitution_default_empty(self):
        """Canvas without substitutions field gets [] default."""
        d = _toml_with_substitutions()
        # Remove the substitutions from the parent
        d["canvases"][0]["trigger"].pop("substitutions", None)
        template = normalize(d)
        parent = next(c for c in template.canvases if c.id == "parent_canvas")
        self.assertEqual(parent.trigger.substitutions, [])

    def test_substitution_only_default_false(self):
        """substitution_only flag absent → defaults to False."""
        d = _toml_with_substitutions()
        # Remove the field
        d["canvases"][1]["trigger"].pop("substitution_only", None)
        template = normalize(d)
        target = next(c for c in template.canvases if c.id == "target_canvas")
        self.assertFalse(target.trigger.substitution_only)

    def test_substitution_only_true_persists(self):
        """substitution_only = True is preserved through parsing."""
        d = _toml_with_substitutions(substitution_only=True)
        template = normalize(d)
        target = next(c for c in template.canvases if c.id == "target_canvas")
        self.assertTrue(target.trigger.substitution_only)


class SubstitutionsValidatorTests(SimpleTestCase):
    """PRD 25 §4.3 — validator rejects bad inputs + warns on conflicts."""

    def test_validator_rejects_unknown_target_canvas_id(self):
        rules = [{"target_canvas_id": "nonexistent_canvas", "chance": 0.5}]
        d = _toml_with_substitutions(rules=rules)
        template = normalize(d)
        errors = validate(template)
        self.assertTrue(
            any("nonexistent_canvas" in e and "does not match any canvas" in e for e in errors),
            f"Expected validator to reject unknown target_canvas_id; errors={errors}",
        )

    def test_validator_rejects_chance_out_of_range_high(self):
        rules = [{"target_canvas_id": "target_canvas", "chance": 1.5}]
        d = _toml_with_substitutions(rules=rules)
        template = normalize(d)
        errors = validate(template)
        self.assertTrue(
            any("chance" in e and "[0.0, 1.0]" in e for e in errors),
            f"Expected validator to reject chance > 1.0; errors={errors}",
        )

    def test_validator_rejects_chance_negative(self):
        rules = [{"target_canvas_id": "target_canvas", "chance": -0.1}]
        d = _toml_with_substitutions(rules=rules)
        template = normalize(d)
        errors = validate(template)
        self.assertTrue(
            any("chance" in e and "[0.0, 1.0]" in e for e in errors),
            f"Expected validator to reject negative chance; errors={errors}",
        )

    def test_validator_warns_on_substitution_only_with_npcid(self):
        import warnings
        d = _toml_with_substitutions(substitution_only=True)
        # Add npc to the substitution_only target
        d["canvases"][1]["trigger"]["npc"] = "npc_frank"
        template = normalize(d)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            validate(template)
            messages = [str(w.message) for w in caught]
        self.assertTrue(
            any("substitution_only = true AND npc set" in m for m in messages),
            f"Expected warning about substitution_only + npc conflict; got {messages}",
        )

    def test_validator_warns_on_substitutions_plus_trigger_chance(self):
        import warnings
        d = _toml_with_substitutions()
        # Add trigger-level chance to the parent canvas (which has substitutions)
        d["canvases"][0]["trigger"]["chance"] = 0.4
        d["canvases"][0]["trigger"]["trigger_mode"] = "random"
        template = normalize(d)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            validate(template)
            messages = [str(w.message) for w in caught]
        self.assertTrue(
            any("substitutions (Lane 3 dispatcher) AND trigger.chance" in m for m in messages),
            f"Expected warning about substitutions + trigger.chance conflict; got {messages}",
        )


class SubstitutionsEngineEmissionTests(TestCase):
    """PRD 25 §5 — engine emits the substitution check + helpers + map."""

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            email="prd25-substitutions-test@example.com", password="testpass123"
        )

    def _build_with_substitutions(self, rules=None, substitution_only=False):
        d = _toml_with_substitutions(rules=rules, substitution_only=substitution_only)
        template = normalize(d)
        result = create_project_from_template(template, str(self.user.id))
        project = Project.objects.get(id=result["project_id"])
        from apps.game_generation.twee_comprehensive.generators.v1 import (
            TweeComprehensiveGeneratorV1,
        )
        gen = TweeComprehensiveGeneratorV1()
        return gen.generate(project), project

    def _build_without_substitutions(self):
        d = _toml_with_substitutions()
        d["canvases"][0]["trigger"].pop("substitutions", None)
        template = normalize(d)
        result = create_project_from_template(template, str(self.user.id))
        project = Project.objects.get(id=result["project_id"])
        from apps.game_generation.twee_comprehensive.generators.v1 import (
            TweeComprehensiveGeneratorV1,
        )
        gen = TweeComprehensiveGeneratorV1()
        return gen.generate(project), project

    def test_substitution_check_emitted_for_parent_canvas(self):
        """Parent canvas's Node 1 passage must have the
        <<set _sub_target = setup.checkAndSubstituteCanvas("<uuid>")>><<if _sub_target>><<goto _sub_target>><</if>>
        injection. (Use <<set>>+<<goto>> pattern, NOT <<script>>+return — naked
        return is illegal in SugarCube's <<script>> macro.)"""
        twee, project = self._build_with_substitutions()
        from apps.stories.models import StoryCanvas
        parent = StoryCanvas.objects.get(project=project, metadata__slug="parent_canvas")
        expected_call = f'setup.checkAndSubstituteCanvas("{parent.id}")'
        self.assertIn(expected_call, twee, "Substitution check missing from parent canvas passage")
        # Verify the <<set>>+<<goto>> wrapper is present (not <<script>>+return)
        self.assertIn("<<set _sub_target = setup.checkAndSubstituteCanvas", twee)
        self.assertIn("<<if _sub_target>><<goto _sub_target>><</if>>", twee)

    def test_substitution_check_NOT_emitted_for_canvas_without_substitutions(self):
        """Canvas without substitutions field gets NO injection — zero overhead."""
        twee, project = self._build_without_substitutions()
        from apps.stories.models import StoryCanvas
        parent = StoryCanvas.objects.get(project=project, metadata__slug="parent_canvas")
        not_expected = f'setup.checkAndSubstituteCanvas("{parent.id}")'
        self.assertNotIn(not_expected, twee, "Substitution check should not appear for canvas without substitutions")

    def test_canvasSubstitutions_map_populated(self):
        """setup.canvasSubstitutions JSON map includes parent UUID with rules."""
        twee, project = self._build_with_substitutions()
        from apps.stories.models import StoryCanvas
        parent = StoryCanvas.objects.get(project=project, metadata__slug="parent_canvas")
        target = StoryCanvas.objects.get(project=project, metadata__slug="target_canvas")
        # Map declaration emitted
        self.assertIn("setup.canvasSubstitutions = ", twee)
        # Parent UUID is a key
        self.assertIn(f'"{parent.id}"', twee)
        # Target UUID resolved into the rule (not the slug)
        self.assertIn(f'"target_canvas_id": "{target.id}"', twee)

    def test_canvasSubstitutions_map_empty_when_no_substitutions(self):
        twee, project = self._build_without_substitutions()
        # Map declaration emitted but empty
        self.assertIn("setup.canvasSubstitutions = {}", twee)

    def test_helpers_emitted(self):
        """setup.checkAndSubstituteCanvas + setup.getCanvasById helper definitions exist."""
        twee, project = self._build_with_substitutions()
        self.assertIn("setup.checkAndSubstituteCanvas = function", twee)
        self.assertIn("setup.getCanvasById = function", twee)

    def test_selectors_skip_substitution_only(self):
        """All 3 selectors (selectAutoFireCanvasForLocation, selectNpcPortraitCanvasesForLocation,
        selectSoloActivityCanvasesForLocation) include the substitutionOnly filter line."""
        twee, project = self._build_with_substitutions(substitution_only=True)
        # Count occurrences of the filter — should appear in all 3 selectors
        filter_count = twee.count("if (c.substitutionOnly) continue;")
        self.assertGreaterEqual(filter_count, 3,
            f"Expected substitutionOnly filter in at least 3 selectors; found {filter_count}")

    def test_substitution_only_canvas_marked_in_help_data(self):
        """A substitution_only target canvas has substitutionOnly: true in locationCanvases."""
        twee, project = self._build_with_substitutions(substitution_only=True)
        # The target canvas's substitutionOnly field should be true in the JSON
        self.assertIn('"substitutionOnly": true', twee)

    def test_substitution_only_target_not_pruned(self):
        """A substitution_only canvas referenced ONLY by another canvas's
        substitution rule should still be included in the build (not pruned)."""
        twee, project = self._build_with_substitutions(substitution_only=True)
        from apps.stories.models import StoryCanvas
        target = StoryCanvas.objects.get(project=project, metadata__slug="target_canvas")
        # The target canvas's passage should be emitted
        self.assertIn(f"Canvas_target_canvas_Node_1", twee.replace(" ", ""), )


# ════════════════════════════════════════════════════════════════════════════════
# L2-2 — Lane 2 anti-toggle cooldown tests (entry_only_from field)
# Audit doc 26 + remediation doc 27. Engine extension shipped 2026-05-12.
# ════════════════════════════════════════════════════════════════════════════════


def _toml_with_entry_only_from(slugs=None, trigger_mode="random", extra_locations=None):
    """Build a minimal TOML dict with two canvases:
       - start_canvas: starting canvas (excluded from help_data per the build pipeline)
       - ambient_canvas: the Lane 2 canvas with entry_only_from (lands in locationCanvases)

    Default: ambient_canvas at loc_test with entry_only_from = ['loc_hub'], random-mode.
    """
    if slugs is None:
        slugs = ["loc_hub"]
    locations = [
        {"id": "loc_test", "name": "Test Location", "description": "test"},
        {"id": "loc_hub", "name": "Hub Location", "description": "hub"},
    ]
    if extra_locations:
        locations.extend(extra_locations)
    d = _base_toml()
    d["project"]["starting_canvas"] = "start_canvas"
    d["locations"] = locations
    d["canvases"] = [
        {
            "id": "start_canvas",
            "name": "Start Canvas",
            "description": "Starting canvas (dummy — excluded from help_data).",
            "trigger": {
                "location": "loc_test",
                "is_repeatable": True,
                "priority": 5,
                "is_active": True,
            },
            "nodes": [
                {
                    "id": "base",
                    "name": "Start node",
                    "blocks": [{"type": "paragraph", "content": "Start content."}],
                    "exit_block": {"type": "location", "config": {"destinationType": "trigger"}},
                }
            ],
        },
        {
            "id": "ambient_canvas",
            "name": "Ambient Canvas",
            "description": "Lane 2 ambient with entry_only_from gate",
            "trigger": {
                "location": "loc_test",
                "is_repeatable": True,
                "priority": 4,
                "is_active": True,
                "trigger_mode": trigger_mode,
                "chance": 0.30,
                "entry_only_from": slugs,
            },
            "nodes": [
                {
                    "id": "base",
                    "name": "Ambient body",
                    "blocks": [{"type": "paragraph", "content": "Ambient content."}],
                    "exit_block": {"type": "location", "config": {"destinationType": "trigger"}},
                }
            ],
        },
    ]
    return d


class EntryOnlyFromRoundTripTests(SimpleTestCase):
    """L2-2 §schema — TemplateTrigger.entry_only_from preserved through parser."""

    def test_entry_only_from_round_trips(self):
        d = _toml_with_entry_only_from(slugs=["loc_hub", "loc_other"],
                                        extra_locations=[{"id": "loc_other", "name": "Other", "description": "x"}])
        template = normalize(d)
        canvas = next(c for c in template.canvases if c.id == "ambient_canvas")
        self.assertEqual(canvas.trigger.entry_only_from, ["loc_hub", "loc_other"])

    def test_entry_only_from_default_empty(self):
        d = _toml_with_entry_only_from()
        d["canvases"][1]["trigger"].pop("entry_only_from", None)
        template = normalize(d)
        canvas = next(c for c in template.canvases if c.id == "ambient_canvas")
        self.assertEqual(canvas.trigger.entry_only_from, [])

    def test_entry_only_from_strips_whitespace_and_drops_empty(self):
        d = _toml_with_entry_only_from(slugs=["  loc_hub  ", "", "   "])
        template = normalize(d)
        canvas = next(c for c in template.canvases if c.id == "ambient_canvas")
        # Whitespace stripped, empty/whitespace-only entries dropped
        self.assertEqual(canvas.trigger.entry_only_from, ["loc_hub"])


class EntryOnlyFromValidatorTests(SimpleTestCase):
    """L2-2 §validator — cross-ref location IDs + non-random warning."""

    def test_validator_rejects_unknown_location(self):
        d = _toml_with_entry_only_from(slugs=["loc_nonexistent"])
        template = normalize(d)
        errors = validate(template)
        self.assertTrue(
            any("loc_nonexistent" in e and "does not match any location" in e for e in errors),
            f"Expected validator to reject unknown location slug; errors={errors}",
        )

    def test_validator_accepts_valid_location(self):
        d = _toml_with_entry_only_from(slugs=["loc_hub"])  # loc_hub is in the test fixture
        template = normalize(d)
        errors = validate(template)
        # No entry_only_from-related errors; other validation may still produce errors
        # (e.g., location image not found — these are warnings not errors). Filter:
        relevant_errors = [e for e in errors if "entry_only_from" in e]
        self.assertEqual(relevant_errors, [], f"Expected no entry_only_from errors; got {relevant_errors}")

    def test_validator_warns_on_non_random_canvas(self):
        import warnings
        d = _toml_with_entry_only_from(slugs=["loc_hub"], trigger_mode="manual")
        template = normalize(d)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            validate(template)
            messages = [str(w.message) for w in caught]
        self.assertTrue(
            any("entry_only_from" in m and "trigger_mode is 'manual'" in m for m in messages),
            f"Expected warning about entry_only_from on non-random canvas; got {messages}",
        )


class EntryOnlyFromEngineEmissionTests(TestCase):
    """L2-2 §engine — help_data emits entryOnlyFromPassages with slug→passage translation."""

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            email="l2-2-entry-only-from-test@example.com", password="testpass123"
        )

    def _build_with_entry_only_from(self, slugs=None, trigger_mode="random"):
        d = _toml_with_entry_only_from(slugs=slugs, trigger_mode=trigger_mode)
        template = normalize(d)
        result = create_project_from_template(template, str(self.user.id))
        project = Project.objects.get(id=result["project_id"])
        from apps.game_generation.twee_comprehensive.generators.v1 import (
            TweeComprehensiveGeneratorV1,
        )
        gen = TweeComprehensiveGeneratorV1()
        return gen.generate(project), project

    def test_entry_only_from_translated_to_passage_names(self):
        """Author writes ['loc_hub']; build emits 'entryOnlyFromPassages':['Location_Hub_Location']."""
        twee, project = self._build_with_entry_only_from(slugs=["loc_hub"])
        # Hub Location → Location_Hub_Location (spaces replaced)
        self.assertIn('"entryOnlyFromPassages":', twee)
        self.assertIn('"Location_Hub_Location"', twee)

    def test_entry_only_from_empty_when_unset(self):
        """Canvas without entry_only_from emits empty array."""
        d = _toml_with_entry_only_from()
        d["canvases"][1]["trigger"].pop("entry_only_from", None)
        template = normalize(d)
        result = create_project_from_template(template, str(self.user.id))
        project = Project.objects.get(id=result["project_id"])
        from apps.game_generation.twee_comprehensive.generators.v1 import (
            TweeComprehensiveGeneratorV1,
        )
        gen = TweeComprehensiveGeneratorV1()
        twee = gen.generate(project)
        # Empty array present (defensive default for engine)
        self.assertIn('"entryOnlyFromPassages": []', twee)

    def test_engine_emits_anti_toggle_filter(self):
        """The checkRandomEncounters function includes the entry_only_from filter loop."""
        twee, project = self._build_with_entry_only_from(slugs=["loc_hub"])
        # Engine code fragments
        self.assertIn("entryOnlyFromPassages", twee)
        self.assertIn("afterEntryGate", twee)
        # SugarCube's previous() call wrapped in try/catch (fail-safe)
        self.assertIn("prevPassage = previous()", twee)


# ════════════════════════════════════════════════════════════════════════════════
# L1-2 — Image pool variety tests (files = [...] array on image blocks)
# Audit doc 26 + remediation doc 27 §L1-2. Engine extension shipped 2026-05-12.
# ════════════════════════════════════════════════════════════════════════════════


def _toml_with_image_block(image_props):
    """Build a minimal TOML dict with one canvas containing one image block.

    image_props: dict of props for the image block (e.g. {"file": "x.jpg"} or
    {"files": ["a.jpg", "b.jpg"]} or both, plus optional alt/caption/description).
    """
    d = _base_toml()
    d["project"]["starting_canvas"] = "start_canvas"
    d["locations"] = [
        {"id": "loc_test", "name": "Test Location", "description": "test"}
    ]
    d["canvases"] = [
        {
            "id": "start_canvas",
            "name": "Start",
            "description": "start",
            "trigger": {
                "location": "loc_test",
                "is_repeatable": True,
                "priority": 5,
                "is_active": True,
            },
            "nodes": [
                {
                    "id": "base",
                    "name": "Start node",
                    "blocks": [{"type": "paragraph", "content": "Start."}],
                    "exit_block": {"type": "location", "config": {"destinationType": "trigger"}},
                }
            ],
        },
        {
            "id": "image_canvas",
            "name": "Image Canvas",
            "description": "image",
            "trigger": {
                "location": "loc_test",
                "is_repeatable": True,
                "priority": 5,
                "is_active": True,
            },
            "nodes": [
                {
                    "id": "base",
                    "name": "Image node",
                    "blocks": [
                        {"type": "image", "props": image_props},
                        {"type": "paragraph", "content": "Body."},
                    ],
                    "exit_block": {"type": "location", "config": {"destinationType": "trigger"}},
                }
            ],
        },
    ]
    return d


class ImagePoolTests(TestCase):
    """L1-2 — image block accepts `files = [...]` array; emits either() macro
    + @src="_img" SugarCube attribute-directive for per-render random selection."""

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            email="l1-2-image-pool-test@example.com", password="testpass123"
        )

    def _build(self, image_props):
        d = _toml_with_image_block(image_props)
        template = normalize(d)
        result = create_project_from_template(template, str(self.user.id))
        project = Project.objects.get(id=result["project_id"])
        from apps.game_generation.twee_comprehensive.generators.v1 import (
            TweeComprehensiveGeneratorV1,
        )
        gen = TweeComprehensiveGeneratorV1()
        # Debug mode so missing-pool placeholder renders (matches dev build flow)
        return gen.generate(project, options={"debug": True}), project, gen

    def test_files_array_collected_in_missing_media(self):
        """Pool with no real assets: each pool entry collected in missing_media
        with search_queries propagated. Build doesn't fail."""
        twee, project, gen = self._build({
            "files": ["scenes/pool_a.jpg", "scenes/pool_b.jpg"],
            "description": "Test pool",
            "search_queries": ["query one", "query two"],
        })
        missing_files = [m['file'] for m in gen.missing_media if m['type'] == 'image']
        self.assertIn("scenes/pool_a.jpg", missing_files)
        self.assertIn("scenes/pool_b.jpg", missing_files)
        # search_queries propagate to each pool entry
        for m in gen.missing_media:
            if m['file'] in ("scenes/pool_a.jpg", "scenes/pool_b.jpg"):
                self.assertEqual(m['search_queries'], ["query one", "query two"])

    def test_all_missing_pool_falls_through_to_placeholder(self):
        """When ALL pool files missing in debug mode: emits the
        [IMAGE POOL MISSING — N files] placeholder. No either() macro emitted."""
        twee, project, gen = self._build({
            "files": ["scenes/missing_1.jpg", "scenes/missing_2.jpg", "scenes/missing_3.jpg"],
            "description": "All missing",
        })
        # Placeholder includes the pool-size hint
        self.assertIn("[IMAGE POOL MISSING — 3 files]", twee)
        # No either() macro emitted when no files resolved
        self.assertNotIn("<<set _img to either(", twee)

    def test_single_file_path_unchanged_when_no_pool(self):
        """Image block with `file = "..."` (no `files` key) emits static
        <img src="..." (no either() macro, no _img). Zero-regression test."""
        twee, project, gen = self._build({
            "file": "scenes/single.jpg",
            "description": "Single file",
        })
        # Single-file path preserved — no pool macro
        self.assertNotIn("<<set _img to either(", twee)
        self.assertNotIn('@src="_img"', twee)
        # Single file collected as missing (not as a pool)
        missing_files = [m['file'] for m in gen.missing_media if m['type'] == 'image']
        self.assertIn("scenes/single.jpg", missing_files)

    def test_files_wins_over_file_when_both_present(self):
        """When both `file` and `files` present, pool wins; single `file` ignored
        (no entry in missing_media for the single file)."""
        twee, project, gen = self._build({
            "file": "scenes/single_should_be_ignored.jpg",
            "files": ["scenes/pool_x.jpg", "scenes/pool_y.jpg"],
            "description": "Both keys",
        })
        missing_files = [m['file'] for m in gen.missing_media if m['type'] == 'image']
        # Pool entries collected
        self.assertIn("scenes/pool_x.jpg", missing_files)
        self.assertIn("scenes/pool_y.jpg", missing_files)
        # Single file path NOT taken — its file is not in missing_media
        self.assertNotIn("scenes/single_should_be_ignored.jpg", missing_files)

    def test_macro_emitted_when_pool_files_resolve(self):
        """When pool files resolve via _find_media_file: emits
        <<set _img to either(...)>> macro + <img @src="_img"> attribute-directive."""
        from unittest.mock import patch
        d = _toml_with_image_block({
            "files": ["scenes/found_a.jpg", "scenes/found_b.jpg", "scenes/found_c.jpg"],
            "alt": "pool alt",
        })
        template = normalize(d)
        result = create_project_from_template(template, str(self.user.id))
        project = Project.objects.get(id=result["project_id"])
        from apps.game_generation.twee_comprehensive.generators.v1 import (
            TweeComprehensiveGeneratorV1,
        )
        gen = TweeComprehensiveGeneratorV1()

        # Mock _find_media_file to claim all 3 pool entries exist as .jpg files.
        # IMAGE_EXTENSIONS uses leading-dot ".jpg" so the mock must too.
        def fake_find(path):
            return (path, ".jpg")

        # Patch on the class so the method override survives the generate() call's
        # internal state setup (instance-level patch can be lost on re-init).
        from apps.game_generation.twee_comprehensive.generators.v1 import (
            TweeComprehensiveGeneratorV1 as Gen,
        )
        with patch.object(Gen, "_find_media_file", side_effect=fake_find, autospec=False):
            twee = gen.generate(project, options={"debug": True})

        # Macro emitted with all 3 paths quoted + comma-separated
        self.assertIn("<<set _img to either(", twee)
        self.assertIn('"media/images/scenes/found_a.jpg"', twee)
        self.assertIn('"media/images/scenes/found_b.jpg"', twee)
        self.assertIn('"media/images/scenes/found_c.jpg"', twee)
        # SugarCube attribute-directive (NOT src="@_img")
        self.assertIn('@src="_img"', twee)
        self.assertNotIn('src="@_img"', twee)
        # All 3 tracked in used_assets
        self.assertIn("scenes/found_a.jpg", gen.used_assets['external_images'])
        self.assertIn("scenes/found_b.jpg", gen.used_assets['external_images'])
        self.assertIn("scenes/found_c.jpg", gen.used_assets['external_images'])


# -- Worn-clothing-stats engine feature (doc 37) -----------------------------


class WornClothingStatsTests(TestCase):
    """Doc 37: clothing items carry beauty/corruption; worn_beauty/worn_corruption
    predicates gate on the MAX stat across the equipped outfit.

    Static-emission tests (assert against the generated Twee string). Runtime
    truth (does the gate fire on equip) is verified by live-play, not here.
    """

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            email="worn-clothing-test@example.com", password="testpass123"
        )
        with open(FIXTURE_PATH, "rb") as f:
            cls.toml_data = tomli.load(f)

    def _generate(self, toml_dict):
        template = normalize(copy.deepcopy(toml_dict))
        errors = validate(template)
        self.assertEqual(errors, [], f"Template should validate clean: {errors}")
        result = create_project_from_template(template, str(self.user.id))
        project = Project.objects.get(id=result["project_id"])
        from apps.game_generation.twee_comprehensive.generators.v1 import (
            TweeComprehensiveGeneratorV1,
        )
        twee = TweeComprehensiveGeneratorV1().generate(project)
        return project, twee

    def _clothing_enabled_toml(self):
        """Deep-copy the fixture and switch the clothing system on with two
        items — one carrying beauty/corruption, one without (defaults to 0)."""
        data = copy.deepcopy(self.toml_data)
        data.setdefault("settings", {})["clothing_enabled"] = True
        data["clothing"] = [
            {
                "id": "daring_top",
                "name": "Daring Top",
                "slot": "top",
                "initial": True,
                "beauty": 4,
                "corruption": 30,
            },
            {
                "id": "plain_bottom",
                "name": "Plain Bottom",
                "slot": "bottom",
                "initial": True,
            },
        ]
        return data

    # --- aggregates: present only when clothing enabled ---------------------

    def test_aggregates_emitted_when_clothing_enabled(self):
        _, twee = self._generate(self._clothing_enabled_toml())
        self.assertIn("setup.getWornStatMax = function", twee)
        self.assertIn("setup.getWornBeauty = function", twee)
        self.assertIn("setup.getWornCorruption = function", twee)

    def test_aggregates_absent_when_clothing_disabled(self):
        # Default fixture has clothing_enabled=false → the enabled-only
        # wardrobe_js_block (and thus the aggregate DEFINITIONS) must not be
        # emitted. Note: the bare names still appear in the always-emitted
        # dispatch branch (`setup.getWornBeauty()`), so assert the function
        # DEFINITIONS are absent, not the names.
        _, twee = self._generate(self.toml_data)
        self.assertNotIn("setup.getWornStatMax = function", twee)
        self.assertNotIn("setup.getWornBeauty = function", twee)
        self.assertNotIn("setup.getWornCorruption = function", twee)

    # --- dispatch + formatter: always-emitted core JS -----------------------

    def test_worn_dispatch_branch_always_emitted(self):
        _, twee = self._generate(self.toml_data)  # clothing disabled
        self.assertIn("type === 'worn_beauty' || type === 'worn_corruption'", twee)

    def test_worn_formatter_branch_always_emitted(self):
        _, twee = self._generate(self.toml_data)  # clothing disabled
        self.assertIn("Outfit must be revealing (corruption ", twee)
        self.assertIn('item.type === "worn_beauty"', twee)

    # --- schema round-trip --------------------------------------------------

    def test_metadata_round_trips_beauty_and_corruption(self):
        project, _ = self._generate(self._clothing_enabled_toml())
        items = project.metadata["clothing_settings"]["items"]
        by_id = {it["id"]: it for it in items}
        self.assertEqual(by_id["daring_top"]["beauty"], 4)
        self.assertEqual(by_id["daring_top"]["corruption"], 30)
        # Omitted stats default to 0.
        self.assertEqual(by_id["plain_bottom"]["beauty"], 0)
        self.assertEqual(by_id["plain_bottom"]["corruption"], 0)

    def test_clothing_data_carries_stats_into_setup(self):
        _, twee = self._generate(self._clothing_enabled_toml())
        # setup.clothing_data is the source of truth the aggregate reads.
        self.assertIn("setup.clothing_data = ", twee)
        self.assertIn('"corruption": 30', twee)


class DailyTickTraitEffectsTests(TestCase):
    """Doc 40: [engine.daily_tick].traitEffects apply trait deltas once per
    in-game day (the RTS arousal daily auto-rise). Static-emission tests; the
    runtime +1/day-with-cap behavior is verified by live-play, not here.
    """

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            email="daily-tick-trait-test@example.com", password="testpass123"
        )
        with open(FIXTURE_PATH, "rb") as f:
            cls.toml_data = tomli.load(f)

    def _generate(self, toml_dict):
        template = normalize(copy.deepcopy(toml_dict))
        errors = validate(template)
        self.assertEqual(errors, [], f"Template should validate clean: {errors}")
        result = create_project_from_template(template, str(self.user.id))
        project = Project.objects.get(id=result["project_id"])
        from apps.game_generation.twee_comprehensive.generators.v1 import (
            TweeComprehensiveGeneratorV1,
        )
        twee = TweeComprehensiveGeneratorV1().generate(project)
        return project, twee

    def _with_daily_tick_trait(self):
        """Fixture + an [engine.daily_tick] that raises player arousal +1/day,
        capped at 10 (the canonical RTS-faithful config)."""
        data = copy.deepcopy(self.toml_data)
        engine = data.setdefault("engine", {})
        engine["daily_tick"] = {
            "traitEffects": [
                {
                    "targetType": "player",
                    "trait": "arousal",
                    "op": "add",
                    "value": 1,
                    "cap": 10,
                }
            ]
        }
        return data

    # --- always-emitted runtime loop ---------------------------------------

    def test_daily_tick_trait_loop_always_emitted(self):
        # The advanceDay traitEffects loop is core JS — present even with no
        # daily_tick configured, iterating an empty list.
        _, twee = self._generate(self.toml_data)
        self.assertIn("setup.daily_tick.traitEffects.length", twee)
        self.assertIn("setup.applyAndNotifyTrait(", twee)

    def test_back_compat_traiteffects_empty_without_config(self):
        # No [engine.daily_tick] in the fixture → setup.daily_tick still carries
        # an empty traitEffects list (stable loop target, no behavior change).
        _, twee = self._generate(self.toml_data)
        self.assertIn('"traitEffects": []', twee)

    # --- configured: round-trip + emission ----------------------------------

    def test_traiteffects_round_trip_into_metadata(self):
        project, _ = self._generate(self._with_daily_tick_trait())
        te = project.metadata["daily_tick"]["traitEffects"]
        self.assertEqual(len(te), 1)
        self.assertEqual(te[0]["trait"], "arousal")
        self.assertEqual(te[0]["targetType"], "player")
        self.assertEqual(te[0]["op"], "add")
        self.assertEqual(te[0]["value"], 1)
        self.assertEqual(te[0]["cap"], 10)

    def test_traiteffects_emitted_into_setup(self):
        _, twee = self._generate(self._with_daily_tick_trait())
        # The configured entry rides into setup.daily_tick.traitEffects.
        self.assertIn('"trait": "arousal"', twee)
        self.assertIn('"cap": 10', twee)


# ---------------------------------------------------------------------------
# Doc 45 Tier 1 — RTS phone parity: G6 (conditional daily_tick), G1 (delivery
# toast), G3 (photo quick-actions). Schema round-trips + runtime emission.
# ---------------------------------------------------------------------------


class DailyTickConditionsSchemaTests(SimpleTestCase):
    """G6 — optional per-effect `conditions` on daily_tick flag/trait effects."""

    def test_flag_effect_conditions_round_trip(self):
        cond = {"version": "1.0", "logic": "AND", "items": [
            {"type": "trait", "subject": "player", "trait_key": "corruption",
             "operator": "gte", "value": 20}
        ]}
        d = _toml_with_daily_tick(
            [{"targetType": "player", "flag": "talked_to_frank_today",
              "op": "unset", "conditions": cond}]
        )
        template = normalize(d)
        self.assertEqual(template.daily_tick.flagEffects[0].conditions, cond)

    def test_trait_effect_conditions_round_trip(self):
        cond = {"version": "1.0", "items": [
            {"type": "trait", "subject": "player", "trait_key": "corruption",
             "operator": "gte", "value": 20}
        ]}
        d = _base_toml()
        d["engine"] = {"daily_tick": {"traitEffects": [
            {"targetType": "player", "trait": "arousal", "op": "add",
             "value": 1, "cap": 10, "conditions": cond}
        ]}}
        template = normalize(d)
        self.assertEqual(template.daily_tick.traitEffects[0].conditions, cond)

    def test_absent_conditions_is_none(self):
        d = _toml_with_daily_tick(
            [{"targetType": "player", "flag": "talked_to_frank_today", "op": "unset"}]
        )
        template = normalize(d)
        self.assertIsNone(template.daily_tick.flagEffects[0].conditions)


def _toml_with_phone():
    """Minimal phone block exercising the doc-45 Tier-1 fields."""
    d = _base_toml()
    d["phone"] = {
        "enabled": True,
        "apps": [
            {"id": "messages", "type": "chat", "label": "Messages"},
            {"id": "flaunt", "type": "social_feed", "label": "Flaunt"},
        ],
        "conversations": [
            {
                "id": "frank_text_1", "app": "messages", "npc": "npc_frank",
                "notify": "Frank texted you",
                "trigger": {"conditions": {"version": "1.0", "items": [
                    {"type": "flag", "subject": "player",
                     "flag_key": "summer_started", "operator": "is_true"}
                ]}},
                "blocks": [{"type": "message", "sender": "npc", "content": "hey"}],
            }
        ],
        "posts": [
            {"id": "stranger_post_1", "app": "flaunt", "poster_name": "@x",
             "caption": "hi", "notify": "New post from @x"}
        ],
        "daily_topics": [
            {"id": "send_selfie", "npc": "npc_frank",
             "player_message": "sent you a selfie", "npc_response": "cute",
             "image": "phone/selfie1.jpg", "corruption_min": 3,
             "cooldown": "per_topic",
             "effects": [{"targetType": "npc", "npcId": "npc_frank",
                          "trait": "trust", "op": "add", "value": 1}]},
            {"id": "say_hi", "npc": "npc_frank",
             "player_message": "hey", "npc_response": "hi"},
        ],
    }
    return d


class PhoneParityFieldsSchemaTests(SimpleTestCase):
    """G1 + G3 — notify on conversation/post; image/corruption_min/cooldown on topics."""

    def test_phone_fields_round_trip(self):
        template = normalize(_toml_with_phone())
        self.assertTrue(template.phone_enabled)
        self.assertEqual(template.phone.conversations[0].notify, "Frank texted you")
        self.assertEqual(template.phone.posts[0].notify, "New post from @x")
        dt = template.phone.daily_topics[0]
        self.assertEqual(dt.image, "phone/selfie1.jpg")
        self.assertEqual(dt.corruption_min, 3)
        self.assertEqual(dt.cooldown, "per_topic")

    def test_phone_field_defaults_backcompat(self):
        d = _base_toml()
        d["phone"] = {
            "enabled": True,
            "apps": [{"id": "messages", "type": "chat", "label": "Messages"}],
            "daily_topics": [{"id": "t", "npc": "npc_frank",
                              "player_message": "hi", "npc_response": "yo"}],
        }
        template = normalize(d)
        dt = template.phone.daily_topics[0]
        self.assertEqual(dt.image, "")
        self.assertIsNone(dt.corruption_min)
        self.assertEqual(dt.cooldown, "")


class PhoneParityIntegrationTests(TestCase):
    """Build a phone-enabled project and grep the generated Twee (v1 + v2)
    for the doc-45 Tier-1 runtime: G6 guard, G1 toast, G3 per-topic cooldown."""

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            email="phone-parity-test@example.com", password="testpass123"
        )
        with open(FIXTURE_PATH, "rb") as f:
            cls.toml_data = tomli.load(f)

    def _build(self, gen_cls):
        toml_data = copy.deepcopy(self.toml_data)
        # enable a minimal phone
        toml_data["phone"] = _toml_with_phone()["phone"]
        # a conditional daily_tick (G6)
        toml_data["player"]["flag_keys"] = list(
            toml_data["player"].get("flag_keys", [])
        ) + ["talked_to_frank_today"]
        toml_data["engine"] = {"daily_tick": {"traitEffects": [
            {"targetType": "player", "trait": "arousal", "op": "add", "value": 1,
             "cap": 10,
             "conditions": {"version": "1.0", "items": [
                 {"type": "trait", "subject": "player", "trait_key": "corruption",
                  "operator": "gte", "value": 20}]}}
        ]}}
        template = normalize(toml_data)
        errors = validate(template)
        self.assertEqual(errors, [], f"phone fixture should validate clean: {errors}")
        result = create_project_from_template(template, str(self.user.id))
        project = Project.objects.get(id=result["project_id"])
        twee = gen_cls().generate(project)
        self.assertIsInstance(twee, str)
        return twee

    def _assert_runtime(self, twee):
        # G6 — conditional daily_tick guard
        self.assertIn("setup.triggerConditionsSatisfied(dtTe.conditions)", twee)
        # G1 — delivery toast helper + class + per-conv notify
        self.assertIn("setup._notifyPhoneDelivery", twee)
        self.assertIn("phone-notify", twee)
        self.assertIn("Frank texted you", twee)
        # G3 — per-topic cooldown + corruption lock + image
        self.assertIn("topic_days", twee)
        self.assertIn("phone-daily-locked", twee)
        self.assertIn("corruption_min", twee)

    def test_v2_runtime(self):
        from apps.game_generation.twee_comprehensive.generators.v2 import (
            TweeComprehensiveGeneratorV2,
        )
        self._assert_runtime(self._build(TweeComprehensiveGeneratorV2))

    def test_v1_parity_runtime(self):
        from apps.game_generation.twee_comprehensive.generators.v1 import (
            TweeComprehensiveGeneratorV1,
        )
        self._assert_runtime(self._build(TweeComprehensiveGeneratorV1))


# ---------------------------------------------------------------------------
# Doc 45 Tier 2 — quest primitive (G4), delay queue (G5), social posting (G2).
# ---------------------------------------------------------------------------


class QuestSchemaTests(SimpleTestCase):
    """G4 — [[quests]] + questEffects parse."""

    def _toml_with_quest(self):
        d = _base_toml()
        d["quests"] = [
            {"id": "befriend_frank", "name": "Befriend Frank",
             "steps": ["Say hi", "Have coffee", "Earn his trust"], "repeatable": False}
        ]
        return d

    def test_quest_round_trip(self):
        template = normalize(self._toml_with_quest())
        self.assertEqual(len(template.quests), 1)
        q = template.quests[0]
        self.assertEqual(q.id, "befriend_frank")
        self.assertEqual(len(q.steps), 3)

    def test_quest_effects_on_choice_parse(self):
        with open(FIXTURE_PATH, "rb") as f:
            d = tomli.load(f)
        eb = d["canvases"][0]["nodes"][0]["exit_block"]
        eb["type"] = "choices"
        eb.setdefault("choices", [])
        eb["choices"].append({
            "text": "Start it", "targetType": "trigger",
            "questEffects": [{"quest": "befriend_frank", "op": "start"}],
            "scheduleEffects": [{"delayDays": 3, "action": "set_flag", "flag": "reminder"}],
        })
        template = normalize(d)
        found = None
        for c in template.canvases[0].nodes[0].exit_block.choices:
            if c.quest_effects:
                found = c
                break
        self.assertIsNotNone(found)
        self.assertEqual(found.quest_effects[0]["quest"], "befriend_frank")
        self.assertEqual(found.schedule_effects[0]["action"], "set_flag")


class PhonePostActionsSchemaTests(SimpleTestCase):
    """G2 — social_feed post_actions parse."""

    def test_post_actions_round_trip(self):
        d = _base_toml()
        d["phone"] = {
            "enabled": True,
            "apps": [{"id": "flaunt", "type": "social_feed", "label": "Flaunt",
                      "post_actions": [
                          {"label": "Selfie", "followers_min": 5, "followers_max": 20, "counter_trait": "followers"},
                          {"label": "Lewd", "corruption_min": 30, "followers_min": 30, "followers_max": 50, "counter_trait": "followers"},
                      ]}],
        }
        template = normalize(d)
        app = template.phone.apps[0]
        self.assertEqual(len(app.post_actions), 2)
        self.assertEqual(app.post_actions[1]["corruption_min"], 30)


class Tier2RuntimeIntegrationTests(TestCase):
    """Build a project exercising G4/G5/G2 and grep generated Twee (v1 + v2)."""

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            email="tier2-test@example.com", password="testpass123"
        )
        with open(FIXTURE_PATH, "rb") as f:
            cls.toml_data = tomli.load(f)

    def _build(self, gen_cls):
        d = copy.deepcopy(self.toml_data)
        d["quests"] = [{"id": "q1", "name": "Quest One", "steps": ["a", "b"]}]
        d["phone"] = {
            "enabled": True,
            "apps": [
                {"id": "messages", "type": "chat", "label": "Messages"},
                {"id": "flaunt", "type": "social_feed", "label": "Flaunt",
                 "post_actions": [{"label": "Selfie", "followers_min": 5, "followers_max": 20, "counter_trait": "followers"}]},
                {"id": "quests", "type": "quests", "label": "Quests"},
            ],
        }
        template = normalize(d)
        errors = validate(template)
        self.assertEqual(errors, [], f"tier2 fixture should validate: {errors}")
        result = create_project_from_template(template, str(self.user.id))
        project = Project.objects.get(id=result["project_id"])
        twee = gen_cls().generate(project)
        self.assertIsInstance(twee, str)
        return twee

    def _assert_runtime(self, twee):
        # G4
        self.assertIn("setup.applyQuestEffect", twee)
        self.assertIn("setup._renderQuests", twee)
        self.assertIn("type === 'quest'", twee)
        self.assertIn("setup.quests_data", twee)
        # G5
        self.assertIn("setup.scheduleEvent", twee)
        self.assertIn("setup.fireScheduledEvent", twee)
        # G2
        self.assertIn("setup.sendSocialPost", twee)
        self.assertIn("phone-post-btn", twee)

    def test_v2_runtime(self):
        from apps.game_generation.twee_comprehensive.generators.v2 import (
            TweeComprehensiveGeneratorV2,
        )
        self._assert_runtime(self._build(TweeComprehensiveGeneratorV2))

    def test_v1_parity_runtime(self):
        from apps.game_generation.twee_comprehensive.generators.v1 import (
            TweeComprehensiveGeneratorV1,
        )
        self._assert_runtime(self._build(TweeComprehensiveGeneratorV1))


# ---------------------------------------------------------------------------
# Doc 45 Tier 3 — corruption tiers (G7), gallery (G8), purchase gate (G11),
# custom app (G12), fast jobs + bank (G9).
# ---------------------------------------------------------------------------


class Tier3SchemaTests(SimpleTestCase):
    def test_corruption_tiers_parse(self):
        d = _base_toml()
        d["engine"] = {"corruption_tiers": [0, 10, 25, 50, 80]}
        template = normalize(d)
        self.assertEqual(template.corruption_tiers, [0, 10, 25, 50, 80])

    def test_phone_purchase_flag_and_gallery_parse(self):
        d = _base_toml()
        d["phone"] = {
            "enabled": True,
            "purchase_flag": "owns_phone",
            "apps": [{"id": "g", "type": "gallery", "label": "Gallery"},
                     {"id": "c", "type": "custom", "label": "xCam", "passage": "xcam_scene"}],
            "gallery_items": [
                {"id": "p1", "image": "x.jpg", "caption": "hi",
                 "trigger": {"version": "1.0", "items": [{"type": "corruption_level", "operator": "gte", "value": 2}]},
                 "link": "watch_p1"}],
        }
        template = normalize(d)
        self.assertEqual(template.phone.purchase_flag, "owns_phone")
        self.assertEqual(len(template.phone.gallery_items), 1)
        self.assertEqual(template.phone.gallery_items[0].link, "watch_p1")
        self.assertEqual(template.phone.apps[1].type, "custom")

    def test_fast_jobs_and_bank_parse(self):
        d = _base_toml()
        d["fast_jobs"] = [{"id": "dog", "name": "Dog walking", "income": 45,
                           "xp_req": 0, "cooldown_days": 2, "money_trait": "money"}]
        d["bank"] = {"enabled": True, "interest_rate": 0.02}
        template = normalize(d)
        self.assertEqual(len(template.fast_jobs), 1)
        self.assertEqual(template.fast_jobs[0].income, 45)
        self.assertIsNotNone(template.bank)
        self.assertEqual(template.bank.interest_rate, 0.02)


class Tier3RuntimeIntegrationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            email="tier3-test@example.com", password="testpass123"
        )
        with open(FIXTURE_PATH, "rb") as f:
            cls.toml_data = tomli.load(f)

    def _build(self, gen_cls):
        d = copy.deepcopy(self.toml_data)
        d["engine"] = dict(d.get("engine", {}) or {})
        d["engine"]["corruption_tiers"] = [0, 5, 15, 30, 45]
        d["fast_jobs"] = [{"id": "dog", "name": "Dog walking", "income": 45, "cooldown_days": 2}]
        d["bank"] = {"enabled": True, "interest_rate": 0.01}
        d["phone"] = {
            "enabled": True, "purchase_flag": "owns_phone",
            "apps": [
                {"id": "g", "type": "gallery", "label": "Gallery"},
                {"id": "c", "type": "custom", "label": "xCam", "passage": "Start"},
                {"id": "jobs", "type": "fast_jobs", "label": "Jobs"},
                {"id": "bank", "type": "bank", "label": "Bank"},
            ],
            "gallery_items": [{"id": "p1", "image": "x.jpg", "link": "Start"}],
        }
        template = normalize(d)
        errors = validate(template)
        self.assertEqual(errors, [], f"tier3 fixture should validate: {errors}")
        result = create_project_from_template(template, str(self.user.id))
        project = Project.objects.get(id=result["project_id"])
        twee = gen_cls().generate(project)
        self.assertIsInstance(twee, str)
        return twee

    def _assert_runtime(self, twee):
        self.assertIn("setup.getCorruptionLevel", twee)          # G7
        self.assertIn("type === 'corruption_level'", twee)       # G7
        self.assertIn("setup._renderGallery", twee)              # G8
        self.assertIn("setup.phone_purchase_flag", twee)         # G11
        self.assertIn("setup._renderCustom", twee)               # G12
        self.assertIn("setup._renderFastJobs", twee)             # G9
        self.assertIn("setup.doFastJob", twee)                   # G9
        self.assertIn("setup._renderBank", twee)                 # G9
        self.assertIn("Bank interest", twee)                     # G9 advanceDay

    def test_v2_runtime(self):
        from apps.game_generation.twee_comprehensive.generators.v2 import (
            TweeComprehensiveGeneratorV2,
        )
        self._assert_runtime(self._build(TweeComprehensiveGeneratorV2))

    def test_v1_parity_runtime(self):
        from apps.game_generation.twee_comprehensive.generators.v1 import (
            TweeComprehensiveGeneratorV1,
        )
        self._assert_runtime(self._build(TweeComprehensiveGeneratorV1))


# ─── PRD 48: Quests Engine V2 ───────────────────────────────────────────────
# Tests for the new author-on-template quests engine. Schema tests
# (SimpleTestCase) exercise QuestsCard parsing + validation + serialization.
# Build dispatch tests confirm V1 vs V2 emission selection works.


def _minimal_v1_toml() -> dict:
    """A minimal but valid TOML dict for a V1 game (no quests_engine flag)."""
    return {
        "schema_version": "0.3",
        "project": {"id": "qv2_smoke", "title": "Smoke", "description": "x"},
        "time": {"enabled": True, "starting_hour": 8, "starting_day": "Monday", "starting_week": 1},
        "player": {"id": "player_p", "name": "P", "starting_location": "loc_a", "core_traits": {}},
        "npcs": [
            {"id": "npc_a", "name": "A", "starting_location": "loc_a",
             "trait_decay": {}, "core_traits": {}},
        ],
        "locations": [
            {"id": "loc_a", "name": "Loc A", "description": "x"},
        ],
        "canvases": [],
    }


def _minimal_v2_toml() -> dict:
    base = _minimal_v1_toml()
    base["project"]["quests_engine"] = "v2"
    return base


class QuestsV2SchemaTests(SimpleTestCase):
    """Schema tests for the V2 quest_cards block."""

    def test_quests_engine_field_defaults_v1(self):
        data = _minimal_v1_toml()
        template = normalize(data)
        self.assertEqual(template.project.quests_engine, "v1")
        self.assertEqual(template.quests_cards, [])

    def test_quests_engine_field_parses_v2(self):
        data = _minimal_v2_toml()
        template = normalize(data)
        self.assertEqual(template.project.quests_engine, "v2")

    def test_v2_card_parses_with_all_fields(self):
        data = _minimal_v2_toml()
        data["quest_cards"] = [{
            "text": "Looking at him.",
            "ready_text": "He sees it now.",
            "tip": "Try the kitchen at dawn.",
            "npc_id": "npc_a",
            "priority": 1,
            "when": [{"flag": "f_caught", "op": "is_false"}],
            "goals": [{
                "trait": "corruption", "subject": "player",
                "op": "gte", "value": 25,
                "label": "Maya corruption",
            }],
        }]
        template = normalize(data)
        self.assertEqual(len(template.quests_cards), 1)
        card = template.quests_cards[0]
        self.assertEqual(card.text, "Looking at him.")
        self.assertEqual(card.ready_text, "He sees it now.")
        self.assertEqual(card.tip, "Try the kitchen at dawn.")
        self.assertEqual(card.npc_id, "npc_a")
        self.assertEqual(card.priority, 1)
        self.assertEqual(len(card.when), 1)
        self.assertEqual(card.when[0].flag, "f_caught")
        self.assertEqual(card.when[0].op, "is_false")
        self.assertEqual(len(card.goals), 1)
        self.assertEqual(card.goals[0].trait, "corruption")
        self.assertEqual(card.goals[0].value, 25.0)
        self.assertEqual(card.goals[0].label, "Maya corruption")

    def test_v1_ignores_quest_cards_block(self):
        # V1 games should NOT populate template.quests_cards even if a
        # [[quest_cards]] block appears in the TOML (defensive — author may
        # be migrating but forgot the flag).
        data = _minimal_v1_toml()
        data["quest_cards"] = [{"text": "x", "when": [{"flag": "f", "op": "is_true"}]}]
        template = normalize(data)
        self.assertEqual(template.quests_cards, [])

    def test_terminal_field_parses(self):
        data = _minimal_v2_toml()
        data["quest_cards"] = [{
            "text": "Done.",
            "npc_id": "npc_a",
            "when": [{"flag": "f_done", "op": "is_true"}],
            "terminal": True,
        }]
        template = normalize(data)
        self.assertTrue(template.quests_cards[0].terminal)

    def test_serialize_omits_null_fields(self):
        from apps.projects.services.template_import import (
            QuestsCard, QuestsCondition, _serialize_quests_card,
        )
        card = QuestsCard(
            text="t",
            when=[QuestsCondition(flag="f", op="is_true")],
        )
        out = _serialize_quests_card(card)
        # Required fields present
        self.assertEqual(out["text"], "t")
        self.assertEqual(out["priority"], 0)
        self.assertEqual(out["when"], [{"flag": "f", "op": "is_true"}])
        # Optional fields NOT in output when null/empty
        self.assertNotIn("ready_text", out)
        self.assertNotIn("tip", out)
        self.assertNotIn("npc_id", out)
        self.assertNotIn("group", out)
        self.assertNotIn("goals", out)
        self.assertNotIn("ready_canvas", out)
        self.assertNotIn("terminal", out)

    def test_serialize_integer_value_stays_integer(self):
        # Smoke: 25 serializes as 25 (not 25.0) so the runtime label reads
        # "X / 25" not "X / 25.0".
        from apps.projects.services.template_import import (
            QuestsCard, QuestsCondition, _serialize_quests_card,
        )
        card = QuestsCard(
            text="t",
            when=[QuestsCondition(flag="f", op="is_true")],
            goals=[QuestsCondition(
                trait="corruption", subject="player", op="gte",
                value=25.0, label="Maya corruption",
            )],
        )
        out = _serialize_quests_card(card)
        self.assertEqual(out["goals"][0]["value"], 25)
        self.assertIsInstance(out["goals"][0]["value"], int)


class QuestsV2ValidatorTests(SimpleTestCase):
    """Validator hard-error rules from PRD 48 §3."""

    def test_missing_text_errors(self):
        data = _minimal_v2_toml()
        data["quest_cards"] = [{
            "text": "",
            "when": [{"flag": "f", "op": "is_true"}],
        }]
        template = normalize(data)
        errors = validate(template)
        self.assertTrue(any("text is required" in e for e in errors), errors)

    def test_missing_when_errors(self):
        data = _minimal_v2_toml()
        data["quest_cards"] = [{"text": "x"}]
        template = normalize(data)
        errors = validate(template)
        self.assertTrue(any("when is required" in e for e in errors), errors)

    def test_trait_goal_without_label_errors(self):
        data = _minimal_v2_toml()
        data["quest_cards"] = [{
            "text": "x",
            "when": [{"flag": "f", "op": "is_true"}],
            "goals": [{"trait": "corr", "subject": "player", "op": "gte", "value": 5}],
        }]
        template = normalize(data)
        errors = validate(template)
        self.assertTrue(any("must have a `label`" in e for e in errors), errors)

    def test_ready_canvas_unknown_slug_errors(self):
        data = _minimal_v2_toml()
        data["quest_cards"] = [{
            "text": "x",
            "npc_id": "npc_a",
            "when": [{"flag": "f", "op": "is_true"}],
            "ready_canvas": "scene_nonexistent",
        }]
        template = normalize(data)
        errors = validate(template)
        self.assertTrue(any("ready_canvas 'scene_nonexistent' not found" in e for e in errors), errors)

    def test_npc_id_unknown_slug_errors(self):
        data = _minimal_v2_toml()
        data["quest_cards"] = [{
            "text": "x",
            "npc_id": "npc_nonexistent",
            "when": [{"flag": "f", "op": "is_true"}],
        }]
        template = normalize(data)
        errors = validate(template)
        self.assertTrue(any("npc_id 'npc_nonexistent' not found" in e for e in errors), errors)

    def test_condition_with_both_flag_and_trait_errors(self):
        data = _minimal_v2_toml()
        data["quest_cards"] = [{
            "text": "x",
            "when": [{"flag": "f", "trait": "t", "subject": "player", "op": "is_true"}],
        }]
        template = normalize(data)
        errors = validate(template)
        self.assertTrue(any("ONLY ONE of `flag` or `trait`" in e for e in errors), errors)

    def test_condition_with_neither_flag_nor_trait_errors(self):
        data = _minimal_v2_toml()
        data["quest_cards"] = [{
            "text": "x",
            "when": [{"op": "is_true"}],
        }]
        template = normalize(data)
        errors = validate(template)
        self.assertTrue(any("must set either `flag` or `trait`" in e for e in errors), errors)

    def test_v1_validator_skips_quest_cards(self):
        # V1 game with a quest_cards block (defensive) — validator should
        # not touch it; no V2 hard errors should fire.
        data = _minimal_v1_toml()
        data["quest_cards"] = [{"text": "", "when": []}]  # would error under V2
        template = normalize(data)
        errors = validate(template)
        v2_errs = [e for e in errors if "quest_cards" in e]
        self.assertEqual(v2_errs, [], v2_errs)


class QuestsV2EmissionTests(SimpleTestCase):
    """Build dispatch tests — V1 vs V2 selection in v2.py."""

    def _v2_generator_with_metadata(self, metadata: dict):
        from unittest.mock import MagicMock
        from apps.game_generation.twee_comprehensive.generators.v2 import (
            TweeComprehensiveGeneratorV2,
        )
        gen = TweeComprehensiveGeneratorV2()
        gen.project = MagicMock()
        gen.project.metadata = metadata
        return gen

    def test_v1_dispatch_emits_v1_quests_block(self):
        gen = self._v2_generator_with_metadata({})
        block = gen._get_quests_block()
        self.assertIn(":: QuestsPage", block)
        self.assertIn("setup.getStageHintForNPC", block)
        self.assertIn("setup.getGlobalHints", block)
        self.assertIn("renderStageHint", block)
        self.assertNotIn(":: QuestsV2Script", block)
        self.assertNotIn("setup.pickQuestsCard", block)
        self.assertNotIn("renderQuestsCard", block)

    def test_v2_dispatch_emits_v2_overlay(self):
        gen = self._v2_generator_with_metadata({"quests_engine": "v2", "quests_cards": []})
        block = gen._get_quests_block()
        self.assertIn(":: QuestsV2Script", block)
        self.assertIn(":: QuestsV2Widgets", block)
        self.assertIn(":: QuestsV2Styles", block)
        self.assertIn(":: QuestsPage", block)
        self.assertIn("setup.pickQuestsCard", block)
        self.assertIn("setup.pickQuestsCards", block)
        self.assertIn("setup.evaluateGoals", block)
        self.assertIn("setup.checkQuestsCondition", block)
        self.assertIn("setup.renderQuestsGoalBlock", block)
        self.assertIn("setup.lookupCanvasBySlug", block)
        self.assertIn("renderQuestsCard", block)
        self.assertNotIn("setup.getStageHintForNPC", block)
        self.assertNotIn("renderStageHint", block)

    def test_v2_overlay_references_reused_v1_utilities(self):
        gen = self._v2_generator_with_metadata({"quests_engine": "v2", "quests_cards": []})
        block = gen._get_quests_block()
        self.assertIn("setup._formatCanvasSchedule", block)
        self.assertIn("setup._locNameFromUuid", block)
        self.assertIn("setup.npcSlugForId", block)
        self.assertIn("setup.npc_slug_map", block)

    def test_v2_overlay_three_frame_renderer(self):
        gen = self._v2_generator_with_metadata({"quests_engine": "v2", "quests_cards": []})
        block = gen._get_quests_block()
        self.assertIn("Arc complete", block)
        self.assertIn("Ready", block)
        self.assertIn("To advance:", block)


class QuestsV2SidebarStripTests(SimpleTestCase):
    """PRD 48 Commit 8 — verify the V2 generator strips the sidebar hint
    JS functions and widget branch from the output, while keeping the
    same functions intact for V1 games."""

    SIDEBAR_FNS = (
        "getSidebarHint",
        "getNextActivity",
        "formatFlagHint",
        "formatActivityHint",
        "getBestFlagHint",
        "resolveUnlockChain",
        "checkTraitRequirement",
        "calculateDaysRemaining",
    )

    def _strip_with_metadata(self, sample_output: str, metadata: dict) -> str:
        """Helper — instantiate the V2 generator with mock metadata and
        run the strip method against a sample output string."""
        from unittest.mock import MagicMock
        from apps.game_generation.twee_comprehensive.generators.v2 import (
            TweeComprehensiveGeneratorV2,
        )
        gen = TweeComprehensiveGeneratorV2()
        gen.project = MagicMock()
        gen.project.metadata = metadata
        return gen._strip_sidebar_mechanism_if_v2(sample_output)

    def _sample_output(self) -> str:
        # Minimal fixture covering every target the strip should remove,
        # plus shared utilities that must stay.
        return (
            "setup.getSidebarHint = function() {\n"
            "    var x = 1;\n"
            "    return x;\n"
            "};\n"
            "setup.getNextActivity = function(npcId) {\n"
            "    return null;\n"
            "};\n"
            "setup.formatFlagHint = function(h, n) {\n"
            "    return '';\n"
            "};\n"
            "setup.formatActivityHint = function(a) {\n"
            "    return '';\n"
            "};\n"
            "setup.getBestFlagHint = function(unmet) {\n"
            "    return null;\n"
            "};\n"
            "setup.resolveUnlockChain = function(k, m, v, d) {\n"
            "    return null;\n"
            "};\n"
            "setup.checkTraitRequirement = function(r) {\n"
            "    return true;\n"
            "};\n"
            "setup.calculateDaysRemaining = function(c) {\n"
            "    return 0;\n"
            "};\n"
            "setup.formatCanvasConditions = function(c) {\n"
            "    return 'Required: x';\n"
            "};\n"
            "setup.checkSingleCondition = function(c) { return true; };\n"
            '  <<elseif _item.type is "hint">>\n'
            "    <<set _hintText to setup.getSidebarHint()>>\n"
            "    <<if _hintText>>\n"
            '      <div>...</div>\n'
            "    <</if>>\n"
            '  <<elseif _item.type is "trait_bar">>\n'
            "    <<set _next to 1>>\n"
        )

    def test_v1_metadata_keeps_everything(self):
        # No quests_engine flag → treated as V1 → no strip.
        output = self._strip_with_metadata(self._sample_output(), {})
        for fn in self.SIDEBAR_FNS:
            self.assertIn(
                f"setup.{fn} = function", output,
                f"V1 emission must keep {fn}",
            )
        self.assertIn('_item.type is "hint"', output)
        self.assertIn("setup.formatCanvasConditions", output)
        self.assertIn("setup.checkSingleCondition", output)

    def test_v2_metadata_strips_sidebar_fns(self):
        output = self._strip_with_metadata(
            self._sample_output(), {"quests_engine": "v2"},
        )
        for fn in self.SIDEBAR_FNS:
            self.assertNotIn(
                f"setup.{fn} = function", output,
                f"V2 emission must strip {fn}",
            )

    def test_v2_metadata_strips_hint_widget_branch(self):
        output = self._strip_with_metadata(
            self._sample_output(), {"quests_engine": "v2"},
        )
        self.assertNotIn('_item.type is "hint"', output)
        # Adjacent trait_bar branch must remain.
        self.assertIn('_item.type is "trait_bar"', output)

    def test_v2_metadata_keeps_format_canvas_conditions(self):
        # formatCanvasConditions is shared with location-blocking UI;
        # must NOT be stripped even under V2.
        output = self._strip_with_metadata(
            self._sample_output(), {"quests_engine": "v2"},
        )
        self.assertIn("setup.formatCanvasConditions = function", output)

    def test_v2_metadata_keeps_shared_utilities(self):
        # Shared utilities used by Quests engine + other systems must stay.
        output = self._strip_with_metadata(
            self._sample_output(), {"quests_engine": "v2"},
        )
        self.assertIn("setup.checkSingleCondition", output)
