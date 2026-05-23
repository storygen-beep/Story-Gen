# 16 — Frank Scene Library Design (Phase 1 Pilot)

> **Created 2026-05-03.**
> Phase 1 deliverable for the sandbox pivot (`15_Sandbox_Pivot_Direction.md` §14). Designs the new Frank scene library that Phase 1 will author — 12 total surfaces (4 existing kept/polished + 8 new).
> Reads: 13 (RTS reference for craft patterns), 14 (engine primitives we can use), 15 (direction + locked decisions).
> Will produce: TOML edits to `3_activities.toml`, `4_story_arc.toml`, `5_scenes.toml` per §18 authoring sequence. **No engine code changes in Phase 1.**
>
> **Status: Step A doctrine updates complete, Step B sample scenes authored + engine bug discovered + fixed (see doc 14 §1 update 2026-05-03), Step C in progress.**

---

## §0 Why this doc exists

Doc 15 locked the sandbox direction. Doc 14 specified the engine primitives. This doc applies both to one NPC (Frank) and produces an authoring spec detailed enough that the prose can be written from it without further design conversations.

Frank is the pilot for three reasons:
1. **Densest existing content** of the 3 slice NPCs — has 4 scenes + 2 activities + 4 hints, analogous to RTS Brother (densest at 15 scenes).
2. **Family/proximity NPC** — the right tendency for ambient random-encounter authoring (per RTS family arc shape).
3. **Stage 0–4 cascade already authored** — proves stage system stays as capstone layer; sandbox additions complement rather than replace.

If Frank works after playtest, pattern extends to Diana → Marge → Ryan → Jake. If not, doctrine gets revisited before scaling.

---

## §1 Locked decisions (from §1 of the design conversation)

### D1. RTS-flat doctrine option = **B (carve-out)**

