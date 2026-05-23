# 11 — Hint Authoring Guide

**Audience:** anyone writing or auditing `[[story_arc.hints.templates]]` entries in a game's TOML.

**Why this exists:** every author of stage-gated hints in this engine has hit the same set of pitfalls — hallucinated mechanics, vague nudges, multi-gate stuck states, hidden schema constraints. This doc captures the recurring traps and the fixes. Read it once before writing or rewriting hints; revisit when something feels confusing during playtest.

**Source:** lessons from the The Long Summer Test Slice (2026-05-01 hint pass). Every anti-pattern below was actually shipped before being caught.

---

## Mental model: what a good hint does

A Quests card has exactly **one piece**: the first-person Maya narrative line (`text` field) — what Maya is thinking about this thread right now. That's the entire card.

No structured goal block. No activity list. No location/schedule/threshold UI. No 💡 tip. State changes are conveyed by **swapping which template fires**, not by adding rows to the card. If state matters, you write a variant template gated on that state; the picker swaps the line at runtime.

Game-level mechanics (decay rates, what affects diner tips, etc.) live on a separate `:: TipsPage` authored under `[ui.tips_page]` — see "Game-level mechanics: the Tips page" below.

This is the post-2026-05-01 model. Earlier iterations shipped Pattern 2 (auto-rendered 🎯 goal block), Pattern 3 (per-NPC activity list), and a per-template `tip` field; all three were removed in favor of narrative variants + a single Tips page. See doc 12 §2.10 / §2.11 / §2.13 for the rollback rationale.

---

## Narrative voice rules

The narrative line's only job is to make the journal entry feel like Maya's own thought — so a player can scan the page and immediately feel which thread each section is about. Inspired by Road to Success's quest-journal style: terse, first-person, mood + intent, no mechanics.

### Rule 1 — First-person, present-tense

Maya's thought, not the narrator's description. The journal feels like Maya is writing in it, not us writing about her.

- ✅ "I should help Frank with the books. I could use the money."
- ❌ "Frank's office at nine. The bookkeeping pays."

### Rule 2 — One complete idea per line

Subject + want + (optional) hint where. No compound clauses, no semicolons, no parenthetical mechanics.

- ✅ "Ryan's out in the yard most days. Maybe I should help him."
- ❌ "Ryan's at the work table (08:00–15:00 weekdays) and needs help with corruption ≥ 25 to advance."

### Rule 3 — Curiosity or pressure baked in

A `?` or a feeling word gives the line emotional weight without spending more words. The player feels Maya's stakes, not just her checklist.

- ✅ "Maybe if I look right, he'll notice me."
- ❌ "Walk past Jake's door three times."

### Rule 4 — No mechanics in the narrative

No numbers, no time bands, no internal trait/flag names, no `≥`, no `<`, no `+1`, no `Mon–Fri`. Auto-render handles all of it. If you find yourself typing a number into `text`, stop — it belongs in the helper or canvas, where the engine will read and display it.

- ✅ "I'm wiped. I need to rest before I can think straight."
- ❌ "Energy < 40. Sleep in Bedroom (22:00+) or Nap (30 min, costs hygiene)."

### Rule 5 — Standalone meaningful

The narrative line should tell the player what the section is *about* even before they scan the auto-rendered block below it. If the line could mean ten different things until you read the goal bullets, it's too vague.

- ✅ "Frank wants help with the books. I could use the money." (clear without mechanics — a player skimming knows: there's bookkeeping work, money's involved)
- ❌ "He looked up from the table." (ambiguous — who? what about? mechanics required to interpret)

---

## Template ordering & narrative variants

The picker resolves competing templates with this rule (per NPC, per global goal):

```
sort by (priority desc, condition_items.length desc, file-order asc)
```

So a more-specific or higher-priority variant **automatically wins** — file order only matters as a final tiebreaker between truly identical candidates (and the linter warns if it has to). This means you can write multiple narrative variants for the same NPC stage, each gated on different state, and let the picker swap which one fires.

### Specificity is the default tiebreaker

Most cases don't need a `priority` field. Just write the more-specific variant — the picker counts normalized `condition_items` and the longer list wins.

