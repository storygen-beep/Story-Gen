# 18 — Frank Arc Redesign (RTS-aligned content / choices / register)

> **Status:** Design spec, not implementation. Authored 2026-05-04 after the Frank pilot live-playtest (notes in `game_explorations/tls-frank-pilot/`) + a focused two-pass RTS exploration session (`game_explorations/rts-discovery-trace/synthesis.md`) revealed three structural gaps in Frank's arc. This doc is an **overlay** on doc 16's 12-scene library — it does not replace doc 16, it specifies what changes in mechanics + choice distribution + register on top of those scenes. Implementation comes in separate plans, ordered per §9.

---

## §1 Purpose & relationship to doc 16

Doc 16 is the **scene library spec** — what scenes exist, what voice Frank speaks in, what tier each scene targets. Its locked decisions (D1-D3 in §1) stay locked here:

- **D1** (RTS-flat default + Tier-3 carve-out for named-NPC introductions / stage-flag capstones / crisis moments) — **PRESERVED**. This redesign uses the carve-out to add 3 more T3 beats for Frank, all of which fall under the existing carve-out categories.
- **D2** (existing 4 Frank scenes = polish, not full rewrite) — **PRESERVED**. The redesign augments existing scenes with new branches and choice variants; it does not rewrite the existing Stage 0/1/2 register prose.
- **D3** (Stage 3→4 deferred) — ⚠️ **SUPERSEDED 2026-05-04 by `19_Frank_Stage_3_Plus_Design.md` §1.** D3 was a slice-budget call (10-day window), not a design-call against Stage 4. With slice scope reframed, doc 19 now specifies Stage 3→4 as a single capstone (bedroom invitation, branch-inside-shell at `scene_office_after_crack`) plus Stage 4 register cascade + `scene_franks_bedroom_evening` T3 anchor — **all shipped in `7_final_game.toml` as of 2026-05-04**. ~~PRESERVED. This redesign covers Stage 0-3 only. Stage 4 cracked-summons content stays out per doc 16.~~

Doc 18 is the **arc redesign overlay**. Three threads:

1. **Content unlock pattern** — bookkeeping (Stage 0→1) and chores (post-catch) get proper RTS-shaped narrative introductions instead of appearing from nowhere.
2. **Choice distribution** — the per-NPC opaque counters (`frank_tease_count`, `frank_chore_count`, `frank_bookkeeping_count`) retire. Tease and chore behaviors distribute across many ambient scenes feeding global stats; gates use cumulative state.
3. **Register escalation** — Stage 2-3 prose moves to the explicit register the mechanics are gating toward, matching RTS PeepBrotherSex / sex-scene shape rather than the current PG-13 hedge.

These three threads reinforce each other. Introduction creates fictional justification for activities; multi-source choices make stat accumulation feel earned; explicit register at Stage 3 makes reaching the gate land as consequence rather than pornography. This is one redesign, not three separate changes.

**Scope:** Frank only. Ryan and Jake are explicitly out — they get their own arc redesigns later, on the same template. Stage 0-3. Slice timeframe (10 days).

---

## §2 RTS pattern reference (concrete, evidence-grounded)

The redesign is grounded in three specific findings from the RTS discovery session. Citations are to `28th_april_TLS_Phase2_Redesign/13_Road_to_Success_Reference.md` and `game_explorations/rts-discovery-trace/`.

### Content unlock pattern — verified live

Doc 13 §12 bootstrap log, turns 28-30 (lines 543-545):

> 28. Eval `handleSubLocation('Library')` → Library: *"There is a girl at the reading tables, lost in a book. You keep seeing her in the halls. Kind of weird you never said hi. Could fix that now."* + [Say hello]
> 29. Click `Say hello 📚` → **🎯 Tier-3 scripted intro: Natasha** — scripted dialogue, speaker label changes "Student" → "Natasha" once names exchanged
> 30. Read scene + return → "Don't be a stranger. I'm here most days." → (per-NPC chat now unlocked)

This is the canonical three-beat: **location prose calls out the new affordance → single choice fires Tier-3 scripted intro → recurring activity unlocks silently after**. The Library room doesn't sit empty until Natasha appears as a button. The room narration explicitly nudges the player toward the intro (*"Could fix that now"*). After the intro, subsequent Library visits drop into normal Library content.

This is what bookkeeping needs. It already had the dialogue ("you any good with numbers?" exists in `scene_kitchen_with_frank_morning` Stage-1 register) but lost its job because bookkeeping was already accessible since Day 1.

### Multi-source stat distribution — verified by source grep

361-passage catalog walked for stat-mutation widget usage:

