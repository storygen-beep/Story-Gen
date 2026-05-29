# Doc 62 — Canvas `guide` Field Schema PRD

**Session:** 2026-05-25
**Branch:** `feature/prd-48-quests-engine-v2-bundled` (off `main`, unpushed)
**Author:** ENI (with LO)
**Status:** Engine PRD — implementation spec; NOT shipped. Doctrine locked in Doc 56 R5; schema work locked here.
**Supersedes:** nothing
**Sibling of:** Doc 63 (Validator Extension PRD), Doc 64 (Sidebar NPC Radar PRD), Doc 48 (Quests Engine V2 PRD — sibling shape of engine work)
**Triggered by:** Doc 56 R5 — every canvas must declare a player-facing `guide` string (player-facing trigger recipe). Schema field not yet added. This PRD locks the implementation. Catalog UI (Doc 56 P2 deferred) consumes the field; landing the schema NOW means new authoring carries it forward instead of requiring backfill later.

---

## §1 — The problem this PRD solves

Doc 56 R5 commits the doctrine: every canvas declares a `guide` string. The doctrine cannot land in TOML until the schema accepts the field. Each new canvas authored from now on without the field creates backfill debt.

Without the field:
- Catalog UI (Doc 56 P2 / Doc 13 §14) can't render trigger recipes per canvas. Players can't see Lane 3 substitution recipes (`"Make tea in the kitchen while Frank is home"`) — invisible content is unplayable for that lane.
- Validator (Doc 63 PRD) can't enforce R5 presence.
- Authoring discipline drifts — Lane 3 substitutions get authored without thinking about how the player discovers them.

The schema cost is small. The doctrine cost of NOT shipping it is large.

---

## §2 — What `guide` is

A one-sentence, player-facing recipe in plain English. Names the lane. Future catalog UI renders it verbatim.

**Convention table** (per Doc 56 R5):

| Lane | Phrasing convention | Example |
|---|---|---|
| Lane 1 (hub) | "Visit X" / "Go to Y and Z" | "Visit Frank in his kitchen during breakfast" |
| Lane 2 (ambient random) | "Walk into X" / "Pass through Y" | "Walk into the kitchen late at night" |
| Lane 3 (substitution) | Activity name + condition | "Make tea in the kitchen while Frank is home" |
| Lane 4 capstone | Narrative milestone | "After the catch, return to Frank's bedroom in the evening" |

Style: player-facing, second-person or Maya-third, short. Not a marketing line; a recipe.

**Not the same as `description`** (which is for developer/author notes). `description` stays internal; `guide` is the player-visible string.

---

## §3 — Schema addition

File: `apps/projects/services/template_import.py`

### Field addition

In the `TemplateCanvas` dataclass (verified at lines 650–658), add:

```python
@dataclass
class TemplateCanvas:
    id: str
    name: str
    description: str = ""
    guide: str = ""    # NEW — Doc 62 / Doc 56 R5
    trigger: TemplateTrigger = field(default_factory=TemplateTrigger)
    nodes: List[TemplateStoryNode] = field(default_factory=list)
    connections: List[Dict[str, Any]] = field(default_factory=list)
    loop: Optional[Dict[str, Any]] = None
```

### Precedent / model

Model on `TemplateStoryNode.guide_hint: str = ""` at template_import.py:696 — already serialized into `help_data` at runtime (line 9691: `"guide_hint": node.get("guide_hint", "")`).