```toml
# Baseline — fires when nothing else applies. 1 condition_item (stage gate).
[[story_arc.hints.templates]]
text      = "Frank wants help with the books. I could use the money."
npc_id    = "npc_frank"
condition = { stage_npc = "npc_frank", stage_op = "eq", stage_value = 0 }

# Crisis variant — fires while rent is unpaid. 2 condition_items
# (stage gate + missing_flag) — wins by specificity, no priority needed.
[[story_arc.hints.templates]]
text      = "Frank's offering bookkeeping work — cash in hand. Rent's hanging over me. I can't afford to skip a session."
npc_id    = "npc_frank"
condition = { stage_npc = "npc_frank", stage_op = "eq", stage_value = 0, missing_flag = "first_rent_paid" }
```

Once `first_rent_paid` flips, the crisis variant stops matching, the baseline takes over, and the narrative softens automatically.

### Use `priority = N` for crisis overrides

Reserve explicit priority for **crisis or pressure variants that should override an ambient line of equal specificity**. Default 0; higher wins. Most templates leave it unset.

A common case: the same number of condition_items but different urgency. The slice's Frank Stage 0 rent-pressure variant uses `priority = 10` belt-and-suspenders alongside the missing_flag specificity bump — both signals point the same direction, and the explicit priority makes intent obvious to a future reader of the TOML.

### Anti-patterns

- **Don't tag `priority` on every template.** Adds visual noise and makes it harder to scan for the variants that actually override.
- **Don't reorder the file expecting behavior to change.** File order is the *last* tiebreaker; if you find yourself moving lines around to fix picker behavior, you need a priority bump or a distinguishing condition instead.
- **Don't ship two templates with identical `npc_id + stage_value + priority + condition_items.length`.** The linter warns about this — bump one's priority or add a condition to differentiate.

### Cross-NPC pressure (Diana arc territory)

When a future arc gates on another NPC's stage (e.g., Diana opens up only after Frank Stage 2), don't add a structured "Progress with Frank" row — write a narrative variant whose `condition.prerequisite_npc_stage = "npc_frank >= 2"` carries the cue:

- Pre-Frank-Stage-2: *"Diana keeps her distance. Maybe she's waiting to see if Frank trusts me first."*
- Post-Frank-Stage-2: *"Diana wants to talk about something private."*

The picker swaps the line; the player reads it as Maya noticing the shift.

### Authoring checklist (for narrative line specifically)

Before saving a `text` field, scan it once:

- [ ] Starts with a personal subject ("I", "Frank", "Ryan", "Jake") not an abstract observation?
- [ ] One sentence, or two short ones — no compound clauses?
- [ ] Zero numbers, zero time bands, zero `≥` / `<` / `+`?
- [ ] Zero internal trait/flag names (`group_settled_in`, `frank_bookkeeping_count`, etc.)?
- [ ] Reads as a journal thought a player would believe Maya wrote in her diary?
- [ ] Standalone meaningful — tells the player what the thread is about?

If any answer is no, rewrite. If you need to mention a number/schedule, the right place is the helper definition or canvas trigger — or, if it's universal game info, the Tips page.

---

## Game-level mechanics: the Tips page

Anything that's a **rule about how the game works** ("Trust decays 1.0/day if you ignore an NPC", "Hygiene below 40 docks your diner tips", "Sleep restores energy fully but Nap costs hygiene") is **universal mechanics**, not quest-specific advice. Putting it on individual hint templates means:

- Authors paste the same line onto every relevant card (drift risk).
- Players read it once and tune it out by Day 2.
- Updating a rate means a search-and-replace across templates.

These belong on the **Tips page** — a separate `:: TipsPage` passage authored under `[ui.tips_page]` in the project metadata TOML, surfaced via a "💡 Tips" sidebar button. Authored once, accessible whenever the player wants it, off the Quests journal entirely. The slice's Tips page in `1_metadata_and_locations.toml` is the worked example — sections for Time / Trust / Hygiene / Energy / Money / Corruption + Beauty / Reading the Quests page.

Schema:

