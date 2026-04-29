# Hub-Event Architecture: The Shape of Phase-2 Locations and Events

> **Created 2026-04-28.** Sibling to `00_TLS_Phase2_Diagnosis_and_Direction.md`.
> Brainstorming doc, not PRD. Commits to vocabulary and a worked example. Major decisions are presented as **options + recommendation + redirect-prompt** so the user can redirect cheaply.
> Status legend: 🔄 PROPOSED · 🔒 DEFERRED to a later doc · ✅ WORKING (already converged from prior conversation).

---

## §0 Frame

The diagnosis (`00_`) named one root cause behind every TLS Phase-1 problem: **canvases were authored at chapter-granularity, not event-granularity.** Three-sub-node "establishment sequences" with single-"Continue" buttons (B1 arrival, B5 town walk, B6 Marge interview) imitated the Prologue's novel register, which the Prologue earned because it was a backstory cinematic and Phase 1 doesn't because it's a sandbox.

This doc commits to a different shape — the **hub-and-event** shape that all four explored reference games share. It does this without changing the engine. Every proposal here maps onto existing TOML primitives (`image`, `paragraph`, `dialog`, `block_pool`, `group`, `choices`, `clip`). The diagnosis was unambiguous: structure was wrong, not the engine. Engine surface stays where it is. What changes is the **author-side convention** — what we call a hub, what we call an event, what shape they take, and where the kitchen-at-six-thirty-on-a-Tuesday lives.

The doc commits to vocabulary, the hub recipe, the disposition of the most-touched current canvas (`first_morning_kitchen`), and a translation framework (α/β/γ) that 04 will apply across the 28 Phase-1 canvases. It defers everything runtime — rotating-opening counts, rare-event injection, NPC cooldowns, stat-gated escalation — to 03.

---

## §1 Patterns we're drawing from

Six pattern handles. Each gets used as shorthand throughout the doc; each comes from one of the four explored games. Where I cite a passage, the passage exists in the explored corpus and the cite was verified during exploration — no inventions.

### Pattern 1 — The hub-menu shape

A hub is a **menu**, not a scene. Road-to-Success's rendered hubs are 5–10 words plus a vertical button list. Sample bodies from `road-to-success/scene_bodies.jsonl`:

```
YOUR BEDROOM
Study 📖
Nap 💤
Wardrobe 👚
Hallway 🚪
```

```
MARCUS'S BEDROOM
Talk with Marcus 💬
Study with Marcus 📖
Hallway 🚪
```

The player *lives* in this menu. They do not read 700 words to get from the doorway to a chair. Hub passages in RtS are 50–350 chars total; the narrative density lives inside the events.

### Pattern 2 — Time-of-day-driven option sets

Same hub passage, different options at different times. RtS uses a `$game.time` enum (EM/M/A/E/N — early morning / morning / afternoon / evening / night). When `$game.time == 'M'`, evening-only locations render with a "CLOSED — Opens at Evening" overlay. The hub passage is **one passage**; the variants are **data-driven** by `$game.time` checks against location open-hours.

The point: hubs feel different across the day **without writing four versions of the prose**.

### Pattern 3 — Stat-gated content unlocks

