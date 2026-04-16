"""
Serializers for story system models.
Handles serialization/deserialization for API requests and responses.
Enhanced with BlockNote content support.
"""

import logging

from rest_framework import serializers

from .models import (
    CanvasTrigger,
    CanvasType,
    NodeConnection,
    StoryCanvas,
    StoryNode,
    TriggerSchedule,
    MediaAsset,
)
from .services.block_conversion import BlockConversionService
from .services.validation import BlockValidationService

logger = logging.getLogger(__name__)


class BlockNoteContentSerializer(serializers.Serializer):
    """Serializer for BlockNote content structure"""

    blocks = serializers.ListField(
        child=serializers.DictField(),
        required=True,
        help_text="Array of BlockNote blocks",
    )
    version = serializers.CharField(
        default="2.0", max_length=10, help_text="Content format version"
    )
    content = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Legacy content for backward compatibility",
    )

    def validate_blocks(self, value):
        """Validate blocks array structure"""
        if not isinstance(value, list):
            raise serializers.ValidationError("Blocks must be an array")

        # Use our validation service to validate blocks
        validation_result = BlockValidationService._validate_node_content(
            {"blocks": value, "version": self.initial_data.get("version", "2.0")}
        )

        if not validation_result.is_valid:
            error_messages = BlockValidationService.format_validation_errors(
                validation_result
            )
            raise serializers.ValidationError(error_messages)

        return value

    def validate_version(self, value):
        """Validate version format"""
        if value not in ["2.0"]:
            raise serializers.ValidationError(f"Unsupported version: {value}")
        return value


class StoryCanvasSerializer(serializers.ModelSerializer):
    """Serializer for StoryCanvas model"""

    # Add field to identify if this is the starting canvas for the project
    is_starting_canvas = serializers.SerializerMethodField()

    class Meta:
        model = StoryCanvas
        fields = [
            "id",
            "project",
            "name",
            "description",
            "canvas_type",
            "status",
            "metadata",
            "tags",
            "version",
            "node_count",
            "connection_count",
            "estimated_play_time",
            "is_valid",
            "validation_errors",
            "last_validated_at",
            "is_favorite",
            "display_order",
            "is_starting_canvas",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "node_count",
            "connection_count",
            "is_valid",
            "validation_errors",
            "last_validated_at",
            "is_starting_canvas",
            "created_at",
            "updated_at",
        ]

    def get_is_starting_canvas(self, obj):
        """Check if this canvas is the starting canvas for its project."""
        return (
            obj.project.starting_canvas_id == obj.id
            if obj.project.starting_canvas
            else False
        )

    def to_representation(self, instance):
        """Custom representation matching frontend expectations"""
        data = super().to_representation(instance)
        # Convert UUIDs to strings for JSON serialization
        data["id"] = str(instance.id)
        data["project_id"] = str(instance.project_id)
        # No additional field conversions needed
        return data


class StoryCanvasCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new story canvases"""

    # Make canvas_type optional since model has default
    canvas_type = serializers.ChoiceField(choices=CanvasType.choices, required=False)

    class Meta:
        model = StoryCanvas
        fields = [
            "name",
            "description",
            "canvas_type",
            "metadata",
            "estimated_play_time",
        ]


class StoryCanvasUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating existing story canvases"""

    # Make canvas_type optional for consistency
    canvas_type = serializers.ChoiceField(choices=CanvasType.choices, required=False)

    class Meta:
        model = StoryCanvas
        fields = [
            "name",
            "description",
            "canvas_type",
            "metadata",
            "estimated_play_time",
            "display_order",
        ]


