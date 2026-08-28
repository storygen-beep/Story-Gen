"""
Twee Comprehensive Generator v2.

Forked from v1 on 2026-05-14 as a wholesale copy. All new engine work
(NPC location schedules, requires_npc presence-detection on Lane 2/3
triggers, single-canvas hubs with conditional button injection per RTS
doctrine, etc.) lands here. v1 is frozen as a safe-mode rollback path
and will be deleted once v2 is stable for ~2 weeks.

Comprehensive game generator that creates sophisticated interactive experiences.
This is the isolated, self-contained comprehensive game generation system.
"""

import hashlib
import json
import html
import logging
import re
from typing import Any, Dict, List, Optional, Set, Tuple

from pathlib import Path

from apps.common.media_blocks import block_media_pool
from apps.projects.models import Project

logger = logging.getLogger(__name__)

# Extension sets for media type detection
VIDEO_EXTENSIONS = {'.mp4', '.webm', '.mov', '.m4v', '.avi', '.mkv'}
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp'}

# Cascade-aware exit routing: planted by _render_cascade_tail at the deepest
# advance-beat's linkreplace body. _generate_canvas_node_passages swaps it
# with the rendered exit-block HTML so exits stay hidden until the player
# clicks through the cascade's final advance link. Per RTS Pattern E doctrine
# (memory rts_cross_npc_mechanism_comparison.md). HTML-comment form chosen
# so the string can never collide with author prose (BlockNote → game HTML
# never emits raw HTML comments).
_CASCADE_EXIT_INJECT_SENTINEL = "<!--__CASCADE_EXIT_INJECT__-->"

# P7 audit fix (2026-05-12) — Pattern C support. Cascades whose beats have
# `conditions` (gates) plant this SAFE sentinel instead of the STANDARD one
# above. The cascade-aware exit-routing branch checks for SAFE first: if found
# anywhere in node_content, take the conservative path (strip all sentinels
# + leave passage_body intact for bottom-of-passage exit render). Reason: a
# gated beat can fail its gate at runtime, terminating the cascade before
# the planted-on-last-advance-beat sentinel renders. Without bottom-of-passage
# exits, the player gets stuck. RTS-aligned: scenes with mid-cascade gates
# render exits at passage bottom, not inside cascade. See _render_cascade
# `has_gated_beats` check + cascade-aware exit substitution branch.
_CASCADE_EXIT_INJECT_SAFE_SENTINEL = "<!--__CASCADE_EXIT_INJECT_SAFE__-->"

# Studio identity baked into every build: the funding link (sidebar button + both
# intro/age-gate links) and the credit line under the age gate. These were literals
# in the generator until 2026-07-29; they are now `[project] support_url` /
# `studio_name`, so a game can ship under a different campaign or studio without a
# code change.
#
# The fallback lives HERE, generator-side, not as a TemplateProject default — the
# TOML has a second, independent reader (build_guide.py parses [project] with
# tomllib, bypassing template_import entirely), and an importer-side default would
# leave that reader seeing an empty string and quietly disagreeing with the sidebar.
# One constant, one resolver, three call sites.
#
# Unset => these exact bytes, so every game built before this change still builds
# byte-identical (html.escape is a no-op on both — no &, <, >, " or ').
DEFAULT_SUPPORT_URL = "https://www.patreon.com/cw/nutgames844"
DEFAULT_STUDIO_NAME = "NutGames"


class TweeComprehensiveGeneratorV2:
    """
    Simplified Twee generator for canvas-based stories.

    Generates simple game flow:
    - Game Entry: Project info and start game
    - Starting Canvas: Display designated starting canvas
    - Navigation: Basic location-to-location movement
    - Locations: Simple location descriptions and navigation

    Completely isolated from other generation systems.
    """

    # {row id: plaintext cheat code}, injected by the packager from a game's untracked
    # codes file. Class-level and empty by default so the throwaway instances that only
    # call validate_flag_chains() — which never set options — can still read it, and so
    # a caller that never heard of codes produces a page whose box opens nothing rather
    # than a crash.
    cheat_codes: dict = {}

    def __init__(self):
        self.project = None
        # No-DB build (the DEFAULT): when set, the generator reads this in-memory
        # object graph instead of querying the ORM (see game_graph.build_game_graph).
        # The `if self.graph is None:` ORM fallback branches throughout are the
        # DEPRECATED legacy DB path, kept for the web API / elora / test callers.
        self.graph = None
        self.locations = []
        self.connections = []
        self._adjacency = {}
        self.story_canvases = []
        self.game_config = {}
        self.passage_name_map = {}  # Maps node IDs to Twee passage names
        self.used_assets = {  # Track assets actually used in generated game
            'clips': set(),   # Set of AssetClip IDs
            'videos': set(),  # Set of AssetVideo IDs
            'images': set(),  # Set of image URLs
            'external_videos': set(),  # Set of external video file paths
            'external_images': set(),  # Set of external image file paths
            'location_images': set(),  # Set of location image paths
        }
        # Video file support
        self.video_folder = None
        self.video_path = None  # Direct path mode - use this path in HTML (no copy)
        self.video_files = {}  # relative_path -> full_path mapping
        self.debug = False
        # Dev mode for testing (adds +/- stat controls)
        self.dev_mode = False
        # Missing media tracking for debug page
        self.missing_media = []
        self.current_canvas_id = None  # Set during canvas processing
        # Location images for visual navigation
        self.location_images = {}  # location_id -> resolved image path (only found files)
        self.location_image_defined = set()  # location_ids with image path defined (found or missing)

    def generate(
        self,
        project: Project,
        options: Optional[dict] = None,
        graph: Optional[object] = None,
    ) -> str:
        """
        Generate comprehensive Twee content.

        Args:
            project: Django Project instance
            options: Optional generation options
            graph: Optional in-memory GameGraph for the no-DB build path. When
                provided, all data intake reads the graph instead of the ORM.

        Returns:
            str: Complete Twee content with all features
        """
        self.project = project
        self.graph = graph
        self.options = options or {}

        # Load video files if video_folder is provided
        self.video_folder = self.options.get("video_folder")
        self.video_path = self.options.get("video_path")  # Direct path mode
        self.debug = self.options.get("debug", False)
        self.dev_mode = self.options.get("dev_mode", False)
        # Cheat codes, if the packager was given a codes file. Anything that is not a
        # dict of strings is treated as no codes at all rather than half-trusted.
        _codes = self.options.get("cheat_codes")
        self.cheat_codes = {
            str(k): str(v) for k, v in _codes.items()
        } if isinstance(_codes, dict) else {}
        if self.video_folder:
            self._load_media_files()

        # Load project data and compute included canvases (starting, triggered, and referenced)
        self._load_project_data()
        self._build_location_image_map()
        self._compute_included_canvases()

        # Load clips for included canvases with owner security filtering
        self._load_all_clips()

        # Build passage name map for cross-canvas node references (stable and consistent with emission)
        self._build_passage_name_map()

        # Build game configuration
        self.game_config = self._build_game_config()

        # Generate simplified game
        twee_sections = []

        # Add game metadata
        twee_sections.append(self._generate_metadata())

        # Add simple initialization
        twee_sections.append(self._generate_initialization())

        # Add NPC customization screen (only if customizable NPCs exist)
        customize_passage = self._generate_customize_passage()
        if customize_passage:
            twee_sections.append(customize_passage)

        # Add age blocked passage for users who are not 18+
        twee_sections.append(self._generate_age_blocked_passage())

        # Add time system if enabled
        time_settings = self.project.get_time_settings()
        if time_settings.get("enabled", True):
            twee_sections.append(self._generate_time_system())

        # Trait helpers are injected in Start's initialization script for reliability

        # Add starting canvas
        twee_sections.append(self._generate_starting_canvas())

        # Add basic navigation
        twee_sections.append(self._generate_basic_navigation())

        # Defense-in-depth: broken-exit fallback (loud throw, not silent redirect).
        # Layer 1 (validator) prevents broken refs from shipping; this passage exists
        # only for paths that bypass the validator (test fixtures, dev API, etc.).
        twee_sections.append(self._generate_broken_exit_fallback())

        # Add simple locations
        twee_sections.append(self._generate_simple_locations())

        # Add story canvases
        twee_sections.append(self._generate_story_canvases())

        # Add missing media page (always generated, but button only shows in debug mode)
        twee_sections.append(self._generate_missing_media_page())

        # Player cheat page + its sidebar button widget. Emitted as its OWN section,
        # deliberately not inside _generate_time_system() — that section is only
        # appended when [time] enabled, and the widget must be defined unconditionally
        # (SugarCube throws on an undefined widget call from StoryCaption).
        # Cast page + its sidebar button widget. Same reason as the cheat page for
        # living in its own section: the widget must be defined unconditionally.
        twee_sections.append(self._generate_cast_page())

        twee_sections.append(self._generate_cheat_page())

        # Add canvas review pages (only in dev mode)
        if self.dev_mode:
            twee_sections.append(self._generate_canvas_review_pages())

        # Add theme CSS variables (always, provides defaults for all sections)
        twee_sections.append(self._generate_theme_stylesheet())

        # Add phone CSS (only when phone enabled)
        if self.phone_enabled:
            twee_sections.append(self._generate_phone_css())

        output = "\n\n".join(twee_sections)

        # PRD 48 — strip the sidebar hint mechanism from V2 game output.
        # V1 games keep all functions intact (they're still used by the V1
        # sidebar `hint`-type item). V2 doesn't surface a sidebar hint, so
        # the underlying JS functions are dead code — purge them.
        output = self._strip_sidebar_mechanism_if_v2(output)

        # Last gate before the file leaves the generator: prove no plaintext cheat code
        # reached the output. Raises rather than returning a quietly-wrong file.
        self._assert_no_plaintext_codes(output)

        return output

    def _assert_no_plaintext_codes(self, output: str) -> None:
        """Fail the build if a cheat code reached the output in plaintext.

        Why an assertion and not a regex strip: a strip that under-matches ships a
        leaked file that still looks green. An assertion cannot fail quietly — and the
        thing being protected (a code that is supposed to arrive with a paid guide, in
        a file published to every portal) is not something to discover afterwards.

        Cheap belt-and-braces over `_generate_cheat_code_script`, which only ever emits
        hashes. This catches a future edit that breaks it — for instance an author
        putting the code in a row's `hint`, which would be an easy mistake to make and
        an expensive one to notice.

        The comparison is case-insensitive and whitespace-stripped on the OUTPUT side
        too, because a code that survives normalisation is still a working code.
        """
        if not self.cheat_page or not self.cheat_codes:
            return

        haystack = self.normalize_cheat_code(output)
        for grant_id, code in self.cheat_codes.items():
            needle = self.normalize_cheat_code(code)
            # A one- or two-character "code" would collide with ordinary prose and make
            # this check useless noise; validate() already rejects those upstream.
            if len(needle) >= 3 and needle in haystack:
                raise RuntimeError(
                    f"cheat page integrity: the plaintext code for row '{grant_id}' appears "
                    f"in the output. Codes must reach players through the guide, never "
                    f"through the published file — check the row's hint, label and intro."
                )

    def _strip_sidebar_mechanism_if_v2(self, output: str) -> str:
        """PRD 48 — Remove sidebar hint JS functions and widget branch
        from V2 game output. No-op for V1 games.

        Targets (per audit):
          - 8 `setup.<name> = function ...` definitions used only by the
            sidebar hint walker (getSidebarHint, getNextActivity, +6 helpers)
          - 1 `<<elseif _item.type is "hint">>` branch in the sidebarItems
            widget that calls `setup.getSidebarHint()`

        NOT touched (shared with other systems):
          - `setup.formatCanvasConditions` — used by the location-blocking
            UI ("Required: trust ≥ 10" message). The sidebar caller goes
            away naturally when `getSidebarHint` is stripped.
          - `setup.checkSingleCondition`, `setup.triggerConditionsSatisfied`,
            `setup.npcSlugForId`, `setup.getStageHintForNPC`,
            `setup._formatCanvasSchedule`, `setup._locNameFromUuid`,
            `setup.getDecayWarnings`, `setup.getGlobalHints` — all
            shared utilities used by Quests engine, decay warnings, E10/E11,
            etc. Keep intact.
        """
        if (self.project.metadata or {}).get("quests_engine") != "v2":
            return output

        import re as _re

        # Each sidebar-only function. Pattern matches from the declaration
        # to the terminating `};\n` at column 0 (i.e. the function-level
        # close, not any nested object/closure close). The functions are
        # well-bounded at the top level — inner blocks close with `}` not
        # `};\n` so this is unambiguous.
        sidebar_fns = (
            "getSidebarHint",
            "getNextActivity",
            "formatFlagHint",
            "formatActivityHint",
            "getBestFlagHint",
            "resolveUnlockChain",
            "checkTraitRequirement",
            "calculateDaysRemaining",
        )
        for fn in sidebar_fns:
            pattern = (
                r"setup\." + _re.escape(fn) + r" = function[\s\S]*?\n\};\s*\n"
            )
            output = _re.sub(pattern, "", output)

        # Widget branch: from `  <<elseif _item.type is "hint">>` (2-space
        # indent inside `<<widget "sidebarItems">>`) up to (but not
        # including) the next sibling `<<elseif`. Other branches stay.
        widget_branch_pattern = (
            r'  <<elseif _item\.type is "hint">>\n'
            r'[\s\S]*?'
            r'(?=  <<elseif )'
        )
        output = _re.sub(widget_branch_pattern, "", output)

        return output

    def get_used_assets(self) -> dict:
        """
        Get assets actually used in generated game.

        This method should be called after generate() to retrieve information
        about which media assets (clips, videos, images) were actually rendered
        in the game. Useful for packaging games with only necessary media files.

        Returns:
            Dict with asset lists:
                {
                    'clips': list of AssetClip ID strings,
                    'videos': list of AssetVideo ID strings,
                    'images': list of image URL strings,
                    'external_videos': list of video file relative paths
                }
        """
        return {
            'clips': list(self.used_assets['clips']),
            'videos': list(self.used_assets['videos']),
            'images': list(self.used_assets['images']),
            'external_videos': list(self.used_assets['external_videos']),
            'external_images': list(self.used_assets['external_images']),
            'location_images': list(self.used_assets['location_images']),
        }

    def _load_media_files(self):
        """
        Build mapping of media (video + image) relative paths to full paths.
        Supports nested folders via recursive scan.
        """
        from pathlib import Path

        media_path = Path(self.video_folder)
        if not media_path.is_dir():
            logger.warning(f"Media folder is not a directory: {self.video_folder}")
            return

        # Support common video and image extensions
        video_extensions = {'.mp4', '.webm', '.mov', '.m4v', '.avi', '.mkv'}
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'}
        media_extensions = video_extensions | image_extensions

        # Recursive scan using rglob. NOTE rglob('*') DOES return dotfiles, and this
        # index is what _resolve_pool_dir prefix-matches to decide what the shipped game
        # plays — so a dot-prefixed name (find-media staging, an editor swap file, or
        # macOS AppleDouble `._clip.gif`, which carries a real media suffix) would ship
        # a partial clip to a player. This is the one guard that reaches the build.
        for file in media_path.rglob('*'):
            if file.name.startswith('.'):
                continue
            if file.is_file() and file.suffix.lower() in media_extensions:
                # Store relative path as key (e.g., "chapter1/intro.mp4" or "images/bg.jpg")
                relative_path = file.relative_to(media_path)
                # Normalize to forward slashes for cross-platform consistency
                self.video_files[str(relative_path).replace('\\', '/')] = str(file)

        logger.info(
            f"Loaded {len(self.video_files)} media files from {self.video_folder}",
            extra={"project_id": str(self.project.id) if self.project else None}
        )

    def _load_project_data(self):
        """Load project data including story canvases with schedule information."""
        if self.graph is not None:
            # No-DB path: read the in-memory graph instead of the ORM.
            self.locations = self.graph.locations
            self.clips_by_id = {}
            starting_id = (
                str(self.project.starting_canvas.id)
                if self.project.starting_canvas else None
            )
            # Mirror StoryCanvas.Meta.ordering ["display_order"(=0), "-created_at"]
            # = reverse insertion order (canvases minted in template order).
            ordered = sorted(self.graph.canvases, key=lambda c: c._seq, reverse=True)
            self.story_canvases = [
                c for c in ordered
                if str(c.id) != starting_id
                and getattr(c, 'trigger', None) and c.trigger.location_id
            ]
            return

        from apps.stories.models import StoryCanvas
        from apps.world.models import Location

        # Load locations with simplified navigation (entry_from)
        self.locations = list(Location.objects.filter(project=self.project).select_related('entry_from'))

        # Initialize clips lookup dictionary for bulk loading
        self.clips_by_id = {}

        # Load story canvases initial set (excluding starting canvas) that have triggers with location_id
        # Include schedule data with prefetch_related for efficiency
        story_canvas_query = StoryCanvas.objects.filter(
            project=self.project,
            deleted_at__isnull=True
        ).select_related('trigger').prefetch_related('trigger__schedules', 'nodes')

        # Exclude starting canvas if it exists
        if self.project.starting_canvas:
            story_canvas_query = story_canvas_query.exclude(id=self.project.starting_canvas.id)

        # Initial story canvases: only those with triggers and location_id (more may be included by reference)
        self.story_canvases = []
        for canvas in story_canvas_query:
            if hasattr(canvas, 'trigger') and canvas.trigger and canvas.trigger.location_id:
                self.story_canvases.append(canvas)

    def _build_location_image_map(self):
        """
        Build mapping of location IDs to resolved image paths for visual navigation.
        Uses extension-agnostic matching via _find_media_file().
        Tracks images in used_assets and missing images in missing_media.
        """
        for loc in self.locations:
            loc_props = getattr(loc, 'properties', None) or {}
            loc_id = str(loc.id)
            image_path = loc_props.get("image", "")

            if not image_path:
                continue

            # Track that this location has an image defined (even if file is missing)
            self.location_image_defined.add(loc_id)

            # Get search queries for Missing Media page links
            search_queries = loc_props.get("image_search_queries", [])

            # Validate and resolve image using extension-agnostic matching
            actual_path, actual_ext = self._find_media_file(image_path)

            if actual_path:
                self.location_images[loc_id] = actual_path
                self.used_assets['location_images'].add(actual_path)
                logger.debug(
                    f"Location image resolved: {loc.name} -> {actual_path}",
                    extra={"project_id": str(self.project.id)}
                )
            else:
                # Track missing image for debug page
                self.missing_media.append({
                    'file': image_path,
                    'type': 'location_image',
                    'description': f"Navigation image for {loc.name}",
                    'search_queries': search_queries,
                    'location_id': loc_id,
                    'location_name': loc.name,
                    'canvas_id': 'navigation',
                    'category': 'Locations',
                })
                logger.warning(
                    f"Location image not found: {image_path} for {loc.name}",
                    extra={"project_id": str(self.project.id)}
                )

    def _load_all_clips(self):
        """
        Bulk load clips with SECURITY CRITICAL owner filtering.
        PERFORMANCE: Single query to avoid N+1 problem.
        """
        if self.graph is not None:
            # No-DB / local-media builds don't reference AssetClip UUID blocks;
            # media resolves from the filesystem video-folder instead.
            self.clips_by_id = {}
            return

        from apps.assets.models import AssetClip
        from apps.stories.models import StoryCanvas
        import uuid as uuid_module

        # Collect all clip IDs from included canvases
        clip_ids = set()
        canvas_ids = getattr(self, 'included_canvas_ids', set())
        if not canvas_ids:
            return

        # Get all nodes from included canvases
        canvases = StoryCanvas.objects.filter(
            id__in=list(canvas_ids)
        ).prefetch_related('nodes')

        for canvas in canvases:
            for node in self._get_canvas_nodes_ordered(canvas):
                if not hasattr(node, 'node_data') or not node.node_data:
                    continue
                blocks = node.node_data.get('blocks', [])
                for block in blocks:
                    if block.get('type') == 'clip':
                        clip_id = block.get('props', {}).get('clipId')
                        if clip_id:
                            try:
                                clip_ids.add(uuid_module.UUID(clip_id))
                            except (ValueError, AttributeError):
                                logger.warning(
                                    f"Invalid clip UUID: {clip_id}",
                                    extra={"project_id": str(self.project.id)}
                                )
                                continue

        # SECURITY CRITICAL: Bulk load with owner filter
        if clip_ids:
            clips = AssetClip.objects.filter(
                id__in=list(clip_ids),
                video__group__owner=self.project.owner,  # SECURITY: Owner validation
                deleted_at__isnull=True,
                status="complete"
            ).select_related('video__group')

            self.clips_by_id = {str(clip.id): clip for clip in clips}

            logger.info(
                f"Loaded {len(self.clips_by_id)}/{len(clip_ids)} clips for game generation",
                extra={
                    "project_id": str(self.project.id),
                    "requested": len(clip_ids),
                    "loaded": len(self.clips_by_id)
                }
            )

    def _compute_included_canvases(self):
        """Compute the full set of canvases to include: starting, triggered, and any referenced by node-target choices."""
        if self.graph is not None:
            self._compute_included_canvases_graph()
            return

        from apps.stories.models import StoryCanvas, StoryNode

        included_ids = set()

        # Include starting canvas if present
        if self.project.starting_canvas:
            included_ids.add(str(self.project.starting_canvas.id))

        # Include canvases with triggers (initial set from _load_project_data)
        for c in self.story_canvases:
            included_ids.add(str(c.id))

        # Closure: pull in canvases referenced by any choice targetType 'node'
        # OR by a Lane 3 substitution rule (PRD 25). Both reachability sources
        # walk the same closure; without the substitution walk, canvases marked
        # `substitution_only = true` and only referenced by another canvas's
        # substitution rule would get pruned silently from the build.
        changed = True
        while changed:
            changed = False
            # Iterate over currently included canvases and scan their nodes' exit blocks
            canvases = StoryCanvas.objects.filter(id__in=list(included_ids)).prefetch_related('nodes', 'trigger')
            for canvas in canvases:
                # Walk substitution rules on this canvas's trigger (PRD 25)
                trigger = getattr(canvas, 'trigger', None)
                if trigger:
                    subs = (trigger.metadata or {}).get('substitutions') or []
                    for rule in subs:
                        target_slug = rule.get('target_canvas_id') if isinstance(rule, dict) else None
                        if not target_slug:
                            continue
                        # Resolve slug → canvas. Slug is stored at metadata["slug"]
                        # by template_import.py:4264.
                        target_canvas = StoryCanvas.objects.filter(
                            project=self.project, metadata__slug=target_slug
                        ).only('id').first()
                        if target_canvas and str(target_canvas.id) not in included_ids:
                            included_ids.add(str(target_canvas.id))
                            changed = True

                for node in self._get_canvas_nodes_ordered(canvas):
                    try:
                        exit_block = getattr(node, 'exit_block', None) or {}
                        if exit_block.get('type') == 'choices':
                            for choice in exit_block.get('choices', []) or []:
                                if choice.get('targetType') == 'node':
                                    target_node_id = choice.get('nodeId')
                                    if target_node_id:
                                        target_node = StoryNode.objects.filter(id=target_node_id).only('canvas_id').first()
                                        if target_node and str(target_node.canvas_id) not in included_ids:
                                            included_ids.add(str(target_node.canvas_id))
                                            changed = True
                    except (KeyError, TypeError, ValueError) as e:
                        logger.error(
                            "Malformed exit_block in canvas '%s' node '%s': %s",
                            canvas.name if canvas else "unknown",
                            node.name if hasattr(node, 'name') else "unknown",
                            e
                        )
                        raise ValueError(
                            f"Invalid exit_block structure in canvas '{canvas.name if canvas else 'unknown'}': {e}"
                        ) from e

        # Store the full set of included canvas IDs (for clip loading)
        self.included_canvas_ids = included_ids.copy()

        # Rebuild self.story_canvases to be all included (excluding starting canvas to avoid duplication)
        if self.project.starting_canvas:
            included_ids.discard(str(self.project.starting_canvas.id))
        from apps.stories.models import StoryCanvas as SC
        self.story_canvases = list(SC.objects.filter(id__in=list(included_ids)))

    def _compute_included_canvases_graph(self):
        """No-DB twin of _compute_included_canvases: walk the closure over the
        in-memory graph (canvas_by_slug / node_by_id) instead of the ORM."""
        g = self.graph
        by_id = {str(c.id): c for c in g.canvases}

        included_ids = set()
        if self.project.starting_canvas:
            included_ids.add(str(self.project.starting_canvas.id))
        for c in self.story_canvases:
            included_ids.add(str(c.id))

        changed = True
        while changed:
            changed = False
            for cid in list(included_ids):
                canvas = by_id.get(cid)
                if canvas is None:
                    continue
                trigger = getattr(canvas, 'trigger', None)
                if trigger:
                    subs = (trigger.metadata or {}).get('substitutions') or []
                    for rule in subs:
                        target_slug = rule.get('target_canvas_id') if isinstance(rule, dict) else None
                        if not target_slug:
                            continue
                        target_canvas = g.canvas_by_slug.get(target_slug)
                        if target_canvas and str(target_canvas.id) not in included_ids:
                            included_ids.add(str(target_canvas.id))
                            changed = True
                for node in self._get_canvas_nodes_ordered(canvas):
                    exit_block = getattr(node, 'exit_block', None) or {}
                    if exit_block.get('type') == 'choices':
                        for choice in exit_block.get('choices', []) or []:
                            if choice.get('targetType') == 'node':
                                target_node_id = choice.get('nodeId')
                                if target_node_id:
                                    target_node = g.node_by_id.get(target_node_id)
                                    if target_node and str(target_node.canvas_id) not in included_ids:
                                        included_ids.add(str(target_node.canvas_id))
                                        changed = True

        self.included_canvas_ids = included_ids.copy()
        if self.project.starting_canvas:
            included_ids.discard(str(self.project.starting_canvas.id))
        # Mirror the ORM Meta.ordering (-created_at = reverse insertion order).
        self.story_canvases = [
            c for c in sorted(g.canvases, key=lambda c: c._seq, reverse=True)
            if str(c.id) in included_ids
        ]

    def _build_passage_name_map(self):
        """Build mapping of node IDs to Twee passage names for cross-canvas references."""
        # Map starting canvas nodes (by creation order)
        if self.project.starting_canvas:
            nodes = self._get_canvas_nodes_ordered(self.project.starting_canvas)
            canvas_prefix = self._sanitize_canvas_name(self._get_canvas_slug(self.project.starting_canvas))
            for i, node in enumerate(nodes):
                passage_name = self._node_passage_name("StartingCanvas", canvas_prefix, node)
                self.passage_name_map[str(node.id)] = passage_name

        # Map included story canvas nodes (by creation order)
        for canvas in self.story_canvases:
            nodes = self._get_canvas_nodes_ordered(canvas)
            canvas_prefix = self._sanitize_canvas_name(self._get_canvas_slug(canvas))
            for i, node in enumerate(nodes):
                passage_name = self._node_passage_name("Canvas", canvas_prefix, node)
                self.passage_name_map[str(node.id)] = passage_name

    def _build_game_config(self) -> dict[str, Any]:
        """Build simplified game configuration."""
        return {
            "project_name": self.project.name,
            "project_id": str(self.project.id),
            "has_starting_canvas": self.project.starting_canvas is not None,
            "location_count": len(self.locations),
            "connection_count": len(self.connections),
            "story_canvas_count": len(self.story_canvases),
        }

    def _generate_metadata(self) -> str:
        """Generate game metadata."""
        story_name = self.project.name or "Comprehensive Interactive Game"

        return f""":: Story [meta]
{{
    "name": "{story_name}",
    "ifid": "{self.project.id}",
    "format": "SugarCube",
    "format-version": "2.36.1",
    "start": "Start"
}}

:: StoryTitle
{story_name}

:: StoryData
{{
    "ifid": "{self.project.id}",
    "format": "SugarCube",
    "format-version": "2.36.1",
    "start": "Start"
}}"""

    def _project_metadata(self) -> dict:
        """`self.project.metadata` as a real dict, or {} — never a Mock.

        Some test callers pass a MagicMock project (apps/projects/tests.py), where a
        bare attribute read returns a truthy Mock whose .get() yields another Mock;
        html.escape() then raises. isinstance is the only read that survives both.
        """
        meta = getattr(self, "project", None)
        meta = getattr(meta, "metadata", None)
        return meta if isinstance(meta, dict) else {}

    def _resolve_support_url(self) -> str:
        """HTML-escaped funding URL for the sidebar button and both intro links.

        Authored as `[project] support_url`; falls back to DEFAULT_SUPPORT_URL so a
        game that never sets it emits the bytes it always has. Escaped for an href
        attribute: a `&` in a query string becomes `&amp;` here, which is correct —
        Tweego stores passage text escaped, the browser decodes it once, and the DOM
        href ends up with a real `&` (same round-trip as the known `&amp;#x27;`
        apostrophe behaviour; the missing-media search links at _build_search_url
        already ship this exact urlencode -> html.escape -> href pattern).
        """
        url = str(self._project_metadata().get("support_url", "") or "").strip()
        return html.escape(url or DEFAULT_SUPPORT_URL)

    def _resolve_studio_name(self) -> str:
        """HTML-escaped studio credit for the age-gate footer ("Developed by X")."""
        name = str(self._project_metadata().get("studio_name", "") or "").strip()
        return html.escape(name or DEFAULT_STUDIO_NAME)

    def _generate_initialization(self) -> str:
        """Generate simple initialization with time system."""
        project_name = self.game_config.get('project_name', 'Interactive Game')
        project_description = getattr(self.project, 'description', '') or 'An interactive story experience'
        support_url = self._resolve_support_url()
        studio_name = self._resolve_studio_name()

        # Get time settings from project
        time_settings = self.project.get_time_settings()

        # Determine the start game target dynamically
        start_target = "StartingCanvas"  # Default fallback

        if self.project.starting_canvas:
            try:
                # Check if starting canvas has nodes
                nodes = self._get_canvas_nodes_ordered(self.project.starting_canvas)
                if nodes:
                    # Point directly to first node (by stable node slug)
                    canvas_name = self._sanitize_canvas_name(self._get_canvas_slug(self.project.starting_canvas))
                    start_target = self._node_passage_name("StartingCanvas", canvas_name, nodes[0])
                # If no nodes, keep default "StartingCanvas"
            except (AttributeError, TypeError) as e:
                logger.warning(
                    "Error determining start target for starting canvas: %s. Using fallback.",
                    e
                )

        # Check for customizable NPCs — redirect to customization screen if any exist
        self._original_start_target = start_target

        # Load player and NPC trait/flag data
        player_name = "Player"
        player_portrait = ""
        player_traits = {}
        player_flag_keys: list[str] = []
        player_trait_decay: dict[str, float] = {}
        try:
            pc = getattr(self.project, 'player_character', None)
            if pc is not None:
                player_name = pc.name or player_name
                # Read portrait from character_metadata JSON (not URLField)
                pc_metadata = getattr(pc, 'character_metadata', None) or {}
                player_portrait = pc_metadata.get("portrait", "")
                player_traits = pc.core_traits or {}
                player_flag_keys = list(getattr(pc, 'flag_keys', []) or [])
                # Per-day decay for player traits (hygiene, etc.)
                _td_raw = pc_metadata.get("trait_decay") or {}
                if isinstance(_td_raw, dict):
                    for k, v in _td_raw.items():
                        try:
                            player_trait_decay[str(k)] = float(v)
                        except (ValueError, TypeError):
                            pass
        except (AttributeError, TypeError) as e:
            logger.warning("Error loading player character data: %s", e)
        self.player_trait_decay_config = player_trait_decay

        # Store player portrait and description as instance variables
        self.player_portrait = player_portrait
        self.player_description = getattr(pc, 'description', '') if pc else ''
        # Track player portrait for file copying
        if player_portrait:
            self.used_assets['external_images'].add(player_portrait)

        # Load player customization data
        self.player_customizable = False
        self.player_customization_fields = []
        self.player_name = player_name
        try:
            pc_metadata = getattr(pc, 'character_metadata', None) or {} if pc else {}
            self.player_customizable = pc_metadata.get("customizable", False)
            self.player_customization_fields = pc_metadata.get("customization_fields", [])
            # Track image_select option images for file copying
            for cf in self.player_customization_fields:
                if cf.get("type") == "image_select":
                    for opt in cf.get("options", []):
                        if opt.get("image"):
                            self.used_assets['external_images'].add(opt["image"])
        except (AttributeError, TypeError):
            pass

        npc_map = {}
        npc_slug_map = {}  # Maps NPC slug to UUID for condition resolution
        hidden_npcs_map = {}  # Maps NPC UUID -> True for NPCs flagged hidden_from_ui
        # E9/E10/E11: slug → [stage display names]. Foundation registry. Empty
        # for NPCs without arc_stages — runtime checks length to know whether
        # to engage stage-related code paths.
        npc_arc_stages_map = {}
        # G: slug → [tag phrases] for the cast card's tag line. A SEPARATE registry
        # rather than a field on $npcs, deliberately: $npcs is snapshotted into every
        # history moment, which is the same reason `description` is popped below.
        npc_tags_map = {}
        # Phase A (2026-05-14): slug-keyed NPC schedule registry. Engine
        # consults this first in setup.getNpcLocation(); falls back to
        # canvas-derived presence when an NPC has no declared schedule.
        # Each entry is a list of {location, location_slug, weekdays, start_time, end_time, activity}.
        # `location` is a UUID string (runtime-comparable to $player.current_location +
        # locationCanvases keys); `location_slug` is the original TOML slug, kept for
        # debugging only (DevTools inspection). See Phase A bugfix entry in memory.
        npc_schedules_map = {}
        # Phase A bugfix (2026-05-14 PM): build a slug→UUID lookup BEFORE the
        # NPC walk so schedule entries can resolve location refs at emission
        # time. The TOML schedule field uses slugs (loc_kitchen) but every
        # runtime location identifier is a UUID. Without this, getNpcLocation
        # returns slugs that never `===` match runtime UUIDs and all three
        # Phase A gates silently no-op.
        loc_slug_to_uuid = {}
        for loc in self.locations:
            loc_props = getattr(loc, 'properties', None) or {}
            loc_slug = loc_props.get("slug") or f"loc_{loc.id}"
            loc_slug_to_uuid[loc_slug] = str(loc.id)
        try:
            from apps.npcs.models import NPC

            for n in self._all_npcs():
                flags_map = {}
                try:
                    for k in (getattr(n, 'flag_keys', []) or []):
                        flags_map[str(k)] = False
                except (TypeError, AttributeError) as e:
                    logger.warning("Error processing flag_keys for NPC '%s': %s", n.name, e)
                    flags_map = {}
                npc_uuid = str(n.id)
                ai_config = getattr(n, 'ai_behavior_config', None) or {}
                npc_map[npc_uuid] = {
                    "name": n.name,
                    "description": n.description or "",  # For customize screen intro (generation-time only)
                    "portrait": ai_config.get("portrait", ""),  # Portrait path from JSON (relative to video_folder)
                    "core_traits": (n.core_traits or {}),
                    "flags": flags_map,
                    "schedule": [],  # Derived at runtime from setup.help_data.locationCanvases
                    "relationship": ai_config.get("relationship", ""),
                    "role": ai_config.get("role", ""),  # F10 — the label under the name
                    "customizable": ai_config.get("customizable", False),
                    "relationship_options": ai_config.get("relationship_options", []),
                    "trait_decay": ai_config.get("trait_decay", {}),
                }
                # Track NPC portrait for file copying
                npc_portrait = ai_config.get("portrait", "")
                if npc_portrait:
                    self.used_assets['external_images'].add(npc_portrait)
                # Build slug→UUID mapping for condition resolution
                # Prefer slug from ai_behavior_config, fallback to lowercase name
                slug = ai_config.get("slug") or (n.name.lower().strip().replace(' ', '_') if n.name else "")
                if slug:
                    npc_slug_map[slug] = npc_uuid
                    # Also map short name (without npc_ prefix) for @-reference resolution
                    short_name = slug.replace("npc_", "", 1) if slug.startswith("npc_") else slug
                    if short_name and short_name != slug:
                        npc_slug_map[short_name] = npc_uuid
                # Track NPCs hidden from Guide Page, Stats Page, and sidebar NPC-traits widget.
                # The NPC still exists in $npcs at runtime so narrative UUID lookups keep working.
                if getattr(n, "hidden_from_ui", False):
                    hidden_npcs_map[npc_uuid] = True
                # E9/E10/E11: per-NPC arc_stages registry, slug-keyed.
                # Trait name is derived as `<slug>_stage` everywhere — never stored.
                arc_stages_for_npc = ai_config.get("arc_stages") or []
                if arc_stages_for_npc and slug:
                    npc_arc_stages_map[slug] = list(arc_stages_for_npc)
                # G: per-NPC cast-card tag line, slug-keyed. Same shape as above.
                tags_for_npc = ai_config.get("tags") or []
                if tags_for_npc and slug:
                    npc_tags_map[slug] = list(tags_for_npc)
                # Phase A (2026-05-14): per-NPC schedule registry, slug-keyed.
                # Consumed by setup.getNpcLocation() at runtime. Schedules with no
                # entries leave the NPC un-keyed → getNpcLocation falls back to
                # canvas-derived logic for that NPC.
                #
                # Phase A bugfix (2026-05-14 PM): translate location slug → UUID
                # at emission so runtime gates (Lane 2 / Lane 3 / portrait
                # filter) can compare with raw `===` against UUIDs. Carry the
                # original slug as location_slug for DevTools debuggability.
                schedules_for_npc = ai_config.get("schedules") or []
                if schedules_for_npc and slug:
                    resolved_entries = []
                    for sch in schedules_for_npc:
                        if not isinstance(sch, dict):
                            continue
                        sch_loc_slug = sch.get("location")
                        if not sch_loc_slug:
                            continue
                        sch_loc_uuid = loc_slug_to_uuid.get(sch_loc_slug)
                        if not sch_loc_uuid:
                            # Defensive: the template_import validator
                            # rejects unknown location refs in NPC schedules
                            # before reaching the generator. Skip rather
                            # than emit a slug that won't match runtime UUIDs.
                            logger.warning(
                                "NPC '%s' schedule entry references unknown "
                                "location slug '%s' — skipping. (Should have "
                                "been caught by template_import validate().)",
                                slug, sch_loc_slug,
                            )
                            continue
                        resolved_entries.append({
                            "location": sch_loc_uuid,
                            "location_slug": sch_loc_slug,
                            "weekdays": list(sch.get("weekdays") or []),
                            "start_time": sch.get("start_time", "00:00"),
                            "end_time": sch.get("end_time"),
                            "activity": sch.get("activity", ""),
                        })
                    if resolved_entries:
                        npc_schedules_map[slug] = resolved_entries
        except (AttributeError, TypeError) as e:
            logger.warning("Error loading NPC map: %s", e)
            npc_map = {}
            npc_slug_map = {}
            hidden_npcs_map = {}
            npc_arc_stages_map = {}
            npc_tags_map = {}
            npc_schedules_map = {}

        # Store as instance variables for use in _convert_blocks_to_game_html
        self.npc_map = npc_map
        self.npc_slug_map = npc_slug_map
        # E9/E10/E11 foundation: slug-keyed arc_stages registry. Empty when
        # no NPC has stage chains — runtime checks Object.keys(...).length > 0
        # before engaging stalled-detection / stage-gate / stage_label paths.
        self.npc_arc_stages_map = npc_arc_stages_map
        # G: slug-keyed cast-card tag registry. Empty when no NPC declares `tags`
        # — the cast card checks length before rendering the line.
        self.npc_tags_map = npc_tags_map
        # Phase A (2026-05-14): slug-keyed schedule registry. Empty when no
        # NPC has declared schedules — engine.getNpcLocation falls back to
        # canvas-derived presence for those NPCs.
        self.npc_schedules_map = npc_schedules_map

        # Build locations map for schedule display (location slug → name)
        # NPC schedules reference locations by TOML slug stored in properties["slug"]
        locations_map = {}
        for loc in self.locations:
            # Location slug is stored in properties during template import
            loc_props = getattr(loc, 'properties', None) or {}
            loc_slug = loc_props.get("slug") or f"loc_{loc.id}"
            locations_map[loc_slug] = {
                "name": loc.name,
                "id": str(loc.id),
                "clothing_rules": loc_props.get("clothing_rules", []),
                # Travel-friction (entry cost) + lock-as-prose (visible-but-blocked) data.
                # Both default empty → free, always-open move (today's behavior).
                "entry_costs": loc_props.get("entry_costs", {}),
                "entry_conditions": loc_props.get("entry_conditions", {}),
                "blocked_message": loc_props.get("blocked_message", ""),
            }

        # Build passage name → location slug reverse map (for clothing checks)
        passage_to_location = {}
        for loc in self.locations:
            loc_props = getattr(loc, 'properties', None) or {}
            loc_slug = loc_props.get("slug") or f"loc_{loc.id}"
            passage_name = self._location_passage_name(loc)
            passage_to_location[passage_name] = loc_slug
        passage_to_location_json = json.dumps(passage_to_location)

        # NPC schedules are derived at runtime from setup.help_data.locationCanvases
        # (see getNpcScheduleFromCanvases JS function) — no static schedule needed

        # Strip runtime-only fields from npc_map before serializing to game JSON
        # (relationship_options and customizable are used for passage generation, not runtime state)
        # `role` (F10) belongs here too: the label is baked into the passage HTML at BUILD
        # time and nothing reads it back at runtime, so shipping it in $npcs would put a
        # dead key in every save of every game — including the games that never set one.
        npc_map_for_json = {}
        npc_trait_decay_config = {}  # {npc_uuid: {trait: decay_per_day}}
        for uuid, data in npc_map.items():
            entry = dict(data)
            entry.pop("customizable", None)
            entry.pop("relationship_options", None)
            entry.pop("description", None)
            entry.pop("role", None)
            # Extract trait_decay config for setup (not runtime state)
            td = entry.pop("trait_decay", None)
            if td:
                npc_trait_decay_config[uuid] = td
            npc_map_for_json[uuid] = entry
        npc_map_json = json.dumps(npc_map_for_json)
        self.npc_trait_decay_config = npc_trait_decay_config
        npc_slug_map_json = json.dumps(npc_slug_map)
        hidden_npcs_json = json.dumps(hidden_npcs_map)

        # Build customizable NPCs list and redirect start_target if needed
        customizable_npcs = [
            (uuid, data) for uuid, data in npc_map.items()
            if data.get("customizable")
        ]
        has_player_customization = bool(self.player_customizable and self.player_customization_fields)
        if customizable_npcs or has_player_customization:
            start_target = "CustomizeCharacters"
        locations_map_json = json.dumps(locations_map)
        # Build flags init dict combining per-key defaults (false) with the
        # engine metadata keys. $flags is the canonical store — read by
        # triggerConditionsSatisfied, written by applyFlagEffect, displayed by
        # FlagsPage. Pre-2026-05-06 we initialized a separate $player.flags
        # object that drifted out of sync (only one legacy direct-write site
        # at the rent eviction passage ever updated it). $player.flags is
        # retired; per-passage migration runs on load to clean up old saves.
        flags_init_map = {str(k): False for k in player_flag_keys}
        flags_init_map["game_started"] = True
        flags_init_map["debug_mode"] = bool(self.debug)
        # Dev jumps: --dev builds flip this on so any dev-shortcut canvas (trigger
        # gated on dev_mode_enabled) is live and the sidebar <<devJumps>> list can
        # reach it. Never set in a shipped build → dev shortcuts stay inert there.
        if self.dev_mode:
            flags_init_map["dev_mode_enabled"] = True
        flags_init_json = json.dumps(flags_init_map)

        # Story arc data for narrative journal
        story_arc_json = self._build_story_arc_json()

        # Help data for Quest Page (per-NPC activities)
        help_data_json = self._build_help_data()

        # PRD 48 — Quests Engine V2 cards. Empty list for V1 games; V2 games
        # carry their [[quest_cards]] entries through template_import.py's
        # _serialize_quests_card into project.metadata["quests_cards"].
        # Always emitted as a JSON array on setup so the runtime can read it
        # without an existence check.
        quests_cards_json = json.dumps(
            (self.project.metadata or {}).get("quests_cards", [])
        )

        # Narrative person — labels the player's own dialog / thought-bubble blocks so
        # they agree with the prose. A third-person game left on the default renders
        # "You:" directly under a paragraph that says "she".
        self.narration_person = (self.project.metadata or {}).get(
            "narration_person", "second"
        )

        # Clothing system data
        clothing_settings = (self.project.metadata or {}).get("clothing_settings", {})
        self.clothing_enabled = clothing_settings.get("enabled", False)
        self.wardrobe_location_slug = clothing_settings.get("wardrobe_location", "")
        self.shop_location_slug = clothing_settings.get("shop_location", "")
        clothing_items = clothing_settings.get("items", [])
        clothing_requirements = clothing_settings.get("requirements", {})
        if self.clothing_enabled:
            # Prefix clothing image paths with video_path and track assets
            video_prefix = (self.video_path or "./videos").rstrip("/")
            for item in clothing_items:
                if item.get("image"):
                    self.used_assets['external_images'].add(item["image"])
                    item["image"] = f"{video_prefix}/{item['image']}"
            initial_wardrobe = {}
            initial_equipped = {
                "bra": None, "underwear": None, "top": None,
                "bottom": None, "dress": None, "legwear": None, "shoes": None,
            }
            for item in clothing_items:
                if item.get("initial", False):
                    initial_wardrobe[item["id"]] = {
                        "id": item["id"],
                        "name": item["name"],
                        "slot": item["slot"],
                        "image": item.get("image", ""),
                    }
                    initial_equipped[item["slot"]] = item["id"]
            clothing_data_json = json.dumps(clothing_items)
            clothing_requirements_json = json.dumps(clothing_requirements)

        # Rent system data
        rent_settings = (self.project.metadata or {}).get("rent_settings", {})
        self.rent_enabled = rent_settings.get("enabled", False)
        self.rent_amount = rent_settings.get("amount", 0)
        self.rent_due_day = rent_settings.get("due_day", "Monday")
        self.rent_collector_npc = rent_settings.get("collector_npc", "")
        self.rent_grace_periods = rent_settings.get("grace_periods", 1)
        self.rent_start_after_flag = rent_settings.get("start_after_flag", "")
        self.rent_text = rent_settings.get("text", {})
        self.rent_eviction_mode = rent_settings.get("eviction_mode", "game_end")
        self.rent_eviction_flag = rent_settings.get("eviction_flag", "rent_evicted")
        # The RentDay pages used to hardcode "$". Every other price in a game comes from
        # authored prose, so a game written in pounds had exactly one screen quoting
        # dollars — and it was the screen the whole economy hangs off. Default stays "$"
        # so no existing build moves.
        self.rent_currency_symbol = rent_settings.get("currency_symbol", "$") or "$"

        # Passes (recurring time-limited purchases)
        self.passes = (self.project.metadata or {}).get("passes", [])
        # Items (consumable inventory)
        self.items = (self.project.metadata or {}).get("items", [])
        # Day-rollover hook ([engine.daily_tick]) — fires inside advanceDay().
        # Always present as a dict with a flagEffects list (possibly empty)
        # so the generated JS loop has a stable target.
        _daily_tick_meta = (self.project.metadata or {}).get("daily_tick") or {}
        self.daily_tick = {
            "flagEffects": _daily_tick_meta.get("flagEffects", []) or [],
            # doc 40 — per-day trait deltas (RTS arousal daily auto-rise).
            "traitEffects": _daily_tick_meta.get("traitEffects", []) or [],
        }
        # doc 45 G4 — quest catalog ([[quests]]); read by the Quests app.
        self.quests = (self.project.metadata or {}).get("quests", []) or []
        # doc 45 G7 — optional corruption tier thresholds ([engine].corruption_tiers).
        self.corruption_tiers = (self.project.metadata or {}).get("corruption_tiers")
        # doc 45 G9 — economy: fast jobs + bank.
        self.fast_jobs_data = (self.project.metadata or {}).get("fast_jobs", []) or []
        self.bank_data = (self.project.metadata or {}).get("bank")
        # E4: Stage helpers ([[engine.stage_helpers]]) — named composite gates.
        # Loaded as a list; runtime builds an O(1) name → helper lookup map.
        self.stage_helpers = (self.project.metadata or {}).get("stage_helpers", []) or []
        # Pattern 2 (2026-05-01): label registries for setup.computeHintGoal.
        # Maps internal trait/flag names → player-facing labels.
        self.trait_labels = (self.project.metadata or {}).get("trait_labels", {}) or {}
        self.flag_labels = (self.project.metadata or {}).get("flag_labels", {}) or {}
        # Hidden-trait registry (2026-05-30): any [[traits.labels]] entry with
        # hidden=true names a core_trait that must NEVER render in a player-facing
        # trait dump (playerTraits/npcTraits widgets + Stats page), in dev AND
        # non-dev builds. Internal stage/pregnancy/awareness traits live in
        # core_traits (the engine reads them there) but leak through the
        # Object.keys() dump loops; this set drives a <<continue>> skip in each.
        # Name-keyed (not namespaced) — a hidden key is hidden for player + any NPC.
        self.hidden_trait_keys = [
            k for k, v in self.trait_labels.items()
            if isinstance(v, dict) and v.get("hidden")
        ]
        # Pattern 2: stage_setter_canvases — runtime index mapping
        # (npc_slug, stage_value) → canvas_id for branch-inside-shell transitions
        # (where the helper isn't the source of truth — the canvas's exit_block
        # writes the stage flag directly). Built by scanning canvases' choice
        # effects and exit_block.config.effects for `<npc>_stage = N` setters.
        self.stage_setter_canvases = self._build_stage_setter_canvases_index()
        # Pattern 2 v2.1 (2026-05-04): flag_setter_canvases — runtime index
        # mapping flag_key → canvas_id (first non-dev setter wins). Used by
        # setup.computeHintGoal's State B branch to surface 📍/🕒 for unmet
        # flag gates in stage helpers. See _build_flag_setter_canvases_index.
        self.flag_setter_canvases = self._build_flag_setter_canvases_index()
        # Sub-menu parent index (2026-05-09) — maps a triggerless sub-menu
        # canvas back to the menu canvas that routes to it via cross-canvas
        # `targetType="node"` choices. Used by _findFlagSetterCanvas to walk
        # back from a triggerless flag setter (e.g., scene_office_after_crack
        # which is reached only via scene_franks_office_setter's "Bend over
        # the page" item) to a parent canvas that IS in locationCanvases —
        # so State B's "Where" frame can surface 📍 location + 🕒 schedule
        # of the parent menu hub instead of returning null.
        # Format: {child_canvas_id: parent_canvas_id} (first parent wins).
        # See _build_sub_menu_parent_index.
        self.sub_menu_parents = self._build_sub_menu_parent_index()
        # Tips page — game-level mechanics surface. Empty dict = page + sidebar
        # button not emitted. Authored under [ui.tips_page] in TOML.
        self.tips_page = (self.project.metadata or {}).get("tips_page", {}) or {}
        # Cast page — the who-is-who surface. Empty dict = page + sidebar button
        # not emitted. Authored under [ui.cast_page]. Carries chrome only: the
        # roster is built at runtime from $npcs and setup.quests_cards.
        self.cast_page = (self.project.metadata or {}).get("cast_page", {}) or {}
        # Player cheat page — empty dict = page + sidebar button not emitted.
        # Authored under [ui.cheat_page]. One build ships everywhere; which rows are
        # live is decided at runtime by the codes the player has entered.
        self.cheat_page = (self.project.metadata or {}).get("cheat_page", {}) or {}
        # Theme (visual customization)
        raw_theme = (self.project.metadata or {}).get("theme", {})
        self.theme = self._resolve_theme(raw_theme)

        # Sidebar items (custom display elements configurable via TOML)
        self.sidebar_items = list(
            (self.project.metadata or {}).get("sidebar_items", []) or []
        )
        # E18 — auto-emit trait_bar sidebar items for counter traits referenced
        # by stage helpers. Closes the "I can't see my counter" UX gap (hints
        # like "×3 sessions" assume the player can track count). Skips if the
        # author already authored a sidebar item for the same trait_key.
        self._auto_emit_counter_sidebar_items()
        # E20 — auto-emit trait_decay_warning sidebar items for decaying traits
        # near the next stage gate. Renders an amber banner when a snapshot-vs-
        # current comparison shows decrease today. Snapshot lives in
        # State.variables.last_day_snapshot, populated in advanceDay().
        self._auto_emit_decay_warning_sidebar_items()
        sidebar_items_json = json.dumps(self.sidebar_items)

        # Player-portrait config (state-reactive sidebar image, opt-in). Images are
        # prefixed with video_path and tracked as assets for copying (like clothing at
        # ~1013); getPlayerPortrait() returns the ready path and the widget uses it directly.
        pp_settings = (self.project.metadata or {}).get("player_portrait", {})
        self.player_portrait_enabled = bool(pp_settings.get("enabled", False))
        player_portrait_json = "null"
        if self.player_portrait_enabled:
            pp_prefix = (self.video_path or "./videos").rstrip("/")
            pp_cfg = dict(pp_settings)
            for _pk in ("naked_image", "topless_image", "bottomless_image",
                        "underwear_image", "default_image"):
                _pv = pp_cfg.get(_pk, "")
                if _pv:
                    self.used_assets['external_images'].add(_pv)
                    pp_cfg[_pk] = f"{pp_prefix}/{_pv}"
            _pp_outfits = []
            for _po in (pp_settings.get("outfits") or []):
                _pimg = _po.get("image", "")
                if _pimg:
                    self.used_assets['external_images'].add(_pimg)
                    _pimg = f"{pp_prefix}/{_pimg}"
                _pp_outfits.append({"image": _pimg, "when": _po.get("when", {})})
            pp_cfg["outfits"] = _pp_outfits
            # Also track Preg-variant files (dressed images get the suffix inserted at
            # runtime by getPlayerPortrait). Only track ones that actually exist in the
            # media folder so a game without Preg art doesn't log spurious copy failures.
            if pp_settings.get("pregnancy_trait"):
                _suffix = pp_settings.get("pregnancy_suffix", "Preg") or "Preg"
                _dressed_raw = [pp_settings.get("default_image", "")] + [
                    _po.get("image", "") for _po in (pp_settings.get("outfits") or [])
                ]
                for _draw in _dressed_raw:
                    if not _draw:
                        continue
                    _dot = _draw.rfind(".")
                    _preg_raw = (_draw[:_dot] + _suffix + _draw[_dot:]) if _dot > -1 else (_draw + _suffix)
                    if _preg_raw in self.video_files:
                        self.used_assets['external_images'].add(_preg_raw)
            player_portrait_json = json.dumps(pp_cfg)

        # Phone system data
        phone_settings = (self.project.metadata or {}).get("phone_settings", {})
        self.phone_enabled = phone_settings.get("enabled", False)
        self.phone_purchase_flag = phone_settings.get("purchase_flag", "") or ""  # doc 45 G11
        phone_data_json = "null"
        if self.phone_enabled:
            phone_apps = phone_settings.get("apps", [])
            phone_conversations = phone_settings.get("conversations", [])
            video_prefix = (self.video_path or "./videos").rstrip("/")
            for app in phone_apps:
                if app.get("icon"):
                    actual_path, actual_ext = self._find_media_file(app["icon"])
                    if actual_path:
                        self.used_assets['external_images'].add(actual_path)
                        app["icon"] = actual_path
                        app["_icon_src"] = f"{video_prefix}/{actual_path}"
                    else:
                        self.missing_media.append({
                            'file': app["icon"],
                            'type': 'app_icon',
                            'description': f"Phone app icon for {app.get('label') or app.get('id', 'unknown')}",
                            'search_queries': [],
                            'canvas_id': 'phone',
                            'category': 'Social Media',
                        })
                        app["_icon_src"] = ""
                else:
                    app["_icon_src"] = ""
            phone_posts = phone_settings.get("posts", [])
            phone_profiles = phone_settings.get("profiles", [])
            # Validate and track post images and profile photos
            for post in phone_posts:
                if post.get("image"):
                    actual_path, actual_ext = self._find_media_file(post["image"])
                    if actual_path:
                        self.used_assets['external_images'].add(actual_path)
                        post["image"] = actual_path
                    else:
                        self.missing_media.append({
                            'file': post["image"],
                            'type': 'social_post_image',
                            'description': f"Social post image for {post.get('poster_name') or post.get('id', 'unknown')}",
                            'search_queries': post.get('search_queries', []),
                            'canvas_id': 'phone',
                            'category': 'Social Media',
                        })
            for prof in phone_profiles:
                resolved_photos = []
                for photo in (prof.get("photos") or []):
                    if not photo:
                        resolved_photos.append(photo)
                        continue
                    actual_path, actual_ext = self._find_media_file(photo)
                    if actual_path:
                        self.used_assets['external_images'].add(actual_path)
                        resolved_photos.append(actual_path)
                    else:
                        resolved_photos.append(photo)
                        self.missing_media.append({
                            'file': photo,
                            'type': 'dating_profile_photo',
                            'description': f"Dating profile photo for {prof.get('npc') or prof.get('id', 'unknown')}",
                            'search_queries': prof.get('search_queries', []),
                            'canvas_id': 'phone',
                            'category': 'Social Media',
                        })
                prof["photos"] = resolved_photos
            phone_daily_topics = phone_settings.get("daily_topics", [])
            # doc 45 G3 — resolve photo-action images like post images
            for dt in phone_daily_topics:
                if dt.get("image"):
                    actual_path, actual_ext = self._find_media_file(dt["image"])
                    if actual_path:
                        self.used_assets['external_images'].add(actual_path)
                        dt["image"] = actual_path
                    else:
                        self.missing_media.append({
                            'file': dt["image"],
                            'type': 'phone_chat_photo',
                            'description': f"Phone photo-action image for {dt.get('npc') or dt.get('id', 'unknown')}",
                            'search_queries': [],
                            'canvas_id': 'phone',
                            'category': 'Social Media',
                        })
            phone_gallery_items = phone_settings.get("gallery_items", [])
            # doc 45 G8 — resolve gallery images like post images
            for gitem in phone_gallery_items:
                if gitem.get("image"):
                    actual_path, actual_ext = self._find_media_file(gitem["image"])
                    if actual_path:
                        self.used_assets['external_images'].add(actual_path)
                        gitem["image"] = actual_path
                    else:
                        self.missing_media.append({
                            'file': gitem["image"],
                            'type': 'phone_gallery_image',
                            'description': f"Phone gallery image {gitem.get('id', 'unknown')}",
                            'search_queries': [],
                            'canvas_id': 'phone',
                            'category': 'Social Media',
                        })
            phone_data_json = json.dumps({
                "apps": phone_apps,
                "conversations": phone_conversations,
                "posts": phone_posts,
                "profiles": phone_profiles,
                "daily_topics": phone_daily_topics,
                "gallery_items": phone_gallery_items,
            })

        # Dev mode JS helpers moved to [script] tagged passage in _generate_time_system()
        # This ensures they're available on page refresh/save load, not just when Start is visited

        # NPC portrait path prefix (resolved at generation time, embedded in JS)
        npc_portrait_prefix = (getattr(self, 'video_path', '') or './media').rstrip('/') + '/'

        # ── The state skeleton, built ONCE as data ────────────────────────────
        # $player and $game_state are serialized into :: Start from these dicts
        # AND handed to setup.stateDefaults, so the save-migration backfill can
        # never fall behind what a fresh game starts with. They used to be two
        # hand-maintained string blocks and a three-key defaults dict, which is
        # why turning on the phone (or rent, passes, inventory, clothing) in a
        # new release left the whole sub-map undefined in every existing save.
        player_init = {
            "name": player_name,
            "portrait": player_portrait,
            "current_location": "",
            "core_traits": player_traits,
        }
        if self.clothing_enabled:
            player_init["wardrobe"] = initial_wardrobe
            player_init["equipped"] = initial_equipped
        if self.player_customizable and self.player_customization_fields:
            for cf in self.player_customization_fields:
                if cf["id"] == "name":
                    continue  # name is already in $player.name
                player_init[cf["id"]] = cf.get("default", "")
        player_init_json = json.dumps(player_init, indent=4)

        game_state_init = {
            "current_canvas": "",
            "visited_locations": [],
            "visited_nodes": [],
            "trigger_history": {},
            "activity_trigger_history": {},
            "visited_choices": {},
            "active_modifiers": {},
            "random_cooldowns": {},
            "stage_advancement_log": {},
            "media_cycle": {},
            "quests": {},
            "scheduled": [],
            "fast_jobs": {"xp": 0, "cooldowns": {}},
            "bank": {"balance": 0},
            "time_state": {
                "current_hour": time_settings["starting_hour"],
                "current_minute": 0,
                "current_day": time_settings["starting_day"],
                "current_week": time_settings["starting_week"],
                "day": 1,
            },
        }
        # Optional systems. Each one is the case the backfill exists for: a game
        # that ships without it and turns it on later.
        if self.rent_enabled:
            game_state_init["rent_state"] = {
                "last_paid_week": time_settings.get("starting_week", 1),
                "warnings": 0,
                "is_due": False,
            }
        if self.passes:
            game_state_init["passes"] = {}
        if self.items:
            game_state_init["inventory"] = {}
        if self.phone_enabled:
            game_state_init["phone"] = {
                "triggered_conversations": {},
                "read_conversations": {},
                "replies": {},
                "triggered_posts": {},
                "viewed_feed": False,
                "triggered_profiles": {},
                "liked_profiles": {},
                "passed_profiles": {},
                "matches": {},
            }
        # Schema signature stamped into every save via Config.saves.version: a
        # fingerprint of the trait/flag key surface and the corruption tiers, so a
        # build can tell whether a save was written against its own data shape.
        import hashlib as _hashlib
        _schema_sig_src = json.dumps(
            {
                "player_traits": sorted(player_traits.keys()),
                "npc_traits": {
                    u: sorted((e.get("core_traits") or {}).keys())
                    for u, e in npc_map_for_json.items()
                },
                "flags": sorted(flags_init_map.keys()),
                "tiers": self.project.metadata.get("corruption_tiers"),
            },
            sort_keys=True,
        )
        saves_version = int(_hashlib.sha1(_schema_sig_src.encode()).hexdigest()[:8], 16)
        # Stable save id — pin to the template slug (rename-safe), NOT the default
        # slugify(StoryTitle), which orphans saves when the game title changes.
        saves_id = (self.project.metadata.get("template", {}) or {}).get("slug") or str(
            self.project.id
        )
        saves_id_json = json.dumps(saves_id)

        # ── Release provenance, recorded INSIDE the save ──────────────────────
        # There is no other durable channel. setup.* is rebuilt from the CURRENT
        # build on every load, so by the time anything can ask "which release wrote
        # this save?" the old build's constants are already gone. Only $game_state
        # travels with the player.
        #
        # origin_* is written once by :: Start and never touched again — the backfill
        # fills only keys that are ABSENT, so it cannot overwrite them. last_* is
        # reassigned by the :passagestart handler whenever the running build differs.
        # Together they answer "started on X, now running Y", which is the pair a bug
        # report needs and neither field gives alone.
        build_version = str(
            (self.project.metadata or {}).get("version", "") or ""
        ).strip()
        build_version_json = json.dumps(build_version or None)
        game_state_init["origin_version"] = build_version or None
        game_state_init["origin_schema"] = saves_version
        game_state_init["last_version"] = build_version or None
        game_state_init["last_schema"] = saves_version
        game_state_init_json = json.dumps(game_state_init, indent=4)

        # ── Save-migration seam (fill-if-absent backfill for cross-release saves) ──
        # SugarCube never re-runs :: Start on load, so a returning player's save
        # (from an earlier release) is missing any $npcs / trait / flag / state
        # map a new release added. setup.stateDefaults carries the current
        # defaults — the SAME dicts Start serializes, so they can't drift — and
        # the :passagestart handler deep-merges MISSING keys only into loaded
        # state. See setup.backfillStateDefaults for the depth rules.
        #
        # ⚠️ origin_* is the ONE deliberate divergence between Start and the
        # defaults, and it has to be one. A save written before the stamp existed
        # carries no origin_*; filling it from the current build would make that
        # save claim to have STARTED here, which is the opposite of the truth.
        # Absent means unknown, and unknown is the honest answer to record.
        game_state_defaults = dict(game_state_init)
        game_state_defaults["origin_version"] = None
        game_state_defaults["origin_schema"] = None
        state_defaults = {
            "player": player_init,
            "npcs": npc_map_for_json,
            "flags": flags_init_map,
            "game_state": game_state_defaults,
        }
        state_defaults_json = json.dumps(state_defaults)

        # Pre-build conditional wardrobe JS blocks (regular strings with literal braces)
        # These get interpolated into the f-string below via {wardrobe_js_block} and {wardrobe_handlers_block}
        wardrobe_js_block = ""
        wardrobe_handlers_block = ""
        if self.clothing_enabled:
            wardrobe_js_block = """
setup.addToWardrobe = function(itemId) {
    var sv = State.variables;
    if (!sv.player || !sv.player.wardrobe) return;
    var item = null;
    var cdata = setup.clothing_data || [];
    for (var i = 0; i < cdata.length; i++) {
        if (cdata[i].id === itemId) { item = cdata[i]; break; }
    }
    if (!item) return;
    if (sv.player.wardrobe[itemId]) return;
    sv.player.wardrobe[itemId] = item;
    setup.pendingEffects = setup.pendingEffects || [];
    setup.pendingEffects.push({ "type": "wardrobe", "name": item.name });
};

setup.equipItem = function(itemId) {
    var sv = State.variables;
    if (!sv.player || !sv.player.wardrobe || !sv.player.equipped) return false;
    var item = sv.player.wardrobe[itemId];
    if (!item) return false;
    var slot = item.slot;
    if (item.conditions && item.conditions.items && item.conditions.items.length > 0) {
        if (!setup.triggerConditionsSatisfied(item.conditions)) return false;
    }
    if (slot === 'dress') {
        sv.player.equipped['top'] = null;
        sv.player.equipped['bottom'] = null;
    }
    if (slot === 'top' || slot === 'bottom') {
        sv.player.equipped['dress'] = null;
    }
    sv.player.equipped[slot] = itemId;
    return true;
};

setup.unequipSlot = function(slotName) {
    var sv = State.variables;
    if (!sv.player || !sv.player.equipped) return;
    sv.player.equipped[slotName] = null;
};

setup.getWardrobeItemsForSlot = function(slotName) {
    var sv = State.variables;
    if (!sv.player || !sv.player.wardrobe) return [];
    var items = [];
    var wd = sv.player.wardrobe;
    for (var id in wd) {
        if (wd.hasOwnProperty(id) && wd[id] && wd[id].slot === slotName) {
            items.push(wd[id]);
        }
    }
    return items;
};

// Worn-stat aggregates (MAX over equipped slots). Read stats from
// setup.clothing_data BY EQUIPPED ID — the equipped/wardrobe records only
// carry id/name/slot/image, so clothing_data is the single source of truth.
// These ROUTE content; they never touch the global player.corruption trait.
setup.getWornStatMax = function(field) {
    var sv = State.variables;
    if (!setup.clothing_enabled) return 0;
    var eq = (sv.player && sv.player.equipped) || {};
    var cdata = setup.clothing_data || [];
    var best = 0;
    for (var slot in eq) {
        if (!eq.hasOwnProperty(slot)) continue;
        var id = eq[slot];
        if (!id) continue;
        for (var i = 0; i < cdata.length; i++) {
            if (cdata[i].id === id) {
                var v = cdata[i][field] || 0;
                if (v > best) best = v;
                break;
            }
        }
    }
    return best;
};
setup.getWornBeauty = function() { return setup.getWornStatMax('beauty'); };
setup.getWornCorruption = function() { return setup.getWornStatMax('corruption'); };

// ─────────────────────────────────────────────────────────────────────────────
// EXPOSURE — how much of her is showing. 0 covered / 1 underwear-level / 2 bare.
//
// ⚠️ THIS IS THE ONE AGGREGATE THAT READS EMPTY SLOTS. getWornStatMax above SKIPS a slot
// with nothing in it and starts at 0, so worn_beauty and worn_corruption return the SAME
// VALUE for a naked player and one in a plain bra and briefs.
//
// ⚠️ CORRECTION TO THIS FEATURE'S OWN FIRST CLAIM: nakedness was NOT unaskable before
// this. The `clothing_slot` predicate (empty/filled, evaluated a few hundred lines below)
// has always been able to ask whether one slot is filled, and `engine.md` §17 documents it.
// What did not exist is a DERIVED value that folds the regions together into one 0/1/2
// scale. That is worth having because it is what the field actually gates on:
// degrees-of-lewdity tests its derived `$exposed` 961 times against 54 reads of any
// per-slot `.exposed`. The scalar is the thing the world asks; per-slot is the exception.
//
// The model is the field's. degrees-of-lewdity's `$exposed` is the most-read variable in
// that game — 654 tests of `gte 1`, 307 of `gte 2` — against 54 reads of any per-slot
// `.exposed`, so the 0/1/2 scalar is what the world actually asks and the per-slot detail
// is not worth building. 71% of its 407 world gates are about how much skin is showing,
// and they sit in ordinary places: streets, an arcade, a canteen, a park.
//
// Two ways to reach a level. A garment may DECLARE `exposure` (a mesh top is 1 while
// worn), and an empty core region IS exposure regardless of what any garment says:
//   upper — bare unless `top` or `dress` is filled; underwear-level if only `bra`
//   lower — bare unless `bottom` or `dress` is filled; underwear-level if only `underwear`
// The result is the MAX of the two regions and every declared garment exposure, so the
// most-revealed part of her is what the world reacts to.
setup.getWornExposure = function() {
    if (!setup.clothing_enabled) return 0;
    var sv = State.variables;
    var eq = (sv.player && sv.player.equipped) || {};
    var cdata = setup.clothing_data || [];
    var filled = function(slot) { return !!eq[slot]; };

    var dress = filled('dress');
    // upper region
    var upper = 0;
    if (!dress && !filled('top')) upper = filled('bra') ? 1 : 2;
    // lower region
    var lower = 0;
    if (!dress && !filled('bottom')) lower = filled('underwear') ? 1 : 2;

    var best = upper > lower ? upper : lower;
    // a garment can declare its own exposure while worn — a mesh top covers the slot
    // but does not cover HER, so the slot being filled is not the end of the question
    for (var slot in eq) {
        if (!eq.hasOwnProperty(slot)) continue;
        var id = eq[slot];
        if (!id) continue;
        for (var i = 0; i < cdata.length; i++) {
            if (cdata[i].id === id) {
                var v = cdata[i].exposure || 0;
                if (v > best) best = v;
                break;
            }
        }
    }
    return best;
};

// Doc 72 / Doc 71 R2 — Outfit-category aggregator. Returns array of unique
// non-empty `type` strings across all currently-equipped items. Used by the
// `worn_type` predicate. Returns array (not Set) for SugarCube serialization
// compatibility — callers use indexOf to test membership.
setup.getWornTypes = function() {
    if (!setup.clothing_enabled) return [];
    var sv = State.variables;
    var eq = (sv.player && sv.player.equipped) || {};
    var cdata = setup.clothing_data || [];
    var types = [];
    for (var slot in eq) {
        if (!eq.hasOwnProperty(slot)) continue;
        var id = eq[slot];
        if (!id) continue;
        for (var i = 0; i < cdata.length; i++) {
            if (cdata[i].id === id) {
                var t = cdata[i].type || '';
                if (t && types.indexOf(t) === -1) types.push(t);
                break;
            }
        }
    }
    return types;
};

// State-reactive player portrait (opt-in). getUndressLevel() derives the undress
// state from equipped slots (null when clothing is off so the resolver skips the
// undress branch). getPlayerPortrait() resolves ONE ready-prefixed image path:
// undress-override -> outfit rule (dominant-slot type + corruption LEVEL/flag) ->
// Preg suffix (dressed images only). Returns '' when nothing resolves.
setup.getUndressLevel = function() {
    if (!setup.clothing_enabled) return null;
    var eq = ((State.variables.player || {}).equipped) || {};
    // An area is "bare" only when NOTHING covers it — including the underwear layer.
    // Top is covered by a top / dress / bra; bottom by a bottom / dress / underwear(briefs).
    var topCovered    = !!(eq.top || eq.dress || eq.bra);
    var bottomCovered = !!(eq.bottom || eq.dress || eq.underwear);
    var hasOuter      = !!(eq.top || eq.bottom || eq.dress);
    if (!topCovered && !bottomCovered) return 'naked';       // nothing anywhere
    if (!topCovered)    return 'topless';                    // breasts bare (not even a bra), bottom covered
    if (!bottomCovered) return 'bottomless';                 // crotch bare (not even briefs), top covered
    if (!hasOuter)      return 'underwear';                  // both covered by ONLY bra/briefs, no outer garment
    return 'dressed';                                        // an outer garment covers her
};

setup.getPlayerPortrait = function() {
    var cfg = setup.player_portrait;
    if (!setup.player_portrait_enabled || !cfg) return '';
    var sv = State.variables;
    var img = '';
    var fromUndress = false;
    // 1. undress override (only when clothing enabled; getUndressLevel is null otherwise)
    var u = setup.getUndressLevel();
    if (u === 'naked' && cfg.naked_image) { img = cfg.naked_image; fromUndress = true; }
    else if (u === 'underwear' && cfg.underwear_image) { img = cfg.underwear_image; fromUndress = true; }
    else if (u === 'topless' && cfg.topless_image) { img = cfg.topless_image; fromUndress = true; }
    else if (u === 'bottomless' && cfg.bottomless_image) { img = cfg.bottomless_image; fromUndress = true; }
    // 2. dressed / clothing-off -> outfit rules, dominant-slot keyed (dress || top || bottom)
    if (!img) {
        var domType = '';
        if (setup.clothing_enabled) {
            var eq = ((sv.player || {}).equipped) || {};
            var domId = eq.dress || eq.top || eq.bottom;
            if (domId) {
                var cdata = setup.clothing_data || [];
                for (var i = 0; i < cdata.length; i++) {
                    if (cdata[i].id === domId) { domType = cdata[i].type || ''; break; }
                }
            }
        }
        var lvl = setup.getCorruptionLevel();
        var flags = sv.flags || {};
        var outfits = cfg.outfits || [];
        for (var j = 0; j < outfits.length; j++) {
            var w = outfits[j].when || {};
            var ok = true;
            if (w.worn_type && w.worn_type !== domType) ok = false;
            if (ok && w.corruption) {
                var op = w.corruption.operator || 'gte';
                var val = w.corruption.value || 0;
                if (op === 'gte') ok = (lvl >= val);
                else if (op === 'lt') ok = (lvl < val);
                else if (op === 'lte') ok = (lvl <= val);
                else if (op === 'gt') ok = (lvl > val);
                else if (op === 'eq') ok = (lvl === val);
            }
            if (ok && w.flag && !flags[w.flag]) ok = false;
            if (ok) { img = outfits[j].image; break; }
        }
        if (!img) img = cfg.default_image || '';
    }
    // 3. pregnancy suffix — dressed images only (undress overrides skip it)
    if (img && !fromUndress && cfg.pregnancy_trait) {
        var preg = ((sv.player || {}).core_traits || {})[cfg.pregnancy_trait];
        if (preg) {
            var dot = img.lastIndexOf('.');
            if (dot > -1) img = img.slice(0, dot) + (cfg.pregnancy_suffix || 'Preg') + img.slice(dot);
        }
    }
    return img || '';
};

setup.isSlotDisabled = function(slotName) {
    var sv = State.variables;
    if (!sv.player || !sv.player.equipped) return false;
    var eq = sv.player.equipped;
    if ((slotName === 'top' || slotName === 'bottom') && eq['dress']) return true;
    return false;
};

setup.renderWardrobePage = function() {
    var sv = State.variables;
    var eq = (sv.player && sv.player.equipped) || {};
    var slots = ['bra', 'underwear', 'top', 'bottom', 'dress', 'legwear', 'shoes'];
    var slotLabels = {
        'bra': 'Bra', 'underwear': 'Underwear', 'top': 'Top',
        'bottom': 'Bottom', 'dress': 'Dress', 'legwear': 'Legwear', 'shoes': 'Shoes'
    };

    var html = '<div class="wardrobe-page">';
    html += '<table class="wardrobe-table">';

    for (var s = 0; s < slots.length; s++) {
        var slot = slots[s];
        var label = slotLabels[slot];
        var disabled = setup.isSlotDisabled(slot);
        var items = setup.getWardrobeItemsForSlot(slot);
        var currentlyEquipped = eq[slot] || null;

        html += '<tr class="wardrobe-row' + (disabled ? ' wardrobe-row-disabled' : '') + '">';
        html += '<td class="wardrobe-slot-label">' + label + '</td>';
        html += '<td class="wardrobe-slot-items">';

        if (disabled) {
            if (slot === 'dress') {
                html += '<span class="wardrobe-disabled-hint">Remove top/bottom first</span>';
            } else {
                html += '<span class="wardrobe-disabled-hint">Remove dress first</span>';
            }
        } else if (items.length === 0) {
            html += '<span class="wardrobe-empty-hint">No items</span>';
        } else {
            for (var i = 0; i < items.length; i++) {
                var it = items[i];
                var isEquipped = (currentlyEquipped === it.id);
                var condMet = true;
                if (it.conditions && it.conditions.items && it.conditions.items.length > 0) {
                    condMet = setup.triggerConditionsSatisfied(it.conditions);
                }
                var cls = 'wardrobe-item';
                if (isEquipped) cls += ' wardrobe-item-equipped';
                if (!condMet) cls += ' wardrobe-item-locked';
                var titleText = it.name;
                if (!condMet) titleText += ' (locked)';
                if (it.image) {
                    html += '<div class="' + cls + '" data-item-id="' + it.id + '" title="' + titleText + '">';
                    html += '<img src="' + it.image + '" alt="' + it.name + '" class="wardrobe-item-img" />';
                    if (isEquipped) html += '<span class="wardrobe-badge-equipped">&#10003;</span>';
                    if (!condMet) html += '<span class="wardrobe-badge-locked">&#128274;</span>';
                    html += '</div>';
                } else {
                    html += '<div class="' + cls + '" data-item-id="' + it.id + '" title="' + titleText + '">';
                    html += '<span class="wardrobe-item-text">' + it.name + '</span>';
                    if (isEquipped) html += '<span class="wardrobe-badge-equipped">&#10003;</span>';
                    if (!condMet) html += '<span class="wardrobe-badge-locked">&#128274;</span>';
                    html += '</div>';
                }
            }
        }

        if (!disabled && currentlyEquipped && setup.canRemoveSlot(slot)) {
            html += '<button class="wardrobe-unequip-btn" data-slot="' + slot + '" title="Remove">&times;</button>';
        }

        html += '</td>';
        html += '</tr>';
    }

    html += '</table>';
    html += '</div>';
    return html;
};

setup.canRemoveSlot = function(slotName) {
    var req = setup.clothingRequirements || {};
    var sv = State.variables;
    var flags = sv.flags || {};

    // Always-required slots (global safety net)
    var always = req.always_required || [];
    if (always.indexOf(slotName) !== -1) return false;

    // All other slots can be removed freely
    // Location-based clothing checks handle enforcement on navigation
    return true;
};

setup.validateClothing = function() {
    var sv = State.variables;
    var eq = (sv.player && sv.player.equipped) || {};
    var flags = sv.flags || {};
    var req = setup.clothingRequirements || {};
    var issues = [];

    // Body coverage: must have (top AND bottom) OR dress
    if (req.body_coverage) {
        if (!eq['dress'] && (!eq['top'] || !eq['bottom'])) {
            issues.push("Emma needs to be wearing a top and bottom, or a dress.");
        }
    }

    // Always required slots
    var always = req.always_required || [];
    for (var i = 0; i < always.length; i++) {
        var s = always[i];
        if (!eq[s]) {
            issues.push("Emma needs to put on " + s + ".");
        }
    }

    // Conditional slots — required until flag is set
    var cond = req.conditional || {};
    for (var slot in cond) {
        if (cond.hasOwnProperty(slot) && !eq[slot] && !flags[cond[slot].until_flag]) {
            issues.push(cond[slot].message || "Emma needs " + slot + ".");
        }
    }

    return issues;
};

// Check if player's clothing meets a location's requirements
// Returns null if OK, or a blocking message string if not
setup.checkLocationClothing = function(passageName) {
    if (!setup.clothing_enabled) return null;
    var locSlug = (setup.passage_to_location || {})[passageName];
    if (!locSlug) return null;

    var locData = (setup.locations || {})[locSlug];
    if (!locData || !locData.clothing_rules || locData.clothing_rules.length === 0) {
        return null;
    }

    var eq = (State.variables.player && State.variables.player.equipped) || {};
    var rules = locData.clothing_rules;

    // Find first rule whose conditions are satisfied
    var activeRule = null;
    for (var i = 0; i < rules.length; i++) {
        var rule = rules[i];
        if (!rule.conditions || !rule.conditions.items || rule.conditions.items.length === 0) {
            activeRule = rule;
            break;
        }
        if (setup.triggerConditionsSatisfied(rule.conditions)) {
            activeRule = rule;
            break;
        }
    }

    if (!activeRule) return null;

    var required = activeRule.slots_required || [];
    var missing = [];
    for (var j = 0; j < required.length; j++) {
        var slot = required[j];
        if ((slot === 'top' || slot === 'bottom') && eq['dress']) continue;
        if (!eq[slot]) missing.push(slot);
    }

    if (missing.length === 0) return null;

    return activeRule.message || "You need to put on more clothes before going there.";
};
"""
            wardrobe_handlers_block = """
// Wardrobe page event handlers
jQuery(document).on('click', '.wardrobe-item:not(.wardrobe-item-locked)', function(e) {
    e.preventDefault();
    var itemId = jQuery(this).data('item-id');
    if (itemId) {
        setup.equipItem(String(itemId));
        Engine.play("WardrobePage");
    }
});

jQuery(document).on('click', '.wardrobe-unequip-btn', function(e) {
    e.preventDefault();
    e.stopPropagation();
    var slot = jQuery(this).data('slot');
    if (slot) {
        setup.unequipSlot(String(slot));
        Engine.play("WardrobePage");
    }
});
"""

        # Shop system JS
        shop_js_block = ""
        shop_handlers_block = ""
        if self.clothing_enabled and self.shop_location_slug:
            shop_js_block = """
setup.getCorruptionThreshold = function(item) {
    if (!item.conditions || !item.conditions.items) return 0;
    for (var i = 0; i < item.conditions.items.length; i++) {
        var cond = item.conditions.items[i];
        if (cond.type === 'trait' && cond.trait_key === 'corruption' && cond.operator === 'gte') {
            return cond.value || 0;
        }
    }
    return 0;
};

// Human-readable summary of the conditions on an item that are NOT currently met.
// Generic over any trait, using the same operator vocabulary as
// triggerConditionsSatisfied so the message can never disagree with the gate.
// Returns "" if nothing fails (or only un-describable items fail).
setup.describeUnmetConditions = function(conditions) {
    if (!conditions || !conditions.items) return "";
    var sv = State.variables || {};
    var traits = (sv.player && sv.player.core_traits) || {};
    var flags = sv.flags || {};
    var parts = [];
    function cap(s) { s = String(s == null ? "" : s); return s.charAt(0).toUpperCase() + s.slice(1); }
    function num(v) { var n = Number(v); return isNaN(n) ? null : n; }
    for (var i = 0; i < conditions.items.length; i++) {
        var it = conditions.items[i];
        if (!it || typeof it !== 'object') continue;
        if (it.type === 'trait') {
            var key = it.trait_key;
            var op = it.operator;
            var want = it.value;
            var cur = (it.subject === 'npc') ? null : num(traits[key]);
            if (cur !== null) {
                var sat = false;
                if (op === 'gte') sat = cur >= want;
                else if (op === 'gt') sat = cur > want;
                else if (op === 'lte') sat = cur <= want;
                else if (op === 'lt') sat = cur < want;
                else if (op === 'eq') sat = cur === want;
                else if (op === 'ne') sat = cur !== want;
                if (sat) continue;
            }
            var label = cap(key);
            var phrase;
            if (op === 'gte') phrase = label + ' ' + want + '+';
            else if (op === 'gt') phrase = label + ' above ' + want;
            else if (op === 'lte') phrase = label + ' ' + want + ' or lower';
            else if (op === 'lt') phrase = label + ' under ' + want;
            else if (op === 'eq') phrase = label + ' exactly ' + want;
            else if (op === 'ne') phrase = label + ' not ' + want;
            else phrase = label + ' ' + op + ' ' + want;
            if (cur !== null) phrase += ' (you have ' + cur + ')';
            parts.push(phrase);
        } else if (it.type === 'flag') {
            var fkey = String(it.flag_key || '');
            var fop = it.operator;
            var v = flags[fkey];
            var fsat = false;
            if (fop === 'is_true') fsat = (v === true);
            else if (fop === 'is_false') fsat = (v === false || v === undefined);
            else if (fop === 'exists') fsat = Object.prototype.hasOwnProperty.call(flags, fkey);
            if (fsat) continue;
            var disp = cap(fkey.replace(/_/g, ' '));
            parts.push(fop === 'is_false' ? ('Requires: not ' + disp) : ('Requires: ' + disp));
        }
    }
    return parts.join(', ');
};

setup.buyItem = function(itemId) {
    var sv = State.variables;
    if (!sv.player || !sv.player.wardrobe) return false;
    if (sv.player.wardrobe[itemId]) return false;

    var item = null;
    var cdata = setup.clothing_data || [];
    for (var i = 0; i < cdata.length; i++) {
        if (cdata[i].id === itemId) { item = cdata[i]; break; }
    }
    if (!item) return false;

    var price = item.price || 0;
    var money = (sv.player.core_traits && sv.player.core_traits.money) || 0;
    if (money < price) return false;

    if (item.conditions && item.conditions.items && item.conditions.items.length > 0) {
        if (!setup.triggerConditionsSatisfied(item.conditions)) {
            var why = setup.describeUnmetConditions(item.conditions);
            setup.queueGatedNotification(why ? ("Not yet — needs " + why) : "Not available yet.");
            return false;
        }
    }

    sv.player.core_traits.money -= price;
    setup.addToWardrobe(itemId);
    return true;
};

setup.renderShopPage = function() {
    var sv = State.variables;
    var cdata = setup.clothing_data || [];
    var wardrobe = (sv.player && sv.player.wardrobe) || {};
    var money = (sv.player && sv.player.core_traits && sv.player.core_traits.money) || 0;
    var corruption = (sv.player && sv.player.core_traits && sv.player.core_traits.corruption) || 0;

    var shopItems = [];
    for (var i = 0; i < cdata.length; i++) {
        if (!cdata[i].initial && (cdata[i].price || 0) > 0) {
            shopItems.push(cdata[i]);
        }
    }

    var tiers = [
        { name: 'Basic', threshold: 0, items: [] },
        { name: 'Cute', threshold: 45, items: [] },
        { name: 'Bold', threshold: 85, items: [] },
        { name: 'Daring', threshold: 135, items: [] }
    ];

    for (var i = 0; i < shopItems.length; i++) {
        var item = shopItems[i];
        var threshold = setup.getCorruptionThreshold(item);
        var placed = false;
        for (var t = tiers.length - 1; t >= 0; t--) {
            if (threshold >= tiers[t].threshold) {
                tiers[t].items.push(item);
                placed = true;
                break;
            }
        }
        if (!placed) tiers[0].items.push(item);
    }

    var slotLabels = {
        'bra': 'Bra', 'underwear': 'Underwear', 'top': 'Top',
        'bottom': 'Bottom', 'dress': 'Dress', 'legwear': 'Legwear', 'shoes': 'Shoes'
    };

    var html = '<div class="shop-page">';
    html += '<div class="shop-money">Your money: <strong>$' + money + '</strong></div>';

    for (var t = 0; t < tiers.length; t++) {
        var tier = tiers[t];
        if (tier.items.length === 0) continue;

        var tierLocked = corruption < tier.threshold;

        html += '<div class="shop-tier' + (tierLocked ? ' shop-tier-locked' : '') + '">';
        html += '<h3 class="shop-tier-header">' + tier.name;
        if (tier.threshold > 0) {
            html += ' <span class="shop-tier-req">(Corruption ' + tier.threshold + '+)</span>';
        }
        html += '</h3>';

        html += '<div class="shop-items">';
        var slotOrder = ['bra', 'underwear', 'top', 'bottom', 'dress', 'legwear', 'shoes'];
        var slotGroups = {};
        for (var i = 0; i < tier.items.length; i++) {
            var sl = tier.items[i].slot;
            if (!slotGroups[sl]) slotGroups[sl] = [];
            slotGroups[sl].push(tier.items[i]);
        }
        for (var si = 0; si < slotOrder.length; si++) {
            var slotKey = slotOrder[si];
            if (!slotGroups[slotKey]) continue;
            var grpItems = slotGroups[slotKey];
            var slotLabel = slotLabels[slotKey] || slotKey;
            html += '<div class="shop-slot-group">';
            html += '<div class="shop-slot-label">' + slotLabel + '</div>';
            html += '<div class="shop-slot-items">';
            for (var gi = 0; gi < grpItems.length; gi++) {
                var item = grpItems[gi];
                var owned = !!wardrobe[item.id];
                var canAfford = money >= (item.price || 0);

                var cls = 'shop-item';
                if (owned) cls += ' shop-item-owned';
                else if (tierLocked) cls += ' shop-item-unaffordable';
                else if (!canAfford) cls += ' shop-item-unaffordable';

                html += '<div class="' + cls + '">';
                html += '<div class="shop-item-thumb">';
                if (item.image) {
                    html += '<img src="' + item.image + '" alt="' + item.name + '" class="shop-item-thumb-img" />';
                } else {
                    html += '<span class="shop-item-thumb-text">' + item.name + '</span>';
                }
                html += '</div>';
                html += '<div class="shop-item-info">';
                html += '<span class="shop-item-name">' + item.name + '</span>';
                html += '</div>';
                html += '<div class="shop-item-action">';

                if (owned) {
                    html += '<span class="shop-item-owned-badge">&#10003; Owned</span>';
                } else if (tierLocked) {
                    html += '<span class="shop-item-price">$' + item.price + '</span>';
                    html += '<span class="shop-item-cant-afford">&#128274; Corruption ' + tier.threshold + '+</span>';
                } else if (!canAfford) {
                    html += '<span class="shop-item-price">$' + item.price + '</span>';
                    html += '<span class="shop-item-cant-afford">Can\\\'t afford</span>';
                } else {
                    html += '<span class="shop-item-price">$' + item.price + '</span>';
                    html += '<button class="shop-buy-btn" data-item-id="' + item.id + '">Buy</button>';
                }

                html += '</div>';
                html += '</div>';
            }
            html += '</div>';
            html += '</div>';
        }
        html += '</div>';
        html += '</div>';
    }

    html += '</div>';
    return html;
};
"""
            shop_handlers_block = """
// Shop page event handlers
jQuery(document).on('click', '.shop-buy-btn', function(e) {
    e.preventDefault();
    var itemId = jQuery(this).data('item-id');
    if (itemId) {
        setup.buyItem(String(itemId));
        setup.showEffectNotification();
        Engine.play("ShopPage");
    }
});
"""

        # Phone system JS blocks
        phone_js_block = ""
        phone_handlers_block = ""
        if self.phone_enabled:
            video_path_js = (self.video_path or "./videos").rstrip("/")
            phone_js_block = f"""
// ========== PHONE SYSTEM ==========
// doc 45 G1 — phone delivery toast (body-append, auto-dismiss; mirrors showEffectNotification)
setup._notifyPhoneDelivery = function(messages) {{
    if (!messages || !messages.length) return;
    var safe = messages.map(function(m) {{ var d = document.createElement('div'); d.textContent = m; return d.innerHTML; }});
    jQuery('body').append('<div class="effect-toast phone-notify">' + safe.join('<br>') + '</div>');
    setTimeout(function() {{ jQuery('.phone-notify').remove(); }}, 3000);
}};
setup.checkPhoneConversations = function() {{
    if (!setup.phone_enabled || !setup.phone_data) return;
    var sv = State.variables;
    if (!sv.game_state || !sv.game_state.phone) return;
    var ps = sv.game_state.phone;
    // doc 45 G1 — baseline the first scan (no toasts for already-satisfied items),
    // then "ding" on each new arrival on subsequent passage renders.
    var _firstScan = !ps._phone_scanned;
    ps._phone_scanned = true;
    var _phoneToasts = [];
    var convs = setup.phone_data.conversations || [];
    for (var i = 0; i < convs.length; i++) {{
        var conv = convs[i];
        if (ps.triggered_conversations[conv.id]) continue;
        var trigCond = conv.trigger ? conv.trigger.conditions : null;
        if (trigCond && !setup.triggerConditionsSatisfied(trigCond)) continue;
        var ts = sv.game_state.time_state || {{}};
        ps.triggered_conversations[conv.id] = {{
            triggered_day: ts.day || 1,
            triggered_hour: ts.current_hour || 0,
            conv_index: i
        }};
        if (!_firstScan) _phoneToasts.push(setup.resolveAtRefs(conv.notify) || "📱 New message");
    }}
    // Check posts
    var posts = setup.phone_data.posts || [];
    for (var i = 0; i < posts.length; i++) {{
        var post = posts[i];
        if (ps.triggered_posts[post.id]) continue;
        var trigCond = post.trigger ? post.trigger.conditions : null;
        if (trigCond && !setup.triggerConditionsSatisfied(trigCond)) continue;
        var ts = sv.game_state.time_state || {{}};
        ps.triggered_posts[post.id] = {{ triggered_day: ts.day || 1, triggered_hour: ts.current_hour || 0 }};
        if (!_firstScan) _phoneToasts.push(setup.resolveAtRefs(post.notify) || "📱 New post");
    }}
    // Check profiles
    var profiles = setup.phone_data.profiles || [];
    for (var i = 0; i < profiles.length; i++) {{
        var prof = profiles[i];
        if (ps.triggered_profiles[prof.id]) continue;
        var trigCond = prof.trigger ? prof.trigger.conditions : null;
        if (trigCond && !setup.triggerConditionsSatisfied(trigCond)) continue;
        ps.triggered_profiles[prof.id] = true;
    }}
    if (_phoneToasts.length) setup._notifyPhoneDelivery(_phoneToasts);
}};

setup.getPhoneUnreadCount = function() {{
    var ps = ((State.variables || {{}}).game_state || {{}}).phone;
    if (!ps) return 0;
    var count = 0;
    // Unread conversations
    var triggered = ps.triggered_conversations || {{}};
    var read = ps.read_conversations || {{}};
    var keys = Object.keys(triggered);
    for (var i = 0; i < keys.length; i++) {{
        if (!read[keys[i]]) count++;
    }}
    // Unviewed posts
    if (!ps.viewed_feed && Object.keys(ps.triggered_posts || {{}}).length > 0) count++;
    return count;
}};

setup.getPhoneThreads = function(appId) {{
    var sv = State.variables;
    var ps = (sv.game_state || {{}}).phone;
    if (!ps || !setup.phone_data) return [];
    var convs = setup.phone_data.conversations || [];
    var triggered = ps.triggered_conversations || {{}};
    var read = ps.read_conversations || {{}};
    var npcs = sv.npcs || {{}};
    var byNpc = {{}};
    for (var i = 0; i < convs.length; i++) {{
        var conv = convs[i];
        if (conv.app !== appId || !triggered[conv.id]) continue;
        var npcSlug = conv.npc || "";
        if (!byNpc[npcSlug]) {{
            var resolvedId = setup.resolveNpcId(npcSlug);
            var npcData = npcs[resolvedId] || {{}};
            byNpc[npcSlug] = {{
                npcSlug: npcSlug,
                npcName: npcData.name || npcSlug.replace("npc_", "").replace(/_/g, " "),
                npcPortrait: npcData.portrait || "",
                conversations: [],
                unreadCount: 0,
                lastDay: 0, lastHour: 0
            }};
        }}
        var entry = byNpc[npcSlug];
        entry.conversations.push(conv);
        if (!read[conv.id]) entry.unreadCount++;
        var trig = triggered[conv.id];
        if (trig.triggered_day > entry.lastDay || (trig.triggered_day === entry.lastDay && trig.triggered_hour > entry.lastHour)) {{
            entry.lastDay = trig.triggered_day;
            entry.lastHour = trig.triggered_hour;
        }}
    }}
    // Sort conversations within each thread by trigger time (oldest first)
    var npcKeys = Object.keys(byNpc);
    for (var nk = 0; nk < npcKeys.length; nk++) {{
        byNpc[npcKeys[nk]].conversations.sort(function(a, b) {{
            var ta = triggered[a.id] || {{}};
            var tb = triggered[b.id] || {{}};
            if ((ta.triggered_day || 0) !== (tb.triggered_day || 0)) return (ta.triggered_day || 0) - (tb.triggered_day || 0);
            if ((ta.triggered_hour || 0) !== (tb.triggered_hour || 0)) return (ta.triggered_hour || 0) - (tb.triggered_hour || 0);
            return (ta.conv_index || 0) - (tb.conv_index || 0);
        }});
    }}
    var threads = Object.values(byNpc);
    threads.sort(function(a, b) {{ return b.lastDay !== a.lastDay ? b.lastDay - a.lastDay : b.lastHour - a.lastHour; }});
    return threads;
}};

setup.sendPhoneReply = function(convId, choiceIndex, roundNum) {{
    var sv = State.variables;
    var ps = sv.game_state.phone;
    if (!ps) return;
    roundNum = roundNum || 1;
    // Multi-round: store replies as array of {{round, choice}}
    if (!Array.isArray(ps.replies[convId])) {{
        // Backward compat: convert old int format
        if (typeof ps.replies[convId] === 'number') {{
            ps.replies[convId] = [{{round: 1, choice: ps.replies[convId]}}];
        }} else {{
            ps.replies[convId] = [];
        }}
    }}
    ps.replies[convId].push({{round: roundNum, choice: choiceIndex}});
    ps.read_conversations[convId] = true;
    // Find the reply block for this round and apply effects
    var convs = setup.phone_data.conversations || [];
    for (var i = 0; i < convs.length; i++) {{
        if (convs[i].id !== convId) continue;
        var blocks = convs[i].blocks || [];
        for (var b = 0; b < blocks.length; b++) {{
            if (blocks[b].type !== "reply") continue;
            var blockRound = blocks[b].round || 1;
            if (blockRound !== roundNum) continue;
            var choices = blocks[b].choices || [];
            if (choiceIndex >= 0 && choiceIndex < choices.length) {{
                var choice = choices[choiceIndex];
                setup.pendingEffects = [];
                var effs = choice.effects || [];
                for (var e = 0; e < effs.length; e++) {{
                    var eff = effs[e];
                    if (eff.trait) {{
                        setup.applyAndNotifyTrait(eff.targetType || "player", eff.npcId || null, eff.trait, eff.op || "add", Number(eff.value || 0), eff.clamp || false, eff.cap || null);
                    }}
                }}
                var feffs = choice.flagEffects || [];
                for (var f = 0; f < feffs.length; f++) {{
                    var fe = feffs[f];
                    // Delegate to setup.applyAndNotifyFlag so op = set | unset | toggle
                    // is honored uniformly with passage-flow flag emission.
                    setup.applyAndNotifyFlag(
                        fe.targetType || "player",
                        fe.npcId || null,
                        fe.flag,
                        fe.op || "set"
                    );
                }}
                // doc 45 G4/G5 — quest + scheduled effects on chat reply choices
                var qeffs = choice.questEffects || [];
                for (var qi = 0; qi < qeffs.length; qi++) {{
                    setup.applyQuestEffect(qeffs[qi].quest, qeffs[qi].op || "start", qeffs[qi].step);
                }}
                var seffs = choice.scheduleEffects || [];
                for (var sj = 0; sj < seffs.length; sj++) {{ setup.scheduleEvent(seffs[sj]); }}
                setup.showEffectNotification();
            }}
            break;
        }}
        break;
    }}
    setup._chatAnimConv = convId;
    setup._chatAnimRound = roundNum;
    setup.refreshPhoneView();
    setup.updatePhoneBadge();
}};

setup.markConversationRead = function(convId) {{
    var ps = ((State.variables || {{}}).game_state || {{}}).phone;
    if (ps) ps.read_conversations[convId] = true;
}};

// Daily player-initiated chat
setup.sendDailyChat = function(npcSlug, topicId) {{
    var sv = State.variables;
    var ps = sv.game_state.phone;
    if (!ps) return;
    var dailyTopics = (setup.phone_data || {{}}).daily_topics || [];
    var topic = null;
    for (var i = 0; i < dailyTopics.length; i++) {{
        if (dailyTopics[i].id === topicId && dailyTopics[i].npc === npcSlug) {{
            topic = dailyTopics[i]; break;
        }}
    }}
    if (!topic) return;
    // Update daily chat state
    var dc = ps.daily_chats = ps.daily_chats || {{}};
    var npcDc = dc[npcSlug] = dc[npcSlug] || {{ last_day_key: '', count: 0, used_topics: [] }};
    npcDc.topic_days = npcDc.topic_days || {{}};
    // doc 45 G3 — defensive gates (button is hidden when locked, but guard stale clicks)
    var _curKey = setup.getCurrentDayKey();
    if (topic.cooldown === "per_topic" && npcDc.topic_days[topicId] === _curKey) return;
    if (topic.corruption_min != null && (((sv.player || {{}}).core_traits || {{}}).corruption || 0) < topic.corruption_min) return;
    npcDc.last_day_key = _curKey;
    npcDc.topic_days[topicId] = _curKey;
    if (topic.cooldown !== "per_topic") {{
        npcDc.count = (npcDc.count || 0) + 1;
        npcDc.used_topics = npcDc.used_topics || [];
        npcDc.used_topics.push(topicId);
    }}
    // Store chat message in history for display
    var chatHistory = ps.daily_chat_history = ps.daily_chat_history || {{}};
    var npcHistory = chatHistory[npcSlug] = chatHistory[npcSlug] || [];
    npcHistory.push({{
        topic_id: topicId,
        player_message: topic.player_message,
        npc_response: topic.npc_response,
        day_key: _curKey,
        image: topic.image || ''
    }});
    // Apply effects
    setup.pendingEffects = [];
    var effs = topic.effects || [];
    for (var e = 0; e < effs.length; e++) {{
        var eff = effs[e];
        if (eff.trait) {{
            setup.applyAndNotifyTrait(eff.targetType || "player", eff.npcId || null, eff.trait, eff.op || "add", Number(eff.value || 0), eff.clamp || false, eff.cap || null);
        }}
    }}
    setup.showEffectNotification();
    setup.refreshPhoneView();
}};

setup.openPhone = function() {{
    setup.closePhone();
    var apps = (setup.phone_data || {{}}).apps || [];
    var html = '<div class="phone-overlay"><div class="phone-frame">';
    html += '<div class="phone-header"><span class="phone-title">Phone</span><span class="phone-close">&times;</span></div>';
    html += '<div class="phone-screen"><div class="phone-app-grid">';
    for (var i = 0; i < apps.length; i++) {{
        var app = apps[i];
        var iconHtml = app._icon_src
            ? '<img src="' + app._icon_src + '" class="phone-app-icon-img" alt="' + (app.label || app.id) + '">'
            : '<div class="phone-app-icon-letter">' + (app.label || app.id).charAt(0).toUpperCase() + '</div>';
        var badge = '';
        if (app.type === "chat") {{
            var threads = setup.getPhoneThreads(app.id);
            var unread = 0;
            for (var t = 0; t < threads.length; t++) unread += threads[t].unreadCount;
            if (unread > 0) badge = '<span class="phone-app-badge">' + unread + '</span>';
        }}
        html += '<div class="phone-app-item" data-app-id="' + app.id + '" data-app-type="' + app.type + '">';
        html += '<div class="phone-app-icon-wrap">' + iconHtml + badge + '</div>';
        html += '<div class="phone-app-label">' + (app.label || app.id) + '</div>';
        html += '</div>';
    }}
    html += '</div></div></div></div>';
    jQuery(html).appendTo('#story');
    setup._phoneView = 'home';
}};

setup.openPhoneApp = function(appId) {{
    var apps = (setup.phone_data || {{}}).apps || [];
    var appDef = null;
    for (var i = 0; i < apps.length; i++) {{ if (apps[i].id === appId) {{ appDef = apps[i]; break; }} }}
    if (!appDef) return;
    if (appDef.type === "chat") {{ setup._renderThreadList(appId, appDef.label); }}
    else if (appDef.type === "social_feed") {{ setup._renderSocialFeed(appId, appDef.label); }}
    else if (appDef.type === "dating") {{ setup._renderDatingApp(appId, appDef.label); }}
    else if (appDef.type === "quests") {{ setup._renderQuests(appId, appDef.label); }}
    else if (appDef.type === "gallery") {{ setup._renderGallery(appId, appDef.label); }}
    else if (appDef.type === "custom" && appDef.passage) {{ setup._renderCustom(appId, appDef.label, appDef.passage); }}
    else if (appDef.type === "fast_jobs") {{ setup._renderFastJobs(appId, appDef.label); }}
    else if (appDef.type === "bank") {{ setup._renderBank(appId, appDef.label); }}
    else {{ setup._renderPlaceholder(appDef); }}
}};

setup._renderThreadList = function(appId, appLabel) {{
    var threads = setup.getPhoneThreads(appId);
    var vp = '{video_path_js}';
    var html = '<div class="phone-header"><span class="phone-back" data-target="home">&larr;</span><span class="phone-title">' + appLabel + '</span><span class="phone-close">&times;</span></div>';
    html += '<div class="phone-screen"><div class="phone-thread-list">';
    if (threads.length === 0) html += '<div class="phone-empty">No messages yet</div>';
    for (var i = 0; i < threads.length; i++) {{
        var th = threads[i];
        var avatarHtml = th.npcPortrait
            ? '<img src="' + vp + '/' + th.npcPortrait + '" class="phone-thread-avatar">'
            : '<div class="phone-thread-avatar-letter">' + th.npcName.charAt(0).toUpperCase() + '</div>';
        var badge = th.unreadCount > 0 ? '<span class="phone-thread-badge">' + th.unreadCount + '</span>' : '';
        var cls = th.unreadCount > 0 ? ' phone-thread-unread' : '';
        var preview = "";
        if (th.conversations.length > 0) {{
            var lastConv = th.conversations[th.conversations.length - 1];
            var blocks = lastConv.blocks || [];
            for (var b = blocks.length - 1; b >= 0; b--) {{
                if (blocks[b].type === "message" && !blocks[b].after_reply) {{ preview = setup.resolveAtRefs(blocks[b].content); break; }}
            }}
            if (preview.length > 40) preview = preview.substring(0, 40) + "...";
        }}
        html += '<div class="phone-thread-item' + cls + '" data-app-id="' + appId + '" data-npc="' + th.npcSlug + '">';
        html += '<div class="phone-thread-avatar-wrap">' + avatarHtml + '</div>';
        html += '<div class="phone-thread-info"><div class="phone-thread-name">' + th.npcName + badge + '</div>';
        html += '<div class="phone-thread-preview">' + preview + '</div></div></div>';
    }}
    html += '</div></div>';
    jQuery('.phone-frame').html(html);
    setup._phoneView = 'threadList';
    setup._phoneApp = appId;
}};

setup.openChatThread = function(appId, npcSlug) {{
    var threads = setup.getPhoneThreads(appId);
    var thread = null;
    for (var i = 0; i < threads.length; i++) {{ if (threads[i].npcSlug === npcSlug) {{ thread = threads[i]; break; }} }}
    if (!thread) return;
    var sv = State.variables;
    var ps = sv.game_state.phone;
    var html = '<div class="phone-header"><span class="phone-back" data-target="threadList">&larr;</span><span class="phone-title">' + thread.npcName + '</span><span class="phone-close">&times;</span></div>';
    html += '<div class="phone-screen"><div class="phone-chat-messages">';
    // Helper: find reply for a specific round in the replies array
    var _getRoundReply = function(replies, round) {{
        if (!Array.isArray(replies)) return null;
        for (var r = 0; r < replies.length; r++) {{
            if (replies[r].round === round) return replies[r];
        }}
        return null;
    }};
    var _hasPendingReply = false;
    for (var ci = 0; ci < thread.conversations.length; ci++) {{
        // Stop rendering if a previous conversation has an unanswered reply
        if (_hasPendingReply) break;
        var conv = thread.conversations[ci];
        var blocks = conv.blocks || [];
        // Multi-round: get replies array (backward compat: convert old int format)
        var convReplies = ps.replies[conv.id];
        if (typeof convReplies === 'number') {{
            convReplies = [{{round: 1, choice: convReplies}}];
        }}
        convReplies = Array.isArray(convReplies) ? convReplies : [];
        var hasAnyReply = convReplies.length > 0;
        setup.markConversationRead(conv.id);
        for (var bi = 0; bi < blocks.length; bi++) {{
            var block = blocks[bi];
            var blockAfterRound = block.after_round;
            var blockAfterChoice = block.after_choice;
            // Check after_round dependency
            if (blockAfterRound != null) {{
                var parentReply = _getRoundReply(convReplies, blockAfterRound);
                if (!parentReply) continue;
                if (blockAfterChoice != null && parentReply.choice !== blockAfterChoice) continue;
            }}
            // Backward compat: old after_reply field
            if (block.after_reply && !hasAnyReply) continue;
            if (block.type === "message") {{
                var cls = block.sender === "npc" ? "phone-bubble-npc" : "phone-bubble-player";
                var pending = '';
                if (block.sender === "npc" && setup._chatAnimConv === conv.id && blockAfterRound != null && blockAfterRound === setup._chatAnimRound) {{
                    pending = ' phone-bubble-pending';
                }}
                html += '<div class="phone-bubble ' + cls + pending + '">' + setup.resolveAtRefs(block.content) + '</div>';
            }} else if (block.type === "reply") {{
                var blockRound = block.round || 1;
                var thisRoundReply = _getRoundReply(convReplies, blockRound);
                if (thisRoundReply) {{
                    // Already replied — show locked-in choice
                    var choices = block.choices || [];
                    if (thisRoundReply.choice >= 0 && thisRoundReply.choice < choices.length) {{
                        html += '<div class="phone-bubble phone-bubble-player">' + setup.resolveAtRefs(choices[thisRoundReply.choice].text) + '</div>';
                    }}
                }} else {{
                    // Check if this reply block's round dependency is met
                    if (blockAfterRound != null) {{
                        var depReply = _getRoundReply(convReplies, blockAfterRound);
                        if (!depReply) continue;
                    }}
                    // Show reply buttons
                    _hasPendingReply = true;
                    var replyPending = '';
                    if (setup._chatAnimConv === conv.id && blockAfterRound != null && blockAfterRound === setup._chatAnimRound) {{
                        replyPending = ' phone-reply-pending';
                    }}
                    html += '<div class="phone-reply-options' + replyPending + '">';
                    var choices = block.choices || [];
                    for (var ri = 0; ri < choices.length; ri++) {{
                        html += '<button class="phone-reply-btn" data-conv-id="' + conv.id + '" data-choice="' + ri + '" data-round="' + blockRound + '">' + setup.resolveAtRefs(choices[ri].text) + '</button>';
                    }}
                    html += '</div>';
                }}
            }}
        }}
    }}
    // Render daily chat history for this NPC
    var chatHistory = ((ps.daily_chat_history || {{}})[npcSlug]) || [];
    for (var dh = 0; dh < chatHistory.length; dh++) {{
        var dmsg = chatHistory[dh];
        html += '<div class="phone-bubble phone-bubble-player">' + setup.resolveAtRefs(dmsg.player_message) + '</div>';
        if (dmsg.image) html += '<img src="{video_path_js}/' + dmsg.image + '" class="phone-chat-image" onerror="this.remove()">';
        html += '<div class="phone-bubble phone-bubble-npc">' + setup.resolveAtRefs(dmsg.npc_response) + '</div>';
    }}
    // Daily chat: show "Say something..." area if daily limit not reached
    var dailyTopics = (setup.phone_data || {{}}).daily_topics || [];
    var npcTopics = [];
    for (var dti = 0; dti < dailyTopics.length; dti++) {{
        if (dailyTopics[dti].npc === npcSlug) npcTopics.push(dailyTopics[dti]);
    }}
    if (npcTopics.length > 0 && !_hasPendingReply) {{
        var dc = ps.daily_chats = ps.daily_chats || {{}};
        var npcDc = dc[npcSlug] || {{ last_day_key: '', count: 0, used_topics: [] }};
        var currentDayKey = setup.getCurrentDayKey();
        if (npcDc.last_day_key !== currentDayKey) {{
            npcDc.count = 0;
        }}
        // doc 45 G3 — split photo quick-actions (per-topic cooldown + corruption
        // lock + image) from legacy per-NPC daily topics.
        var _corr = ((sv.player || {{}}).core_traits || {{}}).corruption || 0;
        npcDc.topic_days = npcDc.topic_days || {{}};
        var photoTopics = [];
        var legacyTopics = [];
        for (var pti = 0; pti < npcTopics.length; pti++) {{
            var ptp = npcTopics[pti];
            if (ptp.conditions && ptp.conditions.items && !setup.triggerConditionsSatisfied(ptp.conditions)) continue;
            if (ptp.cooldown === "per_topic") photoTopics.push(ptp); else legacyTopics.push(ptp);
        }}
        var photoHtml = '';
        for (var phi = 0; phi < photoTopics.length; phi++) {{
            var ph = photoTopics[phi];
            if (ph.corruption_min != null && _corr < ph.corruption_min) {{
                photoHtml += '<div class="phone-daily-locked">🔒 ' + setup.resolveAtRefs(ph.player_message) + '</div>';
            }} else if (npcDc.topic_days[ph.id] !== currentDayKey) {{
                photoHtml += '<button class="phone-daily-btn" data-npc="' + npcSlug + '" data-topic-id="' + ph.id + '">' + setup.resolveAtRefs(ph.player_message) + '</button>';
            }}
        }}
        // Legacy "Say something" — per-NPC 1/day over non-photo topics.
        var canChat = (npcDc.count || 0) < 1;
        var sayHtml = '';
        if (canChat && legacyTopics.length > 0) {{
            var usedTopics = npcDc.used_topics || [];
            var available = [];
            for (var ati = 0; ati < legacyTopics.length; ati++) {{
                if (usedTopics.indexOf(legacyTopics[ati].id) !== -1) continue;
                available.push(legacyTopics[ati]);
            }}
            if (available.length === 0) {{ npcDc.used_topics = []; available = legacyTopics.slice(); }}
            for (var si = available.length - 1; si > 0; si--) {{
                var ri = Math.floor(Math.random() * (si + 1));
                var tmp = available[si]; available[si] = available[ri]; available[ri] = tmp;
            }}
            var shown = available.slice(0, 3);
            for (var sti = 0; sti < shown.length; sti++) {{
                sayHtml += '<button class="phone-daily-btn" data-npc="' + npcSlug + '" data-topic-id="' + shown[sti].id + '">' + setup.resolveAtRefs(shown[sti].player_message) + '</button>';
            }}
        }}
        if (photoHtml || sayHtml) {{
            html += '<div class="phone-daily-topics">';
            html += '<div class="phone-daily-label">Say something...</div>';
            html += photoHtml + sayHtml;
            html += '</div>';
        }}
    }}
    html += '</div></div>';
    jQuery('.phone-frame').html(html);
    var chatEl = jQuery('.phone-chat-messages')[0];
    if (chatEl) chatEl.scrollTop = chatEl.scrollHeight;
    setup._phoneView = 'chat';
    setup._phoneApp = appId;
    setup._phoneNpc = npcSlug;
    setup.updatePhoneBadge();
    // Animate pending NPC messages with typing indicator
    if (setup._chatAnimConv) {{
        var pendingBubbles = jQuery('.phone-bubble-pending');
        var pendingReply = jQuery('.phone-reply-pending');
        setup._chatAnimConv = null;
        setup._chatAnimRound = null;
        if (pendingBubbles.length > 0) {{
            jQuery('.phone-reply-btn').prop('disabled', true);
            var chatContainer = jQuery('.phone-chat-messages');
            var _scrollBottom = function() {{
                var el = chatContainer[0];
                if (el) el.scrollTop = el.scrollHeight;
            }};
            var _showNext = function(idx) {{
                if (idx >= pendingBubbles.length) {{
                    pendingReply.removeClass('phone-reply-pending');
                    jQuery('.phone-reply-btn').prop('disabled', false);
                    _scrollBottom();
                    return;
                }}
                var indicator = jQuery('<div class="phone-typing-indicator"><span></span><span></span><span></span></div>');
                jQuery(pendingBubbles[idx]).before(indicator);
                _scrollBottom();
                setTimeout(function() {{
                    indicator.remove();
                    jQuery(pendingBubbles[idx]).removeClass('phone-bubble-pending').addClass('phone-bubble-appear');
                    _scrollBottom();
                    setTimeout(function() {{ _showNext(idx + 1); }}, 300);
                }}, 800 + Math.floor(Math.random() * 400));
            }};
            _showNext(0);
        }}
    }}
}};

// ===== Social Feed =====
setup._renderSocialFeed = function(appId, appLabel) {{
    var sv = State.variables;
    var ps = sv.game_state.phone;
    var posts = (setup.phone_data || {{}}).posts || [];
    var triggered = ps.triggered_posts || {{}};
    var npcs = sv.npcs || {{}};
    var vp = '{video_path_js}';
    // Mark feed as viewed
    ps.viewed_feed = true;
    // Gather triggered posts for this app, sorted newest first
    var feed = [];
    for (var i = 0; i < posts.length; i++) {{
        if (posts[i].app !== appId || !triggered[posts[i].id]) continue;
        feed.push({{ post: posts[i], trig: triggered[posts[i].id] }});
    }}
    feed.sort(function(a, b) {{ return b.trig.triggered_day !== a.trig.triggered_day ? b.trig.triggered_day - a.trig.triggered_day : b.trig.triggered_hour - a.trig.triggered_hour; }});

    var html = '<div class="phone-header"><span class="phone-back" data-target="home">&larr;</span><span class="phone-title">' + appLabel + '</span><span class="phone-close">&times;</span></div>';
    html += '<div class="phone-screen"><div class="phone-feed">';
    // doc 45 G2 — player posting composer (post_actions on the social_feed app)
    var appDef = ((setup.phone_data || {{}}).apps || []).filter(function(a) {{ return a.id === appId; }})[0] || {{}};
    var postActions = appDef.post_actions || [];
    if (postActions.length) {{
        var _corr = ((sv.player || {{}}).core_traits || {{}}).corruption || 0;
        var _pd = ps.posted_days = ps.posted_days || {{}};
        var _dayKey = setup.getCurrentDayKey();
        html += '<div class="phone-post-composer">';
        for (var pa = 0; pa < postActions.length; pa++) {{
            var act = postActions[pa];
            var cap = (act.daily_cap != null ? Number(act.daily_cap) : 1);
            var usedKey = appId + ':' + pa;
            var usedToday = (_pd[usedKey] && _pd[usedKey].day === _dayKey) ? _pd[usedKey].count : 0;
            if (act.corruption_min != null && _corr < act.corruption_min) {{
                html += '<div class="phone-daily-locked">🔒 ' + (act.label || 'Post') + '</div>';
            }} else if (usedToday >= cap) {{
                html += '<div class="phone-daily-locked">' + (act.label || 'Post') + ' ✓</div>';
            }} else {{
                html += '<button class="phone-post-btn" data-app-id="' + appId + '" data-action-idx="' + pa + '">' + (act.label || 'Post') + '</button>';
            }}
        }}
        html += '</div>';
    }}
    if (feed.length === 0) {{
        html += '<div class="phone-empty">No posts yet</div>';
    }}
    for (var i = 0; i < feed.length; i++) {{
        var p = feed[i].post;
        var npcName, avatarHtml;
        if (p.poster_name) {{
            npcName = p.poster_name;
            avatarHtml = '<div class="phone-post-avatar-letter">' + npcName.replace(/^@/, '').charAt(0).toUpperCase() + '</div>';
        }} else {{
            var resolvedId = setup.resolveNpcId(p.npc);
            var npcData = npcs[resolvedId] || {{}};
            npcName = npcData.name || p.npc.replace("npc_", "").replace(/_/g, " ");
            avatarHtml = npcData.portrait
                ? '<img src="' + vp + '/' + npcData.portrait + '" class="phone-post-avatar">'
                : '<div class="phone-post-avatar-letter">' + npcName.charAt(0).toUpperCase() + '</div>';
        }}
        var imgHtml = p.image ? '<img src="' + vp + '/' + p.image + '" class="phone-post-image" onerror="this.remove()">' : '';
        html += '<div class="phone-post">';
        html += '<div class="phone-post-header">' + avatarHtml + '<span class="phone-post-name">' + npcName + '</span></div>';
        if (imgHtml) html += imgHtml;
        if (p.caption) html += '<div class="phone-post-caption">' + p.caption + '</div>';
        if (p.likes) html += '<div class="phone-post-likes">' + p.likes + ' likes</div>';
        html += '</div>';
    }}
    html += '</div></div>';
    jQuery('.phone-frame').html(html);
    setup._phoneView = 'feed';
    setup._phoneApp = appId;
    setup.updatePhoneBadge();
}};

// doc 45 G2 — player posts to a social_feed: corruption-gated, daily-capped,
// increments an author-named followers counter.
setup.sendSocialPost = function(appId, actionIdx) {{
    var sv = State.variables;
    var ps = sv.game_state.phone;
    if (!ps) return;
    var appDef = ((setup.phone_data || {{}}).apps || []).filter(function(a) {{ return a.id === appId; }})[0] || {{}};
    var act = (appDef.post_actions || [])[actionIdx];
    if (!act) return;
    var _corr = ((sv.player || {{}}).core_traits || {{}}).corruption || 0;
    if (act.corruption_min != null && _corr < act.corruption_min) return;
    var _pd = ps.posted_days = ps.posted_days || {{}};
    var _dayKey = setup.getCurrentDayKey();
    var usedKey = appId + ':' + actionIdx;
    var cap = (act.daily_cap != null ? Number(act.daily_cap) : 1);
    var rec = (_pd[usedKey] && _pd[usedKey].day === _dayKey) ? _pd[usedKey] : {{ day: _dayKey, count: 0 }};
    if (rec.count >= cap) return;
    rec.count += 1; rec.day = _dayKey; _pd[usedKey] = rec;
    var lo = Number(act.followers_min != null ? act.followers_min : 1);
    var hi = Number(act.followers_max != null ? act.followers_max : lo);
    var gain = lo + Math.floor(Math.random() * (Math.max(lo, hi) - lo + 1));
    var trait = act.counter_trait || 'followers';
    setup.pendingEffects = [];
    setup.applyAndNotifyTrait('player', null, trait, 'add', gain, false, null);
    setup.showEffectNotification();
    setup._renderSocialFeed(appId, appDef.label || '');
}};

// ===== Dating App =====
setup._renderDatingApp = function(appId, appLabel) {{
    var sv = State.variables;
    var ps = sv.game_state.phone;
    var profiles = (setup.phone_data || {{}}).profiles || [];
    var triggered = ps.triggered_profiles || {{}};
    var liked = ps.liked_profiles || {{}};
    var passed = ps.passed_profiles || {{}};
    var matches = ps.matches || {{}};
    var npcs = sv.npcs || {{}};
    var vp = '{video_path_js}';

    var html = '<div class="phone-header"><span class="phone-back" data-target="home">&larr;</span><span class="phone-title">' + appLabel + '</span><span class="phone-close">&times;</span></div>';
    html += '<div class="phone-screen" style="position:relative;">';

    // Matches section at top
    var matchKeys = Object.keys(matches);
    if (matchKeys.length > 0) {{
        html += '<div class="phone-matches-section"><div class="phone-matches-title">Matches</div><div class="phone-matches-row">';
        for (var m = 0; m < matchKeys.length; m++) {{
            var mProf = matches[matchKeys[m]];
            var mNpc = npcs[setup.resolveNpcId(mProf.npc)] || {{}};
            var mAvatar = mNpc.portrait ? '<img src="' + vp + '/' + mNpc.portrait + '" class="phone-match-avatar">' : '<div class="phone-match-avatar-letter">' + (mNpc.name || "?").charAt(0) + '</div>';
            html += mAvatar;
        }}
        html += '</div></div>';
    }}

    // Find next unseen profile
    var nextProf = null;
    for (var i = 0; i < profiles.length; i++) {{
        var prof = profiles[i];
        if (prof.app !== appId || !triggered[prof.id]) continue;
        if (liked[prof.id] || passed[prof.id] || matches[prof.id]) continue;
        nextProf = prof;
        break;
    }}

    if (nextProf) {{
        var resolvedId = setup.resolveNpcId(nextProf.npc);
        var npcData = npcs[resolvedId] || {{}};
        var profName = npcData.name || nextProf.npc.replace("npc_", "").replace(/_/g, " ");
        var photoHtml = '';
        if (nextProf.photos && nextProf.photos.length > 0 && nextProf.photos[0]) {{
            photoHtml = '<img src="' + vp + '/' + nextProf.photos[0] + '" class="phone-profile-photo" onerror="this.remove()">';
        }} else if (npcData.portrait) {{
            photoHtml = '<img src="' + vp + '/' + npcData.portrait + '" class="phone-profile-photo">';
        }} else {{
            photoHtml = '<div class="phone-profile-photo-placeholder">' + profName.charAt(0).toUpperCase() + '</div>';
        }}
        html += '<div class="phone-dating-card">';
        html += photoHtml;
        html += '<div class="phone-profile-info">';
        html += '<span class="phone-profile-name">' + profName + '</span>';
        if (nextProf.age) html += '<span class="phone-profile-age">' + nextProf.age + '</span>';
        html += '</div>';
        if (nextProf.bio) html += '<div class="phone-profile-bio">' + nextProf.bio + '</div>';
        if (nextProf.interests && nextProf.interests.length > 0) {{
            html += '<div class="phone-profile-interests">';
            for (var t = 0; t < nextProf.interests.length; t++) {{
                html += '<span class="phone-profile-tag">' + nextProf.interests[t] + '</span>';
            }}
            html += '</div>';
        }}
        html += '<div class="phone-dating-actions">';
        html += '<button class="phone-dating-btn phone-dating-pass" data-profile-id="' + nextProf.id + '">&times;</button>';
        html += '<button class="phone-dating-btn phone-dating-like" data-profile-id="' + nextProf.id + '">&hearts;</button>';
        html += '</div></div>';
    }} else {{
        html += '<div class="phone-empty">No new profiles</div>';
    }}

    html += '</div>';
    jQuery('.phone-frame').html(html);
    setup._phoneView = 'dating';
    setup._phoneApp = appId;
}};

setup.likeProfile = function(profileId) {{
    var sv = State.variables;
    var ps = sv.game_state.phone;
    if (!ps) return;
    var profiles = (setup.phone_data || {{}}).profiles || [];
    var prof = null;
    for (var i = 0; i < profiles.length; i++) {{ if (profiles[i].id === profileId) {{ prof = profiles[i]; break; }} }}
    if (!prof) return;

    // Check match condition
    var matchCond = prof.match_condition ? prof.match_condition.conditions : null;
    var isMatch = !matchCond || setup.triggerConditionsSatisfied(matchCond);

    if (isMatch) {{
        ps.matches[profileId] = {{ npc: prof.npc, profile_id: profileId }};
        // Show match overlay briefly
        var resolvedId = setup.resolveNpcId(prof.npc);
        var npcData = (sv.npcs || {{}})[resolvedId] || {{}};
        var matchName = npcData.name || prof.npc.replace("npc_", "");
        var overlay = jQuery('<div class="phone-match-overlay"><div class="phone-match-text">It\\\'s a Match!</div><div style="color:#ccc;font-size:14px;">You and ' + matchName + ' liked each other</div><button class="phone-match-dismiss" style="margin-top:20px;padding:10px 24px;border:1px solid #4ecdc4;color:#4ecdc4;background:transparent;border-radius:20px;cursor:pointer;">Keep Swiping</button></div>');
        jQuery('.phone-screen').append(overlay);
    }} else {{
        ps.liked_profiles[profileId] = true;
        setup._renderDatingApp(setup._phoneApp, '');
    }}
    setup.updatePhoneBadge();
}};

setup.passProfile = function(profileId) {{
    var sv = State.variables;
    var ps = sv.game_state.phone;
    if (!ps) return;
    ps.passed_profiles[profileId] = true;
    setup._renderDatingApp(setup._phoneApp, '');
}};

// doc 45 G4 — Quests app: list active + completed quests with current step text.
setup._renderQuests = function(appId, appLabel) {{
    var catalog = setup.quests_data || [];
    var qstate = ((State.variables.game_state || {{}}).quests) || {{}};
    var html = '<div class="phone-header"><span class="phone-back" data-target="home">&larr;</span><span class="phone-title">' + (appLabel || 'Quests') + '</span><span class="phone-close">&times;</span></div>';
    html += '<div class="phone-screen"><div class="phone-quests">';
    var shown = 0;
    for (var i = 0; i < catalog.length; i++) {{
        var def = catalog[i];
        var st = qstate[def.id];
        if (!st || (!st.active && !st.completed)) continue;
        shown++;
        var steps = def.steps || [];
        var idx = Math.min(Number(st.progress || 0), Math.max(0, steps.length - 1));
        var journal = steps.length ? steps[idx] : '';
        var cls = st.completed ? ' quest-completed' : '';
        html += '<div class="phone-quest-card' + cls + '">';
        html += '<div class="phone-quest-name">' + (st.completed ? '✓ ' : '') + (def.name || def.id) + '</div>';
        if (journal && !st.completed) html += '<div class="phone-quest-step">' + journal + '</div>';
        html += '</div>';
    }}
    if (shown === 0) html += '<div class="phone-empty">No quests yet</div>';
    html += '</div></div>';
    jQuery('.phone-frame').html(html);
    setup._phoneView = 'quests';
    setup._phoneApp = appId;
}};

// doc 45 G8 — Gallery app: trigger-gated images, optionally clickable (link → passage).
setup._renderGallery = function(appId, appLabel) {{
    var items = (setup.phone_data || {{}}).gallery_items || [];
    var vp = '{video_path_js}';
    var html = '<div class="phone-header"><span class="phone-back" data-target="home">&larr;</span><span class="phone-title">' + (appLabel || 'Gallery') + '</span><span class="phone-close">&times;</span></div>';
    html += '<div class="phone-screen"><div class="phone-gallery">';
    var shown = 0;
    for (var i = 0; i < items.length; i++) {{
        var it = items[i];
        var trig = it.trigger ? it.trigger.conditions : null;
        if (trig && !setup.triggerConditionsSatisfied(trig)) continue;
        shown++;
        var imgHtml = it.image ? '<img src="' + vp + '/' + it.image + '" class="phone-gallery-img" onerror="this.remove()">' : '';
        var clickable = it.link ? ' phone-gallery-link" data-link="' + it.link : '';
        html += '<div class="phone-gallery-cell' + clickable + '">' + imgHtml + (it.caption ? '<div class="phone-gallery-cap">' + it.caption + '</div>' : '') + '</div>';
    }}
    if (shown === 0) html += '<div class="phone-empty">Nothing here yet</div>';
    html += '</div></div>';
    jQuery('.phone-frame').html(html);
    setup._phoneView = 'gallery';
    setup._phoneApp = appId;
}};

// doc 45 G12 — Custom app: render an authored passage inside the phone frame.
setup._renderCustom = function(appId, appLabel, passage) {{
    var html = '<div class="phone-header"><span class="phone-back" data-target="home">&larr;</span><span class="phone-title">' + (appLabel || '') + '</span><span class="phone-close">&times;</span></div>';
    html += '<div class="phone-screen"><div class="phone-custom" id="phone-custom-body"></div></div>';
    jQuery('.phone-frame').html(html);
    try {{
        var p = Story.get(passage);
        if (p) jQuery('#phone-custom-body').wiki(p.processText());
        else jQuery('#phone-custom-body').html('<div class="phone-empty">Missing: ' + passage + '</div>');
    }} catch (e) {{
        jQuery('#phone-custom-body').html('<div class="phone-empty">Unavailable</div>');
    }}
    setup._phoneView = 'custom';
    setup._phoneApp = appId;
}};

// doc 45 G9 — Fast Jobs app: XP-laddered, cooldown-gated money jobs.
setup._renderFastJobs = function(appId, appLabel) {{
    var sv = State.variables;
    var fj = sv.game_state.fast_jobs = sv.game_state.fast_jobs || {{ xp: 0, cooldowns: {{}} }};
    var jobs = setup.fast_jobs_data || [];
    var html = '<div class="phone-header"><span class="phone-back" data-target="home">&larr;</span><span class="phone-title">' + (appLabel || 'Fast Jobs') + '</span><span class="phone-close">&times;</span></div>';
    html += '<div class="phone-screen"><div class="phone-jobs"><div class="phone-jobs-xp">XP: ' + (fj.xp || 0) + '</div>';
    for (var i = 0; i < jobs.length; i++) {{
        var j = jobs[i];
        var cd = fj.cooldowns[j.id] || 0;
        html += '<div class="phone-job-card"><div class="phone-job-name">' + j.name + '</div>';
        html += '<div class="phone-job-meta">$' + j.income + (j.time_period ? ' · ' + j.time_period : '') + (j.xp_req ? ' · needs ' + j.xp_req + ' xp' : '') + '</div>';
        if ((fj.xp || 0) < (j.xp_req || 0)) html += '<div class="phone-daily-locked">🔒 Need more XP</div>';
        else if (cd > 0) html += '<div class="phone-daily-locked">Again in ' + cd + 'd</div>';
        else html += '<button class="phone-job-btn" data-job-id="' + j.id + '">Work</button>';
        html += '</div>';
    }}
    html += '</div></div>';
    jQuery('.phone-frame').html(html);
    setup._phoneView = 'fast_jobs'; setup._phoneApp = appId;
}};
setup.doFastJob = function(jobId) {{
    var sv = State.variables;
    var fj = sv.game_state.fast_jobs = sv.game_state.fast_jobs || {{ xp: 0, cooldowns: {{}} }};
    var jobs = setup.fast_jobs_data || []; var job = null;
    for (var i = 0; i < jobs.length; i++) {{ if (jobs[i].id === jobId) {{ job = jobs[i]; break; }} }}
    if (!job) return;
    if ((fj.xp || 0) < (job.xp_req || 0)) return;
    if ((fj.cooldowns[jobId] || 0) > 0) return;
    setup.pendingEffects = [];
    setup.applyAndNotifyTrait('player', null, job.money_trait || 'money', 'add', Number(job.income || 0), false, null);
    setup.showEffectNotification();
    fj.xp = (fj.xp || 0) + 1;
    fj.cooldowns[jobId] = Number(job.cooldown_days || 0);
    setup._renderFastJobs(setup._phoneApp, '');
}};

// doc 45 G9 — Bank app: savings balance + deposit/withdraw (daily interest in advanceDay).
setup._renderBank = function(appId, appLabel) {{
    var sv = State.variables;
    var bk = sv.game_state.bank = sv.game_state.bank || {{ balance: 0 }};
    var mtrait = ((setup.bank_data || {{}}).money_trait) || 'money';
    var money = ((sv.player || {{}}).core_traits || {{}})[mtrait] || 0;
    var html = '<div class="phone-header"><span class="phone-back" data-target="home">&larr;</span><span class="phone-title">' + (appLabel || 'Bank') + '</span><span class="phone-close">&times;</span></div>';
    html += '<div class="phone-screen"><div class="phone-bank">';
    html += '<div class="phone-bank-balance">Balance: $' + (bk.balance || 0) + '</div>';
    html += '<div class="phone-bank-cash">Cash: $' + money + '</div>';
    html += '<button class="phone-bank-btn" data-bank="deposit">Deposit all</button>';
    html += '<button class="phone-bank-btn" data-bank="withdraw">Withdraw all</button>';
    html += '</div></div>';
    jQuery('.phone-frame').html(html);
    setup._phoneView = 'bank'; setup._phoneApp = appId;
}};
setup.bankTransfer = function(dir) {{
    var sv = State.variables;
    var bk = sv.game_state.bank = sv.game_state.bank || {{ balance: 0 }};
    var mtrait = ((setup.bank_data || {{}}).money_trait) || 'money';
    var ct = sv.player.core_traits = sv.player.core_traits || {{}};
    var money = ct[mtrait] || 0;
    if (dir === 'deposit' && money > 0) {{ bk.balance = (bk.balance || 0) + money; ct[mtrait] = 0; }}
    else if (dir === 'withdraw' && (bk.balance || 0) > 0) {{ ct[mtrait] = money + bk.balance; bk.balance = 0; }}
    setup._renderBank(setup._phoneApp, '');
}};

setup._renderPlaceholder = function(appDef) {{
    var html = '<div class="phone-header"><span class="phone-back" data-target="home">&larr;</span><span class="phone-title">' + appDef.label + '</span><span class="phone-close">&times;</span></div>';
    html += '<div class="phone-screen"><div class="phone-placeholder"><p>Coming Soon</p></div></div>';
    jQuery('.phone-frame').html(html);
    setup._phoneView = 'placeholder';
}};

setup.closePhone = function() {{
    jQuery('.phone-overlay').remove();
    setup._phoneView = null;
    setup.updatePhoneBadge();
}};

setup.refreshPhoneView = function() {{
    if (!setup._phoneView) return;
    if (setup._phoneView === 'chat' && setup._phoneApp && setup._phoneNpc) {{
        setup.openChatThread(setup._phoneApp, setup._phoneNpc);
    }} else if (setup._phoneView === 'threadList' && setup._phoneApp) {{
        setup._renderThreadList(setup._phoneApp, '');
    }} else {{ setup.openPhone(); }}
}};

setup.updatePhoneBadge = function() {{
    var count = setup.getPhoneUnreadCount();
    var container = jQuery('#phone-sidebar-btn');
    var badge = container.find('.phone-badge');
    if (count > 0) {{
        if (badge.length) {{ badge.text(count); }}
        else {{ container.append('<span class="phone-badge">' + count + '</span>'); }}
    }} else {{
        badge.remove();
    }}
}};
"""

            phone_handlers_block = """
// Phone event handlers
jQuery(document).on('click', '.phone-overlay', function(e) {
    if (jQuery(e.target).hasClass('phone-overlay')) setup.closePhone();
});
jQuery(document).on('click', '.phone-close', function(e) { e.preventDefault(); setup.closePhone(); });
jQuery(document).on('click', '.phone-app-item', function() { setup.openPhoneApp(jQuery(this).data('app-id')); });
jQuery(document).on('click', '.phone-thread-item', function() { setup.openChatThread(jQuery(this).data('app-id'), jQuery(this).data('npc')); });
jQuery(document).on('click', '.phone-back', function() {
    var target = jQuery(this).data('target');
    if (target === 'home') setup.openPhone();
    else if (target === 'threadList') setup.openPhoneApp(setup._phoneApp);
});
// The phone is rendered INSIDE the current passage — every handler below mutates state and
// then re-renders the phone frame by hand, navigating nowhere. So each one commits a moment
// (setup.commitMoment) or its effect would live only in the active moment: Save and a page
// refresh would both replay the state from before the tap. bankTransfer is the sharpest case —
// it moves money, so without a commit a refresh can hand the balance back.
// The commit is CONDITIONAL: setup.commitMoment no-ops on a canvas node, because committing a
// post-render state there would make the node's own advanceTime/trait scripts re-fire on every
// reload. Phoning mid-scene therefore still doesn't survive a refresh — deliberately.
// .phone-gallery-link is exempt: it Engine.plays, so the navigation commits for it.
jQuery(document).on('click', '.phone-reply-btn', function(e) {
    e.preventDefault();
    setup.sendPhoneReply(jQuery(this).data('conv-id'), parseInt(jQuery(this).data('choice'), 10), parseInt(jQuery(this).data('round'), 10) || 1);
    setup.commitMoment();
});
// Daily chat handlers
jQuery(document).on('click', '.phone-daily-btn', function(e) {
    e.preventDefault();
    setup.sendDailyChat(String(jQuery(this).data('npc')), String(jQuery(this).data('topic-id')));
    setup.commitMoment();
});
// Dating app handlers
jQuery(document).on('click', '.phone-post-btn', function(e) {
    e.preventDefault();
    setup.sendSocialPost(jQuery(this).data('app-id'), parseInt(jQuery(this).data('action-idx'), 10));
    setup.commitMoment();
});
jQuery(document).on('click', '.phone-gallery-link', function(e) {
    e.preventDefault();
    var link = jQuery(this).data('link');
    if (link) { setup.closePhone(); Engine.play(String(link)); }
});
jQuery(document).on('click', '.phone-job-btn', function(e) {
    e.preventDefault();
    setup.doFastJob(String(jQuery(this).data('job-id')));
    setup.commitMoment();
});
jQuery(document).on('click', '.phone-bank-btn', function(e) {
    e.preventDefault();
    setup.bankTransfer(String(jQuery(this).data('bank')));
    setup.commitMoment();
});
jQuery(document).on('click', '.phone-dating-like', function(e) {
    e.preventDefault();
    setup.likeProfile(jQuery(this).data('profile-id'));
    setup.commitMoment();
});
jQuery(document).on('click', '.phone-dating-pass', function(e) {
    e.preventDefault();
    setup.passProfile(jQuery(this).data('profile-id'));
    setup.commitMoment();
});
jQuery(document).on('click', '.phone-match-dismiss', function(e) {
    e.preventDefault();
    jQuery('.phone-match-overlay').remove();
    setup._renderDatingApp(setup._phoneApp, '');
});
// Auto-close sidebar on mobile after any sidebar link click
jQuery(document).on('click', '#ui-bar-body a', function() {{ if (window.innerWidth <= 768) {{ UIBar.stow(); }} }});
"""

        return f""":: GameEngine [script]
// Initialize setup object and time management functions
if (typeof setup === 'undefined') {{
    window.setup = {{}};
}}

// Allow multi-step back navigation (SugarCube default is 40; 20 is a good balance)
Config.history.maxStates = 20;

// Save identity + version. id is pinned to the stable template slug (rename-safe),
// not the default slugify(StoryTitle) which orphans saves on a title change.
// version is a schema signature so a future build can detect an incompatible save.
Config.saves.id = {saves_id_json};
Config.saves.version = {saves_version};

// This build's own identity, for save provenance. Read by the :passagestart
// handler, which writes it into $game_state.last_* — the copy inside the save is
// the only record that survives, since setup.* is rebuilt by whichever build the
// player next opens.
setup.buildVersion = {build_version_json};
setup.buildSchema = {saves_version};

// Load hook. SugarCube 2.30 calls this with the save object BEFORE
// State.unmarshalForSave, so State.variables here is still the PRE-load state —
// never write to it from this function. `save.version` is the schema stamp of the
// build that wrote the save (SugarCube copies Config.saves.version in on save).
//
// It never throws, and that is a decision rather than an omission. A throw here
// aborts the load with UI.alert — the call sits inside unmarshal's try — and that
// is exactly the reject-on-mismatch handler this stamp was minted for. We do not
// want it: setup.backfillStateDefaults already heals the mismatches a player can
// actually hit, and refusing a save costs someone their whole run over a schema
// difference they cannot act on. If that ever changes, throw from here; the
// mechanism is wired and this comment is the only thing standing in its way.
Config.saves.onLoad = function (save) {{
    var wroteSchema = (save && save.version) || null;
    setup.saveOrigin = {{
        schema: wroteSchema,
        mismatch: wroteSchema !== setup.buildSchema
    }};
    if (typeof console !== 'undefined' && console.info) {{
        console.info('[save] written by schema ' + wroteSchema + ', this build is ' +
            setup.buildSchema + (setup.saveOrigin.mismatch ? ' — MIGRATED' : ''));
    }}
}};

// Static lookup data — stored on setup (not State.variables) to avoid deep-clone on every passage transition
setup.help_data = {help_data_json};
setup.stateDefaults = {state_defaults_json};
setup.npc_slug_map = {npc_slug_map_json};
setup.hiddenNpcs = {hidden_npcs_json};
setup.locations = {locations_map_json};
setup.story_arc = {story_arc_json};
setup.quests_cards = {quests_cards_json};
setup.clothing_enabled = {"true" if self.clothing_enabled else "false"};
setup.passage_to_location = {passage_to_location_json};
{f"setup.clothing_data = {clothing_data_json};" if self.clothing_enabled else "setup.clothing_data = [];"}
{f"setup.clothingRequirements = {clothing_requirements_json};" if self.clothing_enabled else "setup.clothingRequirements = {};"}
setup.rent_enabled = {"true" if self.rent_enabled else "false"};
{f'setup.rent_amount = {self.rent_amount};' if self.rent_enabled else ''}
{f'setup.rent_collector_npc = "{self.rent_collector_npc}";' if self.rent_enabled else ''}
{f'setup.rent_grace_periods = {self.rent_grace_periods};' if self.rent_enabled else ''}
{f'setup.rent_due_day = "{self.rent_due_day}";' if self.rent_enabled else ''}
{f'setup.rent_start_after_flag = "{self.rent_start_after_flag}";' if self.rent_enabled else ''}
{f'setup.rent_text = {json.dumps(self.rent_text)};' if self.rent_enabled else ''}
{f'setup.rent_eviction_mode = "{self.rent_eviction_mode}";' if self.rent_enabled else ''}
{f'setup.rent_eviction_flag = "{self.rent_eviction_flag}";' if self.rent_enabled else ''}
{f'setup.rent_currency_symbol = {json.dumps(self.rent_currency_symbol)};' if self.rent_enabled else ''}
setup.sidebar_items = {sidebar_items_json};
setup.player_portrait_enabled = {"true" if self.player_portrait_enabled else "false"};
setup.player_portrait = {player_portrait_json};
setup.passes = {json.dumps(self.passes)};
setup.passes_map = {{}};
for (var _pi = 0; _pi < setup.passes.length; _pi++) {{
    setup.passes_map[setup.passes[_pi].id] = setup.passes[_pi];
}}
setup.items = {json.dumps(self.items)};
setup.items_map = {{}};
for (var _ii = 0; _ii < setup.items.length; _ii++) {{
    setup.items_map[setup.items[_ii].id] = setup.items[_ii];
}}
setup.npc_trait_decay = {json.dumps(self.npc_trait_decay_config)};
setup.player_trait_decay = {json.dumps(self.player_trait_decay_config)};
setup.daily_tick = {json.dumps(self.daily_tick)};
setup.quests_data = {json.dumps(self.quests)};
setup.corruption_tiers = {json.dumps(self.corruption_tiers)};
setup.fast_jobs_data = {json.dumps(self.fast_jobs_data)};
setup.bank_data = {json.dumps(self.bank_data)};
setup.stage_helpers = {json.dumps(self.stage_helpers)};
setup.stage_helpers_map = {{}};
for (var _shi = 0; _shi < setup.stage_helpers.length; _shi++) {{
    setup.stage_helpers_map[setup.stage_helpers[_shi].name] = setup.stage_helpers[_shi];
}}
// Pattern 2 (2026-05-01): label registries + stage-setter index for the
// auto-rendered 🎯 goal block (setup.computeHintGoal).
setup.trait_labels = {json.dumps(self.trait_labels)};
setup.flag_labels = {json.dumps(self.flag_labels)};
// Hidden traits (2026-05-30) — flat list of core_trait keys flagged hidden=true
// in [[traits.labels]]. Every player/NPC trait-dump loop skips these via
// <<continue>>, so internal stage/pregnancy/awareness traits never surface.
setup.hiddenTraits = {json.dumps(self.hidden_trait_keys)};
setup.stage_setter_canvases = {json.dumps(self.stage_setter_canvases)};
setup.flag_setter_canvases = {json.dumps(self.flag_setter_canvases)};
// Sub-menu parent index (2026-05-09) — child_canvas_id → parent_menu_canvas_id
// for triggerless sub-menu canvases reached via cross-canvas targetType="node"
// routing. Used by _findFlagSetterCanvas to walk back from triggerless setter
// canvases to a parent that IS in locationCanvases (so State B's Where-frame
// can render 📍/🕒 from the parent menu hub).
setup.sub_menu_parents = {json.dumps(self.sub_menu_parents)};
// PRD 25 — Lane 3 dispatcher substitution map. Keyed by parent canvas UUID;
// each entry is a list of substitution rules with target_canvas_id resolved
// to runtime UUID. Walked at canvas-render entry by setup.checkAndSubstituteCanvas.
setup.canvasSubstitutions = {self._build_canvas_substitutions_json()};
// Phase A (2026-05-14) — NPC location schedule registry. Keyed by NPC slug;
// each entry is a list of {{location, weekdays, start_time, end_time, activity}}.
// setup.getNpcLocation() consults this first; falls back to canvas-derived
// presence when an NPC slug is absent here. Empty for NPCs without declared
// [[npcs.schedules]] in TOML.
setup.npcSchedules = {json.dumps(self.npc_schedules_map)};
// PRD 25 §5.2 — boot-time canvas-id → canvas-data lookup (lazy build on first call).
setup._canvasByIdMap = null;
setup.getCanvasById = function(canvasId) {{
    if (!setup._canvasByIdMap) {{
        setup._canvasByIdMap = {{}};
        var lc = (setup.help_data || {{}}).locationCanvases || {{}};
        for (var loc in lc) {{
            var list = lc[loc] || [];
            for (var i = 0; i < list.length; i++) {{
                if (list[i] && list[i].id) {{
                    setup._canvasByIdMap[String(list[i].id)] = list[i];
                }}
            }}
        }}
    }}
    return setup._canvasByIdMap[String(canvasId)] || null;
}};
// Tips page — game-level mechanics surface. Empty object = sidebar button
// + page suppress (graceful no-op for games without [ui.tips_page]).
setup.tips_page = {json.dumps(self.tips_page or {})};
// E9/E10/E11 foundation: per-NPC stage display names, slug-keyed.
// Empty object = no NPC has a stage chain (existing TOMLs unaffected).
// Trait name convention: <slug>_stage in $player.core_traits (integer 0..N).
setup.npc_arc_stages = {json.dumps(self.npc_arc_stages_map)};
// G: per-NPC cast-card tag line, slug-keyed. Empty object = no NPC declares
// `tags` and the cast card renders no tag row (existing TOMLs unaffected).
setup.npc_tags = {json.dumps(self.npc_tags_map)};
setup.phone_enabled = {"true" if self.phone_enabled else "false"};
setup.phone_purchase_flag = {json.dumps(self.phone_purchase_flag)};
setup.phone_data = {phone_data_json};

// NPC ID resolver: converts slugs to UUIDs for $npcs lookups
// Conditions from TOML use NPC slugs (e.g., "elena") but $npcs is keyed by UUID
setup.resolveNpcId = function(idOrSlug) {{
    if (!idOrSlug) return null;
    var slugMap = setup.npc_slug_map || {{}};
    var key = String(idOrSlug);
    // If it's a slug, resolve to UUID; otherwise return as-is (already UUID)
    return slugMap[key] || key;
}};

// Resolve @npc_short and @player references in JS strings at runtime
// Used for emotion mapping descriptions and help_data text where <<print>> macros don't work
setup.resolveAtRefs = function(text) {{
    if (!text || typeof text !== 'string') return text;
    return text.replace(/@(\\w+(?:\\.\\w+)?)/g, function(match, ref) {{
        var parts = ref.split('.');
        var shortName = parts[0];
        var field = parts[1] || 'name';
        // Handle @player references
        if (shortName === 'player') {{
            var p = State.variables.player;
            if (!p) return match;
            if (field === 'name') return p.name || match;
            return p[field] || '';
        }}
        // Handle @npc references
        var slug = 'npc_' + shortName;
        var slugMap = setup.npc_slug_map || {{}};
        var uuid = slugMap[slug] || slugMap[shortName];
        if (!uuid) return match;
        var npc = (State.variables.npcs || {{}})[uuid];
        if (!npc) return match;
        if (field === 'rel') return npc.relationship || '';
        return npc.name || match;
    }});
}};

// Player image_select handler — updates $player field and optionally portrait
setup.selectPlayerField = function(fieldId, value, imagePath, setsPortrait) {{
    var sv = State.variables;
    if (!sv.player) return;
    sv.player[fieldId] = value;
    if (setsPortrait && imagePath) {{
        sv.player.portrait = imagePath;
    }}
}};

// Image select click handler (event delegation)
jQuery(document).on('click', '.player-img-option', function(e) {{
    var $el = jQuery(this);
    var fieldId = $el.data('field');
    var value = $el.data('value');
    var image = $el.data('image');
    var setsPortrait = String($el.data('sets-portrait')) === 'true';
    $el.siblings('.player-img-option').removeClass('player-img-selected');
    $el.addClass('player-img-selected');
    setup.selectPlayerField(fieldId, value, image, setsPortrait);
    // Navigates nowhere — commit, or the pick is lost on save/refresh (see setup.commitMoment).
    if (setup.commitMoment) {{ setup.commitMoment(); }}
}});

// Time period calculation function
setup.getTimePeriod = function(hour) {{
    if (hour >= 6 && hour < 12) return "Morning";
    if (hour >= 12 && hour < 18) return "Afternoon";
    if (hour >= 18 && hour < 22) return "Evening";
    return "Night";
}};

// Schedule evaluation function for trigger conditionals
// Accepts array of schedule objects, returns true if ANY schedule is active (OR logic)
setup.isScheduleActive = function(scheduleArray) {{
    // Empty/null = always active (no schedule restriction)
    if (!scheduleArray || scheduleArray.length === 0) return true;

    const timeState = State.variables.game_state.time_state;
    const dayIndex = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].indexOf(timeState.current_day);
    const currentHour = timeState.current_hour;
    const currentMinute = timeState.current_minute;
    const currentTotal = (currentHour * 60) + currentMinute;

    // Check each schedule - return true if ANY matches (OR logic)
    for (var i = 0; i < scheduleArray.length; i++) {{
        var sched = scheduleArray[i];
        var weekdays = sched.weekdays || [];
        var startTime = sched.startTime;
        var endTime = sched.endTime;

        // Check day (empty weekdays = any day)
        if (weekdays.length > 0 && !weekdays.includes(dayIndex)) continue;

        // Parse start time
        var startParts = startTime.split(':');
        var startTotal = parseInt(startParts[0]) * 60 + parseInt(startParts[1]);

        if (endTime) {{
            // Range trigger
            var endParts = endTime.split(':');
            var endTotal = parseInt(endParts[0]) * 60 + parseInt(endParts[1]);

            // Handle overnight schedules (e.g., 22:00 to 08:00)
            if (endTotal < startTotal) {{
                if (currentTotal >= startTotal || currentTotal < endTotal) return true;
            }} else {{
                if (currentTotal >= startTotal && currentTotal < endTotal) return true;
            }}
        }} else {{
            // Point trigger - active for 1 hour window
            if (currentTotal >= startTotal && currentTotal < startTotal + 60) return true;
        }}
    }}
    return false;
}};

// ===== NPC Schedule Helper Functions =====
// Schedules are derived dynamically from setup.help_data.locationCanvases at runtime.
// This ensures non-repeatable canvases disappear after being played and
// condition-gated canvases only appear when conditions are met.

// Build reverse map: location UUID → TOML slug (cached per passage render)
setup._getLocUuidToSlug = function() {{
    if (setup._locUuidToSlugCache) return setup._locUuidToSlugCache;
    var locs = setup.locations || {{}};
    var map = {{}};
    for (var slug in locs) {{
        if (locs[slug] && locs[slug].id) {{
            map[String(locs[slug].id)] = slug;
        }}
    }}
    setup._locUuidToSlugCache = map;
    return map;
}};

// Build reverse map: NPC UUID → slug (cached)
setup._getNpcUuidToSlug = function() {{
    if (setup._npcUuidToSlugCache) return setup._npcUuidToSlugCache;
    var slugMap = setup.npc_slug_map || {{}};
    var map = {{}};
    for (var slug in slugMap) {{
        var uuid = String(slugMap[slug]);
        // Prefer the canonical long-form `npc_<x>` slug over the short alias.
        // npc_slug_map intentionally has both `npc_frank` and `frank` mapping
        // to the same UUID (the short form supports `@frank.name` references
        // in narrative text per v1.py:572-575). For UUID->slug lookups we want
        // the long form because that's what canvas trigger metadata stores in
        // `c.npcId`. Without this guard, JS object iteration order causes the
        // short alias to overwrite the long form, breaking
        // getNpcScheduleFromCanvases' string-equality filter.
        if (map[uuid] && /^npc_/.test(map[uuid])) continue;
        map[uuid] = slug;
    }}
    setup._npcUuidToSlugCache = map;
    return map;
}};

// Check if a canvas is available (conditions + completion) WITHOUT checking time.
// Used by schedule functions that need all time windows, not just currently active ones.
setup._isCanvasAvailable = function(c) {{
    try {{
        // Check conditions if present
        if (c.conditions && !setup.triggerConditionsSatisfied(c.conditions)) {{
            return false;
        }}
        // Check repeatability (non-repeatable and already triggered ever)
        var hist = State.variables.game_state.trigger_history || {{}};
        var rec = hist[String(c.id)];
        if (!c.isRepeatable && rec && (rec.total || 0) >= 1) {{
            return false;
        }}
        return true;
    }} catch (e) {{
        return false;
    }}
}};

// Core: Get available schedule entries for an NPC from canvas triggers
// Checks conditions + completion but NOT current time (returns all time windows)
// Returns array of {{location, start_time, end_time, weekdays, activity}}
setup.getNpcScheduleFromCanvases = function(npcSlug) {{
    try {{
        var sv = State.variables;
        var helpData = setup.help_data || {{}};
        var locationCanvases = helpData.locationCanvases || {{}};
        var locUuidToSlug = setup._getLocUuidToSlug();
        var result = [];
        var seen = {{}};  // Dedup key: "locSlug|startTime|endTime"

        for (var locUuid in locationCanvases) {{
            var canvasList = locationCanvases[locUuid];
            var locSlug = locUuidToSlug[locUuid];
            if (!locSlug) continue;

            for (var i = 0; i < canvasList.length; i++) {{
                var c = canvasList[i];
                // Only canvases linked to this NPC
                if (c.npcId !== npcSlug) continue;
                // Must have schedules
                if (!c.hasSchedules || !c.scheduleParams || c.scheduleParams.length === 0) continue;
                // Check conditions + completion (but NOT time — we want all windows)
                if (!setup._isCanvasAvailable(c)) continue;

                // Extract schedule entries
                for (var s = 0; s < c.scheduleParams.length; s++) {{
                    var sp = c.scheduleParams[s];
                    var startTime = sp.startTime || "00:00";
                    var endTime = sp.endTime || null;
                    var weekdays = sp.weekdays || [];

                    // Dedup: same location + same time window → keep first
                    var dedupKey = locSlug + "|" + startTime + "|" + endTime + "|" + weekdays.join(",");
                    if (seen[dedupKey]) continue;
                    seen[dedupKey] = true;

                    result.push({{
                        location: locSlug,
                        start_time: startTime,
                        end_time: endTime,
                        weekdays: weekdays,
                        activity: c.displayName || c.name || ""
                    }});
                }}
            }}
        }}
        return result;
    }} catch (e) {{
        return [];
    }}
}};

// Get the current location of an NPC based on game time (dynamic)
setup.getNpcLocation = function(npcId) {{
    try {{
        var resolvedId = setup.resolveNpcId(npcId);
        var uuidToSlug = setup._getNpcUuidToSlug();
        var npcSlug = uuidToSlug[resolvedId] || npcId;
        if (!npcSlug) return null;

        // Phase A (2026-05-14) — Path 1: declared [[npcs.schedules]] is the
        // canonical source of truth. If the NPC has explicit schedule
        // entries in setup.npcSchedules, walk them first. First match wins;
        // returning null here means the NPC is explicitly "gone" / offscreen
        // (not co-located anywhere) at the current time.
        var declared = (setup.npcSchedules || {{}})[npcSlug];
        if (declared && declared.length > 0) {{
            var timeState = State.variables.game_state.time_state;
            var DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday",
                             "Friday", "Saturday", "Sunday"];
            var todayIndex = DAY_NAMES.indexOf(timeState.current_day);
            for (var di = 0; di < declared.length; di++) {{
                var ds = declared[di];
                if (!setup._weekdayMatches(ds.weekdays, todayIndex)) continue;
                if (!setup.isCurrentTimeSlot(ds.start_time, ds.end_time)) continue;
                return {{
                    location: ds.location,
                    activity: ds.activity || ""
                }};
            }}
            return null;  // Declared schedule but no current match = NPC absent.
        }}

        // Path 2 (back-compat fallback) — original canvas-derived presence.
        // Only reached for NPCs without declared schedules. Lets un-migrated
        // NPCs keep working without changes.
        var entries = setup.getNpcScheduleFromCanvases(npcSlug);
        if (entries.length === 0) return null;

        for (var i = 0; i < entries.length; i++) {{
            var sch = entries[i];
            if (setup.isCurrentTimeSlot(sch.start_time, sch.end_time)) {{
                return {{
                    location: sch.location,
                    activity: sch.activity || ""
                }};
            }}
        }}
        return null;
    }} catch (e) {{
        return null;
    }}
}};

// Get all NPC slugs currently resolved to a location (shared-space occupancy, redesign_phase_3/25).
// Backs the any-NPC ("room occupied"/"room empty") form of the npc_at_location condition.
setup.getNpcsAtLocation = function(locId) {{
    var out = [];
    try {{
        var locMap = setup._getLocUuidToSlug() || {{}};
        var target = (locId && locMap[locId]) ? locMap[locId] : locId;
        var schedules = setup.npcSchedules || {{}};
        for (var slug in schedules) {{
            if (!schedules.hasOwnProperty(slug)) continue;
            var loc = setup.getNpcLocation(slug);
            if (!loc || !loc.location) continue;
            var here = locMap[loc.location] || loc.location;
            if (here === target) out.push(slug);
        }}
    }} catch (e) {{ return out; }}
    return out;
}};

// Get schedule entries for a specific NPC on a specific day (dynamic)
setup.getNpcDaySchedule = function(npcId, dayIndex) {{
    try {{
        var resolvedId = setup.resolveNpcId(npcId);
        var uuidToSlug = setup._getNpcUuidToSlug();
        var npcSlug = uuidToSlug[resolvedId];
        if (!npcSlug) return [];

        // Prefer the declared [[npcs.schedules]] registry (authoritative weekly
        // timetable); fall back to canvas-derived entries for un-migrated games.
        // Declared entries carry location_slug; setup.locations is slug-keyed, so
        // always surface the slug for the display name lookup.
        var declared = (setup.npcSchedules || {{}})[npcSlug];
        var entries = (declared && declared.length > 0) ? declared : setup.getNpcScheduleFromCanvases(npcSlug);
        var result = [];
        for (var i = 0; i < entries.length; i++) {{
            var sch = entries[i];
            // Empty weekdays = all days
            if (!sch.weekdays || sch.weekdays.length === 0 || sch.weekdays.includes(dayIndex)) {{
                result.push({{
                    location: sch.location_slug || sch.location,
                    start_time: sch.start_time || "00:00",
                    end_time: sch.end_time || null,
                    activity: sch.activity || ""
                }});
            }}
        }}
        return result;
    }} catch (e) {{
        return [];
    }}
}};

// Get all NPCs with available schedule entries (dynamic)
setup.getNpcsWithSchedules = function() {{
    try {{
        var sv = State.variables;
        var helpData = setup.help_data || {{}};
        var locationCanvases = helpData.locationCanvases || {{}};
        var npcs = sv.npcs || {{}};
        var slugMap = setup.npc_slug_map || {{}};
        var found = {{}};  // npcSlug → true
        var result = [];

        // Scan all location canvases for NPC-linked entries with schedules
        for (var locUuid in locationCanvases) {{
            var canvasList = locationCanvases[locUuid];
            for (var i = 0; i < canvasList.length; i++) {{
                var c = canvasList[i];
                if (!c.npcId || !c.hasSchedules) continue;
                if (found[c.npcId]) continue;
                // Check conditions + completion (NOT time — schedule button should show if NPC has any available canvases)
                if (!setup._isCanvasAvailable(c)) continue;
                found[c.npcId] = true;
            }}
        }}

        // Declared [[npcs.schedules]] registry is the authoritative source —
        // surface every NPC that has a declared schedule, regardless of whether
        // any of its canvases are unlocked yet. (Canvas scan above stays as a
        // back-compat fallback for games that declare no [[npcs.schedules]].)
        var declaredSched = setup.npcSchedules || {{}};
        for (var dSlug in declaredSched) {{
            if (declaredSched[dSlug] && declaredSched[dSlug].length > 0) found[dSlug] = true;
        }}

        // Resolve slugs to UUIDs and build result
        for (var npcSlug in found) {{
            var npcUuid = slugMap[npcSlug];
            if (!npcUuid || !npcs[npcUuid]) continue;
            result.push({{
                id: npcUuid,
                name: npcs[npcUuid].name
            }});
        }}
        return result;
    }} catch (e) {{
        return [];
    }}
}};

// Get solo repeatable activities for today, sorted by start time
// Returns: [{{name, locationName, startTime, endTime, isCurrent}}]
setup.getSoloActivitiesForToday = function() {{
    try {{
        var helpData = setup.help_data || {{}};
        var locationCanvases = helpData.locationCanvases || {{}};
        var locUuidToSlug = setup._getLocUuidToSlug();
        var locs = setup.locations || {{}};
        var timeState = State.variables.game_state.time_state;
        var DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
        var todayIndex = DAY_NAMES.indexOf(timeState.current_day);
        var result = [];

        for (var locUuid in locationCanvases) {{
            var canvasList = locationCanvases[locUuid];
            var locSlug = locUuidToSlug[locUuid];
            var locationName = locSlug && locs[locSlug] ? (locs[locSlug].name || locSlug) : (locSlug || locUuid);

            for (var i = 0; i < canvasList.length; i++) {{
                var c = canvasList[i];
                // Solo canvases only: no NPC, has schedules, is repeatable
                if (c.npcId) continue;
                if ((c.triggerMode || "manual") === "random") continue;
                if (!c.hasSchedules || !c.scheduleParams || c.scheduleParams.length === 0) continue;
                if (!c.isRepeatable) continue;
                if (!setup._isCanvasAvailable(c)) continue;

                for (var s = 0; s < c.scheduleParams.length; s++) {{
                    var sp = c.scheduleParams[s];
                    var weekdays = sp.weekdays || [];
                    if (weekdays.length > 0 && weekdays.indexOf(todayIndex) === -1) continue;

                    var startTime = sp.startTime || "00:00";
                    var endTime = sp.endTime || null;
                    var isCurrent = setup.isCurrentTimeSlot(startTime, endTime);

                    result.push({{
                        name: c.displayName || c.name || "Activity",
                        locationName: locationName,
                        startTime: startTime,
                        endTime: endTime,
                        isCurrent: isCurrent
                    }});
                }}
            }}
        }}

        result.sort(function(a, b) {{
            var aParts = a.startTime.split(':');
            var bParts = b.startTime.split(':');
            var aMin = parseInt(aParts[0]) * 60 + parseInt(aParts[1]);
            var bMin = parseInt(bParts[0]) * 60 + parseInt(bParts[1]);
            return aMin - bMin;
        }});

        return result;
    }} catch (e) {{
        return [];
    }}
}};

// Get today's schedule sorted by start time
setup.getTodayScheduleSorted = function(npcId) {{
    var timeState = State.variables.game_state.time_state;
    var dayIndex = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                   .indexOf(timeState.current_day);
    var schedules = setup.getNpcDaySchedule(npcId, dayIndex);

    // Sort by start time
    schedules.sort(function(a, b) {{
        var aParts = a.start_time.split(':');
        var bParts = b.start_time.split(':');
        var aMinutes = parseInt(aParts[0]) * 60 + parseInt(aParts[1]);
        var bMinutes = parseInt(bParts[0]) * 60 + parseInt(bParts[1]);
        return aMinutes - bMinutes;
    }});
    return schedules;
}};

// Get all schedule entries for an NPC (across all weekdays), with weekdays preserved.
// Used by SchedulePage's all-weekday view.
setup.getNpcAllSchedulesSorted = function(npcId) {{
    try {{
        var resolvedId = setup.resolveNpcId(npcId);
        var uuidToSlug = setup._getNpcUuidToSlug();
        var npcSlug = uuidToSlug[resolvedId];
        if (!npcSlug) return [];

        // Prefer the declared [[npcs.schedules]] registry (authoritative weekly
        // timetable); fall back to canvas-derived entries for un-migrated games.
        // Declared entries carry location_slug; setup.locations is slug-keyed.
        var declared = (setup.npcSchedules || {{}})[npcSlug];
        var entries = (declared && declared.length > 0) ? declared : setup.getNpcScheduleFromCanvases(npcSlug);
        var result = [];
        for (var i = 0; i < entries.length; i++) {{
            var sch = entries[i];
            result.push({{
                location: sch.location_slug || sch.location,
                start_time: sch.start_time || "00:00",
                end_time: sch.end_time || null,
                weekdays: sch.weekdays || [],
                activity: sch.activity || ""
            }});
        }}
        result.sort(function(a, b) {{
            var aParts = a.start_time.split(':');
            var bParts = b.start_time.split(':');
            var aMinutes = parseInt(aParts[0]) * 60 + parseInt(aParts[1]);
            var bMinutes = parseInt(bParts[0]) * 60 + parseInt(bParts[1]);
            return aMinutes - bMinutes;
        }});
        return result;
    }} catch (e) {{
        return [];
    }}
}};

// Get all solo activities (across all weekdays), with weekdays preserved.
// Mirrors getSoloActivitiesForToday but returns one row per (canvas, schedule) pair
// regardless of today's weekday. `isCurrent` still computed against today.
setup.getSoloActivitiesAllSchedules = function() {{
    try {{
        var helpData = setup.help_data || {{}};
        var locationCanvases = helpData.locationCanvases || {{}};
        var locUuidToSlug = setup._getLocUuidToSlug();
        var locs = setup.locations || {{}};
        var timeState = State.variables.game_state.time_state;
        var DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
        var todayIndex = DAY_NAMES.indexOf(timeState.current_day);
        var result = [];

        for (var locUuid in locationCanvases) {{
            var canvasList = locationCanvases[locUuid];
            var locSlug = locUuidToSlug[locUuid];
            var locationName = locSlug && locs[locSlug] ? (locs[locSlug].name || locSlug) : (locSlug || locUuid);

            for (var i = 0; i < canvasList.length; i++) {{
                var c = canvasList[i];
                if (c.npcId) continue;
                if ((c.triggerMode || "manual") === "random") continue;
                if (!c.hasSchedules || !c.scheduleParams || c.scheduleParams.length === 0) continue;
                if (!c.isRepeatable) continue;
                if (!setup._isCanvasAvailable(c)) continue;

                for (var s = 0; s < c.scheduleParams.length; s++) {{
                    var sp = c.scheduleParams[s];
                    var weekdays = sp.weekdays || [];
                    var startTime = sp.startTime || "00:00";
                    var endTime = sp.endTime || null;
                    var matchesToday = (weekdays.length === 0) || (weekdays.indexOf(todayIndex) !== -1);
                    var isCurrent = matchesToday && setup.isCurrentTimeSlot(startTime, endTime);

                    result.push({{
                        name: c.displayName || c.name || "Activity",
                        locationName: locationName,
                        startTime: startTime,
                        endTime: endTime,
                        weekdays: weekdays,
                        isCurrent: isCurrent
                    }});
                }}
            }}
        }}

        result.sort(function(a, b) {{
            var aParts = a.startTime.split(':');
            var bParts = b.startTime.split(':');
            var aMin = parseInt(aParts[0]) * 60 + parseInt(aParts[1]);
            var bMin = parseInt(bParts[0]) * 60 + parseInt(bParts[1]);
            return aMin - bMin;
        }});

        return result;
    }} catch (e) {{
        return [];
    }}
}};

// True if the entry's weekdays array includes todayIndex (or is empty = all days).
setup._weekdayMatches = function(weekdays, todayIndex) {{
    if (!weekdays || weekdays.length === 0) return true;
    return weekdays.indexOf(todayIndex) !== -1;
}};

// Render weekday availability as a row of pill chips. Empty/missing or full-week
// (length === 7) collapses to a single "Daily" chip.
setup.renderWeekdayBadges = function(weekdays, todayIndex) {{
    var SHORT = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
    var hasAll = !weekdays || weekdays.length === 0 || weekdays.length === 7;
    if (hasAll) {{
        return '<span class="weekday-badges"><span class="weekday-badge weekday-all">Daily</span></span>';
    }}
    var present = {{}};
    for (var i = 0; i < weekdays.length; i++) {{ present[weekdays[i]] = true; }}
    var html = '<span class="weekday-badges">';
    for (var d = 0; d < 7; d++) {{
        if (!present[d]) continue;
        var cls = 'weekday-badge';
        if (d === todayIndex) cls += ' weekday-today';
        html += '<span class="' + cls + '">' + SHORT[d] + '</span>';
    }}
    html += '</span>';
    return html;
}};

// Check if current game time is within a time slot
setup.isCurrentTimeSlot = function(startTime, endTime) {{
    var timeState = State.variables.game_state.time_state;
    var currentTotal = (timeState.current_hour * 60) + timeState.current_minute;

    var startParts = startTime.split(':');
    var startTotal = parseInt(startParts[0]) * 60 + parseInt(startParts[1]);

    var endTotal;
    if (endTime) {{
        var endParts = endTime.split(':');
        endTotal = parseInt(endParts[0]) * 60 + parseInt(endParts[1]);
    }} else {{
        endTotal = startTotal + 60;
    }}

    // Handle overnight (e.g., 22:00-06:00)
    if (endTotal < startTotal) {{
        return currentTotal >= startTotal || currentTotal < endTotal;
    }}
    return currentTotal >= startTotal && currentTotal < endTotal;
}};

// Format hour:minute to readable time (e.g., "10:30 AM")
setup.formatTime = function(hour, minute) {{
    var period = hour >= 12 ? 'PM' : 'AM';
    var displayHour = hour % 12 || 12;
    var displayMinute = minute < 10 ? '0' + minute : minute;
    return displayHour + ':' + displayMinute + ' ' + period;
}};

// ===== Trigger Conditions Evaluator =====
// Evaluates v1.0 trigger conditions against current game state (flags/traits)
setup.triggerConditionsSatisfied = function(conditions) {{
    try {{
        // Treat missing/empty conditions as satisfied
        if (!conditions || typeof conditions !== 'object') return true;
        if (!conditions.version || conditions.version !== '1.0') return true;
        var items = Array.isArray(conditions.items) ? conditions.items : [];
        if (items.length === 0) return true;
        var logic = (conditions.logic === 'OR') ? 'OR' : 'AND';

        var sv = State.variables || {{}};
        var player = sv.player || {{}};
        var npcs = sv.npcs || {{}};

        function hasKey(obj, key) {{
            if (!obj || typeof obj !== 'object') return false;
            return Object.prototype.hasOwnProperty.call(obj, String(key));
        }}

        function coerceNumber(v) {{
            var n = Number(v);
            return isNaN(n) ? null : n;
        }}

        function compare(op, left, right) {{
            if (op === 'eq') return left === right;
            if (op === 'ne') return left !== right;
            if (op === 'gt' || op === 'gte' || op === 'lt' || op === 'lte') {{
                var lnum = coerceNumber(left);
                var rnum = coerceNumber(right);
                if (lnum === null || rnum === null) return false;
                if (op === 'gt') return lnum > rnum;
                if (op === 'gte') return lnum >= rnum;
                if (op === 'lt') return lnum < rnum;
                if (op === 'lte') return lnum <= rnum;
            }}
            if (op === 'in') {{
                if (!Array.isArray(right)) return false;
                return right.includes(left);
            }}
            if (op === 'not_in') {{
                if (!Array.isArray(right)) return false;
                return !right.includes(left);
            }}
            if (op === 'contains') {{
                if (Array.isArray(left)) return left.includes(right);
                if (typeof left === 'string') return String(left).includes(String(right));
                return false;
            }}
            if (op === 'not_contains') {{
                if (Array.isArray(left)) return !left.includes(right);
                if (typeof left === 'string') return !String(left).includes(String(right));
                return false;
            }}
            if (op === 'exists') return (left !== undefined && left !== null);
            if (op === 'not_exists') return (left === undefined || left === null);
            return false;
        }}

        var results = [];
        for (var i = 0; i < items.length; i++) {{
            var it = items[i];
            if (!it || typeof it !== 'object') {{ results.push(false); continue; }}
            var type = it.type;
            var subject = it.subject;
            var satisfied = false;

            if (type === 'flag') {{
                var key = it.flag_key;
                var op = it.operator;
                if (!key || (subject !== 'player' && subject !== 'npc')) {{ results.push(false); continue; }}
                if (subject === 'player') {{
                    // Use global $flags for player flags (sv.flags = State.variables.flags)
                    var flags = (sv.flags || {{}});
                    if (op === 'exists') {{
                        satisfied = hasKey(flags, key);
                    }} else if (op === 'is_true') {{
                        satisfied = (flags[String(key)] === true);
                    }} else if (op === 'is_false') {{
                        // Treat missing or strictly false as false
                        var v = flags[String(key)];
                        satisfied = (v === false || v === undefined);
                    }} else {{
                        satisfied = false;
                    }}
                }} else if (subject === 'npc') {{
                    var rawNpcId = it.npc_id || it.character_id || '';
                    var npcId = setup.resolveNpcId(rawNpcId);
                    var npc = npcId ? (npcs[npcId] || null) : null;
                    var flagsNpc = npc && npc.flags ? npc.flags : {{}};
                    if (op === 'exists') {{
                        satisfied = hasKey(flagsNpc, key);
                    }} else if (op === 'is_true') {{
                        satisfied = (flagsNpc[String(key)] === true);
                    }} else if (op === 'is_false') {{
                        var v2 = flagsNpc[String(key)];
                        satisfied = (v2 === false || v2 === undefined);
                    }} else {{
                        satisfied = false;
                    }}
                }}
                results.push(satisfied);
                continue;
            }}

            // Temporary modifier condition type
            if (type === 'modifier') {{
                var mkey = it.modifier_key || '';
                var mop = it.operator || 'is_active';
                var isActive = setup.isModifierActive(mkey);
                satisfied = (mop === 'is_active') ? isActive : !isActive;
                results.push(satisfied);
                continue;
            }}

            if (type === 'trait') {{
                var tkey = it.trait_key;
                var top = it.operator;
                if (!tkey || (subject !== 'player' && subject !== 'npc')) {{ results.push(false); continue; }}
                var leftVal = null;
                if (subject === 'player') {{
                    leftVal = (player.core_traits || {{}})[String(tkey)];
                    // Add temporary modifier offset (modifiers affect checks, not actual traits)
                    var modOffset = setup.getModifierOffset(String(tkey));
                    if (modOffset !== 0) {{
                        leftVal = (leftVal || 0) + modOffset;
                    }}
                }} else if (subject === 'npc') {{
                    var rawNpc2Id = it.npc_id || it.character_id || '';
                    var npc2Id = setup.resolveNpcId(rawNpc2Id);
                    var npc2 = npc2Id ? (npcs[npc2Id] || null) : null;
                    leftVal = npc2 && npc2.core_traits ? npc2.core_traits[String(tkey)] : undefined;
                }}
                var rightVal = it.value;
                satisfied = compare(top, leftVal, rightVal);
                results.push(satisfied);
                continue;
            }}

            // days_since_flag: Check how many days have passed since a flag was set
            if (type === 'days_since_flag') {{
                var flagKey = it.flag_key;
                var dsOp = it.operator;
                var requiredDays = it.value;
                if (!flagKey) {{ results.push(false); continue; }}

                var flagValue = false;
                var setDay = null;

                if (subject === 'player' || !subject) {{
                    flagValue = (sv.flags || {{}})[String(flagKey)];
                    var meta = (sv.flags_meta || {{}})[String(flagKey)];
                    setDay = meta ? meta.set_day : null;
                }} else if (subject === 'npc') {{
                    var rawNpc3Id = it.npc_id || it.character_id || '';
                    var npc3Id = setup.resolveNpcId(rawNpc3Id);
                    var npc3 = npc3Id ? (npcs[npc3Id] || null) : null;
                    if (npc3) {{
                        flagValue = (npc3.flags || {{}})[String(flagKey)];
                        var npcMeta = (npc3.flags_meta || {{}})[String(flagKey)];
                        setDay = npcMeta ? npcMeta.set_day : null;
                    }}
                }}

                // If flag not set or no metadata, condition fails
                if (!flagValue || setDay === null) {{
                    satisfied = false;
                }} else {{
                    var currentDay = (sv.game_state && sv.game_state.time_state) ? sv.game_state.time_state.day : 1;
                    var daysSince = currentDay - setDay;
                    satisfied = compare(dsOp, daysSince, requiredDays);
                }}
                results.push(satisfied);
                continue;
            }}

            // clothing_slot: Check if a slot has something equipped or not
            if (type === 'clothing_slot') {{
                if (!setup.clothing_enabled) {{ results.push(false); continue; }}
                var slotName = it.slot;
                var slotOp = it.operator;
                var equipped = (sv.player && sv.player.equipped) ? sv.player.equipped[slotName] : null;
                if (slotOp === 'equipped') {{
                    satisfied = (equipped !== null && equipped !== undefined);
                }} else if (slotOp === 'unequipped') {{
                    satisfied = (equipped === null || equipped === undefined);
                }} else {{
                    satisfied = false;
                }}
                results.push(satisfied);
                continue;
            }}

            // clothing_item: Check if a specific item is equipped or owned
            if (type === 'clothing_item') {{
                if (!setup.clothing_enabled) {{ results.push(false); continue; }}
                var itemId = it.item_id;
                var itemOp = it.operator;
                var playerObj = sv.player || {{}};
                if (itemOp === 'equipped') {{
                    var eq = playerObj.equipped || {{}};
                    satisfied = Object.values(eq).indexOf(itemId) !== -1;
                }} else if (itemOp === 'unequipped') {{
                    var eq2 = playerObj.equipped || {{}};
                    satisfied = Object.values(eq2).indexOf(itemId) === -1;
                }} else if (itemOp === 'owned') {{
                    var wd = playerObj.wardrobe || {{}};
                    satisfied = !!wd[itemId];
                }} else if (itemOp === 'not_owned') {{
                    var wd2 = playerObj.wardrobe || {{}};
                    satisfied = !wd2[itemId];
                }} else {{
                    satisfied = false;
                }}
                results.push(satisfied);
                continue;
            }}

            // worn_beauty / worn_corruption: gate on the MAX stat across the
            // equipped outfit. Routes content; does NOT touch global corruption.
            // Guard MUST short-circuit before calling the aggregate — the
            // aggregates only exist in clothing-enabled builds.
            // worn_exposure: how much of her is showing, 0/1/2. Unlike the two
            // aggregates below it READS EMPTY SLOTS — see setup.getWornExposure.
            if (type === 'worn_exposure') {{
                if (!setup.clothing_enabled) {{ results.push(false); continue; }}
                satisfied = compare(it.operator || 'gte',
                                    setup.getWornExposure(),
                                    it.value || 0);
                results.push(satisfied);
                continue;
            }}

            // time_of_day: is the clock inside an hour window right now. The
            // field's second most common phone gate (20 of 27 corpus games) and
            // the only one we could not express — see references/the-phone.md P4.
            // Delegates to setup.isCurrentTimeSlot so the overnight wrap
            // (22:00-06:00) behaves exactly as it does for NPC schedules; there
            // is no second implementation of the wrap to drift from the first.
            // Unlike a schedule, this is re-evaluated on every read, so it is a
            // window and not a latch — an omitted end_time means one hour.
            if (type === 'time_of_day') {{
                satisfied = setup.isCurrentTimeSlot(it.start_time || '00:00',
                                                    it.end_time || null);
                results.push(satisfied);
                continue;
            }}

            if (type === 'worn_beauty' || type === 'worn_corruption') {{
                if (!setup.clothing_enabled) {{ results.push(false); continue; }}
                var wornOp = it.operator || 'gte';
                var wornVal = it.value || 0;
                var wornCur = (type === 'worn_beauty')
                    ? setup.getWornBeauty()
                    : setup.getWornCorruption();
                satisfied = compare(wornOp, wornCur, wornVal);
                results.push(satisfied);
                continue;
            }}

            // Doc 72 — worn_type: outfit-category gate. `eq` returns true when
            // any equipped item declares the matching type; `neq` is the
            // inverse. Empty value never matches (defensive). Doc 71 R2.
            if (type === 'worn_type') {{
                if (!setup.clothing_enabled) {{ results.push(false); continue; }}
                var wtOp = it.operator || 'eq';
                var wtVal = it.value || '';
                var wornT = setup.getWornTypes();
                if (!wtVal) {{
                    satisfied = false;
                }} else if (wtOp === 'eq') {{
                    satisfied = wornT.indexOf(wtVal) !== -1;
                }} else if (wtOp === 'neq') {{
                    satisfied = wornT.indexOf(wtVal) === -1;
                }} else {{
                    satisfied = false;
                }}
                results.push(satisfied);
                continue;
            }}

            // pass: Check if a recurring pass is active
            if (type === 'pass') {{
                var passId = it.pass_id || '';
                var passOp = it.operator || 'is_active';
                var isActive = setup.isPassActive(passId);
                satisfied = (passOp === 'is_active') ? isActive : !isActive;
                results.push(satisfied);
                continue;
            }}

            // item: Check inventory item count
            if (type === 'item') {{
                var itemId = it.item_id || '';
                var itemOp = it.operator || 'gte';
                var itemVal = it.value || 0;
                var count = setup.getItemCount(itemId);
                satisfied = compare(itemOp, count, itemVal);
                results.push(satisfied);
                continue;
            }}

            // E4: stage — reference a named composite gate by name.
            // Helpers reference primitive types only (validated at template
            // import time), so this single-level recurse is cycle-free.
            if (type === 'stage') {{
                var helperName = String(it.helper || '');
                var stageOp = String(it.operator || 'is_true');
                var helper = (setup.stage_helpers_map || {{}})[helperName];
                if (!helper || !helper.conditions) {{
                    if (window.console && setup.dev_mode) {{
                        console.warn('Stage helper not found: ' + helperName);
                    }}
                    results.push(false);
                    continue;
                }}
                var inner = setup.triggerConditionsSatisfied(helper.conditions);
                results.push(stageOp === 'is_false' ? !inner : inner);
                continue;
            }}
            // doc 45 G4 — quest condition: {{type:'quest', quest_id, operator:'active'|'completed'|'step_gte', value?}}
            if (type === 'quest') {{
                var qid = String(it.quest_id || it.quest || '');
                var qop = String(it.operator || 'active');
                var qstate = (((State.variables.game_state || {{}}).quests) || {{}})[qid] || {{ active: false, progress: 0, completed: false }};
                var qres;
                if (qop === 'completed') {{ qres = !!qstate.completed; }}
                else if (qop === 'step_gte') {{ qres = (Number(qstate.progress || 0) >= Number(it.value || 0)); }}
                else {{ qres = !!qstate.active; }}  // 'active'
                results.push(qres);
                continue;
            }}
            // doc 45 G7 — corruption tier: {{type:'corruption_level', operator:'gte'|'lt'|'eq', value}}
            if (type === 'corruption_level') {{
                var lvl = setup.getCorruptionLevel();
                var clop = String(it.operator || 'gte');
                var clval = Number(it.value || 0);
                var clres = (clop === 'lt') ? (lvl < clval) : (clop === 'eq') ? (lvl === clval) : (lvl >= clval);
                results.push(clres);
                continue;
            }}
            // shared-space occupancy (redesign_phase_3/25) — cross-room presence:
            // {{type:'npc_at_location', npc_id?, location_id, operator:'is_present'|'is_absent'}}
            // npc_id given → that NPC present/absent at location_id; npc_id omitted → location occupied/empty.
            if (type === 'npc_at_location') {{
                var nalLoc = String(it.location_id || it.location || '');
                if (!nalLoc) {{ results.push(false); continue; }}
                var nalOp = String(it.operator || 'is_present');
                var nalMap = setup._getLocUuidToSlug() || {{}};
                var nalTarget = nalMap[nalLoc] || nalLoc;
                var nalNpc = String(it.npc_id || it.character_id || '');
                var nalPresent;
                if (nalNpc) {{
                    var nalWhere = setup.getNpcLocation(nalNpc);
                    var nalHere = (nalWhere && nalWhere.location) ? (nalMap[nalWhere.location] || nalWhere.location) : null;
                    nalPresent = (nalHere !== null && nalHere === nalTarget);
                }} else {{
                    nalPresent = (setup.getNpcsAtLocation(nalLoc).length > 0);
                }}
                results.push(nalOp === 'is_absent' ? !nalPresent : nalPresent);
                continue;
            }}

            // Unknown type
            results.push(false);
        }}

        if (results.length === 0) return false;
        if (logic === 'AND') return results.every(function(x) {{ return !!x; }});
        return results.some(function(x) {{ return !!x; }});
    }} catch (e) {{
        // Fail open to avoid breaking gameplay
        return true;
    }}
}};

// ===== Wardrobe System (conditional) =====
{wardrobe_js_block}
// ===== Shop System (conditional) =====
{shop_js_block}
// ===== Phone System (conditional) =====
{phone_js_block}
// ===== Trigger Repeatability & Limits =====
// Utility to build a unique day key combining week and day
setup.getCurrentDayKey = function() {{
    try {{
        var ts = State.variables.game_state.time_state;
        return String(ts.current_week) + ':' + String(ts.current_day);
    }} catch (e) {{
        return '0:Monday';
    }}
}};

// Check if a canvas can trigger based on repeatability and per-day limit
setup.canTriggerCanvas = function(canvasId, isRepeatable, maxPerDay) {{
    try {{
        var sv = State.variables;
        sv.game_state = sv.game_state || {{}};
        var hist = sv.game_state.trigger_history = sv.game_state.trigger_history || {{}};
        var rec = hist[String(canvasId)] || null;

        if (!rec) {{
            // Never triggered before; allowed
            return true;
        }}

        // Not repeatable and already triggered once
        if (!isRepeatable && (rec.total || 0) >= 1) {{
            return false;
        }}

        // Per-day limit check
        if (maxPerDay !== null && maxPerDay !== undefined) {{
            var currentDayKey = setup.getCurrentDayKey();
            var dayKey = rec.dayKey || '';
            var dayCount = rec.dayCount || 0;
            if (dayKey !== currentDayKey) {{
                // New day; reset dayCount logic allows trigger
                return true;
            }}
            if (dayCount >= Number(maxPerDay)) {{
                return false;
            }}
        }}

        return true;
    }} catch (e) {{
        // Fail open
        return true;
    }}
}};

// Check if an activity can trigger based on shared per-day limit across all tiers
// All tiers of the same activity name share the same daily limit
setup.canTriggerActivity = function(activityName, maxPerDay) {{
    try {{
        // No limit set - always allowed
        if (maxPerDay === null || maxPerDay === undefined) {{
            return true;
        }}

        var sv = State.variables;
        sv.game_state = sv.game_state || {{}};
        var actHist = sv.game_state.activity_trigger_history =
            sv.game_state.activity_trigger_history || {{}};

        var rec = actHist[String(activityName)] || null;
        if (!rec) {{
            // Never triggered before; allowed
            return true;
        }}

        var currentDayKey = setup.getCurrentDayKey();
        if (rec.dayKey !== currentDayKey) {{
            // New day; allowed
            return true;
        }}

        // Check daily limit
        if ((rec.dayCount || 0) >= Number(maxPerDay)) {{
            return false;
        }}

        return true;
    }} catch (e) {{
        return true; // Fail open
    }}
}};

// Mark an activity as triggered: increments per-day counter at activity name level
setup.markActivityTriggered = function(activityName) {{
    try {{
        var sv = State.variables;
        sv.game_state = sv.game_state || {{}};
        var actHist = sv.game_state.activity_trigger_history =
            sv.game_state.activity_trigger_history || {{}};

        var key = String(activityName);
        var rec = actHist[key] || {{ dayKey: '', dayCount: 0 }};
        var currentDayKey = setup.getCurrentDayKey();

        if (rec.dayKey !== currentDayKey) {{
            rec.dayKey = currentDayKey;
            rec.dayCount = 0;
        }}

        rec.dayCount = (rec.dayCount || 0) + 1;
        actHist[key] = rec;
    }} catch (e) {{
        // ignore
    }}
}};

// Mark a canvas as triggered: increments total and per-day counters
// Also tracks at activity level for shared daily limits across tiers
setup.markCanvasTriggered = function(canvasId) {{
    try {{
        var sv = State.variables;
        sv.game_state = sv.game_state || {{}};
        var hist = sv.game_state.trigger_history = sv.game_state.trigger_history || {{}};
        var key = String(canvasId);
        var rec = hist[key] || {{ total: 0, dayKey: '', dayCount: 0 }};
        var currentDayKey = setup.getCurrentDayKey();
        if (rec.dayKey !== currentDayKey) {{
            rec.dayKey = currentDayKey;
            rec.dayCount = 0;
        }}
        rec.total = (rec.total || 0) + 1;
        rec.dayCount = (rec.dayCount || 0) + 1;
        hist[key] = rec;

        // Also track at activity level (all tiers share same daily limit)
        var helpData = setup.help_data || {{}};
        var canvasNameMap = helpData.canvasIdToActivityName || {{}};
        var activityName = canvasNameMap[key];
        if (activityName) {{
            setup.markActivityTriggered(activityName);
        }}

        // Track NPC interaction for trait decay (prevents decay for NPCs interacted with today)
        var npcUuidMap = helpData.canvasIdToNpcUuid || {{}};
        var npcUuid = npcUuidMap[key];
        if (npcUuid) {{
            sv.npc_interacted_today = sv.npc_interacted_today || {{}};
            sv.npc_interacted_today[npcUuid] = true;
        }}
    }} catch (e) {{
        // ignore
    }}
}};

// ===== Temporary Modifier System =====

// Apply a temporary modifier that offsets trait condition checks for a duration
setup.applyModifier = function(key, name, durationHours, traitOffsets) {{
    try {{
        var ts = State.variables.game_state.time_state;
        var expiresHour = ts.current_hour + durationHours;
        var expiresDay = ts.day;
        while (expiresHour >= 24) {{
            expiresHour -= 24;
            expiresDay += 1;
        }}
        State.variables.game_state.active_modifiers = State.variables.game_state.active_modifiers || {{}};
        State.variables.game_state.active_modifiers[key] = {{
            name: name,
            expires_day: expiresDay,
            expires_hour: expiresHour,
            trait_offsets: traitOffsets || {{}}
        }};
    }} catch (e) {{
        // ignore
    }}
}};

// Check if a modifier is currently active
setup.isModifierActive = function(key) {{
    var mods = (State.variables.game_state || {{}}).active_modifiers;
    return !!(mods && mods[key]);
}};

// Get total trait offset from all active modifiers for a given trait
setup.getModifierOffset = function(traitKey) {{
    var mods = ((State.variables.game_state || {{}}).active_modifiers) || {{}};
    var total = 0;
    for (var key in mods) {{
        var offsets = mods[key].trait_offsets || {{}};
        if (typeof offsets[traitKey] === 'number') {{
            total += offsets[traitKey];
        }}
    }}
    return total;
}};

// ===== Recurring Pass System =====
setup.purchasePass = function(passId) {{
    var config = setup.passes_map[passId];
    if (!config) return false;
    var money = (State.variables.player.core_traits || {{}}).money || 0;
    if (money < config.cost) return false;
    State.variables.player.core_traits.money -= config.cost;
    var currentDay = State.variables.game_state.time_state.day;
    State.variables.game_state.passes = State.variables.game_state.passes || {{}};
    State.variables.game_state.passes[passId] = {{
        purchased_day: currentDay,
        expires_day: currentDay + config.duration_days
    }};
    return true;
}};

setup.isPassActive = function(passId) {{
    var passes = (State.variables.game_state || {{}}).passes || {{}};
    var p = passes[passId];
    if (!p) return false;
    var currentDay = (State.variables.game_state.time_state || {{}}).day || 1;
    return currentDay <= p.expires_day;
}};

setup.getPassDaysRemaining = function(passId) {{
    var passes = (State.variables.game_state || {{}}).passes || {{}};
    var p = passes[passId];
    if (!p) return -1;
    var currentDay = (State.variables.game_state.time_state || {{}}).day || 1;
    return Math.max(0, p.expires_day - currentDay);
}};

// ===== Inventory System =====
setup.addItem = function(itemId, quantity) {{
    var config = setup.items_map[itemId];
    if (!config) return false;
    var inv = State.variables.game_state.inventory = State.variables.game_state.inventory || {{}};
    var current = inv[itemId] || 0;
    var maxStack = config.max_stack || 99;
    inv[itemId] = Math.min(current + (quantity || 1), maxStack);
    return true;
}};

setup.removeItem = function(itemId, quantity) {{
    var inv = (State.variables.game_state || {{}}).inventory || {{}};
    var current = inv[itemId] || 0;
    var toRemove = quantity || 1;
    if (current < toRemove) return false;
    inv[itemId] = current - toRemove;
    if (inv[itemId] <= 0) delete inv[itemId];
    return true;
}};

setup.getItemCount = function(itemId) {{
    var inv = (State.variables.game_state || {{}}).inventory || {{}};
    return inv[itemId] || 0;
}};

// Check if a canvas has never been completed (for highlighting new content)
setup.isCanvasNew = function(canvasId) {{
    try {{
        var sv = State.variables;
        sv.game_state = sv.game_state || {{}};
        var hist = sv.game_state.trigger_history || {{}};
        var record = hist[String(canvasId)];
        return !record || (record.total || 0) === 0;
    }} catch (e) {{
        return true; // Fail open - show as new if error
    }}
}};

// ===== Pure-selection helpers for the three location-entry routing paths =====
// Single source of truth for "what content will the player encounter when
// they walk into this location." Used by:
//   - getStoryCanvasRedirect (auto-fire on entry)
//   - renderNpcPortraits   (NPC portrait click)
//   - renderSoloActivities (solo button click)
//   - locationHasNewCanvases (the NEW badge — checks isCanvasNew on the
//     same picks the renderers will produce, so the badge can't promise
//     content the player can't actually reach from the location screen).
// All three are PURE — no side effects, no marking, no RNG side effects.

// Auto-fire selection: which non-repeatable canvas would auto-fire on
// location entry? Returns canvas object or null.
setup.selectAutoFireCanvasForLocation = function(locationId) {{
    try {{
        var helpData = setup.help_data || {{}};
        var canvasList = (helpData.locationCanvases || {{}})[String(locationId)] || [];
        var best = null, bestPriority = -1;
        for (var i = 0; i < canvasList.length; i++) {{
            var c = canvasList[i];
            if (c.isRepeatable) continue;
            if ((c.triggerMode || "manual") === "random") continue;
            if (c.substitutionOnly) continue;  // PRD 25 §5.5 — defensive filter
            if (!setup.isCanvasValid(c)) continue;
            if ((c.priority || 0) > bestPriority) {{
                bestPriority = c.priority || 0;
                best = c;
            }}
        }}
        return best;
    }} catch (e) {{
        return null;
    }}
}};

// NPC portrait selection: which NPC portraits will render at this location,
// and which canvas does each route to? Returns a map (npcSlug to canvas)
// of AFFORDABLE picks only. Blocked portraits are excluded — clicking them
// lands on a cost-blocked gate, not on playable content, so they shouldn't
// trigger the NEW badge even if the underlying canvas is unvisited. The
// renderer collects blocked portraits separately for greying out — that
// stays inline since only the renderer needs it.
setup.selectNpcPortraitCanvasesForLocation = function(locationId) {{
    var picks = {{}};
    try {{
        var helpData = setup.help_data || {{}};
        var canvasList = (helpData.locationCanvases || {{}})[String(locationId)] || [];
        var npcAffordable = {{}};
        for (var i = 0; i < canvasList.length; i++) {{
            var c = canvasList[i];
            if (!c.isRepeatable) continue;
            if ((c.triggerMode || "manual") === "random") continue;
            if (c.substitutionOnly) continue;  // PRD 25 §5.5
            if (!c.npcId) continue;
            if (!setup.isCanvasValid(c)) continue;
            if (!setup.canTriggerActivity(c.name || c.id, c.maxPerDay)) continue;
            if (c.costs && c.costs.length > 0 && !setup.checkCostsAffordable(c.costs)) continue;
            if (!npcAffordable[c.npcId]) npcAffordable[c.npcId] = [];
            npcAffordable[c.npcId].push(c);
        }}
        var sortByPriorityDesc = function(a, b) {{ return (b.priority || 0) - (a.priority || 0); }};
        for (var slug in npcAffordable) {{
            npcAffordable[slug].sort(sortByPriorityDesc);
            picks[slug] = npcAffordable[slug][0];
        }}
    }} catch (e) {{
        // empty picks
    }}
    return picks;
}};

// Solo activity selection: which solo (NPC-less) activities will render at
// this location? Returns array of AFFORDABLE, cooldown-clear canvases only.
// Same blocked-exclusion rationale as the portrait selector.
setup.selectSoloActivityCanvasesForLocation = function(locationId) {{
    var picks = [];
    try {{
        var helpData = setup.help_data || {{}};
        var canvasList = (helpData.locationCanvases || {{}})[String(locationId)] || [];
        for (var i = 0; i < canvasList.length; i++) {{
            var c = canvasList[i];
            if (!c.isRepeatable) continue;
            if ((c.triggerMode || "manual") === "random") continue;
            if (c.substitutionOnly) continue;  // PRD 25 §5.5
            if (c.npcId) continue;  // belongs to portrait path
            if (!setup.isCanvasValid(c)) continue;
            if (!setup.canTriggerActivity(c.name || c.id, c.maxPerDay)) continue;
            if (c.costs && c.costs.length > 0 && !setup.checkCostsAffordable(c.costs)) continue;
            picks.push(c);
        }}
    }} catch (e) {{
        // empty picks
    }}
    return picks;
}};

// Capstone-only NEW badge (2026-05-25 doctrine tightening) — fires iff a
// non-repeatable auto-fire canvas is queued for this location's entry.
// selectAutoFireCanvasForLocation already filters !isRepeatable, non-random
// trigger, non-substitution, valid schedule+conditions. Per-portrait and
// per-solo NEW indicators (always repeatable click targets) were removed in
// the same pass — repeatable surfaces no longer carry NEW signals anywhere.
setup.locationHasNewCanvases = function(locationId) {{
    try {{
        var autoFire = setup.selectAutoFireCanvasForLocation(locationId);
        return !!(autoFire && setup.isCanvasNew(autoFire.id));
    }} catch (e) {{
        return false; // Fail closed
    }}
}};

// ===== Conditional Choice Unlock Tracking =====
// Check if a specific conditional choice has been visited
setup.isChoiceVisited = function(choiceKey) {{
    try {{
        return !!State.variables.game_state.visited_choices[String(choiceKey)];
    }} catch (e) {{
        return false;
    }}
}};

// Mark a conditional choice as visited (called when player clicks it)
setup.markChoiceVisited = function(choiceKey) {{
    try {{
        var vc = State.variables.game_state.visited_choices = State.variables.game_state.visited_choices || {{}};
        vc[String(choiceKey)] = true;
    }} catch (e) {{
        // ignore
    }}
}};

// ===== Priority-Based Canvas Selection =====
// Check if a canvas is valid (schedule, conditions, repeatability)
setup.isCanvasValid = function(c) {{
    try {{
        // Check schedule if present
        if (c.hasSchedules && c.scheduleParams) {{
            if (!setup.isScheduleActive(c.scheduleParams)) {{
                return false;
            }}
        }}
        // Check conditions if present
        if (c.conditions && !setup.triggerConditionsSatisfied(c.conditions)) {{
            return false;
        }}
        // Check repeatability
        if (!setup.canTriggerCanvas(c.id, c.isRepeatable, c.maxPerDay)) {{
            return false;
        }}
        return true;
    }} catch (e) {{
        return false;
    }}
}};

// Check if canvas is valid for tiered selection (schedule + conditions only)
// Does NOT check per-canvas daily limit since daily limit is checked at activity level
// Used by selectCanvasByPriority where all tiers share the same daily limit
setup.isCanvasValidForSelection = function(c) {{
    try {{
        // Check schedule if present
        if (c.hasSchedules && c.scheduleParams) {{
            if (!setup.isScheduleActive(c.scheduleParams)) {{
                return false;
            }}
        }}
        // Check conditions if present
        if (c.conditions && !setup.triggerConditionsSatisfied(c.conditions)) {{
            return false;
        }}
        // Check repeatability (non-repeatable and already triggered ever)
        var hist = State.variables.game_state.trigger_history || {{}};
        var rec = hist[String(c.id)];
        if (!c.isRepeatable && rec && (rec.total || 0) >= 1) {{
            return false;
        }}
        return true;
    }} catch (e) {{
        return false;
    }}
}};

// ===== Resource Cost System =====
// Check if player can afford all costs for a canvas
// costs: array of {{trait: string, value: number}}
setup.checkCostsAffordable = function(costs) {{
    if (!costs || costs.length === 0) return true;
    var sv = State.variables;
    var playerTraits = (sv.player && sv.player.core_traits) ? sv.player.core_traits : {{}};
    for (var i = 0; i < costs.length; i++) {{
        var cost = costs[i];
        var current = Number(playerTraits[String(cost.trait)] || 0);
        if (current < Number(cost.value)) return false;
    }}
    return true;
}};

// Look up costs for a canvas by its ID (searches all locations)
setup.getCanvasCosts = function(canvasId) {{
    var helpData = setup.help_data || {{}};
    var allCanvases = helpData.locationCanvases || {{}};
    var locIds = Object.keys(allCanvases);
    for (var i = 0; i < locIds.length; i++) {{
        var list = allCanvases[locIds[i]];
        for (var j = 0; j < list.length; j++) {{
            if (list[j].id === String(canvasId)) {{
                return list[j].costs || [];
            }}
        }}
    }}
    return [];
}};

// Apply a raw [{{trait, value}}] cost array as deductions. Shared by canvas costs
// and location entry costs so the two paths can never drift.
setup.deductCostArray = function(costs) {{
    if (!costs || costs.length === 0) return;
    setup.pendingEffects = [];
    for (var k = 0; k < costs.length; k++) {{
        setup.applyAndNotifyTrait('player', null, costs[k].trait, 'add', -Number(costs[k].value), true, null);
    }}
    setup.showEffectNotification();
}};

// Deduct costs for a canvas (called on canvas entry)
setup.deductCosts = function(canvasId) {{
    setup.deductCostArray(setup.getCanvasCosts(canvasId));
}};

// Get a human-readable blocked message for unaffordable costs
setup.getCostBlockedMessage = function(costs) {{
    if (!costs || costs.length === 0) return '';
    var sv = State.variables;
    var playerTraits = (sv.player && sv.player.core_traits) ? sv.player.core_traits : {{}};
    var lines = [];
    for (var i = 0; i < costs.length; i++) {{
        var cost = costs[i];
        var current = Number(playerTraits[String(cost.trait)] || 0);
        var traitDisplay = String(cost.trait).charAt(0).toUpperCase() + String(cost.trait).slice(1);
        if (current < Number(cost.value)) {{
            lines.push('Requires ' + cost.value + ' ' + traitDisplay + ' (you have ' + Math.floor(current) + ')');
        }}
    }}
    return lines.join('. ');
}};

// ===== Location entry-cost system (travel friction) =====
// A location's per-entry cost lives in setup.locations[slug].entry_costs as a dict
// {{time, energy, ...}}. `time` (minutes) advances the day-cycle clock; every other
// key is a player-trait deduction. Empty/absent = a free move (today's behavior).
setup.getLocationEntryCosts = function(slug) {{
    var loc = (setup.locations || {{}})[String(slug)] || {{}};
    return loc.entry_costs || {{}};
}};

// The trait-deduction portion (everything except `time`) as a [{{trait,value}}] array.
setup.locationCostTraitArray = function(slug) {{
    var ec = setup.getLocationEntryCosts(slug);
    var arr = [];
    Object.keys(ec).forEach(function(k) {{
        if (k === 'time') return;
        arr.push({{ trait: k, value: Number(ec[k]) }});
    }});
    return arr;
}};

// Affordability for entering a location. `time` is never a gate (you can always
// spend time) — only the trait portion is checked, via the shared affordability fn.
setup.checkLocationCostsAffordable = function(slug) {{
    return setup.checkCostsAffordable(setup.locationCostTraitArray(slug));
}};

// Charge a location's entry cost exactly once: advance the clock by `time`, deduct traits.
setup.deductLocationCosts = function(slug) {{
    var ec = setup.getLocationEntryCosts(slug);
    if (!ec || Object.keys(ec).length === 0) return;
    var mins = Number(ec.time || 0);
    if (mins > 0 && typeof window.advanceTime === 'function') {{
        window.advanceTime(mins);
    }}
    setup.deductCostArray(setup.locationCostTraitArray(slug));
}};

// Short nav-card cost tag, e.g. "30m · 10 Energy". Empty when the location is free.
setup.getLocationCostTag = function(slug) {{
    var ec = setup.getLocationEntryCosts(slug);
    var parts = [];
    if (Number(ec.time || 0) > 0) parts.push(Number(ec.time) + 'm');
    Object.keys(ec).forEach(function(k) {{
        if (k === 'time') return;
        var disp = String(k).charAt(0).toUpperCase() + String(k).slice(1);
        parts.push(Number(ec[k]) + ' ' + disp);
    }});
    return parts.join(' · ');
}};

// Reason string when a location's entry is unaffordable (trait portion only).
setup.getLocationCostBlockedMessage = function(slug) {{
    return setup.getCostBlockedMessage(setup.locationCostTraitArray(slug));
}};

// ===== Lock-as-prose on the nav surface =====
// Is this destination's door open right now? Versionless/empty conditions fail OPEN
// (matches the passage-entry guard + the global condition evaluator), so a location
// without real entry_conditions always renders a normal, clickable link.
setup.navDestUnlocked = function(slug) {{
    var loc = (setup.locations || {{}})[String(slug)] || {{}};
    var ec = loc.entry_conditions || {{}};
    if (!ec.items || ec.items.length === 0) return true;
    return setup.triggerConditionsSatisfied(ec);
}};

// The in-world reason a locked destination shows in-place: the authored blocked_message,
// else the formatted conditions, else a quiet default. Same source the passage guard
// uses, so the nav card and the blocked passage can never disagree.
setup.navDestBlockedReason = function(slug) {{
    var loc = (setup.locations || {{}})[String(slug)] || {{}};
    if (loc.blocked_message) return loc.blocked_message;
    if (typeof setup.formatCanvasConditions === 'function' && loc.entry_conditions) {{
        var f = setup.formatCanvasConditions(loc.entry_conditions);
        if (f) return f;
    }}
    return 'Locked for now.';
}};

// Get NPCs whose declared [[npcs.schedules]] places them at this location right
// now AND who have a reachable affordable+valid canvas here. Schedule-only —
// no canvas-derived fallback (2026-05-25 doctrine tightening).
//
// Intake from selectNpcPortraitCanvasesForLocation (the renderer's pure pick
// helper) so the badge inherits the same substitutionOnly / cost / daily-cap
// Nav-card "someone's here" presence badge. SCHEDULE-OCCUPANCY — the SAME logic
// as the door / occupancy gate (setup.getNpcsAtLocation + the npc_at_location
// condition). An NPC counts as present at a destination if they are SCHEDULED
// there now, NOT if they own an interactable canvas there — so the map's
// presence and the locked-door / occupancy check always agree (a housemate
// showering shows at the bathroom AND blocks its door). The clickable portrait
// GRID (renderNpcPortraits) stays canvas-gated — only offer a click where there
// is an interaction (D72 dead-presence). Returns {{id,name,portrait}}.
setup.getNpcsPresentAtLocation = function(locationId) {{
    var result = [];
    try {{
        var npcs = (State.variables || {{}}).npcs || {{}};
        var slugMap = setup.npc_slug_map || {{}};
        var slugs = setup.getNpcsAtLocation(locationId);
        var seen = {{}};
        for (var pi = 0; pi < slugs.length; pi++) {{
            var slug = slugs[pi];
            if (seen[slug]) continue;
            seen[slug] = true;
            var npcUuid = slugMap[slug];
            var npc = npcUuid ? npcs[npcUuid] : null;
            if (!npc) continue;
            result.push({{
                id: npcUuid,
                name: npc.name,
                portrait: npc.portrait
            }});
        }}
    }} catch (e) {{
        // Fail gracefully - return empty array
    }}
    return result;
}};

// Select appropriate canvas per activity name with tiered progression logic
// Returns array of selected canvases (one per unique activity name)
// Logic:
// 1. Check if activity was triggered today -> skip entire group (one per day)
// 2. Find lowest priority unvisited tier -> return it (progression)
// 3. If all visited -> return highest priority only (replay mode)
setup.selectCanvasByPriority = function(canvasList) {{
    try {{
        if (!canvasList || canvasList.length === 0) return [];

        // Random-mode canvases: roll probability to decide if they appear as clickable options
        var filteredList = [];
        for (var f = 0; f < canvasList.length; f++) {{
            if ((canvasList[f].triggerMode || "manual") === "random") {{
                var chance = canvasList[f].chance || 0;
                if (Math.random() < chance) {{
                    filteredList.push(canvasList[f]);
                }}
            }} else {{
                filteredList.push(canvasList[f]);
            }}
        }}
        canvasList = filteredList;
        if (canvasList.length === 0) return [];

        // Check if any canvas has priority > 0 (new tiered system)
        var hasPriorities = false;
        for (var i = 0; i < canvasList.length; i++) {{
            if ((canvasList[i].priority || 0) > 0) {{
                hasPriorities = true;
                break;
            }}
        }}

        // Backward compatibility: if no priorities set, return all valid canvases
        if (!hasPriorities) {{
            var allValid = [];
            for (var j = 0; j < canvasList.length; j++) {{
                if (setup.isCanvasValid(canvasList[j])) {{
                    allValid.push(canvasList[j]);
                }}
            }}
            return allValid;
        }}

        // New tiered system: group by activity name
        var groups = {{}};
        for (var k = 0; k < canvasList.length; k++) {{
            var canvas = canvasList[k];
            var name = canvas.name || canvas.id;
            if (!groups[name]) groups[name] = [];
            groups[name].push(canvas);
        }}

        var selected = [];
        var groupNames = Object.keys(groups);

        for (var g = 0; g < groupNames.length; g++) {{
            var activityName = groupNames[g];
            var group = groups[activityName];

            // Get maxPerDay from first tier (all tiers share same limit)
            var maxPerDay = group[0].maxPerDay;

            // STEP 1: Check if activity was already triggered today
            // All tiers share the same daily limit at the activity level
            if (!setup.canTriggerActivity(activityName, maxPerDay)) {{
                continue; // Skip entire activity group
            }}

            // STEP 2: Filter to canvases valid for selection (schedule + conditions)
            // Uses isCanvasValidForSelection which excludes per-canvas daily limit
            var validCanvases = [];
            for (var v = 0; v < group.length; v++) {{
                if (setup.isCanvasValidForSelection(group[v])) {{
                    validCanvases.push(group[v]);
                }}
            }}
            if (validCanvases.length === 0) continue;

            // STEP 3: Find unvisited tiers (never triggered ever)
            var unvisited = [];
            for (var u = 0; u < validCanvases.length; u++) {{
                if (setup.isCanvasNew(validCanvases[u].id)) {{
                    unvisited.push(validCanvases[u]);
                }}
            }}

            if (unvisited.length > 0) {{
                // STEP 4a: Return LOWEST priority unvisited tier (progression)
                // Sort ascending so lowest priority comes first
                unvisited.sort(function(a, b) {{
                    return (a.priority || 0) - (b.priority || 0);
                }});
                selected.push(unvisited[0]);
            }} else {{
                // STEP 4b: All visited - return HIGHEST priority tier only (replay mode)
                // Sort descending so highest priority comes first
                validCanvases.sort(function(a, b) {{
                    return (b.priority || 0) - (a.priority || 0);
                }});
                selected.push(validCanvases[0]);
            }}
        }}

        return selected;
    }} catch (e) {{
        return [];
    }}
}};

// ===== Player-Initiated Interaction System =====
// Location screens show NPC portraits for repeatable activities (player chooses),
// auto-fire non-repeatable story events, and roll random encounters.

// Check if a non-repeatable story event should auto-fire at this location.
// Returns passage name to redirect to, or null if no story event fires.
setup.getStoryCanvasRedirect = function(locationId) {{
    try {{
        // Selection delegated to selectAutoFireCanvasForLocation so the
        // NEW badge can ask the same question without side effects. This
        // wrapper adds the markCanvasTriggered + random-encounter fallback
        // that only matter at actual entry time.
        var best = setup.selectAutoFireCanvasForLocation(locationId);
        if (best) {{
            setup.markCanvasTriggered(best.id);
            return best.passageName;
        }}
        // Random encounters intentionally NOT predicted by the badge —
        // they surface probabilistically; promising them would mislead.
        return setup.checkRandomEncounters(locationId);
    }} catch (e) {{
        return null;
    }}
}};

// Render NPC portrait grid for repeatable manual canvases at a location.
// Each NPC with a valid activity shows as a clickable circular portrait.
// Cost-blocked activities are shown greyed out with a cost badge.
// Returns HTML string.
setup.renderNpcPortraits = function(locationId) {{
    try {{
        var sv = State.variables;
        var helpData = setup.help_data || {{}};
        var locationCanvases = helpData.locationCanvases || {{}};
        var canvasList = locationCanvases[String(locationId)] || [];

        // Collect ALL valid repeatable manual canvases per NPC, separated by
        // affordability. Two-pass selection: gather first, then per NPC pick the
        // highest-priority canvas (preferring affordable over blocked). This handles
        // the multi-canvas-per-NPC overlap case where two surfaces (e.g. tier-2
        // supervised + tier-3 explicit) for the same NPC at the same location are
        // simultaneously valid — the higher-priority surface wins, matching the
        // semantics the canvas `priority` field already documents.
        // Composes with selectCanvasByPriority, which handles same-`name` tier
        // groups; this dedup handles different-name surfaces for the same NPC.
        // Affordable picks delegated to selectNpcPortraitCanvasesForLocation
        // (single source of truth shared with the NEW badge). Blocked
        // collection stays inline — only the renderer needs it (greyed
        // portraits with cost tag), the badge ignores blocked picks.
        var npcActivities = setup.selectNpcPortraitCanvasesForLocation(locationId);
        var npcBlockedAll = {{}};  // NPC slug -> array of valid cost-blocked canvases
        for (var i = 0; i < canvasList.length; i++) {{
            var c = canvasList[i];
            if (!c.isRepeatable) continue;
            if ((c.triggerMode || "manual") === "random") continue;
            if (!c.npcId) continue;
            if (npcActivities[c.npcId]) continue;  // NPC already has affordable pick
            if (!setup.isCanvasValid(c)) continue;
            if (!setup.canTriggerActivity(c.name || c.id, c.maxPerDay)) continue;
            if (!(c.costs && c.costs.length > 0 && !setup.checkCostsAffordable(c.costs))) continue;
            if (!npcBlockedAll[c.npcId]) npcBlockedAll[c.npcId] = [];
            npcBlockedAll[c.npcId].push(c);
        }}

        // Per NPC: blocked pick is highest-priority of the blocked-only group.
        // (Affordable picks already came in priority-sorted from the helper.)
        var npcBlocked = {{}};      // NPC slug -> canvas (blocked, highest priority)
        var sortByPriorityDesc = function(a, b) {{ return (b.priority || 0) - (a.priority || 0); }};
        for (var bSlug in npcBlockedAll) {{
            if (!npcActivities[bSlug]) {{
                npcBlockedAll[bSlug].sort(sortByPriorityDesc);
                npcBlocked[bSlug] = npcBlockedAll[bSlug][0];
            }}
        }}

        var allSlugs = Object.keys(npcActivities).concat(
            Object.keys(npcBlocked).filter(function(s) {{ return !npcActivities[s]; }})
        );

        // Schedule-only presence gate (2026-05-25 doctrine tightening) —
        // NPC must have declared [[npcs.schedules]] AND getNpcLocation must
        // place them at this location right now. NPCs without declared
        // schedules are suppressed (no canvas-derived fallback). This is the
        // INTERACTION surface (canvas-gated — only show a clickable portrait
        // where there's something to do). The nav-card presence badge
        // (getNpcsPresentAtLocation) is schedule-occupancy: the two agree for
        // normal hubs and intentionally differ only for hub-less occupancy rooms
        // (a showering housemate shows on the nav + blocks the door, but has no
        // clickable portrait inside).
        allSlugs = allSlugs.filter(function(slug) {{
            try {{
                var npcSched = (setup.npcSchedules || {{}})[slug];
                if (!npcSched || npcSched.length === 0) return false;
                var npcLoc = setup.getNpcLocation(slug);
                return npcLoc && npcLoc.location === locationId;
            }} catch (errFilter) {{
                return false;
            }}
        }});

        if (allSlugs.length === 0) return '';

        var html = '<div class="location-npcs">';
        for (var n = 0; n < allSlugs.length; n++) {{
            var slug = allSlugs[n];
            var isBlocked = !npcActivities[slug] && !!npcBlocked[slug];
            var activity = npcActivities[slug] || npcBlocked[slug];
            var npcUuid = (setup.npc_slug_map || {{}})[slug];
            var npcData = npcUuid ? (sv.npcs || {{}})[npcUuid] : null;
            var portrait = npcData ? (npcData.portrait || '') : '';
            var npcName = npcData ? (npcData.name || slug) : slug;
            var passageName = activity.passageName || '';
            if (!passageName) continue;

            // Per-portrait NEW/unlocked indicators removed 2026-05-25 —
            // NPC activities are always repeatable; capstone-only NEW lives
            // on the nav card; 🔓 unlocked-choices indicator removed entirely.
            var blockedClass = isBlocked ? ' npc-portrait-blocked' : '';

            html += '<div class="npc-portrait-card' + blockedClass + '">';
            // Link always points to the real canvas passage — cost gate in passage handles blocking
            html += '<a class="npc-portrait-link link-internal" data-passage="' + passageName + '">';

            // Resolve portrait path (video_path prefix embedded at generation time)
            var portraitSrc = portrait ? '{npc_portrait_prefix}' + portrait : '';

            if (portraitSrc) {{
                html += '<img class="npc-portrait-img" src="' + portraitSrc + '" alt="' + npcName + '">';
            }} else {{
                // Fallback: initial letter circle
                var initial = npcName.charAt(0).toUpperCase();
                html += '<div class="npc-portrait-placeholder">' + initial + '</div>';
            }}

            html += '<span class="npc-portrait-name">' + npcName + '</span>';

            // Cost badge for blocked portraits
            if (isBlocked && activity.costs && activity.costs.length > 0) {{
                var costTrait = String(activity.costs[0].trait);
                var costTraitDisplay = costTrait.charAt(0).toUpperCase() + costTrait.slice(1);
                html += '<span class="npc-badge npc-cost-badge">' + activity.costs[0].value + ' ' + costTraitDisplay + '</span>';
            }}

            html += '</a>';
            html += '</div>';
        }}
        html += '</div>';

        return html;
    }} catch (e) {{
        return '';
    }}
}};

// Render solo activity buttons (repeatable canvases with no NPC).
// Cost-blocked activities shown dimmed with cost tag.
// Returns HTML string.
setup.renderSoloActivities = function(locationId) {{
    try {{
        var helpData = setup.help_data || {{}};
        var locationCanvases = helpData.locationCanvases || {{}};
        var canvasList = locationCanvases[String(locationId)] || [];

        // Affordable picks delegated to selectSoloActivityCanvasesForLocation
        // (single source of truth shared with the NEW badge). Blocked +
        // cooldown-visible collections stay inline — only the renderer
        // needs them (greyed buttons / cooldown labels), badge ignores both.
        var soloActivities = setup.selectSoloActivityCanvasesForLocation(locationId);
        var soloBlocked = [];
        var soloCooldownBlocked = [];  // E21: opt-in cooldown-visible entries
        for (var i = 0; i < canvasList.length; i++) {{
            var c = canvasList[i];
            if (!c.isRepeatable) continue;
            if ((c.triggerMode || "manual") === "random") continue;
            if (c.npcId) continue;  // Has NPC = shown as portrait, not here
            if (!setup.isCanvasValid(c)) {{
                // E21 — if author opted in, surface as a grayed cooldown entry
                if (c.showWhenBlocked) {{
                    soloCooldownBlocked.push(c);
                }}
                continue;
            }}
            if (!setup.canTriggerActivity(c.name || c.id, c.maxPerDay)) {{
                if (c.showWhenBlocked) {{
                    soloCooldownBlocked.push(c);
                }}
                continue;
            }}
            if (c.costs && c.costs.length > 0 && !setup.checkCostsAffordable(c.costs)) {{
                soloBlocked.push(c);
            }}
            // affordable + cooldown-clear case is handled by the helper
        }}

        if (soloActivities.length === 0 && soloBlocked.length === 0 && soloCooldownBlocked.length === 0) return '';

        var html = '<div class="location-solo-activities">';
        // Affordable activities
        for (var s = 0; s < soloActivities.length; s++) {{
            var solo = soloActivities[s];
            var displayName = solo.displayName || solo.name || 'Activity';
            var passageName = solo.passageName || '';
            if (!passageName) continue;

            // Per-solo NEW indicator removed 2026-05-25 (capstone-only NEW doctrine).
            html += '<a class="link-internal solo-activity-btn" data-passage="' + passageName + '">' + displayName + '</a><br>';
        }}
        // Cost-blocked activities (dimmed with cost tag)
        for (var sb = 0; sb < soloBlocked.length; sb++) {{
            var blocked = soloBlocked[sb];
            var bDisplayName = blocked.displayName || blocked.name || 'Activity';
            var bPassageName = blocked.passageName || '';
            if (!bPassageName) continue;

            var costTag = '';
            if (blocked.costs && blocked.costs.length > 0) {{
                var ct = blocked.costs[0];
                var ctDisplay = String(ct.trait).charAt(0).toUpperCase() + String(ct.trait).slice(1);
                costTag = ' <span class="solo-cost-tag">(' + ct.value + ' ' + ctDisplay + ')</span>';
            }}
            html += '<a class="link-internal solo-activity-btn solo-activity-blocked" data-passage="' + bPassageName + '">' + bDisplayName + costTag + '</a><br>';
        }}
        // E21 — Cooldown-blocked activities (author opt-in via show_when_blocked).
        // Render as non-clickable dimmed text with cooldown message.
        for (var cd = 0; cd < soloCooldownBlocked.length; cd++) {{
            var cdItem = soloCooldownBlocked[cd];
            var cdDisplayName = cdItem.displayName || cdItem.name || 'Activity';
            var cdMessage = cdItem.cooldownMessage || 'Available again later';
            html += '<span class="solo-activity-cooldown">' + cdDisplayName +
                    ' — <em>' + cdMessage + '</em></span><br>';
        }}
        html += '</div>';

        return html;
    }} catch (e) {{
        return '';
    }}
}};

// Legacy compatibility wrapper — calls the new split functions
// Kept for any code that still references renderLocationCanvases
setup.renderLocationCanvases = function(locationId) {{
    try {{
        // Check for story event auto-fire first (legacy callers may not use getStoryCanvasRedirect)
        var redirect = setup.getStoryCanvasRedirect(locationId);
        if (redirect) {{
            return '<div class="auto-fire-redirect" data-passage="' + redirect + '"></div>';
        }}
        // Render player-choice content
        return (setup.renderNpcPortraits(locationId) || '') + (setup.renderSoloActivities(locationId) || '');
    }} catch (e) {{
        return '';
    }}
}};

// ===== Random Encounter System =====
// Check for random encounters when entering a location.
// Returns passage name to redirect to, or null if no encounter fires.
setup.checkRandomEncounters = function(locationId) {{
    try {{
        var sv = State.variables;
        var helpData = setup.help_data || {{}};
        var locationCanvases = helpData.locationCanvases || {{}};
        var canvasList = locationCanvases[String(locationId)] || [];

        // Coming back from a sidebar/info page is NOT an arrival — the player never walked in,
        // they closed a menu. Bail before the roll AND before the cooldown decrement below:
        // a re-render must neither draw a fresh encounter nor burn a tick of the cooldown that
        // spaces encounters out. Without this, "← Back" re-rolls at full chance every press
        // (a MISS records nothing), which yanked players into once-only scenes they never
        // entered the room for.
        //
        // This is the always-on FLOOR of the RTS rule below (RTS gates room ambients on
        // previous() == the adjacent room). It composes with, and does not replace, the
        // per-canvas opt-in entryOnlyFromPassages gate further down.
        var prevP = '';
        try {{ prevP = previous() || ''; }} catch (eP) {{}}
        if (prevP && setup.infoPages && setup.infoPages.indexOf(prevP) !== -1) return null;

        // Cooldown: after a random event fires, skip N visits before rolling again
        var cooldowns = sv.game_state.random_cooldowns = sv.game_state.random_cooldowns || {{}};
        var locKey = String(locationId);
        if (cooldowns[locKey] && cooldowns[locKey] > 0) {{
            cooldowns[locKey]--;
            return null;
        }}

        // Filter to random-mode canvases only
        var randomCanvases = [];
        for (var i = 0; i < canvasList.length; i++) {{
            if (canvasList[i].triggerMode === "random") {{
                randomCanvases.push(canvasList[i]);
            }}
        }}
        if (randomCanvases.length === 0) return null;

        // Filter to valid canvases (schedule, conditions, repeatability)
        var valid = [];
        for (var j = 0; j < randomCanvases.length; j++) {{
            if (setup.isCanvasValid(randomCanvases[j])) {{
                valid.push(randomCanvases[j]);
            }}
        }}
        if (valid.length === 0) return null;

        // Check activity-level daily limit (shared across same-named canvases)
        var afterLimit = [];
        for (var k = 0; k < valid.length; k++) {{
            var actName = valid[k].name || valid[k].id;
            var maxPerDay = valid[k].maxPerDay;
            if (setup.canTriggerActivity(actName, maxPerDay)) {{
                afterLimit.push(valid[k]);
            }}
        }}
        if (afterLimit.length === 0) return null;

        // L2-2 — Lane 2 anti-toggle cooldown: filter by previous-passage gate.
        // RTS doctrine: random encounters only fire when entered FROM the hub
        // (not from sub-passage returns). Author writes location slugs in TOML's
        // `entry_only_from`; build translates → runtime passage names; engine
        // compares to SugarCube's `previous()`. Empty list = no gate (default).
        var prevPassage = '';
        try {{ prevPassage = previous() || ''; }} catch (eP) {{}}
        var afterEntryGate = [];
        for (var n = 0; n < afterLimit.length; n++) {{
            var canv = afterLimit[n];
            var entryFrom = canv.entryOnlyFromPassages || [];
            if (entryFrom.length === 0) {{
                afterEntryGate.push(canv);  // no gate = always allowed (default)
            }} else if (prevPassage && entryFrom.indexOf(prevPassage) !== -1) {{
                afterEntryGate.push(canv);  // gate matched
            }}
            // else: gate failed, canvas skipped this entry
        }}
        if (afterEntryGate.length === 0) return null;

        // Phase A (2026-05-14) — NPC presence gate. When canvas declares
        // requiresNpc, the named NPC must be co-located with the player at
        // current time per setup.getNpcLocation(). Canvases without
        // requiresNpc are unaffected. ANDs with all preceding gates.
        var afterNpcGate = [];
        for (var np = 0; np < afterEntryGate.length; np++) {{
            var canvNpc = afterEntryGate[np];
            if (!canvNpc.requiresNpc) {{
                afterNpcGate.push(canvNpc);
                continue;
            }}
            var npcLoc = setup.getNpcLocation(canvNpc.requiresNpc);
            if (npcLoc && npcLoc.location === locationId) {{
                afterNpcGate.push(canvNpc);
            }}
            // else: NPC not here — canvas skipped
        }}
        if (afterNpcGate.length === 0) return null;

        // Shuffle for fairness (Fisher-Yates)
        var shuffled = afterNpcGate.slice();
        for (var s = shuffled.length - 1; s > 0; s--) {{
            var r = Math.floor(Math.random() * (s + 1));
            var temp = shuffled[s];
            shuffled[s] = shuffled[r];
            shuffled[r] = temp;
        }}

        // Roll probability for each candidate
        for (var m = 0; m < shuffled.length; m++) {{
            var canvas = shuffled[m];
            var chance = canvas.chance || 0;
            if (Math.random() < chance) {{
                // Hit — mark as triggered, set cooldown, and return passage name
                setup.markCanvasTriggered(canvas.id);
                cooldowns[locKey] = 3;
                return canvas.passageName;
            }}
        }}

        return null; // No encounter fired
    }} catch (e) {{
        return null; // Fail safe
    }}
}};

// PRD 25 — Lane 3 dispatcher substitution. Called via <<set>>+<<goto>> from
// the top of a parent canvas's emitted passage body (per §5.4 injection).
// Walks the canvas's substitution rules in declaration order; for each rule
// evaluates target validity + optional extra conditions + rolls dice. First
// rule with all gates passing returns the target passage name (caller uses
// <<goto>> to switch). If no rule fires, returns null and parent renders.
//
// IMPORTANT: returns the target passage NAME (string), not boolean. SugarCube's
// <<script>> macro doesn't allow naked `return` statements, so the original
// PRD spec ("if (...) return") fails at runtime. The <<set>>+<<goto>> pattern
// works around this and is the canonical SugarCube way to do conditional nav.
//
// Doctrine: doc 24 §7 + PRD 25 §3 (Pattern A — independent rolls, first-match).
// Doc 69 Item 1 (2026-05-27) — Pattern B `exclusive_group` extension:
// rules sharing an exclusive_group string share ONE dice roll (mutual
// exclusion via cumulative bucket partition); failed-condition in a claimed
// slot falls to solo (does NOT promote to next rule in the group). Groups
// process FIRST per LO Q2 decision; if no group fires, fall through to
// Pattern A independent rules. Fail-open on errors.
setup.checkAndSubstituteCanvas = function(parentCanvasId) {{
    try {{
        var subs = (setup.canvasSubstitutions || {{}})[parentCanvasId] || [];
        if (subs.length === 0) return null;
        // Resolve current location once; needed for the NPC presence gate.
        var sv = State.variables || {{}};
        var currentLocation = (sv.player && sv.player.current_location) || null;

        // Helper: validate target + conditions + requiresNpc gate for a rule.
        // Returns the resolved target (truthy) or null.
        var _tryRule = function(s) {{
            var target = setup.getCanvasById(s.target_canvas_id);
            if (!target) return null;
            if (!setup.isCanvasValid(target)) return null;
            if (s.conditions && !setup.triggerConditionsSatisfied(s.conditions)) return null;
            if (target.requiresNpc) {{
                var subNpcLoc = setup.getNpcLocation(target.requiresNpc);
                if (!subNpcLoc || subNpcLoc.location !== currentLocation) return null;
            }}
            return target;
        }};

        // ── Doc 69 Item 1 — partition substitution rules by exclusive_group.
        var groups = {{}};            // group_name → [rule, rule, ...] in declaration order
        var groupOrder = [];          // first-seen order of group names (for deterministic iteration)
        var independentRules = [];    // rules without exclusive_group
        for (var pi = 0; pi < subs.length; pi++) {{
            var pr = subs[pi];
            if (pr && pr.exclusive_group) {{
                var gn = String(pr.exclusive_group);
                if (!groups[gn]) {{
                    groups[gn] = [];
                    groupOrder.push(gn);
                }}
                groups[gn].push(pr);
            }} else {{
                independentRules.push(pr);
            }}
        }}

        // ── Pattern B groups first: single dice per group; cumulative buckets.
        // If dice falls in a slot but the rule's target/conditions/requiresNpc
        // fail, FALL THROUGH TO SOLO (return null) — do not promote next rule.
        // This is the load-bearing Pattern B semantic per Doc 69 §3.4.
        for (var gi = 0; gi < groupOrder.length; gi++) {{
            var groupName = groupOrder[gi];
            var groupRules = groups[groupName];
            var groupDice = Math.random();
            var cumulativeChance = 0;
            for (var gri = 0; gri < groupRules.length; gri++) {{
                var gs = groupRules[gri];
                cumulativeChance += (gs.chance || 0);
                if (groupDice < cumulativeChance) {{
                    // Dice claimed this slot. Validate target+conditions.
                    var groupTarget = _tryRule(gs);
                    if (groupTarget) {{
                        setup.markCanvasTriggered(groupTarget.id);
                        return groupTarget.passageName;
                    }}
                    // Claimed slot failed conditions → fall to solo, not next rule.
                    return null;
                }}
            }}
            // Dice fell outside all buckets in this group → continue to next group.
        }}

        // ── Pattern A independent rules: each rule rolls own dice; first match wins.
        for (var i = 0; i < independentRules.length; i++) {{
            var s = independentRules[i];
            var target = _tryRule(s);
            if (!target) continue;
            if (Math.random() < (s.chance || 0)) {{
                setup.markCanvasTriggered(target.id);
                return target.passageName;
            }}
        }}
        return null;
    }} catch (e) {{
        return null;  // Fail-open: don't break gameplay if substitution misfires
    }}
}};

// Time advancement functions
window.advanceTime = function(minutes) {{
    // Add minutes to current time
    State.variables.game_state.time_state.current_minute += minutes;

    // Handle minute/hour rollover
    while (State.variables.game_state.time_state.current_minute >= 60) {{
        State.variables.game_state.time_state.current_minute -= 60;
        State.variables.game_state.time_state.current_hour += 1;
    }}

    // Handle day rollover
    while (State.variables.game_state.time_state.current_hour >= 24) {{
        State.variables.game_state.time_state.current_hour -= 24;
        advanceDay();
    }}

    // Expire temporary modifiers (checked every time advance, not just day rollover)
    var mods = (State.variables.game_state || {{}}).active_modifiers;
    if (mods) {{
        var ts = State.variables.game_state.time_state;
        for (var mk in mods) {{
            var m = mods[mk];
            if (ts.day > m.expires_day ||
                (ts.day === m.expires_day && ts.current_hour >= m.expires_hour)) {{
                delete mods[mk];
            }}
        }}
    }}

    // Update display
    updateTimeDisplay();
}};

// The sidebar wait buttons' entry point: advance the clock, then COMMIT a moment.
//
// advanceTime() deliberately does NOT commit — deductLocationCosts() calls it mid-navigation
// from :passagestart, where the in-flight navigation commits for us and an extra moment would
// be spurious. But a wait BUTTON navigates nowhere, so its change would live only in the
// active moment: Save (which serializes the history) and a page refresh would both replay the
// OLD clock. Committing here publishes it. This covers the whole daily tick too — advanceDay,
// trait decay, arousal rise and bank interest all run inside advanceTime.
window.waitTime = function(minutes) {{
    window.advanceTime(minutes);
    if (setup.commitMoment) {{ setup.commitMoment(); }}
}};

window.advanceDay = function() {{
    const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
    const currentIndex = days.indexOf(State.variables.game_state.time_state.current_day);
    const nextIndex = (currentIndex + 1) % 7;
    State.variables.game_state.time_state.current_day = days[nextIndex];

    // Increment numeric day counter for days_since_flag conditions
    State.variables.game_state.time_state.day += 1;

    // New week starts on Monday
    if (nextIndex === 0) {{
        State.variables.game_state.time_state.current_week += 1;
    }}
{"" if not self.rent_enabled else '''
    // Rent comes due on its configured weekday (default Monday), once per week,
    // only after start_after_flag is met (if configured). advanceDay() runs one
    // day per call, so this matches every occurrence of due_day as days pass.
    var dueDay = setup.rent_due_day || "Monday";
    if (days[nextIndex] === dueDay && setup.rent_enabled) {{
        var rs = State.variables.game_state.rent_state;
        var flagOk = !setup.rent_start_after_flag || (State.variables.flags && State.variables.flags[setup.rent_start_after_flag]);
        if (rs && flagOk) {{
            rs.is_due = true;
        }}
    }}
'''}
    // Check pass expirations
    if (setup.passes && setup.passes.length > 0) {{
        var gsPasses = (State.variables.game_state || {{}}).passes || {{}};
        var curDay = State.variables.game_state.time_state.day;
        for (var pid in gsPasses) {{
            var pState = gsPasses[pid];
            if (pState && curDay > pState.expires_day) {{
                var pConf = setup.passes_map[pid];
                if (pConf && typeof setup.showNotification === 'function') {{
                    setup.showNotification((pConf.icon || '') + ' ' + pConf.name + ' has expired.');
                }}
                delete gsPasses[pid];
            }}
        }}
    }}

    // E20 — snapshot decaying traits BEFORE decay applies. The render-time
    // decay-warning widget compares snapshot vs current to detect "this
    // trait dropped today" so it can show an amber banner.
    (function _snapshotDecayingTraits() {{
        if (!State.variables.last_day_snapshot) {{
            State.variables.last_day_snapshot = {{}};
        }}
        var snap = State.variables.last_day_snapshot;
        // Player traits
        if (setup.player_trait_decay) {{
            var pt = State.variables.player && State.variables.player.core_traits;
            if (pt) {{
                for (var ptKey in setup.player_trait_decay) {{
                    if (typeof pt[ptKey] === "number") {{
                        snap["player::" + ptKey] = pt[ptKey];
                    }}
                }}
            }}
        }}
        // NPC traits
        if (setup.npc_trait_decay) {{
            for (var npcUuid in setup.npc_trait_decay) {{
                var npc = State.variables.npcs && State.variables.npcs[npcUuid];
                if (!npc || !npc.core_traits) continue;
                var dc = setup.npc_trait_decay[npcUuid];
                for (var traitName in dc) {{
                    if (typeof npc.core_traits[traitName] === "number") {{
                        snap["npc:" + npcUuid + ":" + traitName] = npc.core_traits[traitName];
                    }}
                }}
            }}
        }}
    }})();

    // Trait decay: reduce NPC traits if player didn't interact today
    if (setup.npc_trait_decay && Object.keys(setup.npc_trait_decay).length > 0) {{
        var interacted = State.variables.npc_interacted_today || {{}};
        for (var npcId in setup.npc_trait_decay) {{
            if (interacted[npcId]) continue; // Player interacted, skip decay
            var decayConfig = setup.npc_trait_decay[npcId];
            var npcData = State.variables.npcs[npcId];
            if (!npcData || !npcData.core_traits) continue;
            for (var traitName in decayConfig) {{
                var decayAmount = decayConfig[traitName];
                if (typeof npcData.core_traits[traitName] === 'number' && decayAmount > 0) {{
                    npcData.core_traits[traitName] = Math.max(0, npcData.core_traits[traitName] - decayAmount);
                }}
            }}
        }}
    }}
    // Player trait decay: applied every in-game day, no skip logic (player always "participates")
    if (setup.player_trait_decay && Object.keys(setup.player_trait_decay).length > 0) {{
        var _pt = State.variables.player && State.variables.player.core_traits;
        if (_pt) {{
            for (var _ptKey in setup.player_trait_decay) {{
                var _ptDecay = setup.player_trait_decay[_ptKey];
                if (typeof _pt[_ptKey] === 'number' && _ptDecay > 0) {{
                    _pt[_ptKey] = Math.max(0, _pt[_ptKey] - _ptDecay);
                }}
            }}
        }}
    }}
    // [engine.daily_tick] hook — silently apply configured flag effects
    // (no notification queueing; daily clears are bookkeeping, not events).
    if (setup.daily_tick && setup.daily_tick.flagEffects && setup.daily_tick.flagEffects.length > 0) {{
        var dtEffs = setup.daily_tick.flagEffects;
        for (var dti = 0; dti < dtEffs.length; dti++) {{
            var dtFe = dtEffs[dti];
            // doc 45 G6 — optional per-effect condition gate
            if (dtFe.conditions && !setup.triggerConditionsSatisfied(dtFe.conditions)) continue;
            try {{
                window.applyFlagEffect(
                    dtFe.targetType || 'player',
                    dtFe.npcId || null,
                    dtFe.flag,
                    dtFe.op || 'set'
                );
            }} catch (e) {{
                // ignore — keep day-rollover resilient
            }}
        }}
    }}
    // [engine.daily_tick] hook — apply configured trait deltas (doc 40).
    // This is the RTS arousal "daily auto-rise": e.g. player arousal +1 (cap 10),
    // NPC arousal +1 (cap 3). Reuses the standard trait-effect path so clamp/cap
    // behave exactly like choice/canvas effects.
    if (setup.daily_tick && setup.daily_tick.traitEffects && setup.daily_tick.traitEffects.length > 0) {{
        var dtTraitEffs = setup.daily_tick.traitEffects;
        for (var dtti = 0; dtti < dtTraitEffs.length; dtti++) {{
            var dtTe = dtTraitEffs[dtti];
            // doc 45 G6 — optional per-effect condition gate
            if (dtTe.conditions && !setup.triggerConditionsSatisfied(dtTe.conditions)) continue;
            try {{
                setup.applyAndNotifyTrait(
                    dtTe.targetType || 'player',
                    dtTe.npcId || null,
                    dtTe.trait,
                    dtTe.op || 'add',
                    Number(dtTe.value || 0),
                    (dtTe.clamp === undefined || dtTe.clamp === null) ? false : dtTe.clamp,
                    (dtTe.cap === undefined) ? null : dtTe.cap
                );
            }} catch (e) {{
                // ignore — keep day-rollover resilient
            }}
        }}
    }}
    // doc 45 G5 — decrement the scheduled-event queue; fire + remove at 0.
    if (State.variables.game_state && Array.isArray(State.variables.game_state.scheduled)) {{
        var _sched = State.variables.game_state.scheduled;
        var _kept = [];
        for (var _si = 0; _si < _sched.length; _si++) {{
            var _ev = _sched[_si];
            _ev.daysLeft = Number(_ev.daysLeft || 0) - 1;
            if (_ev.daysLeft <= 0) {{ setup.fireScheduledEvent(_ev); }}
            else {{ _kept.push(_ev); }}
        }}
        State.variables.game_state.scheduled = _kept;
    }}
    // doc 45 G9 — decrement fast-job cooldowns
    if (State.variables.game_state && State.variables.game_state.fast_jobs) {{
        var _cds = State.variables.game_state.fast_jobs.cooldowns || {{}};
        for (var _jk in _cds) {{ if (_cds[_jk] > 0) _cds[_jk] -= 1; }}
    }}
    // doc 45 G9 — daily bank interest
    if (setup.bank_data && State.variables.game_state && State.variables.game_state.bank) {{
        var _bk = State.variables.game_state.bank;
        var _rate = Number(setup.bank_data.interest_rate || 0);
        if (_bk.balance > 0 && _rate > 0) {{
            var _gain = Math.floor(_bk.balance * _rate);
            if (_gain > 0) {{ _bk.balance += _gain; if (typeof createNotification === 'function') {{ try {{ createNotification('Bank interest +$' + _gain, 'info'); }} catch(e) {{}} }} }}
        }}
    }}
    // Reset daily NPC interaction tracking
    State.variables.npc_interacted_today = {{}};
}};

window.updateTimeDisplay = function() {{
    // Format time for 12-hour display
    const hour = State.variables.game_state.time_state.current_hour;
    const minute = State.variables.game_state.time_state.current_minute;
    const displayHour = hour === 0 ? 12 : hour > 12 ? hour - 12 : hour;
    const ampm = hour < 12 ? 'AM' : 'PM';
    const formattedTime = displayHour + ':' + (minute < 10 ? '0' : '') + minute + ' ' + ampm;

    // Update time display
    const timeElement = document.getElementById('time-display');
    if (timeElement) {{
        timeElement.textContent = formattedTime;
    }}

    // Update current day
    const currentDayElement = document.getElementById('current-day');
    if (currentDayElement) {{
        currentDayElement.textContent = State.variables.game_state.time_state.current_day;
    }}

    // Update day count (dev mode only - element may not exist)
    const dayCountElement = document.getElementById('day-count');
    if (dayCountElement) {{
        dayCountElement.textContent = 'Day ' + State.variables.game_state.time_state.day;
    }}

    // Update sidebar countdown items
    if (setup.sidebar_items) {{
        for (var si = 0; si < setup.sidebar_items.length; si++) {{
            var item = setup.sidebar_items[si];
            if (item.type === 'countdown') {{
                var el = document.getElementById('sidebar-countdown-' + si);
                if (el) {{
                    var daysLeft = item.total_days - State.variables.game_state.time_state.day + 1;
                    if (daysLeft > 1) {{
                        el.textContent = daysLeft + ' ' + item.label;
                    }} else if (daysLeft === 1) {{
                        el.textContent = 'Tomorrow is ' + item.label.replace('days until ', '');
                    }} else if (daysLeft === 0) {{
                        el.textContent = 'Today is ' + item.label.replace('days until ', '');
                    }} else {{
                        el.textContent = item.label.replace('days until ', '') + ' has passed';
                    }}
                }}
            }}
        }}
    }}

    // Update pass displays
    if (setup.passes) {{
        for (var pi = 0; pi < setup.passes.length; pi++) {{
            var passEl = document.getElementById('pass-display-' + setup.passes[pi].id);
            if (passEl) {{
                var rem = setup.getPassDaysRemaining(setup.passes[pi].id);
                if (rem >= 0) {{
                    passEl.textContent = (setup.passes[pi].icon || '') + ' ' + setup.passes[pi].name + ': ' + rem + 'd';
                }} else {{
                    passEl.style.display = 'none';
                }}
            }}
        }}
    }}

    // Update inventory displays
    if (setup.items) {{
        for (var ii = 0; ii < setup.items.length; ii++) {{
            var invEl = document.getElementById('inventory-display-' + setup.items[ii].id);
            if (invEl) {{
                var cnt = setup.getItemCount(setup.items[ii].id);
                if (cnt > 0) {{
                    invEl.textContent = (setup.items[ii].icon || '') + ' ' + setup.items[ii].name + ': ' + cnt;
                    invEl.style.display = '';
                }} else {{
                    invEl.style.display = 'none';
                }}
            }}
        }}
    }}
}};

// ===== Trait Helpers =====
window._traitClamp = function(v, min, max) {{
  v = Number(v);
  if (isNaN(v)) {{ v = 0; }}
  if (min !== undefined && v < min) v = min;
  if (max !== undefined && v > max) v = max;
  return v;
}};

window.applyTraitEffect = function(targetType, npcId, trait, op, val, clampFlag, cap) {{
  try {{
    var sv = State.variables;
    if (!sv) return;

    // Resolve NPC slug to UUID
    if (targetType === 'npc' && npcId) {{
      npcId = setup.resolveNpcId(npcId);
    }}

    // Resolve target object
    var traitsObj = null;
    if (targetType === 'player') {{
      sv.player = sv.player || {{}};
      sv.player.core_traits = sv.player.core_traits || {{}};
      traitsObj = sv.player.core_traits;
    }} else if (targetType === 'npc') {{
      sv.npcs = sv.npcs || {{}};
      var npc = sv.npcs[String(npcId)] || null;
      if (!npc) return; // Unknown NPC
      npc.core_traits = npc.core_traits || {{}};
      traitsObj = npc.core_traits;
    }} else {{
      return; // Unknown target type
    }}

    // Normalize inputs
    var key = String(trait);
    var current = Number(traitsObj[key]);
    if (isNaN(current)) current = 0;
    var value = Number(val);
    if (isNaN(value)) value = 0;

    // Apply operation
    var next = current;
    if (op === 'add') {{
      next = current + value;
    }} else if (op === 'set') {{
      next = value;
    }} else {{
      // Unknown op; do nothing
      return;
    }}

    // Clamp 0-100 if requested (default true)
    if (clampFlag === undefined || clampFlag === null) {{ clampFlag = true; }}
    if (clampFlag) {{
      next = window._traitClamp(next, 0, 100);
    }}
    // Apply cap if provided
    if (cap !== undefined && cap !== null) {{
      var capNum = Number(cap);
      if (!isNaN(capNum)) {{
        if (next > capNum) next = Math.max(current, capNum);
      }}
    }}

    traitsObj[key] = next;
  }} catch (e) {{
    // Ignore to avoid breaking navigation
  }}
}};

// ===== Flag Helpers =====
// op: "set" (default) | "unset" | "toggle"
//   - set:    flag = true,  flags_meta updated
//   - unset:  flag = false, flags_meta untouched (preserves last set_day for re-arming)
//   - toggle: flag = !flag, flags_meta updated only when new value is true
window.applyFlagEffect = function(targetType, npcId, flag, op) {{
  try {{
    var sv = State.variables;
    if (!sv) return;
    op = op || 'set';

    // Resolve NPC slug to UUID
    if (targetType === 'npc' && npcId) {{
      npcId = setup.resolveNpcId(npcId);
    }}

    var key = String(flag);
    var currentDay = (sv.game_state && sv.game_state.time_state) ? sv.game_state.time_state.day : 1;

    var flagsObj = null;
    var metaObj = null;
    if (targetType === 'player') {{
      sv.flags = sv.flags || {{}};
      sv.flags_meta = sv.flags_meta || {{}};
      flagsObj = sv.flags;
      metaObj = sv.flags_meta;
    }} else if (targetType === 'npc') {{
      sv.npcs = sv.npcs || {{}};
      var npc = sv.npcs[String(npcId)];
      if (!npc) return;
      npc.flags = npc.flags || {{}};
      npc.flags_meta = npc.flags_meta || {{}};
      flagsObj = npc.flags;
      metaObj = npc.flags_meta;
    }} else {{
      return;
    }}

    if (op === 'unset') {{
      flagsObj[key] = false;
      // Do NOT clear flags_meta — set_day stays for days_since_flag math.
      return;
    }}
    if (op === 'toggle') {{
      var newVal = !flagsObj[key];
      flagsObj[key] = newVal;
      if (newVal === true) {{
        metaObj[key] = {{ set_day: currentDay }};
      }}
      return;
    }}
    // Default: 'set' (and any unrecognized op falls through to set for safety).
    flagsObj[key] = true;
    metaObj[key] = {{ set_day: currentDay }};
  }} catch (e) {{
    // ignore
  }}
}};

// ========== EFFECT NOTIFICATION SYSTEM ==========

// Pending effects to show
setup.pendingEffects = [];

// Get current trait value helper
setup.getTraitValue = function(targetType, npcId, trait) {{
  var sv = State.variables;
  // Resolve NPC slug to UUID
  if (targetType === 'npc' && npcId) {{
    npcId = setup.resolveNpcId(npcId);
  }}
  if (targetType === 'player') {{
    return (sv.player && sv.player.core_traits) ? (sv.player.core_traits[trait] || 0) : 0;
  }} else if (targetType === 'npc' && npcId) {{
    var npc = sv.npcs ? sv.npcs[String(npcId)] : null;
    return (npc && npc.core_traits) ? (npc.core_traits[trait] || 0) : 0;
  }}
  return 0;
}};

// Apply trait and queue notification
setup.applyAndNotifyTrait = function(targetType, npcId, trait, op, val, clampFlag, cap) {{
  var oldVal = setup.getTraitValue(targetType, npcId, trait);
  applyTraitEffect(targetType, npcId, trait, op, val, clampFlag, cap);
  var newVal = setup.getTraitValue(targetType, npcId, trait);
  var delta = newVal - oldVal;
  // E9: log stage advancement when a player <slug>_stage trait moves upward.
  // Keyed by NPC slug (matches setup.npc_arc_stages registry). Records the
  // current in-game day. Only positive deltas count — a `set` op that
  // decreases the value isn't an advancement.
  if (targetType === 'player' && delta > 0 && setup.npc_arc_stages) {{
    var stageMatch = /^([a-z_]+)_stage$/.exec(trait);
    if (stageMatch && setup.npc_arc_stages[stageMatch[1]]) {{
      var sv = State.variables;
      sv.game_state.stage_advancement_log = sv.game_state.stage_advancement_log || {{}};
      var currentDay = (sv.game_state.time_state && sv.game_state.time_state.day) || 1;
      sv.game_state.stage_advancement_log[stageMatch[1]] = currentDay;
    }}
  }}
  if (delta !== 0) {{
    var npcName = '';
    if (targetType === 'npc' && npcId) {{
      npcId = setup.resolveNpcId(npcId);
      var npc = State.variables.npcs ? State.variables.npcs[String(npcId)] : null;
      npcName = npc ? (npc.name || npcId) : npcId;
    }}
    setup.pendingEffects.push({{
      type: 'trait',
      name: npcName,
      trait: trait,
      delta: delta
    }});
  }}
}};

// Apply flag and queue notification.
// op: "set" (default) | "unset" | "toggle" — passed through to applyFlagEffect.
setup.applyAndNotifyFlag = function(targetType, npcId, flag, op) {{
  op = op || 'set';
  // Resolve NPC slug to UUID
  if (targetType === 'npc' && npcId) {{
    npcId = setup.resolveNpcId(npcId);
  }}
  applyFlagEffect(targetType, npcId, flag, op);
  var npcName = '';
  if (targetType === 'npc' && npcId) {{
    var npc = State.variables.npcs ? State.variables.npcs[String(npcId)] : null;
    npcName = npc ? (npc.name || npcId) : npcId;
  }}
  setup.pendingEffects.push({{
    type: 'flag',
    name: npcName,
    flag: flag,
    op: op
  }});
}};

// doc 45 G4 — quest primitive: mutate $game_state.quests[id] = {{active,progress,completed}}
setup.applyQuestEffect = function(questId, op, step) {{
  if (!questId) return;
  var sv = State.variables;
  if (!sv.game_state) sv.game_state = {{}};
  var qs = sv.game_state.quests = sv.game_state.quests || {{}};
  var st = qs[questId] = qs[questId] || {{ active: false, progress: 0, completed: false }};
  op = op || 'start';
  if (op === 'start') {{ st.active = true; st.completed = false; if (st.progress == null) st.progress = 0; }}
  else if (op === 'update') {{ st.active = true; st.progress = (step != null ? Number(step) : (st.progress || 0) + 1); }}
  else if (op === 'complete') {{ st.completed = true; st.active = false; }}
  else if (op === 'cancel') {{ st.active = false; }}
  setup.pendingEffects = setup.pendingEffects || [];
  setup.pendingEffects.push({{ type: 'quest', quest: questId, op: op }});
}};
setup.isQuestActive = function(questId) {{
  var qs = ((State.variables.game_state || {{}}).quests) || {{}};
  return !!(qs[questId] && qs[questId].active);
}};
setup.isQuestCompleted = function(questId) {{
  var qs = ((State.variables.game_state || {{}}).quests) || {{}};
  return !!(qs[questId] && qs[questId].completed);
}};

// doc 45 G7 — derive a discrete corruption LEVEL (0-4) from raw corruption
// points via tier thresholds (RTS default [0,5,15,30,45]; override via
// setup.corruption_tiers). RTS getCorruptionLevel equivalent.
setup.getCorruptionLevel = function() {{
  var pts = (((State.variables.player || {{}}).core_traits || {{}}).corruption) || 0;
  var tiers = setup.corruption_tiers || [0, 5, 15, 30, 45];
  var lvl = 0;
  for (var i = 0; i < tiers.length; i++) {{ if (pts >= tiers[i]) lvl = i; }}
  return lvl;
}};

// doc 45 G5 — delay queue: push a {{daysLeft, action, ...}} onto $game_state.scheduled
setup.scheduleEvent = function(entry) {{
  if (!entry || !entry.action) return;
  var sv = State.variables;
  if (!sv.game_state) sv.game_state = {{}};
  var q = sv.game_state.scheduled = sv.game_state.scheduled || [];
  q.push({{
    daysLeft: Math.max(0, Number(entry.delayDays != null ? entry.delayDays : 1)),
    action: entry.action,
    flag: entry.flag || null,
    quest: entry.quest || null,
    conversation: entry.conversation || null,
    step: (entry.step != null ? entry.step : null)
  }});
}};
setup.fireScheduledEvent = function(e) {{
  try {{
    if (e.action === 'set_flag' && e.flag) {{ window.applyFlagEffect('player', null, e.flag, 'set'); }}
    else if (e.action === 'start_quest' && e.quest) {{ setup.applyQuestEffect(e.quest, 'start', null); }}
    else if (e.action === 'trigger_conversation' && e.conversation) {{ window.applyFlagEffect('player', null, 'scheduled_' + e.conversation, 'set'); }}
  }} catch (err) {{}}
}};

// Show notification and clear
setup.showEffectNotification = function() {{
  var effects = setup.pendingEffects;
  if (!effects || effects.length === 0) return;

  // Separate gated-action notifications (S4) from regular effect lines.
  // Gated actions render as their own warning toast, distinct from the
  // green effect-toast — they publish a threshold the player didn't meet,
  // not an effect that fired. Mirrors RTS <<NotifyCorruption N>> pattern.
  var lines = [];
  var gatedMessages = [];
  for (var i = 0; i < effects.length; i++) {{
    var eff = effects[i];
    if (eff.type === 'trait') {{
      var sign = eff.delta > 0 ? '+' : '';
      var traitDisplay = eff.trait.charAt(0).toUpperCase() + eff.trait.slice(1);
      var prefix = eff.name ? (eff.name + "'s ") : '';
      lines.push(sign + eff.delta + ' ' + prefix + traitDisplay);
    }} else if (eff.type === 'flag') {{
      var flagDisplay = eff.flag.replace(/_/g, ' ');
      flagDisplay = flagDisplay.charAt(0).toUpperCase() + flagDisplay.slice(1);
      lines.push('🔓 ' + flagDisplay);
    }} else if (eff.type === 'wardrobe') {{
      lines.push('👗 New item: ' + eff.name);
    }} else if (eff.type === 'quest') {{
      lines.push('📜 ' + (eff.op === 'complete' ? 'Quest complete' : eff.op === 'cancel' ? 'Quest dropped' : 'Quest updated'));
    }} else if (eff.type === 'gated_action') {{
      gatedMessages.push(eff.message);
    }}
  }}

  // Emit the standard effect-toast for trait/flag/wardrobe lines.
  if (lines.length > 0) {{
    var html = '<div class="effect-toast">' + lines.join(' • ') + '</div>';
    jQuery('body').append(html);
    setTimeout(function() {{
      jQuery('.effect-toast').remove();
    }}, 2000);
  }}

  // Emit a separate warning toast for each gated_action — these are
  // threshold-publishers, not effect summaries. Slightly longer dwell so
  // the player has time to read the in-character explanation.
  if (gatedMessages.length > 0) {{
    var gatedHtml = '<div class="effect-toast notify-warning">' + gatedMessages.map(function(m) {{
      // Escape any embedded HTML in the author-supplied message.
      var div = document.createElement('div');
      div.textContent = m;
      return div.innerHTML;
    }}).join('<br>') + '</div>';
    jQuery('body').append(gatedHtml);
    setTimeout(function() {{
      jQuery('.notify-warning').remove();
    }}, 3000);
  }}

  setup.pendingEffects = [];
}};

// S4 — Queue a gated-action notification (threshold-publisher), to be
// rendered as a warning toast on next showEffectNotification() call.
// Use case: player clicks a locked choice; this fires the in-character
// threshold message ("I'd need to be more comfortable — at least 25
// corruption — before I could.") without actually navigating.
setup.queueGatedNotification = function(message) {{
  setup.pendingEffects = setup.pendingEffects || [];
  setup.pendingEffects.push({{ type: 'gated_action', message: String(message || '') }});
}};

// ========== STORY JOURNAL SYSTEM ==========

// Detect current story position based on story arc and game state
setup.detectStoryPosition = function() {{
    var arc = setup.story_arc || {{}};
    var result = {{
        current_chapter: null,
        completed_nodes: [],
        available_nodes: [],
        locked_nodes: [],
        active_groups: [],
        is_stuck: false,
        progress_percent: 0
    }};

    if (!arc.nodes || arc.nodes.length === 0) {{
        // Use auto-inference if no story arc defined
        return setup.autoInferStoryPosition();
    }}

    var completedIds = [];
    var availableIds = [];
    var lockedIds = [];

    // Filter out nodes whose branch_condition isn't met (wrong path)
    var visibleNodes = arc.nodes.filter(function(node) {{
        if (!node.branch_condition) return true;
        return State.variables.flags && State.variables.flags[node.branch_condition];
    }});

    // Check each node's completion status
    visibleNodes.forEach(function(node) {{
        var isCompleted = false;

        // Check linked_flag first (flags is an object, not an array)
        if (node.linked_flag) {{
            isCompleted = State.variables.flags && State.variables.flags[node.linked_flag];
        }}

        // Check linked_canvas via visited_nodes tracking
        if (node.linked_canvas && !isCompleted) {{
            var visitedNodes = State.variables.game_state.visited_nodes || [];
            if (node.linked_canvas_node) {{
                // Specific node target — check that exact node was visited
                var nodeKey = node.linked_canvas + "." + node.linked_canvas_node;
                isCompleted = visitedNodes.indexOf(nodeKey) !== -1;
            }} else {{
                // Any node in canvas — check if ANY visited_node starts with canvas slug
                var canvasPrefix = node.linked_canvas + ".";
                isCompleted = visitedNodes.some(function(vn) {{
                    return vn.indexOf(canvasPrefix) === 0;
                }});
            }}
        }}

        if (isCompleted) {{
            completedIds.push(node.id);
            result.completed_nodes.push({{
                id: node.id,
                name: node.name,
                chapter: node.chapter,
                journal_entry: node.journal_entry,
                is_milestone: node.is_milestone || false
            }});
        }}
    }});

    // Determine available vs locked nodes
    visibleNodes.forEach(function(node) {{
        if (completedIds.indexOf(node.id) !== -1) return; // Already completed

        var canUnlock = true;

        // Check requires_nodes
        if (node.requires_nodes && node.requires_nodes.length > 0) {{
            for (var i = 0; i < node.requires_nodes.length; i++) {{
                if (completedIds.indexOf(node.requires_nodes[i]) === -1) {{
                    canUnlock = false;
                    break;
                }}
            }}
        }}

        // Check requires_group
        if (canUnlock && node.requires_group && arc.groups) {{
            var group = arc.groups.find(function(g) {{ return g.id === node.requires_group; }});
            if (group) {{
                var groupNodes = visibleNodes.filter(function(n) {{ return n.group === group.id; }});
                var completedCount = groupNodes.filter(function(n) {{
                    return completedIds.indexOf(n.id) !== -1;
                }}).length;
                if (completedCount < group.required_count) {{
                    canUnlock = false;
                }}
            }}
        }}

        if (canUnlock) {{
            availableIds.push(node.id);
            result.available_nodes.push({{
                id: node.id,
                name: node.name,
                chapter: node.chapter,
                journal_entry: node.journal_entry,
                group: node.group || null
            }});
        }} else {{
            lockedIds.push(node.id);
            result.locked_nodes.push({{
                id: node.id,
                name: node.name,
                chapter: node.chapter,
                requires_group: node.requires_group || null,
                requires_nodes: node.requires_nodes || []
            }});
        }}
    }});

    // Build active groups status
    if (arc.groups) {{
        arc.groups.forEach(function(group) {{
            var groupNodes = visibleNodes.filter(function(n) {{ return n.group === group.id; }});
            var completedCount = groupNodes.filter(function(n) {{
                return completedIds.indexOf(n.id) !== -1;
            }}).length;

            result.active_groups.push({{
                id: group.id,
                name: group.name,
                description: group.description || "",
                completed: completedCount,
                required: group.required_count,
                total: groupNodes.length,
                isComplete: completedCount >= group.required_count
            }});
        }});
    }}

    // Determine current chapter based on most recent milestone or available nodes
    if (arc.chapters && arc.chapters.length > 0) {{
        var currentChapterId = null;

        // Find the chapter of the most recent milestone
        var milestones = result.completed_nodes.filter(function(n) {{ return n.is_milestone; }});
        if (milestones.length > 0) {{
            currentChapterId = milestones[milestones.length - 1].chapter;
        }}

        // Or use chapter of first available node
        if (!currentChapterId && result.available_nodes.length > 0) {{
            currentChapterId = result.available_nodes[0].chapter;
        }}

        // Or use first chapter
        if (!currentChapterId) {{
            currentChapterId = arc.chapters[0].id;
        }}

        result.current_chapter = arc.chapters.find(function(c) {{ return c.id === currentChapterId; }});
    }}

    // Calculate progress (only count visible nodes for accurate percentage)
    var totalNodes = visibleNodes.length;
    if (totalNodes > 0) {{
        result.progress_percent = Math.round((completedIds.length / totalNodes) * 100);
    }}

    // Check if stuck (no available nodes and not all completed)
    result.is_stuck = result.available_nodes.length === 0 && result.completed_nodes.length < totalNodes;

    // E9: stage-stall augmentation. ORs a per-NPC stage-flag stall signal
    // into is_stuck so generateNarrativeHint fires for players who are
    // visiting hubs/activities normally but failing to advance any NPC's
    // stage chain. Preserves the not-complete clause from the original
    // is_stuck calc — fully completed games never emit stalled hints.
    result.stage_progression_stalled = false;
    if (setup.npc_arc_stages && Object.keys(setup.npc_arc_stages).length > 0) {{
        var stallHints = (arc.guidance || arc.hints || {{}});
        var threshold = stallHints.stuck_threshold_days || 7;
        var sv = State.variables;
        sv.game_state.stage_advancement_log = sv.game_state.stage_advancement_log || {{}};
        var currentDay = (sv.game_state.time_state && sv.game_state.time_state.day) || 1;
        var log = sv.game_state.stage_advancement_log;
        var slugMap = setup.npc_slug_map || {{}};
        var stalled = true;
        for (var slug in setup.npc_arc_stages) {{
            // Skip hidden NPCs — their advancement isn't visible to the
            // player, so a hidden NPC stalling shouldn't fire stall hints.
            var uuid = slugMap[slug];
            var npc = uuid && sv.npcs ? sv.npcs[uuid] : null;
            if (npc && npc.hidden_from_ui) continue;
            var lastAdvance = log[slug] || 0;
            if (currentDay - lastAdvance < threshold) {{ stalled = false; break; }}
        }}
        result.stage_progression_stalled = stalled;
        // OR with existing canvas-stall, but keep the not-complete guard.
        // Empty-arc edge case: totalNodes === 0 means there's no story-arc graph
        // (test fixtures, prologue-only games) — treat any stall as honest.
        if (stalled && (result.completed_nodes.length < totalNodes || totalNodes === 0)) {{
            result.is_stuck = true;
        }}
    }}

    return result;
}};

// Get completed activities as "memories" for the journal
setup.getCompletedActivities = function() {{
    var position = setup.detectStoryPosition();
    return position.completed_nodes.map(function(node) {{
        return {{
            name: node.name,
            journal_entry: node.journal_entry || "A moment to remember...",
            is_milestone: node.is_milestone
        }};
    }});
}};

// Interpret NPC state as emotional description instead of numbers
setup.interpretNpcState = function(npcId) {{
    var arc = setup.story_arc || {{}};
    var mappings = arc.emotion_mappings || {{}};
    var result = {{
        npc_name: "",
        primary_emotion: "neutral",
        description: "Your relationship is developing...",
        relationship_summary: "",
        trait_interpretations: []
    }};

    // Get NPC data - $npcs is an object keyed by UUID, not an array
    var npc = null;
    var npcs = State.variables.npcs || {{}};

    // Try direct lookup first (npcId might already be a UUID)
    if (npcs[npcId]) {{
        npc = npcs[npcId];
    }} else {{
        // Try resolving as slug
        var resolvedId = setup.resolveNpcId(npcId);
        if (resolvedId && npcs[resolvedId]) {{
            npc = npcs[resolvedId];
        }}
    }}

    // Fallback to npc_states if available
    if (!npc && State.variables.npc_states) {{
        npc = State.variables.npc_states[npcId];
    }}

    if (!npc) return result;

    result.npc_name = npc.name || npcId;
    var traits = npc.core_traits || {{}};

    // Process each mapped trait
    var primaryEmotion = null;
    var highestPriority = -1;
    var traitOrder = Object.keys(mappings);

    traitOrder.forEach(function(traitName, priority) {{
        var traitValue = traits[traitName];
        if (typeof traitValue !== "number") return;

        var mapping = mappings[traitName];
        if (!mapping || !mapping.ranges) return;

        // Find matching range
        var matchedRange = null;
        for (var i = 0; i < mapping.ranges.length; i++) {{
            var range = mapping.ranges[i];
            if (traitValue >= range.min && traitValue <= range.max) {{
                matchedRange = range;
                break;
            }}
        }}

        if (matchedRange) {{
            result.trait_interpretations.push({{
                trait: traitName,
                value: traitValue,
                label: matchedRange.label,
                description: matchedRange.description
            }});

            // Track primary emotion (highest value trait)
            if (traitValue > highestPriority) {{
                highestPriority = traitValue;
                primaryEmotion = matchedRange.label;
                result.description = setup.resolveAtRefs(matchedRange.description);
            }}
        }}
    }});

    if (primaryEmotion) {{
        result.primary_emotion = primaryEmotion;
    }}

    // Generate relationship summary based on trait interpretations
    if (result.trait_interpretations.length > 0) {{
        var summaryParts = result.trait_interpretations.slice(0, 2).map(function(t) {{
            return setup.resolveAtRefs(t.description);
        }});
        result.relationship_summary = summaryParts.join(" ");
    }}

    return result;
}};

// Generate subtle narrative hint (not mechanical instructions)
setup.generateNarrativeHint = function() {{
    var arc = setup.story_arc || {{}};
    var hints = arc.guidance || arc.hints || {{}};
    var position = setup.detectStoryPosition();

    var result = {{
        hint_type: "none",
        text: ""
    }};

    // E9: stage stall is a top-priority signal. Fires even when the player
    // still has available canvases — the player is mid-graph but no NPC's
    // stage chain is moving, which the doctrine treats as stalled.
    if (position.stage_progression_stalled) {{
        result.hint_type = "stage_stall";
        var customMsg = hints.stage_stall_message;
        result.text = (customMsg && String(customMsg).trim())
            ? customMsg
            : "Days are slipping past. Something needs to shift.";
        return result;
    }}

    // Only show hints when stuck or making slow progress
    if (!position.is_stuck && position.available_nodes.length > 0) {{
        return result;
    }}

    // Check active groups for progress hints
    var incompleteGroup = position.active_groups.find(function(g) {{
        return !g.isComplete && g.completed < g.required;
    }});

    if (incompleteGroup) {{
        result.hint_type = "observation";
        var remaining = incompleteGroup.required - incompleteGroup.completed;
        if (hints.group_incomplete) {{
            result.text = hints.group_incomplete
                .replace("{{group_name}}", incompleteGroup.name)
                .replace("{{remaining}}", remaining);
        }} else {{
            result.text = "There might be more to explore...";
        }}
        return result;
    }}

    // Check locked nodes for what might be possible
    if (position.locked_nodes.length > 0) {{
        result.hint_type = "suggestion";
        if (hints.progress_needed) {{
            result.text = hints.progress_needed;
        }} else {{
            result.text = "Perhaps spending more time together would reveal new possibilities...";
        }}
        return result;
    }}

    // All done
    if (position.progress_percent >= 100) {{
        result.hint_type = "completion";
        result.text = hints.story_complete || "Your story together has reached a beautiful conclusion.";
    }}

    return result;
}};

// ============== QUEST PAGE HELPER FUNCTIONS ==============

// E10: Resolve UUID → slug. Inverse of setup.npc_slug_map (slug → UUID).
// Used by getNextActivity to translate the npcId arg into the slug needed
// for the stage-hint lookup. Returns null when no match (e.g. the player
// pseudo-id or stale UUIDs).
setup.npcSlugForId = function(npcId) {{
    if (!npcId) return null;
    var slugMap = setup.npc_slug_map || {{}};
    var key = String(npcId);
    for (var s in slugMap) {{
        if (slugMap[s] === key) return s;
    }}
    // Allow the input itself to be a slug (e.g. when callers already pass a
    // slug). Treat as slug if it appears as a key in the registry.
    if (setup.npc_arc_stages && setup.npc_arc_stages[key]) return key;
    return null;
}};

// E10: Stage-gated hint consumer. Walks arc.hints.templates, evaluates each
// template's normalized condition_items via setup.checkSingleCondition (the
// same evaluator used by canvas trigger conditions). Returns the FIRST
// template whose npc_id matches AND all condition_items pass.
//
// Templates without npc_id are skipped — those are global and outside the
// per-NPC routing. condition_items being empty means "always fires" for
// the matched NPC, useful for default fallback per-NPC content.
setup.getStageHintForNPC = function(npcSlug) {{
    if (!npcSlug) return null;
    // E17 short-circuit DEPRECATED 2026-05-09. Previously called
    // setup._getReadyHintForNPC here to synthesize a "ready" hint replacing
    // the regular Stage N flavor. Removed because computeHintGoal's State C
    // path (added 2026-05-09) handles the same scenario better — keeps
    // authored flavor + ready_text swap + 🔓 Ready badge + 📍 Location/🕒
    // Schedule from the transition canvas via _findStageSetterCanvas. Two
    // parallel ready surfaces was the root cause of jarring author-prose
    // loss when helpers cleared. The orphaned helpers (_getReadyHintForNPC
    // + _findHelperTransitionLocation) remain defined below for E17 test
    // backward-compat (string-presence assertions); safe to delete in a
    // follow-up cleanup PR after stability.
    var arc = setup.story_arc || {{}};
    var hints = (arc.guidance || arc.hints || {{}});
    var templates = hints.templates || [];
    // Collect every matching candidate, then sort by (priority desc,
    // specificity desc, file-order asc) so author-tagged crisis lines
    // win over ambient lines and more-specific conditions win over
    // less-specific ones automatically.
    var candidates = [];
    for (var ti = 0; ti < templates.length; ti++) {{
        var tpl = templates[ti];
        if (!tpl || !tpl.npc_id || tpl.npc_id !== npcSlug) continue;
        var items = tpl.condition_items || [];
        var allMet = true;
        for (var ci = 0; ci < items.length; ci++) {{
            if (!setup.checkSingleCondition(items[ci])) {{ allMet = false; break; }}
        }}
        if (allMet && tpl.text) candidates.push({{ tpl: tpl, ti: ti, items: items }});
    }}
    if (candidates.length === 0) return null;
    candidates.sort(function(a, b) {{
        var pa = a.tpl.priority || 0, pb = b.tpl.priority || 0;
        if (pb !== pa) return pb - pa;
        if (b.items.length !== a.items.length) return b.items.length - a.items.length;
        return a.ti - b.ti;
    }});
    var picked = candidates[0].tpl;
    // Pattern 2: pass through condition + tip + auto_goal so the
    // renderer can compute the structured 🎯 goal block.
    // 2026-05-09: also pass ready_text — renderStageHint widget swaps
    // flavor → ready_text when setup._isHintReady returns true (State C).
    // 2026-05-09: also pass arc_complete — when an author marks a hint
    // template `arc_complete = true` (terminal stage in the slice),
    // computeHintGoal renders a "✓ Arc complete" frame instead of trying
    // to surface a non-existent next-stage helper.
    return {{
        text: picked.text,
        npc_id: npcSlug,
        condition: picked.condition || null,
        tip: picked.tip || null,
        auto_goal: (picked.auto_goal !== false),
        ready_text: picked.ready_text || null,
        arc_complete: (picked.arc_complete === true),
        // 2026-05-10 — flag-based arc closure target (see computeHintGoal).
        arc_closure_flag: (typeof picked.arc_closure_flag === "string" ? picked.arc_closure_flag : "")
    }};
}};

// E20 — Decay warnings. For each threshold entry (auto-emitted from
// stage helpers, see _auto_emit_decay_warning_sidebar_items in v1.py),
// check if the trait value DROPPED since yesterday's snapshot AND is
// within 2.0 of the next gate. Returns warning text objects for sidebar
// rendering as amber banners.
setup.getDecayWarnings = function(thresholds) {{
    var snap = State.variables.last_day_snapshot || {{}};
    var warnings = [];
    if (!thresholds) return warnings;
    for (var synthKey in thresholds) {{
        var entries = thresholds[synthKey];
        if (!Array.isArray(entries) || entries.length === 0) continue;
        // Take the first entry to learn subject/key — they all share these.
        var first = entries[0];
        var subj = first.subject;
        var traitKey = first.trait_key;
        var npcId = first.npc_id || "";
        // Resolve current trait value
        var currentVal = null;
        var snapKey = "";
        var entityLabel = "";
        if (subj === "player") {{
            var pt = State.variables.player && State.variables.player.core_traits;
            if (!pt || typeof pt[traitKey] !== "number") continue;
            currentVal = pt[traitKey];
            snapKey = "player::" + traitKey;
            entityLabel = "Your";
        }} else if (subj === "npc") {{
            // npcId in helper is a slug — resolve to UUID
            var resolvedUuid = (setup.npc_slug_map || {{}})[npcId] || npcId;
            var npc = State.variables.npcs && State.variables.npcs[resolvedUuid];
            if (!npc || !npc.core_traits || typeof npc.core_traits[traitKey] !== "number") continue;
            currentVal = npc.core_traits[traitKey];
            snapKey = "npc:" + resolvedUuid + ":" + traitKey;
            // Look up NPC display name
            entityLabel = (npc.name || npcId);
        }} else {{
            continue;
        }}
        // Need a snapshot AND current must be < snapshot (decreased today)
        if (!(snapKey in snap)) continue;
        var snapVal = snap[snapKey];
        if (currentVal >= snapVal) continue;  // Did not decrease
        // Find next gate above current (lowest threshold > currentVal)
        var nextGate = null;
        for (var ei = 0; ei < entries.length; ei++) {{
            var v = entries[ei].value;
            if (v > currentVal && (nextGate === null || v < nextGate)) {{
                nextGate = v;
            }}
        }}
        if (nextGate === null) continue;  // Already past all gates
        // Only warn if within 2.0 of the next gate
        if (nextGate - currentVal > 2.0) continue;
        // Build human-readable warning
        var dropAmount = (snapVal - currentVal).toFixed(1);
        warnings.push({{
            text: entityLabel + " " + traitKey + " dropping (" + currentVal.toFixed(1) +
                  " today, was " + snapVal.toFixed(1) + " yesterday). " +
                  "Next gate at " + nextGate + " — interact today or lose more."
        }});
    }}
    return warnings;
}};

// E15 — Global hint walker. Returns one winning template per "goal-key"
// (missing_flag || missing_trait || file index) so authors can write
// crisis variants for the same goal and the picker keeps only the best
// one. Used by QuestsPage to render the "Story Goals" section.
setup.getGlobalHints = function() {{
    var arc = setup.story_arc || {{}};
    var hints = (arc.guidance || arc.hints || {{}});
    var templates = hints.templates || [];
    // Pass 1: collect every match grouped by goal-key.
    var groups = {{}};
    var groupOrder = [];
    for (var ti = 0; ti < templates.length; ti++) {{
        var tpl = templates[ti];
        if (!tpl || tpl.npc_id) continue;
        var items = tpl.condition_items || [];
        var allMet = true;
        for (var ci = 0; ci < items.length; ci++) {{
            if (!setup.checkSingleCondition(items[ci])) {{ allMet = false; break; }}
        }}
        if (!allMet || !tpl.text) continue;
        var cond = tpl.condition || {{}};
        var goalKey = cond.missing_flag || cond.missing_trait || ("__idx_" + ti);
        if (!groups[goalKey]) {{
            groups[goalKey] = [];
            groupOrder.push({{ key: goalKey, firstTi: ti }});
        }}
        groups[goalKey].push({{ tpl: tpl, ti: ti, items: items }});
    }}
    // Pass 2: within each group, sort by (priority desc, specificity desc,
    // file-order asc) and keep the top entry only.
    var winners = {{}};
    for (var gk in groups) {{
        var arr = groups[gk];
        arr.sort(function(a, b) {{
            var pa = a.tpl.priority || 0, pb = b.tpl.priority || 0;
            if (pb !== pa) return pb - pa;
            if (b.items.length !== a.items.length) return b.items.length - a.items.length;
            return a.ti - b.ti;
        }});
        winners[gk] = arr[0];
    }}
    // Pass 3: emit survivors in original first-seen order so visible card
    // sequence stays predictable.
    var matches = [];
    for (var oi = 0; oi < groupOrder.length; oi++) {{
        var entry = winners[groupOrder[oi].key];
        if (!entry) continue;
        var pickedTpl = entry.tpl;
        // Pattern 2 parity with getStageHintForNPC (2026-05-17): pass the
        // same goal-block fields through so global "Story Goals" cards can
        // render the structured frame (tip + auto_goal + ready_text swap +
        // arc_complete badge + flag-based arc_closure_flag Ready frame).
        // Previously only text/npc_id/condition survived, which is why
        // npc_id-less objectives rendered as flat narrative with no location.
        matches.push({{
            text: pickedTpl.text,
            npc_id: null,
            condition: pickedTpl.condition || null,
            tip: pickedTpl.tip || null,
            auto_goal: (pickedTpl.auto_goal !== false),
            ready_text: pickedTpl.ready_text || null,
            arc_complete: (pickedTpl.arc_complete === true),
            arc_closure_flag: (typeof pickedTpl.arc_closure_flag === "string" ? pickedTpl.arc_closure_flag : "")
        }});
    }}
    return matches;
}};

// ⚠️ DEPRECATED 2026-05-09 — orphaned by the State C unification (see the
// note inside setup.getStageHintForNPC). No longer called from any runtime
// path. Kept defined here for E17 test backward-compat (3 tests in
// E17ReadyTextEngineEmissionTests assert string-presence: "tpl.ready_text"
// + "All gates cleared. Visit"). Safe to delete in a follow-up cleanup PR
// after the new State C surface has stabilized in production.
//
// Original purpose: synthesize a "ready" hint when the NPC's next-stage
// helper has cleared but the stage trait hasn't advanced yet. Returned
// null when no such state, or no helper existed for the next stage.
//
// 2026-05-06 — supported per-hint `ready_text` author override. When the
// matching template (by npc_id + stage_value=curStage) had a non-empty
// `ready_text` field, used it verbatim. Else fell back to the engine
// default ("All gates cleared. Visit X to seal the moment."). Today the
// `ready_text` swap lives in renderStageHint widget via setup._isHintReady
// — author opts in by defining ready_text on the hint template directly.
setup._getReadyHintForNPC = function(npcSlug) {{
    if (!npcSlug) return null;
    // Current stage trait lives at $player.core_traits[<slug>_stage]
    var pl = State.variables.player;
    var traits = (pl && pl.core_traits) || {{}};
    var stageKey = npcSlug + "_stage";
    var curStage = traits[stageKey];
    if (typeof curStage !== "number") return null;
    // Helper convention: "<bare>_stage_<N+1>" where bare = npcSlug w/o "npc_" prefix.
    var bareSlug = npcSlug.replace(/^npc_/, "");
    var helperName = bareSlug + "_stage_" + (curStage + 1);
    var helper = (setup.stage_helpers_map || {{}})[helperName];
    if (!helper || !helper.conditions) return null;
    // Evaluate the helper's conditions against current state.
    var cleared = false;
    try {{
        cleared = setup.triggerConditionsSatisfied(helper.conditions);
    }} catch (e) {{
        return null;
    }}
    if (!cleared) return null;
    // Helper cleared. Find the transition canvas's location.
    var locName = setup._findHelperTransitionLocation(helperName);
    if (!locName) return null;
    // E17 (2026-05-06) — look up the matching template's ready_text override.
    // Match by (npc_id, condition.stage_value=curStage, condition.stage_op=eq).
    // First match wins (consistent with setup.getStageHintForNPC's picker).
    var readyText = null;
    var arc = setup.story_arc || {{}};
    var hints = (arc.guidance || arc.hints || {{}});
    var templates = hints.templates || [];
    for (var ti = 0; ti < templates.length; ti++) {{
        var tpl = templates[ti];
        if (!tpl || tpl.npc_id !== npcSlug) continue;
        var tplCond = tpl.condition || {{}};
        if (tplCond.stage_npc !== npcSlug) continue;
        if (tplCond.stage_op !== "eq") continue;
        if (tplCond.stage_value !== curStage) continue;
        if (tpl.ready_text && typeof tpl.ready_text === "string" && tpl.ready_text.length > 0) {{
            readyText = tpl.ready_text;
            break;
        }}
    }}
    var finalText = readyText || ("All gates cleared. Visit " + locName + " to seal the moment.");
    return {{
        text: finalText,
        npc_id: npcSlug,
        isReadyHint: true
    }};
}};

// ⚠️ DEPRECATED 2026-05-09 — orphaned by the State C unification. Was
// only ever called from setup._getReadyHintForNPC (now also deprecated).
// Kept defined for symmetry + safety (no test asserts its presence today
// but removing it without removing the parent function would be sloppy).
// Safe to delete in the same follow-up cleanup PR as _getReadyHintForNPC.
//
// Original purpose: walk locationCanvases to find the canvas that uses the
// given stage helper as a trigger condition (operator is_true). Returned
// the canvas's location display name (from setup.locations[slug].name).
// computeHintGoal's State C path uses _findStageSetterCanvas instead —
// indexes by trait setter (npc_<slug>_stage = N) rather than helper ref,
// which is more robust + cheaper than walking locationCanvases live.
setup._findHelperTransitionLocation = function(helperName) {{
    var helpData = setup.help_data || {{}};
    var locationCanvases = helpData.locationCanvases || {{}};
    var locUuidToSlug = setup._getLocUuidToSlug();
    var locs = setup.locations || {{}};
    for (var locUuid in locationCanvases) {{
        var canvasList = locationCanvases[locUuid];
        for (var i = 0; i < canvasList.length; i++) {{
            var c = canvasList[i];
            var conds = (c.conditions && c.conditions.items) || [];
            for (var ci = 0; ci < conds.length; ci++) {{
                var it = conds[ci];
                if (it && it.type === "stage" && it.helper === helperName && it.operator === "is_true") {{
                    var locSlug = locUuidToSlug[locUuid];
                    var locData = locs[locSlug];
                    return (locData && locData.name) || locSlug || null;
                }}
            }}
        }}
    }}
    return null;
}};

// =====================================================================
// Pattern 2 (2026-05-01) — auto-render the structured 🎯 goal block
// =====================================================================
// Author writes only narrative text + optional `tip`. Engine pulls helper
// conditions (or canvas trigger conditions for branch-inside-shell), maps
// trait/flag keys to player-facing labels, evaluates each gate against
// current state, and renders bulleted progress (✓ / ◯ + current/target).

// Format a single trait value (handles ints and floats cleanly).
setup._fmtTraitValue = function(v) {{
    if (typeof v !== "number") return String(v);
    if (Math.abs(v - Math.round(v)) < 0.05) return String(Math.round(v));
    return v.toFixed(1);
}};

// Pretty-print a comparison operator for player-facing display.
setup._fmtOp = function(op) {{
    var map = {{ "gte": "≥", "gt": ">", "lte": "≤", "lt": "<", "eq": "=" }};
    return map[op] || op;
}};

// Get current value for a trait condition_item. Returns number or null.
setup._currentTraitValue = function(item) {{
    if (!item || item.type !== "trait") return null;
    if (item.subject === "player") {{
        var pt = State.variables.player && State.variables.player.core_traits;
        return (pt && typeof pt[item.trait_key] === "number") ? pt[item.trait_key] : 0;
    }}
    if (item.subject === "npc") {{
        var slug = item.npc_id;
        var uuid = (setup.npc_slug_map || {{}})[slug] || slug;
        var npc = State.variables.npcs && State.variables.npcs[uuid];
        return (npc && npc.core_traits && typeof npc.core_traits[item.trait_key] === "number")
            ? npc.core_traits[item.trait_key] : 0;
    }}
    return null;
}};

// Resolve a player-facing label for a trait condition_item.
// For NPC subjects, prepends NPC display name (e.g., "Frank trust").
setup._labelForTrait = function(item) {{
    var key = item.trait_key;
    var labelData = (setup.trait_labels || {{}})[key];
    var labelText = labelData ? labelData.label : key;
    if (item.subject === "npc" && item.npc_id) {{
        var slug = item.npc_id;
        var uuid = (setup.npc_slug_map || {{}})[slug] || slug;
        var npc = State.variables.npcs && State.variables.npcs[uuid];
        var npcName = (npc && npc.name) || slug.replace("npc_", "");
        // Capitalize first letter of NPC name if needed
        npcName = npcName.charAt(0).toUpperCase() + npcName.slice(1);
        return npcName + " " + labelText;
    }}
    return labelText;
}};

// Resolve a player-facing label for a flag condition_item.
setup._labelForFlag = function(item) {{
    var key = item.flag_key;
    var labelData = (setup.flag_labels || {{}})[key];
    return labelData ? labelData.label : key;
}};

// Render a single AND-gate condition_item as an HTML <li>.
setup._renderGoalGate = function(item) {{
    if (!item || typeof item !== "object") return "";
    var met = false;
    try {{ met = setup.checkSingleCondition(item); }} catch (e) {{ met = false; }}
    var marker = met ? '<span class="stage-hint-met">✓</span>'
                     : '<span class="stage-hint-unmet">◯</span>';
    if (item.type === "trait") {{
        var label = setup._labelForTrait(item);
        var current = setup._currentTraitValue(item);
        var target = item.value;
        var op = setup._fmtOp(item.operator);
        var progress = "";
        if (typeof current === "number" && typeof target === "number") {{
            progress = '<span class="stage-hint-progress">'
                + setup._fmtTraitValue(current) + " / " + setup._fmtTraitValue(target)
                + "</span>";
        }}
        var className = met ? "stage-hint-met-row" : "stage-hint-unmet-row";
        return '<li class="' + className + '">' + marker + " " + label
            + " " + op + " " + setup._fmtTraitValue(target) + " " + progress + "</li>";
    }}
    if (item.type === "flag") {{
        var flagLabel = setup._labelForFlag(item);
        var className2 = met ? "stage-hint-met-row" : "stage-hint-unmet-row";
        return '<li class="' + className2 + '">' + marker + " " + flagLabel + "</li>";
    }}
    // stage / pass / item / other types: render minimally
    return '<li>' + marker + " " + (item.helper || item.flag_key || item.trait_key || "(condition)") + "</li>";
}};

// Render an OR-path branch — used when helper conditions.logic === "OR".
setup._renderGoalPath = function(item, idx) {{
    var labels = ["Path A", "Path B", "Path C", "Path D"];
    var pathLabel = labels[idx] || ("Path " + (idx + 1));
    var inner = setup._renderGoalGate(item);
    return '<div class="stage-hint-path"><strong>' + pathLabel + ':</strong> '
        + '<ul>' + inner + '</ul></div>';
}};

// Find the canvas whose trigger conditions describe this stage transition
// (used for branch-inside-shell — Frank 1→2). Returns {{conditions, canvas}}
// or null.
setup._findStageSetterCanvas = function(npcSlug, stageValue) {{
    var index = (setup.stage_setter_canvases || {{}})[npcSlug] || {{}};
    var cvId = index[stageValue];
    if (!cvId) return null;
    var helpData = setup.help_data || {{}};
    var locationCanvases = helpData.locationCanvases || {{}};

    function findInLocations(canvasId) {{
        for (var locUuid in locationCanvases) {{
            var canvasList = locationCanvases[locUuid];
            for (var i = 0; i < canvasList.length; i++) {{
                var c = canvasList[i];
                if (c && c.id === canvasId) {{
                    return {{ canvas: c, locUuid: locUuid }};
                }}
            }}
        }}
        return null;
    }}

    // Direct lookup — triggered setter canvases land here.
    var direct = findInLocations(cvId);
    if (direct) return direct;

    // Fallback (2026-05-09): triggerless sub-menu setter canvases (e.g.,
    // scene_office_after_crack which sets npc_frank_stage=4 but is reached
    // only via the office menu's "Bend over the page" choice) aren't in
    // locationCanvases. Walk back via sub_menu_parents to find a parent
    // menu canvas that IS in locationCanvases — surface that parent's
    // location/schedule for State C "🔓 Ready" frame's 📍/🕒. Mirrors the
    // same fallback in _findFlagSetterCanvas. Cap at 5 hops + cycle-safe.
    var parents = setup.sub_menu_parents || {{}};
    var current = cvId;
    var visited = {{}};
    for (var hop = 0; hop < 5; hop++) {{
        var parent = parents[current];
        if (!parent || visited[parent]) break;
        visited[parent] = true;
        var hit = findInLocations(parent);
        if (hit) return hit;
        current = parent;
    }}

    return null;
}};

// Pattern 2 v2.1 (2026-05-04): find the canvas whose flagEffects set the
// given flag (first non-dev setter wins per the Python index builder).
// Returns {{canvas, locUuid}} or null. Used by setup.computeHintGoal's
// State B "Where" frame — when a stage helper has an unmet flag gate but
// all non-flag gates are met, this surfaces the canvas the player needs
// to find to set the flag.
// Returns true when an auto_goal hint's helper conditions are all currently
// satisfied — i.e. the hint is in State C "🔓 Ready". Mirrors the triggerFired
// evaluation inside computeHintGoal. Used by the renderStageHint widget to
// swap flavor → ready_text when the hint is ready (2026-05-09).
setup._isHintReady = function(hintObj) {{
    if (!hintObj || typeof hintObj !== "object") return false;
    // 2026-05-10 — closure-flag hint is "ready" whenever the flag is unset
    // (the closure scene exists; the player just needs to visit it). Once
    // the flag flips true, computeHintGoal renders the ✓ Arc complete badge
    // and ready_text swap becomes irrelevant. Sits before the auto_goal=false
    // short-circuit so closure templates can leave auto_goal=false.
    if (typeof hintObj.arc_closure_flag === "string" && hintObj.arc_closure_flag.length > 0) {{
        var ciFlag = {{ type: "flag", subject: "player", flag_key: hintObj.arc_closure_flag, operator: "is_false" }};
        try {{ return setup.checkSingleCondition(ciFlag); }} catch (e) {{ return false; }}
    }}
    if (hintObj.auto_goal === false) return false;
    var cond = hintObj.condition || {{}};
    if (!cond.stage_npc || cond.stage_value == null) return false;
    var bareSlug = cond.stage_npc.replace(/^npc_/, "");
    var helperName = bareSlug + "_stage_" + (cond.stage_value + 1);
    var helper = (setup.stage_helpers_map || {{}})[helperName];
    if (!helper || !helper.conditions || !Array.isArray(helper.conditions.items)) return false;
    var conditions = helper.conditions.items;
    var logic = (helper.conditions.logic || "AND").toUpperCase();
    if (logic === "OR") {{
        for (var k = 0; k < conditions.length; k++) {{
            try {{ if (setup.checkSingleCondition(conditions[k])) return true; }} catch (e) {{}}
        }}
        return false;
    }}
    for (var m = 0; m < conditions.length; m++) {{
        try {{ if (!setup.checkSingleCondition(conditions[m])) return false; }} catch (e) {{ return false; }}
    }}
    return true;
}};

setup._findFlagSetterCanvas = function(flagKey) {{
    var index = setup.flag_setter_canvases || {{}};
    var cvId = index[flagKey];
    if (!cvId) return null;
    var helpData = setup.help_data || {{}};
    var locationCanvases = helpData.locationCanvases || {{}};

    // Inline lookup — direct hit on locationCanvases.
    function findInLocations(canvasId) {{
        for (var locUuid in locationCanvases) {{
            var canvasList = locationCanvases[locUuid];
            for (var i = 0; i < canvasList.length; i++) {{
                var c = canvasList[i];
                if (c && c.id === canvasId) {{
                    return {{ canvas: c, locUuid: locUuid }};
                }}
            }}
        }}
        return null;
    }}

    // First try: direct lookup. Triggered setter canvases land here.
    var direct = findInLocations(cvId);
    if (direct) return direct;

    // Fallback (2026-05-09): triggerless sub-menu canvases aren't in
    // locationCanvases. Walk back via sub_menu_parents to find a parent
    // menu canvas that IS in locationCanvases — surface that parent's
    // location/schedule as the "where to go" for the flag's set action.
    // Cap at 5 hops to handle nested menus and prevent runaway loops on
    // any pathological cycle.
    var parents = setup.sub_menu_parents || {{}};
    var current = cvId;
    var visited = {{}};
    for (var hop = 0; hop < 5; hop++) {{
        var parent = parents[current];
        if (!parent || visited[parent]) break;
        visited[parent] = true;
        var hit = findInLocations(parent);
        if (hit) return hit;
        current = parent;
    }}

    return null;
}};

// Format a canvas trigger schedule into a player-facing string like
// "Mon–Fri 20:00–22:30". Returns "" if no schedule.
// Reads canvas.scheduleParams (camelCase, set by _build_help_data); each
// entry has weekdays/startTime/endTime. Field names corrected 2026-05-04 —
// previously this read canvas.schedule with snake_case fields and silently
// returned "" for every canvas.
setup._formatCanvasSchedule = function(canvas) {{
    if (!canvas || !canvas.scheduleParams) return "";
    var sched = canvas.scheduleParams;
    if (!Array.isArray(sched) || sched.length === 0) return "";
    var s = sched[0];  // take the first window for display
    var weekdayLabels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
    var days = (s.weekdays || []).map(function(d) {{ return weekdayLabels[d] || ""; }}).filter(Boolean);
    var dayStr = "";
    if (days.length === 7) dayStr = "every day";
    else if (days.length === 5 && days.indexOf("Sat") === -1 && days.indexOf("Sun") === -1) dayStr = "Mon–Fri";
    else if (days.length === 2 && days.indexOf("Sat") !== -1 && days.indexOf("Sun") !== -1) dayStr = "weekends";
    else dayStr = days.join("/");
    var timeStr = (s.startTime && s.endTime) ? (s.startTime + "–" + s.endTime) : "";
    if (dayStr && timeStr) return dayStr + " " + timeStr;
    return dayStr || timeStr;
}};

// Get a location display name from a locUuid (via setup.help_data + setup.locations).
setup._locNameFromUuid = function(locUuid) {{
    var locUuidToSlug = setup._getLocUuidToSlug();
    var slug = locUuidToSlug[locUuid];
    var locs = setup.locations || {{}};
    var locData = locs[slug];
    return (locData && locData.name) || slug || null;
}};

// Main entry — returns HTML for the structured goal block.
//
// THREE frames depending on gate state (helper path; canvas-trigger fallback
// keeps its existing two-frame Ready/To-Advance behavior unchanged):
//   - State A — Goals frame (🎯 To advance:): some non-flag gate unmet.
//     Player still grinding traits. Bullet list with progress.
//   - State B — "Where" frame (🎯 Next beat:): all non-flag gates met,
//     some flag gate unmet, AND first unmet flag has a known setter canvas
//     in setup.flag_setter_canvases. Surfaces 📍 + 🕒 of the setter — the
//     player has done the prep work; only thing left is to be at the right
//     place at the right time. NEW Pattern 2 v2.1 (2026-05-04).
//   - State C — Ready frame (🔓 Ready): all gates met. Helper-driven
//     transition canvas's location + schedule.
//
// States are mutually exclusive — never two at once. Narrative text
// (the .stage-hint-flavor div from renderStageHint) stays static across
// state transitions; the frame swap IS the state-change signal.
setup.computeHintGoal = function(hintObj) {{
    if (!hintObj || typeof hintObj !== "object") return "";
    // 2026-05-10 — flag-based arc closure. When a hint template names an
    // arc_closure_flag, look up that flag's setter canvas and surface its
    // location + schedule as a Ready frame. Once the flag is set (player
    // played the closure scene), render the ✓ Arc complete badge instead.
    // Lets terminal-stage hints reflect actual consummation state instead
    // of firing the badge prematurely on stage entry. Author pattern: pair
    // arc_closure_flag (pre) + arc_complete=true (post) templates gated by
    // trait_checks on the same flag (is_false / is_true). Bypasses the
    // auto_goal=false suppression below — closure rendering is independent.
    if (typeof hintObj.arc_closure_flag === "string" && hintObj.arc_closure_flag.length > 0) {{
        var closureFlag = hintObj.arc_closure_flag;
        var flagItem = {{ type: "flag", subject: "player", flag_key: closureFlag, operator: "is_true" }};
        var flagSet = false;
        try {{ flagSet = setup.checkSingleCondition(flagItem); }} catch (e) {{ flagSet = false; }}
        if (flagSet) {{
            return '<div class="stage-hint-goal">'
                 + '<div class="stage-hint-goal-header stage-hint-arc-complete">'
                 + '<span class="stage-hint-target">✓</span> Arc complete</div>'
                 + '</div>';
        }}
        var setterFound = setup._findFlagSetterCanvas(closureFlag);
        if (!setterFound) return "";
        var setterLocName = setup._locNameFromUuid(setterFound.locUuid);
        var setterSchedStr = setup._formatCanvasSchedule(setterFound.canvas);
        var closureHtml = '<div class="stage-hint-goal">'
                        + '<div class="stage-hint-goal-header stage-hint-ready">'
                        + '<span class="stage-hint-target">🔓</span> Ready</div>';
        if (setterLocName) closureHtml += '<div class="stage-hint-where">📍 ' + setterLocName + '</div>';
        if (setterSchedStr) closureHtml += '<div class="stage-hint-where">🕒 ' + setterSchedStr + '</div>';
        closureHtml += '</div>';
        return closureHtml;
    }}
    // Terminal-stage badge (2026-05-09) — when an author marks a hint
    // template `arc_complete = true`, render a fixed "✓ Arc complete"
    // frame instead of trying to surface a non-existent next-stage helper.
    // Bypasses the auto_goal=false suppression below; arc_complete is its
    // own independent concern from auto-goal-rendering of progress gates.
    if (hintObj.arc_complete === true) {{
        return '<div class="stage-hint-goal">'
             + '<div class="stage-hint-goal-header stage-hint-arc-complete">'
             + '<span class="stage-hint-target">✓</span> Arc complete</div>'
             + '</div>';
    }}
    if (hintObj.auto_goal === false) return "";
    var cond = hintObj.condition || {{}};
    if (!cond.stage_npc || cond.stage_value == null) return "";

    var npcSlug = cond.stage_npc;
    var nextStage = cond.stage_value + 1;

    var bareSlug = npcSlug.replace(/^npc_/, "");
    var helperName = bareSlug + "_stage_" + nextStage;
    var helper = (setup.stage_helpers_map || {{}})[helperName];

    var conditions = null;
    var sourceLogic = "AND";
    var locName = null;
    var schedStr = "";
    var fromHelper = false;

    if (helper && helper.conditions && Array.isArray(helper.conditions.items)) {{
        conditions = helper.conditions.items;
        sourceLogic = (helper.conditions.logic || "AND").toUpperCase();
        fromHelper = true;
    }} else {{
        var found = setup._findStageSetterCanvas(npcSlug, nextStage);
        if (!found) return "";
        var canvas = found.canvas;
        if (!canvas || !canvas.conditions || !Array.isArray(canvas.conditions.items)) return "";
        conditions = canvas.conditions.items;
        sourceLogic = (canvas.conditions.logic || "AND").toUpperCase();
        locName = setup._locNameFromUuid(found.locUuid);
        schedStr = setup._formatCanvasSchedule(canvas);
    }}

    if (!conditions || conditions.length === 0) return "";

    // Compute trigger-fired state. AND → all met; OR → any met.
    var triggerFired;
    if (sourceLogic === "OR") {{
        triggerFired = false;
        for (var k = 0; k < conditions.length; k++) {{
            var passedOr = false;
            try {{ passedOr = setup.checkSingleCondition(conditions[k]); }} catch (e) {{ passedOr = false; }}
            if (passedOr) {{ triggerFired = true; break; }}
        }}
    }} else {{
        triggerFired = true;
        for (var m = 0; m < conditions.length; m++) {{
            var passedAnd = false;
            try {{ passedAnd = setup.checkSingleCondition(conditions[m]); }} catch (e) {{ passedAnd = false; }}
            if (!passedAnd) {{ triggerFired = false; break; }}
        }}
    }}

    // Ready frame needs location/schedule even when helper drove the gates.
    if (triggerFired && fromHelper) {{
        var foundReady = setup._findStageSetterCanvas(npcSlug, nextStage);
        if (foundReady) {{
            locName = setup._locNameFromUuid(foundReady.locUuid);
            schedStr = setup._formatCanvasSchedule(foundReady.canvas);
        }}
    }}

    // State B detection (helper path, AND logic, all non-flag gates met,
    // some flag gate(s) unmet, first unmet flag has a known setter canvas).
    // Pattern 2 v2.1 (2026-05-04) — flag-setter drill-down for the goal block.
    var stateB = null;
    if (fromHelper && !triggerFired && sourceLogic === "AND") {{
        var allNonFlagMet = true;
        var firstUnmetFlagItem = null;
        for (var n = 0; n < conditions.length; n++) {{
            var item = conditions[n];
            if (!item || typeof item !== "object") continue;
            var passedItem = false;
            try {{ passedItem = setup.checkSingleCondition(item); }} catch (e) {{ passedItem = false; }}
            if (item.type === "flag") {{
                if (!passedItem && !firstUnmetFlagItem) firstUnmetFlagItem = item;
            }} else {{
                if (!passedItem) {{ allNonFlagMet = false; break; }}
            }}
        }}
        if (allNonFlagMet && firstUnmetFlagItem) {{
            var setterFound = setup._findFlagSetterCanvas(firstUnmetFlagItem.flag_key);
            if (setterFound) {{
                stateB = {{
                    flagItem: firstUnmetFlagItem,
                    locName: setup._locNameFromUuid(setterFound.locUuid),
                    schedStr: setup._formatCanvasSchedule(setterFound.canvas),
                }};
            }}
        }}
    }}

    var html = '<div class="stage-hint-goal">';

    if (triggerFired) {{
        // State C — Ready frame
        html += '<div class="stage-hint-goal-header stage-hint-ready">'
             + '<span class="stage-hint-target">🔓</span> Ready</div>';
        if (locName) {{
            html += '<div class="stage-hint-where">📍 ' + locName + '</div>';
        }}
        if (schedStr) {{
            html += '<div class="stage-hint-where">🕒 ' + schedStr + '</div>';
        }}
    }} else if (stateB) {{
        // State B — "Where" frame: surface the setter canvas's location/schedule.
        // Optional one-line action hint pulled from the flag's player-facing label.
        html += '<div class="stage-hint-goal-header"><span class="stage-hint-target">🎯</span> Next beat:</div>';
        if (stateB.locName) {{
            html += '<div class="stage-hint-where">📍 ' + stateB.locName + '</div>';
        }}
        if (stateB.schedStr) {{
            html += '<div class="stage-hint-where">🕒 ' + stateB.schedStr + '</div>';
        }}
        var stateBLabel = setup._labelForFlag(stateB.flagItem);
        if (stateBLabel && stateBLabel !== stateB.flagItem.flag_key) {{
            html += '<div class="stage-hint-where">' + stateBLabel + '</div>';
        }}
    }} else {{
        // State A — Goals frame (existing To-Advance behavior).
        // Pattern 2 v2.2 (2026-05-04): filter out flag-typed items from the
        // bullet list. Flags in helpers are quest-destination markers carried
        // by the narrative line + handled by State B's "Where" frame when
        // their non-flag prereqs clear. The build-time validator
        // (template_import.py validate()) guarantees every helper-referenced
        // flag has either a non-dev setter (Case 1, drilled via State B) OR
        // is dev_only-tagged (Case 3, intentional out-of-scope). Case 4
        // (bug — no setter, no dev_only tag) gets caught at build, not
        // surfaced as a runtime checkbox.
        html += '<div class="stage-hint-goal-header"><span class="stage-hint-target">🎯</span> '
             + (sourceLogic === "OR" ? "Two paths to advance:" : "To advance:") + '</div>';

        var bulletConditions = [];
        for (var bi = 0; bi < conditions.length; bi++) {{
            var ci = conditions[bi];
            if (ci && ci.type === "flag") continue;
            bulletConditions.push(ci);
        }}

        if (sourceLogic === "OR") {{
            for (var i = 0; i < bulletConditions.length; i++) {{
                html += setup._renderGoalPath(bulletConditions[i], i);
            }}
        }} else {{
            html += '<ul>';
            for (var j = 0; j < bulletConditions.length; j++) {{
                html += setup._renderGoalGate(bulletConditions[j]);
            }}
            html += '</ul>';
        }}

        if (locName) {{
            html += '<div class="stage-hint-where">📍 ' + locName + '</div>';
        }}
        if (schedStr) {{
            html += '<div class="stage-hint-where">🕒 ' + schedStr + '</div>';
        }}
    }}

    html += '</div>';
    return html;
}};


// Get the next activity for an NPC or player (first incomplete in node order)
setup.getNextActivity = function(npcId) {{
    // E10: stage-gated hint takes priority over the canvas-graph walk.
    // For NPC sources only — the player pseudo-id has no stage chain.
    if (npcId && npcId !== "_player_") {{
        var slug = setup.npcSlugForId(npcId);
        if (slug) {{
            var stageHint = setup.getStageHintForNPC(slug);
            if (stageHint) {{
                return {{
                    isStageHint: true,
                    stageHint: stageHint,
                    conditionsNotMet: false
                }};
            }}
        }}
    }}

    var helpData = setup.help_data || {{}};
    var npcData;
    if (npcId === "_player_") {{
        npcData = helpData.player || null;
    }} else {{
        npcData = helpData.npcs ? helpData.npcs[npcId] : null;
    }}
    if (!npcData) return null;

    var activities = npcData.activities || [];
    var flags = State.variables.flags || {{}};
    var hist = (State.variables.game_state && State.variables.game_state.trigger_history) || {{}};
    var startingCanvasId = helpData.starting_canvas_id || null;

    // Activities are in node order from story_arc
    for (var i = 0; i < activities.length; i++) {{
        var activity = activities[i];

        // Skip non-story-arc activities (repeatable canvases without node_id)
        if (!activity.node_id) continue;

        // Skip completed activities
        var isCompleted = false;

        // Check linked_flag
        if (activity.linked_flag && flags[activity.linked_flag]) {{
            isCompleted = true;
        }}

        // Check visited_nodes tracking (replaces dead completed_canvases)
        if (!isCompleted && activity.canvas_slug) {{
            var visitedNodes = State.variables.game_state.visited_nodes || [];
            if (activity.linked_canvas_node) {{
                // Specific node target
                var nodeKey = activity.canvas_slug + "." + activity.linked_canvas_node;
                isCompleted = visitedNodes.indexOf(nodeKey) !== -1;
            }} else {{
                // Any node in canvas
                var canvasPrefix = activity.canvas_slug + ".";
                isCompleted = visitedNodes.some(function(vn) {{
                    return vn.indexOf(canvasPrefix) === 0;
                }});
            }}
        }}

        if (isCompleted) continue;

        // Starting canvas has no location — show "start the game" instead of skipping
        if (!activity.location) {{
            if (activity.canvas_id && activity.canvas_id === startingCanvasId) {{
                return {{
                    activity: activity,
                    isStartingCanvas: true,
                    conditionsNotMet: false
                }};
            }}
            // Phone-linked node: show "Message NPC" hint
            if (activity.linked_phone) {{
                return {{
                    activity: activity,
                    isPhoneActivity: true,
                    conditionsNotMet: false
                }};
            }}
            continue;
        }}

        // Check if canvas trigger conditions are met
        var canvasConditions = activity.canvas_conditions;
        if (canvasConditions && canvasConditions.items) {{
            var items = canvasConditions.items;
            var traitItems = [];
            var flagItems = [];
            var daysSinceFlagItems = [];

            // Separate trait, flag, and days_since_flag conditions
            for (var k = 0; k < items.length; k++) {{
                if (items[k].type === 'trait') traitItems.push(items[k]);
                else if (items[k].type === 'flag') flagItems.push(items[k]);
                else if (items[k].type === 'days_since_flag') daysSinceFlagItems.push(items[k]);
            }}

            // Check trait conditions FIRST (priority)
            var unmetTraits = [];
            for (var t = 0; t < traitItems.length; t++) {{
                if (!setup.checkSingleCondition(traitItems[t])) {{
                    unmetTraits.push(traitItems[t]);
                }}
            }}

            if (unmetTraits.length > 0) {{
                // Trait not met - show trait requirement
                return {{
                    activity: activity,
                    isLocked: false,
                    conditionsNotMet: true,
                    traitConditionsNotMet: true,
                    canvasConditions: {{ items: unmetTraits, logic: canvasConditions.logic, version: '1.0' }}
                }};
            }}

            // Traits met - check flags
            var unmetFlags = [];
            for (var f = 0; f < flagItems.length; f++) {{
                if (!setup.checkSingleCondition(flagItems[f])) {{
                    unmetFlags.push(flagItems[f]);
                }}
            }}

            if (unmetFlags.length > 0) {{
                // Flags not met - show actionable hint
                var flagHint = setup.getBestFlagHint(unmetFlags);
                return {{
                    activity: activity,
                    isLocked: false,
                    conditionsNotMet: true,
                    flagConditionsNotMet: true,
                    flagHint: flagHint
                }};
            }}

            // Flags met - check days_since_flag conditions
            var unmetDaysConditions = [];
            for (var d = 0; d < daysSinceFlagItems.length; d++) {{
                if (!setup.checkSingleCondition(daysSinceFlagItems[d])) {{
                    unmetDaysConditions.push(daysSinceFlagItems[d]);
                }}
            }}

            if (unmetDaysConditions.length > 0) {{
                // Days condition not met - check if actually need to wait
                var daysRemaining = setup.calculateDaysRemaining(unmetDaysConditions[0]);
                if (daysRemaining < 0) {{
                    // Flag not set yet — show as flag hint, not a wait message
                    var daysFlagHint = setup.getBestFlagHint([{{
                        type: 'flag', subject: 'player',
                        flag_key: unmetDaysConditions[0].flag_key,
                        operator: 'is_true'
                    }}]);
                    return {{
                        activity: activity,
                        isLocked: false,
                        conditionsNotMet: true,
                        flagConditionsNotMet: true,
                        flagHint: daysFlagHint
                    }};
                }}
                if (daysRemaining > 0) {{
                    // Still need to wait - show wait message
                    return {{
                        activity: activity,
                        isLocked: false,
                        conditionsNotMet: true,
                        daysConditionsNotMet: true,
                        daysRemaining: daysRemaining
                    }};
                }}
                // daysRemaining is 0 - condition effectively met, fall through
            }}
        }}

        // Check node-level conditions (for linked_canvas_node targeting)
        var nodeConditions = activity.node_conditions;
        if (nodeConditions && nodeConditions.items) {{
            var nodeItems = nodeConditions.items;
            var unmetNodeTraits = [];
            var unmetNodeFlags = [];
            for (var nc = 0; nc < nodeItems.length; nc++) {{
                if (!setup.checkSingleCondition(nodeItems[nc])) {{
                    if (nodeItems[nc].type === 'trait') unmetNodeTraits.push(nodeItems[nc]);
                    else if (nodeItems[nc].type === 'flag') unmetNodeFlags.push(nodeItems[nc]);
                }}
            }}

            if (unmetNodeTraits.length > 0) {{
                return {{
                    activity: activity,
                    isLocked: false,
                    conditionsNotMet: true,
                    nodeConditionsNotMet: true,
                    traitConditionsNotMet: true,
                    canvasConditions: {{ items: unmetNodeTraits, logic: nodeConditions.logic, version: '1.0' }}
                }};
            }}
            if (unmetNodeFlags.length > 0) {{
                var nodeFlagHint = setup.getBestFlagHint(unmetNodeFlags);
                return {{
                    activity: activity,
                    isLocked: false,
                    conditionsNotMet: true,
                    nodeConditionsNotMet: true,
                    flagConditionsNotMet: true,
                    flagHint: nodeFlagHint
                }};
            }}
        }}

        // Found next visitable activity - check if locked by traits
        var traitReqs = activity.trait_requirements || [];
        var missingTraits = [];

        for (var j = 0; j < traitReqs.length; j++) {{
            if (!setup.checkTraitRequirement(traitReqs[j])) {{
                missingTraits.push(traitReqs[j]);
            }}
        }}

        return {{
            activity: activity,
            isLocked: missingTraits.length > 0,
            missingTraits: missingTraits,
            conditionsNotMet: false
        }};
    }}

    return null; // All completed
}};

// Check if a trait requirement is met
setup.checkTraitRequirement = function(req) {{
    var player = State.variables.player || {{}};
    var traits = player.traits || {{}};
    var currentValue = traits[req.trait] || 0;

    switch (req.operator) {{
        case ">": return currentValue > req.value;
        case ">=": return currentValue >= req.value;
        case "<": return currentValue < req.value;
        case "<=": return currentValue <= req.value;
        case "==": return currentValue === req.value;
        default: return currentValue >= req.value;
    }}
}};

// Check a single condition item (trait or flag)
setup.checkSingleCondition = function(item) {{
    var sv = State.variables || {{}};

    if (item.type === 'flag') {{
        var flags = sv.flags || {{}};
        if (item.subject === 'player') {{
            if (item.operator === 'is_true') return flags[item.flag_key] === true;
            if (item.operator === 'is_false') return !flags[item.flag_key];
        }}
        return false;
    }}

    if (item.type === 'trait') {{
        var leftVal = null;
        if (item.subject === 'player') {{
            leftVal = ((sv.player || {{}}).core_traits || {{}})[item.trait_key];
        }} else if (item.subject === 'npc') {{
            var npcId = setup.resolveNpcId(item.npc_id || '');
            var npc = npcId ? ((sv.npcs || {{}})[npcId] || null) : null;
            leftVal = npc && npc.core_traits ? npc.core_traits[item.trait_key] : undefined;
        }}
        var rightVal = item.value;
        var op = item.operator;
        if (op === 'gte') return Number(leftVal) >= Number(rightVal);
        if (op === 'gt') return Number(leftVal) > Number(rightVal);
        if (op === 'lte') return Number(leftVal) <= Number(rightVal);
        if (op === 'lt') return Number(leftVal) < Number(rightVal);
        if (op === 'eq') return leftVal === rightVal;
        // `ne` added 2026-08-24. THIS IS THE SECOND EVALUATOR. compare() at the top
        // of this file has handled `ne` since v2 shipped, and the canvas/node/choice
        // path goes through that one -- but hints, quest cards and
        // _findFlagSetterCanvas all read the SAME condition item through here, and
        // without this line the identical item evaluated true on a canvas and false
        // in a quest card. Any operator added to compare() has to be added here too.
        if (op === 'ne') return leftVal !== rightVal;
        return false;
    }}

    if (item.type === 'pass') {{
        var isActive = setup.isPassActive(item.pass_id || '');
        if (item.operator === 'is_active') return isActive;
        if (item.operator === 'is_inactive') return !isActive;
        return false;
    }}

    if (item.type === 'item') {{
        var count = setup.getItemCount(item.item_id || '');
        var op = item.operator;
        var val = item.value || 0;
        if (op === 'gte') return count >= val;
        if (op === 'gt') return count > val;
        if (op === 'lte') return count <= val;
        if (op === 'lt') return count < val;
        if (op === 'eq') return count === val;
        return false;
    }}

    return false;
}};

// Find actionable hint for unmet flag conditions (with recursive chain resolution)
setup.getBestFlagHint = function(unmetFlags) {{
    var helpData = setup.help_data || {{}};
    var flagUnlockMap = helpData.flag_unlock_map || {{}};
    var startingCanvasId = helpData.starting_canvas_id;

    // First pass: find directly visitable unlock canvas
    for (var i = 0; i < unmetFlags.length; i++) {{
        var flagKey = unmetFlags[i].flag_key;
        var unlockInfo = flagUnlockMap[flagKey];

        if (unlockInfo) {{
            // Skip flags set by starting canvas (it plays automatically via "Start Game")
            if (startingCanvasId && unlockInfo.canvas_id === startingCanvasId) {{
                continue;
            }}

            var canvasConditions = unlockInfo.canvas_conditions;
            var isVisitable = !canvasConditions || setup.triggerConditionsSatisfied(canvasConditions);

            if (isVisitable) {{
                return {{
                    location: unlockInfo.location,
                    schedule: unlockInfo.schedule,
                    canvas_name: unlockInfo.canvas_name,
                    npc_name: unlockInfo.npc_name || null
                }};
            }}
        }}
    }}

    // Second pass: recursive chain resolution
    // If unlock canvas has flag conditions, find what unlocks THOSE flags
    var visited = {{}};
    for (var i = 0; i < unmetFlags.length; i++) {{
        var flagKey = unmetFlags[i].flag_key;
        var chainHint = setup.resolveUnlockChain(flagKey, flagUnlockMap, visited, 0);
        if (chainHint) {{
            return chainHint;
        }}
    }}

    // Final fallback: generic message (no specific hint available)
    return null;
}};

// Recursively resolve the unlock chain to find a visitable canvas
setup.resolveUnlockChain = function(flagKey, flagUnlockMap, visited, depth) {{
    // Prevent infinite loops and excessive depth
    if (depth > 10 || visited[flagKey]) return null;
    visited[flagKey] = true;

    var unlockInfo = flagUnlockMap[flagKey];
    if (!unlockInfo) return null;

    var canvasConditions = unlockInfo.canvas_conditions;

    // Check if this canvas is visitable
    if (!canvasConditions || setup.triggerConditionsSatisfied(canvasConditions)) {{
        return {{
            location: unlockInfo.location,
            schedule: unlockInfo.schedule,
            canvas_name: unlockInfo.canvas_name,
            npc_name: unlockInfo.npc_name || null
        }};
    }}

    // Canvas has conditions - check what's blocking it
    var items = canvasConditions.items || [];
    var helpData = setup.help_data || {{}};
    var startingCanvasId = helpData.starting_canvas_id;
    var hasUnresolvableCondition = false;

    for (var i = 0; i < items.length; i++) {{
        var item = items[i];
        var isFlagType = (item.type === 'flag');
        var isDaysSinceFlag = (item.type === 'days_since_flag');

        // Handle flag and days_since_flag conditions
        if ((isFlagType || isDaysSinceFlag) && !setup.triggerConditionsSatisfied({{ version: '1.0', items: [item] }})) {{
            var blockingFlagKey = item.flag_key;

            // Check if this flag is set by starting canvas (will be auto-met)
            var nestedUnlockInfo = flagUnlockMap[blockingFlagKey];
            if (startingCanvasId && nestedUnlockInfo && nestedUnlockInfo.canvas_id === startingCanvasId) {{
                continue; // Auto-met by starting canvas, skip this condition
            }}

            // Recurse to find hint for this blocking flag
            var nestedHint = setup.resolveUnlockChain(blockingFlagKey, flagUnlockMap, visited, depth + 1);
            if (nestedHint) {{
                return nestedHint;
            }}
            hasUnresolvableCondition = true;
        }}

        // Trait conditions that aren't met
        if (item.type === 'trait' && !setup.checkSingleCondition(item)) {{
            hasUnresolvableCondition = true;
        }}
    }}

    // If all blocking conditions were auto-met (skipped), this canvas IS visitable
    if (!hasUnresolvableCondition) {{
        return {{
            location: unlockInfo.location,
            schedule: unlockInfo.schedule,
            canvas_name: unlockInfo.canvas_name,
            npc_name: unlockInfo.npc_name || null
        }};
    }}

    // Trait conditions block this canvas, but we still have useful info
    // (npc_name, location) — return it so formatFlagHint can show "Progress with [NPC]"
    return {{
        location: unlockInfo.location,
        schedule: unlockInfo.schedule,
        canvas_name: unlockInfo.canvas_name,
        npc_name: unlockInfo.npc_name || null,
        traitBlocked: true
    }};
}};

// Format flag hint as "Visit X between Y" or "Progress with [NPC]" for cross-NPC
setup.formatFlagHint = function(hint, currentNpcName) {{
    if (!hint) return "Complete a prerequisite activity";

    // Cross-NPC or player canvas: hint points to a different entity's canvas
    var hintName = hint.npc_name;
    if (hintName === "player") {{
        var helpData = setup.help_data || {{}};
        hintName = (helpData.player && helpData.player.name) || "Player";
    }}
    if (hintName && currentNpcName && hintName !== currentNpcName) {{
        if (hint.is_phone) {{
            return "📱 Message " + hintName;
        }}
        return "Progress with " + hintName;
    }}

    // Phone conversation hint (same NPC)
    if (hint.is_phone && hint.npc_name) {{
        return "📱 Check your messages";
    }}

    if (hint.location && hint.schedule) {{
        return "Visit " + hint.location + " " + hint.schedule;
    }} else if (hint.location) {{
        return "Visit " + hint.location;
    }}
    return "Complete: " + (hint.canvas_name || "a prerequisite activity");
}};

// Format trait requirements as "Love > 30 and Trust > 20 required"
setup.formatTraitRequirements = function(missingTraits) {{
    if (!missingTraits || missingTraits.length === 0) return "";

    var parts = missingTraits.map(function(req) {{
        var traitName = req.trait.charAt(0).toUpperCase() + req.trait.slice(1);
        return traitName + " " + (req.operator || ">") + " " + req.value;
    }});

    return parts.join(" and ") + " required";
}};

// Calculate remaining days for a days_since_flag condition
setup.calculateDaysRemaining = function(condition) {{
    var sv = State.variables;
    var flagKey = condition.flag_key;
    var requiredDays = condition.value || 1;

    var meta = (sv.flags_meta || {{}})[String(flagKey)];
    var setDay = meta ? meta.set_day : null;

    // If flag not set yet, return -1 (caller should treat as unset flag, not a wait)
    if (setDay === null) return -1;

    var currentDay = (sv.game_state && sv.game_state.time_state) ? sv.game_state.time_state.day : 1;
    var daysSince = currentDay - setDay;
    var remaining = requiredDays - daysSince;

    return Math.max(0, remaining);
}};

// Format canvas trigger conditions as clickable links "Required: Elena Affection ≥ 50"
setup.formatCanvasConditions = function(conditions) {{
    if (!conditions || !conditions.items) return "Conditions not met";

    var parts = [];
    var items = conditions.items;

    for (var i = 0; i < items.length; i++) {{
        var item = items[i];

        if (item.type === "trait") {{
            // Format as clickable link: "Elena Affection ≥ 50" or "Your Boldness ≥ 40"
            var npcId = item.npc_id || "";
            var isPlayerTrait = item.subject === "player" || !npcId;
            var trait = item.trait_key;
            var value = item.value;
            var op = item.operator === "gte" ? "≥" :
                     item.operator === "gt" ? ">" :
                     item.operator === "lte" ? "≤" :
                     item.operator === "lt" ? "<" :
                     item.operator === "eq" ? "=" :
                     item.operator === "ne" ? "≠" : "≥";

            // Look up NPC display name via slug map, fall back to raw ID
            var displayNpc = "Your";
            if (!isPlayerTrait) {{
                var slugMap = setup.npc_slug_map || {{}};
                var npcsData = State.variables.npcs || {{}};
                var uuid = slugMap[npcId];
                var npcName = (uuid && npcsData[uuid]) ? (npcsData[uuid].name || npcId) : npcId;
                displayNpc = npcName + "'s";
            }}
            var displayTrait = trait.charAt(0).toUpperCase() + trait.slice(1);

            // Wrap in clickable span with data attributes
            var link = '<span class="trait-requirement-link" ' +
                'data-npc="' + npcId + '" ' +
                'data-trait="' + trait + '" ' +
                'data-value="' + value + '">' +
                displayNpc + ' ' + displayTrait + ' ' + op + ' ' + value +
                '</span>';
            parts.push(link);
        }}
        else if (item.type === "clothing_slot") {{
            var slotName = item.slot || "?";
            var slotOp = item.operator || "equipped";
            var displaySlot = slotName.charAt(0).toUpperCase() + slotName.slice(1);
            if (slotOp === "equipped") {{
                parts.push(displaySlot + " must be worn");
            }} else {{
                parts.push(displaySlot + " must be removed");
            }}
        }}
        else if (item.type === "clothing_item") {{
            var itemId = item.item_id || "?";
            var itemOp = item.operator || "equipped";
            // Look up display name from clothing_data
            var itemName = itemId;
            var cdata = setup.clothing_data || [];
            for (var ci = 0; ci < cdata.length; ci++) {{
                if (cdata[ci].id === itemId) {{ itemName = cdata[ci].name; break; }}
            }}
            if (itemOp === "equipped") {{
                parts.push("Wearing: " + itemName);
            }} else if (itemOp === "unequipped") {{
                parts.push("Not wearing: " + itemName);
            }} else if (itemOp === "owned") {{
                parts.push("Requires: " + itemName);
            }} else if (itemOp === "not_owned") {{
                parts.push("Must not own: " + itemName);
            }}
        }}
        else if (item.type === "npc_at_location") {{
            var nalLocId = item.location_id || item.location || "";
            var nalLocMap = setup._getLocUuidToSlug() || {{}};
            var nalLocSlug = nalLocMap[nalLocId] || nalLocId;
            var nalLocs = setup.locations || {{}};
            var nalLocName = (nalLocs[nalLocSlug] && nalLocs[nalLocSlug].name) ? nalLocs[nalLocSlug].name : nalLocSlug;
            var nalAbsent = (item.operator === "is_absent");
            var nalNpcId = item.npc_id || "";
            if (nalNpcId) {{
                var nalSlugMap = setup.npc_slug_map || {{}};
                var nalNpcsData = State.variables.npcs || {{}};
                var nalUuid = nalSlugMap[nalNpcId];
                var nalNpcName = (nalUuid && nalNpcsData[nalUuid]) ? (nalNpcsData[nalUuid].name || nalNpcId) : nalNpcId;
                parts.push(nalNpcName + (nalAbsent ? " must not be in " : " must be in ") + nalLocName);
            }} else {{
                parts.push(nalAbsent ? (nalLocName + " must be empty") : (nalLocName + " must be occupied"));
            }}
        }}
        else if (item.type === "time_of_day") {{
            var todStart = item.start_time || "00:00";
            var todEnd = item.end_time || "";
            parts.push(todEnd
                ? ("Only between " + todStart + " and " + todEnd)
                : ("Only at " + todStart));
        }}
        else if (item.type === "worn_exposure") {{
            var weOp = item.operator || "gte";
            var weSym = weOp === "gt" ? ">" : weOp === "lte" ? "≤" : weOp === "lt" ? "<" : weOp === "eq" ? "=" : "≥";
            var weWord = (item.value || 0) >= 2 ? "bare" : "showing";
            parts.push("She must be " + weWord + " (exposure " + weSym + " " + (item.value || 0) + ")");
        }}
        else if (item.type === "worn_corruption") {{
            var wcOp = item.operator || "gte";
            var wcSym = wcOp === "gt" ? ">" : wcOp === "lte" ? "≤" : wcOp === "lt" ? "<" : wcOp === "eq" ? "=" : "≥";
            parts.push("Outfit must be revealing (corruption " + wcSym + " " + (item.value || 0) + ")");
        }}
        else if (item.type === "worn_beauty") {{
            var wbOp = item.operator || "gte";
            var wbSym = wbOp === "gt" ? ">" : wbOp === "lte" ? "≤" : wbOp === "lt" ? "<" : wbOp === "eq" ? "=" : "≥";
            parts.push("Appearance " + wbSym + " " + (item.value || 0));
        }}
        else if (item.type === "worn_type") {{
            // Doc 72 / Doc 71 R2 — outfit-category gate
            var wtOpFmt = item.operator || "eq";
            var wtValFmt = item.value || "?";
            if (wtOpFmt === "neq") {{
                parts.push("Not wearing " + wtValFmt);
            }} else {{
                parts.push("Wearing " + wtValFmt);
            }}
        }}
        else if (item.type === "pass") {{
            var pConf = setup.passes_map[item.pass_id || ''];
            var pName = pConf ? pConf.name : item.pass_id;
            if (item.operator === 'is_active') {{
                parts.push(pName + " required");
            }} else {{
                parts.push(pName + " must be expired");
            }}
        }}
        else if (item.type === "item") {{
            var iConf = setup.items_map[item.item_id || ''];
            var iName = iConf ? iConf.name : item.item_id;
            var iOp = item.operator === "gte" ? "\u2265" :
                      item.operator === "gt" ? ">" :
                      item.operator === "lte" ? "\u2264" :
                      item.operator === "lt" ? "<" : "=";
            parts.push(iName + " " + iOp + " " + (item.value || 0));
        }}
        // Skip flag conditions - they're internal game mechanics, not player-actionable
    }}

    if (parts.length === 0) return "Conditions not met";
    var logic = conditions.logic === "OR" ? " or " : " and ";
    return "Required: " + parts.join(logic);
}};

// Format activity hint as "Visit X between Y"
setup.formatActivityHint = function(activity) {{
    var text = "";
    if (activity.location && activity.schedule) {{
        text = "Visit " + activity.location + " " + activity.schedule;
    }} else if (activity.location) {{
        text = "Visit " + activity.location;
    }} else {{
        text = activity.name;
    }}
    if (activity.guide_hint) {{
        text += '<br><span class="guide-hint">' + activity.guide_hint + '</span>';
    }}
    return text;
}};

// Get sidebar hint text — iterates player + NPCs, returns first useful hint
setup.getSidebarHint = function() {{
    var helpData = setup.help_data || {{}};
    var sources = [];

    if (helpData.player && helpData.player.activities) {{
        sources.push({{ id: "_player_", name: helpData.player.name }});
    }}
    if (helpData.npcs) {{
        Object.keys(helpData.npcs).forEach(function(npcId) {{
            sources.push({{ id: npcId, name: (State.variables.npcs[npcId] && State.variables.npcs[npcId].name) || helpData.npcs[npcId].name }});
        }});
    }}

    for (var i = 0; i < sources.length; i++) {{
        var next = setup.getNextActivity(sources[i].id);
        if (next === null) continue;

        // E10: stage-gated hints win priority — checked first.
        if (next.isStageHint && next.stageHint && next.stageHint.text) {{
            return next.stageHint.text;
        }}
        if (next.isStartingCanvas) return "Start the game";
        if (next.flagConditionsNotMet) return setup.formatFlagHint(next.flagHint, sources[i].name);
        if (next.traitConditionsNotMet) return setup.formatCanvasConditions(next.canvasConditions);
        if (next.daysConditionsNotMet) {{
            return next.daysRemaining === 1 ? "Come back tomorrow" : "Wait " + next.daysRemaining + " more days";
        }}
        if (!next.conditionsNotMet) return setup.formatActivityHint(next.activity);
    }}
    return "";
}};

// Show modal with activities that increase a specific trait for an NPC or player
setup.showTraitActivitiesModal = function(npcId, traitKey, requiredValue) {{
    var helpData = setup.help_data || {{}};
    var npcs = State.variables.npcs || {{}};

    // Detect if this is a player trait (empty/undefined npcId)
    var isPlayerTrait = !npcId || npcId === "";

    var displayName, currentValue, activities;

    if (isPlayerTrait) {{
        // Player trait - use player data and trait_activities index
        displayName = "Your";
        var playerData = State.variables.player || {{}};
        currentValue = (playerData.core_traits || {{}})[traitKey] || 0;

        // Get activities from trait_activities index that boost this trait for player
        var allTraitActivities = helpData.trait_activities ? helpData.trait_activities[traitKey] : [];
        activities = allTraitActivities.filter(function(act) {{
            // Check if any effect targets player (no npc_id) with this trait
            var effects = act.trait_effects || [];
            for (var e = 0; e < effects.length; e++) {{
                if (effects[e].trait === traitKey && !effects[e].npc_id && effects[e].value > 0) {{
                    return true;
                }}
            }}
            return false;
        }});
    }} else {{
        // NPC trait - use NPC data and NPC activities
        var resolvedId = setup.resolveNpcId(npcId);
        var npcData = npcs[resolvedId] || {{}};
        displayName = npcData.name || npcId.charAt(0).toUpperCase() + npcId.slice(1);
        currentValue = (npcData.core_traits || {{}})[traitKey] || 0;

        var npcHelpData = helpData.npcs ? helpData.npcs[resolvedId] : null;
        activities = npcHelpData ? npcHelpData.activities : [];
    }}

    // Filter to activities that:
    // 1. Have a location (skip intro activities)
    // 2. Canvas conditions met (NPC trait requirements)
    // 3. Activity trait requirements met (player traits)
    // 4. Increase the requested trait
    var relevantActivities = [];
    for (var i = 0; i < activities.length; i++) {{
        var act = activities[i];
        if (!act.location) continue; // Skip intro activities

        // Skip completed non-repeatable activities (story arc OR regular non-repeatable)
        if (act.is_repeatable === false || act.linked_flag) {{
            var flags = State.variables.flags || {{}};
            var hist = (State.variables.game_state && State.variables.game_state.trigger_history) || {{}};
            var isCompleted = (act.linked_flag && flags[act.linked_flag]) ||
                              (act.canvas_id && hist[act.canvas_id] && hist[act.canvas_id].total > 0);
            if (isCompleted) continue;
        }}

        // Check canvas conditions (NPC trait requirements like "Elena Affection >= 30")
        var canvasConditions = act.canvas_conditions;
        if (canvasConditions && !setup.triggerConditionsSatisfied(canvasConditions)) {{
            continue; // Skip - canvas conditions not met
        }}

        // Check activity trait requirements (player traits)
        var traitReqs = act.trait_requirements || [];
        var isLocked = false;
        for (var r = 0; r < traitReqs.length; r++) {{
            if (!setup.checkTraitRequirement(traitReqs[r])) {{
                isLocked = true;
                break;
            }}
        }}
        if (isLocked) continue; // Skip locked activities

        // Check if this activity boosts the requested trait
        // Tiered activities: only show effects from accessible tiers
        // Non-tiered: use flat trait_effects (legacy)
        var tieredEffects = act.tiered_effects;
        if (tieredEffects && tieredEffects.length > 0) {{
            var bestBonus = 0;
            for (var t = 0; t < tieredEffects.length; t++) {{
                var tier = tieredEffects[t];
                if (tier.conditions && !setup.triggerConditionsSatisfied(tier.conditions)) {{
                    continue;
                }}
                var tierEffs = tier.effects || [];
                for (var te = 0; te < tierEffs.length; te++) {{
                    var tEff = tierEffs[te];
                    var tMatch = tEff.trait === traitKey && tEff.value > 0;
                    var tTarget = isPlayerTrait ? !tEff.npc_id : true;
                    if (tMatch && tTarget && tEff.value > bestBonus) {{
                        bestBonus = tEff.value;
                    }}
                }}
            }}
            if (bestBonus > 0) {{
                relevantActivities.push({{
                    name: act.name,
                    location: act.location,
                    schedule: act.schedule,
                    bonus: bestBonus,
                    is_random: act.is_random || false
                }});
            }}
        }} else {{
            var effects = act.trait_effects || [];
            for (var j = 0; j < effects.length; j++) {{
                var eff = effects[j];
                var traitMatches = eff.trait === traitKey && eff.value > 0;
                var targetMatches = isPlayerTrait ? !eff.npc_id : true;
                if (traitMatches && targetMatches) {{
                    relevantActivities.push({{
                        name: act.name,
                        location: act.location,
                        schedule: act.schedule,
                        bonus: eff.value,
                        is_random: act.is_random || false
                    }});
                    break;
                }}
            }}
        }}
    }}

    // Deduplicate by name: keep only highest bonus per activity name
    var byName = {{}};
    for (var d = 0; d < relevantActivities.length; d++) {{
        var ra = relevantActivities[d];
        if (!byName[ra.name] || byName[ra.name].bonus < ra.bonus) {{
            byName[ra.name] = ra;
        }}
    }}
    relevantActivities = Object.values(byName);

    // Build modal HTML (no inline onclick - use jQuery event delegation)
    var traitDisplay = traitKey.charAt(0).toUpperCase() + traitKey.slice(1);
    var html = '<div class="trait-modal-overlay">';
    html += '<div class="trait-modal">';
    html += '<div class="trait-modal-header">';
    var titlePossessive = isPlayerTrait ? (displayName + ' ') : (displayName + "'s ");
    html += '<h3>How to increase ' + titlePossessive + traitDisplay + '</h3>';
    html += '<span class="trait-modal-close">×</span>';
    html += '</div>';
    html += '<div class="trait-modal-progress">';
    html += 'Current: ' + currentValue + ' / Required: ' + requiredValue;
    html += '</div>';
    html += '<div class="trait-modal-body">';

    if (relevantActivities.length === 0) {{
        html += '<p>No activities found that increase this trait.</p>';
    }} else {{
        html += '<ul class="trait-activity-list">';
        for (var k = 0; k < relevantActivities.length; k++) {{
            var ra = relevantActivities[k];
            html += '<li>';
            html += '<span class="activity-name">' + ra.name + '</span>';
            html += '<span class="activity-bonus">+' + ra.bonus + ' ' + traitDisplay + '</span>';
            html += '<div class="activity-hint">→ ' + (ra.is_random ? 'Random event at ' : 'Visit ') + ra.location;
            if (ra.schedule) html += ' ' + ra.schedule;
            html += '</div>';
            html += '</li>';
        }}
        html += '</ul>';
    }}

    html += '</div></div></div>';

    jQuery(html).appendTo('#story');
}};

// Close trait activities modal
setup.closeTraitModal = function() {{
    jQuery('.trait-modal-overlay').remove();
}};

// ============== END QUEST PAGE HELPERS ==============

// Auto-inference for games without author-defined story arc
setup.autoInferStoryPosition = function() {{
    var result = {{
        current_chapter: {{
            id: "auto_chapter",
            name: "Your Story",
            mood: "developing",
            description: "Your adventure continues..."
        }},
        completed_nodes: [],
        available_nodes: [],
        locked_nodes: [],
        active_groups: [],
        is_stuck: false,
        progress_percent: 0,
        is_auto_inferred: true
    }};

    // Check completed canvases from game state
    if (State.variables.game_state && State.variables.game_state.completed_canvases) {{
        State.variables.game_state.completed_canvases.forEach(function(canvasId) {{
            // Avoid duplicates
            var existing = result.completed_nodes.find(function(n) {{ return n.id === canvasId; }});
            if (!existing) {{
                result.completed_nodes.push({{
                    id: canvasId,
                    name: canvasId.replace(/_/g, " "),
                    chapter: "auto_chapter",
                    journal_entry: "A chapter of your story...",
                    is_milestone: true
                }});
            }}
        }});
    }}

    // Calculate progress estimate
    var total = result.completed_nodes.length + result.available_nodes.length + result.locked_nodes.length;
    if (total > 0) {{
        result.progress_percent = Math.round((result.completed_nodes.length / total) * 100);
    }}

    result.is_stuck = result.available_nodes.length === 0 && result.locked_nodes.length > 0;

    return result;
}};

// Initialize trait requirement click handlers (event delegation)
jQuery(document).on('click', '.trait-requirement-link', function(e) {{
    e.preventDefault();
    var npcId = jQuery(this).data('npc');
    var trait = jQuery(this).data('trait');
    var value = jQuery(this).data('value');
    setup.showTraitActivitiesModal(npcId, trait, value);
}});

// Modal close handlers (event delegation)
jQuery(document).on('click', '.trait-modal-overlay', function(e) {{
    // Close when clicking overlay (but not modal content)
    if (jQuery(e.target).hasClass('trait-modal-overlay')) {{
        setup.closeTraitModal();
    }}
}});

jQuery(document).on('click', '.trait-modal-close', function(e) {{
    e.preventDefault();
    setup.closeTraitModal();
}});
{wardrobe_handlers_block}
{shop_handlers_block}
{phone_handlers_block}


:: Start
<<set $player = {player_init_json}>>\
<<set $npcs = {npc_map_json}>>\
<<set $npc_interacted_today = {{}}>>\
<<set $flags = {flags_init_json}>>\
<<set $flags_meta = {{}}>>\
<<set $game_state = {game_state_init_json}>>\
<<nobr>>
<div class="game-intro">
<h1>{project_name}</h1>
<p class="game-description">{project_description}</p>
<div class="developer-intro">
<p class="developer-about">We're a small indie studio crafting intimate, story-driven experiences. Every game is made with care, and your support helps us keep creating. If you enjoy our work, consider supporting us!</p>
<p class="support-link">👉 <a href="{support_url}" target="_blank" rel="noopener">Support us on Patreon</a></p>
</div>
<div class="age-gate">
<p class="age-warning">⚠️ This game contains adult content intended for players 18 years of age or older.</p>
<div class="age-buttons">
[[✓ I am 18 or older - Enter Game->{start_target}]]
[[✗ I am NOT 18 or older->AgeBlocked]]
</div>
</div>
<div class="developer-footer">
<p class="developer-credit">Developed by <strong>{studio_name}</strong></p>
<p class="support-link">👉 <a href="{support_url}" target="_blank" rel="noopener">Support us on Patreon</a></p>
</div>
</div>
<</nobr>>"""

    def _generate_age_blocked_passage(self) -> str:
        """Generate the AgeBlocked passage for users who are not 18+."""
        return """:: AgeBlocked
<div class="blocked-page">
<h2>Access Denied</h2>
<p>This content is not available for you.</p>
<p>Please close this page.</p>
</div>"""

    # ───────── Theme System ─────────

    @staticmethod
    def _hex_to_rgb(hex_color: str) -> tuple:
        """Convert '#rrggbb' to (r, g, b) tuple."""
        h = hex_color.lstrip("#")
        if len(h) == 3:
            h = h[0]*2 + h[1]*2 + h[2]*2
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

    @classmethod
    def _rgba(cls, hex_color: str, alpha: float) -> str:
        """Convert hex + alpha to 'rgba(r, g, b, a)' CSS value."""
        r, g, b = cls._hex_to_rgb(hex_color)
        return f"rgba({r}, {g}, {b}, {alpha})"

    @classmethod
    def _darken(cls, hex_color: str, amount: float) -> str:
        """Darken a hex color by amount (0-1). Returns '#rrggbb'."""
        r, g, b = cls._hex_to_rgb(hex_color)
        r = max(0, int(r * (1 - amount)))
        g = max(0, int(g * (1 - amount)))
        b = max(0, int(b * (1 - amount)))
        return f"#{r:02x}{g:02x}{b:02x}"

    @classmethod
    def _lighten(cls, hex_color: str, amount: float) -> str:
        """Lighten a hex color by amount (0-1). Returns '#rrggbb'."""
        r, g, b = cls._hex_to_rgb(hex_color)
        r = min(255, int(r + (255 - r) * amount))
        g = min(255, int(g + (255 - g) * amount))
        b = min(255, int(b + (255 - b) * amount))
        return f"#{r:02x}{g:02x}{b:02x}"

    def _auto_emit_counter_sidebar_items(self) -> None:
        """E18 — auto-emit trait_bar sidebar items for counter traits used in
        stage helpers. Skips traits the author already authored a sidebar item
        for. Picks the LOWEST helper threshold per counter (the most-immediate
        gate the player is racing toward)."""
        # Map counter trait_key → (min_threshold, label_hint)
        counters: dict[str, int] = {}
        for helper in (self.stage_helpers or []):
            conds = (helper.get("conditions") or {}).get("items") or []
            for it in conds:
                if not isinstance(it, dict):
                    continue
                if it.get("type") != "trait":
                    continue
                if it.get("subject") != "player":
                    continue
                key = it.get("trait_key", "")
                if not (key.endswith("_count") or key.endswith("_done")):
                    continue
                op = it.get("operator", "")
                val = it.get("value")
                if op != "gte" or not isinstance(val, (int, float)):
                    continue
                cur_min = counters.get(key)
                if cur_min is None or val < cur_min:
                    counters[key] = int(val)
        if not counters:
            return
        # Skip counters the author already added a sidebar item for.
        existing_traits = {
            si.get("trait") for si in self.sidebar_items
            if isinstance(si, dict) and si.get("type") == "trait_bar"
        }
        for trait_key, max_val in sorted(counters.items()):
            if trait_key in existing_traits:
                continue
            # Build a human-readable label: frank_bookkeeping_count → "Frank bookkeeping"
            base = trait_key.replace("_count", "").replace("_done", "")
            label = base.replace("_", " ").strip().capitalize()
            self.sidebar_items.append({
                "type": "trait_bar",
                "trait": trait_key,
                "label": label,
                "max": max_val,
                # Hide once the gate is cleared (counter exceeds max).
                "show_when": {
                    "version": "1.0",
                    "logic": "AND",
                    "items": [
                        {
                            "type": "trait",
                            "subject": "player",
                            "trait_key": trait_key,
                            "operator": "lt",
                            "value": max_val,
                        }
                    ],
                },
                "_auto_emitted": True,
            })

    def _auto_emit_decay_warning_sidebar_items(self) -> None:
        """E20 — auto-emit a single trait_decay_warning sidebar item if any
        decaying traits exist. Render-time logic compares snapshots vs current
        and shows an amber banner when a tracked trait dropped today AND is
        within 2.0 of the next stage gate. Snapshot is populated in advanceDay.
        """
        # Only emit if at least one trait has decay configured. Use the already-
        # loaded class fields (populated earlier in _load_project_data).
        any_decay = bool(getattr(self, "player_trait_decay_config", None)) or bool(
            getattr(self, "npc_trait_decay_config", None)
        )
        if not any_decay:
            return
        # Skip if author already added one.
        for si in self.sidebar_items:
            if isinstance(si, dict) and si.get("type") == "trait_decay_warning":
                return
        # Build a map of trait_key → list of helper thresholds, used at render
        # time to find "next gate above current value" for warning trigger.
        trait_thresholds: dict[str, list[dict[str, Any]]] = {}
        for helper in (self.stage_helpers or []):
            conds = (helper.get("conditions") or {}).get("items") or []
            for it in conds:
                if not isinstance(it, dict):
                    continue
                if it.get("type") != "trait":
                    continue
                op = it.get("operator", "")
                val = it.get("value")
                if op not in ("gte", "gt") or not isinstance(val, (int, float)):
                    continue
                # Build a synthetic key: subject:[npc_id:]trait_key
                subj = it.get("subject", "")
                key = it.get("trait_key", "")
                npc_id = it.get("npc_id", "")
                synth = f"{subj}:{npc_id}:{key}" if subj == "npc" else f"player::{key}"
                trait_thresholds.setdefault(synth, []).append({
                    "value": int(val),
                    "subject": subj,
                    "npc_id": npc_id,
                    "trait_key": key,
                })
        self.sidebar_items.append({
            "type": "trait_decay_warning",
            "thresholds": trait_thresholds,
            "_auto_emitted": True,
        })

    def _build_stage_setter_canvases_index(self) -> dict:
        """Pattern 2: scan canvases for branch-inside-shell stage setters.

        Returns: {npc_slug: {stage_value: canvas_slug_or_id}}.

        Walks every story canvas's nodes' exit_block; checks both choice-level
        effects and config-level effects (raw dicts for location-type
        exit_blocks). Records canvases whose effects set `<npc>_stage = N`
        (op="set", numeric value). The canvas identifier stored is the slug
        used in `setup.canvases_by_id` (via passage_name_map) when available,
        else the canvas UUID.

        Used by setup.computeHintGoal as a fallback when no helper exists
        for the next-stage transition (Frank 1→2 sets npc_frank_stage = 2
        inside scene_living_room_evening choices).
        """
        index: Dict[str, Dict[int, str]] = {}
        # Only consider NPCs with arc_stages — they are the only ones whose
        # `<slug>_stage` trait is meaningful.
        all_npc_slugs = set(self.npc_arc_stages_map.keys()) if getattr(
            self, "npc_arc_stages_map", None
        ) else set()
        if not all_npc_slugs:
            return index
        for canvas in (self.story_canvases or []):
            cv_id = str(getattr(canvas, "id", "") or "")
            try:
                cv_nodes = list(self._get_canvas_nodes_ordered(canvas))
            except Exception:
                cv_nodes = []
            for node in cv_nodes:
                eb = getattr(node, "exit_block", {}) or {}
                if not isinstance(eb, dict):
                    continue
                effect_dicts: List[Dict[str, Any]] = []
                cfg = eb.get("config") or {}
                if isinstance(cfg, dict):
                    for e in (cfg.get("effects") or []):
                        if isinstance(e, dict):
                            effect_dicts.append(e)
                for choice in (eb.get("choices") or []):
                    if not isinstance(choice, dict):
                        continue
                    for e in (choice.get("effects") or []):
                        if isinstance(e, dict):
                            effect_dicts.append(e)
                for e in effect_dicts:
                    if e.get("op") != "set":
                        continue
                    trait_key = e.get("trait", "")
                    val = e.get("value")
                    if not isinstance(trait_key, str) or not trait_key.endswith("_stage"):
                        continue
                    if not isinstance(val, (int, float)):
                        continue
                    npc_slug = trait_key[: -len("_stage")]
                    if npc_slug not in all_npc_slugs:
                        continue
                    index.setdefault(npc_slug, {})[int(val)] = cv_id
        return index

    def _is_dev_shortcut_canvas(self, canvas) -> bool:
        """True if this canvas is a DEV SHORTCUT — a jump/teleport authored for
        testing, gated on the `dev_mode_enabled` flag in its trigger.

        The flag is set at StoryInit ONLY in `--dev` builds (see flags_init_map),
        so these canvases never fire in a shipped game. The trigger condition is a
        MARKER, not a real gate: the sidebar `<<devJumps>>` widget reaches them by
        direct Engine.play, and the flag-chain validator + hint index both SKIP
        them (a dev jump is not a narrative node — it must not win as a flag setter,
        pollute quest guidance, or trip the located-setter check). Single source of
        truth for all three call sites.
        """
        trigger = getattr(canvas, "trigger", None)
        if not trigger:
            return False
        try:
            conds = trigger.conditions or {}
            items = conds.get("items", []) if isinstance(conds, dict) else []
            return any(
                isinstance(it, dict)
                and it.get("flag_key") == "dev_mode_enabled"
                and it.get("operator") == "is_true"
                for it in items
            )
        except Exception:
            return False

    def _dev_shortcut_jumps(self) -> list:
        """List of {label, passage} for every dev-shortcut canvas, for the sidebar
        `<<devJumps>>` widget. Each entry links to the canvas's FIRST node passage
        (Engine.play jumps straight in, bypassing the trigger). Empty when there are
        no dev shortcuts. Only consulted in `--dev` builds."""
        jumps = []
        for canvas in (self.story_canvases or []):
            if not self._is_dev_shortcut_canvas(canvas):
                continue
            try:
                nodes = list(self._get_canvas_nodes_ordered(canvas))
            except Exception:
                nodes = []
            if not nodes:
                continue
            canvas_prefix = self._sanitize_canvas_name(self._get_canvas_slug(canvas))
            passage = self._node_passage_name("Canvas", canvas_prefix, nodes[0])
            jumps.append({"label": canvas.name or canvas_prefix, "passage": passage})
        return jumps

    def _build_flag_setter_canvases_index(self) -> dict:
        """Pattern 2 v2.1 (2026-05-04): scan canvases for flag-setter effects.

        Returns: {flag_key: canvas_id} — first non-dev setter wins.

        Walks every story canvas's nodes' exit_block.flagEffects (config-level
        for location-type exits, and choice-level for choices-type exits).
        Records the first canvas whose flagEffects set each flag (op="set").
        Skips canvases gated on `dev_mode_enabled` so dev shortcuts don't
        win over canonical narrative scenes.

        Used by setup.computeHintGoal's State B branch — when a stage helper
        has an unmet flag gate AND all non-flag gates are met, the goal block
        switches to the "Where" frame and uses this index to look up the
        canvas the player needs to find to set the flag.
        """
        index: Dict[str, str] = {}
        for canvas in (self.story_canvases or []):
            cv_id = str(getattr(canvas, "id", "") or "")
            # Skip dev-shortcut canvases — a dev jump must not win as a flag setter.
            if self._is_dev_shortcut_canvas(canvas):
                continue
            try:
                cv_nodes = list(self._get_canvas_nodes_ordered(canvas))
            except Exception:
                cv_nodes = []
            for node in cv_nodes:
                eb = getattr(node, "exit_block", {}) or {}
                if not isinstance(eb, dict):
                    continue
                flag_effect_dicts: List[Dict[str, Any]] = []
                cfg = eb.get("config") or {}
                if isinstance(cfg, dict):
                    for e in (cfg.get("flagEffects") or []):
                        if isinstance(e, dict):
                            flag_effect_dicts.append(e)
                for choice in (eb.get("choices") or []):
                    if not isinstance(choice, dict):
                        continue
                    for e in (choice.get("flagEffects") or []):
                        if isinstance(e, dict):
                            flag_effect_dicts.append(e)
                for e in flag_effect_dicts:
                    if e.get("op") != "set":
                        continue
                    flag_key = e.get("flag", "")
                    if not isinstance(flag_key, str) or not flag_key:
                        continue
                    # First non-dev setter wins (slice scope; dev shortcuts excluded above)
                    if flag_key not in index:
                        index[flag_key] = cv_id
        return index

    def _build_sub_menu_parent_index(self) -> dict:
        """Map triggerless sub-menu canvases back to their parent menu canvas (2026-05-09).

        Returns: {child_canvas_id: parent_canvas_id} (UUIDs, first parent wins).

        When a canvas exposes a cross-canvas `targetType="node"` choice with a
        nodeId of the form `<canvas_id>.<node_id>` OR a raw node UUID, the
        target node's canvas becomes a "child" of the choice's owning canvas.
        For our purposes only triggerless children matter (triggered children
        are already in locationCanvases and lookup works directly); but we
        index ALL parent→child relationships and let the JS-side lookup ignore
        parents that themselves aren't in locationCanvases.

        Used by setup._findFlagSetterCanvas to walk back from a triggerless
        flag-setter canvas to a parent menu canvas that IS in locationCanvases,
        so State B's Where-frame can surface 📍 location + 🕒 schedule from
        the parent menu hub instead of returning null.

        Mirrors the closure pass at _compute_included_canvases (line 354) but
        builds an explicit index instead of just collecting reachable IDs.
        """
        from apps.stories.models import StoryNode

        index: Dict[str, str] = {}
        for canvas in (self.story_canvases or []):
            parent_id = str(getattr(canvas, "id", "") or "")
            if not parent_id:
                continue
            try:
                cv_nodes = list(self._get_canvas_nodes_ordered(canvas))
            except Exception:
                cv_nodes = []
            for node in cv_nodes:
                eb = getattr(node, "exit_block", {}) or {}
                if not isinstance(eb, dict):
                    continue
                if eb.get("type") != "choices":
                    continue
                for choice in (eb.get("choices") or []):
                    if not isinstance(choice, dict):
                        continue
                    if choice.get("targetType") != "node":
                        continue
                    target_node_id = choice.get("nodeId")
                    if not target_node_id:
                        continue
                    # Resolve target node UUID → canvas UUID. nodeId may be a
                    # raw UUID (after template_import resolves "canvas_id.node_id")
                    # or still in the dotted form pre-resolution. Try UUID first.
                    try:
                        target_node = self._node_by_id(target_node_id)
                        if not target_node:
                            continue
                        child_id = str(target_node.canvas_id)
                    except Exception:
                        continue
                    if not child_id or child_id == parent_id:
                        continue
                    # First parent wins — keeps lookup deterministic and
                    # matches the spirit of flag_setter_canvases.
                    if child_id not in index:
                        index[child_id] = parent_id
        return index

    def _resolve_theme(self, raw: dict) -> dict:
        """Resolve theme config into a complete set of CSS token values.

        Fills in derived values from mode, user overrides take precedence.
        Returns a dict ready for CSS variable generation.
        """
        mode = raw.get("mode", "dark")

        # Mode-derived base colors
        if mode == "dark":
            defaults = {
                "bg": "#0f0f1a",
                "surface": "#1a1a2e",
                "surface_alt": "#16213e",
                "border": "#333333",
                "text": "#e0e0e0",
                "text_muted": "#9aa0ab",  # ≈4.6:1 on surface — clears WCAG 4.5:1 for the small uppercase labels (was #888888 ≈3.6:1)
            }
        else:
            defaults = {
                "bg": "#ffffff",
                "surface": "#f8f9fa",
                "surface_alt": "#e9ecef",
                "border": "#dee2e6",
                "text": "#212529",
                "text_muted": "#6c757d",
            }

        # User-defined accent colors (with defaults)
        primary = raw.get("primary") or "#4a90d9"
        secondary = raw.get("secondary") or "#764ba2"
        accent = raw.get("accent") or "#4ecdc4"
        success = raw.get("success") or "#22c55e"
        danger = raw.get("danger") or "#dc3545"
        warning = raw.get("warning") or "#ffc107"

        # Base colors — user overrides take precedence over mode defaults
        bg = raw.get("bg") or defaults["bg"]
        surface = raw.get("surface") or defaults["surface"]
        surface_alt = raw.get("surface_alt") or defaults["surface_alt"]
        border = raw.get("border") or defaults["border"]
        text = raw.get("text") or defaults["text"]
        text_muted = raw.get("text_muted") or defaults["text_muted"]

        # Computed derived tokens
        text_strong = self._darken(text, 0.15) if mode == "light" else self._lighten(text, 0.15)
        text_secondary = text_muted  # alias
        surface_hover = self._darken(surface, 0.08) if mode == "light" else self._lighten(surface, 0.08)

        # RGBA background tints
        primary_bg = self._rgba(primary, 0.1)
        success_bg = self._rgba(success, 0.1)
        danger_bg = self._rgba(danger, 0.1)
        warning_bg = self._rgba(warning, 0.15)
        warning_text = self._darken(warning, 0.45) if mode == "light" else self._lighten(warning, 0.3)

        # Journal-specific derivations
        if mode == "dark":
            journal = {
                "bg": "#2a2318",
                "bg_end": "#1f1a12",
                "text": "#d4c4a8",
                "text_muted": "#a89070",
                "border": "#3a2f20",
                "accent": "#8b7355",
            }
        else:
            journal = {
                "bg": "#fdf6e3",
                "bg_end": "#f5e6d3",
                "text": "#5d4e37",
                "text_muted": "#8b7355",
                "border": "#c9b896",
                "accent": "#6d5a40",
            }

        return {
            "mode": mode,
            # Base
            "bg": bg,
            "surface": surface,
            "surface_alt": surface_alt,
            "border": border,
            "text": text,
            "text_muted": text_muted,
            "text_strong": text_strong,
            "text_secondary": text_secondary,
            "surface_hover": surface_hover,
            # Accents
            "primary": primary,
            "secondary": secondary,
            "accent": accent,
            "success": success,
            "danger": danger,
            "warning": warning,
            # Tinted backgrounds
            "primary_bg": primary_bg,
            "success_bg": success_bg,
            "danger_bg": danger_bg,
            "warning_bg": warning_bg,
            "warning_text": warning_text,
            # Typography
            "font_heading": raw.get("font_heading") or "Georgia, serif",
            "font_mono": raw.get("font_mono") or "'Courier New', monospace",
            # Shape
            "border_radius": raw.get("border_radius") or "8px",
            # Journal
            "journal_bg": journal["bg"],
            "journal_bg_end": journal["bg_end"],
            "journal_text": journal["text"],
            "journal_text_muted": journal["text_muted"],
            "journal_border": journal["border"],
            "journal_accent": journal["accent"],
            # Custom CSS
            "custom_css": raw.get("custom_css") or "",
        }

    def _generate_theme_stylesheet(self) -> str:
        """Generate CSS custom properties as a stylesheet passage."""
        t = self.theme
        custom = t.get("custom_css", "")
        custom_block = f"\n/* Custom CSS */\n{custom}" if custom else ""
        return f""":: ThemeStyles [stylesheet]
:root {{
    /* Base */
    --theme-bg: {t['bg']};
    --theme-surface: {t['surface']};
    --theme-surface-alt: {t['surface_alt']};
    --theme-surface-hover: {t['surface_hover']};
    --theme-border: {t['border']};
    --theme-text: {t['text']};
    --theme-text-muted: {t['text_muted']};
    --theme-text-strong: {t['text_strong']};
    --theme-text-secondary: {t['text_secondary']};
    /* Accents */
    --theme-primary: {t['primary']};
    --theme-secondary: {t['secondary']};
    --theme-accent: {t['accent']};
    --theme-success: {t['success']};
    --theme-danger: {t['danger']};
    --theme-warning: {t['warning']};
    /* Tinted backgrounds */
    --theme-primary-bg: {t['primary_bg']};
    --theme-success-bg: {t['success_bg']};
    --theme-danger-bg: {t['danger_bg']};
    --theme-warning-bg: {t['warning_bg']};
    --theme-warning-text: {t['warning_text']};
    /* Typography */
    --theme-font-heading: {t['font_heading']};
    --theme-font-mono: {t['font_mono']};
    /* Shape */
    --theme-radius: {t['border_radius']};
    /* Journal */
    --journal-bg: {t['journal_bg']};
    --journal-bg-end: {t['journal_bg_end']};
    --journal-text: {t['journal_text']};
    --journal-text-muted: {t['journal_text_muted']};
    --journal-border: {t['journal_border']};
    --journal-accent: {t['journal_accent']};
}}{custom_block}
"""

    def _generate_phone_css(self) -> str:
        """Generate phone system CSS as a stylesheet passage."""
        return """:: PhoneStyles [stylesheet]
/* ========== PHONE SYSTEM ========== */
.phone-overlay {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0, 0, 0, 0.65);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 10001;
}
.phone-frame {
    width: 340px;
    max-width: 92vw;
    height: 600px;
    max-height: 85vh;
    background: #1a1a2e;
    border-radius: 28px;
    border: 3px solid #333;
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    display: flex;
    flex-direction: column;
    overflow: hidden;
}
.phone-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 16px;
    background: #16213e;
    border-bottom: 1px solid #333;
    flex-shrink: 0;
}
.phone-title { font-weight: 600; font-size: 16px; color: #e0e0e0; }
.phone-close { font-size: 22px; color: #999; cursor: pointer; padding: 0 4px; }
.phone-close:hover { color: #fff; }
.phone-back { font-size: 18px; color: #7ec8e3; cursor: pointer; padding: 0 4px; }
.phone-back:hover { color: #fff; }
.phone-screen { flex: 1; overflow-y: auto; padding: 0; }

/* App Grid (home screen) */
.phone-app-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    padding: 24px 16px;
}
.phone-app-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    cursor: pointer;
}
.phone-app-item:hover .phone-app-icon-wrap { transform: scale(1.08); }
.phone-app-icon-wrap {
    position: relative;
    width: 56px;
    height: 56px;
    border-radius: 14px;
    overflow: visible;
    transition: transform 0.15s ease;
}
.phone-app-icon-img {
    width: 56px;
    height: 56px;
    border-radius: 14px;
    object-fit: cover;
}
.phone-app-icon-letter {
    width: 56px;
    height: 56px;
    border-radius: 14px;
    background: linear-gradient(135deg, var(--theme-primary) 0%, var(--theme-secondary) 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    font-weight: bold;
    color: #fff;
}
.phone-app-badge {
    position: absolute;
    top: -4px; right: -4px;
    background: var(--theme-danger);
    color: #fff;
    font-size: 11px;
    font-weight: bold;
    min-width: 18px;
    height: 18px;
    border-radius: 9px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0 4px;
}
.phone-app-label { font-size: 11px; color: #ccc; text-align: center; }

/* Thread List */
.phone-thread-list { display: flex; flex-direction: column; }
.phone-thread-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    border-bottom: 1px solid #2a2a3e;
    cursor: pointer;
}
.phone-thread-item:hover { background: #1e2a45; }
.phone-thread-unread { background: rgba(126, 200, 227, 0.06); }
.phone-thread-avatar-wrap { flex-shrink: 0; }
.phone-thread-avatar {
    width: 44px; height: 44px;
    border-radius: 50%;
    object-fit: cover;
}
.phone-thread-avatar-letter {
    width: 44px; height: 44px;
    border-radius: 50%;
    background: #3a3a5a;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    font-weight: bold;
    color: #ccc;
}
.phone-thread-info { flex: 1; min-width: 0; }
.phone-thread-name { font-weight: 600; font-size: 14px; color: #e0e0e0; }
.phone-thread-preview {
    font-size: 12px; color: #888;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.phone-thread-badge {
    background: var(--theme-danger); color: #fff;
    font-size: 10px; font-weight: bold;
    padding: 1px 5px; border-radius: 8px; margin-left: 6px;
}

/* Chat Bubbles */
.phone-chat-messages {
    display: flex;
    flex-direction: column;
    gap: 6px;
    padding: 12px;
    min-height: 100%;
}
.phone-bubble {
    max-width: 80%;
    padding: 8px 12px;
    border-radius: 16px;
    font-size: 13px;
    line-height: 1.4;
    word-wrap: break-word;
}
.phone-bubble-npc {
    align-self: flex-start;
    background: #2a3a5e;
    color: #e0e0e0;
    border-bottom-left-radius: 4px;
}
.phone-bubble-player {
    align-self: flex-end;
    background: var(--theme-primary);
    color: #fff;
    border-bottom-right-radius: 4px;
}

/* Reply Options */
.phone-reply-options {
    display: flex;
    flex-direction: column;
    gap: 6px;
    align-self: flex-end;
    max-width: 85%;
    margin-top: 4px;
}
.phone-reply-btn {
    background: transparent;
    border: 1px solid var(--theme-primary);
    color: var(--theme-primary);
    padding: 8px 14px;
    border-radius: 16px;
    font-size: 13px;
    cursor: pointer;
    text-align: right;
    transition: background 0.15s;
}
.phone-reply-btn:hover { background: rgba(10, 132, 255, 0.15); }

/* Daily chat topics */
.phone-daily-topics {
    padding: 12px;
    border-top: 1px solid #2a2a3e;
}
.phone-daily-label {
    font-size: 12px;
    color: #888;
    margin-bottom: 8px;
}
.effect-toast.phone-notify { background: #0a84ff; }
.phone-daily-locked { color: #888; font-size: 13px; padding: 6px 14px; text-align: right; opacity: 0.75; }
.phone-quests { padding: 8px; }
.phone-quest-card { background: rgba(255,255,255,0.06); border-radius: 10px; padding: 10px 12px; margin-bottom: 8px; }
.phone-quest-card.quest-completed { opacity: 0.6; }
.phone-quest-name { font-weight: bold; margin-bottom: 4px; }
.phone-quest-step { font-size: 13px; color: #bbb; }
.phone-post-composer { display: flex; flex-wrap: wrap; gap: 8px; padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.1); }
.phone-post-btn { background: #0a84ff; color: #fff; border: none; border-radius: 16px; padding: 8px 14px; font-size: 13px; cursor: pointer; }
.phone-gallery { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; padding: 8px; }
.phone-gallery-cell { background: rgba(255,255,255,0.05); border-radius: 8px; overflow: hidden; }
.phone-gallery-link { cursor: pointer; }
.phone-gallery-img { width: 100%; display: block; }
.phone-gallery-cap { font-size: 12px; color: #bbb; padding: 4px 6px; }
.phone-custom { padding: 10px; }
.phone-daily-btn {
    display: block;
    width: 100%;
    background: transparent;
    border: 1px solid var(--theme-primary);
    color: var(--theme-primary);
    padding: 8px 14px;
    border-radius: 16px;
    font-size: 13px;
    cursor: pointer;
    text-align: right;
    margin-bottom: 6px;
    transition: background 0.15s;
}
.phone-daily-btn:hover { background: rgba(10, 132, 255, 0.15); }

.phone-empty, .phone-placeholder {
    text-align: center; color: #666;
    padding: 40px 20px; font-size: 14px;
}

/* Sidebar phone button — matches the band-card language (see .trait-*-item / .band-value) */
/* The phone button is styled by the SAME rules as the action buttons (its id
   #phone-sidebar-btn is in those selectors above) so it is pixel-identical. Only
   the unread badge below is phone-specific. */
.phone-badge {                     /* unread count — notification dot on the top-right corner */
    position: absolute;
    top: 2px;
    right: 5px;
    background: var(--theme-danger); color: #fff;
    font-size: 10px; font-weight: bold;
    min-width: 16px; text-align: center; box-sizing: border-box;
    border: 2px solid var(--theme-surface);   /* surface stroke so the pill floats over the icon */
    padding: 0 4px; border-radius: 9px;
}

/* Social Feed */
.phone-feed { padding: 0; }
.phone-post { border-bottom: 1px solid #2a2a3e; }
.phone-post-header { display: flex; align-items: center; gap: 8px; padding: 10px 12px; }
.phone-post-avatar { width: 32px; height: 32px; border-radius: 50%; object-fit: cover; }
.phone-post-avatar-letter {
    width: 32px; height: 32px; border-radius: 50%;
    background: #3a3a5a; display: flex; align-items: center; justify-content: center;
    font-size: 14px; font-weight: bold; color: #ccc;
}
.phone-post-name { font-weight: 600; font-size: 13px; color: #e0e0e0; }
.phone-post-image { width: 100%; aspect-ratio: 1; object-fit: cover; }
.phone-post-caption { padding: 8px 12px; font-size: 13px; line-height: 1.4; color: #e0e0e0; }
.phone-post-likes { padding: 4px 12px 10px; font-size: 12px; opacity: 0.6; }

/* Dating App */
.phone-dating-card { padding: 12px; }
.phone-profile-photo { width: 100%; aspect-ratio: 3/4; object-fit: cover; border-radius: 12px; }
.phone-profile-photo-placeholder {
    width: 100%; aspect-ratio: 3/4; border-radius: 12px;
    background: #3a3a5a; display: flex; align-items: center; justify-content: center;
    font-size: 64px; font-weight: bold; color: #666;
}
.phone-profile-info { padding: 12px 0 4px; }
.phone-profile-name { font-size: 20px; font-weight: bold; color: #e0e0e0; }
.phone-profile-age { opacity: 0.7; margin-left: 8px; font-size: 18px; color: #ccc; }
.phone-profile-bio { font-size: 13px; margin: 8px 0; opacity: 0.85; line-height: 1.4; color: #ccc; }
.phone-profile-interests { display: flex; flex-wrap: wrap; gap: 6px; margin: 8px 0; }
.phone-profile-tag { background: rgba(255,255,255,0.1); padding: 4px 10px; border-radius: 12px; font-size: 11px; color: #ccc; }
.phone-dating-actions { display: flex; justify-content: center; gap: 24px; padding: 16px; }
.phone-dating-btn {
    width: 56px; height: 56px; border-radius: 50%; border: 2px solid;
    font-size: 24px; cursor: pointer; background: transparent; transition: transform 0.15s;
}
.phone-dating-btn:hover { transform: scale(1.1); }
.phone-dating-pass { border-color: var(--theme-danger); color: var(--theme-danger); }
.phone-dating-like { border-color: var(--theme-accent); color: var(--theme-accent); }
.phone-match-overlay {
    position: absolute; inset: 0; background: rgba(0,0,0,0.85);
    display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 1;
}
.phone-match-text { font-size: 28px; font-weight: bold; color: var(--theme-accent); margin-bottom: 12px; }
.phone-matches-section { border-bottom: 1px solid #2a2a3e; padding: 12px; }
.phone-matches-title { font-size: 12px; text-transform: uppercase; opacity: 0.5; margin-bottom: 8px; letter-spacing: 1px; color: #999; }
.phone-matches-row { display: flex; gap: 10px; overflow-x: auto; }
.phone-match-avatar { width: 48px; height: 48px; border-radius: 50%; border: 2px solid var(--theme-accent); object-fit: cover; }
.phone-match-avatar-letter {
    width: 48px; height: 48px; border-radius: 50%; border: 2px solid var(--theme-accent);
    background: #3a3a5a; display: flex; align-items: center; justify-content: center;
    font-size: 18px; font-weight: bold; color: #ccc;
}
/* Chat typing animation */
.phone-bubble-pending {{ display: none !important; }}
.phone-reply-pending {{ display: none !important; }}
.phone-bubble-appear {{ animation: bubbleAppear 0.25s ease-out; }}
@keyframes bubbleAppear {{
    from {{ opacity: 0; transform: translateY(8px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
.phone-typing-indicator {{
    align-self: flex-start; background: #2a3a5e; border-radius: 16px;
    border-bottom-left-radius: 4px; padding: 10px 16px; display: flex; gap: 4px; align-items: center;
}}
.phone-typing-indicator span {{
    width: 7px; height: 7px; background: #888; border-radius: 50%;
    animation: typingDot 1.2s infinite ease-in-out;
}}
.phone-typing-indicator span:nth-child(2) {{ animation-delay: 0.2s; }}
.phone-typing-indicator span:nth-child(3) {{ animation-delay: 0.4s; }}
@keyframes typingDot {{
    0%, 60%, 100% {{ opacity: 0.3; transform: translateY(0); }}
    30% {{ opacity: 1; transform: translateY(-3px); }}
}}
"""

    def _generate_customize_passage(self) -> str:
        """Generate the CustomizeCharacters passage for player and NPC customization.

        Returns empty string if no customizable player or NPCs exist.
        The Start passage age gate links here instead of StartingCanvas when active.
        Player section appears FIRST, then NPC section.
        """
        npc_map = getattr(self, 'npc_map', {})
        customizable_npcs = [
            (uuid, data) for uuid, data in npc_map.items()
            if data.get("customizable")
        ]
        has_player_customization = bool(
            getattr(self, 'player_customizable', False)
            and getattr(self, 'player_customization_fields', [])
        )
        if not customizable_npcs and not has_player_customization:
            return ""

        original_target = getattr(self, '_original_start_target', 'StartingCanvas')
        video_path = getattr(self, 'video_path', None) or ""

        sections = []

        # ── Player customization section (BEFORE NPCs) ──
        if has_player_customization:
            sections.append(self._build_player_customize_html(
                self.player_customization_fields, video_path
            ))

        # ── NPC customization section (existing logic) ──
        if customizable_npcs:
            npc_fields = []
            for npc_uuid, npc_data in customizable_npcs:
                npc_name = npc_data.get("name", "NPC")
                portrait = npc_data.get("portrait", "")
                options = npc_data.get("relationship_options", [])

                if portrait and video_path:
                    portrait_html = (
                        f'<img src="{video_path}/{html.escape(portrait)}" '
                        f'alt="{html.escape(npc_name)}" class="customize-portrait" '
                        f'onerror="this.style.display=\'none\'">'
                    )
                else:
                    initial = html.escape(npc_name[0].upper()) if npc_name else "?"
                    portrait_html = f'<div class="customize-portrait-placeholder">{initial}</div>'

                name_field = f'<<textbox "$npcs[\\"{npc_uuid}\\"].name" "{html.escape(npc_name)}">>'

                rel_field = ""
                if options:
                    option_tags = "\n".join(
                        f'  <<option "{opt}" "{opt}">>'
                        for opt in options
                    )
                    rel_field = (
                        f'<div class="customize-field">\n'
                        f'<label>Relationship</label>\n'
                        f'<<listbox "$npcs[\\"{npc_uuid}\\"].relationship" autoselect>>\n'
                        f'{option_tags}\n'
                        f'<</listbox>>\n'
                        f'</div>'
                    )

                # NPC description/intro
                npc_desc = html.escape(npc_data.get("description", "") or "")
                desc_html = f'<p class="customize-description">{npc_desc}</p>' if npc_desc else ''

                npc_fields.append(
                    f'<div class="customize-npc">\n'
                    f'<div class="customize-npc-header">\n'
                    f'{portrait_html}\n'
                    f'<span class="customize-npc-default-name">{html.escape(npc_name)}</span>\n'
                    f'</div>\n'
                    f'{desc_html}\n'
                    f'<div class="customize-field">\n'
                    f'<label>Name</label>\n'
                    f'{name_field}\n'
                    f'</div>\n'
                    f'{rel_field}\n'
                    f'</div>'
                )
            sections.append(
                '<h3 class="customize-section-title">Characters</h3>\n'
                + "\n".join(npc_fields)
            )

        all_sections = "\n".join(sections)

        return f""":: CustomizeCharacters
<<nobr>>
<div class="customize-page">
<h2>Customize Characters</h2>
<p class="customize-intro">Personalize the characters in your story.</p>
{all_sections}
<div class="customize-actions">
[[Continue to Game->{original_target}]]
</div>
</div>
<</nobr>>

<style>
.customize-page {{
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
}}
.customize-page h2 {{
    text-align: center;
    margin-bottom: 5px;
}}
.customize-intro {{
    text-align: center;
    opacity: 0.7;
    margin-bottom: 25px;
    font-size: 0.9em;
}}
.customize-section-title {{
    margin: 20px 0 10px;
    opacity: 0.6;
    font-size: 0.9em;
    text-transform: uppercase;
    letter-spacing: 1px;
}}
.customize-npc, .customize-player {{
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 20px;
}}
.customize-npc-header {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 15px;
}}
.customize-portrait {{
    width: 60px;
    height: 60px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid rgba(255,255,255,0.2);
}}
.customize-portrait-placeholder {{
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: rgba(255,255,255,0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    font-weight: bold;
    border: 2px solid rgba(255,255,255,0.2);
}}
.customize-npc-default-name {{
    font-size: 1.2em;
    font-weight: bold;
}}
.customize-description {{
    font-size: 0.9em;
    opacity: 0.75;
    margin-bottom: 15px;
    line-height: 1.4;
}}
.customize-field {{
    margin-bottom: 12px;
}}
.customize-field label {{
    display: block;
    font-size: 0.85em;
    opacity: 0.7;
    margin-bottom: 4px;
    text-transform: uppercase;
    letter-spacing: 1px;
}}
.customize-field input[type="text"] {{
    width: 100%;
    min-width: 0;
    max-width: 100%;
    padding: 8px 12px;
    background: rgba(0,0,0,0.3);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 6px;
    color: inherit;
    font-size: 1em;
    box-sizing: border-box;
}}
.customize-field select {{
    width: 100%;
    min-width: 0;
    max-width: 100%;
    padding: 8px 12px;
    background: rgba(0,0,0,0.3);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 6px;
    color: inherit;
    font-size: 1em;
    box-sizing: border-box;
}}
.customize-actions {{
    text-align: center;
    margin-top: 25px;
}}
.customize-actions a {{
    display: inline-block;
    padding: 12px 30px;
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 8px;
    text-decoration: none;
    font-size: 1.1em;
    transition: background 0.2s;
}}
.customize-actions a:hover {{
    background: rgba(255,255,255,0.2);
}}
.player-img-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 12px;
    margin-top: 8px;
}}
.player-img-option {{
    cursor: pointer;
    border: 2px solid rgba(255,255,255,0.15);
    border-radius: 8px;
    overflow: hidden;
    text-align: center;
    transition: border-color 0.2s, transform 0.1s;
    padding: 4px;
}}
.player-img-option:hover {{
    border-color: rgba(255,255,255,0.4);
    transform: scale(1.03);
}}
.player-img-option.player-img-selected {{
    border-color: var(--theme-primary);
    box-shadow: 0 0 8px var(--theme-primary-bg);
}}
.player-img-option img {{
    width: 100%;
    aspect-ratio: 3/4;
    object-fit: cover;
    border-radius: 4px;
}}
.player-img-label {{
    display: block;
    font-size: 0.8em;
    margin-top: 4px;
    opacity: 0.8;
}}
</style>
"""

    def _build_player_customize_html(self, fields, video_path):
        """Build HTML for the player customization section."""
        parts = ['<h3 class="customize-section-title">Your Character</h3>',
                 '<div class="customize-player">']

        # Player description/intro
        player_desc = html.escape(getattr(self, 'player_description', '') or '')
        if player_desc:
            parts.append(f'<p class="customize-description">{player_desc}</p>')

        for cf in fields:
            field_id = cf["id"]
            field_type = cf["type"]
            label = html.escape(cf.get("label", field_id))
            default = cf.get("default", "")

            if field_type == "text":
                # id="name" maps to $player.name, others to $player.field_id
                if field_id == "name":
                    target_var = "$player.name"
                    default_display = html.escape(
                        default or getattr(self, 'player_name', 'Player')
                    )
                else:
                    target_var = f"$player.{field_id}"
                    default_display = html.escape(default)
                parts.append(
                    f'<div class="customize-field">\n'
                    f'<label>{label}</label>\n'
                    f'<<textbox "{target_var}" "{default_display}">>\n'
                    f'</div>'
                )

            elif field_type == "select":
                options = cf.get("options", [])
                option_tags = "\n".join(
                    f'  <<option "{html.escape(str(opt))}" "{html.escape(str(opt))}">>'
                    for opt in options
                )
                parts.append(
                    f'<div class="customize-field">\n'
                    f'<label>{label}</label>\n'
                    f'<<listbox "$player.{field_id}" autoselect>>\n'
                    f'{option_tags}\n'
                    f'<</listbox>>\n'
                    f'</div>'
                )

            elif field_type == "image_select":
                options = cf.get("options", [])
                sets_portrait = cf.get("sets_portrait", False)
                grid_items = []
                for opt in options:
                    opt_id = html.escape(opt["id"])
                    opt_image = opt.get("image", "")
                    opt_label = html.escape(opt.get("label", opt_id))
                    img_src = (
                        f"{video_path}/{html.escape(opt_image)}"
                        if video_path and opt_image else ""
                    )
                    selected_class = (
                        "player-img-selected" if opt["id"] == default else ""
                    )
                    sp = "true" if sets_portrait else "false"
                    grid_items.append(
                        f'<div class="player-img-option {selected_class}" '
                        f'data-field="{html.escape(field_id)}" '
                        f'data-value="{opt_id}" '
                        f'data-image="{html.escape(opt_image)}" '
                        f'data-sets-portrait="{sp}">'
                        f'<img src="{img_src}" alt="{opt_label}" '
                        f'onerror="this.style.display=\'none\'">'
                        f'<span class="player-img-label">{opt_label}</span>'
                        f'</div>'
                    )
                parts.append(
                    f'<div class="customize-field">\n'
                    f'<label>{label}</label>\n'
                    f'<div class="player-img-grid">\n'
                    f'{"".join(grid_items)}\n'
                    f'</div>\n'
                    f'</div>'
                )

        parts.append('</div>')
        return "\n".join(parts)

    # ========== SIMPLIFIED CORE FLOW METHODS ==========

    def _generate_starting_canvas(self) -> str:
        """Generate starting canvas display (per-node emission)."""
        if not self.project.starting_canvas:
            return self._generate_default_intro()

        canvas = self.project.starting_canvas

        # Generate per-node passages for the starting canvas
        node_passages = self._generate_canvas_node_passages(canvas, "StartingCanvas")
        if node_passages:
            return node_passages

        # Canvas has no nodes - create fallback StartingCanvas passage
        return_target = self._get_return_location(canvas, "Navigation")

        return f""":: StartingCanvas
<p>Welcome to your interactive story!</p>

<<set $game_state.current_canvas = "{canvas.id}">>

[[Continue->{return_target}]]"""

    def _generate_default_intro(self) -> str:
        """Generate default intro when no starting canvas exists."""
        return """:: StartingCanvas
<h2>Welcome</h2>
<p>Welcome to your interactive story! This is a basic introduction.</p>

<p>Your adventure is about to begin...</p>

[[Continue->Navigation]]"""

    def _generate_basic_navigation(self) -> str:
        """Generate navigation hub with neighbor-only behavior when possible."""
        if not self.locations:
            return self._generate_minimal_navigation()

        # If there are no connections, keep global list (back-compat)
        if len(getattr(self, 'connections', []) or []) == 0:
            content = """:: Navigation
<h2>Navigation</h2>
<p>Where would you like to go?</p>

<div class="location-list">
"""
            for location in self.locations:
                location_name = location.name.replace(' ', '_')
                content += f"""    [[{location.name}->{self._location_passage_for_name(location_name)}]]<br>\n"""
            content += """</div>"""
            return content

        # Connections exist: guide user back to current location
        lines = [
            ":: Navigation",
            "<h2>Navigation</h2>",
            "<p>Return to your current location to explore nearby places.</p>",
        ]
        for loc in self.locations:
            pass_name = self._location_passage_name(loc)
            lines.append(
                f'<<if $player.current_location == "{loc.id}">>[[Back to {loc.name}->{pass_name}]]<</if>>'
            )
        # If current location unknown, allow initial selection
        lines.append("<<if $player.current_location == \"\">>")
        lines.append("<div class=\"location-list\">")
        for location in self.locations:
            location_name = location.name.replace(' ', '_')
            lines.append(f"    [[{location.name}->{self._location_passage_for_name(location_name)}]]<br>")
        lines.append("</div>")
        lines.append("<</if>>")
        return "\n".join(lines)

    def _generate_minimal_navigation(self) -> str:
        """Generate minimal navigation when no locations exist."""
        return """:: Navigation
<h2>Navigation</h2>
<p>This is the main navigation area.</p>

<p>Your story continues here...</p>

<!-- No locations available for navigation -->
<p><em>Explore your world by adding locations to your project.</em></p>"""

    def _generate_broken_exit_fallback(self) -> str:
        """Defense-in-depth passage for unresolved exit refs.

        The validator hard-fails on any unresolved nodeId / locationId / destinationId
        in choices and exit_blocks (template_import.py validate()), so this passage is
        unreachable in any normally-built game. It exists for test fixtures and dev-API
        paths that bypass validation — instead of silently routing to Navigation (the
        old behavior, which made broken refs invisible), we throw loudly so the bug is
        immediately obvious in the SugarCube error overlay and browser console.
        """
        return (
            ":: _BrokenExitFallback\n"
            "<<run\n"
            "  var msg = State.variables._broken_exit_msg || "
            "'Unresolved exit reference (no message captured)';\n"
            "  console.error('[BROKEN EXIT]', msg);\n"
            "  throw new Error('Broken exit: ' + msg);\n"
            "<</run>>"
        )

    def _generate_simple_locations(self) -> str:
        """Generate simple location passages."""
        if not self.locations:
            return "<!-- No locations to generate -->"

        content = "<!-- LOCATION PASSAGES -->\n\n"

        for location in self.locations:
            location_name = location.name.replace(' ', '_')
            location_id = str(location.id)

            # Check if this is a container
            if getattr(location, 'is_container', False):
                default_entry = getattr(location, 'default_entry_location', None)

                if default_entry:
                    # Container WITH default entry: Auto-redirect
                    default_name = default_entry.name.replace(' ', '_')
                    content += f""":: {self._location_passage_name(location)}
<!-- Container with default entry: Auto-redirect -->
<<goto "{self._location_passage_for_name(default_name)}">>

"""
                else:
                    # Container WITHOUT default entry: Show inner locations
                    content += f""":: {self._location_passage_name(location)}
<h2>{location.name}</h2>
<p>Choose where to go in {location.name}:</p>\
<<nobr>>
<<set $player.current_location = "{location_id}">>
<<if not $game_state.visited_locations.includes("{location_id}")>>
<<set $game_state.visited_locations.push("{location_id}")>>
<</if>>
<</nobr>>
"""
                    # Add destinations (all connected locations)
                    connected_locations = self._locations_entered_from(location)
                    for connected_loc in connected_locations:
                        connected_name = connected_loc.name.replace(' ', '_')
                        # Handle destination containers with default_entry appropriately
                        if getattr(connected_loc, 'is_container', False) and getattr(connected_loc, 'default_entry_location', None):
                            # If destination is container with default_entry, go to default_entry directly
                            default_entry_name = connected_loc.default_entry_location.name.replace(' ', '_')
                            content += f"[[{connected_loc.name}->{self._location_passage_for_name(default_entry_name)}]]<br>\n"
                        else:
                            # Regular location or container without default_entry
                            content += f"[[{connected_loc.name}->{self._location_passage_for_name(connected_name)}]]<br>\n"

                    # Add normal hierarchical navigation for containers without default_entry
                    content += """<div class="location-navigation">
"""
                    navigation_options = self._generate_hierarchical_navigation(location)
                    content += navigation_options
                    content += """</div>

"""
            else:
                # Regular location: Normal passage generation
                entry_conditions = (location.properties or {}).get('entry_conditions') if hasattr(location, 'properties') else None
                if entry_conditions and isinstance(entry_conditions, dict) and entry_conditions.get('items'):
                    entry_cond_json = json.dumps(entry_conditions)
                    blocked_message = (location.properties or {}).get('blocked_message', '')
                    # Find parent location for "go back" link
                    parent_name = None
                    if hasattr(location, 'entry_from') and location.entry_from:
                        parent_name = location.entry_from.name.replace(' ', '_')

                    # Check if this location has the wardrobe
                    loc_slug_ec = (location.properties or {}).get("slug", "")
                    wardrobe_link_ec = ""
                    if self.clothing_enabled and loc_slug_ec and loc_slug_ec == self.wardrobe_location_slug:
                        wardrobe_link_ec = "[[Change Clothes->WardrobePage]]<br>\n"

                    # Check if this location has the shop
                    shop_link_ec = ""
                    if self.clothing_enabled and self.shop_location_slug and loc_slug_ec == self.shop_location_slug:
                        shop_link_ec = '[[Browse Clothes->ShopPage]]<br>\n'

                    content += f""":: {self._location_passage_name(location)}
<<if setup.triggerConditionsSatisfied({entry_cond_json})>>\
<<nobr>>
<<set $player.current_location = "{location_id}">>
<<if not $game_state.visited_locations.includes("{location_id}")>>
<<set $game_state.visited_locations.push("{location_id}")>>
<</if>>
<</nobr>>\
<<set _autoFire = setup.getStoryCanvasRedirect("{location_id}")>>\
<<if _autoFire>><<goto _autoFire>><<else>>\
<h2>{location.name}</h2>
{self._render_location_description(location)}
{wardrobe_link_ec}{shop_link_ec}<<= setup.renderNpcPortraits("{location_id}")>>
<<= setup.renderSoloActivities("{location_id}")>>
<div class="location-navigation">
"""
                    navigation_options = self._generate_hierarchical_navigation(location)
                    content += navigation_options
                    go_back_target = self._location_passage_for_name(parent_name) if parent_name else "Start"
                    if blocked_message:
                        resolved_blocked = self._resolve_at_references(blocked_message)
                        blocked_html = f'<p class="entry-blocked-narrative">{resolved_blocked}</p>'
                    else:
                        blocked_html = (
                            '<p class="entry-blocked">You can\'t go here right now.</p>\n'
                            f'<p class="entry-requirements"><<print setup.formatCanvasConditions({entry_cond_json})>></p>'
                        )
                    content += f"""</div>
<</if>>\
<<else>>
<h2>{location.name}</h2>
{blocked_html}
[[Go back->{go_back_target}]]
<</if>>

"""
                else:
                    # Check if this location has the wardrobe
                    loc_slug = (location.properties or {}).get("slug", "")
                    wardrobe_link = ""
                    if self.clothing_enabled and loc_slug and loc_slug == self.wardrobe_location_slug:
                        wardrobe_link = "[[Change Clothes->WardrobePage]]<br>\n"

                    # Check if this location has the shop
                    shop_link = ""
                    if self.clothing_enabled and self.shop_location_slug and loc_slug == self.shop_location_slug:
                        shop_link = '[[Browse Clothes->ShopPage]]<br>\n'

                    content += f""":: {self._location_passage_name(location)}
<<nobr>>
<<set $player.current_location = "{location_id}">>
<<if not $game_state.visited_locations.includes("{location_id}")>>
<<set $game_state.visited_locations.push("{location_id}")>>
<</if>>
<</nobr>>\
<<set _autoFire = setup.getStoryCanvasRedirect("{location_id}")>>\
<<if _autoFire>><<goto _autoFire>><<else>>\
<h2>{location.name}</h2>
{self._render_location_description(location)}
{wardrobe_link}{shop_link}<<= setup.renderNpcPortraits("{location_id}")>>
<<= setup.renderSoloActivities("{location_id}")>>
<div class="location-navigation">
"""

                    # Generate hierarchical navigation using entry/exit connections
                    navigation_options = self._generate_hierarchical_navigation(location)
                    content += navigation_options

                    content += """</div>
<</if>>

"""

        return content

    def _render_location_description(self, location) -> str:
        """The description slot on a room screen — one paragraph, or a chain of them.

        A room is the screen a player re-enters more than any other, and until now it
        said the same sentence at 03:00 and at 18:00, on day one and on day ninety.
        `description` is still the base and still required; `description_variants` is a
        list of {conditions, text} rendered as a FIRST-MATCH chain with the base as the
        else — the same semantics adjacent [group] blocks already have (v2.py:14561).

        No new runtime primitive: setup.triggerConditionsSatisfied is the same helper the
        location passage already calls for entry_conditions a few lines above.

        ⚠️ Emitted from BOTH location paths (with and without entry_conditions). They were
        byte-identical copies before this and that is how a change like this gets half-
        applied, so the slot lives here and nowhere else.
        """
        base = (self._resolve_at_references(location.description)
                if location.description else "A location in your story.")
        variants = (location.properties or {}).get("description_variants") or []
        if not variants:
            return f"<p>{base}</p>"
        parts = []
        for i, var in enumerate(variants):
            if not isinstance(var, dict):
                continue
            text = str(var.get("text") or "").strip()
            cond = var.get("conditions")
            if not text or not isinstance(cond, dict) or not cond:
                continue
            kw = "if" if not parts else "elseif"
            parts.append(f"<<{kw} setup.triggerConditionsSatisfied({json.dumps(cond)})>>"
                         f"<p>{self._resolve_at_references(text)}</p>")
        if not parts:
            return f"<p>{base}</p>"
        return "".join(parts) + f"<<else>><p>{base}</p><</if>>"

    def _generate_story_canvases(self) -> str:
        """Generate story canvas passages (per-node emission)."""
        if not self.story_canvases:
            return "<!-- No story canvases to generate -->"

        content = "<!-- STORY CANVAS PASSAGES -->\n\n"

        for canvas in self.story_canvases:
            try:
                # Get trigger location for validation IF the canvas has a trigger.
                # Triggerless canvases (sub-menu-only — pulled in by closure pass via
                # targetType="node" cross-canvas references) skip this check and
                # generate passages directly. Closure pass at _compute_included_canvases
                # is the source of truth for inclusion; generator just emits the passages.
                if hasattr(canvas, 'trigger') and canvas.trigger and canvas.trigger.location_id:
                    trigger_location = self._get_location_by_id(canvas.trigger.location_id)
                    if not trigger_location:
                        continue  # Skip if trigger location not found

                # Generate per-node passages for this canvas
                node_passages = self._generate_canvas_node_passages(canvas, "Canvas")
                content += node_passages

            except (KeyError, TypeError, ValueError, AttributeError) as e:
                logger.error(
                    "Error generating passages for canvas '%s': %s",
                    canvas.name if hasattr(canvas, 'name') else str(canvas.id),
                    e
                )
                raise ValueError(
                    f"Canvas generation failed for '{canvas.name if hasattr(canvas, 'name') else str(canvas.id)}': {e}"
                ) from e

        return content

    def _cast_page_css(self) -> str:
        """Cast-page styling, emitted ONLY for games that author a cast page.

        Deliberately small: the card body reuses `.stats-card-with-portrait` /
        `.stats-portrait` / `.stats-info` / `.stats-name` from the Stats page and
        `.quests-goal` / `.quests-tip` from the Quests page, so a cast card reads
        as the same object the player already knows from two other screens. Only
        the two lines that exist nowhere else get rules of their own.
        """
        if not self.cast_page:
            return ""
        return """
/* Cast page. Who these people are to her, where they are, what moves them. */
.cast-intro {
    margin-bottom: 12px;
    color: var(--theme-text-muted, #8a8a8a);
    font-size: 13px;
}
.cast-card .cast-relationship {
    color: var(--theme-text, #c8c8c8);
    font-size: 13px;
    line-height: 1.45;
    margin: 2px 0 6px;
}
/* G: the tag line. Reads quieter than `relationship` and at the same weight as
   the location row — it is a label, not a sentence, and it must not compete with
   the one sentence above it. */
.cast-card .cast-tags {
    color: var(--theme-text-muted, #8a8a8a);
    font-size: 12px;
    margin: 0 0 6px;
}
.cast-card .cast-where {
    color: var(--theme-text-muted, #8a8a8a);
    font-size: 12px;
    margin: 0 0 6px;
}
/* Off-schedule reads quieter than on — the page should not look broken when
   somebody is simply not around at this hour. */
.cast-card .cast-where.cast-away {
    opacity: 0.6;
    font-style: italic;
}
.cast-card .quests-goal,
.cast-card .quests-tip {
    margin-top: 6px;
}
"""

    def _cheat_page_css(self) -> str:
        """Cheat-page styling, emitted ONLY for games that author a cheat page.

        Gated on the same principle the retired build badge used: a game that does not
        author this feature should not carry it. Until now these rules shipped in every
        game's stylesheet whether or not it had a cheat page — a pre-existing leak this
        change closes rather than widens.

        The leading newline lives HERE, and the seam is spliced onto the closing brace
        of the previous rule, so the emitted stylesheet is unchanged for a game with a
        cheat page and simply has no gap for a game without one.
        """
        if not self.cheat_page:
            return ""
        return """
/* Cheat page rows. Flat and mechanical by design — this page is read as a list of
   levers, not as prose, so the fiction lives on the container and the rows stay legible. */
.cheat-intro {
    margin-bottom: 12px;
    color: var(--theme-text-muted, #8a8a8a);
    font-size: 13px;
}
.cheat-row {
    padding: 7px 0;
    border-bottom: 1px solid var(--theme-border, #2a2a2a);
}
.cheat-row:last-of-type { border-bottom: none; }
.cheat-hint, .cheat-at-cap {
    margin-top: 2px;
    color: var(--theme-text-muted, #8a8a8a);
    font-size: 12px;
}
.cheat-row-maxed {
    font-weight: 600;
    opacity: 0.5;
}
/* Code entry. The box is the whole surface for a player with no code, so it is
   sized to be obviously the thing to use rather than tucked in a corner. */
.cheat-entry {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px;
    margin-bottom: 10px;
}
.cheat-entry input[type="text"] {
    flex: 1 1 160px;
    min-width: 0;
    padding: 6px 8px;
    border: 1px solid var(--theme-border, #3a3a3a);
    border-radius: 4px;
    background: var(--theme-surface-alt, #1a1a1a);
    color: var(--theme-text, #e8e8e8);
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
#cheat-reply { flex: 1 1 100%; }
.cheat-reply-bad {
    color: var(--theme-danger, #d06a6a);
    font-size: 12px;
}
/* The join line is this page's only advertising: for a player with no code it is the
   sole thing on the page that tells them what the box is for. */
.cheat-join {
    margin-bottom: 14px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--theme-border, #2a2a2a);
    color: var(--theme-text-muted, #8a8a8a);
    font-size: 12px;
}
/* Version chip — the release a player matches against their guide, since codes are
   scoped per release. Rides inside .sidebar-version and the cheat page's heading. */
.build-badge {
    display: inline-block;
    padding: 0 5px;
    border: 1px solid var(--theme-border, #3a3a3a);
    border-radius: 3px;
    font-size: 10px;
    letter-spacing: 0.02em;
    white-space: nowrap;
    color: var(--theme-text-muted, #8a8a8a);
}"""

    def _generate_cast_page(self) -> str:
        """Emit the cast page, plus its sidebar button widget.

        THE WHO-IS-WHO SURFACE. Measured across the 25-game mopoga corpus
        (2026-08-23): 17 of 25 shipped sandboxes carry a page like this, and 7 of
        the 8 parsed top-ten do — the lone exception, degrees-of-lewdity, carries
        the same load inside its prose instead by swapping description for name on
        the meeting flag in 64 places. NONE of the 25 uses a third-person narrator
        to tell the player who somebody is. A page is the field's answer.

        NOTHING HERE IS AUTHORED. Every line on a card already exists in the game:

          name             $npcs[uuid].name
          who they are     $npcs[uuid].relationship   ([[npcs]] relationship)
          where, right now setup.getNpcLocation + setup._locNameFromUuid
          what to do next  the character's own quest card — tip + goal block,
                           via setup.pickQuestsCard / renderQuestsGoalBlock

        WHO IS LISTED IS THE QUEST CARDS' DECISION. A character appears exactly
        when pickQuestsCard returns a card for them, which is the same call and the
        same gate QuestsPage makes. Put the meeting flag on a character's cards and
        both surfaces reveal them together; they cannot fall out of step, and there
        is no second gate to keep in sync. The cost of that choice is real and
        worth stating: a character with no quest card can never appear here. The
        `guidance exists` gate already requires every [[npcs]] entry to carry one,
        so this cannot happen in a game that passes its own scoreboard.

        Roster ORDER mirrors QuestsPage (walk setup.quests_cards, dedupe by npc_id,
        keep file order) so the two pages read in the same sequence.

        The `castButton` widget is ALWAYS defined, empty when there is no cast
        page, because StoryCaption calls it unconditionally and SugarCube throws on
        an undefined widget — the same rule the cheat page records below.
        """
        cp = self.cast_page or {}
        if not cp:
            return ':: CastWidgets [widget nobr]\n<<widget "castButton">><</widget>>\n'

        title = html.escape(cp.get("title") or "The Cast")
        btn_label = html.escape(cp.get("button_label") or cp.get("title") or "The Cast")
        btn_icon = html.escape(cp.get("button_icon") or "")
        intro = cp.get("intro") or ""

        icon_span = f'<span class="nav-i">{btn_icon}</span>' if btn_icon else ""
        widget = (
            ':: CastWidgets [widget nobr]\n'
            '<<widget "castButton">>\n'
            '<div id="cast-btn-widget">\n'
            f'  <<if passage() isnot "CastPage">><<link "{btn_label}" "CastPage">><</link>>'
            f'<<else>><span class="nav-row">{btn_label}</span><</if>>{icon_span}\n'
            '</div>\n'
            '<</widget>>\n'
        )

        video_path = getattr(self, 'video_path', '') or './media'
        placeholder_svg = self._get_placeholder_svg()
        escaped_svg = html.escape(placeholder_svg).replace("'", "\\'")

        intro_line = f'<div class="cast-intro">{html.escape(intro)}</div>\n' if intro else ""

        page = f""":: CastPage
<<nobr>>
<h2>{title}</h2>
{intro_line}
/* Roster + reveal, both from the quest cards. See _generate_cast_page's docstring. */
<<set _allCards to setup.quests_cards || []>>
<<set _hidden to setup.hiddenNpcs || {{}}>>
<<set _slugMap to setup.npc_slug_map || {{}}>>
<<set _slugs to []>>
<<for _c range _allCards>>
  <<if _c && _c.npc_id && _slugs.indexOf(_c.npc_id) === -1>>
    /* hiddenNpcs is UUID-keyed; check both forms so hidden_from_ui holds in
       either build mode, exactly as QuestsPage does. */
    <<if !_hidden[_c.npc_id] && !_hidden[_slugMap[_c.npc_id]]>>
      <<run _slugs.push(_c.npc_id)>>
    <</if>>
  <</if>>
<</for>>

<<set _shown to 0>>
<<for _slug range _slugs>>
  <<set _card to setup.pickQuestsCard(_slug)>>
  <<if _card>>
    <<set _nid to _slugMap[_slug] || _slug>>
    <<set _npc to State.variables.npcs ? (State.variables.npcs[_nid] || State.variables.npcs[_slug]) : null>>
    <<if _npc>>
      <<set _shown to _shown + 1>>
      <<set _loc to setup.getNpcLocation(_slug)>>
      <<set _locName to _loc ? (setup._locNameFromUuid(_loc.location) || "") : "">>
      <<set _goalBlock to setup.renderQuestsGoalBlock(_card, setup.evaluateGoals(_card))>>
      <div class="stats-card stats-card-with-portrait cast-card">
        <div class="stats-portrait">
          <<if _npc.portrait>>
            <img @src="'{video_path}/' + _npc.portrait" @alt="_npc.name" onerror="this.style.display='none';this.parentElement.innerHTML='{escaped_svg}';">
          <<else>>
            {placeholder_svg}
          <</if>>
        </div>
        <div class="stats-info">
          <div class="stats-name"><<print _npc.name>></div>
          <<if _npc.relationship>><div class="cast-relationship"><<print _npc.relationship>></div><</if>>
          <<set _tags to setup.npc_tags[_slug]>>
          <<if _tags && _tags.length>><div class="cast-tags"><<print _tags.join(" &middot; ")>></div><</if>>
          <<if _locName>>
            <div class="cast-where">📍 <<print _locName>></div>
          <<else>>
            <div class="cast-where cast-away">📍 Not about right now</div>
          <</if>>
          <<if _goalBlock>><<print _goalBlock>><</if>>
          <<if _card.tip>><div class="quests-tip">💡 <<print _card.tip>></div><</if>>
        </div>
      </div>
    <</if>>
  <</if>>
<</for>>

<<if _shown === 0>>
  <div class="no-quests">You have not met anybody yet.</div>
<</if>>
<</nobr>>
<<link "← Back">><<run setup.smartBack()>><</link>>
"""
        return widget + "\n" + page

    def _generate_cheat_page(self) -> str:
        """Emit the player cheat page, its code-entry script, and its sidebar button.

        ONE build ships everywhere — to the portals, to itch, to a supporter. Which
        rows are live is a RUNTIME property of the codes the player has entered, not
        a property of the file. That is what the studied field does: 8 of the 26 top
        mopoga games carry a live supporter-code box inside the free web build, and
        only 3 ship a separate paid file (which a phone cannot practically open).

        A player who has entered nothing sees the title, the intro, an empty box and
        the join line. Each row is emitted inside a check on its own unlock flag, so
        a locked row renders NO bytes — no label, no padlock, no hint. Reading the
        page teaches a free player nothing about what exists or what it costs.

        The `cheatButton` widget is ALWAYS defined (empty when there is no cheat page),
        because StoryCaption calls it unconditionally and SugarCube throws on an
        undefined widget.

        NOTE the deliberate absence of a `setup.cheat_page = {...}` ship line. The only
        runtime object is `setup.cheatCodes`, which maps hash -> row id and carries no
        trait, value, cap or hint. Everything else is baked into passage markup.
        """
        cp = self.cheat_page or {}
        # Widget first — defined in both cases so StoryCaption never calls a ghost.
        if not cp:
            return ':: CheatWidgets [widget nobr]\n<<widget "cheatButton">><</widget>>\n'

        title = html.escape(cp.get("title") or "Cheats")
        btn_label = html.escape(cp.get("button_label") or cp.get("title") or "Cheats")
        btn_icon = html.escape(cp.get("button_icon") or "")
        intro = cp.get("intro") or ""
        join_note = cp.get("join_note") or ""
        join_url = cp.get("join_url") or self._resolve_support_url()
        grants = cp.get("grants") or []

        icon_span = f'<span class="nav-i">{btn_icon}</span>' if btn_icon else ""
        widget = (
            ':: CheatWidgets [widget nobr]\n'
            '<<widget "cheatButton">>\n'
            '<div id="cheat-btn-widget">\n'
            f'  <<if passage() isnot "CheatPage">><<link "{btn_label}" "CheatPage">><</link>>'
            f'<<else>><span class="nav-row">{btn_label}</span><</if>>{icon_span}\n'
            '</div>\n'
            '<</widget>>\n'
        )

        # The version chip. Codes are scoped to a release, so the number a player has
        # to match against their guide belongs on this page and not only in the
        # sidebar footer. Reuses the existing .build-badge rule.
        version = str((self.project.metadata or {}).get("version", "") or "").strip()
        badge = (
            f' <span class="build-badge">v{html.escape(version)}</span>' if version else ""
        )

        rows = [self._cheat_row_markup(g) for g in grants]

        # Failure copy names the build. We cannot tell a wrong code from a right code
        # for another release (the hash is salted with the version, so both simply
        # miss) — and we do not need to. Naming the version answers both cases, and
        # "your code is for a different release" is the likeliest one.
        miss_msg = (
            f"No match. This build is v{html.escape(version)} — check you are using the "
            f"v{html.escape(version)} guide."
            if version else "No match. Check the code against your guide."
        )

        entry = [
            '<div class="cheat-entry">',
            '<<textbox "_cheatcode" "">>',
            '<<link "Unlock">>',
            '  <<set _hit to setup.cheatTry(_cheatcode)>>',
            '  <<if _hit>><<goto "CheatPage">>',
            f'  <<else>><<replace "#cheat-reply">>'
            f'<span class="cheat-reply-bad">{miss_msg}</span><</replace>>',
            '  <</if>>',
            '<</link>>',
            '<span id="cheat-reply"></span>',
            '</div>',
        ]

        join_block = ""
        if join_note:
            join_block = (
                f'<div class="cheat-join">{html.escape(join_note)} '
                f'<a href="{html.escape(join_url)}" target="_blank" rel="noopener">'
                f'Open the membership page</a></div>'
            )

        body = [
            ":: CheatPage",
            "<<nobr>>",
            # Re-apply anything this browser has already unlocked for this build.
            # Idempotent, and the only reason a new game does not need re-typing.
            "<<run setup.cheatRestore()>>",
            f"<h2>{title}{badge}</h2>",
            '<div class="npc-section">',
        ]
        if intro:
            body.append(f'<div class="cheat-intro">{html.escape(intro)}</div>')
        body.extend(entry)
        if join_block:
            body.append(join_block)
        body.extend(rows)
        body.append("</div>")
        body.append("<</nobr>>")
        body.append('<<link "← Back">><<run setup.smartBack()>><</link>>')

        return widget + "\n" + self._generate_cheat_code_script() + "\n" + "\n".join(body) + "\n"

    # FNV-1a 32-bit. Chosen because it is four lines in both Python and JavaScript and
    # needs no library on either side; `crypto.subtle` is async and would turn every
    # code check into a promise inside a SugarCube macro for no gain.
    #
    # This is obfuscation, not security, and that is the right ceiling: of the 26 top
    # mopoga games examined, ZERO validate server-side (inseminator looks like it does
    # — its `fetch(` count is 0; it is client-side salted SHA-256). The code ships in a
    # public HTML file for everyone in this genre. What keeps the product alive is
    # rotating the codes each release, not the strength of the check.
    CHEAT_HASH_OFFSET = 2166136261
    CHEAT_HASH_PRIME = 16777619

    @staticmethod
    def normalize_cheat_code(raw: str) -> str:
        """Fold away every difference a phone keyboard can introduce.

        ALL whitespace is stripped, not just the ends: a code read off a PDF gets
        retyped with stray spaces, and autocapitalisation makes case meaningless.
        The JS side does the same thing, so the two agree byte for byte.
        """
        return "".join(str(raw or "").split()).upper()

    @classmethod
    def cheat_code_hash(cls, version: str, grant_id: str, code: str) -> str:
        """Hash one code for one row of one release.

        Salted with BOTH the version and the row id, which buys two properties for
        free: a code cannot be used on a row it was not issued for, and last release's
        codes cannot open this release's rows.
        """
        payload = f"{version}|{grant_id}|{cls.normalize_cheat_code(code)}"
        h = cls.CHEAT_HASH_OFFSET
        for byte in payload.encode("utf-8"):
            h ^= byte
            h = (h * cls.CHEAT_HASH_PRIME) & 0xFFFFFFFF
        return format(h, "08x")

    def _generate_cheat_code_script(self) -> str:
        """The code-entry runtime: hash, lookup table, unlock, and restore.

        `setup.cheatCodes` carries hash -> row id and nothing else. The row ids are
        already visible in the page's own flag checks, so this object leaks nothing
        the markup does not, and it replaces what would otherwise be a hand-built
        if/elseif chain one entry long per row.
        """
        cp = self.cheat_page or {}
        version = str((self.project.metadata or {}).get("version", "") or "").strip()
        # {row id: plaintext code} injected by the packager from the untracked codes
        # file. Absent (an explicit --no-codes build) means the box accepts nothing,
        # which is a valid state: the page still advertises, no row can be opened.
        codes = self.cheat_codes or {}
        table = {
            self.cheat_code_hash(version, g.get("id"), codes[g.get("id")]): g.get("id")
            for g in (cp.get("grants") or [])
            if g.get("id") in codes
        }
        # Keyed by version so a release rotation retires the stored unlocks with the
        # codes themselves — no invalidation step to remember, and a player on an old
        # portal build keeps working with the guide that shipped beside it.
        store_key = f"cheat_unlocks_v{version or '0'}"

        return (
            ":: CheatCodes [script]\n"
            "setup.cheatCodes = " + json.dumps(table, sort_keys=True) + ";\n"
            "setup.cheatStoreKey = " + json.dumps(store_key) + ";\n"
            "setup.cheatVersion = " + json.dumps(version) + ";\n"
            "\n"
            "setup.cheatHash = function (payload) {\n"
            "  var h = " + str(self.CHEAT_HASH_OFFSET) + ";\n"
            "  var s = unescape(encodeURIComponent(String(payload)));\n"
            "  for (var i = 0; i < s.length; i++) {\n"
            "    h ^= s.charCodeAt(i);\n"
            "    h = Math.imul(h, " + str(self.CHEAT_HASH_PRIME) + ") >>> 0;\n"
            "  }\n"
            "  return ('0000000' + h.toString(16)).slice(-8);\n"
            "};\n"
            "\n"
            "// Whitespace-stripped and upper-cased, matching normalize_cheat_code().\n"
            "setup.cheatNormalize = function (raw) {\n"
            "  return String(raw == null ? '' : raw).replace(/\\s+/g, '').toUpperCase();\n"
            "};\n"
            "\n"
            "// localStorage is a MIRROR, never the source of truth. The unlock lives in\n"
            "// $flags like every other flag, so it rides in the save and survives export.\n"
            "// The mirror only spares a returning player from retyping on a new game, and\n"
            "// a browser that refuses storage (we run inside a cross-origin iframe on the\n"
            "// portals) must degrade to that, not throw.\n"
            "setup.cheatRemember = function (id) {\n"
            "  try {\n"
            "    var seen = recall(setup.cheatStoreKey, []);\n"
            "    if (!Array.isArray(seen)) seen = [];\n"
            "    if (seen.indexOf(id) === -1) seen.push(id);\n"
            "    memorize(setup.cheatStoreKey, seen);\n"
            "  } catch (e) { /* storage blocked — unlock still lives in the save */ }\n"
            "};\n"
            "\n"
            "setup.cheatRestore = function () {\n"
            "  var seen;\n"
            "  try { seen = recall(setup.cheatStoreKey, []); } catch (e) { return; }\n"
            "  if (!Array.isArray(seen) || !seen.length) return;\n"
            "  var sv = State.variables;\n"
            "  sv.flags = sv.flags || {};\n"
            "  for (var i = 0; i < seen.length; i++) {\n"
            "    var key = 'cheat_' + seen[i];\n"
            "    if (!sv.flags[key]) sv.flags[key] = true;\n"
            "  }\n"
            "};\n"
            "\n"
            "// Returns the unlocked row id, or null. The caller navigates on a hit so the\n"
            "// new row renders; a miss is reported in place, without spending a moment.\n"
            "setup.cheatTry = function (raw) {\n"
            "  var code = setup.cheatNormalize(raw);\n"
            "  if (!code) return null;\n"
            "  var ids = Object.keys(setup.cheatCodes);\n"
            "  for (var i = 0; i < ids.length; i++) {\n"
            "    var id = setup.cheatCodes[ids[i]];\n"
            "    if (setup.cheatHash(setup.cheatVersion + '|' + id + '|' + code) === ids[i]) {\n"
            "      setup.pendingEffects = [];\n"
            "      setup.applyAndNotifyFlag('player', null, 'cheat_' + id, 'set');\n"
            "      setup.showEffectNotification();\n"
            "      setup.cheatRemember(id);\n"
            "      return id;\n"
            "    }\n"
            "  }\n"
            "  return null;\n"
            "};\n"
        )

    def _cheat_row_markup(self, g: dict) -> str:
        """One cheat row: a live self-navigating link behind its own unlock flag.

        The unlock check wraps the WHOLE row, label included, so a row the player has
        no code for emits nothing at all. A padlocked placeholder would tell a free
        player exactly what is on sale and how many there are; nothing is the point.
        """
        target = "npc" if g.get("targetType") == "npc" else "player"
        npc_js = f'"{g.get("npcId")}"' if target == "npc" else "null"
        trait = g.get("trait")
        op = g.get("op") or "add"
        value = g.get("value")
        cap = g.get("cap")
        clamp_js = "true" if g.get("clamp", True) else "false"
        cap_js = "null" if cap is None else self._fmt_num(cap)
        val_js = self._fmt_num(value)

        # Button text: authored, or composed so it reads like the effect it applies.
        btn = g.get("button_text") or (
            f"{g.get('label')} → {self._fmt_num(value)}" if op == "set"
            else f"{g.get('label')} {'+' if (value or 0) >= 0 else '−'}{self._fmt_num(abs(value or 0))}"
        )
        btn = html.escape(str(btn))

        # At-cap guard, evaluated at RENDER — which is why every row navigates to
        # itself: only a re-render can grey a row the instant it reaches its ceiling.
        # Without this the row stays lit and silently does nothing, which is the
        # failure the studied games generate support threads over.
        read = f'setup.getTraitValue("{target}", {npc_js}, "{trait}")'
        if op == "set":
            guard = f"{read} isnot {val_js}"
        elif cap is not None:
            guard = f"{read} lt {cap_js}"
        else:
            guard = ""   # unbounded resource — always available

        grant = (
            f'<<link "{btn}" "CheatPage">><<script>>setup.pendingEffects = [];'
            f'setup.applyAndNotifyTrait("{target}", {npc_js}, "{trait}", "{op}", '
            f'{val_js}, {clamp_js}, {cap_js});setup.showEffectNotification();'
            f'<</script>><</link>>'
        )
        hint = g.get("hint") or ""
        hint_div = f'<div class="cheat-hint">{html.escape(hint)}</div>' if hint else ""
        at_cap = html.escape(str(g.get("at_cap_text") or "Already at the ceiling."))

        if not guard:
            row = f'  <div class="cheat-row">{grant}{hint_div}</div>'
        else:
            row = (
                f'  <div class="cheat-row">\n'
                f'    <<if {guard}>>{grant}{hint_div}\n'
                f'    <<else>><span class="cheat-row-maxed">{btn}</span>'
                f'<div class="cheat-at-cap">{at_cap}</div>\n'
                f'    <</if>>\n'
                f'  </div>'
            )

        unlock = f'$flags["cheat_{g.get("id")}"]'
        return f'  <<if {unlock}>>\n{row}\n  <</if>>'

    @staticmethod
    def _fmt_num(n) -> str:
        """Render a number for SugarCube without a stray trailing .0 on whole values."""
        try:
            f = float(n)
        except (TypeError, ValueError):
            return "0"
        return str(int(f)) if f == int(f) else str(f)

    def _generate_missing_media_page(self) -> str:
        """Generate the Missing Media Page passage for debug mode."""
        if not self.missing_media:
            # No missing media - return empty passage that just redirects back
            return """:: MissingMediaPage
<h2>Missing Media Files</h2>
<p>No missing media files found.</p>

<<link "← Back">><<run setup.smartBack()>><</link>>
"""

        # Group missing media by category
        from collections import defaultdict
        by_category = defaultdict(list)
        for item in self.missing_media:
            by_category[item['category']].append(item)

        # Get game folder name for search URLs
        game_name = self.options.get("game_folder") or self._slugify(self.project.name)

        # Build page content
        total_missing = len(self.missing_media)
        content = f""":: MissingMediaPage
<h2>⚠️ Missing Media Files</h2>
<p>Found <strong>{total_missing}</strong> missing media file{"s" if total_missing != 1 else ""}.</p>

"""

        # Category order
        category_order = ['Locations', 'Story Scenes', 'Endings', 'Activities', 'Solo Activities', 'Social Media', 'Images', 'Other']

        for category in category_order:
            if category not in by_category:
                continue

            items = by_category[category]
            count = len(items)
            content += f"""<h3>{category} ({count} missing)</h3>
<div class="missing-media-section" style="margin-bottom:20px;">
"""

            # Sort items by file path
            sorted_items = sorted(items, key=lambda x: x['file'])

            for item in sorted_items:
                file_path = html.escape(item['file'])
                media_type = item['type'].upper()
                description = html.escape(item['description']) if item['description'] else ''
                search_queries = item.get('search_queries', [])

                content += f"""<div class="missing-item" style="border:1px solid #ddd;padding:12px;margin:8px 0;border-radius:6px;background:#fafafa;">
  <p style="margin:0;font-weight:bold;color:#333;">[{media_type}] {file_path}</p>
"""
                if description:
                    content += f"""  <p style="margin:4px 0 0;color:#666;font-style:italic;font-size:14px;">{description}</p>
"""

                # Add search links
                if search_queries and isinstance(search_queries, list):
                    content += """  <div style="margin-top:8px;">
"""
                    for query in search_queries:
                        if query and isinstance(query, str):
                            search_url = self._build_search_url(query.strip(), game_name, item['file'])
                            escaped_url = html.escape(search_url)
                            escaped_query = html.escape(query.strip())
                            content += f"""    <a href="{escaped_url}" target="_blank" style="display:inline-block;margin:4px 8px 4px 0;padding:6px 12px;background:#3b82f6;color:white;text-decoration:none;border-radius:4px;font-size:13px;">🔍 {escaped_query}</a>
"""
                    content += """  </div>
"""

                content += """</div>
"""

            content += """</div>
"""

        # Add back link
        content += """
<<link "← Back">><<run setup.smartBack()>><</link>>
"""

        return content

    def _get_story_arc_canvas_order(self):
        """
        Get ordered list of (chapter_name, canvas_list) from story arc.
        Returns (ordered_chapters, story_canvas_slugs_set).
        """
        from collections import defaultdict

        story_arc = self.project.metadata.get("story_arc", {}) if self.project.metadata else {}
        if not story_arc:
            return [], set()

        chapters = story_arc.get("chapters", [])
        nodes = story_arc.get("nodes", [])

        if not chapters or not nodes:
            return [], set()

        # Sort chapters by order
        sorted_chapters = sorted(chapters, key=lambda c: c.get("order", 0))

        # Group nodes by chapter, maintaining order from nodes list
        chapter_canvases = defaultdict(list)
        story_canvas_slugs = set()

        for node in nodes:
            canvas_slug = node.get("linked_canvas")
            chapter_id = node.get("chapter")
            if canvas_slug and chapter_id:
                chapter_canvases[chapter_id].append({
                    "slug": canvas_slug,
                    "name": node.get("name", canvas_slug)
                })
                story_canvas_slugs.add(canvas_slug)

        # Build ordered result
        ordered = []
        for chapter in sorted_chapters:
            chapter_id = chapter.get("id", "")
            chapter_name = chapter.get("name", chapter_id)
            canvases = chapter_canvases.get(chapter_id, [])
            if canvases:
                ordered.append((chapter_name, canvases))

        return ordered, story_canvas_slugs

    def _generate_canvas_review_pages(self) -> str:
        """
        Generate Canvas Review pages for dev mode.

        Returns CanvasReviewList and individual CanvasReview_{slug} passages.
        Uses static HTML with baked-in canvas IDs and approval status.
        No SugarCube variables or <<run>> macros for IDs - eliminates timing issues.

        Structure:
        1. Story Progression - canvases ordered by story arc (chapter order → node sequence)
        2. Activities - grouped by name, sorted by tier
        """
        from collections import defaultdict
        from pathlib import Path

        # Get game folder name for storing approvals
        game_folder = self.options.get("game_folder", "")

        # Load approval status from JSON file (if exists)
        approvals = self._load_canvas_approvals(game_folder)

        # Get video path for media URLs (default to ./media)
        video_path = getattr(self, 'video_path', '') or './media'

        # Process all included canvases
        all_canvases = list(self.story_canvases)
        if self.project.starting_canvas:
            all_canvases.insert(0, self.project.starting_canvas)

        # Get story arc ordering
        story_chapters, story_canvas_slugs = self._get_story_arc_canvas_order()

        # Helper to get approval badge HTML
        def get_badge_html(canvas_slug):
            status = approvals.get(canvas_slug, {}).get('status', 'pending')
            if status == 'approved':
                return '<span class="approval-badge approved">✓</span>'
            elif status == 'needs_changes':
                return '<span class="approval-badge needs-changes">✗</span>'
            else:
                return '<span class="approval-badge pending">·</span>'

        # Build Story Progression HTML (from story arc)
        story_html = ""
        if story_chapters:
            story_html = '<h3>Story Progression</h3>\n<div class="story-chapters">\n'
            for chapter_name, canvases in story_chapters:
                story_html += f'<div class="chapter-group">\n'
                story_html += f'  <strong>{chapter_name}</strong>\n'
                story_html += '  <div class="chapter-canvases">\n'
                for c in canvases:
                    badge = get_badge_html(c['slug'])
                    story_html += f'''    <span class="canvas-item" data-canvas-id="{c['slug']}">
      {badge}
      <<button "{c['name']}">><<goto "CanvasReview_{c['slug']}">><</button>>
    </span>\n'''
                story_html += '  </div>\n</div>\n'
            story_html += '</div>\n'

        # Build Activities HTML (all activity canvases, including story-arc-linked ones)
        # Group by name (for activities with tiers)
        activity_groups = defaultdict(list)
        for canvas in all_canvases:
            canvas_slug = self._get_canvas_slug(canvas)

            canvas_name = canvas.name or "Unnamed Canvas"

            # Get tier from trigger priority if available
            tier = 0
            if hasattr(canvas, 'trigger') and canvas.trigger:
                tier = getattr(canvas.trigger, 'priority', 0)

            activity_groups[canvas_name].append({
                'slug': canvas_slug,
                'name': canvas_name,
                'tier': tier,
                'tier_label': f"T{tier}" if tier > 0 else "T0",
            })

        activity_html = ""
        if activity_groups:
            activity_html = "<h3>Activities</h3>\n"
            for activity_name, canvases in sorted(activity_groups.items()):
                # Sort by tier within each activity group
                canvases = sorted(canvases, key=lambda x: x['tier'])
                activity_html += f'<div class="activity-group">\n'
                activity_html += f'  <strong>{activity_name}</strong>\n'
                activity_html += f'  <div class="tier-buttons">\n'
                for c in canvases:
                    badge = get_badge_html(c['slug'])
                    activity_html += f'''    <span class="canvas-item" data-canvas-id="{c['slug']}">
      {badge}
      <<button "{c['tier_label']}">><<goto "CanvasReview_{c['slug']}">><</button>>
    </span>\n'''
                activity_html += f'  </div>\n</div>\n'

        empty_msg = ""
        if not story_chapters and not activity_groups:
            empty_msg = "<p><em>No canvases found in this project.</em></p>\n"

        list_passage = f""":: CanvasReviewList
<div class="canvas-review-list" data-game-name="{game_folder}">
<h2>Canvas Review</h2>

{story_html}{activity_html}{empty_msg}
<div class="review-back-btn">
<<button "Back to Game">><<goto "Navigation">><</button>>
</div>
</div>
"""

        # Generate one detail passage per canvas (static canvas ID, no timing issues)
        detail_passages = []
        for canvas in all_canvases:
            canvas_slug = self._get_canvas_slug(canvas)
            canvas_name = canvas.name or "Unnamed Canvas"

            # Render canvas content (nodes and blocks)
            content_html = self._render_canvas_review_content(canvas, video_path)

            passage = f""":: CanvasReview_{canvas_slug}
<div id="canvas-review-detail" data-canvas-id="{canvas_slug}" data-game-name="{game_folder}">
<h2>{canvas_name}</h2>
<p class="canvas-id-display">Canvas ID: <code>{canvas_slug}</code></p>

{content_html}

<div class="review-back-btn">
<<button "← Back to List">><<goto "CanvasReviewList">><</button>>
</div>
</div>
"""
            detail_passages.append(passage)

        # CSS for review pages
        css_passage = """:: CanvasReviewStyles [stylesheet]
/* Canvas Review Styles - Dev Mode Only */

.canvas-review-list {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.activity-group {
  margin-bottom: 16px;
  padding: 12px;
  background: rgba(255,255,255,0.05);
  border-radius: 8px;
}

.activity-group strong {
  display: block;
  margin-bottom: 8px;
  color: #4a90d9;
}

.tier-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tier-buttons button {
  padding: 6px 12px;
  font-size: 13px;
  min-width: 40px;
}

.canvas-item {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.approval-badge {
  font-weight: bold;
  font-size: 14px;
  color: #888;
}

.approval-badge.approved {
  color: #22c55e;
}

.approval-badge.needs-changes {
  color: #ef4444;
}

.approval-badge.pending {
  color: #888;
}

/* Story Progression - Chapter Groups */
.story-chapters {
  margin-bottom: 24px;
}

.chapter-group {
  margin-bottom: 16px;
  padding: 12px;
  background: rgba(255,255,255,0.05);
  border-radius: 8px;
  border-left: 3px solid #4a90d9;
}

.chapter-group strong {
  display: block;
  margin-bottom: 10px;
  color: #4a90d9;
  font-size: 14px;
}

.chapter-canvases {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding-left: 8px;
}

.chapter-canvases .canvas-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.chapter-canvases button {
  text-align: left;
  padding: 6px 12px;
}

#canvas-review-detail {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.canvas-id-display {
  font-size: 12px;
  color: #888;
  margin-bottom: 20px;
}

.canvas-id-display code {
  background: rgba(255,255,255,0.1);
  padding: 2px 6px;
  border-radius: 4px;
}

.review-node {
  border: 1px solid #444;
  border-radius: 8px;
  padding: 16px;
  margin: 16px 0;
  background: rgba(255,255,255,0.03);
}

.review-node h4 {
  margin: 0 0 12px 0;
  color: #4a90d9;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.review-block {
  margin: 8px 0;
  padding: 8px;
}

.review-block-paragraph p {
  margin: 0;
}

.review-block-dialog blockquote {
  margin: 0;
  padding-left: 12px;
  border-left: 3px solid #4a90d9;
}

.review-block-dialog strong {
  color: #4a90d9;
}

.media-placeholder {
  background: rgba(74, 144, 217, 0.1);
  padding: 12px;
  border-radius: 6px;
  font-family: monospace;
  font-size: 12px;
  color: #888;
}

.media-caption {
  font-size: 12px;
  color: #888;
  margin: 4px 0 0 0;
}

.exit-info {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px dashed #444;
  color: #666;
  font-size: 13px;
}

.exit-info ul {
  margin: 8px 0 0 20px;
  padding: 0;
}

.exit-info li {
  margin: 4px 0;
}

.review-back-btn {
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid #333;
}

.review-back-btn button {
  padding: 10px 20px;
}
"""

        # Combine all passages
        all_passages = [list_passage] + detail_passages + [css_passage]
        return "\n\n".join(all_passages)

    def _load_canvas_approvals(self, game_folder: str) -> dict:
        """Load approval status from JSON file (if exists)."""
        from pathlib import Path
        from django.conf import settings

        if not game_folder:
            return {}

        approval_file = Path(settings.BASE_DIR) / game_folder / "game" / "canvas_approvals.json"
        if approval_file.exists():
            try:
                with open(approval_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def _render_canvas_review_content(self, canvas, video_path: str) -> str:
        """Render canvas content (nodes and blocks) as static HTML for review."""
        from html import escape

        nodes = self._get_canvas_nodes_ordered(canvas)
        html_parts = []

        for node in nodes:
            node_name = escape(node.name or 'Unnamed Node')
            node_html = f'<div class="review-node">\n<h4>NODE: {node_name}</h4>\n'

            # Render blocks
            if hasattr(node, 'node_data') and node.node_data:
                blocks = node.node_data.get('blocks', [])
                for block in blocks:
                    block_type = block.get('type', 'unknown')
                    props = block.get('props', {}) or {}
                    content_parts = block.get('content', '')

                    # Extract text content
                    text_content = ''
                    if isinstance(content_parts, str):
                        text_content = content_parts
                    elif isinstance(content_parts, list):
                        for part in content_parts:
                            if isinstance(part, dict) and 'text' in part:
                                text_content += part.get('text', '')

                    text_content = escape(text_content)

                    if block_type == 'paragraph':
                        node_html += f'<div class="review-block review-block-paragraph"><p>{text_content}</p></div>\n'
                    elif block_type == 'dialog':
                        speaker = escape(props.get('speaker', ''))
                        node_html += f'<div class="review-block review-block-dialog"><blockquote><strong>{speaker}:</strong> {text_content}</blockquote></div>\n'
                    elif block_type == 'image':
                        file_path = props.get('file', '')
                        description = escape(props.get('description', ''))
                        if file_path:
                            node_html += f'<div class="review-block review-block-image"><img src="{video_path}/{file_path}" style="max-width:100%;max-height:70vh;object-fit:contain;height:auto;border-radius:8px;" />'
                            if description:
                                node_html += f'<p class="media-caption"><em>{description}</em></p>'
                            node_html += '</div>\n'
                        else:
                            node_html += '<div class="review-block"><div class="media-placeholder">[IMAGE] (no file)</div></div>\n'
                    elif block_type == 'video':
                        file_path = props.get('file', '')
                        description = escape(props.get('description', ''))
                        if file_path:
                            node_html += f'<div class="review-block review-block-video"><video src="{video_path}/{file_path}" autoplay muted loop playsinline controls preload="metadata" style="max-width:100%;max-height:70vh;object-fit:contain;height:auto;border-radius:8px;"></video>'
                            if description:
                                node_html += f'<p class="media-caption"><em>{description}</em></p>'
                            node_html += '</div>\n'
                        else:
                            node_html += '<div class="review-block"><div class="media-placeholder">[VIDEO] (no file)</div></div>\n'
                    elif block_type == 'clip':
                        clip_id = props.get('clipId')
                        if clip_id:
                            clip = self.clips_by_id.get(str(clip_id))
                            if clip:
                                clip_url = clip.file_url if hasattr(clip, 'file_url') else ""
                                if clip_url:
                                    poster_url = clip.poster_url if hasattr(clip, 'poster_url') else None
                                    poster_attr = f' poster="{escape(poster_url)}"' if poster_url else ""
                                    description = escape(props.get('description', ''))
                                    node_html += f'<div class="review-block review-block-video"><video src="{escape(clip_url)}" autoplay muted loop playsinline controls preload="metadata"{poster_attr} style="max-width:100%;max-height:70vh;object-fit:contain;height:auto;border-radius:8px;"></video>'
                                    if description:
                                        node_html += f'<p class="media-caption"><em>{description}</em></p>'
                                    node_html += '</div>\n'
                                else:
                                    node_html += f'<div class="review-block"><div class="media-placeholder">[CLIP: {clip_id}] (no URL)</div></div>\n'
                            else:
                                node_html += f'<div class="review-block"><div class="media-placeholder">[CLIP: {clip_id}] (not found)</div></div>\n'
                        else:
                            node_html += '<div class="review-block"><div class="media-placeholder">[CLIP] (no clipId)</div></div>\n'
                    elif block_type == 'heading':
                        node_html += f'<div class="review-block review-block-heading"><h3>{text_content}</h3></div>\n'
                    else:
                        node_html += f'<div class="review-block block-other">{text_content}</div>\n'

            # Render exit block info
            exit_block = getattr(node, 'exit_block', {}) or {}
            if exit_block:
                exit_type = exit_block.get('type', 'none')
                node_html += f'<div class="exit-info"><em>Exit: {exit_type}</em>'
                if exit_type == 'choices':
                    choices = exit_block.get('choices', [])
                    if choices:
                        node_html += '<ul>'
                        for choice in choices:
                            if choice:
                                choice_text = escape(choice.get('text', ''))
                                node_html += f'<li>{choice_text}</li>'
                        node_html += '</ul>'
                node_html += '</div>\n'

            node_html += '</div>'
            html_parts.append(node_html)

        return '\n'.join(html_parts)

    # ========== HELPER METHODS ==========

    def _get_canvases_for_location(self, location_id):
        """Get story canvases triggered by a specific location."""
        return [canvas for canvas in self.story_canvases
                if hasattr(canvas, 'trigger') and canvas.trigger and str(canvas.trigger.location_id) == str(location_id)]

    def _get_canvases_for_location_with_schedules(self, location_id):
        """Get story canvases with schedule metadata for a specific location."""
        canvases_with_schedules = []
        for canvas in self.story_canvases:
            if hasattr(canvas, 'trigger') and canvas.trigger and str(canvas.trigger.location_id) == str(location_id):
                # Get schedules for this trigger (already prefetched)
                schedules = self._trigger_schedules(canvas.trigger)
                canvases_with_schedules.append({
                    'canvas': canvas,
                    'schedules': schedules,
                    'has_schedules': len(schedules) > 0
                })
        return canvases_with_schedules

    def _get_location_by_id(self, location_id):
        """Get location object by UUID."""
        for location in self.locations:
            if str(location.id) == str(location_id):
                return location
        return None

    def _get_location_name(self, location_id):
        """Get location name by UUID from pre-loaded locations."""
        loc = self._get_location_by_id(location_id)
        return loc.name if loc else "Unknown"

    def _format_schedule_human_readable_with_days(self, schedules):
        """Convert schedules to human-readable format like 'Mon-Fri 5-7 PM or 7-10 PM'."""
        if not schedules:
            return "anytime"

        DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        def format_single_schedule(schedule):
            # Format days
            days = sorted(schedule.weekdays) if schedule.weekdays else []
            if not days or days == list(range(7)):
                day_str = "Daily"
            elif days == [0, 1, 2, 3, 4]:
                day_str = "Mon-Fri"
            elif days == [5, 6]:
                day_str = "Sat-Sun"
            elif len(days) == 1:
                day_str = DAY_NAMES[days[0]]
            else:
                # Compress consecutive days: [0,1,2] → "Mon-Wed"
                if days == list(range(days[0], days[-1] + 1)):
                    day_str = f"{DAY_NAMES[days[0]]}-{DAY_NAMES[days[-1]]}"
                else:
                    day_str = ", ".join(DAY_NAMES[d] for d in days)

            # Format time
            start = schedule.start_time.strftime("%I:%M %p").lstrip("0").replace(":00", "")
            if schedule.end_time:
                end = schedule.end_time.strftime("%I:%M %p").lstrip("0").replace(":00", "")
                time_str = f"{start}-{end}"
            else:
                time_str = f"at {start}"

            return f"{day_str} {time_str}"

        # Format all schedules
        formatted = [format_single_schedule(s) for s in schedules]
        return " or ".join(formatted)

    def _build_story_arc_json(self) -> str:
        """
        Build story_arc JSON for runtime story journal.

        Loads from Project.metadata if available (set during TOML import),
        otherwise falls back to empty structure with default emotion mappings.
        """
        # Load story_arc from Project.metadata if available
        metadata = getattr(self.project, 'metadata', None) or {}
        story_arc = metadata.get("story_arc")

        if story_arc:
            # Ensure emotion_mappings has defaults if not specified
            if not story_arc.get("emotion_mappings"):
                story_arc["emotion_mappings"] = self._get_default_emotion_mappings()
            return json.dumps(story_arc)

        # Fallback to auto-inference structure (for projects without story_arc)
        return json.dumps({
            "version": "1.0",
            "chapters": [],
            "nodes": [],
            "groups": [],
            "emotion_mappings": self._get_default_emotion_mappings(),
            "guidance": {
                "stuck_threshold_minutes": 30,
                "hint_style": "observation",
                "templates": []
            },
            "is_auto_inferred": True
        })

    def _get_default_emotion_mappings(self) -> dict:
        """Generate default emotion mappings for common traits."""
        return {
            "affection": {
                "trait_owner": "npc",
                "ranges": [
                    {"min": 0, "max": 25, "label": "distant", "description": "There's still a barrier between you"},
                    {"min": 26, "max": 50, "label": "warming", "description": "Something is slowly growing between you"},
                    {"min": 51, "max": 75, "label": "connected", "description": "She feels genuinely close to you now"},
                    {"min": 76, "max": 100, "label": "devoted", "description": "Her feelings for you run deep"}
                ]
            },
            "arousal": {
                "trait_owner": "npc",
                "ranges": [
                    {"min": 0, "max": 20, "label": "calm", "description": "Composed and relaxed"},
                    {"min": 21, "max": 50, "label": "aware", "description": "There's a subtle tension in her gaze"},
                    {"min": 51, "max": 75, "label": "yearning", "description": "Her body language speaks of desire"},
                    {"min": 76, "max": 100, "label": "burning", "description": "The passion is barely contained"}
                ]
            },
            "appreciation": {
                "trait_owner": "npc",
                "ranges": [
                    {"min": 0, "max": 25, "label": "indifferent", "description": "Your efforts go unnoticed"},
                    {"min": 26, "max": 50, "label": "noticing", "description": "She's starting to notice your care"},
                    {"min": 51, "max": 75, "label": "grateful", "description": "She deeply appreciates what you do"},
                    {"min": 76, "max": 100, "label": "cherishing", "description": "She treasures every moment with you"}
                ]
            },
            "trust": {
                "trait_owner": "npc",
                "ranges": [
                    {"min": 0, "max": 25, "label": "wary", "description": "She keeps her guard up"},
                    {"min": 26, "max": 50, "label": "opening", "description": "Walls are slowly coming down"},
                    {"min": 51, "max": 75, "label": "trusting", "description": "There's real trust between you"},
                    {"min": 76, "max": 100, "label": "complete", "description": "Complete faith in each other"}
                ]
            }
        }

    def _build_canvas_substitutions_json(self) -> str:
        """
        PRD 25 — build the runtime canvas substitution map.

        Returns JSON: { "<parent_canvas_uuid>": [ {target_canvas_id, chance, conditions}, ... ] }

        Author writes substitution rules in TOML using slugs. This method
        resolves slugs to runtime UUIDs (matching `setup.help_data.locationCanvases`
        keying) so the runtime helper `setup.checkAndSubstituteCanvas` can
        look up targets directly.
        """
        from apps.stories.models import StoryCanvas

        # Build slug→UUID lookup once across all included canvases
        all_canvases = list(self._all_canvases())
        slug_to_uuid = {}
        for c in all_canvases:
            slug = (c.metadata or {}).get("slug")
            if slug:
                slug_to_uuid[slug] = str(c.id)

        canvas_subs_map = {}
        for canvas in all_canvases:
            trigger = getattr(canvas, 'trigger', None)
            if not trigger:
                continue
            rules = (trigger.metadata or {}).get("substitutions") or []
            if not rules:
                continue
            parent_uuid = str(canvas.id)
            resolved = []
            for r in rules:
                if not isinstance(r, dict):
                    continue
                target_slug = r.get("target_canvas_id")
                target_uuid = slug_to_uuid.get(target_slug)
                if not target_uuid:
                    # Validator should have caught this; defensive skip.
                    continue
                resolved.append({
                    "target_canvas_id": target_uuid,
                    "chance": float(r.get("chance", 0)),
                    "conditions": r.get("conditions") or None,
                    # Doc 69 Item 1 — Pattern B exclusive_group passthrough.
                    # When non-None, rules sharing the same group name share one
                    # dice roll at runtime (mutual exclusion). Absent / None
                    # means Pattern A independent rolls.
                    "exclusive_group": r.get("exclusive_group") or None,
                })
            if resolved:
                canvas_subs_map[parent_uuid] = resolved
        return json.dumps(canvas_subs_map)

    def _canvases_with_substitutions(self) -> Dict[str, str]:
        """
        PRD 25 — return mapping {canvas_uuid: parent_uuid_string} for
        emission injection in `_generate_canvas_node_passages`. Cached on
        first call.
        """
        from apps.stories.models import StoryCanvas

        if hasattr(self, "_canvases_with_subs_cache"):
            return self._canvases_with_subs_cache

        cache: Dict[str, str] = {}
        all_canvases = self._all_canvases()
        for canvas in all_canvases:
            trigger = getattr(canvas, 'trigger', None)
            if not trigger:
                continue
            rules = (trigger.metadata or {}).get("substitutions") or []
            if rules:
                cache[str(canvas.id)] = str(canvas.id)
        self._canvases_with_subs_cache = cache
        return cache

    def _build_help_data(self) -> str:
        """
        Build per-NPC activity data for Quest Page.

        Creates a JSON structure grouping activities by NPC with:
        - Location and schedule information for "Visit X between Y" display
        - Trait requirements for locked activities
        - Trait effects for the modal feature
        """
        from apps.npcs.models import NPC

        # Get player name from project's player character
        player_name = "Player"
        pc = getattr(self.project, 'player_character', None)
        if pc is not None:
            player_name = pc.name or player_name

        help_data = {
            "npcs": {},  # npc_id -> {name, activities: [...]}
            "player": {  # Solo/player activities (no NPC association)
                "name": player_name,
                "activities": []
            },
            "trait_activities": {},  # trait_name -> [activities that boost this trait]
            "flag_unlock_map": {},  # flag_key -> canvas info that sets this flag
            "starting_canvas_id": str(self.project.starting_canvas.id) if self.project.starting_canvas else None,
            "locationCanvases": {},  # location_id -> [canvas_ids] for nav indicators
            "canvasIdToActivityName": {},  # canvas_id -> activity name for shared daily limits
            "canvasConditionalChoices": {},  # canvas_id -> [{key, conditions}] for unlock highlighting
            "canvasIdToNpcUuid": {},  # canvas_id -> npc_uuid for trait decay interaction tracking
        }

        # Load story_arc from Project.metadata
        metadata = getattr(self.project, 'metadata', None) or {}
        story_arc = metadata.get("story_arc", {})
        nodes = story_arc.get("nodes", [])

        # Load NPCs for name lookup - index by TOML slug AND name-based slug
        npc_lookup = {}
        hidden_npc_ids: set = set()
        try:
            for npc in self._all_npcs():
                npc_info = {"id": str(npc.id), "name": npc.name}
                # Index by name-based slug (legacy)
                name_slug = npc.name.lower().strip().replace(' ', '_') if npc.name else str(npc.id)
                npc_lookup[name_slug] = npc_info
                # Also index by TOML slug from ai_behavior_config (matches story_arc.nodes.npc)
                toml_slug = (npc.ai_behavior_config or {}).get("slug")
                if toml_slug:
                    npc_lookup[toml_slug] = npc_info
                if getattr(npc, "hidden_from_ui", False):
                    hidden_npc_ids.add(str(npc.id))
        except (AttributeError, TypeError) as e:
            logger.warning("Error building NPC lookup for help system: %s", e)

        # Build canvas lookup for trigger info - by slug, name, and ID
        # Query ALL project canvases to ensure we find linked canvases
        from apps.stories.models import StoryCanvas
        canvas_by_slug = {}
        canvas_by_name = {}
        all_canvases = self._all_canvases()
        for canvas in all_canvases:
            canvas_by_name[canvas.name] = canvas
            # Index by slug from metadata (matches TOML canvas IDs)
            slug = canvas.metadata.get("slug") if canvas.metadata else None
            if slug:
                canvas_by_slug[slug] = canvas
            # Also index by database ID
            canvas_by_slug[str(canvas.id)] = canvas

        # Build location lookup for flag_unlock_map
        location_lookup = {str(loc.id): loc.name for loc in self.locations}

        # Build canvas_id -> npc_name map for cross-NPC hint detection
        canvas_npc_map = {}  # canvas_id (str) -> npc_name (str)

        # From story_arc nodes: npc -> linked_canvas -> resolve canvas ID
        for node in nodes:
            npc_slug = node.get("npc")
            if npc_slug:
                linked_canvas_id = node.get("linked_canvas")
                if linked_canvas_id:
                    canvas = canvas_by_slug.get(linked_canvas_id) or canvas_by_name.get(linked_canvas_id)
                    if canvas:
                        npc_info = npc_lookup.get(npc_slug, {})
                        canvas_npc_map[str(canvas.id)] = npc_info.get("name", npc_slug)

        # From canvas trait effects (for non-story-arc canvases)
        for canvas in all_canvases:
            cid = str(canvas.id)
            if cid not in canvas_npc_map:
                effects = self._extract_trait_effects_from_canvas(canvas)
                for eff in effects:
                    if eff.get("npc_id"):
                        npc_info = npc_lookup.get(eff["npc_id"], {})
                        canvas_npc_map[cid] = npc_info.get("name", eff["npc_id"])
                        break

        # Build flag_unlock_map: flag_key -> canvas info that sets it
        help_data["flag_unlock_map"] = self._build_flag_unlock_map(all_canvases, location_lookup, canvas_npc_map)

        for node in nodes:
            npc_slug = node.get("npc")

            # Get canvas and trigger info
            linked_canvas_id = node.get("linked_canvas")
            canvas = None
            trigger = None
            location_name = None
            schedule_text = None

            if linked_canvas_id:
                # Find canvas by slug first (matches TOML canvas IDs)
                canvas = canvas_by_slug.get(linked_canvas_id)
                # Fall back to name match
                if not canvas:
                    canvas = canvas_by_name.get(linked_canvas_id)

                # Skip location/schedule extraction for starting canvas (it plays automatically via "Start Game")
                is_starting_canvas = (
                    self.project.starting_canvas and canvas and
                    str(canvas.id) == str(self.project.starting_canvas.id)
                )

                if canvas and hasattr(canvas, 'trigger') and canvas.trigger and not is_starting_canvas:
                    trigger = canvas.trigger
                    # Get location name
                    if trigger.location_id:
                        for loc in self.locations:
                            if str(loc.id) == str(trigger.location_id):
                                location_name = loc.name
                                break
                    # Get schedule text
                    if self._trigger_has_schedules(trigger):
                        schedule_text = self._format_schedule_human_readable(trigger)

            # Extract trait effects from canvas nodes (tiered + flat fallback)
            trait_effects = []
            tiered_effects = None
            if canvas:
                tiered_effects = self._extract_tiered_effects_from_canvas(canvas)
                if tiered_effects is not None:
                    # Flatten for backward-compat uses (trait_activities index)
                    for tier in tiered_effects:
                        trait_effects.extend(tier.get("effects", []))
                else:
                    trait_effects = self._extract_trait_effects_from_canvas(canvas)

            # Extract canvas trigger conditions (for Quest Page to show requirements)
            canvas_conditions = None
            if canvas and hasattr(canvas, 'trigger') and canvas.trigger:
                cond = getattr(canvas.trigger, 'conditions', None)
                if cond and isinstance(cond, dict) and cond.get('items'):
                    canvas_conditions = cond

            # Extract node-level conditions if linked_canvas_node is set
            linked_canvas_node = node.get("linked_canvas_node")
            node_conditions = None
            if linked_canvas_node and canvas:
                node_conditions = self._extract_conditions_for_target_node(
                    canvas, linked_canvas_node
                )

            activity = {
                "node_id": node.get("id"),
                "name": node.get("name"),
                "linked_flag": node.get("linked_flag"),
                "canvas_id": str(canvas.id) if canvas else None,
                "canvas_slug": linked_canvas_id,
                "linked_canvas_node": linked_canvas_node,
                "requires_nodes": node.get("requires_nodes", []),
                "requires_group": node.get("requires_group"),
                "location": location_name,
                "schedule": schedule_text,
                "trait_requirements": node.get("trait_requirements", []),
                "trait_effects": trait_effects,
                "tiered_effects": tiered_effects,
                "canvas_conditions": canvas_conditions,
                "node_conditions": node_conditions,
                "guide_hint": node.get("guide_hint", ""),
                "linked_phone": node.get("linked_phone"),
            }

            # Add to NPC's activities or player's activities
            if npc_slug:
                npc_info = npc_lookup.get(npc_slug, {"id": npc_slug, "name": npc_slug.title()})
                npc_id = npc_info["id"]
                if npc_id in hidden_npc_ids:
                    pass  # hidden NPCs omitted from Guide Page
                else:
                    if npc_id not in help_data["npcs"]:
                        help_data["npcs"][npc_id] = {
                            "name": npc_info["name"],
                            "activities": []
                        }
                    help_data["npcs"][npc_id]["activities"].append(activity)
            else:
                # Solo/player node — no NPC association
                help_data["player"]["activities"].append(activity)

            # Index by trait effects for modal
            for effect in trait_effects:
                trait_name = effect.get("trait")
                if trait_name:
                    if trait_name not in help_data["trait_activities"]:
                        help_data["trait_activities"][trait_name] = []
                    help_data["trait_activities"][trait_name].append(activity)

        # Process regular activity canvases (not in story_arc)
        # These include Morning Coffee, Helping Chores, etc.
        processed_canvas_ids = set()
        for npc_id, npc_data in help_data["npcs"].items():
            for activity in npc_data["activities"]:
                if activity.get("canvas_id"):
                    processed_canvas_ids.add(activity["canvas_id"])

        for canvas in all_canvases:
            canvas_id_str = str(canvas.id)
            if canvas_id_str in processed_canvas_ids:
                continue  # Already processed via story_arc

            # Extract trait effects from canvas (tiered + flat fallback)
            tiered_effects = self._extract_tiered_effects_from_canvas(canvas)
            if tiered_effects is not None:
                trait_effects = []
                for tier in tiered_effects:
                    trait_effects.extend(tier.get("effects", []))
                if not trait_effects:
                    continue
            else:
                trait_effects = self._extract_trait_effects_from_canvas(canvas)
                if not trait_effects:
                    continue

            # Get NPC from effects (effects contain npc_id for NPC-targeted effects)
            # Some activities only boost player traits (no NPC) - we still need to index them
            npc_id = None
            for effect in trait_effects:
                if effect.get("npc_id"):
                    npc_id = effect["npc_id"]
                    break

            # Get trigger info for location, schedule, and conditions
            trigger = getattr(canvas, 'trigger', None)

            # Check if random-mode canvas (passive events, not quest-trackable)
            is_random = bool(trigger and trigger.metadata and trigger.metadata.get("trigger_mode") == "random")

            location_name = None
            schedule_text = None
            canvas_conditions = None

            if trigger:
                # Get location
                if trigger.location_id:
                    location_name = location_lookup.get(str(trigger.location_id))

                # Get schedule
                if self._trigger_has_schedules(trigger):
                    schedule_text = self._format_schedule_human_readable(trigger)

                # Get canvas trigger conditions (for filtering tiered activities)
                cond = getattr(trigger, 'conditions', None)
                if cond and isinstance(cond, dict) and cond.get('items'):
                    canvas_conditions = cond

            activity = {
                "node_id": None,  # Not a story arc node
                "name": canvas.name,
                "linked_flag": None,
                "canvas_id": canvas_id_str,
                "requires_nodes": [],
                "requires_group": None,
                "location": location_name,
                "schedule": schedule_text,
                "trait_requirements": [],
                "trait_effects": trait_effects,
                "tiered_effects": tiered_effects,
                "canvas_conditions": canvas_conditions,
                "is_repeatable": trigger.is_repeatable if trigger else True,
                "is_random": is_random,
            }

            # Add to NPC's/player's quest activities (skip random — not quest-trackable)
            if not is_random:
                if npc_id:
                    npc_info = npc_lookup.get(npc_id, {"id": npc_id, "name": npc_id.replace("npc_", "").replace("_", " ").title()})
                    resolved_npc_id = npc_info["id"]  # Use database UUID as key, not TOML slug

                    if resolved_npc_id in hidden_npc_ids:
                        pass  # hidden NPCs omitted from Guide Page
                    else:
                        if resolved_npc_id not in help_data["npcs"]:
                            help_data["npcs"][resolved_npc_id] = {
                                "name": npc_info["name"],
                                "activities": []
                            }
                        help_data["npcs"][resolved_npc_id]["activities"].append(activity)
                else:
                    # Solo/player activity — no NPC association
                    help_data["player"]["activities"].append(activity)

            # Index by trait effects for modal (includes player-only activities)
            for effect in trait_effects:
                trait_name = effect.get("trait")
                if trait_name:
                    if trait_name not in help_data["trait_activities"]:
                        help_data["trait_activities"][trait_name] = []
                    help_data["trait_activities"][trait_name].append(activity)

        # L2-2 — Build local slug → runtime passage name map for entry_only_from
        # translation at help_data emission. Same logic as _generate_initialization
        # builds passage_to_location, but inverted (forward map). Local to this
        # method since cross-method state would require self.* promotion.
        slug_to_passage_name = {}
        for loc in self.locations:
            loc_props = getattr(loc, 'properties', None) or {}
            loc_slug = loc_props.get("slug") or f"loc_{loc.id}"
            slug_to_passage_name[loc_slug] = self._location_passage_name(loc)

        # Build locationCanvases mapping for navigation indicators
        # Maps location_id -> list of canvas metadata for availability checking
        for location in self.locations:
            location_canvas_list = []
            # Get canvases for this location with inheritance
            canvases_info = self._get_canvases_for_location_with_inheritance(location)
            for canvas_info in canvases_info:
                canvas = canvas_info['canvas']
                schedules = canvas_info['schedules']
                trigger = canvas.trigger if hasattr(canvas, 'trigger') else None

                # Build schedule params for isScheduleActive check (supports multiple schedules)
                schedule_params = []
                if schedules:
                    for schedule in schedules:
                        schedule_params.append({
                            "weekdays": list(schedule.weekdays) if schedule.weekdays else [],
                            "startTime": schedule.start_time.strftime("%H:%M") if schedule.start_time else None,
                            "endTime": schedule.end_time.strftime("%H:%M") if schedule.end_time else None
                        })

                # Get conditions
                conditions = None
                if trigger:
                    try:
                        cond_obj = getattr(trigger, 'conditions', None)
                        if cond_obj:
                            conditions = cond_obj
                    except AttributeError as e:
                        logger.warning("Error accessing trigger conditions: %s", e)

                # Get repeatability settings
                is_repeatable = getattr(trigger, 'is_repeatable', True) if trigger else True
                max_per_day = getattr(trigger, 'max_triggers_per_day', None) if trigger else None

                # Get priority for priority-based selection (default 0 for backward compatibility)
                priority = getattr(trigger, 'priority', 0) if trigger else 0

                # Build passage name for dynamic rendering (stable node slug)
                canvas_prefix = self._sanitize_canvas_name(self._get_canvas_slug(canvas))
                _cv_nodes = self._get_canvas_nodes_ordered(canvas)
                first_node_passage = (
                    self._node_passage_name("Canvas", canvas_prefix, _cv_nodes[0])
                    if _cv_nodes else f"Canvas_{canvas_prefix}"
                )

                # Check if inherited
                inherited_from = canvas_info.get('inherited_from')
                display_name = canvas.name
                if inherited_from:
                    display_name = f"{canvas.name} (from {inherited_from})"

                # Get NPC slug from trigger metadata (for navigation indicators)
                npc_id = None
                if trigger and hasattr(trigger, 'metadata') and trigger.metadata:
                    npc_id = trigger.metadata.get("npc")

                # Get trigger_mode and chance from metadata (for random encounters)
                trigger_mode = "manual"
                trigger_chance = None
                if trigger and hasattr(trigger, 'metadata') and trigger.metadata:
                    trigger_mode = trigger.metadata.get("trigger_mode", "manual")
                    trigger_chance = trigger.metadata.get("chance")

                # Get costs from metadata (energy/resource gating)
                costs = []
                if trigger and hasattr(trigger, 'metadata') and trigger.metadata:
                    costs = trigger.metadata.get("costs", []) or []

                # E21 — opt-in cooldown visibility: when canvas filtered by
                # unmet conditions, render a grayed entry with a message.
                show_when_blocked = False
                cooldown_message = None
                if trigger and hasattr(trigger, 'metadata') and trigger.metadata:
                    show_when_blocked = bool(trigger.metadata.get("show_when_blocked", False))
                    cooldown_message = trigger.metadata.get("cooldown_message") or None

                # PRD 25 — substitution_only flag (excludes from selectors).
                substitution_only = False
                if trigger and hasattr(trigger, 'metadata') and trigger.metadata:
                    substitution_only = bool(trigger.metadata.get("substitution_only", False))

                # L2-2 — Lane 2 anti-toggle cooldown. Translate location slugs
                # → runtime passage names at build time so engine doesn't need
                # a slug→passage helper. Empty list = no gate (default behavior).
                entry_only_from_passages = []
                if trigger and hasattr(trigger, 'metadata') and trigger.metadata:
                    entry_only_from_slugs = trigger.metadata.get("entry_only_from", []) or []
                    for loc_slug in entry_only_from_slugs:
                        pname = slug_to_passage_name.get(loc_slug)
                        if pname:
                            entry_only_from_passages.append(pname)

                # Phase A (2026-05-14) — Lane 2/3 NPC presence gate. Carries
                # an NPC slug; runtime checks getNpcLocation(slug) against
                # current location. None = no presence gate.
                requires_npc = None
                if trigger and hasattr(trigger, 'metadata') and trigger.metadata:
                    requires_npc = trigger.metadata.get("requires_npc") or None

                location_canvas_list.append({
                    "id": str(canvas.id),
                    "name": canvas.name,  # For grouping tiers by activity name
                    "displayName": display_name,  # For link display
                    "passageName": first_node_passage,  # For link target
                    "canvasSlug": canvas_prefix,  # Explicit slug (was parsed from passageName; now node slugs make that ambiguous)
                    "priority": priority,  # For priority-based selection
                    "hasSchedules": canvas_info['has_schedules'],
                    "scheduleParams": schedule_params,
                    "conditions": conditions,
                    "isRepeatable": is_repeatable,
                    "maxPerDay": max_per_day,
                    "npcId": npc_id,  # NPC slug for navigation portrait indicators
                    "triggerMode": trigger_mode,  # "manual" or "random"
                    "chance": trigger_chance,  # Probability for random mode (0.0–1.0)
                    "costs": costs,  # Resource costs [{trait, value}] — checked/deducted on canvas entry
                    "showWhenBlocked": show_when_blocked,  # E21
                    "cooldownMessage": cooldown_message,    # E21
                    "substitutionOnly": substitution_only,  # PRD 25 — excludes from selectors
                    "entryOnlyFromPassages": entry_only_from_passages,  # L2-2 anti-toggle gate
                    "requiresNpc": requires_npc,  # Phase A — NPC presence gate
                })

                # Add to canvas-to-activity mapping for shared daily limits
                help_data["canvasIdToActivityName"][str(canvas.id)] = canvas.name

                # Map canvas_id → npc_uuid for trait decay interaction tracking
                if npc_id:
                    resolved_uuid = self.npc_slug_map.get(npc_id)
                    if resolved_uuid:
                        help_data["canvasIdToNpcUuid"][str(canvas.id)] = resolved_uuid

                # Extract conditional choices for unlock highlighting
                conditional_choices = []
                cc_idx = 0
                try:
                    for node in self._get_canvas_nodes_ordered(canvas):
                        eb = getattr(node, 'exit_block', None) or {}
                        if eb.get('type') != 'choices':
                            continue
                        for ch in eb.get('choices', []):
                            cond = ch.get('conditions')
                            if cond and isinstance(cond, dict) and cond.get('items'):
                                conditional_choices.append({
                                    "key": f"{canvas.id}:cc{cc_idx}",
                                    "conditions": cond,
                                })
                                cc_idx += 1
                except Exception:
                    pass
                if conditional_choices:
                    help_data["canvasConditionalChoices"][str(canvas.id)] = conditional_choices

            if location_canvas_list:
                help_data["locationCanvases"][str(location.id)] = location_canvas_list

        # NB (2026-05-06): An S3 walkthrough-counter discovery pass briefly
        # shipped here, walking stage_helpers to emit per-NPC counter badges
        # in the Quests panel. Removed same-day — duplicated the auto-rendered
        # goal block (Pattern 2, `setup.computeHintGoal`) which already shows
        # the active next-stage gate with progress for hints that opt in via
        # `auto_goal = true`. The counter row was either redundant (goal block
        # already there) or chaotic (merged conditions from multiple stage
        # helpers into one row, mixing Stage-1 + Stage-3 gates for the same
        # NPC). Decision: keep S4 (threshold notification on click), drop S3.
        # See git history for the implementation if ever needed.

        return json.dumps(help_data)

    def _format_schedule_human_readable(self, trigger) -> str:
        """Format trigger schedules as human-readable text like 'between 8 AM - 12 PM or 7 PM - 10 PM'."""
        if not self._trigger_has_schedules(trigger):
            return None

        schedules = self._trigger_schedules(trigger)
        if not schedules:
            return None

        def format_time(time_obj):
            """Convert time object to '8:30 AM' format; omit minutes when zero."""
            try:
                # Handle both time objects and string formats
                if hasattr(time_obj, 'hour'):
                    hour = time_obj.hour
                    minute = time_obj.minute
                else:
                    parts = str(time_obj).split(':')
                    hour = int(parts[0])
                    minute = int(parts[1]) if len(parts) > 1 else 0

                if hour == 0:
                    display_hour, ampm = 12, "AM"
                elif hour < 12:
                    display_hour, ampm = hour, "AM"
                elif hour == 12:
                    display_hour, ampm = 12, "PM"
                else:
                    display_hour, ampm = hour - 12, "PM"

                if minute == 0:
                    return f"{display_hour} {ampm}"
                return f"{display_hour}:{minute:02d} {ampm}"
            except (ValueError, IndexError, AttributeError) as e:
                logger.debug("Time format parse error for '%s': %s", time_obj, e)
                return str(time_obj)

        DAY_ABBREVS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        # Build time ranges and collect weekdays across all schedules
        time_ranges = []
        all_weekdays = set()
        for schedule in schedules:
            start = format_time(schedule.start_time)
            end = format_time(schedule.end_time) if schedule.end_time else None

            if end:
                time_ranges.append(f"{start} - {end}")
            else:
                time_ranges.append(f"at {start}")

            wds = schedule.weekdays or []
            all_weekdays.update(wds)

        if len(time_ranges) == 1:
            text = f"between {time_ranges[0]}"
        else:
            text = "between " + " or ".join(time_ranges)

        # Append weekday restriction if not every day
        if all_weekdays and len(all_weekdays) < 7:
            sorted_days = sorted(all_weekdays)
            day_names = ", ".join(DAY_ABBREVS[d] for d in sorted_days if 0 <= d <= 6)
            text += f" ({day_names})"

        return text

    def _extract_conditions_for_target_node(self, canvas, target_node_slug: str) -> dict:
        """Extract the conditions required to reach a specific node within a canvas.

        Looks through canvas node choices for a choice that targets the given node,
        and returns the conditions dict from that choice.
        """
        try:
            # Build slug-to-UUID map for this canvas's nodes
            node_uuid_by_slug = {}
            for node in self._get_canvas_nodes_ordered(canvas):
                slug = (node.node_data or {}).get("slug", "")
                if slug:
                    node_uuid_by_slug[slug] = str(node.id)

            target_uuid = node_uuid_by_slug.get(target_node_slug)
            if not target_uuid:
                return None

            # Search all nodes for a choice that targets this node
            for node in self._get_canvas_nodes_ordered(canvas):
                exit_block = node.exit_block or {}
                choices = exit_block.get("choices", [])
                for choice in choices:
                    if choice.get("targetType") == "node":
                        choice_node_id = choice.get("nodeId", "")
                        if choice_node_id == target_uuid:
                            conditions = choice.get("conditions")
                            if conditions and isinstance(conditions, dict) and conditions.get("items"):
                                return conditions
        except (KeyError, TypeError, AttributeError) as e:
            logger.warning(
                "Error extracting node conditions for '%s.%s': %s",
                canvas.name if canvas else "unknown", target_node_slug, e
            )
        return None

    def _extract_trait_effects_from_canvas(self, canvas) -> list:
        """Extract trait effects from canvas nodes for the modal feature.

        Returns list of dicts with: trait, value, npc_id (if targetType is 'npc')
        """
        effects = []
        try:
            for node in self._get_canvas_nodes_ordered(canvas):
                exit_block = node.exit_block or {}

                # Check effects in choices (for "choices" type exit blocks)
                choices = exit_block.get("choices", [])
                for choice in choices:
                    choice_effects = choice.get("effects", [])
                    for effect in choice_effects:
                        trait = effect.get("trait")
                        value = effect.get("value", 0)
                        if trait and value > 0:
                            effect_entry = {"trait": trait, "value": value}
                            # Include npcId if this is an NPC-targeted effect
                            if effect.get("targetType") == "npc" and effect.get("npcId"):
                                effect_entry["npc_id"] = effect.get("npcId")
                            effects.append(effect_entry)

                # Check effects in config (for "location" type exit blocks)
                config = exit_block.get("config", {})
                if config:
                    config_effects = config.get("effects", [])
                    for effect in config_effects:
                        trait = effect.get("trait")
                        value = effect.get("value", 0)
                        if trait and value > 0:
                            effect_entry = {"trait": trait, "value": value}
                            # Include npcId if this is an NPC-targeted effect
                            if effect.get("targetType") == "npc" and effect.get("npcId"):
                                effect_entry["npc_id"] = effect.get("npcId")
                            effects.append(effect_entry)
        except (KeyError, TypeError, AttributeError) as e:
            logger.warning(
                "Error extracting trait effects from canvas '%s': %s",
                canvas.name if canvas else "unknown", e
            )
        return effects

    def _extract_tiered_effects_from_canvas(self, canvas):
        """Extract per-tier effects with conditions from tiered activity canvas.

        Returns list of [{"effects": [...], "conditions": {...} or None}, ...]
        Returns None if canvas is not a tiered activity (no base node with choices).
        """
        tiers = []
        node_map = {}
        base_node = None

        try:
            for node in self._get_canvas_nodes_ordered(canvas):
                node_map[str(node.id)] = node
                eb = node.exit_block or {}
                if eb.get("type") == "choices":
                    choices = eb.get("choices", [])
                    if any(c.get("targetType") in ("trigger", "node") for c in choices):
                        base_node = node

            if not base_node:
                return None

            choices = (base_node.exit_block or {}).get("choices", [])
            for choice in choices:
                target_type = choice.get("targetType")
                conditions = choice.get("conditions")

                if target_type == "trigger":
                    raw_effects = choice.get("effects", [])
                    tiers.append({
                        "effects": [
                            {"trait": e["trait"], "value": e["value"],
                             **({"npc_id": e["npcId"]} if e.get("targetType") == "npc" and e.get("npcId") else {})}
                            for e in raw_effects if e.get("trait") and e.get("value", 0) > 0
                        ],
                        "conditions": None
                    })
                elif target_type == "node":
                    node_id = choice.get("nodeId", "")
                    target_node = node_map.get(node_id)
                    if target_node:
                        config = (target_node.exit_block or {}).get("config", {})
                        raw_effects = config.get("effects", [])
                        tiers.append({
                            "effects": [
                                {"trait": e["trait"], "value": e["value"],
                                 **({"npc_id": e["npcId"]} if e.get("targetType") == "npc" and e.get("npcId") else {})}
                                for e in raw_effects if e.get("trait") and e.get("value", 0) > 0
                            ],
                            "conditions": conditions
                        })
        except (KeyError, TypeError, AttributeError) as e:
            logger.warning(
                "Error extracting tiered effects from canvas '%s': %s",
                canvas.name if canvas else "unknown", e
            )
            return None

        return tiers if tiers else None

    def _build_flag_unlock_map(self, all_canvases, location_lookup, canvas_npc_map=None) -> dict:
        """Build a map of flag_key -> canvas info that sets this flag."""
        flag_unlock_map = {}
        canvas_npc_map = canvas_npc_map or {}

        for canvas in all_canvases:
            # Dev shortcuts never register as flag setters — they're invisible to
            # flag-chain validation (same skip as _build_flag_setter_canvases_index
            # and the requirer loops in validate_flag_chains). A dev jump that seeds
            # a real story flag must not shadow that flag's real located setter.
            if self._is_dev_shortcut_canvas(canvas):
                continue
            # Skip location/schedule extraction for starting canvas (it plays automatically)
            is_starting_canvas = (
                self.project.starting_canvas and
                str(canvas.id) == str(self.project.starting_canvas.id)
            )

            trigger = getattr(canvas, 'trigger', None)
            location_name = None
            schedule_text = None
            canvas_conditions = None

            if trigger and not is_starting_canvas:
                if trigger.location_id:
                    location_name = location_lookup.get(str(trigger.location_id))
                if self._trigger_has_schedules(trigger):
                    schedule_text = self._format_schedule_human_readable(trigger)
                cond = getattr(trigger, 'conditions', None)
                if cond and isinstance(cond, dict) and cond.get('items'):
                    canvas_conditions = cond

            # Extract flagEffects from all nodes
            try:
                for node in self._get_canvas_nodes_ordered(canvas):
                    exit_block = node.exit_block or {}

                    # Check flagEffects in choices (for "choices" type exit blocks)
                    choices = exit_block.get("choices", [])
                    for choice in choices:
                        flag_effects = choice.get("flagEffects", [])
                        for fe in flag_effects:
                            flag_key = fe.get("flag")
                            if flag_key and flag_key not in flag_unlock_map:
                                flag_unlock_map[flag_key] = {
                                    "canvas_name": canvas.name,
                                    "canvas_id": str(canvas.id),
                                    "location": location_name,
                                    "schedule": schedule_text,
                                    "canvas_conditions": canvas_conditions,
                                    "npc_name": canvas_npc_map.get(str(canvas.id)) or "player"
                                }

                        # Also check effects array in choices for flag property
                        choice_effects = choice.get("effects", [])
                        for eff in choice_effects:
                            flag_key = eff.get("flag")
                            if flag_key and flag_key not in flag_unlock_map:
                                flag_unlock_map[flag_key] = {
                                    "canvas_name": canvas.name,
                                    "canvas_id": str(canvas.id),
                                    "location": location_name,
                                    "schedule": schedule_text,
                                    "canvas_conditions": canvas_conditions,
                                    "npc_name": canvas_npc_map.get(str(canvas.id)) or "player"
                                }

                    # Check flagEffects in config (for "location" type exit blocks)
                    config = exit_block.get("config", {})
                    if config:
                        config_flag_effects = config.get("flagEffects", [])
                        for fe in config_flag_effects:
                            flag_key = fe.get("flag")
                            if flag_key and flag_key not in flag_unlock_map:
                                flag_unlock_map[flag_key] = {
                                    "canvas_name": canvas.name,
                                    "canvas_id": str(canvas.id),
                                    "location": location_name,
                                    "schedule": schedule_text,
                                    "canvas_conditions": canvas_conditions,
                                    "npc_name": canvas_npc_map.get(str(canvas.id)) or "player"
                                }

                        # Also check effects array in config for flag property
                        config_effects = config.get("effects", [])
                        for eff in config_effects:
                            flag_key = eff.get("flag")
                            if flag_key and flag_key not in flag_unlock_map:
                                flag_unlock_map[flag_key] = {
                                    "canvas_name": canvas.name,
                                    "canvas_id": str(canvas.id),
                                    "location": location_name,
                                    "schedule": schedule_text,
                                    "canvas_conditions": canvas_conditions,
                                    "npc_name": canvas_npc_map.get(str(canvas.id)) or "player"
                                }
            except (KeyError, TypeError, AttributeError) as e:
                logger.warning(
                    "Error building flag unlock map for canvas '%s': %s",
                    canvas.name if hasattr(canvas, 'name') else str(canvas.id), e
                )

        # Also scan phone conversations for flags set by replies
        phone_settings = (self.project.metadata or {}).get("phone_settings", {})
        if phone_settings.get("enabled"):
            npc_lookup_local = canvas_npc_map  # reuse existing npc lookup
            for conv in phone_settings.get("conversations", []):
                conv_npc = conv.get("npc", "")
                npc_display = None
                if conv_npc:
                    # Try to resolve NPC display name
                    for slug, name in canvas_npc_map.items():
                        pass  # canvas_npc_map is canvas_id → name, not slug → name
                    # Use npc slug directly — formatFlagHint resolves at runtime
                    npc_display = conv_npc.replace("npc_", "").replace("_", " ").title()
                for block in conv.get("blocks", []):
                    if block.get("type") != "reply":
                        continue
                    for choice in block.get("choices", []):
                        for fe in (choice.get("flagEffects") or []):
                            flag_key = fe.get("flag")
                            if flag_key and flag_key not in flag_unlock_map:
                                flag_unlock_map[flag_key] = {
                                    "canvas_name": conv.get("id", ""),
                                    "canvas_id": None,
                                    "location": None,
                                    "schedule": None,
                                    "canvas_conditions": None,
                                    "npc_name": npc_display or "player",
                                    "is_phone": True,
                                }

        # Also register flags the ENGINE sets (not any canvas): the rent
        # eviction_flag (set when the weekly payment is missed past grace) and any
        # [engine.daily_tick] flagEffects with op == "set". These are legitimately
        # set at runtime but have no canvas setter, so a trigger gated on them is
        # valid — register them here so the flag-chain validator doesn't raise a
        # false "NEVER SET". They are engine-global (no location/schedule binding),
        # so give a human schedule hint to satisfy the missing-hint check.
        # Read straight from project.metadata: in the validation path the generator
        # is constructed without a project and `self.project` is assigned afterward,
        # so the __init__-populated rent/daily_tick attributes are stale defaults.
        _engine_meta = (getattr(self, "project", None) and self.project.metadata) or {}
        _rent = _engine_meta.get("rent_settings", {}) or {}
        if _rent.get("enabled") and _rent.get("eviction_flag"):
            ef = _rent["eviction_flag"]
            if ef not in flag_unlock_map:
                flag_unlock_map[ef] = {
                    "canvas_name": "the weekly payment (rent system)",
                    "canvas_id": None,
                    "location": None,
                    "schedule": "when the payment is missed past grace",
                    "canvas_conditions": None,
                    "npc_name": _rent.get("collector_npc", "") or "player",
                    "is_engine": True,
                }
        for fe in ((_engine_meta.get("daily_tick", {}) or {}).get("flagEffects", []) or []):
            if fe.get("op") == "set":
                fk = fe.get("flag")
                if fk and fk not in flag_unlock_map:
                    flag_unlock_map[fk] = {
                        "canvas_name": "the daily cycle (engine.daily_tick)",
                        "canvas_id": None,
                        "location": None,
                        "schedule": "each new day",
                        "canvas_conditions": None,
                        "npc_name": "player",
                        "is_engine": True,
                    }

        return flag_unlock_map

    def validate_flag_chains(self) -> list:
        """
        Validate that all required flags have resolvable hints.
        Returns list of error dicts: {flag_key, canvas_name, issue}

        This is called by package_from_toml to catch flag chain issues
        before game generation.
        """
        from apps.stories.models import StoryCanvas
        from apps.npcs.models import NPC

        errors = []

        # Build the flag unlock map
        location_lookup = {str(loc.id): loc.name for loc in self.locations}
        all_canvases = self._all_canvases()

        # Build canvas_npc_map for NPC association validation
        canvas_npc_map = {}
        npc_lookup = {}

        for npc in self._all_npcs():
            npc_info = {"id": str(npc.id), "name": npc.name}
            name_slug = npc.name.lower().strip().replace(' ', '_') if npc.name else str(npc.id)
            npc_lookup[name_slug] = npc_info
            toml_slug = (npc.ai_behavior_config or {}).get("slug")
            if toml_slug:
                npc_lookup[toml_slug] = npc_info

        canvas_by_slug = {}
        canvas_by_name = {}
        for canvas in all_canvases:
            canvas_by_name[canvas.name] = canvas
            slug = canvas.metadata.get("slug") if canvas.metadata else None
            if slug:
                canvas_by_slug[slug] = canvas
            canvas_by_slug[str(canvas.id)] = canvas

        # From story_arc nodes
        metadata = getattr(self.project, 'metadata', None) or {}
        story_arc = metadata.get("story_arc", {})
        nodes = story_arc.get("nodes", [])
        for node in nodes:
            npc_slug = node.get("npc")
            if npc_slug:
                linked_canvas_id = node.get("linked_canvas")
                if linked_canvas_id:
                    canvas = canvas_by_slug.get(linked_canvas_id) or canvas_by_name.get(linked_canvas_id)
                    if canvas:
                        npc_info = npc_lookup.get(npc_slug, {})
                        canvas_npc_map[str(canvas.id)] = npc_info.get("name", npc_slug)

        # From canvas trait effects
        for canvas in all_canvases:
            cid = str(canvas.id)
            if cid not in canvas_npc_map:
                effects = self._extract_trait_effects_from_canvas(canvas)
                for eff in effects:
                    if eff.get("npc_id"):
                        npc_info = npc_lookup.get(eff["npc_id"], {})
                        canvas_npc_map[cid] = npc_info.get("name", eff["npc_id"])
                        break

        flag_unlock_map = self._build_flag_unlock_map(all_canvases, location_lookup, canvas_npc_map)

        # Get starting canvas ID to skip its flags (it plays automatically)
        starting_canvas_id = (
            str(self.project.starting_canvas.id)
            if self.project.starting_canvas else None
        )

        # Track which flags we've already reported to avoid duplicates
        reported_flags = set()

        # Find all flag requirements from canvas trigger conditions
        for canvas in all_canvases:
            # Dev-shortcut canvases are invisible to flag-chain validation: their
            # trigger's `dev_mode_enabled is_true` is a marker, not a real gate
            # (the flag is init-set only in --dev builds), so it has no located
            # setter and would false-positive as NEVER SET.
            if self._is_dev_shortcut_canvas(canvas):
                continue
            trigger = getattr(canvas, 'trigger', None)
            if not trigger:
                continue
            conditions = trigger.conditions or {}
            items = conditions.get("items", [])

            for item in items:
                # Only validate is_true flag conditions (actual dependencies).
                # is_false conditions are guards to prevent re-triggering, not prerequisites.
                if item.get("type") == "flag" and item.get("operator") == "is_true":
                    flag_key = item.get("flag_key")
                    if not flag_key or flag_key in reported_flags:
                        continue

                    # Check if flag has a setter
                    if flag_key not in flag_unlock_map:
                        errors.append({
                            "flag_key": flag_key,
                            "canvas_name": canvas.name,
                            "issue": "NEVER SET - no canvas sets this flag"
                        })
                        reported_flags.add(flag_key)
                    else:
                        # Check if setter has location/schedule hint
                        info = flag_unlock_map[flag_key]
                        # Skip flags set by starting canvas (plays automatically)
                        if starting_canvas_id and info.get("canvas_id") == starting_canvas_id:
                            continue
                        if not info.get("location") and not info.get("schedule"):
                            errors.append({
                                "flag_key": flag_key,
                                "canvas_name": canvas.name,
                                "issue": f"MISSING HINT - set by '{info['canvas_name']}' but no location/schedule"
                            })
                            reported_flags.add(flag_key)

        # 2b. Choice-level flag conditions (exit_block choices with conditions)
        for canvas in all_canvases:
            if self._is_dev_shortcut_canvas(canvas):
                continue
            for node in self._get_canvas_nodes_ordered(canvas):
                exit_block = node.exit_block or {}
                for choice in exit_block.get("choices", []):
                    conditions = choice.get("conditions", {})
                    for item in conditions.get("items", []):
                        if item.get("type") == "flag" and item.get("operator") == "is_true":
                            flag_key = item.get("flag_key")
                            if not flag_key or flag_key in reported_flags:
                                continue
                            if flag_key not in flag_unlock_map:
                                errors.append({
                                    "flag_key": flag_key,
                                    "canvas_name": canvas.name,
                                    "issue": f"NEVER SET - required by choice '{choice.get('text', '?')}' but no canvas sets this flag"
                                })
                                reported_flags.add(flag_key)
                            else:
                                info = flag_unlock_map[flag_key]
                                if starting_canvas_id and info.get("canvas_id") == starting_canvas_id:
                                    continue
                                if not info.get("location") and not info.get("schedule"):
                                    errors.append({
                                        "flag_key": flag_key,
                                        "canvas_name": canvas.name,
                                        "issue": f"MISSING HINT - required by choice '{choice.get('text', '?')}', set by '{info['canvas_name']}' but no location/schedule"
                                    })
                                    reported_flags.add(flag_key)

        # Detect circular flag dependencies
        def get_required_flags(canvas_obj):
            """Get flag requirements that are actual dependencies (is_true only).
            is_false conditions are guards to prevent re-triggering, not prerequisites.
            """
            trigger = getattr(canvas_obj, 'trigger', None)
            if not trigger:
                return []
            conditions = trigger.conditions or {}
            items = conditions.get("items", [])
            return [item.get("flag_key") for item in items
                    if item.get("type") == "flag"
                    and item.get("flag_key")
                    and item.get("operator") == "is_true"]

        # Map: flag_key -> canvas that sets it
        flag_to_setter_canvas = {}
        for canvas in all_canvases:
            for node in self._get_canvas_nodes_ordered(canvas):
                exit_block = node.exit_block or {}
                # Check config.effects
                config = exit_block.get("config", {})
                for eff in config.get("effects", []):
                    if eff.get("flag"):
                        flag_to_setter_canvas[eff["flag"]] = canvas
                # Check choices
                for choice in exit_block.get("choices", []):
                    for eff in choice.get("effects", []):
                        if eff.get("flag"):
                            flag_to_setter_canvas[eff["flag"]] = canvas

        # Detect cycles using DFS
        def detect_cycle(start_flag, visited_set, path):
            if start_flag in path:
                # Found cycle - return the cycle path
                cycle_start = path.index(start_flag)
                return path[cycle_start:] + [start_flag]
            if start_flag in visited_set:
                return None

            visited_set.add(start_flag)
            path.append(start_flag)

            # Get the canvas that sets this flag
            setter_canvas = flag_to_setter_canvas.get(start_flag)
            if setter_canvas:
                # Get flags required by the setter canvas
                required_flags = get_required_flags(setter_canvas)
                for req_flag in required_flags:
                    cycle = detect_cycle(req_flag, visited_set, path)
                    if cycle:
                        return cycle

            path.pop()
            return None

        # Check each flag for cycles
        all_flags = set(flag_unlock_map.keys())
        cycle_visited = set()
        for flag_key in all_flags:
            if flag_key not in cycle_visited:
                cycle = detect_cycle(flag_key, cycle_visited, [])
                if cycle:
                    cycle_str = " → ".join(cycle)
                    errors.append({
                        "flag_key": cycle[0],
                        "canvas_name": "(circular chain)",
                        "issue": f"CIRCULAR DEPENDENCY: {cycle_str}"
                    })
                    break  # Report one cycle at a time

        return errors

    def _sanitize_canvas_name(self, canvas_name):
        """Sanitize canvas name for use in Twee passage names."""
        return canvas_name.replace(' ', '_').replace('-', '_').replace("'", "").replace('"', '')

    def _node_passage_name(self, passage_prefix, canvas_prefix, node):
        """Twee passage name for a node — STABLE across releases.

        Uses the node SLUG (its TOML id, unique within the canvas), NOT its
        positional ordinal. So inserting/reordering/deleting a node in a shipped
        canvas no longer shifts other nodes' passage names → a returning player's
        save (which stores the passage name) still resolves to the same scene.
        """
        node_slug = self._sanitize_canvas_name(
            ((node.node_data or {}).get("slug") or "node")
        )
        return f"{passage_prefix}_{canvas_prefix}_Node_{node_slug}"

    def _location_passage_name(self, loc):
        """Twee passage name for a location — STABLE across releases.

        Uses the location SLUG, not its display name, so renaming a room no
        longer moves its passage → a save parked there still resolves.
        """
        return f"Location_{self._location_nav_slug(loc)}"

    def _location_passage_for_name(self, name_underscored):
        """Map a display-name-derived string (``loc.name.replace(' ','_')``) to the
        slug-based Location passage name, for the many link/goto sites that only
        have the name string in scope. Falls back to the old form if unknown."""
        cache = getattr(self, '_loc_passage_name_cache', None)
        if cache is None:
            cache = {
                loc.name.replace(' ', '_'): self._location_passage_name(loc)
                for loc in self.locations
            }
            self._loc_passage_name_cache = cache
        return cache.get(name_underscored, f"Location_{name_underscored}")

    def _slugify(self, name: str) -> str:
        """Convert a name to a URL-safe slug (lowercase, underscores)."""
        import re
        # Convert to lowercase, replace spaces/hyphens with underscores
        slug = name.lower().replace(' ', '_').replace('-', '_')
        # Remove any non-alphanumeric characters except underscores
        slug = re.sub(r'[^a-z0-9_]', '', slug)
        # Collapse multiple underscores
        slug = re.sub(r'_+', '_', slug)
        return slug.strip('_') or 'game'

    def _build_search_url(self, query: str, game_name: str, scene_path: str) -> str:
        """Build a Google search URL with media capture extension params."""
        from urllib.parse import urlencode
        params = {
            'q': query,
            '_tmc_game': game_name,
            '_tmc_scene': scene_path
        }
        return f"https://www.google.com/search?{urlencode(params)}"

    def _find_media_file(self, requested_path: str) -> tuple[str | None, str | None]:
        """
        Find a media file with extension-agnostic matching.

        Args:
            requested_path: Path from TOML (e.g., "scenes/intro.mp4")

        Returns:
            (actual_path, actual_extension) or (None, None) if not found

        Example:
            requested: "scenes/intro.mp4"
            available: "scenes/intro.webm"
            returns: ("scenes/intro.webm", ".webm")
        """
        # Normalize path
        normalized = requested_path.replace('\\', '/')

        # 1. Try exact match first (backward compatibility)
        if normalized in self.video_files:
            ext = Path(normalized).suffix.lower()
            return normalized, ext

        # 2. Extension-agnostic search
        # Get base path without extension: "scenes/intro.mp4" -> "scenes/intro"
        base_path = str(Path(normalized).with_suffix(''))

        # Try with original path, then strip "videos/" prefix if present.
        # TOML paths like "videos/activities/foo.mp4" won't match indexed keys
        # like "activities/foo.gif" because the video_folder root IS "videos/".
        candidates = [base_path]
        if base_path.startswith('videos/'):
            candidates.append(base_path[len('videos/'):])

        for candidate in candidates:
            for file_path in self.video_files.keys():
                file_base = str(Path(file_path).with_suffix(''))
                if file_base == candidate:
                    ext = Path(file_path).suffix.lower()
                    return file_path, ext

        return None, None

    def _is_video_extension(self, ext: str) -> bool:
        """Check if extension is a video format."""
        return ext.lower() in VIDEO_EXTENSIONS

    def _is_image_extension(self, ext: str) -> bool:
        """Check if extension is an image format (including GIF)."""
        return ext.lower() in IMAGE_EXTENSIONS

    # ── Media pools ───────────────────────────────────────────────────────────
    #
    # A pool is a media block that shows a DIFFERENT clip on each visit. It
    # CYCLES: visit 1 shows clip 1, visit 2 clip 2, wrapping back round.
    # Repeatable beats (activities, ambients, brothel loops) are what a player
    # sees most, and one fixed clip per beat goes stale fast.
    #
    # Cycle, NOT random. `either()`/`random()` over four clips repeats
    # back-to-back 25% of the time — exactly the staleness a pool exists to
    # remove. A cycle therefore has to remember where it got to, so the counter
    # lives in $game_state and not in a `_temp` that dies with the render.
    #
    # Two ways to declare one, both landing in `_render_media_pool`:
    #   pool_dir = "sex/oral_t5"        — a FOLDER; contents discovered from disk
    #   files    = ["a.webm", …]        — an explicit list (legacy)
    # `pool_dir` is preferred: the count is never hardcoded, so the human curates
    # by adding/removing files instead of editing TOML. Precedence and the shapes
    # live in `apps/common/media_blocks.py`.

    @staticmethod
    def _natural_key(path: str):
        """Sort key that orders `clip_2` before `clip_10`.

        Folder contents are ordered by name, and plain lexical sort puts `_10`
        before `_2` — which silently reorders a pool the moment it passes nine
        entries.
        """
        return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', path)]

    def _resolve_pool_dir(self, pool_dir: str) -> List[str]:
        """Every media file inside a pool folder, in natural-sort order.

        Reads the media index built by `_load_media_files` (an rglob of the media
        root, `:403-408`) rather than touching disk again — the folder's contents
        are already in `self.video_files`.

        Matching is prefix-on-a-path-boundary, so `sex/oral_t5` picks up
        `sex/oral_t5/1.webm` but never `sex/oral_t5_alt/1.webm`.
        """
        prefix = pool_dir.replace('\\', '/').strip().rstrip('/') + '/'
        found = [p for p in self.video_files if p.startswith(prefix)]
        return sorted(found, key=self._natural_key)

    def _media_pool_key(self, pool_files: List[str], pool_dir: Optional[str] = None) -> str:
        """Stable per-pool identity for the cycle counter.

        For a FOLDER pool the key is the folder — stable by design. That matters:
        the contents change every time the human selects or unselects a clip in
        the review UI, and keying on the contents would change the key, reset
        `$game_state.media_cycle`, and snap every player back to clip 1.

        For a legacy `files = [...]` pool there is no folder, so the key is
        derived from the declared list — a block dict is anonymous
        (`_convert_blocks_to_game_html` sees no id and no ordinal), and the TOML
        is the only stable thing to hash.

        Two nodes declaring the same pool share one counter either way. That is
        deliberate: the player gets variety across both rather than clip 1 at each.
        """
        if pool_dir:
            slug = re.sub(r'[^A-Za-z0-9_]', '_', pool_dir.strip().rstrip('/'))
            return slug[-48:] or 'pool'
        digest = hashlib.md5(",".join(pool_files).encode("utf-8")).hexdigest()[:8]
        stem = re.sub(r'[^A-Za-z0-9_]', '_', Path(pool_files[0]).stem)[:32]
        return f"{stem}_{digest}"

    def _pool_missing_placeholder(self, props: dict, label: str, kind: str) -> str:
        """The dashed-border '[… POOL MISSING]' block, debug builds only.

        Returns '' in a normal build — a player must never see build scaffolding.
        Shared by the image, video and folder-pool paths so the three cannot drift.
        """
        if not self.debug:
            return ''
        desc = props.get("description", "") or props.get("alt", "")
        out = (
            f'<div style="border:2px dashed #666;padding:20px;'
            f'margin:10px 0;border-radius:8px;background:#f5f5f5;">'
            f'<p style="margin:0;font-weight:bold;color:#333;">'
            f'[{kind.upper()} POOL MISSING] {html.escape(label)}</p>'
        )
        if desc:
            out += (
                f'<p style="margin:5px 0 0;color:#666;font-style:italic;">'
                f'{html.escape(desc)}</p>'
            )
        queries = props.get("search_queries", [])
        if queries and isinstance(queries, list):
            game_name = self.options.get("game_folder") or self._slugify(self.project.name)
            out += '<div style="margin-top:10px;">'
            for query in queries:
                if query and isinstance(query, str):
                    search_url = self._build_search_url(query.strip(), game_name, label)
                    out += (
                        f'<a href="{html.escape(search_url)}" target="_blank" '
                        f'style="display:inline-block;margin:4px 8px 4px 0;'
                        f'padding:6px 12px;background:#3b82f6;color:white;'
                        f'text-decoration:none;border-radius:4px;font-size:13px;">'
                        f'🔍 {html.escape(query.strip())}</a>'
                    )
            out += '</div>'
        return out + '</div>'

    def _render_media_pool(
        self, props: dict, pool_files: List[str], block_kind: str,
        pool_dir: Optional[str] = None,
    ) -> Optional[str]:
        """Resolve a media pool and emit the cycling SugarCube markup.

        Returns None when NOTHING resolved, so the caller emits its own "pool
        missing" placeholder. A partial pool cycles over the survivors only.

        `block_kind` ('image' | 'video') sets the missing-media label and the
        format rule: a VIDEO pool accepts any resolved media, because the video
        handler has always rendered a `.gif` through `<img>`; an IMAGE pool keeps
        its image-only rule but now WARNS instead of dropping the file in silence.
        """
        desc = props.get("description", "") or props.get("alt", "")
        entries: List[Tuple[str, bool]] = []   # (escaped src, is_video)

        if pool_dir and not pool_files:
            # An empty (or absent) pool folder. Record the FOLDER as the missing
            # thing — there are no declared filenames to report, and a pool that
            # silently vanished from the missing list is the exact regression
            # `apps/common/media_blocks.py` was written to stop.
            self.missing_media.append({
                'file': pool_dir,
                'type': block_kind,
                'description': desc,
                'search_queries': props.get("search_queries", []),
                'canvas_id': self.current_canvas_id or 'unknown',
                'category': self._categorize_media(self.current_canvas_id or '', pool_dir),
            })
            return None

        for pool_file in pool_files:
            normalized = str(pool_file).replace('\\', '/')
            actual_path, actual_ext = self._find_media_file(normalized)

            if actual_path is None:
                # One row PER missing entry — the missing-media page and
                # find-media must see the real shortfall, not just "a block".
                self.missing_media.append({
                    'file': normalized,
                    'type': block_kind,
                    'description': desc,
                    'search_queries': props.get("search_queries", []),
                    'canvas_id': self.current_canvas_id or 'unknown',
                    'category': self._categorize_media(self.current_canvas_id or '', normalized),
                })
                continue

            if block_kind == 'image' and not self._is_image_extension(actual_ext):
                # This used to `continue` in silence: the file was not rendered,
                # not recorded as missing, and not copied — it just vanished.
                logger.warning(
                    "Image pool entry '%s' resolved to non-image '%s' and was dropped. "
                    "Use a video block for clips.", normalized, actual_path
                )
                continue

            is_video = self._is_video_extension(actual_ext)
            if is_video:
                self.used_assets['external_videos'].add(actual_path)
            else:
                self.used_assets['external_images'].add(actual_path)

            if self.video_path:
                src = f"{self.video_path.rstrip('/')}/{html.escape(actual_path)}"
            else:
                src = f"media/{'videos' if is_video else 'images'}/{html.escape(actual_path)}"
            entries.append((src, is_video))

        if not entries:
            return None

        alt = html.escape(str(props.get("alt", "") or desc))
        poster = html.escape(str(props.get("poster", ""))) if props.get("poster") else ""

        def _tag(src: str, is_video: bool) -> str:
            # Chosen per ENTRY, not once for the pool: `_find_media_file` is
            # extension-agnostic, so a pool asking for .webm can legitimately
            # resolve to a .gif on disk, and <video src="x.gif"> renders nothing.
            # One shared `@src` attribute-directive cannot straddle both tags.
            if is_video:
                poster_attr = f' poster="{poster}"' if poster else ""
                return (
                    f'<video src="{src}" autoplay muted loop playsinline controls '
                    f'preload="metadata"{poster_attr} '
                    f'style="max-width:100%;max-height:70vh;object-fit:contain;'
                    f'height:auto;border-radius:8px;"></video>'
                )
            return (
                f'<img src="{src}" alt="{alt}" loading="lazy" decoding="async" '
                f'style="max-width:100%;max-height:70vh;object-fit:contain;'
                f'height:auto;border-radius:8px;" />'
            )

        if len(entries) == 1:
            # Nothing to cycle — don't burn a state key on it.
            return _tag(*entries[0])

        ref = f'$game_state.media_cycle["{self._media_pool_key(pool_files, pool_dir)}"]'
        max_idx = len(entries) - 1

        # Belt and braces. media_cycle is in the :: Start skeleton and
        # setup.backfillStateDefaults now heals a missing $game_state sub-map on
        # every passage, so a save written before the pool existed arrives here
        # already carrying the map. The guard stays because it costs one `ndef`
        # and it is the only thing standing between a save the backfill somehow
        # missed and a hard undefined on first render.
        parts = [
            '<<if ndef $game_state.media_cycle>><<set $game_state.media_cycle to {}>><</if>>',
            f'<<set {ref} to ({ref} === undefined ? 0 : ({ref} + 1) % {len(entries)})>>',
            f'<<set _mc to {ref}>>',
        ]
        for idx, (src, is_video) in enumerate(entries):
            if idx == 0:
                parts.append('<<if _mc is 0>>')
            elif idx < max_idx:
                parts.append(f'<<elseif _mc is {idx}>>')
            else:
                parts.append('<<else>>')
            parts.append(_tag(src, is_video))
        parts.append('<</if>>')
        return ''.join(parts)

    def _categorize_media(self, canvas_id: str, file_path: str) -> str:
        """Categorize a media file by section for the missing media page."""
        file_lower = file_path.lower()
        canvas_lower = canvas_id.lower() if canvas_id else ''

        if file_lower.startswith('endings/') or 'ending_' in file_lower:
            return 'Endings'
        elif file_lower.startswith('solo/') or 'solo_' in canvas_lower:
            return 'Solo Activities'
        elif file_lower.startswith('activities/'):
            return 'Activities'
        elif file_lower.startswith('scenes/') or canvas_lower.startswith('scene_'):
            return 'Story Scenes'
        elif file_lower.startswith('images/'):
            return 'Images'
        elif file_lower.startswith('social/'):
            return 'Social Media'
        else:
            return 'Other'

    def _get_canvas_slug(self, canvas) -> str:
        """Get canvas slug from metadata, raising error if missing.

        All canvases must have a unique slug for proper passage name generation.
        This prevents name collisions between canvases with the same display name.
        """
        slug = None
        if canvas.metadata:
            slug = canvas.metadata.get("slug")

        if not slug:
            raise ValueError(
                f"Canvas '{canvas.name}' (id: {canvas.id}) is missing required 'slug' in metadata. "
                f"Ensure all canvases are imported from TOML with proper IDs."
            )
        return slug

    def _format_schedule_for_sugarcube(self, schedules):
        """Convert TriggerSchedules to SugarCube setup function call parameters (array format)."""
        if not schedules:
            return ""

        # Build array of schedule objects for isScheduleActive (supports OR logic)
        schedule_items = []
        for schedule in schedules:
            weekdays = f"[{','.join(map(str, schedule.weekdays))}]"
            start_time = f'"{schedule.start_time.strftime("%H:%M")}"'
            end_time = f'"{schedule.end_time.strftime("%H:%M")}"' if schedule.end_time else "null"
            schedule_items.append(f'{{weekdays:{weekdays},startTime:{start_time},endTime:{end_time}}}')

        return f'([{",".join(schedule_items)}])'

    # ========== NODE CHAIN HELPER METHODS ==========

    def _get_canvas_nodes_ordered(self, canvas):
        """Get canvas nodes ordered by creation time (insertion order).

        No-DB path: canvas._nodes is a plain list already in insertion order,
        which is exactly what order_by('created_at') yields for the DB path
        (nodes are minted in template order; StoryNode has no Meta.ordering).
        """
        if self.graph is not None:
            return canvas._nodes
        return canvas.nodes.all().order_by('created_at')

    def _trigger_schedules(self, trigger):
        """Reverse-manager stand-in: trigger.schedules as a plain list."""
        if trigger is None:
            return []
        if self.graph is not None:
            return getattr(trigger, '_schedules', [])
        return list(trigger.schedules.all())

    def _trigger_has_schedules(self, trigger):
        """Reverse-manager stand-in: trigger.schedules.exists()."""
        if trigger is None:
            return False
        if self.graph is not None:
            return bool(getattr(trigger, '_schedules', []))
        return hasattr(trigger, 'schedules') and trigger.schedules.exists()

    def _locations_entered_from(self, location):
        """Reverse-filter stand-in: Location.objects.filter(entry_from=location)."""
        if self.graph is not None:
            return self.graph.children_by_entry_from.get(str(location.id), [])
        from apps.world.models import Location
        return list(Location.objects.filter(entry_from=location))

    def _all_npcs(self):
        """Project NPCs — graph list in no-DB mode, else the ORM queryset."""
        if self.graph is not None:
            return self.graph.npcs
        from apps.npcs.models import NPC
        return NPC.objects.filter(project=self.project, deleted_at__isnull=True)

    def _all_canvases(self):
        """All project canvases (graph order = reverse insertion, mirroring the
        ORM Meta.ordering) in no-DB mode, else the ORM queryset."""
        if self.graph is not None:
            return sorted(self.graph.canvases, key=lambda c: c._seq, reverse=True)
        from apps.stories.models import StoryCanvas
        return StoryCanvas.objects.filter(
            project=self.project, deleted_at__isnull=True
        )

    def _node_by_id(self, node_id):
        """Resolve a node id to its StoryNode — graph index in no-DB mode."""
        if self.graph is not None:
            return self.graph.node_by_id.get(node_id)
        from apps.stories.models import StoryNode
        return StoryNode.objects.filter(id=node_id).only('canvas_id').first()

    def _ordered_navigation(self, location):
        """Ordered nav destinations for a location.

        No-DB twin of Location.get_ordered_navigation (apps/world/models.py),
        which internally queries Location.objects.filter(entry_from=self)
        .exclude(parent_location=self). Reproduces the same set + ordering from
        the in-memory graph. children_by_entry_from is in created_at order
        (Location.Meta.ordering), matching the ORM.
        """
        if self.graph is None:
            return location.get_ordered_navigation()

        loc_id = str(location.id)
        destinations = [
            d for d in self.graph.children_by_entry_from.get(loc_id, [])
            if not (d.parent_location is not None and str(d.parent_location.id) == loc_id)
        ]
        nav_order = location.navigation_order
        if nav_order and len(nav_order) > 0:
            dest_by_id = {str(loc.id): loc for loc in destinations}
            ordered = []
            for oid in nav_order:
                if str(oid) in dest_by_id:
                    ordered.append(dest_by_id[str(oid)])
                    del dest_by_id[str(oid)]
            ordered.extend(dest_by_id.values())
            return ordered
        direct = [d for d in destinations if not d.is_container]
        containers = [d for d in destinations if d.is_container]
        direct.sort(key=lambda x: x.name.lower())
        containers.sort(key=lambda x: x.name.lower())
        return direct + containers

    def _build_node_chain(self, nodes):
        """Build linear node chain following connections."""
        if not nodes:
            return []

        # Create a map of nodes by ID for quick lookup
        node_map = {str(node.id): node for node in nodes}

        # Find starting node (node with no incoming connections or first by creation)
        starting_node = None
        nodes_with_incoming = set()

        # Check all connections to find nodes with incoming connections
        for node in nodes:
            for connection in node.outgoing_connections.all():
                nodes_with_incoming.add(str(connection.target_node_id))

        # Find node without incoming connections
        for node in nodes:
            if str(node.id) not in nodes_with_incoming:
                starting_node = node
                break

        # If no clear starting node, use first by creation time
        if not starting_node:
            starting_node = nodes[0]

        # Build chain by following outgoing connections
        chain = []
        current_node = starting_node
        visited = set()

        while current_node and str(current_node.id) not in visited:
            chain.append(current_node)
            visited.add(str(current_node.id))

            # Find next node via outgoing connection
            next_node = None
            outgoing_connections = current_node.outgoing_connections.all()
            if outgoing_connections:
                # Take first outgoing connection for linear flow
                connection = outgoing_connections[0]
                next_node_id = str(connection.target_node_id)
                next_node = node_map.get(next_node_id)

            current_node = next_node

        return chain

    def _extract_node_content(self, node):
        """Extract displayable content from node data - BlockNote format only."""
        try:
            # Process BlockNote content from node_data
            if hasattr(node, 'node_data') and node.node_data:
                node_data = node.node_data

                # Check for BlockNote blocks format
                if isinstance(node_data, dict) and 'blocks' in node_data:
                    blocks = node_data.get('blocks', [])
                    if blocks and isinstance(blocks, list):
                        return self._convert_blocks_to_game_html(blocks)

                # Log warning for non-block format
                logger.warning(f"Node {node.id} has node_data but no blocks", extra={
                    "node_id": str(node.id),
                    "node_name": node.name,
                    "node_data_keys": list(node_data.keys()) if isinstance(node_data, dict) else "not_dict"
                })

            # No valid content found - fail fast
            logger.error(f"Node {node.id} has no valid BlockNote content", extra={
                "node_id": str(node.id),
                "node_name": node.name,
                "has_node_data": hasattr(node, 'node_data'),
                "node_data_type": type(node.node_data) if hasattr(node, 'node_data') else None
            })
            return f"<p><strong>{node.name}</strong></p><p><em>No content available</em></p>"

        except (KeyError, TypeError, AttributeError) as e:
            logger.error(f"Error extracting content from node {node.id}: {e}", extra={
                "node_id": str(node.id),
                "node_name": node.name,
                "error": str(e)
            })
            raise ValueError(
                f"Failed to extract content from node '{node.name}' ({node.id}): {e}"
            ) from e

    def _get_return_location(self, canvas, default_target="Navigation"):
        """Determine where to return after canvas completion."""
        try:
            if hasattr(canvas, 'trigger') and canvas.trigger and canvas.trigger.location_id:
                location = self._get_location_by_id(canvas.trigger.location_id)
                if location:
                    return self._location_passage_name(location)
        except (AttributeError, TypeError) as e:
            logger.warning("Error determining return location for canvas: %s", e)

        return default_target

    def _get_loop_config(self, canvas):
        """Get loop config from canvas metadata. Returns dict or None."""
        loop = canvas.metadata.get("loop") if canvas.metadata else None
        if not loop or not loop.get("enabled"):
            return None
        return {
            "max_revisits": loop.get("max_revisits", 2),
            "loop_back_text": loop.get("loop_back_text", "Stay a while"),
        }

    def _is_node_loop_terminal(self, node):
        """Check if node's exit_block has loop_terminal flag."""
        eb = getattr(node, 'exit_block', None) or {}
        return eb.get("loop_terminal", False)

    def _generate_canvas_node_passages(self, canvas, passage_prefix="Canvas") -> str:
        """Generate Twee passages for every node in a canvas (per-node emission)."""
        # Track current canvas for missing media categorization
        self.current_canvas_id = str(canvas.id) if canvas else None
        nodes = self._get_canvas_nodes_ordered(canvas)
        if not nodes:
            # No nodes - return fallback content
            canvas_passage_name = self._sanitize_canvas_name(self._get_canvas_slug(canvas))
            return_target = self._get_return_location(canvas)
            return f""":: {passage_prefix}_{canvas_passage_name}
<p><em>This story canvas has no content yet.</em></p>

<<set $game_state.current_canvas = "{canvas.id}">>

[[Continue->{return_target}]]

"""

        content = ""
        return_target = self._get_return_location(canvas)
        canvas_prefix = self._sanitize_canvas_name(self._get_canvas_slug(canvas))

        # Get costs for this canvas (for cost gate on Node 1)
        canvas_costs = []
        if hasattr(canvas, 'trigger') and canvas.trigger:
            if hasattr(canvas.trigger, 'metadata') and canvas.trigger.metadata:
                canvas_costs = canvas.trigger.metadata.get("costs", []) or []

        # Counter for conditional choice keys (must match _build_help_data order)
        cc_counter = 0

        # Loop config for this canvas (if any)
        loop_config = self._get_loop_config(canvas)
        base_passage_name = self._node_passage_name(passage_prefix, canvas_prefix, nodes[0]) if (loop_config and nodes) else None

        # Build node map for loop_terminal checks (keyed by UUID string)
        canvas_node_map = {str(n.id): n for n in nodes} if loop_config else {}

        # Map of node.id -> passage name is already built; use it for links
        for i, node in enumerate(nodes):
            node_passage_name = self._node_passage_name(passage_prefix, canvas_prefix, node)
            node_content = self._extract_node_content(node)

            # Dev mode: show canvas/node info at top of passage
            dev_canvas_info = ""
            if self.dev_mode:
                node_display_name = node.name or f"Node {i+1}"
                dev_canvas_info = (
                    f'<div class="dev-canvas-info">'
                    f'<strong>Canvas:</strong> {canvas.name} '
                    f'<span style="opacity:0.7;">({canvas_prefix})</span> | '
                    f'<strong>Node:</strong> {node_display_name}'
                    f'</div>\n'
                )

            mark_trigger = ""
            if passage_prefix in ("Canvas", "StartingCanvas") and i == 0:
                mark_trigger = f"<<script>>setup.markCanvasTriggered(\"{canvas.id}\");<</script>>\n"

            # PRD 25 — Lane 3 dispatcher substitution injection. Fires BEFORE
            # any visible content renders. Only emitted for Node 1 of canvases
            # with non-empty substitution rules. Zero overhead for canvases
            # without substitutions (no injection at all).
            #
            # Pattern: <<set>> the helper's return value (target passage name OR
            # null) into a temp var, then <<if>>+<<goto>> on it. This works
            # around SugarCube's <<script>> macro disallowing naked `return`
            # statements. <<goto>> immediately switches passages and discards
            # the rest of the parent's body — exactly the no-flicker behavior
            # PRD 25 §3 specifies.
            substitution_check = ""
            # Doc 69 Item 2 — pre-substitution effects: emit BEFORE the
            # substitution check so they execute unconditionally. If a
            # substitution rule fires via <<goto>>, these effects have already
            # run — the activity "counts" even when interrupted. See Doc 69 §4.
            pre_substitution_macros = ""
            if i == 0 and hasattr(canvas, 'trigger') and canvas.trigger:
                if hasattr(canvas.trigger, 'metadata') and canvas.trigger.metadata:
                    if canvas.trigger.metadata.get("substitutions"):
                        substitution_check = (
                            f"<<set _sub_target = setup.checkAndSubstituteCanvas(\"{canvas.id}\")>>"
                            f"<<if _sub_target>><<goto _sub_target>><</if>>\n"
                        )
                    pre_effects = canvas.trigger.metadata.get("pre_substitution_effects") or []
                    if pre_effects:
                        macro_lines = []
                        for _pe in pre_effects:
                            if not isinstance(_pe, dict):
                                continue
                            _pe_tt = str(_pe.get("targetType", "player"))
                            _pe_npc = _pe.get("npcId")
                            _pe_npc_js = f'"{_pe_npc}"' if _pe_npc else "null"
                            _pe_trait = str(_pe.get("trait", ""))
                            _pe_op = str(_pe.get("op", "add"))
                            _pe_val_js = self._resolve_effect_value(_pe.get("value", 0))
                            _pe_clamp = "true" if _pe.get("clamp") else "false"
                            _pe_cap = _pe.get("cap")
                            _pe_cap_js = (
                                json.dumps(_pe_cap)
                                if _pe_cap is not None else "null"
                            )
                            macro_lines.append(
                                f'<<script>>setup.applyAndNotifyTrait('
                                f'"{_pe_tt}", {_pe_npc_js}, "{_pe_trait}", '
                                f'"{_pe_op}", {_pe_val_js}, {_pe_clamp}, '
                                f'{_pe_cap_js});<</script>>'
                            )
                        if macro_lines:
                            pre_substitution_macros = "\n".join(macro_lines) + "\n"

            # Track node visit in visited_nodes for story arc completion
            node_slug = ""
            if hasattr(node, 'node_data') and node.node_data:
                node_slug = node.node_data.get("slug", "")
            canvas_slug = self._get_canvas_slug(canvas)
            track_visited_node = ""
            if node_slug and canvas_slug:
                visit_key = f"{canvas_slug}.{node_slug}"
                track_visited_node = (
                    f'<<script>>'
                    f'var vn = State.variables.game_state.visited_nodes;'
                    f'if (vn.indexOf("{visit_key}") === -1) {{ vn.push("{visit_key}"); }}'
                    f'<</script>>\n'
                )

            passage_header = (
                f":: {node_passage_name}\n"
                f"{pre_substitution_macros}"  # Doc 69 Item 2 — unconditional effects, BEFORE substitution check
                f"{substitution_check}"  # PRD 25 — fires before body / exit_block; Doc 69 Item 2 moves pre-sub effects earlier still
                f"{dev_canvas_info}"
                f"{node_content}\n\n"
                f"<<set $game_state.current_canvas = \"{canvas.id}\">>\n"
                f"<<set $game_state.current_node = \"{node.id}\">>\n"
                f"{mark_trigger}"
                f"{track_visited_node}"
            )

            exit_block = getattr(node, 'exit_block', None) or {}
            exit_type = exit_block.get('type', 'location')

            # ── Loop: determine role of each choice for this node ──
            # loop_choice_roles maps choice index -> {'role': 'non_terminal'|'terminal'|'exit', 'node_slug': str}
            loop_choice_roles = {}
            is_loop_base = loop_config and i == 0
            is_loop_sub = loop_config and i > 0
            is_loop_terminal_node = loop_config and self._is_node_loop_terminal(node)

            if loop_config and exit_type == 'choices':
                raw_choices = exit_block.get('choices', [])
                for ci, raw_ch in enumerate(raw_choices):
                    raw_target_type = raw_ch.get('targetType', 'trigger')
                    raw_node_id = raw_ch.get('nodeId')
                    if raw_target_type == 'trigger' or raw_target_type == 'location':
                        loop_choice_roles[ci] = {'role': 'exit'}
                    elif raw_target_type == 'node' and raw_node_id:
                        # Check if target node is loop_terminal
                        target_node_obj = canvas_node_map.get(str(raw_node_id))
                        if target_node_obj and self._is_node_loop_terminal(target_node_obj):
                            loop_choice_roles[ci] = {'role': 'terminal', 'node_slug': str(raw_node_id)}
                        else:
                            # Derive a readable slug for the visited tracking
                            node_slug = raw_ch.get('nodeId', '').split('.')[-1] if '.' in raw_ch.get('nodeId', '') else str(raw_node_id)
                            loop_choice_roles[ci] = {'role': 'non_terminal', 'node_slug': node_slug}

            if exit_type == 'choices':
                # Process choices and render multiple links
                exit_result = self._process_exit_block(node, return_target)
                passage_body = "\n"

                # ── Loop: add loop state init for base node ──
                if is_loop_base:
                    passage_body += '<<if ndef $game_state.loop_count>><<set $game_state.loop_count to 0>><<set $game_state.loop_visited to []>><</if>>\n'

                passage_body += "<<nobr>>\n"
                if isinstance(exit_result, list):
                    # Track if any unconditional choices exist and build runtime OR of conditional choices
                    conditional_expr_parts = []
                    has_unconditional_choice = False
                    for choice_idx, choice_tuple in enumerate(exit_result):
                        # Unpack: (target, text, time, traitEffects, flagEffects, conditions, wardrobeEffects, show_when_locked, locked_text, rejection_passage, rejection_effects)
                        target_passage = choice_tuple[0]
                        choice_text = choice_tuple[1]
                        time_minutes = choice_tuple[2]
                        trait_effects = choice_tuple[3] if len(choice_tuple) > 3 else []
                        flag_effects = choice_tuple[4] if len(choice_tuple) > 4 else []
                        choice_conditions = choice_tuple[5] if len(choice_tuple) > 5 else None
                        wardrobe_effects = choice_tuple[6] if len(choice_tuple) > 6 else []
                        show_when_locked = choice_tuple[7] if len(choice_tuple) > 7 else False
                        locked_text = choice_tuple[8] if len(choice_tuple) > 8 else ''
                        rejection_passage = choice_tuple[9] if len(choice_tuple) > 9 else None
                        rejection_effects = choice_tuple[10] if len(choice_tuple) > 10 else []
                        modifier_effects_list = choice_tuple[11] if len(choice_tuple) > 11 else []
                        pass_effects_list = choice_tuple[12] if len(choice_tuple) > 12 else []
                        item_effects_list = choice_tuple[13] if len(choice_tuple) > 13 else []
                        text_variants_list = choice_tuple[14] if len(choice_tuple) > 14 else []
                        # S4 — author-supplied threshold-publisher message for
                        # locked Mode A choices. Falls back to '' (no toast).
                        locked_text_threshold = choice_tuple[15] if len(choice_tuple) > 15 else ''
                        quest_effects_list = choice_tuple[16] if len(choice_tuple) > 16 else []
                        schedule_effects_list = choice_tuple[17] if len(choice_tuple) > 17 else []
                        choice_costs_list = choice_tuple[18] if len(choice_tuple) > 18 else []

                        # ── Loop: get role for this choice ──
                        choice_role = loop_choice_roles.get(choice_idx, {})
                        role = choice_role.get('role') if choice_role else None
                        choice_node_slug = choice_role.get('node_slug', '') if choice_role else ''

                        # ── Loop: open visited check for non-terminal choices on base node ──
                        if is_loop_base and role == 'non_terminal' and choice_node_slug:
                            passage_body += f'<<if not $game_state.loop_visited.includes("{choice_node_slug}")>>\n'

                        # Open gate(s): main-lock `conditions` (OUTER) then per-choice
                        # `costs` affordability (INNER). The unlocked-choice span lives
                        # only in the affordable branch so the cost-blocked rung renders
                        # as a plain greyed span (not inside the highlight wrapper).
                        choice_key = None
                        cond_expr = None
                        # Normalize per-choice costs → JSON once (None = no cost gate).
                        choice_costs_js = None
                        if choice_costs_list:
                            try:
                                _norm_costs = [
                                    {"trait": str(cc["trait"]), "value": int(cc["value"])}
                                    for cc in choice_costs_list
                                    if isinstance(cc, dict) and "trait" in cc and "value" in cc
                                ]
                                if _norm_costs:
                                    choice_costs_js = json.dumps(_norm_costs)
                            except (KeyError, TypeError, ValueError) as e:
                                logger.warning("Invalid costs for choice '%s': %s", choice_text, e)
                                choice_costs_js = None
                        # Outer: main-lock conditions
                        if choice_conditions:
                            try:
                                conditions_js = json.dumps(choice_conditions)
                                passage_body += f"<<if setup.triggerConditionsSatisfied({conditions_js})>>\n"
                                cond_expr = f"setup.triggerConditionsSatisfied({conditions_js})"
                                # Generate choice key for unlock highlighting
                                choice_key = f"{canvas.id}:cc{cc_counter}"
                                cc_counter += 1
                            except (TypeError, ValueError) as e:
                                logger.warning(
                                    "Error serializing choice conditions for '%s': %s. Treating as unconditional.",
                                    choice_text, e
                                )
                        # Inner: per-choice cost affordability (wraps link + highlight span)
                        if choice_costs_js:
                            passage_body += f"<<if setup.checkCostsAffordable({choice_costs_js})>>\n"
                        # Highlight wrapper for newly unlocked conditional choices.
                        # Uses @class dynamic attribute to avoid SugarCube HTML parsing
                        # errors (conditional <span> open/close in separate <<if>> blocks
                        # causes "cannot find closing tag").
                        if choice_key:
                            passage_body += f'<span @class="setup.isChoiceVisited(\'{choice_key}\') ? \'\' : \'unlocked-choice\'">\n'
                        # No-exits fallback: a choice is "available" only if BOTH its
                        # main-lock AND its cost are satisfied. Register the combined
                        # expression; a choice with neither gate is truly unconditional.
                        _sat_parts = [p for p in (
                            cond_expr,
                            (f"setup.checkCostsAffordable({choice_costs_js})" if choice_costs_js else None),
                        ) if p]
                        if _sat_parts:
                            conditional_expr_parts.append("(" + " and ".join(_sat_parts) + ")")
                        else:
                            has_unconditional_choice = True

                        # Resolve @npc references in choice text
                        # <<print>> macros don't work inside <<link "...">> quoted strings,
                        # so we use backtick expression syntax for dynamic text:
                        #   <<link `"Chat with " + $npcs["uuid"].name` "Target">>
                        if text_variants_list:
                            # E6: Pre-resolve label via SugarCube <<set _cv>> chain.
                            # Variant texts are static strings; @npc references inside
                            # variants are NOT supported in v1 (the base text path also
                            # gets a static treatment when variants are present — keeps
                            # the variable-label form simple).
                            escaped_base = choice_text.replace('"', '\\"').replace('[', '&#91;').replace(']', '&#93;')
                            passage_body += f'<<set _cv to "{escaped_base}">>\n'
                            for vi, variant in enumerate(text_variants_list):
                                v_text = (variant.get('text') or '')
                                v_text_esc = v_text.replace('"', '\\"').replace('[', '&#91;').replace(']', '&#93;')
                                v_conds = json.dumps(variant.get('conditions') or {})
                                keyword = '<<if' if vi == 0 else '<<elseif'
                                passage_body += f'{keyword} setup.triggerConditionsSatisfied({v_conds})>><<set _cv to "{v_text_esc}">>\n'
                            passage_body += '<</if>>\n'
                            passage_body += f'<<link _cv "{target_passage}">>'
                        else:
                            resolved_expr, is_dynamic = self._resolve_at_references_expr(choice_text)
                            if is_dynamic:
                                # Backtick expression — no bracket escaping needed (it's JS)
                                passage_body += f'<<link `{resolved_expr}` "{target_passage}">>'
                            else:
                                # Static text — escape as before
                                escaped_choice_text = choice_text.replace('"', '\\"').replace('[', '&#91;').replace(']', '&#93;')
                                passage_body += f'<<link "{escaped_choice_text}" "{target_passage}">>'
                        # Clear pending effects at start
                        # Per-choice costs deduct here too (the spend), so they count
                        # toward has_effects (clear+flush pendingEffects) even if the
                        # choice carries no other effects.
                        has_effects = (trait_effects and isinstance(trait_effects, list)) or (flag_effects and isinstance(flag_effects, list)) or (self.clothing_enabled and wardrobe_effects and isinstance(wardrobe_effects, list)) or bool(choice_costs_js)
                        if has_effects:
                            passage_body += "<<script>>setup.pendingEffects = [];<</script>>"
                        # Emit trait + flag + wardrobe effects via shared inline helpers
                        # (consolidated 2026-05-06 alongside S7 cascade work — same semantics).
                        ctx = f"choice '{choice_text}'"
                        passage_body += self._emit_trait_effects_inline(trait_effects, ctx)
                        passage_body += self._emit_flag_effects_inline(flag_effects, ctx)
                        passage_body += self._emit_wardrobe_effects_inline(wardrobe_effects, ctx)
                        # Deduct per-choice costs (the resource spend) — negative
                        # applyAndNotifyTrait per cost, mirroring canvas-level deductCosts.
                        if choice_costs_js:
                            for _cc in _norm_costs:
                                _ct = str(_cc["trait"]).replace('"', '\\"')
                                passage_body += f'<<script>>setup.applyAndNotifyTrait("player", null, "{_ct}", "add", {-int(_cc["value"])}, false, null);<</script>>'
                        # Emit modifier effects (apply temporary modifiers)
                        if modifier_effects_list and isinstance(modifier_effects_list, list):
                            for me in modifier_effects_list:
                                try:
                                    me_key = str(me.get('key', '')).replace('"', '\\"')
                                    me_name = str(me.get('name', '')).replace('"', '\\"')
                                    me_dur = int(me.get('duration_hours', 1))
                                    me_offsets = json.dumps(me.get('trait_offsets', {}))
                                    passage_body += f'<<script>>setup.applyModifier("{me_key}", "{me_name}", {me_dur}, {me_offsets});<</script>>'
                                except (KeyError, TypeError, ValueError) as e:
                                    logger.warning("Invalid modifier effect in choice '%s': %s", choice_text, e)
                        # Pass effects (recurring pass purchases)
                        if pass_effects_list and isinstance(pass_effects_list, list):
                            for pe in pass_effects_list:
                                try:
                                    pe_id = str(pe.get('pass_id', '')).replace('"', '\\"')
                                    if pe_id:
                                        passage_body += f'<<script>>setup.purchasePass("{pe_id}");<</script>>'
                                except (KeyError, TypeError, ValueError) as e:
                                    logger.warning("Invalid pass effect in choice '%s': %s", choice_text, e)
                        # Item effects (inventory add/remove)
                        if item_effects_list and isinstance(item_effects_list, list):
                            for ie in item_effects_list:
                                try:
                                    ie_id = str(ie.get('item_id', '')).replace('"', '\\"')
                                    ie_action = str(ie.get('action', 'add'))
                                    ie_qty = int(ie.get('quantity', 1))
                                    if ie_id:
                                        if ie_action == 'remove':
                                            passage_body += f'<<script>>setup.removeItem("{ie_id}", {ie_qty});<</script>>'
                                        else:
                                            passage_body += f'<<script>>setup.addItem("{ie_id}", {ie_qty});<</script>>'
                                except (KeyError, TypeError, ValueError) as e:
                                    logger.warning("Invalid item effect in choice '%s': %s", choice_text, e)
                        # doc 45 G4 — quest effects on canvas choices
                        if quest_effects_list and isinstance(quest_effects_list, list):
                            for qe in quest_effects_list:
                                try:
                                    q_id = str(qe.get('quest', '')).replace('"', '\\"')
                                    q_op = str(qe.get('op', 'start'))
                                    q_step = qe.get('step')
                                    q_step_js = 'null' if q_step is None else str(int(q_step))
                                    if q_id:
                                        passage_body += f'<<script>>setup.applyQuestEffect("{q_id}", "{q_op}", {q_step_js});<</script>>'
                                except (KeyError, TypeError, ValueError) as e:
                                    logger.warning("Invalid quest effect in choice '%s': %s", choice_text, e)
                        # doc 45 G5 — scheduled (delayed) effects on canvas choices
                        if schedule_effects_list and isinstance(schedule_effects_list, list):
                            for se in schedule_effects_list:
                                try:
                                    passage_body += f'<<script>>setup.scheduleEvent({json.dumps(se)});<</script>>'
                                except (TypeError, ValueError) as e:
                                    logger.warning("Invalid schedule effect in choice '%s': %s", choice_text, e)
                        # Show effect notification before time progression
                        if has_effects:
                            passage_body += "<<script>>setup.showEffectNotification();<</script>>"
                        # Mark conditional choice as visited when clicked
                        if choice_key:
                            passage_body += f'<<script>>setup.markChoiceVisited("{choice_key}");<</script>>'

                        # ── Loop: inject loop state changes inside the link ──
                        if is_loop_base and role == 'non_terminal' and choice_node_slug:
                            # Track this choice as visited in loop state
                            passage_body += f'<<run $game_state.loop_visited.push("{choice_node_slug}")>>'
                        if loop_config and role in ('exit', 'terminal'):
                            # Clear loop state when exiting canvas or entering terminal node
                            passage_body += '<<set $game_state.loop_count to 0>><<set $game_state.loop_visited to []>>'

                        # Then emit time progression and close link
                        passage_body += f"<<script>>advanceTime({int(time_minutes)});<</script>><</link>><br>\n"

                        # ── Close gate(s): span, then INNER cost rung, then OUTER conditions ──
                        # Close highlight wrapper (only opened when a real conditions gate exists).
                        if choice_key:
                            passage_body += '</span>\n'
                        # Inner cost-affordability rung — always greyed-visible when unaffordable
                        # (independent of show_when_locked, which governs the main-lock tier below).
                        if choice_costs_js:
                            # Keep the ACTION label and append the requirement in a bracket
                            # beside it (don't replace the text) — matches the main-lock
                            # locked_text style, e.g. "Work a shift 🍺 (Requires 15 Energy (you have 6))".
                            _esc_choice_label = choice_text.replace('"', '\\"').replace('[', '&#91;').replace(']', '&#93;')
                            passage_body += "<<else>>\n"
                            passage_body += f'<span class="locked-choice" title="{_esc_choice_label}">{_esc_choice_label} (<<= setup.getCostBlockedMessage({choice_costs_js})>>)</span><br>\n'
                            passage_body += "<</if>>\n"
                        # ── Rejection / locked-visible system (main-lock tier) ──
                        if cond_expr is not None:
                            if show_when_locked:
                                passage_body += "<<else>>\n"
                                escaped_locked = (locked_text or choice_text).replace('"', '\\"').replace('[', '&#91;').replace(']', '&#93;')
                                if rejection_passage:
                                    # Mode B: Clickable rejection — redirects to rejection node
                                    passage_body += f'<span class="rejection-choice">\n'
                                    passage_body += f'<<link "{escaped_locked}" "{rejection_passage}">>'
                                    # Apply rejection effects
                                    if rejection_effects and isinstance(rejection_effects, list):
                                        passage_body += "<<script>>setup.pendingEffects = [];<</script>>"
                                        for eff in rejection_effects:
                                            try:
                                                ttype = eff.get('targetType', 'player')
                                                npc_id = eff.get('npcId')
                                                trait = str(eff.get('trait', ''))
                                                op = eff.get('op', 'add')
                                                val = eff.get('value', 0)
                                                clamp_flag = eff.get('clamp', False)
                                                cap = eff.get('cap', None)
                                                npc_id_js = f'"{npc_id}"' if npc_id else 'null'
                                                trait_js = trait.replace('"', '\\"')
                                                clamp_js = 'true' if clamp_flag else 'false'
                                                cap_js = 'null' if (cap is None) else str(int(cap) if isinstance(cap, (int, float)) else cap)
                                                passage_body += (
                                                    f'<<script>>setup.applyAndNotifyTrait("{ttype}", {npc_id_js}, "{trait_js}", "{op}", {self._resolve_effect_value(val)}, {clamp_js}, {cap_js});<</script>>'
                                                )
                                            except (KeyError, TypeError, ValueError) as e:
                                                logger.warning("Invalid rejection effect: %s", e)
                                        passage_body += "<<script>>setup.showEffectNotification();<</script>>"
                                    passage_body += f"<<script>>advanceTime({int(time_minutes)});<</script>><</link>>\n"
                                    passage_body += '</span><br>\n'
                                else:
                                    # Mode A: Greyed-out locked choice with tooltip.
                                    # S4 (2026-05-06) — if locked_text_threshold
                                    # is set, wrap the label in a <<button>> that
                                    # fires a threshold-notification toast on
                                    # click. Mirrors RTS <<NotifyCorruption N>>
                                    # pattern (doc 13 §7.4 + doc 22 §11). When
                                    # no threshold is set, fall back to the
                                    # static span (no behavior change for
                                    # pre-existing locked choices).
                                    if locked_text_threshold:
                                        escaped_threshold = locked_text_threshold.replace('"', '\\"').replace('[', '&#91;').replace(']', '&#93;')
                                        passage_body += f'<span class="locked-choice" title="{escaped_locked}">'
                                        passage_body += f'<<button "{escaped_locked}">>'
                                        passage_body += f'<<run setup.queueGatedNotification("{escaped_threshold}")>>'
                                        passage_body += f'<<run setup.showEffectNotification()>>'
                                        passage_body += '<</button>>'
                                        passage_body += '</span><br>\n'
                                    else:
                                        passage_body += f'<span class="locked-choice" title="{escaped_locked}">'
                                        passage_body += f'{escaped_locked}'
                                        passage_body += '</span><br>\n'
                            passage_body += "<</if>>\n"

                        # ── Loop: close visited check for non-terminal choices on base node ──
                        if is_loop_base and role == 'non_terminal' and choice_node_slug:
                            passage_body += '<</if>>\n'

                    # ── Loop: add loop-back choice for non-terminal sub-nodes ──
                    if is_loop_sub and not is_loop_terminal_node and base_passage_name:
                        max_revisits = loop_config.get('max_revisits', 2)
                        loop_back_text = loop_config.get('loop_back_text', 'Stay a while')
                        escaped_lb_text = loop_back_text.replace('"', '\\"').replace('[', '&#91;').replace(']', '&#93;')
                        passage_body += f'<<if $game_state.loop_count lt {max_revisits}>>\n'
                        passage_body += f'<<link "{escaped_lb_text}" "{base_passage_name}">>'
                        # Duplicate effects from the sub-node's first exit choice
                        first_exit = exit_result[0] if exit_result else None
                        if first_exit:
                            lb_trait_effects = first_exit[3] if len(first_exit) > 3 else []
                            lb_flag_effects = first_exit[4] if len(first_exit) > 4 else []
                            lb_wardrobe_effects = first_exit[6] if len(first_exit) > 6 else []
                            lb_quest_effects = first_exit[16] if len(first_exit) > 16 else []   # doc 45 G4
                            lb_schedule_effects = first_exit[17] if len(first_exit) > 17 else []  # doc 45 G5
                            lb_time = first_exit[2] if len(first_exit) > 2 else 3
                            lb_has_effects = (lb_trait_effects and isinstance(lb_trait_effects, list)) or (lb_flag_effects and isinstance(lb_flag_effects, list)) or (self.clothing_enabled and lb_wardrobe_effects and isinstance(lb_wardrobe_effects, list)) or (lb_quest_effects and isinstance(lb_quest_effects, list)) or (lb_schedule_effects and isinstance(lb_schedule_effects, list))
                            if lb_has_effects:
                                passage_body += "<<script>>setup.pendingEffects = [];<</script>>"
                            if lb_trait_effects and isinstance(lb_trait_effects, list):
                                for eff in lb_trait_effects:
                                    ttype = eff.get('targetType', 'player')
                                    npc_id = eff.get('npcId')
                                    trait = str(eff.get('trait', ''))
                                    op = eff.get('op', 'add')
                                    val = eff.get('value', 0)
                                    clamp_flag = eff.get('clamp', False)
                                    cap = eff.get('cap', None)
                                    npc_id_js = f'"{npc_id}"' if npc_id else 'null'
                                    trait_js = trait.replace('"', '\\"')
                                    clamp_js = 'true' if clamp_flag else 'false'
                                    cap_js = 'null' if (cap is None) else str(int(cap) if isinstance(cap, (int, float)) else cap)
                                    passage_body += f'<<script>>setup.applyAndNotifyTrait("{ttype}", {npc_id_js}, "{trait_js}", "{op}", {self._resolve_effect_value(val)}, {clamp_js}, {cap_js});<</script>>'
                            if lb_flag_effects and isinstance(lb_flag_effects, list):
                                for fe in lb_flag_effects:
                                    ftype = fe.get('targetType', 'player')
                                    fnpc = fe.get('npcId')
                                    flag_val = str(fe.get('flag', ''))
                                    fop = str(fe.get('op', 'set') or 'set')
                                    npc_js = f'"{fnpc}"' if fnpc else 'null'
                                    passage_body += f'<<script>>setup.applyAndNotifyFlag("{ftype}", {npc_js}, "{flag_val}", "{fop}");<</script>>'
                            if self.clothing_enabled and lb_wardrobe_effects and isinstance(lb_wardrobe_effects, list):
                                for we in lb_wardrobe_effects:
                                    w_action = we.get('action', 'add')
                                    w_item_id = str(we.get('item_id', '')).replace('"', '\\"')
                                    if w_action == 'add' and w_item_id:
                                        passage_body += f'<<script>>setup.addToWardrobe("{w_item_id}");<</script>>'
                                    elif w_action == 'equip' and w_item_id:
                                        passage_body += f'<<script>>setup.addToWardrobe("{w_item_id}"); setup.equipItem("{w_item_id}");<</script>>'
                            # doc 45 G4/G5 — duplicate quest + scheduled effects on the loop-back choice
                            if lb_quest_effects and isinstance(lb_quest_effects, list):
                                for qe in lb_quest_effects:
                                    q_id = str(qe.get('quest', '')).replace('"', '\\"')
                                    if q_id:
                                        q_step = qe.get('step')
                                        q_step_js = 'null' if q_step is None else str(int(q_step))
                                        passage_body += f'<<script>>setup.applyQuestEffect("{q_id}", "{str(qe.get("op", "start"))}", {q_step_js});<</script>>'
                            if lb_schedule_effects and isinstance(lb_schedule_effects, list):
                                for se in lb_schedule_effects:
                                    passage_body += f'<<script>>setup.scheduleEvent({json.dumps(se)});<</script>>'
                            if lb_has_effects:
                                passage_body += "<<script>>setup.showEffectNotification();<</script>>"
                        passage_body += '<<set $game_state.loop_count to $game_state.loop_count + 1>>'
                        lb_time_val = int(lb_time) if first_exit else 3
                        passage_body += f'<<script>>advanceTime({lb_time_val});<</script>><</link>><br>\n'
                        passage_body += '<</if>>\n'

                    # If all choices were conditional and none are currently
                    # satisfied, emit a layered diagnostic + the Continue
                    # fallback. Three behaviors when zero exits satisfy:
                    #   (1) console.warn always — canvas slug + conditions +
                    #       state snapshot. Surfaces dead-ends to anyone with
                    #       DevTools open, including production players.
                    #   (2) Dev-mode visible banner — for each conditional
                    #       choice, walk its conditions.items array and render
                    #       ✓/✗ per item. Author sees instantly which clauses
                    #       are failing. Gated on $flags.debug_mode.
                    #   (3) Continue link to return_target (preserved).
                    # Without this diagnostic, dead-ends were silent — see
                    # the scene_office_after_crack dead-end of 2026-05-06
                    # (took several rounds of console paste-back to find).
                    if (not has_unconditional_choice) and conditional_expr_parts:
                        or_expr = ' or '.join(conditional_expr_parts)
                        # Build per-choice diagnostic data: text + conditions
                        # JSON for each conditional choice.
                        diag_choices = []
                        for ct in exit_result:
                            t = ct[1] if len(ct) > 1 else ''
                            c = ct[5] if len(ct) > 5 else None
                            if c:
                                diag_choices.append({"text": t, "conditions": c})
                        # JSON literals injected directly into JS — Python
                        # f-strings can't safely contain JSON braces, so
                        # build the body via string concatenation.
                        canvas_slug = self._get_canvas_slug(canvas)
                        # Sanitize slug for use as a JS identifier suffix
                        diag_var_suffix = re.sub(r'[^a-zA-Z0-9_]', '_', canvas_slug)
                        diag_var_name = "_engineNoExitsDiag_" + diag_var_suffix
                        choices_json = json.dumps(diag_choices)
                        canvas_slug_json = json.dumps(canvas_slug)
                        passage_body += "<<if not (" + or_expr + ")>>\n"
                        # (1) console.warn — always fires
                        passage_body += "<<script>>\n"
                        passage_body += "try {\n"
                        passage_body += "  window." + diag_var_name + " = " + choices_json + ";\n"
                        passage_body += "  if (typeof console !== 'undefined' && console.warn) {\n"
                        passage_body += "    console.warn('[engine] no exit choices satisfied', {\n"
                        passage_body += "      canvas: " + canvas_slug_json + ",\n"
                        passage_body += "      choices: window." + diag_var_name + ",\n"
                        passage_body += "      flags: State.variables.flags,\n"
                        passage_body += "      player_traits: (State.variables.player || {}).core_traits\n"
                        passage_body += "    });\n"
                        passage_body += "  }\n"
                        passage_body += "} catch(e) {}\n"
                        passage_body += "<</script>>\n"
                        # (2) Dev-mode visible diagnostic banner
                        passage_body += "<<if $flags.debug_mode>>\n"
                        passage_body += "<<set _diagChoices to window." + diag_var_name + ">>\n"
                        passage_body += '<div class="engine-diag-no-exits">\n'
                        passage_body += '<div class="engine-diag-header">⚠️ DEV: No exit choices satisfied — canvas ' + canvas_slug + '</div>\n'
                        passage_body += '<div class="engine-diag-hint">All exits are conditional and none of their gates currently evaluate true. Player will use the Continue link below to escape, but the visit fires no effects. Likely authoring gap — add a fallback choice or broaden a condition.</div>\n'
                        passage_body += "<<for _i to 0; _i lt _diagChoices.length; _i++>>\n"
                        passage_body += "<<set _ch to _diagChoices[_i]>>\n"
                        passage_body += '<div class="engine-diag-choice">\n'
                        passage_body += '<div class="engine-diag-choice-text">Choice: "<<print _ch.text>>"</div>\n'
                        passage_body += '<div class="engine-diag-choice-logic">Combined as: <<print _ch.conditions.logic>></div>\n'
                        passage_body += '<ul class="engine-diag-items">\n'
                        passage_body += "<<for _j to 0; _j lt _ch.conditions.items.length; _j++>>\n"
                        passage_body += "<<set _it to _ch.conditions.items[_j]>>\n"
                        passage_body += '<<set _single to {version: "1.0", logic: "AND", items: [_it]}>>\n'
                        passage_body += "<<set _ok to setup.triggerConditionsSatisfied(_single)>>\n"
                        passage_body += '<li class="<<print _ok ? \'engine-diag-pass\' : \'engine-diag-fail\'>>"><<if _ok>>✓<<else>>✗<</if>> <<print JSON.stringify(_it)>></li>\n'
                        passage_body += "<</for>>\n"
                        passage_body += "</ul>\n"
                        passage_body += "</div>\n"
                        passage_body += "<</for>>\n"
                        passage_body += "</div>\n"
                        passage_body += "<</if>>\n"
                        # (3) Continue fallback (player-facing escape). No "No available
                        # choices" line — when rungs are cost/condition-locked they're still
                        # shown greyed with their own reason ("Requires N Energy …"), so that
                        # text was redundant and contradictory. The dev banner above (gated on
                        # $flags.debug_mode) still flags genuine authoring dead-ends.
                        passage_body += "[[Continue->" + return_target + "]]\n"
                        passage_body += "<</if>>\n"
                    passage_body += "<</nobr>>\n"
                else:
                    # Shouldn't happen for 'choices', but guard anyway
                    next_passage, continue_text = exit_result
                    time_progression = self._get_time_progression_for_node(node)
                    passage_body += f"{time_progression}\n[[{continue_text}->{next_passage}]]\n"

                # Cascade-aware exit routing: if the rendered node body carries
                # the cascade-exit sentinel(s), splice the entire passage_body
                # (links + no-exits diagnostic + every gating wrapper) INTO
                # each cascade's last advance-beat linkreplace body, and skip
                # the tail emit. Player sees only Beat 0 + the first advance
                # link at first render; clicking through to the last advance
                # reveals the terminal beat content + the exit choices in one
                # DOM swap. Per RTS Pattern E (memory
                # rts_cross_npc_mechanism_comparison.md).
                #
                # Multi-cascade case: a node body may contain N cascades nested
                # inside mutually-exclusive group blocks (the kitchen_morning
                # stage-variant pattern). Each cascade's last advance beat
                # plants its own sentinel; we substitute ALL of them with the
                # same exit HTML so any group-variant the player lands on
                # routes exits correctly. The rendered HTML duplicates the exit
                # block once per cascade variant; only one variant ever fires
                # at runtime (group conditions are mutually exclusive), so the
                # duplication is invisible to players.
                # P7 audit fix (2026-05-12) — Pattern C support. Check SAFE
                # sentinel FIRST: if any cascade in this node body has gated
                # beats (Pattern C), it planted SAFE instead of STANDARD.
                # Conservative path = strip ALL sentinels (including STANDARD
                # if any other cascade in this node body is non-Pattern-C) +
                # leave passage_body intact so exits render at passage bottom.
                # Reason: gated beats can fail at runtime, terminating the
                # cascade before its sentinel renders. Without bottom exits,
                # the player is stuck. Multi-cascade fall-through to bottom
                # is acceptable UX (slight inline-vs-bottom degradation for
                # the non-gated tier variants in the same node body) and is
                # RTS-aligned (RTS scenes render exits at passage bottom).
                if _CASCADE_EXIT_INJECT_SAFE_SENTINEL in node_content:
                    # Strip both sentinel types; keep passage_body intact.
                    node_content = node_content.replace(
                        _CASCADE_EXIT_INJECT_SAFE_SENTINEL, ""
                    )
                    node_content = node_content.replace(
                        _CASCADE_EXIT_INJECT_SENTINEL, ""
                    )
                    # Rebuild passage_header with the cleaned node_content.
                    # passage_body NOT cleared — exits render at passage bottom.
                    passage_header = (
                        f":: {node_passage_name}\n"
                        f"{dev_canvas_info}"
                        f"{node_content}\n\n"
                        f"<<set $game_state.current_canvas = \"{canvas.id}\">>\n"
                        f"<<set $game_state.current_node = \"{node.id}\">>\n"
                        f"{mark_trigger}"
                        f"{track_visited_node}"
                    )
                elif _CASCADE_EXIT_INJECT_SENTINEL in node_content:
                    inner = passage_body
                    # Strip the wrapping `\n<<nobr>>\n` ... `<</nobr>>\n` so
                    # the links land directly inside the linkreplace body.
                    # SugarCube tolerates nested <<nobr>> if the strip misses,
                    # but stripping keeps rendered HTML cleaner.
                    if inner.startswith("\n<<nobr>>\n"):
                        inner = inner[len("\n<<nobr>>\n"):]
                    if inner.endswith("<</nobr>>\n"):
                        inner = inner[:-len("<</nobr>>\n")]
                    # Replace ALL sentinels (multi-cascade safety).
                    node_content = node_content.replace(
                        _CASCADE_EXIT_INJECT_SENTINEL, inner
                    )
                    # Rebuild passage_header with the substituted node_content.
                    passage_header = (
                        f":: {node_passage_name}\n"
                        f"{dev_canvas_info}"
                        f"{node_content}\n\n"
                        f"<<set $game_state.current_canvas = \"{canvas.id}\">>\n"
                        f"<<set $game_state.current_node = \"{node.id}\">>\n"
                        f"{mark_trigger}"
                        f"{track_visited_node}"
                    )
                    passage_body = ""

                passage = passage_header + passage_body + "\n"
            elif exit_type == 'game_end':
                # Game end: apply effects, show restart button, no navigation
                time_progression = self._get_time_progression_for_node(node)
                trait_effects = self._get_trait_effects_for_node(node)
                flag_effects = self._get_flag_effects_for_node(node)
                wardrobe_effects_code = self._get_wardrobe_effects_for_node(node)
                end_text = exit_block.get('text', 'The End')
                from html import escape as html_escape
                safe_end_text = html_escape(str(end_text))
                passage = (
                    passage_header
                    + f"{time_progression}\n{trait_effects}\n{flag_effects}\n{wardrobe_effects_code}\n"
                    + f"<div class='game-end'><h2>{safe_end_text}</h2>"
                    + f"<<link 'Play Again'>><<run Engine.restart()>><</link>>"
                    + f"</div>\n\n"
                )
            else:
                # Location type - if outgoing connections exist, continue to first outgoing node
                next_passage = None
                # NodeConnection is never created on this pipeline (dead relation);
                # in no-DB mode the reverse manager would query an empty table.
                if self.graph is not None:
                    outgoing = []
                else:
                    outgoing = list(getattr(node, 'outgoing_connections', []).all()) if hasattr(node, 'outgoing_connections') else []
                if outgoing:
                    first_conn = outgoing[0]
                    target_id = str(first_conn.target_node_id)
                    next_passage = self.passage_name_map.get(target_id)

                if next_passage:
                    continue_text = "Continue"
                else:
                    # Fallback per exit block config to trigger/specific location
                    resolved = self._process_exit_block(node, return_target)
                    if isinstance(resolved, list):
                        # Unexpected for location type; default to return target
                        next_passage, continue_text = return_target, "Continue"
                    else:
                        next_passage, continue_text = resolved

                time_progression = self._get_time_progression_for_node(node)
                trait_effects = self._get_trait_effects_for_node(node)
                flag_effects = self._get_flag_effects_for_node(node)
                wardrobe_effects_code = self._get_wardrobe_effects_for_node(node)
                effects_block = (
                    f"{time_progression}\n{trait_effects}\n"
                    f"{flag_effects}\n{wardrobe_effects_code}\n"
                )
                exit_link = f"[[{continue_text}->{next_passage}]]\n"

                # Cascade-aware exit routing for the single-Continue (location)
                # exit — mirror of the choices-branch splice (~line 11971). When
                # the node body carries a cascade-exit sentinel, the lone
                # Continue link is spliced INTO the cascade's last advance-beat
                # <<linkreplace>> body, so it appears only after the player has
                # clicked all the way through the cascade — never at passage
                # bottom beside the advance "show more" link. Without this, a
                # cascade on a location-type node leaked its sentinel and
                # rendered the exit immediately, letting the player skip the
                # whole scene (the opening cold-open was skippable in one click).
                # Node-level effects stay on entry (fire on load, unchanged).
                # The SAFE sentinel (a gated beat can fail mid-cascade, ending it
                # before its planted sentinel renders) is stripped and the exit
                # kept at passage bottom so the player can't be stranded — same
                # conservative rule as the choices branch. The sentinel lives
                # inside node_content, which is already embedded in
                # passage_header, so a string replace on passage_header handles
                # it while preserving pre_substitution_macros / substitution_check
                # (which the choices-branch rebuild drops). `.replace` swaps every
                # occurrence, covering the multi-cascade (group-variant) case.
                if _CASCADE_EXIT_INJECT_SAFE_SENTINEL in passage_header:
                    passage_header = passage_header.replace(
                        _CASCADE_EXIT_INJECT_SAFE_SENTINEL, ""
                    )
                    passage_header = passage_header.replace(
                        _CASCADE_EXIT_INJECT_SENTINEL, ""
                    )
                    passage = passage_header + effects_block + exit_link + "\n"
                elif _CASCADE_EXIT_INJECT_SENTINEL in passage_header:
                    passage_header = passage_header.replace(
                        _CASCADE_EXIT_INJECT_SENTINEL, exit_link
                    )
                    passage = passage_header + effects_block + "\n"
                else:
                    passage = passage_header + effects_block + exit_link + "\n"

            # Cost gate: wrap Node 1 of canvases with costs
            # If player can't afford costs, show blocked message instead of content
            if i == 0 and canvas_costs and passage_prefix in ("Canvas", "StartingCanvas"):
                costs_json = json.dumps(canvas_costs)
                # Split passage into header line (:: PassageName) and body
                passage_lines = passage.split('\n', 1)
                passage_title = passage_lines[0]  # :: Canvas_X_Node_1
                passage_body = passage_lines[1] if len(passage_lines) > 1 else ''
                passage = (
                    f"{passage_title}\n"
                    f"<<set _costs to {costs_json}>>\\\n"
                    f"<<if setup.checkCostsAffordable(_costs)>>\\\n"
                    f"<<script>>setup.deductCosts(\"{canvas.id}\");<</script>>\n"
                    f"{passage_body}"
                    f"<<else>>\n"
                    f"<div class=\"cost-blocked-message\">\n"
                    f"<p><<= setup.getCostBlockedMessage(_costs)>></p>\n"
                    f"</div>\n"
                    f"[[Back->{return_target}]]\n"
                    f"<</if>>\n"
                )

            # Modifier redirect: if node has modifier_redirect, inject <<goto>> before content
            node_data = getattr(node, 'node_data', None) or {}
            mod_redirect = node_data.get('modifier_redirect')
            if mod_redirect:
                mod_key = mod_redirect.get('modifier_key', '')
                redirect_node_id = mod_redirect.get('node')
                if mod_key and redirect_node_id:
                    redirect_passage = self.passage_name_map.get(str(redirect_node_id))
                    if redirect_passage:
                        escaped_mod_key = mod_key.replace('"', '\\"')
                        passage_lines = passage.split('\n', 1)
                        passage_title = passage_lines[0]
                        passage_rest = passage_lines[1] if len(passage_lines) > 1 else ''
                        passage = (
                            f"{passage_title}\n"
                            f'<<if setup.isModifierActive("{escaped_mod_key}")>>'
                            f'<<goto "{redirect_passage}">>'
                            f'<</if>>\n'
                            f"{passage_rest}"
                        )

            content += passage

        return content

    def _process_exit_block(self, node, return_target: str):
        """
        Process Exit Block configuration to determine next passage and link text.

        Args:
            node: Story node with exit_block configuration
            return_target: Default return target (trigger location)

        Returns:
            For 'location' type: Tuple of (next_passage, continue_text)
            For 'choices' type: List of tuples [(target_passage, choice_text, time_minutes), ...]
        """
        try:
            # Get exit block configuration
            exit_block = getattr(node, 'exit_block', None) or {}

            # Default fallback values
            default_text = "Continue"
            default_target = return_target

            # Extract configuration values
            exit_type = exit_block.get('type', 'location')
            config = exit_block.get('config', {})

            if exit_type == 'choices':
                # Process choices type - return list of choice tuples
                choices = exit_block.get('choices', [])
                default_time = config.get('default_time_progression', 3)

                if not choices:
                    # No choices defined, fallback to single link
                    logger.warning(f"Exit block for node {node.id} has type 'choices' but no choices defined")
                    return return_target, default_text

                processed_choices = []
                for choice in choices:
                    choice_text = choice.get('text', 'Continue')
                    # Don't use _resolve_at_references here — <<print>> macros break
                    # inside <<link "...">> quoted strings. The expression-mode resolver
                    # is applied later when rendering the <<link>> tag (line ~6489).
                    target_type = choice.get('targetType', 'trigger')
                    time_minutes = choice.get('time_progression_minutes', default_time)
                    effects = choice.get('effects', []) or []
                    flag_effects = choice.get('flagEffects', []) or []
                    conditions_obj = choice.get('conditions') if isinstance(choice.get('conditions'), dict) else None
                    wardrobe_effects = choice.get('wardrobeEffects', []) or []
                    # Rejection system fields
                    show_when_locked = bool(choice.get('show_when_locked', False))
                    locked_text = choice.get('locked_text', '')
                    locked_text_threshold = choice.get('locked_text_threshold', '')
                    rejection_node_id = choice.get('rejection_node')
                    rejection_effects = choice.get('rejection_effects', []) or []
                    # Modifier effects
                    modifier_effects = choice.get('modifier_effects', []) or []
                    # Pass effects (recurring pass purchases)
                    pass_effects = choice.get('pass_effects', []) or []
                    # Item effects (inventory add/remove)
                    item_effects = choice.get('item_effects', []) or []
                    # doc 45 G4/G5 — quest + scheduled effects
                    quest_effects = choice.get('questEffects', []) or []
                    schedule_effects = choice.get('scheduleEffects', []) or []
                    # Per-choice resource costs (energy/hygiene tier under `conditions`)
                    choice_costs = choice.get('costs', []) or []

                    # Resolve target based on targetType.
                    # Broken refs route to _BrokenExitFallback (loud throw) instead of
                    # silently redirecting to the trigger location / Navigation. The
                    # validator (template_import.py validate()) hard-fails on these
                    # before they reach emission in any normal build — so reaching
                    # the BROKEN_EXIT branches below means a code path bypassed the
                    # validator (test fixture, direct dev API, etc.).
                    BROKEN_EXIT = "_BrokenExitFallback"
                    if target_type == 'trigger':
                        target_passage = return_target
                    elif target_type == 'location':
                        location_id = choice.get('locationId')
                        if location_id:
                            loc = self._get_location_by_id(location_id)
                            if loc:
                                target_passage = self._location_passage_name(loc)
                            else:
                                target_passage = BROKEN_EXIT
                                logger.error(f"BROKEN EXIT — choice in node {node.id} references unknown locationId {location_id!r} (validator should have caught this)")
                        else:
                            target_passage = BROKEN_EXIT
                            logger.error(f"BROKEN EXIT — choice in node {node.id} has targetType 'location' but no locationId (validator should have caught this)")
                    elif target_type == 'node':
                        node_id = choice.get('nodeId')
                        if node_id:
                            # Look up passage name in the map
                            target_passage = self.passage_name_map.get(str(node_id))
                            if not target_passage:
                                target_passage = BROKEN_EXIT
                                logger.error(f"BROKEN EXIT — choice in node {node.id} references unknown nodeId {node_id!r} (validator should have caught this)")
                        else:
                            target_passage = BROKEN_EXIT
                            logger.error(f"BROKEN EXIT — choice in node {node.id} has targetType 'node' but no nodeId (validator should have caught this)")
                    else:
                        # Unknown target type
                        target_passage = BROKEN_EXIT
                        logger.error(f"BROKEN EXIT — unknown targetType {target_type!r} in choice for node {node.id} (validator should have caught this)")

                    # Resolve rejection_node to passage name
                    rejection_passage = None
                    if rejection_node_id:
                        rejection_passage = self.passage_name_map.get(str(rejection_node_id))
                        if not rejection_passage:
                            logger.warning(f"Choice in node {node.id} references unknown rejection_node {rejection_node_id}")

                    text_variants = choice.get('text_variants', []) or []
                    processed_choices.append((
                        target_passage, choice_text, time_minutes, effects, flag_effects,
                        conditions_obj, wardrobe_effects,
                        show_when_locked, locked_text, rejection_passage, rejection_effects,
                        modifier_effects,
                        pass_effects,
                        item_effects,
                        text_variants,
                        locked_text_threshold,  # S4 — position 15
                        quest_effects,           # doc 45 G4 — position 16
                        schedule_effects,        # doc 45 G5 — position 17
                        choice_costs,            # per-choice costs — position 18
                    ))

                return processed_choices

            elif exit_type == 'location':
                # Process location type - return single tuple.
                # Broken refs route to _BrokenExitFallback (loud throw) — see the
                # 'choices' branch above for rationale. Validator should have caught
                # any broken ref reaching this code path.
                link_text = exit_block.get('text', default_text) or default_text
                destination_type = config.get('destinationType', 'trigger')
                BROKEN_EXIT = "_BrokenExitFallback"

                if destination_type == 'trigger':
                    # Return to trigger location (default behavior)
                    next_passage = return_target
                elif destination_type == 'specific':
                    # Go to specific location (if locationId is provided)
                    location_id = config.get('locationId')
                    if location_id:
                        # Resolve by ID and format using the location's name (matches passage naming)
                        loc = self._get_location_by_id(location_id)
                        if loc:
                            next_passage = self._location_passage_name(loc)
                        else:
                            next_passage = BROKEN_EXIT
                            logger.error(f"BROKEN EXIT — exit_block for node {node.id} references unknown locationId {location_id!r} (validator should have caught this)")
                    else:
                        next_passage = BROKEN_EXIT
                        logger.error(f"BROKEN EXIT — exit_block for node {node.id} has specific destination but no locationId (validator should have caught this)")
                elif destination_type == 'node':
                    node_id = config.get('destinationId')
                    if node_id:
                        target_passage = self.passage_name_map.get(str(node_id))
                        if target_passage:
                            next_passage = target_passage
                        else:
                            next_passage = BROKEN_EXIT
                            logger.error(f"BROKEN EXIT — exit_block for node {node.id} references unknown destinationId {node_id!r} (validator should have caught this)")
                    else:
                        next_passage = BROKEN_EXIT
                        logger.error(f"BROKEN EXIT — exit_block for node {node.id} has destinationType 'node' but no destinationId (validator should have caught this)")
                else:
                    # Unknown destination type
                    next_passage = BROKEN_EXIT
                    logger.error(f"BROKEN EXIT — unknown destinationType {destination_type!r} in exit_block for node {node.id} (validator should have caught this)")

                return next_passage, link_text
            elif exit_type == 'game_end':
                # Game end type - no navigation, handled in passage builder
                link_text = exit_block.get('text', 'The End')
                return None, link_text
            else:
                # Unknown exit type, fallback to default behavior
                logger.warning(f"Unknown exit type '{exit_type}' in exit block for node {node.id}")
                return return_target, default_text

        except (KeyError, TypeError, ValueError) as e:
            logger.error(f"Error processing exit block for node {node.id}: {e}")
            raise ValueError(
                f"Failed to process exit block for node {node.id}: {e}"
            ) from e

    def _get_time_progression_for_node(self, node) -> str:
        """
        Extract time progression from node's exit block configuration.

        Args:
            node: Story node with exit_block configuration

        Returns:
            String containing SugarCube time advancement code
        """
        try:
            # Get exit block configuration
            exit_block = getattr(node, 'exit_block', None) or {}
            config = exit_block.get('config', {})

            # Get time progression minutes (default to 3 if not specified)
            time_minutes = config.get('time_progression_minutes', 3)

            # Validate time value
            if not isinstance(time_minutes, (int, float)) or time_minutes < 0:
                time_minutes = 3  # Fallback to default

            # Generate SugarCube time advancement code
            if time_minutes > 0:
                return f"<<script>>advanceTime({int(time_minutes)});<</script>>"
            else:
                return ""

        except (KeyError, TypeError, AttributeError) as e:
            logger.warning(f"Error getting time progression for node {node.id}: {e}. Using default 3 minutes.")
            return "<<script>>advanceTime(3);<</script>>"

    def _get_flag_effects_for_node(self, node) -> str:
        """
        Extract flag effects from node's exit block configuration.

        Args:
            node: Story node with exit_block configuration

        Returns:
            String containing SugarCube flag effect code
        """
        try:
            exit_block = getattr(node, 'exit_block', None) or {}
            config = exit_block.get('config', {})

            # Collect flag effects from both sources:
            # 1. Dedicated flagEffects array
            # 2. Effects array items with 'flag' property (no 'trait')
            flag_effects = list(config.get('flagEffects', []))

            for eff in config.get('effects', []):
                if eff.get('flag') and not eff.get('trait'):
                    flag_effects.append(eff)

            if not flag_effects:
                return ""

            code_parts = []
            for fe in flag_effects:
                target_type = fe.get('targetType', 'player')
                npc_id = fe.get('npcId')
                flag = fe.get('flag', '')
                fop = str(fe.get('op', 'set') or 'set')

                if not flag:
                    continue

                npc_js = f'"{npc_id}"' if npc_id else 'null'
                flag_js = flag.replace('"', '\\"')
                code_parts.append(f'setup.applyAndNotifyFlag("{target_type}", {npc_js}, "{flag_js}", "{fop}");')

            if code_parts:
                return "<<script>>" + "".join(code_parts) + "<</script>>"
            return ""

        except (KeyError, TypeError, AttributeError) as e:
            logger.warning(f"Error getting flag effects for node {node.id}: {e}. Skipping flag effects.")
            return ""

    def _get_trait_effects_for_node(self, node) -> str:
        """
        Extract trait effects from node's exit block configuration.

        Args:
            node: Story node with exit_block configuration

        Returns:
            String containing SugarCube trait effect code
        """
        try:
            exit_block = getattr(node, 'exit_block', None) or {}
            config = exit_block.get('config', {})
            effects = config.get('effects', [])

            if not effects:
                return ""

            code_parts = []
            for eff in effects:
                target_type = eff.get('targetType', 'player')
                npc_id = eff.get('npcId')
                trait = str(eff.get('trait', ''))
                op = eff.get('op', 'add')
                val = eff.get('value', 0)
                clamp_flag = eff.get('clamp', False)
                cap = eff.get('cap', None)

                if not trait:
                    continue

                npc_js = f'"{npc_id}"' if npc_id else 'null'
                trait_js = trait.replace('"', '\\"')
                clamp_js = 'true' if clamp_flag else 'false'
                cap_js = 'null' if (cap is None) else str(int(cap) if isinstance(cap, (int, float)) else cap)

                code_parts.append(
                    f'setup.applyAndNotifyTrait("{target_type}", {npc_js}, "{trait_js}", "{op}", {self._resolve_effect_value(val)}, {clamp_js}, {cap_js});'
                )

            if code_parts:
                return "<<script>>setup.pendingEffects = [];" + "".join(code_parts) + "setup.showEffectNotification();<</script>>"
            return ""

        except (KeyError, TypeError, AttributeError) as e:
            logger.warning(f"Error getting trait effects for node {node.id}: {e}. Skipping trait effects.")
            return ""

    def _get_wardrobe_effects_for_node(self, node) -> str:
        """Extract wardrobe effects from node's exit block configuration."""
        if not self.clothing_enabled:
            return ""
        try:
            exit_block = getattr(node, 'exit_block', None) or {}
            config = exit_block.get('config', {})
            wardrobe_effects = config.get('wardrobeEffects', [])

            if not wardrobe_effects:
                return ""

            code_parts = []
            for we in wardrobe_effects:
                action = we.get('action', 'add')
                item_id = str(we.get('item_id', '')).replace('"', '\\"')
                if not item_id:
                    continue
                if action == 'add':
                    code_parts.append(f'setup.addToWardrobe("{item_id}");')
                elif action == 'equip':
                    code_parts.append(f'setup.addToWardrobe("{item_id}"); setup.equipItem("{item_id}");')

            if code_parts:
                return "<<script>>setup.pendingEffects = setup.pendingEffects || [];" + "".join(code_parts) + "setup.showEffectNotification();<</script>>"
            return ""

        except (KeyError, TypeError, AttributeError) as e:
            logger.warning(f"Error getting wardrobe effects for node {node.id}: {e}. Skipping.")
            return ""

    # ── Inline-effect helpers (S7 cascade beats + choice path consolidation) ──
    # These produce per-effect `<<script>>setup.applyAndNotifyX(...)<</script>>` fragments
    # for use INSIDE link / linkreplace / button macro bodies. Mirrors the
    # historical inline emission at the choice-rendering path; cascade beats
    # call the same helpers so per-beat effect semantics match choice-exit
    # effect semantics exactly. (S7 doctrine: live-verified in doc 22 §11
    # MarcusParkDate, where <<MakeBoyfriend>> fired on the Accept linkreplace
    # click — beat effects must fire on the click that reveals the beat.)
    def _resolve_effect_value(self, val) -> str:
        """Resolve an effect's `value` field into a JS expression string for emission.

        Accepts two shapes:
        - Numeric (int / float): emitted as a float literal (e.g. ``"5.0"``).
          Backwards-compatible with all pre-2026-05-08 effect specs.
        - Random-range dict (``{"type": "random", "min": N, "max": M}``):
          emitted as an inclusive integer-random JS expression
          ``"(Math.floor(Math.random() * <span>) + <min>)"``.
          Used by the sex-loop hub pleasure mutations per
          ``28th_april_TLS_Phase2_Redesign/23_Location_Menu_Sex_Loop_Hybrid.md`` §6.

        Returns the raw JS expression string — caller interpolates it directly
        into the ``setup.applyAndNotifyTrait(...)`` call site (no extra quoting).

        Raises ``ValueError`` on malformed input (matches ``_emit_trait_effects_inline``
        strictness — authoring mistakes surface as render errors, not nonsense effects).
        """
        # Bool guard FIRST: in Python ``isinstance(True, int)`` is True, so without this
        # check ``value = true`` in TOML would silently coerce to ``1.0``. Boolean effects
        # don't make sense (use flagEffects for booleans) — reject explicitly.
        if isinstance(val, bool):
            raise ValueError(
                f"Effect value must be a number or random-range dict; got bool: {val!r}. "
                f"If you meant a flag, use flagEffects instead of effects."
            )

        # Static numeric — current behavior, byte-equivalent emission.
        if isinstance(val, (int, float)):
            return str(float(val))

        # Random-range dict — new shape.
        if isinstance(val, dict):
            vtype = val.get("type")
            if vtype != "random":
                raise ValueError(
                    f"Effect value dict has unknown type {vtype!r}; "
                    f"only 'random' is supported. Got: {val!r}"
                )
            try:
                mn = int(val["min"])
                mx = int(val["max"])
            except (KeyError, TypeError, ValueError) as e:
                raise ValueError(
                    f"Random-range effect value missing/invalid 'min' or 'max' "
                    f"(both must be ints). Got: {val!r}"
                ) from e
            if mn > mx:
                raise ValueError(
                    f"Random-range effect value has min ({mn}) > max ({mx}). Got: {val!r}"
                )
            # Inclusive integer range:
            #   Math.floor(Math.random() * (max - min + 1)) + min
            # Wrapped in parens so it composes cleanly inside the
            # applyAndNotifyTrait call site.
            span = mx - mn + 1
            return f"(Math.floor(Math.random() * {span}) + {mn})"

        raise ValueError(
            f"Effect value must be a number or {{type: 'random', min, max}} dict. "
            f"Got: {val!r} (type={type(val).__name__})"
        )

    def _emit_trait_effects_inline(self, effects, context: str = "") -> str:
        """Emit trait-effect <<script>> blocks for a list of effect dicts.
        Returns concatenated SugarCube fragments. Empty string if no effects.
        Raises ValueError on malformed effects (preserving the choice-path strictness).
        """
        if not effects or not isinstance(effects, list):
            return ""
        out = []
        for eff in effects:
            try:
                ttype = eff.get('targetType', 'player')
                npc_id = eff.get('npcId')
                trait = str(eff.get('trait', ''))
                op = eff.get('op', 'add')
                val = eff.get('value', 0)
                clamp_flag = eff.get('clamp', False)
                cap = eff.get('cap', None)

                npc_id_js = f'"{npc_id}"' if npc_id else 'null'
                trait_js = trait.replace('"', '\\"')
                clamp_js = 'true' if clamp_flag else 'false'
                cap_js = 'null' if (cap is None) else str(int(cap) if isinstance(cap, (int, float)) else cap)

                out.append(
                    f"<<script>>setup.applyAndNotifyTrait(\"{ttype}\", {npc_id_js}, \"{trait_js}\", \"{op}\", {self._resolve_effect_value(val)}, {clamp_js}, {cap_js});<</script>>"
                )
            except (KeyError, TypeError, ValueError) as e:
                logger.error(
                    "Invalid trait effect in %s: %s. Effect data: %s",
                    context or "unknown context", e, eff
                )
                raise ValueError(
                    f"Invalid trait effect structure in {context or 'unknown'}: {e}"
                ) from e
        return "".join(out)

    def _emit_flag_effects_inline(self, effects, context: str = "") -> str:
        """Emit flag-effect <<script>> blocks for a list of effect dicts.
        Returns concatenated SugarCube fragments. Empty string if no effects.
        Raises ValueError on malformed effects.
        """
        if not effects or not isinstance(effects, list):
            return ""
        out = []
        for fe in effects:
            try:
                ftype = fe.get('targetType', 'player')
                fnpc = fe.get('npcId')
                flag = str(fe.get('flag', ''))
                fop = str(fe.get('op', 'set') or 'set')
                flag_js = flag.replace('"', '\\"')
                npc_js = f'"{fnpc}"' if fnpc else 'null'
                out.append(
                    f"<<script>>setup.applyAndNotifyFlag(\"{ftype}\", {npc_js}, \"{flag_js}\", \"{fop}\");<</script>>"
                )
            except (KeyError, TypeError, ValueError) as e:
                logger.error(
                    "Invalid flag effect in %s: %s. Effect data: %s",
                    context or "unknown context", e, fe
                )
                raise ValueError(
                    f"Invalid flag effect structure in {context or 'unknown'}: {e}"
                ) from e
        return "".join(out)

    def _emit_wardrobe_effects_inline(self, effects, context: str = "") -> str:
        """Emit wardrobe-effect <<script>> blocks for a list of effect dicts.
        Respects clothing_enabled flag. Returns "" if disabled or no effects.
        Logs warnings (not errors) on malformed effects — wardrobe is non-critical.
        """
        if not self.clothing_enabled or not effects or not isinstance(effects, list):
            return ""
        out = []
        for we in effects:
            try:
                w_action = we.get('action', 'add')
                w_item_id = str(we.get('item_id', '')).replace('"', '\\"')
                if w_action == 'add' and w_item_id:
                    out.append(f'<<script>>setup.addToWardrobe("{w_item_id}");<</script>>')
                elif w_action == 'equip' and w_item_id:
                    out.append(f'<<script>>setup.addToWardrobe("{w_item_id}"); setup.equipItem("{w_item_id}");<</script>>')
            except (KeyError, TypeError, ValueError) as e:
                logger.warning("Invalid wardrobe effect in %s: %s", context or "unknown context", e)
        return "".join(out)

    def _get_placeholder_svg(self) -> str:
        """Return inline SVG silhouette for missing portraits."""
        return (
            '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">'
            '<circle cx="50" cy="35" r="20" fill="#6c757d"/>'
            '<ellipse cx="50" cy="85" rx="35" ry="25" fill="#6c757d"/>'
            '</svg>'
        )

    def _get_location_placeholder_svg(self) -> str:
        """Return inline SVG silhouette for locations without images (building icon)."""
        return (
            '<svg viewBox="0 0 100 60" xmlns="http://www.w3.org/2000/svg">'
            '<rect x="10" y="20" width="35" height="35" fill="#6c757d" rx="2"/>'
            '<rect x="55" y="10" width="35" height="45" fill="#6c757d" rx="2"/>'
            '<rect x="17" y="27" width="8" height="8" fill="#4a4a5a"/>'
            '<rect x="30" y="27" width="8" height="8" fill="#4a4a5a"/>'
            '<rect x="17" y="40" width="8" height="8" fill="#4a4a5a"/>'
            '<rect x="30" y="40" width="8" height="8" fill="#4a4a5a"/>'
            '<rect x="62" y="17" width="8" height="8" fill="#4a4a5a"/>'
            '<rect x="75" y="17" width="8" height="8" fill="#4a4a5a"/>'
            '<rect x="62" y="30" width="8" height="8" fill="#4a4a5a"/>'
            '<rect x="75" y="30" width="8" height="8" fill="#4a4a5a"/>'
            '<rect x="62" y="43" width="8" height="8" fill="#4a4a5a"/>'
            '<rect x="75" y="43" width="8" height="8" fill="#4a4a5a"/>'
            '</svg>'
        )

    def _get_player_speech_labels(self) -> tuple[str, str, str]:
        """Speaker labels for the player's own dialog and thought-bubble blocks.

        Returns (dialog_label, thought_label, alt_label) for the game's
        `narration_person`.

        Third person emits the SugarCube macro rather than a build-time constant so a
        customizable player who renames themselves still sees their own name — the NPC
        branch of the same renderer already resolves speakers this way.

        `alt_label` is a separate PLAIN-TEXT variant: `_render_portrait` HTML-escapes its
        alt text, so a macro placed there would render as the literal string
        "<<print $player.name>>" instead of the name.
        """
        person = getattr(self, "narration_person", "second")
        if person == "first":
            return "Me", "💭 I'm thinking:", "Me"
        if person == "third":
            name = "<<print $player.name>>"
            alt = getattr(self, "player_name", "") or "Player"
            return name, f"💭 {name} is thinking:", alt
        return "You", "💭 You are thinking:", "You"

    def _render_portrait(self, portrait_path: str, alt_text: str) -> str:
        """Render portrait image with fallback placeholder.

        Args:
            portrait_path: Portrait filename relative to video_path
            alt_text: Alt text for the image (usually character name)

        Returns:
            HTML string for portrait div
        """
        if not portrait_path:
            return self._render_portrait_placeholder()

        # Resolve path relative to video_path
        video_path = getattr(self, 'video_path', None) or ""
        if video_path:
            full_path = f"{video_path}/{portrait_path}"
        else:
            full_path = portrait_path

        safe_alt = html.escape(str(alt_text))
        safe_path = html.escape(full_path)
        # Use onerror to show placeholder if image fails to load
        placeholder_svg = html.escape(self._get_placeholder_svg())
        return (
            f'<div class="portrait">'
            f'<img src="{safe_path}" alt="{safe_alt}" '
            f'onerror="this.style.display=\'none\';this.parentElement.innerHTML=\'{placeholder_svg}\';" />'
            f'</div>'
        )

    def _render_portrait_placeholder(self) -> str:
        """Render SVG silhouette placeholder."""
        return f'<div class="portrait portrait-placeholder">{self._get_placeholder_svg()}</div>'

    def _render_group_chain(self, groups: list[dict]) -> str:
        """Render consecutive group blocks as a variant chain.
        Groups with conditions -> <<if>>/<<elseif>>
        Group without conditions -> <<else>> (fallback)
        """
        conditional = []
        default = None

        for g in groups:
            g_props = g.get("props") or {}
            conditions = g_props.get("conditions")
            child_blocks = g_props.get("blocks", [])
            if conditions and isinstance(conditions, dict) and conditions.get("items"):
                conditional.append((conditions, child_blocks))
            else:
                default = child_blocks

        # No conditional groups, only default -> render directly
        if not conditional and default is not None:
            return self._convert_blocks_to_game_html(default)

        # No groups at all
        if not conditional and default is None:
            return ""

        # Build <<if>>..<<elseif>>..<<else>>..<</if>> chain
        parts = []
        for idx, (conditions, child_blocks) in enumerate(conditional):
            conditions_json = json.dumps(conditions)
            if idx == 0:
                parts.append(f'<<if setup.triggerConditionsSatisfied({conditions_json})>>')
            else:
                parts.append(f'<<elseif setup.triggerConditionsSatisfied({conditions_json})>>')
            parts.append(self._convert_blocks_to_game_html(child_blocks))

        if default is not None:
            parts.append('<<else>>')
            parts.append(self._convert_blocks_to_game_html(default))

        parts.append('<</if>>')
        return "\n".join(parts)

    def _escape_linkreplace_text(self, text: str) -> str:
        """Escape link text for safe embedding in <<linkreplace "...">>.
        Same escaping the choice path uses (quotes + Twine bracket-link sigils).
        """
        return (text or "").replace('"', '\\"').replace('[', '&#91;').replace(']', '&#93;')

    def _render_cascade(self, cascade_block: dict) -> str:
        """Render a cascade block (S7) — multi-beat linkreplace-drip scene.

        TOML shape:
            { type = "cascade", props = { id = "<id>", beats = [
                { blocks = [...] },                                # beat 0 (always renders on entry, no advance link)
                { advance_text = "...", blocks = [...], effects = [...] },  # subsequent beats
                { advance_text = "...", conditions = {...}, show_when_locked = true,
                  locked_text = "...", blocks = [...] },           # gated beat with locked sibling
                { blocks = [...] },                                # terminal beat (no advance link)
            ] } }

        Output: nested SugarCube <<linkreplace>> macros. Each beat (after the
        opening one) is wrapped in a <<linkreplace "advance_text">> ... <</linkreplace>>;
        gated beats are wrapped in <<if setup.triggerConditionsSatisfied(...)>> with
        an optional <<else>> sibling for the locked variant. Per-beat effects
        fire INSIDE the linkreplace body (via the inline-effect helpers), which
        means they fire on the click that reveals the beat — matching the
        live-verified RTS contract (doc 22 §11 MarcusParkDate Accept click).

        Algorithm: render Beat 0 unconditionally; emit nested cascade tail for
        each subsequent beat. Last beat with no advance_text renders inline
        (no link wrapper) and yields control back to the surrounding context
        (typically the canvas's choice exits).
        """
        if not isinstance(cascade_block, dict):
            return ""
        props = cascade_block.get("props") or {}
        if not isinstance(props, dict):
            return ""
        cascade_id = str(props.get("id") or cascade_block.get("id") or "cascade")
        beats = props.get("beats") or []
        if not isinstance(beats, list) or not beats:
            return ""

        # Author-supplied cascade ids are expected to be unique per project
        # (same convention as flag keys, canvas ids). Beat spans are namespaced
        # under the cascade id for CSS targeting and debugging.
        ns = f"cascade-{cascade_id}"

        # P7 audit fix (2026-05-12) — Pattern C support. Detect whether ANY
        # beat in this cascade has a non-empty `conditions` predicate. If so,
        # this cascade is "gate-fail-risk": a runtime gate failure on any beat
        # terminates the cascade, so exits MUST render at passage bottom (not
        # inside the cascade). Use the SAFE sentinel; the substitution branch
        # at _generate_canvas_node_passages handles SAFE differently (strips
        # without splice + leaves passage_body intact).
        has_gated_beats = any(
            isinstance(b, dict)
            and isinstance(b.get("conditions"), dict)
            and bool(b.get("conditions", {}).get("items"))
            for b in beats
        )
        sentinel_to_use = (
            _CASCADE_EXIT_INJECT_SAFE_SENTINEL if has_gated_beats
            else _CASCADE_EXIT_INJECT_SENTINEL
        )

        # Beat 0 — opens unconditionally on scene entry. No advance link, no gate.
        first_beat = beats[0]
        first_blocks = first_beat.get("blocks") or [] if isinstance(first_beat, dict) else []
        first_html = self._convert_blocks_to_game_html(first_blocks) if first_blocks else ""

        # Find LAST beat with a non-empty advance_text. -1 if cascade has no
        # advance links anywhere (single-beat or all-terminal). The exit-routing
        # sentinel is planted INSIDE that beat's linkreplace body, so exits
        # become visible in the same DOM swap that reveals the terminal beat.
        last_advance_idx = -1
        for j in range(len(beats) - 1, 0, -1):
            bj = beats[j]
            if isinstance(bj, dict) and str(bj.get("advance_text", "")).strip():
                last_advance_idx = j
                break

        tail_html = self._render_cascade_tail(
            ns, cascade_id, beats, idx=1, last_advance_idx=last_advance_idx,
            sentinel_to_use=sentinel_to_use,
        )

        return (
            f'<span id="{ns}-beat-0">'
            f'{first_html}'
            f'{tail_html}'
            f'</span>'
        )

    def _render_cascade_tail(
        self, ns: str, cascade_id: str, beats: list, idx: int,
        last_advance_idx: int = -1,
        sentinel_to_use: str = _CASCADE_EXIT_INJECT_SENTINEL,
    ) -> str:
        """Recursively emit the nested linkreplace chain for beats[idx:].

        Each beat becomes a <<linkreplace "advance_text">> macro whose body
        contains: per-beat effects (script blocks), the beat's content blocks,
        and the recursive tail for the next beat. Gated beats wrap the
        linkreplace in <<if setup.triggerConditionsSatisfied(...)>> with an
        optional <<else>> branch carrying the show_when_locked sibling.

        last_advance_idx: when this matches `idx`, this beat is the LAST
        advance link in the cascade — emit the cascade-exit sentinel inside
        its linkreplace body so the passage assembler can splice the exit
        choices in (cascade-aware exit routing).
        """
        if idx >= len(beats):
            return ""
        beat = beats[idx]
        if not isinstance(beat, dict):
            return self._render_cascade_tail(ns, cascade_id, beats, idx + 1, last_advance_idx)

        advance_text = str(beat.get("advance_text", "")).strip()
        beat_blocks = beat.get("blocks") or []
        beat_conditions = beat.get("conditions")
        beat_effects = beat.get("effects") or []
        beat_flag_effects = beat.get("flagEffects") or []
        show_when_locked = bool(beat.get("show_when_locked", False))
        locked_text = str(beat.get("locked_text", "") or advance_text)
        # S4 — author-supplied threshold-publisher message for the locked sibling.
        locked_text_threshold = str(beat.get("locked_text_threshold", ""))

        # Terminal beat (no advance link): render inline, no wrapper. Yields
        # control to the surrounding context.
        if not advance_text:
            inline_html = self._convert_blocks_to_game_html(beat_blocks) if beat_blocks else ""
            # No further tail beats expected after a terminal — but if the author
            # added beats after, render them inline too (they all become unconditional).
            rest = self._render_cascade_tail(
                ns, cascade_id, beats, idx + 1, last_advance_idx,
                sentinel_to_use=sentinel_to_use,
            )
            return inline_html + rest

        ctx = f"cascade '{cascade_id}' beat {idx}"
        # Effect emission — fires on the click that reveals this beat.
        effect_html = ""
        has_effects = (
            (beat_effects and isinstance(beat_effects, list))
            or (beat_flag_effects and isinstance(beat_flag_effects, list))
        )
        if has_effects:
            effect_html += "<<script>>setup.pendingEffects = [];<</script>>"
            effect_html += self._emit_trait_effects_inline(beat_effects, ctx)
            effect_html += self._emit_flag_effects_inline(beat_flag_effects, ctx)
            effect_html += "<<script>>setup.showEffectNotification();<</script>>"

        # Beat body — content + recursive nested tail.
        body_html = self._convert_blocks_to_game_html(beat_blocks) if beat_blocks else ""
        nested_tail = self._render_cascade_tail(
            ns, cascade_id, beats, idx + 1, last_advance_idx,
            sentinel_to_use=sentinel_to_use,
        )

        # Cascade-aware exit-routing sentinel — only on the LAST advance beat.
        # _generate_canvas_node_passages swaps this for the rendered exit-block
        # HTML so exits are revealed in the same DOM swap as the terminal beat.
        # P7 audit fix: `sentinel_to_use` is SAFE for cascades with gated beats
        # (substitution branch handles SAFE conservatively — strip without splice
        # + leave passage_body intact for bottom-of-passage exits).
        sentinel_html = sentinel_to_use if idx == last_advance_idx else ""

        # Wrap the beat in a span for cascade-aware CSS / debugging affordance.
        # The <span> wraps the entire <<linkreplace>>...<</linkreplace>>, so
        # SugarCube's "cannot find closing tag" issue (split open/close across
        # <<if>>/<<else>>) does not arise here.
        escaped_advance = self._escape_linkreplace_text(advance_text)
        linkreplace_html = (
            f'<span id="{ns}-beat-{idx}">'
            f'<<linkreplace "{escaped_advance}">>'
            f'{effect_html}'
            f'{body_html}'
            f'{nested_tail}'
            f'{sentinel_html}'
            f'<</linkreplace>>'
            f'</span>'
        )

        # If beat is gated, wrap in <<if>> with optional <<else>> locked sibling.
        if isinstance(beat_conditions, dict) and beat_conditions.get("items"):
            try:
                cond_json = json.dumps(beat_conditions)
            except (TypeError, ValueError) as e:
                logger.warning(
                    "Cascade beat %d in '%s' has unserializable conditions: %s. Treating as unconditional.",
                    idx, cascade_id, e
                )
                return linkreplace_html

            gated = f'<<if setup.triggerConditionsSatisfied({cond_json})>>{linkreplace_html}'
            if show_when_locked:
                escaped_locked = self._escape_linkreplace_text(locked_text)
                # Locked sibling: a span styled with `locked-choice` (existing class)
                # carrying a non-clickable label. We do NOT recurse into the
                # locked branch — the cascade ends here for the player who
                # didn't meet the gate. (Mirrors RTS Pattern D Brother
                # rejection variants — terminate the cascade with a short
                # rejection beat.)
                # S4 (2026-05-06) — if locked_text_threshold is set, wrap
                # the label in a <<button>> that fires a threshold-notification
                # toast on click. Same mechanism as the choice-path S4 (RTS
                # <<NotifyCorruption N>> pattern, doc 13 §7.4 + doc 22 §11).
                if locked_text_threshold:
                    escaped_threshold = self._escape_linkreplace_text(locked_text_threshold)
                    locked_html = (
                        f'<span class="locked-choice" title="{escaped_locked}">'
                        f'<<button "{escaped_locked}">>'
                        f'<<run setup.queueGatedNotification("{escaped_threshold}")>>'
                        f'<<run setup.showEffectNotification()>>'
                        f'<</button>>'
                        f'</span>'
                    )
                else:
                    locked_html = (
                        f'<span class="locked-choice" title="{escaped_locked}">{escaped_locked}</span>'
                    )
                gated += f'<<else>>{locked_html}'
            gated += '<</if>>'
            return gated

        return linkreplace_html

    def _resolve_at_references(self, text: str) -> str:
        """Replace @player and @npc_short references with SugarCube <<print>> macros.

        For use in passage body content (paragraphs, headings, dialog).
        Do NOT use for <<link>> text — use _resolve_at_references_expr() instead.

        Examples:
            @player          → <<print $player.name>>
            @player.body_type → <<print $player.body_type || "">>
            @ethan           → <<print $npcs["uuid"].name>>
            @ethan.rel       → <<print $npcs["uuid"].relationship || "">>
            @unknown         → @unknown  (unmatched, left as-is)
        """
        if not text or '@' not in text:
            return text

        import re

        slug_map = getattr(self, 'npc_slug_map', {})

        def _replacer(match):
            ref = match.group(1)  # e.g., "ethan" or "ethan.rel" or "player.body_type"
            if '.' in ref:
                short_name, field = ref.split('.', 1)
            else:
                short_name, field = ref, 'name'

            # Handle @player references
            if short_name == 'player':
                if field == 'name':
                    return '<<print $player.name>>'
                else:
                    return f'<<print $player.{field} || "">>'

            # Handle @npc references: @ethan → npc_ethan → uuid
            slug = f"npc_{short_name}" if not short_name.startswith("npc_") else short_name
            uuid = slug_map.get(slug) or slug_map.get(short_name)
            if not uuid:
                return match.group(0)  # Not a known NPC, leave as-is

            if field == 'rel':
                return f'<<print $npcs["{uuid}"].relationship || "">>'
            else:
                return f'<<print $npcs["{uuid}"].name>>'

        return re.sub(r'@(\w+(?:\.\w+)?)', _replacer, text)

    def _resolve_at_references_expr(self, text: str):
        """Resolve @player and @npc references in text for use inside <<link>> expressions.

        Returns (resolved_text, has_dynamic) tuple.
        - If no @ refs found: returns (original_text, False) — use as quoted string
        - If @ refs found: returns (js_expression, True) — use with backtick syntax

        SugarCube <<link>> doesn't support <<print>> macros in quoted text.
        Instead, we build a JS string concatenation expression for backtick eval:
            "Chat with @alex" → '"Chat with " + $npcs["uuid"].name', True
        """
        if not text or '@' not in text:
            return text, False

        import re

        slug_map = getattr(self, 'npc_slug_map', {})
        has_dynamic = False

        # Split text by @ references, building JS expression parts
        parts = []
        last_end = 0

        for match in re.finditer(r'@(\w+(?:\.\w+)?)', text):
            ref = match.group(1)
            if '.' in ref:
                short_name, field = ref.split('.', 1)
            else:
                short_name, field = ref, 'name'

            # Handle @player references
            if short_name == 'player':
                has_dynamic = True
                literal = text[last_end:match.start()]
                if literal:
                    parts.append(f'"{literal}"')
                if field == 'name':
                    parts.append('$player.name')
                else:
                    parts.append(f'($player.{field} || "")')
                last_end = match.end()
                continue

            # Handle @npc references
            slug = f"npc_{short_name}" if not short_name.startswith("npc_") else short_name
            uuid = slug_map.get(slug) or slug_map.get(short_name)
            if not uuid:
                continue  # Not a known NPC, skip

            has_dynamic = True
            literal = text[last_end:match.start()]
            if literal:
                parts.append(f'"{literal}"')
            if field == 'rel':
                parts.append(f'($npcs["{uuid}"].relationship || "")')
            else:
                parts.append(f'$npcs["{uuid}"].name')
            last_end = match.end()

        if not has_dynamic:
            return text, False

        # Add trailing literal text
        trailing = text[last_end:]
        if trailing:
            parts.append(f'"{trailing}"')

        return ' + '.join(parts), True

    def _convert_blocks_to_game_html(self, blocks: list[dict]) -> str:
        """
        Convert BlockNote blocks to basic HTML for SugarCube games.
        Handles group blocks as variant chains (consecutive groups form
        <<if>>..<<elseif>>..<<else>>..<</if>> structures).

        Args:
            blocks: List of BlockNote block dictionaries

        Returns:
            Basic HTML string without CSS classes
        """
        if not blocks:
            logger.warning("Empty blocks provided for HTML conversion")
            return "<p><em>No content</em></p>"

        try:
            html_parts = []
            i = 0

            while i < len(blocks):
                block = blocks[i]
                block_type = (block.get("type") or "").strip()

                # Collect consecutive group blocks into a variant chain
                if block_type == "group":
                    group_chain = []
                    while i < len(blocks) and (blocks[i].get("type") or "").strip() == "group":
                        group_chain.append(blocks[i])
                        i += 1
                    chain_html = self._render_group_chain(group_chain)
                    if chain_html:
                        html_parts.append(chain_html)
                    continue

                # Random content pool — pick one block each render
                if block_type == "block_pool":
                    pool_blocks = (block.get("props") or {}).get("blocks", [])
                    if pool_blocks and isinstance(pool_blocks, list):
                        if len(pool_blocks) == 1:
                            # Single item — render directly, no random
                            html_parts.append(self._convert_blocks_to_game_html(pool_blocks))
                        else:
                            max_idx = len(pool_blocks) - 1
                            parts = [f'<<set _bp to random(0, {max_idx})>>']
                            for pi, pool_item in enumerate(pool_blocks):
                                if pi == 0:
                                    parts.append('<<if _bp is 0>>')
                                elif pi < max_idx:
                                    parts.append(f'<<elseif _bp is {pi}>>')
                                else:
                                    parts.append('<<else>>')
                                parts.append(self._convert_blocks_to_game_html([pool_item]))
                            parts.append('<</if>>')
                            html_parts.append('\n'.join(parts))
                    i += 1
                    continue

                # S7 — multi-beat linkreplace cascade. Renders Beat 0
                # unconditionally + nested <<linkreplace>> chain for the
                # remaining beats. Per-beat effects fire on click, gates can
                # appear at any beat, terminal beats yield to choice exits.
                if block_type == "cascade":
                    cascade_html = self._render_cascade(block)
                    if cascade_html:
                        html_parts.append(cascade_html)
                    i += 1
                    continue

                i += 1
                props = block.get("props", {}) or {}

                # Media blocks: render even if text content is empty
                if block_type == "image":
                    # ─── Image pool: CYCLES through the stills ──────────────────
                    # Two shapes, `pool_dir` (a folder, contents from disk) winning
                    # over `files` (an explicit list) winning over `file` — the
                    # precedence lives in apps/common/media_blocks.py. A partial
                    # pool cycles over whatever resolved; an empty one falls
                    # through to the debug placeholder. See _render_media_pool for
                    # why this cycles rather than picking at random.
                    pool_spec = block_media_pool(props)
                    image_files = props.get("files")

                    if pool_spec is not None:
                        resolved = self._resolve_pool_dir(pool_spec["dir"])
                        pool_html = self._render_media_pool(
                            props, resolved, 'image', pool_dir=pool_spec["dir"]
                        )
                        label = f'{pool_spec["dir"]}/ (0 of {pool_spec["target"]})'
                    elif isinstance(image_files, list) and len(image_files) > 0 and all(isinstance(f, str) for f in image_files):
                        pool_html = self._render_media_pool(props, image_files, 'image')
                        label = f'{str(image_files[0]).replace(chr(92), "/")} ({len(image_files)} files)'
                    else:
                        pool_html = None
                        label = None

                    if label is not None:
                        if pool_html is None:
                            placeholder = self._pool_missing_placeholder(props, label, 'image')
                            if placeholder:
                                html_parts.append(placeholder)
                            continue

                        # 1+ pool files found. The caption wraps the whole cycle
                        # chain so the figcaption renders once, not once per branch.
                        caption_pool = html.escape(str(props.get("caption", "")))
                        if caption_pool:
                            html_parts.append(
                                f'<figure style="margin:10px 0;">{pool_html}'
                                f'<figcaption style="font-size:12px;color:#6b7280;margin-top:4px;">{caption_pool}</figcaption>'
                                f'</figure>'
                            )
                        else:
                            html_parts.append(pool_html)
                        continue

                    image_file = props.get("file")  # File-based image
                    image_url = props.get("url")    # URL-based image

                    media_src = None
                    is_image_format = True  # Default to image tag

                    if image_file:
                        # File-based image from --video-path folder
                        image_file_normalized = str(image_file).replace('\\', '/')

                        # Extension-agnostic file matching
                        actual_path, actual_ext = self._find_media_file(image_file_normalized)

                        if actual_path is None:
                            # File not found in media folder
                            # Collect for Missing Media Page
                            image_desc = props.get("description", "") or props.get("alt", "")
                            self.missing_media.append({
                                'file': image_file_normalized,
                                'type': 'image',
                                'description': image_desc,
                                'search_queries': props.get("search_queries", []),
                                'canvas_id': self.current_canvas_id or 'unknown',
                                'category': self._categorize_media(self.current_canvas_id or '', image_file_normalized),
                            })

                            if self.debug:

                                # Show placeholder with dashed border
                                placeholder = (
                                    f'<div style="border:2px dashed #666;padding:20px;'
                                    f'margin:10px 0;border-radius:8px;background:#f5f5f5;">'
                                    f'<p style="margin:0;font-weight:bold;color:#333;">'
                                    f'[IMAGE MISSING] {html.escape(image_file_normalized)}</p>'
                                )
                                if image_desc:
                                    placeholder += (
                                        f'<p style="margin:5px 0 0;color:#666;font-style:italic;">'
                                        f'{html.escape(image_desc)}</p>'
                                    )
                                # Add search links if search_queries provided
                                search_queries = props.get("search_queries", [])
                                if search_queries and isinstance(search_queries, list):
                                    # Get game folder name from options or derive from project name
                                    game_name = self.options.get("game_folder") or self._slugify(self.project.name)
                                    scene_path = image_file_normalized

                                    placeholder += '<div style="margin-top:10px;">'
                                    for query in search_queries:
                                        if query and isinstance(query, str):
                                            search_url = self._build_search_url(query.strip(), game_name, scene_path)
                                            placeholder += (
                                                f'<a href="{html.escape(search_url)}" target="_blank" '
                                                f'style="display:inline-block;margin:4px 8px 4px 0;'
                                                f'padding:6px 12px;background:#3b82f6;color:white;'
                                                f'text-decoration:none;border-radius:4px;font-size:13px;">'
                                                f'🔍 {html.escape(query.strip())}</a>'
                                            )
                                    placeholder += '</div>'
                                placeholder += '</div>'
                                html_parts.append(placeholder)
                            # else: skip silently (default behavior)
                            continue

                        # Determine if actual file is image or video format
                        is_image_format = self._is_image_extension(actual_ext)

                        # Track for packaging based on actual file type
                        if is_image_format:
                            self.used_assets['external_images'].add(actual_path)
                        else:
                            self.used_assets['external_videos'].add(actual_path)

                        # Generate media source path
                        if self.video_path:
                            # Direct path mode - use provided path prefix
                            base = self.video_path.rstrip('/')
                            media_src = f"{base}/{html.escape(actual_path)}"
                        else:
                            # Copy mode - use relative media path
                            subfolder = "images" if is_image_format else "videos"
                            media_src = f"media/{subfolder}/{html.escape(actual_path)}"

                    elif image_url:
                        # URL-based image (existing behavior)
                        media_src = html.escape(str(image_url))
                    else:
                        # No file or URL, skip
                        continue

                    alt = html.escape(str(props.get("alt", "")))
                    caption = html.escape(str(props.get("caption", "")))

                    # Render appropriate tag based on actual file type
                    if is_image_format:
                        media_tag = (
                            f'<img src="{media_src}" alt="{alt}" loading="lazy" decoding="async" '
                            f'style="max-width:100%;max-height:70vh;object-fit:contain;height:auto;border-radius:8px;" />'
                        )
                    else:
                        # Render as video (if a video file was downloaded for an image block)
                        media_tag = (
                            f'<video src="{media_src}" autoplay muted loop playsinline controls preload="metadata" '
                            f'style="max-width:100%;max-height:70vh;object-fit:contain;height:auto;border-radius:8px;"></video>'
                        )

                    if caption and is_image_format:
                        html_parts.append(
                            f'<figure style="margin:10px 0;">{media_tag}'
                            f'<figcaption style="font-size:12px;color:#6b7280;margin-top:4px;">{caption}</figcaption>'
                            f'</figure>'
                        )
                    else:
                        html_parts.append(media_tag)
                    continue

                if block_type == "video":
                    video_file = props.get("file")       # File-based video
                    video_url = props.get("url")         # URL-based video
                    video_desc = props.get("description", "")  # Description for debug

                    # ─── Clip pool: CYCLES through the clips ────────────────────
                    # One description and one `search_queries` set covering N
                    # clips, so find-media searches ONCE and keeps the gate-
                    # survivors it already paid to judge. `pool_dir` (a folder)
                    # wins over `files` wins over `file`.
                    #
                    # This is why `block_pool` of N video blocks is the wrong shape
                    # for replay variety: N blocks means N descriptions and N
                    # searches for a single beat.
                    pool_spec = block_media_pool(props)
                    video_files = props.get("files")

                    if pool_spec is not None:
                        resolved = self._resolve_pool_dir(pool_spec["dir"])
                        pool_html = self._render_media_pool(
                            props, resolved, 'video', pool_dir=pool_spec["dir"]
                        )
                        label = f'{pool_spec["dir"]}/ (0 of {pool_spec["target"]})'
                    elif isinstance(video_files, list) and len(video_files) > 0 and all(isinstance(f, str) for f in video_files):
                        pool_html = self._render_media_pool(props, video_files, 'video')
                        label = f'{str(video_files[0]).replace(chr(92), "/")} ({len(video_files)} files)'
                    else:
                        pool_html = None
                        label = None

                    if label is not None:
                        if pool_html is None:
                            placeholder = self._pool_missing_placeholder(props, label, 'video')
                            if placeholder:
                                html_parts.append(placeholder)
                            continue

                        html_parts.append(pool_html)
                        continue

                    media_src = None
                    is_video_format = True  # Default to video tag

                    if video_file:
                        # File-based video from --video-folder
                        # Normalize path separators
                        video_file_normalized = str(video_file).replace('\\', '/')

                        # Extension-agnostic file matching
                        actual_path, actual_ext = self._find_media_file(video_file_normalized)

                        if actual_path is None:
                            # File not found in video folder
                            # Collect for Missing Media Page
                            self.missing_media.append({
                                'file': video_file_normalized,
                                'type': 'video',
                                'description': video_desc,
                                'search_queries': props.get("search_queries", []),
                                'canvas_id': self.current_canvas_id or 'unknown',
                                'category': self._categorize_media(self.current_canvas_id or '', video_file_normalized),
                            })

                            if self.debug:
                                # Render placeholder block with dashed border
                                placeholder = (
                                    f'<div style="border:2px dashed #666;padding:20px;'
                                    f'margin:10px 0;border-radius:8px;background:#f5f5f5;">'
                                    f'<p style="margin:0;font-weight:bold;color:#333;">'
                                    f'[VIDEO MISSING] {html.escape(video_file_normalized)}</p>'
                                )
                                if video_desc:
                                    placeholder += (
                                        f'<p style="margin:5px 0 0;color:#666;font-style:italic;">'
                                        f'{html.escape(video_desc)}</p>'
                                    )
                                # Add search links if search_queries provided
                                search_queries = props.get("search_queries", [])
                                if search_queries and isinstance(search_queries, list):
                                    # Get game folder name from options or derive from project name
                                    game_name = self.options.get("game_folder") or self._slugify(self.project.name)
                                    scene_path = video_file_normalized

                                    placeholder += '<div style="margin-top:10px;">'
                                    for query in search_queries:
                                        if query and isinstance(query, str):
                                            search_url = self._build_search_url(query.strip(), game_name, scene_path)
                                            placeholder += (
                                                f'<a href="{html.escape(search_url)}" target="_blank" '
                                                f'style="display:inline-block;margin:4px 8px 4px 0;'
                                                f'padding:6px 12px;background:#3b82f6;color:white;'
                                                f'text-decoration:none;border-radius:4px;font-size:13px;">'
                                                f'🔍 {html.escape(query.strip())}</a>'
                                            )
                                    placeholder += '</div>'
                                placeholder += '</div>'
                                html_parts.append(placeholder)
                            # else: skip silently (default behavior)
                            continue

                        # Determine if actual file is video or image format
                        is_video_format = self._is_video_extension(actual_ext)

                        # Track for packaging based on actual file type
                        if is_video_format:
                            self.used_assets['external_videos'].add(actual_path)
                        else:
                            self.used_assets['external_images'].add(actual_path)

                        # Generate media source path
                        if self.video_path:
                            # Direct path mode - use provided path prefix (no copy)
                            base = self.video_path.rstrip('/')
                            media_src = f"{base}/{html.escape(actual_path)}"
                        else:
                            # Copy mode - use relative media path
                            subfolder = "videos" if is_video_format else "images"
                            media_src = f"media/{subfolder}/{html.escape(actual_path)}"

                    elif video_url:
                        # URL-based video (existing behavior)
                        media_src = html.escape(str(video_url))
                    else:
                        # No file or URL, skip
                        continue

                    # Render appropriate tag based on actual file type
                    if is_video_format:
                        poster = html.escape(str(props.get("poster", ""))) if props.get("poster") else ""
                        poster_attr = f' poster="{poster}"' if poster else ""
                        # Do not autoplay by default; always include controls
                        media_tag = (
                            f'<video src="{media_src}" autoplay muted loop playsinline controls preload="metadata"{poster_attr} '
                            f'style="max-width:100%;max-height:70vh;object-fit:contain;height:auto;border-radius:8px;"></video>'
                        )
                    else:
                        # Render as image (for GIFs downloaded instead of video)
                        alt_text = html.escape(video_desc) if video_desc else ""
                        media_tag = (
                            f'<img src="{media_src}" alt="{alt_text}" '
                            f'style="max-width:100%;max-height:70vh;object-fit:contain;height:auto;border-radius:8px;" />'
                        )
                    html_parts.append(media_tag)
                    continue

                # Handle clip blocks
                if block_type == "clip":
                    clip_id = props.get("clipId")
                    if not clip_id:
                        # No clipId, skip silently
                        continue

                    # Lookup in pre-loaded map (O(1), no database query)
                    clip = self.clips_by_id.get(str(clip_id))
                    if not clip:
                        # Clip not found or not accessible (wrong owner, deleted, etc.)
                        logger.warning(
                            f"Clip {clip_id} not accessible for rendering",
                            extra={
                                "project_id": str(self.project.id),
                                "clip_id": clip_id
                            }
                        )
                        continue

                    # Get file URL (required)
                    clip_url = clip.file_url if hasattr(clip, 'file_url') else ""
                    if not clip_url:
                        logger.warning(
                            f"Clip {clip_id} has no file URL",
                            extra={"project_id": str(self.project.id), "clip_id": clip_id}
                        )
                        continue

                    # Track asset usage - clip is valid and will be rendered
                    self.used_assets['clips'].add(str(clip.id))
                    if hasattr(clip, 'video') and clip.video:
                        self.used_assets['videos'].add(str(clip.video.id))

                    # Get poster URL (optional)
                    poster_url = clip.poster_url if hasattr(clip, 'poster_url') else None
                    if poster_url:
                        self.used_assets['images'].add(poster_url)
                    poster_attr = f' poster="{html.escape(poster_url)}"' if poster_url else ""

                    # Render HTML5 video element
                    clip_tag = (
                        f'<video src="{html.escape(clip_url)}" autoplay muted loop playsinline controls preload="metadata"{poster_attr} '
                        f'style="max-width:100%;max-height:70vh;object-fit:contain;height:auto;border-radius:8px;"></video>'
                    )
                    html_parts.append(clip_tag)
                    continue

                # Text/dialog blocks: require content
                content = str(block.get("content", "")).strip()
                if not content:
                    continue
                # Resolve @npc references (e.g., @ethan → <<print $npcs["uuid"].name>>)
                content = self._resolve_at_references(content)
                # Convert *italic* markers to <em> (SugarCube wiki markup doesn't work inside HTML tags)
                content = re.sub(r'(?<!\w)\*([^*]+)\*(?!\w)', r'<em>\1</em>', content)

                if block_type == "heading":
                    level = block.get("props", {}).get("level", 1)
                    html_parts.append(f"<h{level}>{content}</h{level}>")
                elif block_type == "paragraph":
                    html_parts.append(f"<p>{content}</p>")
                elif block_type == "dialog":
                    # Handle dialog blocks with speaker attribution and portraits
                    speaker = props.get("speaker", "npc")

                    if speaker == "player":
                        # Player dialog with portrait support. The label follows the
                        # game's narration_person so it agrees with the prose around it.
                        player_label, _, alt_label = self._get_player_speech_labels()
                        player_portrait = getattr(self, 'player_portrait', '') or ''
                        # Unguarded: _render_portrait("") returns the SVG silhouette, so the
                        # speaker column is never visually empty. The old `if portrait else ''`
                        # guard left a hole in the column for anyone without art.
                        portrait_html = self._render_portrait(player_portrait, alt_label)
                        # No role on the player, so the NAME carries the colon and the line
                        # runs straight on from it. `dlg-inline` is what keeps the name on
                        # the speech's own line instead of a row of its own.
                        html_parts.append(
                            f'<div class="dialog-block dialog-player">'
                            f'{portrait_html}'
                            f'<div class="dialog-content">'
                            f'<strong class="dlg-inline">{player_label}</strong> {content}'
                            f'</div>'
                            f'</div>'
                        )
                    elif speaker == "unknown":
                        # A stranger still gets a face, so the block keeps its shape next to
                        # named lines. No role: nobody knows it, so the name takes the colon.
                        html_parts.append(
                            f'<div class="dialog-block dialog-npc">'
                            f'{self._render_portrait("", "Stranger")}'
                            f'<div class="dialog-content">'
                            f'<strong class="dlg-inline">Stranger</strong> {content}'
                            f'</div>'
                            f'</div>'
                        )
                    else:
                        # NPC dialog with portrait support
                        npc_id = props.get("npcId", "")
                        npc_uuid = getattr(self, 'npc_slug_map', {}).get(npc_id, npc_id)
                        npc_data = getattr(self, 'npc_map', {}).get(npc_uuid, {})
                        npc_name = npc_data.get("name") if npc_data else None
                        npc_portrait = npc_data.get("portrait", "") if npc_data else ""
                        # Fallback: convert slug to title case (npc_ethan → Ethan)
                        if not npc_name:
                            npc_name = npc_id.replace("npc_", "").replace("_", " ").title() or "NPC"
                        portrait_html = self._render_portrait(npc_portrait, npc_name)
                        # For customizable NPCs, use runtime name from $npcs
                        if npc_data and npc_data.get("customizable") and npc_uuid:
                            speaker_html = f'<<print $npcs["{npc_uuid}"].name>>'
                        else:
                            speaker_html = html.escape(str(npc_name))
                        # F10 — the short label under the NAME. `relationship` is a
                        # cast-page sentence and repeats across a cast (five of one
                        # game's six contain "husband"); `role` is authored to be
                        # unique and validate() refuses duplicates. Absent = no line,
                        # and the box renders exactly as it did before this existed.
                        npc_role = (npc_data.get("role") or "").strip() if npc_data else ""
                        # Whichever of the two comes LAST carries the colon, and the speech
                        # runs straight on from it:
                        #     with a role     Dorn
                        #                     husband: Back Friday. Late.
                        #     without one     Dorn: Back Friday. Late.
                        # `dlg-inline` is the no-role case, where the name must not take a
                        # row of its own. The colon itself is added in CSS, so the role text
                        # stays clean for anything that reads it.
                        if npc_role:
                            name_html = f'<strong>{speaker_html}</strong>'
                            role_html = (
                                f'<span class="dialog-role">{html.escape(npc_role)}</span>')
                        else:
                            name_html = f'<strong class="dlg-inline">{speaker_html}</strong>'
                            role_html = ''
                        html_parts.append(
                            f'<div class="dialog-block dialog-npc">'
                            f'{portrait_html}'
                            f'<div class="dialog-content">'
                            f'{name_html}{role_html} {content}'
                            f'</div>'
                            f'</div>'
                        )
                elif block_type == "thought_bubble":
                    # NPC / player interior thought bubble (S8 — bundled with S7
                    # cascade work 2026-05-06 per doc 22 §11 live verification:
                    # thought bubbles paired naturally with cascade beats in
                    # BrotherBedroomSex1 / BedroomSleepDadScene). Reuses the
                    # dialog speaker resolution; renders as an italic bubble
                    # distinct from speech (💭 glyph, dashed border, muted color).
                    speaker = props.get("speaker", "npc")
                    if speaker == "player":
                        _, thought_label, alt_label = self._get_player_speech_labels()
                        player_portrait = getattr(self, 'player_portrait', '') or ''
                        portrait_html = self._render_portrait(player_portrait, alt_label) if player_portrait else ''
                        html_parts.append(
                            f'<div class="thought-bubble thought-bubble-player">'
                            f'{portrait_html}'
                            f'<div class="thought-bubble-content">'
                            f'<em>{thought_label}</em> {content}'
                            f'</div></div>'
                        )
                    elif speaker == "unknown" or not speaker.startswith(("npc_", "npc")):
                        html_parts.append(
                            f'<div class="thought-bubble thought-bubble-npc">'
                            f'<div class="thought-bubble-content">'
                            f'<em>💭 Someone is thinking:</em> {content}'
                            f'</div></div>'
                        )
                    else:
                        npc_id = props.get("npcId") or speaker
                        npc_uuid = getattr(self, 'npc_slug_map', {}).get(npc_id, npc_id)
                        npc_data = getattr(self, 'npc_map', {}).get(npc_uuid, {})
                        npc_name = npc_data.get("name") if npc_data else None
                        npc_portrait = npc_data.get("portrait", "") if npc_data else ""
                        if not npc_name:
                            npc_name = npc_id.replace("npc_", "").replace("_", " ").title() or "NPC"
                        portrait_html = self._render_portrait(npc_portrait, npc_name) if npc_portrait else ''
                        if npc_data and npc_data.get("customizable") and npc_uuid:
                            speaker_html = f'<<print $npcs["{npc_uuid}"].name>>'
                        else:
                            speaker_html = html.escape(str(npc_name))
                        html_parts.append(
                            f'<div class="thought-bubble thought-bubble-npc">'
                            f'{portrait_html}'
                            f'<div class="thought-bubble-content">'
                            f'<em>💭 {speaker_html} is thinking:</em> {content}'
                            f'</div></div>'
                        )
                else:
                    # Fallback to paragraph for unknown types. Warn loudly — an
                    # unrecognized block type means authored content (e.g. a
                    # mistyped "dialogue"/"speech" dialog block) silently loses its
                    # speaker/structure here. The importer hard-fails on this, but
                    # other entry points (e.g. the editor) reach this path too.
                    logger.warning(
                        "Unknown block type %r — rendering as plain paragraph; "
                        "speaker/structure lost. Recognized: heading, paragraph, "
                        "dialog, thought_bubble, image, video, cascade, group, "
                        "block_pool, clip.",
                        block_type,
                    )
                    html_parts.append(f"<p>{content}</p>")

            result = "".join(html_parts)

            if not result:
                logger.warning("All blocks were empty after processing")
                return "<p><em>No content</em></p>"

            return result

        except (KeyError, TypeError, AttributeError, ValueError) as e:
            logger.error(f"Error converting blocks to game HTML: {e}", extra={
                "blocks_count": len(blocks) if blocks else 0,
                "error": str(e)
            })
            raise ValueError(f"Failed to convert BlockNote content to HTML: {e}") from e

    def _get_quests_block(self) -> str:
        # PRD 48 — Return the Quests page block (passage + dependencies).
        #
        # Dispatches on `project.metadata["quests_engine"]`:
        #   - "v2"  → V2 overlay: 6 new JS functions + widget + CSS + V2 passage
        #   - else  → V1 inline (byte-identical to pre-PRD-48 emission)
        #
        # Spliced into the inline emission via concatenation inside
        # _generate_time_system. Docstring uses '#' comments instead of a
        # docstring because the body references the literal '\"\"\"' token,
        # which Python triple-quoted docstrings cannot contain.
        if (self.project.metadata or {}).get("quests_engine") == "v2":
            return self._quests_v2_overlay()
        return self._quests_v1_block()

    def _quests_v1_block(self) -> str:
        """The unchanged V1 QuestsPage passage. Byte-identical to what was
        inline at v2.py:16077-16112 before the PRD 48 refactor — preserved
        as a string so games on the V1 engine emit exactly the same HTML.
        """
        return """:: QuestsPage
<<nobr>>
<h2>What's Next</h2>
<<set _helpData = setup.help_data || {}>>
<<set _hasNpcs = _helpData.npcs && Object.keys(_helpData.npcs).length > 0>>

/* Quests cards = narrative line only. Game-level mechanics (decay rates,
   time costs, what affects diner tips, etc.) live on :: TipsPage instead.
   The picker swaps which narrative line fires based on state. */

<<set _globals = setup.getGlobalHints()>>
<<if _globals.length > 0>>
  <div class="npc-section">
    <h3 class="npc-name">Story Goals</h3>
    <<for _g range _globals>><<renderStageHint _g>><</for>>
  </div>
<</if>>

<<if _hasNpcs>>
  <<for _npcId, _npcData range _helpData.npcs>>
    <<set _slug = setup.npcSlugForId(_npcId)>>
    <<set _hint = _slug ? setup.getStageHintForNPC(_slug) : null>>
    <<if _hint>>
      <div class="npc-section">
        <h3 class="npc-name"><<print ($npcs[_npcId] && $npcs[_npcId].name) || _npcData.name>></h3>
        <<renderStageHint _hint>>
      </div>
    <</if>>
  <</for>>
<</if>>

<<if _globals.length === 0 && !_hasNpcs>>
  <div class="no-quests">No active quests.</div>
<</if>>
<</nobr>>
<<link "← Back">><<run setup.smartBack()>><</link>>
"""

    def _quests_v2_overlay(self) -> str:
        """PRD 48 — The V2 Quests Engine overlay. Replaces the V1 QuestsPage
        with the new author-on-template engine. Emitted only when
        `project.metadata["quests_engine"] == "v2"`.

        Contents (in order):
          1. `:: QuestsV2Script [script]` — six new setup.* functions
          2. `:: QuestsV2Widgets [widget nobr]` — <<renderQuestsCard>>
          3. `:: QuestsV2Styles [stylesheet]` — .quests-* CSS
          4. `:: QuestsPage` — the V2 passage (replaces V1's same-named passage)

        Reuses utilities from V1 emission untouched: `setup._formatCanvasSchedule`,
        `setup._locNameFromUuid`, `setup.npcSlugForId`, `setup.npc_slug_map`,
        `setup.help_data.locationCanvases`.
        """
        return """:: QuestsV2Script [script]
// PRD 48 — Quests Engine V2. Single-path renderer driven by author-on-template
// goals arrays. Reads from setup.quests_cards (serialized at build time).

(function() {

// _whenMatches — private helper. True iff every routing condition matches.
function _whenMatches(items) {
    for (var i = 0; i < items.length; i++) {
        try {
            if (!setup.checkQuestsCondition(items[i])) return false;
        } catch (e) {
            return false;
        }
    }
    return true;
}

// _readCurrentValue — for trait/counter goals, the live numeric value (used
// for the bullet's "X / Y" suffix). Returns null for flag-only goals.
function _readCurrentValue(item) {
    if (!item || !item.trait) return null;
    if (item.subject === "player") {
        var pt = State.variables.player && State.variables.player.core_traits;
        return (pt && typeof pt[item.trait] === "number") ? pt[item.trait] : 0;
    }
    if (item.subject === "npc") {
        var slugMap = setup.npc_slug_map || {};
        var uuid = slugMap[item.npc_id] || item.npc_id;
        var npc = State.variables.npcs && State.variables.npcs[uuid];
        var nt = npc && npc.core_traits;
        return (nt && typeof nt[item.trait] === "number") ? nt[item.trait] : 0;
    }
    return null;
}

// ── Picker: NPC arc card ─────────────────────────────────────────────
// Returns the highest-priority quest_card with matching npc_id and all
// `when` conditions met. Sort: priority desc, when-length desc, file-order asc.
setup.pickQuestsCard = function(npcSlug) {
    if (!npcSlug) return null;
    var cards = setup.quests_cards || [];
    var matches = [];
    for (var i = 0; i < cards.length; i++) {
        var c = cards[i];
        if (!c || c.npc_id !== npcSlug) continue;
        if (!_whenMatches(c.when || [])) continue;
        matches.push({ card: c, fileIndex: i });
    }
    if (matches.length === 0) return null;
    matches.sort(function(a, b) {
        var pa = a.card.priority || 0, pb = b.card.priority || 0;
        if (pb !== pa) return pb - pa;
        var la = (a.card.when || []).length, lb = (b.card.when || []).length;
        if (lb !== la) return lb - la;
        return a.fileIndex - b.fileIndex;
    });
    return matches[0].card;
};

// ── Picker: Story Goals (multiple cards) ─────────────────────────────
// Returns ALL matching cards with no npc_id. Cards sharing a `group` value
// collapse to one winner (the highest-priority match in that group). Output
// is in original file order.
setup.pickQuestsCards = function(scope) {
    if (scope !== "story_goals") return [];
    var cards = setup.quests_cards || [];
    var matches = [];
    for (var i = 0; i < cards.length; i++) {
        var c = cards[i];
        if (!c || c.npc_id) continue;
        if (!_whenMatches(c.when || [])) continue;
        matches.push({ card: c, fileIndex: i });
    }
    if (matches.length === 0) return [];
    var groups = {};
    var groupOrder = [];
    for (var k = 0; k < matches.length; k++) {
        var key = matches[k].card.group || ("__idx_" + matches[k].fileIndex);
        if (!groups[key]) {
            groups[key] = [];
            groupOrder.push({ key: key, firstIdx: matches[k].fileIndex });
        }
        groups[key].push(matches[k]);
    }
    var winners = [];
    for (var gi = 0; gi < groupOrder.length; gi++) {
        var arr = groups[groupOrder[gi].key];
        arr.sort(function(a, b) {
            var pa = a.card.priority || 0, pb = b.card.priority || 0;
            if (pb !== pa) return pb - pa;
            var la = (a.card.when || []).length, lb = (b.card.when || []).length;
            if (lb !== la) return lb - la;
            return a.fileIndex - b.fileIndex;
        });
        winners.push({ card: arr[0].card, firstIdx: groupOrder[gi].firstIdx });
    }
    winners.sort(function(a, b) { return a.firstIdx - b.firstIdx; });
    return winners.map(function(w) { return w.card; });
};

// ── Gate evaluator (new flat shape) ──────────────────────────────────
// Items are `{ flag, op }` for flags or `{ trait, subject, op, value }` for
// traits/counters. Returns true/false. Used by `_whenMatches` (routing) and
// by `evaluateGoals` (bullet progress).
setup.checkQuestsCondition = function(item) {
    if (!item || typeof item !== "object") return false;
    if (item.flag) {
        var v = State.variables.flags && State.variables.flags[item.flag] === true;
        if (item.op === "is_true") return !!v;
        if (item.op === "is_false") return !v;
        return false;
    }
    if (item.trait) {
        var current;
        if (item.subject === "player") {
            var pt = State.variables.player && State.variables.player.core_traits;
            current = (pt && typeof pt[item.trait] === "number") ? pt[item.trait] : 0;
        } else if (item.subject === "npc") {
            var slugMap = setup.npc_slug_map || {};
            var uuid = slugMap[item.npc_id] || item.npc_id;
            var npc = State.variables.npcs && State.variables.npcs[uuid];
            var nt = npc && npc.core_traits;
            current = (nt && typeof nt[item.trait] === "number") ? nt[item.trait] : 0;
        } else {
            return false;
        }
        var target = item.value;
        switch (item.op) {
            case "gte": return current >= target;
            case "lte": return current <= target;
            case "gt":  return current > target;
            case "lt":  return current < target;
            case "eq":  return current === target;
        }
        return false;
    }
    return false;
};

// ── Goal evaluator ───────────────────────────────────────────────────
// Walks card.goals; for each item, evaluates and reads live value.
// Empty goals → allMet vacuously true (cards with only routing-flag gates).
setup.evaluateGoals = function(card) {
    if (!card || !card.goals || card.goals.length === 0) {
        return { allMet: true, items: [] };
    }
    var items = [];
    var allMet = true;
    for (var i = 0; i < card.goals.length; i++) {
        var g = card.goals[i];
        var met = false;
        try { met = setup.checkQuestsCondition(g); } catch (e) {}
        var current = _readCurrentValue(g);
        items.push({ goal: g, currentValue: current, met: met });
        if (!met) allMet = false;
    }
    return { allMet: allMet, items: items };
};

// ── Canvas lookup by slug ────────────────────────────────────────────
// Used by renderQuestsGoalBlock to surface ready_canvas's location + schedule
// on the 🔓 Ready frame. The TOML-level slug (e.g. "scene_livingroom_catch")
// is encoded into the canvas's `passageName` as `Canvas_<slug>_Node_1`. Canvas
// objects themselves carry UUIDs as `id`. We extract the slug from passageName
// to match against the author-facing ready_canvas field.
setup.lookupCanvasBySlug = function(slug) {
    if (!slug) return null;
    var helpData = setup.help_data || {};
    var locCanvases = helpData.locationCanvases || {};
    for (var locUuid in locCanvases) {
        var list = locCanvases[locUuid];
        for (var i = 0; i < list.length; i++) {
            var c = list[i];
            if (!c) continue;
            // Primary match: explicit canvasSlug field (node passages are now
            // Canvas_<slug>_Node_<nodeSlug>, so re-parsing the name is ambiguous).
            if (c.canvasSlug && c.canvasSlug === slug) {
                return { canvas: c, locUuid: locUuid };
            }
            // Fallback: direct id match (covers any future canvas indexing by slug).
            if (c.id === slug) {
                return { canvas: c, locUuid: locUuid };
            }
        }
    }
    return null;
};

// ── Goal block renderer — ONE PATH, three exclusive frames ──────────
// Frame priority: terminal → ready → bullets → empty.
setup.renderQuestsGoalBlock = function(card, goalState) {
    if (!card) return "";

    // Frame 1: ✓ Arc complete (terminal overrides everything)
    // terminal_text overrides the label. A finished NPC arc and a finished
    // BUILD are different endings — the card that ends a release has to be
    // able to say so, and "Arc complete" cannot.
    if (card.terminal === true) {
        var _tlabel = card.terminal_text || "Arc complete";
        return '<div class="quests-goal">' +
               '<div class="quests-goal-header quests-terminal">' +
               '<span class="quests-target">✓</span> ' + _tlabel +
               '</div></div>';
    }

    // Frame 2: 🔓 Ready + 📍 + 🕒 (all goals met + ready_canvas set)
    if (goalState && goalState.allMet && card.ready_canvas) {
        var found = setup.lookupCanvasBySlug(card.ready_canvas);
        if (!found) return "";
        var locName = setup._locNameFromUuid(found.locUuid);
        var schedStr = setup._formatCanvasSchedule(found.canvas);
        var html = '<div class="quests-goal">' +
                   '<div class="quests-goal-header quests-ready">' +
                   '<span class="quests-target">🔓</span> Ready</div>';
        if (locName) html += '<div class="quests-where">📍 ' + locName + '</div>';
        if (schedStr) html += '<div class="quests-where">🕒 ' + schedStr + '</div>';
        html += '</div>';
        return html;
    }

    // Frame 3: 🎯 To advance + ◯ bullets with live progress
    if (goalState && goalState.items.length > 0 && !goalState.allMet) {
        var html2 = '<div class="quests-goal">' +
                    '<div class="quests-goal-header">' +
                    '<span class="quests-target">🎯</span> To advance:</div>' +
                    '<ul>';
        for (var i = 0; i < goalState.items.length; i++) {
            var it = goalState.items[i];
            var marker = it.met ? '✓' : '◯';
            var label = (it.goal && it.goal.label) ||
                        (it.goal && it.goal.trait) ||
                        (it.goal && it.goal.flag) || "";
            if (it.goal.trait && typeof it.currentValue === "number") {
                label += ' — ' + it.currentValue + ' / ' + it.goal.value;
            }
            html2 += '<li>' + marker + ' ' + label + '</li>';
        }
        html2 += '</ul></div>';
        return html2;
    }

    // No frame — narrative text only (card uses routing-only gates with
    // no ready_canvas; happens for transitional cards between capstones).
    return "";
};

})();

:: QuestsV2Widgets [widget nobr]
<<widget "renderQuestsCard">>
<<set _card to $args[0]>>
<<if _card>>
  <<set _goalState to setup.evaluateGoals(_card)>>
  <<set _flavor to (_goalState.allMet && _card.ready_text) ? _card.ready_text : _card.text>>
  <<set _goalBlock to setup.renderQuestsGoalBlock(_card, _goalState)>>
  <div class="quests-card">
    <div class="quests-flavor"><<print _flavor>></div>
    <<if _goalBlock>><<print _goalBlock>><</if>>
    <<if _card.tip>><div class="quests-tip">💡 <<print _card.tip>></div><</if>>
  </div>
<</if>>
<</widget>>

:: QuestsV2Styles [stylesheet]
/* PRD 48 — Quests Engine V2 card styles. Self-contained, parallel to .stage-hint-*. */
.quests-section {
    margin: 16px 0;
}
.quests-section h3 {
    color: var(--theme-text-strong);
    font-size: 1.1em;
    margin: 0 0 8px;
}
.quests-card {
    background: var(--theme-surface);
    border: 1px solid var(--theme-border);
    border-radius: 6px;
    padding: 12px 16px;
    margin: 8px 0;
}
.quests-flavor {
    color: var(--theme-text);
    font-style: italic;
    line-height: 1.5;
    margin-bottom: 8px;
}
.quests-goal {
    margin: 8px 0;
    padding: 8px 12px;
    background: rgba(0,0,0,0.04);
    border-radius: 4px;
}
.quests-goal-header {
    font-weight: 600;
    color: var(--theme-text-strong);
    margin-bottom: 4px;
}
.quests-goal-header.quests-ready,
.quests-goal-header.quests-terminal {
    color: var(--theme-success, #28a745);
}
.quests-goal ul {
    list-style: none;
    padding: 0;
    margin: 4px 0;
}
.quests-goal li {
    padding: 2px 0;
    color: var(--theme-text);
}
.quests-where {
    padding: 2px 0;
    color: var(--theme-text);
}
.quests-tip {
    margin-top: 8px;
    padding: 6px 10px;
    background: rgba(255, 235, 100, 0.15);
    border-left: 3px solid var(--theme-warning, #f0ad4e);
    border-radius: 3px;
    color: var(--theme-text);
    font-size: 0.95em;
}
.quests-target {
    margin-right: 4px;
}
.no-quests {
    color: var(--theme-text-muted);
    font-style: italic;
    padding: 12px;
}

:: QuestsPage
<<nobr>>
<h2>What's Next</h2>

/* PRD 48 — Quests Engine V2 page. One card per arc NPC + Story Goals
   section. Picker swaps cards as state crosses; goal-block frame swaps
   from 🎯 (climbing) → 🔓 (ready) → ✓ (terminal) automatically. */

<<set _goals = setup.pickQuestsCards("story_goals")>>
<<if _goals.length > 0>>
  <div class="quests-section">
    <h3>Story Goals</h3>
    <<for _g range _goals>><<renderQuestsCard _g>><</for>>
  </div>
<</if>>

/* The NPC sections come from the CARDS, not from setup.help_data.npcs. help_data.npcs is
   populated only by canvases carrying targetType="npc" trait effects (_build_help_data), so an
   NPC with a full quest ladder but no stat bumps — one whose arc runs on player counters — was
   silently absent and its cards never rendered (Vesper's Colm: 4 cards, 0 renders). quests_cards
   IS the source of truth for who has cards, and pickQuestsCard() matches card.npc_id directly,
   so no slug/uuid translation is needed and this behaves the same in --use-db builds. */
<<set _allCards = setup.quests_cards || []>>
<<set _hidden = setup.hiddenNpcs || {}>>
<<set _slugMap = setup.npc_slug_map || {}>>
<<set _npcSlugs = []>>
<<for _c range _allCards>>
  <<if _c && _c.npc_id && _npcSlugs.indexOf(_c.npc_id) === -1>>
    /* hiddenNpcs is UUID-keyed (hidden_npcs_map); check both forms so hidden_from_ui still
       suppresses a section whichever build mode this is. */
    <<if !_hidden[_c.npc_id] && !_hidden[_slugMap[_c.npc_id]]>>
      <<run _npcSlugs.push(_c.npc_id)>>
    <</if>>
  <</if>>
<</for>>

<<set _rendered = 0>>
<<for _slug range _npcSlugs>>
  <<set _card = setup.pickQuestsCard(_slug)>>
  <<if _card>>
    <<set _nid = _slugMap[_slug] || _slug>>
    <<set _rendered = _rendered + 1>>
    <div class="quests-section">
      <h3><<print ($npcs[_nid] && $npcs[_nid].name) || ($npcs[_slug] && $npcs[_slug].name) || _slug.replace("npc_", "")>></h3>
      <<renderQuestsCard _card>>
    </div>
  <</if>>
<</for>>

/* "did we draw a card", not "does help_data list anybody" — the old test could leave a bare
   Story-Goals heading with nothing under it. */
<<if _goals.length === 0 && _rendered === 0>>
  <div class="no-quests">No active quests.</div>
<</if>>
<</nobr>>
<<link "← Back">><<run setup.smartBack()>><</link>>
"""

    def _generate_time_system(self) -> str:
        """Generate time system with proper SugarCube widgets and display."""
        # Dev mode [script] passage - runs at story initialization, always available
        # This ensures dev functions work even after page refresh or save/load
        dev_script_passage = ""
        if self.dev_mode:
            dev_script_passage = """:: DevModeInit [script]
// ===== DEV MODE HELPER FUNCTIONS =====
// These mutate $player / $npcs and hand-patch the DOM without navigating, so each one
// commits a moment (setup.commitMoment) to publish the change into the history — otherwise
// it lives only in the active moment and a save or refresh replays the old value.
// (The previous comment here claimed sessionStorage persistence; no such code ever existed.)

window.devAdjustNpcTrait = function(npcId, trait, delta) {
    var npc = State.variables.npcs[npcId];
    if (npc && npc.core_traits) {
        var current = npc.core_traits[trait] || 0;
        var newValue = Math.max(0, current + delta);
        npc.core_traits[trait] = newValue;
        // Direct DOM update
        var el = document.getElementById('npc-trait-' + npcId + '-' + trait);
        if (el) el.textContent = newValue;
        var sidebarEl = document.getElementById('sidebar-npc-trait-' + npcId + '-' + trait);
        if (sidebarEl) sidebarEl.textContent = newValue;
    }
};

window.devAdjustPlayerTrait = function(trait, delta) {
    var player = State.variables.player;
    if (player && player.core_traits) {
        var current = player.core_traits[trait] || 0;
        var newValue = Math.max(0, current + delta);
        player.core_traits[trait] = newValue;
        // Direct DOM update - update all instances
        var sidebarEl = document.getElementById('sidebar-player-trait-' + trait);
        if (sidebarEl) sidebarEl.textContent = newValue;
        var statsEl = document.getElementById('stats-player-trait-' + trait);
        if (statsEl) statsEl.textContent = newValue;
    }
};

// Dev clock buttons navigate nowhere, so they must commit (see setup.commitMoment) or the
// jump is lost on save/refresh. waitTime() already commits; devNextDay writes past advanceDay
// and has to commit for itself.
window.devAdvanceHour = function() {
    window.waitTime(60);
};

window.devNextDay = function() {
    window.advanceDay();
    State.variables.game_state.time_state.current_hour = 6;
    State.variables.game_state.time_state.current_minute = 0;
    if (setup.commitMoment) { setup.commitMoment(); }
};

// Event delegation for dev mode trait adjustment buttons
document.addEventListener('click', function(e) {
    if (e.target.matches('.dev-player-trait-btn')) {
        var trait = e.target.dataset.trait;
        var delta = parseInt(e.target.dataset.delta, 10);
        window.devAdjustPlayerTrait(trait, delta);
        if (setup.commitMoment) { setup.commitMoment(); }
    }
    if (e.target.matches('.dev-npc-trait-btn')) {
        var npcId = e.target.dataset.npc;
        var trait = e.target.dataset.trait;
        var delta = parseInt(e.target.dataset.delta, 10);
        window.devAdjustNpcTrait(npcId, trait, delta);
        if (setup.commitMoment) { setup.commitMoment(); }
    }
});

// Simple back navigation using SugarCube's history stack
window.devGoBack = function() {
    if (State.length > 1) { Engine.backward(); }
    else { Engine.play("Navigation"); }
};

"""

        # Info page back-navigation: track last game passage via [script] tag
        # so the handler survives save/load (runs on every story initialization)
        rent_redirect_block = ""
        if self.rent_enabled:
            rent_redirect_block = """
    // Rent intercept: redirect to RentDay when rent is due
    // Only trigger on location passages or Navigation — never mid-canvas
    var rs = State.variables.game_state && State.variables.game_state.rent_state;
    if (rs && rs.is_due && psg !== "RentDay" && infoPages.indexOf(psg) === -1
        && (psg.indexOf("Location_") === 0 || psg === "Navigation")) {
        // Save the current passage so "Continue your day" returns here after rent
        State.variables.last_game_passage = psg;
        setTimeout(function() { Engine.play("RentDay"); }, 10);
        return;
    }
"""

        clothing_redirect_block = ""
        if self.clothing_enabled:
            clothing_redirect_block = """
    // Clothing intercept: block location entry if not dressed enough
    if (psg.indexOf("Location_") === 0 && infoPages.indexOf(psg) === -1) {
        var clothingMsg = setup.checkLocationClothing(psg);
        if (clothingMsg) {
            State.variables._clothing_block_message = clothingMsg;
            State.variables._clothing_block_destination = psg;
            setTimeout(function() { Engine.play("ClothingBlock"); }, 10);
            return;
        }
    }
"""

        # Travel-friction: charge a location's entry cost (time + traits) on a genuine
        # move. Runs AFTER rent/clothing so a blocked entry never charges (no
        # double-charge on retry). Only emitted when some location declares costs;
        # otherwise movement stays free (backward-compatible).
        has_location_costs = any(
            (getattr(loc, 'properties', None) or {}).get('entry_costs')
            for loc in self.locations
        )
        travel_cost_block = ""
        if has_location_costs:
            travel_cost_block = """
    // Travel-friction intercept: charge entry cost on a genuine move.
    if (psg.indexOf("Location_") === 0 && infoPages.indexOf(psg) === -1) {
        var travelSlug = (setup.passage_to_location || {})[psg];
        if (travelSlug) {
            var destLoc = (setup.locations || {})[travelSlug] || {};
            var curLoc = (sv.player && sv.player.current_location) || "";
            // Only a real move (entering a DIFFERENT location) is charged — re-entry
            // and back-from-a-menu are free.
            if (String(destLoc.id) !== String(curLoc)) {
                if (!setup.checkLocationCostsAffordable(travelSlug)) {
                    sv._travel_block_message = setup.getLocationCostBlockedMessage(travelSlug);
                    sv._travel_block_destination = psg;
                    setTimeout(function() { Engine.play("TravelBlock"); }, 10);
                    return;
                }
                setup.deductLocationCosts(travelSlug);
            }
        }
    }
"""

        # FlagsPage belongs here too: it has a smartBack back-link and a sidebar button, so
        # omitting it let the tracker record it as $last_game_passage and let smartBack land
        # back INSIDE it.
        info_pages_list = '["QuestsPage", "TipsPage", "StatsPage", "SchedulePage", "MissingMediaPage", "StoryJournal", "WardrobePage", "ShopPage", "ClothingBlock", "FlagsPage"'
        if self.rent_enabled:
            info_pages_list += ', "RentDay", "RentDay_Paid", "RentDay_Short"'
        if has_location_costs:
            info_pages_list += ', "TravelBlock"'
        # The cheat page MUST be registered: setup.commitMoment refuses to publish a
        # moment on any passage isRerenderSafe() rejects, so without this every grant
        # is lost on save/refresh. Membership also keeps Back from landing on it.
        if self.cast_page:
            info_pages_list += ', "CastPage"'
        if self.cheat_page:
            info_pages_list += ', "CheatPage"'
        info_pages_list += ']'

        info_nav_script = """:: InfoPageNav [script]
// Track the last non-info-page passage so info page back buttons always work.
// Fixes softlock when history fills with info pages and Engine.backward() loops.

// Info/sidebar page titles, exposed once so the last_game_passage tracker below
// AND setup.smartBack() share ONE list (they can't drift apart).
setup.infoPages = """ + info_pages_list + """;

// Cross-release save migration: fill-if-absent deep-merge of the current default
// skeleton (setup.stateDefaults) into a loaded save's State.variables. Adds any
// $npcs / core_trait / flag / $game_state sub-map a newer release introduced
// (SugarCube never re-runs :: Start on load); NEVER overwrites an earned value.
// Idempotent. Called from the :passagestart handler below on every passage
// (fresh play = no-op, all present).
//
// DEPTH IS NOT UNIFORM, and the asymmetry is deliberate:
//   $game_state  top level AND one level into a sub-map. Safe because every
//                non-empty default here is engine bookkeeping (phone, rent_state,
//                fast_jobs, bank, time_state) whose keys are structural. The
//                player-owned maps (quests, inventory, passes, trigger_history)
//                all default to {}, so there is nothing to fill into them.
//   $player      top level ONLY, plus core_traits named explicitly. $player.wardrobe
//                is an id -> garment map, so filling INTO it would hand back a
//                starting garment the player sold or discarded. core_traits is
//                named because a new release's new meter must appear, and a trait
//                is bookkeeping the player never deletes.
// Arrays are never merged at any depth: a default [] would otherwise re-seed a
// list the player has legitimately emptied.
setup.backfillStateDefaults = function (sv) {
    var sd = setup.stateDefaults;
    if (!sd || !sv) return;
    // Defaults live on setup and are shared by every save in the session, so hand
    // out copies — otherwise a player's state aliases the default object and the
    // next mutation edits the template every later backfill reads from.
    function clone(v) {
        return (v && typeof v === 'object') ? JSON.parse(JSON.stringify(v)) : v;
    }
    function isFillable(v) {
        return v && typeof v === 'object' && !Array.isArray(v);
    }
    if (!sv.flags) sv.flags = {};
    var df = sd.flags || {};
    for (var fk in df) { if (!(fk in sv.flags)) sv.flags[fk] = clone(df[fk]); }
    var dp = sd.player || {};
    if (sv.player) {
        for (var pk in dp) { if (!(pk in sv.player)) sv.player[pk] = clone(dp[pk]); }
        if (!sv.player.core_traits) sv.player.core_traits = {};
        var pt = dp.core_traits || {};
        for (var tk in pt) { if (!(tk in sv.player.core_traits)) sv.player.core_traits[tk] = pt[tk]; }
    }
    var dg = sd.game_state || {};
    if (!sv.game_state) sv.game_state = {};
    for (var gk in dg) {
        var dv = dg[gk];
        if (!(gk in sv.game_state)) { sv.game_state[gk] = clone(dv); continue; }
        var cv = sv.game_state[gk];
        if (!isFillable(dv) || !isFillable(cv)) continue;
        for (var sk in dv) { if (!(sk in cv)) cv[sk] = clone(dv[sk]); }
    }
    if (!sv.npcs) sv.npcs = {};
    var dn = sd.npcs || {};
    for (var ns in dn) {
        var def = dn[ns];
        if (!sv.npcs[ns]) {
            sv.npcs[ns] = JSON.parse(JSON.stringify(def));  // whole new NPC (deep-copy off setup; JSON-safe)
        } else {
            var cur = sv.npcs[ns];
            if (!cur.core_traits) cur.core_traits = {};
            var dct = def.core_traits || {};
            for (var ct in dct) { if (!(ct in cur.core_traits)) cur.core_traits[ct] = dct[ct]; }
            if (!cur.flags) cur.flags = {};
            var dfl = def.flags || {};
            for (var cf in dfl) { if (!(cf in cur.flags)) cur.flags[cf] = dfl[cf]; }
        }
    }
};

// "Back" for sidebar/info pages.
//
// SugarCube snapshots a moment's variables at passage START. Engine.goTo(i) re-activates
// an EARLIER moment, which restores that moment's variables — so it discards everything
// the player changed since the current passage rendered. That silently ate the wardrobe:
// equip an outfit, press Back, and the equip was rolled away. In Vesper it made the game
// unfinishable (the cover is granted un-worn and 13 canvases gate on it being equipped).
//
// So we navigate FORWARD to the stored passage instead, which is what Road to Success does
// (`<<goto previous()>>`): a new moment is created and it carries the player's changes.
// $last_game_passage is maintained by the :passagestart handler below and already excludes
// every info page, so it is exactly the "previous real passage" we want.
//
// Engine.goTo survives ONLY for canvas nodes. Forward-playing INTO a canvas node re-runs its
// body — re-firing its advanceTime/flag scripts (the original bug this function was written
// for: "going back doesn't work from one-time canvases"). Rolling state back is the lesser
// evil there, and it costs nothing the player can see: the only info pages that MUTATE state
// (Wardrobe/Shop) are reachable solely from a location, never from mid-canvas.
setup.smartBack = function () {
    var dest = State.variables.last_game_passage || "Navigation";
    // Locations and the nav screen are safe to re-render (see setup.isRerenderSafe): auto-fire
    // is idempotent via markCanvasTriggered, entry costs are guarded (destLoc.id !== curLoc),
    // and the random roll is gated on entry provenance (see checkRandomEncounters). Go FORWARD
    // so the player's changes ride along.
    if (setup.isRerenderSafe(dest) && setup.infoPages.indexOf(dest) === -1) {
        Engine.play(dest);
        return;
    }
    var hist = State.history, active = State.activeIndex;
    for (var i = active - 1; i >= 0; i--) {
        var t = hist[i] && hist[i].title;
        if (t && setup.infoPages.indexOf(t) === -1) { Engine.goTo(i); return; }
    }
    // dest is a canvas node AND its moment has been evicted (maxStates). Forward-playing it
    // would re-run its body — re-firing advanceTime and additive trait effects. Bounce to the
    // hub instead: losing your place beats silently re-applying a scene's effects.
    Engine.play("Navigation");
};

// May a passage safely carry a COMMITTED post-render state?
//
// This is the load-bearing invariant of SugarCube's state model: a moment stores the
// variables as of passage ARRIVAL (State.create snapshots before Passage.render runs), and
// on save-load / refresh the engine RE-RENDERS the active passage from that snapshot. So a
// moment is only sound if re-running its passage body from the stored state is a no-op.
//
// Locations, Navigation and the info pages qualify — their bodies are pure renders, or their
// writes are guarded (visited_locations by .includes, entry costs by an id-equality check).
// CANVAS NODES DO NOT: their bodies carry render-time advanceTime() script macros and additive
// trait effects (75 of Vesper's 160 nodes). Commit a post-render state on one and every reload
// re-applies them — verified: the clock drifts forward on each refresh, forever.
// (NB: never write a literal closing-script-macro in these comments — the raw text would close
// the emitted HTML <script> element early and truncate the whole engine. It has happened.)
setup.isRerenderSafe = function (title) {
    if (!title) return false;
    if (title === "Navigation") return true;
    if (title.indexOf("Location_") === 0) return true;
    return setup.infoPages.indexOf(title) !== -1;
};

// Commit a history moment WITHOUT navigating or re-rendering.
//
// Both Save and the refresh-restore serialize State.history, not the live variables object.
// A handler that mutates state without navigating (the sidebar wait buttons, the phone, the
// dev trait buttons) therefore leaves its change in the active moment only — invisible to
// save and lost on refresh. Committing publishes it into the history.
//
// Gated by isRerenderSafe: on a canvas node we deliberately DON'T commit. That keeps the
// pre-fix behaviour there (a wait made mid-canvas still won't survive a refresh) — which is
// the right trade, because the alternative is a save that re-fires the scene's effects on
// every load. A lost 10-minute wait beats a corrupted save.
//
// Call it LAST in a handler: State.create re-clones the active variables, so any object
// reference held across this call is detached and later writes through it are lost.
setup.commitMoment = function () {
    try {
        var t = State.passage;
        if (!setup.isRerenderSafe(t)) return false;
        State.create(t);
        return true;
    } catch (e) { return false; }
};

$(document).on(':passagestart', function(ev) {
    // One-time legacy save migration: $player.flags retired 2026-05-06.
    // Saves made before the consolidation have $player.flags populated with
    // init-time defaults (and possibly a rent_eviction_flag write from the
    // pre-fix rent passage). Copy any TRUE values into the canonical $flags
    // store, then delete the legacy property. Idempotent: after delete the
    // guard fails on every subsequent passagestart.
    var sv = State.variables;
    if (sv.player && sv.player.flags) {
        var legacyFlags = sv.player.flags;
        if (!sv.flags) sv.flags = {};
        for (var lk in legacyFlags) {
            if (legacyFlags[lk] === true && sv.flags[lk] !== true) {
                sv.flags[lk] = true;
            }
        }
        delete sv.player.flags;
    }
    // Cross-release save backfill: fill-if-absent from setup.stateDefaults so a
    // save from an earlier release picks up any NPC / trait / flag a newer release
    // added (SugarCube never re-runs :: Start on load). See setup.backfillStateDefaults.
    if (setup.backfillStateDefaults) { setup.backfillStateDefaults(sv); }
    // Release provenance: last_* follows the build currently running, origin_* was
    // written once by :: Start and the backfill cannot overwrite it. Guarded on a
    // difference so a save that has not changed builds is not dirtied every passage.
    if (sv.game_state && sv.game_state.last_schema !== setup.buildSchema) {
        sv.game_state.last_version = setup.buildVersion;
        sv.game_state.last_schema = setup.buildSchema;
    }
    var psg = ev.passage.title;
    var infoPages = setup.infoPages;
""" + rent_redirect_block + clothing_redirect_block + travel_cost_block + """    if (infoPages.indexOf(psg) === -1) {
        State.variables.last_game_passage = psg;
    }
    // Check for newly triggered phone conversations
    if (setup.phone_enabled && typeof setup.checkPhoneConversations === 'function') {
        setup.checkPhoneConversations();
    }
});

"""

        # Dev mode indicator widget
        dev_indicator = ""
        if self.dev_mode:
            dev_indicator = """
<<widget "devIndicator">>
<div id="dev-indicator" style="background:#dc3545;color:white;padding:4px 8px;border-radius:4px;font-weight:bold;text-align:center;margin-bottom:8px;font-size:12px;">[DEV MODE]</div>
<</widget>>
"""

        # Dev mode review button widget
        review_button = ""
        if self.dev_mode:
            review_button = """
<<widget "reviewButton">>
<div id="review-btn-widget" style="text-align:center;margin-bottom:8px;">
  <<button "📋 Review Canvases">><<goto "CanvasReviewList">><</button>>
</div>
<</widget>>
"""

        # Dev jumps widget — one link per dev-shortcut canvas (trigger gated on
        # dev_mode_enabled). Clicking Engine.plays straight into the canvas's first
        # node, bypassing its trigger; the canvas itself seeds state + bounces to
        # the target. Dev builds only. Empty list → a muted "author one" hint so the
        # section is discoverable even before any jump exists.
        dev_jumps_widget = ""
        if self.dev_mode:
            jumps = self._dev_shortcut_jumps()
            if jumps:
                jumps_body = "\n".join(
                    '  <div class="dev-jump-row"><<link "{label}" "{passage}">><</link>></div>'.format(
                        label=(j["label"] or "Jump").replace('\\', '').replace('"', "'"),
                        passage=j["passage"],
                    )
                    for j in jumps
                )
            else:
                jumps_body = (
                    '  <div style="opacity:0.65;font-size:11px;">No dev jumps yet — '
                    'author a canvas gated on flag <code>dev_mode_enabled</code>.</div>'
                )
            dev_jumps_widget = """
<<widget "devJumps">>
<div id="dev-jumps-widget" style="background:#212529;color:#fff;border:1px solid #dc3545;border-radius:4px;padding:6px 8px;margin-bottom:8px;">
<div style="font-weight:bold;font-size:11px;color:#ffc107;margin-bottom:4px;">&#9193; DEV JUMPS</div>
""" + jumps_body + """
</div>
<</widget>>
"""

        # Dev mode time controls (extra shortcuts)
        dev_time_controls = ""
        if self.dev_mode:
            dev_time_controls = """
    <div class="dev-control-line" style="text-align:center;font-size:11px;margin-top:4px;border-top:1px dashed #ced4da;padding-top:4px;">
        <button class="time-btn dev-btn" onclick="devAdvanceHour()" title="Dev: +1 hour" style="background:#ffc107;color:#000;">+1hr</button> | <button class="time-btn dev-btn" onclick="devNextDay()" title="Dev: Next day 7AM" style="background:#ffc107;color:#000;">Next Day</button>
    </div>"""

        # Player traits widget with optional dev controls
        if self.dev_mode:
            player_traits_widget = """<<widget "playerTraits">>
<div id="traits-widget" class="traits-display">
  <div class="traits-header">Your Traits</div>
  <<if $player and $player.core_traits and Object.keys($player.core_traits).length > 0>>
    <<set _keys to Object.keys($player.core_traits).sort()>>
    <ul class="traits-list">
      <<for _i to 0; _i lt _keys.length; _i++>>
        <<set _k to _keys[_i]>>
        <<if setup.hiddenTraits && setup.hiddenTraits.includes(_k)>><<continue>><</if>>
        <li class="trait-item">
          <span class="trait-name"><<print _k>></span>
          <span class="trait-controls"><button class="dev-adj-btn dev-player-trait-btn" @data-trait="_k" data-delta="-1">-</button> <span @id="'sidebar-player-trait-' + _k" class="trait-value"><<print $player.core_traits[_k]>></span> <button class="dev-adj-btn dev-player-trait-btn" @data-trait="_k" data-delta="1">+</button></span>
        </li>
      <</for>>
    </ul>
  <<else>>
    <div class="no-traits">No traits</div>
  <</if>>
  <div class="traits-hint">Use +/- to adjust for testing.</div>
</div>
<</widget>>"""

            npc_traits_widget = """<<widget "npcTraits">>
<div id="npc-traits-widget" class="traits-display">
  <div class="traits-header">NPC Traits</div>
  <<for _npcId, _npc range $npcs>>
    <<if (setup.hiddenNpcs && setup.hiddenNpcs[_npcId])>><<continue>><</if>>
    <<if _npc.core_traits && Object.keys(_npc.core_traits).length > 0>>
      <div class="npc-trait-section">
        <div class="npc-trait-name"><<print _npc.name>></div>
        <ul class="traits-list">
          <<set _npcKeys to Object.keys(_npc.core_traits).sort()>>
          <<for _j to 0; _j lt _npcKeys.length; _j++>>
            <<set _nk to _npcKeys[_j]>>
            <<if setup.hiddenTraits && setup.hiddenTraits.includes(_nk)>><<continue>><</if>>
            <li class="trait-item">
              <span class="trait-name"><<print _nk>></span>
              <span class="trait-controls"><button class="dev-adj-btn dev-npc-trait-btn" @data-npc="_npcId" @data-trait="_nk" data-delta="-1">-</button> <span @id="'sidebar-npc-trait-' + _npcId + '-' + _nk" class="trait-value"><<print _npc.core_traits[_nk]>></span> <button class="dev-adj-btn dev-npc-trait-btn" @data-npc="_npcId" @data-trait="_nk" data-delta="1">+</button></span>
            </li>
          <</for>>
        </ul>
      </div>
    <</if>>
  <</for>>
</div>
<</widget>>"""
        else:
            player_traits_widget = """<<widget "playerTraits">>
<div id="traits-widget" class="traits-display">
  <div class="traits-header">Traits</div>
  <<if $player and $player.core_traits and Object.keys($player.core_traits).length > 0>>
    <<set _keys to Object.keys($player.core_traits).sort()>>
    <ul class="traits-list">
      <<for _i to 0; _i lt _keys.length; _i++>>
        <<set _k to _keys[_i]>>
        <<if setup.hiddenTraits && setup.hiddenTraits.includes(_k)>><<continue>><</if>>
        <li class="trait-item">
          <span class="trait-name"><<print _k>></span>
          <span class="trait-value"><<print $player.core_traits[_k]>></span>
        </li>
      <</for>>
    </ul>
  <<else>>
    <div class="no-traits">No traits</div>
  <</if>>
  <div class="traits-hint">Updates after each choice.</div>

</div>
<</widget>>"""
            npc_traits_widget = ""

        # StoryCaption with optional dev indicator and missing media button
        phone_btn_line = "\n<<phoneButton>>" if self.phone_enabled else ""
        # State-reactive player portrait — mounts just below the time display (time stays at the
        # very top of the sidebar), above the HUD/stat items. Opt-in.
        portrait_line = "<<playerPortrait>>\n" if self.player_portrait_enabled else ""
        # Sidebar version/release-date footer — build-time constants baked as literal
        # markup (same style as <<patreonButton>>'s static URL). html.escape guards
        # build-breaking chars. Renders nothing when both empty, but the widget is
        # ALWAYS defined (SugarCube throws on an undefined <<versionFooter>> call).
        _ver = html.escape((self.project.metadata or {}).get("version", "") or "")
        _rel = html.escape((self.project.metadata or {}).get("release_date", "") or "")
        _footer_parts = ([f"v{_ver}"] if _ver else []) + ([_rel] if _rel else [])
        _footer_text = " · ".join(_footer_parts)
        # No build badge any more: there is one build. What a player needs to identify
        # is the RELEASE (it is what their guide's codes are scoped to), and the version
        # string already does that here and in the cheat page's own heading.
        _footer_inner = _footer_text
        version_footer_widget = (
            f'\n<<widget "versionFooter">>\n<div class="sidebar-version">{_footer_inner}</div>\n<</widget>>\n'
            if _footer_inner else '\n<<widget "versionFooter">><</widget>>\n'
        )
        if self.dev_mode:
            story_caption = f""":: StoryCaption
<<devIndicator>>
<<reviewButton>>
<<devJumps>>
<<missingMediaButton>>
<<timeDisplay>>
{portrait_line}<<sidebarItems>>{phone_btn_line}
<<activeModifiers>>
<<journalButton>>
<<castButton>>
<<tipsButton>>
<<cheatButton>>
<<statsButton>>
<<scheduleButton>>
<<flagsButton>>
<<playerTraits>>
<<npcTraits>>
<<patreonButton>>
<<versionFooter>>"""
        else:
            story_caption = f""":: StoryCaption
<<missingMediaButton>>
<<timeDisplay>>
{portrait_line}<<sidebarItems>>{phone_btn_line}
<<activeModifiers>>
<<journalButton>>
<<castButton>>
<<tipsButton>>
<<cheatButton>>
<<statsButton>>
<<scheduleButton>>
<<playerTraits>>
<<patreonButton>>
<<versionFooter>>"""

        # Stats page with optional dev controls for NPC traits
        # Get video path for portrait URLs
        video_path = getattr(self, 'video_path', '') or './media'
        placeholder_svg = self._get_placeholder_svg()
        # Escape SVG for use in onerror handler
        escaped_svg = html.escape(placeholder_svg).replace("'", "\\'")

        if self.dev_mode:
            stats_page = f""":: StatsPage
<<nobr>>
<h2>All Stats</h2>

<!-- Player Stats -->
<div class="stats-card stats-card-with-portrait">
  <div class="stats-portrait">
    <<if $player.portrait>>
      <img @src="'{video_path}/' + $player.portrait" @alt="$player.name" onerror="this.style.display='none';this.parentElement.innerHTML='{escaped_svg}';">
    <<else>>
      {placeholder_svg}
    <</if>>
  </div>
  <div class="stats-info">
    <div class="stats-name">You (<<print $player.name>>)</div>
    <div class="stats-traits">
      <<if $player && $player.core_traits && Object.keys($player.core_traits).length > 0>>
        <<for _tk, _tv range $player.core_traits>>
          <<if setup.hiddenTraits && setup.hiddenTraits.includes(_tk)>><<continue>><</if>>
          <div class="stats-trait-item">
            <span><<print _tk>></span>
            <span class="trait-controls"><button class="dev-adj-btn dev-player-trait-btn" @data-trait="_tk" data-delta="-1">-</button> <span @id="'stats-player-trait-' + _tk" class="stats-trait-value"><<print _tv>></span> <button class="dev-adj-btn dev-player-trait-btn" @data-trait="_tk" data-delta="1">+</button></span>
          </div>
        <</for>>
      <<else>>
        <em>No traits</em>
      <</if>>
    </div>
  </div>
</div>

<!-- NPC Stats -->
<<if Object.keys($npcs).length > 0>>
  <<for _npcId, _npc range $npcs>>
    <<if (setup.hiddenNpcs && setup.hiddenNpcs[_npcId])>><<continue>><</if>>
    <div class="stats-card stats-card-with-portrait">
      <div class="stats-portrait">
        <<if _npc.portrait>>
          <img @src="'{video_path}/' + _npc.portrait" @alt="_npc.name" onerror="this.style.display='none';this.parentElement.innerHTML='{escaped_svg}';">
        <<else>>
          {placeholder_svg}
        <</if>>
      </div>
      <div class="stats-info">
        <div class="stats-name"><<print _npc.name>></div>
        <div class="stats-traits">
          <<if _npc.core_traits && Object.keys(_npc.core_traits).length > 0>>
            <<for _tk, _tv range _npc.core_traits>>
              <<if setup.hiddenTraits && setup.hiddenTraits.includes(_tk)>><<continue>><</if>>
              <div class="stats-trait-item">
                <span><<print _tk>></span>
                <span class="trait-controls"><button class="dev-adj-btn dev-npc-trait-btn" @data-npc="_npcId" @data-trait="_tk" data-delta="-1">-</button> <span @id="'npc-trait-' + _npcId + '-' + _tk" class="stats-trait-value"><<print _tv>></span> <button class="dev-adj-btn dev-npc-trait-btn" @data-npc="_npcId" @data-trait="_tk" data-delta="1">+</button></span>
              </div>
            <</for>>
          <<else>>
            <em>No traits</em>
          <</if>>
        </div>
      </div>
    </div>
  <</for>>
<<else>>
  <p><em>No NPCs found.</em></p>
<</if>>
<</nobr>>
<<link "← Back">><<run setup.smartBack()>><</link>>"""
        else:
            stats_page = f""":: StatsPage
<<nobr>>
<h2>All Stats</h2>

<!-- Player Stats -->
<div class="stats-card stats-card-with-portrait">
  <div class="stats-portrait">
    <<if $player.portrait>>
      <img @src="'{video_path}/' + $player.portrait" @alt="$player.name" onerror="this.style.display='none';this.parentElement.innerHTML='{escaped_svg}';">
    <<else>>
      {placeholder_svg}
    <</if>>
  </div>
  <div class="stats-info">
    <div class="stats-name">You (<<print $player.name>>)</div>
    <div class="stats-traits">
      <<if $player && $player.core_traits && Object.keys($player.core_traits).length > 0>>
        <<for _tk, _tv range $player.core_traits>>
          <<if setup.hiddenTraits && setup.hiddenTraits.includes(_tk)>><<continue>><</if>>
          <div class="stats-trait-item">
            <span><<print _tk>></span>
            <span class="stats-trait-value"><<print _tv>></span>
          </div>
        <</for>>
      <<else>>
        <em>No traits</em>
      <</if>>
    </div>
  </div>
</div>

<!-- NPC Stats -->
<<if Object.keys($npcs).length > 0>>
  <<for _npcId, _npc range $npcs>>
    <<if (setup.hiddenNpcs && setup.hiddenNpcs[_npcId])>><<continue>><</if>>
    <div class="stats-card stats-card-with-portrait">
      <div class="stats-portrait">
        <<if _npc.portrait>>
          <img @src="'{video_path}/' + _npc.portrait" @alt="_npc.name" onerror="this.style.display='none';this.parentElement.innerHTML='{escaped_svg}';">
        <<else>>
          {placeholder_svg}
        <</if>>
      </div>
      <div class="stats-info">
        <div class="stats-name"><<print _npc.name>></div>
        <div class="stats-traits">
          <<if _npc.core_traits && Object.keys(_npc.core_traits).length > 0>>
            <<for _tk, _tv range _npc.core_traits>>
              <<if setup.hiddenTraits && setup.hiddenTraits.includes(_tk)>><<continue>><</if>>
              <div class="stats-trait-item">
                <span><<print _tk>></span>
                <span class="stats-trait-value"><<print _tv>></span>
              </div>
            <</for>>
          <<else>>
            <em>No traits</em>
          <</if>>
        </div>
      </div>
    </div>
  <</for>>
<<else>>
  <p><em>No NPCs found.</em></p>
<</if>>
<</nobr>>
<<link "← Back">><<run setup.smartBack()>><</link>>"""

        # Wardrobe page and clothing block (only if clothing enabled)
        wardrobe_page = ""
        clothing_block_page = ""
        if self.clothing_enabled:
            wardrobe_page = """
:: WardrobePage
<<nobr>>
<h2>Change Clothes</h2>
<<= setup.renderWardrobePage()>>
<</nobr>>
<div id="wardrobe-warning" style="display:none; color:#ff6b6b; margin:10px 0; padding:8px; border:1px solid #ff6b6b; border-radius:4px;"></div>
<<link "← Back">><<script>>
var dest = State.variables.last_game_passage || "Navigation";
var clothingMsg = setup.checkLocationClothing(dest);
if (clothingMsg) {
    var el = document.getElementById('wardrobe-warning');
    if (el) { el.innerHTML = clothingMsg; el.style.display = 'block'; }
} else {
    setup.smartBack();
}
<</script>><</link>>"""

            clothing_block_page = """
:: ClothingBlock
<h2>Not Dressed for This</h2>
<p><<print State.variables._clothing_block_message || "You need to put on more clothes.">></p>
<div class="clothing-block-choices">
<<link "Change clothes">><<script>>
    State.variables.last_game_passage = State.variables._clothing_block_destination;
    Engine.play("WardrobePage");
<</script>><</link>>
<br>
<<link "Go back">><<script>>
    Engine.play(State.variables.last_game_passage || "Navigation");
<</script>><</link>>
</div>"""

        # Travel-block page (only when some location has an entry cost) — shown when the
        # player can't afford the trait cost of a move. Mirrors ClothingBlock.
        travel_block_page = ""
        if has_location_costs:
            travel_block_page = """
:: TravelBlock
<h2>Not Right Now</h2>
<p><<print State.variables._travel_block_message || "You don't have what it takes to get there right now.">></p>
<div class="clothing-block-choices">
<<link "Go back">><<script>>
    Engine.play(State.variables.last_game_passage || "Navigation");
<</script>><</link>>
</div>"""

        # Shop page (only if clothing and shop enabled)
        shop_page = ""
        if self.clothing_enabled and self.shop_location_slug:
            shop_page = """
:: ShopPage
<<nobr>>
<h2>Clothing Store</h2>
<<= setup.renderShopPage()>>
<</nobr>>
<<link "\u2190 Back">><<run setup.smartBack()>><</link>>"""

        # Rent day page (only if rent enabled)
        rent_page = ""
        if self.rent_enabled:
            rent_page = """
:: RentDay
<<nobr>>
<<set _money to $player.core_traits.money || 0>>
<<set _rent to setup.rent_amount>>
<<set _cur to setup.rent_currency_symbol || "$">>
<<set _rt to setup.rent_text || {}>>
<<set _collectorName to "the landlord">>
<<set _npcPortrait to "">>
<<if setup.rent_collector_npc && setup.npc_slug_map[setup.rent_collector_npc]>>
  <<set _npcId to setup.npc_slug_map[setup.rent_collector_npc]>>
  <<set _npcData to $npcs[_npcId]>>
  <<if _npcData && _npcData.name>>
    <<set _collectorName to _npcData.name>>
    <<set _npcPortrait to _npcData.portrait || "">>
  <</if>>
<</if>>

<h2 class="rent-title"><<print _rt.title || "Monday Morning">> — Rent Day</h2>

<p><<print _rt.scene || "A heavy knock on the door. You open it to find " + _collectorName + " standing there, hand already extended.">></p>

<div class="dialog-block dialog-npc">
  <div class="dialog-content">
    <strong class="dlg-inline"><<print _collectorName>></strong> <<print _rt.greeting || "Rent. " + _cur + _rent + ". You know how this works.">>
  </div>
</div>

<p>You have <<print _cur>><<print _money>>. Rent is <<print _cur>><<print _rent>>.</p>
<div class="rent-choices">
  <<if _money gte _rent>>
    <<set _payText to "Pay " + _cur + _rent + " rent">>
    <<link _payText>>
      <<set $player.core_traits.money -= _rent>>
      <<set $game_state.rent_state.last_paid_week to $game_state.time_state.current_week>>
      <<set $game_state.rent_state.is_due to false>>
      <<set $game_state.rent_state.warnings to 0>>
      <<goto "RentDay_Paid">>
    <</link>>
  <</if>>
  <<set _cantPayText to (_rt.cant_pay || "Tell them you can't pay")>>
  <<link _cantPayText>>
    <<goto "RentDay_Short">>
  <</link>>
</div>
<</nobr>>

:: RentDay_Paid
<<nobr>>
<<set _rt to setup.rent_text || {}>>
<<set _collectorName to "the landlord">>
<<if setup.rent_collector_npc && setup.npc_slug_map[setup.rent_collector_npc]>>
  <<set _npcId to setup.npc_slug_map[setup.rent_collector_npc]>>
  <<set _npcData to $npcs[_npcId]>>
  <<if _npcData && _npcData.name>>
    <<set _collectorName to _npcData.name>>
  <</if>>
<</if>>

<p><<print _rt.paid_scene || "You hand over the cash. " + _collectorName + " counts it, nods once, and turns to leave.">></p>

<div class="dialog-block dialog-npc">
  <div class="dialog-content">
    <strong class="dlg-inline"><<print _collectorName>></strong> <<print _rt.paid_response || "Same time next week.">>
  </div>
</div>

<p><<print _rt.paid_closing || "Another week secured.">></p>

<<set _cur to setup.rent_currency_symbol || "$">>
<p class="rent-balance">Remaining money: <strong><<print _cur>><<print $player.core_traits.money>></strong></p>

<<set _returnTo to (State.variables.last_game_passage || "Navigation")>>
<<link "Continue your day" _returnTo>><</link>>
<</nobr>>

:: RentDay_Short
<<nobr>>
<<set _rt to setup.rent_text || {}>>
<<set _collectorName to "the landlord">>
<<if setup.rent_collector_npc && setup.npc_slug_map[setup.rent_collector_npc]>>
  <<set _npcId to setup.npc_slug_map[setup.rent_collector_npc]>>
  <<set _npcData to $npcs[_npcId]>>
  <<if _npcData && _npcData.name>>
    <<set _collectorName to _npcData.name>>
  <</if>>
<</if>>

<<if $game_state.rent_state.warnings lt setup.rent_grace_periods>>
  <p><<print _rt.warning_scene || "You explain that you're short this week. " + _collectorName + "'s expression doesn't change.">></p>

  <div class="dialog-block dialog-npc">
    <div class="dialog-content">
      <strong class="dlg-inline"><<print _collectorName>></strong> <<print _rt.warning_response || "Next Monday. Don't make me ask twice.">>
    </div>
  </div>

  <p><<print _rt.warning_closing || "You have one week to find the money.">></p>

  <<set $game_state.rent_state.warnings += 1>>
  <<set $game_state.rent_state.is_due to false>>

  <p class="rent-balance">You have: <strong>$<<print $player.core_traits.money>></strong>. You need: <strong>$<<print setup.rent_amount>></strong>.</p>

  <<set _returnTo to (State.variables.last_game_passage || "Navigation")>>
  <<link "Continue your day" _returnTo>><</link>>
<<else>>
  <<if setup.rent_eviction_mode is "flag_set">>
    <<run setup.applyAndNotifyFlag('player', null, setup.rent_eviction_flag, 'set')>>
    <<set $game_state.rent_state.warnings to 0>>
    <<set $game_state.rent_state.is_due to false>>

    <p><<print _rt.eviction_scene_soft || _rt.eviction_scene || _collectorName + " stops waiting for the money. Something shifts in the way " + _collectorName + " looks at you now.">></p>

    <div class="dialog-block dialog-npc">
      <div class="dialog-content">
        <strong class="dlg-inline"><<print _collectorName>></strong> <<print _rt.eviction_response_soft || _rt.eviction_response || "We'll be having a different conversation from here on out.">>
      </div>
    </div>

    <p><<print _rt.eviction_closing_soft || _rt.eviction_closing || "You're still here. But the terms have changed.">></p>

    <<set _returnTo to (State.variables.last_game_passage || "Navigation")>>
    <<link "Continue" _returnTo>><</link>>
  <<else>>
    <p><<print _rt.eviction_scene || _collectorName + " doesn't wait for excuses this time.">></p>

    <div class="dialog-block dialog-npc">
      <div class="dialog-content">
        <strong class="dlg-inline"><<print _collectorName>></strong> <<print _rt.eviction_response || "Locks are getting changed today. Pack your things.">>
      </div>
    </div>

    <p><<print _rt.eviction_closing || "No negotiation. No extension. You had your chance.">></p>

    <p class="game-over-text">GAME OVER</p>

    <<link "Start Over">><<run Engine.restart()>><</link>>
  <</if>>
<</if>>
<</nobr>>"""

        # Build the time widgets content using string concatenation to avoid f-string escaping issues
        time_widgets_start = """:: TimeWidgets [widget nobr]
<!-- Time Display Widgets -->
<<widget "timeFormatted">>
<<set _hour to $game_state.time_state.current_hour>>
<<set _minute to $game_state.time_state.current_minute>>
<<set _displayHour to (_hour is 0 ? 12 : (_hour > 12 ? _hour - 12 : _hour))>>
<<set _ampm to (_hour < 12 ? "AM" : "PM")>>
<<set _minuteStr to (_minute < 10 ? "0" + _minute : _minute)>>
<<print _displayHour + ":" + _minuteStr + " " + _ampm>>
<</widget>>

<!-- Render a quest card: narrative line + (Pattern 2) auto-rendered 🎯 goal
     block + 💡 tip line. Author tags state-pressure variants in the TOML and
     the picker swaps which line fires; widget renders the chosen line, then
     calls setup.computeHintGoal() to render the structured progress block from
     the hint's stage condition (or canvas trigger conditions for branch-inside-
     shell transitions). Game-level mechanics (decay rates, time costs, etc.)
     live on :: TipsPage instead. -->
<<widget "renderStageHint">>
/* Pattern 2 (2026-05-01): accepts either a string (legacy callers) OR a
   hint object {text, condition, tip, auto_goal, ...}. When passed an object
   with auto_goal=true and a stage condition, the engine computes the
   structured 🎯 goal block (bullets + live progress + 📍 location). When
   passed a string OR a no-auto-goal object, falls back to splitting on
   " — 🎯 " (legacy behavior) so existing games keep working unchanged. */
<<set _hintArg to $args[0]>>
<<set _hintObj to (typeof _hintArg === "object" && _hintArg !== null) ? _hintArg : null>>
<<set _hintText to _hintObj ? (_hintObj.text || "") : (_hintArg || "")>>
<<set _computedGoalHtml to _hintObj ? setup.computeHintGoal(_hintObj) : "">>
<<set _separator to " — 🎯 ">>
<<set _splitIdx to _hintText.indexOf(_separator)>>
<<if _computedGoalHtml>>
  /* New path: structured auto-render. If text contains " — 🎯 ", strip the
     manual goal portion (auto-render replaces it). */
  <<if _splitIdx gt -1>>
    <<set _flavor to _hintText.substring(0, _splitIdx)>>
  <<else>>
    <<set _flavor to _hintText>>
  <</if>>
  /* 2026-05-09: when State C "🔓 Ready" fires AND the hint defines
     ready_text, swap flavor → ready_text. The author-supplied ready_text
     replaces the regular text once all helper gates are met. */
  <<if _hintObj && _hintObj.ready_text && setup._isHintReady(_hintObj)>>
    <<set _flavor to _hintObj.ready_text>>
  <</if>>
  <div class="stage-hint-card">
    <div class="stage-hint-flavor"><<print _flavor>></div>
    <<print _computedGoalHtml>>
    <<if _hintObj && _hintObj.tip>>
      <div class="stage-hint-tip">💡 <<print _hintObj.tip>></div>
    <</if>>
  </div>
<<elseif _splitIdx gt -1>>
  /* Legacy path: split on " — 🎯 " */
  <<set _flavor to _hintText.substring(0, _splitIdx)>>
  <<set _goal to _hintText.substring(_splitIdx + _separator.length)>>
  <div class="stage-hint-card">
    <div class="stage-hint-flavor"><<print _flavor>></div>
    <div class="stage-hint-goal"><span class="stage-hint-target">🎯</span> <<print _goal>></div>
    <<if _hintObj && _hintObj.tip>>
      <div class="stage-hint-tip">💡 <<print _hintObj.tip>></div>
    <</if>>
  </div>
<<elseif _hintText>>
  <div class="stage-hint-card">
    <div class="stage-hint-flavor"><<print _hintText>></div>
  </div>
<</if>>
<</widget>>

"""

        # Dev mode: show day count in time display
        if self.dev_mode:
            time_display_widget = """<<widget "timeDisplay">>
<div id="time-widget" class="time-display">
    <div class="time-line">
        <span id="time-display"><<timeFormatted>></span> | <span id="current-day"><<print $game_state.time_state.current_day>></span> | <span id="day-count" style="color:#dc3545;font-weight:bold;">Day <<print $game_state.time_state.day>></span>
    </div>
    <div class="control-line">
        <button class="time-btn" onclick="waitTime(10)" title="Advance 10 minutes">></button> | <button class="time-btn" onclick="waitTime(60)" title="Advance 1 hour">>></button> | <button class="time-btn" onclick="waitTime(1440)" title="Advance 1 day">>>>>></button>
    </div>""" + dev_time_controls + """
</div>
<</widget>>

"""
        else:
            time_display_widget = """<<widget "timeDisplay">>
<div id="time-widget" class="time-display">
    <div class="time-line">
        <span id="time-display"><<timeFormatted>></span> | <span id="current-day"><<print $game_state.time_state.current_day>></span>
    </div>
    <div class="control-line">
        <button class="time-btn" onclick="waitTime(10)" title="Advance 10 minutes">></button> | <button class="time-btn" onclick="waitTime(60)" title="Advance 1 hour">>></button> | <button class="time-btn" onclick="waitTime(1440)" title="Advance 1 day">>>>>></button>
    </div>""" + dev_time_controls + """
</div>
<</widget>>

"""

        # Sidebar items widget (configurable via TOML [[sidebar_items]])
        sidebar_items_widget = """
<<widget "sidebarItems">>
<<if setup.sidebar_items && setup.sidebar_items.length > 0>>
<div id="sidebar-items-widget">
<<for _si to 0; _si lt setup.sidebar_items.length; _si++>>
  <<set _item to setup.sidebar_items[_si]>>
  <<if _item.show_when and not setup.triggerConditionsSatisfied(_item.show_when)>>
    <<continue>>
  <</if>>
  <<if _item.type is "countdown">>
    <<set _daysLeft to _item.total_days - $game_state.time_state.day + 1>>
    <div class="sidebar-item countdown-item" id="sidebar-countdown-<<print _si>>">
    <<if _daysLeft gt 1>>
      <<print _daysLeft + " " + _item.label>>
    <<elseif _daysLeft is 1>>
      <<print "Tomorrow is " + _item.label.replace("days until ", "")>>
    <<elseif _daysLeft is 0>>
      <<print "Today is " + _item.label.replace("days until ", "")>>
    <<else>>
      <<print _item.label.replace("days until ", "") + " has passed">>
    <</if>>
    </div>
  <<elseif _item.type is "hint">>
    <<set _hintText to setup.getSidebarHint()>>
    <<if _hintText>>
      <div class="sidebar-item hint-item" id="sidebar-hint-<<print _si>>">
        <<print _hintText>>
      </div>
    <</if>>
  <<elseif _item.type is "quest_next">>
    /* The next STEP, on every screen — as opposed to trait_status_text, which is the
       next STATE. A game shipped with four band strings in the sidebar and no verb, no
       place and no person anywhere in the always-visible chrome: a player who never
       opened the Quests page had no direction at all. Renders the same goal block as
       the Quests page and the npc_panel "next" row (setup.renderQuestsGoalBlock), so
       there is one implementation of what an objective looks like, not three.
       `npc_id` picks that character's live card; omitted, it takes the live tier cards
       in file order. `max` caps how many render (default 3). Terminal cards are
       skipped: they carry no goals and would render a bare completion badge forever. */
    <<if setup.renderQuestsGoalBlock and setup.evaluateGoals>>
      <<set _qnCards to []>>
      <<if _item.npc_id>>
        <<set _qnOne to setup.pickQuestsCard(_item.npc_id)>>
        <<if _qnOne>><<run _qnCards.push(_qnOne)>><</if>>
      <<else>>
        <<set _qnCards to setup.pickQuestsCards("story_goals") || []>>
      <</if>>
      <<set _qnMax to _item.max || 3>>
      <<set _qnShown to 0>>
      <<for _qi to 0; _qi lt _qnCards.length; _qi++>>
        <<set _qnCard to _qnCards[_qi]>>
        <<if _qnShown lt _qnMax and _qnCard and _qnCard.goals and _qnCard.goals.length gt 0 and not _qnCard.terminal>>
          <<set _qnBlock to setup.renderQuestsGoalBlock(_qnCard, setup.evaluateGoals(_qnCard))>>
          <<if _qnBlock>>
            <<set _qnShown to _qnShown + 1>>
            <div class="sidebar-item quest-next-item" id="sidebar-questnext-<<print _si>>-<<print _qi>>">
              <<print _qnBlock>>
            </div>
          <</if>>
        <</if>>
      <</for>>
    <</if>>
  <<elseif _item.type is "trait_bar">>
    <<set _tbOwner to _item.trait_owner || "player">>
    <<set _tbKey to _item.trait>>
    <<if _tbOwner is "npc">>
      <<set _tbNpcId to _item.npc_id>>
      <<set _tbNpcObj to (setup.npc_slug_map && setup.npc_slug_map[_tbNpcId]) ? State.variables.npcs[setup.npc_slug_map[_tbNpcId]] : (State.variables.npcs ? State.variables.npcs[_tbNpcId] : null)>>
      <<set _traitVal to (_tbNpcObj && _tbNpcObj.core_traits) ? (_tbNpcObj.core_traits[_tbKey] || 0) : 0>>
    <<else>>
      <<set _traitVal to ($player && $player.core_traits) ? ($player.core_traits[_tbKey] || 0) : 0>>
    <</if>>
    <<set _traitMax to _item.max || 100>>
    <<set _traitLabel to _item.label || _tbKey>>
    <<set _traitPct to Math.max(0, Math.min(100, (_traitVal / _traitMax) * 100))>>
    <<set _tbTier to "">>
    <<if _item.color_tiers>>
      <<for _ti to 0; _ti lt _item.color_tiers.length; _ti++>>
        <<if _tbTier is "" and _traitPct lte (_item.color_tiers[_ti].up_to)>>
          <<set _tbTier to _item.color_tiers[_ti].class>>
        <</if>>
      <</for>>
    <</if>>
    <<set _tbBandText to "">>
    <<set _tbBandIcon to "">>
    <<if _item.bands>>
      <<for _bi to 0; _bi lt _item.bands.length; _bi++>>
        <<set _bb to _item.bands[_bi]>>
        <<if _tbBandText is "" and _bb.min isnot undefined and _bb.max isnot undefined and _traitVal gte _bb.min and _traitVal lte _bb.max>>
          <<set _tbBandText to _bb.text>>
          <<set _tbBandIcon to _bb.icon || "">>
        <</if>>
      <</for>>
    <</if>>
    <div class="sidebar-item trait-bar-item" id="sidebar-trait-bar-<<print _si>>">
      <div class="trait-bar-label">
        <<if _item.hide_value is true>>
          <<print _traitLabel>>
        <<else>>
          <<print _traitLabel>>: <<print Math.floor(_traitVal)>> / <<print _traitMax>>
        <</if>>
      </div>
      <div class="trait-bar-bg">
        <div class="trait-bar-fill <<print _tbTier>>" style="width: <<print _traitPct>>%"></div>
        <<if _tbBandText isnot "">>
          <span class="trait-bar-band-text"><<print (_tbBandIcon ? _tbBandIcon + " " : "") + _tbBandText>></span>
        <</if>>
      </div>
    </div>
  <<elseif _item.type is "trait_status_text">>
    <<set _tsOwner to _item.trait_owner || "player">>
    <<set _tsKey to _item.trait>>
    <<if _tsOwner is "npc">>
      <<set _tsNpcId to _item.npc_id>>
      <<set _tsNpcObj to (setup.npc_slug_map && setup.npc_slug_map[_tsNpcId]) ? State.variables.npcs[setup.npc_slug_map[_tsNpcId]] : (State.variables.npcs ? State.variables.npcs[_tsNpcId] : null)>>
      <<set _tsVal to (_tsNpcObj && _tsNpcObj.core_traits) ? (_tsNpcObj.core_traits[_tsKey] || 0) : 0>>
    <<else>>
      <<set _tsVal to ($player && $player.core_traits) ? ($player.core_traits[_tsKey] || 0) : 0>>
    <</if>>
    <<set _tsText to "">>
    <<set _tsIcon to "">>
    <<if _item.bands>>
      <<for _bi to 0; _bi lt _item.bands.length; _bi++>>
        <<set _bb to _item.bands[_bi]>>
        <<set _bMin to (_bb.min isnot undefined) ? _bb.min : -1e9>>
        <<set _bMax to (_bb.max isnot undefined) ? _bb.max : 1e9>>
        <<if _tsText is "" and _tsVal gte _bMin and _tsVal lte _bMax>>
          <<set _tsText to _bb.text>>
          <<set _tsIcon to _bb.icon || "">>
        <</if>>
      <</for>>
    <</if>>
    <<if _tsText isnot "">>
      <div class="sidebar-item trait-status-text-item">
        <<if _item.label>><div class="band-header"><<print _item.label>></div><</if>>
        <span class="band-value"><<print (_tsIcon ? _tsIcon + " " : "") + _tsText>></span>
      </div>
    <</if>>
  <<elseif _item.type is "trait_decay_warning">>
    <!-- E20: render an amber warning when a decaying trait dropped today AND
         is within 2.0 of its next stage gate. setup.getDecayWarnings() walks
         the configured thresholds and compares last_day_snapshot vs current. -->
    <<set _decayWarnings to setup.getDecayWarnings(_item.thresholds || {})>>
    <<for _dw range _decayWarnings>>
      <div class="sidebar-item trait-decay-warning-item">
        ⚠ <<print _dw.text>>
      </div>
    <</for>>
  <<elseif _item.type is "passes">>
    <div class="sidebar-item passes-item" id="sidebar-passes-<<print _si>>">
      <<for _pi to 0; _pi lt setup.passes.length; _pi++>>
        <<set _pass to setup.passes[_pi]>>
        <<set _remaining to setup.getPassDaysRemaining(_pass.id)>>
        <<if _remaining gte 0>>
          <div class="pass-entry pass-active" id="pass-display-<<print _pass.id>>">
            <<print (_pass.icon || "") + " " + _pass.name + ": " + _remaining + "d">>
          </div>
        <</if>>
      <</for>>
    </div>
  <<elseif _item.type is "inventory">>
    <div class="sidebar-item inventory-item" id="sidebar-inventory-<<print _si>>">
      <<for _ii to 0; _ii lt setup.items.length; _ii++>>
        <<set _itm to setup.items[_ii]>>
        <<set _count to setup.getItemCount(_itm.id)>>
        <<if _count gt 0>>
          <div class="inventory-entry" id="inventory-display-<<print _itm.id>>">
            <<print (_itm.icon || "") + " " + _itm.name + ": " + _count>>
          </div>
        <</if>>
      <</for>>
    </div>
  <<elseif _item.type is "trait_words">>
    <<set _twOwner to _item.trait_owner || "player">>
    <<set _twKey to _item.trait>>
    <<if _twOwner is "npc">>
      <<set _twNpcId to _item.npc_id>>
      <<set _twNpcObj to (setup.npc_slug_map && setup.npc_slug_map[_twNpcId]) ? State.variables.npcs[setup.npc_slug_map[_twNpcId]] : (State.variables.npcs ? State.variables.npcs[_twNpcId] : null)>>
      <<set _twVal to (_twNpcObj && _twNpcObj.core_traits) ? (_twNpcObj.core_traits[_twKey] || 0) : 0>>
    <<else>>
      <<set _twVal to ($player && $player.core_traits) ? ($player.core_traits[_twKey] || 0) : 0>>
    <</if>>
    <<set _twMatched to "">>
    <<set _twFound to false>>
    <<if _item.bands>>
      <<for _bi to 0; _bi lt _item.bands.length; _bi++>>
        <<if not _twFound>>
          <<set _twBand to _item.bands[_bi]>>
          <<if _twBand.flag>>
            <<if $flags and $flags[_twBand.flag] is true>>
              <<set _twMatched to _twBand.text>>
              <<set _twFound to true>>
            <</if>>
          <<elseif _twBand.min isnot undefined and _twBand.max isnot undefined>>
            <<if _twVal gte _twBand.min and _twVal lte _twBand.max>>
              <<set _twMatched to _twBand.text>>
              <<set _twFound to true>>
            <</if>>
          <</if>>
        <</if>>
      <</for>>
    <</if>>
    <<if _twMatched isnot "">>
      <div class="sidebar-item trait-words-item" id="sidebar-trait-words-<<print _si>>">
        <<if _item.label>><div class="band-header"><<print _item.label>></div><</if>>
        <span class="band-value"><<print _twMatched>></span>
      </div>
    <</if>>
  <<elseif _item.type is "stage_label">>
    /* E11: render "<prefix>: <stage label>" sourced from arc_stages.
       Stage value lives in $player.core_traits[<slug>_stage] (integer).
       Out-of-range value → highest-defined label. Undefined trait → just
       the prefix with no colon. Empty arc_stages → renders nothing. */
    <<set _slNpcId to _item.npc_id>>
    <<set _slStages to (setup.npc_arc_stages && setup.npc_arc_stages[_slNpcId]) ? setup.npc_arc_stages[_slNpcId] : []>>
    <<set _slRawStage to ($player && $player.core_traits) ? $player.core_traits[_slNpcId + "_stage"] : undefined>>
    <<set _slPrefix to _item.prefix>>
    <<if not _slPrefix>>
      <<set _slUuid to (setup.npc_slug_map && setup.npc_slug_map[_slNpcId]) ? setup.npc_slug_map[_slNpcId] : _slNpcId>>
      <<set _slNpcObj to State.variables.npcs ? State.variables.npcs[_slUuid] : null>>
      <<set _slPrefix to _slNpcObj ? (_slNpcObj.name || _slNpcId) : _slNpcId>>
    <</if>>
    <<if _slStages.length gt 0 and _slRawStage isnot undefined>>
      <<set _slIdx to Math.max(0, Math.min(Number(_slRawStage), _slStages.length - 1))>>
      <<set _slLabel to _slStages[_slIdx]>>
      <div class="sidebar-item stage-label-item" id="sidebar-stage-label-<<print _si>>">
        <<print _slPrefix>>: <<print _slLabel>>
      </div>
    <<elseif _slPrefix>>
      <div class="sidebar-item stage-label-item" id="sidebar-stage-label-<<print _si>>">
        <<print _slPrefix>>
      </div>
    <</if>>
  <<elseif _item.type is "npc_panel">>
    /* RTS-style per-NPC card: name header + rows (arousal band / corruption / location).
       Location uses setup.getNpcLocation — the SAME schedule source the Schedule page uses. */
    <<set _npId to _item.npc_id>>
    <<set _npObj to (setup.npc_slug_map && setup.npc_slug_map[_npId]) ? State.variables.npcs[setup.npc_slug_map[_npId]] : (State.variables.npcs ? State.variables.npcs[_npId] : null)>>
    <<if _npObj>>
      <<set _npRows to _item.rows || ["arousal"]>>
      <<set _npHeader to _item.label || _npObj.name || _npId>>
      <div class="sidebar-item npc-panel-item" id="sidebar-npc-panel-<<print _si>>">
        <div class="npc-panel-header"><<print _npHeader>></div>
        <<for _npri to 0; _npri lt _npRows.length; _npri++>>
          <<set _npRow to _npRows[_npri]>>
          <<if _npRow is "arousal">>
            <<if not (setup.hiddenTraits && setup.hiddenTraits.includes("arousal"))>>
              <<set _npAr to (_npObj.core_traits) ? (_npObj.core_traits.arousal || 0) : 0>>
              <<set _npBands to _item.arousal_bands || [{"min":0,"max":0,"text":"❄️"},{"min":1,"max":1,"text":"🔥"},{"min":2,"max":2,"text":"🔥🔥"},{"min":3,"max":3,"text":"🔥🔥🔥"}]>>
              <<set _npArText to "">>
              <<for _nbi to 0; _nbi lt _npBands.length; _nbi++>>
                <<set _nb to _npBands[_nbi]>>
                <<if _npArText is "" and _nb.min isnot undefined and _nb.max isnot undefined and _npAr gte _nb.min and _npAr lte _nb.max>>
                  <<set _npArText to _nb.text>>
                <</if>>
              <</for>>
              <div class="sidebar-row"><span class="sidebar-label">🔥 Arousal</span> <span class="sidebar-value"><<print _npArText>></span></div>
            <</if>>
          <<elseif _npRow is "corruption">>
            <<if not (setup.hiddenTraits && setup.hiddenTraits.includes("corruption"))>>
              <<set _npCorr to (_npObj.core_traits) ? (_npObj.core_traits.corruption || 0) : 0>>
              <<set _npCorrOut to _npCorr>>
              <<if _item.corruption_max_value isnot undefined and _npCorr gte _item.corruption_max_value>>
                <<set _npCorrOut to (_item.corruption_max_label || "MAX")>>
              <</if>>
              <div class="sidebar-row"><span class="sidebar-label">🫦 Corruption</span> <span class="sidebar-value"><<print _npCorrOut>></span></div>
            <</if>>
          <<elseif _npRow is "location">>
            <<set _npLoc to setup.getNpcLocation(_npId)>>
            <<set _npLocName to _npLoc ? (setup._locNameFromUuid(_npLoc.location) || _npLoc.location) : (_item.away_label || "Away")>>
            <div class="sidebar-row"><span class="sidebar-label">📍 Location</span> <span class="sidebar-value"><<print _npLocName>></span></div>
          <<elseif _npRow is "next">>
            /* Next-milestone block — EXACT Quests-page parity: reuses setup.renderQuestsGoalBlock, so
               the card shows the same goal block as the Quests page — 🎯 To advance + ◯ live progress
               (climbing) / 🔓 Ready + 📍 + 🕒 (ready) / ✓ Arc complete (terminal). No flavor/tip text. */
            <<if setup.pickQuestsCard and setup.renderQuestsGoalBlock>>
              <<set _npCard to setup.pickQuestsCard(_npId)>>
              <<if _npCard>>
                <<set _npGoalBlock to setup.renderQuestsGoalBlock(_npCard, setup.evaluateGoals(_npCard))>>
                <<if _npGoalBlock>>
                  <div class="npc-panel-next"><<print _npGoalBlock>></div>
                <</if>>
              <</if>>
            <</if>>
          <</if>>
        <</for>>
      </div>
    <</if>>
  <</if>>
<</for>>
</div>
<</if>>
<</widget>>

"""

        phone_widget = ""
        if self.phone_enabled:
            phone_widget = """
<<widget "phoneButton">>
<<if setup.phone_enabled and (setup.phone_purchase_flag === '' or (State.variables.flags and State.variables.flags[setup.phone_purchase_flag]))>>
<<set _phoneUnread to setup.getPhoneUnreadCount()>>
<div id="phone-sidebar-btn" class="phone-btn-item">
  <<link "Phone">><<script>>setup.openPhone();<</script>><</link>><span class="nav-i">📱</span>
  <<if _phoneUnread gt 0>>
    <span class="phone-badge"><<print (_phoneUnread gt 9 ? "9+" : _phoneUnread)>></span>
  <</if>>
</div>
<</if>>
<</widget>>

"""

        # State-reactive player portrait widget (opt-in). Renders one image chosen by
        # setup.getPlayerPortrait(); the temp-var @src="_pimg" directive interpolates the
        # ready-prefixed path (NOT src="@_pimg"). Missing file hides via onerror.
        player_portrait_widget = ""
        if self.player_portrait_enabled:
            player_portrait_widget = """
<<widget "playerPortrait">>
<<if setup.player_portrait_enabled and setup.player_portrait>>
<<set _pimg to setup.getPlayerPortrait()>>
<<if _pimg>>
<div class="sidebar-player-portrait"><img @src="_pimg" @alt="$player.name" onerror="this.style.display='none';"></div>
<</if>>
<</if>>
<</widget>>

"""

        active_modifiers_widget = """
<<widget "activeModifiers">>
<<if $game_state && $game_state.active_modifiers && Object.keys($game_state.active_modifiers).length gt 0>>
<div id="sidebar-modifiers-widget" class="traits-display">
  <div class="traits-header">Active Effects</div>
  <<set _modKeys to Object.keys($game_state.active_modifiers)>>
  <<for _mi to 0; _mi lt _modKeys.length; _mi++>>
    <<set _mod to $game_state.active_modifiers[_modKeys[_mi]]>>
    <<set _hoursLeft to (_mod.expires_day - $game_state.time_state.day) * 24 + (_mod.expires_hour - $game_state.time_state.current_hour)>>
    <div class="modifier-badge"><<print _mod.name>> (<<print _hoursLeft>>h)</div>
  <</for>>
</div>
<</if>>
<</widget>>

"""

        # E7: counter increment / decrement widgets — thin wrappers over
        # setup.applyAndNotifyTrait. Always emitted; no dev-mode gate.
        # Usage: <<inc trait_name>> or <<inc trait_name 3>> (and <<dec ...>>).
        counter_widgets = """
<<widget "inc">>
<<set _incTrait to $args[0]>>
<<set _incBy to ($args[1] != null) ? Number($args[1]) : 1>>
<<script>>setup.applyAndNotifyTrait("player", null, _incTrait, "add", _incBy, false, null);<</script>>
<</widget>>

<<widget "dec">>
<<set _decTrait to $args[0]>>
<<set _decBy to ($args[1] != null) ? Number($args[1]) : 1>>
<<script>>setup.applyAndNotifyTrait("player", null, _decTrait, "add", -_decBy, false, null);<</script>>
<</widget>>

"""

        # Sidebar funding button. Spliced in as its own variable rather than left in
        # the surrounding literal, because that literal is a PLAIN string and the one
        # that follows it (the <style> block) carries ~300 unescaped braces — the
        # <<versionFooter>> widget is composed the same way, a few lines down, for the
        # same reason. Everything but the href is fixed markup.
        patreon_button_widget = f"""<<widget "patreonButton">>
<div id="patreon-btn-widget">
  <a href="{self._resolve_support_url()}" target="_blank" rel="noopener" class="patreon-link">
    <svg class="patreon-icon" viewBox="0 0 24 24" width="16" height="16">
      <path fill="currentColor" d="M15.386.524c-4.764 0-8.64 3.876-8.64 8.64 0 4.75 3.876 8.613 8.64 8.613 4.75 0 8.614-3.864 8.614-8.613C24 4.4 20.136.524 15.386.524M.003 23.537h4.22V.524H.003"/>
    </svg>
    Support Us
  </a>
</div>
<</widget>>"""

        return info_nav_script + dev_script_passage + time_widgets_start + dev_indicator + review_button + dev_jumps_widget + time_display_widget + sidebar_items_widget + phone_widget + player_portrait_widget + active_modifiers_widget + counter_widgets + player_traits_widget + npc_traits_widget + """

<<widget "playerFlags">>
<div id="flags-widget" class="traits-display">
  <div class="traits-header">Flags</div>
  <<if $flags and Object.keys($flags).length > 0>>
    <<set _fkeys to Object.keys($flags).sort()>>
    <ul class="traits-list">
      <<for _j to 0; _j lt _fkeys.length; _j++>>
        <<set _fk to _fkeys[_j]>>
        <li class="trait-item">
          <span class="trait-name"><<print _fk>></span>
          <span class="trait-value"><<print $flags[_fk] ? '✔' : '✖'>></span>
        </li>
      <</for>>
    </ul>
  <<else>>
    <div class="no-traits">No flags</div>
  <</if>>
  <div class="traits-hint">Set by choices and story logic.</div>
</div>
<</widget>>

<<widget "questsButton">>
<!-- Debug/legacy quest view - shows raw mechanics -->
<div id="quests-btn-widget">
  <<if passage() isnot "QuestsPage">><<link "Quests" "QuestsPage">><</link>><<else>><span class="nav-row">Quests</span><</if>><span class="nav-i">📋</span>
</div>
<</widget>>

<<widget "missingMediaButton">>
<<if $flags.debug_mode>>
<div id="missing-media-btn-widget" style="margin-bottom:8px;">
  <<if passage() isnot "MissingMediaPage">><<link "⚠️ Missing Media" "MissingMediaPage">><</link>><<else>>⚠️ Missing Media<</if>>
</div>
<</if>>
<</widget>>

<<widget "journalButton">>
<!-- Quests - active per-NPC quest cards -->
<div id="journal-btn-widget">
  <<if passage() isnot "QuestsPage">><<link "Quests" "QuestsPage">><</link>><<else>><span class="nav-row">Quests</span><</if>><span class="nav-i">📋</span>
</div>
<</widget>>

<<widget "tipsButton">>
<!-- Tips - game-level mechanics surface; conditional on [ui.tips_page] authored -->
<<if setup.tips_page && setup.tips_page.content>>
<div id="tips-btn-widget">
  <<if passage() isnot "TipsPage">><<link "Tips" "TipsPage">><</link>><<else>><span class="nav-row">Tips</span><</if>><span class="nav-i">💡</span>
</div>
<</if>>
<</widget>>

<<widget "statsButton">>
<div id="stats-btn-widget">
  <<if passage() isnot "StatsPage">><<link "Stats" "StatsPage">><</link>><<else>><span class="nav-row">Stats</span><</if>><span class="nav-i">📊</span>
</div>
<</widget>>

<<widget "scheduleButton">>
<<set _npcsWithSchedules to setup.getNpcsWithSchedules()>>
<<set _soloActivities to setup.getSoloActivitiesForToday()>>
<<if _npcsWithSchedules.length > 0 || _soloActivities.length > 0>>
<div id="schedule-btn-widget">
  <<if passage() isnot "SchedulePage">><<link "Schedules" "SchedulePage">><</link>><<else>><span class="nav-row">Schedules</span><</if>><span class="nav-i">📅</span>
</div>
<</if>>
<</widget>>

""" + patreon_button_widget + """

<<widget "flagsButton">>
<div id="flags-btn-widget">
  <<if passage() isnot "FlagsPage">><<link "Flags" "FlagsPage">><</link>><<else>><span class="nav-row">Flags</span><</if>><span class="nav-i">🚩</span>
</div>
<</widget>>

""" + version_footer_widget + story_caption + """

<style>
#time-widget {
    background: var(--theme-surface);
    border: 1px solid var(--theme-border);
    border-radius: 4px;
    padding: 8px;
    margin-bottom: 10px;
    font-family: var(--theme-font-mono);
    font-size: 14px;
    line-height: 1.2;
    color: var(--theme-text);
}

.time-line {
    text-align: center;
    margin-bottom: 4px;
    font-weight: bold;
    color: var(--theme-text-strong);
}

.control-line {
    text-align: center;
    font-size: 12px;
}

.time-btn {
    background: var(--theme-surface-alt);
    border: 1px solid var(--theme-border);
    border-radius: 3px;
    color: var(--theme-text-secondary);
    cursor: pointer;
    padding: 3px 6px;
    font-size: 12px;
    font-family: var(--theme-font-mono);
    font-weight: bold;
}

.time-btn:hover {
    background: var(--theme-border);
    color: var(--theme-text-strong);
    border-color: var(--theme-border);
}

#sidebar-items-widget {
    margin-bottom: 8px;
}
.sidebar-item {
    text-align: left;       /* one type system across the rail — left, theme sans (was centered mono) */
    padding: 6px 8px;
    font-size: 13px;
    line-height: 1.3;
}
.countdown-item {
    background: var(--theme-warning-bg);
    border: 1px solid var(--theme-warning);
    border-radius: 4px;
    color: var(--theme-warning-text);
    font-weight: bold;
}
.hint-item {
    background: var(--theme-success-bg);
    border: 1px solid var(--theme-success);
    border-radius: 4px;
    color: var(--theme-success);
    font-style: italic;
}
/* quest_next — the next STEP in the rail. Quieter than the hint card on purpose: it
   is there on every screen, so it reads as chrome rather than as an alert. The inner
   goal block reuses the Quests-page classes (.quests-goal / .quests-ready / .quests-where). */
.quest-next-item {
    padding: 4px 8px;
    border-left: 2px solid var(--theme-border);
    margin-bottom: 4px;
}

#traits-widget {
    background: var(--theme-surface);
    border: 1px solid var(--theme-border);
    border-radius: 4px;
    padding: 8px;
    margin-top: 8px;
    font-family: var(--theme-font-mono);
    font-size: 13px;
    color: var(--theme-text);
}

#flags-widget {
    background: var(--theme-surface);
    border: 1px solid var(--theme-border);
    border-radius: 4px;
    padding: 8px;
    margin-top: 8px;
    font-family: var(--theme-font-mono);
    font-size: 13px;
    color: var(--theme-text);
}

.traits-header {
    font-weight: bold;
    margin-bottom: 6px;
}

.traits-list {
    list-style: none;
    padding-left: 0;
    margin: 0;
}

.trait-item {
    display: flex;
    justify-content: space-between;
    border-bottom: 1px dashed var(--theme-border);
    padding: 2px 0;
}

.trait-name {
    color: var(--theme-text-secondary);
}

.trait-value {
    color: var(--theme-primary);
    font-weight: bold;
}

.no-traits {
    font-style: italic;
    color: var(--theme-text-muted);
}

.traits-hint {
    margin-top: 6px;
    font-size: 11px;
    color: var(--theme-text-muted);
}

#time-display, #current-day {
    font-family: var(--theme-font-mono);
    color: var(--theme-text-strong);
}

/* ===== Sidebar action buttons — ONE neutral pill family =====
   Structure is carried by neutral surfaces; the accent is reserved for hover
   (and .is-active). Replaces the old zoo: 4 tinted pills + 2 parchment-serif
   journal/tips. All six now share one filled surface pill, left-aligned, muted
   label, accent on hover, single 6px radius. */
/* ===== Sidebar action buttons — ONE neutral pill family =====
   The link (or the current-page .nav-row span) FILLS the whole padded box, so
   the ENTIRE box is clickable — not just the text. The icon overlays the right
   edge with pointer-events:none, so clicks there pass through to the link beneath.
   Structure in neutrals; accent reserved for hover. */
#phone-sidebar-btn,
#quests-btn-widget,
#journal-btn-widget,
#tips-btn-widget,
#cast-btn-widget,
#cheat-btn-widget,
#stats-btn-widget,
#schedule-btn-widget,
#flags-btn-widget {
    position: relative;          /* anchor the icon overlay + unread badge */
    background: var(--theme-surface);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 6px;
    margin: 8px 0 0 0;           /* uniform 8px rhythm — same as the cards */
}
/* the clickable fill: <a> in nav state, .nav-row span on the current page */
#phone-sidebar-btn a,
#quests-btn-widget a, #journal-btn-widget a, #tips-btn-widget a, #cast-btn-widget a, #cheat-btn-widget a, #stats-btn-widget a, #schedule-btn-widget a, #flags-btn-widget a,
#quests-btn-widget .nav-row, #journal-btn-widget .nav-row, #tips-btn-widget .nav-row, #cast-btn-widget .nav-row, #cheat-btn-widget .nav-row, #stats-btn-widget .nav-row, #schedule-btn-widget .nav-row, #flags-btn-widget .nav-row {
    display: block;
    width: 100%;
    box-sizing: border-box;
    padding: 8px 30px 8px 10px;  /* padded fill → whole box clickable; right room for the icon */
    text-align: left;            /* override the #ui-bar default center */
    color: var(--theme-text-muted);
    text-decoration: none;
    font-weight: 600;
}
#phone-sidebar-btn a:hover,
#quests-btn-widget a:hover, #journal-btn-widget a:hover, #tips-btn-widget a:hover, #cast-btn-widget a:hover, #cheat-btn-widget a:hover, #stats-btn-widget a:hover, #schedule-btn-widget a:hover, #flags-btn-widget a:hover {
    color: var(--theme-accent);
    text-decoration: none;
}
.nav-i {                         /* right-edge icon overlay; clicks pass through to the link */
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    pointer-events: none;
}
/* Sidebar spacing is margin-driven, not <br>-driven (kill stray empty-widget breaks). */
#story-caption br { display: none; }

/* State-reactive player portrait (opt-in) — the TOP-MOST sidebar image. The theme's
   global img rule does not reach sidebar imgs, so without this the raw image renders at
   natural size and overflows the narrow sidebar (you'd see a background edge, not the
   face). Constrain to the sidebar width and frame it as a 3:4 portrait crop centred a bit
   high, so a square or tall source shows the face/torso rather than the legs/background. */
.sidebar-player-portrait {
    margin: 0 0 12px 0;
    text-align: center;
}
.sidebar-player-portrait img {
    display: block;
    width: 100%;
    max-width: 100%;
    height: auto;
    aspect-ratio: 3 / 4;
    object-fit: cover;
    object-position: 50% 18%;
    border-radius: 6px;
}

/* Patreon Button in Sidebar */
#patreon-btn-widget {
    margin: 15px 0 0 0;
    padding: 15px 0 0 0;
    border-top: 1px solid #444;
    text-align: center;
}

/* Version / release-date footer at the very bottom of the sidebar */
.sidebar-version {
    margin-top: 8px;
    font-size: 11px;
    color: var(--theme-text-muted, #8a8a8a);
    text-align: center;
}""" + self._cast_page_css() + self._cheat_page_css() + """

/* Reduce gap between StoryCaption and Save/Restart menu */
#story-caption {
    margin-bottom: 0 !important;
    padding-bottom: 0 !important;
}

#menu-story {
    margin-top: 8px !important;
}

.patreon-link {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 12px;
    background: #f96854;
    color: #fff !important;
    border-radius: 4px;
    text-decoration: none;
    font-size: 0.9em;
    font-weight: bold;
}

.patreon-link:hover {
    background: #e85a47;
    text-decoration: none !important;
}

.patreon-icon {
    flex-shrink: 0;
}

.stats-card {
    background: var(--theme-surface);
    border: 1px solid var(--theme-border);
    border-radius: 6px;
    padding: 12px;
    margin-bottom: 12px;
}

.stats-name {
    font-weight: bold;
    font-size: 1.2em;
    color: var(--theme-text);
    margin-bottom: 8px;
    border-bottom: 1px solid var(--theme-border);
    padding-bottom: 6px;
}

.stats-traits {
    margin-top: 8px;
}

.stats-trait-item {
    display: flex;
    justify-content: space-between;
    padding: 4px 8px;
    border-bottom: 1px dashed var(--theme-border);
    color: var(--theme-text-strong);
}

.stats-trait-value {
    font-weight: bold;
    color: var(--theme-primary);
}

/* Story Arc Help Page Styles */
.chapter-context {
    background: linear-gradient(135deg, var(--theme-surface) 0%, var(--theme-surface-alt) 100%);
    padding: 12px 16px;
    border-radius: 8px;
    margin-bottom: 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.chapter-name {
    font-size: 1.1em;
    color: var(--theme-text);
    font-weight: bold;
}

.chapter-mood {
    font-size: 0.9em;
    color: var(--theme-text-muted);
    font-style: italic;
}

.available-section h3 {
    font-size: 1em;
    color: var(--theme-text-secondary);
    margin: 0 0 10px 0;
    border-bottom: 1px solid var(--theme-border);
    padding-bottom: 6px;
}

.help-card {
    background: var(--theme-surface);
    border: 1px solid var(--theme-border);
    border-radius: 6px;
    padding: 12px 16px;
    margin-bottom: 10px;
}

.node-name {
    font-weight: bold;
    color: var(--theme-text);
}

.node-hint {
    color: var(--theme-text-muted);
    font-size: 0.9em;
    margin-top: 4px;
}

.narrative-hint {
    background: var(--theme-warning-bg);
    border: 1px solid var(--theme-warning);
    border-radius: 6px;
    padding: 12px;
    margin: 16px 0;
}

.narrative-hint p {
    margin: 0;
    color: var(--theme-warning-text);
}

.progress-summary {
    text-align: center;
    color: var(--theme-text-muted);
    font-size: 0.9em;
    margin-top: 16px;
    padding-top: 12px;
    border-top: 1px solid var(--theme-border);
}

.no-quests-msg {
    font-style: italic;
    color: var(--theme-text-muted);
    padding: 10px;
}

/* Quest Page - Simplified One Activity Per NPC */
.npc-section {
    margin-bottom: 20px;
    padding: 16px;
    background: linear-gradient(135deg, var(--theme-surface) 0%, var(--theme-surface-alt) 100%);
    border-radius: 10px;
    border: 1px solid var(--theme-border);
}

.npc-name {
    font-size: 1.2em;
    color: var(--theme-text);
    margin: 0 0 12px 0;
    border-bottom: 2px solid var(--theme-primary);
    padding-bottom: 8px;
    font-weight: 600;
}

.guide-hint {
    font-size: 0.85em;
    color: #f0c040;
    font-style: italic;
}

.quest-available {
    color: var(--theme-success);
    font-weight: 500;
    padding: 10px 14px;
    background: rgba(40, 167, 69, 0.1);
    border-radius: 6px;
    border-left: 4px solid var(--theme-success);
}

/* E16: Stage hint two-part card. Flavor on top, goal block below. */
.stage-hint-card {
    padding: 12px 14px;
    background: rgba(40, 167, 69, 0.08);
    border-radius: 6px;
    border-left: 4px solid var(--theme-success);
    margin: 8px 0;
}
.stage-hint-flavor {
    font-style: italic;
    opacity: 0.75;
    margin-bottom: 10px;
    font-size: 0.95em;
}

/* Pattern 2 (2026-05-01) — auto-rendered structured goal block */
.stage-hint-goal-header {
    font-weight: 600;
    margin-bottom: 6px;
    color: var(--theme-success);
}
.stage-hint-goal ul {
    list-style: none;
    padding-left: 8px;
    margin: 4px 0;
}
.stage-hint-goal li {
    padding: 3px 0;
    font-family: var(--theme-font-mono, 'Courier New', monospace);
    font-size: 0.92em;
    line-height: 1.4;
}
.stage-hint-met {
    color: var(--theme-success);
    font-weight: 600;
    display: inline-block;
    width: 1.2em;
}
.stage-hint-unmet {
    color: var(--theme-text-muted);
    display: inline-block;
    width: 1.2em;
}
.stage-hint-met-row {
    color: var(--theme-success);
    opacity: 0.9;
}
.stage-hint-unmet-row {
    color: var(--theme-text);
    opacity: 0.85;
}
.stage-hint-progress {
    color: var(--theme-text-muted);
    margin-left: 6px;
    font-size: 0.88em;
}
.stage-hint-where {
    margin-top: 8px;
    font-size: 0.9em;
    opacity: 0.85;
    color: var(--theme-text);
    font-style: normal;
}
.stage-hint-tip {
    margin-top: 10px;
    padding: 6px 10px;
    background: rgba(255, 193, 7, 0.08);
    border-left: 3px solid var(--theme-warning, #ffc107);
    border-radius: 3px;
    font-size: 0.9em;
    line-height: 1.45;
    opacity: 0.92;
}
.stage-hint-path {
    margin-top: 6px;
    padding: 6px 8px;
    border-left: 2px solid var(--theme-accent, #4ecdc4);
    background: rgba(78, 205, 196, 0.05);
}
.stage-hint-path strong {
    color: var(--theme-accent, #4ecdc4);
    font-size: 0.92em;
}
/* Pattern 2 (2026-05-04) — Ready frame: shown when every gate of a stage
   transition's trigger evaluates true. Replaces the gate checklist with a
   compact "go here, this time window" surface. */
.stage-hint-ready {
    color: var(--theme-success);
    font-weight: 700;
    letter-spacing: 0.02em;
}

/* Pattern 2 (2026-05-09) — Arc-complete frame: shown when an author marks
   a hint template `arc_complete = true` (terminal stage in the slice).
   Quieter than Ready — reads as closure rather than an action prompt. */
.stage-hint-arc-complete {
    color: var(--theme-text-muted, #888);
    font-weight: 600;
    font-style: italic;
    letter-spacing: 0.02em;
}

.quest-locked {
    color: var(--theme-warning-text);
    font-weight: 500;
    padding: 10px 14px;
    background: rgba(255, 193, 7, 0.15);
    border-radius: 6px;
    border-left: 4px solid var(--theme-warning);
}

.quest-conditions {
    color: var(--theme-danger);
    font-weight: 500;
    padding: 10px 14px;
    background: rgba(220, 53, 69, 0.1);
    border-radius: 6px;
    border-left: 4px solid var(--theme-danger);
}

.quest-waiting {
    color: var(--theme-warning-text);
    font-weight: 500;
    padding: 10px 14px;
    background: rgba(255, 193, 7, 0.15);
    border-radius: 6px;
    border-left: 4px solid var(--theme-warning);
    font-style: italic;
}

.dev-canvas-info {
    background: var(--theme-primary);
    color: white;
    padding: 6px 10px;
    border-radius: 4px;
    margin-bottom: 10px;
    font-size: 11px;
    font-family: var(--theme-font-mono);
}

.quest-complete {
    color: var(--theme-success);
    font-style: italic;
    padding: 10px 14px;
    text-align: center;
}

.no-quests {
    color: var(--theme-text-muted);
    font-style: italic;
    padding: 12px;
    text-align: center;
}

/* Tips page — wrapped inside an .npc-section card frame on the page itself.
   Section headers (<h3>) use the same accent treatment as .npc-name dividers
   in the Quests page so the two pages read as the same family. */
.tips-page-content {
    line-height: 1.55;
    color: var(--theme-text);
}
.tips-page-content h3 {
    font-size: 1.05em;
    color: var(--theme-text);
    margin: 18px 0 8px;
    padding-bottom: 6px;
    border-bottom: 2px solid var(--theme-primary);
    font-weight: 600;
}
.tips-page-content h3:first-child {
    margin-top: 0;
}
.tips-page-content p {
    margin: 6px 0;
}
.tips-page-content strong {
    color: var(--theme-text);
    font-weight: 600;
}

/* Trait Requirement Link */
.trait-requirement-link {
    color: var(--theme-danger);
    text-decoration: underline;
    cursor: pointer;
}
.trait-requirement-link:hover {
    color: var(--theme-danger);
}

/* Trait Activities Modal Overlay */
.trait-modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.6);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 10000;
}

/* Modal Container */
.trait-modal {
    background: #fff;
    border-radius: 12px;
    max-width: 400px;
    width: 90%;
    max-height: 80vh;
    overflow: hidden;
    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
}

.trait-modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 20px;
    background: var(--theme-surface);
    border-bottom: 1px solid var(--theme-border);
}

.trait-modal-header h3 {
    margin: 0;
    font-size: 1.1em;
    color: #333;
}

.trait-modal-close {
    font-size: 24px;
    cursor: pointer;
    color: var(--theme-text-muted);
    line-height: 1;
}

.trait-modal-close:hover {
    color: #333;
}

.trait-modal-progress {
    padding: 12px 20px;
    background: rgba(220, 53, 69, 0.1);
    color: var(--theme-danger);
    font-weight: 500;
    text-align: center;
}

.trait-modal-body {
    padding: 16px 20px;
    max-height: 50vh;
    overflow-y: auto;
}

/* Activity List */
.trait-activity-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.trait-activity-list li {
    padding: 12px;
    border-bottom: 1px solid var(--theme-border);
}

.trait-activity-list li:last-child {
    border-bottom: none;
}

.activity-name {
    font-weight: 600;
    color: #333;
}

.activity-bonus {
    float: right;
    color: var(--theme-success);
    font-weight: 500;
}

.activity-hint {
    margin-top: 4px;
    color: var(--theme-text-muted);
    font-size: 0.9em;
    clear: both;
}

/* Effect Toast Notification */
.effect-toast {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(0, 0, 0, 0.85);
    color: var(--theme-success);
    padding: 10px 20px;
    border-radius: 6px;
    font-size: 14px;
    z-index: 10002;
    white-space: nowrap;
}

/* S4 — Threshold-publisher toast (gated_action). Distinct from the green
   effect-toast: amber/warning palette, italic, allows wrapping for the longer
   in-character explanation, slightly higher z-index so it doesn't get hidden
   behind the success toast when both fire on the same click. */
.effect-toast.notify-warning {
    background: rgba(255, 152, 0, 0.95);
    color: #1a1a1a;
    border-left: 4px solid #c66900;
    font-style: italic;
    white-space: normal;
    max-width: 480px;
    text-align: left;
    line-height: 1.4;
    z-index: 10003;
}

/* Game Intro - Top Left Aligned */
.game-intro {
    text-align: left;
}

/* Age Gate Section */
.age-gate {
    background: var(--theme-warning-bg);
    border: 1px solid var(--theme-warning);
    border-radius: 8px;
    padding: 20px;
    margin: 20px 0;
    text-align: center;
}

.age-warning {
    font-weight: bold;
    color: var(--theme-warning-text);
    margin-bottom: 15px;
}

.age-buttons {
    display: flex;
    flex-direction: column;
    gap: 10px;
    align-items: center;
}

/* Developer Intro Section (above age gate) */
.developer-intro {
    text-align: left;
    color: var(--theme-text-muted);
    margin: 20px 0;
}

/* Developer Footer Section (below age gate) */
.developer-footer {
    margin-top: 30px;
    padding-top: 20px;
    border-top: 1px solid var(--theme-border);
    text-align: center;
    color: var(--theme-text-muted);
    font-size: 0.9em;
}

.developer-intro a,
.developer-footer a {
    color: #f96854;
    text-decoration: none;
}

.developer-intro a:hover,
.developer-footer a:hover {
    text-decoration: underline;
}

.developer-about {
    line-height: 1.5;
    margin: 10px 0;
}

.support-link {
    margin-top: 8px;
}

.developer-footer .support-link {
    font-weight: bold;
}

/* Age Blocked Page */
.blocked-page {
    text-align: center;
    padding: 50px;
    color: var(--theme-danger);
    background: var(--theme-danger-bg);
    border-radius: 8px;
    margin: 50px auto;
    max-width: 400px;
}

/* Override SugarCube default vertical centering */
#story {
    align-items: flex-start !important;
    justify-content: flex-start !important;
    padding-top: 1em !important;
}

.passage {
    margin-top: 0 !important;
    padding-top: 0 !important;
}

/* New/Unvisited Canvas Highlight */
.new-canvas a {
    color: var(--theme-success) !important;
    font-weight: 600;
}
.new-canvas a::before {
    content: "✨ ";
}

/* Unlocked conditional choice highlight (in passages) */
.unlocked-choice a, .unlocked-choice .link-internal {
    color: var(--theme-warning) !important;
    font-weight: 600;
}
.unlocked-choice a::before, .unlocked-choice .link-internal::before {
    content: "\U0001f513 ";
}

/* Locked choice (visible but not available — Mode A) */
.locked-choice {
    color: var(--theme-text-muted);
    font-style: italic;
    cursor: not-allowed;
    opacity: 0.6;
    display: inline-block;
    padding: 2px 0;
}
.locked-choice::before {
    content: "\U0001f512 ";
}

/* Rejection choice (clickable but leads to rejection — Mode B) */
.rejection-choice a, .rejection-choice .link-internal {
    color: #b45555 !important;
    font-style: italic;
}
.rejection-choice a::before, .rejection-choice .link-internal::before {
    content: "\u26a0\ufe0f ";
}

/* Active modifier sidebar badge */
.modifier-badge {
    display: inline-block;
    background: rgba(168, 85, 247, 0.15);
    color: #c084fc;
    border: 1px solid rgba(168, 85, 247, 0.3);
    border-radius: 12px;
    padding: 2px 10px;
    font-size: 0.8em;
    font-style: italic;
    margin: 2px 0;
}

/* Unlocked choice canvas link highlight (in location activity list) */
.unlocked-choice-canvas a {
    color: var(--theme-warning) !important;
    font-weight: 600;
}
.unlocked-choice-canvas a::before {
    content: "\U0001f513 ";
}

/* Navigation New Content Indicator */
.nav-new {
    color: var(--theme-warning);
    font-weight: bold;
    font-size: 1.1em;
}

/* Navigation NPC Portrait Indicator */
.nav-npc-portrait {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    object-fit: cover;
    vertical-align: middle;
    margin-left: 4px;
    border: 2px solid var(--theme-border);
}

/* ===============================================
   VISUAL NAVIGATION GRID
   =============================================== */

.location-nav-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
    margin: 8px 0;
}

@media (min-width: 768px) {
    .location-nav-grid {
        grid-template-columns: repeat(3, 1fr);
    }
}

@media (min-width: 1024px) {
    .location-nav-grid {
        grid-template-columns: repeat(4, 1fr);
    }
}

/* Location Card */
.location-card {
    display: flex;
    flex-direction: column;
    background: #2a2a2a;
    border-radius: 8px;
    overflow: hidden;
    text-decoration: none !important;
    color: inherit !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    cursor: pointer;
}

.location-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

/* Card Image Area (5:2 aspect ratio - more compact) */
.location-card-image {
    width: 100%;
    padding-bottom: 40%; /* 5:2 ratio */
    background-size: cover;
    background-position: center;
    position: relative;
    background-color: #1a1a1a;
}

/* Placeholder silhouette for locations without images */
.location-card-placeholder {
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #2d2d3a 0%, #1a1a2a 100%);
}

.location-card-placeholder svg {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 60%;
    height: 60%;
    opacity: 0.5;
}

/* Card Content Area */
.location-card-content {
    padding: 6px 8px;
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.location-card-name {
    font-weight: 600;
    font-size: 0.9em;
    line-height: 1.2;
    color: var(--theme-text);
}

/* Indicators Row */
.location-card-indicators {
    display: flex;
    align-items: center;
    gap: 4px;
    flex-wrap: wrap;
}

/* NEW badge (replaces ! indicator in visual mode) */
.nav-new-badge {
    background: var(--theme-warning);
    color: #000;
    font-size: 0.65em;
    font-weight: bold;
    padding: 2px 5px;
    border-radius: 3px;
    text-transform: uppercase;
}

/* NPC portrait badges (smaller version for cards) */
.nav-npc-badge {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    object-fit: cover;
    border: 1px solid var(--theme-text-muted);
}

/* Locked destination card (lock-as-prose): shown but not clickable, with the reason */
.location-card-locked {
    opacity: 0.6;
    cursor: not-allowed;
    filter: grayscale(0.4);
}
.location-card-locked .location-card-image {
    filter: grayscale(0.6) brightness(0.85);
}
.nav-locked-reason {
    font-size: 0.7em;
    line-height: 1.25;
    color: var(--theme-text-muted);
    font-style: italic;
    margin-top: 2px;
}
/* Text-mode locked link */
.nav-link-locked {
    color: var(--theme-text-muted);
    font-style: italic;
}
/* Travel-cost tag on a nav destination (neutral, informational) */
.nav-cost-tag {
    font-size: 0.65em;
    color: var(--theme-text-muted);
    background: var(--theme-surface);
    border: 1px solid var(--theme-border, rgba(255,255,255,0.12));
    border-radius: 3px;
    padding: 1px 5px;
    margin-left: 4px;
    white-space: nowrap;
    font-variant-numeric: tabular-nums;
}

/* Exit Links Section (text-only, below grid) */
.location-nav-exits {
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid #444;
}

.location-nav-exits a {
    color: var(--theme-text-muted);
}

.location-nav-exits a:hover {
    color: #fff;
}

/* ===== NPC Portrait System (Location Interaction) ===== */
/* Grid of clickable NPC portraits shown at locations */
.location-npcs {
    display: flex;
    gap: 1.5rem;
    justify-content: center;
    padding: 1.5rem 0;
    flex-wrap: wrap;
}

.npc-portrait-card {
    text-align: center;
    cursor: pointer;
    transition: transform 0.2s ease;
    position: relative;
}

.npc-portrait-card:hover {
    transform: scale(1.08);
}

.npc-portrait-link {
    text-decoration: none !important;
    color: inherit !important;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.4rem;
}

.npc-portrait-img {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid var(--theme-text-muted);
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.npc-portrait-card:hover .npc-portrait-img {
    border-color: var(--theme-border);
    box-shadow: 0 0 12px rgba(200, 200, 200, 0.2);
}

/* Initial letter fallback for missing portraits */
.npc-portrait-placeholder {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: linear-gradient(135deg, #3a3a4a 0%, #2a2a3a 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.8rem;
    font-weight: 600;
    color: var(--theme-border);
    border: 3px solid var(--theme-text-muted);
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.npc-portrait-card:hover .npc-portrait-placeholder {
    border-color: var(--theme-border);
    box-shadow: 0 0 12px rgba(200, 200, 200, 0.2);
}

.npc-portrait-name {
    display: block;
    font-size: 0.85rem;
    color: var(--theme-text-muted);
    line-height: 1.2;
}

/* .npc-badge kept as base class for .npc-cost-badge (cost-blocked portraits).
   NEW/unlocked portrait border + badge classes removed 2026-05-25. */
.npc-badge {
    position: absolute;
    top: -4px;
    right: -4px;
    font-size: 0.6rem;
    font-weight: bold;
    padding: 2px 5px;
    border-radius: 8px;
    text-transform: uppercase;
}

/* Solo activity buttons (activities with no NPC) */
.location-solo-activities {
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid #333;
}

.solo-activity-btn {
    display: inline-block;
    padding: 0.4rem 1rem;
    margin: 0.3rem 0;
    background: var(--theme-surface);
    border: 1px solid var(--theme-border);
    border-radius: 4px;
    color: var(--theme-text) !important;
    text-decoration: none !important;
    transition: background 0.2s ease;
}

.solo-activity-btn:hover {
    background: var(--theme-surface-alt);
    color: var(--theme-text-strong) !important;
}

/* ===== Cost-blocked states ===== */

/* Blocked NPC portraits (greyed out) */
.npc-portrait-blocked .npc-portrait-img,
.npc-portrait-blocked .npc-portrait-placeholder {
    filter: grayscale(70%) brightness(0.6);
    border-color: #444;
}
.npc-portrait-blocked .npc-portrait-name {
    color: var(--theme-text-muted);
}
.npc-portrait-blocked:hover {
    transform: scale(1.04);
}

/* Cost badge on portraits */
.npc-cost-badge {
    background: var(--theme-danger);
    color: #fff;
    font-size: 0.55rem;
    position: absolute;
    bottom: 18px;
    left: 50%;
    transform: translateX(-50%);
    white-space: nowrap;
    padding: 1px 6px;
    border-radius: 8px;
    top: auto;
    right: auto;
}

/* Blocked solo activities */
.solo-activity-blocked {
    opacity: 0.5;
}
.solo-activity-blocked:hover {
    opacity: 0.7;
}
.solo-cost-tag {
    font-size: 0.75em;
    color: var(--theme-danger);
}
/* E21 — author-opt-in cooldown entry. Non-clickable dimmed text. */
.solo-activity-cooldown {
    display: inline-block;
    padding: 4px 8px;
    margin-bottom: 2px;
    color: var(--theme-border);
    font-style: normal;
    font-size: 0.9em;
    opacity: 0.65;
}
.solo-activity-cooldown em {
    font-size: 0.85em;
    opacity: 0.85;
}

/* Cost-blocked passage message */
.cost-blocked-message {
    text-align: center;
    padding: 2rem;
    color: var(--theme-text-muted);
    font-style: italic;
}
.cost-blocked-message p {
    margin-bottom: 1rem;
}

/* ===== E20: Sidebar decay warning ===== */
.trait-decay-warning-item {
    margin-top: 0.5rem;
    padding: 6px 10px;
    background: rgba(255, 193, 7, 0.18);
    border-left: 3px solid var(--theme-warning);
    border-radius: 4px;
    color: var(--theme-warning-text);
    font-size: 0.78rem;
    line-height: 1.35;
}

/* ===== Sidebar band cards (trait_words / trait_status_text / trait_bar) =====
   ONE card language. Structure is carried by NEUTRAL surfaces + spacing; the
   accent is RESERVED for signal (hover / .is-active), never the resting stripe.
   trait_words is the HERO stat (corruption / identity) — raised surface + larger
   value so it anchors the top of the rail instead of reading as a peer card. */
.trait-words-item,
.trait-status-text-item,
.trait-bar-item {
    text-align: left;
    margin-top: 0.5rem;
    padding: 8px 10px;
    background: var(--theme-surface);
    border: 1px solid rgba(255, 255, 255, 0.07);   /* hairline — survives across tiers, clears the eye (the old #333 border was ~1.3:1, invisible) */
    border-left: 3px solid rgba(255, 255, 255, 0.10);   /* neutral at rest */
    border-radius: 6px;
    color: var(--theme-text);
    font-size: 0.78rem;
    line-height: 1.35;
}
/* HERO: the identity word-state (corruption) reads as the top-of-rail anchor. */
.trait-words-item {
    background: var(--theme-surface-hover);   /* +0.08 lighter — the existing 'raised' tier */
}
.trait-words-item .band-value {
    font-size: 1.05rem;
    line-height: 1.25;
}
/* The accent/semantic left-stripe is a SCARCE SIGNAL (active / urgent / locked),
   not decoration — a row earns it; toggled by emitting the class on that item. */
.sidebar-item.is-active { border-left-color: var(--theme-accent); }
.sidebar-item.is-urgent { border-left-color: var(--theme-warning); }
.sidebar-item.is-locked { border-left-color: var(--theme-danger); }
/* the label, rendered as a compact card header (matches .npc-panel-header) */
.band-header {
    color: var(--theme-text-muted);
    font-weight: bold;
    font-size: 11px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 4px;
}
/* the value line (word / status text) */
.band-value {
    color: var(--theme-text-strong);
    font-weight: 600;
    font-size: 0.86rem;
    font-variant-numeric: tabular-nums lining-nums;   /* columns don't jitter as values change */
}

/* ===== trait_bar — banded word over a flat fill bar ===== */
.trait-bar-label {
    color: var(--theme-text-muted);
    font-weight: bold;
    font-size: 11px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 5px;
}
.trait-bar-bg {
    height: 8px;
    background: var(--theme-surface-alt);
    border-radius: 6px;
    overflow: hidden;
    position: relative;
}
.trait-bar-fill {
    height: 100%;
    background: var(--theme-accent);
    border-radius: 6px;
    transition: width 0.3s ease;
}
/* Banded mode: when a trait_bar's band-text overlay is rendered, the bg grows
   to fit the overlay text. Gated via :has() so non-banded bars stay at 8px. */
.trait-bar-bg:has(.trait-bar-band-text) {
    height: 26px;
    border-radius: 6px;
}
.trait-bar-band-text {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding-right: 9px;
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--theme-text-strong);
    font-variant-numeric: tabular-nums lining-nums;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.55);
    pointer-events: none;
    z-index: 2;
    white-space: nowrap;
}
/* Built-in value-tier fills — flat & matte (set a tier class via color_tiers).
   Authors can override by shipping their own .trait-bar-fill.<class> rules. */
.trait-bar-fill.low {
    background: #3b82c4;
}
.trait-bar-fill.medium {
    background: #d98a3a;
}
.trait-bar-fill.high {
    background: #d65a5a;
}

/* NPC panel card (npc_panel sidebar item) — RTS House-card: header strip + label/value rows */
.npc-panel-item {
    text-align: left;
    padding: 0;
    margin-top: 0.5rem;
    background: var(--theme-surface);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 6px;
    overflow: hidden;
}
.npc-panel-header {
    padding: 5px 8px;
    background: var(--theme-surface-alt);
    border-bottom: 1px solid rgba(255, 255, 255, 0.07);
    color: var(--theme-text-strong);
    font-weight: bold;
    font-size: 12px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.npc-panel-item .sidebar-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    padding: 4px 8px;
    font-size: 12px;
}
.npc-panel-item .sidebar-label {
    color: var(--theme-text-muted);
    white-space: nowrap;
}
.npc-panel-item .sidebar-value {
    color: var(--theme-text-strong);
    font-weight: 500;
    text-align: right;
    font-variant-numeric: tabular-nums lining-nums;
}
.npc-panel-next {
    margin-top: 4px;
    padding: 4px 8px 2px;
    border-top: 1px solid rgba(255, 255, 255, 0.07);
}
/* the inner goal block reuses the Quests-page classes (.quests-goal/.quests-ready/.quests-where) */

/* Dev Mode Controls */
.dev-adj-btn {
    background: var(--theme-text-muted);
    color: white;
    border: none;
    border-radius: 3px;
    width: 20px;
    height: 20px;
    font-size: 14px;
    font-weight: bold;
    cursor: pointer;
    padding: 0;
    line-height: 1;
    vertical-align: middle;
}

.dev-adj-btn:hover {
    background: var(--theme-text-muted);
}

.trait-controls {
    display: flex;
    align-items: center;
    gap: 4px;
}

.trait-controls .trait-value {
    min-width: 24px;
    text-align: center;
}

/* Portrait System */
.portrait {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    overflow: hidden;
    flex-shrink: 0;
    background: var(--theme-surface-alt);
    display: flex;
    align-items: center;
    justify-content: center;
}

.portrait img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.portrait-placeholder svg {
    width: 70%;
    height: 70%;
}

/* Dialog Block — the face floats, and ONE text flow runs beside and under it.

   Two earlier shapes were built and rejected in the same session, and the reasons are
   worth keeping because both look reasonable on paper:

     · a fixed-width speaker COLUMN — every box's text started at the same x, which was
       the point, but the identity stack drove the height: a one-line box measured 120px
       carrying 28px of text, so 77% of it was not text.
     · the same column FLOATED — height dropped to 68px, but a fixed column still holds
       its width whether the name needs it or not, which left a wide empty gap between
       "husband" and the line the character was actually saying.

   The gap was the complaint, and a column of any kind causes it. So there is no column:
   the name, the role and the speech are one flow. Whichever of name/role comes last takes
   a colon and the speech continues straight from it, wrapping beside the portrait and then
   under it.

       ┌──────┐ Dorn
       │ face │ husband: Back Friday. Late.
       └──────┘ ...and the rest wraps under the face.

   ⚠️ FLOAT, NOT FLEX. Neither flex nor grid can make text wrap around a box; only a float
   can. `display: block` here is the mechanism, not a style choice.

   ⚠️ The 480px breakpoint the floated column needed is GONE, and should not come back.
   It existed because a fixed column plus a face ate 142px of a 360px screen and left a
   14-character first line. With no column there is nothing to reserve, so the phone and
   the laptop want the same rules. */
.dialog-block {
    /* ⚠️ THE FACE IS DERIVED FROM THE IDENTITY, NOT THE OTHER WAY ROUND. The label beside
       the portrait is two rows — the name's own row, and the row the role SHARES with the
       first words of the speech — so its height is `name-row + leading` no matter what the
       portrait does. Sizing the rows as a fraction of the face made the label overflow it
       by 8-9px, and could not be fixed by changing the fraction: solving
       `0.7*F + leading <= F` needs `F >= leading / 0.3`, which at a 28px leading is a 93px
       portrait. Deriving the face from the rows makes `identity == face` true by
       construction, at any font size. */
    --dlg-lead:     1.5em;
    --dlg-name-row: 1.35em;
    --dlg-face:     calc(var(--dlg-name-row) + var(--dlg-lead));
    display: block;
    margin: 10px 0;
    padding: 10px;
    border-radius: 8px;
    color: var(--theme-text);
}

/* ⚠️ MANDATORY. A block containing only floats collapses to zero height, and it looks
   fine until a box has a short line. `::after` rather than `overflow: hidden`: same
   effect on height, no risk of clipping a rounded portrait. */
.dialog-block::after {
    content: "";
    display: block;
    clear: both;
}

/* Scoped to the dialog block: the global `.portrait` rule above is 40px and still serves
   the thought bubble and every other caller. */
.dialog-block > .portrait {
    float: left;
    width: var(--dlg-face);
    height: var(--dlg-face);
    margin: 0 10px 4px 0;
}

.dialog-player {
    border-left: 4px solid var(--theme-primary);
    background: var(--theme-primary-bg);
}

.dialog-player strong {
    color: var(--theme-primary);
}

.dialog-npc {
    border-left: 4px solid var(--theme-text-muted);
    background: var(--theme-surface);
}

.dialog-npc strong {
    color: var(--theme-text-secondary);
}

/* Normal flow on purpose — this is what wraps around the floated face, and it now holds
   the name and role as well as the speech.
   ⚠️ `overflow-wrap: anywhere` stays: one long unbroken string would otherwise overflow
   and give the phone a horizontal scrollbar, invisible at desktop width. */
.dialog-content {
    overflow-wrap: anywhere;
    line-height: var(--dlg-lead);
}

/* The name takes a row of its own ONLY when a role follows it, so the role can sit under
   it. With no role there is nothing to sit under, and `dlg-inline` keeps the name on the
   speech's own line. */
/* The name takes a row of its own ONLY when a role follows it, and the two are
   proportioned to the FACE — 70% of its height for the name, 30% for the role — so the
   identity reads as one unit standing the same height as the portrait beside it. Both
   are derived from `--dlg-face` rather than fixed, so they track it at every viewport.
   The font sizes carry floors: 24% of a 36px phone face is 8.6px, which is too small to
   read, so `max()` holds the role at 9px there. */
.dialog-content strong {
    display: block;
    height: var(--dlg-name-row);
    line-height: var(--dlg-name-row);
    font-size: 1.05em;
}

/* ⚠️ The role-less case shares its line with the speech, so it must NOT inherit the 70%
   line box above — that would stretch the line the character is speaking on. It keeps
   the surrounding leading instead. */
.dialog-content strong.dlg-inline {
    display: inline;
    height: auto;
    line-height: inherit;
    font-size: 1em;
}

/* F10 — the short label under a speaker's name. Quieter than the name, because it is a
   label and must not compete with the line the character is actually saying. INLINE, so
   the speech continues from it rather than starting a new row.
   ⚠️ Its 30% is the height of the ROLE's own inline box. The line it sits on also holds
   the first words of the speech, and a line box is as tall as its tallest inline box, so
   that line renders at the speech's leading — the 30% governs the label, not the row. */
.dialog-role {
    display: inline;
    font-size: max(9px, 0.62em);
    line-height: inherit;
    color: var(--theme-text-muted, #8a8a8a);
}

/* The colon lives in CSS so the role and name TEXT stay clean for anything that reads
   them. It goes on whichever of the two is last. */
.dialog-role::after,
.dialog-content strong.dlg-inline::after {
    content: ":";
}

/* Thought Bubble Block (S8) — interior monologue, paired with cascade beats */
.thought-bubble {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 8px 0 8px 24px;
    padding: 8px 12px;
    border-radius: 12px;
    background: var(--theme-surface-alt);
    color: var(--theme-text-secondary);
    font-style: italic;
    border-left: 4px dashed var(--theme-text-secondary);
}
.thought-bubble-player {
    border-left-color: var(--theme-accent, var(--theme-text-primary));
}
.thought-bubble-content {
    flex: 1;
}

/* Cascade Advance Links (S7) — visual cue distinct from choice exits */
.macro-linkreplace a {
    display: inline-block;
    margin-top: 1px;
    padding: 2px 8px;
    background: var(--theme-surface);
    border: 1px solid var(--theme-accent, var(--theme-text-primary));
    border-radius: 6px;
    color: var(--theme-accent, var(--theme-text-primary));
    text-decoration: none;
    font-size: 0.95em;
    line-height: 1.3;
}
.macro-linkreplace a:hover {
    background: var(--theme-accent, var(--theme-text-primary));
    color: var(--theme-bg, #fff);
}

/* Engine "no exits satisfied" dev diagnostic (2026-05-06) — fires when a
   canvas's all-conditional exit_block has zero satisfied choices. Visible
   only when $flags.debug_mode is true. The console.warn fires regardless. */
.engine-diag-no-exits {
    background: #2a0a0a;
    border: 2px solid #c0392b;
    padding: 12px 16px;
    margin: 16px 0;
    border-radius: 4px;
    color: #f5d8d6;
    font-family: var(--theme-font-mono, monospace);
    font-size: 12px;
}
.engine-diag-header {
    font-weight: bold;
    color: #ff6b6b;
    margin-bottom: 8px;
}
.engine-diag-hint {
    color: #f0c0bd;
    margin-bottom: 12px;
    font-style: italic;
}
.engine-diag-choice {
    background: #1a0505;
    padding: 8px 12px;
    margin: 8px 0;
    border-left: 3px solid #c0392b;
}
.engine-diag-choice-text { font-weight: bold; }
.engine-diag-choice-logic { font-size: 11px; color: #d4a8a4; margin-bottom: 4px; }
.engine-diag-items { margin: 4px 0 0 0; padding-left: 16px; list-style: none; }
.engine-diag-items li { margin: 2px 0; }
.engine-diag-pass { color: #6dcf6d; }
.engine-diag-fail { color: #ff8a85; }

/* Stats Card Portrait (larger) */
.stats-portrait {
    width: 80px;
    height: 100px;
    border-radius: 8px;
    overflow: hidden;
    background: var(--theme-surface-alt);
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
}

.stats-portrait img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.stats-portrait svg {
    width: 60%;
    height: 60%;
}

/* Stats Card with Portrait Layout */
.stats-card-with-portrait {
    display: flex;
    gap: 12px;
    align-items: flex-start;
}

.stats-info {
    flex: 1;
    min-width: 0;
}

/* Wardrobe Page */
.wardrobe-page {
    margin: 12px 0;
    background: var(--theme-surface);
    border: 1px solid var(--theme-border);
    border-radius: 10px;
    padding: 16px;
}

.wardrobe-table {
    width: 100%;
    border-collapse: collapse;
}

.wardrobe-row {
    border-bottom: 1px solid var(--theme-border);
}

.wardrobe-row:last-child {
    border-bottom: none;
}

.wardrobe-row-disabled {
    opacity: 0.45;
}

.wardrobe-slot-label {
    padding: 12px 8px;
    font-weight: 700;
    color: #333;
    width: 90px;
    vertical-align: middle;
    font-size: 0.85em;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.wardrobe-slot-items {
    padding: 10px 4px;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px;
}

.wardrobe-item {
    position: relative;
    width: 76px;
    height: 76px;
    border: 2px solid var(--theme-border);
    border-radius: 8px;
    cursor: pointer;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #fff;
    transition: border-color 0.15s, transform 0.15s, box-shadow 0.15s;
}

.wardrobe-item:hover {
    border-color: var(--theme-text-muted);
    transform: translateY(-1px);
    box-shadow: 0 2px 6px rgba(0,0,0,0.12);
}

.wardrobe-item-equipped {
    border-color: var(--theme-success);
    background: var(--theme-success-bg);
    box-shadow: 0 0 0 2px rgba(40, 167, 69, 0.25);
}

.wardrobe-item-equipped:hover {
    border-color: var(--theme-success);
}

.wardrobe-item-locked {
    opacity: 0.5;
    cursor: not-allowed;
    filter: grayscale(50%);
}

.wardrobe-item-locked:hover {
    transform: none;
    box-shadow: none;
    border-color: var(--theme-border);
}

.wardrobe-item-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.wardrobe-item-text {
    font-size: 0.8em;
    text-align: center;
    padding: 6px;
    word-break: break-word;
    color: #333;
    line-height: 1.2;
}

.wardrobe-badge-equipped {
    position: absolute;
    top: 2px;
    right: 2px;
    background: var(--theme-success);
    color: #fff;
    font-size: 11px;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.wardrobe-badge-locked {
    position: absolute;
    bottom: 2px;
    right: 2px;
    font-size: 13px;
}

.wardrobe-unequip-btn {
    background: none;
    border: 1px solid var(--theme-text-muted);
    color: var(--theme-text-muted);
    width: 28px;
    height: 28px;
    border-radius: 50%;
    cursor: pointer;
    font-size: 16px;
    line-height: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-left: auto;
    transition: background 0.15s, color 0.15s;
}

.wardrobe-unequip-btn:hover {
    background: var(--theme-danger);
    border-color: var(--theme-danger);
    color: #fff;
}

.wardrobe-disabled-hint,
.wardrobe-empty-hint {
    color: var(--theme-text-muted);
    font-style: italic;
    font-size: 0.85em;
}

.entry-blocked {
    color: var(--theme-danger);
    font-weight: 500;
}

.entry-requirements {
    color: var(--theme-warning-text);
    background: var(--theme-warning-bg);
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 0.9em;
}

.entry-blocked-narrative {
    font-style: italic;
    color: var(--theme-text-muted);
    line-height: 1.6;
    margin: 12px 0;
}

#wardrobe-btn-widget button {
    background: var(--theme-surface);
    border: 1px solid var(--theme-border);
    color: #333;
    padding: 6px 12px;
    border-radius: 6px;
    cursor: pointer;
    width: 100%;
    font-size: 0.95em;
    margin: 4px 0;
}

#wardrobe-btn-widget button:hover {
    background: var(--theme-surface-alt);
    border-color: var(--theme-border);
}

/* Shop page styles */
.shop-page {
    margin: 12px 0;
}

.shop-money {
    background: var(--theme-success-bg);
    border: 1px solid var(--theme-success);
    border-radius: 8px;
    padding: 10px 16px;
    font-size: 1.05em;
    font-weight: 600;
    color: var(--theme-success);
    margin-bottom: 16px;
    display: inline-block;
}

.shop-tier {
    margin-bottom: 20px;
    border: 1px solid var(--theme-border);
    border-radius: 10px;
    overflow: hidden;
    background: var(--theme-surface);
}

.shop-tier-locked {
    opacity: 0.55;
}

.shop-tier-header {
    background: var(--theme-text-strong);
    color: #fff;
    padding: 10px 16px;
    font-weight: 700;
    font-size: 0.95em;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.shop-tier-locked .shop-tier-header {
    background: var(--theme-text-muted);
}

.shop-tier-req {
    font-weight: 400;
    font-size: 0.85em;
    opacity: 0.8;
}

.shop-tier-locked-msg {
    padding: 12px 16px;
    color: var(--theme-warning-text);
    background: var(--theme-warning-bg);
    font-style: italic;
    font-size: 0.9em;
    text-align: center;
}

.shop-items {
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.shop-slot-group {
    margin-bottom: 4px;
}

.shop-slot-label {
    font-weight: 700;
    font-size: 0.8em;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--theme-text-secondary);
    padding: 4px 0;
    border-bottom: 1px solid var(--theme-surface-alt);
    margin-bottom: 6px;
}

.shop-slot-items {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.shop-item {
    display: flex;
    align-items: center;
    gap: 12px;
    background: #fff;
    border: 1px solid var(--theme-border);
    border-radius: 8px;
    padding: 10px 14px;
    transition: border-color 0.15s;
}

.shop-item-thumb {
    width: 56px;
    height: 56px;
    border: 2px solid var(--theme-border);
    border-radius: 8px;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--theme-surface);
    flex-shrink: 0;
}

.shop-item-thumb-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.shop-item-thumb-text {
    font-size: 0.7em;
    text-align: center;
    padding: 4px;
    word-break: break-word;
    color: var(--theme-text-muted);
    line-height: 1.2;
}

.shop-item:hover {
    border-color: var(--theme-border);
}

.shop-item-owned {
    border-color: var(--theme-success);
    background: var(--theme-success-bg);
}

.shop-item-unaffordable {
    opacity: 0.55;
}

.shop-item-info {
    display: flex;
    flex-direction: column;
    gap: 2px;
    flex: 1;
    min-width: 0;
}

.shop-item-name {
    font-weight: 600;
    color: var(--theme-text);
    font-size: 0.95em;
}


.shop-item-action {
    display: flex;
    align-items: center;
    gap: 10px;
}

.shop-item-price {
    font-weight: 600;
    color: var(--theme-text-secondary);
    font-size: 0.95em;
}

.shop-item-owned-badge {
    color: var(--theme-success);
    font-weight: 600;
    font-size: 0.9em;
}

.shop-item-cant-afford {
    color: var(--theme-danger);
    font-size: 0.85em;
    font-style: italic;
}

.shop-buy-btn {
    background: var(--theme-primary);
    color: #fff;
    border: none;
    padding: 6px 16px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.9em;
    font-weight: 600;
    transition: background 0.15s;
}

.shop-buy-btn:hover {
    background: var(--theme-primary);
}

/* Rent page styles */
.rent-title {
    color: var(--theme-bg);
    margin-bottom: 16px;
    font-size: 1.4em;
}

.rent-choices {
    margin: 16px 0;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.rent-choices a {
    display: block;
    padding: 10px 16px;
    background: var(--theme-surface);
    border: 1px solid var(--theme-border);
    border-radius: 6px;
    color: var(--theme-text);
    text-decoration: none;
    font-weight: 500;
    transition: background 0.15s, border-color 0.15s;
}

.rent-choices a:hover {
    background: var(--theme-surface-alt);
    border-color: var(--theme-border);
}

.rent-balance {
    margin-top: 12px;
    padding: 8px 12px;
    background: rgba(0,0,0,0.04);
    border-radius: 6px;
    font-size: 0.95em;
}

.game-over-text {
    text-align: center;
    font-size: 1.5em;
    font-weight: bold;
    color: var(--theme-danger);
    margin: 20px 0;
    letter-spacing: 2px;
}
</style>

""" + self._get_quests_block() + """

:: TipsPage
<<nobr>>
<<set _tp = setup.tips_page || {}>>
<h2><<print _tp.title || "Tips">></h2>
<div class="npc-section">
  <div class="tips-page-content">
    <<print _tp.content || "No tips available.">>
  </div>
</div>
<</nobr>>
<<link "← Back">><<run setup.smartBack()>><</link>>

:: StoryJournalStyles [stylesheet]
/* Story Journal Styles - Immersive narrative presentation */
.journal-container {
    background: linear-gradient(180deg, var(--journal-bg) 0%, var(--journal-bg-end) 100%);
    border: 1px solid var(--journal-border);
    border-radius: 12px;
    padding: 24px;
    margin: 16px 0;
    font-family: var(--theme-font-heading);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.journal-header {
    text-align: center;
    border-bottom: 2px solid var(--journal-border);
    padding-bottom: 16px;
    margin-bottom: 20px;
}

.journal-chapter-title {
    font-size: 1.5em;
    color: var(--journal-text);
    margin: 0 0 8px 0;
    font-weight: normal;
    font-style: italic;
}

.journal-chapter-mood {
    font-size: 0.95em;
    color: var(--journal-accent);
}

.journal-chapter-mood.hopeful { color: #6b8e23; }
.journal-chapter-mood.romantic { color: #c71585; }
.journal-chapter-mood.tense { color: #b22222; }
.journal-chapter-mood.passionate { color: #ff4500; }
.journal-chapter-mood.peaceful { color: #4682b4; }

.journal-progress {
    text-align: center;
    margin: 16px 0;
}

.journal-progress-bar {
    height: 8px;
    background: var(--journal-border);
    border-radius: 4px;
    overflow: hidden;
    margin: 8px 0;
}

.journal-progress-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--journal-accent), var(--journal-text-muted));
    border-radius: 4px;
    transition: width 0.5s ease;
}

.journal-section {
    margin: 20px 0;
}

.journal-section-title {
    font-size: 1.1em;
    color: var(--journal-text-muted);
    margin-bottom: 12px;
    padding-bottom: 4px;
    border-bottom: 1px dashed var(--journal-border);
}

.journal-memory {
    background: rgba(255,255,255,0.5);
    border-left: 3px solid var(--journal-accent);
    padding: 12px 16px;
    margin: 10px 0;
    font-style: italic;
    color: var(--journal-text);
}

.journal-memory.milestone {
    border-left-color: var(--theme-warning);
    background: rgba(201, 162, 39, 0.08);
}

.journal-memory-title {
    font-weight: bold;
    font-style: normal;
    color: var(--journal-text);
    margin-bottom: 4px;
}

.journal-npc {
    background: rgba(255,255,255,0.4);
    border-radius: 8px;
    padding: 16px;
    margin: 12px 0;
}

.journal-npc-name {
    font-size: 1.15em;
    color: var(--journal-text);
    margin-bottom: 8px;
}

.journal-npc-emotion {
    font-size: 1em;
    color: var(--journal-text-muted);
    line-height: 1.6;
}

.journal-npc-summary {
    font-style: italic;
    color: var(--journal-accent);
    margin-top: 8px;
}

.journal-group {
    background: rgba(255,255,255,0.3);
    border-radius: 6px;
    padding: 12px;
    margin: 8px 0;
}

.journal-group-name {
    font-weight: bold;
    color: var(--journal-text);
}

.journal-group-progress {
    font-size: 0.9em;
    color: var(--journal-accent);
    margin-top: 4px;
}

.journal-group-complete {
    color: #6b8e23;
}

.journal-hint {
    background: linear-gradient(135deg, rgba(139,115,85,0.1), rgba(109,90,64,0.15));
    border-radius: 8px;
    padding: 16px;
    margin-top: 20px;
    text-align: center;
    font-style: italic;
    color: var(--journal-text-muted);
}

.journal-hint.observation {
    border-left: 3px solid #4682b4;
}

.journal-hint.suggestion {
    border-left: 3px solid var(--journal-accent);
}

.journal-empty {
    text-align: center;
    padding: 40px 20px;
    color: var(--journal-accent);
    font-style: italic;
}

.journal-back-link {
    text-align: center;
    margin-top: 24px;
    padding-top: 16px;
    border-top: 1px solid var(--journal-border);
}

:: StoryJournal
<<set _position = setup.detectStoryPosition()>>
<<set _hint = setup.generateNarrativeHint()>>

<div class="journal-container">
  <div class="journal-header">
    <<if _position.current_chapter>>
      <h2 class="journal-chapter-title"><<print _position.current_chapter.name>></h2>
      <<if _position.current_chapter.mood>>
        <div class="journal-chapter-mood <<print _position.current_chapter.mood>>">
          <<print _position.current_chapter.description || "">>
        </div>
      <</if>>
    <<else>>
      <h2 class="journal-chapter-title">Your Story</h2>
    <</if>>

    <<if _position.progress_percent > 0>>
      <div class="journal-progress">
        <div class="journal-progress-bar">
          <div class="journal-progress-fill" style="width: <<print _position.progress_percent>>%;"></div>
        </div>
      </div>
    <</if>>
  </div>

  <!-- Memories (completed story moments) -->
  <<if _position.completed_nodes.length > 0>>
    <div class="journal-section">
      <div class="journal-section-title">Memories</div>
      <<for _i, _node range _position.completed_nodes>>
        <div class="journal-memory <<if _node.is_milestone>>milestone<</if>>">
          <div class="journal-memory-title"><<print _node.name>></div>
          <<if _node.journal_entry>>
            <<print _node.journal_entry>>
          <</if>>
        </div>
      <</for>>
    </div>
  <</if>>

  <!-- Active story threads (groups in progress) -->
  <<if _position.active_groups.length > 0>>
    <<set _incompleteGroups = _position.active_groups.filter(function(g) { return !g.isComplete && g.completed > 0; })>>
    <<if _incompleteGroups.length > 0>>
      <div class="journal-section">
        <div class="journal-section-title">Unfolding</div>
        <<for _i, _group range _incompleteGroups>>
          <div class="journal-group">
            <div class="journal-group-name"><<print _group.name>></div>
            <div class="journal-group-progress">
              <<print _group.description>>
            </div>
          </div>
        <</for>>
      </div>
    <</if>>
  <</if>>

  <!-- Relationship states (NPC emotions) -->
  <<if Object.keys($npcs).length > 0>>
    <div class="journal-section">
      <div class="journal-section-title">Connections</div>
      <<for _npcId range Object.keys($npcs)>>
        <<set _state = setup.interpretNpcState(_npcId)>>
        <<if _state.npc_name>>
          <div class="journal-npc">
            <div class="journal-npc-name"><<print _state.npc_name>></div>
            <div class="journal-npc-emotion"><<print _state.description>></div>
            <<if _state.relationship_summary && _state.relationship_summary !== _state.description>>
              <div class="journal-npc-summary"><<print _state.relationship_summary>></div>
            <</if>>
          </div>
        <</if>>
      <</for>>
    </div>
  <</if>>

  <!-- Subtle narrative hint (only when needed) -->
  <<if _hint.hint_type !== "none" && _hint.text>>
    <div class="journal-hint <<print _hint.hint_type>>">
      <<print _hint.text>>
    </div>
  <</if>>

  <!-- Empty state -->
  <<if _position.completed_nodes.length === 0 && Object.keys($npcs).length === 0>>
    <div class="journal-empty">
      Your story is just beginning...
    </div>
  <</if>>

  <div class="journal-back-link">
    [[Return to your story->Navigation]]
  </div>
</div>

""" + stats_page + wardrobe_page + clothing_block_page + travel_block_page + shop_page + rent_page + """

:: SchedulePage
<!-- LOCK-AWARENESS (2026-08-11). The Schedules page is a GUIDANCE surface: it is the only screen that
     publishes NPC hours, so the player uses it to decide where to walk. Schedule rows carry no conditions
     by design — the resolver reads exactly five keys and drops the rest — so a row keeps pointing at a
     location long after the story seals it, and getNpcLocation happily resolves "NOW" to a building the
     player can no longer enter. Measured on vesper: after the Act-1a close it advertised Mercer as NOW at
     his penthouse for 15 hours of every 24, and Calloway and Vane at Vance Securities, all three sealed by
     the same flag. That is worse than saying nothing, because the player walks there.
     The fix is on the PAGE, never on the rows: navDestUnlocked() is a pure entry_conditions check on the
     location (no current-location dependency, no side effects), so it answers "can she get in right now"
     for any slug. Locked rows are muted and show navDestBlockedReason() instead of the activity, and the
     NOW badge and its activity line are suppressed entirely rather than naming a door that will not open. -->
<<nobr>>
<<set _currentDay to $game_state.time_state.current_day>>
<<set _todayIndex to ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].indexOf(_currentDay)>>
<h2>📅 Weekly Schedule</h2>
<p class="current-time">Today is <<print _currentDay>> · <<print setup.formatTime($game_state.time_state.current_hour, $game_state.time_state.current_minute)>></p>
<<set _npcsWithSchedules to setup.getNpcsWithSchedules()>>
<<if _npcsWithSchedules.length === 0>>
<p><em>No NPCs have schedules defined.</em></p>
<<else>>
<<for _npcInfo range _npcsWithSchedules>>
<<set _npcId to _npcInfo.id>>
<<set _npcName to _npcInfo.name>>
<<set _currentLoc to setup.getNpcLocation(_npcId)>>
<<set _allSchedules to setup.getNpcAllSchedulesSorted(_npcId)>>
<div class="npc-section">
<h3 class="npc-name">
<<print _npcName>>
<<set _nowSlug to _currentLoc ? (setup._getLocUuidToSlug()[_currentLoc.location] || _currentLoc.location) : "">>
<<set _nowOpen to _currentLoc ? setup.navDestUnlocked(_nowSlug) : false>>
<<if _currentLoc and _nowOpen>>
<<set _locName to (setup.locations[_currentLoc.location] && setup.locations[_currentLoc.location].name) || setup._locNameFromUuid(_currentLoc.location) || _currentLoc.location>>
<span class="now-badge">NOW: <<print _locName>></span>
<</if>>
</h3>
<<if _currentLoc and _nowOpen and _currentLoc.activity>>
<div class="current-activity">"<<print _currentLoc.activity>>"</div>
<</if>>
<<if _allSchedules.length === 0>>
<p><em>No schedule entries.</em></p>
<<else>>
<table class="schedule-table">
<thead><tr><th>Time</th><th>Location</th><th>Activity</th><th>Days</th></tr></thead>
<tbody>
<<for _sch range _allSchedules>>
<<set _schSlug to _sch.location_slug || _sch.location>>
<<set _schOpen to setup.navDestUnlocked(_schSlug)>>
<<set _isCurrent to _schOpen && setup.isCurrentTimeSlot(_sch.start_time, _sch.end_time) && setup._weekdayMatches(_sch.weekdays, _todayIndex)>>
<<set _rowClass to _isCurrent ? "current-slot" : (_schOpen ? "" : "locked-slot")>>
<<set _schLocName to (setup.locations[_sch.location] && setup.locations[_sch.location].name) || _sch.location>>
<!-- @class, NOT class="<<print>>". SugarCube does not evaluate macros inside a raw HTML attribute — it
     emits them verbatim, so the row shipped with the literal string as its class and `.current-slot`
     never matched anything. Found 2026-08-11 while adding `.locked-slot`; the attribute directive is the
     same one the choice renderer already uses for `unlocked-choice`. -->
<tr @class="_rowClass">
<td><<if _isCurrent>>▶ <</if>><<print _sch.start_time>>-<<print _sch.end_time || "?">></td>
<td><<print _schLocName>></td>
<td><<if _schOpen>><<print _sch.activity>><<else>><span class="locked-slot-reason"><<print setup.navDestBlockedReason(_schSlug)>></span><</if>></td>
<td><<print setup.renderWeekdayBadges(_sch.weekdays, _todayIndex)>></td>
</tr>
<</for>>
</tbody>
</table>
<</if>>
</div>
<</for>>
<</if>>
<<set _soloActivities to setup.getSoloActivitiesAllSchedules()>>
<<if _soloActivities.length > 0>>
<div class="npc-section solo-activities-section">
<h3 class="npc-name">Your Activities</h3>
<table class="schedule-table">
<thead><tr><th>Time</th><th>Location</th><th>Activity</th><th>Days</th></tr></thead>
<tbody>
<<for _act range _soloActivities>>
<<set _rowClass to _act.isCurrent ? "current-slot" : "">>
<!-- @class for the same reason as the NPC table above — the literal-attribute bug applied here too. -->
<tr @class="_rowClass">
<td><<if _act.isCurrent>>▶ <</if>><<print _act.startTime>>-<<print _act.endTime || "?">></td>
<td><<print _act.locationName>></td>
<td><<print _act.name>></td>
<td><<print setup.renderWeekdayBadges(_act.weekdays, _todayIndex)>></td>
</tr>
<</for>>
</tbody>
</table>
</div>
<</if>>
<<link "← Back">><<run setup.smartBack()>><</link>>
<</nobr>>

<style>
.current-time {
    color: var(--theme-text-strong);
    font-size: 0.9em;
    margin: 0 0 10px 0;
}

.now-badge {
    background: var(--theme-success);
    color: white;
    padding: 3px 8px;
    border-radius: 10px;
    font-size: 0.75em;
    font-weight: bold;
    margin-left: 10px;
    vertical-align: middle;
}

.current-activity {
    color: var(--theme-text-muted);
    font-style: italic;
    margin-bottom: 8px;
    font-size: 0.85em;
}

.schedule-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85em;
    color: var(--theme-text);
}

.schedule-table th {
    text-align: left;
    padding: 4px 8px;
    background: var(--theme-surface);
    border-bottom: 2px solid var(--theme-border);
    color: var(--theme-text-strong);
    font-weight: 600;
}

.schedule-table td {
    padding: 4px 8px;
    border-bottom: 1px solid var(--theme-border);
    color: var(--theme-text-strong);
    vertical-align: middle;
}

.schedule-table tr.current-slot {
    background: var(--theme-warning-bg);
    font-weight: 500;
}

.schedule-table tr.current-slot td:first-child {
    color: var(--theme-warning-text);
}

/* A schedule row whose location the player cannot currently enter. Muted rather than hidden: a row that
   vanishes reads as "he has no schedule there", where a muted one reads as "that door is shut for now",
   which is the truth and is what a returning player needs. Never carries the ▶ current marker. */
.schedule-table tr.locked-slot {
    opacity: 0.55;
}

.schedule-table tr.locked-slot .locked-slot-reason {
    font-style: italic;
    opacity: 0.85;
}

.solo-activities-section {
    margin-top: 18px;
}

.weekday-badges {
    display: inline-flex;
    flex-wrap: wrap;
    gap: 3px;
}

.weekday-badge {
    display: inline-block;
    padding: 1px 6px;
    border-radius: 8px;
    font-size: 0.72em;
    font-weight: 600;
    background: var(--theme-surface);
    color: var(--theme-text-muted);
    border: 1px solid var(--theme-border);
}

.weekday-badge.weekday-today {
    background: var(--theme-primary);
    color: white;
    border-color: var(--theme-primary);
}

.weekday-badge.weekday-all {
    background: var(--theme-surface-alt);
    color: var(--theme-text);
    border-style: dashed;
}
</style>

:: FlagsPage
<<nobr>>
<h2>🚩 Game Flags</h2>

<div class="flags-container">
<<if $flags && Object.keys($flags).length > 0>>
  <div class="flags-section">
    <h3>Story Flags</h3>
    <<set _gkeys to Object.keys($flags).sort()>>
    <ul class="flags-list">
    <<for _i to 0; _i lt _gkeys.length; _i++>>
      <<set _gk to _gkeys[_i]>>
      <li class="flag-item">
        <span class="flag-name"><<print _gk>></span>
        <span class="flag-value <<print $flags[_gk] ? 'flag-true' : 'flag-false'>>"><<print $flags[_gk] ? '✔' : '✖'>></span>
      </li>
    <</for>>
    </ul>
  </div>
<<else>>
  <div class="no-flags">No story flags set.</div>
<</if>>
</div>

<<link "← Back">><<run setup.smartBack()>><</link>>
<</nobr>>

<style>
.flags-container {
    background: var(--theme-surface);
    border: 1px solid var(--theme-border);
    border-radius: 8px;
    padding: 16px;
    margin: 16px 0;
}

.flags-section {
    margin-bottom: 20px;
}

.flags-section:last-child {
    margin-bottom: 0;
}

.flags-section h3 {
    color: var(--theme-text-secondary);
    border-bottom: 2px solid var(--theme-border);
    padding-bottom: 8px;
    margin: 0 0 12px 0;
}

.flags-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.flag-item {
    display: flex;
    justify-content: space-between;
    padding: 6px 0;
    border-bottom: 1px solid var(--theme-surface-alt);
}

.flag-item:last-child {
    border-bottom: none;
}

.flag-name {
    font-weight: 500;
    color: var(--theme-text);
}

.flag-value {
    font-family: var(--theme-font-mono);
}

.flag-true {
    color: var(--theme-text-strong);
}

.flag-false {
    color: var(--theme-text-strong);
}

.no-flags {
    color: var(--theme-text-muted);
    font-style: italic;
    padding: 12px;
    background: #fff;
    border-radius: 4px;
}
</style>
"""

    def _generate_trait_system(self) -> str:
        """Generate trait helper functions for SugarCube runtime (widgets + JS)."""
        return """:: TraitFunctions [widget nobr]
<!-- Trait Helper Functions -->
<<widget "traitFunctions">>
<<script>>
window._traitClamp = function(v, min, max) {
  v = Number(v);
  if (isNaN(v)) { v = 0; }
  if (min !== undefined && v < min) v = min;
  if (max !== undefined && v > max) v = max;
  return v;
};

window.applyTraitEffect = function(targetType, npcId, trait, op, val, clampFlag, cap) {
  try {
    var sv = State.variables;
    if (!sv) return;

    // Resolve target object
    var traitsObj = null;
    if (targetType === 'player') {
      sv.player = sv.player || {};
      sv.player.core_traits = sv.player.core_traits || {};
      traitsObj = sv.player.core_traits;
    } else if (targetType === 'npc') {
      sv.npcs = sv.npcs || {};
      var npc = sv.npcs[String(npcId)] || null;
      if (!npc) return; // Unknown NPC
      npc.core_traits = npc.core_traits || {};
      traitsObj = npc.core_traits;
    } else {
      return; // Unknown target type
    }

    // Normalize inputs
    var key = String(trait);
    var current = Number(traitsObj[key]);
    if (isNaN(current)) current = 0;
    var value = Number(val);
    if (isNaN(value)) value = 0;

    // Apply operation
    var next = current;
    if (op === 'add') {
      next = current + value;
    } else if (op === 'set') {
      next = value;
    } else {
      // Unknown op; do nothing
      return;
    }

    // Clamp 0-100 if requested (default true)
    if (clampFlag === undefined || clampFlag === null) { clampFlag = true; }
    if (clampFlag) {
      next = window._traitClamp(next, 0, 100);
    }
    // Apply cap if provided
    if (cap !== undefined && cap !== null) {
      var capNum = Number(cap);
      if (!isNaN(capNum)) {
        if (next > capNum) next = Math.max(current, capNum);
      }
    }

    traitsObj[key] = next;
  } catch (e) {
    // Ignore to avoid breaking navigation
  }
};
<</script>>
<</widget>>
"""

    def _location_nav_slug(self, loc):
        """The runtime slug a location is keyed by in setup.locations (mirror of the
        locations_map build): properties['slug'] or a loc_<id> fallback."""
        return (getattr(loc, 'properties', None) or {}).get('slug') or f"loc_{loc.id}"

    def _render_location_nav_card(self, loc, video_path):
        """A single nav-grid card for a destination, lock-as-prose aware: a normal
        clickable card when the door is open, else a greyed non-clickable card showing
        the in-world reason. A travel-cost tag rides along when the location has costs."""
        loc_id = str(loc.id)
        slug = self._location_nav_slug(loc)
        passage_name = self._location_passage_name(loc)
        safe_name = html.escape(loc.name)
        image = self.location_images.get(loc_id, "")
        if image:
            img_html = f'<div class="location-card-image" style="background-image: url(\'{video_path}/{image}\')"></div>'
        else:
            img_html = f'<div class="location-card-image location-card-placeholder">{self._get_location_placeholder_svg()}</div>'
        indicators = (
            f'<div class="location-card-indicators">'
            f'<<if setup.locationHasNewCanvases("{loc_id}")>><span class="nav-new-badge">NEW</span><</if>>'
            f'<<for _npc range setup.getNpcsPresentAtLocation("{loc_id}")>><<if _npc.portrait>><img @src="\'{video_path}/\' + _npc.portrait" class="nav-npc-badge" @alt="_npc.name"><</if>><</for>>'
            f'</div>'
        )
        cost_tag = f'<<if setup.getLocationCostTag("{slug}")>><span class="nav-cost-tag"><<= setup.getLocationCostTag("{slug}")>></span><</if>>'
        open_card = (
            f'<a class="location-card link-internal" data-passage="{passage_name}">{img_html}'
            f'<div class="location-card-content"><span class="location-card-name">{safe_name}</span>{cost_tag}{indicators}</div></a>'
        )
        locked_card = (
            f'<div class="location-card location-card-locked">{img_html}'
            f'<div class="location-card-content"><span class="location-card-name">{safe_name}</span>'
            f'<span class="nav-locked-reason"><<= setup.navDestBlockedReason("{slug}")>></span></div></div>'
        )
        return f'<<if setup.navDestUnlocked("{slug}")>>{open_card}<<else>>{locked_card}<</if>>'

    def _render_location_nav_link(self, loc, video_path):
        """Text-mode sibling of _render_location_nav_card (lock-as-prose + cost tag)."""
        loc_id = str(loc.id)
        slug = self._location_nav_slug(loc)
        link_name = self._location_passage_name(loc)
        cost_tag = f'<<if setup.getLocationCostTag("{slug}")>> <span class="nav-cost-tag"><<= setup.getLocationCostTag("{slug}")>></span><</if>>'
        open_link = (
            f'[[{loc.name}->{link_name}]]'
            f'<<if setup.locationHasNewCanvases("{loc_id}")>> <span class="nav-new">!</span><</if>>'
            f'<<for _npc range setup.getNpcsPresentAtLocation("{loc_id}")>><<if _npc.portrait>> <img @src="\'{video_path}/\' + _npc.portrait" class="nav-npc-portrait" @alt="_npc.name"><</if>><</for>>'
            f'{cost_tag}'
        )
        locked_link = f'<span class="nav-link-locked">{html.escape(loc.name)} — <<= setup.navDestBlockedReason("{slug}")>></span>'
        return f'<<if setup.navDestUnlocked("{slug}")>>{open_link}<<else>>{locked_link}<</if>>'

    def _generate_hierarchical_navigation(self, location) -> str:
        """Generate hierarchical navigation using simplified entry_from system.

        Supports two modes:
        - Visual grid mode: When any destination has an image, displays clickable cards
        - Text-only mode: Falls back to text links when no images exist

        Args:
            location: Location object to generate navigation for

        Returns:
            HTML string with navigation options based on simplified navigation
        """
        navigation_html = ""

        # Get video path for media URLs
        video_path = getattr(self, 'video_path', '') or './media'

        # Get placeholder SVG for locations without images
        placeholder_svg = html.escape(self._get_location_placeholder_svg())

        # Get ordered navigation destinations using the navigation ordering system.
        # Offscreen locations are never navigable destinations (NPC "away" labels).
        def _loc_offscreen(_l):
            return bool((getattr(_l, 'properties', None) or {}).get('offscreen'))
        # A TRANSIT STOP (auto_exit=false) is arrived at and left by CANVAS — a car drop-off, a
        # lift. The engine's tree model doesn't describe it, so it takes no auto "Leave <name>"
        # link and its empty nav list is intentional, not a stranding to be rescued.
        auto_exit = (getattr(location, 'properties', None) or {}).get('auto_exit', True) is not False
        ordered_destinations = [d for d in self._ordered_navigation(location) if not _loc_offscreen(d)]

        if ordered_destinations:
            # Check if ANY destination has an image path defined (enables visual mode)
            has_any_images = any(
                str(dest.id) in self.location_image_defined
                for dest in ordered_destinations
            )

            if has_any_images:
                # VISUAL GRID MODE
                navigation_html += '<<nobr>><div class="location-nav-grid">'

                for dest in ordered_destinations:
                    navigation_html += self._render_location_nav_card(dest, video_path)

                navigation_html += '</div><</nobr>>\n'
            else:
                # TEXT-ONLY MODE (no images)
                navigation_html += "    <strong>Available destinations:</strong><br>\n"
                for dest in ordered_destinations:
                    navigation_html += "    " + self._render_location_nav_link(dest, video_path) + "<br>\n"

        # EXIT LINKS (always text-only, below the grid)
        exit_links = []

        # Generate automatic exit (go back to where we came from)
        if location.entry_from and auto_exit:
            exit_location = location.entry_from
            # Use smart exit destination that avoids infinite loops
            smart_destination = self._get_smart_exit_destination(exit_location)
            exit_links.append(f"    [[Leave {location.name}->{smart_destination}]]<br>\n")

        # Smart container exit logic: use direct exit with loop detection
        if location.parent_location and location.parent_location.is_container:
            container = location.parent_location
            show_exit = False

            # Check if container has a default entry location
            default_entry = getattr(container, 'default_entry_location', None)

            if default_entry:
                # Case 1: Container HAS default entry - only the default entry can exit
                show_exit = (location == default_entry)
            else:
                # Case 2: Container has NO default entry - any location with entry_from=container can exit
                show_exit = (location.entry_from == container)

            if show_exit:
                # Exit to container's entry_from location if it exists
                if container.entry_from:
                    exit_destination_name = container.entry_from.name.replace(' ', '_')
                    exit_destination = self._location_passage_for_name(exit_destination_name)
                    exit_links.append(f"    [[Exit {container.name}->{exit_destination}]]<br>\n")

        # Add exit links section if any exist
        if exit_links:
            navigation_html += '    <div class="location-nav-exits">\n'
            navigation_html += ''.join(exit_links)
            navigation_html += '    </div>\n'

        # Fallback: if no hierarchical connections, list all other locations
        # (excluding offscreen "away" labels — they're never navigable).
        # A transit stop is nav-less ON PURPOSE (its canvases carry the exits), so the rescue
        # would dump the whole map onto it — skip.
        if not navigation_html and auto_exit:
            other_locations = [loc for loc in self.locations if loc.id != location.id and not _loc_offscreen(loc)]
            if other_locations:
                # Check if any has image path defined for fallback visual mode
                has_any_images = any(
                    str(loc.id) in self.location_image_defined
                    for loc in other_locations
                )

                if has_any_images:
                    navigation_html += "    <p><strong>All locations:</strong></p>\n"
                    navigation_html += '<<nobr>><div class="location-nav-grid">'

                    for other_loc in other_locations:
                        navigation_html += self._render_location_nav_card(other_loc, video_path)

                    navigation_html += '</div><</nobr>>\n'
                else:
                    navigation_html += "    <p><strong>All locations:</strong></p>\n"
                    for other_loc in other_locations:
                        navigation_html += "    " + self._render_location_nav_link(other_loc, video_path) + "<br>\n"

        return navigation_html

    def _would_cause_infinite_loop(self, exit_location):
        """Check if direct exit to location would cause infinite loop.

        Args:
            exit_location: The location we want to exit to

        Returns:
            Boolean indicating if infinite loop would occur
        """
        # Loop occurs if exit destination is a container with default_entry
        # that would auto-redirect back, creating a cycle
        return (getattr(exit_location, 'is_container', False) and
                getattr(exit_location, 'default_entry_location', None))

    def _get_smart_exit_destination(self, exit_location):
        """Get the appropriate exit destination, avoiding infinite loops.

        Args:
            exit_location: The location we want to exit to

        Returns:
            String with the correct passage name to link to
        """
        if self._would_cause_infinite_loop(exit_location):
            # If exit location would auto-redirect, go to its default_entry directly
            default_entry = exit_location.default_entry_location
            default_entry_name = default_entry.name.replace(' ', '_')
            return self._location_passage_for_name(default_entry_name)
        else:
            # Normal direct exit
            exit_name = exit_location.name.replace(' ', '_')
            return self._location_passage_for_name(exit_name)

    def _generate_exit_navigation(self, container):
        """Generate exit navigation options with bidirectional connection discovery.

        Args:
            container: The container location being exited

        Returns:
            HTML string with navigation options
        """
        navigation_html = ""

        # Find outbound connections: locations that can be entered FROM this container
        outbound_connections = self._locations_entered_from(container)

        # Find inbound connection: where this container can be entered from
        inbound_connection = getattr(container, 'entry_from', None)

        # Add outbound destinations
        if outbound_connections:
            navigation_html += "<strong>Available destinations:</strong><br>\n"
            for dest in sorted(outbound_connections, key=lambda l: l.name):
                dest_name = dest.name.replace(' ', '_')
                # Handle destination containers with default_entry appropriately
                if getattr(dest, 'is_container', False) and getattr(dest, 'default_entry_location', None):
                    # If destination is container with default_entry, go to default_entry directly
                    default_entry_name = dest.default_entry_location.name.replace(' ', '_')
                    navigation_html += f"[[{dest.name}->{self._location_passage_for_name(default_entry_name)}]]<br>\n"
                else:
                    # Regular location or container without default_entry
                    navigation_html += f"[[{dest.name}->{self._location_passage_for_name(dest_name)}]]<br>\n"

        # Add inbound connection (where this container came from)
        if inbound_connection:
            navigation_html += "<strong>Go back to:</strong><br>\n"
            inbound_name = inbound_connection.name.replace(' ', '_')
            # Handle inbound containers with default_entry appropriately
            if getattr(inbound_connection, 'is_container', False) and getattr(inbound_connection, 'default_entry_location', None):
                # If inbound is container with default_entry, go to default_entry directly
                default_entry_name = inbound_connection.default_entry_location.name.replace(' ', '_')
                navigation_html += f"[[Back to {inbound_connection.name}->{self._location_passage_for_name(default_entry_name)}]]<br>\n"
            else:
                # Regular location or container without default_entry
                navigation_html += f"[[Back to {inbound_connection.name}->{self._location_passage_for_name(inbound_name)}]]<br>\n"

        # Add re-enter container option (to cancel exit and go back inside)
        navigation_html += "<p><strong>Or stay inside:</strong></p>\n"
        container_name = container.name.replace(' ', '_')

        if getattr(container, 'default_entry_location', None):
            # Container WITH default_entry: go to default_entry location
            default_entry = container.default_entry_location
            default_entry_name = default_entry.name.replace(' ', '_')
            navigation_html += f"[[Re-enter {container.name}->{self._location_passage_for_name(default_entry_name)}]]<br>\n"
        else:
            # Container WITHOUT default_entry: go to main container passage
            navigation_html += f"[[Re-enter {container.name}->{self._location_passage_for_name(container_name)}]]<br>\n"

        # Add fallback navigation if no connections found
        if not navigation_html:
            navigation_html += "<p><strong>No connections available.</strong></p>\n"

        return navigation_html

    def _get_canvases_for_location_with_inheritance(self, location):
        """Get story canvases with hierarchical inheritance through container hierarchy.

        Args:
            location: Location object to get canvases for

        Returns:
            List of canvas info dictionaries including inherited canvases
        """
        canvases_with_schedules = []
        visited_locations = set()

        # Start with current location and walk up hierarchy
        current_location = location
        while current_location and current_location.id not in visited_locations:
            visited_locations.add(current_location.id)

            # Get canvases directly triggered at this location
            for canvas in self.story_canvases:
                if hasattr(canvas, 'trigger') and canvas.trigger and str(canvas.trigger.location_id) == str(current_location.id):
                    # Get schedules for this trigger
                    schedules = self._trigger_schedules(canvas.trigger)
                    canvases_with_schedules.append({
                        'canvas': canvas,
                        'schedules': schedules,
                        'has_schedules': len(schedules) > 0,
                        'inherited_from': current_location.name if current_location.id != location.id else None
                    })

            # Move up to parent location in hierarchy
            current_location = getattr(current_location, 'parent_location', None)

        return canvases_with_schedules
