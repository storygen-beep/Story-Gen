# 34 — TLS Engine PRD (Phase E Additions)

> **Status:** Engine-side companion to doc 30 (`30_TLS_Test_Redesign_PRD.md`). Scopes the new engine systems the wider TLS redesign requires beyond what's already shipped in v2.
>
> **Date:** 2026-05-15
> **Type:** Engine PRD — implementation-level spec for new mechanics. Read this for engine work; read doc 30 for content/design intent.
>
> **Dependencies:** Doc 30 (master PRD). v2 generator at `apps/game_generation/twee_comprehensive/generators/v2.py`.

---

## 1. Context

Doc 30 (TLS Test Redesign PRD) lays out the wider game vision (90-day open sandbox, 6 NPCs, cross-arc world state, transparent walkthrough discovery). Most of the architecture leverages existing v2 engine primitives — NPC schedules, Lane 1/2/3, conditional in-canvas branching, wardrobe, money + shop, partial quest journal.

But doc 30 §6.3 + §11 identifies **5 engine systems that don't exist yet** and would need to be built for the wider game:

1. Pregnancy schema + father attribution
2. Scandal/reputation global score
3. Gallery + achievements panel
4. Walkthrough scene-table panel UI
5. Explicit StartQuest/CompleteQuest macros (currently partial)

Plus one cross-cutting capability:

6. Cross-arc completed-scenes tracker (per-NPC scene completion flags readable by other arcs)

This doc scopes each system as a phased engine deliverable. **Phase 1 (slice rewrite) does NOT depend on any of this** — slice ships against current engine. These additions land in Phase 2+.

---

## 2. Goals & Non-goals

### Goals

1. **Each new system is fully spec'd** — schema, helper macros, integration points, TOML authoring contract, test plan.
2. **Backward compatibility preserved** — existing TLS slice canvases keep working without modification when these systems land.
3. **Authoring path clear** — TOML authors know how to use each new system without engine spelunking.
4. **Phased delivery** — systems can be shipped independently; engine work can parallelize across multiple slices.

### Non-goals

- **Slice content rewrite** — see doc 30. This doc is engine-only.
- **UI polish / visual design** — sidebar widget structure spec'd; pixel-level styling is implementation detail.
- **RTS-port engine work** — TLS-only. RTS-direct engine inheritance not required.
- **Migration tooling** — clean break is acceptable; existing save states will not auto-migrate to new schemas.

---

## 3. Engine Capabilities — Current vs Target

| System | Current state | Target state | Phase |
|---|---|---|---|
| NPC schedules | YES (v2.py:2237) | YES — no change | ✓ Already shipped |
| Lane 1/2/3 architecture | YES (v2.py:3408-3826, 9385, 9062-9110, 4226) | YES — no change | ✓ Already shipped |
| Time + day model | YES (24-hour clock, isScheduleActive helper) | YES — no change for Phase 1; possible 6-band migration in Phase 3+ | ✓ Already shipped |
| Player corruption + per-NPC stats | YES (player.core_traits + npc.X.{arousal, corruption, love, trust}) | YES — no change | ✓ Already shipped |
| Wardrobe / outfit system | YES (v2.py:791-1289) | YES — no change | ✓ Already shipped |
| Money + shop + rent | YES (v2.py:824-832, 1314-1401) | YES — no change | ✓ Already shipped |
| Conditional in-canvas branching | YES (v2.py:10605-10886, supports `<<if>>` + linkreplace gates) | YES — no change | ✓ Already shipped |
| Block types (image/video/paragraph/dialog/cascade) | YES (v2.py:12045-12302) | YES — no change | ✓ Already shipped |
| Quest journal | PARTIAL (v2.py:13196-13703 — quest cards + display, no explicit macros) | YES — full StartQuest/CompleteQuest/UpdateObjective | E10a |
| **Pregnancy system** | NO | Schema + macros + birth event + parallel pregnant variants | E10b |
| **Scandal/reputation** | NO (only NPC-scoped diana_awareness) | Global scandal_level (0-100) + cross-arc reads | E10c |
| **Walkthrough panel UI** | NO | Sidebar widget rendering scene table per NPC | E10d |
| **Gallery + achievements** | NO (only "unlocked" indicators in hubs) | Sidebar gallery panel + achievements list + replay-from-gallery | E10e |
| **Cross-arc completed-scenes tracker** | NO (only `visited_choices` per game-state) | Per-NPC `completed_scenes[]` array | E10f |

