# TLS Rewrite Spec — Master Document

> **Created 2026-04-28.** Supersedes `archive_02_Hub_Event_Architecture_superseded_2026-04-28.md`.
> Sibling to `00_TLS_Phase2_Diagnosis_and_Direction.md`.
>
> **Mandate:** complete rewrite of TLS Phase 1 from scratch, mapped onto the verified Road-to-Success design pattern. The locked design book stays canon. The engine stays. The Prologue stays. Everything else gets rebuilt.

---

## §0 Frame

### What this doc is

The master spec for rewriting TLS. It defines the object types, the location/NPC/schedule model, the per-NPC arc-progression contracts, the economic loop, and a vertical-slice build order. Per-canvas prose and per-canvas flag effects are NOT in this doc — those are the build-phase deliverables that ride on top of this spec.

### Why a complete rewrite

Three reasons (full diagnostic in `00_`):

1. **Granularity is not patchable.** The current 79 story canvases are sized like book chapters (400–1500 words, linear "Continue" sub-nodes). The verified working pattern from RtS is hub-with-buttons (50–350 chars) + linkreplace-cascade events (1–3 sentences per beat). Closing the granularity gap means rewriting every canvas — so building from scratch costs no more than patching, with much lower drift risk.

2. **The inventory ratio is upside-down.** Today: 79 story canvases carry the weight, 139 activities are skeletal stat-vending machines. RtS: small story-canvas count, dense hub/event/activity inventory carrying the loop. To flip the ratio, story canvases mostly disappear, hubs are added (don't currently exist as a concept), and activities multiply. That's not 79 edits; it's an inventory transformation.

3. **22 sessions of `content_rewrite/` produced more polished prose at the same wrong granularity.** A 23rd session at the same target produces the same outcome. The bottleneck is the design unit, not the prose quality.

### What stays canon

| Survives | Status |
|---|---|
| Engine (F1–F4, all block types, schedule schema, trait decay) | ✅ No engine work for the rewrite. |
| `Game_Redesign.md` + `final_book.md` (1,460 + 3,900 lines of locked design) | ✅ The spec the rewrite implements against. |
| `2b_systems_budget.md` (5 whiteboard goals, 7 income channels, 40 hints, NPC trait baselines) | ✅ Raw material for the rewrite. |
| The 38 locations in `1_metadata_and_locations.toml` | ✅ Right list, just need hub canvases attached. |
| The 10 player traits + sub-reputations in `0_systems_spec.toml` | ✅ Stay as-is. |
| The Prologue (1 canvas × 9 nodes, ~8,500 words of literary prose) | ✅ The one Tier-A literary canvas. Survives intact. |
| Style sheets in `content_rewrite/style_sheets/` (Maya, Frank, Ryan, Jake, Diana, Marge, Cookie) | ✅ Voice guidance for new authoring. |

### What gets archived

| Archived | Disposition |
|---|---|
| The 79 non-Prologue story canvases | Kept on disk as reference. Prose mined where useful. Not edited going forward. |
| The 139 activity canvases | Same. Some prose may be salvaged at micro-scale; structure is replaced. |
| The 22 sessions of `content_rewrite/` work | Reference. `priority_queue.yaml`, `session_log.md`, `qa_rubric.md` become historical artifacts. The 27 standards remain useful as voice guidance. |
| The α/β/γ disposition framework from old doc 02 | Obsolete. There's no "translation" if we're building from scratch. |

### How to read this doc

§1 — what we verified from live RtS exploration.
§2 — the five object types (the architecture).
§3 — the location → hub map.
§4 — the NPC schedule model.
§5 — the state-pump button roster.
§6 — the per-NPC arc-progression contracts.
§7 — the economic loop.
§8 — the vertical slice (Day 1–3 build, the proof-of-pattern).
§9 — build order across the full rewrite.

---

## §1 What we verified (RtS live exploration)

Verbatim findings from the 2026-04-28 live recon. Each cited where the pattern surfaced.

**1. Hub passages are 50–350 chars, no atmospheric prose.** RtS `Bedroom`: title + image + 6 emoji-buttons. RtS `Kitchen`: title + image + 4 emoji-buttons. RtS `Hallway`: title + image grid of 9 destinations. **No paragraph of "the kitchen at 6:30 AM smells of coffee" anywhere.** The room's identity is the menu.

**2. Buttons gate inline on `<<if>>`.** Verified at RtS `Bedroom` source: time-gated `<<if $game.time == "LN">><<button '❌ Too late to study ❌'>>`, item-gated `<<if isPurchased("phone")>><<button "Masturbate 🍆">>`, corruption-gated `<<if getCorruptionLevel() >= 3>>`.

**3. Two hub archetypes.**
- **Type A — Shared room.** Solo buttons always. NPC presence at this location → maybe a tail-block random encounter. Verified: `Kitchen` (Stepfather there per schedule, zero interaction in passage). `Bathroom` (Brother there, zero interaction). `LivingRoom` (Grandpa there, one optional encounter at the tail).
- **Type B — NPC personal room.** Whole menu splits on NPC presence. Verified: `BrotherBedroom`, `DadBedroom`, `GrandpaBedroom`. If NPC here → interaction menu. If NPC not here → "He's not here" + back-button. **No solo activities in NPC personal rooms.**

**4. NPC interactions canonically live in NPC's personal space.** Stepfather is in the Kitchen → Kitchen has zero Stepfather interaction. Brother is in the Bathroom → Bathroom has zero Brother interaction. Interaction with an NPC happens when you go to THEIR bedroom AND they are there.

**5. Three button types at any NPC-bearing hub.**
- **State-pump button.** Click → toast notification → `npc.X.relation +1`, `npc.X.talkedToday = true` → stay on same passage. Verified: clicked "Talk with Grandpa" → no transition, only state diff `npc.Grandpa.relation: 0→1, npc.Grandpa.talkedToday: false→true`. Second click same day → silent no-op (cooldown).
- **Scene-trigger button.** Click → `<<goto>>` to a scene passage → linkreplace cascade → Return. If gate fails, toast notification ("I'm not aroused enough"), stay on hub. Verified: clicked "Seduce Grandpa" at corruption 0 → no diff, no transition, toast.
- **Conditionally-rendered button.** Wrapped in `<<if>>`; only exists when precondition true. Verified: `<<if isBoyfriend("Marcus")>><<button "Have sex with Marcus 🔥">>` in `MarcusBedroom`.

**6. Schedule is a single `.location` field per NPC.** Verified: `npc.Dad.location = "Kitchen"`, `npc.Brother.location = "Bathroom"`, `npc.Grandpa.location = "Bedroom"`, `npc.Marcus.location = "School"`. The function `GetNpcLocation("X")` literally returns `game().npc.X.location`. A scheduler ticks the field at time-band transitions.

**7. Time is 6 bands × 7 days.** Verified from `%%cycles`: `time` cycle has phases `["EM", "M", "A", "E", "N", "LN"]` with `period: 2` (each band lasts 2 ticks). `day` cycle has 7 phases Monday-Sunday. So a compressed 12-hour day. NPC `.location` field gets re-set when the time band changes.

**8. Right sidebar always shows NPC roster + current location.** DOM-verified. Panel content:
```
🏠 House
🧓🏻 Stepfather    🔥 Arousal ❄️    🫦 Corruption 0    📍 Location Kitchen
🧑🏻 Stepbrother   🔥 Arousal ❄️    🫦 Corruption 0    📍 Location Bathroom
🧓🏻 Stepgrandfather 🔥 Arousal ❄️ 🫦 Corruption 0    📍 Location Bedroom
```
The schedule is **made visible** to the player. This is the planning tool — "Stepfather is in the Kitchen, no point going to his bedroom now."

**9. Player state always in left sidebar.** Outfit (avatar image + clothing meta), Corruption (band label + numeric points), Energy & Arousal (with bars), Money, Stats (Exhibitionism / Intelligence / Social / Fitness / Beauty). The player NEVER reads prose to know their state.

**10. Walkthrough panel in chrome explicitly tells the player gating rules.** Verbatim from RtS Walkthrough probe: *"Once you reach 5 corruption points, you unlock the option to flash your Stepbrother through his bedroom, gaining 1 exhibitionism point."* The gates ARE the gameplay — they're surfaced, not hidden.

**11. Scene density is 1–3 sentences per beat across all tiers.**
- **Tier 1 (Tease, Flash):** Title + 1-sentence narrative + random image + state updates + Return. Whole passage ~20 words. Verified at `BrotherBedroomTease`.
- **Tier 2 (multi-beat scene):** Single passage with `<<linkreplace>>` cascade. Each beat = 1–3 sentences + image/video + 2–3 `<<Speech>>` lines. Verified at `StudyWithMarcus`, `BrotherBedroomSex1`, `MarcusParkDate`.
- **Tier 3 (big setpiece):** Same linkreplace pattern, longer cascade (8–15 beats). Each beat still 1–3 sentences max. Verified at `BrotherShowerSex`, `MarcusParkSex`.

**12. Dialogue is a first-class macro, not narration.** `<<Speech Marcus "...">>` renders styled "Marcus: ..." dialogue. `<<Think Player "...">>` for internal thought. Stage direction lives in `<h3>` lines that are 1–3 sentences. **No interior monologue paragraphs.**

**13. Quest-progress gates reveal more content on later visits.** Same passage, multiple visits. `<<if getQuestProgress("StudyWithMarcus") > 2>>` reveals a deeper section of the linkreplace cascade. First visit shows 3 beats; third visit shows 12 beats — same passage. Verified at `StudyWithMarcus`.

**14. Per-NPC corruption is a separate axis.** `npc.Brother.corruption` is distinct from `player.corruption`. The macro `<<AddBrotherCorruption>>` increments only the NPC's corruption. Two-axis gates: Maya needs corruption ≥ N to UNLOCK the option, AND the NPC needs corruption ≥ M for them to RECEIVE the action.

**15. Engine vocabulary for events:** `<<AddTime '1'>>`, `<<AddArousal>>`, `<<AddExb>>`, `<<AddBrotherCorruption>>`, `<<UnlockNPCScene Brother BrotherBedroomTease>>`, `<<MakeBoyfriend Marcus>>`, `<<NotifyCorruption N>>`, `<<Energy -15>>`, `<<GetNaked>>`, `<<FinishQuest MarcusDate>>`. Every interaction is built from this list.

---

## §2 The five object types

Each object type maps cleanly onto existing TLS TOML primitives. No engine change.

### 2.1 Hub canvas

**What it is.** A canvas at a location that always renders when the player navigates to that location. Contains a button menu. Possibly a one-line NPC-presence note. **No atmospheric prose paragraphs.**

**TOML skeleton:**
```toml
[[canvases]]
id = "hub_kitchen"
name = "Kitchen"

[canvases.trigger]
location = "loc_kitchen"
is_repeatable = true
priority = 1                  # Hub priority. Events route here when their gates miss.
is_active = true
conditions = { version = "1.0", items = [
  { type = "flag", subject = "player", flag_key = "arrived_at_franks", operator = "is_true" }
] }

[[canvases.nodes]]
id = "base"
blocks = [
  { type = "image", props = { file = "hubs/kitchen.jpg", description = "...", search_queries = [...] } },
  # Optional: ONE-LINE NPC-presence text via group block
  # (only if the room has scheduled NPC visitors that the player needs to know about)
]

# Each menu option is its own group-variant wrapping a choice.
# Engine constraint: choices array can't have per-choice conditions; group-wrap each.
exit_block = { type = "choices", choices = [
  { text = "Cook 🍳", targetType = "specific", canvasId = "activity_cook_solo", time_progression_minutes = 60 },
  { text = "Eat from the fridge 🍽️", targetType = "specific", canvasId = "activity_eat_fridge", time_progression_minutes = 10 },
  { text = "Wash dishes 🫧", targetType = "specific", canvasId = "activity_wash_dishes", time_progression_minutes = 20 },
  { text = "Hallway 🚪", targetType = "location", locationId = "loc_hallway", time_progression_minutes = 1 }
] }
```

**Rule:** total visible buttons ≤6. Total options across all states up to 12-15 (some only visible after stat thresholds — surfaced via separate priority-gated canvases that pre-empt the hub when their conditions match).

**Three sub-types:**

| Sub-type | Pattern | TLS examples |
|---|---|---|
| **Hub-A — Shared room** | Solo buttons always. NPC presence informational, surfaced via separate priority canvases. | `hub_kitchen`, `hub_living_room`, `hub_dining_room`, `hub_bathroom`, `hub_porch` |
| **Hub-B — NPC personal space** | Menu splits on NPC presence. NPC here → interaction buttons. NPC not here → "Frank's not here" + back. No solo activities. | `hub_franks_office`, `hub_franks_bedroom`, `hub_jakes_bedroom` |
| **Hub-C — Outdoor / city** | Solo / navigation buttons. Time-gated open/closed for sub-locations. | `hub_main_street`, `hub_creek`, `hub_yard`, `hub_property` |

### 2.2 State-pump button

**What it is.** A button on a hub canvas that fires effects and stays on the same canvas. No new passage. Toast notification gives the player feedback.

**TOML skeleton:** lives as a CHOICE entry on a hub canvas's exit_block, but uses `targetType = "trigger"` (re-fires the current canvas), with effects + a notification flag.

```toml
# Inside hub_franks_office.exit_block.choices:
{
  text = "Talk with Frank 💬",
  targetType = "trigger",          # Re-fire the same canvas → menu re-renders
  time_progression_minutes = 30,
  effects = [
    { targetType = "npc", npcId = "npc_frank", trait = "trust", op = "add", value = 1 }
  ],
  flagEffects = [
    { targetType = "player", flag = "talked_to_frank_today" }
  ],
  conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "talked_to_frank_today", operator = "is_false" }
  ] }
}
```

**Note on conditions on choices:** the engine has no per-choice condition; we use the group-wrap workaround (each state-pump button wrapped in a `group`-variant that renders the choice or nothing).

**Daily reset:** `talked_to_*_today` flags get cleared on the Sleep activity. (One-line addition to the existing sleep activity.)

**Roster of state-pump buttons** detailed in §5.

### 2.3 Event canvas (one-shot)

**What it is.** A scene that fires once, gated by flags or first-entry-after-X conditions. Linkreplace cascade reveals beats in-place. Each beat 1–3 sentences + image/video + dialogue. Sets a completion flag on exit. Routes back to a hub.

**TOML skeleton:**
```toml
[[canvases]]
id = "event_first_morning_kitchen"
name = "First Morning"

[canvases.trigger]
location = "loc_kitchen"
is_repeatable = false
priority = 10                 # High — pre-empts hub_kitchen
is_active = true
conditions = { version = "1.0", items = [
  { type = "flag", subject = "player", flag_key = "arrived_at_franks", operator = "is_true" },
  { type = "flag", subject = "player", flag_key = "first_morning_kitchen_done", operator = "is_false" }
] }
[[canvases.trigger.schedules]]
weekdays = [6]                # Sunday only
start_time = "06:30"
end_time = "08:30"

[[canvases.nodes]]
id = "base"
blocks = [
  { type = "image", props = { file = "events/first_morning_kitchen.jpg", ... } },
  { type = "paragraph", content = "She came down the fourteen stairs in yesterday's clothes." },
  { type = "dialog", content = "Sit.", props = { speaker = "npc", npcId = "npc_diana" } },
  { type = "paragraph", content = "Frank folded the paper." },
  { type = "dialog", content = "Maya. Rent's sixty a week, due Sundays.", props = { speaker = "npc", npcId = "npc_frank" } },
  { type = "dialog", content = "Church is at ten. You can come. You can not.", props = { speaker = "npc", npcId = "npc_frank" } }
]
exit_block = { type = "choices", choices = [
  { text = "I'll come.", targetType = "trigger", time_progression_minutes = 30,
    effects = [{ targetType = "player", trait = "rep_church", op = "add", value = 2 }],
    flagEffects = [
      { targetType = "player", flag = "first_morning_kitchen_done" },
      { targetType = "player", flag = "rent_terms_set" },
      { targetType = "player", flag = "attended_church_week_1" }
    ] },
  { text = "I'll stay.", targetType = "trigger", time_progression_minutes = 30,
    flagEffects = [
      { targetType = "player", flag = "first_morning_kitchen_done" },
      { targetType = "player", flag = "rent_terms_set" }
    ] }
] }
```

**Density target:** 80–250 words total body. Two real choices on exit. No "Continue" buttons.

### 2.4 Activity canvas (repeatable)

**What it is.** A repeatable solo or NPC-paired action at a location. Tier-1 density (verified RtS pattern): 1-sentence narrative + image + state effects + Return.

**Anti-staleness mechanism — RtS pattern, no prose-pool rotation.** Verified at RtS `BrotherBedroomTease`: ONE fixed sentence of prose + 5 random images selected via `<<set $game.randomMedia to either(...)>>`. The PROSE stays fixed across visits; the IMAGE rotates. This is the only verified-RtS rotation pattern for repeatable activities. We follow it.

Variety across visits comes from three mechanisms:
1. **Image rotation** — image block authors 3–5 search_queries; engine selects one at random per render.
2. **Arc-state group variants** — when NPC-arc state changes (e.g., Frank's `frank_restrict_declared` flag flips), the activity's body paragraph swaps to a different fixed paragraph for that state. NOT random rotation; deterministic state-driven swap.
3. **Rare-event sibling canvases** — separate canvases at the same location with `trigger.chance = 0.X` that occasionally pre-empt the standard activity (e.g., 1-in-10 mornings Frank says something arc-relevant during breakfast).

**TOML skeleton (Tier-1 solo, fixed prose + image rotation):**
```toml
[[canvases]]
id = "activity_sketch_bedroom"
name = "Sketch (bedroom)"

[canvases.trigger]
location = "loc_mayas_bedroom"
is_repeatable = true
priority = 2
is_active = true
max_triggers_per_day = 3

[[canvases.nodes]]
id = "base"
blocks = [
  { type = "image", props = { file = "activities/sketch_bedroom.jpg", description = "...", search_queries = [
    "young woman sketching at small bedroom desk afternoon light",
    "girl drawing in sketchbook on bed sunny window",
    "artist's hand close-up pencil over open sketchbook pages",
    "teenage girl bedroom sketchbook quiet afternoon Southern home",
    "young woman lost in sketching small desk warm yellow lamp"
  ] } },
  { type = "paragraph", content = "She sketched the water mark on the ceiling. The comma. The fan ran on. The line on the page held." }
]
exit_block = { type = "location", text = "Close the sketchbook.", config = {
  destinationType = "trigger",
  time_progression_minutes = 60,
  effects = [
    { targetType = "player", trait = "energy", op = "add", value = -10 },
    { targetType = "player", trait = "calculation", op = "add", value = 1 }
  ]
} }
```

**Density target:** ONE FIXED paragraph per arc-state, 30–80 words. Image block carries 3–5 search_queries for visual variety. Total source weight ≈ 60-100 words for the prose plus the image manifest. Compare to current TLS `activity_breakfast_frank` ≈ 540 words for the same role — ~5–8× tighter.

**For NPC-paired activities (e.g., breakfast with Frank):** add NPC-arc-state group blocks that swap the prose by Frank/Ryan/Jake stage. ONE fixed paragraph per state (DEFAULT / WITHDRAWN / WARM / CONSEQUENCE), not multiple variants per state. The state-swap is deterministic (gated on flags), not random rotation. Pattern in current TLS's `activity_breakfast_frank` is structurally correct on the state axis — just needs each variant compressed from ~80–120 words to ~30–80 words.

**For occasional dispatch to alternative scenarios:** author a sibling canvas at the same location with `trigger.chance = 0.1` (1-in-10) and higher priority. Engine pre-empts the standard activity when the chance roll succeeds AND its other conditions match. Verified RtS pattern — `BedroomStudy` dispatches to Dad/Brother grope events via dice + presence + corruption gates.

### 2.5 Scene canvas (repeatable, gated, linkreplace cascade)

**What it is.** A repeatable but state-gated scene that uses the linkreplace cascade pattern. Same passage shows more on later visits via `<<if>>`-progressed gates. Tier-2 density: each beat 1–3 sentences + image + dialogue.

**Engine note.** TLS doesn't have a `<<linkreplace>>` macro natively in the block-types. The functional equivalent is **multi-node canvas with conditional sub-node routing**: the canvas has 3–10 nodes, the player's first visit hits node 1, sets a quest flag, exits. The player's third visit hits node 3 (because nodes 1 and 2 are now flag-gated as "already seen"). This produces the same revealed-progressively behavior. ALTERNATIVELY: the scene canvas IS a single node with multiple `group` block variants gated on `quest_progress_<scene>` value, and the exit_block re-fires the canvas after each beat. Both work; we'll pick one in §8 worked example.

**TOML skeleton (single-node multi-group approach):**
```toml
[[canvases]]
id = "scene_marge_thursday_close"
name = "Thursday close"

[canvases.trigger]
location = "loc_diner_front"
is_repeatable = true
priority = 8
is_active = true
conditions = { version = "1.0", items = [
  { type = "flag", subject = "player", flag_key = "first_ambient_tilt", operator = "is_true" },
  { type = "flag", subject = "player", flag_key = "marge_thursday_close_today", operator = "is_false" }
] }
[[canvases.trigger.schedules]]
weekdays = [3]                # Thursday
start_time = "21:00"
end_time = "22:00"

[[canvases.nodes]]
id = "base"
blocks = [
  { type = "image", props = { file = "scenes/marge_thursday_close.jpg", ... } },
  # Beat 1 — always visible
  { type = "paragraph", content = "Thursday. The 9:00 lull. Marge slid the till key across the counter at her." },
  { type = "dialog", content = "Lock up at ten. Cash drawer in the safe. You done it before.", props = { speaker = "npc", npcId = "npc_marge" } },
  # Beat 2 — visible if quest progress > 0
  { type = "group", blocks = [
    { type = "paragraph", content = "..." }
  ], conditions = { version = "1.0", items = [
    { type = "trait", subject = "player", trait_key = "quest_marge_thursday_close", operator = "gte", value = 1 }
  ] } },
  # ... more beats with progressively higher quest gates ...
]
exit_block = { type = "choices", choices = [...] }
```

**Density target:** 80–400 words per scene. Each beat 1–3 sentences. Linkreplace-equivalent revealed progressively.

### 2.5b Explicit-tier scene canvas additions

When a scene canvas reaches into corruption-gated adult territory (Frank tease, Jake peek/draw, Diner T3, Ryan big-ticket close, the Cracks themselves), the same template applies plus four additions. All four are directly verified in RtS source (33 passages reference per-NPC corruption gating; `BrotherBedroomSex1` / `MarcusParkSex` / `StudyWithMarcus` verified at 10–12 linkreplace beats each).

**1. Per-NPC corruption gates.** Two-axis (Maya corruption + NPC corruption + per-act stage) gating. Verified pattern from `BrotherShowerSex`: `<<if StageTwoCorruption($npc.Brother)>><<linkreplace "Lean against the wall">>`. The per-act beat unlocks only when the NPC's own corruption stage clears — Maya alone can't drag a not-yet-corrupted NPC into a deeper act.

**2. Per-act progression counters.** Numeric counters (not flags) — `lean_by_desk_count`, `tease_jake_count`, `t3_back_booth_count`. Counter increments on scene completion. Beat-reveals gate on counter values. Verified pattern: RtS uses `getQuestProgress("StudyWithMarcus") > 2` and `> 4` to gate cascade depth across visits.

**3. Random media variety.** 3–5 image/video search queries per scene. The engine selects one at render time. Verified at `BrotherBedroomTease`: `<<set $game.randomMedia to either("brothertease1.webp", ..., "brothertease5.webp")>>`. The `find-media` skill retrieves; the rotation is the anti-staleness mechanism.

**4. Speech-dominant prose.** Verified ratio at `BrotherBedroomSex1`: 38 Speech lines + 13 videos in 5,877 chars ≈ 60% dialogue, 40% stage direction. Stage direction limited to 1–2 sentences per beat. Maya's interior monologue surfaces only at register-shift moments (corruption-band crossings, Crack-trigger pivots).

These four are verified mechanical patterns. The literary-vs-terse register choice (how the prose VOICE handles these scenes for TLS specifically) is governed by §10 below.

---

## §2.6 Stage-function helpers (RtS-derived pattern)

Borrowed from RtS source. Verified at `BrotherShowerSex`, `DadShowerSex`, `GrandpaShowerSex`, `BedroomSleepDadScene`, `BrotherBedroomTease` — 33 passages reference helper-function-style per-NPC corruption gates.

Pattern: define corruption "stages" once per NPC as helper functions. Gates check the helper, not the raw threshold. Tuning happens in one place per NPC.

```
StageTwoCorruption(npc) = npc.arousal >= 30 AND npc.corruption >= 25
StageThreeCorruption(npc) = npc.arousal >= 60 AND npc.corruption >= 50
```

For TLS, define analogous helpers per arc-NPC in `0_systems_spec.toml` or as engine setup:

| Helper | Gate (proposed) | Used by |
|---|---|---|
| `frank_stage_2()` | `frank.trust ≥ 40 AND frank.arousal ≥ 30 AND corruption ≥ 25 AND frank_restrict_declared` | Frank tease tier scenes |
| `frank_stage_3()` | `frank.arousal ≥ 60 AND corruption ≥ 50 AND frank.love ≥ 40` | Frank Crack-adjacent scenes |
| `ryan_stage_2()` | `ryan.trust ≥ 40 AND corruption ≥ 25 AND ryan_partner_open` | Ryan partner-tier closes |
| `ryan_stage_3()` | `ryan.love ≥ 60 AND corruption ≥ 75 AND ryan_partner_open` | Ryan big-ticket close |
| `jake_stage_2()` | `jake.love ≥ 0 AND corruption ≥ 30 AND jake_peek_draw_open` | Jake tease tier |
| `jake_stage_3()` | `jake.love ≥ 30 AND corruption ≥ 50 AND jake_caught` | Jake hand tier |

Gates throughout the codebase use `frank_stage_2()`, not the raw threshold. When playtesting reveals the threshold is wrong, the fix is one helper update, not 40 gate edits.

**Engine note.** TLS's current `conditions` schema doesn't natively support function calls (only flag/trait checks). Implementation options: (a) Author the helper as a derived flag computed at canvas-trigger time and stored as `frank_stage_2_active`. (b) Extend `conditions` schema with a `helper` type. (a) is convention-only; (b) is engine work. Recommend (a) for the rewrite; (b) deferred to engine track.

---

## §3 The location → hub map

The 38 locations in `1_metadata_and_locations.toml` get classified. Each Phase-1-accessible location gets exactly one hub canvas of one type.

| Location ID | Hub type | Rationale |
|---|---|---|
| `loc_property` | Hub-C (outdoor) | Yard-and-house exterior. Buttons to specific zones. |
| `loc_front_porch` | Hub-A (shared, light) | Diana sometimes here. Mostly transition. |
| `loc_back_porch` | Hub-A (shared, light) | Solo / smoke / sketch. |
| `loc_hallway` | Hub-A (transition) | Just navigation to upstairs rooms. |
| `loc_mayas_bedroom` | Hub-A (player solo space) | Solo activities. Variant of Type-A — Maya's own room. |
| `loc_kitchen` | Hub-A (shared) | Solo cook/eat/wash. NPC-presence-driven family dinner event. |
| `loc_living_room` | Hub-A (shared) | TV / sit / read. Frank-trigger event surface (Maya picks living room). |
| `loc_dining_room` | Hub-A (shared) | Mostly used during DIN band; family-dinner event. |
| `loc_bathroom` | Hub-A (shared) | Shower / mirror. |
| `loc_franks_office` | Hub-B (NPC personal) | Frank-arc primary surface. |
| `loc_franks_bedroom` | Hub-B (NPC personal) | Frank-arc late-tier surface (post-Crack romantic / arrangement routes). |
| `loc_jakes_bedroom` | Hub-B (NPC personal) | Jake-arc primary surface. |
| `loc_yard` | Hub-C (outdoor) | Ryan-arc primary surface. NPC presence keyed (Ryan scheduled here). |
| `loc_shop_customer_area` | Hub-C (outdoor) | Ryan-arc customer-close surface. |
| `loc_creek` | Hub-C (outdoor) | Solo time / sketch. |
| `loc_main_street` | Hub-C (outdoor) | Town hub. Sub-locations (diner / drugstore / college admin) gated by time. |
| `loc_diner_front` | Hub-A (workplace) | Marge + Cookie scheduled. T0/T1/T2/T3 shifts as scene canvases. |
| `loc_diner_back_booth` | Hub-A (workplace, gated) | T3 only. Phase-1 corruption-75 gate. |
| `loc_college_admin` | Hub-C (outdoor, single-shot) | Brochure event. Phase-1-only access. |
| `loc_church_front` | Hub-C (outdoor) | Sunday service surface. |
| `loc_general_store` | Hub-C (outdoor) | Goods purchase. |
| `loc_truck_stop_bar`, `loc_fairground`, `loc_hs_stadium`, `loc_church_interior`, `loc_college_campus` | (Phase 2+ locked) | No Phase-1 hub. Canvases stub out for later. |

**Total Phase-1 hub canvases: ~17.** Compare to current TLS Phase 1 having 0 hub canvases. This is a brand new layer.

---

## §4 The NPC schedule model

Following RtS verbatim. Each NPC has a single `.location` string field, mutated by a scheduler at time-band transitions.

### Engine support

The engine does NOT currently have an NPC-location scheduler that ticks `.location` automatically. Two options:

**(a) Author-driven schedule via NPC trigger schedules.** Each NPC has `[[npcs.npc_X.schedules]]` entries (already supported per `0_systems_spec.toml`). The engine queries the schedule when a canvas's trigger asks "is NPC X at this location now?". The `.location` field doesn't exist; instead, NPC presence is computed at canvas-trigger time from the schedule table.

**(b) Add an NPC-location scheduler ticker.** New engine-level component that mutates `npc.X.location` at time-band boundaries. Adds a sidebar item type for displaying NPC location in the right sidebar. **Engine work required.**

**Recommendation: (a) for the rewrite spec, defer (b) as a separate Phase-2-engine task.** Option (a) gives correctness; option (b) gives the visible-sidebar-roster RtS pattern. The rewrite can ship without (b).

### Sidebar visibility

Without (b), the right sidebar can't natively show "NPC X is in Kitchen now." Two workarounds:

- **Workaround 1 — text-only NPC location panel** assembled at canvas render time from the schedule lookup. Author it as a pseudo `trait_words` style item that emits "Frank: Office", "Diana: Kitchen", "Jake: Bedroom" based on schedule lookup at the current time band.
- **Workaround 2 — Guide page assembles the schedule** as a static reference table (per band × per NPC). Less dynamic but useful.

Both are author-side; no engine work. Recommendation: ship Workaround 1 in the vertical slice if it's mechanically possible; fall back to Workaround 2 if not.

### Per-NPC schedule tables

Derived from `2b_systems_budget.md` § 2 (Authority = Diana + Frank), § 3 (per-NPC arc stages), and `final_book.md` Frank-window references (06:30–07:30, 17:30–18:30 confirmed). Filling in across the 6 bands × 7 days.

**Frank** (60s, landlord, disciplined Southern man):

| Band | Hours | Mon-Fri | Sat | Sun |
|---|---|---|---|---|
| EM | 05:00–07:00 | Office (early bookkeeping) | Office | Porch (paper) |
| M | 07:00–09:00 | Kitchen (breakfast) | Kitchen | Kitchen → Church (10am) |
| MID | 09:00–13:00 | Office | Yard / errands | Living room (post-church) |
| A | 13:00–17:00 | Office | Yard / repair | Porch |
| DINPREP | 17:00–18:30 | Kitchen (cooks with Maya) | Kitchen | Kitchen |
| DIN | 18:30–19:30 | Dining room | Dining room | Dining room |
| E | 19:30–21:00 | Living room (TV) | Porch | Porch |
| N | 21:00–23:00 | Office (late) | Office | Bedroom |
| LN | 23:00–01:00 | Bedroom | Bedroom | Bedroom |

**Diana** (50s, mother, household anchor):

| Band | Hours | Mon-Sun |
|---|---|---|
| EM | 05:00–07:00 | Kitchen (always — the safe-harbor signal) |
| M | 07:00–09:00 | Kitchen |
| MID | 09:00–13:00 | Side garden / sewing room (Mon-Fri); errands (Sat); church (Sun) |
| A | 13:00–17:00 | Sewing room / laundry / quiet |
| DINPREP | 17:00–18:30 | Kitchen |
| DIN | 18:30–19:30 | Dining room |
| E | 19:30–21:00 | Living room (reading) |
| N | 21:00–23:00 | Bedroom |
| LN | 23:00–01:00 | Bedroom |

**Ryan** (mid-20s, used-equipment flipper, hands-on):

| Band | Hours | Mon-Fri | Sat | Sun |
|---|---|---|---|---|
| EM | 05:00–07:00 | Bedroom | Bedroom | Bedroom |
| M | 07:00–09:00 | Kitchen → Yard | Yard | Kitchen → Yard |
| MID | 09:00–13:00 | Yard / Shop | Shop (customer day) | Yard / repair |
| A | 13:00–17:00 | Yard / Shop | Shop / road trip | Yard |
| DINPREP | 17:00–18:30 | Yard (clean up) | Yard | Yard |
| DIN | 18:30–19:30 | Dining room | Dining room | Dining room |
| E | 19:30–21:00 | Yard / shed | Bar (Phase 2+, locked) | Living room |
| N | 21:00–23:00 | Bedroom | Bar / Bedroom | Bedroom |
| LN | 23:00–01:00 | Bedroom | Bedroom | Bedroom |

**Jake** (early-20s, hostile artist, draws):

| Band | Hours | Mon-Sun |
|---|---|---|
| EM | 05:00–07:00 | Bedroom (asleep) |
| M | 07:00–09:00 | Bedroom (drawing) |
| MID | 09:00–13:00 | Bedroom |
| A | 13:00–17:00 | Bedroom (mostly); occasional creek walk |
| DINPREP | 17:00–18:30 | Bedroom |
| DIN | 18:30–19:30 | Dining room (headphones around neck) |
| E | 19:30–21:00 | Bedroom |
| N | 21:00–23:00 | Bedroom |
| LN | 23:00–01:00 | Bedroom (drawing late) |

**Marge** (50s, diner owner):

| Band | Mon-Sat | Sun |
|---|---|---|
| EM | Diner kitchen (prep) | Closed |
| M | Diner front (open 7am) | Closed |
| MID | Diner front | Closed |
| A | Diner front | Closed |
| DINPREP | Diner front | Closed |
| DIN | Diner front | Closed |
| E | Diner front | Closed |
| N | Diner front (close 10pm) | Closed |
| LN | Diner kitchen (cleanup, gone by 11) | Closed |

**Cookie** (mid-30s, line cook, peer): same diner schedule as Marge but on the line, not the floor.

These tables will become the `[[npcs.npc_X.schedules]]` entries in the new `0_systems_spec.toml`.

---

## §5 The state-pump button roster

State-pump buttons are the workhorse interaction surface. One per NPC × per "lighter" interaction type. Daily-cooldown-gated.

### Design template

```
[Button text] @ [hub canvas] when [NPC scheduled here]:
  → effects: [npc.X.relation +1 OR npc.X.arousal +1 OR npc.X.corruption +1]
  → flagEffects: [talked_to_X_today]
  → cooldown: blocked if talked_to_X_today already true
  → toast: "[short Maya-voice line]"
```

### Per-NPC roster

**Frank** (at hub_franks_office during MID/A/N; hub_kitchen during M/DINPREP/DIN; hub_living_room during E):
- "Talk to Frank 💬" — pumps `frank.trust +1`, sets `talked_to_frank_today`. Toast: *"He looked up. The page stayed where it was."*
- "Help with bookkeeping 📒" (gated `corruption ≤ 49` — pure work option) — pumps `frank.trust +2`, costs 1 hour, sets `bookkeeping_today`. Toast: *"He passed the ledger across. The numbers were the numbers."*
- "Sit with Frank on the porch 🪑" (E band only, hub_porch) — pumps `frank.trust +1`, sets `sat_with_frank_today`. Toast: *"He didn't look over. He didn't move the paper either."*

**Diana** (at hub_kitchen during EM/M/DINPREP/DIN; hub_living_room during E):
- "Help Diana 🥖" (DINPREP/DIN at hub_kitchen) — pumps `diana_awareness +1`, sets `helped_diana_today`. Toast: *"She handed her the basil without looking up."*
- "Sit with Mom 📖" (E at hub_living_room) — pumps `diana_awareness +1`, sets `sat_with_diana_today`. Toast: *"Mom turned the page of the book. She didn't say anything."*

**Ryan** (at hub_yard during M/MID/A; hub_shop during MID/A on Sat):
- "Hand him a tool 🔧" (hub_yard, when Ryan there) — pumps `ryan.trust +1`, sets `handed_ryan_tool_today`. Toast: *"Wrench'd help. Thanks, kid."*
- "Bring him water 🧊" (hub_yard, A band, summer heat) — pumps `ryan.trust +1`, sets `brought_ryan_water_today`. Toast: *"Don't drink it all at once."*
- "Watch him work 👀" (hub_yard, no cooldown — soft observe) — pumps `ryan.trust +0.5` rounded down to 0 some visits + sets a passive flag. Toast: *(no toast, Maya's standing in the yard for the duration.)*

**Jake** (at hub_jakes_bedroom almost always — knock interaction):
- "Knock on Jake's door 🚪" (hub_hallway always available) — IF `jake_door_cracked` open: pumps `jake.love +1`, opens scene canvas. ELSE: blocked silently with toast: *"He didn't answer. Of course he didn't."*

**Marge** (at hub_diner_front during work hours):
- "Ask about a shift" (covered by hire / shift-claim event canvases — not state-pump).
- "Read the room" (state-pump) — pumps `rep_road +1` on slow shifts, no cooldown but limited use. Toast: *"Nobody needed anything. Marge nodded once."*

**Cookie** (at hub_diner_front during work hours):
- "Talk to Cookie 💬" (during diner shifts) — pumps `cookie.trust +1`, sets `talked_to_cookie_today`. Toast: *"Cookie laughed at the joke. Cookie laughed at most things."*

**Total state-pump buttons: ~12–15.** They fire dozens of times across a playthrough. Per-button source weight: ~30 words including the toast. Total source for the roster: ~500 words.

### Per-act progression counters

Distinct from state-pump buttons. Counters are NUMERIC (not flags) and don't reset daily. They track how many times Maya has performed a specific act with a specific NPC. Scene canvases gate beat reveals on counter values.

Per-NPC × per-act counter roster:

| Counter | Increments when | Used by |
|---|---|---|
| `bookkeeping_count` | activity_bookkeeping_with_frank fires | Frank trust progression milestones |
| `lean_by_desk_count` | scene_frank_lean_by_desk fires | Frank tease tier reveal-depth |
| `chore_porch_supervised_count` | activity_chore_porch_sweep fires under Restrict | Frank Phase B accumulator |
| `flash_jake_count` | scene_jake_flash fires (post-noticed) | Jake tease tier |
| `peek_jake_count` | event_peek_jake fires | Jake caught-trigger threshold |
| `tease_jake_count` | scene_jake_doorway_lean fires | Jake hand-tier reveal-depth |
| `ride_shotgun_with_ryan_count` | activity_ride_shotgun fires | Ryan partner-tier ambient |
| `shop_close_small_count` | scene_ryan_close_small_X fires | Ryan partner-tier unlock |
| `t1_shift_count`, `t2_shift_count`, `t3_back_booth_count` | corresponding diner shift scene fires | Tier escalation gates |
| `mirror_look_count` | activity_mirror_look fires | Maya self-recognition prose-band swap |

**Counters reset only at game start, not at sleep.** Beat reveals in scene canvases gate on counter values (e.g., the deeper beats of `scene_frank_lean_by_desk` reveal at `lean_by_desk_count >= 3`).

**Engine note.** TLS engine currently supports flag/trait checks in `conditions`. Counters can ride on the existing `trait` channel (player or NPC) — author them as numeric traits, not flags. Increment via `effects` blocks. No engine change needed.

### Daily-reset

The Sleep activity adds `clear_all_today_flags` to its effects:
```toml
flagEffects = [
  { targetType = "player", flag = "talked_to_frank_today", op = "unset" },
  { targetType = "player", flag = "talked_to_diana_today", op = "unset" },
  ...
]
```

---

## §6 Per-NPC arc-progression contracts

How accumulating state-pump and scene engagement converts into new buttons appearing at hubs. RtS isBoyfriend-pattern adapted.

### Frank arc

Stages from `2b_systems_budget.md` §3 collapsed onto button-availability:

| Stage | Trigger | New button(s) appear |
|---|---|---|
| **Meet** | Day 1, `arrived_at_franks` | `hub_franks_office`: "Talk", "Help with bookkeeping" |
| **Phase A (Rules established)** | `frank.trust >= 20` AND `bookkeeping_count >= 3` | "Sit with Frank on the porch" appears at hub_back_porch E band |
| **Trigger fired** (Maya picks living room → caught) | One-shot canvas `event_frank_catch` fires when Maya does corruption-25-gated solo masturbation in `hub_living_room` AND Frank scheduled home | `frank_caught` flag set; `hub_franks_office` "Talk" button text changes to *"Talk to Frank — about it"* (different scene_canvas behind it) |
| **Restrict declared** | Frank-arc decision after catch → `frank_restrict_declared = true` | New buttons at hub_kitchen / hub_living_room: "Chore: porch sweep" "Chore: kitchen cleanup" — small income, supervision-flavored |
| **Tease under compliance** | `corruption >= 50` AND `frank_restrict_declared` AND `frank.arousal >= 30` | Tease scene canvas `scene_frank_tease_X` becomes available at `hub_franks_office` |
| **Crack** | Tease scene fired N times AND `frank.arousal >= X` | One-shot `event_frank_crack`. After: `frank_cracked = true` |
| **Call-out** | Player choice in `event_frank_crack` | One-shot `event_frank_called_out` |
| **Keep route** | One of {romantic, arrangement, rupture, power_inverted} flags set | Hub_franks_bedroom unlocks; specific scene_canvases per route |

**Surface in hub menu:**
- **Initially:** hub_franks_office shows 2 buttons (Talk, Bookkeeping).
- **After Trigger:** still 2, but Talk leads to a different scene.
- **After Restrict:** still 2 main + chore options at kitchen.
- **After Tease unlock:** hub_franks_office shows 3 buttons (Talk, Bookkeeping, "Linger by the desk" — the corruption-50 gated tease entry).
- **After Crack:** hub_franks_office button set transforms — Bookkeeping replaced by Keep-route options.

**This is the design contract.** No prose-state changes; option-set changes.

### Ryan arc

| Stage | Trigger | New button(s) appear |
|---|---|---|
| **Meet** | Day 1 (ambient first encounter event) | `hub_yard`: "Hand him a tool", "Watch him work", "Bring water" |
| **Help tier open** | `ryan_help_tier_open = true` (gated by `ryan.trust >= 15` + `group_settled_in`) | `hub_shop_customer_area`: small-ticket close scene canvases |
| **Partner** | `corruption >= 25` AND `ryan_help_tier_open` AND `partner_invitation_event` fired | `hub_shop_customer_area`: mid-ticket close scene canvases (charm-gated) |
| **Big deal** | `corruption >= 75` AND `ryan_partner_open` AND customer-flag | `hub_shop_customer_area`: big-ticket close scene canvas (sex-included) |
| **Beach** | Big deal closed | One-shot `event_ryan_beach_proposal` fires next morning |
| **Keep route** | Player answer at beach (yes_engaged / not_yet / no_withdrawn) | Hub_yard's "Watch him work" button text changes per route |

### Jake arc

| Stage | Trigger | New button(s) appear |
|---|---|---|
| **Meet (hostile)** | Day 1 | `hub_jakes_bedroom`: "Knock" (always silently rebuffs), no other buttons |
| **Noticed** | `beauty >= 50` AND ambient event `event_jake_first_glance` fires | `hub_dining_room` DIN band: ambient observation prose changes; no new button yet |
| **Peek/draw** | After 3+ Noticed-tier ambient events | One-shot `event_jake_peek_draw_revealed`. After: `jake_peek_draw_open = true`. Hub_jakes_bedroom: "Lean in the doorway" appears (corruption-30 gated tease) |
| **Tease** | `corruption mid-band` AND `jake_peek_draw_open` | "Lean in the doorway" leads to `scene_jake_tease` |
| **Caught** | Tease scene fired AND Maya choice to push → `event_jake_caught` | `jake_caught = true`; hub_jakes_bedroom transforms |
| **Hand** | Player choice in caught event | `jake_hand = true`; hub_jakes_bedroom shows new options |
| **Keep route** | One of {owned, lovers, withdrawn, she_uses_him} | Hub_jakes_bedroom transforms again |

### Diana arc (Phase 2+)

No Phase-1 buttons surface beyond the state-pump "Help Diana" / "Sit with Mom." The accumulator runs invisibly via `diana_awareness`. Phase 2 spec deferred.

### Marge arc

Marge stays clean per design lock. Hub_diner_front shows: "Take a shift" → diner-tier scene canvases. "Talk to Marge" state-pump. No sexual arc.

---

## §7 The economic loop

Lifted from `2b_systems_budget.md` §4. Recast as scene canvases.

### Diner shifts as tier-gated scene canvases

`hub_diner_front` shows shift options based on time band + corruption tier:

| Shift | Hub button | Gate | Scene canvas | Pay |
|---|---|---|---|---|
| **T0 Distance** | "Take a shift (T0)" | always when `hired_at_diner` AND M/A/E/N | `scene_diner_t0` | $45 / 5h |
| **T1 Play along** | "Take the shift (read the floor)" | corruption ≥ 25, rep_road ≥ 15, beauty ≥ 45 | `scene_diner_t1` | $45 + $8-20 tips |
| **T2 Work the floor** | "Take the floor" | corruption ≥ 50, beauty ≥ 55 | `scene_diner_t2` | $45 + $25-60 tips |
| **T3 Back booth** | "Stay for the back booth" | corruption ≥ 75, first_ambient_tilt, customer flag | `scene_diner_t3_<customer>` | $50-200 / scene |

T0 fires unconditionally as the daily working shift. T1/T2 are *replacements* for T0 once gates clear (player can opt for higher tier or stay at T0). T3 is *additional* (after-close, Thursday-only via `marge_thursday_key`).

Each scene is the linkreplace cascade pattern: 1-2 paragraph opening + 5-10 customer beats (each 1-3 sentences + dialogue) + clock-out. Source weight per shift scene: ~250-400 words.

### Ryan shop closes as scene canvases

`hub_shop_customer_area` shows close options based on customer schedule + arc:

| Close | Hub button | Gate | Scene canvas | Pay |
|---|---|---|---|---|
| **Small** | "Help with the close (small)" | ryan_help_tier_open + customer scheduled | `scene_ryan_close_small_<customer>` | $10-25 |
| **Mid** | "Close it" | ryan_partner_open + corruption ≥ 25 + mid customer | `scene_ryan_close_mid_<customer>` | $40-100 |
| **Big** | "Close the big one" | ryan_partner_open + corruption ≥ 75 + big customer | `scene_ryan_close_big_<customer>` | $80-300 |

Customer flags follow the schedule (`customer_farmer_thursday`, `customer_contractor_saturday` — set by passive weekly-tick). Player chooses to be present at hub_shop during close window; if conditions match, the close scene is available.

### Frank chores as activity canvases

Post-Restrict only. Small payments. Activity canvases at hub_kitchen / hub_living_room / hub_yard:

| Activity | Pay | Gate |
|---|---|---|
| `activity_chore_porch_sweep` | $5 | frank_restrict_declared |
| `activity_chore_kitchen_cleanup` | $8 | frank_restrict_declared, M/E band |
| `activity_chore_yard_clean` | $10 | frank_restrict_declared |
| `activity_chore_office_paper_file` | $15 | frank_restrict_declared, MID band, hub_franks_office |

### Income math from `2b_systems_budget.md` carries forward as-is

Pure T0 = $150/wk net = ~10 weeks to $1500. T1+Help = $230/wk = ~6.5 weeks. T2+Partner = $380/wk = ~4 weeks. The math stays. The implementation moves to scene canvases.

---

## §8 The vertical slice (Day 1–3 build)

Proof-of-pattern. The minimum playable scope that demonstrates every object type.

### Scope: Saturday Week 1 → Monday Week 1 evening

Three days. Maya arrives Saturday evening, has the first morning kitchen scene Sunday, walks to town Monday, gets hired at the diner, plays first T0 shift Monday evening, sleeps.

### Required canvases for the slice

**Hubs (8):**
1. `hub_property` — outdoor establishment, navigation to house/yard/road
2. `hub_front_porch` — Diana sometimes, route to house
3. `hub_hallway` — house transition (already exists per existing TLS — keeps shape, content rewritten)
4. `hub_mayas_bedroom` — solo activities + sleep
5. `hub_kitchen` — Type-A shared, Diana scheduled M/DINPREP, Frank M
6. `hub_living_room` — Type-A shared
7. `hub_main_street` — outdoor city hub
8. `hub_diner_front` — workplace, Marge + Cookie scheduled

**One-shot events (5):**
9. `event_arrival_at_franks` — Saturday 5pm. Replaces current B1. Single-node ~150 words. Frank takes suitcase, Diana hugs, Ryan voice from yard, Jake at dinner. Sets all 5 first-meet flags + `arrived_at_franks`.
10. `event_first_morning_kitchen` — Sunday 6:30. Replaces current B2. Single-node ~150 words. Rent terms + church choice. Two-button exit.
11. `event_first_walk_to_town` — Monday 9am. Replaces current B5. Single-node ~80 words. Diana names the route, Maya leaves.
12. `event_marge_interview` — Monday 5pm. Replaces current B6. Single-node ~120 words. Marge's "Tie it. Learn as you go." + Cookie's two-hour shadow.
13. `event_first_diner_t0_shift` — Monday 5-10pm. Single-node ~250 words. Cookie's instructions + 3 customer beats + clock-out.

**Activities (12):**
14. `activity_sleep` — replaces current. Daily flag reset + 480 min + energy 100. Block_pool of 5 sleep paragraphs.
15. `activity_shower` — replaces current. Block_pool of 4. Hygiene reset.
16. `activity_sketch_bedroom` — replaces current. Block_pool of 5.
17. `activity_eat_fridge` — Type-A kitchen action. Block_pool of 3.
18. `activity_cook_solo` — kitchen action. Block_pool of 4.
19. `activity_wash_dishes` — kitchen action. Single paragraph.
20. `activity_walk_to_creek` — outdoor.
21. `activity_walk_property` — outdoor.
22. `activity_porch_sit` — front_porch action, low energy cost.
23. `activity_living_room_tv` — living room action.
24. `activity_mirror_look` — bathroom action, special (~600w per spec — corruption-band variants matter here).
25. `activity_diner_t0` — repeatable shift after first-shift event done.

**Scenes (3 in this slice):**
26. `scene_diner_t0_repeat` — the shift scene that fires for visits 2..N, with rotating customer beats.
27. `scene_marge_talk` — talk-with-Marge state-pump-attached scene? Actually this is a state-pump button, not a scene. Skip.
28. (Reserve slot.)

**State-pump buttons** (effects on hubs, not separate canvases):
- "Help Diana 🥖" at `hub_kitchen` DINPREP (Mon-Sun)
- "Sit with Mom 📖" at `hub_living_room` E (any day)
- "Talk to Marge" at `hub_diner_front` (during shift)
- "Talk to Cookie 💬" at `hub_diner_front`

### Total slice inventory: 25 canvases + 4 state-pump buttons

vs. current Day-1-to-Monday equivalent in TLS: B1 (1300w) + B2 (700w) + B5 (700w) + B6 (700w) + B7 + scattered activities ≈ 8 canvases at current density = ~5500 words. New: 25 canvases at ~80-250 words each = ~3500-5000 words across 25 objects + activities reusable for hundreds of visits. **Source weight comparable. Repeat-value vastly higher.**

### Build order within the slice

1. **Day 0 — schema check.** Author 1 hub canvas (`hub_kitchen`) + 1 event (`event_first_morning_kitchen`) + 1 activity (`activity_sleep`) + run `package_from_toml --dry-run`. Confirm engine accepts the patterns.
2. **Day 1 — Saturday.** `hub_property`, `hub_front_porch`, `hub_hallway`, `hub_mayas_bedroom`. `event_arrival_at_franks`. `activity_sleep`. Player can play: drive in, see family, go to bed.
3. **Day 2 — Sunday morning.** `hub_kitchen`. `event_first_morning_kitchen`. Player can play: come down, hear rent terms, choose church or stay.
4. **Day 3 — Sunday afternoon to Monday.** `hub_living_room`, `hub_main_street`, `hub_diner_front`. `event_first_walk_to_town`, `event_marge_interview`, `event_first_diner_t0_shift`. Activities: `activity_shower`, `activity_sketch_bedroom`, `activity_eat_fridge`, `activity_walk_to_creek`. Player can play: free afternoon, town walk, hire, first shift, home, sleep.
5. **State-pump roster.** Add the 4 buttons.
6. **Validation.** `package_from_toml --dry-run`. Manual playthrough.

### Acceptance criteria for the slice

- Player can run Saturday-Sunday-Monday in sequence without error.
- Each canvas density meets target (event ≤250 words, activity ≤150 words, hub ≤300 chars body).
- State-pump buttons fire effects without scene transitions.
- Sleep clears all `*_today` flags.
- Diner T0 first shift sets `hired_at_diner` and unlocks `activity_diner_t0` for repeats.
- The 5 first-meet flags from current B1 (`met_diana_day_1`, etc.) are preserved.
- The Prologue still triggers correctly at game start.

If acceptance passes, the pattern is proven. The remaining ~125-200 canvases of Phase 1 ride on the same template.

---

## §9 Build order across the full rewrite

### Phase A — Vertical slice (this doc's §8)
3 in-game days. ~25 canvases. **First milestone.** Proves the pattern. Pause for review and redirect before continuing.

### Phase B — Week 1 complete
Mon evening through following Monday morning. Add the day-2-to-day-7 routine: weekday diner shifts, Sunday church, Saturday market (Phase 1 limited), Ryan first encounter, Jake first cold-shoulder. ~40 additional canvases.

### Phase C — Phase 1 first-month spine
Weeks 2-4. Frank Phase A + first ambient tilt + Ryan help tier + Jake noticed. ~60 additional canvases (events + scenes for the arc-progression unlocks).

### Phase D — Phase 1 escalation
Weeks 5-12. Tier escalations (T1, T2, Ryan partner, Jake peek-draw, Frank trigger), Cracks (Beach, Frank Crack, Jake Hand). The 8 Tier-A scenes. ~50 additional canvases.

### Phase E — Phase 1 close
Keep-tier Fork. The summer-end family dinner. Phase 1 close event. ~10 additional canvases.

### Phase F — Polish + validation
Full playthrough audit. Flag-graph verification. Voice consistency pass against style sheets. Media manifest authoring (image/video search_queries on every canvas). ~no new canvases; rework only.

### Total rewrite scope estimate

~185-220 canvases across all phases. Compare to current TLS Phase 1 inventory: 79 + 139 = 218.

**Net inventory size similar; ratio inverted; total wordcount 30-50% lower; repeat-value 5-10× higher.**

### Migration plan for the existing canvases

Three options for the existing `2_story_canvases.toml` and `3_activities.toml`:

**(a) Hard archive.** Move files to `archive/` directory. Build new TOML files (`2_story_canvases_v2.toml`, `3_activities_v2.toml`). Update `6_final_game.toml` build script.

**(b) Soft archive.** Keep files in place. Mark every existing canvas `is_active = false`. Add new canvases inline. Less disruptive but creates clutter.

**(c) Parallel rebuild.** Build `toml_phases_v2/` directory alongside current. Switch the source-of-truth pointer when v2 is shippable.

**Recommendation: (c) parallel rebuild.** Keeps current game playable as reference. Lets us A/B compare any time. Switch over when v2 passes acceptance.

---

## §10 Voice register rule

**This is a creative choice, not an RtS finding.** RtS's prose at every tier is transactional and terse — *"Get on all fours."* + a one-sentence stage direction. TLS keeps a literary voice as canon (the Prologue is the strongest specimen) but chooses where to apply it and where to step back. The rule below sets that boundary.

| Object type | Register | Density | Rationale |
|---|---|---|---|
| **Prologue** (frozen) | Full literary novella. FID, long subordinated sentences, sustained interior monologue. | 400–800 words per node | Backstory cinematic before the player has agency. Earns the density. |
| **Tier-A Cracks** (Beach, Frank Crack, Jake Hand) | TLS-literary, tighter than Prologue. FID surfaces at register-shift moments. | 120–200 words per node, 8–15 nodes | Dramatic pivots that genuinely re-shape Maya. Prose carries weight. |
| **Event canvases** (one-shot story beats) | TLS-literary at compressed density. Single-node. | 80–250 words total | A specific moment with real choice. Prose lands the moment, choice carries forward. |
| **Activity canvases** (ambient repeatables) | TLS-literary, Failbetter density. Single fixed paragraph per arc-state; image-rotated. | 30–80 words per arc-state | Ambient color. Variety from rotating images (3–5 search queries) + occasional rare-event sibling canvases (`trigger.chance`). NO prose-pool rotation — verified RtS pattern is image rotation only. |
| **Scene canvases (non-explicit)** | TLS-literary, Failbetter density. | 80–400 words across all reveals | Repeatable arc-progressing beats. Same shape as event canvas, gated for re-entry. |
| **Scene canvases (explicit-tier)** | **Hybrid: short stage direction (1–2 sentences) + dialog-heavy.** Maya interior surfaces only at corruption-band shifts or register-marker moments. | 80–300 words across all reveals | The act itself is mechanical (per design book §1: *"Every sexual act is mechanical, not taboo-crossing"*). Prose carries Maya's reaction at register-pivots, not the choreography. |
| **State-pump toasts** | Single sentence. Maya-voice or short stage direction. | 8–20 words | Feedback signal, not a scene. |

### Where the literary register goes silent

The shift from "literary" to "stage-direction-heavy" is sharpest at the explicit-scene tier. RtS's terse register isn't rejected — it's adopted *where the act itself is the load-bearing element*. Crude dialogue, brief stage direction, the corruption-band marker that surfaces *only* when Maya's relationship to the act has changed in a way she registers.

In an Operating-band sex scene, the prose is mostly:
- Brief stage direction: *"He turned her against the desk."*
- Dialog: *"Bend over."* / *"Like this."*
- One register-marker line per scene (the band signal): *She watched her own hand on the wood. She watched it like she was watching someone else's hand.*

In a Saturated-band version of the same act, that register-marker line shifts: *Her hand was her hand. The desk was a thing she had bent against before. The minute had a shape she knew the count of.*

The mechanical beats are nearly identical. The single register-marker line is what carries the corruption-band signal. The `corruption_band_register.md` four-band voice catalog applies to these marker lines, not to every paragraph.

### Where the literary register stays full

- Prologue (frozen).
- Tier-A Cracks (the eight scheduled Crack beats per design book).
- The first canvas of each chapter (B-tier opening event canvases).
- The first instance of each NEW act with a given NPC (the first-time variant gets the register; subsequent visits compress).

### Why this isn't RtS

RtS doesn't write moments where Maya watches her own hand. RtS doesn't shift register based on a four-band catalog. The mechanical engine is RtS-derived; the register placement is the TLS authorship choice. **The two layers are separable: someone could implement the rewrite spec mechanically (hubs, state-pumps, scene canvases, per-NPC corruption, three-axis gates) and still write every passage in pure transactional register.** Choosing the literary-where-it-matters / terse-where-it-doesn't hybrid is the explicit creative decision the rewrite makes.

### Practical authorship checklist for any explicit-tier scene

Before writing prose:
1. What is the Maya corruption band at this firing? (Closed / Opening / Operating / Saturated.)
2. What is the NPC arc state at this firing? (Restrict, Tease, Crack-adjacent, post-Crack.)
3. What is the per-act counter at this firing? (First time? Tenth time?)
4. Is THIS the register-marker beat? (Usually one per scene, sometimes zero on counter-deep visits.)

If 1+2+3 don't move from the previous scene firing, the prose stays mostly the same — only random media + small surface variation. If any of them move, that's where the register-marker line lands.

This converts the corruption-band register from "voice across 700 words of canvas" (current TLS approach, drift-prone) to "single sentence at the register-shift moment" (verifiable, auditable, hard to drift).

---

## §11 What this doc is NOT

- **Per-canvas prose.** Each canvas is authored against this spec at build time. Style sheets in `content_rewrite/style_sheets/` remain valid for voice.
- **Per-canvas flag effects.** Flag list and effect tables are in the design book sections 7-8. This doc references them; doesn't repeat.
- **A voice/style guide.** `content_rewrite/standards.md` 27 rules + style sheets remain authoritative for HOW prose is written. This doc dictates SHAPE.
- **An engine spec.** Engine work (NPC scheduler, sidebar items for NPC location) is deferred and tracked separately.
- **A test plan.** Acceptance criteria per phase live in §8. Detailed test plans per scene are author-time deliverables.

---

## §12 Status

**Date:** 2026-04-28.

**Sequence:**
- ✅ §1 RtS pattern verified via live exploration.
- ✅ §2 five object types defined with TOML skeletons grounded in verified RtS source + existing TLS engine block-types.
- ✅ §2.5b explicit-tier scene canvas additions (per-NPC corruption gates, per-act counters, random media, speech-dominant prose). Verified against 33 RtS passages.
- ✅ §2.6 stage-function helpers (RtS-derived `StageTwoCorruption`/`StageThreeCorruption` pattern) — 6 helpers for Frank/Ryan/Jake.
- ✅ §3 location → hub map drafted from `1_metadata_and_locations.toml`.
- ✅ §4 NPC schedule model drafted; sidebar visibility deferred to optional engine work.
- ✅ §5 state-pump roster drafted (~12-15 buttons) + per-act progression counter roster (~12 counters).
- ✅ §6 arc-progression contracts drafted from `2b_systems_budget.md` §3.
- ✅ §7 economic loop drafted from `2b_systems_budget.md` §4.
- ✅ §8 vertical slice scoped (25 canvases + 4 state-pump buttons).
- ✅ §9 full-rewrite phasing drafted (Phases A-F).
- ✅ §10 voice register rule — TLS literary-where-it-matters / terse-where-it-doesn't hybrid. Explicit creative choice, not RtS-derived. Practical authorship checklist included.

**Next concrete deliverable:** vertical slice TOML authoring (Phase A). Begin with `hub_kitchen` + `event_first_morning_kitchen` + `activity_sleep` for engine sanity check.

**Open questions before vertical slice authoring:**
- Migration choice (a/b/c for retiring current canvases). Recommend **(c) parallel rebuild**.
- Sidebar NPC-location panel: Workaround 1 (text-only assembled) vs. Workaround 2 (Guide page static) vs. defer entirely. Recommend **Workaround 1** if mechanically possible.
- Prologue: confirmed survives intact ✅.
- Vertical slice first ✅.
