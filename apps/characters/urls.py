"""
Character Management URL routing configuration.

Maps character management endpoints to views following REST conventions
and frontend expectations.
"""

from django.urls import path

from .views import (
    CharacterTemplatesView,
    PlayerCharacterLocationView,
    PlayerCharacterTraitsView,
    PlayerCharacterView,
)

urlpatterns = [
    # Player character main endpoint (handles GET, POST, PUT)
    path(
        "<uuid:project_id>/character",
        PlayerCharacterView.as_view(),
        name="player-character",
    ),
    # Player character management endpoints
    path(
        "<uuid:project_id>/character/traits",
        PlayerCharacterTraitsView.as_view(),
        name="player-character-traits",
    ),
    path(
        "<uuid:project_id>/character/location",
        PlayerCharacterLocationView.as_view(),
        name="player-character-location",
    ),
    # Character templates endpoint
    path(
        "<uuid:project_id>/character/templates",
        CharacterTemplatesView.as_view(),
        name="character-templates",
    ),
]
