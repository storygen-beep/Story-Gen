# 21 — RTS Brother Mechanism Audit (per-scene structural pass)

> **Status:** Audit record. Authored 2026-05-05.
> **Purpose:** Resolve a generalization risk surfaced during doc 20 review — prior Phase 2 docs cited "linkreplace-drip + stat-conditional branches" as the RTS pattern, but the evidence base was 3-6 scenes out of Brother's 16. This doc walks all 16 Brother-arc passages directly from `passage_catalog.json` (full Twine source) and classifies each by mechanism. Updates the framing in doc 20 §1.E + §3 row 5 (engine S1 vs S7 conflation).
> **Method:** Source extraction only. Local artifact: `game_explorations/rts-arc-trace/passage_catalog.json` (361 passages, captured 2026-04-29). Per methodology rule §N (doc 15 §1), structure questions are extraction-answerable; behavior questions need live play. The mechanism question is structural.
> **Scope:** Brother-arc scenes only. Same audit template should be applied to Dad / Marcus / Edward before any TLS engine prioritization decision.

---

## §1 What we're answering

Three questions, all from doc 20 § review:

1. **Do all/most Brother scenes use the linkreplace-drip + stat-branch mechanism**, or is it concentrated in a subset?
2. **What's the structural shape** when they do — single stat-gate at cascade entry, multiple gates inside the cascade, or something else?
3. **Does PRD 14's S1 (per-block text_variants) match what RTS actually does**, or is it a different mechanism with similar-looking output?

---

## §2 Brother scene set — full enumeration (16 surfaces)

Sourced from `passage_catalog.json` grep + walkthrough cross-reference. 13 Brother-named passages + 3 multi-NPC bridges where Brother is a participant.

### Brother-bound (13)

`BrotherBedroom` (hub) · `PeepBrotherSex` · `BrotherCaughtMasturbating` · `BrotherBedroomTease` · `BrotherBedroomFlash` · `BrotherBedroomSex1` · `BrotherBedroomPregnantSex1` · `BrotherShowerSex` · `BrotherWashDishesSex` · `BrotherHelpStudy` · `SleepingBrother` · `BedroomStudyBrotherGrope` · `BedroomStudyBrotherGropePregnant`

### Multi-NPC bridges (3)

`PlayingGamesSex` (Brother + scenario) · `SellingMyStepsister` (Brother→Josh transfer) · `BedroomGrope` (Brother OR Dad, dice-rolled)

---

## §3 Mechanism table — every scene classified

Columns:
- **Words**: total source word count
- **LR**: count of `<<linkreplace>>` macros in source
- **StatIf**: count of stat-gate `<<if>>` patterns (`getCorruptionLevel`, `getArousal`, NPC stat refs)
- **StatInLR**: how many linkreplace blocks contain stat-gated content inside
- **ChoiceInLR**: how many linkreplace blocks contain a nested button or further linkreplace
- **Vid / Img**: media counts

| Scene | Type | Words | LR | StatIf | StatInLR | ChoiceInLR | Vid | Img | Pattern |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `BrotherBedroom` | hub | 222 | 0 | 0 | 0 | 0 | 0 | 1 | **Hub** (button injection by presence + time + relation) |
| `BrotherBedroomTease` | button (Tier-1) | 69 | 0 | 0 | 0 | 0 | 0 | 5 | **Pattern A** — single-render utility |
| `BrotherBedroomFlash` | button (Tier-1) | 93 | 0 | 0 | 0 | 0 | 0 | 11 | **Pattern A** — single-render utility |
| `BedroomGrope` | random multi-NPC | 130 | 0 | 2 | 0 | 0 | 0 | 5 | **Pattern B** — random-flash with NPC dice |
| `BedroomStudyBrotherGrope` | random | 127 | 1 | 2 | 0 | 0 | 0 | 3 | **Pattern B'** — random-flash with 1-beat reveal |
| `PeepBrotherSex` | random | 341 | 4 | 0* | 1 | 1 | 4 | 5 | **Pattern C** — per-step stat-gated cascade |
| `BrotherCaughtMasturbating` | random | 902 | 10 | 1 | 1 | 1 | 11 | 0 | **Pattern D** — top-of-cascade stat-gated entry, then linear |
| `BrotherBedroomSex1` | button | 811 | 12 | 0 | 0 | 1 | 13 | 0 | **Pattern E** — pure linear cascade (gate is on the BUTTON, not in scene) |
| `BrotherBedroomPregnantSex1` | button-variant | 523 | 8 | 0 | 0 | 1 | 9 | 0 | **Pattern E** — variant of Sex1, pregnancy branch |
| `BrotherShowerSex` | button (bathroom) | 673 | 9 | 2 | 1 | 1 | 15 | 0 | **Pattern D** |
| `BrotherWashDishesSex` | event (kitchen) | 556 | 8 | 0 | 1 | 1 | 8 | 0 | **Pattern D / E** (mostly linear with one mid-cascade check) |
| `BrotherHelpStudy` | event | 867 | 10 | 3 | 1 | 1 | 11 | 0 | **Pattern D** with multiple intermediate stat gates |
| `SleepingBrother` | button (LN) | 527 | 7 | 1 | 1 | 1 | 11 | 0 | **Pattern D** — top gate (relation/corruption); rejection variant if low |
| `BedroomStudyBrotherGropePregnant` | random-variant | 876 | 11 | 3 | 1 | 2 | 10 | 1 | **Pattern D** with pregnancy-aware variants |
| `PlayingGamesSex` | event-multi | 877 | 11 | 0 | 1 | 1 | 11 | 0 | **Pattern E** |
| `SellingMyStepsister` | random cross-NPC | 1077 | 18 | 0 | 1 | 2 | 16 | 0 | **Pattern F** — long cascade + real `[Accept]/[Refuse]` choice branch |

