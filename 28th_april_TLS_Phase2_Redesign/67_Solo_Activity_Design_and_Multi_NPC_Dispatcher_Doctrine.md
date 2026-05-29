# Doc 67 — Solo Activity Design & Multi-NPC Dispatcher Doctrine

**Date:** 2026-05-26
**Author:** ENI (with LO)
**Status:** Doctrine — applies to all RTS-shape sandbox games on this engine.
**Triggered by:** LO question on whether Doc 24–65 covered solo activity design + the multi-NPC dispatcher resolution mechanism. Honest audit (Doc 66 follow-up) confirmed two specific gaps; this doc closes them.
**Extends:** Doc 24 (3-lane mechanism — Lane 3 substitution from the NPC-scene side) + Doc 56 (per-arc canvas distribution) + Doc 57 (capstones).
**Supersedes:** nothing.
**Sibling of:** Doc 24 (which covered the NPC-substitution side of Lane 3 but not the parent activity itself), Doc 56 (which covered authoring rules R1–R7 but did not address solo-activity authoring).
**Source evidence:** live extraction from `game_explorations/rts-arc-trace/` (2026-05-26): 9 RTS passage bodies (7 dispatchers + 2 location passages) pulled verbatim from `passage_catalog.json`; cross-referenced with `notes.md` (8 timestamped observation blocks) and `synthesis_repeatable_narrative_auto_2026-05-10.md` (live-verified Shower Sex dispatch). **Every claim in this doc is source-verified — no hallucination.**

---

## §1 — The question this doc answers

Doc 24 named Lane 3 (the dispatcher substitution mechanism) and covered it from the NPC-scene side: how a "walk-in" scene attaches to a parent activity, when each lane carries which fictional intent, what the per-arc-shape budget looks like. **It did not cover two specific gaps that authoring a new RTS-shape game requires.**

**Gap A — The solo-activity side.** What shape is the parent activity itself? How does RTS author it? What's the menu structure, the dispatcher passage, the time/stat cost model, the per-day cap mechanism? Without this, an author wiring substitution rules into a TOML has nothing concrete to attach them TO.

**Gap B — Multi-NPC dispatcher resolution.** When one parent activity supports walk-ins from MULTIPLE NPCs simultaneously (Maya washes dishes; both Frank AND Jake could walk in), what mechanism does RTS use? Sequential? Single roll? Priority? The TLS engine implements substitution as a sequential first-match (Doc 24 §7), but the authoring rule was never named.

This doc fills both gaps with source evidence. §3 covers the solo-activity anatomy. §4 covers the three distinct multi-NPC patterns observed in RTS. §6 names the rules (R1–R7) future authors apply. §7 is a copy-pasteable template.

---

## §2 — Source evidence (verbatim RTS extraction)

All passages quoted verbatim from `game_explorations/rts-arc-trace/passage_catalog.json` (1.2MB, 2464 passages catalogued, pulled 2026-05-26 this session).

### §2.1 — `BathroomShowerMasturbate` (the canonical Lane 3 dispatcher)

```twee
:: BathroomShowerMasturbate
<center>
<h1 class="ptitle">MASTURBATE 🚿</h1>
<<if isPlayerAtHouse() && random(1,3) == 1 && StageOneCorruption($npc.Brother) && IsNpcAtHome("Brother")>>
    <<goto 'BrotherShowerSex'>>
<<else>>
    <h3 class="ptitle">You masturbate yourself. Corruption increased!</h3>
    [...solo image + body...]
    <<FinishMasturbation>>
<</if>>

<<ReturnButton "Bathroom" "Bathroom 🚾">>
    <<GetDressed>>
<</ReturnButton>>
</center>
```

Pattern: single-NPC dispatcher. 1/3 chance + `StageOneCorruption` + `IsNpcAtHome` → Brother scene, else solo body. ReturnButton outside the if/else, with `<<GetDressed>>` running on click.

### §2.2 — `WashDishes` (two-NPC Pattern A — sequential first-match)

```twee
:: WashDishes
<center>
<h1 class="ptitle">WASHING DISHES</h1>
<<if isPlayerAtHouse()>>
    <<if random(1,3) == 1 && $npc.Dad.arousal > 0 && IsNpcAtHome("Dad")>>
        <<if changeMediaPregnant()>>
            <<goto 'DadWashDishesSexPregnant'>>
        <<else>>
            <<goto 'DadWashDishesSex'>>
        <</if>>
    <<elseif random(1,3) == 1 && $npc.Brother.arousal > 0 && StageTwoCorruption($npc.Brother) && IsNpcAtHome("Brother")>>
        <<goto 'BrotherWashDishesSex'>>
    <<else>>
        <h3>Washing dishes is a boring chore, but it needs to be done.</h3>
        [...solo image...]
    <</if>>
<<else>>
    [...solo-body-when-not-at-home variant...]
<</if>>
<br>
<<ReturnButton "Kitchen">>
    <<AddTime '1'>>
    <<Energy -10>>
<</ReturnButton>>
</center>
```

Pattern: Dad checked first with own `random(1,3)`, Brother checked second with own `random(1,3)`. Sequential evaluation via `if/elseif`. **First-match priority via rule order.** Stat cost (`AddTime`, `Energy -10`) inside ReturnButton, outside all if blocks → applies only on solo-branch return (NPC scenes have their own cost).

### §2.3 — `BedroomStudy` (Pattern B — single dice partition)

```twee
:: BedroomStudy
<center>
<h1 class="ptitle">STUDY</h1>
<<set $game.dice to random(1,6)>>
<<if $game.dice == 1 && $npc.Dad.arousal > 0 && $npc.Dad.corruption > 0>>
    <<goto 'BedroomStudyDadGrope'>>
<<elseif $game.dice == 2 && $npc.Brother.arousal > 0 && $npc.Brother.corruption > 0>>
    <<if changeMediaPregnant()>>
        <<goto 'BedroomStudyBrotherGropePregnant'>>
    <<else>>
        <<goto 'BedroomStudyBrotherGrope'>>
    <</if>>
<<elseif $game.dice == 3 && $npc.Brother.arousal > 0 && $npc.Brother.corruption > 0>>
    <<goto 'BrotherHelpStudy'>>
<<else>>
    [img[setup.ImagePath+'/house/bedroom/study/study.webp']]
    <h3>You studied an hour and feel smarter!</h3>
    <<ReturnButton "Bedroom">>
        <<AddInt>>
        <<Energy -10>>
        <<AddTime '2'>>
    <</ReturnButton>>
<</if>>
</center>
```

Pattern: ONE shared dice roll (`random(1,6)`). Buckets partition the result:
- `dice == 1` (16.7%) → Dad grope (conditions gate)
- `dice == 2` (16.7%) → Brother grope
- `dice == 3` (16.7%) → Brother helps study
- `else` (50%) → solo

