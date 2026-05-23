# 20 — Frank Slice Review through the RTS Doctrine Lens

> **Status:** Review record, not a redesign or implementation. Authored 2026-05-05.
> **⚠️ PARTIAL SUPERSESSION 2026-05-05** — §1.E + §1.H + §3 row 5 + §4 ranking were partially superseded same-day by **doc 21** (Brother mechanism audit) and **doc 22** (cross-NPC mechanism comparison across 4 NPCs / 40 surfaces). The S1-as-doctrine-match framing is wrong; S7 (linkreplace cascades) is the doctrine match. Inline ⚠️ correction notes added at affected sections; see §10 below for the trace.
> **Purpose:** Capture a deliberate review pass that (a) extracted the *portable* RTS learnings from Phase 2 (separating doctrine from Frank-specific iteration work), then (b) audited the current Frank state in `7_final_game.toml` against that doctrine. Produces a punch list of doctrine-vs-implementation gaps so future sessions can see "this review was done, here's what it found."
> **Method:** Read-only. Source-extraction across docs 13 / 14 / 15 + RTS memory files (`rts_three_arc_shapes.md`, `rts_discovery_patterns.md`); Frank canvas inventory via grep on `7_final_game.toml`. No live play; gaps marked accordingly in §3.
> **Scope:** Frank only. Ryan / Jake analogous reviews are next-doc territory.

---

## §0 Why this doc exists

Across the Phase 2 redesign folder, Frank-specific iteration work (docs 02 §"Frank — full chain", 16, 18, 19) is interleaved with NPC-agnostic doctrinal learnings from RTS exploration (docs 13, 14, 15 and the two RTS memory files). When future sessions ask "where is Frank now relative to RTS doctrine," answering requires re-deriving the doctrine separation each time. This doc fixes the answer in place.

It is **not** a new design. It is **not** an implementation plan. It is the recorded output of one review pass: doctrine-on-the-left, slice-on-the-right, gaps-in-the-middle.

---

## §1 The portable Phase 2 learnings (RTS-derived, NPC-agnostic)

The 14 learning items below are the doctrinal carry-forward — independent of any specific Frank decision. Each item cites primary sources so future docs can follow the chain.

### A. Doctrine flip — content library, not arc spine

Stages are the **capstone layer** (single-digit ledger of one-shot moments per doc 01). The daily-texture layer is the scene library. Old TLS thinking ("each NPC has a 0→1→2→3 arc you progress through") is dropped; new thinking is **"the world is a content library; NPCs live in it; scenes happen when player walks into the right place at the right time with the right stats; stats are LEVERAGE for depth, not GATES for access"**.

Source: doc 15 §6 (eight philosophical shifts), doc 13 §13 #4 ("Story lives at the SCENE level, not the ARC level").

### B. Three arc tendencies, mixed not categorized

Brother / Marcus / Edward looked like 3 clean shapes from data extraction; live play (doc 13 §16 Correction 7) showed every NPC is hybrid — random + deterministic + time-gated + cross-NPC bridges. Ratios differ; categories don't. **Don't pick one shape per NPC — pick a ratio of triggers.**

Source: doc 13 §5 + §16 Correction 7, `rts_three_arc_shapes.md`.

### C. Day-1 immediate content

RTS serves voyeur scenes with images + video at MC corruption 0 within ~5 moves. Stat grinding is for *escalation to active participation*, not *initial access*. Game must prove itself in 5 minutes, not gate everything behind prereqs.

Source: doc 13 §12 (turn-by-turn play log), doc 13 §13 #1.

### D. Three writing tiers, deliberately budgeted

T1 utility (~15w) for activities; T2 vignette (~30-100w) for ambient encounters; T3 character (~200-600w) reserved for intros / capstones / transitions. **Tier-3 is a budget, not a default.** ~30% T3 / 50% T2 / 20% T1 in RTS. NPC thought bubbles (`💭 Alfred is thinking...`) are a 4th orthogonal dimension that adds interiority without text density.

Source: doc 13 §9 + §16 Finding 1.

### E. Same scene, different depth at different stats — **doctrine match is S7, not S1**

