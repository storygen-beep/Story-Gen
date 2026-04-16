"""
Story Canvas API views.

Provides REST API endpoints for story canvas management including canvases,
nodes, connections, flags, and triggers.
"""

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.projects.models import Project

from .legacy_services import (
    CanvasTriggerService,
    NodeConnectionService,
    StoryCanvasService,
    StoryNodeService,
)
from .models import (
    CanvasTrigger,
    NodeConnection,
    StoryCanvas,
    StoryNode,
    TriggerSchedule,
    MediaAsset,
    MediaKind,
)
from .serializers import (
    ActiveTriggersSerializer,
    # BlockNote-specific serializers
    BlockValidationResultSerializer,
    CanvasTemplateSerializer,
    CanvasTriggerCreateSerializer,
    CanvasTriggerUpdateSerializer,
    ContentConversionResponseSerializer,
    NodeConnectionCreateSerializer,
    NodeConnectionSerializer,
    NodeConnectionUpdateSerializer,
    SaveStoryResponseSerializer,
    # Story save serializers
    SaveStorySerializer,
    StoryCanvasCreateSerializer,
    StoryCanvasDetailSerializer,
    StoryCanvasSerializer,
    StoryCanvasUpdateSerializer,
    StoryNodeCreateSerializer,
    StoryNodeSerializer,
    StoryNodeUpdateSerializer,
    TriggerScheduleCreateSerializer,
    TriggerScheduleSerializer,
    MediaAssetSerializer,
    MediaUploadResponseSerializer,
)
from .services.block_conversion import BlockConversionService
from .services.validation import BlockValidationService


