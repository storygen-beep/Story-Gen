"""
World Designer models for location and connection management.

Converted from FastAPI SQLModel implementation to Django ORM.
"""

import uuid

from django.contrib.auth import get_user_model
from django.db import models

from apps.projects.models import Project

User = get_user_model()


class LocationType(models.TextChoices):
    """Location type choices."""

    GENERIC = "generic", "Generic"
    RESIDENTIAL = "residential", "Residential"
    COMMERCIAL = "commercial", "Commercial"
    RECREATIONAL = "recreational", "Recreational"
    EDUCATIONAL = "educational", "Educational"
    WORKPLACE = "workplace", "Workplace"
    OUTDOOR = "outdoor", "Outdoor"
    TRANSPORT = "transport", "Transport"
    SPECIAL = "special", "Special"


class ConnectionType(models.TextChoices):
    """Deprecated - legacy connection type choices (kept for backward compatibility)."""

    PATH = "path", "Path"
    ROAD = "road", "Road"
    PORTAL = "portal", "Portal"
    STAIRS = "stairs", "Stairs"
    ELEVATOR = "elevator", "Elevator"
    BRIDGE = "bridge", "Bridge"
    TUNNEL = "tunnel", "Tunnel"
    GATE = "gate", "Gate"


class HandlePosition(models.TextChoices):
    """Deprecated - legacy handle positions (kept for backward compatibility)."""

    TOP = "top", "Top"
    BOTTOM = "bottom", "Bottom"
    LEFT = "left", "Left"
    RIGHT = "right", "Right"


