from rest_framework import serializers
from .models import AssetGroup, AssetVideo, AssetClip, ClipFrame


class AssetGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetGroup
        fields = ["id", "name", "description", "tags", "created_at"]
        read_only_fields = ["id", "created_at"]


class AssetVideoSerializer(serializers.ModelSerializer):
    poster_url = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = AssetVideo
        fields = [
            "id",
            "group",
            "mime_type",
            "size_bytes",
            "width",
            "height",
            "duration_sec",
            "poster_url",
            "file_url",
            "status",
            "error",
            "processing_stage",
            "processing_progress",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "width",
            "height",
            "duration_sec",
            "poster_url",
            "file_url",
            "status",
            "error",
            "processing_stage",
            "processing_progress",
            "created_at",
        ]

    def get_poster_url(self, obj):
        return obj.poster_url

    def get_file_url(self, obj):
        return obj.file_url


class AssetClipSerializer(serializers.ModelSerializer):
    poster_url = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = AssetClip
        fields = [
            "id",
            "video",
            "index",
            "start_sec",
            "end_sec",
            "duration_sec",
            "poster_url",
            "file_url",
            "status",
            "description",
            "description_model",
            "description_generated_at",
            "description_error",
            "deleted_at",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "poster_url",
            "file_url",
            "status",
            "description",
            "description_model",
            "description_generated_at",
            "description_error",
            "deleted_at",
        ]

    def get_poster_url(self, obj):
        return obj.poster_url

    def get_file_url(self, obj):
        return obj.file_url


class ClipFrameSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ClipFrame
        fields = [
            "id",
            "clip",
            "timestamp_sec",
            "image_url",
            "caption_text",
            "status",
            "created_at",
        ]
        read_only_fields = ["id", "image_url", "status", "created_at"]

    def get_image_url(self, obj):
        return obj.image_url

