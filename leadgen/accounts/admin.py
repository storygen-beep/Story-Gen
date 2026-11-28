from django.contrib import admin

from .models import Agent, Organization


class AgentInline(admin.TabularInline):
    model = Agent
    extra = 0
    fk_name = "organization"
    fields = ("name", "whatsapp_number", "role", "languages", "areas", "backup_agent", "is_active")


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "status", "plan", "created_at")
    list_filter = ("status", "country")
    search_fields = ("name", "license_number")
    inlines = [AgentInline]


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ("name", "organization", "role", "whatsapp_number", "is_active")
    list_filter = ("organization", "role", "is_active")
    search_fields = ("name", "whatsapp_number")
