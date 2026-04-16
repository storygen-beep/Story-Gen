"""Unit tests for video_file_utils module."""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from apps.assets.services.video_file_utils import (
    sanitize_caption_for_filename,
    parse_captioned_filename,
    is_frame_captioned,
    rename_frame_with_caption,
    extract_frames_from_video,
)


class TestSanitizeCaptionForFilename:
    """Tests for caption sanitization function."""

    def test_removes_unsafe_characters(self):
        """Test that filesystem-unsafe characters are removed."""
        caption = 'A video / with : special * chars ? " < > |'
        result = sanitize_caption_for_filename(caption)

        # All unsafe chars should be replaced with space
        assert '/' not in result
        assert ':' not in result
        assert '*' not in result
        assert '?' not in result
        assert '"' not in result
        assert '<' not in result
        assert '>' not in result
        assert '|' not in result

    def test_collapses_multiple_spaces(self):
        """Test that multiple spaces are collapsed."""
        caption = 'A   video    with     many      spaces'
        result = sanitize_caption_for_filename(caption)

        assert '  ' not in result  # No double spaces
        assert result == 'A video with many spaces'

    def test_truncates_long_captions(self):
        """Test that long captions are truncated to max length."""
        long_caption = 'A ' * 100  # Very long caption
        result = sanitize_caption_for_filename(long_caption, max_length=60)

        assert len(result) <= 60

    def test_truncates_at_word_boundary(self):
        """Test that truncation happens at word boundaries."""
        caption = 'The quick brown fox jumps over the lazy dog'
        result = sanitize_caption_for_filename(caption, max_length=20)

        # Should truncate at word boundary, not mid-word
        assert not result.endswith('fox')  # Shouldn't cut mid-word
        assert result == 'The quick brown fox'

    def test_strips_whitespace(self):
        """Test that leading/trailing whitespace is stripped."""
        caption = '  A caption with spaces  '
        result = sanitize_caption_for_filename(caption)

        assert result == 'A caption with spaces'
        assert not result.startswith(' ')
        assert not result.endswith(' ')

    def test_empty_caption(self):
        """Test handling of empty caption."""
        result = sanitize_caption_for_filename('')
        assert result == ''

    def test_only_unsafe_characters(self):
        """Test caption with only unsafe characters."""
        caption = '/:*?"<>|'
        result = sanitize_caption_for_filename(caption)

        # Should result in empty string after stripping
        assert result == ''


class TestParseCaptionedFilename:
    """Tests for filename parsing function."""

    def test_parses_captioned_filename(self):
        """Test parsing filename with caption."""
        filename = 'frame_002.50_A woman dancing.jpg'
        prefix, timestamp, caption = parse_captioned_filename(filename)

        assert prefix == 'frame'
        assert timestamp == 2.5
        assert caption == 'A woman dancing'

    def test_parses_uncaptioned_filename(self):
        """Test parsing filename without caption."""
        filename = 'frame_002.50.jpg'
        prefix, timestamp, caption = parse_captioned_filename(filename)

        assert prefix == 'frame'
        assert timestamp == 2.5
        assert caption == ''

    def test_invalid_filename_format(self):
        """Test that invalid filename raises ValueError."""
        with pytest.raises(ValueError):
            parse_captioned_filename('invalid.jpg')

    def test_invalid_timestamp(self):
        """Test that invalid timestamp raises ValueError."""
        with pytest.raises(ValueError):
            parse_captioned_filename('frame_invalid_caption.jpg')


class TestIsFrameCaptioned:
    """Tests for caption detection function."""

    def test_detects_captioned_frame(self):
        """Test detection of captioned frame."""
        frame_path = Path('frame_002.50_A woman dancing.jpg')
        assert is_frame_captioned(frame_path) is True

    def test_detects_uncaptioned_frame(self):
        """Test detection of uncaptioned frame."""
        frame_path = Path('frame_002.50.jpg')
        assert is_frame_captioned(frame_path) is False

    def test_handles_invalid_filename(self):
        """Test handling of invalid filename format."""
        frame_path = Path('invalid.jpg')
        assert is_frame_captioned(frame_path) is False


