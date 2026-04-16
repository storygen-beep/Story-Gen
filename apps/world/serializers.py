"""
World Designer serializers for API requests and responses.

Matches the frontend interface expectations exactly.
"""

from rest_framework import serializers

from .models import Location


class LocationSerializer(serializers.ModelSerializer):
    """Serializer for Location model with all fields."""

    id = serializers.UUIDField(read_only=True)
    project_id = serializers.UUIDField(source="project.id", read_only=True)
    parent_location_id = serializers.UUIDField(
        source="parent_location.id", read_only=True, allow_null=True
    )
    # Simplified navigation fields (read-only for overview; separate endpoints will mutate)
    entry_from_id = serializers.UUIDField(
        source="entry_from.id", read_only=True, allow_null=True
    )
    default_entry_location_id = serializers.UUIDField(
        source="default_entry_location.id", read_only=True, allow_null=True
    )

    class Meta:
        model = Location
        fields = [
            "id",
            "project_id",
            "name",
            "description",
            "location_type",
            "canvas_x",
            "canvas_y",
            "canvas_width",
            "canvas_height",
            "is_container",
            "parent_location_id",
            "relative_x",
            "relative_y",
            "hierarchy_level",
            "supports_realistic_movement",
            "requires_realistic_movement",
            "icon",
            "color",
            "properties",
            "accessibility_info",
            "is_starting_location",
            "is_accessible",
            "requires_unlock",
            "unlock_conditions",
            # Simplified navigation fields
            "entry_from_id",
            "default_entry_location_id",
            "navigation_order",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "project_id",
            "hierarchy_level",
            "created_at",
            "updated_at",
        ]

    def to_representation(self, instance):
        """Override to match frontend expectations exactly."""
        data = super().to_representation(instance)

        # Ensure defaults for frontend compatibility
        data["icon"] = data["icon"] or "🏢"
        data["color"] = data["color"] or "#3b82f6"
        data["properties"] = data["properties"] or {}
        data["accessibility_info"] = data["accessibility_info"] or {}
        data["unlock_conditions"] = data["unlock_conditions"] or {}

        # Nothing additional to populate; entry_from_id is provided via source mapping
        
        return data


class LocationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating locations."""

    class Meta:
        model = Location
        fields = [
            "name",
            "description",
            "location_type",
            "canvas_x",
            "canvas_y",
            "canvas_width",
            "canvas_height",
            "is_container",
            "parent_location",
            "relative_x",
            "relative_y",
            "supports_realistic_movement",
            "requires_realistic_movement",
            "icon",
            "color",
            "properties",
            "is_starting_location",
        ]

    def validate_name(self, value):
        """Validate location name."""
        if not value.strip():
            raise serializers.ValidationError("Location name cannot be empty")
        return value.strip()

    def validate_parent_location(self, value):
        """Validate parent location is a container."""
        if value and not value.is_container:
            raise serializers.ValidationError("Parent location must be a container")
        return value


class LocationUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating locations."""

    class Meta:
        model = Location
        fields = [
            "name",
            "description",
            "location_type",
            "canvas_x",
            "canvas_y",
            "canvas_width",
            "canvas_height",
            "is_container",
            "parent_location",
            "relative_x",
            "relative_y",
            "supports_realistic_movement",
            "requires_realistic_movement",
            "icon",
            "color",
            "properties",
            "navigation_order",
            "is_starting_location",
        ]

    def validate_name(self, value):
        """Validate location name."""
        if value is not None and not value.strip():
            raise serializers.ValidationError("Location name cannot be empty")
        return value.strip() if value else value

    def validate_parent_location(self, value):
        """Validate parent location is a container."""
        if value and not value.is_container:
            raise serializers.ValidationError("Parent location must be a container")
        return value


class LocationConnectionSerializer(serializers.Serializer):
    """Deprecated placeholder (removed model). Use world overview derived connections."""
    pass


