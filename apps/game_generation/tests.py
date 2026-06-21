"""
Tests for Game Generation System.

Comprehensive tests for the modular game generation architecture.
"""

import unittest
from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.game_generation.services.game_service import GameService
from apps.game_generation.twee_comprehensive.services import TweeComprehensiveService
from apps.game_generation.twee_navigation.services import TweeNavigationService
from apps.projects.models import Project

User = get_user_model()


class GameServiceTestCase(TestCase):
    """Test cases for the unified GameService API."""

    def setUp(self):
        """Set up test environment."""
        self.service = GameService()
        self.user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )
        self.project = Project.objects.create(
            name="Test Project",
            owner=self.user,
            description="Test project for game generation",
        )

    def test_available_systems(self):
        """Test getting list of available game generation systems."""
        systems = self.service.get_available_systems()

        # Should have our two registered systems
        self.assertEqual(len(systems), 2)

        # Check twee_navigation system
        twee_nav = next(s for s in systems if s["system_type"] == "twee_navigation")
        self.assertIsNotNone(twee_nav)
        self.assertIn("description", twee_nav)
        self.assertIn("Simple navigation", twee_nav["description"])

        # Check twee_comprehensive system
        twee_comp = next(s for s in systems if s["system_type"] == "twee_comprehensive")
        self.assertIsNotNone(twee_comp)
        self.assertIn("Sophisticated interactive", twee_comp["description"])

    def test_invalid_system_type(self):
        """Test that invalid system type raises appropriate error."""
        with self.assertRaises(ValueError) as context:
            self.service.generate_game(self.project, "invalid_system", "v1")

        self.assertIn("Unknown system type", str(context.exception))
        self.assertIn("invalid_system", str(context.exception))

    def test_system_service_loading(self):
        """Test dynamic loading of system services."""
        # Test loading twee_navigation service
        nav_service = self.service._get_system_service("twee_navigation")
        self.assertIsInstance(nav_service, TweeNavigationService)

        # Test loading twee_comprehensive service
        comp_service = self.service._get_system_service("twee_comprehensive")
        self.assertIsInstance(comp_service, TweeComprehensiveService)

    @patch("apps.game_generation.services.game_service.subprocess.run")
    def test_tweego_compilation(self, mock_subprocess):
        """Test Tweego compilation when available."""
        # Mock successful Tweego execution
        mock_subprocess.return_value = Mock(
            returncode=0, stdout="Tweego version 2.1.1", stderr=""
        )

        twee_content = ":: Start\nWelcome to the game!"

        # Test compilation (will use fallback since we're mocking)
        with patch("builtins.open", create=True) as mock_open:
            mock_open.return_value.__enter__ = Mock()
            mock_open.return_value.__exit__ = Mock()

            result = self.service._try_tweego_compilation(twee_content, "Test Game")

            # Should attempt to run Tweego
            self.assertTrue(mock_subprocess.called)

    def test_html_fallback_generation(self):
        """Test HTML fallback when Tweego is not available."""
        twee_content = ":: Start\nThis is test content."
        project_name = "Test Game"

        html = self.service._generate_html_fallback(twee_content, project_name)

        # Check basic HTML structure
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn(f"<title>{project_name}</title>", html)
        self.assertIn(twee_content, html)
        self.assertIn("Basic Preview Mode", html)


class TweeNavigationServiceTestCase(TestCase):
    """Test cases for the TweeNavigationService."""

    def setUp(self):
        """Set up test environment."""
        self.service = TweeNavigationService()
        self.user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )
        self.project = Project.objects.create(name="Navigation Test", owner=self.user)

    def test_project_validation_empty(self):
        """Test validation of empty project."""
        result = self.service.validate_project(self.project)

        self.assertTrue(result["has_errors"])
        self.assertIn("errors", result)
        self.assertIn("No story canvases found", result["errors"][0])

    def test_capabilities(self):
        """Test getting service capabilities."""
        capabilities = self.service.get_capabilities()

        self.assertEqual(capabilities["system_type"], "twee_navigation")
        self.assertIn("versions", capabilities)
        self.assertIn("v1", capabilities["versions"])
        self.assertEqual(capabilities["output_format"], "twee")

        # Check features
        self.assertIn("features", capabilities)
        self.assertIn("Basic navigation", capabilities["features"])

    def test_invalid_version(self):
        """Test that invalid version raises error."""
        with self.assertRaises(ValueError) as context:
            self.service.generate(self.project, "v99")

        self.assertIn("Version v99 not found", str(context.exception))


class TweeComprehensiveServiceTestCase(TestCase):
    """Test cases for the TweeComprehensiveService."""

    def setUp(self):
        """Set up test environment."""
        self.service = TweeComprehensiveService()
        self.user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )
        self.project = Project.objects.create(
            name="Comprehensive Test", owner=self.user
        )

    def test_project_validation_warnings(self):
        """Test validation warnings for project without content."""
        result = self.service.validate_project(self.project)

        # Should have warnings but not errors for comprehensive
        self.assertFalse(result["has_errors"])
        self.assertIn("warnings", result)
        self.assertTrue(len(result["warnings"]) > 0)

    def test_capabilities(self):
        """Test getting service capabilities."""
        capabilities = self.service.get_capabilities()

        self.assertEqual(capabilities["system_type"], "twee_comprehensive")
        self.assertIn("versions", capabilities)
        self.assertIn("v1", capabilities["versions"])

        # Check comprehensive features
        self.assertIn("features", capabilities)
        features = capabilities["features"]
        self.assertIn("Character progression", features)
        self.assertIn("NPC interactions", features)
        self.assertIn("Location discovery", features)

        # Check layers
        self.assertIn("layers", capabilities)
        layers = capabilities["layers"]
        self.assertIn("Foundation Layer", layers[0])
        self.assertIn("Character Layer", layers[1])


class GameGenerationAPITestCase(TestCase):
    """Test cases for game generation API endpoints."""

    def setUp(self):
        """Set up test environment."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )
        self.project = Project.objects.create(name="API Test Project", owner=self.user)

        # Generate JWT token
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    @patch("apps.game_generation.services.game_service.GameService.generate_game")
    @patch(
        "apps.game_generation.services.game_service.GameService.compile_twee_to_html"
    )
    def test_preview_navigation_game(self, mock_compile, mock_generate):
        """Test preview navigation game endpoint."""
        mock_generate.return_value = ":: Start\nTest game content"
        mock_compile.return_value = "<html><body>Test HTML</body></html>"

        response = self.client.post(
            f"/api/v1/foundation/projects/{self.project.id}/preview-game"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/html")
        self.assertIn("no-cache", response["Cache-Control"])

        # Verify service was called correctly
        mock_generate.assert_called_once_with(self.project, "twee_navigation", "v1")
        mock_compile.assert_called_once()

    @patch("apps.game_generation.services.game_service.GameService.generate_game")
    @patch(
        "apps.game_generation.services.game_service.GameService.compile_twee_to_html"
    )
    def test_preview_comprehensive_game(self, mock_compile, mock_generate):
        """Test preview comprehensive game endpoint."""
        mock_generate.return_value = ":: Start\nComprehensive content"
        mock_compile.return_value = "<html><body>Comprehensive HTML</body></html>"

        response = self.client.post(
            f"/api/v1/foundation/projects/{self.project.id}/preview-comprehensive-game"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/html")

        # Verify comprehensive system was used
        mock_generate.assert_called_once_with(self.project, "twee_comprehensive", "v1")

    @patch("apps.game_generation.services.game_service.GameService.generate_game")
    def test_generate_twee_file(self, mock_generate):
        """Test generating Twee file for download."""
        mock_generate.return_value = ":: Start\nDownloadable content"

        response = self.client.post(
            f"/api/v1/foundation/projects/{self.project.id}/generate-game?format=twee"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/plain")
        self.assertIn("attachment", response["Content-Disposition"])
        self.assertIn(".twee", response["Content-Disposition"])

    def test_invalid_project_id(self):
        """Test accessing non-existent project."""
        response = self.client.post(
            "/api/v1/foundation/projects/99999999-9999-9999-9999-999999999999/preview-game"
        )

        self.assertEqual(response.status_code, 404)
        self.assertIn("Project Not Found", response.content.decode())

    def test_unauthorized_access(self):
        """Test accessing without authentication."""
        self.client.credentials()  # Remove auth

        response = self.client.post(
            f"/api/v1/foundation/projects/{self.project.id}/preview-game"
        )

        self.assertEqual(response.status_code, 401)


class SystemIsolationTestCase(TestCase):
    """Test cases to verify system isolation."""

    def test_systems_are_isolated(self):
        """Verify that systems don't share dependencies."""
        # Import both generator modules
        from apps.game_generation.twee_comprehensive.generators import v1 as comp_v1
        from apps.game_generation.twee_navigation.generators import v1 as nav_v1

        # Check they have their own generator classes
        self.assertTrue(hasattr(nav_v1, "BasicTweeGeneratorV1"))
        self.assertTrue(hasattr(comp_v1, "TweeComprehensiveGeneratorV1"))

        # Verify they're different classes
        self.assertNotEqual(
            nav_v1.BasicTweeGeneratorV1, comp_v1.TweeComprehensiveGeneratorV1
        )

    def test_service_isolation(self):
        """Verify services are isolated."""
        nav_service = TweeNavigationService()
        comp_service = TweeComprehensiveService()

        # Check they have different validation logic
        nav_caps = nav_service.get_capabilities()
        comp_caps = comp_service.get_capabilities()

        self.assertNotEqual(nav_caps["features"], comp_caps["features"])
        self.assertNotEqual(nav_caps["description"], comp_caps["description"])


class V2ForkTests(TestCase):
    """Tests guarding the v1 → v2 fork (2026-05-14).

    v2 was created as a wholesale copy of v1, with v2 becoming the default.
    v1 is frozen as a safe-mode rollback. These tests prove:
      1. v2 is importable + has the same public interface.
      2. v1 and v2 produce byte-identical output at fork time (the freeze
         guarantee — when v2 deliberately diverges, this test gets scoped or
         replaced with version-specific equivalence tests).
    """

    def test_v2_class_importable_with_same_interface(self):
        from apps.game_generation.twee_comprehensive.generators import v2 as comp_v2
        from apps.game_generation.twee_comprehensive.generators import v1 as comp_v1

        self.assertTrue(hasattr(comp_v2, "TweeComprehensiveGeneratorV2"))
        self.assertTrue(hasattr(comp_v1, "TweeComprehensiveGeneratorV1"))

        # Same public method signature — both expose generate(project, options).
        v1_gen = comp_v1.TweeComprehensiveGeneratorV1
        v2_gen = comp_v2.TweeComprehensiveGeneratorV2
        self.assertTrue(callable(getattr(v1_gen, "generate", None)))
        self.assertTrue(callable(getattr(v2_gen, "generate", None)))

    def test_services_default_is_v2(self):
        """Default version should be v2 (set during fork on 2026-05-14)."""
        import inspect

        service = TweeComprehensiveService()
        sig = inspect.signature(service.generate)
        self.assertEqual(sig.parameters["version"].default, "v2")

        caps = service.get_capabilities()
        self.assertIn("v2", caps["versions"])
        self.assertEqual(caps["current_version"], "v2")

    @unittest.skip(
        "v2 deliberately diverges from v1 starting 2026-05-14 (Phase A: NPC "
        "schedule primitive + requires_npc + getNpcLocation rewrite + "
        "renderNpcPortraits gating). The byte-equality guarantee no longer "
        "holds. See memory v2_engine_fork.md + the Phase A plan. Replace with "
        "version-specific equivalence tests as v2 evolves."
    )
    def test_v1_v2_byte_equality_at_fork(self):
        """v1 and v2 must produce byte-identical output until v2 diverges.

        Uses the same fixture pattern as apps/projects/tests.py — load the
        engine PRD fixture TOML, build a Project, run both generators, diff.
        """
        import copy
        from pathlib import Path

        import tomli

        from apps.projects.services.template_import import (
            normalize,
            validate,
            create_project_from_template,
        )
        from apps.game_generation.twee_comprehensive.generators.v1 import (
            TweeComprehensiveGeneratorV1,
        )
        from apps.game_generation.twee_comprehensive.generators.v2 import (
            TweeComprehensiveGeneratorV2,
        )

        fixture_path = (
            Path(__file__).resolve().parent
            / "games_toml_files"
            / "engine_prd_2026_04_22.toml"
        )
        with open(fixture_path, "rb") as f:
            toml_data = tomli.load(f)

        user = User.objects.create_user(
            email="v2-fork-byte-equality@example.com", password="testpass123"
        )
        template = normalize(copy.deepcopy(toml_data))
        errors = validate(template)
        self.assertEqual(errors, [], f"Fixture should validate clean: {errors}")
        result = create_project_from_template(template, str(user.id))
        project = Project.objects.get(id=result["project_id"])

        v1_twee = TweeComprehensiveGeneratorV1().generate(project)
        v2_twee = TweeComprehensiveGeneratorV2().generate(project)

        self.assertEqual(
            v1_twee,
            v2_twee,
            "v1 and v2 must produce byte-identical output at fork. "
            "If this fails, either v2 has drifted (likely the cause if you "
            "haven't intentionally diverged it yet) or the fork-copy was "
            "incomplete. Scope this test once v2 deliberately diverges.",
        )