Same shape:
- Default empty string (back-compat — existing canvases don't break)
- Serialized at the same emission point as `guide_hint` (both are player-facing prose surfaces)
- No validation on content (just present-or-not; Doc 63 validator handles presence enforcement when the rule activates)

### Parser hook

Wherever `TemplateCanvas` is constructed from raw TOML dict (find the parser function — likely in `template_import.py`), include `guide = data.get('guide', '')`. Should be a 1-line addition matching the existing `description` parse.

### Serializer hook

In `_build_help_data()` at template_import.py:9510, where canvas-level metadata is emitted (lines 9675–9793 per agent inventory), add `guide` to the dict alongside `description`. Pattern match the existing `guide_hint` emission at line 9691.

If the serializer emits canvases into a `canvasGuides` map separate from the activity records (cleaner for the future catalog UI to consume), that's preferred. Otherwise inline emission on the activity record is fine.

---

## §4 — Runtime exposure

The serialized canvas guides land in `setup.help_data` per v1.py:2445. Available to:

- **Future catalog UI** (Doc 56 P2 deferred) — iterates `setup.help_data` canvas entries to render the published-scene-table. Each row's GUIDE column reads from the canvas's `guide` field.
- **Future validator surface** (Doc 63) — quest cards' `ready_canvas` pointer can be checked against the target canvas's `guide` for consistency (does the card's `tip` match the canvas's `guide`?).
- **Dev tooling** — debug surface listing all canvas guides for authoring review.

No JS-side rendering changes in this PRD. The field is **schema-only**. Rendering = Doc 65 (catalog) or a separate dev-tool PRD.

---

## §5 — Authoring convention

Per Doc 56 R5 table (§2 above). Additional style guidance:

- **Match the player's POV.** "Visit Frank" not "Frank gets visited."
- **Name the lane in plain English** — don't reference TOML mechanics. "Make tea in the kitchen while Frank is home" not "trigger substitution on activity_make_tea while npc_frank.location matches loc_kitchen."
- **One sentence.** Multi-sentence guides bloat the catalog and undermine the recipe shape.
- **Time/schedule cues land as natural language.** "during breakfast" / "late at night" / "after work" — not "06:00-09:00 weekdays."
- **Condition cues land as natural language.** "while Frank is home" / "once Maya has the apartment key" — not raw flag names.

Concrete examples for current TLS canvases (forward-reference for backfill):

| Canvas | Lane | Proposed `guide` |
|---|---|---|
| `scene_yard_with_ryan` | L2 | "Walk into the yard while Ryan is working" |
| `activity_make_tea` | L3 parent | "Make tea in the kitchen" |
| `scene_frank_passes_kitchen_door` | L3 substitution target | "Make tea in the kitchen while Frank is around" |
| `scene_franks_bedroom_evening` | Lane 4 capstone | "Visit Frank's bedroom in the evening after Frank's catch" |
| `canvas_marge_interview` | Lane 4 capstone | "Walk into the diner for the first time" |
| `transition_jake_to_1_via_beauty` | Lane 4 capstone | "Pass Jake's door looking your best (Maya's beauty ≥ 50)" |
| `frank_kitchen_morning_hub` | L1 hub | "Visit the kitchen in the morning while Frank is there" |

---

## §6 — Backfill plan

All 83 existing TLS canvases need `guide` authored. Phased:

1. **Frank slice** (~28 canvases) — author guides during the next Frank polish pass. ~1.5 hours.
2. **Other NPCs** (Marge ~8, Ryan ~6, Jake ~6, Diana ~4, Cookie ~2) — ~1 hour.
3. **Solo activities + situational capstones** (~8 + ~5) — ~30 min.
4. **Hub stubs + dev shortcuts** — guide can be empty for dev shortcuts (they're not player-facing). ~15 min.

**Total backfill: ~3-5 hours of authoring.** Ship after schema lands. Until backfilled, new canvases ship with `guide` and existing canvases default to empty string — both render correctly in the catalog (empty just means "no recipe published yet").

**Validator soft-warn vs hard-error:** Doc 63 PRD addresses validator enforcement of R5 presence. Likely starts as a warning (not an error) so existing canvases without guides don't fail builds during backfill.

---

## §7 — Tests

In `apps/projects/tests.py` (or wherever template_import tests live):

1. **Round-trip test.** Canvas with `guide = "Visit Frank in the kitchen"` round-trips through parser + serializer; field present in output.
2. **Default test.** Canvas without `guide` declared parses with empty string default.
3. **Help data emission test.** `_build_help_data()` includes `guide` field in canvas entries.
4. **Back-compat test.** Existing TLS slice TOML parses cleanly post-schema-add (no field-strict rejection of canvases lacking `guide`).

Pattern match existing `guide_hint` tests if any exist (search for `guide_hint` in tests). Otherwise model the round-trip on existing canvas field tests.

---

## §8 — Engine work estimate

| Task | Estimated time |
|---|---:|
| Schema field addition (TemplateCanvas dataclass) | 5 min |
| Parser hook (data.get pattern) | 5 min |
| Serializer hook (_build_help_data emission) | 15 min |
| Tests (4 cases) | 30 min |
| TOML round-trip validation against TLS slice | 15 min |
| Total | **~1 hour** |

Trivial scope. The doctrine work was the hard part; the schema is the codification.

---

## §9 — Out of scope (intentional)

- **Catalog UI** — separate doc / future PRD. This PRD only adds the data primitive.
- **Validator enforcement of R5 presence** — Doc 63 PRD. Likely lands as a warning that escalates to error post-backfill.
- **Backfill itself** — listed in §6 but execution is separate authoring work, not this PRD's implementation scope.
- **Schema for `guide_hint` → `guide` migration on existing TemplateStoryNode** — `guide_hint` stays as-is for story arc nodes; `guide` is a NEW field on Canvas. Don't conflate.
- **Localization / i18n of guide strings** — currently TLS ships single-language. Localization is its own PRD if/when multi-language ships.
- **`guide` field on other entity types** (e.g., `[[npcs]]`, `[[locations]]`) — locations may benefit from a `guide` too (per Doc 13 §14 RTS Walkthrough has a Location Scenes section). Defer to a follow-up PRD if catalog UI needs it.

---

## §10 — References

### Sibling and ancestor docs

- **Doc 13** — Road to Success Reference (§14 RTS Walkthrough as published catalog — the surface `guide` feeds)
- **Doc 48** — Quests Engine V2 PRD (sibling-shape engine PRD)
- **Doc 56** — RTS Principles & TLS Alignment Doctrine (R5 doctrine commit)
- **Doc 63** — Validator Extension PRD (will enforce R5 presence)
- **Doc 64** — Sidebar NPC Radar PRD (sibling engine work)
- **Doc 65** — Phase 2+ Strategic Scope (Catalog UI in P2+ scope; depends on this PRD shipping)

### Live engine references (verified)

- `apps/projects/services/template_import.py:650-658` — `TemplateCanvas` dataclass
- `apps/projects/services/template_import.py:696` — `TemplateStoryNode.guide_hint` (precedent)
- `apps/projects/services/template_import.py:9510-9809` — `_build_help_data()` serializer
- `apps/projects/services/template_import.py:9691` — `guide_hint` emission (model for new `guide` emission)
- `apps/game_generation/twee_comprehensive/generators/v1.py:2445` — `setup.help_data` runtime exposure
