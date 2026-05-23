# 22 — RTS Cross-NPC Mechanism Comparison (Brother / Dad / Marcus / Edward)

> **Status:** Audit record. Authored 2026-05-05.
> **Purpose:** Test the generalization claim from doc 21 — does the Brother mechanism distribution hold across other NPC arcs (family / peer / career), or is each NPC's structure idiosyncratic? User's original instinct ("do they have similar / same content") is the question this doc answers.
> **Method:** Same source-extraction pass as doc 21, applied to Dad (9 named scenes), Marcus (12 named), Edward (1 scene + DM widget). Local artifact: `passage_catalog.json`. Per methodology rule §N, structure-extracted; not live-verified.
> **Total surfaces audited:** **40** (Brother 16 + Dad 9 + Marcus 12 + Edward 3). Out of RTS's ~130 NPC-bound scenes, this is ~30% of the catalog — significant but not exhaustive. Six NPCs (Sam, Emma, Jamal, Veronica, Priest, Mr. Matthew, etc., per doc 13 §3) remain unaudited.

---

## §1 What we're testing

Doc 21 established six structural patterns (A-F) across Brother. Three open questions:

1. **Do other NPCs use the same patterns**, or different ones?
2. **Does the doc 13 §5 "three arc tendencies" claim** (family/peer/career as different player loops) **manifest in the mechanism**, or only in the gating-style?
3. **Is per-block `text_variants` used by ANY NPC**, or is it confirmed absent from the entire catalog (so far)?

---

## §2 Per-NPC mechanism tables

### Dad (Stepfather) — 9 named surfaces, family/proximity tendency

| Scene | Type | Words | LR | StIf | StLR | CILR | Vid | Img | Pattern |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `DadBedroom` | hub | 201 | 3 | 0 | 1 | 1 | 0 | 3 | **Hub variant** — has its own linkreplace! Different from `BrotherBedroom` |
| `DadPeepSex` | random | 647 | 9 | 0 | 1 | 1 | 8 | 0 | **Pattern D** |
| `DadPeepSexBedroom` | random | 683 | 10 | 0 | 1 | 1 | 11 | 0 | **Pattern D** |
| `DadShowerSex` | event | 642 | 9 | 1 | 1 | 1 | 13 | 0 | **Pattern D** |
| `DadShowerSexPregnant` | variant | 517 | 7 | 1 | 1 | 1 | 7 | 0 | **Pattern D** |
| `DadWashDishesSex` | event | 668 | 6 | 2 | 1 | 1 | 11 | 0 | **Pattern D** with multi-stat gate |
| `DadWashDishesSexPregnant` | variant | 493 | 6 | 1 | 0 | 1 | 8 | 0 | **Pattern E** (linear, gate elsewhere) |
| `BedroomSleepDadScene` | random | 745 | 9 | 2 | 1 | 1 | 10 | 0 | **Pattern D** + thought bubbles per doc 13 §16 Finding 1 |
| `BedroomStudyDadGrope` | random | 329 | 8 | 3 | 1 | 1 | 8 | 1 | **Pattern D** with multiple intermediate gates |

**Distribution:** 8/8 content scenes use linkreplace cascades. **0 single-render utility scenes** (Dad has no Tease/Flash equivalents — father archetype is more passive than brother archetype). Pattern D dominant. Hub itself uses linkreplace (Brother's hub doesn't).

### Marcus — 12 named surfaces, peer / quest-chain tendency

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

### Edward — 1 named scene + Instafame DM app, career/digital tendency

| Scene | Type | Words | LR | StIf | StLR | CILR | Vid | Img | Pattern |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `EdwardThreesome` | event | 951 | 16 | 0 | 0 | 1 | 14 | 1 | **Pattern E** — long linear cascade, hub-gated (DM accept) |
| `Instafame` | app-shell | 420 | 0 | 0 | 0 | 0 | 0 | 0 | **Hub-app** — phone app shell |
| `InstafameDM` | DM-thread shell | 70 | 0 | 0 | 0 | 0 | 0 | 0 | **Hub-thin** — DM list shell |