> ⚠️ **CORRECTED 2026-05-05** — original framing here cited engine S1 (per-block text_variants) as the doctrine match. Doc 21 + doc 22 audited 40 RTS surfaces across 4 NPCs and confirmed **per-block text_variants appears in 0 of 40 scenes**. The actual mechanism is `<<linkreplace>>` cascades (engine S7) with stat gates positioned at one of three locations: (1) the hub button, (2) top of cascade after opening beat, (3) intermediate cascade beats. See doc 21 §4 for the six pattern definitions (A-F), doc 22 §4 for the cross-NPC distribution.

The single most counter-intuitive RTS pattern. `BrotherCaughtMasturbating` plays a 5-line rejection at MC corr 6 and a ~590-word seduction at MC corr 31 — **same passage**. Player's reward for grinding is *more of the same scene*, not a new scene. Even "100% chance" deterministic scenes have stat-tier branches inside (Finding 2 in §16). This drives the come-back-later loop.

**Mechanism (corrected):** `<<linkreplace>>` cascade with one stat gate at the top — the `[Shhh]` button only renders if `getCorruptionLevel() >= 3 AND StageTwoCorruption(Brother)`. Below threshold, the scene plays a 5-line rejection variant. The cascade is the structural primitive; the stat gate determines which branch the cascade enters. Per-block text-swap-on-render (S1) doesn't reproduce this — it would render different opening text per stat, not gate cascade entry.

Source: doc 13 §11 #2 + §16 Finding 2; **archived** PRD 14 S7 (the actual doctrine match) + S1 (a TLS-engine-fit alternative producing a different effect).

### F. Walkthrough = primary planning UI (engine S3)

Publishes the literal scene table (SCENE / NPC / REQUIREMENTS / CHANCE / GUIDE / STATUS). GUIDE is concrete prose ("Have at least 15 relationship points... wait for invite, go to date"). **STATUS = scene-completion tracker (✅ flips at terminal-click)**, not real-time gate. Requirements are SOFT for attempts (fall-through alt content possible at partial prereqs) but HARD for completion-credit. Player loop is *literally* "open → pick close-to-unlock → execute GUIDE → ✅ ticks."

Source: doc 13 §6 + `rts_discovery_patterns.md`; engine PRD doc 14 S3.

### G. Failure is information, not progress (engine S4)

`<<NotifyCorruption N>>` is a UI threshold-publisher (corrected 2026-05-02). Three notify-fail tiers graduated by gate severity:
- **Visible-disabled label** (`❌ Too early to sleep ❌`) — trivial state gate, no click needed.
- **Transient toast** (click "Go to School" in casual outfit) — preference/prep gate.
- **Modal page with upgrade path** (Cheats → Become a Patreon) — hard fundamental gate.

Source: doc 13 §11 #3 + §7.2 + §7.4, `rts_discovery_patterns.md`; engine PRD doc 14 S4.

### H. Discovery via in-context button injection — **mechanism mostly presence+time, not stats**

> ⚠️ **CORRECTED 2026-05-05** — original framing claimed hub buttons render conditionally on stat thresholds. Doc 21 §6 + doc 22 §5 audited 4 hub passages directly: Talk/Tease/Flash/Sex buttons in `BrotherBedroom` render conditionally on **NPC presence + time band**, not on stats. Stat gating happens INSIDE click handlers (e.g., `Have sex` click checks `getCorruptionLevel() >= 3` → goto OR `NotifyCorruption(4)`). Only `Sleep with him` button is truly stat-injected (`relation >= 10`). The "1 button → 4 buttons across days" differential observed in 2026-05-04 was the presence-injection (Brother arriving home), not stat-injection.

Hub passages walk NPC scene table at render time and emit one button per scene whose **NPC-presence + time-band conditions** are met (with rare stat conditions on specific buttons). Visiting BrotherBedroom went from 1 button (Hallway return only, Brother at school) → 4 buttons (Talk/Tease/Flash/Sex when Brother home and not LN). **The differential ("the room has more buttons than last time") IS the unlock notification.** Silent. Combined with walkthrough pre-declaration, the perception is "Oh right, I knew that scene existed — now I can do it" rather than surprise.

