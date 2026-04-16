"""
Project serializers for API endpoints.

Provides serializers that match the exact frontend interface expectations.
"""

from rest_framework import serializers

from .models import Project, ProjectComplexity


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for Project model read operations.

    Returns data in the exact format expected by the frontend.
    """

    # Frontend expects 'user_id' instead of 'owner'
    user_id = serializers.SerializerMethodField()
    starting_canvas_id = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "summary",
            "complexity",
            "genre",
            "theme",
            "world_size",
            "settings",
            "metadata",
            "user_id",
            "starting_canvas_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "user_id",
            "starting_canvas_id",
        ]

    def get_user_id(self, obj):
        """Return owner ID as user_id to match frontend expectations."""
        return str(obj.owner.id)

    def get_starting_canvas_id(self, obj):
        """Return starting canvas ID or None."""
        return str(obj.starting_canvas.id) if obj.starting_canvas else None

    def to_representation(self, instance):
        """
        Custom representation to ensure exact format match with frontend.
        """
        data = super().to_representation(instance)

        # Ensure UUIDs are strings
        data["id"] = str(instance.id)
        data["user_id"] = str(instance.owner.id)
        data["starting_canvas_id"] = (
            str(instance.starting_canvas.id) if instance.starting_canvas else None
        )

        # Format timestamps as ISO strings
        if instance.created_at:
            data["created_at"] = instance.created_at.isoformat()
        if instance.updated_at:
            data["updated_at"] = instance.updated_at.isoformat()

        # Ensure null values for optional fields
        for field in ["genre", "theme"]:
            if data.get(field) == "":
                data[field] = None

        return data


class ProjectCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for Project creation.

    Handles the data transformation from frontend format.
    """

    class Meta:
        model = Project
        fields = [
            "name",
            "description",
            "summary",
            "complexity",
            "genre",
            "theme",
            "world_size",
            "settings",
            "metadata",
        ]

    def validate_name(self, value):
        """Validate project name."""
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "Project name must be at least 3 characters long."
            )
        return value.strip()

    def validate_complexity(self, value):
        """Validate complexity is a valid choice."""
        if value not in [choice[0] for choice in ProjectComplexity.choices]:
            raise serializers.ValidationError(
                f"Invalid complexity. Must be one of: {[choice[0] for choice in ProjectComplexity.choices]}"
            )
        return value

    def create(self, validated_data):
        """
        Create project with the authenticated user as owner.
        Also creates a default starting canvas.
        """
        # Get the authenticated user from the request context
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError(
                "Authentication required to create project."
            )

        # Set the owner
        validated_data["owner"] = request.user

        # Create the project
        project = Project.objects.create(**validated_data)

        # Create default starting canvas
        try:
            # Import here to avoid circular imports
            from apps.stories.legacy_services import StoryCanvasService

            StoryCanvasService.create_default_starting_canvas(
                project=project
            )
        except Exception as e:
            # Log error but don't fail project creation
            # The starting canvas can be created manually later
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(
                f"Failed to create default starting canvas for project {project.id}: {str(e)}"
            )

        return project


class ProjectUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for Project updates.

    Allows partial updates of project fields.
    """

    class Meta:
        model = Project
        fields = [
            "name",
            "description",
            "summary",
            "complexity",
            "genre",
            "theme",
            "world_size",
            "settings",
            "metadata",
        ]
        extra_kwargs = {
            # All fields are optional for updates
            "name": {"required": False},
            "description": {"required": False},
            "summary": {"required": False},
            "complexity": {"required": False},
            "genre": {"required": False},
            "theme": {"required": False},
            "world_size": {"required": False},
            "settings": {"required": False},
            "metadata": {"required": False},
        }

    def validate_name(self, value):
        """Validate project name if provided."""
        if value and len(value.strip()) < 3:
            raise serializers.ValidationError(
                "Project name must be at least 3 characters long."
            )
        return value.strip() if value else value

    def validate_complexity(self, value):
        """Validate complexity if provided."""
        if value and value not in [choice[0] for choice in ProjectComplexity.choices]:
            raise serializers.ValidationError(
                f"Invalid complexity. Must be one of: {[choice[0] for choice in ProjectComplexity.choices]}"
            )
        return value

    def validate_starting_canvas_id(self, value):
        """Validate starting canvas ID if provided."""
        if value is None:
            return value

        # Get the project instance from the context
        project = self.instance
        if not project:
            raise serializers.ValidationError(
                "Project instance required for canvas validation."
            )

        # Import here to avoid circular imports
        from apps.stories.models import StoryCanvas

        try:
            canvas = StoryCanvas.objects.get(
                id=value, project=project, deleted_at__isnull=True
            )
            return value
        except StoryCanvas.DoesNotExist:
            raise serializers.ValidationError(
                "Canvas does not exist or does not belong to this project."
            )


class ProjectListSerializer(serializers.Serializer):
    """
    Serializer for project list responses with pagination.

    Matches the format expected by frontend ProjectService.getProjects().
    """

    projects = ProjectSerializer(many=True)
    total = serializers.IntegerField()
    page = serializers.IntegerField(default=1)
    per_page = serializers.IntegerField(default=50)

    def to_representation(self, instance):
        """
        Format the response to match frontend expectations.
        """
        return {
            "projects": instance.get("projects", []),
            "total": instance.get("total", 0),
            "page": instance.get("page", 1),
            "per_page": instance.get("per_page", 50),
        }


class ProjectSettingsSerializer(serializers.Serializer):
    """
    Serializer for project settings endpoint.

    Handles the Settings Tab data structure matching FastAPI backend.
    """

    # Basic project fields
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(allow_blank=True, required=False)
    genre = serializers.CharField(max_length=100, allow_blank=True, required=False)
    theme = serializers.CharField(max_length=100, allow_blank=True, required=False)
    complexity = serializers.ChoiceField(choices=ProjectComplexity.choices)
    world_size = serializers.ChoiceField(choices=["small", "medium", "large"])

    # Settings fields (stored in settings JSON)
    max_locations = serializers.IntegerField(min_value=1, max_value=500)
    max_characters = serializers.IntegerField(min_value=1, max_value=100)
    max_experiences = serializers.IntegerField(min_value=1, max_value=1000)
    autonomous_enabled = serializers.BooleanField()
    time_events_enabled = serializers.BooleanField()
    resource_management_enabled = serializers.BooleanField()
    discovery_generation_enabled = serializers.BooleanField()

    # Full settings and metadata
    settings = serializers.JSONField(read_only=True)
    metadata = serializers.JSONField(read_only=True)

    # Starting canvas info
    starting_canvas_id = serializers.SerializerMethodField()

    def get_starting_canvas_id(self, obj):
        """Return starting canvas ID or None."""
        return str(obj.starting_canvas.id) if obj.starting_canvas else None

    def to_representation(self, instance):
        """Convert Project instance to settings response."""
        settings = instance.settings or {}

        # Get available canvases for dropdown
        from apps.stories.legacy_services import StoryCanvasService

        available_canvases = StoryCanvasService.get_project_canvases_for_settings(
            instance
        )

        return {
            "id": str(instance.id),
            "name": instance.name,
            "description": instance.description or "",
            "genre": instance.genre or "",
            "theme": instance.theme or "",
            "complexity": instance.complexity,
            "world_size": instance.world_size,
            "max_locations": settings.get("max_locations", 50),
            "max_characters": settings.get("max_characters", 20),
            "max_experiences": settings.get("max_experiences", 100),
            "autonomous_enabled": settings.get("autonomous_enabled", False),
            "time_events_enabled": settings.get("time_events_enabled", False),
            "resource_management_enabled": settings.get(
                "resource_management_enabled", False
            ),
            "discovery_generation_enabled": settings.get(
                "discovery_generation_enabled", False
            ),
            "starting_canvas_id": str(instance.starting_canvas.id)
            if instance.starting_canvas
            else None,
            "available_canvases": available_canvases,
            "story_config": {
                "total_canvases": len(available_canvases),
                "has_starting_canvas": instance.starting_canvas is not None,
                "starting_canvas_name": instance.starting_canvas.name
                if instance.starting_canvas
                else None,
            },
            "settings": settings,
            "metadata": instance.metadata or {},
        }


class ProjectSettingsUpdateSerializer(serializers.Serializer):
    """
    Serializer for updating project settings.

    All fields are optional for partial updates.
    """

    name = serializers.CharField(max_length=255, required=False)
    description = serializers.CharField(allow_blank=True, required=False)
    genre = serializers.CharField(max_length=100, allow_blank=True, required=False)
    theme = serializers.CharField(max_length=100, allow_blank=True, required=False)
    complexity = serializers.ChoiceField(
        choices=ProjectComplexity.choices, required=False
    )
    world_size = serializers.ChoiceField(
        choices=["small", "medium", "large"], required=False
    )
    max_locations = serializers.IntegerField(min_value=1, max_value=500, required=False)
    max_characters = serializers.IntegerField(
        min_value=1, max_value=100, required=False
    )
    max_experiences = serializers.IntegerField(
        min_value=1, max_value=1000, required=False
    )
    autonomous_enabled = serializers.BooleanField(required=False)
    time_events_enabled = serializers.BooleanField(required=False)
    resource_management_enabled = serializers.BooleanField(required=False)
    discovery_generation_enabled = serializers.BooleanField(required=False)
    starting_canvas_id = serializers.UUIDField(required=False, allow_null=True)

    def validate_name(self, value):
        """Validate project name if provided."""
        if value and len(value.strip()) < 3:
            raise serializers.ValidationError(
                "Project name must be at least 3 characters long."
            )
        return value.strip() if value else value

    def validate_starting_canvas_id(self, value):
        """Validate starting canvas ID if provided."""
        if value is None:
            return value

        # Get the project instance from the context
        project = self.instance
        if not project:
            raise serializers.ValidationError(
                "Project instance required for canvas validation."
            )

        # Import here to avoid circular imports
        from apps.stories.models import StoryCanvas

        try:
            canvas = StoryCanvas.objects.get(
                id=value, project=project, deleted_at__isnull=True
            )
            return value
        except StoryCanvas.DoesNotExist:
            raise serializers.ValidationError(
                "Canvas does not exist or does not belong to this project."
            )

    def update(self, instance, validated_data):
        """Update project and settings fields."""
        # Fields that go directly on the project model
        direct_fields = [
            "name",
            "description",
            "genre",
            "theme",
            "complexity",
            "world_size",
        ]

        # Fields that go in the settings JSON
        settings_fields = [
            "max_locations",
            "max_characters",
            "max_experiences",
            "autonomous_enabled",
            "time_events_enabled",
            "resource_management_enabled",
            "discovery_generation_enabled",
        ]

        # Update direct fields
        for field in direct_fields:
            if field in validated_data:
                setattr(instance, field, validated_data[field])

        # Handle starting canvas update
        if "starting_canvas_id" in validated_data:
            canvas_id = validated_data["starting_canvas_id"]
            if canvas_id is None:
                instance.starting_canvas = None
            else:
                # Import here to avoid circular imports
                from apps.stories.models import StoryCanvas

                try:
                    canvas = StoryCanvas.objects.get(
                        id=canvas_id, project=instance, deleted_at__isnull=True
                    )
                    instance.starting_canvas = canvas
                except StoryCanvas.DoesNotExist:
                    # This should not happen due to validation, but handle gracefully
                    pass

        # Update settings fields
        if not instance.settings:
            instance.settings = {}

        for field in settings_fields:
            if field in validated_data:
                instance.settings[field] = validated_data[field]

        instance.save()
        return instance
