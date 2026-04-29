# 01 — Repeatable-First Doctrine

> **Created 2026-04-29.**
> Sets the vocabulary and frame every other Phase 2 redesign doc inherits.
> Successor in spirit to `00_TLS_Phase2_Diagnosis_and_Direction.md` — diagnosis identifies the problem; this doc names the fix.

---

## Thesis

**Phase 2 is a state machine, not a novel.**

Phase 1 was authored as a sequence of plot beats — separate canvases for first morning, the catch, the restrict declaration, the first tease. Each beat got its own non-repeatable canvas, and the player's job was to walk through them in order. That is novelistic thinking dressed in canvas vocabulary, and it produces what the diagnosis calls "novel-prose pretending to be a game."

The fix is to invert the relationship between content and state. **Stop writing scenes that fire once and end. Start writing scenes that fire many times and read differently each visit because the player's state moved in between.** Story advancement happens because flags flipped, not because a new canvas got triggered.

Once that flip is internalized, three consequences follow, and they're the spine of every other doc in this set.

---

## The three-layer model

Drawn directly from the Road-to-Success live recon (2026-04-29). RtS is the proof: 358 passages, no separate "story arc" content track, every passage tagged by location (`kitchen-background`, `bathroom-background`, `Casa`, `vipers-background`) — none tagged `story` / `cutscene` / `event` / `oneshot`. Plot, dialogue, character development, and even major milestones (graduation, gang initiation, prison route) all live as flag-gated branches inside repeatable shells.

The shape is three layers, all repeatable:

| Layer | What it is | What it carries | Rough size |
|---|---|---|---|
| **Hub** | Location menu | Buttons, no prose | 50–350 chars |
| **Activity router** | Thin probability + state gate | One sentence fallback + `<<goto>>` rules | ~1000–1500 chars |
| **Scene** | Where the prose lives | Stage-gated branches + linkreplace cascades + dialogue | 3000–8000 chars |

A click flows hub → router → scene. The hub renders every visit; the router evaluates state and dispatches; the scene's internal cascade picks a branch by stage flag and reveals beats. After exit, time advances, energy decrements, the player returns to the hub. The next click might land on a different branch of the same scene because a flag flipped.

**The five object types from the master spec (`archive_02_TLS_Rewrite_Spec_2026-04-29.md` §2) all map onto this model:**

- Hub canvas = layer 1
- State-pump button = layer 1, button-shaped
- Activity canvas = layer 2 (when it dispatches) or layer 3 (when it carries content)
- Scene canvas = layer 3
- Event canvas = layer 3 with a one-shot guard (rare; see §"When to use a true one-shot")

Object types remain valid vocabulary. This doctrine doesn't replace them — it reframes them. Layers and stages are *what moves*. Object types are *the shells movement happens inside*.

---

## Why repeatable shells beat one-shot chains

Three reasons, in order of weight.

**1. Replayability is the engine.** RtS's most-visited passages (`Center` 21 visits, `Library` 14, `RestaurantWork` 11, `ParkJog` 8, `LibraryExhibitionism` 7) are all repeatable activities. The player lives in the loop. A one-shot chain is consumed once and never returns; a repeatable scene with five stage branches generates effective novelty across dozens of visits at the source weight of one canvas. Inventory shrinks, repeat-value multiplies.

**2. Flags do the narrative work, not prose.** Once content lives inside repeatable shells, advancement is communicated by what the player sees *change* between visits — a new button at the kitchen hub after `frank.trust >= 20`, a new stage branch in the office scene after `frank_caught` flips, a tone shift in the post-Restrict register. The system tracks; the prose stays terse. Phase 1's pattern of carrying every relationship change in 700-word literary narration is exactly the load-bearing failure the diagnosis identified.

**3. Author drift is bounded.** A 100-word repeatable scene per stage requires the author to hold voice for 100 words at a time. A 700-word linear novella requires the author to hold voice for 700 words at a time, and that's where the count-percolators-ticked-at-when monotonic tic took over Phase 1. **Length is the variance multiplier on voice drift.** Short scenes are controllable. Long scenes drift.

---

## The "same passage, different stage" principle

This is the single most important pattern to internalize. It's the entire shape of how RtS tells a story.

The same canvas fires on the player's first visit, fifth visit, and twentieth visit. The internal cascade evaluates stage flags and picks a different branch each time. The player sees a different scene because state moved, not because the engine routed them somewhere new.

Doctrine implication: **plot beats are not canvases. Plot beats are stage transitions.** When the design book says "Frank crosses a line at the catch event," the engine implementation is not "fire `event_frank_catch`" — it's "the conditions for `frank_caught` clear inside the living-room hub's evening branch, the branch fires its one-time block (gated by `frank_caught == false`), and on exit it sets `frank_caught = true` so subsequent visits route to a different branch."

The catch lives inside the living-room hub. Not as its own canvas. The next time the player enters the living room, the catch branch doesn't show; new content shows because the flag is set. **The same passage. A different stage.**