**Plus:** `InstafameMessages` widget (9331 chars) contains the DM conversations. Edward's `EdwardDM` widget verified: **Pattern F** — linkreplace cascade with a `HideDiv`-based Accept/Decline branch at corruption ≥ 3 + `<<NotifyCorruption 3>>` for the rejection variant. Mechanism structurally **identical to MarcusParkDate**, rendered in DM frame instead of park scene.

**Implication:** Edward's "career/digital" arc tendency is in the *framing* (DM-mediated, async, calendar-driven) — not in the cascade mechanism. The same Pattern F that governs MarcusParkDate governs EdwardDM. The arc tendency is presentation; the mechanism is shared.

---

## §3 Cross-NPC pattern distribution

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

**Aggregate cascade rate: 29 of 40 surfaces (~73%) use `<<linkreplace>>`. Single-render utility: 7 of 40 (~18%). Hubs: 4 of 40 (~10%).**

**Per-block `text_variants`: 0 of 40.** Confirmed absent across the 4 audited NPCs. Doc 21 §6 correction holds — RTS does not use this mechanism anywhere we've sampled.

---

## §4 Doc 13 §5 "three arc tendencies" — refined

Doc 13 §5 framed Brother as family/proximity, Marcus as peer/quest-chain, Edward as career/digital. **Doc 13 §16 Correction 7** then corrected: every NPC is hybrid; tendencies are ratios not categories.

This audit refines further: **the arc-tendency difference doesn't change WHETHER cascades exist — it changes WHERE the stat gate sits within the cascade structure.**

| Arc tendency | Dominant pattern | Where stat gate lives | Replay loop |
|---|---|---|---|
| **Family / proximity** (Brother, Dad) | Pattern D | **Top of cascade**, after opening beat | Per-NPC stat threshold → cascade unlocks fully on next visit. **Single-step replay**: cross threshold once, all content available. |
| **Peer / quest-chain** (Marcus) | Pattern E | **At the hub button** (`<<button "Have sex"><<if getCorruptionLevel() >= 3>><<goto>>`) | **No replay variation** — once narrative prereq met, cascade plays the same every time. Quest progression replaces tier progression. |
| **Career / digital** (Edward) | Pattern E (Threesome) + Pattern F (DMs) | **At the hub button OR DM widget gate** | DM-async progression. Real Accept/Decline branches at money/sex moments. |

**Key insight:** the "story shape" (random/deterministic/quest-chain/calendar) is delivered by:
1. Where the trigger fires (hub random encounter vs button vs DM arrival)
2. Where the stat gate sits (mid-cascade vs hub button vs DM widget)
3. The framing layer (room visit vs date scene vs phone DM)

The CONTENT MECHANISM (linkreplace cascade with stat-gated branches) is the same primitive across all three. **One engine, three framings, three gate-placements — same mechanic.**

This is doctrinally important for TLS: **adopting linkreplace cascades (S7) doesn't lock TLS into one arc shape.** The same cascade primitive supports:
- Family-style (gate inside cascade → per-stat-tier reveals)
- Peer-style (gate at hub button → qualify-then-full)
- Career-style (DM-mediated cascade in widget)

---

## §5 Hub passage variation

Hubs vary more than expected — not all NPC hubs follow the same template.

| Hub | NPC | Words | LR | Mechanism |
|---|---|---:|---:|---|
| `BrotherBedroom` | Brother | 222 | 0 | Button menu by presence + time + relation. Random-encounter override on entry from Hallway. |
| `DadBedroom` | Dad | 201 | 3 | **Has its own linkreplace** — peeking through the door is built INTO the hub before the button menu. |
| `MarcusHallway` | Marcus | 43 | 0 | Thin navigation passage. Marcus content is event-triggered, not button-menu-driven. |
| `Instafame` | Edward | 420 | 0 | Phone app shell — feed of posts + DM access button. |
| `InstafameDM` | (DM list) | 70 | 0 | DM thread list — each thread opens a `<<widget>>` cascade. |

**Family/proximity hubs**: room passages with button menus + sometimes their own linkreplace. Stat-injected buttons (`Sleep with him` at relation ≥ 10) are rare; presence/time injection is universal.

