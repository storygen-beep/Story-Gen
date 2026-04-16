"""Management command to export clip descriptions to files."""

from django.core.management.base import BaseCommand, CommandError
from apps.assets.models import AssetVideo, AssetGroup
from apps.assets.services.export_service import ClipDescriptionExportService
import os


class Command(BaseCommand):
    help = "Export clip descriptions from a video or group to CSV or JSON file"

    def add_arguments(self, parser):
        """Define command arguments."""
        parser.add_argument(
            "resource_id",
            type=str,
            help="UUID of the video or group to export",
        )
        parser.add_argument(
            "--group",
            action="store_true",
            help="Treat resource_id as group_id instead of video_id",
        )
        parser.add_argument(
            "--format",
            type=str,
            choices=["json", "csv"],
            default="json",
            help="Export format (default: json)",
        )
        parser.add_argument(
            "--output",
            type=str,
            help="Output file path (prints to stdout if not provided)",
        )
        parser.add_argument(
            "--extended",
            action="store_true",
            help="Include all metadata (timestamps, model info)",
        )
        parser.add_argument(
            "--only-described",
            action="store_true",
            help="Only export clips with descriptions",
        )

    def handle(self, *args, **options) -> None:
        """Execute the command."""
        resource_id: str = options["resource_id"]
        is_group: bool = options["group"]
        format_type: str = options["format"]
        output_path: str | None = options.get("output")
        extended: bool = options["extended"]
        only_described: bool = options["only_described"]

        # 1. Verify resource exists
        if is_group:
            try:
                group = AssetGroup.objects.get(id=resource_id)
                resource_name = f"group '{group.name}'"
            except AssetGroup.DoesNotExist:
                raise CommandError(f"Group not found: {resource_id}")
        else:
            try:
                video = AssetVideo.objects.get(id=resource_id)
                resource_name = f"video {resource_id}"
            except AssetVideo.DoesNotExist:
                raise CommandError(f"Video not found: {resource_id}")

        # 2. Generate export
        try:
            if is_group:
                if format_type == "json":
                    content = ClipDescriptionExportService.export_group_to_json(
                        resource_id, extended, only_described
                    )
                else:  # csv
                    content = ClipDescriptionExportService.export_group_to_csv(
                        resource_id, extended, only_described
                    )
            else:
                if format_type == "json":
                    content = ClipDescriptionExportService.export_to_json(
                        resource_id, extended, only_described
                    )
                else:  # csv
                    content = ClipDescriptionExportService.export_to_csv(
                        resource_id, extended, only_described
                    )
        except Exception as e:
            raise CommandError(f"Export failed: {e}")

        # 3. Output to file or stdout
        if output_path:
            # Write to file
            try:
                # Ensure directory exists
                os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(content)

                self.stdout.write(
                    self.style.SUCCESS(f"✓ Exported {resource_name} to {output_path}")
                )
            except IOError as e:
                raise CommandError(f"Failed to write file: {e}")
        else:
            # Print to stdout
            self.stdout.write(content)
