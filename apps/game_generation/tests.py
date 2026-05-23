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
