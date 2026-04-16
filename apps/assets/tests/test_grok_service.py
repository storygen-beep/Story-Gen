import pytest
from unittest.mock import Mock, patch, MagicMock
from django.utils import timezone
from apps.assets.services.grok_clip_service import (
    GrokClipDescriptionClient,
    generate_clip_description,
    get_grok_client
)
from apps.assets.models import AssetClip, ClipFrame


@pytest.fixture
def mock_settings():
    """Mock Django settings for Grok."""
    return {
        "enabled": True,
        "api_key": "test-api-key",
        "api_base_url": "https://api.x.ai/v1",
        "model": "grok-4-fast",
        "temperature": 0.7,
        "max_tokens": 800,
        "min_frames": 3,
        "timeout": 30,
    }


@pytest.fixture
def clip_with_frames(db):
    """Create clip with multiple captioned frames."""
    from apps.assets.models import AssetVideo, AssetGroup
    from django.contrib.auth import get_user_model

    User = get_user_model()
    user = User.objects.create_user(email="test@example.com", password="testpass123")
    group = AssetGroup.objects.create(name="Test Group", owner=user)
    video = AssetVideo.objects.create(
        group=group,
        mime_type="video/mp4",
        size_bytes=1000000,
        duration_sec=30.0,
    )
    clip = AssetClip.objects.create(
        video=video,
        index=0,
        start_sec=0.0,
        end_sec=30.0,
        duration_sec=30.0,
    )

    # Add captioned frames
    for i in range(5):
        ClipFrame.objects.create(
            clip=clip,
            timestamp_sec=i * 5.0,
            caption_text=f"Frame {i} showing test content",
            status="complete"
        )

    return clip


