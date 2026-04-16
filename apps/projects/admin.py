"""
Project Admin for Django Admin Panel.

Provides comprehensive project management with custom fields and functionality.
"""

import json

from django.contrib import admin
from django.utils.html import format_html

from .models import Project, ProjectStatus


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Custom Project Admin with full functionality."""

    # Display fields in the project list
    list_display = (
        "name",
        "owner_display",
        "status",
        "complexity",
        "genre",
        "world_size",
        "created_at",
        "updated_at",
    )

    # Fields that can be searched
    search_fields = ("name", "description", "summary", "genre", "theme")

    # Filters in the admin sidebar
    list_filter = (
        "status",
        "complexity",
        "world_size",
        "genre",
        "theme",
        "owner",
        "created_at",
        "updated_at",
        "deleted_at",
    )

    # Fields displayed when editing a project
    fieldsets = (
        ("Basic Information", {"fields": ("name", "description", "summary")}),
        (
            "Project Configuration",
            {"fields": ("status", "complexity", "genre", "theme", "world_size")},
        ),
        ("Ownership", {"fields": ("owner",)}),
        (
            "Advanced Settings",
            {
                "fields": ("settings_display", "metadata_display"),
                "classes": ("collapse",),
            },
        ),
        (
            "System Information",
            {
                "fields": ("id", "created_at", "updated_at", "deleted_at"),
                "classes": ("collapse",),
            },
        ),
    )

    # Read-only fields
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "settings_display",
        "metadata_display",
    )

    # Ordering in the list
    ordering = ("-created_at",)

    # Items per page
    list_per_page = 25

    # Additional functionality
    actions = [
        "mark_as_draft",
        "mark_as_active",
        "mark_as_published",
        "mark_as_archived",
        "restore_deleted",
    ]

    def owner_display(self, obj):
        """Display owner with link to user admin."""
        if obj.owner:
            return format_html(
                '<a href="/admin/authentication/user/{}/change/">{}</a>',
                obj.owner.id,
                obj.owner.email,
            )
        return "-"

    owner_display.short_description = "Owner"
    owner_display.admin_order_field = "owner__email"

    def settings_display(self, obj):
        """Display settings JSON in a formatted way."""
        if obj.settings:
            return format_html(
                '<pre style="background: #f8f8f8; padding: 10px; border-radius: 4px;">{}</pre>',
                json.dumps(obj.settings, indent=2),
            )
        return "No settings"

    settings_display.short_description = "Project Settings"

    def metadata_display(self, obj):
        """Display metadata JSON in a formatted way."""
        if obj.metadata:
            return format_html(
                '<pre style="background: #f8f8f8; padding: 10px; border-radius: 4px;">{}</pre>',
                json.dumps(obj.metadata, indent=2),
            )
        return "No metadata"

    metadata_display.short_description = "Project Metadata"

    def get_queryset(self, request):
        """Include soft-deleted projects for admin users."""
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            # Show all projects including soft-deleted ones for superusers
            return queryset.all()
        return queryset.filter(deleted_at__isnull=True)

    # Custom actions
    def mark_as_draft(self, request, queryset):
        """Mark selected projects as draft."""
        queryset.update(status=ProjectStatus.DRAFT)
        self.message_user(request, f"{queryset.count()} projects marked as draft.")

    mark_as_draft.short_description = "Mark selected projects as draft"

    def mark_as_active(self, request, queryset):
        """Mark selected projects as active."""
        queryset.update(status=ProjectStatus.ACTIVE)
        self.message_user(request, f"{queryset.count()} projects marked as active.")

    mark_as_active.short_description = "Mark selected projects as active"

    def mark_as_published(self, request, queryset):
        """Mark selected projects as published."""
        queryset.update(status=ProjectStatus.PUBLISHED)
        self.message_user(request, f"{queryset.count()} projects marked as published.")

    mark_as_published.short_description = "Mark selected projects as published"

    def mark_as_archived(self, request, queryset):
        """Mark selected projects as archived."""
        queryset.update(status=ProjectStatus.ARCHIVED)
        self.message_user(request, f"{queryset.count()} projects marked as archived.")

    mark_as_archived.short_description = "Mark selected projects as archived"

    def restore_deleted(self, request, queryset):
        """Restore soft-deleted projects."""
        count = 0
        for project in queryset:
            if project.deleted_at:
                project.restore()
                count += 1
        self.message_user(request, f"{count} projects restored from deleted status.")

    restore_deleted.short_description = "Restore deleted projects"

    def get_form(self, request, obj=None, **kwargs):
        """Customize the form for project creation/editing."""
        form = super().get_form(request, obj, **kwargs)

        # Set the current user as the default owner for new projects
        if not obj and "owner" in form.base_fields:
            form.base_fields["owner"].initial = request.user

        return form