class TestRenameFrameWithCaption:
    """Tests for frame renaming function."""

    def test_renames_frame_with_caption(self, tmp_path):
        """Test renaming frame with caption."""
        # Create a test frame file
        frame_path = tmp_path / 'frame_002.50.jpg'
        frame_path.write_text('test')

        # Rename with caption
        new_path = rename_frame_with_caption(
            frame_path,
            'A woman dancing in the park',
            max_length=30
        )

        # Check new filename
        assert new_path.exists()
        assert not frame_path.exists()  # Old file should be gone
        assert 'A woman dancing' in new_path.name
        assert new_path.name.startswith('frame_002.50_')

    def test_sanitizes_caption_in_filename(self, tmp_path):
        """Test that caption is sanitized when renaming."""
        frame_path = tmp_path / 'frame_002.50.jpg'
        frame_path.write_text('test')

        new_path = rename_frame_with_caption(
            frame_path,
            'A video / with : special chars',
            max_length=60
        )

        # Unsafe characters should be removed
        assert '/' not in new_path.name
        assert ':' not in new_path.name

    def test_raises_error_for_missing_file(self, tmp_path):
        """Test that missing file raises FileNotFoundError."""
        frame_path = tmp_path / 'nonexistent.jpg'

        with pytest.raises(FileNotFoundError):
            rename_frame_with_caption(frame_path, 'Test caption')

    def test_preserves_extension(self, tmp_path):
        """Test that file extension is preserved."""
        frame_path = tmp_path / 'frame_002.50.jpg'
        frame_path.write_text('test')

        new_path = rename_frame_with_caption(frame_path, 'Test')

        assert new_path.suffix == '.jpg'


class TestExtractFramesFromVideo:
    """Tests for frame extraction function."""

    @patch('apps.assets.services.video_file_utils._probe_metadata')
    @patch('apps.assets.services.video_file_utils._extract_frame')
    @patch('apps.assets.services.video_file_utils._ensure_dir')
    def test_extracts_frames_at_intervals(
        self,
        mock_ensure_dir,
        mock_extract_frame,
        mock_probe_metadata,
        tmp_path
    ):
        """Test that frames are extracted at correct intervals."""
        # Mock video duration
        mock_probe_metadata.return_value = (1920, 1080, 10.0)  # 10 second video
        mock_extract_frame.return_value = True

        video_path = tmp_path / 'test.mp4'
        video_path.write_text('fake video')

        output_dir = tmp_path / 'frames'

        # Extract frames every 2 seconds
        frames = extract_frames_from_video(
            video_path,
            output_dir,
            interval_sec=2.0
        )

        # Should extract at 0, 2, 4, 6, 8, 10 = 6 frames
        assert mock_extract_frame.call_count == 6

        # Check timestamps
        timestamps = [call[0][1] for call in mock_extract_frame.call_args_list]
        assert timestamps == [0.0, 2.0, 4.0, 6.0, 8.0, 10.0]

    @patch('apps.assets.services.video_file_utils._probe_metadata')
    def test_handles_invalid_duration(self, mock_probe_metadata, tmp_path):
        """Test handling of invalid video duration."""
        mock_probe_metadata.return_value = (1920, 1080, 0.0)  # Invalid duration

        video_path = tmp_path / 'test.mp4'
        video_path.write_text('fake video')

        with pytest.raises(RuntimeError, match='Invalid video duration'):
            extract_frames_from_video(video_path, tmp_path / 'frames')

    @patch('apps.assets.services.video_file_utils._probe_metadata')
    @patch('apps.assets.services.video_file_utils._extract_frame')
    @patch('apps.assets.services.video_file_utils._ensure_dir')
    def test_handles_frame_extraction_failure(
        self,
        mock_ensure_dir,
        mock_extract_frame,
        mock_probe_metadata,
        tmp_path
    ):
        """Test handling when some frames fail to extract."""
        mock_probe_metadata.return_value = (1920, 1080, 6.0)

        # Simulate some frames failing
        mock_extract_frame.side_effect = [True, False, True]  # Middle frame fails

        video_path = tmp_path / 'test.mp4'
        video_path.write_text('fake video')

        frames = extract_frames_from_video(
            video_path,
            tmp_path / 'frames',
            interval_sec=2.0
        )

        # Should only return successful extractions
        # With side_effect, only frames at 0.0 and 4.0 should succeed
        assert len(frames) == 2