**Critical detail:** if `dice == 1` but Dad conditions fail, falls through to ELSE (solo) — NOT to Brother. The dice value claims the slot; failed conditions don't promote the next NPC. Mutual exclusion guaranteed.

ReturnButton with stat cost (`AddInt`, `Energy -10`, `AddTime 2`) inside the ELSE branch — applies only on solo branch.

### §2.4 — `Exercise` (Pattern C — post-activity event check)

```twee
:: Exercise
<center>
<h1 class="ptitle">EXERCISE</h1>
[...solo image + body...]
<h3>You exercise for a while and feel your body getting stronger! 🏋️‍♂️</h3>
<<AddFit>>
<<ReturnButton "LivingRoom" "Living Room 🚪">>
    <<Energy -15>>
    <<AddTime 1>>
<</ReturnButton>>
</center>

<<if isPlayerAtHouse()>>
    <<if GetNpcLocation("Grandpa") == "Living Room" && getCorruptionLevel() >= 4 && random(1,3) == 3>>
        <<goto 'GrandpaExerciseSex'>>
    <</if>>
<</if>>
```

Pattern: solo activity body executes FIRST. `<<AddFit>>` runs unconditionally (outside ReturnButton). Then events block at end of passage rolls for NPC interrupt.

**Key distinction from Pattern A:** if NPC scene fires, `<<AddFit>>` already applied. The activity "counts" toward fitness even if interrupted. Energy/AddTime inside ReturnButton, so only apply on solo branch.

Also note: uses `GetNpcLocation("Grandpa") == "Living Room"` (strict location check), not `IsNpcAtHome` — different from Pattern A. See §3.5.

### §2.5 — `BedroomSleep` (single-NPC dispatcher with `previous()` guard)

```twee
:: BedroomSleep
<center>
<h1 class="ptitle">SLEEP</h1>
[...image...]
<<if $npc.Dad.arousal > 0 && $npc.Dad.corruption > 0 && $player.energy > 0 && random(1,4) == 1 
    && previous() isnot "BedroomSleepDadScene" 
    && previous() isnot "SleepingBrother"
    && previous() isnot "OldSaveImport">>
    <<goto 'BedroomSleepDadScene'>>
<<else>>
    <<SleepCommon>>
    <<button 'Wake up' 'Bedroom'>><</button>>
<</if>>
</center>
```

Pattern: single-NPC dispatcher (Dad only). 1/4 chance. **`previous()` guard** prevents loop-spam: if player just came back from `BedroomSleepDadScene`, won't re-fire immediately. Three previous-passage exclusions catalogued.

### §2.6 — `PlayingVideogame` (Pattern C variant — strict location check)

```twee
:: PlayingVideogame
<center>
<h1 class="ptitle">PLAYING 🎮</h1>
<h3>You are playing a game on the console, you are very focused on the game.</h3>
[...image...]
<<ReturnButton "LivingRoom">>
    <<AddTime 1>>
<</ReturnButton>>
</center>

/*EVENTS */
<<if isPlayerAtHouse()>>
    <<if random(1,3) == 1 && StageTwoCorruption($npc.Brother) && GetNpcLocation("Brother") == "Living Room">>
        <<if changeMediaPregnant()>>
            <<goto "PlayingGamesSexPregnant">>
        <<else>>
            <<goto "PlayingGamesSex">>
        <</if>>
    <</if>>
<</if>>
```

Pattern C variant: solo body first, NPC event at end. Uses `GetNpcLocation("Brother") == "Living Room"` (strict) — Brother must already be in Living Room. Different from `WashDishes` which uses `IsNpcAtHome` (loose).

### §2.7 — `Bathroom` location passage (Lane 2 events on entry, NOT Lane 3)

```twee
:: Bathroom
<center>
<h1 class="ptitle">BATHROOM</h1>
[...image...]
<div class="menuLocation">
    <<button 'Shower 🚿'>>
        <<if $game.time == "LN">>
            <<Notification 'warning' "It's too late, you should go to bed">>
        <<else>>
            <<goto 'BathroomShower'>>
        <</if>>
    <</button>>
    <<button 'Mirror 🪞' 'BathroomMirror'>><</button>>
    [...more activity buttons + return...]
</div>
</center>

/*EVENTS */
<<if isPlayerAtHouse()>>
    <<if previous() == "Hallway">>
        <<if GetNpcLocation("Dad") == "Bathroom" && random(1, 4) == 1>>
            <<if changeMediaPregnant() && !$npc.Dad.scenes.DadShowerSexPregnant.executedToday>>
                <<goto "DadShowerSexPregnant">>
            <<elseif !$npc.Dad.scenes.DadShowerSex.executedToday>>
                <<goto "DadShowerSex">>
            <<elseif !$npc.Dad.scenes.DadPeepSex.executedToday>>
                <<goto "DadPeepSex">>
            <</if>>
        <</if>>

        <<if GetNpcLocation("Grandpa") == "Bathroom" && random(1,4) == 1 && !$npc.Grandpa.scenes.GrandpaShowerSex.executedToday>>
            <<goto "GrandpaShowerSex">>
        <</if>>
    <</if>>
    [...pregnancy variants...]
<</if>>
```

**This is the LOCATION passage, not an activity.** Renders the menu (Shower / Mirror / Pregnancy pill / Hallway). EVENTS at bottom are Lane 2 (location-entry randoms) — fires when player enters bathroom from hallway with NPC already at this location. Uses `GetNpcLocation` (strict).

**Key observation:** Bathroom has Lane 2 events for Dad + Grandpa, but Brother's bathroom content (`BrotherShowerSex`) fires on Lane 3 (inside `BathroomShowerMasturbate`). Same NPC at same location can use different lanes — depends on the fictional intent (Maya walks in on NPC = Lane 2; NPC walks in on Maya = Lane 3). See §3.5 for the rule.

Also: per-day cap via `$npc.Dad.scenes.DadShowerSex.executedToday` — fires once per day per scene.

Also: sequential first-match within Dad's bucket — pregnant variant > non-pregnant > peep. Inner priority by rule order.

---

## §3 — Solo activity anatomy

### §3.1 — The three-layer structure

```
LOCATION PASSAGE (e.g. Bathroom)
  ├─ Menu buttons (time-gated, energy-gated, purchase-gated)
  └─ Lane 2 events (fires on entry from Hallway with NPC at loc)
      │
      ▼
INTERMEDIATE PASSAGE (e.g. BathroomShower) — optional
  ├─ Activity setup (clothes off, image, body)
  ├─ Inline encounter check (e.g. BathroomFlashScene)
  └─ Sub-menu button (Masturbate ❤️‍🔥)
      │
      ▼
DISPATCHER PASSAGE (e.g. BathroomShowerMasturbate)
  ├─ Roll dice + check NPC conditions
  ├─ HIT → <<goto NpcScene>>
  ├─ MISS → render solo content (image + body + ReturnButton)
  └─ ReturnButton applies time/energy cost
```

