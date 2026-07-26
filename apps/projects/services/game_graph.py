"""In-memory game-object graph — the no-DB build path.

`build_game_graph(template)` constructs the same Django model instances that
`create_project_from_template` would persist, but with NO database: no `.save()`,
no owner/User, no `full_clean()` side-effect queries. It wires foreign keys as
in-memory object references, carries reverse relations (canvas nodes, trigger
schedules) as plain lists, and precomputes the reverse indexes the generator
would otherwise fetch through ORM reverse-managers.

Stage 1: ids are still `uuid4` (minted Python-side by the models' field defaults
at construction), so the output is structurally identical to the DB path — this
is validated by the byte-equivalence oracle. Stage 2 switches ids to constant
slugs. See the no-DB refactor plan.

The metadata-assembly block is shared with the DB path via
`_assemble_project_metadata`; only the construction/wiring below is specific to
the no-DB path (and reproduces the DB path's logic minus persistence).
"""
import uuid
from typing import Any, Dict, List, Optional, Tuple

from apps.characters.models import Character
from apps.npcs.models import NPC
from apps.projects.models import Project
from apps.stories.models import CanvasTrigger, StoryCanvas, StoryNode, TriggerSchedule
from apps.stories.services.block_conversion import BlockConversionService
from apps.world.models import Location

from .template_import import (
    GameTemplate,
    _assemble_project_metadata,
    _normalize_block_list,
    _serialize_exit_block,
)

# Coerce "HH:MM" schedule strings to datetime.time exactly as a DB save would
# (the generator calls .strftime() on these with no string fallback).
_SCHEDULE_TIME_FIELD = TriggerSchedule._meta.get_field("start_time")


class GameGraph:
    """The in-memory object graph the generator consumes in no-DB mode.

    Holds unsaved Django model instances plus plain-list relations and reverse
    indexes that stand in for the ORM reverse-managers.
    """

    def __init__(self) -> None:
        self.project: Optional[Project] = None
        self.player: Optional[Character] = None
        self.npcs: List[NPC] = []
        self.locations: List[Location] = []
        self.canvases: List[StoryCanvas] = []
        self.starting_canvas: Optional[StoryCanvas] = None
        # Reverse indexes — replace the ORM reverse-managers the generator queries.
        self.canvas_by_slug: Dict[
            str, StoryCanvas
        ] = {}  # replaces filter(metadata__slug=)
        self.node_by_id: Dict[
            str, StoryNode
        ] = {}  # replaces StoryNode.objects.filter(id=)
        self.children_by_entry_from: Dict[
            str, List[Location]
        ] = {}  # replaces filter(entry_from=)
        self.ids: Dict[str, Any] = {}  # stats/id dict the command prints