| Stat | Distinct passages incrementing it |
|---|---|
| `<<AddCor>>` (player corruption) | **18 different scenes** — BedroomGrope, DiscountSex, ClubGloryHole, CarWashChallenge, BeachChallenge1, ParkChallenge, LibraryExhibitionism, PublicExhibitionism, PayingRent1, StreetChallenge1 + more |
| `<<AddExb>>` (player exhibitionism) | **27 different scenes** |
| `<<AddBrotherCorruption>>` (NPC stat) | **6 different scenes** — BrotherShowerSex (×2), BedroomGrope, BedroomStudyBrotherGrope, BrotherBedroomFlash, BrotherBedroomTease |
| `<<linkreplace>>` (drip primitive) | **1559 occurrences** across 361 passages |

RTS uses no per-NPC opaque counters for "actions of type X." Brother's arc uses HIS corruption + HIS arousal + global player corruption — all fed from many parallel sources. There's no `brother_grope_count` or `brother_tease_count`. The stage-tier escalation is purely cumulative stats.

### Explicit register at climax — verified by playthrough

PeepBrotherSex was played to completion in Pass 2 (synthesis.md §"Linkreplace-drip pattern"). Four-step linkreplace within a single passage:

1. Peep → opening paragraph + image. Choice: Peep / Hallway.
2. Click Peep → adds *"Heat flares in your belly..."* + new video URL + choice [Stroke your pussy].
3. Click Stroke → adds *"You can't help yourself. You slip your hand under your shorts..."* + video swap + choice [Masturbate].
4. Click Masturbate → adds *"You're so turned on, you can't stand it anymore. You pull up your shirt, exposing your aching breasts..."* + choice [Cum!].
5. Click Cum! → climax paragraph + writes `npc.Brother.scenes.PeepBrotherSex.unlocked = true`, `player.corruption.points +1`, `player.arousal -1`, exit to Hallway.

Direct anatomical language. Per-step consent (Hallway exit always present). Climax writes scene-completion + small global stat changes. This is the register that the TLS Frank arc's "Stage 3 tease + Stage 3-4 sex" gates target. We've been authoring at PG-13 register for content meant to land at this register.

---

## §3 Stage 0→1 redesign — bookkeeping introduction

### Current broken shape

| Element | Current state |
|---|---|
| `activity_bookkeeping_with_frank` | Available Day 1, no flag-gate, just location + schedule + npc trigger |
| `frank_stage_1` helper | `trust >= 15 + bookkeeping_count >= 3` (chicken/egg — can't gain bookkeeping_count if activity weren't already accessible) |
| Stage-1 dialogue ("you any good with numbers?") | Exists in `scene_kitchen_with_frank_morning` Stage-1 branch, but fires AFTER stage 1 already cleared — the offer prose has no gating function |

The bookkeeping appeared from nowhere because the offer scene got disconnected from the activity gate. Doc 02 §line 112 already specified this should be a Stage-1 branch that sets a flag; the implementation skipped it.

### Redesigned shape

**Day 1-5: Stage 0 ambient surface.** Player gets:
- `scene_kitchen_with_frank_morning` Stage-0 register (existing — unchanged)
- `scene_kitchen_with_frank_dinprep` Stage-0 register (existing — unchanged)
- New ambient scenes #5-#8 from doc 16 (hallway pass, kitchen coffee alone, living room radio, porch evening smoke) at Stage-0 register
- Trust accrues from these scenes — currently `+1` per attendance via the existing scene effects

**Trust threshold lowered from 15 → 10.** With bookkeeping_count gone from the helper, trust is the only mechanical gate. 10 is reachable in 5-6 days at +1/day cadence (kitchen + 1-2 ambient scenes per day).

**New Stage-0→1 transition branch in `scene_kitchen_with_frank_morning`.** High-priority `group` block, gated on:
- `npc_frank.trust >= 10`
- `frank_offered_bookkeeping is_false` (one-time guard)
- Stage 0 register (so it fires during the existing morning visit, not as a separate canvas)

This is the offer beat — Tier-3 scripted, ~200 words. Sample prose in Frank's voice per doc 16 §2:

```
KITCHEN — MORNING

She comes in for coffee. Frank's already at the table. Not eating —
he's done eating. Receipts. Three short stacks she hadn't noticed
on the prior mornings, set out the way you'd set a hand of cards.
He's looking at the top one of the middle stack and not turning it.

Frank: "You eat?"

She nods.

Frank: "Sit a minute."

She sits. He doesn't push the receipts toward her, just lets them
stay where they are between them. Like they're a thing he hasn't
decided about yet either.

Frank: "You any good with numbers?"

The way he says it — not a job interview, not a casual question.
Like he's already been thinking about it for a few mornings and
finally said it out loud.

She looks at the stacks.

  [Yeah. I can help.]
  [I'm not really…]
```