**Two-step activities** (Bathroom Shower → Masturbate) use an intermediate passage. **One-step activities** (Wash Dishes, Study) go straight from location button to dispatcher.

The dispatcher is always a SEPARATE NAMED PASSAGE — not inline logic in the menu button. This makes substitution rules inspectable, debuggable, and authoring-friendly. Crucially: this is how RTS makes Lane 3 distinct from Lane 1 (hub button) and Lane 2 (location-entry event). The dispatcher passage IS the Lane 3 primitive.

### §3.2 — Location passage anatomy (the menu)

Location passages render the activity menu. Each button:

1. **Conditionally rendered or conditionally enabled.** Example from `Bedroom`:
   ```twee
   <<if $game.time == "LN">>
       <<button '❌ Too late to study ❌'>><</button>>
   <<elseif $player.energy <= 0>>
       <<button '🪫 Too tired to study 🪫'>><</button>>
   <<else>>
       <<button 'Study 📖' 'BedroomStudy'>><</button>>
   <</if>>
   ```
   Disabled-button-with-explanation is the visible-fail pattern (button still renders so player knows the option exists, but click does nothing / shows notification).

2. **OR notification-on-click.** Example from `Bathroom`:
   ```twee
   <<button 'Shower 🚿'>>
       <<if $game.time == "LN">>
           <<Notification 'warning' "It's too late, you should go to bed">>
       <<else>>
           <<goto 'BathroomShower'>>
       <</if>>
   <</button>>
   ```
   Click attempts the action; if gated, shows notification and stays on menu.

3. **Time-of-day, energy, purchase state, quest state** are the four common gates. NPC presence is **NOT checked at menu level** — the dispatcher handles that. Player always sees the activity button regardless of NPC presence.

4. **Naked / corruption gating** on exit-to-other-locations (e.g. Hallway button checks clothing + corruption):
   ```twee
   <<button 'Hallway 🚪'>>
       <<if $player.clothing.type == 'naked' && getCorruptionLevel() < 3>>
           <<Notification 'warning' "I should wear some clothes.. 30+ Corruption Needed">>
       ...
   <</button>>
   ```
   The notification text **publishes the threshold** (Doc 56 P2 transparent gating — verified live here).

### §3.3 — Dispatcher passage anatomy

A dispatcher is a named separate Twine passage with this structure:

```twee
:: DispatcherName
<center>
<h1>ACTIVITY TITLE</h1>

[OPTIONAL: <<if isPlayerAtHouse()>>]

[NPC SCENE CHECK(S) — Pattern A, B, or C — see §4]
    <<goto NpcScene>>

[ELSE BRANCH: solo content]
    <h3>Solo activity description</h3>
    <image>
    [optional: stat-effect macros like <<FinishMasturbation>>]

<<ReturnButton "ParentLocation">>
    <<AddTime N>>
    <<Energy -X>>
<</ReturnButton>>
</center>
```

**Stat cost placement matters.** Two choices:
- Inside ReturnButton (e.g. WashDishes Energy -10): applies ONLY if solo branch reached and player clicks Return.
- Outside ReturnButton (e.g. Exercise `<<AddFit>>`): applies UNCONDITIONALLY whenever the dispatcher is reached, even if NPC scene preempts.

The choice depends on whether the activity should "count" when an NPC walks in (see Pattern C in §4.3).

### §3.4 — Time-of-day + energy + purchase + quest gates

**Authoring rule (verified):** all four gates live in the **location button**, not the dispatcher.

| Gate | Location | Example |
|---|---|---|
| Time-of-day | Location button | `if $game.time == "LN" → notification` |
| Energy | Location button | `if $player.energy <= 0 → disabled button` |
| Purchase | Location button | `if isPurchased("phone") → button visible, else hidden` |
| Quest state | Location button | `if quest active && !done → button visible, else hidden` |
| NPC stage / corruption | Dispatcher | inside the if/elseif on the substitution check |
| NPC presence | Dispatcher | `IsNpcAtHome` or `GetNpcLocation` in substitution check |
| Per-day cap | Dispatcher | `!scenes.XXX.executedToday` in substitution check |

The dispatcher trusts the menu's gating; doesn't double-gate on time/energy.

### §3.5 — NPC presence check: `IsNpcAtHome` vs `GetNpcLocation`

Two distinct checks observed; the choice is doctrine, not arbitrary.

| Check | Semantics | Used for | Fictional intent |
|---|---|---|---|
| `IsNpcAtHome(npcId)` | NPC at home (any room) | Lane 3 dispatchers (`WashDishes`, `BathroomShowerMasturbate`) | "NPC walks in" — Maya is solo, NPC arrives mid-activity. NPC doesn't need to be at the room yet; they "come in" |
| `GetNpcLocation(npcId) == "Loc"` | NPC at exact location | Lane 2 location-entry events (`Bathroom`, `Bedroom` EVENTS blocks) AND Pattern C post-activity events (`Exercise`, `PlayingVideogame`) | "Maya walks in on NPC" — NPC is already there; Maya encounters them |

**Doctrine: direction of the walk-in determines the check.**

- Brother walking in on Maya showering → `IsNpcAtHome` (Lane 3 dispatcher inside `BathroomShowerMasturbate`)
- Dad already in bathroom when Maya arrives → `GetNpcLocation == "Bathroom"` (Lane 2 event on `Bathroom` entry)

This is why same NPC at same location can fire on different lanes — depends on which direction the encounter goes narratively.

### §3.6 — Per-day cooldowns

Two mechanisms observed for preventing same-scene repeat-fire:

1. **`executedToday` flag (per-scene per-day):**
   ```twee
   <<if !$npc.Dad.scenes.DadShowerSex.executedToday>>
       <<goto "DadShowerSex">>
   ```
   Resets at sleep / day rollover. Scene fires at most once per day.

2. **`previous()` guard (per-passage immediate):**
   ```twee
   <<if previous() isnot "BedroomSleepDadScene" 
       && previous() isnot "SleepingBrother"
       && previous() isnot "OldSaveImport">>
   ```
   Prevents the SAME passage that just played from re-triggering. Used in `BedroomSleep` to stop sleep-scene from re-firing if player came back from one.

**TLS engine support:**
- `executedToday` → `max_triggers_per_day = 1` on canvas trigger (already supported)
- `previous() != "X"` → not directly supported; equivalent achievable via flag-set on scene exit + flag-clear on next-day rollover (more complex). For most cases not needed in TLS.

---

## §4 — Multi-NPC dispatcher patterns

Three patterns observed in RTS source. Each is the right answer in different situations. **The selection rule is fictional, not arbitrary.**

### §4.1 — Pattern A: Sequential first-match with independent dice rolls

**Canonical example:** `WashDishes` (§2.2).

```twee
<<if random(1,3) == 1 && $npc.Dad.arousal > 0 && IsNpcAtHome("Dad")>>
    <<goto 'DadWashDishesSex'>>
<<elseif random(1,3) == 1 && $npc.Brother.arousal > 0 && StageTwoCorruption($npc.Brother) && IsNpcAtHome("Brother")>>
    <<goto 'BrotherWashDishesSex'>>
<<else>>
    [...solo content...]
<</if>>
```