---

## 4. System Specs

### 4.1 E10a — Quest journal (full StartQuest / CompleteQuest macros)

**Status:** PARTIAL today. Quest cards render in sidebar (v2.py:13196-13703) but no explicit macros for authors. Quest tracking is implicit (tied to canvas activity data).

**Target schema:**
```javascript
$quests = {
  payRentDay7: {
    active: true,
    completed: false,
    dateStarted: "Day 1",
    dateCompleted: null,
    objectives: [
      { id: "earn_400", text: "Earn $400 by Sunday", done: false },
      { id: "pay_diana", text: "Pay Diana on Sunday morning", done: false }
    ]
  },
  // ...
}
```

**TOML authoring contract:**
```toml
[[quests]]
id = "payRentDay7"
name = "Pay rent by Day 7"
auto_start = true                           # starts on game init OR via macro
auto_start_conditions = []                  # optional state gate

  [[quests.objectives]]
  id = "earn_400"
  text = "Earn $400 by Sunday"
  completion_condition = "player.money gte 400"

  [[quests.objectives]]
  id = "pay_diana"
  text = "Pay Diana on Sunday morning"
  completion_condition = "flag rent_paid_week_1 is_true"
```

**Macros:**
```html
<<StartQuest "questId">>           // sets active, dateStarted
<<CompleteQuest "questId">>        // sets completed, dateCompleted
<<UpdateObjective "questId" "objId" true>>   // marks objective done
<<FailQuest "questId">>            // sets completed but failed (for branching outcomes)
```

**Sidebar widget:** Already exists. Extend to display objectives + done/not-done state.

**Helper functions:**
- `setup.startQuest(questId)`
- `setup.completeQuest(questId)`
- `setup.updateObjective(questId, objectiveId, done)`
- `setup.isQuestActive(questId)` → bool
- `setup.isQuestCompleted(questId)` → bool

**Build-time emission:** quest definitions emitted as `setup.questDefinitions = {...}` JSON. Auto-start quests fire on game init.

**Integration points:**
- Sidebar quest card renders objectives
- Canvas conditions can read `quest.X.active` / `quest.X.completed`
- Canvas effects can call `<<StartQuest>>` / `<<CompleteQuest>>` / `<<UpdateObjective>>`

**Test plan:**
- Unit: quest-state schema correctly initialized on game start
- Integration: clicking a canvas with `<<CompleteQuest "X">>` flips quest.X.completed to true; sidebar updates
- Live-play: complete the rent quest end-to-end + verify sidebar reflects state

**Estimated engine effort:** ~6-8 hours.

---

### 4.2 E10b — Pregnancy system

**Status:** NO. Zero pregnancy references in v2 today.

**Target schema:**
```javascript
$player.pregnancy = {
  enabled: true,                  // global toggle (Patreon-gated like RTS, or always on)
  isPregnant: false,
  discovered: false,              // player took pregnancy test
  days: 0,                        // days since conception
  pillDays: 0,                    // remaining birth control days
  father: {
    name: null,                   // "Frank" / "Jake" / "Ryan" / "Marcus" / etc
    discovered: false             // player took DNA test
  }
}

$player.babies = []               // array, populated on each birth
// Each baby = { name: string, gender: "M"|"F", father: { name, discovered }, dateOfBirth: "Day X" }
```

**TOML authoring contract:**

```toml
# Per-canvas: opt into pregnancy risk
[[canvases]]
id = "frank_first_night"
# ... existing fields ...

  [canvases.pregnancy_risk]
  npc_id = "npc_frank"            # who would be the father
  chance = 0.15                   # 15% chance of impregnation per fire
  conditions = { ... }            # optional: only if no pillDays remaining, etc

# Per-canvas: mark as pregnant variant of another scene
[[canvases]]
id = "frank_first_night_pregnant"
parent_canvas_id = "frank_first_night"   # NEW field
fires_when_pregnant = true              # NEW field, alternative to parent
# ... rest of canvas spec ...
```

**Macros:**
```html
<<TryImpregnate "Frank" 0.15>>         // rolls dice; if hit, sets isPregnant + father
<<AdvancePregnancyDay>>                // called from day-rollover hook
<<FinishPregnancy>>                    // ends pregnancy (birth or termination); appends to babies[]
<<TakePill>>                           // adds pillDays
```

