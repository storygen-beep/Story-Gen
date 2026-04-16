"""
Custom User Admin for Django Admin Panel.

Provides comprehensive user management with custom fields and functionality.
"""

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    """Custom User Admin with support for custom fields."""

    # Display fields in the user list
    list_display = (
        "email",
        "username",
        "full_name",
        "role",
        "status",
        "is_active",
        "is_verified",
        "date_joined",
        "last_login_at",
    )

    # Fields that can be searched
    search_fields = ("email", "username", "full_name")

    # Filters in the admin sidebar
    list_filter = (
        "role",
        "status",
        "is_active",
        "is_verified",
        "is_staff",
        "is_superuser",
        "date_joined",
        "last_login",
    )

    # Fields displayed when editing a user
    fieldsets = (
        ("Basic Information", {"fields": ("email", "password")}),
        ("Profile", {"fields": ("username", "full_name", "avatar_url")}),
        (
            "Permissions & Role",
            {
                "fields": (
                    "role",
                    "status",
                    "is_active",
                    "is_verified",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "OAuth Information",
            {"fields": ("oauth_provider", "oauth_id"), "classes": ("collapse",)},
        ),
        (
            "Important Dates",
            {
                "fields": ("date_joined", "last_login", "last_login_at"),
                "classes": ("collapse",),
            },
        ),
        (
            "System Fields",
            {
                "fields": ("id",),
                "classes": ("collapse",),
            },
        ),
    )

    # Fields displayed when creating a new user
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "role", "status"),
            },
        ),
        (
            "Profile",
            {"classes": ("wide",), "fields": ("username", "full_name", "avatar_url")},
        ),
    )

    # Read-only fields
    readonly_fields = ("id", "date_joined", "last_login", "last_login_at")

    # Ordering in the list
    ordering = ("-date_joined",)

    # Fields to display by default
    list_per_page = 25

    # Additional functionality
    actions = ["make_active", "make_inactive", "verify_users", "unverify_users"]

    def make_active(self, request, queryset):
        """Mark selected users as active."""
        queryset.update(status="active")
        self.message_user(request, f"{queryset.count()} users marked as active.")

    make_active.short_description = "Mark selected users as active"

    def make_inactive(self, request, queryset):
        """Mark selected users as inactive."""
        queryset.update(status="inactive")
        self.message_user(request, f"{queryset.count()} users marked as inactive.")

    make_inactive.short_description = "Mark selected users as inactive"

    def verify_users(self, request, queryset):
        """Verify selected users."""
        queryset.update(is_verified=True)
        self.message_user(request, f"{queryset.count()} users verified.")

    verify_users.short_description = "Verify selected users"

    def unverify_users(self, request, queryset):
        """Unverify selected users."""
        queryset.update(is_verified=False)
        self.message_user(request, f"{queryset.count()} users unverified.")

    unverify_users.short_description = "Unverify selected users"