Hub variation by arc tendency (doc 22 §5): family-NPC hubs are button menus with presence/time injection; peer-NPC hubs are thin navigation passages (event-driven, not menu-driven); career-NPC hubs are app shells (DM-mediated).

Source: `rts_discovery_patterns.md` (Pass-2 finding) + doc 21 §6 (corrected source-extracted) + doc 22 §5 (cross-NPC hub comparison). **Not currently in any active PRD** (PRDs archived 2026-05-05).

### I. Linkreplace-drip (S7) + thought bubbles (S8) — structural

Each scene = multi-step in-place reveal. Click → +paragraph → +video → next reveal. Stat changes apply per-beat. Bridges "dice roll triggered" → "I'm reading a chapter."

Source: doc 13 §8 + §16 Finding 1; engine PRD doc 14 §10 (deferred to Phase 3).

### J. Passive trait drift / gains (engine S6)

Brother arousal climbed 0→3 over 3 days *without MC doing anything to him*. Day-1 voyeur works because by Day-1 evening, family arousals are already non-zero. World drifts on its own. TLS already supports decay; the gain mirror is ~15 LOC per PRD §9.

Source: doc 13 §16 Finding 4; engine PRD doc 14 S6.

### K. Cross-NPC scene flag dependencies

`SellingMyStepsister` gates on Brother corruption + Josh-not-unlocked. Once unlocked, transfers Brother arc INTO Josh. Arcs converge instead of running parallel forever. **Engine already supports this** (PRD 14 §1 row 2 ✅).

Source: doc 13 §7.2 + §16 (live verified).

### L. Composed gates over central rule tables

Time × clothing × location × stats compose at the per-passage level. Same room, different button set per `$game.time` × `$player.energy` × `isPurchased(item)` × `getQuestProgress(quest)`. **Layered constraints make the world feel rule-bound without writing explicit blockers everywhere.**

Source: doc 13 §10 ("The clothing × location × time × stats product is the gating space").

### M. Counter-design anti-pattern

Per-NPC opaque counters that gate cross-counter scenes are a known anti-pattern. RTS uses GLOBAL stats almost exclusively for cross-NPC gates; per-NPC chains use single-prereq narrative beats. **Marcus's hardest gate is "Have ≥15 relationship points + wait for invite + go to date" — one stat + one event.** TLS Stage-3 5-AND chains were doctrinal outliers, retired in doc 18 §3 → §5.

Source: `rts_discovery_patterns.md` ("Anti-pattern to avoid in TLS"), doc 18 §3 + §5 retirement.

### N. Methodology rule

**Source extraction generates clean stories; live play generates messy truth.** Use both, never one alone. Five inferences from data extraction were corrected by live play in 2026-05-02→04 sessions; this rule applies to every future "let's see what game X does" exploration.

Source: doc 15 §1, doc 13 §11 + §16, MEMORY.md.

---

## §2 Slice inventory — Frank as it currently exists

Snapshot of `games/the_long_summer_test/toml_phases/7_final_game.toml` at HEAD (5224 lines, 239 top-level blocks). Frank-touching canvases enumerated below.

