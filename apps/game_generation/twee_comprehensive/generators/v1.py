"""
Twee Comprehensive Generator v1.

Comprehensive game generator that creates sophisticated interactive experiences.
This is the isolated, self-contained comprehensive game generation system.
"""

import json
import html
import logging
import re
from typing import Any, Optional

from pathlib import Path

from apps.projects.models import Project

logger = logging.getLogger(__name__)

# Extension sets for media type detection
VIDEO_EXTENSIONS = {'.mp4', '.webm', '.mov', '.m4v', '.avi', '.mkv'}
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp'}


class TweeComprehensiveGeneratorV1:
    """
    Simplified Twee generator for canvas-based stories.

    Generates simple game flow:
    - Game Entry: Project info and start game
    - Starting Canvas: Display designated starting canvas
    - Navigation: Basic location-to-location movement
    - Locations: Simple location descriptions and navigation

    Completely isolated from other generation systems.
    """

    def __init__(self):
        self.project = None
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

    def generate(self, project: Project, options: Optional[dict] = None) -> str:
        """
        Generate comprehensive Twee content.

        Args:
            project: Django Project instance
            options: Optional generation options

        Returns:
            str: Complete Twee content with all features
        """
        self.project = project
        self.options = options or {}

        # Load video files if video_folder is provided
        self.video_folder = self.options.get("video_folder")
        self.video_path = self.options.get("video_path")  # Direct path mode
        self.debug = self.options.get("debug", False)
        self.dev_mode = self.options.get("dev_mode", False)
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

        # Add simple locations
        twee_sections.append(self._generate_simple_locations())

        # Add story canvases
        twee_sections.append(self._generate_story_canvases())

        # Add missing media page (always generated, but button only shows in debug mode)
        twee_sections.append(self._generate_missing_media_page())

        # Add canvas review pages (only in dev mode)
        if self.dev_mode:
            twee_sections.append(self._generate_canvas_review_pages())

        # Add theme CSS variables (always, provides defaults for all sections)
        twee_sections.append(self._generate_theme_stylesheet())

        # Add phone CSS (only when phone enabled)
        if self.phone_enabled:
            twee_sections.append(self._generate_phone_css())

        return "\n\n".join(twee_sections)

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

        # Recursive scan using rglob
        for file in media_path.rglob('*'):
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
            for node in canvas.nodes.all():
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
        from apps.stories.models import StoryCanvas, StoryNode

        included_ids = set()

        # Include starting canvas if present
        if self.project.starting_canvas:
            included_ids.add(str(self.project.starting_canvas.id))

        # Include canvases with triggers (initial set from _load_project_data)
        for c in self.story_canvases:
            included_ids.add(str(c.id))

        # Closure: pull in canvases referenced by any choice targetType 'node'
        changed = True
        while changed:
            changed = False
            # Iterate over currently included canvases and scan their nodes' exit blocks
            canvases = StoryCanvas.objects.filter(id__in=list(included_ids)).prefetch_related('nodes')
            for canvas in canvases:
                for node in canvas.nodes.all():
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

    def _build_passage_name_map(self):
        """Build mapping of node IDs to Twee passage names for cross-canvas references."""
        # Map starting canvas nodes (by creation order)
        if self.project.starting_canvas:
            nodes = self._get_canvas_nodes_ordered(self.project.starting_canvas)
            canvas_prefix = self._sanitize_canvas_name(self._get_canvas_slug(self.project.starting_canvas))
            for i, node in enumerate(nodes):
                passage_name = f"StartingCanvas_{canvas_prefix}_Node_{i+1}"
                self.passage_name_map[str(node.id)] = passage_name

        # Map included story canvas nodes (by creation order)
        for canvas in self.story_canvases:
            nodes = self._get_canvas_nodes_ordered(canvas)
            canvas_prefix = self._sanitize_canvas_name(self._get_canvas_slug(canvas))
            for i, node in enumerate(nodes):
                passage_name = f"Canvas_{canvas_prefix}_Node_{i+1}"
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

    def _generate_initialization(self) -> str:
        """Generate simple initialization with time system."""
        project_name = self.game_config.get('project_name', 'Interactive Game')
        project_description = getattr(self.project, 'description', '') or 'An interactive story experience'

        # Get time settings from project
        time_settings = self.project.get_time_settings()

        # Determine the start game target dynamically
        start_target = "StartingCanvas"  # Default fallback

        if self.project.starting_canvas:
            try:
                # Check if starting canvas has nodes
                nodes = self._get_canvas_nodes_ordered(self.project.starting_canvas)
                if nodes:
                    # Point directly to first node
                    canvas_name = self._sanitize_canvas_name(self._get_canvas_slug(self.project.starting_canvas))
                    start_target = f"StartingCanvas_{canvas_name}_Node_1"
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
        try:
            from apps.npcs.models import NPC

            for n in NPC.objects.filter(project=self.project, deleted_at__isnull=True):
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
        except (AttributeError, TypeError) as e:
            logger.warning("Error loading NPC map: %s", e)
            npc_map = {}
            npc_slug_map = {}
            hidden_npcs_map = {}
            npc_arc_stages_map = {}

        # Store as instance variables for use in _convert_blocks_to_game_html
        self.npc_map = npc_map
        self.npc_slug_map = npc_slug_map
        # E9/E10/E11 foundation: slug-keyed arc_stages registry. Empty when
        # no NPC has stage chains — runtime checks Object.keys(...).length > 0
        # before engaging stalled-detection / stage-gate / stage_label paths.
        self.npc_arc_stages_map = npc_arc_stages_map

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
            }

        # Build passage name → location slug reverse map (for clothing checks)
        passage_to_location = {}
        for loc in self.locations:
            loc_props = getattr(loc, 'properties', None) or {}
            loc_slug = loc_props.get("slug") or f"loc_{loc.id}"
            passage_name = f"Location_{loc.name.replace(' ', '_')}"
            passage_to_location[passage_name] = loc_slug
        passage_to_location_json = json.dumps(passage_to_location)

        # NPC schedules are derived at runtime from setup.help_data.locationCanvases
        # (see getNpcScheduleFromCanvases JS function) — no static schedule needed

        player_traits_json = json.dumps(player_traits)
        # Strip runtime-only fields from npc_map before serializing to game JSON
        # (relationship_options and customizable are used for passage generation, not runtime state)
        npc_map_for_json = {}
        npc_trait_decay_config = {}  # {npc_uuid: {trait: decay_per_day}}
        for uuid, data in npc_map.items():
            entry = dict(data)
            entry.pop("customizable", None)
            entry.pop("relationship_options", None)
            entry.pop("description", None)
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
        # Build player flags map from keys (default false)
        player_flags_map = {str(k): False for k in player_flag_keys}
        player_flags_json = json.dumps(player_flags_map)

        # Story arc data for narrative journal
        story_arc_json = self._build_story_arc_json()

        # Help data for Quest Page (per-NPC activities)
        help_data_json = self._build_help_data()

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
            wardrobe_json = json.dumps(initial_wardrobe)
            equipped_json = json.dumps(initial_equipped)
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

        # Passes (recurring time-limited purchases)
        self.passes = (self.project.metadata or {}).get("passes", [])
        # Items (consumable inventory)
        self.items = (self.project.metadata or {}).get("items", [])
        # Day-rollover hook ([engine.daily_tick]) — fires inside advanceDay().
        # Always present as a dict with a flagEffects list (possibly empty)
        # so the generated JS loop has a stable target.
        _daily_tick_meta = (self.project.metadata or {}).get("daily_tick") or {}
        self.daily_tick = {"flagEffects": _daily_tick_meta.get("flagEffects", []) or []}
        # E4: Stage helpers ([[engine.stage_helpers]]) — named composite gates.
        # Loaded as a list; runtime builds an O(1) name → helper lookup map.
        self.stage_helpers = (self.project.metadata or {}).get("stage_helpers", []) or []

        # Theme (visual customization)
        raw_theme = (self.project.metadata or {}).get("theme", {})
        self.theme = self._resolve_theme(raw_theme)

        # Sidebar items (custom display elements configurable via TOML)
        self.sidebar_items = (self.project.metadata or {}).get("sidebar_items", [])
        sidebar_items_json = json.dumps(self.sidebar_items)

        # Phone system data
        phone_settings = (self.project.metadata or {}).get("phone_settings", {})
        self.phone_enabled = phone_settings.get("enabled", False)
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
            phone_data_json = json.dumps({
                "apps": phone_apps,
                "conversations": phone_conversations,
                "posts": phone_posts,
                "profiles": phone_profiles,
                "daily_topics": phone_daily_topics,
            })

        # Dev mode JS helpers moved to [script] tagged passage in _generate_time_system()
        # This ensures they're available on page refresh/save load, not just when Start is visited

        # Escape player portrait for JSON
        player_portrait_escaped = json.dumps(player_portrait)

        # NPC portrait path prefix (resolved at generation time, embedded in JS)
        npc_portrait_prefix = (getattr(self, 'video_path', '') or './media').rstrip('/') + '/'

        # Build optional wardrobe lines for $player
        clothing_player_fields = ""
        if self.clothing_enabled:
            clothing_player_fields = f',\n    "wardrobe": {wardrobe_json},\n    "equipped": {equipped_json}'

        # Build optional player customization default fields for $player
        player_custom_fields = ""
        if self.player_customizable and self.player_customization_fields:
            for cf in self.player_customization_fields:
                if cf["id"] == "name":
                    continue  # name is already in $player.name
                player_custom_fields += f',\n    "{cf["id"]}": {json.dumps(cf.get("default", ""))}'

        # Build optional rent_state block for $game_state
        rent_state_block = ""
        if self.rent_enabled:
            starting_week = time_settings.get('starting_week', 1)
            rent_state_block = f""",
    "rent_state": {{
        "last_paid_week": {starting_week},
        "warnings": 0,
        "is_due": false
    }}"""

        # Build optional passes state block for $game_state
        passes_state_block = ""
        if self.passes:
            passes_state_block = ',\n    "passes": {}'

        # Build optional inventory state block for $game_state
        inventory_state_block = ""
        if self.items:
            inventory_state_block = ',\n    "inventory": {}'

        # Build optional phone state block for $game_state
        phone_state_block = ""
        if self.phone_enabled:
            phone_state_block = """,
    "phone": {
        "triggered_conversations": {},
        "read_conversations": {},
        "replies": {},
        "triggered_posts": {},
        "viewed_feed": false,
        "triggered_profiles": {},
        "liked_profiles": {},
        "passed_profiles": {},
        "matches": {}
    }"""

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
        if (!setup.triggerConditionsSatisfied(item.conditions)) return false;
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
setup.checkPhoneConversations = function() {{
    if (!setup.phone_enabled || !setup.phone_data) return;
    var sv = State.variables;
    if (!sv.game_state || !sv.game_state.phone) return;
    var ps = sv.game_state.phone;
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
    npcDc.last_day_key = setup.getCurrentDayKey();
    npcDc.count = (npcDc.count || 0) + 1;
    npcDc.used_topics = npcDc.used_topics || [];
    npcDc.used_topics.push(topicId);
    // Store chat message in history for display
    var chatHistory = ps.daily_chat_history = ps.daily_chat_history || {{}};
    var npcHistory = chatHistory[npcSlug] = chatHistory[npcSlug] || [];
    npcHistory.push({{
        topic_id: topicId,
        player_message: topic.player_message,
        npc_response: topic.npc_response,
        day_key: setup.getCurrentDayKey()
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
                if (blocks[b].type === "message" && !blocks[b].after_reply) {{ preview = blocks[b].content; break; }}
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
                html += '<div class="phone-bubble ' + cls + pending + '">' + block.content + '</div>';
            }} else if (block.type === "reply") {{
                var blockRound = block.round || 1;
                var thisRoundReply = _getRoundReply(convReplies, blockRound);
                if (thisRoundReply) {{
                    // Already replied — show locked-in choice
                    var choices = block.choices || [];
                    if (thisRoundReply.choice >= 0 && thisRoundReply.choice < choices.length) {{
                        html += '<div class="phone-bubble phone-bubble-player">' + choices[thisRoundReply.choice].text + '</div>';
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
                        html += '<button class="phone-reply-btn" data-conv-id="' + conv.id + '" data-choice="' + ri + '" data-round="' + blockRound + '">' + choices[ri].text + '</button>';
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
        html += '<div class="phone-bubble phone-bubble-player">' + dmsg.player_message + '</div>';
        html += '<div class="phone-bubble phone-bubble-npc">' + dmsg.npc_response + '</div>';
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
        var canChat = (npcDc.count || 0) < 1;
        if (canChat) {{
            var usedTopics = npcDc.used_topics || [];
            var available = [];
            for (var ati = 0; ati < npcTopics.length; ati++) {{
                var tp = npcTopics[ati];
                if (tp.conditions && tp.conditions.items && !setup.triggerConditionsSatisfied(tp.conditions)) continue;
                if (usedTopics.indexOf(tp.id) !== -1) continue;
                available.push(tp);
            }}
            if (available.length === 0 && npcTopics.length > 0) {{
                npcDc.used_topics = [];
                for (var ati2 = 0; ati2 < npcTopics.length; ati2++) {{
                    var tp2 = npcTopics[ati2];
                    if (tp2.conditions && tp2.conditions.items && !setup.triggerConditionsSatisfied(tp2.conditions)) continue;
                    available.push(tp2);
                }}
            }}
            if (available.length > 0) {{
                for (var si = available.length - 1; si > 0; si--) {{
                    var ri = Math.floor(Math.random() * (si + 1));
                    var tmp = available[si]; available[si] = available[ri]; available[ri] = tmp;
                }}
                var shown = available.slice(0, 3);
                html += '<div class="phone-daily-topics">';
                html += '<div class="phone-daily-label">Say something...</div>';
                for (var sti = 0; sti < shown.length; sti++) {{
                    html += '<button class="phone-daily-btn" data-npc="' + npcSlug + '" data-topic-id="' + shown[sti].id + '">' + shown[sti].player_message + '</button>';
                }}
                html += '</div>';
            }}
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
jQuery(document).on('click', '.phone-reply-btn', function(e) {
    e.preventDefault();
    setup.sendPhoneReply(jQuery(this).data('conv-id'), parseInt(jQuery(this).data('choice'), 10), parseInt(jQuery(this).data('round'), 10) || 1);
});
// Daily chat handlers
jQuery(document).on('click', '.phone-daily-btn', function(e) {
    e.preventDefault();
    setup.sendDailyChat(String(jQuery(this).data('npc')), String(jQuery(this).data('topic-id')));
});
// Dating app handlers
jQuery(document).on('click', '.phone-dating-like', function(e) {
    e.preventDefault();
    setup.likeProfile(jQuery(this).data('profile-id'));
});
jQuery(document).on('click', '.phone-dating-pass', function(e) {
    e.preventDefault();
    setup.passProfile(jQuery(this).data('profile-id'));
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

// Static lookup data — stored on setup (not State.variables) to avoid deep-clone on every passage transition
setup.help_data = {help_data_json};
setup.npc_slug_map = {npc_slug_map_json};
setup.hiddenNpcs = {hidden_npcs_json};
setup.locations = {locations_map_json};
setup.story_arc = {story_arc_json};
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
setup.sidebar_items = {sidebar_items_json};
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
setup.stage_helpers = {json.dumps(self.stage_helpers)};
setup.stage_helpers_map = {{}};
for (var _shi = 0; _shi < setup.stage_helpers.length; _shi++) {{
    setup.stage_helpers_map[setup.stage_helpers[_shi].name] = setup.stage_helpers[_shi];
}}
// E9/E10/E11 foundation: per-NPC stage display names, slug-keyed.
// Empty object = no NPC has a stage chain (existing TOMLs unaffected).
// Trait name convention: <slug>_stage in $player.core_traits (integer 0..N).
setup.npc_arc_stages = {json.dumps(self.npc_arc_stages_map)};
setup.phone_enabled = {"true" if self.phone_enabled else "false"};
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
        map[String(slugMap[slug])] = slug;
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
        var npcSlug = uuidToSlug[resolvedId];
        if (!npcSlug) return null;

        var entries = setup.getNpcScheduleFromCanvases(npcSlug);
        if (entries.length === 0) return null;

        // Find first entry whose time window is currently active
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

// Get schedule entries for a specific NPC on a specific day (dynamic)
setup.getNpcDaySchedule = function(npcId, dayIndex) {{
    try {{
        var resolvedId = setup.resolveNpcId(npcId);
        var uuidToSlug = setup._getNpcUuidToSlug();
        var npcSlug = uuidToSlug[resolvedId];
        if (!npcSlug) return [];

        var entries = setup.getNpcScheduleFromCanvases(npcSlug);
        var result = [];
        for (var i = 0; i < entries.length; i++) {{
            var sch = entries[i];
            // Empty weekdays = all days
            if (!sch.weekdays || sch.weekdays.length === 0 || sch.weekdays.includes(dayIndex)) {{
                result.push({{
                    location: sch.location,
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

// Check if a location has any unvisited AND available canvases (for navigation indicators)
// Uses selectCanvasByPriority to respect activity-level daily limits
setup.locationHasNewCanvases = function(locationId) {{
    try {{
        var sv = State.variables;
        var helpData = setup.help_data || {{}};
        var locationCanvases = helpData.locationCanvases || {{}};
        var canvasList = locationCanvases[String(locationId)] || [];

        // Use selectCanvasByPriority to get ACTUALLY available canvases
        // This respects activity-level daily limits (all tiers share same limit)
        var availableCanvases = setup.selectCanvasByPriority(canvasList);

        // Check if any available canvas is new (unvisited)
        // Skip random canvases — they appear probabilistically, not reliably
        for (var i = 0; i < availableCanvases.length; i++) {{
            if ((availableCanvases[i].triggerMode || "manual") === "random") continue;
            if (setup.isCanvasNew(availableCanvases[i].id)) {{
                return true;
            }}
        }}
        return false;
    }} catch (e) {{
        return false; // Fail closed - don't show indicator if error
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

// Check if a canvas has any unlocked + unvisited conditional choices
setup.canvasHasNewUnlockedChoices = function(canvasId) {{
    try {{
        var cc = (setup.help_data || {{}}).canvasConditionalChoices || {{}};
        var choices = cc[String(canvasId)];
        if (!choices || choices.length === 0) return false;
        for (var i = 0; i < choices.length; i++) {{
            if (setup.triggerConditionsSatisfied(choices[i].conditions)
                && !setup.isChoiceVisited(choices[i].key)) {{
                return true;
            }}
        }}
        return false;
    }} catch (e) {{
        return false;
    }}
}};

// Check if a location has any canvases with newly unlocked choices
setup.locationHasNewUnlockedChoices = function(locationId) {{
    try {{
        var lc = (setup.help_data || {{}}).locationCanvases || {{}};
        var canvasList = lc[String(locationId)] || [];
        var selected = setup.selectCanvasByPriority(canvasList);
        for (var i = 0; i < selected.length; i++) {{
            if (setup.canvasHasNewUnlockedChoices(selected[i].id)) {{
                return true;
            }}
        }}
        return false;
    }} catch (e) {{
        return false;
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

// Deduct costs for a canvas (called on canvas entry)
setup.deductCosts = function(canvasId) {{
    var costs = setup.getCanvasCosts(canvasId);
    if (!costs || costs.length === 0) return;
    setup.pendingEffects = [];
    for (var k = 0; k < costs.length; k++) {{
        setup.applyAndNotifyTrait('player', null, costs[k].trait, 'add', -Number(costs[k].value), true, null);
    }}
    setup.showEffectNotification();
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

// Get NPCs that have available canvases at a location
// Returns array of {{id, name, portrait}} for NPCs with valid activities
// Uses selectCanvasByPriority to respect activity-level daily limits
setup.getNpcsWithCanvasesAtLocation = function(locationId) {{
    var result = [];
    try {{
        var sv = State.variables;
        var helpData = setup.help_data || {{}};
        var locationCanvases = helpData.locationCanvases || {{}};
        var canvasList = locationCanvases[String(locationId)] || [];
        var npcs = sv.npcs || {{}};

        // Use selectCanvasByPriority to get ACTUALLY available canvases
        // This respects activity-level daily limits (all tiers share same limit)
        var availableCanvases = setup.selectCanvasByPriority(canvasList);

        var addedNpcs = {{}};

        for (var i = 0; i < availableCanvases.length; i++) {{
            var c = availableCanvases[i];
            if (!c.npcId) continue;
            if (addedNpcs[c.npcId]) continue;

            // Resolve NPC slug to UUID
            var npcUuid = setup.npc_slug_map ? setup.npc_slug_map[c.npcId] : null;
            if (!npcUuid) continue;

            var npc = npcs[npcUuid];
            if (!npc) continue;

            addedNpcs[c.npcId] = true;
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
        var helpData = setup.help_data || {{}};
        var locationCanvases = helpData.locationCanvases || {{}};
        var canvasList = locationCanvases[String(locationId)] || [];

        // Find highest-priority valid non-repeatable, non-random canvas
        var best = null;
        var bestPriority = -1;
        for (var i = 0; i < canvasList.length; i++) {{
            var c = canvasList[i];
            if (c.isRepeatable) continue;
            if ((c.triggerMode || "manual") === "random") continue;
            if (!setup.isCanvasValid(c)) continue;
            if ((c.priority || 0) > bestPriority) {{
                bestPriority = c.priority || 0;
                best = c;
            }}
        }}

        if (best) {{
            setup.markCanvasTriggered(best.id);
            return best.passageName;
        }}

        // Also check random encounters (auto-fire with probability)
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

        // Collect valid repeatable manual canvases, grouped by NPC
        // Split into affordable vs cost-blocked
        var npcActivities = {{}};   // NPC slug -> canvas (affordable)
        var npcBlocked = {{}};      // NPC slug -> canvas (valid but can't afford costs)
        for (var i = 0; i < canvasList.length; i++) {{
            var c = canvasList[i];
            if (!c.isRepeatable) continue;
            if ((c.triggerMode || "manual") === "random") continue;
            if (!c.npcId) continue;
            if (!setup.isCanvasValid(c)) continue;
            if (!setup.canTriggerActivity(c.name || c.id, c.maxPerDay)) continue;
            // One per NPC (uniqueness constraint enforced by validation)
            if (!npcActivities[c.npcId] && !npcBlocked[c.npcId]) {{
                if (c.costs && c.costs.length > 0 && !setup.checkCostsAffordable(c.costs)) {{
                    npcBlocked[c.npcId] = c;
                }} else {{
                    npcActivities[c.npcId] = c;
                }}
            }}
        }}

        var allSlugs = Object.keys(npcActivities).concat(
            Object.keys(npcBlocked).filter(function(s) {{ return !npcActivities[s]; }})
        );
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

            // Check for NEW or unlocked indicators (only for affordable)
            var indicatorClass = '';
            if (!isBlocked) {{
                var isNew = setup.isCanvasNew(activity.id);
                var hasUnlocked = !isNew && setup.canvasHasNewUnlockedChoices(activity.id);
                indicatorClass = isNew ? ' npc-portrait-new' : (hasUnlocked ? ' npc-portrait-unlocked' : '');
            }}
            var blockedClass = isBlocked ? ' npc-portrait-blocked' : '';

            html += '<div class="npc-portrait-card' + indicatorClass + blockedClass + '">';
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

            if (!isBlocked) {{
                if (isNew) html += '<span class="npc-badge npc-badge-new">NEW</span>';
                if (hasUnlocked) html += '<span class="npc-badge npc-badge-unlocked">!</span>';
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

        var soloActivities = [];
        var soloBlocked = [];
        for (var i = 0; i < canvasList.length; i++) {{
            var c = canvasList[i];
            if (!c.isRepeatable) continue;
            if ((c.triggerMode || "manual") === "random") continue;
            if (c.npcId) continue;  // Has NPC = shown as portrait, not here
            if (!setup.isCanvasValid(c)) continue;
            if (!setup.canTriggerActivity(c.name || c.id, c.maxPerDay)) continue;
            if (c.costs && c.costs.length > 0 && !setup.checkCostsAffordable(c.costs)) {{
                soloBlocked.push(c);
            }} else {{
                soloActivities.push(c);
            }}
        }}

        if (soloActivities.length === 0 && soloBlocked.length === 0) return '';

        var html = '<div class="location-solo-activities">';
        // Affordable activities
        for (var s = 0; s < soloActivities.length; s++) {{
            var solo = soloActivities[s];
            var displayName = solo.displayName || solo.name || 'Activity';
            var passageName = solo.passageName || '';
            if (!passageName) continue;

            var isNew = setup.isCanvasNew(solo.id);
            var cls = 'link-internal solo-activity-btn' + (isNew ? ' solo-activity-new' : '');
            html += '<a class="' + cls + '" data-passage="' + passageName + '">' + displayName + '</a><br>';
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

        // Shuffle for fairness (Fisher-Yates)
        var shuffled = afterLimit.slice();
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
    // Rent due on new week (only after start_after_flag is met, if configured)
    if (nextIndex === 0 && setup.rent_enabled) {{
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

// Show notification and clear
setup.showEffectNotification = function() {{
  var effects = setup.pendingEffects;
  if (!effects || effects.length === 0) return;

  var lines = [];
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
    }}
  }}

  if (lines.length === 0) {{ setup.pendingEffects = []; return; }}

  var html = '<div class="effect-toast">' + lines.join(' • ') + '</div>';
  jQuery('body').append(html);

  setTimeout(function() {{
    jQuery('.effect-toast').remove();
  }}, 2000);

  setup.pendingEffects = [];
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

// Get the next activity for an NPC or player (first incomplete in node order)
setup.getNextActivity = function(npcId) {{
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
                     item.operator === "eq" ? "=" : "≥";

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
<<set $player = {{
    "name": "{player_name}",
    "portrait": {player_portrait_escaped},
    "current_location": "",
    "core_traits": {player_traits_json},
    "flags": {player_flags_json}{clothing_player_fields}{player_custom_fields}
}}>>\
<<set $npcs = {npc_map_json}>>\
<<set $npc_interacted_today = {{}}>>\
<<set $flags = {{
    "game_started": true,
    "debug_mode": {"true" if self.debug else "false"}
}}>>\
<<set $flags_meta = {{}}>>\
<<set $game_state = {{
    "current_canvas": "",
    "visited_locations": [],
    "visited_nodes": [],
    "trigger_history": {{}},
    "activity_trigger_history": {{}},
    "visited_choices": {{}},
    "active_modifiers": {{}},
    "random_cooldowns": {{}},
    "time_state": {{
        "current_hour": {time_settings['starting_hour']},
        "current_minute": 0,
        "current_day": "{time_settings['starting_day']}",
        "current_week": {time_settings['starting_week']},
        "day": 1
    }}{rent_state_block}{passes_state_block}{inventory_state_block}{phone_state_block}
}}>>\
<<nobr>>
<div class="game-intro">
<h1>{project_name}</h1>
<p class="game-description">{project_description}</p>
<div class="developer-intro">
<p class="developer-about">We're a small indie studio crafting intimate, story-driven experiences. Every game is made with care, and your support helps us keep creating. If you enjoy our work, consider supporting us!</p>
<p class="support-link">👉 <a href="https://www.patreon.com/cw/nutgames844" target="_blank" rel="noopener">Support us on Patreon</a></p>
</div>
<div class="age-gate">
<p class="age-warning">⚠️ This game contains adult content intended for players 18 years of age or older.</p>
<div class="age-buttons">
[[✓ I am 18 or older - Enter Game->{start_target}]]
[[✗ I am NOT 18 or older->AgeBlocked]]
</div>
</div>
<div class="developer-footer">
<p class="developer-credit">Developed by <strong>NutGames</strong></p>
<p class="support-link">👉 <a href="https://www.patreon.com/cw/nutgames844" target="_blank" rel="noopener">Support us on Patreon</a></p>
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

    def _resolve_theme(self, raw: dict) -> dict:
        """Resolve theme config into a complete set of CSS token values.

        Fills in derived values from mode, user overrides take precedence.
        Returns a dict ready for CSS variable generation.
        """
        mode = raw.get("mode", "light")

        # Mode-derived base colors
        if mode == "dark":
            defaults = {
                "bg": "#0f0f1a",
                "surface": "#1a1a2e",
                "surface_alt": "#16213e",
                "border": "#333333",
                "text": "#e0e0e0",
                "text_muted": "#888888",
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

/* Sidebar phone button */
.phone-btn-item { position: relative; padding: 10px 8px; font-size: 16px; }
.phone-badge {
    background: var(--theme-danger); color: #fff;
    font-size: 10px; font-weight: bold;
    padding: 1px 5px; border-radius: 8px;
    margin-left: 4px;
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
                content += f"""    [[{location.name}->Location_{location_name}]]<br>\n"""
            content += """</div>"""
            return content

        # Connections exist: guide user back to current location
        lines = [
            ":: Navigation",
            "<h2>Navigation</h2>",
            "<p>Return to your current location to explore nearby places.</p>",
        ]
        for loc in self.locations:
            pass_name = f"Location_{loc.name.replace(' ', '_')}"
            lines.append(
                f'<<if $player.current_location == "{loc.id}">>[[Back to {loc.name}->{pass_name}]]<</if>>'
            )
        # If current location unknown, allow initial selection
        lines.append("<<if $player.current_location == \"\">>")
        lines.append("<div class=\"location-list\">")
        for location in self.locations:
            location_name = location.name.replace(' ', '_')
            lines.append(f"    [[{location.name}->Location_{location_name}]]<br>")
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
                    content += f""":: Location_{location_name}
<!-- Container with default entry: Auto-redirect -->
<<goto "Location_{default_name}">>

"""
                else:
                    # Container WITHOUT default entry: Show inner locations
                    content += f""":: Location_{location_name}
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
                    from apps.world.models import Location
                    connected_locations = Location.objects.filter(entry_from=location)
                    for connected_loc in connected_locations:
                        connected_name = connected_loc.name.replace(' ', '_')
                        # Handle destination containers with default_entry appropriately
                        if getattr(connected_loc, 'is_container', False) and getattr(connected_loc, 'default_entry_location', None):
                            # If destination is container with default_entry, go to default_entry directly
                            default_entry_name = connected_loc.default_entry_location.name.replace(' ', '_')
                            content += f"[[{connected_loc.name}->Location_{default_entry_name}]]<br>\n"
                        else:
                            # Regular location or container without default_entry
                            content += f"[[{connected_loc.name}->Location_{connected_name}]]<br>\n"

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

                    content += f""":: Location_{location_name}
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
<p>{self._resolve_at_references(location.description) if location.description else "A location in your story."}</p>
{wardrobe_link_ec}{shop_link_ec}<<= setup.renderNpcPortraits("{location_id}")>>
<<= setup.renderSoloActivities("{location_id}")>>
<div class="location-navigation">
"""
                    navigation_options = self._generate_hierarchical_navigation(location)
                    content += navigation_options
                    go_back_target = f"Location_{parent_name}" if parent_name else "Start"
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

                    content += f""":: Location_{location_name}
<<nobr>>
<<set $player.current_location = "{location_id}">>
<<if not $game_state.visited_locations.includes("{location_id}")>>
<<set $game_state.visited_locations.push("{location_id}")>>
<</if>>
<</nobr>>\
<<set _autoFire = setup.getStoryCanvasRedirect("{location_id}")>>\
<<if _autoFire>><<goto _autoFire>><<else>>\
<h2>{location.name}</h2>
<p>{self._resolve_at_references(location.description) if location.description else "A location in your story."}</p>
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

    def _generate_story_canvases(self) -> str:
        """Generate story canvas passages (per-node emission)."""
        if not self.story_canvases:
            return "<!-- No story canvases to generate -->"

        content = "<!-- STORY CANVAS PASSAGES -->\n\n"

        for canvas in self.story_canvases:
            try:
                # Get trigger location for validation
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

    def _generate_missing_media_page(self) -> str:
        """Generate the Missing Media Page passage for debug mode."""
        if not self.missing_media:
            # No missing media - return empty passage that just redirects back
            return """:: MissingMediaPage
<h2>Missing Media Files</h2>
<p>No missing media files found.</p>

<<link "← Back">><<run Engine.play(State.variables.last_game_passage || "Navigation")>><</link>>
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
<<link "← Back">><<run Engine.play(State.variables.last_game_passage || "Navigation")>><</link>>
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
                schedules = list(canvas.trigger.schedules.all())
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
            for npc in NPC.objects.filter(project=self.project, deleted_at__isnull=True):
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
        all_canvases = StoryCanvas.objects.filter(
            project=self.project, deleted_at__isnull=True
        ).select_related('trigger')
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
                    if hasattr(trigger, 'schedules') and trigger.schedules.exists():
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
                if hasattr(trigger, 'schedules') and trigger.schedules.exists():
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

                # Build passage name for dynamic rendering
                canvas_prefix = self._sanitize_canvas_name(self._get_canvas_slug(canvas))
                first_node_passage = f"Canvas_{canvas_prefix}_Node_1"

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

                location_canvas_list.append({
                    "id": str(canvas.id),
                    "name": canvas.name,  # For grouping tiers by activity name
                    "displayName": display_name,  # For link display
                    "passageName": first_node_passage,  # For link target
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
                    for node in canvas.nodes.all().order_by('created_at'):
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

        return json.dumps(help_data)

    def _format_schedule_human_readable(self, trigger) -> str:
        """Format trigger schedules as human-readable text like 'between 8 AM - 12 PM or 7 PM - 10 PM'."""
        if not hasattr(trigger, 'schedules') or not trigger.schedules.exists():
            return None

        schedules = list(trigger.schedules.all())
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
            for node in canvas.nodes.all():
                slug = (node.node_data or {}).get("slug", "")
                if slug:
                    node_uuid_by_slug[slug] = str(node.id)

            target_uuid = node_uuid_by_slug.get(target_node_slug)
            if not target_uuid:
                return None

            # Search all nodes for a choice that targets this node
            for node in canvas.nodes.all():
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
            for node in canvas.nodes.all():
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
            for node in canvas.nodes.all():
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
                if hasattr(trigger, 'schedules') and trigger.schedules.exists():
                    schedule_text = self._format_schedule_human_readable(trigger)
                cond = getattr(trigger, 'conditions', None)
                if cond and isinstance(cond, dict) and cond.get('items'):
                    canvas_conditions = cond

            # Extract flagEffects from all nodes
            try:
                for node in canvas.nodes.all():
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
        all_canvases = StoryCanvas.objects.filter(
            project=self.project, deleted_at__isnull=True
        ).select_related('trigger').prefetch_related('nodes')

        # Build canvas_npc_map for NPC association validation
        canvas_npc_map = {}
        npc_lookup = {}

        for npc in NPC.objects.filter(project=self.project, deleted_at__isnull=True):
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
            for node in canvas.nodes.all():
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
            for node in canvas.nodes.all():
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
        """Get canvas nodes ordered by creation time."""
        return canvas.nodes.all().order_by('created_at')

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
                    return f"Location_{location.name.replace(' ', '_')}"
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
        base_passage_name = f"{passage_prefix}_{canvas_prefix}_Node_1" if loop_config else None

        # Build node map for loop_terminal checks (keyed by UUID string)
        canvas_node_map = {str(n.id): n for n in nodes} if loop_config else {}

        # Map of node.id -> passage name is already built; use it for links
        for i, node in enumerate(nodes):
            node_passage_name = f"{passage_prefix}_{canvas_prefix}_Node_{i+1}"
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

                        # ── Loop: get role for this choice ──
                        choice_role = loop_choice_roles.get(choice_idx, {})
                        role = choice_role.get('role') if choice_role else None
                        choice_node_slug = choice_role.get('node_slug', '') if choice_role else ''

                        # ── Loop: open visited check for non-terminal choices on base node ──
                        if is_loop_base and role == 'non_terminal' and choice_node_slug:
                            passage_body += f'<<if not $game_state.loop_visited.includes("{choice_node_slug}")>>\n'

                        # Open conditional gate if conditions present
                        choice_key = None
                        if choice_conditions:
                            try:
                                conditions_js = json.dumps(choice_conditions)
                                passage_body += f"<<if setup.triggerConditionsSatisfied({conditions_js})>>\n"
                                conditional_expr_parts.append(f"setup.triggerConditionsSatisfied({conditions_js})")
                                # Generate choice key for unlock highlighting
                                choice_key = f"{canvas.id}:cc{cc_counter}"
                                cc_counter += 1
                                # Highlight wrapper for newly unlocked conditional choices
                                # Uses @class dynamic attribute to avoid SugarCube HTML parsing errors
                                # (conditional <span> open/close in separate <<if>> blocks causes "cannot find closing tag")
                                passage_body += f'<span @class="setup.isChoiceVisited(\'{choice_key}\') ? \'\' : \'unlocked-choice\'">\n'
                            except (TypeError, ValueError) as e:
                                logger.warning(
                                    "Error serializing choice conditions for '%s': %s. Treating as unconditional.",
                                    choice_text, e
                                )
                                has_unconditional_choice = True
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
                        has_effects = (trait_effects and isinstance(trait_effects, list)) or (flag_effects and isinstance(flag_effects, list)) or (self.clothing_enabled and wardrobe_effects and isinstance(wardrobe_effects, list))
                        if has_effects:
                            passage_body += "<<script>>setup.pendingEffects = [];<</script>>"
                        # Emit trait effects first (if any)
                        if trait_effects and isinstance(trait_effects, list):
                            for eff in trait_effects:
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
                                    op_js = op
                                    clamp_js = 'true' if clamp_flag else 'false'
                                    cap_js = 'null' if (cap is None) else str(int(cap) if isinstance(cap, (int, float)) else cap)

                                    passage_body += (
                                        f"<<script>>setup.applyAndNotifyTrait(\"{ttype}\", {npc_id_js}, \"{trait_js}\", \"{op_js}\", {float(val)}, {clamp_js}, {cap_js});<</script>>"
                                    )
                                except (KeyError, TypeError, ValueError) as e:
                                    logger.error(
                                        "Invalid trait effect in choice '%s': %s. Effect data: %s",
                                        choice_text, e, eff
                                    )
                                    raise ValueError(
                                        f"Invalid trait effect structure in choice '{choice_text}': {e}"
                                    ) from e
                        # Emit flag effects next (op = set | unset | toggle, defaults to set)
                        if flag_effects and isinstance(flag_effects, list):
                            for fe in flag_effects:
                                try:
                                    ftype = fe.get('targetType', 'player')
                                    fnpc = fe.get('npcId')
                                    flag = str(fe.get('flag', ''))
                                    fop = str(fe.get('op', 'set') or 'set')
                                    flag_js = flag.replace('"', '\\"')
                                    npc_js = f'"{fnpc}"' if fnpc else 'null'
                                    passage_body += f"<<script>>setup.applyAndNotifyFlag(\"{ftype}\", {npc_js}, \"{flag_js}\", \"{fop}\");<</script>>"
                                except (KeyError, TypeError, ValueError) as e:
                                    logger.error(
                                        "Invalid flag effect in choice '%s': %s. Effect data: %s",
                                        choice_text, e, fe
                                    )
                                    raise ValueError(
                                        f"Invalid flag effect structure in choice '{choice_text}': {e}"
                                    ) from e
                        # Emit wardrobe effects (add items to wardrobe)
                        if self.clothing_enabled and wardrobe_effects and isinstance(wardrobe_effects, list):
                            for we in wardrobe_effects:
                                try:
                                    w_action = we.get('action', 'add')
                                    w_item_id = str(we.get('item_id', '')).replace('"', '\\"')
                                    if w_action == 'add' and w_item_id:
                                        passage_body += f'<<script>>setup.addToWardrobe("{w_item_id}");<</script>>'
                                    elif w_action == 'equip' and w_item_id:
                                        passage_body += f'<<script>>setup.addToWardrobe("{w_item_id}"); setup.equipItem("{w_item_id}");<</script>>'
                                except (KeyError, TypeError, ValueError) as e:
                                    logger.warning("Invalid wardrobe effect in choice '%s': %s", choice_text, e)
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

                        # Close conditional gate if opened
                        if choice_conditions:
                            # Close highlight wrapper (always-present span with dynamic @class)
                            if choice_key:
                                passage_body += '</span>\n'
                            # ── Rejection / locked-visible system ──
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
                                                    f'<<script>>setup.applyAndNotifyTrait("{ttype}", {npc_id_js}, "{trait_js}", "{op}", {float(val)}, {clamp_js}, {cap_js});<</script>>'
                                                )
                                            except (KeyError, TypeError, ValueError) as e:
                                                logger.warning("Invalid rejection effect: %s", e)
                                        passage_body += "<<script>>setup.showEffectNotification();<</script>>"
                                    passage_body += f"<<script>>advanceTime({int(time_minutes)});<</script>><</link>>\n"
                                    passage_body += '</span><br>\n'
                                else:
                                    # Mode A: Greyed-out locked choice with tooltip
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
                            lb_time = first_exit[2] if len(first_exit) > 2 else 3
                            lb_has_effects = (lb_trait_effects and isinstance(lb_trait_effects, list)) or (lb_flag_effects and isinstance(lb_flag_effects, list)) or (self.clothing_enabled and lb_wardrobe_effects and isinstance(lb_wardrobe_effects, list))
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
                                    passage_body += f'<<script>>setup.applyAndNotifyTrait("{ttype}", {npc_id_js}, "{trait_js}", "{op}", {float(val)}, {clamp_js}, {cap_js});<</script>>'
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
                            if lb_has_effects:
                                passage_body += "<<script>>setup.showEffectNotification();<</script>>"
                        passage_body += '<<set $game_state.loop_count to $game_state.loop_count + 1>>'
                        lb_time_val = int(lb_time) if first_exit else 3
                        passage_body += f'<<script>>advanceTime({lb_time_val});<</script>><</link>><br>\n'
                        passage_body += '<</if>>\n'

                    # If all choices were conditional and none are currently satisfied, provide a fallback
                    if (not has_unconditional_choice) and conditional_expr_parts:
                        or_expr = ' or '.join(conditional_expr_parts)
                        passage_body += f"<<if not ({or_expr})>>\nNo available choices<br>\n[[Continue->{return_target}]]\n<</if>>\n"
                    passage_body += "<</nobr>>\n"
                else:
                    # Shouldn't happen for 'choices', but guard anyway
                    next_passage, continue_text = exit_result
                    time_progression = self._get_time_progression_for_node(node)
                    passage_body += f"{time_progression}\n[[{continue_text}->{next_passage}]]\n"
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
                passage = (
                    passage_header
                    + f"{time_progression}\n{trait_effects}\n{flag_effects}\n{wardrobe_effects_code}\n[[{continue_text}->{next_passage}]]\n\n"
                )

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
                    rejection_node_id = choice.get('rejection_node')
                    rejection_effects = choice.get('rejection_effects', []) or []
                    # Modifier effects
                    modifier_effects = choice.get('modifier_effects', []) or []
                    # Pass effects (recurring pass purchases)
                    pass_effects = choice.get('pass_effects', []) or []
                    # Item effects (inventory add/remove)
                    item_effects = choice.get('item_effects', []) or []

                    # Resolve target based on targetType
                    if target_type == 'trigger':
                        target_passage = return_target
                    elif target_type == 'location':
                        location_id = choice.get('locationId')
                        if location_id:
                            loc = self._get_location_by_id(location_id)
                            if loc:
                                target_passage = f"Location_{loc.name.replace(' ', '_')}"
                            else:
                                target_passage = return_target
                                logger.warning(f"Choice in node {node.id} references unknown locationId {location_id}")
                        else:
                            target_passage = return_target
                            logger.warning(f"Choice in node {node.id} has targetType 'location' but no locationId")
                    elif target_type == 'node':
                        node_id = choice.get('nodeId')
                        if node_id:
                            # Look up passage name in the map
                            target_passage = self.passage_name_map.get(str(node_id))
                            if not target_passage:
                                target_passage = return_target
                                logger.warning(f"Choice in node {node.id} references unknown nodeId {node_id}")
                        else:
                            target_passage = return_target
                            logger.warning(f"Choice in node {node.id} has targetType 'node' but no nodeId")
                    else:
                        # Unknown target type
                        target_passage = return_target
                        logger.warning(f"Unknown targetType '{target_type}' in choice for node {node.id}")

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
                    ))

                return processed_choices

            elif exit_type == 'location':
                # Process location type - return single tuple
                link_text = exit_block.get('text', default_text) or default_text
                destination_type = config.get('destinationType', 'trigger')

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
                            next_passage = f"Location_{loc.name.replace(' ', '_')}"
                        else:
                            next_passage = return_target
                            logger.warning(f"Exit block for node {node.id} references unknown locationId {location_id}")
                    else:
                        # Fallback to trigger location if no locationId
                        next_passage = return_target
                        logger.warning(f"Exit block for node {node.id} has specific destination but no locationId")
                elif destination_type == 'node':
                    node_id = config.get('destinationId')
                    if node_id:
                        target_passage = self.passage_name_map.get(str(node_id))
                        if target_passage:
                            next_passage = target_passage
                        else:
                            next_passage = return_target
                            logger.warning(f"Exit block for node {node.id} references unknown destinationId {node_id}")
                    else:
                        next_passage = return_target
                        logger.warning(f"Exit block for node {node.id} has destinationType 'node' but no destinationId")
                else:
                    # Unknown destination type, fallback to trigger
                    next_passage = return_target
                    logger.warning(f"Unknown destinationType '{destination_type}' in exit block for node {node.id}")

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
                    f'setup.applyAndNotifyTrait("{target_type}", {npc_js}, "{trait_js}", "{op}", {float(val)}, {clamp_js}, {cap_js});'
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

                i += 1
                props = block.get("props", {}) or {}

                # Media blocks: render even if text content is empty
                if block_type == "image":
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
                        # Player dialog with portrait support
                        player_portrait = getattr(self, 'player_portrait', '') or ''
                        portrait_html = self._render_portrait(player_portrait, "You") if player_portrait else ''
                        html_parts.append(
                            f'<div class="dialog-block dialog-player">'
                            f'{portrait_html}'
                            f'<div class="dialog-content">'
                            f'<strong>You:</strong> {content}'
                            f'</div></div>'
                        )
                    elif speaker == "unknown":
                        html_parts.append(
                            f'<div class="dialog-block dialog-npc">'
                            f'<div class="dialog-content">'
                            f'<strong>Stranger:</strong> {content}'
                            f'</div></div>'
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
                        portrait_html = self._render_portrait(npc_portrait, npc_name) if npc_portrait else ''
                        # For customizable NPCs, use runtime name from $npcs
                        if npc_data and npc_data.get("customizable") and npc_uuid:
                            speaker_html = f'<<print $npcs["{npc_uuid}"].name>>'
                        else:
                            speaker_html = html.escape(str(npc_name))
                        html_parts.append(
                            f'<div class="dialog-block dialog-npc">'
                            f'{portrait_html}'
                            f'<div class="dialog-content">'
                            f'<strong>{speaker_html}:</strong> {content}'
                            f'</div></div>'
                        )
                else:
                    # Fallback to paragraph for unknown types
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

    def _generate_time_system(self) -> str:
        """Generate time system with proper SugarCube widgets and display."""
        # Dev mode [script] passage - runs at story initialization, always available
        # This ensures dev functions work even after page refresh or save/load
        dev_script_passage = ""
        if self.dev_mode:
            dev_script_passage = """:: DevModeInit [script]
// ===== DEV MODE HELPER FUNCTIONS =====
// Dev trait modifications are stored in sessionStorage and reapplied on every
// passage start. This ensures changes persist across all navigation (back/forward).

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

window.devAdvanceHour = function() {
    window.advanceTime(60);
};

window.devNextDay = function() {
    window.advanceDay();
    State.variables.game_state.time_state.current_hour = 6;
    State.variables.game_state.time_state.current_minute = 0;
};

// Event delegation for dev mode trait adjustment buttons
document.addEventListener('click', function(e) {
    if (e.target.matches('.dev-player-trait-btn')) {
        var trait = e.target.dataset.trait;
        var delta = parseInt(e.target.dataset.delta, 10);
        window.devAdjustPlayerTrait(trait, delta);
    }
    if (e.target.matches('.dev-npc-trait-btn')) {
        var npcId = e.target.dataset.npc;
        var trait = e.target.dataset.trait;
        var delta = parseInt(e.target.dataset.delta, 10);
        window.devAdjustNpcTrait(npcId, trait, delta);
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

        info_pages_list = '["QuestsPage", "StatsPage", "SchedulePage", "MissingMediaPage", "StoryJournal", "WardrobePage", "ShopPage", "ClothingBlock"'
        if self.rent_enabled:
            info_pages_list += ', "RentDay", "RentDay_Paid", "RentDay_Short"'
        info_pages_list += ']'

        info_nav_script = """:: InfoPageNav [script]
// Track the last non-info-page passage so info page back buttons always work.
// Fixes softlock when history fills with info pages and Engine.backward() loops.
$(document).on(':passagestart', function(ev) {
    var psg = ev.passage.title;
    var infoPages = """ + info_pages_list + """;
""" + rent_redirect_block + clothing_redirect_block + """    if (infoPages.indexOf(psg) === -1) {
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
        if self.dev_mode:
            story_caption = f""":: StoryCaption
<<devIndicator>>
<<reviewButton>>
<<missingMediaButton>>
<<timeDisplay>>
<<sidebarItems>>{phone_btn_line}
<<activeModifiers>>
<<journalButton>>
<<statsButton>>
<<scheduleButton>>
<<flagsButton>>
<<playerTraits>>
<<npcTraits>>
<<patreonButton>>"""
        else:
            story_caption = f""":: StoryCaption
<<missingMediaButton>>
<<timeDisplay>>
<<sidebarItems>>{phone_btn_line}
<<activeModifiers>>
<<journalButton>>
<<statsButton>>
<<scheduleButton>>
<<playerTraits>>
<<patreonButton>>"""

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
<<link "← Back">><<run Engine.play(State.variables.last_game_passage || "Navigation")>><</link>>"""
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
<<link "← Back">><<run Engine.play(State.variables.last_game_passage || "Navigation")>><</link>>"""

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
    Engine.play(dest);
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

        # Shop page (only if clothing and shop enabled)
        shop_page = ""
        if self.clothing_enabled and self.shop_location_slug:
            shop_page = """
:: ShopPage
<<nobr>>
<h2>Clothing Store</h2>
<<= setup.renderShopPage()>>
<</nobr>>
<<link "\u2190 Back">><<run Engine.play(State.variables.last_game_passage || "Navigation")>><</link>>"""

        # Rent day page (only if rent enabled)
        rent_page = ""
        if self.rent_enabled:
            rent_page = """
:: RentDay
<<nobr>>
<<set _money to $player.core_traits.money || 0>>
<<set _rent to setup.rent_amount>>
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
    <strong><<print _collectorName>>:</strong> <<print _rt.greeting || "Rent. $" + _rent + ". You know how this works.">>
  </div>
</div>

<p>You have $<<print _money>>. Rent is $<<print _rent>>.</p>
<div class="rent-choices">
  <<if _money gte _rent>>
    <<set _payText to "Pay $" + _rent + " rent">>
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
    <strong><<print _collectorName>>:</strong> <<print _rt.paid_response || "Same time next week.">>
  </div>
</div>

<p><<print _rt.paid_closing || "Another week secured.">></p>

<p class="rent-balance">Remaining money: <strong>$<<print $player.core_traits.money>></strong></p>

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
      <strong><<print _collectorName>>:</strong> <<print _rt.warning_response || "Next Monday. Don't make me ask twice.">>
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
    <<set $player.flags[setup.rent_eviction_flag] to true>>
    <<set $game_state.rent_state.warnings to 0>>
    <<set $game_state.rent_state.is_due to false>>

    <p><<print _rt.eviction_scene_soft || _rt.eviction_scene || _collectorName + " stops waiting for the money. Something shifts in the way " + _collectorName + " looks at you now.">></p>

    <div class="dialog-block dialog-npc">
      <div class="dialog-content">
        <strong><<print _collectorName>>:</strong> <<print _rt.eviction_response_soft || _rt.eviction_response || "We'll be having a different conversation from here on out.">>
      </div>
    </div>

    <p><<print _rt.eviction_closing_soft || _rt.eviction_closing || "You're still here. But the terms have changed.">></p>

    <<set _returnTo to (State.variables.last_game_passage || "Navigation")>>
    <<link "Continue" _returnTo>><</link>>
  <<else>>
    <p><<print _rt.eviction_scene || _collectorName + " doesn't wait for excuses this time.">></p>

    <div class="dialog-block dialog-npc">
      <div class="dialog-content">
        <strong><<print _collectorName>>:</strong> <<print _rt.eviction_response || "Locks are getting changed today. Pack your things.">>
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

"""

        # Dev mode: show day count in time display
        if self.dev_mode:
            time_display_widget = """<<widget "timeDisplay">>
<div id="time-widget" class="time-display">
    <div class="time-line">
        <span id="time-display"><<timeFormatted>></span> | <span id="current-day"><<print $game_state.time_state.current_day>></span> | <span id="day-count" style="color:#dc3545;font-weight:bold;">Day <<print $game_state.time_state.day>></span>
    </div>
    <div class="control-line">
        <button class="time-btn" onclick="advanceTime(10)" title="Advance 10 minutes">></button> | <button class="time-btn" onclick="advanceTime(60)" title="Advance 1 hour">>></button> | <button class="time-btn" onclick="advanceTime(1440)" title="Advance 1 day">>>>>></button>
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
        <button class="time-btn" onclick="advanceTime(10)" title="Advance 10 minutes">></button> | <button class="time-btn" onclick="advanceTime(60)" title="Advance 1 hour">>></button> | <button class="time-btn" onclick="advanceTime(1440)" title="Advance 1 day">>>>>></button>
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
  <<elseif _item.type is "trait_bar">>
    <<set _traitKey to _item.trait>>
    <<set _traitVal to ($player && $player.core_traits) ? ($player.core_traits[_traitKey] || 0) : 0>>
    <<set _traitMax to _item.max || 100>>
    <<set _traitLabel to _item.label || _traitKey>>
    <<set _traitPct to Math.max(0, Math.min(100, (_traitVal / _traitMax) * 100))>>
    <div class="sidebar-item trait-bar-item" id="sidebar-trait-bar-<<print _si>>">
      <div class="trait-bar-label"><<print _traitLabel>>: <<print Math.floor(_traitVal)>> / <<print _traitMax>></div>
      <div class="trait-bar-bg">
        <div class="trait-bar-fill" style="width: <<print _traitPct>>%"></div>
      </div>
    </div>
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
        <<print _twMatched>>
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
<<if setup.phone_enabled>>
<<set _phoneUnread to setup.getPhoneUnreadCount()>>
<div id="phone-sidebar-btn" class="sidebar-item phone-btn-item">
  <<link "📱 Phone">><<script>>setup.openPhone();<</script>><</link>>
  <<if _phoneUnread gt 0>>
    <span class="phone-badge"><<print _phoneUnread>></span>
  <</if>>
</div>
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

        return info_nav_script + dev_script_passage + time_widgets_start + dev_indicator + review_button + time_display_widget + sidebar_items_widget + phone_widget + active_modifiers_widget + counter_widgets + player_traits_widget + npc_traits_widget + """

<<widget "playerFlags">>
<div id="flags-widget" class="traits-display">
  <div class="traits-header">Flags</div>
  <<if $player and $player.flags and Object.keys($player.flags).length > 0>>
    <<set _fkeys to Object.keys($player.flags).sort()>>
    <ul class="traits-list">
      <<for _j to 0; _j lt _fkeys.length; _j++>>
        <<set _fk to _fkeys[_j]>>
        <li class="trait-item">
          <span class="trait-name"><<print _fk>></span>
          <span class="trait-value"><<print $player.flags[_fk] ? '✔' : '✖'>></span>
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
  <<if passage() isnot "QuestsPage">><<link "📋 Quests" "QuestsPage">><</link>><<else>>📋 Quests<</if>>
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
<!-- Guide - simplified what's next help -->
<div id="journal-btn-widget">
  <<if passage() isnot "QuestsPage">><<link "📖 Guide" "QuestsPage">><</link>><<else>>📖 Guide<</if>>
</div>
<</widget>>

<<widget "statsButton">>
<div id="stats-btn-widget">
  <<if passage() isnot "StatsPage">><<link "📊 Stats" "StatsPage">><</link>><<else>>📊 Stats<</if>>
</div>
<</widget>>

<<widget "scheduleButton">>
<<set _npcsWithSchedules to setup.getNpcsWithSchedules()>>
<<set _soloActivities to setup.getSoloActivitiesForToday()>>
<<if _npcsWithSchedules.length > 0 || _soloActivities.length > 0>>
<div id="schedule-btn-widget">
  <<if passage() isnot "SchedulePage">><<link "📅 Schedules" "SchedulePage">><</link>><<else>>📅 Schedules<</if>>
</div>
<</if>>
<</widget>>

<<widget "patreonButton">>
<div id="patreon-btn-widget">
  <a href="https://www.patreon.com/cw/nutgames844" target="_blank" rel="noopener" class="patreon-link">
    <svg class="patreon-icon" viewBox="0 0 24 24" width="16" height="16">
      <path fill="currentColor" d="M15.386.524c-4.764 0-8.64 3.876-8.64 8.64 0 4.75 3.876 8.613 8.64 8.613 4.75 0 8.614-3.864 8.614-8.613C24 4.4 20.136.524 15.386.524M.003 23.537h4.22V.524H.003"/>
    </svg>
    Support Us
  </a>
</div>
<</widget>>

<<widget "flagsButton">>
<div id="flags-btn-widget">
  <<if passage() isnot "FlagsPage">><<link "🚩 Flags" "FlagsPage">><</link>><<else>>🚩 Flags<</if>>
</div>
<</widget>>

""" + story_caption + """

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
    text-align: center;
    padding: 6px 8px;
    font-size: 13px;
    font-family: var(--theme-font-mono);
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

#quests-btn-widget {
    background: var(--theme-primary-bg);
    border: 1px solid var(--theme-primary);
    border-radius: 4px;
    padding: 6px 8px;
    margin-bottom: 8px;
    text-align: center;
}

#quests-btn-widget a {
    color: var(--theme-primary);
    text-decoration: none;
    font-weight: bold;
}

#quests-btn-widget a:hover {
    color: var(--theme-primary);
    text-decoration: underline;
}

#journal-btn-widget {
    background: linear-gradient(180deg, var(--journal-bg) 0%, var(--journal-bg-end) 100%);
    border: 1px solid var(--journal-border);
    border-radius: 4px;
    padding: 6px 8px;
    margin-bottom: 8px;
    text-align: center;
}

#journal-btn-widget a {
    color: var(--journal-text-muted);
    text-decoration: none;
    font-weight: bold;
    font-family: var(--theme-font-heading);
}

#journal-btn-widget a:hover {
    color: var(--journal-text);
    text-decoration: underline;
}

#stats-btn-widget {
    background: var(--theme-success-bg);
    border: 1px solid var(--theme-success);
    border-radius: 4px;
    padding: 6px 8px;
    margin-bottom: 8px;
    text-align: center;
}

#stats-btn-widget a {
    color: var(--theme-success);
    text-decoration: none;
    font-weight: bold;
}

#stats-btn-widget a:hover {
    color: var(--theme-success);
    text-decoration: underline;
}

#schedule-btn-widget {
    background: var(--theme-primary-bg);
    border: 1px solid var(--theme-primary);
    border-radius: 4px;
    padding: 6px 8px;
    margin-bottom: 8px;
    text-align: center;
}

#schedule-btn-widget a {
    color: var(--theme-primary);
    text-decoration: none;
    font-weight: bold;
}

#schedule-btn-widget a:hover {
    color: var(--theme-primary);
    text-decoration: underline;
}

/* Flags Button in Sidebar */
#flags-btn-widget {
    background: var(--theme-warning-bg);
    border: 1px solid var(--theme-warning);
    border-radius: 4px;
    padding: 6px 8px;
    margin-bottom: 8px;
    text-align: center;
}

#flags-btn-widget a {
    color: var(--theme-warning-text);
    text-decoration: none;
    font-weight: bold;
}

#flags-btn-widget a:hover {
    color: var(--theme-warning-text);
    text-decoration: underline;
}

/* Patreon Button in Sidebar */
#patreon-btn-widget {
    margin: 15px 0 0 0;
    padding: 15px 0 0 0;
    border-top: 1px solid #444;
    text-align: center;
}

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

/* Navigation Unlocked Choice Indicators */
.nav-unlocked {
    color: var(--theme-warning);
    font-weight: bold;
    font-size: 1.0em;
}
.nav-unlocked-badge {
    font-size: 0.65em;
    padding: 2px 5px;
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

/* NEW / unlocked indicators on portraits */
.npc-portrait-new .npc-portrait-img,
.npc-portrait-new .npc-portrait-placeholder {
    border-color: var(--theme-warning);
}

.npc-portrait-unlocked .npc-portrait-img,
.npc-portrait-unlocked .npc-portrait-placeholder {
    border-color: var(--theme-success);
}

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

.npc-badge-new {
    background: var(--theme-warning);
    color: #000;
}

.npc-badge-unlocked {
    background: var(--theme-success);
    color: #fff;
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

.solo-activity-new {
    border-left: 3px solid var(--theme-warning);
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

/* ===== Sidebar trait bar ===== */
.trait-bar-item {
    margin-top: 0.5rem;
}
.trait-bar-label {
    font-size: 0.75rem;
    color: var(--theme-border);
    margin-bottom: 3px;
}
.trait-bar-bg {
    height: 8px;
    background: #1a1a2a;
    border-radius: 4px;
    overflow: hidden;
}
.trait-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--theme-warning), var(--theme-success));
    border-radius: 4px;
    transition: width 0.3s ease;
}

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

/* Dialog Block with Portrait */
.dialog-block {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 10px 0;
    padding: 10px;
    border-radius: 8px;
    color: var(--theme-text);
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

.dialog-content {
    flex: 1;
}

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

:: QuestsPage
<<nobr>>
<h2>What's Next</h2>
<<set _helpData = setup.help_data || {}>>
<<set _hasPlayer = _helpData.player && _helpData.player.activities && _helpData.player.activities.some(function(a) { return a.node_id; })>>
<<set _hasNpcs = _helpData.npcs && Object.keys(_helpData.npcs).length > 0>>
<<if _hasPlayer>>
  <div class="npc-section">
    <h3 class="npc-name"><<print _helpData.player.name>></h3>
    <<set _next = setup.getNextActivity("_player_")>>
    <<if _next === null>>
      <div class="quest-complete">✓ All activities completed!</div>
    <<elseif _next.isStartingCanvas>>
      <div class="quest-available">→ Start the game</div>
    <<elseif _next.isPhoneActivity>>
      <div class="quest-available">
        → 📱 Message <<print _next.activity.name || "someone">>
      </div>
    <<elseif _next.traitConditionsNotMet>>
      <div class="quest-conditions">
        🔒 <<print setup.formatCanvasConditions(_next.canvasConditions)>>
      </div>
    <<elseif _next.flagConditionsNotMet>>
      <div class="quest-conditions">
        🔒 <<print setup.formatFlagHint(_next.flagHint, _helpData.player.name)>>
      </div>
    <<elseif _next.daysConditionsNotMet>>
      <div class="quest-waiting">
        ⏳ <<if _next.daysRemaining === 1>>Come back tomorrow<<else>>Wait <<print _next.daysRemaining>> more days<</if>>
      </div>
    <<elseif _next.conditionsNotMet>>
      <div class="quest-conditions">
        🔒 <<print setup.formatCanvasConditions(_next.canvasConditions)>>
      </div>
    <<elseif _next.isLocked>>
      <div class="quest-locked">
        🔒 <<print setup.formatTraitRequirements(_next.missingTraits)>>
      </div>
    <<else>>
      <div class="quest-available">
        → <<print setup.formatActivityHint(_next.activity)>>
      </div>
    <</if>>
  </div>
<</if>>
<<if _hasNpcs>>
  <<for _npcId, _npcData range _helpData.npcs>>
    <div class="npc-section">
      <h3 class="npc-name"><<print ($npcs[_npcId] && $npcs[_npcId].name) || _npcData.name>></h3>
      <<set _next = setup.getNextActivity(_npcId)>>
      <<if _next === null>>
        <div class="quest-complete">✓ All activities completed!</div>
      <<elseif _next.isStartingCanvas>>
        <div class="quest-available">→ Start the game</div>
      <<elseif _next.isPhoneActivity>>
        <div class="quest-available">
          → 📱 Message <<print _next.activity.name || "someone">>
        </div>
      <<elseif _next.traitConditionsNotMet>>
        <div class="quest-conditions">
          🔒 <<print setup.formatCanvasConditions(_next.canvasConditions)>>
        </div>
      <<elseif _next.flagConditionsNotMet>>
        <div class="quest-conditions">
          🔒 <<print setup.formatFlagHint(_next.flagHint, _npcData.name)>>
        </div>
      <<elseif _next.daysConditionsNotMet>>
        <div class="quest-waiting">
          ⏳ <<if _next.daysRemaining === 1>>Come back tomorrow<<else>>Wait <<print _next.daysRemaining>> more days<</if>>
        </div>
      <<elseif _next.conditionsNotMet>>
        <div class="quest-conditions">
          🔒 <<print setup.formatCanvasConditions(_next.canvasConditions)>>
        </div>
      <<elseif _next.isLocked>>
        <div class="quest-locked">
          🔒 <<print setup.formatTraitRequirements(_next.missingTraits)>>
        </div>
      <<else>>
        <div class="quest-available">
          → <<print setup.formatActivityHint(_next.activity)>>
        </div>
      <</if>>
    </div>
  <</for>>
<</if>>
<<if !_hasPlayer && !_hasNpcs>>
  <div class="no-quests">No activities available.</div>
<</if>>
<</nobr>>
<<link "← Back">><<run Engine.play(State.variables.last_game_passage || "Navigation")>><</link>>

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

""" + stats_page + wardrobe_page + clothing_block_page + shop_page + rent_page + """

:: SchedulePage
<<nobr>>
<<set _currentDay to $game_state.time_state.current_day>>
<h2>📅 <<print _currentDay>>'s Schedules</h2>
<p class="current-time">Current Time: <<print setup.formatTime($game_state.time_state.current_hour, $game_state.time_state.current_minute)>></p>
<<set _npcsWithSchedules to setup.getNpcsWithSchedules()>>
<<if _npcsWithSchedules.length === 0>>
<p><em>No NPCs have schedules defined.</em></p>
<<else>>
<<for _npcInfo range _npcsWithSchedules>>
<<set _npcId to _npcInfo.id>>
<<set _npcName to _npcInfo.name>>
<<set _currentLoc to setup.getNpcLocation(_npcId)>>
<<set _todaySchedule to setup.getTodayScheduleSorted(_npcId)>>
<<set _dayIndex to ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].indexOf(_currentDay)>>
<div class="schedule-card">
<div class="schedule-header">
<span class="npc-name"><<print _npcName>></span>
<<if _currentLoc>>
<<set _locName to (setup.locations[_currentLoc.location] && setup.locations[_currentLoc.location].name) || _currentLoc.location>>
<span class="now-badge">NOW: <<print _locName>></span>
<</if>>
</div>
<<if _currentLoc && _currentLoc.activity>>
<div class="current-activity">"<<print _currentLoc.activity>>"</div>
<</if>>
<<if _todaySchedule.length === 0>>
<p><em>No schedule entries for <<print _currentDay>>.</em></p>
<<else>>
<p class="schedule-day-info"><<print _todaySchedule.length>> schedule entries for <<print _currentDay>></p>
<table class="schedule-table">
<thead><tr><th>Time</th><th>Location</th><th>Activity</th></tr></thead>
<tbody>
<<for _sch range _todaySchedule>>
<<set _isCurrent to setup.isCurrentTimeSlot(_sch.start_time, _sch.end_time)>>
<<set _rowClass to _isCurrent ? "current-slot" : "">>
<<set _schLocName to (setup.locations[_sch.location] && setup.locations[_sch.location].name) || _sch.location>>
<tr class="<<print _rowClass>>">
<td><<if _isCurrent>>▶ <</if>><<print _sch.start_time>>-<<print _sch.end_time || "?">></td>
<td><<print _schLocName>></td>
<td><<print _sch.activity>></td>
</tr>
<</for>>
</tbody>
</table>
<</if>>
</div>
<</for>>
<</if>>
<<set _soloActivities to setup.getSoloActivitiesForToday()>>
<<if _soloActivities.length > 0>>
<div class="solo-activities-section schedule-card">
<h3>Your Activities</h3>
<table class="schedule-table">
<thead><tr><th>Time</th><th>Location</th><th>Activity</th></tr></thead>
<tbody>
<<for _act range _soloActivities>>
<<set _rowClass to _act.isCurrent ? "current-slot" : "">>
<tr class="<<print _rowClass>>">
<td><<if _act.isCurrent>>▶ <</if>><<print _act.startTime>>-<<print _act.endTime || "?">></td>
<td><<print _act.locationName>></td>
<td><<print _act.name>></td>
</tr>
<</for>>
</tbody>
</table>
</div>
<</if>>
<<link "← Back">><<run Engine.play(State.variables.last_game_passage || "Navigation")>><</link>>
<</nobr>>

<style>
.current-time {
    color: var(--theme-text-strong);
    font-size: 0.9em;
    margin: 0 0 10px 0;
}

.schedule-card {
    background: var(--theme-bg);
    border: 1px solid var(--theme-border);
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 12px;
}

.schedule-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 4px;
}

.npc-name {
    font-size: 1.1em;
    font-weight: bold;
    color: var(--theme-text);
}

.now-badge {
    background: var(--theme-success);
    color: white;
    padding: 3px 8px;
    border-radius: 10px;
    font-size: 0.8em;
    font-weight: bold;
}

.current-activity {
    color: var(--theme-text-muted);
    font-style: italic;
    margin-bottom: 6px;
    font-size: 0.85em;
}

.schedule-day-info {
    color: var(--theme-text-muted);
    font-size: 0.8em;
    margin: 0 0 6px 0;
    padding: 2px 6px;
    background: var(--theme-surface);
    border-radius: 3px;
    display: inline-block;
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
}

.schedule-table tr.current-slot {
    background: var(--theme-warning-bg);
    font-weight: 500;
}

.schedule-table tr.current-slot td:first-child {
    color: var(--theme-warning-text);
}

.solo-activities-section {
    margin-top: 18px;
}

.solo-activities-section h3 {
    color: var(--theme-text);
    margin: 0 0 8px 0;
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

<<if $player && $player.flags && Object.keys($player.flags).length > 0>>
  <div class="flags-section">
    <h3>Player Flags</h3>
    <<set _pkeys to Object.keys($player.flags).sort()>>
    <ul class="flags-list">
    <<for _j to 0; _j lt _pkeys.length; _j++>>
      <<set _pk to _pkeys[_j]>>
      <li class="flag-item">
        <span class="flag-name"><<print _pk>></span>
        <span class="flag-value <<print $player.flags[_pk] ? 'flag-true' : 'flag-false'>>"><<print $player.flags[_pk] ? '✔' : '✖'>></span>
      </li>
    <</for>>
    </ul>
  </div>
<</if>>
</div>

<<link "← Back">><<run Engine.play(State.variables.last_game_passage || "Navigation")>><</link>>
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

        # Get ordered navigation destinations using the navigation ordering system
        ordered_destinations = location.get_ordered_navigation()

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
                    dest_id = str(dest.id)
                    dest_name = dest.name.replace(' ', '_')
                    dest_image = self.location_images.get(dest_id, "")
                    passage_name = f"Location_{dest_name}"
                    safe_name = html.escape(dest.name)

                    # Build card HTML (no newlines to avoid whitespace)
                    navigation_html += f'<a class="location-card link-internal" data-passage="{passage_name}">'

                    if dest_image:
                        # Card with image
                        image_src = f"{video_path}/{dest_image}"
                        navigation_html += f'<div class="location-card-image" style="background-image: url(\'{image_src}\')"></div>'
                    else:
                        # Card with placeholder silhouette
                        navigation_html += f'<div class="location-card-image location-card-placeholder">{self._get_location_placeholder_svg()}</div>'

                    navigation_html += f'<div class="location-card-content">'
                    navigation_html += f'<span class="location-card-name">{safe_name}</span>'

                    # Indicators container (NPC portraits + new canvas badge)
                    navigation_html += f'<div class="location-card-indicators">'
                    navigation_html += f'<<if setup.locationHasNewCanvases("{dest_id}")>><span class="nav-new-badge">NEW</span><</if>>'
                    navigation_html += f'<<if setup.locationHasNewUnlockedChoices("{dest_id}")>><span class="nav-unlocked-badge">\U0001f513</span><</if>>'
                    navigation_html += f'<<for _npc range setup.getNpcsWithCanvasesAtLocation("{dest_id}")>><<if _npc.portrait>><img @src="\'{video_path}/\' + _npc.portrait" class="nav-npc-badge" @alt="_npc.name"><</if>><</for>>'
                    navigation_html += f'</div>'
                    navigation_html += f'</div>'
                    navigation_html += f'</a>'

                navigation_html += '</div><</nobr>>\n'
            else:
                # TEXT-ONLY MODE (no images)
                navigation_html += "    <strong>Available destinations:</strong><br>\n"
                for dest in ordered_destinations:
                    dest_name = dest.name.replace(' ', '_')
                    navigation_html += f"""    [[{dest.name}->Location_{dest_name}]]<<if setup.locationHasNewCanvases("{dest.id}")>> <span class="nav-new">!</span><</if>><<if setup.locationHasNewUnlockedChoices("{dest.id}")>> <span class="nav-unlocked">\U0001f513</span><</if>><<for _npc range setup.getNpcsWithCanvasesAtLocation("{dest.id}")>><<if _npc.portrait>> <img @src="'{video_path}/' + _npc.portrait" class="nav-npc-portrait" @alt="_npc.name"><</if>><</for>><br>\n"""

        # EXIT LINKS (always text-only, below the grid)
        exit_links = []

        # Generate automatic exit (go back to where we came from)
        if location.entry_from:
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
                    exit_destination = f"Location_{exit_destination_name}"
                    exit_links.append(f"    [[Exit {container.name}->{exit_destination}]]<br>\n")

        # Add exit links section if any exist
        if exit_links:
            navigation_html += '    <div class="location-nav-exits">\n'
            navigation_html += ''.join(exit_links)
            navigation_html += '    </div>\n'

        # Fallback: if no hierarchical connections, list all other locations
        if not navigation_html:
            other_locations = [loc for loc in self.locations if loc.id != location.id]
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
                        loc_id = str(other_loc.id)
                        other_name = other_loc.name.replace(' ', '_')
                        loc_image = self.location_images.get(loc_id, "")
                        passage_name = f"Location_{other_name}"
                        safe_name = html.escape(other_loc.name)

                        navigation_html += f'<a class="location-card link-internal" data-passage="{passage_name}">'

                        if loc_image:
                            image_src = f"{video_path}/{loc_image}"
                            navigation_html += f'<div class="location-card-image" style="background-image: url(\'{image_src}\')"></div>'
                        else:
                            navigation_html += f'<div class="location-card-image location-card-placeholder">{self._get_location_placeholder_svg()}</div>'

                        navigation_html += f'<div class="location-card-content">'
                        navigation_html += f'<span class="location-card-name">{safe_name}</span>'
                        navigation_html += f'<div class="location-card-indicators">'
                        navigation_html += f'<<if setup.locationHasNewCanvases("{loc_id}")>><span class="nav-new-badge">NEW</span><</if>>'
                        navigation_html += f'<<if setup.locationHasNewUnlockedChoices("{loc_id}")>><span class="nav-unlocked-badge">\U0001f513</span><</if>>'
                        navigation_html += f'<<for _npc range setup.getNpcsWithCanvasesAtLocation("{loc_id}")>><<if _npc.portrait>><img @src="\'{video_path}/\' + _npc.portrait" class="nav-npc-badge" @alt="_npc.name"><</if>><</for>>'
                        navigation_html += f'</div>'
                        navigation_html += f'</div>'
                        navigation_html += f'</a>'

                    navigation_html += '</div><</nobr>>\n'
                else:
                    navigation_html += "    <p><strong>All locations:</strong></p>\n"
                    for other_loc in other_locations:
                        other_name = other_loc.name.replace(' ', '_')
                        navigation_html += f"""    [[{other_loc.name}->Location_{other_name}]]<<if setup.locationHasNewCanvases("{other_loc.id}")>> <span class="nav-new">!</span><</if>><<if setup.locationHasNewUnlockedChoices("{other_loc.id}")>> <span class="nav-unlocked">\U0001f513</span><</if>><<for _npc range setup.getNpcsWithCanvasesAtLocation("{other_loc.id}")>><<if _npc.portrait>> <img @src="'{video_path}/' + _npc.portrait" class="nav-npc-portrait" @alt="_npc.name"><</if>><</for>><br>\n"""

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
            return f"Location_{default_entry_name}"
        else:
            # Normal direct exit
            exit_name = exit_location.name.replace(' ', '_')
            return f"Location_{exit_name}"

    def _generate_exit_navigation(self, container):
        """Generate exit navigation options with bidirectional connection discovery.

        Args:
            container: The container location being exited

        Returns:
            HTML string with navigation options
        """
        from apps.world.models import Location
        navigation_html = ""

        # Find outbound connections: locations that can be entered FROM this container
        outbound_connections = Location.objects.filter(entry_from=container)

        # Find inbound connection: where this container can be entered from
        inbound_connection = getattr(container, 'entry_from', None)

        # Add outbound destinations
        if outbound_connections.exists():
            navigation_html += "<strong>Available destinations:</strong><br>\n"
            for dest in outbound_connections.order_by('name'):
                dest_name = dest.name.replace(' ', '_')
                # Handle destination containers with default_entry appropriately
                if getattr(dest, 'is_container', False) and getattr(dest, 'default_entry_location', None):
                    # If destination is container with default_entry, go to default_entry directly
                    default_entry_name = dest.default_entry_location.name.replace(' ', '_')
                    navigation_html += f"[[{dest.name}->Location_{default_entry_name}]]<br>\n"
                else:
                    # Regular location or container without default_entry
                    navigation_html += f"[[{dest.name}->Location_{dest_name}]]<br>\n"

        # Add inbound connection (where this container came from)
        if inbound_connection:
            navigation_html += "<strong>Go back to:</strong><br>\n"
            inbound_name = inbound_connection.name.replace(' ', '_')
            # Handle inbound containers with default_entry appropriately
            if getattr(inbound_connection, 'is_container', False) and getattr(inbound_connection, 'default_entry_location', None):
                # If inbound is container with default_entry, go to default_entry directly
                default_entry_name = inbound_connection.default_entry_location.name.replace(' ', '_')
                navigation_html += f"[[Back to {inbound_connection.name}->Location_{default_entry_name}]]<br>\n"
            else:
                # Regular location or container without default_entry
                navigation_html += f"[[Back to {inbound_connection.name}->Location_{inbound_name}]]<br>\n"

        # Add re-enter container option (to cancel exit and go back inside)
        navigation_html += "<p><strong>Or stay inside:</strong></p>\n"
        container_name = container.name.replace(' ', '_')

        if getattr(container, 'default_entry_location', None):
            # Container WITH default_entry: go to default_entry location
            default_entry = container.default_entry_location
            default_entry_name = default_entry.name.replace(' ', '_')
            navigation_html += f"[[Re-enter {container.name}->Location_{default_entry_name}]]<br>\n"
        else:
            # Container WITHOUT default_entry: go to main container passage
            navigation_html += f"[[Re-enter {container.name}->Location_{container_name}]]<br>\n"

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
                    schedules = list(canvas.trigger.schedules.all())
                    canvases_with_schedules.append({
                        'canvas': canvas,
                        'schedules': schedules,
                        'has_schedules': len(schedules) > 0,
                        'inherited_from': current_location.name if current_location.id != location.id else None
                    })

            # Move up to parent location in hierarchy
            current_location = getattr(current_location, 'parent_location', None)

        return canvases_with_schedules