class PhaseANpcScheduleTests(TestCase):
    """Phase A (2026-05-14) — NPC schedule primitive + requires_npc gate.

    Verifies the engine extension that lifts NPC location into a first-class
    declaration consumed by Lane 2/3 random encounters and substitutions.
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="phase-a-npc-schedule@example.com", password="testpass123"
        )

    def _build_minimal_template(self, *, with_schedule=True, requires_npc=None,
                                 trigger_npc=None):
        """Synthesize a minimal valid template dict for normalize/validate.

        Returns the parsed/normalized template ready for create_project_from_template.
        """
        loc_id = "loc_kitchen"
        npc_id = "npc_test"
        canvas_id = "canvas_test_random"
        template_dict = {
            "schema_version": "1.0",
            "project": {
                "id": "phase_a_test",
                "title": "Phase A Schedule Fixture",
                "description": "Minimal fixture for testing NPC schedule primitive.",
                "starting_canvas": canvas_id,
            },
            "time": {"enabled": True, "starting_hour": 8, "starting_day": "Monday"},
            "locations": [
                {"id": loc_id, "name": "Kitchen", "description": "Test kitchen"},
            ],
            "npcs": [
                {
                    "id": npc_id,
                    "name": "Test NPC",
                    "description": "Fixture NPC",
                    "core_traits": {},
                    "flag_keys": [],
                },
            ],
            "canvases": [
                {
                    "id": canvas_id,
                    "name": "Test Random Canvas",
                    "type": "scene",
                    "trigger": {
                        "location": loc_id,
                        "is_active": True,
                        "is_repeatable": True,
                        "trigger_mode": "random",
                        "chance": 0.5,
                    },
                    "nodes": [
                        {
                            "id": "n1",
                            "name": "Test Node 1",
                            "blocks": [
                                {"type": "paragraph", "props": {},
                                 "content": [{"type": "text", "text": "test"}]}
                            ],
                        }
                    ],
                },
            ],
        }
        if with_schedule:
            template_dict["npcs"][0]["schedules"] = [
                {
                    "location": loc_id,
                    "weekdays": [0, 1, 2, 3, 4],
                    "start_time": "06:00",
                    "end_time": "10:00",
                    "activity": "morning coffee",
                },
            ]
        if requires_npc is not None:
            template_dict["canvases"][0]["trigger"]["requires_npc"] = requires_npc
        if trigger_npc is not None:
            template_dict["canvases"][0]["trigger"]["npc"] = trigger_npc
        return template_dict

    def _build_and_generate(self, raw):
        """Helper: normalize+validate+create+generate. Returns (project, twee)."""
        import copy
        from apps.projects.services.template_import import (
            normalize, validate, create_project_from_template,
        )
        from apps.game_generation.twee_comprehensive.generators.v2 import (
            TweeComprehensiveGeneratorV2,
        )
        template = normalize(copy.deepcopy(raw))
        errors = validate(template)
        self.assertEqual(errors, [], f"Fixture should validate clean: {errors}")
        result = create_project_from_template(template, str(self.user.id))
        project = Project.objects.get(id=result["project_id"])
        twee = TweeComprehensiveGeneratorV2().generate(project)
        return project, twee

    @staticmethod
    def _extract_setup_assignment(twee, varname):
        """Pull the JSON value from a `setup.<varname> = {...};` line in the Twee."""
        import json
        import re
        # Find the assignment, then balanced-brace scan for the JSON object.
        m = re.search(r'setup\.' + re.escape(varname) + r'\s*=\s*', twee)
        if not m:
            return None
        start = m.end()
        if start >= len(twee) or twee[start] != '{':
            return None
        depth = 0
        for i in range(start, len(twee)):
            ch = twee[i]
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    return json.loads(twee[start:i + 1])
        return None

    def test_npc_schedule_emitted_into_setup_blob(self):
        """When TOML declares [[npcs.schedules]], setup.npcSchedules contains
        a structured entry keyed by NPC slug. Strengthened post-bugfix to
        parse the actual JSON instead of relying on substring presence."""
        raw = self._build_minimal_template(with_schedule=True)
        _, twee = self._build_and_generate(raw)

        npc_schedules = self._extract_setup_assignment(twee, "npcSchedules")
        self.assertIsNotNone(npc_schedules,
                             "setup.npcSchedules assignment must be parseable JSON")
        self.assertIn("npc_test", npc_schedules,
                      "Schedule blob must be keyed by NPC slug")
        entries = npc_schedules["npc_test"]
        self.assertEqual(len(entries), 1, "One declared schedule entry expected")
        entry = entries[0]
        self.assertEqual(entry["start_time"], "06:00")
        self.assertEqual(entry["end_time"], "10:00")
        self.assertEqual(entry["weekdays"], [0, 1, 2, 3, 4])
        self.assertEqual(entry["activity"], "morning coffee")

    def test_schedule_location_emitted_as_uuid_not_slug(self):
        """Phase A bugfix (2026-05-14 PM) regression test.

        The schedule entry's `location` field must be a UUID matching
        setup.locations[slug].id — runtime gates compare with raw `===`
        against UUIDs ($player.current_location, locationCanvases keys).
        Pre-bugfix this field was the literal slug 'loc_kitchen', which
        never matched any runtime UUID, silently breaking all three Phase A
        gates (Lane 2 random, Lane 3 substitution, NPC portrait filter).
        """
        import uuid as uuid_mod
        raw = self._build_minimal_template(with_schedule=True)
        _, twee = self._build_and_generate(raw)

        npc_schedules = self._extract_setup_assignment(twee, "npcSchedules")
        locations = self._extract_setup_assignment(twee, "locations")
        self.assertIsNotNone(npc_schedules)
        self.assertIsNotNone(locations)
        self.assertIn("loc_kitchen", locations,
                      "setup.locations must contain the declared location slug")
        expected_uuid = locations["loc_kitchen"]["id"]

        entry = npc_schedules["npc_test"][0]
        self.assertEqual(
            entry["location"], expected_uuid,
            f"Schedule entry location must be the runtime UUID "
            f"({expected_uuid}), not a slug. Got: {entry['location']!r}. "
            f"This is the bug that broke all Phase A runtime gates."
        )
        # Sanity: the field must look like a UUID, not a slug.
        try:
            uuid_mod.UUID(entry["location"])
        except (ValueError, TypeError):
            self.fail(
                f"Schedule entry.location {entry['location']!r} is not a valid "
                f"UUID — runtime `===` comparisons against $player.current_location "
                f"will never match."
            )
        # Debug field carrying original slug must also be present.
        self.assertEqual(
            entry.get("location_slug"), "loc_kitchen",
            "location_slug debug field must carry the original TOML slug "
            "so a developer inspecting setup.npcSchedules in DevTools can "
            "trace back to the source location declaration."
        )

    def test_requires_npc_validator_rejects_unknown_npc(self):
        """trigger.requires_npc pointing at a non-existent NPC must error out."""
        import copy
        from apps.projects.services.template_import import normalize, validate

        raw = self._build_minimal_template(requires_npc="ghost_npc")
        template = normalize(copy.deepcopy(raw))
        errors = validate(template)

        matching = [e for e in errors if "requires_npc" in e and "ghost_npc" in e]
        self.assertTrue(
            matching,
            f"Expected validate() to reject unknown requires_npc 'ghost_npc'. "
            f"Got errors: {errors}"
        )

    def test_trigger_npc_validator_rejects_unknown_npc_gap_fix(self):
        """Gap-fix: trigger.npc pointing at a non-existent NPC must now error.

        Previously trigger.npc was read by 3 downstream validators but never
        cross-referenced. Phase A closes that gap.
        """
        import copy
        from apps.projects.services.template_import import normalize, validate

        raw = self._build_minimal_template(trigger_npc="ghost_npc")
        template = normalize(copy.deepcopy(raw))
        errors = validate(template)

        matching = [e for e in errors if "trigger.npc" in e and "ghost_npc" in e]
        self.assertTrue(
            matching,
            f"Expected validate() to reject unknown trigger.npc 'ghost_npc'. "
            f"Got errors: {errors}"
        )

    def test_npc_schedule_no_longer_emits_deprecation_warning(self):
        """Declaring [[npcs.schedules]] used to emit DeprecationWarning. Phase A undoes that."""
        import copy
        import warnings
        from apps.projects.services.template_import import normalize, validate

        raw = self._build_minimal_template(with_schedule=True)
        template = normalize(copy.deepcopy(raw))

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            errors = validate(template)
            dep_warnings = [warning for warning in w
                           if issubclass(warning.category, DeprecationWarning)
                           and "npcs.schedules" in str(warning.message)]

        self.assertEqual(errors, [], f"Fixture should validate clean: {errors}")
        self.assertEqual(
            dep_warnings, [],
            f"DeprecationWarning for [[npcs.schedules]] should be gone. "
            f"Got: {[str(w.message) for w in dep_warnings]}"
        )


class NpcAtLocationConditionTests(TestCase):
    """Shared-space occupancy predicate (redesign_phase_3/25).

    The `npc_at_location` condition type asks cross-room NPC presence — the
    foundation of peep / occupied-bathroom / caught. It validates permissively
    (condition types have no allowlist) and emits an evaluator branch in
    `triggerConditionsSatisfied` plus the `getNpcsAtLocation` helper that backs
    the any-NPC (room occupied/empty) form.

    NOTE: the evaluator is JS embedded in a string template; the Python suite does
    NOT execute it. These tests prove *emitted + validates*, not runtime gating —
    runtime correctness is a live-play check (a peep/occupied canvas in a real game).
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="npc-at-location@example.com", password="testpass123"
        )

    def _template(self, condition_items, *, entry_conditions=None):
        loc_id = "loc_bathroom"
        hall_id = "loc_hallway"
        npc_id = "npc_frank"
        canvas_id = "canvas_peep"
        td = {
            "schema_version": "1.0",
            "project": {
                "id": "occ_test",
                "title": "Occupancy Fixture",
                "description": "Minimal fixture for npc_at_location.",
                "starting_canvas": canvas_id,
            },
            "time": {"enabled": True, "starting_hour": 8, "starting_day": "Monday"},
            "locations": [
                {"id": hall_id, "name": "Hallway", "description": "The hallway"},
                {"id": loc_id, "name": "Bathroom", "description": "Shared bath"},
            ],
            "npcs": [
                {
                    "id": npc_id,
                    "name": "Frank",
                    "description": "Fixture NPC",
                    "core_traits": {},
                    "flag_keys": [],
                    "schedules": [
                        {
                            "location": loc_id,
                            "weekdays": [0, 1, 2, 3, 4, 5, 6],
                            "start_time": "06:00",
                            "end_time": "10:00",
                            "activity": "showering",
                        },
                    ],
                },
            ],
            "canvases": [
                {
                    "id": canvas_id,
                    "name": "Peep Canvas",
                    "type": "scene",
                    "trigger": {
                        "location": hall_id,
                        "is_active": True,
                        "is_repeatable": True,
                        "trigger_mode": "random",
                        "chance": 0.5,
                        "conditions": {"version": "1.0", "items": condition_items},
                    },
                    "nodes": [
                        {
                            "id": "n1",
                            "name": "Test Node 1",
                            "blocks": [
                                {"type": "paragraph", "props": {},
                                 "content": [{"type": "text", "text": "test"}]}
                            ],
                        }
                    ],
                },
            ],
        }
        if entry_conditions is not None:
            for loc in td["locations"]:
                if loc["id"] == loc_id:
                    loc["entry_conditions"] = entry_conditions
                    loc["blocked_message"] = "The door's shut. Someone's in there."
        return td

    def _build_and_generate(self, raw):
        import copy
        from apps.projects.services.template_import import (
            normalize, validate, create_project_from_template,
        )
        from apps.game_generation.twee_comprehensive.generators.v2 import (
            TweeComprehensiveGeneratorV2,
        )
        template = normalize(copy.deepcopy(raw))
        errors = validate(template)
        self.assertEqual(errors, [], f"Fixture should validate clean: {errors}")
        result = create_project_from_template(template, str(self.user.id))
        project = Project.objects.get(id=result["project_id"])
        twee = TweeComprehensiveGeneratorV2().generate(project)
        return project, twee

    def test_all_forms_validate_clean(self):
        """present/absent, specific-NPC and any-NPC forms validate with no errors
        (condition types are permissive — no allowlist registration needed)."""
        import copy
        from apps.projects.services.template_import import normalize, validate
        items = [
            {"type": "npc_at_location", "npc_id": "npc_frank",
             "location_id": "loc_bathroom", "operator": "is_present"},
            {"type": "npc_at_location", "npc_id": "npc_frank",
             "location_id": "loc_bathroom", "operator": "is_absent"},
            {"type": "npc_at_location", "location_id": "loc_bathroom",
             "operator": "is_present"},
        ]
        template = normalize(copy.deepcopy(self._template(items)))
        errors = validate(template)
        self.assertEqual(errors, [],
                         f"npc_at_location should validate clean: {errors}")

    def test_evaluator_branch_and_helper_emitted(self):
        """The generated runtime carries the npc_at_location evaluator branch and
        the getNpcsAtLocation helper backing the any-NPC occupancy form."""
        raw = self._template([
            {"type": "npc_at_location", "npc_id": "npc_frank",
             "location_id": "loc_bathroom", "operator": "is_present"},
        ])
        _, twee = self._build_and_generate(raw)
        self.assertIn("type === 'npc_at_location'", twee,
                      "evaluator must dispatch the npc_at_location condition type")
        self.assertIn("setup.getNpcsAtLocation", twee,
                      "the any-NPC occupancy helper must be emitted")

    def test_entry_conditions_occupied_block_builds(self):
        """A location whose entry_conditions use npc_at_location(is_absent) — the
        'bathroom occupied, can't enter' shape — builds, validates, and generates."""
        raw = self._template(
            [{"type": "npc_at_location", "npc_id": "npc_frank",
              "location_id": "loc_bathroom", "operator": "is_present"}],
            entry_conditions={"version": "1.0", "items": [
                {"type": "npc_at_location", "location_id": "loc_bathroom",
                 "operator": "is_absent"},
            ]},
        )
        _, twee = self._build_and_generate(raw)
        self.assertIn("type === 'npc_at_location'", twee)

    def test_nav_presence_badge_is_schedule_occupancy(self):
        """The nav-card "someone's here" badge uses schedule-occupancy
        (getNpcsPresentAtLocation → getNpcsAtLocation) — the SAME logic as the
        door — so the map and the occupied-bathroom block always agree. The old
        canvas-gated feeder is gone; the clickable portrait grid
        (renderNpcPortraits) stays canvas-gated."""
        raw = self._template([
            {"type": "npc_at_location", "npc_id": "npc_frank",
             "location_id": "loc_bathroom", "operator": "is_present"},
        ])
        _, twee = self._build_and_generate(raw)
        self.assertIn("setup.getNpcsPresentAtLocation", twee,
                      "nav presence feeder must be the schedule-based one")
        self.assertNotIn("getNpcsWithCanvasesAtLocation", twee,
                         "the old canvas-gated nav feeder must be gone")
        i = twee.find("setup.getNpcsPresentAtLocation = function")
        body = twee[i:i + 800]
        self.assertIn("setup.getNpcsAtLocation", body,
                      "nav presence must seed from schedule-occupancy")
        self.assertNotIn("selectNpcPortraitCanvasesForLocation", body,
                         "nav presence must NOT require a canvas")


