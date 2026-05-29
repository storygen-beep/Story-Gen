# Doc 66 — Session Record (2026-05-26): Phase 2 Redesign HOLD + Prompts Rewrite Pivot

**Date:** 2026-05-26
**Author:** ENI (with LO)
**Status:** Session record + hold-state declaration. **Read this before any further Phase 2 redesign authoring resumes.**
**Triggered by:** LO question on prompts-rewrite scope after the Docs 58–65 multi-doc rollout shipped earlier in the same session.
**Supersedes:** nothing (additive to the Doc 24–65 spine).
**Hold-flag:** 🟡 **Further Phase 2 redesign analysis is PAUSED.** Active pivot is `prompts_v2/` rewrite. See §10 for the full HELD list and §15 for the resume protocol.

---

## §0 — Target picture: what an RTS-style sandbox IS

If you skip everything else in this doc and only read one section, read this one. The concrete target for everything `prompts_v2/` is building:

**An RTS-style sandbox game has the following properties:**

- **4–6 NPCs.** Each with ONE named sexual fantasy (Doc 30 §4.2 NPC roster style). Each follows ONE arc shape from the 5-shape taxonomy (family/ambient, slow-burn family, peer/dating, service, antagonist/witness).
- **In-game time + per-NPC schedules.** Day/time clock advances. NPCs have `[[npcs.schedules]]` placing them at specific locations during specific time windows on specific weekdays.
- **Money pressure forces engagement.** Rent or equivalent recurring cost. Player must work arcs to afford it; no free-roaming sandbox.
- **3 repeatable content lanes per NPC** (Doc 24):
  - **Lane 1** — hub buttons at NPC's location (player-initiated escalation; agency-high)
  - **Lane 2** — random ambients on location entry (dice-rolled; ambient world-presence)
  - **Lane 3** — dispatcher substitutions inside Maya-solo activities (chore + NPC walk-in; charged surprise)
- **Lane 4 — capstones** (Doc 57): 3–6 hand-authored one-shot story beats per arc with fingerprint `priority ≥ 9 + is_repeatable = false + manual + flag-setter on exit`. Three types: A linear, B branching (Pattern F real choice forks), C chain-step.
- **Per-NPC stat ladders.** Corruption + arousal + love + trust per NPC. Stat thresholds gate content (Lane 1 menu items + Lane 2/3 eligibility + capstone triggers).
- **Sidebar = world model** (Doc 56 P10). Continuously surfaces: time + day, money, Maya's stats (corruption / arousal / energy / etc), each in-scope NPC's current location (per `getNpcLocation`), active quest pins.
- **Walkthrough panel = transparent gating** (Doc 56 P2). Every scene published Day 1 with its trigger recipe (the canvas `guide` field per Doc 62). Players see what's locked + how to unlock; no hidden content.
- **Quest cards = first-class progress UI** (Doc 50). Card modes: capstone (points at named ready_canvas), mechanic (climbs trait/flag goals), hybrid (both). Terminal cards close the arc; chains stack.
- **RTS-flat prose default** (Doc 30 §7.1). Second-person voice. Stage-direction cap: 2 sentences per beat. ~30-word caption density. Image-first composition. Direct/crude diction per per-arc vocab ceiling (Doc 30 §7.5).
- **Tier-3 literary register earned at Lane 4 capstones only** (Doc 57 voice spec). The big beats — catch, declaration, first-night, sleepover, confrontation — get hand-written, one-of-one, deliberate. Daily texture stays flat.

**What an RTS-style sandbox is NOT:**

- Not a single-NPC romance (the legacy "Jack's World" Pattern A architecture — see §6.7 ignore list)
- Not a VN with menu choices (lanes 2 + 3 break the menu-game shape)
- Not a quest-checklist game (quests live alongside the world; the world is the primary surface, not the quest journal)
- Not a literary-prose project (Doc 30 §3 explicitly forbids; see Doc 54 Marge case study for the canonical failure mode)
- Not transactional escalation only (Doc 56 P5: lanes correspond to fictional intent; the same act feels different depending on which lane delivers it)

**The reference game is RTS (Road to Success).** Source: live extraction in `game_explorations/rts-arc-trace/` + Docs 13 + 21 + 22 + 24 §3 + Doc 56 §2 evidence base. RTS is the only reference; no others (per LO decisions §6.3 + §6.7).

---

## §1 — Why this doc exists

