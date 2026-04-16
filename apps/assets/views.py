from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

import os
from django.http import FileResponse, StreamingHttpResponse, HttpResponse
from django.core.files import File
from django.core.files.storage import default_storage
from django.utils import timezone

import tempfile
import socket
import ipaddress
from urllib.parse import urlparse, urljoin
import requests
from pathlib import Path
import time
import hmac
import hashlib
from django.conf import settings

from .models import AssetGroup, AssetVideo, AssetClip, ClipFrame, AssetVideoStatus
from .services.processing import process_video_sync, recaption_frame_sync
from .services.clip_deletion import ClipDeletionService
from .services.grok_clip_service import get_grok_client
from .services.export_service import ClipDescriptionExportService
from .serializers import (
    AssetGroupSerializer,
    AssetVideoSerializer,
    AssetClipSerializer,
    ClipFrameSerializer,
)
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)


class AssetGroupListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = AssetGroup.objects.filter(owner=request.user, deleted_at__isnull=True).order_by("-created_at")
        # Simple pagination params
        limit = int(request.query_params.get("limit", 50))
        offset = int(request.query_params.get("offset", 0))
        total = qs.count()
        items = qs[offset : offset + limit]
        data = AssetGroupSerializer(items, many=True).data
        return Response({
            "items": data,
            "pagination": {
                "total": total,
                "offset": offset,
                "limit": limit,
                "has_more": offset + len(data) < total,
            },
        })

    def post(self, request):
        serializer = AssetGroupSerializer(data=request.data)
        if serializer.is_valid():
            group = AssetGroup(owner=request.user, **serializer.validated_data)
            group.save()
            return Response(group.to_dict(), status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AssetGroupDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request, group_id):
        return get_object_or_404(AssetGroup, id=group_id, owner=request.user, deleted_at__isnull=True)

    def get(self, request, group_id):
        group = self.get_object(request, group_id)
        return Response(AssetGroupSerializer(group).data)

    def put(self, request, group_id):
        group = self.get_object(request, group_id)
        serializer = AssetGroupSerializer(group, data=request.data, partial=True)
        if serializer.is_valid():
            for k, v in serializer.validated_data.items():
                setattr(group, k, v)
            group.save()
            return Response(AssetGroupSerializer(group).data)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, group_id):
        group = self.get_object(request, group_id)
        group.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AssetVideoListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        group = get_object_or_404(AssetGroup, id=group_id, owner=request.user, deleted_at__isnull=True)
        status_filter = request.query_params.get("status")
        q = request.query_params.get("q")
        qs = AssetVideo.objects.filter(group=group)
        if status_filter in {s.value for s in AssetVideoStatus}:
            qs = qs.filter(status=status_filter)
        if q:
            qs = qs.filter(file__icontains=q)
        limit = int(request.query_params.get("limit", 50))
        offset = int(request.query_params.get("offset", 0))
        total = qs.count()
        items = qs.order_by("-created_at")[offset : offset + limit]
        data = AssetVideoSerializer(items, many=True).data
        return Response({
            "items": data,
            "pagination": {
                "total": total,
                "offset": offset,
                "limit": limit,
                "has_more": offset + len(data) < total,
            },
        })


class AssetVideoUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, group_id):
        group = get_object_or_404(AssetGroup, id=group_id, owner=request.user, deleted_at__isnull=True)
        uploaded = request.FILES.get("file")
        if not uploaded:
            return Response({"error": "Missing file"}, status=status.HTTP_400_BAD_REQUEST)

        content_type = getattr(uploaded, "content_type", "") or request.META.get("CONTENT_TYPE", "")
        size_bytes = getattr(uploaded, "size", None) or uploaded.size

        if not (content_type.startswith("video/") or uploaded.name.lower().endswith((".mp4", ".mov", ".mkv", ".avi", ".ts", ".wmv"))):
            return Response({"error": f"Unsupported content type: {content_type}"}, status=status.HTTP_400_BAD_REQUEST)

        max_video = 500 * 1024 * 1024
        if size_bytes and size_bytes > max_video:
            return Response({"error": "Video too large (max 500MB)"}, status=status.HTTP_400_BAD_REQUEST)

        video = AssetVideo(
            group=group,
            mime_type=content_type or "application/octet-stream",
            size_bytes=size_bytes or 0,
            status=AssetVideoStatus.PENDING,
        )
        video.file = uploaded
        video.save()

        # Kick off synchronous processing for development
        try:
            error = process_video_sync(video)
            if error:
                # Processing failed but error was handled by processor
                video.refresh_from_db()
        except Exception as e:
            # Unexpected error during processing - log and update status
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Video processing failed for {video.id}: {e}", exc_info=True)

            video.status = AssetVideoStatus.FAILED
            video.error = f"Processing failed: {str(e)[:500]}"
            video.save(update_fields=["status", "error"])

        return Response(AssetVideoSerializer(AssetVideo.objects.get(id=video.id)).data, status=status.HTTP_201_CREATED)