class Doc69FieldNameValidatorTests(TestCase):
    """Doc 69 Item 3 — Field-name mismatch validator.

    The TLS engine uses different field names for effects vs predicates:
      - Effect schema: `targetType` / `npcId` / `trait` / `flag` / `op`
      - Predicate schema: `subject` / `npc_id` / `trait_key` / `flag_key` / `operator`

    Mixing them causes silent no-op at runtime. These tests verify the
    validator catches mismatches at build time with helpful error messages
    citing Doc 68 §7.6.
    """

    def _build_minimal_template(self):
        """Minimal valid template — same shape as PhaseANpcScheduleTests fixture.

        Caller mutates the returned dict to inject effect/predicate field-name
        mismatches at the desired location.
        """
        return {
            "schema_version": "1.0",
            "project": {
                "id": "doc69_test",
                "title": "Doc 69 Field-Name Validator Fixture",
                "description": "Minimal fixture for field-name mismatch testing.",
                "starting_canvas": "canvas_test",
            },
            "time": {"enabled": True, "starting_hour": 8, "starting_day": "Monday"},
            "player": {
                "id": "player",
                "name": "Test Player",
                "core_traits": {"corruption": 0, "arousal": 0},
                "flag_keys": ["test_flag"],
            },
            "locations": [
                {"id": "loc_kitchen", "name": "Kitchen", "description": "Test"},
            ],
            "npcs": [
                {
                    "id": "npc_test",
                    "name": "Test NPC",
                    "description": "Fixture NPC",
                    "core_traits": {"relation": 0},
                    "flag_keys": [],
                },
            ],
            "canvases": [
                {
                    "id": "canvas_test",
                    "name": "Test Canvas",
                    "type": "scene",
                    "trigger": {
                        "location": "loc_kitchen",
                        "is_active": True,
                        "is_repeatable": True,
                        "trigger_mode": "manual",
                    },
                    "nodes": [
                        {
                            "id": "n1",
                            "name": "Test Node",
                            "blocks": [{"type": "paragraph", "props": {},
                                        "content": [{"type": "text", "text": "test"}]}],
                            "exit_block": {
                                "type": "choices",
                                "choices": [
                                    {
                                        "text": "Continue",
                                        "targetType": "trigger",
                                        "effects": [],
                                    },
                                ],
                            },
                        },
                    ],
                },
            ],
        }

    def _validate_template(self, raw):
        """Helper: normalize + validate, return error list."""
        import copy
        from apps.projects.services.template_import import normalize, validate
        template = normalize(copy.deepcopy(raw))
        return validate(template), template

    # ─── Effect-context mismatches (5 tests) ────────────────────────────────

    def test_effect_with_subject_field_errors(self):
        """Effect dict using predicate's `subject` field → ERROR."""
        raw = self._build_minimal_template()
        raw["canvases"][0]["nodes"][0]["exit_block"]["choices"][0]["effects"].append({
            "subject": "player",  # WRONG — predicate field in effect context
            "trait": "corruption",
            "op": "add",
            "value": 1,
        })
        errors, _ = self._validate_template(raw)
        matching = [e for e in errors if "`subject`" in e and "Doc 68" in e]
        self.assertTrue(matching,
                        f"Expected error for `subject` in effect context. Got: {errors}")

    def test_effect_with_trait_key_field_errors(self):
        """Effect dict using predicate's `trait_key` field → ERROR."""
        raw = self._build_minimal_template()
        raw["canvases"][0]["nodes"][0]["exit_block"]["choices"][0]["effects"].append({
            "targetType": "player",
            "trait_key": "corruption",  # WRONG — should be `trait`
            "op": "add",
            "value": 1,
        })
        errors, _ = self._validate_template(raw)
        matching = [e for e in errors if "`trait_key`" in e and "Doc 68" in e]
        self.assertTrue(matching,
                        f"Expected error for `trait_key` in effect context. Got: {errors}")

    def test_effect_with_npc_id_field_errors(self):
        """Effect dict using predicate's `npc_id` field → ERROR."""
        raw = self._build_minimal_template()
        raw["canvases"][0]["nodes"][0]["exit_block"]["choices"][0]["effects"].append({
            "targetType": "npc",
            "npc_id": "npc_test",  # WRONG — should be `npcId`
            "trait": "relation",
            "op": "add",
            "value": 1,
        })
        errors, _ = self._validate_template(raw)
        matching = [e for e in errors if "`npc_id`" in e and "Doc 68" in e]
        self.assertTrue(matching,
                        f"Expected error for `npc_id` in effect context. Got: {errors}")

    def test_effect_with_operator_field_errors(self):
        """Effect dict using predicate's `operator` field → ERROR."""
        raw = self._build_minimal_template()
        raw["canvases"][0]["nodes"][0]["exit_block"]["choices"][0]["effects"].append({
            "targetType": "player",
            "trait": "corruption",
            "operator": "add",  # WRONG — should be `op`
            "value": 1,
        })
        errors, _ = self._validate_template(raw)
        matching = [e for e in errors if "`operator`" in e and "Doc 68" in e]
        self.assertTrue(matching,
                        f"Expected error for `operator` in effect context. Got: {errors}")

    def test_effect_with_flag_key_field_errors(self):
        """Flag-effect dict using predicate's `flag_key` field → ERROR."""
        raw = self._build_minimal_template()
        raw["canvases"][0]["nodes"][0]["exit_block"]["choices"][0]["flagEffects"] = [{
            "targetType": "player",
            "flag_key": "test_flag",  # WRONG — should be `flag`
            "op": "set",
        }]
        errors, _ = self._validate_template(raw)
        matching = [e for e in errors if "`flag_key`" in e and "Doc 68" in e]
        self.assertTrue(matching,
                        f"Expected error for `flag_key` in flag-effect context. Got: {errors}")

    # ─── Predicate-context mismatches (5 tests) ─────────────────────────────

    def test_predicate_with_targetType_field_errors(self):
        """Predicate item using effect's `targetType` field → ERROR."""
        raw = self._build_minimal_template()
        raw["canvases"][0]["trigger"]["conditions"] = {
            "version": "1.0",
            "items": [
                {
                    "type": "trait",
                    "targetType": "player",  # WRONG — should be `subject`
                    "trait_key": "corruption",
                    "operator": "gte",
                    "value": 15,
                },
            ],
        }
        errors, _ = self._validate_template(raw)
        matching = [e for e in errors if "`targetType`" in e and "Doc 68" in e]
        self.assertTrue(matching,
                        f"Expected error for `targetType` in predicate context. Got: {errors}")

    def test_predicate_with_trait_field_errors(self):
        """Predicate item with type=trait using effect's `trait` field → ERROR."""
        raw = self._build_minimal_template()
        raw["canvases"][0]["trigger"]["conditions"] = {
            "version": "1.0",
            "items": [
                {
                    "type": "trait",
                    "subject": "player",
                    "trait": "corruption",  # WRONG — should be `trait_key`
                    "operator": "gte",
                    "value": 15,
                },
            ],
        }
        errors, _ = self._validate_template(raw)
        matching = [e for e in errors if "`trait`" in e and "type = 'trait'" in e and "Doc 68" in e]
        self.assertTrue(matching,
                        f"Expected error for `trait` in trait-predicate. Got: {errors}")

    def test_predicate_with_flag_field_errors(self):
        """Predicate item with type=flag using effect's `flag` field → ERROR."""
        raw = self._build_minimal_template()
        raw["canvases"][0]["trigger"]["conditions"] = {
            "version": "1.0",
            "items": [
                {
                    "type": "flag",
                    "subject": "player",
                    "flag": "test_flag",  # WRONG — should be `flag_key`
                    "operator": "is_true",
                },
            ],
        }
        errors, _ = self._validate_template(raw)
        matching = [e for e in errors if "`flag`" in e and "type = 'flag'" in e and "Doc 68" in e]
        self.assertTrue(matching,
                        f"Expected error for `flag` in flag-predicate. Got: {errors}")

    def test_predicate_with_op_field_errors(self):
        """Predicate item using effect's `op` field → ERROR."""
        raw = self._build_minimal_template()
        raw["canvases"][0]["trigger"]["conditions"] = {
            "version": "1.0",
            "items": [
                {
                    "type": "trait",
                    "subject": "player",
                    "trait_key": "corruption",
                    "op": "gte",  # WRONG — should be `operator`
                    "value": 15,
                },
            ],
        }
        errors, _ = self._validate_template(raw)
        matching = [e for e in errors if "`op`" in e and "Doc 68" in e and "operator" in e]
        self.assertTrue(matching,
                        f"Expected error for `op` in predicate context. Got: {errors}")

    def test_predicate_with_npcId_field_errors(self):
        """Predicate item using effect's `npcId` field → ERROR."""
        raw = self._build_minimal_template()
        raw["canvases"][0]["trigger"]["conditions"] = {
            "version": "1.0",
            "items": [
                {
                    "type": "trait",
                    "subject": "npc",
                    "npcId": "npc_test",  # WRONG — should be `npc_id`
                    "trait_key": "relation",
                    "operator": "gte",
                    "value": 5,
                },
            ],
        }
        errors, _ = self._validate_template(raw)
        matching = [e for e in errors if "`npcId`" in e and "Doc 68" in e]
        self.assertTrue(matching,
                        f"Expected error for `npcId` in predicate context. Got: {errors}")

    # ─── Backward-compat / no-false-positives (2 tests) ─────────────────────

    def test_correct_effect_passes(self):
        """Effect using all correct field names → no errors."""
        raw = self._build_minimal_template()
        raw["canvases"][0]["nodes"][0]["exit_block"]["choices"][0]["effects"].append({
            "targetType": "player",
            "trait": "corruption",
            "op": "add",
            "value": 1,
        })
        errors, _ = self._validate_template(raw)
        fn_errs = [e for e in errors if "Doc 68" in e]
        self.assertEqual(fn_errs, [],
                         f"Correct effect should not raise field-name errors. Got: {fn_errs}")

    def test_correct_predicate_passes(self):
        """Predicate using all correct field names → no errors."""
        raw = self._build_minimal_template()
        raw["canvases"][0]["trigger"]["conditions"] = {
            "version": "1.0",
            "items": [
                {
                    "type": "trait",
                    "subject": "player",
                    "trait_key": "corruption",
                    "operator": "gte",
                    "value": 15,
                },
                {
                    "type": "flag",
                    "subject": "player",
                    "flag_key": "test_flag",
                    "operator": "is_true",
                },
                {
                    "type": "trait",
                    "subject": "npc",
                    "npc_id": "npc_test",
                    "trait_key": "relation",
                    "operator": "gte",
                    "value": 5,
                },
            ],
        }
        errors, _ = self._validate_template(raw)
        fn_errs = [e for e in errors if "Doc 68" in e]
        self.assertEqual(fn_errs, [],
                         f"Correct predicates should not raise field-name errors. Got: {fn_errs}")

    def test_tls_slice_builds_clean(self):
        """Integration: live TLS slice TOML should not trigger any field-name errors.

        Per Doc 68 audit (2026-05-26), live TLS uses correct field names everywhere.
        This is the regression guard — if a future TLS edit introduces a mismatch,
        the validator catches it.
        """
        import os
        from apps.projects.services.template_import import normalize, validate, parse_toml

        toml_path = (
            "games/the_long_summer_test/toml_phases/7_final_game.toml"
        )
        if not os.path.exists(toml_path):
            self.skipTest(f"TLS slice not available at {toml_path}")

        data = parse_toml(toml_path)
        template = normalize(data)
        errors = validate(template)
        fn_errs = [e for e in errors if "Doc 68" in e or "predicate-syntax" in e
                                       or "effect-syntax" in e]
        self.assertEqual(
            fn_errs, [],
            f"TLS slice should pass field-name validation. "
            f"Found {len(fn_errs)} field-name errors:\n" +
            "\n".join(f"  - {e}" for e in fn_errs[:5])
        )