class Location(models.Model):
    """Location model for world building."""

    # Primary key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Foreign keys
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="locations"
    )

    # Basic location information
    name = models.CharField(max_length=255, help_text="Location name")
    description = models.TextField(blank=True, help_text="Location description")
    location_type = models.CharField(
        max_length=20,
        choices=LocationType.choices,
        default=LocationType.GENERIC,
        help_text="Type of location",
    )

    # Canvas positioning (absolute coordinates)
    canvas_x = models.FloatField(default=0.0, help_text="Canvas X position")
    canvas_y = models.FloatField(default=0.0, help_text="Canvas Y position")
    canvas_width = models.FloatField(default=120.0, help_text="Canvas width")
    canvas_height = models.FloatField(default=80.0, help_text="Canvas height")

    # Hierarchical positioning
    is_container = models.BooleanField(
        default=False, help_text="Can contain other locations"
    )
    parent_location = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="child_locations",
        help_text="Parent container location",
    )
    relative_x = models.FloatField(default=0.0, help_text="Position relative to parent")
    relative_y = models.FloatField(default=0.0, help_text="Position relative to parent")
    hierarchy_level = models.PositiveIntegerField(
        default=0, help_text="Nesting depth level"
    )

    # Visual properties
    icon = models.CharField(
        max_length=50, blank=True, null=True, help_text="Location icon"
    )
    color = models.CharField(
        max_length=7, blank=True, null=True, help_text="Hex color code"
    )

    # Location properties (JSON field for flexible data)
    properties = models.JSONField(
        default=dict, blank=True, help_text="Additional location properties"
    )
    accessibility_info = models.JSONField(
        default=dict, blank=True, help_text="Accessibility information"
    )

    # Gameplay properties
    is_starting_location = models.BooleanField(
        default=False, help_text="Is this the starting location"
    )
    is_accessible = models.BooleanField(
        default=True, help_text="Is location accessible"
    )
    requires_unlock = models.BooleanField(
        default=False, help_text="Requires unlock to access"
    )
    unlock_conditions = models.JSONField(
        default=dict, blank=True, help_text="Conditions to unlock location"
    )

    # Navigation mode support
    supports_realistic_movement = models.BooleanField(
        default=True, help_text="Supports realistic movement"
    )
    requires_realistic_movement = models.BooleanField(
        default=False, help_text="Requires realistic movement"
    )

    # Simplified Navigation System for Hierarchical Navigation
    entry_from = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="can_enter",
        help_text="The single location this can be entered from"
    )
    default_entry_location = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="default_for_container",
        help_text="Default location when entering this container"
    )

    # Navigation Ordering System
    navigation_order = models.JSONField(
        default=list,
        blank=True,
        help_text="Ordered list of location UUIDs for custom navigation display (exit options always appear at bottom)"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "locations"
        ordering = ["created_at"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(hierarchy_level__lte=20), name="max_hierarchy_level"
            ),
            models.CheckConstraint(
                check=models.Q(canvas_width__gte=50.0)
                & models.Q(canvas_width__lte=2000.0),
                name="valid_canvas_width",
            ),
            models.CheckConstraint(
                check=models.Q(canvas_height__gte=30.0)
                & models.Q(canvas_height__lte=2000.0),
                name="valid_canvas_height",
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.location_type})"

    def clean(self):
        """Validate model data."""
        from django.core.exceptions import ValidationError

        # Prevent self-referencing parent
        if self.parent_location and self.parent_location.id == self.id:
            raise ValidationError("Location cannot be its own parent")

        # Prevent self-referencing entry_from
        if self.entry_from and self.entry_from.id == self.id:
            raise ValidationError("Location cannot enter from itself")

        # Validate parent is a container
        if self.parent_location and not self.parent_location.is_container:
            raise ValidationError("Parent location must be a container")

        # Validate no circular entry paths (prevent A→B→A cycles)
        if self.entry_from:
            visited = set()
            current = self.entry_from
            while current and current.entry_from:
                if current.id in visited:
                    raise ValidationError("Circular entry path detected")
                visited.add(current.id)
                current = current.entry_from
                if len(visited) > 20:  # Safety limit
                    raise ValidationError("Entry path too deep")

        # Navigation Consistency Rules

        # Helper: is `self` a descendant (at any depth) of a given container?
        def _is_descendant_of(container: "Location", node: "Location") -> bool:
            current = node.parent_location
            depth = 0
            while current is not None and depth <= 20:
                if current.id == container.id:
                    return True
                current = current.parent_location
                depth += 1
            return False

        # Rule 1 (updated): Containers with a default entry cannot be used as
        # entry_from for their descendants. They MAY be used as entry_from for
        # locations outside their subtree (outer locations).
        if (
            self.entry_from
            and self.entry_from.is_container
            and self.entry_from.default_entry_location
        ):
            if _is_descendant_of(self.entry_from, self):
                raise ValidationError(
                    f"Cannot set entry_from to container '{self.entry_from.name}' from within its subtree. "
                    f"Enter through its default entry: '{self.entry_from.default_entry_location.name}'."
                )

        # Rule 2 (relaxed): Containers with default entries are allowed to have
        # an entry_from. The restriction is now enforced differently: such
        # containers cannot be used as entry_from by their descendants (handled
        # in Rule 1 above). The default entry location itself still must not
        # have an entry_from (Rule 3 below).

        # Rule 3: Default entry consistency - default entries should NOT have entry_from
        if self.parent_location and hasattr(self.parent_location, 'default_entry_location') and self.parent_location.default_entry_location == self:
            if self.entry_from is not None:
                raise ValidationError(
                    f"As default entry for '{self.parent_location.name}', "
                    f"this location should not have entry_from set (automatic container entry)"
                )

        # Rule 4 (removed/relaxed by Rule 1): Previously, any location with a
        # default entry could not be used as entry_from at all. This is now
        # relaxed: only descendants are forbidden (handled by Rule 1 above).

        # Rule 5: Container boundary respect (except for default entries and the
        # new outer-location allowance). Disallow cross-container links by
        # default, unless:
        #  - this location is its parent's default entry, OR
        #  - entry_from is a container that has a default entry AND this
        #    location is NOT a descendant of that container (outer connection)
        if (
            self.entry_from
            and self.parent_location
            and self.entry_from.parent_location != self.parent_location
        ):
            is_default_entry = (
                hasattr(self.parent_location, "default_entry_location")
                and self.parent_location.default_entry_location == self
            )
            allow_outer_to_container_with_default = (
                self.entry_from.is_container
                and bool(self.entry_from.default_entry_location)
                and not _is_descendant_of(self.entry_from, self)
            )
            if not (is_default_entry or allow_outer_to_container_with_default):
                raise ValidationError(
                    f"Cannot create entry from different container "
                    f"('{self.entry_from.name}' in '{self.entry_from.parent_location.name if self.entry_from.parent_location else 'root'}' "
                    f"to '{self.name}' in '{self.parent_location.name}') unless this is a default entry location "
                    f"or an allowed outer connection to a container with a default entry."
                )

        # Calculate hierarchy level
        if self.parent_location:
            self.hierarchy_level = self.parent_location.hierarchy_level + 1
            if self.hierarchy_level > 20:
                raise ValidationError("Maximum nesting depth of 20 levels exceeded")
        else:
            self.hierarchy_level = 0

    def save(self, *args, **kwargs):
        """Override save to run validation."""
        self.full_clean()
        super().save(*args, **kwargs)

    def get_navigable_locations(self):
        """
        Get all locations accessible from this location following twee generation logic.

        Returns:
            dict: Dictionary with 'destinations', 'leave_option', and 'exit_container' keys
        """
        result = {
            'destinations': [],
            'leave_option': None,
            'exit_container': None
        }

        # 1. Get destinations (locations with entry_from = this location, excluding inside locations)
        destinations = Location.objects.filter(
            entry_from=self
        ).exclude(
            parent_location=self
        ).select_related('project')

        result['destinations'] = list(destinations)

        # 2. Add leave option if location has entry_from
        if self.entry_from:
            result['leave_option'] = self.entry_from

        # 3. Add exit container if applicable
        if self.parent_location and self.parent_location.is_container:
            container = self.parent_location
            show_exit = False

            # Check if container has a default entry location
            if container.default_entry_location:
                # Case 1: Container HAS default entry - only the default entry can exit
                show_exit = (self == container.default_entry_location)
            else:
                # Case 2: Container has NO default entry - any location with entry_from=container can exit
                show_exit = (self.entry_from == container)

            if show_exit and container.entry_from:
                result['exit_container'] = {
                    'container': container,
                    'destination': container.entry_from
                }

        return result

    def get_ordered_navigation(self):
        """
        Get navigation destinations in the proper order using custom order or defaults.

        Returns:
            list: Ordered list of location objects (exit options handled separately)
        """
        navigable = self.get_navigable_locations()
        destinations = navigable['destinations']

        if self.navigation_order and len(self.navigation_order) > 0:
            # Use custom ordering
            ordered_destinations = []
            destination_dict = {str(loc.id): loc for loc in destinations}

            # First, add locations in specified order
            for loc_id in self.navigation_order:
                if str(loc_id) in destination_dict:
                    ordered_destinations.append(destination_dict[str(loc_id)])
                    del destination_dict[str(loc_id)]

            # Add any remaining destinations (newly connected) at the end
            ordered_destinations.extend(destination_dict.values())

            return ordered_destinations
        else:
            # Use default sorting: direct locations first, then containers, alphabetically within groups
            direct_locations = []
            container_locations = []

            for dest in destinations:
                if dest.is_container:
                    container_locations.append(dest)
                else:
                    direct_locations.append(dest)

            # Sort alphabetically within each group
            direct_locations.sort(key=lambda x: x.name.lower())
            container_locations.sort(key=lambda x: x.name.lower())

            return direct_locations + container_locations

    def to_dict(self):
        """Convert location to dictionary for API responses."""
        return {
            "id": str(self.id),
            "project_id": str(self.project.id),
            "name": self.name,
            "description": self.description,
            "location_type": self.location_type,
            "canvas_x": self.canvas_x,
            "canvas_y": self.canvas_y,
            "canvas_width": self.canvas_width,
            "canvas_height": self.canvas_height,
            # Hierarchical fields
            "is_container": self.is_container,
            "parent_location_id": str(self.parent_location.id)
            if self.parent_location
            else None,
            "relative_x": self.relative_x,
            "relative_y": self.relative_y,
            "hierarchy_level": self.hierarchy_level,
            "supports_realistic_movement": self.supports_realistic_movement,
            "requires_realistic_movement": self.requires_realistic_movement,
            # Simplified navigation
            "entry_from_id": str(self.entry_from.id) if self.entry_from else None,
            "default_entry_location_id": str(self.default_entry_location.id) if self.default_entry_location else None,
            # Visual properties
            "icon": self.icon or "🏢",
            "color": self.color or "#3b82f6",
            "properties": self.properties,
            "accessibility_info": self.accessibility_info,
            # Gameplay properties
            "is_starting_location": self.is_starting_location,
            "is_accessible": self.is_accessible,
            "requires_unlock": self.requires_unlock,
            "unlock_conditions": self.unlock_conditions,
            # Timestamps
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


# Simplified navigation system - no additional fields needed
# entry_from ForeignKey provides single-entry navigation
# default_entry_location ForeignKey handles container entry points