**Accept choice effects:**
- `frank_offered_bookkeeping = true` (flag — opens activity at office)
- `npc_frank.trust += 2` (small bump — agreeing was the right answer for him)
- Frank line follows: *"Eight bucks a session. Office. Evenings. Don't be late."*
- Player exit text confirms acceptance, time +15 min

**Decline choice effects:**
- `frank_declined_bookkeeping_today = true` (daily-reset flag)
- Frank line: *"Suit yourself."* + brief continuation of morning, no trust change
- Offer comes back next day's morning visit

**Activity gate:** `activity_bookkeeping_with_frank` trigger conditions add `frank_offered_bookkeeping is_true`. Until the player accepts the offer, the activity does not appear in the office (the office stays empty / only shows `activity_talk_to_frank` at Stage 0).

**Helper rewrite:** `frank_stage_1` becomes:

```toml
[[engine.stage_helpers]]
name = "frank_stage_1"
description = "Frank Stage 0→1 — bookkeeping accepted. Trust threshold + offer accepted flag."
conditions = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "npc",    npc_id = "npc_frank", trait_key = "trust",                  operator = "gte", value = 10 },
  { type = "flag",  subject = "player",                       flag_key  = "frank_offered_bookkeeping", operator = "is_true" },
] }
```

The offer scene IS the gate. Bookkeeping_count drops out entirely. The narrative beat (offer + accept) is what moves the stage forward.

---

## §4 Stage 1→2 redesign — catch + post-catch context

### What's already correct (no changes)

`scene_living_room_evening` (the catch) is the doctrinal poster child — Tier-3 polished per doc 16 §8, branch-inside-shell, writes `frank_caught + frank_restrict_declared + npc_frank_stage = 2` in the same effects block. **Catch scene unchanged.**

### What's missing — post-catch narrative context

After the catch fires and Maya is at Stage 2, two activities currently appear with no fictional setup:
- `activity_morning_chore` (Stage-2+ gated)
- `scene_franks_office_supervised` Stage-2 register (Stage-2+ gated)

Both should have introduction beats explaining the new arrangement, mirroring the bookkeeping pattern.

**Chore offer.** Add Stage-2 branch to `scene_kitchen_with_frank_morning` — Tier-2 vignette, ~80 words, fires once when player visits kitchen at Stage 2 with `frank_offered_chores is_false`:

```
KITCHEN — MORNING (post-catch)

Frank's already at the table when she comes in. Coffee, no paper.
He doesn't look up.

Frank: "Porch needs sweeping."

She stops at the counter.

Frank: "Before you sit. Every morning."

He turns the page he isn't reading.

Frank: "We'll see how that goes."
```

Sets `frank_offered_chores = true`. `activity_morning_chore` trigger adds `frank_offered_chores is_true`. Chore activity now has narrative justification.

**Supervised office context.** Add Tier-3 one-time branch to `scene_franks_office_supervised` — fires the first time player enters the office post-catch (`frank_restrict_declared is_true + frank_supervision_explained is_false`). ~150 words:

```
FRANK'S OFFICE — FIRST EVENING POST-CATCH

The lamp's on. Door's open. Frank at the desk, the receipts in
three stacks now where there used to be one, sorted in some way
she doesn't read yet.

He doesn't look up when she comes in.

Frank: "Door open."

She'd already left it open. He says it anyway.

Frank: "Always. I don't care who's in the house."

He passes her the smaller stack across without looking.

Frank: "Sit. Where I can see you."

The chair he means is the one across from him, lamp between them.
She sits. He goes back to the page he was on. They work an hour
that way and he doesn't speak again.
```

Sets `frank_supervision_explained = true`. The new arrangement is now narratively established; subsequent visits use the existing Stage-2 supervised office register.

---

## §5 Stage 2→3 redesign — multi-source tease + crack moment

### Current broken shape

`frank_stage_3` helper requires:
```
corruption >= 50
+ frank_restrict_declared is_true
+ npc_frank.arousal >= 30
+ frank_tease_count >= 3   ← single-source counter
+ frank_chore_count >= 3   ← single-source counter
```