class Doc69TraitDeclarationValidatorTests(TestCase):
    """Doc 69 Item 4 — Undeclared trait validator.

    Every player + NPC trait referenced in effects or conditions MUST be
    pre-declared in `[player.core_traits]` or per-NPC `core_traits`. Engine
    reads undefined → silent runtime misbehavior. Validator converts the
    Doc 68 §2.5 doctrine to build-time enforcement.

    Stage trait pattern (`<slug>_stage`): tracked specially per Doc 68 §9 +
    Doc 69 §6.3 #4 — declared on player namespace; matching NPC must have
    `arc_stages`; ERROR if not declared, WARN if declared but no arc.
    """

    def _build_minimal_template(self, *, extra_player_traits=None,
                                 npc_arc_stages=None, npc_traits=None):
        """Minimal valid template — same shape as Phase 1 tests, with
        configurable player core_traits, NPC core_traits, and arc_stages.
        """
        player_core = {"corruption": 0, "arousal": 0}
        if extra_player_traits:
            player_core.update(extra_player_traits)
        npc_core = {"relation": 0}
        if npc_traits:
            npc_core.update(npc_traits)
        npc_block = {
            "id": "npc_test",
            "name": "Test NPC",
            "description": "Fixture NPC",
            "core_traits": npc_core,
            "flag_keys": [],
        }
        if npc_arc_stages is not None:
            npc_block["arc_stages"] = list(npc_arc_stages)
        return {
            "schema_version": "1.0",
            "project": {
                "id": "doc69_item4_test",
                "title": "Doc 69 Item 4 Fixture",
                "description": "Trait-declaration validator fixture.",
                "starting_canvas": "canvas_test",
            },
            "time": {"enabled": True, "starting_hour": 8, "starting_day": "Monday"},
            "player": {
                "id": "player",
                "name": "Test Player",
                "core_traits": player_core,
                "flag_keys": [],
            },
            "locations": [
                {"id": "loc_kitchen", "name": "Kitchen", "description": "Test"},
            ],
            "npcs": [npc_block],
            "canvases": [
                {
                    "id": "canvas_test",
                    "name": "Test Canvas",
                    "type": "scene",
                    "trigger": {
                        "location": "loc_kitchen",
                        "is_active": True,
                        "is_repeatable": True,
                        "trigger_mode": "manual",
                    },
                    "nodes": [
                        {
                            "id": "n1",
                            "name": "Test Node",
                            "blocks": [{"type": "paragraph", "props": {},
                                        "content": [{"type": "text", "text": "test"}]}],
                            "exit_block": {
                                "type": "choices",
                                "choices": [
                                    {
                                        "text": "Continue",
                                        "targetType": "trigger",
                                        "effects": [],
                                    },
                                ],
                            },
                        },
                    ],
                },
            ],
        }

    def _validate_template(self, raw):
        import copy, warnings
        from apps.projects.services.template_import import normalize, validate
        with warnings.catch_warnings(record=True) as ws:
            warnings.simplefilter("always")
            template = normalize(copy.deepcopy(raw))
            errors = validate(template)
        return errors, [str(w.message) for w in ws], template

    # ─── Player trait declaration (effects + conditions) ────────────────────

    def test_effect_undeclared_player_trait_errors(self):
        """Effect targeting a player trait not in [player.core_traits] → ERROR."""
        raw = self._build_minimal_template()
        raw["canvases"][0]["nodes"][0]["exit_block"]["choices"][0]["effects"].append({
            "targetType": "player",
            "trait": "nonexistent_trait",
            "op": "add",
            "value": 1,
        })
        errors, _, _ = self._validate_template(raw)
        matching = [e for e in errors
                    if "nonexistent_trait" in e and "Doc 68 §2.5" in e]
        self.assertTrue(matching,
                        f"Expected error for undeclared player trait. Got: {errors}")

    def test_effect_declared_player_trait_passes(self):
        """Effect on a declared player trait → no trait-declaration errors."""
        raw = self._build_minimal_template()
        raw["canvases"][0]["nodes"][0]["exit_block"]["choices"][0]["effects"].append({
            "targetType": "player",
            "trait": "corruption",  # declared in fixture
            "op": "add",
            "value": 1,
        })
        errors, _, _ = self._validate_template(raw)
        td_errs = [e for e in errors if "Doc 68 §2.5" in e]
        self.assertEqual(td_errs, [],
                         f"Declared player trait should pass. Got: {td_errs}")

    def test_condition_undeclared_player_trait_errors(self):
        """Predicate item with trait_key not in player.core_traits → ERROR."""
        raw = self._build_minimal_template()
        raw["canvases"][0]["trigger"]["conditions"] = {
            "version": "1.0",
            "items": [
                {
                    "type": "trait",
                    "subject": "player",
                    "trait_key": "ghost_trait",
                    "operator": "gte",
                    "value": 1,
                },
            ],
        }
        errors, _, _ = self._validate_template(raw)
        matching = [e for e in errors
                    if "ghost_trait" in e and "Doc 68 §2.5" in e]
        self.assertTrue(matching,
                        f"Expected error for undeclared player trait in predicate. "
                        f"Got: {errors}")

    def test_condition_declared_player_trait_passes(self):
        """Predicate on declared player trait → no trait-declaration errors."""
        raw = self._build_minimal_template()
        raw["canvases"][0]["trigger"]["conditions"] = {
            "version": "1.0",
            "items": [
                {
                    "type": "trait",
                    "subject": "player",
                    "trait_key": "corruption",
                    "operator": "gte",
                    "value": 15,
                },
            ],
        }
        errors, _, _ = self._validate_template(raw)
        td_errs = [e for e in errors if "Doc 68 §2.5" in e]
        self.assertEqual(td_errs, [],
                         f"Declared player trait in predicate should pass. Got: {td_errs}")

    # ─── NPC trait declaration ──────────────────────────────────────────────

    def test_effect_declared_npc_trait_passes(self):
        """Effect on declared NPC trait → no trait-declaration errors."""
        raw = self._build_minimal_template()
        raw["canvases"][0]["nodes"][0]["exit_block"]["choices"][0]["effects"].append({
            "targetType": "npc",
            "npcId": "npc_test",
            "trait": "relation",  # declared in NPC core_traits
            "op": "add",
            "value": 1,
        })
        errors, _, _ = self._validate_template(raw)
        td_errs = [e for e in errors if "Doc 68 §2.5" in e]
        self.assertEqual(td_errs, [],
                         f"Declared NPC trait should pass. Got: {td_errs}")

    def test_effect_undeclared_npc_trait_errors(self):
        """Effect on NPC trait not in NPC's core_traits → ERROR."""
        raw = self._build_minimal_template()
        raw["canvases"][0]["nodes"][0]["exit_block"]["choices"][0]["effects"].append({
            "targetType": "npc",
            "npcId": "npc_test",
            "trait": "ghost_npc_trait",
            "op": "add",
            "value": 1,
        })
        errors, _, _ = self._validate_template(raw)
        matching = [e for e in errors
                    if "ghost_npc_trait" in e and "npc_test" in e
                    and "Doc 68 §2.5" in e]
        self.assertTrue(matching,
                        f"Expected error for undeclared NPC trait. Got: {errors}")

    # ─── Stage trait special-case ────────────────────────────────────────────

    def test_stage_trait_declared_with_arc_stages_passes(self):
        """Stage trait declared in player + NPC has arc_stages → passes."""
        raw = self._build_minimal_template(
            extra_player_traits={"npc_test_stage": 0},
            npc_arc_stages=["Stage 0", "Stage 1", "Stage 2"],
        )
        # Use it in an effect
        raw["canvases"][0]["nodes"][0]["exit_block"]["choices"][0]["effects"].append({
            "targetType": "player",
            "trait": "npc_test_stage",
            "op": "set",
            "value": 1,
        })
        errors, warns, _ = self._validate_template(raw)
        td_errs = [e for e in errors if "Doc 68 §2.5" in e]
        self.assertEqual(td_errs, [],
                         f"Stage trait with declared+arc_stages should pass. Got: {td_errs}")
        # Should also have NO arc-stages warning
        td_warns = [w for w in warns if "Doc 68 §9.0" in w]
        self.assertEqual(td_warns, [],
                         f"No stage-pattern warning expected. Got: {td_warns}")

    def test_stage_trait_not_declared_but_npc_has_arc_errors(self):
        """Stage trait pattern matches NPC with arc_stages, but trait NOT
        declared in [player.core_traits] → ERROR with stage-pattern hint."""
        raw = self._build_minimal_template(
            extra_player_traits=None,  # don't add npc_test_stage to player
            npc_arc_stages=["Stage 0", "Stage 1"],
        )
        raw["canvases"][0]["nodes"][0]["exit_block"]["choices"][0]["effects"].append({
            "targetType": "player",
            "trait": "npc_test_stage",  # matches stage pattern; NPC has arc
            "op": "set",
            "value": 1,
        })
        errors, _, _ = self._validate_template(raw)
        matching = [e for e in errors
                    if "npc_test_stage" in e and "stage" in e.lower()
                    and "Doc 68" in e]
        self.assertTrue(matching,
                        f"Expected stage-pattern ERROR for undeclared stage trait. "
                        f"Got: {errors}")

    def test_stage_trait_declared_but_no_arc_stages_warns(self):
        """Stage trait declared in player, but NPC has empty arc_stages → WARN."""
        raw = self._build_minimal_template(
            extra_player_traits={"npc_test_stage": 0},
            npc_arc_stages=[],  # empty
        )
        raw["canvases"][0]["nodes"][0]["exit_block"]["choices"][0]["effects"].append({
            "targetType": "player",
            "trait": "npc_test_stage",
            "op": "set",
            "value": 1,
        })
        errors, warns, _ = self._validate_template(raw)
        # Should NOT error (trait IS declared)
        td_errs = [e for e in errors if "Doc 68 §2.5" in e and "npc_test_stage" in e]
        self.assertEqual(td_errs, [],
                         f"Declared stage trait should not error. Got: {td_errs}")
        # SHOULD warn about empty arc_stages
        td_warns = [w for w in warns
                    if "npc_test_stage" in w and "Doc 68 §9.0" in w]
        self.assertTrue(td_warns,
                        f"Expected WARN for stage trait with empty arc_stages. "
                        f"Got warnings: {warns}")

    def test_tls_slice_traits_all_declared(self):
        """Integration: TLS slice should pass trait-declaration validation
        (after the 2026-05-27 loop_*_pleasure declaration fix)."""
        import os
        from apps.projects.services.template_import import normalize, validate, parse_toml

        toml_path = "games/the_long_summer_test/toml_phases/7_final_game.toml"
        if not os.path.exists(toml_path):
            self.skipTest(f"TLS slice not available at {toml_path}")

        data = parse_toml(toml_path)
        template = normalize(data)
        errors = validate(template)
        td_errs = [e for e in errors if "Doc 68 §2.5" in e or "undeclared" in e]
        self.assertEqual(
            td_errs, [],
            f"TLS slice should have all traits declared. Found {len(td_errs)} errors:\n"
            + "\n".join(f"  - {e[:200]}" for e in td_errs[:5])
        )


