# prompts_v2 — Index

The prompt pipeline for RTS-shape sandbox adult interactive fiction games. Replaces the frozen-at-2026-04-19 `prompts/` folder (which stays as historical record per Doc 66 §6.7).

**Status:** 100% complete (21 files, ~24K lines). Doc 66 Batches 1+2+3 all shipped (commits `9c2e450` / `2dffd7a` / Batch 3 final).

---

## What this folder is

A complete LLM-consumable prompt corpus for generating RTS-shape sandbox games. Hand any modern LLM the full corpus + an LO game concept input, and it produces:

1. **A design book** (Stage 1) — structured markdown with per-NPC R7 briefs + world setup + capstone chains
2. **A TOML file** (Stage 2) — valid against `apps/projects/services/template_import.py` schema; builds via `python manage.py package_from_toml`
3. **Media assets** (Stage 3) — images + videos per canvas image block
4. **A publish-ready listing** (Stage 4) — description + tags for distribution sites

The pipeline produces RTS-shape sandbox games (per Road to Success doctrine; not Jack's World / New In Town / Two Weeks shape).

---

## LO's 7 locked decisions (Doc 66 §6, 2026-05-26)

These constrain everything in the corpus:

1. **Every game is RTS-shape.** No selectable shapes; no "Single-NPC Romance vs Multi-NPC Parallel Arcs" architecture choice.
2. **Greenfield `prompts_v2/`.** Clean slate. Nothing inherited from `prompts/` except deliberately ported mechanics (stages/03-04).
3. **RTS-only reference + explicit ignore list.** Jack's World / New In Town / Two Weeks / Pattern A–J / 7-driver / archetype-system / whiteboard-goals / narrative-gates / income-channels = NAMED AS IGNORED in `00_LEGACY_IGNORE.md` §3.
4. **Ignore CLAUDE.md.** No carve-outs in v2. The prompts override CLAUDE.md when active.
5. **Regenerate COMPREHENSIVE.** Done — see `prompts_v2/COMPREHENSIVE_SYSTEM_REFERENCE.md`.
6. **Ignore context window.** No size budget; correctness first.
7. **No migration.** Legacy games (Two Weeks / Jack's World / New In Town) dropped. They stay as historical record; the new pipeline is unburdened by backward compat.

---

## Scope modes (added 2026-05-29)

The pipeline supports two scope modes:

- **`scope_mode: full_game`** (DEFAULT) — produces a complete game. Per-arc-shape FULL canvas budgets per `doctrine/03_arc_shapes.md` §2 (family/ambient 25–35, slow-burn 10–15, peer/dating 8–12, service 6–10, antagonist 6–10). Full Stage 0→4 trajectories per NPC. Full capstone chains per Doc 57. Phase 2+ Strategic Scope decisions (pregnancy / scandal / gallery / tracker per Doc 65) surface as interactive Q&A at Stage 1 §0.
- **`scope_mode: slice`** — produces a shippable validating chunk. ~10–14 day playable window. 1 NPC at full depth (gold standard) + 4–5 NPCs at minimum-contract depth. Locked-visible escalation rungs telegraph deferred arcs. All four Phase 2+ decisions default to "defer." Used for doctrine validation, dev cycles, incremental expansion (the TLS test slice was authored in this mode).

Concept input declares scope mode explicitly. If omitted, default to `full_game`. Slice authoring is preserved as opt-in for incremental work; the locked-visible escalation ladder applies at BOTH scopes as a UI/pacing device (see `doctrine/03_arc_shapes.md` §10).

### Invocation example (full_game mode)

```
[Attach: prompts_v2/COMPREHENSIVE_SYSTEM_REFERENCE.md]

Execute Stage 1 per `stages/01_game_book_prompt.md`.

## Concept
scope_mode: full_game
Title: <working title>
Setting: <one-paragraph setup>
Cast: <NPCs + arc shape hints; let doctrine pick if unsure>
Constraints: <kink ceilings, time model overrides, etc.>
Phase 2+ decisions: <leave blank to trigger Stage 1 §0 Q&A; or specify
  pregnancy/scandal/gallery/tracker = include|defer per Doc 65>

## Output
Single Markdown game-book per `stages/01_game_book_prompt.md` deliverable spec.
```

### Invocation example (slice mode, opt-in)

```
[Same attachment]

Execute Stage 1 per `stages/01_game_book_prompt.md`.

## Concept
scope_mode: slice
Title: <working title>
... (rest as above)
Slice scope: <N>-day window; 1 NPC at full depth + 4-5 NPCs at minimum-contract
```

---

## Folder structure (21 files)

```
prompts_v2/
├── 00_LEGACY_IGNORE.md                  # Explicit "do NOT use these" list
├── README.md                            # This file
├── COMPREHENSIVE_SYSTEM_REFERENCE.md    # All 21 files concatenated (mechanical)
│
├── stages/                              # LLM-consumed pipeline prompts
│   ├── 01_game_book_prompt.md           # Stage 1: input concept → design book
│   ├── 02_toml_generation_prompt.md     # Stage 2: design book → TOML
│   ├── 03_image_finder_prompt.md        # Stage 3: image/video search per canvas
│   └── 04_game_listing_prompt.md        # Stage 4: back-of-book blurb for publishing
│
├── doctrine/                            # Consulted at every stage
│   ├── 01_rts_principles.md             # P1–P10 (Doc 56 §2)
│   ├── 02_three_lanes_plus_capstone.md  # Lanes 1/2/3 + Lane 4 capstone (Doc 24 + 57 + 67)
│   ├── 03_arc_shapes.md                 # 5 arc shapes + per-shape distribution (Doc 56 §5)
│   ├── 04_authoring_rules.md            # R1–R7 (Doc 56) + R1–R6 (Doc 50) + R1–R5 (Doc 57) + F1–F5 + R1–R7 (Doc 67)
│   ├── 05_rts_flat_prose.md             # 8 prose rules + dual register (Lane 1/2/3 RTS-flat vs Lane 4 Tier-3)
│   ├── 06_design_brief_template.md      # R7 brief template + Frank/Marge gold standards
│   ├── 07_anti_patterns.md              # Doc 54's 27 failure modes + cross-doc catalog
│   ├── 08_kink_vocab_ceilings.md        # Doc 30 §7.5 verbatim + default-explicit pattern
│   ├── 09_trait_catalog.md              # Tier 1 + Tier 2 traits + stage internal-only doctrine
│   ├── 10_location_design.md            # location layering + reachability triad (silent-runtime bug prevention)
│   ├── 11_clothing_design.md            # clothing → public content + beauty/exhibitionism axes (NPC arcs never read the outfit)
│   ├── 12_rent_economy_design.md        # rent = the money drive: arm-after, eviction-mode choice, budget math, scoping trap
│   ├── 13_phone_design.md               # phone = the digital surface: chat threads on real flags, photo-action tiers, purchase gate, no day/time triggers
│   └── 14_customization_design.md       # player/NPC personalization: the @player/@npc token contract + the un-tokenizable-surface trap (location/sidebar labels)
│
├── reference/                           # RTS extraction (replaces Jack's World docs)
│   ├── 01_rts_overview.md               # Game shape + bootstrap + writing tiers
│   ├── 02_rts_scene_catalog.md          # Brother / Dad / Marcus / Edward scene tables + 6 patterns A–F
│   ├── 03_rts_walkthrough_panel.md      # P2 transparent-gating UI doctrine
│   └── 04_rts_hud_world_model.md        # P10 sidebar = world model
│
└── schema/                              # Engine capability surface
    ├── 01_engine_capabilities.md        # Every engine primitive with v2.py line numbers
    ├── 02_toml_schema.md                # Per-section field tables + minimal RTS-shape skeleton
    └── 03_example_toml.md               # TLS Frank slice canonical TOML excerpts
```

---

## Reading order for fresh LLM sessions

If you're picking up the corpus fresh (no prior context), read in this order:

1. **`00_LEGACY_IGNORE.md`** — what to NOT reach for. Sets vocabulary discipline.
2. **`doctrine/01_rts_principles.md`** — P1–P10. The heart of the design philosophy.
3. **`doctrine/02_three_lanes_plus_capstone.md`** — the mechanism vocabulary.
4. **`doctrine/03_arc_shapes.md`** — the 5 shapes the cast picks from.
5. **`doctrine/04_authoring_rules.md`** — the rule layer (R1–R7 + R1–R6 + R1–R5 + F1–F5 + R1–R7).
6. **`doctrine/06_design_brief_template.md`** — the R7 brief template Stage 1 produces.
7. **`doctrine/09_trait_catalog.md`** — the canonical trait vocabulary.

**For Stage 1 authoring** (game-book), additionally:
- `reference/01_rts_overview.md` — RTS broad context
- `reference/02_rts_scene_catalog.md` — per-NPC scene catalogs
- `doctrine/05_rts_flat_prose.md` — voice register
- `doctrine/08_kink_vocab_ceilings.md` — per-arc vocab register

**For Stage 2 authoring** (TOML), additionally:
- `schema/01_engine_capabilities.md` — engine primitives
- `schema/02_toml_schema.md` — TOML schema
- `schema/03_example_toml.md` — canonical TLS Frank slice excerpts
- `doctrine/07_anti_patterns.md` — anti-pattern catalog
- `reference/03_rts_walkthrough_panel.md` + `reference/04_rts_hud_world_model.md` — UI surfaces

**For Stages 3 + 4** (media + listing): the respective stage prompt is self-contained.

If you only have time for THREE files: `doctrine/01_rts_principles.md` + `doctrine/02_three_lanes_plus_capstone.md` + `doctrine/06_design_brief_template.md`. These three contain the design philosophy + mechanism + brief shape — enough to author against doctrine in the abstract.

---

## How to invoke the pipeline

The pipeline is 4 stages. Each stage's prompt is self-contained; the LLM is given the prompt + the previous stage's output.

```
LO concept input
       │
       ▼
┌──────────────────────────────────────┐
│  Stage 1: stages/01_game_book_prompt │   →   design book (markdown)
└──────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│  Stage 2: stages/02_toml_generation  │   →   slice    → 7_final_game.toml (1 response)
│                                      │       full_game → phases 0-6 (7 responses)
└──────────────────────────────────────┘                  + merge via scripts/merge_toml_phases.py
       │
       ├──────────────────────────────────┐
       ▼                                  ▼
┌─────────────────────────┐  ┌────────────────────────┐
│ Stage 3: image_finder   │  │ Stage 4: game_listing  │
│ → images + video clips  │  │ → description + tags   │
└─────────────────────────┘  └────────────────────────┘
       │
       ▼
   merge:    python scripts/merge_toml_phases.py games/<game_slug> --validate    (full_game only)
   build:    python manage.py package_from_toml --file games/<game_slug>/toml_phases/7_final_game.toml --owner-id <uuid> --output games/<game_slug>/output --dev
   play:     open games/<game_slug>/output/index.html
```

### Stage invocation

For each stage, the LLM is given:
1. The stage prompt (e.g., `stages/01_game_book_prompt.md`)
2. The previous stage's output (concept input for Stage 1; design book for Stage 2; TOML for Stages 3+4)
3. (Optional but recommended) The relevant `doctrine/` + `reference/` + `schema/` files cited by the stage prompt

For Stage 1: cite `doctrine/01–09` + `reference/01–04`. For Stage 2: cite `schema/01–03` + `doctrine/02, 04, 05, 07, 09`. Stages 3 + 4 are mostly self-contained.

### Game folder convention

Each generated game lives at `games/<game_slug>/`:

```
games/<game_slug>/
├── concept.md                       # Stage 1 output (markdown design book)
├── toml_phases/
│   ├── 0_systems_spec.toml          # ┐
│   ├── 1_metadata_and_locations.toml│ │
│   ├── 2_one_shots.toml             │ ├─ Stage 2 phased output at full_game
│   ├── 3_activities.toml            │ │  (one phase per LLM response)
│   ├── 4_story_arc.toml             │ │
│   ├── 5_scenes.toml                │ │
│   ├── 6_dev_shortcuts.toml         │ ┘
│   └── 7_final_game.toml            # merged from 0-6 via scripts/merge_toml_phases.py
├── output/                          # build output (Twine HTML)
└── videos/                          # optional media assets per stages/03
```

At `scope_mode: slice`, Stage 2 emits one TOML directly to `7_final_game.toml` (no phased breakdown, no merge step). At `scope_mode: full_game`, Stage 2 emits phases 0–6 (one per response) and you run the merge script. See `stages/02_toml_generation_prompt.md` §12.5 for the per-phase content contract.

### Validation + build

After Stage 2 produces TOML (and at full_game, after the merge):

```bash
cd <story_gen_django>

# At full_game only — merge phases 0-6 into 7_final_game.toml
python scripts/merge_toml_phases.py games/<game_slug> --validate

# Build (both scope modes)
python manage.py package_from_toml \
  --file games/<game_slug>/toml_phases/7_final_game.toml \
  --owner-id <uuid> \
  --output games/<game_slug>/output \
  --dev
```

The validator (`apps/projects/services/template_import.py:validate()`) catches schema errors + a subset of doctrine violations (quest card R1–R4, undeclared traits in sidebar items, worn_type typos, etc.). Build proceeds on warnings; halts on errors.

After validation, compile + run a smoke test in a browser before LO sign-off (per `doctrine/07_anti_patterns.md` §7.3 — live-play is part of pre-ship verification, not deferred to user).

---

## Maintenance notes

### When to regenerate COMPREHENSIVE_SYSTEM_REFERENCE.md

Any source file change → regenerate via the same bash script in `<this folder>/COMPREHENSIVE_SYSTEM_REFERENCE.md` § "Generation." The concat is mechanically derivable; never edit it by hand.

### When to revisit doctrine

The doctrine files (`doctrine/01–09`) are stable per Doc 66 §6 — they capture LO-locked decisions and verified RTS evidence. Revisit when:

- LO surfaces a new locked decision (e.g., "ship pregnancy in Phase 2+") that affects doctrine
- A new RTS reference extraction (deeper Brother audit; new NPC arcs) surfaces a 7th principle or rule
- The TLS test slice produces a failure mode not in `doctrine/07_anti_patterns.md` — add to the catalog
- An engine PRD ships (Doc 62 / 63 / 64) that changes the schema layer

### When to revisit reference

The reference files (`reference/01–04`) are RTS extraction snapshots. Revisit when:

- A new RTS playthrough surfaces patterns/behaviors not in the catalog
- Doc 13 / 21 / 22 source docs get extended

### Source-of-truth cross-references

Each `prompts_v2/` doctrine file lists its source doc(s) in `28th_april_TLS_Phase2_Redesign/`. The source docs are the canonical record; `prompts_v2/` is the distilled LLM-consumable form. Source docs may evolve faster than `prompts_v2/` — when they do, the doctrine file should be revisited to reflect the change.

---

## Cross-references

### Source docs (`28th_april_TLS_Phase2_Redesign/`)

The 70+ doctrine docs that feed `prompts_v2/`. Read these when you need the full-detail backstory + open questions + LO decision trails. Load-bearing docs:

- **Doc 13** — Road to Success Reference (the RTS catalog)
- **Doc 24** — 3 Lanes for Repeatable NPC Content
- **Doc 30** — TLS Test Redesign PRD (master design vision)
- **Doc 31** — Frank Arc Design Brief (family/ambient gold standard)
- **Doc 50** — Quest Card Shape Doctrine
- **Doc 53** — Marge Redesign Brief (service gold standard)
- **Doc 54** — Marge Redesign Session Lessons (27 failure modes)
- **Doc 56** — RTS Principles & TLS Alignment Doctrine
- **Doc 57** — Capstone Doctrine / Lane 4
- **Doc 66** — Session record / Prompts Rewrite Pivot (this folder's origin)
- **Doc 67** — Solo Activity Design & Multi-NPC Dispatcher Doctrine
- **Doc 68** — Trait Catalog

### Engine

- `apps/projects/services/template_import.py` — schema + validator (~9,800 lines)
- `apps/game_generation/twee_comprehensive/generators/v2.py` — TOML → Twine emitter (~17,500 lines)
- `apps/game_generation/twee_comprehensive/generators/v1.py` — frozen rollback (do NOT edit)

### Legacy

- `prompts/` — pre-2026-04-19 corpus. Historical record only per LO §6.7. No migration; no inheritance.

---

**End of file.** The pipeline is complete. Invoke per §"How to invoke the pipeline" above.
