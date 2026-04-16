"""
Django admin configuration for Elora Simplified models.
"""

from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

from .models import AgentMemory, AgentSession


@admin.register(AgentMemory)
class AgentMemoryAdmin(admin.ModelAdmin):
    """Admin interface for AgentMemory model."""

    list_display = [
        'kind',
        'topic',
        'truncated_text',
        'project_name',
        'tags_display',
        'created_at',
        'is_expired_display'
    ]

    list_filter = [
        'kind',
        'created_at',
        'ttl_days',
        'project__name',
    ]

    search_fields = [
        'topic',
        'text',
        'tags',
        'project__name',
    ]

    readonly_fields = [
        'id',
        'created_at',
        'is_expired_display',
    ]

    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'project', 'kind', 'topic')
        }),
        ('Content', {
            'fields': ('text', 'tags')
        }),
        ('References', {
            'fields': ('refs',),
            'description': 'JSON references to canvas/node/location IDs'
        }),
        ('Lifecycle', {
            'fields': ('ttl_days', 'created_at', 'is_expired_display')
        }),
    )

    ordering = ['-created_at']

    def truncated_text(self, obj):
        """Show truncated text in list view."""
        if len(obj.text) > 50:
            return f"{obj.text[:50]}..."
        return obj.text
    truncated_text.short_description = 'Text'

    def project_name(self, obj):
        """Show project name."""
        return obj.project.name if obj.project else 'No Project'
    project_name.short_description = 'Project'
    project_name.admin_order_field = 'project__name'

    def tags_display(self, obj):
        """Display tags as badges."""
        if not obj.tags:
            return '-'

        badges = []
        for tag in obj.tags[:3]:  # Show max 3 tags
            badges.append(f'<span style="background:#e1f5fe; padding:2px 6px; border-radius:3px; font-size:11px;">{tag}</span>')

        if len(obj.tags) > 3:
            badges.append(f'<span style="color:#666;">+{len(obj.tags) - 3} more</span>')

        return format_html(' '.join(badges))
    tags_display.short_description = 'Tags'

    def is_expired_display(self, obj):
        """Show if memory is expired."""
        if obj.is_expired():
            return format_html('<span style="color:red;">⚠️ Expired</span>')
        elif obj.ttl_days <= 0:
            return format_html('<span style="color:green;">♾️ Never expires</span>')
        else:
            days_left = obj.ttl_days - (timezone.now() - obj.created_at).days
            if days_left <= 7:
                return format_html(f'<span style="color:orange;">⏳ {days_left} days left</span>')
            else:
                return format_html(f'<span style="color:green;">✅ {days_left} days left</span>')
    is_expired_display.short_description = 'Status'


@admin.register(AgentSession)
class AgentSessionAdmin(admin.ModelAdmin):
    """Admin interface for AgentSession model."""

    list_display = [
        'id',
        'project_name',
        'user_email',
        'mode',
        'is_active',
        'duration',
        'started_at',
        'last_tool'
    ]

    list_filter = [
        'mode',
        'is_active',
        'started_at',
        'project__name',
        'user__email',
    ]

    search_fields = [
        'user_goal',
        'project__name',
        'user__email',
        'last_tool',
    ]

    readonly_fields = [
        'id',
        'started_at',
        'updated_at',
        'ended_at',
        'duration',
    ]

    fieldsets = (
        ('Session Info', {
            'fields': ('id', 'project', 'user', 'mode', 'is_active')
        }),
        ('Current Context', {
            'fields': ('user_goal', 'context_snippets', 'feedback_topics', 'last_tool')
        }),
        ('Timestamps', {
            'fields': ('started_at', 'updated_at', 'ended_at', 'duration')
        }),
    )

    ordering = ['-started_at']

    def project_name(self, obj):
        """Show project name."""
        return obj.project.name if obj.project else 'No Project'
    project_name.short_description = 'Project'
    project_name.admin_order_field = 'project__name'

    def user_email(self, obj):
        """Show user email."""
        return obj.user.email if obj.user else 'No User'
    user_email.short_description = 'User'
    user_email.admin_order_field = 'user__email'

    def duration(self, obj):
        """Show session duration."""
        if obj.ended_at:
            duration = obj.ended_at - obj.started_at
        elif obj.is_active:
            duration = timezone.now() - obj.started_at
        else:
            return 'Unknown'

        total_seconds = int(duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60

        if hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
    duration.short_description = 'Duration'

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('project', 'user')
