"""
API v1 URL routing configuration.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.projects.views import ProjectSettingsView

# Initialize DRF router
router = DefaultRouter()

# TODO: Register viewsets here as we create them
# router.register(r'projects', ProjectViewSet)
# router.register(r'stories', StoryViewSet)

urlpatterns = [
    # Authentication endpoints
    path("auth/", include("apps.authentication.urls")),
    # Foundation system endpoints
    path("foundation/projects/", include("apps.projects.urls")),
    # Project settings endpoints - matches frontend expectations exactly
    path(
        "projects/<uuid:project_id>/settings",
        ProjectSettingsView.as_view(),
        name="project-settings",
    ),
    # World Designer endpoints - matches frontend expectations exactly
    path("projects/", include("apps.world.urls")),
    # Character Management endpoints - matches frontend expectations exactly
    path("projects/", include("apps.characters.urls")),
    # NPC Management endpoints - matches frontend expectations exactly
    path("projects/", include("apps.npcs.urls")),
    # Story Management endpoints - matches frontend expectations exactly
    path("", include("apps.stories.urls")),
    # Global Asset Library endpoints
    path("", include("apps.assets.urls")),
    # Main API routes
    path("", include(router.urls)),
    # Health check endpoint
    path("health/", include("api.v1.health")),
    # Development tools (not for production)
    path("dev/", include("api.v1.dev")),
    # Video browser dev tool
    path("dev/video-browser/", include("api.v1.video_browser")),
    # Game review dev tool
    path("dev/game-review/", include("api.v1.game_review")),
    # Media finder dev tool
    path("dev/media-finder/", include("api.v1.media_finder")),
]