| Layer | Canvas id | Role | Tier (target) |
|---|---|---|---|
| **Capstone (one-shot)** | `scene_frank_offer_bookkeeping` | Stage 0→1 trigger | T3 |
| **Capstone (branch in shell)** | catch branch in `scene_living_room_evening` | Stage 1→2 | T3 |
| **Capstone (one-shot canvas)** | `scene_office_crack` | Stage 2→3 | T3 |
| **Capstone (branch in shell)** | bedroom-invitation branch in `scene_office_after_crack` | Stage 3→4 (doc 19 §4) | T3 |
| **Stage-cascaded canonical surfaces** | `scene_kitchen_with_frank_morning` · `scene_kitchen_with_frank_dinprep` · `scene_franks_office_supervised` · `scene_office_supervision_intro` | Repeating surfaces with `[group]` blocks per stage | T2 base + T3 stage groups |
| **Stage 3 / 4 anchors** | `scene_office_after_crack` (S3 evening sex, repeating) · `scene_franks_bedroom_evening` (S4 T3 anchor, doc 19 §5) | Repeatable anchor scenes | T3 |
| **Daily-texture sandbox pilot** | `scene_hallway_frank_pass` · `scene_kitchen_frank_coffee_alone` · `scene_living_room_frank_radio` · `scene_porch_frank_evening_smoke` · `scene_kitchen_late_night_raid` | Random-ambient repeatables | T2 (target — unverified) |
| **Player-initiated** | `activity_talk_to_frank` · `activity_bookkeeping_with_frank` | Deterministic, button-driven | T2 |
| **Transition watcher** | `transition_frank_to_1` | Helper-driven stage commit | utility |
| **Dev shortcuts** | `dev_advance_frank_to_3` · `dev_advance_frank_to_4` · `dev_zero_trust_frank` | QA only | utility |

**Total Frank-facing canvases: ~15** (excluding dev shortcuts and the transition watcher). Numerically at parity with RTS Brother (15 scenes per doc 13 §3).

### Stage helpers (current, post doc-18 + doc-19)

```
frank_stage_1 = AND(
  npc_frank.trust >= 10,
  flag frank_offered_bookkeeping is_true
)

frank_stage_2 — REFACTORED OUT 2026-05-04 (post-condition tautology;
                catch branch writes npc_frank_stage = 2 directly)

frank_stage_3 = AND(
  flag frank_restrict_declared is_true,
  npc_frank.arousal >= 30,
  npc_frank.corruption >= 15
)

frank_stage_4 — N/A (doc 19 §8 row 4: branch-inside-shell at
                bedroom-invitation writes npc_frank_stage = 4 directly)
```

### Counters & flags actively used in gates

- `frank_office_visits` (single-source, increments at `scene_office_after_crack` choice exits; gates Stage 3→4 capstone trigger per doc 19 §4)
- `Frank.corruption` / `Frank.arousal` / `Frank.trust` (multi-source NPC traits, replace retired per-NPC opaque counters)
- One-shot guards: `frank_offered_bookkeeping`, `frank_offered_chores`, `frank_supervision_explained`, `frank_office_first_sex_done`, `frank_invited_to_bedroom`, `frank_bedroom_first_done`
- Daily resets: `talked_to_frank_today`, `frank_hallway_pass_today`, `frank_coffee_alone_today`, `frank_radio_today`, `frank_porch_smoke_today`, `frank_declined_bookkeeping_today`
- Lifetime: `frank_late_night_used`

### One-shot ledger (post doc-19)

4 total: bookkeeping offer · catch · crack · bedroom invitation. **Within single-digit ceiling per doc 01 doctrine.**

---

## §3 Doctrine-vs-implementation audit

For each doctrine item from §1, the slice's current state. Status legend: ✅ aligned · 🟡 partial · ❌ gap · ⚠️ design tension.