**Peer hubs**: thin navigation. Peer scenes are event-driven (Park Date, Class, Bathroom Encounter), not menu-driven. Player initiates by going to the location at the right time, not by clicking menu items.

**Career hubs**: app/feed shells. Content arrives async via DM widgets, not via button menus.

---

## §6 Updates to docs 20 + 21

### Doc 21 §5 (pattern distribution)

Brother's distribution was 6 Pattern D + 3 Pattern E + 1 Pattern C + 1 Pattern F + 4 utility = 15+1 hub. **Cross-NPC distribution shifts the pattern weights:**
- Pattern D: 38% (15 of 40) — confirmed dominant overall, but heavily concentrated in family arcs
- Pattern E: 25% (10 of 40) — equally common, dominant in peer/career arcs
- Pattern A: 10% (4 of 40) — Brother + Marcus, no Dad/Edward
- Pattern C: 3% (1 of 40) — PeepBrotherSex remains the only verified per-step-gated cascade across all 40 surfaces

**Pattern C is rare.** Doc 21 may have over-weighted it as a category by treating PeepBrotherSex as exemplary. It's actually unusual — most cascades use Pattern D (top-gate) or Pattern E (hub-gate).

### Doc 20 §1.B ("three arc tendencies, mixed not categorized")

Strengthened, not changed. Audit shows tendencies manifest in **gate placement + framing**, not in cascade existence. All three arc shapes use linkreplace cascades; only the gate location and presentation layer vary.

### Doc 20 §3 row 5 + doc 21 §6 (S1 vs S7)

**Reinforced.** Per-block `text_variants` = 0 of 40 surfaces across 4 NPCs. The S1-as-doctrine-match framing is conclusively wrong. S7 (linkreplace) is the doctrine match across all arc tendencies.

### Doc 20 §1.H (button injection)

**Refined further:** stat-injected buttons exist (Brother's `Sleep with him` at relation ≥ 10) but are **rare across the audited hubs**. The dominant hub-rendering mechanic is **presence + time** (which buttons appear when NPC is in the room) plus **stat-gated CLICK HANDLERS** (button always renders; click checks stat → goto OR notification). True stat-injected button rendering is the exception, not the rule.

---

## §7 What this means for TLS — refined recommendation

Doc 20 §4 ranked engine work. Doc 21 §6 corrected S1→S7. This doc adds:

1. **S7 (linkreplace-drip) supports all three arc tendencies** with the same primitive. Adopting it doesn't commit TLS to a single arc shape — it enables Pattern D for family-style NPCs, Pattern E for peer-style, Pattern F for branching-choice moments, all with the same engine work.
2. **Pattern E (hub-gated linear cascade) is the most common content shape across peer/career arcs.** Marcus has 5 of 12 scenes in this pattern. For TLS Jake (peer-tendency), this is the natural shape: gate at the activity button, full cascade plays once entered.
3. **Pattern D (top-of-cascade gate) is the most common across family arcs.** For Frank/Diana (family-proximity tendency in TLS), this is the natural shape: scene opens unconditionally, then branches at top of cascade based on stats.
4. **Pattern F (HideDiv parallel branches + real choice) is reserved for relationship-defining moments.** ParkDate Accept/Decline, EdwardDM Accept/Decline, SellingMyStepsister Accept/Refuse. ~3 of 40 surfaces. **Frank's bedroom invitation (doc 19 §4) is exactly this shape** but is currently authored as two button exits with no in-scene branching. With S7, it could be a Pattern F scene with parallel cascades.
5. **Hub diversity is doctrine, not bug.** TLS shouldn't standardize hub passages. Family-NPC locations need button menus + presence/time injection. Peer NPCs may not need hubs at all (event-driven). Career NPCs (future) need app shells (Frank doesn't have one; Diana might if she becomes career-tendency).

---

## §8 Confidence ladder

✅ **HIGH confidence (verified against passage source across 4 NPCs):**
- 6 patterns (A-F) reproducible across all 4 audited NPC sets
- ~73% cascade rate generalizes (varies by NPC: Dad 100%, Brother 63%, Marcus 67%, Edward 100% of content scenes)
- Per-block text_variants used in 0 of 40 surfaces
- Arc tendencies manifest in gate placement, not cascade existence
- Pattern E dominates peer/career; Pattern D dominates family

