# 23 — Location Menu + Sex-Loop Hybrid (Phase 3 design capture)

> **Status:** Forward-looking design capture. **Authored 2026-05-07, 16:21 IST.**
> **Phase:** Phase 3. NOT for Phase 2 execution. Phase 2 stays in shipping/polish mode (Frank Stage 3+ shipped per doc 19, NEW badge truth-matching shipped 2026-05-07, cascade exit routing shipped 2026-05-07). This doc captures the next major design direction so the thinking from the 2026-05-07 live-play + design session is not lost — without it, the next contributor starting Phase 3 would have to re-do the live-play and the synthesis from scratch.
> **Triggered by:** A 2026-05-07 live-play session of RTS (`game_explorations/rts-arousal-sex-trace/`) and Shady Deals (`game_explorations/shady-deals-loop-trace/`) and an extended design conversation about how to give the player **menu agency at locations** + **replayable sex scenes** without losing TLS's state-aware prose strength or its first-time cascade story moments.
> **Outcome (if Phase 3 adopts this):** Three-layer hybrid — scene-setter / location menu / sex-loop hub — that combines TLS strength (dynamic state-aware prose) + RTS strength (per-location player-driven menu) + Shady Deals strength (replayable per-scene loop) without copying any one in full. Maya keeps full control inside sex scenes (no NPC override, no dom dice — explicit deviation from Shady Deals).

---

## §1 Why this design exists

### Three problems in TLS today

| # | Problem | Player-facing symptom |
|---|---|---|
| 1 | **No location-level player agency.** | Maya walks into Frank's bedroom → engine auto-routes ONE canvas → player has no menu choice over what to do that night. Whatever scene fires, that's tonight. |
| 2 | **No scene-level replay value.** | Once a sex cascade is played, every future visit shows the same beats in the same order. After 5 plays the prose is memorized, the click sequence is mechanical. |
| 3 | **Cascade-only doctrine forces all-or-nothing pacing.** | "Have sex with Frank" is one fixed 13-beat sequence. Player can't do JUST a BJ tonight, or just kiss and leave, or edge-and-stop without us authoring a separate canvas for each variation. |

### Three corresponding strengths to preserve

| # | Strength | Where it lives today |
|---|---|---|
| 1 | **State-aware prose.** | Canvases that change based on dozens of state vars — TLS's existing strength via `[group]` blocks + priority-based canvas selection. |
| 2 | **First-time scenes as authored stories.** | Maya's first sex with Frank IS a moment — needs to land as written, not be randomized into a menu. Doc 19 §4 capstone, `scene_office_after_crack` first-sex prose, `scene_franks_bedroom_evening` first-night cascade. |
| 3 | **Type C narrative choices.** | "Stay through" / "Back to my room before Diana wakes" — the post-scene character-defining choices that aren't sex actions. Doc 19 §5 establishes these as register-not-route exits with stat distinguishers (`Frank.trust +1` vs `Maya.calculation +1`). |

The hybrid in §2 reconciles both lists.

---

## §2 The three layers (the model)

```
[Maya enters loc_franks_bedroom at Tuesday evening, Stage 4 repeat]

  ▼  Layer 1 — Scene-setter canvas (auto-routed by current TLS priority/conditions)
     "Frank in bed, paperback on his chest, lamp on. He looks up.
      Frank: 'Hey.'"
     (no exit choices — falls through to Layer 2)

  ▼  Layer 2 — Location activity menu (player picks)
     💬 Sit on the edge and talk        [always, daily cap → relation +1]
     🛏️ Get into bed with him           [Stage 4 → opens Layer 3]
     ❤️‍🔥 Tease him from across the room  [Maya corr ≥ 30 → opens Layer 3 with arousal bonus]
     🚪 Just say goodnight              [exit, no commitment]

  ▼  [Maya picks 🛏️ Get into bed with him]

     ┌──────────────────────────────────────────┐
     │ FIRST TIME EVER → cascade (story scene)  │
     │ REPEAT TIMES   → Layer 3 sex-loop hub    │
     └──────────────────────────────────────────┘

  ▼  Layer 3 — Sex-loop hub (Shady Deals model, Maya-controlled)
     [stage menu refills after each action; twin pleasure meters race;
      climax fires when npc_pleasure ≥ 50]

  ▼  [climax → Sex Main Finisher → cumshot type by stage at climax]

  ▼  Type C narrative exit choices (UNCHANGED FROM TODAY)
     "Stay through. Sleep here."           [Frank.trust +1, diana_awareness +1]
     "Back to my room before Diana wakes."  [Maya.calculation +1]
```

### Concrete example — Frank's bedroom Stage 4 evening

**Same location, two different nights, two different setters:**

#### Night A — Tuesday 21:30, Frank calm

State: `frank_bedroom_first_done is_true`, `frank.arousal < 4`, `weekday`, no recent fights, Diana asleep two rooms over.