```toml
[ui.tips_page]
title = "Tips"
content = """
<h3>Trust</h3>
<p>NPC trust climbs when you spend time on their stuff and decays roughly <strong>1.0/day</strong> when you ignore them.</p>

<h3>Hygiene</h3>
<p>Drops with sweat. Below 40, the diner manager docks your tips.</p>

...
"""
```

Author writes raw HTML (engine prints `content` verbatim — no markdown engine). When the block is absent, the sidebar button + page are not emitted (graceful no-op for games without a Tips page).

**Quest-specific advice that isn't a universal rule** ("Frank's office tease count comes from supervised office scenes — push corruption first") has two homes today:

1. **Folded into the narrative variant** — write a Frank Stage 2 variant whose narrative implies the path: *"Frank's lessons run past their hour. He's making excuses to keep me there. I should let him."*
2. **Accept the player discovers it through play.** TLS-style sandboxes generally trust the player to experiment; not every gate needs a hint.

If neither feels right, the quest needs a redesign — the player is being asked to guess something genuinely arbitrary.

### Reference example pairs (from the slice)

| Stage | Before (third-person observation) | After (first-person journal) |
|---|---|---|
| Frank Stage 0 | "Frank's office at nine. The bookkeeping pays." | "Frank wants help with the books. I could use the money." |
| Ryan Stage 0 | "Ryan's at the work table with the saw." | "Ryan's out in the yard most days. Maybe I should help him." |
| Jake Stage 0 | "Jake's door is mostly shut." | "Jake stays in his room. Maybe if I look right, he'll notice me." |
| Rent (global) | "Rent's Sunday. — 🎯 $60 due Sunday morning in the Kitchen. Earn it at the Diner shift (Mon–Sat 17:00–22:00). Miss it → eviction." | "Rent's due Sunday morning. If I don't have it, I'm out on the street." |
| Hygiene (global) | "I smell the day on me. — 🎯 Hygiene's running low. Shower in the Bathroom." | "Ugh, I really need a shower." |
| Energy (global) | "Everything costs more when I'm tired. — 🎯 Energy's running low. Sleep in the Bedroom or take a Nap." | "I'm wiped. I need to rest before I can think straight." |

---

## The eleven recurring pitfalls

### 1. Hallucinated mechanics

**Symptom:** the hint references an action, item, or interaction that doesn't exist in the game.

**Real example caught in TLS slice:**
> *"Ryan's in the yard with the belt sander. He could use a water. Make him notice me work."*

There's no "bring water" mechanic. The actual lever is `activity_help_ryan_in_yard` (hold boards while Ryan saws) or `scene_yard_with_ryan` (Watch / Help choice). A player who interprets the hint literally finds nothing.

**Fix:** before writing any hint, open the canvas the hint is pointing at. Read the `[[canvases.nodes]]` and the choices' effects. The hint must name an action that exists in those nodes.

**Audit trick:** for every verb in the hint, ask "which canvas executes this?" If you can't name the canvas, the hint is fiction.

---

### 2. Numeric thresholds that don't match the actual gate

**Symptom:** hint says "corruption ≥ 25" but the canvas trigger requires `corruption >= 45`. Player pushes corruption to 26, expects something to fire, nothing does.

**Real example caught in TLS slice:**
> Frank Stage 1 hint said *"Auto-fires when corruption ≥ 25"*. Actual `scene_living_room_evening` trigger required `corruption >= 45`. **20-point gap.**

**Fix:** for every numeric threshold in the hint, grep for the canvas's `[canvases.trigger]` block (or the helper's `[[engine.stage_helpers]]` block) and copy the number verbatim.

