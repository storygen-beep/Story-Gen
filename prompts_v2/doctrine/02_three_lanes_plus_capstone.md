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

**TLS engine support: ❌ NOT YET SUPPORTED.** `setup.checkAndSubstituteCanvas` evaluates each rule's dice independently. Authoring approximation (N rules with chance summing < 1) **diverges from true Pattern B** in two ways:
1. Cumulative probability: true B = Σcᵢ; approximation = 1 − ∏(1 − cᵢ). For 3 NPCs at "1/6 each," true B = 50%; approximation ≈ 42%.
2. Failed-condition fall-through: true B falls to solo; engine `continue`s to next rule.

**No build error fires for the divergence.** Use Pattern A and document the approximation. Future `exclusive_group` field (Doc 67 §5.1) will support Pattern B natively; defer until LO scopes the engine work.

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

**TLS engine support: ⚠️ PARTIAL via `pre_substitution_effects`** (Doc 69 Item 2, 2026-05-27). Effects run BEFORE the substitution check, so they execute even when `<<goto _sub_target>>` preempts. Workaround for slice phase (until full Pattern C ships): duplicate the unconditional effect on every substitution target's effect list. Mechanically equivalent — author duplication is the cost.

### §4.7 — Selection rule (the doctrine call)

| Authoring intent | Pattern |
|---|---|
| "Multiple independent NPCs could walk in on this chore; priority by arc focus" | **A** (default) |
| "Several mutually exclusive variants — one fires per attempt" (often same NPC with sub-variants) | **B** (engine extension required) |
| "Activity has unconditional stat outcome that counts even when interrupted" | **C** (use `pre_substitution_effects`) |

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

This is the approximation noted in §4.6.2. It's not mutual-exclusion-correct. Acceptable in slice phase if Pattern B is rare; document the approximation. The engine extension (`exclusive_group`) is `doctrine/04_authoring_rules.md` §future-engine for when load-bearing.

### §8.7 — Stat cost in wrong placement (Pattern A vs C)

If Exercise costs Energy only in the `exit_block` (Pattern A placement), the workout doesn't "count" when Grandpa walks in — but Pattern C design says it SHOULD. Place unconditional effects in `pre_substitution_effects` (Pattern C).

### §8.8 — Strict location check on Lane 3 walk-in dispatcher

Lane 3 walk-in = "NPC walks in on Maya" = loose `IsNpcAtHome` check. Tightening Lane 3 to "NPC must already be in kitchen" breaks the fictional intent — Frank wandered into the kitchen because Maya was there, he didn't pre-stage himself.

### §8.9 — No `max_triggers_per_day` on Lane 3 substitution target

Same scene firing 5 times in one day breaks the "once per day" cadence RTS uses. Doc 67 R7.

### §8.10 — Substitution target not marked `substitution_only`

Then it appears in the NPC portrait hub at the location, the player can click it directly — defeating the "you were doing X and he happened" fictional intent. Pre-ship check: every Lane 3 substitution target has `substitution_only = true`.

---

## §9 — Engine support summary

| Lane | TLS engine support |
|---|---|
| **Lane 1** — Hub button | ✅ Native via NPC portraits + `exit_block.choices` + per-choice conditions |
| **Lane 2** — Location-entry random | ✅ Native via `trigger_mode = "random"` + `chance` |
| **Lane 3** — Pattern A dispatcher | ✅ Native via `substitutions` + `substitution_only` (`v2.py:4649`) |
| **Lane 3** — Pattern B dispatcher | ❌ Not yet — use Pattern A approximation; defer until LO scopes `exclusive_group` engine work |
| **Lane 3** — Pattern C dispatcher | ⚠️ Partial via `pre_substitution_effects` (Doc 69 Item 2) |
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
- `doctrine/05_rts_flat_prose.md` *(Batch 2+ — pending)* — voice register (RTS-flat default; Tier-3 capstones)
- `doctrine/09_trait_catalog.md` — trait vocabulary used in lane gating

### Schema files

- `schema/01_engine_capabilities.md` §3 (canvas + trigger) + §4 (Lane 3 substitution) + §5 (schedule + NPC presence)
- `schema/02_toml_schema.md` §5–§7 (canvas + trigger + node schema)

### Source docs

- `28th_april_TLS_Phase2_Redesign/24_RTS_Three_Lanes_Repeatable_Activities.md` — Lane mechanism source
- `28th_april_TLS_Phase2_Redesign/57_Capstone_Doctrine.md` — Lane 4 source
- `28th_april_TLS_Phase2_Redesign/67_Solo_Activity_Design_and_Multi_NPC_Dispatcher_Doctrine.md` — solo activity + dispatcher patterns source

### Engine primitives

- `setup.renderNpcPortraits` (`v2.py:4295`) — Lane 1 portraits
- `setup.checkRandomEncounters` (`v2.py:4520`) — Lane 2 dispatcher
- `setup.checkAndSubstituteCanvas` (`v2.py:4649`) — Lane 3 substitution
- `setup.selectAutoFireCanvasForLocation` (`v2.py:3885`) — Lane 4 capstone auto-fire

---

**End of file.** Next: `doctrine/03_arc_shapes.md` for per-arc canvas distribution.
