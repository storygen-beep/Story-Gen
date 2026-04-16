from __future__ import annotations

import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.assets.services.vllm_captioning import get_vllm_client


# Validation ranges for parameters
VALIDATION_RANGES = {
    "temperature": (0.0, 2.0),
    "max_tokens": (1, 512),
    "timeout": (5, 300),
}


class Command(BaseCommand):
    help = "Generate a caption for a local image using vLLM server with customizable prompts and parameters."

    def add_arguments(self, parser):
        # Required: Image path
        parser.add_argument(
            "--path",
            type=str,
            required=True,
            help="Path to the image file (e.g., /app/sample_image.webp)",
        )

        # Backward compatibility: keep --max-new-tokens
        parser.add_argument(
            "--max-new-tokens",
            type=int,
            default=None,
            help="(Deprecated: use --max-tokens) Maximum new tokens to generate",
        )

        # Prompt customization
        parser.add_argument(
            "--prompt",
            type=str,
            default=None,
            help="User prompt sent to the model (default: 'Write a short, specific caption for this image.')",
        )

        parser.add_argument(
            "--system-prompt",
            type=str,
            default=None,
            help="System prompt for model context (default: 'You are a concise, visual captioner.')",
        )

        # Parameter tuning
        parser.add_argument(
            "--temperature",
            type=float,
            default=None,
            help="Sampling temperature (0.0-2.0, default from settings: 0.6). Lower = more deterministic, higher = more creative.",
        )

        parser.add_argument(
            "--max-tokens",
            type=int,
            default=None,
            help="Maximum tokens to generate (1-512, default from settings: 64). Overrides --max-new-tokens if both specified.",
        )

        parser.add_argument(
            "--timeout",
            type=int,
            default=None,
            help="Request timeout in seconds (5-300, default from settings: 60)",
        )

        # Output control
        parser.add_argument(
            "--json",
            action="store_true",
            help="Output results as JSON with caption and metadata",
        )

        parser.add_argument(
            "--verbose",
            action="store_true",
            help="Show detailed parameter information during execution",
        )

    def handle(self, *args, **options):
        # 1. Extract and validate parameters
        params = self._extract_parameters(options)

        # 2. Validate image path
        path = Path(options["path"])
        if not path.exists():
            raise CommandError(f"Image not found: {path}")

        # 3. Display verbose info if requested
        if options["verbose"]:
            self._display_parameters(params)

        # 4. Get vLLM client directly (bypass simple wrapper)
        client = get_vllm_client()

        # 5. Check availability
        if not client.is_available():
            raise CommandError(
                "vLLM captioning service is not available. "
                "Ensure the joycaption container is running and healthy. "
                "Check with: docker ps | grep joycaption"
            )

        # 6. Temporarily override client parameters
        original_params = self._override_client_params(client, params)

        try:
            # 7. Call captioning service

            if params["prompt"] is not None or params["system_prompt"] is not None:
                caption = client.caption_image(
                    str(path),
                    prompt=params["prompt"],
                    system_prompt=params["system_prompt"],
                )
            else:
                caption = client.caption_image(
                    str(path),
                )

            # 8. Output result
            if options["json"]:
                self._output_json(caption, params, path)
            else:
                self.stdout.write(caption or "")

        except Exception as e:
            raise CommandError(f"Captioning failed: {e}")

        finally:
            # 9. Restore original client parameters
            self._restore_client_params(client, original_params)

    def _extract_parameters(self, options):
        """Extract and validate all captioning parameters."""
        config = getattr(settings, "VLLM_CAPTIONING", {})

        # Handle backward compatibility: --max-new-tokens vs --max-tokens
        max_tokens = options.get("max_tokens")
        if max_tokens is None:
            max_tokens = options.get("max_new_tokens")
        if max_tokens is None:
            max_tokens = config.get("max_tokens", 64)

        params = {
            "prompt": options["prompt"],
            "system_prompt": options["system_prompt"],
            "max_tokens": max_tokens,
            "temperature": options.get("temperature") or config.get("temperature", 0.6),
            "timeout": options.get("timeout") or config.get("timeout", 60),
        }

        # Validate parameters
        self._validate_parameters(params)

        return params

    def _validate_parameters(self, params):
        """Validate parameter ranges."""
        # Validate temperature
        temp_min, temp_max = VALIDATION_RANGES["temperature"]
        if not (temp_min <= params["temperature"] <= temp_max):
            raise CommandError(
                f"Temperature must be between {temp_min} and {temp_max}. "
                f"Got: {params['temperature']}\n"
                "  Temperature controls randomness. 0.0 = deterministic, 2.0 = very creative. Recommended: 0.3-1.0"
            )

        # Validate max_tokens
        tokens_min, tokens_max = VALIDATION_RANGES["max_tokens"]
        if not (tokens_min <= params["max_tokens"] <= tokens_max):
            raise CommandError(
                f"Max tokens must be between {tokens_min} and {tokens_max}. "
                f"Got: {params['max_tokens']}\n"
                "  Maximum tokens for caption. Short captions: 32-64, detailed: 128-256"
            )

        # Validate timeout
        timeout_min, timeout_max = VALIDATION_RANGES["timeout"]
        if not (timeout_min <= params["timeout"] <= timeout_max):
            raise CommandError(
                f"Timeout must be between {timeout_min} and {timeout_max} seconds. "
                f"Got: {params['timeout']}\n"
                "  Request timeout in seconds. Increase for slower connections or larger images."
            )

    def _override_client_params(self, client, params):
        """Temporarily override client parameters for this request."""
        original = {
            "max_tokens": client.max_tokens,
            "temperature": client.temperature,
            "timeout": client.timeout,
        }

        client.max_tokens = params["max_tokens"]
        client.temperature = params["temperature"]
        client.timeout = params["timeout"]

        # Also update the lazy-loaded OpenAI client timeout if it exists
        if client._client is not None:
            client._client.timeout = params["timeout"]

        return original

    def _restore_client_params(self, client, original):
        """Restore original client parameters."""
        client.max_tokens = original["max_tokens"]
        client.temperature = original["temperature"]
        client.timeout = original["timeout"]

        if client._client is not None:
            client._client.timeout = original["timeout"]

    def _display_parameters(self, params):
        """Display parameter information in verbose mode."""
        self.stdout.write(self.style.SUCCESS("\nCaptioning Parameters:"))
        self.stdout.write(f"  Prompt: {params['prompt']}")
        self.stdout.write(f"  System Prompt: {params['system_prompt']}")
        self.stdout.write(f"  Max Tokens: {params['max_tokens']}")
        self.stdout.write(f"  Temperature: {params['temperature']}")
        self.stdout.write(f"  Timeout: {params['timeout']}s")
        self.stdout.write("")

    def _output_json(self, caption, params, path):
        """Output results as JSON with metadata."""
        result = {
            "success": True,
            "caption": caption,
            "image": {
                "path": str(path),
                "name": path.name,
                "size": path.stat().st_size,
            },
            "parameters": {
                "prompt": params["prompt"],
                "system_prompt": params["system_prompt"],
                "max_tokens": params["max_tokens"],
                "temperature": params["temperature"],
                "timeout": params["timeout"],
            },
        }

        self.stdout.write(json.dumps(result, indent=2))