**Audit trick:** the hint and the canvas/helper must reference the SAME number. If they drift, the hint is wrong (the canvas is the source of truth — it's what actually fires).

---

### 3. Time bands that don't match the schedule

**Symptom:** hint says "20:00–22:00" but schedule is `start_time = "20:00", end_time = "22:30"`.

**Real example caught in TLS slice:**
> Frank Stage 1 hint said *"Living Room evening (19:30–22:00)"*. Actual `[[canvases.trigger.schedules]]` was `20:00–22:30`. Player visits at 19:30, nothing fires (window hasn't opened) → blames the hint.

**Fix:** copy `start_time` and `end_time` verbatim from the canvas's schedule block. Don't approximate.

**Audit trick:** for every time mention in the hint, find the canvas's `[[canvases.trigger.schedules]]` and confirm.

---

### 4. Mentioning only one of multiple AND-gates

**Symptom:** stage helper has multiple AND conditions; hint surfaces only the visible one (usually trust). Player satisfies it, expects advancement, gets confused.

**Real example caught in TLS slice:**
> Ryan Stage 0→1 helper: `trust >= 10 AND group_settled_in == true`. Original hint only mentioned the yard work that builds trust, not the settling-in flag. Player drove trust to 12, opened journal, same hint, no advancement. *"I've done this for a week, why is the journal still telling me to do it?"*

**Fix:** when the helper has N gates, the hint MUST list all N. Use language like *"Need BOTH: …"* or *"Need ALL of: …, …, …"*. Never let a gate go unmentioned.

**Audit trick:** for every stage hint, open the matching `[[engine.stage_helpers]]` block. Count the items in the `conditions` array. Count the gates mentioned in the hint. They must match.

---

### 5. No transitional template for "one gate met, others missing"

> **Engine constraint lifted 2026-05-01 (E14).** Hint conditions now support `trait_checks` arrays — see "Engine features that support hint authoring" section below for the full schema. The pitfall pattern remains useful guidance for authoring discipline (you still need to *think about* multi-gate states), but the schema now permits the precise expression. See doc 12 §2.2 for the as-built record.

**Symptom:** even when a hint lists all gates, a player who has cleared some still sees the same hint forever. They can't tell which sub-state they're in. Feels static.

**Workaround within current schema:** add a SECOND template ordered BEFORE the baseline, gated on `missing_flag` for whichever flag is the diagnostic blocker. When that flag flips, the transitional stops matching and the baseline takes over. Engine returns first match (`v1.py:4515`), so ordering matters.

**Real example shipped:**
```toml
# Transitional — fires when diner shift hasn't happened (the major settling-in blocker)
[[story_arc.hints.templates]]
text      = "Ryan's warming up — but you're still the new girl in this house. — 🎯 Settle in first: do a diner shift with Marge tonight..."
npc_id    = "npc_ryan"
condition = { stage_npc = "npc_ryan", stage_op = "eq", stage_value = 0, missing_flag = "first_t0_shift_done" }

# Baseline — fires once the diner shift is done
[[story_arc.hints.templates]]
text      = "Ryan's at the work table with the saw. — 🎯 Help in Back Yard..."
npc_id    = "npc_ryan"
condition = { stage_npc = "npc_ryan", stage_op = "eq", stage_value = 0 }
```

**Schema constraint (current):** the `condition` field only supports `missing_flag` (singular) + the `stage_npc/stage_op/stage_value` triple. **Cannot** gate on trait thresholds (e.g., "trust < 10") today. To express "trust ≥ 10 but flag false" precisely, the engine needs E14 (trait_check support in hint conditions).

**When you can't add a transitional:** make the baseline maximally diagnostic. Tell the player to read their sidebar: *"…whichever number is lower in your sidebar is the bottleneck."*

---

### 6. "Cleared but not triggered" gap (universal — engine limitation)

**Symptom:** player satisfies all helper conditions. Helper returns true. But the actual stage advancement happens on the *next visit* to the transition canvas's location. Until that visit, the hint still shows the OLD stage's text.

**Concrete case:** Ryan trust hits 10, group_settled_in is true. `ryan_stage_1` helper clears. But the player is in the kitchen. Until they walk to the Yard, `transition_ryan_to_1` doesn't fire. Hint still says "Help in Back Yard until trust ≥ 10" — even though they've already cleared 10. They re-grind a satisfied gate.

**Slice-side mitigation:** none reliable today. Best practice: choose transition-canvas locations that the player visits naturally as part of grinding the gate (e.g., Frank's transition canvas lives in Frank's Office, where bookkeeping happens). This minimizes the stuck window.

**Engine fix (future, E17):** detect when a helper clears but the corresponding `<slug>_stage` trait hasn't advanced. Render a special hint: *"→ Visit X to seal it."* ~25 lines in v1.py around `setup.getStageHintForNPC`.

---

### 7. Visual ambiguity — `✓` read as completion checkmarks

**Symptom:** author uses `✓` as a bullet character; player reads it as "done" (because that's what ✓ means in any other UI).

**Real example caught in TLS slice:**
> *"Settling-in checklist: morning kitchen ✓ (pre-seeded), first diner shift ✓, one yard visit."*

The author intended ✓ as bullets (3 list items). Player read it as "morning kitchen DONE, first diner shift DONE, only yard visit remains" — even when first_t0_shift_done was actually false.

**Fix:** use `•` for list bullets, NEVER ✓. Reserve ✓ for actual state tracking IF the engine ever supports per-gate live-render (it doesn't today — see E14/E17).

---

### 8. Internal variable names leaking to the player

**Symptom:** hint includes raw flag/counter names. Reads like log spam, not English.

**Real example caught in TLS slice:**
> *"Need Ryan trust ≥ 40 + ryan_help_count ≥ 5 + corruption ≥ 25..."*

`ryan_help_count` is a TOML key. The player has no UI to see its value, no idea what it means. Should read: *"…helped him in the yard 5+ times…"*

**Fix:** every variable name in a hint must be translated to plain English. The conversion rules:
- Flags → *"the … invitation"*, *"after the … event"*
- Counters → *"…N+ times"*, *"after N sessions"*
- Trait stats → *"trust"*, *"corruption"*, *"beauty"* (these stat names are visible in the sidebar, OK to use literally)

**Audit trick:** for every word in the hint, ask "would a player who never opened the TOML understand this?" If no, translate.

---

### 9. Hints with no `npc_id` are silently dropped (current engine limitation)

> **Engine constraint lifted 2026-05-01 (E15).** Templates with no `npc_id` now render in a "Story Goals" section above per-NPC sections via `setup.getGlobalHints()`. Just author them normally — no special syntax needed. See doc 12 §2.4 for the as-built record.

**Symptom:** author writes a "global" hint (rent, hygiene, energy, story-wide goal) without an `npc_id`. Hint never appears anywhere in the Quests page. Author thinks it's working.

**Cause:** `setup.getStageHintForNPC(npcSlug)` at `v1.py:4517` explicitly skips any template whose `npc_id` doesn't match the NPC currently being looked up. Templates without `npc_id` never match any lookup → never render.

**Workaround today:** don't author them. Add a comment in the TOML explaining the limitation (so the next author doesn't re-add them):

```toml
# Backbone (rent / hygiene / energy) — REMOVED until E15 lands.
# Templates without `npc_id` are skipped by setup.getStageHintForNPC
# (v1.py:4517). Re-author once E15 (global hint rendering) ships.
```

**Engine fix (future, E15):** add a "Global Goals" or "Backbone" section to QuestsPage that walks templates with no `npc_id` and renders the first one whose `missing_flag`/`missing_trait` matches.

---

### 10. Template ordering matters — most-specific FIRST

**Symptom:** transitional template added correctly, but the baseline still fires because it appears earlier in the array.

**Cause:** `setup.getStageHintForNPC` returns the FIRST matching template (`v1.py:4515-4528`). It doesn't pick "most specific" — it picks "first listed."

**Fix:** for each NPC, order templates from MOST CONSTRAINED conditions to LEAST CONSTRAINED. Pattern:
```
1. Transitional templates (stage + missing_flag)
2. Baseline Stage 0 (stage only)
3. Stage 1 (different stage, doesn't conflict)
4. Stage 2
...
```

If you add a transitional after the baseline, it will never fire.

---

### 11. Forgetting that hints are slice-side, not engine-side

**Symptom:** "but the engine should know about this" thinking. Author tries to add complex evaluation logic in the hint itself.

**Reality:** the hint is a string. It's chosen by `getStageHintForNPC` based on the template's condition. The string is then `<<print>>`-ed verbatim. There is no per-gate live evaluation today (would be E14 + E17 territory).

So if the hint says *"…whichever number is lower in your sidebar is the bottleneck"*, the engine isn't going to actually highlight which number. The player has to look. Phrase your hints accordingly — always actionable by the player without engine introspection.

---

## Authoring checklist (use this every time)

Before committing any new or revised `[[story_arc.hints.templates]]` block:

1. ☐ Open the canvas this hint points at. Confirm the action you describe exists.
2. ☐ Open the stage helper this hint gates on. List its `conditions` items.
3. ☐ Confirm every numeric threshold in the hint matches a number in the helper or trigger. Verbatim.
4. ☐ Confirm every time band in the hint matches a `[[canvases.trigger.schedules]]`. Verbatim.
5. ☐ For every gate in the helper, confirm the hint mentions it (or a clear path to it).
6. ☐ Replace any `✓` bullets with `•`.
7. ☐ Replace any TOML variable names (flags, counters) with plain-English equivalents. Trait names (trust, corruption, beauty) are OK to use as-is.
8. ☐ If the helper has N AND conditions and you can't add transitional templates (schema doesn't allow), make the baseline maximally diagnostic ("…whichever is lower in sidebar…").
9. ☐ If you add a transitional template, place it BEFORE the baseline of the same stage.
10. ☐ If the hint is global (no `npc_id`): don't write it yet. Add a comment marker. Wait for E15.
11. ☐ Format: one short flavor sentence, ` — 🎯 `, then the action block. Example below.

---

## Format reference (one canonical example)

```toml
[[story_arc.hints.templates]]
text      = "Ryan's at the work table with the saw. — 🎯 Help in Back Yard (08:00–15:00 weekdays) until Ryan trust ≥ 10. Settling-in checklist (need 3 of 4): • morning kitchen (already done at game start) • first diner shift • visit yard at least once. Help/Watch each adds +1–+2 trust; trust decays 0.8/day if you skip."
npc_id    = "npc_ryan"
condition = { stage_npc = "npc_ryan", stage_op = "eq", stage_value = 0 }
```

Breakdown:
- **Flavor:** *"Ryan's at the work table with the saw."* (≤ 12 words, Maya POV)
- **Separator:** ` — 🎯 ` (em-dash space target space — engine widget splits on this)
- **Where:** Back Yard
- **When:** 08:00–15:00 weekdays
- **What:** Help in (the named activity)
- **Threshold:** Ryan trust ≥ 10
- **Other gate:** settling-in checklist with 3 bulleted items
- **Cost/cooldown:** trust decays 0.8/day

---

## Engine features that support hint authoring

The PRD 09 batch (shipped 2026-05-01) closed the engine constraints that previously blocked precise hint authoring. Conventions and schema below — full as-built record in `12_Engine_PRD_09_Hint_System_Completeness.md`.

### `trait_checks` in hint conditions (E14)

Express precise multi-gate transitionals like "stage 0 AND trust ≥ 10 AND group_settled_in is_false":

```toml
condition = { stage_npc = "npc_ryan", stage_op = "eq", stage_value = 0, trait_checks = [ { type = "trait", subject = "npc", npc_id = "npc_ryan", trait_key = "trust", operator = "gte", value = 10 }, { type = "flag", subject = "player", flag_key = "group_settled_in", operator = "is_false" } ] }
```

**Ordering matters:** transitional templates with TIGHTER conditions must come BEFORE broader baselines. Engine returns first match.

**TOML constraint:** inline tables can't span multiple lines per TOML 1.0 spec. Trait_checks arrays must be on a single line — gets long but works.

### Cross-NPC prerequisite (E22)

Express "Diana's arc only opens once Frank reaches Stage 2":

```toml
condition = { stage_npc = "npc_diana", stage_op = "eq", stage_value = 0, prerequisite_npc_stage = "npc_frank >= 2" }
```

Format: `"npc_<slug> <op> <int>"`. Validator confirms NPC exists and value is in range.

### Global hints render in "Story Goals" (E15)

Templates with no `npc_id` (like rent/hygiene/energy) render in a "Story Goals" section above per-NPC sections in QuestsPage. Just author them — no special syntax needed:

```toml
[[story_arc.hints.templates]]
text = "Rent's Sunday. — 🎯 $60 due Sunday morning..."
condition = { missing_flag = "first_rent_paid" }
```

### "All gates cleared" auto-hint (E17)

When a stage helper clears but the player hasn't visited the transition canvas's location yet, the engine auto-synthesizes: *"All gates cleared. — 🎯 Visit Back Yard to seal the moment."*

**No author action needed** — works for every NPC with a `<bare>_stage_<N+1>` helper convention. The location is resolved by walking `locationCanvases` for the canvas where the helper appears as a trigger condition.

### Counter sidebar bars (E18)

The engine **auto-emits** a `trait_bar` sidebar item for every counter trait used in stage helpers (any trait with `_count`/`_done` suffix referenced by `subject="player"` with `operator="gte"`). Picks the lowest threshold per counter as the immediate gate.

**No author action needed** — bars appear automatically. Override with explicit `[[sidebar_items]]` only if you need a custom label or special styling.

### Decay warnings (E20)

The engine **auto-emits** a `trait_decay_warning` sidebar item if any decaying traits exist. At day rollover, decaying traits are snapshotted; at render time, an amber banner fires when a tracked trait dropped today AND is within 2.0 of its next gate.

**No author action needed** — decay configuration on player + NPC traits is the only input.

### Cooldown opt-in (E21)

Per-canvas opt-in for daily-cooldown solo activities to render as grayed entries instead of disappearing:

```toml
[canvases.trigger]
show_when_blocked = true
cooldown_message = "Available again tomorrow morning"
```

Default off (silent filter). Opt in per-canvas where the cooldown rhythm matters to the player.

### Hint linter (E23)

Runs at every `package_from_toml` build. Cross-checks hint text against helper / canvas actuals and surfaces drift as ⚠️ warnings (never blocks the build):

- Numeric threshold drift (`trust ≥ N` in hint vs different N in helper)
- Time band drift (`HH:MM–HH:MM` in hint vs different schedule in canvas)
- Internal name leak (counter/flag names showing up in player-facing text)
- ✓ used as bullet (player reads it as "completed")
- Missing `npc_id` and no `stage_npc` (template silently dropped — see §9 below)
- Helper has N AND-gates but hint mentions <N

Two known false positives in current linter: branch-inside-shell transitions and OR-logic helpers. See doc 12 §2.1 for details.

---

## Engine TODOs — shipped status

| ID | Description | Status | Lifts pitfall |
|----|-------------|--------|---------------|
| **E14** | `trait_checks` items in hint conditions | ✅ Shipped 2026-05-01 (doc 12 §2.2) | #5 (precise transitionals) |
| **E15** | Global hint rendering | ✅ Shipped 2026-05-01 (doc 12 §2.4) | #9 (no-`npc_id` silently dropped) |
| **E16** | Stage hint visual split | ✅ Shipped 2026-05-01 (doc 12 §2.6) | (visual scannability) |
| **E17** | Cleared-but-not-triggered detection | ✅ Shipped 2026-05-01 (doc 12 §2.5) | #6 (universal stuck-feeling) |
| **E18** | Counter sidebar bars (auto-emit) | ✅ Shipped 2026-05-01 (doc 12 §2.7) | (counter visibility) |
| **E20** | Decay warnings (auto-emit) | ✅ Shipped 2026-05-01 (doc 12 §2.8) | (silent decay surprise) |
| **E21** | Cooldown opt-in | ✅ Shipped 2026-05-01 (doc 12 §2.9) | (silent filter rhythm) |
| **E22** | Cross-NPC prerequisite | ✅ Shipped 2026-05-01 (doc 12 §2.3) | (cross-arc dependency visibility) |
| **E23** | Build-time hint linter | ✅ Shipped 2026-05-01 (doc 12 §2.1) | #1, #2, #3, #7, #8, #9 (all auto-detected) |

**The pitfalls below remain useful guidance** for authoring discipline even when the engine permits the precise expression — the discipline catches things the linter doesn't (intent, story coherence, voice). But the schema constraints documented in pitfalls #5 and #9 above no longer apply.

---

End of guide.