def build_game_graph(
    template: GameTemplate, name_override: Optional[str] = None
) -> GameGraph:
    graph = GameGraph()

    # ── Project (no owner; never saved) ───────────────────────────────────────
    project = Project(
        name=name_override or template.project.title,
        description=template.project.description,
    )
    # Deterministic project id (drives the Twine IFID). Tweego requires a valid
    # UUID here (rejects a bare slug: "invalid IFID length"), so derive a stable
    # UUID from the slug — constant across rebuilds, valid format. NPC/canvas/node
    # ids below stay raw slugs (that's what fixes $npcs save-survival).
    project.id = uuid.uuid5(uuid.NAMESPACE_DNS, template.project.slug)
    _assemble_project_metadata(project, template)
    graph.project = project

    # ── Player ────────────────────────────────────────────────────────────────
    _player_flag_keys = list(template.player.flag_keys or [])
    if template.rent_enabled and template.rent_eviction_mode == "flag_set":
        if (
            template.rent_eviction_flag
            and template.rent_eviction_flag not in _player_flag_keys
        ):
            _player_flag_keys.append(template.rent_eviction_flag)

    player = Character(
        project=project,
        name=template.player.name or "Player",
        description=template.player.description or "",
        core_traits=template.player.core_traits or {},
        flag_keys=_player_flag_keys,
    )
    player.id = template.player.id
    player.character_metadata = player.character_metadata or {}
    player.character_metadata["slug"] = template.player.id
    if template.player.portrait:
        player.character_metadata["portrait"] = template.player.portrait
    if template.player.trait_decay:
        player.character_metadata["trait_decay"] = template.player.trait_decay
    if template.player.customizable:
        player.character_metadata["customizable"] = True
        player.character_metadata["customization_fields"] = [
            {
                "id": cf.id,
                "type": cf.type,
                "label": cf.label,
                "default": cf.default,
                "options": (
                    [
                        {"id": o.id, "image": o.image, "label": o.label}
                        for o in cf.options
                    ]
                    if cf.type == "image_select"
                    else cf.options
                ),
                "sets_portrait": cf.sets_portrait,
            }
            for cf in template.player.customization_fields
        ]
    # Prime the reverse-o2o cache so project.player_character is query-free.
    Project.player_character.related.set_cached_value(project, player)
    graph.player = player

    # ── NPCs ──────────────────────────────────────────────────────────────────
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
        npc.id = n.id
        npc.ai_behavior_config = npc.ai_behavior_config or {}
        npc.ai_behavior_config["slug"] = n.id
        if n.portrait:
            npc.ai_behavior_config["portrait"] = n.portrait
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
        if n.customizable:
            npc.ai_behavior_config["customizable"] = True
        if n.relationship:
            npc.ai_behavior_config["relationship"] = n.relationship
        if n.relationship_options:
            npc.ai_behavior_config["relationship_options"] = n.relationship_options
        if n.trait_decay:
            npc.ai_behavior_config["trait_decay"] = n.trait_decay
        if n.arc_stages:
            npc.ai_behavior_config["arc_stages"] = n.arc_stages
        graph.npcs.append(npc)
        npc_ids.append(str(npc.id))

    # ── Locations ─────────────────────────────────────────────────────────────
    slug_map: Dict[str, Location] = {}
    for l in template.locations:
        loc = Location(
            project=project,
            name=l.name,
            description=l.description or "",
            is_container=bool(l.is_container),
        )
        loc.id = l.id
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
            loc.properties["entry_costs"] = {k: int(v) for k, v in l.costs.items()}
        if l.clothing_rules:
            loc.properties["clothing_rules"] = l.clothing_rules
        slug_map[l.id] = loc
        graph.locations.append(loc)

    # Pass 2a: parent links (in-memory object refs; no full_clean/save)
    for l in template.locations:
        loc = slug_map[l.id]
        loc.parent_location = slug_map.get(l.parent) if l.parent else None

    # Pass 2b: entry_from + default_entry
    for l in template.locations:
        loc = slug_map[l.id]
        loc.entry_from = slug_map.get(l.entry_from) if l.entry_from else None
        loc.default_entry_location = (
            slug_map.get(l.default_entry) if l.default_entry else None
        )

    # navigation_order
    for l in template.locations:
        if not l.navigation_order:
            continue
        loc = slug_map[l.id]
        loc.navigation_order = [
            str(slug_map[s].id) for s in l.navigation_order if s in slug_map
        ]

    # Reverse index: children_by_entry_from (replaces Location.objects.filter(entry_from=))
    for loc in graph.locations:
        if loc.entry_from is not None:
            graph.children_by_entry_from.setdefault(str(loc.entry_from.id), []).append(
                loc
            )

    # ── Story canvases / triggers / nodes ─────────────────────────────────────
    canvas_slug_map: Dict[str, StoryCanvas] = {}
    node_slug_map: Dict[str, StoryNode] = {}
    node_local_map: Dict[Tuple[str, str], StoryNode] = {}
    starting_canvas = None
    starting_canvas_node_count = 0

    if getattr(template, "canvases", None):
        seq = 0
        for c in template.canvases:
            sc = StoryCanvas(
                project=project,
                name=c.name,
                description=c.description or "",
            )
            sc.id = (
                c.id
            )  # set before nodes so StoryNode(canvas=sc) inherits the slug canvas_id
            sc.metadata = sc.metadata or {}
            sc.metadata["slug"] = c.id
            if c.loop:
                sc.metadata["loop"] = c.loop
            sc._seq = seq  # ordering key (mirrors StoryCanvas.Meta -created_at)
            seq += 1
            # Prime the reverse-o2o cache so `canvas.trigger` is query-free.
            # None = triggerless (getattr(canvas,'trigger',None) → None, no query).
            StoryCanvas.trigger.related.set_cached_value(sc, None)
            sc._nodes = []  # plain list, insertion order == order_by('created_at')
            canvas_slug_map[c.id] = sc
            graph.canvas_by_slug[c.id] = sc
            graph.canvases.append(sc)

        # Starting canvas (required)
        if template.starting_canvas:
            if template.starting_canvas not in canvas_slug_map:
                raise ValueError(
                    f"starting_canvas '{template.starting_canvas}' not found in canvases. "
                    f"Available canvas IDs: {list(canvas_slug_map.keys())[:10]}..."
                )
            starting_canvas = canvas_slug_map[template.starting_canvas]
            project.starting_canvas = starting_canvas  # forward FK, in-memory
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
                        k: v
                        for k, v in {
                            "npc": c.trigger.npc or None,
                            "trigger_mode": c.trigger.trigger_mode
                            if c.trigger.trigger_mode != "manual"
                            else None,
                            "chance": c.trigger.chance,
                            "costs": c.trigger.costs if c.trigger.costs else None,
                            "show_when_blocked": c.trigger.show_when_blocked or None,
                            "cooldown_message": c.trigger.cooldown_message,
                            "substitutions": c.trigger.substitutions
                            if c.trigger.substitutions
                            else None,
                            "substitution_only": c.trigger.substitution_only
                            if c.trigger.substitution_only
                            else None,
                            "entry_only_from": c.trigger.entry_only_from
                            if c.trigger.entry_only_from
                            else None,
                            "requires_npc": c.trigger.requires_npc or None,
                            "pre_substitution_effects": (
                                c.trigger.pre_substitution_effects
                                if c.trigger.pre_substitution_effects
                                else None
                            ),
                        }.items()
                        if v is not None
                    },
                )
                trig._schedules = []  # plain list stand-in for trigger.schedules
                for s in c.trigger.schedules:
                    trig._schedules.append(
                        TriggerSchedule(
                            trigger=trig,
                            name=f"{sc.name} schedule",
                            weekdays=s.weekdays,
                            start_time=_SCHEDULE_TIME_FIELD.to_python(s.start_time),
                            end_time=_SCHEDULE_TIME_FIELD.to_python(s.end_time),
                        )
                    )
                # Prime the reverse-o2o cache with the trigger object (query-free).
                StoryCanvas.trigger.related.set_cached_value(sc, trig)

        # Nodes
        for c in template.canvases:
            sc = canvas_slug_map[c.id]
            for n in c.nodes:
                safe_blocks = _normalize_block_list(n.blocks or [])
                node_data_dict: Dict[str, Any] = {
                    "blocks": safe_blocks,
                    "version": BlockConversionService.DEFAULT_VERSION,
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
                    node_data=node_data_dict,
                    exit_block=_serialize_exit_block(n.exit_block),
                )
                node.id = f"{c.id}.{n.id}"  # constant, canvas-qualified slug id
                sc._nodes.append(node)
                key = f"{c.id}.{n.id}"
                node_slug_map[key] = node
                node_local_map[(c.id, n.id)] = node
                graph.node_by_id[str(node.id)] = node
                if starting_canvas and sc.id == starting_canvas.id:
                    starting_canvas_node_count += 1

        # (Connections: NodeConnection is dead — never read by the generator — skipped.)

        # Rewrite exit_block slugs to UUIDs (verbatim with the DB path, minus save)
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

    graph.starting_canvas = starting_canvas
    graph.ids = {
        "project_id": str(project.id),
        "player_id": str(player.id),
        "npc_ids": npc_ids,
        "location_ids": [str(slug_map[s].id) for s in slug_map.keys()],
        "canvas_ids": [str(sc.id) for sc in canvas_slug_map.values()],
        "node_count": len(node_slug_map),
        "starting_canvas_id": (str(starting_canvas.id) if starting_canvas else None),
        "starting_canvas_name": starting_canvas.name if starting_canvas else None,
        "starting_canvas_nodes": starting_canvas_node_count,
        "template_starting_canvas_slug": template.starting_canvas,
        "available_canvas_slugs": list(canvas_slug_map.keys()),
    }
    return graph