---

## When to use a true one-shot

A non-repeatable canvas (`is_repeatable = false`) is reserved for content that has no meaningful "next visit" semantics — biological transitions, terminal arc beats, summer's end. The decision tree:

```
Could this content fire more than once if the player returned?
├── Yes (or "the second visit shows something different")
│   → Repeatable canvas with stage-gated cascade.
│   → The "first time" content is a flag-gated branch inside.
│
└── No (the moment is genuinely terminal)
    │
    Is the moment a single transition that closes a track?
    ├── Pregnancy → birth, eviction, summer end, arc terminal beat
    │   → True one-shot, is_repeatable = false.
    │
    └── A "first time you do X" beat
        → NOT a true one-shot. Use a flag-gated branch inside the
          repeatable shell that handles X. Set the flag on exit
          so subsequent visits route elsewhere.
```

The full list of true one-shots for TLS Phase 2 will be enumerated in `06_One_Shot_Inventory.md` (deferred). Working estimate: birth, abortion, summer-end departure, possibly Frank's terminal beat. Single-digit count, total. **If a list of one-shots gets longer than ten items, the doctrine has been violated and most of those items should fold into repeatable scene cascades.**

---

## Worked example — `kitchen_with_frank`

A single transition (Frank's first kitchen encounter, then the early-warmth tier) shown two ways. Same prose surface; different control flow.

### Phase 1 framing (what we're moving away from)

```
event_frank_kitchen_first_morning
  is_repeatable = false
  priority = 10
  conditions = [first_morning_kitchen_done = false]
  body: 700 words establishing the kitchen, Frank's morning paper, rent terms.
  on_exit: first_morning_kitchen_done = true

activity_breakfast_with_frank
  is_repeatable = true
  body: 540 words of WARM/WITHDRAWN/CONSEQUENCE prose variants.

event_frank_offers_bookkeeping
  is_repeatable = false
  priority = 9
  conditions = [frank.trust >= 20, bookkeeping_offered = false]
  body: 400 words of him noticing she's careful with numbers.
  on_exit: bookkeeping_offered = true
```

Three canvases. Two of them fire once and never return. The third carries the daily texture but doesn't advance the arc — that's the job of the one-shot canvases. Plot is a chain of one-shot firings. The arc is a script the player walks through.

### Phase 2 framing (the doctrine)

```
hub_kitchen
  is_repeatable = true
  body: title + image + button menu

  buttons (visible per state):
    "Cook 🍳"           — always
    "Eat from fridge 🍽️" — always
    "Wash dishes 🫧"    — always
    "Talk with Frank 💬" — when frank_present_via_schedule()
                          AND talked_to_frank_today == false
    "Help with bookkeeping" — when frank_stage >= 1 AND ...
    "Hallway 🚪"        — always

scene_kitchen_with_frank          (the cascade lives here)
  is_repeatable = true
  trigger.chance = 0.25            (1-in-4 mornings: ambient Frank beat)
  conditions = [frank_present_via_schedule(), time_band in [M, DINPREP]]

  cascade (illustrative TOML — schema PR will finalize field names):
    if frank_stage == 0:
        80–120 words: he's at the table, paper, terse exchange.
        +1 frank.trust on exit.
        if bond_count >= N (counter): set frank_stage = 1.
    elif frank_stage == 1:
        80–120 words: he asks if she's any good with numbers.
        offers bookkeeping. choice sets bookkeeping_unlocked.
    elif frank_stage == 2:
        80–120 words: post-Restrict register. supervised tone.
    elif frank_stage == 3:
        100–150 words: Crack-adjacent register.
```

One hub. One scene canvas. The "first morning" content is the `frank_stage == 0` branch on the first time the scene fires. The bookkeeping offer is the `frank_stage == 1` branch on whichever visit the gate clears. The post-Restrict register is the `frank_stage == 2` branch on every subsequent visit until the next stage. **Three "scenes" of plot worth from one repeatable canvas at a fraction of the source weight.**

The contrast is not about prose quality. The same words could be authored either way. The contrast is about *what gets re-entered*. Phase 1's three canvases each get walked through once. Phase 2's one canvas gets re-entered every morning Frank is in the kitchen, and it reads differently as Maya's state with him changes.

---

## Anti-patterns being deleted

These are the Phase 1 reflexes the doctrine forbids. When a draft canvas matches one of these patterns, rewrite it as a stage-gated branch inside a repeatable shell.

1. **The "establishment scene."** Three sub-nodes of "Continue / Continue / Continue" walking the player through atmosphere. Banned outside the Prologue and Tier-A Cracks. A single moment is one node. Atmospheric setup is a hub's image + a 50-character title.

2. **The one-shot story canvas chain.** A `frank_*` arc consisting of `event_frank_meet` → `event_frank_offers_books` → `event_frank_catch` → `event_frank_restrict` → `event_frank_first_tease` → `event_frank_crack`. Six canvases that each fire once. Phase 2 collapses this to three or four repeatable shells (kitchen scene, office scene, living-room hub branch) with stage-gated branches inside. The catch is a branch, not a canvas.

3. **The activity that doesn't advance state.** Activities whose only effect is +1 trust and time progression. If a repeatable activity isn't either (a) advancing a counter that gates a stage transition somewhere or (b) producing income/energy/hygiene, it's decoration and shouldn't exist.

4. **The flag without a payoff.** A flag set somewhere that no scene reads. Phase 1 has many of these from rewrites that referenced future canvases that never arrived. Every flag needs a consumer; every set has a check. A "fiction debt" flag with no payoff gets deleted from the design.

5. **Story arc as plot driver.** The `[story_arc]` table currently uses `linked_canvas` to chain milestone canvases. In Phase 2 the table becomes a journal display layer (full spec deferred to `07_Journal_Display_Spec.md`). It reads flags, never writes them. It does not gate content.

6. **Prose carrying state.** A scene whose only signal that "Maya has changed" is a paragraph of literary narration about her noticing she's different. The signal is the new button at the hub, the new branch in the cascade, the corruption number on the sidebar. Prose registers the moment; the system carries the change.

7. **The "Rule 17 exception."** When a canvas needs an exception declaration to justify its single-Continue chain, it's not an exception — the doctrine has been violated. Rewrite as a single node or as a hub-event split.

---

## Doctrine checklist for every new canvas

Before authoring any canvas in Phase 2, the author answers:

1. **Is `is_repeatable = true`?** If no, justify against the one-shot decision tree. Default is yes.
2. **What stage flag(s) does this canvas read?** Name them. If none, justify (probably a hub or a true ambient activity).
3. **What stage flag(s) or counters does this canvas write?** Name them. If none, justify (probably a hub).
4. **If a flag is read, where does it get set?** Cite the canvas. If the answer is "a future one-shot canvas we'll write later," stop — refactor that one-shot into a flag-gated branch inside an existing repeatable shell.
5. **What happens on the next visit?** If the answer is "the canvas wouldn't fire again because of `is_repeatable = false`," see #1. If the answer is "the same content fires," see #3 — it's not advancing anything.
6. **Density target.** Hub ≤300 chars body. Activity 30–80 words per arc-state. Event 80–250 words. Scene 80–400 words across all reveals. State-pump toast 8–20 words.
7. **Image search queries.** 3–5 per image block (see master spec §2.4). Image rotation is the verified RtS variety mechanism; prose-pool rotation is not.

A canvas that can't answer 1–5 cleanly doesn't ship.

---

## Vocabulary lock

Terms used identically across `02_NPC_Stage_Chains.md`, `04_Scene_Cascade_Pattern.md`, and forward to 05/06/07:

- **Repeatable canvas.** `is_repeatable = true`. Default for Phase 2.
- **One-shot canvas.** `is_repeatable = false`. Rare; see decision tree.
- **Hub.** A repeatable canvas at a location whose body is a button menu. Three sub-types per master spec §2.1: Type-A shared, Type-B NPC personal, Type-C outdoor/city.
- **Scene.** A repeatable canvas where prose lives, with internal stage-gated branches.
- **Activity router.** A repeatable canvas that exists to dispatch (`<<goto>>`-equivalent) to scene canvases based on probability + presence + stage gates. Thin; ~1000–1500 chars.
- **Stage.** A named position in an NPC's arc, expressed as a flag (illustrative: `frank_stage = 0..N`). Defined in `02_NPC_Stage_Chains.md`.
- **State-pump button.** A choice on a hub that fires effects + toast and re-renders the hub. No transition.
- **Cascade.** The internal `<<if stage_X>>` branching inside a scene canvas. Subject of `04_Scene_Cascade_Pattern.md`.
- **Stage advancement.** The act of flipping a stage flag. Happens from inside a scene's effects, not from a separate "advance the plot" canvas.

---

## Cross-references

- **`02_NPC_Stage_Chains.md`** — defines the stage flags (`frank_stage`, etc.) every cascade reads.
- **`04_Scene_Cascade_Pattern.md`** — shows the canonical cascade implementation; `kitchen_with_frank` walked in full.
- **`06_One_Shot_Inventory.md`** (deferred) — enumerates the small set of true one-shots.
- **`07_Journal_Display_Spec.md`** (deferred) — the journal's repurposing as flag-driven display.
- **`archive_02_TLS_Rewrite_Spec_2026-04-29.md` §1, §2, §10** — verified RtS reference patterns, object-type definitions, voice register rule.
- **`00_TLS_Phase2_Diagnosis_and_Direction.md`** — diagnosis this doctrine is the corrective for.

---

## What this doc is not

It is not the implementation. It is not a TOML schema spec — TOML field names appearing in examples are illustrative; the schema PR finalizes them. It is not the inventory of canvases. It is not the voice rule (master spec §10 covers register).

It is the frame. Every other doc in the Phase 2 redesign set inherits the vocabulary and the doctrine checklist defined here.