Both counters are single-source. `frank_tease_count` only increments via the "Lean against the desk" choice in `scene_franks_office_supervised`, which is itself gated on Stage 3+ (verified in current TOML at line 2880-2882 — the choice's `conditions` block requires `npc_frank_stage >= 3`). So tease is unreachable until you're already at Stage 3, which requires tease_count ≥ 3. Circular dependency. Stage 2→3 is mechanically dev-button-only.

### Counter retirement

| Trait | Action | Reason |
|---|---|---|
| `frank_tease_count` | DELETE from `player.core_traits` and every reference | Single-source counter; per-NPC opaque counters violate RTS doctrine |
| `frank_chore_count` | DELETE from `player.core_traits` and every reference | Same — chore_count was an audit fix; better expressed as `npc_frank.trust` increments |
| `frank_bookkeeping_count` | DELETE from `player.core_traits` and every reference | Replaced by `frank_offered_bookkeeping` flag at the gate level |
| `lean_by_desk_count` | KEEP for dev-only verification | Already documented as dev-only counter; no gate references it |
| **`npc_frank_corruption`** | **NEW** per-NPC stat (parallel to `npc_frank.trust` and `npc_frank.arousal`) | Multi-source, RTS-aligned |

### Multi-source tease distribution

Add a "tease" choice variant to **6 ambient/repeating Frank scenes**. Each choice gated on:
- `npc_frank_stage >= 2`
- `frank_restrict_declared is_true`
- `player.corruption >= 30` (matches existing teasing-readiness threshold across the slice)

Each choice produces the same triple effect:
- `npc_frank.arousal += 1`
- `npc_frank_corruption += 1`
- `player.corruption += 1`

| # | Scene | Choice text (sample, terse, RTS-flat for choice surface) | Sample prose register (when chosen) |
|---|---|---|---|
| 1 | `scene_kitchen_with_frank_morning` | "Brush past him at the coffee maker" | Tier-2 vignette ~50 words: she leans across him for the sugar; her hip brushes his arm; he doesn't move; she takes longer than she needs to; she feels his breath catch and pretends she didn't |
| 2 | `scene_kitchen_with_frank_dinprep` | "Reach for a plate above his head" | Tier-2: she stretches up; her shirt rides; his eyes go to the gap of skin and stay there; she lets the reach be slow; he hands her the plate without speaking |
| 3 | `scene_hallway_frank_pass` | "Linger in the doorway in just your robe" | Tier-2: he comes through the hall; she's at the bedroom door; the robe is loose at the top; she doesn't pull it closed; he passes within arm's reach; the look she gets is the look |
| 4 | `scene_living_room_frank_radio` | "Sit on the rug at his feet" | Tier-2: he's in the chair, radio on; she sits on the rug, knees drawn up, her thighs visible; he doesn't change the angle of his head but his hand stops adjusting the dial |
| 5 | `scene_franks_office_supervised` | **"Lean against the desk a moment longer"** (existing choice — preserve as-is, just retag the effect to the new triple) | Existing prose stays |
| 6 | `scene_porch_frank_evening_smoke` | "Sit on the railing where he can see your legs" | Tier-2: he's on the porch chair smoking; she perches on the railing, knees apart by an inch more than necessary; he doesn't ash his cigarette for a long minute |

Six tease sources. At Stage 2 with `frank_restrict_declared`, the player can do 1-2 of these per day in the natural flow. Frank.arousal climbs from 0 (or wherever the catch left it) to 30 in ~5-7 days. Frank.corruption climbs in parallel. Stage 3 gate becomes naturally reachable in the slice timeframe.

### The crack moment — Stage 2→3 transition

NEW Tier-3 scene: **`scene_office_crack`**. Branch-inside-shell at `scene_franks_office_supervised`. One-time guard, fires when:
- `npc_frank_stage == 2`
- `frank_restrict_declared is_true`
- `player.corruption >= 50`
- `npc_frank.arousal >= 30`
- `npc_frank_corruption >= 15`
- `frank_cracked is_false` (one-time guard)

The branch sets `frank_cracked = true + npc_frank_stage = 3` in choice exits. ~300-400 words, in Frank's voice. Sample:

```
FRANK'S OFFICE — EVENING

The lamp's lower than usual. She'd noticed it when she came in.
He'd dimmed it at some point and not raised it back. The receipts
are out but she's not sure he was working — the top page hasn't
been turned in the time she's been here.

She'd sat. He hadn't said sit. He'd just looked up when she came
through the door and looked back down at the page and not said
anything, and she'd sat anyway.

Now her foot is bare. She'd toed her shoe off ten minutes ago.
She'd pretended it was an accident. The shoe is on its side under
the desk. He'd looked at it once.

Frank: "Door."

She looks up.

He's looking at the door. The door behind her. The door that's
been propped open every evening since the catch — propped open
because he said it. Because *door open, always, I don't care who's
in the house.*

Frank: "Close it."

She doesn't move. The lamp light catches her bare foot under the
desk.

Frank: "I told you. Door open."

He sets the pen down. The first thing he's set down all evening.

Frank: "I changed my mind."

  [Get up. Close the door.]
  [Don't move. Make him say it twice.]
```

Both choices set `frank_cracked = true + npc_frank_stage = 3`. The first choice has Frank's voice harden ("good"); the second has him cross the room himself, close the door, come back to the desk and stand over her. Both lead into the new Stage 3 register.

### Helper rewrite

```toml
[[engine.stage_helpers]]
name = "frank_stage_3"
description = "Frank Stage 2→3 — restraint broken. Stat-cumulative gate, no opaque counters."
conditions = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "player",                       trait_key = "corruption",        operator = "gte", value = 50 },
  { type = "flag",  subject = "player",                       flag_key  = "frank_restrict_declared", operator = "is_true" },
  { type = "trait", subject = "npc",    npc_id = "npc_frank", trait_key = "arousal",           operator = "gte", value = 30 },
  { type = "trait", subject = "npc",    npc_id = "npc_frank", trait_key = "npc_frank_corruption", operator = "gte", value = 15 },
] }
```

4-AND, all stat-cumulative, all multi-sourced. No counters.

---

## §6 Stage 3 explicit-register content

D3 (Stage 3→4 deferred) stays in force. But Stage 3 needs at least one playable scene at the explicit register, otherwise the crack moment is a tease without payoff and the stage transition feels arbitrary mechanically.

### Scope cap

**One** Stage-3 explicit scene, repeatable, replaces the current Stage-3 dev-fragment branch in `scene_franks_office_supervised` (`7_final_game.toml:2834-2840`). No additional Stage-3 sex scenes in this slice. Stage 4 cracked content stays out.

### `scene_office_after_crack` — design spec

Repeatable post-crack supervised office variant. Trigger same as existing `scene_franks_office_supervised` plus `frank_cracked is_true`. Stage-3 register replaces the current 2-line dev fragment.

4-step linkreplace drip matching RTS PeepBrotherSex shape. Sample prose at full register, ~700 words, in Frank's voice (terse dialogue, sensory grounding, no academic vocabulary, Maya's interiority as Tier-3 carries the prose weight):