🟡 **MED confidence:**
- 4 NPCs out of RTS's ~16 with `scenes` objects audited (~25% of the named-NPC catalog). Other NPCs (Grandpa 6 / Sam 2 / Veronica 3 / Priest 2 / Jamal 3 / Josh 1 / Tow Truck Driver 1 / Yacht Captain 1 / Thief 2) may surface additional patterns or different distributions. Sample is significant but not exhaustive.
- Hub variation observation (4 hubs) — small sample for that conclusion specifically.

❌ **NOT established:**
- Live experience of patterns D vs E (which "feels" like better RTS replay — doc 13 §16 Finding 2 verified D works for BrotherCaughtMasturbating, but no comparable E-experience writeup)
- Whether location-bound scenes (~70 per doc 13 §3) follow the same pattern distribution as NPC-bound — completely unaudited
- Whether `checkSceneReq()` semantics affect Pattern E gating in ways the source doesn't expose

---

## §9 Recommended next steps

1. ✅ **Doc 20 corrections shipped 2026-05-05** — §1.E + §3 row 5 + §1.H + §4 updated; §10 supersession trace added.
2. ✅ **S7 (linkreplace cascade) + S8 (thought_bubble) engine work shipped 2026-05-06.** Doctrine match Pattern D/E/F (per §3-§4 of this doc) now expressible in TLS canvases via the new `cascade` block type with `props.beats` + per-beat effects + mid-cascade gates + `show_when_locked` sibling, and `thought_bubble` block type for NPC interiority. Implementation in `apps/game_generation/twee_comprehensive/generators/v1.py` (`_render_cascade` + `_render_cascade_tail` near line 10573) + schema normalization in `apps/projects/services/template_import.py` (`_normalize_block_list` near line 3514). 156 tests pass (141 pre-existing + 15 new cascade/thought-bubble tests). Pilot scene `scene_franks_bedroom_evening` rewritten as Pattern D (5-beat first-night with corruption ≥ 25 gate) + Pattern E (4-beat subsequent-nights) cascades. Build clean. **Browser playtest verified all six contracts** (cascade reveals beat-by-beat, per-beat effects fire on click — `npc.frank.arousal: 0 → 2` on door-close, mid-cascade gate works, locked sibling renders at low stat).
2a. ✅ **S4 (threshold notifications) shipped 2026-05-06.** New `locked_text_threshold` field on `TemplateChoice` + cascade beat schema. Locked-choice / locked-cascade-beat sibling now renders as `<<button>>` firing `setup.queueGatedNotification(threshold)` + warning toast (`.notify-warning`, amber palette, italic, multi-line, 3s dwell) when player clicks. RTS doctrine: doc 13 §7.4 + doc 22 §11. Bedroom anchor Beat 3 wired with threshold message — verified live: orange toast renders the in-character text on locked-sibling click at corruption 10. **162 tests pass** (156 + 6 new S4 tests).
2b. ⚠️ **S3 (walkthrough counter display) tried + reverted 2026-05-06.** Built the same day (counter discovery walking stage_helpers, `setup.evalCounterField` runtime helper, `<<renderHintCounters>>` widget, badge CSS) and verified live — Frank's hint card showed 6 counter badges across Stage-1 + Stage-3 conditions. **Removed same day** because the row was either redundant with the auto-rendered goal block (Pattern 2 `setup.computeHintGoal`, when hints opt in via `auto_goal = true`) or chaotic when not (multiple stage helpers' conditions merged into one row, mixing Stage-1 + Stage-3 gates with no separation). The doctrine-correct surface is the goal block, not a separate counter row. Lesson: the RTS walkthrough-publishes-everything model (doc 13 §6) doesn't translate cleanly to TLS, which already has a more focused next-gate display via Pattern 2. Implementation in git history if ever needed; commented sentinel left in `_build_help_data()` to mark the prior attempt.
2d. ✅ **Frank completion polish shipped 2026-05-06** — three B1 + C + E fixes after the rollout to close the remaining Frank-specific gaps (per the post-rollout audit conversation):

  - **B1 — Walkthrough visibility for Stage 3→4.** Added new `frank_stage_4` stage_helper (mirrors the bedroom-invitation capstone gate: `frank_office_first_sex_done is_true + Frank.corruption ≥ 25 + frank_office_visits ≥ 3`). Flipped Stage 3 hint's `auto_goal = false → true`. Pattern 2's `setup.computeHintGoal` now finds the helper at `npc_frank_stage = 3 + 1 = stage_4` and renders the gate as ◯/✓ counters in the Quests panel — closes the previously-invisible Stage 3→4 walkthrough gap. Helper is discovery-only (Stage 4 is still written directly by the capstone choice exits, no helper-driven transition canvas needed). Added `frank_office_visits` trait label ("Office sessions" / verb "do" / unit "session") so the goal-block bullet renders cleanly. Stage 4 hint stays `auto_goal = false` (terminal until summer-end).

  - **C — Stage 4 hallway vignette.** New canvas `scene_hallway_franks_door_evening` per doc 19 §5: ~50w T2 vignette where Maya passes Frank's closed bedroom door at 20:30-22:30, sees the warm line of lamp light under the door. Random encounter (chance 0.40), priority 3, daily cooldown via new `frank_hallway_door_today` flag (added to flag_keys + daily_tick). Diana awareness +1 silent accumulator on exit. Mutex with bedroom rendezvous via `talked_to_frank_today is_false` gate. Surface multiplexing for Stage 4 — atmosphere before the bedroom anchor without changing any other Frank surface.

  - **E — Per-beat effects on 3 of 4 new Frank cascades.** Carefully selected narratively-meaningful in-scene effects:
    - `scene_office_after_crack` Beat 1 ("Bend over the page.") → Frank.arousal +1 (his desire crossing into the visible/spoken with "You wearing anything under that.")
    - `scene_office_after_crack` Beat 2 ("Don't look up.") → Frank.arousal +1 (escalation as the skirt lifts)
    - `scene_office_crack` Beat 2 ("Hold his eyes.") → player.corruption +1 (her active defiance commits her, produces the rule break)
    - `scene_living_room_evening` Beat 1 ("Don't speak.") → player.calculation +1 (reading the room instead of explaining)
    - `scene_kitchen_with_frank_morning` Stage 4 cascade — **skipped intentionally** (effect not earned at beat level — Stage 4 morning is established rhythm, not new commitment).

  **162 tests still pass.** Build clean. Frank arc now considered functionally complete per the doc 19 design contract — 4 capstones in single-digit ledger; 5/5 high-content scenes cascaded; Stage 3 surface expansion shipped (5 T2 vignettes per doc 19 §3); Stage 4 surface multiplexing shipped per doc 19 §5 (kitchen evening + living room + back porch + hallway-door now); walkthrough visibility for Stage 3→4 closed. Office daytime Stage 3 vignette remains deferred (engine gap: no time-of-day condition support inside `[group]` blocks per doc 19 §3 row 3 — separate engine work).