class Doc69PatternBExclusiveGroupTests(TestCase):
    """Doc 69 Item 1 — Pattern B `exclusive_group` substitution extension.

    Substitution rules sharing an `exclusive_group` string share ONE dice roll
    at runtime (mutual exclusion via cumulative bucket partition). Failed-
    condition in claimed slot falls to solo, NOT next rule in group. Groups
    process FIRST per LO Q2 decision; then Pattern A independent rules.
    """

    def _build_minimal_template_with_sub(self, substitutions=None):
        """Minimal template with two canvases: parent + substitution target.
        Caller passes a list of substitution rule dicts.
        """
        return {
            "schema_version": "1.0",
            "project": {
                "id": "doc69_item1_test",
                "title": "Doc 69 Item 1 Pattern B Fixture",
                "description": "exclusive_group substitution extension test.",
                "starting_canvas": "canvas_parent",
            },
            "time": {"enabled": True, "starting_hour": 8, "starting_day": "Monday"},
            "player": {
                "id": "player",
                "name": "Player",
                "core_traits": {"corruption": 0},
                "flag_keys": [],
            },
            "locations": [
                {"id": "loc_kitchen", "name": "Kitchen", "description": "Test"},
            ],
            "npcs": [],
            "canvases": [
                {
                    "id": "canvas_parent",
                    "name": "Parent",
                    "type": "scene",
                    "trigger": {
                        "location": "loc_kitchen",
                        "is_active": True,
                        "is_repeatable": True,
                        "trigger_mode": "manual",
                        "substitutions": substitutions or [],
                    },
                    "nodes": [{"id": "n1", "name": "n1", "blocks": [{"type": "paragraph",
                                "props": {}, "content": [{"type": "text", "text": "."}]}]}],
                },
                {
                    "id": "canvas_target_a",
                    "name": "Target A",
                    "type": "scene",
                    "trigger": {"location": "loc_kitchen", "trigger_mode": "manual",
                                 "is_repeatable": True, "substitution_only": True},
                    "nodes": [{"id": "n1", "name": "n1", "blocks": [{"type": "paragraph",
                                "props": {}, "content": [{"type": "text", "text": "A"}]}]}],
                },
                {
                    "id": "canvas_target_b",
                    "name": "Target B",
                    "type": "scene",
                    "trigger": {"location": "loc_kitchen", "trigger_mode": "manual",
                                 "is_repeatable": True, "substitution_only": True},
                    "nodes": [{"id": "n1", "name": "n1", "blocks": [{"type": "paragraph",
                                "props": {}, "content": [{"type": "text", "text": "B"}]}]}],
                },
                {
                    "id": "canvas_target_c",
                    "name": "Target C",
                    "type": "scene",
                    "trigger": {"location": "loc_kitchen", "trigger_mode": "manual",
                                 "is_repeatable": True, "substitution_only": True},
                    "nodes": [{"id": "n1", "name": "n1", "blocks": [{"type": "paragraph",
                                "props": {}, "content": [{"type": "text", "text": "C"}]}]}],
                },
            ],
        }

    def _normalize_and_validate(self, raw):
        import copy, warnings
        from apps.projects.services.template_import import normalize, validate
        with warnings.catch_warnings(record=True) as ws:
            warnings.simplefilter("always")
            template = normalize(copy.deepcopy(raw))
            errors = validate(template)
        return template, errors, [str(w.message) for w in ws]

    # ─── Schema round-trip ──────────────────────────────────────────────────

    def test_exclusive_group_field_round_trips(self):
        """exclusive_group field survives normalize() into template.canvases."""
        raw = self._build_minimal_template_with_sub([
            {"target_canvas_id": "canvas_target_a", "chance": 0.17,
             "exclusive_group": "test_group"},
            {"target_canvas_id": "canvas_target_b", "chance": 0.17,
             "exclusive_group": "test_group"},
        ])
        template, errors, _ = self._normalize_and_validate(raw)
        parent = next(c for c in template.canvases if c.id == "canvas_parent")
        self.assertEqual(len(parent.trigger.substitutions), 2)
        self.assertEqual(parent.trigger.substitutions[0]["exclusive_group"], "test_group")
        self.assertEqual(parent.trigger.substitutions[1]["exclusive_group"], "test_group")

    def test_exclusive_group_absent_means_pattern_a(self):
        """Substitution without exclusive_group → field stored as None (Pattern A)."""
        raw = self._build_minimal_template_with_sub([
            {"target_canvas_id": "canvas_target_a", "chance": 0.33},
        ])
        template, errors, _ = self._normalize_and_validate(raw)
        parent = next(c for c in template.canvases if c.id == "canvas_parent")
        self.assertIsNone(parent.trigger.substitutions[0]["exclusive_group"])

    # ─── Validator: chance-sum bounds ───────────────────────────────────────

    def test_chance_sum_over_1_0_warns(self):
        """Chance values in same exclusive_group summing > 1.0 → WARN."""
        raw = self._build_minimal_template_with_sub([
            {"target_canvas_id": "canvas_target_a", "chance": 0.5,
             "exclusive_group": "g1"},
            {"target_canvas_id": "canvas_target_b", "chance": 0.7,
             "exclusive_group": "g1"},  # sum = 1.2
        ])
        _, errors, warns = self._normalize_and_validate(raw)
        # Should NOT error (sum <= 1.5)
        chance_errs = [e for e in errors if "g1" in e and "chance sum" in e]
        self.assertEqual(chance_errs, [],
                         f"Sum 1.2 should warn, not error. Got errors: {chance_errs}")
        # Should warn
        chance_warns = [w for w in warns
                        if "g1" in w and "chance sum" in w and "Doc 69 §3.6" in w]
        self.assertTrue(chance_warns,
                        f"Expected WARN for chance sum > 1.0. Got warnings: {warns}")

    def test_chance_sum_over_1_5_errors(self):
        """Chance values in same exclusive_group summing > 1.5 → ERROR."""
        raw = self._build_minimal_template_with_sub([
            {"target_canvas_id": "canvas_target_a", "chance": 0.9,
             "exclusive_group": "g_too_big"},
            {"target_canvas_id": "canvas_target_b", "chance": 0.9,
             "exclusive_group": "g_too_big"},  # sum = 1.8
        ])
        _, errors, _ = self._normalize_and_validate(raw)
        matching = [e for e in errors
                    if "g_too_big" in e and "chance sum" in e and "Doc 69" in e]
        self.assertTrue(matching,
                        f"Expected ERROR for chance sum > 1.5. Got errors: {errors}")

    # ─── Validator: target ownership ────────────────────────────────────────

    def test_duplicate_target_across_groups_errors(self):
        """Same target_canvas_id in two different groups → ERROR."""
        raw = self._build_minimal_template_with_sub([
            {"target_canvas_id": "canvas_target_a", "chance": 0.5,
             "exclusive_group": "group1"},
            {"target_canvas_id": "canvas_target_a", "chance": 0.5,
             "exclusive_group": "group2"},
        ])
        _, errors, _ = self._normalize_and_validate(raw)
        matching = [e for e in errors
                    if "canvas_target_a" in e and "group1" in e and "group2" in e]
        self.assertTrue(matching,
                        f"Expected ERROR for duplicate target across groups. Got: {errors}")

    def test_target_in_group_and_independent_errors(self):
        """Same target in a group AND as independent rule → ERROR."""
        raw = self._build_minimal_template_with_sub([
            {"target_canvas_id": "canvas_target_a", "chance": 0.5,
             "exclusive_group": "g1"},
            {"target_canvas_id": "canvas_target_a", "chance": 0.3},  # no group
        ])
        _, errors, _ = self._normalize_and_validate(raw)
        matching = [e for e in errors
                    if "canvas_target_a" in e and "independent" in e and "g1" in e]
        self.assertTrue(matching,
                        f"Expected ERROR for target in group+independent. Got: {errors}")

    # ─── Validator: single-rule group ───────────────────────────────────────

    def test_single_rule_group_warns(self):
        """exclusive_group with only one rule → WARN (no behavioral difference)."""
        raw = self._build_minimal_template_with_sub([
            {"target_canvas_id": "canvas_target_a", "chance": 0.5,
             "exclusive_group": "solo_group"},
        ])
        _, _, warns = self._normalize_and_validate(raw)
        matching = [w for w in warns
                    if "solo_group" in w and "only one" in w and "Doc 69" in w]
        self.assertTrue(matching,
                        f"Expected WARN for single-rule group. Got warnings: {warns}")

    # ─── Engine emission ────────────────────────────────────────────────────

    def test_exclusive_group_in_emitted_substitutions_json(self):
        """Engine emits exclusive_group in the canvasSubstitutions JSON map."""
        import copy
        from apps.projects.services.template_import import normalize
        from apps.projects.services.template_import import (
            create_project_from_template,
        )
        from apps.game_generation.twee_comprehensive.generators.v2 import (
            TweeComprehensiveGeneratorV2,
        )
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.create_user(
            email="doc69-item1-emit@example.com", password="testpass123"
        )
        raw = self._build_minimal_template_with_sub([
            {"target_canvas_id": "canvas_target_a", "chance": 0.17,
             "exclusive_group": "kitchen_walk_in"},
            {"target_canvas_id": "canvas_target_b", "chance": 0.17,
             "exclusive_group": "kitchen_walk_in"},
        ])
        template = normalize(copy.deepcopy(raw))
        result = create_project_from_template(template, str(user.id))
        from apps.projects.models import Project
        project = Project.objects.get(id=result["project_id"])
        twee = TweeComprehensiveGeneratorV2().generate(project)
        # The emitted JSON map should contain "exclusive_group" field.
        self.assertIn('"exclusive_group": "kitchen_walk_in"', twee,
                      "exclusive_group should appear in emitted canvasSubstitutions JSON")

    # ─── Backward compat ────────────────────────────────────────────────────

    def test_pattern_a_substitution_still_works(self):
        """Substitution without exclusive_group (existing Pattern A) → validates clean."""
        raw = self._build_minimal_template_with_sub([
            {"target_canvas_id": "canvas_target_a", "chance": 0.33},
            {"target_canvas_id": "canvas_target_b", "chance": 0.33},
        ])
        _, errors, warns = self._normalize_and_validate(raw)
        phase3_issues = [e for e in errors if "Doc 69" in e] + \
                        [w for w in warns if "Doc 69" in w]
        self.assertEqual(phase3_issues, [],
                         f"Pattern A (no exclusive_group) should validate clean. "
                         f"Got: {phase3_issues}")

    def test_tls_slice_no_exclusive_group_drift(self):
        """TLS slice has no exclusive_group anywhere → builds clean with no
        new Phase 3 errors/warnings. Backward-compat regression guard."""
        import os, warnings
        from apps.projects.services.template_import import normalize, validate, parse_toml
        toml_path = "games/the_long_summer_test/toml_phases/7_final_game.toml"
        if not os.path.exists(toml_path):
            self.skipTest(f"TLS slice not available")
        data = parse_toml(toml_path)
        with warnings.catch_warnings(record=True) as ws:
            warnings.simplefilter("always")
            template = normalize(data)
            errors = validate(template)
        phase3_errs = [e for e in errors if "Doc 69 §3" in e]
        phase3_warns = [str(w.message) for w in ws if "Doc 69 §3" in str(w.message)]
        self.assertEqual(phase3_errs, [],
                         f"TLS slice should have no Phase 3 errors. Got: {phase3_errs}")
        self.assertEqual(phase3_warns, [],
                         f"TLS slice should have no Phase 3 warnings. Got: {phase3_warns}")