| # | Doctrine (§1 ref) | Slice state | Status | Severity |
|---|---|---|---|---|
| 1 | **A. Capstone vs daily-texture separation** | 4 one-shot capstones isolated; 11+ repeatable surfaces. Ledger at 4, single-digit doctrine respected. | ✅ | — |
| 2 | **B. Mixed trigger ratios per NPC** | Frank reads as "mostly deterministic + some random ambient" — close to Brother family/proximity tendency. Ryan/Jake similar. **Slice is single-tempo across all 3 NPCs**; no metric+wait career-tempo presence. | 🟡 (Frank ok, slice as a whole single-tempo) | MED |
| 3 | **C. Day-1 immediate content** | Pre-seed skips prologue; player lands at Frank's already. 5 ambient repeatables (`hallway_pass`, `coffee_alone`, `radio`, `porch_smoke`, `late_night_raid`) authored. **Unverified in browser** whether Day-1 ambient actually fires within first 5-10 turns at zero stats. | 🟡 (authored, not playtest-verified) | HIGH |
| 4 | **D. Three writing tiers** | Capstones authored T3; `[group]` stage cascades intend tier escalation; new daily-texture canvases (5) target T2. **Tier discipline of the daily-texture canvases unmeasured** — possible T2-drifting-toward-T3. | 🟡 | MED |
| 5 | **E. Same scene, different depth at different stats (S7, not S1 — corrected)** | Engine doesn't ship `<<linkreplace>>` cascade primitive (PRD 14 S7 🟦, archived). Stage-cascade `[group]` blocks give cross-stage variety on render, but no in-place click-to-reveal cascade with stat gates. **Frank kitchen morning at trust 5 reads same as at trust 25; bedroom anchor (~400w) lands as a wall.** Come-back-later loop only fires across whole stage transitions. **Per doc 21 §6 + doc 22 §3: per-block text_variants (S1) appears in 0 of 40 audited RTS surfaces — S1 was a citation conflation, not a doctrine match.** | ❌ | **HIGHEST** |
| 6 | **F. Walkthrough counter surfacing (S3)** | Doc 19 §6 specs "Office visits 2/3, Frank corruption 18/25" panel rendering — engine doesn't surface counters yet (PRD 14 S3 🟦). Player can't see distance to a gate. | ❌ | **HIGHEST** |
| 7 | **G. Threshold notifications (S4)** | Gated TLS choices silently don't render. No "I'd need to know him better — at least 15 trust" feedback. Failure is silence, not information. (PRD 14 S4 🟦.) | ❌ | HIGH |
| 8 | **H. In-context button injection** | Frank's hub locations don't grow new buttons silently as state crosses thresholds. Scene presence is binary (canvas trigger fires or not). **The "room has more buttons than last time" notification mechanism is missing.** Not in PRD 14 at all. | ❌ (and not specified) | **HIGH** (and a coverage gap in PRD 14) |
| 9 | **I. Linkreplace-drip + thought bubbles** | Both deferred to Phase 3 (PRD 14 S7 / S8). Bedroom T3 anchor (`scene_franks_bedroom_evening`, ~400w) lands as wall of paragraphs, not paced reveal. NPC interiority not available as block primitive. | ❌ (deferred by design) | MED |
| 10 | **J. Passive trait gains (S6)** | Frank trust only moves on player click. Decay supported, gains not (PRD 14 S6 🟡). NPC arousal can't drift up over days without interaction. | ❌ | MED |
| 11 | **K. Cross-NPC bridges** | Engine supports today (PRD 14 §1 ✅). Frank doesn't bridge into anyone — `diana_awareness` is a silent accumulator, not a content unlock. No `SellingMyStepsister`-style arc transfer. | 🟡 (engine ready, content not authored) | LOW |
| 12 | **L. Composed gates** | TLS multi-schedule OR-logic per canvas is more expressive than RTS (doc 15 §4 row 8 — TLS ahead). Composition pattern in active use. | ✅ | — |
| 13 | **M. Counter-design anti-pattern** | Doc 18 §3 → §5 retired the per-NPC opaque counter trio (`frank_bookkeeping_count`, `frank_chore_count`, `frank_tease_count`) in favor of `npc.frank.corruption` multi-source. Stage 3→4 gate is now `frank_office_first_sex_done + frank_invited_to_bedroom is_false + Frank.corruption ≥ 25 + frank_office_visits ≥ 3 + talked_to_frank_today is_false` — **5-AND, with `frank_office_visits` walkthrough-breadcrumbed per doc 19 §6.** Better than retired 5-AND (which was opaque-counter heavy), but still wider than Marcus's "one stat + one event" benchmark. | ⚠️ design tension | MED |
| 14 | **N. Methodology rule** | This review is source-extraction-only. **No live play behind the gap claims in items 3, 5, 6, 7.** Per the rule itself, recommendations grounded in this review need browser validation before action. | ⚠️ noted | — |

---

## §4 Engine work that activates already-shipped Frank content

> ⚠️ **REVISED 2026-05-05** — original ranking put S1 first based on PRD 14's framing. Doc 21 + doc 22 corrected the doctrine match: S7 (linkreplace cascade) is what RTS actually uses across all 40 audited surfaces. Revised ranking below.

