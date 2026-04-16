"""
Project URL configuration.

Defines URL patterns for project CRUD operations matching the frontend expectations.
"""

from django.urls import path

from .views import (
    GenerateGameView,
    PreviewComprehensiveGameView,
    PreviewNavigationGameView,
    ProjectDetailView,
    ProjectListCreateView,
)

app_name = "projects"

urlpatterns = [
    # Project CRUD endpoints - no trailing slashes to match frontend expectations
    path("", ProjectListCreateView.as_view(), name="project-list-create"),
    path("<uuid:project_id>", ProjectDetailView.as_view(), name="project-detail"),
    # Game generation endpoints - match frontend expectations exactly
    path(
        "<uuid:project_id>/preview-game",
        PreviewNavigationGameView.as_view(),
        name="preview-navigation-game",
    ),
    path(
        "<uuid:project_id>/preview-comprehensive-game",
        PreviewComprehensiveGameView.as_view(),
        name="preview-comprehensive-game",
    ),
    path(
        "<uuid:project_id>/generate-game",
        GenerateGameView.as_view(),
        name="generate-game",
    ),
]
