"""
Character Management serializers for Django REST Framework.

Provides serialization for character CRUD operations, trait management,
and template generation.
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.world.models import Location

from .models import Character

User = get_user_model()


class CharacterListSerializer(serializers.ModelSerializer):
    """Serializer for character list views."""

    project_id = serializers.UUIDField(source="project.id", read_only=True)
    current_location_id = serializers.UUIDField(
        source="current_location.id", read_only=True, allow_null=True
    )

    class Meta:
        model = Character
        fields = [
            "id",
            "project_id",
            "name",
            "description",
            "status",
            "age",
            "gender",
            "appearance",
            "portrait_url",
            "core_traits",
            "flag_keys",
            "current_location_id",
            "tags",
            "categories",
            "experience_points",
            "character_level",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "project_id",
        ]


class CharacterDetailSerializer(serializers.ModelSerializer):
    """Serializer for character detail views with all fields."""

    project_id = serializers.UUIDField(source="project.id", read_only=True)
    current_location_id = serializers.UUIDField(
        source="current_location.id", read_only=True, allow_null=True
    )

    class Meta:
        model = Character
        fields = [
            "id",
            "project_id",
            "name",
            "description",
            "status",
            "age",
            "gender",
            "appearance",
            "portrait_url",
            "core_traits",
            "flag_keys",
            "current_location_id",
            "relationships",
            "ai_behavior_config",
            "character_metadata",
            "game_properties",
            "tags",
            "categories",
            "development_notes",
            "inspiration_sources",
            "experience_points",
            "character_level",
            "progression_data",
            "inventory",
            "equipment",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "project_id",
        ]


class CharacterCreateSerializer(serializers.ModelSerializer):
    """Serializer for character creation."""

    class Meta:
        model = Character
        fields = [
            "name",
            "description",
            "age",
            "gender",
            "appearance",
            "core_traits",
            "flag_keys",
            "tags",
            "categories",
            "ai_behavior_config",
        ]

    def validate_name(self, value):
        """Validate character name is not empty."""
        if not value or not value.strip():
            raise serializers.ValidationError("Character name cannot be empty")
        return value.strip()

    def validate_age(self, value):
        """Validate character age range."""
        if value is not None and (value < 0 or value > 200):
            raise serializers.ValidationError("Age must be between 0 and 200")
        return value

    def validate_character_level(self, value):
        """Validate character level is at least 1."""
        if value is not None and value < 1:
            raise serializers.ValidationError("Character level must be at least 1")
        return value


class CharacterUpdateSerializer(serializers.ModelSerializer):
    """Serializer for character updates with partial updates support."""

    current_location = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Character
        fields = [
            "name",
            "description",
            "status",
            "age",
            "gender",
            "appearance",
            "portrait_url",
            "core_traits",
            "flag_keys",
            "current_location",
            "relationships",
            "ai_behavior_config",
            "tags",
            "categories",
            "development_notes",
            "inspiration_sources",
            "experience_points",
            "character_level",
            "progression_data",
            "inventory",
            "equipment",
        ]

    def validate_flag_keys(self, value):
        if value is None:
            return []
        if not isinstance(value, list):
            raise serializers.ValidationError("flag_keys must be a list of strings")
        for v in value:
            if not isinstance(v, str) or not v.strip():
                raise serializers.ValidationError("Each flag name must be a non-empty string")
        # Dedupe while preserving order
        seen = set()
        deduped = []
        for k in value:
            key = k.strip()
            if key not in seen:
                seen.add(key)
                deduped.append(key)
        return deduped

    def validate_name(self, value):
        """Validate character name is not empty."""
        if value is not None and (not value or not value.strip()):
            raise serializers.ValidationError("Character name cannot be empty")
        return value.strip() if value else value

    def validate_age(self, value):
        """Validate character age range."""
        if value is not None and (value < 0 or value > 200):
            raise serializers.ValidationError("Age must be between 0 and 200")
        return value

    def validate_character_level(self, value):
        """Validate character level is at least 1."""
        if value is not None and value < 1:
            raise serializers.ValidationError("Character level must be at least 1")
        return value

    def validate_current_location(self, value):
        """Validate current location belongs to same project."""
        if value and hasattr(self, "instance") and self.instance:
            if value.project_id != self.instance.project_id:
                raise serializers.ValidationError(
                    "Location must belong to the same project"
                )
        return value


class CharacterTraitsSerializer(serializers.Serializer):
    """Serializer for character traits update."""

    core_traits = serializers.DictField(required=False, allow_empty=True)

    def validate(self, data):
        """Ensure core traits are provided."""
        if not data.get("core_traits"):
            raise serializers.ValidationError("Core traits must be provided")
        return data


class CharacterRelationshipSerializer(serializers.Serializer):
    """Serializer for character relationships update."""

    relationships = serializers.DictField(required=True)

    def validate_relationships(self, value):
        """Validate relationships data structure."""
        if not isinstance(value, dict):
            raise serializers.ValidationError("Relationships must be a dictionary")
        return value


class CharacterLocationSerializer(serializers.Serializer):
    """Serializer for character location assignment."""

    location_id = serializers.UUIDField(required=True)

    def validate_location_id(self, value):
        """Validate location exists and belongs to project."""
        from apps.world.models import Location

        try:
            location = Location.objects.get(id=value)
            # Additional validation can be added here if context is needed
            return value
        except Location.DoesNotExist:
            raise serializers.ValidationError("Location not found")


class CharacterTemplateSerializer(serializers.Serializer):
    """Serializer for character templates and presets."""

    trait_templates = serializers.DictField(read_only=True)
    relationship_types = serializers.ListField(read_only=True)

    def to_representation(self, instance):
        """Generate template data."""
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


class CharacterStatisticsSerializer(serializers.Serializer):
    """Serializer for character statistics."""

    total_characters = serializers.IntegerField()
    type_distribution = serializers.DictField()


class CharacterOverviewSerializer(serializers.Serializer):
    """Serializer for character overview response."""

    project_id = serializers.UUIDField()
    characters = CharacterListSerializer(many=True)
    character_statistics = CharacterStatisticsSerializer()
    character_limits = serializers.DictField()
