from django.urls import path
from . import views


urlpatterns = [
    # Groups
    path("assets/groups", views.AssetGroupListCreateView.as_view(), name="asset-group-list-create"),
    path("assets/groups/<uuid:group_id>", views.AssetGroupDetailView.as_view(), name="asset-group-detail"),
    # Videos in a group
    path("assets/groups/<uuid:group_id>/videos", views.AssetVideoListView.as_view(), name="asset-video-list"),
    path("assets/groups/<uuid:group_id>/videos/upload", views.AssetVideoUploadView.as_view(), name="asset-video-upload"),
    path("assets/groups/<uuid:group_id>/videos/ingest-url", views.AssetVideoIngestUrlView.as_view(), name="asset-video-ingest-url"),
    # Video detail
    path("assets/videos/<uuid:video_id>", views.AssetVideoDetailView.as_view(), name="asset-video-detail"),
    path("assets/videos/<uuid:video_id>/signed-url", views.AssetVideoSignedUrlView.as_view(), name="asset-video-signed-url"),
    # Clips and frames
    path("assets/videos/<uuid:video_id>/clips", views.AssetClipListView.as_view(), name="asset-clip-list"),
    path("assets/videos/<uuid:video_id>/clips/deleted", views.AssetClipDeletedListView.as_view(), name="asset-clip-deleted-list"),
    path("assets/clips/<uuid:clip_id>", views.AssetClipDetailView.as_view(), name="asset-clip-detail"),
    path("assets/clips/<uuid:clip_id>/signed-url", views.AssetClipSignedUrlView.as_view(), name="asset-clip-signed-url"),
    path("assets/clips/<uuid:clip_id>/delete", views.AssetClipDeleteView.as_view(), name="asset-clip-delete"),
    path("assets/clips/<uuid:clip_id>/restore", views.AssetClipRestoreView.as_view(), name="asset-clip-restore"),
    path("assets/clips/<uuid:clip_id>/permanent", views.AssetClipHardDeleteView.as_view(), name="asset-clip-hard-delete"),
    path("assets/clips/<uuid:clip_id>/frames", views.ClipFrameListView.as_view(), name="asset-clip-frame-list"),
    # Clip description generation
    path("assets/clips/<uuid:clip_id>/generate-description", views.AssetClipGenerateDescriptionView.as_view(), name="asset-clip-generate-description"),
    # Batch video description generation
    path("assets/videos/<uuid:video_id>/generate-descriptions", views.AssetVideoGenerateDescriptionsView.as_view(), name="asset-video-generate-descriptions"),
    # Export clip descriptions
    path("assets/videos/<uuid:video_id>/export-descriptions", views.AssetVideoExportDescriptionsView.as_view(), name="asset-video-export-descriptions"),
    path("assets/groups/<uuid:group_id>/export-descriptions", views.AssetGroupExportDescriptionsView.as_view(), name="asset-group-export-descriptions"),
    # Disabled endpoints
    # path("assets/frames/<uuid:frame_id>/recaption", views.FrameRecaptionView.as_view(), name="asset-frame-recaption"),
]