```
FRANK'S OFFICE — EVENING

The door's closed. It stays closed every evening now. Has since
the night he closed it himself — the night the lamp was low and
he set the pen down and changed his mind. She still doesn't know
what changed his mind, only that something did, and the receipts
are still on the desk every evening because the bookkeeping is
still happening, only it's not really bookkeeping anymore and
they both know it.

He's at the desk when she comes in. Page open. Pen in his hand.
Lamp on. Same as before, same as always — only the door's closed
behind her now.

Frank: "Sit."

She sits.

Frank: "Read the column."

The page is the deductibles. She bends over the desk to see, her
hands on the wood, her hair coming forward.

  [Bend a little more than you need to.]
  [Just read the column.]
```

**Choice 1 (tease — drip continues):**

Click → linkreplace adds:

```
She bends. The shirt she chose tonight is the loose one. She
knows what he sees from his angle and she takes a second longer
than the column needs.

His hand finds her hip. He doesn't move it — just sets it there
the way he'd set a glass down. Like he's checking it stays.

Frank: "You wearing anything under that."

It's not a question.

  [Tell him no.]
  [Don't answer.]
```

Click `Tell him no` → linkreplace adds:

```
She doesn't look up from the page.

Maya: "No."

His hand stays where it is for another second. Then it slides up
the back of her thigh, slow, finding the hem of her skirt and
lifting it. He still doesn't look at her — he's looking at the
page she's pretending to read.

Frank: "Keep reading."

The pen is still in his other hand. He hasn't put it down. The
lamp light is steady. Outside the office the house is quiet —
Diana asleep, the hallway dark, the kitchen clock ticking the
way it does at this hour. Inside the office his hand is on her
ass and the skirt is up and she's still bent over the desk and
he hasn't said anything else.

  [Push back against his hand.]
  [Stay still and read.]
```

Click `Push back against his hand` → climax beat:

