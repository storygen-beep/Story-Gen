import json
from io import StringIO
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError


class TestCaptionImageCommand:
    """Test suite for caption_image management command."""

    @pytest.fixture
    def mock_client(self):
        """Mock VLLMCaptioningClient."""
        client = MagicMock()
        client.is_available.return_value = True
        client.caption_image.return_value = "A test caption"
        client.max_tokens = 64
        client.temperature = 0.6
        client.timeout = 60
        client._client = None
        return client

    @pytest.fixture
    def temp_image(self, tmp_path):
        """Create temporary test image."""
        from PIL import Image

        img_path = tmp_path / "test.jpg"
        img = Image.new("RGB", (100, 100), color="red")
        img.save(img_path)
        return str(img_path)

    def test_basic_usage(self, mock_client, temp_image):
        """Test basic command with default parameters."""
        with patch(
            "apps.assets.management.commands.caption_image.get_vllm_client",
            return_value=mock_client,
        ):
            out = StringIO()
            call_command("caption_image", "--path", temp_image, stdout=out)

            assert out.getvalue().strip() == "A test caption"
            mock_client.caption_image.assert_called_once()

    def test_custom_prompt(self, mock_client, temp_image):
        """Test custom prompt parameter."""
        with patch(
            "apps.assets.management.commands.caption_image.get_vllm_client",
            return_value=mock_client,
        ):
            out = StringIO()
            call_command(
                "caption_image",
                "--path",
                temp_image,
                "--prompt",
                "Custom prompt",
                stdout=out,
            )

            # Verify custom prompt was passed
            call_args = mock_client.caption_image.call_args
            assert call_args[1]["prompt"] == "Custom prompt"

    def test_custom_system_prompt(self, mock_client, temp_image):
        """Test custom system_prompt parameter."""
        with patch(
            "apps.assets.management.commands.caption_image.get_vllm_client",
            return_value=mock_client,
        ):
            out = StringIO()
            call_command(
                "caption_image",
                "--path",
                temp_image,
                "--system-prompt",
                "Custom system prompt",
                stdout=out,
            )

            # Verify custom system prompt was passed
            call_args = mock_client.caption_image.call_args
            assert call_args[1]["system_prompt"] == "Custom system prompt"

    def test_custom_temperature(self, mock_client, temp_image):
        """Test custom temperature parameter."""
        # Capture temperature when caption_image is called
        captured_temp = None

        def capture_temp(*args, **kwargs):
            nonlocal captured_temp
            captured_temp = mock_client.temperature
            return "A test caption"

        mock_client.caption_image.side_effect = capture_temp

        with patch(
            "apps.assets.management.commands.caption_image.get_vllm_client",
            return_value=mock_client,
        ):
            out = StringIO()
            call_command(
                "caption_image",
                "--path",
                temp_image,
                "--temperature",
                "0.8",
                stdout=out,
            )

            # Verify temperature was set during execution
            assert captured_temp == 0.8
            # Should be restored after execution
            assert mock_client.temperature == 0.6

    def test_custom_max_tokens(self, mock_client, temp_image):
        """Test custom max_tokens parameter."""
        # Capture max_tokens when caption_image is called
        captured_tokens = None

        def capture_tokens(*args, **kwargs):
            nonlocal captured_tokens
            captured_tokens = mock_client.max_tokens
            return "A test caption"

        mock_client.caption_image.side_effect = capture_tokens

        with patch(
            "apps.assets.management.commands.caption_image.get_vllm_client",
            return_value=mock_client,
        ):
            out = StringIO()
            call_command(
                "caption_image", "--path", temp_image, "--max-tokens", "128", stdout=out
            )

            # Verify max_tokens was set during execution
            assert captured_tokens == 128
            # Should be restored after execution
            assert mock_client.max_tokens == 64

    def test_custom_timeout(self, mock_client, temp_image):
        """Test custom timeout parameter."""
        # Capture timeout when caption_image is called
        captured_timeout = None

        def capture_timeout(*args, **kwargs):
            nonlocal captured_timeout
            captured_timeout = mock_client.timeout
            return "A test caption"

        mock_client.caption_image.side_effect = capture_timeout

        with patch(
            "apps.assets.management.commands.caption_image.get_vllm_client",
            return_value=mock_client,
        ):
            out = StringIO()
            call_command(
                "caption_image", "--path", temp_image, "--timeout", "90", stdout=out
            )

            # Verify timeout was set during execution
            assert captured_timeout == 90
            # Should be restored after execution
            assert mock_client.timeout == 60

    def test_json_output(self, mock_client, temp_image):
        """Test JSON output format."""
        with patch(
            "apps.assets.management.commands.caption_image.get_vllm_client",
            return_value=mock_client,
        ):
            out = StringIO()
            call_command("caption_image", "--path", temp_image, "--json", stdout=out)

            result = json.loads(out.getvalue())
            assert result["success"] is True
            assert result["caption"] == "A test caption"
            assert "parameters" in result
            assert "image" in result
            assert result["image"]["name"] == "test.jpg"

    def test_verbose_output(self, mock_client, temp_image):
        """Test verbose output mode."""
        with patch(
            "apps.assets.management.commands.caption_image.get_vllm_client",
            return_value=mock_client,
        ):
            out = StringIO()
            call_command(
                "caption_image", "--path", temp_image, "--verbose", stdout=out
            )

            output = out.getvalue()
            assert "Captioning Parameters:" in output
            assert "Prompt:" in output
            assert "Temperature:" in output
            assert "Max Tokens:" in output

    def test_verbose_and_json_combined(self, mock_client, temp_image):
        """Test verbose and JSON output combined."""
        with patch(
            "apps.assets.management.commands.caption_image.get_vllm_client",
            return_value=mock_client,
        ):
            out = StringIO()
            call_command(
                "caption_image",
                "--path",
                temp_image,
                "--verbose",
                "--json",
                stdout=out,
            )

            output = out.getvalue()
            assert "Captioning Parameters:" in output
            # JSON should be after verbose output
            assert "{" in output
            # Verify JSON is valid
            json_start = output.index("{")
            result = json.loads(output[json_start:])
            assert result["success"] is True

    def test_temperature_validation_too_low(self, mock_client, temp_image):
        """Test temperature validation - too low."""
        with patch(
            "apps.assets.management.commands.caption_image.get_vllm_client",
            return_value=mock_client,
        ):
            with pytest.raises(CommandError, match="Temperature must be between"):
                call_command(
                    "caption_image", "--path", temp_image, "--temperature", "-0.1"
                )

    def test_temperature_validation_too_high(self, mock_client, temp_image):
        """Test temperature validation - too high."""
        with patch(
            "apps.assets.management.commands.caption_image.get_vllm_client",
            return_value=mock_client,
        ):
            with pytest.raises(CommandError, match="Temperature must be between"):
                call_command(
                    "caption_image", "--path", temp_image, "--temperature", "2.5"
                )

    def test_max_tokens_validation_too_low(self, mock_client, temp_image):
        """Test max_tokens validation - too low."""
        with patch(
            "apps.assets.management.commands.caption_image.get_vllm_client",
            return_value=mock_client,
        ):
            with pytest.raises(CommandError, match="Max tokens must be between"):
                call_command("caption_image", "--path", temp_image, "--max-tokens", "0")

    def test_max_tokens_validation_too_high(self, mock_client, temp_image):
        """Test max_tokens validation - too high."""
        with patch(
            "apps.assets.management.commands.caption_image.get_vllm_client",
            return_value=mock_client,
        ):
            with pytest.raises(CommandError, match="Max tokens must be between"):
                call_command(
                    "caption_image", "--path", temp_image, "--max-tokens", "1000"
                )

    def test_timeout_validation_too_low(self, mock_client, temp_image):
        """Test timeout validation - too low."""
        with patch(
            "apps.assets.management.commands.caption_image.get_vllm_client",
            return_value=mock_client,
        ):
            with pytest.raises(CommandError, match="Timeout must be between"):
                call_command("caption_image", "--path", temp_image, "--timeout", "2")

    def test_timeout_validation_too_high(self, mock_client, temp_image):
        """Test timeout validation - too high."""
        with patch(
            "apps.assets.management.commands.caption_image.get_vllm_client",
            return_value=mock_client,
        ):
            with pytest.raises(CommandError, match="Timeout must be between"):
                call_command("caption_image", "--path", temp_image, "--timeout", "400")

    def test_backward_compatibility_max_new_tokens(self, mock_client, temp_image):
        """Test backward compatibility with --max-new-tokens."""
        # Capture max_tokens when caption_image is called
        captured_tokens = None

        def capture_tokens(*args, **kwargs):
            nonlocal captured_tokens
            captured_tokens = mock_client.max_tokens
            return "A test caption"

        mock_client.caption_image.side_effect = capture_tokens

        with patch(
            "apps.assets.management.commands.caption_image.get_vllm_client",
            return_value=mock_client,
        ):
            out = StringIO()
            call_command(
                "caption_image",
                "--path",
                temp_image,
                "--max-new-tokens",
                "128",
                stdout=out,
            )

            # Should set max_tokens on client during execution
            assert captured_tokens == 128

    def test_max_tokens_priority_over_max_new_tokens(self, mock_client, temp_image):
        """Test that --max-tokens overrides --max-new-tokens."""
        # Capture max_tokens when caption_image is called
        captured_tokens = None

        def capture_tokens(*args, **kwargs):
            nonlocal captured_tokens
            captured_tokens = mock_client.max_tokens
            return "A test caption"

        mock_client.caption_image.side_effect = capture_tokens

        with patch(
            "apps.assets.management.commands.caption_image.get_vllm_client",
            return_value=mock_client,
        ):
            out = StringIO()
            call_command(
                "caption_image",
                "--path",
                temp_image,
                "--max-tokens",
                "256",
                "--max-new-tokens",
                "128",  # Should be ignored
                stdout=out,
            )

            # --max-tokens should override --max-new-tokens
            assert captured_tokens == 256

    def test_image_not_found(self, mock_client):
        """Test error handling for missing image."""
        with patch(
            "apps.assets.management.commands.caption_image.get_vllm_client",
            return_value=mock_client,
        ):
            with pytest.raises(CommandError, match="Image not found"):
                call_command("caption_image", "--path", "/nonexistent/image.jpg")

    def test_service_unavailable(self, mock_client, temp_image):
        """Test error handling when vLLM service is unavailable."""
        mock_client.is_available.return_value = False

        with patch(
            "apps.assets.management.commands.caption_image.get_vllm_client",
            return_value=mock_client,
        ):
            with pytest.raises(
                CommandError, match="vLLM captioning service is not available"
            ):
                call_command("caption_image", "--path", temp_image)

    def test_parameter_restoration(self, mock_client, temp_image):
        """Test that client parameters are restored after command."""
        original_temp = 0.6
        original_tokens = 64
        original_timeout = 60

        mock_client.temperature = original_temp
        mock_client.max_tokens = original_tokens
        mock_client.timeout = original_timeout

        with patch(
            "apps.assets.management.commands.caption_image.get_vllm_client",
            return_value=mock_client,
        ):
            call_command(
                "caption_image",
                "--path",
                temp_image,
                "--temperature",
                "0.9",
                "--max-tokens",
                "128",
                "--timeout",
                "90",
            )

            # Parameters should be restored
            assert mock_client.temperature == original_temp
            assert mock_client.max_tokens == original_tokens
            assert mock_client.timeout == original_timeout

    def test_api_error_handling(self, mock_client, temp_image):
        """Test graceful handling of API errors."""
        mock_client.caption_image.side_effect = Exception("API Error: Test failure")

        with patch(
            "apps.assets.management.commands.caption_image.get_vllm_client",
            return_value=mock_client,
        ):
            with pytest.raises(CommandError, match="Captioning failed"):
                call_command("caption_image", "--path", temp_image)

    def test_all_custom_parameters_combined(self, mock_client, temp_image):
        """Test all custom parameters combined."""
        # Capture all parameters when caption_image is called
        captured_params = {}

        def capture_params(*args, **kwargs):
            captured_params["temperature"] = mock_client.temperature
            captured_params["max_tokens"] = mock_client.max_tokens
            captured_params["timeout"] = mock_client.timeout
            return "A test caption"

        mock_client.caption_image.side_effect = capture_params

        with patch(
            "apps.assets.management.commands.caption_image.get_vllm_client",
            return_value=mock_client,
        ):
            out = StringIO()
            call_command(
                "caption_image",
                "--path",
                temp_image,
                "--prompt",
                "Test prompt",
                "--system-prompt",
                "Test system",
                "--temperature",
                "0.7",
                "--max-tokens",
                "100",
                "--timeout",
                "45",
                "--json",
                "--verbose",
                stdout=out,
            )

            output = out.getvalue()

            # Verify verbose output
            assert "Captioning Parameters:" in output

            # Verify JSON output
            json_start = output.index("{")
            result = json.loads(output[json_start:])

            assert result["success"] is True
            assert result["caption"] == "A test caption"
            assert result["parameters"]["prompt"] == "Test prompt"
            assert result["parameters"]["system_prompt"] == "Test system"
            assert result["parameters"]["temperature"] == 0.7
            assert result["parameters"]["max_tokens"] == 100
            assert result["parameters"]["timeout"] == 45

            # Verify client was configured during execution
            assert captured_params["temperature"] == 0.7
            assert captured_params["max_tokens"] == 100
            assert captured_params["timeout"] == 45

            # Verify prompts were passed
            call_args = mock_client.caption_image.call_args
            assert call_args[1]["prompt"] == "Test prompt"
            assert call_args[1]["system_prompt"] == "Test system"

            # Verify parameters were restored after execution
            assert mock_client.temperature == 0.6
            assert mock_client.max_tokens == 64
            assert mock_client.timeout == 60