class Doc69PatternCPreSubstitutionEffectsTests(TestCase):
    """Doc 69 Item 2 — Pattern C `pre_substitution_effects` canvas trigger
    extension. Effects in this list fire UNCONDITIONALLY at canvas entry,
    BEFORE the Lane 3 substitution check. If a substitution rule preempts
    via <<goto>>, these effects have already executed — the activity
    "counts" even when an NPC walks in (RTS Exercise pattern).
    """

    def _build_minimal_template_with_pse(
        self, pre_substitution_effects=None, substitutions=None,
    ):
        """Minimal template; caller passes pre_substitution_effects + optional
        substitutions on the parent canvas."""
        trigger = {
            "location": "loc_kitchen",
            "is_active": True,
            "is_repeatable": True,
            "trigger_mode": "manual",
        }
        if pre_substitution_effects:
            trigger["pre_substitution_effects"] = pre_substitution_effects
        if substitutions:
            trigger["substitutions"] = substitutions
        return {
            "schema_version": "1.0",
            "project": {
                "id": "doc69_item2_test",
                "title": "Doc 69 Item 2 Pattern C Fixture",
                "description": "pre_substitution_effects test.",
                "starting_canvas": "canvas_parent",
            },
            "time": {"enabled": True, "starting_hour": 8, "starting_day": "Monday"},
            "player": {
                "id": "player",
                "name": "Player",
                "core_traits": {"fitness": 0, "energy": 100, "corruption": 0},
                "flag_keys": [],
            },
            "locations": [
                {"id": "loc_kitchen", "name": "Kitchen", "description": "Test"},
            ],
            "npcs": [],
            "canvases": [
                {
                    "id": "canvas_parent",
                    "name": "Parent",
                    "type": "scene",
                    "trigger": trigger,
                    "nodes": [{"id": "n1", "name": "n1",
                                "blocks": [{"type": "paragraph", "props": {},
                                            "content": [{"type": "text", "text": "."}]}]}],
                },
                {
                    "id": "canvas_target",
                    "name": "Target",
                    "type": "scene",
                    "trigger": {"location": "loc_kitchen", "trigger_mode": "manual",
                                 "is_repeatable": True, "substitution_only": True},
                    "nodes": [{"id": "n1", "name": "n1",
                                "blocks": [{"type": "paragraph", "props": {},
                                            "content": [{"type": "text", "text": "T"}]}]}],
                },
            ],
        }

    def _normalize_and_validate(self, raw):
        import copy, warnings
        from apps.projects.services.template_import import normalize, validate
        with warnings.catch_warnings(record=True) as ws:
            warnings.simplefilter("always")
            template = normalize(copy.deepcopy(raw))
            errors = validate(template)
        return template, errors, [str(w.message) for w in ws]

    # ─── Schema round-trip ──────────────────────────────────────────────────

    def test_pre_substitution_effects_round_trip(self):
        """pre_substitution_effects survives normalize() into TemplateTrigger."""
        raw = self._build_minimal_template_with_pse(
            pre_substitution_effects=[
                {"targetType": "player", "trait": "fitness", "op": "add",
                 "value": 1, "cap": 100},
            ],
            substitutions=[
                {"target_canvas_id": "canvas_target", "chance": 0.5},
            ],
        )
        template, errors, _ = self._normalize_and_validate(raw)
        parent = next(c for c in template.canvases if c.id == "canvas_parent")
        self.assertEqual(len(parent.trigger.pre_substitution_effects), 1)
        self.assertEqual(parent.trigger.pre_substitution_effects[0]["trait"], "fitness")
        self.assertEqual(parent.trigger.pre_substitution_effects[0]["op"], "add")
        self.assertEqual(parent.trigger.pre_substitution_effects[0]["cap"], 100)

    def test_empty_pre_substitution_effects_backward_compat(self):
        """Canvas without pre_substitution_effects → defaults to empty list."""
        raw = self._build_minimal_template_with_pse(
            substitutions=[{"target_canvas_id": "canvas_target", "chance": 0.5}],
        )
        template, errors, _ = self._normalize_and_validate(raw)
        parent = next(c for c in template.canvases if c.id == "canvas_parent")
        self.assertEqual(parent.trigger.pre_substitution_effects, [])

    # ─── Emitter ordering (the load-bearing test) ───────────────────────────

    def test_emission_pre_substitution_before_substitution_check(self):
        """The emitted passage MUST have pre-substitution macros BEFORE the
        substitution_check <<set>>+<<goto>>. This is the load-bearing test
        per Doc 69 §4.4 — if the order is wrong, Pattern C semantics break."""
        import copy
        from apps.projects.services.template_import import (
            normalize, create_project_from_template,
        )
        from apps.game_generation.twee_comprehensive.generators.v2 import (
            TweeComprehensiveGeneratorV2,
        )
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.create_user(
            email="doc69-item2-order@example.com", password="testpass123"
        )
        raw = self._build_minimal_template_with_pse(
            pre_substitution_effects=[
                {"targetType": "player", "trait": "fitness", "op": "add", "value": 1},
            ],
            substitutions=[
                {"target_canvas_id": "canvas_target", "chance": 0.5},
            ],
        )
        template = normalize(copy.deepcopy(raw))
        result = create_project_from_template(template, str(user.id))
        from apps.projects.models import Project
        project = Project.objects.get(id=result["project_id"])
        twee = TweeComprehensiveGeneratorV2().generate(project)
        # Find the parent canvas's passage in the emitted Twee
        # — it should have applyAndNotifyTrait BEFORE checkAndSubstituteCanvas.
        # Locate the chunk between `:: ` (passage header) and the next blank line.
        lines = twee.split("\n")
        in_target = False
        pse_idx = None
        sub_check_idx = None
        for i, line in enumerate(lines):
            if line.startswith(":: ") and "canvas_parent" in line:
                in_target = True
                continue
            if in_target and line.startswith(":: "):
                break
            if in_target and "applyAndNotifyTrait" in line and pse_idx is None:
                pse_idx = i
            if in_target and "checkAndSubstituteCanvas" in line and sub_check_idx is None:
                sub_check_idx = i
        self.assertIsNotNone(pse_idx,
            f"Expected applyAndNotifyTrait macro in canvas_parent passage. Twee[:1500]:\n{twee[:1500]}")
        self.assertIsNotNone(sub_check_idx,
            "Expected checkAndSubstituteCanvas call in canvas_parent passage")
        self.assertLess(pse_idx, sub_check_idx,
            f"Pre-substitution macro (line {pse_idx}) must appear BEFORE "
            f"substitution check (line {sub_check_idx}) — Doc 69 §4.4 ordering.")

    def test_emission_no_pre_substitution_when_field_empty(self):
        """No pre-substitution effects → no applyAndNotifyTrait macros emitted
        in the canvas's passage header. Backward compat regression guard."""
        import copy
        from apps.projects.services.template_import import (
            normalize, create_project_from_template,
        )
        from apps.game_generation.twee_comprehensive.generators.v2 import (
            TweeComprehensiveGeneratorV2,
        )
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.create_user(
            email="doc69-item2-empty@example.com", password="testpass123"
        )
        # Canvas with substitutions but NO pre_substitution_effects
        raw = self._build_minimal_template_with_pse(
            substitutions=[
                {"target_canvas_id": "canvas_target", "chance": 0.5},
            ],
        )
        template = normalize(copy.deepcopy(raw))
        result = create_project_from_template(template, str(user.id))
        from apps.projects.models import Project
        project = Project.objects.get(id=result["project_id"])
        twee = TweeComprehensiveGeneratorV2().generate(project)
        # The canvas_parent passage should NOT have a pre-substitution
        # applyAndNotifyTrait before its substitution_check.
        lines = twee.split("\n")
        in_target = False
        sub_check_idx = None
        for i, line in enumerate(lines):
            if line.startswith(":: ") and "canvas_parent" in line:
                in_target = True
                start_idx = i
                continue
            if in_target and line.startswith(":: "):
                break
            if in_target and "checkAndSubstituteCanvas" in line:
                sub_check_idx = i
                break
        self.assertIsNotNone(sub_check_idx)
        # Between passage header and substitution_check, there should be no
        # applyAndNotifyTrait (those would be pre-substitution effects).
        between = "\n".join(lines[start_idx:sub_check_idx])
        self.assertNotIn("applyAndNotifyTrait", between,
            f"Empty pre_substitution_effects should emit no macros before "
            f"substitution check. Got between passage header and sub check:\n{between}")

    # ─── Validator ──────────────────────────────────────────────────────────

    def test_pre_substitution_effects_without_substitutions_warns(self):
        """pre_substitution_effects set without any substitution rules → WARN."""
        raw = self._build_minimal_template_with_pse(
            pre_substitution_effects=[
                {"targetType": "player", "trait": "fitness", "op": "add", "value": 1},
            ],
            # No substitutions!
        )
        _, errors, warns = self._normalize_and_validate(raw)
        matching = [w for w in warns
                    if "pre_substitution_effects" in w and "no substitutions" in w
                    and "Doc 69" in w]
        self.assertTrue(matching,
                        f"Expected WARN for pre-sub effects without substitutions. "
                        f"Got warnings: {warns}")

    # ─── Validator integration: field-name + trait-declaration ──────────────

    def test_pre_sub_with_wrong_field_name_errors(self):
        """pre_substitution_effects entry using predicate-syntax field name
        → ERROR (Phase 1 + Phase 2 validators apply here too)."""
        raw = self._build_minimal_template_with_pse(
            pre_substitution_effects=[
                {"subject": "player",  # WRONG — predicate field in effect
                 "trait": "fitness", "op": "add", "value": 1},
            ],
            substitutions=[{"target_canvas_id": "canvas_target", "chance": 0.5}],
        )
        _, errors, _ = self._normalize_and_validate(raw)
        matching = [e for e in errors
                    if "pre_substitution_effects" in e and "subject" in e
                    and "Doc 68" in e]
        self.assertTrue(matching,
                        f"Expected field-name ERROR on pre-sub effect. Got: {errors}")

    def test_pre_sub_with_undeclared_trait_errors(self):
        """pre_substitution_effects entry on undeclared player trait → ERROR
        (Phase 2 trait-declaration validator applies here too)."""
        raw = self._build_minimal_template_with_pse(
            pre_substitution_effects=[
                {"targetType": "player", "trait": "nonexistent_trait",
                 "op": "add", "value": 1},
            ],
            substitutions=[{"target_canvas_id": "canvas_target", "chance": 0.5}],
        )
        _, errors, _ = self._normalize_and_validate(raw)
        matching = [e for e in errors
                    if "pre_substitution_effects" in e and "nonexistent_trait" in e
                    and "Doc 68 §2.5" in e]
        self.assertTrue(matching,
                        f"Expected trait-declaration ERROR on pre-sub effect. Got: {errors}")

    # ─── TLS regression ─────────────────────────────────────────────────────

    def test_tls_slice_no_pattern_c_drift(self):
        """TLS slice has no pre_substitution_effects anywhere → builds clean."""
        import os, warnings
        from apps.projects.services.template_import import normalize, validate, parse_toml
        toml_path = "games/the_long_summer_test/toml_phases/7_final_game.toml"
        if not os.path.exists(toml_path):
            self.skipTest(f"TLS slice not available")
        data = parse_toml(toml_path)
        with warnings.catch_warnings(record=True) as ws:
            warnings.simplefilter("always")
            template = normalize(data)
            errors = validate(template)
        phase4_errs = [e for e in errors if "Doc 69 §4" in e]
        phase4_warns = [str(w.message) for w in ws if "Doc 69 §4" in str(w.message)]
        self.assertEqual(phase4_errs, [],
                         f"TLS slice should have no Phase 4 errors. Got: {phase4_errs}")
        self.assertEqual(phase4_warns, [],
                         f"TLS slice should have no Phase 4 warnings. Got: {phase4_warns}")