class StoryCanvasListView(APIView):
    """List and create story canvases for a project."""

    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        """List canvases with optional filters."""
        project = get_object_or_404(Project, id=project_id)

        # Get query parameters
        status_filter = request.query_params.get("status")
        canvas_type_filter = request.query_params.get("canvas_type_filter")
        limit = int(request.query_params.get("limit", 50))
        offset = int(request.query_params.get("offset", 0))

        try:
            overview_data = StoryCanvasService.get_canvas_overview(
                project=project,
                status_filter=status_filter,
                canvas_type_filter=canvas_type_filter,
                limit=limit,
                offset=offset,
            )

            return Response(overview_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Failed to retrieve canvases: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request, project_id):
        """Create a new story canvas."""
        project = get_object_or_404(Project, id=project_id)

        serializer = StoryCanvasCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = StoryCanvasService.create_canvas_with_validation(
                project=project,
                canvas_data=serializer.validated_data,
            )

            return Response(result, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": f"Failed to create canvas: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class StoryCanvasDetailView(APIView):
    """Get, update, and delete specific story canvases."""

    permission_classes = [IsAuthenticated]

    def get(self, request, project_id, canvas_id):
        """Get canvas details with optional nested data."""
        project = get_object_or_404(Project, id=project_id)
        canvas = get_object_or_404(
            StoryCanvas, id=canvas_id, project=project, deleted_at__isnull=True
        )

        # Check query parameters for nested data
        include_nodes = (
            request.query_params.get("include_nodes", "true").lower() == "true"
        )
        include_connections = (
            request.query_params.get("include_connections", "true").lower() == "true"
        )
        include_flags = (
            request.query_params.get("include_flags", "true").lower() == "true"
        )

        try:
            if include_nodes or include_connections or include_flags:
                serializer = StoryCanvasDetailSerializer(canvas)
            else:
                serializer = StoryCanvasSerializer(canvas)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Failed to retrieve canvas: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, project_id, canvas_id):
        """Update canvas details."""
        project = get_object_or_404(Project, id=project_id)
        canvas = get_object_or_404(
            StoryCanvas, id=canvas_id, project=project, deleted_at__isnull=True
        )

        serializer = StoryCanvasUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = StoryCanvasService.update_canvas(
                canvas=canvas,
                update_data=serializer.validated_data,
            )

            return Response(result, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": f"Failed to update canvas: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, project_id, canvas_id):
        """Soft delete a canvas."""
        project = get_object_or_404(Project, id=project_id)
        canvas = get_object_or_404(
            StoryCanvas, id=canvas_id, project=project, deleted_at__isnull=True
        )

        try:
            result = StoryCanvasService.soft_delete_canvas(
                canvas=canvas, deleted_by=request.user
            )

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Failed to delete canvas: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class IntroCanvasView(APIView):
    """Get project's intro canvas with trigger information."""

    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        """Get intro canvas details."""
        project = get_object_or_404(Project, id=project_id)

        include_trigger = (
            request.query_params.get("include_trigger", "true").lower() == "true"
        )
        include_validation = (
            request.query_params.get("include_validation", "false").lower() == "true"
        )

        try:
            result = StoryCanvasService.get_intro_canvas(
                project=project,
                include_trigger=include_trigger,
                include_validation=include_validation,
            )

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Failed to retrieve intro canvas: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CanvasValidateView(APIView):
    """Validate a story canvas."""

    permission_classes = [IsAuthenticated]

    def post(self, request, project_id, canvas_id):
        """Validate canvas structure and content."""
        project = get_object_or_404(Project, id=project_id)
        canvas = get_object_or_404(
            StoryCanvas, id=canvas_id, project=project, deleted_at__isnull=True
        )

        try:
            validation_result = StoryCanvasService.validate_canvas(canvas)
            return Response(validation_result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Failed to validate canvas: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CanvasDuplicateView(APIView):
    """Duplicate a story canvas."""

    permission_classes = [IsAuthenticated]

    def post(self, request, project_id, canvas_id):
        """Duplicate canvas with all its components."""
        project = get_object_or_404(Project, id=project_id)
        canvas = get_object_or_404(
            StoryCanvas, id=canvas_id, project=project, deleted_at__isnull=True
        )

        new_name = request.query_params.get("new_name", f"{canvas.name} (Copy)")

        try:
            result = StoryCanvasService.duplicate_canvas(
                canvas=canvas, new_name=new_name
            )

            return Response(result, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": f"Failed to duplicate canvas: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CanvasTemplatesView(APIView):
    """Get available canvas templates."""

    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        """Get list of available canvas templates."""
        # Verify project exists
        get_object_or_404(Project, id=project_id)

        try:
            templates = StoryCanvasService.get_canvas_templates()
            serializer = CanvasTemplateSerializer(templates, many=True)

            return Response(
                {"canvas_templates": serializer.data}, status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": f"Failed to retrieve templates: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class StoryNodeListView(APIView):
    """List and create story nodes for a canvas."""

    permission_classes = [IsAuthenticated]

    def get(self, request, project_id, canvas_id):
        """List nodes in a canvas."""
        project = get_object_or_404(Project, id=project_id)
        canvas = get_object_or_404(
            StoryCanvas, id=canvas_id, project=project, deleted_at__isnull=True
        )

        # Get query parameters
        include_data = (
            request.query_params.get("include_data", "true").lower() == "true"
        )
        limit = int(request.query_params.get("limit", 100))
        offset = int(request.query_params.get("offset", 0))

        try:
            queryset = canvas.nodes.all()

            total_count = queryset.count()
            nodes = queryset[offset : offset + limit]

            serializer = StoryNodeSerializer(nodes, many=True)

            return Response(
                {
                    "nodes": serializer.data,
                    "pagination": {
                        "total": total_count,
                        "offset": offset,
                        "limit": limit,
                        "has_more": offset + len(serializer.data) < total_count,
                    },
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": f"Failed to retrieve nodes: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request, project_id, canvas_id):
        """Create a new story node."""
        project = get_object_or_404(Project, id=project_id)
        canvas = get_object_or_404(
            StoryCanvas, id=canvas_id, project=project, deleted_at__isnull=True
        )

        serializer = StoryNodeCreateSerializer(data=request.data, context={"project": project})
        if not serializer.is_valid():
            print("❌ Node creation validation failed:")
            print(f"Request data: {request.data}")
            print(f"Serializer errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = StoryNodeService.create_node(
                canvas=canvas, node_data=serializer.validated_data
            )

            return Response(result, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": f"Failed to create node: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class StoryNodeDetailView(APIView):
    """Get, update, and delete specific story nodes."""

    permission_classes = [IsAuthenticated]

    def get(self, request, project_id, canvas_id, node_id):
        """Get node details."""
        project = get_object_or_404(Project, id=project_id)
        canvas = get_object_or_404(
            StoryCanvas, id=canvas_id, project=project, deleted_at__isnull=True
        )
        node = get_object_or_404(StoryNode, id=node_id, canvas=canvas)

        try:
            serializer = StoryNodeSerializer(node)
            return Response({"node": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Failed to retrieve node: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, project_id, canvas_id, node_id):
        """Update node details."""
        project = get_object_or_404(Project, id=project_id)
        canvas = get_object_or_404(
            StoryCanvas, id=canvas_id, project=project, deleted_at__isnull=True
        )
        node = get_object_or_404(StoryNode, id=node_id, canvas=canvas)

        # Allow partial updates so clients can send only changed fields
        serializer = StoryNodeUpdateSerializer(instance=node, data=request.data, partial=True, context={"project": project})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = StoryNodeService.update_node(
                node=node, update_data=serializer.validated_data
            )

            return Response(result, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": f"Failed to update node: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, project_id, canvas_id, node_id):
        """Delete a node."""
        project = get_object_or_404(Project, id=project_id)
        canvas = get_object_or_404(
            StoryCanvas, id=canvas_id, project=project, deleted_at__isnull=True
        )
        node = get_object_or_404(StoryNode, id=node_id, canvas=canvas)

        try:
            result = StoryNodeService.delete_node(node)
            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Failed to delete node: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class NodeConnectionListView(APIView):
    """List and create node connections for a canvas."""

    permission_classes = [IsAuthenticated]

    def get(self, request, project_id, canvas_id):
        """List connections in a canvas."""
        project = get_object_or_404(Project, id=project_id)
        canvas = get_object_or_404(
            StoryCanvas, id=canvas_id, project=project, deleted_at__isnull=True
        )

        # Get query parameters
        connection_type = request.query_params.get("connection_type")
        source_node_id = request.query_params.get("source_node_id")
        target_node_id = request.query_params.get("target_node_id")
        limit = int(request.query_params.get("limit", 100))
        offset = int(request.query_params.get("offset", 0))

        try:
            queryset = canvas.connections.all()

            if connection_type:
                queryset = queryset.filter(connection_type=connection_type)
            if source_node_id:
                queryset = queryset.filter(source_node_id=source_node_id)
            if target_node_id:
                queryset = queryset.filter(target_node_id=target_node_id)

            total_count = queryset.count()
            connections = queryset[offset : offset + limit]

            serializer = NodeConnectionSerializer(connections, many=True)

            return Response(
                {
                    "connections": serializer.data,
                    "pagination": {
                        "total": total_count,
                        "offset": offset,
                        "limit": limit,
                        "has_more": offset + len(serializer.data) < total_count,
                    },
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": f"Failed to retrieve connections: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request, project_id, canvas_id):
        """Create a new node connection."""
        project = get_object_or_404(Project, id=project_id)
        canvas = get_object_or_404(
            StoryCanvas, id=canvas_id, project=project, deleted_at__isnull=True
        )

        serializer = NodeConnectionCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = NodeConnectionService.create_connection(
                canvas=canvas, connection_data=serializer.validated_data
            )

            return Response(result, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": f"Failed to create connection: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class NodeConnectionDetailView(APIView):
    """Get, update, and delete specific node connections."""

    permission_classes = [IsAuthenticated]

    def get(self, request, project_id, canvas_id, connection_id):
        """Get connection details."""
        project = get_object_or_404(Project, id=project_id)
        canvas = get_object_or_404(
            StoryCanvas, id=canvas_id, project=project, deleted_at__isnull=True
        )
        connection = get_object_or_404(NodeConnection, id=connection_id, canvas=canvas)

        try:
            serializer = NodeConnectionSerializer(connection)
            return Response({"connection": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Failed to retrieve connection: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, project_id, canvas_id, connection_id):
        """Update connection details."""
        project = get_object_or_404(Project, id=project_id)
        canvas = get_object_or_404(
            StoryCanvas, id=canvas_id, project=project, deleted_at__isnull=True
        )
        connection = get_object_or_404(NodeConnection, id=connection_id, canvas=canvas)

        serializer = NodeConnectionUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Update fields
            for field, value in serializer.validated_data.items():
                setattr(connection, field, value)
            connection.save()

            result_serializer = NodeConnectionSerializer(connection)
            return Response(
                {
                    "connection": result_serializer.data,
                    "message": "Connection updated successfully",
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": f"Failed to update connection: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, project_id, canvas_id, connection_id):
        """Delete a connection."""
        project = get_object_or_404(Project, id=project_id)
        canvas = get_object_or_404(
            StoryCanvas, id=canvas_id, project=project, deleted_at__isnull=True
        )
        connection = get_object_or_404(NodeConnection, id=connection_id, canvas=canvas)

        try:
            result = NodeConnectionService.delete_connection(connection)
            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Failed to delete connection: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


## StoryFlag endpoints removed


class CanvasTriggerView(APIView):
    """Canvas trigger management endpoint."""

    permission_classes = [IsAuthenticated]

    def get(self, request, project_id, canvas_id):
        """Get trigger for a canvas."""
        project = get_object_or_404(Project, id=project_id)
        canvas = get_object_or_404(
            StoryCanvas, id=canvas_id, project=project, deleted_at__isnull=True
        )

        try:
            trigger_data = CanvasTriggerService.get_canvas_trigger(canvas)

            # If trigger exists, compute availability details
            availability = None
            if trigger_data:
                try:
                    trigger_obj = CanvasTrigger.objects.get(canvas=canvas)
                    from .services.conditions import (
                        validate_conditions_schema,
                        evaluate_conditions,
                        schedule_active_now,
                        next_schedule_start,
                    )
                    conditions = trigger_obj.conditions or None
                    conditions_satisfied = False
                    details = []
                    if conditions and isinstance(conditions, dict) and conditions.get("version"):
                        try:
                            cleaned = validate_conditions_schema(conditions, project)
                            conditions_satisfied, details_objs = evaluate_conditions(project, cleaned)
                            details = [
                                {
                                    "index": d.index,
                                    "type": d.type,
                                    "satisfied": d.satisfied,
                                    "reason": d.reason,
                                }
                                for d in details_objs
                            ]
                        except Exception:
                            conditions_satisfied = False
                            details = []

                    sched_active = schedule_active_now(trigger_obj)
                    is_available = bool(trigger_obj.is_active and sched_active and (conditions is None or conditions_satisfied))
                    next_at = None if is_available else next_schedule_start(trigger_obj)
                    availability = {
                        "has_conditions": bool(conditions),
                        "condition_count": len((conditions or {}).get("items", [])) if conditions else 0,
                        "schedule_active_now": sched_active,
                        "conditions_satisfied_now": conditions_satisfied,
                        "is_available_now": is_available,
                        "next_available_at": next_at.isoformat() if next_at else None,
                        "evaluation_details": details,
                    }
                except Exception:
                    availability = None

            payload = {
                "canvas_id": str(canvas_id),
                "trigger": trigger_data,
                "has_trigger": trigger_data is not None,
            }
            if availability is not None:
                payload.update(availability)

            return Response(payload, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Failed to retrieve canvas trigger: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request, project_id, canvas_id):
        """Create a new trigger for a canvas."""
        project = get_object_or_404(Project, id=project_id)
        canvas = get_object_or_404(
            StoryCanvas, id=canvas_id, project=project, deleted_at__isnull=True
        )

        serializer = CanvasTriggerCreateSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = CanvasTriggerService.create_canvas_trigger(
                canvas, serializer.validated_data
            )

            # Return enriched GET response after creation
            return self.get(request, project_id, canvas_id)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": f"Failed to create canvas trigger: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, project_id, canvas_id):
        """Update an existing canvas trigger."""
        project = get_object_or_404(Project, id=project_id)
        canvas = get_object_or_404(
            StoryCanvas, id=canvas_id, project=project, deleted_at__isnull=True
        )

        try:
            trigger = CanvasTrigger.objects.get(canvas=canvas)
        except CanvasTrigger.DoesNotExist:
            return Response(
                {"error": "Canvas trigger not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = CanvasTriggerUpdateSerializer(
            trigger, data=request.data, partial=True
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = CanvasTriggerService.update_canvas_trigger(
                trigger, serializer.validated_data
            )

            # Return enriched GET response after update
            return self.get(request, project_id, canvas_id)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": f"Failed to update canvas trigger: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, project_id, canvas_id):
        """Delete a canvas trigger."""
        project = get_object_or_404(Project, id=project_id)
        canvas = get_object_or_404(
            StoryCanvas, id=canvas_id, project=project, deleted_at__isnull=True
        )

        try:
            trigger = CanvasTrigger.objects.get(canvas=canvas)
        except CanvasTrigger.DoesNotExist:
            return Response(
                {"error": "Canvas trigger not found"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            result = CanvasTriggerService.delete_canvas_trigger(trigger)
            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Failed to delete canvas trigger: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# BlockNote-specific API endpoints

class StoryNodeContentConversionView(APIView):
    """Convert legacy story node content to BlockNote blocks."""

    permission_classes = [IsAuthenticated]

    def post(self, request, project_id, canvas_id, node_id):
        """Convert legacy content to BlockNote blocks format."""

        # Get the node
        project = get_object_or_404(Project, id=project_id)
        canvas = get_object_or_404(
            StoryCanvas, id=canvas_id, project=project, deleted_at__isnull=True
        )
        node = get_object_or_404(StoryNode, id=node_id, canvas=canvas)

        try:
            # Get current node data
            node_data = node.node_data or {}

            # Check if already in block format
            if BlockConversionService._is_block_format(node_data):
                return Response({
                    "success": True,
                    "message": "Content is already in block format",
                    "blocks": node_data.get('blocks', []),
                    "version": node_data.get('version', '2.0'),
                    "content_stats": BlockConversionService.get_content_stats(
                        node_data.get('blocks', [])
                    ),
                    "preview_text": BlockConversionService.get_preview_text(
                        node_data.get('blocks', [])
                    )
                }, status=status.HTTP_200_OK)

            # Convert legacy content
            migrated_data = BlockConversionService.migrate_node_data(node_data)

            # Update the node with migrated data
            node.node_data = migrated_data
            node.save()

            # Generate response
            response_data = {
                "success": True,
                "message": "Content successfully converted to block format",
                "blocks": migrated_data['blocks'],
                "version": migrated_data['version'],
                "content_stats": BlockConversionService.get_content_stats(
                    migrated_data['blocks']
                ),
                "preview_text": BlockConversionService.get_preview_text(
                    migrated_data['blocks']
                )
            }

            serializer = ContentConversionResponseSerializer(data=response_data)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "success": False,
                "error": f"Failed to convert content: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StoryCanvasContentConversionView(APIView):
    """Batch convert all story nodes in a canvas to BlockNote format."""

    permission_classes = [IsAuthenticated]

    def post(self, request, project_id, canvas_id):
        """Convert all legacy content in canvas to BlockNote blocks format."""

        # Get the canvas
        project = get_object_or_404(Project, id=project_id)
        canvas = get_object_or_404(
            StoryCanvas, id=canvas_id, project=project, deleted_at__isnull=True
        )

        try:
            nodes = StoryNode.objects.filter(canvas=canvas)
            converted_count = 0
            skipped_count = 0
            errors = []

            for node in nodes:
                try:
                    node_data = node.node_data or {}

                    # Skip if already in block format
                    if BlockConversionService._is_block_format(node_data):
                        skipped_count += 1
                        continue

                    # Convert legacy content
                    migrated_data = BlockConversionService.migrate_node_data(node_data)

                    # Update the node
                    node.node_data = migrated_data
                    node.save()

                    converted_count += 1

                except Exception as e:
                    errors.append({
                        "node_id": str(node.id),
                        "node_name": node.name,
                        "error": str(e)
                    })

            return Response({
                "success": True,
                "message": "Conversion completed",
                "converted_count": converted_count,
                "skipped_count": skipped_count,
                "total_nodes": nodes.count(),
                "errors": errors
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "success": False,
                "error": f"Failed to convert canvas content: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StoryNodeValidationView(APIView):
    """Validate story node content with BlockNote validation service."""

    permission_classes = [IsAuthenticated]

    def post(self, request, project_id, canvas_id, node_id):
        """Validate a specific story node's content."""

        # Get the node
        project = get_object_or_404(Project, id=project_id)
        canvas = get_object_or_404(
            StoryCanvas, id=canvas_id, project=project, deleted_at__isnull=True
        )
        node = get_object_or_404(StoryNode, id=node_id, canvas=canvas)

        try:
            # Prepare validation data
            validation_data = {
                "name": node.name,
                "node_data": node.node_data or {},
                "tags": node.tags or []
            }

            # Validate using our service
            validation_result = BlockValidationService.validate_story_node(validation_data)

            # Format response
            response_data = {
                "is_valid": validation_result.is_valid,
                "errors": BlockValidationService.format_validation_errors(validation_result),
                "warnings": BlockValidationService.format_validation_warnings(validation_result)
            }

            serializer = BlockValidationResultSerializer(data=response_data)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "is_valid": False,
                "errors": [f"Validation failed: {str(e)}"],
                "warnings": []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StoryCanvasSaveView(APIView):
    """Save complete story content (nodes, connections, flags) atomically."""

    permission_classes = [IsAuthenticated]

    def post(self, request, project_id, canvas_id):
        """Save complete story content for a canvas."""
        project = get_object_or_404(Project, id=project_id)
        canvas = get_object_or_404(
            StoryCanvas, id=canvas_id, project=project, deleted_at__isnull=True
        )

        serializer = SaveStorySerializer(data=request.data, context={"project": project})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = StoryCanvasService.save_story_content(
                canvas=canvas,
                story_data=serializer.validated_data
            )

            # Format response using response serializer
            response_serializer = SaveStoryResponseSerializer(data=result)
            if response_serializer.is_valid():
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            else:
                # Fallback to raw result if serializer fails
                return Response(result, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": f"Failed to save story content: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class TriggerScheduleViewSet(viewsets.ModelViewSet):
    """ViewSet for managing trigger schedules"""

    queryset = TriggerSchedule.objects.all()
    serializer_class = TriggerScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter schedules by trigger if provided"""
        queryset = super().get_queryset().select_related('trigger__canvas')
        trigger_id = self.request.query_params.get('trigger_id')

        if trigger_id:
            queryset = queryset.filter(trigger_id=trigger_id)

        return queryset.order_by('start_time')

    def perform_create(self, serializer):
        """Handle schedule creation with additional business logic"""
        from .services.scheduling import TriggerScheduleService

        try:
            # Validate data using service (this also handles time format conversion)
            validated_data = TriggerScheduleService.validate_schedule_data(serializer.validated_data)
            # Save with validated data
            serializer.save(**validated_data)
        except ValidationError as e:
            # Re-raise validation errors for proper API response
            raise e

    @action(detail=False, methods=['post'])
    def create_multiple(self, request):
        """Create multiple schedules for a trigger at once"""
        serializer = TriggerScheduleCreateSerializer(data=request.data)

        if serializer.is_valid():
            result = serializer.save()
            return Response({
                'trigger_id': str(result['trigger_id']),
                'schedules': [TriggerScheduleSerializer(schedule).data for schedule in result['schedules']],
                'count': len(result['schedules'])
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def validate_schedule(self, request):
        """Validate schedule data without saving"""
        try:
            from .services.scheduling import TriggerScheduleService
            validated_data = TriggerScheduleService.validate_schedule_data(request.data)
            return Response({
                'valid': True,
                'validated_data': validated_data
            })
        except ValidationError as e:
            return Response({
                'valid': False,
                'errors': e.message_dict if hasattr(e, 'message_dict') else str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def active_now(self, request):
        """Get triggers that are currently active"""
        from datetime import datetime

        from .services.scheduling import TriggerScheduleService

        now = datetime.now()
        current_weekday = now.weekday()
        current_time = now.time()

        active_triggers = TriggerScheduleService.get_active_triggers_at(current_weekday, current_time)

        # Format trigger data for response
        trigger_data = []
        for trigger in active_triggers:
            trigger_data.append({
                'id': str(trigger.id),
                'canvas_name': trigger.canvas.name,
                'is_activity': trigger.is_activity,
                'is_repeatable': trigger.is_repeatable
            })

        return Response(ActiveTriggersSerializer({
            'current_weekday': current_weekday,
            'current_time': current_time,
            'active_triggers': trigger_data
        }).data)

    @action(detail=True, methods=['get'])
    def preview(self, request, pk=None):
        """Preview when a schedule will fire over the next week"""
        from .services.scheduling import TriggerScheduleService

        days_ahead = int(request.query_params.get('days', 7))
        preview_data = TriggerScheduleService.preview_trigger_schedule(pk, days_ahead)

        return Response({
            'schedule_id': pk,
            'days_ahead': days_ahead,
            'preview': preview_data
        })

    @action(detail=False, methods=['get'])
    def conflicts(self, request):
        """Check for scheduling conflicts for a trigger"""
        from .services.scheduling import TriggerScheduleService

        trigger_id = request.query_params.get('trigger_id')
        if not trigger_id:
            return Response({
                'error': 'trigger_id parameter is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            conflicts = TriggerScheduleService.get_schedule_conflicts(trigger_id)
            return Response({
                'trigger_id': trigger_id,
                'conflicts': conflicts,
                'has_conflicts': len(conflicts) > 0
            })
        except Exception as e:
            return Response({
                'error': f'Failed to check conflicts: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TriggerScheduleListView(APIView):
    """List and create trigger schedules for a canvas trigger (nested endpoint)."""

    permission_classes = [IsAuthenticated]

    def get(self, request, project_id, canvas_id):
        """List schedules for a canvas trigger."""
        project = get_object_or_404(Project, id=project_id)
        canvas = get_object_or_404(
            StoryCanvas, id=canvas_id, project=project, deleted_at__isnull=True
        )

        try:
            # Get the canvas trigger
            trigger = get_object_or_404(CanvasTrigger, canvas=canvas)

            # Get all schedules for this trigger
            schedules = trigger.schedules.all().order_by('start_time')

            # Serialize schedules
            serializer = TriggerScheduleSerializer(schedules, many=True)

            return Response({
                'schedules': serializer.data,
                'total_count': len(serializer.data),
                'canvas_id': str(canvas_id),
                'trigger_id': str(trigger.id)
            }, status=status.HTTP_200_OK)

        except CanvasTrigger.DoesNotExist:
            return Response({
                'schedules': [],
                'total_count': 0,
                'canvas_id': str(canvas_id),
                'trigger_id': None,
                'message': 'No trigger found for this canvas'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Failed to retrieve schedules: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request, project_id, canvas_id):
        """Create a new schedule for a canvas trigger."""
        project = get_object_or_404(Project, id=project_id)
        canvas = get_object_or_404(
            StoryCanvas, id=canvas_id, project=project, deleted_at__isnull=True
        )

        try:
            # Get the canvas trigger
            trigger = get_object_or_404(CanvasTrigger, canvas=canvas)

            # Validate schedule data
            from .services.scheduling import TriggerScheduleService

            schedule_data = request.data.copy()

            try:
                # Create the schedule using the service
                schedule = TriggerScheduleService.create_schedule(trigger, schedule_data)

                # Serialize the created schedule
                serializer = TriggerScheduleSerializer(schedule)

                return Response({
                    'schedule': serializer.data,
                    'message': 'Schedule created successfully'
                }, status=status.HTTP_201_CREATED)

            except ValidationError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except CanvasTrigger.DoesNotExist:
            return Response(
                {"error": "Canvas trigger not found. Create a trigger first."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return Response(
                {"error": f"Failed to create schedule: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CanvasTriggerCheckView(APIView):
    """Evaluate trigger availability and conditions on-demand."""

    permission_classes = [IsAuthenticated]

    def post(self, request, project_id, canvas_id):
        project = get_object_or_404(Project, id=project_id)
        canvas = get_object_or_404(
            StoryCanvas, id=canvas_id, project=project, deleted_at__isnull=True
        )
        try:
            trigger = CanvasTrigger.objects.get(canvas=canvas)
        except CanvasTrigger.DoesNotExist:
            return Response({"error": "Canvas trigger not found"}, status=status.HTTP_404_NOT_FOUND)

        from .services.conditions import (
            validate_conditions_schema,
            evaluate_conditions,
            schedule_active_now,
            next_schedule_start,
        )

        conditions = trigger.conditions or None
        cleaned = None
        cond_ok = False
        details = []
        if conditions and isinstance(conditions, dict) and conditions.get("version"):
            try:
                cleaned = validate_conditions_schema(conditions, project)
                cond_ok, details_objs = evaluate_conditions(project, cleaned)
                details = [
                    {"index": d.index, "type": d.type, "satisfied": d.satisfied, "reason": d.reason}
                    for d in details_objs
                ]
            except Exception:
                cleaned = None
                cond_ok = False
                details = []

        sched_active = schedule_active_now(trigger)
        is_available = bool(trigger.is_active and sched_active and (cleaned is None or cond_ok))
        next_at = None if is_available else next_schedule_start(trigger)

        return Response(
            {
                "has_conditions": bool(cleaned),
                "condition_count": len((cleaned or {}).get("items", [])) if cleaned else 0,
                "schedule_active_now": sched_active,
                "conditions_satisfied_now": cond_ok,
                "is_available_now": is_available,
                "next_available_at": next_at.isoformat() if next_at else None,
                "evaluation_details": details,
            },
            status=status.HTTP_200_OK,
        )


## Global flags endpoint removed (using per-entity flag_keys)


class TriggerOptionsCharactersView(APIView):
    """List player and NPCs trait keys for dropdowns."""

    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        # Player
        from apps.characters.models import Character
        try:
            player = Character.objects.get(project=project)
            player_traits = list((player.core_traits or {}).keys())
            player_flags = list((player.flag_keys or []))
            player_obj = {"id": str(player.id), "name": player.name, "trait_keys": player_traits, "flag_keys": player_flags}
        except Character.DoesNotExist:
            player_obj = None

        # NPCs
        from apps.npcs.models import NPC
        npcs = (
            NPC.objects.filter(project=project, deleted_at__isnull=True)
            .order_by("name")
        )
        npc_list = []
        for n in npcs:
            npc_list.append(
                {
                    "id": str(n.id),
                    "name": n.name,
                    "trait_keys": list((n.core_traits or {}).keys()),
                    "flag_keys": list((n.flag_keys or [])),
                }
            )

        return Response({"player": player_obj, "npcs": npc_list}, status=status.HTTP_200_OK)


class ProjectMediaListView(APIView):
    """List media assets for a project (optional filter by kind)."""

    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        kind = request.query_params.get("kind")
        q = request.query_params.get("q")
        limit = int(request.query_params.get("limit", 50))
        offset = int(request.query_params.get("offset", 0))

        qs = MediaAsset.objects.filter(project=project)
        if kind in {MediaKind.IMAGE, MediaKind.VIDEO, MediaKind.GIF}:
            qs = qs.filter(kind=kind)
        if q:
            qs = qs.filter(file__icontains=q)

        total = qs.count()
        items = qs.order_by("-created_at")[offset : offset + limit]
        data = MediaAssetSerializer(items, many=True).data
        return Response(
            {
                "items": data,
                "pagination": {
                    "total": total,
                    "offset": offset,
                    "limit": limit,
                    "has_more": offset + len(data) < total,
                },
            },
            status=status.HTTP_200_OK,
        )


class ProjectMediaUploadView(APIView):
    """Upload a media asset (image, video, gif) for a project."""

    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)

        uploaded = request.FILES.get("file")
        if not uploaded:
            return Response({"error": "Missing file"}, status=status.HTTP_400_BAD_REQUEST)

        # Determine kind from query or content type
        kind_param = request.query_params.get("kind")
        content_type = getattr(uploaded, "content_type", "") or request.META.get("CONTENT_TYPE", "")
        size_bytes = getattr(uploaded, "size", None) or uploaded.size

        def infer_kind(ct: str):
            if ct.startswith("image/"):
                if ct == "image/gif":
                    return MediaKind.GIF
                return MediaKind.IMAGE
            if ct.startswith("video/"):
                return MediaKind.VIDEO
            return None

        if kind_param in {MediaKind.IMAGE, MediaKind.VIDEO, MediaKind.GIF}:
            kind = kind_param
        else:
            kind = infer_kind(content_type)

        if not kind:
            return Response({"error": f"Unsupported content type: {content_type}"}, status=status.HTTP_400_BAD_REQUEST)

        # Basic size limits (configurable)
        max_image = 20 * 1024 * 1024
        max_video = 500 * 1024 * 1024
        if kind in {MediaKind.IMAGE, MediaKind.GIF} and size_bytes > max_image:
            return Response({"error": "Image too large (max 20MB)"}, status=status.HTTP_400_BAD_REQUEST)
        if kind == MediaKind.VIDEO and size_bytes > max_video:
            return Response({"error": "Video too large (max 500MB)"}, status=status.HTTP_400_BAD_REQUEST)

        asset = MediaAsset(
            project=project,
            kind=kind,
            mime_type=content_type or "application/octet-stream",
            size_bytes=size_bytes or 0,
            uploaded_by=request.user if request.user.is_authenticated else None,
        )
        asset.file = uploaded

        # Optional metadata extraction
        if kind in {MediaKind.IMAGE, MediaKind.GIF}:
            try:
                from PIL import Image  # type: ignore

                uploaded.seek(0)
                with Image.open(uploaded) as im:
                    asset.width, asset.height = im.size
            except Exception:
                pass

        # Save first to get URL
        asset.save()

        # Attempt poster extraction for videos (best-effort; skip if unavailable)
        if kind == MediaKind.VIDEO:
            try:
                # Placeholder for optional poster generation using ffmpeg
                pass
            except Exception:
                pass

        return Response(asset.to_dict(), status=status.HTTP_201_CREATED)


class ExitChoicesCheckView(APIView):
    """Evaluate per-choice conditions for a node's Exit Block (choices type)."""

    permission_classes = [IsAuthenticated]

    def post(self, request, project_id, canvas_id, node_id):
        project = get_object_or_404(Project, id=project_id)
        canvas = get_object_or_404(
            StoryCanvas, id=canvas_id, project=project, deleted_at__isnull=True
        )
        node = get_object_or_404(StoryNode, id=node_id, canvas=canvas)

        exit_block = node.exit_block or {}
        if not isinstance(exit_block, dict) or exit_block.get("type") != "choices":
            return Response(
                {"error": "Exit block is not of type 'choices'"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        from .services.conditions import validate_conditions_schema, evaluate_conditions

        choices = exit_block.get("choices", []) or []
        results = []
        for idx, choice in enumerate(choices):
            try:
                cond = (choice or {}).get("conditions")
                has_conditions = bool(cond and isinstance(cond, dict) and cond.get("version"))
                if has_conditions:
                    cleaned = validate_conditions_schema(cond, project)
                    satisfied, details_objs = evaluate_conditions(project, cleaned)
                    details = [
                        {
                            "index": d.index,
                            "type": d.type,
                            "satisfied": d.satisfied,
                            "reason": d.reason,
                        }
                        for d in details_objs
                    ]
                else:
                    satisfied = True
                    details = []

                results.append(
                    {
                        "index": idx,
                        "has_conditions": has_conditions,
                        "conditions_satisfied_now": bool(satisfied),
                        "available": bool(satisfied),
                        "evaluation_details": details,
                    }
                )
            except Exception as e:
                results.append(
                    {
                        "index": idx,
                        "has_conditions": bool((choice or {}).get("conditions")),
                        "conditions_satisfied_now": False,
                        "available": False,
                        "evaluation_details": [{"index": -1, "type": "error", "satisfied": False, "reason": str(e)}],
                    }
                )

        from datetime import datetime
        return Response(
            {"choices": results, "evaluated_at": datetime.now().isoformat()},
            status=status.HTTP_200_OK,
        )
