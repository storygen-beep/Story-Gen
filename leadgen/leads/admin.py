from django.contrib import admin

from .models import FollowUpTask, Handoff, Inquiry, Lead, LeadEvent


class InquiryInline(admin.TabularInline):
    model = Inquiry
    extra = 0
    fields = ("source", "listing", "message", "received_at")
    readonly_fields = ("received_at",)


class LeadEventInline(admin.TabularInline):
    model = LeadEvent
    extra = 0
    fields = ("kind", "details", "created_at")
    readonly_fields = fields
    can_delete = False


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("__str__", "phone", "organization", "score", "status", "assigned_agent", "created_at")
    list_filter = ("organization", "score", "status", "opted_out")
    search_fields = ("name", "phone")
    inlines = [InquiryInline, LeadEventInline]


@admin.register(Handoff)
class HandoffAdmin(admin.ModelAdmin):
    list_display = ("lead", "agent", "outcome", "offered_at", "accepted_at")
    list_filter = ("outcome", "agent__organization")


@admin.register(FollowUpTask)
class FollowUpTaskAdmin(admin.ModelAdmin):
    list_display = ("lead", "step", "due_at", "status")
    list_filter = ("status",)


admin.site.register(Inquiry)
admin.site.register(LeadEvent)
