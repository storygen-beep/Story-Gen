"""
NPC Management URL patterns.

Defines URL routing for NPC endpoints matching frontend expectations.
"""

from django.urls import path

from .views import (
    NPCBulkUpdateView,
    NPCDetailView,
    NPCListCreateView,
    NPCOverviewView,
    NPCScheduleView,
    NPCStatsView,
)

urlpatterns = [
    # NPC Overview - GET /projects/{id}/npcs
    path("<uuid:project_id>/npcs", NPCOverviewView.as_view(), name="npc-overview"),
    # NPC List and Create - GET, POST /projects/{id}/npcs/npcs
    path(
        "<uuid:project_id>/npcs/npcs",
        NPCListCreateView.as_view(),
        name="npc-list-create",
    ),
    # NPC Detail Operations - GET, PUT, PATCH, DELETE /projects/{id}/npcs/{npc_id}
    path(
        "<uuid:project_id>/npcs/<uuid:npc_id>",
        NPCDetailView.as_view(),
        name="npc-detail",
    ),
    # NPC Schedule Management - PUT /projects/{id}/npcs/{npc_id}/schedule
    path(
        "<uuid:project_id>/npcs/<uuid:npc_id>/schedule",
        NPCScheduleView.as_view(),
        name="npc-schedule",
    ),
    # NPC Statistics - GET /projects/{id}/npcs/stats
    path("<uuid:project_id>/npcs/stats", NPCStatsView.as_view(), name="npc-stats"),
    # NPC Bulk Operations - PATCH /projects/{id}/npcs/bulk
    path(
        "<uuid:project_id>/npcs/bulk",
        NPCBulkUpdateView.as_view(),
        name="npc-bulk-update",
    ),
]
