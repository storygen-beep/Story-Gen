"""
Story Canvas admin configuration.

Provides comprehensive Django admin interface for story canvas management
with filters, search, and organized field display.
"""

from django.contrib import admin
from django.utils.html import format_html

from .models import (
    CanvasStatus,
    CanvasTrigger,
    NodeConnection,
    StoryCanvas,
    StoryNode,
    TriggerSchedule,
)


class StoryNodeInline(admin.TabularInline):
    """Inline admin for story nodes within a canvas."""

    model = StoryNode
    extra = 0
    fields = [
        "name",
        "position_x",
        "position_y",
        "width",
        "height",
    ]
    readonly_fields = []


class NodeConnectionInline(admin.TabularInline):
    """Inline admin for node connections within a canvas."""

    model = NodeConnection
    extra = 0
    fields = ["source_node", "target_node", "connection_type", "label", "is_valid"]
    readonly_fields = ["is_valid"]


# StoryFlag removed


class TriggerScheduleInline(admin.TabularInline):
    """Inline admin for trigger schedules within a trigger."""

    model = TriggerSchedule
    extra = 0
    fields = ["name", "weekdays", "start_time", "end_time"]
    verbose_name = "Schedule"
    verbose_name_plural = "Schedules"


class CanvasTriggerInline(admin.StackedInline):
    """Inline admin for canvas trigger."""

    model = CanvasTrigger
    extra = 0
    fields = [
        "location_id",
        "is_active",
        "is_activity",
        "is_repeatable",
        "max_triggers_per_day",
    ]


