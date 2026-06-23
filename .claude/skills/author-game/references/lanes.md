# The four lanes — when to use each, and how to write them

NPC content uses four mechanisms. They are the SAME canvas+trigger engine; the
"lane" is the *combination of trigger fields* (the per-lane fingerprints below — `references/engine-reference.md`
has the full field reference). An NPC arc is built **across** lanes, sized by the NPC's arc shape (budget
table below). Read this before authoring any `npc_intro` / `arc_escalation` / `cross_npc` / `capstone` beat.

**Two companion references:** pick each NPC's gating *spine* — which trait drives the arc, by shape —
per `references/trait-design.md` (don't gate every NPC on `relation`). The repeatable explicit layer
(after the first-night capstone) is the **sex-loop menu**, its own pattern — `references/sex-loop.md`.

## The lanes at a glance
| Lane | Who picks | Player POV | Intent |
|---|---|---|---|
| **1 — Hub button** | Player clicks a menu item | "I'll click Tease." | Intentional escalation; high agency |
| **2 — Location-entry random** | Dice on room entry | "I walked in and he was…" | Ambient coexistence; texture |
| **3 — Dispatcher substitution** | Dice inside a Maya-solo activity | "I was showering and he walked in." | Charged surprise; happens *to* her |
| **4 — Capstone** | Engine, on threshold cross | "The night he caught me." | One-shot milestone; point of no return |

## The master rule — Lane 1 leads
> Lane 1 leads the arc; Lanes 2/3 follow as consequences of Lane 1 escalation; Lane 4 capstones
> gate the milestones, fired by the stat/flag combos Lane 1 produces.

The player clicks Lane 1 → stats rise → at thresholds, Lane 2/3 content *lights up* and Lane 4
capstones fire. "The world fills out around me as I escalate." So: **every arc is enterable from a
cold start** (corruption 0, no flags) through ordinary presence — the Lane 1 hub's base renders
unconditionally (presence floor). Never gate an arc's entry on a stat only raisable *inside* that
arc — that's the **"backwards on-ramp"**: the door locked behind a key that lives on the far side of
it, so the arc can never be entered from a cold start.

## The 3×3 grid — mix lanes AND tiers
Within each lane, intensity scales with stat tier. A game that is all-one-lane feels wrong:
all Lane 1 = transactional "menu game"; all Lane 2 = inert/passive; all Lane 3 = no agency.
**Mix all three lanes across all three tiers → alive.** Lane 4 sits outside the grid (the milestones).

## Per-arc-shape budget — the canvas-distribution matrix
Each arc shape (chosen per `references/trait-design.md`) has a per-lane canvas budget — L1 escalation
rungs / L2 ambients / L3 walk-ins / capstones, plus a per-shape total. **These are FULL-game targets
and the matrix below is the single source of truth** — size every arc against it; cell values are
guidelines, not quotas (the NPC's design brief commits to a specific number within each range).

| Lane / Tier | Family/ambient | Slow-burn family | Peer/dating | Service | Antagonist/witness |
|---|---|---|---|---|---|
| **L1 / T1** | 1–2 base + 1–2 self-display | 1 (room visit) | 1 (visit at workplace) | 1 (workplace base) | 0–1 (shared-space neutral) |
| **L1 / T2** | 1–2 mid escalation | 0–1 (charged moment) | 0–1 (date intro) | 0 | 0 (no escalation register) |
| **L1 / T3** | 1–2 explicit | 0–1 (consummation if vocab allows) | 0–1 (commit beat) | 0 | 0 |
| **L2 / T1** | 1–2 morning/passing | 0–1 (corridor) | 1 (workplace ambient) | 1 (workplace texture) | 1–2 (presence beats) |
| **L2 / T2** | 2–3 evening/charged | 0–1 (charged corridor) | 0–1 (low density) | 0–1 | 1–2 (charged presence) |
| **L2 / T3** | 1–2 late-night/explicit | 0 | 0 | 0 | 0–1 (confrontation precursors) |
| **L3 / T1–T3** | 4–7 walk-ins on chores | 1–3 (discrete revelation walk-ins) | 0 | 0 | 0 own (appears in others' L3) |
| **Capstones** | 4–6 (catch, declare, first-night, sleepover, confrontation) | 3–5 (transitions + revelation + relationship turn) | 3–4 (dating chain) | 1–2 (hire + escalation if vocab allows) | 1–2 (confrontation, resolution) |

**Total canvas budget by shape:**

| Shape | Total | Notes |
|---|---|---|
| **Family/ambient** | **25–35** | The dense shape; the gold standard. Lane 3 is the dominant lane (~47%). |
| **Slow-burn family** | **10–15** | Sparse but focused; each revelation beat is concentrated, not a routine. |
| **Peer/dating** | **8–12** | Quest-chain progression; capstones do the heavy lifting. No Lane 3. |
| **Service** | **6–10** | Bounded by workplace register. No Lane 2 or 3. |
| **Antagonist/witness** | **6–10 standalone** | + cross-appearances in others' arcs. Standalone count is low; presence saturates the family arcs' lanes. |

How the skill applies that budget:

- **Empty cells are honest.** Peer/dating → no Lane 3. Service → no Lane 2 or 3. If the shape has 0 in
  a cell, the brief commits to 0 — filling an empty cell with relational/atmospheric texture to "fill out
  the world" is the failure, not the omission. (This governs the L2/L3 *escalation* surfaces; it never
  excuses a missing presence hub — see the next note.)
- **L1 cells count escalation *rungs*, not hubs.** The number of Lane 1 **hubs** is set separately by
  presence: **one Lane 1 hub per distinct `[[npcs.schedules]]` row** (location × window). An NPC
  scheduled across 5 windows has 5 hubs even with a tiny rung budget — the extra hubs are *light*
  (base + talk + leave), exposure-tier-capped, not extra escalation. Even a service/antagonist NPC gets
  a light hub at each scheduled location. Presence floor (a hub) and escalation register (the rungs on
  it) are independent axes.
- **Offscreen schedule rows are exempt from the hub rule.** A row at an `offscreen = true` location
  (the NPC's home/sleep/away block) is a non-navigable label — the player can't go there, so it gets
  NO hub and is exempt from the presence floor (`references/location-design.md`, the Day System). Use
  offscreen rows to complete an NPC's day without manufacturing dead presence. Only **reachable** rows
  earn a hub; **locked** rows follow the unlock contract (the locked-location unlock contract in
  `references/location-design.md`).
- **A third independent axis the L3 cells don't count: the player's own daily loop.** The L3 cells count
  *NPC walk-ins*, correctly shape-gated (a peer doesn't barge into private chores). They do NOT count the
  player's solo daily activities — sleep, eat, bathe, self-care feeders, the earning chore — which exist
  in **every** game regardless of shape. A shape with `L3 = 0` has no NPC walk-ins; it still has a full
  daily routine and a feeder floor. Misreading "0 walk-ins" as "no daily loop" is how games ship dead
  kitchens and solo-forever baths.
- Author against the **shape**, never by cloning the gold-standard NPC. Copying the dense family
  distribution onto a peer/dating shape produces Lane 2/3 surfaces where neither belongs.
- **Budgets are always full-game.** Author each arc to its full per-shape budget — every game is the
  complete game. Locked-visible rungs still telegraph the ladder ahead, but the whole budget is the
  target, not a fraction of it.

---

## Three surfaces at one location are SEPARATE canvases
Where the player both interacts with an NPC AND does solo work at one location, that's THREE
independent canvases — the **NPC hub** (Lane 1), the **solo work canvas** (Maya-only,
location-triggered), and a **Lane 3 dispatcher** routing the NPC into the activity. Never put solo
work in the hub menu.

**Pronoun-in-the-verb test:** read each hub menu choice — if the NPC isn't the grammatical object, it
isn't Lane 1. "Pour **her** coffee" / "Tease **him**" → hub ✓; "Take a long shift" / "Wipe the booths"
→ solo work canvas, not the hub ✗.

---

## Lane 1 — hub button (how to write)
**Fingerprint:** `trigger_mode = "manual"`, `is_repeatable = true`, `location` + `npc` set,
`schedules` covering the NPC's window. Base node renders what the NPC is doing; `exit_block.choices`
IS the menu.
- **Choices = verbs with the NPC as object.** Vocabulary by register: **relational** (Talk — build
  trust), **self-display** (Tease, Flash), **contact** (grope, kiss), **explicit** (Have sex).
- **Label = the action, RTS-flat (not a literary sentence).** A choice label is a terse action verb,
  and the flavor lives in the scene the click opens, NOT in the label (one-beat-one-click —
  `references/rts-flat-prose.md`). Strip self-justifying subtext: "Square the crate 😏", not "Square the crate. Ten minutes.
  Tell yourself it's just business." At explicit tiers put the crude word IN the label at the NPC's
  ceiling ("Suck his cock", not "Go down on him"). **Emoji: RTS-style on menu/hub buttons** (🔥 sex/
  seduce · 💬 talk · 🥃 pour · 💰 deal · ↩️ leave) — but **bare on in-loop cascade beats** (RTS's
  `<<linkreplace>>` beats carry none; see `references/sex-loop.md`).
- **Locked-visible ladder:** ship the escalation rungs visible from day 1; a locked rung
  renders greyed with `show_when_locked = true` + its (versioned) `conditions`. Telegraphs the arc.
  **Two render modes — pick deliberately:** OMIT `locked_text`/`locked_text_threshold` → a **bare
  greyed span** showing the action text (the TLS look, the default); set `locked_text_threshold` → a
  clickable **button** that toasts the gate value (RTS `<<NotifyCorruption>>` style). Use the toast
  only if you actually want it — by default omit it.
- **Grey vs hide.** Only *escalation rungs* get `show_when_locked` (they telegraph the ladder).
  Daily-capped rungs, intra-loop beats, and conditional narrative branches **hide** (gated, no
  `show_when_locked`) — you don't telegraph "talk again tomorrow" or a pose inside the sex loop.
- **Hub cap ~5–6 items.** More rungs → make them locked-visible stages, not parallel tasks.
- **Exposure-tier ceiling:** the location's *privacy* caps which rungs may appear — Public
  (talk/look only) / Semi-private (tease/grope) / Private (full ladder). Relationship stats unlock
  rungs *within* that ceiling. Same-NPC hubs stay consistent (shared rung names/thresholds/voice).
- **Base + exit with zero unlocked choices is a complete, valid hub** (the presence floor). Never
  flag-gate the base node — gate the choices.
- **The hub opener is ONE constant paragraph.** Do NOT tier the base node into T0/T1/T2 `[group]`
  blocks — the opening stays the same as the arc escalates; *only the choices* change. Tiering the
  opener is a known failure (an arc whose base node rewrites itself per stat band reads as N different
  scenes instead of one escalating hub). (Period-split hubs are different: a *separate* hub per schedule
  window is fine; tiering one hub's opener by stat is not.)

## Lane 2 — location-entry random ambient (how to write)
**Fingerprint:** `trigger_mode = "random"`, `chance = 0.2–0.3`, `is_repeatable = true`,
`requires_npc`, `schedules`, optional stat `conditions`. Fires on entry, substitutes the hub render.
- **Vocabulary:** pass-by (NPC crosses with a mug), solo-activity glimpse (making coffee alone),
  passive contact (he gropes you as you pass), atmospheric voyeurism (you walk in on something).
- **NOT in Lane 2:** high-agency consummation (that's Lane 1 earned or Lane 4 scripted). Lane 2 is
  brief, charged-but-bounded contact.
- **In-fiction interruption:** lower-tier endings must stop on a real beat — external
  (a kettle, a door), internal (she stops herself), or NPC-stopping (he lets go). Higher tiers blow through.
- Cooldown is engine-handled (3 visits) — don't author your own.

## Lane 3 — dispatcher substitution (how to write)
The hardest lane; RTS's biggest. Two canvases per activity:
1. **Solo-activity host:** its own `[[canvases]]`, `trigger_mode = "manual"`,
   `is_repeatable = true`, `location`, `schedules`. The parent activity (work a shift, shower,
   study) MUST be **authentically not-about-the-NPC** — that's what makes the walk-in land. The
   energy/resource COST of doing it goes in **`costs`** (per-choice on the exit for a multi-intensity
   activity like work −15/−28, or trigger-level for a single-exit chore) — `costs` gates *and* deducts.
   NEVER put the energy spend in `exit_block.effects` (that decrements without gating → cosmetic
   meter) or gate it with `conditions`+`locked_text_threshold` (blue toast-button). `effects` carries
   only the *gains* (money/relation) + `time_progression_minutes`. See `toml-gotchas.md` "Resource gating".
2. **Dispatcher:** rolls dice + checks NPC conditions → HIT routes to the NPC scene, MISS plays solo
   content. The host declares its `substitutions = [...]` rules in `[canvases.trigger]` metadata; on
   entry the engine rolls them (`setup.checkAndSubstituteCanvas`, `v2.py:4875`) and, on a hit, jumps to
   the target's passage. **Each substitution target canvas ships ALL FOUR of:**
   - `substitution_only = true` — keeps it out of the Lane 1/2 location selectors (serialized as
     `substitutionOnly`; the selectors skip it at `v2.py:4034/4064/4095`).
   - `max_triggers_per_day = 1` — once-per-day is the felt cadence (a walk-in that can fire twice in one
     day reads as spam). Serialized as `maxPerDay`, read at `v2.py:10389`.
   - `is_repeatable = true` — so it can fire again on later days (`isRepeatable`, `v2.py:10388`).
   - a `location` — **load-bearing.** The dispatcher resolves its target via
     `setup.getCanvasById(target)` (`v2.py:2751`), whose lookup is built **only** from
     `help_data.locationCanvases` — the per-location registry assembled by iterating `self.locations`
     (`v2.py:10358`+). A target with no `location` never lands in any bucket, so `getCanvasById` returns
     `null` and the dispatcher silently misses (no build error). This is the single most common dead-Lane-3 bug.

   All four are required; missing any is a silent anti-pattern that a green build will NOT catch.
   - **Multiple mutually-exclusive variants at one activity (Pattern B):** give each rule the same
     `exclusive_group = "<name>"` string → ONE shared dice roll partitioned into cumulative buckets,
     fall-to-solo on a claimed-but-failed slot (engine: `v2.py:4919`+, the group branch of
     `checkAndSubstituteCanvas`). Do NOT approximate with summed Pattern A `chance` values — Pattern A
     rules each roll their OWN independent dice (`v2.py:4946`), so summed chances over-fire and the
     "mutually exclusive" intent is lost.
   - **Walk-in direction:** Lane 3 walk-ins use a *loose* presence check (NPC is around — "is he home"
     style); a *strict* exact-location match (NPC must be in this very room) is Lane 2's flavor, not a
     walk-in. Loose presence works by scheduling the NPC at one meta-location that resolves to wherever
     the player is standing.
   - **Cross-room siblings (peep / occupied / caught):** "is he in the *other* room" ships via the
     `npc_at_location` occupancy predicate — the peep, occupied-bathroom, and caught family, the
     cross-room counterpart of the co-location walk-in. Author them ONLY at a **user-confirmed** shared
     private space (`run-mode.md` Mode A; `content-framework.md` §5H). The compact model:
     - **The occupied room stays ENTERABLE; occupancy gates the ACTIVITIES, not the door.** A hard
       `entry_conditions` lock turns "occupied" into a dead-end (the engine renders only the
       `blocked_message` + a Go-back link — no activities), so the peek can't live there. For a shared
       private room you want interactive while occupied (a bathroom): keep it enterable; make the
       **description dynamic** (name the occupant when there is one); and gate each activity by occupancy
       on its own `conditions` — the player's **shower/self-care** shows only when the room is empty
       (`is_absent`); the **peek** shows only when the NPC is in there (`is_present`), and it lives **ON
       the bathroom canvas**, not a hallway. Reserve a hard `entry_conditions` lock for **genuinely
       SEALED** rooms (a locked office you earn a key to) where the dead-end IS the intent.
     - **The peek** — a solo-link on the bathroom canvas, gated on the NPC present, `max_triggers_per_day = 1`:
       ```toml
       [[canvases]]
       id = "peek_npc_shower"
       [canvases.trigger]
       location             = "loc_bathroom"
       is_repeatable        = true
       max_triggers_per_day = 1
       conditions = { version = "1.0", items = [
         { type = "npc_at_location", npc_id = "npc_X", location_id = "loc_bathroom", operator = "is_present" },
       ] }
       ```
       Base beat ≈ **30 flat words** (the image carries it); the player's read is **one `thought_bubble`**,
       not woven into the paragraph. For several housemates, the engine shows whichever one is actually in
       there (each peek gates on its own NPC). Escalate by stat tier — only the **deepest, once-per-arc
       tier** earns a dialog line + capstone density.
     - **Caught (an NPC catches the showering player) — catch-then-react.** Don't make the player
       pre-choose to "leave the door open." The shower is one terse activity; getting caught is
       **automatic by chance**, authored as a `substitution_only` target on the shower's trigger (rolls on
       entry), gated on a `chance` + the NPC's arc + **who's home now** (gate on the NPC's current
       location being a residence room — their schedule puts them home — **never a fixed time-of-day
       window**, so morning catches the morning-home housemates and evening the evening ones for free).
       It routes to a **short interstitial** that gives the agency *as a reaction*: a corruption-gated
       **flash/show vs cover-up/shut-it** choice. Only the bold branch routes into the longer capstone
       payoff. `max_triggers_per_day = 1` is the re-fire guard.
     - **Overhear** = the same occupancy gate, authored audio-only (no image).

     Engine: the `npc_at_location` condition type lives in `setup.triggerConditionsSatisfied`
     (`v2.py:3711`) — operator `is_present`/`is_absent`, optional `npc_id` (omitted = the room itself
     occupied/empty). It evaluates in canvas, choice, substitution, AND `entry_conditions` (one canonical
     evaluator). The condition block needs `version = "1.0"` or it fails OPEN. Register stays RTS-flat
     (~30w base, scheme in a `thought_bubble`); the capstone it routes into is where density is earned.
     *(Note: two-NPC co-presence — "catch two of them together" — needs a separate engine feature the
     renderer doesn't have yet; only the player-is-a-party configs above are buildable today.)*
   - **Rising frequency (the saturation curve):** a single substitution rule's `chance` is a fixed
     constant, so one rule = a flat hijack rate forever — the tell of a routine that never escalates. To
     make the hijack **climb** (early = never; late = most visits), **stack several Pattern A rules on the
     same host**, one per corruption band, with **disjoint `gte`/`lt` conditions** so exactly one band is
     eligible at a time, and a **`chance` that rises per band**:
     ```toml
     # on the solo-activity host's [canvases.trigger]
     substitutions = [
       { target_canvas_id = "scene_npc_walks_in", chance = 0.10,
         conditions = { version = "1.0", items = [
           { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 10 },
           { type = "trait", subject = "player", trait_key = "corruption", operator = "lt",  value = 25 } ] } },
       { target_canvas_id = "scene_npc_walks_in", chance = 0.35,
         conditions = { version = "1.0", items = [
           { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 25 },
           { type = "trait", subject = "player", trait_key = "corruption", operator = "lt",  value = 45 } ] } },
       { target_canvas_id = "scene_npc_walks_in", chance = 0.70,
         conditions = { version = "1.0", items = [
           { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 45 } ] } },
     ]
     ```
     Each band item is the engine's typed `trait` condition (`subject = "player"`, `trait_key`,
     `operator`, `value` — verified `v2.py:3508`; `gte`/`lt` are real operators, `v2.py:3420`). Because
     the bands are disjoint, only the matching band's rule passes `_tryRule`, and each Pattern A rule rolls
     its OWN `Math.random() < chance` (`v2.py:4946`) — so the felt frequency steps up band by band. (Each
     `conditions` block needs `version = "1.0"` or it fails OPEN. This is the Pattern A path, NOT
     `exclusive_group` — these rules don't share a dice roll; they're gated apart by band so only one is
     ever live. To gate on the corruption *tier* 0–5 instead of the raw 0–100 odometer, use
     `type = "corruption_level"` — `v2.py:3700` — but for a saturation curve the raw-trait bands above are
     what you want.)
- **Vocabulary:** he walks in (mid-activity), he arrives while she's vulnerable, innocent setup →
  charged shift. The setup is genuinely a chore; the seduction happens *to* her.
- **A solo activity is also the game's earning/utility loop** — "work a shift" earns money and is the
  natural Lane 3 host. Splitting work (host) from the NPC hub (Lane 1) is the "three surfaces are
  separate canvases" rule above in action.
- **Self-care chores are first-class hosts too — not just "work a shift."** Shower, bath, sleep, eat are
  the highest-volume routine surface; at a location an NPC shares, each carries a dispatcher by default.
  A self-care canvas authored as a bare restore (no solo-lewd
  branch, no substitution) where an NPC is present is the **dead-bath anti-pattern** — it throws away the
  game's biggest content channel.
- **A solo host can fire a PLAYER-LEWD event, not only an NPC walk-in** (the player thread —
  `references/content-framework.md` §2; designed at `step-4-deep-design.md` Pass 1, structured at
  `step-5-blueprint.md` Pass 1).
  The walk-in (the dispatcher `if`) and the feeder (the solo `else`) are the **same canvas, not two
  systems** — the *fused unit*. The solo branch is the **player/world lewd
  track** — solo self-acts, location flashing/exhibitionism, public dares, job-lewd — the *base activity
  itself being lewd*, gated on the **player** `corruption`/`exhibitionism` tier and raising those odometers
  every time, hit or miss. This is the **corruption-feeder economy**: the supply that makes NPC seduction
  floors (the player-corruption gates on NPC seduction rungs) reachable. *Which* feeders exist and what each is
  worth is designed in the **player thread** (Step 4 story → Step 5 blueprint, `content-framework.md` §2E
  count); they then live **on the host canvas** as its solo branch. A game with rich NPC arcs but no feeder
  floor on its daily loop starves its player odometer (the Last Call finding).

## Lane 4 — capstone (how to write)
**Fingerprint:** `priority ≥ 9` (typically 9–12), `trigger_mode = "manual"`, auto-fire on location
entry when conditions match, flag-gated + sets a one-shot flag on completion. **Repeat field is one of
two forms:**
- `is_repeatable = false` — once it fires, done; OR
- `is_repeatable = true` **+ a self-gate on its own setter flag** — the "retry" variant. The
  self-gate is a normal typed trigger condition on its OWN completion flag, e.g.
  `{ type = "flag", subject = "player", flag_key = "<its_setter_flag>", operator = "is_false" }`
  ("flag_is_false" is doctrine shorthand — emit the typed condition, NOT a literal `flag_is_false`
  key, which the engine ignores). The canvas re-fires next eligible time *until* its flag is set, so
  a **Refuse branch that doesn't set the flag keeps it alive** (the branching-fork retry rule below).
  Use this whenever a branching capstone has a decline path.

Three types: **A** linear deterministic, **B** branching choice (both branches playable, diverge in
downstream effect), **C** quest-chain step. **Type-B forks follow the branching-fork rules:** both
branches written good-faith (no "obviously wrong" decline), the choice diverges in *downstream* effect
not on-the-spot reward, the fork sits at the **terminal** beat (don't branch mid-scene then re-converge),
a refuse path is retryable (doesn't burn the flag — the retry variant above), and the fork doesn't
compound (one decision per capstone, not a tree). Per-NPC capstone budget per shape (table above). Voice:
Tier-3 earned (once-only, so the prose can spend).

**Gate a capstone on the ODOMETER, never the throttle** (`references/trait-design.md` "Throttle vs
odometer"). A capstone is a one-shot permanent milestone, so it gates on a **permanent** axis —
`player.corruption` (the depravity odometer) and/or `npc.relation`/`npc.corruption` — **plus its flag
chain**. NEVER gate it on `arousal`: that's a **throttle** (resets at climax), which belongs on the
**repeatable** sex-loop content, not a one-shot. Pick the odometer by who-initiates: NPC-initiated
dating → `npc.relation`; NPC-initiated seduction → player `corruption` + the relationship flags (the
NPC's `arousal` throttle then drives the repeatable loop afterward, and colors the hub prose
heat-framed). The split-spine failure to avoid is about an **odometer**: a relation/own-corruption
meter the hub builds that the milestone never reads (LC's Marcus — relation gates only capstone #1).

**The repeatable layer comes after.** Capstones are the once-only *first* time; the replayable
explicit surface that follows (opened from the hub once the first-night flag is set) is the
**sex-loop menu** — its own pattern, see `references/sex-loop.md`.

## Voice register
- **Lane 1 / 2 / 3:** RTS-flat default — ~30-word caption density, direct/crude diction per the NPC's
  **per-tier vocab ceiling** (declared in its design brief; the ceiling model is
  `references/kink-ceilings.md`, default-to-maximum-explicit). Re-readable (these repeat).
- **Lane 4 capstones:** Tier-3 EARNED — interior monologue + layered sensory detail +
  character-distinguishing diction. Once-only, so the prose can spend.
- **Choice labels** are tighter than the prose — label = action, no subtext, crude-in-label at the
  ceiling, emoji on menu buttons / bare on in-loop beats (Lane 1 above + `references/sex-loop.md`).
- **Mode, not just density.** The flat register governs how *dense* the prose is, not whether people
  speak. Where a beat is an actual exchange — player ↔ NPC, or a group in one room — carry it in `dialog`
  blocks (their words, interruptions, refusals), not a narrated summary of what was said; RTS plays
  dialogue even in its explicit scenes (the full mode-not-density rule is `references/rts-flat-prose.md`).
  **Lean hardest at the hot beats** (capstones, sex, confrontations): narrating the encounter as summary
  is the worst drift — play them. Multi-party beats give each present NPC a voiced moment under the
  no-monologue cap (one terse beat each, not a speech). EXEMPT only when **no one's there to speak**:
  solo activities, voyeur/peek where you're unseen, and the interior-monologue stretches of a capstone.
  A present NPC is not exempt — even a mood glimpse gives them one terse line.

## Runtime rendering rules (live-verified — these bite even when the build is green)
The location screen renders four separate paths; a canvas only appears if it matches the right one:
- **An NPC hub needs `npc` set, not just `requires_npc` — separate fields.** `requires_npc` gates
  presence only; `npc` sets the `npcId` that `renderNpcPortraits` requires
  (`selectNpcPortraitCanvasesForLocation` skips `!c.npcId`, `v2.py:4065`). A repeatable hub with
  `requires_npc` but no `npc` renders as a flat **solo link**, not a portrait. Lane 2 ambients likewise
  need `trigger_mode = "random"` + `chance` or they render as links instead of rolling on entry. Set
  both on hubs; random+chance on ambients. (Full engine trace + grep guard: `toml-gotchas.md`.)
- **NPC first-contact one-shot → make it AUTO-FIRE**, NOT an NPC-portrait canvas. `renderNpcPortraits`
  skips non-repeatable canvases, so a one-shot *with* `npc`/`requires_npc` set renders NOWHERE (it's
  neither a repeatable portrait nor an auto-fire). Author it like the boot canvas: `is_repeatable=false`,
  `priority≥9`, **no `npc`/`requires_npc`**, gated on flags; it auto-fires on entry and sets the
  `<npc>_opened_up` flag. The ongoing **hub** (repeatable, `npc` set) renders the portrait from then on.
- **Solo activity → no per-canvas `schedule`** if it should be available whenever the location is
  reachable. A `schedule` block on a solo activity suppressed its button (match the proven
  `activity_make_tea` shape: location + `is_repeatable` + `priority` + optional `conditions`/`substitutions`,
  no `schedule`). Gate availability via `conditions` and location reachability instead.
- **Distinct `name` per canvas.** A non-repeatable first-contact and its repeatable hub sharing a
  `name` collide in the name-group selector — give them different `name`s.
- **A hub portrait renders only while the NPC is present** (`getNpcLocation(slug).location == here`).
  If a hub won't show, verify the NPC's `[[npcs.schedules]]` actually places them at that location at
  the current time (and that schedule slugs resolved). Presence is the gate, not just `is_active`.
- **Presence-on-nav is FREE — surface it.** The nav cards already paint avatars of the NPCs scheduled at
  each *destination* (`getNpcsPresentAtLocation`), so the player can see *who's there* before spending
  time to travel — the same schedule source the hub + the occupancy door read (see
  `references/location-design.md` on presence-on-nav).
  You get this just by authoring schedules + hubs where the NPCs actually are; it's a reason to anchor a
  hub at the NPC's real location, not a convenient one. (Pairs with travel-friction: see who's home, then
  decide if the trip is worth the hour.)

## Beat type → lanes (what a beat authors)
- `npc_intro` → a **designed first-encounter beat** (pretext + name-on-page + hook-as-want → fire once → open the hub — the 7-step Renner template, `references/npc-intro.md`), THEN the NPC's **Lane 1 hub(s)** (one per schedule row) + optionally the first **Lane 2** ambient. Cold-start enterable; the dramatized auto-fire one-shot is the introduction, the repeatable hub follows it gated on `<npc>_opened_up` (runtime shape: Runtime rendering rules above).
- `arc_escalation` → add **Lane 1 rungs** (locked-visible) AND the **Lane 2/3** content that lights up at those thresholds — per the shape's budget, respecting empty cells.
- `economic` → usually a **solo work activity** (Lane 3 host that earns money) + its dispatcher; keep it OUT of any NPC hub (the work-is-a-separate-canvas rule).
- `cross_npc` → an NPC as interruptor in another's **Lane 3** ending, or a shared scene.
- `capstone` → a **Lane 4** one-shot gating a milestone.
- `location_reveal` / `story_turn` → structure + the scenes the new place/turn needs (often a hub + ambients).
