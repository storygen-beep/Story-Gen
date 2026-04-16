"""
Tests for Game Generation System.

Comprehensive tests for the modular game generation architecture.
"""

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
