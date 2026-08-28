"""
Template import service for creating a new Project from a single TOML file.

Scope v0.1: project basics, time, player, NPCs, locations + navigation only.
No twee generation or canvases. Creates a brand-new Project and related rows.
"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass, field, is_dataclass
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
    # PRD 48 — Quests Engine V2 opt-in flag. "v1" (default) → existing
    # [[story_arc.hints.templates]] engine. "v2" → new [[quests.cards]]
    # engine. Per-game opt-in; other games stay on v1 untouched.
    quests_engine: str = "v1"
    # Optional sidebar-footer metadata; default "" so games without these keys
    # render no footer. Purely additive.
    version: str = ""
    release_date: str = ""
    # Optional studio identity baked into the build: the funding link (sidebar
    # button + both intro/age-gate links) and the "Developed by X" credit under
    # the age gate. Default "" — the GENERATOR supplies the fallback
    # (v2.DEFAULT_SUPPORT_URL / DEFAULT_STUDIO_NAME), deliberately not this
    # dataclass, so the second [project] reader (build_guide.py, raw tomllib)
    # cannot resolve a different value than the sidebar does.
    support_url: str = ""
    studio_name: str = ""


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
    # G · the cast card's tag line. Up to NPC_TAGS_MAX short phrases naming what
    # this person is about — how they operate, what they want, an aesthetic, and
    # something mundane they consume. Rendered on the cast page under
    # `relationship`. Ships to runtime via the slug-keyed `setup.npc_tags`
    # registry, NOT via $npcs — see v2.py's npc_tags_map for why.
    tags: List[str] = field(default_factory=list)
    # F10 · the short label under this character's NAME in every dialogue box.
    # NOT `relationship`, which is a cast-page sentence and — measured across the
    # repo — repeats: five of one game's six relationship strings contain
    # "husband", and another game has two people whose strings both begin "Your
    # brother". A label that repeats is the confusion this field exists to remove,
    # so it is AUTHORED and never derived, and validate() refuses two that match.
    #   · no "Your" — it is on every label and carries nothing
    #   · 1-3 words: "husband's eldest", "brother-in-law", "elder brother"
    #   · unique in the cast; when the relation word repeats, the label carries
    #     what actually separates them — birth order, side of the family, a place
    # Empty is fine and renders no line at all.
    role: str = ""


@dataclass
class TemplateLocation:
    id: str
    name: str
    description: str = ""
    image: str = ""  # Relative to video_folder, e.g., "locations/kitchen.jpg"
    image_search_queries: List[str] = field(default_factory=list)  # For Missing Media page
    is_container: bool = False
    offscreen: bool = False  # Non-navigable "away" location (NPC schedule label; no nav card, no hub, exempt from presence floor + reachability)
    parent: str = ""
    entry_from: str = ""
    default_entry: str = ""
    navigation_order: List[str] = field(default_factory=list)
    entry_conditions: Dict[str, Any] = field(default_factory=dict)
    blocked_message: str = ""
    # A TRANSIT STOP opts out of engine-built navigation: no auto "Leave <name>" link, and an
    # empty nav list is treated as intentional rather than as a stranded location (so the
    # list-every-location fallback stays quiet). For a location the player arrives at and leaves
    # by CANVAS — a car drop-off, a lift — where the engine's tree model doesn't apply. The author
    # owns the way out; there is no safety net. Default True = every existing game unchanged.
    auto_exit: bool = True
    # Per-ENTRY travel friction charged when the player moves INTO this location.
    # `time` (minutes) advances the day-cycle clock; every other key deducts that
    # player trait (e.g. energy). Empty = a free move (today's behavior).
    costs: Dict[str, int] = field(default_factory=dict)
    clothing_rules: List[Dict[str, Any]] = field(default_factory=list)
    # State-reactive room prose. `description` above is the ELSE branch and stays
    # required; each variant is {conditions, text} and the generator emits them as a
    # first-match <<if>>/<<elseif>>/<<else>> chain, the same semantics adjacent [group]
    # blocks already have. Empty = one static paragraph, exactly as before.
    #
    # WHY: a room read identically at 03:00 and at 18:00, on day one and day ninety.
    # Measured across a 26-game field, 22% of rooms rotate their text and 17% vary by
    # hour; ours did neither, because there was no way to author it.
    description_variants: List[Dict[str, Any]] = field(default_factory=list)


# -------- Narrative person --------

# Which grammatical person the game's prose is written in. Set once per game via
# `[settings] narration_person`; the generator uses it to label the player's own
# dialog and thought-bubble blocks. Without it the engine assumed second person and
# stamped "You:" onto every player line — which reads as a contradiction in a game
# narrated in third ("she") or first ("I").
VALID_NARRATION_PERSONS = {"second", "first", "third"}

# Ceiling on `[[npcs]] tags` — the cast card's tag line. Four, because the field is
# unanimous at four: friends-of-mine's Characterpedia gives all fifteen of its
# characters exactly four ("Manipulation | Attention | Writing | Oriental Food"),
# and the shape is consistent — how they operate, what they want, an aesthetic, and
# something mundane they consume. A fifth entry turns the line into a stat block,
# which is the thing the trivial fourth slot exists to prevent.
NPC_TAGS_MAX = 4

# -------- Clothing System Data Shapes --------

VALID_CLOTHING_SLOTS = {"bra", "underwear", "top", "bottom", "dress", "legwear", "shoes"}

# Soft-guidance type catalog for the `type` field on clothing items (Doc 72 / Doc 71 R2).
# Authors can use any string — this is the typo-catch reference set, not a closed allowlist.
# The `worn_type` predicate matches against whatever string the item declares.
RECOMMENDED_CLOTHING_TYPES = {
    "casual", "swim", "costume", "schoolwear", "fitness", "uniform", "sleepwear",
}


@dataclass
class TemplateClothingItem:
    id: str
    name: str
    slot: str  # Must be in VALID_CLOTHING_SLOTS
    image: str = ""  # Relative to video_folder, e.g., "clothing/white_blouse.jpg"
    initial: bool = False  # If true, player starts with this item
    conditions: Dict[str, Any] = field(default_factory=dict)  # v1.0 conditions for wearing
    price: int = 0  # Price in dollars, 0 for initial/free items
    beauty: int = 0  # Appearance contribution of this garment (worn_beauty reads MAX)
    corruption: int = 0  # How revealing/lewd; worn_corruption reads MAX. Routes
    # content only — never mutates the global player.corruption core_trait.
    type: str = ""  # Optional category tag ("swim", "costume", etc.); read by `worn_type`
    # predicate. Doc 72 / Doc 71 R2. Empty string = untyped; worn_type matches return false.
    exposure: int = 0  # How much of her this garment leaves showing: 0 covers, 1 shows
    # underwear-level skin, 2 leaves the region bare. Read by `worn_exposure`, which takes
    # the MAX across the outfit AND treats an empty core slot as bare — that second half is
    # the whole point for the AGGREGATES: getWornStatMax skips empty slots and starts at 0,
    # so worn_beauty and worn_corruption cannot tell naked from plainly dressed. (Per-slot
    # emptiness was always askable via the `clothing_slot` predicate — engine.md §17.)
    #
    # Measured, degrees-of-lewdity: `$exposed` is the most-read variable in the game — 654
    # tests of `gte 1` and 307 of `gte 2` against 54 reads of any per-slot `.exposed`, so the
    # single 0/1/2 scalar is what the field actually gates on and the per-slot detail is not.


@dataclass
class TemplateClothingRequirements:
    body_coverage: bool = True  # Must wear (top + bottom) OR dress
    always_required: List[str] = field(default_factory=list)  # Slots that can never be removed
    conditional: Dict[str, Dict[str, str]] = field(default_factory=dict)  # slot -> {until_flag, message}


# -------- Phone System Data Shapes --------

VALID_PHONE_APP_TYPES = {"chat", "social_feed", "gallery", "dating", "custom", "quests", "fast_jobs", "bank"}


@dataclass
class TemplatePhoneApp:
    id: str
    type: str  # "chat", "social_feed", "gallery", "custom", "quests"
    label: str = ""
    icon: str = ""  # Relative to video_folder, optional
    # doc 45 G2 — social_feed posting actions (selfie/lewd/nude analog).
    # Each: {label, corruption_min?, followers_min, followers_max, daily_cap?, counter_trait}
    post_actions: List[Dict[str, Any]] = field(default_factory=list)


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
    # doc 45 G1 — optional toast text shown when this conversation is delivered
    # (its trigger first satisfied). Empty ⇒ default "📱 New message".
    notify: str = ""


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
    # doc 45 G1 — optional toast text shown when this post is delivered.
    # Empty ⇒ default "📱 New post".
    notify: str = ""


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
    # doc 45 G3 — photo quick-action extensions (all optional).
    # image: a media path rendered as a sent-photo bubble.
    # corruption_min: lock the action until player corruption ≥ this (🔒 + note).
    # cooldown: "per_topic" ⇒ this topic has its OWN once-per-day cap (RTS photo
    #   actions); default ("") keeps the legacy per-NPC 1/day cap.
    image: str = ""
    corruption_min: Optional[int] = None
    cooldown: str = ""


@dataclass
class TemplatePhoneGalleryItem:
    """doc 45 G8 — a gallery image, optionally trigger-gated + clickable (link)."""
    id: str
    image: str = ""
    caption: str = ""
    trigger: Dict[str, Any] = field(default_factory=dict)
    link: str = ""  # optional passage to open on click (PornCenter "watch")


@dataclass
class TemplatePhone:
    enabled: bool = True
    apps: List[TemplatePhoneApp] = field(default_factory=list)
    conversations: List[TemplatePhoneConversation] = field(default_factory=list)
    posts: List[TemplatePhonePost] = field(default_factory=list)
    profiles: List[TemplatePhoneProfile] = field(default_factory=list)
    daily_topics: List[TemplatePhoneDailyTopic] = field(default_factory=list)
    gallery_items: List[TemplatePhoneGalleryItem] = field(default_factory=list)
    # doc 45 G11 — when set, the sidebar phone button shows only once this
    # player flag is true (the phone is "acquired" in-world). "" = always shown.
    purchase_flag: str = ""


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
    # Narrative person — which grammatical person the game's prose is written in.
    # The engine labels the player's own dialogue/thought blocks to match: a game
    # narrated in third person would otherwise render "You:" over prose saying "she".
    # "second" (default, RTS-native) | "first" | "third".
    narration_person: str = "second"
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
    # Symbol the RentDay pages print in front of an amount. Defaults to "$" because
    # that is what those pages hardcoded before this field existed — a game shipped
    # with every price in the prose written "£3" and its rent page saying "$245".
    rent_currency_symbol: str = "$"
    # Sidebar items (custom display elements)
    sidebar_items: List[Dict[str, Any]] = field(default_factory=list)
    # Phone system
    phone_enabled: bool = False
    phone: Optional[TemplatePhone] = None
    # Recurring passes (gym, bus, etc.)
    passes: List[TemplatePass] = field(default_factory=list)
    # doc 45 G4 — quests (story objectives with steps + journal)
    quests: List["TemplateQuest"] = field(default_factory=list)
    # PRD 48 — Quests Engine V2 cards. Populated only when project.quests_engine
    # == "v2". Empty list for V1 games (which keep using story_arc.hints.templates).
    quests_cards: List["QuestsCard"] = field(default_factory=list)
    # doc 45 G7 — optional corruption tier thresholds (default [0,5,15,30,45])
    corruption_tiers: Optional[List[int]] = None
    # doc 45 G9 — economy: fast jobs + bank
    fast_jobs: List["TemplateFastJob"] = field(default_factory=list)
    bank: Optional["TemplateBank"] = None
    # State-reactive player portrait (opt-in) — sidebar image reacts to outfit/undress/corruption/pregnancy
    player_portrait: Optional["TemplatePlayerPortrait"] = None
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
    # Pattern 2 (2026-05-01): label registries — map internal trait/flag names
    # to player-facing labels used by setup.computeHintGoal when auto-rendering
    # the 🎯 goal block. Authored under [[traits.labels]] / [[flags.labels]].
    trait_labels: List["TemplateTraitLabel"] = field(default_factory=list)
    flag_labels: List["TemplateFlagLabel"] = field(default_factory=list)
    # Tips page — game-level mechanics surface (decay rates, time costs, what
    # affects diner tips, etc.). Authored under [ui.tips_page] in TOML. None
    # = page + sidebar button not emitted; runtime-conditional.
    tips_page: Optional["TemplateTipsPage"] = None
    # Cast page — the who-is-who surface. Authored under [ui.cast_page]. None =
    # page + sidebar button not emitted. Carries no authored content: the roster
    # is derived from [[npcs]] and the quest cards at runtime.
    cast_page: Optional["TemplateCastPage"] = None
    # Player cheat page — authored under [ui.cheat_page]. None = page + sidebar
    # button not emitted. One build ships everywhere: every row is emitted live but
    # wrapped in a check on its own unlock flag, which the player sets by entering
    # that row's code. The codes are never in this file (see parse_template).
    cheat_page: Optional["TemplateCheatPage"] = None
    # Doc 69 Item 3 — parse-time errors collected during normalize() for the
    # field-name mismatch validator. validate() prepends these to its own
    # error list. Populated only by normalize(); never mutated downstream.
    # Empty list = no parse-time errors detected.
    _parse_errors: List[str] = field(default_factory=list)
    # Raw [[ui.cheat_page.grants]] dicts as authored, carried through so validate()
    # can run the shared effect validators against the ORIGINAL keys — the
    # normalized dataclass has already discarded a misspelled field name.
    _cheat_raw_rows: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class TemplateTraitLabel:
    """Player-facing label for a trait key (Pattern 2).

    Used by setup.computeHintGoal to render gates as
    '◯ <Label> <op> <value> (<currentValue>)' instead of the raw trait_key.
    For NPC-subject traits, the renderer prepends the NPC name.
    """
    key: str
    label: str
    verb: str = "reach"   # framing word: "reach trust ≥ 15" / "do Bookkeeping ×3"
    unit: str = ""        # optional unit noun for counter pluralization
    hidden: bool = False  # when True, hide this trait from ALL player-facing trait dumps
                          # (playerTraits widget + Stats page, dev AND non-dev). For
                          # internal traits — <slug>_stage, pregnancy, antagonist awareness.
                          # A label entry may exist SOLELY to hide (label may be empty).
                          # NOTE: name-keyed, not namespaced — hides for player + any NPC
                          # that has a core_trait of this name.


@dataclass
class TemplateFlagLabel:
    """Player-facing label for a flag key (Pattern 2)."""
    key: str
    label: str


@dataclass
class TemplateTipsPage:
    """Content for the standalone :: TipsPage passage. Universal game mechanics
    that would otherwise be repeated as per-template tips on every quest card
    live here instead. Engine prints `content` verbatim into the passage —
    author writes raw HTML so formatting is predictable without a markdown pass.
    """
    title: str = "Tips"
    content: str = ""


@dataclass
class TemplateCastPage:
    """The [ui.cast_page] surface: a sidebar button plus a standalone passage
    listing the people the player has met — who they are to her, where they are
    right now, and what advances them.

    NO CONTENT IS AUTHORED HERE. The page draws entirely from data the game
    already carries: `relationship` off [[npcs]], live presence off
    setup.getNpcLocation, and the next-step block off the character's own quest
    card. Presence of the block IS the opt-in; the fields below are chrome.

    WHO APPEARS is the quest cards' decision, not this block's. A character is
    listed exactly when setup.pickQuestsCard returns a card for them, so the
    meeting flag on their cards gates the guidance page and this page together
    and the two cannot fall out of step. Measured field practice: 17 of 25
    shipped sandboxes carry a page like this, and 7 of the 8 parsed top-ten do.
    """
    title: str = "The Cast"
    intro: str = ""
    button_label: str = ""    # defaults to title
    button_icon: str = ""


@dataclass
class TemplateCheatGrant:
    """One row on the player cheat page — a single trait write, nothing else.

    Field names deliberately mirror the choice-effect schema
    (targetType/npcId/trait/op/value/clamp/cap) so a raw row dict can be fed to
    the existing effect validators for free.

    NOTHING here reaches a player who has not entered this row's code. The whole
    row — label, hint, button text — is emitted inside a check on the row's unlock
    flag, so a locked row renders no bytes at all. That is why `id` is required and
    explicit rather than derived from `label`: the id is the flag key and the key
    into the codes file, and renaming a label must not orphan a player's unlock.

    `clamp` defaults True here (unlike the choice path, which passes an explicit
    False when omitted) because this page emits its own calls and a banded meter
    must never escape its bands. An unbounded resource — money, coin — must set
    `clamp = false`, or the engine's hardcoded 0-100 clamp silently caps a wallet
    at 100.
    """
    id: str
    label: str
    trait: str
    value: float
    targetType: str = "player"
    npcId: str = ""
    op: str = "add"
    cap: Optional[float] = None
    clamp: bool = True
    hint: str = ""
    button_text: str = ""     # default composed from label + op + value
    at_cap_text: str = ""


@dataclass
class TemplateCheatPage:
    """The [ui.cheat_page] surface: a sidebar button plus a standalone passage.

    Unlike TemplateTipsPage this is NOT dropped when empty — an authored-but-empty
    block is a validate() error. The tips_page silent drop is the documented cause
    of a game shipping with its 💡 button permanently absent.

    One build ships everywhere. A player who has entered no code sees the title, the
    intro, the join block and an empty code box — no row names, no numbers, no hints.
    `join_note` and `join_url` are that page's only advertising, so they are required
    (the url falls back to [project] support_url).
    """
    title: str = "Cheats"
    intro: str = ""
    button_label: str = ""    # defaults to title
    button_icon: str = ""
    join_note: str = ""       # the one line telling a free player what the box is for
    join_url: str = ""        # defaults to [project] support_url at emission
    grants: List["TemplateCheatGrant"] = field(default_factory=list)


@dataclass
class TemplateDailyTick:
    """Effects that fire once per in-game day at advanceDay() rollover.

    `flagEffects` clear/set daily-cooldown flags (silent, via applyFlagEffect).
    `traitEffects` (doc 40) apply trait deltas each day via applyAndNotifyTrait —
    this is the RTS arousal "daily auto-rise": e.g. player arousal +1 (cap 10),
    NPC arousal +1 (cap 3). Each entry reuses the choice-effect shape
    (targetType/npcId/trait/op/value/clamp/cap).
    """
    flagEffects: List[TemplateFlagEffect] = field(default_factory=list)
    traitEffects: List[TemplateChoiceEffect] = field(default_factory=list)


@dataclass
class TemplateStageHelper:
    """Named composite gate. Recipe of conditions referenced by name.

    Helpers reference primitive condition types only — recursion (helper
    references helper) is rejected at validate() time. Single-level lookup
    in runtime keeps cycle risk zero.

    `dev_only` (Pattern 2 v2.2, 2026-05-04): silences the flag-setter-
    coverage validator warning. Set to True when a helper intentionally
    references a flag that has no canonical canvas setter — i.e., the
    next stage is reachable only via dev shortcuts in the current scope.
    See template_import.py validate() block for the check.
    """
    name: str
    description: str = ""
    conditions: Dict[str, Any] = field(default_factory=dict)
    dev_only: bool = False


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
    # E21 — opt-in: when this canvas is filtered out by an unmet condition
    # (e.g., daily-cooldown flag), render a grayed-out entry on QuestsPage
    # explaining when it will be available again. Default off (silent filter).
    show_when_blocked: bool = False
    cooldown_message: Optional[str] = None  # custom text; falls back to a generic message
    # Lane 2 anti-toggle cooldown (L2-2 doctrine fix, 2026-05-12).
    # When non-empty, this canvas only fires if the player entered the current
    # location from one of these locations. Empty list = fire on any entry.
    # Build resolves slugs → runtime passage names at help_data emission.
    # NAMING: chose `entry_only_from` to avoid collision with Location.entry_from
    # (the location-hierarchy parent field used by back-navigation).
    entry_only_from: List[str] = field(default_factory=list)
    # Lane 3 dispatcher substitution rules (PRD 25 §4.1).
    # Each rule shape:
    #   { "target_canvas_id": str, "chance": float, "conditions": Optional[Dict] }
    # Author writes target_canvas_id as a slug (matches canvas.id in TOML);
    # the generator resolves slug→UUID at engine emission time.
    # When non-empty, the canvas's body is preceded by a substitution check —
    # if any rule matches (target valid + conditions pass + dice hit), the
    # target canvas plays in place of the parent.
    substitutions: List[Dict[str, Any]] = field(default_factory=list)
    # When True, this canvas is excluded from renderNpcPortraits +
    # renderSoloActivities + selectAutoFireCanvasForLocation (PRD 25 §5.5).
    # Reachable ONLY as the target of another canvas's substitution rule.
    substitution_only: bool = False
    # Lane 2/3 NPC-presence gate (Phase A, 2026-05-14). The named NPC must be
    # co-located with the player per their declared [[npcs.schedules]].
    #
    # ⚠️ THIS GATES TWO PATHS AND ONLY TWO. `requiresNpc` is read in exactly
    #    setup.checkRandomEncounters (v2.py:5245) — Lane 2 random ambients,
    #    trigger_mode = "random" — and setup.checkAndSubstituteCanvas
    #    (v2.py:5318) — Lane 3 substitution targets, substitution_only = true.
    #    On EVERY other path it does nothing at all. An auto-firing canvas is
    #    selected by selectAutoFireCanvasForLocation -> isCanvasValid
    #    (v2.py:4559), which reads schedules, conditions and repeatability and
    #    never looks at this field; isCanvasValidForSelection (v2.py:4584) is
    #    the same. So on a one-shot meeting canvas, `trigger.schedules` is what
    #    stops it firing in an empty room, and this field is documentation.
    #
    #    An earlier version of this comment said requires_npc "lets authors drop
    #    per-canvas location+time gates", with no scope on the claim. A game was
    #    then authored with five meeting canvases and no windows, and its
    #    introductions played to rooms the characters were not in — one of them
    #    at 06:10 on a Saturday, saying "it's Monday". The skill said the right
    #    thing the whole time (the-first-hour.md F5); this file did not, and this
    #    file is what an author reads while writing TOML.
    #
    # Back-compat: canvases carrying both keep working — the two AND together.
    requires_npc: Optional[str] = None
    # Doc 69 Item 2 (2026-05-27) — Pattern C `pre_substitution_effects`.
    # Effects that run UNCONDITIONALLY at canvas entry, BEFORE the Lane 3
    # substitution check. If a substitution rule preempts via <<goto>>, these
    # effects have already executed — the activity "counts" even when an NPC
    # walks in. Each entry uses the same shape as a regular trait effect
    # (targetType / npcId / trait / op / value / clamp / cap). Empty list =
    # current behavior unchanged (Pattern A semantics). See Doc 69 §4 + §5.2.
    pre_substitution_effects: List[Dict[str, Any]] = field(default_factory=list)


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
    # Optional condition gate (doc 45 G6). When set on a [engine.daily_tick]
    # effect, the effect applies on day rollover ONLY if these conditions are
    # satisfied. Standard {version, logic, items} block. None ⇒ unconditional
    # (today's behavior).
    conditions: Optional[Dict[str, Any]] = None


@dataclass
class TemplateFlagEffect:
    targetType: str = "player"  # 'player'|'npc'
    npcId: Optional[str] = None
    flag: str = ""
    op: str = "set"  # 'set'|'unset'|'toggle' — runtime defaults to set when unrecognized
    # Optional condition gate (doc 45 G6) — see TemplateChoiceEffect.conditions.
    conditions: Optional[Dict[str, Any]] = None


@dataclass
class TemplateModifierEffect:
    key: str = ""  # modifier identifier (e.g., "tipsy")
    name: str = ""  # display name (e.g., "Tipsy")
    duration_hours: int = 1  # how long it lasts in game hours
    trait_offsets: Dict[str, float] = field(default_factory=dict)  # {trait: offset} for condition checks


@dataclass
class TemplateQuest:
    """doc 45 G4 — a quest with ordered steps. Each `steps[i]` is the journal
    text for step i. Driven by `questEffects` on choices (start/update/cancel/
    complete) and read by the `quest` condition type + the Quests phone app."""
    id: str = ""
    name: str = ""
    steps: List[str] = field(default_factory=list)
    repeatable: bool = False


@dataclass
class TemplateFastJob:
    """doc 45 G9 — a repeatable money job. Worked from the Fast Jobs phone app."""
    id: str = ""
    name: str = ""
    income: int = 0
    xp_req: int = 0          # fast-jobs XP needed to unlock
    cooldown_days: int = 0   # days locked after working it
    time_period: str = ""    # optional game.time gate (e.g. "M","A")
    money_trait: str = "money"


@dataclass
class TemplateBank:
    """doc 45 G9 — savings account: deposit/withdraw + daily interest."""
    enabled: bool = False
    interest_rate: float = 0.01
    money_trait: str = "money"


@dataclass
class TemplatePlayerPortraitOutfit:
    """One outfit rule for the state-reactive portrait: `image` shown when `when` matches.
    `when` = { worn_type?, corruption?: {operator, value(LEVEL 0-4)}, flag? } — first-match wins."""
    image: str = ""
    when: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TemplatePlayerPortrait:
    """State-reactive sidebar portrait (opt-in). setup.getPlayerPortrait() resolves in priority:
    undress-override (naked/topless/bottomless/underwear, only when clothing_enabled) ->
    outfit rule (dominant-slot type + corruption/flag) -> Preg suffix. Off unless `[player_portrait]`
    with enabled=true is authored."""
    enabled: bool = False
    naked_image: str = ""
    topless_image: str = ""
    bottomless_image: str = ""
    underwear_image: str = ""
    default_image: str = ""
    pregnancy_trait: str = ""
    pregnancy_suffix: str = "Preg"
    outfits: List["TemplatePlayerPortraitOutfit"] = field(default_factory=list)


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
    # S4 (2026-05-06) — RTS-style threshold notification on locked-choice click.
    # When set + show_when_locked=True (Mode A — greyed-out, no rejection node),
    # clicking the locked choice fires a warning toast publishing the threshold
    # in-character. e.g., "I'd need to know him better — at least 15 trust."
    # Mirrors RTS <<NotifyCorruption N>> pattern (doc 13 §7.4 + doc 22 §11).
    locked_text_threshold: str = ""
    rejection_node: Optional[str] = None  # Node to redirect to on rejection (clickable even locked)
    rejection_effects: List[TemplateChoiceEffect] = field(default_factory=list)  # Effects on rejection
    # Temporary modifier system: apply short-lived trait offsets to condition checks
    modifier_effects: List[TemplateModifierEffect] = field(default_factory=list)
    # Recurring pass system: purchase time-limited passes
    pass_effects: List[Dict[str, str]] = field(default_factory=list)
    # Inventory system: add/remove consumable items
    item_effects: List[Dict[str, Any]] = field(default_factory=list)
    # doc 45 G4: quest mutations — [{quest, op:start|update|cancel|complete, step?}]
    quest_effects: List[Dict[str, Any]] = field(default_factory=list)
    # doc 45 G5: scheduled (delayed) events — [{delayDays, action, flag?/quest?/conversation?}]
    schedule_effects: List[Dict[str, Any]] = field(default_factory=list)
    # E6: per-choice text variants — first match wins, falls back to `text`.
    # Each variant: {"text": str, "conditions": {version, items}}.
    text_variants: List[Dict[str, Any]] = field(default_factory=list)
    # Per-choice resource costs — [{trait: str, value: int}]. The energy/hygiene TIER under
    # the choice's `conditions` (main lock): checked via checkCostsAffordable, deducted on
    # click, and shown as a greyed getCostBlockedMessage rung when unaffordable. Mirrors the
    # canvas-level `costs` semantic (TemplateTrigger.costs) at the choice level.
    costs: List[Dict[str, Any]] = field(default_factory=list)


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
    # E10: stage gate. All three required together; tri-required validation
    # in validate(). The triple is normalized at create_project_from_template
    # time into a regular trait condition on $player.core_traits[<slug>_stage]
    # so the runtime evaluator (setup.checkSingleCondition) handles it
    # without a new branch.
    stage_npc: Optional[str] = None         # NPC slug; must reference an NPC with arc_stages
    stage_op: Optional[str] = None          # 'eq' | 'gte' | 'lte'
    stage_value: Optional[int] = None       # 0..len(arc_stages)-1
    # E14 — list of additional trait/flag predicates AND-combined with stage gate.
    # Each item is a normalized condition_item dict matching the engine's
    # checkSingleCondition shape (type/subject/operator/...). Lets authors
    # express "stage 0 AND trust >= 10 AND group_settled_in is_false" precisely.
    trait_checks: List[Dict[str, Any]] = field(default_factory=list)
    # E22 — cross-NPC stage prerequisite. Format: "npc_<slug> <op> <int>"
    # e.g., "npc_frank >= 2". Parsed at serialization into a trait condition_item
    # on $player.core_traits[<slug>_stage]. Lets a hint document why an arc is
    # locked behind another NPC's progress.
    prerequisite_npc_stage: Optional[str] = None


@dataclass
class TemplateHintTemplate:
    """A hint template with conditions."""

    condition: Optional[TemplateHintCondition] = None
    text: str = ""
    # E10: routing field — which NPC's section this hint belongs to in the
    # Quests page. When stage_npc is set on the condition, npc_id defaults
    # to it; otherwise authors set npc_id explicitly to scope the hint.
    npc_id: Optional[str] = None
    # Picker priority — higher wins. Default 0. Use to flag crisis / pressure
    # variants that should override an ambient line of equal specificity.
    # See picker rule in v1.py:setup.getStageHintForNPC.
    priority: int = 0
    # Pattern 2 (2026-05-01): optional player-facing tip rendered as 💡 line
    # below the auto-rendered goal block. Used for strategic advice that
    # doesn't fit structured gate data ("Trust decays 1.0/day if ignored").
    tip: Optional[str] = None
    # Pattern 2: when true (default), engine auto-renders the 🎯 goal block
    # from the helper conditions or canvas trigger conditions. When false,
    # engine treats `text` as fully authored (legacy behavior).
    auto_goal: bool = True
    # E17 (2026-05-06) — author-supplied override for the ready-frame text
    # (the line shown when the next-stage helper has cleared but the stage
    # trait hasn't advanced yet). Replaces the engine default
    # ("All gates cleared. Visit X to seal the moment.") with in-character
    # prose. Empty string = use engine default. Per-NPC-per-stage author
    # control over the player-facing "ready" surface.
    ready_text: str = ""
    # 2026-05-09 — terminal-stage badge. When true, the engine renders a
    # "✓ Arc complete" frame in the goal block instead of trying to surface
    # a non-existent next-stage helper. Author opt-in: set true on the hint
    # template for the highest defined stage of an NPC's slice. Bypasses
    # auto_goal=false suppression so closure displays even on terminal
    # stages whose author left auto_goal=false.
    arc_complete: bool = False
    # 2026-05-10 — terminal-stage flag-based closure target. When set,
    # computeHintGoal looks up the named flag's setter canvas via
    # _findFlagSetterCanvas and renders a Ready frame (📍 + 🕒) so the
    # player knows where/when to consummate the arc. Once the flag flips
    # true, engine renders the ✓ Arc complete badge instead. Mutex with
    # arc_complete=true (which renders the badge unconditionally). Author
    # pattern: pair arc_closure_flag (pre) + arc_complete=true (post)
    # templates gated by trait_checks on the same flag (is_false / is_true).
    arc_closure_flag: str = ""


# ─── PRD 48: Quests Engine V2 ───────────────────────────────────────────────
# New schema replacing [[story_arc.hints.templates]]. Authors write one card
# per state-window per arc; the picker swaps cards as state crosses. Each
# card carries everything the renderer needs — no helper indirection, no
# transition canvases, no label registry. See docs 47 + 48.


@dataclass
class QuestsCondition:
    """A single condition item used in QuestsCard.when (routing) and
    QuestsCard.goals (progress bullets). Flat shape — flag XOR trait, not
    both. `label` only required on goals items targeting traits/counters
    (it's what renders next to each ◯ bullet)."""

    # Flag gate: set `flag` + `op` ("is_true" | "is_false"). `label` optional.
    flag: Optional[str] = None
    # Trait / counter gate: set `trait`, `subject` ("player" | "npc"), `op`
    # ("gte" | "lte" | "gt" | "lt" | "eq"), `value`, and `label`.
    # When subject == "npc", `npc_id` is required.
    trait: Optional[str] = None
    subject: Optional[str] = None
    npc_id: Optional[str] = None
    op: str = ""
    value: Optional[float] = None
    label: Optional[str] = None


@dataclass
class QuestsCard:
    """A single Quests page card.

    Routes to a section by presence/absence of `npc_id`:
      - npc_id set → renders in that NPC's section (one card per NPC per render)
      - npc_id absent → renders in the top "Story Goals" section (multiple cards)

    The engine picks the winning card per scope by walking `when` against
    current state, sorting matches by (priority desc, when.length desc,
    file-order asc). Story Goals additionally group by optional `group` key.
    """

    text: str = ""
    ready_text: Optional[str] = None
    tip: Optional[str] = None
    npc_id: Optional[str] = None
    priority: int = 0
    # Story Goal only — cards sharing a group value collapse to one (highest
    # priority match wins). Lets authors write crisis variants of the same
    # goal. Ignored on NPC cards (validator warns).
    group: Optional[str] = None
    # Routing — ALL items must evaluate true for this card to win the picker.
    when: List[QuestsCondition] = field(default_factory=list)
    # The 🎯 To advance bullets. Each item renders as ◯ <label> — X / Y.
    # When goals is empty, the card has no climbing phase (goalState.allMet
    # is vacuously true).
    goals: List[QuestsCondition] = field(default_factory=list)
    # When all goals met AND ready_canvas is set, the renderer emits a
    # 🔓 Ready frame with 📍 + 🕒 pulled from the named canvas's metadata
    # (location + first schedule entry). Optional — pure-mechanic cards
    # leave this unset.
    ready_canvas: Optional[str] = None
    # Terminal — when true AND when matches, renderer emits ✓ Arc complete
    # regardless of goals/ready_canvas. Author opt-in for the final card in
    # an arc.
    terminal: bool = False
    # Overrides the terminal frame's "Arc complete" label. Only renders when
    # `terminal` is also true (the validator warns if it isn't). Exists because
    # a finished NPC arc and a finished BUILD are different endings and the
    # hardcoded label can only say the first: the card that ends a release has
    # to be able to say so, e.g. "Chapter complete — the story continues in
    # the next release".
    terminal_text: Optional[str] = None


def _parse_quests_condition(d: Dict[str, Any]) -> QuestsCondition:
    """Parse a single condition item from a card's `when` or `goals` list."""
    flag = d.get("flag")
    trait = d.get("trait")
    # Coerce stray empty strings to None so the validator sees a clean shape.
    if not flag:
        flag = None
    if not trait:
        trait = None
    subject = d.get("subject") or None
    npc_id = d.get("npc_id") or None
    op = str(d.get("op", "") or "")
    raw_value = d.get("value")
    value: Optional[float] = None
    if raw_value is not None:
        try:
            value = float(raw_value)
        except (TypeError, ValueError):
            # Validator will catch this with a clear error.
            value = None
    label = d.get("label") or None
    return QuestsCondition(
        flag=flag,
        trait=trait,
        subject=subject,
        npc_id=npc_id,
        op=op,
        value=value,
        label=label,
    )


def _parse_quests_card(d: Dict[str, Any]) -> QuestsCard:
    """Parse one [[quest_cards]] entry into a QuestsCard."""
    when_items = [
        _parse_quests_condition(item)
        for item in (d.get("when") or [])
        if isinstance(item, dict)
    ]
    goals_items = [
        _parse_quests_condition(item)
        for item in (d.get("goals") or [])
        if isinstance(item, dict)
    ]
    priority_raw = d.get("priority", 0)
    try:
        priority = int(priority_raw) if priority_raw is not None else 0
    except (TypeError, ValueError):
        priority = 0
    terminal_raw = d.get("terminal", False)
    terminal = bool(terminal_raw) if isinstance(terminal_raw, bool) else False
    return QuestsCard(
        text=_require_str(d, "text", ""),
        ready_text=_require_str(d, "ready_text", "") or None,
        tip=_require_str(d, "tip", "") or None,
        npc_id=_require_str(d, "npc_id", "") or None,
        priority=priority,
        group=_require_str(d, "group", "") or None,
        when=when_items,
        goals=goals_items,
        ready_canvas=_require_str(d, "ready_canvas", "") or None,
        terminal=terminal,
        terminal_text=_require_str(d, "terminal_text", "") or None,
    )


@dataclass
class TemplateStoryHints:
    """Hint configuration for story journal."""

    stuck_threshold_minutes: int = 30
    hint_style: str = "observation"  # observation|suggestion|memory
    templates: List[TemplateHintTemplate] = field(default_factory=list)
    # E9 — stage-stall detection threshold + custom hint message.
    # When no NPC with arc_stages has had its <slug>_stage trait advance
    # in this many in-game days, the engine flags position.stage_progression_stalled
    # and surfaces the stall hint via generateNarrativeHint.
    stuck_threshold_days: int = 7
    # Author-customized stall hint text. Empty string falls back to the
    # generic "Days are slipping past. Something needs to shift." default.
    stage_stall_message: str = ""


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


# Doc 69 Item 3 — Field-name mismatch validators.
# Effect schema (TemplateChoiceEffect/TemplateFlagEffect) uses field names:
#   targetType / npcId / trait / flag / op
# Predicate schema (triggerConditionsSatisfied items) uses field names:
#   subject / npc_id / trait_key / flag_key / operator + type
# Mixing them causes silent no-op at runtime (e.g., `_require_str(e, "trait", "")`
# returns empty string when the dict only has `trait_key`). Doc 68 §7.6 is the
# doctrine reference card; these validators convert it to build-time enforcement.

# Predicate-context field names that MUST NOT appear in effect blocks.
# Maps wrong-field → (correct-field, source-context-name).
_EFFECT_FORBIDDEN_FIELDS: Dict[str, str] = {
    "subject": "targetType",
    "trait_key": "trait",
    "flag_key": "flag",
    "npc_id": "npcId",
    "operator": "op",
}

# Effect-context field names that MUST NOT appear in predicate items.
# Maps wrong-field → (correct-field, source-context-name).
_PREDICATE_FORBIDDEN_FIELDS: Dict[str, str] = {
    "targetType": "subject",
    "npcId": "npc_id",
}


def _validate_effect_field_names(raw_eff: Dict[str, Any], ctx: str) -> List[str]:
    """Validate that an effect dict does NOT use predicate-context field names.

    Returns a list of error messages (empty if clean). Doc 68 §7.6 + Doc 69 §5.3.
    Callers should append the returned errors to their accumulating errors list.
    """
    if not isinstance(raw_eff, dict):
        return []
    errors: List[str] = []
    for wrong_field, right_field in _EFFECT_FORBIDDEN_FIELDS.items():
        if wrong_field in raw_eff:
            val = raw_eff[wrong_field]
            errors.append(
                f"{ctx}: field `{wrong_field}` is not allowed in an effect block "
                f"(use `{right_field}` instead — predicate-syntax field mixed into "
                f"effect context). See Doc 68 §7.6 field-name reference card. "
                f"Field appeared with value: {val!r}."
            )
    return errors


def _validate_predicate_field_names(raw_item: Dict[str, Any], ctx: str) -> List[str]:
    """Validate that a predicate item dict does NOT use effect-context field names.

    Returns a list of error messages (empty if clean). Doc 68 §7.6 + Doc 69 §5.3.
    Conditionally bans `trait` (when type=trait), `flag` (when type=flag), and
    `op` (always — predicate uses `operator`).
    """
    if not isinstance(raw_item, dict):
        return []
    errors: List[str] = []
    # Unconditional bans (these effect-only fields are never valid in predicates).
    for wrong_field, right_field in _PREDICATE_FORBIDDEN_FIELDS.items():
        if wrong_field in raw_item:
            val = raw_item[wrong_field]
            errors.append(
                f"{ctx}: field `{wrong_field}` is not allowed in a predicate item "
                f"(use `{right_field}` instead — effect-syntax field mixed into "
                f"condition context). See Doc 68 §7.6 field-name reference card. "
                f"Field appeared with value: {val!r}."
            )
    # Conditional bans based on predicate `type`.
    item_type = raw_item.get("type")
    if item_type == "trait" and "trait" in raw_item:
        errors.append(
            f"{ctx}: field `trait` is not allowed in a predicate item with "
            f"`type = 'trait'` (use `trait_key` instead). See Doc 68 §7.6. "
            f"Field appeared with value: {raw_item['trait']!r}."
        )
    if item_type == "flag" and "flag" in raw_item:
        errors.append(
            f"{ctx}: field `flag` is not allowed in a predicate item with "
            f"`type = 'flag'` (use `flag_key` instead). See Doc 68 §7.6. "
            f"Field appeared with value: {raw_item['flag']!r}."
        )
    if "op" in raw_item:
        errors.append(
            f"{ctx}: field `op` is not allowed in a predicate item "
            f"(use `operator` instead — `op` is the effect-context name). "
            f"See Doc 68 §7.6. Field appeared with value: {raw_item['op']!r}."
        )
    return errors


def _validate_predicate_items_block(
    cond_block: Any, ctx: str
) -> List[str]:
    """Walk a `{version, logic, items: [...]}` condition block and validate
    field names of each item. No-op for empty/missing blocks.

    Used by validate() at each place predicates are stored (canvas trigger
    conditions, choice conditions, exit_block conditions, daily_tick effect
    conditions, etc.). Returns flat list of error messages.
    """
    if not isinstance(cond_block, dict):
        return []
    items = cond_block.get("items")
    if not isinstance(items, list):
        return []
    errors: List[str] = []
    for ii, item in enumerate(items):
        errors.extend(_validate_predicate_field_names(item, f"{ctx}.items[{ii}]"))
    return errors


# Doc 72 — `worn_type` predicate validator. Soft typo-catch: if a condition
# references `worn_type == "X"` but no clothing item declares `type = "X"`,
# emit a WARN naming the bad value. Plus an info note if `X` is outside the
# RECOMMENDED_CLOTHING_TYPES set (uncommon type — confirm intentional). Never
# errors — build proceeds.

def _validate_worn_type_items_block(
    cond_block: Any, ctx: str, known_types: set, recommended_types: set
) -> List[str]:
    """Walk a `{version, logic, items: [...]}` condition block and validate
    `worn_type` predicate values against the catalog's declared `type` set.
    Returns flat list of warning messages."""
    if not isinstance(cond_block, dict):
        return []
    items = cond_block.get("items")
    if not isinstance(items, list):
        return []
    warnings: List[str] = []
    for ii, item in enumerate(items):
        if not isinstance(item, dict):
            continue
        if item.get("type") != "worn_type":
            continue
        value = item.get("value", "")
        if not isinstance(value, str) or not value:
            continue
        item_ctx = f"{ctx}.items[{ii}]"
        if value not in known_types:
            warnings.append(
                f"WARN: {item_ctx} worn_type references '{value}' but no clothing "
                f"item declares type='{value}'. Possible typo. (Doc 72)"
            )
        elif value not in recommended_types:
            warnings.append(
                f"INFO: {item_ctx} worn_type uses uncommon type '{value}' — "
                f"confirm intentional. Recommended: {sorted(recommended_types)}. (Doc 72)"
            )
    return warnings


# Doc 69 Item 4 — Undeclared trait validator.
# Each player + NPC trait referenced in any effect or condition MUST be
# pre-declared in the corresponding `core_traits` block. Engine reads
# undefined → silent runtime misbehavior (per v2.py:3370, v2.py:5065).
# Doc 68 §2.5 is the doctrine reference; this validator enforces it at build
# time.
#
# Stage trait special case (Doc 69 §6.3 #4 + Doc 68 §9):
#   Stage is stored on the player namespace as `<slug>_stage` (e.g.,
#   `frank_stage`). The matching NPC must have `arc_stages` declared.
#   - declared in [player.core_traits] + NPC has arc_stages → OK
#   - matches stage pattern + NPC has arc_stages but NOT declared → ERROR
#   - declared in [player.core_traits] but NPC has no arc_stages → WARN
#   - matches stage pattern + no matching NPC → treated as ordinary
#     player trait (must be declared in [player.core_traits])

import re as _re_for_stage_pattern
_STAGE_TRAIT_PATTERN = _re_for_stage_pattern.compile(r"^([a-z0-9_]+)_stage$")


def _build_trait_registries(
    player_core_traits: Optional[Dict[str, Any]],
    npcs_list: Optional[List["TemplateNPC"]],
) -> Dict[str, Any]:
    """Build lookup tables of declared traits.

    Returns a dict with:
      - 'player': set of declared player trait keys
      - 'npc_by_slug': dict mapping NPC slug → set of declared NPC trait keys
      - 'npc_arc_stages': dict mapping NPC slug → list of arc_stage names
        (empty list if NPC has no arc_stages declared, missing key if no
        such NPC exists)

    Accepts player core_traits dict + npcs list rather than a full
    GameTemplate so it can be called both inside normalize() (before the
    template is constructed) and inside validate() (with a parsed template).
    """
    player_keys = set((player_core_traits or {}).keys())
    npc_by_slug: Dict[str, Set[str]] = {}
    npc_arc_stages: Dict[str, List[str]] = {}
    for n in npcs_list or []:
        npc_by_slug[n.id] = set((n.core_traits or {}).keys())
        npc_arc_stages[n.id] = list(n.arc_stages or [])
    return {
        "player": player_keys,
        "npc_by_slug": npc_by_slug,
        "npc_arc_stages": npc_arc_stages,
    }


def _classify_stage_trait(
    trait_name: str, registries: Dict[str, Any]
) -> Optional[str]:
    """Classify a trait name against the stage-pattern. Returns:
      - 'stage_with_arc' — trait matches `<slug>_stage` AND the slug
        corresponds to an existing NPC with non-empty arc_stages
      - 'stage_without_arc' — matches pattern, NPC exists but arc_stages empty
      - 'stage_unknown_npc' — matches pattern but no such NPC slug
      - None — does not match stage pattern at all
    """
    m = _STAGE_TRAIT_PATTERN.match(trait_name)
    if not m:
        return None
    slug = m.group(1)
    arc_stages_by_npc = registries.get("npc_arc_stages") or {}
    if slug not in arc_stages_by_npc:
        return "stage_unknown_npc"
    if arc_stages_by_npc[slug]:
        return "stage_with_arc"
    return "stage_without_arc"


def _validate_trait_declaration_in_effect(
    raw_eff: Dict[str, Any],
    registries: Dict[str, Any],
    ctx: str,
) -> Tuple[List[str], List[str]]:
    """Validate that an effect's `trait` field references a declared trait.

    Returns (errors, warnings). Doc 69 §6.3.
    """
    if not isinstance(raw_eff, dict):
        return [], []
    errors: List[str] = []
    warnings_out: List[str] = []
    # Only validate trait effects — flag effects use a separate field-name path.
    trait_name = raw_eff.get("trait")
    if not trait_name or not isinstance(trait_name, str):
        return [], []
    target = str(raw_eff.get("targetType", "player"))
    if target == "player":
        player_keys = registries.get("player") or set()
        if trait_name in player_keys:
            # Declared. If it looks like a stage trait, check that the
            # corresponding NPC has arc_stages declared (WARN otherwise).
            stage_kind = _classify_stage_trait(trait_name, registries)
            if stage_kind == "stage_without_arc":
                warnings_out.append(
                    f"{ctx}: trait `{trait_name}` matches stage pattern `<slug>_stage` "
                    f"and IS declared in [player.core_traits], but the corresponding "
                    f"NPC has an empty `arc_stages` list. Stage trait exists with no arc "
                    f"to advance through — likely an authoring oversight. See Doc 68 §9.0."
                )
            return errors, warnings_out
        # Not declared. If it looks like a stage trait + the NPC exists,
        # emit a stage-pattern hint; otherwise standard undeclared error.
        stage_kind = _classify_stage_trait(trait_name, registries)
        if stage_kind == "stage_with_arc":
            slug = _STAGE_TRAIT_PATTERN.match(trait_name).group(1)
            errors.append(
                f"{ctx}: effect references stage trait `{trait_name}` "
                f"(matches `<slug>_stage` pattern + NPC '{slug}' has arc_stages "
                f"declared), but `{trait_name}` is NOT declared in "
                f"[player.core_traits]. Declare it with initial value 0. "
                f"See Doc 68 §2.5 + §9.0."
            )
        elif stage_kind == "stage_unknown_npc":
            errors.append(
                f"{ctx}: effect references undeclared player trait `{trait_name}` "
                f"(name matches `<slug>_stage` pattern but no NPC has slug matching "
                f"its prefix). Declare it in [player.core_traits] block with an "
                f"initial value. See Doc 68 §2.5."
            )
        else:
            errors.append(
                f"{ctx}: effect references undeclared player trait `{trait_name}`. "
                f"Declare it in [player.core_traits] block with an initial value "
                f"before use. See Doc 68 §2.5."
            )
    elif target == "npc":
        npc_id = raw_eff.get("npcId")
        if not npc_id or not isinstance(npc_id, str):
            # Field-name validator (Phase 1) catches missing npcId for NPC
            # effects via a different path; skip silently here to avoid
            # double-reporting.
            return errors, warnings_out
        npc_by_slug = registries.get("npc_by_slug") or {}
        if npc_id not in npc_by_slug:
            # Unknown NPC — existing semantic validator catches this; skip.
            return errors, warnings_out
        if trait_name not in npc_by_slug[npc_id]:
            errors.append(
                f"{ctx}: effect references undeclared NPC trait `{trait_name}` "
                f"for NPC '{npc_id}'. Declare it in the NPC's `core_traits` "
                f"block. See Doc 68 §2.5."
            )
    return errors, warnings_out


def _validate_trait_declaration_in_predicate(
    raw_item: Dict[str, Any],
    registries: Dict[str, Any],
    ctx: str,
) -> Tuple[List[str], List[str]]:
    """Validate that a predicate item's `trait_key` references a declared trait.

    Returns (errors, warnings). Doc 69 §6.3.
    Only fires for `type = "trait"` items; flag/modifier/etc skipped.
    """
    if not isinstance(raw_item, dict):
        return [], []
    if raw_item.get("type") != "trait":
        return [], []
    trait_name = raw_item.get("trait_key")
    if not trait_name or not isinstance(trait_name, str):
        return [], []
    errors: List[str] = []
    warnings_out: List[str] = []
    subject = raw_item.get("subject")
    if subject == "player":
        player_keys = registries.get("player") or set()
        if trait_name in player_keys:
            stage_kind = _classify_stage_trait(trait_name, registries)
            if stage_kind == "stage_without_arc":
                warnings_out.append(
                    f"{ctx}: trait_key `{trait_name}` matches stage pattern + IS "
                    f"declared in [player.core_traits], but the corresponding NPC "
                    f"has an empty `arc_stages` list. See Doc 68 §9.0."
                )
            return errors, warnings_out
        stage_kind = _classify_stage_trait(trait_name, registries)
        if stage_kind == "stage_with_arc":
            slug = _STAGE_TRAIT_PATTERN.match(trait_name).group(1)
            errors.append(
                f"{ctx}: predicate references stage trait `{trait_name}` "
                f"(matches `<slug>_stage` pattern + NPC '{slug}' has arc_stages "
                f"declared), but `{trait_name}` is NOT declared in "
                f"[player.core_traits]. Declare it with initial value 0. "
                f"See Doc 68 §2.5 + §9.0."
            )
        elif stage_kind == "stage_unknown_npc":
            errors.append(
                f"{ctx}: predicate references undeclared player trait `{trait_name}` "
                f"(name matches `<slug>_stage` pattern but no NPC has slug matching "
                f"its prefix). Declare it in [player.core_traits]. See Doc 68 §2.5."
            )
        else:
            errors.append(
                f"{ctx}: predicate references undeclared player trait `{trait_name}`. "
                f"Declare it in [player.core_traits] block. See Doc 68 §2.5."
            )
    elif subject == "npc":
        npc_id = raw_item.get("npc_id")
        if not npc_id or not isinstance(npc_id, str):
            return errors, warnings_out
        npc_by_slug = registries.get("npc_by_slug") or {}
        if npc_id not in npc_by_slug:
            return errors, warnings_out
        if trait_name not in npc_by_slug[npc_id]:
            errors.append(
                f"{ctx}: predicate references undeclared NPC trait `{trait_name}` "
                f"for NPC '{npc_id}'. Declare it in the NPC's `core_traits` block. "
                f"See Doc 68 §2.5."
            )
    return errors, warnings_out


def _validate_trait_declaration_items_block(
    cond_block: Any, registries: Dict[str, Any], ctx: str
) -> Tuple[List[str], List[str]]:
    """Walk a `{version, logic, items: [...]}` condition block + validate
    each item's trait_key against the registries. Returns (errors, warnings).
    """
    if not isinstance(cond_block, dict):
        return [], []
    items = cond_block.get("items")
    if not isinstance(items, list):
        return [], []
    errors: List[str] = []
    warnings_out: List[str] = []
    for ii, item in enumerate(items):
        item_errs, item_warns = _validate_trait_declaration_in_predicate(
            item, registries, f"{ctx}.items[{ii}]"
        )
        errors.extend(item_errs)
        warnings_out.extend(item_warns)
    return errors, warnings_out


def normalize(data: Dict[str, Any]) -> GameTemplate:
    # Doc 69 Item 3 — parse-time accumulator for field-name mismatch errors.
    # Populated at each effect parse site; consumed by validate() (which
    # prepends these to its own errors list). Local-scope to this normalize()
    # invocation; assigned to template._parse_errors before return.
    _parse_errors: List[str] = []
    # Raw [[ui.cheat_page.grants]] dicts, kept so validate() can run the shared
    # effect validators (_validate_effect_field_names / _validate_trait_declaration_
    # in_effect) against the authored keys rather than the normalized dataclass.
    _cheat_raw_rows: List[Dict[str, Any]] = []

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
        quests_engine=_require_str(p, "quests_engine", "v1"),
        version=_require_str(p, "version", ""),
        release_date=_require_str(p, "release_date", ""),
        support_url=_require_str(p, "support_url", ""),
        studio_name=_require_str(p, "studio_name", ""),
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

        # G · Parse tags: short phrases for the cast card's tag line.
        # Empty/missing = no tag line (default; existing TOMLs unaffected).
        tags_raw = n.get("tags") or []
        if not isinstance(tags_raw, list):
            raise TypeError(
                f"npcs[{ni}].tags must be a list, got {type(tags_raw).__name__}"
            )
        if len(tags_raw) > NPC_TAGS_MAX:
            raise ValueError(
                f"npcs[{ni}].tags has {len(tags_raw)} entries, max {NPC_TAGS_MAX}. "
                f"The field ships exactly four (friends-of-mine gives all 15 of its "
                f"characters four: how they operate, what they want, an aesthetic, "
                f"and something they consume). More than that reads as a stat block."
            )
        npc_tags: List[str] = []
        for ti, tag in enumerate(tags_raw):
            if not isinstance(tag, str):
                raise TypeError(
                    f"npcs[{ni}].tags[{ti}] must be a string, "
                    f"got {type(tag).__name__}: {tag!r}"
                )
            if not tag.strip():
                raise ValueError(f"npcs[{ni}].tags[{ti}] is empty")
            npc_tags.append(tag.strip())

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
                tags=npc_tags,
                role=_require_str(n, "role", ""),
            )
        )

    # Doc 69 Item 4 — build trait registries from the just-parsed player + NPCs.
    # Used by the trait-declaration validators at each effect parse site below
    # and again in validate() for predicate-context checks. Built once here so
    # the per-effect cost is just a dict lookup.
    _trait_registries = _build_trait_registries(player.core_traits, npcs)
    _parse_warnings: List[str] = []  # collected via warnings.warn() at function end

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
                offscreen=bool(l.get("offscreen", False)),
                parent=_require_str(l, "parent", ""),
                entry_from=_require_str(l, "entry_from", ""),
                default_entry=_require_str(l, "default_entry", ""),
                navigation_order=[str(x) for x in _require_list(l, "navigation_order")],
                entry_conditions=_require_dict(l, "entry_conditions"),
                blocked_message=_require_str(l, "blocked_message", ""),
                auto_exit=bool(l.get("auto_exit", True)),
                costs=_require_dict(l, "costs"),
                clothing_rules=l.get("clothing_rules", []) or [],
                description_variants=l.get("description_variants", []) or [],
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
                    show_when_blocked=bool(trig_def.get("show_when_blocked", False)),
                    cooldown_message=_require_str(trig_def, "cooldown_message", "") or None,
                    # L2-2 — Lane 2 anti-toggle cooldown. Author writes location slugs;
                    # validator cross-refs to existing locations. Build resolves to
                    # runtime passage names at help_data emission (v1.py).
                    entry_only_from=[
                        str(loc).strip()
                        for loc in (trig_def.get("entry_only_from") or [])
                        if isinstance(loc, str) and loc.strip()
                    ],
                    # PRD 25 — Lane 3 dispatcher substitution rules. Each rule:
                    #   { "target_canvas_id": str (slug), "chance": float, "conditions": Optional[Dict] }
                    # Validation (cross-canvas reference + chance bounds + conflict warnings)
                    # happens later in validate(). Slug→UUID resolution happens at
                    # engine emission time (v1.py).
                    substitutions=[
                        {
                            "target_canvas_id": str(sub.get("target_canvas_id", "")),
                            "chance": float(sub.get("chance", 0)),
                            "conditions": sub.get("conditions") or None,
                            # Doc 69 Item 1 — Pattern B `exclusive_group` for
                            # single-dice-partition substitution. Rules in the
                            # same group share one dice roll; mutual exclusion
                            # guaranteed; failed-condition in claimed slot falls
                            # to solo (NOT next rule in group). Absent / None /
                            # empty string → Pattern A independent rolls.
                            "exclusive_group": (
                                str(sub["exclusive_group"]).strip()
                                if isinstance(sub.get("exclusive_group"), str)
                                and sub["exclusive_group"].strip()
                                else None
                            ),
                        }
                        for sub in (trig_def.get("substitutions") or [])
                        if isinstance(sub, dict) and sub.get("target_canvas_id")
                    ],
                    substitution_only=bool(trig_def.get("substitution_only", False)),
                    # Phase A — Lane 2/3 NPC presence gate. AND-gates with all
                    # other trigger conditions; engine resolves NPC location
                    # against [[npcs.schedules]] at fire-time.
                    requires_npc=(_require_str(trig_def, "requires_npc", "") or None),
                    # Doc 69 Item 2 — pre-substitution effects passthrough.
                    # Validated below (field-name + trait-declaration) inline so
                    # errors surface with helpful canvas-level context.
                    pre_substitution_effects=[
                        dict(eff)
                        for eff in (trig_def.get("pre_substitution_effects") or [])
                        if isinstance(eff, dict)
                    ],
                )
                # Doc 69 Item 2 — validate pre_substitution_effects field names
                # + trait declarations (reuses Phase 1 + Phase 2 validators).
                _pse_canvas_id = str(c.get("id") or "<unknown>")
                for _psei, _pse in enumerate(trig_def.get("pre_substitution_effects") or []):
                    if not isinstance(_pse, dict):
                        continue
                    _pse_ctx = (
                        f"canvases['{_pse_canvas_id}'].trigger"
                        f".pre_substitution_effects[{_psei}]"
                    )
                    _parse_errors.extend(_validate_effect_field_names(_pse, _pse_ctx))
                    _td_errs, _td_warns = _validate_trait_declaration_in_effect(
                        _pse, _trait_registries, _pse_ctx
                    )
                    _parse_errors.extend(_td_errs)
                    _parse_warnings.extend(_td_warns)

            # Nodes
            nodes: List[TemplateNode] = []
            # Doc 69 Item 3 — context prefix for any field-name validation errors
            # raised during this canvas's effect parsing.
            _canvas_id_for_ctx = str(c.get("id") or c.get("slug") or "<unknown>")
            for ni, n in enumerate(c.get("nodes") or []):
                if not isinstance(n, dict):
                    continue
                _node_id_for_ctx = str(n.get("id") or n.get("slug") or f"node[{ni}]")
                eb_raw = n.get("exit_block", {}) or {}
                choices: List[TemplateChoice] = []
                for chi, ch in enumerate(eb_raw.get("choices") or []):
                    if not isinstance(ch, dict):
                        continue
                    effs = []
                    for ei, e in enumerate(ch.get("effects") or []):
                        if not isinstance(e, dict):
                            continue
                        _eff_ctx = (
                            f"canvases['{_canvas_id_for_ctx}'].nodes['{_node_id_for_ctx}']"
                            f".exit_block.choices[{chi}].effects[{ei}]"
                        )
                        # Doc 69 Item 3 — field-name mismatch check.
                        _parse_errors.extend(_validate_effect_field_names(e, _eff_ctx))
                        # Doc 69 Item 4 — undeclared trait check.
                        _td_errs, _td_warns = _validate_trait_declaration_in_effect(
                            e, _trait_registries, _eff_ctx
                        )
                        _parse_errors.extend(_td_errs)
                        _parse_warnings.extend(_td_warns)
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
                    for fei, e in enumerate(ch.get("flagEffects") or []):
                        if not isinstance(e, dict):
                            continue
                        # Doc 69 Item 3 — field-name mismatch check (flag-effect context).
                        _parse_errors.extend(_validate_effect_field_names(
                            e,
                            f"canvases['{_canvas_id_for_ctx}'].nodes['{_node_id_for_ctx}']"
                            f".exit_block.choices[{chi}].flagEffects[{fei}]"
                        ))
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
                    for rei, e in enumerate(ch.get("rejection_effects") or []):
                        if not isinstance(e, dict):
                            continue
                        _rej_ctx = (
                            f"canvases['{_canvas_id_for_ctx}'].nodes['{_node_id_for_ctx}']"
                            f".exit_block.choices[{chi}].rejection_effects[{rei}]"
                        )
                        # Doc 69 Item 3 — field-name mismatch check.
                        _parse_errors.extend(_validate_effect_field_names(e, _rej_ctx))
                        # Doc 69 Item 4 — undeclared trait check.
                        _td_errs, _td_warns = _validate_trait_declaration_in_effect(
                            e, _trait_registries, _rej_ctx
                        )
                        _parse_errors.extend(_td_errs)
                        _parse_warnings.extend(_td_warns)
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

                    # doc 45 G4: parse questEffects (quest mutations)
                    quest_effs: List[Dict[str, Any]] = []
                    for qe in ch.get("questEffects") or []:
                        if isinstance(qe, dict) and qe.get("quest"):
                            entry = {"quest": str(qe["quest"]),
                                     "op": str(qe.get("op", "start"))}
                            if qe.get("step") is not None:
                                entry["step"] = int(qe["step"])
                            quest_effs.append(entry)

                    # doc 45 G5: parse scheduleEffects (delayed events)
                    schedule_effs: List[Dict[str, Any]] = []
                    for se in ch.get("scheduleEffects") or []:
                        if isinstance(se, dict) and se.get("action"):
                            entry = {"delayDays": int(se.get("delayDays", 1)),
                                     "action": str(se["action"])}
                            for k in ("flag", "quest", "conversation", "step"):
                                if se.get(k) is not None:
                                    entry[k] = se[k]
                            schedule_effs.append(entry)

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
                            locked_text_threshold=_require_str(ch, "locked_text_threshold", ""),
                            rejection_node=_require_str(ch, "rejection_node", "") or None,
                            rejection_effects=rej_effs,
                            modifier_effects=mod_effs,
                            pass_effects=pass_effs,
                            item_effects=item_effs,
                            quest_effects=quest_effs,
                            schedule_effects=schedule_effs,
                            text_variants=text_variants_parsed,
                            costs=[
                                {"trait": str(ci["trait"]), "value": int(ci["value"])}
                                for ci in (ch.get("costs") or [])
                                if isinstance(ci, dict) and "trait" in ci and "value" in ci
                            ],
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
                        # Stage-gate fields. None when missing — validate() catches
                        # partial triples (one or two of three set).
                        sg_npc = _require_str(cond_raw, "stage_npc", "") or None
                        sg_op = _require_str(cond_raw, "stage_op", "") or None
                        sg_val_raw = cond_raw.get("stage_value")
                        sg_val: Optional[int] = None
                        if sg_val_raw is not None:
                            try:
                                sg_val = int(sg_val_raw)
                            except (ValueError, TypeError):
                                raise TypeError(
                                    f"hint condition stage_value must be int, "
                                    f"got {type(sg_val_raw).__name__}: {sg_val_raw!r}"
                                )
                        # E14: parse trait_checks list (optional). Each entry must be
                        # a dict matching engine's condition_item shape; we don't
                        # re-validate here (validator runs separately).
                        trait_checks_raw = cond_raw.get("trait_checks") or []
                        trait_checks_list: List[Dict[str, Any]] = []
                        if isinstance(trait_checks_raw, list):
                            for tc in trait_checks_raw:
                                if isinstance(tc, dict):
                                    trait_checks_list.append(dict(tc))
                        # E22: parse prerequisite_npc_stage string (optional).
                        prereq_raw = _require_str(cond_raw, "prerequisite_npc_stage", "") or None
                        cond_obj = TemplateHintCondition(
                            missing_flag=_require_str(cond_raw, "missing_flag", "")
                            or None,
                            missing_trait=_require_str(cond_raw, "missing_trait", "")
                            or None,
                            gap_gte=_require_int(cond_raw, "gap_gte", 0) or None,
                            stage_npc=sg_npc,
                            stage_op=sg_op,
                            stage_value=sg_val,
                            trait_checks=trait_checks_list,
                            prerequisite_npc_stage=prereq_raw,
                        )
                    # Routing: explicit npc_id, or fall back to the stage_npc
                    # from the condition (the common case).
                    tpl_npc = _require_str(ht, "npc_id", "") or None
                    if not tpl_npc and cond_obj and cond_obj.stage_npc:
                        tpl_npc = cond_obj.stage_npc
                    # Optional priority (picker tiebreaker; default 0).
                    tpl_priority_raw = ht.get("priority", 0)
                    try:
                        tpl_priority = int(tpl_priority_raw) if tpl_priority_raw is not None else 0
                    except (TypeError, ValueError):
                        tpl_priority = 0
                    if tpl_priority < 0:
                        tpl_priority = 0
                    # Pattern 2: tip + auto_goal (both optional; auto_goal defaults true)
                    tpl_tip = _require_str(ht, "tip", "") or None
                    tpl_auto_goal = ht.get("auto_goal", True)
                    if not isinstance(tpl_auto_goal, bool):
                        tpl_auto_goal = True
                    # E17 (2026-05-06): per-hint ready-frame text override.
                    tpl_ready_text = _require_str(ht, "ready_text", "")
                    # 2026-05-09: terminal-stage badge opt-in.
                    tpl_arc_complete = ht.get("arc_complete", False)
                    if not isinstance(tpl_arc_complete, bool):
                        tpl_arc_complete = False
                    # 2026-05-10: flag-based arc closure target.
                    tpl_arc_closure_flag = ht.get("arc_closure_flag", "") or ""
                    if not isinstance(tpl_arc_closure_flag, str):
                        tpl_arc_closure_flag = ""
                    hint_templates.append(
                        TemplateHintTemplate(
                            condition=cond_obj,
                            text=_require_str(ht, "text", ""),
                            npc_id=tpl_npc,
                            priority=tpl_priority,
                            tip=tpl_tip,
                            auto_goal=tpl_auto_goal,
                            ready_text=tpl_ready_text,
                            arc_complete=tpl_arc_complete,
                            arc_closure_flag=tpl_arc_closure_flag,
                        )
                    )
            hints_obj = TemplateStoryHints(
                stuck_threshold_minutes=_require_int(
                    hints_raw, "stuck_threshold_minutes", 30
                ),
                hint_style=_require_str(hints_raw, "hint_style", "observation"),
                templates=hint_templates,
                stuck_threshold_days=_require_int(hints_raw, "stuck_threshold_days", 7),
                stage_stall_message=_require_str(hints_raw, "stage_stall_message", ""),
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
    narration_person = _require_str(settings_raw, "narration_person", "second")
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
                    beauty=_require_int(c_raw, "beauty", 0),
                    corruption=_require_int(c_raw, "corruption", 0),
                    type=_require_str(c_raw, "type", ""),
                    exposure=_require_int(c_raw, "exposure", 0),
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

    # ── Quests (doc 45 G4) ──
    quests_raw = data.get("quests", []) or []
    quests: List[TemplateQuest] = []
    for qi, q in enumerate(quests_raw):
        if not isinstance(q, dict):
            continue
        quests.append(
            TemplateQuest(
                id=_require_str(q, "id"),
                name=_require_str(q, "name", ""),
                steps=[str(s) for s in (q.get("steps") or [])],
                repeatable=bool(q.get("repeatable", False)),
            )
        )

    # ── PRD 48: Quests Engine V2 cards ──
    # Top-level key is `quest_cards` (flat, not nested under `quests`) to
    # avoid future namespace collision with doc 45 G4's `[[quests]]` table
    # array. Only populated when project.quests_engine == "v2"; v1 games
    # ignore this block entirely.
    quests_cards_parsed: List[QuestsCard] = []
    if project.quests_engine == "v2":
        for qc_raw in (data.get("quest_cards", []) or []):
            if not isinstance(qc_raw, dict):
                continue
            quests_cards_parsed.append(_parse_quests_card(qc_raw))

    # ── Fast jobs (doc 45 G9) ──
    fast_jobs_raw = data.get("fast_jobs", []) or []
    fast_jobs: List[TemplateFastJob] = []
    for fj in fast_jobs_raw:
        if not isinstance(fj, dict):
            continue
        fast_jobs.append(
            TemplateFastJob(
                id=_require_str(fj, "id"),
                name=_require_str(fj, "name", ""),
                income=_require_int(fj, "income", 0),
                xp_req=_require_int(fj, "xp_req", 0),
                cooldown_days=_require_int(fj, "cooldown_days", 0),
                time_period=_require_str(fj, "time_period", ""),
                money_trait=_require_str(fj, "money_trait", "money") or "money",
            )
        )

    # ── Bank (doc 45 G9) ──
    bank_obj: Optional[TemplateBank] = None
    bank_raw = data.get("bank")
    if isinstance(bank_raw, dict) and _require_bool(bank_raw, "enabled", True):
        bank_obj = TemplateBank(
            enabled=True,
            interest_rate=float(bank_raw.get("interest_rate", 0.01) or 0.01),
            money_trait=_require_str(bank_raw, "money_trait", "money") or "money",
        )

    # ── Player portrait (state-reactive sidebar image, opt-in) ──
    player_portrait_obj: Optional[TemplatePlayerPortrait] = None
    pp_raw = data.get("player_portrait")
    if isinstance(pp_raw, dict) and _require_bool(pp_raw, "enabled", True):
        pp_outfits: List[TemplatePlayerPortraitOutfit] = []
        for od in (pp_raw.get("outfits") or []):
            if not isinstance(od, dict):
                continue
            pp_outfits.append(
                TemplatePlayerPortraitOutfit(
                    image=_require_str(od, "image", ""),
                    when=od.get("when") if isinstance(od.get("when"), dict) else {},
                )
            )
        player_portrait_obj = TemplatePlayerPortrait(
            enabled=True,
            naked_image=_require_str(pp_raw, "naked_image", ""),
            topless_image=_require_str(pp_raw, "topless_image", ""),
            bottomless_image=_require_str(pp_raw, "bottomless_image", ""),
            underwear_image=_require_str(pp_raw, "underwear_image", ""),
            default_image=_require_str(pp_raw, "default_image", ""),
            pregnancy_trait=_require_str(pp_raw, "pregnancy_trait", ""),
            pregnancy_suffix=_require_str(pp_raw, "pregnancy_suffix", "Preg") or "Preg",
            outfits=pp_outfits,
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
    rent_currency_symbol = _require_str(rent_raw, "currency_symbol", "$") or "$"

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
                    post_actions=list(a_raw.get("post_actions") or []),
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
                    notify=_require_str(c_raw, "notify", ""),
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
                    notify=_require_str(p_raw, "notify", ""),
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
                _dt_corr_min = dt_raw.get("corruption_min")
                phone_daily_topics.append(TemplatePhoneDailyTopic(
                    id=_require_str(dt_raw, "id"),
                    npc=_require_str(dt_raw, "npc", ""),
                    player_message=_require_str(dt_raw, "player_message", ""),
                    npc_response=_require_str(dt_raw, "npc_response", ""),
                    effects=dt_raw.get("effects", []) or [],
                    conditions=dt_raw.get("conditions", {}) or {},
                    image=_require_str(dt_raw, "image", ""),
                    corruption_min=int(_dt_corr_min) if _dt_corr_min is not None else None,
                    cooldown=_require_str(dt_raw, "cooldown", ""),
                ))

            phone_gallery_items: List[TemplatePhoneGalleryItem] = []
            for gi, g_raw in enumerate(phone_raw.get("gallery_items") or []):
                if not isinstance(g_raw, dict):
                    continue
                phone_gallery_items.append(TemplatePhoneGalleryItem(
                    id=_require_str(g_raw, "id"),
                    image=_require_str(g_raw, "image", ""),
                    caption=_require_str(g_raw, "caption", ""),
                    trigger=g_raw.get("trigger", {}) or {},
                    link=_require_str(g_raw, "link", ""),
                ))

            phone_obj = TemplatePhone(
                enabled=phone_enabled,
                apps=phone_apps,
                conversations=phone_conversations,
                posts=phone_posts,
                profiles=phone_profiles,
                daily_topics=phone_daily_topics,
                gallery_items=phone_gallery_items,
                purchase_flag=_require_str(phone_raw, "purchase_flag", ""),
            )

    # ── Day-rollover hook ── [engine.daily_tick]
    daily_tick_obj: Optional[TemplateDailyTick] = None
    # ── Stage helpers ── [[engine.stage_helpers]]
    stage_helpers: List[TemplateStageHelper] = []
    corruption_tiers_obj: Optional[List[int]] = None
    engine_raw = data.get("engine")
    if isinstance(engine_raw, dict):
        _ct_raw = engine_raw.get("corruption_tiers")
        if isinstance(_ct_raw, list) and _ct_raw:
            corruption_tiers_obj = [int(x) for x in _ct_raw]
        dt_raw = engine_raw.get("daily_tick")
        if isinstance(dt_raw, dict):
            dt_flag_effs: List[TemplateFlagEffect] = []
            for dt_fei, fe in enumerate(dt_raw.get("flagEffects") or []):
                if not isinstance(fe, dict):
                    continue
                # Doc 69 Item 3 — field-name mismatch check (daily_tick flagEffect context).
                _parse_errors.extend(_validate_effect_field_names(
                    fe,
                    f"engine.daily_tick.flagEffects[{dt_fei}]"
                ))
                dt_flag_effs.append(
                    TemplateFlagEffect(
                        targetType=str(fe.get("targetType", "player")),
                        npcId=_require_str(fe, "npcId", "") or None,
                        flag=_require_str(fe, "flag", ""),
                        op=_require_str(fe, "op", "set") or "set",
                        conditions=fe.get("conditions") or None,
                    )
                )
            dt_trait_effs: List[TemplateChoiceEffect] = []
            for dt_tei, te in enumerate(dt_raw.get("traitEffects") or []):
                if not isinstance(te, dict):
                    continue
                _dtte_ctx = f"engine.daily_tick.traitEffects[{dt_tei}]"
                # Doc 69 Item 3 — field-name mismatch check.
                _parse_errors.extend(_validate_effect_field_names(te, _dtte_ctx))
                # Doc 69 Item 4 — undeclared trait check.
                _td_errs, _td_warns = _validate_trait_declaration_in_effect(
                    te, _trait_registries, _dtte_ctx
                )
                _parse_errors.extend(_td_errs)
                _parse_warnings.extend(_td_warns)
                dt_trait_effs.append(
                    TemplateChoiceEffect(
                        targetType=str(te.get("targetType", "player")),
                        npcId=_require_str(te, "npcId", "") or None,
                        trait=_require_str(te, "trait", ""),
                        op=_require_str(te, "op", "add") or "add",
                        value=te.get("value", 0),
                        clamp=te.get("clamp", None),
                        cap=te.get("cap", None),
                        conditions=te.get("conditions") or None,
                    )
                )
            daily_tick_obj = TemplateDailyTick(
                flagEffects=dt_flag_effs, traitEffects=dt_trait_effs
            )
        for sh_raw in engine_raw.get("stage_helpers") or []:
            if not isinstance(sh_raw, dict):
                continue
            stage_helpers.append(
                TemplateStageHelper(
                    name=_require_str(sh_raw, "name", ""),
                    description=_require_str(sh_raw, "description", ""),
                    conditions=_require_dict(sh_raw, "conditions"),
                    dev_only=bool(sh_raw.get("dev_only", False)),
                )
            )

    # Tips page (game-level mechanics surface). Authored under [ui.tips_page].
    tips_page_obj: Optional[TemplateTipsPage] = None
    ui_raw = data.get("ui")
    if isinstance(ui_raw, dict):
        tp_raw = ui_raw.get("tips_page")
        if isinstance(tp_raw, dict):
            tp_content = _require_str(tp_raw, "content", "")
            if tp_content:
                tips_page_obj = TemplateTipsPage(
                    title=_require_str(tp_raw, "title", "Tips") or "Tips",
                    content=tp_content,
                )

    # Cast page (the who-is-who surface). Authored under [ui.cast_page].
    # PRESENCE of the block is the whole opt-in — unlike tips_page there is no
    # content field to be empty, because the roster comes from [[npcs]] and the
    # quest cards. A non-table here is a hard error rather than a silent drop,
    # for the reason recorded on TemplateCheatPage: a silently-dropped UI block
    # is invisible until somebody notices the button never appeared.
    cast_page_obj: Optional[TemplateCastPage] = None
    if isinstance(ui_raw, dict):
        castp_raw = ui_raw.get("cast_page")
        if castp_raw is not None:
            if not isinstance(castp_raw, dict):
                raise TypeError(
                    f"[ui.cast_page] must be a table, got {type(castp_raw).__name__}"
                )
            castp_title = _require_str(castp_raw, "title", "The Cast") or "The Cast"
            cast_page_obj = TemplateCastPage(
                title=castp_title,
                intro=_require_str(castp_raw, "intro", ""),
                button_label=_require_str(castp_raw, "button_label", "") or castp_title,
                button_icon=_require_str(castp_raw, "button_icon", ""),
            )

    # Player cheat page. Authored under [ui.cheat_page] + [[ui.cheat_page.grants]].
    # NOTE the deliberate divergence from tips_page above: an authored-but-empty
    # block is NOT silently dropped here. It is constructed and left for validate()
    # to reject, because a silently-dropped page is invisible until someone notices
    # the sidebar button never appeared.
    cheat_page_obj: Optional[TemplateCheatPage] = None
    if isinstance(ui_raw, dict):
        cp_raw = ui_raw.get("cheat_page")
        if cp_raw is not None:
            if not isinstance(cp_raw, dict):
                raise TypeError(f"[ui.cheat_page] must be a table, got {type(cp_raw).__name__}")
            # Reject a TOML-side unlock selector. Which rows are live is decided at
            # RUNTIME by the code the player typed; a value committed here would open
            # every row for everyone, in a file that ships publicly.
            for _bad_key in (
                "enabled", "paid", "free", "grants_enabled", "cheat_grants", "unlocked",
            ):
                if _bad_key in cp_raw:
                    _parse_errors.append(
                        f"[ui.cheat_page] must not declare '{_bad_key}' — rows unlock at runtime "
                        f"when the player enters that row's code. Remove it."
                    )
            # The codes themselves are NEVER authored here. This file is git-tracked
            # and the repo is public; committing a code publishes it. Codes live in an
            # untracked per-game codes file read by `package_from_toml --codes`.
            for _bad_key in ("code", "codes", "code_words", "password"):
                if _bad_key in cp_raw:
                    _parse_errors.append(
                        f"[ui.cheat_page] must not declare '{_bad_key}' — this file is committed "
                        f"to a public repo. Put codes in the game's untracked codes file and pass "
                        f"it with `package_from_toml --codes <path>`."
                    )
            grants: List[TemplateCheatGrant] = []
            for gi, g_raw in enumerate(cp_raw.get("grants", []) or []):
                if not isinstance(g_raw, dict):
                    raise TypeError(
                        f"ui.cheat_page.grants[{gi}] must be a table, got {type(g_raw).__name__}"
                    )
                for _bad_key in ("code", "password"):
                    if _bad_key in g_raw:
                        _parse_errors.append(
                            f"ui.cheat_page.grants[{gi}] must not declare '{_bad_key}' — codes live "
                            f"in the untracked codes file, keyed by this row's `id`."
                        )
                _cap = g_raw.get("cap")
                grants.append(
                    TemplateCheatGrant(
                        id=_require_str(g_raw, "id", ""),
                        label=_require_str(g_raw, "label", ""),
                        trait=_require_str(g_raw, "trait", ""),
                        value=g_raw.get("value"),
                        targetType=_require_str(g_raw, "targetType", "player") or "player",
                        npcId=_require_str(g_raw, "npcId", ""),
                        op=_require_str(g_raw, "op", "add") or "add",
                        cap=_cap if isinstance(_cap, (int, float)) else None,
                        clamp=bool(g_raw.get("clamp", True)),
                        hint=_require_str(g_raw, "hint", ""),
                        button_text=_require_str(g_raw, "button_text", ""),
                        at_cap_text=_require_str(g_raw, "at_cap_text", ""),
                    )
                )
                # Keep the raw dict for the shared effect validators in validate().
                _cheat_raw_rows.append(g_raw)
            cheat_page_obj = TemplateCheatPage(
                title=_require_str(cp_raw, "title", "Cheats") or "Cheats",
                intro=_require_str(cp_raw, "intro", ""),
                button_label=_require_str(cp_raw, "button_label", ""),
                button_icon=_require_str(cp_raw, "button_icon", ""),
                join_note=_require_str(cp_raw, "join_note", ""),
                join_url=_require_str(cp_raw, "join_url", ""),
                grants=grants,
            )

    # [builds] is retired. One build ships everywhere now — which cheat rows are live
    # is a runtime property of the code the player entered, not a property of the file.
    # A leftover block is a parse error rather than a silent no-op, so a game carrying
    # the old labels tells its author instead of quietly losing its footer badge.
    if data.get("builds") is not None:
        _parse_errors.append(
            "[builds] is no longer supported — the free/paid build split was removed. "
            "One build ships everywhere and cheat rows unlock at runtime by code. "
            "Delete the [builds] block; the sidebar footer keeps [project] version "
            "and release_date."
        )

    # Pattern 2: label registries — top-level [[traits.labels]] / [[flags.labels]]
    trait_labels: List[TemplateTraitLabel] = []
    traits_raw = data.get("traits")
    if isinstance(traits_raw, dict):
        for tl_raw in traits_raw.get("labels") or []:
            if not isinstance(tl_raw, dict):
                continue
            trait_labels.append(
                TemplateTraitLabel(
                    key=_require_str(tl_raw, "key", ""),
                    label=_require_str(tl_raw, "label", ""),
                    verb=_require_str(tl_raw, "verb", "reach") or "reach",
                    unit=_require_str(tl_raw, "unit", ""),
                    hidden=bool(tl_raw.get("hidden", False)),
                )
            )

    flag_labels: List[TemplateFlagLabel] = []
    flags_raw = data.get("flags")
    if isinstance(flags_raw, dict):
        for fl_raw in flags_raw.get("labels") or []:
            if not isinstance(fl_raw, dict):
                continue
            flag_labels.append(
                TemplateFlagLabel(
                    key=_require_str(fl_raw, "key", ""),
                    label=_require_str(fl_raw, "label", ""),
                )
            )

    # Doc 69 Item 4 — emit any trait-declaration warnings collected at parse
    # time. Warnings (not errors) for stage-trait-without-arc_stages edge case.
    if _parse_warnings:
        import warnings as _w
        for _warn_msg in _parse_warnings:
            _w.warn(_warn_msg, UserWarning, stacklevel=2)

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
        narration_person=narration_person,
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
        rent_currency_symbol=rent_currency_symbol,
        sidebar_items=sidebar_items,
        phone_enabled=phone_enabled,
        phone=phone_obj,
        passes=passes,
        quests=quests,
        quests_cards=quests_cards_parsed,
        items=items,
        theme=theme_obj,
        daily_tick=daily_tick_obj,
        stage_helpers=stage_helpers,
        corruption_tiers=corruption_tiers_obj,
        fast_jobs=fast_jobs,
        bank=bank_obj,
        player_portrait=player_portrait_obj,
        trait_labels=trait_labels,
        flag_labels=flag_labels,
        tips_page=tips_page_obj,
        cast_page=cast_page_obj,
        # This kwarg is the silent-no-op step: parse the block, forget the kwarg,
        # and the feature vanishes with no error anywhere. Covered by a test.
        cheat_page=cheat_page_obj,
        # Doc 69 Item 3 — parse-time field-name mismatch errors collected
        # by the effect-context validators at the 5 effect parse sites.
        _parse_errors=_parse_errors,
        _cheat_raw_rows=_cheat_raw_rows,
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


# Content block types the comprehensive generator's _convert_blocks_to_game_html
# (v2.py / v1.py) can actually render. Anything else hits the generator's silent
# `<p>{content}</p>` fallback, which DISCARDS the speaker/structure — this is the
# bug that shipped two whole games (the_inheritance authored "dialogue", last_call
# authored "speech", both rendered as anonymous paragraphs). The build now hard-
# fails on an unrecognized content block type so the next typo is caught here, not
# silently in the shipped HTML. Keep in sync with the generator's block dispatch.
RECOGNIZED_CONTENT_BLOCK_TYPES = frozenset({
    "heading", "paragraph", "dialog", "thought_bubble",
    "image", "video", "cascade", "group", "block_pool", "clip",
})

# Common authoring near-misses → the canonical type, for a "did you mean" hint.
_CONTENT_BLOCK_TYPE_SUGGESTIONS = {
    "dialogue": "dialog",
    "speech": "dialog",
    "say": "dialog",
    "thought": "thought_bubble",
    "thoughtbubble": "thought_bubble",
    "img": "image",
    "picture": "image",
    "text": "paragraph",
    "p": "paragraph",
}


def _validate_content_block_types(blocks: Any, ctx: str) -> List[str]:
    """Walk a CONTENT-block list (a canvas node's `blocks`), recursing into the
    container blocks the renderer descends into (group / block_pool / cascade
    beats), and flag any block whose `type` the generator can't render.

    Scoped to content blocks only — never touches the `type` fields used by
    condition items (flag/trait/random/...), exit blocks (location/choices/
    game_end), or phone apps, so it can't false-fail those.
    """
    errs: List[str] = []
    if not isinstance(blocks, list):
        return errs
    for bi, b in enumerate(blocks):
        if not isinstance(b, dict):
            continue
        b_type = str(b.get("type", "")).strip()
        if not b_type:
            continue
        if b_type not in RECOGNIZED_CONTENT_BLOCK_TYPES:
            hint = _CONTENT_BLOCK_TYPE_SUGGESTIONS.get(b_type.lower())
            suggestion = f" (did you mean '{hint}'?)" if hint else ""
            errs.append(
                f"{ctx}.blocks[{bi}]: unrecognized content block type "
                f"'{b_type}'{suggestion}. The generator would silently render it "
                f"as a plain paragraph and discard any speaker. Recognized types: "
                f"{', '.join(sorted(RECOGNIZED_CONTENT_BLOCK_TYPES))}."
            )
            # Unknown container shape is undefined — don't recurse into it.
            continue
        props = b.get("props") or {}
        if not isinstance(props, dict):
            props = {}
        # Recurse exactly where the renderer descends into children.
        if b_type in ("group", "block_pool"):
            child = b.get("blocks") or props.get("blocks") or []
            errs.extend(_validate_content_block_types(child, f"{ctx}.blocks[{bi}]"))
        elif b_type == "cascade":
            for ti, beat in enumerate(props.get("beats") or []):
                if isinstance(beat, dict):
                    errs.extend(_validate_content_block_types(
                        beat.get("blocks") or [], f"{ctx}.blocks[{bi}].beats[{ti}]"
                    ))
    return errs


def validate(template: GameTemplate) -> List[str]:
    errors: List[str] = []

    # Doc 69 Item 3 — prepend parse-time field-name mismatch errors collected
    # during normalize() at the 5 effect parse sites. These are surfaced first
    # so authors fix syntax problems before semantic validation runs.
    if getattr(template, "_parse_errors", None):
        errors.extend(template._parse_errors)

    # Narrative person must be one of the three the generator knows how to label.
    # A typo here would silently fall back to "You:" over third-person prose —
    # exactly the mismatch this setting exists to prevent — so fail the build.
    if template.narration_person not in VALID_NARRATION_PERSONS:
        errors.append(
            f"[settings] narration_person = '{template.narration_person}' is not valid. "
            f"Expected one of: {', '.join(sorted(VALID_NARRATION_PERSONS))}."
        )

    # Doc 69 Item 3 — predicate-context field-name validation. Walks every
    # `conditions = {version, logic, items}` block stored on parsed dataclasses
    # (canvas triggers, choices, effect conditions, etc.) and checks each item
    # for forbidden effect-context field names (`targetType` / `npcId` / `op`
    # in predicate context; also `trait`/`flag` when type=trait/flag).
    #
    # Doc 69 Item 4 — undeclared trait check on each predicate item. Built
    # alongside the field-name walk for efficiency. Both validators share the
    # same condition-block traversal.
    _trait_registries_for_validate = _build_trait_registries(
        template.player.core_traits if template.player else {},
        template.npcs,
    )
    # Doc 72 — collect known clothing types from the catalog so the worn_type
    # walker can typo-catch references to types no item declares.
    _known_clothing_types = {
        ci.type for ci in (template.clothing_items or []) if ci.type
    }
    _validate_warnings: List[str] = []

    # Player-portrait <-> clothing type-coverage drift (WARN, not block — mirrors clothing's own
    # worn_type typo-warn). If the portrait is on with outfit rules, a clothing `type` the player
    # can wear that has NO matching rule shows default_image (a silent wrong-picture as the wardrobe
    # grows); and a rule whose `worn_type` no clothing item carries is a dead rule.
    if (template.player_portrait is not None and template.player_portrait.enabled
            and template.clothing_enabled):
        _pp_rule_types = {
            (o.when or {}).get("worn_type")
            for o in (template.player_portrait.outfits or [])
            if isinstance(o.when, dict) and o.when.get("worn_type")
        }
        for _ct in sorted(_known_clothing_types):
            if _ct not in _pp_rule_types:
                _validate_warnings.append(
                    f"player_portrait: clothing type '{_ct}' has no outfit rule — wearing it falls "
                    f"back to default_image (add a [[player_portrait.outfits]] with when.worn_type = '{_ct}')"
                )
        for _rt in sorted(t for t in _pp_rule_types if t not in _known_clothing_types):
            _validate_warnings.append(
                f"player_portrait: outfit rule worn_type '{_rt}' matches no [[clothing]] item's type "
                f"— dead rule (fix the tag or remove it)"
            )

    def _check_cond_block(cond_block: Any, ctx: str) -> None:
        """Closure helper — apply both validators to one conditions block."""
        # Field-name validation (Item 3)
        errors.extend(_validate_predicate_items_block(cond_block, ctx))
        # Trait-declaration validation (Item 4)
        td_errs, td_warns = _validate_trait_declaration_items_block(
            cond_block, _trait_registries_for_validate, ctx
        )
        errors.extend(td_errs)
        _validate_warnings.extend(td_warns)
        # Doc 72 — worn_type typo-catch (warnings only, never blocks build)
        _validate_warnings.extend(_validate_worn_type_items_block(
            cond_block, ctx, _known_clothing_types, RECOMMENDED_CLOTHING_TYPES,
        ))

    for ci, canvas in enumerate(template.canvases or []):
        canvas_ctx_id = canvas.id or f"<canvas[{ci}]>"
        # Canvas trigger conditions
        if canvas.trigger and isinstance(canvas.trigger.conditions, dict):
            _check_cond_block(
                canvas.trigger.conditions,
                f"canvases['{canvas_ctx_id}'].trigger.conditions"
            )
        # Per-substitution-rule conditions
        if canvas.trigger and canvas.trigger.substitutions:
            for si, sub_rule in enumerate(canvas.trigger.substitutions):
                if isinstance(sub_rule, dict) and isinstance(sub_rule.get("conditions"), dict):
                    _check_cond_block(
                        sub_rule["conditions"],
                        f"canvases['{canvas_ctx_id}'].trigger.substitutions[{si}].conditions"
                    )
        # Per-node choice + effect + flag-effect + rejection-effect conditions
        for ni, node in enumerate(canvas.nodes or []):
            node_ctx_id = node.id or f"node[{ni}]"
            # Content block-type allowlist (build-fatal) — runs for EVERY node,
            # before the exit_block guard below, so a node that's pure content
            # still gets checked.
            errors.extend(_validate_content_block_types(
                node.blocks,
                f"canvases['{canvas_ctx_id}'].nodes['{node_ctx_id}']",
            ))
            eb = getattr(node, "exit_block", None)
            if eb is None:
                continue
            for chi, choice in enumerate(eb.choices or []):
                choice_ctx = (
                    f"canvases['{canvas_ctx_id}'].nodes['{node_ctx_id}']"
                    f".exit_block.choices[{chi}]"
                )
                if isinstance(choice.conditions, dict):
                    _check_cond_block(choice.conditions, f"{choice_ctx}.conditions")
                # Per-effect conditions (Doc 45 G6 — optional condition gate on effects).
                for ei, eff in enumerate(choice.effects or []):
                    if isinstance(eff.conditions, dict):
                        _check_cond_block(
                            eff.conditions, f"{choice_ctx}.effects[{ei}].conditions"
                        )
                for fei, feff in enumerate(choice.flagEffects or []):
                    if isinstance(feff.conditions, dict):
                        _check_cond_block(
                            feff.conditions, f"{choice_ctx}.flagEffects[{fei}].conditions"
                        )
                for rei, reff in enumerate(choice.rejection_effects or []):
                    if isinstance(reff.conditions, dict):
                        _check_cond_block(
                            reff.conditions, f"{choice_ctx}.rejection_effects[{rei}].conditions"
                        )
                # Per-text-variant conditions (E6).
                for tvi, tv in enumerate(choice.text_variants or []):
                    if isinstance(tv, dict) and isinstance(tv.get("conditions"), dict):
                        _check_cond_block(
                            tv["conditions"], f"{choice_ctx}.text_variants[{tvi}].conditions"
                        )
    # Daily-tick effect conditions (Doc 45 G6).
    if template.daily_tick:
        for fei, fe in enumerate(template.daily_tick.flagEffects or []):
            if isinstance(fe.conditions, dict):
                _check_cond_block(
                    fe.conditions, f"engine.daily_tick.flagEffects[{fei}].conditions"
                )
        for tei, te in enumerate(template.daily_tick.traitEffects or []):
            if isinstance(te.conditions, dict):
                _check_cond_block(
                    te.conditions, f"engine.daily_tick.traitEffects[{tei}].conditions"
                )
    # Quest card `when` conditions (PRD 48).
    for qi, card in enumerate(template.quests_cards or []):
        card_ctx_id = getattr(card, "id", None) or f"quests_cards[{qi}]"
        when_block = getattr(card, "when", None)
        if isinstance(when_block, dict):
            _check_cond_block(when_block, f"quests_cards['{card_ctx_id}'].when")

    # Doc 69 Item 4 — emit any trait-declaration warnings collected during the
    # validate() walk (e.g., stage-trait-without-arc_stages edge cases).
    # Doc 72 — also catches worn_type typo / uncommon-type INFO notes.
    # Warnings are emitted via the warnings module (legacy) AND attached to the
    # template (for test introspection).
    if _validate_warnings:
        import warnings as _w
        for _warn_msg in _validate_warnings:
            _w.warn(_warn_msg, UserWarning, stacklevel=2)
    # Always attach (empty list if no warnings) so tests can introspect cleanly.
    template._validate_warnings = _validate_warnings

    # project
    if not template.project.title:
        errors.append("project.title is required")
    if not _is_valid_slug(template.project.slug):
        errors.append("project.id must be lowercase snake_case (^[a-z0-9_]+$)")
    # support_url lands in an href on EVERY passage of a published file. html.escape
    # already stops the build-break (a `"` closes nothing, `<<` fires no macro), but
    # it does not stop `javascript:` or `data:text/html,` — those would ship as a
    # live click target. Scheme-gate at import time; empty means "use the default".
    if template.project.support_url and not template.project.support_url.startswith(
        ("http://", "https://")
    ):
        errors.append("project.support_url must start with http:// or https://")

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
        # NPC schedules un-deprecated 2026-05-14 — now the canonical source
        # of truth for engine.getNpcLocation(). When declared, the engine
        # consults [[npcs.schedules]] FIRST and falls back to canvas-derived
        # presence only for NPCs without explicit schedules. See memory
        # `v2_engine_fork.md` + the Phase A plan for context.
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
        elif itype == "trait_bar":
            # Generic colored-bar-with-bands primitive. trait + max produce a
            # plain bar (today's behavior); optional bands add a per-range icon
            # + text overlay; optional color_tiers add a percentage-keyed CSS
            # class on the fill so authors can paint blue → orange → red tiers
            # without writing per-game CSS. hide_value suppresses the
            # "Label: N / max" line for games using bands as the read-out.
            ctx = f"sidebar_items[{i}] (trait_bar)"
            trait = item.get("trait")
            owner = item.get("trait_owner", "player")
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
                errors.append(
                    f"{ctx}: trait '{trait}' not found in player.core_traits (widget will render empty)"
                )
            if "max" in item:
                max_val = item["max"]
                if not isinstance(max_val, (int, float)) or isinstance(max_val, bool) or max_val <= 0:
                    errors.append(f"{ctx}: 'max' must be a positive number")
            if "bands" in item:
                bands = item["bands"]
                if not isinstance(bands, list) or not bands:
                    errors.append(f"{ctx}: 'bands' must be a non-empty list when provided")
                else:
                    for bi, band in enumerate(bands):
                        bctx = f"{ctx} bands[{bi}]"
                        if not isinstance(band, dict):
                            errors.append(f"{bctx}: must be a table/dict")
                            continue
                        if "text" not in band:
                            errors.append(f"{bctx}: missing 'text'")
                        elif not isinstance(band["text"], str):
                            errors.append(f"{bctx}: 'text' must be a string")
                        # Bars are value-driven; flag-mode bands belong on
                        # trait_words, not on a numeric meter overlay.
                        if "flag" in band:
                            errors.append(
                                f"{bctx}: 'flag' is not supported on trait_bar bands "
                                f"(use 'min' and 'max' — flag-mode is trait_words-only)"
                            )
                        if "min" not in band or "max" not in band:
                            errors.append(f"{bctx}: requires both 'min' and 'max'")
                        else:
                            bmin, bmax = band["min"], band["max"]
                            if isinstance(bmin, (int, float)) and isinstance(bmax, (int, float)) and bmin > bmax:
                                errors.append(f"{bctx}: min ({bmin}) must be <= max ({bmax})")
                        if "icon" in band and not isinstance(band["icon"], str):
                            errors.append(f"{bctx}: 'icon' must be a string when set")
            if "color_tiers" in item:
                tiers = item["color_tiers"]
                if not isinstance(tiers, list) or not tiers:
                    errors.append(f"{ctx}: 'color_tiers' must be a non-empty list when provided")
                else:
                    prev_up_to = -1.0
                    for ti, tier in enumerate(tiers):
                        tctx = f"{ctx} color_tiers[{ti}]"
                        if not isinstance(tier, dict):
                            errors.append(f"{tctx}: must be a table/dict")
                            continue
                        up_to = tier.get("up_to")
                        cls = tier.get("class")
                        if (
                            not isinstance(up_to, (int, float))
                            or isinstance(up_to, bool)
                            or up_to < 0
                            or up_to > 100
                        ):
                            errors.append(f"{tctx}: 'up_to' must be a number between 0 and 100")
                        elif up_to <= prev_up_to:
                            errors.append(
                                f"{tctx}: 'up_to' ({up_to}) must be strictly greater than the previous "
                                f"tier's up_to ({prev_up_to}); color_tiers must be sorted ascending"
                            )
                        else:
                            prev_up_to = float(up_to)
                        if not isinstance(cls, str) or not cls:
                            errors.append(f"{tctx}: 'class' is required (non-empty string)")
            if "hide_value" in item and not isinstance(item["hide_value"], bool):
                errors.append(f"{ctx}: 'hide_value' must be a boolean")
        elif itype == "trait_status_text":
            # Passive body-state surface — renders the first matching band's
            # text when the trait falls within range, renders nothing when no
            # band matches. Sibling of trait_decay_warning (which is event-
            # based) but authored, threshold-driven, continuous. Use for
            # hygiene/energy/hunger-style needs that recover on action.
            ctx = f"sidebar_items[{i}] (trait_status_text)"
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
                    has_min = "min" in band
                    has_max = "max" in band
                    if not has_min and not has_max:
                        errors.append(
                            f"{bctx}: must provide at least one of 'min' or 'max' "
                            f"(a band with neither bound would always match)"
                        )
                    if has_min:
                        bmin = band.get("min")
                        if not isinstance(bmin, (int, float)) or isinstance(bmin, bool):
                            errors.append(f"{bctx}: 'min' must be a number when set")
                    if has_max:
                        bmax = band.get("max")
                        if not isinstance(bmax, (int, float)) or isinstance(bmax, bool):
                            errors.append(f"{bctx}: 'max' must be a number when set")
                    if has_min and has_max:
                        bmin, bmax = band.get("min"), band.get("max")
                        if (
                            isinstance(bmin, (int, float))
                            and isinstance(bmax, (int, float))
                            and bmin > bmax
                        ):
                            errors.append(f"{bctx}: min ({bmin}) must be <= max ({bmax})")
                    if "text" not in band:
                        errors.append(f"{bctx}: missing 'text'")
                    elif not isinstance(band["text"], str) or not band["text"]:
                        errors.append(f"{bctx}: 'text' must be a non-empty string")
                    if "icon" in band and not isinstance(band["icon"], str):
                        errors.append(f"{bctx}: 'icon' must be a string when set")
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
        elif itype == "npc_panel":
            # RTS House-card: per-NPC arousal band / corruption / location (from schedule).
            ctx = f"sidebar_items[{i}] (npc_panel)"
            np_npc_id = item.get("npc_id")
            np_npc = None
            if not np_npc_id:
                errors.append(f"{ctx}: 'npc_id' is required")
            elif np_npc_id not in _npc_ids_for_sidebar:
                errors.append(f"{ctx}: npc_id '{np_npc_id}' not found in NPC definitions")
            else:
                np_npc = next((n for n in template.npcs if n.id == np_npc_id), None)
            np_rows = item.get("rows")
            if not isinstance(np_rows, list) or not np_rows:
                errors.append(
                    f"{ctx}: 'rows' is required (non-empty list from: arousal, corruption, location)"
                )
            else:
                for r in np_rows:
                    if r not in ("arousal", "corruption", "location", "next"):
                        errors.append(
                            f"{ctx}: invalid row '{r}' (allowed: arousal, corruption, location, next)"
                        )
                    elif (
                        np_npc is not None
                        and r in ("arousal", "corruption")
                        and r not in (np_npc.core_traits or {})
                    ):
                        errors.append(
                            f"{ctx}: row '{r}' but NPC '{np_npc_id}' has no '{r}' in core_traits "
                            f"(declare it before use)"
                        )

        elif itype == "quest_next":
            # The next STEP in the always-visible chrome, as opposed to
            # trait_status_text, which is the next STATE. Renders the same goal block
            # as the Quests page. `npc_id` picks that character's live card; omitted,
            # it takes the live tier cards (those with no npc_id) in file order.
            ctx = f"sidebar_items[{i}] (quest_next)"
            if template.project.quests_engine != "v2":
                errors.append(
                    f"{ctx}: requires project.quests_engine = \"v2\" — the goal-block "
                    f"renderer this reuses only exists on the v2 quests page"
                )
            if not (template.quests_cards or []):
                errors.append(f"{ctx}: no [[quest_cards]] defined — nothing to show")
            qn_npc = item.get("npc_id")
            if qn_npc is not None and qn_npc not in _npc_ids_for_sidebar:
                errors.append(f"{ctx}: npc_id '{qn_npc}' not found in NPC definitions")
            qn_max = item.get("max")
            if qn_max is not None and (
                not isinstance(qn_max, int) or isinstance(qn_max, bool) or qn_max < 1
            ):
                errors.append(f"{ctx}: 'max' must be a positive integer when set")

    # ── Cheat page ([ui.cheat_page]) ───────────────────────────────────────────
    # Placed here so the sidebar-item scan above is still in scope: "is this trait
    # banded?" is answered from [[sidebar_items]], and an uncapped grant on a banded
    # trait is the one failure that silently DELETES a HUD row.
    if template.cheat_page is not None:
        cp = template.cheat_page

        # (owner, trait) -> top band max. inf when a band omits 'max' (open-ended
        # top band), which means no cap can be derived and none is required.
        _banded: Dict[tuple, float] = {}
        for item in template.sidebar_items or []:
            if not isinstance(item, dict):
                continue
            if item.get("type") not in ("trait_words", "trait_bar", "trait_status_text"):
                continue
            _bands = item.get("bands")
            if not isinstance(_bands, list) or not _bands:
                continue
            _bt = item.get("trait")
            if not isinstance(_bt, str) or not _bt:
                continue
            _owner = item.get("trait_owner", "player")
            _key = (item.get("npc_id") or "player") if _owner == "npc" else "player"
            _maxes = [b.get("max") for b in _bands if isinstance(b, dict)]
            _top = float("inf") if (_maxes and _maxes[-1] is None) else max(
                (m for m in _maxes if isinstance(m, (int, float))), default=float("inf")
            )
            prev = _banded.get((_key, _bt))
            _banded[(_key, _bt)] = _top if prev is None else max(prev, _top)

        _hidden_traits = {tl.key for tl in template.trait_labels if tl.hidden}

        if not cp.grants:
            errors.append(
                "[ui.cheat_page] is authored but declares no [[ui.cheat_page.grants]] rows — "
                "the page would render a title and nothing else (add rows or remove the block)"
            )
        # The join block is this page's only advertising. Without it a player who has
        # no code sees a bare box and cannot tell what it is for or where to get one —
        # the commonest complaint in the 26 shipped cheat surfaces that were studied.
        if not cp.join_note:
            errors.append(
                "[ui.cheat_page] is authored but 'join_note' is missing — a player without a "
                "code sees only an empty box, so the page must say in one line what the box is "
                "for (the url comes from 'join_url', or falls back to [project] support_url)"
            )
        if not cp.join_url and not template.project.support_url:
            errors.append(
                "[ui.cheat_page] is authored but neither 'join_url' nor [project] support_url is "
                "set — the join line would have nowhere to point"
            )
        # Same rule as project.support_url (see the scheme check above): this lands in
        # an href in a published file, so a scheme-less value becomes a relative link.
        if cp.join_url and not cp.join_url.startswith(("http://", "https://")):
            errors.append("[ui.cheat_page] join_url must start with http:// or https://")
        # The sidebar, setup.infoPages and setup.commitMoment are all emitted inside
        # the time-system section, which the generator only appends when time is
        # enabled. Without it the button has nowhere to live and a grant could not
        # commit — so this is a hard requirement, not a warning.
        if template.time is not None and not template.time.enabled:
            errors.append(
                "[ui.cheat_page] requires [time] enabled = true — the sidebar button and the "
                "info-page machinery the grants commit through are only emitted for "
                "time-enabled games"
            )

        _seen_rows: Dict[tuple, int] = {}
        _seen_ids: Dict[str, int] = {}
        _raw_rows = template._cheat_raw_rows or []
        for i, g in enumerate(cp.grants):
            ctx = f"ui.cheat_page.grants[{i}]"
            raw = _raw_rows[i] if i < len(_raw_rows) else {}

            # `id` is load-bearing in two places that outlive this build: it is the
            # unlock flag stored in the player's save, and it is the key the codes file
            # is matched on. Restricting it to [a-z0-9_] keeps it safe as both a flag
            # name and a TOML bare key.
            if not g.id:
                errors.append(
                    f"{ctx}: 'id' is required — it is the unlock flag saved in the player's "
                    f"save file and the key this row's code is looked up by"
                )
            elif not set(g.id) <= set("abcdefghijklmnopqrstuvwxyz0123456789_"):
                errors.append(
                    f"{ctx}: 'id' must be lowercase letters, digits and underscores only, "
                    f"got '{g.id}' (it becomes a flag name and a TOML key)"
                )
            elif g.id in _seen_ids:
                errors.append(
                    f"{ctx}: duplicate id '{g.id}' "
                    f"(already used at ui.cheat_page.grants[{_seen_ids[g.id]}]) — one code per "
                    f"row, so ids must be unique"
                )
            else:
                _seen_ids[g.id] = i

            if not g.label:
                errors.append(
                    f"{ctx}: 'label' is required (non-empty string) — it is the row's button text"
                )
            if not g.trait:
                errors.append(f"{ctx}: 'trait' is required (string)")
            if g.targetType not in ("player", "npc"):
                errors.append(
                    f"{ctx}: 'targetType' must be 'player' or 'npc', got '{g.targetType}' "
                    f"(the cheat page writes traits only)"
                )
            if g.op not in ("add", "set"):
                errors.append(
                    f"{ctx}: 'op' must be 'add' or 'set', got '{g.op}' "
                    f"(the cheat page writes traits only)"
                )
            if not isinstance(g.value, (int, float)) or isinstance(g.value, bool):
                errors.append(f"{ctx}: 'value' must be a number, got {g.value!r}")

            # owner resolution + NPC existence
            _owner_key = "player"
            if g.targetType == "npc":
                if not g.npcId:
                    errors.append(f"{ctx}: 'npcId' is required when targetType='npc'")
                elif g.npcId not in _npc_ids_for_sidebar:
                    errors.append(f"{ctx}: npcId '{g.npcId}' not found in NPC definitions")
                else:
                    _owner_key = g.npcId
                    _npc = next((n for n in template.npcs if n.id == g.npcId), None)
                    if _npc is not None and g.trait and g.trait not in (_npc.core_traits or {}):
                        errors.append(
                            f"{ctx}: NPC '{g.npcId}' has no '{g.trait}' in core_traits "
                            f"(declare it before use)"
                        )
            elif g.trait and g.trait not in _player_trait_keys:
                errors.append(
                    f"{ctx}: trait '{g.trait}' not found in [player.core_traits] "
                    f"(declare it with an initial value before use)"
                )

            # duplicates — two rows writing the same meter is a UI bug, not a feature
            if g.trait:
                _dup_key = (_owner_key, g.trait, g.op)
                if _dup_key in _seen_rows:
                    errors.append(
                        f"{ctx}: duplicate cheat row for trait '{g.trait}' "
                        f"(already declared at ui.cheat_page.grants[{_seen_rows[_dup_key]}])"
                    )
                else:
                    _seen_rows[_dup_key] = i

            # authored-key hygiene — catches subject/trait_key/operator mixups
            errors.extend(_validate_effect_field_names(raw, ctx))

            # causal state is out of bounds, by design
            for _bad in (
                "flag", "flagEffects", "flag_effects", "quest", "questEffects",
                "questId", "stage", "nodeId", "targetPassage", "effects", "costs",
                "time_progression_minutes", "itemEffects",
            ):
                if _bad in raw:
                    errors.append(
                        f"{ctx}: field '{_bad}' is not allowed on a cheat-page row — the page "
                        f"grants TRAITS ONLY (no flags, no quests, no items, no scene jumps). "
                        f"Causality lives in the game, not in a cheat row."
                    )

            if g.trait:
                # <slug>_stage and friends are arc counters wearing a number
                if _classify_stage_trait(g.trait, _trait_registries_for_validate) is not None:
                    errors.append(
                        f"{ctx}: trait '{g.trait}' is a stage/arc counter — never grant one from "
                        f"the cheat page (advance the arc, don't set the number). Exclusive bands "
                        f"and first-time clauses skip forever once jumped."
                    )
                if g.trait in _hidden_traits:
                    errors.append(
                        f"{ctx}: trait '{g.trait}' is declared hidden in [[traits.labels]] (an "
                        f"internal counter) — the cheat page grants player-facing traits only"
                    )

                # banding: the cap rules
                _ceiling = _banded.get((_owner_key, g.trait))
                if _ceiling is not None and _ceiling != float("inf"):
                    if g.cap is None:
                        errors.append(
                            f"{ctx}: trait '{g.trait}' is banded by a sidebar item but the row "
                            f"declares no 'cap' — an uncapped grant can push the value past the "
                            f"top band, which makes a trait_status_text row VANISH from the "
                            f"sidebar and drops a trait_bar's band overlay. Add cap = {int(_ceiling)}."
                        )
                    elif g.cap > _ceiling:
                        errors.append(
                            f"{ctx}: cap {g.cap} exceeds the top band max ({int(_ceiling)}) for "
                            f"trait '{g.trait}' — a cap above the last band leaves the value unbanded"
                        )
                    if not g.clamp:
                        errors.append(
                            f"{ctx}: clamp = false is not allowed on banded trait '{g.trait}' — "
                            f"without the 0-100 clamp the value escapes every band"
                        )
                    if g.op == "set" and isinstance(g.value, (int, float)) and g.value > _ceiling:
                        errors.append(
                            f"{ctx}: op = 'set' writes {g.value} to banded trait '{g.trait}', "
                            f"above its top band max ({int(_ceiling)}) — the sidebar row would vanish"
                        )
                if g.cap is not None and g.cap > 100 and g.clamp:
                    errors.append(
                        f"{ctx}: cap {g.cap} is above 100 but clamp is true — the engine clamps to "
                        f"0-100 BEFORE applying the cap, so the cap is unreachable "
                        f"(set clamp = false for an unbounded resource)"
                    )

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

    # ===== Role labels (F10) — the one rule a machine can hold here =====
    # It cannot invent the words. It CAN refuse two people wearing the same label,
    # which is the only thing that makes a label worth having: `brother` is fine
    # with one brother and useless with two. Measured in this repo before the field
    # existed — one game's cast has two characters whose relationship both begin
    # "Your brother", and that is the game whose reader said "I don't know who is
    # who".
    seen_roles: Dict[str, str] = {}
    for i, n in enumerate(template.npcs):
        role = (n.role or "").strip()
        if not role:
            continue
        if len(role.split()) > 5:
            errors.append(
                f"npcs[{i}] '{n.id}' role '{role}' is {len(role.split())} words. A role is a "
                f"LABEL under the name (1-3 words); a sentence about them belongs in "
                f"`relationship`, which the cast page renders."
            )
        key = role.casefold()
        if key in seen_roles:
            errors.append(
                f"npcs[{i}] '{n.id}' role '{role}' is already used by '{seen_roles[key]}'. "
                f"A role label has to be unique in the cast or it tells the player nothing — "
                f"carry what separates them (birth order, side of the family, a place): "
                f"'elder brother' / 'younger brother', not 'brother' twice."
            )
        else:
            seen_roles[key] = n.id

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

    # ===== Description variants validation (per-location) =====
    for l in template.locations:
        for vi, var in enumerate(l.description_variants):
            where = f"location '{l.id}' description_variants[{vi}]"
            if not isinstance(var, dict):
                errors.append(f"{where} must be a dict of {{ conditions, text }}")
                continue
            if not str(var.get("text") or "").strip():
                errors.append(f"{where} has no text")
            cond = var.get("conditions")
            if not isinstance(cond, dict) or not cond:
                errors.append(f"{where} has no conditions — a variant with nothing to "
                              f"match on would render forever and hide the base description")
                continue
            # ⚠️ setup.triggerConditionsSatisfied returns TRUE for any conditions{}
            # missing `version`, with no build error. A fail-open here is worse than
            # having no variants at all: the first variant would render permanently and
            # the location's own description would never be seen again.
            if str(cond.get("version") or "") != "1.0":
                errors.append(f'{where} conditions must carry version = "1.0" — without '
                              f"it the engine fails OPEN and this variant renders always")
            if not l.description:
                errors.append(f"{where} needs a base `description` on the location to fall "
                              f"back to when no variant matches")

    # ===== Location entry-cost (travel friction) validation =====
    for l in template.locations:
        if not l.costs:
            continue
        if not isinstance(l.costs, dict):
            errors.append(f"location '{l.id}' costs must be a dict (e.g. {{ time = 30, energy = 10 }})")
            continue
        for k, v in l.costs.items():
            if not isinstance(v, (int, float)) or isinstance(v, bool):
                errors.append(f"location '{l.id}' costs['{k}'] must be a number")
            elif v < 0:
                errors.append(f"location '{l.id}' costs['{k}'] must not be negative")

    # ===== Story validation (optional) =====
    canvas_ids = {c.id for c in getattr(template, "canvases", [])}
    if template.starting_canvas and template.starting_canvas not in canvas_ids:
        errors.append(
            f"starting_canvas '{template.starting_canvas}' not found in canvases"
        )

    loc_index = {l.id: l for l in template.locations}

    # Node universe for resolving choice/exit_block node references.
    # nodeIds in the TOML come in two forms:
    #   - Bare:      "result_makeout"                          → resolves within the containing canvas
    #   - Qualified: "loop_franks_bedroom_sex.result_makeout"  → resolves globally
    # Build both lookup structures once, then use them in the per-node validator below.
    nodes_by_canvas: Dict[str, Set[str]] = {
        c.id: {n.id for n in c.nodes}
        for c in getattr(template, "canvases", [])
    }
    all_qualified_nodes: Set[str] = {
        f"{c.id}.{n.id}"
        for c in getattr(template, "canvases", [])
        for n in c.nodes
    }

    def _node_ref_resolves(ref: str, containing_canvas: str) -> bool:
        """A nodeId is either bare (same-canvas) or qualified (canvas.node)."""
        if not ref:
            return False
        if "." in ref:
            return ref in all_qualified_nodes
        return ref in nodes_by_canvas.get(containing_canvas, set())

    # Build NPC id set once for trigger.npc + trigger.requires_npc validators.
    # (npc_id_set built earlier at line ~2198 is scoped inside phone validation.)
    canvas_npc_ids = {n.id for n in template.npcs}

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

            # Phase A — Lane 2/3 NPC presence gate validation.
            if c.trigger.requires_npc and c.trigger.requires_npc not in canvas_npc_ids:
                errors.append(
                    f"canvases[{ci}].trigger.requires_npc "
                    f"'{c.trigger.requires_npc}' not found in npcs"
                )
            elif c.trigger.requires_npc and c.trigger.requires_npc in canvas_npc_ids:
                # Phase A author trap (2026-05-14 PM): if requires_npc is set
                # but the NPC has no declared [[npcs.schedules]], runtime
                # presence falls back to canvas-derived inference — which can
                # include the very canvas that requires the NPC. Almost always
                # an authoring oversight. Warn, don't block.
                _trap_npc = next(
                    (n for n in template.npcs if n.id == c.trigger.requires_npc),
                    None,
                )
                if _trap_npc is not None and not _trap_npc.schedules:
                    import warnings as _w
                    _w.warn(
                        f"canvases[{ci}] '{c.id}' has requires_npc = "
                        f"'{c.trigger.requires_npc}' but that NPC has no "
                        f"declared [[npcs.schedules]]. Runtime presence will "
                        f"fall back to canvas-derived inference, which can "
                        f"include this very canvas in the inference set — "
                        f"usually not what you want. Add a [[npcs.schedules]] "
                        f"entry for '{c.trigger.requires_npc}'.",
                        UserWarning,
                        stacklevel=2,
                    )

            # Gap-fix (2026-05-14) — trigger.npc was previously read by 3
            # downstream validators (substitution_only conflict + repeatable
            # uniqueness checks) but never cross-referenced against the npcs
            # list. Now it is.
            if c.trigger.npc and c.trigger.npc not in canvas_npc_ids:
                errors.append(
                    f"canvases[{ci}].trigger.npc "
                    f"'{c.trigger.npc}' not found in npcs"
                )
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

            # L2-2 — Lane 2 anti-toggle cooldown: validate entry_only_from
            # location slugs exist + warn if used on non-random canvas.
            for ei, loc_id in enumerate(c.trigger.entry_only_from or []):
                if loc_id not in loc_index:
                    errors.append(
                        f"canvases[{ci}].trigger.entry_only_from[{ei}] '{loc_id}' "
                        f"does not match any location in this project"
                    )
            if (c.trigger.entry_only_from or []) and c.trigger.trigger_mode != "random":
                import warnings as _w
                _w.warn(
                    f"canvases[{ci}] '{c.id}' has entry_only_from set but trigger_mode "
                    f"is '{c.trigger.trigger_mode}'. The anti-toggle filter only applies "
                    f"to random-mode encounters (checkRandomEncounters). The field will "
                    f"be ignored on manual-mode canvases.",
                    UserWarning,
                    stacklevel=2,
                )

            # PRD 25 — Lane 3 substitution rule validation
            for ri, rule in enumerate(c.trigger.substitutions or []):
                ctx = f"canvases[{ci}].trigger.substitutions[{ri}]"
                target_id = rule.get("target_canvas_id")
                if not target_id:
                    errors.append(f"{ctx}.target_canvas_id is required")
                elif target_id not in canvas_ids:
                    errors.append(
                        f"{ctx}.target_canvas_id '{target_id}' does not match any canvas in this project"
                    )
                chance_val = rule.get("chance")
                if chance_val is None:
                    errors.append(f"{ctx}.chance is required")
                elif not isinstance(chance_val, (int, float)) or chance_val < 0.0 or chance_val > 1.0:
                    errors.append(f"{ctx}.chance must be a float in [0.0, 1.0], got {chance_val!r}")

            # Doc 69 Item 1 — Pattern B exclusive_group cross-rule validation.
            # Walk substitution rules grouped by exclusive_group name.
            # Checks: chance sum per group, duplicate target across groups +
            # group/independent boundary, single-rule group.
            _sub_groups: Dict[str, List[Tuple[int, Dict[str, Any]]]] = {}
            _sub_independents: List[Tuple[int, Dict[str, Any]]] = []
            _sub_target_to_group: Dict[str, Optional[str]] = {}
            for ri, rule in enumerate(c.trigger.substitutions or []):
                if not isinstance(rule, dict):
                    continue
                group = rule.get("exclusive_group")
                target_id = rule.get("target_canvas_id")
                if isinstance(group, str) and group.strip():
                    group = group.strip()
                    _sub_groups.setdefault(group, []).append((ri, rule))
                    if target_id:
                        if target_id in _sub_target_to_group:
                            prev = _sub_target_to_group[target_id]
                            if prev != group:
                                errors.append(
                                    f"canvases[{ci}].trigger.substitutions: target_canvas_id "
                                    f"'{target_id}' appears in exclusive_group '{group}' AND "
                                    f"{'exclusive_group ' + repr(prev) if prev else 'independent rules'}. "
                                    f"Each target can be claimed by at most one group/independent. "
                                    f"See Doc 69 §3.6."
                                )
                        else:
                            _sub_target_to_group[target_id] = group
                else:
                    _sub_independents.append((ri, rule))
                    if target_id:
                        if target_id in _sub_target_to_group:
                            prev = _sub_target_to_group[target_id]
                            if prev is not None:
                                errors.append(
                                    f"canvases[{ci}].trigger.substitutions: target_canvas_id "
                                    f"'{target_id}' appears as an independent rule AND in "
                                    f"exclusive_group '{prev}'. Each target can be claimed by at "
                                    f"most one group/independent. See Doc 69 §3.6."
                                )
                        else:
                            _sub_target_to_group[target_id] = None
            # Per-group chance-sum + single-rule checks.
            import warnings as _w_subgroup
            for group_name, group_rules in _sub_groups.items():
                # Single-rule group → WARN (no behavioral difference from
                # independent; signals likely authoring oversight).
                if len(group_rules) == 1:
                    _w_subgroup.warn(
                        f"canvases[{ci}] '{c.id}' exclusive_group '{group_name}' has only one "
                        f"substitution rule. Behavior is identical to an independent rule — "
                        f"drop the `exclusive_group` field unless you plan to add more rules. "
                        f"See Doc 69 §3.6.",
                        UserWarning,
                        stacklevel=2,
                    )
                # Chance-sum check (Doc 69 §3.6).
                chance_sum = 0.0
                for _ri, gr in group_rules:
                    cv = gr.get("chance")
                    if isinstance(cv, (int, float)):
                        chance_sum += float(cv)
                if chance_sum > 1.5:
                    errors.append(
                        f"canvases[{ci}] '{c.id}' exclusive_group '{group_name}' chance sum is "
                        f"{chance_sum:.3f} (> 1.5). Buckets beyond 1.0 can never fire; this is a "
                        f"major authoring confusion. See Doc 69 §3.6."
                    )
                elif chance_sum > 1.0:
                    _w_subgroup.warn(
                        f"canvases[{ci}] '{c.id}' exclusive_group '{group_name}' chance sum is "
                        f"{chance_sum:.3f} (> 1.0). Buckets beyond 1.0 can never fire — the rules "
                        f"after that point are dead code. See Doc 69 §3.6.",
                        UserWarning,
                        stacklevel=2,
                    )

            # PRD 25 §4.3 #3 — substitution_only + npcId conflict warning
            if c.trigger.substitution_only and c.trigger.npc:
                import warnings as _w
                _w.warn(
                    f"canvases[{ci}] '{c.id}' has substitution_only = true AND npc set "
                    f"('{c.trigger.npc}'). The canvas will be excluded from NPC portrait + "
                    f"solo activity selectors but the npc reference may indicate authoring intent "
                    f"to also surface as a portrait. Verify intentional.",
                    UserWarning,
                    stacklevel=2,
                )

            # Doc 69 Item 2 §4.6 — pre_substitution_effects without substitutions
            # warning. If author sets pre-sub effects but no substitution rules,
            # the effects fire on every canvas entry — same as body effects.
            # Likely an authoring mistake (intended substitution_only canvas?).
            if (c.trigger.pre_substitution_effects or []) and not (c.trigger.substitutions or []):
                import warnings as _w
                _w.warn(
                    f"canvases[{ci}] '{c.id}' has pre_substitution_effects but no "
                    f"substitutions. The effects will fire on every canvas entry, "
                    f"identical to body-level effects. Consider moving them to the "
                    f"canvas's body or exit_block effects. See Doc 69 §4.6.",
                    UserWarning,
                    stacklevel=2,
                )

            # PRD 25 §4.3 #4 — substitutions + trigger.chance both set warning
            if (c.trigger.substitutions or []) and c.trigger.chance is not None:
                import warnings as _w
                _w.warn(
                    f"canvases[{ci}] '{c.id}' has both substitutions (Lane 3 dispatcher) AND "
                    f"trigger.chance set (Lane 2 random encounter). The canvas would behave as both "
                    f"a substitution dispatcher AND a random-fire encounter. Likely an authoring mistake.",
                    UserWarning,
                    stacklevel=2,
                )

        # Layer 3 — silent-Navigation gate.
        # Mirrors v1.py:10240 _get_return_location() — if a canvas has no
        # resolving trigger.location, the engine's return_target falls back to
        # the literal "Navigation" passage. Any trigger-type exit (explicit OR
        # default-omitted) on such a canvas silently lands the player on the
        # global location list. Hard-fail with an explicit suggested fix.
        return_will_resolve = bool(
            c.trigger and c.trigger.location and c.trigger.location in loc_index
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
                # Layer 3 — silent-Navigation gate (single-link form).
                if dest == "trigger" and not return_will_resolve:
                    eb_text = (eb.text or "").strip() or "<no text>"
                    errors.append(
                        f"canvases[{ci}].nodes[{ni}].exit_block ('{c.id}.{n.id}') uses "
                        f"destinationType='trigger' but canvas has no resolving "
                        f"trigger.location — runtime return_target would silently "
                        f"land on the Navigation page. Exit text: {eb_text!r}. "
                        f"Fix: change destinationType to 'specific' and set "
                        f"locationId to the location the player came from."
                    )
                if dest == "specific":
                    loc_slug = eb.config.get("locationId")
                    if not loc_slug or loc_slug not in loc_index:
                        errors.append(
                            f"canvases[{ci}].nodes[{ni}].exit_block.config.locationId not found in locations"
                        )
                if dest == "node":
                    # exit_block single-link form: destinationId must resolve.
                    # Silent fallback to trigger location is gone — broken refs hard-fail here.
                    dest_node_ref = eb.config.get("destinationId")
                    if not dest_node_ref:
                        errors.append(
                            f"canvases[{ci}].nodes[{ni}].exit_block.config.destinationId "
                            f"required for destinationType 'node'"
                        )
                    elif not _node_ref_resolves(dest_node_ref, c.id):
                        errors.append(
                            f"canvases[{ci}].nodes[{ni}].exit_block.config.destinationId "
                            f"'{dest_node_ref}' does not resolve to any node "
                            f"(bare = same-canvas '{c.id}', qualified = '<canvas>.<node>')"
                        )
            else:
                for chi, ch in enumerate(eb.choices):
                    if ch.targetType not in ("trigger", "location", "node"):
                        errors.append(
                            f"canvases[{ci}].nodes[{ni}].choices[{chi}].targetType invalid"
                        )
                    # Layer 3 — silent-Navigation gate (choices form).
                    # Mirrors v1.py:10942 default (`choice.get('targetType', 'trigger')`):
                    # omitted targetType behaves as 'trigger' at runtime.
                    effective_tt = ch.targetType or "trigger"
                    if effective_tt == "trigger" and not return_will_resolve:
                        ch_text = (ch.text or "").strip() or "<no text>"
                        errors.append(
                            f"canvases[{ci}].nodes[{ni}].choices[{chi}] ('{c.id}.{n.id}') "
                            f"uses targetType='trigger' but canvas has no resolving "
                            f"trigger.location — runtime return_target would silently "
                            f"land on the Navigation page. Choice text: {ch_text!r}. "
                            f"Fix: change targetType to 'location' and add a locationId "
                            f"for the location the player came from."
                        )
                    if ch.targetType == "location":
                        if not ch.locationId or ch.locationId not in loc_index:
                            errors.append(
                                f"canvases[{ci}].nodes[{ni}].choices[{chi}].locationId not found"
                            )
                    if ch.targetType == "node":
                        if not ch.nodeId:
                            errors.append(
                                f"canvases[{ci}].nodes[{ni}].choices[{chi}].nodeId required for targetType 'node'"
                            )
                        elif not _node_ref_resolves(ch.nodeId, c.id):
                            # Silent fallback to Navigation is gone — broken refs hard-fail.
                            errors.append(
                                f"canvases[{ci}].nodes[{ni}].choices[{chi}].nodeId "
                                f"'{ch.nodeId}' does not resolve to any node "
                                f"(bare = same-canvas '{c.id}', qualified = '<canvas>.<node>'); "
                                f"choice text: {ch.text!r}"
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
        and not c.trigger.substitution_only  # PRD 25 — substitution_only canvases
        # are excluded from NPC portrait + solo activity selectors at runtime,
        # so they cannot compete for the location's portrait slot. Skip them
        # in the overlap check to avoid spurious warnings.
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

    # ===== Player-portrait validation (optional) =====
    if template.player_portrait is not None:
        pp = template.player_portrait
        # At least one image must resolve or the sidebar renders nothing but the onerror SVG.
        if not (pp.default_image or pp.naked_image or pp.outfits):
            errors.append(
                "player_portrait is enabled but declares no images "
                "(need default_image and/or outfits and/or the undress-override images)"
            )
        for oi, o in enumerate(pp.outfits):
            if not o.image:
                errors.append(f"player_portrait.outfits[{oi}].image is required")
        # Soft: unknown worn_type / trait refs are not blocked — the resolver falls through to
        # default_image, matching clothing's warn-not-block policy for the `type` tag (Doc 72).

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

    # ===== Effect `op` must be an op the RUNTIME actually runs =====
    #
    # ⚠️ SILENT NO-OP, AND THE MOST EXPENSIVE KIND OF BUG THIS FILE CAN LET THROUGH.
    # `window.applyTraitEffect` runs 'add' and 'set' and falls through to
    # "// Unknown op; do nothing" + return on anything else
    # (twee_comprehensive/generators/v2.py:5742-5751). Nothing normalises the value —
    # the string "subtract" appears nowhere in this file or in the generator. So an
    # effect written `op = "subtract"` parses, validates, builds, and emits verbatim
    # into the HTML, where it does nothing at all.
    #
    # Measured on two shipped games authored from the same instructions: 35 dead
    # effects in one and 70 in the other. In the first, a whole declared meter never
    # moved for the entire game, twenty activities never charged the energy they said
    # they cost, and the only NPC penalty in the game never applied. Every ship gate
    # passed it and so did a live play-through, because a number that never changes
    # looks exactly like a number the player has not moved yet.
    #
    # `op` is already validated this way for cheat-page grants further down; this is
    # the same check applied to the effects that are actually the game.
    _LIVE_OPS = {
        "trait": {"add", "set"},
        "flag": {"set", "unset", "toggle"},
        "quest": {"start", "update", "complete", "cancel"},
    }

    def _check_ops(node: Any, ctx: str, out: List[str]) -> None:
        if is_dataclass(node) and not isinstance(node, type):
            node = asdict(node)
        if isinstance(node, dict):
            op = node.get("op")
            if isinstance(op, str) and "subject" not in node and "operator" not in node:
                kind = ("flag" if node.get("flag") else
                        "quest" if (node.get("quest_id") or node.get("questId")
                                    or node.get("quest")) else
                        "trait" if node.get("trait") else None)
                if kind and op not in _LIVE_OPS[kind]:
                    out.append(
                        f"{ctx}: {kind} effect uses op='{op}', which the engine discards "
                        f"(applyTraitEffect runs only {sorted(_LIVE_OPS[kind])}, "
                        f"generators/v2.py:5742-5751). To take something away write "
                        f"op='add' with a NEGATIVE value; a quantity like money also "
                        f"needs clamp=false."
                    )
            for v in node.values():
                _check_ops(v, ctx, out)
        elif isinstance(node, (list, tuple)):
            for v in node:
                _check_ops(v, ctx, out)

    _op_errors: List[str] = []
    for ci, c in enumerate(template.canvases):
        _check_ops(c, f"canvases[{ci}] '{c.id}'", _op_errors)
    # Collapse to one line per canvas: a game with 70 of these should not emit 70
    # near-identical errors and bury everything else the validator found.
    _seen_op_ctx: Set[str] = set()
    for e in _op_errors:
        key = e.split(":", 1)[0]
        if key not in _seen_op_ctx:
            _seen_op_ctx.add(key)
            errors.append(e)
    if len(_op_errors) > len(_seen_op_ctx):
        errors.append(
            f"({len(_op_errors)} dead-op effects across {len(_seen_op_ctx)} canvases "
            f"in total)"
        )

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
            # Restrict OR-logic in stage helpers (2026-05-03).
            # OR-helpers produce the awkward "Two paths to advance: Path A /
            # Path B" rendering in the Pattern 2 goal block on the Quests
            # page. RTS-aligned pattern is to express multi-path goals as
            # separate transition canvases, each with its own AND-logic gate.
            sh_logic = (sh.conditions.get("logic") or "AND").upper()
            if sh_logic == "OR":
                errors.append(
                    f"{ctx} ('{sh.name}'): OR-logic is not allowed in "
                    f"stage_helpers. Refactor as separate transition canvases "
                    f"— one per path — each with inline AND-logic trigger "
                    f"conditions. See jake_stage_1 refactor (2026-05-03) as "
                    f"the canonical example."
                )

        # Pattern 2 v2.2 (2026-05-04) — flag-setter coverage check.
        # For each is_true flag gate in any non-dev_only helper, verify some
        # non-dev canvas sets the flag. Otherwise the stage is unreachable in
        # normal play (either authoring bug or unfinished out-of-slice content).
        # Validator emits warnings, not errors — preserves the _lint pattern
        # and doesn't block content-in-progress builds.
        if template.canvases:
            import warnings as _w

            # Build flag → setter coverage set, excluding dev shortcuts.
            # Dev shortcuts have a trigger condition `dev_mode_enabled is_true`.
            nondev_set_flags: Set[str] = set()
            for cv in template.canvases:
                is_dev = False
                if cv.trigger and isinstance(cv.trigger.conditions, dict):
                    for it in (cv.trigger.conditions.get("items") or []):
                        if (
                            isinstance(it, dict)
                            and it.get("flag_key") == "dev_mode_enabled"
                            and it.get("operator") == "is_true"
                        ):
                            is_dev = True
                            break
                if is_dev:
                    continue
                nondev_set_flags |= _extract_flags_set_by_canvas(cv)

            for sh in template.stage_helpers:
                if sh.dev_only:
                    continue
                items = sh.conditions.get("items") or []
                for item in items:
                    if not isinstance(item, dict):
                        continue
                    if item.get("type") != "flag" or item.get("operator") != "is_true":
                        continue
                    flag_key = item.get("flag_key", "")
                    if not flag_key or flag_key in nondev_set_flags:
                        continue
                    _w.warn(
                        f"HINT LINTER WARN engine.stage_helpers "
                        f"('{sh.name}'): flag '{flag_key}' is required for "
                        f"stage advancement but no non-dev canvas sets it. "
                        f"Players cannot advance through this stage in normal "
                        f"play. Either author the missing setter scene OR "
                        f"mark the helper as `dev_only = true` to silence "
                        f"this warning (acknowledges the stage is dev-shortcut-"
                        f"only in current scope).",
                        UserWarning,
                        stacklevel=2,
                    )

    # ===== E10: stage_gate validation on hint conditions =====
    # Tri-required: stage_npc, stage_op, stage_value all set together.
    # stage_npc must reference an NPC with arc_stages declared.
    # 0 ≤ stage_value < len(arc_stages).
    if template.story_arc and template.story_arc.hints:
        npc_arc_lookup = {n.id: n.arc_stages for n in template.npcs if n.arc_stages}
        all_npc_ids = {n.id for n in template.npcs}
        valid_stage_ops = {"eq", "gte", "lte"}
        for ti, t in enumerate(template.story_arc.hints.templates):
            ctx = f"story_arc.hints.templates[{ti}]"
            cond = t.condition
            if cond is None:
                # No condition is fine — the hint always applies (if anything ever
                # consumes ungated hints in this layer).
                if t.npc_id and t.npc_id not in all_npc_ids:
                    errors.append(
                        f"{ctx}.npc_id '{t.npc_id}' not found in NPC definitions"
                    )
                continue
            sg_set = sum(
                1
                for v in (cond.stage_npc, cond.stage_op, cond.stage_value)
                if v is not None
            )
            if 0 < sg_set < 3:
                errors.append(
                    f"{ctx}.condition: stage_npc, stage_op, and stage_value "
                    f"must all be set together (got {sg_set} of 3)"
                )
            elif sg_set == 3:
                if cond.stage_op not in valid_stage_ops:
                    errors.append(
                        f"{ctx}.condition.stage_op must be one of "
                        f"{sorted(valid_stage_ops)}, got '{cond.stage_op}'"
                    )
                if cond.stage_npc not in npc_arc_lookup:
                    if cond.stage_npc in all_npc_ids:
                        errors.append(
                            f"{ctx}.condition.stage_npc '{cond.stage_npc}' "
                            f"references an NPC without arc_stages — declare "
                            f"arc_stages on the NPC before gating hints on it"
                        )
                    else:
                        errors.append(
                            f"{ctx}.condition.stage_npc '{cond.stage_npc}' "
                            f"not found in NPC definitions"
                        )
                else:
                    arc_len = len(npc_arc_lookup[cond.stage_npc])
                    sv = cond.stage_value
                    if sv < 0 or sv >= arc_len:
                        errors.append(
                            f"{ctx}.condition.stage_value {sv} out of range "
                            f"for NPC '{cond.stage_npc}' arc_stages "
                            f"(must be 0..{arc_len - 1})"
                        )
            # Validate routing field if explicitly set.
            if t.npc_id and t.npc_id not in all_npc_ids:
                errors.append(
                    f"{ctx}.npc_id '{t.npc_id}' not found in NPC definitions"
                )

            # E14 — validate trait_checks shape (each item must have
            # subject + (trait_key XOR flag_key) + operator).
            for tci, tc in enumerate(cond.trait_checks or []):
                tc_ctx = f"{ctx}.condition.trait_checks[{tci}]"
                if not isinstance(tc, dict):
                    errors.append(f"{tc_ctx}: must be a dict, got {type(tc).__name__}")
                    continue
                tc_type = tc.get("type")
                if tc_type not in ("trait", "flag"):
                    errors.append(
                        f"{tc_ctx}.type must be 'trait' or 'flag', got '{tc_type}'"
                    )
                tc_subject = tc.get("subject")
                if tc_subject not in ("player", "npc"):
                    errors.append(
                        f"{tc_ctx}.subject must be 'player' or 'npc', got '{tc_subject}'"
                    )
                tc_op = tc.get("operator")
                valid_ops = {"eq", "gte", "lte", "gt", "lt", "is_true", "is_false"}
                if tc_op not in valid_ops:
                    errors.append(
                        f"{tc_ctx}.operator must be one of {sorted(valid_ops)}, "
                        f"got '{tc_op}'"
                    )
                # Cross-field: trait → trait_key required + value; flag → flag_key required.
                if tc_type == "trait":
                    if not tc.get("trait_key"):
                        errors.append(f"{tc_ctx}: type=trait requires trait_key")
                    if "value" not in tc:
                        errors.append(f"{tc_ctx}: type=trait requires value")
                if tc_type == "flag":
                    if not tc.get("flag_key"):
                        errors.append(f"{tc_ctx}: type=flag requires flag_key")
                # NPC subject must reference real NPC.
                if tc_subject == "npc":
                    tc_npc = tc.get("npc_id")
                    if not tc_npc:
                        errors.append(f"{tc_ctx}: subject=npc requires npc_id")
                    elif tc_npc not in all_npc_ids:
                        errors.append(
                            f"{tc_ctx}.npc_id '{tc_npc}' not found in NPC definitions"
                        )

            # 2026-05-10 — arc_complete (boolean badge) and arc_closure_flag
            # (flag-resolved Ready / Complete frame) are mutually exclusive.
            # Author pattern: split into two trait-check-mutex templates instead.
            if t.arc_complete and t.arc_closure_flag:
                errors.append(
                    f"{ctx}: cannot set both `arc_complete = true` and "
                    f"`arc_closure_flag = '{t.arc_closure_flag}'`. They are "
                    f"mutually exclusive — use arc_closure_flag on the "
                    f"pre-completion template + arc_complete on the "
                    f"post-completion template, gated by trait_checks."
                )

            # E22 — validate prerequisite_npc_stage syntax + NPC reference.
            if cond.prerequisite_npc_stage:
                parsed = _parse_prerequisite_npc_stage(cond.prerequisite_npc_stage)
                if parsed is None:
                    errors.append(
                        f"{ctx}.condition.prerequisite_npc_stage "
                        f"'{cond.prerequisite_npc_stage}' must match format "
                        f"'npc_<slug> <op> <int>' (e.g., 'npc_frank >= 2')"
                    )
                else:
                    pre_npc, _, pre_val = parsed
                    if pre_npc not in all_npc_ids:
                        errors.append(
                            f"{ctx}.condition.prerequisite_npc_stage references "
                            f"unknown NPC '{pre_npc}'"
                        )
                    elif pre_npc not in npc_arc_lookup:
                        errors.append(
                            f"{ctx}.condition.prerequisite_npc_stage references "
                            f"NPC '{pre_npc}' without arc_stages — declare "
                            f"arc_stages on the NPC first"
                        )
                    else:
                        arc_len = len(npc_arc_lookup[pre_npc])
                        if pre_val < 0 or pre_val >= arc_len:
                            errors.append(
                                f"{ctx}.condition.prerequisite_npc_stage value "
                                f"{pre_val} out of range for NPC '{pre_npc}' "
                                f"arc_stages (0..{arc_len - 1})"
                            )

    # Pattern 2 — Validate label registries (FAIL on duplicate keys; warn
    # via linter if a helper-referenced trait/flag has no label entry).
    seen_trait_label_keys: Set[str] = set()
    # Build the union of declared core_trait keys (player + every NPC) once, for the
    # hide-only typo warning below.
    _all_core_trait_keys: Set[str] = set((template.player.core_traits or {}).keys())
    for _n in (template.npcs or []):
        _all_core_trait_keys |= set((_n.core_traits or {}).keys())
    for tl in (template.trait_labels or []):
        if not tl.key:
            errors.append("traits.labels entry missing required `key` field")
            continue
        # A hide-only entry (hidden=true) may omit `label` — its sole purpose is to
        # suppress the trait from player-facing dumps, not to render a goal label.
        if not tl.label and not tl.hidden:
            errors.append(f"traits.labels[{tl.key}] missing required `label` field")
        if tl.hidden and tl.key not in _all_core_trait_keys and warnings is not None:
            warnings.append(
                f"traits.labels[{tl.key}] hidden=true but '{tl.key}' is not a declared "
                f"core_trait on the player or any NPC — typo? (the hide will no-op)"
            )
        if tl.key in seen_trait_label_keys:
            errors.append(f"traits.labels duplicate key '{tl.key}'")
        seen_trait_label_keys.add(tl.key)

    seen_flag_label_keys: Set[str] = set()
    for fl in (template.flag_labels or []):
        if not fl.key:
            errors.append("flags.labels entry missing required `key` field")
            continue
        if not fl.label:
            errors.append(f"flags.labels[{fl.key}] missing required `label` field")
        if fl.key in seen_flag_label_keys:
            errors.append(f"flags.labels duplicate key '{fl.key}'")
        seen_flag_label_keys.add(fl.key)

    # E23 — Hint linter (warn-only). Cross-checks hint text against the
    # numeric thresholds, time bands, and gate counts in the matching stage
    # helpers and canvas triggers. Catches the recurring authoring drift
    # documented in 11_Hint_Authoring_Guide.md before publish.
    _lint_hint_templates(template)

    # PRD 48 — Quests Engine V2 schema validation. Only runs for v2 games;
    # v1 games keep using _lint_hint_templates above for their old-shape
    # templates. Validates `quest_cards` entries against canvas + NPC refs.
    if template.project.quests_engine == "v2":
        _validate_quests_cards(
            template.quests_cards,
            template.canvases,
            {n.id for n in template.npcs},
            errors,
        )

    return errors


def _validate_quests_cards(
    cards: List[QuestsCard],
    canvases: List["TemplateCanvas"],
    npc_ids: Set[str],
    errors: List[str],
) -> None:
    """PRD 48 — Validate [[quest_cards]] entries for the V2 engine.

    Mutates `errors` in place. Catches structural issues that would silently
    produce broken cards at runtime (bad slug references, missing labels on
    trait bullets, malformed condition items). Warning-tier issues
    (terminal + ready_canvas both set, group on NPC card) emit Python
    warnings.

    Hard errors (raise):
      - text empty
      - when empty
      - goals item targeting trait/counter without `label`
      - ready_canvas references unknown canvas slug
      - npc_id references unknown NPC slug
      - condition item uses old V1 fields (`type`, `flag_key`, `trait_key`,
        `operator`) — explicit reject to catch migration mistakes
      - priority not an integer
      - condition item has neither `flag` nor `trait` set
      - condition item has both `flag` and `trait` set
    """
    canvas_slugs = {c.id for c in canvases}

    def _is_condition_well_formed(
        item: QuestsCondition, ctx: str, *, require_label: bool
    ) -> None:
        # Detect old-schema field leakage via the raw __dict__ (since we
        # parsed permissively, stray fields are dropped silently — catch at
        # validate time by looking for both flag and trait being None).
        has_flag = item.flag is not None
        has_trait = item.trait is not None
        if not has_flag and not has_trait:
            errors.append(
                f"{ctx}: condition item must set either `flag` or `trait`"
            )
            return
        if has_flag and has_trait:
            errors.append(
                f"{ctx}: condition item must set ONLY ONE of `flag` or "
                f"`trait`, not both"
            )
            return
        if has_flag:
            if item.op not in ("is_true", "is_false"):
                errors.append(
                    f"{ctx}: flag condition op must be is_true/is_false, "
                    f"got {item.op!r}"
                )
        else:  # trait/counter
            if item.subject not in ("player", "npc"):
                errors.append(
                    f"{ctx}: trait condition subject must be 'player' or "
                    f"'npc', got {item.subject!r}"
                )
            if item.subject == "npc" and not item.npc_id:
                errors.append(
                    f"{ctx}: trait condition subject='npc' requires npc_id"
                )
            # ⚠️ NO `ne` HERE, AND THAT IS DELIBERATE (2026-08-24). This is the
            # QUEST-CARD validator, and quest cards are evaluated by a third
            # evaluator — setup.checkQuestsCondition — whose switch has no `ne`
            # case and falls through to `return false`. Widening this whitelist
            # without adding that case would let an author write a condition
            # that is silently always false. Canvas/node/choice conditions are a
            # different path entirely; see engine.md §37.
            if item.op not in ("gte", "lte", "gt", "lt", "eq"):
                errors.append(
                    f"{ctx}: trait condition op must be gte/lte/gt/lt/eq, "
                    f"got {item.op!r}"
                )
            if item.value is None:
                errors.append(f"{ctx}: trait condition requires numeric value")
            if require_label and not item.label:
                errors.append(
                    f"{ctx}: trait/counter goal item must have a `label` "
                    f"(it renders next to the ◯ bullet)"
                )
            if item.subject == "npc" and item.npc_id and item.npc_id not in npc_ids:
                errors.append(
                    f"{ctx}: condition npc_id '{item.npc_id}' not found in "
                    f"[[npcs]]"
                )

    import warnings as _w

    for idx, card in enumerate(cards):
        ctx = f"quest_cards[{idx}]"
        if not card.text:
            errors.append(f"{ctx}: text is required (non-empty)")
        if not card.when:
            errors.append(
                f"{ctx}: when is required (at least one routing condition). "
                f"Every card must scope itself to a state-window."
            )
        for wi, item in enumerate(card.when):
            _is_condition_well_formed(item, f"{ctx}.when[{wi}]", require_label=False)
        for gi, item in enumerate(card.goals):
            _is_condition_well_formed(item, f"{ctx}.goals[{gi}]", require_label=True)
        if card.ready_canvas and card.ready_canvas not in canvas_slugs:
            errors.append(
                f"{ctx}: ready_canvas '{card.ready_canvas}' not found in "
                f"any [[canvases]] block"
            )
        if card.npc_id and card.npc_id not in npc_ids:
            errors.append(
                f"{ctx}: npc_id '{card.npc_id}' not found in [[npcs]]"
            )
        if card.terminal and card.ready_canvas:
            _w.warn(
                f"{ctx}: terminal=true overrides ready_canvas — both are set; "
                f"the ✓ Arc complete frame will render, ready_canvas will be "
                f"ignored. Drop one to silence."
            )
        if card.terminal_text and not card.terminal:
            _w.warn(
                f"{ctx}: terminal_text is set but terminal is not — the label "
                f"only renders inside the terminal frame, so this string is "
                f"dead. Add `terminal = true` or drop terminal_text."
            )
        if card.group and card.npc_id:
            _w.warn(
                f"{ctx}: `group` is Story Goal only (cards without npc_id). "
                f"Setting group on an NPC card has no effect."
            )


def _lint_hint_templates(template: "GameTemplate") -> None:
    """Warn-only linter for [[story_arc.hints.templates]] entries.

    Detects the recurring authoring pitfalls (hallucinated thresholds, time
    band drift, internal name leaks, ✓-as-bullet, etc.) by parsing each
    hint's `text` and cross-checking against the matching stage helper /
    canvas trigger. Emits Python warnings (caught by package_from_toml and
    surfaced as ⚠️ lines in the build output) — does not block the build.
    """
    import re
    import warnings as _warnings

    if not template.story_arc or not template.story_arc.hints:
        return
    templates = template.story_arc.hints.templates
    if not templates:
        return

    # Build lookups once.
    helpers_by_name: Dict[str, Any] = {
        h.name: h for h in (template.stage_helpers or [])
    }
    location_names: Set[str] = {loc.name for loc in template.locations}
    npc_arc_lookup: Dict[str, List[str]] = {
        n.id: n.arc_stages for n in template.npcs if n.arc_stages
    }
    # Pattern 2 (2026-05-01) — label registries for "unlabeled trait/flag" rule
    trait_label_keys: Set[str] = {tl.key for tl in (template.trait_labels or [])}
    flag_label_keys: Set[str] = {fl.key for fl in (template.flag_labels or [])}
    # Collect all schedule blocks per NPC for time-band checks.
    npc_schedules: Dict[str, List[Tuple[str, str, str]]] = {}  # npc_id -> [(start, end, canvas_id)]
    for cv in template.canvases:
        if not cv.trigger:
            continue
        cv_npc = cv.trigger.npc
        if not cv_npc:
            continue
        for s in (cv.trigger.schedules or []):
            if s.start_time and s.end_time:
                npc_schedules.setdefault(cv_npc, []).append((s.start_time, s.end_time, cv.id))

    # Detection rules.
    THRESHOLD_RE = re.compile(
        r"\b(trust|corruption|beauty|arousal|fitness|love|energy|hygiene|calculation|money)\s*[≥>=]+\s*(\d+)",
        re.IGNORECASE,
    )
    COUNTER_RE = re.compile(
        r"(?:×|x)(\d+)\s*(?:sessions|times|visits|helps)|(\d+)\+\s*times",
        re.IGNORECASE,
    )
    TIME_BAND_RE = re.compile(r"(\d{2}:\d{2})\s*[–\-]\s*(\d{2}:\d{2})")
    LOCATION_PAREN_RE = re.compile(r"\(([A-Z][\w\s']+?),\s*\d{2}:\d{2}")
    INTERNAL_NAME_RE = re.compile(r"\b\w+_(count|done|today|open|noticed|revealed|caught|cracked)\b")
    CHECKMARK_AS_BULLET_RE = re.compile(r"\w+\s+✓(?!\s*\(already)")

    INTERNAL_NAME_WHITELIST = {
        # NPC-facing flag names players might see referenced in safe contexts;
        # extend as needed.
    }

    # --- Linter v2 (2026-05-01) — 5 additional rules ---
    TIER_ABBREV_RE = re.compile(r"\bT(\d)\b")
    MONEY_AMOUNT_RE = re.compile(r"\$(\d+)")
    STAGE_ARROW_RE = re.compile(r"Stage\s*\d+\s*[→\-]\s*\d+", re.IGNORECASE)
    ADVANCES_STAGE_RE = re.compile(r"\badvances\s+Stage\s+\d+", re.IGNORECASE)
    THE_X_FLAG_RE = re.compile(r"\bthe\s+[\w\-]+\s+flag\b", re.IGNORECASE)

    FOURTH_WALL_KEYWORDS = (
        "NOT REACHABLE",
        "dev shortcut",
        "dev mode",
        "🔧",
        "slice testing",
        "for slice",
        "in slice",
        "out of scope",
        "TODO",
        "FIXME",
    )
    AUTHOR_SCENE_TAG_PHRASES = (
        "the catch fires",
        "the catch happens",
        "the reveal",
        "first-glance moment",
        "doorway confrontation",
    )
    MONEY_DEBIT_CONTEXT = ("due", "rent", "pay", "owe", "cost", "miss")

    # Build set of known money payouts across all canvases (for rule 2).
    # Effects can live in two places depending on exit_block.type:
    #   - type="choices": each TemplateChoice.choices[].effects (typed objects)
    #   - type="location": exit_block.config["effects"] (raw dicts from TOML)
    known_money_payouts: Set[int] = set()
    for cv in template.canvases:
        for node in (cv.nodes or []):
            eb = node.exit_block
            if not eb:
                continue
            # Typed effects on choices
            for choice in (eb.choices or []):
                for e in (choice.effects or []):
                    if (
                        getattr(e, "trait", None) == "money"
                        and getattr(e, "op", None) == "add"
                        and isinstance(getattr(e, "value", None), (int, float))
                        and e.value > 0
                    ):
                        known_money_payouts.add(int(e.value))
            # Raw effects in config dict (location-type exit_blocks)
            cfg = eb.config or {}
            for e in (cfg.get("effects") or []):
                if not isinstance(e, dict):
                    continue
                if (
                    e.get("trait") == "money"
                    and e.get("op") == "add"
                    and isinstance(e.get("value"), (int, float))
                    and e["value"] > 0
                ):
                    known_money_payouts.add(int(e["value"]))

    def _emit(template_index: int, severity: str, msg: str) -> None:
        # All linter findings are warn-only — these are heuristic checks
        # (helper might not capture branch-inside-shell transitions, OR-logic
        # alternate paths, etc.). Severity label kept for triage.
        ctx = f"story_arc.hints.templates[{template_index}]"
        full_msg = f"HINT LINTER {severity} {ctx}: {msg}"
        _warnings.warn(full_msg, UserWarning, stacklevel=4)

    for ti, t in enumerate(templates):
        text = t.text or ""
        cond = t.condition

        # --- Rule: missing npc_id and no stage_npc → silently dropped ---
        if not t.npc_id and not (cond and cond.stage_npc):
            _emit(
                ti,
                "WARN",
                f"hint has no npc_id and no stage_npc — engine "
                f"setup.getStageHintForNPC skips global templates today (E15 ETA). "
                f"Either add npc_id or wait for E15.",
            )

        # --- Pattern 2 Rule: auto_goal=true + manual " — 🎯 " in text ---
        # Engine renders the goal block automatically; the author's manual goal
        # line will be stripped from display. Warn so the author either removes
        # the manual goal OR sets `auto_goal = false` to opt out.
        if (
            getattr(t, "auto_goal", True)
            and cond and cond.stage_npc and cond.stage_value is not None
            and " — 🎯 " in text
        ):
            _emit(
                ti,
                "WARN",
                "hint has `auto_goal = true` (default) AND a manual ' — 🎯 ' "
                "goal line in text. Engine will auto-render from the helper "
                "and strip the manual portion. Either remove the ' — 🎯 ...' "
                "tail from text, or set `auto_goal = false` to opt out.",
            )

        # --- Rule: ✓ used as bullet character ---
        if CHECKMARK_AS_BULLET_RE.search(text):
            _emit(
                ti,
                "WARN",
                "uses ✓ as a list bullet — players read ✓ as 'completed'. "
                "Replace with • for bullets.",
            )

        # --- Rule: internal name leak ---
        for m in INTERNAL_NAME_RE.finditer(text):
            name = m.group(0)
            if name in INTERNAL_NAME_WHITELIST:
                continue
            _emit(
                ti,
                "WARN",
                f"hint text contains internal variable name '{name}' — "
                f"translate to plain English (e.g., '5+ times' instead of "
                f"'<counter_name> ≥ 5').",
            )

        # --- Rule: location paren references unknown location ---
        for m in LOCATION_PAREN_RE.finditer(text):
            loc = m.group(1).strip()
            if loc not in location_names:
                # Allow common short forms not in [[locations]] (Home, etc.)
                # but still warn if it's likely a typo.
                _emit(
                    ti,
                    "WARN",
                    f"hint mentions location '{loc}' which doesn't match any "
                    f"[[locations]].name in the game. Check for typo.",
                )

        # === Linter v2 (2026-05-01) — 5 additional rules ===

        # --- Rule v2.1: tier abbreviation (T0/T1/T2) leak ---
        for m in TIER_ABBREV_RE.finditer(text):
            _emit(
                ti,
                "WARN",
                f"hint contains tier abbreviation '{m.group(0)}' — players don't "
                f"know what 'T0/T1/T2' means. Use a player-facing label "
                f"(e.g., 'basic shift', 'busy shift') or rename the canvas itself.",
            )

        # --- Rule v2.2: dollar amount doesn't match any scene payout ---
        for m in MONEY_AMOUNT_RE.finditer(text):
            amount = int(m.group(1))
            if amount <= 0 or amount in known_money_payouts:
                continue
            # False-positive filter: if the surrounding ±30 chars look like a
            # debit (rent due, pay, owe, cost, miss), skip — we only check payouts.
            ctx_start = max(0, m.start() - 30)
            ctx_end = min(len(text), m.end() + 30)
            ctx = text[ctx_start:ctx_end].lower()
            if any(w in ctx for w in MONEY_DEBIT_CONTEXT):
                continue
            payouts_str = ", ".join(f"${v}" for v in sorted(known_money_payouts)) or "(none found)"
            _emit(
                ti,
                "WARN",
                f"hint mentions '${amount}' as a payout/earning but no canvas has "
                f"'money += {amount}' in any exit_block effect. Known payouts: "
                f"{payouts_str}. Update hint to match actual scene payouts.",
            )

        # --- Rule v2.3: fourth-wall / dev memo leak ---
        text_lower = text.lower()
        for kw in FOURTH_WALL_KEYWORDS:
            if kw.lower() in text_lower:
                _emit(
                    ti,
                    "WARN",
                    f"hint contains author/dev memo '{kw}' — the player will see this. "
                    f"Either gate the hint with `dev_only = true`, or rewrite as "
                    f"in-fiction text (e.g., 'this story continues in a later chapter').",
                )
                break  # one warning per template — don't flood

        # --- Rule v2.4: engine-jargon stage-arrow framing ---
        for m in STAGE_ARROW_RE.finditer(text):
            _emit(
                ti,
                "WARN",
                f"hint uses engine-jargon stage notation '{m.group(0)}' — players "
                f"see stage labels in the sidebar but not the arrow framing. "
                f"Rephrase as 'Next stage needs:' or 'To advance:'.",
            )
        for m in ADVANCES_STAGE_RE.finditer(text):
            _emit(
                ti,
                "WARN",
                f"hint says '{m.group(0)}' — 'Stage' as an engine concept leaks. "
                f"Rephrase ('moves things forward', 'unlocks the next chapter', etc.).",
            )

        # --- Rule v2.5: author-side phrasing ---
        # 5a — "the X flag" engine-word leak
        for m in THE_X_FLAG_RE.finditer(text):
            _emit(
                ti,
                "WARN",
                f"hint says '{m.group(0)}' — 'flag' is an engine word. Players "
                f"don't know what flags are. Describe the player-facing condition "
                f"instead (e.g., 'until Ryan invites you as a partner').",
            )
        # 5b — known author scene tag phrases
        for phrase in AUTHOR_SCENE_TAG_PHRASES:
            if phrase.lower() in text_lower:
                _emit(
                    ti,
                    "WARN",
                    f"hint mentions author-side scene tag '{phrase}' — players "
                    f"don't know which scene this refers to. Describe what the "
                    f"player will SEE happen instead.",
                )

        # === End linter v2 ===

        # --- Rules requiring stage_gate context (need to know which helper) ---
        if not (cond and cond.stage_npc and cond.stage_value is not None):
            continue
        npc_slug = cond.stage_npc
        cur_stage = cond.stage_value
        next_stage = cur_stage + 1
        # Look up the helper that gates the NEXT stage advancement.
        helper_name = f"{npc_slug.replace('npc_', '')}_stage_{next_stage}"
        helper = helpers_by_name.get(helper_name)
        if not helper:
            continue  # No helper for this transition — terminal stage or non-helper-driven

        # Extract numeric thresholds from helper conditions.
        helper_items = (helper.conditions or {}).get("items", []) if isinstance(helper.conditions, dict) else []
        # Build map: trait_key -> threshold
        helper_thresholds: Dict[str, int] = {}
        helper_counters: Dict[str, int] = {}
        for item in helper_items:
            if not isinstance(item, dict):
                continue
            if item.get("type") != "trait":
                continue
            trait_key = item.get("trait_key", "")
            value = item.get("value")
            op = item.get("operator", "")
            if not isinstance(value, (int, float)) or op not in ("gte", "gt", "eq"):
                continue
            if trait_key.endswith("_count") or trait_key.endswith("_done"):
                helper_counters[trait_key] = int(value)
            else:
                helper_thresholds[trait_key] = int(value)

        # --- Rule: numeric threshold drift (trust ≥ N etc.) ---
        for m in THRESHOLD_RE.finditer(text):
            stat_name = m.group(1).lower()
            hint_val = int(m.group(2))
            actual = helper_thresholds.get(stat_name)
            if actual is not None and actual != hint_val:
                _emit(
                    ti,
                    "FAIL",
                    f"hint says '{stat_name} ≥ {hint_val}' but helper "
                    f"'{helper_name}' requires '{stat_name} >= {actual}'. "
                    f"Update hint to match helper (canvas/helper is source of truth).",
                )

        # --- Rule: counter drift (×N sessions / N+ times) ---
        for m in COUNTER_RE.finditer(text):
            hint_val = int(m.group(1) or m.group(2))
            # Match any counter — heuristic: if the helper has exactly one counter,
            # compare. If multiple, can't disambiguate from text alone.
            if len(helper_counters) == 1:
                only_counter = list(helper_counters.values())[0]
                if only_counter != hint_val:
                    counter_name = list(helper_counters.keys())[0]
                    _emit(
                        ti,
                        "FAIL",
                        f"hint says '×{hint_val}' but helper '{helper_name}' "
                        f"requires '{counter_name} >= {only_counter}'. "
                        f"Update hint to match.",
                    )

        # --- Rule: time band drift ---
        for m in TIME_BAND_RE.finditer(text):
            hint_start = m.group(1)
            hint_end = m.group(2)
            schedules = npc_schedules.get(npc_slug, [])
            if not schedules:
                continue
            # Check if the hint's band matches ANY of the NPC's canvas schedules.
            matched = any(
                s_start == hint_start and s_end == hint_end
                for s_start, s_end, _ in schedules
            )
            if not matched:
                actual_bands = ", ".join(f"{s}–{e} ({c})" for s, e, c in schedules)
                _emit(
                    ti,
                    "FAIL",
                    f"hint mentions time band '{hint_start}–{hint_end}' but "
                    f"NPC '{npc_slug}' has no canvas with that exact schedule. "
                    f"Actual schedules: {actual_bands}",
                )

        # --- Rule: helper has N AND-gates, hint mentions <N ---
        gate_count_in_helper = len([i for i in helper_items if isinstance(i, dict)])
        # Heuristic: count "BOTH"/"ALL of"/"need:" mentions, fall back to "•" or "+" markers.
        has_both = bool(re.search(r"\bBOTH\b|\bALL of\b|\bneed:\b", text, re.IGNORECASE))
        bullet_count = text.count("•")
        plus_separator_count = text.count(" + ")
        if (
            gate_count_in_helper >= 2
            and not has_both
            and bullet_count < 2
            and plus_separator_count < 1
        ):
            _emit(
                ti,
                "WARN",
                f"helper '{helper_name}' has {gate_count_in_helper} AND-gates "
                f"but hint text doesn't appear to enumerate them "
                f"(no 'BOTH'/'ALL of'/'•'/' + ' markers). You may be omitting "
                f"a gate the player needs to know about.",
            )

    # === Picker tie-warning rule ===
    # When two per-NPC templates would compete on equal footing — same
    # npc_id + same stage_value + same priority + same condition_items.length
    # — the picker falls back to file order, which is exactly the silent
    # contract the priority/specificity rule is meant to kill. Warn so the
    # author either bumps a priority or adds a distinguishing condition.
    seen_signatures: Dict[Tuple[Optional[str], Optional[int], int, int], int] = {}
    for ti, t in enumerate(templates):
        cond = t.condition
        if not (cond and cond.stage_npc and cond.stage_value is not None):
            continue
        npc = t.npc_id or cond.stage_npc
        priority = getattr(t, "priority", 0) or 0
        # Approximate condition_items length — the real serializer count.
        # Mirrors the items the picker will see at runtime.
        items_count = 0
        if cond.stage_npc and cond.stage_op and cond.stage_value is not None:
            items_count += 1
        if cond.missing_flag:
            items_count += 1
        items_count += len(cond.trait_checks or [])
        if cond.prerequisite_npc_stage:
            items_count += 1
        sig = (npc, cond.stage_value, priority, items_count)
        if sig in seen_signatures:
            other_ti = seen_signatures[sig]
            _emit(
                ti,
                "WARN",
                f"undecidable picker tie with templates[{other_ti}]: same "
                f"npc_id='{npc}', stage_value={cond.stage_value}, priority={priority}, "
                f"and {items_count} condition_items. File order would silently "
                f"win — bump `priority` on the variant that should fire first "
                f"or add a distinguishing condition.",
            )
        else:
            seen_signatures[sig] = ti

    # === Pattern 2 (2026-05-01) — registry coverage scan ===
    # Walk every helper's conditions; warn for trait_keys / flag_keys that are
    # referenced in a gate but have no corresponding [[traits.labels]] /
    # [[flags.labels]] entry. The auto-renderer (setup.computeHintGoal) will
    # fall back to printing the raw key — functional but ugly. Cosmetic warn.
    if template.trait_labels or template.flag_labels:
        # Only run the coverage scan when the author has started using labels;
        # legacy games with no label registry shouldn't get spammed.
        helper_unlabeled_traits: Set[str] = set()
        helper_unlabeled_flags: Set[str] = set()
        for helper in (template.stage_helpers or []):
            cond_dict = helper.conditions if isinstance(helper.conditions, dict) else {}
            for it in (cond_dict.get("items") or []):
                if not isinstance(it, dict):
                    continue
                if it.get("type") == "trait":
                    tkey = it.get("trait_key")
                    if tkey and tkey not in trait_label_keys:
                        helper_unlabeled_traits.add(tkey)
                elif it.get("type") == "flag":
                    fkey = it.get("flag_key")
                    if fkey and fkey not in flag_label_keys:
                        helper_unlabeled_flags.add(fkey)
        for tkey in sorted(helper_unlabeled_traits):
            _warnings.warn(
                f"HINT LINTER WARN traits.labels: helper-referenced trait "
                f"'{tkey}' has no [[traits.labels]] entry. Auto-rendered goal "
                f"bullets will show the raw key. Add a `key = \"{tkey}\"` entry "
                f"with a player-facing `label`.",
                UserWarning,
                stacklevel=4,
            )
        for fkey in sorted(helper_unlabeled_flags):
            _warnings.warn(
                f"HINT LINTER WARN flags.labels: helper-referenced flag "
                f"'{fkey}' has no [[flags.labels]] entry. Auto-rendered goal "
                f"bullets will show the raw flag name. Add a `key = \"{fkey}\"` "
                f"entry with a player-facing `label`.",
                UserWarning,
                stacklevel=4,
            )


# -------- Creation --------


def _ensure_user(owner_id: str) -> User:
    try:
        return User.objects.get(id=owner_id)
    except Exception:
        raise ValueError(f"owner id not found: {owner_id}")


def _parse_prerequisite_npc_stage(spec: str) -> Optional[Tuple[str, str, int]]:
    """Parse "npc_<slug> <op> <int>" into (npc_slug, op, value).

    Returns None if the string doesn't parse — validator should have caught
    this earlier; serializer is defensive.
    """
    import re
    m = re.match(
        r"^\s*(\w+)\s*(>=|<=|>|<|==|=)\s*(\d+)\s*$", spec
    )
    if not m:
        return None
    npc_slug = m.group(1)
    op_raw = m.group(2)
    value = int(m.group(3))
    op_map = {">=": "gte", "<=": "lte", ">": "gt", "<": "lt", "==": "eq", "=": "eq"}
    op = op_map.get(op_raw)
    if op is None:
        return None
    return npc_slug, op, value


def _serialize_quests_condition(c: QuestsCondition) -> Dict[str, Any]:
    """Emit a condition item into the runtime JSON shape. Only the fields
    actually set survive — null/empty fields are omitted to keep the
    runtime JSON small and unambiguous about which shape (flag vs trait)
    each item is."""
    out: Dict[str, Any] = {}
    if c.flag is not None:
        out["flag"] = c.flag
    if c.trait is not None:
        out["trait"] = c.trait
    if c.subject is not None:
        out["subject"] = c.subject
    if c.npc_id is not None:
        out["npc_id"] = c.npc_id
    if c.op:
        out["op"] = c.op
    if c.value is not None:
        # Emit ints as ints (not 25.0) so the runtime label reads "X / 25"
        # not "X / 25.0".
        if float(c.value).is_integer():
            out["value"] = int(c.value)
        else:
            out["value"] = c.value
    if c.label is not None:
        out["label"] = c.label
    return out


def _serialize_quests_card(card: QuestsCard) -> Dict[str, Any]:
    """PRD 48 — Emit a QuestsCard into the runtime JSON shape consumed by
    setup.quests_cards at the SugarCube runtime. Field names match the V2
    runtime functions in v2.py.

    Optional fields (ready_text, tip, npc_id, group, ready_canvas) are
    omitted when null so the runtime can do `if (card.field)` cleanly.
    """
    out: Dict[str, Any] = {
        "text": card.text,
        "priority": card.priority,
        "when": [_serialize_quests_condition(c) for c in card.when],
    }
    if card.ready_text:
        out["ready_text"] = card.ready_text
    if card.tip:
        out["tip"] = card.tip
    if card.npc_id:
        out["npc_id"] = card.npc_id
    if card.group:
        out["group"] = card.group
    if card.goals:
        out["goals"] = [_serialize_quests_condition(c) for c in card.goals]
    if card.ready_canvas:
        out["ready_canvas"] = card.ready_canvas
    if card.terminal:
        out["terminal"] = True
    if card.terminal_text:
        out["terminal_text"] = card.terminal_text
    return out


def _serialize_hint_template(t: TemplateHintTemplate) -> Dict[str, Any]:
    """Emit a hint template into the runtime JSON shape.

    Three pieces:
      - condition: legacy shape (missing_flag/missing_trait/gap_gte) preserved
        for back-compat; runtime today doesn't read it but tests may, and
        future-us shouldn't have to dig through old TOMLs to reconstruct
        author intent.
      - npc_id: routing field — which NPC's section the hint belongs to in
        the Quests page.
      - condition_items: NORMALIZED predicate list evaluated by
        setup.checkSingleCondition (v1.py:4636) at runtime. Each item shape
        matches the existing condition-item DSL (type/subject/operator/...).
        Empty list = always fires.
    """
    cond = t.condition
    legacy = None
    items: List[Dict[str, Any]] = []
    npc_id = t.npc_id  # may be None for global hints
    if cond is not None:
        legacy = {
            "missing_flag": cond.missing_flag,
            "missing_trait": cond.missing_trait,
            "gap_gte": cond.gap_gte,
            "stage_npc": cond.stage_npc,
            "stage_op": cond.stage_op,
            "stage_value": cond.stage_value,
            "trait_checks": cond.trait_checks,
            "prerequisite_npc_stage": cond.prerequisite_npc_stage,
        }
        # Stage-gate triple → trait condition on $player.core_traits[<slug>_stage].
        # Validator guarantees the triple is whole when any of three is set.
        if cond.stage_npc and cond.stage_op and cond.stage_value is not None:
            items.append({
                "type": "trait",
                "subject": "player",
                "trait_key": f"{cond.stage_npc}_stage",
                "operator": cond.stage_op,
                "value": cond.stage_value,
            })
        # missing_flag → flag is_false (the hint applies WHILE the flag isn't set).
        if cond.missing_flag:
            items.append({
                "type": "flag",
                "subject": "player",
                "flag_key": cond.missing_flag,
                "operator": "is_false",
            })
        # E14 — append each trait_checks item verbatim as a condition_item.
        # Validator already verified shape (subject, trait_key/flag_key, operator).
        for tc in (cond.trait_checks or []):
            items.append(dict(tc))
        # E22 — parse "npc_<slug> <op> <int>" into a trait condition_item on
        # $player.core_traits[<slug>_stage]. Validator confirmed the syntax
        # and that the referenced NPC exists.
        if cond.prerequisite_npc_stage:
            parsed = _parse_prerequisite_npc_stage(cond.prerequisite_npc_stage)
            if parsed is not None:
                npc_slug, op, value = parsed
                items.append({
                    "type": "trait",
                    "subject": "player",
                    "trait_key": f"{npc_slug}_stage",
                    "operator": op,
                    "value": value,
                })
        # missing_trait + gap_gte are PRD 03 legacy semantics with no
        # author-spec'd subject. Surfaced in the legacy shape for back-compat
        # but not normalized into condition_items (would need disambiguation
        # work in a follow-up). Authors targeting E10 use stage_gate or
        # missing_flag for predicate logic.
    return {
        "condition": legacy,
        "npc_id": npc_id,
        "condition_items": items,
        "text": t.text,
        # Priority is the picker's primary sort key (higher wins). Default 0.
        "priority": t.priority,
        # Pattern 2 (2026-05-01): tip + auto_goal flow through to runtime.
        # Renderer (setup.computeHintGoal) reads condition.stage_npc/stage_value
        # from `condition` to look up the helper; renders 🎯 block + 💡 tip line.
        "tip": t.tip,
        "auto_goal": t.auto_goal,
        # E17 (2026-05-06): ready-frame author override. Read by
        # setup._getReadyHintForNPC at runtime when synthesizing the "all
        # gates cleared" hint. Empty string → engine default.
        "ready_text": t.ready_text,
        # 2026-05-09: terminal-stage badge. Read by setup.computeHintGoal —
        # when true, emits "✓ Arc complete" frame regardless of auto_goal.
        "arc_complete": t.arc_complete,
        # 2026-05-10: flag-based arc closure target. Read by
        # setup.computeHintGoal — when set, looks up the named flag's setter
        # canvas and renders Ready (📍+🕒) or ✓ Complete frame based on the
        # flag's live value. Mutex with arc_complete (validated upstream).
        "arc_closure_flag": t.arc_closure_flag,
    }


def _normalize_block_list(
    raw_blocks: Any,
    max_depth: int = 4,
    _depth: int = 0,
    _prefix: str = "b",
) -> List[Dict[str, Any]]:
    """Recursively normalize a list of TOML block dicts to the canonical safe shape.

    Each block becomes ``{id, type, props, content, children}``. Container types
    (``group``, ``block_pool``) get their inner ``blocks`` recursively
    normalized. Reads ``conditions`` and ``blocks`` from top-level OR ``props``
    (the 2026-05-03 bug-fix pattern: TOML may legitimately use either form).
    Caps recursion at ``max_depth`` (default 4) to prevent pathological nesting;
    the historical hand-unrolled implementation supported at most depth 3
    (group inside pool inside group), so 4 is a defensive ceiling.

    Container nesting: ``group`` MAY be nested directly inside ``group`` —
    a stage gate wrapping flag-gated sub-branches is a legitimate, common
    shape, and the Twee renderer (``_render_group_chain`` →
    ``_convert_blocks_to_game_html``) already recurses it into a nested
    ``<<if>>/<<elseif>>`` variant chain. The old "no group-in-group"
    same-type-skip rule silently emptied such groups (children dropped →
    "No content"); it is removed (2026-05-17). ``block_pool`` still cannot
    nest a ``block_pool`` directly inside itself (random-pick-of-a-random-
    pick is ambiguous; left restricted intentionally). All nesting — same
    or mixed type — is bounded by ``max_depth``.

    Returns: list of normalized block dicts, ready for ``StoryNode.node_data``.

    The ``cascade`` block type (S7) is also handled here as a container —
    each beat's ``blocks`` is recursively normalized via this same helper.
    Beat-level fields (``advance_text``, ``conditions``, ``effects``,
    ``flagEffects``, ``show_when_locked``, ``locked_text``) are passed through
    after type-checking.
    """
    if _depth >= max_depth:
        logger.warning(
            "Block nesting depth %d exceeded; flattening deeper blocks", max_depth
        )
        return []
    if not isinstance(raw_blocks, list):
        return []

    safe: List[Dict[str, Any]] = []
    for i, b in enumerate(raw_blocks):
        if not isinstance(b, dict):
            continue
        b_type = str(b.get("type", "")).strip()
        if not b_type:
            continue
        # Deterministic fallback id (position-based) for blocks with no TOML id —
        # keeps builds reproducible (was uuid4, which churned every build).
        _bid = f"{_prefix}{i}"
        props = b.get("props") or {}
        if not isinstance(props, dict):
            props = {}

        # Default heading.level so frontend schema accepts level-less headings.
        if b_type == "heading" and not props.get("level"):
            props["level"] = 1

        # Convert top-level clip_id → clipId for frontend's camelCase expectation.
        if b_type == "clip":
            clip_id = b.get("clip_id")
            if clip_id and isinstance(clip_id, str):
                props["clipId"] = str(clip_id).strip()

        # Container blocks — read .conditions/.blocks from top-level OR props
        # (the 2026-05-03 4-place bug-fix pattern), recursively normalize children.
        if b_type == "group":
            cond = b.get("conditions") or props.get("conditions")
            if cond and isinstance(cond, dict):
                props["conditions"] = cond
            inner_raw = b.get("blocks") or props.get("blocks") or []
            inner_safe = _normalize_block_list(
                inner_raw, max_depth=max_depth, _depth=_depth + 1, _prefix=f"{_bid}."
            )
            # Nested groups are PRESERVED (2026-05-17). A stage group wrapping
            # flag-gated sub-branch groups is a legitimate shape; the renderer
            # recurses it into a nested <<if>>/<<elseif>> chain. The recursion
            # above already normalized them + the max_depth cap bounds depth,
            # so no same-type-skip filter here. (block_pool keeps its filter.)
            props["blocks"] = inner_safe
        elif b_type == "block_pool":
            inner_raw = b.get("blocks") or props.get("blocks") or []
            inner_safe = _normalize_block_list(
                inner_raw, max_depth=max_depth, _depth=_depth + 1, _prefix=f"{_bid}."
            )
            # Preserve original same-type-skip rule: drop any nested pools.
            inner_safe = [ib for ib in inner_safe if ib.get("type") != "block_pool"]
            # Original behavior: warn if pool has mixed child types.
            child_types = {ib.get("type") for ib in inner_safe}
            if len(child_types) > 1:
                logger.warning(
                    "block_pool has mixed types %s — all items should be same type",
                    child_types,
                )
            props["blocks"] = inner_safe
        elif b_type == "cascade":
            # S7 — multi-beat linkreplace cascade. Reads `id` + `beats` from
            # top-level OR `props` (same bug-fix-pattern as group/pool).
            cascade_id = b.get("id") or props.get("id") or _bid
            props["id"] = str(cascade_id)
            raw_beats = b.get("beats") or props.get("beats") or []
            if not isinstance(raw_beats, list):
                raw_beats = []
            safe_beats: List[Dict[str, Any]] = []
            for bi, beat in enumerate(raw_beats):
                if not isinstance(beat, dict):
                    continue
                beat_blocks_raw = beat.get("blocks") or []
                # Recursively normalize the beat's child blocks. A beat's
                # blocks can themselves contain groups, pools, thought
                # bubbles, or even nested cascades — depth cap protects.
                beat_blocks_safe = _normalize_block_list(
                    beat_blocks_raw, max_depth=max_depth, _depth=_depth + 1,
                    _prefix=f"{_bid}.beat{bi}.",
                )
                beat_conditions = beat.get("conditions")
                if beat_conditions is not None and not isinstance(beat_conditions, dict):
                    beat_conditions = None
                safe_beats.append({
                    "advance_text": str(beat.get("advance_text", "")),
                    "conditions": beat_conditions,
                    "effects": beat.get("effects") if isinstance(beat.get("effects"), list) else [],
                    "flagEffects": beat.get("flagEffects") if isinstance(beat.get("flagEffects"), list) else [],
                    "show_when_locked": bool(beat.get("show_when_locked", False)),
                    "locked_text": str(beat.get("locked_text", "")),
                    # S4 (2026-05-06) — threshold-publisher message for the
                    # locked sibling. When set + show_when_locked = True,
                    # clicking the locked label fires a warning toast with
                    # this in-character message. Mirrors the choice-path S4.
                    "locked_text_threshold": str(beat.get("locked_text_threshold", "")),
                    "blocks": beat_blocks_safe,
                })
            props["beats"] = safe_beats

        safe.append(
            {
                "id": str(b.get("id") or _bid),
                "type": b_type,
                "props": props,
                "content": str(b.get("content", "")),
                "children": [],
            }
        )
    return safe



def _assemble_project_metadata(project, template):
    """Assemble project.metadata from the parsed template (pure; no DB).

    Extracted so the DB path and the no-DB build_game_graph share one copy.
    """
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
    # PRD 48 — surface the Quests engine version onto project metadata so the
    # generator can dispatch (V1 default vs V2 opt-in) at emission time.
    project.metadata["quests_engine"] = template.project.quests_engine
    # Narrative person — the generator reads this to label the player's own dialog
    # and thought-bubble blocks ("You:" / "Me:" / the character's name).
    project.metadata["narration_person"] = template.narration_person
    # Optional sidebar version/release-date footer (new top-level metadata keys).
    project.metadata["version"] = template.project.version
    project.metadata["release_date"] = template.project.release_date
    # Optional studio identity — the generator falls back to its own defaults when
    # these are "" (see v2.DEFAULT_SUPPORT_URL / DEFAULT_STUDIO_NAME).
    project.metadata["support_url"] = template.project.support_url
    project.metadata["studio_name"] = template.project.studio_name
    # PRD 48 — serialize V2 cards onto project.metadata. Empty list for v1
    # games (their hints stay in project.metadata["story_arc"]["hints"]).
    if template.project.quests_engine == "v2":
        project.metadata["quests_cards"] = [
            _serialize_quests_card(c) for c in template.quests_cards
        ]
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
                    "beauty": ci.beauty,
                    "corruption": ci.corruption,
                    "type": ci.type,  # Doc 72 — outfit-category tag for worn_type predicate
                    "exposure": ci.exposure,  # 0 covers / 1 underwear-level / 2 bare
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
    # Store corruption tiers if overridden (doc 45 G7)
    if template.corruption_tiers:
        project.metadata["corruption_tiers"] = template.corruption_tiers
    # Store fast jobs + bank (doc 45 G9)
    if template.fast_jobs:
        project.metadata["fast_jobs"] = [
            {"id": j.id, "name": j.name, "income": j.income, "xp_req": j.xp_req,
             "cooldown_days": j.cooldown_days, "time_period": j.time_period,
             "money_trait": j.money_trait}
            for j in template.fast_jobs
        ]
    if template.bank is not None:
        project.metadata["bank"] = {
            "enabled": template.bank.enabled,
            "interest_rate": template.bank.interest_rate,
            "money_trait": template.bank.money_trait,
        }
    # Store player-portrait config (state-reactive sidebar image). Key == block name so
    # v2.py's (metadata).get("player_portrait") round-trips (mirror bank, NOT phone_settings).
    if template.player_portrait is not None:
        pp = template.player_portrait
        project.metadata["player_portrait"] = {
            "enabled": pp.enabled,
            "naked_image": pp.naked_image,
            "topless_image": pp.topless_image,
            "bottomless_image": pp.bottomless_image,
            "underwear_image": pp.underwear_image,
            "default_image": pp.default_image,
            "pregnancy_trait": pp.pregnancy_trait,
            "pregnancy_suffix": pp.pregnancy_suffix,
            "outfits": [{"image": o.image, "when": o.when} for o in pp.outfits],
        }
    # Store quests if defined (doc 45 G4)
    if template.quests:
        project.metadata["quests"] = [
            {
                "id": q.id,
                "name": q.name,
                "steps": q.steps,
                "repeatable": q.repeatable,
            }
            for q in template.quests
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
                    "conditions": fe.conditions,
                }
                for fe in template.daily_tick.flagEffects
            ],
            "traitEffects": [
                {
                    "targetType": te.targetType,
                    "npcId": te.npcId,
                    "trait": te.trait,
                    "op": te.op,
                    "value": te.value,
                    "clamp": te.clamp,
                    "cap": te.cap,
                    "conditions": te.conditions,
                }
                for te in template.daily_tick.traitEffects
            ],
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
    # Pattern 2: store label registries on project metadata.
    # Engine reads them at runtime via setup.trait_labels / setup.flag_labels
    # for the goal-block renderer (setup.computeHintGoal).
    if template.trait_labels:
        project.metadata["trait_labels"] = {
            tl.key: {"label": tl.label, "verb": tl.verb, "unit": tl.unit, "hidden": tl.hidden}
            for tl in template.trait_labels
        }
    if template.flag_labels:
        project.metadata["flag_labels"] = {
            fl.key: {"label": fl.label}
            for fl in template.flag_labels
        }
    # Tips page (game-level mechanics surface).
    if template.tips_page:
        project.metadata["tips_page"] = {
            "title": template.tips_page.title,
            "content": template.tips_page.content,
        }
    # Cast page. Chrome only — the roster itself is built at runtime from $npcs
    # and setup.quests_cards, so nothing about the cast is copied here.
    if template.cast_page:
        project.metadata["cast_page"] = {
            "title": template.cast_page.title,
            "intro": template.cast_page.intro,
            "button_label": template.cast_page.button_label,
            "button_icon": template.cast_page.button_icon,
        }
    # Player cheat page. The FULL row data goes here — hints, values, caps and all.
    # Metadata never reaches the output file as a config object; each row is baked
    # into passage markup inside a check on its own unlock flag.
    #
    # The CODES are deliberately absent. They are not a property of the TOML (which
    # is committed to a public repo) — they arrive at package time from an untracked
    # codes file and are injected into this dict by the packager as hashes only.
    if template.cheat_page:
        cp = template.cheat_page
        project.metadata["cheat_page"] = {
            "title": cp.title,
            "intro": cp.intro,
            "button_label": cp.button_label,
            "button_icon": cp.button_icon,
            "join_note": cp.join_note,
            "join_url": cp.join_url,
            "grants": [
                {
                    "id": g.id,
                    "label": g.label,
                    "trait": g.trait,
                    "value": g.value,
                    "targetType": g.targetType,
                    "npcId": g.npcId,
                    "op": g.op,
                    "cap": g.cap,
                    "clamp": g.clamp,
                    "hint": g.hint,
                    "button_text": g.button_text,
                    "at_cap_text": g.at_cap_text,
                }
                for g in cp.grants
            ],
        }
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
            "currency_symbol": template.rent_currency_symbol,
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
                    "stuck_threshold_days": (
                        template.story_arc.hints.stuck_threshold_days
                        if template.story_arc.hints
                        else 7
                    ),
                    "stage_stall_message": (
                        template.story_arc.hints.stage_stall_message
                        if template.story_arc.hints
                        else ""
                    ),
                    "templates": [
                        _serialize_hint_template(t)
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
            "purchase_flag": phone.purchase_flag,
            "apps": [
                {"id": a.id, "type": a.type, "label": a.label, "icon": a.icon,
                 **({"post_actions": a.post_actions} if a.post_actions else {})}
                for a in phone.apps
            ],
            "conversations": [
                {
                    "id": c.id,
                    "app": c.app,
                    "npc": c.npc,
                    "trigger": c.trigger,
                    "notify": c.notify,
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
                    "notify": p.notify,
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
                    "image": dt.image,
                    "corruption_min": dt.corruption_min,
                    "cooldown": dt.cooldown,
                }
                for dt in phone.daily_topics
            ],
            "gallery_items": [
                {"id": g.id, "image": g.image, "caption": g.caption,
                 "trigger": g.trigger, "link": g.link}
                for g in phone.gallery_items
            ],
        }

@transaction.atomic
def create_project_from_template(
    template: GameTemplate, owner_id: str, name_override: Optional[str] = None
) -> Dict[str, Any]:
    """DEPRECATED for game builds — the legacy DB path (writes/reads DB rows).

    The default build path is now the no-DB `game_graph.build_game_graph`
    (zero database interaction, constant slug ids, reproducible). This is kept
    for the web-API `generate-game` endpoint, the standalone
    `create_project_from_template` management command, elora tooling, and the
    existing test suite, which still rely on a persisted Project.
    """
    owner = _ensure_user(owner_id)

    # Project
    project = Project(
        name=name_override or template.project.title,
        description=template.project.description,
        owner=owner,
    )
    _assemble_project_metadata(project, template)
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
        # G: per-NPC cast-card tag line.
        if n.tags:
            npc.ai_behavior_config["tags"] = n.tags
        if n.role:
            npc.ai_behavior_config["role"] = n.role
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
        if l.offscreen:
            loc.properties["offscreen"] = True
        if l.image:
            loc.properties["image"] = l.image
        if l.image_search_queries:
            loc.properties["image_search_queries"] = l.image_search_queries
        if l.entry_conditions:
            loc.properties["entry_conditions"] = l.entry_conditions
        if l.blocked_message:
            loc.properties["blocked_message"] = l.blocked_message
        if not l.auto_exit:
            # Transit stop — the author owns the way out (see TemplateLocation.auto_exit).
            loc.properties["auto_exit"] = False
        if l.costs:
            # int-coerce (TOML may give floats); the generator reads entry_costs.
            loc.properties["entry_costs"] = {k: int(v) for k, v in l.costs.items()}
        if l.clothing_rules:
            loc.properties["clothing_rules"] = l.clothing_rules
        if l.description_variants:
            loc.properties["description_variants"] = l.description_variants
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
                            # E21 — opt-in cooldown visibility
                            "show_when_blocked": c.trigger.show_when_blocked or None,
                            "cooldown_message": c.trigger.cooldown_message,
                            # PRD 25 — Lane 3 dispatcher substitution
                            "substitutions": c.trigger.substitutions if c.trigger.substitutions else None,
                            "substitution_only": c.trigger.substitution_only if c.trigger.substitution_only else None,
                            # L2-2 — Lane 2 anti-toggle cooldown (location slugs)
                            "entry_only_from": c.trigger.entry_only_from if c.trigger.entry_only_from else None,
                            # Phase A (2026-05-14) — Lane 2/3 NPC presence gate.
                            # Engine reads requiresNpc from canvas metadata at
                            # runtime and AND-gates with all other conditions.
                            "requires_npc": c.trigger.requires_npc or None,
                            # Doc 69 Item 2 — Pattern C pre-substitution effects.
                            # Engine reads from canvas metadata + emits
                            # <<script>>setup.applyAndNotifyTrait(...)<</script>>
                            # macros BEFORE the substitution check so effects
                            # fire unconditionally even when a substitution preempts.
                            "pre_substitution_effects": (
                                c.trigger.pre_substitution_effects
                                if c.trigger.pre_substitution_effects else None
                            ),
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
                # Normalize TOML blocks via the shared recursive helper
                # (consolidated 2026-05-06 — replaced ~200 lines of triplicated
                # hand-unrolled normalization with `_normalize_block_list`,
                # which preserves the 2026-05-03 4-place-bug-fix pattern at
                # every nesting level).
                safe_blocks = _normalize_block_list(n.blocks or [])

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
                        if ch.locked_text_threshold:
                            ch_d["locked_text_threshold"] = ch.locked_text_threshold
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
                        if ch.quest_effects:
                            ch_d["questEffects"] = ch.quest_effects
                        if ch.schedule_effects:
                            ch_d["scheduleEffects"] = ch.schedule_effects
                        if ch.costs:
                            ch_d["costs"] = ch.costs

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
                **({"locked_text_threshold": ch.locked_text_threshold} if ch.locked_text_threshold else {}),
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
                **({"questEffects": ch.quest_effects} if ch.quest_effects else {}),
                **({"scheduleEffects": ch.schedule_effects} if ch.schedule_effects else {}),
                **({"costs": ch.costs} if ch.costs else {}),
            }
            for ch in eb.choices
        ]
    return d