```
She pushes back. His hand tightens. The pen finally goes down.

She hears the chair scrape — he's standing. Belt. The sound of
the buckle. Then his hands are on both her hips and he's behind
her and there's a moment where she can feel him just there, just
the heat and the weight of him, before he pushes in.

The desk takes her weight. The page she was reading slides
sideways. She braces her forearms on the wood and lets her head
drop forward and lets him have it the way he wants it — slow at
first, then not slow, his hand bracing her hip, his other hand
flat against her lower back like he's pressing her down into the
desk.

Frank: "Quiet."

She bites the inside of her cheek. The desk creaks once. The
lamp doesn't move. He doesn't speak again until he's close —

Frank: "Keep still."

— and then he holds her hip hard, pulls her back into him once,
twice, and finishes. He stays like that for a long second after,
his hand still flat against her back, his breathing slow.

Then he pulls out. She hears the rustle of him fixing his belt.
She doesn't move from the desk.

Frank: "Wipe yourself off. Receipts for tomorrow are in the
middle stack."

He sits back down.

  [Hallway 🚪]
```

**Choice 2 (read straight) at any drip step:** falls through to the existing Stage-2 register beat ("Run the deductibles." choice equivalent). No stat changes beyond normal supervised-office. Player can attempt the Stage-3 scene without going through to climax — they get a shorter version that still progresses the stage's lower-tier content. Matches RTS's "fall-through alt content for partial commitment" pattern.

### Climax effects (terminal Cum click)

```toml
effects = [
  { targetType = "player",                       trait = "corruption",         op = "add", value = 2 },
  { targetType = "npc",    npcId = "npc_frank", trait = "arousal",            op = "add", value = -3 },
  { targetType = "npc",    npcId = "npc_frank", trait = "npc_frank_corruption", op = "add", value = 2 },
  { targetType = "player",                       trait = "money",              op = "add", value = 8 },
  { targetType = "player",                       trait = "energy",             op = "add", value = -10 },
]
flagEffects = [
  { targetType = "player", flag = "frank_office_first_sex_done", op = "set" },
  { targetType = "player", flag = "talked_to_frank_today",       op = "set" },
]
# time_progression_minutes = 60
```

The bookkeeping pretense survives — $8 still pays out (he still calls it bookkeeping, he still hands her the receipts after). That's part of the dynamic.

### Authoring discipline reminders for the explicit register

- Frank's voice rules from doc 16 §2 still apply. He says "Quiet." not "Don't make a sound, baby." He says "Keep still." not "Stay there for me." Terse, imperative, no soft-talk.
- Maya's interiority carries the Tier-3 weight. The sensory grounding is HER experience (the desk takes her weight, the page slides, the lamp doesn't move, the kitchen clock ticking).
- Direct anatomy. No euphemism. RTS's PeepBrotherSex says "stroke your pussy" and "your aching breasts" — that's the register. Don't write around it.
- No apology in Frank's prose. He doesn't soften the next morning, doesn't acknowledge it happened in the kitchen breakfast scene at Stage 3+. Adjusted behavior, not words.

---

## §7 Per-stage cumulative summary

| Stage | Transition gate | Mechanical effect on transition | Narrative beat | Register |
|---|---|---|---|---|
| 0 (Suspicious) | (start state) | — | Frank as wary landlord, kitchen morning Stage-0 | Tier-2 (existing) |
| 0 → 1 | `trust >= 10 + frank_offered_bookkeeping is_true` | Bookkeeping activity opens at office | NEW: bookkeeping offer beat in kitchen morning | Tier-3 (new — §3) |
| 1 (Bookkeeping) | — | — | Frank with bookkeeping working relationship; ambient scenes at Stage-1 register | Tier-2 (existing + new ambients) |
| 1 → 2 | catch trigger (corruption ≥ 45 + restrict false + living room evening + Frank home) | `frank_caught + frank_restrict_declared + npc_frank_stage = 2` written in same effects block | The catch (existing — doc 16 §8 polish) | Tier-3 (existing, polished) |
| 2 (Restrict) | — | — | Chore offer + supervised office intro fire as one-time post-catch beats | Tier-2 (chore) + Tier-3 (office intro) — both new (§4) |
| 2 → 3 | `corruption ≥ 50 + restrict + Frank.arousal ≥ 30 + Frank.corruption ≥ 15` | `frank_cracked + npc_frank_stage = 3` written in choice exits | NEW: crack moment in office (§5) | Tier-3 (new) |
| 3 (Cracked / first sex) | — | — | NEW: `scene_office_after_crack` repeatable explicit office sex (§6) | Tier-3 explicit (new) |
| 3 → 4 | DEFERRED per D3 | dev shortcut only | — | — |
| 4 (Cracked / Keep route) | DEFERRED per D3 | — | — | — |

---

## §8 Counter retirement + helper rewrites + new flags (mechanical changes)

Single concise list for implementation.

### Traits — DELETE from `player.core_traits` (and every reference)

- `frank_tease_count`
- `frank_chore_count`
- `frank_bookkeeping_count`