The slice has done content-volume work (15 canvases ≈ Brother) and doctrine-cleanup work (counters retired, capstones isolated, branch-inside-shell pattern in place, surface multiplexing exercised). What it hasn't done is the engine work that activates the doctrine.

**Highest-leverage missing engine items**, ranked (revised):

1. **S7 — Linkreplace-drip multi-step scenes** (archived PRD 14 §10, ~150 LOC, structural). The actual RTS doctrine match per doc 21 §4 + doc 22 §3-§4. Enables Pattern D for family-style Frank content (kitchen morning, office after-crack), Pattern E for high-stakes scenes (bedroom anchor), and Pattern F for branching capstones (bedroom invitation could become real Accept/Decline parallel cascades). Without this, no come-back-later loop exists in TLS.
2. **S3 — Walkthrough counter display** (archived PRD 14 §6, ~25 LOC). Player can't plan without distance-to-gate visibility. The entire RTS player-loop ("open Walkthrough → pick close-to-unlocking → close gap") is gated on this.
3. **§H button injection (presence + time + occasional stats)** (not in any active PRD). Hub-rendered scene-table walks evolve the room as state changes — most discovery happens through this. Frank's locations don't grow new buttons silently. **Revised understanding** (doc 21 §6): mostly presence/time-driven, with rare stat-injected buttons.
4. **S4 — Threshold notifications / `NotifyCorruption`-style** (archived PRD 14 §7, ~35 LOC). Universal RTS pattern — every gated button publishes its threshold. Failure as information vs failure as silence is the difference between learning and grinding-blind.
5. **S6 — Passive trait gains** (archived PRD 14 §9, ~15 LOC). Without world-drift, Day-1 ambient encounters require explicit player priming; Brother-style "by Day 1 evening, family arousal is already non-zero" doesn't happen.
6. **S1 — Per-block `text_variants`** (archived PRD 14 §4, ~20 LOC) — **demoted**. Not the doctrine match (per doc 21 §6 + doc 22 §3 — 0 of 40 surfaces use it). Could ship as a cheaper TLS-engine-fit alternative that produces depth-shift differently than RTS does. Optional substitute for S7 if S7 is rejected as too structural.

Items 2 + 4 + 5 = ~75 LOC small additions. Item 1 (S7) = ~150 LOC structural — but it's the actual mechanism. Item 3 (button injection) is unestimated — needs a PRD addendum or refresh of an archived PRD.

---

## §5 What's working in Frank's slice (don't regress)

Naming the wins explicitly so they aren't lost in the gap list above.

