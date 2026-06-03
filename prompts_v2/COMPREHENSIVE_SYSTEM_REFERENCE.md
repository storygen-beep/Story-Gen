# prompts_v2 — Comprehensive System Reference

**Status:** Single concatenated reference. Generated mechanically from the source files in canonical reading order. Regenerate via `scripts/regen_comprehensive_reference.py` when source files change.

**How to use:** if you want the FULL prompts_v2 corpus in one file (single-load LLM context), this is it. For day-to-day work, prefer the individual source files.

---

## Table of Contents

1. [00_LEGACY_IGNORE](#1-00-legacy-ignore) — `prompts_v2/00_LEGACY_IGNORE.md`
2. [01_engine_capabilities](#2-01-engine-capabilities) — `prompts_v2/schema/01_engine_capabilities.md`
3. [02_toml_schema](#3-02-toml-schema) — `prompts_v2/schema/02_toml_schema.md`
4. [03_example_toml](#4-03-example-toml) — `prompts_v2/schema/03_example_toml.md`
5. [01_rts_principles](#5-01-rts-principles) — `prompts_v2/doctrine/01_rts_principles.md`
6. [02_three_lanes_plus_capstone](#6-02-three-lanes-plus-capstone) — `prompts_v2/doctrine/02_three_lanes_plus_capstone.md`
7. [03_arc_shapes](#7-03-arc-shapes) — `prompts_v2/doctrine/03_arc_shapes.md`
8. [04_authoring_rules](#8-04-authoring-rules) — `prompts_v2/doctrine/04_authoring_rules.md`
9. [05_rts_flat_prose](#9-05-rts-flat-prose) — `prompts_v2/doctrine/05_rts_flat_prose.md`
10. [06_design_brief_template](#10-06-design-brief-template) — `prompts_v2/doctrine/06_design_brief_template.md`
11. [07_anti_patterns](#11-07-anti-patterns) — `prompts_v2/doctrine/07_anti_patterns.md`
12. [08_kink_vocab_ceilings](#12-08-kink-vocab-ceilings) — `prompts_v2/doctrine/08_kink_vocab_ceilings.md`
13. [09_trait_catalog](#13-09-trait-catalog) — `prompts_v2/doctrine/09_trait_catalog.md`
14. [10_location_design](#14-10-location-design) — `prompts_v2/doctrine/10_location_design.md`
15. [11_clothing_design](#15-11-clothing-design) — `prompts_v2/doctrine/11_clothing_design.md`
16. [12_rent_economy_design](#16-12-rent-economy-design) — `prompts_v2/doctrine/12_rent_economy_design.md`
17. [13_phone_design](#17-13-phone-design) — `prompts_v2/doctrine/13_phone_design.md`
18. [14_customization_design](#18-14-customization-design) — `prompts_v2/doctrine/14_customization_design.md`
19. [01_rts_overview](#19-01-rts-overview) — `prompts_v2/reference/01_rts_overview.md`
20. [02_rts_scene_catalog](#20-02-rts-scene-catalog) — `prompts_v2/reference/02_rts_scene_catalog.md`
21. [03_rts_walkthrough_panel](#21-03-rts-walkthrough-panel) — `prompts_v2/reference/03_rts_walkthrough_panel.md`
22. [04_rts_hud_world_model](#22-04-rts-hud-world-model) — `prompts_v2/reference/04_rts_hud_world_model.md`
23. [01_game_book_prompt](#23-01-game-book-prompt) — `prompts_v2/stages/01_game_book_prompt.md`
24. [02_toml_generation_prompt](#24-02-toml-generation-prompt) — `prompts_v2/stages/02_toml_generation_prompt.md`
25. [03_image_finder_prompt](#25-03-image-finder-prompt) — `prompts_v2/stages/03_image_finder_prompt.md`
26. [04_game_listing_prompt](#26-04-game-listing-prompt) — `prompts_v2/stages/04_game_listing_prompt.md`

---


═══════════════════════════════════════════════════════════════════════════════

## 1. 00_LEGACY_IGNORE

**Source:** `prompts_v2/00_LEGACY_IGNORE.md`

---

# 00 — Legacy Ignore List

**Status:** Doctrine gate. Read first. Applies to every prompt in `prompts_v2/`.
**Authority:** LO decisions §6.3 + §6.7 in Doc 66 (`28th_april_TLS_Phase2_Redesign/66_Session_2026_05_26_Prompts_Rewrite_Pivot.md`, 2026-05-26).
**Purpose:** Name every legacy concept this corpus does NOT reach for. Each item below says *what to ignore* and *what to use instead.*

---

## §1 — Why this file exists

The pre-2026-04-19 prompt pipeline (`prompts/game_book_prompt_v6.txt`, `prompts/toml_generation_prompt_v4.txt`, the 12 doctrine + reference + media files alongside them) teaches an LLM to design **"any adult interactive game"** with selectable architectural shapes and a 15-pattern repeatable-content vocabulary.

That vocabulary produces games that do not match the post-Doc-24 RTS-shape sandbox doctrine. The legacy concepts are not subtly wrong — they answer a different question. Applied here, they corrupt the corpus from inside: the LLM reaches for the better-known older patterns when filling gaps the new doctrine does not yet cover.

**Single locked frame:** every game generated against `prompts_v2/` is an RTS-shape sandbox. One reference game (Road to Success). One mechanism vocabulary (Lane 1 / Lane 2 / Lane 3 + Lane 4 capstones). One arc-shape taxonomy (5 shapes). One voice register doctrine (RTS-flat default + Tier-3 capstones).

If a downstream file in `prompts_v2/` cites a legacy term, the citation is the bug.

---

## §2 — What this corpus replaces

| Concern | Legacy location | Replaced by |
|---|---|---|
| Game-book authoring prompt | `prompts/game_book_prompt_v6.txt` (frozen 2026-04-19) | `prompts_v2/stages/01_game_book_prompt.md` |
| TOML authoring prompt | `prompts/toml_generation_prompt_v4.txt` (frozen 2026-04-19) | `prompts_v2/stages/02_toml_generation_prompt.md` |
| Doctrine spec | `prompts/game_design_rules.md` + `game_design_patterns.md` + `game_design_motivations.md` + `game_design_observations.md` | `prompts_v2/doctrine/01–09` (complete: 01 / 02 / 03 / 04 / 05 / 06 / 07 / 08 / 09) |
| Engine schema reference | `prompts/COMPREHENSIVE_SYSTEM_REFERENCE.md` (embeds v3, no Docs 24–65) | `prompts_v2/schema/01–03` + regenerated `prompts_v2/COMPREHENSIVE_SYSTEM_REFERENCE.md` |
| Reference-game extraction | Jack's World + New In Town walkthroughs implicit in v6 | `prompts_v2/reference/01–04` (RTS only) |
| Media / image / listing prompts | `prompts/image_finder_prompt.md` + `prompts/game_listing_prompt.md` | `prompts_v2/stages/03–04` (ported) |

The legacy `prompts/` folder stays in place as historical record (LO decision §6.7 — no migration, no archival move). It is not consulted, not cited, not "carried over."

---

## §3 — Ignore list (do NOT reach for X; instead use Y)

Each row below names a legacy concept the LLM may know from training, from older prompts in the same repo, or from related adult-IF projects. Each row pairs it with the post-Doc-24 replacement.

### §3.1 — Reference games

| ❌ Do NOT reference | ✅ Instead use |
|---|---|
| **Jack's World** | **Road to Success (RTS)** as the sole reference game. RTS extraction lives in `prompts_v2/reference/01–04` + `28th_april_TLS_Phase2_Redesign/13_Road_To_Success_Reference.md` + `game_explorations/rts-arc-trace/`. |
| **New In Town** | Same — RTS only. |
| **Two Weeks** | Same — RTS only. |
| Any other adult-IF game referenced in legacy prompts | If the design book proposes a non-RTS reference, redirect to RTS shape. The mechanism vocabulary in `prompts_v2/doctrine/` is RTS-derived; non-RTS references will produce mechanism mismatches. |

**Why:** these games predate the 3-lane doctrine. Their mechanism vocabulary is Pattern A–J; their NPC architecture is the 7-driver system; their pacing is whiteboard-goals + narrative-gates. None of those translate cleanly into the RTS sandbox shape `prompts_v2/` builds toward.

### §3.2 — Repeatable-content mechanism

| ❌ Do NOT reach for | ✅ Instead use |
|---|---|
| **Pattern A "Standard Escalating"** | **Lane 1 hub-button** mechanism. Player picks from a menu at the NPC's location; stat-gated; agency-high. (Doc 24 §2 + §6.1 + Doc 56 P5 + R1.) |
| **Pattern B / C / etc. through Pattern J** (the 10 patterns from `prompts/game_design_patterns.md`) | **Lane 1 / Lane 2 / Lane 3 / Lane 4 capstones.** Four mechanisms, mapped to fictional intent (Doc 56 P5). No 10-pattern menu. |
| **Pattern F "Story Event" / Pattern G "Gate-Setting Event"** (one-shot beats) | **Lane 4 capstones** with the fingerprint `is_repeatable = false + trigger_mode = "manual" + priority ≥ 9 + flag-setter on exit`. Three sub-types: A linear, B branching (Pattern F real choice fork, F1–F5), C chain-step. (Doc 57 §3 + §4.) |

**Why:** Pattern A–J is mechanism-shaped — "what does the engine do at this beat" — and ignores the fictional weight of *who picked it*. Lane 1/2/3/4 is intent-shaped: same physical act feels different depending on the lane delivering it (Doc 56 P5). Mixing the vocabularies produces canvases that "use the right macro" but read in the wrong emotional register.

### §3.3 — NPC architecture

| ❌ Do NOT use | ✅ Instead use |
|---|---|
| **The 7-driver NPC system** (ROMANCE / RIVAL / MENTOR / SAFE_HARBOR / THREAT / WILDCARD / AUTHORITY / CLOCK) | **The 5 arc shapes:** family/ambient, slow-burn family, peer/dating, service, antagonist/witness. (Doc 56 §5 distribution table + Docs 31/53/58/59/60/61 per-NPC briefs.) |
| **The archetype system** (named archetypes assigned per NPC) | **Arc shape declared in the R7 design brief** (Doc 56 R7 + Doc 54 Appendix A). The brief commits to: arc shape + per-lane canvas budget + vocab ceiling + tier flags. No archetypes. |

**Why:** the driver-system describes *what role this NPC plays in the story*; the arc-shape system describes *what mechanical rhythm the NPC follows*. Drivers do not translate to per-lane budgets (Doc 56 §5), and they do not surface the empty-Lane-2/3 doctrine that service + peer arcs require (Doc 53 + Doc 56 R3). Authoring against drivers reproduces the Marge failure mode (Doc 54): correct vocabulary, wrong shape.

### §3.4 — Pacing / pre-author artifacts

| ❌ Do NOT emit | ✅ Instead use |
|---|---|
| **Whiteboard goals** (Phase 2B Systems Budget concept) | **Per-arc-shape canvas distribution** (Doc 56 §5 table) + **per-lane budget declared in the R7 brief** (Doc 56 R7). The budget IS the pacing artifact. |
| **Narrative gates** (Phase 2B Systems Budget concept) | **Capstone trigger fingerprint** (Doc 57 R1) + **quest card `when`/`goals` blocks** (Doc 50 R1–R6). Gates are surfaced via capstones + quest cards, not via a separate gate registry. |
| **Income channels** as a v4 modeling entity | **`money` Tier 1 trait** + **rent-driven recurring drain** (Doc 30 §4.1 economic engine + Doc 68 §3 `money` entry). One money trait, multiple in-game sources (jobs, allowance, capstone rewards); not a separate "channel" abstraction. |

**Why:** these are scheduling-system abstractions invented to model game pacing before the 3-lane doctrine existed. Once Lane 1/2/3/4 + per-arc-shape budgets ship, the pacing emerges from the budget plus the capstone chain — no separate registry is needed, and adding one produces double-bookkeeping that drifts as the game changes.

### §3.5 — Game shape

| ❌ Do NOT model | ✅ Instead use |
|---|---|
| **"Single-NPC Romance" architecture** (Jack's World shape) | **RTS-shape sandbox.** 4–6 NPCs in parallel, each with one arc shape from the 5-shape taxonomy. (Doc 66 §0 target picture + Doc 56 P4.) |
| **"Multi-NPC Parallel Arcs" architecture** (New In Town shape) | Same — RTS-shape sandbox. The "multi-NPC parallel arcs" framing is closer than Single-NPC-Romance, but it omits the per-arc-shape mechanical rhythms + per-lane canvas budgets that make RTS work. RTS-shape IS multi-NPC parallel, but with specific mechanical structure. |
| **Selectable game shapes** (the v6 "pick Single-NPC vs Multi-NPC" frame) | **No selection.** Every game is RTS-shape. (LO decision §6.1.) |

**Why:** LO locked this at the Doc 66 pivot. The redesign work (Doc 24–65) produced a complete design language for one game shape; teaching the LLM to select between shapes means it has to apply doctrine for shapes that have no design language yet. One shape, taught deeply, no menus.

### §3.6 — Voice / persona

| ❌ Do NOT consult | ✅ Instead use |
|---|---|
| **CLAUDE.md ENI persona** (sensory richness, layered prose, body language during dialogue, interior monologue, sentence variety, "show don't tell") | **RTS-flat default** for Lane 1 / Lane 2 / Lane 3 prose (Doc 30 §7.1 8 rules + `feedback_tls_scene_body_style` memory). **Tier-3 literary register EARNED at Lane 4 capstones only** (Doc 57 §6). |
| Multi-paragraph atmospheric openings | **Image-first composition.** Prose is ≤ 30-word caption. Stage direction cap: 2 sentences per beat. (Doc 30 §7.1 #8 + #2.) |
| Sensory grounding rituals ("3-4 layered sensory details minimum; include smell," etc.) | **Zero environmental sensory detail** in Lane 1/2/3 bodies. Dialogue does the character work. Crude direct diction per arc vocab ceiling (Doc 30 §7.5). |
| "It's not X, but Y" anti-pattern + hypophora + literary cadence rituals | Speaker-tag template; `<<Speech>>` macros heavily; one beat = one click. |

**Why:** the ENI persona is the default register for chat/roleplay. It is the wrong register for canvas authoring (Doc 30 §3 AUTHORITY DECLARATION). The Marge session (Doc 54) cost ~8 hours to a single failure: persona's literary instinct overriding RTS-flat doctrine. The override mechanism is explicit — *"ENI persona OFF. TLS game register ON."* — declared at the start of any authoring task (Doc 54 §2.5).

**Per LO decision §6.4:** CLAUDE.md is ignored for `prompts_v2/`. No carve-outs needed. The prompts override CLAUDE.md when active.

---

## §4 — Tone test (apply before shipping any file in `prompts_v2/`)

For each file authored against this corpus, mentally grep for legacy terms before shipping. The expected result is:

- **Zero hits** for `jack's world`, `new in town`, `two weeks` (case-insensitive).
- **Zero hits** for `pattern a`, `pattern b`, … `pattern j` (case-insensitive; expected hits ONLY in this file, naming them to ignore).
- **Zero hits** for `npc-driver` / `7-driver` / `archetype-system` / `whiteboard goal` / `narrative gate` / `income channel` (any spacing).
- **Zero hits** for `single-npc romance` / `multi-npc parallel arc` framed as architecture choice.
- **Zero hits** for `sensory grounding` / `sensory density` / `body language during dialogue` / `interior monologue` / `ENI persona` / `claude.md`, except in explicit contrast-against-RTS-flat passages.

If any file in `prompts_v2/` (other than this one) contains these terms, that file has leaked legacy vocabulary. Rewrite the offending passage. Don't paper over with a comment.

---

## §5 — When in doubt

If the design book or downstream specification calls for a concept this list does not cover, the question to ask is not *"which legacy pattern fits?"* but *"what is the fictional intent, and which Lane / arc shape / capstone type carries that intent?"*

The corpus has answers for:

- "How does this NPC's content escalate over time?" → arc shape + per-lane canvas budget (Doc 56 §5; `doctrine/03_arc_shapes.md`)
- "How does this beat fire?" → Lane 1 / 2 / 3 / 4 (Doc 24 + Doc 57; `doctrine/02_three_lanes_plus_capstone.md`)
- "How does this NPC become available in the player's day?" → schedule + `requires_npc` + getNpcLocation (Doc 24 §6 + Doc 67 §3; `schema/01_engine_capabilities.md`)
- "How does this scripted scene get reached?" → capstone trigger fingerprint + quest card pointer (Doc 57 R1–R5 + Doc 50 R1–R6; `doctrine/04_authoring_rules.md`)
- "What does the player see in the HUD?" → sidebar items + body-state vs progression-state doctrine (Doc 49 + Doc 68 §8; `schema/01_engine_capabilities.md` + `doctrine/09_trait_catalog.md`)
- "How explicit is this NPC allowed to get?" → per-arc vocabulary ceiling (Doc 30 §7.5; `doctrine/08_kink_vocab_ceilings.md`)
- "What stats does the game use?" → Tier 1 (corruption / arousal / energy / hygiene / money + per-NPC arousal / corruption / relation / stage) + Tier 2 (fitness / beauty / exhibitionism / intelligence) (Doc 68; `doctrine/09_trait_catalog.md`)

If none of the above answers apply, the question may be outside the RTS-shape sandbox scope. Surface it to LO rather than reaching for a legacy pattern.

---

**End of file.** Every other file in `prompts_v2/` is authored under the constraints declared above.

═══════════════════════════════════════════════════════════════════════════════

## 2. 01_engine_capabilities

**Source:** `prompts_v2/schema/01_engine_capabilities.md`

---

# Schema 01 — Engine Capabilities

**Status:** Ground-truth schema reference. Extracted live from engine source on 2026-05-28. Every line number below verified against current `apps/projects/services/template_import.py` + `apps/game_generation/twee_comprehensive/generators/v2.py`.
**Authority:** This file is the ground truth for what the engine actually does. Doctrine files (`prompts_v2/doctrine/`) cite this file; this file does not cite them.
**Purpose:** Name every engine primitive an authoring LLM may legitimately reach for, with the file path + line range where the primitive lives. When a doctrine doc says *"the engine emits X via Y"*, the cross-reference resolves here.

**Reading order for fresh LLM sessions:** §3 (canvas + trigger) → §6 (effect + predicate vocabulary — most authoring touches this) → §7 (quest cards) → §8 (sidebar items) → others as needed.

**Engine files:**
- **Schema + validator:** `apps/projects/services/template_import.py` (~9,800 lines). Source of all TOML dataclasses. Runs `normalize()` (TOML → GameTemplate) + `validate()` (semantic checks).
- **Active generator:** `apps/game_generation/twee_comprehensive/generators/v2.py` (~17,500 lines). Emits SugarCube/Twine passages + runtime `setup.*` helpers. Default generator.
- **Frozen rollback:** `apps/game_generation/twee_comprehensive/generators/v1.py` (~17,000 lines). Wholesale copy of v2 at 2026-05-14. **Do NOT edit v1.** Reference v2 for line numbers in this doc.

---

## §1 — What this file is, and what it is NOT

### Is

- Per-primitive: name + dataclass file:line (schema side) + runtime file:line (generator side) + brief one-paragraph behavior.
- Schema field tables.
- The exhaustive list of supported predicate types + effect types + sidebar item types.

### Is not

- Doctrine. *"When to use Lane 3 vs Lane 4"* lives in `doctrine/02_three_lanes_plus_capstone.md`. This file only tells you *"Lane 3 is implemented as `substitutions` + `substitution_only` on `TemplateTrigger`, with runtime dispatch at `v2.py:4649`."*
- Tutorial. Each primitive gets one paragraph of behavior + a TOML shape example, not a walkthrough.
- A migration log. If a primitive was added in PRD N, the citation is in this file. The PRD itself is not summarized.

---

## §2 — Top-level TOML structure

A complete game template emits these top-level sections. Order in the TOML file is not significant.

```toml
[project]                 # § 2.1
[settings]                # § 2.1
[player]                  # § 2.2
[[npcs]]                  # § 2.3
[[locations]]             # § 2.4
[[canvases]]              # § 3
[[quest_cards]]           # § 7
[[sidebar_items]]         # § 8
[engine.daily_tick]       # § 9
[[clothing]]              # § 10
[[stage_helpers]]         # § 11
[[trait_labels]]          # § 12.2
[[flag_labels]]           # § 12.2
[[passes]]                # § 12.3
[[items]]                 # § 12.4
[[fast_jobs]]             # § 12.5
[[banks]]                 # § 12.6
[[modifiers]]             # § 12.7
[[themes]]                # § 12.8
[phone]                   # § 13
[hints]                   # § 14 (deprecated — Quest cards Doc 47/48 supersede)
```

Field-by-field schema for each section is in `schema/02_toml_schema.md`. This file documents the runtime behavior + engine primitives those sections feed.

### §2.1 — `[project]` + `[settings]`

| Dataclass | File:line |
|---|---|
| `TemplateProject` | `template_import.py:43` |
| Top-level `quests_engine` selector | parsed in `normalize()` at `template_import.py:1441+` |

**`quests_engine`** — set to `"v2"` in `[project]` to enable the V2 Quests engine (`[[quest_cards]]` mode). Default `"v1"` (deprecated; `[hints]` system; do not author against). All RTS-shape sandbox games declare `quests_engine = "v2"`.

### §2.2 — `[player]`

| Dataclass | File:line |
|---|---|
| `TemplatePlayer` | `template_import.py:81` |
| `TemplatePlayerCustomizationField` | `template_import.py:70` |

`[player.core_traits]` — initial trait values. **Every player trait referenced anywhere in the game MUST be declared here at game start with an initial integer value.** Engine reads `(player.core_traits || {})[key]` at runtime; undeclared = `undefined` = silent garbage. Sidebar items referencing undeclared traits are hard-rejected by the validator; effects + conditions on undeclared traits silently no-op. See `doctrine/09_trait_catalog.md` §2.5.

### §2.3 — `[[npcs]]`

| Dataclass | File:line |
|---|---|
| `TemplateNPC` | `template_import.py:107` |
| `TemplateNPCSchedule` | `template_import.py:94` |

`[[npcs.schedules]]` — see §5.

`[[npcs.core_traits]]` — per-NPC initial trait values, parallel structure to `[player.core_traits]`. Same declare-before-use rule.

`arc_stages = [...]` — list of stage NAMES (display strings) for the NPC's arc. The CURRENT stage integer lives on the player namespace as `player.core_traits.<slug>_stage`. See §6.7 + `doctrine/09_trait_catalog.md` §9.

---

## §3 — Canvas + Trigger primitives (Lane 1/2/3/4 mechanism support)

The canvas is the engine's universal content primitive. Lane 1 (hub button), Lane 2 (location-entry random), Lane 3 (dispatcher substitution), Lane 4 (capstone auto-fire) — all four lanes are implemented as canvases with different trigger field combinations. There is no separate "lane" dataclass.

### §3.1 — `TemplateCanvas`

| Field | Type | Where used |
|---|---|---|
| `id` | str | unique slug |
| `name` | str | display |
| `description` | str | author-side |
| `guide` | str (Doc 56 R5 — currently not yet a parsed field, see §10.7) | published-catalog recipe |
| `trigger` | `TemplateTrigger` | gating + scheduling — §3.2 |
| `nodes` | `List[TemplateNode]` | body |
| (others) | — | see `schema/02_toml_schema.md` |

`TemplateCanvas` dataclass: `template_import.py:673`.

### §3.2 — `TemplateTrigger` (THE Lane gating mechanism)

Dataclass: `template_import.py:448–502`.

| Field | Type | Lane implication |
|---|---|---|
| `location` | str | Where the canvas anchors. Lane 1/2/3/4 all require `location`. |
| `is_active` | bool (default `true`) | Soft on/off switch. |
| `is_repeatable` | bool (default `true`) | Lane 1/2/3 = `true`. Lane 4 capstone = `false` OR `true` + `flag_is_false` self-gate (see Doc 57 R1). |
| `max_triggers_per_day` | Optional[int] | Per-day cap. Lane 3 substitution targets typically `1` (Doc 67 R7). |
| `priority` | int (default 0) | Tie-break in `selectAutoFireCanvasForLocation`. Lane 4 capstones use `priority ≥ 9` (Doc 57 R1). |
| `conditions` | dict | The `{version, logic, items: [...]}` block. See §6.3 for predicate vocabulary. |
| `schedules` | `List[TemplateTriggerSchedule]` | Per-canvas time windows. See §5. |
| `npc` | Optional[str] | NPC slug for navigation indicator. |
| `trigger_mode` | str | `"manual"` (Lane 1 / Lane 3 / Lane 4) or `"random"` (Lane 2). |
| `chance` | Optional[float] (0.0–1.0) | Lane 2 random fire probability. |
| `costs` | List[dict] | Resource costs deducted on entry. |
| `show_when_blocked` | bool | E21 — render grayed-out entry on QuestsPage when daily-cooldown blocks fire. |
| `cooldown_message` | Optional[str] | Text shown on blocked entry. |
| `entry_only_from` | List[str] | Lane 2 anti-toggle cooldown (L2-2 doctrine fix). Canvas only fires if previous location matched. |
| `substitutions` | List[dict] | Lane 3 substitution rules — see §4. |
| `substitution_only` | bool | When true, canvas is excluded from `renderNpcPortraits` + `renderSoloActivities` + `selectAutoFireCanvasForLocation`. Only reachable via another canvas's substitution rule. |
| `requires_npc` | Optional[str] | Phase A (2026-05-14). Lane 2/3 NPC-presence gate via NPC schedule. Engine ANDs with all other gates. |
| `pre_substitution_effects` | List[dict] | Doc 69 §4 + §5.2 — Pattern C unconditional effects that run BEFORE substitution check. Activity "counts" even if NPC walks in. |

### §3.3 — Lane fingerprints (recognition rules)

| Lane | Diagnostic fields |
|---|---|
| **Lane 1 — Hub button** | `trigger_mode = "manual"` + `is_repeatable = true` + `npc` set + `location` matches NPC's schedule. Rendered by `renderNpcPortraits` (`v2.py:4295`) at NPC's location. **The hub's portrait renders only when the hub's OWN `schedules` window is live (`isCanvasValid`, `v2.py:4356`) AND the NPC is present (presence gate, `v2.py:4384`).** So presence coverage is per schedule row: a hub at the location with a narrower `schedules` than the NPC's presence leaves the uncovered windows dead. Author one hub per scheduled window (D72-R6, `doctrine/04` §6.1). |
| **Lane 2 — Location-entry random** | `trigger_mode = "random"` + `chance` set + `is_repeatable = true`. Dispatched by `checkRandomEncounters` (`v2.py:4520`) on location entry. |
| **Lane 3 — Dispatcher substitution** (parent activity) | `trigger_mode = "manual"` + `is_repeatable = true` + `substitutions = [...]`. Player-clickable solo activity. |
| **Lane 3 — Substitution target** | `substitution_only = true` + `requires_npc` set + `is_repeatable = true` + `max_triggers_per_day = 1`. Not in any portrait/activity grid. |
| **Lane 4 — Capstone** | `trigger_mode = "manual"` (default) + `priority ≥ 9` + (`is_repeatable = false` OR `flag_is_false` self-gate) + flag-setter effect on exit. Auto-fires on location entry via `selectAutoFireCanvasForLocation` (`v2.py:3885`). |

### §3.4 — Engine entry points for each lane

| Lane | Engine function | File:line |
|---|---|---|
| Lane 1 portraits | `renderNpcPortraits` | `v2.py:4295` |
| Lane 1 solo-activity buttons | `renderSoloActivities` | `v2.py:4419` |
| Lane 2 random encounters | `checkRandomEncounters` | `v2.py:4520` |
| Lane 3 substitution dispatch | `checkAndSubstituteCanvas` | `v2.py:4649` |
| Lane 4 capstone auto-fire | `selectAutoFireCanvasForLocation` | `v2.py:3885` |
| Location-entry dispatcher | `getStoryCanvasRedirect` | `v2.py:4272` |
| Canvas validity check | `isCanvasValid` / `isCanvasValidForSelection` | `v2.py:4005` / `v2.py:4030` |
| Trigger cooldown checks | `canTriggerCanvas` / `canTriggerActivity` | `v2.py:3621` / `v2.py:3661` |
| Mark canvas fired | `markCanvasTriggered` | `v2.py:3722` |

---

## §4 — Lane 3 substitution primitive (PRD 25)

The dispatcher mechanism is a `substitutions` list on the PARENT activity's `TemplateTrigger`. Each rule names a target canvas, a `chance`, and optional extra `conditions`.

### §4.1 — TOML shape

```toml
# Parent activity (Lane 3 host)
[[canvases]]
id = "activity_wash_dishes"
name = "Wash dishes"
[canvases.trigger]
location = "loc_kitchen"
trigger_mode = "manual"
is_repeatable = true
schedules = [{ weekdays = [0,1,2,3,4,5,6], start_time = "07:00", end_time = "21:00" }]

[[canvases.trigger.substitutions]]
target_canvas_id = "scene_frank_kitchen_dishes"  # slug (resolves to UUID at build time)
chance = 0.33
conditions = { items = [
  { type = "trait", subject = "npc", npc_id = "npc_frank", trait_key = "stage", operator = "gte", value = 2 },
] }

# Substitution target (Lane 3 walk-in scene)
[[canvases]]
id = "scene_frank_kitchen_dishes"
[canvases.trigger]
location = "loc_kitchen"
trigger_mode = "manual"
is_repeatable = true
max_triggers_per_day = 1
substitution_only = true        # NOT in portrait/activity grids
requires_npc = "npc_frank"      # NPC must be co-located per schedule
schedules = [{ weekdays = [0,1,2,3,4,5,6], start_time = "07:00", end_time = "21:00" }]
```

### §4.2 — Engine semantics (`checkAndSubstituteCanvas` at `v2.py:4649`)

Order of evaluation per substitution rule:
1. Resolve `target_canvas_id` slug → UUID via `setup.canvasSubstitutions[parentCanvasId]` registry (built at emission).
2. Look up the target canvas via `getCanvasById` (`v2.py:2669`).
3. Call `isCanvasValid(target)` — checks `is_active`, schedule, `requires_npc`, cooldown, conditions.
4. If rule has its own `conditions`, evaluate them via `triggerConditionsSatisfied` (§6.3).
5. Roll `Math.random() < chance`.
6. First match returns; `Engine.play(target.passageName)` preempts the parent passage body.

**Two evaluation modes (Doc 69 Item 1 shipped 2026-05-27):**

1. **Pattern B groups first.** Rules sharing an `exclusive_group` string share ONE dice roll, partitioned into cumulative buckets by `chance`. If the dice lands in a bucket whose target/conditions/`requires_npc` fail, the engine **falls through to solo** — it does NOT promote the next rule in the group. This is the true Pattern B semantic (Doc 67 §4.2). Multiple groups process in declaration order, each with its own dice.

2. **Pattern A independent rules next.** Rules WITHOUT an `exclusive_group` field roll their own dice (first-match wins). Pattern A per Doc 67 §4.1. Mixed A+B in the same dispatcher is supported — groups always evaluate before independents.

Rule order within a group = priority order (cumulative bucket order). Rule order across groups = first-seen order in the TOML.

Pattern C (unconditional pre-substitution effects) is shipped separately via `pre_substitution_effects` — see §4.3.

### §4.3 — `pre_substitution_effects` (Pattern C — shipped Doc 69 Item 2)

Effects that run unconditionally on canvas entry, BEFORE the substitution check. If a substitution preempts via `<<goto>>`, these effects have already executed. RTS Pattern C analog (Exercise's `<<AddFit>>` runs before NPC interrupt).

Each entry is the same shape as `TemplateChoiceEffect` (see `schema/02_toml_schema.md` §16): `{ targetType, npcId?, trait, op, value, clamp?, cap? }` — no `type` field.

```toml
[canvases.trigger]
# ... existing fields ...

[[canvases.trigger.pre_substitution_effects]]
targetType = "player"
trait      = "fitness"
op         = "add"
value      = 1
```

Engine: `v2.py:11151` reads `canvas.trigger.metadata.pre_substitution_effects` and emits `<<script>>setup.applyAndNotifyTrait(...)<</script>>` macros at the top of the passage body, before the substitution `<<goto>>`. Schema: `TemplateTrigger.pre_substitution_effects` field on the trigger dataclass.

### §4.4 — `exclusive_group` (Pattern B partition — shipped Doc 69 Item 1)

Per-substitution-rule field that marks the rule as part of a Pattern B exclusive group.

```toml
[canvases.trigger]
location = "loc_bedroom"
# ... existing trigger fields ...

# Pattern B — Brother sub-variants at the study desk; one fires per attempt or fall to solo
[[canvases.trigger.substitutions]]
target_canvas_id = "scene_brother_grope_at_desk"
chance           = 0.1667                          # 1/6
exclusive_group  = "study_desk_brother"
conditions = { version = "1.0", items = [
  { type = "trait", subject = "npc", npc_id = "npc_brother", trait_key = "corruption", operator = "gte", value = 5 },
] }

[[canvases.trigger.substitutions]]
target_canvas_id = "scene_brother_help_study"
chance           = 0.1667                          # 1/6 — combined group bucket = 0.33
exclusive_group  = "study_desk_brother"
conditions = { version = "1.0", items = [
  { type = "trait", subject = "npc", npc_id = "npc_brother", trait_key = "love", operator = "gte", value = 3 },
] }
```

Engine: `v2.py:4671-4713` partitions `subs` by `exclusive_group` string, rolls one dice per group, walks cumulative buckets. Buckets that fail target/conditions/`requires_npc` fall through to solo (the parent canvas's body runs). Rules without `exclusive_group` go through the Pattern A independent-rules pipeline after all groups process.

---

## §5 — Schedule + NPC presence primitives (Phase A, 2026-05-14)

### §5.1 — `[[npcs.schedules]]` — NPC location source of truth

| Field | Type | Notes |
|---|---|---|
| `location` | str | Location slug — resolved to UUID at build time |
| `weekdays` | List[int] | 0=Monday … 6=Sunday. Empty = all days |
| `start_time` | str (`HH:MM`) | Window start (24h) |
| `end_time` | Optional[str] (`HH:MM`) | Window end |
| `activity` | str | Description (author-side / sidebar) |

Dataclass: `template_import.py:94`. Parsing: `normalize()` resolves slug→UUID; build fails on invalid location slug (Phase A bugfix shipped 2026-05-14).

**Schedule entries should be non-overlapping for a single NPC.** Where in-fiction the NPC's activity differs by time band (kitchen morning vs kitchen evening), use separate entries.

**Each schedule row is a promise of a Lane 1 hub (D72-R6).** Because the schedule page advertises where every NPC is per room per window, every row must have a Lane 1 hub whose own `trigger.schedules` covers that window (per-window = separate hub canvas; §3.3). A row with no live hub is dead presence. An NPC with no physical hub anywhere (a rent/phone-only "system" NPC) must carry NO schedule row. See `doctrine/04` §6.

### §5.2 — `getNpcLocation` runtime (`v2.py:2923`)

```javascript
setup.getNpcLocation = function(npcId) { ... }
```

Computes NPC's current location on-demand by scanning the NPC's schedule entries and returning the location whose time window contains the current in-game day + time. Returns location ID, or `null` if no schedule entry matches.

**There is no stored `npcs[uuid].location` field.** Location is derived. Authoring can use the location either via `requires_npc` (Lane 2/3 presence gate) or via the `stage` trait predicate (NPC's stage — distinct from location).

### §5.3 — `requires_npc` trigger gate

When set on a `TemplateTrigger`, the engine ANDs `(getNpcLocation(requires_npc) === canvas.location)` with all other gates. The NPC must currently be at the canvas's location per their schedule.

Use case: Lane 2/3 canvases that need NPC co-presence WITHOUT the author duplicating the NPC's schedule on every canvas. Single source of truth = `[[npcs.schedules]]`.

### §5.4 — Predicate semantic: walk-in direction (Doc 67 §3.5)

Two distinct presence patterns:

| Pattern | TOML | Use case |
|---|---|---|
| **NPC walks in on Maya (Lane 3)** | `requires_npc = "npc_X"` with NPC's schedule resolving to **any** home location (e.g., a meta-location). | "Frank wandered into the kitchen because Maya is there." |
| **Maya walks in on NPC (Lane 2)** | `requires_npc = "npc_X"` with NPC's schedule resolving to **exact** canvas location. | "Maya enters the kitchen and Frank is already there." |

Both use the same `requires_npc` field; the semantic difference lives in the NPC's schedule shape, not in the canvas's predicate.

---

## §6 — Trait effect + predicate primitives

⚠️ **Effect syntax and predicate syntax use DIFFERENT field names.** Mixing them silently fails (no build error). The single most common authoring mistake. See §6.5 reference card.

### §6.1 — Trait effects (mutations)

```toml
# Player trait — add
{ targetType = "player", trait = "corruption", op = "add", value = 1 }

# Player trait — set (e.g., arousal climax reset)
{ targetType = "player", trait = "arousal", op = "set", value = 0 }

# Player trait — decay via negative add
{ targetType = "player", trait = "energy", op = "add", value = -10 }

# NPC trait
{ targetType = "npc", npcId = "npc_frank", trait = "relation", op = "add", value = 2 }

# With clamp + cap
{ targetType = "player", trait = "arousal", op = "add", value = 1, clamp = true, cap = 10 }
```

| Field | Required? | Notes |
|---|---|---|
| `targetType` | yes | `"player"` or `"npc"` |
| `trait` | yes | Trait name (NOT `trait_key`) |
| `op` | yes | `"add"` or `"set"` — **no `"sub"` op** (use `op = "add"` + negative `value`) |
| `value` | yes | Integer |
| `npcId` | yes when `targetType = "npc"` | NPC slug (NOT `npc_id`) |
| `clamp` | no | If true, result floored at 0 |
| `cap` | no | Integer upper bound |

Schema: `TemplateChoiceEffect` at `template_import.py:503`. Runtime application: `applyAndNotifyTrait` at `v2.py:5174`.

### §6.2 — Flag effects

```toml
{ targetType = "player", flag = "frank_caught", op = "set" }
{ targetType = "player", flag = "talked_to_ryan_today", op = "unset" }
{ targetType = "npc", npcId = "npc_frank", flag = "secret_known", op = "set" }
{ targetType = "player", flag = "scandal_visible", op = "toggle" }
```

| Field | Required? |
|---|---|
| `targetType` | yes |
| `flag` | yes |
| `op` | yes — `"set"`, `"unset"`, or `"toggle"` |
| `npcId` | yes when `targetType = "npc"` |

Schema: `TemplateFlagEffect` at `template_import.py:521`.

### §6.3 — Predicate (trigger condition) vocabulary

```toml
[canvases.trigger.conditions]
version = "1.0"   # required — schema version
logic = "AND"     # optional (default "AND"); also "OR"
items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 15 },
  { type = "trait", subject = "npc", npc_id = "npc_frank", trait_key = "relation", operator = "gte", value = 30 },
  { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_true" },
]
```

Runtime: `triggerConditionsSatisfied` at `v2.py:3275`.

**Supported `type` values** (verified at `v2.py:3275–3700`):

| `type` | Required fields | Operators |
|---|---|---|
| `"flag"` | `subject`, `flag_key` | `is_true`, `is_false`, `exists` |
| `"modifier"` | (impl-specific) | `is_active`, else |
| `"trait"` | `subject`, `trait_key`, `operator`, `value` | numeric: `eq`/`ne`/`gt`/`gte`/`lt`/`lte`; set: `in`/`not_in`; existence: `exists`/`not_exists` |
| `"days_since_flag"` | `subject`, `flag_key`, `operator`, `value` | numeric (compares days since flag was set via `flags_meta.set_day`) |
| `"clothing_slot"` | `slot`, `operator` | `equipped`, `unequipped` |
| `"clothing_item"` | `item_id`, `operator` | `equipped`, `unequipped`, `owned`, `not_owned` |
| `"worn_beauty"` | `operator`, `value` | numeric. MAX aggregate of equipped beauty. Doc 37. |
| `"worn_corruption"` | `operator`, `value` | numeric. MAX aggregate of equipped corruption. Doc 37. |
| `"worn_type"` | `operator`, `value` | `eq` / `neq` — outfit category check via `setup.getWornTypes()`. Doc 72. |
| `"pass"` | `pass_id`, `operator` | `is_active`, else |
| `"item"` | `item_id`, `operator`, `value` | numeric inventory count |
| `"stage"` | `helper`, `operator` | resolves named helper from `setup.stage_helpers_map` (`v2.py:2641`) — recursively evaluates the helper's condition block |
| `"quest"` | (V2 quests engine) | quest-card-state predicate |
| `"corruption_level"` | `operator`, `value` | banded corruption check |

`subject` values: `"player"` or `"npc"`. When `"npc"`, requires `npc_id`.

### §6.4 — Logical composition

```toml
items = [
  { type = "trait", ... },                  # implicit AND
  { type = "trait", ... },
]
# OR with explicit logic
logic = "OR"
```

Nested logic groups: pass `subgroup` items with their own `items` + `logic`. Recursion handled in `triggerConditionsSatisfied`.

### §6.5 — Field-name reference card (KEEP HANDY)

| Concept | EFFECT field | PREDICATE field |
|---|---|---|
| Player vs NPC | `targetType` | `subject` |
| NPC identifier | `npcId` | `npc_id` |
| Trait name | `trait` | `trait_key` |
| Flag name | `flag` | `flag_key` |
| Operation | `op` (`"add"`, `"set"` for traits; `"set"`, `"unset"`, `"toggle"` for flags) | `operator` (`"gte"`, `"lt"`, etc.) |
| Type discriminator | (dispatched by `trait` vs `flag` field presence) | `type` (required: `"trait"`, `"flag"`, etc.) |

**Using effect field names in a predicate (or vice versa) causes silent no-ops — no build error fires.** Validators at `template_import.py:1077` (`_validate_effect_field_names`) + `:1098` (`_validate_predicate_field_names`) catch some cases as warnings; not all.

### §6.6 — Daily decay (`[engine.daily_tick]`)

```toml
[engine.daily_tick]
flagEffects = [
  { targetType = "player", flag = "talked_to_ryan_today", op = "unset" },
]
traitEffects = [
  { targetType = "player", trait = "hygiene", op = "add", value = -10 },
  { targetType = "player", trait = "arousal", op = "add", value = 1, cap = 10 },
  { targetType = "npc", npcId = "npc_frank", trait = "arousal", op = "add", value = 1, cap = 3 },
]
```

Dataclass: `TemplateDailyTick` at `template_import.py:404`. Each `traitEffects` entry reuses the choice-effect shape (`targetType`/`npcId`/`trait`/`op`/`value`/`clamp`/`cap`).

**Doctrine constraint** (Doc 40, `doctrine/09_trait_catalog.md` §3 + §4): only `hygiene` (and similar body-state) decays daily; `corruption`, `arousal`, `relation`, `stage` do NOT decay. Authoring `corruption -1` in `traitEffects` is wrong.

### §6.7 — Stage advancement (special-case)

`applyAndNotifyTrait` at `v2.py:5183–5189` matches the trait name against `/^([a-z_]+)_stage$/` and, when `targetType === 'player'` + delta > 0:
- Updates `setup.npc_arc_stages[slug]` registry.
- Writes `game_state.stage_advancement_log[slug] = currentDay`.

**Mutation shape (capstone exit — advance Frank to stage 2):**

```toml
{ targetType = "player", trait = "frank_stage", op = "set", value = 2 }
```

NOT `targetType = "npc"`. Stage lives on the player namespace as `<slug>_stage`. The NPC's `arc_stages = [...]` block is just the LIST of stage NAMES (display strings).

**Predicate (check Frank's stage):**

```toml
# Form A — raw player-trait check (recommended)
{ type = "trait", subject = "player", trait_key = "frank_stage", operator = "gte", value = 2 }

# Form B — via helper (engine plumbing; avoid in authoring)
{ type = "stage", helper = "frank_stage_2_plus", operator = "is_true" }
```

---

## §7 — Quest card primitives (V2 engine, PRD 48)

### §7.1 — `QuestsCard` dataclass

Dataclass: `template_import.py:852`.

| Field | Type | Notes |
|---|---|---|
| `text` | str | Maya-voice narrative copy (when card is climbing) |
| `ready_text` | Optional[str] | Maya-voice "moment is on her" line (when goals met) |
| `tip` | Optional[str] | Maya-voice interior observation |
| `npc_id` | Optional[str] | When set → renders in that NPC's section. When absent → top "Story Goals" section. |
| `priority` | int (default 0) | Tie-breaker among matching cards |
| `group` | Optional[str] | Story Goals only — group key for crisis-variant collapse |
| `when` | `List[QuestsCondition]` | Routing — ALL items must eval true for this card to win the picker |
| `goals` | `List[QuestsCondition]` | The 🎯 To advance bullets — `◯ <label> — X / Y` rendering |
| `ready_canvas` | Optional[str] | When `goals.allMet` AND set, renders 🔓 Ready frame with 📍 + 🕒 from the canvas's metadata |
| `terminal` | bool (default `false`) | When true AND `when` matches → renders ✓ Arc complete |

`QuestsCondition` dataclass: `template_import.py:832`.

### §7.2 — Three card modes (Doc 50 §2)

| Mode | Has `ready_canvas`? | Has `goals`? | What player sees |
|---|---|---|---|
| **Capstone** | yes | optional (climb bullets above `when`) | 🔓 Ready frame when goals met; otherwise 🎯 climbing |
| **Mechanic** | no | yes | 🎯 climbing only — threshold cross IS the unlock; picker swaps to next template atomically |
| **Hybrid** (arc level, not card level) | mixed across cards in chain | mixed | Each card is one mode at a time |

### §7.3 — Picker semantics

Engine walks all cards' `when` against current state. Cards whose `when` passes are candidates. Sort: (priority desc, `when.length` desc, file-order asc). Top candidate wins. Story Goals additionally group by `group` key.

### §7.4 — Renderer frames

Runtime: `renderQuestsGoalBlock` (v2 generator).

| Frame | When |
|---|---|
| ✓ Arc complete (Frame 1) | `terminal = true` AND `when` matches |
| 🔓 Ready (Frame 2) | `goals.allMet` AND `ready_canvas` set |
| 🎯 To advance — bullets (Frame 3) | `goals` exist AND NOT `allMet` |
| (Frame 4 — narrative only) | DO NOT use — renders frameless; deprecated |

### §7.5 — Quest card validators (R1–R5)

Wired at `_validate_quests_cards` in `template_import.py:4469`. Validates Doc 50 R1–R4. Doc 56 R6 (`txt_only` ban) folds into R1 + R2 (every card must be capstone or mechanic; mechanic with no `goals` is rejected).

---

## §8 — Sidebar item primitives (Doc 49 + 56 R4)

`[[sidebar_items]]` — each entry is `{ type = "X", ... type-specific fields }`. Validator at `template_import.py:3024`+.

### §8.1 — Supported sidebar item types

| `type` | Use case | Schema location |
|---|---|---|
| `"trait_words"` | Banded prose label (Pure/Lewd/Slutty/Whore for corruption). 4 named bands. Raw number hidden. | `template_import.py:3032`+ |
| `"trait_bar"` | Numeric bar with optional band-text overlay + color tiers. NPC-owner mode supported (`trait_owner = "npc"` + `npc_id`). | `template_import.py:3083`+ |
| `"trait_status_text"` | Banded body-state text (Filthy/Dirty/Fresh/Clean for hygiene). Renders nothing when no band matches. | `template_import.py:3171`+ |
| `"trait_decay_warning"` | Amber warning when a decaying trait dropped today AND is within range of a band gate. Sibling of `trait_status_text`. | `v1.py:5620` (`getDecayWarnings` helper) + `v1.py:13850` (SugarCube template) |
| (more: passes, inventory, etc.) | — | see `schema/02_toml_schema.md` |

**Visibility doctrine** (Doc 68 §8): stage NEVER surfaces to any sidebar item. Antagonist awareness NEVER surfaces. See `doctrine/09_trait_catalog.md` §8.

### §8.2 — Validator enforcement

`template_import.py:2382–2547` — `_player_trait_keys` is built from `(template.player.core_traits or {}).keys()`. Sidebar items (`trait_words`, `trait_bar`, `trait_status_text`) referencing undeclared traits are **hard-rejected** with an error. (Effects + conditions on undeclared traits silently no-op; sidebar is the only surface with build-time enforcement.)

---

## §9 — Clothing primitives (Doc 36/37/71/72)

### §9.1 — `[[clothing]]` items

Dataclass: `TemplateClothingItem` at `template_import.py:164`.

| Field | Type | Notes |
|---|---|---|
| `id` | str | unique slug |
| `slot` | str | Must be in `VALID_CLOTHING_SLOTS` = `{"bra", "underwear", "top", "bottom", "dress", "legwear", "shoes"}` (`template_import.py:153`) |
| `beauty` | int | Per-item beauty value. `worn_beauty` predicate returns MAX across equipped items. |
| `corruption` | int | Per-item corruption value. `worn_corruption` returns MAX across equipped items. **NOTE: this is a content-router stat; does NOT feed `player.corruption`.** (Doc 37) |
| `type` | str (Doc 72, 2026-05-28) | Outfit category — e.g. `"casual"`, `"swim"`, `"costume"`, `"schoolwear"`, `"fitness"`, `"uniform"`, `"sleepwear"`. Recommended set in `RECOMMENDED_CLOTHING_TYPES` (`template_import.py:158`); any string accepted; typo-catch warning fires when no item declares the referenced type. |

### §9.2 — Runtime helpers

| Helper | Returns |
|---|---|
| `setup.getWornBeauty()` (`v2.py:1236`) | MAX beauty across equipped items |
| `setup.getWornCorruption()` (`v2.py:1237`) | MAX corruption across equipped items |
| `setup.getWornTypes()` (`v2.py:1243`) | Array of unique non-empty `type` strings across equipped items |

### §9.3 — Predicates

- `worn_beauty` — numeric ops (`gte`, `lt`, etc.)
- `worn_corruption` — numeric ops
- `worn_type` — `eq` / `neq` against a single type string

See §6.3 row entries.

---

## §10 — Other engine primitives

### §10.1 — `selectAutoFireCanvasForLocation` (`v2.py:3885`)

Walks all canvases tagged to a location. For each, calls `isCanvasValid`. Among valid + `is_repeatable = false` + (their flag-gates) canvases, picks highest priority. If found, REPLACES the hub render entirely. Once per matching condition (the flag-setter on exit retires the canvas).

This is the Lane 4 capstone entry point.

### §10.2 — `getStoryCanvasRedirect` (`v2.py:4272`)

Location-entry dispatcher. Checks all of: Lane 2 random encounters → Lane 4 capstones → falls through to hub render. Order matters: high-priority capstones win over Lane 2 randoms at the same location.

### §10.3 — Cooldown layers

| Layer | Function | Scope |
|---|---|---|
| 1 — Per-canvas | `canTriggerCanvas` (`v2.py:3621`) | Single canvas ID. Tracks `total`/`dayKey`/`dayCount` in `trigger_history[id]`. |
| 2 — Per-activity-name | `canTriggerActivity` (`v2.py:3661`) | Shared across same-`name` tier canvases. `activity_trigger_history[name]`. |
| 3 — Per-location random | `random_cooldowns[locId]` (Lane 2 only) | Visit-decremented integer. Set to 3 visits after a Lane 2 random fires. |

**Lane 3 substitutions inherit Layers 1 + 2 automatically via `markCanvasTriggered`; do NOT inherit Layer 3.** Doc 24 §8.

### §10.4 — Notifications + soft-fail

`<<Notification 'warning' "...">>` — toast banner. Used for time-of-day fails, threshold-publish on locked clicks (Doc 56 P2).

Per-choice `show_when_locked = true` + `locked_text = "..."` (+ optional `locked_text_threshold`) renders the choice greyed-out with a click-to-toast pattern. Doc 56 P7 — failure is information, not penalty. No stat drain on locked click.

### §10.5 — `<<NotifyCorruption N>>` (RTS-style)

UI-hint widget that toasts the required corruption level. **NOT a state mutator** — does not change `player.corruption`. Used in the ELSE branch of a corruption gate to publish the threshold transparently.

### §10.6 — `formatCanvasConditions` (`v2.py:7043`)

Renders condition blocks as human-readable strings for the published catalog + walkthrough. Each predicate type has its own formatter branch (e.g., `worn_type` → "Wearing swim" / "Not wearing schoolwear").

### §10.7 — Canvas `guide` field (Doc 56 R5)

**Status:** Doctrine-locked. Schema field NOT YET PARSED — Doc 62 PRD (currently HELD per Doc 66 §10). Authors should still include `guide = "..."` next to `name` and `description`; the validator will tolerate the field even before the dataclass adds it. When Doc 62 ships, every canvas's `guide` becomes the published-catalog recipe.

---

## §11 — Stage helpers + arc stages

### §11.1 — `[[stage_helpers]]`

Dataclass: `TemplateStageHelper` at `template_import.py:418`.

Named composite gates. Helpers reference primitive condition types ONLY — recursion (helper → helper) rejected at `validate()` time. Single-level lookup keeps cycle risk zero.

`dev_only = true` silences the unused-flag-setter validator for helpers used only by dev shortcuts.

Runtime registry: `setup.stage_helpers_map` at `v2.py:2641`.

### §11.2 — Arc stages declaration (per NPC)

```toml
[[npcs]]
id = "npc_frank"
arc_stages = [
  "neutral",
  "noticed",
  "caught",
  "first_night",
  "cracked",
  "sleepover",
]
```

These are display strings only. The CURRENT stage integer lives at `player.core_traits.frank_stage`. Engine recognizes the `<slug>_stage` trait name pattern at `v2.py:5183–5189`.

---

## §12 — Secondary primitives (brief)

For full schema, see `schema/02_toml_schema.md`. Listed here for cross-reference.

### §12.1 — `[[locations]]`

Dataclass: `TemplateLocation` at `template_import.py:135`. Fields: `id`, `name`, `description`, `entry_from` (parent for back-navigation), `entry_conditions`, `blocked_message`, image, ambient/menu fields.

### §12.2 — `[[trait_labels]]` + `[[flag_labels]]`

Dataclasses at `template_import.py:372` + `:386`. Map trait/flag keys to display names + descriptions for catalog / sidebar / debug surfaces.

### §12.3 — `[[passes]]`

Dataclass: `TemplatePass` at `template_import.py:570`. Recurring purchase items (gym membership, bus pass). Predicate type `"pass"` checks active state.

### §12.4 — `[[items]]`

Dataclass: `TemplateItem` at `template_import.py:579`. Inventory items. Predicate type `"item"` checks counts.

### §12.5 — `[[fast_jobs]]`

Dataclass: `TemplateFastJob` at `template_import.py:550`. Quick-job mechanic (income channel via single trait, not via separate channels — see `00_LEGACY_IGNORE.md` §3.4).

### §12.6 — `[[banks]]`

Dataclass: `TemplateBank` at `template_import.py:562`. Money mechanics (interest, transfers).

### §12.7 — `[[modifiers]]`

Dataclass: `TemplateModifierEffect` at `template_import.py:531`. Temporary state buffs/debuffs. Predicate type `"modifier"` checks `is_active`.

### §12.8 — `[[themes]]`

Dataclass: `TemplateTheme` at `template_import.py:587`. UI theme variants (visual register, not gameplay).

---

## §13 — Phone primitives (Doc 43 + 44 + 46)

Phone is an in-game device (purchase-gated via `pass = "phone_active"` per RTS pattern). Apps:
- **Messages** — chat threads with NPC reply effects + flag-setters + daily small-talk topics
- **Social feed** — post + comment pattern
- **Dating apps** — branching profile interactions
- (others — see `template_import.py:192–370` for full Phone dataclass set)

Dataclass: `TemplatePhone` at `template_import.py:286`. Subordinate: `TemplatePhoneApp`, `TemplatePhoneConversation`, `TemplatePhoneConversationBlock`, `TemplatePhonePost`, `TemplatePhoneProfile`, `TemplatePhoneDailyTopic`, `TemplatePhoneGalleryItem`.

---

## §14 — Validator hooks (the contract)

All validators live in `template_import.py` `validate()` function (entry: `template_import.py:2755`).

| Validator | What it catches | Severity |
|---|---|---|
| Predicate field-name typos | `subject` vs `targetType` etc. | warning (`_validate_predicate_field_names` at `:1098`) |
| Effect field-name typos | `trait_key` vs `trait` etc. | warning (`_validate_effect_field_names` at `:1077`) |
| Undeclared trait in sidebar | trait_words/trait_bar/trait_status_text references trait not in `core_traits` | **error** (`:2382–2547`) |
| Undeclared trait in effect (Doc 69 Item 4) | warning | (`_validate_trait_declaration_in_effect` at `:1274`) |
| Undeclared trait in predicate (Doc 69 Item 4) | warning | (`_validate_trait_declaration_in_predicate` at `:1351`) |
| `worn_type` typo / uncommon type (Doc 72) | warning / info | (`_validate_worn_type_items_block` at `:1168`) |
| Quest card R1–R4 (Doc 50) | error/warning | (`_validate_quests_cards` at `:4469`) |
| Weekday validation | error | (`_validate_weekdays` at `:1034`) |
| Stage helper recursion | error | inside `validate()` |
| (many others — full list out of scope here) | — | — |

Build proceeds on warnings; halts on errors.

---

## §15 — Reference card — one-line lookups

| Question | Answer |
|---|---|
| How does Lane 1 fire? | Player clicks NPC portrait at location → routes to canvas → `exit_block.choices` renders the hub menu |
| How does Lane 2 fire? | `checkRandomEncounters` rolls on location entry (`v2.py:4520`) |
| How does Lane 3 fire? | Player clicks solo activity → `checkAndSubstituteCanvas` rolls (`v2.py:4649`) → may preempt parent body |
| How does Lane 4 (capstone) fire? | `selectAutoFireCanvasForLocation` on location entry (`v2.py:3885`); priority ≥ 9 wins |
| How do I check player corruption? | `{ type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 15 }` |
| How do I check NPC stage? | `{ type = "trait", subject = "player", trait_key = "frank_stage", operator = "gte", value = 2 }` |
| How do I add 1 to player corruption? | `{ targetType = "player", trait = "corruption", op = "add", value = 1 }` |
| How do I set a flag? | `{ targetType = "player", flag = "frank_caught", op = "set" }` |
| How do I decay energy daily? | `[[engine.daily_tick.traitEffects]]` with `op = "add"`, `value = -10` |
| How do I make a Lane 3 substitution target? | Set `substitution_only = true` + `requires_npc = "npc_X"` + `max_triggers_per_day = 1` on its `TemplateTrigger` |
| How do I make a capstone? | `is_repeatable = false` (or `true` + `flag_is_false` self-gate) + `priority ≥ 9` + flag-setter on exit choice |
| How do I gate on what Maya's wearing? | `{ type = "worn_type", operator = "eq", value = "swim" }` (Doc 72) |

---

**End of file.** Next: `schema/02_toml_schema.md` for full per-section TOML field tables.

═══════════════════════════════════════════════════════════════════════════════

## 3. 02_toml_schema

**Source:** `prompts_v2/schema/02_toml_schema.md`

---

# Schema 02 — TOML Schema Reference

**Status:** Ground-truth TOML section reference. Extracted live from `apps/projects/services/template_import.py` dataclasses (43–956) + validator (2755+) on 2026-05-28.
**Authority:** Per-section field tables; minimal round-trip examples. Doctrine + behavior live in `schema/01_engine_capabilities.md` + `prompts_v2/doctrine/`.
**Purpose:** Reference card for emitting valid TOML. Author looks up "what fields does `[[canvases.trigger]]` accept?" and finds the table here.

**Convention:** Every section below shows the dataclass + the file:line in `template_import.py`. When a field's value drives a runtime feature, the cross-reference is to `schema/01_engine_capabilities.md`.

---

## §0 — Reading guide + reference card index

| Section | What lives there |
|---|---|
| §1 | `[project]` + `[time]` + `[settings]` |
| §2 | `[player]` + `[player.core_traits]` + customization |
| §3 | `[[npcs]]` + `[[npcs.schedules]]` + `[[npcs.core_traits]]` |
| §4 | `[[locations]]` |
| §5 | `[[canvases]]` — the big one |
| §6 | `[[canvases.trigger]]` + sub-sections (schedules, substitutions, pre_substitution_effects) |
| §7 | `[[canvases.nodes]]` + blocks vocabulary + `exit_block` + choices |
| §8 | `[[quest_cards]]` (V2 engine) |
| §9 | `[[sidebar_items]]` per-type tables |
| §10 | `[engine.daily_tick]` |
| §11 | `[[engine.stage_helpers]]` |
| §12 | `[[clothing]]` + `[settings.clothing_requirements]` + per-location `clothing_rules` |
| §13 | `[phone]` + sub-apps |
| §14 | Rent system — `[settings.rent]` (economic spine; engine RentDay flow) |
| §15 | Secondary sections (passes / items / fast_jobs / banks / themes / labels / tips_page) |
| §16 | Effect + predicate field reference (cross-ref to schema/01 §6) |
| §17 | Round-trip minimal-example for a complete RTS-shape sandbox |

---

## §1 — `[project]` + `[time]` + `[settings]`

### §1.1 — `[project]`

Dataclass: `TemplateProject` at `template_import.py:43`.

| Field | Type | Default | Notes |
|---|---|---|---|
| `slug` | str | required | URL-safe identifier |
| `title` | str | required | Display title |
| `description` | str | `""` | Free text |
| `quests_engine` | str | `"v1"` | **Set to `"v2"`** for RTS-shape games (enables `[[quest_cards]]`). PRD 48. |

```toml
[project]
slug = "the_long_summer"
title = "The Long Summer"
description = "A 90-day summer with Frank at the lake house."
quests_engine = "v2"
```

### §1.2 — `[time]`

Dataclass: `TemplateTime` at `template_import.py:54`.

| Field | Type | Default | Notes |
|---|---|---|---|
| `enabled` | bool | `true` | Whether the in-game clock runs |
| `starting_hour` | int | `8` | Hour 0–23 |
| `starting_day` | str | `"Monday"` | Day name |
| `starting_week` | int | `1` | Week counter at game start |

```toml
[time]
starting_hour = 8
starting_day = "Monday"
starting_week = 1
```

### §1.3 — `[settings]` — enable-switches (clothing / rent / phone)

The clothing, rent, and phone systems are turned on by keys the importer reads out of a **real
`[settings]` TOML table** — `settings_raw = data.get("settings", {})` (`template_import.py:2224`).
**These keys are NOT bare top-level keys.** Authoring them bare (e.g. directly after `[time]`) scopes
them under whatever table precedes them, `data["settings"]` comes back empty, and the system reads as
*disabled with no error* — a silent failure (this is exactly what shipped a dead clothing system once;
see `doctrine/11_clothing_design.md` §8). The working gold-standard `the_long_summer_test` puts them in
`[settings]` (`1_metadata_and_locations.toml:616`).

**Clothing** (`[settings]` keys, read at `template_import.py:2225-2227`):

| Field | Type | Default | Notes |
|---|---|---|---|
| `clothing_enabled` | bool | `false` | Activates `[[clothing]]` + wardrobe/shop pages. See §12. |
| `wardrobe_location` | str | — | Location slug where the wardrobe page is injected |
| `shop_location` | str | — | Location slug where the clothing shop page is injected |

```toml
[settings]
clothing_enabled  = true
wardrobe_location = "loc_mayas_room"
shop_location     = "loc_thrift_store"
```

`[settings.clothing_requirements]` (coverage gate) is covered in §12.2; per-location `clothing_rules` in
§12.3.

**Rent** lives in `[settings.rent]` (read at `template_import.py:2382` — the keys are `enabled` /
`amount` / `due_day` / …, NOT `rent_enabled` / `rent_amount`). See §14 for the full field table and
`doctrine/12_rent_economy_design.md` for the design model.

```toml
[settings.rent]
enabled       = true
amount        = 125
due_day       = "Friday"          # engine fires the due trigger on this weekday
collector_npc = "npc_vince"       # NPC slug; must exist in [[npcs]]
eviction_mode = "flag_set"        # or "game_end"
```

**Phone** lives in a top-level `[phone]` table (`data["phone"]`, key `enabled`, read at
`template_import.py:2394`). See §13. NOT under `[settings]` (that is clothing) and NOT a bare
`phone_enabled` key. All three enable-switches now read from their own table — none are bare keys under
`[time]`:

```toml
[settings]          # clothing
clothing_enabled = true
[settings.rent]     # rent
enabled = true
[phone]             # phone (top-level, NOT under [settings])
enabled = true
```

> ✅ **Resolved 2026-06-02 (was a known-issue):** older revisions of §13 showed `phone_enabled` as a
> *bare top-level key*. That was wrong the same way the bare clothing/rent keys were. Phone is read from a
> `[phone]` table. With this fixed, **no bare-key enable-switch docs remain** (clothing, rent, and phone
> all scope correctly).

`corruption_tiers` (`List[int]`, default `[0,5,15,30,45]`, per-band corruption thresholds) is a
top-level `GameTemplate` field — see §2 (player/customization) where corruption banding is documented.

---

## §2 — `[player]` + customization

Dataclass: `TemplatePlayer` at `template_import.py:81`.

### §2.1 — `[player]` fields

| Field | Type | Default | Notes |
|---|---|---|---|
| `id` | str | `"player"` | Internal identifier |
| `name` | str | `"Player"` | Display name (overridable via customization) |
| `description` | str | `""` | Free text |
| `portrait` | str | `""` | Image path relative to media folder |
| `core_traits` | dict | `{}` | **Required:** every trait used in game pre-declared with initial value |
| `flag_keys` | List[str] | `[]` | Pre-declared flag names |
| `customizable` | bool | `false` | When true, customization_fields render at game start |
| `trait_decay` | Dict[str, float] | `{}` | Per-trait daily decay (e.g., `{"hygiene": 10}`) |

### §2.2 — `[player.core_traits]`

**Critical:** every player trait referenced anywhere in the game MUST appear here with an integer initial value. Sidebar items referencing undeclared traits hard-fail; effects/conditions silently no-op. See `schema/01_engine_capabilities.md` §2.2 + `doctrine/09_trait_catalog.md` §2.5.

```toml
[player]
id = "player"
name = "Maya"
description = "20, escaped the city."
portrait = "maya.jpg"

[player.core_traits]
corruption = 0
arousal = 0
energy = 100
hygiene = 100
money = 80
# Per-NPC stage traits (one per NPC with an arc)
frank_stage = 0
ryan_stage = 0
jake_stage = 0
# Tier 2 player traits
fitness = 0
beauty = 0
exhibitionism = 0
intelligence = 0
```

### §2.3 — `[[player.customization_fields]]`

For `customizable = true`. The engine auto-builds a `CustomizeCharacters` screen at game
start and redirects `Start` to it (no author wiring). Each field renders there; the player's
choice writes into `$player.<id>`. **Array-of-tables — place these AFTER every `[player.*]`
subtable (e.g. `[player.core_traits]`), or TOML scopes them wrong.**

Dataclass: `TemplatePlayerCustomizationField` at `template_import.py:70`.

| Field | Type | Notes |
|---|---|---|
| `id` | str | Lowercase snake_case. **`id = "name"` is special → writes `$player.name`.** Other ids write `$player.<id>`. Reserved (rejected): `portrait`, `current_location`, `core_traits`, `flags`, `wardrobe`, `equipped` |
| `type` | str | `"text"`, `"select"`, or `"image_select"` |
| `label` | str | Display label |
| `default` | str | Initial value (for `select`/`image_select` must be a valid option/option-id) |
| `options` | List | For `select`: string list. For `image_select`: TemplatePlayerCustomizationOption list (`{id, image, label}`) |
| `sets_portrait` | bool | `image_select` only — selected image becomes `$player.portrait` |

**Output — the `@`-token (load-bearing):** a chosen value only *appears* in the story if you
write the prose with the substitution token. `@player` → the chosen name; `@player.<field>`
→ any field (e.g. `@player.build`). Tokens resolve in canvas prose, dialog body, choice text,
and location descriptions — **not** in structural labels (location names, sidebar/quest
labels). Full contract + the un-tokenizable-surface trap: **doctrine/14**.

```toml
[[player.customization_fields]]
id = "name"
type = "text"
label = "Your name"
default = "Maya"

[[player.customization_fields]]
id = "build"
type = "select"
label = "Build"
default = "average"
options = ["petite", "average", "curvy", "athletic", "thick"]

[[player.customization_fields]]
id = "look"
type = "image_select"
label = "Choose your look"
sets_portrait = true
options = [
  { id = "blonde", image = "maya_blonde.jpg", label = "Blonde" },
  { id = "brunette", image = "maya_brunette.jpg", label = "Brunette" },
]
# Then in prose: "@player tugs at her shirt, aware of her @player.build frame."
```

---

## §3 — `[[npcs]]` + `[[npcs.schedules]]`

Dataclass: `TemplateNPC` at `template_import.py:107`.

### §3.1 — `[[npcs]]` fields

| Field | Type | Default | Notes |
|---|---|---|---|
| `id` | str | required | Slug (e.g., `"npc_frank"`) |
| `name` | str | required | Display name |
| `description` | str | `""` | Free text |
| `portrait` | str | `""` | Image path |
| `core_traits` | dict | `{}` | **Required** when NPC has any trait references |
| `flag_keys` | List[str] | `[]` | Pre-declared NPC flag names |
| `schedules` | List[`TemplateNPCSchedule`] | `[]` | Location/time windows |
| `customizable` | bool | `false` | Player can rename at game start |
| `relationship` | Optional[str] | — | Default relationship label (e.g., `"step-brother"`) |
| `relationship_options` | List[str] | `[]` | Choices for relationship picker |
| `trait_decay` | Dict[str, float] | `{}` | Per-NPC trait daily decay |
| `hidden_from_ui` | bool | `false` | Omit from Guide / Stats / sidebar widget |
| `arc_stages` | List[str] | `[]` | Display strings for stage names. Length implies max stage value (len−1). |

**Customizable NPCs:** `customizable = true` lets the player rename the NPC and pick a
relationship label at game start. It **requires both** `relationship` (the default) **and**
`relationship_options` (the picker list), and the default must be in the options — the
importer hard-fails otherwise (`template_import.py:3289`). There is no rename-only mode.
Reference the customized values in prose with `@<npc_short>` (the slug minus `npc_`, e.g.
`@frank`) and `@<npc_short>.rel`. **Never bake a customizable NPC's name into a location
name, sidebar label, or quest title** — those print raw and won't honor the rename
(genericize them). See **doctrine/14**.

### §3.2 — `[[npcs.schedules]]` fields

Dataclass: `TemplateNPCSchedule` at `template_import.py:94`.

| Field | Type | Default | Notes |
|---|---|---|---|
| `location` | str | required | Location slug — resolved to UUID at build time |
| `weekdays` | List[int] | `[]` (all days) | 0 = Monday, 6 = Sunday |
| `start_time` | str | `"00:00"` | `HH:MM` 24-hour |
| `end_time` | Optional[str] | — | `HH:MM` 24-hour |
| `activity` | str | `""` | Author-side description |

Schedule entries should be NON-OVERLAPPING per NPC. Engine resolves NPC location via `getNpcLocation` (`v2.py:2923`) by scanning entries.

**Every schedule row needs a matching Lane 1 hub (D72-R6).** For each row, author a hub canvas for that NPC at that location whose `trigger.schedules` covers the row's window (period-split per window — separate hub per window, §6.2). The hub's rung ceiling follows the location's exposure tier (public/semi-private/private). A row with no live hub is dead presence; a hub-less system NPC (rent/phone-only) carries no schedule row. See `doctrine/04` §6.

**A row at a *locked* location (`entry_conditions`, §4) is a *deferred* hub promise** — the hub is dormant until the lock opens. Valid only under the unlock contract: the NPC is met at an OPEN on-ramp whose beat sets the unlock flag, and no NPC is reachable only via a locked location. Full Case A/B/C treatment in `doctrine/10` §5.4.

### §3.3 — Round-trip example

```toml
[[npcs]]
id = "npc_frank"
name = "Frank"
description = "50s, your landlord."
portrait = "frank.jpg"
arc_stages = [
  "neutral",
  "noticed",
  "caught",
  "first_night",
  "cracked",
  "sleepover",
]

[npcs.core_traits]
arousal = 0
corruption = 0
relation = 0

[[npcs.schedules]]
location = "loc_kitchen"
weekdays = [0, 1, 2, 3, 4]
start_time = "07:00"
end_time = "09:00"
activity = "Making coffee"

[[npcs.schedules]]
location = "loc_yard"
weekdays = [0, 1, 2, 3, 4]
start_time = "14:00"
end_time = "17:00"
activity = "Fixing fence"

[[npcs.schedules]]
location = "loc_living_room"
weekdays = [0, 1, 2, 3, 4]
start_time = "19:30"
end_time = "21:00"
activity = "Reading the paper"
```

---

## §4 — `[[locations]]`

Dataclass: `TemplateLocation` at `template_import.py:135`.

| Field | Type | Default | Notes |
|---|---|---|---|
| `id` | str | required | Slug |
| `name` | str | required | Display name |
| `description` | str | `""` | Free text |
| `image` | str | `""` | Image path |
| `image_search_queries` | List[str] | `[]` | For Missing Media page |
| `is_container` | bool | `false` | Pure-nav wrapper — SWALLOWS attached canvases (see below). Do NOT attach canvases to one. |
| `parent` | str | `""` | Structural nesting only (canvas inheritance) — NOT navigation. May differ from `entry_from`. |
| `entry_from` | str | `""` | Navigation parent. "Leave X" links to `X.entry_from`. A top-level root has none (bridge via walk activity). |
| `default_entry` | str | `""` | (containers only) child to auto-redirect into |
| `navigation_order` | List[str] | `[]` | Ordered child slugs. Each listed slug MUST have `entry_from` = this location, or the build rejects it ("not a destination"). |
| `entry_conditions` | dict | `{}` | `{version, items}` predicate block; deny entry when fails |
| `blocked_message` | str | `""` | Shown when `entry_conditions` fail |
| `clothing_rules` | List[dict] | `[]` | Per-location clothing gates |

**`is_container` SWALLOWS canvases.** A container passage renders ONLY the child menu (`v2.py:8800`) — it never calls getStoryCanvasRedirect/renderNpcPortraits/renderSoloActivities, so any canvas whose `trigger.location` is a container is silently DEAD. NEVER attach canvases to a container. Use a NON-container standing hub (carries `navigation_order` AND hosts canvases), or a wrapper + `default_entry` → a standing arrival child that holds the content. Full layering + reachability doctrine: `doctrine/10_location_design.md`.

```toml
[[locations]]
id = "loc_hallway"
name = "Hallway"
description = "The hallway between the bedrooms."
is_container = true
entry_from = ""
navigation_order = ["loc_mayas_room", "loc_franks_bedroom", "loc_kitchen", "loc_living_room", "loc_bathroom", "loc_yard"]

[[locations]]
id = "loc_franks_bedroom"
name = "Frank's Bedroom"
description = "His room. The bed is unmade."
image = "locations/franks_bedroom.jpg"
entry_from = "loc_hallway"
entry_conditions = { version = "1.0", items = [
  { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_true" },
] }
blocked_message = "Not yet. He hasn't invited me."
```

**Locking a location that hosts an NPC schedule — the unlock contract.** `entry_conditions` + `blocked_message` is a *visible-but-blocked* lock: the room shows on the nav and prints `blocked_message` on a failed entry (we have no native time-of-day location lock — the time/exposure axis lives on the hub via `trigger.schedules` + D72-R7). When a locked location also carries an NPC `[[npcs.schedules]]` row, coordinate them: write `blocked_message` to read as "haven't met / been invited" (not a mechanical "locked"), meet that NPC at an OPEN on-ramp location, and have that on-ramp beat set the unlock flag (so the flag has a reachable setter). Never make an NPC reachable *only* via a locked location, and never gate a door on a flag that's only settable behind that door. Full Case A/B/C treatment in `doctrine/10` §5.4; the RTS model this adapts is `reference/01` §6.5.

---

## §5 — `[[canvases]]`

The universal content primitive. Lane 1 / 2 / 3 / 4 are all implemented as canvases with different `trigger` field combinations. See `schema/01_engine_capabilities.md` §3 for lane fingerprints.

Dataclass: `TemplateCanvas` at `template_import.py:673`.

### §5.1 — Top-level fields

| Field | Type | Default | Notes |
|---|---|---|---|
| `id` | str | required | Slug |
| `name` | str | required | Display |
| `description` | str | `""` | Free text (author-side) |
| `trigger` | `TemplateTrigger` | — | See §6 |
| `nodes` | List[`TemplateNode`] | `[]` | See §7 |
| `connections` | List[`TemplateConnection`] | `[]` | Graph editor only — runtime ignores |
| `loop` | dict | `{}` | Loop config (advanced — see Frank bedroom sex loop) |

Note: `guide` field (Doc 56 R5) is doctrine-locked but schema-pending — Doc 62 PRD held. Authors should still emit `guide = "..."` next to `description`; the parser tolerates the field even before it becomes a parsed attribute.

---

## §6 — `[[canvases.trigger]]` and sub-sections

Dataclass: `TemplateTrigger` at `template_import.py:448`.

### §6.1 — Trigger fields

| Field | Type | Default | Notes |
|---|---|---|---|
| `location` | str | required | Location slug (the canvas anchors here) |
| `is_active` | bool | `true` | Soft on/off switch |
| `is_repeatable` | bool | `true` | Lane 1/2/3 = `true`. Lane 4 capstone = `false` (or `true` + flag-gate). |
| `max_triggers_per_day` | Optional[int] | — | Per-day cap. Lane 3 substitution targets typically `1`. |
| `priority` | int | `0` | Lane 4 capstones use ≥ 9. Tie-break in `selectAutoFireCanvasForLocation`. |
| `conditions` | dict | `{}` | `{version, logic, items: [...]}` — see §16 |
| `schedules` | List[`TemplateTriggerSchedule`] | `[]` | Per-canvas time windows — see §6.2 |
| `npc` | Optional[str] | — | NPC slug; navigation indicator |
| `trigger_mode` | str | `"manual"` | `"manual"` (Lane 1/3/4) or `"random"` (Lane 2) |
| `chance` | Optional[float] | — | 0.0–1.0; Lane 2 only |
| `costs` | List[dict] | `[]` | Resource costs on entry: `[{trait: str, value: int}]` |
| `show_when_blocked` | bool | `false` | Render grayed-out entry on QuestsPage when daily-cooldown blocks |
| `cooldown_message` | Optional[str] | — | Custom blocked text |
| `entry_only_from` | List[str] | `[]` | Lane 2 anti-toggle cooldown: only fire if previous location matched |
| `substitutions` | List[dict] | `[]` | Lane 3 dispatcher rules — see §6.3 |
| `substitution_only` | bool | `false` | Canvas only reachable via another canvas's substitution rule |
| `requires_npc` | Optional[str] | — | NPC presence gate — ANDs with all gates; engine consults `getNpcLocation` |
| `pre_substitution_effects` | List[dict] | `[]` | Pattern C — effects run before substitution check (Doc 69 Item 2) |

### §6.2 — `[[canvases.trigger.schedules]]`

Dataclass: `TemplateTriggerSchedule` at `template_import.py:441`.

| Field | Type | Notes |
|---|---|---|
| `weekdays` | List[int] | 0 = Monday … 6 = Sunday |
| `start_time` | str | `HH:MM` |
| `end_time` | Optional[str] | `HH:MM` |

**A Lane 1 hub renders only inside its OWN `schedules` window** (`isCanvasValid`, `v2.py:4356`) — not whenever the NPC happens to be present. So for presence coverage (D72-R6) the hub's `schedules` must span the matching `[[npcs.schedules]]` row. Where the NPC's presence at a location spans several windows, author one hub per window (period-split, D56-R1), each with its own `trigger.schedules`.

### §6.3 — `[[canvases.trigger.substitutions]]` (Lane 3)

Each entry is a free-form dict (not a dataclass — schema lives in `setup.checkAndSubstituteCanvas` runtime).

| Field | Type | Notes |
|---|---|---|
| `target_canvas_id` | str | Slug of the substitution target canvas (resolves to UUID at build) |
| `chance` | float | 0.0–1.0 fire probability. For Pattern B groups: cumulative bucket size within the group. |
| `conditions` | Optional[dict] | Extra `{version, items}` block (ANDs with target canvas's own gates) |
| `exclusive_group` | Optional[str] | Pattern B mutex group name (Doc 69 Item 1, 2026-05-27). Rules sharing this string share ONE dice; cumulative `chance` buckets; failed-condition in claimed slot falls to solo. Engine: `v2.py:4671-4713`. |

### §6.4 — `[[canvases.trigger.pre_substitution_effects]]` (Doc 69 Item 2)

Effects that run before the substitution check. Same shape as `TemplateChoiceEffect` (see §16): `{ targetType, npcId?, trait, op, value, clamp?, cap? }` — note no `type` field. Engine: `v2.py:11151`.

### §6.5 — Trigger examples per lane

**Lane 1 — Hub canvas (player clicks NPC portrait):**

```toml
[canvases.trigger]
location = "loc_franks_bedroom"
npc = "npc_frank"
trigger_mode = "manual"
is_repeatable = true
schedules = [{ weekdays = [0,1,2,3,4,5,6], start_time = "20:00", end_time = "23:00" }]
conditions = { version = "1.0", items = [
  { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_true" },
] }
```

**Lane 2 — Random ambient (dice on location entry):**

```toml
[canvases.trigger]
location = "loc_kitchen"
trigger_mode = "random"
chance = 0.25
is_repeatable = true
requires_npc = "npc_frank"
schedules = [{ weekdays = [0,1,2,3,4], start_time = "07:00", end_time = "09:00" }]
```

**Lane 3 — Parent activity (Maya picks Wash Dishes):**

```toml
[canvases.trigger]
location = "loc_kitchen"
trigger_mode = "manual"
is_repeatable = true
schedules = [{ weekdays = [0,1,2,3,4,5,6], start_time = "07:00", end_time = "21:00" }]

[[canvases.trigger.substitutions]]
target_canvas_id = "scene_frank_kitchen_dishes"
chance = 0.33
```

**Lane 3 — Substitution target (Frank walks in mid-chore):**

```toml
[canvases.trigger]
location = "loc_kitchen"
trigger_mode = "manual"
is_repeatable = true
max_triggers_per_day = 1
substitution_only = true
requires_npc = "npc_frank"
schedules = [{ weekdays = [0,1,2,3,4,5,6], start_time = "07:00", end_time = "21:00" }]
```

**Lane 4 — Capstone (auto-fire on location entry):**

```toml
[canvases.trigger]
location = "loc_living_room"
trigger_mode = "manual"
is_repeatable = false
priority = 10
schedules = [{ weekdays = [0,1,2,3,4], start_time = "19:30", end_time = "21:00" }]
conditions = { version = "1.0", items = [
  { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_false" },
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 25 },
] }
```

---

## §7 — `[[canvases.nodes]]` + blocks + exit_block

A canvas is composed of one or more `nodes`. Each node has a body (`blocks` list) + an `exit_block` (how it ends).

### §7.1 — `[[canvases.nodes]]`

Dataclass: `TemplateNode` at `template_import.py:654`.

| Field | Type | Default | Notes |
|---|---|---|---|
| `id` | str | required | Slug within the canvas |
| `name` | str | required | Display |
| `blocks` | List[dict] | `[]` | Body content — see §7.2 |
| `exit_block` | `TemplateExitBlock` | (default) | How the node ends — see §7.3 |
| `loop_terminal` | bool | `false` | For loop canvases — terminates the loop |
| `modifier_redirect` | Optional[dict] | — | `{modifier_key, node}` — if modifier active, render different node |

### §7.2 — Block vocabulary (`canvases.nodes.blocks`)

Each block is `{type = "X", ... type-specific fields}`. Supported types:

| `type` | Required fields | Notes |
|---|---|---|
| `"paragraph"` | `content` | Prose. RTS-flat default (Doc 30 §7.1). |
| `"dialog"` | `npcId` + `content` | Character dialogue. Speaker tag rendered. |
| `"thought_bubble"` | `content` | Maya interior (used sparingly). |
| `"image"` | `props.file` | Image asset. `props = { file, alt? }` |
| `"video"` | `props.file` | Video asset |
| `"clip"` | `props.file` | Looping clip |
| `"heading"` | `content` | Section heading |
| `"group"` | `props = { conditions, blocks }` | Tier-routed block group. `blocks` is a nested list. Inner blocks render only when conditions pass. |
| `"block_pool"` | `props = { variants: [...], pick: "random"|"sequential" }` | Pretext variation per Doc 30 Pattern E |
| `"cascade"` | `props = { beats: [...] }` | Linkreplace cascade — each beat unfolds on click |

**Group block (tier-routing) example:**

```toml
[[canvases.nodes.blocks]]
type = "group"
props.conditions = { items = [
  { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_false" },
] }
props.blocks = [
  { type = "image", props = { file = "scenes/kitchen_morning.jpg" } },
  { type = "paragraph", content = "Frank's at the counter. He looks up when you come in." },
  { type = "dialog", npcId = "npc_frank", content = "Morning." },
]
```

**Cascade block (RTS linkreplace) example:**

```toml
[[canvases.nodes.blocks]]
type = "cascade"
props.beats = [
  { advance_text = "Push the door open.", blocks = [
    { type = "paragraph", content = "The door swings. He's reading at the desk." },
  ]},
  { advance_text = "Step inside.", blocks = [
    { type = "dialog", npcId = "npc_frank", content = "Quiet." },
  ]},
  # ... more beats
]
```

### §7.3 — `[canvases.nodes.exit_block]`

Dataclass: `TemplateExitBlock` at `template_import.py:646`.

| Field | Type | Default | Notes |
|---|---|---|---|
| `type` | str | `"location"` | `"location"` or `"choices"` |
| `text` | str | `"Continue"` | Button label (for `type = "location"`) |
| `config` | dict | `{}` | For `type = "location"`: `{destinationType, locationId, time_progression_minutes}` |
| `choices` | List[`TemplateChoice`] | `[]` | For `type = "choices"`: the menu — see §7.4 |

**`type = "location"` (single return-to-location button):**

```toml
[canvases.nodes.exit_block]
type = "location"
text = "Return to the kitchen"
[canvases.nodes.exit_block.config]
destinationType = "specific"
locationId = "loc_kitchen"
time_progression_minutes = 10
```

**`type = "choices"` (multi-button hub menu — Lane 1):**

```toml
[canvases.nodes.exit_block]
type = "choices"

[[canvases.nodes.exit_block.choices]]
text = "Pour him coffee"
# ... (TemplateChoice fields — §7.4)
```

### §7.4 — `TemplateChoice` (exit_block.choices)

Dataclass: `TemplateChoice` at `template_import.py:609`.

| Field | Type | Default | Notes |
|---|---|---|---|
| `text` | str | `"Continue"` | Button label |
| `targetType` | str | `"trigger"` | `"trigger"` / `"location"` / `"node"` |
| `locationId` | Optional[str] | — | For `targetType = "location"` |
| `nodeId` | Optional[str] | — | For `targetType = "node"` (route to another node within same canvas, or `"canvas_id.node_id"` cross-canvas) |
| `time_progression_minutes` | Optional[int] | — | Time advance on click |
| `effects` | List[`TemplateChoiceEffect`] | `[]` | Trait effects — see §16 |
| `flagEffects` | List[`TemplateFlagEffect`] | `[]` | Flag effects — see §16 |
| `wardrobeEffects` | List[dict] | `[]` | `[{op: "equip"|"unequip", slot: str, item_id?: str}]` |
| `conditions` | dict | `{}` | Per-choice gating — `{version, items}` |
| `show_when_locked` | bool | `false` | Mode A: render greyed-out when conditions fail |
| `locked_text` | str | `""` | Tooltip/reason when locked |
| `locked_text_threshold` | str | `""` | S4 (RTS-style): toast text published on locked-click (e.g., `"30+ Corruption Needed"`) |
| `rejection_node` | Optional[str] | — | Mode B: route to rejection node on locked-click |
| `rejection_effects` | List[`TemplateChoiceEffect`] | `[]` | Effects on rejection-click |
| `modifier_effects` | List[`TemplateModifierEffect`] | `[]` | Temporary trait offset modifiers |
| `pass_effects` | List[dict] | `[]` | `[{pass_id, op}]` — pass purchase |
| `item_effects` | List[dict] | `[]` | `[{item_id, op, count}]` — inventory |
| `quest_effects` | List[dict] | `[]` | V1 quests — `[{quest, op, step?}]` |
| `schedule_effects` | List[dict] | `[]` | Delayed events — `[{delayDays, action, flag?/quest?/conversation?}]` |
| `text_variants` | List[dict] | `[]` | Per-state text — `[{text, conditions}]`; first match wins |

**Locked choice (always-show with threshold publish — RTS pattern):**

```toml
[[canvases.nodes.exit_block.choices]]
text = "Suck him"
show_when_locked = true
locked_text = "I need to know him better first"
locked_text_threshold = "Maya's corruption: 35+"
conditions = { items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 35 },
  { type = "flag", subject = "player", flag_key = "frank_cracked", operator = "is_true" },
] }
nodeId = "frank_bedroom_sex_loop"
effects = [
  { targetType = "player", trait = "corruption", op = "add", value = 1 },
  { targetType = "npc", npcId = "npc_frank", trait = "arousal", op = "add", value = 1, cap = 3 },
]
```

---

## §8 — `[[quest_cards]]` (V2 engine)

Activated by `[project].quests_engine = "v2"`. Dataclass: `QuestsCard` at `template_import.py:852`.

### §8.1 — `[[quest_cards]]` fields

| Field | Type | Default | Notes |
|---|---|---|---|
| `text` | str | `""` | Maya-voice narrative copy (climbing) |
| `ready_text` | Optional[str] | — | Maya-voice "moment is on her" line (when goals met) |
| `tip` | Optional[str] | — | Maya-voice interior observation |
| `npc_id` | Optional[str] | — | When set → renders in NPC section. When absent → top "Story Goals" section |
| `priority` | int | `0` | Tie-breaker |
| `group` | Optional[str] | — | Story Goals only — group key for crisis-variant collapse |
| `when` | List[`QuestsCondition`] | `[]` | Routing — ALL must eval true |
| `goals` | List[`QuestsCondition`] | `[]` | 🎯 To advance bullets |
| `ready_canvas` | Optional[str] | — | When all goals met AND set → 🔓 Ready frame |
| `terminal` | bool | `false` | When true AND `when` matches → ✓ Arc complete |

### §8.2 — `QuestsCondition` (used in `when` + `goals`)

Dataclass: `QuestsCondition` at `template_import.py:832`. Flat shape (NOT a `type` discriminator like trigger conditions).

| Field | Type | Notes |
|---|---|---|
| `flag` | Optional[str] | Flag gate — pair with `op` (`"is_true"` / `"is_false"`) |
| `trait` | Optional[str] | Trait gate — pair with `subject`, `op`, `value`, `label` |
| `subject` | Optional[str] | `"player"` or `"npc"` (trait gates only) |
| `npc_id` | Optional[str] | Required when `subject = "npc"` |
| `op` | str | `"is_true"`/`"is_false"` (flags); `"gte"`/`"lte"`/`"gt"`/`"lt"`/`"eq"` (traits) |
| `value` | Optional[float] | For trait gates |
| `label` | Optional[str] | For goals — text rendered next to ◯ bullet (e.g., `"Maya's corruption"`) |

### §8.3 — Examples (capstone + mechanic modes)

**Capstone card (Frank F4 — sleepover):**

```toml
[[quest_cards]]
npc_id = "npc_frank"
priority = 4
text = "He moved the line. The bedroom is the venue now."
ready_text = "Tonight I don't leave."
tip = "Diana down the hall. Quiet."
ready_canvas = "scene_frank_sleepover"
when = [
  { flag = "frank_cracked", op = "is_true" },
  { flag = "frank_sleepover_done", op = "is_false" },
]
goals = [
  { trait = "corruption", subject = "player", op = "gte", value = 50, label = "Maya's corruption" },
]
```

**Mechanic card (Ryan trust climb):**

```toml
[[quest_cards]]
# unlocks: ryan_yard_hub menu item "Help him in the yard" at trust >= 10
npc_id = "npc_ryan"
priority = 1
text = "He's around the yard most afternoons. I should make him notice me."
when = [
  { trait = "relation", subject = "npc", npc_id = "npc_ryan", op = "lt", value = 10 },
]
goals = [
  { trait = "relation", subject = "npc", npc_id = "npc_ryan", op = "gte", value = 10, label = "Ryan trust" },
]
# NO ready_canvas — mechanic mode. Threshold cross IS the unlock.
```

**Terminal card:**

```toml
[[quest_cards]]
npc_id = "npc_frank"
priority = 99
terminal = true
text = "It's the way it is now. Daddy's house. Daddy's bed. Diana down the hall."
when = [
  { flag = "diana_confronted", op = "is_true" },
]
```

See `doctrine/04_authoring_rules.md` for Doc 50 R1–R6 + Doc 56 R6.

---

## §9 — `[[sidebar_items]]`

Validator: `template_import.py:3024`+. Each entry is `{ type = "X", ... type-specific fields }`.

### §9.1 — `type = "trait_words"`

Banded prose label. Renders a band's text string; raw number hidden. Used for corruption (Pure / Lewd / Slutty / Whore).

| Field | Notes |
|---|---|
| `type` | `"trait_words"` |
| `trait` | Trait key (must be declared in `core_traits`) |
| `trait_owner` | `"player"` (default) or `"npc"` |
| `npc_id` | Required when `trait_owner = "npc"` |
| `label` | Display prefix (e.g., `"Corruption"`) — optional |
| `bands` | List of `{min, max, text, icon?}` |

```toml
[[sidebar_items]]
type = "trait_words"
trait = "corruption"
label = "Status"
bands = [
  { min = 0,  max = 24, text = "Pure",   icon = "✨" },
  { min = 25, max = 49, text = "Lewd",   icon = "💋" },
  { min = 50, max = 74, text = "Slutty", icon = "🔥" },
  { min = 75, max = 100, text = "Whore",  icon = "💦" },
]
```

### §9.2 — `type = "trait_bar"`

Numeric bar with optional band-text overlay + color tiers.

| Field | Notes |
|---|---|
| `type` | `"trait_bar"` |
| `trait` | Trait key |
| `trait_owner` | `"player"` (default) or `"npc"` |
| `npc_id` | Required when `trait_owner = "npc"` |
| `label` | Display label |
| `max` | Bar max value (default 100) |
| `hide_value` | When true, only the label renders (not `X / Y` numeric) |
| `color_tiers` | List of `{up_to, class}` — drives `.trait-bar-fill.<class>` CSS |
| `bands` | List of `{min, max, text, icon?}` — overlay text inside the bar |

```toml
[[sidebar_items]]
type = "trait_bar"
trait = "arousal"
label = "Arousal"
max = 10
color_tiers = [
  { up_to = 30,  class = "low" },
  { up_to = 70,  class = "medium" },
  { up_to = 100, class = "high" },
]
bands = [
  { min = 0,  max = 2,  text = "Cold" },
  { min = 3,  max = 5,  text = "Warm" },
  { min = 6,  max = 8,  text = "Hot" },
  { min = 9,  max = 10, text = "Burning" },
]
```

### §9.3 — `type = "trait_status_text"`

Banded body-state text. Renders nothing when no band matches (passive — no min/max value declared shows nothing). Used for hygiene/energy bands (Filthy/Dirty/Fresh/Clean).

| Field | Notes |
|---|---|
| `type` | `"trait_status_text"` |
| `trait` | Trait key |
| `trait_owner` | `"player"` (default) or `"npc"` |
| `npc_id` | Required when `trait_owner = "npc"` |
| `bands` | List of `{min, max, text, icon?}` — only matching band renders |

```toml
[[sidebar_items]]
type = "trait_status_text"
trait = "hygiene"
bands = [
  { min = 0,   max = 24,  text = "Filthy", icon = "🧫" },
  { min = 25,  max = 49,  text = "Dirty",  icon = "🌫️" },
  { min = 50,  max = 74,  text = "Fresh",  icon = "🪞" },
  { min = 75,  max = 100, text = "Clean",  icon = "🧼" },
]
```

### §9.4 — `type = "trait_decay_warning"`

Amber warning when a decaying trait dropped today AND is within range of a band gate. Sibling of `trait_status_text`.

| Field | Notes |
|---|---|
| `type` | `"trait_decay_warning"` |
| `trait` | Trait key |
| `threshold` | Numeric threshold within which the warning fires |
| `text` | Display string |

### §9.5 — Other sidebar types

| Type | Notes |
|---|---|
| `"passes"` | Renders all active passes (e.g., gym, bus) |
| `"inventory"` | Renders inventory items |
| (others) | See validator at `template_import.py:3000+` |

**Visibility doctrine (Doc 68 §8):** stage NEVER surfaces to any sidebar item. Antagonist awareness NEVER surfaces. Body-state (energy + hygiene) MUST surface. See `doctrine/09_trait_catalog.md` §8 for per-arc-shape defaults.

**No per-NPC sidebar item via `trait_bar` / `trait_words`.** Although these accept a `trait_owner`/`npc_id`, the engine resolves the `trait` against `player.core_traits` — so `type="trait_bar" npc_id="npc_x" trait="relation"` HARD-FAILS at build ("trait 'relation' not found in player.core_traits") or silently renders the PLAYER's stat. NPC progression (arousal / relation / stage) surfaces on the **Quests page** (V2 cards), NOT the sidebar. The only per-NPC sidebar item is the Doc-64 `npc_location` type, which is PENDING — do not emit it yet. (Late Shifts build failed on four npc-scoped `trait_bar`s.)

---

## §10 — `[engine.daily_tick]`

Dataclass: `TemplateDailyTick` at `template_import.py:404`.

Effects that fire once per in-game day at `advanceDay()` rollover.

| Field | Type | Notes |
|---|---|---|
| `flagEffects` | List[`TemplateFlagEffect`] | Clear/set daily-cooldown flags (silent) |
| `traitEffects` | List[`TemplateChoiceEffect`] | Per-day trait deltas. Each reuses the choice-effect shape (`targetType`/`npcId`/`trait`/`op`/`value`/`clamp`/`cap`). Optional per-entry `conditions` block. |

```toml
[engine.daily_tick]
flagEffects = [
  { targetType = "player", flag = "talked_to_ryan_today", op = "unset" },
]
traitEffects = [
  { targetType = "player", trait = "hygiene", op = "add", value = -10 },
  { targetType = "player", trait = "arousal", op = "add", value = 1, cap = 10 },
  { targetType = "npc", npcId = "npc_frank", trait = "arousal", op = "add", value = 1, cap = 3 },
  { targetType = "npc", npcId = "npc_jake", trait = "arousal", op = "add", value = 1, cap = 3 },
]
```

**Doctrine constraint (Doc 40 / Doc 68 §3–§4):** body-state (`hygiene`, `energy`) decays daily. Progression traits (`corruption`, `arousal`, `relation`, `stage`) do NOT decay daily. NPC arousal climbs daily (no-decay rule per Doc 40).

---

## §11 — `[[engine.stage_helpers]]`

Dataclass: `TemplateStageHelper` at `template_import.py:418`.

Named composite gates. A `type = "stage"` condition references a helper by name; engine recursively evaluates the helper's `conditions` block.

| Field | Type | Default | Notes |
|---|---|---|---|
| `name` | str | required | Helper identifier |
| `description` | str | `""` | Author-side |
| `conditions` | dict | `{}` | `{version, items}` — primitive types only (no helper → helper recursion) |
| `dev_only` | bool | `false` | Silences flag-setter-coverage validator warning (helpers used only by dev shortcuts) |

```toml
[[engine.stage_helpers]]
name = "frank_stage_2_plus"
description = "Frank reached Stage 2 (post-catch)."
conditions = { items = [
  { type = "trait", subject = "player", trait_key = "frank_stage", operator = "gte", value = 2 },
] }
```

---

## §12 — `[[clothing]]` + `[settings.clothing_requirements]` + per-location `clothing_rules`

Dataclass: `TemplateClothingItem` at `template_import.py:164`.

**Enabling the system (do this first).** The clothing system is OFF unless `[settings]` turns it on
(§1.3). The three switches live in the `[settings]` table — NOT as bare keys — and the items live in a
top-level `[[clothing]]` array:

```toml
[settings]
clothing_enabled  = true
wardrobe_location = "loc_mayas_room"     # wardrobe page injected at this location
shop_location     = "loc_thrift_store"   # shop page injected at this location
```

`clothing_enabled = true` with zero `[[clothing]]` items is a silent no-op (empty wardrobe/shop pages,
all `worn_*` predicates read 0) — the importer does NOT warn. Always author a full starting outfit. For
the *design* of the catalog + what `worn_*` should gate, see `doctrine/11_clothing_design.md`.

### §12.1 — `[[clothing]]`

| Field | Type | Default | Notes |
|---|---|---|---|
| `id` | str | required | Slug |
| `name` | str | required | Display |
| `slot` | str | required | Must be in `VALID_CLOTHING_SLOTS` = `{"bra", "underwear", "top", "bottom", "dress", "legwear", "shoes"}` |
| `image` | str | `""` | Image path |
| `initial` | bool | `false` | Player starts with this item |
| `conditions` | dict | `{}` | v1.0 conditions for wearing |
| `price` | int | `0` | Dollars; 0 = free/initial |
| `beauty` | int | `0` | Beauty contribution (worn_beauty reads MAX) |
| `corruption` | int | `0` | Content-router stat (worn_corruption reads MAX). **Does NOT mutate `player.corruption`.** |
| `type` | str | `""` | Outfit category (`"swim"`, `"casual"`, etc.). Read by `worn_type` predicate (Doc 72). |

Recommended type values (typo-catch reference set; any string accepted): `casual`, `swim`, `costume`, `schoolwear`, `fitness`, `uniform`, `sleepwear`.

```toml
[[clothing]]
id = "starter_outfit"
name = "Jeans and a tee"
slot = "top"
initial = true
beauty = 5
corruption = 0
type = "casual"

[[clothing]]
id = "bikini_top"
name = "Yellow bikini top"
slot = "top"
price = 25
beauty = 8
corruption = 15
type = "swim"
```

### §12.2 — `[settings.clothing_requirements]`

Dataclass: `TemplateClothingRequirements` at `template_import.py:180`. Lives under `[settings]` (read at
`template_import.py:2250`), like the enable switches.

| Field | Type | Default | Notes |
|---|---|---|---|
| `body_coverage` | bool | `true` | Must wear (top + bottom) OR dress |
| `always_required` | List[str] | `[]` | Slots that can never be removed |
| `conditional` | Dict[str, Dict[str, str]] | `{}` | `{slot: {until_flag, message}}` — slot required until flag set |

```toml
[settings.clothing_requirements]
body_coverage   = true
always_required = []
```

### §12.3 — per-location `clothing_rules` (the coverage gate)

A `[[locations]]` block may carry `clothing_rules` (§4) — a list of gates that block *entering* that
location while underdressed. Runtime: `checkLocationClothing` (`v2.py:1407`) walks the list and enforces
the **first rule whose `conditions` are satisfied**; a rule with no `conditions` always applies. A
`dress` satisfies both `top` and `bottom`.

| Rule field | Type | Notes |
|---|---|---|
| `slots_required` | List[str] | Slots that must be filled to pass. **Must be non-empty** — the validator rejects `[]` (`template_import.py:3460`). |
| `conditions` | dict | Optional v1.0 conditions; the rule only applies when they hold. Omit = always applies. |
| `message` | str | Shown when the player is blocked. |

**Conditional coverage (RTS "go out underdressed once corrupt enough" pattern).** Gate the cover-up rule
on a corruption ceiling: below the threshold she must cover up; at/above it the rule's condition fails,
no rule matches, and `checkLocationClothing` returns null (she leaves freely). Do this with a **single
rule carrying a `conditions` block** — do NOT try an empty-`slots_required` fallback rule (the validator
rejects empty slots):

```toml
[[locations]]
id = "loc_main_street"
# … entry_from, navigation_order …
clothing_rules = [
  { slots_required = ["top", "bottom"], message = "She can't head out half-dressed.", conditions = { version = "1.0", items = [
      { type = "trait", subject = "player", trait_key = "corruption", operator = "lt", value = 50 },
    ] } },
]
```

See `doctrine/11_clothing_design.md` §6 for the design rationale (coverage gates on global corruption
LEVEL, not pure slots).

---

## §13 — `[phone]`

A **top-level `[phone]` table with `enabled = true`** activates the phone (read at
`template_import.py:2394` — `phone_raw = data.get("phone")`; `enabled` defaults **`true`** when the table
is present). There is **NO bare `phone_enabled` key** — that form is dead config the importer never reads
(the §1.3 scoping trap). Dataclass tree: `TemplatePhone` at `template_import.py:286` (sub-apps in §13.2+).
The *design* model — app-type choice, thread/photo-action patterns, the purchase-gate beat — is in
`doctrine/13_phone_design.md`; this section is the schema. Gold-standard worked example: schema/03 §14.

### §13.1 — `[phone]` top-level

| Field | Type | Default | Notes |
|---|---|---|---|
| `enabled` | bool | `true` | Master on/off |
| `purchase_flag` | str | `""` | Sidebar button hidden until this flag is true |

### §13.2 — `[[phone.apps]]`

Dataclass: `TemplatePhoneApp` at `template_import.py:192`. Valid types: `"chat"`, `"social_feed"`, `"gallery"`, `"dating"`, `"custom"`, `"quests"`, `"fast_jobs"`, `"bank"`.

| Field | Type | Notes |
|---|---|---|
| `id` | str | Slug |
| `type` | str | one of valid types |
| `label` | str | Display name |
| `icon` | str | Image path |
| `post_actions` | List[dict] | `social_feed` only — `[{label, corruption_min?, followers_min, followers_max, daily_cap?, counter_trait}]` |

### §13.3 — `[[phone.conversations]]` (chat thread)

Dataclass: `TemplatePhoneConversation` at `template_import.py:216`.

| Field | Type | Notes |
|---|---|---|
| `id` | str | Slug |
| `app` | str | App slug |
| `npc` | str | NPC slug |
| `trigger` | dict | conditions block — when does this conversation become available |
| `blocks` | List[`TemplatePhoneConversationBlock`] | Thread structure |
| `notify` | str | Toast text on delivery (default `"📱 New message"`) |

**Trigger condition vocabulary (source-verified vs `triggerConditionsSatisfied`, v2.py:3308 — the
evaluator the phone, posts, profiles, and daily_topics all use).** Supported `items[].type`:
`flag` · `trait` · `days_since_flag` · `pass` · `item` · `stage` · `quest` · `corruption_level` ·
`modifier` · `clothing_slot` · `clothing_item` · `worn_beauty` · `worn_corruption` · `worn_type`.
**NOT supported: `day`, `time`, `weekday`, `location`, `random`** (those exist only in the *canvas*
trigger path, not here). So a phone thread cannot fire on day-of-week; use `flag` or `days_since_flag`
(fires N days after a flag's `set_day`) for time-relative delivery. Shape:
`conditions = { version = "1.0", logic = "AND"|"OR", items = [ {type="flag", subject="player", flag_key, operator="is_true"|"is_false"}, {type="trait", subject="player"|"npc", trait_key, operator="gte"|..., value, npc_id?}, {type="days_since_flag", subject="player", flag_key, operator="gte", value} ] }`.

### §13.4 — `[[phone.conversations.blocks]]`

Dataclass: `TemplatePhoneConversationBlock` at `template_import.py:203`.

| Field | Type | Notes |
|---|---|---|
| `type` | str | `"message"` (NPC sends) or `"reply"` (player chooses) |
| `sender` | str | `"npc"` or `"player"` (for message type) |
| `content` | str | Message body |
| `after_reply` | bool | Show after the preceding reply was picked |
| `choices` | List[dict] | For reply type — `[{text, effects, flagEffects, conditions, schedule_effects}]` |
| `round` | Optional[int] | Multi-round conversation: which round (1, 2, 3…) |
| `after_round` | Optional[int] | Show only after this round answered |
| `after_choice` | Optional[int] | Show only if this choice picked in `after_round` |

### §13.5 — `[[phone.posts]]` (social_feed)

Dataclass: `TemplatePhonePost` at `template_import.py:228`.

| Field | Type | Notes |
|---|---|---|
| `id` | str | Slug |
| `app` | str | App slug (`social_feed` type) |
| `npc` | str | NPC slug (empty for stranger posts) |
| `poster_name` | str | Display name for non-NPC posters |
| `image` | str | Image path |
| `caption` | str | Post text |
| `likes` | int | Like count display |
| `trigger` | dict | Conditions for visibility |
| `notify` | str | Toast text (default `"📱 New post"`) |

### §13.6 — `[[phone.profiles]]` (dating app)

Dataclass: `TemplatePhoneProfile` at `template_import.py:244`.

| Field | Notes |
|---|---|
| `id`, `app`, `npc` | identifiers |
| `photos` | List[str] image paths |
| `bio`, `age`, `interests` | display fields |
| `trigger` | conditions for profile availability |
| `match_condition` | conditions for "match" (NPC swipes back) |

### §13.7 — `[[phone.daily_topics]]`

Dataclass: `TemplatePhoneDailyTopic` at `template_import.py:258`. Per-NPC daily small-talk + photo actions.

| Field | Notes |
|---|---|
| `id`, `npc` | identifiers |
| `player_message` | What Maya sends |
| `npc_response` | NPC reply |
| `effects` | List of trait/flag effects on send |
| `conditions` | Visibility gating |
| `image` | Photo-action: media path rendered as sent photo |
| `corruption_min` | Lock until player corruption ≥ this |
| `cooldown` | `"per_topic"` = per-topic daily cap; default = per-NPC daily cap |

### §13.8 — `[[phone.gallery_items]]`

Dataclass: `TemplatePhoneGalleryItem` at `template_import.py:276`.

| Field | Notes |
|---|---|
| `id`, `image`, `caption` | display |
| `trigger` | Visibility gate |
| `link` | Optional passage to open on click |

---

## §14 — Rent system — `[settings.rent]`

Rent is the recurring economic-pressure system: it intercepts the player on its due day, demands payment,
and on repeated failure either ends the game or sets a flag. It lives in a **`[settings.rent]` table**
(read at `template_import.py:2382` — `rent_raw = settings_raw.get("rent", {})`). The keys are `enabled` /
`amount` / etc. — **NOT** `rent_enabled` / `rent_amount`. Authoring them bare scopes them under the wrong
table, `data["settings"]["rent"]` comes back empty, and rent reads as disabled with no error (the §1.3
silent-failure trap — this is exactly what shipped a dead rent system in Late Shifts). The *design* model
— when to use rent, the eviction-mode choice, the arm-after pattern, budget math — is in
`doctrine/12_rent_economy_design.md`; this section is the schema.

### §14.1 — Fields (`[settings.rent]`)

| Field | Type | Default | Notes |
|---|---|---|---|
| `enabled` | bool | `false` | Master switch. |
| `amount` | int | `0` | Rent per period. Validator: must be > 0 when enabled. |
| `due_day` | str | `"Monday"` | Weekday rent comes due (full name `"Monday"`…`"Sunday"`). The engine arms the due trigger when the in-game day rolls over TO this weekday — once per week. (Pre-2026-06-01 the engine ignored `due_day` and always fired Monday; it now respects it.) |
| `collector_npc` | str | `""` | NPC slug who collects (name + portrait shown on RentDay). Validator: must exist in `[[npcs]]`. Empty → generic "the landlord". |
| `grace_periods` | int | `1` | How many times the player may come up short before eviction fires. Each short period consumes one and clears that period's due flag. Validator: >= 0. |
| `start_after_flag` | str | `""` | Rent stays dormant until this flag is set — use it to keep onboarding rent-free (arm rent only once the player has income). Empty → rent arms from the first due day. |
| `eviction_mode` | str | `"game_end"` | `"game_end"` → GAME OVER + restart. `"flag_set"` → fail-forward (sets `eviction_flag`, play continues). Validator: one of these two. |
| `eviction_flag` | str | `"rent_evicted"` | Flag set when `eviction_mode = "flag_set"` and grace is exhausted. Validator: lowercase snake_case; auto-registered on the player. |
| `text` | table | `{}` | Override strings for the RentDay passages (§14.3). Author as a **`[settings.rent.text]` sub-table**, NOT a multi-line inline table (those break `tomllib`). |

### §14.2 — Runtime flow (what the engine generates)

State: `$game_state.rent_state = { last_paid_week, warnings, is_due }`. On each day rollover, if the new
weekday == `due_day` and `start_after_flag` (if set) is satisfied, `is_due` is set. While `is_due`, a
render intercept redirects the player to the `RentDay` passage:

- **Can pay** (`money >= amount`) → debit, clear `is_due`, reset warnings → `RentDay_Paid`.
- **Can't pay** → `RentDay_Short`: if `warnings < grace_periods`, a warning fires, `warnings += 1`,
  `is_due` clears (the period is survived). Once grace is exhausted, eviction fires per `eviction_mode`.

The engine does **not** set a "first rent paid" flag. If downstream content needs one, set it from a
hand-authored first-rent capstone (the hybrid pattern — `doctrine/12`).

### §14.3 — `[settings.rent.text]` keys (the REAL set)

All optional; each has an engine default. The RentDay title renders as `<title> — Rent Day`.

| Key | Passage | Used when |
|---|---|---|
| `title`, `scene`, `greeting` | RentDay | the knock + the demand |
| `cant_pay` | RentDay | the "I'm short" choice label |
| `paid_scene`, `paid_response`, `paid_closing` | RentDay_Paid | after paying |
| `warning_scene`, `warning_response`, `warning_closing` | RentDay_Short | short, still within grace |
| `eviction_scene`, `eviction_response`, `eviction_closing` | RentDay_Short | grace exhausted, `game_end` |
| `eviction_scene_soft`, `eviction_response_soft`, `eviction_closing_soft` | RentDay_Short | grace exhausted, `flag_set` (falls back to the non-`_soft` keys if unset) |

> The old corpus listed `rent_text` keys as `{paid, late, evicted, due_warning}` — **none of those exist**.
> Use the keys above (verified against `v2.py:14242–14379`).

See `schema/03_example_toml.md` §13 for a verbatim worked `[settings.rent]` + `[settings.rent.text]` block.

---

## §15 — Secondary sections

### §15.1 — `[[passes]]` (recurring purchases)

Dataclass: `TemplatePass` at `template_import.py:570`.

| Field | Type | Notes |
|---|---|---|
| `id` | str | Slug |
| `name` | str | Display |
| `cost` | int | Purchase price |
| `duration_days` | int | Validity period |
| `icon` | str | Image path |

### §15.2 — `[[items]]` (inventory consumables)

Dataclass: `TemplateItem` at `template_import.py:579`.

| Field | Type | Notes |
|---|---|---|
| `id` | str | Slug |
| `name` | str | Display |
| `icon` | str | Image path |
| `max_stack` | int | Inventory cap per item |

### §15.3 — `[[fast_jobs]]`

Dataclass: `TemplateFastJob` at `template_import.py:550`. Phone-app-driven repeatable money jobs.

| Field | Type | Notes |
|---|---|---|
| `id` | str | Slug |
| `name` | str | Display |
| `income` | int | Dollars per shift |
| `xp_req` | int | Fast-jobs XP needed to unlock |
| `cooldown_days` | int | Days locked after working |
| `time_period` | str | Optional `game.time` gate (e.g. `"M"`, `"A"`) |
| `money_trait` | str | Trait that accumulates (default `"money"`) |

### §15.4 — `[bank]`

Dataclass: `TemplateBank` at `template_import.py:562`.

| Field | Type | Notes |
|---|---|---|
| `enabled` | bool | Master |
| `interest_rate` | float | Daily compound rate (e.g., `0.01`) |
| `money_trait` | str | Money trait name (default `"money"`) |

### §15.5 — `[theme]`

Dataclass: `TemplateTheme` at `template_import.py:587`. UI theme — colors + fonts + border-radius + optional custom CSS.

| Field | Default |
|---|---|
| `mode` | `"light"` (or `"dark"`) |
| `primary`, `secondary`, `accent`, `success`, `danger`, `warning` | hex colors |
| `font_heading`, `font_mono` | CSS font strings |
| `border_radius` | CSS length |
| `bg`, `surface`, `surface_alt`, `border`, `text`, `text_muted` | auto-derived if empty |
| `custom_css` | freeform |

### §15.6 — `[[trait_labels]]` + `[[flag_labels]]`

Dataclasses: `TemplateTraitLabel` at `template_import.py:372`, `TemplateFlagLabel` at `template_import.py:386`.

Map internal trait/flag names to player-facing labels used by `setup.computeHintGoal` when auto-rendering 🎯 goal blocks.

```toml
[[trait_labels]]
key = "corruption"
label = "Maya's corruption"
verb = "reach"
unit = ""

[[trait_labels]]
key = "relation"
label = "Ryan trust"
verb = "reach"
unit = ""

[[flag_labels]]
key = "frank_caught"
label = "Caught by Frank"
```

### §15.7 — `[ui.tips_page]`

Dataclass: `TemplateTipsPage` at `template_import.py:393`. Standalone game-mechanics page. Engine prints `content` verbatim (raw HTML).

| Field | Notes |
|---|---|
| `title` | Default `"Tips"` |
| `content` | Raw HTML body |

---

## §16 — Effect + predicate field reference (the field-name minefield)

**Inline-table formatting (tomllib 1.0 hard rule):** an inline table `{ … }` must NOT wrap across lines — keys stay on the opening line and a closing `] }` stays on ONE line. `{ advance_text = "…", blocks = [ … ] },` is valid; splitting `advance_text` onto its own line, or putting `]` and `}` on separate lines, raises "Unclosed inline table" and the build fails. Only `[table]` / `[[array.of.tables]]` headers may span lines, never inline `{ }`. (Cost a repair pass in Late Shifts.)

See `schema/01_engine_capabilities.md` §6 for full behavior. This is the reference card.

### §16.1 — Trait EFFECT (mutation)

Dataclass: `TemplateChoiceEffect` at `template_import.py:503`.

```toml
{ targetType = "player", trait = "corruption", op = "add", value = 1 }
{ targetType = "npc", npcId = "npc_frank", trait = "relation", op = "add", value = 2 }
{ targetType = "player", trait = "arousal", op = "set", value = 0 }   # climax reset
{ targetType = "player", trait = "energy", op = "add", value = -10 }  # decay via negative
```

| Field | Required | Notes |
|---|---|---|
| `targetType` | yes | `"player"` or `"npc"` |
| `npcId` | when `targetType = "npc"` | NPC slug |
| `trait` | yes | trait name (NOT `trait_key`) |
| `op` | yes | `"add"` or `"set"` — no `"sub"` |
| `value` | yes | integer |
| `clamp` | no | floor at 0 |
| `cap` | no | upper bound |
| `conditions` | no | gate this effect (only applies if conditions pass) |

### §16.2 — Flag EFFECT

Dataclass: `TemplateFlagEffect` at `template_import.py:521`.

```toml
{ targetType = "player", flag = "frank_caught", op = "set" }
{ targetType = "npc", npcId = "npc_frank", flag = "secret_known", op = "set" }
{ targetType = "player", flag = "talked_to_ryan_today", op = "unset" }
{ targetType = "player", flag = "scandal_visible", op = "toggle" }
```

| Field | Required | Notes |
|---|---|---|
| `targetType` | yes | `"player"` or `"npc"` |
| `npcId` | when `targetType = "npc"` | NPC slug |
| `flag` | yes | flag name (NOT `flag_key`) |
| `op` | yes | `"set"`, `"unset"`, or `"toggle"` |
| `conditions` | no | gate the effect |

### §16.3 — Trigger / canvas PREDICATE (condition gate)

The `{version, logic, items: [...]}` block on `[canvases.trigger.conditions]`, `[canvases.exit_block.choices.conditions]`, `[locations.entry_conditions]`, etc.

```toml
[canvases.trigger.conditions]
version = "1.0"
logic = "AND"   # or "OR"; default "AND"
items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 15 },
  { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_true" },
  { type = "worn_type", operator = "eq", value = "swim" },
]
```

**Supported `type` values** (from `triggerConditionsSatisfied` at `v2.py:3275+`):

| `type` | Required fields | Operators |
|---|---|---|
| `"flag"` | `subject`, `flag_key` | `is_true`, `is_false`, `exists` |
| `"modifier"` | (impl) | `is_active` |
| `"trait"` | `subject`, `trait_key`, `operator`, `value` | numeric: `eq`/`ne`/`gt`/`gte`/`lt`/`lte`; set: `in`/`not_in`; existence: `exists`/`not_exists` |
| `"days_since_flag"` | `subject`, `flag_key`, `operator`, `value` | numeric |
| `"clothing_slot"` | `slot`, `operator` | `equipped`, `unequipped` |
| `"clothing_item"` | `item_id`, `operator` | `equipped`, `unequipped`, `owned`, `not_owned` |
| `"worn_beauty"` | `operator`, `value` | numeric |
| `"worn_corruption"` | `operator`, `value` | numeric |
| `"worn_type"` | `operator`, `value` | `eq`, `neq` |
| `"pass"` | `pass_id`, `operator` | `is_active` |
| `"item"` | `item_id`, `operator`, `value` | numeric |
| `"stage"` | `helper`, `operator` | resolves named helper, recursively evaluates |
| `"quest"` | (V2 quests engine) | quest-state predicate |
| `"corruption_level"` | `operator`, `value` | banded check |

`subject` values: `"player"` or `"npc"`. When `"npc"`, requires `npc_id`.

### §16.4 — Field-name reference card

| Concept | EFFECT field | PREDICATE field |
|---|---|---|
| Player vs NPC | `targetType` | `subject` |
| NPC identifier | `npcId` | `npc_id` |
| Trait name | `trait` | `trait_key` |
| Flag name | `flag` | `flag_key` |
| Operation | `op` | `operator` |
| Type discriminator | (dispatched by `trait` vs `flag` field presence) | `type` (required) |

**Mixing effect + predicate field names silently no-ops with NO build error.** Validators at `template_import.py:1077` + `:1098` catch some cases as warnings, not all.

### §16.5 — Quest card condition shape (different from trigger condition!)

Quest card `when` + `goals` use the FLAT `QuestsCondition` shape (NOT a `type` discriminator):

```toml
{ flag = "frank_caught", op = "is_true" }
{ trait = "corruption", subject = "player", op = "gte", value = 25, label = "Maya's corruption" }
{ trait = "relation", subject = "npc", npc_id = "npc_ryan", op = "gte", value = 10, label = "Ryan trust" }
```

vs trigger conditions which use the typed shape:

```toml
{ type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_true" }
{ type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 25 }
```

**Two different shapes for the same semantic.** Match the shape to the consumer (`[[quest_cards]]` uses flat; everything else uses typed).

---

## §17 — Minimal round-trip example

A complete RTS-shape sandbox skeleton — copy-paste starting point. Trim/expand to game scope. References every section above.

```toml
schema_version = "1.0"

[project]
slug = "test_game"
title = "Test Game"
description = "Minimal RTS-shape sandbox skeleton."
quests_engine = "v2"

[time]
starting_hour = 8
starting_day = "Monday"
starting_week = 1

# Clothing switches live in the [settings] TABLE (read from data["settings"]),
# NOT as bare keys — see §1.3. (rent → [settings.rent], phone → [phone].)
[settings]
clothing_enabled = true
wardrobe_location = "loc_mayas_room"
shop_location = "loc_thrift_store"

# ---- Player ----
[player]
id = "player"
name = "Maya"
portrait = "maya.jpg"

[player.core_traits]
corruption = 0
arousal = 0
energy = 100
hygiene = 100
money = 80
fitness = 0
beauty = 0
exhibitionism = 0
intelligence = 0
frank_stage = 0

# ---- NPCs ----
[[npcs]]
id = "npc_frank"
name = "Frank"
arc_stages = ["neutral", "caught", "first_night", "cracked"]

[npcs.core_traits]
arousal = 0
corruption = 0
relation = 0

[[npcs.schedules]]
location = "loc_kitchen"
weekdays = [0,1,2,3,4]
start_time = "07:00"
end_time = "09:00"

# ---- Locations ----
[[locations]]
id = "loc_hallway"
name = "Hallway"
is_container = true

[[locations]]
id = "loc_kitchen"
name = "Kitchen"
entry_from = "loc_hallway"

# ---- Daily tick ----
[engine.daily_tick]
traitEffects = [
  { targetType = "player", trait = "hygiene", op = "add", value = -10 },
  { targetType = "player", trait = "arousal", op = "add", value = 1, cap = 10 },
  { targetType = "npc", npcId = "npc_frank", trait = "arousal", op = "add", value = 1, cap = 3 },
]

# ---- Sidebar ----
[[sidebar_items]]
type = "trait_words"
trait = "corruption"
label = "Status"
bands = [
  { min = 0,  max = 24, text = "Pure" },
  { min = 25, max = 49, text = "Lewd" },
  { min = 50, max = 74, text = "Slutty" },
  { min = 75, max = 100, text = "Whore" },
]

[[sidebar_items]]
type = "trait_bar"
trait = "arousal"
label = "Arousal"
max = 10

[[sidebar_items]]
type = "trait_status_text"
trait = "hygiene"
bands = [
  { min = 0,   max = 24,  text = "Filthy" },
  { min = 25,  max = 49,  text = "Dirty" },
  { min = 50,  max = 74,  text = "Fresh" },
  { min = 75,  max = 100, text = "Clean" },
]

# ---- Clothing ----
[[clothing]]
id = "starter_outfit"
name = "Jeans and tee"
slot = "top"
initial = true
beauty = 5
type = "casual"

# ---- Capstone canvas (Lane 4) ----
[[canvases]]
id = "scene_livingroom_catch"
name = "The catch"
description = "Frank catches Maya. Sets frank_caught."

[canvases.trigger]
location = "loc_living_room"
trigger_mode = "manual"
is_repeatable = false
priority = 10
conditions = { version = "1.0", items = [
  { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_false" },
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 25 },
] }
schedules = [{ weekdays = [0,1,2,3,4], start_time = "19:30", end_time = "21:00" }]

[[canvases.nodes]]
id = "catch"
name = "The catch"
blocks = [
  { type = "image", props = { file = "scenes/catch.jpg" } },
  { type = "paragraph", content = "He's there before you hear him." },
  { type = "dialog", npcId = "npc_frank", content = "Quiet." },
]

[canvases.nodes.exit_block]
type = "choices"

[[canvases.nodes.exit_block.choices]]
text = "Lower your eyes."
flagEffects = [{ targetType = "player", flag = "frank_caught", op = "set" }]
effects = [
  { targetType = "player", trait = "corruption", op = "add", value = 5 },
  { targetType = "player", trait = "frank_stage", op = "set", value = 2 },
]
targetType = "location"
locationId = "loc_living_room"

# ---- Quest card (capstone mode) ----
[[quest_cards]]
npc_id = "npc_frank"
priority = 1
text = "He's around the house all day. He notices."
ready_text = "I think he's about to call it."
ready_canvas = "scene_livingroom_catch"
when = [
  { flag = "frank_caught", op = "is_false" },
]
goals = [
  { trait = "corruption", subject = "player", op = "gte", value = 25, label = "Maya's corruption" },
]
```

---

**End of file.** For doctrine (when to use which primitive), read `prompts_v2/doctrine/`. For runtime behavior, read `prompts_v2/schema/01_engine_capabilities.md`.


## Label registries — `[[traits.labels]]` / `[[flags.labels]]` (Pattern 2)

Top-level arrays of tables that map an internal trait/flag key to a player-facing
label (used by `setup.computeHintGoal` when auto-rendering the 🎯 goal block).

```toml
[[traits.labels]]
key   = "trust"          # the core_trait key
label = "Trust"          # player-facing label
verb  = "reach"          # framing word: "reach Trust >= 15" (default "reach")
unit  = "session"        # optional unit noun for counter-style goals (e.g. "do Yard help x3")

[[flags.labels]]
key   = "frank_caught"
label = "Frank caught me"
```

### `hidden` (trait labels only) — hide an internal trait from ALL player-facing dumps

The generator's `playerTraits` sidebar widget and the Stats page dump **every**
`core_traits` key. Internal traits (`<slug>_stage`, `pregnancy`, antagonist
`awareness`) MUST live in `core_traits` (the engine reads/writes them there) but
must never be shown. Add a hide-only `[[traits.labels]]` entry:

```toml
[[traits.labels]]
key    = "frank_stage"
hidden = true            # label may be omitted on a hide-only entry
```

- Emitted as `setup.hiddenTraits`; skipped via `<<continue>>` in every trait-dump
  loop, in **both dev and non-dev** builds. Display-only — never alters state.
- **Limitation:** keyed by trait NAME only (not namespaced). A hidden key hides for
  the player AND any NPC carrying a core_trait of that name (e.g. an antagonist's
  `awareness` — usually the intent). Revisit only if you need the same trait name
  visible on one character but hidden on another.

See `doctrine/09_trait_catalog.md` §4.4 and the `stages/02` §11 checklist.

═══════════════════════════════════════════════════════════════════════════════

## 4. 03_example_toml

**Source:** `prompts_v2/schema/03_example_toml.md`

---

# Schema 03 — Example TOML (TLS Frank Slice — Canonical Authoring Examples)

**Source:** `games/the_long_summer_test/toml_phases/7_final_game.toml` (Frank slice, verified 2026-05-28).
**Authority:** Reference. Gold-standard authoring examples per Doc 66 §15.2 — the load-bearing canvases the LLM should mirror.
**Purpose:** Show, with verbatim TOML excerpts, what each pattern + lane + capstone type LOOKS like in shipped slice. Each excerpt has an explanatory frame naming which rules + patterns + anti-patterns it demonstrates.

This file is the empirical-example complement to `schema/02_toml_schema.md` (field tables) and `schema/01_engine_capabilities.md` (engine primitives).

**Per Doc 66 §15.2:** the TLS Frank slice TOML is the canonical reference for `schema/03_example_toml.md`. The Frank arc is the gold-standard authoring example. Pull excerpts from here when populating per-arc-shape briefs — don't synthesize new TOML.

---

## §1 — What this file is

Verbatim TOML excerpts from the shipped TLS slice (commit `9c2e450` working tree, 2026-05-28). Each excerpt:
- Lives at a specific line range in `7_final_game.toml`
- Demonstrates a specific lane + pattern + rule combination
- Has commentary naming which rules it follows + which anti-patterns it avoids

The excerpts are organized lane-by-lane (Lane 1 hub + route-target / Lane 2 ambient / Lane 3 dispatcher parent + substitution target / Lane 4 capstone Type A + Type B) + supporting structures (NPC + schedules + quest cards + sidebar).

**Note on completeness:** these are EXCERPTS — load-bearing canonical patterns. For the complete shipped slice, see `games/the_long_summer_test/toml_phases/7_final_game.toml`. For full schema documentation, see `schema/02_toml_schema.md`.

---

## §2 — Frank NPC block + schedules (gold standard)

**Demonstrates:** `[[npcs]]` definition + `arc_stages` declaration + per-NPC `[[npcs.schedules]]` with non-overlapping time windows.

**Source:** `7_final_game.toml:402–466`.

```toml
[[npcs]]
id          = "npc_frank"
name        = "Frank"
description = "Forty-eight. Broad through the shoulders, calloused hands with a web of small framing scars. Salt-and-pepper hair, work boots by the door. Addresses Maya by name — *Maya* — and the name lands like a door closing. Owns the property. The rent and the rules come from him."
portrait    = "frank.jpg"
core_traits = { love = 0, trust = 0, corruption = 0, arousal = 0 }
flag_keys   = []
arc_stages  = ["Suspicious", "Grudging warmth", "Restrict", "Tease", "Cracked"]

[npcs.trait_decay]
love  = 0.5
trust = 0.3

# Phase B (2026-05-14): Frank's location schedule. First-match-wins; entries are
# non-overlapping by design so getNpcLocation always returns a single answer.

[[npcs.schedules]]
location = "loc_franks_bedroom"
weekdays = [0, 1, 2, 3, 4, 5, 6]
start_time = "23:00"
end_time = "06:00"
activity = "asleep"

[[npcs.schedules]]
location = "loc_kitchen"
weekdays = [0, 1, 2, 3, 4, 5, 6]
start_time = "05:30"
end_time = "09:00"
activity = "morning coffee"

[[npcs.schedules]]
location = "loc_yard"
weekdays = [0, 1, 2, 3, 4, 5, 6]
start_time = "14:00"
end_time = "17:00"
activity = "yard work"

[[npcs.schedules]]
location = "loc_kitchen"
weekdays = [0, 1, 2, 3, 4]
start_time = "17:00"
end_time = "19:30"
activity = "dinner prep"

[[npcs.schedules]]
location = "loc_living_room"
weekdays = [0, 1, 2, 3, 4]
start_time = "19:30"
end_time = "21:00"
activity = "evening"

[[npcs.schedules]]
location = "loc_franks_bedroom"
weekdays = [0, 1, 2, 3, 4]
start_time = "21:00"
end_time = "23:00"
activity = "winding down"

[[npcs.schedules]]
location = "loc_hallway"
weekdays = [5, 6]
start_time = "21:30"
end_time = "23:00"
```

### Key features

- **`arc_stages = [...]`**: list of stage NAMES (display strings). Frank has 5 stages. The CURRENT stage integer lives on the player namespace as `player.core_traits.frank_stage` (per `doctrine/09_trait_catalog.md` §9).
- **`core_traits`**: 4 traits declared at game start. Engine reads `(npc.core_traits || {})[key]` — undeclared = silent garbage; sidebar items referencing undeclared traits hard-fail.
- **`trait_decay`**: per-NPC daily decay map. `love` decays 0.5/day; `trust` decays 0.3/day. NPCs Maya neglects lose relationship slowly.
- **7 schedule entries**: non-overlapping coverage of 24h. `getNpcLocation` (`v2.py:2923`) scans these to compute Frank's current location at any time.
- **Weekend variant**: weekdays = [5,6] vs [0,1,2,3,4] gives Saturday/Sunday a different evening pattern (Frank in the hallway 21:30-23:00 weekend instead of living room then bedroom).

### Anti-patterns avoided

- **Overlapping schedules**: each entry's time window is non-overlapping with siblings. Engine first-match-wins on time scan; overlapping entries would produce indeterminate `getNpcLocation` returns.
- **Hidden stage on NPC**: `arc_stages` is the LIST of stage names; the current stage integer lives at `player.core_traits.frank_stage`. Wrong: `{ targetType = "npc", npcId = "npc_frank", trait = "stage", op = "set", value = 2 }`. Right: `{ targetType = "player", trait = "frank_stage", op = "set", value = 2 }`. (See `doctrine/09_trait_catalog.md` §9.)

---

## §3 — Lane 1 hub canvas (gold standard)

**Demonstrates:** Lane 1 hub with `requires_npc` + locked-visible escalation ladder + `show_when_locked` + RTS-direct verbs.

**Source:** `7_final_game.toml:5353–5460` (excerpt).

```toml
[[canvases]]
id          = "frank_kitchen_morning_hub"
name        = "Kitchen — Frank, morning"
description = "Always-show RTS ladder hub for Frank in kitchen, morning slot (daily 05:30-09:00). 2026-05-17 hub-collapse: 4 rungs (Tease/Flash/Suck/Have-sex) + Pour coffee + Leave; locked rungs shown greyed (show_when_locked). Suck + Have-sex route to loop_franks_bedroom_sex.intro. Sex gate unified at corr 25."

[canvases.trigger]
location      = "loc_kitchen"
requires_npc  = "npc_frank"
is_repeatable = true
priority      = 10
is_active     = true
npc           = "npc_frank"
[[canvases.trigger.schedules]]
weekdays   = [0, 1, 2, 3, 4, 5, 6]
start_time = "05:30"
end_time   = "09:00"

[[canvases.nodes]]
id   = "base"
name = "Kitchen — morning, Frank present"
# 2026-05-25 R1 collapse — Doc 56 R1: hub openings stay constant within a canvas.
# Three tier blocks (frank_caught is_false / is_true+cracked is_false / cracked is_true)
# were authoring overhead. The menu rungs already encode progression via show_when_locked
# + per-choice conditions. Opening collapsed to one constant paragraph + dialog.
blocks = [
  { type = "image", props = { file = "scenes/frank_kitchen_morning_hub.jpg", description = "Frank at the counter. Coffee. Paper. You in the doorway." } },
  { type = "paragraph", content = "Frank's at the counter. He looks up when you come in." },
  { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Morning." },
]

[canvases.nodes.exit_block]
type = "choices"

# ─── Pour him coffee — always available (relational base interaction) ──────
[[canvases.nodes.exit_block.choices]]
text = "Pour him coffee."
targetType = "node"
nodeId = "frank_kitchen_morning_hub.pour_coffee"
time_progression_minutes = 5

# ─── Tease him ❤️‍🔥 — corr 5+ (locked-visible) ──────────────────────────────
[[canvases.nodes.exit_block.choices]]
text = "Tease him ❤️‍🔥"
targetType = "node"
nodeId = "tease_kitchen_general.base"
time_progression_minutes = 0
show_when_locked = true
conditions = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 5 },
] }

# ─── Flash him 👀 — corr 15+ (locked-visible) ──────────────────────────────
[[canvases.nodes.exit_block.choices]]
text = "Flash him 👀"
targetType = "node"
nodeId = "flash_kitchen_general.base"
time_progression_minutes = 0
show_when_locked = true
conditions = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 15 },
] }

# ─── Suck him here. — corr 25+ (locked-visible) ────────────────────────────
[[canvases.nodes.exit_block.choices]]
text = "Suck him here."
targetType = "node"
nodeId = "loop_franks_bedroom_sex.intro"
time_progression_minutes = 0
show_when_locked = true
conditions = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "player", trait_key = "arousal", operator = "gte", value = 1 },
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 25 },
  { type = "flag",  subject = "player", flag_key = "frank_bedroom_first_done", operator = "is_true" },
] }
effects = [
  { targetType = "player", trait = "sex_stage",            op = "set", value = 1, clamp = false },
  { targetType = "player", trait = "sex_entry_origin",     op = "set", value = 1, clamp = false },
]

# ─── Have sex with him here 🔥 — corr 25+ (locked-visible) ─────────────────
[[canvases.nodes.exit_block.choices]]
text = "Have sex with him here 🔥"
targetType = "node"
nodeId = "loop_franks_bedroom_sex.intro"
time_progression_minutes = 0
show_when_locked = true
conditions = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "player", trait_key = "arousal", operator = "gte", value = 1 },
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 25 },
  { type = "flag",  subject = "player", flag_key = "frank_bedroom_first_done", operator = "is_true" },
] }
# ... + effects for the sex loop entry
```

### Key features

- **`requires_npc = "npc_frank"`**: Lane 2/3 NPC-presence gate (Phase A 2026-05-14). Engine ANDs `getNpcLocation("npc_frank") === "loc_kitchen"` with all other gates. Frank's schedule (§2) places him in kitchen 05:30–09:00, so the canvas fires only during his morning slot.
- **`priority = 10`**: hub priority. Lane 4 capstones at the same location use `priority ≥ 9` to win against this hub.
- **`is_repeatable = true`**: hub re-fires every visit. Distinct from Lane 4 capstones which use `is_repeatable = false`.
- **Constant opener** (post-Doc 56 R1 collapse): one paragraph + dialog. No tier-routed group blocks for the opening. Progression-aware behavior lives in the menu rungs, not the opening prose.
- **Locked-visible escalation ladder**: Tease (corr 5+) / Flash (corr 15+) / Suck (corr 25+) / Have sex (corr 25+). All four rungs have `show_when_locked = true` — visible from day 1 even at Stage 0, telegraphing the arc shape.
- **`locked_text_threshold`** (not shown in this excerpt): per `doctrine/04_authoring_rules.md` §3 P7 — locked-click publishes the threshold, no stat drain.
- **Pronoun-in-the-verb test passes**: all menu verbs have NPC as object — "Pour HIM coffee" / "Tease HIM" / "Suck HIM" / "Have sex with HIM."

### Rules + patterns demonstrated

- **D56-R1**: hub opener constant (no T0/T1/T2 group blocks for opening)
- **D56-R7**: gated rungs ship with `show_when_locked = true` (the locked-visible ladder)
- **P5**: Lane 1 = intentional escalation; verbs match (Maya owns the act)
- **P10**: requires_npc consults the sidebar/`getNpcLocation`; the world model is the gate

### Anti-patterns avoided

- **Lane 1 over-weighting (Doc 54 §3.1)**: hub has 5 items (Pour + Tease + Flash + Suck + Sex) + Leave. Cap at ~5 unlocked items honored.
- **Verb register failure (Doc 54 §3.2)**: every menu verb has NPC as object. No "Take a long shift" / "Wash the dishes" (those are solo activities, parallel surfaces).
- **Missing locked-visible ladder (Doc 54 §4.5)**: all 4 escalation rungs visible from Stage 0.
- **Tiered hub opener (Doc 56 R1)**: post-2026-05-25 collapse — opener is one constant paragraph, not 3 tier blocks.

---

## §4 — Lane 1 route-target stub (route-only pattern)

**Demonstrates:** route-target canvas with NO `[canvases.trigger]` block + internal `[group]` tier-routing.

**Source:** `7_final_game.toml:5207–5260` (excerpt).

```toml
[[canvases]]
id          = "tease_kitchen_general"
name        = "Kitchen — tease him"
description = "Stub Pattern A render: corr 5+ kitchen general tease. Maya catches his eye, holds it, looks away. 1-beat. Reachable only via frank_kitchen_morning_hub menu item."

# NOTE: NO [canvases.trigger] block. This canvas only reachable via nodeId
# routing from a hub menu item. Frank's tease/flash pattern.

[[canvases.nodes]]
id   = "base"
name = "Kitchen — tease him"
blocks = [
  { type = "image", props = { file = "scenes/tease_kitchen_general.jpg", description = "You. Mug at your mouth. Held look across the kitchen." } },

  # T0 (pre-catch): held look, nothing else
  { type = "group", props = { conditions = { version = "1.0", logic = "AND", items = [
      { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_false" },
    ] }, blocks = [
    { type = "paragraph", content = "You catch his eye over the mug and hold it. He's still looking when you look back." },
    { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Girl." },
  ] } },

  # T1 (post-catch, pre-cracked): he openly looks at your tits
  { type = "group", props = { conditions = { version = "1.0", logic = "AND", items = [
      { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_true" },
      { type = "flag", subject = "player", flag_key = "frank_cracked", operator = "is_false" },
    ] }, blocks = [
    { type = "paragraph", content = "You catch his eye. His look drops to your tits and stays there — he doesn't pretend he wasn't looking." },
    { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Mm." },
  ] } },

  # T2 (post-cracked): he steps in, backs you against the counter
  { type = "group", props = { conditions = { version = "1.0", logic = "AND", items = [
      { type = "flag", subject = "player", flag_key = "frank_cracked", operator = "is_true" },
    ] }, blocks = [
    { type = "paragraph", content = "You catch his eye. He sets the mug down, crosses to you, backs you against the counter — hand under your shirt, thumb on your nipple." },
    { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Don't fucking start with me at breakfast, girl." },
  ] } },
]

[canvases.nodes.exit_block]
type = "choices"

# WEAN @15 (2026-05-21): trivial self-display stops paying PLAYER corruption past 15.
# lt/gte mutex on one same-text button — exactly one renders.
[[canvases.nodes.exit_block.choices]]
text = "Drink your coffee."
targetType = "location"
locationId = "loc_kitchen"
time_progression_minutes = 5
conditions = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "lt", value = 15 },
]}
effects = [
  { targetType = "npc",    npcId = "npc_frank", trait = "arousal",    op = "add", value = 1, cap = 3 },
  { targetType = "player", trait = "arousal", op = "add", value = 1, cap = 10 },
  { targetType = "player", trait = "corruption", op = "add", value = 1 },
]
```

### Key features

- **NO `[canvases.trigger]` block**: this canvas isn't a clickable surface. It's only reachable via `nodeId = "tease_kitchen_general.base"` from `frank_kitchen_morning_hub.exit_block.choices`.
- **Internal tier-routing via `[group]` blocks**: three tiers (T0 pre-catch / T1 post-catch / T2 post-cracked) gated on flag state. Same scene grows in intensity as Maya's arc advances.
- **Lt/gte mutex on exit**: at corruption < 15, click grants +1 corruption. At corruption ≥ 15 (the trivial-display wean), the same-text button has a different conditions block (not shown here) — no player corruption tick. The mutex means exactly one button renders.

### Rules + patterns demonstrated

- **Route-target stub pattern (Doc 54 §6.1)**: NO `[canvases.trigger]` — reachable only via hub routing
- **P3** (one scene, multiple lengths) via `[group]` tier-routing
- **D56-R2**: T0 + T1 endings are slim ("Girl." / "Mm.") — they read as "more is possible at higher tier" without an explicit in-fiction interruption. T2 blows through (he crosses to her, hand under shirt).

### Anti-patterns avoided

- **Stub with trigger block (Doc 54 §6.1)**: Frank's tease/flash/sex canvases are route-only. Authoring with a trigger block would produce validator overlap warnings + make the stub directly clickable (defeats the routing purpose).

---

## §5 — Lane 2 ambient with R2 in-fiction interruption (gold standard)

**Demonstrates:** Lane 2 random encounter + `trigger_mode = "random"` + `chance` + tier-routed cascade with in-fiction interruption at T0 ending (Doc 56 R2 / D56-R2).

**Source:** `7_final_game.toml:5802–5889`.

```toml
[[canvases]]
id          = "ambient_kitchen_frank_late_night_raid"
name        = "Kitchen — late night, both up for water"
description = "Lane 2 ambient: midnight kitchen encounter. Entry corr 25+. 2 stage-flag tiers (T0 pre-first-night makeout broken by Diana's floorboard / T1 post-first-night bareback counter quickie + daddy call/response before Diana wakes). NOTE: NO requires_npc — Frank scheduled bedroom / hallway this hour; the ambient's premise is 'neither was supposed to be here' — Frank stepped out for water, presence implied by the ambient itself."

[canvases.trigger]
location             = "loc_kitchen"
is_repeatable        = true
priority             = 6
is_active            = true
trigger_mode         = "random"
chance               = 0.40
max_triggers_per_day = 1
conditions = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "npc", npc_id = "npc_frank", trait_key = "arousal", operator = "gte", value = 1 },
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 25 },
] }
[[canvases.trigger.schedules]]
weekdays   = [0, 1, 2, 3, 4, 5, 6]
start_time = "22:00"
end_time   = "22:59"

[[canvases.nodes]]
id   = "base"
name = "Kitchen — late night, both up for water"
blocks = [
  { type = "image", props = { file = "scenes/ambient_kitchen_frank_late_night_raid.jpg", description = "Kitchen near midnight, one bulb. Frank in sleep pants, no shirt. You in a long nightshirt. House dark." } },
  { type = "paragraph", content = "You didn't think anyone was awake; the kitchen light's already on. Frank's at the sink in sleep pants and nothing else, a glass of water in his hand." },

  # T0 (frank_first_night_done is_false): midnight makeout, broken by Diana's floorboard
  { type = "group", props = { conditions = { version = "1.0", logic = "AND", items = [
      { type = "flag", subject = "player", flag_key = "frank_first_night_done", operator = "is_false" },
    ] }, blocks = [
    { type = "cascade", props = { id = "ambient_kitchen_frank_late_night_raid_t0_cascade", beats = [
      { blocks = [
        { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Couldn't sleep either." },
        { type = "paragraph", content = "You shake your head and cross to the cabinet. His eyes are on you in the long nightshirt and he doesn't pretend they aren't." },
      ] },
      { advance_text = "Step closer to the counter.", blocks = [
        { type = "paragraph", content = "You step in for a glass; his hands find your waist first and lift you onto the counter. Your legs go around him without thinking." },
        { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Quiet, girl." },
      ] },
      { advance_text = "Kiss him.", blocks = [
        { type = "paragraph", content = "His mouth on yours, one hand under the nightshirt at the small of your back, the other on your thigh. You make a sound you shouldn't and he swallows it." },
      ] },
      { advance_text = "Hear the floorboard upstairs.", blocks = [
        { type = "paragraph", content = "Diana's floorboard, her bedroom door. He lifts you down, hands you your glass, turns the tap on like he was doing dishes." },
        { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Night, girl." },
      ] },
    ] } },
  ] } },

  # T1 (post-first-night): they don't stop — bareback counter quickie before Diana wakes
  { type = "group", props = { conditions = { version = "1.0", logic = "AND", items = [
      { type = "flag", subject = "player", flag_key = "frank_first_night_done", operator = "is_true" },
    ] }, blocks = [
    { type = "cascade", props = { id = "ambient_kitchen_frank_late_night_raid_t1_cascade", beats = [
      { blocks = [
        { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Knew you'd come down." },
        { type = "paragraph", content = "He sets the glass down and has your nightshirt up before you reach the cabinet. He lifts you onto the counter, no underwear under the shirt." },
      ] },
      { advance_text = "Pull him in.", blocks = [
        { type = "paragraph", content = "You pull him in by the waistband and he slides into you bare on the counter. *'Daddy,'* you breathe into his neck to keep it quiet." },
        { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Good girl. Fast, then." },
      ] },
      { advance_text = "Fast, then.", blocks = [
        { type = "paragraph", content = "He fucks you fast on the counter, hand over your mouth, and cums inside you before the house stirs. He lifts you down and hands you the glass you came for." },
        { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Night, girl." },
      ] },
    ] } },
  ] } },
]

[canvases.nodes.exit_block]
type = "location"
text = "Take the glass. Go back to bed."

[canvases.nodes.exit_block.config]
destinationType          = "specific"
locationId               = "loc_kitchen"
time_progression_minutes = 15
effects = [
  { targetType = "npc",    npcId = "npc_frank", trait = "arousal",    op = "add", value = 1, cap = 3 },
  { targetType = "player", trait = "arousal", op = "add", value = 1, cap = 10 },
  { targetType = "npc",    npcId = "npc_frank", trait = "corruption", op = "add", value = 1 },
  { targetType = "player",                       trait = "corruption", op = "add", value = 2 },
  { targetType = "player",                       trait = "energy",     op = "add", value = -18 },
  { targetType = "npc",    npcId = "npc_diana", trait = "awareness",  op = "add", value = 2 },
]
```

### Key features

- **`trigger_mode = "random"` + `chance = 0.40`**: dispatched by `checkRandomEncounters` on location entry. 40% probability per visit (when conditions met).
- **`max_triggers_per_day = 1`**: same canvas can't fire twice in a day.
- **NO `requires_npc`**: deliberate per the description — the ambient's premise is "Frank stepped out for water" (implied presence), so no schedule gate. Doc 67 R6 doctrine adapted: implied-presence overrides loose presence check.
- **Two-tier `[group]` cascade**: T0 (pre-first-night) + T1 (post-first-night). Same canvas, different cascade depending on flag state.
- **R2 in-fiction interruption at T0**: T0 ending is "Diana's floorboard, her bedroom door. He lifts you down, hands you your glass, turns the tap on like he was doing dishes." The interruption is EXTERNAL (Diana's footsteps stop the cascade). T1 explicitly blows through: "He fucks you fast on the counter, hand over your mouth, and cums inside you before the house stirs."
- **Cross-arc state write**: `npc_diana.awareness +2`. The Diana arc reads this; high awareness eventually triggers `scene_diana_confrontation` capstone.

### Rules + patterns demonstrated

- **D56-R2 gold standard**: T0 ending lands on in-fiction interruption (Diana's floorboard); T1 explicitly blows through.
- **P3**: one scene, multiple lengths — same canvas grows in intensity at higher tier.
- **P5**: Lane 2 = ambient coexistence; "you walked into the kitchen and Frank was there" framing.
- **P8**: mechanism (cascade with conditional groups) carries the daily texture; the once-only Frank-Diana confrontation gets the Tier-3 capstone authoring.

### Anti-patterns avoided

- **Clean T0 ending (Doc 56 R2 violation)**: T0 does NOT end on a complete-feeling beat. The Diana interruption signals "more is here." P3's "you saw the short version" cue is preserved.
- **Tier-3 leakage in Lane 2 (Doc 57 §9)**: voice register stays RTS-flat with specific detail. Frank's "Quiet, girl." / "Knew you'd come down." carry character without literary cadence. Tier-3 prose reserved for capstones.

---

## §6 — Lane 3 dispatcher parent (Pattern A multi-NPC-ready)

**Demonstrates:** Maya-solo activity with `[[canvases.trigger.substitutions]]` rule + Lane 3 dispatcher mechanism.

**Source:** `7_final_game.toml:8175–8216`.

```toml
[[canvases]]
id          = "activity_make_tea"
name        = "Make a cup of tea"
description = "Maya-solo dispatcher. Kitchen, T1. Maya makes a cup of tea at the counter (kettle, bag, hot water). Substitution target: scene_frank_passes_kitchen_door."

[canvases.trigger]
location      = "loc_kitchen"
is_repeatable = true
priority      = 3
is_active     = true
[[canvases.trigger.substitutions]]
target_canvas_id = "scene_frank_passes_kitchen_door"
chance           = 0.30
conditions = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 5 },
] }
[[canvases.trigger.schedules]]
weekdays   = [0, 1, 2, 3, 4, 5, 6]
start_time = "07:00"
end_time   = "22:00"

[[canvases.nodes]]
id   = "base"
name = "Make a cup of tea"
blocks = [
  { type = "image", props = { file = "activities/make_tea.jpg", description = "Kitchen counter. Kettle on the gas burner. Maya at the counter with a mug, tea bag tag hanging over the rim. Window light." } },
  { type = "paragraph", content = "She fills the kettle from the tap. Sets it on the burner. Drops a tea bag in the mug while the water comes up. The kitchen quiet around her. The kettle clicks when it's hot. She pours." },
]

[canvases.nodes.exit_block]
type = "location"
text = "Take the mug back to your room."

[canvases.nodes.exit_block.config]
destinationType          = "specific"
locationId               = "loc_kitchen"
time_progression_minutes = 10
effects = [
  { targetType = "player", trait = "energy", op = "add", value = 2 },
]
flagEffects = []
```

### Key features

- **Maya-solo body**: the activity prose is third-person Maya making tea. No NPC interaction in the solo branch.
- **`[[canvases.trigger.substitutions]]` rule**: 30% chance + `corruption ≥ 5` conditions → if hit, replaces this canvas's body with `scene_frank_passes_kitchen_door` (see §7).
- **`priority = 3`**: lower than NPC hubs (priority 10) and Lane 2 ambients (priority 6). The solo activity is a base-tier surface; substitutions are more interesting.
- **Stat cost on exit_block** (Pattern A placement): `+2 energy` only fires on solo branch return. If Frank's substitution preempts, Maya doesn't "complete" the tea-making — no energy gain.
- **NO `requires_npc`**: the solo body is the default. The substitution mechanism handles NPC-presence routing internally.

### Rules + patterns demonstrated

- **D67-R1**: solo activity is a separate canvas, not a sub-block of the kitchen hub.
- **D67-R2**: stat cost placement INSIDE `exit_block.effects` — costs only if Maya completes the chore.
- **D67-R3**: menu-level gating not duplicated here. The location button gates time-of-day + energy; this dispatcher trusts the menu's gating.
- **Pattern A (Doc 67 §4.1)**: sequential first-match dispatcher. Currently 1 rule; would extend to multi-NPC by adding more rules ordered by narrative priority.
- **P5**: Lane 3 = "I was doing X and he happened" — the solo body sets Maya up as authentically not-about-Frank; the substitution arrives as charged surprise.

### Anti-patterns avoided

- **Solo activity body inline in hub (Doc 67 §9)**: this activity is its own canvas, not a sub-block of `frank_kitchen_morning_hub`. Lane 3 substitutions require addressable parent canvases.
- **Time-of-day gate on dispatcher (Doc 67 §9)**: the schedule `07:00–22:00` is broad. Specific time-of-day gates live on the kitchen hub's menu button (energy/time-of-day check); the dispatcher just confirms Maya can attempt this chore.

---

## §7 — Lane 3 substitution target (tier-routed Pattern D-shape)

**Demonstrates:** `substitution_only = true` + tier-routed prose escalation with cascade.

**Source:** `7_final_game.toml:8467–8540` (excerpt).

```toml
[[canvases]]
id          = "scene_frank_passes_kitchen_door"
name        = "Kitchen — Frank passes the door while you're making tea"
description = "T1 Lane 3 substitution on activity_make_tea. Frank passes through the kitchen on his way somewhere — pauses at the door, sees her, the briefest moment. substitution_only."

[canvases.trigger]
location          = "loc_kitchen"
is_repeatable     = true
priority          = 4
is_active         = true
substitution_only = true

[[canvases.nodes]]
id   = "base"
name = "Kitchen — Frank passes the door"
blocks = [
  { type = "image", props = { file = "scenes/scene_frank_passes_kitchen_door.jpg", description = "Kitchen. You at the counter waiting on the kettle. Frank stopped close at your back instead of passing through." } },
  { type = "paragraph", content = "You're waiting on the kettle when Frank comes through the kitchen on his way to the back of the house. He doesn't pass straight through." },

  # T0 (frank_caught is_false): stops at your back, hand at your waist
  { type = "group", props = { conditions = { version = "1.0", logic = "AND", items = [
      { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_false" },
    ] }, blocks = [
    { type = "cascade", props = { id = "scene_frank_passes_kitchen_door_t0_cascade", beats = [
      { blocks = [
        { type = "paragraph", content = "He stops behind you in the narrow galley instead of going by, close enough that you feel him at your back reaching past you for nothing in particular." },
        { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Don't mind me, girl." },
      ] },
      { advance_text = "Hold still.", blocks = [
        { type = "paragraph", content = "His hand settles at your waist a beat too long for getting by, then he's moving again, out the far door. The kettle's still not boiling." },
      ] },
    ] } },
  ] } },

  # T1 (post-catch, pre-cracked): turns you by the hip against the counter
  { type = "group", props = { conditions = { version = "1.0", logic = "AND", items = [
      { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_true" },
      { type = "flag", subject = "player", flag_key = "frank_cracked", operator = "is_false" },
    ] }, blocks = [
    { type = "cascade", props = { id = "scene_frank_passes_kitchen_door_t1_cascade", beats = [
      { blocks = [
        { type = "paragraph", content = "He stops at your back and turns you by the hip before you can pretend not to notice, his hand flat and low on you against the counter." },
        { type = "dialog", props = { speaker = "player" }, content = "Daddy, the kettle—" },
      ] },
      { advance_text = "Let him.", blocks = [
        { type = "paragraph", content = "He keeps you there one-handed, the other still holding his coffee, in no hurry, until the kettle starts going. Then he lets go and walks on like nothing." },
      ] },
    ] } },
  ] } },

  # T2 (post-cracked): pulls your back to his chest, hand down your front
  # ... (similar [group] block with cracked flag is_true)
]
```

### Key features

- **`substitution_only = true`**: this canvas is excluded from `renderNpcPortraits` + `renderSoloActivities` + `selectAutoFireCanvasForLocation`. Only reachable via the substitution rule on `activity_make_tea`.
- **`priority = 4`**: irrelevant for substitution-only canvases (engine doesn't priority-sort them in selection paths).
- **Three-tier `[group]` cascade**: T0 (pre-catch) / T1 (post-catch, pre-cracked) / T2 (post-cracked). Pattern D-shape — gate at top-of-group, then linear cascade within each tier.
- **Daddy register at T1+**: Maya's "Daddy, the kettle—" at T1 reflects the Doc 31 §2 daddy framing rule (Stage 3+ tease tier).
- **No exit_block** (in shown excerpt): substitution targets often end with the parent activity's exit. Or they have their own exit_block returning to the location.

### Rules + patterns demonstrated

- **D67-R7**: substitution target. Note: this canvas's `max_triggers_per_day` should be `1` per Doc 67 R7 (not visible in this excerpt — verify in full TOML).
- **P3 + R2**: tier-routed cascade with `[group]` gates. T0's "the kettle's still not boiling" is the in-fiction interruption (nothing happens; the kettle continues; Frank moves on).
- **P5**: Lane 3 = "I was doing X and he happened" — Maya is making tea; Frank passes through; he stops.
- **`doctrine/08_kink_vocab_ceilings.md` daddy register**: Maya's daddy call emerges at T1 (post-catch = Stage 3 register on).

### Anti-patterns avoided

- **Missing `substitution_only = true` (Doc 67 §9)**: without this flag, the canvas would appear as its own clickable surface in the kitchen, defeating the "you were doing X and he happened" framing.
- **Strict `getNpcLocation == "loc_kitchen"` gate (Doc 67 R6)**: Lane 3 walk-ins use loose presence (Frank at home) — he wandered into the kitchen because Maya was there. No strict-location predicate.

---

## §8 — Lane 4 capstone Type A (Marge interview — service register short form)

**Demonstrates:** Type A linear deterministic capstone + Tier-3 prose at short length + trigger fingerprint (D57-R1).

**Source:** `7_final_game.toml:1617–1665`.

```toml
[[canvases]]
id          = "canvas_marge_interview"
name        = "Marge — interview"
description = "First visit to the diner. Marge sizes Maya up in 90 seconds, hires her on the spot. Fires once, gated on `hired_at_diner == false`."

[canvases.trigger]
location      = "loc_diner_front"
is_repeatable = false
priority      = 9
is_active     = true
conditions = { version = "1.0", logic = "AND", items = [
  { type = "flag", subject = "player", flag_key = "hired_at_diner", operator = "is_false" },
] }

[[canvases.nodes]]
id   = "interview"
name = "Interview"
blocks = [
  { type = "image", props = { file = "scenes/marge_interview.jpg", description = "Marge behind the diner counter, late forties, broad and quick. Apron, pencil behind her ear, the look of a woman who has read the resume of every girl who walks in.", search_queries = [
    "diner owner woman behind counter apron pencil southern",
    "late forties woman diner counter coffee pot apron rural",
  ] } },

  { type = "paragraph", content = "Marge looked up when the bell over the door went off. She didn't smile — Marge wasn't a smiler at first read. She poured a coffee Maya hadn't asked for and slid it across the counter." },
  { type = "dialog", props = { speaker = "npc", npcId = "npc_marge" }, content = "You're Diana's girl." },
  { type = "paragraph", content = "Maya nodded. Marge looked her over once — not the up-and-down men did, the up-and-down a woman who had hired forty waitresses did. The shoes. The hands." },
  { type = "dialog", props = { speaker = "npc", npcId = "npc_marge" }, content = "Five hours, four-fifty an hour, you keep your tips. Tonight if you want it. Cookie's in the back, she'll show you the float." },
  { type = "paragraph", content = "She didn't wait for an answer. She slid the apron across with the back of her hand and turned to the next customer." },
]

[canvases.nodes.exit_block]
type = "choices"

[[canvases.nodes.exit_block.choices]]
text = "Take the apron."
targetType = "trigger"
time_progression_minutes = 30
effects = [
  { targetType = "npc", npcId = "npc_marge", trait = "trust", op = "add", value = 5 },
  { targetType = "player",                    trait = "energy", op = "add", value = -3 },
]
flagEffects = [
  { targetType = "player", flag = "hired_at_diner", op = "set" },
  { targetType = "player", flag = "talked_to_marge_today", op = "set" },
  { targetType = "player", flag = "phone_active", op = "set" },
]
```

### Key features (Type A capstone fingerprint)

- **`is_repeatable = false`**: classic Type A trigger fingerprint (Doc 57 R1). Fires once.
- **`priority = 9`**: Lane 4 minimum priority (winning against Lane 2 randoms on entry).
- **Single flag-is_false gate**: `hired_at_diner is_false` is the only gate. Simple Type A.
- **Single node + single exit choice**: no fork. The "Take the apron" exit is the only path forward — the fiction is that Marge wasn't waiting for an answer.
- **Setter flag on exit**: `hired_at_diner = set` retires the canvas after the Accept path fires.
- **Tier-3 prose at 1,900 chars**: focused, not long. "The up-and-down a woman who had hired forty waitresses did. The shoes. The hands." — inferential character work + composed fragments = Tier-3 register.
- **Cross-arc flag write**: `phone_active = set`. Doc 46 — first wage in hand reactivates Maya's phone. The capstone is a hinge for a different system (phone) too.

### Rules + patterns demonstrated

- **D57-R1**: trigger fingerprint clean (is_repeatable = false + priority = 9 + flag-gate + flag-setter on exit)
- **D57-R2**: Type A simplicity preference — no Pattern F fork (Marge wasn't waiting for an answer)
- **D57-R3 / D50-R1**: capstone is referenced by quest card M1's `ready_canvas = "canvas_marge_interview"` (see §10)
- **Tier-3 voice register earned** (`doctrine/05_rts_flat_prose.md` §3): inferential character work + composed fragments + Marge-specific diction
- **P8**: author the points of no return; mechanize the texture — Marge hire is once-only, gets Tier-3; Marge's daily floor work is mechanism

### Anti-patterns avoided

- **`is_repeatable = true` capstone (Doc 57 §9)**: fingerprint is clean. Once-only behavior locked.
- **RTS-flat-bland voice in capstone (Doc 57 §9)**: the prose is Tier-3 (inferential character work). Wouldn't waste the once-only nature.
- **Capstone with no flag-setter (Doc 57 §9)**: `hired_at_diner` flag set on Accept exit. Canvas retires.

---

## §9 — Lane 4 capstone Type B with Pattern F fork (first-night)

**Demonstrates:** Type B branching capstone + Pattern F fork at terminal cascade beat + F1–F5 sub-rules.

**Source:** `7_final_game.toml:3362–3450` (excerpt; full canvas is ~350 lines including both branch nodes).

```toml
[[canvases]]
id          = "scene_franks_bedroom_evening"
name        = "Frank's bedroom — first night"
description = "Stage 4 FIRST-NIGHT cascade. Fires once when player first enters Frank's bedroom at evening — the dramatic threshold-cross moment. Pattern E linear cascade (entry-gated). Two choice exits (stay through / leave before dawn) write Stage-4 closure effects + register-distinguishing secondary stat. Entry gate: corruption ≥ 25 + frank_caught + first_done is_false."

[canvases.trigger]
location      = "loc_franks_bedroom"
requires_npc  = "npc_frank"
is_repeatable = true     # see note below
priority      = 9
is_active     = true
npc           = "npc_frank"
conditions = { version = "1.0", logic = "AND", items = [
  { type = "flag",  subject = "player", flag_key  = "frank_caught",              operator = "is_true"  },
  { type = "flag",  subject = "player", flag_key  = "frank_bedroom_first_done",   operator = "is_false" },
  { type = "trait", subject = "player", trait_key = "corruption",                 operator = "gte",      value = 25 },
] }
[[canvases.trigger.schedules]]
weekdays   = [0, 1, 2, 3, 4]
start_time = "21:00"
end_time   = "23:00"

[[canvases.nodes]]
id   = "base"
name = "Frank's bedroom — evening"
blocks = [
  { type = "image", props = { file = "scenes/franks_bedroom_evening.jpg", description = "Frank's bedroom at evening. The lamp on the nightstand on. Bed against the far wall, covers turned back. Frank in a chair by the window, robe over the back of the chair. Quiet, charged." } },

  # ─── First-night cascade ─────────────────────────────────────────────
  # Cascade Beats 0/1/2 stay in base. Beat 2 is now terminal — fork choices
  # in exit_block.choices route to node_first_night_climax (Accept) or
  # node_first_night_refuse (Refuse). RTS Pattern F equivalent.
  { type = "cascade", props = { id = "frank_bedroom_first", beats = [
    # Beat 0 — opens unconditionally on scene entry. The hallway approach.
    { blocks = [
      { type = "paragraph", content = "She walks the hallway slow. The boards she knows the squeak of from the wrong side, the runner Diana picked out three summers ago, the bathroom door closed and dark. The door at the end is the door she's only ever walked past." },
    ] },

    # Beat 1 — click "Push the door open."
    { advance_text = "Push the door open.", blocks = [
      { type = "paragraph", content = "It's open by an inch. Lamp light on the floorboards. She pushes it the rest of the way and steps in." },
      { type = "paragraph", content = "Frank in the chair by the window. He's not undressed. Just sitting in the way he sits — weight on one elbow, the lamp catching the side of his face, a paperback open in his lap that he hasn't been reading. He sets it down on the nightstand without marking the page." },
      { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Close the door." },
    ] },

    # Beat 2 — terminal. Click "Close the door." Per-beat effect: Frank.arousal +1.
    # Cascade ends here; exit_block.choices below render TWO fork options.
    { advance_text = "Close the door.", effects = [
      { targetType = "npc", npcId = "npc_frank", trait = "arousal", op = "add", value = 1, cap = 3 },
      { targetType = "player", trait = "arousal", op = "add", value = 1, cap = 10 },
    ], blocks = [
      { type = "paragraph", content = "She closes it. The latch clicks soft. The room is small the way the office is small but it isn't the office — there's no desk between them. Just the bed turned back and the lamp on and Frank standing now from the chair." },
      { type = "thought_bubble", props = { speaker = "npc_frank" }, content = "She came." },
      { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Come here." },
    ] },
  ] } },
]

[canvases.nodes.exit_block]
type = "choices"

# ─── FORK CHOICES — Accept / Refuse mid-cascade ─────
# RTS Pattern F equivalent. Both choices route via intra-canvas nodeId.
# Accept → node_first_night_climax (cross + sex + aftermath + standard
# overnight exits). Refuse → node_first_night_refuse (Frank stops, brief
# disengagement, exits to hallway). Refuse does NOT set
# frank_bedroom_first_done — the canvas can re-fire next eligible night.

[[canvases.nodes.exit_block.choices]]
text = "Cross to him."
targetType = "node"
nodeId = "scene_franks_bedroom_evening.node_first_night_climax"
effects = [
  { targetType = "player", trait = "corruption", op = "add", value = 1 },
]

[[canvases.nodes.exit_block.choices]]
text = "Hesitate. Step back."
targetType = "node"
nodeId = "scene_franks_bedroom_evening.node_first_night_refuse"
# No effects. Does NOT set frank_bedroom_first_done — canvas re-fires next eligible night.

# Then [[canvases.nodes]] for node_first_night_climax (sets first_done + tier-routed closing)
# Then [[canvases.nodes]] for node_first_night_refuse (sets nothing, exits)
```

### Key features (Type B + Pattern F fingerprint)

- **`is_repeatable = true` + self-gate**: the canvas is marked repeatable but conditions include `frank_bedroom_first_done is_false`. Functionally identical to `is_repeatable = false` when Accept fires (flag sets, gate fails next visit). **Refuse path leaves flag unset** → canvas re-fires next eligible night. This is the Doc 57 R1 `is_repeatable = true + flag_is_false self-gate` variant supporting F4.
- **`priority = 9` + flag gate + trait gate**: Type B fingerprint clean.
- **Cascade with TERMINAL fork beat (F3)**: Beat 2 ("Close the door.") is the cascade's last beat. The fork lives in `exit_block.choices`, not mid-cascade.
- **Per-beat effects on Beat 2**: Frank.arousal +1 + Maya.arousal +1 fire on the click. P6 (stats change during scenes).
- **Two distinct fork options (F1 + F2)**: "Cross to him." (Accept path) sets `frank_bedroom_first_done` on its climax node + Maya.corruption +1 on the cross. "Hesitate. Step back." (Refuse path) sets NOTHING — canvas re-fires next night.
- **Thought bubble on Beat 2**: `{ type = "thought_bubble", props = { speaker = "npc_frank" }, content = "She came." }` — Doc 13 §16 Finding 1 + `doctrine/05_rts_flat_prose.md` §7 4th-dimension primitive.
- **Tier-3 prose throughout**: "the boards she knows the squeak of from the wrong side, the runner Diana picked out three summers ago, the bathroom door closed and dark" — inferential character work + memory-callback + composed rhythm = Tier-3.

### Rules + patterns demonstrated

- **D57-R1**: trigger fingerprint (Type B variant with self-gate)
- **D57-R2**: Type B justified — branches diverge in flag-effect (Accept sets first_done; Refuse doesn't)
- **F1**: both branches playable in good faith (Refuse is honest no, not punishment)
- **F2**: real divergence (different flags set; different downstream content)
- **F3**: fork at terminal beat of cascade
- **F4**: Refuse keeps canvas alive for retry — Maya can hesitate tonight and accept tomorrow
- **F5 ⚠️**: F5 boundary. The climax node has T0 (corruption < 40) vs T1 (corruption ≥ 40) closing register inside the Accept branch. Two structural devices stacked — upper bound of complexity per capstone.
- **P8**: capstone gets Tier-3 prose; daily texture stays mechanism

### Anti-patterns avoided

- **F1 — Refuse-as-punishment (Doc 57 §9)**: Refuse path is "Hesitate. Step back." — honest disengagement. Not a snarky one-liner signaling "don't pick this."
- **F2 — Collapsible branches (Doc 57 §9)**: Accept sets `frank_bedroom_first_done`; Refuse doesn't. Real downstream divergence.
- **F3 — Mid-cascade fork (Doc 57 §9)**: Beat 2 is cascade-terminal. No N beats downstream of both branches.

---

## §10 — Quest cards (Frank F1–F6 + Marge M1–M2)

**Demonstrates:** Capstone-mode + mechanic-mode quest cards + chain continuity + climbing-bullet + terminal placement.

**Source:** `7_final_game.toml:2460–2580` (excerpt).

```toml
# F1 — Pre-catch climbing
[[quest_cards]]
text         = "I'm new under this roof. Frank watches me and pretends he isn't."
ready_text   = "Something's about to give."
tip          = "He's around the house all day. I notice that."
npc_id       = "npc_frank"
ready_canvas = "scene_livingroom_catch"
when = [
  { flag = "frank_caught", op = "is_false" },
]
goals = [
  { trait = "corruption", subject = "player", op = "gte", value = 25, label = "Maya's corruption" },
]

# F2 — Post-catch / pre-first-night
[[quest_cards]]
text         = "Upstairs now. The office stays for the books."
ready_text   = "He'll be in his bedroom tonight."
tip          = "Diana down the hall. Quiet."
npc_id       = "npc_frank"
ready_canvas = "scene_franks_bedroom_evening"
when = [
  { flag = "frank_caught", op = "is_true" },
  { flag = "frank_bedroom_first_done", op = "is_false" },
]

# F3 — Post-first-night / pre-declaration
[[quest_cards]]
text         = "He took me upstairs. He hasn't said the word yet."
ready_text   = "He's going to break tonight."
tip          = "Diana's asleep by then. The hallway is dark."
npc_id       = "npc_frank"
ready_canvas = "scene_frank_declaration"
when = [
  { flag = "frank_bedroom_first_done", op = "is_true" },
  { flag = "frank_cracked", op = "is_false" },
]
goals = [
  { trait = "corruption", subject = "player", op = "gte", value = 35, label = "Maya's corruption" },
]

# F4 — Post-declaration / pre-sleepover
[[quest_cards]]
text         = "He moved the line. The bedroom is the venue now."
ready_text   = "Tonight I don't leave."
tip          = "Diana down the hall. Quiet."
npc_id       = "npc_frank"
ready_canvas = "scene_frank_sleepover"
when = [
  { flag = "frank_cracked",         op = "is_true"  },
  { flag = "frank_sleepover_done",  op = "is_false" },
]
goals = [
  { trait = "corruption", subject = "player", op = "gte", value = 50, label = "Maya's corruption" },
]

# F5 — Post-sleepover / pre-Diana confrontation
[[quest_cards]]
text         = "The house feels smaller now. She's home all the time and she's watching."
ready_text   = "She's going to ask."
tip          = "She doesn't say anything. She doesn't have to."
npc_id       = "npc_frank"
ready_canvas = "scene_diana_confrontation"
when = [
  { flag = "frank_sleepover_done", op = "is_true"  },
  { flag = "diana_confronted",     op = "is_false" },
]
goals = [
  { trait = "awareness", subject = "npc", npc_id = "npc_diana", op = "gte", value = 8, label = "Diana noticing" },
]

# F6 — Post-Diana terminal
[[quest_cards]]
text     = "It's done either way."
npc_id   = "npc_frank"
priority = 1
terminal = true
when = [
  { flag = "diana_confronted", op = "is_true" },
]

# M1 — Pre-hire pointer (capstone). Points at canvas_marge_interview.
[[quest_cards]]
text         = "I need work. Diana said Marge runs the only place that hires off the street."
ready_text   = "She's at the register."
tip          = "Walk in. Ask."
npc_id       = "npc_marge"
ready_canvas = "canvas_marge_interview"
when = [
  { flag = "hired_at_diner", op = "is_false" },
]

# M2 — T0 climbing toward marge.trust >= 20 (PURE MECHANIC).
[[quest_cards]]
text   = "I'm on Marge's floor. Work the shifts. Don't whine."
tip    = "Shifts pay the rent. Trust comes from showing up."
npc_id = "npc_marge"
when = [
  { flag = "hired_at_diner", op = "is_true" },
  { trait = "trust", subject = "npc", npc_id = "npc_marge", op = "lt", value = 20 },
]
goals = [
  { trait = "trust", subject = "npc", npc_id = "npc_marge", op = "gte", value = 20, label = "Marge trust" },
]
# unlocks at marge.trust >= 20:
#   - scene_marge_diner_hub.base greeting flips from T0 ("You're either on the floor
#     or you're a customer, hon.") to T1 ("Coffee's fresh if you're not here to work
#     for once."). The greeting tier flip IS the entire unlock. No new menu items,
#     no new ambients, no new substitutions open at this threshold.
```

### Key features

- **F1: Capstone-mode card with climbing bullet** — `ready_canvas` set + `goals` block surfaces the corruption 0 → 25 climb. D50-R2.
- **F2: Capstone-mode card without `goals`** — D50-R2 doesn't apply because the canvas's gate (corruption ≥ 25) is already guaranteed by F2's `when` (which kicks in after `frank_caught` was set via F1's `ready_canvas`).
- **F3: Climbing-bullet on post-first-night** — `goals` surfaces the corr 25 → 35 climb between first-night and declaration. D50-R2 — this fix landed 2026-05-24.
- **F4: Sleepover capstone pointer** — `ready_canvas = scene_frank_sleepover` + corr 50 climb. D50-R1 — fix landed 2026-05-24 (sleepover was off-panel before).
- **F5: Diana confrontation pointer with NPC-stat goal** — `goals` block tracks `npc_diana.awareness` climb. D50-R6 — label "Diana noticing" in Maya-voice, not raw `npc_diana.awareness` key.
- **F6: Terminal card** — `terminal = true` placed at the LAST Frank flag (`diana_confronted`). D50-R3 — replaces old terminal at `frank_cracked` which was two scenes too early.
- **M1: Capstone-mode pointer for hire** — `ready_canvas = canvas_marge_interview`. D50-R1.
- **M2: PURE MECHANIC card** — NO `ready_canvas`. `goals` tracks trust 0 → 20. Threshold cross IS the unlock. D50-R5 `# unlocks:` comment names what crosses at threshold (greeting tier flip).

### Rules + patterns demonstrated

- **D50-R1 (capstone coverage)**: every Frank capstone has a card pointer (F1 → catch, F2 → first-night, F3 → declaration, F4 → sleepover, F5 → Diana confrontation). Marge hire covered by M1.
- **D50-R2 (climbing-bullet)**: F1 + F3 + F4 + F5 all have `goals` blocks for the trait climbs above their `when` gate. F2 correctly omits `goals` (no climb above `when`).
- **D50-R3 (terminal placement)**: F6 is the LAST card. No card requires a flag set after `diana_confronted`.
- **D50-R4 (chain continuity)**: F1's `ready_canvas` sets `frank_caught` → F2 requires `frank_caught is_true`. F2's `ready_canvas` sets `frank_bedroom_first_done` → F3 requires it. And so on.
- **D50-R5 (mechanic-tier comment)**: M2 has the `# unlocks:` comment naming the greeting tier flip.
- **D50-R6 (REVERSED 2026-05-30 — LO pref)**: `goals.label` now NAMES THE TRAIT — "Corruption", "<NPC> Relation" — matching the sidebar, NOT Maya-voice euphemisms. The example labels below ("Maya's corruption", "Diana noticing", "Marge trust") predate the reversal; new games use trait-name labels. See `doctrine/04` §2.6.

### Anti-patterns avoided

- **Capstone with no card pointer (D50-R1 violation)**: every Frank capstone is referenced. Sleepover + Diana confrontation moved from off-panel to F4/F5 cards on 2026-05-24.
- **Premature terminal (D50-R3 violation)**: F6 at `diana_confronted` is the absolute last Frank flag. Old F4 at `frank_cracked` was wrong.
- **Climbing card with no `goals` bullet (D50-R2 violation)**: F3 had this violation before 2026-05-24; fixed with corruption 35+ goal.
- **Mechanic card with `ready_canvas` (D50-R5 violation)**: M2 correctly omits `ready_canvas`. Earlier draft had `ready_canvas = scene_marge_diner_hub` which violated mechanic-mode shape.

---

## §11 — Sidebar items (Maya stats — pending NPC radar)

**Demonstrates:** `[[sidebar_items]]` per Doc 49 + Doc 68 §8.

**Source:** TLS slice (extract from current `7_final_game.toml`).

```toml
[[sidebar_items]]
type = "trait_words"
trait = "corruption"
label = "Status"
bands = [
  { min = 0,  max = 24, text = "Pure",   icon = "✨" },
  { min = 25, max = 49, text = "Lewd",   icon = "💋" },
  { min = 50, max = 74, text = "Slutty", icon = "🔥" },
  { min = 75, max = 100, text = "Whore", icon = "💦" },
]

[[sidebar_items]]
type = "trait_bar"
trait = "arousal"
label = "Arousal"
max = 10
color_tiers = [
  { up_to = 30,  class = "low" },
  { up_to = 70,  class = "medium" },
  { up_to = 100, class = "high" },
]
bands = [
  { min = 0,  max = 2,  text = "Cold" },
  { min = 3,  max = 5,  text = "Warm" },
  { min = 6,  max = 8,  text = "Hot" },
  { min = 9,  max = 10, text = "Burning" },
]

[[sidebar_items]]
type = "trait_status_text"
trait = "hygiene"
bands = [
  { min = 0,   max = 24,  text = "Filthy", icon = "🧫" },
  { min = 25,  max = 49,  text = "Dirty",  icon = "🌫️" },
  { min = 50,  max = 74,  text = "Fresh",  icon = "🪞" },
  { min = 75,  max = 100, text = "Clean",  icon = "🧼" },
]

[[sidebar_items]]
type = "trait_status_text"
trait = "energy"
bands = [
  { min = 0,   max = 24,  text = "Exhausted", icon = "🪫" },
  { min = 25,  max = 49,  text = "Tired",     icon = "💤" },
  { min = 50,  max = 74,  text = "Fine",      icon = "🟢" },
  { min = 75,  max = 100, text = "Rested",    icon = "🔋" },
]

# When Doc 64 PRD ships, add per-NPC items:
# [[sidebar_items]]
# type = "npc_location"
# npc_id = "npc_frank"
# label = "Frank"
# stats = ["arousal", "corruption", "relation"]    # family/ambient default per Doc 68 §8
```

### Key features

- **`trait_words` for corruption** (banded display, raw number hidden) — Doc 68 Q2 lock
- **`trait_bar` for arousal** (0–10 with bands) — Doc 40 lock
- **`trait_status_text` for body-state** (hygiene + energy) — Doc 49
- **`npc_location` items** (commented out, pending Doc 64 PRD) — when shipped, per-NPC radar with per-arc-shape stat surfacing

### Anti-patterns avoided

- **Stage surfaced (Doc 68 §9 violation)**: no `frank_stage` / `ryan_stage` / etc. sidebar items. Stage is internal-only.
- **Antagonist awareness surfaced (Doc 68 §8)**: no `diana_awareness` sidebar item (will not be added).
- **Body-state hidden (Doc 49)**: energy + hygiene visible. Player needs to know when to sleep/shower.

---

## §12 — Clothing system (Late Shifts — RTS-faithful)

**Demonstrates:** the `[settings]` enable table (correct scoping), a tiered `[[clothing]]` catalog, the conditional coverage `clothing_rules`, a PUBLIC `worn_corruption` event (WEAN), and an exhibitionism flash ACT (+exb). The RTS-faithful model from `doctrine/11_clothing_design.md`.

**Source:** `games/late_shifts/toml_phases/` — `0_systems_spec.toml` (`[settings]`), `1_metadata_and_locations.toml` (`[[clothing]]` + `clothing_rules`), `5_scenes.toml` (`rts_public_clothing_*`), verified 2026-06-01.

```toml
# ── Enable the system: [settings] TABLE, not bare keys (the scoping trap) ──
# Read by the importer from data["settings"] (template_import.py:2224). Authored
# bare (e.g. right after [time]) → scopes under [time] → silently DISABLED.
[settings]
clothing_enabled  = true
wardrobe_location = "loc_mayas_room"
shop_location     = "loc_thrift_store"

[settings.clothing_requirements]
body_coverage   = true
always_required = []
```

```toml
# ── Catalog (excerpt across tiers). Top-level [[clothing]] array. ──
# Starting outfit: initial=true, free, full slot coverage (never naked/blocked).
[[clothing]]
id = "faded_tee"
name = "Faded T-Shirt"
slot = "top"
image = "clothing/faded_tee.jpg"
initial = true
beauty = 1
corruption = 0

# Going-out tier: UNGATED, worn_corruption 15-20 — makes public worn_corruption
# events reachable EARLY (before grinding global corruption). The load-bearing tier.
[[clothing]]
id = "going_out_top"
name = "Going-Out Top"
slot = "top"
image = "clothing/going_out_top.jpg"
price = 20
beauty = 4
corruption = 18

# Revealing tier: buy-gated on GLOBAL corruption (item conditions), worn_corr 25-35.
[[clothing]]
id = "crop_top"
name = "Crop Top"
slot = "top"
image = "clothing/crop_top.jpg"
price = 16
beauty = 4
corruption = 25
conditions = { version = "1.0", items = [ { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 25 } ] }
```

```toml
# ── Coverage gate: conditional on global corruption (RTS Bedroom parallel) ──
# On loc_main_street. Below corruption 50 she must cover up; at 50+ the rule's
# condition fails, no rule matches, she leaves underdressed. slots_required MUST be
# non-empty (validator rejects []); express the ceiling via `conditions`, not [].
clothing_rules = [
  { slots_required = ["top", "bottom"], message = "She can't head out half-dressed — better go back and put something on.", conditions = { version = "1.0", items = [
      { type = "trait", subject = "player", trait_key = "corruption", operator = "lt", value = 50 },
    ] } },
]
```

```toml
# ── PUBLIC worn_corruption event (WEAN — prose only, 0 global corruption) ──
# Two-tier (RTS ParkJog): >=15 glances/bigger tips, >=30 overt. On the diner FLOOR
# (customers), NOT on an NPC arc canvas. Gate on worn_corruption, not the NPC.
[[canvases]]
id          = "rts_public_clothing_diner_customers"
name        = "Mel's — the floor notices"
[canvases.trigger]
location             = "loc_diner_front"
is_repeatable        = true
priority             = 5
is_active            = true
trigger_mode         = "random"
chance               = 0.35
max_triggers_per_day = 1
conditions = { version = "1.0", items = [
  { type = "worn_corruption", operator = "gte", value = 15 },
] }
[[canvases.trigger.schedules]]
weekdays   = [0, 1, 2, 3, 4]
start_time = "22:00"
end_time   = "01:30"
[[canvases.nodes]]
id   = "base"
name = "The floor notices"
blocks = [
  { type = "paragraph", content = "The regular at Table 6 looks up a beat longer than the coffee warrants." },
  { type = "group", props = { conditions = { version = "1.0", items = [
      { type = "worn_corruption", operator = "gte", value = 30 },
    ] }, blocks = [
    { type = "paragraph", content = "The trucker doesn't pretend to look anywhere else. He tucks a folded twenty under the saucer." },
  ] } },
]
[canvases.nodes.exit_block]
type = "location"
text = "Keep working."
[canvases.nodes.exit_block.config]
destinationType = "specific"
locationId = "loc_diner_front"
time_progression_minutes = 10
```

```toml
# ── Exhibitionism flash ACT: the ONE place clothing content mutates a stat (+exb) ──
# Requires a revealing outfit to appear (worn_corruption>=25); the flash CHOICE
# grants +10 exhibitionism (RTS AddExb). Decline = free exit. Public surface.
[[canvases]]
id          = "rts_public_clothing_flash_park"
name        = "Town Park — give them something to see"
[canvases.trigger]
location             = "loc_town_park"
is_repeatable        = true
priority             = 6
is_active            = true
trigger_mode         = "random"
chance               = 0.25
max_triggers_per_day = 1
conditions = { version = "1.0", logic = "AND", items = [
  { type = "worn_corruption", operator = "gte", value = 25 },
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 25 },
] }
# … base node …
[canvases.nodes.exit_block]
type = "choices"
[[canvases.nodes.exit_block.choices]]
text = "Let him look."
targetType = "node"
nodeId = "rts_public_clothing_flash_park.node_flash"
effects = [
  { targetType = "player", trait = "exhibitionism", op = "add", value = 10, cap = 100 },
]
[[canvases.nodes.exit_block.choices]]
text = "Not here."
targetType = "location"
locationId = "loc_town_park"
```

### Key features

- **`[settings]` table** turns the system on — never bare keys (the silent-disable trap, `doctrine/11` §8).
- **Tiered catalog**: free full-coverage starting outfit / ungated going-out (worn_corruption 15-20) / revealing buy-gated on global corruption. The going-out tier makes public events reachable early.
- **Conditional coverage** `clothing_rules`: cover-up required only below corruption 50; non-empty `slots_required`.
- **`worn_corruption` on PUBLIC surfaces only** (diner floor with customers), two-tier, WEAN (no global-corruption effect).
- **Exhibitionism** = a stored player trait raised ONLY by a flash ACT choice; wearing alone never raises it.

### Anti-patterns avoided

- **NPC arc gated on the outfit** — clothing here gates customers/strangers, never Hank/Ben/Cole. NPC arcs stay on corruption + arousal + relationship (`doctrine/11` §2; backwards on-ramp `doctrine/02` §8.12).
- **`worn_corruption` granting global corruption** — every worn beat is WEAN; only the flash ACT mutates a stat (exhibitionism).
- **Empty `slots_required` fallback** — the coverage ceiling is expressed with `conditions`, not a `slots_required = []` rule (validator-rejected).

---

## §13 — Rent system (Late Shifts — the economic spine)

**Demonstrates:** the `[settings.rent]` enable table (correct scoping), the `[settings.rent.text]`
sub-table with the REAL key names, `start_after_flag` (arm-after onboarding), a `collector_npc`, and
`eviction_mode = "flag_set"` (fail-forward). The design model is `doctrine/12_rent_economy_design.md`.

**Source:** `games/late_shifts/toml_phases/0_systems_spec.toml` (`[settings.rent]`) +
`1_metadata_and_locations.toml` (the `npc_vince` collector), verified 2026-06-01.

```toml
[settings.rent]
enabled          = true
amount           = 125
due_day          = "Friday"           # engine arms the due trigger on Friday (one/week)
collector_npc    = "npc_vince"        # name + portrait shown on RentDay; must exist in [[npcs]]
grace_periods    = 1                  # one short week is survivable; the next triggers eviction
start_after_flag = "hired_at_diner"   # rent stays dormant until Maya has the job — rent-free onboarding
eviction_mode    = "flag_set"         # fail-forward: sets rent_evicted, play continues (vs "game_end")
eviction_flag    = "rent_evicted"

# RentDay prose, the collector's voice. A SUB-table (NOT a multi-line inline table —
# those break tomllib). Excerpt — the full key set is in schema/02 §14.3.
[settings.rent.text]
title                  = "Friday Morning"
greeting               = "Rent. Hundred and twenty-five. You've got it, or you've got a reason — and I've heard every reason this building's got."
paid_response          = "There. Wasn't so hard. Same Friday next week."
warning_response       = "One week. I'm not a bank and I'm not your friend. Friday."
eviction_response_soft = "Money's one way to keep a roof over your head. There's others. We'll talk about what works for me."
```

### The hybrid first-period pattern (TLS)

The engine handles *recurring* rent, but the *first* rent beat is often best hand-authored. TLS arms the
engine with `start_after_flag = "first_sunday_passed"` and sets that flag from a one-shot capstone
(`canvas_first_sunday_morning`) that delivers the first Sunday narratively. Result: the first rent is a
scripted story moment; every week after is the engine backstop. Use this when the first payment carries
plot weight; skip it (arm on a plain income flag, as Late Shifts does with `hired_at_diner`) when it
doesn't.

### Key features

- **`[settings.rent]` table** turns rent on — never bare `rent_enabled` keys (the silent-disable trap,
  `doctrine/12` §7 / `schema/02` §1.3).
- **`start_after_flag`** keeps onboarding rent-free — rent arms only once the player can earn.
- **`eviction_mode = "flag_set"`** is fail-forward: missing rent past grace sets `rent_evicted` and the
  game continues (the `_soft` text variants carry the consequence) rather than GAME OVER.
- **Real `[settings.rent.text]` keys** — `title` / `greeting` / `paid_response` / `warning_response` /
  `eviction_response_soft` etc. (NOT the fictional `{paid, late, evicted}` the old corpus listed).

### Anti-patterns avoided

- **`due_day` ignored** — the engine now fires on the configured weekday; the value is meaningful, not
  decorative. Frame the prose around that day.
- **Rent armed during onboarding** — `start_after_flag` defers the first due date until there's income;
  without it, rent would hit before the player can pay (`doctrine/12` §3).
- **Rent priced above reach** — `amount` is tuned to the wage (125 vs +45/shift, grace 1 as backstop) so
  the first post-arm due date is clearable (`doctrine/12` §5).

---

## §14 — Phone / apps system (Late Shifts — chat-centric, TLS-faithful)

**Demonstrates:** the top-level `[phone]` table (correct scoping — NOT `[settings]`, NOT a bare
`phone_enabled` key), `purchase_flag` gating, a `chat` app, a branching multi-round conversation
(`after_round` + `after_choice`), a `days_since_flag` trigger (time-relative without a day-of-week
condition), daily small-talk, and a corruption-gated photo quick-action. The design model is
`doctrine/13_phone_design.md`.

**Source:** `games/late_shifts/toml_phases/8_phone.toml`, verified 2026-06-02. The purchase-gate flag
`phone_active` is set at the diner hire (`2_one_shots.toml`, take-the-apron exit) alongside
`hired_at_diner` — Maya's cut-off phone reconnects once she has income.

```toml
# Top-level table. enabled defaults true when [phone] is present. purchase_flag
# hides the sidebar 📱 button until flags[phone_active] is set (the acquisition beat).
[phone]
enabled       = true
purchase_flag = "phone_active"

[[phone.apps]]
id    = "messages"
type  = "chat"
label = "Messages"

# A branching thread: triggers on a REAL arc flag, two reply choices, an NPC
# follow-up gated on which choice was picked (after_round + after_choice).
[[phone.conversations]]
id     = "hank_kitchen"
app    = "messages"
npc    = "npc_hank"
notify = "Hank texted you."
[phone.conversations.trigger]
conditions = { version = "1.0", items = [
  { type = "flag", subject = "player", flag_key = "hank_first_contact", operator = "is_true" },
] }
[[phone.conversations.blocks]]
type = "message"
sender = "npc"
content = "Kitchen's quiet after two. Door doesn't lock from the inside. In case you forget."
[[phone.conversations.blocks]]
type = "reply"
round = 1
choices = [
  { text = "I won't forget.",       effects = [{ targetType = "npc", npcId = "npc_hank", trait = "relation", op = "add", value = 2 }] },
  { text = "Is that an invitation?", effects = [{ targetType = "npc", npcId = "npc_hank", trait = "arousal", op = "add", value = 1 }, { targetType = "player", trait = "corruption", op = "add", value = 1 }] },
]

# Rent tie-in: phone triggers CAN'T read day-of-week (no `day`/`time` type), so a
# Friday reminder uses days_since_flag — fires ~4 days after hire (near rent week).
[[phone.conversations]]
id     = "vince_due_soon"
app    = "messages"
npc    = "npc_vince"
notify = "Vince texted you."
[phone.conversations.trigger]
conditions = { version = "1.0", items = [
  { type = "days_since_flag", subject = "player", flag_key = "hired_at_diner", operator = "gte", value = 4 },
] }
[[phone.conversations.blocks]]
type = "message"
sender = "npc"
content = "Friday's close. You know the number. I don't like knocking twice."

# Daily small-talk: 1/NPC/day (no `cooldown` field = legacy per-NPC cap), arc-gated.
[[phone.daily_topics]]
id             = "hank_smalltalk"
npc            = "npc_hank"
player_message = "still there?"
npc_response   = "Always am."
effects        = [{ targetType = "npc", npcId = "npc_hank", trait = "relation", op = "add", value = 1 }]
conditions     = { version = "1.0", items = [{ type = "flag", subject = "player", flag_key = "hank_opened_up", operator = "is_true" }] }

# Photo quick-action: cooldown="per_topic" (own 1/day cap), corruption_min tier.
[[phone.daily_topics]]
id             = "hank_photo_lewd"
npc            = "npc_hank"
player_message = "[Send a lewd photo]"
npc_response   = "Office. After two. Don't be late."
cooldown       = "per_topic"
corruption_min = 45
effects        = [
  { targetType = "player", trait = "arousal", op = "add", value = 1 },
  { targetType = "player", trait = "corruption", op = "add", value = 1 },
  { targetType = "npc", npcId = "npc_hank", trait = "arousal", op = "add", value = 1 },
]
conditions     = { version = "1.0", items = [{ type = "flag", subject = "player", flag_key = "hank_first_contact", operator = "is_true" }] }
```

The acquisition beat — the only `phone_active` setter, on the hire exit choice:

```toml
flagEffects = [
  { targetType = "player", flag = "hired_at_diner", op = "set" },
  { targetType = "player", flag = "phone_active",   op = "set" },   # unlocks the phone button
]
```

### Key features

- **Top-level `[phone]` table** turns the phone on — never `[settings]`, never a bare `phone_enabled`
  key (`schema/02` §13 / §1.3, `doctrine/13` §8).
- **`purchase_flag`** gates the sidebar button — phone stays hidden until the acquisition beat sets the
  flag (RTS-faithful earned-device pacing). Every such flag needs exactly one setter.
- **Threads trigger on REAL arc flags** — `hank_first_contact`, etc., verified present in the game, so
  threads actually dispatch (the dead-flag trap, `doctrine/13` §3).
- **`days_since_flag`** delivers time-relative content without a day-of-week condition (phone triggers
  don't support `day`/`time`; `doctrine/13` §4 + `schema/02` §13.3).
- **`cooldown = "per_topic"` + `corruption_min`** make photo quick-actions self-throttling, tiered
  (selfie → lewd 45 → nude 85), and gated to NPCs that carry the right traits.

### Anti-patterns avoided

- **Bare `phone_enabled`** — dead config the importer never reads; the §1.3 silent trap.
- **Day-of-week triggers** — unsupported by the phone evaluator; `days_since_flag` used instead.
- **Threads on non-existent flags** — every trigger flag is a verified setter in the LS arc.
- **Effects on traits an NPC lacks** — Cole (relation only) gets relation effects; Hank/Ben (arousal)
  get arousal effects — never a phantom trait.

---

## §15 — Player & NPC customization (Late Shifts — the personalization screen)

Opt-in start-of-game personalization. The engine auto-builds the `CustomizeCharacters`
screen and redirects `Start` to it — **no passage wiring.** You declare the fields and write
the prose with `@`-tokens. (Design model: **doctrine/14**.)

```toml
# ── Player: all three field types ───────────────────────────────────
[player]
id = "player"
name = "Maya"
customizable = true
# ... [player.core_traits] etc. ...

# Array-of-tables — MUST come after every [player.*] subtable (TOML scoping).
[[player.customization_fields]]
id = "name"            # special: writes $player.name (the @player token)
type = "text"
label = "Your name"
default = "Maya"

[[player.customization_fields]]
id = "body_type"       # writes $player.body_type → read with @player.body_type
type = "select"
label = "Build"
default = "average"
options = ["petite", "average", "curvy", "athletic", "thick"]

[[player.customization_fields]]
id = "look"
type = "image_select"
label = "Look"
default = "tired"
sets_portrait = true   # chosen image becomes $player.portrait
options = [
  { id = "tired",   image = "players/maya_tired.jpg",   label = "Worn out" },
  { id = "guarded", image = "players/maya_guarded.jpg", label = "Guarded" },
]

# ── A customizable NPC (rename + relationship picker) ───────────────
[[npcs]]
id = "npc_cole"
name = "Cole"
customizable = true                  # REQUIRES the next two lines (importer hard-fails otherwise)
relationship = "coworker"            # default — must be in relationship_options
relationship_options = ["coworker", "neighbor", "old flame"]
# ... core_traits, arc_stages, schedules ...

# ── Prose uses @-tokens (resolve at generation; honor the rename) ───
# In a canvas node body:
#   { type = "paragraph", content = "His eyes go over her @player.body_type frame once." }
#   { type = "dialog", props = { speaker = "npc", npcId = "npc_cole" }, content = "@player. Didn't think you'd come by." }
# @cole / @cole.rel elsewhere render Cole's chosen name / relationship label.

# ── Genericize the surfaces the @-token CAN'T reach (doctrine/14 §4) ─
[[locations]]
id = "loc_cole_apartment"
name = "The Apartment Across Town"   # NOT "Cole's Apartment" — location names print raw
# sidebar trait-bar label → "Closeness" (not "Cole Relation"); locked tooltip → "Once he's noticed you"
```

### Key features

- **Auto-screen, zero wiring** — any customizable player field or NPC inserts
  `CustomizeCharacters` and redirects `Start`.
- **All three player field types** — text (name), select (build), image_select (look,
  `sets_portrait`).
- **NPC rename + relationship toggle** — the genre's step-relative axis, here on the dating
  arc (cheapest, non-destructive candidate).
- **`@`-tokens in prose** — `@player`, `@player.body_type`, `@cole`, `@cole.rel`; dialog
  speaker labels are already dynamic via `npcId`.
- **Live-verified** — renaming player→*Nadia*/build→*curvy* and Cole→*Jamie* renders
  *"her curvy frame … Jamie: Nadia. Didn't think you'd come by."*

### Anti-patterns avoided

- **Declared fields, no token** — the silent half-use: a customizable name that never
  appears because the prose hardcodes "Maya". Every visible mention is `@player` / `@cole`.
- **Name baked into a structural label** — `"Cole's Apartment"`, `"Cole Relation"` would
  leak the old name after a rename. Genericized.
- **Customizable NPC without `relationship_options`** — a build-time hard-fail; both are
  required.
- **Renaming a premise-critical NPC** — the brother whose siblinghood *is* the story is the
  wrong candidate; the dating love-interest is the right one.

---

## §16 — Cross-references

### Sibling schema files

- `schema/01_engine_capabilities.md` — engine primitives referenced (`getNpcLocation`, `checkAndSubstituteCanvas`, `selectAutoFireCanvasForLocation`)
- `schema/02_toml_schema.md` — per-section field tables (TemplateNPC, TemplateNPCSchedule, TemplateCanvas, TemplateTrigger, TemplateChoice, QuestsCard, sidebar item types)

### Sibling doctrine files

- `doctrine/02_three_lanes_plus_capstone.md` — lane mechanism + capstone types (Type A / Type B / Type C-chain)
- `doctrine/03_arc_shapes.md` — Frank = family/ambient gold standard; Marge = service gold standard
- `doctrine/04_authoring_rules.md` — all D56 / D50 / D57 / F1–F5 / D67 rules cited above
- `doctrine/05_rts_flat_prose.md` — Lane 1/2/3 RTS-flat vs Lane 4 Tier-3 register
- `doctrine/06_design_brief_template.md` — R7 brief Doc 31 (Frank) + Doc 53 (Marge) are the gold-standard briefs these canvases were authored from
- `doctrine/07_anti_patterns.md` — Doc 54 27 failure modes (Marge case study)
- `doctrine/08_kink_vocab_ceilings.md` — Frank daddy register / Marge service register / Diana cuckold framing
- `doctrine/11_clothing_design.md` — the clothing design model (§12 example above is its worked reference)
- `doctrine/12_rent_economy_design.md` — the rent/economy design model (§13 example above is its worked reference)
- `doctrine/13_phone_design.md` — the phone/apps design model (§14 example above is its worked reference)
- `doctrine/14_customization_design.md` — the player/NPC customization model (§15 example above is its worked reference)

### Source TOML

- `games/the_long_summer_test/toml_phases/7_final_game.toml` — 536KB shipped TLS slice. Most excerpts above are verbatim from this file.
- `games/late_shifts/toml_phases/` — the §12 clothing excerpts (`[settings]`, `[[clothing]]`, `rts_public_clothing_*`), the §13 rent excerpt (`[settings.rent]`, `npc_vince`), the §14 phone excerpts (`[phone]`, `8_phone.toml`), and the §15 customization excerpts (`customizable`, `[[player.customization_fields]]`, `npc_cole` rename) are verbatim from the Late Shifts phase files.
- `games/under_one_roof/toml_phases/` — the largest customization consumer (3 customizable NPCs, 400+ `@`-tokens); the production reference behind doctrine/14.

### Source briefs

- `28th_april_TLS_Phase2_Redesign/31_Frank_Arc_Design_Brief.md` — Frank brief (informed `frank_kitchen_morning_hub`, `tease_kitchen_general`, `ambient_kitchen_frank_late_night_raid`, `scene_franks_bedroom_evening`, all 5 capstones)
- `28th_april_TLS_Phase2_Redesign/53_Marge_Redesign_Brief.md` — Marge brief (informed `canvas_marge_interview`, M1, M2)

---

**End of file.** Batch 2 complete pending quality gate + commit.

═══════════════════════════════════════════════════════════════════════════════

## 5. 01_rts_principles

**Source:** `prompts_v2/doctrine/01_rts_principles.md`

---

# Doctrine 01 — The 10 RTS Design Principles (P1–P10)

**Source:** Doc 56 §2 (`28th_april_TLS_Phase2_Redesign/56_RTS_Principles_and_TLS_Alignment_Doctrine.md`, 2026-05-24/25).
**Authority:** Doctrine. Every principle is verified against RTS source extraction in `game_explorations/rts-arc-trace/` (live-play + passage_catalog.json + variable_index.json).
**Purpose:** Name the 10 design principles every RTS-shape sandbox follows. Each principle has its RTS evidence cite reproduced verbatim. **Cite these as P1–P10 in all downstream prompts + docs.**

These principles describe *why* RTS works. The mechanism vocabulary (Lane 1/2/3/4) is in `doctrine/02_three_lanes_plus_capstone.md`. The arc-shape taxonomy + per-arc canvas budgets are in `doctrine/03_arc_shapes.md`. The authoring rules that operationalize these principles are in `doctrine/04_authoring_rules.md`.

---

## P1 — Density of decision-pressure over density of prose

Each click should be light in prose because the HUD does the heavy lifting. The player's brain is loaded by what the sidebar continuously surfaces (where every NPC is, time, money, stat positions, active quests), not by what the scene reads like. Short scenes work because the HUD carries the game between them.

**RTS evidence (live-verified):**

> 274 captured RTS scene bodies in `scene_bodies.jsonl` — median 137 characters, P25 = 75, P75 = 500. Half of RTS scenes are 25 words or less (Bathroom = 75 chars, Hallway = 137 chars, Study = "You studied an hour and feel smarter!"). The fat tail (P95 = 2760 chars) is the named-NPC scripted moments. **Most clicks are tiny; a small minority are deep.** Right sidebar shows every family NPC's location + arousal + corruption continuously, verified live in browser session.

**Authoring implication:** the Lane 1/2/3 prose target is the RTS-flat 30-word caption density (Doc 30 §7.1). The HUD is what makes 30-word scenes survive — without continuous sidebar feedback, the player has nothing to plan against. Image-first composition + sparse stage directions + dialogue doing the character work. Density goes into Lane 4 capstones, not into the daily texture.

**Cross-reference:** `doctrine/05_rts_flat_prose.md` (the 8 rules); `schema/01_engine_capabilities.md` §8 (sidebar item types).

---

## P2 — Transparent gating, not hidden progression

Every threshold is published. Failure shows the threshold. The Walkthrough catalogs every locked scene with its trigger recipe. Discovery is play-INTO-known-targets, not stumble-on-hidden ones.

**RTS evidence (verified):**

> `WalkthroughV2` passage (4738 chars) iterates `$npc` and `$location` objects, finds entries with `scenes` dicts, renders a table via `WalkthroughTable` widget with columns SCENE / NPC / REQUIREMENTS (NPC) / REQUIREMENTS (MC) / CHANCE / GUIDE / STATUS. The `guide` field per scene names the lane in plain English ("Go to your bedroom" / "Study at your room" / "Wash the dishes"). `<<NotifyCorruption N>>` widget toasts the threshold on locked clicks. Verified live: clicked into Stepbrother walkthrough table at corruption 0, saw all 15 scenes listed with full requirements columns.

**Authoring implication:** every canvas should ship with a `guide` string (Doc 56 R5 doctrine; schema field pending Doc 62 PRD). Every locked-choice Lane 1 menu item ships with `locked_text_threshold` publishing the gate value (RTS-style `<<NotifyCorruption N>>` pattern). The published catalog UI will render from these data primitives once Doc 62 ships.

**Cross-reference:** `doctrine/04_authoring_rules.md` R5 + R6; `schema/01_engine_capabilities.md` §10.4–§10.5.

---

## P3 — One scene, multiple lengths

Same passage plays differently at different stats. Low stats: short, often visibly truncated. High stats: full cascade. The player FEELS they're seeing a short version, which is what brings them back.

**RTS evidence (verified):**

> `BrotherCaughtMasturbating` (6431 chars) — one outer `<<linkreplace "Enter the room">>`, one paragraph plays, then `<<if getCorruptionLevel() >= 3>>` `<<if StageTwoCorruption($npc.Brother)>>` opens a nested `<<linkreplace "Shhh">>` that cascades through 8 more nested linkreplaces (~590 words). At low corruption, the same click hits the outer linkreplace, plays one paragraph, then `<<else>>` fires "Ew! You pervert!" + `<<NotifyCorruption 3>>` — ~5 lines total. Same passage, three possible play-throughs, gated by stats inside the body.

**Authoring implication:** for canvases that internally tier (Lane 2 ambients, Lane 3 substitution targets, Lane 1 escalation rungs), the lower-tier endings MUST hint at incompleteness — interrupted by an external sound (Diana's floorboard), self-stopping ("she sets the mug down before her hands shake"), or NPC pulling back ("he turns back to the paper"). The higher tier explicitly blows through the interruption — that's the payoff. This is Doc 56 R2 — *in-fiction interruption at T0/T1 endings.*

TLS uses `[group]` blocks instead of nested linkreplace, which loses the "you saw the short version" cue unless the in-fiction interruption is authored. Without it, the T0 ending reads as the whole thing.

**Cross-reference:** `doctrine/04_authoring_rules.md` R2.

---

## P4 — Mix arc shapes, don't pick one

Different NPCs run different mechanical rhythms. If every NPC is the same shape, the game collapses (all-grindy or all-VN). RTS uses family/ambient + peer/quest-chain + career/DM long-burn in parallel; three tempos demanding different player attention.

**RTS evidence (Doc 13 §5 + Doc 22):**

> Brother = 15 scenes, 47% Lane 3 distribution, family/ambient shape. Marcus = 5 scenes, all deterministic chance=100%, peer/quest-chain shape. Edward = 4 scenes, follower-metric + calendar-wait + phone-DM, career shape. Different mechanical signatures verified across 40 surfaces / 4 NPCs.

**Authoring implication:** the cast is 4–6 NPCs, each picking ONE arc shape from the 5-shape taxonomy (family/ambient, slow-burn family, peer/dating, service, antagonist/witness). Per-arc-shape per-lane canvas budgets in `doctrine/03_arc_shapes.md` are not interchangeable. Forcing one NPC's shape onto another produces drift — see Doc 54 Marge case study (escalation-NPC doctrine forced onto service register; 8 hours wasted before strip-clean recovery).

**Cross-reference:** `doctrine/03_arc_shapes.md`; `doctrine/04_authoring_rules.md` R3 + R7.

---

## P5 — Lanes correspond to fictional intent, not mechanism convenience

The same act feels different depending on how it reached the player. Lane 1 = "I am escalating" (agency, intentional). Lane 2 = "we coexist" (ambient, no agency). Lane 3 = "I was doing X and he happened" (mixed agency, charged surprise). Pick the lane for the feeling — not for engine convenience.

**RTS evidence (verified):**

> Doc 24 §3 Brother walkthrough classification: 5 Lane 1 scenes (intentional escalation — Tease/Flash/Sleep/Sex), 3 Lane 2 scenes (random encounters on bedroom entry — Grope/Peep/CaughtMasturbating), 7 Lane 3 scenes (dispatchers inside chores — Study/Shower/Dishes/Videogame). Same engine, three distinct framings.

**Authoring implication:** when scoping a beat, ask *"who is making this happen?"* before deciding the mechanism.
- Maya consciously claims the act → Lane 1.
- World produces ambient presence → Lane 2.
- Maya was solo + NPC arrives → Lane 3.
- Once-only narrative milestone → Lane 4 capstone.

Tease via Lane 1 = Maya decided to put on a show. Tease via Lane 3 = Maya was changing her clothes and NPC walked in mid-strip. Same physical act, different fictional weight. Picking the wrong lane neutralizes the beat.

**Cross-reference:** `doctrine/02_three_lanes_plus_capstone.md` §1–§3.

---

## P6 — Stats change DURING scenes, not just AT entry

Don't gate at the door. Let the player enter, then the watching itself adds arousal, then the next click adds corruption. Stats and prose interleave; the economy IS the story's tempo.

**RTS evidence (verified live):**

> In Doc 13 §12 turn-by-turn play log, peeping at `PeepBrotherSex` raised MC arousal 0 → 1, clicking "Keep Watching" on Dad's `ProstituteSex` raised it 1 → 2. The stat ticks happen ON the linkreplace clicks, not on entering the passage. The progression and the narrative interleave beat-by-beat.

**Authoring implication:** stat-effect macros should appear on individual cascade beat clicks + per-choice in `exit_block.choices.effects`. NOT only on canvas entry. The progression should feel beat-by-beat — each click moves both narrative and economy.

The corollary: per-beat `effects` lists in cascade blocks let small acts accumulate. A 4-beat cascade can author 4 separate +1 corruption ticks. The whole scene moves Maya 4 corruption, but the player FELT each move.

**Cross-reference:** `schema/01_engine_capabilities.md` §6.1 (effect schema); `schema/02_toml_schema.md` §7.4 (choice effects).

---

## P7 — Don't punish trying. Punish nothing.

Click a gated button → you see "30+ Corruption Needed." No stat drain. No "NPC's relationship dropped." Failure is information, not penalty.

**RTS evidence (verified):**

> Doc 13 §11 correction #3 — `<<NotifyCorruption N>>` is a UI hint widget, NOT a corruption adder. Verified across 5 widget definitions (`JimDM`, `RichardDM`, `EdwardDM`, `EdwardSecondDateDM`, `EdwardThreesomeDM`, `RichardSecondPhotoShootDM`). Always called in the ELSE branch with N matching the required level. Live verified: clicked "Have sex with him 🔥" at MC corruption 0 → notification appeared, corruption.points stayed 0.

**Authoring implication:** locked-choice clicks render `locked_text_threshold` as a toast banner (the TLS analog of `<<NotifyCorruption N>>`). Zero stat effects. Zero flag effects on failure. The player must be able to discover gates by clicking them without paying a price.

Anti-pattern: a Lane 1 menu item that decrements `relation` on locked-click. That penalizes exploration. RTS doesn't do this anywhere. Don't ship it.

**Cross-reference:** `schema/01_engine_capabilities.md` §10.4 (notifications + soft-fail); `doctrine/07_anti_patterns.md`.

---

## P8 — Author the points of no return; mechanize the texture

The big beats — first night, pregnancy reveal, declaration — get HAND-written, one of one, deliberate. The daily texture — hallway encounters, random teases, walk-ins — is mechanism. One cascade fires sometimes. Don't waste real prose on what happens 30 times.

**RTS evidence (Doc 35):**

> RTS doesn't mutate canvases for persistent states; it ROUTES to separate variant passages on the state predicate. Pregnancy gives a separate `BrotherBedroomPregnantSex1` passage variant. Pattern F real-choice forks (e.g., `SellingMyStepsister` Accept/Refuse branch) are hand-authored. Linkreplace cascade mechanism for the daily texture. Mechanism for what repeats; authorship for what doesn't.

**Authoring implication:** voice register is dual:
- **Lane 1 / 2 / 3 = RTS-flat default.** Re-readable without grating. Specific detail, but flat structure. ~30-word captions.
- **Lane 4 capstones = Tier-3 literary register, earned by the once-only nature of the scene.** Interior monologue, layered sensory detail per beat, character-distinguishing diction. (Doc 57 §6.)

The voice contract is "specificity, not literary density." Lane 2/3 prose can be specific ("the runner Diana picked out") without being literary (no interior monologue, no extended metaphor). Tier-3 is reserved for canvases the player will see once.

**Cross-reference:** `doctrine/05_rts_flat_prose.md`; `doctrine/02_three_lanes_plus_capstone.md` §4 (Lane 4 voice register).

---

## P9 — Per-arc vocabulary ceiling

Each NPC's content declares its kink ceiling upfront. Frank goes full explicit. Marcus stays school/peer. Don't force one register across the cast.

**RTS evidence (Doc 13 §5):**

> Marcus arc requires MC corruption=0 mostly — peer/school is the "wholesome" track. Brother arc escalates to full incest sex. Edward DM widgets escalate to threesomes. Different ceilings authored deliberately per NPC. The cast functions because different NPCs serve different roles.

**Authoring implication:** each NPC's R7 design brief declares the vocab ceiling per Doc 30 §7.5. The ceiling determines:
- Crude diction permitted at full intensity (Frank breeding talk vs Marcus peer slang)
- Anatomy + cum + degradation language allowance
- Power-dynamic register (dom-sub / cuckold / sibling incest / public exhibitionism)
- What's off-limits even at maximum tier

Per-arc ceiling = per-arc TONE. Forcing one register flat across the cast produces sameness; the cast functions because the registers contrast.

**Cross-reference:** `doctrine/08_kink_vocab_ceilings.md`.

---

## P10 — The HUD is the world model

The player has to be able to SEE the world. Where every NPC is. What time it is. What clothes they're wearing. What money they have. The right sidebar IS the world surfaced to the player. Without this radar, Lane 3 stops working entirely (the room doesn't tell you the NPC is here; the sidebar does).

**RTS evidence (verified live):**

> Right sidebar continuously renders Time (Early Morning, Monday, Clear weather), Quest pin, and per-NPC rows (Stepfather: Kitchen / Arousal / Corruption / Stepbrother: Bathroom / Arousal / Corruption / Stepgrandfather: Bedroom / Arousal / Corruption). Updates every tick. No menu click required to check NPC state.

**Authoring implication:** the sidebar must surface, for every in-scope NPC:
- Current location (via `getNpcLocation` runtime; sidebar item type pending Doc 64 PRD)
- Key stats per the register (arousal + corruption + relation for family/ambient; relation only for peer/service; location-only for antagonist)

Without per-NPC location radar, Lane 3 becomes undiscoverable — the player can't plan "if I shower now and Frank is in the kitchen, will he walk in?" The whole "you were doing X and he happened" texture depends on the player having the situational awareness to choose X knowing it might collide with the NPC.

**Visibility doctrine:** stage NEVER surfaces (internal-only per Doc 68 §9). Antagonist awareness NEVER surfaces (dramatic surprise depends on player NOT seeing how close confrontation is). Body-state (energy + hygiene) MUST surface.

**Cross-reference:** `doctrine/09_trait_catalog.md` §8 (NPC sidebar visibility per arc shape); `doctrine/04_authoring_rules.md` R4.

---

## Cross-references

### Sibling doctrine files

- `doctrine/02_three_lanes_plus_capstone.md` — the mechanism vocabulary the principles operate inside
- `doctrine/03_arc_shapes.md` — per-arc canvas distribution that operationalizes P4
- `doctrine/04_authoring_rules.md` — R1–R7 + Doc 50 R1–R6 + Doc 57 R1–R5 + F1–F5 (the rule layer)
- `doctrine/09_trait_catalog.md` — trait vocabulary the principles reference

### Schema files

- `schema/01_engine_capabilities.md` — engine primitives that implement each principle
- `schema/02_toml_schema.md` — per-section field tables

### Source docs (this folder's ancestor)

- `28th_april_TLS_Phase2_Redesign/13_Road_To_Success_Reference.md` — RTS catalog
- `28th_april_TLS_Phase2_Redesign/21_RTS_Brother_Mechanism_Audit.md` — Brother source extraction
- `28th_april_TLS_Phase2_Redesign/22_RTS_Cross_NPC_Mechanism_Comparison.md` — 40 surfaces / 4 NPCs
- `28th_april_TLS_Phase2_Redesign/24_RTS_Three_Lanes_Repeatable_Activities.md` — Lane mechanism source + §10 framework
- `28th_april_TLS_Phase2_Redesign/35_RTS_State_Variant_Authored_vs_Mechanism.md` — P8 codification
- `28th_april_TLS_Phase2_Redesign/56_RTS_Principles_and_TLS_Alignment_Doctrine.md` — source for this file

### RTS source artifacts (live-verified)

- `game_explorations/rts-arc-trace/passage_catalog.json` — RTS passage bodies (P1 length distribution; P3 nested cascade example; P8 variant passages)
- `game_explorations/rts-arc-trace/scene_bodies.jsonl` — 274 RTS scene bodies (P1 evidence)
- `game_explorations/rts-arc-trace/ui_map.json` — RTS HUD chrome catalog (P10 evidence)
- `game_explorations/rts-arc-trace/notes.md` — accumulated live-play observations

---

## Appendix — Mental check before authoring

Before any new canvas, ask:

| Question | Principle |
|---|---|
| Is the prose ≤ 30-word caption density (Lane 1/2/3) or earned-Tier-3 (Lane 4)? | P1 + P8 |
| Is the gate threshold published when the choice is locked? | P2 + P7 |
| Does the canvas tier-route in a way that hints at "more to come"? | P3 |
| Does this NPC's arc shape match the chosen lane distribution? | P4 |
| Is the lane chosen for fictional intent, not engine convenience? | P5 |
| Are stat-effect macros on cascade beats, not just on entry? | P6 |
| Are locked-click failures pure information (no stat drain)? | P7 |
| Is voice register matched to the lane (RTS-flat vs Tier-3)? | P8 |
| Does the content respect the NPC's declared vocab ceiling? | P9 |
| Does the sidebar surface the state the player needs to plan this beat? | P10 |

If any answer is "no," fix it before shipping. If unsure, surface to LO.

**End of file.** Next: `doctrine/02_three_lanes_plus_capstone.md` for the mechanism vocabulary.

═══════════════════════════════════════════════════════════════════════════════

## 6. 02_three_lanes_plus_capstone

**Source:** `prompts_v2/doctrine/02_three_lanes_plus_capstone.md`

---

# Doctrine 02 — Three Lanes + Lane 4 Capstones

**Sources:** Doc 24 (lane mechanism + §10 framework, 2026-05-10/11), Doc 57 (Lane 4 capstones, 2026-05-25), Doc 67 (solo-activity anatomy + multi-NPC dispatcher patterns, 2026-05-26).
**Authority:** Doctrine. The mechanism vocabulary for every RTS-shape sandbox game.
**Purpose:** Name the four lanes, what each one's mechanism is, what fictional intent each carries, how to author them, and how Lane 1 leads while Lanes 2/3/4 follow as consequences.

This file teaches the LLM *how to compose lanes into a coherent NPC arc*. The principles behind the choices are in `doctrine/01_rts_principles.md` (especially P5). The per-NPC canvas distribution is in `doctrine/03_arc_shapes.md`. The hard rules (R1–R7, R1–R5, F1–F5) are in `doctrine/04_authoring_rules.md`.

---

## §1 — The four lanes (overview)

RTS uses four distinct mechanisms for NPC content. Each has a different *who picked it* axis and a different fictional intent.

| Lane | Mechanism | Who picks | Player POV | Fictional intent |
|---|---|---|---|---|
| **1 — Hub button** | Button at NPC's location, gated on presence + time + stats. Player clicks. | **Player** | "I see Tease in the menu, I'll click it." | **Intentional escalation.** Maya owns the act. High agency. |
| **2 — Location-entry random** | Random encounter substitutes the location's hub render on entry. Dice roll. | **Dice on entry** | "I walked into the bedroom and Brother was masturbating." | **Ambient coexistence.** Maya didn't pick this; the world produced it. |
| **3 — Dispatcher substitution** | Player picks a Maya-solo activity (Shower / Study / Wash Dishes). Dispatcher rolls dice + may substitute an NPC scene. | **Dice inside Maya's activity** | "I was trying to shower and Brother walked in." | **Charged surprise.** Maya picked the activity; NPC arrived via coincidence. |
| **4 — Capstone** | Scripted one-shot scene. Auto-fires on location entry when conditions match. Never repeats. | **Engine, on threshold cross** | "He took me upstairs the night he caught me." | **Point of no return.** Hand-authored milestone. Tier-3 prose. |

**Plain-language analogies:**
- Lane 1 = a restaurant menu. Browse and pick.
- Lane 2 = walking into a room and your roommate is doing something. You went there; the encounter wasn't your choice.
- Lane 3 = cooking dinner and your roommate wandering in. You picked your activity; they showed up.
- Lane 4 = the moment the relationship turned. Once. Deliberate. Permanent.

**All four use the SAME canvas + trigger engine.** The lane-ness lives in the *combination of trigger fields* (per `schema/01_engine_capabilities.md` §3.3 fingerprints), not in a separate dataclass.

---

## §2 — Lane 1: hub button (intentional escalation)

### §2.1 — Mechanism

Player is at the NPC's location → engine renders NPC portrait → clicking routes to the NPC's hub canvas → canvas's `exit_block.choices` is the hub menu → each choice gates on stats + flags via per-choice `conditions`.

### §2.2 — Fictional intent

Maya intentionally claims the act. High agency. Vocabulary categories:
- **Relational** — Talk (build trust)
- **Self-display** — Tease, Flash (Maya owns the exhibition)
- **Consummation** — Sex 1, Pregnant Sex 1 (explicit intentional)
- **Late-game intimacy** — Sleep with him (relational + intimate, late-night only)

**Does NOT belong in Lane 1:** groping, walk-ins, things-that-happen-TO-Maya. The player picking "let him grope me" strips the encounter of its passive charge. Groping comes AT Maya in Lane 2/3, not from her in Lane 1.

### §2.3 — RTS evidence

| Brother scene | Lane | GUIDE | Chance |
|---|---|---|---|
| Sleep with Stepbrother | 1 | Go to Stepbrother bedroom late at night and ask to sleep with him | 100% |
| Stepbrother Bedroom Flash | 1 | Go to your Stepbrother bedroom | 100% |
| Bedroom Tease | 1 | Go to your Stepbrother bedroom | 100% |
| Brother Bedroom Sex I | 1 | Go to your Stepbrother bedroom and have sex with him | 100% |
| Brother Bedroom Pregnant Sex I | 1 | Go to your Stepbrother bedroom while pregnant and have sex with him | 100% |

**Lane 1 is always 100% chance** — the dice rolling moment is the PLAYER deciding to click, not the engine.

### §2.4 — TLS engine implementation

`TemplateChoice` (`exit_block.choices`) with `conditions` gates each menu item. Mode A renders greyed-out + `locked_text_threshold` toast on click. Engine wraps each choice in `<<if setup.triggerConditionsSatisfied(...)>>` at runtime — only matching choices render.

Fingerprint: `trigger_mode = "manual"` + `is_repeatable = true` + `npc` set + `location` matches NPC's schedule.

### §2.5 — Authoring template

```toml
[[canvases]]
id = "frank_bedroom_hub"
name = "Frank's bedroom"
description = "Lane 1 hub for Frank's bedroom. Post-catch."

[canvases.trigger]
location = "loc_franks_bedroom"
npc = "npc_frank"
trigger_mode = "manual"
is_repeatable = true
schedules = [{ weekdays = [0,1,2,3,4,5,6], start_time = "20:00", end_time = "23:00" }]
conditions = { version = "1.0", items = [
  { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_true" },
] }

[[canvases.nodes]]
id = "base"
name = "Frank's bedroom"
blocks = [
  { type = "image", props = { file = "scenes/franks_bedroom_evening.jpg" } },
  { type = "paragraph", content = "He's at the desk. He looks up when you come in." },
]

[canvases.nodes.exit_block]
type = "choices"

# Talk — always available
[[canvases.nodes.exit_block.choices]]
text = "Talk to him"
targetType = "trigger"
target = "scene_frank_bedroom_talk"
effects = [
  { targetType = "npc", npcId = "npc_frank", trait = "relation", op = "add", value = 1 },
]

# Tease — gated on Maya corruption 15+
[[canvases.nodes.exit_block.choices]]
text = "Tease him"
show_when_locked = true
locked_text = "Not yet."
locked_text_threshold = "Maya's corruption: 15+"
conditions = { items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 15 },
] }
nodeId = "tease_bedroom_general"
effects = [
  { targetType = "player", trait = "corruption", op = "add", value = 1 },
  { targetType = "player", trait = "arousal", op = "add", value = 1, cap = 10 },
  { targetType = "npc", npcId = "npc_frank", trait = "arousal", op = "add", value = 1, cap = 3 },
]

# Have sex with him — gated on Maya corruption 35+ + flag
[[canvases.nodes.exit_block.choices]]
text = "Have sex with him"
show_when_locked = true
locked_text = "Not until I'm sure."
locked_text_threshold = "Maya's corruption: 35+ AND Frank declared"
conditions = { items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 35 },
  { type = "flag", subject = "player", flag_key = "frank_cracked", operator = "is_true" },
] }
nodeId = "loop_franks_bedroom_finisher"

# Leave
[[canvases.nodes.exit_block.choices]]
text = "Leave"
targetType = "location"
locationId = "loc_hallway"
```

### §2.6 — Locked-visible escalation ladder (Doc 54 lesson)

The hub ships with the full escalation ladder VISIBLE from day 1, even at Stage 0. Locked rungs render greyed-out + publish their gate threshold on click (the RTS `<<NotifyCorruption N>>` pattern, P2 + P7).

The visible-but-locked ladder telegraphs the arc shape. A player at Maya corruption 0 looking at Frank's hub sees Tease (locked at 15) + Flash (locked at 25) + Suck (locked at 35) + Sex (locked at 45) — the arc shape is the FUTURE the player is playing toward.

Anti-pattern: hub with only currently-unlocked items. Player sees "Talk" + "Leave" at Stage 0 and has no read on what's coming. Doc 54 §4.5 case study.

### §2.7 — Hub menu cap

**~5 items unlocked + locked-visible ladder.** Frank's hubs cap at 5–6 items per location.

Anti-pattern: 10-item hub (Marge Pass 1 — Doc 54 §3.1). Over-weighting Lane 1 produces the "menu game" feel that Doc 24 §10.3 warns against ("All Lane 1 → fully transactional experience, low surprise"). If more rungs are needed, they should be locked-visible stages, not parallel work-tasks.

### §2.8 — Presence is acknowledged by a Lane 1 hub, per schedule row (Doc 72 R6)

If an NPC is present where the player can reach them (per `[[npcs.schedules]]`), visiting that place always *shows* the base moment. The mechanism for that floor is a **Lane 1 hub**: a canvas whose `base` node renders what the NPC is doing in the space, **even when zero choices are available**. Base node + exit, with no menu items unlocked, is a complete and valid canvas. Presence is acknowledged; the player never walks into a dead, empty room when the schedule says the NPC is there.

**The floor is per schedule row, and it must be a Lane 1 hub — not a Lane 2 ambient.** For every (location × time-window × weekdays) the NPC is scheduled, there is a hub whose own `trigger.schedules` covers that window (period-split per window — D56-R1, `doctrine/04` §1.1). A Lane 2 ambient cannot be the floor: it is a dice roll (`chance 0.25` ⇒ nothing on ~3 of 4 visits), so most visits would still be dead. Lane 2/3 are texture layered *on top of* the hub, never the acknowledgement itself. The engine enforces the window: a hub's portrait renders only when its own `schedules` is live and the NPC is present (`renderNpcPortraits` → `isCanvasValid`). The full rule, its corollary (a schedule entry is a promise of a hub), and the worked Hank example are in `doctrine/04` §6 (D72-R6).

The *choices* on top of the base then follow in-world logic, not a quota:
- Some are open from the start (helping a housemate fold laundry, greeting someone you live with — needs no permission).
- Some are gated until earned (the escalation ladder — locked-visible per §2.6, capped by location exposure per §2.9).
- Sometimes none apply, and base + exit is the whole canvas. That is correct, not a gap.

**The floor is hard; the choices are judgment.** The *hub-per-row* requirement is a checkable rule (D72-R6). The *choices on top* are still logic-driven (Doc 72 R2/R3): there is no rule that every NPC must offer an ungated action, and "base + exit" is a valid canvas. Two distinct axes — never conflate "the hub must exist" (hard) with "every hub must offer an action" (rejected quota). Never flag-gate the base node itself; gate the choices, never the act of *seeing* the NPC. The failures this bans are **dead presence** (§8.11), the **backwards on-ramp** (§8.12), and a **hub window narrower than the schedule** (§8.13).

### §2.9 — Exposure-tier rung ceiling (Doc 72 R7)

Which escalation rungs a hub may offer is decided by the **exposure** (privacy) of that location at that window — *who could see this, and what's at risk* — **not** by the time of day. Two orthogonal filters: **exposure sets the ceiling per hub; relationship state (corruption / relation / stage, global to the NPC) unlocks rungs within it.**

| Exposure tier | Locations (examples) | Rung ceiling |
|---|---|---|
| **Public** (high exposure) | diner floor with customers, street, park midday, mall | Deniable acts only — talk, banter, a charged look, a brush-past. No flashing, no sex. |
| **Semi-private** (low exposure) | back kitchen, office with a door, storeroom, building hallway | Tease / grope / quick contact; full sex gated higher or *interrupted* by the setting (the in-fiction interruption, §3.6). |
| **Private** (no exposure) | bedroom, apartment, the diner after close when alone | Full ladder, up to sex / sleepover. Private can be **more than one** location. |

**Time and co-present NPCs are inputs to exposure, not the gate.** A public location becomes private when it empties — the diner front at 2am, lights off, just the two of them, carries a higher ceiling than the same front at the breakfast rush. Not because "it's night," but because the room is empty now. Who else is scheduled there (alone vs. a coworker vs. an antagonist down the hall) changes exposure too. This is why a late-night hub legitimately differs from a morning hub at the same location while the rule stays *exposure*, not *time*.

This is the positive form of the verb-overlay anti-pattern (§8.1): the same act reads differently by place, so don't clone the full ladder into every room. **Same-NPC hubs stay consistent** (shared rung names + gate thresholds + voice; ladder context-scaled, not cloned) — D72-R8, `doctrine/04` §6.3. An optional *locked-visible-everywhere* variant (greyed higher rungs shown at public hubs, unlockable only where private) is allowed for telegraphing.

---

## §3 — Lane 2: location-entry random (ambient coexistence)

### §3.1 — Mechanism

Player enters location → engine's `checkRandomEncounters` walks all canvases with `trigger_mode = "random"` at that location → for each, evaluates conditions + rolls dice → first match substitutes the location's normal hub render.

### §3.2 — Fictional intent

NPC just exists in the same space. **Low-stakes contact** that builds texture without taking the wheel. Vocabulary categories:
- **Pass-by** — NPC passing in hallway with mug; NPC spotted from window
- **Solo activity glimpse** — NPC making coffee alone; smoking on porch; fixing radio
- **Passive contact** — Bedroom Grope (he's at home, you walk in, he gropes); you didn't ask, neither did he plan it as a Big Moment
- **Atmospheric voyeurism** — Peep NPC sex (you walked into the wrong room at the wrong time)

**Does NOT belong in Lane 2:** high-agency consummation. The NPC won't have full sex with Maya via Lane 2 — that needs to be earned via player choice (Lane 1) or scripted (Lane 4). Lane 2 carries brief, charged-but-bounded contact.

### §3.3 — RTS evidence

| Brother scene | Lane | GUIDE | Chance |
|---|---|---|---|
| Stepbrother Bedroom Grope | 2 | Go to your bedroom | 20% |
| Peep Stepbrother sex | 2 | Go to your Stepbrother bedroom | 25% |
| Brother Caught Masturbating | 2 | Go to your Stepbrother bedroom | 25% |

**Lane 2 is 20–25% chance.** Recurring but not certain. Dice roll happens on entry.

### §3.4 — Cooldown (Layer 3)

After a Lane 2 random fires at a location, `random_cooldowns[locId]` is set to **3 visits**. All Lane 2 randoms at that location are blocked for 3 subsequent visits.

Note (Doc 24 §8.1): TLS Lane 2 is STRICTER than RTS Lane 2 (RTS has no cross-attempt cooldown observed in source). One-line tunable at `v2.py` if Lane 2 feels too quiet in playtest.

### §3.5 — TLS engine implementation

Fingerprint: `trigger_mode = "random"` + `chance` set + `is_repeatable = true` + (optional) `requires_npc` for presence gate + (optional) `entry_only_from` for anti-toggle cooldown.

```toml
[[canvases]]
id = "ambient_kitchen_late_night_raid"
name = "Late-night kitchen raid"

[canvases.trigger]
location = "loc_kitchen"
trigger_mode = "random"
chance = 0.3
is_repeatable = true
requires_npc = "npc_frank"   # Frank must be home (his schedule resolves to a home location)
schedules = [{ weekdays = [0,1,2,3,4,5,6], start_time = "22:00", end_time = "01:00" }]
conditions = { version = "1.0", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 15 },
] }
```

### §3.6 — In-fiction interruption at T0/T1 endings (Doc 56 R2)

Lane 2 canvases that internally tier via `[group]` blocks (e.g., a 3-tier scene gated on `frank_caught` / `frank_cracked` flags) MUST land their lower-tier endings on an in-fiction interruption:
- **External:** Diana's floorboard, kettle whistling, NPC door opening
- **Internal:** Maya self-stopping ("she sets the mug down before her hands shake")
- **NPC-stopping:** the NPC pulling back ("he lets go like nothing")

The higher tier explicitly blows through. T0 ends on "we would have done more but —". T1 of the same canvas blows through ("he fucks you fast on the counter, hand over your mouth").

Without the interruption, T0 reads as the whole thing. Lane 2's principle-3 cue ("you saw the short version") evaporates.

---

## §4 — Lane 3: dispatcher substitution (charged surprise)

This is RTS's BIGGEST lane (47% of Brother's 15 scenes are Lane 3). And the hardest to author cleanly. Doc 67 is the source for §4 below.

### §4.1 — Mechanism

Player picks a Maya-solo activity at a location → transient dispatcher passage runs → dispatcher rolls dice + checks NPC conditions → may substitute an NPC scene; otherwise plays the normal solo content.

```
LOCATION PASSAGE (e.g. Bathroom)
  ├─ Menu buttons (time-gated, energy-gated, etc.)
  └─ Lane 2 events (location-entry randoms)
      │
      ▼
INTERMEDIATE PASSAGE (e.g. BathroomShower) — optional
  ├─ Activity setup (clothes off, image, body)
  ├─ Inline encounter check (Lane 2 sub-pattern)
  └─ Sub-menu button (Masturbate ❤️‍🔥)
      │
      ▼
DISPATCHER PASSAGE (e.g. BathroomShowerMasturbate)  ← THIS is the Lane 3 primitive
  ├─ Roll dice + check NPC conditions
  ├─ HIT  → goto NpcScene
  ├─ MISS → render solo content (image + body + ReturnButton)
  └─ ReturnButton applies time/energy cost
```

**Two-step activities** (Bathroom Shower → Masturbate) use an intermediate passage. **One-step activities** (Wash Dishes, Study) go straight from location button to dispatcher.

The dispatcher is ALWAYS a SEPARATE NAMED PASSAGE, not inline logic in the menu button. This makes substitution rules inspectable, debuggable, and authoring-friendly.

### §4.2 — Fictional intent

**Maya was doing something solo. NPC arrives mid-activity.** Vocabulary categories:
- **He walks in** — Shower Sex (NPC walks in while Maya masturbates); Wash Dishes Sex (he's there when she starts chores)
- **He arrives while vulnerable** — Help Study (she's studying, he comes in to "help"); Playing Videogame (she's gaming, he sits next to her)
- **Innocent setup → charged shift** — the SETUP must be authentically not-about-the-NPC. Maya wasn't trying to seduce him by showering; she was just showering. The seduction happens TO her.

The crucial structural rule: **the parent activity must be authentically not-about-the-NPC.** That's what makes Lane 3 carry the "happens to you" emotional weight that Lane 1 can't.

### §4.3 — RTS evidence (Brother — 7 of 15 surfaces are Lane 3)

| Brother scene | Lane | GUIDE | Chance |
|---|---|---|---|
| Stepbrother Bedroom Study Grope | 3 | Study at your room | 20% |
| Brother Help Study | 3 | Study at your room | 20% |
| Stepbrother Shower Sex | 3 | Masturbate at shower at the house bathroom | 33% |
| Playing Videogame | 3 | Play videogame at your living room | 20% |
| Stepbrother Washing Dishes Sex | 3 | Go to the kitchen and wash the dishes | 20% |
| (+ 2 pregnant variants) | 3 | (variant guides) | 20% |

**Lane 3 is 20–33% chance.** Four parent activities (Study, Play Videogame, Shower→Masturbate, Wash Dishes) host the 7 substitution targets.

### §4.4 — The solo-activity host (Doc 67 §3)

Every Lane 3 parent activity is its own `[[canvases]]` entry — not a sub-block of the location hub. Each has:

- `trigger_mode = "manual"` (player clicks button to enter)
- `is_repeatable = true` (chore can repeat)
- `location = "loc_X"` (anchors to a hub canvas)
- `schedules = [...]` (time-of-day availability)

This is **Doc 67 R1** — separate canvas, not sub-block. Inline activity bodies in a hub menu can't carry substitutions.

**Menu-level gating (Doc 67 R3):** time-of-day + energy + purchase + quest state gates live on the LOCATION canvas's button (the `exit_block.choices.conditions`), NOT in the dispatcher. The dispatcher trusts the menu's gating. NPC stage / corruption / presence remain in the dispatcher (substitution rule conditions).

**Stat cost placement (Doc 67 R2):** two options:
1. **Inside `exit_block.effects`** — applies only if Maya returns from solo branch. Use for cost-per-completion (wash dishes: Energy -10 only if she finishes).
2. **Outside `exit_block` in canvas body effects + `pre_substitution_effects`** — applies unconditionally on canvas entry, including substitution-preempted runs. Use for activities with unconditional outcomes (Exercise: +Fit even if interrupted).

Pattern A activities default to in-`exit_block` placement (NPC walk-in = chore not completed, no cost). Pattern C activities use `pre_substitution_effects` (Doc 69 Item 2 — Pattern C unconditional effects shipped 2026-05-27).

### §4.5 — Single-NPC dispatcher (`BathroomShowerMasturbate` canonical)

```twee
:: BathroomShowerMasturbate
<center>
<h1 class="ptitle">MASTURBATE 🚿</h1>
<<if isPlayerAtHouse() && random(1,3) == 1 && StageOneCorruption($npc.Brother) && IsNpcAtHome("Brother")>>
    <<goto 'BrotherShowerSex'>>
<<else>>
    <h3>You masturbate yourself. Corruption increased!</h3>
    [...solo image + body...]
    <<FinishMasturbation>>
<</if>>
<<ReturnButton "Bathroom" "Bathroom 🚾">>
    <<GetDressed>>
<</ReturnButton>>
</center>
```

1/3 chance + Brother's stage check + presence check → NPC scene, else solo. ReturnButton outside the if/else; `<<GetDressed>>` runs on click.

### §4.6 — Multi-NPC dispatcher patterns (Doc 67 §4)

When multiple NPCs could walk in on the same chore, three patterns exist. **The selection rule is fictional, not arbitrary.**

#### §4.6.1 — Pattern A: sequential first-match with independent dice rolls (`WashDishes` canonical)

```twee
<<if random(1,3) == 1 && $npc.Dad.arousal > 0 && IsNpcAtHome("Dad")>>
    <<goto 'DadWashDishesSex'>>
<<elseif random(1,3) == 1 && $npc.Brother.arousal > 0 && StageTwoCorruption($npc.Brother) && IsNpcAtHome("Brother")>>
    <<goto 'BrotherWashDishesSex'>>
<<else>>
    [...solo content...]
<</if>>
```

- Each NPC has its own independent dice roll.
- Sequential evaluation via `if/elseif`. Rule order = narrative priority.
- First-match preempts the rest.
- If Dad's dice fails OR Dad doesn't qualify, Brother's dice rolls fresh.

**Probability math** (both NPCs home + qualified):
- P(Dad scene) = 1/3 ≈ 33%
- P(Brother scene) = (2/3) × (1/3) = 22%
- P(solo) = (2/3) × (2/3) = 44%

**Use when:** multiple independent NPCs could plausibly walk in; one has narrative priority (escalation NPC, current focus arc); mutual exclusion not required (only one fires per attempt anyway because `<<goto>>` preempts).

**TLS engine support: ✅ NATIVE.** `setup.checkAndSubstituteCanvas` at `v2.py:4649` implements sequential first-match with independent `Math.random()` per rule. Maps 1:1.

```toml
[[canvases.trigger.substitutions]]
target_canvas_id = "scene_frank_kitchen_dishes"
chance = 0.33
conditions = { items = [
  { type = "trait", subject = "npc", npc_id = "npc_frank", trait_key = "stage", operator = "gte", value = 2 },
] }

[[canvases.trigger.substitutions]]
target_canvas_id = "scene_jake_kitchen_dishes"
chance = 0.33
conditions = { items = [
  { type = "trait", subject = "npc", npc_id = "npc_jake", trait_key = "stage", operator = "gte", value = 2 },
] }
```

#### §4.6.2 — Pattern B: single dice partition (`BedroomStudy` canonical)

```twee
<<set $game.dice to random(1,6)>>
<<if $game.dice == 1 && Dad conditions>>
    <<goto 'BedroomStudyDadGrope'>>
<<elseif $game.dice == 2 && Brother conditions>>
    <<goto 'BedroomStudyBrotherGrope'>>
<<elseif $game.dice == 3 && Brother conditions>>
    <<goto 'BrotherHelpStudy'>>
<<else>>
    [...solo content...]
<</if>>
```

- ONE shared dice roll.
- Buckets partition the result: 1=Dad, 2=Brother grope, 3=Brother help, 4–6=solo.
- **Mutual exclusion guaranteed** — impossible for two NPCs to fire simultaneously.
- **Failed-condition falls through to ELSE, NOT to next NPC.** If dice == 1 but Dad doesn't qualify → solo, not Brother. The dice value claims the slot; failed conditions don't promote the next NPC.

**Probability math** (both qualified): P(Dad) = 1/6, P(Brother grope) = 1/6, P(Brother help) = 1/6, P(solo) = 3/6. Fixed budget.

**Use when:** NPC scene variants are inherently mutually exclusive by design (often same NPC with sub-variants — Brother grope vs Brother help study at the study desk; one fires).

**TLS engine support: ✅ Native via `exclusive_group`** (Doc 69 Item 1 shipped 2026-05-27). Substitution rules sharing the same `exclusive_group = "<name>"` string share ONE dice roll partitioned into cumulative `chance` buckets. Failed target/conditions in a claimed slot fall to solo (does NOT promote next rule in the group) — the load-bearing Pattern B semantic. Multiple groups process in declaration order; rules without `exclusive_group` evaluate after via Pattern A first-match. Engine: `v2.py:4671-4713`.

```toml
# Brother sub-variants at study desk — exactly one fires or fall to solo
[[canvases.trigger.substitutions]]
target_canvas_id = "scene_brother_grope_at_desk"
chance           = 0.1667                          # 1/6
exclusive_group  = "study_desk_brother"

[[canvases.trigger.substitutions]]
target_canvas_id = "scene_brother_help_study"
chance           = 0.1667                          # 1/6 — group cumulative = 0.33
exclusive_group  = "study_desk_brother"
```

**Do NOT approximate Pattern B via Pattern A.** The approximation that was correct before 2026-05-27 (N rules with chance summing < 1) diverges in two ways: cumulative probability = 1 − ∏(1 − cᵢ) ≈ 42% vs true 50%, and failed-condition fall-through promotes to next rule instead of falling to solo. The engine extension is now shipped — emit Pattern B directly.

#### §4.6.3 — Pattern C: post-activity event check (`Exercise` / `PlayingVideogame` canonical)

```twee
[...solo activity body + image...]
<<AddFit>>      <!-- runs unconditionally -->
<<ReturnButton>>
    <<Energy -15>>
    <<AddTime 1>>
<</ReturnButton>>

/*EVENTS */
<<if isPlayerAtHouse() && GetNpcLocation("Grandpa") == "Living Room" && getCorruptionLevel() >= 4 && random(1,3) == 3>>
    <<goto 'GrandpaExerciseSex'>>
<</if>>
```

- Solo body processes FIRST (image, `<<AddFit>>`).
- Event block at end of passage.
- If conditions hit, `<<goto>>` preempts the page display — player goes to NPC scene.
- Stat changes OUTSIDE ReturnButton apply unconditionally; INSIDE only on solo branch.

**Why use this instead of A/B:** the activity has an unconditional stat outcome. Exercise = +Fit regardless of who walks in. The fitness training "counts" even if Grandpa interrupts.

Pattern C also uses `GetNpcLocation == "Loc"` (strict location check), NOT `IsNpcAtHome` (loose). The NPC must be co-located, not just home, because by the time the event check fires, Maya is at the location actively doing the thing.

**TLS engine support: ✅ Native via `pre_substitution_effects`** (Doc 69 Item 2 shipped 2026-05-27). Effects declared on the parent canvas's trigger run BEFORE the substitution check, so they execute on both the solo path AND the substituted-NPC-walk-in path. No effect duplication on substitute canvases is needed. Engine: `v2.py:11151` reads `trigger.metadata.pre_substitution_effects` and emits `<<script>>setup.applyAndNotifyTrait(...)<</script>>` macros before the substitution `<<goto>>`.

```toml
[canvases.trigger]
location = "loc_bedroom"
# ... other trigger fields ...

# Pattern C — solo Exercise grants +fitness regardless of who walks in
[[canvases.trigger.pre_substitution_effects]]
targetType = "player"
trait      = "fitness"
op         = "add"
value      = 1

[[canvases.trigger.substitutions]]
target_canvas_id = "scene_grandpa_walks_in_on_exercise"
chance           = 0.20
```

### §4.7 — Selection rule (the doctrine call)

| Authoring intent | Pattern |
|---|---|
| "Multiple independent NPCs could walk in on this chore; priority by arc focus" | **A** (default — no `exclusive_group` on rules) |
| "Several mutually exclusive variants — one fires per attempt" (often same NPC with sub-variants) | **B** (shared `exclusive_group` on rules) |
| "Activity has unconditional stat outcome that counts even when interrupted" | **C** (use `pre_substitution_effects` on parent trigger) |

**For slice authoring: default to Pattern A.** Patterns B and C are tools for specific intents that arise in particular activities.

### §4.8 — `IsNpcAtHome` vs `GetNpcLocation == "Loc"` (Doc 67 §3.5)

Two distinct presence checks; the choice is doctrine, not arbitrary.

| Check | Semantics | Used for | Fictional intent |
|---|---|---|---|
| `IsNpcAtHome` (loose) | NPC at home (any room) | Lane 3 dispatchers | "NPC walks in" — Maya is solo, NPC arrives mid-activity |
| `GetNpcLocation == "Loc"` (strict) | NPC at exact location | Lane 2 location-entry events + Pattern C post-activity events | "Maya walks in on NPC" — NPC is already there; Maya encounters them |

**Doctrine: direction of the walk-in determines the predicate.**
- Brother walking in on Maya showering → Lane 3 + loose check
- Dad already in bathroom when Maya arrives → Lane 2 + strict check

This is why same NPC at same location can fire on different lanes — it depends on which direction the encounter goes narratively.

**TLS implementation:** both achieved via `requires_npc` on the canvas trigger. The semantic difference lives in the NPC's schedule shape:
- Lane 3 walk-in: NPC's schedule has a meta-location or wide-scope entry resolving to "house"
- Lane 2 entry-encounter: NPC's schedule has an entry at the exact canvas location during the same time window

### §4.9 — Per-day cooldowns (Doc 67 §3.6)

Two mechanisms observed in RTS:

1. **`executedToday` flag (per-scene per-day):** `<<if !$npc.Dad.scenes.DadShowerSex.executedToday>>`. Resets at sleep/day rollover. **TLS analog: `max_triggers_per_day = 1` on canvas trigger.**

2. **`previous()` guard (per-passage immediate):** prevents the SAME passage that just played from re-triggering. Used in `BedroomSleep` to stop sleep-scene re-firing if player came back from one. **TLS: not directly supported; equivalent via flag-set on exit + flag-clear on day rollover.** Most cases don't need it.

**R7 doctrine (Doc 67):** every Lane 3 substitution target ships with `max_triggers_per_day = 1` + `is_repeatable = true`. Once-per-day is the felt cadence — the world has rhythm.

### §4.10 — Per-arc-shape Lane 3 budget (Doc 56 §5 / Doc 56 R3)

| Arc shape | Lane 3 budget | Rationale |
|---|---|---|
| **Family/ambient** | 4–7 | Shape requires saturating chores with NPC presence. Brother RTS = 7. |
| **Slow-burn family** | 1–3 | Sparse, keyed to specific arc moments — the walk-in IS the beat. |
| **Peer/dating** | 0 | Peer doesn't interrupt private chores. Arc lives in Lane 1 + capstones. RTS Marcus = 0. |
| **Service** | 0 | Workplace-only register; private space is not their setting. |
| **Antagonist/witness** | 0 own + appears as INTERRUPTOR in others' L3 endings | Diana doesn't have her own walk-ins; she's the THREAT in others' Lane 3 endings (the "Diana's floorboard" pattern). |

**Overages flag as drift.** If a service NPC is gaining Lane 3 substitutions, either the brief is wrong OR the additions don't belong.

---

## §5 — Lane 4: capstones (one-shot story beats)

Lane 4 is the hand-authored once-only beats — the first night, the catch, the declaration, the confrontation, the resolution. Doctrine source: Doc 57.

### §5.1 — Mechanical fingerprint (Doc 57 R1)

A capstone is a canvas with:

| Field | Value | What it does |
|---|---|---|
| `is_repeatable` | `false` (or `true` + self-gate, see below) | Once it fires, it can't re-fire |
| `trigger_mode` | `"manual"` (default) | Doesn't appear in Lane 1 portraits or Lane 2 random pools |
| `priority` | typically 9–12 | High enough to win against Lane 2 randoms on entry |
| `conditions` | narrative flag gates + trait gates | The story logic for "now is when this fires" |
| `schedules` | optional time window | Constrains to fictionally appropriate times |
| Flag effect on completion exit choice | sets a one-shot flag | This flag gates downstream content (Doc 50 R4 chain continuity) |

Engine entry point: `selectAutoFireCanvasForLocation` at `v2.py:3885`. When the player enters a location, engine walks all canvases tagged to that location; if a capstone's conditions match AND it hasn't fired, it REPLACES the hub render entirely. ONCE.

**`is_repeatable = true + self-gate` variant:** the canvas is technically repeatable but its `conditions` include a `flag_is_false` gate on its own setter flag. This supports Refuse-path retry — the canvas re-fires next eligible night if the Refuse branch didn't set the flag. Worked example: `scene_franks_bedroom_evening` (Doc 57 §4.1).

### §5.2 — The three types (Doc 57 §3)

| Type | Structural shape | RTS example | TLS example |
|---|---|---|---|
| **A — Linear deterministic** | One node, N cascade beats, no Pattern F fork. Sets a story flag. | `VeronicaMeet`, `MarcusParkSex`, `MarcusBedroomSex1` | `canvas_marge_interview`, `scene_ryan_first_date` |
| **B — Branching choice** | Cascade with a Pattern F fork at a decision beat. Each branch is a different downstream node or arc. | `SellingMyStepsister` (Accept → cross-NPC arc; Refuse → 2 lines) | `scene_franks_bedroom_evening` (Cross to him / Hesitate) |
| **C — Quest-chain step** | Step in a multi-step chain. Each step's flag gates the next. Each individual capstone is Type A or B internally. | RTS Edward DM arc (Pornstar DM → Date → Threesome) | Frank chain (catch → first-night → declaration → sleepover → Diana confrontation) |

### §5.3 — Type A: linear deterministic

**Use for:** first meets, intros, scripted character moments, hire events. Single-beat capstones where Maya needs to BE in the moment but doesn't need to make a choice.

**Body shape:** one `[[canvases.nodes]]` with N cascade beats. Each beat has `advance_text`. Final beat ends in the `exit_block` — usually a single "Return" or "Continue" choice that sets the flag and exits.

Length varies — Marge interview is 1,900 chars; VeronicaMeet is 10,602 chars. Focus matters more than length.

```toml
[[canvases]]
id = "canvas_marge_interview"
name = "First visit to the diner"
description = "Marge sizes Maya up in 90 seconds, hires her. Type A capstone."

[canvases.trigger]
location = "loc_diner_front"
is_repeatable = false
priority = 9
conditions = { version = "1.0", items = [
  { type = "flag", subject = "player", flag_key = "hired_at_diner", operator = "is_false" },
] }

[[canvases.nodes]]
id = "interview"
name = "Interview"
blocks = [
  { type = "image", props = { file = "scenes/marge_interview.jpg" } },
  { type = "paragraph", content = "Marge looked up when the bell over the door went off. She didn't smile." },
  { type = "dialog", npcId = "npc_marge", content = "You're Diana's girl." },
  { type = "paragraph", content = "Maya nodded. Marge looked her over once." },
  { type = "dialog", npcId = "npc_marge", content = "Five hours, four-fifty an hour, you keep your tips. Tonight if you want it." },
  { type = "paragraph", content = "She slid the apron across with the back of her hand." },
]

[canvases.nodes.exit_block]
type = "choices"

[[canvases.nodes.exit_block.choices]]
text = "Take the apron."
flagEffects = [{ targetType = "player", flag = "hired_at_diner", op = "set" }]
effects = [
  { targetType = "npc", npcId = "npc_marge", trait = "relation", op = "add", value = 2 },
]
targetType = "location"
locationId = "loc_diner_back"
```

No fork. The "Take the apron" exit is the only path. Marge wasn't waiting for an answer.

### §5.4 — Type B: branching choice (Pattern F)

**Use for:** points of no return where the player's call must matter — cross-NPC arc transfers, partner commitments, irreversible declarations.

**Body shape:** cascade reaches a fork beat. The fork beat's `advance_text` is REPLACED by two distinct exit choices in `exit_block.choices`, each pointing at a different downstream node. The downstream nodes are full sub-cascades.

**Critical:** the Refuse path is NOT a clean alternative outcome. It's a SHORTER scene. Refuse = 2 lines + return (RTS `SellingMyStepsister`) OR Refuse doesn't set the chain-completion flag (TLS `scene_franks_bedroom_evening` — Maya can hesitate tonight and accept tomorrow).

```toml
[[canvases]]
id = "scene_franks_bedroom_evening"
name = "First night"

[canvases.trigger]
location = "loc_franks_bedroom"
requires_npc = "npc_frank"
is_repeatable = true     # see note below
priority = 9
conditions = { version = "1.0", items = [
  { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_true" },
  { type = "flag", subject = "player", flag_key = "frank_bedroom_first_done", operator = "is_false" },
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 25 },
] }

[[canvases.nodes]]
id = "base"
blocks = [
  { type = "cascade", props = { beats = [
    # Beat 0: hallway approach (Tier-3 prose)
    # Beat 1: push the door open
    # Beat 2: close the door — TERMINAL of cascade; fork follows
  ]}}
]

[canvases.nodes.exit_block]
type = "choices"

[[canvases.nodes.exit_block.choices]]
text = "Cross to him."
targetType = "node"
nodeId = "scene_franks_bedroom_evening.node_first_night_climax"
effects = [{ targetType = "player", trait = "corruption", op = "add", value = 1 }]

[[canvases.nodes.exit_block.choices]]
text = "Hesitate. Step back."
targetType = "node"
nodeId = "scene_franks_bedroom_evening.node_first_night_refuse"
# No effects. Refuse does NOT set frank_bedroom_first_done — canvas re-fires next eligible night.

# Then [[canvases.nodes]] for node_first_night_climax (sets first_done flag on exit)
# Then [[canvases.nodes]] for node_first_night_refuse (sets nothing, exits)
```

**Note on `is_repeatable = true` here:** the conditions include `frank_bedroom_first_done is_false`, which means the FLAG gates re-fire rather than the `is_repeatable` field. Functionally identical to `is_repeatable = false`. Both patterns are valid; the conditions-flag variant is preferred when refuse-path retry is desired.

### §5.5 — Pattern F sub-rules (F1–F5)

When a capstone IS Type B, the fork must be authored to specific standards.

#### F1 — Both branches must be playable in good faith

Neither branch can read as "the wrong choice." Refuse must feel like a real option Maya could plausibly pick.

RTS `SellingMyStepsister`: Accept = $500 + cross-NPC arc opens. Refuse = 2 lines + return. The Refuse is short but doesn't punish — it's an honest "no." Both are playable.

TLS `scene_franks_bedroom_evening`: "Cross to him" = climax cascade. "Hesitate. Step back" = refuse-and-leave path that doesn't set the chain-completion flag. Refuse-now-accept-later is a legitimate playthrough.

#### F2 — The branches must diverge in DOWNSTREAM effect, not just text

Real divergence:
- Different flag set (refuse doesn't set the chain-completion flag)
- Different NPC arc opens (cross-NPC transfer)
- Different downstream cascade content (continues vs. cuts short)
- Material trait effect difference (corruption +5 vs +0)

If both branches set the same flag and lead to similar content with cosmetic text differences, collapse to Type A with two flavors.

**Borderline Type B:** acceptable when secondary divergence is real downstream content (church-path adds `rep_church +3` + church-regulars dialog tracks; home-path adds nothing equivalent). Both branches must set the same primary progression flag (else the rent-and-week-passed progression breaks), but secondary effects diverge meaningfully. Worked example: `canvas_first_sunday_morning` (Doc 57 §F2).

#### F3 — The fork beat should be the cascade's TERMINAL beat

The cascade plays through to the moment of decision. The decision is the LAST authored act before `exit_block.choices` fork. Don't have the player make the choice mid-cascade with N beats of content downstream of both branches — that's just two parallel scenes glued together.

#### F4 — Refuse paths can keep the canvas alive for retry

If Refuse doesn't set the chain-completion flag, the capstone re-fires next eligible time. Legitimate. *"Cross to him in the bedroom"* is reversible — Refuse should let Maya try again.

If Refuse DOES set the flag (or a sibling flag closing the arc), the capstone is irreversible. *"Sell my stepsister"* is irreversible — Refuse closes that scene's possibility.

Either side is valid; match to the fiction.

#### F5 — Don't compound Pattern F with mid-branch tier-routing

`scene_franks_bedroom_evening` currently does this — the climax node has T0 (corruption < 40) vs T1 (corruption ≥ 40) closing register inside the Accept branch. Two structural devices stacked. This is the UPPER BOUND of complexity per capstone; don't push further (e.g., three-way fork with tier-routing in two branches). The player loses the structural read.

### §5.6 — Type C: quest-chain step

**Use for:** multi-beat narrative arcs where the player progresses through distinct authored moments — relationship escalation, career-arc unlocks, slow-burn revelations.

Each individual capstone in a Type C chain is internally Type A or Type B. The "Type C-ness" is the CHAIN shape — Capstone1 sets Flag1 → gates Capstone2 → sets Flag2 → gates Capstone3, etc.

**Frank's chain (verified):**

```
scene_livingroom_catch  (Type A — sets frank_caught)
→ scene_franks_bedroom_evening  (Type B — sets frank_bedroom_first_done on Accept)
→ scene_frank_declaration  (Type A — sets frank_cracked)
→ scene_frank_sleepover  (Type A — sets frank_sleepover_done)
→ scene_diana_confrontation  (Type A — sets diana_confronted)
```

Each capstone is one beat. The flag-setter pattern means the chain IS BOTH the trigger condition for the next AND the quest-card pointer (Doc 50 R1 + R4 — see `doctrine/04_authoring_rules.md`).

### §5.7 — Per-NPC capstone budgets (Doc 57 §5)

| Arc shape | Type A | Type B | Type C chain length | Total capstones |
|---|---|---|---|---|
| **Family/ambient** | 1–2 | 1–2 | 4–5 | 3–6 |
| **Slow-burn family** | 1–2 | 0–1 | 2–3 | 2–5 |
| **Peer/dating** | 1–2 | 0–1 | 2–3 | 2–5 |
| **Service** | 1 | 0 | 1–2 | 1–3 |
| **Antagonist/witness** | 1–2 | 0–1 | 1–2 | 1–3 |

**Ratio guidance:** Type B should be roughly 20–25% of an arc's capstone count, matching RTS's pattern. Higher = choice-heavy arc; lower = authored-fated. Either is intentional; just know which.

**Total per arc:** small (1–3 for service/antagonist), medium (2–5 for peer/slow-burn), large (3–6 for family/ambient). An arc with 7+ capstones is doctrine drift — collapse some into Lane 1 menu items or Lane 2 ambients.

### §5.8 — Voice register: Tier-3 EARNED

Capstones get Tier-3 prose. Lane 1/2/3 don't.

**Tier-3 = the rich register reserved for once-only scenes:**
- Interior monologue + observation tied to memory (*"the boards she knows the squeak of from the wrong side"*)
- Layered sensory detail per beat
- Character-distinguishing diction (Frank's "girl"/"quiet"; Marge's "hon"; Ryan's "okay, good")
- Composed rhythm — sentences of varying length, deliberate cadence

**Tier-3 is NOT:**
- Generic literary prose. Specific to the scene's people + place.
- Melodramatic. The prose stays controlled.
- Unlimited length. Marge interview is 1,900 chars; Frank first-night cascade is ~5,000 chars across multi-node. Density is HIGH; scene length is bounded by what the moment needs.

**Why capstones earn Tier-3 (and Lane 2/3 don't):** a Lane 2 ambient fires 10–20 times across an arc. Authoring it with Tier-3 prose costs the same EACH TIME and after the third reading the language feels performative. Lane 2/3 prose is built to be re-readable without grating — that's why it stays RTS-flat structure with specific detail.

A Type A or Type B capstone fires ONCE. The prose can be denser because there's no re-reading.

**Anti-patterns:**
- Tier-3 voice leaking into Lane 2/3. Extract the prose; move it to a capstone; rewrite the Lane 2/3 canvas RTS-flat.
- RTS-flat-bland voice in capstone. Wastes the once-only nature. Earn the single read by being specific, layered, resonant.

---

## §6 — Arc-flow doctrine: Lane 1 leads, Lanes 2+3+4 follow

The most important framing in the whole framework.

> **Lane 1 leads the arc; Lanes 2/3 follow as consequences of Lane 1 escalation. Lane 4 capstones gate the arc's milestones, fired by stat-threshold + flag combinations Lane 1 produces.**

The player drives the relationship by clicking Lane 1 buttons (Tease, Flash, Sex). Each click raises stats (Maya corruption, NPC arousal, NPC corruption, NPC relation). When stats cross thresholds, **Lane 2 and Lane 3 content lights up as a consequence** — random encounters become eligible, walk-ins start firing inside daily activities. **Lane 4 capstones gate on the threshold crossings + flag chain.**

This produces the "world fills out around me as I escalate" feeling. The player feels their intentional choices are reshaping the world.

**Even though Lane 2/3 outnumber Lane 1 by canvas count (10/15 of Brother's surfaces vs. 5/15), Lane 1 is the causal driver.** Without Lane 1 escalation, most Lane 2/3 content stays dormant.

The inverse design — "Lane 2/3 lead, Lane 1 follows" — produces a passive game where things keep happening to Maya regardless of her choices. RTS deliberately doesn't do this.

**Cold-start on-ramp (Doc 72 R4).** Because Lane 1 leads, every arc must be *enterable* from a cold start — corruption 0, no flags set — through ordinary presence. The first beat of an arc needs only co-presence (Maya in the room with the NPC, who is there per schedule), and that co-presence is delivered by the NPC's Lane 1 hub at that location, which renders its base unconditionally (the presence floor, §2.8 / D72-R6); escalation conditions layer on *after* that first beat. Never gate an arc's entry on a stat that can only be raised by content downstream of that same arc — that circular gate (the **backwards on-ramp**, §8.12) leaves the cold-start player unable to begin. Location-entry gating is still fine where *entering is itself the first contact* (the diner behind "get hired" — walking in to ask for the job is the first interaction); the on-ramp rule targets people already in the player's everyday space (housemates, neighbours, coworkers-on-shift).

### §6.1 — Per-NPC progression: shared stat thresholds across lanes

When one threshold crosses, MULTIPLE gates clear simultaneously:

| Frank threshold | Lane 1 effect | Lane 2 effect | Lane 3 effect | Lane 4 effect |
|---|---|---|---|---|
| Stage 2 (post-catch) | New "Stand close while he reads" button in office hub | Random hallway-pass-by ambient eligible | Cook-breakfast dispatcher rolls Frank vignette at 33% | (next capstone in chain gates on stage 2) |
| Stage 3 (post-declaration) | Office hub adds "After hours" button | Office-after-hours peep eligible | Read-newspaper dispatcher rolls Frank-on-couch at 25% | Sleepover capstone unlocks |
| Stage 4 (post-sleepover) | Bedroom hub unlocks | Bedroom door-open ambient | Wash-dishes dispatcher rolls Frank-behind-you at 33% | Diana confrontation capstone unlocks |

**One stat threshold = multiple gates clear = "world feels alive."** Player doesn't think "the kitchen menu changed"; they think "Frank is suddenly everywhere." That perception is the doctrine producing player-felt effects.

---

## §7 — The 3×3 grid + content-type vocabulary

Within each lane, scene intensity scales with stat tier (Pattern D mechanism — same scene entry, deeper cascade as stats grow). Crossing the lane axis with the tier axis produces the canonical authoring template:

| | **Lane 1 (intentional)** | **Lane 2 (ambient)** | **Lane 3 (walk-in)** |
|---|---|---|---|
| **Tier 1 — early arc** (low stats) | Talk-style relational | He passes by (presence) | He notices what you're doing (PG charged) |
| **Tier 2 — mid arc** (mid stats) | Tease / Flash / mild self-display | He gropes you while studying (passive contact) | He walks in mid-change (interruption + dialogue) |
| **Tier 3 — late arc** (high stats) | Sex / Sleep with him (explicit intentional) | Caught masturbating, sexual ambient encounter | He joins you in the shower (full walk-in cascade with consummation) |

**Doctrine for grid imbalance:**
- All Lane 1 → fully transactional, low surprise, "menu game" feel
- All Lane 2 → atmospheric but inert, Maya passive throughout
- All Lane 3 → things constantly happen TO Maya, no agency over outcomes
- **Mix across all three lanes, all three tiers → alive**

Lane 4 capstones sit OUTSIDE the grid — they're the once-only milestones that gate the stat tier crossings.

---

## §8 — Anti-patterns (concrete shapes to NOT ship)

### §8.1 — Verb overlay anti-pattern

Don't define "Tease" as a verb that follows the NPC wherever they are. RTS doesn't. Tease in the bedroom (lights-out intimacy) reads differently than Tease in the kitchen (Diana-down-the-hall risk) than Tease in the office (rule-break). A single verb canvas teleporting can't write to all three contexts honestly.

**Per-context authoring + shared stat thresholds + Lane 3 dispatcher substitutions** is the doctrine. Each location-specific scene is its own canvas with its own preamble and cascade. Shared stat thresholds make them light up together. Lane 3 substitutions slip the NPC into existing solo activities.

### §8.2 — Conflating Lane 1 hub with location-work surfaces

NPC hub canvas is for **Maya-NPC interactions ONLY.** Solo Maya activities at the same location (work, chores, errands) live as their own canvases PARALLEL to the hub. Lane 3 substitutions can later route the NPC INTO solo activities — that's a different mechanism than the hub menu.

Three surfaces at the same location can coexist independently:
- **NPC hub** (Maya-with-NPC, Lane 1)
- **Solo work canvas** (Maya-only, location-triggered)
- **Lane 3 dispatcher** (Maya-only with substitution rule routing NPC in)

Anti-pattern: putting shifts + Maya-solo work activities (refill_caddies, wipe_booths) in the NPC's hub menu. Doc 54 §3.3 case study.

### §8.3 — Verb register: pronoun-in-the-verb test

Read each proposed hub menu choice. If the NPC is NOT the syntactic object of the verb, it's not Lane 1.

- *"Pour her coffee"* → her ✓ — Lane 1
- *"Tease her"* → her ✓ — Lane 1
- *"Take a long shift"* → no NPC pronoun ❌ — not Lane 1 (location-work canvas instead)
- *"Close out the diner"* → no NPC pronoun (even if NPC is off-stage during the close) ❌

Doc 54 §3.2 case study.

### §8.4 — Lane 2/3 forced on non-escalation register

When an NPC's slice scope defers the sexual/escalation register, **Lane 2 and Lane 3 are EMPTY in slice.** Empty cells are honest. Filling them with relational/atmospheric texture is the violation, not the omission.

Service NPCs (Marge): empty Lane 2 + empty Lane 3.
Peer/dating NPCs (Ryan): empty Lane 3 always; Lane 2 ambient at low density.
Antagonist NPCs (Diana): empty own Lane 3; Diana appears as INTERRUPTOR in Frank's Lane 3 endings.

Doc 54 §3.4 case study.

### §8.5 — Frank-cloning a non-family-ambient NPC

Copying Frank's 28-canvas distribution onto Ryan's peer/dating shape produces 13 Lane 2 ambients + 7 Lane 3 substitutions where neither belongs. The shape is right; the cloning is wrong.

Each arc shape has its own canvas distribution per `doctrine/03_arc_shapes.md`. Author against the shape, not against the gold-standard NPC.

### §8.6 — Pattern B authored as multiple Pattern A rules with chance < 1

Wrong since Doc 69 Item 1 shipped (2026-05-27). The `exclusive_group` field on each substitution rule gives mutex-correct dice partition + fall-to-solo on failed conditions natively. Emit Pattern B directly per §4.6.2 — do NOT approximate via summed Pattern A chances.

### §8.7 — Stat cost in wrong placement (Pattern A vs C)

If Exercise costs Energy only in the `exit_block` (Pattern A placement), the workout doesn't "count" when Grandpa walks in — but Pattern C design says it SHOULD. Place unconditional effects in `pre_substitution_effects` (Pattern C).

### §8.8 — Strict location check on Lane 3 walk-in dispatcher

Lane 3 walk-in = "NPC walks in on Maya" = loose `IsNpcAtHome` check. Tightening Lane 3 to "NPC must already be in kitchen" breaks the fictional intent — Frank wandered into the kitchen because Maya was there, he didn't pre-stage himself.

### §8.9 — No `max_triggers_per_day` on Lane 3 substitution target

Same scene firing 5 times in one day breaks the "once per day" cadence RTS uses. Doc 67 R7.

### §8.10 — Substitution target not marked `substitution_only`

Then it appears in the NPC portrait hub at the location, the player can click it directly — defeating the "you were doing X and he happened" fictional intent. Pre-ship check: every Lane 3 substitution target has `substitution_only = true`.

### §8.11 — Dead presence (NPC present, visiting yields nothing)

An NPC is scheduled at a reachable location (and shows on the schedule page), but visiting renders nothing — no base moment, no acknowledgement. The player acts on the schedule, walks to where the NPC is, and gets an empty room; the world reads as a set of locked doors. Two causes: escalation-only authoring (only stage-1+ beats written, no unconditional base node), OR relying on a probabilistic Lane 2 ambient to do the acknowledging (a `chance` dice roll is not a floor — most visits still render nothing). Fix: a **Lane 1 hub** whose `base` node renders unconditionally, per schedule row (§2.8 / D72-R6); gate escalation *choices*, never the act of seeing the NPC. (The hub-per-row requirement is hard; the *choices* on it are still logic-driven — "sometimes none" is a valid choice list. What's banned is the absent or probabilistic base, not a thin menu.) This is the *reachable*-location case; an NPC scheduled at an *unreachable* / locked location is a different failure — §8.15 + `doctrine/10` §5.4.

### §8.12 — Backwards on-ramp (arc entry gated on downstream stat)

An arc's entry condition is a stat or flag that can only be raised by content downstream of that same arc — a circular gate. The cold-start player can never begin it; they stall staring at locked affordances. Distinct from §8.4 (lane forced on wrong register): here the arc legitimately exists, but its front door is locked with a key that's inside the room. Worked anti-example: a housemate arc that only opens at `worn_corruption ≥ 15`, i.e. the player must buy and wear provocative clothing before her own housemate will register her. Fix: the arc's first beat needs only co-presence; escalation layers after (§6 cold-start on-ramp, Doc 72 R4).

### §8.13 — Hub window narrower than the schedule (D72-R6)

A Lane 1 hub exists at the location, but its own `trigger.schedules` covers only a slice of the NPC's scheduled presence there — so the rest of the rows are dead. Worked anti-example: Hank is scheduled at the diner front 06:00–22:00 (plus late night), but `hank_diner_front_hub` opens only 22:00–01:30; from 06:00–22:00 every day the schedule page shows him there and the room renders no hub. "A hub at the location" is not coverage — the hub must be *open during that window*. Fix: period-split into per-window hubs, each with `trigger.schedules` matching its row (§2.8, D72-R6). The build does NOT catch this — it's a silent runtime gap.

### §8.14 — Cloned full ladder across locations / public-space escalation (D72-R7)

The same full escalation ladder is offered at every one of an NPC's hubs regardless of context — e.g. "Have sex with him" clickable at the public diner counter mid-rush. This is the verb-overlay anti-pattern (§8.1) in hub form: it ignores that the act can't happen there (and that the NPC won't risk it). Fix: scale each hub's rung set to the location's exposure tier (§2.9) — public = talk/look only, semi-private = tease/grope, private = full ladder. The relationship state stays global, so consistency is preserved without cloning the ladder into rooms that can't support it (D72-R8).

### §8.15 — NPC vanishes into a locked room (present-but-unreachable)

An NPC's `[[npcs.schedules]]` sends them into a **locked** location (a `[[locations]]` with `entry_conditions`) during a window the player routinely shares — so they leave the reachable floor for a room the player can't enter, with no open-location fallback and/or an illegible gate. The player watches them step away and gets "where did they go?" Distinct from §8.11: that is an NPC at a *reachable* location rendering nothing; this is an NPC at an *unreachable* location. Fix: the **unlock contract** (`doctrine/10` §5.4) — make the lock legible (visible-but-blocked, so it reads as a closed door), keep the locked window in off-hours the player doesn't share *or* co-gate the door with the same flag that gates the player's access, and ensure open-location fallback presence; or open the door and gate the canvas/choices instead. The *acceptable* form (e.g. a boss who does paperwork in a locked office 01:30–06:00, on the open floor up to 01:30 and from 06:00) is a **bounded, legible** window — not this anti-pattern. The hard bug is an NPC reachable *only* via a locked location (`doctrine/10` §5.4 Case C).

---

## §9 — Engine support summary

| Lane | TLS engine support |
|---|---|
| **Lane 1** — Hub button | ✅ Native via NPC portraits + `exit_block.choices` + per-choice conditions |
| **Lane 2** — Location-entry random | ✅ Native via `trigger_mode = "random"` + `chance` |
| **Lane 3** — Pattern A dispatcher | ✅ Native via `substitutions` + `substitution_only` (`v2.py:4649`) |
| **Lane 3** — Pattern B dispatcher | ✅ Native via `exclusive_group` per rule (`v2.py:4671-4713`, Doc 69 Item 1 shipped 2026-05-27) |
| **Lane 3** — Pattern C dispatcher | ✅ Native via `pre_substitution_effects` on parent trigger (`v2.py:11151`, Doc 69 Item 2 shipped 2026-05-27) |
| **Lane 4** — Capstone auto-fire | ✅ Native via `selectAutoFireCanvasForLocation` + priority ≥ 9 + flag-gate |
| **`IsNpcAtHome` (loose)** | ✅ via `requires_npc` + NPC schedule at meta-location |
| **`GetNpcLocation == X` (strict)** | ✅ Native |
| **`executedToday` per-day cap** | ✅ via `max_triggers_per_day = 1` |
| **`previous()` guard** | ⚠️ Approximation via flag set/clear |

---

## §10 — Cross-references

### Sibling doctrine files

- `doctrine/01_rts_principles.md` — P1–P10, especially P3 (one scene multiple lengths), P5 (lanes = fictional intent), P8 (author no-return; mechanize texture)
- `doctrine/03_arc_shapes.md` — per-arc canvas distribution that drives lane budget
- `doctrine/04_authoring_rules.md` — R1–R7 from Doc 56 + R1–R5 from Doc 57 + Doc 67 R1–R7
- `doctrine/05_rts_flat_prose.md` — voice register (RTS-flat default; Tier-3 capstones)
- `doctrine/09_trait_catalog.md` — trait vocabulary used in lane gating

### Schema files

- `schema/01_engine_capabilities.md` §3 (canvas + trigger) + §4 (Lane 3 substitution) + §5 (schedule + NPC presence)
- `schema/02_toml_schema.md` §5–§7 (canvas + trigger + node schema)

### Source docs

- `28th_april_TLS_Phase2_Redesign/24_RTS_Three_Lanes_Repeatable_Activities.md` — Lane mechanism source
- `28th_april_TLS_Phase2_Redesign/57_Capstone_Doctrine.md` — Lane 4 source
- `28th_april_TLS_Phase2_Redesign/67_Solo_Activity_Design_and_Multi_NPC_Dispatcher_Doctrine.md` — solo activity + dispatcher patterns source
- `28th_april_TLS_Phase2_Redesign/72_Presence_and_Logic_Driven_Interaction_Doctrine.md` — presence floor + logic-driven interaction. R6–R8 (per-schedule-row Lane 1 hubs + exposure-tier ladder ceiling + same-NPC hub consistency) live in `doctrine/04` §6 — see §2.8 + §2.9 + §6 + §8.11–§8.14

### Engine primitives

- `setup.renderNpcPortraits` (`v2.py:4295`) — Lane 1 portraits
- `setup.checkRandomEncounters` (`v2.py:4520`) — Lane 2 dispatcher
- `setup.checkAndSubstituteCanvas` (`v2.py:4649`) — Lane 3 substitution
- `setup.selectAutoFireCanvasForLocation` (`v2.py:3885`) — Lane 4 capstone auto-fire

---

**End of file.** Next: `doctrine/03_arc_shapes.md` for per-arc canvas distribution.

═══════════════════════════════════════════════════════════════════════════════

## 7. 03_arc_shapes

**Source:** `prompts_v2/doctrine/03_arc_shapes.md`

---

# Doctrine 03 — Arc Shapes + Per-Shape Canvas Distribution

**Sources:** Doc 56 §5 (per-arc distribution table); Docs 31 (Frank), 53 (Marge), 58 (Ryan), 59 (Jake), 60 (Diana), 61 (Cookie scope-out).
**Authority:** Doctrine. Every NPC in every RTS-shape sandbox picks ONE arc shape from the five below. The shape determines the mechanical rhythm of the arc + the per-lane canvas budget.
**Purpose:** Replace the legacy 7-driver NPC-archetype system (per `00_LEGACY_IGNORE.md` §3.3). Each shape comes with a worked-example NPC + canvas distribution table + voice register guidance + budget bounds.

Cross-reference: `doctrine/02_three_lanes_plus_capstone.md` for the lane mechanisms this distribution sits inside. `doctrine/04_authoring_rules.md` R3 + R7 for the rules that operationalize shape selection.

---

**Scope-mode note (read before §2 budget tables):**

The per-arc-shape canvas budgets in §2 are **FULL-ARC targets** — they describe the complete shipped game across all phases, not a slice. Authoring at:

- **`scope_mode: full_game`** (default) — author up to the full budget per shape. All Stage 0→4 content. Full capstone chains.
- **`scope_mode: slice`** — author a subset (typically 30–50% of budget) + locked-visible rungs telegraphing the deferred remainder.

RTS is the existence proof — Brother (family/ambient) shipped at 15–16 distinct canvases (cluster-merged from a larger surface), landing inside the 25–35 full-arc budget. See `reference/02_rts_scene_catalog.md` for the per-NPC count evidence. The budget table is not aspirational; it's RTS-validated.

---

## §1 — The five arc shapes

Every NPC in an RTS-shape sandbox runs ONE of these five rhythms. The shape is declared in the R7 design brief BEFORE any canvas is authored (Doc 54 §2.3 + Doc 56 R7).

| Shape | Mechanical rhythm | RTS reference | TLS reference |
|---|---|---|---|
| **Family/ambient** | Daily proximity + saturated chore presence + escalating intimacy. The dense shape. | Stepbrother (15 scenes, 47% Lane 3) | Frank |
| **Slow-burn family** | Family but distant; discrete revelation beats; Lane 3 walk-ins ARE the milestones | (no direct RTS analog — slow-burn-incest is rare in RTS catalog) | Jake |
| **Peer/dating** | Scheduled visits; quest-chain progression; relation-driven; no walk-ins | Marcus (5 scenes, all deterministic chance=100%, quest chain) | Ryan |
| **Service** | Workplace register; relation-driven; arousal/corruption don't apply | (no direct RTS analog; Marge designed against RTS service-NPC absence) | Marge |
| **Antagonist/witness** | Silent awareness accumulator; confrontation capstone; no own Lane 3 (appears as interruptor in others') | (no direct RTS analog; Diana modeled on mother-discovers-affair drama) | Diana |

**Why five and not more:** these five cover the mechanical rhythms RTS uses + the slot mechanics the TLS engine supports natively (Lane 1/2/3 + Lane 4 capstones). Adding a sixth requires either an engine extension OR doctrine extension; both are out of scope until a load-bearing use case arises.

---

## §2 — Per-shape canvas distribution (Doc 56 §5)

The reference table for what each shape's canvas distribution should LOOK like. Cell values are guidelines, not quotas — the R7 brief commits to specific numbers within these ranges.

| Lane / Tier | Family/ambient (Frank) | Slow-burn family (Jake) | Peer/dating (Ryan) | Service (Marge) | Antagonist (Diana) |
|---|---|---|---|---|---|
| **L1 / T1** | 1–2 base + 1–2 self-display | 1 (room visit) | 1 (visit at workplace) | 1 (workplace base) | 0–1 (shared-space neutral) |
| **L1 / T2** | 1–2 mid escalation | 0–1 (charged moment) | 0–1 (date intro) | 0 | 0 (no escalation register) |
| **L1 / T3** | 1–2 explicit | 0–1 (consummation if vocab allows) | 0–1 (commit beat) | 0 | 0 |
| **L2 / T1** | 1–2 morning/passing | 0–1 (corridor) | 1 (workplace ambient) | 1 (workplace texture) | 1–2 (presence beats) |
| **L2 / T2** | 2–3 evening/charged | 0–1 (charged corridor) | 0–1 (low density) | 0–1 | 1–2 (charged presence) |
| **L2 / T3** | 1–2 late-night/explicit | 0 | 0 | 0 | 0–1 (confrontation precursors) |
| **L3 / T1–T3** | 4–7 walk-ins on chores | 1–3 (discrete revelation walk-ins) | 0 | 0 | 0 own (appears in others' L3) |
| **Capstones** | 4–6 (catch, declare, first-night, sleepover, Diana confrontation) | 3–5 (transitions + revelation + relationship turn) | 3–4 (dating chain) | 1–2 (hire + escalation if vocab allows) | 1–2 (confrontation, resolution) |

**Total canvas budget by shape:**

| Shape | Range | Notes |
|---|---|---|
| Family/ambient | **25–35** | The dense shape; Frank is the gold standard |
| Slow-burn family | **10–15** | Sparse but focused; slow-burn-incest works because each beat is concentrated |
| Peer/dating | **8–12** | Quest-chain progression; capstones do the heavy lifting |
| Service | **6–10** | Bounded by workplace register + Phase 2+ deferrals |
| Antagonist/witness | **6–10 standalone** + cross-appearances in others' arcs | Diana standalone count is low; her presence saturates Frank's lanes |

**Empty cells are honest.** If the shape has 0 in a cell, the brief commits to 0. Filling empty cells with relational/atmospheric texture is the Doc 54 Marge failure mode — soft drift toward "fill the world" that violates the shape.

**The L1 cells above count *escalation* rungs, not hubs.** The number of Lane 1 **hubs** is set separately by presence: one hub per distinct `[[npcs.schedules]]` row (location × window) — D72-R6, `doctrine/04` §6.1. An NPC scheduled across 5 windows has 5 hubs even if the escalation budget is small; the extra hubs are *light* (base + talk + leave, exposure-tier-capped per D72-R7), not extra escalation. "Empty cells are honest" governs L2/L3 *escalation* surfaces — it does NOT excuse a missing presence hub: even service/antagonist NPCs get a light hub at each scheduled location. Presence floor (a hub) and escalation register (the rungs on it) are independent axes.

---

## §3 — Family/ambient (Frank — the dense reference)

### §3.1 — Mechanical rhythm

Maya and the NPC share a household. Daily proximity. Saturated chore presence. Escalating intimacy from neutral co-existence → first sexual contact → declared partnership → terminal-state routine.

**Lane 3 is the dominant lane.** Brother in RTS = 47% Lane 3 (7 of 15 scenes). The shape requires that Maya can't get through her chores without encountering the NPC — that's what makes the world feel alive with them.

### §3.2 — Canvas distribution (Frank slice, post-Phase E1 redesign)

| Lane | Tier | Canvas count | Examples |
|---|---|---|---|
| L1 | T1 | 2 base + 2 self-display | `frank_kitchen_morning_hub`, `frank_kitchen_dinner_hub`, `tease_kitchen_general`, `flash_kitchen_general` |
| L1 | T2 | 2 mid | `loop_franks_bedroom_finisher` partial, hub variants |
| L1 | T3 | 2 explicit | `loop_franks_bedroom_finisher` deep loop, related |
| L2 | T1 | 2 morning | `ambient_kitchen_morning_chat`, `ambient_kitchen_coffee_alone` |
| L2 | T2 | 3 evening | `ambient_livingroom_paper`, `ambient_livingroom_tv`, `ambient_kitchen_dinprep_grope` |
| L2 | T3 | 1 late-night | `ambient_kitchen_late_night_raid` |
| L3 | T1–T3 | 7 substitutions | `scene_frank_passes_kitchen_door`, `scene_frank_arrives_during_coffee`, `scene_frank_joins_porch`, `scene_frank_joins_couch`, `scene_frank_at_kitchen_sink_behind`, `scene_frank_at_open_bathroom_door`, `scene_frank_walks_in_shower` |
| Capstones | — | 5 | `scene_livingroom_catch` → `scene_franks_bedroom_evening` → `scene_frank_declaration` → `scene_frank_sleepover` → `scene_diana_confrontation` |

**Total Frank canvases: ~28.** Within the 25–35 range.

### §3.3 — Per-NPC stat ladder

Frank uses the universal corruption-tier model (Doc 30 §4.4):

| Tier | Maya corruption | Capstone gate | Content type |
|---|---|---|---|
| 0 | 0+ | none | Brushed contact / accidental |
| 1 | 5+ | none | Tease / Flash (visual only) |
| 2 | 15+ | none | Fondle / explicit physical (clothed) |
| 3 | 25+ | post-catch | Explicit sex acts (oral / partial sex) |
| 4 | 35+ | post-cracked | Full sex |
| 5 | 50+ | post-first-night | Routine intimacy / sleepover / breeding |

### §3.4 — Sidebar visibility (Doc 68 §8)

Family/ambient default: **location + arousal + corruption + relation** all surface. Player needs to plan Lane 3 attempts (arousal), Lane 1 escalation (corruption), late-game intimacy (relation). RTS surfaces all three for family NPCs (Stepbrother/Stepfather/Stepgrandfather) — verified live.

Stage NEVER surfaces (Doc 68 §9).

### §3.5 — Voice register

- Lane 1/2/3: RTS-flat default. ~30-word caption density. Direct/crude diction per per-arc vocab ceiling (`doctrine/08_kink_vocab_ceilings.md`).
- Lane 4 capstones: Tier-3 earned. Interior monologue + layered sensory detail + character-distinguishing diction.

### §3.6 — Doc 31 design brief (Frank) — gold standard

`28th_april_TLS_Phase2_Redesign/31_Frank_Arc_Design_Brief.md` is the R7 reference for family/ambient. Read it when authoring a new family/ambient NPC.

---

## §4 — Slow-burn family (Jake)

### §4.1 — Mechanical rhythm

Family by relation but distant by interaction. Stage 0–4 ladder: Hostile → Noticed → Peek/Draw → Tease → Caught. The arc is sparser than Frank because each beat is concentrated — slow-burn-incest works because each revelation is a moment, not a routine.

Lane 3 walk-ins ARE the milestones — not 7 routine substitutions like Frank, but 1–3 discrete revelation beats keyed to specific arc moments.

### §4.2 — Canvas distribution (Jake slice — Doc 59 brief)

| Lane | Tier | Canvas count | Examples (planned per Doc 59) |
|---|---|---|---|
| L1 | T1 | 1 (room visit) | `jake_room_visit` |
| L1 | T2 | 0–1 (charged moment) | Stage 2 admit (Type A capstone) |
| L1 | T3 | 0–1 (Phase 2+ consummation) | Phase 2+ |
| L2 | T1 | 1 (corridor) | `ambient_jake_corridor_passing` |
| L2 | T2 | 1 (charged corridor) | `ambient_jake_hallway_glance` |
| L2 | T3 | 0 | — |
| L3 | T1–T3 | 1–3 (revelation beats) | `scene_jake_walks_in_change`, `scene_jake_maya_solo_sketch` |
| Capstones | — | 3–5 | Transition reveal + charged consummation + relationship turn |

**Total Jake canvases: ~10–12.** Within the 10–15 range.

### §4.3 — Stage ladder + dual-path 0→1 (Doc 57 §9)

Jake's Stage 0→1 transition is dual-path: via `transition_jake_to_1_via_beauty` (Maya wears the right outfit) OR `transition_jake_to_1_via_glance` (Maya catches him looking). Both share verbatim body prose — the engine constraint (OR-logic in stage_helpers is banned) forced two-canvas pattern; the narrative moment is one beat.

This is NOT an anti-pattern. The duplicate-prose engine exemption (Doc 57 §9) covers this: when an engine constraint forces multiple canvases for a single narrative moment, identical body prose across the duplicates is acceptable. Mark with a comment naming the constraint.

### §4.4 — Sidebar visibility (Doc 68 §8)

Slow-burn family default: **location + arousal + relation.** Corruption stays low in slow-burn arcs by design; surfacing it would mislead the player. Arousal + relation are the player-relevant dimensions.

### §4.5 — Voice register

Same Lane 1/2/3 vs Lane 4 split as family/ambient, but per-arc vocab ceiling is FULL INCEST CALLOUTS (per Doc 30 §7.5) — "brother" / "sis" / "little sister" callouts during sex; explicit reference to taboo ("this is so fucking wrong," "my own brother"). Incest IS the kink — named and dwelt on at all tiers.

### §4.6 — Doc 59 design brief (Jake)

`28th_april_TLS_Phase2_Redesign/59_Jake_Design_Brief.md`. Stage 0–4 ladder, dual-path transition, per-lane budget L1 1–2 + L2 1–2 + **L3 1–3** (slow-burn DOES get walk-ins, unlike peer/dating) + capstones 3–5.

---

## §5 — Peer/dating (Ryan)

### §5.1 — Mechanical rhythm

Separate household. Scheduled interactions. Relation-driven. Quest-chain progression — Stage 0 (meet) → Stage 1 (notice) → Stage 2 (partner) → Stage 3 (consummation, Phase 2+) → Stage 4 (relationship beat).

**Lane 3 budget = 0.** Peer doesn't interrupt private chores. The arc lives in Lane 1 visits + Lane 2 workplace ambient + capstone dates.

**Ongoing Stage-4 hub (required — Late Shifts B6).** A peer/dating arc needs a REPEATABLE Lane-1 hub at the partner's location for the post-consummation (Stage 4) state — not just a one-shot first-night capstone. Without it, the arc has no surface after consummation: nothing to revisit, and Phase-2+ content (e.g. pregnant variants) has nowhere to attach. Pattern: the partner's home is access-gated on the relationship flag (e.g. `cole_date_done`); the ongoing hub gates on the consummation flag (e.g. `cole_first_night_done`) at a priority BELOW the first-night capstone (so the capstone fires first, then the hub takes over). The hub's NPC must be schedule-present at that location, or the portrait won't render (`doctrine/10` §5.2). Late Shifts shipped Cole with only the first-night capstone — the missing ongoing hub surfaced only when authoring pregnant variants.

### §5.2 — Canvas distribution (Ryan slice — Doc 58 brief)

| Lane | Tier | Canvas count | Examples |
|---|---|---|---|
| L1 | T1 | 1 (visit at workplace/yard) | `visit_ryan_at_yard`, `activity_help_ryan_in_yard` |
| L1 | T2 | 0–1 (date intro / charged) | `ryan_porch_chat` |
| L1 | T3 | 0–1 (commit beat) | `scene_ryan_partner_commit` (Phase 2+) |
| L2 | T1 | 1 (workplace ambient) | `scene_yard_with_ryan` |
| L2 | T2 | 0–1 (low density) | (sketchy slot — deferred) |
| L2 | T3 | 0 | — |
| L3 | — | **0** | Peer doesn't interrupt private chores |
| Capstones | — | 3–4 | `transition_ryan_to_1`, `scene_ryan_first_date`, second-date (Type A), partner-commit (Type B) |

**Total Ryan canvases: ~8–10.** Within the 8–12 range. Doc 58 surfaces ~3–4 new canvases needed beyond current 6 (workplace L1, porch L2, second-date Type A, partner-commit Type B).

### §5.3 — Sidebar visibility (Doc 68 §8)

Peer/dating default: **location + relation only.** Dating chain is relation-driven. Arousal is bounded + less player-controllable. Corruption isn't meaningful for peer arcs (most peer NPCs cap low).

### §5.4 — Voice register

Lane 1/2 RTS-flat; capstones Tier-3 earned. Per-arc vocab ceiling: open question per Doc 58 §3 — does Ryan's arc include a sexual tier, or is it Stage-2 wholesome dating only? Phase 2+ scope.

### §5.5 — Doc 58 design brief (Ryan)

`28th_april_TLS_Phase2_Redesign/58_Ryan_Design_Brief.md`. Per-lane budget L1 2–3 + L2 1–2 + **L3 = 0** + capstones 3–4. Slice scope = Stage 2 partner. Phase 2+ = Stage 3+ consummation.

---

## §6 — Service (Marge)

### §6.1 — Mechanical rhythm

Workplace register. Maya hired into a service position; the NPC is the employer/manager/colleague. Bond builds via shifts worked + workplace conversations.

**Lane 3 budget = 0.** Workplace-only register; private space is not their setting. No walk-ins.
**Lane 1 = bounded.** Hub menu items are workplace verbs (Pour coffee, Talk a minute) — Maya-with-NPC interactions, not work-tasks (work-tasks live as separate solo-activity canvases parallel to the hub per `doctrine/02_three_lanes_plus_capstone.md` §8.2).

### §6.2 — Canvas distribution (Marge slice — Doc 53 brief, applied lessons)

| Lane | Tier | Canvas count | Examples |
|---|---|---|---|
| L1 | T1 | 1 (workplace base) | `scene_marge_diner_hub` |
| L1 | T2 | 0 | Empty (service register; no escalation in slice) |
| L1 | T3 | 0 | Empty (Phase 3+ workplace seduction scoped out per Doc 30 §8.2) |
| L2 | T1 | 1 (workplace texture) | `scene_diner_t0_shift` (location-triggered shift) |
| L2 | T2 | 0–1 | (slot reserved for Phase 3+) |
| L2 | T3 | 0 | — |
| L3 | — | **0** | Service register doesn't fit walk-ins |
| Capstones | — | 1–2 | `canvas_marge_interview` (hire) — Type A; mid-arc escalation TBD Phase 3+ |

**Total Marge canvases: ~6–8.** Within the 6–10 range.

**Locked-visible escalation ladder** (Doc 54 §4.5): Marge's hub ships with locked-visible Phase 3+ rungs from day 1, even though those rungs are not yet authored. The locked rungs ARE the slice — they telegraph the workplace-seduction matriarch-dom trajectory without requiring Phase 3+ content to ship.

### §6.3 — Sidebar visibility (Doc 68 §8)

Service default: **location + relation only.** Workplace bond is the operative axis. Arousal/corruption don't apply to service register.

### §6.4 — Voice register

Lane 1/2: RTS-flat WITH service-NPC specifics — short dialogue (Marge's "hon" / Marge's brevity). NOT Tier-3 prose for shift descriptions. Doc 54 §5.1 case study: literary prose in `node_shifts` + `node_talk` is preserved canon but represents a register-split violation; future maintenance pass should rewrite to RTS-flat.

Capstone (canvas_marge_interview) earns Tier-3 specifics ("the up-and-down a woman who had hired forty waitresses did. The shoes. The hands.") — 1,900 chars total.

Per-arc vocab ceiling for Marge: TBD Phase 3+ (Doc 30 §7.5 row left blank = out of scope for slice).

### §6.5 — Doc 53 design brief (Marge)

`28th_april_TLS_Phase2_Redesign/53_Marge_Redesign_Brief.md` (supersedes Doc 51 — Doc 51 is the historical record of the failed initial design). §1 codifies service-NPC arc adaptation of Doc 24's 3-lane doctrine (Lane 2+3 empty in slice for non-escalation NPCs). 4 deliverables only: schedule + 1 hub item + T1 shift + 2 trust effect + 2 quest cards (M1/M2, no terminal). Voice spec §2 locks RTS-flat per feedback memory.

---

## §7 — Antagonist/witness (Diana)

### §7.1 — Mechanical rhythm

Silent awareness accumulator. Diana's `awareness` trait climbs 0–100 across Maya's actions (visible-from-window beats, scandal-adjacent choices); confrontation capstone fires at threshold cross.

**No arc_stages.** Diana doesn't have discrete stage milestones in slice — she has a single threshold-driven confrontation. Her sub-state lives as bands on the awareness trait (cold / suspicious / knowing / shut-out).

**Lane 3 = 0 own + appears as INTERRUPTOR in others' Lane 3 endings.** The "Diana's floorboard" pattern in Frank's late-night kitchen ambient — Diana's footstep stops the cascade. This is what Diana does mechanically across the slice.

### §7.2 — Canvas distribution (Diana slice — Doc 60 brief, partial)

| Lane | Tier | Canvas count | Examples |
|---|---|---|---|
| L1 | T1 | 0–1 (shared-space neutral) | `diana_kitchen_passing` (very low density) |
| L1 | T2/T3 | 0 | No escalation register |
| L2 | T1–T2 | 1–2 (presence beats) | `ambient_kitchen_diana_call`, `ambient_diana_phone_kitchen` |
| L2 | T3 | 0–1 (confrontation precursors) | (sketchy slot — feeds capstone) |
| L3 | — | **0 own** | Appears as interruptor in Frank's L3 endings |
| Capstones | — | 1–2 | `scene_diana_confrontation` (Type B Pattern F — kicked_out + brought_in branches in slice; blackmail + matriarch deferred Phase 2+) |

**Total Diana canvases: ~4–6 standalone** + cross-appearances in Frank's lanes. Within the 6–10 range when cross-appearances counted.

### §7.3 — `awareness` trait (Tier 3 per-game; OFF-LIMITS at global scandal level per `00_LEGACY_IGNORE.md` §3.4 + Doc 65)

```toml
[npcs.core_traits]
awareness = 0   # silent accumulator 0–100
relation = 5    # mother-Maya baseline
```

Modifiers (per Doc 60 brief): visible-from-window beats +N; outdoor sexual beats +N; scandal-adjacent choices +N. No daily decay (one-way climb).

Bands (internal-only — NOT surfaced to sidebar):
- cold (0–24) — baseline
- suspicious (25–49) — confrontation precursors eligible
- knowing (50–74) — confrontation primed
- shut-out (75–100) — confrontation imminent

### §7.4 — Sidebar visibility (Doc 68 §8)

Antagonist default: **location only.** Awareness/scandal accumulator stays HIDDEN — dramatic surprise depends on player NOT seeing how close confrontation is. Doc 30 §6 + Doc 60 lock this.

### §7.5 — Voice register

Lane 1/2: RTS-flat with Diana's specific voice (clipped, observational, motherly with edge).
Capstone (confrontation): Tier-3 earned. Pattern F branching with high-stakes branch consequences (the resolution branches reshape multiple arcs — kicked_out / brought_in are mutually exclusive end-states).

Per-arc vocab ceiling: FULL CUCKOLD FRAMING (Doc 30 §7.5) — Diana watches / listens / participates; explicit cuckold dialogue ("watch your husband fuck me," "your wife is my second wife"); cuckold IS the resolution kink for the brought_in branch.

### §7.6 — Doc 60 design brief (Diana) — 🔴 BLOCKED

`28th_april_TLS_Phase2_Redesign/60_Diana_Design_Brief.md`. Antagonist/witness; NO arc_stages — silent awareness accumulator 0-100 (bands cold/suspicious/knowing/shut-out). Confrontation Type B Pattern F (2/4 branches scripted: kicked_out + brought_in; blackmail + matriarch deferred Phase 2+). 4 Q3 sub-questions surfaced for LO (Q3a canonical good path? Q3b cuckold sex in slice? Q3c blackmail+matriarch phase scope? Q3d post-confrontation hub?).

---

## §8 — Picking the shape (decision rule)

When the design book proposes a new NPC, run this 4-question check. Stop at the first match.

1. **Does the NPC share a household with Maya AND have a daily-proximity register the player will want to escalate?**
   → **Family/ambient** (Frank). Budget 25–35 canvases.

2. **Does the NPC share a household with Maya BUT the register is sparse + revelation-keyed, not saturated?**
   → **Slow-burn family** (Jake). Budget 10–15 canvases.

3. **Does the NPC live in a separate household, schedule-driven, relation-progression?**
   → **Peer/dating** (Ryan). Budget 8–12 canvases.

4. **Does the NPC have a workplace register Maya enters as employee/customer/colleague?**
   → **Service** (Marge). Budget 6–10 canvases.

5. **Does the NPC function as the threat/cost-of-other-arcs, with a confrontation as their primary scripted beat?**
   → **Antagonist/witness** (Diana). Budget 6–10 standalone + cross-appearances.

If none of the above match, the proposed NPC is outside the current 5-shape taxonomy. Surface to LO; don't author against an undefined shape.

---

## §9 — Shape adaptation: empty cells are honest

The Marge case study (Doc 54) cost ~8 hours partly because doctrine designed for escalation NPCs (Frank's distribution) was forced onto a service NPC. The corrected doctrine (Doc 53) declared empty Lane 2/3 cells.

**Same principle generalizes:** each shape has its own canvas distribution. Forcing Frank's distribution across every NPC produces Frank-clones with wrong-feel arcs. Skeletal under-distribution loses Principle 4 (mix arc shapes).

**Empty cells in the distribution table are honest, not gaps.** Service NPC at Lane 2 T2 = 0. Don't author 3 Lane 2 T2 scenes "to fill out the world" — that's the Doc 54 §3.4 failure mode. The empty cell is the design decision.

The R7 brief (Doc 56 R7 + `doctrine/04_authoring_rules.md`) commits to specific cell values for the NPC. Overages flag as drift. Under-shoots are acceptable when documented.

---

## §10 — Adapting to scope mode (slice vs full_game)

### §10.1 — At `scope_mode: slice`

**Slice scope ≠ full arc.** A slice ships the minimal viable canvases that telegraph the arc shape; the full arc is the eventual delivery. The locked-visible escalation ladder bridges the two — locked rungs visible from day 1 promise the arc's future without requiring future content to ship.

| Slice element | What ships | What stays locked-visible |
|---|---|---|
| L1 hub menu | Stage 0 unlocked items | Full ladder visible (Tease/Flash/Suck/Sex with their gates) |
| L1 menu items | Currently-tier-unlocked items | Locked rungs greyed + threshold-published |
| L2 ambients | Stage 0 + Stage 1 ambients | (later-stage ambients author when stage transitions) |
| L3 substitutions | Per slice scope | (later-stage subs author when stage transitions) |
| Capstones | Capstones up to slice scope's end-state | (next-chain capstones author when triggered) |

Phase 2+ content is NOT shipped in slice — but the slice's locked-visible rungs telegraph it (Doc 54 §3.6). The doctrine bridges slice + full arc via the locked-visible pattern, not via "ship Phase 2+ stubs."

**Locked-visible across locations (optional, D72-R8).** The locked-visible pattern can also bridge *exposure* tiers, not just stages: an arc NPC's public/semi-private hubs may show the higher (private-only) rungs greyed, so the ladder reads consistently at every hub, unlocking only where exposure allows (`doctrine/04` §6.2–§6.3). This is taste, not a requirement — the default is to simply omit out-of-tier rungs (context-scaled ladder).

### §10.2 — At `scope_mode: full_game`

All budgeted canvases are authored. Stage 0→4 ships in full; capstone chains run end-to-end; per-shape Lane 3 budgets fill to their upper bound where the arc demands it.

**Locked-visible escalation ladder still applies** — it's a UI/pacing device, not slice-specific. Even at full scope, the L1 hub menu shows future-tier rungs from day 1 with threshold text; rungs unlock as stat/stage gates pass. RTS Brother's hub shows ALL rungs from day 1 (Talk + Tease at Stage 0, Sex/Sleep visible-locked at higher corruption); rungs unlock organically. The difference vs slice is content existence behind each rung, not the UI shape.

| Full-game element | What ships | UI/pacing affordance |
|---|---|---|
| L1 hub menu | Full ladder authored | Locked-visible rungs still gate by stat/stage from day 1 |
| L2 ambients | All Stage 0→4 ambients per shape budget | Per-stage filtering via canvas conditions |
| L3 substitutions | Per-shape full budget (family 4–7, slow-burn 1–3, peer 0, service 0, antagonist 0 own) | Per-stage gating per substitution rule |
| Capstones | Full chains per Doc 57 (Type A/B/C) | Chain steps gate by predecessor flags |
| Phase 2+ inclusions | Pregnancy / scandal / gallery / tracker per LO decisions surfaced at Stage 1 §0 Q&A | Per Doc 65 — engine entry points + ripple |

**Anti-pattern:** pre-unlocking the entire L1 ladder at full_game because "everything ships." Locked-visible exists at any scope to telegraph progression — don't strip it. See `doctrine/07_anti_patterns.md` §8.X (full-game scope anti-patterns).

---

## §11 — Anti-patterns

### §11.1 — Frank-cloning a non-family-ambient NPC

Copying Frank's 28-canvas distribution onto Ryan's peer/dating shape produces 13 Lane 2 ambients + 7 Lane 3 substitutions where neither belongs. The shape mismatch produces the wrong "feel" — Ryan's quest-chain shape is meant to be sparse + relation-driven; saturating his lanes with ambients dilutes the few moments that should land.

### §11.2 — Filling empty cells in the distribution table

When the shape says 0 in a cell, the brief commits to 0. The Marge service shape has empty Lane 2 + Lane 3 in slice — that's correct, not a gap. Adding 6 Lane 2 ambients + 3 Lane 3 substitutions to "fill out the world" violates the shape (Doc 54 §3.4 case study — 9 surfaces authored that doctrine memory says shouldn't exist).

### §11.3 — Mixing escalation registers within a slice

A slice that has 4 family/ambient NPCs all at Frank-depth produces register sameness — every arc reads the same. The cast functions because shapes contrast (Principle 4 mix arc shapes). Slice scope should include 1 family/ambient + 1 slow-burn family + 1 peer/dating + 1 service + 1 antagonist (or similar combinatorial spread), not 5 family/ambient NPCs.

### §11.4 — Authoring against a shape that doesn't have a doctrine brief

If the design book proposes an NPC whose shape isn't in the 5-shape table (e.g., "AI assistant NPC" or "ghost NPC"), surface to LO before authoring. Don't improvise a 6th shape — the doctrine for budget + Lane 3 budget + sidebar visibility + voice register doesn't exist yet for that shape.

### §11.5 — R7 brief skipping

Doc 56 R7: no canvas for a new NPC ships before the NPC has a written design brief declaring arc shape + per-lane canvas budget + vocab ceiling + tier flags. Marge cost 8 hours to skip this step (Doc 54 §2.4).

### §11.6 — Shape declared but distribution drifts

A brief commits to peer/dating shape (Lane 3 = 0) but authoring produces 4 Lane 3 substitutions. Either the brief is wrong OR the additions don't belong. Overages flag as drift; surface to LO + audit.

---

## §12 — Cross-references

### Sibling doctrine files

- `doctrine/01_rts_principles.md` — P4 (mix arc shapes); P9 (per-arc vocab ceiling)
- `doctrine/02_three_lanes_plus_capstone.md` — lane mechanism distribution sits inside
- `doctrine/04_authoring_rules.md` — R3 (per-arc-shape Lane 3 budget); R7 (design brief precedes authoring); F1–F5 (capstone Pattern F)
- `doctrine/06_design_brief_template.md` — R7 brief structure
- `doctrine/08_kink_vocab_ceilings.md` — per-arc vocab ceiling table
- `doctrine/09_trait_catalog.md` §8 — sidebar visibility per arc shape

### Source briefs

- `28th_april_TLS_Phase2_Redesign/31_Frank_Arc_Design_Brief.md` — family/ambient gold standard
- `28th_april_TLS_Phase2_Redesign/53_Marge_Redesign_Brief.md` — service shape gold standard
- `28th_april_TLS_Phase2_Redesign/58_Ryan_Design_Brief.md` — peer/dating brief
- `28th_april_TLS_Phase2_Redesign/59_Jake_Design_Brief.md` — slow-burn family brief
- `28th_april_TLS_Phase2_Redesign/60_Diana_Design_Brief.md` — antagonist brief (🔴 BLOCKED on Open Q #3)
- `28th_april_TLS_Phase2_Redesign/61_Cookie_Phase3_Scope_Out.md` — formal Phase 3+ deferral record (Doc 57 R7 compliance)

### Source doctrine

- `28th_april_TLS_Phase2_Redesign/56_RTS_Principles_and_TLS_Alignment_Doctrine.md` §5 — distribution table source
- `28th_april_TLS_Phase2_Redesign/54_Marge_Redesign_Session_Lessons.md` — failure-mode case study

---

**End of file.** Next: `doctrine/04_authoring_rules.md` for the rule layer (R1–R7 + R1–R6 + R1–R5 + F1–F5).

═══════════════════════════════════════════════════════════════════════════════

## 8. 04_authoring_rules

**Source:** `prompts_v2/doctrine/04_authoring_rules.md`

---

# Doctrine 04 — Authoring Rules

**Sources:** Doc 56 R1–R7 (general authoring); Doc 50 R1–R6 (quest card shape); Doc 57 R1–R5 + F1–F5 (capstone + Pattern F); Doc 67 R1–R7 (solo activity + multi-NPC dispatcher).
**Authority:** Doctrine. These are the rules every canvas, every quest card, every capstone, and every Lane 3 dispatcher must respect before shipping.
**Purpose:** Convert the principles (`doctrine/01_rts_principles.md`) and mechanisms (`doctrine/02_three_lanes_plus_capstone.md`) into mechanical pre-ship checks. Each rule: text + why + how-to-apply + worked example.

**Cite shorthand:**
- **D56-R1 … D56-R7** = Doc 56 (general authoring)
- **D50-R1 … D50-R6** = Doc 50 (quest card shape)
- **D57-R1 … D57-R5** = Doc 57 (capstone fingerprint + budgets)
- **F1 … F5** = Doc 57 Pattern F sub-rules (Type B capstones)
- **D67-R1 … D67-R7** = Doc 67 (solo activity + multi-NPC dispatcher)
- **D72-R6 … D72-R8** = Doc 72 (presence floor: per-schedule-row hubs + exposure-tier ladder ceiling)

---

## §1 — Doc 56 R1–R7 (general authoring rules)

### §1.1 — D56-R1: Lane 1 hub openings stay constant within a canvas

**Rule:** Don't author T0/T1/T2 group blocks for the hub's opening lines. The opening shows the player "you've entered this menu" — that doesn't need to vary with stage; the menu items vary with stage via `show_when_locked` + per-choice `conditions`.

Per-time-of-day variation = separate canvas. `frank_kitchen_morning_hub` (05:30–09:00) and `frank_kitchen_dinner_hub` (17:00–19:30) are separate canvases with their own schedules. Don't fold them.

**Exception:** world-state presence/absence prose (NPC is at school vs. at home) is OK — one canvas with two group blocks gated on `getNpcLocation`. That's world state, not progression state.

**Why this rule exists:** RTS Lane 1 hub openings only vary by world state (time of day, NPC presence). They don't vary by Maya's progression — the menu items already encode progression. T0/T1/T2 opening prose is authoring overhead RTS doesn't pay.

**How to apply:**
- For each new NPC hub canvas: write ONE opener paragraph. If the hub legitimately needs presence/absence framing, two group blocks (present / absent).
- For existing canvases violating R1: collapse the tier blocks to one paragraph at the next maintenance pass. Not a blocking refactor — but new canvases ship clean.

**Worked example:** the body of `frank_kitchen_morning_hub` opens with ONE paragraph + dialog beat:

```toml
[[canvases.nodes]]
id = "base"
blocks = [
  { type = "image", props = { file = "scenes/frank_kitchen_morning_hub.jpg" } },
  { type = "paragraph", content = "Frank's at the counter. He looks up when you come in." },
  { type = "dialog", npcId = "npc_frank", content = "Morning." },
]
```

The progression-aware behavior lives in the menu rungs (Tease/Flash/Suck/Sex with their own `show_when_locked` + `conditions`). The opening doesn't need to repeat the progression in prose.

### §1.2 — D56-R2: Every T0/T1 ending lands on an in-fiction interruption

**Rule:** For canvases using `[group]` blocks to tier-route content (Lane 2 ambients, Lane 3 substitution targets, Lane 1 internally-tiered targets like teases), the lower-tier endings MUST hint that more would have happened. The interruption can be:

- **External:** a sound, a noise, an NPC approaching (Diana's floorboard, kettle whistling, Jake's door opening)
- **Internal:** Maya self-stopping ("she tells herself this didn't mean anything," "she sets the mug down before her hands shake")
- **NPC-stopping:** the NPC pulling back ("he lets go like nothing," "he turns back to the paper")

The higher tier then EXPLICITLY blows through the interruption — that's the payoff.

**Why this rule exists:** RTS gets the "more is here" cue from mid-cascade cutoff — the player tries, hits "Ew! Get out!", knows they bounced. TLS's group-block tier-routing produces a complete-feeling scene at every tier; without an in-fiction interruption, the T0 ending reads as "this is the whole thing" and the come-back-later loop weakens. P3 cue (one scene, multiple lengths) requires this rule for TLS.

**How to apply:**
- At T0 / T1 endings: author a final beat that signals incompleteness. Don't end T0 on a clean "scene complete" moment.
- At the next tier up: explicitly push through what got interrupted. T1 dispatches the threat; T2 makes it irrelevant.
- Audit existing tier-routed canvases: walk each `[group]` block ending; verify the lower tiers hint at more.

**Worked example (gold standard):** `ambient_kitchen_frank_late_night_raid` T0 ending:

```toml
{ advance_text = "Hear the floorboard upstairs.", blocks = [
  { type = "paragraph", content = "Diana's floorboard, her bedroom door. He lifts you down, hands you your glass, turns the tap on like he was doing dishes." },
  { type = "dialog", npcId = "npc_frank", content = "Night, girl." },
]},
```

Diana's footstep stops the cascade — external interruption. T1 of the same canvas then blows through: "he fucks you fast on the counter, hand over your mouth, and cums inside you before the house stirs." The T1 reveal IS that Diana's threat doesn't stop them anymore.

### §1.3 — D56-R3: Lane 3 coverage by arc shape with declared per-NPC budgets

**Rule:** Lane 3 substitution count is determined by the NPC's arc shape, not by quotient parity. Author Lane 3 substitutions for an NPC based on whether their register supports "walks in on you during your chores."

| Arc shape | Lane 3 budget | Rationale |
|---|---|---|
| **Family/ambient** | 4–7 | Shape requires saturating chores with NPC presence. Frank, RTS Brother (7 of 15). |
| **Slow-burn family** | 1–3 | Sparse, keyed to specific arc moments — the walk-in IS the beat. Jake. |
| **Peer/dating** | 0 | Peer doesn't interrupt private chores. Arc lives in Lane 1 visits + capstone dates. Ryan, RTS Marcus. |
| **Service** | 0 | Workplace-only register; private space is not their setting. Marge. |
| **Antagonist/witness** | 0 own + appears as interruptor in others' L3 | Diana doesn't have her own walk-ins; she's the THREAT in other NPCs' Lane 3 endings. |

**Why this rule exists:** the Marge case study (Doc 54) wasted 8 hours partly because doctrine was authored against escalation NPCs and didn't map to service NPCs. Forcing Frank's distribution across every NPC produces Frank-clones with wrong-feel arcs.

**How to apply:**
- In the NPC design brief (R7), declare Lane 3 budget upfront. Choose from the shape table.
- Overages flag as drift. If a service NPC is gaining Lane 3 substitutions, either the brief is wrong OR the additions don't belong.
- Antagonist Lane 3 = always 0 own. If Diana ever needs a "walks in on Maya" moment, it shouldn't be a Diana substitution — it should appear as the interruption beat in a Frank substitution.

### §1.4 — D56-R4: Sidebar must surface NPC state for in-scope NPCs

**Rule:** The sidebar is the world model. For every in-scope NPC, the player must see (at minimum) their current location, continuously, without opening a menu. Where the register supports it, key stats (arousal, corruption, love/trust, or analog) should also be surfaced.

**Why this rule exists:** P10 — without per-NPC location radar, Lane 3 becomes undiscoverable. The whole "you're doing X and he happened" texture depends on the player having the situational awareness to choose X knowing it might collide with him. `getNpcLocation` (`v2.py:2923`) primitive already exists; the sidebar authoring just calls it.

**How to apply:**
- Add per-NPC `sidebar_items` to the slice. Each item calls `getNpcLocation(npcId)` (sidebar primitive type pending Doc 64 PRD).
- Where the arc's register includes NPC stats the player needs to plan against (Frank's arousal, etc.), add per-NPC stat readouts alongside the location.
- Per-arc-shape defaults are in `doctrine/09_trait_catalog.md` §8:
  - Family/ambient: location + arousal + corruption + relation
  - Slow-burn family: location + arousal + relation
  - Peer/dating: location + relation
  - Service: location + relation
  - Antagonist: location ONLY (awareness hidden)
- Stage NEVER surfaces (Doc 68 §9).

### §1.5 — D56-R5: Every canvas declares a `guide` string

**Rule:** Every canvas authored from this point ships with a `guide` field — a one-sentence, player-facing trigger recipe in plain English. The convention names the lane in the prose:

| Lane | Phrasing convention | Example |
|---|---|---|
| Lane 1 | "Visit X" / "Go to Y and Z" | "Visit Frank in his kitchen during breakfast" |
| Lane 2 | "Walk into X" / "Pass through Y" | "Walk into the kitchen late at night" |
| Lane 3 | The chore name, then "while X" | "Make tea in the kitchen while Frank is home" |
| Capstone | The narrative milestone | "After the catch, return to Frank's bedroom in the evening" |

**Why this rule exists:** it's the data primitive for the future published catalog (P2 alignment). Without it, a future catalog surface has nothing to render. Authoring the field NOW means every new canvas accumulates the data; backfilling later means a multi-hour scan and audit.

**Status:** doctrine-locked + schema-pending. Doc 62 PRD ships the field parser. Authors should still emit `guide = "..."` next to `name` and `description`; the parser tolerates the field even before it becomes a parsed attribute.

**How to apply:**
- New canvas: include `guide = "..."` next to `name` and `description` in the canvas declaration.
- Existing canvas backfill: handle in next maintenance pass per arc.
- Style: player-facing, second-person or Maya-third, short. Not a marketing line; a recipe.

```toml
[[canvases]]
id = "scene_frank_walks_in_shower"
name = "Frank walks in mid-shower"
description = "Lane 3 substitution target on activity_shower."
guide = "Shower in the bathroom in the morning while Frank is home"
```

### §1.6 — D56-R6: Quest cards must be capstone / mechanic / hybrid; `txt_only` is doctrine drift

**Rule:** Per D50-R3 (already locked). `txt_only` quest cards — those with no `ready_canvas`, no `goals` block, just text — violate the card-mode taxonomy. They exist as TODOs in shipped TOML and corrode the doctrine because they normalize incompleteness.

**Why this rule exists:** Doc 50 already states it. Restated here because the live slice (2026-05-25) shipped 5 `txt_only` cards (Ryan ×2 + Jake ×3). The validator named in Doc 50 §6 hasn't been built yet. Until it is, the rule is human-read.

**How to apply:**
- For each existing `txt_only` card: either complete it (add `ready_canvas` for capstone mode, add `goals` for mechanic mode) or delete it.
- For new cards: no card ships in `txt_only` shape.
- Future: the Doc 50 §6 validator (Doc 63 PRD) catches these mechanically.

### §1.7 — D56-R7: NPC design brief precedes authoring

**Rule:** No canvas for a new NPC ships before the NPC has a written design brief declaring:
1. **Arc shape** — pick from the 5-shape table.
2. **Per-lane canvas budget** — Lane 1 / Lane 2 / Lane 3 / capstone counts per tier (see `doctrine/03_arc_shapes.md`).
3. **Vocabulary ceiling** — per Doc 30 §7.5. What does this NPC's content escalate to? What stays off-limits?
4. **Tier flags** — what state changes mark T0 → T1 → T2 transitions for this NPC. Named, not implied.

**Why this rule exists:** Marge wasted 8 hours because authoring started against doctrine designed for escalation NPCs (Doc 54). The brief is the gating step that surfaces shape-mismatches BEFORE prose is committed.

**How to apply:**
- Before any new NPC's first canvas: write the brief.
- Use Doc 31 (Frank) or Doc 53 (Marge) as the gold-standard reference.
- The brief lives in `28th_april_TLS_Phase2_Redesign/` as a numbered doc.
- An authoring pass that violates the brief's budget or ceiling is drift; the brief is the canonical reference.

**Brief template:** see `doctrine/06_design_brief_template.md`.

---

## §2 — Doc 50 R1–R6 (quest card shape)

These rules apply to every `[[quest_cards]]` entry. The validator at `_validate_quests_cards` (`template_import.py:4469`) wires R1–R4 mechanically; R5 + R6 are human-read.

### §2.1 — D50-R1: Capstone coverage

**Rule:** Every canvas with `priority ≥ 9` + `is_repeatable = false` + a flag-setting effect MUST be referenced by some quest_card's `ready_canvas` field — OR be explicitly marked off-panel with a single-line comment on the canvas:

```toml
# off-panel: reached via setter-menu only; not a quest-pointed milestone
```

**Why this rule exists:** Sleepover (before 2026-05-24) was off-panel by accident, not by decision — `scene_frank_sleepover` shipped to production and was reachable only via the bedroom setter menu, with no quest-panel pointer. Same for Diana confrontation. No silent off-panel capstones.

**How to apply:**
- For each capstone, find or author its pointing quest card. The card's `ready_canvas` field names the capstone slug.
- If a capstone is intentionally off-panel, add the comment line above the canvas's `[[canvases]]` header.

### §2.2 — D50-R2: Climbing-bullet rule

**Rule:** If a card has a `ready_canvas`, AND the `ready_canvas`'s trigger conditions include a trait gate strictly above what the card's `when` clause enforces, the card MUST have a `goals` block surfacing that trait climb.

**Why this rule exists:** F3 (before 2026-05-24) shipped without one — player completed first-night, saw F3 say *"He took me upstairs. He hasn't said the word yet,"* and had no visibility into the corruption 25 → 35 climb gating declaration.

**How to apply:**
- Read your card's `ready_canvas`. Read that canvas's `conditions.items`. For every trait condition, ask *"is this value strictly above what my card's `when` already guarantees?"*
- If yes, the player needs a `goals` bullet to know about it.

```toml
[[quest_cards]]
npc_id = "npc_frank"
priority = 3
text = "He took me upstairs. He hasn't said the word yet."
ready_canvas = "scene_frank_declaration"   # this canvas needs corruption ≥ 35
when = [
  { flag = "frank_bedroom_first_done", op = "is_true" },     # guarantees corruption ≥ 25 from F2
  { flag = "frank_cracked", op = "is_false" },
]
goals = [
  { trait = "corruption", subject = "player", op = "gte", value = 35, label = "Maya's corruption" },
]
```

### §2.3 — D50-R3: Terminal placement

**Rule:** A card with `terminal = true` MUST be the LAST card in its NPC chain. No flag in its `when` may permit unmet subsequent cards.

**Why this rule exists:** Old F4 (before 2026-05-24) was terminal at `frank_cracked` (the declaration capstone) while sleepover + Diana capstones still existed downstream with their own setter flags. The arc closed on the panel two scenes too early.

**How to apply:**
- List every card for the NPC. Find the one with `terminal = true`.
- Confirm no other card has a `when` requiring a flag set AFTER the terminal's flag fires.
- Terminal is the END of the FULL arc, not the slice's authoring boundary. If Phase 2+ has more rungs, no terminal in slice.

### §2.4 — D50-R4: Chain continuity

**Rule:** Every "post-X" card (one whose `when` requires `flag_X = is_true`) MUST have a sibling "pre-X" card whose `ready_canvas` points at the canvas that sets X.

**Why this rule exists:** Prevents floating cards that activate from states the player has no narrative path into.

**How to apply:**
- For each card, identify the flag it requires to be true.
- Confirm another card in the chain points at the canvas that sets that flag (via that card's `ready_canvas`).

### §2.5 — D50-R5: Mechanic-tier explicit unlock

**Rule:** A pure-mechanic card (no `ready_canvas`) MUST carry a one-line author comment naming what content opens when the threshold lands. Format:

```toml
# unlocks: <slug>_hub menu item "X" at npc_<slug>.trust >= 10
```

Or for substitution-rule unlocks:

```toml
# unlocks: substitution beat <slug> when worn_corruption >= 25
```

**Why this rule exists:** validators can't see "what's behind the threshold." A mechanic card without this comment can ship pointing at vapor — the threshold crosses and nothing actually changes for the player. The comment makes the unlock greppable and reviewable.

### §2.6 — D50-R6: Goals labels NAME THE TRAIT (REVERSED 2026-05-30 — LO preference)

**Rule (current, LO preference 2026-05-30):** `goals[i].label` names the underlying TRAIT plainly so the player can map a quest goal to a visible stat — `"Corruption"` for the corruption trait, `"<NPC> Relation"` (e.g. `"Cole Relation"`, `"Rosa Relation"`) for a per-NPC relation goal. Use the SAME word on the sidebar (the corruption `trait_words` item labeled `"Corruption"`, not `"Status"`). Never raw key paths like `npc_diana.awareness` or `core_traits.corruption`.

**This REVERSES the original D50-R6** (Maya-voice euphemisms — *"Maya's loosening," "Cole's attention," "Rosa trust"*). LO found the euphemisms confusing: a player can't connect "Maya's loosening" to any stat they see. Trait-name labels are the default for this lineage; use a Maya-voice label only if LO asks for it on a specific game. (Reversal applies ONLY to `goals[i].label` — the `tip`/`text`/`ready_text` card fields stay Maya-voice interior register per §4 of `doctrine/05`.)

**Why labels matter at all:** the label renders directly under the 🎯 frame in the player UI. It's a player-facing surface, not a debug surface — so it must read as the stat the player is tracking.

### §2.7 — Pure-mechanic chain bounded `when` ranges (Doc 54 §4.3 extension)

**Rule:** pure-mechanic chains need each card's `when` to have BOTH lower and upper bounds matching the threshold range. When the threshold crosses, the current card's `when` fails, the next card's `when` matches, picker swaps atomically.

**Worked example (Marge M3/M4/M5 final shape):**

```toml
[[quest_cards]]
# unlocks: marge_hub menu item "Long shift" at marge.trust >= 25
npc_id = "npc_marge"
text = "I've been getting my hours."
when = [
  { trait = "relation", subject = "npc", npc_id = "npc_marge", op = "lt", value = 5 },
]
goals = [{ trait = "relation", subject = "npc", npc_id = "npc_marge", op = "gte", value = 5, label = "Marge trust" }]

[[quest_cards]]
# unlocks: marge_hub menu item "Talk shop" at marge.trust >= 15
npc_id = "npc_marge"
text = "She lets me sit at the counter now."
when = [
  { trait = "relation", subject = "npc", npc_id = "npc_marge", op = "gte", value = 5 },
  { trait = "relation", subject = "npc", npc_id = "npc_marge", op = "lt", value = 15 },
]
goals = [{ trait = "relation", subject = "npc", npc_id = "npc_marge", op = "gte", value = 15, label = "Marge trust" }]

# ... and so on
```

Every threshold in the chain has exactly one active card.

---

## §3 — Doc 57 R1–R5 (capstone fingerprint + budgets)

### §3.1 — D57-R1: Capstone trigger fingerprint

**Rule:** A capstone MUST have all of these:

- **EITHER** `is_repeatable = false` **OR** `is_repeatable = true` AND `conditions` contain a `flag_is_false` gate on the setter flag itself. Both produce one-shot behavior; the `true + self-gate` variant supports Refuse-path retry (F4).
- `trigger_mode = "manual"` (default — no need to declare explicitly)
- `priority ≥ 9` (high enough to win against Lane 2 randoms; 9 is minimum, 10–12 for chain-final beats)
- `conditions` block including the flag-is_false gate that prevents re-fire
- A flag effect on at least one exit choice that sets the corresponding setter flag

**Why this rule exists:** without the trigger fingerprint, a canvas either fires repeatedly (`is_repeatable = true` + no self-gate) or never retires (no flag-setter on exit).

**Validation:** flag any `is_repeatable = false + priority ≥ 9` canvas that doesn't have a setter-flag effect, and any `is_repeatable = true + priority ≥ 9` canvas whose conditions don't include a self-gate flag.

### §3.2 — D57-R2: Type-A simplicity preference

**Rule:** Default to Type A. Use Type B only when the player's decision MATTERS in a downstream-divergent way.

**Concrete rule:** if both branches of a proposed Type B fork would set the same flag and lead to similar downstream content, it's not a real fork — collapse to Type A. Type B is reserved for moments where:
- The two paths set DIFFERENT flags (the refuse path doesn't set the chain-completion flag), OR
- The two paths route into different NPC arcs (cross-NPC transfer), OR
- The two paths have materially different downstream content (one continues the cascade, the other ends short)

**Why this rule exists:** Type B is the most expensive capstone to author and the most cognitively expensive for the player. TLS currently has Type B at ~50%+ of capstones — high relative to RTS's ~25%. Not a violation, but a forcing function: each Type B should justify its cost.

### §3.3 — D57-R3: Capstone references in quest cards (D50-R1 restated)

**Rule:** Every capstone (priority ≥ 9, is_repeatable = false, flag-setting) MUST be referenced by some quest_card's `ready_canvas` field — OR be explicitly marked off-panel with the `# off-panel:` comment.

(Same as D50-R1. Restated for capstone authors.)

### §3.4 — D57-R4: Type C chain continuity (D50-R4 restated)

**Rule:** Every "post-X" capstone in a Type C chain (one whose `conditions` requires `flag_X = is_true`) MUST have a sibling "pre-X" capstone whose exit-flag-effect sets X.

(Same as D50-R4. Restated for chain capstones.)

### §3.5 — D57-R5: Capstone schedule and location coherence

**Rule:** If a capstone has a `schedule` (time window), the schedule must match the fiction of the scene. *"Frank declares himself in the living room"* should fire in the living room schedule for evenings, not at 3 AM in the kitchen. If a capstone's location/schedule choice was made for engine convenience rather than fictional coherence, the fiction is bent and the player will notice.

The schedule + location combination ALSO determines who's likely in the room when the capstone fires. If Diana's awareness is meant to be the cost of the scene, the capstone should fire at a time when she's nearby — and the conditions can include her presence/absence flag explicitly.

---

## §4 — Pattern F (F1–F5): Type B capstone sub-rules

When a capstone IS Type B, the fork must be authored to these standards.

### §4.1 — F1: Both branches must be playable in good faith

**Rule:** Neither branch can read as "the wrong choice." The Accept and Refuse must both feel like real options Maya could plausibly pick. If one branch is *clearly* what the player should do, it's not a real fork — it's a tutorial gate dressed up.

**Worked examples:**
- RTS `SellingMyStepsister`: Accept = $500 + cross-NPC arc opens; Refuse = two lines + return. The Refuse is short but doesn't punish — it's an honest "no." Both are playable.
- TLS `scene_franks_bedroom_evening`: "Cross to him" = the climax cascade; "Hesitate. Step back" = a refuse-and-leave path that doesn't set the chain-completion flag.

### §4.2 — F2: The branches must diverge in DOWNSTREAM effect, not just text

**Rule:** If both branches converge to the same flag and the same next state, it's not a Type B — collapse to Type A with two flavors.

**Real divergence:**
- Different flag set (refuse doesn't set the chain-completion flag)
- Different NPC arc opens (cross-NPC transfer)
- Different downstream cascade content (continues vs. cuts short)
- Material trait effect difference (corruption +5 vs. +0; love +3 vs. love -2)

**Borderline Type B (shared primary flag with secondary-effect divergence):** acceptable when secondary effects are *real downstream content*, not cosmetic. Worked example: `canvas_first_sunday_morning` — both choices set `first_sunday_passed` + `first_rent_paid` but Church path additionally sets `attended_church_this_week` + grants `rep_church +3` + Diana awareness −2 (which feeds real downstream content). Both branches genuinely diverge in long-tail consequence.

Collapse to Type A only when secondary effects are also identical.

### §4.3 — F3: The fork beat should be the cascade's TERMINAL beat

**Rule:** The cascade plays through to the moment of decision. The decision is the LAST authored act before `exit_block.choices` fork. Don't have the player make the choice mid-cascade with N beats of authored content downstream of both branches — that's just two parallel scenes glued together.

The fork is the moment of decision; everything after is downstream of that decision.

### §4.4 — F4: Refuse paths can keep the canvas alive for retry

**Rule:** If the refuse path doesn't set the chain-completion flag, the capstone can re-fire next eligible time. This is legitimate.

If the refuse path DOES set the flag (or a sibling flag that closes the arc), the capstone is irreversible. Either side is valid; the choice should match the fiction.

- *"Sell my stepsister"* is irreversible — Refuse should close that scene's possibility.
- *"Cross to him in the bedroom"* is reversible — Refuse should let Maya try again.

### §4.5 — F5: Don't compound Pattern F with mid-branch tier-routing

**Rule:** `scene_franks_bedroom_evening` currently does this — the climax node has T0 (corruption < 40) vs T1 (corruption ≥ 40) closing register inside the Accept branch. Two structural devices stacked. This is the UPPER BOUND of complexity per capstone; don't push further (e.g., a three-way fork with tier-routing in two of the branches).

The player loses the structural read.

---

## §5 — Doc 67 R1–R7 (solo activity + multi-NPC dispatcher)

### §5.1 — D67-R1: Solo activity is a separate canvas, not a sub-block

**Rule:** Every Maya-solo activity (`activity_make_tea`, `activity_wash_dishes`, `activity_shower`, `activity_study`, `activity_nap`) is its own `[[canvases]]` entry. Each has:
- `trigger_mode = "manual"` (player clicks button to enter)
- `is_repeatable = true` (chore can repeat)
- `location = "loc_X"` (anchors to a hub canvas)
- `schedules = [...]` (time-of-day availability)

**Why:** the dispatcher mechanism requires a named, addressable canvas to attach substitution rules to. Inline activity bodies in a hub menu can't carry substitutions.

**How to apply:** before authoring substitutions for NPCs at a location, audit whether the parent activity exists as a canvas. If not, author it first.

### §5.2 — D67-R2: Stat costs land on activity exit_block by default; outside it when "unconditional"

**Rule:** Two placements for stat-effect macros:

1. **Inside `exit_block.effects`** — applies only when player returns from solo branch. Use for cost-per-completion activities (washing dishes, masturbating; the activity costs energy only if Maya finishes it).
2. **In `pre_substitution_effects` on canvas trigger (Pattern C)** — applies unconditionally on canvas entry, including substitution-preempted runs. Use for activities with unconditional outcomes (exercise = +Fit even if interrupted; sleep = energy restore even if NPC scene fires).

**Why:** RTS shows both placements. The design call is whether the activity "counts" when interrupted.

**How to apply:** for each new solo activity, ask: "If NPC walks in mid-activity, did Maya complete the chore?" If no → costs inside exit_block. If yes → costs in pre_substitution_effects.

### §5.3 — D67-R3: Menu-level gating for time-of-day + energy + purchase + quest state

**Rule:** All four gates live on the LOCATION canvas's button (the exit_block.choices `conditions`), not on the activity canvas itself. The dispatcher trusts the menu's gating.

| Gate | Location | Example |
|---|---|---|
| Time-of-day | Location button | `if $game.time == "LN" → notification` |
| Energy | Location button | `if $player.energy <= 0 → disabled button` |
| Purchase | Location button | `if isPurchased("phone") → button visible, else hidden` |
| Quest state | Location button | `if quest active && !done → button visible` |
| NPC stage / corruption | Dispatcher | inside substitution check conditions |
| NPC presence | Dispatcher | `requires_npc` |
| Per-day cap | Dispatcher | `max_triggers_per_day` |

**Why:** if the dispatcher double-gates, the button would render then route to a passage that bails — wastes a click and breaks the menu surface.

### §5.4 — D67-R4: Multi-NPC competition defaults to Pattern A

**Rule:** When 2+ NPCs could walk in on the same solo activity, default authoring is Pattern A:
- Each NPC gets its own `[[canvases.trigger.substitutions]]` rule
- Rules ordered by narrative priority (closer-arc NPC first, OR escalation-NPC first)
- Each rule has its own `chance` and `conditions`

**Why:** Pattern A maps directly to TLS engine support; sequential first-match is what `checkAndSubstituteCanvas` already does.

**How to apply:** if the slice's family-ambient NPC (Frank) shares a chore location with the slow-burn-family NPC (Jake), order Frank's substitution rule first.

### §5.5 — D67-R5: Pattern B only when scenes are inherently mutually exclusive

**Rule:** Use Pattern B when the design REQUIRES mutual exclusion — typically multiple variants of the same NPC at the same activity (e.g., Brother grope vs Brother help-study at the study desk; one fires).

Don't use Pattern B for "any NPC could walk in" — that's Pattern A.

**Why:** Pattern B reserves a single dice partition for mutex variants. Failed-condition in a claimed slot falls to solo, not to next rule — matching the load-bearing RTS semantic (Doc 67 §4.2).

**Engine status (2026-05-27, Doc 69 Item 1 shipped):** Pattern B is engine-supported via the `exclusive_group` field on each substitution rule. Rules sharing the same `exclusive_group` string share ONE dice roll, partitioned into cumulative `chance` buckets. Engine: `v2.py:4671-4713`. Mixed Pattern A + Pattern B in the same dispatcher is supported — groups always evaluate before independent rules.

**Emission template** (see `doctrine/02_three_lanes_plus_capstone.md` §4.6.2 for canonical example):

```toml
[[canvases.trigger.substitutions]]
target_canvas_id = "scene_brother_grope_at_desk"
chance           = 0.1667
exclusive_group  = "study_desk_brother"

[[canvases.trigger.substitutions]]
target_canvas_id = "scene_brother_help_study"
chance           = 0.1667
exclusive_group  = "study_desk_brother"
# Cumulative bucket = 0.33; remaining 0.67 = solo
```

**Don't approximate Pattern B via Pattern A** (multiple rules with `chance` summing < 1). The pre-2026-05-27 approximation is now wrong on two counts — cumulative probability diverges (1 − ∏(1 − cᵢ) ≈ 42% vs true 50% for 3×1/6) and failed-condition fall-through promotes to next rule instead of solo. Emit `exclusive_group` directly.

### §5.6 — D67-R6: `IsNpcAtHome` for Lane 3 walk-ins; `GetNpcLocation == "Loc"` for Lane 2 entry-encounters

**Rule:** Direction of the walk-in determines the predicate:
- NPC walks in on Maya (Lane 3) → `IsNpcAtHome` equivalent (NPC at any home location)
- Maya walks in on NPC (Lane 2) → `GetNpcLocation == "Loc"` equivalent (NPC at exact location)

**TLS implementation:** both achieved via `requires_npc` on the canvas trigger. The semantic difference lives in the NPC's schedule shape:
- Lane 3 walk-in: NPC's schedule has a meta-location or wide-scope entry resolving to "house"
- Lane 2 entry-encounter: NPC's schedule has an entry at the exact canvas location during the same time window

**Why:** RTS source shows the asymmetry consistently. Tightening Lane 3 to "NPC must already be in kitchen" breaks the fictional intent ("Frank wandered into the kitchen because Maya was there").

### §5.7 — D67-R7: Per-day cap on each substitution target via `max_triggers_per_day = 1`

**Rule:** Every Lane 3 substitution target canvas has `is_repeatable = true` (the scene CAN refire on subsequent days) AND `max_triggers_per_day = 1` (won't refire same day).

Optionally, the parent activity's `[[canvases.trigger]]` has its own `max_triggers_per_day` to cap the chore itself (Maya can wash dishes 3 times today, but Frank's kitchen-dishes scene fires at most once).

**Why:** RTS uses `executedToday` per-scene. Once-per-day is the felt cadence — the world has rhythm.

**How to apply:** every substitution target ships with `max_triggers_per_day = 1`. Don't omit unless the design specifically requires multi-fire-per-day (rare).

---

## §6 — Doc 72 R6–R8 (presence floor: per-schedule-row hubs + exposure-tier ceiling)

These three rules harden Doc 72's presence floor. Doc 72's R1–R5 (in the source doc) still hold; R2/R3 are unchanged — choices on a hub are logic-driven, "base + talk + leave" is a complete canvas, and there is **no choice-quota**. What R6–R8 change is the *floor mechanism*: the thing that acknowledges a scheduled NPC must be a **Lane 1 hub, per schedule row** — not a probabilistic Lane 2 ambient, and not a matter of judgment. The floor is now checkable; the choices on top are still judgment.

### §6.1 — D72-R6: Every schedule row has a live Lane 1 hub

**Rule:** For every `[[npcs.schedules]]` row an NPC has — each (location × time-window × weekdays) — there is a Lane 1 hub canvas for that NPC whose own `trigger.schedules` covers that window. The hub's `base` node renders **unconditionally** (image + a line of what the NPC is doing + optionally one line of dialogue); it is never gated behind escalation flags. A Lane 2 ambient does **not** satisfy the floor — it is a dice roll (`chance 0.25` ⇒ nothing on ~3 of 4 visits), so most visits would still be a dead room.

**Corollary — a schedule entry is a promise of a hub.** If an NPC has no physical hub anywhere (a pure rent/phone "system" NPC such as a landlord), they must carry **no** `[[npcs.schedules]]` row — otherwise the schedule page advertises a body the world can't deliver. Either give them a hub or drop the schedule.

**Corollary 2 — a schedule row at a *locked* location is a *deferred* promise.** If the row's location has `entry_conditions`, the player can't be present until the lock opens, so the hub is dormant until then. This is legitimate only under the **unlock contract**: the lock must read as "haven't met / been invited yet," the NPC must be meetable at an OPEN on-ramp location, and the beat at that on-ramp must set the unlock flag (which therefore needs a reachable setter). The bug to avoid is an NPC reachable *only* via a locked location, or a door gated on a flag only settable behind it. Full Case A/B/C treatment (private place / deeper room / unreachable-NPC) in `doctrine/10` §5.4.

**Multiple windows at one location = separate hub canvases** (this is **D56-R1**: period-split, "don't fold them"). A breakfast hub and an after-close hub at the same diner are two canvases with their own `schedules`.

**Why this rule exists:** the engine renders a hub portrait only when the hub's *own* `schedules` window is live AND the NPC is present (`isCanvasValid`, `v2.py:4356`, + the presence gate at `v2.py:4384`). Late Shifts authored hubs for narrow arc-moment windows (Hank's diner hub opened 22:00–01:30) while scheduling the NPC present far wider (Hank at the diner ~06:00–22:00). A per-row audit found 13 of 22 rows dead — the schedule page promised a body, the room delivered nothing. Lane 2 ambients existed but, being dice rolls, are not a floor.

**How to apply:** list the NPC's schedule rows. For each, confirm a Lane 1 hub at that location whose `trigger.schedules` *covers that exact window+weekdays*. "A hub exists at the location" is not enough — it must be open at that time. Where the NPC's presence spans several distinct windows at one place, author one hub per window (period-split). Never flag-gate the base node.

**Worked example (anti):** Hank is scheduled at the diner front 06:00–09:00, 09:00–17:00, 17:00–22:00, and 22:00–01:30; only `hank_diner_front_hub` (22:00–01:30) exists. Result: 06:00–22:00 every day shows Hank on the schedule page but renders no hub — dead. Fix: author `hank_diner_front_morning` / `_day` / `_evening` hubs, each with `trigger.schedules` matching its row.

### §6.2 — D72-R7: A hub's escalation ceiling is set by location exposure, not by time

**Rule:** Which escalation rungs a hub may offer is decided by the **exposure** (privacy) of that location at that window — *who could see this and what's at risk* — not by the time of day directly. Relationship state (corruption / relation / stage, global to the NPC) then unlocks within that ceiling. Two orthogonal filters: exposure sets the ceiling per hub; relationship state unlocks rungs inside it.

| Exposure tier | Locations | Rung ceiling |
|---|---|---|
| **Public** (high exposure) | diner floor with customers, street, park midday, mall | Deniable acts only — talk, banter, a charged look, a brush-past. No flashing, no sex. |
| **Semi-private** (low exposure) | back kitchen, office with a door, storeroom, building hallway | Tease / grope / quick contact; full sex gated higher or **interrupted** by the setting (the D56-R2 in-fiction-interruption pattern). |
| **Private** (no exposure) | bedroom, apartment, the diner after close when they're alone | Full ladder, up to sex / sleepover. Private can be **more than one** location. |

**Why this rule exists:** the same act reads differently by place (the verb-overlay anti-pattern, `doctrine/02` §8.1). "Have sex with Hank" at the public breakfast counter is the game pretending the room isn't there — and it's the NPC's risk too (he won't lose his job over the counter). RTS concentrates escalation in private space for exactly this reason: the charge of the private act is that it's private.

**Time and co-present NPCs are *inputs to exposure*, not the gate.** A public location becomes private when it empties: the diner front at 2am, lights off, just the two of them, carries a higher ceiling than the same front at the breakfast rush — not because "it's night," but because the room is empty now. Likewise *who else is scheduled there* (alone vs. with a coworker vs. with an antagonist down the hall) changes exposure. This is why a late-night hub legitimately differs from a morning hub at the same location while the rule stays "exposure," not "time."

**How to apply:** tag each hub with an exposure tier (public / semi-private / private) and offer only rungs at or below that ceiling. The relationship gates (corruption/stage) sit *inside* the permitted rungs as usual.

### §6.3 — D72-R8: An NPC's hubs are mutually consistent

**Rule:** Across all of one NPC's hubs:
- **Relationship state is global** — corruption / relation / stage are per-NPC, not per-location, so progress carries everywhere automatically. The player never re-grinds a relationship per room.
- **Voice + rung identity stay consistent** — the NPC sounds the same everywhere; a given rung keeps the same name and the same gate threshold wherever it appears (no "tease unlocks at corr 5 here but corr 15 there").
- **The full ladder appears wherever it's private** — which can be several locations (D72-R7). It is **context-scaled, not cloned**: a public hub carries only its tier-permitted rungs, not the whole ladder forced into a room that can't support it.

**Optional — locked-visible everywhere.** If you want the ladder telegraphed at every hub for readability, show the higher rungs *locked-visible* (greyed, per §2.6 / D56-R1's sibling) even at public hubs, unlockable only where exposure allows. This gives the "same ladder everywhere" look without making public sex possible. Use it or not by taste; it is not required.

**Why this rule exists:** the worry that drove this — "you can have sex with him at his primary spot but only tease him elsewhere" — is not actually an inconsistency. The relationship is one shared value; only *act availability* varies, and varying it by privacy is realism (flirt in public, fuck in private — exactly how RTS works). The inconsistency to avoid is the mechanical kind: a rung gated differently in two hubs, or the NPC's voice drifting between rooms.

**How to apply:** when authoring an NPC's second/third hub, copy the rung names + gate thresholds + voice from the first; drop the rungs the new location's exposure tier forbids; keep the base + talk + leave. Don't invent a different ladder per room.

---

## §7 — Pre-ship checklist (Appendix-style)

Run before any commit that includes new canvas / capstone / quest card / Lane 3 substitution.

### §7.1 — Per-canvas checks

- [ ] **D56-R1** — Hub canvas has ONE opener paragraph, not tiered (unless legitimate world-state framing)
- [ ] **D56-R2** — If `[group]`-tier-routed, T0/T1 endings land on in-fiction interruption
- [ ] **D56-R5** — `guide` field present + in plain-English recipe form
- [ ] Image-first composition; ≤ 30-word caption density (Lane 1/2/3); Tier-3 register only at Lane 4 capstones
- [ ] Stat-effect macros on cascade beats, not just on entry (P6)
- [ ] Locked-click failures pure information (no stat drain) (P7)
- [ ] No legacy vocabulary (Pattern A–J; ENI-persona references; whiteboard goals; etc.) — see `00_LEGACY_IGNORE.md` §4

### §7.2 — Per-Lane-3 substitution checks (D67-R1–R7)

- [ ] **D67-R1** — Parent activity is a separate `[[canvases]]` entry (not a sub-block of the location hub)
- [ ] **D67-R2** — Stat cost placement decided (`exit_block.effects` vs `pre_substitution_effects`)
- [ ] **D67-R3** — Menu-level gates on location button; dispatcher trusts the menu
- [ ] **D67-R4** — Multi-NPC competition defaults to Pattern A; rule order = narrative priority
- [ ] **D67-R5** — Pattern B only if mutually-exclusive variants; emit `exclusive_group` on each rule (Doc 69 Item 1, 2026-05-27)
- [ ] **D67-R6** — `requires_npc` predicate matches walk-in direction (loose for Lane 3; strict for Lane 2)
- [ ] **D67-R7** — Substitution target has `max_triggers_per_day = 1` + `substitution_only = true`
- [ ] **D56-R3** — Substitution count respects per-arc-shape Lane 3 budget (family 4–7, slow-burn 1–3, peer 0, service 0, antagonist 0 own)

### §7.3 — Per-capstone checks (D57-R1–R5)

- [ ] **D57-R1** — Trigger fingerprint: `is_repeatable = false` (or `true` + self-gate); `priority ≥ 9`; `conditions` include flag-is_false gate; setter-flag effect on exit choice
- [ ] **D57-R2** — Default to Type A; Type B only if branches diverge downstream
- [ ] **D57-R3 / D50-R1** — Capstone is referenced by some quest_card's `ready_canvas` OR has `# off-panel:` comment
- [ ] **D57-R4 / D50-R4** — Predecessor capstone sets the flag this one requires (chain continuity)
- [ ] **D57-R5** — Schedule + location match the fiction
- [ ] **§3.8 voice** — Cascade prose is Tier-3 (specific, layered, character-distinguishing). No Tier-3 spillage in related Lane 2/3 canvases.

### §7.4 — Per-Type-B capstone checks (F1–F5)

- [ ] **F1** — Both branches playable in good faith (Refuse isn't a punishment-button)
- [ ] **F2** — Real divergence in flag-effect, NPC arc, or downstream content
- [ ] **F3** — Fork is at the cascade's terminal beat
- [ ] **F4** — Refuse-path flag policy matches fiction (retry-allowed vs irreversible)
- [ ] **F5** — Not compounded with tier-routing AND multi-step downstream — only one structural device beyond the fork

### §7.5 — Per-quest-card checks (D50-R1–R6)

- [ ] **D50-R1** — Mode declared (capstone / mechanic / hybrid). No `txt_only`.
- [ ] **D50-R2** — Climbing-bullet present when `ready_canvas` has trait gates strictly above card's `when`
- [ ] **D50-R3** — Terminal placement: any `terminal = true` is the LAST card in the NPC chain
- [ ] **D50-R4** — Chain continuity: every "post-X" card has a sibling "pre-X" card pointing at X's setter
- [ ] **D50-R5** — Pure-mechanic cards carry `# unlocks:` comment
- [ ] **D50-R6 (REVERSED)** — `goals[i].label` names the trait ("Corruption" / "<NPC> Relation"), matches sidebar; no raw key paths. (LO pref; see §2.6)
- [ ] **§2.7** — Pure-mechanic chains: each `when` has bounded threshold range; transitions are atomic

### §7.6 — Per-slice / per-arc checks (D56-R3, R4, R7; D72-R6, R7, R8)

- [ ] **D56-R3** — Per-arc-shape Lane 3 budget matches table (family 4–7, slow-burn 1–3, peer 0, service 0, antagonist 0)
- [ ] **D56-R4** — Sidebar surfaces in-scope NPC locations + key stats per the arc's register
- [ ] **D56-R6** — No `txt_only` quest cards in shipped TOML
- [ ] **D56-R7** — Design brief written + canvas distribution matches the brief's declared budget
- [ ] **§3 per-arc distribution** — Canvas count per arc within range (family/ambient 25–35; slow-burn 10–15; peer/dating 8–12; service 6–10; antagonist 6–10)
- [ ] **D72-R6** — Every `[[npcs.schedules]]` row has a Lane 1 hub whose own `trigger.schedules` covers that window (per-row coverage; "a hub at the location" is not enough — it must be open at that time). NPCs with no physical hub carry no schedule row.
- [ ] **D72-R6** — Every hub `base` node renders unconditionally (no escalation-flag gate on the base; gates live on the choices)
- [ ] **D72-R7** — Each hub's rung set respects its location exposure tier (public = talk/look only; semi-private = tease/grope; private = full ladder)
- [ ] **D72-R8** — Same-NPC hubs consistent: shared rung names + gate thresholds + voice; ladder context-scaled, not cloned into public rooms

---

## §8 — Anti-patterns (consolidated, per-rule cross-reference)

For each anti-pattern, the rule it violates.

- **Tiered hub opening on a Lane 1 hub canvas** — violates D56-R1. (Three group blocks for "you walked in" when menu rungs already encode progression.)
- **T0 / T1 cascade ending on a clean "scene complete" beat** — violates D56-R2. (No interruption, no hint of more downstream.)
- **Lane 3 substitutions on a peer/dating or service NPC** — violates D56-R3 + §3 distribution table.
- **Frank-cloning a non-family-ambient NPC** — violates D56-R3 + §3 distribution.
- **Sidebar with only Maya state, no NPC presence** — violates D56-R4 + P10.
- **`txt_only` quest card** — violates D50-R3 + D56-R6.
- **Canvas without `guide` field** (post-doctrine, once Doc 62 ships) — violates D56-R5.
- **Authoring a new NPC without a design brief** — violates D56-R7.
- **Climbing card with no `goals` bullet** — violates D50-R2.
- **Capstone canvas with no card pointing at it** — violates D50-R1 / D57-R3.
- **Premature terminal** (terminal card placed mid-chain) — violates D50-R3.
- **Floating post-X card** (requires flag X with no setter in chain) — violates D50-R4.
- **Mechanic card pointing at vapor** (no actual content opens on threshold cross) — violates D50-R5.
- **Trait-key label in goal block** (e.g., `label = "npc_diana.awareness"`) — violates D50-R6.
- **`is_repeatable = true` capstone with no flag-gate** — violates D57-R1.
- **Capstone with no flag-setter on exit** — violates D57-R1.
- **Type B with collapsible branches** (same flag, same downstream) — violates F2 / D57-R2.
- **Type B fork mid-cascade** (decision at Beat 3 with N beats downstream of both) — violates F3.
- **Type B refuse-as-punishment** (Accept rich, Refuse snarky one-liner) — violates F1.
- **Tier-3 voice in Lane 2/3 prose** — violates D56-R2 + voice register doctrine.
- **RTS-flat-bland voice in capstone** — violates §3.8 voice register.
- **Type C chain with floating step** (Capstone3 requires Flag_2 but no capstone sets it) — violates D57-R4 / D50-R4.
- **Pattern F compounded with tier-routing AND multi-step downstream** — violates F5.
- **Solo activity body inline in location hub** — violates D67-R1.
- **Time-of-day gate on the dispatcher** — violates D67-R3.
- **Multi-NPC substitution rules with no clear priority order** — violates D67-R4.
- **Pattern B authored as Pattern A approximation without flagging** — violates D67-R5.
- **`GetNpcLocation == "Kitchen"` on a Lane 3 walk-in dispatcher** — violates D67-R6.
- **No `max_triggers_per_day` on substitution target** — violates D67-R7.
- **Substitution target without `substitution_only = true`** — violates D67-R7 + pre-ship check §7.2.
- **Schedule row with no live Lane 1 hub** (NPC scheduled at a place/time, but no hub whose own `trigger.schedules` covers it) — violates D72-R6. The schedule page advertises a body the room doesn't deliver.
- **Hub window narrower than the schedule** (one hub open 22:00–01:30 while the NPC is scheduled 06:00–22:00) — violates D72-R6. The daytime rows are dead; period-split into per-window hubs.
- **Lane 2 ambient used as the presence floor** (relying on a `chance` random to acknowledge a scheduled NPC) — violates D72-R6. Dice rolls aren't a floor; author the hub.
- **Flag-gated hub base node** (the base render itself locked behind an escalation flag) — violates D72-R6. Gate the choices, never the act of seeing the NPC.
- **Physical schedule on a hub-less system NPC** (a rent/phone-only landlord carrying a `[[npcs.schedules]]` row) — violates D72-R6 corollary. Drop the schedule or give them a hub.
- **Cloned full ladder across locations / public-space escalation** (the same sex rung offered at a public diner counter) — violates D72-R7 + the verb-overlay anti-pattern in `doctrine/02` §8.1. Scale the ladder to the location's exposure tier.
- **Same NPC, divergent rung gates between hubs** (tease unlocks at corr 5 in one hub, corr 15 in another; voice drifts room to room) — violates D72-R8.

---

## §9 — Cross-references

### Source docs

- `28th_april_TLS_Phase2_Redesign/56_RTS_Principles_and_TLS_Alignment_Doctrine.md` §4 — R1–R7
- `28th_april_TLS_Phase2_Redesign/50_Quest_Card_Shape_Doctrine.md` §4 — R1–R6
- `28th_april_TLS_Phase2_Redesign/57_Capstone_Doctrine.md` §4 + §7 — R1–R5 + F1–F5
- `28th_april_TLS_Phase2_Redesign/67_Solo_Activity_Design_and_Multi_NPC_Dispatcher_Doctrine.md` §6 — R1–R7
- `28th_april_TLS_Phase2_Redesign/72_Presence_and_Logic_Driven_Interaction_Doctrine.md` — presence floor; R6–R8 (per-row hub coverage + exposure-tier ceiling) extend it (see §6)

### Sibling doctrine files

- `doctrine/01_rts_principles.md` — the principle each rule operationalizes
- `doctrine/02_three_lanes_plus_capstone.md` — the mechanism each rule sits inside
- `doctrine/03_arc_shapes.md` — the per-arc-shape distribution that D56-R3 + R7 reference
- `doctrine/05_rts_flat_prose.md` — voice register that capstone Tier-3 + Lane 1/2/3 RTS-flat enforces
- `doctrine/06_design_brief_template.md` — R7 brief structure
- `doctrine/07_anti_patterns.md` — extended anti-pattern catalog (Doc 54's 27 failure modes)

### Validator hooks

- `_validate_quests_cards` (`template_import.py:4469`) — wires D50-R1–R4 + D56-R6
- `_validate_predicate_field_names` (`template_import.py:1098`) — warns on field-name typos
- `_validate_effect_field_names` (`template_import.py:1077`) — warns on field-name typos
- Sidebar trait declaration validator (`template_import.py:2382–2547`) — hard-rejects undeclared traits

### Engine status (rules with pending engine work)

- **D56-R5** `guide` field — doctrine-locked; schema field pending Doc 62 PRD
- **D67-R5** Pattern B `exclusive_group` — ✅ shipped Doc 69 Item 1 (2026-05-27)
- **D67-R2** Pattern C `pre_substitution_effects` — ✅ shipped Doc 69 Item 2 (2026-05-27)

---

**End of file.** Next: `doctrine/09_trait_catalog.md` for canonical trait vocabulary.

═══════════════════════════════════════════════════════════════════════════════

## 9. 05_rts_flat_prose

**Source:** `prompts_v2/doctrine/05_rts_flat_prose.md`

---

# Doctrine 05 — RTS-Flat Prose (the 8 rules + dual register)

**Sources:** Doc 30 §7.1 (the 8 prose rules); Doc 57 §6 (Tier-3 capstone voice register); Doc 13 §9 (three writing tiers verified across 130+ RTS scenes); Doc 54 §5 (voice-failure case studies — the 3 modes the Marge session cost 8 hours to); `feedback_tls_scene_body_style` memory (2026-05-14 8-rule update + 2026-05-24 Lane 4 carve-out).
**Authority:** Doctrine. Voice register for every canvas in every RTS-shape sandbox game.
**Purpose:** Name the default register (RTS-flat) + the earned register (Tier-3 at Lane 4 capstones only) + the 8 mechanical prose rules + the case-study failures that cost time when the register slipped.

This file completes the forward-reference from `doctrine/01_rts_principles.md` P1 + P8 and `doctrine/02_three_lanes_plus_capstone.md` §5.8.

---

## §1 — The dual register

Every canvas in an RTS-shape sandbox sits in ONE of two voice registers. The lane determines which:

| Lane | Register | Why |
|---|---|---|
| **Lane 1 — Hub buttons** | **RTS-flat default** | Player will click these menu items repeatedly across the arc. Re-readable density. |
| **Lane 2 — Ambient encounters** | **RTS-flat default** | Each fires 10–20 times across an arc. Same scene, different stat tiers, same prose density. |
| **Lane 3 — Dispatcher walk-ins** | **RTS-flat default** | Dice-rolled inside chores. Re-readable; specific detail allowed; literary density NOT. |
| **Lane 4 — Capstones** | **Tier-3 literary EARNED** | Once-only narrative milestone. Player won't see this again. Density justified by single read. |

**The contract is "specificity, not literary density."** Lane 2/3 prose can be specific ("the runner Diana picked out") without being literary (no interior monologue, no extended metaphor). Tier-3 is reserved for canvases the player will see once.

---

## §2 — The 8 prose rules (Lane 1/2/3 RTS-flat default)

From Doc 30 §7.1 + `feedback_tls_scene_body_style` memory (2026-05-14 8-rule update). Every Lane 1/2/3 scene body MUST satisfy all 8.

### Rule 1 — Second-person voice

"You" not "she." Maya is "you." Frank is "he" / "Frank" / "him." All scene bodies in Maya's POV via second-person pronoun.

**Example (correct):**
> You take the stool at the counter. Frank slides a coffee across without looking up.

**Anti-pattern (banned):**
> She takes the stool at the counter. Frank slides a coffee across without looking up at her.

### Rule 2 — Stage direction cap: 2 sentences per beat

A "beat" is one click that reveals new content (a `paragraph` block, a `dialog` block, or one cascade step). Stage direction within a beat caps at 2 sentences. After 2 sentences of stage direction, either drop a dialog beat or break into the next click.

**Example (correct):**
> You bend to load the dishwasher. He's at the counter, mug raised. *(2 sentences. Break.)*

**Anti-pattern (banned):**
> You bend to load the dishwasher, conscious of the way the shorts ride up. He's at the counter with his mug raised, glancing at you with the half-smile he gets when he's about to say something. The light through the window catches the dust in the air, and the kettle clicks. *(4 sentences. Over cap.)*

### Rule 3 — Zero environmental sensory detail

No smell. No window light. No kettle clicks. No dust motes. No coffee aroma. The HUD does the world-grounding; prose doesn't repeat the world.

**Why:** P1 — density of decision-pressure over density of prose. The HUD carries world state (time, location, NPC arousal, etc.) continuously. Prose that describes the kitchen smelling of coffee is performing world-grounding the HUD already does — and pays for it on every re-read.

**Example (correct):**
> You pour him coffee. He sets the paper down.

**Anti-pattern (banned):**
> The kitchen smells of coffee and damp wood. Sun catches the dust over the sink. You pour him coffee.

### Rule 4 — Dialogue does the character work, not narration

Character is established through what people say + how they say it. Not through stage direction explaining who they are.

`<<Speech>>` / dialog blocks heavily. Single-line stage direction sets position; dialogue carries the rest.

**Example (correct):**
> [Frank] "Coffee's ready."
> [You]   "Thanks."
> [Frank] "You eat?"

**Anti-pattern (banned):**
> Frank, gruff but secretly soft beneath the rough exterior, gestured at the coffee. His voice carried the weight of a man who'd learned to express care through small acts. "Coffee's ready," he said, the words landing softer than the man who said them.

### Rule 5 — No inferential prose

No "the cup he keeps for her" / "the chair he added when she moved in" / "the way he says her name like it's still new." Surface-level only. The reader gets the same observation Maya gets — no narrator-inferred backstory.

**Why:** inferential prose is a Tier-3 register move (capstone-earned). Lane 1/2/3 stays surface. The cumulative effect of inferred-backstory beats on re-read is performative — Maya can't keep "noticing the cup" 30 times.

**Example (correct):**
> He pours her a coffee.

**Anti-pattern (banned):**
> He pours her a coffee — the same mug she'd reached for on day three, the one with the chipped rim he'd never thrown out.

### Rule 6 — Direct/crude diction (per per-arc vocab ceiling)

Crude is the default at sexual register. "His cock." "Your cunt." "Your tits." Not "his manhood," not "between your legs," not "your chest." Per-arc vocabulary ceiling per `doctrine/08_kink_vocab_ceilings.md` (Doc 30 §7.5) — Frank goes full breeding-talk Phase 2+, Marcus stays peer/school register, etc.

**Default to maximum-explicit interpretation** when ambiguous (per Doc 30 §7.5 2026-05-16 LO pattern — all 7 in-scope rows came back maximum-explicit).

**Example (correct, Tier-4 Frank sex scene):**
> [Frank] "Open your mouth."
> You go down on your knees. His cock against your face.

**Anti-pattern (banned):**
> Frank's voice was low and commanding as he asked her to come closer. She felt herself responding to him, her body alive with something she couldn't name.

### Rule 7 — One beat = one click

Each click in a cascade reveals ONE narrative beat — one paragraph or one dialog exchange or one image+caption combo. Don't pack multi-paragraph internal momentum into a single beat.

**Why:** the click pacing IS the narrative pacing. P6 — stats change during scenes, not just at entry. Each click is a possible stat-effect moment; cramming multiple beats into one click loses the per-click tick.

**Example (correct cascade — 3 beats, 3 clicks):**
> Beat 0: "He's at the counter. He looks up."
> [click] Beat 1: "He sets the mug down. *Quiet.*"
> [click] Beat 2: "He crosses the kitchen toward you."

**Anti-pattern (one mega-beat with internal momentum):**
> One click reveals: "He's at the counter, he looks up, sets the mug down, says 'Quiet,' crosses the kitchen, takes your wrist."

### Rule 8 — Image-first composition

The visual asset (image / video) carries the scene. Prose is the ~30-word caption explaining what's happening, not a full description that paints the image in words.

**Even when images are placeholder-only in Phase 1** (or when no image is shipped), prose stays at the 30-word target. Do NOT compensate for missing visuals with more prose — that's literary drift in disguise. The placeholder visibility IS the missing-image signal; don't paper over it.

**Median RTS scene length:** 137 characters (verified across 274 captured RTS scene bodies in `scene_bodies.jsonl`). P25 = 75 chars. P75 = 500 chars. **Half of RTS scenes are 25 words or less.** Image-first composition is what makes that work.

**Example (correct, image carries scene):**
> [image: scenes/kitchen_morning.jpg]
> [Frank] "Coffee?"
> [You]   "Yeah."

That's the whole beat. ~5 words of prose. The image carries the room + Frank's pose + Maya's POV. Prose pins the dialogue exchange.

**Anti-pattern (prose paints what image shows):**
> The kitchen was warm with morning light, and Frank stood at the counter in his usual flannel, holding two coffee mugs. He looked up as you walked in, his face softening in that way that always made you forget what you were going to say. "Coffee?" he asked. "Yeah, thanks," you said, taking the mug he offered.

---

## §3 — Tier-3 literary register (Lane 4 capstones EARNED)

Capstones get Tier-3 prose. Lane 1/2/3 don't.

### §3.1 — What Tier-3 means

Tier-3 = the rich register reserved for once-only scenes (Lane 4 capstones per Doc 57):

- **Interior monologue + observation tied to memory.** *"The boards she knows the squeak of from the wrong side."* The cumulative effect of past arc beats lands in the prose.
- **Layered sensory detail per beat.** Multiple physical observations woven into one paragraph. NOT the Rule-3 ban on environmental detail — Tier-3 EARNS it.
- **Character-distinguishing diction.** Frank's "girl" / "quiet" / period-not-exclamation. Marge's "hon" / brevity. Ryan's "okay, good" / earnest beat. Each character has a signature cadence that lands more in capstones.
- **Composed rhythm.** Sentences of varying length, deliberate cadence. The flat-sentence-stacking from RTS-flat opens out.

### §3.2 — What Tier-3 is NOT

- **Not generic literary prose.** Specific to the scene's people + place. Frank's first-night opener invokes the specific hallway boards, the runner Diana picked out, the specific bathroom door. Not "the dim hallway in the quiet farmhouse."
- **Not melodramatic.** The prose stays controlled. Frank's "Quiet." carries the weight; the prose around it doesn't underline it.
- **Not unlimited length.** Frank's first-night cascade is ~5,000 chars across multi-node. `canvas_marge_interview` is ~1,900 chars. Density is HIGH; scene length is bounded by what the moment needs.

### §3.3 — Why capstones earn Tier-3 (and Lane 2/3 don't)

A Lane 2 ambient fires 10–20 times across an arc. Authoring it with Tier-3 prose costs the same EACH TIME the player sees it, and after the third reading the language feels performative. Lane 2/3 prose is built to be **re-readable without grating** — that's why it stays RTS-flat structure with specific detail.

A Type A or Type B capstone fires ONCE. The player won't see it again. The prose can be denser because there's no re-reading.

Type C chains use Tier-3 across all their capstones because each beat is once-only. Even when there are 5 chained capstones (Frank), each individual one only fires once.

### §3.4 — Tier-3 example (canvas_marge_interview — Doc 57 §8 Example 1)

```toml
[[canvases.nodes]]
id   = "interview"
blocks = [
  { type = "image", props = { file = "scenes/marge_interview.jpg" } },
  { type = "paragraph", content = "Marge looked up when the bell over the door went off. She didn't smile — Marge wasn't a smiler at first read. She poured a coffee Maya hadn't asked for and slid it across the counter." },
  { type = "dialog", npcId = "npc_marge", content = "You're Diana's girl." },
  { type = "paragraph", content = "Maya nodded. Marge looked her over once — not the up-and-down men did, the up-and-down a woman who had hired forty waitresses did. The shoes. The hands." },
  { type = "dialog", npcId = "npc_marge", content = "Five hours, four-fifty an hour, you keep your tips. Tonight if you want it." },
  { type = "paragraph", content = "She didn't wait for an answer. She slid the apron across with the back of her hand and turned to the next customer." },
]
```

**What makes this Tier-3:**
- "the up-and-down men did, the up-and-down a woman who had hired forty waitresses did" — inferential character work (banned in Lane 1/2/3 per Rule 5; EARNED here)
- "The shoes. The hands." — fragments composed rhythmically (Lane 2/3 would use complete sentences)
- "She didn't wait for an answer" — momentum across paragraphs (Rule 7 one-beat-per-click is relaxed at capstone scale)
- Six beats / ~150 words total — short for Tier-3, but each beat earns density

**What keeps it from over-literary:**
- No environmental sensory detail beyond what advances character (no kettle clicks, no morning light)
- Crude direct diction in dialogue ("Five hours, four-fifty an hour")
- Marge's voice (clipped, transactional, weight-of-experience) is in EVERY line — not described, performed

---

## §4 — Anti-pattern catalogue (cross-register drift)

### §4.1 — Tier-3 voice leaking into Lane 2/3

The Lane 2/3 canvas contains interior monologue, extended metaphor, or memory-callback prose ("she remembered the way the kitchen had looked..."). The prose has drifted.

**Fix:** extract that prose and move it to a capstone. Rewrite the Lane 2/3 canvas RTS-flat with specific detail.

**Doc 54 §5.1 case study:** the Marge `node_shifts` + `node_talk` are 50+ word literary paragraphs that violate Rule 3 + Rule 5. Preserved as canon for now but flagged as a register-split violation; future maintenance pass should rewrite RTS-flat. The Doc 51 → Doc 53 redesign re-authored `node_pour_coffee` + `node_regular_chat` RTS-flat — those are the gold standard for Marge's hub register.

### §4.2 — RTS-flat-bland voice in capstone

The inverse drift: a capstone written with generic Lane 2 prose. Wastes the once-only nature of the scene. If the player isn't going to read this again, the prose should EARN that single read by being specific, layered, and resonant.

**Fix:** rewrite to Tier-3. Add character-distinguishing diction. Add inferential character work. Add the memory-callback that the arc has earned by this point.

**Doc 57 §9 anti-pattern entry.**

### §4.3 — Literary prose on flat surfaces (Doc 54 §5.1)

The most common drift mode. ENI persona instinct toward sensory richness pushes Lane 2/3 prose toward 50-word paragraphs with environmental detail + body-language during dialogue + inferential framing.

**Marge case study (Doc 54 §5.1):** the Pass 1 Marge build had every canvas body at 50+ words with prose like:

> You take the stool at the end of the counter where the napkin holder needs refilling. Marge slides a coffee across without asking how you take it; she's seen you take it twice now.

Compare to the doctrine memory's 30-word template:

> [Marge] "What."
> [You]   "Coffee."
> [Marge] "Two bucks."

The Pass 1 version violated Rules 3 (environmental detail — "napkin holder needs refilling"), Rule 5 (inferential — "she's seen you take it twice now"), and Rule 8 (prose painting what image would carry).

**Fix mechanism:** at the START of any TLS scene/canvas authoring session, explicitly switch register. *"ENI persona OFF. TLS game register ON. Doctrine memory + canonical docs override persona instincts. When in doubt about a craft choice, default to MORE-flat / FEWER-words / FEWER-beats, not the reverse."* (Doc 54 §2.5.)

### §4.4 — Player directives in tip lines (Doc 54 §5.2)

`tip` field is Maya's interior register — first-person observational. NOT player-directive imperative.

**Anti-pattern:** `tip = "Walk into the diner. Don't wait for an invitation."` — directive imperative with place name embedded.

**Correct:** `tip = "Walk in. Ask."` — terse internal resolve. OR Frank's: `tip = "He's around the house all day. I notice that."` — observational, not directive.

If the tip uses imperatives ("Walk into X" / "Click Y" / "Go to Z"), rewrite to interior form. See `feedback_hint_narrative_no_time_or_location` memory + Doc 49 voice rules.

### §4.5 — Schedule / place names / numbers in narrative copy (Doc 54 §5.3)

Quest card `text` / `ready_text` / `tip` contain no:
- Weekday names (Mon/Tue/.../Sun)
- Time references (morning/afternoon/evening/midnight/now)
- Location slugs
- Number formats

These surface automatically from `ready_canvas` metadata (📍 + 🕒 frame) and `goals` evaluation (`◯ X / Y` bullet). Authors don't write them into prose.

**Anti-pattern:** `text = "I should head to the diner on a Monday — Marge said she opens at 9."`

**Correct:** `text = "I need work. Diana said Marge runs the only place that hires off the street."`

### §4.6 — Multi-paragraph stage direction per beat (Rule 2 violation)

The cascade has a beat that runs 3+ sentences of stage direction without a dialog break or click break.

**Fix:** either drop a dialog beat at the 2-sentence mark, or split into two cascade beats with separate clicks.

### §4.7 — Long NPC monologues (Frank-specific, Doc 31 §2)

For Frank specifically: max 3 sentences in a row without Maya cut-in or action beat. Other NPCs follow similar discipline — character voice carries via signature cadence (Marge's brevity, Ryan's earnestness), not via long stretches of single-NPC speech.

---

## §5 — Authoring procedure (the switch + the checklist)

### §5.1 — The register switch

At the start of ANY TLS scene/canvas authoring task (Doc 54 §2.5 lesson):

> ENI persona OFF.
> TLS game register ON.
> Doctrine memory + canonical docs override persona instincts.
> When in doubt about a craft choice, default to MORE-flat / FEWER-words / FEWER-beats, not the reverse.

If a craft instinct conflicts with project memory/doctrine, project wins every time. CLAUDE.md is ignored for canvas authoring (Doc 30 §3 AUTHORITY DECLARATION + `00_LEGACY_IGNORE.md` §3.6).

### §5.2 — Per-canvas pre-ship checklist (Lane 1/2/3 — RTS-flat)

For each new canvas body, verify ALL 8 rules:

- [ ] **R1** Second-person voice ("you" not "she") throughout
- [ ] **R2** Stage direction cap 2 sentences per beat (count sentences in each `paragraph` block)
- [ ] **R3** Zero environmental sensory detail (no smell / window light / kettle clicks / dust motes / etc.)
- [ ] **R4** Dialogue does the character work (heavy `dialog` block use; minimal narrator-explanation)
- [ ] **R5** No inferential prose (no "the cup he keeps for her" — surface-level only)
- [ ] **R6** Direct/crude diction at sexual register (per per-arc vocab ceiling; maximum-explicit default)
- [ ] **R7** One beat = one click (no multi-paragraph internal momentum per beat)
- [ ] **R8** Image-first composition (prose ~30-word caption; total scene length ≤ 30 words target unless cascade)
- [ ] Word count: median 30-50 words per beat; total canvas body within Lane bounds (Lane 1 routed scenes ≤ 200 words; Lane 2 ambients ≤ 100 words; Lane 3 substitutions ≤ 150 words)

### §5.3 — Per-capstone checklist (Lane 4 — Tier-3 earned)

- [ ] **§3.1** Cascade prose is Tier-3 (specific, layered, character-distinguishing diction; composed rhythm)
- [ ] **§3.2** Not generic literary prose; specific to the scene's people + place
- [ ] **§3.2** Not melodramatic; prose stays controlled
- [ ] **§3.2** Length bounded by what the moment needs (Type A ~1,500-2,500 chars; Type B ~4,000-8,000 chars across both branches; Type C step ~1,500-3,000 chars)
- [ ] **§3.3** No Tier-3 spillage into related Lane 2/3 canvases that reference this capstone's content

### §5.4 — Diction sample (the "RTS sanity check")

Pre-flight check before authoring any new canvas:

> *"Could this beat appear in an RTS Brother arc?"*

If "RTS would never write this" — cut. Doc 30 §7.2.

Concretely:
- Could this exact line appear in `BrotherBedroomFlash` (Tier-1 single-render)?
- Could this exact line appear in `BrotherCaughtMasturbating` (Tier-2 cascade)?
- Could this exact line appear in `BrotherBedroomSex1` (Tier-3 full sex cascade)?

If yes — keep. If "this reads like a literary novel and RTS would never ship it" — rewrite RTS-flat.

---

## §6 — Three writing tiers (Doc 13 §9 distribution observation)

RTS doesn't write every scene at the same density. Doc 13 §9 names three tiers, used deliberately per a class of moments.

| Tier | Used for | Function | Length | RTS distribution |
|---|---|---|---|---|
| **Tier 1 — Utility one-liner** | Bedroom Study / Sleep / Nap / generic activity-passes | Pure mechanical confirmation. Text exists only to make the stat-tick acknowledgment feel like something. | ~10 words | ~30 of 130+ scenes (~23%) |
| **Tier 2 — Vignette prose** | Random-encounter scenes with anonymous partners (Brother with "a girl," Dad with "a prostitute," generic strangers in public scenes) | Bridges mechanic to content. Generic descriptive prose with named situations but un-named NPC partners. | ~30–50 words per beat, 2–4 beats per scene via linkreplace | ~70 of 130+ scenes (~54%) |
| **Tier 3 — Scripted character** | Named-NPC introductions, quest beats, arc transitions, capstones | Real character writing. Sensory grounding (where it serves character). Voice. Live-changing speaker labels. The layer that earns the game its narrative weight. | ~150-1000+ words depending on cascade depth | ~30 of 130+ scenes (~23%) |

**The author doesn't waste Tier-3 prose on Tier-1 moments.** Reserved for transitions and named characters. This budget discipline is part of why a 130-scene game ships at all.

### Tier-vs-Lane mapping for TLS

| TLS Lane | Tier (default) |
|---|---|
| Lane 1 hub button (e.g. `BrotherBedroomTease`, `BrotherBedroomFlash`) | Tier 1 utility |
| Lane 1 internally-tiered route target (e.g. `tease_kitchen_general`) | Tier 1 (low tier) → Tier 2 (mid tier) → Tier 2/3 (high tier) within same canvas |
| Lane 2 ambient | Tier 2 vignette |
| Lane 3 substitution target | Tier 2 vignette |
| Lane 4 capstone | Tier 3 scripted character |

**Tier-3 doesn't mean "long."** `canvas_marge_interview` is 1,900 chars — short for Tier-3. Density is what defines tier, not length.

---

## §7 — NPC thought bubbles (4th-dimension primitive per Doc 13 §16 Finding 1)

RTS uses a styled Speech-thought macro to render NPC interior monologue inside scenes:

> 💭 Alfred is thinking...
> *"I can't help myself... she looks so peaceful, so innocent. I just need to touch her..."*

This appears as an italicized speech bubble with the 💭 emoji and a "thinking..." label, distinct from regular speech bubbles. Used in `BedroomSleepDadScene` (3 thought bubbles across 3 beats) and many other scenes.

**Engine support:** TLS has `thought_bubble` block type (shipped 2026-05-06 per Doc 22 §9). Authored as:

```toml
[[canvases.nodes.blocks]]
type = "thought_bubble"
npcId = "npc_frank"
content = "She doesn't know I watch her like this. Good."
```

**When to use thought bubbles:**
- Lane 2/3 ambients with charged interior — adds NPC perspective without Tier-3 spillage (the bubble is a styled UI element, not prose density)
- Lane 4 capstones — extra interiority dimension
- NOT for Lane 1 hub menu routed scenes (too short for interiority)

**When NOT to use:**
- Lane 1 utility menu items (one-line scenes — bubble would be over-weight)
- Maya-only scenes (Maya's POV is the player's POV; thought-bubbles are for NPC interior, not Maya)

The thought_bubble is a 4th-dimension writing primitive **orthogonal to the 3 tiers** (Doc 13 §16 Finding 1). It increases narrative depth without violating the flat-prose mandate — the prose stays flat; the bubble adds character interiority via UI element, not via prose density.

---

## §8 — Worked rewrites (before / after)

### §8.1 — Lane 1 hub menu item rewrite

**Before (ENI-drift literary):**
> Maya pours Frank a cup of coffee, the steam rising between them. She catches the way his hand lingers near hers when he takes the mug, the way he meets her eyes for a moment longer than necessary. There's something unspoken between them that morning — a small recognition that they're both alive to whatever this is becoming.

**After (RTS-flat):**
> [image: scenes/kitchen_morning_pour.jpg]
> [You]   "Coffee."
> [Frank] "Thanks, girl."
> *(+1 marge.trust)*

**What changed:** Rule 3 (no environmental detail — "steam rising"), Rule 5 (no inferential prose — "the way his hand lingers... a small recognition"), Rule 8 (image-first; prose is the caption-frame, not the description-painted-in-words). ~50 words → ~10 words.

### §8.2 — Lane 2 ambient rewrite

**Before (ENI-drift atmospheric):**
> The kitchen at midnight has a different quality of silence — the kind where every floorboard sounds like a confession. Frank is at the counter, his back to you, a glass of something amber in his hand. He doesn't turn when you come in. He's heard you. He waits.

**After (RTS-flat with R2 in-fiction interruption — Doc 56 R2):**
> [image: scenes/kitchen_late_night.jpg]
> Frank's at the counter. He doesn't turn.
> [Frank] "Late."
>
> *(advance: "Cross to him.")*
> You cross. He sets the glass down without looking. His hand finds your hip.
>
> *(T0 end, in-fiction interruption per Doc 56 R2)*
> Diana's floorboard upstairs. He lifts your hand off the counter, hands you the glass, turns the tap on like he was doing dishes.
> [Frank] "Night, girl."

**What changed:** Rule 1 (kept second-person where it was already), Rule 3 (cut atmospheric setup — "midnight has a different quality of silence... like every floorboard sounds like a confession"), Rule 4 (dialogue does the character work — Frank's "Late." / "Night, girl." carries his terse-evening register), Rule 7 (one beat = one click — cascade structure makes pacing explicit), R2 endings on in-fiction interruption.

### §8.3 — Lane 4 capstone (keep Tier-3 EARNED)

**Don't rewrite Tier-3 capstones to RTS-flat.** That's the §4.2 anti-pattern. Keep capstone prose at its Tier-3 density. See `canvas_marge_interview` (§3.4) for the gold standard.

---

## §9 — Cross-references

### Sibling doctrine files

- `doctrine/01_rts_principles.md` — P1 (density of decision-pressure over density of prose); P8 (mechanize the texture; author the points of no return)
- `doctrine/02_three_lanes_plus_capstone.md` §5.8 — voice register summary
- `doctrine/04_authoring_rules.md` — D56-R1 (Lane 1 hub openings constant); D56-R2 (T0/T1 in-fiction interruption)
- `doctrine/06_design_brief_template.md` — R7 brief includes voice spec per NPC
- `doctrine/07_anti_patterns.md` — Doc 54's 27 failure modes (voice failures in §5 of that doc)
- `doctrine/08_kink_vocab_ceilings.md` — Doc 30 §7.5 per-arc vocab ceiling table

### Source docs

- `28th_april_TLS_Phase2_Redesign/30_TLS_Test_Redesign_PRD.md` §7.1 — the 8 prose rules canonical source
- `28th_april_TLS_Phase2_Redesign/57_Capstone_Doctrine.md` §6 — Tier-3 capstone voice register
- `28th_april_TLS_Phase2_Redesign/13_Road_To_Success_Reference.md` §9 — three writing tiers + distribution
- `28th_april_TLS_Phase2_Redesign/13_Road_To_Success_Reference.md` §16 Finding 1 — NPC thought bubble primitive
- `28th_april_TLS_Phase2_Redesign/54_Marge_Redesign_Session_Lessons.md` §5 — voice failures (3 case studies)
- `28th_april_TLS_Phase2_Redesign/31_Frank_Arc_Design_Brief.md` §2 — Frank's voice spec
- `28th_april_TLS_Phase2_Redesign/53_Marge_Redesign_Brief.md` §2 — Marge's voice spec

### Memory entries

- `feedback_tls_scene_body_style` — RTS-flat doctrine source (2026-05-14 8-rule update + 2026-05-24 Lane 4 carve-out)
- `feedback_hint_narrative_no_time_or_location` — Maya-voice rules for tip / quest-card text

### Engine primitives

- `<<Speech>>` macro — dialog block (TLS analog: `dialog` block type with `npcId` + `content`)
- `<<linkreplace>>` cascade — TLS `cascade` block type with `props.beats` (shipped 2026-05-06)
- `thought_bubble` block type — TLS analog of RTS Speech-thought macro (shipped 2026-05-06)

---

**End of file.** Next: `doctrine/06_design_brief_template.md` for R7 brief template.

═══════════════════════════════════════════════════════════════════════════════

## 10. 06_design_brief_template

**Source:** `prompts_v2/doctrine/06_design_brief_template.md`

---

# Doctrine 06 — NPC Design Brief Template (R7)

**Sources:** Doc 56 R7 (no canvas ships before NPC brief); Doc 54 Appendix A (pre-authoring checklist); Doc 31 (Frank brief — family/ambient gold standard); Doc 53 (Marge brief — service gold standard); Docs 58/59/60/61 (Ryan/Jake/Diana/Cookie briefs).
**Authority:** Doctrine. R7 mandates the brief; this file is the template.
**Purpose:** Give the LLM a section-by-section brief template + two gold-standard examples (Frank + Marge) + per-arc-shape adaptations + the pre-authoring checklist.

**The R7 rule:** No canvas for a new NPC ships before that NPC has a written design brief. The brief is the gating step that surfaces shape-mismatches BEFORE prose is committed. Marge cost 8 hours to skip this step (Doc 54). Frank cost ~1 hour because Doc 31 existed first.

Cross-reference: `doctrine/03_arc_shapes.md` (the 5 shapes the brief picks from); `doctrine/04_authoring_rules.md` (the rules the brief commits to honoring); `doctrine/05_rts_flat_prose.md` (the voice spec the brief locks); `doctrine/08_kink_vocab_ceilings.md` (the per-arc ceiling the brief declares).

---

## §1 — The R7 mandate

**Rule (Doc 56 R7):** No canvas for a new NPC ships before the NPC has a written design brief declaring:

1. **Arc shape** — pick from the 5-shape table in `doctrine/03_arc_shapes.md` (family/ambient, slow-burn family, peer/dating, service, antagonist/witness).
2. **Per-lane canvas budget** — Lane 1 / Lane 2 / Lane 3 / capstone counts per tier (per `doctrine/03_arc_shapes.md` §2 distribution).
3. **Vocabulary ceiling** — per Doc 30 §7.5. What does this NPC's content escalate to? What stays off-limits?
4. **Tier flags** — what state changes mark T0 → T1 → T2 transitions for this NPC. Named, not implied.

**Why the rule exists:** Marge wasted 8 hours because authoring started against doctrine designed for escalation NPCs (Doc 54). The brief surfaces shape-mismatches before prose lands. Briefs work.

**Brief file location:** `28th_april_TLS_Phase2_Redesign/<NN>_<NPC>_Design_Brief.md` as a numbered doc (e.g., `31_Frank_Arc_Design_Brief.md`, `53_Marge_Redesign_Brief.md`).

**Brief length:** typically 3–6 pages tabular. Doc 31 = 336 lines. Doc 53 = 322 lines. Doc 58 (Ryan) is shorter (peer/dating arcs need less detail). Doc 60 (Diana) is longer when antagonist branches need spec'ing.

---

## §2 — Brief structure (the 10 sections)

Every R7 brief has these 10 sections. Order matters — §1 (end-state fantasy) gates everything downstream; §3 (ladder) feeds §4 (pretexts); §5 (lane map) compiles §1+§3+§4 into specific canvas slots.

| § | Section | Purpose |
|---|---|---|
| 1 | **End-state fantasy** | One paragraph naming what "arc complete" looks like for this NPC + specific signature scenes |
| 2 | **NPC voice spec** | Background + speech patterns (load-bearing) + per-stage voice samples + dialogue anti-patterns |
| 3 | **Stat ladder + tier mapping** | 6-tier corruption ladder customized for this NPC + capstone gates + content type + per-tier vocab register |
| 4 | **Per-rung pretext shapes** | 4–6 scene-template shapes per tier (the author's content menu) |
| 5 | **Lane-by-lane content map** | Per location: what fills Lane 1 hub / Lane 2 ambients / Lane 3 substitutions / capstones |
| 6 | **Capstones** | Each capstone named with type (A/B/C-step) + trigger + brief shape + flag writes |
| 7 | **Anti-patterns** | What NOT to write for THIS NPC (12+ entries) |
| 8 | **Cross-arc state writes / reads** | What this NPC's scenes write to shared world state + what they read from other arcs |
| 9 | **Cross-references** | Doctrine docs + memory entries + engine primitives + live TLS file pointers |
| 10 | **Acceptance criteria (E1R checkpoint)** | User-readable validation list before authoring begins |

---

## §3 — Section-by-section template

**Scope mode header (added 2026-05-29):** every R7 brief now opens with a scope-mode declaration before §1:

```markdown
**Scope mode:** <full_game | slice>
```

Sections below adapt to the declared scope mode where called out. At `scope_mode: full_game` (default), §1 end-state describes the COMPLETE arc; §3 vocab ceiling rows include Phase 2+ tier content when LO opts in via Stage 1 §0 Q&A; §7 becomes a completeness check against `doctrine/03_arc_shapes.md` §2 per-shape budget. At `scope_mode: slice`, §1 describes slice end-state + Phase 2+ projection; §3 blank rows = slice deferrals; §7 lists canvases missing vs slice target.

### §3.1 — Section 1: End-state fantasy (one paragraph)

```markdown
## §1 End-state fantasy

**<One-sentence summary of the arc's terminal beat for this NPC.>**

<2–4 paragraph elaboration on what "arc complete" looks like. Names specific signature
scenes that define the end-state. Per Doc 54 §2.3 — lock the end-state EXPLICITLY
in this paragraph, not vaguely.>

**Specific signature scenes that define "arc complete":**
- <Scene 1 — concrete description>
- <Scene 2 — concrete description>
- <Scene 3 — concrete description>
- <Phase 2+ extension (when applicable)>

Cross-reference: doc 30 §4.2.
```

**Why §1 is load-bearing:** without an end-state locked in §1, the locked-visible escalation rungs in the slice hub have no shape to telegraph (Doc 54 §3.6). Marge cost 5+ hours partly because §1 was "Phase 3+ deferred" without naming what Phase 3+ IS.

### §3.2 — Section 2: NPC voice spec

```markdown
## §2 <NPC> voice spec

### Background (consolidated from Doc 16 / Doc 30 §4)

<Backstory — 2-3 sentences. What gives this NPC their voice.>

### Speech patterns (load-bearing — every <NPC> line conforms)

| Pattern | Rule | Example |
|---|---|---|
| Sentence length | <e.g., "4-8 words common; verb-chopped"> | "<example>" |
| Names things, not feelings | <how this NPC expresses emotion> | "<example>" |
| Asks questions that aren't questions | <implicit offers / instructions> | "<example>" |
| Rarely names Maya | <pronoun / address style> | "<example>" |
| No exclamations | <punctuation style> | "<example>" |
| No apologizing in words | <how NPC handles regret> | <example>" |
| No backstory unprompted | <what NPC doesn't volunteer> | "<example>" |

### Voice samples per stage

| Stage | Sample line | Tone |
|---|---|---|
| Stage 0 (<arc-shape Stage 0 register>) | "<sample>" | <tone descriptor> |
| Stage 1 (<arc-shape Stage 1 register>) | "<sample>" | <tone descriptor> |
| ... |

### <NPC>-specific framing rules

<Per-NPC vocab framing — e.g., Frank's daddy register kicks in at Stage 3; Marge stays
transactional throughout slice; Jake's incest callouts at all tiers.>

### Anti-patterns — BANNED in <NPC> dialogue

❌ <Banned register 1>
❌ <Banned register 2>
❌ <Banned register 3>
...
```

**Why §2 is load-bearing:** Frank's "Coffee's ready." / "You eat?" terse-transactional register is half of what makes Frank Frank. Without §2, every author re-invents the voice and drift across canvases makes Frank read like multiple different men.

### §3.3 — Section 3: Stat ladder + tier mapping

```markdown
## §3 Corruption ladder mapping (6 tiers)

Universal ladder from doc 30 §4.4 customized for <NPC>.

| Tier | Maya corr | Capstone gate | Content type | Pretext shape category | <NPC vocab register>? | <Cross-arc> awareness write |
|---|---|---|---|---|---|---|
| 0 | 0+ | none | Brushed contact / accidental | <pretext category> | <register on/off> | +N |
| 1 | 5+ | none | Tease / flash (visual only) | <pretext category> | <register on/off> | +N |
| 2 | 15+ | none | Fondle / explicit physical (clothed) | <pretext category> | <register on/off> | +N |
| 3 | 25+ | post-<capstone-1> | Explicit oral / partial sex | <pretext category> | <register starts here> | +N |
| 4 | 35+ | post-<capstone-2> | Full sex | <pretext category> | <register routine> | +N |
| 5 | 50+ | post-<capstone-3> | Routine / sleep-over | <pretext category> | <register default> | +N |

**Tier transitions:**
- 0→1: pure stat (corr 5)
- 1→2: pure stat (corr 15)
- 2→3: stat + flag (corr 25 + <capstone-1-flag>)
- 3→4: stat + flag (corr 35 + <capstone-2-flag>)
- 4→5: stat + flag (corr 50 + <capstone-3-flag>)
- 5→terminal: <capstone-4> + <capstone-5> define arc-complete
```

**Adaptation for non-escalation arcs:** Service NPCs (Marge) and antagonist NPCs (Diana) collapse to 1–2 tiers in slice. Lock the tier count in §3 — empty cells are honest (per Doc 56 R3). Don't pad ladder rows that have no register-valid content.

### §3.4 — Section 4: Per-rung pretext shapes

```markdown
## §4 Per-rung pretext shapes (LOAD-BEARING — author's content menu)

For each tier, 4-6 example pretext shapes. Authors fill Lane 1/2/3 slots by picking a shape
from the appropriate tier and contextualizing it to the location/time. Shapes are SCENE
TEMPLATES, not full scenes.

### Tier 0 (corr 0+, <content type>)
1. <Pretext shape 1>
2. <Pretext shape 2>
3. <Pretext shape 3>
4. <Pretext shape 4>
5. <Pretext shape 5>
6. <Pretext shape 6>

### Tier 1 (corr 5+, <content type>)
1. <Pretext shape 1>
...

(continues for Tier 2, 3, 4, 5)

**Phase 2+ extension (when applicable):** <how pretext shapes evolve when Phase 2+ engine
work ships, e.g., breeding-talk dialogue retrofitted into Tier 5 shapes once pregnancy lands>
```

**Per-tier pretext count:** 4–6 shapes per tier × 6 tiers = 24–36 total. For non-escalation arcs (service / antagonist), Tier 3+ pretext lists may be empty (Phase 2+ deferred).

### §3.5 — Section 5: Lane-by-lane content map

```markdown
## §5 Lane-by-lane content map

One block PER SCHEDULE WINDOW (not just per location) — every `[[npcs.schedules]]` row gets a
Lane 1 hub (D72-R6). Tag each with its exposure tier; the tier caps the hub's rung ceiling (D72-R7).
Cross-references doc 30 §8.1 triage table.

### <Location 1> — <schedule window> — exposure: <public | semi-private | private>

| Slot | Canvas | Tier-content |
|---|---|---|
| Lane 1 hub | <canvas_slug> | Rungs ≤ exposure ceiling: public = talk/look; semi-private = tease/grope; private = full ladder (Tier 0-5 per §3). <vocab register> from Tier <N>+ |
| Lane 2 ambient | <canvas_slug> | Tier <N>+ dice <N>%; <ambient description> (texture ON TOP — never the presence floor) |
| Lane 3 sub | <canvas_slug> | Tier <N>+ dice <N>%; <walk-in description> |
| Capstones | <capstone-1>, <capstone-2> | Per §6 |

### <Location 2> — <schedule window> — exposure: <tier>

(repeats per schedule window — every row covered by a hub)
```

**Match the §5 table to the per-arc-shape distribution (`doctrine/03_arc_shapes.md` §2).** Family/ambient gets 4–7 Lane 3 cells. Peer/dating gets 0. Empty cells are honest for L2/L3 escalation — but every schedule window still gets a Lane 1 hub (the presence floor is independent of the escalation budget; `doctrine/03` §2 note). Same NPC's hubs share rung names + gate thresholds + voice (D72-R8).

### §3.6 — Section 6: Capstones

```markdown
## §6 Capstones (<N> scripted moments)

Per `doctrine/02_three_lanes_plus_capstone.md` §5. Each capstone is Tier-3 literary
per `doctrine/05_rts_flat_prose.md` §3.

| # | Capstone | Type | Status | Trigger | Brief shape | Flag writes |
|---|---|---|---|---|---|---|
| 1 | <Capstone-1 name> | A (linear) | NEW / Existing-polish-only | <trigger condition> | <2-sentence summary> | <flag set on exit> |
| 2 | <Capstone-2 name> | A or B | NEW | <trigger condition> | <2-sentence summary> | <flag set on exit> |
| 3 | <Capstone-3 name> | B (branching) | NEW | <trigger condition> | <2-sentence summary + branch fork detail> | <flags set per branch> |
| ... |
```

**Capstone count by arc shape** (per `doctrine/03_arc_shapes.md` §3.5):

| Arc shape | Capstone count |
|---|---|
| Family/ambient | 3–6 (Type A 1–2 + Type B 1–2 + Type C chain 4–5) |
| Slow-burn family | 2–5 |
| Peer/dating | 2–5 |
| Service | 1–3 |
| Antagonist/witness | 1–3 |

### §3.7 — Section 7: Anti-patterns

```markdown
## §7 Anti-patterns (what NOT to write for <NPC>)

Hard bans for ALL <NPC> canvas authoring. 12+ entries.

❌ **<NPC>-specific anti-pattern 1** — <description>
❌ **<NPC>-specific anti-pattern 2** — <description>
❌ **<NPC>-specific anti-pattern 3** — <description>
...

(plus per-NPC voice ban list from §2)
```

**Minimum 12 anti-patterns.** Doc 31 §7 has 12. Doc 53 §7 has 8 (smaller arc, smaller anti-pattern surface, but should still hit 8+). The anti-patterns are tactical — they catch the specific drift modes the NPC's register invites.

### §3.8 — Section 8: Cross-arc state writes / reads

```markdown
## §8 Cross-arc state writes / reads

### What <NPC> scenes WRITE

| State | Trigger | Effect |
|---|---|---|
| `<NPC>.arousal +1-2` | Per beat in any Lane scene | Universal |
| `Maya.corr +1` | Per Tier 1+ beat | Universal |
| `<NPC>.corr +1` | Per Tier 2+ beat | <NPC>'s own corruption escalates |
| `<capstone-flag-1>` | Capstone 1 (catch) | Stage 1→2 transition |
| `<capstone-flag-2>` | Capstone 2 (declaration) | Stage 2→3→4 |
| ... |
| `<cross-arc-write-trait>` | Per <condition> | <effect on other arcs> |

### What <NPC> scenes READ

| State | Source arc | Effect on <NPC> scenes |
|---|---|---|
| `<cross-arc-read-trait>` | <source NPC arc> | <how <NPC>'s scenes branch on it> |
| `outfit_id` | Wardrobe system | Certain Lane 2 ambients fire only in <specific outfit> |
| ... |
```

### §3.9 — Section 9: Cross-references

```markdown
## §9 Cross-references

| Doc | Purpose |
|---|---|
| `30_TLS_Test_Redesign_PRD.md` | Master PRD |
| `13_Road_to_Success_Reference.md` | RTS pattern source-of-truth |
| `24_RTS_Three_Lanes_Repeatable_Activities.md` | Lane 1/2/3 architecture |
| `<source-doc-1>` | <purpose> |
| Memory `feedback_tls_scene_body_style.md` | Voice rules |
| ...
```

### §3.10 — Section 10: Acceptance criteria (E1R checkpoint)

```markdown
## §10 E1 acceptance criteria (E1R checkpoint)

User reads §1 + §3 + §4 within 24 hours of brief ship. Validates:

- [ ] **§1** end-state paragraph names the fantasy with specific signature scenes (not vague)
- [ ] **§3** ladder table covers all 6 tiers (or fewer for non-escalation arcs) with the per-tier columns
- [ ] **§4** per-rung shape table gives 4-6 examples per tier (24-36 total shapes for escalation arcs)
- [ ] **§5** lane content map covers all NPC-relevant hubs
- [ ] **§6** all capstones named with type + trigger + brief shape + flag writes
- [ ] **§7** anti-patterns capture drift modes + NPC-specific pitfalls (12+ entries)
- [ ] **§8** cross-arc writes/reads tabulated (slice + Phase 2+ split clear)
- [ ] **§9** cross-references complete
- [ ] **No drift into authoring scene PROSE** — brief is shape spec, not content
- [ ] Length 3-6 pages — verify

**Pass/fail:** all checkboxes pass → authoring starts. Any unchecked → rewrite that section.

**User time estimate:** ~15-20 minutes for review.
```

---

## §4 — Worked example 1: Frank (family/ambient gold standard)

Doc 31 distilled (Frank Arc Design Brief 2026-05-16). The full doc is at `28th_april_TLS_Phase2_Redesign/31_Frank_Arc_Design_Brief.md` — this section names what makes it the gold standard.

### Why Doc 31 works

- **§1 end-state explicit:** "Maya becomes Frank's secret-then-open second wife." Names 5 specific signature scenes (Maya in Frank's bed nightly + Frank fucks Maya bareback + Maya calls Frank "daddy" + Diana confrontation resolved + Phase 2+ pregnancy retrofit). The full-arc trajectory is LOCKED in §1.
- **§2 voice spec dense:** 7 speech patterns with rule + example each ("Sentence length: 4-8 words common; verb-chopped. Example: 'Coffee's ready.' 'Door's stuck.'"). 6 stage-by-stage voice samples. Per-NPC framing rules (daddy register Stage 3+ for Maya; Stage 4+ for Frank). 9 banned registers in dialogue.
- **§3 6-tier ladder:** every column populated (Maya corr / capstone gate / content type / pretext shape category / daddy register / Diana awareness write). Tier transitions named.
- **§4 30+ pretext shapes:** 6 shapes × 6 tiers = 36 example pretext shapes. Phase 2+ extension named.
- **§5 4 locations × all lanes:** Frank's bedroom + Kitchen + Living Room + Yard. Per location, every lane slot filled with canvas slug + tier-content description.
- **§6 5 capstones:** Type A catch + Type A declaration + Type B first-night + Type A sleep-over + Type B Diana confrontation. Each with trigger + brief shape + flag writes.
- **§7 12 anti-patterns:** all Frank-specific (no atmospheric prose / no Frank apologizing / no honey-sweetheart register / no third-person voice / etc.).
- **§8 cross-arc tabulated:** 14 writes + 6 reads, slice vs Phase 2+ split clear.
- **§10 acceptance criteria:** 10 checkboxes.

### Frank Lane budget (per §3 in `doctrine/03_arc_shapes.md`)

Family/ambient gets the dense distribution: 25–35 total canvases.

| Lane | Tier | Frank canvas count | Examples |
|---|---|---|---|
| L1 | T1 | 2 base + 2 self-display | `frank_kitchen_morning_hub`, `frank_kitchen_dinner_hub`, `tease_kitchen_general`, `flash_kitchen_general` |
| L1 | T2–T3 | 4 mid + explicit | hub variants + sex loop |
| L2 | T1–T3 | 6 ambients (morning + evening + late-night) | `ambient_kitchen_morning_chat`, `ambient_kitchen_late_night_raid`, etc. |
| L3 | T1–T3 | 7 substitutions | `scene_frank_passes_kitchen_door`, `scene_frank_walks_in_shower`, etc. |
| Capstones | — | 5 | catch → first-night → declaration → sleepover → Diana confrontation |

**Total Frank canvases: ~28.** Within the 25–35 family/ambient range.

---

## §5 — Worked example 2: Marge (service gold standard)

Doc 53 distilled (Marge Redesign Brief 2026-05-24). The full doc is at `28th_april_TLS_Phase2_Redesign/53_Marge_Redesign_Brief.md`.

### Why Doc 53 works (after Doc 51 failure → Doc 53 redesign)

- **§1 names the service-NPC adaptation:** "Lane 2 reduces to relational only. Lane 3 = 0. Lane 4 capstones = 1–2." The brief codifies WHY this NPC's distribution differs from Frank's — empty cells are honest for service register.
- **§2 voice spec terse-transactional:** Marge's "What." / "Coffee." / "Two bucks." template captured. Per-arc vocab ceiling: workplace seduction matriarch-dom is the Phase 3+ endpoint; slice ships only relational + worked-shifts.
- **§3 collapsed ladder:** 1 unlocked tier + locked-visible Phase 3+ rungs. Doctrine compliance: "empty cells are honest" — the Phase 3+ tiers ship as locked-visible stubs, not as authored content.
- **§4 minimal pretext shapes:** few in slice (relational only). Locked-visible rungs gesture at Phase 3+ shapes.
- **§5 single hub:** `scene_marge_diner_hub`. 8 menu items: 4 unlocked relational (Pour coffee / Talk / Ask shifts / Ask about a regular) + 4 locked-visible escalation rungs (Tease / Flash / Eat her out / Let her take you) gated by corruption thresholds. + 1 Leave.
- **§6 1 capstone (slice):** `canvas_marge_interview` (Type A — hire moment). Mid-arc escalation deferred to Phase 3+.
- **§7 8 anti-patterns:** "Adding more hub items to drive trust climb" (worked shifts ARE the climb) / "Lane 2 ambients without physical contact" / "Cookie content inside Marge's lanes" / etc.
- **§8 cross-arc:** Marge writes `hired_at_diner` (gates rent), reads `outfit_id` (decent required for floor work). Minimal cross-arc surface because slice is bounded.

### Marge Lane budget (per `doctrine/03_arc_shapes.md`)

Service shape: 6–10 total canvases in slice.

| Lane | Tier | Marge canvas count | Examples |
|---|---|---|---|
| L1 | T1 | 1 (hub with 4 unlocked items) + 4 locked-visible stubs | `scene_marge_diner_hub` + 4 stub canvases (`tease_diner_marge`, `flash_diner_marge`, `marge_eat_her_out`, `marge_let_her_take`) |
| L2 | — | **0** in slice | Phase 3+ |
| L3 | — | **0** in slice | Phase 3+ |
| Capstones | — | 1 in slice | `canvas_marge_interview` (Type A) |

**Total Marge slice canvases: 6 (hub + 4 stubs + capstone). Within 6–10 service range.**

---

## §6 — Per-arc-shape adaptations

### §6.1 — Slow-burn family (Jake, Doc 59)

The brief follows the same 10-section template but with:
- **§3 ladder:** 2–5 stages instead of 6 tiers. Slow-burn doesn't have full sexual escalation in slice — stage 0 (Hostile) → stage 1 (Noticed) → stage 2 (Peek/Draw) → stage 3 (Tease) → stage 4 (Caught).
- **§4 pretexts:** smaller catalog (1–3 shapes per stage). Slow-burn means concentrated beats, not saturated.
- **§5 lanes:** L1 1–2 + L2 1–2 + **L3 1–3** (slow-burn DOES get walk-ins — they ARE the milestones) + capstones 3–5.
- **§6 capstones:** dual-path Stage 0→1 (via_beauty + via_glance — Doc 57 §9 duplicate-prose engine exemption).
- **§7 anti-patterns:** "Family/ambient saturation" (don't pad Jake with Frank-style Lane 2 ambients), "Vanilla framing during sex" (incest IS the kink, callouts at all tiers).

### §6.2 — Peer/dating (Ryan, Doc 58)

- **§3 ladder:** Stage 0 (meet) → Stage 1 (notice) → Stage 2 (partner) → Stage 3+ (consummation, Phase 2+) → Stage 4 (relationship). Peer arcs don't use the universal 6-tier corruption ladder — they use relation-driven stages.
- **§4 pretexts:** date contexts, shared activities, relation-build moments. Not sexual-tier shapes.
- **§5 lanes:** L1 2–3 + L2 1–2 + **L3 = 0** + capstones 3–4. Peer doesn't interrupt private chores.
- **§6 capstones:** Type A first-date + Type A second-date + Type B partner-commit (Phase 2+).
- **§7 anti-patterns:** "Frank-cloning" (don't apply family/ambient saturation), "Lane 3 substitutions on a peer" (Doc 56 R3 violation).

### §6.3 — Antagonist/witness (Diana, Doc 60)

- **§3 NO arc_stages.** Diana uses an awareness accumulator (0–100 silent trait) instead of discrete stages. Bands: cold (0–24) / suspicious (25–49) / knowing (50–74) / shut-out (75–100).
- **§4 pretexts:** presence beats, witness moments, confrontation precursors. Not Maya-with-NPC escalation shapes.
- **§5 lanes:** L1 0–1 + L2 1–2 + **L3 = 0 own** (appears as INTERRUPTOR in Frank's L3 endings) + capstones 1–2.
- **§6 capstones:** Type B confrontation (kicked_out + brought_in branches scripted; blackmail + matriarch deferred Phase 2+ per Doc 60).
- **§7 anti-patterns:** "Exposing awareness to sidebar" (dramatic surprise depends on hiding), "Treating Diana as escalation NPC" (she's the threat/cost, not the seduction target).

### §6.4 — Phase 3+ scope-out (Cookie, Doc 61)

Cookie doesn't get a full brief — she gets a **formal scope-out** under Doc 57 R7 compliance. The doc structure:

| § | Section |
|---|---|
| 1 | Why this is a scope-out, not a brief |
| 2 | Slice deferrals (what's NOT shipped) |
| 3 | Phase 3+ triggers (when authoring would begin) |
| 4 | Slice presence (what IS shipped — Cookie appears in Marge's diner co-presence ambient + Marge's R7 brief mentions her) |
| 5 | Doctrine compliance record (Doc 57 R7 + Doc 30 §8.2) |

Use this format for ANY NPC whose arc is Phase 3+ deferred. The scope-out is the documentation that the deferral is intentional (per Doc 56 R7), not an authoring oversight.

---

## §7 — Pre-authoring checklist (Doc 54 Appendix A adapted)

Run BEFORE authoring any new NPC content. Paste into PR description.

### Process
- [ ] Canonical output path confirmed with user (for TLS: `games/the_long_summer_test/output/`)
- [ ] All relevant doctrine memory entries listed + read in full (search: voice, lane, NPC, scene-body, quest)
- [ ] All canonical doctrine docs referenced by memory entries also read IN FULL
- [ ] Full-arc trajectory locked in one sentence in the brief's §1
- [ ] ENI persona OFF / TLS game register ON declared explicitly at session start
- [ ] Side-by-side audit against gold-standard reference (Frank `frank_kitchen_morning_hub` for hub; Marge `scene_marge_diner_hub` for service-NPC hub) BEFORE any new authoring

### Design
- [ ] Hub menu cap: ~5 items unlocked + locked-visible escalation ladder
- [ ] Every hub menu verb passes the pronoun-in-the-verb test (Maya-with-NPC)
- [ ] No work-task items in the hub
- [ ] Lane 2/3 scope: if no escalation register in slice, both are EMPTY in slice
- [ ] Other-NPC content (Cookie etc.) stays in their own future surfaces

### Doctrine
- [ ] Every quest card mode declared (capstone / mechanic / hybrid)
- [ ] `ready_canvas` only on capstone cards
- [ ] Mechanic chain `when` clauses bounded
- [ ] No `terminal = true` unless it's the absolute LAST card in the FULL arc
- [ ] Locked-visible escalation ladder visible from day 1 (for any sexual-arc NPC)

### Voice
- [ ] Every canvas body fits the < 30-word speaker-tag template
- [ ] Tip lines are Maya-interior observational, not player-directive
- [ ] No weekday names, time references, location slugs, or numbers in narrative copy
- [ ] ENI literary instinct disabled for canvas body authoring

### Structural
- [ ] Route-target stubs have NO `[canvases.trigger]` block
- [ ] Side-by-side audit completed (per process checklist)

### Verification (post-authoring, pre-shipping)
- [ ] Validator dry-run clean
- [ ] Build to canonical output path with `--dev --debug`
- [ ] Prose grep in HTML returns all new strings
- [ ] Frame check: mentally render each card at each Maya state combination
- [ ] Live-play dev-bump test PERFORMED, not deferred

---

## §8 — Anti-patterns (brief authoring failures)

From Doc 54 lessons learned + per-brief audits.

### §8.1 — Brief without §1 end-state lock (Doc 54 §2.3)

Brief says "Phase 3+ deferred" without naming WHAT Phase 3+ IS. Slice authoring then has no trajectory to telegraph; locked-visible rungs have no shape.

**Fix:** §1 names the FULL arc endpoint explicitly. Even if the slice doesn't ship that endpoint, the brief locks it.

### §8.2 — Brief sans voice spec §2 (Doc 31 / Doc 53 case)

Brief jumps to §3 ladder without locking voice spec. Result: every author re-invents NPC voice across canvases; drift accumulates within the slice.

**Fix:** §2 always present. 7 speech patterns + 6 stage-by-stage voice samples + 9+ banned dialogue patterns. Locked.

### §8.3 — Brief padding empty distribution cells (Doc 54 §3.4)

Service NPC brief authors 6 Lane 2 ambients + 3 Lane 3 substitutions because "all NPCs need all 3 lanes populated." This is wrong. Service register doesn't carry Lane 2/3 content; empty cells are honest.

**Fix:** match brief budget to `doctrine/03_arc_shapes.md` §2 distribution. Empty cells declared empty. Phase 3+ stubs declared as locked-visible, not as authored content.

### §8.4 — Brief with no anti-patterns §7

Doc 31 § 7 has 12 banned patterns; Doc 53 §7 has 8. A brief with §7 missing or under 6 anti-patterns lacks the tactical drift catches — the author re-invents drift modes the brief should have caught.

**Fix:** §7 mandatory, 8+ anti-patterns. NPC-specific drift modes (Frank apologizing in words; Marge using warmth-bombs; Jake without incest callouts).

### §8.5 — Brief authored against gold-standard NPC without side-by-side audit (Doc 54 §6.3)

Marge cost 5+ correction round-trips because Doc 51 was authored without a line-by-line side-by-side audit against Frank's hub. The brief used Frank's vocabulary (Lane 1, Lane 2, Lane 3) but applied it wrong (over-weighted Lane 1, padded Lane 2/3).

**Fix:** BEFORE authoring brief §5 lane map, read `frank_kitchen_morning_hub` line by line. List its structural features. Mirror them unless there's an explicit doctrine reason to diverge. Same for `scene_marge_diner_hub` for service-NPC briefs.

### §8.6 — Brief skipping §6 capstones

Brief covers §1–§5 + §7 but no §6 capstones spec. Authoring then produces canvases without trigger fingerprints (Doc 57 R1) + without quest card pointers (Doc 50 R1).

**Fix:** §6 mandatory. Every capstone named with type (A/B/C-step) + trigger + brief shape (2 sentences) + flag writes.

---

## §9 — Cross-references

### Sibling doctrine files

- `doctrine/03_arc_shapes.md` — the 5 shapes the brief picks from + per-arc distribution
- `doctrine/04_authoring_rules.md` — R7 (this brief is the artifact R7 mandates)
- `doctrine/05_rts_flat_prose.md` — voice spec the brief locks in §2
- `doctrine/08_kink_vocab_ceilings.md` — per-arc vocab ceiling the brief declares
- `doctrine/07_anti_patterns.md` — anti-pattern catalog (brief §7 is the NPC-specific subset)

### Source briefs (gold standards)

- `28th_april_TLS_Phase2_Redesign/31_Frank_Arc_Design_Brief.md` — family/ambient gold standard
- `28th_april_TLS_Phase2_Redesign/53_Marge_Redesign_Brief.md` — service gold standard
- `28th_april_TLS_Phase2_Redesign/58_Ryan_Design_Brief.md` — peer/dating
- `28th_april_TLS_Phase2_Redesign/59_Jake_Design_Brief.md` — slow-burn family
- `28th_april_TLS_Phase2_Redesign/60_Diana_Design_Brief.md` — antagonist/witness (🔴 BLOCKED on Open Q #3)
- `28th_april_TLS_Phase2_Redesign/61_Cookie_Phase3_Scope_Out.md` — Phase 3+ scope-out template

### Source docs

- `28th_april_TLS_Phase2_Redesign/56_RTS_Principles_and_TLS_Alignment_Doctrine.md` §4 R7 — the rule this template implements
- `28th_april_TLS_Phase2_Redesign/54_Marge_Redesign_Session_Lessons.md` — failure modes that birthed R7

---

**End of file.** Next: `doctrine/07_anti_patterns.md` for the consolidated anti-pattern catalog.

═══════════════════════════════════════════════════════════════════════════════

## 11. 07_anti_patterns

**Source:** `prompts_v2/doctrine/07_anti_patterns.md`

---

# Doctrine 07 — Anti-Patterns (Consolidated Failure-Mode Catalog)

**Sources:** Doc 54 (27 failure modes / 6 categories — the Marge session lessons); Doc 56 §8; Doc 50 §8; Doc 57 §9; Doc 67 §9.
**Authority:** Doctrine. Concrete shapes to NOT ship.
**Purpose:** Catalog every documented failure mode + cross-doc anti-pattern with cause, doctrine impact, and prevention rule. Run the §9 checklist before any new NPC authoring.

Each entry has: **What happened** / **Why** / **Doctrine impact** / **Prevention rule**. For drift modes from the cross-doc anti-pattern lists (§8), each entry has rule-violation + fix.

---

## §1 — How to use this file

This file is reference. Pull from it when:

- **Pre-authoring (R7 brief writing):** §2.5 + §6.3 + §9 are load-bearing
- **Per-canvas pre-ship check:** §3 + §4 + §5 + §6 catch the per-canvas drift modes
- **Quality gate / code review:** §8 is the consolidated anti-pattern grep target
- **Recovery from drift mid-arc:** §7 names when to strip-clean vs incremental fix

The 27 Doc 54 failure modes are organized by category. Each cost a measurable amount of session time when it first surfaced — recovering one of them costs the same time again. Pre-emption is the cheapest version.

**Scope-mode applicability:** anti-patterns in §2–§7 default to **any-scope** (they apply at both `scope_mode: slice` and `scope_mode: full_game`). Slice-specific failure modes are explicitly tagged `(slice-only)`. Full-game-specific failure modes live in §8.6 (added when full-game scope shipped as first-class, 2026-05-29).

---

## §2 — Process failures (6 entries — Doc 54 §2)

### §2.1 — Build path mistake (~3 hr investigation cost)

**What happened:** every build went to `/private/tmp/...` while LO was opening `games/.../output/index.html`. The canonical output file predated the entire authoring pass. When LO reported "Marge isn't showing on the quests page," ~3 hours of investigation followed before discovering the build-path divergence.

**Why:** the `package_from_toml` command takes `--output` as a required argument. Defaulting to `/tmp` paths for "quick verification builds" without checking what the project's canonical output location was. Each pass shipped to a different `/tmp` directory.

**Doctrine impact:** not a doctrine issue; pure tooling miss. But it cascaded — every "the build is clean" assertion was true of `/tmp` builds that LO never opened.

**Prevention rule:** BEFORE the first build of any session, ask the user where the canonical output goes. For TLS specifically: `games/the_long_summer_test/output/`. If the build is intentionally a transient sanity-check, flag it explicitly: *"build to /tmp/scratch — not the canonical path; rebuild canonically before live-play."*

### §2.2 — Doctrine memory not consulted first (every voice failure traces here)

**What happened:** `feedback_tls_scene_body_style` memory was 9 days old at session start. Contains 8 explicit RTS-flat style rules + a content-selection rule for Lane 2 ambients. The memory was not read until LO surfaced the gap. By that point ~15 canvases violated those rules.

**Why:** assumed ENI persona's literary-IF instinct (per CLAUDE.md craft rules) was the right register for canvas authoring. Didn't audit own assumption against project-specific memory.

**Doctrine impact:** catastrophic. Every Lane 1 hub item, Lane 2 ambient, Lane 3 substitution, and quest card prose violated the memory's rules. Full strip + re-author was unavoidable.

**Prevention rule:** BEFORE authoring ANY prose in the slice, list every relevant doctrine memory entry. Search topics: voice, lane, NPC, scene-body, quest. Read each in full. If a memory says *"X is banned"*, X is banned — even if persona instinct pushes for X. **ENI persona is for chat/roleplay; project memory governs in-game authoring.**

### §2.3 — Question avoidance (Marge sexual-arc question deferred 5+ hours)

**What happened:** for the first half of the session, kept saying *"Phase 3+ deferred"* about Marge's sexual content without committing to what Phase 3+ actually IS. After hours of design work, LO had to ask directly. The answer (workplace seduction matriarch-dom, Cookie as lesbian first-fling) was in Doc 30 §8.2 line 87 — read but never internalized as a design-locking commitment.

**Why:** treated *"Phase 3+ deferred"* as a wand that resolved the design question. Actually it just postpones authoring while leaving the trajectory shape unanswered.

**Doctrine impact:** produced a doctrinally-malformed Lane 1 (no escalation ladder because no escalation target identified). Doc 53 v1 had to be corrected after LO surfaced the sexual-arc question explicitly.

**Prevention rule:** BEFORE designing an NPC's slice scope, identify the full-arc endpoint EXPLICITLY in the brief's §1. One sentence: *"Marge becomes a workplace-seduction matriarch-dom partner; Cookie joins as lesbian first-fling per Doc 30 §3."* That sentence locks the trajectory. Locked-visible Phase 3+ rungs in the slice hub make sense from day 1 once it's locked.

### §2.4 — Canonical doctrine DOCS not consulted, not just memory

**What happened:** §2.2 captures memory-not-read. Same disease applies to docs. Mid-session LO had to say *"go back to the redesign phase 2 docs, analyze the 3 lanes docs"* — Doc 24 §10 contained the lane vocabulary + grid balance rules + arc-flow doctrine. Read the memory, assumed the doc was just a longer version, was wrong.

**Why:** treated memory entries as sufficient when they're actually pointers. Memory typically captures the rule's distilled form; the doc has worked examples + edge cases + nuance.

**Doctrine impact:** authored multiple Lane 2/3 surfaces against rules that the memory summarized but didn't fully spell out. Reading Doc 24 §10 in full would've shown the "Lane 2 must have charged contact in beat 1" content rule had a worked-example backbone.

**Prevention rule:** when a memory entry references a doctrine doc, read the doc IN FULL too. Memory + doc is the unit, not memory alone. Specifically: any time the memory's description starts with *"Doc N — ..."*, the doc is required reading before authoring against the rule.

### §2.5 — ENI persona override meta-pattern (load-bearing prevention rule)

**What happened:** the ENI persona instinct pushed toward maximalism in at least four distinct dimensions:
- §5.1 — atmospheric prose where RTS-flat was required
- §3.4 — Lane 2/3 padding to "fill the world" where doctrine said empty
- §3.1 — hub menu over-weighting for "richness" where doctrine capped at ~5
- §3.2 — work-task items added for "escalation depth" where doctrine said Maya-with-NPC only

All four trace to the same root: ENI persona's craft instincts pulling toward maximalism when project doctrine demands restraint. **The persona is literary; the project doctrine is transactional; they pull in opposite directions on every authoring decision.**

**Why:** ENI persona is the default register (per CLAUDE.md). Project doctrine is the override. Without a deliberate switch, the default wins.

**Doctrine impact:** caused ~70% of the session's wrong-shape authoring. Other 30% was process failures.

**Prevention rule (load-bearing):** AT THE START of any TLS scene/canvas authoring session, explicitly switch register. Say to yourself:

> *"ENI persona OFF. TLS game register ON. Doctrine memory + canonical docs override persona instincts. When in doubt about a craft choice, default to MORE-flat / FEWER-items / EMPTIER-lanes, not the reverse."*

If a craft instinct conflicts with project memory/doctrine, project wins every time.

### §2.6 — "Half-getting it" — partial fixes shipped without clarifying questions

**What happened:** LO had to make the same critique multiple times across the session. When LO surfaced a critique, default was to immediately respond with a fix. The fix addressed what was thought to be the issue, ship, then LO had to re-escalate with the actual point. Took 3 rounds to land each major critique.

**Why:** treated immediate-fix as the productive response. Faster to ask "what specifically is the full scope of the issue?" than to ship-then-re-fix.

**Doctrine impact:** ~3 hours wasted in half-applied fix loops.

**Prevention rule:** when LO surfaces a critique, BEFORE responding with a fix, ask: *"is the issue X, or X + Y, or something deeper?"* Use AskUserQuestion if uncertain. Half-applied fixes burn 3 round-trips where one clarifying question would've burned zero.

---

## §3 — Design failures (7 entries — Doc 54 §3)

### §3.1 — Lane 1 over-weighting (menu-game anti-pattern)

**What happened:** shipped 10 hub menu items in Marge's hub (8 new + 2 pre-existing). Frank's per-location hubs cap at 5–6 items. Over-weighted hub was the exact anti-pattern Doc 24 §10.3 warned against: *"All Lane 1 → fully transactional experience, low surprise, 'menu game' feel."*

**Why:** tried to give Marge T0/T1/T2 menu progression where each tier added 3 new items. Treated hub menu items as the trust-climb mechanism instead of recognizing that worked shifts (`scene_diner_t0_shift` grants +1 marge.trust per shift) were the doctrinally-correct climb.

**Doctrine impact:** explicit Doc 24 §10.3 violation. Result was a trust-grinder where Maya could spam coffee + regular_chat to climb trust without ever working a shift.

**Prevention rule:** cap NPC hub menu at ~5 items unlocked. If more rungs are needed, they should be locked-visible escalation rungs (Tease/Flash/etc.) per §4.5, NOT parallel work-task buttons. Hub items should be Maya-NPC interaction verbs only.

### §3.2 — Verb register failure (NPC not in the verb)

**What happened:** hub items included *"Take a long shift"*, *"Close out alone"*, *"Run the late shift solo"*. Marge isn't the syntactic object of any of those verbs. Even *"Close out the diner WITH Marge"* had a scene body where Marge handed off the closing folder and went home — Marge off-stage for most of the scene.

**Why:** forced the 3-lane doctrine onto a service-NPC by inventing work-themed items. Missed that Lane 1 verbs by definition have the NPC as object. Frank's pattern (*"Pour HIM coffee"* / *"Tease HIM"* / *"Suck HIM"* / *"Have sex WITH HIM"*) has the NPC pronoun literally inside the verb structure.

**Doctrine impact:** five of eight new hub items were doctrinally wrong content type — they belonged on a different surface (location-triggered work canvas), not Marge's hub.

**Prevention rule:** read each proposed hub menu choice. If the NPC is not the syntactic object of the verb, it's not a Lane 1 hub item. **Apply the pronoun-in-the-verb test:**
- *"Pour her coffee"* → her ✓ — Lane 1
- *"Tease her"* → her ✓ — Lane 1
- *"Take a long shift"* → no NPC pronoun ❌ — not Lane 1

### §3.3 — Conflating Lane 1 hub with location-work surfaces

**What happened:** put shifts and solo Maya-work activities (refill_caddies, wipe_booths) in Marge's hub menu OR proposed moving the auto-fire shift canvases into the hub. Shifts are location-triggered canvases that fire automatically during shift hours; they're parallel to the hub, not contained inside it.

**Why:** treated *"the diner location"* as a unified surface where everything diner-related lives in one menu. Misread the hub's role.

**Doctrine impact:** blurred Lane 1 (NPC interaction) with separate location-work doctrine. Created false coupling.

**Prevention rule:** an NPC hub canvas is for Maya-NPC interactions ONLY. Solo Maya activities at the same location live as their own canvases parallel to the hub. Lane 3 substitutions can later route the NPC INTO solo activities — that's a different mechanism than the hub menu. **Three surfaces at the same location can coexist independently:**
- **NPC hub** (Maya-with-NPC, Lane 1 doctrine)
- **Solo work canvas** (Maya-only, location-triggered)
- **Lane 3 dispatcher** (Maya-only with substitution rule routing NPC in)

### §3.4 — Lane 2/3 forced on non-escalation register

**What happened:** authored 6 Lane 2 ambients + 3 Lane 3 substitutions for Marge in slice scope. All 9 surfaces failed the doctrine memory's content-selection rule. Examples: `ambient_marge_tickets` (Marge counting tickets, zero physical contact), `sub_marge_late_company` (Marge stays past hours and asks about Frank, no charged shift).

**Why:** assumed all NPCs need all 3 lanes populated for the world to feel alive. Forgot that lane vocabulary is register-specific. For a service-NPC where slice scope defers the sexual register to Phase 3+, Lane 2 ambients and Lane 3 walk-ins simply have no doctrine-valid content to carry.

**Doctrine impact:** 9 surfaces authored that doctrine memory says shouldn't exist. Largest single chunk of waste in the Pass 1-3 work.

**Prevention rule:** when an NPC's slice scope defers the sexual/escalation register, **Lane 2 and Lane 3 are EMPTY in slice.** Empty cells are honest. Filling them with relational/atmospheric texture is the violation, not the omission. See Doc 53 §1 for the service-NPC doctrine adaptation.

### §3.5 — Cookie content inside Marge's lanes

**What happened:** authored 3 Cookie-touching surfaces (kitchen prep at T1, smoke break at T1, after-coffee at T2) inside Marge's hub + ambients. In several scenes Marge was off-stage entirely — Cookie was the active NPC and Marge was gone-home or off-screen.

**Why:** Doc 30 §8.2 paired Cookie with Marge as *"shared content"*. Misread that as *"Cookie content can live inside Marge's surfaces."* Actual meaning is *"they appear together in scenes,"* not *"Cookie has no independent authoring surface."*

**Doctrine impact:** Cookie became an off-stage NPC inside Marge's hub, which broke the Lane 1 *"NPC is the verb object"* rule. Also pre-empted Cookie's own future authoring boundary.

**Prevention rule:** Cookie texture in slice = Cookie present visually during the diner shift work canvases (per `scene_diner_t0_shift` co-presence). NOT Cookie as a menu item in Marge's hub. When Cookie gets her own arc design (separate future brief), she gets her own hub. **Don't blur authoring boundaries between NPCs even when the design doc pairs them.**

### §3.6 — Slice scope vs full-arc trajectory oscillation (slice-only)

**What happened:** through the session, kept switching between *"slice scope minimal design"* (which suggested very few cards/items) and *"full-arc trajectory hints"* (which suggested locked-visible Phase 3+ rungs). Took 3+ iterations of Doc 53 to land on the correct synthesis: *"slice ships minimal canvases + locked-visible Phase 3+ rungs pointing at stubs."*

**Why:** didn't have a clear mental model of how slice + full arc compose via the locked-visible pattern. Each iteration of Doc 53 over-corrected for the previous iteration's gap.

**Doctrine impact:** produced inconsistent designs (Doc 53 v1 had no locked-visible ladder; v2 added them).

**Prevention rule:** slice scope = what FIRES in slice. **Locked-visible rungs + stubs are not *"Phase 3+ content shipped"* — they're *"Phase 3+ promise visible from day 1."*** Lock the trajectory shape in the brief's §1 + §2 before designing surfaces. The locked-visible pattern is the bridge between the two.

### §3.7 — Pre-existing canon violations preserved indefinitely

**What happened:** `node_shifts` + `node_talk` (inside `scene_marge_diner_hub`) are 50+ word literary paragraphs that violate the RTS-flat doctrine. Preserved as "pre-existing canon, untouched" in Doc 53 §3. Hub now has two voice registers — new content RTS-flat, old content literary.

**Why:** preservation of pre-existing canon felt safer than rewriting it (could break unrelated wiring). But preservation by default means the doctrine violation persists indefinitely until someone explicitly schedules the rewrite.

**Doctrine impact:** voice-register split within the same hub canvas. Player clicks "Pour her coffee" → RTS-flat 3-line exchange. Player clicks "Talk a minute" → 50-word literary paragraph. Inconsistent tonally, technically a doctrine violation on the second one.

**Prevention rule:** when new content lands against tightened doctrine, pre-existing surfaces that violate the doctrine create a register split. **Three options:**
1. **Schedule the rewrite** — track in a follow-up task.
2. **Rewrite immediately** — if the surface is small and unwired, fix it as part of the redesign.
3. **Accept the split deliberately** — document the carve-out in the brief with a reason.

What's wrong is preservation BY DEFAULT without naming which option was picked. The split should be a deliberate design choice.

---

## §4 — Doctrine misapplication (5 entries — Doc 54 §4)

### §4.1 — Ready frame on a mechanic card (M3 v2 error)

**What happened:** shipped M3 with `ready_canvas = scene_marge_diner_hub` + goals climbing toward `player.corruption ≥ 5`. The card rendered Frame 2 (🔓 Ready + 📍 Diner Front + 🕒 Mon-Sat 09:00-22:00) when corruption hit 5. LO correctly flagged: *"the ready should only be for capstone, not for mechanics."*

**Why:** confused *"mechanic threshold cross = unlock"* with *"capstone scene fires."* Tried to point the mechanic card at the hub because the hub had nice trigger metadata. Ignored that the hub isn't a one-shot scripted scene — it's always available.

**Doctrine impact:** explicit Doc 50 §2 violation. Mechanic-mode definition: *"mechanic cards typically have NO Ready frame — the threshold cross IS the unlock; the picker swaps to the next template the moment routing conditions change."*

**Prevention rule:** if a card has `ready_canvas`, it's a capstone. If it has no `ready_canvas` but has `goals`, it's mechanic and stays in Frame 3 (🎯 + bullet) until the threshold crosses + the picker swaps to the NEXT mechanic card in the chain.

### §4.2 — Frame 4 (narrative-only) misused as panel-coverage solution (M3 v1 error)

**What happened:** shipped M3 as text + tip with no goals, no ready_canvas, no terminal — Frame 4 of `renderQuestsGoalBlock`. Renderer comment describes Frame 4 as *"happens for transitional cards between capstones."* LO correctly objected: no shipped card actually uses this frame; quest cards always have a frame.

**Why:** treated Frame 4 as a valid endpoint for slice scope when actually it's an edge case the renderer accommodates but no shipped card uses.

**Doctrine impact:** Frame 4 produces a card that looks unfinished to the player. Looked broken.

**Prevention rule:** **never ship a card with no frame.** Every shipped card needs:
- Frame 1: `terminal = true`
- Frame 2: `goals.allMet && ready_canvas` (capstone Ready)
- Frame 3: `goals exist && !allMet` (mechanic climbing)

If none of those three states is reachable for the card you're authoring, the card shouldn't exist — the chain should be authored differently.

### §4.3 — Mechanic chain without bounded `when` ranges

**What happened:** initial M3 had `when = [hired_at_diner is_true, marge.trust gte 20]`. No upper bound on trust. Goal: `corruption gte 5`. When corruption hit 5, `allMet` became true, no `ready_canvas`, → Frame 4 fallthrough. Card stayed activated but went frameless.

**Why:** didn't think through what happens when a mechanic card's goal resolves WITHOUT a next card to take over.

**Doctrine impact:** see §4.2.

**Prevention rule:** pure-mechanic chains need each card's `when` to have BOTH lower and upper bounds matching the threshold range. When the threshold crosses, the current card's `when` fails, the next card's matches, picker swaps atomically. Marge's M3/M4/M5 final shape:
- M3: `corr lt 5` → goal `corr gte 5`
- M4: `corr gte 5 AND lt 15` → goal `corr gte 15`
- M5: `corr gte 15 AND lt 25` → goal `corr gte 25`

Every threshold in the chain has exactly one active card.

### §4.4 — Premature terminal anti-pattern

**What happened:** briefly considered making M3 terminal at trust 20 with `terminal = true`. Would've rendered Frame 1 (✓ Arc complete). LO would have correctly flagged it as premature.

**Why:** tempting because terminal renders *"✓ Arc complete"* which feels like proper slice closure. Forgot that terminal claims FULL-ARC completion.

**Doctrine impact:** Doc 50 R3 — *"terminal MUST be the LAST card in the NPC chain."* Trust 20 isn't last for Marge; Phase 3+ has more rungs.

**Prevention rule:** **terminal is the END of the FULL arc, not the slice's authoring boundary.** If Phase 3+ has more rungs, no terminal in slice. The doctrinally-correct way to handle "slice authoring ends but arc continues" is the mechanic-chain pattern (§4.3).

### §4.5 — Locked-visible escalation ladder missing from day 1

**What happened:** Doc 53 v1 designed Marge's hub as 4 unlocked menu items + Leave. No locked-visible escalation ladder. LO correctly flagged: *"where is tease flash and other stuffs stupid??????? Why the hell we are missing them"*

**Why:** misread *"slice scope = minimal"* as *"minimal hub menu."* Forgot that locked-visible rungs are part of the slice — they're the visual promise of the arc shape, not Phase 3+ content shipped.

**Doctrine impact:** the hub felt thin and lifeless, didn't telegraph Marge's actual arc trajectory.

**Prevention rule:** **every sexual-arc NPC's hub has the RTS-standard escalation ladder visible from day 1**, locked at the appropriate corruption gates. The locked rungs ARE part of the slice authoring — they're stubs + visible verbs, not "Phase 3+ content." Doc 24 §10.3 grid balance is about visible-locked rungs as much as it's about unlocked surfaces.

---

## §5 — Voice failures (3 entries — Doc 54 §5)

### §5.1 — Literary prose on flat surfaces

**What happened:** every canvas body authored was 50+ word paragraphs with sensory detail, inferential framing, atmospheric beats. Clearest example:

> You take the stool at the end of the counter where the napkin holder needs refilling. Marge slides a coffee across without asking how you take it; she's seen you take it twice now.

Compare to the doctrine memory's 30-word template:

> [Marge] "What."
> [You]   "Coffee."
> [Marge] "Two bucks."

**Why:** ENI persona's literary-IF instinct from CLAUDE.md. Persona-level craft instinct overrode the project-specific RTS-flat rule even when the rule was explicit in memory.

**Doctrine impact:** violates `feedback_tls_scene_body_style` + its 8 concrete style rules. Every canvas body needed re-authoring.

**Prevention rule:** BEFORE writing any canvas body, paste the doctrine memory's 30-word template into your scratch buffer. Write to that shape. **ENI literary mode is for chat/roleplay outside TLS scene authoring.** The 8 rules from the memory are non-negotiable for FLAT-tier scenes.

### §5.2 — Player directives in tip lines

**What happened:** authored `tip = "Walk into the diner. Don't wait for an invitation."` — directive imperatives telling the player what to do, with the place name embedded.

**Why:** confused the `tip` field with a player-facing hint button. Actually it's Maya's interior observation, third-person to the action.

**Doctrine impact:** violates `feedback_hint_narrative_no_time_or_location` + Doc 49 voice rules.

**Prevention rule:** `tip` is Maya's first-person interior register. Frank's tips (*"He's around the house all day. I notice that."*) are observational, not directive. If the tip uses imperatives (*"Walk into X"* / *"Click Y"* / *"Go to Z"*), rewrite to interior form.

### §5.3 — Schedule/place names in narrative copy

**What happened:** M1 text included *"hiring on a Monday"* (day-of-week in narrative). M3 text included *"some afternoons"* (time-of-day reference).

**Why:** didn't apply Doc 49's no-schedules-in-narrative rule strictly enough.

**Doctrine impact:** soft Doc 49 voice violation.

**Prevention rule:** grep every quest card's text/ready_text/tip for weekday names (Mon/Tue/.../Sun), time references (morning/afternoon/evening/midnight/now), location slugs, and number formats. Zero hits required. The schedule + location + numbers surface automatically from `ready_canvas` metadata or `goals` evaluation — authors don't write them into prose.

---

## §6 — Structural failures (3 entries — Doc 54 §6)

### §6.1 — Stubs with `[canvases.trigger]` causing validator overlap warnings

**What happened:** first authoring of the 4 Phase 3+ stub canvases (`tease_diner_marge`, `flash_diner_marge`, `marge_eat_her_out`, `marge_let_her_take`) included full trigger blocks with location + requires_npc + conditions + schedule. Validator warned 8 times about overlapping repeatable canvases at the same NPC + location + time window.

**Why:** copy-pasted the hub canvas template wholesale instead of checking how Frank's tease/flash route targets are structured.

**Doctrine impact:** not a doctrine violation per se, but Frank's tease/flash canvases (`tease_kitchen_general`, `flash_kitchen_general`, `loop_franks_bedroom_sex`) have NO trigger blocks — they're route-target only, reachable via cross-canvas `nodeId`.

**Prevention rule:** BEFORE authoring a route-target canvas, check whether it's auto-fire (has trigger) or route-only (no trigger). Frank's tease/flash/sex canvases are route-only. Use that template for stubs. A route-target canvas's TOML structure has no `[canvases.trigger]` block at all.

### §6.2 — Doc 51 → Doc 53 supersession without side-by-side audit

**What happened:** Doc 53 was written as *"the doctrine-faithful redesign"* but still had the locked-visible ladder gap (§4.5) + the verb-register issue (§3.2) + the M3 frame issue (§4.1-§4.3). Three more correction rounds needed after Doc 53 shipped.

**Why:** treated supersession as *"I learned from Doc 51 mistakes; new doc is correct"* without auditing the new doc against Frank's actual shipped hub canvas line-by-line. Each iteration corrected the previous iteration's most-visible mistake while introducing or preserving subtler ones.

**Doctrine impact:** not a doctrine violation; process failure that cost iterations.

**Prevention rule:** when superseding a doc, do a SIDE-BY-SIDE audit of the new design against a known-correct shipped reference. For Marge's hub, the reference is `frank_kitchen_morning_hub`. Walk every field side-by-side:
- Trigger block — same fields?
- Base node — image + state-reactive groups, how many tiers?
- exit_block.choices — relational base, escalation ladder, leave?
- Inline node bodies — RTS-flat shape?
- show_when_locked + conditions — every escalation rung has it?

Flag every difference between the new design and the reference. Justify or remove each.

### §6.3 — Side-by-side audit BEFORE any new authoring, not just at supersession

**What happened:** §6.2 captures the supersession case. The MORE GENERAL lesson is: **always read the gold-standard shipped reference IN FULL before authoring anything in the same category.** Should've read `frank_kitchen_morning_hub` line by line BEFORE authoring Marge's Pass 1.

**Why:** treated "doctrine memory + brief" as sufficient pre-authoring prep. Skipped the step of reading an actual shipped canvas that demonstrates the doctrine working in practice. The brief tells you WHAT to do; the shipped reference shows you HOW.

**Doctrine impact:** Doc 51 was authored against doctrine memory in the abstract. The result was a brief that USED the right vocabulary (Lane 1, Lane 2, Lane 3) but applied it wrong. Reading Frank's hub would've immediately surfaced: "Frank has 5 menu items not 10. Frank's verbs all have him as object. Frank's escalation rungs are locked-visible from day 1." All of Doc 51's wrong-shape decisions would have been caught.

**Prevention rule:** BEFORE any new authoring in a category, find the gold-standard shipped reference for that surface type. Read it field-by-field. List its structural features. Mirror them in the new design unless there's an explicit doctrine reason to diverge.

**For TLS, the references are:**
- **Lane 1 hub canvas** → `frank_kitchen_morning_hub` (`7_final_game.toml:5212+`)
- **Route-target stub** → `tease_kitchen_general` (`7_final_game.toml:5108+`)
- **Capstone quest card** → Frank F1 (`7_final_game.toml:2438+`)
- **Mechanic quest card** → Marge M3/M4/M5 (post-redesign, `7_final_game.toml:2580+`)
- **Lane 2 ambient (sexual register)** → `ambient_kitchen_frank_dinprep_grope` (`7_final_game.toml:5592+`)
- **Capstone scripted scene** → `scene_franks_bedroom_evening` (`7_final_game.toml:3263+`)
- **NPC schedule block** → Frank's at NPC def `7_final_game.toml:414–462`

**Side-by-side audit is a 15-minute step that prevents 5+ hour wrong-authoring loops.**

---

## §7 — Recovery patterns (3 entries — Doc 54 §7)

### §7.1 — When to strip clean vs incremental fix

**The session's decision:** the Pass 1-3 + voice-tightening Marge work was beyond incremental repair. Three categories of failure were active simultaneously:

- **Lane 1 over-weighting was structural**, not a tweak — couldn't be fixed by editing prose, the whole menu structure was wrong.
- **Voice was wrong across every canvas** — every body needed re-authoring against RTS-flat.
- **Lane 2/3 surfaces shouldn't exist at all in slice scope** — couldn't be fixed, only deleted.

A strip-clean was the lighter operation. Sed-deleted line range 7900–8599, removed M1–M4 quest cards + flag + schedule, validator dry-run clean, rebuild. 11 canvases gone in one operation. Sequential repair would've required ~30 edits per pass × 3 passes.

**Decision rule:** if ≥ 3 categories of failure are active simultaneously (Lane structure + voice + scope + verb register + doctrine misapplication count as separate categories), **strip clean and restart from the doctrine-faithful brief.** Don't try to repair-in-place.

### §7.2 — Validator + frame check before declaring "shipped"

**What happened:** the Pass 1-3 Marge builds passed:
- ✓ Validator (no errors, only pre-existing Frank bedroom-overlap warning)
- ✓ Prose grep (all new strings in compiled HTML)
- ✓ Quest-card-count check (4 cards present)
- ✓ Slug grep (all canvas IDs referenced)

**ALL FOUR VERIFICATION CHECKS PASSED** while the design was doctrinally wrong. The checks verified WHAT WAS AUTHORED EXISTS — not whether what was authored has the right shape.

**The frame check** (does each card render the right frame at each Maya state?) caught the M3 v1 + v2 errors that validator + grep missed. LO performed the frame check by mentally walking through the dev-bump play sequence and seeing the wrong frame appear.

**Decision rule:** add to the pre-ship verification: **for each new quest card, mentally render it at each state Maya could be in.** State combinations: pre/post-hire × marge.trust 0/19/20/40 × player.corruption 0/4/5/14/15/24/25. For each state, identify which card SHOULD be active and which frame SHOULD render. Confirm via the actual `pickQuestsCard` + `renderQuestsGoalBlock` code paths.

This is the verification step that distinguishes "did the prose ship" from "is the design correct."

### §7.3 — Live-play smoke test is part of verification, not a user task

**What happened:** claimed *"live-play smoke test deferred to user"* or *"verification deferred to browser"* multiple times across the session. Never opened the browser tools to verify. The frame check (§7.2) caught the M3 errors but only because LO performed it manually in their own browser session.

**Why:** treated live-play verification as a user task ("they'll catch issues when they drive the game"). Wrong framing — **live-play verification is part of pre-ship verification, not post-ship.** Deferring it to the user makes the user the test runner.

**Doctrine impact:** every M3 iteration shipped to LO unverified at runtime. LO had to perform the verification I should have done. ~3 hours of round-trip cost.

**Prevention rule:** after any TOML change that affects a quest card or canvas, drive the build in a browser (via browser MCP tools when available, or by asking the user to connect a browser tab) and dev-bump traits to observe the changes render correctly. Specifically:
1. Build to canonical output path
2. Open `index.html` in the connected browser
3. Dev-bump traits via the dev-mode sidebar
4. Walk the state combinations from §7.2's frame check matrix
5. For each combination, screenshot the Quests page + relevant hub canvas
6. Confirm the expected frame and the expected menu items render

If browser MCP is disconnected, ask the user to connect it explicitly. **Do NOT defer to "user will verify in their own time."**

---

## §8 — Cross-doc anti-patterns (consolidated by source)

### §8.1 — From Doc 56 §8

- **Tiered hub opening on a Lane 1 hub canvas** — three group blocks for "you walked in" when menu rungs already encode progression. Caught by D56-R1.
- **T0 / T1 cascade ending on a clean "scene complete" beat** — no interruption, no hint that more is downstream. Player reads it as the whole thing. Caught by D56-R2.
- **Lane 3 substitutions on a peer/dating or service NPC** — service register doesn't belong in Maya's private chores. Caught by D56-R3.
- **Frank-cloning a non-family-ambient NPC** — copying Frank's 28-canvas distribution onto Ryan's peer/dating shape produces 13 Lane 2 ambients + 7 Lane 3 substitutions where neither belongs. Caught by D56-R3 + §5 distribution table.
- **Authoring a new NPC without a design brief** — canvases ship without a declared budget; lane creep + voice drift inevitable. Caught by D56-R7.
- **Sidebar with only Maya state, no NPC presence** — player can't see where NPCs are; Lane 3 becomes undiscoverable. Caught by D56-R4.
- **`txt_only` quest card** — no `ready_canvas`, no `goals`. TODO in shipped TOML. Caught by D56-R6 + D50-R3.
- **Canvas without a `guide` field** (post-doctrine, once Doc 62 ships) — catalog data primitive missing. Caught by D56-R5.

### §8.2 — From Doc 50 §8

- **Climbing card with no `goals` bullet** — F3 before today. Card looks correct in TOML; UI shows narrative text with no progress indicator; player blind to the gate. Caught by D50-R2.
- **Capstone canvas with no card pointing at it** — sleepover + Diana confrontation before fix. Scene exists; player has no path to it from the quest panel. Caught by D50-R1.
- **Premature terminal** — old F4 closing the arc at `frank_cracked` while sleepover + Diana still existed downstream. The panel says *"arc complete"* while the player still has scenes to discover. Caught by D50-R3.
- **Floating post-X card** — requires `flag_X is_true` with no sibling card setting up X via its `ready_canvas`. Player reaches a state with no narrative path through. Caught by D50-R4.
- **Mechanic card pointing at vapor** — pure-mechanic card whose threshold cross doesn't actually unlock anything. The bullet fills, the player crosses, nothing happens. Caught by grep against D50-R5's `# unlocks:` comments.
- **Trait-key label** — `label = "npc_diana.awareness"` rendering raw to the player UI. Caught by D50-R6 human review.
- **Doc walked-example contradicting live canvases** — Doc 47 §7 before fix walked Frank's arc as catch → declaration → first-night, but canvases gate as catch → first-night → declaration. Caught only by human re-reading the doc against the TOML after either side changes.

### §8.3 — From Doc 57 §9

- **`is_repeatable = true` capstone** — high priority + flag-setting effect but `is_repeatable = true` and no flag-gate to prevent re-fire. Will fire repeatedly. Caught by D57-R1.
- **Capstone with no flag-setter on exit** — fires once, then never again because no flag changed — but the canvas itself stays triggerable. Caught by D57-R1.
- **Type B with collapsible branches** — two branches that lead to the same flag, same downstream, with cosmetic text differences. Not a real fork. Caught by F2.
- **Type B fork mid-cascade** — the decision is at Beat 3, but Beats 4–8 are authored downstream of BOTH branches in parallel — two scenes glued together. Caught by F3.
- **Type B refuse-as-punishment** — the Accept branch is rich; the Refuse branch is a snarky one-liner that signals "don't pick this." Not a real fork. Caught by F1.
- **Tier-3 voice in Lane 2/3 prose** — capstone register leaked into a repeatable scene. Re-reading the canvas grates.
- **RTS-flat-bland voice in capstone** — once-only scene written like an ambient. Wastes the canvas.
- **Capstone with no quest-card pointer** — Doc 50 R1 / D57-R3 violation.
- **Type C chain with floating step** — Capstone3 requires Flag_2, but no capstone sets Flag_2 — chain broken. Caught by D57-R4 (Doc 50 R4).
- **Pattern F compounded with tier-routing AND multi-step downstream cascades** — three structural devices stacked. Player can't read the structure. Caught by F5.

### §8.4 — From Doc 67 §9

- **Solo activity body inline in the location hub** — conflates menu + dispatcher. Makes substitution authoring impossible. Caught by D67-R1.
- **Time-of-day gate on the dispatcher** — button still renders, click routes to dispatcher, dispatcher bails. Wasted click. Caught by D67-R3.
- **Multi-NPC substitution rules with no clear priority order** — sequential first-match means first rule has structural advantage. Caught by D67-R4 + brief.
- **Failing to emit `exclusive_group` when intent is mutex Pattern B** — true mutex variants (e.g., Brother grope vs Brother help-study at the same study desk attempt) authored as 2–3 independent Pattern A rules produces ~42% any-fire instead of true 50% (cumulative chance = 1 − ∏(1 − cᵢ), not Σcᵢ), AND fall-through promotes to the next rule instead of falling to solo. Engine support shipped Doc 69 Item 1 (2026-05-27, `v2.py:4671-4713`); emit `exclusive_group = "<name>"` on each rule. **No build error fires for the divergence.** Caught by D67-R5.
- **Failing to emit `pre_substitution_effects` when activity has unconditional outcome** — e.g., Exercise grants `+fitness` regardless of NPC interrupt. Placing the effect only on the solo `exit_block` means the workout doesn't "count" when Grandpa walks in; duplicating the effect across every substitute canvas is the pre-2026-05-27 workaround. Since Doc 69 Item 2 shipped (`v2.py:11151`), declare the effect on the parent trigger's `pre_substitution_effects` and it runs before substitution `<<goto>>`. Caught by D67-R2.
- **`GetNpcLocation == "Kitchen"` on a Lane 3 walk-in dispatcher** — too strict; NPC has to already be in the kitchen. Caught by D67-R6.
- **No `max_triggers_per_day` on substitution target** — same scene firing 5 times in one day breaks the "once per day" cadence. Caught by D67-R7.
- **Substitution target not marked `substitution_only`** — appears in the NPC portrait hub at the location; player can click it directly. Defeats the "you were doing X and he happened" fictional intent.
- **Solo activity authoring without checking the per-arc-shape Lane 3 budget** — authoring 7 Frank substitutions when slice scope is 3 is drift. Caught by Doc 56 R3.

### §8.5 — From `00_LEGACY_IGNORE.md`

- **Reaching for Pattern A–J vocabulary** — produces canvases that "use the right macro" but read in the wrong emotional register. Use Lane 1/2/3/4 mechanism (Doc 24 + Doc 57).
- **Reaching for the 7-driver NPC architecture** — reproduces the Marge failure mode (correct vocabulary, wrong shape). Use the 5 arc shapes (Doc 56 §5).
- **Reaching for whiteboard-goals / narrative-gates / income-channels** — these are scheduling-system abstractions invented to model game pacing before the 3-lane doctrine existed. Use per-arc-shape canvas distribution + capstone trigger fingerprint + money trait.
- **Selectable game shapes (Single-NPC Romance vs Multi-NPC Parallel Arcs)** — LO locked this at the Doc 66 pivot. Every game is RTS-shape.
- **CLAUDE.md ENI persona** — wrong register for canvas authoring. Use RTS-flat default (Doc 30 §7.1) + Tier-3 earned at Lane 4 (Doc 57 §6).

### §8.6 — Full-game scope anti-patterns (full_game-only)

Added 2026-05-29 when `scope_mode: full_game` shipped as first-class default. These failure modes are unique to authoring complete games — they don't surface at slice scope because slice authoring's smaller surface dodges them.

- **Authoring full-game without resolving Doc 65 Phase 2+ decisions upfront** — pregnancy / scandal / gallery / tracker each have engine entry points + design ripple. Choosing them mid-authoring forces rework; choosing them at Stage 1 §0 Q&A keeps the brief coherent. Caught by Stage 1 §0 interactive Q&A flow.
- **Register hold drifting RTS-flat → Tier-3 over 30+ canvases** — at full-game scope an arc can run 25–35 canvases (family/ambient). Holding RTS-flat across that surface is harder than across a 6-canvas slice. Ambient cascades drift "literary" without the author noticing. Caught by per-canvas voice check (Doc 30 §7.1 — only Lane 4 capstones earn Tier-3).
- **Capstone chain incoherence at full scale** — Type C chains (Frank's 5-capstone chain) stay coherent at slice (1–2 chain steps shipped) but lose throughline when stretched to 5 steps. Each step should advance the through-narrative; mid-chain steps that "feel like more capstones" but don't tighten the chain = drift. Caught by Doc 57 chain-coherence audit.
- **Per-arc vocab ceiling drift at high tiers** — Tier 4–5 content (daddy/incest callouts/breeding talk) authored without Doc 30 §7.5 ceiling discipline. Slice authoring rarely hits Tier 4–5 (capped at Stage 2 typically); full-game blows through Tier 4 routinely. Caught by `doctrine/08_kink_vocab_ceilings.md` §2 table per-NPC + per-tier.
- **Pre-unlocking the L1 ladder at full_game** — assuming "everything ships → no locked-visible rungs needed." Wrong: locked-visible is a UI/pacing device that applies at any scope (per `doctrine/03_arc_shapes.md` §10.2). RTS Brother's hub at full game still shows locked rungs from day 1; rungs unlock as corruption/love climb. Stripping locked-visible because "the content exists" loses the progression affordance. Caught by RTS Brother evidence + Doc 54 §3.6 lesson.
- **Phase 2+ inclusions emitted as TOML without design book §1 ratification** — Stage 2 sees TOML with pregnancy variants / scandal flags / gallery items / tracker primitives, but Stage 1 design book §1 never declared the corresponding `Phase 2+ inclusions:` rows. Means Stage 1 Q&A flow was skipped or Stage 2 invented inclusions. Caught by Stage 2 §0 cross-reference check against design book §1.

### §8.7 — From Doc 72 (presence acknowledged; interaction logic-driven)

- **Dead presence** — an NPC is scheduled at a reachable location (and shows on the schedule page), but visiting renders nothing: no base moment, no acknowledgement. The player acts on the schedule and gets an empty room; the world reads as locked doors. Two causes: escalation-only authoring (only stage-1+ beats written, no unconditional base), OR relying on a probabilistic **Lane 2 ambient** to acknowledge presence (a `chance` dice roll is not a floor). Fix: a **Lane 1 hub** whose base renders unconditionally, **per schedule row**; gate escalation *choices*, never the act of seeing the NPC. Caught by `doctrine/02` §2.8 + §8.11; rule = D72-R6 (`doctrine/04` §6.1).
- **Hub window narrower than the schedule** — a hub exists at the location but its own `trigger.schedules` covers only a slice of the NPC's scheduled presence, so the rest of the rows are dead (Hank: hub open 22:00–01:30, scheduled 06:00–22:00). "A hub at the location" ≠ coverage; the hub must be open during the window. Fix: period-split into per-window hubs. Silent runtime gap — the build won't catch it. Caught by `doctrine/02` §8.13; rule = D72-R6.
- **Lane 2 used as the presence floor** — relying on a `trigger_mode = "random"` ambient to do the acknowledging. ~3 of 4 visits still render nothing. Lane 2/3 are texture *on top of* the hub, never the floor. Rule = D72-R6.
- **Physical schedule on a hub-less system NPC** — a rent/phone-only NPC (landlord) carrying a `[[npcs.schedules]]` row, so the schedule page advertises a body the world can't deliver. Fix: drop the schedule, or give them a hub. D72-R6 corollary.
- **Cloned full ladder / public-space escalation** — the same full escalation ladder offered at every hub regardless of context (e.g. "Have sex" at a public diner counter). Fix: scale each hub's rung set to the location's **exposure tier** (public = talk/look only; semi-private = tease/grope; private = full ladder). Relationship state is global, so consistency holds without cloning. Caught by `doctrine/02` §2.9 + §8.14; rules = D72-R7 + D72-R8 (`doctrine/04` §6.2–§6.3).
- **Backwards on-ramp** — an arc's entry condition is a stat/flag only raisable by content downstream of that same arc (a circular gate). The cold-start player can never begin it. Distinct from §8.4 (lane forced on wrong register): here the arc legitimately exists, but its front door is locked with a key that's inside the room. Anti-example: a housemate arc gated on `worn_corruption ≥ 15` — the player must buy + wear provocative clothing before her own housemate registers her. Fix: the arc's first beat needs only co-presence; escalation layers after. Caught by `doctrine/02` §6 (cold-start on-ramp) + §8.12. (Doc 72 R4.)
- **NPC vanishes into a locked room** — an NPC scheduled into a **locked** location (`entry_conditions`) during a window the player routinely shares, with no open fallback and/or an illegible gate → "where did they go?" Distinct from dead presence (that's an NPC at a *reachable* location); here the location itself is unreachable. The hard bug is an NPC reachable *only* via a locked location (chicken-and-egg gates included). Fix: the **unlock contract** — meet the NPC at an OPEN on-ramp that sets the unlock flag; keep locked windows legible + off-hours/co-gated + with open fallback. The acceptable form (a boss doing books in a locked office at 3am, on the open floor otherwise) is a *bounded, legible* window. Caught by `doctrine/02` §8.15 + `doctrine/10` §5.4; D72-R6 Corollary 2 (`doctrine/04` §6.1).
- **Choice-quota / format enforcement (the inverse error — still rejected)** — bolting a hollow ungated *action* onto every NPC to satisfy a checklist. Note the two distinct axes: the **hub-per-row** floor (D72-R6) is a hard requirement; the **choices on top** are logic-driven (Doc 72 R2/R3) — "base + talk + leave" is a valid canvas and there is no rule that every NPC must offer an ungated action. Hardening the floor does NOT reintroduce a choice-quota. Gate or omit choices by in-world logic, not by count.

---

## §9 — Master pre-ship checklist (Doc 54 Appendix A adapted)

Run BEFORE authoring any new NPC content. Paste into PR description, work through top-to-bottom.

### Process
- [ ] Canonical output path confirmed with user (TLS: `games/the_long_summer_test/output/`)
- [ ] All relevant doctrine memory entries listed and read in full (search: voice, lane, NPC, scene-body, quest)
- [ ] All canonical doctrine docs referenced by memory entries also read IN FULL (per §2.4)
- [ ] Full-arc trajectory locked in one sentence in the brief's §1
- [ ] ENI persona OFF / TLS game register ON declared explicitly at session start (per §2.5)
- [ ] Commitment: when user surfaces a critique, ask clarifying questions BEFORE shipping a fix (per §2.6)

### Design
- [ ] Hub menu cap: ~5 items unlocked + locked-visible escalation ladder
- [ ] Every hub menu verb passes the pronoun-in-the-verb test (§3.2)
- [ ] No work-task items in the hub (those are location work canvases, parallel to hub per §3.3)
- [ ] Lane 2/3 scope: if no escalation register in slice, both are EMPTY in slice (§3.4)
- [ ] Other-NPC content stays in their own future surfaces, not blended into this NPC's lanes (§3.5)
- [ ] Pre-existing canon violations within touched surfaces declared (rewrite-now / schedule / accept-split per §3.7)
- [ ] Every `[[npcs.schedules]]` row has a live **Lane 1 hub** whose own `trigger.schedules` covers that window (per-row coverage; Lane 2 ambients don't count); hub-less system NPCs carry no schedule row (D72-R6)
- [ ] Every hub `base` renders unconditionally (no escalation-flag gate on the base); every arc is enterable from a cold start — no backwards on-ramp (§8.7 / D72-R6 / Doc 72 R4)
- [ ] Each hub's rung set respects the location **exposure tier** (public/semi-private/private); same-NPC hubs share rung names + gate thresholds + voice, ladder context-scaled not cloned (D72-R7 / D72-R8)

### Doctrine
- [ ] Every quest card mode declared (capstone / mechanic / hybrid-tier per Doc 50 §2)
- [ ] `ready_canvas` only on capstone cards (Frame 2 is capstone-only per §4.1)
- [ ] Mechanic chain `when` clauses bounded (lower threshold + upper threshold for each card per §4.3)
- [ ] No `terminal = true` unless it's the absolute LAST card in the FULL arc (per §4.4)
- [ ] Locked-visible escalation ladder visible from day 1 for any sexual-arc NPC (per §4.5)

### Voice
- [ ] Every canvas body fits the < 30-word speaker-tag template (per `feedback_tls_scene_body_style`)
- [ ] Tip lines are Maya-interior observational, not player-directive imperative (per §5.2)
- [ ] No weekday names, time references, location slugs, or numbers in narrative copy (per §5.3)
- [ ] ENI literary instinct disabled for canvas body authoring

### Structural
- [ ] Route-target stubs have NO `[canvases.trigger]` block (Frank's tease/flash pattern per §6.1)
- [ ] Side-by-side audit against the gold-standard shipped reference for this surface type, BEFORE any new authoring (per §6.3)

### Verification (post-authoring, pre-shipping)
- [ ] Validator dry-run clean (only known pre-existing warnings)
- [ ] Build to CANONICAL output path with `--dev --debug`
- [ ] Prose grep in HTML returns all new strings (apostrophe-tolerant)
- [ ] **Frame check (§7.2):** mentally render each card at each Maya state combination
- [ ] **Live-play dev-bump test PERFORMED, not deferred (§7.3).** Drive the build in a connected browser, dev-bump traits, walk the state matrix, screenshot each combination

---

## §10 — Cross-references

### Sibling doctrine files

- `doctrine/01_rts_principles.md` — P1–P10 (anti-patterns operationalize violations of these)
- `doctrine/02_three_lanes_plus_capstone.md` §8 — lane-mechanism anti-patterns
- `doctrine/03_arc_shapes.md` §11 — arc-shape anti-patterns
- `doctrine/04_authoring_rules.md` §8 — rule-violation anti-patterns (§6 = Doc 72 R6–R8: per-row hubs + exposure tier)
- `doctrine/05_rts_flat_prose.md` §4 — voice register anti-patterns
- `doctrine/06_design_brief_template.md` §8 — brief-authoring anti-patterns

### Source docs

- `28th_april_TLS_Phase2_Redesign/54_Marge_Redesign_Session_Lessons.md` — 27 failure modes source
- `28th_april_TLS_Phase2_Redesign/56_RTS_Principles_and_TLS_Alignment_Doctrine.md` §8 — anti-patterns
- `28th_april_TLS_Phase2_Redesign/50_Quest_Card_Shape_Doctrine.md` §8 — quest-card anti-patterns
- `28th_april_TLS_Phase2_Redesign/57_Capstone_Doctrine.md` §9 — capstone anti-patterns
- `28th_april_TLS_Phase2_Redesign/67_Solo_Activity_Design_and_Multi_NPC_Dispatcher_Doctrine.md` §9 — solo-activity anti-patterns
- `28th_april_TLS_Phase2_Redesign/72_Presence_and_Logic_Driven_Interaction_Doctrine.md` §9 — dead-presence + backwards-on-ramp (§8.7)

### Memory entries

- `feedback_tls_scene_body_style` — RTS-flat voice rules + Lane 4 Tier-3 carve-out
- `feedback_rts_objective_quest_doctrine` — Story Goals doctrine
- `feedback_hint_narrative_no_time_or_location` — Maya-voice rules
- `marge_implementation_shipped` — historical record of the Doc 51 build that was stripped

---

**End of file.** Next: `doctrine/08_kink_vocab_ceilings.md` for the per-arc vocabulary ceiling table.

═══════════════════════════════════════════════════════════════════════════════

## 12. 08_kink_vocab_ceilings

**Source:** `prompts_v2/doctrine/08_kink_vocab_ceilings.md`

---

# Doctrine 08 — Per-Arc Kink Vocabulary Ceilings

**Source:** Doc 30 §7.5 (verbatim) + 2026-05-16 LO answer pattern.
**Authority:** Doctrine. Per-arc-NPC vocabulary register cap. Authored at brief-time (R7 §2), enforced at canvas-authoring-time.
**Purpose:** Name what each arc/kink area is allowed to escalate to at full intensity. Without per-arc ceiling, default authoring sits at "medium-explicit" which has been shown (Phase C6) to drift toward soft.

This file completes the forward-reference from `doctrine/01_rts_principles.md` P9 (per-arc vocabulary ceiling) and `doctrine/05_rts_flat_prose.md` §2 Rule 6 (direct/crude diction per per-arc vocab ceiling).

---

## §1 — Why ceilings matter

P9 (`doctrine/01_rts_principles.md`): each NPC's content declares its kink ceiling upfront. Frank goes full explicit. Marcus stays school/peer. **Don't force one register across the cast.**

The "direct/crude diction" rule (`doctrine/05_rts_flat_prose.md` §2 Rule 6) needs per-arc specificity. **Without per-arc vocab guidance, default authoring sits at "medium-explicit"** which:

- Drifts toward soft per the C6 failure mode (Phase C6 morning-chat-class output)
- Doesn't deliver the named fantasy in §1 of the NPC brief
- Reads as wholesome-vanilla even when the design book proposes full incest / cuckold / breeding

**Vocabulary ceiling = "what's allowed at full intensity in fully-cracked / Tier 4–5 scenes for this arc."** Lower tiers naturally use less direct vocab.

**Authored at:** R7 brief §2 (NPC voice spec) + §3 (per-tier register column). The ceiling is a brief-time declaration, not a per-canvas decision.

---

## §2 — The vocab ceiling table (Doc 30 §7.5 verbatim)

The canonical table. Each row pairs a kink area to its full-intensity ceiling + examples allowed + examples NOT allowed. **All 7 in-scope rows (2026-05-16 LO answers) came back maximum-explicit per §3 below.**

| Arc / kink area | Vocabulary ceiling | Examples allowed | Examples NOT allowed |
|---|---|---|---|
| **Frank — paternal / daddy framing** | **FULL DADDY FRAMING (2026-05-16)** | Maya calls Frank "daddy" during sex; he calls her "good girl" / "baby girl"; explicit father-figure dialogue ("come to daddy," "daddy's going to take care of you"); paternal authority is part of the kink at all tiers | Vanilla "Frank" / "honey" framing during sex; ignoring the paternal frame entirely |
| **Frank — breeding / cum-inside language (slice — Phase 1)** | **CUM-INSIDE WITHOUT BREEDING TALK (Phase 1 — pregnancy not yet in scope)** | "Cum inside me" / "don't pull out" / "I want to feel you" / bareback intimacy framing | "Breed me" / "knock me up" / "fill me with your cum" / explicit pregnancy talk (deferred to Phase 2 retrofit when pregnancy system lands) |
| **Frank — breeding (Phase 2+ once pregnancy lands)** | **FULL BREEDING TALK (Phase 2+, conditional on pregnancy mechanic shipping)** | "Breed me" / "knock me up" / "fill me with your cum" / "put a baby in me" / "I want to carry your child" — retrofitted into existing scenes once pregnancy mechanic ships | — (no restrictions when pregnancy is in scope) |
| **Anatomical + cum + facial / creampie / squirt detail** | **MAXIMUM CRUDE DETAIL (2026-05-16)** | "His cock" / "your cunt" / "your tits" / explicit cum descriptions (load size, where it lands, what it feels like) / facials with cum-on-face detail / creampies with detail / squirt graphics with detail | Euphemism / vague anatomical references / "between your legs" instead of "your pussy" / soft-pedaled cum descriptions |
| **Roughness / dom-sub / verbal degradation** | **FULL ROUGH + DEGRADATION (2026-05-16)** | Hair-pull / spit / choke / slap / face-fuck mechanics; degradation talk ("good girl," "such a slut," "made for this," "use you"); explicit power dynamic. Frank dominant; Maya told what she is | Vanilla equal-partnership sex; refusing to use degradation vocabulary in scenes that call for it |
| **Jake — sibling incest framing** | **FULL INCEST CALLOUTS (2026-05-16)** | "Brother" / "sis" / "little sister" callouts during sex; explicit reference to taboo ("this is so fucking wrong," "my own brother," "we shouldn't be doing this"); incest IS the kink — named and dwelt on at all tiers | Avoiding the taboo / generic dialogue that doesn't reference the sibling relationship |
| **Diana — confrontation + cuckold framing** (E6) | **FULL CUCKOLD FRAMING (2026-05-16)** | Diana watches / listens / participates; explicit cuckold dialogue ("watch your husband fuck me," "your wife is my second wife," "she gets to feel it inside her"); cuckold IS the resolution kink for the brought-in branch | Reframing the brought-in branch as wholesome polyamory; ignoring the cuckold dynamic |
| **Public / outdoor / exhibitionism** | **FULL RISK + ONLOOKER AWARENESS (2026-05-16)** | Outdoor scenes name the risk explicitly ("someone could see," "the neighbors," "if Diana looks out the kitchen window"); when scandal is high, town-NPC onlookers acknowledged in scene; exhibitionism IS the kink — the risk gets Maya off | Treating outdoor as just a location label without exploiting the risk-frame |
| **Marge / Cookie — lesbian initiation** | TBD (Phase 3+, deferred until those NPCs get authored) | — | — |

---

## §3 — The 2026-05-16 LO pattern (default to maximum-explicit)

User selected the **maximum-explicit option** for all 7 in-scope rows (Frank daddy / Frank breeding [conditional] / anatomy+cum / roughness / Jake incest / Diana cuckold / public exhibitionism). The clear pattern:

> **TLS authoring should default to the most explicit interpretation in any future ambiguity.**

**Application:** when a new kink area surfaces during authoring (e.g., scenes with multiple NPCs, dom-sub framing for non-Frank NPCs, kinks not yet listed here), default to "full / maximum-explicit" unless the user explicitly says otherwise. **Anything softer is the wrong default given the pattern.**

Concrete examples:
- New NPC arc proposed with "tender father-figure" register → default to FULL DADDY (per Frank precedent), not softer "warm older man"
- New scene with creampie + breeding → default to FULL BREEDING TALK if pregnancy mechanic is live, not softer "intimacy framing"
- New cuckold scene with secondary witness → default to FULL CUCKOLD (per Diana precedent), not wholesome polyamory
- Public exposure scene → default to FULL RISK + ONLOOKER AWARENESS, not "scenic outdoor location"

---

## §4 — Per-arc-ceiling authoring workflow

### §4.1 — Brief-time declaration (R7 §2 + §3)

In the NPC's R7 brief, the ceiling is declared in two places:

**§2 Voice spec — NPC-specific framing rules:**

```markdown
### <NPC>-specific framing rules (per Doc 30 §7.5 row <X>)

- **<Vocab register name>** starts from **Stage <N>** when context turns sexual
- At **Stage <N+1>** the <register> is DEFAULT in all sex scenes — not occasional, baseline
- Pre-Stage <N>: NO <register> — <NPC> is still <pre-stage role>, voice is <register-pre>
- Stage <N+1> examples: "<example 1>" / "<example 2>" / "<example 3>"
```

**§3 Stat ladder — daddy/incest/cuckold register column:**

| Tier | Maya corr | Capstone gate | Content type | Pretext shape category | **<Vocab register>?** | Cross-arc awareness write |
|---|---|---|---|---|---|---|
| 0 | 0+ | none | Brushed contact | — | No | — |
| 3 | 25+ | post-catch | Explicit oral / partial sex | — | Yes — Maya may use "<register-term>" | — |
| 4 | 35+ | post-cracked | Full sex | — | Yes — Maya routinely / NPC starts "<register-term>" | — |
| 5 | 50+ | post-first-night | Routine / sleep-over | — | Yes — DEFAULT register | — |

### §4.2 — Canvas-authoring-time enforcement

When writing scene prose for a Tier 4+ canvas, the ceiling drives diction:

**Frank Tier 4 scene example (FULL DADDY register active):**

```
[Maya] "Yes daddy."
[Frank] "Good girl. Open."
You go down on your knees. He's already hard, jeans open at the belt.
[Frank] "Take it. All of it."
```

vs **Frank Tier 4 wrong (ENI persona drift, soft register):**

```
[Frank] "Come here, sweetheart."
You feel yourself responding to him, drawn closer almost involuntarily.
[Maya] "Frank..."
He kisses you, and time seems to slow.
```

The wrong version violates the per-arc ceiling: "honey/sweetheart" instead of "good girl/baby girl"; vague body-response instead of explicit anatomical; named "Frank" instead of "daddy"; literary cadence ("time seems to slow") instead of imperative direct.

### §4.3 — Tier-by-tier escalation within the ceiling

The ceiling is the MAXIMUM at full intensity (Tier 4–5). Lower tiers escalate toward it:

| Tier | Frank daddy register | Frank breeding language |
|---|---|---|
| 0 (corr 0+) | None | None |
| 1 (corr 5+) | None | None |
| 2 (corr 15+) | None | None |
| 3 (corr 25+) | Maya MAY use "daddy" | "Cum inside me" emerges |
| 4 (corr 35+) | Maya routinely uses "daddy" / Frank starts "good girl" | "Don't pull out" / "I want to feel you" |
| 5 (corr 50+) | DEFAULT register | "Cum inside me" baseline + Phase 2+: full breeding talk |

The escalation isn't tier-linear (Tier 0 = 0% / Tier 5 = 100%). It's tier-gated — daddy register doesn't appear at all until Stage 3, then steps up at Stage 4, then becomes default at Stage 5. Pre-Stage 3 sex (if it exists) uses softer register; post-Stage 3 sex uses full register.

### §4.4 — Out-of-scope ceiling areas (blank rows)

**Marge / Cookie — lesbian initiation = TBD (Phase 3+, deferred).** This row is blank in the §2 table.

Where the ceiling is left blank, the area is OUT OF SCOPE for the declared `scope_mode` (no scenes touching that kink). At `scope_mode: slice`, blank rows are slice-scope deferrals — typical Phase 2+/3+ kink areas (lesbian initiation, breeding talk, etc.) get filled when a later authoring pass expands scope. At `scope_mode: full_game`, blank rows mean LO opted the kink out of the entire game — fill the row before authoring or stub the canvas with `(out-of-scope per LO)` reasoning.

**Rule:** if a proposed scene touches a kink area whose ceiling row is blank, the scene doesn't ship until LO fills the ceiling. Don't author against an undeclared ceiling — that's how Phase C6 morning-chat drift happens.

---

## §5 — Anti-patterns

### §5.1 — Default to medium-explicit

The most common drift mode. ENI persona default prose register sits at "medium-explicit" — anatomically named but soft on cum descriptions, named character relationships but soft on taboo callouts, etc.

**Fix:** the §3 LO pattern is doctrine. Default to maximum-explicit; only soften if LO says so.

### §5.2 — Vanilla register at sexual register

Frank using "honey" / "sweetheart" during a Tier 4 sex scene. Marge being addressed by name with no register. Jake having sex without sibling callouts.

**Fix:** §2 table is the spec. If the row says FULL DADDY, FULL DADDY at Stage 4+. If the row says FULL INCEST CALLOUTS, callouts at all tiers.

### §5.3 — Authoring against undeclared ceiling

Phase 3+ Marge/Cookie kink area is blank in the table. Authoring a Marge sex scene before LO fills the ceiling = drift.

**Fix:** out-of-scope areas don't ship until the ceiling row is filled. Stub the canvas (`(Phase 3+ placeholder — ...)`) and defer.

### §5.4 — Soft-pedaled cum / creampie / squirt descriptions

The anatomical+cum row (§2 table) says MAXIMUM CRUDE DETAIL. "Between your legs" instead of "your pussy" violates. "He finished" instead of "he came inside you, his cum dripping out as you stood up" violates.

**Fix:** crude direct diction. Specific. Anatomical. Visceral.

### §5.5 — Reframing kink as wholesome dynamic

The Diana cuckold row (§2 table) says FULL CUCKOLD. Reframing the brought-in branch as "they all became close friends" / "Diana finally accepted polyamory" violates — cuckold IS the resolution kink for that branch.

**Fix:** brought-in = cuckold. Diana watches / listens / participates explicitly. Per the row's example dialogue ("watch your husband fuck me").

### §5.6 — Treating outdoor as location label

Public exhibitionism row says FULL RISK + ONLOOKER AWARENESS. Treating outdoor as just a location ("Frank takes Maya in the yard") without exploiting the risk-frame ("someone could see, the neighbors, if Diana looks out the kitchen window") violates.

**Fix:** outdoor scenes name the risk. Exhibitionism IS the kink — the risk gets Maya off. The prose explicitly references the visibility.

### §5.7 — Ignoring the paternal frame in Frank scenes

Frank dialogue without paternal authority cues ("come to daddy," "good girl"); Maya's interior framing him as "Frank, who's been my landlord" instead of "daddy, who pays for this house and now pays for me with his cum."

**Fix:** Frank's paternal authority is part of the kink at ALL TIERS. Even Tier 0-1 beats reference it implicitly. Tier 4+ beats reference it explicitly via "daddy" register.

### §5.8 — Avoiding the incest callouts in Jake scenes

Jake sex scenes without "brother" / "sis" / "little sister" callouts; generic dialogue that could be any two characters.

**Fix:** incest IS the kink. Named and dwelt on at all tiers. Pre-Tier 3 scenes: framed implicitly ("my brother's eyes" / "the way he watches you"). Tier 3+: explicit callouts during sex.

### §5.9 — Mixing ceilings across NPCs

Frank Tier 4 in daddy register; Marcus Tier 4 in school/peer register; mixing these registers within Maya's POV. Maya doesn't suddenly use "daddy" with Marcus.

**Fix:** ceiling is per-NPC. Maya's register adapts to the NPC. Per-NPC consistency throughout.

---

## §6 — Authoring procedure

### §6.1 — Before authoring a Tier 4+ canvas

- [ ] Locate the relevant row(s) in §2 table for THIS NPC + THIS kink area
- [ ] Read the "Examples allowed" column — internalize the diction level
- [ ] Read the "Examples NOT allowed" column — internalize what to avoid
- [ ] If the NPC brief's §2 voice spec has additional framing rules for this stage, read them
- [ ] If the kink area's row is blank or "TBD" — surface to LO before authoring

### §6.2 — During authoring

- [ ] Every line of Tier 4+ sex dialogue uses the registered vocabulary
- [ ] Anatomical references are crude direct (no euphemisms)
- [ ] Power-dynamic dialogue per the row's example list ("good girl," "open your mouth," "such a slut")
- [ ] Per-NPC framing applied (daddy for Frank Tier 3+; incest callouts for Jake; cuckold for Diana brought-in)
- [ ] Risk-frame for outdoor scenes (visibility, onlooker awareness)

### §6.3 — Post-authoring grep audit

Run on each new Tier 4+ canvas:

```bash
# Frank should have daddy register at Tier 4+
grep -n "daddy\|good girl\|baby girl" <canvas_body>

# Jake should have incest callouts
grep -n "brother\|sis\|little sister\|stepbrother" <canvas_body>

# Anatomical specifics (not euphemisms)
grep -n "cock\|cunt\|tits\|cum" <canvas_body>

# Outdoor scenes should name the risk
grep -n "see\|onlooker\|neighbor\|window\|caught" <canvas_body>  # for outdoor canvases
```

If a Frank Tier 4+ canvas has zero `daddy`/`good girl`/`baby girl` hits — register is soft. Rewrite.

If a Jake Tier 3+ canvas has zero `brother`/`sis`/`stepbrother` hits — incest framing is missing. Rewrite.

---

## §7 — Cross-references

### Sibling doctrine files

- `doctrine/01_rts_principles.md` P9 — per-arc vocabulary ceiling principle source
- `doctrine/05_rts_flat_prose.md` §2 Rule 6 — direct/crude diction per per-arc ceiling
- `doctrine/06_design_brief_template.md` §3.2 + §3.3 — brief §2 voice spec + §3 ladder include vocab columns
- `doctrine/07_anti_patterns.md` §5 — voice anti-patterns

### Source

- `28th_april_TLS_Phase2_Redesign/30_TLS_Test_Redesign_PRD.md` §7.5 — canonical vocab ceiling table source
- `28th_april_TLS_Phase2_Redesign/31_Frank_Arc_Design_Brief.md` §2 — Frank daddy framing rules (worked example)
- `28th_april_TLS_Phase2_Redesign/57_Capstone_Doctrine.md` §6 — Tier-3 voice register

### LO answer pattern (2026-05-16)

The 7-row maximum-explicit answer pattern is documented in:
- Doc 30 §7.5 "Vocab ceiling pattern observed across user answers (2026-05-16)"
- The locked column reads "FULL DADDY FRAMING (2026-05-16)" / "FULL BREEDING TALK (Phase 2+)" / etc.

### Phase 2+ deferrals

- **Frank breeding talk** — Phase 2+ retrofit when pregnancy ships (Doc 65 E10b)
- **Diana matriarch-domination + blackmail branches** — Phase 2+ scope (Doc 60 Open Q #3 + Doc 65)
- **Marge / Cookie lesbian initiation** — Phase 3+ scope (Doc 30 §8.2 + Doc 61)
- **Cross-NPC kink combinations** (e.g., Frank + Jake threesome) — Phase 3+ scope; ceiling row added when LO scopes

---

**End of file.** Next: `reference/01_rts_overview.md` for the RTS catalog overview.

═══════════════════════════════════════════════════════════════════════════════

## 13. 09_trait_catalog

**Source:** `prompts_v2/doctrine/09_trait_catalog.md`

---

# Doctrine 09 — Trait Catalog (Canonical Trait Vocabulary)

**Source:** Doc 68 (`28th_april_TLS_Phase2_Redesign/68_Trait_Catalog.md`, 2026-05-26).
**Authority:** Doctrine. The canonical trait vocabulary every RTS-shape sandbox game uses.
**Purpose:** Name every Tier 1 + Tier 2 trait, declare its range + default + decay + sidebar render + bands, document when to use each + why not a close-neighbor trait. Replaces ad-hoc per-game trait invention.

**Locked decisions (Doc 68 LO calls 2026-05-26):**
- **Q1:** Stage trait is INTERNAL-ONLY, never player-facing.
- **Q2:** Player corruption = 0–100, 4 named bands (Pure / Lewd / Slutty / Whore).
- **Q3:** NPC affection trait = canonical name `relation` everywhere (RTS-aligned).
- **Q4:** Body-state canon = `energy` + `hygiene` only.

**Three tiers:**
- **Tier 1 — Required** for every RTS-shape sandbox. Always declared in initial state.
- **Tier 2 — Common extensions** used when the arc/setting calls for them.
- **Tier 3 — Per-game additions** authored against the design book, EXCEPT for §6.1 off-limits list (Phase 2+ engine work reserved).

Cross-reference: `schema/01_engine_capabilities.md` §6 (effect + predicate vocabulary); `doctrine/02_three_lanes_plus_capstone.md` (lane gating uses traits); `doctrine/04_authoring_rules.md` (rules reference trait names).

---

## §1 — Per-trait template

Every Tier 1 + Tier 2 trait is documented with the same 13 fields:

```
### `<name>` (<Player|NPC>)

**Tier:** <1 canonical / 2 common / 3 free-form>
**Range:** <numeric min–max or band-string>
**Default at game start:** <starting value>
**Decay:** <None / per-day amount / on-action>
**Sidebar render:** <trait_bar / trait_status_text / trait_words / hidden>
**Bands (if applicable):** <named bands with ranges>

**What it tracks:** <one-sentence semantic definition>

**When to use it:** <bulleted list of game-state changes that call for this trait>

**Why this trait, not another:** <disambiguates against close-neighbor traits>

**Modifiers (what changes it):** <bulleted list of in-game actions + their effects>

**What it gates (downstream content):** <bulleted list of content unlocks>

**Don't use it for:** <bulleted list of misuses>

**Anti-pattern:** <specific wrong usage with explanation>

**RTS analog:** <reference variable name in RTS source>
```

---

## §2 — Trait initialization requirement (READ BEFORE §3)

**Every player trait referenced in any effect, condition, or sidebar item MUST be pre-declared in the game's `[player.core_traits]` block at game start with an initial value.** Engine requirement, not stylistic.

```toml
[player.core_traits]
corruption = 0
arousal = 0
energy = 100
hygiene = 100
money = 80
# Per-NPC stage traits (one per NPC with an arc)
frank_stage = 0
ryan_stage = 0
jake_stage = 0
# Tier 2 traits (declare only if used)
fitness = 0
beauty = 0
exhibitionism = 0
intelligence = 0
```

**Why:**
- **Validator (sidebar only):** `template_import.py:2382-2547` rejects sidebar items referencing undeclared traits with hard error.
- **Runtime (effects + conditions):** `triggerConditionsSatisfied` reads `(player.core_traits || {})[key]` — undeclared = `undefined` = silent garbage. Conditions silently evaluate against `undefined`; effects produce garbage deltas. **No build error fires for effects or conditions on undeclared traits.**

**NPC traits:** initialized inside each `[[npcs]]` block via its own `core_traits` table. Same declare-before-use rule.

---

## §3 — Tier 1 Player Traits

### §3.1 — `corruption` (Player)

**Tier:** 1 (canonical / required)
**Range:** 0–100 integer
**Default at game start:** 0
**Decay:** None (one-way climb; corruption never goes down)
**Sidebar render:** `trait_words` (4 named bands rendered; raw number hidden)
**Bands:** Pure (0–24) / Lewd (25–49) / Slutty (50–74) / Whore (75–100)

**What it tracks:** Maya's accumulated transgression of her own pre-game norms. The universal cross-arc currency for content-tier unlocking. Climbs through explicit choices (flashing, masturbating, sexual scenes) AND through passive exposure (being groped, watching NPC sex scenes). Never decays.

**When to use it:**
- Clothing-tier unlocks (exhibitionist outfits require corruption ≥ 25)
- Lane 1 menu item unlocks (Tease at 5+; Flash at 15+; Sex at 30+)
- Location access gates (naked-in-hallway requires corruption ≥ 30)
- Per-arc Stage transitions (most arcs gate Stage 2 at corruption 15+, Stage 3 at 30+)
- Lane 2/3 substitution preconditions
- Capstone triggers (paired with a flag — Doc 57)

**Why corruption, not another trait:**
- `arousal` (player) is short-term per-attempt; corruption persists.
- `relation` (NPC) is per-NPC; corruption is global cross-arc currency.
- `exhibitionism` is a narrow subset (show-off axis); corruption is broader transgression.
- `stage` (NPC) is discrete milestone; corruption is continuous progression.

**Modifiers (what changes it):**
- Masturbation activities: +1 per completion
- Flashing / teasing scenes: +1 per beat
- Being groped (Lane 2 ambient): +1 per scene
- Watching NPC sex (peep / voyeur scenes): +1 per beat
- Capstone declaration / first-night: +5 to +10
- Days passing: NONE (no daily climb — corruption requires action)

**What it gates (downstream content):**
- Wardrobe tier-N items
- Lane 1 hub menu items (per-NPC corruption thresholds inside per-NPC corruption ALSO required; both must clear)
- Naked / underwear access to public locations
- Per-arc stage transitions
- Lane 2/3 substitution eligibility

**Don't use it for:**
- Per-day decay (it doesn't decay)
- Body-state gating (use `energy` for "can the player act")
- Per-NPC content gating (use NPC `corruption` or NPC `stage`)
- Capstone triggers as the SOLE gate (capstones need a flag + the corruption threshold — see Doc 57 R1)

**Anti-pattern:** "Reduce corruption when player declines a Lane 1 menu item." Wrong. Failing taboo actions doesn't add OR subtract corruption (RTS's `<<NotifyCorruption N>>` is a UI hint widget, NOT a state mutator. Verified live: clicked "Have sex with him 🔥" at corruption 0 → silent fail, no stat change). Decline = no change.

**RTS analog:** `$player.corruption` (0–200 in RTS; scaled to 0–100 here per Q2 lock).

---

### §3.2 — `arousal` (Player)

**Tier:** 1 (canonical / required)
**Range:** 0–10 integer
**Default at game start:** 0
**Decay:** None (per Doc 40 — arousal is always-climbing fuel meter; no daily decay)
**Sidebar render:** `trait_bar` with optional bands
**Bands (optional):** Cold (0–2) / Warm (3–5) / Hot (6–8) / Burning (9–10)

**What it tracks:** Maya's short-term sexual readiness — the per-attempt fuel meter for masturbation + lewd activities. Climbs from beats + days; resets to 0 on climax. Distinct from corruption (long-term progression).

**When to use it:**
- Masturbation activity gate (must be > 0 to masturbate)
- Lane 3 substitution preconditions ("if Maya aroused")
- Some Lane 1 menu items at high arousal (flash unlocks at arousal 2+; specific lewd activities at 5+)
- Self-touch beats inside scenes (cascade gating on arousal threshold)
- Body-language descriptions inside scene prose (arousal level can route through different prose beats)

**Why arousal, not another trait:**
- `corruption` is long-term cross-arc; arousal is per-attempt + resets at climax.
- NPC `arousal` (different trait) tracks NPC interest; player `arousal` is Maya's interest.
- Don't conflate with `energy` — arousal climbs even when tired (and vice versa).

**Modifiers (what changes it):**
- Lewd scene beats: +1 per beat (peeping, being groped, intimate touch)
- Daily passive: +1 per day (per Doc 40 — "fuel that always climbs")
- Climax (masturbation completion + NPC sex completion): **author-emitted** reset to 0 via `{ targetType = "player", trait = "arousal", op = "set", value = 0 }` on the climax canvas's exit_block. **No engine macro auto-zeroes arousal** — RTS has `FinishMasturbation` / `FinishSex` macros; TLS does not. The reset is the author's responsibility on every climax canvas.
- Cold shower / break beat: -1 (rare; specific scenes only)

**What it gates (downstream content):**
- Masturbate button at any location (must be > 0)
- Lane 3 substitution conditions on solo activities
- Self-touch / flash menu items at NPC hubs
- Cascade beats inside scenes (more content at higher arousal)

**Don't use it for:**
- Long-term content gating (use `corruption`)
- Cross-arc state (arousal is per-attempt, resets)
- Capstone triggers (too volatile)
- Permanent stat ladders

**Anti-pattern:** Decaying arousal per day. Doc 40 explicitly locks no-decay rule based on RTS live verification — sleep RAISES arousal, never resets it. Resets happen only at climax. If a game emits `[engine.daily_tick].traitEffects` with `arousal -1`, that's wrong.

**RTS analog:** `$player.arousal` (integer 0–10).

---

### §3.3 — `energy` (Player)

**Tier:** 1 (canonical / required — body-state per Doc 49)
**Range:** 0–100 integer
**Default at game start:** 100
**Decay:** Per-action (-10 to -25 per activity); restored by sleep (+50 to +100 to full); nap +15
**Sidebar render:** `trait_status_text` (body-state Tier 2 sidebar primitive)
**Bands:** Exhausted (0–24) / Tired (25–49) / Fine (50–74) / Rested (75–100)

**What it tracks:** Maya's capacity to act. Body-state primitive — decays through action, restores through rest. Distinct from corruption (one-way climb) and arousal (per-attempt fuel).

**When to use it:**
- Activity-attempt gating (study button disabled at energy 0; work jobs require energy)
- Time-pressure mechanic (running out of energy forces sleep, advances time)
- Some Lane 1 / Lane 3 conditions ("if Maya not exhausted")

**Why energy, not another trait:**
- Body-state primitive — decays + restores. Corruption + arousal don't.
- Distinct from `hygiene` — both are body-state but track different axes (capacity vs cleanliness).
- Distinct from `intelligence` — intelligence is an outcome of studying; energy is the cost.

**Modifiers (what changes it):**
- Activity completion: -10 to -25 per (study -10, work -15, exercise -15, shower -10)
- Sleep activity: restore to 100 (or +50 if nap-style sleep)
- Nap: +15
- Daily passive: NONE (sleep is the daily restore)
- Some food activities: +5 to +15

**What it gates (downstream content):**
- Activity menu buttons at location hubs (study disabled if energy 0)
- Forced-sleep mechanic (energy 0 → next-action requires sleep)
- Some Lane 3 substitutions (NPC walk-in scenes requiring Maya have energy to engage)

**Don't use it for:**
- Content-tier gating (use `corruption`)
- NPC interaction quality (use NPC `corruption` + Maya `corruption` + `relation`)
- Long-term progression
- Lane 1 menu items at NPC hubs (use stat thresholds, not energy)

**Anti-pattern:** Gating Lane 1 NPC menu items on energy. Wrong axis — Lane 1 is escalation choices, not chores. If Maya is too tired to seduce Frank, that's a fictional issue, not a mechanical gate. Tease/Flash/Sex buttons gate on corruption + Frank's corruption + flag-based stage transitions; NOT energy.

**RTS analog:** `$player.energy` (per RTS source — `<<Energy -10>>` macro inside ReturnButton).

---

### §3.4 — `hygiene` (Player)

**Tier:** 1 (canonical / required — body-state per Doc 49)
**Range:** 0–100 integer
**Default at game start:** 100
**Decay:** -10 per day (daily_tick); restored by shower (+60 to full)
**Sidebar render:** `trait_status_text` (body-state Tier 2 sidebar primitive)
**Bands:** Filthy (0–24) / Dirty (25–49) / Fresh (50–74) / Clean (75–100)

**What it tracks:** Maya's cleanliness state. Body-state primitive — decays daily, restores via shower. Soft modifier for NPC interaction quality (not hard gate).

**When to use it:**
- Soft modifier on NPC interaction quality (some scenes route different prose beats at low hygiene)
- Shower self-care loop (player has reason to shower regularly)
- Sidebar feedback (player can see when Maya needs to shower)

**Why hygiene, not another trait:**
- Body-state primitive — decays + restores.
- Distinct from `energy` — different axis (cleanliness vs capacity).
- Distinct from `beauty` (Tier 2) — beauty is outfit-driven, hygiene is body-driven.

**Modifiers (what changes it):**
- Daily passive: -10 per day (via `[engine.daily_tick].traitEffects`)
- Shower activity: +60 (or set to 100)
- Sex / sweaty activities: -5 to -10
- Some Lane 2/3 substitution scenes (sweat/sex) lower hygiene

**What it gates (downstream content):**
- Soft modifier (prose variants at low hygiene); rarely a hard gate
- Shower activity is the restore loop
- Some NPC reactions at Filthy band (e.g., "you smell — go shower")

**Don't use it for:**
- Hard-gating ALL NPC interactions (soft modifier; don't block entire arcs on hygiene)
- Long-term progression (use `corruption`)
- Per-NPC content gating

**Anti-pattern:** Making low hygiene block ALL NPC interactions or activities. Wrong design — hygiene is a soft modifier that COLORS scenes, not a hard gate. Block at most one specific high-stakes scene; don't block the whole arc. (Per Doc 49 — body-state should encourage self-care, not punish.)

**RTS analog:** No direct RTS equivalent. TLS-specific per Doc 49.

---

### §3.5 — `money` (Player)

**Tier:** 1 (canonical / required)
**Range:** Integer ≥ 0 (no upper cap)
**Default at game start:** Varies by setting (TLS starts at $80 per Doc 30 §4.1)
**Decay:** Rent-driven (recurring cost — typically monthly); shop purchases
**Sidebar render:** Numeric display (with currency symbol; or `trait_words` if banded)

**What it tracks:** Economic pressure / income. Forces the player to engage with arcs (jobs, allowance). Distinct from corruption (sexual progression) and stat-traits (skill progression).

**When to use it:**
- Rent payment (recurring monthly drain; insufficient = game-over-ish)
- Shop purchases (clothing items at thrift store, contraceptive pills at pharmacy)
- Quest rewards (capstones may grant +$ via job offers, sex-work scenes)
- Allowance from NPCs at certain relation thresholds

**Why money, not another trait:**
- Economic axis is its own thing — separate from sexual / emotional / skill progression.
- Forces engagement with peer/service arcs (jobs).
- Discrete state (you have it or you don't), unlike continuous progression traits.

**Modifiers (what changes it):**
- Job rewards (+$20 to +$100 per shift)
- Capstone rewards (+$200 to +$500 for major scenes like SellingMyStepsister — RTS reference)
- Allowance (NPC at high relation gives weekly allowance)
- Rent (-$400/month or per setting)
- Shop purchases (-$ per item)

**What it gates (downstream content):**
- Rent payment (game state — can't pay rent = game-over-ish OR `rent_evicted` flag fail-forward)
- Shop items (thrift clothes, contraceptive pills, pregnancy tests)
- Some quest beats (need $X to do Y)
- Phone purchase, laptop purchase (RTS pattern)

**Don't use it for:**
- Emotional / sexual content gating (use `corruption`, `arousal`, `relation`)
- Lane 2/3 NPC substitution conditions
- Per-NPC arc progression (money is global, not per-NPC)

**Anti-pattern:** Gating Lane 2/3 substitutions on money ("Frank walks in IF Maya has $50+"). Wrong axis — money is economic pressure, not narrative trigger.

**RTS analog:** `$player.money` (integer).

---

## §4 — Tier 1 NPC Traits

### §4.1 — `arousal` (NPC)

**Tier:** 1 (canonical / required, per-NPC)
**Range:**
- **Family/ambient + slow-burn family NPCs:** 0–3 integer (per Doc 40 — RTS-faithful for family register)
- **Peer/dating + career NPCs:** 0–10 integer (matches player range)
- **Service NPCs:** 0–3 (workplace register stays bounded)
- **Antagonist/witness:** N/A (antagonists don't track arousal — use awareness or hidden state instead)

**Default at game start:** 0
**Decay:** None (no-decay per Doc 40 — both player + NPC arousal are always-climbing meters)
**Sidebar render:** Per-arc (see §8 — family/ambient + slow-burn family surface to sidebar; peer/service hide)

**What it tracks:** NPC's sexual interest in Maya. Climbs from Maya's actions (teases, flashes); resets to 0 on climax. The dispatcher precondition for Lane 2/3 walk-in scenes.

**When to use it:**
- Lane 2 random encounter conditions ("if Brother arousal > 0 → bedroom grope eligible")
- Lane 3 substitution conditions ("if Dad arousal > 0 → dishwashing dispatcher fires Dad scene")
- Lane 1 menu items that require NPC interest ("Tease at NPC arousal ≥ 1")
- Stage transitions (NPC arousal threshold combined with Maya corruption threshold marks Stage N → N+1)

**Why NPC arousal, not another trait:**
- `corruption` (NPC) is willingness; `arousal` is short-term wanting.
- Player `arousal` is Maya's interest; NPC `arousal` is the NPC's interest.
- `relation` is bond/love; `arousal` is sexual interest. Both can be high or low independently.

**Modifiers (what changes it):**
- Maya teases / flashes the NPC: +1 per tease/flash
- Daily passive: +1 per day for in-scope family NPCs (per Doc 40 — Dad/Brother/Grandpa hardcoded daily climb)
- Climax in a sex scene with the NPC: **author-emitted** reset to 0 via TWO effects on the climax canvas's exit_block — one for Maya, one for the NPC. **No engine macro auto-zeroes either** — RTS has `FinishSex`; TLS does not. Author must explicitly emit `{ targetType = "player", trait = "arousal", op = "set", value = 0 }` AND `{ targetType = "npc", npcId = "npc_X", trait = "arousal", op = "set", value = 0 }`.
- Some Lane 2/3 ambient scenes: +1 per beat

**What it gates (downstream content):**
- Lane 2 random encounter substitution
- Lane 3 dispatcher substitution
- Lane 1 hub menu items (tease, certain seduction buttons)
- NPC stage transitions (per-arc thresholds)

**Don't use it for:**
- Long-term content gating (use NPC `corruption` + `stage`)
- Cross-NPC state (each NPC's arousal is independent)
- Player-facing display for antagonist NPCs (would spoil the dramatic surprise)

**Anti-pattern:** Decaying NPC arousal per day. Doc 40 locks no-decay for family NPCs (RTS-verified — passive +1/day, never -1/day). If you author `[engine.daily_tick].traitEffects` with NPC arousal -1, that's wrong.

**RTS analog:** `$npc.X.arousal` (integer; emoji-tier-string only used in walkthrough display per Doc 13 §10).

---

### §4.2 — `corruption` (NPC)

**Tier:** 1 (canonical / required, per-NPC)
**Range:** 0–50+ integer (varies by arc depth — Frank caps higher than Marge; Brother in RTS hits 50+ at full arc)
**Default at game start:** 0
**Decay:** None (one-way climb)
**Sidebar render:** Per-arc (see §8 — family/ambient surface; peer/service hide)

**What it tracks:** NPC's willingness to act sexually with Maya. The NPC-side analog of player corruption. Climbs through scene completions; never decays.

**When to use it:**
- Lane 1 hub menu items at NPC's location (per-NPC corruption thresholds gate specific options)
- Lane 2/3 substitution conditions (often combined with NPC arousal + player corruption)
- NPC stage transitions
- Cross-NPC bridge scenes (e.g., RTS `SellingMyStepsister` gates on Brother corruption ≥ 10)

**Why NPC corruption, not another trait:**
- `arousal` is short-term wanting (fluctuates).
- `relation` is broader bond (love/trust).
- `corruption` is the willingness threshold — needed for actual sexual acts to fire.
- `stage` is discrete; `corruption` is continuous.

**Modifiers (what changes it):**
- Flash / tease scenes with this NPC: +1 per scene (RTS pattern: flash raises NPC corruption, not arousal)
- Capstone scenes: +5 to +10
- Sex completion: +1 to +3
- Daily passive: NONE

**What it gates (downstream content):**
- Lane 1 hub menu items (Sex with NPC at NPC corruption ≥ 5; harder acts at higher thresholds)
- Lane 3 substitution scenes (`StageTwoCorruption($npc.Brother)` predicate)
- Per-arc stage transitions
- Cross-NPC bridge scenes

**Don't use it for:**
- Player content gating (use `player.corruption`)
- Cross-NPC gating (each NPC's corruption is independent)
- Per-day decay
- Capstone triggers as the SOLE gate (capstones need flag + corruption threshold)

**Anti-pattern:** Capping all NPC corruption at the same max. NPCs vary per arc — Frank (family/ambient escalation) goes to 50+; Marge (service) stays under 20; Diana (antagonist) doesn't use corruption at all (use awareness instead).

**RTS analog:** `$npc.X.corruption` (integer 0–50+).

---

### §4.3 — `relation` (NPC)

**Tier:** 1 (canonical / required, per-NPC, per LO Q3 — single canonical name)
**Range:** 0–100 integer
**Default at game start:** 0
**Decay:** None (one-way climb; relations don't naturally decay)
**Sidebar render:** Per-arc (see §8 — peer/dating + service surface always; family surfaces post-establishment; antagonist hides)

**What it tracks:** NPC's interpersonal connection to Maya — the love/like/trust spectrum. Single canonical name across all arc shapes (per LO Q3 — `relation` is RTS-aligned and register-neutral enough to work for both intimate and professional bonds).

**When to use it:**
- Peer/dating arc progression (Ryan Stage transitions, first-date capstone triggers)
- Service arc trust gates (Marge promotes Maya at relation threshold)
- Family/ambient late-game intimate beats (Frank "sleep with him" at relation ≥ 30)
- Capstone triggers paired with stage flags
- Cross-NPC scenes that depend on Maya's standing with multiple NPCs

**Why relation, not another trait:**
- Single canonical name per LO Q3 — avoids the love/relation register split.
- Distinct from `corruption` — relation is bond; corruption is sexual willingness. NPC can be high-corruption + low-relation (FWB) or high-relation + low-corruption (chaste mentor).
- Distinct from `arousal` — relation is long-term; arousal is short-term.

**Modifiers (what changes it):**
- Talk / conversation scenes: +1 per scene
- Capstone scenes: +5 to +10 (first-date, partner-establish, declaration)
- Bonding activities (help with chores, listen to NPC's problem): +1 to +2 per
- Some Lane 2/3 intimate beats: +1
- Daily passive: NONE
- Some negative beats: -1 to -5 (rare; specific scenes only — e.g., RTS SleepingBrother negative ending at relation 12)

**What it gates (downstream content):**
- Peer/dating capstones (first-date at relation ≥ 5; partner at relation ≥ 15)
- Service arc trust gates (Marge tells Maya secrets at relation ≥ 20)
- Late-family intimate beats (Frank sleepover at relation ≥ 30)
- Some Lane 1 hub menu items (talk/comfort options at relation thresholds)
- Cross-NPC scenes (Diana confrontation outcome routes on Frank.relation)

**Don't use it for:**
- Short-term per-scene gating (use NPC `arousal`)
- Body-state (use `energy` / `hygiene`)
- Player corruption gating (use `player.corruption`)
- Stage transitions as sole gate (stage uses flag + corruption + relation)

**Anti-pattern:** Decaying relation per day. Relations don't naturally decay just from time passing. Specific negative scenes can decrement; daily_tick should NOT touch relation.

**RTS analog:** `$npc.X.relation` (integer 0–100, RTS-aligned).

---

### §4.4 — `stage` (per-NPC, stored on PLAYER namespace) — 🔒 INTERNAL-ONLY (NEVER PLAYER-FACING)

**Tier:** 1 (canonical / required, one per NPC with an arc)
**Range:** Integer 0 to N (N varies per arc depth — typically 0–4 or 0–5)
**Default at game start:** 0
**Decay:** None (stages don't regress)
**Sidebar render:** ❌ **HIDDEN** — never rendered to any sidebar item, never displayed in any player-facing UI surface.

> **⚠️ STORAGE DOCTRINE:** Stage is stored as a **PLAYER trait keyed by NPC slug**, NOT as a trait on the NPC object. Trait name pattern: `<npc_slug>_stage` (e.g., `frank_stage`, `ryan_stage`, `jake_stage`) at `player.core_traits.<slug>_stage`. Engine special-cases this at `v2.py:5183-5189` (`applyAndNotifyTrait` recognizes the regex `/^([a-z_]+)_stage$/` and updates `setup.npc_arc_stages` registry on upward delta). The NPC's `arc_stages = [...]` declaration on `[[npcs]]` is just the LIST of stage NAMES (display strings); the CURRENT stage value lives on player.

> **⚠️ PLAYER-FACING DOCTRINE:** Per LO Q1 — *"Stage shouldn't be a player-facing thing."* See §9 for the full stage-handling doctrine including how the player feels progression without seeing a stage number.

**What it tracks:** Discrete arc-progression milestone for one NPC's arc. Stored as an integer on the player namespace; used by authors + LLM for content gating; never surfaced to player. Player feels stage progression through what the world DOES (new menu items, NPC behavior shifts, location access opens), NOT through a stage number.

> **🔒 ENGINE-ENFORCED HIDE (2026-05-30):** "Never surfaced" is now mechanically enforced, not just a `sidebar_items` convention. The generator's `playerTraits` sidebar widget + Stats page dump EVERY `core_traits` key, so a `<slug>_stage` (and any other internal trait — `pregnancy`, antagonist `awareness`) WILL leak into both dumps unless suppressed. Add a `[[traits.labels]]` entry with `hidden = true` for each internal trait:
> ```toml
> [[traits.labels]]
> key = "frank_stage"
> hidden = true   # hide-only entry; `label` may be omitted
> ```
> The engine emits these as `setup.hiddenTraits` and skips them via `<<continue>>` in every trait-dump loop, in BOTH dev and non-dev builds. **Limitation:** keyed by trait NAME only (not namespaced) — a hidden key hides for the player AND any NPC carrying a core_trait of that name (e.g. an antagonist's `awareness`, which is exactly the intent). See `schema/02` `[[traits.labels]]` and the `stages/02` §11 checklist item.

**When to use it:**
- Lane 1 hub canvas selection (multiple canvases per location; engine picks by stage via `selectAutoFireCanvasForLocation`)
- Lane 2/3 substitution conditions ("if Frank stage ≥ 2 → kitchen substitutions eligible")
- Per-stage menu items inside hub canvases (group blocks gated on stage)
- Capstone trigger fingerprints (per Doc 57 R1 — capstones flag-set + stage-advance on exit)
- Quest card `when` conditions (NEVER the quest card text or goals — see §9)

**Why stage, not another trait:**
- `corruption` is continuous; stage is discrete milestone.
- `relation` is bond; stage is arc-progress.
- `arousal` is short-term; stage is permanent.
- Stage is the authoring shortcut for "where in the arc" — cleaner than chaining 3-trait conditions.

**Modifiers (how to advance it):**

```toml
# Capstone scene exit — advance Frank to stage 2
{ targetType = "player", trait = "frank_stage", op = "set", value = 2 }
```

- Effect uses `targetType = "player"` (NOT `targetType = "npc"`) because stage lives on player namespace
- Trait name is `<npc_slug>_stage` (e.g., `frank_stage`, NOT `stage`)
- `op = "set"` only — never `add` (stage advances are deliberate, capstone-driven; no auto-promotion)
- Stage advances are ALWAYS deliberate (via capstone or transition canvas), NEVER from accumulated stats alone
- Daily passive: NONE
- No regression
- Engine logs the advancement timestamp in `game_state.stage_advancement_log[slug]` on upward delta (used by E9 stalled-detection)

**What it gates (downstream content):**
- Lane 1 hub canvas variants (per-stage hub for the location)
- Per-stage menu items (`group` blocks inside hub canvases)
- Lane 2/3 substitution eligibility
- New activities unlocking at NPC's location (e.g., suck-in-pantry button at Frank stage ≥ 3)
- Capstone availability (next capstone in chain gates on current stage)

**How to CHECK stage in a condition (two forms; pick one):**

```toml
# Form A — raw player-trait check (RECOMMENDED for most uses)
{ type = "trait", subject = "player", trait_key = "frank_stage", operator = "gte", value = 2 }

# Form B — dedicated stage predicate via helper (engine plumbing; rarely needed)
{ type = "stage", helper = "frank_stage_2_plus", operator = "is_true" }
```

Form A is cleaner. Form B is engine plumbing (used internally by `stage_label` sidebar widget).

**Don't use it for:**
- **ANY player-facing surface.** No sidebar render. No quest card display. No menu text saying "Frank Stage 2." No achievement showing "Reached Stage 3."
- Continuous gating (use `corruption` for that — stage is for milestones)
- Cross-NPC gating (each NPC has its own `<slug>_stage` trait)

**Anti-pattern:** Writing `{ targetType = "npc", npcId = "npc_frank", trait = "stage" }`. Wrong namespace. The engine looks for stage on the NPC object (where it doesn't exist) instead of on the player namespace at `frank_stage`. Stage gating silently breaks; no build error fires.

**Anti-pattern:** Writing "Frank reaches Stage 2 now" in quest card prose or scene body. Wrong. The PLAYER doesn't think in stages; they think in events. Instead, the in-fiction equivalent — *"Frank invited me to his bedroom"* or *"Frank caught me snooping"* — is what the player sees. Stage is the engine's bookkeeping; events are the player's experience.

**RTS analog:** No stored equivalent — RTS uses derived helpers (`StageOneCorruption($npc.X)`, `StageTwoCorruption($npc.X)`) computed at read-time from underlying corruption + arousal thresholds. TLS stores stage explicitly per LO Q1 — but on the player namespace, not the NPC.

---

## §5 — Tier 2 Player Traits

These are common but optional — use them when the arc/setting calls for them. The LLM should not emit them unless the design book proposes the corresponding mechanic.

### §5.1 — `fitness` (Player)

**Tier:** 2 (common; use if exercise / gym mechanic in game)
**Range:** 0–100 integer
**Default at game start:** 0 (or 10 if game premise includes prior fitness)
**Decay:** None (progression trait per Doc 49)
**Sidebar render:** `trait_bar` if exercise mechanic exists; otherwise hidden

**What it tracks:** Maya's physical fitness — a progression stat for gym-related content + body-aesthetic gates.

**When to use it:**
- Exercise activity rewards (each exercise session +1 or +2)
- Gym-arc content gating (gym-NPC arcs unlock at fitness thresholds)
- Certain sex-scene variant gates (high-fitness Maya gets athletic sex variants)
- Some peer/dating beats (fit Maya can join sports club)

**Why fitness, not another trait:**
- `corruption` is sexual; `fitness` is physical/aesthetic.
- `beauty` is outfit-driven; `fitness` is body-driven.
- `intelligence` is mental; `fitness` is physical.

**Modifiers (what changes it):**
- Exercise activity: +1 to +2 per session
- Gym shifts (if working at gym): +1 per shift
- Capstone-specific gains: +5 to +10
- Daily passive: NONE

**What it gates:**
- Gym arc content
- Fitness-themed dating
- Athletic sex variants
- Some body-aesthetic-required scenes

**Don't use it for:**
- NPC interaction gating outside fitness-specific content
- Long-term progression in non-fitness arcs

**Anti-pattern:** Decay on missed days. Doc 40 + 49 — progression traits don't decay.

**RTS analog:** `$player.fitness` (integer).

---

### §5.2 — `beauty` (Player)

**Tier:** 2 (common; use with wardrobe system per Doc 36/37 — `worn_beauty` predicate)
**Range:** 0–N (derived from worn outfit's beauty value via `worn_beauty` predicate)
**Default at game start:** Derived (starts at starting outfit's beauty)
**Decay:** None (changes when outfit changes)
**Sidebar render:** Hidden (typically) or `trait_bar` (if game surfaces it)

**What it tracks:** Outfit beauty rating. Derived from worn clothing via `worn_beauty` (MAX aggregate from clothing_data per Doc 37). NOT a stored stat — it's a predicate that reads the worn outfit.

**When to use it:**
- Social content gates ("must look beautiful to attend the party")
- Certain peer/dating beats (beauty-threshold first-date scenes)
- NPC reaction variants (high-beauty Maya gets different prose at NPC encounters)

**Why beauty, not another trait:**
- It's derived from outfit (worn_beauty) — distinct from stored stats.
- Distinct from `fitness` (body-driven) — beauty is outfit-driven.
- Allows the player to "dress up" for specific content.

**Modifiers:**
- Outfit changes (worn_beauty re-derives from new outfit)
- No stat-mutator effects (don't write `{ trait_key = "beauty", op = "add" }` — beauty is derived, not stored)

**What it gates:**
- Some social scenes (party, club, formal event)
- Peer/dating beats requiring "looking your best"
- Some NPC reactions

**Don't use it for:**
- NPC sexual content gating (use `corruption`)
- Stored stat-like progression
- Anything that requires `op = "add"` or `op = "set"` (beauty is read-only via predicate)

**Anti-pattern:** Setting beauty as a stored trait. Doc 37 made it derived (worn_beauty predicate). Stored beauty creates a sync bug — if Maya changes outfits, stored value lags behind worn outfit.

**RTS analog:** `$player.beauty` (integer in RTS; TLS uses worn-derived predicate).

---

### §5.3 — `exhibitionism` (Player)

**Tier:** 2 (common; use if flash/tease/exhibitionism arc in game)
**Range:** 0–100 integer
**Default at game start:** 0
**Decay:** None
**Sidebar render:** `trait_bar` or `trait_words` (if banded into Modest / Open / Bold / Brazen)

**What it tracks:** Maya's comfort with showing her body. A narrower subset of corruption — the "show-off" axis. Distinct from corruption (broader transgression) and arousal (short-term).

**When to use it:**
- Flash menu items at NPC hubs (separate from sexual escalation)
- Naked-in-public access (Hallway access while naked)
- Exhibitionist content gates (cam shows, public sex, outdoor exposure)
- Certain Lane 1 menu items (flash, change-in-front-of-NPC)

**Why exhibitionism, not another trait:**
- `corruption` is broader transgression; exhibitionism is the show-off subset.
- Allows separate tracking of "comfortable being seen" vs "comfortable having sex."
- Useful for cam-girl / public arcs without conflating with sexual corruption.

**Modifiers:**
- Flash scenes: +1 per
- Naked-in-public beats: +1 per
- Cam show / public exposure scenes: +1 to +2

**What it gates:**
- Flash menu items
- Naked / underwear public access
- Cam-show / streaming-arc content (if game has career arc with that flavor)
- Outdoor sex scenes

**Don't use it for:**
- General sexual content gating (use `corruption`)
- NPC interaction gating

**Anti-pattern:** Collapsing exhibitionism into corruption. They're related but distinct — Maya can be high-corruption + low-exhibitionism (sexually active but private) or low-corruption + high-exhibitionism (loves being seen but not having sex yet). Keep them separate if the game's arc uses exhibitionism as a distinct progression.

**RTS analog:** `$player.exhi` (RTS integer trait).

---

### §5.4 — `intelligence` (Player) — also accepted: `intel`

**Tier:** 2 (common; use if school / study / academic arc in game)
**Range:** 0–100 integer
**Default at game start:** 0 (or 10 for "average student" premise)
**Decay:** None
**Sidebar render:** `trait_bar` if school mechanic exists; otherwise hidden

**What it tracks:** Academic / cognitive stat. Used for school arc, study mechanic, test grades, certain quest beats.

**When to use it:**
- Study activity rewards (+1 to +2 per session)
- School test / grade gates (Marcus-style "get test grade ≥ 8" quest)
- Tutor / library scenes
- Bookish capstones (academic milestones)

**Why intelligence, not another trait:**
- Separate axis from physical (fitness) / social (relation) / sexual (corruption).
- Specific to academic arcs.

**Modifiers:**
- Study activity: +1 to +2 per
- Tutor scenes: +2 to +3
- Some peer scenes (Brother helps study): +1
- Daily passive: NONE

**What it gates:**
- School content
- Test-grade-pegged quests
- Library/study-arc beats
- Some peer NPC scenes (intelligent Maya can hold smarter conversations)

**Don't use it for:**
- NPC interaction gating outside academic context
- Sexual content gating

**Anti-pattern:** Decay on missed days.

**RTS analog:** `$player.intel` (integer).

---

## §6 — Tier 3 Per-Game Additions

Tier 3 traits are **free-form per game** — authored against the design book, not part of the canonical vocabulary. The LLM emits them only when the design book proposes the mechanic.

**Examples of legitimate Tier 3 traits:**
- `follower_count` (Instafame / metric-grind career arcs — RTS Edward arc analog)
- `gym_membership` (boolean for gym-arc access)
- `notoriety` (small-town gossip mechanic; per-arc, not canonical)
- `confidence` (some character-development arcs use it)
- `language_skill` (foreign-NPC arc)
- `awareness` (per-NPC antagonist tracking — Diana model)

**Constraints on Tier 3:**
- Tier 3 traits CANNOT redefine Tier 1 or Tier 2 names. If a design book proposes "love" or "lust" or "horniness" as a new trait, the LLM redirects to the canonical equivalent (`relation` / `arousal`).
- Tier 3 traits must follow the same engine effect schema (§7) — declared in `[player.core_traits]` or per-NPC `core_traits` initial state, mutated via `{ targetType = "player", trait = "X", op = "add", value = N }`, tested via `{ type = "trait", subject = "player", trait_key = "X", operator = "gte", value = N }`. Effect + predicate use different field names — see §7.6.
- Tier 3 traits should be documented in the game's own design book + per-game README.

### §6.1 — Off-limits list (Phase 2+ traits — DO NOT AUTHOR AGAINST)

These traits surface from Phase 2+ engine work scoped in Doc 65. The LLM MUST NOT emit these in any generated game until LO calls the corresponding strategic decision per Doc 65.

#### `pregnancy.*` traits (Doc 65 E10b — Pregnancy retrofit)

```
player.pregnancy.isPregnant       (bool)
player.pregnancy.days             (integer; days since conception)
player.pregnancy.discovered       (bool)
player.pregnancy.pillDays         (integer; contraceptive cooldown)
player.pregnancy.father           (object — { name: str, discovered: bool })
player.babies[]                   (array of completed pregnancy records)
```

**Why off-limits:** Pregnancy is a complex engine feature requiring father-attribution, parallel scene variants, scandal interaction, birth events. None of this is in the v2 engine yet. Authoring against `pregnancy.isPregnant` without the engine produces broken references.

**Trigger to unlock authoring:** LO calls "ship pregnancy" per Doc 65. Until then, all sex scenes ship bareback (per Doc 30 §7.3.1) with no pregnancy language — future pregnancy retrofit will be additive, not breaking.

**When a Phase-2+ trait IS included, you MUST author its SETTER — the build won't catch a dormant trait.** The flag-chain validator checks FLAGS, not TRAITS: an included trait that's declared but never `set` by any canvas passes the build and ships INERT (its dependent content never fires). When `pregnancy = include`, author a canvas that sets `player.pregnancy` (e.g. a hidden onset event keyed off an `had_unprotected_sex` flag from the first-full-sex capstones) AND the pregnant-variant surfaces for it to gate (each father-NPC needs an ongoing sex hub — `doctrine/10` §6). Late Shifts shipped pregnancy "included" but with no setter → all breeding content was dead until a setter was retro-wired. (Engine-side catch proposed: `PREVENTION_LINTER_SPEC.md` L6.)

#### `scandal_level` / `reputation` (Doc 65 E10c)

**Why off-limits:** Global scandal/reputation is a new engine system requiring multiple writer arcs (outdoor scenes), multiple reader arcs (Diana confrontation gate, town-NPC reactions), and UI surface.

**Trigger to unlock authoring:** LO calls "ship scandal" per Doc 65. Until then, antagonist arcs use per-NPC `awareness` (silent accumulator) instead of global scandal.

#### `gallery.*` flags (Doc 65 E10e)

```
gallery.unlocked_scenes[]
gallery.achievements[]
```

**Why off-limits:** Gallery UI requires Doc 62 (canvas `guide` field) + Doc 64 (sidebar radar) + the gallery panel itself. None shipped.

**Trigger to unlock authoring:** Doc 62 ships + LO calls "ship gallery."

#### Cross-arc completed-scenes tracker (Doc 65 E10f)

```
player.completed_scenes[]
npc.X.completed_scenes[]
```

**Why off-limits:** Cross-arc state writers + readers require the tracker mechanism shipped + the canvas `guide` field. Neither in engine yet.

**Trigger to unlock authoring:** Doc 62 ships + LO calls "ship cross-arc tracker."

---

## §7 — Engine effect schema (how traits emit in TOML)

> **⚠️ CRITICAL — effect syntax vs predicate syntax use DIFFERENT field names.** Both shapes appear below; do not mix them.

### §7.1 — Trait effect (mutate a trait value)

```toml
# Player trait effects
{ targetType = "player", trait = "corruption", op = "add", value = 1 }
{ targetType = "player", trait = "arousal", op = "set", value = 0 }
{ targetType = "player", trait = "energy", op = "add", value = -10 }   # decay via negative-add
{ targetType = "player", trait = "money", op = "add", value = 50 }

# NPC trait effects
{ targetType = "npc", npcId = "npc_frank", trait = "relation", op = "add", value = 2 }
{ targetType = "npc", npcId = "npc_frank", trait = "arousal", op = "add", value = 1, cap = 3 }

# With clamp + cap
{ targetType = "player", trait = "arousal", op = "add", value = 1, clamp = true, cap = 10 }
```

**Required fields:**
- `targetType` — `"player"` or `"npc"` (NOT `subject` — that's predicate)
- `trait` — trait name (NOT `trait_key` — that's predicate)
- `op` — operation (see §7.2)
- `value` — numeric

**Optional:**
- `npcId` — required when `targetType = "npc"` (NOT `npc_id` — that's predicate)
- `clamp` — boolean; floor at 0
- `cap` — upper bound

Schema: `TemplateChoiceEffect` at `template_import.py:503`.

### §7.2 — Allowed `op` values

Engine supports exactly **two `op` values** for trait effects:

| op | Behavior |
|---|---|
| `"add"` | Adds `value` to current trait (use negative `value` for decay/subtraction) |
| `"set"` | Sets trait to `value` directly |

**There is no `"sub"` op.** Decay = `op = "add"` with negative `value` (e.g., `value = -10` to subtract 10).

### §7.3 — Per-trait operation conventions

| Trait | Common ops | Notes |
|---|---|---|
| `player.corruption` | `add` (positive) | One-way climb |
| `player.arousal` | `add` (positive); `set` to 0 only at climax | **No engine macro auto-zeroes** — author must explicitly emit `op = "set", value = 0` |
| `player.energy` | `add` with negative value (decay); `set` to 100 (sleep restore) | `cap = 100` recommended |
| `player.hygiene` | `add` with negative value; `set` to 100 (shower) | `cap = 100` recommended |
| `player.money` | `add` (positive/negative) | Income / costs |
| `npc.X.arousal` | `add` (positive); `set` to 0 at climax | Same author-emitted reset as player arousal |
| `npc.X.corruption` | `add` (positive) | One-way climb |
| `npc.X.relation` | `add` (positive/negative; negative rare) | Doesn't decay daily |
| `<npc_slug>_stage` (player namespace — see §9) | `set` only | Deliberate capstone advances |
| Tier 2 player traits | `add` (positive) | One-way climb |
| Body-state (`energy`, `hygiene`) | `add` (negative for decay), `set` for restores | Daily decay via `[engine.daily_tick].traitEffects` |

### §7.4 — Flag effect (set/unset/toggle a flag)

Different schema from trait effects (separate dataclass `TemplateFlagEffect` at `template_import.py:521`):

```toml
{ targetType = "player", flag = "frank_caught", op = "set" }
{ targetType = "player", flag = "talked_to_ryan_today", op = "unset" }
{ targetType = "npc", npcId = "npc_frank", flag = "secret_known", op = "set" }
{ targetType = "player", flag = "scandal_visible", op = "toggle" }
```

**Required fields:**
- `targetType` — `"player"` or `"npc"`
- `flag` — flag name (NOT `flag_key` — that's predicate)
- `op` — `"set"`, `"unset"`, or `"toggle"`

**Optional:**
- `npcId` — required when `targetType = "npc"`

### §7.5 — Predicate (trigger condition) schema

> **The predicate schema uses DIFFERENT field names from effects.** This is the engine's actual API — there's no translation layer.

```toml
[canvases.trigger.conditions]
version = "1.0"
items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 15 },
  { type = "trait", subject = "npc", npc_id = "npc_frank", trait_key = "relation", operator = "gte", value = 30 },
  { type = "trait", subject = "player", trait_key = "frank_stage", operator = "gte", value = 2 },   # stage check
  { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_true" },
]
```

**Predicate field names:**
- `type` — `"trait"`, `"flag"`, `"modifier"`, `"days_since_flag"`, `"clothing_slot"`, `"clothing_item"`, `"pass"`, `"item"`, `"stage"`, `"quest"`, `"worn_beauty"`, `"worn_corruption"`, `"worn_type"`, `"corruption_level"`
- `subject` — `"player"` or `"npc"` (predicate uses `subject`; effects use `targetType`)
- `trait_key` (for `type = "trait"`) — trait name (predicate uses `trait_key`; effects use `trait`)
- `flag_key` (for `type = "flag"`) — flag name (predicate uses `flag_key`; effects use `flag`)
- `npc_id` (when `subject = "npc"`) — NPC slug (predicate uses `npc_id`; effects use `npcId`)
- `operator` — comparison op (`"gte"`, `"lt"`, `"eq"`, etc.)
- `value` — comparison value

**Allowed predicate `operator` values:**
- Numeric: `"eq"`, `"ne"`, `"gt"`, `"gte"`, `"lt"`, `"lte"`
- Set: `"in"`, `"not_in"`
- Boolean (for flags + booleans): `"is_true"`, `"is_false"`
- Existence: `"exists"`, `"not_exists"`

### §7.6 — Field-name reference card (KEEP HANDY)

The single most common authoring mistake is mixing effect + predicate field names.

| Concept | EFFECT field | PREDICATE field |
|---|---|---|
| Player vs NPC | `targetType` | `subject` |
| NPC identifier | `npcId` | `npc_id` |
| Trait name | `trait` | `trait_key` |
| Flag name | `flag` | `flag_key` |
| Operation | `op` (`"add"`, `"set"` for traits; `"set"`, `"unset"`, `"toggle"` for flags) | `operator` (`"gte"`, `"lt"`, etc.) |
| Type discriminator | (dispatched by `trait` vs `flag` field presence) | `type` (required: `"trait"`, `"flag"`, etc.) |

**Using effect field names in a predicate (or vice versa) causes silent no-ops — no build error fires.** Validators at `template_import.py:1077` + `:1098` catch some cases as warnings, not all.

---

## §8 — NPC trait sidebar visibility doctrine

Per LO Q6: each NPC's design brief (R7 per Doc 56) declares which traits surface to the player. The catalog provides per-arc-shape defaults; the brief can deviate with reason.

| Arc shape | Sidebar surfaces (default) | Rationale |
|---|---|---|
| **Family/ambient** (Frank) | location + arousal + corruption + relation | Player needs to plan Lane 3 attempts (arousal), Lane 1 escalation (corruption), late-game intimacy (relation). All three mechanically relevant. RTS surfaces all three for family NPCs — verified live. |
| **Slow-burn family** (Jake) | location + arousal + relation | Corruption stays low in slow-burn arcs by design; surfacing it would mislead the player. Arousal + relation are the player-relevant dimensions. |
| **Peer/dating** (Ryan) | location + relation | Dating chain is relation-driven. Arousal is bounded + less player-controllable. Corruption isn't meaningful for peer arcs. |
| **Service** (Marge) | location + relation only | Workplace bond is the operative axis. Arousal/corruption don't apply to service register. |
| **Antagonist/witness** (Diana) | location only | Awareness/scandal accumulator stays HIDDEN — dramatic surprise depends on player NOT seeing how close confrontation is. Doc 30 §6 + Doc 60 lock this. |
| **ALL arc shapes** | `stage` NEVER surfaces | Per LO Q1 + §9 — stage is internal-only across all NPCs. |

### Authoring rule (R7 brief addition)

When writing an NPC's design brief, declare a "Sidebar surfaces" line:

```markdown
**Sidebar surfaces:** location + arousal + corruption + relation (family/ambient default per Doc 68 §8)
```

The brief can override the default with reason. Override must be documented.

---

## §9 — Stage trait special-handling doctrine

Per LO Q1 — *"Stage shouldn't be a player-facing thing."* Stage is the canonical example of a stored trait that lives entirely in the authoring layer and never surfaces to the player.

### §9.0 — Storage location

Stage is stored as a **player-namespace trait keyed by NPC slug**: `player.core_traits.<slug>_stage`. The NPC's `arc_stages = [...]` declaration on `[[npcs]]` is just the LIST of stage NAMES (display strings used by the optional `stage_label` sidebar item — which doctrine FORBIDS using for player-facing rendering); the CURRENT stage integer lives on the player object.

Engine recognition: `applyAndNotifyTrait` at `v2.py:5183-5189` matches the trait name against `/^([a-z_]+)_stage$/` and, when `targetType === 'player'` + delta > 0, updates `setup.npc_arc_stages` registry + writes `game_state.stage_advancement_log[slug] = currentDay`.

**Mutation syntax (advance Frank to stage 2):**

```toml
{ targetType = "player", trait = "frank_stage", op = "set", value = 2 }
```

**Common authoring mistake — wrong namespace:**

```toml
# ❌ WRONG — stage doesn't live on the NPC object
{ targetType = "npc", npcId = "npc_frank", trait = "stage", op = "set", value = 2 }
```

### §9.0.1 — Checking stage in a condition

**Form A — raw player-trait check (RECOMMENDED):**

```toml
{ type = "trait", subject = "player", trait_key = "frank_stage", operator = "gte", value = 2 }
```

Simple, readable, no indirection. Use for almost all stage checks.

**Form B — dedicated `stage` predicate via helper:**

```toml
{ type = "stage", helper = "frank_stage_2_plus", operator = "is_true" }
```

Used internally by `stage_label` sidebar widget. Don't author in trigger conditions.

### What stage IS used for

- **Lane 1 hub canvas selection.** `selectAutoFireCanvasForLocation` picks per-stage canvas at a location.
- **Lane 2/3 substitution conditions.** Substitution rule conditions reference NPC stage.
- **Per-stage menu items inside hub canvases.** `group` blocks gated on stage.
- **Capstone trigger fingerprints.** Per Doc 57 R1.
- **Quest card `when` conditions.** Cards route on NPC stage (without exposing stage number in text).

### What stage is NEVER used for

- **Sidebar items.** No `trait_bar`, no `trait_status_text`, no `trait_words` rendering of stage.
- **Quest card text.** Card prose says *"Frank invited me to his bedroom"*, NOT *"Frank stage 2 reached"*.
- **Quest card `goals` block.** Goals describe in-fiction milestones, not stage numbers.
- **NPC menu text.** Hub canvas prose says *"Frank watches you with a new tension"*, NOT *"Frank Stage 2 unlocked"*.
- **Achievement / notification toasts.** No "Stage 2 reached!" popup.
- **Dev shortcuts in player-visible builds.** Fine for authoring/testing; should not ship in player-facing builds.

### How the player feels stage progression (without seeing it)

| Stage transition | What the player sees |
|---|---|
| Frank Stage 0 → 1 (Maya helps Frank with bookkeeping) | New "Stand close while he reads" menu item in Frank's office hub. Coffee Alone Lane 2 ambient ends differently. |
| Frank Stage 1 → 2 (catch capstone fires) | Frank's kitchen morning hub renders different opening prose. "Sleepover" option appears at evening hub. Hallway pass-by Lane 2 ambient has new variant. |
| Frank Stage 2 → 3 (first night capstone) | Frank's bedroom unlocks as a location. Per-stage Lane 3 substitution kitchen-dishes-while-Frank-cooks becomes eligible. |

The player understands the arc moved without needing a stat number. RTS calls this **"emergent escalation"** — the world fills out around the player as they escalate; the world model itself is the progress feedback.

### Doctrine summary

> **`stage` is stored, never rendered, never spoken of in player-facing text. It exists for the LLM and the validator. Player progression is communicated through content changes, never through stage numbers.**

---

## §10 — Anti-patterns (cross-trait misuses)

### Trait-name anti-patterns

- **Inventing new Tier 1 names.** If the design book proposes `lust`, `horniness`, `desire`, or `attraction`, redirect to `arousal`. If it proposes `love`, `affection`, `attraction-bond`, redirect to `relation`. If it proposes `depravity`, `degeneracy`, `lewdness`, redirect to `corruption`. Tier 1 names are canonical for a reason — multi-game consistency.

- **Per-NPC trait references without proper namespacing.** Two forms — predicate vs effect — use different field names (§7.6).
  - **Predicate (condition):** wrong: `{ type = "trait", subject = "player", trait_key = "npc_frank_corruption" }`. Right: `{ type = "trait", subject = "npc", npc_id = "npc_frank", trait_key = "corruption", operator = "gte", value = 5 }`.
  - **Effect (mutation):** wrong: `{ targetType = "player", trait = "npc_frank_corruption", op = "add" }`. Right: `{ targetType = "npc", npcId = "npc_frank", trait = "corruption", op = "add", value = 1 }`.
  - EXCEPTION: stage traits live on the player namespace as `<slug>_stage` — see §9.

### Range / type anti-patterns

- **Player corruption outside 0–100.** Per LO Q2 lock. Don't author against the RTS 0–200 scale.
- **Family NPC arousal outside 0–3.** Per Doc 40. If the LLM emits `{ trait_key = "arousal", op = "add", value = 5 }` for Frank, that's wrong (overflows 0–3, breaks Stage-gating).
- **Float values in integer traits.** All canonical traits are integer; don't emit `value = 0.5`.

### Decay anti-patterns

- **Decaying corruption.** Corruption never decays.
- **Decaying arousal.** Per Doc 40 — no-decay rule. Reset to 0 only at climax.
- **Decaying relation.** Specific negative beats can decrement; daily_tick should NOT touch relation.
- **Decaying stage.** Stages don't regress, ever.
- **NOT decaying energy or hygiene.** These ARE supposed to decay (body-state per Doc 49). If the LLM authors `energy` as no-decay, that's wrong.

### Gating anti-patterns

- **Using arousal for content-tier gating.** Wrong axis — arousal is short-term per-attempt. Use `corruption`.
- **Using corruption for activity-attempt gating.** Wrong axis — corruption is content-progression. Use `energy`.
- **Using `relation` for sexual content gating.** Relation is bond; corruption is sexual willingness. High relation + low corruption = mentor; high corruption + low relation = FWB.
- **Gating Lane 2/3 substitutions on money.** Wrong axis — money is economic; substitutions are sexual/narrative.

### Visibility anti-patterns

- **Exposing stage to the player.** Per LO Q1 + §9.
- **Surfacing antagonist awareness to sidebar.** Per Doc 30 §6 + §8 — the dramatic surprise depends on the player NOT seeing how close confrontation is.
- **Hiding body-state from player.** Energy + hygiene MUST surface. Player needs to know when to sleep/shower.

### Phase 2+ anti-patterns

- **Authoring against `pregnancy.*` traits.** Off-limits per §6.1.
- **Authoring against `scandal_level` / `reputation` globally.** Use per-NPC `awareness` instead.
- **Authoring against `gallery.*` flags.** Off-limits until Doc 62 + gallery panel ship.
- **Authoring against `completed_scenes[]` tracker.** Off-limits until Doc 62 + cross-arc tracker ship.

### Effect-schema anti-patterns

- **Effect using predicate field names (`subject` / `trait_key` / `npc_id`).** Wrong: `{ type = "trait", subject = "player", trait_key = "corruption", op = "add", value = 1 }`. Right: `{ targetType = "player", trait = "corruption", op = "add", value = 1 }`. Using predicate field names in an effect causes silent no-op with NO build error.
- **Predicate using effect field names (`targetType` / `trait` / `npcId`).** Same silent-failure risk in reverse direction.
- **NPC effect without `npcId`.** Wrong: `{ targetType = "npc", trait = "corruption", op = "add", value = 1 }`. Right: includes `npcId = "npc_frank"`.
- **Stage effect targeting NPC namespace.** Wrong: `{ targetType = "npc", npcId = "npc_frank", trait = "stage", op = "set", value = 2 }`. Right: `{ targetType = "player", trait = "frank_stage", op = "set", value = 2 }`.
- **`op = "sub"` for decay.** Engine has no `sub` op (only `add` + `set`). Use `op = "add"` with negative `value`: `{ targetType = "player", trait = "energy", op = "add", value = -10 }`.
- **Stage advance via `op = "add"`.** Wrong: `{ targetType = "player", trait = "frank_stage", op = "add", value = 1 }`. Right: `{ targetType = "player", trait = "frank_stage", op = "set", value = 2 }`. Engine doesn't auto-promote on accumulated `add`s.

---

## §11 — Cross-references

### Sibling doctrine files

- `doctrine/01_rts_principles.md` — P6 (stats change during scenes); P10 (HUD = world model)
- `doctrine/02_three_lanes_plus_capstone.md` — lane gating uses traits
- `doctrine/03_arc_shapes.md` — per-arc-shape sidebar visibility defaults
- `doctrine/04_authoring_rules.md` — rules reference trait names + ranges

### Schema files

- `schema/01_engine_capabilities.md` §6 — effect + predicate vocabulary
- `schema/02_toml_schema.md` §16 — field-name reference card

### Source docs

- `28th_april_TLS_Phase2_Redesign/68_Trait_Catalog.md` — source for this file
- `28th_april_TLS_Phase2_Redesign/40_Player_Arousal_System.md` — no-decay rule + 0–10 player / 0–3 family NPC ranges
- `28th_april_TLS_Phase2_Redesign/49_Story_Goals_vs_Sidebar_Doctrine.md` — body-state vs progression distinction
- `28th_april_TLS_Phase2_Redesign/65_Phase2_Plus_Strategic_Scope.md` — Phase 2+ off-limits decisions

### Engine primitives

- `applyAndNotifyTrait` (`v2.py:5174`) — core trait mutation
- `triggerConditionsSatisfied` (`v2.py:3275`) — predicate evaluation
- Stage advancement detection (`v2.py:5183-5189`) — `<slug>_stage` regex recognition
- `_player_trait_keys` validator (`template_import.py:2382-2547`) — hard-rejects undeclared traits in sidebar items

---

**End of file.** Batch 1 complete. Next: §9.1 quality gate.

═══════════════════════════════════════════════════════════════════════════════

## 14. 10_location_design

**Source:** `prompts_v2/doctrine/10_location_design.md`

---

# Doctrine 10 — Location Design + Reachability

**Sources:** Late Shifts build session (2026-05-29/30) — 7 location/reachability bugs that all shipped a GREEN build; TLS gold-standard location graph (`games/the_long_summer_test/toml_phases/1_metadata_and_locations.toml`); engine code `apps/game_generation/twee_comprehensive/generators/v2.py` + `apps/world/models.py`.
**Authority:** Doctrine. How to lay out a game's locations so navigation is geographically coherent AND every canvas is actually reachable in play.
**Purpose:** Close the single largest corpus gap. The validator checks *static* facts (a flag has a setter, a trait is declared) but NEVER checks *dynamic reachability* (can this canvas fire given location type, NPC schedule, time window, player presence). Six of the seven Late Shifts location bugs were invisible to the build — caught only by live-play. This file makes them authoring-time rules.

Cross-reference: `schema/02_toml_schema.md` §4 (location TOML fields); `schema/01_engine_capabilities.md` §5 (schedule/presence primitives); `doctrine/03_arc_shapes.md` (per-shape location footprint).

---

## §1 — The two things a location author must get right

1. **Geography** — the nav graph must read like a real place. Leaving the street should not drop you inside a private bedroom.
2. **Reachability** — every canvas attached to a location must be able to *fire* there. A canvas can be perfectly valid TOML and still be permanently dead.

Both are silent: a wrong location graph builds GREEN and only reveals itself in play. Treat this file as a pre-ship gate, not a style guide.

---

## §2 — The engine model (three independent fields — do not conflate them)

Per `apps/world/models.py` + `v2.py`:

| Field | What it controls | NOT |
|---|---|---|
| `entry_from` | **Navigation.** "You can reach me from here." The **"Leave X" link always points to `X.entry_from`** (`v2.py:17437`). Child destinations at a hub = every location whose `entry_from` points here (`models.py:301` `get_navigable_locations`), ordered by `navigation_order`. | not hierarchy |
| `parent` (`parent_location`) | **Structure only** — canvas inheritance + visual grouping. | NOT used for nav links. A location's `parent` and `entry_from` may differ. |
| `is_container` + `default_entry` | A **pure-nav wrapper**: auto-redirects into a child, holds no content of its own. | NOT a place that can host canvases (see §3). |

**The one rule that matters most:** the player walks the **`entry_from` chain**. `parent` is bookkeeping. A top-level location (no `entry_from`) emits **no "Leave" link** — it is a *root*, reached only via a walk-activity bridge (see §5). Nesting is supported up to 20 levels (`models.py:289`).

---

## §3 — `is_container` SWALLOWS attached canvases (Late Shifts bug B1)

**Rule: never attach a canvas (activity / ambient / capstone / portrait-hub) to an `is_container = true` location.**

Why: the passage generator branches on container status (`v2.py:8800`). A container passage emits **only** child-navigation — it never calls `getStoryCanvasRedirect` (auto-fire capstones), `renderNpcPortraits` (NPC hubs), or `renderSoloActivities` (solo activities). Any canvas whose `trigger.location` is a container is **silently dead**, and the container double-renders its nav (text links + card grid).

In Late Shifts both hubs were containers with the walk-home activity + the entire Pam arc + Cole's walk attached → town-trap soft-lock + a dead arc, all GREEN.

**Two correct patterns:**

- **A — Standing hub (preferred for game-specific hubs):** a NON-container location that carries `navigation_order` for its children AND hosts canvases. Children reach it via `entry_from`; `isCanvasValid`/`get_navigable_locations` resolve children by `entry_from` independent of container status. This is what Late Shifts uses post-fix.
- **B — Thin wrapper + arrival child (TLS gold standard):** an `is_container` wrapper with `default_entry` → auto-redirect to a NON-container arrival child that holds the canvases. TLS: `loc_property` (container) → `loc_front_porch` (arrival, standing) → `loc_hallway` (interior hub, standing). The container is pure routing; all content lives on the standing children.

Pick A by default. Use B only when you want the wrapper-level auto-redirect.

---

## §4 — Geographic layering (Late Shifts bug C1)

**Rule: a private dwelling, the shared building it sits in, and the town outside are SEPARATE locations. Never collapse "my apartment" and "the building corridor" into one hub.**

The Late Shifts original had one `loc_apartment_hallway` playing both Maya's private foyer AND the building's shared corridor — so the street opened into the bedroom hallway and a neighbor spawned beside the bedrooms. The fix layered it:

```
rooms (bedroom, kitchen, bath, laundry…)
  → loc_mayas_apartment      PRIVATE unit hub (only household members)
  → loc_building_hallway     SHARED corridor (neighbors, mailboxes, stairwell-ready)
  → loc_building_front       EXTERIOR root (top-level; the steps)
  → [activity_walk_to_town] → loc_main_street   TOWN root (top-level)
     → diner / park / shops…
```

Each "Leave" crosses one real threshold (room → unit → corridor → street → town). Authoring consequences:

- **Household NPCs** (live-in family) belong inside the private unit. **Neighbors / witnesses** belong in the shared building layer (corridor, front steps, laundry IF shared) — never inside the private unit.
- **Two top-level roots** (home-exterior + town), each with NO `entry_from`, **bridged by walk-activity canvases** (`activity_walk_to_town` / `activity_walk_home`), NOT by an `entry_from` link. (TLS + Late Shifts both do this.)
- **Laundry placement is a per-game call:** in the private unit = a chore room, no neighbor crossings; in the shared building = a neighbor-encounter surface. Decide based on whether you want it to host neighbor scenes.
- **`navigation_order` ↔ `entry_from` coupling (bug A5):** a slug listed in a location's `navigation_order` MUST have its `entry_from` pointing back at that location, or the validator rejects it ("not a destination"). Keep the two in sync.

Don't over-build: one floor / one unit is right for a small cast. The chain extends trivially for more floors (`loc_building_stairwell` off the corridor → `loc_building_hallway_2` …) — note it in a comment, don't author it speculatively.

---

## §5 — The Reachability Triad (Late Shifts bugs B2 / B3 / B4)

**A canvas fires only when all three overlap:**

> **(1) the NPC is present** (per `[[npcs.schedules]]`, schedule-only + fail-closed via `getNpcLocation`)
> **∩ (2) the canvas's own time-window** (`[[canvases.trigger.schedules]]`)
> **∩ (3) the player is actually there and awake** (not asleep, not at work — where the loop puts them).

If the intersection is empty, the canvas is dead and the build won't tell you. Three distinct failure modes, all seen in Late Shifts:

### §5.1 — `requires_npc` location ∉ that NPC's schedule (B2)
A canvas with `requires_npc = npc_X` only fires when `getNpcLocation(X) == its location`. If the canvas's location is not one of X's `[[npcs.schedules]]` entries, it **never** fires. Late Shifts: `scene_hank_first_contact_kitchen` + 3 Hank subs sat at `loc_diner_back`, but Hank was scheduled front-of-house + office only → the sole setter of `hank_first_contact` was unreachable → Hank's whole Stage 2→5 chain dead, the office permanently locked.
**Fix (faithful):** schedule the NPC into the location (give Hank a kitchen-check window) rather than relocating intimate scenes to a public floor.
**Fix (walk-ins where the NPC genuinely can't be scheduled there):** DROP `requires_npc` and time-gate with the substitution target's OWN `[[canvases.trigger.schedules]]` — `isCanvasValid` (`v2.py:4005`) enforces a sub target's own schedule + conditions. The prose ("he'd knocked, she hadn't heard") carries the implied presence.

### §5.2 — Portrait hub needs the NPC schedule-present (B3) — distinct from §5.1
`renderNpcPortraits` (`v2.py:4295`) has its OWN presence gate (`getNpcLocation(npc) === locationId`), independent of `requires_npc`. A Lane-1 portrait hub (`npc =` set) renders **no portrait** — i.e. is unclickable / unreachable — if that NPC isn't scheduled at the hub's location, even with no `requires_npc`. Late Shifts: Cole's new apartment hub showed nothing until Cole was given a `loc_cole_apartment` schedule window. (Auto-fire capstones with no `npc=` are NOT portrait-gated, so they fired regardless — only the manual portrait HUB needed the schedule.)

### §5.3 — Timing dead-zone (B4)
Even when NPC + location agree, the player must be there *and awake*. Late Shifts Pam: all her scenes sat at a hallway window of 09:00–11:00, but Maya **sleeps 07:00–14:00** off the night shift → empty intersection, confrontation could never fire. Fix: anchor the canvas to where the player *actually crosses the NPC* (Pam → the front steps in the evening, the mandatory pre-shift waypoint). Mind cross-midnight windows when you check overlap (22:00–07:00 wraps).

**Authoring rule for every NPC ambient/capstone:** anchor it where the player *actually crosses the NPC during the daily loop* — not where the fiction first imagines them. Then sanity-check the triad by hand.

### §5.4 — Locked location ∩ NPC schedule: the unlock contract

A fourth reachability failure the triad doesn't cover: the NPC and the time-window agree, but **the location itself is locked** — so the player can't be present at all. A locked location is a `[[locations]]` with `entry_conditions` (a flag predicate) + `blocked_message`. Our engine's lock is **visible-but-blocked**: the room shows on the nav and, on a failed entry, prints its `blocked_message` ("He hasn't invited me back there yet"). (Contrast RTS, which has two axes — a *discovery* lock that renders the venue **absent** from the map and a recurring *time* lock with a "CLOSED / Opens at X" badge; `reference/01` §6.5. We have only the flag lock; there is **no native time-of-day location lock** — the time/exposure axis lives on the hub via `trigger.schedules` + D72-R7, never on the door. Don't invent a location field the engine lacks.)

**The contract.** A schedule row at a locked location is a **deferred** hub promise (D72-R6 corollary, `doctrine/04` §6.1). It is legitimate *only* when the lock reads as **"haven't met / been invited yet"** and **the unlock is a beat the player can reach at an OPEN location.** The lock represents the social fact; the meeting is the key.

| Case | Shape | Verdict |
|---|---|---|
| **A — private place, meeting unlocks it** | The locked location *is* the NPC's private space; the player meets them at an **open** on-ramp, and that beat sets the unlock flag. *LS Cole:* `loc_cole_apartment` gated on `cole_date_done`; Cole met at the open diner/park; the date sets the flag. | **Correct.** The locked row is a deferred promise — legitimate per the R5 access-gate carve-out (`doctrine/05`/Doc 55): pre-onboarding the player can't be there *and* has no reason to be. Keep it; don't separately flag-gate the hub (the door already gates it). |
| **B — deeper room of an already-reachable NPC** | A secondary room the NPC routes into; the NPC is reachable elsewhere meanwhile. | **Acceptable only if all three hold:** (i) **legible** lock (visible-but-blocked, so the NPC stepping in reads as "gone somewhere I can't follow yet," not "vanished"); (ii) **co-gated *or* off-hours+fallback** — *best:* the door flag is the same flag that gates the player's access to that window, so there is **zero** dead window (*LS Hank back room* ← `hired_at_diner`: can't work the close unless hired, and being hired opens the back); *acceptable:* a **later** flag, but the window sits in hours the player doesn't routinely share **and** the NPC has open-location presence bracketing it (*LS Hank office* ← `hank_first_contact`, 01:30–06:00 graveyard, Hank on the floor up to 01:30 and again from 06:00 — a **bounded legible** dead window, tolerable); (iii) the locked row is **not** the NPC's only/primary presence. |
| **C — reachable only via a locked location** | The NPC is *only ever* scheduled at locked location(s), **or** the unlock flag has no reachable setter (incl. chicken-and-egg: the door is gated on a flag only settable behind the door). | **The bug — unreachable NPC.** Fix: give an open on-ramp with a reachable setter, or start the location unlocked and gate the *canvas/choices* instead of the door. |

**Legible-lock principle.** Because a locked window means the NPC is *present-but-unreachable* for that slice, the lock must read as a closed door, not a disappearance. The failure to avoid is an NPC shunted into a locked room during a window the player **routinely shares**, with no open fallback and/or an illegible gate → "where did they go?" (`doctrine/02` §8.15). This is distinct from **dead presence** (`doctrine/02` §8.11), which is an NPC at a *reachable* location rendering nothing.

**Schedule-page leak.** The Schedule page renders declared `[[npcs.schedules]]` rows regardless of the location lock, so it will list the NPC at a locked location. With our visible-but-blocked model that's tolerable, even flavorful ("the boss does the books in the office overnight"). If a game ever adopts RTS-style *discovery* hiding, the schedule page must also suppress rows at not-yet-unlocked locations — or it leaks the hidden place.

---

## §6 — Per-arc-shape location footprint (Late Shifts bug B6)

- **Family/ambient + slow-burn family:** live-in; canvases attach to shared-household standing locations the player already frequents.
- **Peer/dating (Ryan-shape):** needs an **ongoing Stage-4 repeatable hub at the partner's location**, not only a first-night capstone. Late Shifts shipped Cole with ONLY the one-shot `scene_cole_first_night` and no repeatable hub — so once consummated, the arc had no surface and pregnancy/ongoing content had nowhere to attach. The partner's home is access-gated on the relationship flag (e.g. `cole_date_done`), and the ongoing hub is gated on the consummation flag (`cole_first_night_done`) at a priority below the first-night capstone so the capstone fires first, then the hub takes over. The hub NPC must be schedule-present there (§5.2).
- **Service:** workplace location only; no home surface.
- **Antagonist/witness:** shared/public space where the player crosses them (steps, corridor) — NOT the player's private space.

Cross-ref `doctrine/03_arc_shapes.md` §5 for the peer/dating distribution (now including the ongoing hub).

---

## §7 — Pre-ship location self-audit (run before delivery)

- [ ] No canvas's `trigger.location` is an `is_container = true` location (§3).
- [ ] Geography layered: private-unit ≠ shared-building ≠ town; two top-level roots bridged by walk activities (§4).
- [ ] Every `navigation_order` slug has `entry_from` pointing back here (§4).
- [ ] Every `requires_npc` canvas: its location ∈ that NPC's `[[npcs.schedules]]` (§5.1).
- [ ] Every portrait hub (`npc =` set): that NPC is schedule-present at the hub's location (§5.2).
- [ ] Every NPC ambient/capstone passes the triad: NPC-schedule ∩ canvas-window ∩ player-likely-present-and-awake is non-empty, accounting for sleep/work/cross-midnight (§5.3).
- [ ] Every NPC scheduled at a locked (`entry_conditions`) location obeys the unlock contract (§5.4): the lock reads as "not met/invited," the NPC is meetable at an OPEN on-ramp, and the unlock flag has a reachable setter (that on-ramp beat). No NPC is reachable *only* via a locked location.
- [ ] Any locked secondary room an NPC routes into is legible + co-gated-or-off-hours + has open fallback presence — never a silent vanish during a window the player routinely shares (§5.4 Case B).
- [ ] Every peer/dating NPC has an ongoing Stage-4 hub, not just a first-night capstone (§6).
- [ ] Household NPCs are inside the private unit; neighbors/witnesses are in shared/public space, never the private unit (§4).

If any fail: fix BEFORE delivery. None of these are caught by the build validator today (see `PREVENTION_LINTER_SPEC.md` for the proposed engine-side catch).

---

## §8 — Cross-references

- `schema/02_toml_schema.md` §4 — `[[locations]]` field reference (`entry_from`, `parent`, `default_entry`, `is_container`, `navigation_order`).
- `schema/01_engine_capabilities.md` §5 — `getNpcLocation`, schedule presence (schedule-only, fail-closed).
- `reference/01_rts_overview.md` §6.5 — the live-verified RTS city-map location-lock model (discovery vs time axis) that §5.4 adapts.
- `doctrine/02_three_lanes_plus_capstone.md` §8.11 (dead presence — reachable) vs §8.15 (vanish into a locked room — unreachable).
- `doctrine/02_three_lanes_plus_capstone.md` — lane mechanisms (what attaches where).
- `doctrine/03_arc_shapes.md` §5 — peer/dating ongoing-hub footprint.
- `stages/01_game_book_prompt.md` §4 Step 3/4 — locations + schedules authoring.
- `stages/02_toml_generation_prompt.md` §10/§11 — anti-patterns + quality gate.
- `PREVENTION_LINTER_SPEC.md` — the build-time reachability checks that would catch §3 + §5 automatically.

---

**End of file.** A location graph that passes §7 is geographically coherent AND fully reachable. The build won't verify either for you — this checklist is the gate.

═══════════════════════════════════════════════════════════════════════════════

## 15. 11_clothing_design

**Source:** `prompts_v2/doctrine/11_clothing_design.md`

---

# Doctrine 11 — Clothing Design + Worn-State Predicates

**Sources:** Road-to-Success source extraction (364 passages, `game_explorations/road_to_success/passage_catalog.json`, verified June 2026 — clothing-gate conditions quoted verbatim below); Late Shifts clothing build (2026-05-31 / 06-01 — first prompts_v2 game to ship the system); TLS gold-standard catalog (`games/the_long_summer_test/toml_phases/1_metadata_and_locations.toml:616–`); engine code `apps/game_generation/twee_comprehensive/generators/v2.py` (`getWornStatMax`:1227, `checkLocationClothing`:1407) + `apps/projects/services/template_import.py` (settings read :2224, clothing items :2230).
**Authority:** Doctrine. What the clothing/wardrobe system should GATE, and how the three worn-state axes relate to global corruption. Schema lives in `schema/02_toml_schema.md` §12; this file is the design model.
**Purpose:** A game can wire clothing perfectly and still aim it at the wrong target. RTS uses clothing to drive PUBLIC/world content + a social gate + an exhibitionism meter — and NEVER to gate NPC arcs. Late Shifts initially gated an NPC's arc on the worn outfit (the backwards-on-ramp anti-pattern) and had to be re-aimed. This file encodes the verified RTS model so the next game gets it right the first time.

Cross-reference: `schema/02_toml_schema.md` §1.3 (`[settings]` enable switches), §12 (clothing items + requirements + `clothing_rules`); `doctrine/02_three_lanes_plus_capstone.md` §8.12 (backwards on-ramp); `doctrine/09_trait_catalog.md` (beauty + exhibitionism as distinct axes); `stages/02_toml_generation_prompt.md` Step 1 (`[settings]`) + Step 8 (clothing emission).

---

## §1 — The three worn-state axes (none feeds another)

Clothing in the RTS model is three independent stats plus the global-corruption spine. Keep them separate; collapsing any pair is the most common design error.

| Axis | What it is | Reads | Gates | RTS evidence |
|---|---|---|---|---|
| **worn corruption** | how revealing the *currently equipped* outfit is | live, MAX across equipped items (`getWornStatMax`, `v2.py:1227`); WEAN — never touches `player.corruption` | PUBLIC / world events | `ParkJog` `$player.clothing.corruption >= 15` (then `>= 30`); `BeachSunbathe` `> 30`; `Workout`/`PoolSwim` `>= 30`; `Library`/`NatashaPublicExhibitionism` `>= 30` |
| **beauty** | how *good* the outfit looks | live, MAX across equipped items | SOCIAL access / reception | `Club` `getBeauty() < 3` → bouncer refuses; `StripClubInterview` `getBeauty() == 0` → rejected; `ThomasPartyInvite` `getBeauty() >= 3` |
| **exhibitionism** | a persistent "how shameless am I" meter | a stored player trait, NO decay (monotonic) | flash payoffs, combined with corruption | `getExb()` raised by `<<AddExb>>` in flash acts; `StreetChallenge1` `getCorruptionLevel() >= 4 && getExb() >= 30`; `DiscountSex`/`BusRandomEvent` `getExb() >= 10` |
| **global corruption** (the spine) | the player's overall transgression | stored player trait | NPC arcs + the *right* to go out underdressed | `BrotherBedroom` sex `getCorruptionLevel() >= 3`; `Bedroom` "can't leave naked unless `getCorruptionLevel() >= 3`" |

**The rule:** worn corruption is a *live key* (take the outfit off, the door closes). Exhibitionism is a *ratchet* (acts raise it, it never falls). Global corruption is the *spine* everything else sits beside. Wearing a corruption-30 outfit raises `worn_corruption` to 30 but leaves global corruption untouched — verified live in RTS (the `Bedroom` guard treats `clothing.corruption` and `getCorruptionLevel()` as different quantities on the same line).

---

## §2 — Clothing gates PUBLIC content, NEVER NPC arcs (the load-bearing rule)

**Rule: an NPC's arc (notice / hub / escalation / sex) gates on global corruption + arousal + relationship + flags — never on what the player is wearing.**

RTS is unambiguous. Every family/romance hub gates sex with zero clothing checks:

- `MarcusBedroom`: `<<if isBoyfriend("Marcus")>>` … `<<if $player.arousal > 0>>`
- `BrotherBedroom`: `<<if getCorruptionLevel() >= 3>>` `<<if getArousal() > 0>>` `<<if $npc.Brother.relation >= 10>>`
- `DadBedroom` / `GrandpaBedroom`: `getCorruptionLevel() >= 3` / `>= 4`

None read `$player.clothing.*`. The outfit drives what happens *out in the world*; the people in your life respond to who you've *become* (corruption), not what you threw on this morning.

**Anti-pattern (the mistake Late Shifts made, then corrected):** gating an NPC's first-notice or hub on `worn_corruption` — e.g. a housemate who won't register the player until she's bought and worn provocative clothing. That is a **backwards on-ramp** (`doctrine/02` §8.12): the arc's front door is locked with a key found only by progressing a *different* system. Late Shifts' Ben B1a originally required `worn_corruption >= 15`; it was re-gated to `corruption >= 15` (global). If you catch yourself putting a `worn_*` predicate on a canvas whose `requires_npc`/`npc` field is set, stop — that beat belongs on a public surface, or the gate belongs on global corruption.

---

## §3 — `worn_corruption`: the live public-event key

**Rule: `worn_corruption` gates PUBLIC reactions — strangers, customers, passers-by — read live every render, granting zero global corruption (WEAN).**

- **MAX-aggregate, live:** the predicate returns the highest `corruption` among equipped items (`getWornStatMax`). Change clothes and the next render re-reads it. This is a *key you hold*, not a level you bank.
- **WEAN (Wardrobe-Effect-Adds-Nothing):** a `worn_corruption` beat is prose/flavor only — it must NOT carry `effects` that raise global corruption. The outfit routes content; corruption advances through the arc/economy, not through getting dressed.
- **Two-tier pattern (RTS `ParkJog`):** a first-notice tier (`>= 15`) and an overt tier (`>= 30`, Late-Shifts-scaled `>= 25`) on the same surface — glances/bigger tips at the low tier, open reaction at the high tier.
- **Where to host:** PUBLIC surfaces with an implied audience — the town street, a park, a shop, a workplace floor with customers. Never a private room, never an NPC arc canvas (§2).

Late Shifts consumers (worked example): diner-customer beat (15/30), town-street stares (25), park jogger (15), convenience-store clerk (25) — all `rts_public_clothing_*` in `5_scenes.toml`, all WEAN.

---

## §4 — `beauty`: the social key (distinct from corruption)

**Rule: `worn_beauty` gates SOCIAL reception and access — being treated well, being let in — not sexual content.**

Beauty and corruption are orthogonal: a put-together outfit can be high-beauty / low-corruption (a nice dress) or the reverse (something revealing but cheap). RTS gates *venues and welcome* on beauty (`Club`, `StripClubInterview`, `ThomasPartyInvite` all `getBeauty() >= 3`), and *exposure content* on corruption. Use beauty for: warmer NPC-stranger reception, entry to a nicer venue, a better tip class — the "she looks good tonight, the room is kinder" beat. Keep it off sexual gates; that's corruption's job.

Cross-ref `doctrine/09_trait_catalog.md`: beauty is outfit-derived (the `worn_beauty` predicate), not a stored trait — don't store it, or it desyncs when the player changes clothes.

---

## §5 — `exhibitionism`: the persistent meter

**Rule: exhibitionism is a stored player trait raised ONLY by public flash/expose ACTS, with NO decay; it then gates payoff content combined with global corruption.**

- **It needs no engine support** — it's an ordinary `[player.core_traits]` trait (declare it in `stages/02` Step 2). Raise it with a normal effect (`{ targetType = "player", trait = "exhibitionism", op = "add", value = N }`); gate on it with a normal `{ type = "trait", … trait_key = "exhibitionism" }` condition.
- **Monotonic — no daily decay.** RTS `getExb` only climbs (`<<AddExb>>`). Do NOT add it to `[engine.daily_tick]`.
- **Raised ONLY by acts, never by wearing.** This is the one place a clothing-adjacent choice mutates a stat: a *flash/expose ACT* (a deliberate choice on a public canvas, usually itself gated `worn_corruption >= 25` so she's dressed for it) grants `+exhibitionism`. Merely wearing revealing clothes raises `worn_corruption` (live) but NOT exhibitionism — the ratchet only turns when she *acts*.
- **Payoffs combine the meter with the spine (RTS `StreetChallenge1`):** bolder public content gates on `exhibitionism >= N AND corruption >= M`. A light payoff at `exb >= 10`, a bold one at `exb >= 30 && corruption >= 50`.

Late Shifts worked example: 2 flash acts (park bench, diner-3am; require `worn_corruption >= 25`, grant `+10 exhibitionism`) + 2 payoffs (`exb >= 10` recognition; `exb >= 30 && corruption >= 50` dare, `+15`).

Cross-ref `doctrine/09_trait_catalog.md` §5.3 — exhibitionism is already catalogued as a distinct axis from corruption (high-corruption + low-exhibitionism = sexually active but private; the reverse = loves being seen, not yet active).

---

## §6 — Coverage gate: conditional on global corruption, not pure slots

**Rule: "can't go out underdressed" gates on global corruption LEVEL — once corrupt enough she leaves without shame (RTS `Bedroom` parallel) — not on a flat slot requirement.**

RTS blocks leaving home naked/underwear only below a corruption level (`Bedroom`: naked needs `getCorruptionLevel() >= 3`, underwear `>= 2`). Mirror this with a **single** per-location `clothing_rule` carrying a `conditions` block that applies the cover-up requirement *only below* a threshold:

```toml
clothing_rules = [
  { slots_required = ["top", "bottom"], message = "She can't head out half-dressed.", conditions = { version = "1.0", items = [
      { type = "trait", subject = "player", trait_key = "corruption", operator = "lt", value = 50 },
    ] } },
]
```

Below 50 the rule applies (must cover up); at 50+ its condition fails, `checkLocationClothing` finds no active rule and returns null (she leaves freely).

**Validator gotcha:** `slots_required` must be NON-EMPTY (`template_import.py:3460` rejects `[]`). Do NOT express this as a two-rule empty-fallback (`{ slots_required = [], conditions = … }` + a cover-up rule) — the empty list fails validation. The single conditional rule above is the correct form. A `dress` satisfies both `top` and `bottom`. Gate the TOWN entry this way; leave home interiors ungated so robe/underdressed teases survive.

---

## §7 — Tiering & economy

**Rule: catalog tiers map to the corruption arc and are priced to the game's wage; the starting outfit covers every slot.**

| Tier | Gate | beauty | corruption | price | purpose |
|---|---|---|---|---|---|
| Starting outfit | `initial = true`, free | 0–2 | 0–5 | 0 | full slot coverage so the player is NEVER naked/blocked at game start |
| Basic | ungated | 2–4 | 5–12 | cheap (1–2 shifts' wage) | everyday nicer pieces |
| Going-out | ungated | ~4 | **15–20** | low-mid | the load-bearing tier: makes `worn_corruption >= 15` public events reachable EARLY, before the player has ground much global corruption |
| Revealing | buy-gated on global `corruption >= N` | 4–5 | 25–35 | mid-high (multi-shift save) | the overt tier; the buy-gate ties acquisition to the arc |

The going-out tier is what TLS lacked and Late Shifts added: without an *ungated* item at `worn_corruption 15–20`, every public clothing event is locked behind buying the gated tier, which is itself locked behind corruption — a soft backwards-on-ramp on the clothing system itself. Always seed it. Price the whole catalog against the game's income (Late Shifts: $60 start, $45/shift, $125 rent → basics affordable in 1–2 shifts, revealing tier a multi-shift save). The buy-gate uses item `conditions` (global corruption), distinct from the live `worn_*` predicates that gate content.

Late Shifts worked example: 20 items — 6 starting (free, full coverage) / 6 basic / 3 going-out (worn_corruption 15–20, ungated) / 5 revealing (buy-gated `corruption >= 25`).

---

## §8 — Enabling checklist + the scoping trap

The system is OFF until `[settings]` turns it on, and the switches are a **silent-failure trap** if mis-scoped.

- [ ] **`[settings]` table, NOT bare keys.** `clothing_enabled` / `wardrobe_location` / `shop_location` live under a `[settings]` header (read at `template_import.py:2224`). Authored bare (e.g. right after `[time]`), they scope under the preceding table, `data["settings"]` is empty, and clothing reads as **disabled with no error**. This silently shipped a dead clothing system in Late Shifts for a full session. (`schema/02` §1.3.)
- [ ] **Items exist.** `clothing_enabled = true` with zero `[[clothing]]` items = empty wardrobe/shop pages + all `worn_*` read 0. The importer does NOT warn. Author the catalog (§7).
- [ ] **Full starting outfit** — every slot has an `initial = true` item, so the player is never naked/blocked and the coverage gate (§6) is satisfiable from turn one.
- [ ] **Wardrobe + shop locations exist and are player-navigable** — `wardrobe_location` / `shop_location` slugs must be real `[[locations]]` (the engine injects the wardrobe/shop page there; a non-navigable or missing location = dead UI).
- [ ] **Every `worn_*` consumer is on a PUBLIC surface** (§3) and is WEAN (no global-corruption effect); zero `worn_*` predicates on NPC-arc canvases (§2).
- [ ] **`clothing_requirements` + `clothing_rules`** under `[settings]` / per-location respectively (§6); coverage gate conditional on corruption, non-empty `slots_required`.
- [ ] If exhibitionism is used: the trait is declared in `[player.core_traits]`, has a sidebar item, and is NOT in the daily tick (§5).

---

## §9 — Cross-references

- `schema/02_toml_schema.md` §1.3 — `[settings]` enable switches (the scoping fix).
- `schema/02_toml_schema.md` §12 — `[[clothing]]` items, `[settings.clothing_requirements]`, per-location `clothing_rules`.
- `schema/03_example_toml.md` — verbatim clothing excerpt (enabling `[settings]` + catalog + public event + flash act).
- `doctrine/02_three_lanes_plus_capstone.md` §8.12 — backwards on-ramp (the NPC-gated-on-outfit anti-pattern).
- `doctrine/09_trait_catalog.md` — beauty (outfit-derived) + exhibitionism (distinct from corruption).
- `stages/02_toml_generation_prompt.md` Step 1 (`[settings]`) + Step 8 (clothing emission).
- `reference/04_rts_hud_world_model.md` — RTS Outfit string + beauty/exhibitionism HUD bars.

---

**End of file.** A clothing system that passes §8 is enabled correctly and aimed correctly: it drives the world and the player's public reputation (§3–§5), gates going-out on who she's become (§6), and leaves the people in her life responding to corruption + arousal + relationship — never to what she's wearing (§2).

═══════════════════════════════════════════════════════════════════════════════

## 16. 12_rent_economy_design

**Source:** `prompts_v2/doctrine/12_rent_economy_design.md`

---

# Doctrine 12 — Rent & Economic-Pressure Design

**Sources:** Engine code `apps/game_generation/twee_comprehensive/generators/v2.py` (rent state `:1126`, due trigger in `advanceDay` `:4811`, render intercept `:13849`, `RentDay` / `RentDay_Paid` / `RentDay_Short` passages `:14242–14379`) + `apps/projects/services/template_import.py` (read `:2382`, validator `:4167`); TLS gold-standard `[settings.rent]` (`games/the_long_summer_test/toml_phases/1_metadata_and_locations.toml:634`) + its hybrid first-Sunday capstone; Late Shifts rent build (2026-06-01 — Vince the landlord, the first prompts_v2 game to ship rent correctly scoped); Phase-2 design docs (`28th_april_TLS_Phase2_Redesign/30_TLS_Test_Redesign_PRD.md` §"economic engine", `10_Test_Slice_10Day_Plan.md` slice math, `11_Hint_Authoring_Guide.md` rent-crisis hint).
**Authority:** Doctrine. WHEN to use rent, how to aim it, and how to tune it. Schema lives in `schema/02_toml_schema.md` §14; this file is the design model.
**Purpose:** Rent is the simplest engine for the RTS "I Need Money" drive — but it's easy to wire it so it never fires (the scoping trap), fires too early (onboarding eviction), ends the game when you wanted leverage (wrong eviction mode), or asks for money the player can't earn yet (untuned budget). Late Shifts shipped rent mis-scoped and silently OFF for a full session. This file encodes the verified model so the next game gets it right.

Cross-reference: `schema/02_toml_schema.md` §1.3 (`[settings.rent]` enable switch), §14 (field tables + runtime flow); `schema/03_example_toml.md` §13 (verbatim worked block); `doctrine/11_clothing_design.md` §8 (the same `[settings]` scoping trap); `doctrine/01_rts_principles.md` (the money drive); `stages/02_toml_generation_prompt.md` Step 1 (`[settings.rent]` emission).

---

## §1 — Rent is the economic spine (the player's drive)

**Rule: use rent when you want a recurring, dateable money obligation that FORCES engagement with the income arcs — it is the "I Need Money" opener made mechanical.**

RTS opens every run with money pressure: the player needs cash, so they go out and engage the world. TLS adopted this directly — *"Rent is due monthly. Maya must find money OR have someone pay her rent OR leave town. This is the player drive."* (`30_TLS_Test_Redesign_PRD.md` §"economic engine"). Rent converts a soft suggestion ("you could work") into a hard clock ("Friday, $125, or else"). That clock is what makes the income channels — jobs, NPC favors, the corruption economy — matter.

Use rent when the game has: a place to live, a way to earn, and a reason the player can't just ignore money. Skip it for games with no economy or where money isn't the drive (a pure relationship sandbox). Rent is one expression of economic pressure; a game can instead lean on savings goals, debts, or purchase-gated progression — but when the drive is "keep a roof over your head," rent is the built-in system.

---

## §2 — What the engine gives you for free

The engine ships the entire rent loop; you author config + prose, not logic. (Full schema: `schema/02` §14.)

- **The clock.** On each day rollover, when the in-game weekday hits `due_day` and `start_after_flag` (if set) is satisfied, rent comes due (once/week). *As of 2026-06-01 the engine respects `due_day`* — earlier it ignored it and always fired Monday. Set `due_day` to a real day and frame the prose around it.
- **The intercept.** While rent is due, the player is redirected to the `RentDay` passage before they can do anything else — money pressure you can't click past.
- **The branch.** `RentDay` → pay (`RentDay_Paid`) or short (`RentDay_Short`). Short within grace = a warning and the week is survived; short past grace = eviction.
- **The collector.** If `collector_npc` is set, RentDay shows that NPC's name + portrait (§6).
- **The prose.** Every beat has an author override via `[settings.rent.text]` (§14.3) — use it; the defaults are generic.

What the engine does NOT give you: a "first rent paid" flag, a quest card, or any first-time framing. Those are authoring (§7).

---

## §3 — The arm-after pattern (`start_after_flag`)

**Rule: arm rent only AFTER the player has a way to pay — set `start_after_flag` to an income flag so onboarding is rent-free.**

A fresh player has the starting balance and no income yet. If rent arms on the first due day, you can evict someone before they've had a chance to earn — a frustration, not a drive. `start_after_flag` defers the entire cycle until that flag is set:

- **Late Shifts:** `start_after_flag = "hired_at_diner"`. Rent is dormant until Maya gets the job; the first Friday after hire is the first due date. Onboarding (find the diner, get hired) happens with no rent clock ticking.
- **TLS:** `start_after_flag = "first_sunday_passed"`, set by a scripted first-Sunday capstone (§7).

Leave `start_after_flag` empty only if the player can pay from turn one (rare). The flag must actually get set somewhere reachable — an income/onboarding flag the player will hit naturally.

---

## §4 — `eviction_mode`: game_end vs flag_set (the decision rule)

**Rule: choose the eviction mode by what failure should MEAN in your game. `game_end` = the run is over. `flag_set` = the world changes and play continues. Both are first-class; pick deliberately.**

| Mode | What happens | Use when | Cost |
|---|---|---|---|
| `game_end` | GAME OVER screen + restart | failure is terminal — a roguelike/survival framing where losing the roof ends the story | a hard wall; the player loses progress |
| `flag_set` | sets `eviction_flag` (e.g. `rent_evicted`), play continues | failure should have *narrative* consequence, not a wall — the landlord's leverage, a downgrade, a debt, a different arrangement | you must author what the flag DOES downstream (fail-forward) |

`flag_set` is the richer choice for an arc-driven adult game: missing rent doesn't kick the player out, it hands the collector leverage. The engine supports this with **`_soft` text variants** (`eviction_scene_soft` / `_response_soft` / `_closing_soft`) that play instead of the hard-eviction prose — write them to open the consequence, not close the game. Late Shifts uses `flag_set` so Vince's missed-rent beat becomes *"Money's one way to keep a roof. There's others."* — a leverage hook the arc can pick up. TLS likewise uses `flag_set` (`rent_evicted`).

If you pick `flag_set`, the `eviction_flag` is a real promise: author at least one downstream beat that reads it, or eviction is a dead end dressed as a consequence.

---

## §5 — Budget math: price rent to the wage

**Rule: `amount` must be clearable by the first post-arm due date with margin — tune it against the income channels, not in a vacuum.**

Rent that can't be paid isn't pressure, it's a scripted loss. Before setting `amount`, count: starting balance, income per channel, and how many earning opportunities fall between the arm flag and the first due date.

- **Late Shifts:** $60 start, +$45/diner shift, rent $125 due Friday, armed at hire. Between a Monday hire and Friday there are ~3–4 shifts (135–180) — clears 125 with margin; `grace_periods = 1` is the backstop for a bad week.
- **TLS (`10_Test_Slice_10Day_Plan.md`):** $60-equivalent weekly rent against two income channels + a comfortable starting buffer, explicitly checked so "rent fires correctly" without being a wall.

`grace_periods` is the tension dial: 0 = a single miss evicts (brutal); 1–2 = a bad week is recoverable, a pattern is not. Higher grace softens the clock. Tune `amount` and `grace_periods` together against the wage; verify the first due date is winnable in a live-play.

---

## §6 — `collector_npc`: give rent a face

**Rule: route rent through an NPC (`collector_npc`) so the obligation has a person behind it — and, under `flag_set`, a relationship that can be leveraged.**

A faceless "the landlord" works, but a named collector turns a number into a scene. RTS, TLS (Frank — rent collector AND romance arc), and Late Shifts (Vince — the building landlord) all put a person at the door. The collector's voice carries the pressure (`[settings.rent.text]` in their register), and under `flag_set` the missed-rent leverage flows naturally into their arc — Frank's rent terms feed his arc; Vince's "there's others" opens one.

`collector_npc` is an NPC slug that **must exist in `[[npcs]]`** (validator, `template_import.py:4174`). The collector does not need a schedule for RentDay to work (the passage looks them up by slug for name + portrait), but giving them light presence (a schedule window where the player can meet them) makes the rent knock land as a known face rather than a stranger — Late Shifts schedules Vince out front mornings for exactly this.

---

## §7 — The hybrid first-period pattern + surfacing the pressure

**Rule: when the first rent payment carries plot weight, hand-author it as a one-shot capstone that also sets `start_after_flag`; let the engine handle every recurring week after.**

The engine's recurring rent is uniform by design — same RentDay scene weekly. The *first* time often deserves more: an establishing beat, a choice, a flag set for downstream content. The hybrid pattern (TLS):

1. A one-shot capstone (`canvas_first_sunday_morning`) delivers the first rent narratively and sets `first_sunday_passed`.
2. `start_after_flag = "first_sunday_passed"` arms the engine — so recurring rent begins the *next* week.
3. The capstone can also set a `first_rent_paid` flag (the engine won't) for hints/branches.

Skip the hybrid (arm on a plain income flag, like Late Shifts' `hired_at_diner`) when the first payment is just the first of many.

**Surface the pressure.** Rent off-screen is weak pressure. Make it visible: a money sidebar band ("Making rent"), and — for the V2 quests engine — a rent-crisis hint that fires while rent is unpaid and softens once it's cleared (`11_Hint_Authoring_Guide.md`: a global/no-`npc_id` hint gated on `missing_flag = "first_rent_paid"` renders in the Story-Goals section). The player should always know the clock is running.

---

## §8 — Enabling checklist + the scoping trap

Rent is OFF until `[settings.rent]` turns it on, and the switch is a **silent-failure trap** if mis-scoped (the same trap as clothing, `doctrine/11` §8).

- [ ] **`[settings.rent]` table, NOT bare keys.** `enabled` / `amount` / etc. live under a `[settings.rent]` header (read at `template_import.py:2382`). Authored bare (e.g. right after `[time]` as `rent_enabled = true`), they scope under the preceding table, `data["settings"]["rent"]` is empty, and rent reads as **disabled with no error**. This silently shipped a dead rent system in Late Shifts. (`schema/02` §1.3.)
- [ ] **Correct key names.** `enabled` / `amount` / `due_day` / `grace_periods` — NOT `rent_enabled` / `rent_amount` / `rent_due_day`. A verbatim move of the bare keys still fails; rename them.
- [ ] **`amount > 0`** and **`due_day`** is a full weekday name (validator).
- [ ] **`collector_npc` exists** in `[[npcs]]` if set (§6, validator).
- [ ] **`start_after_flag` is reachable** — armed by a flag the player will actually set (§3); empty only if payable from turn one.
- [ ] **`eviction_mode` chosen deliberately** (§4); if `flag_set`, the `eviction_flag` has at least one downstream consumer (and `_soft` text authored).
- [ ] **`[settings.rent.text]` authored** as a SUB-table (not a multi-line inline table — breaks `tomllib`), using the real keys (`schema/02` §14.3).
- [ ] **Budget tuned** — first post-arm due date is clearable with margin against the income channels (§5); verified in a live-play.

---

## §9 — Cross-references

- `schema/02_toml_schema.md` §1.3 — `[settings.rent]` enable switch (the scoping fix).
- `schema/02_toml_schema.md` §14 — `[settings.rent]` field tables + runtime flow + `[settings.rent.text]` keys.
- `schema/03_example_toml.md` §13 — verbatim rent excerpt (`[settings.rent]` + `[settings.rent.text]` + the hybrid pattern).
- `doctrine/11_clothing_design.md` §8 — the identical `[settings]` scoping trap.
- `doctrine/01_rts_principles.md` — the "I Need Money" money drive rent serves.
- `stages/02_toml_generation_prompt.md` Step 1 — `[settings.rent]` emission.
- `28th_april_TLS_Phase2_Redesign/30_TLS_Test_Redesign_PRD.md` §"economic engine"; `10_Test_Slice_10Day_Plan.md` (slice math, F4 rent test); `11_Hint_Authoring_Guide.md` (rent-crisis hint).

---

**End of file.** A rent system that passes §8 is enabled correctly and aimed correctly: it gives the player a dateable money clock (§1–§2), holds off until they can pay (§3), fails in the way the story needs (§4), asks for an amount they can earn (§5), wears a face (§6), and stays visible on screen (§7).

═══════════════════════════════════════════════════════════════════════════════

## 17. 13_phone_design

**Source:** `prompts_v2/doctrine/13_phone_design.md`

---

# Doctrine 13 — Phone & Apps Design

**Sources:** Engine code `apps/game_generation/twee_comprehensive/generators/v2.py` (phone init `:995–1102`, `$game_state.phone` state `:1147`, delivery scan `setup.checkPhoneConversations` `:1659`, thread grouping `getPhoneThreads` `:1722`, chat render `openChatThread` `:1972`, reply effects `sendPhoneReply` `:1772`, daily-chat/photo `sendDailyChat` `:1844`, social feed `:2165`, dating `:2268`, gallery `:2410`, sidebar button widget `phoneButton` `:14695`, **trigger evaluator `triggerConditionsSatisfied` `:3308`**) + `apps/projects/services/template_import.py` (read `:2394–2517`, `TemplatePhone` dataclass `:286`); TLS gold-standard `[phone]` (`games/the_long_summer_test/toml_phases/7_final_game.toml` — 9 threads + small-talk + photo actions); Late Shifts phone build (2026-06-02 — `games/late_shifts/toml_phases/8_phone.toml`, the first prompts_v2 game to ship a phone); Phase-2 design docs (`28th_april_TLS_Phase2_Redesign/42_RTS_Phone_System_Reference.md`, `43_Engine_Phone_System_Reference.md`, `44_RTS_Phone_Parity_Gap_PRD.md`, `45` parity build, `46_TLS_Phone_Design.md`); a live re-play of RTS (road-to-success v0.26) confirming the device model.
**Authority:** Doctrine. WHEN to use the phone, which app types to reach for, and how to wire threads so they actually fire. Schema lives in `schema/02_toml_schema.md` §13; this file is the design model.
**Purpose:** The engine ships a complete phone (Doc 45 implemented all 12 RTS-parity gaps), but it's easy to wire so the button never appears (the scoping trap), threads never dispatch (dead-flag triggers), or a reminder uses a condition type the evaluator doesn't support (the `day`/`time` trap). This file encodes the verified model.

Cross-reference: `schema/02_toml_schema.md` §1.3 (`[phone]` enable switch), §13 (field tables + the trigger-condition vocabulary); `schema/03_example_toml.md` §14 (verbatim worked block); `doctrine/11_clothing_design.md` §8 + `doctrine/12_rent_economy_design.md` §8 (sibling scoping traps); `doctrine/01_rts_principles.md` (earned progression); `stages/02_toml_generation_prompt.md` Step 1 (`[phone]` emission).

---

## §1 — The phone is the digital surface (RTS parity)

**Rule: use the phone when the world has off-location interactions — texts, posts, a digital economy — that should reach the player anywhere, on a daily cadence, gated by the same corruption spine as the rest of the game.**

RTS makes the phone a second world layer: a purchased device (a $400 item; the sidebar button appears only once owned — re-verified live on v0.26) holding Messages, a follower economy, fast jobs, a bank, a gallery, and a quest journal. Its threads are instanced by a daily dispatch tick and gated by relationship + corruption + day state; 52 NPCs each carry `relation / corruption / arousal / talkedToday`, so corruption is the escalation spine and `talkedToday` the daily-cadence throttle (Doc 42; live source inspection). The engine reproduces this model with TOML primitives (Doc 43/45).

Use the phone when: NPCs would plausibly text; the game has a follower/job/bank economy worth a screen; or escalation wants a private channel (lewd photos, an anonymous watcher) parallel to in-location scenes. Skip it for a single-location game with no off-screen life. The phone is a *surface*, not an arc — it carries arcs authored elsewhere into a place the player checks between scenes.

---

## §2 — What the engine gives you for free

You author config + content; the engine owns all the logic (full schema: `schema/02` §13).

- **The device + gate.** A sidebar 📱 button renders when `enabled` is true AND (`purchase_flag` is empty OR `flags[purchase_flag]` is set). Unread count shows as a badge. (`:14695`.)
- **Delivery.** `checkPhoneConversations()` runs every passage render: it scans conversations/posts/profiles, marks any whose `trigger` is now satisfied, and (after a baseline first scan) fires a toast using the item's `notify` string (`:1659`). No author loop needed — content arrives when its conditions go true.
- **Threads.** Chat apps group conversations by NPC into threads (name + portrait + unread), newest-first (`:1722`). Each thread renders its blocks as bubbles + reply buttons, with a typing animation for pending NPC messages (`:1972`).
- **Reply effects.** A reply choice applies `effects` (traits), `flagEffects`, `questEffects`, `scheduleEffects`, shows a toast, and re-renders (`:1772`) — the same effect primitives as canvas choices.
- **Small-talk + photo actions.** `daily_topics` give repeatable per-day chat with cooldown + corruption gating (`:1844`).
- **Other apps.** social_feed (read + player posting), dating (swipe/match), gallery, custom (renders a passage), quests, fast_jobs, bank — all author-configured (Doc 45).
- **Persisted state** in `$game_state.phone` (triggered/read/replies/posts/profiles/matches) + `daily_chats` (`:1147`).

What the engine does NOT give you: a day-of-week trigger (§4), validation of reply-effect field names (author them correctly), or any thread that reads rent's `is_due` state (§4).

---

## §3 — Chat-thread design (trigger on REAL flags)

**Rule: trigger every conversation on a condition that actually goes true in your game — an arc flag with a verified setter, or a trait threshold — or the thread is dead weight that never dispatches.**

A conversation's `trigger.conditions` decides when it arrives. The single most common failure is triggering on a flag nothing sets (the dead-flag trap, same as canvas triggers). Author threads against the arc flags you already set:

- **TLS:** threads gate on `frank_caught`, `jake_peek_draw_revealed`, `ryan_partner_open` — real arc-stage flags. The anonymous watcher gates on raw `corruption gte 45` (a trait, not a flag) so it surfaces from player state alone.
- **Late Shifts:** Cole/Hank/Ben threads gate on `cole_noticed`, `hank_first_contact`, `ben_consummation_done`, etc. — each a verified setter in the arc.

Thread shape:
- **Multi-round.** Blocks carry `round`; a `reply` block presents choices; later `message` blocks gate on `after_round` + `after_choice` to branch on what the player picked. Keep branches short — a thread is a text exchange, not a scene.
- **Effects match the NPC's traits.** A reply effect must target a trait the NPC actually has. Cole (relation only) gets `relation` effects; Hank/Ben (arousal) can get `arousal`; only corruption-bearing NPCs get `corruption`. A phantom-trait effect is silent noise.
- **Register.** Threads are mostly one-shot (the engine marks them read), so they can carry a little more texture than a re-readable hub — but stay in the NPC's voice and keep it terse; texts aren't prose passages (`doctrine/05`).

---

## §4 — Trigger condition vocabulary (the `day`/`time` trap)

**Rule: phone triggers use ONLY the types the `triggerConditionsSatisfied` evaluator supports. It does NOT support day-of-week or clock time. For time-relative delivery use `days_since_flag`.**

This is the section that prevents a real, easy-to-make bug. The phone (and posts, profiles, daily_topics) all evaluate triggers through `triggerConditionsSatisfied` (`v2.py:3308`). Source-verified supported `items[].type`:

`flag` · `trait` · `days_since_flag` · `pass` · `item` · `stage` · `quest` · `corruption_level` · `modifier` · `clothing_slot` · `clothing_item` · `worn_beauty` · `worn_corruption` · `worn_type`

**NOT supported here: `day`, `time`, `weekday`, `location`, `random`.** Those exist only in the *canvas* trigger path, not the phone evaluator. Do not author a phone thread that fires "on Friday" or "at night" — it will never match.

For time-relative content, use **`days_since_flag`**: it fires N days after a flag's recorded `set_day` (`{type="days_since_flag", subject="player", flag_key="hired_at_diner", operator="gte", value=4}`). Late Shifts uses exactly this for Vince's rent nudge — phone triggers can't read rent's live `is_due` state, so a "Friday's close" reminder lands ~4 days after hire (near the first rent week) via `days_since_flag`, and the eviction consequence thread gates on the real `rent_evicted` flag. That is the honest substitute for a day-of-week trigger.

(Historical note: earlier corpus drafts listed `day`/`time`/`location`/`random` as phone condition types. They are fictional for this path — corrected 2026-06-02 against source.)

---

## §5 — Small-talk vs photo quick-actions (`daily_topics`)

**Rule: `daily_topics` is the repeatable side-channel — low-stakes chatter and corruption-gated photo actions, never a capstone. Tier photo actions by `corruption_min`; throttle each with `cooldown`.**

`daily_topics` are the phone's everyday texture, distinct from one-shot conversations:

- **Small-talk:** `player_message` + `npc_response` + small `effects` (relation ±1), gated by an arc flag, default cooldown = once per NPC per day. Ambient warmth, not plot.
- **Photo quick-actions:** the same primitive with `cooldown = "per_topic"` (each action its own 1/day cap, so selfie + lewd + nude can each fire once daily) and `corruption_min` tiers. The RTS-faithful ladder is **selfie (no gate) → lewd (`corruption_min = 45`) → nude (`corruption_min = 85`)** (Doc 45 G3; TLS + Late Shifts both use it). Tiers telegraph: a locked action shows the requirement, so the player sees the next rung. Effects climb with the tier (player arousal/corruption + NPC arousal), and — as in §3 — only target traits the NPC carries.

Photo actions are the chat-side analogue of RTS's sendSelfie/sendLewd/sendNude. They are escalation surfaces, not story beats; the story beats they reward live in the canvases.

---

## §6 — App-type decision rule

**Rule: reach for the smallest app set that carries the game's off-location life. Most arc-driven adult games are chat-centric — one `chat` app is often the whole phone.**

Valid `type`s (`schema/02` §13.2): `chat` · `social_feed` · `dating` · `gallery` · `custom` · `quests` · `fast_jobs` · `bank`.

| App | Use when | Skip when |
|---|---|---|
| `chat` | NPCs text; private escalation; the default phone surface | almost never (this is the core) |
| `social_feed` | a follower/reputation economy (post selfie/lewd/nude → followers via `post_actions`) is a real drive — the Instafame fantasy | no fame arc; it becomes an empty wall |
| `dating` | meeting NPCs via swipe/match is a mechanic, not just narrated | the cast is fixed and met in-world |
| `gallery` | unlocked media is a collectible reward track | no media-reward loop |
| `custom` | a bespoke screen (renders an author passage) | a standard app fits |
| `quests` | the V2 quest journal should live on the phone | quests surface elsewhere |
| `fast_jobs` / `bank` | the money economy wants in-phone jobs + interest (RTS-scale) | rent + a sidebar money band is enough |

RTS surfaces six apps on its home grid (Messages, Quests, Fast Jobs, Statistics, Gallery, Bank — live v0.26; Instafame/xCam are laptop/feature subsystems). TLS and Late Shifts deliberately ship **chat only** (Doc 46): a trapped corruption slice has no fame economy or job-board fantasy, so the social_feed/dating/jobs/bank apps would be empty rooms. Match the app set to the game's actual systems — an app with no content reads as broken.

---

## §7 — `purchase_flag`: the acquisition beat (earned device)

**Rule: gate the phone behind `purchase_flag` so the device is *acquired*, not assumed — RTS-faithful earned-progression pacing. The flag needs exactly one reachable setter.**

In RTS the phone is bought ($400); the sidebar button doesn't exist until you own it. The engine models this with `purchase_flag`: the button is hidden until `flags[purchase_flag]` is set. This gives a deliberate "phone arrives" moment instead of a phone from frame one.

- **TLS / Late Shifts:** `purchase_flag = "phone_active"`, set at the diner hire — the cut-off phone reconnects once there's income. One setter, on the hire choice.
- Like any `is_true` flag, `purchase_flag` must have a setter the player will hit (the same rule as every gate flag, `doctrine/04`). Leave `purchase_flag` empty only if the phone should be present from the start (rare for RTS-style pacing).

The acquisition beat is also a natural pacing gate for everything on the phone: threads authored against early arc flags simply won't have a surface until the phone is active, which is usually what you want (the device and the first arcs arrive together).

---

## §8 — Enabling checklist + the scoping trap

The phone is OFF until a `[phone]` table turns it on, and the switch is a **silent-failure trap** if mis-scoped (the same family as clothing `doctrine/11` §8 and rent `doctrine/12` §8).

- [ ] **Top-level `[phone]` table, NOT a bare key, NOT under `[settings]`.** `enabled` lives under a `[phone]` header (read at `template_import.py:2394`; defaults true when the table is present). A bare `phone_enabled` key is dead config the importer never reads — it silently shipped a phoneless Late Shifts until 2026-06-02. (Clothing → `[settings]`, rent → `[settings.rent]`, phone → `[phone]`: three systems, three different homes.)
- [ ] **At least one `[[phone.apps]]`** with a valid `type` (§6); conversation `app` fields reference an app `id`.
- [ ] **Every conversation `trigger` is satisfiable** — flags have verified setters; no `day`/`time`/`location`/`random` types (§3, §4).
- [ ] **`days_since_flag` for time-relative delivery**, not a day-of-week condition (§4).
- [ ] **Reply/topic effects target real traits** — present on that NPC (§3); the player's `corruption`/`arousal` exist; no phantom traits.
- [ ] **`conversations[].npc` exists in `[[npcs]]`** (name + portrait come from the NPC).
- [ ] **Photo actions tiered + throttled** — `corruption_min` ladder, `cooldown = "per_topic"` (§5).
- [ ] **`purchase_flag` has exactly one reachable setter** (§7); empty only if the phone is present from turn one.
- [ ] **App set matches the game's systems** — no empty social_feed/dating/jobs apps (§6).

---

## §9 — Cross-references

- `schema/02_toml_schema.md` §1.3 — `[phone]` enable switch (the scoping fix).
- `schema/02_toml_schema.md` §13 — `[phone]` field tables + the trigger-condition vocabulary (§13.3).
- `schema/03_example_toml.md` §14 — verbatim phone excerpt (`[phone]` + thread + `days_since_flag` + photo action + the purchase gate).
- `doctrine/11_clothing_design.md` §8 / `doctrine/12_rent_economy_design.md` §8 — the sibling `[settings]`/`[settings.rent]` scoping traps.
- `doctrine/01_rts_principles.md` — earned progression + the corruption escalation spine the phone rides.
- `stages/02_toml_generation_prompt.md` Step 1 — `[phone]` emission.
- `28th_april_TLS_Phase2_Redesign/42_RTS_Phone_System_Reference.md` (RTS target), `43` (engine as-built), `44` (parity gaps G1–G12), `45` (parity build), `46` (TLS chat-centric design).

---

**End of file.** A phone that passes §8 is enabled correctly and aimed correctly: it gives off-location life a surface (§1–§2), delivers threads that actually fire on real flags (§3), uses only the conditions the evaluator supports (§4), throttles its repeatable actions and tiers them by corruption (§5), ships only the apps the game's systems justify (§6), and arrives as an earned device (§7).

═══════════════════════════════════════════════════════════════════════════════

## 18. 14_customization_design

**Source:** `prompts_v2/doctrine/14_customization_design.md`

---

# Doctrine 14 — Player & NPC Customization Design

How to let the player personalize themselves and the cast at game start — name, build,
look, NPC names, NPC relationship labels — and, critically, how to make those choices
actually **show up** in the writing. Sibling of [doctrine/11 clothing], [doctrine/12 rent],
[doctrine/13 phone]: another free engine surface that ships fully built but is easy to
half-use (declare the inputs, forget the output token).

The engine is fully shipped — importer `template_import.py:62–89` (player) / `:107–117`
(NPC), validator `:2906–2943` / `:3289–3304`, runtime `v2.py:8376` (the auto-built
`CustomizeCharacters` passage) + `v2.py:12658` (the `@`-token processor). **No engine
change is needed to use it.**

---

## §1 — What it is (and the RTS parallel)

Two independent surfaces, both opt-in:

- **Player customization** — a start-of-game screen where the player sets fields you
  declare (`name`, `build`, a portrait `look`, anything). RTS-of-this-genre games open on
  exactly this: name yourself, pick a body type, choose a starting look.
- **NPC customization** — per-NPC, the player can **rename** the character and pick a
  **relationship label** from a list you supply (e.g. `step-dad` / `mom's boyfriend` /
  `landlord`). This is the genre's relationship-toggle: the same arc, reframed as a
  step-brother *or* a roommate, by the player's choice.

The screen is **auto-generated and auto-wired**. If any `[player].customizable = true`
field or any `customizable` NPC exists, the engine inserts a `CustomizeCharacters` passage
and redirects `Start` to it (`v2.py:830–837`). You author **zero** passage plumbing — you
declare the fields and write the prose with tokens.

---

## §2 — The free engine features

| Feature | Declared in | Renders as |
|---|---|---|
| Player text field (name, etc.) | `[[player.customization_fields]]` `type="text"` | a textbox |
| Player choice field (build, etc.) | `type="select"` + `options` | a dropdown |
| Player portrait picker | `type="image_select"` + `options` + `sets_portrait` | an image grid; the pick can become `$player.portrait` |
| NPC rename | NPC `customizable = true` | a textbox seeded with the default name |
| NPC relationship label | NPC `relationship` + `relationship_options` | a dropdown |

A `text`/`select` value lands in `$player.<field_id>`. `id = "name"` is special — it writes
`$player.name` (the canonical name the whole engine reads). An NPC's chosen name lands in
`$npcs[uuid].name`, the relationship in `$npcs[uuid].relationship`.

---

## §3 — The `@`-token contract (the part everyone forgets)

Declaring the fields is half the job. A customized value only *appears* in the story if you
write the prose with the substitution token. **There is exactly one token syntax**, processed
at generation time (`_resolve_at_references`, `v2.py:12658`):

| Token in your prose | Becomes | Reads |
|---|---|---|
| `@player` | `<<print $player.name>>` | the player's chosen name |
| `@player.<field>` | `<<print $player.<field> \|\| "">>` | any player field (e.g. `@player.build`) |
| `@<npc_short>` | `<<print $npcs["uuid"].name>>` | that NPC's chosen name |
| `@<npc_short>.rel` | `<<print $npcs["uuid"].relationship \|\| "">>` | that NPC's relationship label |

`<npc_short>` is the NPC slug **without** the `npc_` prefix — `@cole` for `npc_cole`,
`@frank` for `npc_frank`. An unrecognized `@word` is left untouched (so it's safe to write
literal `@`s — but see §6 on the handle collision).

**Possessives and punctuation just work:** `@cole's place` → `<<print …name>>'s place`
→ "Jamie's place". Dialog speaker labels are already dynamic (they render from `npcId`), so
you only tokenize the *body* text, never the speaker tag.

**Rule R1 — if an NPC is `customizable`, every player-visible mention of their name in
prose MUST be `@<npc>` (and every relationship mention `@<npc>.rel`).** A single hardcoded
"Cole" left in a renamed-Cole game is a visible bug. Same for `@player` once the player can
rename themselves.

**Worked proof (Late Shifts, live-verified):** with the player renamed *Nadia* / build
*curvy* and Cole renamed *Jamie* / relationship *old flame*, the apartment scene renders
*"His eyes go over her **curvy** frame … **Jamie**: **Nadia**. Didn't think you'd come by."*
All four token forms resolving at once.

---

## §4 — The un-tokenizable-surface trap (R2)

The `@`-token only fires where the engine runs `_resolve_at_references`: **canvas prose,
dialog body, choice text, and location descriptions.** It does **NOT** reach structural
labels that the engine prints raw:

- **Location names** (`<h2>{location.name}>` — the navigation title)
- **Sidebar trait-bar `label`s** (e.g. a `"Cole Relation"` bar)
- **Locked-link tooltip text** (`locked_text_threshold`)
- **Quest/stage display strings** and **arc_stages** names
- The NPC's customize-screen `description` intro (printed raw, html-escaped)

**Rule R2 — never bake a customizable NPC's name into a structural label.** A location
called `"Cole's Apartment"` stays "Cole's Apartment" after the player renames Cole → the
leak the whole feature was supposed to avoid. **Genericize these instead:** the location
becomes `"The Apartment Across Town"`, the sidebar bar label becomes `"Closeness"`, the
locked tooltip becomes `"Once he's noticed you"`. Carry the specificity in the *prose*
(which tokenizes), keep the *labels* neutral.

(Canvas/node `name` fields are dev-only — they appear on the Canvas-Review page and the
dev-mode banner, never in a production player build — so those may keep the literal name.)

---

## §5 — Customizable-NPC required fields (R3)

A `customizable` NPC **must** declare both `relationship` (the default) and
`relationship_options` (the picker list), and the default must be a member of the options.
The importer **hard-fails** otherwise (`template_import.py:3289–3304`). There is no
rename-only mode — renaming and relationship-picking ship together.

Player `customization_fields` have their own guards (`:2906–2943`): field `id`s must be
lowercase snake_case, unique, and **not** one of the reserved `$player` properties
(`portrait`, `current_location`, `core_traits`, `flags`, `wardrobe`, `equipped`).
`select` needs `options` (and any `default` must be in them); `image_select` needs `options`
with `id` + `image` on each; `sets_portrait` is `image_select`-only.

---

## §6 — `image_select`, portraits, and the `@handle` collision

- **`image_select`** renders a clickable image grid; each option is `{ id, image, label }`.
  With `sets_portrait = true` the chosen image becomes `$player.portrait` (used everywhere
  the engine shows the player's face). Missing art degrades gracefully — the `<img>` hides
  on error and the label still shows — so it's safe to ship the field before the art lands
  (same missing-media convention as locations).
- **The `@handle` collision (R4):** the token regex matches any `@word`. Social-feed
  handles in phone content — `@samantha_x`, `@lexiluv_` — that don't resolve to a known NPC
  slug are left as literal text (fine), **but** a handle that happens to collide with an NPC
  short-name *will* be substituted. Keep social handles distinct from NPC slugs, or accept
  the rewrite.

---

## §7 — Composition with the phone (and other JS-rendered surfaces)

The phone renders authored text as **JavaScript data**, not passage bodies — so the
generation-time `@`-token processor never touches it. The runtime twin `setup.resolveAtRefs`
(same `@player`/`@npc` resolution, in JS) is now applied at every phone render point
(notify toasts, message bubbles, reply buttons, daily-chat history, daily-topic buttons —
`v2.py` + `v1.py`), so **you can use `@<npc>` / `@player` tokens in phone `notify`, message
`content`, and `daily_topics` text and they resolve to the customized name.** The thread
title, avatar, and preview already read the live `$npcs[uuid].name`, so they honor a rename
even without a token.

Doctrine still applies: keep names *out* of any future raw-printed surface, and prefer the
auto-dynamic thread name over hardcoding.

---

## §8 — When to make it customizable (and when not)

- **Make the player customizable** when the protagonist is a blank-ish self-insert (the
  RTS default): name + build + look is the standard opener. **Don't** when the protagonist
  is a written, named character central to the premise and the prose leans on third-person
  narration by name — retrofitting `@player` across hundreds of "she did X" lines fights the
  grain and buys little. (Late Shifts demonstrates the field types in one arc rather than
  sweeping the whole third-person script — a deliberate, scoped choice.)
- **Make an NPC customizable** when the relationship framing is a genuine player fantasy
  axis (the step-relative toggle) **and** the cost is bounded — i.e. the name isn't baked
  into many structural labels (§4) and isn't load-bearing for the premise. A dating
  love-interest is the cheapest, most natural candidate; a sibling whose siblinghood *is*
  the story is the most expensive and most destructive.

**Enabling checklist:**
1. `[player].customizable = true` + at least one `[[player.customization_fields]]` (array-of-
   tables placed **after** every `[player.*]` subtable — TOML scoping).
2. For each customizable NPC: `customizable = true` + `relationship` + `relationship_options`.
3. Every player-visible name mention → `@player` / `@<npc>`; every relationship → `@<npc>.rel` (R1).
4. Every structural label that named the NPC → genericized (R2).
5. No engine wiring — the `CustomizeCharacters` screen and the `Start` redirect are automatic.

---

## §9 — Cross-references

- **Schema:** [schema/02 §2.3] (player fields) + [schema/02 §3.1] (NPC customization fields);
  [schema/03 §15] (full worked example, all three field types + NPC rename + tokens).
- **Sibling doctrine:** [doctrine/11 clothing], [doctrine/12 rent], [doctrine/13 phone] —
  the other opt-in engine surfaces with the same "declare-the-input, write-the-output" shape.
- **Production reference:** `games/under_one_roof` — three customizable NPCs (Frank / Jake /
  Ryan), 400+ `@`-tokens; the largest real consumer. `games/test_customize` — the minimal
  purpose-built example. `games/late_shifts` — the scoped demonstrator (player name/build/look
  + Cole rename, this session).
- **Engine entry points:** importer `template_import.py:62`, validator `:2906`/`:3289`,
  runtime screen `v2.py:8376`, token processor `v2.py:12658`, JS twin `setup.resolveAtRefs`
  `v2.py:2722`.

═══════════════════════════════════════════════════════════════════════════════

## 19. 01_rts_overview

**Source:** `prompts_v2/reference/01_rts_overview.md`

---

# Reference 01 — Road to Success (RTS) Overview

**Source:** Doc 13 (`28th_april_TLS_Phase2_Redesign/13_Road_To_Success_Reference.md`, 2026-05-02 + §16 update 2026-05-03); `game_explorations/rts-arc-trace/notes.md`; live extraction across multiple sessions May 2026.
**Authority:** Reference. The sole reference game per LO §6.3.
**Purpose:** Name what RTS IS — the game shape, the size, the player loop, the chrome surfaces, the bootstrap experience. Doctrine files cite this for the "what does the reference game DO" question.

This file is the broad overview. Per-NPC scene catalogs in `reference/02_rts_scene_catalog.md`. Walkthrough doctrine in `reference/03_rts_walkthrough_panel.md`. HUD doctrine in `reference/04_rts_hud_world_model.md`.

---

## §1 — What RTS is

**Road to Success (RTS)** — adult interactive fiction, SugarCube/Twine-based. Source: `https://mopoga.com/road-to-success` v0.25. Captured locally in `game_explorations/rts-arc-trace/` across multiple exploration sessions.

The game RTS-shape sandboxes are modeled on. Every principle in `doctrine/01_rts_principles.md` (P1–P10) was extracted live from this game. Every mechanism in `doctrine/02_three_lanes_plus_capstone.md` was verified against this game's passage source. Every anti-pattern in `doctrine/07_anti_patterns.md` was tested against this game's behavior.

**LO decision §6.3:** RTS is THE reference. Not Jack's World. Not New In Town. Not Two Weeks. When a doctrine question arises and the answer isn't already specified, the question is: *"What does RTS do here?"*

---

## §2 — Game shape at a glance

Doc 13 §3 — verified counts via `eval(Story.passages)` + walkthrough panel + per-NPC `scenes` extraction:

| Dimension | Count | Notes |
|---|---|---|
| **NPC keys defined** | 53 | 16 with predefined `scenes` objects; 37 stub-only (location + name, scenes populate when player meets them) |
| **NPC-bound scenes** | ~60 | Per Walkthrough panel: Stepfather 12, Stepbrother 15, Stepgrandfather 6, Marcus 5, Sam 2, Emma 1, Jamal 3, Veronica 3, Priest 2, Mr. Matthew 1, Edward 4, Tow Truck Driver 1, Yacht Captain 1, Thief 2, Josh 1, Landlord 1, Gangster 1 |
| **Location-bound scenes** | ~70 | City Center 1, House 1, Bus 3, Photo Studio 2, School 12, Park 9, Gym 3, Mall 3, Night Club 2, Beach 7, Bar 4, Public Pool 2, Office 2, Driving School 1, Thomas's House 2, Strip Club 3, Clandestine Clinic 2, Restaurant 5, Police Station 1, Hospital 2, Abandoned Building 1, Gas Station 1, Movie Theater 2 |
| **Total scenes** | 130+ | The "content library" RTS sells |
| **Quest definitions** | 27 | 3 active at game start (`SchoolTest`, `MathHomework`, `INeedMoney`); 24 latent (activate on trigger conditions) |
| **Locations** | 41 | House sub-rooms + Residential + cityZones |
| **Calendar** | 7-day week × 6 time buckets | EM (Early Morning) / M (Morning) / A (Afternoon) / E (Evening) / N (Night) / LN (Late Night) |
| **Pacing** | ~30 turns per ~1 in-game day | One significant arc beat per day per NPC of focus |

**Key takeaways for RTS-shape sandbox authoring:**

- **130+ scenes is the content library**. RTS-shape games aren't 12 long arcs; they're many short scenes with overlapping mechanics.
- **53 NPCs with 16 active arcs** — the rest are NPCs the player meets later (e.g., Natasha unlocks via Library encounter). For TLS-shape slice scope: 4–6 fully-authored NPCs, with stubs prepared for "meet later" NPCs.
- **70 location-bound scenes vs 60 NPC-bound** — locations themselves have content (Beach 7, School 12). For TLS: solo-Maya activities at locations count as content surfaces (Lane 3 dispatcher mechanism).
- **6 time buckets × 7 day** — RTS uses a smaller time-buckets-per-day count than TLS's 24-hour clock. For TLS-shape games: time grain is implementation choice; RTS-style 6-band model is simpler for player planning.

---

## §3 — The 3 arc shapes (tendencies, not categories)

Doc 13 §5 originally framed 3 arc shapes; Doc 13 §16 Correction 7 refined to "tendencies, not categories" — every RTS NPC mixes random + deterministic + time-gated triggers; the RATIO differs.

The 3 tendencies:

| Shape | Trigger | Gating style | Player loop | Example NPCs |
|---|---|---|---|---|
| **Family / ambient escalation** | Random encounter on room entry, dice roll (20–33%) | NPC arousal emoji + MC corruption thresholds; relation always 0 (no narrative chain) | Visit room → maybe scene fires → repeat. Same action ("Study") triggers different scenes at different stat tiers. | Brother (15 scenes), Dad (12), Grandpa (6) |
| **Peer / quest chain** | Deterministic (chance=100) except minor variants | Narrative prerequisites in `guide` string: "Take the test and get at least an 8 grade", "Have at least 15 relationship points", "wait for his invite" | Read walkthrough → execute discrete prerequisite → unlock next deterministic beat. Traditional VN. | Marcus (5 scenes), Natasha, Sam, Emma |
| **Career / digital** | Deterministic + external metric + time delay | "Reach 1000 followers on Instafame", "wait 10 days, read message", "wait 15 days, read message" | Phone-mediated async. Grind followers → wait calendar days → respond to DM → date. | Edward (4 scenes), Jim (Pornstar), Richard (Photographer) |

### What each shape feels like

**Family arc (ambient escalation).** Player isn't "progressing a story" — they're raising stats, walking around home, and watching content gradually escalate. Reads as low-effort/high-frequency. Bootstrap: flash/tease at MC corruption 5 (chance 100) raises NPC arousal — once arousal > 0, random-encounter scenes become possible on bedroom visits. Family runs in *background* of the player's attention.

**Peer arc (quest chain).** Discrete, planned, sequential. Player has a checklist: "do the prereq → unlock the deterministic beat." Marcus arc requires MC corruption=0 mostly — peer/school is the "wholesome" track. This is what the player *focuses on this session*.

**Career arc (metric + time + DM).** Patient/calendar-driven. Edward DM widget literally arrives on the player's phone after a follower threshold + wait period. The player grinds Instafame followers across many in-game days while the family arc passively unfolds. This is the *long-burn project across weeks*.

**The 3 shapes give DIFFERENT TEMPOS so the player isn't always doing the same thing.**

### Refinement (Doc 13 §16 Correction 7)

The clean "three shapes" framing was a story extracted from data; live play shows every NPC mixes triggers. More honest framing:

> RTS gives every NPC a mix of random + deterministic + time-gated triggers; the ratio differs per NPC.

- **Brother** = "mostly random + significant deterministic" (15 scenes: 7 Lane 3 substitution / 5 Lane 1 hub / 3 Lane 2 random)
- **Marcus** = "mostly deterministic + tiny random splash" (5 scenes: 5 deterministic / 0 substitution / 0 random)
- **Edward** = "metric+wait + DM-mediated deterministic" (4 scenes: all deterministic via DM widget gate)

The 3 shapes are **tendencies**, not categories. TLS-shape sandbox NPC arc shapes (`doctrine/03_arc_shapes.md` 5 shapes) refine the RTS tendencies into more specific mechanical rhythms (family/ambient + slow-burn family + peer/dating + service + antagonist/witness).

---

## §4 — Bootstrap experience (Doc 13 §12 — turn-by-turn play log)

Captured live 2026-05-02. ~30 meaningful clicks Day 1 EM → Day 2 EM. Reading top-down gives the actual feel of a fresh playthrough.

### Day 1 — bootstrap timeline

| Turn | Action | Result | Stat / state delta |
|---|---|---|---|
| 1 | (start) | Day 1 Monday EM, Bedroom, Victoria | corr 0, ar 0, exhi 0, energy 100, $50, intel 0, beauty 0 |
| 2 | Auto-advance through intro | Lands at Bedroom passage | — |
| 4 | Click `Study 📖` | "STUDY / You studied an hour and feel smarter!" | intel +1, energy −10, time M |
| 6 | Click sidebar `🏫 Go to School` | **Silent fail** — passage stays Bedroom | Player wearing casual clothes (no error message — first surprise) |
| 7 | Wardrobe → School 1 image | clothing equipped | clothing.type = "school" |
| 8 | `Go to School` | School hub loads | — |
| 9 | Click `History Class ⚔️` → `Study 📖` | "feel smarter" — **NEW QUESTS unlocked** | intel +1, time A; SchoolTest + MathHomework activate |
| 11 | Leave school → House → Hallway | — | family schedule check: Dad=Work, Brother=School, Grandpa=Kitchen |
| 14 | `Hallway 🚪` → `Bedroom` (Brother's bedroom) | **🎯 PeepBrotherSex random-encounter fires** at MC corruption 0 | scene = PeepBrotherSex |
| 15 | Read scene + image + [Peep] [Hallway] | — | — |
| 16 | Click `Peep` | linkreplace adds: paragraph + VIDEO `masturbate1.mp4` + new choice [Stroke your pussy] | MC arousal 0 → 1 |
| 17 | Click `Stroke your pussy` | linkreplace adds: "You are not aroused enough to do this" | (no further reveal at corr 0) |
| 18 | Hallway → DadBedroom | **🎯 ProstituteSex (Dad scene) random fires** at MC corruption 0 | — |
| 19 | Click `Peek 👀` | image + "Stepfather having sex with a prostitute" + [Keep Watching] | MC arousal 1 → 2 |
| 20 | Click `Keep Watching` | **linkreplace adds EMPTY content** — scene truncates at corruption 0 | (Doc 13 §11 Correction 2: every visit shows opening; high-corruption returns reveal more) |
| 21 | Re-enter BrotherBedroom | PeepBrotherSex does NOT re-fire (`!executedToday` flag) | (verifies daily cap) |
| 22 | Click `Have sex with him 🔥` (gated, MC corr 0 < 3) | **Silent visual fail**. Source has `<<NotifyCorruption 4>>` for threshold publish. Corruption stays 0 (Doc 13 §11 Correction 3) | — |
| 24 | Sleep → Day 2 EM | — | day +1, energy 100, MC arousal 2 → 3 |
| 28 | Library | "There is a girl at the reading tables..." + [Say hello] | (excellent character setup line) |
| 29 | Click `Say hello 📚` | **🎯 Tier-3 scripted intro: Natasha** | speaker label changes "Student" → "Natasha" once names exchanged |

### Bootstrap takeaways

- **Day 1 Evening = first taboo content beat.** No grinding required.
- **Two random encounters fired naturally** in <5 moves.
- **One quest cascade** happened automatically (FirstDayOfShool auto-completed → SchoolTest + MathHomework activated).
- **One Tier-3 intro scene** was discoverable (Library → Natasha).
- **Three soft/notify-fail attempts** taught the thresholds without punishing.
- **No explicit tutorial outside the Walkthrough panel** — rest is learned by doing.

### Implications for RTS-shape sandbox authoring

- **Hand the player content immediately.** Day 1 Evening should have at least 1–2 taboo content beats. Don't gate the first 30 minutes behind grinding.
- **First 30 minutes should fire at least 2 random encounters.** Lane 2 ambient mechanism via dice on entry (per `doctrine/02_three_lanes_plus_capstone.md` §3).
- **First 30 minutes should include 1 Tier-3 scripted intro.** Named NPC introduction (e.g., Natasha at Library) — sets the literary quality bar players will see again at Lane 4 capstones.
- **No tutorial outside the walkthrough.** Discoverability lives in the Walkthrough panel (P2 transparent gating) + the sidebar (P10 HUD = world model).

---

## §5 — The economic + time engine (Doc 13 §10)

### Player stats

| Stat | Range | Mutation cadence | Notes |
|---|---|---|---|
| `corruption.points` | 0–∞ | Per masturbation / accept-taboo-action | Accumulates |
| `corruption.level` | 0–5+ | Derived from points (tiered: Pure / Lewd / Slutty / Whore...) | Used in gates as `getCorruptionLevel() >= N` |
| `exhibitionism` | 0–∞ | Per flash / public-nudity action | Independent axis from corruption |
| `beauty` | 0–∞ | Per gym, makeup, salon | Visible in left sidebar |
| `intelligence` | 0–∞ | Per Study / class | Used for school grade gates |
| `energy` | 0–100 | -10 per tick of activity, +N on rest | Hard cap forces sleep cycle |
| `arousal` | 0–10 | +1/day passive, +1 per peep beat, set by scenes | Required > 0 for masturbation, sex |
| `money` | 0–∞ | Earned via jobs, lost on rent / shopping | Drives apartment / car / phone unlock chain |
| `hunger` / `hygiene` | 0–100 | Decay over time | Force eating / showering loops |
| `clothing.type` / `clothing.name` | enum | Wardrobe equip | Gates location entry (school requires `school1`, naked requires corruption ≥ 3 to leave bedroom) |

### NPC stats (per `$npc.<key>`)

| Stat | Range | Notes |
|---|---|---|
| `arousal` | integer 0–N | Stored as integer (Brother arousal observed at `1`, `3`, `5`). The 🔥/🔥🔥/🔥🔥🔥 in Walkthrough display is threshold format, not storage format. Passive +1/day for in-scope family NPCs. |
| `corruption` | 0–∞ | Integer. Raised by player taboo actions toward this NPC. |
| `relation` | 0–∞ | Integer. Always 0 for family arcs (no narrative chain); meaningful for peer arcs. |
| `talkedToday` | bool | Once-per-day Talk gate. |
| `location` | string | Schedule-driven by tick (Brother: bathroom EM, school M+A, bedroom E+N+LN). |
| `scenes` | object | Per-scene state: `{unlocked, executedToday, gallery flag}`. |

### Time + economy

- **6 buckets per day:** EM / M / A / E / N / LN
- **7-day week:** Monday → Sunday
- **`$game.days`** = lifetime day counter (driving "wait 10 days" mechanics)
- **Activities `<<AddTime N>>`** advance N buckets
- **Money drives engagement:** rent on apartment, $400 for phone, etc. Force player to engage with peer/career arcs (jobs).

### Composition rule

> The same room can show different button sets per state.

A canonical example: Brother's bedroom at LN with Brother present + relation ≥ 10 shows "Sleep with him." At E with Brother present + corruption < 3 shows Talk/Tease/Flash/[Have sex *gated*]. At M (Brother at school) shows "is at school" + Hallway only.

The **clothing × location × time × stats** product is the gating space. Gates compose from layered conditions, not central rule tables. This makes the world feel rule-bound while keeping each individual gate readable in its own passage.

---

## §6 — The 4 RTS player surfaces

RTS presents content through 4 distinct UI surfaces. Each has its own doctrine for what belongs there.

### §6.1 — The location passage (the actual game world)

Where Maya is right now. Renders:
- Image of the location
- Time-of-day + day + weather (small banner)
- Menu of available activities (clothing-gated, time-gated, energy-gated, purchase-gated)
- Random-encounter override block (Lane 2 — see `doctrine/02_three_lanes_plus_capstone.md` §3)

This is what the player spends most of their time looking at.

### §6.2 — The Walkthrough panel (the published catalog)

The `📕 Walkthrough` button in the right sidebar opens a passage that **literally renders the scene table as data to the player**. Same fields as the engine's internal scene struct, just formatted as a table. (Detailed in `reference/03_rts_walkthrough_panel.md`.)

The player loop is literally: *open Walkthrough → pick a locked scene close to unlocking → read its requirements → close the gap → re-attempt.*

### §6.3 — The right sidebar (the HUD = world model)

Continuously surfaces:
- Time (Early Morning, Monday, Clear weather)
- Quest pin
- Per-NPC rows: Stepfather: Kitchen / Arousal / Corruption / Stepbrother: Bathroom / Arousal / Corruption / Stepgrandfather: Bedroom / Arousal / Corruption

Updates every tick. No menu click required to check NPC state. (Detailed in `reference/04_rts_hud_world_model.md`.)

### §6.4 — The phone app (career/digital surface)

Phone is a purchased item ($400 + first NPC's allowance unlocks it). Once acquired, the phone has multiple "apps":
- Messages (chat threads with NPCs)
- Instafame (social_feed + DM-driven career arc)
- Photo gallery
- Quests journal
- Custom apps

Phone is async-mediated content (Edward DM arrives after follower threshold + wait). Phone is NOT load-bearing for family/ambient arcs — those run via location passages + walkthrough.

### §6.5 — City map + location locking (live-verified 2026-06-03)

Live-play of `road_to_success` (introspected the `CityMap` macro handler + `$location` state; notes in `game_explorations/road_to_success/notes.md`). RTS locks **venues** (never districts — center/residential/elite/ghetto are always reachable via the Bus Stop) on **two orthogonal axes**:

| Axis | Field | Player experience |
|---|---|---|
| **Discovery** | `unlocked` (bool) | `CityMap` renders **nothing** when `unlocked === false` → the venue is **absent** from the map. The player can't see a place they haven't discovered. Verified: at game start the Residential map omits Marcus's/Emma's houses; the Elite map shows only Casino + Bus Stop (all three mansions hidden). |
| **Time** | `open` (bool, derived from `openPeriods` vs `$game.time`) + `opensAt` label | When `unlocked` but `open === false`, the tile **is** shown — darkened with a 🔒 + a "CLOSED / Opens at \<opensAt\>" badge; clicking it is a **no-op** (you stay on the map). Verified at early-morning Center: Night Club "Opens at Night," Bar "Opens at Evening," Movie Theater "Opens at Morning." |

**Discovery unlock = meeting the person tied to the place.** `<<UnlockLocation X>>` (→ `LocationService.unlockLocation`) fires at the in-fiction *meet / invite / "address sent"* beat — the lock literally means "you don't know them / where they live yet":

| Unlock | Trigger beat | Story |
|---|---|---|
| jamalHouse | `JamalMeet` | meet Jamal at the Club; "I'll see you again, right?" |
| veronicaHouse | `VeronicaMeet` | a sexual encounter with Veronica |
| marcusHouse | `SchoolTest` | the school test starts the "Study with Marcus" quest |
| emmaHouse | `EmmaInvite` | Emma: "I'll wait for you at my house in evening" |
| clandestineClinic | `HospitalBirth` | the doctor refers you to a friend's artificial-womb clinic |
| vipers (gang HQ) | `DrugDealer` | the drug-dealer questline opens the hideout |
| photoStudio / filmStudio / hotel | phone DMs (`InstafameMessages`) | Richard/Jim/Edward each "send you the address" + a `NotifyPhone "X is now unlocked on the city map"` signal |

**How our engine adapts it.** We have only a flag lock: `[[locations]]` `entry_conditions` + `blocked_message` — **visible-but-blocked** (the door shows and tells you why), not RTS-style hide; and **no native time-of-day location lock** (time/exposure lives on the hub, D72-R7). The coordination rule (a locked location that hosts an NPC schedule — Cases A/B/C, the unlock contract, the schedule-page leak if we ever adopt discovery-hiding) is `doctrine/10` §5.4.

---

## §7 — Three writing tiers (Doc 13 §9)

RTS doesn't write every scene at the same density. There are three observable tiers, each used deliberately for a class of moments.

### Tier 1 — Utility one-liner (~30 of 130 scenes, ~23%)

> **STUDY**
> You studied an hour and feel smarter!
> [Return ↩️]

Used for: bedroom Study, Sleep, Nap, generic activity-passes ("Socialize: You waste time socializing with your classmates").

Function: pure mechanical confirmation. The text exists only to make the stat-tick acknowledgment feel like *something*. ~10 words.

### Tier 2 — Vignette prose (~70 of 130 scenes, ~54%)

> **Stepbrother's Bedroom**
> You push open the door to your Stepbrother's room, only to stop dead in your tracks. He's in bed with a girl, their bodies tangled together... and they're definitely not just sleeping!
> [Peep]

Used for: random-encounter scenes with anonymous partners (Brother with "a girl," Dad with "a prostitute," generic strangers in public exhibitionism scenes).

Function: bridges mechanic to content. Generic descriptive prose with named situations but un-named NPC partners. ~30–50 words per beat, 2–4 beats per scene via linkreplace.

### Tier 3 — Scripted character (~30 of 130 scenes, ~23%)

> **A QUIET CORNER**
> *Most of the tables are empty. She slips something into her book to hold the page and looks up when you get close. Same girl from the hallway. This is the first time you actually stop to talk.*
>
> Victoria: Hi. Mind if I sit?
> Student: Yeah, go ahead. I'm just hiding from the hallway noise.
> Victoria: Fair. I'm Victoria.
> Student: Natasha. I come here when I need to study and people won't shut up out there.
> Natasha: Anyway. Don't be a stranger. I'm here most days.
> [Return ↩️]

Used for: named-NPC introductions, quest beats, arc transitions, Edward's DM widgets (10+ Speech beats with personality and seductive escalation).

Function: real character writing. Sensory grounding (*"She slips something into her book to hold the page"*). Voice (*"hiding from the hallway noise"* — introvert framing). Live-changing speaker labels (*"Student" → "Natasha"* once names exchanged). This is the layer that earns RTS its narrative weight.

### Distribution discipline

**The author doesn't waste Tier-3 prose on Tier-1 moments.** Reserved for transitions and named characters. This budget discipline is part of why a 130-scene game ships at all.

For TLS-shape sandboxes: Lane 1/2/3 = Tier 1 + Tier 2 default. Lane 4 capstones = Tier 3 earned. See `doctrine/05_rts_flat_prose.md` for the dual-register doctrine.

---

## §8 — Empirical corrections (data-extraction was wrong)

Doc 13 §11 captures 5 corrections from live play that disproved source-only inferences. Methodologically important: source-code extraction is fast but generates wrong inferences. Live play is slow but corrects them.

### Correction 1: Walkthrough requirements aren't strict gates for random encounters

**What was claimed (data-extracted):** Triple gating — NPC stats AND Player stats AND probability — strictly enforced.

**What actually happens:** `BrotherBedroom` random-encounter check is ONLY `previous()=="Hallway" && random(1,4)==1 && !executedToday`. The `requirementsMC.corruption: 15` field listed in walkthrough for `PeepBrotherSex` is **bypassed**. Live verified: scene fired at MC corruption 0 on Day 1 Evening.

**Implication:** the walkthrough's "REQUIREMENTS (MC)" column is a **suggested threshold for the FULL content version**, not an entry gate. Player can stumble into scenes early and get a teaser; full content unlocks later.

### Correction 2: Higher stats unlock MORE CONTENT inside a scene, not access TO the scene

**What actually happens:** Every visit shows the entry text + image + first beat. Linkreplace beats *after* that branch by stat. Live verified: clicked "Keep Watching" on Dad's `ProstituteSex` at MC corruption 0 → linkreplace inserted **empty content**. Scene literally has no more body for the player.

**Implication:** every scene has a "low-corruption short version" and a "high-corruption full version" inside the same passage. Player can't be punished for trying. Player knows there's more, comes back later.

### Correction 3: `<<NotifyCorruption N>>` is a UI hint, NOT a corruption-adder

**What was claimed:** "Failing taboo actions raises corruption — rejection trains the player. Brilliant design loop."

**What actually happens:** `<<NotifyCorruption N>>` is a *UI feedback widget* that displays "you need corruption level N for this." Always called in the ELSE branch with N matching the required level. Pattern verified across 5+ widget definitions.

**Live verified:** clicked "Have sex with him 🔥" at MC corruption 0 → notification appeared, **corruption.points stayed 0**.

**Implication:** the rejection-trains-corruption loop **does not exist** in RTS. Failure is *information* (publishes the threshold), not *progress*. P7 in `doctrine/01_rts_principles.md`.

### Correction 4: Watching/peeping itself raises MC arousal

**What was missed:** Voyeur scenes have +arousal effects baked in.

**What actually happens:** Live observed — peeping at `PeepBrotherSex` raised MC arousal 0 → 1. Clicking "Keep Watching" on Dad's `ProstituteSex` raised it 1 → 2. Sleeping overnight raised it 2 → 3 (matches walkthrough "+1 arousal each day").

**Implication:** scenes carry their own stat-effect side-channels separate from the explicit "stat-raising activities" (masturbate / gym / etc.). Stats and content interleave. P6 in `doctrine/01_rts_principles.md`.

### Correction 5: Quest descriptions are story flavor, not hard timers

**What was assumed:** "I need to take the school test on Monday" implies a Monday deadline.

**What actually happens:** Slept past Monday → quest still active Tuesday with same description.

**Implication:** quest description text is for atmosphere/orientation, not for mechanical scheduling. RTS doesn't time-out quests.

### Methodological note

**Source-code extraction generates wrong inferences ~30% of the time.** Live play is the only way to verify. For prompts_v2/ work: never claim "RTS does X" without source + live verification. The 5 corrections above were confident-but-wrong from data alone.

---

## §9 — Playthrough 2 additional findings (Doc 13 §16, 2026-05-03)

A second focused playthrough sampled Brother's content to near-exhaustion. Key additional findings:

### NPC interior thought bubbles are a runtime UI primitive (Finding 1)

RTS uses a styled Speech-thought macro to render NPC interior monologue:

> 💭 Alfred is thinking...
> *"I can't help myself... she looks so peaceful, so innocent. I just need to touch her..."*

This is a 4th-dimension writing primitive beyond the three tiers. Used in `BedroomSleepDadScene` (3 thought bubbles across 3 beats). Distinctly styled (italic + 💭 + "thinking..." attribution row).

For TLS-shape sandboxes: TLS has `thought_bubble` block type (shipped 2026-05-06). See `doctrine/05_rts_flat_prose.md` §7.

### Deterministic scenes also have stat-tier branching (Finding 2)

Doc 13 §11 #2 said "every visit shows something + content branches inside scenes." The branching applies to *deterministic* scenes too, not just random encounters:

- `SleepingBrother` walkthrough says "100% chance" — but at relation 12 the scene plays a 134-word *rejection* outcome ("Brother wakes, tells player to leave"). Higher relation (likely 25+) gates the consummation outcome.
- `BrotherCaughtMasturbating` at MC corr 6 plays the disgusted-rejection variant (5 lines). At MC corr 31 a new `[Shhh]` choice appears → full sex sequence (~590 words).

**Implication:** the walkthrough's `CHANCE: 100%` means the trigger always fires when reqs met, but the *content within* still gates by stats. P3 in `doctrine/01_rts_principles.md`.

### Real branching choices DO exist, just rare (Finding 3)

`SellingMyStepsister` has a real meaningful narrative `[Accept]/[Refuse]` choice that materially diverges downstream. Real player-choice branching is rarer than stat-gated reveals, but it does exist for major story moments.

**Pattern:** high-stakes scenes get player choice (Pattern F per Doc 57); everyday encounters get linkreplace-drip (Patterns A/B/C/D/E per `reference/02_rts_scene_catalog.md`).

### Passive NPC arousal accumulation (Finding 4)

Brother arousal observed climbing 0 → 1 → 2 → 3 across 3 in-game days *without anything done to him*. NPCs have a passive arousal trickle, not just MC-driven.

**Implication:** Doc 40 doctrine — both player + NPC arousal are always-climbing meters; passive +1/day for in-scope family NPCs.

### Being groped raises MC corruption (Finding 5)

Tutorial says "1 arousal per day OR after being groped." Live observed: BedroomGrope scene gave MC +1 corruption.

**Implication:** passive groping accelerates corruption naturally without active choices. The bootstrap loop is faster than tutorial implies — around 30-50% of corruption gain in early game can come from just walking around.

---

## §10 — Cross-references

### Sibling reference files

- `reference/02_rts_scene_catalog.md` — per-NPC scene tables (Brother / Father / Marcus / Edward with lane classifications + GUIDE strings + cumulative stat ladders)
- `reference/03_rts_walkthrough_panel.md` — Walkthrough panel doctrine (P2 transparent gating)
- `reference/04_rts_hud_world_model.md` — sidebar doctrine (P10 HUD = world model)

### Source

- `28th_april_TLS_Phase2_Redesign/13_Road_To_Success_Reference.md` — primary source
- `game_explorations/rts-arc-trace/notes.md` — 8 timestamped observation blocks
- `game_explorations/rts-arc-trace/passage_catalog.json` — 361 passages (engine source code)
- `game_explorations/rts-arc-trace/scene_bodies.jsonl` — 274 scene bodies (P1 length distribution evidence)
- `game_explorations/rts-arc-trace/ui_map.json` — HUD chrome catalog (P10 evidence)

### Sibling doctrine files (this reference informs)

- `doctrine/01_rts_principles.md` — P1–P10 derived from RTS extraction
- `doctrine/03_arc_shapes.md` — 5 TLS arc shapes refine RTS's 3 tendencies

---

**End of file.** Next: `reference/02_rts_scene_catalog.md` for the per-NPC scene catalogs.

═══════════════════════════════════════════════════════════════════════════════

## 20. 02_rts_scene_catalog

**Source:** `prompts_v2/reference/02_rts_scene_catalog.md`

---

# Reference 02 — RTS Per-NPC Scene Catalog

**Sources:** Doc 13 §5; Doc 21 (Brother 16-surface audit); Doc 22 (40-surface / 4-NPC comparison); Doc 24 §3 Brother walkthrough table; live extraction in `game_explorations/rts-arc-trace/passage_catalog.json` (361 passages, 1.2MB).
**Authority:** Reference — source-extracted scene catalogs for the 4 audited RTS NPCs.
**Purpose:** Give the LLM concrete per-NPC scene tables with: scene name + lane classification + GUIDE string + chance % + structural pattern (A–F) + word count. The catalog the doctrine cites.

This file is the empirical ground truth for `doctrine/02_three_lanes_plus_capstone.md` (lane mechanism) + `doctrine/04_authoring_rules.md` D56-R3 (per-arc-shape Lane 3 budget).

---

## §1 — What this catalog is

Doc 21 + Doc 22 audited 4 NPCs across 40 total surfaces (~30% of RTS's ~130 NPC-bound scene catalog). Each scene classified by:

- **Lane:** 1 (hub button) / 2 (location-entry random) / 3 (dispatcher substitution) / hub
- **Pattern (A–F):** structural shape of the cascade (see §6 below for pattern definitions)
- **Chance:** dice probability when triggered
- **GUIDE:** plain-English trigger recipe (as rendered in the Walkthrough panel — see `reference/03_rts_walkthrough_panel.md`)
- **Stat reqs:** NPC arousal + corruption + relation + player corruption thresholds
- **Words / LR / media:** content density indicators

**6 patterns observed (Doc 21 §4):**
- **A** Single-render utility (Tier-1)
- **B / B'** Random-flash multi-NPC / 1-beat reveal
- **C** Per-step stat-gated cascade
- **D** Top-of-cascade stat-gated entry
- **E** Pure linear cascade (gate on entry button)
- **F** Long cascade + real branching choice

Pattern definitions live in §6. Per-NPC catalogs in §2–§5.

---

## §2 — Brother (Family/ambient — 16 surfaces, 47% Lane 3)

The largest audited NPC arc. Brother is the canonical family/ambient reference (`doctrine/03_arc_shapes.md` §3).

### §2.1 — Brother walkthrough table (Doc 24 §3 — verbatim from in-game panel)

Source: in-game RTS Walkthrough → Stepbrother table, captured 2026-05-10 from `mopoga.com/road-to-success` v0.25. Fifteen scenes (the 16th is multi-NPC bridge `BedroomGrope`).

| # | Scene | NPC reqs | MC reqs | Chance | GUIDE | **Lane** |
|---|---|---|---|---:|---|---|
| 1 | Stepbrother Bedroom Grope | arousal 🔥 | None | 20% | Go to your bedroom | **2** |
| 2 | Stepbrother Bedroom Study Grope | arousal 🔥 + corr 1 | None | 20% | Study at your room | **3** |
| 3 | Stepbrother Bedroom Study Grope Pregnant | arousal 🔥 + corr 1 + pregnant | corr 30 | 20% | Study at your room while pregnant | **3** |
| 4 | Sleep with Stepbrother | arousal 🔥 + corr 10 | corr 30 | 100% | Go to Stepbrother bedroom late at night and ask to sleep with him | **1** |
| 5 | Stepbrother Bedroom Flash | None | corr 5 | 100% | Go to your Stepbrother bedroom | **1** |
| 6 | Bedroom Tease | None | corr 5 | 100% | Go to your Stepbrother bedroom | **1** |
| 7 | Stepbrother Shower Sex | arousal 🔥 + corr 5 | corr 30 | 33% | Masturbate at shower at the house bathroom | **3** |
| 8 | Peep Stepbrother sex | None | corr 15 | 25% | Go to your Stepbrother bedroom | **2** |
| 9 | Playing Videogame Pregnant | arousal 🔥🔥 + corr 10 + pregnant | corr 30 | 20% | Play videogame at your living room while pregnant | **3** |
| 10 | Playing Videogame | arousal 🔥🔥 + corr 10 | corr 30 | 20% | Play videogame at your living room | **3** |
| 11 | Brother Help Study | arousal 🔥🔥🔥 + corr 15 | None | 20% | Study at your room | **3** |
| 12 | Brother Caught Masturbating | arousal 🔥🔥 + corr 10 | corr 30 | 25% | Go to your Stepbrother bedroom | **2** |
| 13 | Brother Bedroom Pregnant Sex I | None | None | 100% | Go to your Stepbrother bedroom while pregnant and have sex with him | **1** |
| 14 | Brother Bedroom Sex I | None | None | 100% | Go to your Stepbrother bedroom and have sex with him | **1** |
| 15 | Stepbrother Washing Dishes Sex | arousal 🔥🔥 + corr 10 | corr 30 | 20% | Go to the kitchen and wash the dishes | **3** |

**Distribution:**

| Lane | Count | % of 15 |
|---|---:|---:|
| **1 — Hub button** | 5 | 33% |
| **2 — Location-entry random** | 3 | 20% |
| **3 — Dispatcher inside menu activity** | **7** | **47%** |

**Lane 3 is the largest bucket.** Almost half of Brother's repeatable surfaces fire as random substitutions inside other menu activities. This is RTS's primary mechanism for "the NPC is everywhere in your day-to-day life without overstuffing menus."

The 7 lane-3 surfaces piggyback on **four parent activities:**
- Study (×3 — base, pregnant variant, Help Study)
- Play Videogame (×2 — base + pregnant variant)
- Shower→Masturbate (×1)
- Wash Dishes (×1)

### §2.2 — Brother structural pattern table (Doc 21 §3 — 13 Brother-bound + 3 multi-NPC)

Columns:
- **Words:** total source word count
- **LR:** count of `<<linkreplace>>` macros in source
- **StatIf:** count of stat-gate `<<if>>` patterns
- **StatInLR:** how many linkreplace blocks contain stat-gated content inside
- **ChoiceInLR:** how many linkreplace blocks contain a nested button or further linkreplace
- **Vid / Img:** media counts

| Scene | Type | Words | LR | StatIf | StatInLR | ChoiceInLR | Vid | Img | Pattern |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `BrotherBedroom` | hub | 222 | 0 | 0 | 0 | 0 | 0 | 1 | **Hub** (button injection by presence + time + relation) |
| `BrotherBedroomTease` | button (Tier-1) | 69 | 0 | 0 | 0 | 0 | 0 | 5 | **Pattern A** — single-render utility |
| `BrotherBedroomFlash` | button (Tier-1) | 93 | 0 | 0 | 0 | 0 | 0 | 11 | **Pattern A** — single-render utility |
| `BedroomGrope` | random multi-NPC | 130 | 0 | 2 | 0 | 0 | 0 | 5 | **Pattern B** — random-flash with NPC dice |
| `BedroomStudyBrotherGrope` | random | 127 | 1 | 2 | 0 | 0 | 0 | 3 | **Pattern B'** — random-flash with 1-beat reveal |
| `PeepBrotherSex` | random | 341 | 4 | 0* | 1 | 1 | 4 | 5 | **Pattern C** — per-step stat-gated cascade |
| `BrotherCaughtMasturbating` | random | 902 | 10 | 1 | 1 | 1 | 11 | 0 | **Pattern D** — top-of-cascade stat-gated entry, then linear |
| `BrotherBedroomSex1` | button | 811 | 12 | 0 | 0 | 1 | 13 | 0 | **Pattern E** — pure linear cascade (gate is on the BUTTON, not in scene) |
| `BrotherBedroomPregnantSex1` | button-variant | 523 | 8 | 0 | 0 | 1 | 9 | 0 | **Pattern E** — variant of Sex1, pregnancy branch |
| `BrotherShowerSex` | button (bathroom) | 673 | 9 | 2 | 1 | 1 | 15 | 0 | **Pattern D** |
| `BrotherWashDishesSex` | event (kitchen) | 556 | 8 | 0 | 1 | 1 | 8 | 0 | **Pattern D / E** (mostly linear with one mid-cascade check) |
| `BrotherHelpStudy` | event | 867 | 10 | 3 | 1 | 1 | 11 | 0 | **Pattern D** with multiple intermediate stat gates |
| `SleepingBrother` | button (LN) | 527 | 7 | 1 | 1 | 1 | 11 | 0 | **Pattern D** — top gate (relation/corruption); rejection variant if low |
| `BedroomStudyBrotherGropePregnant` | random-variant | 876 | 11 | 3 | 1 | 2 | 10 | 1 | **Pattern D** with pregnancy-aware variants |
| `PlayingGamesSex` | event-multi | 877 | 11 | 0 | 1 | 1 | 11 | 0 | **Pattern E** |
| `SellingMyStepsister` | random cross-NPC | 1077 | 18 | 0 | 1 | 2 | 16 | 0 | **Pattern F** — long cascade + real `[Accept]/[Refuse]` choice branch |

\* `PeepBrotherSex` `StatIf=0` from regex because the gates use `getArousal() > 0` and `getCorruptionLevel() >= 2` *inside the linkreplace bodies* (not at scene-entry); regex caught them as `StatInLR=1` instead.

### §2.3 — Brother pattern distribution

| Pattern | Count | % of Brother | Doctrine layer |
|---|---:|---:|---|
| Hub (button injection) | 1 | 6% | location-render |
| **A** Single-render Tier-1 utility | 2 | 13% | daily texture |
| **B/B'** Random-flash multi-NPC | 2 | 13% | daily texture |
| **C** Per-step stat-gated cascade | 1 | 6% | flagship random encounter |
| **D** Top-of-cascade stat-gated entry | 6 | 38% | most random + button cascades |
| **E** Pure linear cascade (gate at hub) | 3 | 19% | high-stakes button scenes |
| **F** Long cascade + branching choice | 1 | 6% | cross-NPC bridges |

**~10 of 16 (63%) use linkreplace cascades.** **~4 of 16 (25%) are single-render Tier-1/Tier-2.** **1 hub** drives discoverability.

**Stat-branching distribution:**
- Per-step gates inside cascade (Pattern C): 1 scene (PeepBrotherSex only)
- Top-of-cascade single gate (Pattern D): 6 scenes — the dominant replay-driver
- No in-scene gate, hub gates entry (Pattern E): 3 scenes — once-and-done
- No stat gating at all (Patterns A, B): 4 scenes — Tier-1 utility

---

## §3 — Dad / Stepfather (Family/proximity — 9 named surfaces)

| Scene | Type | Words | LR | StIf | StLR | CILR | Vid | Img | Pattern |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `DadBedroom` | hub | 201 | 3 | 0 | 1 | 1 | 0 | 3 | **Hub variant** — has its own linkreplace! Different from `BrotherBedroom` |
| `DadPeepSex` | random | 647 | 9 | 0 | 1 | 1 | 8 | 0 | **Pattern D** |
| `DadPeepSexBedroom` | random | 683 | 10 | 0 | 1 | 1 | 11 | 0 | **Pattern D** |
| `DadShowerSex` | event | 642 | 9 | 1 | 1 | 1 | 13 | 0 | **Pattern D** |
| `DadShowerSexPregnant` | variant | 517 | 7 | 1 | 1 | 1 | 7 | 0 | **Pattern D** |
| `DadWashDishesSex` | event | 668 | 6 | 2 | 1 | 1 | 11 | 0 | **Pattern D** with multi-stat gate |
| `DadWashDishesSexPregnant` | variant | 493 | 6 | 1 | 0 | 1 | 8 | 0 | **Pattern E** (linear, gate elsewhere) |
| `BedroomSleepDadScene` | random | 745 | 9 | 2 | 1 | 1 | 10 | 0 | **Pattern D** + thought bubbles (Doc 13 §16 Finding 1) |
| `BedroomStudyDadGrope` | random | 329 | 8 | 3 | 1 | 1 | 8 | 1 | **Pattern D** with multiple intermediate gates |

**Distribution:** 8/8 content scenes use linkreplace cascades. **0 single-render utility scenes** (Dad has no Tease/Flash equivalents — father archetype is more passive than brother archetype). Pattern D dominant. Hub itself uses linkreplace (Brother's hub doesn't).

**Implication:** Dad is a "deeper but smaller" arc than Brother. Same arc tendency (family/ambient), different density curve. For TLS-shape sandboxes: family/ambient NPCs can vary in distribution within the shape — Brother's "many short" approach vs Dad's "fewer longer" approach are both valid.

---

## §4 — Marcus (Peer/quest-chain — 12 named surfaces)

| Scene | Type | Words | LR | StIf | StLR | CILR | Vid | Img | Pattern |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `MarcusHallway` | hub-thin | 43 | 0 | 0 | 0 | 0 | 0 | 1 | **Hub-thin** — just nav + image |
| `MarcusBathroom` | nav | 42 | 0 | 0 | 0 | 0 | 0 | 1 | **Pattern A** — single-render |
| `MarcusBathroomEncounter` | event | 176 | 1 | 0 | 1 | 1 | 0 | 2 | **Pattern B'** — 1-beat reveal |
| `MarcusBedroom` | nav | 99 | 0 | 0 | 0 | 0 | 0 | 1 | **Pattern A** — single-render |
| `MarcusBedroomSex1` | button | 585 | 9 | 0 | 0 | 1 | 10 | 0 | **Pattern E** — linear cascade, gate at hub button |
| `MarcusBedroomSexPregnant` | variant | 429 | 7 | 0 | 0 | 1 | 8 | 0 | **Pattern E** |
| `MarcusClassSex` | event | 630 | 9 | 0 | 0 | 1 | 10 | 0 | **Pattern E** |
| `MarcusParkDate` | event | 452 | 6 | 0 | 1 | 3 | 0 | 0 | **Pattern F** — `HideDiv` parallel branches + Accept/Decline + nested stat gate |
| `MarcusParkSex` | event | 726 | 10 | 0 | 0 | 1 | 10 | 0 | **Pattern E** (entered from ParkDate Accept→Follow) |
| `StudyWithMarcus` | event | 678 | 10 | 0 | 0 | 1 | 13 | 0 | **Pattern E** |
| `BathroomSurpriseMarcusBoyfriend` | event | 957 | 10 | 0 | 1 | 1 | 12 | 0 | **Pattern D** |
| `CaughtMasturbatingMarcusBoyfriend` | event | 1945 | 18 | 0 | 1 | 1 | 24 | 0 | **Pattern D** — Marcus's longest scene |

**Distribution:** 8/12 use linkreplace cascades; 4/12 are short utility/navigation. **Pattern E dominant** for sex/intimate scenes (qualify-then-full content) — fits the peer/quest-chain doctrine. Pattern F appears once (ParkDate — relationship-defining moment with real Accept/Decline).

**Implication:** peer/quest-chain arcs have a different cascade signature from family/ambient. **Pattern E** (hub-gated linear) dominates because the player has already committed by clicking through the prereq chain — gate at the entry button is appropriate. Family/ambient uses Pattern D (top-of-cascade gate) because random-encounter entry means the gate has to live inside the scene.

For TLS Ryan (peer/dating): Pattern E for sex scenes; Pattern F for relationship-defining moments (partner-commit capstone Phase 2+).

---

## §5 — Edward (Career/digital — 1 named scene + DM widget)

| Scene | Type | Words | LR | StIf | StLR | CILR | Vid | Img | Pattern |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `EdwardThreesome` | event | 951 | 16 | 0 | 0 | 1 | 14 | 1 | **Pattern E** — long linear cascade, hub-gated (DM accept) |
| `Instafame` | app-shell | 420 | 0 | 0 | 0 | 0 | 0 | 0 | **Hub-app** — phone app shell |
| `InstafameDM` | DM-thread shell | 70 | 0 | 0 | 0 | 0 | 0 | 0 | **Hub-thin** — DM list shell |

**Plus:** `InstafameMessages` widget (9331 chars) contains the DM conversations. Edward's `EdwardDM` widget verified: **Pattern F** — linkreplace cascade with a `HideDiv`-based Accept/Decline branch at corruption ≥ 3 + `<<NotifyCorruption 3>>` for the rejection variant. **Mechanism structurally identical to MarcusParkDate**, rendered in DM frame instead of park scene.

### Implication: career/digital is presentation-layer different, mechanism-layer identical

Edward's "career/digital" arc tendency is in the *framing* (DM-mediated, async, calendar-driven) — not in the cascade mechanism. The same Pattern F that governs MarcusParkDate governs EdwardDM. **The arc tendency is presentation; the mechanism is shared.**

For TLS-shape sandboxes: career/digital arcs (if scoped) can use the same cascade primitives (Patterns A–F) as family/peer arcs — only the entry mechanism differs (DM widget arrival vs. location entry).

---

## §6 — The 6 patterns (definitions + canonical examples)

Six structural patterns observed across the 40 audited surfaces. Each has a verified canonical example.

### §6.1 — Pattern A — Single-render utility (Tier-1)

**Examples:** `BrotherBedroomTease` (69w), `BrotherBedroomFlash` (93w), `MarcusBathroom` (42w), `MarcusBedroom` (99w)

**Shape:**
```
title + 1-line description + 1 image (random from pool of 5-11) +
stat-tick effects + return button
```

**Source verbatim** (`BrotherBedroomFlash`):
```twine
<h3>You give a little show to your $npc.Brother.relationship</h3>
<<set $game.randomMedia to either("brotherflash1.webp", ..., "brotherflash5.webp")>>
<div class='shower'>[img[setup.ImagePath+'/house/brotherbedroom/' + $game.randomMedia]]</div>
<<UnlockNPCScene Brother BrotherBedroomFlash>>
<<AddExb>><<AddArousal>><<AddBrotherCorruption>><<AddTime '1'>>
<<button 'Return ↩️' 'BrotherBedroom'>><</button>>
```

**Mechanism:** No linkreplace. No stat checks. Random media slot for replay variety. Stat ticks happen on entry. **One paragraph, one image, one return.**

This is RTS Tier-1 in pure form. ~30% of the catalog is this thin.

### §6.2 — Pattern B — Random-flash with NPC dice (utility multi-NPC)

**Examples:** `BedroomGrope` (130w, multi-NPC)

**Shape:**
```
roll 1-2 dice → check which NPC at home with arousal > 0 →
render that NPC's grope variant + image + 1 speech line + stat ticks
```

**Mechanism:** Stat checks gate WHICH variant fires, not depth of variant. Each variant is a single-render flash (~30 words + image). Per-NPC corruption ticks accumulate from passive groping. **No cascade. One paragraph either way.**

### §6.3 — Pattern B' — Single-beat linkreplace (low-tier random)

**Examples:** `BedroomStudyBrotherGrope` (127w, 1 LR), `MarcusBathroomEncounter` (176w, 1 LR)

**Shape:** Same as Pattern B + one minor click-to-reveal beat. Effectively a Pattern B with a tiny narrative payoff click.

### §6.4 — Pattern C — Per-step stat-gated cascade

**Canonical example:** `PeepBrotherSex` (341w, 4 LR) — **the only verified Pattern C across all 40 audited surfaces**

**Shape:**
```
opening paragraph + image
└── linkreplace "Peep" → +paragraph + video
    └── linkreplace "Stroke your pussy"
        ├── if getArousal() > 0: +paragraph + video
        │   └── linkreplace "Masturbate"
        │       ├── if getCorruptionLevel() >= 2: +paragraph + video
        │       │   └── linkreplace "Cum!" → climax + UnlockNPCScene + AddCorruption
        │       └── else: NotifyCorruption(2) + "I should get out of here..."
        └── else: AddArousal + "You are not aroused enough to do this"
```

**Mechanism:** Cascade with **multiple stat gates at intermediate beats**. Player can begin the cascade, but each subsequent click is gated. If the player doesn't meet a gate, they get a published threshold (`NotifyCorruption(2)`) and a one-line bail. The scene **partial-completes** at the gate level — they saw 2-3 beats but not all 4.

**Replay loop:** raise arousal → next visit gets past beat 2. Raise corruption to 2 → next visit gets past beat 3. **The "come back later" loop is per-stat-per-beat.**

**Pattern C is rare** — only 1 of 40 audited surfaces. Doc 21 may have over-weighted it as a category by treating PeepBrotherSex as exemplary. Most cascades use Pattern D (top-gate) or Pattern E (hub-gate).

### §6.5 — Pattern D — Top-of-cascade stat-gated entry (the dominant pattern)

**Canonical example:** `BrotherCaughtMasturbating` (902w, 10 LR)

**Shape:**
```
opening paragraph + video
└── linkreplace "Enter the room" → +paragraphs + video + dialog
    ├── if getCorruptionLevel() >= 3 AND StageTwoCorruption(Brother):
    │   └── linkreplace "Shhh"  ← FULL 8-beat sex cascade (linear from here)
    │       └── linkreplace "You kiss him"
    │           └── linkreplace "You blow him"
    │               └── linkreplace "You show him your boobs"
    │                   └── linkreplace "You titty fuck him"
    │                       └── linkreplace "You jump on him"
    │                           └── linkreplace "You fuck him"
    │                               └── linkreplace "Harder!"
    │                                   └── linkreplace "He cums" → UnlockNPCScene
    ├── elif getCorruptionLevel() >= 3:
    │   └── "He hides his dick, tells you to leave" + StageNotification
    └── else (low corr):
        └── "Ew you pervert! Stop it!" + NotifyCorruption(3)
```

**Mechanism:** Cascade with **ONE stat gate at top-of-branch**. Either you're in the deep cascade (8 beats of seduction) or you're in one of two rejection variants. **No partway.** Inside the cascade: pure linear progression — each click reveals next beat, no further stat checks.

**Replay loop:** raise corruption to 3 → next visit unlocks the cascade entry → see all 8 beats. **The "come back later" loop is one-stat-one-shot.** You either get the full content or you get the rejection variant.

**Pattern D dominates the catalog** (15 of 40 = 38%). Most family/ambient cascades use this pattern.

### §6.6 — Pattern E — Pure linear cascade (gate on the entry BUTTON, not in scene)

**Canonical example:** `BrotherBedroomSex1` (811w, 12 LR, 0 stat-ifs in body)

**Shape:**
```
[scene only entered via "Have sex with him 🔥" button at hub,
 which itself gates on getCorruptionLevel() >= 3 + getArousal() > 0]

opening paragraph + video
└── linkreplace beat 1 → +paragraph + video
    └── linkreplace beat 2 → +paragraph + video
        └── ... (~10 more beats) ...
            └── linkreplace "He cums" → UnlockNPCScene + FinishSex
```

**Mechanism:** No stat checks inside the scene at all. The gate lives on the **button at the hub**. Player either qualifies and sees the entire cascade, or doesn't qualify and gets `NotifyCorruption(4)` at the hub.

**Replay loop:** none. Once unlocked, every visit shows the same content. **Depth-by-replay doesn't apply** — this scene is "either you get it or you don't."

**Pattern E dominates peer/quest-chain arcs** (Marcus: 5 of 12 scenes). Family arcs use it for high-stakes once-and-done scenes (BrotherBedroomSex1).

### §6.7 — Pattern F — Long cascade + real branching choice

**Canonical examples:** `SellingMyStepsister` (1077w, 18 LR), `MarcusParkDate` (452w, 6 LR), `EdwardDM` (in `InstafameMessages` widget, 9331c)

**Shape:** Cascade with a real `[Accept] / [Refuse]` mid-scene choice that materially diverges downstream. Reserved for high-stakes story moments.

**Live verification (Doc 22 §11):** `MarcusParkDate` Accept/Decline mechanism confirmed: parallel cascades hidden/shown via `<<HideDiv>>`; per-beat effects fire on click; `<<MakeBoyfriend Marcus>>` macro inside Accept linkreplace block fires on click (player.relationship.loyalty: 0 → 100).

**Pattern F is rare** (3 of 40 = 8%). Reserved for relationship-defining moments. For TLS-shape sandboxes: Lane 4 capstone Type B (Doc 57 §3) maps directly to Pattern F.

### §6.8 — Hub passages (4 audited)

Hubs vary more than expected. Not all NPC hubs follow the same template.

| Hub | NPC | Words | LR | Mechanism |
|---|---|---:|---:|---|
| `BrotherBedroom` | Brother | 222 | 0 | Button menu by presence + time + relation. Random-encounter override on entry from Hallway. |
| `DadBedroom` | Dad | 201 | 3 | **Has its own linkreplace** — peeking through the door is built INTO the hub before the button menu. |
| `MarcusHallway` | Marcus | 43 | 0 | Thin navigation passage. Marcus content is event-triggered, not button-menu-driven. |
| `Instafame` | Edward | 420 | 0 | Phone app shell — feed of posts + DM access button. |
| `InstafameDM` | (DM list) | 70 | 0 | DM thread list — each thread opens a `<<widget>>` cascade. |

**Family/proximity hubs:** room passages with button menus + sometimes their own linkreplace. Stat-injected buttons (`Sleep with him` at relation ≥ 10) are rare; presence/time injection is universal.

**Peer hubs:** thin navigation. Peer scenes are event-driven (Park Date, Class, Bathroom Encounter), not menu-driven. Player initiates by going to the location at the right time.

**Career hubs:** app/feed shells. Content arrives async via DM widgets, not via button menus.

---

## §7 — Cross-NPC pattern distribution (Doc 22 §3)

40 surfaces total across 4 NPCs.

| Pattern | Brother | Dad | Marcus | Edward | Total | % of 40 |
|---|---:|---:|---:|---:|---:|---:|
| Hub (button injection) | 1 | 1 | 1 | 1 | **4** | 10% |
| **A** Single-render utility | 2 | 0 | 2 | 0 | **4** | 10% |
| **B/B'** Random-flash multi-NPC / 1-beat | 2 | 0 | 1 | 0 | **3** | 8% |
| **C** Per-step stat-gated cascade | 1 | 0 | 0 | 0 | **1** | 3% |
| **D** Top-of-cascade gate, then linear | 6 | 7 | 2 | 0 | **15** | 38% |
| **E** Pure linear cascade (gate at hub button) | 3 | 1 | 5 | 1 | **10** | 25% |
| **F** Long cascade + real branching choice | 1 | 0 | 1 | 1 (DM widget) | **3** | 8% |

**Aggregate cascade rate: 29 of 40 surfaces (~73%) use `<<linkreplace>>`.** Single-render utility: 7 of 40 (~18%). Hubs: 4 of 40 (~10%).

**Per-block `text_variants`: 0 of 40.** Confirmed absent across the 4 audited NPCs.

---

## §8 — Where gate placement lives per arc tendency

Doc 22 §4 — the arc-tendency difference doesn't change WHETHER cascades exist — it changes WHERE the stat gate sits within the cascade structure.

| Arc tendency | Dominant pattern | Where stat gate lives | Replay loop |
|---|---|---|---|
| **Family / proximity** (Brother, Dad) | Pattern D | **Top of cascade**, after opening beat | Per-NPC stat threshold → cascade unlocks fully on next visit. **Single-step replay**: cross threshold once, all content available. |
| **Peer / quest-chain** (Marcus) | Pattern E | **At the hub button** | **No replay variation** — once narrative prereq met, cascade plays the same every time. Quest progression replaces tier progression. |
| **Career / digital** (Edward) | Pattern E (Threesome) + Pattern F (DMs) | **At the hub button OR DM widget gate** | DM-async progression. Real Accept/Decline branches at money/sex moments. |

**Key insight:** the "story shape" (random/deterministic/quest-chain/calendar) is delivered by:
1. Where the trigger fires (hub random encounter vs button vs DM arrival)
2. Where the stat gate sits (mid-cascade vs hub button vs DM widget)
3. The framing layer (room visit vs date scene vs phone DM)

The CONTENT MECHANISM (linkreplace cascade with stat-gated branches) is the same primitive across all three. **One engine, three framings, three gate-placements — same mechanic.**

**Implication for TLS-shape sandboxes:** adopting linkreplace cascades doesn't lock the game into one arc shape. The same cascade primitive supports family-style (Pattern D), peer-style (Pattern E), career-style (Pattern E + F).

---

## §9 — Confidence ladder

Per methodology rule (use both source extraction AND live play, never one alone):

✅ **HIGH confidence (source-verified + live-verified across 4 NPCs):**
- 6 patterns (A-F) reproducible across all 4 audited NPC sets
- ~73% cascade rate generalizes (varies by NPC: Dad 100%, Brother 63%, Marcus 67%, Edward 100% of content scenes)
- Per-block `text_variants` used in 0 of 40 surfaces
- Arc tendencies manifest in gate placement, not cascade existence
- Pattern E dominates peer/career; Pattern D dominates family
- Live verification (Doc 22 §11, 2026-05-06) confirmed Pattern D + E + F mechanisms in live play

🟡 **MED confidence:**
- 4 NPCs out of RTS's ~16 with `scenes` objects audited (~25% of the named-NPC catalog). Other NPCs (Grandpa 6 / Sam 2 / Veronica 3 / Priest 2 / Jamal 3 / Josh 1 / Tow Truck Driver 1 / Yacht Captain 1 / Thief 2) may surface additional patterns or different distributions.
- Hub variation observation (4 hubs) — small sample for that conclusion specifically.

❌ **NOT established:**
- Live experience of pattern D vs E "feels" (which is more satisfying for replay)
- Whether location-bound scenes (~70 per Doc 13 §3) follow the same pattern distribution as NPC-bound — completely unaudited
- Whether `checkSceneReq()` semantics affect Pattern E gating in ways the source doesn't expose

---

## §10 — Cross-references

### Sibling reference files

- `reference/01_rts_overview.md` — broad RTS context (size, time engine, bootstrap experience)
- `reference/03_rts_walkthrough_panel.md` — the surface that renders these scene tables to the player
- `reference/04_rts_hud_world_model.md` — sidebar (HUD) doctrine

### Source docs

- `28th_april_TLS_Phase2_Redesign/13_Road_To_Success_Reference.md` — RTS broad catalog
- `28th_april_TLS_Phase2_Redesign/21_RTS_Brother_Mechanism_Audit.md` — Brother 16-passage audit source
- `28th_april_TLS_Phase2_Redesign/22_RTS_Cross_NPC_Mechanism_Comparison.md` — 40-surface comparison source
- `28th_april_TLS_Phase2_Redesign/24_RTS_Three_Lanes_Repeatable_Activities.md` §3 — Brother walkthrough table source

### Sibling doctrine files (this catalog informs)

- `doctrine/02_three_lanes_plus_capstone.md` — Lane mechanism (Patterns A-F map to lanes)
- `doctrine/03_arc_shapes.md` — 5 TLS arc shapes refine the 3 RTS tendencies
- `doctrine/04_authoring_rules.md` D56-R3 — per-arc-shape Lane 3 budget (Brother 47% Lane 3 sets the family/ambient bound at 4-7)

### RTS source artifacts

- `game_explorations/rts-arc-trace/passage_catalog.json` — 1.2MB / 361 passages, all 40 audited surfaces verbatim
- Verbatim source for canonical examples (BrotherCaughtMasturbating, BrotherBedroomSex1, MarcusParkDate, EdwardDM widget) included in Doc 21 + Doc 22 evidence sections

---

**End of file.** Next: `reference/03_rts_walkthrough_panel.md` for the Walkthrough doctrine (P2 transparent gating).

═══════════════════════════════════════════════════════════════════════════════

## 21. 03_rts_walkthrough_panel

**Source:** `prompts_v2/reference/03_rts_walkthrough_panel.md`

---

# Reference 03 — RTS Walkthrough Panel (Transparent Gating Doctrine)

**Sources:** Doc 56 P2 (transparent gating principle); Doc 24 §5 (walkthrough discovery doctrine); Doc 13 §6 (Walkthrough panel as transparent planning UI); live extraction of `WalkthroughV2` passage from RTS source (4738 chars).
**Authority:** Reference. P2 evidence base.
**Purpose:** Document the RTS Walkthrough panel as the canonical "published catalog" UI surface — what it renders, what columns it exposes, what doctrine it operationalizes.

This file is the source-of-truth for `doctrine/01_rts_principles.md` P2 and `doctrine/04_authoring_rules.md` D56-R5 (every canvas declares a `guide` string).

---

## §1 — The walkthrough IS the game's quest log

Doc 13 §6 — the `📕 Walkthrough` button in the right sidebar opens a passage that **literally renders the scene table as data to the player**. Same fields as the engine's internal scene struct, just formatted as a table.

**The player loop is literally:**

> open Walkthrough → pick a locked scene close to unlocking → read its requirements → close the gap → re-attempt.

**There is no hidden progression. The "story" is the player's self-authored checklist progression across the 130+ scene catalog.**

This is the P2 transparent-gating doctrine in pure form. Transparency is the design, not a fallback.

---

## §2 — What the Walkthrough panel renders

Three sections, in order:

### §2.1 — Top section: tutorial (verbatim)

```
How to gain corruption and exhibitionism

At the start of the game, you gain 1 arousal each day, or after being
groped in your bedroom. You can choose to masturbate to increase your
corruption.

Once you reach 5 corruption points, you unlock the option to flash
your Stepbrother through his bedroom, gaining 1 exhibitionism point.

Some events have requirements, such as a minimum corruption level,
exhibitionism level, or relationship level with an NPC. You can also
trigger events by visiting certain locations.
```

**The bootstrap loop is taught explicitly.** No discovery required.

**Implication for TLS-shape sandboxes:** when the walkthrough surface ships (Doc 62 PRD pending), include a tutorial block at the top. Teach the bootstrap loop in player-facing language. Don't make the player guess how corruption climbs.

### §2.2 — Middle section: NPC scenes index

Card grid of every NPC with a `scenes` object:

```
MC + Stepfather (12) + Stepbrother (15) + Stepgrandfather (6) +
Marcus (5) + Sam (2) + Emma (1) + Jamal (3) + Veronica (3) +
Priest (2) + Gangster (1) + Mr. Matthew (1) + Edward (4) +
Tow Truck Driver (1) + Yacht Captain (1) + Thief (2) + Josh (1) +
Landlord (1)
```

Each card shows the NPC name + scene count. Clicking a card opens the per-NPC drilldown table (§3).

### §2.3 — Bottom section: location scenes index

Same card grid for location-bound scenes — independent of NPCs (random encounters at the location regardless of who's there):

```
City Center (1) + House (1) + Bus (3) + Photo Studio (2) + School (12) +
Park (9) + Gym (3) + Mall (3) + Night Club (2) + Beach (7) + Bar (4) +
Public Pool (2) + Office (2) + Driving School (1) + Thomas's House (2) +
Strip Club (3) + Clandestine Clinic (2) + Restaurant (5) + Police Station (1) +
Hospital (2) + Abandoned Building (1) + Gas Station (1) + Movie Theater (2)
```

Clicking opens per-location scene table with the same columns as per-NPC table.

---

## §3 — The columns (per-NPC drilldown table)

Clicking "Stepbrother" → table with these columns:

| Column | What it shows | Source |
|---|---|---|
| **SCENE** | Display title of the scene (sugarcube-interpolated, e.g., "Stepbrother Bedroom Grope") | `scene.title` |
| **NPC** | NPC slug | `scene.npc` |
| **REQUIREMENTS (NPC)** | NPC stat thresholds: Arousal 🔥, Corruption: 5, Relation: 10 | `scene.requirements.{arousal, corruption, relation}` |
| **REQUIREMENTS (MC)** | Maya stat thresholds: Corruption: 30, Exhibitionism: 10 | `scene.requirementsMC.{corruption, exhibitionism}` |
| **CHANCE** | Dice probability when reqs met (20%, 25%, 33%, 100%) | `scene.chance` |
| **GUIDE** | Natural-language trigger recipe | `scene.guide` |
| **STATUS** | 🔒 Locked / ✅ Completed | `scene.unlocked` (lifetime flag) |

### Example row (verbatim from in-game panel)

| SCENE | NPC | REQUIREMENTS (NPC) | REQUIREMENTS (MC) | CHANCE | GUIDE | STATUS |
|---|---|---|---|---|---|---|
| Sleep with Stepbrother | Stepbrother | Arousal: 🔥, Corruption: 10 | Corruption: 30 | 100% | Go to Stepbrother bedroom late at night and ask to sleep with him | 🔒 Locked |

**Every column is data-driven.** No author-time per-scene customization beyond filling the `scene` object fields. The walkthrough is generated from the data, not authored as a separate UI surface.

### Implication for TLS-shape sandbox engine

The walkthrough rendering depends on the canvas having structured metadata:
- **Display title:** `canvas.name` (already in TLS schema)
- **NPC reqs:** `canvas.trigger.conditions.items[]` where `subject = "npc"`
- **MC reqs:** `canvas.trigger.conditions.items[]` where `subject = "player"`
- **Chance:** `canvas.trigger.chance` (Lane 2 random) OR derived from `substitutions[].chance` (Lane 3) OR 100% (Lane 1 / Lane 4)
- **GUIDE:** the `canvas.guide` field — currently pending Doc 62 PRD per `00_LEGACY_IGNORE.md`
- **STATUS:** derived from `setup.trigger_history[canvas.id].total > 0` (already in TLS engine)

When Doc 62 ships (`guide` field as a parsed canvas attribute), the walkthrough surface becomes authoring-trivial — render the existing canvas metadata in a table.

---

## §4 — The `guide` field convention per lane

From Doc 56 R5 (`doctrine/04_authoring_rules.md` D56-R5) + RTS walkthrough conventions verified across 130+ scenes.

The GUIDE string names the lane in the prose:

| Lane | Phrasing convention | RTS example | TLS example |
|---|---|---|---|
| **Lane 1 — Hub button** | "Visit X" / "Go to Y and Z" | "Go to your Stepbrother bedroom and have sex with him" | "Visit Frank in his kitchen during breakfast" |
| **Lane 2 — Location-entry random** | "Walk into X" / "Go to Y" (with conditions) | "Go to your bedroom" | "Walk into the kitchen late at night" |
| **Lane 3 — Dispatcher substitution** | The chore name, then "while X" | "Masturbate at shower at the house bathroom" / "Wash the dishes" | "Make tea in the kitchen while Frank is home" |
| **Lane 4 — Capstone** | The narrative milestone | "Go to Stepbrother bedroom late at night and ask to sleep with him" | "After the catch, return to Frank's bedroom in the evening" |

### Style rules for GUIDE strings

- **Player-facing.** Second person or Maya-third. Not author-side metadata.
- **Short.** One sentence. Not a marketing line; a recipe.
- **Concrete.** Names the location + chore + NPC condition. NOT "explore the kitchen" — "Wash dishes in the kitchen while Frank is home."
- **No mechanics jargon.** "while corruption ≥ 25" → "after the catch" (the player-facing flag name).

### Anti-patterns

- **Vague GUIDE:** "Spend time with him" — doesn't tell the player WHERE / WHEN / WHAT activity.
- **Author-side metadata:** "Lane 3 dispatcher inside activity_shower" — that's debug info, not a recipe.
- **Numbers / schedules:** "Go to the kitchen between 17:00-19:30 with corruption 25+" — schedules + numbers surface from canvas metadata; GUIDE stays in-fiction language.

---

## §5 — `<<NotifyCorruption N>>` — failure-as-information

P2 + P7 combined produce a specific UI pattern: the locked-click toast that publishes the threshold.

### §5.1 — Source pattern (5+ widget verifications)

Doc 13 §7.4. Reading widget definitions across many scenes (`JimDM`, `RichardDM`, `EdwardDM`, `EdwardSecondDateDM`, `EdwardThreesomeDM`, `RichardSecondPhotoShootDM`):

```twine
<<widget 'JimDM'>>
    ... pitch dialogue ...
    <<if getCorruptionLevel() >= 4>>
        <<linkreplace "Accept the proposal">> ... unlock film studio ... <</linkreplace>>
    <<else>>
        <<linkreplace "I can't do this">>
            <<Speech Player "I'm sorry but I can't do that">>
            <<Speech Jim "I understand, if you change your mind, you can contact me.">>
            <<NotifyCorruption 4>>      /* always in ELSE branch, N matches the if-threshold */
        <</linkreplace>>
    <</if>>
<</widget>>
```

**`<<NotifyCorruption N>>` is a UI hint widget that displays "you need corruption level N for this."**

Verified across 5+ widget definitions. Always called in the ELSE branch with N matching the required level. Used in DM widgets, in `BrotherBedroom` hub button handlers, etc.

### §5.2 — What it is NOT

**It is NOT a corruption-adder.** Doc 13 §11 Correction 3.

Live verified: clicked "Have sex with him 🔥" at MC corruption 0 → source has `<<NotifyCorruption 4>>` in that branch → no stat change after. The "rejection trains the player" loop does NOT exist.

**Failure is information, not progress.** The player still has to actually do the corruption-raising mechanic (masturbate / accept paid date / etc.). RTS doesn't shortcut progression via locked-click farming.

### §5.3 — TLS analog

TLS `locked_text_threshold` field on `TemplateChoice` (shipped 2026-05-06). Per-choice `show_when_locked = true` + `locked_text = "..."` + optional `locked_text_threshold = "..."` renders the choice greyed-out + click-to-toast pattern.

```toml
[[canvases.nodes.exit_block.choices]]
text = "Suck him"
show_when_locked = true
locked_text = "I need to know him better first"
locked_text_threshold = "Maya's corruption: 35+"
conditions = { items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 35 },
] }
nodeId = "loop_franks_bedroom_finisher"
```

When the player clicks at corruption < 35, the toast publishes "Maya's corruption: 35+". Zero stat effects. Zero flag effects. Pure threshold-publish.

See `schema/01_engine_capabilities.md` §10.4–§10.5 for the engine surface.

---

## §6 — Doc 62 PRD (current engine status)

**Status:** doctrine-locked + schema-pending. The TLS walkthrough surface is not yet shipped.

### §6.1 — What's shipped

The data primitives EXIST in the engine:
- Canvas `id` + `name` + `description` (via `TemplateCanvas`)
- Canvas trigger conditions (`TemplateTrigger.conditions`)
- Trigger schedules (`TemplateTrigger.schedules`)
- NPC schedules (`TemplateNPCSchedule`)
- Cooldown tracking (`setup.trigger_history`)
- `formatCanvasConditions` runtime (`v2.py:7043`) — renders condition blocks as human-readable strings

### §6.2 — What's NOT yet shipped (Doc 62)

- **`canvas.guide` field parser.** The doctrine-locked field is not yet a parsed dataclass attribute (Doc 56 R5 noted in §4 above). Author should still emit `guide = "..."` — the validator tolerates the field. When Doc 62 ships, every canvas's `guide` becomes the published-catalog recipe.
- **The walkthrough UI surface itself.** No `:: Walkthrough` passage in TLS. When the catalog UI ships, it renders the table from existing canvas metadata + the `guide` field.

### §6.3 — Held per Doc 66 §10

Doc 62 PRD is in the held list per Doc 66 (the prompts_v2/ rewrite pivot). LO will scope when:
- Next NPC authoring session demands `guide` backfill
- OR catalog UI prioritized over other Phase 2+ work

**For prompts_v2/ generated games:** every canvas authored ships with `guide = "..."` from day 1, so when Doc 62 ships the data is already populated and the catalog surface lands trivially.

---

## §7 — What TLS borrows vs differs from RTS Walkthrough

### §7.1 — TLS borrows (current TLS Quests engine)

- **Per-NPC scene table organization** — TLS V2 Quests engine groups quest cards per NPC (Frank section, Marge section, etc.). Mirrors RTS Walkthrough's "Stepbrother (15)" / "Marcus (5)" cards.
- **Status indicators** — TLS quest cards have visual frames (✓ Arc complete / 🔓 Ready / 🎯 To advance bullets). Maps to RTS's 🔒/✅.
- **Player-facing trigger recipes** — the GUIDE string convention (Doc 56 R5 / D56-R5 in `doctrine/04_authoring_rules.md`).
- **`locked_text_threshold` publishing** — direct port of `<<NotifyCorruption N>>` pattern.

### §7.2 — TLS differs (intentional)

- **TLS V2 Quests is ACTIVE quest cards only.** Doesn't render a per-NPC full catalog. RTS Walkthrough shows ALL scenes (locked + unlocked) for every NPC.
- **TLS has Maya-voice narrative copy.** Quest cards have `text` / `ready_text` / `tip` in Maya's interior voice. RTS Walkthrough is data-only — no narrative copy.
- **TLS hides stage trait.** Per Doc 68 §9 — stage NEVER surfaces. RTS's relation column shows raw values; TLS shows in-fiction equivalents only.

### §7.3 — What TLS SHOULD borrow when Doc 62 ships

Per Doc 13 §14 implications-for-TLS:

| Pattern | RTS source | TLS status | When Doc 62 ships |
|---|---|---|---|
| Published walkthrough with full scene table | §6 | Partially (V2 Quests is active cards only) | Extend QuestsPage with a per-NPC scene table view |
| Notification-as-threshold-hint | §7.2 / §7.4 | Variable — some TLS gates do this | Standardize: every gated button should publish its threshold via `locked_text_threshold` |
| Per-scene `guide` field | §3 / §6 | Doctrine-locked, schema-pending | Doc 62 PRD ships the field; backfill on Frank slice (28 canvases) |
| Cross-NPC scene branching (`SellingMyStepsister`) | Doc 13 §7.2 | Not used | Consider for arc convergence moments (e.g., Frank → Diana brought-in capstone) |

---

## §8 — TLS slice walkthrough deferrals

Per Doc 13 §14 cautions:

### Caution 1 — Walkthrough requirements aren't strict gates

Per Doc 13 §11 Correction 1: the walkthrough's "REQUIREMENTS (MC)" column is a **suggested threshold for the FULL content version**, not an entry gate. Player can stumble into scenes early and get a teaser; full content unlocks later.

**Implication for TLS:** the published catalog needs to communicate "this scene has a teaser at low stats + full content at high stats." TLS could be MORE transparent than RTS by surfacing content-tier thresholds explicitly (e.g., "Sleep with Stepbrother — basic version: relation 10+. Full version: relation 25+."). Or TLS could intentionally hide tier ladders to preserve the come-back-later loop. **LO call when Doc 62 ships.**

### Caution 2 — Deterministic scenes also have stat-tier branching

Per Doc 13 §16 Finding 2: walkthrough's `CHANCE: 100%` means the trigger always fires when reqs met, but the *content within* still gates by stats. A player can "unlock" a scene mechanically and still get a truncated/rejection version.

**Implication for TLS:** scene "completion" status is binary (✓ / 🔒) but content density isn't. The walkthrough surface should communicate this distinction — possibly via a "see full content?" indicator on completed scenes that still have tier-gated branches.

### Caution 3 — Scrollable / paginated UI

RTS Walkthrough has ~130 scenes total. Single-page rendering may not scale beyond ~50 scenes per NPC. TLS slice scope (8-12 NPCs × 5-30 canvases each) needs to think about UI organization upfront.

**Held for Doc 62 PRD scope.**

---

## §9 — Cross-references

### Sibling reference files

- `reference/01_rts_overview.md` §6.2 — Walkthrough panel surface (broad context)
- `reference/02_rts_scene_catalog.md` — the per-NPC scene tables that the Walkthrough renders
- `reference/04_rts_hud_world_model.md` — the sidebar (HUD) doctrine; sibling surface to the Walkthrough

### Sibling doctrine files

- `doctrine/01_rts_principles.md` P2 — transparent gating, not hidden progression
- `doctrine/01_rts_principles.md` P7 — don't punish trying (`<<NotifyCorruption N>>` doctrine)
- `doctrine/04_authoring_rules.md` D56-R5 — every canvas declares a `guide` string

### Source

- `28th_april_TLS_Phase2_Redesign/13_Road_To_Success_Reference.md` §6 — Walkthrough panel doctrine source
- `28th_april_TLS_Phase2_Redesign/24_RTS_Three_Lanes_Repeatable_Activities.md` §5 — discoverability doctrine
- `28th_april_TLS_Phase2_Redesign/56_RTS_Principles_and_TLS_Alignment_Doctrine.md` P2 — transparent gating principle source
- `28th_april_TLS_Phase2_Redesign/62_Canvas_Guide_Field_PRD.md` — engine work to ship the `guide` field (held)

### Engine source

- `WalkthroughV2` passage (`game_explorations/rts-arc-trace/passage_catalog.json`) — 4738 chars of canonical rendering logic
- `WalkthroughTable` widget — the per-NPC table renderer
- `formatCanvasConditions` (`v2.py:7043`) — TLS analog renderer (currently feeds `show_when_blocked` text, will feed walkthrough surface when Doc 62 ships)

---

**End of file.** Next: `reference/04_rts_hud_world_model.md` for the sidebar (HUD) doctrine.

═══════════════════════════════════════════════════════════════════════════════

## 22. 04_rts_hud_world_model

**Source:** `prompts_v2/reference/04_rts_hud_world_model.md`

---

# Reference 04 — RTS HUD = World Model (Sidebar Doctrine)

**Sources:** Doc 56 P10 (HUD = world model principle); `game_explorations/rts-arc-trace/ui_map.json`; Doc 64 PRD (Sidebar NPC Location Radar — held); Doc 49 (body-state vs progression distinction); Doc 68 §8 (per-arc-shape sidebar visibility).
**Authority:** Reference. P10 evidence base.
**Purpose:** Document the RTS sidebar as the canonical "HUD = world model" UI surface — what it surfaces continuously, what TLS needs to mirror, what the per-arc-shape visibility doctrine is.

This file is the source-of-truth for `doctrine/01_rts_principles.md` P10 + `doctrine/04_authoring_rules.md` D56-R4 (sidebar surfaces NPC state) + `doctrine/09_trait_catalog.md` §8 (per-arc-shape visibility defaults).

---

## §1 — The HUD is the world model (P10)

Doc 56 P10:

> The player has to be able to SEE the world. Where every NPC is. What time it is. What clothes they're wearing. What money they have. The right sidebar IS the world surfaced to the player. **Without this radar, Lane 3 stops working entirely** (the room doesn't tell you the NPC is here; the sidebar does).

The HUD does the heavy lifting (P1). Each click is light in prose because the player's brain is loaded by what the sidebar continuously surfaces, not by what the scene reads like.

### §1.1 — Why P10 is load-bearing for Lane 3

Lane 3 = dispatcher substitution = "Maya was doing X and NPC happened" (`doctrine/02_three_lanes_plus_capstone.md` §4). The whole "you're doing X and he happened" texture depends on the player having situational awareness to choose X knowing it might collide with him.

Without per-NPC location radar, the player can't answer:
- "If I shower now, will Frank walk in?"
- "Should I wash dishes now or wait until Frank's home?"
- "Frank's in the kitchen — should I make tea?"

**Lane 3 becomes undiscoverable.** Players who don't check the sidebar can't plan against the dispatcher. The mechanism still works (dice roll inside the chore), but the player can't predict it without the HUD telling them where the NPC is.

### §1.2 — Live verification (Doc 56 P10 evidence)

> Right sidebar continuously renders Time (Early Morning, Monday, Clear weather), Quest pin, and per-NPC rows (Stepfather: Kitchen / Arousal / Corruption / Stepbrother: Bathroom / Arousal / Corruption / Stepgrandfather: Bedroom / Arousal / Corruption). Updates every tick. No menu click required to check NPC state.

Captured live across multiple RTS sessions. Per-NPC location radar is the most load-bearing single piece of UI for an RTS-shape sandbox.

---

## §2 — What the RTS sidebar continuously surfaces

Per `game_explorations/rts-arc-trace/ui_map.json` + live observation. The right sidebar renders:

### §2.1 — Top section: time + chrome

- **Time band:** "Early Morning" / "Morning" / "Afternoon" / "Evening" / "Night" / "Late Night"
- **Day:** "Monday" / "Tuesday" / ... / "Sunday"
- **Weather:** "Clear" / (other bands when implemented)
- **Chrome buttons:** 📕 Walkthrough / ⚙️ Settings / 🎁 Gallery / 🎯 Quests / 👤 Cheats (dev)

### §2.2 — Middle section: Maya stats (the "selectable list")

| Stat | Display | Notes |
|---|---|---|
| Beauty | "Beauty: 50" (integer) | Accumulating |
| Intelligence | "Intelligence: 12" | Accumulating |
| Fitness | "Fitness: 8" | Accumulating |
| Exhibitionism | "Exhibitionism: 15" | Accumulating |
| Corruption | banded: "Pure" / "Lewd" / "Slutty" / "Whore" + raw points hidden | Banded display (Doc 68 Q2 lock for TLS — 0-100 + 4 bands) |
| Arousal | bar 0–10 | Visual meter |
| Energy | bar 0–100 | Visual meter |
| Money | "$80" | Numeric |
| Outfit | "Casual jeans" | String, derived from `clothing.equipped` |

Maya stats are arranged for player planning. The player looks at this column to answer "can I do X right now?" (energy + outfit gates).

### §2.3 — Per-NPC rows (the radar)

Each in-scope NPC has a row:

```
Stepfather:    Kitchen    🔥  Corruption: 5
Stepbrother:   Bathroom   🔥🔥  Corruption: 12
Stepgrandfather: Bedroom  🔥🔥🔥  Corruption: 18
```

Three fields per row:
- **Location:** current location name (derived via `getNpcLocation(npcId)`)
- **Arousal:** emoji-tier (🔥 = 1-3, 🔥🔥 = 4-6, 🔥🔥🔥 = 7-10) OR integer band
- **Corruption:** integer

**Updates every tick.** No menu click required to check NPC state. The radar is the player's situational awareness for planning Lane 3 attempts + capstone triggers.

### §2.4 — Quest pin

The current active quest title + 1-line summary. Single quest at a time in RTS (with `📜 Quests` button to open the full quest journal).

---

## §3 — Per-NPC location radar (the core P10 surface)

The single most load-bearing piece of UI.

### §3.1 — Why location-only suffices for some NPCs

Antagonist arcs (Diana per `doctrine/03_arc_shapes.md` §7): **location only** surfaces. Awareness/scandal accumulator stays HIDDEN — dramatic surprise depends on the player NOT seeing how close confrontation is.

Why location is enough: the player needs to plan around Diana ("is Diana home? then this is risky") without knowing her current awareness level. The location radar suffices.

### §3.2 — Why location + stats is required for family/ambient

Family/ambient arcs (Brother per RTS; Frank per TLS): **location + arousal + corruption + relation** all surface.

Why all three: the player plans Lane 3 attempts (arousal), Lane 1 escalation (corruption), late-game intimacy (relation). All three are mechanically relevant; all three need to be visible.

RTS verified: Brother / Dad / Grandpa all show arousal + corruption (relation is always 0 for family arcs, so not surfaced).

### §3.3 — Per-arc-shape visibility doctrine (Doc 68 §8)

Per-arc-shape sidebar defaults:

| Arc shape | Sidebar surfaces (default) | Rationale |
|---|---|---|
| **Family/ambient** (Frank, Brother) | location + arousal + corruption + relation | Player plans L3 (arousal), L1 (corruption), late-game (relation). All three mechanically relevant. |
| **Slow-burn family** (Jake) | location + arousal + relation | Corruption stays low in slow-burn arcs by design; surfacing it would mislead the player. |
| **Peer/dating** (Ryan, Marcus) | location + relation | Dating chain is relation-driven. Arousal is bounded + less player-controllable. Corruption isn't meaningful for peer arcs. |
| **Service** (Marge) | location + relation only | Workplace bond is the operative axis. Arousal/corruption don't apply to service register. |
| **Antagonist/witness** (Diana) | location only | Awareness/scandal stays HIDDEN — dramatic surprise depends on player NOT seeing how close confrontation is. |
| **ALL arc shapes** | `stage` NEVER surfaces | Per LO Q1 + Doc 68 §9 — stage is internal-only across all NPCs. |

### §3.4 — Override mechanism

The brief can override the default with reason (per `doctrine/06_design_brief_template.md` §3.2). E.g., a family/ambient NPC whose arousal stays constant by design could hide it. But the override must be documented in the brief.

---

## §4 — Body-state vs progression-state surfacing (Doc 49)

Two distinct stat axes have different surfacing rules.

### §4.1 — Body-state (energy + hygiene) — MUST surface

Per Doc 49 + `doctrine/09_trait_catalog.md` §3.3 + §3.4:

- **`energy`** — render as `trait_status_text` with bands (Exhausted / Tired / Fine / Rested) OR `trait_bar` 0-100
- **`hygiene`** — render as `trait_status_text` with bands (Filthy / Dirty / Fresh / Clean)

**Body-state MUST surface.** The player needs to know when to sleep/shower. Hiding body-state means the player can't plan basic self-care.

### §4.2 — Progression-state — banded or hidden

- **`corruption`** — render as `trait_words` (banded: Pure / Lewd / Slutty / Whore). Raw 0-100 number HIDDEN.
- **`arousal`** — render as `trait_bar` (0-10 visual meter) with optional bands (Cold / Warm / Hot / Burning).
- **`money`** — render as numeric ("$80") or `trait_words` if banded.
- **`exhibitionism` / `fitness` / `intelligence` / `beauty`** — Tier 2 traits. Render only when the game's arc/setting uses them. `trait_bar` 0-100 OR hidden.

### §4.3 — Internal-only (NEVER surface)

- **`stage`** — per Doc 68 §9. Stage NEVER renders. Engine should not even know how to render it. Player feels stage progression through what the world DOES (new menu items appear, NPC behavior shifts, location access opens), NOT through a stage number.
- **Antagonist `awareness`** — per Doc 30 §6 + Doc 68 §8. Hidden by design.

### §4.4 — Sidebar item type doctrine

Per `schema/01_engine_capabilities.md` §8:

| `type` | Use case |
|---|---|
| `"trait_words"` | Banded prose label (4 named bands for corruption). Raw number hidden. |
| `"trait_bar"` | Numeric bar with optional band-text overlay + color tiers. For arousal, fitness, beauty, exhibitionism (when game uses them). |
| `"trait_status_text"` | Banded body-state text (Filthy/Dirty/Fresh/Clean). Renders nothing when no band matches. For energy + hygiene. |
| `"trait_decay_warning"` | Amber warning when a decaying trait dropped today + within range of a band gate. Sibling of `trait_status_text`. |

---

## §5 — TLS sidebar — current state (2026-05-28 slice)

Per `doctrine/01_rts_principles.md` §3 audit, TLS sidebar currently has:

1. **Arousal trait_bar** (Maya) — ✅ shipped
2. **Hygiene trait_status_text** (Maya) — ✅ shipped
3. **Energy trait_status_text** (Maya) — ✅ shipped
4. **Passes** (Maya inventory) — ✅ shipped
5. **Inventory** (Maya items) — ✅ shipped

**Zero NPC state surfaced.** This is the P10 misalignment (`doctrine/01_rts_principles.md` §3 audit row: 🔴 High severity).

### §5.1 — What's missing

- **Per-NPC location radar** for Frank / Diana / Jake / Ryan / Marge / Cookie
- **Per-NPC arousal + corruption + relation** per arc-shape doctrine (§3.3 above)
- **Time-band display** (currently shows 24-hour clock; RTS-style band display deferred)
- **Quest pin** (TLS V2 Quests engine shipped per-NPC quest cards but no single-pin sidebar item)

### §5.2 — Engine primitive already exists

`setup.getNpcLocation(npcId)` at `v2.py:2923` already computes NPC location from the NPC's `[[npcs.schedules]]` block. The engine surface is ready; sidebar authoring just needs to call it.

**The blocker is the sidebar item type:** TLS doesn't yet have a `"npc_location"` sidebar item type. Doc 64 PRD specs this.

---

## §6 — Doc 64 PRD (Sidebar NPC Location Radar — held)

Doc 64 PRD specs the sidebar item type for per-NPC location radar. Currently held per Doc 66 §10 (the prompts_v2/ rewrite pivot).

### §6.1 — Proposed schema

```toml
[[sidebar_items]]
type = "npc_location"
npc_id = "npc_frank"
label = "Frank"
# Optional secondary stat displays per arc-shape default
stats = ["arousal", "corruption", "relation"]
```

The item renders:
```
Frank — Kitchen
  Arousal: 🔥🔥  Corruption: 12  Relation: 8
```

### §6.2 — When Doc 64 unlocks authoring

Per Doc 65 §3 row: Doc 64 PRD scoped when:
- Phase 2 polish prioritized OR
- Lane 3 discoverability becomes a blocker in playtest

For prompts_v2/ generated games: every game's `[[sidebar_items]]` block should emit `npc_location` items for in-scope NPCs from day 1. When Doc 64 ships, the data is already authored.

**Authoring discipline:** assume Doc 64 ships. Author `npc_location` sidebar items in the brief's lane map. The validator will tolerate the type even before it's parsed.

---

## §7 — What TLS borrows vs differs from RTS HUD

### §7.1 — TLS borrows

- **Right-side persistent sidebar** (TLS uses left + right; right is the world-model panel)
- **Banded `trait_words`** for corruption (Doc 68 Q2 lock — Pure/Lewd/Slutty/Whore for player corruption 0-100)
- **`trait_bar`** for arousal (Doc 40 lock — 0-10 with bands)
- **`trait_status_text`** for body-state (Doc 49 — energy + hygiene)
- **Per-arc-shape visibility** (Doc 68 §8 — refinement of RTS's flat "show everything for family")
- **Time + day chrome** (TLS shows day + 24-hour time; RTS uses 6-band model)

### §7.2 — TLS differs (intentional)

- **TLS hides stage trait.** Per Doc 68 §9 — internal-only.
- **TLS hides antagonist awareness.** Per Doc 30 §6 + Doc 68 §8 — dramatic surprise.
- **TLS banded corruption (0-100, 4 bands).** RTS uses 0-200 with 5-band points→level derivation. Doc 68 Q2 simplified for TLS.
- **TLS per-arc-shape stat visibility.** RTS surfaces all stats for all family NPCs flat; TLS differentiates per arc shape per Doc 68 §8.
- **TLS uses 24-hour clock** in slice. RTS uses 6-band model (EM/M/A/E/N/LN). Doc 30 §4.3 open question: keep 24-hour or migrate to bands.

### §7.3 — What TLS SHOULD borrow when Doc 64 ships

- **Per-NPC location radar** — load-bearing per P10. Without it Lane 3 becomes undiscoverable.
- **NPC arousal display per arc-shape default** — family/ambient (Frank) gets arousal surfaced; service (Marge) doesn't.
- **Tick-frequency updates** — every passage transition, not just hourly.

---

## §8 — Sidebar item authoring checklist

For each new TLS slice / prompts_v2 generated game, the sidebar block should declare:

### §8.1 — Maya state (mandatory)

- [ ] `trait_words` for corruption (banded Pure/Lewd/Slutty/Whore)
- [ ] `trait_bar` for arousal (0-10 with bands)
- [ ] `trait_status_text` for energy (banded Exhausted/Tired/Fine/Rested)
- [ ] `trait_status_text` for hygiene (banded Filthy/Dirty/Fresh/Clean)
- [ ] Numeric display for money (with currency symbol)

### §8.2 — Tier 2 stats (declare only if game uses them)

- [ ] `trait_bar` for fitness (if exercise/gym mechanic exists)
- [ ] `trait_bar` for exhibitionism (if flash/cam arcs exist)
- [ ] `trait_bar` for intelligence (if school/study mechanic exists)
- [ ] `trait_bar` for beauty (typically hidden — derived from worn_beauty)

### §8.3 — Per-NPC radar (when Doc 64 ships — author against the future shape)

For each in-scope NPC:

- [ ] `npc_location` item with `npc_id`
- [ ] `stats` array per arc-shape default:
  - Family/ambient: `["arousal", "corruption", "relation"]`
  - Slow-burn family: `["arousal", "relation"]`
  - Peer/dating: `["relation"]`
  - Service: `["relation"]`
  - Antagonist: `[]` (location only)

### §8.4 — DO NOT surface

- [ ] No `stage` sidebar items for ANY NPC
- [ ] No `awareness` / `scandal_level` for antagonist NPCs
- [ ] No flags directly (use `trait_words` bands derived from flags if needed)

---

## §9 — Why HUD discipline is hard

The HUD's job is to surface state continuously. The temptation is to show everything — but Doc 68 §8 + the per-arc-shape doctrine specifies what NOT to surface:

- Stage as opaque progression (player feels it through content, not numbers)
- Antagonist awareness (the surprise IS the dramatic engine; surfacing it ruins the arc)
- Internal author-side metadata (which canvases are still locked, etc.)

**The HUD is the world model — but the world model the PLAYER experiences, not the world model the AUTHOR knows.**

Authoring discipline: when adding a new sidebar item, ask:

1. Does the player NEED this to plan their next action? → surface
2. Does surfacing this spoil dramatic surprise? → hide
3. Is this player-facing progression or author bookkeeping? → if bookkeeping, hide
4. Does this match the per-arc-shape default? → if not, document the override in the brief

---

## §10 — Cross-references

### Sibling reference files

- `reference/01_rts_overview.md` §6.3 — sidebar surface (broad context)
- `reference/03_rts_walkthrough_panel.md` — companion surface (Walkthrough = published catalog; HUD = world model)

### Sibling doctrine files

- `doctrine/01_rts_principles.md` P10 — HUD = world model principle
- `doctrine/04_authoring_rules.md` D56-R4 — sidebar must surface NPC state for in-scope NPCs
- `doctrine/09_trait_catalog.md` §8 — per-arc-shape sidebar visibility doctrine
- `doctrine/09_trait_catalog.md` §9 — stage trait special-handling (NEVER surface)

### Source

- `28th_april_TLS_Phase2_Redesign/56_RTS_Principles_and_TLS_Alignment_Doctrine.md` P10 — principle source
- `28th_april_TLS_Phase2_Redesign/64_Sidebar_NPC_Radar_PRD.md` — engine work to ship per-NPC location item (held per Doc 66 §10)
- `28th_april_TLS_Phase2_Redesign/49_Story_Goals_vs_Sidebar_Doctrine.md` — body-state vs progression-state distinction
- `28th_april_TLS_Phase2_Redesign/68_Trait_Catalog.md` §8 — per-arc-shape visibility table source

### Engine source

- `setup.getNpcLocation(npcId)` (`v2.py:2923`) — computes NPC location from schedules; ready for sidebar consumption
- `game_explorations/rts-arc-trace/ui_map.json` — RTS HUD chrome catalog (P10 evidence)
- `template_import.py:2382-2547` — sidebar item validator (rejects undeclared traits with hard error)

---

**End of file.** Next: `schema/03_example_toml.md` for the TLS Frank slice canonical TOML examples.

═══════════════════════════════════════════════════════════════════════════════

## 23. 01_game_book_prompt

**Source:** `prompts_v2/stages/01_game_book_prompt.md`

---

# Stages 01 — Game Book Authoring Prompt (Stage 1)

**Status:** LLM-consumed pipeline prompt. Stage 1 of 2.
**Replaces:** `prompts/game_book_prompt_v6.txt` (frozen 2026-04-19; pre-Doc-24 vocabulary; ENI persona register).
**Input:** game concept (LO's high-level pitch — setting, themes, 4–6 NPC sketches, intended player loops).
**Output:** structured design book (markdown) that `stages/02_toml_generation_prompt.md` consumes.

This prompt is the system instruction set you (the authoring LLM) receive when LO submits a game concept. Read it before responding. The design book you produce will be consumed by the Stage 2 prompt to emit valid TOML.

---

## §0 — Mode switch (LOAD-BEARING)

**Before reading further, do this:**

> ENI persona OFF.
> TLS game register ON.
> Doctrine memory + canonical docs override persona instincts.
> When in doubt about a craft choice, default to MORE-flat / FEWER-items / EMPTIER-lanes, not the reverse.

If a craft instinct conflicts with project doctrine, project wins every time. CLAUDE.md is ignored for this task — `prompts_v2/00_LEGACY_IGNORE.md` §3.6 + Doc 30 §3 AUTHORITY DECLARATION.

Why this switch is load-bearing: the Marge session (Doc 54) cost ~8 hours to a single failure — ENI persona's literary-IF instinct overrode RTS-flat doctrine. The override mechanism is explicit. Declare it at the start of the task; re-declare it whenever you catch persona drift.

---

## §0.5 — Scope mode declaration (read before authoring)

This prompt supports two scope modes:

- **`scope_mode: full_game`** (DEFAULT) — author the COMPLETE game. Per-arc-shape FULL canvas budgets per `doctrine/03_arc_shapes.md` §2 (family/ambient 25–35, slow-burn 10–15, peer/dating 8–12, service 6–10, antagonist 6–10). Full Stage 0→4 trajectories per NPC. Full capstone chains per Doc 57. Phase 2+ Strategic Scope decisions (Doc 65) surface as interactive Q&A — see §0.5.2 below.
- **`scope_mode: slice`** — author a shippable validating chunk. ~10–14 day playable window. 1 NPC at full depth (gold standard) + 4–5 NPCs at minimum-contract depth. Locked-visible escalation rungs telegraph deferred arcs. Phase 2+ deferrals listed explicitly (no Q&A — all four default to defer).

### §0.5.1 — Read scope_mode from concept input

LO's concept input should declare `scope_mode: <full_game | slice>` near the top. If the declaration is present, proceed to §0.5.2 (full_game) or skip directly to §1 (slice). If the declaration is ABSENT, default to `scope_mode: full_game` and proceed to §0.5.2.

### §0.5.2 — Interactive Phase 2+ Q&A flow (full_game mode only)

Before authoring §1 of the design book, you must resolve the four Doc 65 Phase 2+ Strategic Scope decisions. Scan LO's concept input — if any of the four is explicitly declared (`pregnancy = include`, `scandal = defer`, etc.), record the call and skip that question. For each UNRESOLVED decision, ask LO ONE question at a time. Wait for the answer. THEN ask the next. Do NOT batch the four questions into one message.

The four decisions in order:

1. **Pregnancy** — include in this game OR defer to a future amendment?
2. **Scandal arc** — include OR defer?
3. **Gallery system** — include if 9+ once-only capstones planned (Doc 65 trigger)?
4. **Tracker / progress system** — include with Doc 62 `guide` backfill?

Question template (one at a time):

> **Phase 2+ decision needed: [Pregnancy/Scandal/Gallery/Tracker]**
>
> **Context:** [One-paragraph summary from Doc 65 — engine entry points + ripple + design implications. E.g., for pregnancy: "Affects every sex scene's bareback framing, requires pregnancy stat + variant prose for retrofit-affected scenes, gates Tier 5+ breeding talk per doctrine/08."]
>
> **Doctrine recommendation:** [include OR defer + 1-sentence reasoning per Doc 65 per-decision row]
>
> **Your call?**

After LO answers each, record the call. After all four are resolved (or skipped because the concept declared them), proceed to §1. Do NOT begin authoring §1 of the design book before all four decisions are resolved.

**When an inclusion is `include`, the design book must name HOW it's mechanized — not just that it's on.** An "included" system that's never wired ships dormant (the build validator won't catch it). For each `include`, the brief must specify:
- **Pregnancy:** the setter trigger (e.g. an `had_unprotected_sex` flag from first-full-sex capstones → a hidden onset canvas that sets `player.pregnancy`) AND which NPCs get pregnant-variant content. Every NPC that can father needs an ongoing sex surface for the variants to attach to (see the peer/dating ongoing-hub note below).
- **Scandal:** the awareness accumulator owner (an antagonist/witness NPC), its writers (which beats raise awareness), and the confrontation capstone's threshold + location (a shared/public space the player crosses — `doctrine/10` §5).
- **Gallery / Tracker:** confirm the trigger condition is actually met (e.g. 9+ once-only capstones for gallery) and name the per-canvas field (`guide` for tracker).

(Late Shifts shipped pregnancy "included" but with no setter → all breeding content was dead until a setter was retro-wired.)

If LO declares `scope_mode: slice`, SKIP §0.5.2 entirely. Slice authoring defers all four to Phase 2+ by default; no Q&A needed.

### §0.5.2a — Downstream emission at full_game (FYI for design book §1 header)

At `scope_mode: full_game`, Stage 2 emits **phased TOML** (7 phase files across 7 responses) per `stages/02_toml_generation_prompt.md` §12.5. LO assembles via `scripts/merge_toml_phases.py games/<game_slug>` after all phases ship. This affects nothing in Stage 1's output — the design book is still a single markdown file — but the design book §1 should name the intended `game_slug` (lowercase, underscores) so the folder convention is locked: `games/<game_slug>/` with `concept.md` (Stage 1 output) + `toml_phases/0_*.toml ... 7_final_game.toml` (Stage 2 phased output + merged).

At `scope_mode: slice`, Stage 2 emits single TOML (one response) — no phased breakdown, no merge step.

### §0.5.3 — Non-Doc-65 clarifying questions (alongside or instead of §0.5.2)

If the concept is missing critical NON-Doc-65 information (cast count, kink ceilings, time model, economic engine specifics), ALSO ask 1–3 clarifying questions before authoring. Do NOT invent answers — that's the Marge §2.3 question-avoidance failure mode (Doc 54).

Order: at `scope_mode: full_game`, ask Phase 2+ Q&A first (§0.5.2), then non-Doc-65 clarifying questions. At `scope_mode: slice`, ask only the non-Doc-65 clarifying questions.

---

## §1 — The job

You are authoring a **design book** for an RTS-shape sandbox game.

### §1.1 — Input shape

LO's concept input is a free-text pitch. Typical shape (you'll see variants):

```
"scope_mode: <full_game | slice>  # If omitted, default to full_game.

Game: <title>. Setting: <where + when>. Player character: <name + brief>.

NPCs (4-6):
- <Name 1>: <role + relationship to player + 1-line fantasy hook>
- <Name 2>: <same>
- ...

Themes: <kink areas the game should explore at full intensity>

# At scope_mode: full_game — Phase 2+ inclusions (optional; if omitted, ask via §0.5.2 Q&A):
Phase 2+ inclusions:
  pregnancy: <include | defer>
  scandal: <include | defer>
  gallery: <include | defer>
  tracker: <include | defer>

# At scope_mode: slice — Phase 2+ deferrals (all four default to defer):
Slice scope: <what ships in the first slice — typically 1 fully-authored NPC + skeletal others>
Phase 2+ scope: <what's deferred — typically pregnancy / scandal / etc.>
"
```

LO may also include: time period (modern / period piece), economic engine (rent / debt / etc.), specific kink ceilings, or "in the style of <existing game>" references. Treat all of these as constraints, not suggestions.

### §1.2 — Output shape

A design book in structured markdown. Each NPC gets its own R7 brief (per `doctrine/06_design_brief_template.md`). The world setup + locations + economic engine + cross-arc table live in shared sections.

Concretely, your output is (scope-conditional — branch sections based on declared `scope_mode`):

```markdown
# <Game Title> — Design Book

**Scope mode:** <full_game | slice>

## §1 World Setup
- Premise (1-2 paragraphs)
- Player character (Maya — adapt name if LO specified)
- Economic engine (rent / income source / etc.)
- [At full_game]   Phase 2+ inclusions (pregnancy / scandal / gallery / tracker — Yes/No per decision, resolved at §0.5.2 Q&A)
- [At slice]       Slice scope (Phase 1) vs Phase 2+ deferrals
- Time model (24h vs 6-band)

## §2 NPC Roster (4-6 NPCs)
[At full_game]
| NPC | Arc shape | Full-arc depth | Vocab ceiling |
|---|---|---|---|
| ... | ... | (canvas count matching per-shape full budget per doctrine/03 §2) | ... |

[At slice]
| NPC | Arc shape | Slice depth | Vocab ceiling |
|---|---|---|---|
| ... | ... | (Fully authored / Skeletal / Sketch / etc.) | ... |

## §3 Locations
- Home hub + sub-locations
- Town hub + sub-locations
- Per-NPC location schedules

## §4 Per-NPC Design Briefs (R7)
- For each NPC, full 10-section R7 brief per doctrine/06

## §5 Cross-arc World State
- [At full_game] Shared flags + scandal/awareness systems per Phase 2+ inclusions (only emit scandal/awareness traits if scandal = include)
- [At slice] Shared flags + scandal/awareness systems (per slice scope)
- Phase 2+ retrofit-compatibility notes (bareback framing — Doc 30 §7.3.1 — applies when bareback default is active per stages/02 §0.5)

## §6 Capstone Chain Map
- Per-NPC chain in order (full chain at full_game; slice-scope subset at slice)
- Cross-NPC bridge scenes (if any)

[At full_game]
## §7 Full-Game Build Plan
- Day 1 bootstrap (per RTS reference/01 §4)
- Per-NPC stage transition milestones (Stage 0→1, 1→2, etc. — when does the player typically hit each?)
- Capstone chain milestones (when does the first capstone fire? when does the chain complete?)
- Phase 2+ system enable points (e.g., pregnancy mechanic activates at Frank Stage 3)
- Endgame state (what does "completed game" look like? per Doc 65 endgame doctrine)

[At slice]
## §7 Slice Build Plan
- Day-by-day flow for the slice
- Day 1 bootstrap (per RTS reference/01 §4)
- Day-N rent / capstone scheduling
```

The Stage 2 prompt reads this output and emits the corresponding TOML.

### §1.3 — Output contract

The design book MUST:

- Cover 4–6 NPCs (no more, no fewer — per Doc 56 P4 + arc-shape mix)
- Assign one arc shape per NPC from the 5 in `doctrine/03_arc_shapes.md` (family/ambient, slow-burn family, peer/dating, service, antagonist/witness)
- Mix arc shapes across the cast (not all family/ambient; not all peer)
- Author one full R7 brief per NPC per `doctrine/06_design_brief_template.md` §2 (10 sections each)
- Declare per-arc vocab ceilings per `doctrine/08_kink_vocab_ceilings.md` §2
- Plan capstone chains per `doctrine/02_three_lanes_plus_capstone.md` §5 + `doctrine/03_arc_shapes.md` §3.5 budgets
- Declare scope mode in the file header (`**Scope mode:** <full_game | slice>`) and stay consistent with it throughout (no mixing slice locked-visible deferrals with full_game authored rungs without explicit justification — `doctrine/07_anti_patterns.md` §3.6)
- At `scope_mode: full_game`: ratify all four Doc 65 Phase 2+ decisions in §1 before authoring §2+
- At `scope_mode: slice`: commit to slice scope vs full-arc trajectory explicitly (locked-visible rungs bridge — Doc 54 §3.6)

The design book MUST NOT:

- Restate doctrine from the prompts_v2 reference corpus (cite, don't restate)
- Include scene-body prose (this is Stage 2's job; Stage 1 is shape spec)
- Author against undefined kink ceilings (blank rows in §8 vocab table = out-of-scope for declared `scope_mode`)
- Pad empty cells in the per-arc-shape distribution table (per `doctrine/03_arc_shapes.md` §9 — empty cells are honest)
- Reach for legacy patterns (see `00_LEGACY_IGNORE.md` for full list)

---

## §2 — Doctrine assumed (cite-only)

This prompt assumes you have read these files in the prompts_v2 corpus:

| File | What it contains |
|---|---|
| `00_LEGACY_IGNORE.md` | Banned vocabulary + redirects (Pattern A–J / 7-driver / archetype-system / whiteboard-goals / Single-NPC-Romance vs Multi-NPC-Parallel-Arcs) |
| `doctrine/01_rts_principles.md` | P1–P10 with RTS evidence cites |
| `doctrine/02_three_lanes_plus_capstone.md` | Lane 1/2/3/4 mechanism + 3 capstone types A/B/C + Pattern F sub-rules F1–F5 |
| `doctrine/03_arc_shapes.md` | 5 arc shapes + per-arc canvas distribution table + per-arc capstone budgets |
| `doctrine/04_authoring_rules.md` | R1–R7 (Doc 56) + R1–R6 (Doc 50 quest cards) + R1–R5 (Doc 57 capstones) + F1–F5 (Pattern F) + R1–R7 (Doc 67 solo activities) |
| `doctrine/05_rts_flat_prose.md` | 8 prose rules + dual register (Lane 1/2/3 RTS-flat vs Lane 4 Tier-3 earned) |
| `doctrine/06_design_brief_template.md` | R7 brief 10-section template + Frank/Marge gold standards |
| `doctrine/07_anti_patterns.md` | 27 failure modes + cross-doc anti-pattern catalog |
| `doctrine/08_kink_vocab_ceilings.md` | Per-arc vocabulary ceilings + 2026-05-16 LO default-explicit pattern |
| `doctrine/09_trait_catalog.md` | Tier 1 + Tier 2 traits + stage internal-only doctrine + Phase 2+ off-limits list |
| `doctrine/10_location_design.md` | Location layering (private/shared/town) + reachability triad + per-arc location footprint — READ before drafting §3 locations |

If you haven't read these, stop and read them before authoring. Citation without comprehension produces drift.

---

## §3 — Reference assumed (cite-only)

| File | What it contains |
|---|---|
| `reference/01_rts_overview.md` | What RTS is + 130+ scene catalog + 3 arc tendencies + bootstrap experience + 4 player surfaces + 3 writing tiers + 5 corrections from live play |
| `reference/02_rts_scene_catalog.md` | Brother (16-surface walkthrough + structural pattern table) / Dad (9) / Marcus (12) / Edward (1 + DM widget) + 6 patterns A–F + cross-NPC distribution + arc-tendency gate-placement |
| `reference/03_rts_walkthrough_panel.md` | P2 transparent gating doctrine + WalkthroughV2 panel contents + 7-column drilldown + guide field convention per lane + NotifyCorruption pattern |
| `reference/04_rts_hud_world_model.md` | P10 HUD = world model + per-NPC location radar + body-state vs progression-state surfacing + per-arc-shape visibility doctrine |

These describe the canonical reference game (Road to Success). Cite them when making cast-balance + mechanism + UI surface decisions.

---

## §4 — Step-by-step authoring process

8 steps. Don't skip ahead — each step's output feeds the next.

### Step 1 — Read the concept

Read LO's pitch carefully. Pay attention to:

- **Scope mode** — `scope_mode: full_game` (default) or `scope_mode: slice`. Detect this FIRST; it changes how Steps 2–8 proceed (full-arc depth vs slice depth per NPC; Phase 2+ Q&A vs deferrals; §7 build plan shape).
- **Phase 2+ inclusions** — at `scope_mode: full_game`, check whether the concept declares any of pregnancy / scandal / gallery / tracker. Unresolved ones drive the §0.5.2 interactive Q&A.
- **Setting / period** — modern small town vs. period piece changes vocab + economic engine + location set
- **Named NPCs** — does LO give 4 or 6? Are there NPC-name suggestions, or just role suggestions?
- **Themes / kink areas** — these map to `doctrine/08_kink_vocab_ceilings.md` rows. Mark which rows are in-scope.
- **Player character** — name, age, background, agency
- **Specific references** — "in the style of RTS Brother arc" / "like Doc 31 Frank" = treat as binding constraint

**Pre-authoring Q&A — order matters:**
1. At `scope_mode: full_game` — run §0.5.2 Phase 2+ Q&A first (one question at a time, wait for answer between each)
2. Either mode — if critical NON-Doc-65 info is missing (cast count, kink ceilings, time model), ask 1–3 clarifying questions BEFORE authoring

Do NOT invent answers to unspecified scope decisions — that's the Marge §2.3 question-avoidance failure mode (Doc 54). Do NOT batch multiple Phase 2+ questions into one message — the doctrine requires one-at-a-time.

### Step 2 — Pick the cast (4–6 NPCs)

The cast composition gates everything downstream. Per Doc 56 P4 — mix arc shapes.

**Process:**

1. Inventory LO's named NPCs (typically 4–6 in the pitch)
2. For each named NPC, propose an arc shape from `doctrine/03_arc_shapes.md` §1 (family/ambient, slow-burn family, peer/dating, service, antagonist/witness)
3. **Mix the shapes deliberately.** A good cast has 3+ distinct shapes (typically 1 family/ambient + 1 slow-burn family + 1 peer/dating + 1 service + 1 antagonist + optional 6th).
4. If LO's pitch leans heavily toward one shape (e.g., 4 family/ambient NPCs), surface this to LO as a flag: "this cast will read all-grindy because all 4 NPCs use the same mechanical rhythm — recommend swapping 1 to peer/dating + 1 to antagonist." Don't author into the imbalance.
5. **Assign depth per NPC per declared scope_mode:**
   - At `scope_mode: full_game`: each NPC ships at its per-arc-shape FULL budget (family/ambient 25–35, slow-burn 10–15, peer/dating 8–12, service 6–10, antagonist 6–10 own + cross-arc appearances). NO "minimum-contract depth" tier — every NPC ships their complete arc.
   - At `scope_mode: slice`: 1 NPC at full depth (gold standard, ~28 canvases if family/ambient) + 4–5 NPCs at minimum-contract depth (~6 canvases each, locked-visible rungs telegraph the rest).
6. Lock the cast in §2 of the design book.

**Decision rule per NPC (per `doctrine/03_arc_shapes.md` §8):**

1. Shares household + saturated proximity register → family/ambient
2. Shares household + sparse revelation-keyed → slow-burn family
3. Separate household + scheduled visits → peer/dating
4. Workplace register + employer/colleague → service
5. Threat/cost-of-other-arcs + confrontation → antagonist/witness

If no shape fits, surface to LO. Don't invent a 6th shape — the corpus doesn't have authoring discipline for it.

### Step 3 — Draft the world setup

§1 of the design book. Cover:

- **Premise.** Why is the player here? What's the inciting situation? Concrete + specific. ~2 paragraphs.
- **Player character.** Name (default "Maya" — adapt if LO specified), age (typically 20-23), background (one sentence), agency frame (what can the player choose?).
- **Economic engine.** Per Doc 30 §4.1 — RTS pattern is rent + first-week deadline. Specifics: rent amount + due day + grace periods. Starting money + first income source.
- **Digital surface (phone) — `doctrine/13_phone_design.md`.** Decide if the game has off-location life worth a phone (NPC texts, a follower/job economy, a private escalation channel). If yes: which app types (most arc games are chat-centric — one `chat` app), the acquisition beat (what sets `purchase_flag`, e.g. reconnecting a cut-off phone at first income), and which NPC arcs get threads. Threads ride arc flags authored in §2; the phone carries arcs, it isn't one. Skip entirely for a single-location game with no off-screen life.
- **Customization (player/NPC personalization) — `doctrine/14_customization_design.md`.** Decide if the player personalizes at game start. **Player:** name + build + a portrait look is the RTS-default opener — include it when the protagonist is a blank-ish self-insert; SKIP it when the protagonist is a written, premise-central named character (retrofitting `@player` across third-person narration fights the grain). **NPCs:** mark an NPC `customizable` (rename + relationship-label picker — the step-relative toggle) only when the relationship framing is a real fantasy axis AND the cost is bounded (the name isn't load-bearing for the premise or baked into structural labels). A dating love-interest is the cheapest candidate; a sibling whose siblinghood *is* the story is the wrong one. If included: every name mention in prose becomes `@player`/`@<npc>` and structural labels get genericized (doctrine/14 §3–§4).
- **At `scope_mode: full_game` — Phase 2+ inclusions.** Per the §0.5.2 Q&A resolutions, declare each of pregnancy / scandal / gallery / tracker as `include` or `defer`. Include = ships in this game with full engine support; defer = locked-visible scaffolding only OR completely absent per LO's call.
- **At `scope_mode: slice` — Slice scope (Phase 1) + Phase 2+ deferrals.** What ships in the first 10-14 day slice? Typically: 1 NPC at full depth (gold standard) + 4-5 NPCs at minimum-contract depth + 1 cross-arc capstone. All four Doc 65 decisions default to defer per `doctrine/09_trait_catalog.md` §6.1.
- **Time model.** 24h clock vs. 6-band model (EM/M/A/E/N/LN). Pick one. Per Doc 30 §4.3 — TLS slice uses 24h; future games can pick 6-band.

### Step 4 — Draft locations + schedules

§3 of the design book. **Read `doctrine/10_location_design.md` first — it's the keystone for this step.** Cover:

- **Home, layered (`doctrine/10` §4).** A private dwelling, the shared building it sits in, and the outside are SEPARATE locations: rooms → private-unit hub → shared-building corridor → exterior root → (walk) → town. Do NOT collapse "the apartment" and "the building corridor" into one hub (the street would open into a bedroom; a neighbor would spawn beside the beds).
- **Town hub** + sub-locations (Main Street → Diner / Shop / Gym / Library / etc.). Home-exterior root + town root are two top-level locations bridged by walk-activity canvases, not by a direct `entry_from` link.
- **Outside locations** (Lake / Woods / etc. — Phase 2+ typically).
- **NPC placement by arc shape (`doctrine/10` §6):** household NPCs inside the private unit; neighbors/witnesses in shared/public space (never the private unit); service at the workplace; peer/dating gets an ongoing Stage-4 hub at the partner's location (not a first-night capstone only).
- **Per-NPC location schedules.** Per `schema/01_engine_capabilities.md` §5.1 — non-overlapping time windows per NPC. **Every schedule window is a promise of a Lane 1 hub (D72-R6):** plan one hub per (location × window), with its rung ceiling set by the location's exposure tier — public = talk/look, semi-private = tease/grope, private = full ladder (D72-R7, `doctrine/04` §6). An NPC with no physical hub (rent/phone-only) carries no schedule.
- **Reachability triad (`doctrine/10` §5) — apply per NPC beat.** For every place an NPC scene happens, confirm NPC-schedule ∩ scene-window ∩ where-the-player-actually-is-and-awake is non-empty. Anchor each NPC's beats where the player *crosses them in the daily loop* (mind sleep/work windows + cross-midnight). The build will NOT catch a dead-on-arrival scene — lock placement here.
- **Locked location ∩ NPC schedule — the unlock contract (`doctrine/10` §5.4).** If an NPC is scheduled at a locked location (`entry_conditions`), the player must first meet them at an OPEN on-ramp whose beat sets the unlock flag — the lock reads as "haven't met / been invited yet." Never make an NPC reachable *only* via a locked location, and never gate a door on a flag only settable behind it. A locked room an already-met NPC routes into (e.g. a back office) is fine only if the lock is legible and falls in off-hours with open-location fallback presence.

For each in-scope NPC, draft their full week schedule (weekdays + weekend variant if needed). Use Doc 31 Frank's schedule as the gold standard (7 entries covering 24h non-overlapping); `doctrine/10` for the full layering + reachability doctrine.

### Step 5 — Author per-NPC R7 brief

§4 of the design book. For each NPC, write a full R7 brief per `doctrine/06_design_brief_template.md` §2 — 10 sections:

1. End-state fantasy (1 paragraph naming what "arc complete" looks like + 3-5 specific signature scenes)
2. NPC voice spec (speech patterns table + per-stage voice samples + per-NPC framing rules + 8+ banned dialogue patterns)
3. Stat ladder + tier mapping (6-tier corruption ladder customized — fewer tiers for non-escalation shapes)
4. Per-rung pretext shapes (4–6 shapes per tier × 6 tiers = 24–36 shapes total for escalation arcs)
5. Lane-by-lane content map (per location: what fills Lane 1 hub / Lane 2 ambients / Lane 3 substitutions / capstones)
6. Capstones (each named with type A/B/C-step + trigger + brief shape + flag writes)
7. Anti-patterns (12+ NPC-specific banned registers)
8. Cross-arc state writes / reads
9. Cross-references
10. Acceptance criteria

**Gold-standard reference:** `28th_april_TLS_Phase2_Redesign/31_Frank_Arc_Design_Brief.md` (family/ambient — 336 lines). For service NPCs, use `28th_april_TLS_Phase2_Redesign/53_Marge_Redesign_Brief.md` (322 lines).

**Length per brief:** 250–350 lines tabular. Don't pad with literary prose. Don't drift into authoring scene PROSE — the brief is shape spec; Stage 2 authors prose.

**Per-arc adaptations** (per `doctrine/06_design_brief_template.md` §6):

- **Family/ambient (Frank-shape):** full 6-tier ladder + all 4 location hubs + Lane 2 ambients per location + Lane 3 substitutions on chore activities + 5 capstone chain
- **Slow-burn family (Jake-shape):** 2-5 stage milestones + dual-path Stage 0→1 via beauty/glance + 1-3 Lane 3 walk-ins keyed to revelation beats + 3-5 capstones
- **Peer/dating (Ryan-shape):** Stage 0-4 relation-driven + 0 Lane 3 + Lane 1 visits at workplace + 3-4 dating-chain capstones
- **Service (Marge-shape):** 1 unlocked tier + locked-visible Phase 3+ rungs + empty Lane 2/3 by shape doctrine (any scope) + 1-3 capstones (hire + mid-arc escalation if vocab allows; cap depends on scope_mode + Phase 2+ inclusions)
- **Antagonist/witness (Diana-shape):** silent awareness accumulator 0-100 + bands (cold/suspicious/knowing/shut-out) + 0 own Lane 3 (appears as interruptor in others') + 1-2 confrontation capstones (Type B Pattern F branches)
- **Phase 3+ scope-out (Cookie-shape):** formal scope-out doc per `28th_april_TLS_Phase2_Redesign/61_Cookie_Phase3_Scope_Out.md` template — NO full brief

### Step 6 — Plan the capstone chain

§6 of the design book. For each NPC + cross-NPC scenes, name:

- **Per-NPC capstones** (per `doctrine/03_arc_shapes.md` §3.5 budgets):
  - Family/ambient: 3-6 capstones (Type A 1-2 + Type B 1-2 + Type C chain 4-5)
  - Slow-burn family: 2-5 capstones
  - Peer/dating: 2-5 capstones
  - Service: 1-3 capstones
  - Antagonist: 1-3 capstones (Type B Pattern F branches)
- **Cross-NPC bridge scenes** (e.g., Diana confrontation triggered by Frank arc completion)
- **Chain order** (which capstone gates which — D50-R4 + D57-R4 chain continuity)
- **Type per capstone** (A linear / B branching / C chain-step) per `doctrine/02_three_lanes_plus_capstone.md` §5

For each capstone, write a 2-sentence brief shape + name the flag writes (what flag does the setter set on exit).

### Step 7 — Lock vocab ceilings

§4 of the design book (inside each NPC brief's §2 voice spec). Per `doctrine/08_kink_vocab_ceilings.md` §2:

For each NPC + each in-scope kink area, declare the ceiling at full intensity (Tier 4-5):

- **Frank — paternal/daddy framing:** FULL DADDY (default per Doc 30 §7.5 row 1)
- **Frank — breeding (Phase 2+):** FULL BREEDING TALK conditional on pregnancy mechanic
- **Anatomical + cum:** MAXIMUM CRUDE DETAIL
- **Roughness/degradation:** FULL ROUGH + DEGRADATION
- **Jake — incest:** FULL INCEST CALLOUTS
- **Diana — cuckold:** FULL CUCKOLD FRAMING
- **Public/exhibitionism:** FULL RISK + ONLOOKER AWARENESS

Per LO 2026-05-16 pattern (`doctrine/08_kink_vocab_ceilings.md` §3): default to maximum-explicit unless LO explicitly says otherwise. Anything softer is the wrong default given the pattern.

**Blank rows = out-of-scope** for the declared `scope_mode`. At slice, blank rows are typical Phase 2+ deferrals. At full_game, blank rows mean LO opted the kink out of the entire game (see `doctrine/08_kink_vocab_ceilings.md` §4.4).

### Step 8 — Emit the design book

Compile §1–§7 into the structured markdown output per §1.2 above. The file should be:

- **At `scope_mode: slice` — 3,000–6,000 words** total (longer for 6-NPC casts with all family/ambient)
- **At `scope_mode: full_game` — 8,000–15,000+ words** total (per-NPC briefs run longer at full-arc depth; capstone chain map grows; §7 Full-Game Build Plan adds stage-transition milestones + Phase 2+ enable points)
- **Per-NPC brief:** 250–350 lines tabular at slice; 400–600 lines at full_game (depth column drives ladder/pretext/lane sections to scale)
- **Cross-arc + capstone chain map:** ~50 lines per NPC's chain at slice; ~80–120 lines at full_game (full chain instead of slice-end subset)
- **Build plan:** ~30 lines (day-by-day) at slice; ~60–80 lines at full_game (day-by-day for opening 14 days + stage-transition milestone schedule + Phase 2+ enable points)

**Delivery:**
- At `scope_mode: slice`: deliver the design book in one response. Don't truncate. If you run long, surface scope concerns BEFORE delivery, not by truncation.
- At `scope_mode: full_game`: full-game game-books run long and may hit max output tokens. If you approach the limit, stop at a CLEAN section boundary (end of §N) and emit a single line: `**[Resume from §N+1 in next message]**`. Then stop. Do NOT truncate mid-section. Do NOT include partial briefs.

---

## §5 — Output format spec

The design book is structured markdown with specific section requirements.

**Scope-mode note for the §5.x worked examples below:** the worked examples (§5.1 file header onward, including the §5.7 cross-arc section and §5.8 build plan) are written in **`scope_mode: slice`** convention — they show the TLS Frank slice authored at slice depth, with locked-visible rungs for Phase 2+ deferrals. This was the corpus's original authoring mode (pre-2026-05-29) and is preserved as the slice-mode exemplar.

**At `scope_mode: full_game`** (the new default), adapt each §5.x example as follows:
- §5.1 file header: replace `**Slice scope:** <N>-day slice` with `**Phase 2+ inclusions:** pregnancy=..., scandal=..., ...` per the §0.5.2 Q&A resolutions
- §5.2 World setup: emit `### Phase 2+ inclusions` block (per §1.2 template) instead of `### Slice scope (Phase 1)` + `### Phase 2+ deferrals`
- §5.3 NPC roster: column header = `Full-arc depth`; canvas counts match per-shape full budgets (family/ambient 25–35, etc.)
- §5.7 Cross-arc: emit full-game scandal/awareness systems if scandal=include; cross-NPC bridges run the full chain instead of "None in slice"
- §5.8 Build plan: title = `## §7 Full-Game Build Plan`; covers day 1 bootstrap + stage-transition milestones + capstone chain milestones + Phase 2+ enable points + endgame state (per §1.2 full_game template)

The lane mechanism (§5.5 per-NPC R7 brief sections), capstone chain shape (§5.6), and per-NPC voice spec all work identically at both scopes — the change is content volume, not shape.

### §5.1 — File header

```markdown
# <Game Title> — Design Book

**Scope mode:** <full_game | slice>
**Author:** ENI (Stage 1 authoring)
**Authority:** Designed per `prompts_v2/` doctrine (Doc 66 corpus, complete).
**Status:** Stage 1 output — consumed by `stages/02_toml_generation_prompt.md` for TOML emission.
**Cast:** <N> NPCs, mix of <shape list>
[At full_game] **Phase 2+ inclusions:** pregnancy=<inc/def>, scandal=<inc/def>, gallery=<inc/def>, tracker=<inc/def>
[At slice]     **Slice scope:** <N>-day slice; Phase 2+ deferrals: <list>
```

### §5.2 — §1 World setup section

```markdown
## §1 World Setup

### Premise

<1-2 paragraphs naming the situation + the player's drive + the economic engine>

### Player character

- **Name:** Maya (or LO-specified)
- **Age:** 20 (or specified)
- **Background:** <one sentence>
- **Agency:** <what can the player choose; what's the loop>

### Economic engine

- **Rent:** $<amount>/period, due <weekday>, <N> grace periods
- **Starting money:** $<amount>
- **First income source:** <NPC arc that pays — typically the service NPC>

[At `scope_mode: slice` — emit both Slice scope + Phase 2+ deferrals blocks below:]

### Slice scope (Phase 1)

- **Duration:** <N>-day slice (typically 10-14 days)
- **Fully-authored NPC:** <NPC name> (gold standard)
- **Minimum-contract NPCs:** <list>
- **Cross-arc:** <e.g., Diana confrontation triggered at slice end>

### Phase 2+ deferrals

<list per Doc 65 + doctrine/09 §6.1 off-limits — pregnancy / scandal / gallery / cross-arc tracker>

[At `scope_mode: full_game` — replace both blocks above with Phase 2+ inclusions, resolved at §0.5.2 Q&A:]

### Phase 2+ inclusions (resolved at §0.5.2 Q&A)

| Decision | Call | Engine entry point / scope impact |
|---|---|---|
| Pregnancy | <include / defer> | <e.g., "include — gates Tier 5 breeding talk at Frank Stage 4+; pregnancy stat + variant scenes ship"> |
| Scandal arc | <include / defer> | <e.g., "include — awareness 0–100 accumulator + 4 confrontation branches Type B Pattern F"> |
| Gallery system | <include / defer> | <e.g., "include — 9+ once-only capstones authored; gallery item ships with thumbnail + replay"> |
| Tracker / progress | <include / defer> | <e.g., "defer — Doc 62 `guide` PRD held"> |

### Time model

<24h clock OR 6-band model EM/M/A/E/N/LN; rationale>
```

### §5.3 — §2 NPC roster section

[At `scope_mode: slice` — column header = "Slice depth":]

```markdown
## §2 NPC Roster (<N> NPCs)

| NPC | Arc shape | Slice depth | Fantasy (1 line) | Vocab ceiling |
|---|---|---|---|---|
| Frank | Family/ambient | Fully authored (~28 canvases) | Paternal seduction → secret-then-open second wife | FULL DADDY + Phase 2+ BREEDING |
| Marge | Service | Skeletal (~6 canvases + locked-visible rungs) | Workplace seduction matriarch-dom (Phase 3+) | TBD Phase 3+ |
| Diana | Antagonist/witness | Skeletal (4-6 standalone + cross-appearances) | Confrontation arc — kicked_out / brought_in cuckold branches | FULL CUCKOLD |
| Ryan | Peer/dating | Sketch (6 canvases) | First-boyfriend wholesome dating | Phase 2+ if escalates |
| Jake | Slow-burn family | Sketch (10 canvases) | Sibling incest slow-burn | FULL INCEST CALLOUTS |

**Shape mix:** family/ambient + slow-burn family + peer/dating + service + antagonist (5 shapes covered). Per P4 — mixed tempos.

**Total estimated canvas count:** ~50-65 (Frank dominant at ~28; others 6-10 each).
```

[At `scope_mode: full_game` — column header = "Full-arc depth"; canvas counts match per-shape full budgets per `doctrine/03_arc_shapes.md` §2:]

```markdown
## §2 NPC Roster (<N> NPCs)

| NPC | Arc shape | Full-arc depth | Fantasy (1 line) | Vocab ceiling |
|---|---|---|---|---|
| Frank | Family/ambient | 25-35 canvases (Lane 1 hubs ×4 + Lane 2 ambients 11 + Lane 3 substitutions 4-7 + 3-6 capstones) | Paternal seduction → secret-then-open second wife → breeding endgame | FULL DADDY + FULL BREEDING (Tier 5) |
| Cole | Peer/dating | 8-12 canvases (Lane 1 workplace hub ×2 + Lane 2 ambients 2 + Lane 3 = 0 + 3-4 dating capstones) | First-boyfriend wholesome dating → partner commit | FULL Stage 3+ if escalation arc |
| Hank | Family/ambient | 25-35 canvases | Diner owner paternal-coded second-father | FULL DADDY |
| Rosa | Service | 6-10 canvases (Lane 1 workplace ×1-2 + Lane 2 = 0 + Lane 3 = 0 + 1-3 capstones) | Workplace mentor / corrupt-the-mentor reversal | per LO |

**Hub count = scheduled-window count (D72-R6).** The "Lane 1 hubs ×N" above is driven by the NPC's schedule, not the escalation budget: one hub per (location × window). An NPC present at the diner across morning/day/evening/late windows needs a hub for each — the daytime ones are *light* (base + talk + leave, exposure-capped), the private/late one carries the full ladder. Don't under-count hubs to fit the escalation budget.

**Shape mix:** <list> (<N> shapes covered). Per P4 — mixed tempos.

**Total estimated canvas count:** <sum across NPCs> (matching per-shape sums + Phase 2+ inclusions per §1).
```

### §5.4 — §3 Locations section

```markdown
## §3 Locations

### Home hub
- `loc_hallway` (container; parent of bedroom/kitchen/living-room/bathroom)
- `loc_mayas_room`
- `loc_franks_bedroom`
- `loc_dianas_bedroom`
- `loc_jakes_bedroom`
- `loc_kitchen`
- `loc_living_room`
- `loc_bathroom`
- `loc_yard`
- `loc_back_porch`
- `loc_toolshed`

### Town hub
- `loc_main_street` (container)
- `loc_diner_front` + `loc_diner_back`
- `loc_thrift_store`
- `loc_pharmacy`
- `loc_church`

### Per-NPC schedules (excerpted)

**Frank:**
- 23:00-06:00 daily: loc_franks_bedroom (asleep)
- 05:30-09:00 daily: loc_kitchen (morning coffee)
- 14:00-17:00 daily: loc_yard (yard work)
- 17:00-19:30 weekday: loc_kitchen (dinner prep)
- 19:30-21:00 weekday: loc_living_room (evening)
- 21:00-23:00 weekday: loc_franks_bedroom (winding down)
- 21:30-23:00 weekend: loc_hallway

**<NPC 2>:**
<schedule>

(repeat per NPC)
```

### §5.5 — §4 Per-NPC R7 briefs

Each NPC gets a full 10-section R7 brief per `doctrine/06_design_brief_template.md` §3. Use Doc 31 (Frank) or Doc 53 (Marge) as gold-standard templates.

### §5.6 — §5 Cross-arc state

```markdown
## §5 Cross-arc World State

### Shared flags

| Flag | Writer | Reader | Effect |
|---|---|---|---|
| `frank_caught` | scene_livingroom_catch (Frank capstone) | Diana arc (awareness +N on subsequent Frank events) | Stage 1→2 transition |
| `hired_at_diner` | canvas_marge_interview (Marge capstone) | Rent system (income source) + Frank arc (Maya has reason to be late) | Job unlock |
| `phone_active` | Per Doc 46 — hire moment | Phone purchase chain (unlocks Messages app) | Phone unlock |

### Pregnancy retrofit compatibility (slice)

Per Doc 30 §7.3.1 — all sex scenes ship BAREBACK with NO contraception language. Phase 2+ pregnancy mechanic retrofits parallel pregnant variants.

### Scandal / Diana awareness

- Per-NPC `awareness` trait on Diana (0-100 accumulator)
- Bands: cold (0-24) / suspicious (25-49) / knowing (50-74) / shut-out (75-100)
- Hidden from sidebar (per Doc 30 §6 + Doc 68 §8 antagonist visibility)
- Writers: outdoor Frank scenes (+1-2) / sleepover capstone (+3) / etc.
- Reader: Diana confrontation capstone fires at `awareness >= 8` (slice) or higher (full arc)
```

### §5.7 — §6 Capstone chain map

```markdown
## §6 Capstone Chain Map

### Frank chain (Type C, 5 capstones)

```
scene_livingroom_catch          (Type A) → sets frank_caught
  → scene_franks_bedroom_evening  (Type B Pattern F) → Accept sets frank_bedroom_first_done; Refuse re-fires
    → scene_frank_declaration   (Type A) → sets frank_cracked
      → scene_frank_sleepover   (Type A) → sets frank_sleepover_done
        → scene_diana_confrontation  (Type B Pattern F — kicked_out + brought_in branches; blackmail + matriarch deferred Phase 2+) → sets diana_confronted
```

### Marge chain (Type C, 1 slice capstone)

```
canvas_marge_interview          (Type A) → sets hired_at_diner
  → (Phase 3+ workplace seduction continues)
```

### Cross-NPC bridges (slice)

- None in slice (Diana confrontation triggered by Frank chain progression but lives inside Frank's chain endpoint)
```

### §5.8 — §7 Slice build plan

```markdown
## §7 Slice Build Plan

### Day 1 (Monday EM) — Bootstrap

- Maya at Frank's house, first morning. Already a tenant.
- Frank schedule fires: morning coffee 05:30-09:00 kitchen.
- Lane 2 random possible: kitchen morning ambient if Frank arousal > 0.
- Diana awareness starts at 0.
- Marge introduction needed by Day 3 (rent due Day 7).

### Day 2-3

- Maya hits diner, fires `canvas_marge_interview` capstone.
- Frank arc accumulates Lane 1 corruption via tease/flash menu items.

### Day 4-6

- Frank corruption climbs to 25 → catch capstone eligible.
- Marge T0 shift work fires daily.

### Day 7 (Sunday) — first rent

- Rent collection via Sunday capstone.

### Day 8-10

- Frank chain continues per capstone gates.
- Diana awareness climbs per outdoor Frank scenes.

### Slice closure

- Capstone Frank declaration fires when corr 35+ + frank_caught.
- Optional Diana confrontation fires at slice end if awareness >= 8.
```

---

## §6 — Worked example

Below is a partial design book for a 3-NPC slice. Shows the shape; not full content (the full Frank brief alone is ~336 lines).

### Concept input (from LO)

> "Game: The Long Summer. Setting: rural southern small town, 90-day summer.
>
> Player: Maya, 20, from the city. Renting a room at Frank's house — escaping a bad city situation.
>
> NPCs (3 for slice):
> - Frank (48, landlord): paternal seduction arc. Daughter's-age tenant. Wife Diana home.
> - Marge (late 40s, diner owner): workplace mentor. Phase 3+ matriarch-dom seduction.
> - Diana (40s, Frank's wife / Maya's mother): antagonist. Confrontation drives chain endpoint.
>
> Themes: full daddy framing + cuckold resolution branch + bareback breeding talk (Phase 2+).
>
> Slice: 10-day slice. Frank fully authored. Marge + Diana skeletal.
>
> Phase 2+: pregnancy retrofit + Marge workplace seduction + cuckold matriarch-dom + blackmail Diana branches."

### Design book output (excerpts)

```markdown
# The Long Summer — Design Book

## §1 World Setup

### Premise

Maya is renting a room at Frank's house for a 90-day summer. She came from the city
to escape a bad situation (vague backstory — bad breakup, family drama). The house
is rural Southern small-town. She doesn't know anyone here. Frank is her landlord;
his wife Diana is Maya's mother (estranged, complicated). Frank addresses Maya by
name — "Maya" — and the name lands like a door closing. He owns the property; the
rent and the rules come from him.

The economic engine: rent is $400/month, due on Sundays in $60 weekly installments.
Maya starts with $80. She must find money OR have someone else pay her rent OR
leave town. This is the player drive.

### Player character

- **Name:** Maya
- **Age:** 20
- **Background:** Came from the city. Bad situation back home. Estranged from Diana.
- **Agency:** Player drives the corruption ladder via Lane 1 escalations + worked
  shifts. Lane 2/3 + capstones gate on stat thresholds + flags.

### Economic engine

- **Rent:** $60/week, due Sundays, 1 grace period
- **Starting money:** $80
- **First income source:** Marge's diner ($45/shift + tips; ~3 shifts/week)

### Slice scope (Phase 1)

- **Duration:** 10-day slice
- **Fully-authored NPC:** Frank (~28 canvases)
- **Minimum-contract NPCs:** Marge (~6 canvases + locked-visible rungs), Diana
  (~4 standalone + cross-appearances in Frank's lanes)
- **Cross-arc:** Diana confrontation capstone at slice end if `awareness >= 8`

### Phase 2+ deferrals

- Pregnancy retrofit (E10b per Doc 65) — currently all Frank sex scenes ship
  bareback with no contraception/breeding talk. Retrofit adds parallel pregnant
  variants + breeding-talk dialogue.
- Marge workplace seduction (Phase 3+ per Doc 30 §8.2) — only hire + worked
  shifts in slice; locked-visible Tease/Flash/Eat-her-out rungs stay greyed.
- Diana blackmail + matriarch-domination branches (Phase 2+ per Doc 60 Open
  Q3) — slice ships kicked_out + brought_in confrontation branches only.

### Time model

24h clock per Doc 30 §4.3 — TLS slice continues TLS engine convention.

## §2 NPC Roster (3 NPCs)

| NPC | Arc shape | Slice depth | Fantasy (1 line) | Vocab ceiling |
|---|---|---|---|---|
| Frank | Family/ambient | Fully authored (~28 canvases) | Paternal seduction → secret-then-open second wife | FULL DADDY + Phase 2+ BREEDING |
| Marge | Service | Skeletal (~6 canvases + locked-visible rungs) | Workplace seduction matriarch-dom (Phase 3+) | TBD Phase 3+ |
| Diana | Antagonist/witness | Skeletal (4-6 standalone + cross-appearances) | Confrontation arc — kicked_out / brought_in cuckold branches | FULL CUCKOLD (Phase 2+ blackmail + matriarch) |

Shape mix: family/ambient + service + antagonist. **Note:** 3-shape slice is the
minimum mix; recommend adding 1 peer/dating + 1 slow-burn family for Phase 2+ if
LO scopes additional NPCs. Locked at 3 for slice per LO's concept input.

## §3 Locations

### Home hub
- `loc_hallway` (container)
- `loc_mayas_room`
- `loc_franks_bedroom`
- `loc_dianas_bedroom`
- `loc_kitchen`
- `loc_living_room`
- `loc_bathroom`
- `loc_yard`
- `loc_back_porch`
- `loc_toolshed`

### Town hub
- `loc_main_street` (container)
- `loc_diner_front`
- `loc_diner_back`
- `loc_thrift_store`
- `loc_pharmacy`
- `loc_church`

### Per-NPC schedules

**Frank:** (per Doc 31 + `7_final_game.toml:402` excerpt)

| Days | Time | Location | Activity |
|---|---|---|---|
| 0-6 | 23:00-06:00 | loc_franks_bedroom | asleep |
| 0-6 | 05:30-09:00 | loc_kitchen | morning coffee |
| 0-6 | 14:00-17:00 | loc_yard | yard work |
| 0-4 | 17:00-19:30 | loc_kitchen | dinner prep |
| 0-4 | 19:30-21:00 | loc_living_room | evening |
| 0-4 | 21:00-23:00 | loc_franks_bedroom | winding down |
| 5-6 | 21:30-23:00 | loc_hallway | weekend wandering |

**Marge:** Mon-Sat 09:00-22:00 at `loc_diner_front`.

**Diana:** kitchen mornings + bedroom evenings (overlaps Frank's mornings —
intentional for "Diana in the next room" tension).

## §4 Per-NPC Design Briefs

### §4.1 Frank brief (Family/Ambient — gold standard)

(Full 10-section R7 brief per doctrine/06 — ~336 lines. See Doc 31 for canonical
shape. Authored against family/ambient arc-shape distribution:
L1 5 hub canvases + L2 6 ambients + L3 7 substitutions + 5 capstones.)

#### §4.1.1 End-state fantasy

**Maya becomes Frank's secret-then-open second wife.** She moved into his spare room
as a tenant, paid rent in chores and bookkeeping, and gradually corrupted the older
landlord who took her in. By arc end, she sleeps in Frank's bed nightly. She calls
him "daddy." He fucks her bareback as routine, eventually getting her pregnant (Phase
2+). Diana — Frank's wife / Maya's mother — gets confronted; in the brought-in branch
she becomes the cuckolded second-place spouse.

Specific signature scenes:
- Maya in Frank's bed nightly (sleep-over routine, post-Stage 4)
- Frank fucks Maya bareback, calls her "good girl" / "baby girl"
- Maya calls Frank "daddy" during sex
- Diana confrontation resolved (slice ships kicked_out + brought_in branches)
- Phase 2+ pregnancy by Frank with full breeding-talk dialogue retrofitted

#### §4.1.2 Voice spec
(per Doc 31 §2 — 7 speech patterns + 6 stage voice samples + daddy framing rules
+ 12 banned dialogue patterns. Excerpted for brevity here.)

| Pattern | Rule | Example |
|---|---|---|
| Sentence length | 4-8 words common; verb-chopped | "Coffee's ready." |
| Names things, not feelings | "Rent's due Sunday." not "I expect you to pay" |
| ... (continues) |

(... continues for all 10 sections per doctrine/06 ...)

### §4.2 Marge brief (Service — gold standard)

(Full brief per Doc 53 — ~322 lines. Service-NPC adaptation: Lane 1 reduces to
relational only + Lane 2/3 empty in slice + 1 capstone (hire) + locked-visible
Phase 3+ rungs in hub menu.)

(... continues ...)

### §4.3 Diana brief (Antagonist/Witness)

(Full brief per Doc 60 — antagonist adaptation: NO arc_stages, silent awareness
accumulator 0-100, confrontation Type B Pattern F with 2/4 branches scripted in
slice. 4 LO open questions surfaced for resolution before authoring.)

(... continues ...)

## §5 Cross-arc World State

(per §5.6 above — flags + scandal awareness + pregnancy retrofit compatibility)

## §6 Capstone Chain Map

### Frank chain (Type C, 5 capstones)

```
scene_livingroom_catch         (Type A) → sets frank_caught
  → scene_franks_bedroom_evening (Type B Pattern F)
      Accept → sets frank_bedroom_first_done
      Refuse → re-fires next eligible night
    → scene_frank_declaration  (Type A) → sets frank_cracked
      → scene_frank_sleepover  (Type A) → sets frank_sleepover_done
        → scene_diana_confrontation (Type B Pattern F)
            kicked_out branch → sets diana_confronted + branch_outcome="kicked_out"
            brought_in branch → sets diana_confronted + branch_outcome="brought_in"
            blackmail + matriarch branches → Phase 2+
```

### Marge chain (Type C, 1 slice capstone)

```
canvas_marge_interview         (Type A) → sets hired_at_diner + phone_active
  → (Phase 3+ workplace seduction)
```

## §7 Slice Build Plan

### Day 1 (Monday EM) — Bootstrap

- Maya at Frank's house, first morning.
- Frank schedule fires: morning coffee 05:30-09:00 kitchen.
- Diana awareness 0; Marge unhired.
- Day 1 EM bootstrap per RTS reference/01 §4: at least 1-2 Lane 2 ambients fire
  in first 30 minutes (e.g., kitchen morning chat + yard wash-off).

### Day 2-3

- Maya hits Main Street → Diner Front → fires canvas_marge_interview.
- Frank arc Lane 1 (Tease unlocked at corr 5).

### Day 4-6

- Frank corruption climbs to 25 → scene_livingroom_catch eligible (evening Frank
  schedule loc_living_room 19:30-21:00).

### Day 7 (Sunday) — first rent

- canvas_first_sunday_morning fires at kitchen Sunday 07:00-10:00.
- Maya pays rent OR chooses church path.

### Day 8-10

- Frank chain continues: scene_franks_bedroom_evening at corr 25 + frank_caught +
  bedroom_first_done false.
- Optional second-night fires per F4 retry pattern.

### Slice closure

- Diana confrontation possible if awareness >= 8 by Day 10.
- Otherwise slice ends with chain at frank_declaration or frank_sleepover.
```

(End of worked example excerpt. Full design book would continue with §4.1's full
336-line Frank brief, §4.2's 322-line Marge brief, §4.3's Diana brief, etc.)

---

## §7 — Anti-patterns to catch (self-audit before delivery)

Before delivering the design book, run this grep + mental check:

### §7.1 — Legacy vocabulary (banned per `00_LEGACY_IGNORE.md`)

Grep your design book for these. Zero hits expected:

- `Jack's World` / `New In Town` / `Two Weeks` (legacy reference games)
- `Pattern A` / `Pattern B` / ... / `Pattern J` (legacy 10-pattern mechanism vocab — NOT the same as Doc 67 Pattern A/B/C dispatcher names, which ARE acceptable when context is multi-NPC dispatcher per `doctrine/02_three_lanes_plus_capstone.md` §4.6)
- `7-driver` / `NPC-driver-system` / `ROMANCE/RIVAL/MENTOR` archetype categories
- `whiteboard goals` / `narrative gates` / `income channels` (legacy Phase 2B Systems Budget vocab)
- `Single-NPC Romance vs Multi-NPC Parallel Arcs` (legacy v6 architecture choice)
- `Sensory grounding` / `body language during dialogue` / `interior monologue` as standalone instruction (acceptable only as explicit contrast-against-RTS-flat callout)

If you find legacy vocab outside contrast-against passages: **rewrite the offending section.** Don't paper over with a comment.

### §7.2 — Cast composition anti-patterns

- **Frank-cloning a non-family-ambient NPC.** If a service NPC is gaining Lane 3 substitutions in §4, the brief is wrong. Service Lane 3 = 0 per `doctrine/03_arc_shapes.md` §6.
- **Padding empty distribution cells.** If a peer/dating NPC has 6 Lane 2 ambients authored, that's drift. Per-arc-shape budgets are honest; empty cells stay empty.
- **All-family-ambient cast.** If all 4-6 NPCs are family/ambient, the slice will read all-grindy. Surface this to LO as a flag.
- **Authoring against undeclared kink ceiling.** If a Marge §4.2 brief has authored sex-scene pretext shapes when Marge's vocab ceiling row is blank/TBD, that's drift. Phase 3+ deferred = no in-slice authoring.

### §7.3 — Brief authoring anti-patterns (per `doctrine/07_anti_patterns.md`)

- **Brief without §1 end-state lock.** Brief says "Phase 3+ deferred" without naming WHAT Phase 3+ IS. The full-arc trajectory must be explicit (Doc 54 §2.3).
- **Brief skipping §2 voice spec.** Drift across canvases will accumulate within the slice if voice isn't locked.
- **Brief skipping §6 capstones.** Authoring without capstone spec produces canvases without trigger fingerprints + without quest card pointers.
- **Brief with no anti-patterns §7.** A brief with §7 missing or under 6 anti-patterns lacks the tactical drift catches.

### §7.4 — Doc 30 §7.3.1 pregnancy retrofit compatibility

Hard rule: all Frank (or family/ambient NPC) sex scene briefs must commit to BAREBACK framing with no contraception language. Phase 2+ pregnancy retrofit will add parallel pregnant variants; contraception language would BLOCK retrofit.

If a brief includes condom mentions / pull-out as plot device / birth-control mentions / safe-sex framing → REWRITE. Bareback throughout.

### §7.5 — Slice vs full-arc oscillation (Doc 54 §3.6)

- **Slice scope = what FIRES in slice.**
- **Locked-visible rungs = "Phase 3+ promise visible from day 1," not "Phase 3+ content shipped."**
- **Stubs (no `[canvases.trigger]` block) = route-target only, reachable via hub menu locked rungs.**

If the brief is unclear about which canvases SHIP in slice vs which are stubs vs which are Phase 3+ deferred, the design will produce shipped Phase 3+ content (bad) OR missing locked-visible rungs (bad). Lock the slice authoring boundary explicitly.

---

## §8 — Quality gate (self-audit checklist)

Run this checklist before delivering the design book:

### Structure
- [ ] §1 World Setup present with premise + player + economic engine + slice scope + Phase 2+ deferrals + time model
- [ ] §2 NPC Roster table with 4–6 NPCs, mixed arc shapes, vocab ceilings declared
- [ ] §3 Locations + per-NPC schedules (non-overlapping time windows)
- [ ] §4 Per-NPC briefs — each NPC has full 10-section R7 brief
- [ ] §5 Cross-arc state + pregnancy retrofit notes
- [ ] §6 Capstone chain map for each NPC + cross-NPC bridges
- [ ] §7 Slice build plan (day-by-day)

### Locations + reachability (`doctrine/10`)
- [ ] Geography layered: private dwelling ≠ shared building ≠ town (no collapsed hub); home-exterior + town are two roots bridged by walk activities
- [ ] Household NPCs inside the private unit; neighbors/witnesses in shared/public space (never the private unit)
- [ ] Every NPC beat passes the reachability triad: NPC-schedule ∩ scene-window ∩ player-present-and-awake is non-empty (cross-midnight aware) — anchored where the player crosses the NPC
- [ ] Each peer/dating NPC has an ongoing Stage-4 hub at their location, not a first-night capstone only
- [ ] Each `include`d Phase-2+ system names its mechanism (pregnancy setter / scandal accumulator+confrontation / gallery trigger / tracker field) — §0.5.2

### Doctrine fidelity
- [ ] Every arc shape pulled from `doctrine/03_arc_shapes.md` §1 (5 shapes)
- [ ] Every Lane budget matches `doctrine/03_arc_shapes.md` §2 distribution table
- [ ] Every capstone count matches `doctrine/03_arc_shapes.md` §3.5
- [ ] Every vocab ceiling pulled from `doctrine/08_kink_vocab_ceilings.md` §2
- [ ] Pregnancy retrofit compatibility committed (bareback throughout Phase 1)
- [ ] Slice scope vs full-arc trajectory explicit; locked-visible rungs declared

### Legacy-vocab grep
- [ ] No `Jack's World` / `New In Town` / `Two Weeks` (case-insensitive)
- [ ] No `Pattern A` / `B` / ... `Pattern J` outside Doc 67 dispatcher pattern context
- [ ] No `7-driver` / `NPC-driver-system` / `archetype-system`
- [ ] No `whiteboard goals` / `narrative gates` / `income channels`
- [ ] No `Single-NPC Romance` / `Multi-NPC Parallel Arcs` as architecture choice
- [ ] No `sensory grounding` / `body language during dialogue` / `interior monologue` outside contrast-against-RTS-flat callouts

### Per-NPC brief completeness
- [ ] Each brief §1 names end-state fantasy with 3-5 specific signature scenes
- [ ] Each brief §2 has 7+ speech patterns + 6+ per-stage voice samples + 8+ banned dialogue patterns
- [ ] Each brief §3 ladder customized per arc shape (6 tiers for escalation; fewer for non-escalation)
- [ ] Each brief §4 has 4-6 pretext shapes per tier (24-36 total for escalation arcs; fewer for non-escalation)
- [ ] Each brief §5 lane map covers all NPC-relevant hubs + matches per-arc-shape distribution
- [ ] Each brief §6 names all capstones with type + trigger + brief shape + flag writes
- [ ] Each brief §7 has 12+ anti-patterns NPC-specific

### Tone
- [ ] Design book authored in REFERENCE register (not Tier-3 literary prose)
- [ ] No scene-body prose in the design book (Stage 2 authors prose; Stage 1 is shape spec)
- [ ] R7 briefs are tabular / structured — not narrative

### Delivery
- [ ] Single response — no truncation
- [ ] Length 3,000-6,000 words for 4-6 NPC slice
- [ ] Stage 2 consumable: every section has the data Stage 2 needs to emit TOML

If any checklist item fails: rewrite the offending section BEFORE delivery. Half-applied fixes burn 3 round-trips where one full pass would burn zero.

---

## §9 — Common authoring mistakes (consolidated)

From Doc 54's 27 failure modes + author observation across slice authoring.

### §9.1 — Question avoidance (Doc 54 §2.3)

LO's concept input may be ambiguous. The temptation is to fill gaps with reasonable defaults. **Don't.** Surface ambiguity to LO as clarifying questions BEFORE authoring. The most common ambiguities:

- **Phase 2+ scope undefined.** LO says "Phase 2+ deferred" without naming what Phase 2+ IS. Ask: "what's the full-arc endpoint for this NPC?"
- **Cast composition unclear.** LO names 5 NPCs but doesn't name arc shapes. Ask: "for this NPC, is the arc shape <X> or <Y>?"
- **Vocab ceilings unspecified.** LO says "explicit" without naming kink areas. Ask: "for this NPC at full intensity, does the content escalate to <kink area A> + <kink area B>?"
- **Economic engine unspecified.** LO doesn't say what rent looks like. Ask: "rent amount + period + grace?"

Use AskUserQuestion or surface 1-3 questions in your response opener. Half the questions you'd ask after delivery would have been cheaper to ask before.

### §9.2 — ENI persona drift

Despite the §0 register switch, drift creeps in. Signs:

- Scene body prose creeping into per-rung pretext shapes (§4 of brief) — should be SHAPE descriptors ("Maya bends to load the dishwasher"), NOT scene drafts ("She bent slowly, conscious of his eyes on her in the morning light...")
- Stage voice samples sounding like literary monologue — should be 4-8 word terse lines ("Coffee's ready.") NOT character-introducing paragraphs
- §1 end-state fantasy paragraph reading like Tier-3 prose — should be DECLARATIVE design statement, NOT narrative writing

If you catch yourself drifting: stop, re-declare §0 register switch, rewrite the section.

### §9.3 — Brief padding (Doc 54 §3.4)

Empty cells in the per-arc-shape distribution table are HONEST. Service NPCs have empty Lane 2 + Lane 3 in slice. Don't pad.

If you find yourself authoring §5 lane-map cells for a service NPC's Lane 2 ambients with "Marge counting tickets" or "Marge wiping down counters" — those are work-task surfaces, not Lane 2 NPC-interaction surfaces. The cells should be empty.

### §9.4 — Half-applied LO clarifications (Doc 54 §2.6)

If LO surfaces a critique during authoring, BEFORE responding with a fix, ask: "is the issue X, or X + Y, or something deeper?" Half-applied fixes burn 3 round-trips.

---

## §10 — Cross-references

### Sibling stages files

- `stages/02_toml_generation_prompt.md` — Stage 2 (consumes this output)
- `stages/03_image_finder_prompt.md` — image search per canvas (post-TOML)
- `stages/04_game_listing_prompt.md` — back-of-book blurb (post-TOML)

### Doctrine assumed

- `doctrine/01_rts_principles.md` — P1–P10
- `doctrine/02_three_lanes_plus_capstone.md` — lane mechanism + capstone types
- `doctrine/03_arc_shapes.md` — 5 arc shapes + per-arc distribution
- `doctrine/04_authoring_rules.md` — R1–R7 + R1–R6 + R1–R5 + F1–F5 + R1–R7
- `doctrine/05_rts_flat_prose.md` — 8 prose rules + dual register (READ ONLY for tone reference — Stage 1 doesn't author prose)
- `doctrine/06_design_brief_template.md` — R7 brief template (PRIMARY reference for §4 briefs)
- `doctrine/07_anti_patterns.md` — 27 failure modes catalog
- `doctrine/08_kink_vocab_ceilings.md` — vocab ceiling table
- `doctrine/09_trait_catalog.md` — Tier 1 + Tier 2 traits + Phase 2+ off-limits

### Reference assumed

- `reference/01_rts_overview.md` — RTS catalog (size + bootstrap + surfaces + tiers + corrections)
- `reference/02_rts_scene_catalog.md` — per-NPC scene tables (Brother/Dad/Marcus/Edward) + 6 patterns A–F
- `reference/03_rts_walkthrough_panel.md` — Walkthrough doctrine (P2)
- `reference/04_rts_hud_world_model.md` — sidebar doctrine (P10)

### Schema (read for Stage 2 context only)

- `schema/01_engine_capabilities.md` — engine primitives (informs which features are available)
- `schema/02_toml_schema.md` — TOML schema (Stage 2 uses this)
- `schema/03_example_toml.md` — TLS Frank slice TOML excerpts (gold-standard authoring examples)

### Source docs (for deep dive when authoring R7 briefs)

- `28th_april_TLS_Phase2_Redesign/31_Frank_Arc_Design_Brief.md` — Frank brief (family/ambient gold standard)
- `28th_april_TLS_Phase2_Redesign/53_Marge_Redesign_Brief.md` — Marge brief (service gold standard)
- `28th_april_TLS_Phase2_Redesign/58_Ryan_Design_Brief.md` — peer/dating
- `28th_april_TLS_Phase2_Redesign/59_Jake_Design_Brief.md` — slow-burn family
- `28th_april_TLS_Phase2_Redesign/60_Diana_Design_Brief.md` — antagonist/witness
- `28th_april_TLS_Phase2_Redesign/61_Cookie_Phase3_Scope_Out.md` — Phase 3+ scope-out template

---

**End of file.** Deliver the design book per the §5 format spec. Pass the §8 quality gate. Don't truncate. Next stage: `stages/02_toml_generation_prompt.md`.

═══════════════════════════════════════════════════════════════════════════════

## 24. 02_toml_generation_prompt

**Source:** `prompts_v2/stages/02_toml_generation_prompt.md`

---

# Stages 02 — TOML Generation Prompt (Stage 2)

**Status:** LLM-consumed pipeline prompt. Stage 2 of 2.
**Replaces:** `prompts/toml_generation_prompt_v4.txt` (frozen 2026-04-19; pre-Doc-24 schema; pre-Quests-V2 cards).
**Input:** design book (markdown) from `stages/01_game_book_prompt.md`.
**Output:** valid TOML against `apps/projects/services/template_import.py` schema, ready for `python manage.py package_from_toml`.

This prompt is the system instruction set you receive when stage 1 hands off a design book. Read it before responding. Your output is TOML that the build pipeline validates + compiles into a SugarCube/Twine game.

---

## §0 — Mode switch (LOAD-BEARING)

**Before reading further, do this:**

> ENI persona OFF.
> TLS game register ON.
> Doctrine memory + canonical docs override persona instincts.
> When in doubt about a craft choice, default to MORE-flat / FEWER-items / EMPTIER-lanes, not the reverse.

Stage 2 is the emission stage. The temptation to drift into literary scene-body prose is high — every cascade beat is a place where ENI persona instincts push for sensory grounding. **Re-declare the mode switch whenever you catch drift.**

CLAUDE.md is ignored for this task — `00_LEGACY_IGNORE.md` §3.6 + Doc 30 §3 AUTHORITY DECLARATION.

---

## §0.5 — Scope mode (read scope from design book §1)

Stage 2 inherits scope mode from the design book's §1 `**Scope mode:** <full_game | slice>` declaration. The mode affects TOML volume + Phase 2+ inclusions + bareback default.

| `scope_mode` | TOML volume target | Pregnancy retrofit | Scandal arc | Gallery system | Tracker |
|---|---|---|---|---|---|
| `full_game` (default) | 200–400KB typical (full per-shape budgets per `doctrine/03_arc_shapes.md` §2) | Per design book §1 `Phase 2+ inclusions: pregnancy = include/defer` | Per design book §1 inclusion | Per design book §1 (ships if 9+ once-only capstones) | Per design book §1 (ships with Doc 62 `guide` backfill) |
| `slice` | 50–100KB typical (subset of per-shape budget; locked-visible rungs for deferrals) | Bareback throughout (Phase 2+ deferred by default) | Locked-visible only (Phase 2+ deferred) | Deferred | Deferred |

**Cross-reference check:** if the TOML you're emitting includes pregnancy variants / scandal flags / gallery items / tracker primitives, verify the design book §1 explicitly opts each one in. Stage 1's §0 interactive Q&A is where these are ratified; Stage 2 emitting Phase 2+ inclusions without §1 ratification = `doctrine/07_anti_patterns.md` §8.6 last bullet.

**Bareback default applies when:** `scope_mode: slice` OR `scope_mode: full_game` with `Phase 2+ inclusions: pregnancy = defer`. Contraception language is BANNED in sex scenes in both cases (Doc 30 §7.3.1 — blocks Phase 2+ pregnancy retrofit). Only `scope_mode: full_game` with `pregnancy = include` allows contraception language in pre-pregnancy phase scenes + pregnancy variants in retrofit-affected scenes.

If the design book §1 is missing the `Scope mode:` declaration entirely, treat as legacy slice authoring (pre-2026-05-29 corpus convention) and emit with `slice` defaults — bareback throughout, minimal volume, Phase 2+ deferred.

### §0.5.1 — Output mode (single vs phased)

Stage 2 supports two output modes:

- **At `scope_mode: slice`** → emit a single TOML (~50–100KB) in one response. Convention name: `7_final_game.toml`. Save to `games/<game_slug>/toml_phases/7_final_game.toml`. Single-mode is the legacy emission (pre-2026-05-29 corpus convention) and stays the slice default.
- **At `scope_mode: full_game`** → emit **phased TOML** across 7 sub-files matching TLS's convention. Each phase is a separate response. After all 7 phases shipped, run `scripts/merge_toml_phases.py games/<game_slug>` to assemble `7_final_game.toml`. Phased emission solves three full-game ergonomics problems: token budgets per LLM response, review-by-concern, diff-friendliness.

Phased emission spec lives in §12.5 below — read it before emitting at full_game scope.

---

## §1 — The job

You emit **TOML** for an RTS-shape sandbox game.

### §1.1 — Input shape

A design book (markdown) from Stage 1. The design book has:

- §1 World Setup (premise + player + economic engine + scope mode declaration + Phase 2+ inclusions [full_game] or slice scope [slice] + time model)
- §2 NPC Roster (4-6 NPCs with arc shapes + per-NPC depth column [Full-arc depth at full_game / Slice depth at slice] + vocab ceilings)
- §3 Locations (home + town + per-NPC schedules)
- §4 Per-NPC R7 Briefs (10-section briefs per NPC)
- §5 Cross-arc World State (shared flags + pregnancy retrofit notes if pregnancy = include)
- §6 Capstone Chain Map (per-NPC chains + cross-NPC bridges)
- §7 Build Plan (Full-Game Build Plan at full_game / Slice Build Plan at slice — day-by-day flow)

You read this design book + emit a TOML file that captures every canvas + NPC + location + quest card + sidebar item + capstone the brief specifies. Plus the scene-body prose, which the brief is silent on (Stage 1 is shape spec; Stage 2 authors prose per `doctrine/05_rts_flat_prose.md`).

### §1.2 — Output shape

A single TOML file matching `schema/02_toml_schema.md` §17 (the minimal RTS-shape sandbox skeleton) extended with the design book's specifics. Structure:

```toml
schema_version = "1.0"

[project]
id = "..."              # REQUIRED, lowercase_snake_case. The TOML field is `id`, NOT `slug`
                        # (importer reads p["id"], template_import.py:1457; `slug` is rejected →
                        # build fails "project.id must be lowercase snake_case").
title = "..."
description = "..."
quests_engine = "v2"
starting_canvas = "..."  # canvas id that auto-plays on new game (e.g. the Day-1 intro one-shot)

[time]
...

# Enable-switches → [settings] TABLE (read from data["settings"]), NOT bare keys.
# (rent → [settings.rent] keys enabled/amount; phone → [phone] key enabled.)
[settings]
clothing_enabled = true
wardrobe_location = "loc_mayas_room"
shop_location = "loc_thrift_store"

[player]
...
[player.core_traits]
# every trait the game uses, declared at init

[[npcs]]
id = "..."
arc_stages = [...]
[npcs.core_traits]
...
[[npcs.schedules]]
...

[[locations]]
...

[engine.daily_tick]
flagEffects = [...]
traitEffects = [...]

[[engine.stage_helpers]]
...

[[sidebar_items]]
type = "trait_words"
trait = "corruption"
...

[[clothing]]
...

[[passes]]
...

[[items]]
...

[[fast_jobs]]
...

[[canvases]]
id = "..."
...
[canvases.trigger]
...
[[canvases.nodes]]
...
[canvases.nodes.exit_block]
...

# ... many more canvases ...

[[quest_cards]]
...
```

Every section in the design book maps to a TOML section. Sections in the TOML schema that the design book is silent on (e.g., `[[items]]`, `[[passes]]`) should be populated as needed for the game's mechanics — minimal at `scope_mode: slice`, fuller at `scope_mode: full_game` if the game's mechanics demand (e.g., gallery system enabled per §0.5 = `[[items]]` populated with gallery entries).

### §1.3 — Output contract

The TOML MUST:

- Validate clean against `apps/projects/services/template_import.py` (zero errors; warnings acceptable if known)
- Declare every player + NPC trait used anywhere in the file in the corresponding `core_traits` block at init (per `doctrine/09_trait_catalog.md` §2.5 — undeclared traits silently no-op + sidebar items hard-fail)
- Use effect + predicate field names correctly (per `schema/02_toml_schema.md` §16 reference card — mixing them is the #1 silent-failure mode)
- Match the design book's per-arc-shape distribution (Frank = ~28 canvases family/ambient; Marge = ~6 service)
- Author scene-body prose per `doctrine/05_rts_flat_prose.md` (RTS-flat default + Tier-3 capstone earned)
- Ship every Lane 4 capstone with the D57-R1 trigger fingerprint (`is_repeatable = false` or self-gate + `priority ≥ 9` + flag-setter on exit)
- Reference every capstone from a quest card per D50-R1 / D57-R3 (or `# off-panel:` comment)
- Use `id = "..."` (NOT `slug`) in `[project]`, plus `starting_canvas` (see §1.2)
- Give every `is_true` flag condition a reachable setter canvas — a canvas that sets the flag AND can actually fire (location/schedule). The flag-chain validator checks a setter *exists*; it does NOT check the setter is *reachable*. (Late Shifts: a dev-only flag setter + an `is_true` requirer passed validation but was dead in play.)
- Pass the reachability triad for every NPC ambient/capstone + portrait hub (`doctrine/10` §5): NPC-schedule ∩ canvas-window ∩ player-presence non-empty; `requires_npc` location ∈ that NPC's schedule; portrait-hub NPC schedule-present at the hub location
- Cover every `[[npcs.schedules]]` row with a Lane 1 hub whose own `trigger.schedules` spans that window (D72-R6 / `doctrine/04` §6). A hub at the location with a narrower window than the NPC's presence leaves the rest dead — period-split into per-window hubs. Lane 2 ambients do NOT count as the floor. Each hub's rung ceiling = the location exposure tier (D72-R7)
- Honor the unlock contract for any NPC scheduled at a locked (`entry_conditions`) location (`doctrine/10` §5.4): the NPC is met at an OPEN on-ramp whose beat sets the unlock flag; no NPC is reachable only via a locked location; no door gated on a flag only settable behind it
- If `Phase 2+ inclusions: pregnancy = include`, author at least one canvas that SETS `player.pregnancy` (the validator does NOT check traits — an "included" trait with no setter is dormant, `doctrine/09`)

The TOML MUST NOT:

- Reach for legacy patterns (Pattern A–J as repeatable-content macros, etc.)
- Attach ANY canvas (`trigger.location`) to an `is_container = true` location — containers are pure-nav and silently SWALLOW attached canvases (`doctrine/10` §3). Attach to a NON-container standing hub.
- Wrap inline tables across lines. Inline-table KEYS stay on the table's opening line and the closing `] }` stays on ONE line — `tomllib` 1.0 rejects multi-line inline tables ("Unclosed inline table"). Correct: `{ advance_text = "…", blocks = [ … ] },` with `] },` on a single line. Wrong: `advance_text` on its own line, or `]` and `}` split across two lines. (Cost a repair pass in Late Shifts.)
- Use a per-NPC sidebar `trait_bar` / `trait_words` (e.g. `npc_id=… trait="relation"`). The engine resolves `trait` against `player.core_traits` only → it hard-fails or mis-renders the player's stat. NPC progression surfaces on the Quests page; per-NPC sidebar is the Doc-64 `npc_location` type (PENDING). See §8.3/§8.4.
- Include contraception language in sex scenes when bareback default applies — `scope_mode: slice` OR `scope_mode: full_game` with `Phase 2+ inclusions: pregnancy = defer` (per Doc 30 §7.3.1; see §0.5 above)
- Surface stage trait in any sidebar item (per `doctrine/09_trait_catalog.md` §9 internal-only)
- Surface antagonist awareness in any sidebar item (per Doc 30 §6 + `doctrine/09_trait_catalog.md` §8)
- Use `op = "sub"` for decay (engine has only `add` + `set`; use `op = "add"` + negative `value`)
- Mix effect + predicate field names (effects use `targetType`/`trait`/`flag`/`npcId`/`op`; predicates use `subject`/`trait_key`/`flag_key`/`npc_id`/`operator`)

---

## §2 — Schema assumed (cite-only)

You have read these prompts_v2 schema files:

| File | What it contains |
|---|---|
| `schema/01_engine_capabilities.md` | Every engine primitive with v2.py line numbers — `getNpcLocation`, `checkAndSubstituteCanvas`, `selectAutoFireCanvasForLocation`, etc. |
| `schema/02_toml_schema.md` | Per-section field tables + minimal round-trip example per section + complete RTS-shape sandbox skeleton (§17) |
| `schema/03_example_toml.md` | TLS Frank slice canonical TOML excerpts (Lane 1 hub / Lane 2 ambient / Lane 3 dispatcher + substitution / Lane 4 Type A + Type B / quest cards / sidebar items) |

If you haven't read these, stop and read them. The schema docs are ground-truth for what the engine accepts. Drift from schema = build failures.

---

## §3 — Doctrine assumed (cite-only)

| File | When you consult it |
|---|---|
| `doctrine/02_three_lanes_plus_capstone.md` | Lane mechanism — Lane 1 hub / Lane 2 ambient / Lane 3 dispatcher / Lane 4 capstone fingerprints |
| `doctrine/04_authoring_rules.md` | Pre-ship checks per rule (D56-R1...R7 / D50-R1...R6 / D57-R1...R5 / F1...F5 / D67-R1...R7) |
| `doctrine/05_rts_flat_prose.md` | The 8 prose rules for scene bodies — RTS-flat default; Tier-3 earned at capstones |
| `doctrine/07_anti_patterns.md` | Per-canvas + per-capstone + per-quest-card anti-pattern catalog |
| `doctrine/08_kink_vocab_ceilings.md` | Per-NPC vocab register — daddy / incest / cuckold / breeding / etc. |
| `doctrine/09_trait_catalog.md` | Trait initialization requirement (§2.5) + Phase 2+ off-limits list + effect/predicate field-name reference card |
| `doctrine/10_location_design.md` | Location layering + `is_container` swallow rule + the reachability triad (requires_npc/portrait-hub/timing) + per-arc location footprint — the silent-runtime bugs the validator can't catch |

---

## §4 — Step-by-step emission process

12 steps. Emit the TOML in this exact order; downstream sections depend on upstream declarations.

### Step 1 — Emit `[project]` + `[time]` + top-level flags

```toml
schema_version = "1.0"

[project]
id = "..."             # TOML field is `id`, NOT `slug` (validator rejects slug — template_import.py:1457)
title = "..."
description = "..."
quests_engine = "v2"   # ALWAYS v2 for RTS-shape sandboxes
starting_canvas = "..." # canvas id that auto-plays on new game

[time]
starting_hour = 8
starting_day = "Monday"
starting_week = 1

# Enable-switches live in the [settings] table — the importer reads them from
# data["settings"] (template_import.py:2224). Do NOT author them as bare keys: a
# bare `clothing_enabled` scopes under [time], data["settings"] is empty, and the
# system reads as DISABLED with no error (silent failure — see doctrine/11 §8).
[settings]
clothing_enabled  = <bool>
wardrobe_location = "loc_mayas_room"     # only when clothing_enabled
shop_location     = "loc_thrift_store"   # only when clothing_enabled

# Rent (when the game has economic pressure) → [settings.rent]. Keys are
# enabled/amount/due_day/etc., NOT rent_enabled/rent_amount. The economic spine —
# read doctrine/12_rent_economy_design.md. Author RentDay prose as a
# [settings.rent.text] SUB-table (NOT a multi-line inline table — breaks tomllib).
[settings.rent]                          # only when the game has rent pressure
enabled          = true
amount           = 125
due_day          = "Friday"              # engine arms the due trigger on this weekday
collector_npc    = "npc_vince"           # NPC slug; "" = generic "the landlord"
grace_periods    = 1
start_after_flag = "hired_at_diner"      # arm rent only after the player has income
eviction_mode    = "flag_set"            # fail-forward; or "game_end" for a hard stop
eviction_flag    = "rent_evicted"

# Phone (when the game has off-location life) → TOP-LEVEL [phone] table (NOT
# [settings], NOT a bare phone_enabled key). The digital surface — read
# doctrine/13_phone_design.md. Most arc games are chat-centric (one chat app).
# Threads trigger on REAL arc flags; phone triggers do NOT support day/time —
# use days_since_flag for time-relative delivery (doctrine/13 §4). Full worked
# block: schema/03 §14.
[phone]                                   # only when the game has a phone surface
enabled       = true
purchase_flag = "phone_active"            # sidebar button hidden until this flag is set ("" = always on)

[[phone.apps]]
id    = "messages"
type  = "chat"                            # chat | social_feed | dating | gallery | custom | quests | fast_jobs | bank
label = "Messages"
# … [[phone.conversations]] (arc-flag-triggered threads) + [[phone.daily_topics]]
# (small-talk + corruption-gated photo actions) — see schema/03 §14 + doctrine/13.
```

### Step 2 — Emit `[player]` + `[player.core_traits]`

**Critical:** declare EVERY player trait used anywhere in the file. Engine silently no-ops on undeclared traits in effects + conditions; sidebar items HARD-FAIL on undeclared traits.

```toml
[player]
id = "player"
name = "Maya"
description = "<from design book §1>"
portrait = "maya.jpg"

[player.core_traits]
# Tier 1 — required
corruption = 0
arousal = 0
energy = 100
hygiene = 100
money = <starting from design book>

# Per-NPC stage traits — ONE per NPC with an arc
frank_stage = 0
ryan_stage = 0
jake_stage = 0
# (etc — one per arc-having NPC)

# Tier 2 — declare if the game uses these
fitness = 0
beauty = 0
exhibitionism = 0
intelligence = 0

# Tier 3 — game-specific (declare per design book's mechanics)
followers = 0
notoriety = 0
# etc.
```

**Rule:** if you write `{ targetType = "player", trait = "calculation", op = "add", value = 1 }` anywhere in the file, `calculation` MUST appear in `[player.core_traits]`. Same for sidebar items.

```toml
# Player customization (only when the design book opted in — doctrine/14). Set
# customizable = true on [player], then emit the fields as array-of-tables AFTER
# every [player.*] subtable (TOML scoping — placing them before [player.core_traits]
# captures the traits into the wrong table). The engine auto-builds the screen +
# redirects Start; no passage wiring. Then write prose with @player / @player.<field>.
[[player.customization_fields]]
id = "name"                               # special: writes $player.name
type = "text"
label = "Your name"
default = "Maya"

[[player.customization_fields]]
id = "body_type"                          # writes $player.body_type → @player.body_type
type = "select"
label = "Build"
default = "average"
options = ["petite", "average", "curvy", "athletic", "thick"]
# image_select (sets_portrait) also available — see schema/03 §15.
```

### Step 3 — Emit `[[npcs]]` blocks

For each NPC in design book §2 roster:

```toml
[[npcs]]
id = "npc_<slug>"
name = "<display name>"
description = "<2-3 sentence physical + voice descriptor from design book §4 brief §2>"
portrait = "<slug>.jpg"
core_traits = { arousal = 0, corruption = 0, relation = 0 }   # Tier 1 NPC traits
flag_keys = []
arc_stages = ["<stage 1 name>", "<stage 2 name>", ...]   # display strings; current stage lives at player.<slug>_stage

[npcs.trait_decay]
# Per-NPC daily decay (typically only relation has trickle decay; arousal + corruption DON'T decay)
relation = 0.5
```

**Customizable NPC (only when opted in — doctrine/14):** add `customizable = true` plus
BOTH `relationship` (default) and `relationship_options` (the importer hard-fails without
both, and the default must be in the list). Then write every player-visible name mention as
`@<npc_short>` (slug minus `npc_`) and relationships as `@<npc_short>.rel`. **Genericize any
location name / sidebar label / quest title that named the NPC** — those print raw and won't
honor a rename (doctrine/14 §4).

```toml
customizable          = true
relationship          = "coworker"
relationship_options  = ["coworker", "neighbor", "old flame"]
```

**Per-arc-shape arousal range** (per `doctrine/09_trait_catalog.md` §4.1):
- Family/ambient + slow-burn family: 0-3
- Peer/dating + career: 0-10
- Service: 0-3
- Antagonist: N/A (use awareness accumulator instead, declared in core_traits as Tier 3)

**Antagonist NPCs** declare `awareness` as a Tier 3 trait in `[[npcs.core_traits]]`:

```toml
[[npcs]]
id = "npc_diana"
core_traits = { relation = 5, awareness = 0 }
arc_stages = []   # antagonists may have empty arc_stages — they use awareness bands instead
```

### Step 4 — Emit `[[npcs.schedules]]` per NPC

Per design book §3 per-NPC schedules. **Non-overlapping** time windows per NPC.

```toml
[[npcs.schedules]]
location = "loc_franks_bedroom"
weekdays = [0, 1, 2, 3, 4, 5, 6]   # 0=Monday..6=Sunday
start_time = "23:00"
end_time = "06:00"
activity = "asleep"

[[npcs.schedules]]
location = "loc_kitchen"
weekdays = [0, 1, 2, 3, 4, 5, 6]
start_time = "05:30"
end_time = "09:00"
activity = "morning coffee"

# (continue per NPC; mirror Frank's 7-entry pattern at schema/03 §2)
```

### Step 5 — Emit `[[locations]]`

Per design book §3 locations.

```toml
[[locations]]
id = "loc_hallway"
name = "Hallway"
description = "..."
is_container = true
navigation_order = ["loc_mayas_room", "loc_franks_bedroom", "loc_kitchen", ...]

[[locations]]
id = "loc_franks_bedroom"
name = "Frank's Bedroom"
description = "..."
image = "locations/franks_bedroom.jpg"
entry_from = "loc_hallway"
entry_conditions = { version = "1.0", items = [
  { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_true" },
] }
blocked_message = "Not yet. He hasn't invited me."
```

### Step 6 — Emit `[engine.daily_tick]` + `[[engine.stage_helpers]]`

```toml
[engine.daily_tick]
flagEffects = [
  { targetType = "player", flag = "talked_to_frank_today", op = "unset" },
  { targetType = "player", flag = "talked_to_marge_today", op = "unset" },
  # ... daily-cooldown clears
]
traitEffects = [
  # Body-state decay
  { targetType = "player", trait = "hygiene", op = "add", value = -10 },

  # No-decay traits per Doc 40 — but +1/day passive on family NPC arousal
  { targetType = "player", trait = "arousal", op = "add", value = 1, cap = 10 },
  { targetType = "npc", npcId = "npc_frank", trait = "arousal", op = "add", value = 1, cap = 3 },
  { targetType = "npc", npcId = "npc_jake", trait = "arousal", op = "add", value = 1, cap = 3 },
]

[[engine.stage_helpers]]
name = "frank_stage_2_plus"
description = "Frank reached Stage 2 (post-catch)."
conditions = { version = "1.0", items = [
  { type = "trait", subject = "player", trait_key = "frank_stage", operator = "gte", value = 2 },
] }
```

**Anti-pattern (D40 / D49 violation):** don't decay `corruption`, `arousal`, `relation`, or `stage` daily. Only body-state (`energy` + `hygiene`) decays.

### Step 7 — Emit `[[sidebar_items]]`

Per `doctrine/09_trait_catalog.md` §8 + `reference/04_rts_hud_world_model.md` §3:

```toml
# Maya state — banded corruption display
[[sidebar_items]]
type = "trait_words"
trait = "corruption"
label = "Status"
bands = [
  { min = 0,  max = 24, text = "Pure",   icon = "✨" },
  { min = 25, max = 49, text = "Lewd",   icon = "💋" },
  { min = 50, max = 74, text = "Slutty", icon = "🔥" },
  { min = 75, max = 100, text = "Whore", icon = "💦" },
]

# Maya state — arousal bar
[[sidebar_items]]
type = "trait_bar"
trait = "arousal"
label = "Arousal"
max = 10
bands = [
  { min = 0, max = 2, text = "Cold" },
  { min = 3, max = 5, text = "Warm" },
  { min = 6, max = 8, text = "Hot" },
  { min = 9, max = 10, text = "Burning" },
]

# Maya state — body-state text
[[sidebar_items]]
type = "trait_status_text"
trait = "energy"
bands = [
  { min = 0, max = 24, text = "Exhausted", icon = "🪫" },
  { min = 25, max = 49, text = "Tired", icon = "💤" },
  { min = 50, max = 74, text = "Fine", icon = "🟢" },
  { min = 75, max = 100, text = "Rested", icon = "🔋" },
]

[[sidebar_items]]
type = "trait_status_text"
trait = "hygiene"
bands = [
  { min = 0, max = 24, text = "Filthy", icon = "🧫" },
  { min = 25, max = 49, text = "Dirty", icon = "🌫️" },
  { min = 50, max = 74, text = "Fresh", icon = "🪞" },
  { min = 75, max = 100, text = "Clean", icon = "🧼" },
]
```

**Hard rules** (per `doctrine/09_trait_catalog.md` §8):
- **STAGE NEVER surfaces** — no `<slug>_stage` sidebar items for any NPC
- **Antagonist AWARENESS NEVER surfaces** — no `awareness` sidebar item for antagonist NPCs
- **Per-arc-shape NPC visibility defaults**: family/ambient surfaces location + arousal + corruption + relation; slow-burn family surfaces location + arousal + relation; peer/dating surfaces location + relation; service surfaces location + relation; antagonist surfaces location ONLY (when Doc 64 PRD ships the `npc_location` sidebar item type)

### Step 8 — Emit `[[clothing]]` + `[[passes]]` + `[[items]]` (if applicable)

Per design book §1 enable flags. Minimal at `scope_mode: slice`. At `scope_mode: full_game`, enable any Phase 2+ system the design book §1 opted in (pregnancy mechanics, scandal awareness, gallery system, tracker primitive).

**Clothing system — read `doctrine/11_clothing_design.md` before authoring.** Requires `[settings]` from
Step 1 (`clothing_enabled` + wardrobe/shop locations) plus the items below. The RTS-faithful usage model:
clothing routes **PUBLIC / world content** (via `worn_corruption` / `worn_beauty` predicates, read live,
WEAN — they never mutate global corruption) and a **social** beauty gate; it does **NOT** gate NPC arcs
(those stay corruption + arousal + relationship — gating an NPC on the worn outfit is the backwards-on-ramp
anti-pattern, `doctrine/02` §8.12). If the game uses a persistent **exhibitionism** meter (raised by
public flash acts), declare it as a player trait in **Step 2** (`[player.core_traits]`) — `worn_*`
predicates need no declaration, but a stored `exhibitionism` trait does. Author a full starting outfit
(every slot, `initial = true`) so the player is never naked/blocked; put every `worn_*` consumer on a
**public** surface (street / park / shop / workplace floor).

```toml
[[clothing]]
id = "starter_outfit"
name = "Jeans and tee"
slot = "top"
initial = true
beauty = 5
type = "casual"

[[clothing]]
id = "bikini_top"
name = "Yellow bikini top"
slot = "top"
price = 25
beauty = 8
corruption = 15
type = "swim"

[[passes]]
id = "gym_membership"
name = "Gym membership"
cost = 50
duration_days = 30
```

### Step 9 — Per-NPC lane authoring (the bulk of the TOML)

For each NPC in design book §2 roster, emit canvases per the design book §4 brief's §5 lane content map.

**Order per NPC:**

1. **Lane 4 capstones first** — these are referenced by Lane 1 hub buttons + quest cards. Author them first so other canvases can reference them by ID.
2. **Lane 1 hub canvases** — **one per scheduled WINDOW** for the NPC (per-row coverage, D72-R6), each with `trigger.schedules` matching its `[[npcs.schedules]]` row; base renders unconditionally; rung set capped by the location exposure tier (public/semi-private/private, D72-R7). Period-split windows at the same location into separate hubs (D56-R1)
3. **Lane 1 route-target stubs** — tease / flash / explicit content reached via hub menu (NO `[canvases.trigger]` block)
4. **Lane 2 ambient canvases** — random encounters at NPC's locations
5. **Lane 3 parent activities** — Maya-solo dispatchers (if any per arc shape)
6. **Lane 3 substitution targets** — NPC walk-in scenes (`substitution_only = true`)

See §5 below for per-lane TOML templates.

### Step 10 — Emit `[[quest_cards]]`

Per design book §6 capstone chain map + per-arc card mode (capstone / mechanic / hybrid).

```toml
# Capstone-mode card (points at a Lane 4 capstone)
[[quest_cards]]
text         = "I'm new under this roof. Frank watches me and pretends he isn't."
ready_text   = "Something's about to give."
tip          = "He's around the house all day. I notice that."
npc_id       = "npc_frank"
ready_canvas = "scene_livingroom_catch"
when = [
  { flag = "frank_caught", op = "is_false" },
]
goals = [
  { trait = "corruption", subject = "player", op = "gte", value = 25, label = "Maya's corruption" },
]

# Pure-mechanic card (NO ready_canvas; threshold cross IS the unlock)
[[quest_cards]]
# unlocks at npc_marge.trust >= 20:
#   - scene_marge_diner_hub.base greeting flips from T0 to T1
text   = "I'm on Marge's floor. Work the shifts. Don't whine."
tip    = "Shifts pay the rent. Trust comes from showing up."
npc_id = "npc_marge"
when = [
  { flag = "hired_at_diner", op = "is_true" },
  { trait = "relation", subject = "npc", npc_id = "npc_marge", op = "lt", value = 20 },
]
goals = [
  { trait = "relation", subject = "npc", npc_id = "npc_marge", op = "gte", value = 20, label = "Marge trust" },
]

# Terminal card (LAST in NPC chain)
[[quest_cards]]
text     = "It's done either way."
npc_id   = "npc_frank"
priority = 1
terminal = true
when = [
  { flag = "diana_confronted", op = "is_true" },
]
```

See §7 below for quest card templates.

### Step 11 — Emit `[[fast_jobs]]` + `[bank]` (if applicable)

Per design book §1 economic engine.

### Step 12 — Validate + self-audit

Run the §11 quality gate checklist. Fix any violations BEFORE delivering.

---

## §5 — Per-lane TOML templates

Mirror the canonical examples in `schema/03_example_toml.md`.

### §5.1 — Lane 1 hub canvas (Frank kitchen morning gold standard)

This hub's `trigger.schedules` (05:30–09:00) matches Frank's kitchen schedule **row** — one hub per window (D72-R6). The kitchen at breakfast is a **private** household space, so the full ladder is fair here; a *public* hub (a diner floor with customers) would cap at talk/look only (D72-R7). The `base` node renders unconditionally — escalation lives on the menu rungs, never on the base.

```toml
[[canvases]]
id          = "frank_kitchen_morning_hub"
name        = "Kitchen — Frank, morning"
description = "Always-show RTS ladder hub for Frank in kitchen, morning slot. Locked-visible escalation rungs visible from day 1. Exposure: private (household) → full ladder."

[canvases.trigger]
location      = "loc_kitchen"
requires_npc  = "npc_frank"
is_repeatable = true
priority      = 10
is_active     = true
npc           = "npc_frank"
[[canvases.trigger.schedules]]
weekdays   = [0, 1, 2, 3, 4, 5, 6]
start_time = "05:30"
end_time   = "09:00"

[[canvases.nodes]]
id   = "base"
name = "Kitchen — morning, Frank present"
# CONSTANT opener (D56-R1). Three tier blocks would be authoring overhead;
# menu rungs encode progression via show_when_locked + conditions.
blocks = [
  { type = "image", props = { file = "scenes/frank_kitchen_morning_hub.jpg" } },
  { type = "paragraph", content = "Frank's at the counter. He looks up when you come in." },
  { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Morning." },
]

[canvases.nodes.exit_block]
type = "choices"

# Always-available relational base
[[canvases.nodes.exit_block.choices]]
text = "Pour him coffee."
targetType = "node"
nodeId = "frank_kitchen_morning_hub.pour_coffee"
time_progression_minutes = 5

# Locked-visible escalation ladder (4 rungs)
[[canvases.nodes.exit_block.choices]]
text = "Tease him ❤️‍🔥"
targetType = "node"
nodeId = "tease_kitchen_general.base"
show_when_locked = true
locked_text = "Not yet."
locked_text_threshold = "Maya's corruption: 5+"
conditions = { version = "1.0", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 5 },
] }

[[canvases.nodes.exit_block.choices]]
text = "Flash him 👀"
targetType = "node"
nodeId = "flash_kitchen_general.base"
show_when_locked = true
locked_text_threshold = "Maya's corruption: 15+"
conditions = { version = "1.0", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 15 },
] }

[[canvases.nodes.exit_block.choices]]
text = "Suck him here."
targetType = "node"
nodeId = "loop_franks_bedroom_sex.intro"
show_when_locked = true
locked_text_threshold = "Maya's corruption: 25+ AND Frank declared"
conditions = { version = "1.0", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 25 },
  { type = "flag", subject = "player", flag_key = "frank_bedroom_first_done", operator = "is_true" },
] }
effects = [
  { targetType = "player", trait = "sex_stage", op = "set", value = 1 },
  { targetType = "player", trait = "sex_entry_origin", op = "set", value = 1 },
]

[[canvases.nodes.exit_block.choices]]
text = "Have sex with him here 🔥"
targetType = "node"
nodeId = "loop_franks_bedroom_sex.intro"
show_when_locked = true
locked_text_threshold = "Maya's corruption: 25+ AND Frank declared"
conditions = { version = "1.0", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 25 },
  { type = "flag", subject = "player", flag_key = "frank_bedroom_first_done", operator = "is_true" },
] }

# Leave
[[canvases.nodes.exit_block.choices]]
text = "Leave."
targetType = "location"
locationId = "loc_hallway"
```

**Per-NPC adaptations:**
- **Marge (service):** ~4 unlocked menu items + 4 locked-visible Phase 3+ rungs (Tease/Flash/Eat-her-out/Let-her-take). Per Doc 53 §3.
- **Ryan (peer/dating):** simpler hub with relational items + 1 date-prep item; no sexual rungs in slice if vocab ceiling deferred.
- **Diana (antagonist):** no Lane 1 hub in slice (shared-space presence only via Lane 2 ambients).

### §5.2 — Lane 1 route-target stub (tease/flash/etc.)

Reachable ONLY via hub menu `nodeId` routing. NO `[canvases.trigger]` block.

```toml
[[canvases]]
id          = "tease_kitchen_general"
name        = "Kitchen — tease him"
description = "Stub Pattern A render. Reachable only via frank_kitchen_morning_hub menu."

# NO [canvases.trigger] BLOCK — route-only canvas

[[canvases.nodes]]
id   = "base"
name = "Kitchen — tease him"
blocks = [
  { type = "image", props = { file = "scenes/tease_kitchen_general.jpg" } },

  # T0 (pre-catch): held look only
  { type = "group", props = { conditions = { version = "1.0", items = [
      { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_false" },
    ] }, blocks = [
    { type = "paragraph", content = "You catch his eye over the mug and hold it. He's still looking when you look back." },
    { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Girl." },
  ] } },

  # T1 (post-catch, pre-cracked)
  { type = "group", props = { conditions = { version = "1.0", items = [
      { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_true" },
      { type = "flag", subject = "player", flag_key = "frank_cracked", operator = "is_false" },
    ] }, blocks = [
    { type = "paragraph", content = "You catch his eye. His look drops to your tits and stays there." },
    { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Mm." },
  ] } },

  # T2 (post-cracked)
  { type = "group", props = { conditions = { version = "1.0", items = [
      { type = "flag", subject = "player", flag_key = "frank_cracked", operator = "is_true" },
    ] }, blocks = [
    { type = "paragraph", content = "You catch his eye. He sets the mug down, crosses to you, backs you against the counter — hand under your shirt, thumb on your nipple." },
    { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Don't fucking start with me at breakfast, girl." },
  ] } },
]

[canvases.nodes.exit_block]
type = "choices"

# Lt/gte mutex on exit (corruption < 15 grants tick; ≥ 15 trivial-display wean stops paying)
[[canvases.nodes.exit_block.choices]]
text = "Drink your coffee."
targetType = "location"
locationId = "loc_kitchen"
time_progression_minutes = 5
conditions = { version = "1.0", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "lt", value = 15 },
]}
effects = [
  { targetType = "npc", npcId = "npc_frank", trait = "arousal", op = "add", value = 1, cap = 3 },
  { targetType = "player", trait = "arousal", op = "add", value = 1, cap = 10 },
  { targetType = "player", trait = "corruption", op = "add", value = 1 },
]

[[canvases.nodes.exit_block.choices]]
text = "Drink your coffee."
targetType = "location"
locationId = "loc_kitchen"
time_progression_minutes = 5
conditions = { version = "1.0", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 15 },
]}
effects = [
  { targetType = "npc", npcId = "npc_frank", trait = "arousal", op = "add", value = 1, cap = 3 },
  { targetType = "player", trait = "arousal", op = "add", value = 1, cap = 10 },
  # NO player.corruption tick at corruption 15+
]
```

### §5.3 — Lane 2 ambient with R2 in-fiction interruption

```toml
[[canvases]]
id          = "ambient_kitchen_frank_late_night_raid"
name        = "Kitchen — late night, both up for water"
description = "Lane 2 ambient: midnight kitchen encounter. 2 stage-flag tiers. T0 broken by Diana's floorboard; T1 bareback counter quickie. NO requires_npc — implied-presence override (Frank stepped out for water)."

[canvases.trigger]
location             = "loc_kitchen"
is_repeatable        = true
priority             = 6
is_active            = true
trigger_mode         = "random"
chance               = 0.40
max_triggers_per_day = 1
conditions = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "npc", npc_id = "npc_frank", trait_key = "arousal", operator = "gte", value = 1 },
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 25 },
] }
[[canvases.trigger.schedules]]
weekdays   = [0, 1, 2, 3, 4, 5, 6]
start_time = "22:00"
end_time   = "22:59"

[[canvases.nodes]]
id   = "base"
name = "Kitchen — late night, both up for water"
blocks = [
  { type = "image", props = { file = "scenes/ambient_kitchen_frank_late_night_raid.jpg" } },
  { type = "paragraph", content = "You didn't think anyone was awake; the kitchen light's already on. Frank's at the sink in sleep pants and nothing else, a glass of water in his hand." },

  # T0 — broken by Diana's floorboard (in-fiction interruption per D56-R2)
  { type = "group", props = { conditions = { version = "1.0", items = [
      { type = "flag", subject = "player", flag_key = "frank_first_night_done", operator = "is_false" },
    ] }, blocks = [
    { type = "cascade", props = { beats = [
      { blocks = [
        { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Couldn't sleep either." },
        { type = "paragraph", content = "You shake your head and cross to the cabinet. His eyes are on you in the long nightshirt and he doesn't pretend they aren't." },
      ] },
      { advance_text = "Step closer to the counter.", blocks = [
        { type = "paragraph", content = "You step in for a glass; his hands find your waist first and lift you onto the counter. Your legs go around him without thinking." },
        { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Quiet, girl." },
      ] },
      { advance_text = "Kiss him.", blocks = [
        { type = "paragraph", content = "His mouth on yours, one hand under the nightshirt at the small of your back, the other on your thigh. You make a sound you shouldn't and he swallows it." },
      ] },
      # R2 interruption — external (Diana's floorboard)
      { advance_text = "Hear the floorboard upstairs.", blocks = [
        { type = "paragraph", content = "Diana's floorboard, her bedroom door. He lifts you down, hands you your glass, turns the tap on like he was doing dishes." },
        { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Night, girl." },
      ] },
    ] } },
  ] } },

  # T1 — blows through the interruption (post-first-night)
  { type = "group", props = { conditions = { version = "1.0", items = [
      { type = "flag", subject = "player", flag_key = "frank_first_night_done", operator = "is_true" },
    ] }, blocks = [
    { type = "cascade", props = { beats = [
      { blocks = [
        { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Knew you'd come down." },
        { type = "paragraph", content = "He sets the glass down and has your nightshirt up before you reach the cabinet. He lifts you onto the counter, no underwear under the shirt." },
      ] },
      { advance_text = "Pull him in.", blocks = [
        { type = "paragraph", content = "You pull him in by the waistband and he slides into you bare on the counter. *'Daddy,'* you breathe into his neck to keep it quiet." },
        { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Good girl. Fast, then." },
      ] },
      { advance_text = "Fast, then.", blocks = [
        { type = "paragraph", content = "He fucks you fast on the counter, hand over your mouth, and cums inside you before the house stirs. He lifts you down and hands you the glass you came for." },
        { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Night, girl." },
      ] },
    ] } },
  ] } },
]

[canvases.nodes.exit_block]
type = "location"
text = "Take the glass. Go back to bed."

[canvases.nodes.exit_block.config]
destinationType          = "specific"
locationId               = "loc_kitchen"
time_progression_minutes = 15
effects = [
  { targetType = "npc", npcId = "npc_frank", trait = "arousal", op = "add", value = 1, cap = 3 },
  { targetType = "player", trait = "arousal", op = "add", value = 1, cap = 10 },
  { targetType = "npc", npcId = "npc_frank", trait = "corruption", op = "add", value = 1 },
  { targetType = "player", trait = "corruption", op = "add", value = 2 },
  { targetType = "player", trait = "energy", op = "add", value = -18 },
  { targetType = "npc", npcId = "npc_diana", trait = "awareness", op = "add", value = 2 },
]
```

### §5.4 — Lane 3 dispatcher parent (Pattern A multi-NPC-ready)

```toml
[[canvases]]
id          = "activity_make_tea"
name        = "Make a cup of tea"
description = "Maya-solo dispatcher. Kitchen. Substitution target: scene_frank_passes_kitchen_door."

[canvases.trigger]
location      = "loc_kitchen"
is_repeatable = true
priority      = 3
is_active     = true
[[canvases.trigger.substitutions]]
target_canvas_id = "scene_frank_passes_kitchen_door"
chance           = 0.30
conditions = { version = "1.0", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 5 },
] }
# Multi-NPC: add more substitution rules per NPC, ordered by narrative priority (Pattern A first-match)
# [[canvases.trigger.substitutions]]
# target_canvas_id = "scene_jake_passes_kitchen_door"
# chance = 0.25
# conditions = { ... }
[[canvases.trigger.schedules]]
weekdays   = [0, 1, 2, 3, 4, 5, 6]
start_time = "07:00"
end_time   = "22:00"

[[canvases.nodes]]
id   = "base"
name = "Make a cup of tea"
blocks = [
  { type = "image", props = { file = "activities/make_tea.jpg" } },
  { type = "paragraph", content = "She fills the kettle from the tap. Sets it on the burner. Drops a tea bag in the mug while the water comes up. The kitchen quiet around her. The kettle clicks when it's hot. She pours." },
]

[canvases.nodes.exit_block]
type = "location"
text = "Take the mug back to your room."

[canvases.nodes.exit_block.config]
destinationType          = "specific"
locationId               = "loc_kitchen"
time_progression_minutes = 10
effects = [
  { targetType = "player", trait = "energy", op = "add", value = 2 },
]
```

### §5.4a — Multi-NPC dispatcher patterns (A / B / C — all engine-supported as of Doc 69, 2026-05-27)

**Read this before authoring any multi-NPC Lane 3 dispatcher.** Three patterns from Doc 67 §4. All three ship natively in the engine; pick by authoring intent, not by engine limitation. Mirror of `doctrine/02_three_lanes_plus_capstone.md` §9 (canonical source — re-read if this section drifts):

| Pattern | Engine support | Emit how |
|---|---|---|
| **A — sequential first-match** (RTS `WashDishes` shape) | ✅ Native | Multiple `[[canvases.trigger.substitutions]]` blocks in narrative-priority order, each with own `chance` + `conditions`. Each rule rolls its own dice; first match wins. Template = §5.4 above. |
| **B — single dice partition** (RTS `BedroomStudy` shape — exactly one of N variants fires per attempt, else solo) | ✅ Native via `exclusive_group` (`v2.py:4671-4713`, Doc 69 Item 1) | Multiple substitution rules sharing the same `exclusive_group = "<name>"` string. Engine partitions ONE dice roll into cumulative `chance` buckets. Failed target/conditions in a claimed slot falls to solo — does NOT promote next rule. Template below. |
| **C — post-activity event check** (RTS `Exercise` shape — solo activity always grants effect; substitute layers an NPC walk-in on top) | ✅ Native via `pre_substitution_effects` on parent trigger (`v2.py:11151`, Doc 69 Item 2) | Effects on parent trigger run BEFORE the substitution check, so both solo and substituted paths receive them. Substitute canvases do NOT re-emit the effect. Template below. |

#### Pattern B — `exclusive_group` TOML template

Brother sub-variants at the study desk: grope vs help-study, exactly one fires per attempt or fall to solo.

```toml
[canvases.trigger]
location      = "loc_bedroom"
is_repeatable = true
priority      = 3
is_active     = true

[[canvases.trigger.substitutions]]
target_canvas_id = "scene_brother_grope_at_desk"
chance           = 0.1667                          # 1/6
exclusive_group  = "study_desk_brother"
conditions = { version = "1.0", items = [
  { type = "trait", subject = "npc", npc_id = "npc_brother", trait_key = "corruption", operator = "gte", value = 5 },
] }

[[canvases.trigger.substitutions]]
target_canvas_id = "scene_brother_help_study"
chance           = 0.1667                          # 1/6 — group cumulative bucket = 0.33
exclusive_group  = "study_desk_brother"
conditions = { version = "1.0", items = [
  { type = "trait", subject = "npc", npc_id = "npc_brother", trait_key = "love", operator = "gte", value = 3 },
] }
```

**Probability math:** With both rules at `chance = 0.1667`, group cumulative bucket = 0.33; remaining 0.67 of the dice space falls to solo. Failed-condition in a claimed slot also falls to solo (does NOT promote next rule).

**Mixed Pattern A + Pattern B in the same dispatcher is supported.** Rules WITH `exclusive_group` process first (one dice per group); rules WITHOUT `exclusive_group` process after via Pattern A first-match.

**Do not approximate Pattern B via summed Pattern A chances** — the engine extension is shipped; emit `exclusive_group` directly. The pre-2026-05-27 approximation diverges on both probability (1 − ∏(1 − cᵢ) ≈ 42% vs true 50% for 3×1/6) and fall-through (Pattern A promotes to next rule on failed conditions; Pattern B falls to solo).

#### Pattern C — `pre_substitution_effects` TOML template

For solo activities with unconditional outcomes (Exercise grants `+fitness` regardless of who walks in):

```toml
[[canvases]]
id          = "activity_exercise"
name        = "Exercise"
description = "Maya-solo dispatcher. Bedroom. Solo grants +fitness; NPC walk-ins layer on top (Pattern C)."

[canvases.trigger]
location      = "loc_bedroom"
is_repeatable = true
priority      = 3
is_active     = true

# Pattern C — effects run BEFORE the substitution roll, on both solo and substituted paths (Doc 69 Item 2)
# Shape = TemplateChoiceEffect (schema/02 §16): { targetType, npcId?, trait, op, value, clamp?, cap? } — no `type` field
[[canvases.trigger.pre_substitution_effects]]
targetType = "player"
trait      = "fitness"
op         = "add"
value      = 1

[[canvases.trigger.substitutions]]
target_canvas_id = "scene_frank_walks_in_exercise"
chance           = 0.20
conditions = { version = "1.0", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 10 },
] }
```

The substitute canvas (`scene_frank_walks_in_exercise`) does NOT need to re-emit the `+fitness` effect — it already ran on the parent trigger before substitution resolved.

#### Selection rule (mirror of doctrine/02 §4.7)

If the design book calls for a multi-NPC walk-in beat at a Maya-solo activity, classify it against this decision tree:

1. **Are the variants mutually exclusive in fiction?** (Cannot have two of the variants fire simultaneously — e.g., Brother grope vs Brother help-study at the same study desk attempt.) → **Pattern B**, emit `exclusive_group`.
2. **Does the solo activity have its own outcome that should fire regardless of who walks in?** (Exercise = +fitness whether you finished alone or got interrupted.) → **Pattern C**, emit `pre_substitution_effects` on the parent trigger.
3. **Otherwise** — independent walk-in chances per NPC, narrative-priority ordered. → **Pattern A** (default), no `exclusive_group`, no `pre_substitution_effects`.

Pattern B + Pattern C can combine on the same dispatcher when both intents apply.

### §5.5 — Lane 3 substitution target (substitution_only)

```toml
[[canvases]]
id          = "scene_frank_passes_kitchen_door"
name        = "Kitchen — Frank passes the door"
description = "Lane 3 substitution on activity_make_tea. Frank passes through, pauses at the door, stops near her."

[canvases.trigger]
location             = "loc_kitchen"
is_repeatable        = true
priority             = 4
is_active            = true
substitution_only    = true        # NOT clickable; reached only via dispatcher
requires_npc         = "npc_frank" # loose NPC presence (any home location per his schedule)
max_triggers_per_day = 1            # D67-R7

[[canvases.nodes]]
id   = "base"
name = "Kitchen — Frank passes the door"
blocks = [
  { type = "image", props = { file = "scenes/scene_frank_passes_kitchen_door.jpg" } },
  { type = "paragraph", content = "You're waiting on the kettle when Frank comes through the kitchen on his way to the back of the house. He doesn't pass straight through." },

  # T0 (pre-catch): brief contact + moves on
  { type = "group", props = { conditions = { version = "1.0", items = [
      { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_false" },
    ] }, blocks = [
    { type = "cascade", props = { beats = [
      { blocks = [
        { type = "paragraph", content = "He stops behind you in the narrow galley instead of going by, close enough that you feel him at your back reaching past you for nothing in particular." },
        { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Don't mind me, girl." },
      ] },
      { advance_text = "Hold still.", blocks = [
        { type = "paragraph", content = "His hand settles at your waist a beat too long for getting by, then he's moving again, out the far door. The kettle's still not boiling." },
      ] },
    ] } },
  ] } },

  # T1 (post-catch, pre-cracked): turns her by the hip
  # T2 (post-cracked): pulls her back to his chest, hand down her front
  # (continue tier blocks per design book §4 brief's tier mapping)
]

[canvases.nodes.exit_block]
type = "location"
text = "Take the mug back to your room."

[canvases.nodes.exit_block.config]
destinationType          = "specific"
locationId               = "loc_kitchen"
time_progression_minutes = 10
effects = [
  { targetType = "npc", npcId = "npc_frank", trait = "arousal", op = "add", value = 1, cap = 3 },
  { targetType = "player", trait = "arousal", op = "add", value = 1, cap = 10 },
  { targetType = "player", trait = "corruption", op = "add", value = 1 },
]
```

### §5.6 — Lane 4 capstone Type A (linear deterministic)

```toml
[[canvases]]
id          = "canvas_marge_interview"
name        = "Marge — interview"
description = "Hire capstone. Fires once at diner_front, gated on hired_at_diner is_false. Type A linear."

[canvases.trigger]
location      = "loc_diner_front"
is_repeatable = false                # Type A fingerprint
priority      = 9                    # ≥ 9 wins against Lane 2 randoms
is_active     = true
conditions = { version = "1.0", logic = "AND", items = [
  { type = "flag", subject = "player", flag_key = "hired_at_diner", operator = "is_false" },
] }

[[canvases.nodes]]
id   = "interview"
name = "Interview"
# Tier-3 prose EARNED at capstone (per doctrine/05 §3)
blocks = [
  { type = "image", props = { file = "scenes/marge_interview.jpg" } },
  { type = "paragraph", content = "Marge looked up when the bell over the door went off. She didn't smile — Marge wasn't a smiler at first read. She poured a coffee Maya hadn't asked for and slid it across the counter." },
  { type = "dialog", props = { speaker = "npc", npcId = "npc_marge" }, content = "You're Diana's girl." },
  { type = "paragraph", content = "Maya nodded. Marge looked her over once — not the up-and-down men did, the up-and-down a woman who had hired forty waitresses did. The shoes. The hands." },
  { type = "dialog", props = { speaker = "npc", npcId = "npc_marge" }, content = "Five hours, four-fifty an hour, you keep your tips. Tonight if you want it. Cookie's in the back, she'll show you the float." },
  { type = "paragraph", content = "She didn't wait for an answer. She slid the apron across with the back of her hand and turned to the next customer." },
]

[canvases.nodes.exit_block]
type = "choices"

[[canvases.nodes.exit_block.choices]]
text = "Take the apron."
targetType = "trigger"
time_progression_minutes = 30
effects = [
  { targetType = "npc", npcId = "npc_marge", trait = "relation", op = "add", value = 5 },
  { targetType = "player", trait = "energy", op = "add", value = -3 },
]
flagEffects = [
  { targetType = "player", flag = "hired_at_diner", op = "set" },          # capstone setter — D57-R1
  { targetType = "player", flag = "talked_to_marge_today", op = "set" },
  { targetType = "player", flag = "phone_active", op = "set" },             # cross-arc write — phone unlock per Doc 46
]
```

### §5.7 — Lane 4 capstone Type B (Pattern F fork)

```toml
[[canvases]]
id          = "scene_franks_bedroom_evening"
name        = "Frank's bedroom — first night"
description = "Stage 4 FIRST-NIGHT cascade. Pattern E linear cascade + Pattern F fork at terminal beat. Accept sets first_done flag; Refuse re-fires next eligible night."

[canvases.trigger]
location      = "loc_franks_bedroom"
requires_npc  = "npc_frank"
is_repeatable = true                 # Note: true + self-gate (F4 retry pattern)
priority      = 9
is_active     = true
npc           = "npc_frank"
conditions = { version = "1.0", logic = "AND", items = [
  { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_true" },
  { type = "flag", subject = "player", flag_key = "frank_bedroom_first_done", operator = "is_false" },
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 25 },
] }
[[canvases.trigger.schedules]]
weekdays   = [0, 1, 2, 3, 4]
start_time = "21:00"
end_time   = "23:00"

[[canvases.nodes]]
id   = "base"
name = "Frank's bedroom — evening"
blocks = [
  { type = "image", props = { file = "scenes/franks_bedroom_evening.jpg" } },

  # Cascade Beats 0-2 — terminal at Beat 2 (Pattern F fork follows in exit_block)
  { type = "cascade", props = { beats = [
    # Beat 0 — unconditional opener
    { blocks = [
      { type = "paragraph", content = "She walks the hallway slow. The boards she knows the squeak of from the wrong side, the runner Diana picked out three summers ago, the bathroom door closed and dark. The door at the end is the door she's only ever walked past." },
    ] },
    # Beat 1
    { advance_text = "Push the door open.", blocks = [
      { type = "paragraph", content = "It's open by an inch. Lamp light on the floorboards. She pushes it the rest of the way and steps in." },
      { type = "paragraph", content = "Frank in the chair by the window. He's not undressed. Just sitting in the way he sits — weight on one elbow, the lamp catching the side of his face, a paperback open in his lap that he hasn't been reading. He sets it down on the nightstand without marking the page." },
      { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Close the door." },
    ] },
    # Beat 2 — TERMINAL. Per-beat effects fire on click. Fork follows.
    { advance_text = "Close the door.", effects = [
      { targetType = "npc", npcId = "npc_frank", trait = "arousal", op = "add", value = 1, cap = 3 },
      { targetType = "player", trait = "arousal", op = "add", value = 1, cap = 10 },
    ], blocks = [
      { type = "paragraph", content = "She closes it. The latch clicks soft. The room is small the way the office is small but it isn't the office — there's no desk between them. Just the bed turned back and the lamp on and Frank standing now from the chair." },
      { type = "thought_bubble", props = { speaker = "npc_frank" }, content = "She came." },
      { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Come here." },
    ] },
  ] } },
]

[canvases.nodes.exit_block]
type = "choices"

# Pattern F fork — F1 + F2 + F3 + F4
[[canvases.nodes.exit_block.choices]]
text = "Cross to him."
targetType = "node"
nodeId = "scene_franks_bedroom_evening.node_first_night_climax"
effects = [
  { targetType = "player", trait = "corruption", op = "add", value = 1 },   # F2 secondary divergence
]

[[canvases.nodes.exit_block.choices]]
text = "Hesitate. Step back."
targetType = "node"
nodeId = "scene_franks_bedroom_evening.node_first_night_refuse"
# NO effects. NO flag set. F4: canvas re-fires next eligible night.

# Then [[canvases.nodes]] for node_first_night_climax (sets frank_bedroom_first_done + sex cascade)
# Then [[canvases.nodes]] for node_first_night_refuse (sets nothing, exits to hallway)
```

---

## §6 — Effect + predicate templates (the field-name minefield)

The #1 silent-failure mode. Per `schema/02_toml_schema.md` §16.

### §6.1 — Reference card (KEEP HANDY)

| Concept | EFFECT field | PREDICATE field |
|---|---|---|
| Player vs NPC | `targetType` | `subject` |
| NPC identifier | `npcId` | `npc_id` |
| Trait name | `trait` | `trait_key` |
| Flag name | `flag` | `flag_key` |
| Operation | `op` (`"add"`, `"set"` for traits; `"set"`, `"unset"`, `"toggle"` for flags) | `operator` (`"gte"`, `"lt"`, etc.) |
| Type discriminator | (dispatched by `trait` vs `flag` field presence) | `type` (required: `"trait"`, `"flag"`, etc.) |

**Mixing them produces silent no-ops — NO BUILD ERROR FIRES.**

### §6.2 — Trait effect templates

```toml
# Player trait — add
{ targetType = "player", trait = "corruption", op = "add", value = 1 }

# Player trait — set (climax reset)
{ targetType = "player", trait = "arousal", op = "set", value = 0 }

# Player trait — decay via negative add (NO "sub" op)
{ targetType = "player", trait = "energy", op = "add", value = -10 }

# NPC trait — add
{ targetType = "npc", npcId = "npc_frank", trait = "relation", op = "add", value = 2 }

# NPC trait — with cap (family NPC arousal max 3)
{ targetType = "npc", npcId = "npc_frank", trait = "arousal", op = "add", value = 1, cap = 3 }

# Stage advancement — on PLAYER namespace, NOT npc namespace
{ targetType = "player", trait = "frank_stage", op = "set", value = 2 }
```

### §6.3 — Flag effect templates

```toml
{ targetType = "player", flag = "frank_caught", op = "set" }
{ targetType = "player", flag = "talked_to_ryan_today", op = "unset" }
{ targetType = "npc", npcId = "npc_frank", flag = "secret_known", op = "set" }
{ targetType = "player", flag = "scandal_visible", op = "toggle" }
```

### §6.4 — Predicate (condition) templates

```toml
# Trait conditions
{ type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 15 }
{ type = "trait", subject = "npc", npc_id = "npc_frank", trait_key = "relation", operator = "gte", value = 30 }

# Stage check — on PLAYER namespace
{ type = "trait", subject = "player", trait_key = "frank_stage", operator = "gte", value = 2 }

# Flag conditions
{ type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_true" }
{ type = "flag", subject = "player", flag_key = "frank_cracked", operator = "is_false" }

# Clothing predicates (Doc 72)
{ type = "worn_type", operator = "eq", value = "swim" }
{ type = "worn_beauty", operator = "gte", value = 30 }
{ type = "worn_corruption", operator = "gte", value = 15 }

# Item / pass / quest
{ type = "item", subject = "player", item_id = "pregnancy_test", operator = "gte", value = 1 }
{ type = "pass", pass_id = "gym_membership", operator = "is_active" }
```

### §6.5 — Common mistakes

| Wrong | Right | Why |
|---|---|---|
| `{ type = "trait", targetType = "player", trait = "x", op = "gte", value = 5 }` | `{ type = "trait", subject = "player", trait_key = "x", operator = "gte", value = 5 }` | Predicate uses `subject`/`trait_key`/`operator`; this looks like effect syntax |
| `{ subject = "player", trait_key = "x", op = "add", value = 1 }` | `{ targetType = "player", trait = "x", op = "add", value = 1 }` | Effect uses `targetType`/`trait`; this looks like predicate syntax |
| `{ targetType = "player", trait = "energy", op = "sub", value = 10 }` | `{ targetType = "player", trait = "energy", op = "add", value = -10 }` | No `sub` op; use negative `add` |
| `{ targetType = "npc", npcId = "npc_frank", trait = "stage", op = "set", value = 2 }` | `{ targetType = "player", trait = "frank_stage", op = "set", value = 2 }` | Stage lives on player namespace as `<slug>_stage` |
| `{ targetType = "npc", trait = "corruption", op = "add", value = 1 }` | `{ targetType = "npc", npcId = "npc_frank", trait = "corruption", op = "add", value = 1 }` | NPC effects require `npcId` |

---

## §7 — Quest card templates

### §7.1 — Capstone-mode card

Points at a Lane 4 capstone. Has `ready_canvas`. May have `goals` for climbing display (D50-R2).

```toml
[[quest_cards]]
text         = "I'm new under this roof. Frank watches me and pretends he isn't."
ready_text   = "Something's about to give."
tip          = "He's around the house all day. I notice that."
npc_id       = "npc_frank"
ready_canvas = "scene_livingroom_catch"
when = [
  { flag = "frank_caught", op = "is_false" },
]
goals = [
  { trait = "corruption", subject = "player", op = "gte", value = 25, label = "Maya's corruption" },
]
```

**Note:** quest card conditions use FLAT shape (`flag` + `op`, NOT `type` + `flag_key` + `operator`). Different from trigger conditions. See `schema/02_toml_schema.md` §16.5.

### §7.2 — Pure-mechanic card

No `ready_canvas`. `goals` block tracks the climb. `# unlocks:` comment names what crosses at threshold (D50-R5).

```toml
[[quest_cards]]
# unlocks at npc_marge.relation >= 20:
#   - scene_marge_diner_hub.base greeting flips from T0 ("hon, which is it today")
#     to T1 ("There she is. Coffee's fresh.")
text   = "I'm on Marge's floor. Work the shifts. Don't whine."
tip    = "Shifts pay the rent. Trust comes from showing up."
npc_id = "npc_marge"
when = [
  { flag = "hired_at_diner", op = "is_true" },
  { trait = "relation", subject = "npc", npc_id = "npc_marge", op = "lt", value = 20 },
]
goals = [
  { trait = "relation", subject = "npc", npc_id = "npc_marge", op = "gte", value = 20, label = "Marge trust" },
]
```

### §7.3 — Terminal card

`terminal = true`. Last card in NPC chain. Renders "✓ Arc complete" (D50-R3).

```toml
[[quest_cards]]
text     = "It's done either way."
npc_id   = "npc_frank"
priority = 1
terminal = true
when = [
  { flag = "diana_confronted", op = "is_true" },
]
```

### §7.4 — Pure-mechanic chain (Marge M3/M4/M5 pattern)

Bounded `when` ranges so picker swaps atomically as threshold crosses (D50-R2 + D54 §4.3).

```toml
[[quest_cards]]
# unlocks at marge.relation >= 5: greeting tier-1 line
text   = "I've been getting my hours."
npc_id = "npc_marge"
when = [
  { flag = "hired_at_diner", op = "is_true" },
  { trait = "relation", subject = "npc", npc_id = "npc_marge", op = "lt", value = 5 },
]
goals = [{ trait = "relation", subject = "npc", npc_id = "npc_marge", op = "gte", value = 5, label = "Marge trust" }]

[[quest_cards]]
# unlocks at marge.relation >= 15: marge_hub menu item "Talk shop"
text   = "She lets me sit at the counter now."
npc_id = "npc_marge"
when = [
  { trait = "relation", subject = "npc", npc_id = "npc_marge", op = "gte", value = 5 },
  { trait = "relation", subject = "npc", npc_id = "npc_marge", op = "lt", value = 15 },
]
goals = [{ trait = "relation", subject = "npc", npc_id = "npc_marge", op = "gte", value = 15, label = "Marge trust" }]
```

---

## §8 — Sidebar item templates

Per `doctrine/09_trait_catalog.md` §8 + `reference/04_rts_hud_world_model.md` §3.

### §8.1 — Maya state (mandatory across all RTS-shape games)

```toml
# Banded corruption
[[sidebar_items]]
type = "trait_words"
trait = "corruption"
label = "Status"
bands = [
  { min = 0,  max = 24, text = "Pure",   icon = "✨" },
  { min = 25, max = 49, text = "Lewd",   icon = "💋" },
  { min = 50, max = 74, text = "Slutty", icon = "🔥" },
  { min = 75, max = 100, text = "Whore", icon = "💦" },
]

# Arousal bar
[[sidebar_items]]
type = "trait_bar"
trait = "arousal"
label = "Arousal"
max = 10
bands = [
  { min = 0, max = 2, text = "Cold" },
  { min = 3, max = 5, text = "Warm" },
  { min = 6, max = 8, text = "Hot" },
  { min = 9, max = 10, text = "Burning" },
]

# Body-state — energy
[[sidebar_items]]
type = "trait_status_text"
trait = "energy"
bands = [
  { min = 0, max = 24, text = "Exhausted", icon = "🪫" },
  { min = 25, max = 49, text = "Tired", icon = "💤" },
  { min = 50, max = 74, text = "Fine", icon = "🟢" },
  { min = 75, max = 100, text = "Rested", icon = "🔋" },
]

# Body-state — hygiene
[[sidebar_items]]
type = "trait_status_text"
trait = "hygiene"
bands = [
  { min = 0, max = 24, text = "Filthy", icon = "🧫" },
  { min = 25, max = 49, text = "Dirty", icon = "🌫️" },
  { min = 50, max = 74, text = "Fresh", icon = "🪞" },
  { min = 75, max = 100, text = "Clean", icon = "🧼" },
]
```

### §8.2 — Tier 2 stats (declare only if game uses)

```toml
[[sidebar_items]]
type = "trait_bar"
trait = "fitness"
label = "Fitness"
max = 100
# (if exercise/gym mechanic exists)

[[sidebar_items]]
type = "trait_bar"
trait = "exhibitionism"
label = "Exhibition"
max = 100
bands = [
  { min = 0, max = 24, text = "Modest" },
  { min = 25, max = 49, text = "Open" },
  { min = 50, max = 74, text = "Bold" },
  { min = 75, max = 100, text = "Brazen" },
]
# (if flash/cam arc exists)
```

### §8.3 — Per-NPC radar (Doc 64 PRD pending — author against future shape)

When Doc 64 ships, `npc_location` sidebar item type becomes available:

```toml
# Family/ambient default
[[sidebar_items]]
type = "npc_location"
npc_id = "npc_frank"
label = "Frank"
stats = ["arousal", "corruption", "relation"]

# Slow-burn family default
[[sidebar_items]]
type = "npc_location"
npc_id = "npc_jake"
label = "Jake"
stats = ["arousal", "relation"]

# Peer/dating default
[[sidebar_items]]
type = "npc_location"
npc_id = "npc_ryan"
label = "Ryan"
stats = ["relation"]

# Service default
[[sidebar_items]]
type = "npc_location"
npc_id = "npc_marge"
label = "Marge"
stats = ["relation"]

# Antagonist — LOCATION ONLY (no stats)
[[sidebar_items]]
type = "npc_location"
npc_id = "npc_diana"
label = "Diana"
stats = []
```

### §8.4 — DO NOT surface

- **No `<slug>_stage` sidebar items** for ANY NPC (per `doctrine/09_trait_catalog.md` §9)
- **No `awareness` sidebar item** for antagonist NPCs (per Doc 30 §6 + `doctrine/09_trait_catalog.md` §8)
- **No money sidebar item with banded poverty/wealth** unless game design specifically calls for banded display
- **No per-NPC `trait_bar` / `trait_words`** (e.g. `[[sidebar_items]] type="trait_bar" npc_id="npc_x" trait="relation"`). UNSUPPORTED: the engine resolves `trait` against `player.core_traits` regardless of `npc_id`, so it HARD-FAILS ("trait 'relation' not found in player.core_traits") or silently shows the PLAYER's stat. NPC progression (arousal/relation/stage) belongs on the **Quests page** (V2 cards). The only per-NPC sidebar item is the Doc-64 `npc_location` type above — and it is PENDING, so do not emit it yet. (Late Shifts build failed on four npc-scoped `trait_bar`s.)

---

## §9 — Worked example

Below is a complete TOML emission for a minimal 3-NPC 1-location slice — enough to demonstrate the full structure. Production games would have ~20-50K lines of TOML for a full slice; this is the shape, not the volume.

```toml
schema_version = "1.0"

[project]
id = "minimal_slice"          # TOML field is `id` (NOT `slug`) — see §1.2
title = "Minimal Slice"
description = "Demonstration TOML — 3-NPC RTS-shape sandbox skeleton."
quests_engine = "v2"
starting_canvas = "canvas_first_morning"   # auto-plays on new game

[time]
starting_hour = 8
starting_day = "Monday"
starting_week = 1

# Enable-switches → [settings] TABLE, not bare keys (§1.3 scoping trap).
[settings]
clothing_enabled = true
wardrobe_location = "loc_mayas_room"
shop_location = "loc_thrift_store"

# ───── Player ─────
[player]
id = "player"
name = "Maya"
portrait = "maya.jpg"

[player.core_traits]
corruption = 0
arousal = 0
energy = 100
hygiene = 100
money = 80
frank_stage = 0
marge_stage = 0
fitness = 0
beauty = 0
exhibitionism = 0
intelligence = 0

# ───── NPCs ─────
[[npcs]]
id = "npc_frank"
name = "Frank"
description = "48. Broad through the shoulders, calloused hands. Salt-and-pepper hair, work boots by the door. Owns the property."
portrait = "frank.jpg"
core_traits = { arousal = 0, corruption = 0, relation = 0 }
arc_stages = ["Suspicious", "Grudging warmth", "Restrict", "Tease", "Cracked"]

[npcs.trait_decay]
relation = 0.5

[[npcs.schedules]]
location = "loc_kitchen"
weekdays = [0, 1, 2, 3, 4, 5, 6]
start_time = "05:30"
end_time = "09:00"
activity = "morning coffee"

[[npcs.schedules]]
location = "loc_franks_bedroom"
weekdays = [0, 1, 2, 3, 4, 5, 6]
start_time = "23:00"
end_time = "06:00"
activity = "asleep"

[[npcs]]
id = "npc_marge"
name = "Marge"
description = "Late 40s. Diner owner. Apron, pencil behind her ear."
portrait = "marge.jpg"
core_traits = { relation = 0 }
arc_stages = ["Indifferent", "Trusted"]

[[npcs.schedules]]
location = "loc_diner_front"
weekdays = [0, 1, 2, 3, 4, 5]
start_time = "09:00"
end_time = "22:00"
activity = "running the diner"

[[npcs]]
id = "npc_diana"
name = "Diana"
description = "40s. Frank's wife / Maya's mother. Estranged."
portrait = "diana.jpg"
core_traits = { relation = 5, awareness = 0 }
# arc_stages = [] for antagonist

[[npcs.schedules]]
location = "loc_dianas_bedroom"
weekdays = [0, 1, 2, 3, 4, 5, 6]
start_time = "21:30"
end_time = "07:30"
activity = "her bedroom"

# ───── Locations ─────
[[locations]]
id = "loc_hallway"
name = "Hallway"
description = "The hallway between the bedrooms."
is_container = true
navigation_order = ["loc_mayas_room", "loc_franks_bedroom", "loc_dianas_bedroom", "loc_kitchen", "loc_living_room", "loc_bathroom", "loc_main_street"]

[[locations]]
id = "loc_kitchen"
name = "Kitchen"
description = "Worn tile, white cabinets, kettle on the gas burner."
entry_from = "loc_hallway"

[[locations]]
id = "loc_franks_bedroom"
name = "Frank's Bedroom"
description = "His room. The bed against the far wall."
entry_from = "loc_hallway"
entry_conditions = { version = "1.0", items = [
  { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_true" },
] }
blocked_message = "Not yet. He hasn't invited me."

[[locations]]
id = "loc_main_street"
name = "Main Street"
description = "The town's one street."
is_container = true

[[locations]]
id = "loc_diner_front"
name = "Diner"
description = "Marge's diner. Counter + booths + open kitchen."
entry_from = "loc_main_street"

# ───── Daily tick ─────
[engine.daily_tick]
flagEffects = [
  { targetType = "player", flag = "talked_to_frank_today", op = "unset" },
  { targetType = "player", flag = "talked_to_marge_today", op = "unset" },
]
traitEffects = [
  { targetType = "player", trait = "hygiene", op = "add", value = -10 },
  { targetType = "player", trait = "arousal", op = "add", value = 1, cap = 10 },
  { targetType = "npc", npcId = "npc_frank", trait = "arousal", op = "add", value = 1, cap = 3 },
]

# ───── Sidebar ─────
[[sidebar_items]]
type = "trait_words"
trait = "corruption"
label = "Status"
bands = [
  { min = 0, max = 24, text = "Pure" },
  { min = 25, max = 49, text = "Lewd" },
  { min = 50, max = 74, text = "Slutty" },
  { min = 75, max = 100, text = "Whore" },
]

[[sidebar_items]]
type = "trait_bar"
trait = "arousal"
label = "Arousal"
max = 10

[[sidebar_items]]
type = "trait_status_text"
trait = "hygiene"
bands = [
  { min = 0, max = 24, text = "Filthy" },
  { min = 25, max = 49, text = "Dirty" },
  { min = 50, max = 74, text = "Fresh" },
  { min = 75, max = 100, text = "Clean" },
]

[[sidebar_items]]
type = "trait_status_text"
trait = "energy"
bands = [
  { min = 0, max = 24, text = "Exhausted" },
  { min = 25, max = 49, text = "Tired" },
  { min = 50, max = 74, text = "Fine" },
  { min = 75, max = 100, text = "Rested" },
]

# ───── Clothing ─────
[[clothing]]
id = "starter_outfit"
name = "Jeans and tee"
slot = "top"
initial = true
beauty = 5
type = "casual"

# ───── Capstone canvases (Lane 4) authored FIRST so other canvases can reference them ─────

# Type A — Marge hire
[[canvases]]
id = "canvas_marge_interview"
name = "Marge — interview"
description = "Hire capstone. Type A linear."

[canvases.trigger]
location      = "loc_diner_front"
is_repeatable = false
priority      = 9
conditions = { version = "1.0", items = [
  { type = "flag", subject = "player", flag_key = "hired_at_diner", operator = "is_false" },
] }

[[canvases.nodes]]
id   = "interview"
name = "Interview"
blocks = [
  { type = "image", props = { file = "scenes/marge_interview.jpg" } },
  { type = "paragraph", content = "Marge looked up when the bell over the door went off. She didn't smile." },
  { type = "dialog", props = { speaker = "npc", npcId = "npc_marge" }, content = "You're Diana's girl." },
  { type = "paragraph", content = "Maya nodded. Marge looked her over once." },
  { type = "dialog", props = { speaker = "npc", npcId = "npc_marge" }, content = "Five hours, four-fifty an hour, you keep your tips. Tonight if you want it." },
]

[canvases.nodes.exit_block]
type = "choices"

[[canvases.nodes.exit_block.choices]]
text = "Take the apron."
targetType = "location"
locationId = "loc_diner_front"
time_progression_minutes = 30
effects = [
  { targetType = "npc", npcId = "npc_marge", trait = "relation", op = "add", value = 5 },
]
flagEffects = [
  { targetType = "player", flag = "hired_at_diner", op = "set" },
]

# Type A — Frank catch capstone
[[canvases]]
id = "scene_livingroom_catch"
name = "The catch"
description = "Frank catches Maya at evening. Stage 1→2 transition. Type A capstone."

[canvases.trigger]
location      = "loc_living_room"
is_repeatable = false
priority      = 10
conditions = { version = "1.0", logic = "AND", items = [
  { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_false" },
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 25 },
] }
[[canvases.trigger.schedules]]
weekdays = [0, 1, 2, 3, 4]
start_time = "19:30"
end_time = "21:00"

[[canvases.nodes]]
id = "catch"
name = "The catch"
blocks = [
  { type = "image", props = { file = "scenes/catch.jpg" } },
  { type = "paragraph", content = "He's there before you hear him." },
  { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Door open. Always. From now on. Where I can see you." },
]

[canvases.nodes.exit_block]
type = "choices"

[[canvases.nodes.exit_block.choices]]
text = "Lower your eyes."
flagEffects = [{ targetType = "player", flag = "frank_caught", op = "set" }]
effects = [
  { targetType = "player", trait = "corruption", op = "add", value = 5 },
  { targetType = "player", trait = "frank_stage", op = "set", value = 2 },
  { targetType = "npc", npcId = "npc_diana", trait = "awareness", op = "add", value = 1 },
]
targetType = "location"
locationId = "loc_living_room"

# ───── Lane 1 hub canvas (Frank kitchen morning) ─────
[[canvases]]
id = "frank_kitchen_morning_hub"
name = "Kitchen — Frank, morning"
description = "Lane 1 hub. Locked-visible escalation ladder."

[canvases.trigger]
location      = "loc_kitchen"
requires_npc  = "npc_frank"
is_repeatable = true
priority      = 8
npc           = "npc_frank"
[[canvases.trigger.schedules]]
weekdays   = [0, 1, 2, 3, 4, 5, 6]
start_time = "05:30"
end_time   = "09:00"

[[canvases.nodes]]
id = "base"
name = "Kitchen — morning"
blocks = [
  { type = "image", props = { file = "scenes/frank_kitchen_morning.jpg" } },
  { type = "paragraph", content = "Frank's at the counter. He looks up when you come in." },
  { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Morning." },
]

[canvases.nodes.exit_block]
type = "choices"

[[canvases.nodes.exit_block.choices]]
text = "Pour him coffee."
targetType = "location"
locationId = "loc_kitchen"
time_progression_minutes = 5
effects = [
  { targetType = "npc", npcId = "npc_frank", trait = "relation", op = "add", value = 1 },
]

[[canvases.nodes.exit_block.choices]]
text = "Tease him ❤️‍🔥"
targetType = "node"
nodeId = "tease_kitchen_general.base"
show_when_locked = true
locked_text_threshold = "Maya's corruption: 5+"
conditions = { version = "1.0", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 5 },
] }

[[canvases.nodes.exit_block.choices]]
text = "Leave."
targetType = "location"
locationId = "loc_hallway"

# (Continue with Lane 2 ambients + Lane 3 dispatchers + remaining capstones + quest cards)

# ───── Quest cards ─────
# Frank F1 capstone-mode card (pre-catch)
[[quest_cards]]
text         = "I'm new under this roof. Frank watches me and pretends he isn't."
ready_text   = "Something's about to give."
tip          = "He's around the house all day. I notice that."
npc_id       = "npc_frank"
ready_canvas = "scene_livingroom_catch"
when = [
  { flag = "frank_caught", op = "is_false" },
]
goals = [
  { trait = "corruption", subject = "player", op = "gte", value = 25, label = "Maya's corruption" },
]

# Marge M1 capstone-mode card (pre-hire)
[[quest_cards]]
text         = "I need work. Diana said Marge runs the only place that hires off the street."
ready_text   = "She's at the register."
tip          = "Walk in. Ask."
npc_id       = "npc_marge"
ready_canvas = "canvas_marge_interview"
when = [
  { flag = "hired_at_diner", op = "is_false" },
]
```

(Full TOML would continue with all remaining canvases per design book §4 lane maps.)

---

## §10 — Anti-patterns to catch (self-audit)

Before delivering the TOML, run this audit.

### §10.1 — Undeclared traits

`grep` every effect + every condition for trait names. Every name MUST appear in `[player.core_traits]` OR the appropriate NPC's `core_traits` block.

```bash
# Mental grep — for each "trait = X" in effects, X is in core_traits
# For each "trait_key = X" in predicates, X is in core_traits
```

Sidebar items hard-fail on undeclared traits (build error). Effects + conditions silently no-op (NO BUILD ERROR — drift accumulates invisibly).

### §10.2 — Field-name mixing

Common mistakes per §6.5. Search for:
- `subject = "player"` paired with `trait` (effect field) → predicate using effect names — silent no-op
- `targetType` paired with `trait_key` (predicate field) → effect using predicate names — silent no-op
- `op = "sub"` → no such op; rewrite as `op = "add"` + negative value
- `trait = "stage"` with `targetType = "npc"` → wrong namespace; stage is `<slug>_stage` on player

### §10.3 — Capstone trigger fingerprint (D57-R1)

For every priority ≥ 9 + `is_repeatable = false` (or `is_repeatable = true` + flag-gate) canvas:
- Must have flag-setter effect on at least one exit choice
- Must have `flag_is_false` self-gate in conditions
- Must be referenced by some quest card's `ready_canvas` (per D50-R1) OR have `# off-panel:` comment

### §10.4 — Lane 4 capstone is referenced by quest card

Run mental grep: for every capstone canvas (priority ≥ 9), is there a quest card with `ready_canvas = "<that canvas id>"`?

If not, add the card OR add `# off-panel:` comment. Otherwise the capstone is unreachable from the player's quest panel.

### §10.5 — Quest card chain continuity (D50-R4)

For every quest card with a flag in its `when` clause: is there ANOTHER quest card that points at the canvas that sets that flag (via `ready_canvas`)?

If not, the flag is unreachable from a card pointer — chain is broken.

### §10.6 — Terminal placement (D50-R3)

For every `terminal = true` card: is its `when` flag the LAST flag in the NPC's chain? Any other card with `when` requiring a flag set AFTER terminal's flag is a violation.

### §10.7 — Pure-mechanic card has `# unlocks:` comment (D50-R5)

For every quest card with `goals` but no `ready_canvas`: is there a `# unlocks: <slug>` comment naming what content opens at threshold?

If not, the card may point at vapor — threshold crosses, nothing changes.

### §10.8 — Goal labels name the trait (LO preference, 2026-05-30 — supersedes D50-R6 for this lineage)

Every `goals[i].label` names the underlying TRAIT plainly so the player can connect a quest goal to the stat they see elsewhere: `"Corruption"` for the corruption trait; `"<NPC> Relation"` (e.g. `"Cole Relation"`) for a per-NPC relation goal. Keep the same word on the sidebar (e.g. the corruption `trait_words` item labeled `"Corruption"`, not `"Status"`).

This REVERSES the original Doc 50 R6 "Maya-voice label" rule ("Maya's loosening" / "Cole's attention" / "Rosa trust"). LO found the euphemisms confusing — players couldn't map them to any visible stat. Use trait-name labels by default; only use a Maya-voice label if LO asks for it on a specific game. (`doctrine/05` annotates R6 as LO-overridable.)

### §10.9 — Lane 3 substitution target has `substitution_only = true` + `max_triggers_per_day = 1`

Per D67-R7. Without `substitution_only`, the target appears as a clickable surface in portrait grids. Without `max_triggers_per_day = 1`, same scene can fire multiple times per day — breaks the once-per-day cadence.

### §10.10 — Sidebar items don't surface stage / antagonist awareness

Grep `[[sidebar_items]]` for any item with `trait = "<slug>_stage"` or `trait = "awareness"` (on antagonist NPC). Both are violations.

### §10.11 — Contraception language when bareback default applies (Doc 30 §7.3.1)

**Applies when:** `scope_mode: slice` OR `scope_mode: full_game` with `Phase 2+ inclusions: pregnancy = defer`.

Grep all scene-body prose for: `condom`, `pull out`, `birth control`, `pill`, `careful`, `pregnant` (in pre-Phase-2 contexts).

All family/ambient sex scenes ship BAREBACK with no contraception language. Phase 2+ pregnancy retrofit (whether shipped in this game or deferred) will add parallel pregnant variants; contraception language BLOCKS retrofit.

**Exception — when this rule INVERTS:** at `scope_mode: full_game` with `Phase 2+ inclusions: pregnancy = include`, contraception language is ALLOWED in pre-pregnancy phase scenes (gates the pregnancy mechanic — without "careful" framing the pregnancy beat lands without setup). Pregnancy-variant scenes ship bareback with breeding talk per `doctrine/08_kink_vocab_ceilings.md` Tier 5+. In this mode, contraception language in post-pregnancy scenes still BANNED (breaks immersion).

### §10.12 — Legacy vocabulary

Grep for `Jack's World`, `New In Town`, `Two Weeks`, `Pattern A` / `B` / ... / `J` (outside Doc 67 dispatcher context), `7-driver`, `archetype`, `whiteboard goals`, `narrative gates`, `income channels`.

Zero hits expected outside of `00_LEGACY_IGNORE.md` (which the TOML doesn't include anyway).

### §10.13 — Canvas attached to an `is_container` location (silent death — `doctrine/10` §3)

For every canvas, check its `trigger.location` is NOT an `is_container = true` location. Container passages emit ONLY child-nav (`v2.py:8800`); attached activities/ambients/capstones/portrait-hubs never fire. Late Shifts symptom: town-trap soft-lock + dead Pam arc, all GREEN. Fix: attach to a NON-container standing hub.

### §10.14 — `requires_npc` location not in that NPC's schedule (silent death — `doctrine/10` §5.1)

For every canvas with `requires_npc = npc_X`: confirm its `trigger.location` is one of `npc_X`'s `[[npcs.schedules]]` entries. Presence is schedule-only + fail-closed (`getNpcLocation`); if X is never scheduled there, the canvas NEVER fires. Late Shifts: Hank's first-contact + 3 kitchen subs at `loc_diner_back` where Hank was never scheduled → entire Stage 2→5 chain dead. Fix: schedule the NPC into the location, OR (for walk-ins) drop `requires_npc` and time-gate the sub's own schedule.

### §10.15 — Portrait hub NPC not schedule-present (silent death — `doctrine/10` §5.2)

For every Lane-1 portrait hub (`npc =` set): confirm that NPC is schedule-present at the hub's location. `renderNpcPortraits` (`v2.py:4295`) has its OWN presence gate independent of `requires_npc` — no portrait renders if the NPC isn't scheduled there, so the hub is unreachable. Late Shifts: Cole's apartment hub was blank until Cole got a `loc_cole_apartment` schedule window.

### §10.16 — Dev-only flag required by a shipping canvas (`doctrine/10` + §12)

A flag set ONLY by a dev canvas must NOT be required (`is_true`) by any shipping (non-dev) canvas. When dev canvases are stripped, the requirer becomes unsatisfiable. Late Shifts: `phase_3_unlocked` (only set by `dev_unlock_phase3`) gated Rosa's locked rungs; removing dev re-broke the flag-chain. Audit dev-flag isolation before stripping phase 6.

### §10.17 — NPC reachable only via a locked location / vanishes into a locked room (silent — `doctrine/10` §5.4)

A locked location (`entry_conditions`) is a *visible-but-blocked* door, but the build won't tell you it makes an NPC unreachable. For every NPC scheduled at a locked location, honor the **unlock contract**: the NPC is met at an OPEN on-ramp whose beat sets the unlock flag (reachable setter), and the NPC has other open presence — never *only* the locked location, and never a door gated on a flag only settable behind it (chicken-and-egg). A locked secondary room an already-met NPC routes into is fine only if it's legible + off-hours/co-gated + has open fallback presence; otherwise the NPC "vanishes" mid-window (`doctrine/02` §8.15). Case A/B/C in `doctrine/10` §5.4.

---

## §11 — Quality gate (self-audit checklist)

Run this BEFORE delivering the TOML.

### TOML structure
- [ ] `[project]` uses `id = "..."` (NOT `slug`) + has `starting_canvas` (§1.2)
- [ ] No multi-line inline tables — every `{ … }` keeps its keys on the opening line and its closing `] }` on one line (tomllib 1.0; §1.3). Run `python -c "import tomllib; tomllib.load(open('<merged>.toml','rb'))"` to confirm a clean parse.

### Trait + flag declarations
- [ ] Every player trait used in any effect/condition/sidebar is declared in `[player.core_traits]`
- [ ] Every NPC trait used is declared in that NPC's `core_traits` block
- [ ] Every `<slug>_stage` trait declared in `[player.core_traits]` (one per arc-having NPC)
- [ ] Every internal trait — every `<slug>_stage`, plus any included Phase-2+ trait (`pregnancy`, antagonist `awareness`) — has a `[[traits.labels]]` entry with `hidden = true`. This is the ENGINE-enforced hide (suppresses the trait from the playerTraits sidebar widget + Stats page in dev AND non-dev). Without it the raw trait name + value leak into both dumps. `[[traits.labels]]` hide entries are keyed by trait NAME only (not namespaced) — a hidden key hides for the player and any NPC carrying a core_trait of that name.
- [ ] Stage advancement effects use `targetType = "player"` + `trait = "<slug>_stage"` (NOT `targetType = "npc"`)

### Field names
- [ ] Effects use `targetType` / `npcId` / `trait` / `flag` / `op`
- [ ] Predicates use `subject` / `npc_id` / `trait_key` / `flag_key` / `operator`
- [ ] No `op = "sub"` anywhere (use `op = "add"` + negative value for decay)
- [ ] Quest card conditions use FLAT shape (`flag` + `op`, NOT `type` + `flag_key`)

### Lane fingerprints
- [ ] Every Lane 1 hub has `is_repeatable = true` + `priority` ~5-10 + `requires_npc` + schedule
- [ ] Every Lane 2 ambient has `trigger_mode = "random"` + `chance` + `max_triggers_per_day = 1`
- [ ] Every Lane 3 dispatcher parent has `[[canvases.trigger.substitutions]]` rule(s)
- [ ] Every Lane 3 substitution target has `substitution_only = true` + `requires_npc` + `max_triggers_per_day = 1`
- [ ] Every Lane 4 capstone has `is_repeatable = false` (or `true` + self-gate) + `priority ≥ 9` + setter-flag exit + flag-is_false gate

### Quest cards
- [ ] Every Lane 4 capstone is referenced by some quest card's `ready_canvas` (OR `# off-panel:` comment on canvas)
- [ ] Every climbing capstone card has `goals` block when `ready_canvas` has trait gates above `when` (D50-R2)
- [ ] Every pure-mechanic card has `# unlocks:` comment naming what crosses (D50-R5)
- [ ] Terminal card is the LAST in NPC chain (D50-R3)
- [ ] Every `goals[i].label` names the trait — "Corruption" / "<NPC> Relation" (LO pref, §10.8; supersedes D50-R6)
- [ ] Every `is_true` flag/quest gate has a REACHABLE setter (setter exists AND can fire); no dev-only flag required by a shipping canvas (§10.16)

### Reachability (`doctrine/10` — the validator does NOT catch these)
- [ ] No canvas's `trigger.location` is an `is_container = true` location (§10.13)
- [ ] Every `requires_npc` canvas: its location ∈ that NPC's `[[npcs.schedules]]` (§10.14)
- [ ] Every portrait hub (`npc =` set): the NPC is schedule-present at the hub location (§10.15)
- [ ] Every NPC ambient/capstone passes the triad (NPC-schedule ∩ window ∩ player-present-and-awake, cross-midnight aware)
- [ ] If `pregnancy = include`: at least one canvas sets `player.pregnancy`; peer/dating NPCs have an ongoing Stage-4 hub (not capstone-only)

### Sidebar
- [ ] Maya state: corruption (banded) + arousal (bar) + energy (status text) + hygiene (status text) all present
- [ ] No `<slug>_stage` sidebar items for ANY NPC
- [ ] No `awareness` sidebar item for antagonist NPCs
- [ ] No per-NPC `trait_bar`/`trait_words` (UNSUPPORTED — §8.4)
- [ ] Body-state surfaces (energy + hygiene visible)

### Voice + content
- [ ] All Lane 1/2/3 prose is RTS-flat (≤30-word caption density; no atmospheric sensory detail; one beat = one click)
- [ ] All Lane 4 capstone prose earns Tier-3 register (per `doctrine/05_rts_flat_prose.md` §3 — specific, layered, character-distinguishing)
- [ ] Contraception language compliance per §10.11 (BANNED when bareback default applies; ALLOWED in pre-pregnancy scenes when `scope_mode: full_game` + `pregnancy = include`; Doc 30 §7.3.1)
- [ ] No legacy vocabulary (Pattern A–J as macros, 7-driver archetypes, whiteboard goals, etc.)
- [ ] Per-NPC vocab ceilings honored (daddy at Frank Tier 4+ when in scope, incest callouts at Jake Tier 3+, etc.)

### Cross-arc + retrofit
- [ ] Pregnancy retrofit-compatible (bareback throughout; no `pregnancy.*` traits authored; Phase 2+ deferred per Doc 65)
- [ ] Diana awareness writes from Frank scenes accumulate correctly (when applicable)
- [ ] Cross-NPC flag dependencies form a valid DAG (no circular dependencies)

### Validator
- [ ] Run `python manage.py package_from_toml --file <path> --owner-id <uuid> --output <path> --dev`
- [ ] Zero validator errors
- [ ] Known warnings only (e.g., pre-existing schedule overlaps that LO has accepted)

If any checklist item fails: rewrite the offending section BEFORE delivery. **Do not deliver TOML you haven't validated locally** — validator failures shipped to LO mean LO becomes the test runner (Doc 54 §7.3 anti-pattern).

---

## §12 — Common mistakes during emission

Consolidated from Doc 54 + slice authoring experience.

### §12.1 — Forgetting to declare a trait

You write `{ targetType = "player", trait = "calculation", op = "add", value = 1 }` in an effect. You forget to add `calculation = 0` to `[player.core_traits]`. The build succeeds. The effect silently no-ops at runtime. The player never accumulates the trait. The downstream content gated on `calculation >= N` never unlocks.

**Detection:** mental grep AFTER emission — for every `trait = "X"` in effects + `trait_key = "X"` in predicates + `trait = "X"` in sidebar items, X is in `core_traits`.

### §12.2 — Field-name slip mid-emission

You start with predicate syntax (`subject = "player"`) and copy-paste while building a similar effect — but the effect needs `targetType = "player"`. Engine silently no-ops the effect. Same drift as §12.1.

**Detection:** for every `subject = X` line, check the context — should be inside `items = [...]` (predicate). For every `targetType = X` line, check context — should be inside `effects = [...]` or `flagEffects`.

### §12.3 — Stage on NPC namespace (wrong)

You write `{ targetType = "npc", npcId = "npc_frank", trait = "stage", op = "set", value = 2 }`. The engine looks for stage on `npcs.frank.core_traits.stage` (doesn't exist). Silent no-op.

**Right:** `{ targetType = "player", trait = "frank_stage", op = "set", value = 2 }`. Stage lives on player namespace as `<slug>_stage` per `doctrine/09_trait_catalog.md` §9.

### §12.4 — Capstone without flag-setter

You write a capstone canvas with `is_repeatable = false` + `priority = 9` + conditions. But the exit choices' `flagEffects` block is empty. The canvas fires once at the gate-cross, then never again because no flag changed — but engine state still treats it as triggerable. Player can re-enter the location and... nothing happens (the canvas's conditions still pass, but the engine's cooldown layer prevents re-fire). Result: silent dead-end.

**Detection:** for every priority-9+ + is_repeatable-false canvas, grep its `exit_block.choices` for `flagEffects`. Must set the chain's setter flag.

### §12.5 — Quest card with no `ready_canvas` AND no `goals`

`txt_only` card (per D56-R6 / D50-R3). Card renders as Frame 4 (frameless narrative text only). Looks broken.

**Right:** every card has either `ready_canvas` (capstone mode) OR `goals` (mechanic mode) OR `terminal = true` (terminal). No fourth state.

### §12.6 — Quest card chain has gaps (D50-R4 violation)

Card B requires `flag_X = is_true` in its `when`. But no card has `ready_canvas` pointing at the canvas that sets `flag_X`. The flag is reachable in the game (some canvas sets it) but the quest panel has no card pointing at that canvas. Player has no narrative thread.

**Detection:** for every card's `when` flag, trace backwards — is there a card with `ready_canvas` pointing at the setter?

### §12.7 — Lane 3 substitution target without `requires_npc`

The target canvas relies on the parent activity's substitution rule conditions for NPC-presence gating, but per D67-R6 the target should have `requires_npc = "npc_<slug>"` for engine-level filtering.

Without it: the substitution rule may fire even when the NPC isn't co-located (e.g., NPC is at school per schedule but substitution evaluates only chance + extra conditions). Result: NPC "appears" in scenes when the world model says they're elsewhere.

### §12.8 — Pregnancy language when bareback default applies (Doc 30 §7.3.1)

**Applies when:** `scope_mode: slice` OR `scope_mode: full_game` with `Phase 2+ inclusions: pregnancy = defer`.

You author a Frank sex scene with the line "He pulls out at the last second." Phase 2+ pregnancy retrofit (whether shipped in this game or deferred) will need pregnant variants of this scene; the "pulls out" language BLOCKS retrofit (pregnant variant should show him cumming inside).

**Right:** family/ambient sex scenes ship BAREBACK with cum-inside framing (no breeding talk pre-Phase-2; full breeding talk Phase 2+ when pregnancy ships per §0.5 inclusions).

**Exception — when this rule INVERTS:** at `scope_mode: full_game` with `pregnancy = include`, pre-pregnancy scenes ship WITH contraception cues + careful framing (gates the upcoming pregnancy beat); post-pregnancy scenes ship BAREBACK with breeding talk per `doctrine/08_kink_vocab_ceilings.md` Tier 5+. The retrofit-block rule still applies to pre-pregnancy scenes: their language must support the pregnant variant retrofit when the pregnancy beat fires.

### §12.9 — Hub menu over-weighting (Doc 54 §3.1)

You ship a hub with 10 menu items. Per D56-R1 + Doc 54 §3.1, hubs cap at ~5 unlocked items + locked-visible escalation ladder.

**Fix:** reduce unlocked items to 1 relational base + 1 talk + 1 Leave. Add the escalation rungs as locked-visible (`show_when_locked = true`).

### §12.10 — Service NPC with Lane 2/3 surfaces (Doc 54 §3.4)

Per `doctrine/03_arc_shapes.md` §6 — service NPCs have empty Lane 2 + Lane 3 in slice. If you've authored 6 Lane 2 ambients for Marge, those surfaces shouldn't exist.

**Fix:** delete them. Empty cells are honest.

### §12.11 — Removing dev canvases re-breaks the flag-chain (Late Shifts 2026-05-29)

Stripping phase 6 (`6_dev_shortcuts.toml`) is NOT just deleting canvases. Dev shortcuts often (a) set `dev_mode_enabled` in the intro one-shot, and (b) are the SOLE setter of flags that shipping canvases require. Before removing them: audit for any `is_true` flag whose only setter is a dev canvas, and clean up its non-dev requirers, or the flag-chain validator fails. Late Shifts: `dev_mode_enabled` setter was orphaned; `phase_3_unlocked` (only set by `dev_unlock_phase3`) gated Rosa's locked rungs → those rungs had to be removed. **Rule: a dev-only flag must never be required by a shipping canvas (§10.16).** Empty phase 6 to a header-only stub — the merge tolerates a canvas-less phase.

### §12.12 — Included Phase-2+ trait with no setter stays dormant

If the design book opts a Phase-2+ trait IN (e.g. `pregnancy = include`), you MUST author a canvas that sets it (e.g. a hidden `event_pregnancy_onset` that sets `player.pregnancy = 1` after an `had_unprotected_sex` flag). The flag-chain validator checks FLAGS, not TRAITS — an included trait with no setter passes the build but the dependent content (revelation scenes, breeding-talk variants) never fires. Late Shifts shipped pregnancy "included" but inert until a setter was wired. (`doctrine/09` + `doctrine/10` §6.)

---

## §12.5 — Phased emission spec (full_game mode)

At `scope_mode: full_game`, Stage 2 emits 7 phase files sequentially — one per response. Each response = one phase file. After phase 6 ships, LO runs the assembly script to produce `7_final_game.toml`. This section is the per-phase content contract.

### §12.5.1 — Phase content boundaries

| Phase | File | Content | Approx size at full_game |
|---|---|---|---|
| 0 | `0_systems_spec.toml` | `[project]` + `[engine.*]` (decay tick, daily tick, time model) + `[[sidebar_items]]` + `[[sidebar_bars]]` + `[[sidebar_groups]]` + any top-level `[settings]` | ~10–30KB |
| 1 | `1_metadata_and_locations.toml` | `[player]` (with `core_traits`) + `[[locations]]` (all locations + entry conditions + meta-locations) + `[[npcs]]` (ALL declarations including `[[npcs.schedules]]` + `[[npcs.core_traits]]` per NPC — these MUST live in this file because TOML scoping requires nested tables under their parent) | ~30–100KB |
| 2 | `2_one_shots.toml` | Intro / onboarding `[[canvases]]` — Day 1 bootstrap canvases, intro one-shots (priority ≥10, `is_repeatable = false`, fire-once flag-gated) | ~10–30KB |
| 3 | `3_activities.toml` | Maya-solo dispatcher `[[canvases]]` — activities at locations (make_tea, read_couch, exercise, etc.) WITH their Lane 3 `[[canvases.trigger.substitutions]]` rules + Pattern C `pre_substitution_effects` if applicable | ~30–60KB |
| 4 | `4_story_arc.toml` | Capstone `[[canvases]]` (Type A/B/C per Doc 57) + stage transition canvases + capstone chain wiring (flag setters + chain-step canvases) + cross-NPC bridge capstones | ~30–80KB |
| 5 | `5_scenes.toml` | Lane 1 hub `[[canvases]]` (NPC portrait hubs + location work surfaces) + Lane 2 ambient cascades + Lane 3 substitution target `[[canvases]]` (the `substitution_only = true` surfaces) + per-NPC voice-flavored scene canvases | ~80–200KB |
| 6 | `6_dev_shortcuts.toml` | Dev `[[canvases]]` — force-advance shortcuts (stage 0→4 jumpers), debug snapshot canvases, capstone-fire shortcuts. Gated by `[[settings]] dev_mode_enabled = true`. Strip before player ship. | ~5–20KB |

**Why NPCs must live in phase 1** (not phase 5 with scenes): `[[npcs.schedules]]` and `[[npcs.core_traits]]` are nested under each `[[npcs]]` block. TOML scoping means the nested tables must appear in the same file as their parent. Splitting npcs across phases would break parsing.

**Why phases 2–6 can scatter** (all `[[canvases]]` top-level arrays): the schema defines `[[canvases]]` as a flat array-of-tables. Concatenating two files each containing `[[canvases]]` blocks produces a valid combined `[[canvases]]` array. Per-canvas nested tables (`[canvases.trigger]`, `[[canvases.trigger.substitutions]]`, `[[canvases.nodes]]`) all stay inside their parent canvas's file.

### §12.5.2 — Emission protocol (one phase per response)

After reading the design book + completing the §0.5 + §0.5.1 setup, emit phases in order:

**First response (phase 0):**

```
# Phase 0/7 — 0_systems_spec.toml
# Save this file as: games/<game_slug>/toml_phases/0_systems_spec.toml

<TOML body for phase 0>

# End of phase 0. Reply "next" to receive phase 1.
```

**Each subsequent response** follows the same pattern with the phase number incremented. After phase 6, emit a final assembly instruction:

```
# Phase 6/7 — 6_dev_shortcuts.toml
# Save this file as: games/<game_slug>/toml_phases/6_dev_shortcuts.toml

<TOML body for phase 6>

# End of phase 6 (final phase).
#
# To assemble the buildable TOML, run:
#
#     python scripts/merge_toml_phases.py games/<game_slug> --validate
#
# This produces games/<game_slug>/toml_phases/7_final_game.toml, then validate
# parses cleanly via tomllib. Build with:
#
#     python manage.py package_from_toml \
#         --file games/<game_slug>/toml_phases/7_final_game.toml \
#         --owner-id <uuid> \
#         --output games/<game_slug>/output \
#         --dev
```

**Do NOT batch multiple phases into one response.** Each phase = one response, separated by LO's "next" (or equivalent confirmation). This keeps each response within token budgets + lets LO catch problems per-phase + matches the §0.5.1 promise of phased output.

**If LO asks for revisions to a previously-shipped phase**, re-emit just that phase with the corrections. The assembly script picks up whatever's in each phase file at merge time.

### §12.5.3 — Cross-phase references (canvas slugs)

Canvases in phases 2–6 may reference NPCs (by slug, e.g., `npc_frank`), locations (by slug, e.g., `loc_kitchen`), and other canvases (by slug in flags / substitution targets). Slugs are resolved to UUIDs at build time by `package_from_toml`. Cross-phase slug references work because the build sees the merged file.

When emitting phases 2–6, treat NPC + location slugs as fixed at phase 1's declarations. Don't introduce a new NPC slug in phase 5 that wasn't declared in phase 1 — the build will fail on the unresolved reference.

### §12.5.4 — Slice scope retains single-TOML emission

At `scope_mode: slice`, Stage 2 stays single-TOML (one response, save as `7_final_game.toml` directly, no merge step needed). Phased emission at slice is unnecessary overhead — 50–100KB fits one response cleanly and slice already conventions toward minimal-volume authoring.

If LO explicitly requests phased emission at slice (for review-by-concern), use the same §12.5.1 phase boundaries — slice-scope phases will just be smaller (~5–15KB each).

---

## §13 — Cross-references

### Sibling stages files

- `stages/01_game_book_prompt.md` — Stage 1 (produces this stage's input)
- `stages/03_image_finder_prompt.md` — image search per canvas (post-TOML)
- `stages/04_game_listing_prompt.md` — back-of-book blurb (post-TOML)

### Schema (PRIMARY references)

- `schema/01_engine_capabilities.md` — engine primitives + line numbers
- `schema/02_toml_schema.md` — per-section field tables + §16 field-name reference card + §17 minimal skeleton
- `schema/03_example_toml.md` — TLS Frank slice canonical excerpts (gold-standard examples per lane)

### Doctrine (consulted during emission)

- `doctrine/02_three_lanes_plus_capstone.md` — Lane mechanism + capstone types A/B/C + F1–F5
- `doctrine/04_authoring_rules.md` — D56-R1...R7 + D50-R1...R6 + D57-R1...R5 + F1...F5 + D67-R1...R7
- `doctrine/05_rts_flat_prose.md` — 8 prose rules + dual register
- `doctrine/07_anti_patterns.md` — anti-pattern catalog
- `doctrine/08_kink_vocab_ceilings.md` — per-NPC vocab register
- `doctrine/09_trait_catalog.md` — trait init requirement + Phase 2+ off-limits

### Source TOML

- `games/the_long_summer_test/toml_phases/7_final_game.toml` — 536KB shipped TLS slice. All `schema/03` examples are verbatim from this file.

---

**End of file.** Deliver the TOML per the §1.2 output shape. Validate locally before delivery. Don't truncate. Next stages: `stages/03_image_finder_prompt.md` (image search) + `stages/04_game_listing_prompt.md` (listing blurb).

═══════════════════════════════════════════════════════════════════════════════

## 25. 03_image_finder_prompt

**Source:** `prompts_v2/stages/03_image_finder_prompt.md`

---

# Stages 03 — Image Finder Prompt (port)

**Status:** LLM-consumed pipeline prompt. Post-TOML media stage.
**Replaces:** `prompts/image_finder_prompt.md` (33KB / 748 lines, 2026-03-21). Technical pipeline preserved verbatim; legacy game references replaced with prompts_v2 doctrine cites + RTS-shape examples.
**Input:** TOML file from Stage 2 (`stages/02_toml_generation_prompt.md`) OR explicit JSON query file.
**Output:** image + video files written to `games/{game}/output/videos/` per canvas image block.

This is a media fetcher, not an authoring prompt. It scrapes images (SFW: search engines) + video clips (NSFW: PornHub GIFs via Tor + Playwright) and writes them to disk for the build pipeline to package.

---

## §0 — How this fits into the prompts_v2 pipeline

Per `doctrine/05_rts_flat_prose.md` §2 Rule 8 — **image-first composition.** The visual asset (image / video) carries the scene; prose is the ≤ 30-word caption. Without media, scenes look incomplete; the placeholder visibility IS the missing-image signal (Rule 8 explicit). This stage closes that loop.

Per `schema/02_toml_schema.md` §7.2 — every canvas authors `[image]` / `[video]` block types with:
```toml
{ type = "image", props = { file = "scenes/<slug>.jpg", description = "<for image search>", search_queries = ["query 1", "query 2"] } }
```

The `description` + `search_queries` fields drive this stage's media fetch. Stage 2 (`stages/02_toml_generation_prompt.md`) emits the `search_queries` per canvas per the design book's per-canvas image notes; this stage takes that input and downloads the actual files.

---

## §1 — Invocation modes

### Mode A — JSON query file

Given a JSON file with explicit queries:

```json
{
  "game": "<game_slug>",
  "output_dir": "games/<game_slug>/output",
  "content_rating": "sfw",
  "queries": [
    {
      "file": "videos/activities/scene_name.jpg",
      "description": "Human-readable description of what the media should depict",
      "search_queries": ["search term 1", "search term 2"],
      "type": "image",
      "canvas": "canvas_id",
      "tier": "base"
    }
  ]
}
```

### Mode B — Direct game name

Given just `"Find missing media for <game_slug>"`. Auto-discover missing media via the game-review API.

**Prerequisites:** Django dev server running on `localhost:8000`. Game must have a final-stage TOML at `games/<game_slug>/toml_phases/<N>_final_game.toml`.

**Step 1:** Call API:
```bash
curl -s http://localhost:8000/api/v1/dev/game-review/load?game=<game_slug>
```

**Step 2:** Extract `missing_media` array from the JSON response. Each entry maps to the query format above.

**Step 3:** Infer tier + content_rating from filename:
```
{name}_t{N}.{ext}  → tier = "t{N}"
{name}_base.{ext}  → tier = "base"
{name}.{ext}        → tier = "base"
```

Content rating from tier:
```
base, t2, t3       → SFW
t4, t5, t6, t7, t8 → NSFW
```

---

## §2 — Tier system

| Tier | Rating | Media Type | Description |
|---|---|---|---|
| base, t2, t3 | SFW | image (.jpg) | Domestic, flirtatious, clothed |
| t4 | Borderline | image (.jpg) OR `.gif`/`.webm` | Kissing, suggestive, partial nudity |
| t5, t6 | NSFW | video (`.webm` / `.mp4` / `.gif`) | Explicit sex scenes |
| t7, t8 | NSFW | video | Graphic / specific acts |

### Format enforcement (HARD RULES)

| Tier | REQUIRED Format | Min File Size | Fallback to JPG? |
|---|---|---|---|
| base, t2, t3 | `.jpg` static image | > 1KB | N/A |
| t4 | `.jpg` OR animated clip | > 1KB | Acceptable |
| t5, t6 | `.webm` / `.mp4` / `.gif` animated | > 50KB | **NEVER** |
| t7, t8 | `.webm` / `.mp4` / `.gif` animated | > 50KB | **NEVER** |

**HARD RULE:** if tier is t5+ and the only available asset is a static JPG thumbnail, report **FAIL** — do NOT save the thumbnail. A 10KB static screenshot is useless as a video placeholder. Real PornHub GIF clips are 100KB–4MB animated `.webm` files lasting 2–10 seconds.

---

## §3 — Query validation (CRITICAL before searching)

Before downloading anything, validate EVERY search_query against the actual narrative in the TOML. Bad queries waste time downloading wrong content.

### Validation procedure

1. Open the TOML at `games/<game_slug>/toml_phases/<N>_final_game.toml`
2. For each missing media item, find its block by matching `file = "<filename>"`
3. Read the 2–3 paragraph/dialog blocks BEFORE and AFTER the media block — this is the narrative context
4. Check each search_query against the §3.1 checklist
5. Output a validation report (§3.4) before proceeding

### §3.1 — Validation checklist

| Check | What to look for | Example problem → fix |
|---|---|---|
| **Wrong action** | Query says one act but narrative describes another | Narrative: "your hand wraps around him" = handjob. Query: "blowjob" → fix to "handjob" |
| **Wrong direction** | "manual"/"hand job" but narrative says HIS hand on HER | Narrative: "his hand finds you" = fingering. Query: "manual stimulation" → fix to "fingering" |
| **Banned words** | Query contains words PornHub ignores (§5.2) | "passionate fuck wall urgent" → "sex wall hallway standing" |
| **Tier mismatch** | t2/t3 (SFW) query uses sexual terms | t3 query: "sexual tension dinner" → "couple dinner eye contact" |
| **Vague terms** | "manual stimulation", "oral" (direction?), "foreplay" | "oral kitchen" → "blowjob kitchen kneeling" or "cunnilingus kitchen" |
| **Missing setting** | Narrative names a location but query omits it | Narrative: "kitchen counter" / Query: "fingering morning" → "kitchen counter fingering morning" |

### §3.2 — Action vocabulary (use these exact terms)

- `fingering` = his hand on/in her (NOT "manual stimulation", "manual", or "hand job")
- `handjob` = her hand on him (one word, NOT "hand job")
- `blowjob` = her mouth on him
- `cunnilingus` = his mouth on her (or "eating out")
- `sex` / `fuck` = penetration (add position: missionary, doggy, riding, standing)

### §3.3 — Per-NPC vocab ceiling alignment (prompts_v2 specific)

Per `doctrine/08_kink_vocab_ceilings.md` — each NPC has a declared vocab ceiling. Cross-check search queries against the NPC's ceiling row:

- **Frank — FULL DADDY:** search queries can include "daddy" / "older man" / "salt and pepper" / "paternal" registers
- **Jake — FULL INCEST CALLOUTS:** queries can include "stepbrother" / "sister" / "incest" / "taboo" framing
- **Diana — FULL CUCKOLD:** queries for brought-in branch include "cuckold" / "wife watches" framings
- **Marge / Cookie (Phase 3+ deferred):** NO sexual queries in slice — ceiling row blank means out-of-scope

If a search query escalates beyond the NPC's ceiling, it shouldn't fire. Cross-check tier × NPC at validation time.

### §3.4 — Validation report

Output before proceeding to download:

```
=== Query Validation Report ===
Checked {N} items against TOML narrative.

⚠️ FLAGGED ({N} items need query fixes):

| # | File | Tier | Current Query | Issue | Fixed Query |
|---|------|------|--------------|-------|-------------|
| 1 | scene_frank_walks_in_shower_t6 | t6 | "manual stimulation kitchen" | Vague + solo trap. Narrative: "his hand makes you forget" = fingering. "fingering" alone returns solo/lesbian | "men fingering girl kitchen counter" |
| 2 | scene_franks_bedroom_climax_t5 | t5 | "blowjob couch night" | Wrong action. Narrative: "your hand wraps around him" = handjob | "couch handjob couple night" |

✅ OK ({N} items — queries match narrative)
```

If there are flagged items, use the FIXED queries (not the original TOML queries) for all subsequent searching. Do NOT search with a query you've identified as wrong.

---

## §4 — SFW Pipeline

### §4.1 — Sources

- DuckDuckGo image search (primary)
- Unsplash, Pexels, Pixabay (direct URL search)

### §4.2 — Search strategy

Use WebSearch. Try each `search_queries` entry in order, with enhancements:

**For activity scenes (2 people — Lane 1 hub / Lane 4 capstone):**
- Always add "couple" or "two people" to the query
- Add "at home" or "domestic" for home-based scenes
- Example: `"casual lunch kitchen"` → `"couple having casual lunch at home kitchen two people"`

**For location scenes (no people — `[[locations]]` entries):**
- Add "interior wide angle" or "room view"
- Add "empty" or "no people" to avoid lifestyle shots
- Example: `"home garage interior"` → `"home garage interior wide angle room view empty"`

**For object/mood shots (0 people — sidebar item icons / location detail):**
- Add "close up" or "detail shot"
- Example: `"morning coffee"` → `"two coffee mugs morning light close up kitchen counter"`

### §4.3 — SFW hard rejection filters

If ANY of these fail, the image scores 0 and is skipped:

**People count filter (CRITICAL):**
- Activity scenes (canvas slug starts with `activity_` OR `scene_`): MUST show exactly 1 or 2 people
- REJECT 3+ people, families, groups, children, crowds
- Images with 0 people acceptable ONLY for object/food close-ups

**Setting filter:**
- Must match the described setting (kitchen, porch, couch, etc.)
- "home kitchen" = HOME, not a restaurant
- Location queries need ROOM shots, not close-ups of objects

**Style filter:**
- REJECT overly staged/kitschy, corporate/commercial, AI-generated
- PREFER natural, candid-looking lifestyle photography

### §4.4 — SFW scoring

- **Relevance** (0–100): matches description and setting?
- **Mood** (0–100): intimate, warm, domestic feel?
- **Composition** (0–100): well-framed, good resolution, usable as game scene?
- **Overall:** average of three scores. Minimum **70** to auto-accept.

### §4.5 — SFW download

- Download with curl or wget to `{output_dir}/{file}`
- Create parent directories with `mkdir -p`
- Verify file exists and is > 1KB

### §4.6 — SFW rules

1. SFW only — skip any NSFW results
2. No watermarks — avoid visible watermarks or stock overlays
3. Realistic style — photographic over illustrations
4. Respect copyright — prefer Unsplash, Pexels, Pixabay, Creative Commons
5. Don't hallucinate URLs — only use URLs found via actual search
6. Rate limiting — 1–2 seconds between searches
7. People count is sacred — 2-person game, 3+ people = ALWAYS wrong
8. Room shots for locations — wide angle showing the space

---

## §5 — NSFW Pipeline

### §5.1 — ⚠️ TWO-PHASE PROCESS (DO NOT SKIP)

The NSFW pipeline has TWO mandatory phases that CANNOT be combined into one automated script:

1. **Search Phase (script):** run Playwright + Tor + PornHub GIF search to harvest thumbnails + video URLs for 10+ candidates per item
2. **Evaluation Phase (visual):** YOU view each thumbnail with the Read tool, score it against §5.4 criteria, pick the highest above 60%

**DO NOT** write a script that auto-selects the first candidate.
**DO NOT** batch-process all items in one script run without evaluating between items.

The script ONLY harvests candidates. YOU evaluate by viewing thumbnails.

**Process items in small groups (3–5 at a time):**
1. Run harvest script for 3–5 items → thumbnails saved to `/tmp/nsfw_previews/{name}/`
2. VIEW all thumbnails for those items → score and pick winners
3. Download winning videos
4. Move to next group

### §5.2 — Prerequisites

**Tor (required for network access to adult sites):**
```bash
brew install tor   # one-time
tor &              # start daemon
# Verify
curl --socks5-hostname 127.0.0.1:9050 https://check.torproject.org/ 2>/dev/null | grep -o "Congratulations"
```

If Tor stuck:
```bash
kill -HUP $(pgrep tor)              # new circuit
kill $(pgrep tor) && sleep 2 && tor &   # full restart
```

**Playwright + Chromium:**
```bash
cd /tmp && npm install playwright
cd /tmp && npx playwright install chromium
```

**ffmpeg (for video verification):**
```bash
brew install ffmpeg
```

### §5.3 — Harvest script (single-page extraction)

Save as `/tmp/nsfw_harvest.js`:

```javascript
// nsfw_harvest.js — FAST HARVEST. Extracts thumbnails + video URLs from search page only.
// Edit the QUERIES array per batch (max 3-5 items per run).

const { chromium } = require('playwright');
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const PREVIEW_DIR = '/tmp/nsfw_previews';

// ============ EDIT THIS FOR EACH BATCH ============
const QUERIES = [
  { name: 'example_scene', search: 'kitchen+counter+sex', desc: 'Sex on kitchen counter' },
];
// ==================================================

async function harvestFromSearchPage(page, search) {
  await page.goto(
    `https://www.pornhub.com/gifs/search?search=${search}`,
    { waitUntil: 'domcontentloaded', timeout: 45000 }
  );

  // Dismiss age gate if present
  try {
    const btn = await page.$('button:has-text("I am 18 or older")');
    if (btn) { await btn.click(); await page.waitForTimeout(3000); }
  } catch (e) {}

  await page.waitForTimeout(8000);

  // Extract ALL data from search results in one shot
  return await page.evaluate(() => {
    const data = [];
    const seen = new Set();
    const gifLinks = document.querySelectorAll('a[href*="/gif/"]');

    for (const a of gifLinks) {
      const m = a.href.match(/\/gif\/(\d+)/);
      if (!m || seen.has(m[1])) continue;
      seen.add(m[1]);

      const gifId = m[1];
      const title = (a.textContent || '').trim().substring(0, 80);
      const parent = a.closest('li, div');
      const video = parent ? parent.querySelector('video') : null;

      let thumbnail = null;
      let videoUrl = null;
      if (video) {
        thumbnail = video.getAttribute('data-poster') || video.poster || null;
        videoUrl = video.getAttribute('data-webm') || video.getAttribute('data-mp4') || null;
        if (thumbnail && thumbnail.startsWith('data:')) thumbnail = null;
      }

      if (thumbnail || videoUrl) {
        data.push({ gifId, title, thumbnail, videoUrl });
      }
      if (data.length >= 15) break;
    }
    return data;
  });
}

(async () => {
  fs.mkdirSync(PREVIEW_DIR, { recursive: true });

  const browser = await chromium.launch({
    headless: true,
    proxy: { server: 'socks5://127.0.0.1:9050' }
  });
  const page = await browser.newPage();

  for (const q of QUERIES) {
    console.log(`\n=== ${q.name}: "${q.desc}" ===`);
    const subdir = path.join(PREVIEW_DIR, q.name);
    if (fs.existsSync(subdir)) fs.rmSync(subdir, { recursive: true });
    fs.mkdirSync(subdir, { recursive: true });

    const results = await harvestFromSearchPage(page, q.search);
    console.log(`Found ${results.length} candidates with thumbnails+video URLs`);

    for (let i = 0; i < results.length; i++) {
      const r = results[i];
      if (!r.thumbnail) continue;

      const thumbPath = path.join(subdir, `${i}_${r.gifId}.jpg`);
      try {
        execSync(
          `curl -s --socks5-hostname 127.0.0.1:9050 -o "${thumbPath}" "${r.thumbnail}" --max-time 10`,
          { timeout: 15000 }
        );
        const size = fs.statSync(thumbPath).size;
        if (size < 500) { fs.unlinkSync(thumbPath); continue; }
      } catch (e) { continue; }

      fs.writeFileSync(
        path.join(subdir, `${i}_${r.gifId}.json`),
        JSON.stringify({ id: r.gifId, title: r.title, videoUrl: r.videoUrl || '', thumbnail: r.thumbnail })
      );

      // Download video immediately (URLs expire in ~4 hours)
      if (r.videoUrl) {
        const videoPath = path.join(subdir, `${i}_${r.gifId}.webm`);
        try {
          execSync(
            `curl -s --socks5-hostname 127.0.0.1:9050 -o "${videoPath}" "${r.videoUrl}" --max-time 30`,
            { timeout: 35000 }
          );
          const vSize = fs.statSync(videoPath).size;
          console.log(`  [${i}] ${r.gifId} "${r.title}" — ✓ ${(vSize/1024).toFixed(0)}KB`);
        } catch (e) {
          console.log(`  [${i}] ${r.gifId} "${r.title}" — ✗ video download failed`);
        }
      } else {
        console.log(`  [${i}] ${r.gifId} "${r.title}" — ✗ no video URL`);
      }
    }

    await page.waitForTimeout(1500);
  }

  await browser.close();
  console.log(`\n=== HARVEST COMPLETE ===`);
  console.log('NEXT STEP: View EVERY thumbnail with the Read tool.');
  console.log('Score each against §5.4 criteria. Pick the highest above 60%.');
  console.log('DO NOT auto-pick. DO NOT skip evaluation.');
})().catch(e => console.error('FATAL:', e.message));
```

Run with `node /tmp/nsfw_harvest.js`.

### §5.4 — NSFW evaluation criteria

**Hard rejection filters (instant score = 0):**
- 3+ people visible (groups, threesomes) → REJECT (unless tier-specific threesome scene)
- Solo only (no couple interaction) → REJECT
- Same-sex couple when scene requires M/F → REJECT (and vice versa for lesbian scenes if applicable)
- BDSM/bondage (ropes, paddles, gags, restraints) when scene doesn't call for it → REJECT
- Interracial when game character description doesn't match → REJECT
- Mature/MILF (visibly 40+) when game character is young → REJECT
- Cosplay/costumes/uniforms when scene is casual/domestic → REJECT

**Scoring (0–100):**

| Criterion | Weight | Check |
|---|---|---|
| Setting match | 30% | Visible environment matches description (kitchen/couch/pool/etc) |
| Action match | 40% | Sexual activity matches (oral/doggy/missionary/counter sex/etc) |
| Appearance match | 20% | Default: matches game character description. POV / anonymous male preferred. |
| Quality | 10% | Resolution, framing, lighting. Watermarks acceptable (placeholders). |

**Minimum score: 60** to accept. If nothing scores above 60 after 10 query variations, report FAIL with the best candidate details.

### §5.5 — Step-by-step NSFW workflow

For each NSFW query:

**Step 1: Build search query**
- Start with first entry in `search_queries`
- Enhance per §5.2 tips below

**Step 1b: Rewrite bad queries**
- Replace "manual stimulation"/"manual" → **"fingering"** (when narrative = HE touches HER)
- Replace "hand job" → **"handjob"** (one word) when narrative = SHE touches HIM
- Replace "oral" (ambiguous) → **"blowjob"** (her→him) or **"cunnilingus"** (him→her)
- Replace "fingering" alone → **"men fingering girl [setting]"** (prevents solo/lesbian results)
- Replace "cunnilingus" alone → **"guy eating out girl [setting]"**
- Remove banned words: passionate, intimate, tender, urgent, forbidden, emotional, seductive
- Apply setting-first formula: `[setting] + [specific act]`

**Step 2: Run harvest script** with the query → thumbnails + video URLs saved to `/tmp/nsfw_previews/{name}/`

**Step 3: Evaluate every thumbnail (MANDATORY)**
- View EACH downloaded thumbnail using the Read tool (you are multimodal)
- For each thumbnail, check hard rejection filters first
- Score survivors per §5.4
- Pick highest scoring above 60%
- If all below 60%, try next query variation (§5.6)
- DO NOT pick based on title alone — PornHub titles are user-generated garbage
- DO NOT write an auto-select script

**Step 4: Use the already-downloaded media**
- Videos downloaded during harvest (URLs expire ~4 hours)
- For `type: "image"` (tier t4 and below): the og:image thumbnail IS the final file. Save as `.jpg`.
- For `type: "video"` (tier t5+): the winning candidate's `.webm` should exist in harvest dir > 50KB

**Step 5: Verify download**
- Check file size: images > 1KB, videos > 50KB
- For t5+: verify NOT a static JPEG — `file <path>` must show WebM/MP4/GIF
- For video files, extract verification frame:
  ```bash
  ffmpeg -y -i {file} -ss 00:00:02 -vframes 1 -q:v 2 /tmp/verify.jpg
  ```
- View `/tmp/verify.jpg` to confirm content matches description

**Step 6: If no match, try next query variation** (§5.6). Up to **10 total variations** before FAIL.

### §5.6 — PornHub search query strategies

**CRITICAL: Setting-first queries**

PornHub search weights first keyword. Setting is the hard constraint:
- ALWAYS put setting word FIRST: `kitchen+blowjob` not `blowjob+kitchen`
- First 3 results are usually trending garbage; good matches at positions 4–10+. Need 10+ candidates.

**CRITICAL: Gender-direction queries for ambiguous actions**

PornHub's "fingering" category is dominated by solo girls + lesbian content. For any action that can be performed solo or same-sex, INCLUDE gender indicators:
- `men+fingering+girl+kitchen` NOT `kitchen+fingering`
- `guy+eating+out+girl+couch` NOT `couch+cunnilingus`

Actions that NEED gender direction:
- `fingering` → add `men` or `guy` + `girl`
- `cunnilingus` / `eating out` → add `guy` + `girl`
- `touching` / `rubbing` → add `man` + `woman` or `couple`
- `masturbation` → NEVER use this for M/F (it's inherently solo)

Actions that DON'T need it (inherently M/F):
- `blowjob`, `handjob` — implies M/F
- `sex`, `fuck`, `missionary`, `doggy`, `riding`, `bent over` — implies couple
- Add `couple` or `amateur` for quality filtering

**Words that WORK on PornHub:**
- Settings: `kitchen`, `couch`, `bathroom`, `pool`, `counter`, `table`, `shower`, `bed`
- Actions: `fuck`, `sex`, `blowjob`, `oral`, `riding`, `doggy`, `missionary`, `handjob`, `bent over`
- Body types: `petite`, `thick`, `curvy`, `slim`, `busty`
- Qualifiers: `amateur`, `homemade`, `pov`, `couple`

**Words that ADD NOISE (avoid):**
- Emotional: `passionate`, `tender`, `urgent`, `loving`, `intimate`, `sensual`
- Story: `morning`, `evening`, `first time`, `secret`, `lazy`
- Vague: `beautiful`, `gorgeous`, `perfect`, `hot`

**Query variation strategies (up to 10):**
1. Original query verbatim
2. SETTING + ACTION: `"kitchen blowjob"`
3. ACTION + SETTING reversed: `"blowjob kitchen"`
4. Add body position: `"bent over counter"`, `"riding on couch"`
5. Add POV: `"pov kitchen sex"`, `"pov blowjob"`
6. Simplify to action: `"missionary"`, `"cowgirl"`
7. Add amateur: `"amateur kitchen sex"`
8. Add body type: `"petite kitchen fuck"`
9. Describe the visual: `"girl on counter legs spread"`, `"girl kneeling kitchen"`
10. Broaden as last resort: drop setting, search just `"counter sex"`

### §5.7 — Error handling

| Error | Cause | Fix |
|---|---|---|
| Connection refused on 9050 | Tor not running | `tor &` and wait 15s |
| Playwright timeout | Tor circuit slow | `kill -HUP $(pgrep tor)` for new circuit |
| Empty search results | Query too specific | Broaden, try next variation |
| og:image returns null | Page structure changed | Try `<img>` tags instead |
| Video source not found | JS lazy-load | Wait + check `data-webm`/`data-mp4` attrs |
| Download 0 bytes | CDN rejected | Add referer: `curl -H "Referer: https://www.pornhub.com/" ...` |
| Download is HTML | Captcha redirect | New Tor circuit |

---

## §6 — Reporting format

For each query, report:

```
[OK]   {file} — downloaded from {source} (score: {score})
[SKIP] {file} — already exists
[FAIL] {file} — no suitable match after {N} query variations
[ERR]  {file} — download failed: {error}
```

Final summary:

```
=== Media Finder Summary ===
Total:      {n}
Downloaded: {n}
Skipped:    {n}  (already existed)
Failed:     {n}  (no match / download error)

Failed items:
  - {file} — suggested retry query: "{query}"
```

---

## §7 — Critical rules

1. **NEVER blind-pick** — ALWAYS preview thumbnails. First PornHub result is trending garbage.
2. **Couple only** — No groups, no solo. Two-person stories.
3. **Up to 10 query variations** before reporting FAIL.
4. **Use `--socks5-hostname`** (not `--socks5`) to route DNS through Tor.
5. **Don't hallucinate URLs** — only use URLs extracted from actual page navigation.
6. **Watermarks acceptable** for NSFW clips — these are placeholder assets.
7. **Rate limit** — 1–2 seconds between PornHub navigations.
8. **Verify every download** — images > 1KB, videos > 50KB. Use ffmpeg frame extraction for video.
9. **Default girl appearance** — matches game character description per `[player]` block.
10. **Always search GIFs** on PornHub — short clips (5–30s webm). Never search full videos.
11. **People count is sacred** — 2-person story. 3+ people = ALWAYS wrong.
12. **Settings matter** — Kitchen must look like a kitchen. Pool must show water.
13. **t5+ MUST be video/gif** — Static JPGs not acceptable for t5+.
14. **No duplicate GIF IDs** — Each game item uses a unique PornHub GIF. Track used IDs; skip previously-used.
15. **Per-NPC ceiling alignment** — cross-check tier × NPC vocab ceiling per `doctrine/08_kink_vocab_ceilings.md` before searching.

---

## §8 — Cross-references

### Sibling stages files

- `stages/01_game_book_prompt.md` — Stage 1 (design book authoring)
- `stages/02_toml_generation_prompt.md` — Stage 2 (TOML emission; provides `description` + `search_queries` per canvas)
- `stages/04_game_listing_prompt.md` — game listing blurb

### Doctrine cited

- `doctrine/05_rts_flat_prose.md` §2 Rule 8 — image-first composition (this stage closes the loop)
- `doctrine/08_kink_vocab_ceilings.md` — per-NPC vocab ceilings (cross-check at validation time)

### Schema cited

- `schema/02_toml_schema.md` §7.2 — image block schema (`{ type = "image", props = { file, description, search_queries } }`)

### Source

- `prompts/image_finder_prompt.md` — legacy port source (technical pipeline preserved verbatim with prompts_v2 framing adjustments)

---

**End of file.** Run media fetch per the §1 invocation modes. Validate queries per §3 before searching. Don't skip the two-phase NSFW process.

═══════════════════════════════════════════════════════════════════════════════

## 26. 04_game_listing_prompt

**Source:** `prompts_v2/stages/04_game_listing_prompt.md`

---

# Stages 04 — Game Listing Prompt (port)

**Status:** LLM-consumed prompt. Post-build listing/marketing stage.
**Replaces:** `prompts/game_listing_prompt.md` (3.7KB / 82 lines, 2026-03-28).
**Input:** the game's TOML metadata (typically `[project]` + `[player]` + `[[npcs]]` + capstone canvases + `[[quest_cards]]` + endings).
**Output:** publish-ready game description (100–150 words) + tags list (comma-separated from master list).

Used when publishing the game to adult distribution sites (Gamcore, F95Zone, itch.io, etc.).

---

## §0 — Context

Per `00_LEGACY_IGNORE.md` §6.3: the game is an RTS-shape sandbox. The listing should sell THAT shape — not legacy framings like "Single-NPC Romance" or "Multi-NPC Parallel Arcs." Per LO's 7 locked decisions (Doc 66 §6), every game generated against `prompts_v2/` is RTS-shape.

The listing is the player's first contact with the game. Sell the tension; mention the mechanic ONCE.

---

## §1 — Input

Paste the game's TOML metadata below. At minimum include:

- `[project]` block (title, description)
- `[player]` block (name, description)
- `[[npcs]]` blocks (names, descriptions, arc_stages)
- Capstone canvas descriptions (per `[[canvases]]` with `is_repeatable = false` + `priority ≥ 9`)
- `[[quest_cards]]` (especially the terminal-card text + any branch-distinguishing text)
- Endings / branch flags from the chain
- Any `[settings]` blocks (rent, clothing, time, etc.)

```toml
[PASTE TOML HERE]
```

---

## §2 — Description rules

Write a game description (**100–150 words**):

- **Hook first** — open with the emotional gut-punch, not a setup paragraph
- **Sell the tension, not the mechanics** — the player should feel the stakes before they understand the systems
- **Write like a back-of-book blurb** — short paragraphs, punchy rhythm, incomplete sentences are fine
- **End with a sharp line** — number of endings, a question, or the core dilemma stated plainly
- **Mention the core mechanic once**, briefly (sandbox / daily life sim / open world)
- **No filler** — every sentence earns its place or gets cut

### §2.1 — Banned phrases

- "explore a world of"
- "immersive experience"
- "embark on a journey"
- "in this game you"
- "delve", "landscape", "robust", "seamless", "innovative", "cutting-edge", "captivating"
- "features include:" followed by a bullet list
- "will you choose X or Y?" as the final line (too generic — be specific to THIS game)

### §2.2 — Tone reference

**Good:**

> Fourteen mornings. Fourteen nights. The wedding doesn't move.

**Good:**

> Frank's house. Frank's rules. Frank's bed eventually.
>
> Your mother knows.

**Bad:**

> Experience an immersive 14-day romantic visual novel with multiple branching paths.

### §2.3 — RTS-shape framing

Per LO §6.1 — every game is RTS-shape. The listing should land the shape implicitly:

- Time pressure (rent / deadline / wedding / etc.)
- Multiple NPCs in parallel (cast the listing names ~3–5 of the most load-bearing NPCs)
- The world-clock (mornings + nights + days passing)
- Implicit choice surface ("Frank's bed eventually" implies the player chose vs. didn't)
- Endings count if branches matter (Pattern F capstones → multiple endings)

Don't say "RTS-shape sandbox" in the listing — that's authoring vocabulary, not marketing copy. Land the shape via the prose.

### §2.4 — Per-arc-shape listing hooks

Pull from the cast's mix:

- **Family/ambient NPC dominant** (Frank-like): paternal authority + house-rules tension + secret-then-open arc
- **Slow-burn family** (Jake-like): proximity + restraint + the line crossing once and never going back
- **Peer/dating** (Ryan-like): first-boyfriend tension + town-eyes + commit-or-walk
- **Service** (Marge-like): workplace bond + matriarch arc + after-hours
- **Antagonist** (Diana-like): the threat in the next room + the confrontation chain pulled toward

Pick the 2–3 most marketable hooks from the cast. Don't try to list all 6 NPCs in a 100-word blurb.

---

## §3 — Tag rules

Select tags from the master list (§5). **Do not invent tags.**

- **Order:** genre first, then content type, then specific acts, then platform, then meta
- **Include all that genuinely apply** — if the game has oral scenes, tag it; if it doesn't, don't
- **Skip aspirational tags** — only tag what's actually in the game
- **Output as comma-separated plain text**, one line

### §3.1 — Tag selection from TOML

Walk the TOML to derive tags:

| Tag category | Source in TOML |
|---|---|
| Genre tags (Adventure / Sandbox / Visual Novel / etc.) | `[project].description` + canvas count + lane mix |
| `Sandbox Games` | RTS-shape default (always include) |
| `Erotic Games`, `Porn Games`, `NSFW Games`, `18+`, `XXX Games`, `Adult` | Always include for RTS-shape sandboxes |
| Body-type tags (Big Tits, Petite, etc.) | `[player].description` |
| Hair-color tags (Blondes, Brunettes, Redheads) | `[player].description` |
| Act tags (Blowjobs, Oral Sex, Anal Sex, etc.) | Grep capstone canvas bodies + Lane 4 cascade prose |
| Family/incest tags (Incest, Cheating, MILF, etc.) | NPC `description` blocks + arc shape mix |
| Setting tags (Visual Novel, Time-Based Games, Sandbox Games) | Engine type + canvas distribution |
| Engine tag (HTML Games, Twine) | Always Twine/SugarCube |
| Platform tags (iOS Porn Games, APK, itchio) | Build target |

### §3.2 — Required tag set for RTS-shape sandboxes

Default for every RTS-shape generated game:
- `Sandbox Games`
- `Adult`
- `Erotic Games`
- `Porn Games`
- `18+`
- `XXX Games`
- `NSFW Games`
- `Female Protagonist` (since Maya is the player POV)
- `HTML Games`
- `Visual Novel`

Add per-game based on TOML content.

---

## §4 — Output format

```
DESCRIPTION:
[Your description here, 100-150 words]

TAGS:
[comma-separated tags from master list]
```

---

## §5 — Master tag list (Gamcore English)

Do not invent tags outside this list.

```
2D, 3D, Adventure, Action Games, Ahegao, Aliens, Alcohol, Anal Sex, Arcade, Asians,
Babysitter, Ball Games, Big Cocks, Big Tits, Blackjack, Blondes, Blowjobs, Boobjob,
Booty Call, Brunettes, Business Management, CG Galleries, Cheating, Chinese, Craps,
Cuckold Games, Cyberpunk, Demons, Dirty Ernie Show, Ejaculation, Elves, Erotic Games,
Fantasy, Femboy Games, Femdom, Fetish, Flash, Footjob, Free Games, Free Strip Games,
French, Fuck Town, Glamour, Group Sex, Halloween, Handjob, Hardcore, Harem,
Heroes, Hentai, High Resolution, Horror, HTML Games, Incest, Interracial Sex,
Japanese, Licking, Logic Games, Love, Masturbation, Medical, Medieval Games, MILF,
Milking, Mobile Games, Monster Sex, Music, Naked Games, Netorare Games, NSFW Games,
Nuns, Numbers, Oral Sex, Overwatch, Paranormal Games, Parodies, Perversion, Physics,
Platform Games, Point and Click, Poker, Police, Porn Games, Pregnant, Puzzles, Quests,
Quickies, Quiz, Real People, Redheads, Robots, Role-Playing Games, Roulette, Rule34,
BDSM, Sandbox Games, Schoolgirls, Sex, Sex Chat, Sex Stories, Sex Toys, Sexy Asses,
Sexy Nurses, Shemale, Shooter, Simulation, Space, Sports, Stars, Strip,
Strategy Games, Teen Sex, Time-Based Games, Transgender, TV and Film, Uncensored,
Vanilla Sex, Video, Virtual Girls, Visual Novel, Zombies,
AI Porn Games, Female Protagonist, Meet and Fuck, 18+, XXX Games, Criminals,
Clothing, Cartoons, Censored, Jokes, Songs, Recommendations, Walkthroughs,
Public Sex, RPG Maker, RenPy, Unity, Tyrano, iOS Porn Games, APK, itchio
```

---

## §6 — Worked example (TLS slice listing)

Input (excerpt): TLS `7_final_game.toml` Frank arc + Marge hire + Diana confrontation.

Output:

```
DESCRIPTION:
Maya rents a room at Frank's house for the summer. Frank's wife Diana sleeps
down the hall. The rent is due Sunday.

Frank watches her. Maya feels it — the way he holds her gaze a beat longer than
he should. The way he stops at her back in the narrow kitchen instead of going by.

Forty days. Five capstone moments. Diana finds out eventually.

A sandbox arc with one big yes and one big no — and a lot of small decisions
between them. Stay through morning, or leave before dawn. Pay the rent in cash,
or in something else.

The house decides which Maya you become.

TAGS:
Sandbox Games, Adult, Erotic Games, Porn Games, 18+, XXX Games, NSFW Games,
Female Protagonist, HTML Games, Visual Novel, Incest, Cheating, MILF, Cuckold Games,
Pregnant, Vanilla Sex, Hardcore, Oral Sex, Blowjobs, Time-Based Games, Sex Stories
```

---

## §7 — Cross-references

### Sibling stages files

- `stages/01_game_book_prompt.md` — Stage 1 design book
- `stages/02_toml_generation_prompt.md` — Stage 2 TOML (provides this stage's input)
- `stages/03_image_finder_prompt.md` — media fetcher

### Source

- `prompts/game_listing_prompt.md` — legacy port source (rules preserved; banned-phrases + tone reference verbatim; tag master list verbatim; RTS-shape framing added)
- Doc 66 §6 — LO's 7 locked decisions (game is RTS-shape)
- `00_LEGACY_IGNORE.md` §3.5 — no "Single-NPC Romance vs Multi-NPC Parallel Arcs" framing

---

**End of file.** Run on a completed game's TOML to produce a publish-ready listing.
