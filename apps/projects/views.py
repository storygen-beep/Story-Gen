"""
Project API views for CRUD operations.

Provides RESTful endpoints matching FastAPI backend functionality.
"""

from django.core.paginator import Paginator
from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.game_generation.services.game_service import GameService

from .models import Project
from .serializers import (
    ProjectCreateSerializer,
    ProjectSerializer,
    ProjectSettingsSerializer,
    ProjectSettingsUpdateSerializer,
    ProjectUpdateSerializer,
)


class ProjectListCreateView(APIView):
    """
    Handle GET (list) and POST (create) operations for projects.

    GET /api/v1/foundation/projects/ - List user's projects with pagination
    POST /api/v1/foundation/projects/ - Create new project
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        List projects for the authenticated user.

        Query parameters:
        - page: Page number (default: 1)
        - per_page: Items per page (default: 50, max: 100)
        - status: Filter by status (optional)
        """
        try:
            # Get query parameters
            page = int(request.query_params.get("page", 1))
            per_page = min(int(request.query_params.get("per_page", 50)), 100)
            status_filter = request.query_params.get("status")

            # Build queryset
            queryset = (
                Project.objects.filter(owner=request.user)
                .exclude(deleted_at__isnull=False)  # Exclude soft-deleted projects
                .order_by("-created_at")
            )

            # Apply status filter if provided
            if status_filter:
                queryset = queryset.filter(status=status_filter)

            # Apply pagination
            paginator = Paginator(queryset, per_page)

            # Validate page number
            if page > paginator.num_pages and paginator.num_pages > 0:
                page = paginator.num_pages

            projects_page = paginator.get_page(page)

            # Serialize projects
            project_serializer = ProjectSerializer(projects_page.object_list, many=True)

            # Prepare response data
            response_data = {
                "projects": project_serializer.data,
                "total": paginator.count,
                "page": page,
                "per_page": per_page,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except ValueError:
            return Response(
                {"error": "Invalid page or per_page parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to retrieve projects: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):
        """
        Create a new project for the authenticated user.

        Expected request body matches frontend ProjectCreateData interface.
        """
        try:
            serializer = ProjectCreateSerializer(
                data=request.data, context={"request": request}
            )

            if serializer.is_valid():
                project = serializer.save()

                # Return the created project in the expected format
                response_serializer = ProjectSerializer(project)
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
                {"error": f"Failed to create project: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ProjectDetailView(APIView):
    """
    Handle GET, PUT, and DELETE operations for individual projects.

    GET /api/v1/foundation/projects/{id}/ - Retrieve project
    PUT /api/v1/foundation/projects/{id}/ - Update project
    DELETE /api/v1/foundation/projects/{id}/ - Delete project
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, project_id, user):
        """
        Get project by ID, ensuring it belongs to the authenticated user.
        """
        try:
            return Project.objects.get(
                id=project_id,
                owner=user,
                deleted_at__isnull=True,  # Exclude soft-deleted projects
            )
        except Project.DoesNotExist:
            return None

    def get(self, request, project_id):
        """
        Retrieve a specific project.
        """
        try:
            project = self.get_object(project_id, request.user)

            if not project:
                return Response(
                    {"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND
                )

            serializer = ProjectSerializer(project)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Failed to retrieve project: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, project_id):
        """
        Update a specific project.

        Supports partial updates - only provided fields will be updated.
        """
        try:
            project = self.get_object(project_id, request.user)

            if not project:
                return Response(
                    {"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND
                )

            serializer = ProjectUpdateSerializer(
                project,
                data=request.data,
                partial=True,  # Allow partial updates
            )

            if serializer.is_valid():
                updated_project = serializer.save()

                # Return the updated project
                response_serializer = ProjectSerializer(updated_project)
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Validation failed", "details": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            return Response(
                {"error": f"Failed to update project: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, project_id):
        """
        Soft delete a specific project.

        Uses soft delete to preserve data integrity.
        """
        try:
            project = self.get_object(project_id, request.user)

            if not project:
                return Response(
                    {"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND
                )

            # Perform soft delete
            project.soft_delete()

            return Response(
                {"message": "Project deleted successfully"}, status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": f"Failed to delete project: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ProjectSettingsView(APIView):
    """
    Handle GET and PUT operations for project settings.

    GET /api/v1/projects/{id}/settings - Get project settings
    PUT /api/v1/projects/{id}/settings - Update project settings
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, project_id, user):
        """
        Get project by ID, ensuring it belongs to the authenticated user.
        Optimized for settings view with canvas relationships.
        """
        try:
            return Project.objects.select_related("starting_canvas").get(
                id=project_id,
                owner=user,
                deleted_at__isnull=True,  # Exclude soft-deleted projects
            )
        except Project.DoesNotExist:
            return None

    def get(self, request, project_id):
        """
        Get project settings for Settings tab.
        """
        try:
            project = self.get_object(project_id, request.user)

            if not project:
                return Response(
                    {"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND
                )

            serializer = ProjectSettingsSerializer(project)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Failed to retrieve project settings: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, project_id):
        """
        Update project settings from Settings tab.

        Supports partial updates - only provided fields will be updated.
        """
        try:
            project = self.get_object(project_id, request.user)

            if not project:
                return Response(
                    {"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND
                )

            serializer = ProjectSettingsUpdateSerializer(
                project,
                data=request.data,
                partial=True,  # Allow partial updates
            )

            if serializer.is_valid():
                updated_project = serializer.save()

                # Return the updated project settings
                response_serializer = ProjectSettingsSerializer(updated_project)
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Validation failed", "details": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            return Response(
                {"error": f"Failed to update project settings: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PreviewNavigationGameView(APIView):
    """
    Preview navigation-only game for a project.

    POST /api/v1/foundation/projects/{id}/preview-game - Generate HTML preview
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, project_id, user):
        """Get project by ID, ensuring it belongs to the authenticated user."""
        try:
            return Project.objects.get(
                id=project_id, owner=user, deleted_at__isnull=True
            )
        except Project.DoesNotExist:
            return None

    def post(self, request, project_id):
        """Generate and return navigation-only game HTML."""
        try:
            project = self.get_object(project_id, request.user)

            if not project:
                error_html = """<html><body><h1>Project Not Found</h1>
                <p>The project you're looking for doesn't exist or you don't have access to it.</p>
                </body></html>"""
                return HttpResponse(error_html, content_type="text/html", status=404)

            # Use new game service
            game_service = GameService()

            # Validate project for generation
            validation = game_service.validate_project(project, "twee_navigation")

            # Generate navigation-only Twee content
            twee_content = game_service.generate_game(project, "twee_navigation", "v1")

            # Compile to HTML
            html_content = game_service.compile_twee_to_html(twee_content, project.name)

            # Add cache-busting headers
            response = HttpResponse(html_content, content_type="text/html")
            response["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
            response["Pragma"] = "no-cache"
            response["Expires"] = "0"

            return response

        except ValueError as e:
            # Handle project validation errors
            error_html = f"""<html><body><h1>Game Generation Failed</h1>
            <p>{str(e)}</p>
            <p>Please add story canvases and nodes in the Stories tab.</p>
            </body></html>"""
            return HttpResponse(error_html, content_type="text/html", status=422)

        except Exception as e:
            # Handle unexpected errors
            error_html = f"""<html><body><h1>Game Generation Error</h1>
            <p>An unexpected error occurred: {str(e)}</p>
            </body></html>"""
            return HttpResponse(error_html, content_type="text/html", status=500)


class PreviewComprehensiveGameView(APIView):
    """
    Preview comprehensive game with all features for a project.

    POST /api/v1/foundation/projects/{id}/preview-comprehensive-game - Generate HTML preview
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, project_id, user):
        """Get project by ID, ensuring it belongs to the authenticated user."""
        try:
            return Project.objects.get(
                id=project_id, owner=user, deleted_at__isnull=True
            )
        except Project.DoesNotExist:
            return None

    def post(self, request, project_id):
        """Generate and return comprehensive game HTML."""
        try:
            project = self.get_object(project_id, request.user)

            if not project:
                error_html = """<html><body><h1>Project Not Found</h1>
                <p>The project you're looking for doesn't exist or you don't have access to it.</p>
                </body></html>"""
                return HttpResponse(error_html, content_type="text/html", status=404)

            # Use new game service
            game_service = GameService()

            # Generate comprehensive Twee content
            twee_content = game_service.generate_game(
                project, "twee_comprehensive", "v1"
            )

            # Compile to HTML
            html_content = game_service.compile_twee_to_html(twee_content, project.name)

            # Add cache-busting headers
            response = HttpResponse(html_content, content_type="text/html")
            response["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
            response["Pragma"] = "no-cache"
            response["Expires"] = "0"

            return response

        except ValueError as e:
            # Handle project validation errors
            error_html = f"""<html><body><h1>Game Generation Failed</h1>
            <p>{str(e)}</p>
            <p>Please add story canvases and nodes in the Stories tab.</p>
            </body></html>"""
            return HttpResponse(error_html, content_type="text/html", status=422)

        except Exception as e:
            # Handle unexpected errors
            error_html = f"""<html><body><h1>Game Generation Error</h1>
            <p>An unexpected error occurred: {str(e)}</p>
            </body></html>"""
            return HttpResponse(error_html, content_type="text/html", status=500)


class GenerateGameView(APIView):
    """
    Generate game files for download.

    POST /api/v1/foundation/projects/{id}/generate-game?format={format} - Generate downloadable files
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, project_id, user):
        """Get project by ID, ensuring it belongs to the authenticated user."""
        try:
            return Project.objects.get(
                id=project_id, owner=user, deleted_at__isnull=True
            )
        except Project.DoesNotExist:
            return None

    def post(self, request, project_id):
        """Generate game file for download."""
        try:
            project = self.get_object(project_id, request.user)

            if not project:
                return Response(
                    {"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND
                )

            # Get format parameter (twee or html) from query params or request body
            format_type = request.query_params.get("format") or request.data.get(
                "format", "twee"
            )
            if format_type not in ["twee", "html"]:
                return Response(
                    {"error": 'Invalid format. Must be "twee" or "html"'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Use new game service
            game_service = GameService()

            # Generate Twee content (default to navigation game)
            twee_content = game_service.generate_game(project, "twee_navigation", "v1")

            # Prepare filename
            safe_name = project.name.replace(" ", "_").replace("/", "_")

            if format_type == "twee":
                # Return Twee file
                filename = f"{safe_name}_game.twee"
                response = HttpResponse(twee_content, content_type="text/plain")
                response["Content-Disposition"] = f'attachment; filename="{filename}"'
                return response

            elif format_type == "html":
                # Return HTML file
                html_content = game_service.compile_twee_to_html(
                    twee_content, project.name
                )
                filename = f"{safe_name}_game.html"
                response = HttpResponse(html_content, content_type="text/html")
                response["Content-Disposition"] = f'attachment; filename="{filename}"'
                return response

        except ValueError as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        except Exception as e:
            return Response(
                {"error": f"Failed to generate game: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