class StoryNodeSerializer(serializers.ModelSerializer):
    """Serializer for StoryNode model - enhanced with BlockNote support"""

    # Add computed fields for content statistics
    content_stats = serializers.SerializerMethodField()
    preview_text = serializers.SerializerMethodField()

    class Meta:
        model = StoryNode
        fields = [
            "id",
            "canvas",
            "name",
            "node_data",
            "exit_block",
            "tags",
            "position_x",
            "position_y",
            "width",
            "height",
            "content_stats",
            "preview_text",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "content_stats",
            "preview_text",
            "created_at",
            "updated_at",
        ]

    def get_content_stats(self, obj):
        """Get content statistics for the node"""
        try:
            node_data = obj.node_data or {}
            if "blocks" in node_data:
                return BlockConversionService.get_content_stats(node_data["blocks"])
            else:
                # Legacy content
                legacy_content = node_data.get("content", "")
                return {
                    "heading_count": 0,
                    "paragraph_count": 1 if legacy_content else 0,
                    "total_blocks": 1 if legacy_content else 0,
                    "total_words": len(legacy_content.split()) if legacy_content else 0,
                    "is_empty": not legacy_content,
                }
        except Exception as e:
            logger.error(f"Error calculating content stats: {e}")
            return {
                "heading_count": 0,
                "paragraph_count": 0,
                "total_blocks": 0,
                "total_words": 0,
                "is_empty": True,
            }

    def get_preview_text(self, obj):
        """Get preview text for the node"""
        try:
            node_data = obj.node_data or {}
            if "blocks" in node_data:
                return BlockConversionService.get_preview_text(node_data["blocks"])
            else:
                # Legacy content
                legacy_content = str(node_data.get("content", ""))
                return (
                    legacy_content[:100] + "..."
                    if len(legacy_content) > 100
                    else legacy_content
                )
        except Exception as e:
            logger.error(f"Error generating preview text: {e}")
            return ""

    def to_representation(self, instance):
        """Custom representation with block-aware content handling"""
        data = super().to_representation(instance)
        data["id"] = str(instance.id)
        data["canvas_id"] = str(instance.canvas_id)

        # Ensure node_data is properly migrated to block format
        node_data = instance.node_data or {}

        # Migrate to block format if needed
        migrated_data = BlockConversionService.migrate_node_data(node_data)
        data["node_data"] = migrated_data

        return data


class StoryNodeCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new story nodes - enhanced with block validation"""

    class Meta:
        model = StoryNode
        fields = [
            "name",
            "node_data",
            "exit_block",
            "tags",
            "position_x",
            "position_y",
            "width",
            "height",
        ]
        extra_kwargs = {
            "width": {"default": 400},
            "height": {"default": 566},
            "node_data": {"default": dict},
            "tags": {"default": list},
        }

    def validate(self, attrs):
        """Validate complete node data including BlockNote content"""
        # Use our comprehensive validation service
        validation_result = BlockValidationService.validate_story_node(attrs)

        if not validation_result.is_valid:
            error_messages = BlockValidationService.format_validation_errors(
                validation_result
            )
            raise serializers.ValidationError({"validation_errors": error_messages})

        # Log warnings if any
        if validation_result.warnings:
            warning_messages = BlockValidationService.format_validation_warnings(
                validation_result
            )
            logger.warning(f"Node creation warnings: {warning_messages}")

        return attrs

    def validate_exit_block(self, value):
        """Validate exit_block structure supporting 'location' and 'choices' types"""
        if value is None:
            # Use default if not provided
            from apps.stories.models import get_default_exit_block

            value = get_default_exit_block()

        if not isinstance(value, dict):
            raise serializers.ValidationError("Exit block must be a dictionary")

        # Common required fields
        if "type" not in value:
            raise serializers.ValidationError("Exit block missing required field: type")

        exit_type = value.get("type")
        if exit_type not in ["location", "choices"]:
            raise serializers.ValidationError(
                "Exit block type must be 'location' or 'choices'"
            )

        if exit_type == "location":
            # Required fields for location type
            for field in ["text", "config"]:
                if field not in value:
                    raise serializers.ValidationError(
                        f"Exit block missing required field: {field}"
                    )
            config = value.get("config", {})
            if "destinationType" not in config:
                raise serializers.ValidationError(
                    "Location exit block config missing destinationType"
                )
            if config["destinationType"] not in ["trigger", "specific"]:
                raise serializers.ValidationError(
                    "destinationType must be 'trigger' or 'specific'"
                )
            if config["destinationType"] == "specific" and "locationId" not in config:
                raise serializers.ValidationError(
                    "Specific destination requires locationId"
                )
            # Validate time progression if provided
            if "time_progression_minutes" in config:
                time_minutes = config["time_progression_minutes"]
                if (
                    not isinstance(time_minutes, (int, float))
                    or time_minutes < 0
                    or time_minutes > 1440
                ):
                    raise serializers.ValidationError(
                        "time_progression_minutes must be a number between 0 and 1440"
                    )

        if exit_type == "choices":
            # For choices, require an array of choices (can be empty, but better to validate each if present)
            choices = value.get("choices", [])
            if not isinstance(choices, list):
                raise serializers.ValidationError("choices must be a list")

            # Optional config with default_time_progression
            config = value.get("config", {}) or {}
            if "default_time_progression" in config:
                default_tp = config["default_time_progression"]
                if (
                    not isinstance(default_tp, (int, float))
                    or default_tp < 0
                    or default_tp > 1440
                ):
                    raise serializers.ValidationError(
                        "default_time_progression must be a number between 0 and 1440"
                    )

            for idx, choice in enumerate(choices):
                if not isinstance(choice, dict):
                    raise serializers.ValidationError(
                        f"Choice at index {idx} must be an object"
                    )
                text = choice.get("text", "")
                if not isinstance(text, str) or not text.strip():
                    raise serializers.ValidationError(
                        f"Choice at index {idx} requires non-empty text"
                    )
                target_type = choice.get("targetType")
                if target_type not in ["location", "node", "trigger"]:
                    raise serializers.ValidationError(
                        f"Choice at index {idx} has invalid targetType"
                    )
                if target_type == "location" and not choice.get("locationId"):
                    raise serializers.ValidationError(
                        f"Choice at index {idx} requires locationId for targetType 'location'"
                    )
                if target_type == "node" and not choice.get("nodeId"):
                    raise serializers.ValidationError(
                        f"Choice at index {idx} requires nodeId for targetType 'node'"
                    )
                if "time_progression_minutes" in choice:
                    tp = choice["time_progression_minutes"]
                    if not isinstance(tp, (int, float)) or tp < 0 or tp > 1440:
                        raise serializers.ValidationError(
                            f"Choice at index {idx} has invalid time_progression_minutes (0-1440)"
                        )

                # Optional: validate per-choice conditions using the same v1.0 schema as triggers
                conditions = choice.get("conditions")
                if conditions is not None:
                    if not isinstance(conditions, dict):
                        raise serializers.ValidationError(
                            f"Choice at index {idx} conditions must be an object if provided"
                        )
                    # Resolve project from serializer context (preferred) to validate NPC ownership
                    from .services.conditions import validate_conditions_schema
                    project = self.context.get("project") if hasattr(self, "context") else None
                    try:
                        if project is not None:
                            cleaned = validate_conditions_schema(conditions, project)
                            # Replace with cleaned version to normalize
                            choice["conditions"] = cleaned
                        else:
                            # If project context is missing, allow structural shape (defer full validation)
                            pass
                    except Exception as e:
                        raise serializers.ValidationError(
                            {"choices": {idx: {"conditions": str(e)}}}
                        )

        return value

    def validate_node_data(self, value):
        """Validate and migrate node_data structure"""
        if value is None:
            value = {}

        # Always migrate to block format
        migrated_data = BlockConversionService.migrate_node_data(value)
        return migrated_data


class StoryNodeUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating existing story nodes - enhanced with block validation"""

    class Meta:
        model = StoryNode
        fields = [
            "name",
            "node_data",
            "exit_block",
            "tags",
            "position_x",
            "position_y",
            "width",
            "height",
        ]

    def validate(self, attrs):
        """Validate node updates; merge with instance for required fields.

        Ensures partial updates (e.g., only exit_block) don't fail name/node_data checks
        by validating a merged view of instance + attrs.
        """
        if attrs:
            # Merge with instance so required fields are present during validation
            base = {
                "name": getattr(self.instance, "name", None),
                "node_data": getattr(self.instance, "node_data", {}),
                "tags": getattr(self.instance, "tags", []),
            }
            merged = {**base, **attrs}

            validation_result = BlockValidationService.validate_story_node(merged)

            if not validation_result.is_valid:
                error_messages = BlockValidationService.format_validation_errors(
                    validation_result
                )
                raise serializers.ValidationError({"validation_errors": error_messages})

            if validation_result.warnings:
                warning_messages = BlockValidationService.format_validation_warnings(
                    validation_result
                )
                logger.warning(f"Node update warnings: {warning_messages}")

        return attrs

    def validate_node_data(self, value):
        """Validate and migrate node_data structure"""
        if value is not None:
            # Always migrate to block format
            migrated_data = BlockConversionService.migrate_node_data(value)
            return migrated_data
        return value

    def validate_exit_block(self, value):
        """Reuse create serializer validation for updates"""
        # Propagate context so project is available for conditions validation
        return StoryNodeCreateSerializer(instance=self.instance, context=getattr(self, 'context', {})).validate_exit_block(value)


