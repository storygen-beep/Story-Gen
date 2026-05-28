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

**Brief template:** see `doctrine/06_design_brief_template.md` *(Batch 2+ — pending; for now use Doc 31 Frank brief + Doc 53 Marge brief in `28th_april_TLS_Phase2_Redesign/` as templates)*.

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

### §2.6 — D50-R6: Goals labels in voice

**Rule:** `goals[i].label` MUST be in Maya-voice or in-character framing — *"Maya's corruption,"* *"Diana noticing,"* *"Yard help,"* *"Ryan trust."* Never raw trait keys like `npc_diana.awareness` or `core_traits.corruption`.

**Why this rule exists:** the label renders directly under the 🎯 frame in the player UI. It's a narrative surface, not a debug surface.

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

**Why:** Pattern B requires either engine-level partition support (Doc 67 §5.1 extension) or approximation via summed chance values. Both have costs. Pattern A is the cheap default.

**Engine status (2026-05-26):** Pattern B is **NOT YET ENGINE-SUPPORTED.** The current engine evaluates each substitution rule's dice independently. If Pattern B intent arises during authoring, EITHER defer the authoring until `exclusive_group` extension ships, OR accept Pattern A approximation knowing the math + fall-through divergence documented in `doctrine/02_three_lanes_plus_capstone.md` §4.6.2.

**Don't write Pattern B authoring as if it works natively** — the silent divergence will produce wrong probabilities + wrong fall-through behavior, neither of which surface as build errors.

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

## §6 — Pre-ship checklist (Appendix-style)

Run before any commit that includes new canvas / capstone / quest card / Lane 3 substitution.

### §6.1 — Per-canvas checks

- [ ] **D56-R1** — Hub canvas has ONE opener paragraph, not tiered (unless legitimate world-state framing)
- [ ] **D56-R2** — If `[group]`-tier-routed, T0/T1 endings land on in-fiction interruption
- [ ] **D56-R5** — `guide` field present + in plain-English recipe form
- [ ] Image-first composition; ≤ 30-word caption density (Lane 1/2/3); Tier-3 register only at Lane 4 capstones
- [ ] Stat-effect macros on cascade beats, not just on entry (P6)
- [ ] Locked-click failures pure information (no stat drain) (P7)
- [ ] No legacy vocabulary (Pattern A–J; ENI-persona references; whiteboard goals; etc.) — see `00_LEGACY_IGNORE.md` §4

### §6.2 — Per-Lane-3 substitution checks (D67-R1–R7)

- [ ] **D67-R1** — Parent activity is a separate `[[canvases]]` entry (not a sub-block of the location hub)
- [ ] **D67-R2** — Stat cost placement decided (`exit_block.effects` vs `pre_substitution_effects`)
- [ ] **D67-R3** — Menu-level gates on location button; dispatcher trusts the menu
- [ ] **D67-R4** — Multi-NPC competition defaults to Pattern A; rule order = narrative priority
- [ ] **D67-R5** — Pattern B only if mutually-exclusive variants; engine-extension status known
- [ ] **D67-R6** — `requires_npc` predicate matches walk-in direction (loose for Lane 3; strict for Lane 2)
- [ ] **D67-R7** — Substitution target has `max_triggers_per_day = 1` + `substitution_only = true`
- [ ] **D56-R3** — Substitution count respects per-arc-shape Lane 3 budget (family 4–7, slow-burn 1–3, peer 0, service 0, antagonist 0 own)

### §6.3 — Per-capstone checks (D57-R1–R5)

- [ ] **D57-R1** — Trigger fingerprint: `is_repeatable = false` (or `true` + self-gate); `priority ≥ 9`; `conditions` include flag-is_false gate; setter-flag effect on exit choice
- [ ] **D57-R2** — Default to Type A; Type B only if branches diverge downstream
- [ ] **D57-R3 / D50-R1** — Capstone is referenced by some quest_card's `ready_canvas` OR has `# off-panel:` comment
- [ ] **D57-R4 / D50-R4** — Predecessor capstone sets the flag this one requires (chain continuity)
- [ ] **D57-R5** — Schedule + location match the fiction
- [ ] **§3.8 voice** — Cascade prose is Tier-3 (specific, layered, character-distinguishing). No Tier-3 spillage in related Lane 2/3 canvases.

### §6.4 — Per-Type-B capstone checks (F1–F5)

