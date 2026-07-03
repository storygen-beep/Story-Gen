"""
Twee Comprehensive System Service.

Service layer for the twee comprehensive generation system.
Handles validation, generation, and system-specific business logic.
"""

from typing import Any, Optional

from apps.projects.models import Project

from .generators.v1 import TweeComprehensiveGeneratorV1
from .generators.v2 import TweeComprehensiveGeneratorV2


class TweeComprehensiveService:
    """
    Service for Twee comprehensive game generation.

    This service is completely isolated and handles all comprehensive game logic.
    """

    def generate(
        self,
        project: Project,
        version: str = "v2",
        options: Optional[dict] = None,
        graph: Optional[object] = None,
    ) -> str:
        """
        Generate comprehensive game using the specified version.

        Args:
            project: Django Project instance
            version: Generator version to use
            options: Optional generation options

        Returns:
            str: Generated Twee content

        Raises:
            ValueError: If version not found or generation fails
        """
        # Select generator based on version
        if version == "v2":
            generator = TweeComprehensiveGeneratorV2()
        elif version == "v1":
            # v1 frozen 2026-05-14 — safe-mode rollback path only.
            generator = TweeComprehensiveGeneratorV1()
        else:
            raise ValueError(
                f"Version {version} not found for twee_comprehensive system"
            )

        # Validate project before generation. The no-DB graph path already
        # validated the template during build_game_graph, and validate_project
        # queries the ORM (which the unsaved graph project isn't in), so skip it.
        if graph is None:
            validation_result = self.validate_project(project)
            if validation_result["has_errors"]:
                raise ValueError(
                    f"Project validation failed: {validation_result['errors']}"
                )

        # Store generator reference for asset tracking
        self._last_generator = generator

        # Generate content
        return generator.generate(project, options, graph=graph)

    def validate_project(self, project: Project) -> dict[str, Any]:
        """
        Validate if project is suitable for comprehensive game generation.

        DEPRECATED for the no-DB build path (which validates the template during
        build_game_graph and skips this); queries the ORM for a persisted
        Project. Kept for the web-API / elora / legacy DB callers.

        Args:
            project: Project to validate

        Returns:
            Dict with validation results
        """
        from apps.world.models import Location

        validation_result = {
            "has_errors": False,
            "warnings": [],
            "errors": [],
            "stats": {},
        }

        # Check for starting canvas
        has_starting_canvas = project.starting_canvas is not None
        validation_result["stats"]["has_starting_canvas"] = has_starting_canvas

        if not has_starting_canvas:
            validation_result["warnings"].append(
                "No starting canvas found. A default intro will be used."
            )

        # Check for locations (optional but recommended)
        locations = Location.objects.filter(project=project)
        validation_result["stats"]["location_count"] = locations.count()

        if locations.count() == 0:
            validation_result["warnings"].append(
                "No locations found. Navigation will be minimal."
            )

        # We don't require any specific content - the system can work with minimal data
        # If there's no content at all, we'll generate a basic experience

        return validation_result

    def get_capabilities(self) -> dict[str, Any]:
        """
        Get capabilities of this generation system.

        Returns:
            Dict describing system capabilities
        """
        return {
            "system_type": "twee_comprehensive",
            "name": "Twee Comprehensive Game Generator",
            "description": "Generates canvas-based interactive experiences with simple navigation",
            "versions": ["v1", "v2"],
            "current_version": "v2",
            "output_format": "twee",
            "features": [
                "Starting canvas display",
                "Canvas-to-navigation transition",
                "Basic location navigation",
                "Simple game flow",
            ],
            "layers": [
                "Game Entry Layer (Project info, Start game)",
                "Canvas Layer (Starting canvas display)",
                "Navigation Layer (Location-to-location movement)",
                "Location Layer (Basic location descriptions)",
            ],
            "requirements": [
                "Optional: Starting canvas",
                "Optional: Locations",
                "Works with minimal project data",
            ],
        }