(`lean_by_desk_count` stays — dev-only verification, no gate uses it.)

### Traits — ADD

- `npc_frank_corruption` — new NPC stat. Goes into the same trait set as `npc_frank.trust` and `npc_frank.arousal`. Initial value 0. No decay (per existing pattern for npc_frank stats).

### Flags — ADD to `[player.flag_keys]`

- `frank_offered_bookkeeping` (one-time guard for §3 offer scene; gates `activity_bookkeeping_with_frank`)
- `frank_declined_bookkeeping_today` (daily-reset; goes into `engine.daily_tick.flagEffects` list)
- `frank_offered_chores` (one-time guard for §4 chore offer; gates `activity_morning_chore`)
- `frank_supervision_explained` (one-time guard for §4 office intro)
- `frank_office_first_sex_done` (one-time guard for §6 — distinguishes first-time vs subsequent)

### Flags — VERIFY existing

- `frank_caught` — exists, written by catch
- `frank_restrict_declared` — exists, written by catch
- `frank_cracked` — exists (used by Stage 4 dev shortcut). Verify it's not unset anywhere unintentionally.

### Helper rewrites

**`frank_stage_1`:**
```toml
conditions = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "npc",    npc_id = "npc_frank", trait_key = "trust",                  operator = "gte", value = 10 },
  { type = "flag",  subject = "player",                       flag_key  = "frank_offered_bookkeeping", operator = "is_true" },
] }
```

**`frank_stage_3`:**
```toml
conditions = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "player",                       trait_key = "corruption",            operator = "gte", value = 50 },
  { type = "flag",  subject = "player",                       flag_key  = "frank_restrict_declared", operator = "is_true" },
  { type = "trait", subject = "npc",    npc_id = "npc_frank", trait_key = "arousal",               operator = "gte", value = 30 },
  { type = "trait", subject = "npc",    npc_id = "npc_frank", trait_key = "npc_frank_corruption",  operator = "gte", value = 15 },
] }
```