The engine picks the calm-evening setter (highest-priority valid scene-setter for current state):

```
[Setter: setter_franks_bedroom_calm_evening]

Frank's bedroom. The lamp is on the nightstand. Frank's in bed,
cover turned back on her side. He's reading something — looks like
the kind of paperback he never finishes, page open on his chest.

He looks up when she comes in.

  Frank: "Hey."

──────────────────────────────────────

[Activity menu — Layer 2]

  💬 Sit on the edge and talk
  🛏️ Get into bed with him
  ❤️‍🔥 Undress slowly while he watches    [Maya corr ≥ 30]
  🚪 Just say goodnight
```

#### Night B — Friday 22:00, Frank wound up

State: `frank.arousal >= 7`, `weekend`, Diana visiting her sister (`diana_present is_false`), Maya hasn't visited in 2 days (`talked_to_frank_today is_false` for 2 dayCount cycles).

The engine picks a different setter (higher-priority match for the wound-up state):

```
[Setter: setter_franks_bedroom_wound_up]

Frank's bedroom. Door already cracked when she comes down the
hallway. Lamp on. He's not in bed yet — standing by the window
with a glass in his hand. He turns when she pushes the door open.

  Frank: "Took your time."

──────────────────────────────────────

[Activity menu — same shape, different weight]

  💬 Pour yourself one too
  🛏️ Cross to him
  ❤️‍🔥 Stay in the doorway. Let him come to you   [Maya corr ≥ 30]
  🚪 Tell him you're tired tonight                [Frank.arousal -2 — frustration]
```

Same menu items (mostly). Same activity routes underneath. **The setter changes the meaning of every option** — "Cross to him" against the calm-Frank setter feels different than against the wound-up-Frank setter, even if the sex-loop hub it opens is the same.

This is the multiplicative content model: `N setters × M menu items × K loop variations` gives many-played-out scenes from comparatively little authoring.

---

## §3 Cascade vs Loop — the decision rubric

A first time is a story. A 50th time is a habit.

Stories need to be told a specific way; habits need to be lived. So:

| Scene moment | Pattern | Why |
|---|---|---|
| First BJ ever between Maya and Frank | Cascade | The line crossed is a story. Author the prose. Lock the order. |
| First sex with Frank ever | Cascade | Same — `scene_office_after_crack` first-sex / `scene_franks_bedroom_evening` first-night cascades stay verbatim. |
| 7th BJ | Loop | Line is crossed. Maya is choosing what tonight looks like. |
| 23rd time Frank fucks her | Loop | Habit, not story. Player wants to play. |
| Stage transition moments (e.g., Stage 3→4 capstone) | Cascade | Doc 19 §4 capstone moments are stories. Loops are unsuited. |
| Daily-texture sex (Stage 4 repeating bedroom) | Loop | Doc 19 §5 surface roster: "Stage 4 daily texture loops with internal cascade variety" — the loop IS the variety. |

**Concrete for Frank's existing canvases:**

| Canvas | First-time pattern | Repeat pattern |
|---|---|---|
| `scene_office_after_crack` first sex (current cascade in source) | **Stays as cascade.** First-sex prose at Stage 3 is the story moment. | After `frank_office_first_sex_done is_true` → menu item routes to office sex-loop hub. |
| `scene_franks_bedroom_evening` first night (current Pattern D cascade per doc 19) | **Stays as cascade.** Existing prose preserved verbatim. | After `frank_bedroom_first_done is_true` → bedroom menu routes "Get into bed" to bedroom sex-loop hub. |
| `scene_kitchen_with_frank_morning` Stage 0/1/2 | **Stays as cascade.** Texture scenes; not sex. | Same — texture cascades don't get loop treatment. |

The decision rubric is: **does this scene cross a line (cascade) or extend a habit (loop)?**

---

## §4 The location menu — design pattern from RTS + Shady Deals

### What RTS does (live-pulled from `game_explorations/rts-arousal-sex-trace/passage_catalog.json`)

| Location | Menu items |
|---|---|
| **BrotherBedroom** | Talk with him 🗣️ / Tease him ❤️‍🔥 / Flash to him ❤️‍🔥 / Have sex with him 🔥 (corr ≥ 3, arousal > 0) / Sleep with him 💤 (LN + relation ≥ 10) / Hallway 🚪 |
| **GrandpaBedroom** | Talk with Grandpa 💬 / Seduce Grandpa 🔥 (corr ≥ 4, arousal > 0) / Hallway 🚪 |
| **MarcusBedroom** | Have sex with Marcus 🔥 (boyfriend, arousal > 0) / Talk with Marcus 💬 (daily cap) / Study with Marcus 📖 / Hallway 🚪 |
| **Kitchen** (no NPC) | Eat 🍽️ / Wash Dishes 🫧 / Order Pizza 🍕 / Hallway 🚪 + auto-fire Grandpa-kitchen-sex if random(1,3)=1 + corr ≥ 4 + Grandpa here |
| **Bathroom** (no NPC) | Shower 🚿 / Mirror 🪞 / Take pill 💊 (inv-gated) / Pregnancy Test 🤰 (inv-gated) / Hallway 🚪 |
| **DadBedroom** | (no manual menu — random Peek-Prostitute event only) / Hallway 🚪 |

