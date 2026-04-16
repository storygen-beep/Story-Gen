"""
World Admin for Django Admin Panel.

Provides comprehensive world building management for locations and connections.
"""

import json

from django.contrib import admin
from django.utils.html import format_html

from .models import Location


# Removed LocationConnection admin inline (legacy model removed)


class ChildLocationInline(admin.TabularInline):
    """Inline admin for child locations."""

    model = Location
    fk_name = "parent_location"
    extra = 0
    fields = ("name", "location_type", "relative_x", "relative_y", "is_accessible")
    readonly_fields = ("id",)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Custom Location Admin with hierarchical support."""

    # Display fields in the location list
    list_display = (
        "name",
        "location_type",
        "project_link",
        "parent_location",
        "hierarchy_level",
        "is_starting_location",
        "is_accessible",
        "entry_source",
        "default_entry_child",
        "canvas_position",
        "created_at",
    )

    # Fields that can be searched
    search_fields = ("name", "description", "project__name")

    # Filters in the admin sidebar
    list_filter = (
        "location_type",
        "project",
        "is_starting_location",
        "is_accessible",
        "requires_unlock",
        "is_container",
        "hierarchy_level",
        "created_at",
    )

    # Fields displayed when editing a location
    fieldsets = (
        ("Basic Information", {"fields": ("name", "description", "location_type")}),
        ("Project", {"fields": ("project",)}),
        (
            "Canvas Positioning",
            {"fields": ("canvas_x", "canvas_y", "canvas_width", "canvas_height")},
        ),
        (
            "Hierarchical Structure",
            {
                "fields": (
                    "is_container",
                    "parent_location",
                    "relative_x",
                    "relative_y",
                    "hierarchy_level",
                )
            },
        ),
        ("Visual Properties", {"fields": ("icon", "color"), "classes": ("collapse",)}),
        (
            "Gameplay Properties",
            {
                "fields": (
                    "is_starting_location",
                    "is_accessible",
                    "requires_unlock",
                    "unlock_conditions",
                    "supports_realistic_movement",
                    "requires_realistic_movement",
                )
            },
        ),
        (
            "Navigation",
            {
                "fields": (
                    "entry_from",
                    "default_entry_location",
                )
            },
        ),
        (
            "Advanced Properties",
            {
                "fields": ("properties_display", "accessibility_info_display"),
                "classes": ("collapse",),
            },
        ),
        (
            "System Information",
            {"fields": ("id", "created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    # Read-only fields
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "properties_display",
        "accessibility_info_display",
    )

    # Relationship widgets
    raw_id_fields = (
        "project",
        "parent_location",
        "entry_from",
        "default_entry_location",
    )

    # Ordering in the list
    ordering = ("project", "hierarchy_level", "name")

    # Items per page
    list_per_page = 25

    # Inlines
    inlines = [ChildLocationInline]

    # Actions
    actions = [
        "mark_as_starting_location",
        "mark_as_accessible",
        "mark_as_inaccessible",
        "make_container",
        "remove_container",
    ]

    def project_link(self, obj):
        """Display project with link to project admin."""
        if obj.project:
            return format_html(
                '<a href="/admin/projects/project/{}/change/">{}</a>',
                obj.project.id,
                obj.project.name,
            )
        return "-"

    project_link.short_description = "Project"
    project_link.admin_order_field = "project__name"

    def canvas_position(self, obj):
        """Display canvas position in a formatted way."""
        return f"({obj.canvas_x:.0f}, {obj.canvas_y:.0f})"

    canvas_position.short_description = "Canvas Position"

    def properties_display(self, obj):
        """Display properties JSON in a formatted way."""
        if obj.properties:
            return format_html(
                '<pre style="background: #f8f8f8; padding: 10px; border-radius: 4px;">{}</pre>',
                json.dumps(obj.properties, indent=2),
            )
        return "No properties"

    properties_display.short_description = "Location Properties"

    def accessibility_info_display(self, obj):
        """Display accessibility info JSON in a formatted way."""
        if obj.accessibility_info:
            return format_html(
                '<pre style="background: #f8f8f8; padding: 10px; border-radius: 4px;">{}</pre>',
                json.dumps(obj.accessibility_info, indent=2),
            )
        return "No accessibility info"

    accessibility_info_display.short_description = "Accessibility Information"

    # Navigation helper columns
    def entry_source(self, obj):
        return obj.entry_from.name if obj.entry_from else "-"

    entry_source.short_description = "Entry From"

    def default_entry_child(self, obj):
        return (
            obj.default_entry_location.name if obj.default_entry_location else "-"
        )

    default_entry_child.short_description = "Default Entry"

    # Custom actions
    def mark_as_starting_location(self, request, queryset):
        """Mark selected locations as starting locations."""
        # First, unmark all other starting locations in the same projects
        projects = set(queryset.values_list("project_id", flat=True))
        for project_id in projects:
            Location.objects.filter(
                project_id=project_id, is_starting_location=True
            ).exclude(id__in=queryset.values_list("id", flat=True)).update(
                is_starting_location=False
            )

        queryset.update(is_starting_location=True)
        self.message_user(
            request, f"{queryset.count()} locations marked as starting locations."
        )

    mark_as_starting_location.short_description = "Mark as starting location"

    def mark_as_accessible(self, request, queryset):
        """Mark selected locations as accessible."""
        queryset.update(is_accessible=True)
        self.message_user(
            request, f"{queryset.count()} locations marked as accessible."
        )

    mark_as_accessible.short_description = "Mark as accessible"

    def mark_as_inaccessible(self, request, queryset):
        """Mark selected locations as inaccessible."""
        queryset.update(is_accessible=False)
        self.message_user(
            request, f"{queryset.count()} locations marked as inaccessible."
        )

    mark_as_inaccessible.short_description = "Mark as inaccessible"

    def make_container(self, request, queryset):
        """Mark selected locations as containers."""
        queryset.update(is_container=True)
        self.message_user(
            request, f"{queryset.count()} locations marked as containers."
        )

    make_container.short_description = "Make container locations"

    def remove_container(self, request, queryset):
        """Remove container status from selected locations."""
        queryset.update(is_container=False)
        self.message_user(
            request, f"{queryset.count()} locations no longer containers."
        )

    remove_container.short_description = "Remove container status"


# Removed LocationConnection admin (legacy model removed)
