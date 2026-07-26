"""
Management command to package games with media assets.

Usage:
    python manage.py package_game --project-id <uuid> --output /path/to/output
"""

from django.core.management.base import BaseCommand, CommandError

from apps.game_generation.services.game_service import GameService
from apps.projects.models import Project


class Command(BaseCommand):
    help = "Package game with HTML + media assets for offline play"

    def add_arguments(self, parser):
        parser.add_argument(
            "--project-id",
            type=str,
            required=True,
            help="Project UUID to package",
        )
        parser.add_argument(
            "--output",
            type=str,
            required=True,
            help="Absolute path to output directory",
        )
        parser.add_argument(
            "--system",
            type=str,
            default="twee_comprehensive",
            help="Generation system type (default: twee_comprehensive)",
        )
        parser.add_argument(
            "--gen-version",
            type=str,
            default="v2",
            help="Generator version (default: v2). Pass v1 for frozen safe-mode rollback.",
        )
        parser.add_argument(
            "--force-copy",
            action="store_true",
            help="Force copy all files (skip size comparison)",
        )
        parser.add_argument(
            "--verify-checksums",
            action="store_true",
            help="Use SHA256 checksums instead of size comparison (slower)",
        )
        parser.add_argument(
            "--dev",
            action="store_true",
            help="Enable dev mode with stat adjustment controls in sidebar",
        )
        parser.add_argument(
            "--build",
            type=str,
            choices=["free", "paid"],
            default="free",
            help=(
                "Cheat-page build variant (parity with package_from_toml). 'free' (default) "
                "emits padlocked labels with no working effects; 'paid' emits live rows."
            ),
        )

    def handle(self, *args, **options):
        project_id = options["project_id"]
        output_dir = options["output"]
        system_type = options["system"]
        version = options["gen_version"]
        force_copy = options["force_copy"]
        verify_checksums = options["verify_checksums"]
        dev_mode = options["dev"]
        build_variant = options.get("build", "free") or "free"

        # Load project
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise CommandError(f"Project with ID {project_id} not found")

        self.stdout.write(f"📦 Packaging game: {project.name}")
        self.stdout.write(f"   System: {system_type}")
        self.stdout.write(f"   Output: {output_dir}")
        if dev_mode:
            self.stdout.write(self.style.WARNING("   Dev Mode: ENABLED (stat adjustment controls)"))

        # Generate package
        service = GameService()
        try:
            result = service.package_game(
                project=project,
                system_type=system_type,
                output_dir=output_dir,
                version=version,
                force_copy=force_copy,
                verify_checksums=verify_checksums,
                options=(
                    {"build": build_variant, **({"dev_mode": True} if dev_mode else {})}
                ),
            )
        except Exception as e:
            raise CommandError(f"Packaging failed: {e}")

        # Display results
        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS("✅ Package generated successfully!")
        )
        self.stdout.write(f"📄 HTML: {result['html_path']}")
        self.stdout.write(f"📁 Media: {result['media_dir']}")

        # Asset statistics
        stats = result["assets"]
        self.stdout.write("")
        self.stdout.write("📊 Asset Statistics:")
        self.stdout.write(f"   Total clips: {stats['total']}")
        self.stdout.write(f"   Copied: {stats['copied']}")
        self.stdout.write(f"   Skipped: {stats['skipped']}")
        self.stdout.write(f"   Failed: {stats['failed']}")
        self.stdout.write(f"   Bytes copied: {stats['bytes_copied']:,}")
        self.stdout.write(f"   Bytes saved: {stats['bytes_saved']:,}")

        # Performance tip
        if stats["skipped"] > 0:
            self.stdout.write("")
            self.stdout.write(
                self.style.SUCCESS(
                    f"💰 Saved {stats['bytes_saved']:,} bytes by skipping existing files!"
                )
            )

        # Errors
        if result["errors"]:
            self.stdout.write("")
            self.stdout.write(
                self.style.WARNING(
                    f"⚠️  {len(result['errors'])} error(s) encountered:"
                )
            )
            for error in result["errors"][:5]:  # Show first 5 errors
                self.stdout.write(f"   - {error}")
            if len(result["errors"]) > 5:
                self.stdout.write(
                    f"   ... and {len(result['errors']) - 5} more"
                )

        # Success message
        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"🎉 Package ready! Open {result['html_path']} in a browser."
            )
        )