### What Shady Deals does (live-pulled from `game_explorations/shady-deals-loop-trace/passage_catalog.json`)

The `NPC Talking` widget is the per-NPC menu:

```
[Yapping line — random by NPC trait: Thug/Thief/Traveler/Nothing]
You and NAME spent some time together…

🔥 Sex initiation       [depravity ≥ 15 AND (not married-loyal) OR friendship ≥ 40]
💍 Side-chick offer     [married + depravity ≥ 20 + charm > NPC.charm + 4]
🔗 Dungeon invite       [depravity ≥ 24 AND dom ≥ 48 AND time 8-20 AND cooldown]
🎁 Give a gift          [always]
🕷️ Blackmail            [if dirt held]
🥊 Pick a fight         [always — leads to combat]
```

### Universal pattern across RTS + Shady Deals

| Element | Always include | Variable |
|---|---|---|
| **State preamble** (top) | Yes — short prose explaining current state | "It's late at night, Brother is sleeping." (RTS) / "Yapping line by NPC trait" (Shady Deals) |
| **Talk-tier item** | Yes — relation-builder, daily cap | "Talk with Brother" (RTS) / base-talk in Shady Deals |
| **Activity-tier items** | Yes — non-sex things to do | Bookkeeping with Frank, Study with Marcus, Wash Dishes |
| **Sex-tier item(s)** | Conditional on stage/stats | "Have sex with him" — locked sibling pattern when ungated |
| **Special/quest items** | Conditional on quest state | Side-chick offer, BDSM dungeon invite, quest hooks |
| **Exit** | Always at the bottom | "Hallway 🚪" (RTS) / no explicit exit in Shady Deals' v2 — TLS will keep the exit |

### Recommended TLS menu shape (synthesis)

```
[Scene-setter prose — Layer 1]

[💬 Talk-tier]  Always shown. Daily cap. Relation +1.
[🛠️ Activity-tier items]  Per-NPC, per-location. Bookkeeping, Study, Walk, etc.
[❤️‍🔥 Sex-tier item(s)]  Stage + corruption gated. Locked sibling when ungated.
                          Routes to cascade (first time) OR loop (repeat).
[🎯 Quest items]  Conditional on active quest state.
[🚪 Exit]  Always at the bottom. "Goodnight" / "Take the receipts and go" / etc.
```

Locked items use the existing `show_when_locked = true + locked_text + locked_text_threshold` pattern (currently used on cascade beats — see `scene_franks_bedroom_evening` Beat 3 "Cross to him" vs locked sibling "Hesitate at the door."). **Same engine primitive, applied to menu items instead of cascade beats.**

---

## §5 The sex-loop hub — design from Shady Deals (Maya-controlled mod)

### Shady Deals' 4-passage skeleton

```
Sex Main Idle (hub)        — renders idle video + idle desc + stage menu
        │
        ▼ player picks an action
Sex Main Loop (turn proc)  — runs prose + video, mutates pleasure meters,
        │                    rolls dom-vs-pose-change, routes
        ├──→ Sex NPC Reaction (override, kink pushback) → ... → hub  ← DROPPED for TLS
        ├──→ npc-driven pose change (forced stage transition)        ← DROPPED for TLS
        └──→ back to Sex Main Idle hub
        │
        ▼ when npc_pleasure >= 50
Sex Main Finisher (climax) — cumshot scene by stage at climax
                             post-scene tuning options
```

### TLS adaptation — Maya keeps full control

**Drop the NPC override entirely.** Per user direction, Maya picks every action, every transition, every stage switch. Frank reacts, Frank moans, Frank says things — but Frank never grabs the wheel.