**Helper functions:**
- `setup.tryImpregnate(npcSlug, chance)` → bool
- `setup.isPregnant()` → bool
- `setup.getPregnancyStage()` → "early" | "showing" | "later"
- `setup.hasVisibleBelly()` → bool (used for selecting pregnant scene variants)
- `setup.advancePregnancyDay()` → called automatically on day rollover

**Pregnant scene variant selection:**

When canvas selector picks a parent canvas (e.g., `frank_first_night`) and Maya is pregnant + showing, engine auto-substitutes the pregnant variant (`frank_first_night_pregnant`) if defined. Selection precedence: pregnant variant > base canvas (if pregnant + showing).

**Birth event:**

Auto-fires at `pregnancy.days >= 270`. Fires the canvas tagged `is_birth_event = true`. Random gender + 33% stillbirth chance (per RTS doctrine). On stillbirth, can optionally unlock new location/arc (e.g., `clandestineClinic` for artificial-womb regen). On live birth, names baby (textbox input) and appends to `$player.babies`.

**TOML auto-emission:** All scene canvases that involve unprotected sex must declare `[canvases.pregnancy_risk]` block. Build-time validator warns if a canvas's prose mentions sex but no pregnancy_risk declared (linter rule).

**Sidebar widget:** Pregnancy card with belly status + days left + father name (once discovered) + babies roster.

**Test plan:**
- Unit: tryImpregnate dice roll fires at expected rate
- Integration: getting pregnant by Frank in scene X correctly writes father=Frank
- Variant: Maya pregnant + showing + clicking frank_first_night → renders pregnant variant
- Birth: pregnancy.days reaches 270 → birth event fires + baby added to roster
- Live-play: complete a full pregnancy arc end-to-end

**Estimated engine effort:** ~20-30 hours (largest system).

---

### 4.3 E10c — Scandal / reputation system

**Status:** NO global scandal. Only NPC-scoped `diana_awareness` exists.

**Target schema:**
```javascript
$player.scandal_level = 0           // 0-100 global score
$player.scandal_tier = "clean"     // computed: clean (0-25) / whispers (25-50) / gossiped (50-75) / pariah (75+)
```

**Migration:** `diana_awareness` becomes one of several writers to `scandal_level` (alongside outdoor scenes, public sex, town gossip, etc). The Diana confrontation auto-fires from `scandal_level` threshold instead of `diana_awareness` threshold.

**TOML authoring contract:**

```toml
# Per-canvas effect: scandal +N
[[canvases.nodes.exit_block.choices]]
text = "Suck him in the toolshed"
# ... rest of choice ...
effects = [
  { targetType = "player", trait = "scandal_level", op = "add", value = 1 }
]

# Or as a body-block effect:
[[canvases.nodes]]
id = "outdoor_scene_climax"
# ... rest ...
effects_on_render = [
  { targetType = "player", trait = "scandal_level", op = "add", value = 2 }
]
```

**Helper functions:**
- `setup.getScandalTier()` → "clean" | "whispers" | "gossiped" | "pariah"
- `setup.scandal()` → number

**Integration points:**
- Canvas conditions: `scandal_tier eq "pariah"` (gates content unlocks/refusals)
- Sidebar widget: scandal status display
- Town NPC scenes (Pastor refuses, bar regulars approach) gate on tier
- Diana confrontation auto-fires at tier threshold

**Build-time validator:** warn if a canvas describes "outdoor sex" or "public scene" (per scene atom field 5) but no scandal effect declared.

**Test plan:**
- Unit: scandal_tier computes correctly at boundaries (24/25, 49/50, etc)
- Integration: outdoor scene fires → scandal +N → scandal_tier flips → sidebar updates
- Cross-arc: scandal pariah → Pastor scene refuses entry

**Estimated engine effort:** ~6-8 hours.

---

### 4.4 E10d — Walkthrough panel UI

**Status:** NO walkthrough today. Only the existing hint system (per-NPC narrative hints in sidebar).

**Target UI:** Sidebar panel (or full-page modal) listing every NPC + every Location with their scene tables.

**Per-NPC scene table columns:**
| SCENE | REQUIREMENTS (NPC) | REQUIREMENTS (MC) | CHANCE | GUIDE | STATUS |

**Status values:**
- 🔒 Locked — requirements not met
- 🔓 Unlocked — requirements met but not yet completed
- ✅ Completed — player has fired this scene at least once