Memory entry `feedback_tls_scene_body_style.md` will be updated:
- **Default:** RTS-flat for all scene bodies (existing rule preserved).
- **Carve-out:** Tier-3 character writing explicitly allowed for:
  1. Named-NPC introductions (first time the player meets an NPC who'll have an arc)
  2. Stage-flag capstone scenes (e.g., the catch, the cracked summons, arc transitions)
  3. Crisis priority hint scenes (e.g., the rent-confrontation moment)

For Frank specifically, this means:
- Tier-3 used in: scene #3 (catch polish), Stage 4 cracked-summons branch of scene #1, scene #11 (LN kitchen raid)
- Tier-1/Tier-2 used in: everything else

### D2. Existing 4 Frank scenes = **Polish (not full rewrite)**

- Stage 0/1/2 paragraphs in scenes #1, #2, #4 stay verbatim
- Catch scene (#3) gets Tier-3 prose polish — surgical, prose-only, doesn't touch flag effects
- Stage 4 "cracked summons" branch in scene #1 gets Tier-3 polish (same surgical rule)

### D3. Stage 3→4 natural content = ~~**Defer**~~ ⚠️ **SUPERSEDED 2026-05-04**

> **⚠️ SUPERSEDED by `19_Frank_Stage_3_Plus_Design.md` §1 / §4 / §5.**
> D3's deferral is lifted. Stage 3→4 is now a single branch-inside-shell capstone (bedroom invitation in `scene_office_after_crack`, gated `frank_office_visits ≥ 3 + Frank.corruption ≥ 25`) and Stage 4 has a real anchor canvas (`scene_franks_bedroom_evening`) + register cascade across kitchen / living room / back porch surfaces. **All shipped in `7_final_game.toml` 2026-05-04.** D1 (Tier-3 carve-out) and D2 (existing scenes = polish-not-rewrite) remain locked.

~~Stage 3→4 helper has 5 unmet conditions that won't be reached in 10-day slice anyway. Stays dev-shortcut only. Phase 1 scope = Stages 0/1/2 + ambient layer.~~

---

## §2 Frank's voice — the consistency reference

**The single most important section for authoring discipline.** Every scene must sound like the same Frank. If voice drifts between scenes, the library reads as 12 different characters.

### Background

Ex-construction worker. Built things with his hands for 30 years before retiring to landlording. Owns this property — inherited or earned, doesn't elaborate. Wife is gone (dead? left? Frank doesn't say, Maya hasn't asked). Lives alone, set in his ways, watches TV with the volume up.

Sees Maya as a complication he didn't want — a tenant his late wife or some obligation forced him to take. Suspicious of her motives initially. Slow to soften.

### Speech patterns

**Sentence shape:**
- Short. 4-8 words common.
- Often ends with the verb chopped: "Coffee's ready." "Door's stuck again."
- Rarely a complete grammatical sentence. Implies the rest.

**What he does:**
- Names things instead of feelings: "fan's broken," not "I'm frustrated"
- States facts when others would express opinions: "rent's due Sunday" not "I expect you to pay rent on time"
- Asks questions that aren't really questions: "you eat?" (you should eat), "you cold?" (offer of blanket without offering)

**What he doesn't do:**
- Rarely uses Maya's name. Uses "you" or "girl" (with edge) or just talks at her without address.
- No exclamations. Even surprised, he understates.
- No long explanations. If he has to explain something twice, he stops talking.
- Doesn't apologize. Adjusts behavior wordlessly when he's wrong.

### Voice samples per stage

| Stage | Frank line | Notes |
|---|---|---|
| 0 (Suspicious) | "You eat?" | Not concerned — checking if the kitchen needs cleaning |
| 0 (Suspicious) | "Bookkeeping's tomorrow. Office. Seven." | Statement, not invitation |
| 1 (Grudging warmth) | "Coffee's still warm." | Brief, unprompted offer. The warmth is in the offering, not the words. |
| 1 (Grudging warmth) | "You did good with the books last week." | Acknowledgment without praise |
| 2 (Restrict, post-catch) | "I told you. Door open. Always." | Clipped, controlling |
| 2 (Restrict, post-catch) | "Sit. Where I can see you." | Imperative, no softening |
| 3 (Tease) | "Lessons run late tonight. Hope you weren't planning anything." | Sarcasm with intent under it |
| 4 (Cracked) | "Come here." | Two words. Doesn't pretend anymore. |

### What Frank's INTERIOR (when authored as Tier-3) sounds like

When using NPC thought bubbles (S8 from doc 14, currently Phase 3 deferred but Tier-3 prose can hint at interiority via narration):

- Frank is mostly self-contained. Interior monologue rare.
- When it happens, the same speech rules apply — short sentences, concrete things, no elaboration.
- Example: *He watches her cross the kitchen. Tracks the way she moves now. Different from the first week. Doesn't know what to do with that.*
- Avoid: explicit emotional declarations like "He felt a stirring." Use action.

### Voice anti-patterns (BANNED)

- ❌ "Frank's eyes lit up with surprise" — too explicit, too cinematic
- ❌ "He couldn't help but feel..." — generic, lazy
- ❌ "Maya, I want you to know..." — over-named, too direct
- ❌ Frank explaining his backstory unprompted
- ❌ Frank using academic vocabulary or polysyllabic words ("nevertheless," "consequently")
- ❌ Frank apologizing in words (he adjusts behavior, doesn't say sorry)

---

## §3 Frank's extended schedule (where he is each time band)

Audit revealed Frank's schedule covers M, DINPREP, E bands. The new ambient scenes need Frank present in *other* bands too. Authoring his extended schedule here:

| Band | Time | Frank's location | Notes |
|---|---|---|---|
| EM | 05:00–06:30 | Bedroom (sleeping) → Kitchen (just-rising at ~05:30) | Scene #6 (kitchen coffee alone) targets the 05:30-06:30 window |
| M | 06:30–08:30 | **Kitchen [existing scene #1]** | His main morning surface |
| A | 14:00–17:00 | Office (split with porch) | Scene #7 (living room radio) is 14:00-16:00 alt activity; sometimes on porch |
| DINPREP | 17:00–18:30 | **Kitchen [existing scene #2]** | His prepping-dinner window |
| Pre-E | 18:30–19:00 | **Porch (smoke break) [scene #8]** | Brief evening smoke |
| E | 19:00–21:30 | **Office [existing scene #4 + activity bookkeeping]** | His main work window |
| N | 21:30–23:00 | Living room (TV) → Hallway → Bedroom | Scene #5 (hallway pass) targets the transit between rooms |
| LN | 23:00–02:00 | Bedroom (mostly asleep) | Scene #11 (kitchen raid) is the rare insomnia exception, ~once/week |

**Engine compatibility check:** the new scenes use `npc_frank_present` as the condition (engine evaluates Frank's location at trigger time). The schedule above informs *when* triggers will likely match — actual presence is data-driven by canvas schedules and NPC location updates. This doc specifies authorial intent; the engine handles enforcement.

If Frank's location at any band is ambiguous (engine doesn't know where he is), the trigger silently fails — fine, just means the scene doesn't fire that day. Not a bug.

---

## §4 Tier discrimination — concrete Frank examples

So the author knows what each tier looks like in Frank's voice.

### Tier 1 — Utility one-liner

**Use case:** Activities, stat-tick acknowledgments. Player did a thing; world acknowledges it; move on.

**Word count:** 5-15 words.

**Frank example:**
```
KITCHEN CHORES
You wash the dishes. Frank passes through, nods.
[Return ↩️]
```

That's the entire scene. One image at top, one stage direction, exit. No dialogue, no character moment. Pure mechanical confirmation.

### Tier 2 — Vignette prose

**Use case:** Random ambient encounters. Player walks into a room; brief moment with Frank; small narrative texture; exit.

**Word count:** 30-100 words.

**Frank example:**
```
HALLWAY
Frank passes you in the hallway. Coffee mug in his hand,
the chipped one with the boat on it. He nods.

Frank: "Lights left on in the living room."

You stand there a second.

Frank: "I got it."

He keeps walking. The kitchen door swings shut behind him.
[Bedroom 🛏️] [Kitchen 🍳]
```

~50 words. One physical detail (chipped mug with boat). Two short Frank lines. Player has no dialogue choice — this is ambient, not interactive. Tier-2 vignette done.

### Tier 3 — Scripted character writing

**Use case:** Stage-flag capstones. Named-NPC introductions. Crisis moments. Rare — reserved for moments that earn the density.

**Word count:** 200-600 words.

**Frank example (excerpt from a hypothetical catch polish):**
```
LIVING ROOM
She's on the couch when she hears the back door open. Not
a slam — Frank doesn't slam. The careful weight of the door
fitting back into its frame, the soft click of the latch.
She knows the sound. Has heard it every night for three
weeks now, after he comes in from the porch.

Tonight she didn't expect him this early.

The hallway light catches him before she sees his face.
He stops in the doorway. Looks at her. Looks at the lamp.
Looks at her again.

Frank: "Late."

That's all he says. One word. The air in the room changes
shape around it.

She sits up.

Frank: "Door's supposed to be locked by ten."

She opens her mouth to explain.

Frank: "Don't."

He doesn't move from the doorway. Doesn't sit. Doesn't ask
what she was doing. Just stands there in the hallway light
with the look she's never seen on him before — not anger,
not exactly. Something tighter. Something with measurement
in it.

[Stay where you are]
[Go to your room]
```

~200 words. Sensory grounding ("careful weight of the door fitting back into its frame, the soft click of the latch"). Character voice in the implied things ("Frank doesn't slam"). Real choice at the end with weight to it. Tier-3.

### What separates Tier 2 from Tier 3 (the discipline)

| Aspect | Tier 2 | Tier 3 |
|---|---|---|
| Length | 30-100 words | 200-600 words |
| Sensory detail | One concrete object | Multiple, layered |
| Frank's interiority | None | Hinted via action/observation |
| Player interiority | Minimal | Present (small thoughts, observations) |
| Stakes | Low — moment passes | Higher — moment changes something |
| Choice weight | Often no choice (ambient) or low-weight | Real choice that diverges |
| Pacing | Brisk | Slowed deliberately |

If a Tier-2 scene starts feeling like Tier-3, *cut it shorter*. If a Tier-3 scene reads like Tier-2, *deepen it*. Don't compromise to a middle ground — the discrimination is the point.

---

## §5 The 12-scene library — overview table

Reference for the whole set. Detailed specs in §6–§17.

| # | ID | File | Type | Tier | Status |
|---|---|---|---|---|---|
| 1 | `scene_kitchen_with_frank_morning` | `5_scenes.toml` | Existing — stage cascade | T2 (Stage 0-3), T3 (Stage 4 polish) | Polish Stage 4 only |
| 2 | `scene_kitchen_with_frank_dinprep` | `5_scenes.toml` | Existing — stage cascade | T2 | Keep as-is |
| 3 | `scene_living_room_evening` (catch) | `5_scenes.toml` | Existing — capstone (one-time) | T2 → **T3 polish** | Polish prose, preserve flag effects |
| 4 | `scene_franks_office_supervised` | `5_scenes.toml` | Existing — stage cascade | T2 | Keep as-is |
| 5 | `scene_hallway_frank_pass` | `5_scenes.toml` | NEW — random ambient | T1 (low) → T2 (mid+) | Sample scene #1 (Step 3) |
| 6 | `scene_kitchen_frank_coffee_alone` | `5_scenes.toml` | NEW — random ambient | T2 | |
| 7 | `scene_living_room_frank_radio` | `5_scenes.toml` | NEW — random ambient | T2 | |
| 8 | `scene_porch_frank_evening_smoke` | `5_scenes.toml` | NEW — random ambient | T2 | |
| 9 | `activity_talk_to_frank` | `3_activities.toml` | NEW — player-initiated deterministic | T2 / T3 (depends on tier) | Sample scene #2 (Step 3) |
| 10 | `activity_help_with_chores` | `3_activities.toml` | NEW — player-initiated deterministic | T1 utility | |
| 11 | `scene_kitchen_late_night_raid` | `5_scenes.toml` | NEW — time-gated rare | T3 | |
| 12 | `hint_frank_radio_bill_overdue` | `4_story_arc.toml` | NEW — crisis priority hint variant | — | |

---

## §6 Scene #1 — `scene_kitchen_with_frank_morning` (POLISH only Stage 4)

### Type
Existing — stage cascade (M band 06:30-08:30, daily cooldown). Author currently has stage-conditional `[group]` blocks for each stage 0-4.

### Polish target
Only the Stage 4 "cracked summons" branch. Stage 0/1/2/3 paragraphs stay verbatim.

### Why polish Stage 4
Stage 4 is "cracked" — Frank has dropped pretense. This is a Tier-3 capstone moment per D1 carve-out. Current prose likely matches the Tier-2 cascade pattern; polish makes Stage 4 land differently than earlier stages (which is the narrative point of Stage 4).

### Polish guidance
- Length target: 200-300 words for the Stage 4 branch
- Add: one sensory detail (kitchen physical environment), one beat of Maya's interiority, dropped pretense in Frank's dialogue
- Keep: existing trigger conditions, existing flag/effect writes (don't touch)
- Voice: Frank Stage 4 = "Come here." style. Not pleading, not declarative — assured.

### Authoring notes
- Resist the temptation to escalate further. Stage 4 is "cracked" not "complete" — there's still distance.
- Maya's interiority should reflect ambivalence, not clear approval/disapproval — let player project.

### Test plan
1. Use `dev_advance_frank_to_4` shortcut to reach Stage 4
2. Trigger morning kitchen scene
3. Verify Stage 4 branch reads visibly different (more layered, longer) than Stage 3
4. Verify all original flag effects still write correctly

### Cross-references
- Stage 4 is gated by `frank_cracked` flag (set by `dev_advance_frank_to_4` only in slice)
- Stage 3 → 4 helper deferred per D3

---

## §7 Scene #2 — `scene_kitchen_with_frank_dinprep` (KEEP as-is)

### Status
No changes. Existing scene works for Phase 1. Stage cascade structure already supports the sandbox layer (the new ambient scenes complement, don't replace).

### Why no changes
- Already Tier-2 across all stages — appropriate for routine repeating dinner-prep beat
- DINPREP band is well-utilized — adding more here creates stacking with #2
- Kitchen morning (#1) gets Stage 4 polish; this scene doesn't need it

---

## §8 Scene #3 — `scene_living_room_evening` (CATCH — POLISH to Tier-3)

### Type
Existing — capstone (one-time guard, branch-inside-shell). Triggers when corruption ≥ 45, player in living room, E/N band.

### Why polish
This is the canonical Stage 1 → 2 transition. The narrative pivot of Frank's arc. Currently authored as Tier-2 (estimated ~320 words per audit). Promotes to Tier-3 because:
- Capstone moment (D1 carve-out applies)
- Player will reach this scene at most once (one-time guard) — words spent here have outsized impact
- Sets the tone for everything in Stage 2+ (the "Restrict" stage starts here)

### Polish target
Full prose rewrite of the catch beat. Preserve every flag effect (`frank_caught`, `frank_restrict_declared`, `frank_stage = 2`). Preserve trigger conditions. Surgical prose-only edit.

### Sample prose (target reference for author)

```
LIVING ROOM
She's on the couch when she hears the back door open.
Not a slam — Frank doesn't slam. The careful weight of
the door fitting back into its frame, the soft click of
the latch. She knows the sound now. Has heard it every
night for three weeks, after he comes in from the porch.

Tonight she didn't expect him this early.

The hallway light catches him before she sees his face.
He stops in the doorway. Looks at her. Looks at the lamp
on the side table — the one she turned on after sundown,
the one he doesn't usually find on. Looks at her again.

Frank: "Late."

That's all he says. One word. The air in the room changes
shape around it.

She sits up. The book she wasn't reading slides off her
lap onto the cushion.

Frank: "Door's supposed to be locked by ten."

She opens her mouth to explain — about the hour, about
losing track, about the porch light she meant to turn off
and forgot. Her voice catches before any of it gets out.

Frank: "Don't."

He doesn't move from the doorway. Doesn't sit. Doesn't
ask what she was doing. Just stands there in the hallway
light with a look she's never seen on him before — not
anger, not exactly. Something tighter. Something with
measurement in it. Like he's been thinking about this
for longer than tonight.

The clock above the kitchen says 11:47.

[Stay where you are]
[Go to your room]
```

~270 words. Sensory layered (door sound, lamp, book sliding, clock). Frank's voice unchanged from spec. Real choice at the end with weight.

### Choice effects (preserve from existing — verify in current TOML)
- "Stay where you are" → flag `frank_caught_stayed = true`, +0 trust, +1 Frank corruption
- "Go to your room" → flag `frank_caught_obeyed = true`, +1 Frank trust, -1 Frank corruption

Both: `frank_restrict_declared = true`, `frank_stage = 2`, scene marked one-time complete.

### Authoring notes
- The clock detail (11:47) is a deliberate beat — Frank said "ten." She's nearly two hours over. Don't lampshade it; let player notice.
- "Something tighter. Something with measurement in it." is doing work — *measurement* implies he's been gathering evidence. Don't replace with a generic word.
- Maya's interiority is brief (one beat: "the book she wasn't reading") — don't expand it. Tier-3 doesn't mean overwrite.

### Test plan
1. Pre-conditions: player at corruption ≥ 45, living room, E or N band, never triggered before
2. Verify scene fires
3. Read full Tier-3 prose
4. Make a choice → verify flag writes correctly + stage advances to 2
5. Try to re-trigger → verify one-time guard prevents

### Cross-references
- One-time guard implementation: existing in `5_scenes.toml`
- Triggers Stage 2 hint variants in `4_story_arc.toml`

---

## §9 Scene #4 — `scene_franks_office_supervised` (KEEP as-is)

### Status
No changes. Existing Stage 2/3/4 cascade handles post-catch office content. Tier-2 appropriate for repeatable surface.

### Why no changes
Sample audit shows ~260 words across 3 stages — appropriate density for the cascade. Stage 4 branch could use polish (similar to scene #1) but defer until pilot validates Stage 4 ever gets reached naturally.

---

## §10 Scene #5 — `scene_hallway_frank_pass` (NEW — sample scene)

**This is sample scene #1 in Step 3 — first scene to author. Establishes the random ambient + tier-branched pattern.**

### Type
Random ambient encounter. Triggered when player enters Hallway from any other room, Frank present at home in N band.

### Trigger conditions
```toml
location = "loc_hallway"
chance = 0.30
schedules = [
  { weekdays = [0,1,2,3,4,5,6], start_time = "21:30", end_time = "23:00" }
]
trigger_conditions = {
  version = "1.0",
  logic = "AND",
  items = [
    { type = "npc_at_home", subject = "npc_frank" }
  ]
}
cooldown = "daily"  # once per day max
```

### Stage applicability
All stages 0+. Content branches by Frank trust tier inside the scene.

### Stat-tier branches (in-scene `[group]` blocks)

| Tier label | Condition | Content variant |
|---|---|---|
| Low | `npc_frank.trust < 5` | Tier-1 utility: just a passing nod, no dialogue. ~15 words. |
| Mid | `npc_frank.trust 5-15` | Tier-2 vignette: brief exchange about the house (lights, doors, weather). ~50 words. |
| High | `npc_frank.trust >= 15` | Tier-2 vignette extended: small personal beat (Frank notices something about Maya, or vice versa). ~80 words. |

### Sample prose

**Low (trust < 5):**
```
HALLWAY
Frank passes you in the hallway. Coffee mug in his hand.
He nods.
[Bedroom 🛏️] [Kitchen 🍳] [Living Room 🛋️]
```

**Mid (trust 5-15):**
```
HALLWAY
Frank passes you in the hallway. Coffee mug in his hand,
the chipped one with the boat on it. He nods.

Frank: "Lights left on in the living room."

You stand there a second.

Frank: "I got it."

He keeps walking. The kitchen door swings shut behind him.
[Bedroom 🛏️] [Kitchen 🍳] [Living Room 🛋️]
```

**High (trust >= 15):**
```
HALLWAY
Frank passes you in the hallway. Coffee mug in his hand,
the chipped one with the boat on it.

Frank: "Lights on in the living room."

You start to apologize.

Frank: "Wasn't asking."

He glances at you — quick, unreadable — and keeps walking.

Frank: "Late tonight. You eat?"

The kitchen door swings shut behind him before you answer.
[Bedroom 🛏️] [Kitchen 🍳] [Living Room 🛋️]
```

### Choice structure
None — this is ambient, not interactive. Player exits to whichever room they choose.

### Authoring notes
- The "chipped mug with the boat on it" detail is the recurring physical anchor — same mug across many Frank scenes. Tiny world-building.
- Voice is consistent across tiers — what *changes* is what Frank says, not how he says it. He becomes more present at higher trust, not more verbose.
- Maya's interiority absent throughout — this is observational, brisk.

### Test plan
1. Trust 0, N band, walk Bedroom → Hallway. Roll a few times to verify chance fires (with luck, ~3 attempts).
2. Verify low-tier prose renders.
3. Use dev shortcut to set Frank trust = 10. Re-trigger. Verify mid-tier prose.
4. Set trust = 20. Re-trigger. Verify high-tier prose.
5. Verify daily cooldown — second hallway pass same day shouldn't fire.

### Cross-references
- Uses S1 (per-block text_variants) once shipped — but Phase 1 uses the existing `[group]` block pattern with conditions, which works today
- Frank schedule: depends on Frank being at home in N band per §3

---

## §11 Scene #6 — `scene_kitchen_frank_coffee_alone` (NEW)

### Type
Random ambient encounter. Triggered on kitchen entry EM 05:30-06:30 (just before his official kitchen-morning window).

### Trigger conditions
```toml
location = "loc_kitchen"
chance = 0.35
schedules = [
  { weekdays = [0,1,2,3,4,5,6], start_time = "05:30", end_time = "06:29" }
]
trigger_conditions = {
  version = "1.0",
  logic = "AND",
  items = [
    { type = "npc_at_location", subject = "npc_frank", value = "loc_kitchen" }
  ]
}
cooldown = "daily"
```

Note: this fires *before* scene #1 (kitchen morning M band 06:30-08:30) — different time window, no conflict.

### Stage applicability
All stages 0+. Content branches more by player tier than stage.

### Stat-tier branches

| Tier | Condition | Content variant |
|---|---|---|
| Low | trust < 10 | T2: Frank quiet, distant. Maya feels intrusive. ~40 words. |
| Mid | trust 10-20 | T2: Brief exchange, almost-companionable. ~70 words. |
| High | trust >= 20 | T2: Real moment — Frank lets her in on something small (a memory, an opinion). ~100 words. |

### Sample prose (low tier only — full prose for other tiers in authoring pass)

**Low (trust < 10):**
```
KITCHEN
The kitchen is dim — only the light over the stove. Frank
is at the counter, back to you, mug in his hand. He hears
you come in. Doesn't turn around.

Frank: "Coffee's there."

He gestures with his mug at the pot on the stove without
looking. You pour a cup. The two of you stand on opposite
sides of the kitchen, drinking coffee, not talking.

After a minute Frank rinses his mug in the sink and walks
out. The kitchen door swings shut behind him.
[Make breakfast 🍳] [Leave kitchen 🚪]
```

~75 words. The detail "only the light over the stove" sets atmosphere economically.

### Choice structure
- Make breakfast → goes to existing kitchen activity / makes food
- Leave kitchen → returns to hallway

### Authoring notes
- The "back to you" + "doesn't turn around" beat is doing work — establishes Frank's distance physically without saying "Frank was distant."
- Compress rather than expand — even mid/high tier should stay under 100 words.

### Test plan
1. Day 1 Monday EM. Walk to kitchen at 05:45.
2. Verify scene fires (35% — may need 2-3 attempts).
3. Verify low-tier prose at trust 0.
4. Verify cooldown — re-entering kitchen same day shouldn't fire.

---

## §12 Scene #7 — `scene_living_room_frank_radio` (NEW)

### Type
Random ambient encounter. Living room entry A 14:00-16:00.

### Trigger conditions
```toml
location = "loc_living_room"
chance = 0.25
schedules = [
  { weekdays = [0,1,2,3,4,5,6], start_time = "14:00", end_time = "16:00" }
]
trigger_conditions = {
  version = "1.0",
  logic = "AND",
  items = [
    { type = "npc_at_location", subject = "npc_frank", value = "loc_living_room" }
  ]
}
cooldown = "daily"
```

### Stage applicability
All stages 0+. Tier-branches by trust.

### Stat-tier branches

| Tier | Condition | Content variant |
|---|---|---|
| Low | trust < 10 | T2: Frank fiddling with radio, Maya can sit nearby or leave. Companionable silence at best. ~50 words. |
| Mid | trust 10-20 | T2: Brief discussion of the radio (his old habit, what station he wants). ~80 words. |
| High | trust >= 20 | T2: Real conversation about something he heard / a memory the music brought up. ~100-120 words. |

### Choice structure
- "Sit and listen" → +0.25 trust, +0 effects, advances time 30min, scene ends warmly
- "Leave" → no effects, exit

### Authoring notes
- Radio detail: old AM radio, the kind Frank's owned forever, doesn't get good reception
- Music genre: country / classic rock / news depending on band — author's choice but stay consistent across replays
- Frank's relationship to the radio: ritual, not pleasure — he listens because he always has

### Sample prose pending authoring pass (low tier first to set the bar).

---

## §13 Scene #8 — `scene_porch_frank_evening_smoke` (NEW)

### Type
Random ambient encounter. Porch entry E 18:30-19:00 (the half-hour buffer between kitchen dinprep and office).

### Trigger conditions
```toml
location = "loc_porch"  # or loc_back_porch — verify with current TOML
chance = 0.40
schedules = [
  { weekdays = [0,1,2,3,4,5,6], start_time = "18:30", end_time = "18:59" }
]
trigger_conditions = {
  version = "1.0",
  logic = "AND",
  items = [
    { type = "npc_at_location", subject = "npc_frank", value = "loc_porch" }
  ]
}
cooldown = "daily"
```

Higher chance (40%) than other ambients because the time window is short (30 min) — ensures the scene is reachable.

### Stage applicability
All stages 0+. Tier-branches by trust.

### Stat-tier branches

| Tier | Condition | Content variant |
|---|---|---|
| Low | trust < 5 | T2: Frank smoking, brief acknowledgment of Maya's presence, no exchange. ~40 words. |
| Mid | trust 5-15 | T2: Frank shares a thought about the day or the property. ~70 words. |
| High | trust >= 15 | T2: Almost-friendly conversation, Frank in his most relaxed mode. ~100 words. |

### Sensory anchors (consistent across all tiers)
- Cigarette smell
- Porch light beginning to be needed (twilight)
- Crickets / distant traffic / property-specific ambient sound
- Frank's posture: leaning on the rail, weight on one elbow

### Choice structure
- "Stay a minute" → +0.5 trust at high tier, +0.25 at mid, no effect at low
- "Leave" → exit

### Authoring notes
- This scene is the warmest of the ambient set — porch + cigarette + sunset combine to create unguarded moment
- Frank doesn't offer Maya a cigarette. If she asks, he doesn't comment but extends the pack. Doesn't lecture.
- Don't romanticize the cigarette. It's an old habit, not a character trait.

---

## §14 Activity #9 — `activity_talk_to_frank` (NEW — sample scene)

**This is sample scene #2 in Step 3 — second priority for authoring. Establishes the player-initiated deterministic + tier-branched dialogue pattern.**

### Type
Player-initiated activity. Choice "Talk to Frank" appears in any room where Frank is present, available once per day for trust-gain (subsequent visits same day still trigger content but no trust gain).

### Trigger conditions
- Available when: Frank present in player's current location
- Cost: AddTime(1) [advances 1 time bucket]
- Effects on first use per day: +0.5 npc_frank.trust
- Effects on subsequent uses same day: no trait changes (content still plays)

### Stage applicability
All stages 0+. Content branches by trust + stage combined.

### Tier branches (this is where dialogue swap matters most)

| Trust | Stage | Tier | Conversation type |
|---|---|---|---|
| < 5 | 0 | T2 | Small talk: weather, the house, brief practical exchange |
| 5-14 | 0 | T2 | Slightly more personal: he asks about her week, she answers |
| 15+ | 1 | T2-T3 | Real conversation: he mentions something about himself unprompted |
| Any | 2 (post-catch) | T2 | Cooler — controlled, formal. Trust gain reduced to 0.25. |
| Any | 3-4 | T3 | Charged — different texture entirely, depending on Stage |

### Sample prose

**Low trust (< 5), Stage 0:**
```
TALK TO FRANK
You catch Frank's eye. He doesn't look away, but he doesn't
soften either.

Frank: "Need something?"

You: "Just saying hi."

He nods. Waits a beat to see if there's more. There isn't.

Frank: "Alright."

He goes back to whatever he was doing.
[Return ↩️]
```

~50 words. Almost a non-conversation. Frank doesn't reject her, but doesn't engage either.

**Mid trust (5-14), Stage 0:**
```
TALK TO FRANK
Frank looks up when you come into his line of sight.

Frank: "How was your day?"

You: "Long. School stuff."

Frank: "Mm."

He thinks a second. Tries again.

Frank: "Eat something. Bread's still good. Soup in the
fridge from Tuesday."

You: "Thanks."

Frank: "Mm."

He's not great at this. But he's trying.
[Return ↩️]
```

~75 words. Frank trying to engage and not quite succeeding — that's the character moment.

**High trust (15+), Stage 1:**
```
TALK TO FRANK
Frank's at the kitchen table with the books open. Looks up
when you sit down across from him.

Frank: "Tea on the stove. You want some."

You: "Sure."

You make the tea. Bring two mugs back. Frank pushes the
ledger to the side.

Frank: "My wife used to have peppermint. Hated it myself —
tastes like medicine. But she'd brew it every night after
dinner."

He pauses.

Frank: "Place still smells like it sometimes. Top of the
kitchen pantry. You ever notice?"

You: "I noticed."

Frank: "Yeah."

He drinks his tea. Doesn't continue.
[Return ↩️]
```

~120 words. Tier-2 with Tier-3 elements. Frank shares something real (the wife, the peppermint) without making it a big speech. The "place still smells like it sometimes" is the kind of detail Frank uses instead of feelings.

### Choice structure
- Player has no in-scene branching — the dialogue plays based on tier
- Exit: [Return ↩️]

### Authoring notes
- **Critical:** Frank doesn't ask Maya questions twice. If she gives a non-answer, he stops asking.
- The wife reference is the first time Frank mentions her in any scene — guard this carefully. Don't repeat the wife reference in other scenes unless Frank is clearly choosing to bring her up again.
- Do NOT have Frank explain his backstory. The peppermint detail is metonymic — it stands in for everything Maya doesn't know.

### Test plan
1. Trust 0, Frank in kitchen. Click Talk to Frank.
2. Verify low-tier prose renders.
3. Verify trust +0.5 (now 0.5).
4. Click Talk to Frank again same day. Verify content plays, trust stays 0.5 (no double-gain).
5. Sleep to next day. Trust should still be 0.5. Click Talk again. Verify trust +0.5 (now 1.0).
6. Set trust = 10 via dev. Re-trigger. Verify mid-tier renders.
7. Set trust = 20 + Stage 1. Re-trigger. Verify high-tier renders with peppermint reference.
8. Set Stage 2. Re-trigger. Verify cooler post-catch tier renders.

### Cross-references
- The wife mention is canonical character development — log in any TLS character bible
- Trust gain rate: deliberately conservative (+0.5/day) to avoid breaking bookkeeping path's Stage 0→1 pacing (still need trust ≥ 15 + bookkeeping ≥ 3)

---

## §15 Activity #10 — `activity_help_with_chores` (NEW)

### Type
Player-initiated. Choice "Help with chores" available in kitchen or porch when Frank present, A or DINPREP bands.

### Trigger conditions
- Available when: Frank present in kitchen OR porch, A or DINPREP band
- Cost: AddTime(1)
- Effects: +0.25 npc_frank.trust, +$5, +1 frank_chore_count

### Stage applicability
Stages 1+ only (Frank doesn't accept help in Stage 0 — he's still suspicious).

### Writing tier
Tier-1 utility. ~15-30 words per render.

### Sample prose
```
HELP WITH CHORES
You help Frank wipe down the counters. He nods at you when
you're done.

Frank: "Appreciate it."

You: "No problem."

[Return ↩️] +$5 +0.25 trust
```

### Authoring notes
- Multiple variants by location: kitchen (wiping counters / dishes), porch (sweeping / hauling firewood)
- Don't elaborate. This is utility — purpose is the stat tick + trust gain
- Subtle differentiation from `activity_morning_chore` (existing, Stage 2+ only): this is voluntary helper-mode, that one is post-catch obligation

### Test plan
1. Stage 1, Frank in kitchen, A band. Verify "Help with chores" choice appears.
2. Click. Verify trust +0.25, money +5, frank_chore_count +1.
3. Stage 0 → verify choice does NOT appear.

---

## §16 Scene #11 — `scene_kitchen_late_night_raid` (NEW)

### Type
Time-gated rare. Kitchen entry N band 22:00-23:00 (per Q5 — late N, not actual LN, to avoid sleep collision).

### Trigger conditions
```toml
location = "loc_kitchen"
chance = 1.0  # always fires when conditions met
schedules = [
  { weekdays = [0,1,2,3,4,5,6], start_time = "22:00", end_time = "22:59" }
]
trigger_conditions = {
  version = "1.0",
  logic = "AND",
  items = [
    { type = "npc_at_location", subject = "npc_frank", value = "loc_kitchen" },
    { type = "trait", subject = "npc", npc_slug = "frank", trait_key = "trust", operator = "gte", value = 5 }
  ]
}
cooldown = "weekly"  # rare — once per week max
```

### Stage applicability
Stages 1+ (Frank not the type to share late-night kitchen with a Stage 0 stranger).

### Writing tier
Tier-3 throughout. ~250-400 words.

### Why Tier-3
This is the RTS-style "we're both up too late" trope. The rarity (once/week) + the unusual time slot make it a small capstone every time it fires. Players who trigger it should remember the scene.

### Stat-tier branches

| Tier | Condition | Content variant |
|---|---|---|
| Mid | trust 5-15 | Stiff at first, gradually unguarded. Frank shares something brief. |
| High | trust >= 15 | Real conversation about the past, the property, the wife maybe. |

### Sample prose (high tier excerpt)

```
KITCHEN
22:14. The house is quiet enough that you can hear the
refrigerator hum. You came down for water, expecting the
kitchen empty.

Frank's at the table. The good lamp on, the overhead off.
A glass of something brown in front of him. He doesn't
look surprised to see you.

Frank: "Couldn't sleep either."

You: "How'd you know I couldn't sleep?"

Frank: "Quiet feet. People who sleep make more noise."

He pushes a glass toward the empty chair across from him.
You sit. He doesn't pour for you.

Frank: "Help yourself if you want."

You don't pour either. The two of you sit at the table
with the refrigerator humming and the night outside the
window pretending to be quieter than it is.

After a minute:

Frank: "Bought this property in '79. My wife wanted to live
where there weren't people for a while. We had people. Up
in the city. Too many of them, too close."

You: "Did it help?"

Frank thinks about it. Drinks.

Frank: "For her, yeah. For a while."

He doesn't elaborate. Doesn't seem to plan to. The clock
above the stove ticks. Somewhere outside, a coyote calls
once and stops.

Frank: "You should sleep."

You: "You too."

Frank: "Yeah."

Neither of you moves.

[Stay a while longer]
[Go back to bed]
```

~300 words. Tier-3 hallmarks: sensory layered (refrigerator hum, lamp choice, coyote), Frank shares unprompted (the '79 detail, the wife wanting to leave the city), Maya's interiority is present but minimal, ends on a charged stillness.

### Choice structure
- Stay a while longer → +1 trust, advances to LN, more conversation reveals
- Go back to bed → +0.5 trust, sleep cycle begins

### Authoring notes
- **The '79 date is canonical** — first canonical fact about the property's history. Don't contradict in other scenes.
- The wife reference here doesn't repeat the peppermint reference (#9 high-tier). They're different memories. Both Frank, both about her, but distinct. This is the discipline: he reveals different things, not the same thing twice.
- "Quiet feet. People who sleep make more noise." — this is the kind of Frank line that's doing double work. Observation + character reveal in 9 words.

### Test plan
1. Stage 1, trust 10, sleep through to next N band 22:15. Walk to kitchen.
2. Verify scene fires (chance 1.0).
3. Verify high-tier prose at trust 20+.
4. Verify weekly cooldown — try again next day, shouldn't fire.

---

## §17 Hint #12 — `hint_frank_radio_bill_overdue` (NEW)

### Type
Crisis priority hint variant. Surfaces in Quests panel when bill_overdue flag set + Frank trust > 5.

### TOML structure (mirrors existing rent-crisis pattern in `4_story_arc.toml`)

```toml
[[story_arc.hints.templates]]
text = "Frank noticed the radio bill on the counter. He didn't say anything but his jaw was tight."
npc_id = "npc_frank"
priority = 10
condition = {
  stage_npc = "npc_frank",
  stage_op = "eq",
  stage_value = 0,
  set_flag = "bill_overdue",
  trait = { subject = "npc", npc_slug = "frank", trait_key = "trust", operator = "gte", value = 5 }
}
```

### Why
Demonstrates that the hint priority + specificity picker can handle crisis-mode swaps for *any* stat-driven event, not just rent. Pattern is identical to existing rent-crisis variant.

### Authoring notes
- Hint text is in-character observation — Maya noticing Frank's reaction, not Frank speaking
- Single sentence with concrete physical detail (jaw tight)
- No "tip" field — the situation IS the hint

### Test plan
1. Set `bill_overdue = true`, Frank trust = 10.
2. Open Quests panel.
3. Verify Frank's hint shows the new crisis variant text (not the baseline "Frank wants help with the books").
4. Set `bill_overdue = false`. Verify baseline returns.

### Cross-references
- Mirrors `4_story_arc.toml` lines 60-64 (existing rent-crisis variant)
- Uses existing hint priority picker (v1.py:4704-4745)

---

## §18 Authoring sequence

Step-by-step order with deliverables and gates.

### Step A — Doctrine doc updates (1-2 hours)

1. Update `feedback_tls_scene_body_style.md` (memory entry) with D1 carve-out:
   - Default: RTS-flat for routine scene bodies
   - Carve-out: Tier-3 allowed for named-NPC intros, stage-flag capstones, crisis hint scenes
2. Add a one-paragraph note to `02_NPC_Stage_Chains.md`: stages = capstone layer; ambient scene library = daily texture layer
3. Add a section to `11_Hint_Authoring_Guide.md` if needed (hint #12 already follows existing crisis-priority pattern, may not require new section)

**Gate:** doctrine docs reflect sandbox direction. Future writers won't auto-default to old patterns.

### Step B — Author 3 sample scenes (4-6 hours)

Order matters — do them in this sequence:

1. **Scene #5 (`scene_hallway_frank_pass`)** — proves random ambient + tier-branching
2. **Activity #9 (`activity_talk_to_frank`)** — proves player-initiated + multi-tier dialogue
3. **Scene #3 (catch polish)** — proves Tier-3 doctrine works

After each scene:
- Build slice
- Use dev shortcuts to set up trigger conditions
- Play the scene
- Verify prose renders at correct tier

**Gate:** 3 scenes work in slice. Tier discrimination visible. No build errors.

### Step C — Author remaining 5 scenes + 1 hint (8-12 hours)

Batch order:
- `5_scenes.toml`: scenes #6, #7, #8, #11
- `3_activities.toml`: activity #10
- `4_story_arc.toml`: hint #12
- `5_scenes.toml`: scene #1 Stage 4 polish

After each batch (every 2-3 scenes): build + 5 min sanity play.

**Gate:** full Frank library in TOML. Slice builds. No regressions.

### Step D — Phase 1 playtest (1 hour focused)

Per §19 protocol below.

**Gate:** §20 decision criteria met.

### Step E — Decision (15 min)

Read playtest results. Decide pass/partial/fail per §20.

If pass → propose Phase 2 (engine S1-S6) + Diana scene library design (doc 17).
If partial → propose targeted fixes.
If fail → revisit doctrine before proceeding.

---

## §19 Test plan / playtest protocol

### Setup

- Fresh save, Day 1 Monday EM
- Player at home (Bedroom)
- Default stats (trust 10 with Frank, corruption 0, exhibitionism 0, money $50)
- No dev shortcuts used

### Phase 1: Day 1 ambient validation (15 min)

Walk normal early-game pattern:
- Bedroom → Hallway → Kitchen (try to catch #6 in EM 05:30-06:30)
- Kitchen → Hallway → Bathroom → Hallway → School (regular morning)
- School activities until afternoon
- Return home 14:30 → Living Room (try to catch #7 in A 14:00-16:00)
- Move around until 18:30 → Porch (try to catch #8 in 18:30-19:00)
- Office 19:00-21:30 (existing scene #4)
- Living room 21:30 → Hallway 21:45 (try to catch #5 in N band)
- Bedroom → sleep

**Pass:** ≥ 2 of #5/#6/#7/#8 fired. New scenes feel woven into the day.
**Fail:** 0 fired. Chance values too low or trigger conditions broken.

### Phase 2: Come-back-later loop validation (10 min)

1. Trigger scene #5 (hallway pass) at trust 0. Read prose. Note details.
2. `dev_set_frank_trust 15`
3. Wait until next day, trigger #5 again. Read prose.
4. Compare — content visibly different?

**Pass:** Mid-tier prose renders, longer + has dialogue exchange.
**Fail:** Same low-tier prose renders. `[group]` conditions or trust evaluation broken.

### Phase 3: Tier discrimination validation (10 min)

Read in sequence:
1. Scene #1 Stage 0 morning kitchen (existing T2)
2. Scene #5 high-tier hallway pass (T2)
3. Scene #11 high-tier kitchen raid (T3)
4. Scene #3 catch polish (T3)

**Pass:** T3 scenes feel visibly more layered, slower, more sensory than T2 scenes. Tier discrimination is apparent in reading order.
**Fail:** T3 reads like longer T2. Polish didn't land. Doctrine carve-out didn't change practice.

### Phase 4: Subjective "Frank feels alive" check (5 min)

After playtest, answer:
- Did Frank "show up unbidden" at least twice during the day?
- Did the new scenes add texture vs feel like noise on top?
- Does Frank feel like a person in the house vs a quest-giver?

**Pass:** All three subjective yes.
**Fail:** Frank still mechanical despite the additions.

---

## §20 Decision gate criteria

After playtest:

| Outcome | Criteria | Next action |
|---|---|---|
| ✅ **Pass** | All 4 phases pass. Frank visibly more alive. Authoring throughput ≤ 20 hours actual. | Propose doc 17 = Diana scene library design. Begin Phase 2 engine work (S1-S6) in parallel. |
| 🟡 **Partial** | 2-3 phases pass. Specific gaps identified. | Triage: add scenes? polish writing tier? defer to Phase 2 engine help (especially S1 in-scene branching)? |
| ❌ **Fail** | 0-1 phases pass. Frank still mechanical. | Revisit doctrine. Likely: linkreplace (S7) is required earlier than planned, OR scene volume needs to be higher (15+ per NPC), OR sandbox philosophy doesn't fit TLS as hoped. Re-plan before any further authoring. |

---

## §21 Risks specific to Frank pilot (with mitigations)

### R1 — New ambient scenes pre-empt cascade scenes
**Mitigation:** Conservative chance values (25-40%). Daily cooldowns on cascade scenes still fire in their windows. Test specifically: trigger ambient scenes on Day 1, verify kitchen morning still fires at 06:30.

### R2 — Tier-3 catch polish breaks the one-time guard
**Mitigation:** Surgical prose-only rewrite. Don't touch flag effects. Build slice and verify the catch still flips frank_stage 1 → 2.

### R3 — Activity #9 disrupts trust pacing
**Mitigation:** +0.5/day cap. Stage 0→1 still requires trust ≥ 15 + bookkeeping ≥ 3 — talk alone can't unlock the stage transition without the bookkeeping path. Test: how many days does trust 0 → 15 take with talk + bookkeeping vs bookkeeping alone?

### R4 — Scene #11 sleep collision
**Mitigation:** N band (22:00-23:00) not LN. Player can do scene before sleeping. Once-per-week cap so it doesn't dominate evenings.

### R5 — Voice consistency drift
**Mitigation:** §2 voice spec at top of doc + per-scene authoring notes. Read all 12 sequentially before declaring done.

### R6 — Frank's extended schedule undefined in engine
**Mitigation:** Document intent in §3. Engine matches at trigger time — if Frank isn't where the schedule expects, scene silently doesn't fire. Author can adjust later.

### R7 — Authoring throughput
**Mitigation:** Step B + C estimates total ~12-18 hours. If it stretches to 25+ hours, scope down — fewer high-quality scenes beats more low-quality ones.

### R8 — Wife reference proliferation
**Mitigation:** Wife mentioned in #9 high-tier (peppermint) and #11 high-tier ('79 city). These are distinct memories — don't repeat in other scenes. Track via authoring notes.

---

## §22 Open questions for after pilot

Captured for transparency, not blockers for Phase 1:

- Should activity #9 trust gain become +1/day if pilot shows player isn't reaching trust 15 fast enough?
- Should ambient scene chance values be tuned per NPC tendency? (RTS-style 25-50% baseline; family-NPCs higher, peer-NPCs lower)
- After Stage 4 polish, should the "cracked" stage get its own scene library expansion?
- Does the sandbox direction warrant rebuilding the test slice fresh, or evolving in place?
- Is doc 16's per-scene template the right shape, or does the next NPC (Diana) need a different format?

---

## §23 TL;DR

12 scenes total: 4 existing + 8 new. 3 sample scenes authored first (Step B) to validate the patterns. Full library authored in Step C. Playtest in Step D. Decision gate in Step E.

**Locked decisions:** D1=B (Tier-3 carve-out), D2=Polish (existing scenes), D3=Defer (Stage 3-4), all answers in §1.

**Frank's voice spec is in §2** — the authoring discipline anchor.

**Frank's extended schedule is in §3** — where he is when not in scheduled bands.

**Tier discrimination examples are in §4** — concrete Frank prose at each of T1/T2/T3.

**Per-scene specs in §6-§17** — sample prose for the 3 priority scenes, full structure for the rest.

**No engine code changes in Phase 1.** Pure content authoring + doctrine doc updates.

**~12-18 hours estimated authoring effort.** Validates the philosophy before Phase 2 engine work.

---

**End of doc 16.** 🟦 Designed, not started. Authoring begins at Step A.
