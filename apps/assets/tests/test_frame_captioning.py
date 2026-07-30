"""
Tests for frame captioning service.
"""
import os
import tempfile
from unittest import mock

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.assets.models import AssetGroup, AssetVideo, AssetClip, ClipFrame, AssetVideoStatus
from apps.assets.services.frame_captioning import FrameCaptioningService


@pytest.mark.django_db
class TestFrameCaptioningService(TestCase):
    """Test FrameCaptioningService functionality."""

    def setUp(self):
        """Set up test fixtures."""
        # AssetGroup.owner is a non-null FK — there is no "without auth" path. The
        # sibling suites (test_grok_service.py, test_generate_clip_description_command.py)
        # already create a real user; match them rather than inventing a second pattern.
        User = get_user_model()
        self.user = User.objects.create_user(
            email="frame-captioning@example.com", password="testpass123"
        )
        self.group = AssetGroup.objects.create(
            name="Test Group",
            description="Test group for frame captioning",
            owner=self.user,
        )
        self.video = AssetVideo.objects.create(
            group=self.group,
            mime_type="video/mp4",
            size_bytes=1000000,
            status=AssetVideoStatus.PROCESSING
        )
        self.clip = AssetClip.objects.create(
            video=self.video,
            index=0,
            start_sec=0.0,
            end_sec=10.0,
            duration_sec=10.0,
            status="processing"
        )

    def test_extract_frames_for_clip_no_file(self):
        """Test frame extraction when file doesn't exist."""
        self.clip.temp_file_path = "/nonexistent/file.mp4"
        self.clip.save()

        with pytest.raises(RuntimeError):
            FrameCaptioningService.extract_frames_for_clip(
                clip=self.clip,
                video_file_path=self.clip.temp_file_path,
                interval_sec=2.0
            )

    @mock.patch('apps.assets.services.frame_captioning._probe_metadata')
    def test_extract_frames_invalid_duration(self, mock_probe):
        """Test frame extraction with invalid duration."""
        mock_probe.return_value = (1920, 1080, 0)  # duration = 0

        result = FrameCaptioningService.extract_frames_for_clip(
            clip=self.clip,
            video_file_path="/fake/path.mp4",
            interval_sec=2.0
        )

        assert result == []

    def test_create_frame_records_with_captions(self):
        """Test creating ClipFrame records with successful captions."""
        caption_results = [
            {"timestamp_sec": 0.0, "caption": "A person walking", "error": None},
            {"timestamp_sec": 2.0, "caption": "A car driving", "error": None},
            {"timestamp_sec": 4.0, "caption": "A bird flying", "error": None},
        ]

        frames = FrameCaptioningService.create_frame_records(
            clip=self.clip,
            caption_results=caption_results
        )

        assert len(frames) == 3
        assert all(f.status == "complete" for f in frames)
        assert all(f.caption_text for f in frames)
        assert frames[0].caption_text == "A person walking"
        assert frames[1].caption_text == "A car driving"
        assert frames[2].caption_text == "A bird flying"

        # Verify frames are saved in database
        db_frames = ClipFrame.objects.filter(clip=self.clip)
        assert db_frames.count() == 3

    def test_create_frame_records_vllm_unavailable(self):
        """Test creating frames when vLLM is unavailable."""
        caption_results = [
            {"timestamp_sec": 0.0, "caption": "", "error": "vLLM service unavailable"},
            {"timestamp_sec": 2.0, "caption": "", "error": "vLLM service unavailable"},
        ]

        frames = FrameCaptioningService.create_frame_records(
            clip=self.clip,
            caption_results=caption_results
        )

        assert len(frames) == 2
        assert all(f.status == "pending" for f in frames)  # Can retry later
        assert all(f.caption_text == "" for f in frames)
        assert all("unavailable" in f.error.lower() for f in frames)

    def test_create_frame_records_with_errors(self):
        """Test creating frames with captioning errors."""
        caption_results = [
            {"timestamp_sec": 0.0, "caption": "Success", "error": None},
            {"timestamp_sec": 2.0, "caption": "", "error": "Timeout"},
            {"timestamp_sec": 4.0, "caption": "Another success", "error": None},
        ]

        frames = FrameCaptioningService.create_frame_records(
            clip=self.clip,
            caption_results=caption_results
        )

        assert len(frames) == 3
        assert frames[0].status == "complete"
        assert frames[1].status == "failed"
        assert frames[2].status == "complete"

    @mock.patch('apps.assets.services.frame_captioning.get_vllm_client')
    def test_caption_frames_batch_vllm_unavailable(self, mock_get_client):
        """Test batch captioning when vLLM is unavailable."""
        mock_client = mock.Mock()
        mock_client.is_available.return_value = False
        mock_get_client.return_value = mock_client

        frame_data = [
            {"timestamp_sec": 0.0, "image_data": b"fake_image_data_1"},
            {"timestamp_sec": 2.0, "image_data": b"fake_image_data_2"},
        ]

        results = FrameCaptioningService.caption_frames_batch(
            frame_data=frame_data,
            batch_size=4
        )

        assert len(results) == 2
        assert all(r["caption"] == "" for r in results)
        assert all("unavailable" in r["error"].lower() for r in results)

    @mock.patch('apps.assets.services.frame_captioning.get_vllm_client')
    @mock.patch('tempfile.NamedTemporaryFile')
    def test_caption_frames_batch_success(self, mock_temp_file, mock_get_client):
        """Test successful batch captioning."""
        # Mock vLLM client
        mock_client = mock.Mock()
        mock_client.is_available.return_value = True
        mock_client.caption_images_batch.return_value = [
            ("/tmp/frame1.jpg", "Caption 1", None),
            ("/tmp/frame2.jpg", "Caption 2", None),
        ]
        mock_get_client.return_value = mock_client

        # Mock temp files
        mock_file_1 = mock.Mock()
        mock_file_1.name = "/tmp/frame1.jpg"
        mock_file_2 = mock.Mock()
        mock_file_2.name = "/tmp/frame2.jpg"
        mock_temp_file.side_effect = [mock_file_1, mock_file_2]

        frame_data = [
            {"timestamp_sec": 0.0, "image_data": b"fake_image_data_1"},
            {"timestamp_sec": 2.0, "image_data": b"fake_image_data_2"},
        ]

        results = FrameCaptioningService.caption_frames_batch(
            frame_data=frame_data,
            batch_size=4
        )

        assert len(results) == 2
        assert results[0]["caption"] == "Caption 1"
        assert results[1]["caption"] == "Caption 2"
        assert results[0]["error"] is None
        assert results[1]["error"] is None

    @mock.patch('apps.assets.services.frame_captioning.FrameCaptioningService.extract_frames_for_clip')
    @mock.patch('apps.assets.services.frame_captioning.FrameCaptioningService.caption_frames_batch')
    def test_extract_and_caption_clip_success(self, mock_caption, mock_extract):
        """Test full extraction and captioning workflow."""
        # Mock frame extraction
        mock_extract.return_value = [
            {"timestamp_sec": 0.0, "image_data": b"data1"},
            {"timestamp_sec": 2.0, "image_data": b"data2"},
        ]

        # Mock captioning
        mock_caption.return_value = [
            {"timestamp_sec": 0.0, "caption": "Caption 1", "error": None},
            {"timestamp_sec": 2.0, "caption": "Caption 2", "error": None},
        ]

        config = {
            "frame_interval_sec": 2.0,
            "caption_batch_size": 4
        }

        result = FrameCaptioningService.extract_and_caption_clip(
            clip=self.clip,
            video_file_path="/fake/path.mp4",
            config=config
        )

        assert result["frames_created"] == 2
        assert result["frames_captioned"] == 2
        assert result["frames_pending"] == 0
        assert result["frames_failed"] == 0
        assert len(result["errors"]) == 0

        # Verify frames in database
        frames = ClipFrame.objects.filter(clip=self.clip)
        assert frames.count() == 2

    @mock.patch('apps.assets.services.frame_captioning.FrameCaptioningService.extract_frames_for_clip')
    def test_extract_and_caption_clip_extraction_failure(self, mock_extract):
        """Test handling of frame extraction failure."""
        mock_extract.side_effect = RuntimeError("Video file corrupted")

        config = {
            "frame_interval_sec": 2.0,
            "caption_batch_size": 4
        }

        result = FrameCaptioningService.extract_and_caption_clip(
            clip=self.clip,
            video_file_path="/fake/path.mp4",
            config=config
        )

        assert result["frames_created"] == 0
        assert result["frames_captioned"] == 0
        assert len(result["errors"]) > 0
        assert "Frame extraction failed" in result["errors"][0]

    @mock.patch('apps.assets.services.frame_captioning.FrameCaptioningService.extract_frames_for_clip')
    @mock.patch('apps.assets.services.frame_captioning.FrameCaptioningService.caption_frames_batch')
    def test_extract_and_caption_clip_captioning_failure(self, mock_caption, mock_extract):
        """Test handling of captioning failure."""
        # Extraction succeeds
        mock_extract.return_value = [
            {"timestamp_sec": 0.0, "image_data": b"data1"},
        ]

        # Captioning fails
        mock_caption.side_effect = Exception("vLLM timeout")

        config = {
            "frame_interval_sec": 2.0,
            "caption_batch_size": 4
        }

        result = FrameCaptioningService.extract_and_caption_clip(
            clip=self.clip,
            video_file_path="/fake/path.mp4",
            config=config
        )

        # Frames should still be created with pending status
        assert result["frames_created"] == 1
        assert result["frames_captioned"] == 0
        assert result["frames_pending"] == 1
        assert len(result["errors"]) > 0

        # Verify frame in database with pending status
        frame = ClipFrame.objects.get(clip=self.clip)
        assert frame.status == "pending"
