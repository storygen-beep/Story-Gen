"""
NPC Management API views.

Provides RESTful API endpoints for NPC CRUD operations,
role-based management, and template generation.
"""


from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.projects.models import Project

from .models import NPC
from .serializers import (
    NPCBulkUpdateSerializer,
    NPCCreateSerializer,
    NPCListSerializer,
    NPCScheduleUpdateSerializer,
    NPCUpdateSerializer,
)
from .services import NPCService


class NPCOverviewView(APIView):
    """NPC overview endpoint for project NPC data - handles both GET (overview) and POST (create)."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        """Get complete NPC overview for the project."""
        try:
            # Get and verify project ownership
            project = get_object_or_404(Project, id=project_id, owner=request.user)

            # Use service layer to get NPC overview
            overview = NPCService.get_npc_overview(project)

            return Response(overview, status=status.HTTP_200_OK)

        except Project.DoesNotExist:
            return Response(
                {"error": "Project not found or access denied"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to get NPC overview: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request, project_id):
        """Create a new NPC for the project."""
        try:
            # Get and verify project ownership
            project = get_object_or_404(Project, id=project_id, owner=request.user)

            # Validate request data
            serializer = NPCCreateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {"error": "Invalid data", "details": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Create NPC using service layer
            npc_dict = NPCService.create_npc_with_validation(
                project=project,
                npc_data=serializer.validated_data,
            )

            return Response(npc_dict, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Project.DoesNotExist:
            return Response(
                {"error": "Project not found or access denied"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to create NPC: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class NPCListCreateView(APIView):
    """NPC list and creation endpoint."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        """Get all NPCs for the project."""
        try:
            # Get and verify project ownership
            project = get_object_or_404(Project, id=project_id, owner=request.user)

            # Get NPCs with filtering and pagination
            npcs = NPC.objects.filter(
                project=project, deleted_at__isnull=True
            )

            # Apply filters if provided
            status_filter = request.query_params.get("status")
            if status_filter:
                npcs = npcs.filter(status=status_filter)

            # Serialize NPCs
            serializer = NPCListSerializer(npcs, many=True)

            return Response(
                {
                    "npcs": serializer.data,
                    "total_count": npcs.count(),
                    "project_id": str(project_id),
                },
                status=status.HTTP_200_OK,
            )

        except Project.DoesNotExist:
            return Response(
                {"error": "Project not found or access denied"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to get NPCs: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request, project_id):
        """Create a new NPC."""
        try:
            # Get and verify project ownership
            project = get_object_or_404(Project, id=project_id, owner=request.user)

            # Validate and serialize the request data
            serializer = NPCCreateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {"error": "Invalid data", "details": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Use service layer to create NPC
            npc_dict = NPCService.create_npc_with_validation(
                project=project,
                npc_data=serializer.validated_data,
            )

            return Response(npc_dict, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Project.DoesNotExist:
            return Response(
                {"error": "Project not found or access denied"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to create NPC: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class NPCDetailView(APIView):
    """NPC detail endpoint for individual NPC operations."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id, npc_id):
        """Get specific NPC details."""
        try:
            # Get and verify project ownership
            project = get_object_or_404(Project, id=project_id, owner=request.user)

            # Get NPC using service layer
            npc_dict = NPCService.get_npc_by_id(project, npc_id)

            if not npc_dict:
                return Response(
                    {"error": "NPC not found"}, status=status.HTTP_404_NOT_FOUND
                )

            return Response(npc_dict, status=status.HTTP_200_OK)

        except Project.DoesNotExist:
            return Response(
                {"error": "Project not found or access denied"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to get NPC: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, project_id, npc_id):
        """Update NPC (full update)."""
        return self._update_npc(request, project_id, npc_id, partial=False)

    def patch(self, request, project_id, npc_id):
        """Update NPC (partial update)."""
        return self._update_npc(request, project_id, npc_id, partial=True)

    def delete(self, request, project_id, npc_id):
        """Delete NPC (soft delete)."""
        try:
            # Get and verify project ownership
            project = get_object_or_404(Project, id=project_id, owner=request.user)

            # Delete NPC using service layer
            NPCService.delete_npc(project, npc_id)

            return Response(
                {"message": "NPC deleted successfully"}, status=status.HTTP_200_OK
            )

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Project.DoesNotExist:
            return Response(
                {"error": "Project not found or access denied"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to delete NPC: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def _update_npc(self, request, project_id, npc_id, partial=True):
        """Helper method for NPC updates."""
        try:
            # Get and verify project ownership
            project = get_object_or_404(Project, id=project_id, owner=request.user)

            # Validate request data
            serializer = NPCUpdateSerializer(data=request.data, partial=partial)
            if not serializer.is_valid():
                return Response(
                    {"error": "Invalid data", "details": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Update NPC using service layer
            npc_dict = NPCService.update_npc_with_validation(
                project=project,
                npc_id=npc_id,
                npc_data=serializer.validated_data,
            )

            return Response(npc_dict, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Project.DoesNotExist:
            return Response(
                {"error": "Project not found or access denied"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to update NPC: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class NPCScheduleView(APIView):
    """NPC schedule and behavior management endpoint."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, project_id, npc_id):
        """Update NPC schedule and behavior patterns."""
        try:
            # Get and verify project ownership
            project = get_object_or_404(Project, id=project_id, owner=request.user)

            # Validate request data
            serializer = NPCScheduleUpdateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {"error": "Invalid data", "details": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Update schedule using service layer
            schedule_dict = NPCService.update_npc_schedule(
                project=project,
                npc_id=npc_id,
                schedule_data=serializer.validated_data,
            )

            return Response(schedule_dict, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Project.DoesNotExist:
            return Response(
                {"error": "Project not found or access denied"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to update schedule: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class NPCStatsView(APIView):
    """NPC statistics endpoint."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        """Get detailed NPC statistics for the project."""
        try:
            # Get and verify project ownership
            project = get_object_or_404(Project, id=project_id, owner=request.user)

            # Get statistics from service layer
            stats = NPCService.get_npc_statistics(project)

            return Response(stats, status=status.HTTP_200_OK)

        except Project.DoesNotExist:
            return Response(
                {"error": "Project not found or access denied"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to get statistics: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class NPCBulkUpdateView(APIView):
    """NPC bulk operations endpoint."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, project_id):
        """Bulk update multiple NPCs."""
        try:
            # Get and verify project ownership
            project = get_object_or_404(Project, id=project_id, owner=request.user)

            # Validate request data
            serializer = NPCBulkUpdateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {"error": "Invalid data", "details": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Perform bulk update using service layer
            result = NPCService.bulk_update_npcs(
                project=project,
                npc_ids=serializer.validated_data["npc_ids"],
                update_data=serializer.validated_data["update_data"].validated_data,
            )

            return Response(result, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Project.DoesNotExist:
            return Response(
                {"error": "Project not found or access denied"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to bulk update NPCs: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