1. **Volume hits the Brother bar.** ~15 Frank canvases ≈ RTS Brother density. Phase 1 pilot delivered.
2. **Capstone-vs-daily-texture separation is intact.** 4 one-shots in the ledger; everything else repeatable. Single-digit doctrine respected.
3. **Surface multiplexing is real.** Frank present on kitchen morning / dinprep / coffee-alone / late-night, hallway pass, living room (catch + radio), back porch, office (supervised + crack + after-crack), bedroom. Brother-spread shape.
4. **Per-NPC opaque-counter trio retired** (doc 18 §3 → §5). Direction matches §M (move toward global-stat composition). `frank_office_visits` is single-source and breadcrumbed per doc 19 §6.
5. **Both transition mechanisms in use** — helper-driven `transition_frank_to_1` AND branch-inside-shell at catch / crack / bedroom-invitation. Catches what each is good for.
6. **Stage cascade primitive (`[group]` blocks) is exercised** — and the silent-broken cascade bug got fixed during Phase 1 step B (per PRD 14 §1 update). First time prose actually renders in browser at the right tier.
7. **Bedroom location gate** uses `frank_invited_to_bedroom is_true` correctly. Prevents pre-capstone navigation.
8. **Stage label sidebar item** (E11) gates love band correctly — stage label takes precedence once it appears.
9. **Doc 19 design tweak** (`frank_bedroom_first_done` substituted for spec'd `frank_bedroom_last_night`) — pragmatic engine-fit substitution, same narrative purpose.

---

## §6 Cleanup items (low-priority, observed during review)

- **Dead flag declarations.** `frank_keep_route_romantic` / `_arrangement` / `_rupture` / `_power_inverted` (lines 415-418 of `7_final_game.toml`) still in flag_keys list even though doc 19 §1 explicitly drops the 4-keep-route design. Remove during next maintenance pass.
- **Office daytime negative space.** Doc 19 §3 row 3 deferred a Stage-3 daytime office vignette — the negative space (no daytime office content) was deemed acceptable. Confirm in playtest that players read this as "Stage 3 office is evening-only" rather than "the room is just empty during the day."
- **Hallway optional Stage 4 vignette** (doc 19 §5 row 6) deferred. Re-evaluate after Frank arc has been played end-to-end.

---

## §7 Open questions to answer before recommending engine work

1. **Has anyone played Frank end-to-end in browser since doc 19 step 6 shipped (2026-05-04)?** PRD 14 §2 specifies a 30-minute play validation as the Phase 1 → Phase 2 decision gate. If not done, that's the cheapest next move — confirms Day-1 ambient fires, validates surface multiplexing actually lands, surfaces the "stat doesn't change scene depth" friction live before any engine work commits.
2. **Is Phase 2 engine work (S1-S6) actually queued?** The slice authored Frank assuming this would land. If indefinitely deferred, the slice has a permanent "lifeless stat economy" feel until built.
3. **Should the in-context button-injection pattern (§H) get added to PRD 14?** The 2026-05-04 highest-leverage discovery finding isn't currently specified. Likely bigger return than S7 linkreplace.
4. **Does the new Stage 3→4 5-AND gate (doc 19 §4) play legibly?** Better than retired counters, walkthrough-breadcrumbed, but still wider than Marcus's benchmark. Live play would surface whether players hit one condition + stall on another.

---

## §8 Self-classification

**This doc is:**
- ✅ A review record (captures what was looked at and what was found, dated)
- ✅ A doctrine→implementation gap list (actionable next-step input)
- ✅ A pointer-doc (cites primary sources rather than restating them)

**This doc is NOT:**
- ❌ A redesign (no new design proposals — just gaps in existing design)
- ❌ An implementation plan (PRD 14 already specs the engine work; this doc points at it, doesn't re-spec it)
- ❌ A playtest report (no live play; methodology rule §N flagged this as a limitation)

**Supersedes:** nothing.
**Partially superseded by:** docs 21 + 22 (same-day, 2026-05-05). See §10 below for the trace.

---

## §9 Cross-reference index

| Cited doc | Sections referenced |
|---|---|
| `01_Repeatable_First_Doctrine.md` | Single-digit one-shot ledger doctrine. |
| `13_Road_to_Success_Reference.md` | §3 game shape · §5 three arc tendencies · §6 walkthrough as planning UI · §7 passage mechanics + NotifyCorruption correction · §8 linkreplace-drip · §9 three writing tiers · §11 five corrections · §12 Day-1 turn-by-turn log · §13 ten takeaways · §16 Playthrough 2 findings (NPC arousal int, hybrid arcs, thought bubbles, deterministic-rejection variants, passive accumulation, grope-corruption). |
| `archive_14_Engine_PRD_Sandbox_Additions_2026-05-05.md` (archived) | §1 capability audit · §3 additions table · §4 S1 per-block text_variants (now demoted) · §6 S3 counter display · §7 S4 threshold notifications · §9 S6 passive gains · §10 S7/S8 (S7 now identified as the doctrine match). |
| `21_RTS_Brother_Mechanism_Audit.md` | §3 mechanism table · §4 patterns A-F · §5 Brother distribution · §6 corrections to doc 20 §1.E + §1.H + §3 row 5. |
| `22_RTS_Cross_NPC_Mechanism_Comparison.md` | §3 cross-NPC distribution · §4 arc-tendency manifests in gate placement · §5 hub variation · §6 reinforcing corrections · §7 implications for Frank. |
| `15_Sandbox_Pivot_Direction.md` | §1 methodology lesson · §4 TLS misalignment audit · §5 doctrinal split · §6 eight philosophical shifts · §10 locked vs open. |
| `18_Frank_Arc_Redesign.md` | §3 single-source counter discipline · §5 Stage 2→3 crack · §6 Stage 3 explicit content. |
| `19_Frank_Stage_3_Plus_Design.md` | §4 Stage 3→4 capstone branch + `frank_office_visits` counter · §5 Stage 4 register cascade + bedroom anchor · §6 hint + walkthrough integration · §7 one-shot ledger · §8 implementation order. |
| `frank_phase2_supersession.md` (memory) | Inline ⚠️ markers in docs 02/16/18 noting which Frank-specific sections doc 19 supersedes. |
| `rts_three_arc_shapes.md` (memory) | Three arc tendencies, walkthrough-as-planning-UI, mechanics worth borrowing. |
| `rts_discovery_patterns.md` (memory) | Two discovery surfaces · three notify-fail tiers · five silent unlock vectors (most important: in-context button injection) · walkthrough STATUS = scene completion tracker · counter-design anti-pattern. |

---

## §10 Same-day supersession trace (2026-05-05)

This doc was authored 2026-05-05 morning. Two follow-up audits the same day partially superseded specific sections. Captured here so the trace is visible from this doc, not just from the superseding docs.

### What got corrected

| Section | Original framing | Corrected framing | Source of correction |
|---|---|---|---|
| **§1.E** (Same scene, different depth) | "engine S1 — per-block text_variants" cited as doctrine match | **S7 (linkreplace cascades)** is doctrine match. S1 = 0/40 surfaces; S7 = ~73% of audited content scenes. S1 is a TLS-engine-fit alternative producing a different effect, not a doctrine match. | Doc 21 §6 (Brother audit, 16 scenes) + doc 22 §3 (cross-NPC audit, 40 scenes / 4 NPCs) |
| **§1.H** (In-context button injection) | "stat-thresholds + 100%-chance prereqs" framed as primary mechanism | **NPC presence + time band** is the primary mechanism for hub button rendering. Stat-injected buttons exist (Brother's `Sleep with him`) but are rare — most stat gating happens INSIDE click handlers (`<<button "Have sex"><<if getCorruptionLevel() >= 3>><<goto>>` else `NotifyCorruption`). | Doc 21 §6 (BrotherBedroom hub source verbatim) + doc 22 §5 (4-hub comparison) |
| **§3 row 5** (S1 ranked HIGHEST gap) | S1 ranked highest engine gap | **S7 ranked highest** structural gap; S1 demoted to "optional cheaper substitute." Same severity overall but the priority work is structural cascade primitive, not text-swap. | Doc 21 §6 |
| **§4 ranking** | S1 / S3 / §H / S4 / S6 | **S7 / S3 / §H / S4 / S6 / S1 demoted** — S7 surfaced as highest priority because it's the actual mechanism. S1 stays in the list as an optional cheaper alternative if S7 is rejected as too structural. | Doc 21 §6 + doc 22 §7 |

### What stayed correct

- §1 doctrine items A, B, C, D, F, G, I, J, K, L, M, N — unchanged
- §2 Frank slice inventory — unchanged
- §3 rows 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14 — unchanged
- §5 Frank slice wins — unchanged
- §6 cleanup items — unchanged
- §7 open questions — unchanged

### Why this section exists

Future sessions reading doc 20 might miss the inline ⚠️ markers in §1.E + §1.H + §3 row 5 + §4 if they're skimming. This trace section gives a single place to scan for "what changed and when," matching the supersession-map pattern from `frank_phase2_supersession.md`.

### What this trace does NOT cover

- The PRD archive operation (docs 03/08/12/14 → `archive_<n>_*_2026-05-05.md`) is noted in MEMORY.md but not in this doc's body. Affects how cross-refs resolve: PRD 14 references in this doc still point to file content (file exists, just renamed) but the URL/path now has `archive_` prefix.
- The "Should we un-archive S7" decision — open. Doc 22 §9 leaves it as the Phase 2-vs-3 commit question.

---

End of review.
