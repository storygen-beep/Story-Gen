"""
World Designer URL configuration.

Defines URL patterns for world management operations matching the frontend expectations.
"""

from django.urls import path

from .views import (
    LocationDetailView,
    LocationListCreateView,
    LocationNestView,
    LocationEntryFromView,
    LocationDefaultEntryView,
    LocationUnnestView,
    WorldOverviewView,
)

app_name = "world"

urlpatterns = [
    # World overview endpoint - no trailing slash to match frontend expectations
    path("<uuid:project_id>/world", WorldOverviewView.as_view(), name="world-overview"),
    # Location management endpoints - no trailing slashes to match frontend expectations
    path(
        "<uuid:project_id>/world/locations",
        LocationListCreateView.as_view(),
        name="location-list-create",
    ),
    path(
        "<uuid:project_id>/world/locations/<uuid:location_id>",
        LocationDetailView.as_view(),
        name="location-detail",
    ),
    # Location nesting endpoints - no trailing slashes to match frontend expectations
    path(
        "<uuid:project_id>/world/locations/<uuid:location_id>/nest",
        LocationNestView.as_view(),
        name="location-nest",
    ),
    path(
        "<uuid:project_id>/world/locations/<uuid:location_id>/unnest",
        LocationUnnestView.as_view(),
        name="location-unnest",
    ),
    # Entry-from + Default entry management endpoints
    path(
        "<uuid:project_id>/world/locations/<uuid:location_id>/entry-from",
        LocationEntryFromView.as_view(),
        name="location-entry-from",
    ),
    path(
        "<uuid:project_id>/world/locations/<uuid:location_id>/default-entry",
        LocationDefaultEntryView.as_view(),
        name="location-default-entry",
    ),
    # Legacy connection endpoints removed (use entry/exit/default endpoints above)
]