**Data source:** All canvases with `walkthrough_visible = true` (NEW TOML field) auto-populate the walkthrough table. Engine extracts:
- SCENE: canvas name
- REQUIREMENTS (NPC): trigger conditions on NPC stats (arousal_emoji, corruption)
- REQUIREMENTS (MC): trigger conditions on player stats
- CHANCE: trigger.chance % (or "Click" for menu items)
- GUIDE: NEW TOML field `walkthrough_hint` (concrete prose: "Make tea in the kitchen during morning")
- STATUS: read from `$gallery.completedScenes` (see E10e)

**TOML authoring contract:**

```toml
[[canvases]]
id = "frank_passes_kitchen_door"
walkthrough_visible = true
walkthrough_hint = "Make tea in the kitchen during the morning"
# ... rest ...
```

**Helper functions:**
- `setup.getWalkthroughTable(npcSlug)` → array of scene rows
- `setup.computeSceneStatus(canvasId)` → "🔒" | "🔓" | "✅"

**Sidebar widget:** Walkthrough panel button → opens table view.

**Test plan:**
- Unit: scene status correctly reflects completion + requirements
- Integration: complete a scene → walkthrough flips it to ✅
- Live-play: open walkthrough at Day 1 → see all 130+ scenes locked but visible

**Estimated engine effort:** ~10-12 hours.

---

### 4.5 E10e — Gallery + achievements

**Status:** NO gallery panel. NO achievements. Only "unlocked" hub-level indicators.

**Target schema:**

```javascript
$gallery = {
  completedScenes: {
    "frank_passes_kitchen_door": { firstFiredDay: "Day 5", fireCount: 7 },
    "frank_first_night": { firstFiredDay: "Day 18", fireCount: 1 },
    // ...
  }
}

$achievements = {
  "first_kiss": { unlocked: true, dateUnlocked: "Day 3" },
  "first_blowjob": { unlocked: true, dateUnlocked: "Day 12" },
  "first_pregnancy": { unlocked: false },
  // ...
}
```

**TOML authoring contract:**

```toml
[[achievements]]
id = "first_kiss"
name = "First Kiss"
description = "Kiss any NPC for the first time"
trigger_condition = "any flag *_kissed_first is_true"
reward_text = "Maya remembers her first kiss in this town."

[[achievements]]
id = "frank_arc_complete"
name = "Secret Second Wife"
description = "Complete Frank's arc — sleep over with him while pregnant by him"
trigger_condition = "flag frank_sleepover_done is_true AND pregnancy.father.name eq 'Frank'"
```

**Macros:**
```html
<<UnlockAchievement "first_kiss">>             // explicit unlock
<<ReplayScene "frank_first_night">>            // re-fires the scene from gallery (read-only mode)
```

**Sidebar widget:** Gallery panel (grid of NPC portraits → drill into completed scenes per NPC). Achievements panel (list of locked/unlocked achievements).

**Replay mode:** When a scene is replayed from gallery, no stat effects fire and no flags are written. Pure read-only revisit.

**Helper functions:**
- `setup.markSceneCompleted(canvasId)` → auto-called on scene exit
- `setup.isSceneCompleted(canvasId)` → bool
- `setup.unlockAchievement(achievementId)` → flips to unlocked + writes date
- `setup.checkAchievementConditions()` → called on day rollover, auto-unlocks any newly-met achievements

**Integration points:**
- Every canvas auto-marks itself completed on first exit
- Gallery panel button in sidebar
- Achievements panel button in sidebar
- Walkthrough panel reads `$gallery.completedScenes` for STATUS column

**Test plan:**
- Unit: scene completion correctly written
- Integration: replay from gallery doesn't write stat effects
- Achievement: trigger condition met → auto-unlock fires
- Live-play: complete 5 scenes → gallery shows all 5 → replay one without stat ticks

**Estimated engine effort:** ~10-15 hours.

---

### 4.6 E10f — Cross-arc completed-scenes tracker

**Status:** NO. Only `visited_choices` per game-state.

**Target schema:**

```javascript
$npc.Frank.completed_scenes = ["frank_caught", "frank_first_night", ...]
$npc.Diana.completed_scenes = []
// etc per NPC
```

**Population:** On scene completion, if canvas has `npc_id`, append canvas id to that NPC's completed_scenes array.

**Cross-arc read pattern:**

