"""
URL configuration for Django Story Generation Platform.
"""

import mimetypes
import re
from pathlib import Path

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import FileResponse, HttpResponse, HttpResponseNotFound, StreamingHttpResponse
from django.urls import include, path, re_path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # API Documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    # API v1 routes
    path("api/v1/", include("api.v1.urls")),
]

def _range_file_iterator(file_path, start=0, length=None, chunk_size=8192):
    """Yield file chunks for streaming, starting at offset for `length` bytes."""
    with open(file_path, "rb") as f:
        f.seek(start)
        remaining = length
        while True:
            read_size = min(chunk_size, remaining) if remaining else chunk_size
            data = f.read(read_size)
            if not data:
                break
            yield data
            if remaining is not None:
                remaining -= len(data)
                if remaining <= 0:
                    break


def range_serve(request, path, document_root=""):
    """Serve static files with HTTP Range support (needed for video seeking)."""
    fullpath = Path(document_root) / path
    fullpath = fullpath.resolve()
    if not str(fullpath).startswith(str(Path(document_root).resolve())):
        return HttpResponseNotFound()
    if not fullpath.is_file():
        return HttpResponseNotFound()

    file_size = fullpath.stat().st_size
    content_type, _ = mimetypes.guess_type(str(fullpath))
    content_type = content_type or "application/octet-stream"

    range_header = request.META.get("HTTP_RANGE")
    if range_header:
        match = re.match(r"bytes=(\d+)-(\d*)", range_header)
        if match:
            start = int(match.group(1))
            end = int(match.group(2)) if match.group(2) else file_size - 1
            if start >= file_size:
                resp = HttpResponse(status=416)
                resp["Content-Range"] = f"bytes */{file_size}"
                return resp
            end = min(end, file_size - 1)
            length = end - start + 1
            resp = StreamingHttpResponse(
                _range_file_iterator(fullpath, start, length),
                status=206,
                content_type=content_type,
            )
            resp["Content-Length"] = length
            resp["Content-Range"] = f"bytes {start}-{end}/{file_size}"
            resp["Accept-Ranges"] = "bytes"
            return resp

    resp = FileResponse(open(fullpath, "rb"), content_type=content_type)
    resp["Accept-Ranges"] = "bytes"
    resp["Content-Length"] = file_size
    return resp


# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [
        re_path(r"^games/(?P<path>.*)$", range_serve, {"document_root": str(settings.BASE_DIR / "games")}),
    ]