def build_game_from_toml(
    toml_path: str,
    *,
    output: str,
    video_folder: Optional[str] = None,
    video_path: Optional[str] = None,
    local_media: bool = False,
    dev_mode: bool = False,
    debug: bool = False,
    name_override: Optional[str] = None,
    system_type: str = "twee_comprehensive",
    version: str = "v2",
    build: str = "free",
) -> dict:
    """Build a game HTML package from a single TOML file with ZERO database interaction.

    parse → validate → build_game_graph → flag-chain validate → package. No DB,
    no owner, nothing persisted. Returns the package manifest (html_path, media
    stats, …). Raises ValueError on parse / template / flag-chain validation
    failure. Reusable by the CLI command and the author-game / find-media /
    edit_game skills. `output` must be an absolute path.
    """
    from apps.game_generation.services.game_service import GameService
    from apps.projects.services.template_import import (
        normalize,
        parse_toml,
        validate,
    )

    template = normalize(parse_toml(toml_path))
    errors = validate(template)
    if errors:
        raise ValueError(f"TOML validation failed: {errors}")

    graph = build_game_graph(template, name_override)

    # Flag-chain validation over the in-memory graph (twee_comprehensive only).
    if system_type == "twee_comprehensive" and version == "v2":
        from apps.game_generation.twee_comprehensive.generators.v2 import (
            TweeComprehensiveGeneratorV2,
        )

        gen = TweeComprehensiveGeneratorV2()
        gen.project = graph.project
        gen.graph = graph
        gen.locations = graph.locations
        fc_errors = gen.validate_flag_chains()
        if fc_errors:
            raise ValueError(f"Flag chain validation failed: {fc_errors}")

    # Rewritten from `{"dev_mode": True} if dev_mode else None` — it could only ever
    # carry one key. `build` defaults to "free", so a caller that has never heard of
    # the cheat page cannot produce a paid file.
    options = {"build": "paid" if build == "paid" else "free"}
    if dev_mode:
        options["dev_mode"] = True
    return GameService().package_game(
        project=graph.project,
        system_type=system_type,
        output_dir=output,
        version=version,
        local_media=local_media,
        video_folder=video_folder,
        video_path=video_path,
        debug=debug,
        options=options,
        graph=graph,
    )