```toml
# Diana's scene branches on what Frank's already done
[[canvases.nodes.exit_block.choices]]
text = "Confront Frank"
conditions = { logic = "OR", items = [
  { type = "list_contains", subject = "npc.Frank.completed_scenes", value = "frank_caught" },
  { type = "list_contains", subject = "npc.Frank.completed_scenes", value = "frank_first_night" }
]}
```

**Helper functions:**
- `setup.npcSceneCompleted(npcSlug, canvasId)` → bool
- `setup.npcCompletedSceneCount(npcSlug)` → number
- `setup.npcCompletedScenesList(npcSlug)` → array

**Integration points:**
- Auto-population on scene exit (no author work needed)
- Canvas conditions can read via new `list_contains` operator
- Sidebar can optionally display "X scenes completed with Frank"

**Test plan:**
- Unit: completion correctly appends to per-NPC list
- Cross-arc: Diana scene gates on `frank.completed_scenes contains frank_caught` → fires only when that's true

**Estimated engine effort:** ~4-6 hours (mostly TOML schema + condition evaluator extension).

---

## 5. Integration Order + Dependencies

Recommended shipping order (from cheapest/most-foundational to most-complex):

| Order | System | Effort | Depends on | Unblocks |
|---|---|---|---|---|
| 1 | E10f — Cross-arc completed-scenes tracker | ~4-6h | None | Most cross-arc reads in TOML |
| 2 | E10c — Scandal/reputation | ~6-8h | E10f (optional) | Diana confrontation, town gating |
| 3 | E10a — Quest journal full macros | ~6-8h | None | Player-facing drives + sidebar quests |
| 4 | E10d — Walkthrough panel UI | ~10-12h | E10e (for STATUS column) | Player discovery transparency |
| 5 | E10e — Gallery + achievements | ~10-15h | E10f (for completion data) | Replay + long-game motivation |
| 6 | E10b — Pregnancy system | ~20-30h | E10f (for cross-arc reads) | Long-game cross-arc compounding |

**Total engine effort estimate:** ~56-79 hours focused work. Slice (Phase 1) doesn't depend on any of this. Phase 2 ideally lands E10a + E10c + E10f. Phase 3 lands E10d + E10e + E10b.

---

## 6. TOML Schema Migration

Current TOML contains:
- `[[canvases]]` (no change)
- `[canvases.trigger]` (no change; +new fields per E10b for pregnancy_risk)
- `[[canvases.nodes]]` (no change)
- `[canvases.nodes.exit_block.choices]` (no change; new effect types: `scandal_level`, `list_contains` op)
- `[story_arc.hints.templates]` (existing — preserved)

New TOML blocks (Phase 2+):

| New block | Section | Purpose |
|---|---|---|
| `[canvases.pregnancy_risk]` | per-canvas | Marks canvas as pregnancy-eligible (E10b) |
| `[[quests]]` + `[[quests.objectives]]` | top-level | Quest definitions (E10a) |
| `[[achievements]]` | top-level | Achievement definitions (E10e) |

New canvas-level fields:

| Field | Type | Purpose |
|---|---|---|
| `walkthrough_visible` | bool | Show in walkthrough panel (E10d) |
| `walkthrough_hint` | string | GUIDE column prose (E10d) |
| `parent_canvas_id` | string | Mark pregnant variant (E10b) |
| `fires_when_pregnant` | bool | Pregnant variant selector (E10b) |
| `is_birth_event` | bool | Birth auto-fire (E10b) |

**Backward compatibility:** All new fields are optional. Existing TOML keeps working without modification.

---

## 7. Validator Extensions

The build-time validator (`apps/projects/services/template_import.py`) should grow new linter rules to enforce the new schemas:

| Linter rule | Severity | What it catches |
|---|---|---|
| Pregnancy risk on sex scenes | WARN | Canvas describes sex (effects include `arousal +3` AND clothing-removed marker) but no `[canvases.pregnancy_risk]` block declared |
| Scandal effect on outdoor scenes | WARN | Canvas at outdoor location AND has explicit physical effects but no scandal_level effect |
| Walkthrough metadata for hub-routed scenes | WARN | Canvas referenced from hub menu but missing walkthrough_visible + walkthrough_hint |
| Quest objective unreachable | ERROR | Quest objective's completion_condition references a flag that no canvas writes |
| Pregnant variant orphaned | ERROR | Canvas with `parent_canvas_id = "X"` where canvas X doesn't exist |
| Achievement trigger unreachable | ERROR | Achievement trigger_condition references a flag that no canvas writes |