| Shady Deals primitive | TLS adoption |
|---|---|
| Sex Main Idle hub | **Adopt.** Stage-aware menu refill after each action. |
| Sex Main Loop (turn processor) | **Adopt with mod.** Run prose/video/pleasure mutation. NO dom-roll. NO `_pose_chance` roll. Always returns to hub. |
| Sex NPC Reaction passage | **Drop entirely.** No NPC override, no kink pushback. |
| npc-driven pose change | **Drop entirely.** Stage transitions are player-picked menu items only (e.g., "Get into doggystyle"). |
| Sex Main Finisher | **Adopt.** Cumshot type determined by `$sex_stage` at the moment `npc_pleasure >= 50`. |
| Post-scene tuning options ("Be more rough" → dom +2) | **Drop or rework.** Frank doesn't have a `dom` stat that influences future scenes; Type C exits already cover post-scene character shaping. Keep the post-scene exit pattern but reuse Type C narrative-choice mechanics, not Shady Deals' tuning dial. |
| `_dom_roll`-driven prose tier (NPC dom <15/15-34/35+) | **Replace with Maya-corruption-driven prose tier.** The 3-tier prose system stays, but it's keyed on Maya's corruption (player tier) crossed with Frank's arousal (per-scene state), not NPC dom. |
| Twin pleasure meters scoped to scene | **Adopt.** `loop.player_pleasure` and `loop.npc_pleasure`, both 0-50, both reset on Sex Main Finisher entry. |
| Per-action random ranges (pleasure mutations) | **Adopt.** Author per-action ranges per the math budget in §6. |
| Mid-scene exit penalty (`-20 friendship`, v1 only — v2 removed) | **Adopt v1's flavor, drop the penalty.** TLS lets Maya leave anytime via a "Stop" menu item with no friendship cost. We're not Shady Deals; commitment-lock is wrong for our slower-burn audience. |

### Live-observed Shady Deals loop behavior (for design grounding)

From `game_explorations/shady-deals-loop-trace/notes.md` (2026-05-07 live play):

- 11 menu picks observed Jett scene start-to-finish, foreplay → BJ → ontop → climax
- Per-action pleasure mutations live-observed: Make out (npc 3-5, p 2-5), Tease (npc 3-5, p 2-5), Service (npc +6, p +3, advances stage), Deepthroat (npc 6-10, p 1-3 — biggest single jump observed: npc 17→47 in one click)
- Stage advancement live-observed at "Service him" click → `sex_stage: foreplay → blowjob`
- Climax live-observed: `npc_pleasure: 47 → 50` on a single Ride beat → "Jett is really close to orgasm!" → Sex Main Finisher with `inside=true` cumshot (vaginal — because in `ontop` stage at threshold)

The mechanic works in live play. The structural skeleton is sound. TLS's job is to inherit the skeleton and replace the dom/override layer with Maya-control.

---

## §6 Math budget (concrete numbers, all tunable)

All numbers are first-pass guesses. Pilot will tune them.

### Layer 1 — Long-term integer stats (TLS-like, RTS-like, KEEP)

We mostly already have this. Player corruption + per-NPC arousal/corruption/relation/trust. All integer ladders, hand-picked tier breakpoints.

| Stat | Range | Tier breakpoints | Status |
|---|---|---|---|
| `player.corruption` | 0–50 | [0, 10, 25, 40, 50] = `prim / curious / wanting / committed / lost` | **Already exists.** |
| `npc_<X>_arousal` | 0–10 | RTS-style 5 levels (Calm / Warm / Aroused / Hot / 🔥) | **Already exists per NPC.** |
| `npc_<X>_corruption` | 0–50 | Hand-picked per arc | **Already exists per NPC.** |
| `npc_<X>_relation` | 0–50 | Hand-picked per arc | **Already exists per NPC.** |
| `npc_frank_trust` | 0–10 | Frank-special — set by "Stay through" exit | **Already exists, doc 19 §5.** |

Per-scene mutations (on sex-loop climax via Sex Main Finisher):
- `+1` Maya corruption
- `+1` NPC relation
- `+1` NPC corruption (family-NPC special, RTS pattern)
- `+1` NPC trust if "Stay through" Type C exit
- Reset NPC arousal to 0
- Statistics: `vaginal++` / `blowjobs++` / `creampies++` based on stage at climax + `inside` flag (RTS auto-tracking pattern)

### Layer 2 — Sex-loop scoped pleasure (NEW — only exists during a sex loop)

| Stat | Range | Notes |
|---|---|---|
| `loop_player_pleasure` | 0–50 | Resets at scene end (Sex Main Finisher entry). |
| `loop_npc_pleasure` | 0–50 | Climax fires at 50. Resets at scene end. |
| `loop_npc_max_pleasure` | constant 50 | Threshold (Shady Deals uses 50; we adopt verbatim for parity). |
| `loop_warning_threshold` | derived = 50 - 15 = 35 | At 70% of max, prose adds "Frank is close." |

**Per-action mutations are RANDOM RANGES** (Shady Deals model). First-pass ranges per action archetype:

| Action archetype | NPC pleasure delta | Player pleasure delta | Notes |
|---|---|---|---|
| Light foreplay (kiss, tease, brush against) | random(2, 4) | random(2, 4) | Symmetric — building heat |
| Heavy foreplay (grope, hand on waist, lift skirt) | random(3, 5) | random(2, 4) | Frank-asymmetric |
| BJ general (suck, lick, take in mouth) | random(4, 6) | random(1, 3) | NPC-favored |
| Deepthroat-equivalent (deeper, faster, throat) | random(6, 10) | random(1, 3) | NPC power-move |
| Player riding NPC (cowgirl, ride, grind) | random(3, 5) | random(8, 12) | Player power-move |
| Penetration (mid-position) | random(4, 6) | random(4, 6) | Symmetric |
| "Make him cum" finisher | sets `npc_pleasure = 50` | random(0, 5) | Player-elected climax |

