"""
Character Management API views.

Provides RESTful API endpoints for character CRUD operations,
trait management, and template generation.
"""

import uuid

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.projects.models import Project

from .models import Character
from .serializers import (
    CharacterCreateSerializer,
    CharacterDetailSerializer,
    CharacterLocationSerializer,
    CharacterRelationshipSerializer,
    CharacterTraitsSerializer,
    CharacterUpdateSerializer,
)
from .services import CharacterService


class PlayerCharacterView(APIView):
    """Single player character endpoint for project."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        """Get the player character for the project."""
        try:
            # Get and verify project ownership
            project = get_object_or_404(Project, id=project_id, owner=request.user)

            # Try to get the player character
            try:
                character = project.player_character
                serializer = CharacterDetailSerializer(character)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Character.DoesNotExist:
                # Return 204 No Content when no character exists (expected state)
                return Response(status=status.HTTP_204_NO_CONTENT)

        except Project.DoesNotExist:
            return Response(
                {"error": "Project not found or access denied"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to fetch player character: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request, project_id):
        """Create the player character for the project."""
        try:
            # Get and verify project ownership
            project = get_object_or_404(Project, id=project_id, owner=request.user)

            # Check if character already exists
            try:
                existing_character = project.player_character
                return Response(
                    {"error": "Player character already exists for this project"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except Character.DoesNotExist:
                pass  # Character doesn't exist, we can create one

            # Validate character data
            serializer = CharacterCreateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {"error": "Invalid character data", "details": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Use service layer to create character
            character = CharacterService.create_character(
                project, serializer.validated_data, request.user
            )

            # Return created character
            response_serializer = CharacterDetailSerializer(character)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Project.DoesNotExist:
            return Response(
                {"error": "Project not found or access denied"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to create character: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, project_id):
        """Update the player character for the project."""
        try:
            # Get and verify project ownership
            project = get_object_or_404(Project, id=project_id, owner=request.user)

            # Get the player character
            try:
                character = project.player_character
            except Character.DoesNotExist:
                # Return 204 No Content when no character exists (expected state)
                return Response(status=status.HTTP_204_NO_CONTENT)

            # Validate update data
            serializer = CharacterUpdateSerializer(
                character, data=request.data, partial=True
            )
            if not serializer.is_valid():
                return Response(
                    {"error": "Invalid character data", "details": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Use service layer to update character
            updated_character = CharacterService.update_character(
                character, serializer.validated_data, request.user
            )

            # Return updated character
            response_serializer = CharacterDetailSerializer(updated_character)
            return Response(response_serializer.data, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Project.DoesNotExist:
            return Response(
                {"error": "Project not found or access denied"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to update character: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PlayerCharacterCreateView(APIView):
    """Player character creation endpoint."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):
        """Create the player character for the project."""
        try:
            # Get and verify project ownership
            project = get_object_or_404(Project, id=project_id, owner=request.user)

            # Check if character already exists
            try:
                existing_character = project.player_character
                return Response(
                    {"error": "Player character already exists for this project"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except Character.DoesNotExist:
                pass  # Character doesn't exist, we can create one

            # Validate character data
            serializer = CharacterCreateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {"error": "Invalid character data", "details": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Use service layer to create character
            character = CharacterService.create_character(
                project, serializer.validated_data, request.user
            )

            # Return created character
            response_serializer = CharacterDetailSerializer(character)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Project.DoesNotExist:
            return Response(
                {"error": "Project not found or access denied"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to create character: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PlayerCharacterUpdateView(APIView):
    """Player character update endpoint."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, project_id):
        """Update the player character for the project."""
        try:
            # Get and verify project ownership
            project = get_object_or_404(Project, id=project_id, owner=request.user)

            # Get the player character
            try:
                character = project.player_character
            except Character.DoesNotExist:
                # Return 204 No Content when no character exists (expected state)
                return Response(status=status.HTTP_204_NO_CONTENT)

            # Validate update data
            serializer = CharacterUpdateSerializer(
                character, data=request.data, partial=True
            )
            if not serializer.is_valid():
                return Response(
                    {"error": "Invalid character data", "details": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Use service layer to update character
            updated_character = CharacterService.update_character(
                character, serializer.validated_data, request.user
            )

            # Return updated character
            response_serializer = CharacterDetailSerializer(updated_character)
            return Response(response_serializer.data, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Project.DoesNotExist:
            return Response(
                {"error": "Project not found or access denied"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to update character: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PlayerCharacterTraitsView(APIView):
    """Player character traits update endpoint."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):
        """Update player character traits."""
        try:
            # Get and verify project ownership
            project = get_object_or_404(Project, id=project_id, owner=request.user)

            # Get the player character
            try:
                character = project.player_character
            except Character.DoesNotExist:
                # Return 204 No Content when no character exists (expected state)
                return Response(status=status.HTTP_204_NO_CONTENT)

            # Validate traits data
            serializer = CharacterTraitsSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {"error": "Invalid traits data", "details": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Use service layer to update traits
            result = CharacterService.update_character_traits(
                character, serializer.validated_data, request.user
            )

            return Response({"success": True, **result}, status=status.HTTP_200_OK)

        except Project.DoesNotExist:
            return Response(
                {"error": "Project not found or access denied"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to update character traits: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PlayerCharacterLocationView(APIView):
    """Player character location assignment endpoint."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):
        """Update player character location assignments."""
        try:
            # Get and verify project ownership
            project = get_object_or_404(Project, id=project_id, owner=request.user)

            # Get the player character
            try:
                character = project.player_character
            except Character.DoesNotExist:
                # Return 204 No Content when no character exists (expected state)
                return Response(status=status.HTTP_204_NO_CONTENT)

            # Validate location data
            serializer = CharacterLocationSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {"error": "Invalid location data", "details": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Use service layer to update location
            result = CharacterService.update_character_location(
                character, serializer.validated_data, request.user
            )

            return Response({"success": True, **result}, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Project.DoesNotExist:
            return Response(
                {"error": "Project not found or access denied"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to update character location: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CharacterRelationshipsView(APIView):
    """Character relationships update endpoint."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id, character_id):
        """Update character relationships."""
        try:
            # Validate UUID format
            try:
                uuid.UUID(character_id)
            except ValueError:
                return Response(
                    {"error": "Invalid character ID format"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Get and verify project ownership
            project = get_object_or_404(Project, id=project_id, owner=request.user)

            # Get character
            character = CharacterService.get_character_by_id(character_id, project)
            if not character:
                return Response(
                    {"error": "Character not found"}, status=status.HTTP_404_NOT_FOUND
                )

            # Validate relationships data
            serializer = CharacterRelationshipSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {
                        "error": "Invalid relationships data",
                        "details": serializer.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Use service layer to update relationships
            result = CharacterService.update_character_relationships(
                character, serializer.validated_data, request.user
            )

            return Response({"success": True, **result}, status=status.HTTP_200_OK)

        except Project.DoesNotExist:
            return Response(
                {"error": "Project not found or access denied"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to update character relationships: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CharacterTemplatesView(APIView):
    """Character templates and presets endpoint."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        """Get character creation templates and presets."""
        try:
            # Get and verify project ownership
            project = get_object_or_404(Project, id=project_id, owner=request.user)

            # Use service layer to get templates
            templates = CharacterService.get_character_templates()
            return Response(templates, status=status.HTTP_200_OK)

        except Project.DoesNotExist:
            return Response(
                {"error": "Project not found or access denied"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to fetch character templates: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
