# 47 — Quests Page Unified Card Design (Capstones + Pure Mechanics)

**Session date:** 2026-05-23
**Status:** Analysis + Design proposal (not yet a PRD — engine option deferred)
**Authoring context:** ENI session with LO, opened from the observation that Frank's block isn't showing on the TLS test game's Quests page
**Scope:** Read-only analysis + design rule; no engine work or TOML changes made in this session
**One-line conclusion:** Every Quests card, across capstone arcs and pure-mechanic arcs alike, follows one shape — a Maya-voice line + an engine-rendered next-goal block. The card's *frame* shifts as state changes (🎯 bullets / 🔓 Ready+📍+🕒 / ✓ Complete) while the narrative text swaps via the picker. The full design works on the current engine except for one missing piece: live trait/counter progress bullets for templates without a stage helper.

---

## §1 Why this exists

This doc was written because the design conversation that produced it touched almost every part of the Phase 2 redesign at once, and the conclusions are too load-bearing to leave scattered in a chat log. Future sessions need a single place to land.

### The trigger

LO opened the session with one observation: in the TLS test game (`games/the_long_summer_test/`), the Quests page doesn't show a Frank block at all on a fresh playthrough. Ryan and Jake show up from Day 1; Frank stays silent until the catch fires somewhere around Day 5–7. That asymmetry didn't match the Phase E plan's promise of a "3-quest journal."

### What the trace expanded into

Tracing why Frank was silent led through:

