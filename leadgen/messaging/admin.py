from django.contrib import admin

from .models import Channel, Conversation, Message, MessageTemplate


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "organization", "provider", "status")
    list_filter = ("provider", "status")


@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "language", "purpose", "approval", "channel")
    list_filter = ("approval", "purpose", "language")


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    fields = ("created_at", "direction", "sender", "text", "transcript", "status", "block_reason")
    readonly_fields = ("created_at",)


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("lead", "channel", "mode", "last_message_at")
    list_filter = ("mode",)
    inlines = [MessageInline]


@admin.action(description="Approve and queue selected messages")
def approve_messages(modeladmin, request, queryset):
    # Approve mode: AI drafts sit in pending_approval until a human taps approve.
    queryset.filter(status=Message.Status.PENDING_APPROVAL).update(status=Message.Status.QUEUED)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("conversation", "sender", "status", "created_at")
    list_filter = ("status", "sender", "direction")
    actions = [approve_messages]