Pacing math:
- Average per-action npc_pleasure delta = ~5
- `npc_max_pleasure / avg_delta = 50/5 = 10` actions to climax
- With finisher elections, can be as fast as **1 click** (player picks "Make him cum" early)
- Without finishers, scene runs ~10-14 menu picks

### Layer 3 — Locked-sibling thresholds (already in engine, EXTEND to menu items)

Pattern already exists in TLS engine — used today on cascade beats. Reuse on menu items:

```toml
[[location_menu.items]]
text = "Cross to him."
target_canvas = "scene_franks_bedroom_first_time" (first time) | "loop_franks_bedroom_sex" (repeat)
conditions = { ... player corruption ≥ 25 ... }
show_when_locked = true
locked_text = "Hesitate at the door."
locked_text_threshold = "I'd need to be more comfortable — at least 25 corruption — before I could cross the room without thinking."
```

Same primitive as `scene_franks_bedroom_evening` Beat 3 today. Just applied to menu items instead of cascade beats.

### Pacing budget — what this gives us

If we adopt these numbers:

- **Maya's first sex with Frank** at corruption 25 (Wanting tier) — 25 corruption-bumping events to unlock. ~5-10 in-game days at 3-5 events/day.
- **One sex scene loop** = 10-14 menu picks at avg ~5 npc_pleasure = `npc_pleasure 0 → 50` in 10-14 clicks. Player can shortcut with "Make him cum" finisher.
- **Each completed sex scene** = +1 Maya corruption, +1 Frank relation, +1 Frank corruption, +1 Frank trust (if "Stay through" picked).
- **Stage 4 unlock from Stage 3 start** (Frank.corr ~19 → 25) = 6 successful sex scenes × 1 per day = **6 in-game days** to unlock the bedroom.
- **Full TLS playthrough** = 2-3 in-game weeks. Same order of magnitude as RTS.

---

## §7 TOML schema sketch (paper-only, does NOT compile)

This is illustrative — it shows what a Phase 3 TOML author would write, NOT a compileable schema. The actual schema requires generator work in `apps/game_generation/twee_comprehensive/generators/v1.py`.

### A scene-setter canvas (Layer 1)

```toml
[[canvases]]
id          = "setter_franks_bedroom_calm_evening"
name        = "Frank's bedroom — calm setter"
description = "Layer 1 setter for Frank's bedroom at evening, calm Frank state. No exit choices — falls through to location menu."

[canvases.trigger]
location      = "loc_franks_bedroom"
is_setter     = true                       # NEW field — marks as Layer 1, no exit choices
is_repeatable = true
priority      = 9
is_active     = true
npc           = "npc_frank"
conditions = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "player", trait_key = "npc_frank_stage",            operator = "gte",      value = 4 },
  { type = "flag",  subject = "player", flag_key  = "frank_invited_to_bedroom",   operator = "is_true"  },
  { type = "trait", subject = "npc",    npc_id    = "npc_frank", trait_key = "arousal", operator = "lt", value = 4 },
] }

[[canvases.nodes]]
id   = "base"
name = "Frank's bedroom — calm"
blocks = [
  { type = "image", props = { file = "setters/franks_bedroom_calm.jpg" } },
  { type = "paragraph", content = "Frank's bedroom. The lamp is on the nightstand. Frank's in bed, cover turned back on her side. He's reading something — looks like the kind of paperback he never finishes, page open on his chest." },
  { type = "paragraph", content = "He looks up when she comes in." },
  { type = "dialog", props = { speaker = "npc", npcId = "npc_frank" }, content = "Hey." },
]
# NO exit_block — setters fall through to location menu
```

### A location activity menu (Layer 2)

