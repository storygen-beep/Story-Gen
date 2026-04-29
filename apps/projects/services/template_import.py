"""
Template import service for creating a new Project from a single TOML file.

Scope v0.1: project basics, time, player, NPCs, locations + navigation only.
No twee generation or canvases. Creates a brand-new Project and related rows.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
import uuid
from typing import Any, Dict, List, Optional, Set, Tuple

import tomli
from django.contrib.auth import get_user_model
from django.db import transaction

from apps.projects.models import Project
from apps.characters.models import Character
from apps.npcs.models import NPC
from apps.world.models import Location
from apps.stories.models import (
    StoryCanvas,
    StoryNode,
    NodeConnection,
    CanvasTrigger,
    TriggerSchedule,
)
from apps.stories.services.block_conversion import BlockConversionService


User = get_user_model()

logger = logging.getLogger(__name__)


# -------- Data Shapes (World & Player/NPC) --------


@dataclass
class TemplateProject:
    slug: str
    title: str
    description: str = ""


@dataclass
class TemplateTime:
    enabled: bool = True
    starting_hour: int = 8
    starting_day: str = "Monday"
    starting_week: int = 1


@dataclass
class TemplatePlayerCustomizationOption:
    """An option for image_select fields (portrait/look selection)."""
    id: str
    image: str = ""
    label: str = ""


@dataclass
class TemplatePlayerCustomizationField:
    """A single customization field for the player character."""
    id: str                       # field identifier (lowercase_snake_case)
    type: str                     # "text", "select", "image_select"
    label: str = ""               # display label
    default: str = ""             # default value
    options: List[Any] = field(default_factory=list)  # str list for select, Option list for image_select
    sets_portrait: bool = False   # image_select only: selected image becomes $player.portrait


@dataclass
class TemplatePlayer:
    id: str = "player"
    name: str = "Player"
    description: str = ""
    portrait: str = ""  # Relative to video_folder, e.g., "player.jpg"
    core_traits: Dict[str, Any] = field(default_factory=dict)
    flag_keys: List[str] = field(default_factory=list)
    customizable: bool = False
    customization_fields: List[TemplatePlayerCustomizationField] = field(default_factory=list)
    trait_decay: Dict[str, float] = field(default_factory=dict)


@dataclass
class TemplateNPCSchedule:
    """A time-based schedule entry for NPC location."""

    location: str  # Location ID where NPC will be
    weekdays: List[int] = field(
        default_factory=list
    )  # 0=Monday..6=Sunday, empty=all days
    start_time: str = "00:00"  # HH:MM format
    end_time: Optional[str] = None  # HH:MM format (optional)
    activity: str = ""  # Description of what NPC is doing at this location


@dataclass
class TemplateNPC:
    id: str
    name: str
    description: str = ""
    portrait: str = ""  # Relative to video_folder, e.g., "angela.jpg"
    core_traits: Dict[str, Any] = field(default_factory=dict)
    flag_keys: List[str] = field(default_factory=list)
    schedules: List[TemplateNPCSchedule] = field(default_factory=list)
    customizable: bool = False  # Player can rename at game start
    relationship: Optional[str] = None  # Default relationship label (e.g., "step-brother")
    relationship_options: List[str] = field(default_factory=list)  # Choices for relationship picker
    # Trait decay: {trait_name: decay_per_day}. Traits decay by this amount each day
    # the player doesn't interact with this NPC. Keys must exist in core_traits.
    trait_decay: Dict[str, float] = field(default_factory=dict)
    # UI visibility: when True, the NPC is omitted from the Guide Page, Stats Page,
    # and sidebar NPC-traits widget. Runtime $npcs dict still contains the NPC so
    # prologue/narrative dialog speaker lookups by UUID keep working.
    hidden_from_ui: bool = False
    # E9/E10/E11: ordered stage display names. Length implies max stage value
    # (len-1). Empty = NPC has no stage chain. The corresponding integer stage
    # value lives in $player.core_traits[<slug>_stage]. Used by:
    #   - E9 stalled-detection registry (NPC with arc_stages → tracked for stalls)
    #   - E10 hint stage_gate validation (stage_npc must reference one of these)
    #   - E11 stage_label sidebar widget (renders arc_stages[current_stage])
    arc_stages: List[str] = field(default_factory=list)


@dataclass
class TemplateLocation:
    id: str
    name: str
    description: str = ""
    image: str = ""  # Relative to video_folder, e.g., "locations/kitchen.jpg"
    image_search_queries: List[str] = field(default_factory=list)  # For Missing Media page
    is_container: bool = False
    parent: str = ""
    entry_from: str = ""
    default_entry: str = ""
    navigation_order: List[str] = field(default_factory=list)
    entry_conditions: Dict[str, Any] = field(default_factory=dict)
    blocked_message: str = ""
    clothing_rules: List[Dict[str, Any]] = field(default_factory=list)


# -------- Clothing System Data Shapes --------

VALID_CLOTHING_SLOTS = {"bra", "underwear", "top", "bottom", "dress", "legwear", "shoes"}


@dataclass
class TemplateClothingItem:
    id: str
    name: str
    slot: str  # Must be in VALID_CLOTHING_SLOTS
    image: str = ""  # Relative to video_folder, e.g., "clothing/white_blouse.jpg"
    initial: bool = False  # If true, player starts with this item
    conditions: Dict[str, Any] = field(default_factory=dict)  # v1.0 conditions for wearing
    price: int = 0  # Price in dollars, 0 for initial/free items


@dataclass
class TemplateClothingRequirements:
    body_coverage: bool = True  # Must wear (top + bottom) OR dress
    always_required: List[str] = field(default_factory=list)  # Slots that can never be removed
    conditional: Dict[str, Dict[str, str]] = field(default_factory=dict)  # slot -> {until_flag, message}


# -------- Phone System Data Shapes --------

VALID_PHONE_APP_TYPES = {"chat", "social_feed", "gallery", "dating", "custom"}


@dataclass
class TemplatePhoneApp:
    id: str
    type: str  # "chat", "social_feed", "gallery", "custom"
    label: str = ""
    icon: str = ""  # Relative to video_folder, optional


@dataclass
class TemplatePhoneConversationBlock:
    type: str  # "message" or "reply"
    sender: str = ""  # "npc" or "player" (for message type)
    content: str = ""
    after_reply: bool = False
    choices: List[Dict[str, Any]] = field(default_factory=list)  # for reply type
    # Multi-round conversation support
    round: Optional[int] = None        # For reply blocks: which round this is (1, 2, 3...)
    after_round: Optional[int] = None  # Show only after this round is answered
    after_choice: Optional[int] = None # Show only if this choice was picked in after_round


@dataclass
class TemplatePhoneConversation:
    id: str
    app: str  # which chat app this belongs to
    npc: str  # NPC slug (e.g., "npc_alex")
    trigger: Dict[str, Any] = field(default_factory=dict)  # conditions dict
    blocks: List[TemplatePhoneConversationBlock] = field(default_factory=list)


@dataclass
class TemplatePhonePost:
    id: str
    app: str              # which social_feed app
    npc: str = ""         # NPC slug (optional — empty for stranger posts)
    poster_name: str = "" # display name for non-NPC posters (e.g. "@jessicafit_")
    image: str = ""
    caption: str = ""
    likes: int = 0
    trigger: Dict[str, Any] = field(default_factory=dict)
    search_queries: List[str] = field(default_factory=list)


@dataclass
class TemplatePhoneProfile:
    id: str
    app: str              # which dating app
    npc: str
    photos: List[str] = field(default_factory=list)
    bio: str = ""
    age: str = ""
    interests: List[str] = field(default_factory=list)
    trigger: Dict[str, Any] = field(default_factory=dict)
    match_condition: Dict[str, Any] = field(default_factory=dict)
    search_queries: List[str] = field(default_factory=list)


@dataclass
class TemplatePhoneDailyTopic:
    id: str
    npc: str
    player_message: str = ""
    npc_response: str = ""
    effects: List[Dict[str, Any]] = field(default_factory=list)
    conditions: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TemplatePhone:
    enabled: bool = True
    apps: List[TemplatePhoneApp] = field(default_factory=list)
    conversations: List[TemplatePhoneConversation] = field(default_factory=list)
    posts: List[TemplatePhonePost] = field(default_factory=list)
    profiles: List[TemplatePhoneProfile] = field(default_factory=list)
    daily_topics: List[TemplatePhoneDailyTopic] = field(default_factory=list)


@dataclass
class GameTemplate:
    schema_version: str
    project: TemplateProject
    time: TemplateTime
    player: TemplatePlayer
    npcs: List[TemplateNPC]
    locations: List[TemplateLocation]
    # Story additions (v0.2)
    starting_canvas: Optional[str] = None
    canvases: List["TemplateCanvas"] = field(default_factory=list)
    # Story arc for narrative journal (v0.3)
    story_arc: Optional["TemplateStoryArc"] = None
    # Clothing system
    clothing_enabled: bool = False
    clothing_items: List[TemplateClothingItem] = field(default_factory=list)
    wardrobe_location: Optional[str] = None
    shop_location: Optional[str] = None
    clothing_requirements: Optional[TemplateClothingRequirements] = None
    # Rent system
    rent_enabled: bool = False
    rent_amount: int = 0
    rent_due_day: str = "Monday"
    rent_collector_npc: Optional[str] = None
    rent_grace_periods: int = 1
    rent_start_after_flag: str = ""
    rent_text: Dict[str, str] = field(default_factory=dict)
    rent_eviction_mode: str = "game_end"  # "game_end" (legacy) | "flag_set" (fail-forward)
    rent_eviction_flag: str = "rent_evicted"
    # Sidebar items (custom display elements)
    sidebar_items: List[Dict[str, Any]] = field(default_factory=list)
    # Phone system
    phone_enabled: bool = False
    phone: Optional[TemplatePhone] = None
    # Recurring passes (gym, bus, etc.)
    passes: List[TemplatePass] = field(default_factory=list)
    # Consumable items (groceries, art supplies, etc.)
    items: List[TemplateItem] = field(default_factory=list)
    # Visual theme
    theme: Optional[TemplateTheme] = None
    # Day-rollover hook — fires inside window.advanceDay() once per day flip.
    # Authored under [engine.daily_tick] in TOML. Used for daily-cooldown flag clears.
    daily_tick: Optional["TemplateDailyTick"] = None
    # E4: named composite gates. Authored under [[engine.stage_helpers]] in TOML.
    # A condition with `type = "stage"` references one of these by name.
    stage_helpers: List["TemplateStageHelper"] = field(default_factory=list)


@dataclass
class TemplateDailyTick:
    """Effects that fire once per in-game day at advanceDay() rollover.

    Today only flagEffects are supported. The hook calls window.applyFlagEffect
    directly (no notification queueing) so daily clears are silent.
    """
    flagEffects: List[TemplateFlagEffect] = field(default_factory=list)


@dataclass
class TemplateStageHelper:
    """Named composite gate. Recipe of conditions referenced by name.

    Helpers reference primitive condition types only — recursion (helper
    references helper) is rejected at validate() time. Single-level lookup
    in runtime keeps cycle risk zero.
    """
    name: str
    description: str = ""
    conditions: Dict[str, Any] = field(default_factory=dict)


# -------- Story Data Shapes (v0.2) --------


@dataclass
class TemplateTriggerSchedule:
    weekdays: List[int]
    start_time: str
    end_time: Optional[str] = None


@dataclass
class TemplateTrigger:
    location: str
    is_active: bool = True
    is_repeatable: bool = True
    max_triggers_per_day: Optional[int] = None
    priority: int = 0  # Higher priority canvases selected first when multiple valid
    conditions: Dict[str, Any] = field(default_factory=dict)
    schedules: List[TemplateTriggerSchedule] = field(default_factory=list)
    npc: Optional[str] = None  # NPC slug for this canvas (for navigation indicators)
    trigger_mode: str = "manual"  # "manual" (clickable link) or "random" (auto-fires with probability)
    chance: Optional[float] = None  # Probability 0.0–1.0 for random trigger mode
    costs: List[Dict[str, Any]] = field(default_factory=list)  # [{trait: str, value: int}] — resource costs deducted on canvas entry


@dataclass
class TemplateChoiceEffect:
    targetType: str = "player"  # 'player'|'npc'
    npcId: Optional[str] = None
    trait: str = ""
    op: str = "add"  # 'add'|'set'
    value: Any = 0
    clamp: Optional[bool] = None
    cap: Optional[Any] = None
    # Optional flag field - allows flag effects mixed into effects array
    flag: Optional[str] = None


@dataclass
class TemplateFlagEffect:
    targetType: str = "player"  # 'player'|'npc'
    npcId: Optional[str] = None
    flag: str = ""
    op: str = "set"  # 'set'|'unset'|'toggle' — runtime defaults to set when unrecognized


@dataclass
class TemplateModifierEffect:
    key: str = ""  # modifier identifier (e.g., "tipsy")
    name: str = ""  # display name (e.g., "Tipsy")
    duration_hours: int = 1  # how long it lasts in game hours
    trait_offsets: Dict[str, float] = field(default_factory=dict)  # {trait: offset} for condition checks


@dataclass
class TemplatePass:
    id: str = ""
    name: str = ""
    cost: int = 0
    duration_days: int = 30
    icon: str = ""


@dataclass
class TemplateItem:
    id: str = ""
    name: str = ""
    icon: str = ""
    max_stack: int = 99


@dataclass
class TemplateTheme:
    mode: str = "light"                          # "dark" or "light"
    primary: str = "#4a90d9"                     # Main accent (buttons, links)
    secondary: str = "#764ba2"                   # Secondary accent
    accent: str = "#4ecdc4"                      # Tertiary highlight
    success: str = "#22c55e"                     # Success states
    danger: str = "#dc3545"                      # Error/danger
    warning: str = "#ffc107"                     # Warnings
    font_heading: str = "Georgia, serif"         # Heading font
    font_mono: str = "'Courier New', monospace"  # Monospace font
    border_radius: str = "8px"                   # Global rounding
    # Optional overrides (auto-derived from mode if empty)
    bg: str = ""
    surface: str = ""
    surface_alt: str = ""
    border: str = ""
    text: str = ""
    text_muted: str = ""
    custom_css: str = ""


@dataclass
class TemplateChoice:
    text: str = "Continue"
    targetType: str = "trigger"  # 'trigger'|'location'|'node'
    locationId: Optional[str] = None
    nodeId: Optional[str] = None
    time_progression_minutes: Optional[int] = None
    effects: List[TemplateChoiceEffect] = field(default_factory=list)
    flagEffects: List[TemplateFlagEffect] = field(default_factory=list)
    wardrobeEffects: List[Dict[str, Any]] = field(default_factory=list)
    conditions: Dict[str, Any] = field(default_factory=dict)
    # Rejection system: controls what happens when conditions are NOT met
    show_when_locked: bool = False  # If True, show choice greyed out when conditions fail
    locked_text: str = ""  # Tooltip/reason text shown when locked (e.g., "She's not ready")
    rejection_node: Optional[str] = None  # Node to redirect to on rejection (clickable even locked)
    rejection_effects: List[TemplateChoiceEffect] = field(default_factory=list)  # Effects on rejection
    # Temporary modifier system: apply short-lived trait offsets to condition checks
    modifier_effects: List[TemplateModifierEffect] = field(default_factory=list)
    # Recurring pass system: purchase time-limited passes
    pass_effects: List[Dict[str, str]] = field(default_factory=list)
    # Inventory system: add/remove consumable items
    item_effects: List[Dict[str, Any]] = field(default_factory=list)
    # E6: per-choice text variants — first match wins, falls back to `text`.
    # Each variant: {"text": str, "conditions": {version, items}}.
    text_variants: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class TemplateExitBlock:
    type: str = "location"  # 'location'|'choices'
    text: str = "Continue"
    config: Dict[str, Any] = field(default_factory=dict)
    choices: List[TemplateChoice] = field(default_factory=list)


@dataclass
class TemplateNode:
    id: str
    name: str
    blocks: List[Dict[str, Any]] = field(default_factory=list)
    exit_block: TemplateExitBlock = field(default_factory=TemplateExitBlock)
    loop_terminal: bool = False
    # Modifier redirect: if modifier is active, show this node instead
    # e.g., {"modifier_key": "tipsy", "node": "base_tipsy"}
    modifier_redirect: Optional[Dict[str, str]] = None


@dataclass
class TemplateConnection:
    source: str
    target: str
    connection_type: str = "default"


@dataclass
class TemplateCanvas:
    id: str
    name: str
    description: str = ""
    trigger: Optional[TemplateTrigger] = None
    nodes: List[TemplateNode] = field(default_factory=list)
    connections: List[TemplateConnection] = field(default_factory=list)
    loop: Dict[str, Any] = field(default_factory=dict)


# -------- Story Arc Data Shapes (v0.3) --------


@dataclass
class TemplateStoryChapter:
    """A chapter in the story arc - provides narrative framing."""

    id: str
    name: str
    mood: str = "neutral"  # hopeful|romantic|tense|passionate|peaceful|neutral
    description: str = ""
    order: int = 0


@dataclass
class TemplateStoryNode:
    """A story node - represents a moment in the narrative graph."""

    id: str
    name: str
    chapter: str = ""
    journal_entry: str = ""
    linked_canvas: Optional[str] = None  # Canvas ID that completes this node
    linked_canvas_node: Optional[str] = None  # Specific node within linked_canvas
    linked_flag: Optional[str] = None  # Flag that completes this node
    group: Optional[str] = None  # Part of a parallel group
    requires_group: Optional[str] = None  # Requires a group to be complete
    requires_nodes: List[str] = field(default_factory=list)  # Requires specific nodes
    is_milestone: bool = False  # Major story beat
    npc: Optional[str] = None  # Associated NPC for Quest Page
    trait_requirements: List[dict] = field(
        default_factory=list
    )  # Trait requirements to unlock
    branch_condition: Optional[str] = None  # Flag that must be set for node to be visible
    linked_phone: Optional[str] = None  # Phone conversation ID that completes this node
    guide_hint: str = ""  # Override hint text for Guide page


@dataclass
class TemplateStoryGroup:
    """A parallel activity group - complete N of M activities."""

    id: str
    name: str
    description: str = ""
    required_count: int = 1  # How many members must be completed


@dataclass
class TemplateEmotionRange:
    """A range mapping trait value to emotional description."""

    min: int
    max: int
    label: str
    description: str


@dataclass
class TemplateEmotionMapping:
    """Maps a trait to emotional descriptions at various ranges."""

    trait_owner: str = "npc"  # player|npc
    default_npc: Optional[str] = None
    ranges: List[TemplateEmotionRange] = field(default_factory=list)


@dataclass
class TemplateHintCondition:
    """Condition for when to show a hint."""

    missing_flag: Optional[str] = None
    missing_trait: Optional[str] = None
    gap_gte: Optional[int] = None


@dataclass
class TemplateHintTemplate:
    """A hint template with conditions."""

    condition: Optional[TemplateHintCondition] = None
    text: str = ""


@dataclass
class TemplateStoryHints:
    """Hint configuration for story journal."""

    stuck_threshold_minutes: int = 30
    hint_style: str = "observation"  # observation|suggestion|memory
    templates: List[TemplateHintTemplate] = field(default_factory=list)


@dataclass
class TemplateStoryArc:
    """Complete story arc definition for intelligent narrative tracking."""

    version: str = "1.0"
    chapters: List[TemplateStoryChapter] = field(default_factory=list)
    nodes: List[TemplateStoryNode] = field(default_factory=list)
    groups: List[TemplateStoryGroup] = field(default_factory=list)
    emotion_mappings: Dict[str, TemplateEmotionMapping] = field(default_factory=dict)
    hints: Optional[TemplateStoryHints] = None


# -------- Parsing / Normalization --------


def parse_toml(path: str) -> Dict[str, Any]:
    with open(path, "rb") as f:
        return tomli.load(f)


def _require_str(obj: Dict[str, Any], key: str, default: Optional[str] = None) -> str:
    val = obj.get(key, default)
    if val is None and default is None:
        return ""
    if val is not None and not isinstance(val, str):
        raise TypeError(
            f"Field '{key}' must be string, got {type(val).__name__}: {val}"
        )
    return val if isinstance(val, str) else (default or "")


def _require_bool(obj: Dict[str, Any], key: str, default: bool) -> bool:
    val = obj.get(key, default)
    return bool(val)


def _require_int(obj: Dict[str, Any], key: str, default: int) -> int:
    val = obj.get(key, default)
    if val is None:
        return default
    try:
        return int(val)
    except (ValueError, TypeError) as e:
        raise TypeError(
            f"Field '{key}' must be integer, got {type(val).__name__}: {val}"
        ) from e


def _require_dict(obj: Dict[str, Any], key: str) -> Dict[str, Any]:
    val = obj.get(key, {})
    if val is not None and not isinstance(val, dict):
        raise TypeError(f"Field '{key}' must be dict/table, got {type(val).__name__}")
    return val if isinstance(val, dict) else {}


def _require_list(obj: Dict[str, Any], key: str) -> List[Any]:
    val = obj.get(key, [])
    if val is not None and not isinstance(val, list):
        raise TypeError(f"Field '{key}' must be list/array, got {type(val).__name__}")
    return val if isinstance(val, list) else []


def _validate_weekdays(weekdays_raw: List[Any], context: str) -> List[int]:
    """Validate and convert weekdays list, raising errors for invalid values."""
    if not weekdays_raw:
        return []
    weekdays = []
    for i, x in enumerate(weekdays_raw):
        if not isinstance(x, int):
            raise TypeError(
                f"{context} weekdays[{i}] must be int, got {type(x).__name__}: {x}"
            )
        if x < 0 or x > 6:
            raise ValueError(f"{context} weekdays[{i}] must be 0-6, got {x}")
        weekdays.append(x)
    return weekdays


def normalize(data: Dict[str, Any]) -> GameTemplate:
    schema_version = _require_str(data, "schema_version", "0.1")

    # Required: [project] section
    p = data.get("project")
    if p is None:
        raise ValueError("Missing required [project] section in TOML")
    if not isinstance(p, dict):
        raise TypeError(f"[project] must be a table, got {type(p).__name__}")
    project = TemplateProject(
        slug=_require_str(p, "id"),
        title=_require_str(p, "title"),
        description=_require_str(p, "description"),
    )

    # Optional: [time] section (has sensible defaults)
    t = data.get("time", {}) or {}
    time = TemplateTime(
        enabled=_require_bool(t, "enabled", True),
        starting_hour=_require_int(t, "starting_hour", 8),
        starting_day=_require_str(t, "starting_day", "Monday"),
        starting_week=_require_int(t, "starting_week", 1),
    )

    # Optional: [player] section (has sensible defaults)
    pl = data.get("player", {}) or {}

    # Parse player customization fields
    player_customization_fields: List[TemplatePlayerCustomizationField] = []
    for fi, f in enumerate(pl.get("customization_fields") or []):
        if not isinstance(f, dict):
            raise TypeError(f"player.customization_fields[{fi}] must be a table")
        field_type = _require_str(f, "type", "")
        field_options: List[Any] = []
        if field_type == "image_select":
            for oi, opt in enumerate(f.get("options") or []):
                if not isinstance(opt, dict):
                    raise TypeError(
                        f"player.customization_fields[{fi}].options[{oi}] must be a table for image_select"
                    )
                field_options.append(TemplatePlayerCustomizationOption(
                    id=_require_str(opt, "id", ""),
                    image=_require_str(opt, "image", ""),
                    label=_require_str(opt, "label", ""),
                ))
        elif field_type == "select":
            field_options = [str(o) for o in (f.get("options") or [])]
        player_customization_fields.append(TemplatePlayerCustomizationField(
            id=_require_str(f, "id", ""),
            type=field_type,
            label=_require_str(f, "label", ""),
            default=_require_str(f, "default", ""),
            options=field_options,
            sets_portrait=bool(f.get("sets_portrait", False)),
        ))

    # Parse player trait_decay: {trait_name: decay_per_day}
    player_trait_decay_raw = pl.get("trait_decay") or {}
    player_trait_decay: Dict[str, float] = {}
    if isinstance(player_trait_decay_raw, dict):
        for k, v in player_trait_decay_raw.items():
            try:
                player_trait_decay[str(k)] = float(v)
            except (ValueError, TypeError):
                raise TypeError(
                    f"player.trait_decay['{k}'] must be a number, got {type(v).__name__}"
                )

    player = TemplatePlayer(
        id=_require_str(pl, "id", "player"),
        name=_require_str(pl, "name", "Player"),
        description=_require_str(pl, "description", ""),
        portrait=_require_str(pl, "portrait", ""),
        core_traits=_require_dict(pl, "core_traits"),
        flag_keys=_require_list(pl, "flag_keys"),
        customizable=bool(pl.get("customizable", False)),
        customization_fields=player_customization_fields,
        trait_decay=player_trait_decay,
    )

    npcs_raw = data.get("npcs", []) or []
    npcs = []
    for ni, n in enumerate(npcs_raw):
        if not isinstance(n, dict):
            raise TypeError(f"npcs[{ni}] must be a table, got {type(n).__name__}")
        # Parse NPC schedules
        npc_schedules: List[TemplateNPCSchedule] = []
        for si, sch in enumerate(n.get("schedules") or []):
            if not isinstance(sch, dict):
                raise TypeError(
                    f"npcs[{ni}].schedules[{si}] must be a table, got {type(sch).__name__}"
                )
            npc_schedules.append(
                TemplateNPCSchedule(
                    location=_require_str(sch, "location", ""),
                    weekdays=_validate_weekdays(
                        sch.get("weekdays") or [], f"npcs[{ni}].schedules[{si}]"
                    ),
                    start_time=_require_str(sch, "start_time", "00:00"),
                    end_time=_require_str(sch, "end_time", "") or None,
                    activity=_require_str(sch, "activity", ""),
                )
            )
        # Parse trait_decay: {trait_name: decay_per_day}
        trait_decay_raw = n.get("trait_decay") or {}
        trait_decay: Dict[str, float] = {}
        if isinstance(trait_decay_raw, dict):
            for k, v in trait_decay_raw.items():
                try:
                    trait_decay[str(k)] = float(v)
                except (ValueError, TypeError):
                    raise TypeError(
                        f"npcs[{ni}].trait_decay['{k}'] must be a number, got {type(v).__name__}"
                    )

        # Parse arc_stages: ordered list of stage display names.
        # Empty/missing = NPC has no stage chain (default; existing TOMLs unaffected).
        arc_stages_raw = n.get("arc_stages") or []
        if not isinstance(arc_stages_raw, list):
            raise TypeError(
                f"npcs[{ni}].arc_stages must be a list, got {type(arc_stages_raw).__name__}"
            )
        arc_stages: List[str] = []
        for si, stage in enumerate(arc_stages_raw):
            if not isinstance(stage, str):
                raise TypeError(
                    f"npcs[{ni}].arc_stages[{si}] must be a string, "
                    f"got {type(stage).__name__}: {stage!r}"
                )
            arc_stages.append(stage)

        npcs.append(
            TemplateNPC(
                id=_require_str(n, "id"),
                name=_require_str(n, "name"),
                description=_require_str(n, "description", ""),
                portrait=_require_str(n, "portrait", ""),
                core_traits=_require_dict(n, "core_traits"),
                flag_keys=_require_list(n, "flag_keys"),
                schedules=npc_schedules,
                customizable=bool(n.get("customizable", False)),
                relationship=_require_str(n, "relationship", "") or None,
                relationship_options=_require_list(n, "relationship_options"),
                trait_decay=trait_decay,
                hidden_from_ui=bool(n.get("hidden_from_ui", False)),
                arc_stages=arc_stages,
            )
        )

    locs_raw = data.get("locations", []) or []
    locations = []
    for l in locs_raw:
        if not isinstance(l, dict):
            continue
        locations.append(
            TemplateLocation(
                id=_require_str(l, "id"),
                name=_require_str(l, "name"),
                description=_require_str(l, "description", ""),
                image=_require_str(l, "image", ""),
                image_search_queries=[str(q) for q in _require_list(l, "image_search_queries")],
                is_container=bool(l.get("is_container", False)),
                parent=_require_str(l, "parent", ""),
                entry_from=_require_str(l, "entry_from", ""),
                default_entry=_require_str(l, "default_entry", ""),
                navigation_order=[str(x) for x in _require_list(l, "navigation_order")],
                entry_conditions=_require_dict(l, "entry_conditions"),
                blocked_message=_require_str(l, "blocked_message", ""),
                clothing_rules=l.get("clothing_rules", []) or [],
            )
        )

    # Story - starting_canvas (check both root level and [project] section)
    starting_canvas = _require_str(data, "starting_canvas", "") or None
    if not starting_canvas and isinstance(data.get("project"), dict):
        starting_canvas = _require_str(data["project"], "starting_canvas", "") or None

    # Define story dataclasses inline to avoid forward reference issues
    # We'll parse canvases below only if present
    canvases: List[TemplateCanvas] = []
    if isinstance(data.get("canvases"), list):
        for c in data.get("canvases") or []:
            if not isinstance(c, dict):
                continue
            # Trigger
            trig_def = c.get("trigger") or None
            trigger_obj = None
            if isinstance(trig_def, dict):
                schedules: List[TemplateTriggerSchedule] = []
                for sch in trig_def.get("schedules") or []:
                    if not isinstance(sch, dict):
                        continue
                    schedules.append(
                        TemplateTriggerSchedule(
                            weekdays=[
                                int(x)
                                for x in (sch.get("weekdays") or [])
                                if isinstance(x, int)
                            ],
                            start_time=_require_str(sch, "start_time", "00:00"),
                            end_time=_require_str(sch, "end_time", "") or None,
                        )
                    )
                trigger_obj = TemplateTrigger(
                    location=_require_str(trig_def, "location", ""),
                    is_active=bool(trig_def.get("is_active", True)),
                    is_repeatable=bool(trig_def.get("is_repeatable", True)),
                    max_triggers_per_day=(
                        int(trig_def.get("max_triggers_per_day"))
                        if trig_def.get("max_triggers_per_day") is not None
                        else None
                    ),
                    priority=int(trig_def.get("priority", 0)),
                    conditions=_require_dict(trig_def, "conditions"),
                    schedules=schedules,
                    npc=_require_str(trig_def, "npc", "") or None,
                    trigger_mode=_require_str(trig_def, "trigger_mode", "manual"),
                    chance=(
                        float(trig_def.get("chance"))
                        if trig_def.get("chance") is not None
                        else None
                    ),
                    costs=[
                        {"trait": str(ci["trait"]), "value": int(ci["value"])}
                        for ci in (trig_def.get("costs") or [])
                        if isinstance(ci, dict) and "trait" in ci and "value" in ci
                    ],
                )

            # Nodes
            nodes: List[TemplateNode] = []
            for n in c.get("nodes") or []:
                if not isinstance(n, dict):
                    continue
                eb_raw = n.get("exit_block", {}) or {}
                choices: List[TemplateChoice] = []
                for ch in eb_raw.get("choices") or []:
                    if not isinstance(ch, dict):
                        continue
                    effs = []
                    for e in ch.get("effects") or []:
                        if not isinstance(e, dict):
                            continue
                        effs.append(
                            TemplateChoiceEffect(
                                targetType=str(e.get("targetType", "player")),
                                npcId=_require_str(e, "npcId", "") or None,
                                trait=_require_str(e, "trait", ""),
                                op=_require_str(e, "op", "add"),
                                value=e.get("value", 0),
                                clamp=e.get("clamp", None),
                                cap=e.get("cap", None),
                                flag=_require_str(e, "flag", "") or None,
                            )
                        )
                    flag_effs = []
                    for e in ch.get("flagEffects") or []:
                        if not isinstance(e, dict):
                            continue
                        flag_effs.append(
                            TemplateFlagEffect(
                                targetType=str(e.get("targetType", "player")),
                                npcId=_require_str(e, "npcId", "") or None,
                                flag=_require_str(e, "flag", ""),
                                op=_require_str(e, "op", "set") or "set",
                            )
                        )
                    # E7: `inc` shorthand — expands into add-op TemplateChoiceEffect rows.
                    # Accepts either ["counter_name"] (step=1) or [{counter, by}] forms.
                    for inc_item in ch.get("inc") or []:
                        if isinstance(inc_item, str):
                            counter, by = inc_item, 1
                        elif isinstance(inc_item, dict):
                            counter = _require_str(inc_item, "counter", "")
                            try:
                                by = int(inc_item.get("by", 1))
                            except (TypeError, ValueError):
                                by = 1
                        else:
                            continue
                        if not counter:
                            continue
                        effs.append(
                            TemplateChoiceEffect(
                                targetType="player",
                                trait=counter,
                                op="add",
                                value=by,
                            )
                        )
                    wardrobe_effs = [
                        e for e in (ch.get("wardrobeEffects") or [])
                        if isinstance(e, dict)
                    ]
                    # Parse rejection_effects (same structure as regular effects)
                    rej_effs = []
                    for e in ch.get("rejection_effects") or []:
                        if not isinstance(e, dict):
                            continue
                        rej_effs.append(
                            TemplateChoiceEffect(
                                targetType=str(e.get("targetType", "player")),
                                npcId=_require_str(e, "npcId", "") or None,
                                trait=_require_str(e, "trait", ""),
                                op=_require_str(e, "op", "add"),
                                value=e.get("value", 0),
                                clamp=e.get("clamp", None),
                                cap=e.get("cap", None),
                                flag=_require_str(e, "flag", "") or None,
                            )
                        )

                    # Parse modifier_effects
                    mod_effs: List[TemplateModifierEffect] = []
                    for me in ch.get("modifier_effects") or []:
                        if not isinstance(me, dict):
                            continue
                        # Parse trait_offsets dict
                        raw_offsets = me.get("trait_offsets") or {}
                        trait_offsets: Dict[str, float] = {}
                        if isinstance(raw_offsets, dict):
                            for k, v in raw_offsets.items():
                                try:
                                    trait_offsets[str(k)] = float(v)
                                except (ValueError, TypeError):
                                    pass
                        mod_effs.append(
                            TemplateModifierEffect(
                                key=_require_str(me, "key", ""),
                                name=_require_str(me, "name", ""),
                                duration_hours=int(me.get("duration_hours", 1)),
                                trait_offsets=trait_offsets,
                            )
                        )

                    # Parse passEffects (recurring pass purchases)
                    pass_effs: List[Dict[str, str]] = []
                    for pe in ch.get("passEffects") or []:
                        if isinstance(pe, dict) and pe.get("pass_id"):
                            pass_effs.append({"pass_id": str(pe["pass_id"])})

                    # Parse itemEffects (inventory add/remove)
                    item_effs: List[Dict[str, Any]] = []
                    for ie in ch.get("itemEffects") or []:
                        if isinstance(ie, dict) and ie.get("item_id"):
                            item_effs.append({
                                "item_id": str(ie["item_id"]),
                                "action": str(ie.get("action", "add")),
                                "quantity": int(ie.get("quantity", 1)),
                            })

                    # E6: parse text_variants — list of {text, conditions} dicts.
                    text_variants_parsed: List[Dict[str, Any]] = []
                    for v_raw in ch.get("text_variants") or []:
                        if not isinstance(v_raw, dict):
                            continue
                        text_variants_parsed.append(
                            {
                                "text": _require_str(v_raw, "text", ""),
                                "conditions": _require_dict(v_raw, "conditions"),
                            }
                        )
                    choices.append(
                        TemplateChoice(
                            text=_require_str(ch, "text", "Continue"),
                            targetType=_require_str(ch, "targetType", "trigger"),
                            locationId=_require_str(ch, "locationId", "") or None,
                            nodeId=_require_str(ch, "nodeId", "") or None,
                            time_progression_minutes=(
                                int(ch.get("time_progression_minutes"))
                                if isinstance(
                                    ch.get("time_progression_minutes"), (int, float)
                                )
                                else None
                            ),
                            effects=effs,
                            flagEffects=flag_effs,
                            wardrobeEffects=wardrobe_effs,
                            conditions=_require_dict(ch, "conditions"),
                            show_when_locked=bool(ch.get("show_when_locked", False)),
                            locked_text=_require_str(ch, "locked_text", ""),
                            rejection_node=_require_str(ch, "rejection_node", "") or None,
                            rejection_effects=rej_effs,
                            modifier_effects=mod_effs,
                            pass_effects=pass_effs,
                            item_effects=item_effs,
                            text_variants=text_variants_parsed,
                        )
                    )
                # Validate exit_block type
                eb_type = _require_str(eb_raw, "type", "")
                if not eb_type:
                    eb_type = "location"  # Default for backwards compatibility
                valid_eb_types = {"choices", "location", "trigger", "canvas", "game_end"}
                if eb_type not in valid_eb_types:
                    node_id = n.get("id", "unknown")
                    raise ValueError(
                        f"exit_block.type '{eb_type}' invalid in node '{node_id}'. "
                        f"Must be one of: {valid_eb_types}"
                    )
                exit_block = TemplateExitBlock(
                    type=eb_type,
                    text=_require_str(eb_raw, "text", "Continue"),
                    config=_require_dict(eb_raw, "config"),
                    choices=choices,
                )
                # Parse modifier_redirect (optional dict with modifier_key + node)
                mod_redirect_raw = n.get("modifier_redirect")
                mod_redirect = None
                if isinstance(mod_redirect_raw, dict) and mod_redirect_raw:
                    mod_redirect = {
                        "modifier_key": _require_str(mod_redirect_raw, "modifier_key", ""),
                        "node": _require_str(mod_redirect_raw, "node", ""),
                    }

                nodes.append(
                    TemplateNode(
                        id=_require_str(n, "id"),
                        name=_require_str(n, "name"),
                        blocks=_require_list(n, "blocks"),
                        exit_block=exit_block,
                        loop_terminal=_require_bool(n, "loop_terminal", False),
                        modifier_redirect=mod_redirect,
                    )
                )

            conns: List[TemplateConnection] = []
            for cc in c.get("connections") or []:
                if not isinstance(cc, dict):
                    continue
                conns.append(
                    TemplateConnection(
                        source=_require_str(cc, "source"),
                        target=_require_str(cc, "target"),
                        connection_type=_require_str(cc, "connection_type", "default"),
                    )
                )

            canvases.append(
                TemplateCanvas(
                    id=_require_str(c, "id"),
                    name=_require_str(c, "name"),
                    description=_require_str(c, "description", ""),
                    trigger=trigger_obj,
                    nodes=nodes,
                    connections=conns,
                    loop=_require_dict(c, "loop"),
                )
            )

    # -------- Parse story_arc section (v0.3) --------
    story_arc_obj: Optional[TemplateStoryArc] = None
    sa_raw = data.get("story_arc")
    if isinstance(sa_raw, dict):
        # Parse chapters
        chapters: List[TemplateStoryChapter] = []
        for ch in _require_list(sa_raw, "chapters"):
            if isinstance(ch, dict):
                chapters.append(
                    TemplateStoryChapter(
                        id=_require_str(ch, "id"),
                        name=_require_str(ch, "name"),
                        mood=_require_str(ch, "mood", "neutral"),
                        description=_require_str(ch, "description", ""),
                        order=_require_int(ch, "order", 0),
                    )
                )

        # Parse nodes
        story_nodes: List[TemplateStoryNode] = []
        for n in _require_list(sa_raw, "nodes"):
            if isinstance(n, dict):
                story_nodes.append(
                    TemplateStoryNode(
                        id=_require_str(n, "id"),
                        name=_require_str(n, "name"),
                        chapter=_require_str(n, "chapter", ""),
                        journal_entry=_require_str(n, "journal_entry", ""),
                        linked_canvas=_require_str(n, "linked_canvas", "") or None,
                        linked_canvas_node=_require_str(n, "linked_canvas_node", "") or None,
                        linked_flag=_require_str(n, "linked_flag", "") or None,
                        group=_require_str(n, "group", "") or None,
                        requires_group=_require_str(n, "requires_group", "") or None,
                        requires_nodes=[
                            str(x) for x in _require_list(n, "requires_nodes")
                        ],
                        is_milestone=_require_bool(n, "is_milestone", False),
                        npc=_require_str(n, "npc", "") or None,
                        trait_requirements=_require_list(n, "trait_requirements"),
                        branch_condition=_require_str(n, "branch_condition", "")
                        or None,
                        linked_phone=_require_str(n, "linked_phone", "")
                        or None,
                        guide_hint=_require_str(n, "guide_hint", ""),
                    )
                )

        # Parse groups
        groups: List[TemplateStoryGroup] = []
        for g in _require_list(sa_raw, "groups"):
            if isinstance(g, dict):
                groups.append(
                    TemplateStoryGroup(
                        id=_require_str(g, "id"),
                        name=_require_str(g, "name"),
                        description=_require_str(g, "description", ""),
                        required_count=_require_int(g, "required_count", 1),
                    )
                )

        # Parse emotion_mappings
        emotion_mappings: Dict[str, TemplateEmotionMapping] = {}
        em_raw = _require_dict(sa_raw, "emotion_mappings")
        for trait_name, mapping in em_raw.items():
            if isinstance(mapping, dict):
                ranges: List[TemplateEmotionRange] = []
                for r in _require_list(mapping, "ranges"):
                    if isinstance(r, dict):
                        ranges.append(
                            TemplateEmotionRange(
                                min=_require_int(r, "min", 0),
                                max=_require_int(r, "max", 100),
                                label=_require_str(r, "label", "neutral"),
                                description=_require_str(r, "description", ""),
                            )
                        )
                emotion_mappings[trait_name] = TemplateEmotionMapping(
                    trait_owner=_require_str(mapping, "trait_owner", "npc"),
                    default_npc=_require_str(mapping, "default_npc", "") or None,
                    ranges=ranges,
                )

        # Parse hints
        hints_obj: Optional[TemplateStoryHints] = None
        hints_raw = sa_raw.get("hints")
        if isinstance(hints_raw, dict):
            hint_templates: List[TemplateHintTemplate] = []
            for ht in _require_list(hints_raw, "templates"):
                if isinstance(ht, dict):
                    cond_raw = ht.get("condition")
                    cond_obj = None
                    if isinstance(cond_raw, dict):
                        cond_obj = TemplateHintCondition(
                            missing_flag=_require_str(cond_raw, "missing_flag", "")
                            or None,
                            missing_trait=_require_str(cond_raw, "missing_trait", "")
                            or None,
                            gap_gte=_require_int(cond_raw, "gap_gte", 0) or None,
                        )
                    hint_templates.append(
                        TemplateHintTemplate(
                            condition=cond_obj,
                            text=_require_str(ht, "text", ""),
                        )
                    )
            hints_obj = TemplateStoryHints(
                stuck_threshold_minutes=_require_int(
                    hints_raw, "stuck_threshold_minutes", 30
                ),
                hint_style=_require_str(hints_raw, "hint_style", "observation"),
                templates=hint_templates,
            )

        story_arc_obj = TemplateStoryArc(
            version=_require_str(sa_raw, "version", "1.0"),
            chapters=chapters,
            nodes=story_nodes,
            groups=groups,
            emotion_mappings=emotion_mappings,
            hints=hints_obj,
        )

    # ── Settings & Clothing ──
    settings_raw = data.get("settings", {}) or {}
    clothing_enabled = _require_bool(settings_raw, "clothing_enabled", False)
    wardrobe_location = _require_str(settings_raw, "wardrobe_location", "")
    shop_location = _require_str(settings_raw, "shop_location", "")
    clothing_items: List[TemplateClothingItem] = []
    if clothing_enabled:
        for ci, c_raw in enumerate(data.get("clothing", []) or []):
            if not isinstance(c_raw, dict):
                continue
            clothing_items.append(
                TemplateClothingItem(
                    id=_require_str(c_raw, "id"),
                    name=_require_str(c_raw, "name"),
                    slot=_require_str(c_raw, "slot"),
                    image=_require_str(c_raw, "image", ""),
                    initial=_require_bool(c_raw, "initial", False),
                    conditions=_require_dict(c_raw, "conditions"),
                    price=int(c_raw.get("price", 0)),
                )
            )

    # Parse clothing requirements
    clothing_requirements_obj = None
    req_raw = settings_raw.get("clothing_requirements", {}) or {}
    if req_raw and clothing_enabled:
        conditional = {}
        for slot_name, slot_cfg in (req_raw.get("conditional", {}) or {}).items():
            if isinstance(slot_cfg, dict):
                conditional[slot_name] = {
                    "until_flag": slot_cfg.get("until_flag", ""),
                    "message": slot_cfg.get("message", ""),
                }
        clothing_requirements_obj = TemplateClothingRequirements(
            body_coverage=req_raw.get("body_coverage", True),
            always_required=req_raw.get("always_required", []),
            conditional=conditional,
        )

    # ── Sidebar items ──
    sidebar_items = data.get("sidebar_items", []) or []

    # ── Passes (recurring time-limited purchases) ──
    passes_raw = data.get("passes", []) or []
    passes: List[TemplatePass] = []
    for pi, p in enumerate(passes_raw):
        if not isinstance(p, dict):
            continue
        passes.append(
            TemplatePass(
                id=_require_str(p, "id"),
                name=_require_str(p, "name", ""),
                cost=_require_int(p, "cost", 0),
                duration_days=_require_int(p, "duration_days", 30),
                icon=_require_str(p, "icon", ""),
            )
        )

    # ── Items (consumable inventory) ──
    items_raw = data.get("items", []) or []
    items: List[TemplateItem] = []
    for ii, item_def in enumerate(items_raw):
        if not isinstance(item_def, dict):
            continue
        items.append(
            TemplateItem(
                id=_require_str(item_def, "id"),
                name=_require_str(item_def, "name", ""),
                icon=_require_str(item_def, "icon", ""),
                max_stack=_require_int(item_def, "max_stack", 99),
            )
        )

    # ── Theme ──
    theme_obj: Optional[TemplateTheme] = None
    theme_raw = data.get("theme")
    if isinstance(theme_raw, dict):
        mode = _require_str(theme_raw, "mode", "light")
        if mode not in ("dark", "light"):
            mode = "light"
        theme_obj = TemplateTheme(
            mode=mode,
            primary=_require_str(theme_raw, "primary", TemplateTheme.primary),
            secondary=_require_str(theme_raw, "secondary", TemplateTheme.secondary),
            accent=_require_str(theme_raw, "accent", TemplateTheme.accent),
            success=_require_str(theme_raw, "success", TemplateTheme.success),
            danger=_require_str(theme_raw, "danger", TemplateTheme.danger),
            warning=_require_str(theme_raw, "warning", TemplateTheme.warning),
            font_heading=_require_str(theme_raw, "font_heading", TemplateTheme.font_heading),
            font_mono=_require_str(theme_raw, "font_mono", TemplateTheme.font_mono),
            border_radius=_require_str(theme_raw, "border_radius", TemplateTheme.border_radius),
            bg=_require_str(theme_raw, "bg", ""),
            surface=_require_str(theme_raw, "surface", ""),
            surface_alt=_require_str(theme_raw, "surface_alt", ""),
            border=_require_str(theme_raw, "border", ""),
            text=_require_str(theme_raw, "text", ""),
            text_muted=_require_str(theme_raw, "text_muted", ""),
            custom_css=_require_str(theme_raw, "custom_css", ""),
        )

    # ── Rent system ──
    rent_raw = settings_raw.get("rent", {}) or {}
    rent_enabled = _require_bool(rent_raw, "enabled", False)
    rent_amount = _require_int(rent_raw, "amount", 0)
    rent_due_day = _require_str(rent_raw, "due_day", "Monday")
    rent_collector_npc = _require_str(rent_raw, "collector_npc", "")
    rent_grace_periods = _require_int(rent_raw, "grace_periods", 1)
    rent_start_after_flag = _require_str(rent_raw, "start_after_flag", "")
    rent_text = rent_raw.get("text", {}) or {}
    rent_eviction_mode = _require_str(rent_raw, "eviction_mode", "game_end")
    rent_eviction_flag = _require_str(rent_raw, "eviction_flag", "rent_evicted")

    # ── Phone system ──
    phone_raw = data.get("phone")
    phone_enabled = False
    phone_obj = None
    if isinstance(phone_raw, dict):
        phone_enabled = _require_bool(phone_raw, "enabled", True)
        if phone_enabled:
            phone_apps: List[TemplatePhoneApp] = []
            for ai, a_raw in enumerate(phone_raw.get("apps") or []):
                if not isinstance(a_raw, dict):
                    continue
                phone_apps.append(TemplatePhoneApp(
                    id=_require_str(a_raw, "id"),
                    type=_require_str(a_raw, "type", "chat"),
                    label=_require_str(a_raw, "label", ""),
                    icon=_require_str(a_raw, "icon", ""),
                ))

            phone_conversations: List[TemplatePhoneConversation] = []
            for ci, c_raw in enumerate(phone_raw.get("conversations") or []):
                if not isinstance(c_raw, dict):
                    continue
                trigger_cond = c_raw.get("trigger", {}) or {}
                conv_blocks: List[TemplatePhoneConversationBlock] = []
                for bi, b_raw in enumerate(c_raw.get("blocks") or []):
                    if not isinstance(b_raw, dict):
                        continue
                    block_choices = []
                    if _require_str(b_raw, "type", "message") == "reply":
                        block_choices = list(b_raw.get("choices") or [])
                    conv_blocks.append(TemplatePhoneConversationBlock(
                        type=_require_str(b_raw, "type", "message"),
                        sender=_require_str(b_raw, "sender", ""),
                        content=_require_str(b_raw, "content", ""),
                        after_reply=bool(b_raw.get("after_reply", False)),
                        choices=block_choices,
                        round=b_raw.get("round"),
                        after_round=b_raw.get("after_round"),
                        after_choice=b_raw.get("after_choice"),
                    ))
                phone_conversations.append(TemplatePhoneConversation(
                    id=_require_str(c_raw, "id"),
                    app=_require_str(c_raw, "app", "messages"),
                    npc=_require_str(c_raw, "npc", ""),
                    trigger=trigger_cond,
                    blocks=conv_blocks,
                ))

            # Parse posts (social feed)
            phone_posts: List[TemplatePhonePost] = []
            for pi, p_raw in enumerate(phone_raw.get("posts") or []):
                if not isinstance(p_raw, dict):
                    continue
                phone_posts.append(TemplatePhonePost(
                    id=_require_str(p_raw, "id"),
                    app=_require_str(p_raw, "app", ""),
                    npc=_require_str(p_raw, "npc", ""),
                    poster_name=_require_str(p_raw, "poster_name", ""),
                    image=_require_str(p_raw, "image", ""),
                    caption=_require_str(p_raw, "caption", ""),
                    likes=_require_int(p_raw, "likes", 0),
                    trigger=p_raw.get("trigger", {}) or {},
                    search_queries=[str(q) for q in _require_list(p_raw, "search_queries")],
                ))

            # Parse profiles (dating app)
            phone_profiles: List[TemplatePhoneProfile] = []
            for pi, p_raw in enumerate(phone_raw.get("profiles") or []):
                if not isinstance(p_raw, dict):
                    continue
                phone_profiles.append(TemplatePhoneProfile(
                    id=_require_str(p_raw, "id"),
                    app=_require_str(p_raw, "app", ""),
                    npc=_require_str(p_raw, "npc", ""),
                    photos=[str(p) for p in (p_raw.get("photos") or [])],
                    bio=_require_str(p_raw, "bio", ""),
                    age=_require_str(p_raw, "age", ""),
                    interests=[str(i) for i in (p_raw.get("interests") or [])],
                    trigger=p_raw.get("trigger", {}) or {},
                    match_condition=p_raw.get("match_condition", {}) or {},
                    search_queries=[str(q) for q in _require_list(p_raw, "search_queries")],
                ))

            phone_daily_topics: List[TemplatePhoneDailyTopic] = []
            for dti, dt_raw in enumerate(phone_raw.get("daily_topics") or []):
                if not isinstance(dt_raw, dict):
                    continue
                phone_daily_topics.append(TemplatePhoneDailyTopic(
                    id=_require_str(dt_raw, "id"),
                    npc=_require_str(dt_raw, "npc", ""),
                    player_message=_require_str(dt_raw, "player_message", ""),
                    npc_response=_require_str(dt_raw, "npc_response", ""),
                    effects=dt_raw.get("effects", []) or [],
                    conditions=dt_raw.get("conditions", {}) or {},
                ))

            phone_obj = TemplatePhone(
                enabled=phone_enabled,
                apps=phone_apps,
                conversations=phone_conversations,
                posts=phone_posts,
                profiles=phone_profiles,
                daily_topics=phone_daily_topics,
            )

    # ── Day-rollover hook ── [engine.daily_tick]
    daily_tick_obj: Optional[TemplateDailyTick] = None
    # ── Stage helpers ── [[engine.stage_helpers]]
    stage_helpers: List[TemplateStageHelper] = []
    engine_raw = data.get("engine")
    if isinstance(engine_raw, dict):
        dt_raw = engine_raw.get("daily_tick")
        if isinstance(dt_raw, dict):
            dt_flag_effs: List[TemplateFlagEffect] = []
            for fe in dt_raw.get("flagEffects") or []:
                if not isinstance(fe, dict):
                    continue
                dt_flag_effs.append(
                    TemplateFlagEffect(
                        targetType=str(fe.get("targetType", "player")),
                        npcId=_require_str(fe, "npcId", "") or None,
                        flag=_require_str(fe, "flag", ""),
                        op=_require_str(fe, "op", "set") or "set",
                    )
                )
            daily_tick_obj = TemplateDailyTick(flagEffects=dt_flag_effs)
        for sh_raw in engine_raw.get("stage_helpers") or []:
            if not isinstance(sh_raw, dict):
                continue
            stage_helpers.append(
                TemplateStageHelper(
                    name=_require_str(sh_raw, "name", ""),
                    description=_require_str(sh_raw, "description", ""),
                    conditions=_require_dict(sh_raw, "conditions"),
                )
            )

    return GameTemplate(
        schema_version=schema_version,
        project=project,
        time=time,
        player=player,
        npcs=npcs,
        locations=locations,
        starting_canvas=starting_canvas,
        canvases=canvases,
        story_arc=story_arc_obj,
        clothing_enabled=clothing_enabled,
        clothing_items=clothing_items,
        wardrobe_location=wardrobe_location or None,
        shop_location=shop_location or None,
        clothing_requirements=clothing_requirements_obj,
        rent_enabled=rent_enabled,
        rent_amount=rent_amount,
        rent_due_day=rent_due_day,
        rent_collector_npc=rent_collector_npc or None,
        rent_grace_periods=rent_grace_periods,
        rent_start_after_flag=rent_start_after_flag,
        rent_text=rent_text,
        rent_eviction_mode=rent_eviction_mode,
        rent_eviction_flag=rent_eviction_flag,
        sidebar_items=sidebar_items,
        phone_enabled=phone_enabled,
        phone=phone_obj,
        passes=passes,
        items=items,
        theme=theme_obj,
        daily_tick=daily_tick_obj,
        stage_helpers=stage_helpers,
    )


# -------- Validation --------


VALID_DAYS = {
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
}


def _is_valid_slug(s: str) -> bool:
    if not s:
        return False
    for ch in s:
        if ch.islower() and ch.isalpha():
            continue
        if ch.isdigit() or ch == "_":
            continue
        return False
    return True


def _extract_flags_required_by_canvas(canvas: TemplateCanvas) -> Set[str]:
    """Extract flag keys required by a canvas's trigger conditions."""
    required_flags: Set[str] = set()
    if not canvas.trigger or not canvas.trigger.conditions:
        return required_flags

    items = canvas.trigger.conditions.get("items", [])
    for item in items:
        if isinstance(item, dict) and item.get("type") == "flag":
            flag_key = item.get("flag_key", "")
            if flag_key:
                required_flags.add(flag_key)
    return required_flags