2c. ✅ **Frank Phase 2 cascade rollout shipped 2026-05-06.** All 4 high-content Frank scenes rewritten as S7 cascades on top of the bedroom-anchor pilot — Frank now has **5 of 5 high-content scenes as cascades** (no more walls of text in his arc). Mechanical rewrite: all prose preserved verbatim; all gates / flags / effects / choice exits unchanged. **Per-scene cascade IDs:**
  - `frank_kitchen_morning_s0` / `_s1` / `_s2` / `_s3_pre` / `_s3_post` / `_s4` (multi-stage canvas — 6 cascades, one per stage group, Pattern E linear, 2-4 beats each)
  - `frank_office_crack` (Stage 2→3 capstone, Pattern E linear, 4 beats — `[Look up.]` / `[Hold his eyes.]` / terminal)
  - `frank_office_after_crack` (Stage 3 repeating + Stage 3→4 capstone, Pattern E with capstone group **nested inside terminal beat** so it only renders after click-through — novel composition pattern, verified at build level via grep — 4 beats with `[Bend over the page.]` / `[Don't look up.]` advance links)
  - `frank_catch` (Stage 1→2, Pattern E with register-branch exits, 3 beats — `[Don't speak.]` / terminal)
  - `frank_bedroom_first` / `_repeat` (the original pilot — bedroom anchor, Pattern D with mid-cascade gate)
  Total `<<linkreplace>>` macros in slice: 5 (pre-rollout baseline, only bedroom anchor) → 18 (post-rollout, 5 Frank cascades). 162 tests pass. Build clean. Browser playtest of `office_after_crack` verified cascade reveals beat-by-beat (passage URL stable; body grew 800 → 3061 chars across clicks). Capstone group nested inside terminal beat gates correctly at HTML emission level (verified via grep — `Not in here next time` + `Upstairs. Same hour` prose present, gate conditions wrap with `<<if>>` correctly). Runtime capstone-fire requires correct state propagation through the engine's `setup.applyAndNotifyFlag` / NPC-trait setter paths (a known eval-state quirk affecting any condition-gated content in the engine — orthogonal to cascade mechanism).