@pytest.mark.django_db
class TestGrokClipDescriptionClient:

    @patch('apps.assets.services.grok_clip_service.settings')
    def test_client_initialization(self, mock_settings_module, mock_settings):
        """Test client initializes from settings."""
        mock_settings_module.GROK_CLIP_DESCRIPTIONS = mock_settings

        with patch('apps.assets.services.grok_clip_service.OpenAI'):
            client = GrokClipDescriptionClient()

            assert client.enabled is True
            assert client.api_key == "test-api-key"
            assert client.model == "grok-4-fast"
            assert client.temperature == 0.7
            assert client.max_tokens == 800
            assert client.min_frames == 3

    @patch('apps.assets.services.grok_clip_service.settings')
    def test_is_available_when_enabled(self, mock_settings_module, mock_settings):
        """Test service reports available when properly configured."""
        mock_settings_module.GROK_CLIP_DESCRIPTIONS = mock_settings

        with patch('apps.assets.services.grok_clip_service.OpenAI'):
            client = GrokClipDescriptionClient()
            assert client.is_available() is True

    @patch('apps.assets.services.grok_clip_service.settings')
    def test_is_available_when_disabled(self, mock_settings_module, mock_settings):
        """Test service reports unavailable when disabled."""
        mock_settings["enabled"] = False
        mock_settings_module.GROK_CLIP_DESCRIPTIONS = mock_settings

        client = GrokClipDescriptionClient()
        assert client.is_available() is False

    @patch('apps.assets.services.grok_clip_service.settings')
    def test_is_available_when_no_api_key(self, mock_settings_module, mock_settings):
        """Test service reports unavailable when API key missing."""
        mock_settings["api_key"] = ""
        mock_settings_module.GROK_CLIP_DESCRIPTIONS = mock_settings

        client = GrokClipDescriptionClient()
        assert client.is_available() is False

    def test_build_prompt_includes_clip_metadata(self, clip_with_frames):
        """Test prompt includes clip duration and frame captions."""
        client = GrokClipDescriptionClient()
        frames = clip_with_frames.frames.all()

        prompt = client._build_prompt(clip_with_frames, frames)

        assert "Duration: 30.0 seconds" in prompt
        assert "Time range: 0.0s to 30.0s" in prompt
        assert "Number of frames: 5" in prompt
        for frame in frames:
            assert frame.caption_text in prompt
            assert f"{frame.timestamp_sec:.1f}s:" in prompt

    @patch('apps.assets.services.grok_clip_service.settings')
    @patch('apps.assets.services.grok_clip_service.OpenAI')
    def test_generate_description_success(
        self,
        mock_openai,
        mock_settings_module,
        mock_settings,
        clip_with_frames
    ):
        """Test successful description generation."""
        mock_settings_module.GROK_CLIP_DESCRIPTIONS = mock_settings

        # Mock API response
        mock_response = Mock()
        mock_response.choices = [
            Mock(message=Mock(content="A person walks across a room while talking."))
        ]
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        client = GrokClipDescriptionClient()
        description = client.generate_description(clip_with_frames)

        assert description == "A person walks across a room while talking."
        assert mock_client.chat.completions.create.called
        call_kwargs = mock_client.chat.completions.create.call_args[1]
        assert call_kwargs['model'] == 'grok-4-fast'
        assert call_kwargs['temperature'] == 0.7
        assert call_kwargs['max_tokens'] == 800

    @patch('apps.assets.services.grok_clip_service.settings')
    def test_skips_clips_with_insufficient_frames(
        self,
        mock_settings_module,
        mock_settings,
        clip_with_frames
    ):
        """Test skips clips with fewer than min_frames."""
        mock_settings_module.GROK_CLIP_DESCRIPTIONS = mock_settings

        # Delete frames to have only 2
        clip_with_frames.frames.all()[2:].delete()

        with patch('apps.assets.services.grok_clip_service.OpenAI'):
            client = GrokClipDescriptionClient()
            result = client.generate_description(clip_with_frames)

        assert result is None

    @patch('apps.assets.services.grok_clip_service.settings')
    @patch('apps.assets.services.grok_clip_service.OpenAI')
    @patch('apps.assets.services.grok_clip_service.time.sleep')
    def test_retry_logic_on_api_failure(
        self,
        mock_sleep,
        mock_openai,
        mock_settings_module,
        mock_settings,
        clip_with_frames
    ):
        """Test exponential backoff retry on API failures."""
        mock_settings_module.GROK_CLIP_DESCRIPTIONS = mock_settings

        # Mock API failure then success
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Success after retry"))]
        mock_client.chat.completions.create.side_effect = [
            Exception("API Error"),
            mock_response
        ]
        mock_openai.return_value = mock_client

        client = GrokClipDescriptionClient()
        description = client.generate_description(clip_with_frames)

        assert description == "Success after retry"
        assert mock_client.chat.completions.create.call_count == 2
        mock_sleep.assert_called_once_with(1)  # 2^0 = 1 second backoff

    @patch('apps.assets.services.grok_clip_service.settings')
    @patch('apps.assets.services.grok_clip_service.OpenAI')
    @patch('apps.assets.services.grok_clip_service.time.sleep')
    def test_retry_exhausted_raises_exception(
        self,
        mock_sleep,
        mock_openai,
        mock_settings_module,
        mock_settings,
        clip_with_frames
    ):
        """Test exception raised after all retries exhausted."""
        mock_settings_module.GROK_CLIP_DESCRIPTIONS = mock_settings

        # Mock API failure for all retries
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = Exception("Persistent API Error")
        mock_openai.return_value = mock_client

        client = GrokClipDescriptionClient()

        with pytest.raises(Exception) as exc_info:
            client.generate_description(clip_with_frames)

        assert "Persistent API Error" in str(exc_info.value)
        assert mock_client.chat.completions.create.call_count == 3  # max_retries

    @patch('apps.assets.services.grok_clip_service.settings')
    @patch('apps.assets.services.grok_clip_service.OpenAI')
    def test_process_clips_batch(
        self,
        mock_openai,
        mock_settings_module,
        mock_settings,
        clip_with_frames,
        db
    ):
        """Test batch processing of multiple clips."""
        mock_settings_module.GROK_CLIP_DESCRIPTIONS = mock_settings

        # Create second clip
        clip2 = AssetClip.objects.create(
            video=clip_with_frames.video,
            index=1,
            start_sec=30.0,
            end_sec=60.0,
            duration_sec=30.0,
        )
        for i in range(4):
            ClipFrame.objects.create(
                clip=clip2,
                timestamp_sec=30.0 + i * 7.5,
                caption_text=f"Clip 2 frame {i}",
                status="complete"
            )

        # Mock API responses
        mock_client = Mock()
        mock_response1 = Mock()
        mock_response1.choices = [Mock(message=Mock(content="Description for clip 1"))]
        mock_response2 = Mock()
        mock_response2.choices = [Mock(message=Mock(content="Description for clip 2"))]
        mock_client.chat.completions.create.side_effect = [mock_response1, mock_response2]
        mock_openai.return_value = mock_client

        client = GrokClipDescriptionClient()
        results = client.process_clips_batch([clip_with_frames, clip2], max_workers=2)

        assert len(results) == 2
        # Check that both clips got descriptions
        descriptions = [r[1] for r in results if r[1] is not None]
        assert len(descriptions) == 2
        assert "Description for clip 1" in descriptions
        assert "Description for clip 2" in descriptions

    def test_singleton_client(self):
        """Test get_grok_client returns singleton instance."""
        client1 = get_grok_client()
        client2 = get_grok_client()

        assert client1 is client2

    @patch('apps.assets.services.grok_clip_service.settings')
    @patch('apps.assets.services.grok_clip_service.OpenAI')
    def test_convenience_function(
        self,
        mock_openai,
        mock_settings_module,
        mock_settings,
        clip_with_frames
    ):
        """Test generate_clip_description convenience function."""
        mock_settings_module.GROK_CLIP_DESCRIPTIONS = mock_settings

        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Test description"))]
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        description = generate_clip_description(clip_with_frames)

        assert description == "Test description"

    @patch('apps.assets.services.grok_clip_service.settings')
    def test_service_unavailable_returns_none(
        self,
        mock_settings_module,
        mock_settings,
        clip_with_frames
    ):
        """Test returns None when service unavailable."""
        mock_settings["enabled"] = False
        mock_settings_module.GROK_CLIP_DESCRIPTIONS = mock_settings

        description = generate_clip_description(clip_with_frames)

        assert description is None

    @patch('apps.assets.services.grok_clip_service.settings')
    def test_prompt_excludes_physical_appearance(
        self, mock_settings_module, mock_settings, clip_with_frames
    ):
        """Test prompt explicitly excludes physical appearance descriptions."""
        mock_settings_module.GROK_CLIP_DESCRIPTIONS = mock_settings

        with patch('apps.assets.services.grok_clip_service.OpenAI'):
            client = GrokClipDescriptionClient()
            frames = clip_with_frames.frames.all()

            prompt = client._build_prompt(clip_with_frames, frames)

            # Verify exclusions are mentioned
            assert "Do NOT describe" in prompt
            assert "body types" in prompt
            assert "ethnicities" in prompt
            assert "breast size" in prompt
            assert "penis appearance" in prompt

            # Verify script-style instructions
            assert "script-style" in prompt.lower()
            assert "present tense" in prompt.lower()
            assert "500 words" in prompt

    @patch('apps.assets.services.grok_clip_service.settings')
    def test_prompt_includes_sexual_detail_requirements(
        self, mock_settings_module, mock_settings, clip_with_frames
    ):
        """Test prompt still requires explicit sexual content."""
        mock_settings_module.GROK_CLIP_DESCRIPTIONS = mock_settings

        with patch('apps.assets.services.grok_clip_service.OpenAI'):
            client = GrokClipDescriptionClient()
            frames = clip_with_frames.frames.all()

            prompt = client._build_prompt(clip_with_frames, frames)

            # Verify essential sexual content requirements
            assert "positions" in prompt.lower()
            assert "penetration" in prompt.lower()
            assert "bodily contact" in prompt.lower()
            assert "fluids" in prompt.lower()
            assert "genders" in prompt.lower()