**Mechanics:**
- Each NPC has its own `random(1,3)` check.
- Sequential evaluation via `if/elseif`.
- First-match priority: Dad checked first. If Dad's dice rolls 1 AND Dad qualifies, Dad scene fires.
- If Dad's dice fails (rolled 2 or 3) OR Dad doesn't qualify, Brother's fresh dice rolls.
- If both fail, solo branch.

**Probability math:**
- P(Dad scene) = (1/3) × P(Dad qualifies)
- P(Brother scene | Dad didn't fire) = (1/3) × P(Brother qualifies)
- P(solo) = remainder

**Worked example:** Both Dad and Brother home + qualified.
- P(Dad scene) = 1/3 ≈ 33%
- P(Brother scene) = (2/3) × (1/3) = 2/9 ≈ 22%
- P(solo) = (2/3) × (2/3) = 4/9 ≈ 44%

Cumulative P(any NPC) ≈ 55%. Higher than single-NPC chance (33%), as expected.

**Use when:**
- Multiple NPCs could plausibly walk in on the same chore
- One NPC has narrative priority (escalation NPC, current focus arc)
- Mutual exclusion not required — only one fires per attempt anyway (because `<<goto>>` preempts)

### §4.2 — Pattern B: Single dice partition

**Canonical example:** `BedroomStudy` (§2.3).

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

**Mechanics:**
- ONE shared dice roll.
- Buckets partition the result: 1=Dad, 2=Brother grope, 3=Brother help, 4-6=solo.
- **Mutual exclusion guaranteed** — impossible for two NPCs to fire simultaneously.
- **Failed-condition falls through to ELSE, NOT to next NPC.** If dice == 1 but Dad doesn't qualify, the result is solo, not Brother. The dice value claims the slot.

**Probability math:**
- P(Dad scene) = 1/6 × P(Dad qualifies)
- P(Brother grope) = 1/6 × P(Brother qualifies)
- P(Brother help study) = 1/6 × P(Brother qualifies)
- P(solo) = 3/6 + (failed-condition contributions)

**Worked example:** Both Dad and Brother qualified.
- P(Dad) = 1/6 ≈ 17%
- P(Brother grope) = 1/6 ≈ 17%
- P(Brother help) = 1/6 ≈ 17%
- P(solo) = 3/6 ≈ 50%

P(any NPC) = 50%. Fixed budget across all outcomes.

**Use when:**
- NPC scene variants are inherently mutually exclusive by design
- Author wants explicit probability budget across all outcomes
- Multiple variants of the same NPC (Brother grope vs Brother help study — same NPC, two different walk-ins, one fires)

### §4.3 — Pattern C: Post-activity event check

**Canonical examples:** `Exercise` (§2.4), `PlayingVideogame` (§2.6).

```twee
[...solo activity body + image...]
<<AddFit>>
<<ReturnButton>>
    <<Energy -15>>
    <<AddTime 1>>
<</ReturnButton>>

/*EVENTS */
<<if random conditions>>
    <<goto NpcScene>>
<</if>>
```

**Mechanics:**
- Solo body processes first (image set, `<<AddFit>>` runs).
- Event block at end of passage.
- If conditions hit, `<<goto>>` preempts the page display — player goes to NPC scene without seeing solo content.
- Stat changes OUTSIDE ReturnButton apply unconditionally; stat changes INSIDE ReturnButton apply only if solo.

**Why use this pattern instead of A/B?**

The activity has an unconditional stat outcome. Exercise = +Fit regardless of who walks in. The fitness training "counts" even if Grandpa interrupts.

In Pattern A (WashDishes), all stat changes are inside ReturnButton — if Dad walks in, Maya never finishes the dishes, no Energy cost / Time advance from the chore. The chore was abandoned. Different design call.

**Pattern C also uses `GetNpcLocation == "Loc"` (strict location check), not `IsNpcAtHome`.** This matches the post-activity timing: by the time the event check fires, Maya is at the location actively doing the thing; the NPC needs to be co-located to interrupt.

### §4.4 — Selection rule (the doctrine call)

From source evidence, three patterns coexist in RTS for different design purposes. **The selection rule:**

| Authoring intent | Pattern |
|---|---|
| "Multiple independent NPCs could walk in on this chore; priority by arc focus" | **A** (sequential first-match) |
| "Several mutually exclusive variants — one fires per attempt" (often same NPC with sub-variants) | **B** (dice partition) |
| "Activity has unconditional stat outcome that 'counts' even when interrupted" | **C** (post-activity check) |
| **Default for new authoring** | **A** |

For TLS slice authoring, default to Pattern A. Pattern B and C are tools for specific intents that arise in particular activities.

### §4.5 — Lane 2 location-entry events (NOT a Lane 3 dispatcher pattern, but related)

Location passages have their own EVENTS block at the bottom that handles Lane 2 (random encounter on entry):

```twee
:: Bathroom
[...menu...]

/*EVENTS */
<<if isPlayerAtHouse()>>
    <<if previous() == "Hallway">>
        <<if GetNpcLocation("Dad") == "Bathroom" && random(1, 4) == 1>>
            [...Dad shower events...]
        <</if>>
        <<if GetNpcLocation("Grandpa") == "Bathroom" && random(1,4) == 1 && !$npc.Grandpa.scenes.GrandpaShowerSex.executedToday>>
            <<goto "GrandpaShowerSex">>
        <</if>>
    <</if>>
<</if>>
```

**Key Lane 2 mechanics:**
- Fires on `previous() == "Hallway"` (transition gate — only on entry from hub, not on re-entry to same location)
- Uses `GetNpcLocation == "Bathroom"` (strict location check — NPC must be IN this room)
- Sequential first-match across NPCs (Dad checked before Grandpa)
- Per-day cap via `executedToday`

This is documented here for completeness; the load-bearing Lane 3 patterns are §4.1–§4.3.

---

## §5 — TLS engine support (current state)

> **⚠️ Engine support summary (read first):** Pattern A is fully supported in the current TLS engine. **Patterns B and C are NOT YET SUPPORTED.** Slice-phase authoring should default to Pattern A only. Engine extensions for B and C are documented in §5.1 + §5.2 as forward proposals — scoped out per Doc 56 §9 doctrine ("build engine when an authoring gap forces it"). When a slice case requires Pattern B or C semantics, surface the decision to LO; either land the engine extension first, or accept the Pattern A workaround knowing the documented divergence.
>
> **Correction history:** Doc 67's initial §5 table claimed Pattern C was "✅ Native via authoring" and Pattern B was "⚠️ Approximation only." Code verification this session (v2.py:4597-4626 + v2.py:11020-11053) showed both claims were wrong — the substitution check is emitted FIRST in the canvas Twine passage; any `<<goto>>` it produces preempts all body/effects/exit_block content. The table below is the corrected version.

Map of RTS patterns onto TLS engine primitives:

| RTS pattern | TLS engine support | Notes |
|---|---|---|
| **Pattern A** (sequential first-match, independent rolls) | ✅ Native | `setup.checkAndSubstituteCanvas` at v2.py:4597-4626 implements sequential first-match with independent `Math.random()` per rule. Conditions fail → `continue`; dice fail → `continue`; first match returns immediately. Maps 1:1 onto RTS `WashDishes` (§2.2). Verified line-by-line this session. Authoring: order rules by narrative priority. |
| **Pattern B** (single dice partition) | ❌ Not yet supported | No shared-dice / partition logic in `checkAndSubstituteCanvas`. Each rule rolls its own `Math.random()` independently. Authoring approximation (N rules with chance summing < 1) **diverges** from true Pattern B in two ways: (a) cumulative probability — true B = Σcᵢ across mutually-exclusive buckets; approximation = 1 − ∏(1 − cᵢ). For 3 NPCs at "1/6 each," true B = 50% any-fire; approximation ≈ 42%. (b) failed-condition fall-through — true B falls to solo if dice claims slot but conditions fail; engine `continue`s to next rule. See §5.1 for proposed `exclusive_group` extension. |
| **Pattern C** (post-activity event check) | ❌ Not yet supported | Engine emits substitution check as the FIRST content in canvas Twine passage (v2.py:11020-11053; comment in source: "PRD 25 — fires before any other passage logic"). If it preempts via `<<goto>>`, all subsequent canvas body content + body-level effects + exit_block effects are skipped. RTS Pattern C does the OPPOSITE — solo-body unconditional effects (`<<AddFit>>`) run BEFORE the NPC-event-check at the bottom of the passage. Order is reversed; Pattern C as RTS implements it is **not achievable via authoring placement alone**. Workaround: duplicate the unconditional effect on every substitution target (mechanically equivalent, authoring-duplicated). See §5.2 for proposed `pre_substitution_effects` extension. |
| **`IsNpcAtHome` (loose)** | ✅ Predicate via `requires_npc` + house location | Use `requires_npc = "npc_frank"` with NPC schedule covering "house" as a meta-location. |
| **`GetNpcLocation == "X"` (strict)** | ✅ Native | `requires_npc` on canvas trigger + NPC's schedule resolving to that location at current time. |
| **`executedToday` flag** | ✅ Native | `max_triggers_per_day = 1` on canvas trigger. |
| **`previous() != "X"` guard** | ⚠️ Approximation | Not directly supported. Can approximate via flag-set on canvas exit + flag-clear on day rollover (via `[engine.daily_tick].traitEffects`). Most cases don't need this guard if `max_triggers_per_day` is set. |

### §5.1 — Future engine extension for Pattern B (`exclusive_group`) — NOT SHIPPED

If Pattern B (dice partition) becomes load-bearing in slice authoring, extend `TemplateTrigger.substitutions` schema with an `exclusive_group` field:

```toml
[[canvases.trigger.substitutions]]
target_canvas_id = "scene_frank_kitchen_grope"
chance = 0.17
exclusive_group = "kitchen_walk_in"  # NEW

[[canvases.trigger.substitutions]]
target_canvas_id = "scene_jake_kitchen_grope"
chance = 0.17
exclusive_group = "kitchen_walk_in"  # NEW
```

Engine resolves all rules in the same `exclusive_group` via single dice + partition (per RTS Pattern B). Critical behavior to preserve: failed-condition inside a claimed slot falls through to the implicit-solo branch, NOT to the next rule (that's what differentiates Pattern B from Pattern A). Estimated implementation: ~1 hour engine work in `checkAndSubstituteCanvas` + 3-4 unit tests covering the partition + fall-through semantics. **Defer until needed** per Doc 56 §9 doctrine ("build engine when an authoring gap forces it"). For slice phase, Pattern A is the only natively-supported pattern.

### §5.2 — Future engine extension for Pattern C (`pre_substitution_effects`) — NOT SHIPPED

If Pattern C (activity-counts-when-interrupted) becomes load-bearing in slice authoring, extend `TemplateTrigger` schema with a new field:

```toml
[canvases.trigger]
# ... existing fields ...

# NEW — effects that apply BEFORE the substitution check.
# Run unconditionally whenever this canvas is reached, even if a
# substitution rule preempts via <<goto>>. RTS Pattern C analog:
# Exercise's <<AddFit>> runs before the EVENTS block's <<goto>>.
[[canvases.trigger.pre_substitution_effects]]
type = "trait"
subject = "player"
trait_key = "fit"
op = "add"
value = 1
```

Engine emitter (v2.py:11020-11053) would emit these effects BEFORE the substitution check in the passage header, so they execute even when `<<goto _sub_target>>` preempts the rest of the body. Estimated implementation: ~30 min engine work + 2-3 unit tests covering: (a) effect applies on solo branch; (b) effect applies on substitution-preempt branch; (c) ordering relative to canvas-body effects.

**Workaround for slice phase (until extension lands):** duplicate the unconditional effect on every substitution target's effect list. If `activity_exercise` should grant +Fit always, author +Fit on `activity_exercise`'s exit_block (solo path) AND on `scene_grandpa_exercise_sex`'s effects (substitution path). Mechanically equivalent — player always gets +Fit — at the cost of authoring duplication. Document the duplication in the substitution target's canvas description so it survives future maintenance.

Defer until needed per Doc 56 §9 doctrine. When Pattern C arises and LO scopes the engine work, this section becomes the spec.

---

## §6 — Rules (R1–R7)

### R1 — Solo activity is a separate canvas, not a sub-block

Every Maya-solo activity (`activity_make_tea`, `activity_wash_dishes`, `activity_shower`, `activity_study`, `activity_nap`) is its own `[[canvases]]` entry. Each has:

- `trigger_mode = "manual"` (player clicks button to enter)
- `is_repeatable = true` (chore can repeat)
- `location = "loc_X"` (anchors to a hub canvas)
- `schedules = [...]` (time-of-day availability)

*Why:* the dispatcher mechanism requires a named, addressable canvas to attach substitution rules to. Inline activity bodies in a hub menu can't carry substitutions.

*How to apply:* before authoring substitutions for NPCs at a location, audit whether the parent activity exists as a canvas. If not, author it first.

### R2 — Stat costs land on the activity exit_block by default; outside it when "unconditional"

Two placements for stat-effect macros:

1. **Inside exit_block effects** — applies only when player returns from solo branch. Use for cost-per-completion activities (washing dishes, masturbating; the activity costs energy only if Maya finishes it).
2. **Outside exit_block, in canvas body effects** — applies unconditionally on canvas entry, including substitution-preempted runs. Use for activities with unconditional outcomes (exercise = +Fit even if interrupted; sleep = energy restore even if Dad scene fires).

*Why:* RTS shows both placements (WashDishes vs Exercise §2.2 / §2.4). The design call is whether the activity "counts" when interrupted.

*How to apply:* for each new solo activity, ask: "If NPC walks in mid-activity, did Maya complete the chore?" If no → costs inside exit_block. If yes → costs outside.

### R3 — Menu-level gating for time-of-day + energy + purchase + quest state

All four gates live on the LOCATION canvas's button (the exit_block.choices `conditions`), not on the activity canvas itself. The dispatcher trusts the menu's gating.

*Why:* if the dispatcher double-gates, the button would render then route to a passage that bails — wastes a click and breaks the menu surface.

*How to apply:*
- `loc_kitchen` button "Wash dishes 🫧" has `conditions = [time-of-day check, energy check]`
- `activity_wash_dishes` canvas itself has no time-of-day / energy gates in its trigger
- NPC stage / corruption / presence remain in dispatcher (substitution rule conditions), per §3.4 table

### R4 — Multi-NPC competition defaults to Pattern A (sequential first-match)

When 2+ NPCs could walk in on the same solo activity, default authoring is Pattern A:
- Each NPC gets its own `[[canvases.trigger.substitutions]]` rule
- Rules ordered by narrative priority (closer-arc NPC first, OR escalation-NPC first, OR family/ambient NPC first if mixed with peer/dating)
- Each rule has its own `chance` and `conditions`

*Why:* Pattern A maps directly to TLS engine support; sequential first-match is what `checkAndSubstituteCanvas` already does.

*How to apply:* if the slice's family-ambient NPC (Frank) shares a chore location with the slow-burn-family NPC (Jake), order Frank's substitution rule first.

### R5 — Pattern B (dice partition) only when scenes are inherently mutually exclusive

Use Pattern B when the design REQUIRES mutual exclusion — typically multiple variants of the same NPC at the same activity (e.g., Brother grope vs Brother help-study at the study desk; one fires).

Don't use Pattern B for "any NPC could walk in" — that's Pattern A.

*Why:* Pattern B requires either engine-level partition support (Doc 67 §5.1 extension) or approximation via summed chance values. Both have costs. Pattern A is the cheap default.

*How to apply:* in the design brief (R7 per Doc 56), declare whether any activity needs Pattern B. If yes, either commit to the engine extension or document the approximation strategy.

**Engine status (2026-05-26):** Pattern B is **NOT YET ENGINE-SUPPORTED**. The current engine (`setup.checkAndSubstituteCanvas` at v2.py:4597-4626) evaluates each substitution rule's dice independently — there is no shared-dice / partition logic. If Pattern B intent arises during authoring, EITHER defer the authoring until §5.1's `exclusive_group` extension ships, OR accept Pattern A approximation knowing the math + fall-through divergence documented in §4.2 vs §4.4 + §5. **Don't write Pattern B authoring as if it works natively** — the silent divergence will produce wrong probabilities + wrong fall-through behavior, neither of which surface as build errors.

### R6 — `IsNpcAtHome` for Lane 3 walk-ins; `GetNpcLocation == "Loc"` for Lane 2 entry-encounters

Direction of the walk-in determines the predicate:
- NPC walks in on Maya (Lane 3) → `IsNpcAtHome` equivalent (NPC at any home location)
- Maya walks in on NPC (Lane 2) → `GetNpcLocation == "Loc"` equivalent (NPC at exact location)

*Why:* RTS source shows the asymmetry consistently. Tightening Lane 3 to "NPC must already be in kitchen" breaks the fictional intent ("Frank wandered into the kitchen because Maya was there").

*How to apply:*
- Lane 3 substitution rule conditions: `requires_npc = "npc_frank"` with Frank's schedule resolving to "house" (any home location)
- Lane 2 location-entry canvas conditions: `requires_npc = "npc_frank"` with Frank's schedule resolving to the specific room

### R7 — Per-day cap on each substitution target via `max_triggers_per_day = 1`

Every Lane 3 substitution target canvas has `is_repeatable = true` (the scene CAN refire on subsequent days) AND `max_triggers_per_day = 1` (won't refire same day).

Optionally, the parent activity's `[[canvases.trigger]]` has its own `max_triggers_per_day` to cap the chore itself (Maya can wash dishes 3 times today, but Frank's kitchen-dishes scene fires at most once).

*Why:* RTS uses `executedToday` per-scene (§3.6). Once-per-day is the felt cadence — the world has rhythm.

*How to apply:* every substitution target ships with `max_triggers_per_day = 1`. Don't omit unless the design specifically requires multi-fire-per-day (rare).

---

## §7 — Authoring template for a new solo activity

Copy-paste starting point. Substitute slot names + content per arc.

```toml
# ============================================================
# Step 1: location hub renders the activity menu button
# ============================================================
[[canvases]]
id = "loc_kitchen"
# ... (existing location hub) ...

[canvases.exit_block]
type = "choices"

[[canvases.exit_block.choices]]
text = "Wash dishes 🫧"
target_type = "trigger"
target = "activity_wash_dishes"
# Gating per R3 — time-of-day + energy live here
conditions = { items = [
  { type = "trait", subject = "player", trait_key = "energy", op = "gt", value = 0 },
  { type = "trait", subject = "player", trait_key = "time", op = "lt", value = 23 },  # not late-night
] }
# Soft-fail with threshold publish per Doc 56 P2 (transparent gating)
show_when_locked = true
locked_text = "Too tired to wash dishes — sleep first"


# ============================================================
# Step 2: activity (dispatcher) canvas
# ============================================================
[[canvases]]
id = "activity_wash_dishes"
name = "Wash dishes"
description = "Solo Maya activity. Hosts Frank + Jake Lane 3 substitutions."
guide = "Wash dishes in the kitchen while Frank or Jake is home"  # Doc 56 R5

[canvases.trigger]
location = "loc_kitchen"
trigger_mode = "manual"
is_repeatable = true
max_triggers_per_day = 3  # Maya can wash dishes 3x/day; substitutions cap per R7
schedules = [
  { weekdays = [0,1,2,3,4,5,6], start_time = "07:00", end_time = "21:00" }
]

# ----- Pattern A multi-NPC substitution rules -----
# Frank first (family/ambient — closer arc focus in slice)
[[canvases.trigger.substitutions]]
target_canvas_id = "scene_frank_kitchen_dishes"
chance = 0.33
conditions = { items = [
  { type = "trait", subject = "npc", npc_id = "npc_frank", trait_key = "stage", op = "gte", value = 2 },
  # IsNpcAtHome equivalent: Frank's schedule must resolve to a home location
  # (this is handled at the substitution target's own trigger via requires_npc)
] }

# Jake second (slow-burn family — secondary)
[[canvases.trigger.substitutions]]
target_canvas_id = "scene_jake_kitchen_dishes"
chance = 0.33
conditions = { items = [
  { type = "trait", subject = "npc", npc_id = "npc_jake", trait_key = "stage", op = "gte", value = 2 },
] }

# Solo body (R2 — costs inside exit_block since Maya can be interrupted)
[[canvases.nodes]]
type = "paragraph"
content = "You stack the plates, run the water warm. Soap smells like lemons."
[[canvases.nodes]]
type = "image"
file = "scenes/kitchen/dishes_solo.jpg"

[canvases.exit_block]
type = "location"
target = "loc_kitchen"
effects = [
  { type = "trait", subject = "player", trait_key = "energy", op = "sub", value = 10 },
  { type = "trait", subject = "player", trait_key = "time", op = "add", value = 1 },
]


# ============================================================
# Step 3: substitution target (Frank's walk-in scene)
# ============================================================
[[canvases]]
id = "scene_frank_kitchen_dishes"
name = "Frank in the kitchen — dishes"
guide = "Wash dishes in the kitchen while Frank is home (Stage 2+)"

[canvases.trigger]
location = "loc_kitchen"
trigger_mode = "manual"
is_repeatable = true
max_triggers_per_day = 1  # R7 per-day cap
substitution_only = true  # not directly clickable; only via parent dispatcher
requires_npc = "npc_frank"  # R6 — engine resolves Frank's schedule
schedules = [{ weekdays = [0,1,2,3,4,5,6], start_time = "07:00", end_time = "21:00" }]

# ... (scene body per Doc 30 §7.1 prose rules) ...
```

---

## §8 — Pre-authoring checklist

Before adding a new solo activity to a slice:

**Solo activity itself:**
- [ ] **R1** — separate canvas with `trigger_mode = "manual"` + `is_repeatable = true`
- [ ] **R2** — stat costs placement decided (inside exit_block = costs only if completed; outside = costs always)
- [ ] **R3** — menu-level gates (time-of-day, energy, purchase, quest) on location button's choice conditions; NOT in dispatcher
- [ ] **Doc 56 R5** — `guide` field present (e.g. "Wash dishes in the kitchen while Frank is home")

**For each substitution rule:**
- [ ] **R4** — Pattern A default (sequential first-match); rule order = narrative priority
- [ ] **R5** — Pattern B only if mutually-exclusive variants by design; declared in NPC brief
- [ ] **R6** — `requires_npc` on target canvas with appropriate schedule (loose for Lane 3 walk-ins; strict for Lane 2 entry-encounters)
- [ ] **R7** — target canvas has `max_triggers_per_day = 1`
- [ ] Doc 56 R3 — substitution count per NPC respects per-arc-shape Lane 3 budget (family 4–7, slow-burn 1–3, peer 0, service 0, antagonist 0 own)

**Cross-rule consistency:**
- [ ] If two NPCs share a dispatcher, schedules don't trivially overlap them in same shared space during slice phase (avoids surprises until Pattern B / partition support lands)
- [ ] Each substitution target is `substitution_only = true` (not clickable as standalone canvas)
- [ ] Each substitution target's prose register matches the lane (RTS-flat per Doc 30 §7.1; not Tier-3 literary)

---

## §9 — Anti-patterns

Concrete shapes to NOT ship.

- **Solo activity body inline in the location hub.** Conflates menu + dispatcher. Makes substitution authoring impossible. Caught by R1.

- **Time-of-day gate on the dispatcher.** Button still renders, click routes to dispatcher, dispatcher bails. Wasted click. Caught by R3.

- **Multi-NPC substitution rules with no clear priority order.** Sequential first-match means first rule has structural advantage. If author doesn't name the priority, drift happens silently. Caught by R4 + the NPC design brief (Doc 56 R7).

- **Pattern B authored as multiple Pattern A rules with chance values summing to < 1.** This is the approximation noted in §5. It's not mutual-exclusion-correct (cumulative chance ≈ 1 − ∏(1 − cᵢ), not Σcᵢ). Acceptable in slice phase if Pattern B is rare; document the approximation. Caught by R5.

- **Stat cost in wrong placement for the activity's design intent.** If Exercise costs Energy only in the ELSE branch, the workout doesn't "count" when Grandpa walks in — but the design SAYS it should (Pattern C uses outside-ReturnButton placement for this reason). Caught by R2.

- **`GetNpcLocation == "Kitchen"` on a Lane 3 walk-in dispatcher.** Too strict; NPC has to already be in the kitchen. Use loose check (`requires_npc` with NPC's schedule resolving to "house" or equivalent meta-location). Caught by R6.

- **No `max_triggers_per_day` on substitution target.** Same scene firing 5 times in one day breaks the "once per day" cadence RTS uses. Caught by R7.

- **Substitution target not marked `substitution_only`.** Then it appears in the NPC portrait hub at the location, the player can click it directly — defeating the "you were doing X and he happened" fictional intent. Caught in pre-ship checklist.

- **Solo activity authoring without checking the per-arc-shape Lane 3 budget.** Authoring 7 Frank substitutions when slice scope is 3 is drift. Caught by Doc 56 R3.

- **Authoring against Pattern B or Pattern C assuming engine support.** Current engine natively supports Pattern A only (per §5). Writing substitution rules expecting Pattern B's shared-dice partition or Pattern C's unconditional-effects-before-interrupt will silently produce wrong behavior — Pattern B probabilities diverge (~42% vs 50% for 3-NPC at "1/6 each") and failed-condition behavior fall-through wrong; Pattern C effects never apply when substitution fires. **No build error fires for either case.** Use Pattern A and surface the case to LO if Pattern B/C is genuinely needed; engine extension lands first (§5.1 / §5.2).

---

## §10 — Open questions / scoped-out

Things this doc deliberately does NOT cover. Each is its own future PRD if it becomes load-bearing:

- **Pattern B engine support (the `exclusive_group` field).** Spec'd in §5.1; defer per Doc 56 §9 doctrine. Not blocking for slice authoring.

- **Dynamic priority on substitution rules** (e.g., "fire the NPC whose trust is highest first"). RTS uses static rule order. TLS could evaluate priority via condition expressions, but this is engine work and authoring complexity. Not surfaced as a need yet.

- **Activity-side walkthrough catalog rendering.** RTS Walkthrough lists scenes per NPC; doesn't show "all activities → which NPC walks in" inverted view. The catalog surface (Doc 56 P2 + Doc 62 `guide` field) is per-canvas; activity-side rollup is post-MVP polish.

- **Schedule overlap guardrails.** If Frank AND Jake are both scheduled in kitchen at 8am, both substitution rules can fire (Pattern A) but probability stacks weirdly. No engine guardrail. Authoring rule (R4-adjacent): keep schedules non-overlapping for distinct NPCs in shared spaces during slice phase.

- **Cross-NPC bridge scenes (RTS `SellingMyStepsister`).** Brother conditions trigger a scene that transfers arc to Josh. This is NOT a Lane 3 dispatcher — it's a Lane 4 capstone with cross-NPC effects (Doc 57 Pattern B branching). Mentioned here for completeness; covered in Doc 57.

- **`previous()` guard implementation in TLS.** Approximation noted in §5; native support is engine work. Defer until a slice case requires it (no current case).

- **Lane 2 EVENTS-block design from the location-hub side.** This doc focused on Lane 3 (dispatcher inside activity). Lane 2 location-entry events (§4.5) get a passing mention but a deeper Lane 2 authoring doc would extend Doc 24 §6.

---

## §11 — Cross-references

### Redesign docs (this folder)
- **Doc 24** — 3 Lanes for Repeatable NPC Content (the lane mechanism; this doc extends Lane 3 with the dispatcher passage anatomy)
- **Doc 25** — Lane 3 Dispatcher Substitution PRD (engine spec for `substitutions` list + `substitution_only`)
- **Doc 30 §7.1** — RTS-flat prose rules (apply to all substitution target prose)
- **Doc 50** — Quest Card Shape Doctrine (R6 — `txt_only` cards)
- **Doc 56** — RTS Principles + Alignment Doctrine (R3 per-shape Lane 3 budget; P1–P10 evidence)
- **Doc 56 R5** — Canvas `guide` field (every solo activity + every substitution target needs one)
- **Doc 57** — Capstone Doctrine / Lane 4 (referenced for cross-NPC bridge pattern in §10 open questions)
- **Doc 62** — Canvas `guide` Field PRD (not yet implemented; this doc's templates assume eventual support)
- **Doc 66** — Session Record / Prompts Rewrite Pivot (this doc is the closure of the Doc 66 §15.2 surfaced gap)

### RTS source artifacts (live extraction this session)
- `game_explorations/rts-arc-trace/passage_catalog.json` — 9 passage bodies pulled verbatim (BathroomShowerMasturbate, WashDishes, BedroomStudy, BedroomSleep, Exercise, PlayingVideogame, BathroomShower, Bathroom, Bedroom, Kitchen)
- `game_explorations/rts-arc-trace/notes.md` — 8 timestamped observation blocks from May 2026 RTS exploration
- `game_explorations/rts-arc-trace/synthesis_repeatable_narrative_auto_2026-05-10.md` — live-verified Shower Sex dispatcher chain

### Engine primitives referenced
- `checkAndSubstituteCanvas` — `apps/game_generation/twee_comprehensive/generators/v2.py:4597` (sequential first-match implementation; Pattern A native support)
- `selectAutoFireCanvasForLocation` — v2.py:3839 (related, for Lane 2)
- `getNpcLocation` — v2.py:2898 (strict NPC location check)
- `TemplateTrigger.substitutions` — `apps/projects/services/template_import.py:1266-1280` (substitution rule schema)
- `TemplateTrigger.substitution_only` — same (marker flag for substitution targets)
- `TemplateTrigger.max_triggers_per_day` — template_import.py (per-canvas per-day cap)

---

## §12 — Confidence ladder

Per Doc 24 methodology (source extraction + live play, never one alone):

✅ **HIGH confidence (source-verified this session):**
- The 3 multi-NPC patterns (A sequential / B partition / C post-activity) — direct extraction from RTS source
- `WashDishes` Pattern A mechanism — full passage body in §2.2
- `BedroomStudy` Pattern B mechanism — full passage body in §2.3
- `Exercise` / `PlayingVideogame` Pattern C mechanism — full bodies in §2.4 / §2.6
- `IsNpcAtHome` vs `GetNpcLocation` semantic distinction — verified by cross-referencing 5 dispatcher bodies
- Per-day cap via `executedToday` — verified in `Bathroom` events block §2.7
- `previous()` guard pattern — verified in `BedroomSleep` §2.5
- Menu-level gating placement (location button, not dispatcher) — verified in `Bathroom` and `Bedroom` menu bodies
- Stat cost placement variance (inside vs outside ReturnButton) — verified by comparing WashDishes (inside) vs Exercise (outside)
- Lane 2 vs Lane 3 lane assignment based on walk-in direction — inferred from `BathroomShowerMasturbate` (Brother, Lane 3) vs `Bathroom` events (Dad/Grandpa, Lane 2)

🟡 **MED confidence:**
- Selection rule between Patterns A/B/C (§4.4) — inferred from observed usage; no single deterministic rule in source. Doctrine call by ENI based on patterns.
- Probability math (§4.1, §4.2) — math is correct given the source; not verified by playthrough sampling

✅ **HIGH confidence (verified this session) — engine support for Pattern A:**
- `setup.checkAndSubstituteCanvas` at v2.py:4597-4626 implements sequential first-match with independent `Math.random()` per rule. Conditions fail → `continue`; dice fail → `continue`; first match returns. Maps 1:1 onto RTS Pattern A. Line-by-line verified.

❌ **NOT YET SUPPORTED (verified this session) — engine support for Patterns B + C:**
- **Pattern B:** no shared-dice / partition logic in `checkAndSubstituteCanvas`. Each rule rolls own dice independently. Authoring approximation diverges from true Pattern B in both probability math (P(any) = 1−∏(1−cᵢ) vs Σcᵢ; ~42% vs 50% for 3-NPC) AND failed-condition fall-through (engine `continue`s; true B falls to solo).
- **Pattern C:** substitution check emitted FIRST in canvas Twine passage (v2.py:11020-11053; source comment confirms "PRD 25 — fires before any other passage logic"). If preempts via `<<goto>>`, all body + body-level effects + exit_block effects skip. RTS Pattern C runs solo-body effects BEFORE NPC interrupt; engine reverses this order. Pattern C as RTS implements it is structurally impossible via authoring placement alone in the current engine.
- **Audit trail:** Doc 67's initial §5 table claimed Pattern C was "✅ Native via authoring" and Pattern B was "⚠️ Approximation only." Both were wrong. §5 has been corrected (this session, 2026-05-26). §5.1 + §5.2 document the future engine extensions; both deferred per Doc 56 §9 doctrine.

❌ **NOT established this session:**
- Whether RTS uses Pattern B for any other dispatcher beyond `BedroomStudy` — only one example found in 2464-passage catalog grep
- Whether the cumulative Pattern A probability "feels right" in playtest (math says ~55% any-NPC for 2-NPC dispatcher with 1/3 each; not playtested for TLS feel calibration)
- Whether `previous()` guard is ever needed in TLS slice (no current case where same-canvas re-fire is a problem)
- Whether multi-NPC schedule overlap (Frank + Jake both in kitchen at 8am) actually causes observable issues in playtest, or if Pattern A handles it gracefully

---

## §13 — Doc 66 §15.2 closure

This doc closes the gap surfaced in Doc 66 §15.2 ("Known doctrine gap — solo activity design + multi-NPC dispatcher competition not yet covered"). Recommend Doc 66 §15.1 boot order be updated to include Doc 67 in the mechanism quartet (Doc 24 + Doc 57 + Doc 50 + Doc 67). See follow-up edit to Doc 66.

---

**End of Doc 67.**