```toml
[[location_menus]]
location = "loc_franks_bedroom"
# Renders below the highest-priority active setter at this location.

[[location_menus.items]]
id        = "talk_to_frank_bedroom"
text      = "Sit on the edge and talk."
emoji     = "💬"
target    = "activity_talk_to_frank_bedroom"
conditions = { version = "1.0", logic = "AND", items = [
  { type = "flag", subject = "player", flag_key = "talked_to_frank_today", operator = "is_false" },
] }
locked_text = "Frank's already heard enough from me today."

[[location_menus.items]]
id        = "get_into_bed_with_frank"
text      = "Get into bed with him."
emoji     = "🛏️"
# Routes to FIRST-TIME cascade OR LOOP based on flag
target    = { type = "branched", first_time_target = "scene_franks_bedroom_first_time", repeat_target = "loop_franks_bedroom_sex", flag_key = "frank_bedroom_first_done" }

[[location_menus.items]]
id        = "tease_frank_in_doorway"
text      = "Stay in the doorway. Let him come to you."
emoji     = "❤️‍🔥"
target    = "loop_franks_bedroom_sex"
target_args = { initial_arousal_bonus = 3 }     # frank starts loop with arousal +3
conditions = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 30 },
] }
show_when_locked       = true
locked_text            = "Look at him a moment, then look away."
locked_text_threshold  = "I'd need to be more comfortable with this — at least 30 corruption — before I could pull that off."

[[location_menus.items]]
id        = "say_goodnight_to_frank"
text      = "Just say goodnight."
emoji     = "🚪"
target    = { type = "exit", to_location = "loc_hallway" }
# No effects — clean exit
```

### A sex-loop hub (Layer 3)

```toml
[[loops]]
id          = "loop_franks_bedroom_sex"
name        = "Frank — bedroom sex loop"
location    = "loc_franks_bedroom"
npc         = "npc_frank"
finisher    = "loop_franks_bedroom_finisher"

# Twin pleasure config
loop_state.player_pleasure_max = 50
loop_state.npc_pleasure_max    = 50      # climax threshold

# Per-stage menu — actions available when $sex_stage matches
[[loops.stages]]
id    = "foreplay"
idle_desc = "She's standing at the side of the bed. Frank's eyes on her."

[[loops.stages.actions]]
text = "Kiss him."
prose = [
  # Tier 1: Maya corruption < 15
  { player_tier = "low",  npc_tier = "calm",    p = "She bends down and kisses him, hesitant.", npc = "He kisses back. Brief." },
  # Tier 2: Maya corruption 15-34
  { player_tier = "mid",  npc_tier = "calm",    p = "She leans in and kisses him, slower than the first time.", npc = "His hand finds the back of her neck." },
  # ...etc
]
delta_npc    = { min = 2, max = 4 }
delta_player = { min = 2, max = 4 }
video        = "sex/frank/foreplay/kiss"

[[loops.stages.actions]]
text = "Tease him."
delta_npc    = { min = 3, max = 5 }
delta_player = { min = 2, max = 4 }
# ... etc

# Stage advancement actions
[[loops.stages.actions]]
text = "Drop to your knees."
advances_stage_to = "blowjob"
delta_npc    = { min = 4, max = 6 }
delta_player = { min = 1, max = 3 }
# ... etc

# Finisher action (player-elected climax)
[[loops.stages.actions]]
text = "Make him cum on you."
sets_npc_pleasure = 50    # forces climax
finisher_type     = "facial"
delta_player      = { min = 0, max = 5 }
```

### A sex-loop finisher (climax canvas)

```toml
[[canvases]]
id          = "loop_franks_bedroom_finisher"
name        = "Frank bedroom — climax"
# Internal — only entered from loop, never directly

[[canvases.nodes]]
id   = "base"
blocks = [
  # Switch on $finisher_type set by the loop
  { type = "switch", props = { var = "finisher_type", cases = [
      { value = "facial",     blocks = [ { type = "paragraph", content = "..." }, ... ] },
      { value = "vaginal",    blocks = [ { type = "paragraph", content = "..." }, ... ] },
      { value = "creampie",   blocks = [ { type = "paragraph", content = "..." }, ... ] },
  ] } },
  # Effects on entry — the FinishSex bundle
  # ...
]

[canvases.nodes.exit_block]
type = "choices"

# Type C narrative exits — UNCHANGED from doc 19 §5
[[canvases.nodes.exit_block.choices]]
text = "Stay through. Sleep here."
# ...

[[canvases.nodes.exit_block.choices]]
text = "Back to my room before Diana wakes."
# ...
```

---

## §8 Engine work needed (ranked by cost)