class AssetVideoIngestUrlView(APIView):
    permission_classes = [IsAuthenticated]

    MAX_BYTES = 500 * 1024 * 1024  # 500MB
    MAX_REDIRECTS = 3
    TIMEOUT = (5, 60)  # (connect, read)

    def _is_private_ip(self, host: str) -> bool:
        try:
            infos = socket.getaddrinfo(host, None)
            for family, _, _, _, sockaddr in infos:
                ip_str = sockaddr[0]
                ip = ipaddress.ip_address(ip_str)
                if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast:
                    return True
            return False
        except Exception:
            # If resolution fails, treat as unsafe
            return True

    def _validate_url(self, raw_url: str) -> tuple[bool, str | None]:
        try:
            parsed = urlparse(raw_url)
            if parsed.scheme not in ("http", "https"):
                return False, "Only http(s) URLs are allowed"
            if not parsed.netloc:
                return False, "Invalid URL host"
            host = parsed.hostname or ""
            if self._is_private_ip(host):
                return False, "URL resolves to a private or disallowed IP"
            return True, None
        except Exception:
            return False, "Invalid URL"

    def _follow(self, method: str, url: str, allow_stream: bool = False) -> requests.Response:
        """Perform an HTTP request with manual, validated redirects."""
        current_url = url
        for _ in range(self.MAX_REDIRECTS + 1):
            parsed = urlparse(current_url)
            host = parsed.hostname or ""
            if self._is_private_ip(host):
                raise ValueError("Redirect target resolves to a private IP")
            resp = requests.request(
                method,
                current_url,
                allow_redirects=False,
                stream=allow_stream,
                timeout=self.TIMEOUT,
                headers={"User-Agent": "AssetLibraryBot/1.0"},
            )
            if 300 <= resp.status_code < 400 and resp.headers.get("Location"):
                # Build absolute URL and continue
                loc = resp.headers["Location"]
                current_url = urljoin(current_url, loc)
                continue
            return resp
        raise ValueError("Too many redirects")

    def post(self, request, group_id):
        group = get_object_or_404(AssetGroup, id=group_id, owner=request.user, deleted_at__isnull=True)
        url = (request.data.get("url") or "").strip()
        if not url:
            return Response({"error": "Missing url"}, status=status.HTTP_400_BAD_REQUEST)

        ok, err = self._validate_url(url)
        if not ok:
            return Response({"error": err}, status=status.HTTP_400_BAD_REQUEST)

        # HEAD probe for content-length and type (best effort)
        content_length = None
        mime_type = None
        try:
            head = self._follow("HEAD", url, allow_stream=False)
            if head.status_code >= 400:
                # Some servers don't support HEAD; ignore errors here
                head = None  # type: ignore
            else:
                cl = head.headers.get("Content-Length") if head else None
                if cl and cl.isdigit():
                    content_length = int(cl)
                ct = head.headers.get("Content-Type") if head else None
                if ct:
                    mime_type = ct.split(";")[0].strip()
        except Exception:
            pass

        if content_length and content_length > self.MAX_BYTES:
            return Response({"error": "Video too large (max 500MB)"}, status=status.HTTP_400_BAD_REQUEST)

        # GET and stream to temp file with size cap
        try:
            resp = self._follow("GET", url, allow_stream=True)
        except Exception as e:
            return Response({"error": f"Failed to fetch URL: {e}"}, status=status.HTTP_400_BAD_REQUEST)

        if resp.status_code >= 400:
            return Response({"error": f"Download failed with status {resp.status_code}"}, status=status.HTTP_400_BAD_REQUEST)

        # Determine final filename and mime
        final_url = resp.url
        provided_name = (request.data.get("filename") or "").strip()
        # Extract name from provided or path
        name_candidate = provided_name or Path(urlparse(final_url).path).name or "video.mp4"
        # Sanitize name
        safe_name = name_candidate.split("/")[-1].split("\\")[-1]
        if "." not in safe_name:
            safe_name += ".mp4"
        ext = safe_name.split(".")[-1].lower()
        allowed_exts = {"mp4", "mov", "mkv", "avi", "ts", "wmv"}
        if ext not in allowed_exts:
            return Response({"error": "Unsupported file type"}, status=status.HTTP_400_BAD_REQUEST)

        # Content-Type preference from GET
        ct = resp.headers.get("Content-Type")
        if ct:
            mime_type = ct.split(";")[0].strip()
        if not mime_type:
            # Basic inference
            mime_map = {
                "mp4": "video/mp4",
                "mov": "video/quicktime",
                "mkv": "video/x-matroska",
                "avi": "video/x-msvideo",
                "ts": "video/MP2T",
                "wmv": "video/x-ms-wmv",
            }
            mime_type = mime_map.get(ext, "application/octet-stream")

        if not (mime_type.startswith("video/") or ext in allowed_exts):
            return Response({"error": f"Unsupported content type: {mime_type}"}, status=status.HTTP_400_BAD_REQUEST)

        # Stream download
        total = 0
        tmp = tempfile.NamedTemporaryFile(delete=False)
        tmp_path = Path(tmp.name)
        try:
            for chunk in resp.iter_content(chunk_size=1024 * 1024):  # 1MB chunks
                if not chunk:
                    continue
                total += len(chunk)
                if total > self.MAX_BYTES:
                    tmp.close()
                    try:
                        tmp_path.unlink(missing_ok=True)
                    except Exception:
                        pass
                    return Response({"error": "Video too large (max 500MB)"}, status=status.HTTP_400_BAD_REQUEST)
                tmp.write(chunk)
            tmp.flush()
        except Exception:
            tmp.close()
            try:
                tmp_path.unlink(missing_ok=True)
            except Exception:
                pass
            return Response({"error": "Failed while downloading video"}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            try:
                resp.close()
            except Exception:
                pass

        # Create DB record and attach file
        video = AssetVideo(
            group=group,
            mime_type=mime_type or "application/octet-stream",
            size_bytes=total,
            status=AssetVideoStatus.PENDING,
        )
        # Save file via storage
        with open(tmp_path, "rb") as fh:
            video.file.save(safe_name, File(fh), save=False)
        video.save()

        # Cleanup temp
        try:
            tmp.close()
            tmp_path.unlink(missing_ok=True)
        except Exception:
            pass

        # Kick off synchronous processing for development
        try:
            error = process_video_sync(video)
            if error:
                # Processing failed but error was handled by processor
                video.refresh_from_db()
        except Exception as e:
            # Unexpected error during processing - log and update status
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Video processing failed for {video.id}: {e}", exc_info=True)

            video.status = AssetVideoStatus.FAILED
            video.error = f"Processing failed: {str(e)[:500]}"
            video.save(update_fields=["status", "error"])

        return Response(AssetVideoSerializer(AssetVideo.objects.get(id=video.id)).data, status=status.HTTP_201_CREATED)


class AssetVideoDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, video_id):
        video = get_object_or_404(AssetVideo, id=video_id, group__owner=request.user, group__deleted_at__isnull=True)
        # Counts
        clip_count = video.clips.count()
        frame_count = ClipFrame.objects.filter(clip__video=video).count()
        data = AssetVideoSerializer(video).data
        data["counts"] = {"clips": clip_count, "frames": frame_count}
        return Response(data)