\* `PeepBrotherSex` `StatIf=0` from regex because the gates use `getArousal() > 0` and `getCorruptionLevel() >= 2` *inside the linkreplace bodies* (not at scene-entry); regex caught them as `StatInLR=1` instead. Verified by reading source — see §4.3.

---

## §4 The patterns, named and explained

Six structural patterns observed across Brother's 16 surfaces. Each has a verified canonical example.

### Pattern A — Single-render utility (Tier-1)

**Examples:** `BrotherBedroomTease` (69w), `BrotherBedroomFlash` (93w)

**Shape:**
```
title + 1-line description + 1 image (random from pool of 5-11) +
stat-tick effects + return button
```

**Source verbatim** (`BrotherBedroomFlash`):
```twine
<h3>You give a little show to your $npc.Brother.relationship</h3>
<<set $game.randomMedia to either("brotherflash1.webp", ..., "brotherflash5.webp")>>
<div class='shower'>[img[setup.ImagePath+'/house/brotherbedroom/' + $game.randomMedia]]</div>
<<UnlockNPCScene Brother BrotherBedroomFlash>>
<<AddExb>><<AddArousal>><<AddBrotherCorruption>><<AddTime '1'>>
<<button 'Return ↩️' 'BrotherBedroom'>><</button>>
```

**Mechanism:** No linkreplace. No stat checks. Random media slot for replay variety. Stat ticks happen on entry. **One paragraph, one image, one return.**

This is RTS Tier-1 in pure form. Doc 13 §9 was right that ~30% of the catalog is this thin.

### Pattern B — Random-flash with NPC dice (utility multi-NPC)

**Examples:** `BedroomGrope` (130w, multi-NPC)

**Shape:**
```
roll 1-2 dice → check which NPC at home with arousal > 0 →
render that NPC's grope variant + image + 1 speech line + stat ticks
```

**Mechanism:** Stat checks gate WHICH variant fires, not depth of variant. Each variant is a single-render flash (~30 words + image). Per-NPC corruption ticks accumulate from passive groping. **No cascade. One paragraph either way.**

### Pattern B' — Single-beat linkreplace (low-tier random)

**Examples:** `BedroomStudyBrotherGrope` (127w, 1 LR)

**Shape:** Same as Pattern B + one minor click-to-reveal beat. Effectively a Pattern B with a tiny narrative payoff click.

### Pattern C — Per-step stat-gated cascade

**Canonical example:** `PeepBrotherSex` (341w, 4 LR)

**Shape:**
```
opening paragraph + image
└── linkreplace "Peep" → +paragraph + video
    └── linkreplace "Stroke your pussy"
        ├── if getArousal() > 0: +paragraph + video
        │   └── linkreplace "Masturbate"
        │       ├── if getCorruptionLevel() >= 2: +paragraph + video
        │       │   └── linkreplace "Cum!" → climax + UnlockNPCScene + AddCorruption
        │       └── else: NotifyCorruption(2) + "I should get out of here..."
        └── else: AddArousal + "You are not aroused enough to do this"
```

