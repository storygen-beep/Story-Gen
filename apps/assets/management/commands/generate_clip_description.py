from __future__ import annotations

import json
from typing import Any
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from apps.assets.models import AssetClip
from apps.assets.services.grok_clip_service import get_grok_client


class Command(BaseCommand):
    help = "Generate AI description for a specific clip using Grok AI"

    def add_arguments(self, parser):
        """Define command arguments."""
        parser.add_argument(
            "clip_id",
            type=str,
            help="UUID of the clip to generate description for",
        )

    def handle(self, *args, **options) -> None:
        """Main command logic."""
        clip_id: str = options["clip_id"]

        # 1. Validate Grok service is available
        client = get_grok_client()
        if not client.is_available():
            raise CommandError(
                "Grok service is not available. "
                "Check GROK_CLIP_DESCRIPTIONS_ENABLED and X_API_KEY in settings."
            )

        # 2. Fetch the clip
        try:
            clip = AssetClip.objects.get(id=clip_id)
        except AssetClip.DoesNotExist:
            raise CommandError(f"Clip not found: {clip_id}")

        # 3. Generate description
        result: dict[str, Any] = self._generate_description(clip, client)

        # 4. Output result as JSON
        self.stdout.write(json.dumps(result, indent=2))

    def _generate_description(
        self, clip: AssetClip, client
    ) -> dict[str, Any]:
        """Generate description for a clip and save to database."""
        try:
            # Call Grok service
            description = client.generate_description(clip)

            if description is None:
                # Clip was skipped (insufficient frames)
                return {
                    "clip_id": str(clip.id),
                    "success": False,
                    "skipped": True,
                    "skip_reason": "Insufficient captioned frames (minimum 3 required)",
                    "error": None,
                }

            # Save to database
            clip.description = description
            clip.description_model = client.model
            clip.description_generated_at = timezone.now()
            clip.description_error = ""
            clip.save(update_fields=[
                "description",
                "description_model",
                "description_generated_at",
                "description_error",
            ])

            return {
                "clip_id": str(clip.id),
                "success": True,
                "description": description,
                "model": client.model,
                "generated_at": clip.description_generated_at.isoformat(),
                "skipped": False,
                "error": None,
            }

        except Exception as e:
            # API call failed after retries
            error_msg = str(e)

            # Save error to database
            clip.description_error = error_msg
            clip.save(update_fields=["description_error"])

            return {
                "clip_id": str(clip.id),
                "success": False,
                "skipped": False,
                "error": error_msg,
            }
