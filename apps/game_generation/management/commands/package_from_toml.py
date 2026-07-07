"""
Management command to package games directly from TOML files.

This command combines TOML loading and game packaging into a single operation,
eliminating the need for the two-step process of:
1. create_project_from_template (TOML → Database)
2. package_game (Database → Package)

Usage:
    python manage.py package_from_toml \
        --file path/to/game.toml \
        --owner-id <uuid> \
        --output /path/to/output

By default, the database project is deleted after successful packaging.
Use --keep-project to retain the database records for debugging.
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.authentication.models import User
from apps.game_generation.services.game_service import GameService
from apps.projects.models import Project
from apps.projects.services.template_import import (
    create_project_from_template,
    normalize,
    parse_toml,
    validate,
)


class Command(BaseCommand):
    help = "Load TOML file and package game in one step"

    def add_arguments(self, parser):
        # Required arguments
        parser.add_argument(
            "--file",
            type=str,
            required=True,
            help="Path to TOML game definition file",
        )
        parser.add_argument(
            "--owner-id",
            type=str,
            required=False,
            default=None,
            help="Owner UUID for the project (only needed with --use-db)",
        )
        parser.add_argument(
            "--output",
            type=str,
            required=True,
            help="Absolute path to output directory",
        )

        # Optional packaging settings
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
            "--local-media",
            action="store_true",
            help="Use local media files instead of R2 URLs for offline playback",
        )
        parser.add_argument(
            "--use-db",
            action="store_true",
            help=(
                "Legacy: build through the database (writes/reads/deletes DB rows, "
                "requires --owner-id). The DEFAULT is the no-DB in-memory graph "
                "build — zero database interaction, no owner, nothing persisted."
            ),
        )

        # Video folder for file-based videos
        parser.add_argument(
            "--video-folder",
            type=str,
            default=None,
            help="Path to folder containing video files referenced in TOML blocks",
        )
        parser.add_argument(
            "--debug",
            action="store_true",
            help="Show placeholder blocks for missing videos with filename and description",
        )
        parser.add_argument(
            "--video-path",
            type=str,
            default=None,
            help="Base path/URL for media in generated HTML. "
                 "Auto-derived from --video-folder basename if not set. "
                 "Use to override when HTML is served from a different location.",
        )

        # Optional project settings
        parser.add_argument(
            "--name",
            type=str,
            help="Override project title from TOML",
        )
        parser.add_argument(
            "--keep-project",
            action="store_true",
            help="Keep database records after packaging (default: False)",
        )

        # Optional modes
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Validate only, don't create or package",
        )
        parser.add_argument(
            "--dev",
            action="store_true",
            help="Enable dev mode with stat adjustment controls in sidebar",
        )
        parser.add_argument(
            "--chart",
            action="store_true",
            help="Generate Mermaid markdown chart of story structure (story_chart.md)",
        )

    def handle(self, *args, **options):
        from pathlib import Path

        # Extract arguments
        file_path = options["file"]
        owner_id = options["owner_id"]
        output_dir = options["output"]
        system_type = options["system"]
        version = options["gen_version"]
        force_copy = options["force_copy"]
        verify_checksums = options["verify_checksums"]
        local_media = options["local_media"]
        video_folder = options.get("video_folder")
        video_path = options.get("video_path")
        debug = options.get("debug", False)
        name_override = options.get("name")
        keep_project = options["keep_project"]
        dry_run = options["dry_run"]
        dev_mode = options["dev"]
        generate_chart = options.get("chart", False)
        # No-DB (in-memory graph) is the DEFAULT; --use-db opts into the legacy
        # database build path (which requires an owner and persists rows).
        no_db = not options.get("use_db", False)
        if not no_db and not owner_id:
            raise CommandError("--use-db requires --owner-id (the legacy DB build path).")

        # Validate video folder if provided (used for validation/copying)
        if video_folder:
            video_folder_path = Path(video_folder)
            if not video_folder_path.exists():
                raise CommandError(f"Video folder does not exist: {video_folder}")
            if not video_folder_path.is_dir():
                raise CommandError(f"Video folder is not a directory: {video_folder}")
            self.stdout.write(f"📹 Video folder: {video_folder}")

            # Auto-derive video_path from video_folder basename if not explicitly set
            if not video_path:
                video_path = "./" + video_folder_path.name
                self.stdout.write(f"📹 Video path (auto): {video_path}")

        # If only video_path specified (no video_folder), use it for scanning too
        if video_path and not video_folder:
            self.stdout.write(f"📹 Video path (direct): {video_path}")
            video_folder = video_path

        # Display explicit override if both are set differently
        if video_path and video_folder and video_path != "./" + Path(video_folder).name:
            self.stdout.write(f"📹 Video path (override): {video_path}")

        if dev_mode:
            self.stdout.write(self.style.WARNING("🔧 Dev Mode: ENABLED (stat adjustment controls)"))
        if no_db:
            self.stdout.write("🚫 No-DB build (in-memory graph, nothing persisted)")
        else:
            self.stdout.write(self.style.WARNING("🗄  Legacy DB build (--use-db): writing/reading DB rows"))

        # Phase 1: Validate owner (DB path only — no owner needed for the no-DB default)
        owner = None if no_db else self._get_owner(owner_id)

        # Phase 2: Load and validate TOML
        template = self._load_toml(file_path)

        # Phase 3: Optional dry-run exit
        if dry_run:
            self._report_dry_run(template)
            # Generate chart even in dry-run mode if requested
            if generate_chart:
                chart_path = self._generate_chart(template, output_dir)
                self.stdout.write(f"\n📊 Chart generated: {chart_path}")
            return

        # Phase 4: Build the game — in-memory graph (no-DB) or persisted project (DB).
        if no_db:
            from apps.projects.services.game_graph import build_game_graph
            graph = build_game_graph(template, name_override)
            project = graph.project
        else:
            graph = None
            project = self._create_project(template, owner, name_override)

        # Phase 4.5: Validate flag chains
        self._validate_flag_chains(project, system_type, version, graph=graph)

        # Phase 5: Package game
        # Resolve output_dir to absolute path and get game folder name
        output_path = Path(output_dir).resolve()
        # If output is inside a "game" subfolder, use parent folder name for approvals
        if output_path.name == "game":
            game_folder_name = output_path.parent.name
        else:
            game_folder_name = output_path.name

        try:
            package_result = self._package_game(
                project, str(output_path), system_type, version, force_copy, verify_checksums, local_media,
                video_folder=video_folder, video_path=video_path, debug=debug, dev_mode=dev_mode,
                game_folder=game_folder_name,  # Pass resolved game folder name for approvals
                graph=graph,
            )
        except Exception as e:
            # Keep project for debugging on packaging failure (DB path only —
            # nothing is persisted in no-DB mode).
            if not no_db:
                self.stdout.write("")
                self.stdout.write(
                    self.style.WARNING(
                        f"⚠️  Packaging failed but project kept for debugging: {project.id}"
                    )
                )
            raise CommandError(f"Packaging failed: {e}")

        # Phase 6: Optional cleanup (nothing persisted in no-DB mode)
        if not no_db and not keep_project:
            self._cleanup_project(project)

        # Phase 6.5: Generate chart if requested
        if generate_chart:
            chart_path = self._generate_chart(template, output_dir)
            self.stdout.write(f"\n📊 Chart generated: {chart_path}")

        # Phase 7: Display results
        self._display_results(package_result, project, keep_project)

    def _get_owner(self, owner_id: str) -> User:
        """Validate and retrieve owner user."""
        try:
            return User.objects.get(id=owner_id)
        except User.DoesNotExist:
            raise CommandError(f"Owner with ID {owner_id} not found")
        except ValueError:
            raise CommandError(f"Invalid UUID format: {owner_id}")

    def _load_toml(self, file_path: str) -> dict:
        """Load and validate TOML file."""
        self.stdout.write(f"📦 Loading TOML: {file_path}")

        # Parse TOML
        try:
            raw_data = parse_toml(file_path)
            self.stdout.write("   ✓ TOML parsed successfully")
        except Exception as e:
            raise CommandError(f"Failed to parse TOML: {e}")

        # Normalize to dataclass structure
        try:
            template = normalize(raw_data)
        except Exception as e:
            raise CommandError(f"Failed to normalize TOML data: {e}")

        # Validate (returns list of error strings)
        # Also capture soft warnings (canvas uniqueness, NPC schedule deprecation)
        import warnings as _warnings
        try:
            with _warnings.catch_warnings(record=True) as caught_warnings:
                _warnings.simplefilter("always")
                errors = validate(template)
            if errors:
                self.stdout.write("")
                self.stdout.write(self.style.ERROR("❌ Validation failed:"))
                for error in errors:
                    self.stdout.write(f"   - {error}")
                raise CommandError("TOML validation failed")
            self.stdout.write("   ✓ Validation passed")
            # Show soft warnings (non-blocking)
            for w in caught_warnings:
                self.stdout.write(
                    self.style.WARNING(f"   ⚠️  {w.message}")
                )
        except CommandError:
            raise
        except Exception as e:
            raise CommandError(f"Validation error: {e}")

        return template

    def _create_project(self, template, owner: User, name_override: str = None):
        """Create project in database with atomic transaction."""
        self.stdout.write("")
        self.stdout.write("📂 Creating project in database...")

        try:
            with transaction.atomic():
                result = create_project_from_template(
                    template=template, owner_id=str(owner.id), name_override=name_override
                )
                project = Project.objects.get(id=result["project_id"])

                # Display creation statistics
                self.stdout.write(f"   ✓ Project: {project.name}")
                stats = result.get("stats", {})
                if "locations" in stats:
                    self.stdout.write(f"   ✓ Locations: {stats['locations']} created")
                if "npcs" in stats:
                    self.stdout.write(f"   ✓ NPCs: {stats['npcs']} created")
                if "canvases" in stats:
                    self.stdout.write(f"   ✓ Canvases: {stats['canvases']} created")
                if "nodes" in stats:
                    self.stdout.write(f"   ✓ Nodes: {stats['nodes']} created")

                return project

        except Exception as e:
            raise CommandError(f"Failed to create project: {e}")

    def _validate_flag_chains(self, project: Project, system_type: str, version: str, graph=None):
        """Validate flag chains before packaging."""
        self.stdout.write("")
        self.stdout.write("🔗 Validating flag chains...")

        # Only validate for twee_comprehensive system
        if system_type != "twee_comprehensive":
            self.stdout.write("   ⏭ Skipped (not twee_comprehensive)")
            return

        # Import and instantiate generator (version-aware dispatch).
        # v2 is the default; v1 is frozen 2026-05-14 and exists only as
        # a safe-mode rollback path during the v2 transition.
        from apps.world.models import Location

        if version == "v2":
            from apps.game_generation.twee_comprehensive.generators.v2 import (
                TweeComprehensiveGeneratorV2,
            )
            generator = TweeComprehensiveGeneratorV2()
        elif version == "v1":
            from apps.game_generation.twee_comprehensive.generators.v1 import (
                TweeComprehensiveGeneratorV1,
            )
            generator = TweeComprehensiveGeneratorV1()
        else:
            raise CommandError(
                f"Unknown gen-version {version!r}. Supported: v1, v2."
            )
        generator.project = project
        if graph is not None:
            generator.graph = graph
            generator.locations = graph.locations
        else:
            generator.locations = list(Location.objects.filter(project=project))
        errors = generator.validate_flag_chains()

        if errors:
            self.stdout.write("")
            self.stdout.write(self.style.ERROR("❌ Flag Chain Validation Failed:"))
            self.stdout.write("")
            for err in errors:
                self.stdout.write(f"   ✗ {err['flag_key']}")
                self.stdout.write(f"     Required by: {err['canvas_name']}")
                self.stdout.write(f"     Issue: {err['issue']}")
                self.stdout.write("")
            raise CommandError(
                f"Flag chain validation failed with {len(errors)} error(s). "
                "Fix the TOML to ensure all required flags are set by a canvas with location/schedule."
            )

        self.stdout.write("   ✓ All flag chains valid")

    def _package_game(
        self,
        project: Project,
        output_dir: str,
        system_type: str,
        version: str,
        force_copy: bool,
        verify_checksums: bool,
        local_media: bool,
        video_folder: str = None,
        video_path: str = None,
        debug: bool = False,
        dev_mode: bool = False,
        game_folder: str = None,
        graph=None,
    ) -> dict:
        """Package game using GameService."""
        self.stdout.write("")
        self.stdout.write("🎮 Generating game package...")
        self.stdout.write(f"   System: {system_type}")
        self.stdout.write(f"   Version: {version}")
        if local_media:
            self.stdout.write("   Media: Local (offline playback)")
        if video_path:
            self.stdout.write(f"   Video path (direct, no copy): {video_path}")
        elif video_folder:
            self.stdout.write(f"   Video folder: {video_folder}")
        if debug:
            self.stdout.write("   Debug mode: Enabled (missing videos show placeholders)")
        if dev_mode:
            self.stdout.write(self.style.WARNING("   Dev mode: Enabled (+/- stat controls)"))
            if game_folder:
                self.stdout.write(f"   Game folder (for approvals): {game_folder}")

        # Build options dict
        options = {}
        if dev_mode:
            options["dev_mode"] = True
        if game_folder:
            options["game_folder"] = game_folder

        service = GameService()
        return service.package_game(
            project=project,
            system_type=system_type,
            output_dir=output_dir,
            version=version,
            force_copy=force_copy,
            verify_checksums=verify_checksums,
            local_media=local_media,
            video_folder=video_folder,
            video_path=video_path,
            debug=debug,
            options=options if options else None,
            graph=graph,
        )

    def _cleanup_project(self, project: Project):
        """Delete project and related records."""
        try:
            project_id = project.id
            project.delete()  # Cascade deletes related objects
            self.stdout.write("")
            self.stdout.write("🧹 Database cleanup:")
            self.stdout.write("   ✓ Project removed from database")
        except Exception as e:
            self.stdout.write("")
            self.stdout.write(
                self.style.WARNING(f"⚠️  Could not delete project {project_id}: {e}")
            )

    def _display_results(self, package_result: dict, project: Project, kept: bool):
        """Display packaging results and statistics."""
        self.stdout.write("")

        # Asset statistics (clips)
        stats = package_result["assets"]
        self.stdout.write("📊 Clip Statistics:")
        self.stdout.write(f"   Total clips: {stats['total']}")
        self.stdout.write(f"   Copied: {stats['copied']}")
        self.stdout.write(f"   Skipped: {stats['skipped']}")
        self.stdout.write(f"   Failed: {stats['failed']}")
        self.stdout.write(f"   Bytes copied: {stats['bytes_copied']:,}")
        self.stdout.write(f"   Bytes saved: {stats['bytes_saved']:,}")

        # External video statistics
        video_stats = package_result.get("external_videos")
        if video_stats and video_stats.get("total", 0) > 0:
            self.stdout.write("")
            self.stdout.write("📹 Video Statistics:")
            self.stdout.write(f"   Total videos: {video_stats['total']}")
            self.stdout.write(f"   Copied: {video_stats['copied']}")
            self.stdout.write(f"   Skipped: {video_stats['skipped']}")
            self.stdout.write(f"   Failed: {video_stats['failed']}")
            self.stdout.write(f"   Bytes copied: {video_stats.get('bytes_copied', 0):,}")

        # Loud warning: external assets referenced but not copied (no --video-folder given).
        # The build otherwise looks green while every portrait / NPC / location image 404s.
        if video_stats and video_stats.get("skipped_no_video_folder"):
            n = video_stats["skipped_no_video_folder"]
            self.stdout.write("")
            self.stdout.write(
                self.style.ERROR(
                    f"⚠️  {n} external media file(s) referenced but NOT copied — no --video-folder given."
                )
            )
            self.stdout.write(
                self.style.ERROR(
                    "   Sidebar portraits / NPC / location images will be BROKEN in this build."
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    "   Re-run with:  --video-folder <path to the game's media dir>"
                )
            )

        # Performance tip
        total_saved = stats.get("bytes_saved", 0)
        if video_stats:
            total_saved += video_stats.get("bytes_saved", 0)
        if total_saved > 0:
            self.stdout.write("")
            self.stdout.write(
                self.style.SUCCESS(
                    f"💰 Saved {total_saved:,} bytes by skipping existing files!"
                )
            )

        # Package location
        self.stdout.write("")
        self.stdout.write("📄 Package created:")
        self.stdout.write(f"   HTML: {package_result['html_path']}")
        self.stdout.write(f"   Media: {package_result['media_dir']}")

        # Project retention info
        if kept:
            self.stdout.write("")
            self.stdout.write("📝 Database project retained:")
            self.stdout.write(f"   Project ID: {project.id}")
            self.stdout.write(f"   Name: {project.name}")
            self.stdout.write("")
            self.stdout.write("💡 Use this ID for future operations:")
            self.stdout.write(
                f"   python manage.py package_game --project-id {project.id} --output /path"
            )

        # Errors
        if package_result["errors"]:
            self.stdout.write("")
            self.stdout.write(
                self.style.WARNING(
                    f"⚠️  {len(package_result['errors'])} error(s) encountered:"
                )
            )
            for error in package_result["errors"][:5]:  # Show first 5 errors
                self.stdout.write(f"   - {error}")
            if len(package_result["errors"]) > 5:
                self.stdout.write(f"   ... and {len(package_result['errors']) - 5} more")

        # Success message
        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"🎉 Package ready! Open {package_result['html_path']} in a browser."
            )
        )

    def _report_dry_run(self, template) -> None:
        """Report dry-run validation results."""
        self.stdout.write("")
        self.stdout.write("📊 Project Statistics:")

        # Count elements in template
        location_count = len(template.locations) if hasattr(template, "locations") else 0
        npc_count = len(template.npcs) if hasattr(template, "npcs") else 0
        character_count = (
            len(template.characters) if hasattr(template, "characters") else 0
        )
        canvas_count = len(template.canvases) if hasattr(template, "canvases") else 0

        # Count total nodes across all canvases
        node_count = 0
        connection_count = 0
        if hasattr(template, "canvases"):
            for canvas in template.canvases:
                if hasattr(canvas, "nodes"):
                    node_count += len(canvas.nodes)
                if hasattr(canvas, "connections"):
                    connection_count += len(canvas.connections)

        self.stdout.write(f"   Locations: {location_count}")
        self.stdout.write(f"   NPCs: {npc_count}")
        self.stdout.write(f"   Characters: {character_count}")
        self.stdout.write(f"   Canvases: {canvas_count}")
        self.stdout.write(f"   Nodes: {node_count}")
        self.stdout.write(f"   Connections: {connection_count}")

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS("✓ TOML file is valid and ready for packaging")
        )

    # -------- Chart Generation Methods --------

    # Known gate flags that unlock content tiers
    GATE_FLAGS = {
        "kiss_unlocked",
        "groping_unlocked",
        "manual_unlocked",
        "oral_unlocked",
        "sex_unlocked",
        "outdoor_unlocked",
        "power_play_unlocked",
        "pegging_unlocked",
    }

    # Map gate flags to tier descriptions
    GATE_TO_TIER = {
        "kiss_unlocked": "T3 teasing",
        "groping_unlocked": "T4 groping",
        "manual_unlocked": "T5 manual",
        "oral_unlocked": "T6 oral",
        "sex_unlocked": "T7/T8 full",
        "outdoor_unlocked": "outdoor content",
        "power_play_unlocked": "power play",
        "pegging_unlocked": "pegging content",
    }

    def _generate_chart(self, template, output_dir: str) -> str:
        """Generate a Mermaid markdown file visualizing the game structure."""
        from collections import defaultdict
        from pathlib import Path

        from apps.projects.services.template_import import (
            _extract_flags_set_by_canvas,
        )

        output_path = Path(output_dir) / "story_chart.md"

        # Categorize canvases
        story_canvases, activities_by_location = self._categorize_canvases(
            template.canvases
        )

        # Build location name lookup
        loc_names = {loc.id: loc.name for loc in template.locations}

        # Build markdown content
        lines = [
            f"# {template.project.title} - Story Structure",
            "",
            f"> Generated from TOML schema v{template.schema_version}",
            "",
        ]

        # Section 1: Story Spine
        lines.append(self._build_story_spine_diagram(story_canvases, loc_names))
        lines.append("")

        # Section 2: Activity Tiers per Location
        for loc_id in sorted(activities_by_location.keys()):
            activities = activities_by_location[loc_id]
            loc_name = loc_names.get(loc_id, loc_id)
            lines.append(
                self._build_activity_tier_diagram(loc_id, loc_name, activities)
            )
            lines.append("")

        # Section 3: Gate Unlock Summary
        lines.append(self._build_gate_unlock_table(story_canvases))

        # Write file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("\n".join(lines))

        return str(output_path)

    def _categorize_canvases(self, canvases):
        """Categorize canvases into story (non-repeatable) and activity (repeatable)."""
        from collections import defaultdict

        story_canvases = []
        activities_by_location = defaultdict(list)

        for canvas in canvases:
            trigger = canvas.trigger
            if not trigger:
                continue  # Skip canvases without triggers

            if trigger.is_repeatable:
                # Activity canvas - group by location
                location = trigger.location or "unknown"
                activities_by_location[location].append(canvas)
            else:
                # Story canvas - one-time events
                story_canvases.append(canvas)

        # Sort story canvases by priority (higher first = earlier in story)
        story_canvases.sort(
            key=lambda c: c.trigger.priority if c.trigger else 0, reverse=True
        )

        # Sort activities within each location by priority (tier)
        for location in activities_by_location:
            activities_by_location[location].sort(
                key=lambda c: c.trigger.priority if c.trigger else 0, reverse=True
            )

        return story_canvases, dict(activities_by_location)

    def _build_story_spine_diagram(self, story_canvases, loc_names) -> str:
        """Build Mermaid flowchart for story progression."""
        from apps.projects.services.template_import import _extract_flags_set_by_canvas

        lines = ["## Story Progression", "", "```mermaid", "flowchart TD"]

        # Track previous canvas for connections
        prev_canvas_id = None

        for canvas in story_canvases:
            canvas_id = canvas.id.replace("-", "_")  # Mermaid-safe ID
            loc_name = loc_names.get(canvas.trigger.location, "") if canvas.trigger else ""

            # Get gate flags set by this canvas
            gate_flags = _extract_flags_set_by_canvas(canvas) & self.GATE_FLAGS
            gate_str = "<br/>🔓 " + ", ".join(sorted(gate_flags)) if gate_flags else ""

            # Node label
            label_parts = [canvas.name]
            if loc_name:
                label_parts.append(f"📍 {loc_name}")
            if gate_str:
                label_parts.append(gate_str.replace("<br/>", ""))

            label = "<br/>".join(label_parts)
            lines.append(f'    {canvas_id}["{label}"]')

            # Connection from previous canvas with conditions
            if prev_canvas_id and canvas.trigger and canvas.trigger.conditions:
                cond_str = self._format_conditions(canvas.trigger.conditions)
                if cond_str:
                    # Escape quotes for Mermaid
                    cond_str = cond_str.replace('"', "'")
                    lines.append(f'    {prev_canvas_id} --> |"{cond_str}"| {canvas_id}')
                else:
                    lines.append(f"    {prev_canvas_id} --> {canvas_id}")
            elif prev_canvas_id:
                lines.append(f"    {prev_canvas_id} --> {canvas_id}")

            prev_canvas_id = canvas_id

        lines.append("```")
        return "\n".join(lines)

    def _build_activity_tier_diagram(self, loc_id: str, loc_name: str, activities) -> str:
        """Build Mermaid diagram for a location's activity tiers."""
        from collections import defaultdict

        lines = [f"## Activities: {loc_name}", "", "```mermaid", "flowchart LR"]

        # Group activities by name (same activity, different tiers)
        activities_by_name = defaultdict(list)
        for activity in activities:
            activities_by_name[activity.name].append(activity)

        # Sort by highest tier within each activity group
        for name, group in activities_by_name.items():
            group.sort(key=lambda c: c.trigger.priority if c.trigger else 0)

        # Build subgraph for each activity type
        subgraph_idx = 0
        for activity_name, group in sorted(activities_by_name.items()):
            safe_name = activity_name.replace(" ", "_").replace("-", "_")
            lines.append(f'    subgraph {safe_name}["{activity_name}"]')
            lines.append("        direction TB")

            tier_nodes = []
            for activity in group:
                tier = activity.trigger.priority if activity.trigger else 0
                node_id = f"{safe_name}_T{tier}"

                # Get conditions for this tier
                cond_str = ""
                if activity.trigger and activity.trigger.conditions:
                    cond_str = self._format_conditions(activity.trigger.conditions)

                if cond_str:
                    label = f"T{tier}<br/>{cond_str}"
                else:
                    label = f"T{tier} (fallback)"

                lines.append(f'        {node_id}["{label}"]')
                tier_nodes.append(node_id)

            lines.append("    end")

            # Connect tiers with dotted lines (progression)
            if len(tier_nodes) > 1:
                connections = " -.-> ".join(tier_nodes)
                lines.append(f"    {connections}")

            subgraph_idx += 1

        lines.append("```")
        return "\n".join(lines)

    def _build_gate_unlock_table(self, story_canvases) -> str:
        """Build markdown table showing gate flag unlocks."""
        from apps.projects.services.template_import import _extract_flags_set_by_canvas

        lines = [
            "## Gate Unlocks",
            "",
            "| Story Canvas | Gate Flag | Unlocks |",
            "|--------------|-----------|---------|",
        ]

        for canvas in story_canvases:
            gate_flags = _extract_flags_set_by_canvas(canvas) & self.GATE_FLAGS
            for flag in sorted(gate_flags):
                unlocks = self.GATE_TO_TIER.get(flag, "content")
                lines.append(f"| {canvas.name} | `{flag}` | {unlocks} |")

        if len(lines) == 4:  # Only header, no data
            lines.append("| (none) | - | - |")

        return "\n".join(lines)

    def _format_conditions(self, conditions: dict) -> str:
        """Convert conditions dict to human-readable string."""
        if not conditions:
            return ""

        items = conditions.get("items", [])
        parts = []

        for item in items:
            if not isinstance(item, dict):
                continue

            item_type = item.get("type", "")

            if item_type == "flag":
                flag_key = item.get("flag_key", "")
                operator = item.get("operator", "is_true")
                if operator == "is_true":
                    parts.append(flag_key)
                elif operator == "is_false":
                    parts.append(f"!{flag_key}")

            elif item_type == "trait":
                trait_key = item.get("trait_key", "")
                operator = item.get("operator", "gte")
                value = item.get("value", 0)

                op_map = {"gte": ">=", "lte": "<=", "eq": "=", "gt": ">", "lt": "<"}
                op_str = op_map.get(operator, operator)
                parts.append(f"{trait_key}{op_str}{value}")

            elif item_type == "days_since_flag":
                flag_key = item.get("flag_key", "")
                value = item.get("value", 0)
                parts.append(f"{value}d since {flag_key}")

        logic = conditions.get("logic", "AND")
        separator = " + " if logic == "AND" else " | "

        return separator.join(parts)