def _extract_flags_set_by_canvas(canvas: TemplateCanvas) -> Set[str]:
    """Extract all flags set by a canvas (from any node's exit_block)."""
    set_flags: Set[str] = set()
    for node in canvas.nodes:
        eb = node.exit_block
        if not eb:
            continue

        # Location type: flags in config.flagEffects and config.effects
        if eb.type == "location":
            for fe in eb.config.get("flagEffects") or []:
                if isinstance(fe, dict) and fe.get("flag"):
                    set_flags.add(fe["flag"])
            # Also check effects array for flag-like objects
            for eff in eb.config.get("effects") or []:
                if isinstance(eff, dict) and eff.get("flag"):
                    set_flags.add(eff["flag"])

        # Choices type: flags in each choice's flagEffects and effects
        elif eb.type == "choices":
            for choice in eb.choices:
                # Check flagEffects (typed as TemplateFlagEffect)
                for fe in choice.flagEffects:
                    if fe.flag:
                        set_flags.add(fe.flag)
                # Also check effects array for flag-like objects (stored as dicts or TemplateChoiceEffect)
                for eff in choice.effects:
                    # Could be TemplateChoiceEffect or raw dict
                    if hasattr(eff, "flag") and eff.flag:
                        set_flags.add(eff.flag)
                    elif isinstance(eff, dict) and eff.get("flag"):
                        set_flags.add(eff["flag"])

    return set_flags