| # | Item | Cost | Notes |
|---|---|---|---|
| 1 | Scene-setter canvas type (`is_setter = true` flag) | **LOW** | Mostly markup. New trigger flag. Renderer skips exit block. Falls through to next renderer (Layer 2). |
| 2 | Location-menu hub passage | **LOW-MEDIUM** | New TOML primitive (`[[location_menus]]`). Renderer iterates items, applies gates, emits buttons with route-on-click. Reuses existing `show_when_locked` + `locked_text` logic. |
| 3 | Branched menu target (first-time vs repeat) | **LOW** | One flag check at click-time; routes to one of two passages. |
| 4 | Sex-loop hub state machine | **MEDIUM** | Twin pleasure meters in `$state`. Stage-aware menu dispatch (which actions show by `$sex_stage`). Per-action prose tier dispatch (Maya corruption × Frank arousal tier matrix). Per-action video routing. |
| 5 | Per-action pleasure mutation widget | **LOW** | One macro: `<<loop_action delta_npc='random(N,M)' delta_player='random(K,L)'>>`. Reads from action def. |
| 6 | Climax detection + finisher routing | **LOW** | Switch on `$loop_npc_pleasure >= max`. Routes to finisher canvas with `$finisher_type` set by stage-at-climax. |
| 7 | Per-action prose tier system (3×3) | **MEDIUM-HIGH** | Pilot uses 2×2 (Maya corruption low/high × Frank arousal calm/heated) to keep authoring cost manageable. Tier-up to 3×3 later. |
| 8 | Setter falls through to menu (rendering pipeline) | **LOW** | Generator emits setter prose then menu hub render in same passage. Single-pass. |
| 9 | Menu item routes to setter-aware canvas (e.g., setter sets `loop_initial_arousal`) | **LOW** | Setter canvas can write a per-loop arg via `target_args` on click. |
| 10 | Tests + verification fixtures | **LOW-MEDIUM** | Unit tests for menu rendering, gate evaluation, loop state transitions. Integration test: one full pilot canvas play-through. |

**Total estimate: 1-2 sprints** of engine work for the pilot. Wider rollout (multiple NPCs, multiple loops) is N × per-NPC authoring + zero additional engine work.

---

## §9 Pilot scope (one Frank canvas)

**Pick `scene_franks_bedroom_evening` (Stage 4 repeat) as the pilot canvas.**

### Why this canvas

- **Freshest Frank canvas** — design done 2026-05-04 per doc 19 §5; prose is settled. Won't disturb anything in flight.
- **Naturally repeated** — exactly the case where the loop adds the most value (vs a one-shot reveal scene).
- **First-time version stays as cascade** (`frank_bedroom_first` group already in TOML). The loop only kicks in when `frank_bedroom_first_done is_true`.
- **Frank's bedroom is narrow scope** — small menu (4-5 items), one NPC, one location.
- **Existing Type C exits** (`Stay through` / `Back to my room before Diana wakes`) are already authored — don't need to invent post-scene exits for the pilot.

### Pilot deliverables

| Artifact | Description | First-pass size |
|---|---|---|
| `setter_franks_bedroom_calm_evening` | Layer 1 — calm-Frank scene-setter (3-4 paragraphs) | ~80 words |
| `setter_franks_bedroom_wound_up` | Layer 1 — wound-up-Frank scene-setter (alternative state) | ~80 words |
| `loc_franks_bedroom_menu` | Layer 2 — 4-item activity menu (Talk / Get into bed / Tease in doorway / Goodnight) | TOML def |
| `scene_franks_bedroom_first_time` | First-time cascade (if not already covered by existing Pattern D first-night group) | Reuse existing; small cleanup |
| `loop_franks_bedroom_sex` | Layer 3 — sex-loop hub | ~10 actions × 3 stages |
| `loop_franks_bedroom_finisher` | Climax canvas (3 cumshot variants by stage at climax) | ~120 words × 3 |
| Per-action prose snippets | 2 player tiers × 2 NPC arousal tiers × 10 actions | ~40 short snippets, ~10-30 words each |

### Time estimate

- Engine work: **2-4 dev days** (per §8, items 1-9 partial)
- Authoring prose: **4-8 hours** (40 snippets + 3 cumshot variants + 2 setters + 1 menu)
- Live-play validation: **30-60 minutes** play session

**Total: half a sprint** for pilot.

### Decision gate (before broader rollout)

After pilot ships, run a 30-60 minute live-play session that answers all questions in §11. **Do NOT extend to other NPCs / locations / canvases until pilot validates.** If pilot reveals the loop feels grindy, or the menu cluttered, or Frank passive — revise the design before rolling out.

---

## §10 What this doc does NOT change

Explicit list of Phase 2 work that stays unchanged:

| Phase 2 work | Status | Why unchanged |
|---|---|---|
| Frank arc Stages 0-4 (doc 19) | Stays canonical | Doc 19 is the spec; this doc adds a layer ON TOP for Stage 4 repeats. Stage 0/1/2/3 unchanged. |
| Hint system (doc 12 PRD shipped + doc 11 authoring guide) | Stays canonical | Loop hub + menu items will need hint coverage in Phase 3, but the hint system itself is unchanged. |
| NEW badge truth-matching (shipped 2026-05-07) | Stays | Badge logic operates on canvases — setters and loops will register as canvases for the badge. |
| Cascade exit routing fix (shipped 2026-05-07) | Stays | Exit routing applies to cascade-bodied canvases; loop bodies have a different exit shape (climax → finisher) but use the same engine primitives where applicable. |
| Cascade as the canvas pattern for first-time / one-shot scenes | Stays | This is THE doctrine for story moments. Loops are for repeats only. |
| All existing Type C narrative choices | Stay | "Stay through" / "Leave before dawn" / "Take the receipts" / "Sit on the desk a moment" — these run AFTER the sex loop closes, in the finisher canvas's `exit_block`. Unchanged. |
| Doctrine docs 01 / 04 / 13 / 15 / 16 | Stay | Single-digit one-shot ledger, scene cascade pattern, RTS reference, sandbox doctrine, Frank scene library — all preserved. The hybrid is additive. |

