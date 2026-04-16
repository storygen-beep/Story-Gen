"""
Character Management admin configuration.

Provides comprehensive Django admin interface for character management
with filters, search, and organized field display.
"""

from django.contrib import admin

from .models import Character, CharacterStatus


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    """Admin interface for Character model with comprehensive management features."""

    # List view configuration
    list_display = [
        "name",
        "project",
        "status",
        "age",
        "gender",
        "character_level",
        "experience_points",
        "created_at",
    ]
    list_filter = ["status", "gender", "project", "created_at", "updated_at"]
    list_editable = ["status"]
    list_per_page = 25

    # Search configuration
    search_fields = [
        "name",
        "description",
        "project__name",
        "tags",
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
        ("Core Traits", {"fields": ("core_traits",), "classes": ("collapse",)}),
        (
            "World Integration",
            {"fields": ("current_location", "relationships"), "classes": ("collapse",)},
        ),
        (
            "Game Properties",
            {
                "fields": (
                    "experience_points",
                    "character_level",
                    "progression_data",
                    "inventory",
                    "equipment",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "AI & Behavior",
            {"fields": ("ai_behavior_config",), "classes": ("collapse",)},
        ),
        (
            "Metadata & Organization",
            {
                "fields": (
                    "tags",
                    "categories",
                    "character_metadata",
                    "game_properties",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Development",
            {
                "fields": ("development_notes", "inspiration_sources"),
                "classes": ("collapse",),
            },
        ),
        (
            "System Fields",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                    "deleted_at",
                ),
                "classes": ("collapse",),
                "description": "System-managed fields for auditing and tracking",
            },
        ),
    )

    # Read-only fields
    readonly_fields = ["created_at", "updated_at"]

    # Foreign key optimization
    select_related = ["project", "current_location"]

    # Custom display methods
    def get_queryset(self, request):
        """Optimize queryset with select_related for foreign keys."""
        return (
            super()
            .get_queryset(request)
            .select_related("project", "current_location")
            .filter(deleted_at__isnull=True)
        )

    def has_delete_permission(self, request, obj=None):
        """Allow delete permission - uses soft delete via model."""
        return request.user.is_staff

    def delete_model(self, request, obj):
        """Use soft delete instead of hard delete."""
        obj.soft_delete()

    def delete_queryset(self, request, queryset):
        """Bulk soft delete for selected objects."""
        for obj in queryset:
            obj.soft_delete()

    # Custom actions
    actions = ["archive_characters"]

    def archive_characters(self, request, queryset):
        """Archive selected characters."""
        updated = queryset.update(status=CharacterStatus.ARCHIVED)
        self.message_user(request, f"{updated} characters archived.")

    archive_characters.short_description = "Archive selected characters"

    # Custom form handling
    def save_model(self, request, obj, form, change):
        """Save character model."""
        super().save_model(request, obj, form, change)


# Customize admin site headers
admin.site.site_header = "Story Generation Platform Admin"
admin.site.site_title = "Character Management"
admin.site.index_title = "Character Administration"
