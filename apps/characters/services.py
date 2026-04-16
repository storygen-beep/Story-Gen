"""
Character Management service layer.

Provides business logic for character operations including CRUD, validation,
limits enforcement, and template generation.
"""

from typing import Any, Optional

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.projects.models import Project
from apps.world.models import Location

from .models import Character


class CharacterService:
    """Service layer for character management operations."""

    @staticmethod
    def get_player_character(project: Project) -> Optional[Character]:
        """
        Get the player character for a project.

        Args:
            project: Project instance

        Returns:
            Character instance or None if not found
        """
        try:
            return project.player_character
        except Character.DoesNotExist:
            return None

    @staticmethod
    def get_player_character_overview(project: Project) -> dict[str, Any]:
        """
        Get player character overview for a project.

        Args:
            project: Project instance

        Returns:
            Dictionary containing player character data
        """
        character = CharacterService.get_player_character(project)

        return {
            "project_id": str(project.id),
            "has_character": character is not None,
            "character": character.to_dict(include_details=True) if character else None,
        }

    @staticmethod
    def create_character(
        project: Project, character_data: dict[str, Any], user
    ) -> Character:
        """
        Create the player character for a project.

        Args:
            project: Project instance
            character_data: Character creation data
            user: User creating the character

        Returns:
            Created Character instance

        Raises:
            ValidationError: If character already exists or validation fails
        """
        # Check if character already exists
        try:
            existing_character = project.player_character
            raise ValidationError("Player character already exists for this project")
        except Character.DoesNotExist:
            pass  # Character doesn't exist, we can create one

        # Validate location if provided
        location_id = character_data.get("current_location")
        if location_id:
            try:
                location = Location.objects.get(id=location_id, project=project)
                character_data["current_location"] = location
            except Location.DoesNotExist:
                raise ValidationError("Invalid location for this project")

        # Create character with transaction
        with transaction.atomic():
            character = Character.objects.create(
                project=project, **character_data
            )

        return character

    @staticmethod
    def update_character(
        character: Character, character_data: dict[str, Any], user
    ) -> Character:
        """
        Update an existing character.

        Args:
            character: Character instance to update
            character_data: Update data
            user: User updating the character

        Returns:
            Updated Character instance
        """
        # Validate location if provided
        location_id = character_data.get("current_location")
        if location_id:
            try:
                location = Location.objects.get(
                    id=location_id, project=character.project
                )
                character_data["current_location"] = location
            except Location.DoesNotExist:
                raise ValidationError("Invalid location for this project")

        # Update character with transaction
        with transaction.atomic():
            for field, value in character_data.items():
                if hasattr(character, field):
                    setattr(character, field, value)

            # Character updated automatically
            character.save()

        return character

    @staticmethod
    def delete_character(character: Character) -> bool:
        """
        Soft delete a character.

        Args:
            character: Character instance to delete

        Returns:
            True if successful
        """
        try:
            character.soft_delete()
            return True
        except Exception:
            return False

    @staticmethod
    def update_character_traits(
        character: Character, traits_data: dict[str, Any], user
    ) -> dict[str, Any]:
        """
        Update character traits.

        Args:
            character: Character instance
            traits_data: Traits data to update
            user: User updating the traits

        Returns:
            Updated traits data
        """
        with transaction.atomic():
            updated_traits = {}

            if "core_traits" in traits_data:
                new_traits = traits_data["core_traits"]
                if isinstance(new_traits, dict):
                    # Merge with existing traits
                    current_traits = character.core_traits or {}
                    current_traits.update(new_traits)
                    character.core_traits = current_traits
                    updated_traits["core_traits"] = current_traits

            # Character updated automatically
            character.save()

        return {"character_id": str(character.id), "traits": updated_traits}

    @staticmethod
    def update_character_relationships(
        character: Character, relationships_data: dict[str, Any], user
    ) -> dict[str, Any]:
        """
        Update character relationships.

        Args:
            character: Character instance
            relationships_data: Relationships data
            user: User updating the relationships

        Returns:
            Updated relationships data
        """
        with transaction.atomic():
            relationships = relationships_data.get("relationships", {})

            # Merge with existing relationships
            current_relationships = character.relationships or {}
            current_relationships.update(relationships)

            character.relationships = current_relationships
            # Character updated automatically
            character.save()

        return {
            "character_id": str(character.id),
            "relationships": current_relationships,
        }

    @staticmethod
    def update_character_location(
        character: Character, location_data: dict[str, Any], user
    ) -> dict[str, Any]:
        """
        Update character location assignment.

        Args:
            character: Character instance
            location_data: Location assignment data
            user: User updating the location

        Returns:
            Updated location data
        """
        location_id = location_data.get("location_id")

        if location_id:
            try:
                location = Location.objects.get(
                    id=location_id, project=character.project
                )

                with transaction.atomic():
                    character.current_location = location
                    # Character updated automatically
                    character.save()

                return {
                    "character_id": str(character.id),
                    "locations": {
                        "current_location_id": str(location.id),
                        "current_location_name": location.name,
                    },
                }
            except Location.DoesNotExist:
                raise ValidationError("Invalid location for this project")
        else:
            # Clear current location
            with transaction.atomic():
                character.current_location = None
                # Character updated automatically
                character.save()

            return {
                "character_id": str(character.id),
                "locations": {
                    "current_location_id": None,
                    "current_location_name": None,
                },
            }

    @staticmethod
    def get_character_templates() -> dict[str, Any]:
        """
        Get character creation templates and presets.

        Returns:
            Dictionary with character templates
        """
        return {
            "trait_templates": {
                "core_traits": [
                    {
                        "name": "Strength",
                        "type": "number",
                        "min": 1,
                        "max": 10,
                        "default": 5,
                    },
                    {
                        "name": "Intelligence",
                        "type": "number",
                        "min": 1,
                        "max": 10,
                        "default": 5,
                    },
                    {
                        "name": "Charisma",
                        "type": "number",
                        "min": 1,
                        "max": 10,
                        "default": 5,
                    },
                    {
                        "name": "Wisdom",
                        "type": "number",
                        "min": 1,
                        "max": 10,
                        "default": 5,
                    },
                    {
                        "name": "Dexterity",
                        "type": "number",
                        "min": 1,
                        "max": 10,
                        "default": 5,
                    },
                ],
            },
            "relationship_types": [
                {"value": "friend", "label": "Friend"},
                {"value": "enemy", "label": "Enemy"},
                {"value": "family", "label": "Family"},
                {"value": "romantic", "label": "Romantic Interest"},
                {"value": "mentor", "label": "Mentor"},
                {"value": "rival", "label": "Rival"},
                {"value": "neutral", "label": "Neutral"},
            ],
        }

    @staticmethod
    def get_character_by_id(character_id: str, project: Project) -> Optional[Character]:
        """
        Get character by ID within project scope.

        Args:
            character_id: Character UUID
            project: Project instance

        Returns:
            Character instance or None
        """
        try:
            return Character.objects.get(
                id=character_id, project=project, deleted_at__isnull=True
            )
        except Character.DoesNotExist:
            return None

    @staticmethod
    def validate_character_limits(project: Project) -> tuple[int, int, bool]:
        """
        Validate character limits for a project.

        Args:
            project: Project instance

        Returns:
            Tuple of (current_count, max_characters, can_create)
        """
        current_count = Character.objects.filter(
            project=project, deleted_at__isnull=True
        ).count()

        max_characters = (
            project.settings.get("max_characters", 50) if project.settings else 50
        )
        can_create = current_count < max_characters

        return current_count, max_characters, can_create