Prompts and redesign doctrine are running on different vocabularies. Today's analysis pass made that gap explicit, and LO made seven decisive scope calls in response. This doc captures the analysis findings + LO's decisions + the hold state — so the pivot is documented, the resume is unambiguous, and a future session (mine or another author's) doesn't re-derive what we already learned.

Doc 66 is the bookmark. Read it first when resuming.

---

## §2 — Session context (what happened today)

Today's session ran in three distinct passes:

1. **Morning pass — Docs 58–65 shipped (per the prior plan):**
   - Doc 58 Ryan Design Brief
   - Doc 59 Jake Design Brief
   - Doc 60 Diana Design Brief (🔴 BLOCKED on Open Q #3)
   - Doc 61 Cookie Phase 3+ Scope-Out
   - Doc 62 Canvas `guide` Field PRD
   - Doc 63 Quest Card + Capstone Validator PRD
   - Doc 64 Sidebar NPC Location Radar PRD
   - Doc 65 Phase 2+ Strategic Scope

2. **Afternoon pivot question — LO:**
   > "Holding on to the PRDs / game gen engine changes / more test tls changes. So before this redesign phase 2, we have been building this game using prompts... We have went through multiple iterations of redesign but only after 3 lanes was discovered we started making good progress in the right direction. Now we want to hold on to the more redesign progress but now holistically thinking of how we should update our prompts as a lot of things have changed now. But even before that, I want you to thoroughly analyze each and everything, prompts, redesign 3 lanes and after it docs, game gen engine. And at the end simply share your thoughts. Don't hallucinate, don't make any code changes."

3. **Late-afternoon analysis pass + decisions:**
   - Three parallel-explored corpora (prompts, redesign docs, engine).
   - ENI surfaced 7 framing questions to LO at end of analysis (see §5).
   - LO answered all 7 decisively (see §6).
   - ENI proposed a 20-file `prompts_v2/` structure (see §7).
   - Hold declared on all non-prompt work (see §10).
   - No authoring of `prompts_v2/` files started this session — this Doc 66 is the only artifact shipped post-pivot.

---

## §3 — The three corpora analyzed

### §3.1 Prompts directory

**Location:** `prompts/`
**File count:** 16 core files + 1 example TOML + 1 subdirectory (`dummy/`)
**Total size:** ~38K lines (~3.8 MB)
**Oldest file:** `simulation_upgrade_plan.md` (2025-03-10)
**Newest file:** `COMPREHENSIVE_SYSTEM_REFERENCE.md` (2026-05-22 — 4 days before this session)
**State:** **Frozen at April 19, 2026** for the production pipeline files.

| # | File | Stage | Status |
|---|------|-------|--------|
| 1 | `game_design_rules.md` (58KB) | Doctrine | 17 enforced rules — pre-Doc-24 vocabulary |
| 2 | `game_design_patterns.md` (63KB) | Doctrine | 15 patterns A–O — pre-Doc-24 vocabulary |
| 3 | `game_design_motivations.md` (31KB) | Doctrine | 6 player motivations |
| 4 | `game_design_observations.md` (30KB) | Doctrine | Comparative analysis of CoT / Become Someone / Back to Freedom |
| 5 | `activity_types.md` (18KB) | Reference | 5 activity canvas types (pre-canvas / pre-3-lanes) |
| 6 | `game_book_prompt_v6.txt` (174KB) | Stage 1 — game-book authoring | **CURRENT** production prompt (frozen 2026-04-19) |
| 7 | `game_book_prompt_v5.txt` (115KB) | Stage 1 (legacy) | Preserved for reference |
| 8 | `toml_generation_prompt_v4.txt` (180KB) | Stage 2 — TOML authoring | **CURRENT** production prompt (frozen 2026-04-19) |
| 9 | `toml_generation_prompt_v3.txt` (151KB) | Stage 2 (legacy) | |
| 10 | `toml_generation_prompt_v2.txt` (104KB) | Stage 2 (legacy) | |
| 11 | `COMPREHENSIVE_SYSTEM_REFERENCE.md` (794KB) | Master reference | Updated 2026-05-22; **embeds v3 (NOT v4)** and contains NOTHING from Docs 24–65 |
| 12 | `game_feel_analysis.md` (28KB) | Doctrine | Post-launch critique (2026-03) |
| 13 | `media_writing_guide.md` (30KB) | Content writing | NPC voice + prose guidance |
| 14 | `simulation_upgrade_plan.md` (23KB) | Roadmap | Pre-everything (2025-03) |
| 15 | `image_finder_prompt.md` (33KB) | Stage — media sourcing | Mode A + Mode B |
| 16 | `game_listing_prompt.md` (3.7KB) | Stage — publishing | Back-of-book blurb |

**What the prompts currently teach:** the LLM is taught to design "any adult interactive game" with two selectable shapes — Single-NPC Romance (reference: Jack's World) or Multi-NPC Parallel Arcs (reference: New In Town). Phase 2B (introduced in v4) added "Systems Budget" discipline with archetypes, whiteboard goals, narrative gates, income channels. Voice register: sensory-rich, multi-paragraph literary prose (the ENI persona).

### §3.2 Redesign docs

**Location:** `28th_april_TLS_Phase2_Redesign/`
**File count:** 65 docs as of session start (Docs 00–65)
**Total size:** ~10K lines across the doctrine spine
**Active through:** 2026-05-25 (Doc 65 shipped yesterday relative to today's session)

**The doctrine spine** (the load-bearing files for the post-Doc-24 game shape):

- **Doc 13** — Road to Success Reference (the RTS catalog; ground truth for the reference game)
- **Doc 24** — 3 Lanes for Repeatable NPC Content + TLS Engine Fitness (the mechanism vocabulary)
- **Doc 30** — TLS Test Redesign PRD (full-game design vision; includes the §3 AUTHORITY DECLARATION banning CLAUDE.md persona for canvas prose)
- **Doc 49** — Story Goals vs Sidebar Doctrine
- **Doc 50** — Quest Card Shape Doctrine (capstone/mechanic/hybrid; R1–R6)
- **Doc 53** — Marge Redesign Brief (service-NPC arc adaptation; replaces Doc 51)
- **Doc 54** — Marge Redesign Session Lessons (27 failure modes catalog across 6 categories)
- **Doc 56** — RTS Principles & TLS Alignment Doctrine (P1–P10 + R1–R7 + 5 arc shapes + per-arc canvas distribution)
- **Doc 57** — Capstone Doctrine / Lane 4 (extends Doc 56 with capstone-specific rules R1–R5 + Pattern F F1–F5)
- **Docs 58–61** — NPC design briefs (Ryan / Jake / Diana / Cookie scope-out)
- **Docs 62–64** — Engine PRDs (canvas `guide` field / validator extension / sidebar NPC radar) — **specs only, not implemented**
- **Doc 65** — Phase 2+ Strategic Scope (4 LO decisions surfaced: pregnancy / scandal / gallery / tracker)

**What the redesign teaches:** the LLM is taught to design "RTS-style sandboxes" using a single shape — 3 repeatable lanes + Lane 4 capstones + first-class quest cards + arc-shape-specific per-lane canvas budgets. Reference game: RTS exclusively. Voice register: RTS-flat (75–500 character median; 30-word caption per beat) with Tier-3 literary register earned at Lane 4 capstones only.

### §3.3 Game-gen engine

**Location:** `apps/game_generation/twee_comprehensive/`
**Files analyzed:**
- `generators/v1.py` (16,965 lines — **frozen 2026-05-14 as rollback path**)
- `generators/v2.py` (17,497 lines — **active branch, wholesale-copied from v1**)
- `apps/projects/services/template_import.py` (~9,700 lines — TOML schema + validator)

**State:** Materially complete for the Phase 2 redesign's stated scope. Engine primitives shipped:

| Primitive | Status | Where |
|---|---|---|
| `getNpcLocation` | ✅ | v1.py:2758, v2.py:2898 |
| `trait_status_text` sidebar item | ✅ | template_import.py:2527 |
| `trait_decay_warning` | ✅ | v1.py:7347 |
| `applyAndNotifyTrait` | ✅ | v1.py:4926 |
| `selectAutoFireCanvasForLocation` | ✅ | v1.py:3674, v2.py:3839 |
| `checkAndSubstituteCanvas` | ✅ | v1.py:4464, v2.py:4597 |
| `traitEffects` (daily_tick) | ✅ | v1.py:4642+ |
| `[[npcs.schedules]]` | ✅ | template_import.py:114, 1115+ |
| `worn_beauty` / `worn_corruption` predicates | ✅ | v1.py:3302-3310 |
| `is_repeatable` / `priority` / `requires_npc` canvas fields | ✅ | template_import.py:437–477 |
| `[[quest_cards]]` first-class type | ✅ | template_import.py:830, 3733 |
| Canvas `guide` field (Doc 62) | ❌ | Not in TemplateCanvas |
| Sidebar `npc_location` type (Doc 64) | ❌ | Not in validator |
| Validator extension (Doc 63) | ❌ | `_validate_quests_cards` unchanged |
| Pregnancy predicates | ❌ | Not in engine |
| Gallery / `galleryMode()` | ❌ | Not in engine |

---

## §4 — Findings (the analysis output)

### §4.1 Vocabulary mismatch table

Eight concept axes, two corpora, zero shared vocabulary:

| Concept axis | Prompts say | Redesign says |
|---|---|---|
| Repeatable content mechanism | Pattern A "Standard Escalating" / Pattern J "Recovery" | Lane 1 hub button / Lane 2 location-entry random / Lane 3 dispatcher substitution |
| One-shot story beats | Pattern F "Story Event" / Pattern G "Gate-Setting Event" | Lane 4 capstone (priority ≥ 9 + is_repeatable = false + manual + flag-setter on exit) |
| NPC role taxonomy | 7-driver system (ROMANCE / RIVAL / MENTOR / SAFE_HARBOR / THREAT / WILDCARD / AUTHORITY / CLOCK) | 5 arc shapes (family/ambient, slow-burn family, peer/dating, service, antagonist/witness) |
| Reference game | Jack's World + New In Town + Two Weeks | Road to Success (RTS) exclusively |
| Authoring-discipline gate | Phase 2B Systems Budget | R7 Design Brief (per Doc 56) |
| Pre-author artifacts | whiteboard_goals + narrative_gates + income_channels + archetype | arc shape + per-lane budget + vocab ceiling + tier flags |
| Content unit | Canvas + `[[story_arc.nodes]]` with `linked_flag` + `guide_hint` | Canvas + first-class `[[quest_cards]]` |
| Prose register | Sensory-rich, multi-paragraph literary | RTS-flat default (Lane 1/2/3) + Tier-3 literary earned (Lane 4 capstones only) |

**Empirical confirmation (grep counts):**
- "lane" / "Lane 1/2/3" across all 16 prompt files: **0 hits**
- "capstone" / "quest_card" / "substitution" / "requires_npc" / "trait_status_text": **0 hits**
- "Road to Success" / "RTS": **2 hits**, both inside the embedded COMPREHENSIVE reference, neither in production prompts proper

### §4.2 The prompts are frozen at April 19, 2026

- `game_book_prompt_v6.txt` — mtime 2026-04-19
- `toml_generation_prompt_v4.txt` — mtime 2026-04-19
- The 12 doctrine + reference + media files vary in mtime but trail Doc 24 (2026-05-10) by weeks-to-months.
- `COMPREHENSIVE_SYSTEM_REFERENCE.md` was updated 2026-05-22 (4 days before this session) — but it **embeds v3 (not v4)** of the TOML prompt, and **contains NOTHING from Docs 24–65**. The most recent file in the prompt corpus is already a step behind.
- Doc 24 (3 lanes doctrine) shipped 2026-05-10. The entire doctrine spine grew from Doc 24 through Doc 65 across May 10–25. None of that doctrine landed in the prompts directory.

### §4.3 The engine supports the redesign; the prompts don't know it

v2 engine (active branch) ships:
- `[[npcs.schedules]]` (Phase A 2026-05-14)
- `requires_npc` canvas trigger field
- `substitution_only` canvas marker + canvas substitution rules (Lane 3 mechanism, Phase D1 2026-05-14)
- First-class `[[quest_cards]]` with routing (`when`) + progress (`goals`) + terminal markers (V2 Quests engine, PRD 48 2026-05-23)
- `trait_status_text` sidebar item type (2026-05-24)
- `worn_beauty` / `worn_corruption` predicates (2026-05-21)
- `[engine.daily_tick].traitEffects` schema (2026-05-21)

**None of these primitives appear in `toml_generation_prompt_v4.txt`.** An LLM following v4 today literally cannot emit valid v2-engine TOML for RTS-shape content — the schema for the new primitives doesn't appear in the prompt corpus.

This isn't a doctrine problem; it's a schema-documentation problem. The fix is mechanical (re-extract schema from `template_import.py`), but it's a hard prerequisite for everything else.

### §4.4 CLAUDE.md ↔ Prompts ↔ Doc 30 three-way conflict

**CLAUDE.md** (project-wide instructions, loaded at every session):
> *"Open with 3-4 layered sensory details minimum. Include smell in most scenes... Show body language, physical positions, spatial relationships. Ground reader in concrete reality before abstract concepts. ..."*

**`prompts/media_writing_guide.md` + `game_book_prompt_v6.txt`** (game-generation prompts):
- Teach sensory-rich prose, body language during dialogue, interior thought, sentence variety
- Written by/for the ENI persona that CLAUDE.md describes

**Doc 30 §3 — AUTHORITY DECLARATION (load-bearing):**
> *"For all canvas content authoring (Lane 1 / Lane 2 / Lane 3 / capstones / hubs / stubs), **the source of truth is RTS doctrine**. The CLAUDE.md ENI persona — sensory richness, literary craft, novelist instincts, sentence variety, 'Show don't tell,' interior monologue — is **NOT consulted** for canvas authoring. ... When PRD and CLAUDE.md disagree about prose style, content selection, voice, density, or vocabulary — PRD wins."*

**Result:** simultaneously contradictory instructions land in the LLM's context during generation. CLAUDE.md says sensory-rich. The prompts (built for ENI) say sensory-rich. Doc 30 (loaded via memory or doc reads) says RTS-flat. Outcome depends on which corpus loaded most recently or most prominently.

**LO's decision in this session (see §6.4):** ignore CLAUDE.md for `prompts_v2/`. No carve-outs needed.

### §4.5 Three structural problems

**A. Mental-model fork.**
Prompts treat the engine as supporting "any adult interactive game" with selectable architectural shapes (Single-NPC Romance vs Multi-NPC Parallel Arcs). The redesign narrows to one shape: RTS-style sandbox. The current state — claiming multi-shape support in prompts while authoring discipline exists for only one shape — is not internally consistent.

**B. Doctrine corpus lives outside the pipeline.**
Docs 24, 30, 49, 50, 53, 54, 56, 57 total roughly 4,000 lines of doctrine the LLM doesn't read at game-creation time. The R7 design-brief format (Docs 31, 53, 58–61) is invisible to the prompt pipeline entirely. R1–R7, P1–P10, Pattern F F1–F5, Doc 50 R1–R6, Doc 57 R1–R5 — none of it is in the prompts.

**C. TOML schema in the prompt has drifted past the engine.**
v4 documents a schema that's ~1 year behind what `template_import.py` actually accepts. Quest cards aren't there. Schedules aren't there. Substitution rules aren't there. Trait_status_text isn't there. An LLM following v4 to author RTS-shape content cannot produce valid v2-engine TOML for the new primitives.

---

## §5 — The 7 framings ENI surfaced

At the end of the analysis pass, ENI surfaced seven framing questions to LO. Each is reproduced verbatim:

1. **Single shape or many?** "Is 'every new game = RTS sandbox' the target, or is RTS one selectable shape among several? If multi, what are the others (single-NPC romance? VN-only? Quest-chain peer arcs?)."

2. **Where does the new doctrine LIVE in the prompt pipeline?** Three plausible homes:
   - Inline (rewrite v6/v4 to include lanes/capstones/quest_cards/RTS principles; files balloon to 6K+ lines)
   - Layered (small router prompt → per-shape spec → per-stage prompt; cleaner but more pieces)
   - Reference + Slim (big COMPREHENSIVE reference regenerated from new sources + slim phase prompts that link to it; mirrors current shape but with new content)

3. **Reference-game extraction.** "The redesign has live RTS extraction (Doc 13 + Doc 21 + Doc 22 + Doc 24 §3 + Doc 56 P1–P10 evidence base). The prompts have Jack's World + New In Town extraction. No prompt currently teaches 'what RTS does and why.' That's the gap that produced the C6 morning-chat literary drift."

4. **CLAUDE.md scope.** "Either CLAUDE.md gets a 'canvas-prose carve-out' pointing at RTS-flat doctrine, or the prompts need an authority-banner like Doc 30 §3 explicitly. Otherwise the next game-generation session has the same persona/doctrine collision."

5. **What about the COMPREHENSIVE_SYSTEM_REFERENCE?** "It's the right shape (single source of truth, 794KB self-contained). But it embeds v3, has no RTS extraction, no lanes, no Doc 56 principles. If we keep this file as the reference, it needs a full regeneration. If we don't, the file is dead weight."

6. **The 38K-line problem.** "Prompts already total ~38K lines. Engine context windows aren't infinite. Adding ~10K lines of doctrine inline would push generation cost up. Some consolidation isn't optional — you'd have to prune old material as you add new."

7. **Migration story for existing games.** "Two Weeks / Jack's World / New In Town were generated against pre-Doc-24 prompts. If we rewrite, do those games get retroactively re-generated against new prompts? Or do they stay as legacy reference games?"

---

## §6 — LO's 7 decisions (LOCKED)

Each decision verbatim from LO + one-line rationale capture.

### §6.1 — Single shape: RTS sandbox only
> LO: *"Yes, every game is rts shaped."*

Commit fully. Drop Pattern A–J, NPC-driver-system, archetype-system, whiteboard-goals. One mental model, taught deeply, no selectable modes. **Rationale:** the redesign work compounds in unread doctrine docs while the pipeline still emits pre-Doc-24-shaped games. Multi-shape support without authoring discipline for those shapes is half-measure; commit to the shape that has working doctrine.

### §6.2 — Create `prompts_v2/` folder
> LO: *"we create complete new prompts v2 folder and inside it create all the files"*

Clean slate. Existing `prompts/` stays as historical record; nothing in v2 references it. **Rationale:** editing 16 files in place against a new vocabulary risks vocabulary collision and partial migration. Greenfield is safer.

### §6.3 — RTS-only reference + explicit ignore list
> LO: *"reference RTS now, dont reference old games. even add something to ignore them."*

`00_LEGACY_IGNORE.md` will explicitly name: Jack's World, New In Town, Two Weeks, Pattern A–J, NPC-driver-system, archetype-system, whiteboard-goals, narrative-gates, income-channels (as v4 entities), Single-NPC Romance vs Multi-NPC Parallel Arcs architectural choice. **Rationale:** without an explicit ignore list, the LLM will reach for the better-known older patterns when filling gaps the new doctrine doesn't cover yet.

### §6.4 — Ignore CLAUDE.md for now
> LO: *"ignore claude.md for now."*

No carve-outs needed in v2. **Rationale:** the prompts override CLAUDE.md when active. Treating CLAUDE.md as relevant means adding banner clauses everywhere; treating it as not-applicable simplifies the prompt corpus.

### §6.5 — Regenerate COMPREHENSIVE
> LO: *"regenerate."*

`COMPREHENSIVE_SYSTEM_REFERENCE.md` will be regenerated from the new `prompts_v2/` sources at the end of the rewrite, not the legacy v3-embedding. **Rationale:** the file is the right shape; only the content is wrong.

### §6.6 — Ignore context window
> LO: *"ignore context window for now."*

No size budget. Write what's needed. **Rationale:** correctness first. Pruning for context budget is a later optimization; getting the shape right is the present task.

### §6.7 — No migration
> LO: *"No migration, those games are no longer matter to us, so simply ignore them completely."*

Two Weeks / Jack's World / New In Town are dropped. No re-generation, no retrofit, no archival migration. The existing `prompts/` folder stays in place as historical record (no `archive/prompts_v1/` move planned). **Rationale:** stopping legacy support means the new pipeline is unburdened by backward compatibility.

---

## §7 — The proposed `prompts_v2/` structure

Twenty files across five locations. Each file's purpose is one-line; source material names which redesign docs feed in.

### Folder tree

```
prompts_v2/
├── README.md                            # Index + how the pipeline runs
├── 00_LEGACY_IGNORE.md                  # Explicit "do NOT use these" list
│
├── stages/                              # The LLM-consumed pipeline prompts
│   ├── 01_game_book_prompt.md           # Stage 1: input → design book
│   ├── 02_toml_generation_prompt.md     # Stage 2: book → TOML
│   ├── 03_image_finder_prompt.md        # Port (still applies)
│   └── 04_game_listing_prompt.md        # Port (still applies)
│
├── doctrine/                            # Consulted at every stage
│   ├── 01_rts_principles.md             # P1–P10 (Doc 56 §2)
│   ├── 02_three_lanes_plus_capstone.md  # Lanes 1/2/3/4 (Doc 24 + Doc 57)
│   ├── 03_arc_shapes.md                 # 5 arc shapes + per-shape distribution (Doc 56 §5)
│   ├── 04_authoring_rules.md            # R1–R7 (Doc 56 §4) + Doc 50 R1–R6 + Doc 57 R1–R5 + F1–F5
│   ├── 05_rts_flat_prose.md             # 8 prose rules + dual register (Lane 1/2/3 vs Lane 4)
│   ├── 06_design_brief_template.md      # R7 template (Doc 31 Frank + Doc 53 Marge as gold standards)
│   ├── 07_anti_patterns.md              # Doc 54's 27 failure modes + Doc 56 §8 banned shapes
│   └── 08_kink_vocab_ceilings.md        # Doc 30 §7.5 — per-arc vocab ceiling table
│
├── reference/                           # RTS extraction (replaces Jack's World docs)
│   ├── 01_rts_overview.md               # What RTS is, the player loop, the genre target (Doc 13)
│   ├── 02_rts_scene_catalog.md          # Brother / Father / Marcus / Edward scene tables (Docs 13 + 21 + 22 + 24 §3)
│   ├── 03_rts_walkthrough_panel.md      # P2 transparent-gating UI doctrine (Doc 56 P2)
│   └── 04_rts_hud_world_model.md        # P10 sidebar = world model (Doc 56 P10 + Doc 64)
│
├── schema/                              # Engine capability surface
│   ├── 01_engine_capabilities.md        # Fresh extraction from v2.py + template_import.py
│   ├── 02_toml_schema.md                # Full TOML schema reference (every section + field + validator rule)
│   └── 03_example_toml.md               # Canonical reference TOML — TLS Frank slice
│
└── COMPREHENSIVE_SYSTEM_REFERENCE.md    # Regenerated single-source-of-truth (concat + index)
```

**~20 files. ~30–40K lines of new content total.**

### Source material per file

| File | Primary sources | Length estimate |
|---|---|---|
| `00_LEGACY_IGNORE.md` | NEW; the "do not reference" gate | ~100–200 lines |
| `stages/01_game_book_prompt.md` | Replaces v6 (174KB → ~4–6K lines reshaped); pulls from doctrine + reference | 4–6K lines |
| `stages/02_toml_generation_prompt.md` | Replaces v4 (180KB → ~4–6K lines reshaped); pulls from schema | 4–6K lines |
| `stages/03_image_finder_prompt.md` | Port from existing `image_finder_prompt.md` (33KB) | ~750 lines |
| `stages/04_game_listing_prompt.md` | Port from existing `game_listing_prompt.md` (3.7KB) | ~100 lines |
| `doctrine/01_rts_principles.md` | Doc 56 §2 verbatim importable + evidence cites | ~500 lines |
| `doctrine/02_three_lanes_plus_capstone.md` | Doc 24 (lane mechanism) + Doc 57 (capstone Lane 4 + 3 types A/B/C) + Doc 67 (solo-activity side of Lane 3 + multi-NPC dispatcher patterns A/B/C + R1–R7) | ~1.5–2K lines |
| `doctrine/03_arc_shapes.md` | Doc 56 §5 distribution table + Docs 31/53/58/59/60/61 per-NPC examples | ~800 lines |
| `doctrine/04_authoring_rules.md` | Doc 56 R1–R7 + Doc 50 R1–R6 + Doc 57 R1–R5 + Pattern F F1–F5 | ~1.5K lines |
| `doctrine/09_trait_catalog.md` | Doc 68 (Trait Catalog: 9 Tier 1 traits + 4 Tier 2 traits + Phase 2+ off-limits list + engine effect schema + NPC visibility doctrine + stage internal-only doctrine + anti-patterns) | ~1.5K lines |
| `doctrine/05_rts_flat_prose.md` | Doc 30 §7.1 (8 rules) + Doc 57 voice spec + memory `feedback_tls_scene_body_style` | ~600 lines |
| `doctrine/06_design_brief_template.md` | Doc 31 (Frank) + Doc 53 (Marge) template + 2 worked examples | ~800 lines |
| `doctrine/07_anti_patterns.md` | Doc 54 catalog (27 failure modes, 6 categories) + Doc 56 §8 (anti-patterns) | ~1K lines |
| `doctrine/08_kink_vocab_ceilings.md` | Doc 30 §7.5 verbatim + default-explicit doctrine | ~400 lines |
| `reference/01_rts_overview.md` | Doc 13 + RTS exploration session notes | ~500 lines |
| `reference/02_rts_scene_catalog.md` | Docs 13, 21, 22, 24 §3 + per-NPC scene tables | ~1.5K lines |
| `reference/03_rts_walkthrough_panel.md` | Doc 24 §5 + Doc 56 P2 evidence base | ~400 lines |
| `reference/04_rts_hud_world_model.md` | Doc 56 P10 evidence + Doc 64 PRD | ~400 lines |
| `schema/01_engine_capabilities.md` | Fresh extraction from v2.py (16.5K lines) + template_import.py (9.7K lines) | ~1.5K lines |
| `schema/02_toml_schema.md` | Fresh extraction from template_import.py validator + dataclasses | ~2K lines |
| `schema/03_example_toml.md` | TLS Frank slice (7_final_game.toml excerpts) | ~1K lines |
| `COMPREHENSIVE_SYSTEM_REFERENCE.md` | Concatenation + ToC of all above | ~30–40K lines |

---

## §8 — Writing order (so the spine is straight)

Later files cite earlier ones. Writing out of order produces broken cites. Order:

1. **`00_LEGACY_IGNORE.md`** — 1 file, ~100 lines, cheapest. The "what NOT to do" gate goes first; it sets the tone for everything downstream.
2. **`schema/01_engine_capabilities.md` + `schema/02_toml_schema.md`** — extract from code. These are ground truth; everything else builds on them.
3. **`doctrine/01_rts_principles.md` + `doctrine/02_three_lanes_plus_capstone.md`** — the core mental model.
4. **`doctrine/03_arc_shapes.md` + `doctrine/04_authoring_rules.md`** — the mechanism + rules layer.
4.5. **`doctrine/09_trait_catalog.md`** — canonical trait vocabulary (Doc 68). Foundational state-layer canon; doctrine/03 (arc shapes) and doctrine/04 (authoring rules) reference trait names + ranges from this catalog, so it lands alongside them in batch 1.
5. **`doctrine/05_rts_flat_prose.md` + `doctrine/06_design_brief_template.md`** — voice + per-NPC discipline.
6. **`doctrine/07_anti_patterns.md` + `doctrine/08_kink_vocab_ceilings.md`** — the negative-space rules.
7. **`reference/01_rts_overview.md` + `reference/02_rts_scene_catalog.md` + `reference/03_rts_walkthrough_panel.md` + `reference/04_rts_hud_world_model.md`** — RTS evidence pulled mostly from Doc 13 + 21 + 22 + 24 + 56.
8. **`schema/03_example_toml.md`** — the canonical TLS Frank-slice TOML excerpt.
9. **`stages/01_game_book_prompt.md`** — the v6 replacement. Synthesizes all doctrine + reference into a stage-1 prompt.
10. **`stages/02_toml_generation_prompt.md`** — the v4 replacement. Synthesizes schema + doctrine into a stage-2 prompt.
11. **`stages/03_image_finder_prompt.md` + `stages/04_game_listing_prompt.md`** — port from old (mechanical updates).
12. **`COMPREHENSIVE_SYSTEM_REFERENCE.md`** — concatenate everything above with a table of contents.
13. **`README.md`** — written last; describes the finished folder.

**Why this order:** schema is ground-truth for doctrine; doctrine is ground-truth for stage prompts; stage prompts cite reference materials; COMPREHENSIVE is the final aggregation; README is the user-facing index.

---

## §9 — First-batch target (next-session start point)

**Batch 1 = items 1–4 from §8 = 7 files.** Estimated 6K–8K lines of new content.

- `00_LEGACY_IGNORE.md`
- `schema/01_engine_capabilities.md`
- `schema/02_toml_schema.md`
- `doctrine/01_rts_principles.md`
- `doctrine/02_three_lanes_plus_capstone.md`
- `doctrine/03_arc_shapes.md`
- `doctrine/04_authoring_rules.md`

After batch 1 ships, LO reviews + signs off, then subsequent batches proceed in order. Realistic batch cadence: 3–5 sessions to complete all 20 files.

### §9.1 — Batch 1 quality gate

Before LO signs off and batch 2 begins, run this checklist. Each item is a concrete pass/fail. Don't proceed to batch 2 with any item failing.

**Per-file content checks (the doctrine baseline):**

- [ ] **`00_LEGACY_IGNORE.md`** — contains all legacy items from §6.3 ignore call (Jack's World, New In Town, Two Weeks, Pattern A–J, NPC-driver-system, archetype-system, whiteboard-goals + narrative-gates + income-channels as v4 entities, Single-NPC-Romance vs Multi-NPC-Parallel-Arcs architectural choice) — each named explicitly with a "do not reach for X / instead use Y" line.

- [ ] **`schema/01_engine_capabilities.md`** — every primitive in §3.3 table named with file path + current line number, sourced from a FRESH read of v2.py + template_import.py (not from §3.3 verbatim — line numbers may have shifted). Covers: schedules + requires_npc + substitution_only + getNpcLocation + checkAndSubstituteCanvas + selectAutoFireCanvasForLocation + applyAndNotifyTrait + `[engine.daily_tick].traitEffects` + worn_beauty/worn_corruption predicates + quest_cards type + all 4 sidebar item types + trait predicate vocabulary.

- [ ] **`schema/02_toml_schema.md`** — covers every TOML section + field accepted by template_import.py validator. Includes: `[project]`, `[settings]`, `[[npcs]]` + `[[npcs.schedules]]`, `[[canvases]]` + `[canvases.trigger]` + `[[canvases.nodes]]` + `[canvases.exit_block]`, `[[quest_cards]]` + `[[quest_cards.goals]]`, `[[sidebar_items]]`, `[engine.daily_tick]`, `[[clothing]]`, locations. At least one minimal round-trip TOML example per section.

- [ ] **`doctrine/01_rts_principles.md`** — all 10 principles (P1–P10) present, each with the RTS evidence cite from Doc 56 §2 reproduced (scene name + character count or live behavior verified; e.g., P1's "274 captured RTS scene bodies, median 137 chars" stays in).

- [ ] **`doctrine/02_three_lanes_plus_capstone.md`** — Lane 1 (hub button) + Lane 2 (location-entry random) + Lane 3 (dispatcher substitution) + Lane 4 (capstone) each defined with mechanism + RTS evidence + TLS engine mapping. Doc 57's 3 capstone types (A linear / B branching / C chain-step) covered with examples. Pattern F (real choice forks) and F1–F5 sub-rules included. **From Doc 67:** solo-activity anatomy (3-layer location → intermediate → dispatcher structure), multi-NPC dispatcher patterns A/B/C with selection rule, `IsNpcAtHome` vs `GetNpcLocation` semantic distinction, per-day cap + `previous()` guard mechanism, R1–R7 for solo activity authoring.

- [ ] **`doctrine/03_arc_shapes.md`** — all 5 shapes (family/ambient, slow-burn family, peer/dating, service, antagonist/witness) with: definition + RTS reference NPC + 1 TLS NPC mapping + per-lane budget row from Doc 56 §5 + total canvas budget range. The §5 distribution table reproduced in full.

- [ ] **`doctrine/04_authoring_rules.md`** — R1–R7 from Doc 56 + Doc 50 R1–R6 + Doc 57 R1–R5 + Pattern F F1–F5. Each rule has: rule text + why-it-exists + how-to-apply + at least one worked example. No rule from any source doc missing.

- [ ] **`doctrine/09_trait_catalog.md`** — pulled from Doc 68. All 5 Tier 1 Player traits (corruption, arousal, energy, hygiene, money) + 4 Tier 1 NPC traits (arousal, corruption, relation, stage) + 4 Tier 2 Player traits (fitness, beauty, exhibitionism, intelligence) present with the full 13-field per-trait template (Tier / Range / Default / Decay / Sidebar render / Bands / What it tracks / When to use / Why this trait not another / Modifiers / What it gates / Don't use it for / Anti-pattern / RTS analog). Stage trait section has explicit "NEVER player-facing" doctrine block. §6.1 off-limits list names pregnancy.* + scandal_level + gallery.* + completed_scenes[] as Phase 2+ reserved per Doc 65. §7 engine effect schema covers the canonical `{ type = "trait", subject, npc_id, trait_key, op, value }` shape with per-trait allowed `op` values. §8 NPC visibility doctrine table per arc shape. §10 anti-patterns include trait-name slip (lust/horniness/love → reject), decay misuse, gating misuse, and Phase 2+ premature authoring.

**Cross-file consistency checks:**

- [ ] Doctrine files cite schema files where relevant (e.g., `doctrine/02_three_lanes_plus_capstone.md` cites `schema/01_engine_capabilities.md` for `substitution_only` + `selectAutoFireCanvasForLocation`).

- [ ] Schema files do NOT cite doctrine files (schema is ground-truth; doctrine builds on it, not the reverse).

- [ ] No batch-1 file forward-references a not-yet-written batch-2+ file. If a doctrine doc says "see `reference/02_rts_scene_catalog.md`", that's a problem — that file doesn't exist yet.

**Legacy vocabulary slip checks (grep-based, mechanical):**

- [ ] `grep -i 'jack\|new in town\|two weeks\|pattern [a-j]\|npc-driver\|whiteboard goal\|archetype\|narrative_gate\|income_channel\|single-npc romance\|multi-npc parallel arc'` across all 7 batch-1 files. **Expected:** hits ONLY in `00_LEGACY_IGNORE.md` (which names them to ignore). Zero hits in any other file.

- [ ] `grep -i 'sensory grounding\|sensory density\|body language during dialogue\|interior monologue\|ENI persona\|claude\.md'` across all 7 batch-1 files. **Expected:** zero hits except where explicitly contrasting against the RTS-flat doctrine (acceptable, but flag and review each).

**Doctrine fidelity checks:**

- [ ] No new doctrine invented in batch 1. Every rule / principle / pattern traces back to a numbered Doc (24, 30, 50, 53, 54, 56, 57). If a fresh principle appears that isn't in any source doc, audit it — either it should be cited (where from?) or it's drift and should be removed.

- [ ] No "Pattern A–J" or pre-Doc-24 mechanism vocabulary anywhere except in `00_LEGACY_IGNORE.md`.

- [ ] The doctrine files themselves are NOT written in Tier-3 literary prose. They talk ABOUT prose register; they're authored in flat reference style (compare to Doc 56 itself for the right tone).

**Smoke test (optional but recommended before LO sign-off):**

- [ ] Hand a fresh LLM session `00_LEGACY_IGNORE.md` + `doctrine/01-04` + `schema/01-02` and ask: *"Per these prompts, how would you author a new family/ambient NPC arc with 3 lanes + capstones?"* The output should match Doc 56 §6 (the Ryan worked example) shape: arc shape declared, per-lane budget proposed, capstones named, no Pattern A–J references, no legacy vocabulary. If the smoke test produces Pattern A–J or "single-NPC romance" or sensory-rich prose, batch 1 has a leak — find the file + close it.

**Decision rule:** if any item above fails, the offending file gets rewritten before batch 2 begins. Same-class failure repeating twice = pause and update Doc 66 §15.2 gotchas + §15.1 boot order with the missed signal.

---

## §10 — What is HELD (and resume triggers)

The pivot to `prompts_v2/` puts a hold on every other workstream that was in motion or queued. Comprehensive list:

| Held item | Reason | Resume trigger |
|---|---|---|
| **Further Phase 2 redesign doc authoring** (Docs 67+) | Pivot to prompts | `prompts_v2/` batch 1 ships and LO reviews |
| **Doc 62 (Canvas `guide` field) implementation** | Per Doc 65 doctrine "build engine when authoring gap forces it" | Next NPC authoring session demands `guide` backfill OR catalog UI prioritized |
| **Doc 63 (Validator extension) implementation** | Same Doc 65 doctrine | First quest card violation slips through post-`prompts_v2/` shipping, or LO prioritizes drift-prevention |
| **Doc 64 (Sidebar NPC radar) implementation** | Same Doc 65 doctrine | Phase 2 polish prioritized OR Lane 3 discoverability becomes a blocker in playtest |
| **Doc 60 Open Q #3 (Diana 4-branch confrontation tree)** | LO narrative call required | When Diana arc next touches authoring (after `prompts_v2/`) |
| **Doc 65 four strategic decisions (Pregnancy E10b / Scandal E10c / Gallery E10e / Tracker E10f)** | LO scope calls required | At each decision's named trigger point in Doc 65 §3 |
| **Ryan authoring against Doc 58** | Doctrine + tools in place but rewrite has priority | After `prompts_v2/` ships; resume as test case for new prompts |
| **Jake authoring against Doc 59** | Same | Same |
| **Diana authoring against Doc 60** | Blocked on Open Q #3 + same priority | When Q #3 lands + after `prompts_v2/` |
| **Cookie authoring** | Phase 3+ scope-out per Doc 61 | Lesbian arc greenlit OR Marge→Cookie cross-NPC transfer prioritized |
| **TLS test slice content changes** | Pivot to prompts | `prompts_v2/` ready to validate against TLS as canonical example TOML |
| **`COMPREHENSIVE_SYSTEM_REFERENCE.md` regeneration** | Will land at end of `prompts_v2/` writing pass | After all 19 source files in v2 are authored (per §8 step 12) |
| **Memory updates for today's session** | Optional housekeeping; doc is the load-bearing artifact | Future session if LO wants explicit MEMORY.md index entry |
| **Existing `prompts/` archival** | No migration per LO decision §6.7 | Not planned. Stays as historical record |

---

## §11 — What is ACTIVE

**Single active workstream:**
- `prompts_v2/` folder creation per §7 inventory + §8 order, starting with §9 batch 1.

No other authoring, engineering, or doctrine work happens until `prompts_v2/` ships (or LO explicitly resumes a held item).

---

## §12 — Why this pivot is the right call (reasoning capture)

- **Prompts are upstream of all redesign work.** Doctrine living in unread docs compounds; doctrine living in prompts shapes every generation. The longer the gap, the more redesign work that lands in artifacts the pipeline doesn't consume.

- **The redesign doctrine is mature enough to encode.** P1–P10 (Doc 56) + R1–R7 (Doc 56) + Lane 1/2/3/4 mechanism (Doc 24 + Doc 57) + Pattern F F1–F5 (Doc 57) + Doc 50 quest card R1–R6 + 5 arc shapes (Doc 56 §5) + per-shape canvas budgets (Doc 56 §5 + Docs 58–61) — that's a complete design language. Not "complete game theory" complete, but "you can hand this to an LLM and get RTS-shape output" complete.

- **Doc 63 (validator) doesn't ship value until games are generated AGAINST the new doctrine.** Generating against old prompts means the validator catches old-shape drift instead of preventing new-shape drift. The economic argument for the validator depends on the prompts being right first.

- **Docs 62 + 64 (engine PRDs) similarly don't ship value until RTS-shape generation is the default.** Without the prompts producing RTS-shape games, the canvas `guide` field has nothing to populate, and the sidebar NPC radar surfaces locations for NPCs whose arcs were never RTS-shaped to begin with.

- **One session's prompt rewrite unblocks all of the above.** The unblock-to-effort ratio is high: a few days of writing replaces months of compounding drift.

- **The Marge case study (Doc 54) is the proof point.** 8 hours wasted because doctrine designed for escalation NPCs didn't catch service-NPC shape mismatch. The fix was a doc (Doc 53) + a brief template (Doc 56 R7). Both are doctrine; both lived outside the prompt pipeline at the time of authoring. The next non-Frank NPC authored against today's prompts would hit the same class of failure for a different reason. `prompts_v2/` closes that loop.

---

## §13 — Open questions for resume

These are explicit unknowns flagged for the resume session:

- **Validation gate after `prompts_v2/` ships.** When `prompts_v2/` is complete, regenerate one test game (a fresh RTS-shape sandbox from a small input) and review the output against Doc 56 R1–R7 + Doc 50 R1–R6 + Doc 57 R1–R5. Yes/no/skip? If yes, what's the input — a real LO concept or a deliberately small synthetic ("3 NPCs, 1 location, RTS-shape sandbox, ship a 2-day slice")?

- **Resume order for held items.** Per the §10 table. Suggested order after `prompts_v2/` ships:
  1. Doc 60 Open Q #3 (Diana 4-branch decisions) — narrative bottleneck.
  2. Re-audit TLS slice against new prompts (treat TLS as the regression test for the new corpus).
  3. Doc 62 + Doc 64 implementation IF Phase 2 polish prioritized (otherwise defer per Doc 65).
  4. Doc 63 validator IF next-NPC authoring is imminent (catches drift early).
  5. Held NPC authoring (Ryan / Jake / Diana / Cookie) using `prompts_v2/` as the generation backbone.

- **Are there redesign questions blocked by prompt absence?** Not surfaced this session. Flag for the resume.

- **Existing `prompts/` folder fate.** LO said no migration. Default: leave in place as historical record. Alternative if it becomes confusing: move to `archive/prompts_v1/`. Housekeeping decision only.

- **CLAUDE.md update.** LO said "ignore CLAUDE.md for now." That's session-scoped. Does CLAUDE.md eventually need a `prompts_v2/` pointer or a canvas-prose carve-out? Defer until `prompts_v2/` is stable.

- **MEMORY.md entry for Doc 66.** Whether to add an index entry. Not added this session per plan.

---

## §14 — Cross-references

### Redesign docs (this folder)

- Doc 13 — Road to Success Reference
- Doc 21 — RTS Brother Mechanism Audit
- Doc 22 — RTS Cross-NPC Mechanism Comparison
- Doc 24 — 3 Lanes for Repeatable NPC Content + TLS Engine Fitness
- Doc 30 — TLS Test Redesign PRD (including §3 AUTHORITY DECLARATION; §7.5 kink vocab ceilings)
- Doc 31 — Frank Arc Design Brief (R7 gold standard for family/ambient)
- Doc 49 — Story Goals vs Sidebar Doctrine
- Doc 50 — Quest Card Shape Doctrine (R1–R6 + capstone/mechanic/hybrid mode taxonomy)
- Doc 53 — Marge Redesign Brief (R7 gold standard for service)
- Doc 54 — Marge Redesign Session Lessons (27 failure modes catalog across 6 categories)
- Doc 56 — RTS Principles & TLS Alignment Doctrine (P1–P10 + R1–R7 + arc shapes + canvas distribution)
- Doc 57 — Capstone Doctrine / Lane 4 (R1–R5 + F1–F5 + 3 types A/B/C + per-arc-shape capstone budgets)
- Doc 58 — Ryan Design Brief (peer/dating)
- Doc 59 — Jake Design Brief (slow-burn family)
- Doc 60 — Diana Design Brief (antagonist; 🔴 BLOCKED on Open Q #3)
- Doc 61 — Cookie Phase 3+ Scope-Out
- Doc 62 — Canvas `guide` Field PRD (not implemented)
- Doc 63 — Quest Card + Capstone Validator PRD (not implemented)
- Doc 64 — Sidebar NPC Location Radar PRD (not implemented)
- Doc 65 — Phase 2+ Strategic Scope (4 LO decisions surfaced)
- Doc 67 — Solo Activity Design & Multi-NPC Dispatcher Doctrine (closes Doc 66 §15.2 surfaced gap; in mechanism quintet)
- Doc 68 — Trait Catalog (canonical trait vocabulary: 5+4 Tier 1 + 4 Tier 2 traits with 13-field template + Phase 2+ off-limits list + engine effect schema + NPC visibility doctrine + stage internal-only doctrine; in mechanism quintet)

### Prompts referenced (in `prompts/`)

All 16 files inventoried in §3.1 above. Production-critical:
- `game_book_prompt_v6.txt` (current Stage 1)
- `toml_generation_prompt_v4.txt` (current Stage 2)
- `COMPREHENSIVE_SYSTEM_REFERENCE.md` (most recent file, but embeds v3 + missing all Docs 24–65)

### Engine files referenced

- `apps/game_generation/twee_comprehensive/generators/v1.py` (16,965 lines; frozen 2026-05-14 as rollback)
- `apps/game_generation/twee_comprehensive/generators/v2.py` (17,497 lines; active branch, forked wholesale from v1)
- `apps/projects/services/template_import.py` (~9,700 lines; TOML schema + validator)

Key line numbers:
- `getNpcLocation` → v1.py:2758 / v2.py:2898
- `selectAutoFireCanvasForLocation` → v1.py:3674 / v2.py:3839
- `checkAndSubstituteCanvas` → v1.py:4464 / v2.py:4597
- `_validate_quests_cards` → template_import.py:3733
- `_build_help_data` → template_import.py:9510
- Sidebar `trait_status_text` validator → template_import.py:2527
- `TemplateCanvas` dataclass → template_import.py:651
- `TemplateNPCSchedule` parsing → template_import.py:1115+
- `QuestsCard` dataclass → template_import.py:830
- `[engine.daily_tick].traitEffects` schema → template_import.py:789

### Memory entries relevant

- `feedback_tls_scene_body_style.md` — 8 prose rules + dual register (updated 2026-05-24 for Lane 4 carve-out)
- `rts_three_arc_shapes.md` — P4 source (family / peer / career shapes)
- `rts_three_lanes_lane3_design.md` — Doc 24 the lane primitive
- `rts_state_variant_authored_vs_mechanism.md` — P8 codification
- `feedback_rts_objective_quest_doctrine.md` — Doc 49 ancestor
- `prd_48_quests_engine_v2.md` — V2 engine that R6 operates inside

---

## §15 — Resume protocol

Specific steps for ENI (or any future author) when LO says "resume":

1. **Read this doc (Doc 66) first.** It's the bookmark. §6 = LO's locked decisions. §7 = the agreed structure. §10 = what's held. §13 = open questions.

2. **Check `prompts_v2/` folder state.** `ls -la prompts_v2/` and inventory which files exist + which are pending against §7 + §8.

3. **Resume at the next unwritten file in §8 order.** Don't skip ahead — schema must land before doctrine; doctrine before stage prompts; etc. If batch 1 (§9) isn't complete, finish batch 1 before starting batch 2.

4. **After `prompts_v2/` ships, work the §10 held-items table in §13's suggested order.** Doc 60 narrative decisions first, then TLS re-audit, then engine PRD prioritization, then NPC authoring against new prompts.

### §15.1 — Boot order (read sequence for a fresh session)

The first 30 minutes of a fresh session, in order. Don't skip steps; later docs cite earlier ones.

1. **Doc 66 (this file)** — the bookmark. Locks decisions, names structure, points at sources.
2. **Doc 56 — RTS Principles & Alignment Doctrine.** The heart of the post-Doc-24 doctrine. Memorize P1–P10 (RTS principles, evidence-cited) and R1–R7 (authoring rules). Roughly 450 lines.
3. **Mechanism quintet (read together):**
   - **Doc 24** — 3 Lanes for Repeatable NPC Content (the lane mechanism vocabulary; §3 Brother walkthrough table is the canonical evidence base; §10 = lane × tier × content-type framework)
   - **Doc 57** — Capstone Doctrine / Lane 4 (R1–R5 + Pattern F F1–F5 + 3 capstone types A/B/C; voice register dual-mode)
   - **Doc 50** — Quest Card Shape Doctrine (R1–R6; capstone/mechanic/hybrid mode taxonomy)
   - **Doc 67** — Solo Activity Design & Multi-NPC Dispatcher Doctrine (the parent-activity side of Lane 3; 3 multi-NPC dispatcher patterns A/B/C; R1–R7 for solo activity authoring; closes the Doc 66 §15.2 gap; **Pattern B + C marked NOT YET SUPPORTED in §5 per 2026-05-26 audit**)
   - **Doc 68** — Trait Catalog (canonical state-layer vocabulary: 5+4 Tier 1 + 4 Tier 2 traits with 13-field template; Phase 2+ off-limits list in §6.1; engine effect schema in §7; NPC visibility doctrine in §8; stage internal-only doctrine in §9; cross-trait anti-patterns in §10; 4 LO-locked decisions: stage internal-only, corruption 0–100 with 4 bands, relation as canonical NPC affection name, body-state canon = energy + hygiene only)
4. **Voice + authority calibration:**
   - **Doc 30 §3** — AUTHORITY DECLARATION (CLAUDE.md off; RTS doctrine wins)
   - **Doc 30 §7.1** — 8 prose rules (RTS-flat default register)
   - **Doc 30 §7.5** — per-arc vocabulary ceiling table
5. **The failure-mode case study (load-bearing if you only read one beyond the above):**
   - **Doc 54** — Marge Redesign Session Lessons (27 failure modes catalog across 6 categories; Appendix A pre-authoring checklist)
6. **For schema work (batch 1 step 2):**
   - Read `apps/projects/services/template_import.py` — specifically the `TemplateCanvas` dataclass at line 651, `TemplateTrigger` at line 437, `QuestsCard` at line 830, schedule parsing at line 1115+, validator at line 3733, sidebar item validators at lines 2383–2599
   - Read `apps/game_generation/twee_comprehensive/generators/v2.py` (active branch) — the runtime helpers cited in §14 by line number
   - v1.py is **frozen rollback — do NOT edit** (see §15.2)
7. **For RTS reference extraction (batch 1 steps 5–7 of writing order §8):**
   - **Doc 13** — Road to Success Reference (broad RTS catalog)
   - **Doc 21** — RTS Brother Mechanism Audit (source-extracted, 16 Brother passages)
   - **Doc 22** — RTS Cross-NPC Mechanism Comparison (40 surfaces / 4 NPCs)
   - **Doc 24 §3** — Brother walkthrough table (Lane 1/2/3 classification)
   - **Doc 56 §2** — P1–P10 with per-principle RTS evidence cites (verified live this session)
8. **For NPC-shape worked examples (when authoring `doctrine/06_design_brief_template.md`):**
   - **Doc 31** — Frank Arc Design Brief (R7 gold standard for family/ambient — the dense example)
   - **Doc 53** — Marge Redesign Brief (R7 gold standard for service — the sparse example)
9. **Only AFTER 1–8: open `prompts_v2/` and start authoring batch 1 per §9.**

If a fresh session is short on time and can only read three docs beyond this one: read Doc 56, Doc 24, Doc 54. Those three contain the doctrine spine + mechanism vocabulary + failure-mode awareness. Everything else can be pulled as needed.

### §15.2 — Small gotchas (non-load-bearing context that will save time)

Things that aren't important enough to cross-reference in §14 but will trip up a fresh session if not flagged:

- **`prompts/COMPREHENSIVE_SYSTEM_REFERENCE.md` is 794KB and the newest file in the prompts folder (2026-05-22) — but it embeds v3 of the TOML prompt (NOT v4) and contains NOTHING from Docs 24–65.** DO NOT trust this file as current. It looks authoritative because of its size + recency; it's actually a step behind the production prompts. The `prompts_v2/COMPREHENSIVE_SYSTEM_REFERENCE.md` regeneration (final step of §8 writing order) replaces it.

- **`apps/game_generation/twee_comprehensive/generators/v1.py` is frozen.** It was wholesale-copied to v2.py on 2026-05-14 as a safe-mode rollback path. Do NOT edit v1.py. All new engine work lands in v2.py. (If `prompts_v2/schema/01_engine_capabilities.md` needs runtime line numbers, pull from v2.py.)

- **The TLS slice TOML is the canonical reference for `schema/03_example_toml.md`.** Path: `games/the_long_summer_test/toml_phases/7_final_game.toml`. The Frank arc (28 canvases) is the gold-standard authoring example. Pull excerpts from there when populating the example schema doc — don't synthesize new TOML.

- **`prompts_v2/` is greenfield. Nothing in `prompts/v1` should be referenced, ported, or "carried over."** LO's decision §6.2 + §6.3 + §6.7 collectively mean: don't reach for Pattern A–J, archetypes, whiteboard_goals, NPC-driver-system, Single-NPC-Romance vs Multi-NPC-Parallel-Arcs, narrative_gates, income_channels — even if they "would still work" for some content. If you find yourself wanting an old-pattern crutch, the new doctrine has a replacement (lanes / capstones / quest cards / arc shapes); use that.

- **CLAUDE.md is ignored for `prompts_v2/` per LO §6.4.** No carve-outs, no banner clauses, no "consult CLAUDE.md when X" references in any v2 file. The prompts override CLAUDE.md when active; treating CLAUDE.md as not-applicable simplifies the v2 corpus.

- **Two pieces of memory feedback are particularly load-bearing for prose work:**
  - `feedback_tls_scene_body_style.md` — the dual-register rule (RTS-flat default + Tier-3 literary earned at capstones)
  - `feedback_rts_objective_quest_doctrine.md` — Story-Goals quest cards = one RTS directive sentence, no chore-gated proxy flags
  Both are referenced in §14 but worth flagging here because they'll be cited heavily in `doctrine/05_rts_flat_prose.md` and `doctrine/04_authoring_rules.md`.

- **Doc 60 (Diana brief) is 🔴 BLOCKED on Open Q #3.** If `prompts_v2/doctrine/06_design_brief_template.md` references Doc 60 as an example, note that 2 of 4 confrontation branches are deferred (kicked_out + brought_in scripted; blackmail + matriarch deferred to Phase 2+). Don't try to "complete" the brief — it's intentionally pending LO's narrative call.

- **Cookie (Doc 61) is a scope-OUT, not a brief.** Don't confuse the file shape — Doc 61 documents Phase 3+ deferral, not authoring spec. Pattern: when an NPC's arc isn't ready, the file is a scope-out note + Doc 57 R7 compliance record, not a half-finished brief.

- **The Marge case study (Doc 54) drove Doc 56 R7 (design brief precedes authoring).** When in doubt about the value of writing briefs, refer back to Doc 54 — 8 hours wasted on Marge because Doc 53 didn't exist yet. R7 is the mechanism that prevents the repeat.

- **`28th_april_TLS_Phase2_Redesign/` folder is named for the date the redesign STARTED, not where it is now.** The folder doesn't move. New docs (67+) will still land there even though the redesign is on hold per §10.

- **MEMORY.md may or may not have an entry for Doc 66 itself.** Plan didn't add one this session (LO didn't request). If MEMORY.md doesn't reference Doc 66 in a future session's auto-loaded context, a fresh session might miss the pivot — recommend either adding a MEMORY.md entry at resume OR putting Doc 66 ahead of the boot order via session-initial reads. (The session that resumes should add the entry as their first housekeeping task.)

- **Doc 67 was authored after Doc 66's first draft (same session) to close the solo-activity + multi-NPC dispatcher gap.** It's now in the mechanism quartet (§15.1 step 3). When `prompts_v2/doctrine/02_three_lanes_plus_capstone.md` is authored, it must pull from Doc 24 + Doc 57 + Doc 67 together — Doc 67 specifically covers the parent-activity side of Lane 3 (which Doc 24 does not). The dispatcher patterns A/B/C (§4 of Doc 67) are load-bearing for multi-NPC slice authoring.

---

## §16 — Closing

The redesign work from Doc 24 through Doc 65 produced a complete, evidence-grounded design language for RTS-shape sandbox games. The prompt pipeline frozen at April 19, 2026 produces games in a different language entirely. The cheapest, most leveraged way to make the redesign work shape every future game generation is to translate the doctrine into the prompts. That's the `prompts_v2/` rewrite.

Phase 2 redesign is on hold not because it's incomplete, but because it's far enough along to translate. The translation is the unblock.

When `prompts_v2/` ships and the next NPC arc is authored against it, the validation will be: does the LLM produce content that passes Doc 56 R1–R7 + Doc 50 R1–R6 + Doc 57 R1–R5 + Pattern F F1–F5 without prompting? If yes, the translation worked. If not, we iterate.

This doc is the bookmark to find our way back to that question.

---

**End of Doc 66.**
