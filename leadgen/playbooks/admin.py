from django.contrib import admin

from .models import IndustryTemplate, KnowledgeItem, Playbook, PlaybookVersion


@admin.register(IndustryTemplate)
class IndustryTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "updated_at")
    prepopulated_fields = {"slug": ("name",)}


class PlaybookVersionInline(admin.TabularInline):
    model = PlaybookVersion
    extra = 0
    fields = ("number", "changed_by", "created_at")
    readonly_fields = fields
    can_delete = False
    show_change_link = True


@admin.register(Playbook)
class PlaybookAdmin(admin.ModelAdmin):
    list_display = ("organization", "template", "current_version")
    inlines = [PlaybookVersionInline]


@admin.register(PlaybookVersion)
class PlaybookVersionAdmin(admin.ModelAdmin):
    list_display = ("playbook", "number", "changed_by", "created_at")
    list_filter = ("playbook",)


@admin.register(KnowledgeItem)
class KnowledgeItemAdmin(admin.ModelAdmin):
    list_display = ("title", "kind", "organization", "external_ref", "is_active")
    list_filter = ("organization", "kind", "is_active")
    search_fields = ("title", "body", "external_ref")
