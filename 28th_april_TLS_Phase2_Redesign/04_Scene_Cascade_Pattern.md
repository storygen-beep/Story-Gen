# 04 — Scene Cascade Pattern

> **Created 2026-04-29.**
> The canonical scene shape: how a single repeatable canvas branches internally based on stage flags + time-band + tier.
> Drawn directly from RtS evidence (`DadWashDishesSex`, `MarcusBedroomSex1`, `BrotherShowerSex`, `StudyWithMarcus` source readings).
> Worked example: `kitchen_with_frank` end to end.
> Inherits vocabulary from `01_Repeatable_First_Doctrine.md`. Consumes stages from `02_NPC_Stage_Chains.md`.

---

## What a scene cascade is

A **cascade** is the internal branching inside a single repeatable scene canvas. The scene reads stage flags and picks a branch. Inside that branch, it may further split on time-band, then on per-act tier. Each branch contains the prose, dialogue, and effects for that combination of state.

The shape is borrowed verbatim from RtS. From the source of `DadWashDishesSex` (4848 chars, repeatable):

```
<h1>WASHING DISHES</h1>
<h3>You're elbow-deep in suds when you feel $npc.Dad.relationship's presence behind you.</h3>
<<Speech Player "$npc.Dad.relationship! Stop it!">>
<<Speech Dad "What? I'm just trying to help...">>
<<if StageOneCorruption($npc.Dad)>>
    <<linkreplace "See what he wants">>
        <h3>He sheds his clothes...</h3>
        <<Speech Dad "I can't help myself...">>
        <<linkreplace "You feel a sharp thrust">>
            <h3>His cock buries itself deep inside you...</h3>
            ... cascade continues ...
<<else>>
    <h3>After saying this, he turns around and leaves, you are confused...</h3>
    <<StageNotification $npc.Dad 1>>
<</if>>
```

One canvas. Two top-level branches gated on `StageOneCorruption($npc.Dad)`. The Stage-0 branch (else) is short, terse, and *advances the stage flag on exit* (`<<StageNotification $npc.Dad 1>>`). The Stage-1 branch is a linkreplace cascade revealing beats progressively. **The same canvas, on the next visit, picks a different branch because state moved.**

This is what TLS's scene canvases will do.

---

## Engine note — the TLS implementation of the RtS pattern

TLS's canvas schema doesn't have a `<<linkreplace>>` macro natively in the block-types. Per master spec §2.5, the functional equivalent is one of two approaches. **This doc locks the choice.**

**Locked approach: single-node, multiple `group` block variants gated on conditions.** The scene is one canvas with one node. The node's `blocks` array is a sequence of `group` blocks, each with `conditions` matching a specific (stage, time-band, tier) combination. The engine renders the matching group(s) and skips the others. The exit_block re-fires the canvas after each beat for cascades that need progressive reveal across re-entries (using a `quest_progress_<scene>` counter incremented on exit).

This approach was chosen over the multi-node alternative because:
1. It keeps the entire cascade visually local to one node — easier to read and audit.
2. It maps directly to RtS's `<<if StageOneCorruption>>...<<elseif StageTwoCorruption>>...<<else>>` shape.
3. Per master spec §2.5, group blocks with conditions are an existing engine primitive — no schema change.

The multi-node approach (3–10 nodes routed by quest-progress flags on entry) remains valid for scenes that genuinely need separate page reveals, but is not the default.

---

## The cascade skeleton

Every scene cascade has the same outer shape. Stage flag at the outermost gate; time-band optional; tier (per-act counter) optional and innermost. The order is fixed.

```toml
# Illustrative — schema PR will finalize field names.
[[canvases]]
id = "scene_<location>_with_<npc>"
name = "<short label>"

[canvases.trigger]
location = "<loc_x>"
is_repeatable = true
priority = <2..8>                  # higher than hub, lower than one-shots
is_active = true
chance = <0.0..1.0>                # optional; trigger.chance gates firing
conditions = { items = [
  # NPC-presence + stage minimums + time-band minimums
] }

[[canvases.nodes]]
id = "base"
blocks = [
  { type = "image", props = { ... search_queries = [3..5 entries] ... } },

  # Stage 0 branch — outermost gate
  { type = "group", conditions = { ... frank_stage == 0 ... }, blocks = [
    # Optional time-band split inside the stage
    { type = "group", conditions = { ... time_band in [M] ... }, blocks = [
      # Optional tier split inside the time-band
      { type = "paragraph", content = "<Stage 0, morning, tier 1 prose>" }
    ]},
    # Tier-2 morning content, etc.
  ]},

  # Stage 1 branch
  { type = "group", conditions = { ... frank_stage == 1 ... }, blocks = [ ... ]},

  # Stage 2 branch
  { type = "group", conditions = { ... frank_stage == 2 ... }, blocks = [ ... ]},

  # Stage 3 branch
  { type = "group", conditions = { ... frank_stage == 3 ... }, blocks = [ ... ]}
]
exit_block = { type = "choices", choices = [ ... ] }
```