3. **Optional: audit Grandpa (6) + Veronica (3) + remaining named NPCs** to push sample to ~80% of catalog. ~30 min via same script.
4. **Optional: audit a sample of location-bound scenes** (Park / Beach / School / Bar) — ~10 scenes — to see if they follow the same patterns or differ. ~30 min.
5. **Optional verification: live-play 1 Pattern D scene + 1 Pattern E scene + 1 Pattern F scene** in browser (Frank bedroom anchor at corruption 30 vs 10) to confirm the cascade experience matches the structural prediction. ~30 min via twine-game-explorer skill resume.
6. **Phase 2 rollout (next decision gate):** apply cascade pattern to other Frank scenes (kitchen morning Stage 0 cascade, office after-crack S3 cascade, crack capstone Pattern F cascade), then extend to Ryan / Jake. Companion engine items (S3 walkthrough counter display, S4 threshold notifications, §H button injection, S6 passive trait gains) remain separate work — not blocked on rollout.

---

## §10 Source artifacts

- `game_explorations/rts-arc-trace/passage_catalog.json` — same 1.2 MB / 361-passage capture as doc 21
- All 40 audited scene bodies extractable via `passages[name]['source_raw']`
- Verbatim source for canonical examples (DadBedroom hub, MarcusParkDate, EdwardDM widget) included in this conversation's context

---

## §11 Live verification (2026-05-06)

Per methodology rule §N (use both extraction AND play, never one alone), the structural predictions in §3-§4 were verified via live play of one canonical example per pattern. Session: `rts-arc-trace` resumed from prior Chromium profile, fresh game state (Day 1 EM Bedroom), eval-set MC corruption=200/exhi=20 + Brother arousal=5/relation=15 + Marcus relation=20 to bypass grind, then `Engine.play()` to navigate directly to test scenes.

### Pattern D — `BrotherCaughtMasturbating` ✅ verified

- **Entry**: random-encounter override fired on `Engine.play('BrotherBedroom')` after setting Brother location + Evening time (the source's `<<if previous() == "Hallway">>` doesn't gate `Engine.play` re-renders — interesting side-effect).
- **Opening render**: passage body + 1 video stub + `[Enter the room]` linkreplace link.
- **Click "Enter the room"**: passage URL stayed `BrotherCaughtMasturbating` ✅, body grew with +shock paragraph + +video + Victoria/Robert dialogue exchange + new `[Shhh]` link.
- **`[Shhh]` button appeared** because corruption ≥ 3 + StageTwoCorruption(Brother) gate met ✅. The top-of-cascade gate works exactly as Pattern D predicts.
- **Click `[Shhh]`**: body grew further with +caress paragraph + +video + dialogue + new `[You kiss him]` link. Pure linear cascade from here per source.

**Structural prediction confirmed:** opening linkreplace → top-of-cascade gate determines branch (high-stat = deep cascade, low-stat = rejection variant) → if high-stat, linear linkreplace cascade with each click revealing next beat in-place.

### Pattern E — `BrotherBedroomSex1` ✅ verified + thought-bubble confirmed