def validate(template: GameTemplate) -> List[str]:
    errors: List[str] = []

    # project
    if not template.project.title:
        errors.append("project.title is required")
    if not _is_valid_slug(template.project.slug):
        errors.append("project.id must be lowercase snake_case (^[a-z0-9_]+$)")

    # time
    if template.time.starting_day not in VALID_DAYS:
        errors.append("time.starting_day must be one of Monday..Sunday")
    if not (0 <= template.time.starting_hour <= 23):
        errors.append("time.starting_hour must be 0..23")
    if template.time.starting_week < 1:
        errors.append("time.starting_week must be >= 1")

    # player
    if not _is_valid_slug(template.player.id):
        errors.append("player.id must be lowercase snake_case")

    # Player customization validation
    if template.player.customizable:
        if not template.player.customization_fields:
            errors.append("player is customizable but has no customization_fields")
        reserved_ids = {"portrait", "current_location", "core_traits", "flags", "wardrobe", "equipped"}
        seen_field_ids: Set[str] = set()
        for fi, cf in enumerate(template.player.customization_fields):
            ctx = f"player.customization_fields[{fi}]"
            if not cf.id:
                errors.append(f"{ctx}.id is required")
            elif not _is_valid_slug(cf.id):
                errors.append(f"{ctx}.id must be lowercase snake_case")
            if cf.id in seen_field_ids:
                errors.append(f"player.customization_fields: duplicate id '{cf.id}'")
            seen_field_ids.add(cf.id)
            if cf.id in reserved_ids:
                errors.append(f"{ctx}.id '{cf.id}' is a reserved $player property")
            if cf.type not in ("text", "select", "image_select"):
                errors.append(f"{ctx}.type must be text/select/image_select, got '{cf.type}'")
            if cf.type == "select":
                if not cf.options:
                    errors.append(f"{ctx} type=select requires options list")
                elif cf.default and cf.default not in cf.options:
                    errors.append(f"{ctx} default '{cf.default}' not in options")
            if cf.type == "image_select":
                if not cf.options:
                    errors.append(f"{ctx} type=image_select requires options list")
                else:
                    option_ids = [o.id for o in cf.options]
                    if cf.default and cf.default not in option_ids:
                        errors.append(f"{ctx} default '{cf.default}' not in option ids {option_ids}")
                    for oi, opt in enumerate(cf.options):
                        if not opt.id:
                            errors.append(f"{ctx}.options[{oi}].id is required")
                        if not opt.image:
                            errors.append(f"{ctx}.options[{oi}].image is required")
            if cf.sets_portrait and cf.type != "image_select":
                errors.append(f"{ctx} sets_portrait only valid for image_select type")

    # npcs
    seen_npc_ids: Set[str] = set()
    for i, n in enumerate(template.npcs):
        if not _is_valid_slug(n.id):
            errors.append(f"npcs[{i}].id must be lowercase snake_case")
        if not n.name:
            errors.append(f"npcs[{i}].name is required")
        if n.id in seen_npc_ids:
            errors.append(f"duplicate npc id: {n.id}")
        seen_npc_ids.add(n.id)
        # NPC schedules are deprecated — NPC presence is derived from canvas triggers at runtime.
        # We still parse them for backward compatibility but warn about their presence.
        # (Validation of schedule fields kept for backward compat, but soft-deprecated)
        if n.schedules:
            import warnings
            warnings.warn(
                f"npcs[{i}] '{n.id}' has [[npcs.schedules]] defined. "
                f"NPC schedules are deprecated — NPC presence is derived from canvas triggers at runtime. "
                f"Consider removing [[npcs.schedules]] sections.",
                DeprecationWarning,
                stacklevel=2,
            )
        for si, sch in enumerate(n.schedules):
            # Validate weekdays (0-6)
            for w in sch.weekdays:
                if not isinstance(w, int) or w < 0 or w > 6:
                    errors.append(
                        f"npcs[{i}].schedules[{si}].weekdays must be integers 0..6"
                    )
            # Validate start_time format (HH:MM)
            if not sch.start_time or ":" not in sch.start_time:
                errors.append(
                    f"npcs[{i}].schedules[{si}].start_time must be HH:MM format"
                )
            # Validate end_time format if present
            if sch.end_time and ":" not in sch.end_time:
                errors.append(
                    f"npcs[{i}].schedules[{si}].end_time must be HH:MM format or omitted"
                )
            # Location validation will be done after loc_index is built

    # NPC trait_decay validation
    for i, n in enumerate(template.npcs):
        if n.trait_decay:
            for trait_name, decay_val in n.trait_decay.items():
                if trait_name not in (n.core_traits or {}):
                    errors.append(
                        f"npcs[{i}] '{n.id}' trait_decay key '{trait_name}' "
                        f"not found in core_traits"
                    )
                if decay_val < 0:
                    errors.append(
                        f"npcs[{i}] '{n.id}' trait_decay['{trait_name}'] must be >= 0, "
                        f"got {decay_val}"
                    )

    # Player trait_decay validation
    if template.player.trait_decay:
        for trait_name, decay_val in template.player.trait_decay.items():
            if trait_name not in (template.player.core_traits or {}):
                errors.append(
                    f"player.trait_decay key '{trait_name}' not found in core_traits"
                )
            if decay_val < 0:
                errors.append(
                    f"player.trait_decay['{trait_name}'] must be >= 0, got {decay_val}"
                )

    # ===== arc_stages validation =====
    # Foundation for E9 (stalled detection), E10 (stage_gate), E11 (stage_label).
    # Stage trait lives in $player.core_traits[<slug>_stage] as an integer.
    # If that trait appears in player.trait_decay, decay would silently move
    # the value downward without going through applyAndNotifyTrait — which is
    # where E9 hooks the advancement log. So we reject the combination.
    for i, n in enumerate(template.npcs):
        if not n.arc_stages:
            continue
        # Element typing already enforced in normalize() but double-check len.
        if len(n.arc_stages) < 1:
            errors.append(
                f"npcs[{i}] '{n.id}' arc_stages must have at least one stage name "
                f"(or omit the field entirely)"
            )
        # Reject the trait-decay collision that would break E9.
        stage_trait = f"{n.id}_stage"
        if template.player.trait_decay and stage_trait in template.player.trait_decay:
            errors.append(
                f"npcs[{i}] '{n.id}' declares arc_stages but player.trait_decay "
                f"includes '{stage_trait}' — stage traits must not decay (decay "
                f"bypasses applyAndNotifyTrait, which would silently break "
                f"stage-advancement detection)"
            )

    # Sidebar items validation (per-type; only trait_words is typed-validated today)
    _npc_ids_for_sidebar = {n.id for n in template.npcs}
    _player_trait_keys = set((template.player.core_traits or {}).keys())
    for i, item in enumerate(template.sidebar_items or []):
        if not isinstance(item, dict):
            errors.append(f"sidebar_items[{i}] must be a table/dict")
            continue
        itype = item.get("type")
        if itype == "trait_words":
            ctx = f"sidebar_items[{i}] (trait_words)"
            trait = item.get("trait")
            owner = item.get("trait_owner", "player")
            bands = item.get("bands")
            if not isinstance(trait, str) or not trait:
                errors.append(f"{ctx}: 'trait' is required (string)")
            if owner not in ("player", "npc"):
                errors.append(f"{ctx}: 'trait_owner' must be 'player' or 'npc', got '{owner}'")
            if owner == "npc":
                npc_id = item.get("npc_id")
                if not npc_id:
                    errors.append(f"{ctx}: 'npc_id' is required when trait_owner='npc'")
                elif npc_id not in _npc_ids_for_sidebar:
                    errors.append(f"{ctx}: npc_id '{npc_id}' not found in NPC definitions")
            elif owner == "player" and isinstance(trait, str) and trait and trait not in _player_trait_keys:
                # Warn-style error: surface as soft issue but still an error so authors see it
                errors.append(
                    f"{ctx}: trait '{trait}' not found in player.core_traits (widget will render empty)"
                )
            if not isinstance(bands, list) or not bands:
                errors.append(f"{ctx}: 'bands' must be a non-empty list")
            else:
                for bi, band in enumerate(bands):
                    bctx = f"{ctx} bands[{bi}]"
                    if not isinstance(band, dict):
                        errors.append(f"{bctx}: must be a table/dict")
                        continue
                    if "text" not in band:
                        errors.append(f"{bctx}: missing 'text'")
                    # A band matches either by flag (flag-driven, for narrative
                    # milestones) or by min/max (trait-value range). Require one
                    # of the two modes but not both.
                    has_flag = "flag" in band
                    has_range = ("min" in band) or ("max" in band)
                    if has_flag and has_range:
                        errors.append(f"{bctx}: cannot combine 'flag' with 'min'/'max' in the same band")
                    elif not has_flag and not has_range:
                        errors.append(f"{bctx}: must provide either 'flag' or both 'min' and 'max'")
                    elif has_range:
                        if "min" not in band:
                            errors.append(f"{bctx}: missing 'min'")
                        if "max" not in band:
                            errors.append(f"{bctx}: missing 'max'")
                        bmin, bmax = band.get("min"), band.get("max")
                        if isinstance(bmin, (int, float)) and isinstance(bmax, (int, float)) and bmin > bmax:
                            errors.append(f"{bctx}: min ({bmin}) must be <= max ({bmax})")
                    elif has_flag and not isinstance(band.get("flag"), str):
                        errors.append(f"{bctx}: 'flag' must be a string")
                    if "text" in band and not isinstance(band["text"], str):
                        errors.append(f"{bctx}: 'text' must be a string")
        elif itype == "stage_label":
            # E11: render "<NPC name>: <stage label>" from the NPC's arc_stages
            # array indexed by $player.core_traits[<slug>_stage]. Distinct from
            # trait_words because the label source is the per-NPC stage chain,
            # not a trait-value band — overloading trait_words would force the
            # bands validator into special-case branches.
            ctx = f"sidebar_items[{i}] (stage_label)"
            sl_npc_id = item.get("npc_id")
            if not sl_npc_id:
                errors.append(f"{ctx}: 'npc_id' is required")
            elif sl_npc_id not in _npc_ids_for_sidebar:
                errors.append(f"{ctx}: npc_id '{sl_npc_id}' not found in NPC definitions")
            else:
                sl_npc = next((n for n in template.npcs if n.id == sl_npc_id), None)
                if sl_npc is None or not sl_npc.arc_stages:
                    errors.append(
                        f"{ctx}: NPC '{sl_npc_id}' has no arc_stages defined "
                        f"(declare arc_stages on the NPC before using stage_label)"
                    )
            if "prefix" in item and not isinstance(item.get("prefix"), str):
                errors.append(f"{ctx}: 'prefix' must be a string when set")

    # locations
    loc_ids = [l.id for l in template.locations]
    if len(set(loc_ids)) != len(loc_ids):
        errors.append("duplicate location ids found")
    for i, lid in enumerate(loc_ids):
        if not _is_valid_slug(lid):
            errors.append(f"locations[{i}].id must be lowercase snake_case")

    # reference existence
    loc_index = {l.id: l for l in template.locations}
    for l in template.locations:
        if l.parent and l.parent not in loc_index:
            errors.append(f"location '{l.id}' parent '{l.parent}' not found")
        if l.entry_from and l.entry_from not in loc_index:
            errors.append(f"location '{l.id}' entry_from '{l.entry_from}' not found")
        if l.default_entry and l.default_entry not in loc_index:
            errors.append(
                f"location '{l.id}' default_entry '{l.default_entry}' not found"
            )

    # NPC schedule location validation (now that loc_index is built)
    for i, n in enumerate(template.npcs):
        for si, sch in enumerate(n.schedules):
            if sch.location and sch.location not in loc_index:
                errors.append(
                    f"npcs[{i}].schedules[{si}].location '{sch.location}' not found in locations"
                )

    # Customizable NPC validation
    for i, n in enumerate(template.npcs):
        if n.customizable:
            if not n.relationship:
                errors.append(
                    f"npcs[{i}] '{n.id}' is customizable but has no default relationship"
                )
            if not n.relationship_options:
                errors.append(
                    f"npcs[{i}] '{n.id}' is customizable but has no relationship_options"
                )
            elif n.relationship and n.relationship not in n.relationship_options:
                errors.append(
                    f"npcs[{i}] '{n.id}' default relationship '{n.relationship}' "
                    f"not in relationship_options {n.relationship_options}"
                )

    # Phone system validation
    if template.phone_enabled and template.phone:
        phone = template.phone
        seen_app_ids: Set[str] = set()
        chat_app_ids: Set[str] = set()
        for ai, app in enumerate(phone.apps):
            ctx = f"phone.apps[{ai}]"
            if not app.id:
                errors.append(f"{ctx}.id is required")
            elif not _is_valid_slug(app.id):
                errors.append(f"{ctx}.id must be lowercase snake_case")
            if app.id in seen_app_ids:
                errors.append(f"phone.apps: duplicate id '{app.id}'")
            seen_app_ids.add(app.id)
            if app.type not in VALID_PHONE_APP_TYPES:
                errors.append(f"{ctx}.type must be one of {VALID_PHONE_APP_TYPES}, got '{app.type}'")
            if app.type == "chat":
                chat_app_ids.add(app.id)
            if not app.label:
                errors.append(f"{ctx}.label is required")

        feed_app_ids = {a.id for a in phone.apps if a.type == "social_feed"}
        dating_app_ids = {a.id for a in phone.apps if a.type == "dating"}

        # Post validation
        for pi, post in enumerate(phone.posts):
            ctx = f"phone.posts[{pi}]"
            if not post.id:
                errors.append(f"{ctx}.id is required")
            if post.app not in feed_app_ids:
                errors.append(f"{ctx}.app '{post.app}' not found in social_feed apps")
            if post.npc and post.npc not in {n.id for n in template.npcs}:
                errors.append(f"{ctx}.npc '{post.npc}' not found in npcs")

        # Profile validation
        for pi, prof in enumerate(phone.profiles):
            ctx = f"phone.profiles[{pi}]"
            if not prof.id:
                errors.append(f"{ctx}.id is required")
            if prof.app not in dating_app_ids:
                errors.append(f"{ctx}.app '{prof.app}' not found in dating apps")
            if prof.npc and prof.npc not in {n.id for n in template.npcs}:
                errors.append(f"{ctx}.npc '{prof.npc}' not found in npcs")
            if not prof.bio:
                errors.append(f"{ctx}.bio is required")

        seen_conv_ids: Set[str] = set()
        npc_id_set = {n.id for n in template.npcs}
        for ci, conv in enumerate(phone.conversations):
            ctx = f"phone.conversations[{ci}]"
            if not conv.id:
                errors.append(f"{ctx}.id is required")
            elif not _is_valid_slug(conv.id):
                errors.append(f"{ctx}.id must be lowercase snake_case")
            if conv.id in seen_conv_ids:
                errors.append(f"phone.conversations: duplicate id '{conv.id}'")
            seen_conv_ids.add(conv.id)
            if conv.app not in chat_app_ids:
                errors.append(f"{ctx}.app '{conv.app}' not found in phone chat apps")
            if conv.npc and conv.npc not in npc_id_set:
                errors.append(f"{ctx}.npc '{conv.npc}' not found in npcs")
            for bi, block in enumerate(conv.blocks):
                bctx = f"{ctx}.blocks[{bi}]"
                if block.type not in ("message", "reply"):
                    errors.append(f"{bctx}.type must be 'message' or 'reply'")
                if block.type == "message" and not block.content:
                    errors.append(f"{bctx} is a message but has no content")
                if block.type == "message" and block.sender not in ("npc", "player"):
                    errors.append(f"{bctx}.sender must be 'npc' or 'player'")
                if block.type == "reply" and not block.choices:
                    errors.append(f"{bctx} is a reply but has no choices")

    # container/default entry rules
    for l in template.locations:
        if l.is_container and l.default_entry:
            de = loc_index.get(l.default_entry)
            if not de:
                continue
            if de.parent != l.id:
                errors.append(
                    f"default_entry '{de.id}' must be a child of container '{l.id}'"
                )
            if de.entry_from:
                errors.append(
                    f"default_entry '{de.id}' must not define entry_from (automatic container entry)"
                )

    # descendants using container with default_entry as entry_from
    # build parent chains
    def ancestors(x: TemplateLocation) -> Set[str]:
        s: Set[str] = set()
        cur = x
        guard = 0
        while cur.parent and cur.parent in loc_index and guard < 100:
            s.add(cur.parent)
            cur = loc_index[cur.parent]
            guard += 1
        return s

    containers_with_default = {
        l.id for l in template.locations if l.is_container and l.default_entry
    }
    for l in template.locations:
        if not l.entry_from:
            continue
        # If this location is a descendant of a container with default_entry, it cannot set entry_from to that container
        for c in containers_with_default:
            if c in ancestors(l) and l.entry_from == c:
                errors.append(
                    f"location '{l.id}' cannot set entry_from to its ancestor container '{c}' that has a default_entry"
                )

    # entry_from cycle detection
    # directed edges: entry_from -> location
    graph: Dict[str, List[str]] = {}
    for l in template.locations:
        if l.entry_from:
            graph.setdefault(l.entry_from, []).append(l.id)
    # detect cycles via DFS
    visiting: Set[str] = set()
    visited: Set[str] = set()

    def dfs(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        for nb in graph.get(node, []):
            if dfs(nb):
                return True
        visiting.remove(node)
        visited.add(node)
        return False

    for start in list(graph.keys()):
        if dfs(start):
            errors.append("cycle detected in entry_from graph")
            break

    # navigation_order correctness
    for l in template.locations:
        if not l.navigation_order:
            continue
        # Destinations are locations where entry_from == this
        dests = {x.id for x in template.locations if x.entry_from == l.id}
        for slug in l.navigation_order:
            if slug not in dests:
                errors.append(
                    f"navigation_order for '{l.id}' includes '{slug}' which is not a destination (entry_from != '{l.id}')"
                )

    # ===== Clothing rules validation (per-location) =====
    for l in template.locations:
        for ri, rule in enumerate(l.clothing_rules):
            if not isinstance(rule, dict):
                errors.append(f"location '{l.id}' clothing_rules[{ri}] must be a dict")
                continue
            slots = rule.get("slots_required", [])
            if not isinstance(slots, list) or not slots:
                errors.append(f"location '{l.id}' clothing_rules[{ri}] missing slots_required")
            else:
                for s in slots:
                    if s not in VALID_CLOTHING_SLOTS:
                        errors.append(
                            f"location '{l.id}' clothing_rules[{ri}] invalid slot '{s}', must be one of {sorted(VALID_CLOTHING_SLOTS)}"
                        )

    # ===== Story validation (optional) =====
    canvas_ids = {c.id for c in getattr(template, "canvases", [])}
    if template.starting_canvas and template.starting_canvas not in canvas_ids:
        errors.append(
            f"starting_canvas '{template.starting_canvas}' not found in canvases"
        )

    loc_index = {l.id: l for l in template.locations}

    for ci, c in enumerate(getattr(template, "canvases", [])):
        if not _is_valid_slug(c.id):
            errors.append(f"canvases[{ci}].id must be lowercase snake_case")
        if not c.name:
            errors.append(f"canvases[{ci}].name is required")

        # Trigger
        if c.trigger:
            # Location is optional for story canvases (they fire on day/flag conditions)
            if c.trigger.location and c.trigger.location not in loc_index:
                errors.append(f"canvases[{ci}].trigger.location not found in locations")
            for si, s in enumerate(c.trigger.schedules):
                for w in s.weekdays:
                    if not isinstance(w, int) or w < 0 or w > 6:
                        errors.append(
                            f"canvases[{ci}].trigger.schedules[{si}].weekdays must be integers 0..6"
                        )
                if not isinstance(s.start_time, str) or ":" not in s.start_time:
                    errors.append(
                        f"canvases[{ci}].trigger.schedules[{si}].start_time must be HH:MM"
                    )
                if s.end_time and (
                    not isinstance(s.end_time, str) or ":" not in s.end_time
                ):
                    errors.append(
                        f"canvases[{ci}].trigger.schedules[{si}].end_time must be HH:MM or omitted"
                    )

        # Node IDs unique per canvas
        seen_node_ids: Set[str] = set()
        for ni, n in enumerate(c.nodes):
            if not _is_valid_slug(n.id):
                errors.append(
                    f"canvases[{ci}].nodes[{ni}].id must be lowercase snake_case"
                )
            if n.id in seen_node_ids:
                errors.append(f"duplicate node id in canvas '{c.id}': {n.id}")
            seen_node_ids.add(n.id)
            if not n.name:
                errors.append(f"canvases[{ci}].nodes[{ni}].name is required")

            eb = n.exit_block
            if eb.type not in ("location", "choices", "game_end"):
                errors.append(
                    f"canvases[{ci}].nodes[{ni}].exit_block.type must be 'location', 'choices', or 'game_end'"
                )

            if eb.type == "location":
                dest = eb.config.get("destinationType", "trigger")
                if dest not in ("trigger", "specific", "node"):
                    errors.append(
                        f"canvases[{ci}].nodes[{ni}].exit_block.config.destinationType must be 'trigger', 'specific', or 'node'"
                    )
                if dest == "specific":
                    loc_slug = eb.config.get("locationId")
                    if not loc_slug or loc_slug not in loc_index:
                        errors.append(
                            f"canvases[{ci}].nodes[{ni}].exit_block.config.locationId not found in locations"
                        )
            else:
                for chi, ch in enumerate(eb.choices):
                    if ch.targetType not in ("trigger", "location", "node"):
                        errors.append(
                            f"canvases[{ci}].nodes[{ni}].choices[{chi}].targetType invalid"
                        )
                    if ch.targetType == "location":
                        if not ch.locationId or ch.locationId not in loc_index:
                            errors.append(
                                f"canvases[{ci}].nodes[{ni}].choices[{chi}].locationId not found"
                            )
                    if ch.targetType == "node" and not ch.nodeId:
                        errors.append(
                            f"canvases[{ci}].nodes[{ni}].choices[{chi}].nodeId required for targetType 'node'"
                        )
                    # Rejection node validation
                    if ch.rejection_node:
                        if ch.rejection_node not in seen_node_ids:
                            errors.append(
                                f"canvases[{ci}].nodes[{ni}].choices[{chi}].rejection_node "
                                f"'{ch.rejection_node}' not found in canvas '{c.id}'"
                            )
                        if not ch.conditions:
                            errors.append(
                                f"canvases[{ci}].nodes[{ni}].choices[{chi}] has rejection_node "
                                f"but no conditions — rejection requires conditions to gate against"
                            )

    # ===== Modifier redirect validation =====
    for ci, c in enumerate(template.canvases):
        all_node_ids = {n.id for n in c.nodes}
        for ni, n in enumerate(c.nodes):
            if n.modifier_redirect:
                mr = n.modifier_redirect
                if not mr.get("modifier_key"):
                    errors.append(
                        f"canvases[{ci}].nodes[{ni}].modifier_redirect.modifier_key is required"
                    )
                target_node = mr.get("node", "")
                if not target_node:
                    errors.append(
                        f"canvases[{ci}].nodes[{ni}].modifier_redirect.node is required"
                    )
                elif target_node not in all_node_ids:
                    errors.append(
                        f"canvases[{ci}].nodes[{ni}].modifier_redirect.node "
                        f"'{target_node}' not found in canvas '{c.id}'"
                    )

    # ===== Costs validation =====
    for c in getattr(template, "canvases", []):
        if c.trigger and c.trigger.costs:
            for cost in c.trigger.costs:
                if not cost.get("trait") or not isinstance(cost.get("value"), (int, float)):
                    errors.append(
                        f"Canvas '{c.id}' has invalid cost entry: {cost}. "
                        f"Each cost must have 'trait' (string) and 'value' (number)."
                    )
                elif cost.get("value", 0) < 0:
                    errors.append(
                        f"Canvas '{c.id}' has negative cost value for trait '{cost.get('trait')}'."
                    )

    # ===== Repeatable canvas uniqueness (one per location + NPC + schedule window) =====
    # Enforces: at a given location, for a given NPC, during overlapping time windows,
    # only ONE repeatable manual canvas is allowed. This ensures NPC portraits map 1:1
    # to canvases in the location UI.
    repeatable_npc_canvases = [
        c for c in getattr(template, "canvases", [])
        if c.trigger and c.trigger.is_repeatable
        and (c.trigger.trigger_mode or "manual") != "random"
        and c.trigger.npc  # Only NPC activities — solo activities are exempt
    ]

    def _schedules_overlap(
        sched_a_list: list, sched_b_list: list
    ) -> bool:
        """Check if two schedule lists have any overlapping time windows on shared weekdays."""
        if not sched_a_list or not sched_b_list:
            return True  # No schedule = always active = overlaps with everything
        for sa in sched_a_list:
            for sb in sched_b_list:
                # Check weekday overlap (empty = all days)
                days_a = set(sa.weekdays) if sa.weekdays else set(range(7))
                days_b = set(sb.weekdays) if sb.weekdays else set(range(7))
                if not days_a & days_b:
                    continue
                # Check time overlap
                a_start = sa.start_time or "00:00"
                a_end = sa.end_time or "23:59"
                b_start = sb.start_time or "00:00"
                b_end = sb.end_time or "23:59"
                if a_start < b_end and b_start < a_end:
                    return True
        return False

    _seen_canvas_combos: List[Tuple[str, str, str, list]] = []
    for c in repeatable_npc_canvases:
        loc = c.trigger.location or ""
        npc = c.trigger.npc or ""
        scheds = c.trigger.schedules

        for prev_id, prev_loc, prev_npc, prev_scheds in _seen_canvas_combos:
            if prev_loc == loc and prev_npc == npc and _schedules_overlap(scheds, prev_scheds):
                import warnings
                warnings.warn(
                    f"Repeatable canvases '{prev_id}' and '{c.id}' both trigger for "
                    f"NPC '{npc or '(none)'}' at location '{loc}' with overlapping schedules. "
                    f"Only one repeatable canvas is allowed per location + NPC + time window. "
                    f"Put multiple interactions inside a single canvas as choices instead.",
                    UserWarning,
                    stacklevel=2,
                )
        _seen_canvas_combos.append((c.id, loc, npc, scheds))

    # ===== Story Arc validation (v0.3 - optional) =====
    story_arc = getattr(template, "story_arc", None)
    if story_arc:
        # Collect all valid IDs for reference checking
        all_canvas_ids = {c.id for c in getattr(template, "canvases", [])}
        canvas_lookup = {c.id: c for c in getattr(template, "canvases", [])}
        all_flag_keys = set(template.player.flag_keys)
        for npc in template.npcs:
            all_flag_keys.update(npc.flag_keys)

        # Validate chapter IDs are unique
        chapter_ids: Set[str] = set()
        for i, ch in enumerate(story_arc.chapters):
            if not _is_valid_slug(ch.id):
                errors.append(
                    f"story_arc.chapters[{i}].id must be lowercase snake_case"
                )
            if ch.id in chapter_ids:
                errors.append(f"duplicate story_arc chapter id: {ch.id}")
            chapter_ids.add(ch.id)
            if not ch.name:
                errors.append(f"story_arc.chapters[{i}].name is required")

        # Validate group IDs are unique
        group_ids: Set[str] = set()
        for i, g in enumerate(story_arc.groups):
            if not _is_valid_slug(g.id):
                errors.append(f"story_arc.groups[{i}].id must be lowercase snake_case")
            if g.id in group_ids:
                errors.append(f"duplicate story_arc group id: {g.id}")
            group_ids.add(g.id)
            if not g.name:
                errors.append(f"story_arc.groups[{i}].name is required")
            if g.required_count < 1:
                errors.append(f"story_arc.groups[{i}].required_count must be >= 1")

        # Validate node IDs and references
        node_ids: Set[str] = set()
        for i, n in enumerate(story_arc.nodes):
            if not _is_valid_slug(n.id):
                errors.append(f"story_arc.nodes[{i}].id must be lowercase snake_case")
            if n.id in node_ids:
                errors.append(f"duplicate story_arc node id: {n.id}")
            node_ids.add(n.id)
            if not n.name:
                errors.append(f"story_arc.nodes[{i}].name is required")

            # Check chapter reference
            if n.chapter and n.chapter not in chapter_ids:
                errors.append(f"story_arc.nodes[{i}].chapter '{n.chapter}' not found")

            # Check linked_canvas reference
            if n.linked_canvas and n.linked_canvas not in all_canvas_ids:
                errors.append(
                    f"story_arc.nodes[{i}].linked_canvas '{n.linked_canvas}' not found"
                )

            # Story arc nodes must link to non-repeatable canvases only.
            # Repeatable activities and random encounters are gameplay, not story.
            if n.linked_canvas and n.linked_canvas in all_canvas_ids:
                target_canvas = canvas_lookup.get(n.linked_canvas)
                if target_canvas and target_canvas.trigger:
                    if target_canvas.trigger.is_repeatable:
                        errors.append(
                            f"story_arc.nodes[{i}].linked_canvas '{n.linked_canvas}' is repeatable "
                            f"(is_repeatable=true). Story arc nodes must link to non-repeatable "
                            f"canvases only. If this activity is a story milestone, create a "
                            f"separate non-repeatable canvas for that moment."
                        )
                    if (target_canvas.trigger.trigger_mode or "manual") == "random":
                        errors.append(
                            f"story_arc.nodes[{i}].linked_canvas '{n.linked_canvas}' is a random "
                            f"encounter (trigger_mode='random'). Story arc nodes must link to "
                            f"non-repeatable story event canvases only."
                        )

            # Check linked_canvas_node reference
            if n.linked_canvas_node:
                if not n.linked_canvas:
                    errors.append(
                        f"story_arc.nodes[{i}].linked_canvas_node requires linked_canvas"
                    )
                else:
                    target_canvas = next(
                        (c for c in template.canvases if c.id == n.linked_canvas), None
                    )
                    if target_canvas:
                        canvas_node_ids = {cn.id for cn in target_canvas.nodes}
                        if n.linked_canvas_node not in canvas_node_ids:
                            errors.append(
                                f"story_arc.nodes[{i}].linked_canvas_node "
                                f"'{n.linked_canvas_node}' not found in canvas "
                                f"'{n.linked_canvas}'"
                            )

            # Check linked_flag reference (warning only - flags might be set dynamically)
            # Skip strict validation as flags can be defined elsewhere

            # Check branch_condition reference (no strict validation — flags may be set dynamically)

            # Check group reference
            if n.group and n.group not in group_ids:
                errors.append(f"story_arc.nodes[{i}].group '{n.group}' not found")

            # Check requires_group reference
            if n.requires_group and n.requires_group not in group_ids:
                errors.append(
                    f"story_arc.nodes[{i}].requires_group '{n.requires_group}' not found"
                )

        # Validate requires_nodes references (second pass after all nodes collected)
        for i, n in enumerate(story_arc.nodes):
            for req_node in n.requires_nodes:
                if req_node not in node_ids:
                    errors.append(
                        f"story_arc.nodes[{i}].requires_nodes contains unknown node '{req_node}'"
                    )

        # Validate emotion_mappings
        for trait_name, mapping in story_arc.emotion_mappings.items():
            if mapping.trait_owner not in ("player", "npc"):
                errors.append(
                    f"story_arc.emotion_mappings.{trait_name}.trait_owner must be 'player' or 'npc'"
                )
            if mapping.trait_owner == "npc" and mapping.default_npc:
                if mapping.default_npc not in seen_npc_ids:
                    errors.append(
                        f"story_arc.emotion_mappings.{trait_name}.default_npc '{mapping.default_npc}' not found"
                    )

            # Validate ranges don't overlap
            ranges = sorted(mapping.ranges, key=lambda r: r.min)
            for j in range(len(ranges) - 1):
                if ranges[j].max >= ranges[j + 1].min:
                    errors.append(
                        f"story_arc.emotion_mappings.{trait_name}.ranges overlap at index {j}"
                    )

    # ===== Story Arc Gap Detection =====
    # Detect when a story_arc node's canvas requires a flag, but the canvas
    # that sets that flag has no story_arc node (causing Guide to skip it)
    if story_arc and template.canvases:
        # 1. Build set of canvas IDs that have story_arc nodes
        canvases_with_story_nodes: Set[str] = {
            n.linked_canvas for n in story_arc.nodes if n.linked_canvas
        }

        # 2. Build map: flag_key -> list of canvas_ids that set it
        flag_to_setters: Dict[str, List[str]] = {}
        for canvas in template.canvases:
            for flag in _extract_flags_set_by_canvas(canvas):
                flag_to_setters.setdefault(flag, []).append(canvas.id)

        # 3. Build map: canvas_id -> set of required flag_keys
        canvas_to_required_flags: Dict[str, Set[str]] = {
            canvas.id: _extract_flags_required_by_canvas(canvas)
            for canvas in template.canvases
        }

        # 4. Check for gaps
        for story_node in story_arc.nodes:
            if not story_node.linked_canvas:
                continue

            linked_canvas_id = story_node.linked_canvas
            required_flags = canvas_to_required_flags.get(linked_canvas_id, set())

            for flag in required_flags:
                setters = flag_to_setters.get(flag, [])
                if not setters:
                    continue  # Flag never set - different issue

                # Check if ANY setter has a story_arc node
                setters_with_nodes = [
                    s for s in setters if s in canvases_with_story_nodes
                ]

                if not setters_with_nodes:
                    # Found a gap!
                    setter_list = ", ".join(setters[:3])
                    if len(setters) > 3:
                        setter_list += f" (and {len(setters) - 3} more)"

                    errors.append(
                        f"Story arc gap: {story_node.id} -> {linked_canvas_id} requires flag '{flag}', "
                        f"but {setter_list} sets this flag without a story_arc node. "
                        f"Add a story_arc node for {setters[0]} before {story_node.id}."
                    )

    # ===== Clothing validation (optional) =====
    if template.clothing_enabled:
        seen_clothing_ids: Set[str] = set()
        for i, ci in enumerate(template.clothing_items):
            if not _is_valid_slug(ci.id):
                errors.append(f"clothing[{i}].id '{ci.id}' must be lowercase snake_case")
            if not ci.name:
                errors.append(f"clothing[{i}].name is required")
            if ci.slot not in VALID_CLOTHING_SLOTS:
                errors.append(
                    f"clothing[{i}].slot '{ci.slot}' must be one of {sorted(VALID_CLOTHING_SLOTS)}"
                )
            if ci.id in seen_clothing_ids:
                errors.append(f"duplicate clothing id: {ci.id}")
            seen_clothing_ids.add(ci.id)

    # ===== Passes validation =====
    seen_pass_ids: Set[str] = set()
    for i, p in enumerate(template.passes):
        if not p.id:
            errors.append(f"passes[{i}] missing id")
        if p.id in seen_pass_ids:
            errors.append(f"duplicate pass id: {p.id}")
        seen_pass_ids.add(p.id)
        if p.cost <= 0:
            errors.append(f"passes[{i}].cost must be positive")
        if p.duration_days <= 0:
            errors.append(f"passes[{i}].duration_days must be positive")

    # ===== Items validation =====
    seen_item_ids: Set[str] = set()
    for i, it in enumerate(template.items):
        if not it.id:
            errors.append(f"items[{i}] missing id")
        if it.id in seen_item_ids:
            errors.append(f"duplicate item id: {it.id}")
        seen_item_ids.add(it.id)
        if it.max_stack <= 0:
            errors.append(f"items[{i}].max_stack must be positive")

    # ===== Rent validation (optional) =====
    if template.rent_enabled:
        if template.rent_amount <= 0:
            errors.append("rent amount must be a positive integer")
        if template.rent_due_day not in VALID_DAYS:
            errors.append(
                f"rent due_day '{template.rent_due_day}' must be one of {sorted(VALID_DAYS)}"
            )
        if template.rent_collector_npc:
            npc_ids = {n.id for n in template.npcs}
            if template.rent_collector_npc not in npc_ids:
                errors.append(
                    f"rent collector_npc '{template.rent_collector_npc}' not found in NPC definitions"
                )
        if template.rent_grace_periods < 0:
            errors.append("rent grace_periods must be >= 0")
        if template.rent_eviction_mode not in ("game_end", "flag_set"):
            errors.append(
                f"rent eviction_mode must be 'game_end' or 'flag_set', "
                f"got '{template.rent_eviction_mode}'"
            )
        if template.rent_eviction_mode == "flag_set":
            if not _is_valid_slug(template.rent_eviction_flag):
                errors.append(
                    f"rent eviction_flag must be lowercase snake_case, "
                    f"got '{template.rent_eviction_flag}'"
                )

    # ===== E4: Stage helpers validation =====
    if template.stage_helpers:
        seen_helper_names: Set[str] = set()
        for hi, sh in enumerate(template.stage_helpers):
            ctx = f"engine.stage_helpers[{hi}]"
            if not sh.name:
                errors.append(f"{ctx}.name is required")
                continue
            if sh.name in seen_helper_names:
                errors.append(
                    f"engine.stage_helpers: duplicate name '{sh.name}'"
                )
            seen_helper_names.add(sh.name)
            # Helpers may reference primitive condition types only — `type=stage`
            # nesting is rejected to keep runtime evaluation cycle-free.
            for item in sh.conditions.get("items", []) or []:
                if isinstance(item, dict) and item.get("type") == "stage":
                    errors.append(
                        f"{ctx} ('{sh.name}'): helpers must reference "
                        f"primitive condition types only — nested 'type=stage' "
                        f"items are not allowed in v1"
                    )
                    break

    return errors


# -------- Creation --------


def _ensure_user(owner_id: str) -> User:
    try:
        return User.objects.get(id=owner_id)
    except Exception:
        raise ValueError(f"owner id not found: {owner_id}")


@transaction.atomic
def create_project_from_template(
    template: GameTemplate, owner_id: str, name_override: Optional[str] = None
) -> Dict[str, Any]:
    owner = _ensure_user(owner_id)

    # Project
    project = Project(
        name=name_override or template.project.title,
        description=template.project.description,
        owner=owner,
    )
    project.metadata = project.metadata or {}
    project.metadata["time_settings"] = {
        "enabled": template.time.enabled,
        "starting_hour": template.time.starting_hour,
        "starting_day": template.time.starting_day,
        "starting_week": template.time.starting_week,
    }
    project.metadata["template"] = {
        "schema_version": template.schema_version,
        "slug": template.project.slug,
    }
    # Store clothing settings if enabled
    if template.clothing_enabled:
        clothing_meta = {
            "enabled": True,
            "wardrobe_location": template.wardrobe_location or "",
            "shop_location": template.shop_location or "",
            "items": [
                {
                    "id": ci.id,
                    "name": ci.name,
                    "slot": ci.slot,
                    "image": ci.image,
                    "initial": ci.initial,
                    "conditions": ci.conditions,
                    "price": ci.price,
                }
                for ci in template.clothing_items
            ],
        }
        if template.clothing_requirements:
            req = template.clothing_requirements
            clothing_meta["requirements"] = {
                "body_coverage": req.body_coverage,
                "always_required": req.always_required,
                "conditional": req.conditional,
            }
        project.metadata["clothing_settings"] = clothing_meta
    # Store sidebar items if defined
    if template.sidebar_items:
        project.metadata["sidebar_items"] = template.sidebar_items
    # Store passes if defined
    if template.passes:
        project.metadata["passes"] = [
            {
                "id": p.id,
                "name": p.name,
                "cost": p.cost,
                "duration_days": p.duration_days,
                "icon": p.icon,
            }
            for p in template.passes
        ]
    # Store items if defined
    if template.items:
        project.metadata["items"] = [
            {"id": it.id, "name": it.name, "icon": it.icon, "max_stack": it.max_stack}
            for it in template.items
        ]
    # Store daily-tick hook if defined ([engine.daily_tick])
    if template.daily_tick is not None:
        project.metadata["daily_tick"] = {
            "flagEffects": [
                {
                    "targetType": fe.targetType,
                    "npcId": fe.npcId,
                    "flag": fe.flag,
                    "op": fe.op,
                }
                for fe in template.daily_tick.flagEffects
            ]
        }
    # Store stage helpers if defined ([[engine.stage_helpers]]) — E4
    if template.stage_helpers:
        project.metadata["stage_helpers"] = [
            {
                "name": sh.name,
                "description": sh.description,
                "conditions": sh.conditions,
            }
            for sh in template.stage_helpers
        ]
    # Store theme if defined
    if template.theme:
        t = template.theme
        project.metadata["theme"] = {
            "mode": t.mode,
            "primary": t.primary,
            "secondary": t.secondary,
            "accent": t.accent,
            "success": t.success,
            "danger": t.danger,
            "warning": t.warning,
            "font_heading": t.font_heading,
            "font_mono": t.font_mono,
            "border_radius": t.border_radius,
            "bg": t.bg,
            "surface": t.surface,
            "surface_alt": t.surface_alt,
            "border": t.border,
            "text": t.text,
            "text_muted": t.text_muted,
            "custom_css": t.custom_css,
        }
    # Store rent settings if enabled
    if template.rent_enabled:
        project.metadata["rent_settings"] = {
            "enabled": True,
            "amount": template.rent_amount,
            "due_day": template.rent_due_day,
            "collector_npc": template.rent_collector_npc or "",
            "grace_periods": template.rent_grace_periods,
            "start_after_flag": template.rent_start_after_flag,
            "text": template.rent_text,
            "eviction_mode": template.rent_eviction_mode,
            "eviction_flag": template.rent_eviction_flag,
        }
    # Store story_arc if defined (for narrative journal and help page)
    if template.story_arc:
        project.metadata["story_arc"] = {
            "version": template.story_arc.version,
            "chapters": [
                {
                    "id": ch.id,
                    "name": ch.name,
                    "mood": ch.mood,
                    "description": ch.description,
                    "order": ch.order,
                }
                for ch in template.story_arc.chapters
            ],
            "nodes": [
                {
                    "id": n.id,
                    "name": n.name,
                    "chapter": n.chapter,
                    "journal_entry": n.journal_entry,
                    "linked_canvas": n.linked_canvas,
                    "linked_canvas_node": n.linked_canvas_node,
                    "linked_flag": n.linked_flag,
                    "is_milestone": n.is_milestone,
                    "group": n.group,
                    "requires_nodes": n.requires_nodes,
                    "requires_group": n.requires_group,
                    "npc": n.npc,
                    "trait_requirements": n.trait_requirements,
                    "branch_condition": n.branch_condition,
                    **({"linked_phone": n.linked_phone} if n.linked_phone else {}),
                    **({"guide_hint": n.guide_hint} if n.guide_hint else {}),
                }
                for n in template.story_arc.nodes
            ],
            "groups": [
                {
                    "id": g.id,
                    "name": g.name,
                    "description": g.description,
                    "required_count": g.required_count,
                }
                for g in template.story_arc.groups
            ],
            "emotion_mappings": {
                k: {
                    "trait_owner": v.trait_owner,
                    "default_npc": v.default_npc,
                    "ranges": [
                        {
                            "min": r.min,
                            "max": r.max,
                            "label": r.label,
                            "description": r.description,
                        }
                        for r in v.ranges
                    ],
                }
                for k, v in template.story_arc.emotion_mappings.items()
            },
            "hints": (
                {
                    "stuck_threshold_minutes": (
                        template.story_arc.hints.stuck_threshold_minutes
                        if template.story_arc.hints
                        else 30
                    ),
                    "hint_style": (
                        template.story_arc.hints.hint_style
                        if template.story_arc.hints
                        else "observation"
                    ),
                    "templates": [
                        {
                            "condition": (
                                {
                                    "missing_flag": (
                                        t.condition.missing_flag
                                        if t.condition
                                        else None
                                    ),
                                    "missing_trait": (
                                        t.condition.missing_trait
                                        if t.condition
                                        else None
                                    ),
                                    "gap_gte": (
                                        t.condition.gap_gte if t.condition else None
                                    ),
                                }
                                if t.condition
                                else None
                            ),
                            "text": t.text,
                        }
                        for t in (
                            template.story_arc.hints.templates
                            if template.story_arc.hints
                            else []
                        )
                    ],
                }
                if template.story_arc.hints
                else {}
            ),
        }
    # Store phone settings if enabled
    if template.phone_enabled and template.phone:
        phone = template.phone
        project.metadata["phone_settings"] = {
            "enabled": True,
            "apps": [
                {"id": a.id, "type": a.type, "label": a.label, "icon": a.icon}
                for a in phone.apps
            ],
            "conversations": [
                {
                    "id": c.id,
                    "app": c.app,
                    "npc": c.npc,
                    "trigger": c.trigger,
                    "blocks": [
                        {
                            "type": b.type,
                            "sender": b.sender,
                            "content": b.content,
                            "after_reply": b.after_reply,
                            "choices": b.choices,
                            **({"round": b.round} if b.round is not None else {}),
                            **({"after_round": b.after_round} if b.after_round is not None else {}),
                            **({"after_choice": b.after_choice} if b.after_choice is not None else {}),
                        }
                        for b in c.blocks
                    ],
                }
                for c in phone.conversations
            ],
            "posts": [
                {
                    "id": p.id,
                    "app": p.app,
                    "npc": p.npc,
                    "poster_name": p.poster_name,
                    "image": p.image,
                    "caption": p.caption,
                    "likes": p.likes,
                    "trigger": p.trigger,
                    "search_queries": p.search_queries,
                }
                for p in phone.posts
            ],
            "profiles": [
                {
                    "id": p.id,
                    "app": p.app,
                    "npc": p.npc,
                    "photos": p.photos,
                    "bio": p.bio,
                    "age": p.age,
                    "interests": p.interests,
                    "trigger": p.trigger,
                    "match_condition": p.match_condition,
                    "search_queries": p.search_queries,
                }
                for p in phone.profiles
            ],
            "daily_topics": [
                {
                    "id": dt.id,
                    "npc": dt.npc,
                    "player_message": dt.player_message,
                    "npc_response": dt.npc_response,
                    "effects": dt.effects,
                    "conditions": dt.conditions,
                }
                for dt in phone.daily_topics
            ],
        }
    project.save()

    # Player
    # Auto-register rent eviction flag when fail-forward mode is active,
    # so conditions can gate on $player.flags[<eviction_flag>] at runtime.
    _player_flag_keys = list(template.player.flag_keys or [])
    if template.rent_enabled and template.rent_eviction_mode == "flag_set":
        if template.rent_eviction_flag and template.rent_eviction_flag not in _player_flag_keys:
            _player_flag_keys.append(template.rent_eviction_flag)

    player = Character(
        project=project,
        name=template.player.name or "Player",
        description=template.player.description or "",
        core_traits=template.player.core_traits or {},
        flag_keys=_player_flag_keys,
    )
    player.character_metadata = player.character_metadata or {}
    player.character_metadata["slug"] = template.player.id
    # Store portrait path in JSON (not portrait_url URLField) for generator resolution
    if template.player.portrait:
        player.character_metadata["portrait"] = template.player.portrait
    # Store player trait_decay (per-day decay amounts)
    if template.player.trait_decay:
        player.character_metadata["trait_decay"] = template.player.trait_decay
    # Store player customization fields
    if template.player.customizable:
        player.character_metadata["customizable"] = True
        player.character_metadata["customization_fields"] = [
            {
                "id": cf.id,
                "type": cf.type,
                "label": cf.label,
                "default": cf.default,
                "options": (
                    [{"id": o.id, "image": o.image, "label": o.label} for o in cf.options]
                    if cf.type == "image_select"
                    else cf.options
                ),
                "sets_portrait": cf.sets_portrait,
            }
            for cf in template.player.customization_fields
        ]
    player.save()

    # NPCs
    npc_ids: List[str] = []
    for n in template.npcs:
        npc = NPC(
            project=project,
            name=n.name,
            description=n.description or "",
            core_traits=n.core_traits or {},
            flag_keys=n.flag_keys or [],
            hidden_from_ui=bool(n.hidden_from_ui),
        )
        npc.ai_behavior_config = npc.ai_behavior_config or {}
        npc.ai_behavior_config["slug"] = n.id
        # Store portrait path in JSON (not portrait_url URLField) for generator resolution
        if n.portrait:
            npc.ai_behavior_config["portrait"] = n.portrait
        # Store NPC schedules if present
        if n.schedules:
            npc.ai_behavior_config["schedules"] = [
                {
                    "location": sch.location,
                    "weekdays": sch.weekdays,
                    "start_time": sch.start_time,
                    "end_time": sch.end_time,
                    "activity": sch.activity,
                }
                for sch in n.schedules
            ]
        # Store customization fields
        if n.customizable:
            npc.ai_behavior_config["customizable"] = True
        if n.relationship:
            npc.ai_behavior_config["relationship"] = n.relationship
        if n.relationship_options:
            npc.ai_behavior_config["relationship_options"] = n.relationship_options
        if n.trait_decay:
            npc.ai_behavior_config["trait_decay"] = n.trait_decay
        # E9/E10/E11: per-NPC arc_stages list (display names per stage value).
        if n.arc_stages:
            npc.ai_behavior_config["arc_stages"] = n.arc_stages
        npc.save()
        npc_ids.append(str(npc.id))

    # Locations (two-pass)
    slug_map: Dict[str, Location] = {}
    for l in template.locations:
        loc = Location(
            project=project,
            name=l.name,
            description=l.description or "",
            is_container=bool(l.is_container),
        )
        loc.properties = loc.properties or {}
        loc.properties["slug"] = l.id
        if l.image:
            loc.properties["image"] = l.image
        if l.image_search_queries:
            loc.properties["image_search_queries"] = l.image_search_queries
        if l.entry_conditions:
            loc.properties["entry_conditions"] = l.entry_conditions
        if l.blocked_message:
            loc.properties["blocked_message"] = l.blocked_message
        if l.clothing_rules:
            loc.properties["clothing_rules"] = l.clothing_rules
        loc.save()
        slug_map[l.id] = loc

    # Pass 2a: resolve parent links for all (ensures container context is correct)
    for l in template.locations:
        loc = slug_map[l.id]
        if l.parent:
            loc.parent_location = slug_map.get(l.parent)
        else:
            loc.parent_location = None
        # validate & save hierarchy only
        loc.full_clean()
        loc.save()

    # Pass 2b: resolve entry_from and default_entry now that parents are set
    for l in template.locations:
        loc = slug_map[l.id]
        if l.entry_from:
            loc.entry_from = slug_map.get(l.entry_from)
        else:
            loc.entry_from = None
        if l.default_entry:
            loc.default_entry_location = slug_map.get(l.default_entry)
        else:
            loc.default_entry_location = None
        loc.full_clean()
        loc.save()

    # navigation_order
    for l in template.locations:
        if not l.navigation_order:
            continue
        loc = slug_map[l.id]
        loc.navigation_order = [
            str(slug_map[s].id) for s in l.navigation_order if s in slug_map
        ]
        loc.full_clean()
        loc.save()

    # ===== Story Import (optional) =====
    canvas_slug_map: Dict[str, StoryCanvas] = {}
    node_slug_map: Dict[str, StoryNode] = {}
    node_local_map: Dict[Tuple[str, str], StoryNode] = {}

    starting_canvas_db = None
    starting_canvas_node_count = 0

    if getattr(template, "canvases", None):
        # Create canvases
        for c in template.canvases:
            sc = StoryCanvas(
                project=project,
                name=c.name,
                description=c.description or "",
            )
            sc.metadata = sc.metadata or {}
            sc.metadata["slug"] = c.id
            if c.loop:
                sc.metadata["loop"] = c.loop
            sc.save()
            canvas_slug_map[c.id] = sc

        # Set starting canvas from template slug (required)
        if template.starting_canvas:
            if template.starting_canvas not in canvas_slug_map:
                raise ValueError(
                    f"starting_canvas '{template.starting_canvas}' not found in canvases. "
                    f"Available canvas IDs: {list(canvas_slug_map.keys())[:10]}..."
                )
            starting_canvas_db = canvas_slug_map[template.starting_canvas]
            Project.objects.filter(id=project.id).update(
                starting_canvas_id=starting_canvas_db.id
            )
            project.refresh_from_db(fields=["starting_canvas"])
        else:
            raise ValueError(
                "starting_canvas is required but was not found in TOML. "
                "Add 'starting_canvas = \"your_canvas_id\"' to the [project] section."
            )

        # Triggers + schedules
        for c in template.canvases:
            sc = canvas_slug_map[c.id]
            if c.trigger:
                trig = CanvasTrigger(
                    canvas=sc,
                    location_id=(
                        str(slug_map[c.trigger.location].id)
                        if c.trigger.location in slug_map
                        else None
                    ),
                    conditions=c.trigger.conditions or {},
                    is_active=bool(c.trigger.is_active),
                    is_activity=False,
                    is_repeatable=bool(c.trigger.is_repeatable),
                    max_triggers_per_day=c.trigger.max_triggers_per_day,
                    priority=c.trigger.priority,
                    metadata={
                        k: v for k, v in {
                            "npc": c.trigger.npc or None,
                            "trigger_mode": c.trigger.trigger_mode if c.trigger.trigger_mode != "manual" else None,
                            "chance": c.trigger.chance,
                            "costs": c.trigger.costs if c.trigger.costs else None,
                        }.items() if v is not None
                    },
                )
                trig.save()
                for s in c.trigger.schedules:
                    TriggerSchedule.objects.create(
                        trigger=trig,
                        name=f"{sc.name} schedule",
                        weekdays=s.weekdays,
                        start_time=s.start_time,
                        end_time=s.end_time,
                    )

        # Nodes
        for c in template.canvases:
            sc = canvas_slug_map[c.id]
            for n in c.nodes:
                # Normalize TOML blocks: add id, ensure props/children shapes,
                # and default heading level so frontend schemas accept them.
                safe_blocks: list[dict[str, Any]] = []
                for b in n.blocks or []:
                    if not isinstance(b, dict):
                        continue
                    b_type = str(b.get("type", "")).strip()
                    if not b_type:
                        continue
                    props = b.get("props") or {}
                    if not isinstance(props, dict):
                        props = {}
                    # Default heading.level
                    if b_type == "heading":
                        if not props.get("level"):
                            props["level"] = 1

                    # Handle clip blocks - convert clip_id to clipId
                    if b_type == "clip":
                        clip_id = b.get("clip_id")  # Top-level clip_id from TOML
                        if clip_id and isinstance(clip_id, str):
                            props["clipId"] = str(clip_id).strip()

                    # Handle block_pool - random content variant selection
                    if b_type == "block_pool":
                        pool_blocks_raw = b.get("blocks", [])
                        if not isinstance(pool_blocks_raw, list):
                            pool_blocks_raw = []

                        pool_child_types: set = set()
                        pool_safe_blocks: list[dict[str, Any]] = []
                        for pb in pool_blocks_raw:
                            if not isinstance(pb, dict):
                                continue
                            pb_type = str(pb.get("type", "")).strip()
                            if not pb_type or pb_type == "block_pool":
                                continue  # Skip empty types and nested pools
                            pool_child_types.add(pb_type)
                            pb_props = pb.get("props") or {}
                            if not isinstance(pb_props, dict):
                                pb_props = {}
                            if pb_type == "heading" and not pb_props.get("level"):
                                pb_props["level"] = 1
                            if pb_type == "clip":
                                pb_clip_id = pb.get("clip_id")
                                if pb_clip_id and isinstance(pb_clip_id, str):
                                    pb_props["clipId"] = str(pb_clip_id).strip()
                            # Handle group children inside pool
                            if pb_type == "group":
                                g_cond = pb.get("conditions")
                                if g_cond and isinstance(g_cond, dict):
                                    pb_props["conditions"] = g_cond
                                inner_raw = pb.get("blocks", [])
                                inner_safe: list[dict[str, Any]] = []
                                for ib in (inner_raw if isinstance(inner_raw, list) else []):
                                    if not isinstance(ib, dict):
                                        continue
                                    ib_type = str(ib.get("type", "")).strip()
                                    if not ib_type or ib_type == "group":
                                        continue
                                    ib_props = ib.get("props") or {}
                                    if not isinstance(ib_props, dict):
                                        ib_props = {}
                                    if ib_type == "heading" and not ib_props.get("level"):
                                        ib_props["level"] = 1
                                    inner_safe.append({
                                        "id": str(ib.get("id") or uuid.uuid4()),
                                        "type": ib_type, "props": ib_props,
                                        "content": str(ib.get("content", "")),
                                        "children": [],
                                    })
                                pb_props["blocks"] = inner_safe

                            pool_safe_blocks.append({
                                "id": str(pb.get("id") or uuid.uuid4()),
                                "type": pb_type, "props": pb_props,
                                "content": str(pb.get("content", "")),
                                "children": [],
                            })

                        if len(pool_child_types) > 1:
                            logger.warning(
                                "block_pool has mixed types %s — all items should be same type",
                                pool_child_types,
                            )

                        props["blocks"] = pool_safe_blocks
                        safe_blocks.append({
                            "id": str(b.get("id") or uuid.uuid4()),
                            "type": "block_pool", "props": props,
                            "content": "", "children": [],
                        })
                        continue

                    # Handle group blocks - conditional content variants
                    if b_type == "group":
                        group_conditions = b.get("conditions")
                        if group_conditions and isinstance(group_conditions, dict):
                            props["conditions"] = group_conditions

                        child_blocks_raw = b.get("blocks", [])
                        if not isinstance(child_blocks_raw, list):
                            child_blocks_raw = []

                        child_safe_blocks: list[dict[str, Any]] = []
                        for cb in child_blocks_raw:
                            if not isinstance(cb, dict):
                                continue
                            cb_type = str(cb.get("type", "")).strip()
                            if not cb_type or cb_type == "group":
                                continue  # Skip empty types and nested groups
                            cb_props = cb.get("props") or {}
                            if not isinstance(cb_props, dict):
                                cb_props = {}
                            if cb_type == "heading" and not cb_props.get("level"):
                                cb_props["level"] = 1
                            if cb_type == "clip":
                                cb_clip_id = cb.get("clip_id")
                                if cb_clip_id and isinstance(cb_clip_id, str):
                                    cb_props["clipId"] = str(cb_clip_id).strip()
                            # Handle block_pool children inside group
                            if cb_type == "block_pool":
                                bp_raw = cb.get("blocks", [])
                                bp_safe: list[dict[str, Any]] = []
                                for bp_item in (bp_raw if isinstance(bp_raw, list) else []):
                                    if not isinstance(bp_item, dict):
                                        continue
                                    bp_t = str(bp_item.get("type", "")).strip()
                                    if not bp_t or bp_t == "block_pool":
                                        continue
                                    bp_p = bp_item.get("props") or {}
                                    if not isinstance(bp_p, dict):
                                        bp_p = {}
                                    if bp_t == "heading" and not bp_p.get("level"):
                                        bp_p["level"] = 1
                                    # Handle group items inside pool inside group
                                    if bp_t == "group":
                                        g_cond = bp_item.get("conditions")
                                        if g_cond and isinstance(g_cond, dict):
                                            bp_p["conditions"] = g_cond
                                        g_inner_raw = bp_item.get("blocks", [])
                                        g_inner_safe: list[dict[str, Any]] = []
                                        for gi in (g_inner_raw if isinstance(g_inner_raw, list) else []):
                                            if not isinstance(gi, dict):
                                                continue
                                            gi_t = str(gi.get("type", "")).strip()
                                            if not gi_t or gi_t in ("group", "block_pool"):
                                                continue
                                            gi_p = gi.get("props") or {}
                                            if not isinstance(gi_p, dict):
                                                gi_p = {}
                                            if gi_t == "heading" and not gi_p.get("level"):
                                                gi_p["level"] = 1
                                            g_inner_safe.append({
                                                "id": str(gi.get("id") or uuid.uuid4()),
                                                "type": gi_t, "props": gi_p,
                                                "content": str(gi.get("content", "")),
                                                "children": [],
                                            })
                                        bp_p["blocks"] = g_inner_safe
                                    bp_safe.append({
                                        "id": str(bp_item.get("id") or uuid.uuid4()),
                                        "type": bp_t, "props": bp_p,
                                        "content": str(bp_item.get("content", "")),
                                        "children": [],
                                    })
                                cb_props["blocks"] = bp_safe
                            child_safe_blocks.append({
                                "id": str(cb.get("id") or uuid.uuid4()),
                                "type": cb_type,
                                "props": cb_props,
                                "content": str(cb.get("content", "")),
                                "children": [],
                            })

                        props["blocks"] = child_safe_blocks
                        safe_blocks.append({
                            "id": str(b.get("id") or uuid.uuid4()),
                            "type": "group",
                            "props": props,
                            "content": "",
                            "children": [],
                        })
                        continue

                    # Ensure base shape
                    safe_blocks.append(
                        {
                            "id": str(b.get("id") or uuid.uuid4()),
                            "type": b_type,
                            "props": props,
                            "content": str(b.get("content", "")),
                            "children": [],
                        }
                    )

                node_data_dict = {
                    "blocks": safe_blocks,
                    "version": BlockConversionService.DEFAULT_VERSION,
                    # Optional preview text for convenience; safe to omit
                    "content": (
                        BlockConversionService.get_preview_text(safe_blocks)
                        if safe_blocks
                        else ""
                    ),
                    "slug": n.id,
                }
                if n.modifier_redirect:
                    node_data_dict["modifier_redirect"] = n.modifier_redirect

                node = StoryNode(
                    canvas=sc,
                    name=n.name,
                    # Ensure BlockNote block format is explicitly versioned so
                    # downstream serializers/migration preserve the content
                    node_data=node_data_dict,
                    exit_block=_serialize_exit_block(n.exit_block),
                )
                node.save()
                key = f"{c.id}.{n.id}"
                node_slug_map[key] = node
                node_local_map[(c.id, n.id)] = node
                if starting_canvas_db and sc.id == starting_canvas_db.id:
                    starting_canvas_node_count += 1

        # Connections
        for c in template.canvases:
            sc = canvas_slug_map[c.id]
            for cc in c.connections:
                src = node_local_map.get((c.id, cc.source))
                tgt = node_local_map.get((c.id, cc.target))
                if not src or not tgt:
                    continue
                NodeConnection.objects.create(
                    canvas=sc,
                    source_node=src,
                    target_node=tgt,
                    connection_type=cc.connection_type or "default",
                )

        # Rewrite exit_block slugs to UUIDs
        for c in template.canvases:
            for n in c.nodes:
                node = node_local_map.get((c.id, n.id))
                if not node:
                    continue
                eb = n.exit_block
                eb_dict: Dict[str, Any] = _serialize_exit_block(eb)
                if eb.type == "choices":
                    new_choices: List[Dict[str, Any]] = []
                    for ch in eb.choices:
                        ch_d: Dict[str, Any] = {
                            "text": ch.text or "Continue",
                            "targetType": ch.targetType or "trigger",
                        }
                        if ch.time_progression_minutes is not None:
                            ch_d["time_progression_minutes"] = int(
                                ch.time_progression_minutes
                            )
                        if ch.effects:
                            ch_d["effects"] = [
                                {
                                    "targetType": e.targetType,
                                    "npcId": e.npcId,
                                    "trait": e.trait,
                                    "op": e.op,
                                    "value": e.value,
                                    "clamp": e.clamp,
                                    "cap": e.cap,
                                }
                                for e in ch.effects
                            ]
                        if ch.flagEffects:
                            ch_d["flagEffects"] = [
                                {
                                    "targetType": e.targetType,
                                    "npcId": e.npcId,
                                    "flag": e.flag,
                                    "op": e.op,
                                }
                                for e in ch.flagEffects
                            ]
                        if ch.wardrobeEffects:
                            ch_d["wardrobeEffects"] = ch.wardrobeEffects
                        if ch.conditions:
                            ch_d["conditions"] = ch.conditions
                        if ch.text_variants:
                            ch_d["text_variants"] = ch.text_variants

                        # Rejection system fields
                        if ch.show_when_locked:
                            ch_d["show_when_locked"] = True
                        if ch.locked_text:
                            ch_d["locked_text"] = ch.locked_text
                        if ch.rejection_node:
                            # Resolve rejection_node slug → UUID (same as nodeId)
                            rej_key = (
                                ch.rejection_node
                                if "." in ch.rejection_node
                                else f"{c.id}.{ch.rejection_node}"
                            )
                            rej_target = node_slug_map.get(rej_key)
                            if rej_target:
                                ch_d["rejection_node"] = str(rej_target.id)
                        if ch.rejection_effects:
                            ch_d["rejection_effects"] = [
                                {
                                    "targetType": e.targetType,
                                    "npcId": e.npcId,
                                    "trait": e.trait,
                                    "op": e.op,
                                    "value": e.value,
                                    "clamp": e.clamp,
                                    "cap": e.cap,
                                }
                                for e in ch.rejection_effects
                            ]
                        if ch.modifier_effects:
                            ch_d["modifier_effects"] = [
                                {
                                    "key": me.key,
                                    "name": me.name,
                                    "duration_hours": me.duration_hours,
                                    "trait_offsets": me.trait_offsets,
                                }
                                for me in ch.modifier_effects
                            ]
                        if ch.pass_effects:
                            ch_d["pass_effects"] = ch.pass_effects
                        if ch.item_effects:
                            ch_d["item_effects"] = ch.item_effects

                        if ch.targetType == "location" and ch.locationId:
                            loc_obj = slug_map.get(ch.locationId)
                            if loc_obj:
                                ch_d["locationId"] = str(loc_obj.id)
                        elif ch.targetType == "node" and ch.nodeId:
                            key = (
                                ch.nodeId if "." in ch.nodeId else f"{c.id}.{ch.nodeId}"
                            )
                            target_node = node_slug_map.get(key)
                            if target_node:
                                ch_d["nodeId"] = str(target_node.id)

                        new_choices.append(ch_d)
                    eb_dict["choices"] = new_choices
                else:
                    dest = eb_dict.get("config", {}).get("destinationType", "trigger")
                    if dest == "specific":
                        loc_slug = eb_dict.get("config", {}).get("locationId")
                        if loc_slug and loc_slug in slug_map:
                            eb_dict["config"]["locationId"] = str(slug_map[loc_slug].id)
                    elif dest == "node":
                        dest_id = eb_dict.get("config", {}).get("destinationId", "")
                        if dest_id:
                            key = dest_id if "." in dest_id else f"{c.id}.{dest_id}"
                            target_node = node_slug_map.get(key)
                            if target_node:
                                eb_dict["config"]["destinationId"] = str(target_node.id)

                if n.loop_terminal:
                    eb_dict["loop_terminal"] = True
                node.exit_block = eb_dict

                # Resolve modifier_redirect node slug → UUID
                save_fields = ["exit_block"]
                if n.modifier_redirect and n.modifier_redirect.get("node"):
                    mr_slug = n.modifier_redirect["node"]
                    mr_key = mr_slug if "." in mr_slug else f"{c.id}.{mr_slug}"
                    mr_target = node_slug_map.get(mr_key)
                    if mr_target:
                        node.node_data = node.node_data or {}
                        node.node_data["modifier_redirect"] = {
                            "modifier_key": n.modifier_redirect.get("modifier_key", ""),
                            "node": str(mr_target.id),
                        }
                        save_fields.append("node_data")
                node.save(update_fields=save_fields)

    return {
        "project_id": str(project.id),
        "player_id": str(player.id),
        "npc_ids": npc_ids,
        "location_ids": [str(slug_map[s].id) for s in slug_map.keys()],
        "canvas_ids": [str(sc.id) for sc in canvas_slug_map.values()],
        "node_count": len(node_slug_map),
        "starting_canvas_id": (
            str(starting_canvas_db.id) if starting_canvas_db else None
        ),
        "starting_canvas_name": starting_canvas_db.name if starting_canvas_db else None,
        "starting_canvas_nodes": starting_canvas_node_count,
        "template_starting_canvas_slug": template.starting_canvas,
        "available_canvas_slugs": list(canvas_slug_map.keys()),
    }


def _serialize_exit_block(eb: "TemplateExitBlock") -> Dict[str, Any]:
    d: Dict[str, Any] = {
        "type": eb.type or "location",
        "text": eb.text or "Continue",
        "config": eb.config or {},
    }
    if eb.type == "choices":
        d["choices"] = [
            {
                "text": ch.text or "Continue",
                "targetType": ch.targetType or "trigger",
                **({"locationId": ch.locationId} if ch.locationId else {}),
                **({"nodeId": ch.nodeId} if ch.nodeId else {}),
                **(
                    {"time_progression_minutes": int(ch.time_progression_minutes)}
                    if ch.time_progression_minutes is not None
                    else {}
                ),
                **(
                    {
                        "effects": [
                            {
                                "targetType": e.targetType,
                                "npcId": e.npcId,
                                "trait": e.trait,
                                "op": e.op,
                                "value": e.value,
                                "clamp": e.clamp,
                                "cap": e.cap,
                            }
                            for e in ch.effects
                        ]
                    }
                    if ch.effects
                    else {}
                ),
                **(
                    {
                        "flagEffects": [
                            {
                                "targetType": e.targetType,
                                "npcId": e.npcId,
                                "flag": e.flag,
                                "op": e.op,
                            }
                            for e in ch.flagEffects
                        ]
                    }
                    if ch.flagEffects
                    else {}
                ),
                **({"wardrobeEffects": ch.wardrobeEffects} if ch.wardrobeEffects else {}),
                **({"conditions": ch.conditions} if ch.conditions else {}),
                **({"text_variants": ch.text_variants} if ch.text_variants else {}),
                **({"show_when_locked": True} if ch.show_when_locked else {}),
                **({"locked_text": ch.locked_text} if ch.locked_text else {}),
                **({"rejection_node": ch.rejection_node} if ch.rejection_node else {}),
                **(
                    {
                        "rejection_effects": [
                            {
                                "targetType": e.targetType,
                                "npcId": e.npcId,
                                "trait": e.trait,
                                "op": e.op,
                                "value": e.value,
                                "clamp": e.clamp,
                                "cap": e.cap,
                            }
                            for e in ch.rejection_effects
                        ]
                    }
                    if ch.rejection_effects
                    else {}
                ),
                **(
                    {
                        "modifier_effects": [
                            {
                                "key": me.key,
                                "name": me.name,
                                "duration_hours": me.duration_hours,
                                "trait_offsets": me.trait_offsets,
                            }
                            for me in ch.modifier_effects
                        ]
                    }
                    if ch.modifier_effects
                    else {}
                ),
                **({"pass_effects": ch.pass_effects} if ch.pass_effects else {}),
                **({"item_effects": ch.item_effects} if ch.item_effects else {}),
            }
            for ch in eb.choices
        ]
    return d