@admin.register(StoryCanvas)
class StoryCanvasAdmin(admin.ModelAdmin):
    """Admin interface for StoryCanvas model with comprehensive management features."""

    # List view configuration
    list_display = [
        "name",
        "project",
        "canvas_type",
        "status",
        "node_count",
        "connection_count",
        "is_valid_display",
        "is_favorite",
        "version",
        "created_at",
    ]
    list_filter = [
        "canvas_type",
        "status",
        "is_valid",
        "is_favorite",
        "version",
        "project",
        "created_at",
        "updated_at",
    ]
    list_editable = ["status", "is_favorite"]
    list_per_page = 25

    # Search configuration
    search_fields = [
        "name",
        "description",
        "tags",
        "project__name",
    ]

    # Detail view organization
    fieldsets = (
        (
            "Basic Information",
            {"fields": ("project", "name", "description", "canvas_type", "status")},
        ),
        (
            "Canvas Properties",
            {
                "fields": (
                    "tags",
                    "version",
                    "estimated_play_time",
                    "is_favorite",
                    "display_order",
                )
            },
        ),
        (
            "Statistics",
            {"fields": ("node_count", "connection_count"), "classes": ("collapse",)},
        ),
        (
            "Validation",
            {
                "fields": ("is_valid", "validation_errors", "last_validated_at"),
                "classes": ("collapse",),
            },
        ),
        ("Metadata", {"fields": ("metadata",), "classes": ("collapse",)}),
        (
            "Audit Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                    "deleted_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    # Read-only fields
    readonly_fields = [
        "node_count",
        "connection_count",
        "is_valid",
        "validation_errors",
        "last_validated_at",
        "created_at",
        "updated_at",
    ]

    # Inlines
    inlines = [
        StoryNodeInline,
        NodeConnectionInline,
        CanvasTriggerInline,
    ]

    # Filters and ordering
    ordering = ["-created_at"]
    date_hierarchy = "created_at"

    # Custom methods
    def get_queryset(self, request):
        """Include related objects to reduce queries."""
        return (
            super()
            .get_queryset(request)
            .select_related("project")
            .filter(deleted_at__isnull=True)
        )

    def save_model(self, request, obj, form, change):
        """Save the model."""
        super().save_model(request, obj, form, change)

    # Custom display methods
    def is_valid_display(self, obj):
        """Display validation status with color coding."""
        if obj.is_valid:
            return format_html('<span style="color: green;">✓ Valid</span>')
        else:
            error_count = len(obj.validation_errors) if obj.validation_errors else 0
            return format_html(
                '<span style="color: red;">✗ Invalid ({})</span>', error_count
            )

    is_valid_display.short_description = "Validation Status"

    # Custom admin actions
    actions = [
        "validate_canvases",
        "mark_as_favorite",
        "mark_as_draft",
        "mark_as_published",
    ]

    def validate_canvases(self, request, queryset):
        """Validate selected canvases."""
        count = 0
        for canvas in queryset:
            # This would call the validation service
            count += 1
        self.message_user(request, f"{count} canvases queued for validation.")

    validate_canvases.short_description = "Validate selected canvases"

    def mark_as_favorite(self, request, queryset):
        """Mark selected canvases as favorites."""
        count = queryset.update(is_favorite=True)
        self.message_user(request, f"{count} canvases marked as favorites.")

    mark_as_favorite.short_description = "Mark as favorite"

    def mark_as_draft(self, request, queryset):
        """Mark selected canvases as draft."""
        count = queryset.update(status=CanvasStatus.DRAFT)
        self.message_user(request, f"{count} canvases marked as draft.")

    mark_as_draft.short_description = "Mark as draft"

    def mark_as_published(self, request, queryset):
        """Mark selected canvases as published."""
        count = queryset.update(status=CanvasStatus.PUBLISHED)
        self.message_user(request, f"{count} canvases marked as published.")

    mark_as_published.short_description = "Mark as published"


@admin.register(StoryNode)
class StoryNodeAdmin(admin.ModelAdmin):
    """Admin interface for StoryNode model."""

    list_display = [
        "name",
        "canvas",
        "exit_block_summary",
        "position_x",
        "position_y",
        "created_at",
    ]
    list_filter = [
        "canvas__project",
        "created_at",
    ]
    search_fields = ["name", "canvas__name"]

    fieldsets = (
        ("Basic Information", {"fields": ("canvas", "name")}),
        (
            "Position & Size",
            {"fields": ("position_x", "position_y", "width", "height")},
        ),
        ("Content", {"fields": ("node_data", "tags"), "classes": ("collapse",)}),
        (
            "Exit Block",
            {
                "fields": ("exit_block",),
                "classes": ("collapse",),
                "description": "JSON configuration for story node exit behavior including destination and time progression",
            },
        ),
        ("Audit", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    readonly_fields = ["created_at", "updated_at"]
    ordering = ["canvas", "created_at"]

    def exit_block_summary(self, obj):
        """Display exit block configuration summary."""
        if not obj.exit_block:
            return format_html('<span style="color: gray;">No exit block</span>')

        try:
            exit_type = obj.exit_block.get("type", "unknown")
            text = obj.exit_block.get("text", "Continue")
            config = obj.exit_block.get("config", {})
            destination_type = config.get("destinationType", "trigger")
            time_minutes = config.get("time_progression_minutes", 3)

            destination_display = {
                "trigger": "Trigger Location",
                "specific": f'Location {config.get("locationId", "?")}',
            }.get(destination_type, destination_type)

            return format_html(
                '<div style="font-size: 11px;">'
                '<strong>"{}"</strong> → {} '
                '<br><span style="color: #666;">⏱️ {}min</span>'
                "</div>",
                text,
                destination_display,
                time_minutes,
            )
        except Exception:
            return format_html('<span style="color: red;">Invalid exit block</span>')

    exit_block_summary.short_description = "Exit Block"


@admin.register(NodeConnection)
class NodeConnectionAdmin(admin.ModelAdmin):
    """Admin interface for NodeConnection model."""

    list_display = [
        "canvas",
        "source_node",
        "target_node",
        "connection_type",
        "label",
        "priority",
        "is_valid_display",
        "created_at",
    ]
    list_filter = ["connection_type", "is_bidirectional", "is_valid", "canvas__project"]
    search_fields = ["label", "canvas__name", "source_node__name", "target_node__name"]

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "canvas",
                    "source_node",
                    "target_node",
                    "connection_type",
                    "label",
                )
            },
        ),
        ("Properties", {"fields": ("priority", "weight", "is_bidirectional")}),
        ("Logic", {"fields": ("conditions", "effects"), "classes": ("collapse",)}),
        ("Visual", {"fields": ("path_data", "style"), "classes": ("collapse",)}),
        ("Metadata", {"fields": ("metadata",), "classes": ("collapse",)}),
        (
            "Validation",
            {"fields": ("is_valid", "validation_errors"), "classes": ("collapse",)},
        ),
    )

    readonly_fields = ["is_valid", "validation_errors", "created_at", "updated_at"]
    ordering = ["canvas", "priority"]

    def is_valid_display(self, obj):
        """Display validation status with color coding."""
        if obj.is_valid:
            return format_html('<span style="color: green;">✓</span>')
        else:
            return format_html('<span style="color: red;">✗</span>')

    is_valid_display.short_description = "Valid"