**Mechanism:** Cascade with **multiple stat gates at intermediate beats**. Player can begin the cascade, but each subsequent click is gated. If the player doesn't meet a gate, they get a published threshold (`NotifyCorruption(2)`) and a one-line bail. The scene **partial-completes** at the gate level — they saw 2-3 beats but not all 4.

**Replay loop:** raise arousal → next visit gets past beat 2. Raise corruption to 2 → next visit gets past beat 3. Each stat increment unlocks one more cascade depth. **The "come back later" loop is per-stat-per-beat.**

### Pattern D — Top-of-cascade stat-gated entry

**Canonical example:** `BrotherCaughtMasturbating` (902w, 10 LR)

**Shape:**
```
opening paragraph + video
└── linkreplace "Enter the room" → +paragraphs + video + dialog
    ├── if getCorruptionLevel() >= 3 AND StageTwoCorruption(Brother):
    │   └── linkreplace "Shhh"  ← FULL 8-beat sex cascade (linear from here)
    │       └── linkreplace "You kiss him"
    │           └── linkreplace "You blow him"
    │               └── linkreplace "You show him your boobs"
    │                   └── linkreplace "You titty fuck him"
    │                       └── linkreplace "You jump on him"
    │                           └── linkreplace "You fuck him"
    │                               └── linkreplace "Harder!"
    │                                   └── linkreplace "He cums" → UnlockNPCScene
    ├── elif getCorruptionLevel() >= 3:
    │   └── "He hides his dick, tells you to leave" + StageNotification
    └── else (low corr):
        └── "Ew you pervert! Stop it!" + NotifyCorruption(3)
```

**Mechanism:** Cascade with **ONE stat gate at top-of-branch**. Either you're in the deep cascade (8 beats of seduction) or you're in one of two rejection variants. **No partway.** Inside the cascade: pure linear progression — each click reveals next beat, no further stat checks.

**Replay loop:** raise corruption to 3 → next visit unlocks the cascade entry → see all 8 beats. **The "come back later" loop is one-stat-one-shot.** You either get the full content or you get the rejection variant.

This is the pattern doc 13 §16 Finding 2 captured ("the `[Shhh]` choice appearing where `Ew gross!` was before is the literal payoff for stat-grinding").

### Pattern E — Pure linear cascade (gate on the entry BUTTON, not in scene)

**Canonical example:** `BrotherBedroomSex1` (811w, 12 LR, 0 stat-ifs in body)

**Shape:**
```
[scene only entered via "Have sex with him 🔥" button at hub,
 which itself gates on getCorruptionLevel() >= 3 + getArousal() > 0]

opening paragraph + video
└── linkreplace beat 1 → +paragraph + video
    └── linkreplace beat 2 → +paragraph + video
        └── ... (~10 more beats) ...
            └── linkreplace "He cums" → UnlockNPCScene + FinishSex
```

**Mechanism:** No stat checks inside the scene at all. The gate lives on the **button at the hub** — `BrotherBedroom` source line: `<<if getCorruptionLevel() >= 3>><<if getArousal() > 0>><<goto "BrotherBedroomSex1">>`. Player either qualifies and sees the entire cascade, or doesn't qualify and gets `NotifyCorruption(4)` at the hub.

**Replay loop:** none. Once unlocked, every visit shows the same content. **Depth-by-replay doesn't apply** — this scene is "either you get it or you don't."

### Pattern F — Long cascade + real branching choice

**Canonical example:** `SellingMyStepsister` (1077w, 18 LR, 2 nested-button slots)

**Shape:** Cascade with a real `[Accept] / [Refuse]` mid-scene choice that materially diverges. Per doc 13 §16 Finding 3 — rare, reserved for high-stakes story moments.

---

## §5 Distribution across Brother's 16 surfaces

| Pattern | Count | % of Brother | Doctrine layer |
|---|---:|---:|---|
| Hub (button injection) | 1 | 6% | location-render |
| **A** Single-render Tier-1 utility | 2 | 13% | daily texture |
| **B/B'** Random-flash multi-NPC | 2 | 13% | daily texture |
| **C** Per-step stat-gated cascade | 1 | 6% | flagship random encounter |
| **D** Top-of-cascade stat-gated entry | 6 | 38% | most random + button cascades |
| **E** Pure linear cascade (gate at hub) | 3 | 19% | high-stakes button scenes |
| **F** Long cascade + branching choice | 1 | 6% | cross-NPC bridges |

