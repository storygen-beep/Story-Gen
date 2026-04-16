"""
NPC Management serializers for Django REST Framework.

Provides serialization for NPC CRUD operations, role-based management,
and template generation.
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import NPC

User = get_user_model()


class NPCListSerializer(serializers.ModelSerializer):
    """Serializer for NPC list views."""

    project_id = serializers.UUIDField(source="project.id", read_only=True)

    class Meta:
        model = NPC
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
            "categories",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "project_id",
        ]


class NPCDetailSerializer(serializers.ModelSerializer):
    """Serializer for NPC detail views with all fields."""

    project_id = serializers.UUIDField(source="project.id", read_only=True)

    class Meta:
        model = NPC
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
            "ai_behavior_config",
            "relationships",
            "categories",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "project_id",
        ]


class NPCCreateSerializer(serializers.ModelSerializer):
    """Serializer for NPC creation."""

    class Meta:
        model = NPC
        fields = [
            "name",
            "description",
            "age",
            "gender",
            "appearance",
            "core_traits",
            "flag_keys",
            "ai_behavior_config",
            "relationships",
            "categories",
        ]

    def validate_name(self, value):
        """Validate NPC name is not empty."""
        if not value or not value.strip():
            raise serializers.ValidationError("NPC name cannot be empty")
        return value.strip()

    def validate_age(self, value):
        """Validate NPC age range."""
        if value is not None and (value < 1 or value > 200):
            raise serializers.ValidationError("Age must be between 1 and 200")
        return value


class NPCUpdateSerializer(serializers.ModelSerializer):
    """Serializer for NPC updates with partial updates support."""

    class Meta:
        model = NPC
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
            "ai_behavior_config",
            "relationships",
            "categories",
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
        """Validate NPC name is not empty."""
        if value is not None and (not value or not value.strip()):
            raise serializers.ValidationError("NPC name cannot be empty")
        return value.strip() if value else value

    def validate_age(self, value):
        """Validate NPC age range."""
        if value is not None and (value < 1 or value > 200):
            raise serializers.ValidationError("Age must be between 1 and 200")
        return value


class NPCOverviewSerializer(serializers.Serializer):
    """Serializer for NPC overview statistics."""

    npcs = NPCListSerializer(many=True, read_only=True)
    statistics = serializers.DictField(read_only=True)


class NPCScheduleUpdateSerializer(serializers.Serializer):
    """Serializer for NPC AI behavior updates."""

    ai_behavior_config = serializers.JSONField(required=False)

    def validate(self, attrs):
        """Validate that at least one field is provided."""
        if not any(attrs.values()):
            raise serializers.ValidationError(
                "At least one field must be provided for AI behavior update"
            )
        return attrs


class NPCBulkUpdateSerializer(serializers.Serializer):
    """Serializer for bulk NPC operations."""

    npc_ids = serializers.ListField(
        child=serializers.UUIDField(),
        min_length=1,
        help_text="List of NPC IDs to update",
    )
    update_data = NPCUpdateSerializer(help_text="Data to apply to all NPCs")

    def validate_npc_ids(self, value):
        """Validate NPC IDs list."""
        if len(value) > 50:  # Reasonable limit for bulk operations
            raise serializers.ValidationError("Cannot update more than 50 NPCs at once")
        return value


class NPCStatsSerializer(serializers.Serializer):
    """Serializer for NPC statistics."""

    total_npcs = serializers.IntegerField()
    completion_percentage = serializers.FloatField()
    location_distribution = serializers.DictField(required=False)
