# 17 — Phase 1 Pre-Playtest Audit: RTS Alignment Review

> **Created 2026-05-03.**
> Honest review of the Phase 1 Frank pilot work (Steps A→C complete) against RTS principles documented in `13_Road_to_Success_Reference.md` and `15_Sandbox_Pivot_Direction.md`.
> Conducted BEFORE Step D playtest, so we know going in what we expect to validate vs what we know we're missing.
> **Status: 🟦 captured.** Not a redesign doc — a snapshot of where the pilot stands relative to the RTS target so future sessions don't mistake "Phase 1 shipped" for "fully RTS-aligned."

---

## §0 Why this doc exists

After Step C completed (all 6 new sandbox scenes + Stage 4 polish + catch Tier-3 polish + engine bug fix), we ran an honest review of the work against the RTS target before playtest. The review surfaced specific wins, partial alignments, and gaps. **Without capturing this here, the playtest results will conflate "Frank pilot shipped" with "Frank pilot is fully RTS-aligned," and we'll miss the gaps that explain *why* certain things feel off (or why they feel surprisingly good).**

Read this doc:
- BEFORE Step D playtest — so you know what to look for
- AFTER Step D playtest — to triage which gaps actually mattered
- BEFORE expanding sandbox to Diana/Marge/Ryan/Jake — so the same gaps don't propagate

---

## §1 What we audited

**Phase 1 work done (Steps A→C, 2026-05-03):**