class LocationConnectionCreateSerializer(serializers.Serializer):
    """Deprecated placeholder (removed model). Use entry/exit/default endpoints."""
    pass


class LocationConnectionUpdateSerializer(serializers.Serializer):
    """Deprecated placeholder (removed model)."""
    pass


class WorldOverviewSerializer(serializers.Serializer):
    """Serializer for complete world overview."""

    project_id = serializers.UUIDField(read_only=True)
    locations = LocationSerializer(many=True, read_only=True)
    connections = serializers.JSONField(read_only=True)
    canvas_state = serializers.JSONField(read_only=True)
    world_metadata = serializers.JSONField(read_only=True)
    location_count = serializers.IntegerField(read_only=True)
    connection_count = serializers.IntegerField(read_only=True)
    starting_location_id = serializers.UUIDField(read_only=True, allow_null=True)


class LocationNestSerializer(serializers.Serializer):
    """Serializer for nesting location into container."""

    container_id = serializers.UUIDField()

    def validate_container_id(self, value):
        """Validate container exists and is a container."""
        try:
            container = Location.objects.get(id=value)
            if not container.is_container:
                raise serializers.ValidationError("Target location is not a container")
            return value
        except Location.DoesNotExist:
            raise serializers.ValidationError("Container location not found")


class LocationUnnestSerializer(serializers.Serializer):
    """Serializer for unnesting location from container."""

    x = serializers.FloatField()
    y = serializers.FloatField()


class CanvasStateUpdateSerializer(serializers.Serializer):
    """Serializer for canvas state updates."""

    zoom = serializers.FloatField(min_value=0.1, max_value=10.0)
    pan_x = serializers.FloatField(default=0.0)
    pan_y = serializers.FloatField(default=0.0)
    grid_enabled = serializers.BooleanField(default=True)
    snap_to_grid = serializers.BooleanField(default=True)
    grid_size = serializers.IntegerField(min_value=10, max_value=100, default=20)


class LocationNavigationSerializer(serializers.ModelSerializer):
    """Serializer for location navigation information."""

    accessible_locations = serializers.SerializerMethodField()
    ordered_navigation = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = [
            "id",
            "name",
            "navigation_order",
            "accessible_locations",
            "ordered_navigation"
        ]

    def get_accessible_locations(self, obj):
        """Get all accessible locations from this location."""
        navigable = obj.get_navigable_locations()

        result = {
            'destinations': [],
            'leave_option': None,
            'exit_container': None
        }

        # Add destination locations
        for dest in navigable['destinations']:
            result['destinations'].append({
                'id': str(dest.id),
                'name': dest.name,
                'type': 'destination',
                'is_container': dest.is_container,
                'location_type': dest.location_type
            })

        # Add leave option
        if navigable['leave_option']:
            result['leave_option'] = {
                'id': str(navigable['leave_option'].id),
                'name': navigable['leave_option'].name,
                'type': 'leave',
                'is_container': navigable['leave_option'].is_container
            }

        # Add exit container option
        if navigable['exit_container']:
            container = navigable['exit_container']['container']
            destination = navigable['exit_container']['destination']
            result['exit_container'] = {
                'container_id': str(container.id),
                'container_name': container.name,
                'destination_id': str(destination.id),
                'destination_name': destination.name,
                'type': 'exit_container'
            }

        return result

    def get_ordered_navigation(self, obj):
        """Get ordered navigation destinations."""
        ordered_destinations = obj.get_ordered_navigation()

        return [
            {
                'id': str(dest.id),
                'name': dest.name,
                'is_container': dest.is_container,
                'location_type': dest.location_type
            }
            for dest in ordered_destinations
        ]


class NavigationOrderUpdateSerializer(serializers.Serializer):
    """Serializer for updating navigation order."""

    navigation_order = serializers.ListField(
        child=serializers.UUIDField(),
        allow_empty=True,
        help_text="Ordered list of location UUIDs for navigation display"
    )
