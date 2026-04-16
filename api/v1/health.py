"""
Health check endpoints.
"""

from django.conf import settings
from django.db import connection
from django.urls import path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    """Basic health check endpoint."""

    # Check database connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        db_status = "connected"
    except Exception:
        db_status = "error"

    return Response(
        {
            "status": "healthy",
            "database": db_status,
            "debug": settings.DEBUG,
            "version": "1.0.0",
        }
    )


urlpatterns = [
    path("", health_check, name="health_check"),
]