In RtS, `$player.scenes.HouseCleaning1.requirementsMC.corruption = 30` declares "this scene needs corruption ≥ 30 before it appears." The button only renders when the threshold is met. Same hub, new option appears on visit number whatever-it-takes. NLP uses analogous thresholds against `corrupt`, `inhib`, `allure` (NLP's `corrupt` ranges 0..178 across the explored playthrough).

The point: corruption ≥ 25 should **expose new options at the same hub**, not just shift adjectives in already-written prose.

### Pattern 4 — Anti-staleness via rotating openings

Repeatable activities in RtS visit-count to absurd numbers: Bedroom × 18, Library × 9, ParkJog × 8. They don't go stale because each visit's **opening narrative** is rolled. RtS's `BusRandomEvent` source uses `<<set $game.random to random(1,3)>>` to branch into three distinct opening blocks. NLP's Street passage was hit 46 times in our exploration playthrough. Same hub, fresh first line.

### Pattern 5 — NPC-relationship interaction shells

RtS's `MarcusBedroom` is a static menu shell with **conditionally rendered buttons**. The "Have sex with Marcus 🔥" button is wrapped in `<<if isBoyfriend("Marcus")>>`. The "Talk with Marcus 💬" button checks `!$npc.Marcus.talkedToday` for a daily cooldown. The relationship stat `$npc.Marcus.relation` gates a quest branch through a sibling passage. **Hub menu shell stays static; conditionally rendered options expose the relationship arc.**

Shady Deals reinforces the cooldown pattern with `talkedToday`-equivalent flags consumed at sleep.

### Pattern 6 — "One Return ↩️ button" loop discipline

Events end with a single Return button, side effects on exit. RtS's `ParkJog` exit:

```
<<button 'Return ↩️' 'Park'>>
    <<AddTime 2>>
    <<Energy -15>>
<</button>>
```

Time and energy cost are applied at exit, not at activity start. There is no second choice on the way out — the activity decided itself; the player gets back to the menu.

---

## §2 Vocabulary

Four terms. Used precisely from §3 onward.

**Hub canvas** 🔄 PROPOSED — A canvas whose body is *mostly a menu*. `is_repeatable = true`, fires at a location with no specific schedule (the hub itself is always available; its options vary). The body contains an `image` block, a small set of atmospheric `group`-block variants keyed on time-of-day, and an `exit_block` of type `choices` where each choice is wrapped in its own conditional group-variant. Examples-to-build: `hub_kitchen`, `hub_yard`, `hub_diner_front`, `hub_main_street`, `hub_property`.

**Event canvas** 🔄 PROPOSED — A one-shot scene. 80–250 words. Single-node. Fires once via `is_repeatable = false`, gated by flags or first-entry-after-X conditions. Real choices on exit (not "Continue"). Used for one-shot story beats: `event_first_morning_kitchen`, `event_diner_interview`, `event_jake_first_glance`. Cousin to current Phase-1 canvases B2/B6/B7-style — but cut to the bone.

**Activity canvas** ✅ WORKING — A repeatable, often-fired event. Has rotating openings (via `block_pool`) and stat-gated variant prose (via conditional `group` blocks). Already used today: `activity_sleep`, `activity_shower`, `activity_breakfast_frank`, `activity_diner_t0`. The 50 activities in `3_activities.toml` already use this shape; what's missing is the discipline 03 will spec (rotating-opening counts, rare events, escalation).

**Location** ✅ WORKING — Engine entity. 38 already exist. Hub canvases LIVE at locations. Multiple canvases (hub + events + activities) can reference the same location.

The relationship: *the location is the room; the hub canvas is the menu that renders when the player walks in; events and activities are what they pick from the menu; choices route back to the hub or onward to the next location.*

---

## §3 Decision: hub-as-convention vs hub-as-engine-entity

**The fork.** Do hubs need a new TOML table (`[[hubs]]`) and engine support, or can the hub-and-event shape ride entirely on the existing `[[canvases]]` table with naming conventions?

### Options

**(a) Convention-only.** Hub canvases are just canvases that follow a recipe. Naming convention: `hub_<location>`, `event_<scenename>`, `activity_<activityname>`. No engine change. No new schema. Validator and editor untouched.

**(b) New `[[hubs]]` table.** Engine-level entity for hubs. Changes `template_import.py`, the validator, the generator. Adds a second mental model to a codebase that currently has one.

**(c) New `is_hub = true` boolean on canvases.** Middle ground. No new table, but a dedicated flag the engine treats specially.

### Recommendation: (a) Convention-only.

Three reasons:

1. **The engine isn't broken.** The diagnosis was unambiguous. Adding engine surface to fix a content-shape problem contradicts the diagnostic frame.
2. **The patterns map cleanly onto existing primitives.** Hub menus = single-node canvases with `is_repeatable = true` and a `choices` exit. Time-of-day variants = `group` blocks gated on hour ranges or schedule triggers. Stat-gated options = wrapping each choice in its own group-variant. Rotating openings = `block_pool` (already used in `activity_sleep`). All seven explored-game patterns from §1 have a TOML translation that uses zero new primitives.
3. **Convention scales; schema breaks.** A naming convention can be adopted incrementally: 5 hubs ship, then 10, then all 12, while old single-node canvases keep working. A schema change has a cutover.

### Naming proposal 🔄 PROPOSED

- `hub_<location>` — hub canvases (`hub_kitchen`, `hub_yard`, `hub_diner_front`).
- `event_<scenename>` — one-shot story events (`event_first_morning_kitchen`, `event_diner_interview`).
- `activity_<activityname>` — repeatable activities (`activity_breakfast_frank`, `activity_diner_t0`). **Already in use today** — preserve.

Pure author-side convention. The validator ignores names. The editor ignores names. The benefit accrues to **the human reading the TOML** — when you open `2_story_canvases.toml` and see `hub_kitchen`, you know its content shape without reading.

### Cross-reference: this kills "Rule 17 exception" stacking

`content_rewrite/standards.md` Rule 17 says "player agency where it exists." The diagnosis traced "Rule 17 exception" stacking to canvases that are linear chains imitating the Prologue. With this convention, the default for a sub-Tier-A canvas is **single-node event with real choices** (or a hub fragment). The need to declare an "exception" to Rule 17 disappears because the structural alternative — long linear chain — isn't on the menu.

### Redirect-prompt

If you'd rather (b) or (c) — i.e., engine surface for hubs — say so before the worked example in §5; the hub canvas's TOML skeleton in Layer 4 changes shape if the engine learns about hubs.

---

## §4 The hub canvas in detail

The recipe and its mechanical basis. Five sub-decisions.

### 4.1 The block recipe 🔄 PROPOSED

A hub canvas's `blocks` array follows this shape:

```toml
blocks = [
  # 1. Anchor image.
  { type = "image", props = { file = "hubs/kitchen.jpg", description = "...", search_queries = [...] } },

  # 2. Time-band variants — group blocks gated on hour range / schedule.
  { type = "group", blocks = [
    { type = "paragraph", content = "[40-80w atmospheric paragraph for EM band]" }
  ], conditions = { /* hour 05:00–07:00 */ } },
  { type = "group", blocks = [
    { type = "paragraph", content = "[40-80w atmospheric paragraph for M band]" }
  ], conditions = { /* hour 07:00–09:00 */ } },
  # ... one per band ...
]

exit_block = { type = "choices", choices = [
  # 3. Each choice is wrapped in its own conditional group-variant.
  # See 4.4 — workaround for the lack of per-choice conditions.
] }
```

Why this shape: it matches the verified pattern in `activity_breakfast_frank` (which has image + universal geometry paragraph + 4 conditional group blocks + single exit). The hub recipe extends that pattern by replacing the "universal geometry paragraph + state-conditional groups" with "anchor image + time-conditional groups."

### 4.2 Time-of-day banding 🔄 PROPOSED

Five-to-six bands per hub. 24-hour ranges. Engine `[[canvases.trigger.schedules]]` already uses 24-hour `start_time`/`end_time` (verified at `template_import.py` `TemplateTriggerSchedule` dataclass). For hub canvases, the schedules go on individual group-block conditions, not on the canvas trigger itself — the hub canvas always fires when the player enters the location; the **content** is what varies.

Recommended kitchen banding (worked in §5):

| Band | Hours | Character |
|---|---|---|
| EM | 05:00–07:00 | Diana alone — coffee, the obituaries page |
| M | 07:00–09:00 | Frank + Diana morning, breakfast hand-off |
| MID | 09:00–17:00 | Empty — sketchbook on the table, stillness |
| DINPREP | 17:00–18:30 | Diana cooking, Frank sometimes |
| DIN | 18:30–19:30 | Full family table |
| LATE | 20:00–23:00 | Empty / Jake foraging / late corruption encounters |

How many bands a hub needs is a per-hub call; six is the suggested ceiling. `loc_diner_front` may need more (open hours have texture); `loc_creek` may need only two (day/night).

Further intra-band variety (same band, multiple openings rotating across visits) is `block_pool` territory. 🔒 DEFERRED to 03.

### 4.3 NPC-presence variants — load-bearing fork

**The fork.** When the kitchen at MID has Frank present (abnormal, post-Restrict declared), is the hub canvas's render different from when MID is empty?

**(a) Inline group-blocks gated on NPC presence.** The same `hub_kitchen` canvas has additional group variants whose conditions check both the time band AND the NPC's scheduled presence at the location. Single canvas per hub. Cleanly extends the recipe. **RECOMMEND.**

**(b) Parallel high-priority canvas at "kitchen with Frank present".** A separate `hub_kitchen_frank_present` canvas at higher priority that the engine fires when both the location and the NPC schedule overlap. Two canvases per hub-NPC pair. Fragmenting; the player walking into the kitchen now hits a different canvas-id depending on who's home, which complicates the menu identity.

Recommend (a). Cite the precedent: `activity_breakfast_frank` already uses `npc = "npc_frank"` on its trigger AND has multiple state-conditional variants; the hub takes the same idea and makes it the default for *any* canvas at this location.

### 4.4 Stat-gated options — the only viable workaround 🔄 PROPOSED

**The engine constraint.** Individual entries in `exit_block.choices` have no `conditions` field. Verified at `template_import.py` `TemplateChoice` schema and observed across all 79+139 existing canvases. There is no per-choice condition support.

**The workaround.** Wrap each choice in its own conditional `group`-variant **before** the exit_block. The group renders as either the choice line or empty-string. The exit_block then references the choice if present. This is the ugly part of the engine and the only way without engine change.

Practical authoring: instead of authoring 12 choices in one exit_block where some are gated, author 5–8 visible choices in the exit_block and use *separate* conditional events that route through dedicated entry conditions. The flow becomes:

- Hub menu shows ≤6 choices visible.
- "Late-night with Jake" is itself a `event_late_night_jake` canvas at the same location, gated by `corruption ≥ 50 AND clock=LATE AND jake_caught_open=true` on its **trigger conditions**, with priority high enough that when the player is in `loc_kitchen` LATE and the conditions are met, the engine fires that event canvas before the hub.

In other words: stat-gated options are not "extra buttons on the hub menu" — they are **separate event canvases** whose trigger conditions cause them to interrupt the hub render when the state qualifies. This mirrors RtS's `requirementsMC` pattern (where each scene has a requirements object) but uses the engine primitive that already exists (canvas-level trigger conditions + priority).

🔄 PROPOSED. The doc commits to this approach. 03 will spec the priority gradient.

### 4.5 Hub option count 🔄 PROPOSED

Visible options at any time: ≤6. Total option set across all states: 12–15. RtS `Hallway` shows 9 buttons; that's the upper end of comfortable. Cognitive ceiling is the hub menu — players scan, they don't read.

---

## §5 Worked example: `loc_kitchen`

The centerpiece. Four layers.

### Layer 1 — Current-state diagnosis

`loc_kitchen` is one of TLS's most-touched locations. Today its content lives across **at least eight canvases**:

- `first_morning_kitchen` (B2) — 700w single-node story canvas. Fires on first kitchen entry after `arrived_at_franks`. Frank's rent terms + Diana's coffee + the church-or-stay choice. Two-choice exit.
- `town_walk_day_two` N1 (B5 sub-node) — ~400w "kitchen" sub-node where Diana describes the route to town. Single-"Continue" exit to the walk sub-node.
- `pass_the_salt` (B19 destination) — short cross-NPC dinner-table beat.
- `activity_breakfast_frank` — Mon–Fri 06:30–07:30, 4 state-conditional variants (DEFAULT/WITHDRAWN/WARM/CONSEQUENCE), Frank-arc gated.
- `activity_cook_dinner_frank` — Mon–Fri 17:30–18:30, 4 variants, Frank-trust gated.
- `activity_cook_solo` — solo cooking, schedule unbound.
- `activity_eat_fridge` — quick low-energy refuel.
- `activity_family_dinner` — 18:30–19:30 Mon–Fri, four-NPC dinner.

Plus implicit kitchen presence in B14 (`frank_phase_a_test`'s "Correction" node, currently misfiring with the porch-light hallucination flagged in `under_one_roof/issue.md`), B6 setup beats, and several Diana ambient interactions.

**Observation.** The kitchen already has the data-shape of a hub: many canvases, time-banded, NPC-presence-banded, stat-banded. They're just authored as **eight separate canvases that don't know about each other**, each with its own description, its own exit, its own duplicate atmospheric setup. There's no "the kitchen at MID with no one home" canvas — there's a gap. There's also no menu — when the player enters `loc_kitchen` at 11am with `arrived_at_franks` true, the engine has no canvas to fire and either falls through to a generic location render or surfaces a too-broad activity.

The hub is implicit in the data already. Phase 2 makes it explicit.

### Layer 2 — The redesigned hub

`hub_kitchen` is one canvas. Its body renders as menu. Its content varies along three axes:

**Schedule axis.** Six time bands as in §4.2:
- **EM (05:00–07:00)** — Diana alone, the percolator on, the obituaries folded. The kitchen is Diana's; Maya entering at this hour is entering Diana's space. Atmospheric paragraph foregrounds Diana's morning ritual without putting words in Diana's mouth. 60–80 words.
- **M (07:00–09:00)** — Frank at the table with the paper, Diana at the stove with bacon on. The five-chairs-at-four-person table. 60–80 words.
- **MID (09:00–17:00)** — Empty. Light through the window. The chipped Hayes Hardware mug on the drying rack. The fan moving the heat. The kitchen as a room Maya has the run of. 50–60 words.
- **DINPREP (17:00–18:30)** — Diana cooking. The basil cut and waiting on the board. Frank's truck not back yet. 60–80 words.
- **DIN (18:30–19:30)** — Five chairs filled. Activity-level engagement; the hub-itself probably routes mostly to `activity_family_dinner` and family-dinner-adjacent events. 60–80 words.
- **LATE (20:00–23:00)** — Empty most days; Jake foraging some nights; a register-shift at high corruption. 60–80 words.

**NPC-presence axis.** Drawn from `book_phases/2b_systems_budget.md` (kitchen-at-six-thirty is Diana's; cook dinner Mon-Fri is Frank's prep window) and from existing activity schedules:
- Diana scheduled at kitchen EM, DINPREP, DIN.
- Frank scheduled at M (breakfast), DINPREP-with-Diana on cook nights, DIN.
- Jake — no scheduled presence; appears at LATE only when `jake_caught_open = true` AND the late-corruption flag.
- Ryan — no scheduled kitchen presence (he's the yard).

**Stat-gate axis.** Examples (concrete, not exhaustive):
- "Sit with Diana" deepens at `diana_awareness ≥ 30`. Below that, the option label is "Pass through" or absent; above, it surfaces.
- "Late-night kitchen" appears only when `corruption ≥ 50 AND clock=LATE`. Below those, the late-night menu is "Glass of water. Bed." and nothing else.
- "Steal twenty from the till on the counter" 🔒 (a hypothetical option, deferred to 03 as an example) appears at `corruption ≥ 75 AND money < 60 AND day_of_week = saturday` — the rent-week saturday scarcity gate.

The hub menu's footprint stays small (≤6 options visible) but the option *set* differs per state. A first-week MID visit shows: `[Sketch on the table]` `[Make coffee]` `[Eat from the fridge]` `[Step out the back door]`. A week-six DIN visit shows: `[Sit at the table]` `[Help Diana plate]` `[Step out the back door]`. A week-twelve LATE visit at corruption 60 shows: `[Glass of water]` `[Sketch at the table]` `[Foraging — Jake's already here]`.

### Layer 3 — How `first_morning_kitchen` collapses — load-bearing fork

`first_morning_kitchen` is currently 700 words single-node with rent terms + church choice. In the hub model, it doesn't exist as itself.

**(a) One-shot priority event routed through the hub.** RECOMMEND. Hub renders as menu. A high-priority canvas `event_first_morning_kitchen` exists, gated on first `loc_kitchen` entry after `arrived_at_franks`. It fires once, ~150 words, single-node, with the **load-bearing dialog beats only**: Frank's rent sentence ("Maya. Rent's sixty a week, due Sundays."), Diana's "Sit.", the church-or-stay choice. Real two-choice exit. Sets `first_morning_kitchen_done`. After it fires, the kitchen reverts to standard hub behavior; revisits route to `activity_breakfast_frank` if it's M band. The remaining 550 words of current prose either move to atmospheric color in `event_arrival_at_franks` (the porch and hallway already establish the house geometry) or are cut. Closer to NLP pattern (sparse one-shots punctuating a sandbox).

**(b) Dissolution into 2–3 micro-events.** REJECT. Three separate one-shot events: `event_cook_with_diana_first_time` (rent terms), `event_breakfast_with_frank_first_time` (church choice), `event_morning_at_kitchen_first` (atmosphere). 80–120w each. Closer to RtS pattern (many small events). Reject because the first morning is dramatically singular — fragmenting it into three triggers means the player doesn't get the unified beat of "Frank set the rent terms and asked the church question in the same conversation," which is the canon shape from `final_book.md`.

**Redirect-prompt.** If you prefer (b), the hub recipe doesn't change but the event canvases multiply by ~3×. If you'd prefer to keep the current 700-word single-node `first_morning_kitchen` exactly as it is and just make the *rest* of the kitchen content hub-shaped, that's a third option (c) — which would mean the worked example becomes "the kitchen has one preserved Tier-A canvas + a hub for everything else." That's a viable hybrid; flag if you want it.

### Layer 4 — Render-time skeleton

Schematic only. ~30 lines of TOML pseudocode showing the recipe with placeholders for prose:

```toml
[[canvases]]
id = "hub_kitchen"
name = "Kitchen"
description = "Kitchen hub. Renders the menu of options at loc_kitchen, varying by time band and stat state."

[canvases.trigger]
location = "loc_kitchen"
is_repeatable = true
priority = 1                    # Hub priority — events at 5+, one-shots at 10
is_active = true
conditions = { version = "1.0", items = [
  { type = "flag", subject = "player", flag_key = "arrived_at_franks", operator = "is_true" }
] }

[[canvases.nodes]]
id = "base"
blocks = [
  { type = "image", props = { file = "hubs/kitchen.jpg", description = "...", search_queries = [...] } },

  # Time-band variants — schedule-condition-gated group blocks.
  { type = "group", blocks = [
    { type = "paragraph", content = "[EM atmospheric paragraph — Diana alone]" }
  ], conditions = { /* engine hour-range check 05:00–07:00 */ } },
  { type = "group", blocks = [
    { type = "paragraph", content = "[M atmospheric paragraph — Frank + Diana]" }
  ], conditions = { /* hour 07:00–09:00 */ } },
  # ... MID, DINPREP, DIN, LATE bands ...
]

# Hub options — each visible choice mapped to either a route to an activity/event canvas
# or a navigation to another location. Stat-gated extras are NOT in this exit_block;
# they are separate canvases at higher priority that interrupt the hub render when their
# trigger conditions are met (per §4.4).
exit_block = { type = "choices", choices = [
  { text = "Sketch on the table", targetType = "trigger", time_progression_minutes = 30, ... },
  { text = "Eat from the fridge", targetType = "specific", canvasId = "activity_eat_fridge", ... },
  { text = "Step out the back door", targetType = "location", locationId = "loc_yard", ... },
  # ... 3-5 more options ...
] }
```

The schematic is enough to make the convention legible. Per-band prose, per-state choice details, and the precise schedule-gate-syntax-on-group-conditions (which the engine may or may not support directly — verify in 03) are 03 territory.

---

## §6 How story canvases relate to the hub model

The 28 Phase-1 story canvases (B1–B28) translate into the hub model via three dispositions. 04 will assign each canvas to one of these.

**Pattern α — story canvas becomes a one-shot priority event.** The canvas survives but shrinks. Rewritten as ~150-word single-node event canvas, gated on first-entry-after-X conditions, routed through a hub. `first_morning_kitchen` is the canonical α case.

**Pattern β — story canvas dissolves into hub-content variants.** The canvas disappears as a discrete entity; its content moves into atmospheric variants on the relevant hubs. `town_walk_day_two`'s three sub-nodes (`kitchen` / `walk` / `diner`) plausibly dissolve into: a MID-band variant on `hub_kitchen` (route advice from Diana), a one-shot atmospheric event for first-walk-to-town (cut to ~80 words), and the diner-arrival becomes `event_diner_first_visit` routed through `hub_diner_front`. The current B5 canvas-id stops existing.

**Pattern γ — story canvas stays a multi-node Tier-A canvas.** The Cracks. The Prologue. The Beach proposal. These genuinely earn their length and their multi-node structure. Don't touch in Phase 2 except to confirm they still trigger correctly under the new hub model.

A canvas's disposition depends on its **dramatic load** (does this beat carry irreplaceable plot weight that cannot live as menu-color?) and its **agency shape** (does the player make a real decision here?). 04 will publish the per-canvas disposition matrix.

---

## §7 What 02 commits to / defers to 03 / defers to 04

Cross-doc contract.

### 02 commits to 🔄 PROPOSED (in this doc, pending user approval):

- **Vocabulary** — hub canvas / event canvas / activity canvas / location.
- **Naming convention** — `hub_<location>` / `event_<scenename>` / `activity_<activityname>`.
- **Hub recipe** — image + time-band group variants + conditional choices in exit_block. ≤6 visible options.
- **`first_morning_kitchen` disposition** — Pattern α (one-shot priority event routed through `hub_kitchen`).
- **Convention-only architecture** — no engine change.
- **α/β/γ disposition framework** for the 28 Phase-1 story canvases.
- **Stat-gated options as separate canvases** — gated extras live as their own event canvases at higher priority, not as choices in the hub's exit_block.

### 02 defers to 03 (Activity Loop Spec):

- Rotating-opening counts per tier (3 for E, 4 for F, etc.).
- Rare-event injection: probabilities, one-shot vs. evergreen rares, authoring as separate canvases.
- NPC repeatable-interaction cooldowns (the `talked_to_X_today` flag pattern, reset at sleep).
- Stat-gated escalation tiers — the actual rule for "when does a new option appear at the same hub" with priority gradients.
- Energy / time / stat budgets per activity tier.
- The 50-activity inventory walk: which existing activities are healthy, which need rewriting, which are missing.
- Whether time-band variants are written as one paragraph or `block_pool` of 3–5.

### 02 defers to 04 (Story-to-Event Translation):

- Per-canvas disposition for B1–B28.
- The full α/β/γ matrix.
- Migration order (which 5 canvases get rewritten first).
- Prose-cut budget per canvas (compression ratio, expected ~3:1 across Phase 1).
- Done-criteria for the migration.

---

## §8 Open questions / redirect prompts

Things 02 deliberately did not decide. Pick any of these and we go deeper:

- **Hub canvas explicit "leave this location" exit choice** vs. trusting the engine's location-graph to handle navigation between hubs. (Affects whether every hub menu shows "[Step out the back door]" or whether navigation lives elsewhere in the UI.)
- **Priority gradient.** Hub at priority 1, event at priority 5, one-shot priority event at priority 10 — is this right? Or do we need finer bands (e.g., 1 / 3 / 5 / 8 / 10)?
- **Diner-front + diner-back-booth.** Both get hub canvases or only the front? Back-booth is a corruption-gated extension; arguably it's an *event* surface, not a hub.
- **`loc_main_street` shape.** Main Street is breadth (multiple businesses on three blocks) more than depth (no NPCs scheduled there as default). Does it follow the same recipe or a wider-menu variant?
- **Pattern γ scope.** Are Tier-A Cracks the *only* canvases that stay multi-node, or do some Tier-B chapter milestones (e.g., the diner-tier escalation Crack-adjacents) also earn it?
- **`first_morning_kitchen` Layer 3 option (c).** Hybrid: keep the current 700-word canvas as a frozen Tier-A and hub everything else. Did I underweight this option?

---

## §9 Summary table

| # | Proposal | Status | Decision lives in |
|---|----------|--------|-------------------|
| 1 | Hub canvas = convention, not engine entity | 🔄 PROPOSED | 02 §3 |
| 2 | Naming: `hub_*` / `event_*` / `activity_*` | 🔄 PROPOSED | 02 §3 |
| 3 | Hub recipe: image + time-band groups + conditional choices | 🔄 PROPOSED | 02 §4 |
| 4 | Stat-gated options as separate priority-gated canvases | 🔄 PROPOSED | 02 §4.4 |
| 5 | `first_morning_kitchen` → α one-shot priority event | 🔄 PROPOSED | 02 §5 Layer 3 |
| 6 | α/β/γ disposition framework | 🔄 PROPOSED | 02 §6, applied in 04 |
| 7 | Rotating-opening counts / rare events / cooldowns | 🔒 DEFERRED | 03 |
| 8 | Per-canvas disposition for B1–B28 | 🔒 DEFERRED | 04 |
| 9 | Activity canvases (existing pattern) | ✅ WORKING | already shipped |
| 10 | Locations (engine entity) | ✅ WORKING | engine |

---

*End of 02. Next: 03 — Activity Loop Spec — only after 02 is approved or redirected.*
