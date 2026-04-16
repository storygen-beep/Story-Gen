"""
NPC Management admin configuration.

Provides comprehensive Django admin interface for NPC management
with filters, search, and organized field display.
"""

from django.contrib import admin

from .models import NPC, NPCStatus


@admin.register(NPC)
class NPCAdmin(admin.ModelAdmin):
    """Admin interface for NPC model with comprehensive management features."""

    # List view configuration
    list_display = ["name", "project", "status", "age", "gender", "created_at"]
    list_filter = [
        "status",
        "gender",
        "project",
        "created_at",
        "updated_at",
        "deleted_at",
    ]
    list_editable = ["status"]
    list_per_page = 25

    # Search configuration
    search_fields = [
        "name",
        "description",
        "project__name",
        "categories",
    ]

    # Detail view organization
    fieldsets = (
        (
            "Basic Information",
            {"fields": ("name", "project", "status", "description", "portrait_url")},
        ),
        (
            "Physical Characteristics",
            {"fields": ("age", "gender", "appearance"), "classes": ("collapse",)},
        ),
        (
            "Core Traits & Behavior",
            {"fields": ("core_traits",), "classes": ("collapse",)},
        ),
        (
            "Relationships & AI",
            {
                "fields": ("relationships", "ai_behavior_config"),
                "classes": ("collapse",),
            },
        ),
        ("Organization", {"fields": ("categories",), "classes": ("collapse",)}),
        (
            "Metadata",
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
    readonly_fields = ["created_at", "updated_at"]

    # Filters and ordering
    ordering = ["-created_at"]
    date_hierarchy = "created_at"

    # Custom methods for display
    def get_queryset(self, request):
        """Include related objects to reduce queries."""
        return (
            super()
            .get_queryset(request)
            .select_related("project")
        )

    def save_model(self, request, obj, form, change):
        """Save NPC model."""
        super().save_model(request, obj, form, change)

    # Custom admin actions
    actions = ["mark_as_active", "mark_as_inactive"]

    def mark_as_active(self, request, queryset):
        """Mark selected NPCs as active."""
        count = queryset.update(status=NPCStatus.READY)
        self.message_user(request, f"{count} NPCs marked as active.")

    mark_as_active.short_description = "Mark selected NPCs as active"

    def mark_as_inactive(self, request, queryset):
        """Mark selected NPCs as inactive."""
        count = queryset.update(status=NPCStatus.CONCEPT)
        self.message_user(request, f"{count} NPCs marked as inactive.")

    mark_as_inactive.short_description = "Mark selected NPCs as inactive"