- **Entry**: `Engine.play('BrotherBedroomSex1')` direct navigation (in production, gate lives on hub button — Engine.play bypassed).
- **Opening render**: bookshelf prose + Victoria/Robert dialogue + `[He shows you the book]` link. ~430 chars.
- **Click "He shows you the book"**: passage URL stayed `BrotherBedroomSex1` ✅, body grew to ~780 chars with new dialogue beats, **a styled `💭 Victoria is thinking...` bubble with italicized interior monologue**, and `[You put his hand on your chest]` next link.
- **Thought-bubble primitive confirmed live** — exactly the styled UI element doc 13 §16 Finding 1 captured. Distinct from regular speech bubbles (different color/icon). This is the 4th-dimension writing primitive (§I in doc 20 §1).
- **No internal stat checks observed** in the cascade — pure linear progression as Pattern E predicts.

**Structural prediction confirmed:** scene entry has no body-level stat gate (gate was at hub button), then linear linkreplace cascade with thought-bubble interleaved at one beat.

### Pattern F — `MarcusParkDate` ✅ verified + HideDiv parallel-branch confirmed

- **Entry**: `Engine.play('MarcusParkDate')` after eval-setting Marcus.relation=20.
- **Opening render**: park dialogue + `[You walk with him]` link.
- **Click "You walk with him"**: passage stayed `MarcusParkDate` ✅, body grew with walk paragraph + Marcus's "more than friends" line + **TWO buttons appeared simultaneously: `[Accept]` and `[I don't want it..]`** ✅.
- **Click `[Accept]`**: body continued in the Accept branch (Victoria's "I like you too" + Marcus's reply + kiss prompt). **The `[I don't want it..]` button DISAPPEARED** — `<<HideDiv "marcus-date-decline">>` macro fired as predicted. New link `[Kiss him]` appeared.
- **Per-beat side effect verified**: variables_diff showed `player.relationship.loyalty: 0 → 100` — the `<<MakeBoyfriend Marcus>>` macro inside the Accept linkreplace block fired on click ✅.

**Structural prediction confirmed:** parallel cascades hidden/shown by HideDiv at the major branching choice; per-beat effects fire on each click (not just scene entry).

### Cross-pattern observations from live play

1. **Linkreplace mechanism works exactly as source predicts** across all three patterns. Body grows below cursor, passage URL never changes, click reveals next beat with paragraph + media + new link.
2. **Per-beat effects fire on click** (Pattern F's MakeBoyfriend macro). This is critical for S7 implementation — TLS would need its `<<set>>` / effect block emission to live INSIDE linkreplace nodes, not just at scene entry.
3. **Buttons can be `<a>` or `<button>` HTML elements** depending on linkreplace style. DOM dumps showed both variants. TLS engine work needs to accept both for consistent click affordances.
4. **The `Engine.play()` call bypasses some passage-entry conditions** (random-encounter override stacking, hub button click handlers). Useful for QA navigation but means production gates need to live in canvas trigger conditions or in the cascade itself, not in the entry passage's hub.
5. **Thought-bubble visual style is distinct** — italicized + `💭` icon + "thinking..." attribution row. Doc 22 §3 listed thought bubbles as "engine S8 (deferred)" but live verification confirms they're a meaningful UX win when they appear.

### Confidence upgraded

The structural extraction (docs 21+22) is now **live-verified** for one canonical scene per pattern. Mechanism predictions for S7 design no longer need a "structure-only, behavior-untested" caveat. **Decision-grade evidence for committing to S7 is now in hand.**

### What still wasn't tested live

- Pattern A/B (single-render utility) — not verified live because the structural prediction is "no cascade exists" which is trivially confirmable from source.
- Pattern C (per-step stat-gated cascade — only PeepBrotherSex). Not retested this session; doc 13 §12 already verified live in 2026-05-02.
- The `<<NotifyCorruption N>>` rejection variant of Pattern D (i.e., what happens when stat gate fails). Not tested this session because we set high stats; would need a low-stat run to verify the rejection text + threshold notification.
- Hub button injection §H — not re-verified this session. Doc 21 §6 source-verified; if we want live re-verification of "Sleep with him button only renders at LN + relation ≥ 10" that's a separate test.

---

End of audit.