class StoryNodeUpsertSerializer(serializers.ModelSerializer):
    """Serializer for upsert operations (create or update) - enhanced with block validation"""

    id = serializers.UUIDField(
        required=False, help_text="Optional ID for update operations"
    )

    class Meta:
        model = StoryNode
        fields = [
            "id",
            "name",
            "node_data",
            "exit_block",
            "tags",
            "position_x",
            "position_y",
            "width",
            "height",
        ]
        extra_kwargs = {
            "width": {"default": 400},
            "height": {"default": 566},
            "node_data": {"default": dict},
            "tags": {"default": list},
        }

    def validate(self, attrs):
        """Validate complete node data including BlockNote content"""
        # Use our comprehensive validation service
        validation_result = BlockValidationService.validate_story_node(attrs)

        if not validation_result.is_valid:
            error_messages = BlockValidationService.format_validation_errors(
                validation_result
            )
            raise serializers.ValidationError({"validation_errors": error_messages})

        # Log warnings if any
        if validation_result.warnings:
            warning_messages = BlockValidationService.format_validation_warnings(
                validation_result
            )
            logger.warning(f"Node upsert warnings: {warning_messages}")

        return attrs

    def validate_node_data(self, value):
        """Validate and migrate node_data structure"""
        if value is None:
            value = {}

        # Always migrate to block format
        migrated_data = BlockConversionService.migrate_node_data(value)
        return migrated_data

    def validate_exit_block(self, value):
        """Validate exit_block using same rules as create/update"""
        # Propagate context so project is available for conditions validation
        return StoryNodeCreateSerializer(context=getattr(self, 'context', {})).validate_exit_block(value)


class NodeConnectionSerializer(serializers.ModelSerializer):
    """Serializer for NodeConnection model"""

    class Meta:
        model = NodeConnection
        fields = [
            "id",
            "canvas",
            "source_node",
            "target_node",
            "connection_type",
            "label",
            "conditions",
            "effects",
            "metadata",
            "path_data",
            "style",
            "priority",
            "weight",
            "is_bidirectional",
            "is_valid",
            "validation_errors",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "is_valid",
            "validation_errors",
            "created_at",
            "updated_at",
        ]

    def to_representation(self, instance):
        """Custom representation matching frontend expectations"""
        data = super().to_representation(instance)
        data["id"] = str(instance.id)
        data["canvas_id"] = str(instance.canvas_id)
        data["source_node_id"] = str(instance.source_node_id)
        data["target_node_id"] = str(instance.target_node_id)
        return data


class NodeConnectionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new node connections"""

    class Meta:
        model = NodeConnection
        fields = [
            "source_node",
            "target_node",
            "connection_type",
            "label",
            "conditions",
            "effects",
            "metadata",
            "path_data",
            "style",
            "priority",
            "weight",
            "is_bidirectional",
        ]


class NodeConnectionUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating existing node connections"""

    class Meta:
        model = NodeConnection
        fields = [
            "connection_type",
            "label",
            "conditions",
            "effects",
            "metadata",
            "path_data",
            "style",
            "priority",
            "weight",
            "is_bidirectional",
        ]


class NodeConnectionUpsertSerializer(serializers.ModelSerializer):
    """Serializer for upsert operations (create or update) for node connections"""

    id = serializers.UUIDField(
        required=False, help_text="Optional ID for update operations"
    )

    class Meta:
        model = NodeConnection
        fields = [
            "id",
            "source_node",
            "target_node",
            "connection_type",
            "label",
            "conditions",
            "effects",
            "metadata",
            "path_data",
            "style",
            "priority",
            "weight",
            "is_bidirectional",
        ]


## StoryFlag serializers removed