The stage-gate group is exclusive (engine renders the first matching group; subsequent stage groups are skipped). Time-band and tier groups inside a stage are also exclusive within their axis.

---

## Precedence order — locked

When a scene branches on multiple axes, the order is fixed:

```
Stage flag (outermost)
  └── Time-band
        └── Tier / per-act counter (innermost)
```

**Stage is always the outermost gate.** Stage represents a regime change in the relationship; the player should never see Stage-1 prose followed by Stage-2 prose in the same visit.

**Time-band sits inside stage.** Within a stage, the kitchen at morning vs evening can read differently; the register doesn't change — the surface does (Frank reading the paper at M vs Diana cooking at DINPREP).

**Tier sits innermost.** Per-act counters (`frank.tease_count`, `lean_by_desk_count`) gate progressive reveal inside a stage's branch. Tier escalation happens within a regime, not across regimes.

**No axis is allowed to skip a level.** A cascade does not gate "tier 3 + Stage 1" without also gating Stage 1 outermost. This is what keeps the cascade auditable.

The reason for the lock: cascade nesting depth is the single fastest way to make a scene unreadable. Locking the order means an author looking at any group block can compute its meaning by reading the gates from outside in: "Stage 2, evening, second visit." Reordering the axes per-scene would force the reader to reconstruct the intended hierarchy from arbitrary gate combinations.

---

## Time-band overlay

Time-bands inside a stage are optional. Use them when the same regime feels meaningfully different at different points in the day. Don't use them when the difference is just "morning prose vs evening prose" with no register or content change — that's atmospheric noise.

The TLS time bands per master spec §1 are: EM, M, A, DINPREP, DIN, E, N, LN. A scene typically uses 2–3 of these (the bands when the NPC is scheduled at this location).

```toml
# Inside a Stage-1 branch:
{ type = "group", conditions = { ... time_band in [M] ... }, blocks = [
  { type = "paragraph", content = "Frank at the table with the paper, coffee cooling. He looked up when she came in." }
]},
{ type = "group", conditions = { ... time_band in [DINPREP] ... }, blocks = [
  { type = "paragraph", content = "Frank at the counter with the receipts. The kitchen smelled like onions." }
]}
```

Two short paragraphs. Same Stage-1 register. Different surfaces because the band is different. The author writes one paragraph per band, not a 700-word literary version that tries to cover both.

---

## Probability gating with `trigger.chance`

Per master spec §2.4 and §0 of the engine PRD: `trigger.chance` is already supported (verified at `v1.py:3216, 3585`). The engine evaluates `chance` at trigger time; the scene fires only when the random roll succeeds AND its other conditions match. If the roll fails, the engine routes to the next-highest-priority canvas at this location — usually the hub.

The RtS pattern: not every visit to the kitchen produces a Frank encounter. Even when Frank is home AND aroused (per RtS) AND the time-band matches, the encounter fires roughly 1-in-3. Verified at `WashDishes` source: `<<if random(1,3) == 1 && $npc.Dad.arousal > 0 && IsNpcAtHome("Dad")>>`. The 1-in-3 makes the world feel alive instead of mechanical.

For TLS Phase 2, scenes that route through an activity router (washing dishes, cooking) get `chance = 0.25..0.40` — most days the activity is just the activity, occasionally Frank shows up. Scenes triggered directly from a hub button ("Talk with Frank") fire deterministically when their conditions match.

```toml
[canvases.trigger]
location = "loc_kitchen"
is_repeatable = true
priority = 6                       # higher than hub_kitchen (priority 1)
chance = 0.30                      # 30% of qualifying visits
conditions = { items = [
  { type = "stage", subject = "frank", value_gte = 1 },
  { type = "schedule", npc = "frank", time_band = ["M", "DINPREP"] },
  { type = "flag", flag_key = "talked_to_frank_today", operator = "is_false" }
]}
```

