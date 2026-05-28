# Reference 02 — RTS Per-NPC Scene Catalog

**Sources:** Doc 13 §5; Doc 21 (Brother 16-surface audit); Doc 22 (40-surface / 4-NPC comparison); Doc 24 §3 Brother walkthrough table; live extraction in `game_explorations/rts-arc-trace/passage_catalog.json` (361 passages, 1.2MB).
**Authority:** Reference — source-extracted scene catalogs for the 4 audited RTS NPCs.
**Purpose:** Give the LLM concrete per-NPC scene tables with: scene name + lane classification + GUIDE string + chance % + structural pattern (A–F) + word count. The catalog the doctrine cites.

This file is the empirical ground truth for `doctrine/02_three_lanes_plus_capstone.md` (lane mechanism) + `doctrine/04_authoring_rules.md` D56-R3 (per-arc-shape Lane 3 budget).

---

## §1 — What this catalog is

Doc 21 + Doc 22 audited 4 NPCs across 40 total surfaces (~30% of RTS's ~130 NPC-bound scene catalog). Each scene classified by:

- **Lane:** 1 (hub button) / 2 (location-entry random) / 3 (dispatcher substitution) / hub
- **Pattern (A–F):** structural shape of the cascade (see §6 below for pattern definitions)
- **Chance:** dice probability when triggered
- **GUIDE:** plain-English trigger recipe (as rendered in the Walkthrough panel — see `reference/03_rts_walkthrough_panel.md`)
- **Stat reqs:** NPC arousal + corruption + relation + player corruption thresholds
- **Words / LR / media:** content density indicators

**6 patterns observed (Doc 21 §4):**
- **A** Single-render utility (Tier-1)
- **B / B'** Random-flash multi-NPC / 1-beat reveal
- **C** Per-step stat-gated cascade
- **D** Top-of-cascade stat-gated entry
- **E** Pure linear cascade (gate on entry button)
- **F** Long cascade + real branching choice

Pattern definitions live in §6. Per-NPC catalogs in §2–§5.

---

## §2 — Brother (Family/ambient — 16 surfaces, 47% Lane 3)

The largest audited NPC arc. Brother is the canonical family/ambient reference (`doctrine/03_arc_shapes.md` §3).

### §2.1 — Brother walkthrough table (Doc 24 §3 — verbatim from in-game panel)

Source: in-game RTS Walkthrough → Stepbrother table, captured 2026-05-10 from `mopoga.com/road-to-success` v0.25. Fifteen scenes (the 16th is multi-NPC bridge `BedroomGrope`).

| # | Scene | NPC reqs | MC reqs | Chance | GUIDE | **Lane** |
|---|---|---|---|---:|---|---|
| 1 | Stepbrother Bedroom Grope | arousal 🔥 | None | 20% | Go to your bedroom | **2** |
| 2 | Stepbrother Bedroom Study Grope | arousal 🔥 + corr 1 | None | 20% | Study at your room | **3** |
| 3 | Stepbrother Bedroom Study Grope Pregnant | arousal 🔥 + corr 1 + pregnant | corr 30 | 20% | Study at your room while pregnant | **3** |
| 4 | Sleep with Stepbrother | arousal 🔥 + corr 10 | corr 30 | 100% | Go to Stepbrother bedroom late at night and ask to sleep with him | **1** |
| 5 | Stepbrother Bedroom Flash | None | corr 5 | 100% | Go to your Stepbrother bedroom | **1** |
| 6 | Bedroom Tease | None | corr 5 | 100% | Go to your Stepbrother bedroom | **1** |
| 7 | Stepbrother Shower Sex | arousal 🔥 + corr 5 | corr 30 | 33% | Masturbate at shower at the house bathroom | **3** |
| 8 | Peep Stepbrother sex | None | corr 15 | 25% | Go to your Stepbrother bedroom | **2** |
| 9 | Playing Videogame Pregnant | arousal 🔥🔥 + corr 10 + pregnant | corr 30 | 20% | Play videogame at your living room while pregnant | **3** |
| 10 | Playing Videogame | arousal 🔥🔥 + corr 10 | corr 30 | 20% | Play videogame at your living room | **3** |
| 11 | Brother Help Study | arousal 🔥🔥🔥 + corr 15 | None | 20% | Study at your room | **3** |
| 12 | Brother Caught Masturbating | arousal 🔥🔥 + corr 10 | corr 30 | 25% | Go to your Stepbrother bedroom | **2** |
| 13 | Brother Bedroom Pregnant Sex I | None | None | 100% | Go to your Stepbrother bedroom while pregnant and have sex with him | **1** |
| 14 | Brother Bedroom Sex I | None | None | 100% | Go to your Stepbrother bedroom and have sex with him | **1** |
| 15 | Stepbrother Washing Dishes Sex | arousal 🔥🔥 + corr 10 | corr 30 | 20% | Go to the kitchen and wash the dishes | **3** |

**Distribution:**

| Lane | Count | % of 15 |
|---|---:|---:|
| **1 — Hub button** | 5 | 33% |
| **2 — Location-entry random** | 3 | 20% |
| **3 — Dispatcher inside menu activity** | **7** | **47%** |

**Lane 3 is the largest bucket.** Almost half of Brother's repeatable surfaces fire as random substitutions inside other menu activities. This is RTS's primary mechanism for "the NPC is everywhere in your day-to-day life without overstuffing menus."

The 7 lane-3 surfaces piggyback on **four parent activities:**
- Study (×3 — base, pregnant variant, Help Study)
- Play Videogame (×2 — base + pregnant variant)
- Shower→Masturbate (×1)
- Wash Dishes (×1)

### §2.2 — Brother structural pattern table (Doc 21 §3 — 13 Brother-bound + 3 multi-NPC)

Columns:
- **Words:** total source word count
- **LR:** count of `<<linkreplace>>` macros in source
- **StatIf:** count of stat-gate `<<if>>` patterns
- **StatInLR:** how many linkreplace blocks contain stat-gated content inside
- **ChoiceInLR:** how many linkreplace blocks contain a nested button or further linkreplace
- **Vid / Img:** media counts

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

\* `PeepBrotherSex` `StatIf=0` from regex because the gates use `getArousal() > 0` and `getCorruptionLevel() >= 2` *inside the linkreplace bodies* (not at scene-entry); regex caught them as `StatInLR=1` instead.

### §2.3 — Brother pattern distribution

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
- Per-step gates inside cascade (Pattern C): 1 scene (PeepBrotherSex only)
- Top-of-cascade single gate (Pattern D): 6 scenes — the dominant replay-driver
- No in-scene gate, hub gates entry (Pattern E): 3 scenes — once-and-done
- No stat gating at all (Patterns A, B): 4 scenes — Tier-1 utility

---

## §3 — Dad / Stepfather (Family/proximity — 9 named surfaces)

| Scene | Type | Words | LR | StIf | StLR | CILR | Vid | Img | Pattern |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `DadBedroom` | hub | 201 | 3 | 0 | 1 | 1 | 0 | 3 | **Hub variant** — has its own linkreplace! Different from `BrotherBedroom` |
| `DadPeepSex` | random | 647 | 9 | 0 | 1 | 1 | 8 | 0 | **Pattern D** |
| `DadPeepSexBedroom` | random | 683 | 10 | 0 | 1 | 1 | 11 | 0 | **Pattern D** |
| `DadShowerSex` | event | 642 | 9 | 1 | 1 | 1 | 13 | 0 | **Pattern D** |
| `DadShowerSexPregnant` | variant | 517 | 7 | 1 | 1 | 1 | 7 | 0 | **Pattern D** |
| `DadWashDishesSex` | event | 668 | 6 | 2 | 1 | 1 | 11 | 0 | **Pattern D** with multi-stat gate |
| `DadWashDishesSexPregnant` | variant | 493 | 6 | 1 | 0 | 1 | 8 | 0 | **Pattern E** (linear, gate elsewhere) |
| `BedroomSleepDadScene` | random | 745 | 9 | 2 | 1 | 1 | 10 | 0 | **Pattern D** + thought bubbles (Doc 13 §16 Finding 1) |
| `BedroomStudyDadGrope` | random | 329 | 8 | 3 | 1 | 1 | 8 | 1 | **Pattern D** with multiple intermediate gates |

**Distribution:** 8/8 content scenes use linkreplace cascades. **0 single-render utility scenes** (Dad has no Tease/Flash equivalents — father archetype is more passive than brother archetype). Pattern D dominant. Hub itself uses linkreplace (Brother's hub doesn't).

**Implication:** Dad is a "deeper but smaller" arc than Brother. Same arc tendency (family/ambient), different density curve. For TLS-shape sandboxes: family/ambient NPCs can vary in distribution within the shape — Brother's "many short" approach vs Dad's "fewer longer" approach are both valid.

---

## §4 — Marcus (Peer/quest-chain — 12 named surfaces)

| Scene | Type | Words | LR | StIf | StLR | CILR | Vid | Img | Pattern |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `MarcusHallway` | hub-thin | 43 | 0 | 0 | 0 | 0 | 0 | 1 | **Hub-thin** — just nav + image |
| `MarcusBathroom` | nav | 42 | 0 | 0 | 0 | 0 | 0 | 1 | **Pattern A** — single-render |
| `MarcusBathroomEncounter` | event | 176 | 1 | 0 | 1 | 1 | 0 | 2 | **Pattern B'** — 1-beat reveal |
| `MarcusBedroom` | nav | 99 | 0 | 0 | 0 | 0 | 0 | 1 | **Pattern A** — single-render |
| `MarcusBedroomSex1` | button | 585 | 9 | 0 | 0 | 1 | 10 | 0 | **Pattern E** — linear cascade, gate at hub button |
| `MarcusBedroomSexPregnant` | variant | 429 | 7 | 0 | 0 | 1 | 8 | 0 | **Pattern E** |
| `MarcusClassSex` | event | 630 | 9 | 0 | 0 | 1 | 10 | 0 | **Pattern E** |
| `MarcusParkDate` | event | 452 | 6 | 0 | 1 | 3 | 0 | 0 | **Pattern F** — `HideDiv` parallel branches + Accept/Decline + nested stat gate |
| `MarcusParkSex` | event | 726 | 10 | 0 | 0 | 1 | 10 | 0 | **Pattern E** (entered from ParkDate Accept→Follow) |
| `StudyWithMarcus` | event | 678 | 10 | 0 | 0 | 1 | 13 | 0 | **Pattern E** |
| `BathroomSurpriseMarcusBoyfriend` | event | 957 | 10 | 0 | 1 | 1 | 12 | 0 | **Pattern D** |
| `CaughtMasturbatingMarcusBoyfriend` | event | 1945 | 18 | 0 | 1 | 1 | 24 | 0 | **Pattern D** — Marcus's longest scene |

**Distribution:** 8/12 use linkreplace cascades; 4/12 are short utility/navigation. **Pattern E dominant** for sex/intimate scenes (qualify-then-full content) — fits the peer/quest-chain doctrine. Pattern F appears once (ParkDate — relationship-defining moment with real Accept/Decline).

**Implication:** peer/quest-chain arcs have a different cascade signature from family/ambient. **Pattern E** (hub-gated linear) dominates because the player has already committed by clicking through the prereq chain — gate at the entry button is appropriate. Family/ambient uses Pattern D (top-of-cascade gate) because random-encounter entry means the gate has to live inside the scene.

For TLS Ryan (peer/dating): Pattern E for sex scenes; Pattern F for relationship-defining moments (partner-commit capstone Phase 2+).

---

## §5 — Edward (Career/digital — 1 named scene + DM widget)

| Scene | Type | Words | LR | StIf | StLR | CILR | Vid | Img | Pattern |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `EdwardThreesome` | event | 951 | 16 | 0 | 0 | 1 | 14 | 1 | **Pattern E** — long linear cascade, hub-gated (DM accept) |
| `Instafame` | app-shell | 420 | 0 | 0 | 0 | 0 | 0 | 0 | **Hub-app** — phone app shell |
| `InstafameDM` | DM-thread shell | 70 | 0 | 0 | 0 | 0 | 0 | 0 | **Hub-thin** — DM list shell |

**Plus:** `InstafameMessages` widget (9331 chars) contains the DM conversations. Edward's `EdwardDM` widget verified: **Pattern F** — linkreplace cascade with a `HideDiv`-based Accept/Decline branch at corruption ≥ 3 + `<<NotifyCorruption 3>>` for the rejection variant. **Mechanism structurally identical to MarcusParkDate**, rendered in DM frame instead of park scene.

### Implication: career/digital is presentation-layer different, mechanism-layer identical

Edward's "career/digital" arc tendency is in the *framing* (DM-mediated, async, calendar-driven) — not in the cascade mechanism. The same Pattern F that governs MarcusParkDate governs EdwardDM. **The arc tendency is presentation; the mechanism is shared.**

For TLS-shape sandboxes: career/digital arcs (if scoped) can use the same cascade primitives (Patterns A–F) as family/peer arcs — only the entry mechanism differs (DM widget arrival vs. location entry).

---

## §6 — The 6 patterns (definitions + canonical examples)

Six structural patterns observed across the 40 audited surfaces. Each has a verified canonical example.

### §6.1 — Pattern A — Single-render utility (Tier-1)

**Examples:** `BrotherBedroomTease` (69w), `BrotherBedroomFlash` (93w), `MarcusBathroom` (42w), `MarcusBedroom` (99w)

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

This is RTS Tier-1 in pure form. ~30% of the catalog is this thin.

### §6.2 — Pattern B — Random-flash with NPC dice (utility multi-NPC)

**Examples:** `BedroomGrope` (130w, multi-NPC)

**Shape:**
```
roll 1-2 dice → check which NPC at home with arousal > 0 →
render that NPC's grope variant + image + 1 speech line + stat ticks
```

**Mechanism:** Stat checks gate WHICH variant fires, not depth of variant. Each variant is a single-render flash (~30 words + image). Per-NPC corruption ticks accumulate from passive groping. **No cascade. One paragraph either way.**

### §6.3 — Pattern B' — Single-beat linkreplace (low-tier random)

**Examples:** `BedroomStudyBrotherGrope` (127w, 1 LR), `MarcusBathroomEncounter` (176w, 1 LR)

**Shape:** Same as Pattern B + one minor click-to-reveal beat. Effectively a Pattern B with a tiny narrative payoff click.

### §6.4 — Pattern C — Per-step stat-gated cascade

**Canonical example:** `PeepBrotherSex` (341w, 4 LR) — **the only verified Pattern C across all 40 audited surfaces**

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

**Replay loop:** raise arousal → next visit gets past beat 2. Raise corruption to 2 → next visit gets past beat 3. **The "come back later" loop is per-stat-per-beat.**

**Pattern C is rare** — only 1 of 40 audited surfaces. Doc 21 may have over-weighted it as a category by treating PeepBrotherSex as exemplary. Most cascades use Pattern D (top-gate) or Pattern E (hub-gate).

### §6.5 — Pattern D — Top-of-cascade stat-gated entry (the dominant pattern)

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

**Pattern D dominates the catalog** (15 of 40 = 38%). Most family/ambient cascades use this pattern.

### §6.6 — Pattern E — Pure linear cascade (gate on the entry BUTTON, not in scene)

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

**Mechanism:** No stat checks inside the scene at all. The gate lives on the **button at the hub**. Player either qualifies and sees the entire cascade, or doesn't qualify and gets `NotifyCorruption(4)` at the hub.

**Replay loop:** none. Once unlocked, every visit shows the same content. **Depth-by-replay doesn't apply** — this scene is "either you get it or you don't."

**Pattern E dominates peer/quest-chain arcs** (Marcus: 5 of 12 scenes). Family arcs use it for high-stakes once-and-done scenes (BrotherBedroomSex1).

### §6.7 — Pattern F — Long cascade + real branching choice

**Canonical examples:** `SellingMyStepsister` (1077w, 18 LR), `MarcusParkDate` (452w, 6 LR), `EdwardDM` (in `InstafameMessages` widget, 9331c)

**Shape:** Cascade with a real `[Accept] / [Refuse]` mid-scene choice that materially diverges downstream. Reserved for high-stakes story moments.

**Live verification (Doc 22 §11):** `MarcusParkDate` Accept/Decline mechanism confirmed: parallel cascades hidden/shown via `<<HideDiv>>`; per-beat effects fire on click; `<<MakeBoyfriend Marcus>>` macro inside Accept linkreplace block fires on click (player.relationship.loyalty: 0 → 100).

**Pattern F is rare** (3 of 40 = 8%). Reserved for relationship-defining moments. For TLS-shape sandboxes: Lane 4 capstone Type B (Doc 57 §3) maps directly to Pattern F.

### §6.8 — Hub passages (4 audited)

Hubs vary more than expected. Not all NPC hubs follow the same template.

| Hub | NPC | Words | LR | Mechanism |
|---|---|---:|---:|---|
| `BrotherBedroom` | Brother | 222 | 0 | Button menu by presence + time + relation. Random-encounter override on entry from Hallway. |
| `DadBedroom` | Dad | 201 | 3 | **Has its own linkreplace** — peeking through the door is built INTO the hub before the button menu. |
| `MarcusHallway` | Marcus | 43 | 0 | Thin navigation passage. Marcus content is event-triggered, not button-menu-driven. |
| `Instafame` | Edward | 420 | 0 | Phone app shell — feed of posts + DM access button. |
| `InstafameDM` | (DM list) | 70 | 0 | DM thread list — each thread opens a `<<widget>>` cascade. |

**Family/proximity hubs:** room passages with button menus + sometimes their own linkreplace. Stat-injected buttons (`Sleep with him` at relation ≥ 10) are rare; presence/time injection is universal.

**Peer hubs:** thin navigation. Peer scenes are event-driven (Park Date, Class, Bathroom Encounter), not menu-driven. Player initiates by going to the location at the right time.

**Career hubs:** app/feed shells. Content arrives async via DM widgets, not via button menus.

---

## §7 — Cross-NPC pattern distribution (Doc 22 §3)

40 surfaces total across 4 NPCs.

| Pattern | Brother | Dad | Marcus | Edward | Total | % of 40 |
|---|---:|---:|---:|---:|---:|---:|
| Hub (button injection) | 1 | 1 | 1 | 1 | **4** | 10% |
| **A** Single-render utility | 2 | 0 | 2 | 0 | **4** | 10% |
| **B/B'** Random-flash multi-NPC / 1-beat | 2 | 0 | 1 | 0 | **3** | 8% |
| **C** Per-step stat-gated cascade | 1 | 0 | 0 | 0 | **1** | 3% |
| **D** Top-of-cascade gate, then linear | 6 | 7 | 2 | 0 | **15** | 38% |
| **E** Pure linear cascade (gate at hub button) | 3 | 1 | 5 | 1 | **10** | 25% |
| **F** Long cascade + real branching choice | 1 | 0 | 1 | 1 (DM widget) | **3** | 8% |

**Aggregate cascade rate: 29 of 40 surfaces (~73%) use `<<linkreplace>>`.** Single-render utility: 7 of 40 (~18%). Hubs: 4 of 40 (~10%).

**Per-block `text_variants`: 0 of 40.** Confirmed absent across the 4 audited NPCs.

---

## §8 — Where gate placement lives per arc tendency

Doc 22 §4 — the arc-tendency difference doesn't change WHETHER cascades exist — it changes WHERE the stat gate sits within the cascade structure.

| Arc tendency | Dominant pattern | Where stat gate lives | Replay loop |
|---|---|---|---|
| **Family / proximity** (Brother, Dad) | Pattern D | **Top of cascade**, after opening beat | Per-NPC stat threshold → cascade unlocks fully on next visit. **Single-step replay**: cross threshold once, all content available. |
| **Peer / quest-chain** (Marcus) | Pattern E | **At the hub button** | **No replay variation** — once narrative prereq met, cascade plays the same every time. Quest progression replaces tier progression. |
| **Career / digital** (Edward) | Pattern E (Threesome) + Pattern F (DMs) | **At the hub button OR DM widget gate** | DM-async progression. Real Accept/Decline branches at money/sex moments. |

**Key insight:** the "story shape" (random/deterministic/quest-chain/calendar) is delivered by:
1. Where the trigger fires (hub random encounter vs button vs DM arrival)
2. Where the stat gate sits (mid-cascade vs hub button vs DM widget)
3. The framing layer (room visit vs date scene vs phone DM)

The CONTENT MECHANISM (linkreplace cascade with stat-gated branches) is the same primitive across all three. **One engine, three framings, three gate-placements — same mechanic.**

**Implication for TLS-shape sandboxes:** adopting linkreplace cascades doesn't lock the game into one arc shape. The same cascade primitive supports family-style (Pattern D), peer-style (Pattern E), career-style (Pattern E + F).

---

## §9 — Confidence ladder

Per methodology rule (use both source extraction AND live play, never one alone):

✅ **HIGH confidence (source-verified + live-verified across 4 NPCs):**
- 6 patterns (A-F) reproducible across all 4 audited NPC sets
- ~73% cascade rate generalizes (varies by NPC: Dad 100%, Brother 63%, Marcus 67%, Edward 100% of content scenes)
- Per-block `text_variants` used in 0 of 40 surfaces
- Arc tendencies manifest in gate placement, not cascade existence
- Pattern E dominates peer/career; Pattern D dominates family
- Live verification (Doc 22 §11, 2026-05-06) confirmed Pattern D + E + F mechanisms in live play

🟡 **MED confidence:**
- 4 NPCs out of RTS's ~16 with `scenes` objects audited (~25% of the named-NPC catalog). Other NPCs (Grandpa 6 / Sam 2 / Veronica 3 / Priest 2 / Jamal 3 / Josh 1 / Tow Truck Driver 1 / Yacht Captain 1 / Thief 2) may surface additional patterns or different distributions.
- Hub variation observation (4 hubs) — small sample for that conclusion specifically.

❌ **NOT established:**
- Live experience of pattern D vs E "feels" (which is more satisfying for replay)
- Whether location-bound scenes (~70 per Doc 13 §3) follow the same pattern distribution as NPC-bound — completely unaudited
- Whether `checkSceneReq()` semantics affect Pattern E gating in ways the source doesn't expose

---

## §10 — Cross-references

### Sibling reference files

- `reference/01_rts_overview.md` — broad RTS context (size, time engine, bootstrap experience)
- `reference/03_rts_walkthrough_panel.md` — the surface that renders these scene tables to the player
- `reference/04_rts_hud_world_model.md` — sidebar (HUD) doctrine

### Source docs

- `28th_april_TLS_Phase2_Redesign/13_Road_To_Success_Reference.md` — RTS broad catalog
- `28th_april_TLS_Phase2_Redesign/21_RTS_Brother_Mechanism_Audit.md` — Brother 16-passage audit source
- `28th_april_TLS_Phase2_Redesign/22_RTS_Cross_NPC_Mechanism_Comparison.md` — 40-surface comparison source
- `28th_april_TLS_Phase2_Redesign/24_RTS_Three_Lanes_Repeatable_Activities.md` §3 — Brother walkthrough table source

### Sibling doctrine files (this catalog informs)

- `doctrine/02_three_lanes_plus_capstone.md` — Lane mechanism (Patterns A-F map to lanes)
- `doctrine/03_arc_shapes.md` — 5 TLS arc shapes refine the 3 RTS tendencies
- `doctrine/04_authoring_rules.md` D56-R3 — per-arc-shape Lane 3 budget (Brother 47% Lane 3 sets the family/ambient bound at 4-7)

### RTS source artifacts

- `game_explorations/rts-arc-trace/passage_catalog.json` — 1.2MB / 361 passages, all 40 audited surfaces verbatim
- Verbatim source for canonical examples (BrotherCaughtMasturbating, BrotherBedroomSex1, MarcusParkDate, EdwardDM widget) included in Doc 21 + Doc 22 evidence sections

---

**End of file.** Next: `reference/03_rts_walkthrough_panel.md` for the Walkthrough doctrine (P2 transparent gating).
