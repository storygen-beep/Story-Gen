"""
Twee Comprehensive System Service.

Service layer for the twee comprehensive generation system.
Handles validation, generation, and system-specific business logic.
"""

from typing import Any, Optional

from apps.projects.models import Project

from .generators.v1 import TweeComprehensiveGeneratorV1


class TweeComprehensiveService:
    """
    Service for Twee comprehensive game generation.

    This service is completely isolated and handles all comprehensive game logic.
    """

    def generate(
        self, project: Project, version: str = "v1", options: Optional[dict] = None
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
        if version == "v1":
            generator = TweeComprehensiveGeneratorV1()
        else:
            raise ValueError(
                f"Version {version} not found for twee_comprehensive system"
            )

        # Validate project before generation
        validation_result = self.validate_project(project)
        if validation_result["has_errors"]:
            raise ValueError(
                f"Project validation failed: {validation_result['errors']}"
            )

        # Generate content
        return generator.generate(project, options)

    def validate_project(self, project: Project) -> dict[str, Any]:
        """
        Validate if project is suitable for comprehensive game generation.

        Args:
            project: Project to validate

        Returns:
            Dict with validation results
        """
        from apps.characters.models import Character
        from apps.npcs.models import NPC
        from apps.world.models import Location

        validation_result = {
            "has_errors": False,
            "warnings": [],
            "errors": [],
            "stats": {},
        }

        # Check for player character
        try:
            character = project.player_character
            validation_result["stats"]["has_player_character"] = True
        except Character.DoesNotExist:
            validation_result["warnings"].append(
                "No player character found. Default character will be used."
            )
            validation_result["stats"]["has_player_character"] = False

        # Check for NPCs
        npcs = NPC.objects.filter(project=project, deleted_at__isnull=True)
        validation_result["stats"]["npc_count"] = npcs.count()

        if npcs.count() == 0:
            validation_result["warnings"].append(
                "No NPCs found. NPC interactions will be limited."
            )

        # Check for locations
        locations = Location.objects.filter(project=project)
        validation_result["stats"]["location_count"] = locations.count()

        if locations.count() == 0:
            validation_result["warnings"].append(
                "No locations found. World exploration will be limited."
            )

        # Check if we have at least some content
        if (
            not validation_result["stats"]["has_player_character"]
            and validation_result["stats"]["npc_count"] == 0
            and validation_result["stats"]["location_count"] == 0
        ):
            validation_result["has_errors"] = True
            validation_result["errors"].append(
                "Project has no content for comprehensive game generation."
            )

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
            "description": "Generates sophisticated interactive experiences with multiple layers",
            "versions": ["v1"],
            "current_version": "v1",
            "output_format": "twee",
            "features": [
                "Character progression",
                "NPC interactions",
                "Location discovery",
                "Time management",
                "Relationship tracking",
                "Activity system",
                "Dialogue system",
                "Choice consequences",
            ],
            "layers": [
                "Foundation Layer (Location, Time, Flags)",
                "Character Layer (Player, NPCs, Traits)",
                "Interaction Layer (Navigation, Activities, Triggers)",
                "Narrative Layer (Scenes, Dialogue, Choices)",
                "Presentation Layer (UI, Game Hub)",
            ],
            "requirements": [
                "Optional: Player character",
                "Optional: NPCs",
                "Optional: Locations",
                "At least one content type recommended",
            ],
        }