---

## §11 Open questions for the pilot to answer

These can only be resolved by live play of the pilot canvas:

1. **Does the menu feel cluttered with 4-5 items at peak?** Or does it read as "here are my options for tonight"? RTS BrotherBedroom has 4-5 items and reads fine in play; TLS may need tighter or richer items.
2. **Do random-range pleasure mutations feel varied or chaotic?** Shady Deals does random ranges and it works — but TLS is a slower-burn audience. Players might want more deterministic feedback.
3. **Does Frank feel like a partner without the dom override mechanic, or does he feel passive?** This is the conscious deviation from Shady Deals. If Frank reads as a dummy who waits for Maya's clicks, we may need to add per-action Frank-driven dialogue interjections without giving him pose-control.
4. **Does the existing Frank prose ("Quiet." every action) hold up cast as a loop?** Doc 19 Frank-voice spec is terse. Loops invite repetition. "Quiet." after every BJ click would break. May need per-action dialogue variety library.
5. **Is twin-meter racing engaging or invisible without on-screen meters?** Shady Deals shows no numeric meters — only narrative cues ("Frank is close to climax"). TLS may want optional meter visualization for players who like the game-y feel.
6. **Does the locked-sibling pattern at menu items teach the player thresholds well?** Doc 19's mid-cascade gate works ("Hesitate at the door."). At the menu level it may read cleaner OR more confusing — depends on how many locked items show simultaneously.
7. **Does the setter-pick-meaningfully-changes-menu-meaning effect actually land?** Same menu items against different setters — does the player FEEL it, or is it invisible?
8. **Does "Stop" at any time feel right?** TLS keeps the player able to leave mid-loop with no friendship penalty (drops Shady Deals' commitment-lock). Player may exploit this to never finish. Or may appreciate it. Live play tells.
9. **Does the cascade-vs-loop boundary read clearly?** First time vs repeat. If the first-time cascade plays the same prose as the loop's first-stage menu, the seam shows. Pilot tests the seam.
10. **Does the finisher canvas's stage-at-climax cumshot variant feel earned?** "I picked Ride him so he cums inside me" — does that read as player intentionality or as engine bookkeeping?

---

## §12 Cross-refs

### Phase 2 docs (cross-link)

- **Doc 19 — `19_Frank_Stage_3_Plus_Design.md`** — Frank arc spec; this doc adds a Layer 3 (loop) on top of Stage 4 repeated visits. Doc 19 stays canonical for Stages 0-4 design; this doc is purely about replay-pattern for visits 2+.
- **Doc 21 — `21_RTS_Brother_Mechanism_Audit.md`** — RTS cascade pattern source (Pattern D, Pattern E referenced throughout doc 19). Cascade pattern stays in use for first-time scenes.
- **Doc 22 — `22_RTS_Cross_NPC_Mechanism_Comparison.md`** — RTS cross-NPC menu pattern source (BrotherBedroom, GrandpaBedroom, MarcusBedroom, etc.). Layer 2 menu design draws from doc 22's audit.
- **Doc 04 — `04_Scene_Cascade_Pattern.md`** — Canonical scene shape (group blocks + conditions). Scene-setters in Layer 1 follow this pattern; the only addition is the `is_setter = true` flag.
- **Doc 13 — `13_Road_to_Success_Reference.md`** — RTS as the reference game; this doc cites RTS catalog at multiple points.

### Live-play sources (game_explorations)

- **`game_explorations/rts-arousal-sex-trace/notes.md`** — RTS sex/arousal live-play findings, 2026-05-07. Covers PeepBrotherSex (5-beat cascade), BrotherBedroomSex1 (13-beat player-led), BrotherShowerSex (BJ-led), arousal model, FinishSex closure widget. Source of truth for RTS sex-scene structure.
- **`game_explorations/shady-deals-loop-trace/notes.md`** — Shady Deals menu-loop live-play findings, 2026-05-07. Covers 11-pick Jett scene, Sex Main Idle hub, twin pleasure mechanics, dom override (which we drop), stage transitions, Sex Main Finisher. Source of truth for Shady Deals loop architecture.

### Methodology memory

- **`feedback_play_dont_extract.md`** — Default to live-play, not catalog grep, for game-research sessions.
- **`feedback_live_play_over_console_paste.md`** — Default to live-play verification, not console-paste-back loops.

These two memory entries are the methodology that produced this doc — the design wouldn't exist without the 2026-05-07 live-play sessions of RTS and Shady Deals.

---

End of doc 23.