class CanvasTriggerSerializer(serializers.ModelSerializer):
    """Serializer for CanvasTrigger model"""

    class Meta:
        model = CanvasTrigger
        fields = [
            "id",
            "canvas",
            "location_id",
            "conditions",
            "is_active",
            "max_triggers_per_day",
            "metadata",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def to_representation(self, instance):
        """Custom representation matching frontend expectations"""
        data = super().to_representation(instance)
        data["id"] = str(instance.id)
        data["canvas_id"] = str(instance.canvas_id)
        if instance.location_id:
            data["location_id"] = str(instance.location_id)
        # No additional field conversions needed
        return data


class CanvasTriggerCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new canvas triggers"""

    # Allow explicit null from clients, we will coerce to empty object in validation
    conditions = serializers.JSONField(required=False, allow_null=True)

    def validate_conditions(self, value):
        """Validate trigger conditions against v1.0 schema or coerce empty."""
        # Treat null/empty as clearing conditions
        if value is None or (isinstance(value, dict) and len(value) == 0):
            return {}
        from .services.conditions import validate_conditions_schema

        request = self.context.get("request")
        project = None
        if request and hasattr(request, "parser_context"):
            project = request.parser_context.get("kwargs", {}).get("project_id")
        # Fallback: project from canvas in view is enforced; validation re-fetches project instance below
        from apps.projects.models import Project

        try:
            project_obj = Project.objects.get(id=project) if project else None
        except Exception:
            project_obj = None
        if not project_obj:
            # Attempt to infer from 'canvas' on instance/context if available later in view
            pass
        # When project is not resolved here, schema validation that depends on project ownership may be deferred;
        # however, we still run structural validation and raise if invalid shapes/operators.
        if project_obj:
            return validate_conditions_schema(value, project_obj)
        # Structural validation without project resolution
        return value

    class Meta:
        model = CanvasTrigger
        fields = [
            "location_id",
            "conditions",
            "is_active",
            "is_repeatable",
            "max_triggers_per_day",
            "metadata",
        ]


class CanvasTriggerUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating existing canvas triggers"""

    # Allow explicit null from clients, we will coerce to empty object in validation
    conditions = serializers.JSONField(required=False, allow_null=True)

    def validate_conditions(self, value):
        # Treat null/empty as clearing conditions
        if value is None or (isinstance(value, dict) and len(value) == 0):
            return {}
        from .services.conditions import validate_conditions_schema

        # Try to resolve project from the instance's canvas
        project_obj = None
        try:
            project_obj = self.instance.canvas.project  # type: ignore[attr-defined]
        except Exception:
            project_obj = None
        if project_obj:
            return validate_conditions_schema(value, project_obj)
        return value

    class Meta:
        model = CanvasTrigger
        fields = [
            "location_id",
            "conditions",
            "is_active",
            "is_repeatable",
            "max_triggers_per_day",
            "metadata",
        ]


class StoryCanvasDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer with nested relationships (flags removed)"""

    nodes = StoryNodeSerializer(many=True, read_only=True)
    connections = NodeConnectionSerializer(many=True, read_only=True)
    trigger = CanvasTriggerSerializer(read_only=True)

    class Meta:
        model = StoryCanvas
        fields = [
            "id",
            "project",
            "name",
            "description",
            "canvas_type",
            "status",
            "metadata",
            "tags",
            "version",
            "node_count",
            "connection_count",
            "estimated_play_time",
            "is_valid",
            "validation_errors",
            "last_validated_at",
            "is_favorite",
            "display_order",
            "created_at",
            "updated_at",
            "nodes",
            "connections",
            "trigger",
        ]
        read_only_fields = [
            "id",
            "node_count",
            "connection_count",
            "is_valid",
            "validation_errors",
            "last_validated_at",
            "created_at",
            "updated_at",
            "nodes",
            "connections",
            "flags",
            "trigger",
        ]

    def to_representation(self, instance):
        """Custom representation with nested data"""
        data = super().to_representation(instance)
        data["id"] = str(instance.id)
        data["project_id"] = str(instance.project_id)
        # No additional field conversions needed
        return data


# Template serializers for canvas templates endpoint
class CanvasTemplateSerializer(serializers.Serializer):
    """Serializer for canvas templates"""

    id = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField()
    canvas_type = serializers.ChoiceField(choices=CanvasType.choices)
    node_count = serializers.IntegerField()
    estimated_setup_time = serializers.IntegerField()
    difficulty_level = serializers.CharField()
    tags = serializers.ListField(child=serializers.CharField())
    preview_image = serializers.CharField(required=False)


# Response serializers for API responses
class CanvasOverviewSerializer(serializers.Serializer):
    """Serializer for canvas overview response"""

    canvases = StoryCanvasSerializer(many=True)
    pagination = serializers.DictField()
    available_statuses = serializers.ListField(child=serializers.CharField())
    canvas_limits = serializers.DictField()


class ValidationResultSerializer(serializers.Serializer):
    """Serializer for validation results"""

    is_valid = serializers.BooleanField()
    error_count = serializers.IntegerField()
    warning_count = serializers.IntegerField()
    errors = serializers.ListField(child=serializers.DictField())
    warnings = serializers.ListField(child=serializers.DictField())
    validation_timestamp = serializers.DateTimeField()


class BlockValidationResultSerializer(serializers.Serializer):
    """Serializer for BlockNote validation results"""

    is_valid = serializers.BooleanField()
    errors = serializers.ListField(child=serializers.CharField(), required=False)
    warnings = serializers.ListField(child=serializers.CharField(), required=False)


class ContentConversionSerializer(serializers.Serializer):
    """Serializer for content conversion requests and responses"""

    legacy_content = serializers.CharField(
        required=True,
        allow_blank=True,
        help_text="Legacy text content to convert to blocks",
    )

    def validate_legacy_content(self, value):
        """Validate legacy content input"""
        if value is None:
            return ""
        return str(value)


class ContentConversionResponseSerializer(serializers.Serializer):
    """Serializer for content conversion response"""

    success = serializers.BooleanField()
    blocks = serializers.ListField(child=serializers.DictField())
    version = serializers.CharField()
    content_stats = serializers.DictField()
    preview_text = serializers.CharField()
    warnings = serializers.ListField(child=serializers.CharField(), required=False)


# Story Save Serializers
class SaveStoryMetadataSerializer(serializers.Serializer):
    """Serializer for save metadata"""

    version = serializers.CharField(
        default="1.0", max_length=10, help_text="Save format version"
    )
    client_timestamp = serializers.DateTimeField(
        required=False, help_text="Client-side timestamp of save operation"
    )


class SaveStorySerializer(serializers.Serializer):
    """Serializer for bulk story content save operations"""

    nodes = serializers.ListField(
        child=StoryNodeUpsertSerializer(),
        required=False,
        allow_empty=True,
        help_text="Complete list of nodes to save",
    )
    connections = serializers.ListField(
        child=NodeConnectionUpsertSerializer(),
        required=False,
        allow_empty=True,
        help_text="Complete list of connections to save",
    )
    save_metadata = SaveStoryMetadataSerializer(
        required=False, help_text="Metadata about the save operation"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure nested child serializers receive the same context (for project-aware validation)
        try:
            if 'nodes' in self.fields and hasattr(self.fields['nodes'], 'child'):
                self.fields['nodes'].child.context = self.context
            if 'connections' in self.fields and hasattr(self.fields['connections'], 'child'):
                self.fields['connections'].child.context = self.context
        except Exception:
            # Best-effort; if fields inaccessible, skip
            pass

    def validate(self, attrs):
        """Validate the complete story state"""
        # Ensure we have at least some content to save
        has_content = any(
            [attrs.get("nodes"), attrs.get("connections"), attrs.get("flags")]
        )

        if not has_content:
            raise serializers.ValidationError(
                "At least one of nodes, connections, or flags must be provided"
            )

        return attrs


class SaveStoryResponseSerializer(serializers.Serializer):
    """Serializer for save story response"""

    success = serializers.BooleanField()
    message = serializers.CharField()
    saved_counts = serializers.DictField(help_text="Count of items saved by type")
    errors = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="Any non-fatal errors during save",
    )
    save_timestamp = serializers.DateTimeField()


class TriggerScheduleSerializer(serializers.ModelSerializer):
    """Serializer for trigger schedule creation and updates"""

    # Custom field to handle time formatting
    start_time = serializers.TimeField(format="%H:%M", input_formats=["%H:%M"])
    end_time = serializers.TimeField(
        format="%H:%M", input_formats=["%H:%M"], required=False, allow_null=True
    )

    # Read-only fields for API responses
    trigger_name = serializers.CharField(source="trigger.canvas.name", read_only=True)

    class Meta:
        model = TriggerSchedule
        fields = [
            "id",
            "trigger",
            "trigger_name",
            "name",
            "weekdays",
            "start_time",
            "end_time",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_weekdays(self, value):
        """Validate weekdays list"""
        if not isinstance(value, list) or not value:
            raise serializers.ValidationError("weekdays must be a non-empty list")

        if not all(isinstance(day, int) and 0 <= day <= 6 for day in value):
            raise serializers.ValidationError(
                "weekdays must contain integers between 0-6 (0=Monday, 6=Sunday)"
            )

        # Remove duplicates and sort
        return sorted(list(set(value)))

    def validate(self, attrs):
        """Cross-field validation"""
        start_time = attrs.get("start_time")
        end_time = attrs.get("end_time")

        # Validate time range
        if end_time is not None and start_time and end_time <= start_time:
            raise serializers.ValidationError(
                {"end_time": "end_time must be after start_time"}
            )

        return attrs

    def to_representation(self, instance):
        """Custom representation with additional data"""
        representation = super().to_representation(instance)

        # Add weekday names for easier frontend handling
        weekday_names = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        representation["weekday_names"] = [
            weekday_names[day] for day in instance.weekdays
        ]

        # Add trigger activity info
        representation["is_activity"] = instance.trigger.is_activity
        representation["is_repeatable"] = instance.trigger.is_repeatable

        return representation


class TriggerScheduleCreateSerializer(serializers.Serializer):
    """Serializer for creating multiple schedules for a trigger"""

    trigger_id = serializers.UUIDField()
    schedules = serializers.ListField(
        child=serializers.DictField(),
        min_length=1,
        help_text="List of schedules to create for the trigger",
    )

    def validate_trigger_id(self, value):
        """Validate that trigger exists"""
        try:
            trigger = CanvasTrigger.objects.get(id=value)
            return value
        except CanvasTrigger.DoesNotExist:
            raise serializers.ValidationError("Trigger not found")

    def validate_schedules(self, value):
        """Validate each schedule in the list"""
        validated_schedules = []

        for i, schedule_data in enumerate(value):
            try:
                # Use the service to validate each schedule
                from .services.scheduling import TriggerScheduleService

                validated_schedule = TriggerScheduleService.validate_schedule_data(
                    schedule_data
                )
                validated_schedules.append(validated_schedule)
            except ValidationError as e:
                raise serializers.ValidationError(f"Schedule {i+1}: {e.message}")

        return validated_schedules

    def create(self, validated_data):
        """Create multiple schedules for a trigger"""
        from .services.scheduling import TriggerScheduleService

        trigger_id = validated_data["trigger_id"]
        schedules_data = validated_data["schedules"]

        created_schedules = TriggerScheduleService.create_multiple_schedules(
            trigger_id, schedules_data
        )

        return {"trigger_id": trigger_id, "schedules": created_schedules}


class TriggerSchedulePreviewSerializer(serializers.Serializer):
    """Serializer for schedule preview responses"""

    date = serializers.DateField()
    weekday = serializers.IntegerField()
    weekday_name = serializers.CharField()
    start_time = serializers.CharField()
    end_time = serializers.CharField(allow_null=True)
    trigger_datetime = serializers.DateTimeField()


class TriggerScheduleConflictSerializer(serializers.Serializer):
    """Serializer for schedule conflict information"""

    schedule_id = serializers.UUIDField()
    schedule_name = serializers.CharField()
    conflicting_schedule_id = serializers.UUIDField()
    conflicting_schedule_name = serializers.CharField()
    conflicting_trigger_name = serializers.CharField()
    weekdays = serializers.ListField(child=serializers.IntegerField())
    time_overlap = serializers.CharField()


class ActiveTriggersSerializer(serializers.Serializer):
    """Serializer for active triggers response"""

    current_weekday = serializers.IntegerField()
    current_time = serializers.TimeField(format="%H:%M")
    active_triggers = serializers.ListField(
        child=serializers.DictField(), help_text="List of active trigger information"
    )


class MediaAssetSerializer(serializers.ModelSerializer):
    """Serializer for MediaAsset list/response."""

    url = serializers.SerializerMethodField()
    poster_url = serializers.SerializerMethodField()

    class Meta:
        model = MediaAsset
        fields = [
            "id",
            "project",
            "kind",
            "mime_type",
            "size_bytes",
            "width",
            "height",
            "duration_sec",
            "url",
            "poster_url",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "url",
            "poster_url",
            "created_at",
        ]

    def get_url(self, obj):
        return obj.url

    def get_poster_url(self, obj):
        return obj.poster_url


class MediaUploadResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    kind = serializers.ChoiceField(choices=["image", "video", "gif"])
    url = serializers.URLField()
    mime_type = serializers.CharField()
    size_bytes = serializers.IntegerField()
    width = serializers.IntegerField(required=False, allow_null=True)
    height = serializers.IntegerField(required=False, allow_null=True)
    duration_sec = serializers.FloatField(required=False, allow_null=True)
    poster_url = serializers.URLField(required=False, allow_null=True)
    created_at = serializers.DateTimeField()