- [ ] **F1** — Both branches playable in good faith (Refuse isn't a punishment-button)
- [ ] **F2** — Real divergence in flag-effect, NPC arc, or downstream content
- [ ] **F3** — Fork is at the cascade's terminal beat
- [ ] **F4** — Refuse-path flag policy matches fiction (retry-allowed vs irreversible)
- [ ] **F5** — Not compounded with tier-routing AND multi-step downstream — only one structural device beyond the fork

### §6.5 — Per-quest-card checks (D50-R1–R6)

- [ ] **D50-R1** — Mode declared (capstone / mechanic / hybrid). No `txt_only`.
- [ ] **D50-R2** — Climbing-bullet present when `ready_canvas` has trait gates strictly above card's `when`
- [ ] **D50-R3** — Terminal placement: any `terminal = true` is the LAST card in the NPC chain
- [ ] **D50-R4** — Chain continuity: every "post-X" card has a sibling "pre-X" card pointing at X's setter
- [ ] **D50-R5** — Pure-mechanic cards carry `# unlocks:` comment
- [ ] **D50-R6** — `goals[i].label` in Maya-voice; no raw trait keys
- [ ] **§2.7** — Pure-mechanic chains: each `when` has bounded threshold range; transitions are atomic

### §6.6 — Per-slice / per-arc checks (D56-R3, R4, R7)

- [ ] **D56-R3** — Per-arc-shape Lane 3 budget matches table (family 4–7, slow-burn 1–3, peer 0, service 0, antagonist 0)
- [ ] **D56-R4** — Sidebar surfaces in-scope NPC locations + key stats per the arc's register
- [ ] **D56-R6** — No `txt_only` quest cards in shipped TOML
- [ ] **D56-R7** — Design brief written + canvas distribution matches the brief's declared budget
- [ ] **§3 per-arc distribution** — Canvas count per arc within range (family/ambient 25–35; slow-burn 10–15; peer/dating 8–12; service 6–10; antagonist 6–10)

---

## §7 — Anti-patterns (consolidated, per-rule cross-reference)

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
- **Substitution target without `substitution_only = true`** — violates D67-R7 + pre-ship check §6.2.

---

## §8 — Cross-references

### Source docs

- `28th_april_TLS_Phase2_Redesign/56_RTS_Principles_and_TLS_Alignment_Doctrine.md` §4 — R1–R7
- `28th_april_TLS_Phase2_Redesign/50_Quest_Card_Shape_Doctrine.md` §4 — R1–R6
- `28th_april_TLS_Phase2_Redesign/57_Capstone_Doctrine.md` §4 + §7 — R1–R5 + F1–F5
- `28th_april_TLS_Phase2_Redesign/67_Solo_Activity_Design_and_Multi_NPC_Dispatcher_Doctrine.md` §6 — R1–R7

### Sibling doctrine files

- `doctrine/01_rts_principles.md` — the principle each rule operationalizes
- `doctrine/02_three_lanes_plus_capstone.md` — the mechanism each rule sits inside
- `doctrine/03_arc_shapes.md` — the per-arc-shape distribution that D56-R3 + R7 reference
- `doctrine/05_rts_flat_prose.md` *(Batch 2+ — pending)* — voice register that capstone Tier-3 + Lane 1/2/3 RTS-flat enforces
- `doctrine/06_design_brief_template.md` *(Batch 2+ — pending)* — R7 brief structure
- `doctrine/07_anti_patterns.md` *(Batch 2+ — pending)* — extended anti-pattern catalog (Doc 54's 27 failure modes)

### Validator hooks

- `_validate_quests_cards` (`template_import.py:4469`) — wires D50-R1–R4 + D56-R6
- `_validate_predicate_field_names` (`template_import.py:1098`) — warns on field-name typos
- `_validate_effect_field_names` (`template_import.py:1077`) — warns on field-name typos
- Sidebar trait declaration validator (`template_import.py:2382–2547`) — hard-rejects undeclared traits

### Engine status (rules with pending engine work)

- **D56-R5** `guide` field — doctrine-locked; schema field pending Doc 62 PRD
- **D67-R5** Pattern B `exclusive_group` — doctrine-deferred per Doc 56 §9 (build engine when load-bearing)
- **D67-R2** Pattern C `pre_substitution_effects` — ✅ shipped Doc 69 Item 2 (2026-05-27)

---

**End of file.** Next: `doctrine/09_trait_catalog.md` for canonical trait vocabulary.