class NpcPanelSidebarTests(TestCase):
    """`npc_panel` sidebar item (RTS House-card): per-NPC arousal band / corruption /
    location-from-schedule (2026-06-06). Location reuses setup.getNpcLocation — the same
    schedule source the Schedule page uses."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="npc-panel-sidebar@example.com", password="testpass123"
        )

    def _template(self, *, rows=None, with_schedule=True, with_traits=True, item_override=None):
        loc_id = "loc_kitchen"
        npc_id = "npc_test"
        canvas_id = "canvas_test"
        npc = {
            "id": npc_id,
            "name": "Test NPC",
            "description": "Fixture NPC",
            "core_traits": {"arousal": 0, "corruption": 0} if with_traits else {},
            "flag_keys": [],
        }
        if with_schedule:
            npc["schedules"] = [
                {"location": loc_id, "weekdays": [0, 1, 2, 3, 4, 5, 6],
                 "start_time": "06:00", "end_time": "23:00", "activity": "around"},
            ]
        item = item_override if item_override is not None else {
            "type": "npc_panel",
            "npc_id": npc_id,
            "label": "Test NPC",
            "rows": rows if rows is not None else ["arousal", "corruption", "location"],
        }
        return {
            "schema_version": "1.0",
            "project": {
                "id": "npc_panel_test",
                "title": "NPC Panel Fixture",
                "description": "Minimal fixture for the npc_panel sidebar item.",
                "starting_canvas": canvas_id,
            },
            "time": {"enabled": True, "starting_hour": 8, "starting_day": "Monday"},
            "locations": [{"id": loc_id, "name": "Kitchen", "description": "Test kitchen"}],
            "npcs": [npc],
            "sidebar_items": [item],
            "canvases": [
                {
                    "id": canvas_id,
                    "name": "Test Canvas",
                    "type": "scene",
                    "trigger": {"location": loc_id, "is_active": True, "is_repeatable": True,
                                "trigger_mode": "random", "chance": 0.5},
                    "nodes": [
                        {"id": "n1", "name": "N1",
                         "blocks": [{"type": "paragraph", "props": {},
                                     "content": [{"type": "text", "text": "test"}]}]}
                    ],
                },
            ],
        }

    def _validate(self, raw):
        import copy
        from apps.projects.services.template_import import normalize, validate
        return validate(normalize(copy.deepcopy(raw)))

    def _gen(self, raw, version="v2"):
        import copy
        from apps.projects.services.template_import import (
            normalize, validate, create_project_from_template,
        )
        template = normalize(copy.deepcopy(raw))
        errors = validate(template)
        self.assertEqual(errors, [], f"Fixture should validate clean: {errors}")
        result = create_project_from_template(template, str(self.user.id))
        project = Project.objects.get(id=result["project_id"])
        if version == "v2":
            from apps.game_generation.twee_comprehensive.generators.v2 import (
                TweeComprehensiveGeneratorV2 as Gen,
            )
        else:
            from apps.game_generation.twee_comprehensive.generators.v1 import (
                TweeComprehensiveGeneratorV1 as Gen,
            )
        return Gen().generate(project)

    def test_npc_panel_render_branch_and_item_emitted_v2_and_v1(self):
        for version in ("v2", "v1"):
            twee = self._gen(self._template(), version=version)
            self.assertIn('_item.type is "npc_panel"', twee,
                          f"{version}: npc_panel render branch must be emitted")
            self.assertIn("npc-panel-item", twee, f"{version}: card markup must be present")
            self.assertIn("setup.getNpcLocation", twee,
                          f"{version}: location row must use getNpcLocation (Schedule-page source)")
            # the configured item rides into the sidebar_items blob
            self.assertIn('"npc_panel"', twee, f"{version}: npc_panel item must be serialized")
            self.assertIn("npc_test", twee, f"{version}: the configured npc_id must be present")

    def test_npc_panel_schedule_emitted_for_location_row(self):
        twee = self._gen(self._template(rows=["location"]))
        self.assertIn("npcSchedules", twee)
        self.assertIn("loc_kitchen", twee)

    def test_validation_rejects_unknown_npc_id(self):
        errors = self._validate(self._template(
            item_override={"type": "npc_panel", "npc_id": "npc_ghost", "rows": ["arousal"]}))
        self.assertTrue(any("npc_ghost" in e and "npc_panel" in e for e in errors),
                        f"Expected unknown-npc error, got: {errors}")

    def test_validation_rejects_bad_row(self):
        errors = self._validate(self._template(rows=["arousal", "bogus"]))
        self.assertTrue(any("bogus" in e and "npc_panel" in e for e in errors),
                        f"Expected bad-row error, got: {errors}")

    def test_validation_rejects_missing_rows(self):
        errors = self._validate(self._template(
            item_override={"type": "npc_panel", "npc_id": "npc_test"}))
        self.assertTrue(any("rows" in e and "npc_panel" in e for e in errors),
                        f"Expected missing-rows error, got: {errors}")

    def test_validation_rejects_row_trait_not_declared(self):
        errors = self._validate(self._template(rows=["arousal"], with_traits=False))
        self.assertTrue(any("arousal" in e and "npc_panel" in e for e in errors),
                        f"Expected undeclared-trait error, got: {errors}")

    def test_next_row_valid_and_branch_emitted(self):
        # "next" is an allowed row (no trait declaration needed — it reads the quest system).
        self.assertEqual(self._validate(self._template(rows=["next"])), [])
        twee = self._gen(self._template(rows=["arousal", "location", "next"]))
        self.assertIn('_npRow is "next"', twee, "next render branch must be emitted")
        self.assertIn("npc-panel-next", twee, "next card markup must be present")
        self.assertIn("setup.pickQuestsCard", twee, "next must reuse the quest picker")
        self.assertIn("setup.renderQuestsGoalBlock", twee, "next must reuse the Quests goal-block renderer (full parity)")


class ClothingBuyGateTests(TestCase):
    """Clothing shop buy-gate feedback (2026-06-06).

    A clothing item can carry its own `conditions` block (e.g. corruption >= 25).
    `buyItem` enforces it, but the shop's tier display rounds the threshold down
    into the Basic tier, so the item shows a live Buy button. Before this fix the
    failed click silently no-op'd. Now buyItem publishes a gated-action toast
    (bottom-overlay `notify-warning`) naming the unmet requirement, flushed by the
    shop handler's `showEffectNotification()`. Verified across v1 + v2 parity.
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="clothing-buy-gate@example.com", password="testpass123"
        )

    def _template(self):
        loc_id = "loc_shop"
        canvas_id = "canvas_start"
        return {
            "schema_version": "1.0",
            "project": {
                "id": "clothing_gate_test",
                "title": "Clothing Buy Gate Fixture",
                "description": "Minimal clothing-enabled fixture with a gated item.",
                "starting_canvas": canvas_id,
            },
            "time": {"enabled": True, "starting_hour": 8, "starting_day": "Monday"},
            "settings": {
                "clothing_enabled": True,
                "shop_location": loc_id,
                "wardrobe_location": loc_id,
            },
            "clothing": [
                {
                    "id": "outfit_gated",
                    "name": "Barely-there mini",
                    "slot": "bottom",
                    "price": 55,
                    "beauty": 12,
                    "corruption": 30,
                    "type": "casual",
                    "conditions": {
                        "version": "1.0",
                        "items": [
                            {"type": "trait", "subject": "player",
                             "trait_key": "corruption", "operator": "gte", "value": 25},
                        ],
                    },
                },
            ],
            "locations": [
                {"id": loc_id, "name": "Reece's", "description": "The clothing shop."},
            ],
            "npcs": [],
            "canvases": [
                {
                    "id": canvas_id,
                    "name": "Start",
                    "type": "scene",
                    "trigger": {"location": loc_id, "is_active": True,
                                "is_repeatable": True},
                    "nodes": [
                        {
                            "id": "n1",
                            "name": "Start Node",
                            "blocks": [
                                {"type": "paragraph", "props": {},
                                 "content": [{"type": "text", "text": "test"}]}
                            ],
                        }
                    ],
                },
            ],
        }

    def _build(self, generator_cls):
        import copy
        from apps.projects.services.template_import import (
            normalize, validate, create_project_from_template,
        )
        template = normalize(copy.deepcopy(self._template()))
        errors = validate(template)
        self.assertEqual(errors, [], f"Fixture should validate clean: {errors}")
        result = create_project_from_template(template, str(self.user.id))
        project = Project.objects.get(id=result["project_id"])
        return generator_cls().generate(project)

    def _assert_gate_wired(self, twee):
        # The describe helper is emitted (generic threshold formatter).
        self.assertIn("setup.describeUnmetConditions = function", twee,
                      "describeUnmetConditions helper must be emitted")
        # buyItem resolves the reason then publishes the gated toast on failure.
        self.assertIn(
            "var why = setup.describeUnmetConditions(item.conditions);", twee,
            "buyItem must resolve the unmet-condition reason before notifying",
        )
        self.assertIn(
            'setup.queueGatedNotification(why ? ("Not yet — needs " + why)',
            twee,
            "buyItem must queue a gated notification describing the unmet condition",
        )
        # The shop handler flushes the toast after the buy attempt.
        self.assertIn(
            "setup.buyItem(String(itemId));\n        setup.showEffectNotification();",
            twee,
            "shop buy handler must flush the gated toast via showEffectNotification",
        )

    def test_v2_gate_feedback_wired(self):
        from apps.game_generation.twee_comprehensive.generators.v2 import (
            TweeComprehensiveGeneratorV2,
        )
        self._assert_gate_wired(self._build(TweeComprehensiveGeneratorV2))

    def test_v1_gate_feedback_wired(self):
        from apps.game_generation.twee_comprehensive.generators.v1 import (
            TweeComprehensiveGeneratorV1,
        )
        self._assert_gate_wired(self._build(TweeComprehensiveGeneratorV1))