class AssetVideoSignedUrlView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, video_id):
        """Return a direct play URL for the full source video.

        For uploaded assets backed by django-storages, .url may be signed or public
        depending on storage configuration. We simply surface it here after auth.
        """
        video = get_object_or_404(AssetVideo, id=video_id, group__owner=request.user, group__deleted_at__isnull=True)
        url = video.file.url if video.file else ""
        if not url:
            return Response({"error": "Video file not available"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"url": url})


class AssetClipSignedUrlView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, clip_id):
        """Return the R2 storage URL for a clip."""
        clip = get_object_or_404(
            AssetClip,
            id=clip_id,
            video__group__owner=request.user
        )

        if not clip.file:
            return Response({"error": "Clip file not available"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"url": clip.file.url})

class AssetClipListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, video_id):
        video = get_object_or_404(AssetVideo, id=video_id, group__owner=request.user)
        limit = int(request.query_params.get("limit", 50))
        offset = int(request.query_params.get("offset", 0))
        # Only show active (non-deleted) clips
        qs = video.clips.filter(deleted_at__isnull=True).order_by("index")
        total = qs.count()
        items = qs[offset : offset + limit]
        data = AssetClipSerializer(items, many=True).data
        return Response({
            "items": data,
            "pagination": {
                "total": total,
                "offset": offset,
                "limit": limit,
                "has_more": offset + len(data) < total,
            },
        })


class AssetClipDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, clip_id):
        # Only return active (non-deleted) clips
        clip = get_object_or_404(
            AssetClip,
            id=clip_id,
            video__group__owner=request.user,
            deleted_at__isnull=True
        )
        return Response(AssetClipSerializer(clip).data)


class ClipFrameListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, clip_id):
        clip = get_object_or_404(AssetClip, id=clip_id, video__group__owner=request.user)
        q = request.query_params.get("q")
        qs = clip.frames.all().order_by("timestamp_sec")
        if q:
            qs = qs.filter(caption_text__icontains=q)
        limit = int(request.query_params.get("limit", 50))
        offset = int(request.query_params.get("offset", 0))
        total = qs.count()
        items = qs[offset : offset + limit]
        data = ClipFrameSerializer(items, many=True).data
        return Response({
            "items": data,
            "pagination": {
                "total": total,
                "offset": offset,
                "limit": limit,
                "has_more": offset + len(data) < total,
            },
        })


class FrameRecaptionView(APIView):
    """DISABLED: Frame recaptioning is currently disabled."""
    permission_classes = [IsAuthenticated]

    def post(self, request, frame_id):
        return Response(
            {"error": "Frame recaptioning is currently disabled"},
            status=status.HTTP_501_NOT_IMPLEMENTED
        )


