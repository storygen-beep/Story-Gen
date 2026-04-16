"""
Twee Navigation System Service.

Service layer for the twee navigation generation system.
Handles validation, generation, and system-specific business logic.
"""

from typing import Any, Optional

from apps.projects.models import Project

from .generators.v1 import TweeNavigationGeneratorV1


class TweeNavigationService:
    """
    Service for Twee navigation game generation.

    This service is completely isolated and handles all navigation-specific logic.
    """

    def generate(
        self, project: Project, version: str = "v1", options: Optional[dict] = None
    ) -> str:
        """
        Generate navigation game using the specified version.

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
        if version == "v1":
            generator = TweeNavigationGeneratorV1()
        else:
            raise ValueError(f"Version {version} not found for twee_navigation system")

        # Validate project before generation
        validation_result = self.validate_project(project)
        if not validation_result["is_valid"]:
            raise ValueError(
                f"Project validation failed: {validation_result['errors']}"
            )

        # Generate content
        return generator.generate(project, options)

    def validate_project(self, project: Project) -> dict[str, Any]:
        """
        Validate if project is suitable for navigation game generation.

        Args:
            project: Project to validate

        Returns:
            Dict with validation results
        """
        from apps.world.models import Location

        validation_result = {
            "is_valid": True,
            "warnings": [],
            "errors": [],
            "location_count": 0,
        }

        # Check for locations
        locations = Location.objects.filter(project=project)
        validation_result["location_count"] = locations.count()

        if not locations.exists():
            validation_result["is_valid"] = False
            validation_result["errors"].append(
                "No locations found. Navigation game requires at least one location."
            )

        # Check for starting location
        has_starting = any(
            getattr(loc, "is_starting_location", False) for loc in locations
        )

        if not has_starting and locations.exists():
            validation_result["warnings"].append(
                "No starting location set. First location will be used."
            )

        return validation_result

    def get_capabilities(self) -> dict[str, Any]:
        """
        Get capabilities of this generation system.

        Returns:
            Dict describing system capabilities
        """
        return {
            "system_type": "twee_navigation",
            "name": "Twee Navigation Game Generator",
            "description": "Generates simple navigation-based exploration games",
            "versions": ["v1"],
            "current_version": "v1",
            "output_format": "twee",
            "features": [
                "World exploration",
                "Location discovery",
                "Simple navigation",
                "Bidirectional connections",
            ],
            "requirements": ["At least one location", "Optional: Location connections"],
        }