**~10 of 16 (63%) use linkreplace cascades.** **~4 of 16 (25%) are single-render Tier-1/Tier-2.** **1 hub** drives discoverability.

**Stat-branching distribution:**
- Per-step gates inside cascade (Pattern C): **1 scene (PeepBrotherSex only)**
- Top-of-cascade single gate (Pattern D): **6 scenes** — the dominant replay-driver
- No in-scene gate, hub gates entry (Pattern E): **3 scenes** — once-and-done
- No stat gating at all (Patterns A, B): **4 scenes** — Tier-1 utility

---

## §6 What this corrects in doc 20

### Doc 20 §1.E (E. Same scene, different depth at different stats)

**Original framing (doc 20):** "engine S1 — per-block text_variants" cited as the doctrine match.

**Correct framing (per this audit):** the depth-shift mechanism in RTS is **`<<linkreplace>>` cascades with stat gates positioned at one of three locations:**
1. The **button at the hub** (Pattern E — most one-shot scenes work this way)
2. The **top of the cascade after one opening beat** (Pattern D — most replay-loop scenes)
3. **Inside intermediate cascade beats** (Pattern C — only PeepBrotherSex among Brother's set)

Per-block `text_variants` (PRD 14 S1, now archived) doesn't reproduce any of these three. It would produce a **fourth pattern** — "scene re-renders different paragraph text per-visit based on stats" — that RTS does not use anywhere in Brother's 16 surfaces. S1 is a TLS-engine-fit alternative, not a doctrine match.

The doctrine match is **S7 (linkreplace-drip multi-step scenes)** — also archived.

### Doc 20 §3 row 5 (S1 ranked HIGHEST gap)

**Correct ranking:**
- **HIGHEST**: linkreplace cascade (S7) is the actual mechanism RTS uses for the come-back-later loop. Without it, no Pattern C/D/E/F exists in TLS — the bedroom anchor (`scene_franks_bedroom_evening` ~400w) lands as one wall instead of a paced cascade with one stat gate at top.
- **HIGH (and missing from PRD 14)**: hub button injection by presence + time + NPC stat (`<<if $npc.Brother.relation >= 10>><<button 'Sleep with him 💤' 'SleepingBrother'>>`). The room evolves with the player. **Frank's locations don't do this.**
- **HIGH**: `NotifyCorruption(N)` / threshold notifications (S4) — universal RTS pattern, every gate publishes its threshold.
- **MED-LOW**: `text_variants` per-block (S1) — would approximate Pattern D's "different version of scene per stat" but as a cheaper substitute, not as a doctrine match.

### Doc 20 §1.H (in-context button injection)

**Refinement:** the 2026-05-04 memory said "Visiting BrotherBedroom at corruption 31 + Brother arousal 🔥🔥 + relation 10 in evening rendered 4 NEW buttons (Talk / Tease / Flash / Have sex)." Audit shows the actual hub mechanism is **mixed**:
- Talk / Tease / Flash / Have sex buttons: **render conditionally on NPC PRESENCE + time band**, not on stats. Stat gating happens inside the click handlers (e.g., `Have sex` click → `<<if getCorruptionLevel() >= 3>>` → goto scene OR `NotifyCorruption(4)`).
- Sleep with him button: **renders conditionally on STAT** (`$npc.Brother.relation >= 10`) AND time band (LN only). This is the only true stat-injected button in this hub.
- Random-encounter override: separate path (`<<if previous() == "Hallway">><<set $game.random = random(1,4)>><<if $game.random == 1 && !executedToday>><<goto 'PeepBrotherSex'>>`). Bypasses button menu entirely, replaces hub render with the encounter passage.

So §H button injection is more accurately described as **"hub renders different button SETS per (presence × time × stats), AND can be replaced entirely by random-encounter passage on entry from a hub-of-hub."** Stat-injected buttons exist but are rarer than the memory implied.

---

## §7 What this means for Frank — applicability check

Mapping Brother's pattern distribution onto Frank's slice (per doc 20 §2 inventory):

| Frank canvas | Closest Brother pattern | Currently uses | Gap |
|---|---|---|---|
| `scene_kitchen_with_frank_morning` | Pattern D (top-of-cascade gate, repeating) | `[group]` cascade by stage flag, single-render | No linkreplace → flat wall instead of paced reveal |
| `scene_office_after_crack` (S3 anchor, ~repeating) | Pattern D | single-render | No linkreplace |
| `scene_franks_bedroom_evening` (S4 anchor, ~400w) | Pattern E (long linear cascade, hub-gated) | single-render | No linkreplace — biggest narrative scene reads as a wall |
| `scene_office_crack` (one-shot capstone) | Pattern F (long cascade + maybe branching) | single-render | No linkreplace + no real branching |
| `scene_hallway_frank_pass` (~50w pilot) | Pattern A (single-render Tier-1) | single-render | ✅ aligned |
| `scene_kitchen_frank_coffee_alone` (pilot) | Pattern A or B | single-render | ✅ aligned |
| `scene_living_room_frank_radio` (pilot) | Pattern A or B | single-render | ✅ aligned |
| `scene_porch_frank_evening_smoke` (pilot) | Pattern A or B | single-render | ✅ aligned |
| `activity_talk_to_frank` | varies | single-render | depends on intent |
| `BrotherBedroom`-equivalent hubs (Hallway / Kitchen / Office) | Hub | static button sets | No presence/time/stat-injected button rendering |

**Bottom line:** Frank's pilot daily-texture scenes (5 ambient surfaces) are correctly Pattern A/B-shaped. **The high-content scenes** (kitchen morning cascade, office after-crack, bedroom anchor, crack capstone) **all need Pattern D or E to match RTS feel — and that requires S7 (linkreplace-drip)**, which is archived along with the rest of PRD 14.

---

## §8 Confidence ladder

For honesty about what this audit *does* and *doesn't* establish:

✅ **HIGH confidence (verified against passage source):**
- Brother has 16 scenes (13 named + 3 multi-NPC bridges)
- ~10 of 16 use `<<linkreplace>>` cascades
- Six structural patterns (A-F) are reproducible across the set
- Pattern D dominates (6 scenes — most stat-branched cascades)
- Hub button injection is presence+time-driven, not primarily stat-driven (only Sleep button is stat-injected)
- Per-block text_variants is NOT one of the patterns RTS uses

🟡 **MED confidence (inferred from source but not live-verified):**
- Word-count-to-LR ratio (~50-80w per beat) generalizes to other NPCs
- Pattern distribution percentages — Brother is one NPC; Dad/Marcus/Edward may distribute differently
- Tier classification (which scenes are T1/T2/T3) was eyeballed from word count + structure; doc 13 §9 had the same classification scheme but didn't tag every scene

❌ **NOT established (would need live play OR Dad/Marcus/Edward audits):**
- Whether the Pattern D top-of-cascade gate "feels" like a satisfying replay payoff (live play is the only way to verify the *experience*)
- Whether NPCs other than Brother distribute patterns the same way (the user's original instinct — "do they have similar/same content" — is right to push on; same audit needed on Dad's 12 + Marcus's 5 + Edward's 4 before generalizing)
- Whether `checkSceneReq()` (called in soft-fail button handlers) does anything different from what the docs imply
- Whether Pattern F (real branching choice) appears anywhere besides `SellingMyStepsister`

---

## §9 Recommended next steps

1. **Update doc 20 §1.E + §3 row 5 + §1.H + §4 ranking** to reflect the mechanism corrections in §6 above. (Low effort — text edits.)
2. **Run the same audit on Dad (12 scenes) and Marcus (5 scenes)** to test the generalization. Same `passage_catalog.json`, same script. ~30 min.
3. **Live-play 2-3 unverified Brother scenes** (Tease, Sex1, SleepingBrother) to verify experience matches structural prediction. Optional — structural evidence is strong, but methodology rule §N says use both. ~30 min via twine-game-explorer skill resume.
4. **Decision gate:** with mechanism settled, decide whether to un-archive S7 (linkreplace-drip) as the priority engine work, or accept that TLS is intentionally building a different feel from RTS (single-render scenes with `[group]` cascades by stage flag).

---

## §10 Source artifacts

- `game_explorations/rts-arc-trace/passage_catalog.json` — 1.2 MB, 361 passages, captured 2026-04-29 (engine: SugarCube)
- All 16 Brother-scene source bodies extractable verbatim via `passages[name]['source_raw']`
- Verbatim source for canonical examples (PeepBrotherSex / BrotherCaughtMasturbating / BrotherBedroomFlash / BedroomGrope / BrotherBedroom hub) included in this conversation's context

---

End of audit.