- Step A: Doctrine doc updates (`feedback_tls_scene_body_style.md` Tier-3 carve-out + `02_NPC_Stage_Chains.md` capstone-layer note)
- Step B: 3 sample scenes (#5 hallway / #9 talk-to-Frank / #3 catch Tier-3 polish)
- **Engine bug fix** (`template_import.py` group/block_pool props-nesting, 4-place patch) — pre-existing bug that silently broke ALL group-block content
- Step C: 5 new scenes + Stage 4 polish (#6 coffee alone / #7 living room radio / #8 porch evening smoke / #10 chores activity / #11 LN kitchen raid Tier-3 + Scene #1 Stage 4 cracked-summons polish)
- New daily-reset flags wired into `[engine.daily_tick]`

**Frank now has** (4 existing + 6 new = 10 total surfaces, vs RTS Brother's 15):
- 4 random ambient scenes (#5/#6/#7/#8)
- 2 player-initiated deterministic (#9 talk / #10 chores)
- 1 time-gated rare Tier-3 (#11 LN raid)
- 4 existing stage cascade scenes (kitchen morning, kitchen dinprep, office supervised, living room catch — preserved)
- 4 existing crisis priority hint variants

**What we audited against:** the 10 RTS principles from doc 15 §6 + the 5+ corrections from doc 13 §11/§16 + the doctrine carve-outs from doc 16.

---

## §2 Solidly aligned with RTS (7 items) ✅

These principles are demonstrably implemented in the new content. Verified via TOML inspection + compiled HTML render checks.

### §2.1 Day 1 content with no MC stat gates ✅

All 4 ambient scenes (#5/#6/#7/#8) have only `arrived_at_franks` flag + per-scene daily cooldown + chance roll as trigger conditions. **No MC corruption / exhibitionism / arousal entry gates.** Player at corruption 0 can encounter any of these on Day 1.

| Scene | Trigger conditions | MC stat gate? |
|---|---|---|
| #5 Hallway pass | location + N band + chance + cooldown + arrived_at_franks | ❌ none |
| #6 Kitchen coffee alone | location + EM band + chance + cooldown + arrived + npc=frank | ❌ none |
| #7 Living room radio | location + A band + chance + cooldown + arrived + npc=frank | ❌ none |
| #8 Porch evening smoke | location + E band + chance + cooldown + arrived + npc=frank | ❌ none |

### §2.2 Same scene, different reveal at different stats ✅

Every ambient scene has 3 tier branches via `[group]` blocks. Higher Frank.trust → more content renders within the same canvas. Verified live in compiled HTML — content IS in the scene body, not in a separate canvas per tier.

| Scene | Tier branches by Frank.trust |
|---|---|
| #5 Hallway pass | < 5 (Tier-1) / 5–14 (Tier-2) / ≥15 (Tier-2+) |
| #6 Kitchen coffee alone | < 10 (Tier-2) / 10–19 (Tier-2) / ≥20 (Tier-2+) |
| #7 Living room radio | < 10 / 10–19 / ≥20 |
| #8 Porch evening smoke | < 5 / 5–14 / ≥15 |
| #9 Talk to Frank | 4 branches: low/mid/high trust × Stage 0-1, plus Stage 2+ |
| #11 LN raid | < 15 (Tier-3 brief) / ≥15 (Tier-3 full) |

### §2.3 Three writing tiers used deliberately ✅

| Tier | Frank scenes | Approx word count |
|---|---|---|
| Tier-1 utility | Activity #10 chores | ~40 words |
| Tier-2 vignette | Most ambient scenes (#5-8 mid+, #9 low/mid/Stage 2+) | 30–100 words per branch |
| Tier-3 character | Scene #11 LN raid (~250), Stage 4 polish (~200), catch polish (~270), Scene #9 high-trust peppermint (~120) | 200–600 words |

**4 Tier-3 surfaces total** (3 from new work + 1 polish). Reserved for capstones and high-stakes moments per doc 16 §4 doctrine.

### §2.4 Mix arc shapes per NPC — Frank now hybrid ✅

Frank is no longer pure deterministic quest-chain. He now has all four trigger types:

| Trigger type | Surfaces |
|---|---|
| Random ambient | 4 (#5, #6, #7, #8) |
| Player-initiated deterministic | 2 (#9 talk, #10 chores) + existing bookkeeping + existing morning chore |
| Time-gated rare | 1 (#11 LN raid) |
| Stage capstones (existing) | 4 (kitchen morning cascade, dinprep cascade, office supervised cascade, living room catch) |
| Crisis priority hints (existing) | 4 |

### §2.5 Real choice for stakes moments ✅

Real branching reserved for the moments that warrant it:
- **Scene #11 LN raid:** `[Stay a while longer]` (+2 trust, +1 hour) vs `[Go back to bed]` (+1 trust, +30 min). Different effects.
- **Scene #3 catch (existing, preserved):** `[Stay where you are]` (+3 corruption, +5 Frank arousal) vs `[Stand up. Go to your room]` (+1 corruption, +3 Frank arousal). Same flag effects (catch fired either way).

Routine ambient scenes have single exit choices (`[Continue.]`, `[Excuse yourself.]`) — appropriate for low-stakes texture.

### §2.6 NPC trait integer (not emoji) ✅

All trust conditions use `{ type = "trait", subject = "npc", npc_id = "npc_frank", trait_key = "trust", operator = "gte", value = 15 }` integer comparison. Confirms doc 13 §11 finding 4 (NPC arousal/trust stored as integer, emoji is display-only).

### §2.7 Voice consistency across 6 new scenes ✅

Spot-checked Frank's voice samples:
- "Coffee's there." (terse, gesture-as-statement)
- "You're up." / "Couldn't sleep?" (statement-as-question, no real interest)
- "Best part of the day." (brief opinion shared at high trust)
- "Quiet feet. People who sleep make more noise." (observation + character in 9 words)
- "Bought this property in '79..." (factual sharing, no emotional declaration)
- "Maya." (Stage 4 — one word lands, dropped pretense)
- "Come sit." (Stage 4 — two words, no please, no qualifier)

No drift. Frank reads as the same character across all 6 scenes + the polish.

---

## §3 Partially aligned — functional but not 1:1 with RTS (5 items) 🟡

These principles are addressed but with caveats. Functional for the pilot but worth knowing the gap.

### §3.1 Tier-branching axis: NPC trust vs MC corruption 🟡

**RTS pattern:** Higher MC corruption reveals more content within scenes (`BrotherCaughtMasturbating` short at MC corruption 6, full sex scene at MC corruption 31).

**TLS pilot:** Higher Frank.trust reveals more content. Player builds NPC trust by interacting with Frank — different axis but same effect (player invests stat → unlocks deeper content).

**Trade-off:** NPC trust is less directly grindable than MC corruption. RTS's "masturbate to raise corruption" is a generic stat any player can grind. TLS's "raise Frank trust" requires Frank-specific interactions (bookkeeping, talk, chores). More narrative, less abstract — but also slower for a player who wants to push through Frank's content quickly.

### §3.2 Rejection variants in 100% chance scenes 🟡

**RTS pattern:** `SleepingBrother` is "100% chance" but plays a 134-word *rejection* outcome at low relation. Same scene mechanically fires, but content is a soft no.

**TLS pilot:** Scene #11 LN raid low-trust branch ends with Frank shutting down ("Get some sleep" — only the only thing he's going to say tonight). Activity #9 Stage 2+ branch has cooler tone ("Talking's fine. Door stays open" — conversation cuts off).

**Gap:** We have softening, not full rejection. RTS's rejection is more clearly a "no, come back at higher stats" signal. Ours is more "this is a less-warm version of the same thing." Functional but less crisp signal to the player about what they're missing.

### §3.3 Story at scene level vs arc level 🟡

**RTS pattern:** ~130 micro-stories per game (~15 per dense NPC). Each scene works standalone. No per-NPC narrative throughline.

**TLS pilot:** Frank now has 10 surfaces. ~67% of RTS Brother's density (15). The 4 existing stage cascade scenes still anchor an arc spine (Stage 0→1→2→3→4) — we added daily texture around it but didn't replace it.

**Trade-off:** TLS reads as "stage chain + ambient layer," not "scattered scene library." This is doctrinally intentional per doc 15 §7 — stages stay as capstones. But RTS's no-spine model produces a different feel: the macro-story emerges from scene sequencing rather than from authored arc. **Whether this matters depends on Step D playtest.**

### §3.4 Gates compose without rigid arc spine 🟡

**RTS pattern:** Each scene's gate is independent. No central stage ladder.

**TLS pilot:** New scenes' conditions ARE independent (each has its own trigger gate set). But the existing stage cascade still uses `npc_frank_stage` as a strong axis below the new scenes.

**Gap:** The new layer is sandbox-style; the underlying layer is stage-chain-style. Mixed model. Reads correctly per doc 15 (capstone + texture layers coexist) but isn't pure RTS.

### §3.5 Day 1 reachability of ambient scenes 🟡

| Scene | Day 1 reachable? | Why |
|---|---|---|
| #5 Hallway pass (N band 21:30-23:00) | ✅ Yes | Player typically at home in evening |
| #6 Kitchen coffee alone (EM 05:30-06:29) | ✅ Yes | Game starts in EM, kitchen is right there |
| #7 Living room radio (A 14:00-16:00) | ⚠️ Mostly no | Day 1 player typically at school in afternoon |
| #8 Porch evening smoke (E 18:30-18:59) | ⚠️ Maybe | Narrow 30-min window, may be missed in Day 1 routine |

**Risk:** Only 2-3 of the 4 ambient scenes are reliably Day-1 reachable. Real risk for the playtest: if scene #7 and #8 don't fire on Day 1, the "Day 1 ambient content fires" property may be partially false.

**Mitigation options if playtest confirms the risk:** (a) bump chance to 50-60%, (b) widen time windows, (c) add more ambient surfaces in the player's actual Day 1 path.

---

## §4 Missed entirely — deferred to Phase 2 / Phase 3 (5 items) ❌

These were KNOWN missing per doc 14 — they're explicitly Phase 2 or Phase 3 engine work, deliberately not built in Phase 1. Listing them here so the playtest results are interpreted in context.

### §4.1 Counter-thresholds visible in player UI ❌ (Phase 2 — S3)

**RTS pattern:** Walkthrough panel publishes literal counter values ("Frank bookkeeping: 1/3").

**TLS pilot:** New flags (`frank_hallway_pass_today`, `helped_with_chores_today`, etc.) and `frank_chore_count` from activity #10 are NOT surfaced in Quests panel. Player can't see "how close they are."

**Why deferred:** Doc 14 S3 — explicit Phase 2 engine work (~25 LOC).

**Implication for playtest:** "Transparent walkthrough" RTS principle cannot be fully validated. Player will use new scenes blindly.

### §4.2 Threshold notifications on gated failed actions ❌ (Phase 2 — S4)

**RTS pattern:** Failed gated action shows notification with threshold ("30+ Corruption Needed").

**TLS pilot:** Activity #10 chores has Stage 1+ gate. At Stage 0, the activity simply doesn't appear (silent fail). No notification on attempt. Existing soft-fail pattern preserved.

**Why deferred:** Doc 14 S4 — Phase 2 engine work (~35 LOC).

### §4.3 Per-canvas executedToday (vs per-activity-name) ❌ (Phase 2 — S2)

**RTS pattern:** Each scene independently gated. Multiple scenes of same activity can fire same day.

**TLS pilot:** Each new scene uses its own daily flag (`frank_hallway_pass_today`, `frank_coffee_alone_today`, etc.) — so they don't share cooldowns. **But** existing kitchen morning + dinprep + bookkeeping all share `talked_to_frank_today`. Activity #9 talk also uses `talked_to_frank_today`, so it's mutex with all kitchen scenes.

**Practical effect:** Player who does bookkeeping (E band) cannot also talk to Frank that day. Conservative but possibly too restrictive.

**Why deferred:** Doc 14 S2 — Phase 2 engine work (~5-15 LOC).

### §4.4 Sidebar travel shortcuts ❌ (Phase 2 — S5)

**RTS pattern:** `🏫 Go to School` hard-coded sidebar button.

**TLS pilot:** Travel friction unchanged. Bedroom → Hallway → Kitchen still 2-3 clicks.

**Why deferred:** Doc 14 S5 — Phase 2 engine work (~15 LOC).

### §4.5 Linkreplace-drip multi-step scene structure ❌ (Phase 3 — S7)

**RTS pattern:** Click → reveal next paragraph → click → reveal video → click → next reveal. Scene unfolds page-by-page.

**TLS pilot:** All scenes are single-render. The full body renders at once on canvas entry.

**Why deferred:** Doc 14 S7 — Phase 3 structural work (~150 LOC + new SugarCube macro support).

**Implication for playtest:** Even our 250-word Tier-3 scenes feel like "popup with text" not "scene that unfolds." This is the **#2 biggest craft gap** between TLS and RTS feel. May need to revisit if Phase 1 playtest reveals scenes feel "static."

---

## §5 Missed entirely — could have done in Phase 1 (2 items) ❌

These are gaps we could have addressed within Phase 1 scope but didn't. Worth flagging so the next session catches them.

### §5.1 NPC interior thought bubbles ❌

**RTS pattern:** Styled `💭 Frank is thinking... <em>thought text</em>` bubble distinct from speech. Adds character interiority without bloating prose.

**TLS pilot:** Zero thought bubbles. We use 3rd-person narrator interpretation instead:
- ✗ Our pattern: *"He's not great at this. But he's trying."* (narrator interprets)
- ✓ RTS pattern: `💭 Frank is thinking... "I should say something to her. I don't know what."` (Frank's interior voice rendered as styled bubble)

**Why this is the #1 craft miss:** Doc 14 S8 specifies a new block type + CSS for thought bubbles (~50 LOC, Phase 3). Without that block type, we can't author them properly. **But** we could have at least used italicized 1-line interior monologue inside our Tier-3 prose to approximate the effect:
- *Could have done:* "She turned from the kettle. *He'd been waiting for her to turn.*"
- *Did instead:* "She turned from the kettle." (no interior cue)

**This is doctrinally weird** — our Tier-3 prose reads as good literary fiction but doesn't feel specifically RTS-flavored. The thought bubble is RTS's distinctive craft signature. Without it (or even an italicized substitute), we're producing different *kind* of writing than RTS, even though we're producing high-quality writing.

### §5.2 Cross-NPC bridge scenes ❌

**RTS pattern:** `SellingMyStepsister` gates on Brother corruption + Josh-not-unlocked. Once unlocked, transfers Brother arc INTO Josh arc. NPCs link via scene-flag dependencies.

**TLS pilot:** Zero cross-NPC bridges in the 6 new scenes. Each scene references only Frank state. Diana / Marge / Ryan / Jake state never referenced.

**What we could have done:**
- Scene #11 LN raid high-tier: Frank's monologue could have mentioned Diana's silence in the household ("Diana's been quiet lately. Doesn't say so but it weighs on her.") — establishes Diana state from Frank's POV, hints at cross-arc convergence
- Activity #9 high-trust: Frank could have asked about Maya's tutoring with Jake ("That brother of mine, the one who never comes out of his room. He been talking to you?") — cross-NPC bridge from Frank to Jake
- Scene #6 kitchen coffee alone high-trust: Frank could have mentioned the diner ("Marge says you've been pulling shifts. Honest work.") — references Marge state

**Why we missed it:** Doc 16 didn't explicitly require cross-NPC bridges in the per-scene specs. We followed the spec literally and produced isolated Frank scenes.

**Implication:** Frank still feels like a self-contained NPC, not part of an interconnected world. RTS's cross-NPC bridges are part of why "the world feels alive" — when Brother brokers a deal with Josh, the two NPCs feel genuinely related. Without bridges, our NPCs each have their own pocket dimension.

---

## §6 Unverified assumptions / risks (6 items) 🤔

Things we ASSUMED would work but haven't tested. Need playtest validation.

### §6.1 Frank's extended schedule is authorial intent, not engine-enforced 🤔

Doc 16 §3 specified Frank's location at each time band (e.g., Living room A 14:00-16:00 for scene #7). We assumed this. **The engine actually evaluates `npc = "npc_frank"` at trigger time** — if Frank's actual location (driven by the canvas system) doesn't match the scene's location at that time, the scene silently doesn't fire.

**Test in playtest:** Verify scenes #7 (living room A band) and #8 (porch E band) actually trigger. If they don't, Frank's schedule needs explicit canvas-driven enforcement.

### §6.2 Conservative chance values may be too low for Day 1 feel 🤔

Set 25-40% per scene. With per-scene daily cooldowns, a typical Day 1 has maybe 3-4 attempts per scene. Expected hit rate: 1-2 ambient scenes per day.

**RTS feels "Frank shows up unbidden 2-3 times a day"** — but RTS has more potential surfaces (more rooms, more time bands).

**Test in playtest:** Count ambient scenes that fire on Day 1. If <2, bump chances or add surfaces.

### §6.3 "One trust source per day" via shared `talked_to_frank_today` is restrictive 🤔

Activity #9 talk shares the flag with kitchen morning + dinprep + bookkeeping. So a player doing bookkeeping (E band) cannot also talk to Frank that day. RTS-style discipline — but might be TOO restrictive.

**Test in playtest:** Time how long trust 0 → 15 takes (Stage 0→1 gate) with the talk activity available vs without. If it doesn't speed things up meaningfully, the restriction is over-tight.

### §6.4 Scene #11 LN raid one-time-per-playthrough may be too rare 🤔

Player might never enter kitchen 22:00-22:59 in the slice. Once-per-playthrough also means no come-back-later validation.

**Test in playtest:** Force trigger via dev shortcut at trust 5 + Stage 1 to see the low-trust version, then trust 20 + Stage 1 for the high-trust version. Verify both render correctly.

### §6.5 Stage 4 polish only validates with dev shortcut 🤔

Per doc 16 §1 D3, Stage 3→4 natural content is deferred. Player won't naturally reach Stage 4 in the 10-day slice. Our Stage 4 polish only renders if user uses `dev_advance_frank_to_4`.

**Test in playtest:** Use dev shortcut to advance Frank to Stage 4. Visit kitchen morning. Verify Tier-3 polish renders (not the old dev-fragment).

### §6.6 No regression check on other existing scenes 🤔

Engine bug fix verified existing kitchen morning Stage 0 prose appears (`kettle was already cool` x1). But we didn't check Diana's awareness scenes, Ryan's yard scenes, Marge's diner scenes, Jake's hallway scenes — all of which use `[group]` blocks and were previously broken.

**Test in playtest:** Visit Diana scenes, Ryan yard, Jake hallway. Verify their stage-cascade prose renders (not "No content"). If any are still broken, they have a different bug pattern.

---

## §7 Scoring summary

| Category | Count | Notes |
|---|---|---|
| ✅ Solidly aligned with RTS | 7 principles | Day-1 access, tier-branching, writing tiers, hybrid trigger mix, choice-for-stakes, integer stats, voice consistency |
| 🟡 Partially aligned | 5 principles | NPC-trust vs MC-corruption axis, partial rejection variants, ~67% scene density, arc spine still anchors, mixed Day-1 reachability |
| ❌ Missed (deferred to Phase 2/3 by design) | 5 principles | Counter display, threshold notifs, per-canvas cooldowns, sidebar shortcuts, linkreplace |
| ❌ Missed (could have done in Phase 1) | 2 principles | NPC thought bubbles, cross-NPC bridges |
| 🤔 Unverified assumptions | 6 risks | Frank schedule, chance tuning, shared flag restrictiveness, scene #11 reachability, Stage 4 dev-only, existing-scene regression check |

**Net:** 7 wins / 5 partials / 7 misses (2 of which are on us, 5 are doc-14-deferred) / 6 untested assumptions.

---

## §8 Honest assessment

**The structural sandbox shift is correctly executed.** Frank is now a hybrid NPC with random ambient + deterministic + time-gated + capstones. Tier-branching works. Writing tiers used deliberately. Voice consistent. Engine bug that was silently breaking ALL group blocks across the slice is fixed.

**But this is sandbox-Frank-LITE, not full RTS-Frank.**

Two craft gaps stand out as the primary "doesn't feel exactly like RTS" sources:

1. **NPC thought bubbles** — RTS's distinctive UI primitive for character interiority. We have zero. Our Tier-3 reads as good literary fiction (3rd-person narrator interpretation) instead of RTS's specific NPC-thought-bubble texture. This is doc 14 S8 (Phase 3 deferred), but we could have approximated with italicized 1-line interior in our Tier-3 prose. We didn't.

2. **Linkreplace-drip** — RTS's IF-craft layer that converts "this block of prose" into "a chapter you turn pages of." Without it, even our 250-word Tier-3 scenes feel like "popup with text" not "scene that unfolds." Doc 14 S7 (Phase 3 deferred).

Both are explicitly Phase 3 deferred per doc 14. **This means Phase 1 playtest will validate the sandbox philosophy partially** — content access patterns, tier-branching, voice — **but cannot validate the full "feels alive like RTS" claim until Phase 3 is built.**

---

## §9 What playtest should explicitly look for

The Step D playtest (per doc 16 §19) tests three properties. Mapping them to the audit findings:

### Property 1: Day 1 ambient content fires within first 5–10 turns
- **What to look for:** Scenes #5/#6/#7/#8 firing during normal Day 1 play
- **Audit caveat:** Scenes #7 and #8 may not be Day-1 reachable due to player's school routine (§3.5)
- **Fail signal:** 0-1 ambient scenes fire → bump chance values or add surfaces (§6.2)
- **Pass signal:** ≥2 ambient scenes fire

### Property 2: Come-back-later loop works
- **What to look for:** Scene #5 hallway pass at trust 0 vs trust 15 — content visibly differs
- **Audit caveat:** Tier-branching uses Frank.trust not MC corruption (§3.1)
- **Fail signal:** Same content renders both times (means engine bug or condition logic broken)
- **Pass signal:** Mid-tier prose at trust 5+, high-tier at trust 15+

### Property 3: Frank feels alive vs mechanical
- **What to look for:** Subjective. Does Frank "show up unbidden" during the day? Does the new texture feel like "Frank is around" or like "noise on top of stage scenes"?
- **Audit caveat:** Without thought bubbles + linkreplace, this assessment is *bounded* — even a perfect playtest result here doesn't mean we've achieved full RTS feel (§8)
- **Fail signal:** Frank still feels like a quest-giver
- **Partial signal:** Frank feels more present than before but still missing texture
- **Pass signal:** Frank feels alive *enough* even without Phase 3 craft layers

---

## §10 Recommendations + next actions

### Before Step D playtest — quick fixes (optional)

| Action | Effort | Value | Recommend? |
|---|---|---|---|
| Add italic 1-line NPC interior in Tier-3 prose (approximate thought bubbles) | 30 min | Could close §5.1 gap partially without engine work | 🟡 Maybe |
| Add 1 cross-NPC bridge to scene #11 high-tier (mention Diana) | 15 min | Closes §5.2 gap with one scene change | 🟡 Maybe |
| Bump random encounter chances to 40-50% | 5 min | Mitigates §6.2 risk | 🟡 Maybe |
| Just play as-is | 0 min | Lets gaps naturally surface, plays inform fixes | ✅ Recommend |

**My recommendation:** play as-is. Gaps are theoretical; playtest will tell us which actually bite.

### After Step D playtest — based on results

**If pilot PASSES** (Frank feels alive enough):
1. Apply same content pattern to Diana → Marge → Ryan → Jake (per doc 16 §6)
2. Begin Phase 2 engine work (S1-S6 from doc 14) in parallel
3. Update `15_Sandbox_Pivot_Direction.md` §10 to mark Frank pilot as ✅

**If pilot PARTIALLY passes** (some properties pass, some don't):
1. Triage gaps using §3 partial alignments + §5 missed items + §6 unverified
2. Likely fixes: (a) bump scene chances, (b) add thought bubbles via italic approximation, (c) add cross-NPC bridges
3. Re-playtest before scaling to other NPCs

**If pilot FAILS** (Frank still mechanical):
1. Build Phase 3 structural items (S7 linkreplace + S8 thought bubbles) BEFORE more content authoring
2. The two Phase 3 items are likely the missing ingredients; without them no amount of additional content will close the gap
3. Re-playtest after Phase 3 ships

### Long-term — closing the gaps

The 7 missed items rank by impact for "feels like RTS":

1. 🟥 **Linkreplace-drip** (S7, Phase 3) — biggest experiential gap
2. 🟥 **NPC thought bubbles** (S8, Phase 3) — craft signature gap
3. 🟧 **Counter display in Quests panel** (S3, Phase 2) — transparency gap
4. 🟧 **Cross-NPC bridges** (content-only, can do anytime) — interconnection gap
5. 🟨 **Threshold notifications** (S4, Phase 2) — failure-as-info gap
6. 🟨 **Per-canvas executedToday** (S2, Phase 2) — granularity gap
7. 🟨 **Sidebar travel shortcuts** (S5, Phase 2) — UX friction gap

---

## §11 Cross-references

- `13_Road_to_Success_Reference.md` — empirical RTS observations (§11 corrections, §16 Brother playthrough)
- `14_Engine_PRD_Sandbox_Additions.md` — engine work spec (S1-S8 items + §1 update with bug fix)
- `15_Sandbox_Pivot_Direction.md` — direction synthesis + §6 8 philosophical shifts
- `16_Frank_Scene_Library_Design.md` — Phase 1 scene specs + §19 playtest properties
- `feedback_tls_scene_body_style.md` (memory entry) — Tier-3 carve-out doctrine
- `02_NPC_Stage_Chains.md` — capstone-layer note (2026-05-03 update)

### TOML files modified in Phase 1

- `games/the_long_summer_test/toml_phases/7_final_game.toml` — operational source (all 6 new scenes + Stage 4 polish + catch polish + new daily-reset flags)
- `games/the_long_summer_test/toml_phases/5_scenes.toml` — Step B sample sync + pointer note for Step C scenes
- `games/the_long_summer_test/toml_phases/3_activities.toml` — Step B sample sync + pointer note for Step C activity

### Engine code modified

- `apps/projects/services/template_import.py` — group/block_pool props-nesting bug fix (4-place patch, lines 3838, 3863-3867, 3911-3915, 3957-3962)

---

**End of doc 17.** 🟦 Captured. Read this doc before declaring playtest results, and again after, to triage which gaps actually mattered.
