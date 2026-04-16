"""Service layer for clip description export operations."""

from typing import Any
import csv
import json
from io import StringIO
from itertools import groupby
from django.utils import timezone
from apps.assets.models import AssetClip, AssetVideo, AssetGroup


class ClipDescriptionExportService:
    """Service for exporting clip descriptions in various formats."""

    @staticmethod
    def get_clip_data(
        video_id: str,
        extended: bool = False,
        only_described: bool = False
    ) -> dict[str, Any]:
        """
        Aggregate clip descriptions for export.

        Args:
            video_id: UUID of the video
            extended: Include all metadata (timestamps, model info)
            only_described: Filter to only clips with descriptions

        Returns:
            Dictionary with video metadata and clips array
        """
        video = AssetVideo.objects.get(id=video_id)

        # Query clips
        clips_query = AssetClip.objects.filter(
            video_id=video_id,
            deleted_at__isnull=True
        ).order_by("index")

        if only_described:
            clips_query = clips_query.exclude(description__isnull=True).exclude(description="")

        clips = clips_query.select_related("video")

        # Build clips array
        clips_data = []
        for clip in clips:
            clip_dict = {
                "id": str(clip.id),
                "index": clip.index,
                "description": clip.description or None,
            }

            if extended:
                clip_dict.update({
                    "start_sec": clip.start_sec,
                    "end_sec": clip.end_sec,
                    "duration_sec": clip.duration_sec,
                    "description_model": clip.description_model or None,
                    "description_generated_at": (
                        clip.description_generated_at.isoformat()
                        if clip.description_generated_at else None
                    ),
                })

            clips_data.append(clip_dict)

        # Build response
        result = {
            "video_id": str(video.id),
            "exported_at": timezone.now().isoformat(),
            "clips": clips_data,
        }

        if extended:
            # Count clips with descriptions
            described_count = sum(1 for c in clips_data if c.get("description"))
            result["metadata"] = {
                "total_clips": len(clips_data),
                "clips_with_descriptions": described_count,
            }

        return result

    @staticmethod
    def export_to_json(
        video_id: str,
        extended: bool = False,
        only_described: bool = False
    ) -> str:
        """
        Export clip descriptions as JSON.

        Args:
            video_id: UUID of the video
            extended: Include all metadata
            only_described: Filter to only clips with descriptions

        Returns:
            JSON string
        """
        data = ClipDescriptionExportService.get_clip_data(
            video_id, extended, only_described
        )
        return json.dumps(data, indent=2)

    @staticmethod
    def export_to_csv(
        video_id: str,
        extended: bool = False,
        only_described: bool = False
    ) -> str:
        """
        Export clip descriptions as CSV.

        Args:
            video_id: UUID of the video
            extended: Include all metadata
            only_described: Filter to only clips with descriptions

        Returns:
            CSV string
        """
        data = ClipDescriptionExportService.get_clip_data(
            video_id, extended, only_described
        )

        clips = data.get("clips", [])
        if not clips:
            # Return header only for empty results
            headers = ["clip_id", "clip_index", "description"]
            if extended:
                headers.extend(["start_sec", "end_sec", "duration_sec", "description_model"])
            return ",".join(headers) + "\n"

        # Build CSV
        output = StringIO()
        fieldnames = list(clips[0].keys())
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(clips)

        return output.getvalue()

    @staticmethod
    def generate_filename(video_id: str, format_type: str) -> str:
        """
        Generate standardized filename for export.

        Args:
            video_id: UUID of the video
            format_type: File extension (json, csv)

        Returns:
            Filename string
        """
        timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
        return f"video_{video_id}_descriptions_{timestamp}.{format_type}"

    # Group-level export methods

    @staticmethod
    def get_group_clip_data(
        group_id: str,
        extended: bool = False,
        only_described: bool = False
    ) -> dict[str, Any]:
        """
        Aggregate clip descriptions from all videos in a group.

        Args:
            group_id: UUID of the group
            extended: Include all metadata (timestamps, model info)
            only_described: Filter to only clips with descriptions

        Returns:
            Dictionary with group metadata, videos array, and clips nested within videos
        """
        group = AssetGroup.objects.get(id=group_id)

        # Query all clips in group
        clips_query = AssetClip.objects.filter(
            video__group_id=group_id,
            deleted_at__isnull=True  # Active clips only
        ).select_related('video').order_by('video__id', 'index')

        if only_described:
            clips_query = clips_query.exclude(
                description__isnull=True
            ).exclude(description="")

        clips = list(clips_query)

        # Group clips by video_id
        videos_data = []
        for video_id, clips_iter in groupby(clips, key=lambda c: c.video_id):
            clip_list = list(clips_iter)
            if not clip_list:  # Skip empty videos
                continue

            clips_data = []
            for clip in clip_list:
                clip_dict = {
                    "id": str(clip.id),
                    "index": clip.index,
                    "description": clip.description or None,
                }
                if extended:
                    clip_dict.update({
                        "start_sec": clip.start_sec,
                        "end_sec": clip.end_sec,
                        "duration_sec": clip.duration_sec,
                        "description_model": clip.description_model or None,
                        "description_generated_at": (
                            clip.description_generated_at.isoformat()
                            if clip.description_generated_at else None
                        ),
                    })
                clips_data.append(clip_dict)

            videos_data.append({
                "video_id": str(video_id),
                "clips": clips_data
            })

        # Build response
        result = {
            "group_id": str(group.id),
            "group_name": group.name,
            "exported_at": timezone.now().isoformat(),
            "videos": videos_data,
        }

        if extended:
            total_clips = sum(len(v["clips"]) for v in videos_data)
            described_count = sum(
                1 for v in videos_data
                for c in v["clips"]
                if c.get("description")
            )
            result["metadata"] = {
                "total_videos": len(videos_data),
                "total_clips": total_clips,
                "clips_with_descriptions": described_count,
            }

        return result

    @staticmethod
    def export_group_to_json(
        group_id: str,
        extended: bool = False,
        only_described: bool = False
    ) -> str:
        """
        Export group clip descriptions as JSON.

        Args:
            group_id: UUID of the group
            extended: Include all metadata
            only_described: Filter to only clips with descriptions

        Returns:
            JSON string with nested videos→clips structure
        """
        data = ClipDescriptionExportService.get_group_clip_data(
            group_id, extended, only_described
        )
        return json.dumps(data, indent=2)

    @staticmethod
    def export_group_to_csv(
        group_id: str,
        extended: bool = False,
        only_described: bool = False
    ) -> str:
        """
        Export group clip descriptions as CSV (flattened).

        Args:
            group_id: UUID of the group
            extended: Include all metadata
            only_described: Filter to only clips with descriptions

        Returns:
            CSV string with flattened video_id, clip_id structure
        """
        data = ClipDescriptionExportService.get_group_clip_data(
            group_id, extended, only_described
        )

        # Flatten videos → clips structure
        all_clips = []
        for video in data.get("videos", []):
            video_id = video["video_id"]
            for clip in video.get("clips", []):
                flat_clip = {
                    "video_id": video_id,
                    "clip_id": clip["id"],
                    "clip_index": clip["index"],
                    "description": clip["description"],
                }
                if extended:
                    flat_clip.update({
                        "start_sec": clip.get("start_sec"),
                        "end_sec": clip.get("end_sec"),
                        "duration_sec": clip.get("duration_sec"),
                        "description_model": clip.get("description_model"),
                        "description_generated_at": clip.get("description_generated_at"),
                    })
                all_clips.append(flat_clip)

        if not all_clips:
            # Return header only
            headers = ["video_id", "clip_id", "clip_index", "description"]
            if extended:
                headers.extend([
                    "start_sec", "end_sec", "duration_sec",
                    "description_model", "description_generated_at"
                ])
            return ",".join(headers) + "\n"

        # Build CSV
        output = StringIO()
        fieldnames = list(all_clips[0].keys())
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_clips)

        return output.getvalue()
