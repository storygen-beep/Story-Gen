from django.contrib import admin
from .models import AssetGroup, AssetVideo, AssetClip, ClipFrame


@admin.register(AssetGroup)
class AssetGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "created_at", "deleted_at")
    search_fields = ("name",)
    list_filter = ("owner",)


@admin.register(AssetVideo)
class AssetVideoAdmin(admin.ModelAdmin):
    list_display = ("id", "group", "mime_type", "size_bytes", "status", "processing_stage", "processing_progress", "created_at")
    list_filter = ("status", "group")
    search_fields = ("file",)
    readonly_fields = ("id", "created_at", "updated_at", "processing_stage", "processing_progress", "error", "width", "height", "duration_sec")
    fieldsets = (
        ("Basic Info", {
            "fields": ("id", "group", "file", "mime_type", "size_bytes")
        }),
        ("Video Details", {
            "fields": ("width", "height", "duration_sec", "poster")
        }),
        ("Processing", {
            "fields": ("status", "processing_stage", "processing_progress", "error")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at")
        }),
    )


@admin.register(AssetClip)
class AssetClipAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "video",
        "index",
        "duration_sec",
        "status",
        "has_description",
        "created_at"
    )
    list_filter = (
        "video",
        "status",
        "description_generated_at",
    )
    search_fields = (
        "video__id",
        "description",
    )
    readonly_fields = (
        "id",
        "created_at",
        "description_generated_at",
    )
    actions = ["regenerate_descriptions"]

    def has_description(self, obj):
        """Display if clip has AI description."""
        return bool(obj.description)
    has_description.boolean = True
    has_description.short_description = "Has Description"

    def regenerate_descriptions(self, request, queryset):
        """Admin action to regenerate descriptions for selected clips."""
        from .services.grok_clip_service import get_grok_client
        from django.utils import timezone

        client = get_grok_client()
        if not client.is_available():
            self.message_user(
                request,
                "Grok service not available. Check settings.",
                level="ERROR"
            )
            return

        success_count = 0
        error_count = 0

        for clip in queryset:
            try:
                description = client.generate_description(clip)
                if description:
                    clip.description = description
                    clip.description_model = client.model
                    clip.description_generated_at = timezone.now()
                    clip.description_error = ""
                    clip.save(update_fields=[
                        'description',
                        'description_model',
                        'description_generated_at',
                        'description_error'
                    ])
                    success_count += 1
            except Exception as e:
                clip.description_error = str(e)
                clip.save(update_fields=['description_error'])
                error_count += 1

        self.message_user(
            request,
            f"Successfully regenerated {success_count} descriptions "
            f"({error_count} errors)"
        )

    regenerate_descriptions.short_description = "Regenerate AI descriptions for selected clips"


@admin.register(ClipFrame)
class ClipFrameAdmin(admin.ModelAdmin):
    list_display = ("id", "clip", "timestamp_sec", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("caption_text",)