1. The hint templates section of `7_final_game.toml` (the 2026-05-11 RTS-shape conversion's after-effects)
2. The hint picker (`getStageHintForNPC` in `v2.py`) and why it returns `null` pre-catch
3. The auto-goal renderer (`computeHintGoal`) and its five rendering paths
4. The Frank arc design brief (doc 31 §3-§6) — what progression actually *is* for him
5. The full enumeration of player states for any arc NPC, capstone-driven or pure-mechanic
6. The engine's current support matrix against that enumeration

### Docs and memories this inherits from

| Reference | What it locks |
|---|---|
| Doc 24 — RTS Three Lanes | The Lane 1/2/3 model that frames how NPC content fires |
| Doc 30 — TLS Test Redesign PRD | The slice's overall E-track design, including the "3-quest journal" promise |
| Doc 31 — Frank Arc Design Brief | The 6-tier ladder + 5 capstones + lane-by-lane content map |
| Doc 34 — Engine PRD Phase E Additions | Engine work that landed for Phase E (hint authoring fields, closure flag, etc.) |
| Doc 35 — RTS state-variant + authored-vs-mechanism doctrine | Why "RTS variant-ROUTES content on persistent states" — informs the picker-swap doctrine |
| Doc 11 — Hint Authoring Guide | The current author-facing reference for hints; this doc supersedes its conclusions where they conflict |
| `feedback_hint_narrative_no_time_or_location` | Maya-voice text fields stay in character; mechanical info lives in the auto-rendered block |
| `feedback_tls_scene_body_style` | Scene bodies are RTS-flat, but Quests cards have their own voice rules (this doc) |
| `feedback_rts_objective_quest_doctrine` | One-RTS-directive sentence per Story-Goals card; no chore-gated derivation |

---

## §2 Frank's progression system, in plain words

The model the rest of the doc reasons against. Pulled from doc 31 §3-§6 verbatim with no reinterpretation.

### The 6-tier ladder

| Tier | Maya corruption | Capstone gate | Content type |
|---|---|---|---|
| 0 | 0+ | none | Brushed contact / accidental |
| 1 | 5+ | none | Tease / flash (visual only) |
| 2 | 15+ | none | Fondle / clothed grope |
| 3 | 25+ | post-catch (`frank_caught`) | Explicit oral / partial sex |
| 4 | 35+ | post-cracked (`frank_cracked`) | Full sex |
| 5 | 50+ | post-first-night (`frank_first_night_done`) | Routine / sleep-over / breeding |

**Three observations:**
- Tiers 0/1/2 are **pure-stat** — corruption climbs, new content opens silently. No scripted scene fires.
- Tiers 3/4/5 each require **both** a corruption number **and** a capstone flag. The capstone is a scripted moment.
- Frank's arc is therefore *capstone-dense*. Every meaningful jump past T2 has a scripted moment we can point at.

### The 5 capstones

| # | Capstone | Trigger | Sets |
|---|---|---|---|
| 1 | **Catch** | Auto — living room, weekday 20:00–22:30, corr ≥ 25, frank_caught false | `frank_caught` + `frank_restrict_declared` |
| 2 | **Declaration** | Auto — next evening encounter after corr ≥ 35 + frank_caught | `frank_cracked` |
| 3 | **First-night** | Player-initiated — bedroom hub, post-cracked, corr ≥ 35 | `frank_first_night_done` |
| 4 | **Sleep-over** | Player-initiated — bedroom hub, post-first-night, corr ≥ 50 | `frank_sleepover_done` |
| 5 | **Diana confrontation** | Auto — `diana_awareness ≥ 8` + frank_first_night_done | `diana_confronted` + branch outcome |

### The 3-lane content system

Per doc 24, every location/time slot where Frank is scheduled has three lanes of content firing in parallel:

- **Lane 1** — the hub. Maya clicks an action ("Lean against the counter near him"). Choice-driven.
- **Lane 2** — ambient encounters. When Maya enters the room, dice roll for a random Frank moment ("happens to brush past"). Chance-driven.
- **Lane 3** — substitution. When Maya does a solo activity in Frank's zone (read on couch, shower), dice roll to "hijack" the scene — Frank joins her.

### Where Frank is scheduled

| Location | Window |
|---|---|
| Kitchen — morning | 05:30–09:00 daily |
| Kitchen — dinner prep | 17:00–19:30 weekdays |
| Living room — evening | 19:30–21:00 weekdays |
| Yard — afternoon | 14:00–17:00 daily |
| His bedroom — winding down | 21:00–23:00 weekdays |

### What "progress" actually means for Frank

The player isn't pursuing a checklist. They're choosing **where Maya spends her day**. The 3-lane system drips small amounts of corruption (and Frank's trust/arousal) onto every successful encounter. The capstones land on top of that flow when conditions are right.

> Corruption is a slow-climbing thermometer fed by ambient interaction across 4 locations × 3 lanes. Capstones are 5 scripted gates that the corruption thermometer triggers (auto) or that the player walks into (hub menu).

---

## §3 Why Frank's Quests block is silent pre-catch

Mechanical trace, not opinion.

### The TOML state today

In `games/the_long_summer_test/toml_phases/7_final_game.toml:2604-2632`, Frank has exactly two hint templates:

| # | Condition | text | Renders via |
|---|---|---|---|
| 1 | `frank_caught is_true` **AND** `frank_bedroom_first_done is_false` | *"Upstairs now. The office stays for the books."* | `arc_closure_flag = "frank_bedroom_first_done"` → Path B (🔓 Ready) |
| 2 | `frank_caught is_true` **AND** `frank_bedroom_first_done is_true` | *"He moved the line. The bedroom is the venue now."* | `arc_complete = true` → Path C (✓ Arc complete) |

**Both templates require `frank_caught` to be true.** Before that flag flips (i.e. before the catch fires somewhere around Day 5–7), neither template matches.

### The picker behavior

`setup.getStageHintForNPC("npc_frank")` in `apps/game_generation/twee_comprehensive/generators/v2.py:5648` walks all templates with `npc_id == "npc_frank"`, evaluates each one's `condition_items`, and returns the winning one. When zero templates match, it returns `null`.

### The QuestsPage suppression

The QuestsPage passage in `v2.py:16067-16101` iterates NPCs and only emits the `<div class="npc-section">` block when the picker returns non-null:

```
<<set _hint = _slug ? setup.getStageHintForNPC(_slug) : null>>
<<if _hint>>
  <div class="npc-section">
    ...
  </div>
<</if>>
```

So when Frank's picker returns `null` pre-catch, **no section is rendered at all**. Ryan and Jake have Stage 0 templates whose conditions match the starting state, so their picker returns a winning template from Day 1 and their sections render.

### Root cause

This is a 2026-05-11 RTS-shape conversion side-effect (memory: `frank_rts_shape_pass1`). The conversion retired:

- `npc_frank_stage` integer variable (master stage trait)
- `frank_stage_1/3/4` helpers (`engine.stage_helpers` entries)
- Pre-catch hint templates that depended on `stage_npc/stage_value = npc_frank/0..3`

Cited in the TOML at lines 107-110:
> *"Frank stage helpers (frank_stage_1 / _3 / _4) removed 2026-05-11 — Frank → RTS-shape conversion. `npc_frank_stage` master variable deprecated; canvases now gate on capstone narrative flags + stat thresholds directly per the RTS-pure pattern. No master-stage helpers needed."*

And at lines 2587-2590:
> *"2026-05-11 RTS-shape conversion: stage triples replaced with trait_checks using capstone flags (npc_frank_stage variable + frank_stage_N helpers cut). auto_goal = false on each non-terminal hint (helpers it would render against are gone)."*

The conversion did its job on the canvas/content side. The hint templates got *halved* in the process — Stage 4 templates kept, Stage 0/1/2/3 templates cut — and never re-authored under the new RTS-shape pattern. **That's the gap.** Frank's pre-catch Quests block is missing because the templates that would render it don't exist.

### Was it intentional?

Yes, in the sense that the author knew the templates were getting cut. No, in the sense that nothing in the redesign docs ever specified Frank should be Quests-silent pre-catch. Doc 30 §8 E7 (the "3-quest journal" Phase E deliverable) implicitly assumes every arc NPC has surface throughout the arc. Ryan and Jake honor that. Frank undershoots it.

---

## §4 How `auto_goal` actually works in the engine

The Phase 2 conversation kept circling `auto_goal` as if it were a top-level switch. It isn't. It's a per-template suppression flag on **one** of five rendering paths inside `setup.computeHintGoal` (v2.py:6233). Once you see the path order, the question "should `auto_goal` always be true?" stops making sense.

### The 5 paths in order

`computeHintGoal(hintObj)` executes its paths in this order and **returns at the first matching path**:

| Path | Trigger | Output | Bypasses `auto_goal`? |
|---|---|---|---|
| **A** | `arc_closure_flag` is set on the hint AND that flag is currently TRUE | `<div>...✓ Arc complete</div>` | Yes (lines 6244-6254 return before the `auto_goal` check at 6278) |
| **B** | `arc_closure_flag` is set AND the flag is FALSE AND the engine can find a setter canvas via `setup._findFlagSetterCanvas` | `<div>🔓 Ready + 📍 <setter loc> + 🕒 <setter schedule></div>` | Yes (lines 6255-6266) |
| **C** | `arc_complete = true` on the hint | `<div>...✓ Arc complete</div>` | Yes (lines 6272-6277) |
| **D** | `auto_goal === false` on the hint | `""` (empty string — no frame, narrative text still renders via widget) | This IS the path that the flag triggers |
| **E** | Default. Requires `condition.stage_npc` + `condition.stage_value`. Reads `<bareSlug>_stage_<N+1>` from `setup.stage_helpers_map`, OR falls back to `setup._findStageSetterCanvas` looking for a transition canvas that writes `npc_<slug>_stage = N+1`. | One of three frames depending on gate state: **State A** 🎯 To advance + bulleted gate list with live progress, **State B** 🎯 Next beat + 📍/🕒 of first-unmet-flag's setter, or **State C** 🔓 Ready + 📍/🕒 of transition canvas | (this IS the path `auto_goal=false` suppresses) |

### What Frank's templates actually do

Frank's two existing templates use Path A (post-consummation) and Path B (pre-consummation). Their `auto_goal = false` is **mechanically inert** — the closure path returns before the `auto_goal` check at line 6278 ever runs. Flipping both templates to `auto_goal = true` would produce byte-for-byte identical HTML.

So why is `auto_goal = false` written there? Two reasons stacked:

1. **Historical defense from the 2026-05-11 conversion.** When the helpers were deleted, the author flipped `auto_goal = false` on the surviving templates because, without a helper, Path E would have returned `""` silently. Setting `auto_goal = false` made the suppression intentional rather than accidental.
2. **Engine author convention.** The comment in `v2.py:6111-6112` reads *"Sits before the auto_goal=false short-circuit so closure templates can leave auto_goal=false."* The engine was deliberately ordered so that closure-flag templates could carry `auto_goal = false` as a *marker* meaning "I render via closure, not via helpers."

### The right rule

"Always set `auto_goal = true`" is the wrong internalization. The actual doctrine is:

> **The goal block must always auto-render from engine state. Never hand-write location/time/thresholds into narrative prose.**

That rule is satisfied by Path A (✓), Path B (🔓 + 📍 + 🕒), Path C (✓), or Path E (🎯 / 🔓 / ✓ with bullets). `auto_goal = true` is only *required* for Path E. The other paths render auto-goals just fine without it.

---

## §5 The unified card pattern (the key design conclusion)

After working through Frank's specifics, then Ryan's mixed shape, then asking "what about a pure-mechanic NPC with no capstones at all," the conversation collapsed to one rule:

> **Every Quests card = a Maya-voice line about where she is right now + the engine-rendered next-goal block.**

Three load-bearing properties:

1. **Card structure is identical across every situation.** Same `.stage-hint-card` div, same `.stage-hint-flavor` + computed goal block + optional `.stage-hint-tip`. No special cases.
2. **The next-goal block changes shape**, not the card. 🎯 bullets for climbing, 🔓+📍+🕒 for ready, ✓ for complete.
3. **The narrative text swaps via the picker** — and that swap IS the state-change signal. No badge, no animation, no "🎉 unlocked!" toast. The picker noticing new state and selecting a different template is the moment the player feels the arc move. (Engine comment v2.py:6231: *"narrative text...stays static across state transitions; the frame swap IS the state-change signal."*)

This rule covers both capstone-driven arcs (Frank) and pure-mechanic arcs (a hypothetical trust-only NPC) and mixed arcs (Ryan / Jake) without any branching logic in the UI.

---

## §6 Player situation matrix

Any player, any arc, any NPC — at any moment they are in exactly one of these six situations. The matrix is exhaustive.

| # | Situation | Maya-voice text describes | Next-goal block |
|---|---|---|---|
| 1 | **Climbing toward a capstone** (gates not met, scripted scene will fire) | What she's feeling about the NPC in this in-between state | **🎯 To advance** + ◯ trait/counter bullets with live progress |
| 2 | **Capstone gates met** (ready to fire) | A line acknowledging the moment is on her ( `ready_text` swap) | **🔓 Ready** + 📍 capstone location + 🕒 capstone schedule |
| 3 | **Capstone fired, arc terminal** (no further stages in scope) | Closure line | **✓ Arc complete** |
| 4 | **Climbing toward a pure-mechanic tier** (no scripted scene; new content quietly opens at threshold) | What she's noticing shift between them | **🎯 To advance** + ◯ trait/counter bullets — **no 🕒, no 🔓 Ready** (no fire window) |
| 5 | **Pure-mechanic tier just crossed** (new content quietly opened) | A line in Maya's voice that names what's changed (*"He's started touching me back when I touch him"*) | Whatever's next — bullets if more mechanic ahead, 🔓+📍+🕒 if next is a capstone with gates already met, ✓ if arc done |
| 6 | **Capstone fired → next thing is a mechanic threshold** | Line acknowledging the cross | **🎯** + bullets for next mechanic threshold |

### What changes between situations 1 and 4

The text says it: situation 1 (capstone climbing) has a fire moment to attend; situation 4 (mechanic climbing) doesn't.

| | Capstone climbing (1) | Mechanic climbing (4) |
|---|---|---|
| What clearing the conditions triggers | Scripted scene auto-fires (or hub menu unlocks) at a known location/time | New menu items appear / new ambient prose rolls in |
| Is there a 🔓 Ready state? | Yes | No |
| Is there a 📍 location to show? | Yes — where the scene fires | Optional — where the activity that ticks the meter happens, but no "fire here" |
| Is there a 🕒 time window to show? | Yes — scene's schedule | Usually no |
| Player action shape | "Be there at that time" | "Keep doing what you're doing" |

### Why situation 5 doesn't need a badge

Two options were considered for marking a pure-mechanic tier cross:

1. **Implicit (recommended)** — picker swaps to a new template whose text names the change. No UI ceremony. The text shift IS the signal.
2. **Explicit toast** ("✓ Frank's mood toward you has shifted") — engine work + breaks fictional frame + over-announces what should feel like noticed-not-told.

The picker-swap doctrine (engine comment v2.py:6231, doc 35 RTS state-variant) is exactly this. Authors write one template per state with the right routing conditions; the engine selects the matching one each render. The cross is felt by reading the new line, not by reading a badge.

---

## §7 Walked example — Frank's full arc

The matrix mapped onto Frank's actual progression, from Day 1 to arc terminal. Every line of `text` below is illustrative — final authored copy lives in `7_final_game.toml` F1–F6 — but conforms to the voice doctrine (no location names, no time windows, no numbers in the prose).

> **Scene order is driven by canvas gate values.** Catch and First-night both gate at corr ≥ 25, but the Catch must fire first (Catch's `frank_caught is_false` gate prevents First-night until catch sets the flag). Declaration gates at corr ≥ 35, Sleepover at corr ≥ 50, Diana confrontation at `npc_diana.awareness ≥ 8` + post-first-night. The walked order below reflects that gate truth — earlier drafts of this doc had Declaration before First-night, which contradicted the actual canvases.

| State | Situation # | text | tip | Goal block |
|---|---|---|---|---|
| Day 1, corr 0, no flags | 1 (climbing toward Catch) | *"I'm new under this roof. Frank watches me and pretends he isn't."* | *"He's around the house all day. I notice that."* | 🎯 To advance: ◯ Maya's corruption — 0 / 25 |
| corr 18, no flags | 1 (same template, picker re-pick) | *"I keep finding reasons to be in the same room as him."* | (same or omitted) | 🎯 To advance: ◯ Maya's corruption — 18 / 25 |
| corr 25, frank_caught false | 2 (Catch ready) | `ready_text:` *"Something's about to give."* | (omit or quiet) | 🔓 Ready + 📍 Living room + 🕒 Mon–Fri 20:00–22:30 |
| corr 25+, frank_caught true, frank_bedroom_first_done false | 2 (First-night ready — corr already at 25 from catch threshold) | *"Upstairs now. The office stays for the books."* + `ready_text:` *"He'll be in his bedroom tonight."* | *"Diana down the hall. Quiet."* | 🔓 Ready + 📍 Frank's bedroom + 🕒 Mon–Fri 21:00–23:00 |
| frank_bedroom_first_done true, frank_cracked false, corr 28 | 1 (climbing toward Declaration) | *"He took me upstairs. He hasn't said the word yet."* | *"Diana's asleep by then. The hallway is dark."* | 🎯 To advance: ◯ Maya's corruption — 28 / 35 |
| corr 35, frank_cracked false | 2 (Declaration ready) | `ready_text:` *"He's going to break tonight."* | — | 🔓 Ready + 📍 Hallway + 🕒 weekday evening |
| frank_cracked true, frank_sleepover_done false, corr 42 | 1 (climbing toward Sleepover) | *"He moved the line. The bedroom is the venue now."* | *"Diana down the hall. Quiet."* | 🎯 To advance: ◯ Maya's corruption — 42 / 50 |
| corr 50, frank_sleepover_done false | 2 (Sleepover ready) | `ready_text:` *"Tonight I don't leave."* | — | 🔓 Ready + 📍 Frank's bedroom + 🕒 Mon–Fri 21:00–23:00 |
| frank_sleepover_done true, diana_confronted false, npc_diana.awareness < 8 | 1 (climbing toward Diana confrontation) | *"The house feels smaller now. She's home all the time and she's watching."* | *"She doesn't say anything. She doesn't have to."* | 🎯 To advance: ◯ Diana noticing — <current> / 8 |
| npc_diana.awareness ≥ 8, diana_confronted false | 2 (Diana confrontation ready, auto-fire) | `ready_text:` *"She's going to ask."* | — | 🔓 Ready (auto-fire — surfaces 📍 from canvas; no time bullet, fires on next eligible encounter) |
| diana_confronted true | 3 (arc terminal) | *"It's done either way."* | — | ✓ Arc complete |

The pattern: **one template per state-window**, with `when` flag/trait gates routing each template to the right window. Picker swaps automatically between them as state changes.

### Authoring status (as of 2026-05-24)

All eleven state-windows above are now authored as six cards (F1–F6) at `7_final_game.toml:2439–2535`:

| Card | Covers | Notes |
|---|---|---|
| F1 | Pre-catch climbing + Catch ready | One template, `ready_text` swap at corr ≥ 25 |
| F2 | First-night ready | No climb (corr ≥ 25 already met from catch threshold); pure flag-gated `ready_canvas` pointer |
| F3 | Post-first-night / pre-declaration | Has `goals` bullet for corr 25 → 35 climb |
| F4 | Post-declaration / pre-sleepover | Has `goals` bullet for corr 35 → 50 climb |
| F5 | Post-sleepover / pre-Diana | Has `goals` bullet for `npc_diana.awareness` 0 → 8 climb |
| F6 | Terminal | Branch-agnostic prose (works for both kicked-out and brought-in forks) |

Earlier drafts of this doc listed 6–8 "missing" templates and described F4 as terminal at `frank_cracked`. That gap closed 2026-05-24 alongside the F3 goals-bullet fix.

---

## §8 Walked example — Ryan's mixed arc

To confirm the unified pattern handles arcs that aren't capstone-dense, walk Ryan through.

Ryan's arc per `7_final_game.toml:2635-2648` is:

- Stage 0: pure mechanic (trust climbs to 10)
- Stage 1: transitional (waiting for Ryan to offer partnership — depends on internal pacing)
- Stage 2: capstone-ish (partnership offered + corr + helps)

Walking the states:

| State | Situation # | Authored text (current) | Goal block under unified pattern |
|---|---|---|---|
| Day 1, trust 5 | 4 (climbing pure-mechanic) | *"Ryan's out in the yard most days. Maybe I should help him."* | 🎯 To advance: ◯ Ryan trust — 5 / 10 + 📍 Yard *(optional progress-location)* |
| trust 8 | 4 (same template) | (same text) | 🎯 To advance: ◯ Ryan trust — 8 / 10 |
| trust 10 reached | 5 (mechanic just crossed; picker swap) | *"Ryan treats me like family now. The next step is on him."* | (waiting state — no concrete bullet; pure ambient) |
| Partnership flag set, trust 25, corr 18, helps 3 | 1 (climbing toward Stage 2 capstone) | *"Ryan calls me his partner. He says a big customer's coming."* | 🎯 To advance: ◯ Ryan trust — 25/40, ◯ Maya's corruption — 18/25, ◯ Yard help — 3/5 |
| All gates met | 2 (Stage 2 ready) | `ready_text:` *"It's going to be tonight."* | 🔓 Ready + 📍 Yard + 🕒 ... |

The shape works. Ryan moves through situation 4 → 4 → 5 → 1 → 1 → 2 without any branching UI logic. Same engine, same widget, same authoring grammar.

---

## §9 Engine support matrix

Honest read of what works today against §5/§6/§7/§8.

| Card piece | Engine support today |
|---|---|
| Maya-voice `text` + optional `tip` line | ✅ `renderStageHint` widget at `v2.py:13760` |
| `ready_text` swap when conditions met | ✅ via `setup._isHintReady` at `v2.py:6106` |
| Picker re-runs on every render | ✅ `getStageHintForNPC` at `v2.py:5648` and `getGlobalHints` at `:5777` |
| Routing templates by `condition.trait_checks` (flags + traits) | ✅ via `setup.checkSingleCondition` |
| **🔓 Ready + 📍 + 🕒 for capstones** | ✅ via `arc_closure_flag` (Path B) reading the setter canvas's location + schedule via `setup._findFlagSetterCanvas` |
| **✓ Arc complete** | ✅ via `arc_complete = true` (Path C) or `arc_closure_flag` flag-set (Path A) |
| **🎯 To advance + live ◯ trait/counter bullets** for both climbing situations (1 and 4) | ⚠️ **Only renders via Path E**, which requires a `stage_npc/stage_value` triple AND either a stage helper or a transition canvas. Frank has neither. Pure-mechanic NPCs without stages would have neither. **This is the gap.** |
| Optional 📍 "where the climb happens" for mechanic cards (no 🕒, no Ready badge) | ❌ No current path. Engine surfaces 📍 only inside the Ready or Next-beat frames; there's no "show NPC schedule location below progress bullets" mode. |

### Why the gap matters

Without bullet progress, situation 1 and situation 4 cards reduce to "narrative text only" — no live indication of how close Maya is to the next thing. Authors could put the progress in `tip` text ("Need about 7 more corruption"), but that violates `feedback_hint_narrative_no_time_or_location` (no numbers in narrative copy). The bullet renderer is the right home for that data; the engine just needs a way to reach it without resurrecting full stage helpers.

### What works *enough* to ship Frank's pre-catch right now

Even without closing the bullet gap, Frank's pre-catch card *can* be authored today:

1. New template with `npc_id = "npc_frank"`, `condition = { trait_checks = [{ flag_key = "frank_caught", operator = "is_false" }] }`
2. `arc_closure_flag = "frank_caught"` — Path B will surface 🔓 Ready + 📍 Living room + 🕒 Mon–Fri 20:00–22:30 from `scene_livingroom_catch`'s own metadata (`7_final_game.toml:6032-6100`)
3. Maya-voice `text` for pre-25-corr climbing
4. Optional `ready_text` for post-25-corr "moment is on her"

Caveat: Path B always renders 🔓 Ready as long as a setter is found — it doesn't check the setter canvas's own entry conditions (e.g. `corruption ≥ 25`). The card would advertise the catch's location/schedule before the corruption gate is met. This is the *same property* Frank's existing Stage 4 hint already has (it points at the bedroom without checking the corruption ≥ 35 gate). Consistent, not a regression.

The bullet gap matters *most* when the player wants to know **how close** they are to the next thing. For Frank, that's the corruption-toward-25 bullet during pre-catch.

---

## §10 Two ways to close the bullet gap (non-prescriptive)

Both options unlock §6 situations 1 and 4 — capstone-climbing and pure-mechanic-climbing — with one piece of work. Doc does not pick one; that's a decision for the next session.

### Option A — minimal per-template helper

**What:** Author writes one `[[engine.stage_helpers]]` entry per hint template containing just the trait/counter gates that template should bullet against.

```toml
[[engine.stage_helpers]]
name = "frank_to_catch"
description = "Pre-catch progress gate — corruption toward 25."
conditions = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 25 },
] }

[[story_arc.hints.templates]]
text             = "I'm new under this roof. Frank watches me and pretends he isn't."
ready_text       = "Something's about to give."
npc_id           = "npc_frank"
auto_goal        = true
arc_closure_flag = "frank_caught"
condition = { trait_checks = [
  { flag_key = "frank_caught", operator = "is_false" },
], stage_npc = "npc_frank", stage_value = 0 }
```

The engine's Path E picks up `frank_to_catch` from `stage_helpers_map` (it would resolve `frank_stage_1` from `bareSlug + "_stage_" + (stage_value + 1)` — naming convention would need `frank_stage_1` or a small engine tweak to accept arbitrary helper names per template).

**Pros:**
- Reuses entirely-proven engine pathway (Ryan/Jake already work this way)
- Engine work: zero (or one small naming-convention tweak)
- Renders bullets, 🔓 Ready frame, and 📍/🕒 — full menu

**Cons:**
- Re-introduces "helpers" on Frank after the 2026-05-11 retire. Important nuance: **these helpers do NOT drive any stage-integer write or canvas gate.** They exist only as named gate-bundles read by the hint renderer. That's a *different role* than the retired `npc_frank_stage` — which was the master variable that 27 canvases gated on. A hint-renderer-only helper is doctrinally lighter.
- Authoring overhead: one helper definition per template

### Option B — inline `progress` field on hint templates

**What:** New optional field on the hint template, read directly by a small new engine path in `computeHintGoal` between Path D and Path E:

```toml
[[story_arc.hints.templates]]
text             = "I'm new under this roof. Frank watches me and pretends he isn't."
ready_text       = "Something's about to give."
npc_id           = "npc_frank"
arc_closure_flag = "frank_caught"
progress = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 25 },
]
condition = { trait_checks = [
  { flag_key = "frank_caught", operator = "is_false" },
] }
```

**Pros:**
- No helpers at all — fully RTS-doctrine
- Authoring is local (everything for the card lives on the template)
- Cleaner mental model: "the template owns its own progress display"

**Cons:**
- New engine surface to write and test (~30 lines in `computeHintGoal`, new template field plumbed through `template_import.py` serializer, new test cases)
- Two ways to render bullets long-term (Path E for old templates + the new path) — though Path E can be deprecated over time

### The half-gap — 📍 "where the climb happens"

Both options leave situation 4's optional 📍 unaddressed (renders only inside Ready/Next-beat frames today). Closing it is small: add a `progress_location` field on the template; renderer surfaces it as a `<div>📍 ...</div>` below the bullets when present. Independent of Option A vs B.

---

## §11 Voice doctrine alignment

Cross-check every situation in §6/§7/§8 against the three voice-doctrine sources.

### Doctrine 1 — `feedback_hint_narrative_no_time_or_location`

> *"Player-facing `text` / `tip` / `ready_text` fields stay in NPC/character voice — no time windows, location names, schedule constraints, or counter thresholds in the narrative copy. Mechanical info goes in the auto-rendered goal block (which reflects live game state)."*

**Compliance check on §7's Frank walkthrough:**
- *"I'm new under this roof. Frank watches me and pretends he isn't."* — no location name, no time, no number ✅
- *"He sees me now. He's looking for it."* — no location, no time, no number ✅
- *"Something's about to give."* (ready_text) — no location, no time, no number ✅
- All goal-block content (📍 Living room, 🕒 Mon–Fri 20:00–22:30, ◯ corruption 18/25) lives in the engine-rendered frame, not in the prose ✅

### Doctrine 2 — Picker-swap-as-signal

TOML comment at `7_final_game.toml:2563-2566`:
> *"Each Quests card = first-person Maya narrative line + optional 💡 tip. State changes are conveyed by SWAPPING which template fires, not by adding structural UI. The picker rule is: (priority desc, condition_items.length desc, file-order asc)."*

Engine comment v2.py:6231:
> *"Narrative text (the .stage-hint-flavor div from renderStageHint) stays static across state transitions; the frame swap IS the state-change signal."*

**Compliance check on §6:**
- Situation 5 (pure-mechanic crossed): no toast, no badge — just a new template wins ✅
- Situation 6 (capstone fired → next mechanic): no announcement — the post-capstone template wins on next render ✅
- All shifts in §7/§8 are pure picker re-pickups; no transitional UI proposed ✅

### Doctrine 3 — Doc 31 §2 Frank voice spec

> *"Speech patterns: short, fragmented sentences. Daddy framing from Tier 3+. Maya's interior voice: observational, terse, no swoony literary prose."*

**Compliance check on §7's text samples:**
- All Maya-voice lines are <12 words ✅
- No literary atmospheric prose ("the kettle clicks at dawn, golden light through gingham") ✅
- Observational rather than emotive ("He sees me now" not "My heart races at his glance") ✅

The unified pattern obeys all three doctrines without exception across every situation in §6.

---

## §12 What this doc does NOT decide

Captured here to surface the next-session decisions cleanly.

1. **Engine option A vs B.** Both close the bullet gap; trade-offs in §10 are real. Decision depends on appetite for engine work vs authoring overhead.
2. **Whether to close the bullet gap *before* shipping Frank's pre-catch templates.** Path B alone (without bullets) already enables a pre-catch Frank card. Shipping that first, then closing the bullet gap second, is a valid order. So is closing the gap first.
3. **Exact TOML schema for the new pre-catch Frank templates** — section §7 shows the *shape*, but final field names, text copy, and ordering are authoring decisions.
4. **Whether to apply the unified pattern retroactively to Ryan/Jake.** Their current Stage 0/1/2 templates roughly follow the rule but were authored before this design was articulated. Audit + nudges may be worth a small follow-up pass.
5. **The "📍 where climb happens" half-gap** (§10 tail) — small but optional; needs its own go/no-go.
6. **Whether `auto_goal = false` lines on Frank's existing templates should be cleaned up** (they're inert; cleanup is cosmetic only).

---

## §13 References

File paths and line numbers for every claim in this doc, so future sessions can re-trace without searching.

### Engine — `apps/game_generation/twee_comprehensive/generators/v2.py`

| Location | What it is |
|---|---|
| `:5648-5706` | `setup.getStageHintForNPC` — per-NPC hint picker. Returns object or null. |
| `:5777-5839` | `setup.getGlobalHints` — global "Story Goals" picker (templates with no `npc_id`). |
| `:6106-6136` | `setup._isHintReady` — determines whether `ready_text` swap fires. Closure-flag short-circuits first; then `auto_goal === false` returns false. |
| `:6138-6182` | `setup._findFlagSetterCanvas` — used by Path B to find the canvas whose `flagEffects` set a closure flag, including sub-menu parent walkback. |
| `:6190-6205` | `setup._formatCanvasSchedule` — turns a canvas's `scheduleParams` into "Mon–Fri 20:00–22:30" style string. |
| `:6208-6214` | `setup._locNameFromUuid` — UUID → location display name. |
| `:6233-6438` | `setup.computeHintGoal` — the 5-path renderer. Path order: closure-flag-set → closure-flag-unset → arc_complete → auto_goal=false → helper/transition. |
| `:6244-6266` | Path A + B (closure flag) — bypasses `auto_goal=false`. |
| `:6272-6277` | Path C (`arc_complete = true`) — bypasses `auto_goal=false`. |
| `:6278` | Path D — `auto_goal === false` short-circuit. |
| `:6280-6437` | Path E — helper / transition-canvas-driven 🎯/🔓 frame. |
| `:13760-13810` | `<<widget "renderStageHint">>` — the card template (flavor + goal block + tip). |
| `:16067-16101` | `:: QuestsPage` — the passage that walks NPCs + globals and emits cards. The `<<if _hint>>` guard at `:16089` is the suppression. |

### Engine — `apps/projects/services/template_import.py`

| Location | What it is |
|---|---|
| `:769` | `auto_goal: bool = True` — default on the `HintTemplate` dataclass. |
| `:1535-1557` | Pattern 2 normalize block — passes `auto_goal` through from TOML to dataclass. |
| `:3564-3580` | Lint rule — warns if a template has `auto_goal = true` AND a manual " — 🎯 " in text. |
| `:4000-4011` | Serializer — emits `auto_goal`, `arc_complete`, `arc_closure_flag` into the runtime hint object. |

### TOML — `games/the_long_summer_test/toml_phases/7_final_game.toml`

| Location | What it is |
|---|---|
| `:107-110` | Comment recording the 2026-05-11 helper retirement |
| `:114-145` | Current stage helpers (Ryan + Jake; no Frank entries) |
| `:200-233` | Flag label registry (`frank_caught`, `frank_restrict_declared`, `group_settled_in`, etc.) |
| `:2551-2707` | Phase 4 — all `[story_arc.hints.templates]` entries |
| `:2563-2566` | Authoring-model comment defining the picker-swap doctrine |
| `:2586-2632` | Frank section — the two existing templates and their inline rationale |
| `:2635-2648` | Ryan section — 3 stage-gated templates |
| `:2651-2669` | Jake section — 3 stage-gated templates |
| `:2684-2707` | Backbone / Story Goals section (rent, settled-in, church, hygiene, energy) |
| `:6032-6100` | `scene_livingroom_catch` canvas — Catch capstone, sets `frank_caught` + `frank_restrict_declared` |
| `:6097-6100` | The `flagEffects` block that makes the catch a discoverable setter for Path B |

### Phase 2 redesign docs

- `28th_april_TLS_Phase2_Redesign/24_RTS_Three_Lanes_Repeatable_Activities.md` — Lane 1/2/3 model
- `28th_april_TLS_Phase2_Redesign/30_TLS_Test_Redesign_PRD.md` — slice E-track including the 3-quest journal promise (§8 E7)
- `28th_april_TLS_Phase2_Redesign/31_Frank_Arc_Design_Brief.md` §3-§6 — the 6-tier ladder + 5 capstones + lane content map
- `28th_april_TLS_Phase2_Redesign/34_TLS_Engine_PRD_Phase_E_Additions.md` — Phase E engine work that landed
- `28th_april_TLS_Phase2_Redesign/35_RTS_State_Variant_and_Authored_vs_Mechanism_Doctrine.md` — picker-swap doctrine origin
- `28th_april_TLS_Phase2_Redesign/11_Hint_Authoring_Guide.md` — current author-facing reference

### Memory entries

- `frank_rts_shape_pass1` — the 2026-05-11 conversion that deleted Frank's stage helpers and pre-catch templates
- `feedback_hint_narrative_no_time_or_location` — narrative copy stays Maya-voice
- `feedback_tls_scene_body_style` — RTS-flat scene bodies (scope: scene bodies, not Quests cards)
- `feedback_rts_objective_quest_doctrine` — one-directive Story-Goals cards
- `phase_e_slice_redesign` — the "3-quest journal" Phase E promise

---

## Appendix A — Quick mental model for authors

If a contributor lands on this doc and wants the single takeaway without reading the trace:

> **Write one hint template per state-window for each arc NPC. The template's `condition.trait_checks` routes it to the right window via flags/traits. Maya-voice text only — no location names, no time windows, no numbers. Pick the right engine path for the goal block:**
>
> - **Capstone with gates to climb** → either Option A (helper + Path E for bullets) or Option B (`progress` field), plus `arc_closure_flag` for the eventual 🔓+📍+🕒.
> - **Capstone with no in-between bullets needed** → just `arc_closure_flag` (Path B). Renders 🔓+📍+🕒 from the setter canvas.
> - **Pure-mechanic tier climbing** → Option A or B for bullets (no `arc_closure_flag` since there's no setter scene).
> - **Pure-mechanic tier just crossed** → just a new template with the right routing condition. Picker picks it; the picker swap IS the signal.
> - **Arc terminal** → `arc_complete = true`.

That's it. Same card shape everywhere; the engine path is determined by what kind of "next thing" the player is approaching.