When the chance roll fails, the player sees the hub. When it succeeds, the scene cascade picks the right Stage-X branch.

---

## Tier overlay (per-act counter)

Tier is the innermost axis. It's used inside an explicit-tier scene branch where the same act unfolds across multiple visits with progressive reveal. Per master spec §2.5b: numeric counters (`lean_by_desk_count`, `frank.tease_count`) increment on scene completion; the cascade gates beat depth on counter values.

The RtS pattern: `getQuestProgress("StudyWithMarcus") > 2` reveals beats 4–6; `> 4` reveals beats 7–9. Same passage; the counter accrues across visits; later visits see deeper cascades.

For TLS, tier overlay is used in Stage-3 office tease scenes and in diner T1/T2/T3 shifts (per master spec §7). Most Stage-0/1/2 branches don't need tier overlay — they're shorter scenes with a fixed beat count.

```toml
# Inside a Stage-3 office branch:
{ type = "group", conditions = { ... tease_count >= 0 ... }, blocks = [
  { type = "paragraph", content = "<beat 1: lean against the desk>" },
  { type = "dialog", content = "...", props = { speaker = "npc", npcId = "frank" } }
]},
{ type = "group", conditions = { ... tease_count >= 2 ... }, blocks = [
  { type = "paragraph", content = "<beat 2: she stays longer this time>" }
]},
{ type = "group", conditions = { ... tease_count >= 4 ... }, blocks = [
  { type = "paragraph", content = "<beat 3: register-marker line>" }
]}
```

Beats 2 and 3 are skipped on the first visit (counter is 0); they appear on subsequent visits as the counter accrues. The exit_block increments the counter.

---

## Effect blocks — what a scene may and may not flip

A cascade carries effects. The doctrine constrains which flags it's allowed to flip.

**A scene may flip:**
- Its own NPC's stage flag (`frank_stage`), but only when the helper for the next stage clears, AND only via the agreed advancement mechanism (helper-driven or one-time guard branch).
- Its own NPC's relationship traits (`frank.trust`, `frank.arousal`, `frank.love`) — small increments, per beat.
- Player traits (`corruption`, `energy`, `fitness`) — proportional to the act.
- Per-act counters scoped to this scene (`frank.tease_count`, `lean_by_desk_count`).
- Daily-reset flags it sets (`talked_to_frank_today`).
- One-time guards inside its own cascade (`frank_caught` set inside the catch branch; `frank_cracked` set inside the Crack branch).

**A scene must NOT flip:**
- A different NPC's stage flag. Frank's kitchen scene does not advance Ryan's arc.
- Plot flags belonging to a different arc surface.
- Helper-derived flags directly. Helpers are computed on canvas entry; they're outputs, not inputs.

**A scene should NOT flip the stage flag without the helper clearing.** If `frank_stage_2()` returns false, `frank_stage = 2` should not be set. The helper is the contract; the stage flag follows.

---

## Worked example — `kitchen_with_frank`

The scene that lives at `loc_kitchen` and carries Frank's chain through the kitchen surface. References `02_NPC_Stage_Chains.md` Frank table for stage definitions.

### Scene-level metadata

```toml
# Illustrative — schema PR will finalize field names.
[[canvases]]
id = "scene_kitchen_with_frank"
name = "Kitchen — Frank"

[canvases.trigger]
location = "loc_kitchen"
is_repeatable = true
priority = 6                                  # higher than hub_kitchen
chance = 0.30                                 # 30% of qualifying visits
is_active = true
conditions = { version = "1.0", items = [
  { type = "stage", subject = "frank", value_gte = 0 },
  { type = "schedule", npc = "npc_frank", time_band = ["M", "DINPREP"] }
] }
```

The scene fires only when Frank is scheduled at the kitchen (M or DINPREP). It never fires when Frank is at the office or out. The 30% chance keeps the kitchen feeling like a kitchen most of the time.

### The cascade

Outermost gate: stage. Each stage's branch is one paragraph (Stage 0/1/2/3) plus optional dialog. Stage 1 is shown expanded with time-band overlay; the others are sketched at one branch each.