These validator rules prevent the C7b-class structural bug (target unfindable at runtime) for the new systems.

---

## 8. Test Plan (Per System)

For each system (E10a-E10f):

1. **Unit tests** — schema initialization + helper function behavior in isolation. Test in `apps/game_generation/tests.py`.
2. **Build-time tests** — TOML with new schema parses cleanly + emits expected runtime data. Test against fixture TOMLs.
3. **Live-play tests** — focused twine-game-explorer session per system. Verify end-to-end behavior in a built TLS HTML.
4. **Regression** — pytest baseline preserved (262 passed + 5 pre-existing failures).
5. **Performance** — gallery + walkthrough panels can render 200+ scenes without UI lag.

**System-level acceptance:** for each system, a memory file documenting what shipped + verification results, mirroring the Phase D1 pattern.

---

## 9. Risks + Open Questions

### Risks

| Risk | Mitigation |
|---|---|
| Engine work blocks Phase 2 indefinitely | Ship systems independently per §5 order; each unlocks SOME content even before all are done |
| TOML schema migration breaks existing slice | All new fields optional; backward compat preserved |
| Pregnancy system has unexpected interactions with existing flags | Treat E10b as a major version bump; full regression suite + opt-in via `pregnancy.enabled` flag |
| Walkthrough panel becomes information overload at 200+ scenes | Per-NPC drill-down + filter by status (locked/unlocked/completed) |
| Achievement explosion (200+ achievements) confuses players | Curate to ~30-50 high-signal achievements; avoid per-scene achievement spam |

### Open questions to answer before E10 work starts

1. **Pregnancy gating** — should the pregnancy system be opt-in (Patreon-style toggle like RTS) or always-on?
2. **Birth outcome distribution** — RTS uses 33% stillbirth → unlocks clandestine clinic. TLS analog?
3. **Scandal tier names** — proposed "clean / whispers / gossiped / pariah" — better names?
4. **Walkthrough panel placement** — sidebar slot OR dedicated full-page modal?
5. **Gallery layout** — RTS-style grid by NPC OR chronological by completion date?
6. **Quest auto-start vs manual-start** — should quests like "Pay rent" auto-start on day 1, or fire from a kickoff canvas?
7. **Cross-arc completed-scenes — store full canvas IDs or category labels?** RTS stores per-scene flags. Recommend full IDs for granularity.
8. **Achievement trigger evaluator scope** — should achievement conditions support full canvas condition syntax (`AND`/`OR`/nested)?

### Out of scope (deferred)

- **6-band time migration** — covered separately if needed, after Phase 1 ships.
- **Save migration tooling** — clean break is acceptable.
- **NPC AI / scheduling beyond fixed schedules** — out of scope.
- **Multiplayer / save sharing** — out of scope.

---

## 10. How this PRD relates to existing docs

This PRD is the **engine-side companion to doc 30**. Splits responsibility cleanly:

- **Doc 30** (`30_TLS_Test_Redesign_PRD.md`) — content + design intent, scene authoring rules, phased content delivery
- **Doc 34 (this doc)** — engine systems, schemas, helper macros, validator rules, integration tests

Existing engine PRDs in this folder are all archived:

- `archive_03_Engine_Changes_PRD_2026-05-05.md` — superseded; covered F9-F12
- `archive_08_Engine_PRD_Phase2_Additions_2026-05-05.md` — superseded; covered Scene 8 / NPC thought bubbles
- `archive_12_Engine_PRD_09_Hint_System_Completeness_2026-05-05.md` — superseded; hint system rollback
- `archive_14_Engine_PRD_Sandbox_Additions_2026-05-05.md` — superseded; F13-F15 sandbox feature set

Active engine PRDs:

- `25_Lane_3_Dispatcher_Substitution_PRD.md` — Lane 3 substitution mechanism (shipped Phase D1)
- **`34_TLS_Engine_PRD_Phase_E_Additions.md` (this doc)** — pregnancy + scandal + gallery + walkthrough + StartQuest + cross-arc tracker

Engine work outside Phase E additions remains routed through ad-hoc PRDs as needed.

---

## 11. Stop Point

Engine work delivered per §5 ordering. After E10b (pregnancy) lands, doc 34 work is complete. Updates to engine direction go HERE, not in scattered memory files.

---

**End of Engine PRD.**
