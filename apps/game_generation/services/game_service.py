"""
Unified Game Generation Service.

This is the single API interface for all game generation systems.
It delegates to specific isolated systems based on the requested type.
"""

import logging
import os
import shutil
import subprocess
import tempfile
from importlib import import_module
from typing import Any, Optional

from PIL import Image

from apps.projects.models import Project

logger = logging.getLogger(__name__)

# The compiler is REQUIRED. There is no fallback: a build either comes out of Tweego
# as a real SugarCube game or it does not come out at all.
#
# Why this is not negotiable — 2026-07-28, two cloud-session builds: Tweego was absent,
# compilation returned None, and the packager silently wrote a "Basic Preview Mode" page
# that renders the raw Twee source as text. 324,722 bytes of source dump, announced as
# "🎉 Package ready!", merged and shipped to the portal. Verification missed it because
# every media reference still resolved — they were in the source being printed.
#
# These are what every game on the portal was built with. A mismatch is logged, not
# fatal (an upgrade must stay possible), but it must never pass unnoticed: Tweego bundles
# its own story format, so a different Tweego silently changes the SugarCube every future
# game ships against.
EXPECTED_TWEEGO_VERSION = "2.1.1"
EXPECTED_SUGARCUBE_VERSION = "2.30.0"

# Searched in order. `~/bin` covers the local install; /usr/bin and /usr/local/bin cover
# a container that installed it by hand or by apt.
TWEEGO_SEARCH_PATHS = (
    "tweego",  # anything already on PATH wins
    "/usr/local/bin/tweego",
    "/usr/bin/tweego",
    "/opt/homebrew/bin/tweego",
    os.path.expanduser("~/bin/tweego"),
)