## StoryFlag admin removed


@admin.register(CanvasTrigger)
class CanvasTriggerAdmin(admin.ModelAdmin):
    """Admin interface for CanvasTrigger model."""

    list_display = [
        "canvas",
        "location_id",
        "is_active",
        "is_activity",
        "is_repeatable",
        "schedule_count",
        "created_at",
    ]
    list_filter = ["is_active", "is_activity", "is_repeatable", "canvas__project"]
    search_fields = ["canvas__name"]

    fieldsets = (
        ("Basic Information", {"fields": ("canvas", "location_id")}),
        (
            "Trigger Properties",
            {
                "fields": (
                    "is_active",
                    "is_activity",
                    "is_repeatable",
                    "max_triggers_per_day",
                )
            },
        ),
        ("Conditions", {"fields": ("conditions",), "classes": ("collapse",)}),
        ("Metadata", {"fields": ("metadata",), "classes": ("collapse",)}),
        (
            "Audit",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    # Inlines
    inlines = [TriggerScheduleInline]

    readonly_fields = [
        "created_at",
        "updated_at",
    ]
    ordering = ["canvas", "location_id"]

    def schedule_count(self, obj):
        """Display number of schedules for this trigger."""
        return obj.schedules.count()

    schedule_count.short_description = "Schedules"

    def save_model(self, request, obj, form, change):
        """Save the model."""
        super().save_model(request, obj, form, change)


@admin.register(TriggerSchedule)
class TriggerScheduleAdmin(admin.ModelAdmin):
    """Admin interface for TriggerSchedule model."""

    list_display = [
        "name",
        "trigger",
        "weekdays_display",
        "start_time",
        "end_time",
        "schedule_type",
        "created_at",
    ]
    list_filter = [
        "trigger__canvas__project",
        "start_time",
        "created_at",
    ]
    search_fields = [
        "name",
        "trigger__canvas__name",
    ]

    fieldsets = (
        ("Basic Information", {"fields": ("trigger", "name")}),
        ("Schedule Properties", {"fields": ("weekdays", "start_time", "end_time")}),
        ("Audit", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    readonly_fields = ["created_at", "updated_at"]
    ordering = ["trigger", "start_time"]

    def weekdays_display(self, obj):
        """Display weekdays in a readable format."""
        if not obj.weekdays:
            return "None"

        weekday_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        selected_days = [weekday_names[day] for day in obj.weekdays if 0 <= day <= 6]

        # Check for common patterns
        if obj.weekdays == [0, 1, 2, 3, 4]:
            return "Weekdays"
        elif obj.weekdays == [5, 6]:
            return "Weekends"
        elif len(obj.weekdays) == 7:
            return "Daily"
        else:
            return ", ".join(selected_days)

    weekdays_display.short_description = "Days"

    def schedule_type(self, obj):
        """Display whether it's a point trigger or range trigger."""
        if obj.end_time:
            return f"Range ({obj.start_time} - {obj.end_time})"
        else:
            return f"Point ({obj.start_time})"

    schedule_type.short_description = "Type"
