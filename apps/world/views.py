"""
World Designer API views for location and connection management.

Provides RESTful endpoints matching the FastAPI backend functionality.
"""

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.projects.models import Project

from .models import Location
from django.core.exceptions import ValidationError
from .serializers import (
    LocationCreateSerializer,
    LocationNestSerializer,
    LocationSerializer,
    LocationUnnestSerializer,
    LocationUpdateSerializer,
)


class WorldOverviewView(APIView):
    """
    Handle GET operations for world overview.

    GET /api/v1/projects/{id}/world/ - Get complete world data
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        """Get complete world overview with locations and connections."""
        try:
            # Verify project exists and user has access
            project = get_object_or_404(Project, id=project_id, owner=request.user)

            # Get all locations for this project (no M2M prefetch needed)
            locations = Location.objects.filter(project=project).order_by("created_at")

            # Serialize locations
            location_data = LocationSerializer(locations, many=True).data

            # Derive connections from simplified entry_from field + default entry hint
            derived_connections = []
            for loc in locations:
                # Entry-from edge (from -> loc)
                if getattr(loc, "entry_from", None):
                    derived_connections.append(
                        {
                            "id": f"{loc.entry_from.id}__to__{loc.id}",
                            "from_location_id": str(loc.entry_from.id),
                            "to_location_id": str(loc.id),
                            "connection_type": "path",
                            "distance": 1.0,
                            "travel_time": 1,
                            "difficulty": "1",
                            "is_bidirectional": False,
                            "requires_unlock": False,
                            "properties": {},
                            "from_handle_position": "top",
                            "to_handle_position": "top",
                            "requires_key": False,
                            "line_style": "solid",
                            "line_color": "#3b82f6",
                            "arrow_style": "unidirectional",
                        }
                    )

                # Default entry hint edge (container -> default child)
                if getattr(loc, "is_container", False) and getattr(loc, "default_entry_location", None):
                    child = loc.default_entry_location
                    derived_connections.append(
                        {
                            "id": f"{loc.id}__default__{child.id}",
                            "from_location_id": str(loc.id),
                            "to_location_id": str(child.id),
                            "connection_type": "default_entry",
                            "distance": 1.0,
                            "travel_time": 1,
                            "difficulty": "1",
                            "is_bidirectional": False,
                            "requires_unlock": False,
                            "properties": {"kind": "default_entry"},
                            "from_handle_position": "top",
                            "to_handle_position": "top",
                            "requires_key": False,
                            "line_style": "dotted",
                            "line_color": "#8b5cf6",
                            "arrow_style": "unidirectional",
                        }
                    )

            # Get canvas state from project settings
            canvas_state = (
                project.settings.get(
                    "canvas_state",
                    {
                        "zoom": 1.0,
                        "pan_x": 0.0,
                        "pan_y": 0.0,
                        "grid_enabled": True,
                        "snap_to_grid": True,
                        "grid_size": 20,
                    },
                )
                if project.settings
                else {
                    "zoom": 1.0,
                    "pan_x": 0.0,
                    "pan_y": 0.0,
                    "grid_enabled": True,
                    "snap_to_grid": True,
                    "grid_size": 20,
                }
            )

            # Find starting location
            starting_location_id = None
            for location in locations:
                if location.is_starting_location:
                    starting_location_id = str(location.id)
                    break

            # Build world metadata
            world_metadata = {
                "last_modified": project.updated_at.isoformat(),
                "total_area": len(location_data),
                "connection_density": len(derived_connections) / max(len(location_data), 1),
            }

            response_data = {
                "project_id": str(project.id),
                "locations": location_data,
                "connections": derived_connections,
                "canvas_state": canvas_state,
                "world_metadata": world_metadata,
                "location_count": len(location_data),
                "connection_count": len(derived_connections),
                "starting_location_id": starting_location_id,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Failed to retrieve world data: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LocationListCreateView(APIView):
    """
    Handle GET (list) and POST (create) operations for locations.

    POST /api/v1/projects/{id}/world/locations - Create location
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):
        """Create a new location in the project world."""
        try:
            # Verify project exists and user has access
            project = get_object_or_404(Project, id=project_id, owner=request.user)

            # Validate and create location
            serializer = LocationCreateSerializer(data=request.data)

            if serializer.is_valid():
                with transaction.atomic():
                    # Calculate hierarchy level and relative positioning
                    parent_location = serializer.validated_data.get("parent_location")

                    if parent_location:
                        # Validate parent exists and belongs to same project
                        if parent_location.project != project:
                            return Response(
                                {
                                    "error": "Parent location must belong to the same project"
                                },
                                status=status.HTTP_400_BAD_REQUEST,
                            )

                        if not parent_location.is_container:
                            return Response(
                                {"error": "Parent location is not a container"},
                                status=status.HTTP_400_BAD_REQUEST,
                            )

                        # Set hierarchy level
                        hierarchy_level = parent_location.hierarchy_level + 1
                        if hierarchy_level > 20:
                            return Response(
                                {"error": "Maximum nesting depth exceeded (20 levels)"},
                                status=status.HTTP_400_BAD_REQUEST,
                            )

                    # Create the location
                    location = serializer.save(project=project)

                    # Return the created location
                    response_serializer = LocationSerializer(location)
                    return Response(
                        response_serializer.data, status=status.HTTP_201_CREATED
                    )
            else:
                return Response(
                    {"error": "Validation failed", "details": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            return Response(
                {"error": f"Failed to create location: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LocationDetailView(APIView):
    """
    Handle GET, PUT, and DELETE operations for individual locations.

    GET /api/v1/projects/{project_id}/world/locations/{id}/ - Retrieve location
    PUT /api/v1/projects/{project_id}/world/locations/{id}/ - Update location
    DELETE /api/v1/projects/{project_id}/world/locations/{id}/ - Delete location
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, project_id, location_id, user):
        """Get location by ID, ensuring it belongs to the user's project."""
        return get_object_or_404(
            Location, id=location_id, project__id=project_id, project__owner=user
        )

    def get(self, request, project_id, location_id):
        """Retrieve a specific location."""
        try:
            location = self.get_object(project_id, location_id, request.user)
            serializer = LocationSerializer(location)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Failed to retrieve location: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, project_id, location_id):
        """Update a specific location."""
        try:
            location = self.get_object(project_id, location_id, request.user)

            serializer = LocationUpdateSerializer(
                location, data=request.data, partial=True
            )

            if serializer.is_valid():
                with transaction.atomic():
                    # Handle parent location changes
                    parent_location = serializer.validated_data.get("parent_location")
                    if parent_location:
                        # Validate parent belongs to same project
                        if parent_location.project != location.project:
                            return Response(
                                {
                                    "error": "Parent location must belong to the same project"
                                },
                                status=status.HTTP_400_BAD_REQUEST,
                            )

                    updated_location = serializer.save()

                    # Return the updated location
                    response_serializer = LocationSerializer(updated_location)
                    return Response(response_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Validation failed", "details": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            return Response(
                {"error": f"Failed to update location: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, project_id, location_id):
        """Delete a specific location."""
        try:
            location = self.get_object(project_id, location_id, request.user)

            with transaction.atomic():
                # Check if location has children
                if location.child_locations.exists():
                    return Response(
                        {
                            "error": "Cannot delete location that contains other locations"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Delete the location (connections will be cascaded)
                location.delete()

                return Response(
                    {"message": "Location deleted successfully"},
                    status=status.HTTP_200_OK,
                )

        except Exception as e:
            return Response(
                {"error": f"Failed to delete location: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LocationNestView(APIView):
    """
    Handle POST operations for nesting locations into containers.

    POST /api/v1/projects/{project_id}/world/locations/{id}/nest - Nest location
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id, location_id):
        """Nest location into container."""
        try:
            # Get the location to be nested
            location = get_object_or_404(
                Location,
                id=location_id,
                project__id=project_id,
                project__owner=request.user,
            )

            serializer = LocationNestSerializer(data=request.data)

            if serializer.is_valid():
                container_id = serializer.validated_data["container_id"]

                # Get container location
                container = get_object_or_404(
                    Location, id=container_id, project=location.project
                )

                if not container.is_container:
                    return Response(
                        {"error": "Target location is not a container"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Prevent circular nesting
                if container.id == location.id:
                    return Response(
                        {"error": "Location cannot be nested into itself"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Check nesting depth
                new_hierarchy_level = container.hierarchy_level + 1
                if new_hierarchy_level > 20:
                    return Response(
                        {"error": "Maximum nesting depth exceeded (20 levels)"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                with transaction.atomic():
                    # Update location's parent and hierarchy
                    location.parent_location = container
                    location.hierarchy_level = new_hierarchy_level
                    # Keep current canvas position as relative position
                    location.relative_x = location.canvas_x
                    location.relative_y = location.canvas_y
                    location.save()

                    # Return updated location
                    response_serializer = LocationSerializer(location)
                    return Response(response_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Validation failed", "details": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            return Response(
                {"error": f"Failed to nest location: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LocationUnnestView(APIView):
    """
    Handle POST operations for unnesting locations from containers.

    POST /api/v1/projects/{project_id}/world/locations/{id}/unnest - Unnest location
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id, location_id):
        """Remove location from container."""
        try:
            # Get the location to be unnested
            location = get_object_or_404(
                Location,
                id=location_id,
                project__id=project_id,
                project__owner=request.user,
            )

            if not location.parent_location:
                return Response(
                    {"error": "Location is not nested in a container"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = LocationUnnestSerializer(data=request.data)

            if serializer.is_valid():
                x = serializer.validated_data["x"]
                y = serializer.validated_data["y"]

                with transaction.atomic():
                    # Remove from container
                    location.parent_location = None
                    location.hierarchy_level = 0
                    location.canvas_x = x
                    location.canvas_y = y
                    location.relative_x = x
                    location.relative_y = y
                    location.save()

                    # Return updated location
                    response_serializer = LocationSerializer(location)
                    return Response(response_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Validation failed", "details": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            return Response(
                {"error": f"Failed to unnest location: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# Deprecated ConnectionListCreateView and ConnectionDetailView removed


class LocationEntryFromView(APIView):
    """
    Set or clear the single inbound entry point for a location.

    PUT /api/v1/projects/{project_id}/world/locations/{location_id}/entry-from
    DELETE /api/v1/projects/{project_id}/world/locations/{location_id}/entry-from
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, project_id, location_id):
        try:
            target = get_object_or_404(
                Location,
                id=location_id,
                project__id=project_id,
                project__owner=request.user,
            )
            from_id = request.data.get("from_location_id")
            if not from_id:
                return Response(
                    {"error": "from_location_id is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            source = get_object_or_404(Location, id=from_id, project=target.project)
            if target.id == source.id:
                return Response(
                    {"error": "entry_from cannot point to self"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            target.entry_from = source
            target.save()
            return Response(
                {"message": "entry_from set", "to": str(target.id), "from": str(source.id)},
                status=status.HTTP_200_OK,
            )
        except ValidationError as e:
            details = getattr(e, "message_dict", None) or getattr(e, "messages", None) or str(e)
            return Response(
                {"error": "Validation failed", "details": details},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to set entry_from: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, project_id, location_id):
        try:
            target = get_object_or_404(
                Location,
                id=location_id,
                project__id=project_id,
                project__owner=request.user,
            )
            target.entry_from = None
            target.save()
            return Response({"message": "entry_from cleared"}, status=status.HTTP_200_OK)
        except ValidationError as e:
            details = getattr(e, "message_dict", None) or getattr(e, "messages", None) or str(e)
            return Response(
                {"error": "Validation failed", "details": details},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to clear entry_from: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LocationDefaultEntryView(APIView):
    """
    Set or clear the default entry location for a container.

    PUT /api/v1/projects/{project_id}/world/locations/{location_id}/default-entry
    DELETE /api/v1/projects/{project_id}/world/locations/{location_id}/default-entry
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, project_id, location_id):
        try:
            container = get_object_or_404(
                Location,
                id=location_id,
                project__id=project_id,
                project__owner=request.user,
            )
            if not container.is_container:
                return Response(
                    {"error": "Location is not a container"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            entry_id = request.data.get("entry_location_id")
            if not entry_id:
                return Response(
                    {"error": "entry_location_id is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            entry_loc = get_object_or_404(Location, id=entry_id, project=container.project)

            # Ensure the entry location is a child of the container
            if entry_loc.parent_location_id != container.id:
                return Response(
                    {"error": "Default entry must be a direct child of the container"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Apply changes atomically
            with transaction.atomic():
                # Ensure the chosen default entry location itself has no entry_from
                if entry_loc.entry_from is not None:
                    entry_loc.entry_from = None
                    entry_loc.save()

                # Do not clear container.entry_from; containers may have
                # entry_from even when default_entry is set (descendant rule
                # is enforced by model validation).

                container.default_entry_location = entry_loc
                container.save()
            return Response(
                {"message": "Default entry set", "container": str(container.id), "entry": str(entry_loc.id)},
                status=status.HTTP_200_OK,
            )
        except ValidationError as e:
            details = getattr(e, "message_dict", None) or getattr(e, "messages", None) or str(e)
            return Response(
                {"error": "Validation failed", "details": details},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to set default entry: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, project_id, location_id):
        try:
            container = get_object_or_404(
                Location,
                id=location_id,
                project__id=project_id,
                project__owner=request.user,
            )
            container.default_entry_location = None
            container.save()
            return Response({"message": "Default entry cleared"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Failed to clear default entry: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