class GameService:
    """
    Unified service interface for all game generation systems.

    This is a thin orchestration layer that delegates to completely
    isolated generation systems. No business logic here, only routing.
    """

    def __init__(self):
        # Cache for service instances to preserve state between calls
        self._service_cache = {}

    # Registry of available game generation systems
    REGISTERED_SYSTEMS = {
        "twee_navigation": {
            "module": "apps.game_generation.twee_navigation.services",
            "class": "TweeNavigationService",
            "description": "Simple navigation-based exploration games",
        },
        "twee_comprehensive": {
            "module": "apps.game_generation.twee_comprehensive.services",
            "class": "TweeComprehensiveService",
            "description": "Sophisticated interactive experiences with multiple layers",
        },
        # Future systems can be added here:
        # 'unity_simple': {...},
        # 'godot_rpg': {...},
    }

    def generate_game(
        self,
        project: Project,
        system_type: str,
        version: str = "v2",
        options: Optional[dict] = None,
        graph: Optional[object] = None,
    ) -> str:
        """
        Generate game using specified system and version.

        Args:
            project: Django Project instance
            system_type: Type of game generation system to use
            version: Version of the generator (default: v1)
            options: Optional generation options

        Returns:
            str: Generated game content (usually Twee format)

        Raises:
            ValueError: If system type not found or generation fails
        """
        # Validate system type
        if system_type not in self.REGISTERED_SYSTEMS:
            available = ", ".join(self.REGISTERED_SYSTEMS.keys())
            raise ValueError(
                f"Unknown system type: {system_type}. Available: {available}"
            )

        # Get system service
        service = self._get_system_service(system_type)

        # Delegate generation to specific system. Only the twee_comprehensive
        # system supports the no-DB graph; pass it through only when present so
        # other systems' generate() signatures stay untouched.
        if graph is not None:
            return service.generate(project, version, options, graph=graph)
        return service.generate(project, version, options)

    def validate_project(self, project: Project, system_type: str) -> dict[str, Any]:
        """
        Validate project for specific generation system.

        Args:
            project: Project to validate
            system_type: System to validate against

        Returns:
            Dict with validation results

        Raises:
            ValueError: If system type not found
        """
        # Validate system type
        if system_type not in self.REGISTERED_SYSTEMS:
            raise ValueError(f"Unknown system type: {system_type}")

        # Get system service
        service = self._get_system_service(system_type)

        # Delegate validation to specific system
        return service.validate_project(project)

    def get_available_systems(self) -> list[dict[str, Any]]:
        """
        Get list of available game generation systems.

        Returns:
            List of system information dictionaries
        """
        systems = []

        for system_type, config in self.REGISTERED_SYSTEMS.items():
            try:
                service = self._get_system_service(system_type)
                capabilities = (
                    service.get_capabilities()
                    if hasattr(service, "get_capabilities")
                    else {}
                )

                systems.append(
                    {
                        "system_type": system_type,
                        "description": config["description"],
                        "capabilities": capabilities,
                    }
                )
            except Exception as e:
                # If system fails to load, still include it but mark as unavailable
                systems.append(
                    {
                        "system_type": system_type,
                        "description": config["description"],
                        "available": False,
                        "error": str(e),
                    }
                )

        return systems

    def compile_twee_to_html(
        self, twee_content: str, project_name: str = "Game"
    ) -> str:
        """
        Compile Twee content to a real SugarCube game with Tweego.

        Args:
            twee_content: Raw Twee content
            project_name: Name for the compiled game

        Returns:
            str: Complete HTML game content

        Raises:
            RuntimeError: Tweego is missing, fails, or produces something that is not a
                SugarCube build. There is deliberately no fallback — see the module
                header. A build that cannot be compiled must fail loudly rather than
                quietly ship a page of source text that looks like success.
        """
        return self._compile_with_tweego(twee_content, project_name)

    def _get_system_service(self, system_type: str):
        """
        Dynamically import and instantiate system service.
        Uses caching to preserve service state between calls.

        Args:
            system_type: Type of system to get

        Returns:
            Instantiated service object (cached)
        """
        # Return cached instance if available
        if system_type in self._service_cache:
            return self._service_cache[system_type]

        config = self.REGISTERED_SYSTEMS[system_type]

        # Dynamic import of system module
        module = import_module(config["module"])

        # Get service class
        service_class = getattr(module, config["class"])

        # Instantiate, cache, and return service
        service = service_class()
        self._service_cache[system_type] = service
        return service

    def _find_tweego(self) -> tuple[str, str]:
        """
        Locate the Tweego binary and read its version banner.

        Returns:
            tuple[str, str]: (path invoked, version banner as reported by `--version`)

        Raises:
            RuntimeError: no usable Tweego on this machine. The message names every
                path tried and how to fix it, because this is the error a container
                run hits first and it must be self-explanatory there.
        """
        for tweego_path in TWEEGO_SEARCH_PATHS:
            try:
                result = subprocess.run(
                    [tweego_path, "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
            except (subprocess.TimeoutExpired, FileNotFoundError, PermissionError):
                continue
            # Tweego prints its banner and exits 1 on a bare --version; treat both as found.
            if result.returncode in (0, 1):
                banner = (result.stdout or result.stderr or "").strip().splitlines()
                return tweego_path, (banner[0] if banner else "unknown")

        raise RuntimeError(
            "Tweego not found — cannot compile. Tried: "
            + ", ".join(TWEEGO_SEARCH_PATHS)
            + f". Install Tweego {EXPECTED_TWEEGO_VERSION} (https://www.motoslave.net/tweego/) "
            "and re-run. There is no preview fallback: a build without Tweego would be a "
            "page of raw Twee source, which has shipped to the portal before and must not again."
        )

    def _compile_with_tweego(self, twee_content: str, project_name: str) -> str:
        """
        Compile Twee to a SugarCube game. Raises rather than degrading.

        Args:
            twee_content: Raw Twee content
            project_name: Name for the compiled game

        Returns:
            str: Compiled SugarCube HTML

        Raises:
            RuntimeError: Tweego missing, compilation failed, or the output is not a
                SugarCube build.
        """
        tweego_cmd, version_banner = self._find_tweego()

        if EXPECTED_TWEEGO_VERSION not in version_banner:
            # Not fatal — upgrading must stay possible — but never silent, because the
            # story format is bundled with the compiler, not with our source.
            logger.warning(
                "Tweego version mismatch: expected %s, got %r (from %s). Every existing "
                "game on the portal was built with %s / SugarCube %s; verify the new build "
                "before shipping it.",
                EXPECTED_TWEEGO_VERSION,
                version_banner,
                tweego_cmd,
                EXPECTED_TWEEGO_VERSION,
                EXPECTED_SUGARCUBE_VERSION,
            )

        try:
            # Create temporary files
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".twee", delete=False
            ) as twee_file:
                twee_file.write(twee_content)
                twee_path = twee_file.name

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".html", delete=False
            ) as html_file:
                html_path = html_file.name

            # Compile with Tweego
            cmd = [tweego_cmd, "-f", "sugarcube-2", twee_path, "-o", html_path]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode == 0 and os.path.exists(html_path):
                with open(html_path, encoding="utf-8") as f:
                    html_content = f.read()

                # Clean up temporary files
                os.unlink(twee_path)
                os.unlink(html_path)

                # Exit 0 is necessary and not sufficient. Assert the artifact is
                # actually a playable SugarCube build before handing it back — this is
                # the check that would have caught the 2026-07-28 source-dump builds,
                # and it holds for any future way the compile could quietly degrade.
                if "tw-storydata" not in html_content:
                    raise RuntimeError(
                        f"Tweego exited 0 but produced no SugarCube story data "
                        f"({len(html_content)} bytes, no <tw-storydata>). Refusing to "
                        f"ship it — this is what a broken build looks like."
                    )
                if "tw-passagedata" not in html_content:
                    raise RuntimeError(
                        f"Tweego exited 0 but the build contains ZERO passages "
                        f"({len(html_content)} bytes). Refusing to ship it."
                    )

                logger.info(
                    "Compiled %r with %s (%s), %d bytes",
                    project_name,
                    tweego_cmd,
                    version_banner,
                    len(html_content),
                )
                return html_content
            else:
                # Clean up on failure
                if os.path.exists(twee_path):
                    os.unlink(twee_path)
                if os.path.exists(html_path):
                    os.unlink(html_path)
                raise RuntimeError(
                    f"Tweego compilation failed (exit code {result.returncode}):\n"
                    f"stderr: {result.stderr}\nstdout: {result.stdout}"
                )

        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Tweego compilation failed (exit code {e.returncode}):\n{e.stderr}"
            ) from e
        except subprocess.TimeoutExpired as e:
            raise RuntimeError(f"Tweego compilation timed out after 30 seconds") from e
        except FileNotFoundError as e:
            raise RuntimeError(f"Tweego binary not found during compilation: {e}") from e
        except RuntimeError:
            raise  # Re-raise our own RuntimeError from above
        except Exception as e:
            raise RuntimeError(f"Unexpected error during Tweego compilation: {e}") from e

    def package_game(
        self,
        project: Project,
        system_type: str,
        output_dir: str,
        version: str = "v2",
        options: Optional[dict] = None,
        force_copy: bool = False,
        verify_checksums: bool = False,
        local_media: bool = False,
        video_folder: Optional[str] = None,
        video_path: Optional[str] = None,
        debug: bool = False,
        graph: Optional[object] = None,
    ) -> dict[str, Any]:
        """
        Generate complete game package with HTML + media assets.

        Args:
            project: Django Project instance
            system_type: Type of game generation system
            output_dir: Absolute path to output directory
            version: Generator version (default: v1)
            options: Optional generation options
            force_copy: If True, copy all files; if False, skip existing
            verify_checksums: If True, use SHA256 instead of size check
            local_media: If True, replace R2 URLs with local relative paths
            video_folder: Optional path to folder containing video files (for validation/copying)
            video_path: Optional path prefix to use directly in HTML (no copying)
            debug: If True, show placeholder blocks for missing videos

        Returns:
            {
                'html_path': '/path/to/index.html',
                'media_dir': '/path/to/media/',
                'assets': {
                    'total': 10,
                    'copied': 5,
                    'skipped': 5,
                    'failed': 0,
                    'bytes_copied': 123456789,
                    'bytes_saved': 987654321,
                },
                'external_videos': {...},  # Stats for external video files
                'clips': [...],
                'errors': [...],
            }
        """
        from pathlib import Path

        from apps.assets.models import AssetClip

        # Validate inputs
        if system_type not in self.REGISTERED_SYSTEMS:
            available = ", ".join(self.REGISTERED_SYSTEMS.keys())
            raise ValueError(
                f"Unknown system type: {system_type}. Available: {available}"
            )

        output_path = Path(output_dir)
        if not output_path.is_absolute():
            raise ValueError("output_dir must be an absolute path")

        # Create output directory
        output_path.mkdir(parents=True, exist_ok=True)
        media_dir = output_path / "media"

        # Pass video_folder, video_path, and debug to generator via options
        options = options or {}
        if video_path:
            options["video_path"] = video_path
            # Use video_folder for validation if provided, else use video_path
            if not video_folder:
                video_folder = video_path
        if video_folder:
            options["video_folder"] = video_folder
        options["debug"] = debug

        # Step 1: Generate Twee content
        twee_content = self.generate_game(project, system_type, version, options, graph=graph)

        # Step 2: Compile to HTML
        html_content = self.compile_twee_to_html(twee_content, project.name)

        # Step 3: Get used assets from generator
        service = self._get_system_service(system_type)
        used_assets = {}
        if hasattr(service, "_last_generator"):
            generator = service._last_generator
            if hasattr(generator, "get_used_assets"):
                used_assets = generator.get_used_assets()

        # Step 4: Load clip objects with owner filtering
        clip_ids = used_assets.get("clips", [])
        clips = []
        if clip_ids:
            clips = list(
                AssetClip.objects.filter(
                    id__in=clip_ids, video__group__owner=project.owner
                ).select_related("video", "video__group")
            )

        # Step 5: Transform HTML URLs (absolute → relative)
        html_content = self._transform_html_urls(html_content)

        # Step 6: Copy media files with smart comparison
        copy_stats = self._copy_media_files(
            clips, media_dir, force_copy, verify_checksums
        )

        # Step 6.5: Copy external media files (videos + images + location images)
        external_video_stats = {
            "total": 0,
            "copied": 0,
            "skipped": 0,
            "failed": 0,
            "bytes_copied": 0,
            "bytes_saved": 0,
            "errors": [],
        }
        external_files = (
            used_assets.get("external_videos", [])
            + used_assets.get("external_images", [])
            + used_assets.get("location_images", [])
        )
        if video_folder and external_files:
            # Destination matches video_path prefix (e.g. ./videos → output/videos/)
            if video_path:
                video_output_dir = output_path / video_path.lstrip("./")
            else:
                video_output_dir = media_dir / "videos"
            external_video_stats = self._copy_video_files(
                video_folder=video_folder,
                video_files=external_files,
                output_dir=video_output_dir,
                force_copy=force_copy,
            )
        elif external_files and not video_folder:
            # The game references external images/videos (portraits, NPC/location art, clothing)
            # but no source folder was given, so NONE were copied — the build LOOKS green while
            # every one of those <img>/<video> tags will 404. Surface it loudly rather than ship
            # a silently-broken package. Re-run with --video-folder <path-to-media>.
            external_video_stats["skipped_no_video_folder"] = len(external_files)
            external_video_stats["errors"].append(
                f"{len(external_files)} external media file(s) referenced but NOT copied — "
                f"no --video-folder given. Sidebar portraits / NPC / location images will be "
                f"broken. Re-run with --video-folder <media dir>."
            )
            logger.warning(
                "package_game: %d external media files referenced but no video_folder "
                "provided — they were NOT copied (broken images in output).",
                len(external_files),
            )

        # Step 6.6: Localize R2 URLs if requested
        if local_media:
            url_mapping = self._build_url_mapping(clips)
            html_content = self._localize_media_urls(html_content, url_mapping)

        # Step 7: Write index.html
        html_path = output_path / "index.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        # Combine all errors
        all_errors = copy_stats.get("errors", []) + external_video_stats.get("errors", [])

        # Step 8: Return manifest with stats
        return {
            "html_path": str(html_path),
            "media_dir": str(media_dir),
            "assets": copy_stats,
            "external_videos": external_video_stats,
            "clips": [{"id": str(c.id), "file": c.file.name} for c in clips],
            "errors": all_errors,
        }

    def _transform_html_urls(self, html_content: str) -> str:
        """
        Transform absolute media URLs to relative paths.

        Converts: /media/assets/... → media/assets/...
        Leaves external URLs unchanged
        Handles both regular quotes and HTML entities (&quot;)
        """
        import re

        # Pattern to match both regular quotes and HTML entities
        # Matches: src="/media/..." or src=&quot;/media/...&quot;
        pattern = r'((?:src|poster)=(?:"|&quot;))(/media/[^"&]+)(?:"|&quot;)'

        def replace_url(match):
            prefix = match.group(1)
            url = match.group(2)
            url_relative = url.lstrip("/")
            # Determine quote style from prefix
            if "&quot;" in prefix:
                return f"{prefix}{url_relative}&quot;"
            else:
                return f'{prefix}{url_relative}"'

        return re.sub(pattern, replace_url, html_content)

    def _should_copy_file(
        self,
        source_storage_path: str,
        dest_local_path,
        force: bool,
        verify_checksum: bool,
    ) -> tuple[bool, str]:
        """
        Determine if file should be copied.

        Returns: (should_copy: bool, reason: str)

        Note: If file exists locally, it is preserved (not overwritten).
        This allows locally edited files (e.g., cut videos) to be kept.
        Use force=True to overwrite existing files.
        """
        if force:
            return True, "force_copy enabled"

        if not dest_local_path.exists():
            return True, "destination missing"

        # File exists locally → preserve it (don't overwrite with R2 version)
        return False, "file already exists"

    def _copy_media_files(
        self, clips, media_dir, force_copy: bool, verify_checksums: bool
    ) -> dict:
        """
        Copy media files using Django storage API (supports local + R2).
        """
        import shutil
        from pathlib import Path

        from django.core.files.storage import default_storage

        stats = {
            "total": 0,
            "copied": 0,
            "skipped": 0,
            "failed": 0,
            "bytes_copied": 0,
            "bytes_saved": 0,
            "errors": [],
        }

        for clip in clips:
            stats["total"] += 1

            # Get storage path (works with R2)
            clip_storage_path = clip.file.name
            dest_path = Path(media_dir) / clip_storage_path
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            # Check if copy needed
            should_copy, reason = self._should_copy_file(
                clip_storage_path, dest_path, force_copy, verify_checksums
            )

            if not should_copy:
                stats["skipped"] += 1
                stats["bytes_saved"] += default_storage.size(clip_storage_path)
                continue

            # Copy using storage API (not .path, which fails with R2)
            try:
                with default_storage.open(clip_storage_path, "rb") as src:
                    with open(dest_path, "wb") as dst:
                        shutil.copyfileobj(src, dst)

                file_size = default_storage.size(clip_storage_path)
                stats["copied"] += 1
                stats["bytes_copied"] += file_size

            except Exception as e:
                stats["failed"] += 1
                stats["errors"].append({"clip_id": str(clip.id), "error": str(e)})

            # Copy poster if exists
            if hasattr(clip, "poster") and clip.poster:
                try:
                    poster_storage_path = clip.poster.name
                    poster_dest = Path(media_dir) / poster_storage_path
                    poster_dest.parent.mkdir(parents=True, exist_ok=True)

                    should_copy_poster, _ = self._should_copy_file(
                        poster_storage_path, poster_dest, force_copy, verify_checksums
                    )

                    if should_copy_poster:
                        with default_storage.open(poster_storage_path, "rb") as src:
                            with open(poster_dest, "wb") as dst:
                                shutil.copyfileobj(src, dst)

                        poster_size = default_storage.size(poster_storage_path)
                        stats["bytes_copied"] += poster_size
                    else:
                        stats["bytes_saved"] += default_storage.size(
                            poster_storage_path
                        )

                except Exception as e:
                    stats["errors"].append(
                        {"poster_clip_id": str(clip.id), "error": str(e)}
                    )

        return stats

    def _copy_video_files(
        self,
        video_folder: str,
        video_files: list,
        output_dir,
        force_copy: bool = False,
    ) -> dict:
        """
        Copy external media files from source folder to output directory.
        Preserves nested directory structure.

        Args:
            video_folder: Source folder containing media files
            video_files: List of relative paths to copy (e.g., ["intro.mp4", "images/bg.jpg"])
            output_dir: Output directory (Path object) — files are placed directly here
            force_copy: If True, copy all files; if False, skip existing

        Returns:
            Dict with copy statistics
        """
        import shutil
        from pathlib import Path

        stats = {
            "total": len(video_files),
            "copied": 0,
            "skipped": 0,
            "failed": 0,
            "bytes_copied": 0,
            "bytes_saved": 0,
            "errors": [],
        }

        video_output_dir = Path(output_dir)
        source_folder = Path(video_folder)

        for relative_path in video_files:
            try:
                source_path = source_folder / relative_path
                dest_path = video_output_dir / relative_path

                # Security: Validate path doesn't escape video folder
                try:
                    resolved_source = source_path.resolve()
                    resolved_folder = source_folder.resolve()
                    if not str(resolved_source).startswith(str(resolved_folder)):
                        stats["failed"] += 1
                        stats["errors"].append({
                            "file": relative_path,
                            "error": "Path traversal attempt blocked"
                        })
                        continue
                except Exception:
                    pass  # If resolve fails, continue with normal validation

                if not source_path.exists():
                    stats["failed"] += 1
                    stats["errors"].append({
                        "file": relative_path,
                        "error": "File not found"
                    })
                    continue

                # Create parent directories for nested paths
                dest_path.parent.mkdir(parents=True, exist_ok=True)

                # Check if copy/compress needed.
                # Size is NOT a usable freshness signal here: images are downscaled to
                # max width 800 below, so the destination is always smaller than its
                # source after the first copy. A size-based skip therefore matched every
                # time and a REPLACED source image could never reach the built game —
                # the long-standing "I swapped the art but the game still shows the old
                # one" bug. Compare modification time instead: re-copy whenever the
                # source is newer than what was last written out.
                should_copy = True
                file_size = source_path.stat().st_size
                if not force_copy and dest_path.exists():
                    if source_path.stat().st_mtime <= dest_path.stat().st_mtime:
                        should_copy = False

                if should_copy:
                    image_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
                    if source_path.suffix.lower() in image_extensions:
                        try:
                            img = Image.open(source_path)
                            if img.mode in ('RGBA', 'P'):
                                img = img.convert('RGB')
                            max_width = 800
                            if img.width > max_width:
                                ratio = max_width / img.width
                                new_size = (max_width, int(img.height * ratio))
                                img = img.resize(new_size, Image.LANCZOS)
                            save_kwargs = {'optimize': True}
                            if dest_path.suffix.lower() in {'.jpg', '.jpeg'}:
                                save_kwargs['quality'] = 85
                            elif dest_path.suffix.lower() == '.webp':
                                save_kwargs['quality'] = 85
                            img.save(dest_path, **save_kwargs)
                        except Exception:
                            shutil.copy2(source_path, dest_path)
                    else:
                        shutil.copy2(source_path, dest_path)
                    stats["copied"] += 1
                    stats["bytes_copied"] += file_size
                else:
                    stats["skipped"] += 1
                    stats["bytes_saved"] += file_size

            except Exception as e:
                stats["failed"] += 1
                stats["errors"].append({
                    "file": relative_path,
                    "error": str(e)
                })

        return stats

    def _build_url_mapping(self, clips) -> dict:
        """
        Build mapping from R2 URLs to local relative paths.

        Args:
            clips: List of AssetClip objects

        Returns:
            Dictionary mapping R2 URLs to local relative paths
        """
        url_map = {}

        for clip in clips:
            # Map video file URL
            if clip.file:
                r2_url = clip.file.url
                local_path = f"media/{clip.file.name}"
                url_map[r2_url] = local_path

            # Map poster URL if exists
            if hasattr(clip, "poster") and clip.poster:
                poster_url = clip.poster.url
                poster_path = f"media/{clip.poster.name}"
                url_map[poster_url] = poster_path

        return url_map

    def _localize_media_urls(self, html_content: str, url_mapping: dict) -> str:
        """
        Replace R2 URLs with local relative paths in HTML.

        Args:
            html_content: HTML content with R2 URLs
            url_mapping: Dictionary mapping R2 URLs to local paths

        Returns:
            HTML content with localized URLs
        """
        for r2_url, local_path in url_mapping.items():
            html_content = html_content.replace(r2_url, local_path)

        return html_content