```toml
[[canvases.nodes]]
id = "base"
blocks = [
  { type = "image", props = {
    file = "scenes/kitchen_with_frank.jpg",
    description = "Frank at the kitchen table, morning light",
    search_queries = [
      "older man at kitchen table reading newspaper morning sunlight",
      "rural Southern kitchen interior breakfast",
      "older man with coffee mug at small farmhouse kitchen table",
      "morning light on wooden kitchen table receipts and paper",
      "calm domestic morning kitchen scene older man"
    ]
  }},

  # ─── STAGE 0 — Suspicious landlord ─────────────────────────
  { type = "group", conditions = { ... frank_stage == 0 ... }, blocks = [
    { type = "paragraph", content = "He looked up from the paper when she came in. He didn't say anything. The kettle was already cool." },
    { type = "dialog", content = "Morning.", props = { speaker = "npc", npcId = "npc_frank" } },
    { type = "paragraph", content = "He folded the corner of the paper and went back to it." }
  ]},

  # ─── STAGE 1 — Grudging warmth ─────────────────────────────
  { type = "group", conditions = { ... frank_stage == 1 ... }, blocks = [

    # Stage 1, M band — morning surface
    { type = "group", conditions = { ... time_band in [M] ... }, blocks = [
      { type = "paragraph", content = "Frank had the receipts in two stacks at his elbow. He looked up." },
      { type = "dialog", content = "You any good with numbers?", props = { speaker = "npc", npcId = "npc_frank" } },
      { type = "paragraph", content = "She nodded once. He pushed the smaller stack across to her side of the table." }
    ]},

    # Stage 1, DINPREP band — late-afternoon surface
    { type = "group", conditions = { ... time_band in [DINPREP] ... }, blocks = [
      { type = "paragraph", content = "Frank at the counter with the church-bulletin envelope. The kitchen smelled like onions." },
      { type = "dialog", content = "Diana's setting up. Don't get in her way.", props = { speaker = "npc", npcId = "npc_frank" } }
    ]}
  ]},

  # ─── STAGE 2 — Restrict ────────────────────────────────────
  { type = "group", conditions = { ... frank_stage == 2 ... }, blocks = [
    { type = "paragraph", content = "He didn't look up when she came in. He waited until she had the kettle on." },
    { type = "dialog", content = "Porch needs sweeping. Before you sit.", props = { speaker = "npc", npcId = "npc_frank" } },
    { type = "paragraph", content = "She set the kettle down. Yes, she said, with her body, with the way she crossed the kitchen back to the door." }
  ]},

  # ─── STAGE 3 — Tease under compliance ──────────────────────
  { type = "group", conditions = { ... frank_stage == 3 ... }, blocks = [
    { type = "paragraph", content = "Frank at the table with his coffee cold beside him. He had been watching the door for some time before she came through it." },
    { type = "dialog", content = "Took your time.", props = { speaker = "npc", npcId = "npc_frank" } },
    { type = "paragraph", content = "She crossed to the kettle. He watched her cross to the kettle. The kitchen was the kitchen and was not the kitchen." }
  ]}
]

exit_block = { type = "choices", choices = [
  # Stage 0 exit — only visible at frank_stage == 0
  { text = "Pour your coffee.", targetType = "location", locationId = "loc_kitchen",
    time_progression_minutes = 15,
    effects = [
      { targetType = "npc", npcId = "npc_frank", trait = "trust", op = "add", value = 1 },
      { targetType = "player", trait = "energy", op = "add", value = -3 }
    ],
    flagEffects = [
      { targetType = "player", flag = "talked_to_frank_today" }
    ],
    conditions = { items = [{ type = "stage", subject = "frank", value_eq = 0 }] }
  },

  # Stage 1 exits — visible at frank_stage == 1
  { text = "Sit and run the numbers with him.", targetType = "specific",
    canvasId = "activity_bookkeeping_with_frank",
    time_progression_minutes = 60,
    conditions = { items = [{ type = "stage", subject = "frank", value_eq = 1 }] }
  },
  { text = "Pour your coffee and go.", targetType = "location", locationId = "loc_kitchen",
    time_progression_minutes = 15,
    conditions = { items = [{ type = "stage", subject = "frank", value_eq = 1 }] }
  }

  # Stage 2/3 exits omitted for brevity — same shape, different effects.
]}
```

### What this scene flips

