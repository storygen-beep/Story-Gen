"""
URL configuration for story system.

Maps API endpoints to views for story canvas management.
"""

from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "stories"

# DRF Router for ViewSets
router = DefaultRouter()
router.register(r'schedules', views.TriggerScheduleViewSet, basename='schedule')

urlpatterns = [
    # Canvas endpoints
    path(
        "projects/<uuid:project_id>/story/canvases",
        views.StoryCanvasListView.as_view(),
        name="canvas-list",
    ),
    # Exit choices condition check for a node
    path(
        "projects/<uuid:project_id>/story/canvases/<uuid:canvas_id>/nodes/<uuid:node_id>/choices/check",
        views.ExitChoicesCheckView.as_view(),
        name="exit-choices-check",
    ),
    path(
        "projects/<uuid:project_id>/story/canvases/<uuid:canvas_id>",
        views.StoryCanvasDetailView.as_view(),
        name="canvas-detail",
    ),
    path(
        "projects/<uuid:project_id>/story/intro-canvas",
        views.IntroCanvasView.as_view(),
        name="intro-canvas",
    ),
    path(
        "projects/<uuid:project_id>/story/canvases/<uuid:canvas_id>/validate",
        views.CanvasValidateView.as_view(),
        name="canvas-validate",
    ),
    path(
        "projects/<uuid:project_id>/story/canvases/<uuid:canvas_id>/save-story",
        views.StoryCanvasSaveView.as_view(),
        name="canvas-save-story",
    ),
    path(
        "projects/<uuid:project_id>/story/canvases/<uuid:canvas_id>/duplicate",
        views.CanvasDuplicateView.as_view(),
        name="canvas-duplicate",
    ),
    path(
        "projects/<uuid:project_id>/story/canvas-templates",
        views.CanvasTemplatesView.as_view(),
        name="canvas-templates",
    ),
    # Node endpoints
    path(
        "projects/<uuid:project_id>/story/canvases/<uuid:canvas_id>/nodes",
        views.StoryNodeListView.as_view(),
        name="node-list",
    ),
    path(
        "projects/<uuid:project_id>/story/canvases/<uuid:canvas_id>/nodes/<uuid:node_id>",
        views.StoryNodeDetailView.as_view(),
        name="node-detail",
    ),
    # Connection endpoints
    path(
        "projects/<uuid:project_id>/story/canvases/<uuid:canvas_id>/connections",
        views.NodeConnectionListView.as_view(),
        name="connection-list",
    ),
    path(
        "projects/<uuid:project_id>/story/canvases/<uuid:canvas_id>/connections/<uuid:connection_id>",
        views.NodeConnectionDetailView.as_view(),
        name="connection-detail",
    ),
    # Trigger endpoint
    path(
        "projects/<uuid:project_id>/story/canvases/<uuid:canvas_id>/trigger",
        views.CanvasTriggerView.as_view(),
        name="canvas-trigger",
    ),
    # Trigger availability check
    path(
        "projects/<uuid:project_id>/story/canvases/<uuid:canvas_id>/trigger/check",
        views.CanvasTriggerCheckView.as_view(),
        name="canvas-trigger-check",
    ),
    # Trigger schedules endpoint (nested under canvas trigger)
    path(
        "projects/<uuid:project_id>/story/canvases/<uuid:canvas_id>/trigger/schedules",
        views.TriggerScheduleListView.as_view(),
        name="canvas-trigger-schedules",
    ),
    # BlockNote content processing endpoints
    path(
        "projects/<uuid:project_id>/story/canvases/<uuid:canvas_id>/nodes/<uuid:node_id>/convert-content",
        views.StoryNodeContentConversionView.as_view(),
        name="node-convert-content",
    ),
    path(
        "projects/<uuid:project_id>/story/canvases/<uuid:canvas_id>/convert-all-content",
        views.StoryCanvasContentConversionView.as_view(),
        name="canvas-convert-all-content",
    ),
    path(
        "projects/<uuid:project_id>/story/canvases/<uuid:canvas_id>/nodes/<uuid:node_id>/validate",
        views.StoryNodeValidationView.as_view(),
        name="node-validate",
    ),
    # Options endpoints for trigger condition builder
    path(
        "projects/<uuid:project_id>/story/options/characters",
        views.TriggerOptionsCharactersView.as_view(),
        name="trigger-options-characters",
    ),
    # Media upload and listing
    path(
        "projects/<uuid:project_id>/story/media",
        views.ProjectMediaListView.as_view(),
        name="media-list",
    ),
    path(
        "projects/<uuid:project_id>/story/media/upload",
        views.ProjectMediaUploadView.as_view(),
        name="media-upload",
    ),
]

# Include DRF router URLs
urlpatterns += router.urls