class AssetClipDeleteView(APIView):
    """Soft delete a clip (moves to Deleted Clips section)."""
    permission_classes = [IsAuthenticated]

    def delete(self, request, clip_id):
        clip = get_object_or_404(
            AssetClip,
            id=clip_id,
            video__group__owner=request.user,
            deleted_at__isnull=True  # Only allow deletion of active clips
        )

        try:
            result = ClipDeletionService.soft_delete_clip(clip)
            logger.info(
                f"User {request.user.id} soft deleted clip {clip_id} "
                f"(video={clip.video_id})"
            )
            return Response(result, status=status.HTTP_200_OK)
        except ValidationError as e:
            logger.warning(
                f"Validation failed for clip {clip_id} deletion: {e}"
            )
            return Response(
                {"error": str(e), "error_code": "VALIDATION_FAILED"},
                status=status.HTTP_409_CONFLICT
            )
        except Exception as e:
            logger.error(
                f"Unexpected error deleting clip {clip_id}: {e}",
                exc_info=True
            )
            return Response(
                {"error": "Failed to delete clip"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AssetClipRestoreView(APIView):
    """Restore a soft-deleted clip."""
    permission_classes = [IsAuthenticated]

    def post(self, request, clip_id):
        clip = get_object_or_404(
            AssetClip,
            id=clip_id,
            video__group__owner=request.user,
            deleted_at__isnull=False  # Must be deleted to restore
        )

        try:
            # Clear the deleted_at timestamp to restore the clip
            clip.deleted_at = None
            clip.save(update_fields=["deleted_at"])

            logger.info(
                f"User {request.user.id} restored clip {clip_id} "
                f"(video={clip.video_id})"
            )

            return Response({
                "success": True,
                "clip_id": str(clip.id),
                "message": "Clip restored successfully"
            })
        except Exception as e:
            logger.error(
                f"Failed to restore clip {clip_id}: {e}",
                exc_info=True
            )
            return Response(
                {"error": "Failed to restore clip"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AssetClipHardDeleteView(APIView):
    """Permanently delete a clip (must already be soft-deleted)."""
    permission_classes = [IsAuthenticated]

    def delete(self, request, clip_id):
        clip = get_object_or_404(
            AssetClip,
            id=clip_id,
            video__group__owner=request.user,
            deleted_at__isnull=False  # Must be soft-deleted first
        )

        try:
            result = ClipDeletionService.hard_delete_clip(clip)
            logger.info(
                f"User {request.user.id} permanently deleted clip {clip_id} "
                f"(video={clip.video_id})"
            )
            return Response(result, status=status.HTTP_200_OK)
        except ValidationError as e:
            logger.warning(
                f"Validation failed for permanent deletion of clip {clip_id}: {e}"
            )
            return Response(
                {"error": str(e), "error_code": "VALIDATION_FAILED"},
                status=status.HTTP_409_CONFLICT
            )
        except Exception as e:
            logger.error(
                f"Failed to permanently delete clip {clip_id}: {e}",
                exc_info=True
            )
            return Response(
                {"error": "Failed to delete clip permanently"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AssetClipDeletedListView(APIView):
    """List soft-deleted clips for a video."""
    permission_classes = [IsAuthenticated]

    def get(self, request, video_id):
        video = get_object_or_404(
            AssetVideo,
            id=video_id,
            group__owner=request.user
        )

        # Get only soft-deleted clips
        deleted_clips = video.clips.filter(
            deleted_at__isnull=False
        ).order_by("-deleted_at")

        limit = int(request.query_params.get("limit", 50))
        offset = int(request.query_params.get("offset", 0))
        total = deleted_clips.count()
        items = deleted_clips[offset : offset + limit]

        data = AssetClipSerializer(items, many=True).data

        return Response({
            "items": data,
            "pagination": {
                "total": total,
                "offset": offset,
                "limit": limit,
                "has_more": offset + len(data) < total,
            },
        })


class AssetClipGenerateDescriptionView(APIView):
    """Generate AI description for a single clip."""
    permission_classes = [IsAuthenticated]

    def post(self, request, clip_id):
        # 1. Get clip and verify ownership
        clip = get_object_or_404(
            AssetClip,
            id=clip_id,
            video__group__owner=request.user,
            deleted_at__isnull=True  # Only active clips
        )

        # 2. Check service availability
        try:
            client = get_grok_client()
            if not client.is_available():
                return Response(
                    {
                        "error": "AI description generation service is not enabled or configured",
                        "error_code": "SERVICE_UNAVAILABLE"
                    },
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
        except Exception as e:
            logger.error(f"Failed to initialize Grok client: {e}")
            return Response(
                {
                    "error": "Description generation service unavailable",
                    "error_code": "SERVICE_ERROR"
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        # 3. Generate description
        try:
            result = client.generate_with_result(clip)

            logger.info(
                f"User {request.user.id} generated description for clip {clip_id}: "
                f"success={result['success']}, skipped={result['skipped']}"
            )

            # Return 200 OK even if skipped/failed (client handles based on result.success)
            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(
                f"Unexpected error generating description for clip {clip_id}: {e}",
                exc_info=True
            )
            return Response(
                {
                    "error": "Failed to generate description",
                    "error_code": "GENERATION_ERROR",
                    "details": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AssetVideoGenerateDescriptionsView(APIView):
    """Batch generate descriptions for all clips in a video."""
    permission_classes = [IsAuthenticated]

    def post(self, request, video_id):
        # 1. Get video and verify ownership
        video = get_object_or_404(
            AssetVideo,
            id=video_id,
            group__owner=request.user
        )

        # 2. Parse request body
        only_missing = request.data.get('only_missing', True)
        force_regenerate = request.data.get('force_regenerate', False)

        # 3. Check service availability
        try:
            client = get_grok_client()
            if not client.is_available():
                return Response(
                    {
                        "error": "AI description generation service is not enabled or configured",
                        "error_code": "SERVICE_UNAVAILABLE"
                    },
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
        except Exception as e:
            logger.error(f"Failed to initialize Grok client: {e}")
            return Response(
                {
                    "error": "Description generation service unavailable",
                    "error_code": "SERVICE_ERROR"
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        # 4. Batch generate
        try:
            result = client.batch_generate_for_video(
                video,
                only_missing=only_missing,
                force_regenerate=force_regenerate
            )

            logger.info(
                f"User {request.user.id} batch generated descriptions for video {video_id}: "
                f"processed={result['processed']}, successful={result['summary']['successful']}, "
                f"failed={result['summary']['failed']}, skipped={result['summary']['skipped']}"
            )

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(
                f"Unexpected error in batch generation for video {video_id}: {e}",
                exc_info=True
            )
            return Response(
                {
                    "error": "Failed to generate descriptions",
                    "error_code": "BATCH_GENERATION_ERROR",
                    "details": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AssetVideoExportDescriptionsView(APIView):
    """Export clip descriptions for download."""
    permission_classes = [IsAuthenticated]

    def get(self, request, video_id):
        """
        Export clip descriptions as downloadable file.

        Query Parameters:
            format: json (default) | csv
            extended: boolean (default: false) - Include all metadata
            only_described: boolean (default: false) - Only clips with descriptions
        """
        # 1. Get video and verify ownership
        video = get_object_or_404(
            AssetVideo,
            id=video_id,
            group__owner=request.user
        )

        # 2. Parse query parameters
        export_format = request.query_params.get("format", "json").lower()
        extended = request.query_params.get("extended", "false").lower() == "true"
        only_described = request.query_params.get("only_described", "false").lower() == "true"

        # 3. Validate format
        if export_format not in ("json", "csv"):
            return Response(
                {"error": "Invalid format. Use 'json' or 'csv'"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 4. Generate export content
        try:
            if export_format == "json":
                content = ClipDescriptionExportService.export_to_json(
                    str(video.id), extended, only_described
                )
                mime_type = "application/json; charset=utf-8"
            else:  # csv
                content = ClipDescriptionExportService.export_to_csv(
                    str(video.id), extended, only_described
                )
                mime_type = "text/csv; charset=utf-8"

            # 5. Generate filename
            filename = ClipDescriptionExportService.generate_filename(
                str(video.id), export_format
            )

            # 6. Return as downloadable file
            response = HttpResponse(content, content_type=mime_type)
            response["Content-Disposition"] = f'attachment; filename="{filename}"'

            logger.info(
                f"User {request.user.id} exported descriptions for video {video_id}: "
                f"format={export_format}, clips={video.clips.filter(deleted_at__isnull=True).count()}"
            )

            return response

        except Exception as e:
            logger.error(
                f"Error exporting descriptions for video {video_id}: {e}",
                exc_info=True
            )
            return Response(
                {
                    "error": "Failed to export descriptions",
                    "error_code": "EXPORT_ERROR",
                    "details": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AssetGroupExportDescriptionsView(APIView):
    """Export clip descriptions from all videos in a group."""
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        """
        Export clip descriptions from group as downloadable file.

        Query Parameters:
            format: json (default) | csv
            extended: boolean (default: false) - Include all metadata
            only_described: boolean (default: false) - Only clips with descriptions
        """
        # 1. Get group and verify ownership
        group = get_object_or_404(
            AssetGroup,
            id=group_id,
            owner=request.user,
            deleted_at__isnull=True
        )

        # 2. Parse query parameters
        export_format = request.query_params.get("format", "json").lower()
        extended = request.query_params.get("extended", "false").lower() == "true"
        only_described = request.query_params.get("only_described", "false").lower() == "true"

        # 3. Validate format
        if export_format not in ("json", "csv"):
            return Response(
                {"error": "Invalid format. Use 'json' or 'csv'"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 4. Generate export content
        try:
            if export_format == "json":
                content = ClipDescriptionExportService.export_group_to_json(
                    str(group.id), extended, only_described
                )
                mime_type = "application/json; charset=utf-8"
            else:  # csv
                content = ClipDescriptionExportService.export_group_to_csv(
                    str(group.id), extended, only_described
                )
                mime_type = "text/csv; charset=utf-8"

            # 5. Generate filename
            timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
            filename = f"group_{group.id}_descriptions_{timestamp}.{export_format}"

            # 6. Return as downloadable file
            response = HttpResponse(content, content_type=mime_type)
            response["Content-Disposition"] = f'attachment; filename="{filename}"'

            logger.info(
                f"User {request.user.id} exported descriptions for group {group_id}: "
                f"format={export_format}"
            )

            return response

        except Exception as e:
            logger.error(
                f"Error exporting descriptions for group {group_id}: {e}",
                exc_info=True
            )
            return Response(
                {
                    "error": "Failed to export descriptions",
                    "error_code": "GROUP_EXPORT_ERROR",
                    "details": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