| Field | Conditions | Reason |
|---|---|---|
| `frank.trust += 1` | Stage 0/1 exits | Talking + helping accrues trust |
| `frank.bookkeeping_count += 1` | Stage 1 "run the numbers" exit (set by `activity_bookkeeping_with_frank`, not here) | Counter that gates `frank_stage_1()` → Stage 2 transition (via helper after enough increments + the catch branch firing) |
| `talked_to_frank_today` | Every exit | Daily-reset flag for state-pump cooldowns |
| `energy -= 3..10` | Every exit | Time/energy cost, scaled by stage |
| `corruption` | Stage 3 exits, small increment | Tease register accrues player corruption |

### What this scene does NOT flip

- `frank_stage` directly. The stage advances when the helper clears (Stage 0→1, Stage 2→3) or when the catch / Crack one-time branches fire elsewhere (Stage 1→2 via the living-room hub branch; Stage 3→4 via the office scene's deepest tier). The kitchen scene is a contributor, not a transition site.
- Any other NPC's flags. Frank's kitchen scene does not touch Ryan, Jake, Diana, Marge, or Cookie state.

### Effective texture count

- 4 stages × ~2 time-bands × occasional tier increment = ~8 effective scene textures.
- Authored prose: ~600 words across all branches.
- Source weight per branch: 50–100 words.
- Compare to Phase 1's `activity_breakfast_frank` (~540 words for one DEFAULT/WITHDRAWN/WARM/CONSEQUENCE variant set, all at Stage-0 register only). **Same source weight, ~5× more effective texture, no Phase-1 variant rotation.**

---

## Effect block patterns by stage

A reusable lookup the author consults when filling in cascade exits.

| Stage | Typical effects | Counters touched | Daily-reset flag | One-time guards |
|---|---|---|---|---|
| 0 | `frank.trust += 1`, energy `-3..-5` | none | `talked_to_frank_today` | none |
| 1 | `frank.trust += 1`, energy `-3..-5`, money +X if bookkeeping | `frank.bookkeeping_count` | `talked_to_frank_today` | none |
| 2 | small money from chores, energy `-5..-10` | `frank.chore_count` (optional) | `talked_to_frank_today` | none |
| 3 | `frank.arousal += 2`, `corruption += 1`, energy `-5..-10` | `frank.tease_count` | `talked_to_frank_today` | the Crack branch (if reached this visit) sets `frank_cracked` |
| 4 | per-keep-route effects | per-keep-route counters | `talked_to_frank_today` | none new (the keep-route choice was already made) |

---

## Voice register inside cascades

Per master spec §10, register is governed externally. This doc respects that. Brief recap of what a cascade author needs to know:

- **Stage 0/1 branches** — TLS-literary, Failbetter density. 80–250 words across the visible branches at this stage. Single fixed paragraph per band; image-rotated; no prose-pool.
- **Stage 2/3 non-explicit branches** — TLS-literary, slightly tighter. The Crack-adjacent register lands one or two register-marker lines per branch.
- **Stage 3 explicit-tier branches** (the tease cascade in the office, not in kitchen) — Hybrid: short stage direction + dialog-heavy. 80–300 words across all reveals. Per-NPC corruption gating per master spec §2.5b. Single register-marker line per scene at corruption-band shifts.
- **State-pump button toasts** (8–20 words) — fire from hub buttons, not from this scene. Out of scope.

The author does not invent register choices per scene. The register comes from §10. The cascade gates *which* register the player sees on this visit.

---

## Authoring checklist for a scene cascade

Before drafting prose for a new scene cascade, the author answers in order:

1. **Which NPC and which surface?** "Frank, kitchen" → scene id is `scene_kitchen_with_frank`. The doctrine forbids scenes spanning multiple NPCs except where the design book explicitly calls for an interaction (a Phase-2+ concern).
2. **What stages does this scene cover?** Refer to `02_NPC_Stage_Chains.md`. Most scenes cover all stages of the NPC; some surfaces only matter from a specific stage onward (e.g., `scene_franks_office_supervised` only covers Stage 2/3).
3. **What time-bands does the NPC reach this surface?** From master spec §4 schedule grid. If only one band, no time-band overlay needed.
4. **Does this scene fire from a router (probability) or a hub button (deterministic)?** Sets `trigger.chance` or omits it.
5. **What counters does this scene increment?** Name them. Confirm `02_NPC_Stage_Chains.md` lists them.
6. **What one-time guards (if any) live as branches inside this scene?** Per the doctrine, guards live as branches, not as separate canvases. Name the guard flags. Confirm the gate is `<flag> == false` so the branch fires once.
7. **Density target.** 80–400 words across all branches. Per master spec §10 for register.
8. **Image search queries.** 3–5 per image block. Per master spec §2.4: image rotation is the verified RtS variety mechanism.
9. **What does the scene flip? What does it NOT flip?** Audit against the "Effect blocks" section above.
10. **Re-entry semantics.** What does the player see on the next visit? If the answer is "the same content," check that this is intentional (e.g., Stage-0 ambient texture). If something must change, name the counter or flag that produces the change.

A cascade that can't answer 1–10 cleanly doesn't ship.

---

## Anti-patterns specific to cascades

Beyond the doctrine's anti-patterns (`01_Repeatable_First_Doctrine.md`), cascades have their own failure modes.

1. **Skipping the stage gate.** A group block that gates on `time_band == M` without an outer stage gate. Forbidden — every scene branch lives inside a stage. If Stage 0 and Stage 1 share the same morning prose, write that prose twice or wrap it in a parent group that explicitly gates `frank_stage in [0, 1]`.

2. **Tier overlay outside an explicit-tier scene.** Per-act counters belong to the explicit-tier scenes (Stage 3 office tease, diner T1/T2/T3, Ryan close tiers). Don't sprinkle counter-gated reveals into early-stage scenes — it produces complexity without payoff.

3. **The "all-stage prose" branch.** A branch with no stage gate that fires every visit. The author wrote one paragraph for "every Frank kitchen visit." If the prose really is stage-invariant, it goes in the image block's description or in a state-pump toast. Scene branches without a stage gate are doctrine violations.

4. **Per-visit randomization of prose.** Per master spec §2.4: the verified RtS variety mechanism is image rotation. Prose-pool rotation is not in the doctrine. If a scene needs more variety, the answer is more stage branches or more time-band branches, not prose-pool variants.

5. **Cross-NPC contamination.** A Frank kitchen scene that flips a Ryan flag because "they were both at dinner that day." Forbidden. Cross-NPC interactions are explicit design-book moments and live in their own one-shot canvases — and even then, the canvas reads multiple stage flags but writes only the one whose surface it is.

6. **Cascade depth > 3 axes.** Stage + time-band + tier is the maximum. A fourth axis (corruption-band, weather, weekday) gets refused. If it's truly needed, lift one axis up — e.g., weekday becomes a sibling scene canvas with its own schedule-gated trigger.

---

## Cross-references

- **`01_Repeatable_First_Doctrine.md`** — vocabulary lock; doctrine checklist for new canvases.
- **`02_NPC_Stage_Chains.md`** — Frank's stage table consumed by the cascade above; counters and one-time guards named.
- **`05_Hub_and_Location_Specs.md`** (deferred) — specifies how hub buttons enter this scene (the kitchen hub's "Talk with Frank" button, conditional on schedule + cooldown).
- **`06_One_Shot_Inventory.md`** (deferred) — confirms the catch and the Crack are branches inside scenes, not separate canvases.
- **`archive_02_TLS_Rewrite_Spec_2026-04-29.md` §2.5** — original cascade pattern description; this doc locks the single-node multi-group choice.
- **`archive_02_TLS_Rewrite_Spec_2026-04-29.md` §2.5b** — explicit-tier additions (per-NPC corruption, per-act counters, image rotation, speech-dominant prose).
- **`archive_02_TLS_Rewrite_Spec_2026-04-29.md` §10** — voice register table; cascades pick *which* register fires, the table specifies *what* the register is.
- **`03_Engine_Changes_PRD.md` §0** — confirms `trigger.chance` is shipped (verified at v1.py:3216, 3585).

---

## What this doc is not

It is not a full inventory of TLS scene canvases. (That's a Phase-2 build artifact, not a spec.) It is not the authoritative TOML schema — field names are illustrative. It is not the Frank arc spec. (That's `02_NPC_Stage_Chains.md`.) It is not the voice register. (That's master spec §10.)

It is the canonical scene shape, locked precedence, and one worked example end to end. Every scene canvas authored in Phase 2 follows this shape.