(`frank_stage_2` was deleted in the 2026-05-04 frank_stage_2 refactor — it was a post-condition tautology. Pattern 2's `_findStageSetterCanvas` finds the catch directly. No change needed here.)

### Activity gate additions

| Activity | Add to trigger conditions |
|---|---|
| `activity_bookkeeping_with_frank` | `frank_offered_bookkeeping is_true` |
| `activity_morning_chore` | `frank_offered_chores is_true` (in addition to existing `frank_restrict_declared` + Stage 2+) |

### `engine.daily_tick.flagEffects` — ADD

```toml
{ targetType = "player", flag = "frank_declined_bookkeeping_today", op = "unset" },
```

---

## §9 Implementation order (post-approval)

When implementation begins, in this order (each step is independently shippable):

| Step | Work | Verification |
|---|---|---|
| 1 | **Mechanical/structural** — counter retirement, helper rewrites, flag additions, activity gating, daily_tick update. No prose. | Build clean. All 141 existing tests pass. Compiled HTML no longer references `frank_tease_count` / `frank_chore_count` / `frank_bookkeeping_count`. |
| 2 | **Bookkeeping intro Tier-3 scene** — new Stage-0→1 branch in `scene_kitchen_with_frank_morning`. ~200 words. | Browser playtest: at trust 10 + offer flag false, kitchen morning fires the offer; accept → flag sets → bookkeeping activity appears at office. Decline → daily flag sets → next day offer comes back. |
| 3 | **Tease-choice distribution** — 6 small additions across the named scenes. ~50 words each per choice prose + effect block. | Browser playtest at Stage 2 + restrict + corruption 30: each scene shows the new tease choice; clicking each adds the triple effect; Frank.arousal climbs as expected. |
| 4 | **Crack scene** — new `scene_office_crack` branch in `scene_franks_office_supervised`. ~300 words. | At all 4 prereqs met, scene fires; choice exits set frank_cracked + advance to Stage 3. Subsequent visits use Stage-3 register. |
| 5 | **Stage 3 explicit office sex** — `scene_office_after_crack` branch replacing current Stage-3 dev-fragment. ~700 words. | Browser playtest: at Stage 3, office visit shows the new Stage-3 register; tease drip plays through climax; effects write as specified. |
| 6 | **Chore offer + office intro post-catch** (§4 polish) — Stage-2 branch in kitchen morning + first-time branch in supervised office. ~80 + ~150 words. | Browser playtest: post-catch, both fire as one-time intros; chore activity becomes available after kitchen offer. |

Steps 1-2 are the foundational fixes — without them the rest doesn't have a place to land. 3-6 are the content layer.

---

## §10 Risks and named tradeoffs

### Tier-3 budget

Doc 16 says T3 is rare (~30 of 130 RTS scenes ≈ 23%). This redesign adds 3 new T3 beats for Frank (bookkeeping intro, supervision intro, crack scene) on top of doc 16's planned 2 (catch polish, Stage 4 cracked-summons polish), plus the new Stage-3 explicit office sex which is also Tier-3 register. Frank's T3 share = ~6 of his ~14 scenes ≈ 43%.

Higher than the RTS ratio. Justification: Frank is the **pilot NPC** for the slice; the deluxe treatment is intentional. Ryan and Jake stay leaner — each gets only the canonical 2 carve-out beats (intro + capstone) when their redesigns happen. Slice-wide T3 share should average closer to RTS's 23-30% once all NPCs are redesigned.

### Frank.arousal pacing

Six tease sources at +1 each. A player choosing tease in every applicable scene every day after the catch reaches arousal 30 in ~5 days. Plus Frank.arousal +1/day passive tick (matches existing per-NPC daily arousal in slice). Plus Frank.arousal +5 at the catch itself.

Stage 3 reachable Day ~7-9 of slice, comfortably within the 10-day window. Player who teases less often takes longer; player who never teases never reaches Stage 3. This is correct — the player's choices determine pacing.

### Daily-reset on `frank_declined_bookkeeping_today`

Adds one line to existing `engine.daily_tick.flagEffects`. Not load-bearing. Removable later if the offer gets a different rhythm.

### Voice consistency for Stage 3 explicit content

Doc 16 §2 voice rules apply. Frank stays terse, sensory, no academic vocabulary, no apologizing. The risk is drift toward porn-genre dialogue ("come for me, baby") which is NOT his voice. Frank says "Quiet." and "Keep still." — that's the register. Author note: if a Stage 3 line feels pornographic in the dialogue itself, it's drifted. Cut back.

The explicit register lives in the **action description** (Maya's sensory experience, what is happening physically) and in the **silence and economy** of Frank's words, not in his dialogue going florid.

### Counter retirement breaks Pattern 2 goal block expectations

The Pattern 2 goal block on the Quests page currently renders the counter-based gate items. Once counters are retired, the goal block for Stage 2 → 3 will show the 4-AND helper instead — corruption ≥ 50, restrict, Frank.arousal ≥ 30, Frank.corruption ≥ 15. This is an improvement (every gate is multi-sourced and trackable) but the labels need to be in the trait_labels registry. Verify `npc_frank_corruption` gets a trait label entry when implementing step 1.

### Out-of-scope for this slice

- **Stage 4 cracked content** (D3 deferred — confirmed)
- **Multiple Stage-3 sex scenes.** Only the office scene is in scope. Bedroom/porch/kitchen sex variants stay out. Players can replay the office scene; that's the Stage-3 content for the slice.
- **Diana arc integration with Frank.** Diana stays a silent accumulator in the slice (per doc 16). Stage 3+ Frank doesn't reference Diana.
- **Marge dynamics with Frank.** Marge is an employer NPC in the slice; no Frank-Marge interactions authored.
- **Ryan and Jake.** Their redesigns use the same template (intro pattern + multi-source choices + register escalation) but happen in separate plans.

---

## §11 References

- `28th_april_TLS_Phase2_Redesign/16_Frank_Scene_Library_Design.md` — voice doc §2, schedule §3, tier discrimination §4, 12-scene library §5, locked decisions §1
- `28th_april_TLS_Phase2_Redesign/02_NPC_Stage_Chains.md` — line 112 already specified the bookkeeping intro pattern that was never wired
- `28th_april_TLS_Phase2_Redesign/13_Road_to_Success_Reference.md` — §6 walkthrough as planning UI, §11 bootstrap log lines 519-522 (Library/Natasha pattern), §12 turns 28-30, §10 stat economy
- `28th_april_TLS_Phase2_Redesign/14_Engine_PRD_Sandbox_Additions.md` and `15_Sandbox_Pivot_Direction.md` — sandbox pivot constraints (location-as-hub, repeatable-first)
- `games/the_long_summer_test/toml_phases/7_final_game.toml` — current Frank helpers (lines 100-135), bookkeeping activity (1425-1469), chore activity (1750-1795), supervised office (2789-2870), catch (2895-2982)
- `game_explorations/rts-discovery-trace/synthesis.md` — RTS pattern evidence (two-pass live play, PeepBrotherSex full drip)
- `game_explorations/rts-discovery-trace/passage_catalog.json` — source catalog for additional explicit-register reference

End of doc 18.
