import pytest
import json
from io import StringIO
from django.core.management import call_command, CommandError
from django.utils import timezone
from unittest.mock import patch, Mock
from apps.assets.models import AssetClip, ClipFrame, AssetVideo, AssetGroup


@pytest.mark.django_db
class TestGenerateClipDescriptionCommand:

    @pytest.fixture
    def clip_with_frames(self):
        """Create a clip with sufficient captioned frames."""
        from django.contrib.auth import get_user_model
        User = get_user_model()

        user = User.objects.create_user(email="test@example.com", password="testpass123")
        group = AssetGroup.objects.create(name="Test Group", owner=user)
        video = AssetVideo.objects.create(
            group=group,
            mime_type="video/mp4",
            size_bytes=1000,
            duration_sec=30.0,
        )
        clip = AssetClip.objects.create(
            video=video,
            index=0,
            start_sec=0.0,
            end_sec=30.0,
            duration_sec=30.0,
        )

        # Add 5 captioned frames
        for i in range(5):
            ClipFrame.objects.create(
                clip=clip,
                timestamp_sec=i * 5.0,
                caption_text=f"Frame {i} caption text",
                status="complete",
            )

        return clip

    def test_successful_description_generation(self, clip_with_frames):
        """Test successful description generation for valid clip."""
        with patch('apps.assets.management.commands.generate_clip_description.get_grok_client') as mock_client:
            # Mock Grok service
            mock_service = Mock()
            mock_service.is_available.return_value = True
            mock_service.generate_description.return_value = "Test description of the clip"
            mock_service.model = "grok-4-fast"
            mock_client.return_value = mock_service

            # Call command
            out = StringIO()
            call_command('generate_clip_description', str(clip_with_frames.id), stdout=out)

            # Check output
            result = json.loads(out.getvalue())
            assert result["success"] is True
            assert result["description"] == "Test description of the clip"
            assert result["clip_id"] == str(clip_with_frames.id)
            assert result["model"] == "grok-4-fast"
            assert result["skipped"] is False
            assert result["error"] is None

            # Check database
            clip_with_frames.refresh_from_db()
            assert clip_with_frames.description == "Test description of the clip"
            assert clip_with_frames.description_model == "grok-4-fast"
            assert clip_with_frames.description_generated_at is not None
            assert clip_with_frames.description_error == ""

    def test_clip_not_found(self):
        """Test error when clip doesn't exist."""
        with pytest.raises(CommandError, match="Clip not found"):
            call_command('generate_clip_description', '00000000-0000-0000-0000-000000000000')

    def test_grok_service_unavailable(self, clip_with_frames):
        """Test error when Grok service is not available."""
        with patch('apps.assets.management.commands.generate_clip_description.get_grok_client') as mock_client:
            mock_service = Mock()
            mock_service.is_available.return_value = False
            mock_client.return_value = mock_service

            with pytest.raises(CommandError, match="Grok service is not available"):
                call_command('generate_clip_description', str(clip_with_frames.id))

    def test_insufficient_frames(self, clip_with_frames):
        """Test handling of clips with insufficient frames."""
        # Delete all but 2 frames
        clip_with_frames.frames.all()[2:].delete()

        with patch('apps.assets.management.commands.generate_clip_description.get_grok_client') as mock_client:
            mock_service = Mock()
            mock_service.is_available.return_value = True
            mock_service.generate_description.return_value = None  # Service returns None
            mock_client.return_value = mock_service

            out = StringIO()
            call_command('generate_clip_description', str(clip_with_frames.id), stdout=out)

            result = json.loads(out.getvalue())
            assert result["success"] is False
            assert result["skipped"] is True
            assert "Insufficient" in result["skip_reason"]
            assert result["error"] is None

    def test_api_error_handling(self, clip_with_frames):
        """Test graceful handling of API errors."""
        with patch('apps.assets.management.commands.generate_clip_description.get_grok_client') as mock_client:
            mock_service = Mock()
            mock_service.is_available.return_value = True
            mock_service.generate_description.side_effect = Exception("API Error: Rate limit exceeded")
            mock_service.model = "grok-4-fast"
            mock_client.return_value = mock_service

            out = StringIO()
            call_command('generate_clip_description', str(clip_with_frames.id), stdout=out)

            result = json.loads(out.getvalue())
            assert result["success"] is False
            assert result["skipped"] is False
            assert "API Error" in result["error"]

            # Check error saved to database
            clip_with_frames.refresh_from_db()
            assert "API Error" in clip_with_frames.description_error