class ChoiceCostsTests(TestCase):
    """Per-choice `costs` — tiered "main lock, then energy cost" gating (2026-06-06).

    An exit choice can carry `costs = [{trait, value}]` — the resource tier UNDER its
    `conditions` (main lock). Render is nested: main-lock `conditions` (outer) →
    affordability (inner). A cost-blocked rung shows as a plain greyed `locked-choice`
    span with `getCostBlockedMessage` (NOT a clickable button), the cost deducts on
    click, and a choice WITHOUT costs is unchanged. Mirrors canvas-level `costs`.
    Verified across v1 + v2 parity.
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="choice-costs@example.com", password="testpass123"
        )

    def _template(self, *, with_costs):
        canvas_id = "canvas_start"
        loc_id = "loc_bar"
        # Cost-only choice (no main lock) + tiered choice (main lock + cost) when
        # with_costs; otherwise two plain choices (backward-compat baseline).
        if with_costs:
            choices = [
                {
                    "text": "Work a shift",
                    "targetType": "trigger",
                    "effects": [
                        {"targetType": "player", "trait": "money", "op": "add", "value": 50},
                    ],
                    "costs": [{"trait": "energy", "value": 15}],
                },
                {
                    "text": "Work the floor in less",
                    "targetType": "trigger",
                    "show_when_locked": True,
                    "locked_text": "In less (needs corruption)",
                    "conditions": {
                        "version": "1.0",
                        "items": [
                            {"type": "trait", "subject": "player",
                             "trait_key": "corruption", "operator": "gte", "value": 10},
                        ],
                    },
                    "effects": [
                        {"targetType": "player", "trait": "money", "op": "add", "value": 90},
                    ],
                    "costs": [{"trait": "energy", "value": 15}],
                },
            ]
        else:
            choices = [
                {"text": "Leave", "targetType": "trigger", "effects": []},
            ]
        return {
            "schema_version": "1.0",
            "project": {
                "id": "choice_costs_test",
                "title": "Choice Costs Fixture",
                "description": "Minimal fixture for per-choice costs.",
                "starting_canvas": canvas_id,
            },
            "time": {"enabled": True, "starting_hour": 8, "starting_day": "Monday"},
            "player": {
                "id": "player",
                "name": "Test Player",
                "core_traits": {"corruption": 0, "energy": 100, "money": 0},
                "flag_keys": [],
            },
            "locations": [
                {"id": loc_id, "name": "The Bar", "description": "Test bar."},
            ],
            "npcs": [],
            "canvases": [
                {
                    "id": canvas_id,
                    "name": "Start",
                    "type": "scene",
                    "trigger": {"location": loc_id, "is_active": True,
                                "is_repeatable": True, "trigger_mode": "manual"},
                    "nodes": [
                        {
                            "id": "n1",
                            "name": "Start Node",
                            "blocks": [{"type": "paragraph", "props": {},
                                        "content": [{"type": "text", "text": "test"}]}],
                            "exit_block": {"type": "choices", "choices": choices},
                        }
                    ],
                },
            ],
        }

    def _build(self, generator_cls, *, with_costs):
        import copy
        from apps.projects.services.template_import import (
            normalize, validate, create_project_from_template,
        )
        template = normalize(copy.deepcopy(self._template(with_costs=with_costs)))
        errors = validate(template)
        self.assertEqual(errors, [], f"Fixture should validate clean: {errors}")
        result = create_project_from_template(template, str(self.user.id))
        project = Project.objects.get(id=result["project_id"])
        return generator_cls().generate(project)

    def _assert_costs_wired(self, twee):
        # The inner cost-affordability gate is emitted as a passage <<if>>.
        self.assertIn("<<if setup.checkCostsAffordable(", twee,
                      "per-choice cost gate must emit a checkCostsAffordable <<if>>")
        # Cost-blocked rung = greyed span with the dynamic resource message.
        self.assertIn("<<= setup.getCostBlockedMessage(", twee,
                      "cost-blocked rung must render getCostBlockedMessage")
        self.assertIn('<span class="locked-choice"', twee,
                      "cost-blocked rung must be a greyed locked-choice span")
        # The rung KEEPS the action label and appends the requirement beside it
        # (doesn't replace the choice text with the bare message).
        self.assertIn("Work a shift (<<= setup.getCostBlockedMessage(", twee,
                      "cost-blocked rung must keep the choice text before the requirement")
        # The cost deducts on click (energy -15), NOT via effects.
        self.assertIn('"energy", "add", -15', twee,
                      "per-choice cost must deduct energy on click")
        # The tiered choice's main-lock label still appears (outer conditions tier).
        self.assertIn("In less (needs corruption)", twee,
                      "main-lock locked_text must still render for the outer tier")
        # When all rungs are cost/condition-locked, the player gets a clean Continue
        # escape — NOT the contradictory "No available choices" line (the rungs are
        # still shown greyed with their own reason).
        self.assertIn("[[Continue->", twee,
                      "all-locked canvas must still offer a Continue escape")
        self.assertNotIn("No available choices", twee,
                         "the redundant 'No available choices' line must be gone")

    def test_v2_choice_costs_wired(self):
        from apps.game_generation.twee_comprehensive.generators.v2 import (
            TweeComprehensiveGeneratorV2,
        )
        self._assert_costs_wired(self._build(TweeComprehensiveGeneratorV2, with_costs=True))

    def test_v1_choice_costs_wired(self):
        from apps.game_generation.twee_comprehensive.generators.v1 import (
            TweeComprehensiveGeneratorV1,
        )
        self._assert_costs_wired(self._build(TweeComprehensiveGeneratorV1, with_costs=True))

    def test_v2_no_costs_no_guard(self):
        """Backward-compat: a choice without costs emits no cost guard."""
        from apps.game_generation.twee_comprehensive.generators.v2 import (
            TweeComprehensiveGeneratorV2,
        )
        twee = self._build(TweeComprehensiveGeneratorV2, with_costs=False)
        self.assertNotIn("<<if setup.checkCostsAffordable(", twee,
                         "no costs anywhere → no per-choice cost guard call site")

    def test_v1_no_costs_no_guard(self):
        from apps.game_generation.twee_comprehensive.generators.v1 import (
            TweeComprehensiveGeneratorV1,
        )
        twee = self._build(TweeComprehensiveGeneratorV1, with_costs=False)
        self.assertNotIn("<<if setup.checkCostsAffordable(", twee,
                         "no costs anywhere → no per-choice cost guard call site")


class TravelFrictionAndLockProseTests(TestCase):
    """Location entry-cost (travel friction) + lock-as-prose on the nav surface
    (2026-06-18). v2-only — the v1 generator is deprecated.

    Travel friction: a [[locations]] `costs = {time, energy}` is charged on a genuine
    move (entering a DIFFERENT location), enforced in the :passagestart guard.
    Lock-as-prose: a destination with entry_conditions renders its blocked_message
    in-place on the nav (greyed, non-clickable) instead of only on the blocked passage.
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="travel-friction@example.com", password="testpass123"
        )

    def _build_template(self, *, costs=None, entry_conditions=None, blocked_message=""):
        """Kitchen (start) → Pantry (a reachable destination that may carry an entry
        cost and/or a visible-but-blocked lock). One ungated canvas at the kitchen so
        the build validates."""
        start = "loc_kitchen"
        dest = "loc_pantry"
        canvas_id = "canvas_kitchen_idle"
        pantry = {"id": dest, "name": "Pantry", "description": "A back pantry.",
                  "entry_from": start}
        if costs is not None:
            pantry["costs"] = costs
        if entry_conditions is not None:
            pantry["entry_conditions"] = entry_conditions
        if blocked_message:
            pantry["blocked_message"] = blocked_message
        return {
            "schema_version": "1.0",
            "project": {"id": "travel_test", "title": "Travel Fixture",
                        "description": "Travel-friction + lock-as-prose fixture.",
                        "starting_canvas": canvas_id},
            "time": {"enabled": True, "starting_hour": 8, "starting_day": "Monday"},
            "locations": [
                {"id": start, "name": "Kitchen", "description": "Test kitchen",
                 "navigation_order": [dest]},
                pantry,
            ],
            "npcs": [],
            "canvases": [
                {"id": canvas_id, "name": "Kitchen Idle", "type": "scene",
                 "trigger": {"location": start, "is_active": True, "is_repeatable": True},
                 "nodes": [{"id": "n1", "name": "N1", "blocks": [
                     {"type": "paragraph", "props": {},
                      "content": [{"type": "text", "text": "test"}]}]}]},
            ],
        }

    def _generate(self, raw):
        import copy
        from apps.projects.services.template_import import (
            normalize, validate, create_project_from_template)
        from apps.game_generation.twee_comprehensive.generators.v2 import (
            TweeComprehensiveGeneratorV2)
        template = normalize(copy.deepcopy(raw))
        errors = validate(template)
        self.assertEqual(errors, [], f"Fixture should validate clean: {errors}")
        result = create_project_from_template(template, str(self.user.id))
        project = Project.objects.get(id=result["project_id"])
        return TweeComprehensiveGeneratorV2().generate(project)

    @staticmethod
    def _extract_setup_assignment(twee, varname):
        import json
        import re
        m = re.search(r'setup\.' + re.escape(varname) + r'\s*=\s*', twee)
        if not m:
            return None
        start = m.end()
        if start >= len(twee) or twee[start] != '{':
            return None
        depth = 0
        for i in range(start, len(twee)):
            ch = twee[i]
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    return json.loads(twee[start:i + 1])
        return None

    # ----- Travel friction -----
    def test_entry_costs_round_trip_into_setup_locations(self):
        """costs in TOML → importer properties['entry_costs'] → setup.locations blob.
        One assertion exercises the whole parse→properties→emit path."""
        twee = self._generate(self._build_template(costs={"time": 30, "energy": 10}))
        locs = self._extract_setup_assignment(twee, "locations")
        self.assertIsNotNone(locs, "setup.locations should be emitted")
        self.assertEqual(locs.get("loc_pantry", {}).get("entry_costs"),
                         {"time": 30, "energy": 10})

    def test_travel_block_passage_emitted_only_with_costs(self):
        with_costs = self._generate(self._build_template(costs={"energy": 5}))
        self.assertIn(":: TravelBlock", with_costs)
        self.assertIn("Travel-friction intercept", with_costs)
        without = self._generate(self._build_template())
        self.assertNotIn(":: TravelBlock", without)
        self.assertNotIn("Travel-friction intercept", without)

    def test_cost_tag_rendered_in_nav(self):
        twee = self._generate(self._build_template(costs={"time": 30}))
        self.assertIn('setup.getLocationCostTag("loc_pantry")', twee)

    def test_deduct_location_costs_advances_time(self):
        twee = self._generate(self._build_template(costs={"time": 30}))
        self.assertIn("setup.deductLocationCosts = function", twee)
        self.assertIn("window.advanceTime(mins)", twee)

    def test_validate_rejects_negative_cost(self):
        import copy
        from apps.projects.services.template_import import normalize, validate
        template = normalize(copy.deepcopy(self._build_template(costs={"energy": -5})))
        errors = validate(template)
        self.assertTrue(any("costs" in e and "negative" in e for e in errors),
                        f"expected a negative-cost validation error, got {errors}")

    # ----- Lock-as-prose -----
    def _flag_conditions(self):
        return {"version": "1.0", "items": [
            {"type": "flag", "subject": "player", "flag_key": "pantry_open",
             "operator": "is_true"}]}

    def test_entry_conditions_round_trip_into_setup_locations(self):
        ec = self._flag_conditions()
        twee = self._generate(self._build_template(
            entry_conditions=ec, blocked_message="It's locked."))
        locs = self._extract_setup_assignment(twee, "locations")
        self.assertEqual(locs.get("loc_pantry", {}).get("entry_conditions"), ec)
        self.assertEqual(locs.get("loc_pantry", {}).get("blocked_message"), "It's locked.")

    def test_nav_wraps_locked_destination(self):
        twee = self._generate(self._build_template(
            entry_conditions=self._flag_conditions(), blocked_message="It's locked."))
        self.assertIn('setup.navDestUnlocked("loc_pantry")', twee)
        self.assertIn('setup.navDestBlockedReason("loc_pantry")', twee)
        # The greyed branch renders in whichever nav mode the fixture lands in.
        self.assertTrue("location-card-locked" in twee or "nav-link-locked" in twee,
                        "a locked destination should render the greyed lock-as-prose branch")

    def test_unlocked_destination_navigable(self):
        """No entry_conditions → setup.locations carries an empty dict (fail-open) and
        the destination is still a real navigable target."""
        twee = self._generate(self._build_template())
        locs = self._extract_setup_assignment(twee, "locations")
        self.assertEqual(locs.get("loc_pantry", {}).get("entry_conditions"), {})
        self.assertTrue('data-passage="Location_Pantry"' in twee
                        or "[[Pantry->Location_Pantry]]" in twee,
                        "an unlocked destination should be a navigable nav target")

    def test_navdest_unlocked_helper_fails_open_on_versionless(self):
        """Structural guard: the helper short-circuits to open when there are no
        condition items, so a versionless/empty block renders a normal link (the same
        fail-open the passage guard + the global evaluator use)."""
        twee = self._generate(self._build_template(costs={"energy": 1}))
        self.assertIn("if (!ec.items || ec.items.length === 0) return true;", twee)

    def test_passage_guard_and_nav_share_blocked_reason(self):
        twee = self._generate(self._build_template(
            entry_conditions=self._flag_conditions(), blocked_message="It's locked."))
        # The passage backstop renders the same authored message the nav helper returns.
        self.assertIn("entry-blocked-narrative", twee)
        self.assertIn("It's locked.", twee)


class CascadeLocationExitSpliceTests(TestCase):
    """Regression (2026-06-22) — a cascade on a ``type="location"`` (single
    "Continue") exit node must splice its exit link INTO the cascade's last
    ``<<linkreplace>>`` beat, exactly like the ``type="choices"`` branch already
    did.

    Before the fix the cascade-exit splice ran ONLY in the ``exit_type=='choices'``
    branch of ``_generate_canvas_node_passages``; the location/default branch
    appended ``[[Continue->...]]`` at the passage bottom and never touched the
    planted ``__CASCADE_EXIT_INJECT__`` sentinel. Result: the cascade's advance
    "show more" link and the exit link rendered at the same time (exit visible
    from the first beat), letting the player skip the whole scene in one click —
    and the sentinel leaked into the built HTML un-substituted. Live-caught on
    Vesper's opening cold-open (the cradle/morning canvases).
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="cascade-loc-exit@example.com", password="testpass123"
        )

    @staticmethod
    def _para(text):
        return {"type": "paragraph", "props": {},
                "content": [{"type": "text", "text": text}]}

    def _build_template(self, *, exit_type="location", gated_beat=False):
        canvas_id = "canvas_cascade_test"
        beats = [
            {"blocks": [self._para("BEAT_ZERO_MARKER opens on entry.")]},
            {"advance_text": "Show more.",
             "blocks": [self._para("BEAT_ONE_MARKER revealed on click.")]},
            {"advance_text": "And more.",
             "blocks": [self._para("BEAT_TWO_MARKER the terminal beat.")]},
        ]
        if gated_beat:
            # Any beat with a non-empty conditions.items forces the SAFE path.
            beats[1]["conditions"] = {
                "version": "1.0", "logic": "AND",
                "items": [{"type": "trait", "trait": "energy",
                           "operator": "gte", "value": 999}],
            }
        node = {"id": "n1", "name": "Cascade Node",
                "blocks": [{"type": "cascade",
                            "props": {"id": "test_cascade", "beats": beats}}]}
        if exit_type == "location":
            node["exit_block"] = {"type": "location", "config": {}}
        else:
            node["exit_block"] = {
                "type": "choices",
                "choices": [{"text": "Continue", "targetType": "location",
                             "locationId": "loc_room"}],
            }
        return {
            "schema_version": "1.0",
            "project": {
                "id": "cascade_loc_exit_test",
                "title": "Cascade Location-Exit Fixture",
                "description": "Minimal fixture for the cascade location-exit splice regression.",
                "starting_canvas": canvas_id,
            },
            "time": {"enabled": True, "starting_hour": 8, "starting_day": "Monday"},
            "locations": [{"id": "loc_room", "name": "Room", "description": "Test room"}],
            "canvases": [{
                "id": canvas_id, "name": "Cascade Test Canvas", "type": "scene",
                "trigger": {"location": "loc_room", "is_active": True},
                "nodes": [node],
            }],
        }

    def _generate(self, raw):
        import copy
        from apps.projects.services.template_import import (
            normalize, validate, create_project_from_template,
        )
        from apps.game_generation.twee_comprehensive.generators.v2 import (
            TweeComprehensiveGeneratorV2,
        )
        template = normalize(copy.deepcopy(raw))
        errors = validate(template)
        self.assertEqual(errors, [], f"Fixture should validate clean: {errors}")
        result = create_project_from_template(template, str(self.user.id))
        project = Project.objects.get(id=result["project_id"])
        return TweeComprehensiveGeneratorV2().generate(project)

    def _node_passage(self, twee, marker="BEAT_ZERO_MARKER"):
        for p in twee.split("\n:: "):
            if marker in p:
                return p
        self.fail(f"No passage contained {marker}")

    def test_location_exit_cascade_splices_exit_into_last_beat(self):
        twee = self._generate(self._build_template(exit_type="location"))
        # The sentinel must never leak — it is always substituted or stripped.
        self.assertNotIn("__CASCADE_EXIT_INJECT__", twee,
                         "cascade-exit sentinel leaked un-substituted into output")
        passage = self._node_passage(twee)
        self.assertIn("<<linkreplace", passage, "cascade should render linkreplace beats")
        last_close = passage.rfind("<</linkreplace>>")
        self.assertNotEqual(last_close, -1, "the cascade must close a linkreplace")
        head, tail = passage[:last_close], passage[last_close:]
        # Exit link spliced INSIDE the cascade (before the final close)...
        self.assertRegex(head, r"\[\[[^\]]+->[^\]]+\]\]",
                         "location-exit cascade must splice its exit INTO the last "
                         "<<linkreplace>> beat")
        # ...and NOT rendered at the passage bottom (after the cascade closes).
        self.assertNotRegex(tail, r"\[\[[^\]]+->[^\]]+\]\]",
                            "no exit link may render at passage bottom beside the "
                            "advance 'show more' link")

    def test_choices_exit_cascade_still_defers_exit(self):
        """Control: the pre-existing choices-exit branch is unchanged — its
        choice links still splice inside the cascade, none at passage bottom."""
        twee = self._generate(self._build_template(exit_type="choices"))
        self.assertNotIn("__CASCADE_EXIT_INJECT__", twee)
        passage = self._node_passage(twee)
        last_close = passage.rfind("<</linkreplace>>")
        link_idx = passage.find("<<link")
        self.assertTrue(0 <= link_idx < last_close,
                        "choices-exit cascade should keep deferring exits inside the cascade")

    def test_safe_path_gated_cascade_keeps_exit_at_bottom(self):
        """A gated beat forces the SAFE path: the sentinel is stripped (never
        leaks) and the single exit stays at passage bottom so the player can't
        be stranded if the gate fails mid-cascade."""
        twee = self._generate(self._build_template(exit_type="location", gated_beat=True))
        self.assertNotIn("__CASCADE_EXIT_INJECT__", twee)
        self.assertNotIn("__CASCADE_EXIT_INJECT_SAFE__", twee)
        passage = self._node_passage(twee)
        last_close = passage.rfind("<</linkreplace>>")
        tail = passage[last_close:]
        self.assertRegex(tail, r"\[\[[^\]]+->[^\]]+\]\]",
                         "SAFE (gated) cascade must keep the exit reachable at passage bottom")
