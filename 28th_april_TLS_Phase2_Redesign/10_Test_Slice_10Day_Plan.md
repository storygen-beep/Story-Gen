# 10 — TLS Phase 2 — 10-Day Engine-Validation Test Slice

> **Created 2026-04-30.**
> Sibling to `08_Engine_PRD_Phase2_Additions.md`. The first non-trivial fixture authored against `01_Repeatable_First_Doctrine.md` + `04_Scene_Cascade_Pattern.md`. Successor in size to `apps/game_generation/games_toml_files/engine_prd_phase2_2026_04_29.toml` (which exercises only E9/E10/E11 in isolation with two dev buttons and one NPC).
>
> **Output:** A new game folder `games/the_long_summer_test/` (parallel to `the_long_summer/`), with its own `toml_phases/` and a single compiled `output/index.html`. Does NOT mutate the existing `the_long_summer/toml_phases_v2/` skeleton.
>
> **Plan-only.** No TOML in this doc. The plan defines what gets authored; execution writes the TOML.

---

## 1. Context — why this slice, why now

The TLS Phase 2 redesign has finished its **doctrine + engine work**:

- Doctrine locked across `00`–`09` in this folder.
- Engine PRD 03 (E1–E8) and PRD 08 (E9–E11) all shipped; 111 tests green; engine is unblocked.
- Frank's full stage chain authored in `02_NPC_Stage_Chains.md`; Ryan/Jake scaffolded as "80% liftable from master spec §6."
- The 2B Systems Budget (`book_phases/2b_systems_budget.md`) ties the design book to the engine: 5 whiteboard goals, 6 income channels, 40 hints, full sidebar TOML, in-fiction gate justifications.
- One working Phase 2 fixture exists — but it's a 200-line minimal demo (one NPC, two dev buttons, one location pair).

**What is *not* yet proven:** that a *non-trivial* Phase 2 game — multiple NPCs running concurrently, real schedules, real hubs, scene cascades with stage × time-band overlay, daily-tick resets, decay-driven maintenance pressure, stage-gated hint rotation, stalled-stage detection on a neglected NPC — actually plays as the doctrine claims. The diagnosis (`00_TLS_Phase2_Diagnosis_and_Direction.md`) named this gap explicitly: TLS is currently a kinetic novel that pretends to be a sandbox; we believe the new doctrine produces a sandbox that occasionally hands you a paragraph; we have not yet *played one*.

This slice is that proof. Engine-validation framing (user-locked):

- **Dev shortcuts allowed.** Hidden force-advance buttons unlock Stage 3+ cascades for visual verification. Marked dev-only and stripped before any player slice.
- **Skip Prologue.** Maya wakes in her bedroom on Day 1 morning of her stay. Pre-seed `prologue_complete = true` + `arrived_at_franks = true` + `first_morning_kitchen_done = true` (so Frank's love sidebar is already revealed). The Prologue is locked-correct novel-mode — irrelevant to what's under test.
- **Voice at draft quality.** Density caps must be honored (per `01` Doctrine § "checklist" item 6), but register polish is not the success criterion. A second pass strips dev buttons and tightens prose for a player-facing release.

---

## 2. Scope locks

### In-scope
- **Three deep NPCs:** Frank, Ryan, Jake. Each authored to natural Stage 0 → 1 → 2.
- **Two ambient NPCs:** Diana (kitchen anchor + silent `diana_awareness` accumulator), Marge (employer; hires Maya Day 1 evening).
- **One peer NPC:** Cookie (diner co-worker, evening band only — texture, not arc).
- **10 in-game days** (Mon Day 1 → Wed Day 10, single calendar week + 3 days into the next).
- **One-week rent cycle:** rent due Sunday Day 7. Tests `[settings.rent]` → eviction_mode handling.
- **Hub-and-event architecture** for 8 active locations (kitchen, hallway/home, living room, Frank's office gated, Maya's bedroom, back porch, yard, Jake's doorway, diner front, main street).
- **Income channels 1 + 2 + 5:** diner T0 base wage, diner T1 once unlocked, Ryan small-ticket Help. (T2/T3 and Ryan Partner closes are out per "no Stage 3+ natural progression.")
- **All shipped engine features** — E1 (flag op), E2 (decay), E4 (stage_helpers), E5 (daily_tick), E6 (text_variants), E7 (`<<inc>>`), E9 (stalled detection), E10 (stage-gated hints), E11 (stage_label sidebar). Plus baseline `trigger.chance`, group blocks, `block_pool`, F1–F4.

### Out of scope (deferred / dev-button only)
- **Frank Stage 3 (Tease cascade) + Stage 4 (Crack/Keep)** — dev-button only, no natural advance.
- **Ryan Stage 2 (Partner) + Stage 3 (Big deal/Beach)** — dev-button only.
- **Jake Stage 3 (Caught/Hand) + Stage 4 (Keep)** — dev-button only.
- **Diana arc** — silent accumulator runs; no active arc surfaces in 10 days.
- **Marge Thursday key** (`first_ambient_tilt`) — unreachable in 10 days per the design book (week 3 minimum); deferred.
- **Sub-reputation gating** beyond rep_road from diner T0/T1 — rep_church and rep_college accumulate ambiently but don't gate anything in this slice.
- **Phase-2-locked locations** (truck stop bar, fairground, stadium, church interior, full college campus) — stay locked per book §7.
- **Cookie arc.** Cookie speaks ambient lines on shifts; no progression.
- **Phone, body upgrades, Diana's confrontation, shadow layer, recurring calendar events** — all explicitly Phase 2+ stubs.

---

## 3. Mechanisms validated (the actual checklist)

This is what we look for in browser playtest. Each line corresponds to a doctrine claim or engine feature that this slice exercises.

| # | What gets exercised | Evidence in the test slice |
|---|---|---|
| 1 | Three-layer architecture (hub / activity router / scene) | hub_kitchen renders a button menu every visit; `scene_kitchen_with_frank` fires on a `chance=0.30` router roll when Frank scheduled |
| 2 | Same passage, different stage | `scene_kitchen_with_frank` reads differently on Day 2 (Stage 0) vs Day 5 (Stage 1) vs Day 9 (Stage 2) |
| 3 | Stage × time-band cascade overlay (locked precedence: stage outermost → band → tier) | Frank's Stage 1 branch has separate M (paper at the table) and DINPREP (church-bulletin envelope) sub-paragraphs |
| 4 | One-time guard branch inside repeatable shell | Mix of two engine implementations, both honoring "fires once, gated on flag" semantics: (a) **literal branches** inside repeatable shells: `jake_first_glance_noticed` set inside `activity_walk_past_jakes_door` Stage-0 sub-branch (audit §2.8 fold), `jake_peek_draw_revealed` set inside the same activity's Stage-1 sub-branch; (b) **one-shot canvases** at the host location (engine-equivalent — location IS the repeatable shell, canvas IS the gated branch): `frank_caught` inside `scene_living_room_evening` (is_repeatable=false), `hired_at_diner` inside `canvas_marge_interview`, `first_sunday_passed` inside `canvas_first_sunday_morning`. None re-fire after the first match. |
| 5 | Helper-driven stage advancement (E4) | `frank_stage_1()` clears at trust ≥ 20 + bookkeeping_count ≥ 3; `frank_stage` flips to 1 in same engine cycle |
| 6 | Daily tick (E5) flag resets | `talked_to_frank_today`, `talked_to_diana_today`, `talked_to_ryan_today`, `talked_to_jake_today`, `did_morning_chore_today` all unset at sleep |
| 7 | Trait decay (E2) producing maintenance pressure | If player ignores Ryan for 3 days, `npc_ryan.trust` decays back below the Stage-1 gate |
| 8 | Counter increments (E7 `<<inc>>`) | `frank.bookkeeping_count`, `jake.peek_count`, `ryan.help_count`, `frank.tease_count`, `lean_by_desk_count` all visible incrementing |
| 9 | Stage-gated hint rotation (E10) | Quests page Frank section: Stage-0 hint → Stage-1 hint → Stage-2 hint as `npc_frank_stage` advances |
| 10 | Stalled-stage detection (E9) | Player who pursues Frank+Ryan only — Jake stays at Stage 0 — sees stage-stall hint fire on Day 8 (threshold = 7 days) |
| 11 | `stage_label` sidebar (E11) | Sidebar shows "Frank: Suspicious" on Day 1, updates to "Frank: Grudging warmth" Day 5, "Frank: Restrict" after the catch |
| 12 | `text_variants` on choice labels (E6) | Hub button "Talk to Frank" → "Talk to Frank — about it" after the catch |
| 13 | `flagEffects[].op = unset` (E1) + daily_tick (E5) | "Talk to Frank" disappears from hub same day, returns next morning |
| 14 | `trigger.chance` ambient encounters | Kitchen scene fires roughly 1-in-3 mornings even when conditions match — most days kitchen is just kitchen |
| 15 | Image rotation via 3–5 `search_queries` per image block | `activity_sleep`, `activity_shower`, `activity_sketch` each have ONE fixed paragraph + an image-block with 3–5 search_queries. Prose stays fixed per arc-state per Doc 04 anti-pattern #4 + master spec §10 (image rotation is the verified RtS variety mechanism; prose-pool rotation is not in the doctrine). Engine selects a different image per visit. |
| 16 | F4 rent + eviction_mode | Day 7 Sunday: rent prompt; if `money < 60`, `rent_evicted` flag set, eviction text fires (player can keep playing — flag_set mode, not hard stop) |
| 17 | Sub-reputation movement | `rep_road` rises with diner T0/T1 shifts; visible in sidebar via existing trait_words |
| 18 | Doctrine "stats unlock content, not adjectives" | Diner T1 button only appears at corruption ≥ 25 + rep_road ≥ 15 + beauty ≥ 45 — new menu option, not new prose |
| 19 | Density caps held | Every authored canvas measured: hub ≤ 300 chars body; activity 30–80 words/state; event (one-shot) 80–250 words; scene 80–400 words across all reveals; toast 8–20 words |
| 20 | Confabulation discipline | Every invented background detail logged in a `confabulation.md` registry alongside the slice; no fiction debt |

---

## 4. Starting state (Day 1 Monday 06:30, Maya's bedroom)

Pre-seeded so the Prologue + arrival cinematic are skipped. Player starts inside the sandbox.

**Player core_traits** (additions to existing TLS player declaration):
- Existing kept: `energy=100, hygiene=100, fitness=30, beauty=40, corruption=22, calculation=20, money=400, rep_church=0, rep_road=0, rep_college=0`. Corruption is 22 not 0 — represents Prologue-revenge baseline (per book), within the Closed band (0–24).
- **NEW (declared as integer core_traits per E11 fixture pattern):** `npc_frank_stage=0, npc_ryan_stage=0, npc_jake_stage=0`.
- **NOT in `[player.trait_decay]`** for the three stage traits — validate() rejects that combination because decay bypasses `applyAndNotifyTrait` (where E9 hooks).

**Pre-seeded flags** (set in `[player.flag_keys]` initial state):
- `prologue_complete = true`
- `prologue_at_bed = true`, `prologue_saw_them = true`, `prologue_crossed_line = true`, `prologue_complete = true` (so corruption sidebar shows the post-Prologue band line "Driving south." → flips to "Different house. Same body." once we set `arrived_at_franks`)
- `arrived_at_franks = true`
- `first_morning_kitchen_done = true` — this is the one cheat. Lets Frank's love-band sidebar render from Day 1 and lets us start in-band rather than burning a one-shot. The first-morning event is locked-correct as authored; we're skipping it for slice purposes.
- All daily-reset flags (`talked_to_*_today`) initialized as false.

**NPC starting traits** (kept as declared in existing metadata):
- `npc_frank: trust=10, love=0, arousal=0, corruption=0`
- `npc_ryan: trust=5, love=0, arousal=0, corruption=0`
- `npc_jake: trust=0, love=-5, arousal=0, corruption=5`
- `npc_diana.awareness=0`
- `npc_marge.trust=0`
- `npc_cookie.trust=0`

**Time:** `starting_hour=6, starting_day="Monday", starting_week=1`.
**Starting canvas:** new `event_test_slice_intro` — a 60-word "you wake to the fan, the cicadas, the kitchen sounds downstairs" frame that hands the player to `hub_mayas_bedroom`.

---

## 5. NPC stage chains (test-scope subset)

Lifted from `02_NPC_Stage_Chains.md` (Frank) and the master spec §6 (Ryan, Jake). All Stage 3+ rows are present so the dev buttons have a target, but only Stages 0/1/2 get *naturally* authored cascade content.

### 5.1 Frank — `npc_frank_stage = 0..4`, arc_stages = ["Suspicious", "Grudging warmth", "Restrict", "Tease", "Cracked"]

| Stage | Name | Gate (current) | Advancing trigger → next | Content for slice |
|---|---|---|---|---|
| **0** | Suspicious landlord | default | helper `frank_stage_1()` = `npc_frank.trust >= 20 AND frank.bookkeeping_count >= 3` → Stage 1 | scene_kitchen_with_frank Stage-0 branch (terse, paper, no eye contact) |
| **1** | Grudging warmth | `npc_frank_stage == 1` | one-time branch inside `hub_living_room` evening: gates on `npc_frank_stage == 1 AND corruption >= 45 AND time_band in [E,N] AND frank scheduled home AND frank_caught == false`. Branch sets `frank_caught = true`; on choice resolution sets `frank_restrict_declared = true`. The `npc_frank_stage = 2` advancement is the **helper-derived consequence** per Doc 02 §"Where stages get advanced" — `frank_stage_2()` evaluates true once both flags are set, and the engine writes the stage value in the same engine cycle. | scene_kitchen_with_frank Stage-1 branch (numbers warmth, M + DINPREP variants); activity_bookkeeping_with_frank in office |
| **2** | Restrict | `npc_frank_stage == 2 AND frank_restrict_declared` | helper `frank_stage_3()` = `corruption >= 50 AND frank_restrict_declared AND npc_frank.arousal >= 30 AND frank.tease_count >= 3` → Stage 3. Naturally unreachable in 10 days; dev button only. | scene_kitchen_with_frank Stage-2 branch (supervised tone); chore buttons appear (porch sweep, kitchen cleanup); scene_franks_office_supervised available |
| **3** | Tease under compliance | `frank_stage_3()` | one-time branch inside `scene_franks_office_supervised` deepest tier sets `frank_cracked = true`, `npc_frank_stage = 4`. **Dev button only in slice.** | dev cascade fragment so the branch renders if force-advanced |
| **4** | Cracked / Keep route | `npc_frank_stage == 4` | terminal | dev cascade fragment — single Stage-4 paragraph proving the branch path |

**Counters added to `[player]`:** `frank.bookkeeping_count = 0`, `frank.tease_count = 0`, `frank.chore_count = 0`, `lean_by_desk_count = 0`.
**One-time guards:** `frank_caught`, `frank_restrict_declared`, `frank_cracked`, `frank_keep_route_<x>`.

### 5.2 Ryan — `npc_ryan_stage = 0..4`, arc_stages = ["Stranger", "Helper", "Partner", "Closer", "After Beach"]

| Stage | Name | Gate | Advancing trigger | Content for slice |
|---|---|---|---|---|
| **0** | Stranger | default | helper `ryan_stage_1()` = `npc_ryan.trust >= 15 AND group_settled_in == true` → Stage 1. `group_settled_in` flips when player completes ≥3 of: first kitchen (pre-seeded), first walk to town, first diner shift, first yard help. Reachable Day 4–5. | scene_yard_with_ryan Stage-0 branch (he doesn't look up; brief exchange; +1 trust if she brings water) |
| **1** | Helper | `npc_ryan_stage == 1` | helper `ryan_stage_2()` = `npc_ryan.trust >= 40 AND corruption >= 25 AND ryan.help_count >= 5 AND ryan_partner_open == true` → Stage 2. **Naturally unreachable** (corruption likely 30–35 by Day 10; partner_invitation_event only fires Day 12+ per book pacing). Dev button only. | scene_yard_with_ryan Stage-1 branch (he asks her to fetch the customer water; sets `ryan_help_tier_open`); activity_help_ryan_in_yard increments `ryan.help_count`; scene_shop_customer_area Stage-1 small-ticket close (paid) |
| **2** | Partner | helper | dev button only | dev cascade fragment |
| **3** | Closer (Big deal) | helper | dev button only | dev cascade fragment |
| **4** | After Beach | terminal | — | dev cascade fragment |

**Counters:** `ryan.help_count`. **One-time guards:** `ryan_help_tier_open`, `ryan_partner_open` (manually flipped via dev button only in slice), `ryan_big_deal_closed`, `ryan_beach_proposal`, `ryan_keep_route_<x>`.

### 5.3 Jake — `npc_jake_stage = 0..4`, arc_stages = ["Hostile", "Noticed", "Peek/Draw", "Tease", "Caught"]

| Stage | Name | Gate | Advancing trigger | Content for slice |
|---|---|---|---|---|
| **0** | Hostile | default | helper `jake_stage_1()` = `beauty >= 50 OR jake_first_glance_noticed == true`. Beauty starts at 40; rises with shower + sketch + maintenance — should cross 50 by Day 3–4. Alternately the first-glance sub-branch inside `scene_jakes_doorway` Stage-0 (gated `jake_first_glance_noticed == false AND beauty >= 40`) fires when Maya passes hub_jakes_doorway A-band on Day 2 (`jake.peek_count = 0`); the sub-branch sets `jake_first_glance_noticed = true` and the helper then advances Stage 1. | scene_jakes_doorway Stage-0 branch ("the door's mostly shut"; if knocked, rebuff line) |
| **1** | Noticed | `npc_jake_stage == 1` | one-time branch inside `scene_jakes_doorway` Stage-1 evening when `jake.peek_count >= 3` AND `corruption >= 30`. Sets `jake_peek_draw_revealed = true`, `npc_jake_stage = 2`. Reachable Day 6–7. | scene_jakes_doorway Stage-1 branch (hands stop briefly; longer beat); activity_walk_past_jakes_door (state-pump, +1 peek_count, daily-cooldown via `walked_past_jakes_today`) |
| **2** | Peek/Draw | `npc_jake_stage == 2 AND jake_peek_draw_revealed` | helper `jake_stage_3()` = `npc_jake.love >= 0 AND corruption >= 50 AND jake_caught == true`. Naturally unreachable. Dev button. | scene_jakes_doorway Stage-2 branch ("Lean in the doorway" button appears); brief tease cascade |
| **3** | Tease | helper | dev button only | dev cascade fragment |
| **4** | Caught | terminal | — | dev cascade fragment |

**Counters:** `jake.peek_count`. **One-time guards:** `jake_first_glance_noticed`, `jake_peek_draw_revealed`, `jake_caught`, `jake_hand`, `jake_keep_route_<x>`.

---

## 6. Day-by-day expected play arc (the natural-cadence walkthrough)

Sketches what a "follows-the-hints" player sees. Not a script — actual play diverges based on choice. Used to verify the test exercises every mechanism in §3.

> **Note:** "event" in this walkthrough refers to a narrative moment, not a non-repeatable canvas. Most first-time moments (Marge interview, Jake's first glance, first Sunday morning) are flag-gated branches inside their hub or scene per §7.4 — see also `01_Repeatable_First_Doctrine.md` §"When to use a true one-shot."

| Day | Dow | Headline beats | Stages at end of day | Validations |
|---|---|---|---|---|
| 1 | Mon | Wake, kitchen with Diana (ambient), walk to town, Marge interview (`hired_at_diner`), first T0 diner shift (5–10pm), sleep | F0 R0 J0 | Hub-and-event basic flow; sidebar renders 4 items |
| 2 | Tue | Frank kitchen M (Stage-0 branch fires on chance roll), help Ryan yard A (+trust, `ryan.help_count=1`), walk past Jake's room A (jake.peek_count=1; first-glance sub-branch inside `scene_jakes_doorway` fires → sets `jake_first_glance_noticed = true`; helper `jake_stage_1()` then advances `npc_jake_stage` to 1), diner T0 | F0 R0 J1 | First stage transition; E11 sidebar updates "Jake: Noticed"; E10 hint rotates |
| 3 | Wed | Bookkeeping with Frank (`frank.bookkeeping_count=1`, +trust), Ryan yard A (`ryan.help_count=2`), shower → beauty 45, sketch in bedroom → beauty 47, walk past Jake (peek_count=2), diner T0 | F0 R0 J1 | Daily-tick reset visible Day 2→3; counter increments visible |
| 4 | Thu | Bookkeeping (`bookkeeping_count=2`, trust=18), Ryan yard help (`help_count=3`, trust=12), beauty 50 → `jake_stage_1()` solidified, walk past Jake (peek_count=3 → eligible for Stage 1→2 trigger if corruption ≥ 30; corruption ~25 — not yet), diner T0 (rep_road=8) | F0 R0 J1 | E2 decay visible (Frank trust would have fallen if not maintained — log shows interaction-skip semantics) |
| 5 | Fri | Bookkeeping (`bookkeeping_count=3`, trust=22) → `frank_stage_1()` clears → `npc_frank_stage=1` AT NEXT DAILY TICK / canvas entry. Sidebar updates "Frank: Grudging warmth." Hint rotates. New scene_kitchen_with_frank Stage-1 branch fires on chance roll. New "Sit on porch" button at hub_back_porch E-band. Ryan yard (`help_count=4`). `group_settled_in` flips at Day 4 end (3 of 4 conditions). `ryan_stage_1()` clears → `npc_ryan_stage=1` → Sidebar "Ryan: Helper" → new "Help close customer" at shop hub. Diner T0. | **F1 R1 J1** | Two natural stage transitions in one day; E10 multi-NPC hint rotation; E4 helpers driving derived flags; E11 visible movement |
| 6 | Sat | Frank kitchen M Stage-1 (paper warmth, asks about numbers). Ryan small-ticket close at shop (+$15, `help_count=5`). Walk past Jake A (peek_count=3 already; corruption now ~30 from accumulated diner shifts — `jake_stage_2()` natural advance triggers via `event_jake_peek_draw_revealed` inside scene_jakes_doorway evening). Sidebar "Jake: Peek/Draw." Diner T1 unlocks (corruption 30 ≥ 25 + rep_road ~14 → ~15 by next shift + beauty 50 ≥ 45). | F1 R1 J2 | Doctrine principle: stat threshold unlocks NEW MENU OPTION (T1), not new prose. Three NPC stages visible in sidebar |
| 7 | Sun | **Rent due.** First Sunday morning event — pay $60 (sets `first_rent_paid` + `first_sunday_passed`). Diner closed Sunday. Maya can: church front (rep_church +1), porch with Diana (diana_awareness ticks), sketch, sleep. Frank's `frank.tease_count` and tease buttons are NOT yet in scope (Stage 2 not reached). | F1 R1 J2 | F4 rent system + eviction_mode validation (player has $400 + earned ≈ $250 over week — passes easily) |
| 8 | Mon | Player chooses to do solo activity in living room E-band when Frank scheduled home → corruption now ~35–40, **likely below 45** — catch one-time branch checks gate, doesn't fire (gate fail logged in dev mode). Player notices, instead pursues T1 diner shift to push corruption. **OR** — alternate path — player has been ignoring Jake entirely (didn't peek again past Day 4). Stalled-stage hint for Jake fires (E9: 7-day window from `npc_jake_stage` last advancement Day 6 — won't trigger this slice timeline; **the cleaner E9 test is to ignore one NPC across the whole slice, see §10**). | F1 R1 J2 | E9 stalled-detection observable in dev playthrough variant |
| 9 | Tue | Corruption now ~45+ (cumulative from T1 + ambient). Player tries living-room solo E-band again — `frank_caught` one-time branch fires this time. Player choice resolves to `frank_restrict_declared = true`, `npc_frank_stage = 2`. Sidebar "Frank: Restrict." Hint rotates. Hub_kitchen and hub_living_room get chore buttons (porch sweep, kitchen cleanup). text_variants: "Talk to Frank" → "Talk to Frank — about it." | **F2** R1 J2 | One-time guard branch; multi-flag write; text_variants render; chore buttons appear at hubs |
| 10 | Wed | Frank kitchen M Stage-2 branch (he doesn't look up; "Porch needs sweeping. Before you sit."). Activity_morning_chore (`frank.chore_count=1`). All three NPCs at viable mid-arc stages. End of slice. | F2 R1 J2 | Final state snapshot; cascade depth 3 axes (stage × band × tier) verified |

**End-state expected:** F2 R1 J2 with money ≈ $400 starting + $250 diner − $60 rent − ~$30 groceries (if economy drains modeled) ≈ $560; corruption ~50; sub-rep_road ~22; full hint pool rotated through 7+ different hint texts; daily-tick fired 9 times; trait decay observable on at least one neglected axis.

---

## 7. Canvas inventory

Tagged **REUSE** = lift from existing `the_long_summer/toml_phases/`, light edit at most. **AUTHOR** = new for this slice.

### 7.1 Hubs (Type-A shared, Type-B NPC personal, Type-C outdoor) — all `is_repeatable = true`, low priority

| ID | Type | Tag | Purpose |
|---|---|---|---|
| `hub_mayas_bedroom` | B | AUTHOR | Solo morning hub: shower, sketch, sleep, walk to hallway |
| `hub_hallway` | A | AUTHOR | Transit between bedroom, kitchen, living room, Frank's office (gated), back porch |
| `hub_kitchen` | A | AUTHOR | Diana anchor; Frank scheduled M + DINPREP; eat from fridge, help Diana, talk Frank, talk Diana; first Sunday morning branch (gated `first_sunday_passed == false`) fires rent prompt |
| `hub_living_room` | A | AUTHOR | Evening: solo activity available; one-time Frank catch branch |
| `hub_franks_office` | B | AUTHOR | Schedule-gated visibility (Frank present); bookkeeping button at Stage 0/1; "Linger by desk" at Stage 3 (dev only) |
| `hub_back_porch` | A | AUTHOR | E-band: Frank present; "Sit with Frank" button at Stage 1+ |
| `hub_yard` | C | AUTHOR | Ryan scheduled 08–15; help him work, watch him, bring water; small-ticket close gated to Stage 1 |
| `hub_jakes_doorway` | B | AUTHOR | A-band: Jake usually in his room; walk-past state-pump (peek_count++); door interactions per stage |
| `hub_main_street` | C | AUTHOR | Town container; navigate to diner front, general store, church front (Sun) |
| `hub_diner_front` | C | AUTHOR | Marge present all day Mon–Sat; first visit fires Marge interview branch (gated `hired_at_diner == false`); Maya's shifts T0/T1; Cookie evening overlap |

### 7.2 Scenes (Type-3 — where prose lives, single-node multi-group cascade per `04_Scene_Cascade_Pattern.md`)

| ID | Tag | Stages covered (natural) | Stages covered (dev fragment) |
|---|---|---|---|
| `scene_kitchen_with_frank` | AUTHOR | 0, 1 (×M+DINPREP), 2 | 3, 4 |
| `scene_kitchen_with_diana` | AUTHOR | ambient — Diana awareness band variants only |
| `scene_yard_with_ryan` | AUTHOR | 0, 1 | 2, 3, 4 |
| `scene_jakes_doorway` | AUTHOR | 0 (with first-glance one-time sub-branch gated `jake_first_glance_noticed == false AND beauty >= 40`; sub-branch sets `jake_first_glance_noticed = true`, then helper `jake_stage_1()` computes Stage 1 advancement on the same engine cycle), 1, 2 | 3, 4 |
| `scene_franks_office_supervised` | AUTHOR | 2 (chore-supervision) | 3 (tease cascade) |
| `scene_living_room_evening` | AUTHOR | (always-fires hub branch holding the catch one-time guard) |
| `scene_diner_t0_shift` | AUTHOR | T0 (5h block, 1–2 customer beats, +$45 base) |
| `scene_diner_t1_shift` | AUTHOR | T1 (gates corruption ≥ 25 + rep_road ≥ 15 + beauty ≥ 45; +$45 + $8–20 tips) |

### 7.3 Activities (routers + state-pumps)

| ID | Tag | Notes |
|---|---|---|
| `activity_sleep` | REUSE (already in `toml_phases_v2/3_activities_v2.toml`) | Resets energy + clears all `*_today` flags via E5 daily_tick |
| `activity_shower` | AUTHOR | +hygiene; +beauty (small); ONE fixed paragraph + image-block with 4 search_queries |
| `activity_sketch` | AUTHOR | +calculation tiny; +beauty tiny; rest-mode; ONE fixed paragraph + image-block with 3–5 search_queries |
| `activity_eat_from_fridge` | AUTHOR | -money $5; +energy small |
| `activity_help_diana_kitchen` | AUTHOR | +diana.awareness +1; sets `helped_diana_today`. Forward-looking Phase 2+ seed per Doc 02 §"Diana — `diana_stage` (Phase 2+ deferred)": `diana.awareness` accumulates silently in this slice; gates Diana's eventual arc once authored. Not in-slice decoration — explicit forward-state seed |
| `activity_bookkeeping_with_frank` | AUTHOR | Schedule-gated to Frank in office; `<<inc frank.bookkeeping_count>>`; +money $5–10; +trust 1 |
| `activity_help_ryan_in_yard` | AUTHOR | Schedule-gated to Ryan A-band; `<<inc ryan.help_count>>`; +trust 1; ONE fixed paragraph + image-block with 3–5 search_queries |
| `activity_walk_past_jakes_door` | AUTHOR | A-band; daily-cooldown `walked_past_jakes_today`; `<<inc jake.peek_count>>` |
| `activity_morning_chore` | AUTHOR | Stage 2+ Frank only; sets `did_morning_chore_today`; `<<inc frank.chore_count>>`; +money $5; supervision tone |
| `activity_walk_to_town` | AUTHOR | Bedroom/yard → main_street; 60-min progression |
| `activity_walk_property` | AUTHOR | 30-min loop; +fitness small |

### 7.4 One-shots (true non-repeatable, `is_repeatable = false`)

Per the doctrine: list stays under 10. This slice has **3 narrative + 1 dev** (audit §2.7/§2.8 cleanup — count was 4 + 1 before the Jake first-glance fold):

| ID | Tag | Purpose |
|---|---|---|
| `event_test_slice_intro` | AUTHOR | Day 1 06:30 wake-up frame; hands player to `hub_mayas_bedroom`; sets `slice_started` |
| `canvas_marge_interview` | AUTHOR | First visit to `loc_diner_front`; sets `hired_at_diner` |
| `canvas_first_sunday_morning` | AUTHOR | Day 7 Sunday morning at `loc_kitchen`; rent prompt + church choice; sets `first_sunday_passed` |
| `event_partner_invitation` | AUTHOR — DEV ONLY | Force-open Ryan Partner gate for dev verification |

**Implementation note (audit §2.8 + §13 framing):** the engine has no separate "hub canvas" — `loc_<x>` IS the hub. Per Doc 01's decision tree, "first time you do X" beats want to be flag-gated branches inside repeatable shells. Engine-wise this is achieved either as (a) a literal `group` block with conditions inside a host repeatable canvas, OR (b) a high-priority one-shot canvas at the host location gated on `<flag> == false`. Both have identical firing semantics. The slice uses (a) for the Jake first-glance moment (folded into `activity_walk_past_jakes_door` Stage-0) and (b) for the Marge interview, first Sunday rent prompt, and Frank catch (`scene_living_room_evening`). All four fire once, gate on a guard flag, retire after their flag is set.

### 7.5 Dev shortcuts (hidden behind `dev_mode` flag in `[player.flag_keys]`)

Per user lock — engine validation allows these. Each dev canvas: `is_repeatable = true`, `priority = 1`, gated on `flag dev_mode_enabled == true`, with a sentinel button at hub_mayas_bedroom labeled "🔧 Dev: …". Stripped before any player slice.

| ID | Effect |
|---|---|
| `dev_advance_frank_to_3` | `npc_frank_stage = 3` + `frank_restrict_declared = true` + corruption=60, frank.arousal=30 |
| `dev_advance_frank_to_4` | `npc_frank_stage = 4` + `frank_cracked = true` |
| `dev_advance_ryan_to_2` | `npc_ryan_stage = 2` + `ryan_partner_open = true` + corruption=30 |
| `dev_advance_ryan_to_3` | `npc_ryan_stage = 3` + corruption=75 |
| `dev_advance_jake_to_3` | `npc_jake_stage = 3` + `jake_caught = true` + corruption=50 |
| `dev_advance_jake_to_4` | `npc_jake_stage = 4` + `jake_hand = true` |
| `dev_force_catch` | Force-fires `frank_caught` one-time branch regardless of corruption gate |
| `dev_skip_to_day_8` | Pumps `current_day` forward 7 days for E9 stall verification |
| `dev_zero_trust_frank` | Zeros `npc_frank.trust` to test decay-driven stage regression visibility |

The `dev_mode_enabled` flag is also used to gate a state-snapshot dump button that prints all relevant flags/traits/counters to the screen — for grading playtest validations.

---

## 8. Schedule slice (which time-bands matter)

Reuse the existing TLS schedule grid (already wired in `toml_phases_v2/1_metadata_and_locations.toml`). The slice uses these overlaps:

| NPC | Day pattern | Maya overlap that the slice exercises |
|---|---|---|
| Frank | Mon–Fri kitchen 06:30–07:30, away M+A, kitchen DINPREP, office E (Maya may visit), back porch E (after `frank_stage >= 1`) | Kitchen M, kitchen DINPREP, office E, porch E |
| Ryan | Mon–Fri yard 08:00–15:00, dinner DIN, porch E | Yard A (08–15) |
| Jake | Mon–Fri room mostly (09–17 sketching), brief kitchen 17–18, dinner DIN, room E | Doorway A (13–17 — Jake's deepest isolation window per book) |
| Diana | Daily kitchen 05:30–08:30 + 17:00–20:30 | Kitchen M + DINPREP (overlapping Frank) |
| Marge | Mon–Sat diner 06:00–22:00 | Diner front during Maya's shifts |
| Cookie | Mon–Sat diner 17:00–22:00 (cook shift) | Maya T0/T1 evening shifts |

Locations close per book §9 (NLP-style "you can't go here right now"): diner closed Sundays; Frank's office gated by Frank-present; Jake's room interior locked until Stage 3 (slice doesn't open it via natural play).

---

## 9. Sidebar configuration

Reuse all 7 existing sidebar items from `toml_phases_v2/1_metadata_and_locations.toml` (player corruption + calculation; Frank/Ryan/Jake love bands gated by their reveal flags). **ADD three `stage_label` items** per E11 fixture pattern:

```
[[sidebar_items]] type="stage_label" npc_id="npc_frank" prefix="Frank"
[[sidebar_items]] type="stage_label" npc_id="npc_ryan"  prefix="Ryan"
[[sidebar_items]] type="stage_label" npc_id="npc_jake"  prefix="Jake"
```

Stagger math from `2b_systems_budget.md` allows ≤4 visible at once. The three new stage_label items are gated by the same `show_when` clauses as their love-band counterparts (so Ryan's stage label only appears once `ryan_help_tier_open == true` — same time as his love band reveals). Day-by-day visible-count budget:

- Day 1 morning: corruption + Frank love (pre-seeded) + calculation = 3
- Day 2 after Jake glance: corruption + Frank love + Frank stage_label + Jake love + Jake stage_label = **5 — exceeds budget.**

**Resolution (locked):** when both want the slot, hide love bands. Stage labels are the doctrine-driven progression signal; love bands are legacy. The `show_when` clauses on the love-band sidebar items get extended with `AND <npc>_stage_label_visible == false` — when an NPC's stage_label reveals, that NPC's love band hides. Authoring-side: a small `<npc>_stage_label_visible` flag gets defined in `[player.flag_keys]` and toggled by the same `show_when` mechanism the stage_label sidebar item already uses.

---

## 10. Stage-gated hints (E10 templates)

Author 12 templates total (4 per arc NPC × 3 NPCs), distributed across stages 0/1/2 with one stage-stall fallback per NPC. Lift the Maya-voice hints from `2b_systems_budget.md` §6 where they exist; author the remainder in the same voice.

Per-NPC structure:
- **Stage 0 hint** — what to do to advance ("Frank's porch at nine. He doesn't talk much but he notices when I sit down.")
- **Stage 1 hint** — the next ask ("The bookkeeping pays. It's an hour. I can sit through an hour.")
- **Stage 2 hint** — the post-catch register ("Every time he corrects me the correction is longer than it needs to be.")
- **Stage-stall fallback** — fires only when E9 stalled-detection triggers AND the NPC's stage_advancement_log day is the oldest (per E9 hook). One stall hint per NPC.

`[story_arc.hints]` block:
- `stuck_threshold_days = 7`
- `stage_stall_message = "Days are passing. Maya feels herself standing still — maybe one of these arcs needs a fresh approach."`

**Validation walk-through** for E9: there's a "neglect Jake" play variant — player who never peeks past Day 4 has Jake stuck at Stage 1 from Day 2. By Day 9 (7+ days since `npc_jake_stage` last advanced), the stall hint fires in the Quests page. This is one of the documented validations in §3 row 10.

---

## 11. Income / economy

Three channels active.

| Channel | Pay | Gate | Slice usage |
|---|---|---|---|
| Diner T0 base wage | $45 / 5h shift | `hired_at_diner` (Day 1 evening) | Maya's default income. ~5 shifts in 10 days = $225 |
| Diner T1 tips | $45 + $8–20 | corruption ≥ 25 + rep_road ≥ 15 + beauty ≥ 45 | Unlocks Day 6 in walkthrough; ~3 shifts = $50–60 tips on top |
| Ryan small-ticket cut | $10–25 / close | `ryan_help_tier_open` (Day 5) | 2–3 closes Day 6–10 = $30–60 |
| Frank chores (post-catch) | $5–20 / task | `frank_stage >= 2` | Day 9–10 = $15–30 |

**Rent:** $60 due Sunday Day 7. Existing `[settings.rent]` config kept (eviction_mode = `flag_set`, grace_periods = 2). With $400 starting + ~$225 by Day 7, player sits comfortably above $60.

**Math purpose:** demonstrate Income channels 1 + 2 + 5 work as the systems budget claims, and rent fires correctly. Big-ticket / Tier 3 explicitly out of scope.

---

## 12. Engine wiring additions to TOML

These get added in metadata/systems sections of the new slice game (parallel structure to engine_prd_phase2 fixture):

- **`[engine.daily_tick]`** — `flagEffects` array unsetting all `*_today` flags. ~10 entries (talked_to_frank/ryan/jake/diana/marge/cookie_today, helped_diana_today, did_morning_chore_today, walked_past_jakes_today, watched_ryan_today).
- **`[[engine.stage_helpers]]`** — 7 entries: `frank_stage_1`, `frank_stage_2`, `frank_stage_3`, `ryan_stage_1`, `ryan_stage_2`, `jake_stage_1`, `jake_stage_2` (composite gates referencing trait + flag conditions per E4 syntax).
- **`[[npcs]].arc_stages`** on Frank, Ryan, Jake (5-element arrays per stage chain tables in §5).
- **Three `stage_label` `[[sidebar_items]]`** per §9.
- **Player core_traits additions:** `npc_frank_stage = 0`, `npc_ryan_stage = 0`, `npc_jake_stage = 0`, plus the counters (`frank.bookkeeping_count` etc.).
- **`[story_arc.hints]`** block with `stuck_threshold_days`, `stage_stall_message`, and 12 templates per §10.

No engine code changes needed — every feature used is already shipped.

### §12.1 Engine reality note — helpers don't auto-write the stage trait

Engine audit (`v1.py:2718-2735`, `v1.py:4017-4025`) confirms:

- `[[engine.stage_helpers]]` (E4) emits a `setup.stage_helpers_map` lookup that the `type = "stage"` condition operator queries via `setup.triggerConditionsSatisfied`. **This is gate-check only.** Helpers return a boolean; they do not have side effects.
- `setup.applyAndNotifyTrait` (E9 hook) *records* stage advancements when a `<slug>_stage` trait moves upward (stamps `stage_advancement_log[slug] = current_day`). It does not *cause* the advancement.

Implication: the §5 phrasing "helper-derived consequence — engine writes the stage value in the same engine cycle" is doctrinally aspirational but engine-realistically requires an explicit trait write somewhere. The slice implements stage transitions in two shapes, both engine-real:

- **For "helper-driven" transitions** (Frank 0→1, Frank 2→3, Ryan 0→1, Jake 0→1 via beauty path, etc.) — one **transition canvas** per advancement: `is_repeatable = false`, high priority, located where the player most plausibly is when the helper clears, gated on `(stage helper) AND (current stage trait == old value)`. Body: one tiny transition paragraph (the moment of recognition). Exit `effects` writes `<slug>_stage = new_value`. Auto-pre-empts the hub on next visit.
- **For "branch-inside-shell" transitions** (Frank 1→2 catch, Frank 3→4 Crack, Jake 0→1 via first-glance) — a `group` block inside the host hub/scene, gated on the catch/glance/crack conditions. The group's exit choice writes BOTH the input flag(s) AND the stage trait directly. One-time-fire achieved by gating the group on `<guard_flag> == false`.

The helper still serves as the **single-source threshold check** on the transition canvas's trigger — tuning a helper propagates to every gate site via the `type = "stage"` condition. Authors edit one helper definition; every gate that references it shifts in lockstep. The trait-write happens at one site per transition (the canvas / branch).

Net file impact: §13 critical-files gains a `4b_stage_transitions.toml` (or the transitions fold into `5_hubs_and_scenes.toml` — decision deferred to authoring time). Roughly 6–8 transition canvases (Frank 0→1, 2→3, 3→4; Ryan 0→1, 1→2; Jake 0→1, 1→2, 2→3) — three of them dev-button-only per §7.5.

---

## 13. Critical files

This slice creates a NEW game folder, parallel to `the_long_summer/`:

- **CREATE** `games/the_long_summer_test/` (new directory)
  - `concept.md` — one-paragraph slice description
  - `toml_phases/0_systems_spec.toml` — engine wiring (daily_tick, stage_helpers)
  - `toml_phases/1_metadata_and_locations.toml` — start from `the_long_summer/toml_phases_v2/1_metadata_and_locations.toml`; ADD `arc_stages` to NPCs + `stage_label` sidebar items + stage core_traits + counters
  - `toml_phases/2_story_canvases.toml` — the 2 true one-shots from §7.4 (intro + dev partner invitation)
  - `toml_phases/3_activities.toml` — the 11 activities from §7.3 (lift `activity_sleep` from v2)
  - `toml_phases/4_story_arc.toml` — `[story_arc.hints]` block from §10
  - `toml_phases/5_hubs_and_scenes.toml` — NEW phase file: 10 hubs + 8 scenes from §7.1, §7.2 (the heaviest authoring)
  - `toml_phases/6_dev_shortcuts.toml` — the 9 dev canvases from §7.5
  - `toml_phases/7_final_game.toml` — concat of 0–6
  - `output/index.html` — compiled output
  - `confabulation.md` — the registry per §3 row 20 (every invented detail logged)
  - `playtest_log.md` — observed stage transitions, validation pass/fail per §3 row
- **REUSE — read only:**
  - `games/the_long_summer/output/videos/` (or media folder) — reference for media file paths (slice uses same image/video references as Phase 1 game where surfaces overlap; new surfaces get search_queries blocks per `01` Doctrine §"Doctrine checklist" item 7)
- **NO changes to engine code.** No changes to existing `the_long_summer/` content. No changes to existing tests.

### Build command (the package_from_toml invocation)

```
source venv/bin/activate
python manage.py package_from_toml \
  --file games/the_long_summer_test/toml_phases/7_final_game.toml \
  --owner-id <uuid> \
  --output games/the_long_summer_test/output \
  --dev \
  --video-folder games/the_long_summer/output/videos
```

`--dev` flag enables sidebar stat-adjustment controls (independent of our `dev_mode_enabled` flag — both useful in playtest).

---

## 14. Verification plan (browser playtest)

Open the compiled `output/index.html` in a browser. Run through the §6 day-by-day walkthrough. For each row in the §3 mechanism checklist, confirm:

| # | Pass criterion |
|---|---|
| 1 | Hubs render every visit; scenes fire from triggers, not from menu links |
| 2 | Visit kitchen Day 2 / Day 5 / Day 9 — observe three different paragraphs |
| 3 | Frank Stage-1 morning vs DINPREP visible — different surfaces |
| 4 | Trigger `frank_caught` on Day 9; revisit living room evening — branch does not re-fire |
| 5 | Day 5 morning: Frank stage_label flips "Suspicious"→"Grudging warmth" without any direct stage-set call |
| 6 | Day 2 sleep → Day 3 morning: hub_kitchen shows "Talk to Frank" again (was used Day 2) |
| 7 | Skip Ryan for Days 6–10; confirm `npc_ryan.trust` decays per declared rate |
| 8 | Counter values visible in dev state-snapshot button output |
| 9 | Quests page: Frank hint changes Day 5 (after stage flip), Day 9 (after catch) |
| 10 | Run "neglect Jake" play variant → Day 9 Quests page shows the stall message |
| 11 | Sidebar visibly updates 3× across the 10-day playthrough for each NPC |
| 12 | Hub_kitchen "Talk to Frank" label changes after Day 9 catch |
| 13 | Daily-tick log line in dev mode confirms ~10 unset operations per day |
| 14 | Visit kitchen 5× in same band — encounter only fires ~1.5 times on average |
| 15 | Sleep, shower, sketch each show different opening across consecutive uses |
| 16 | Day 7 Sunday: rent prompt fires; pay $60; sidebar money decrements |
| 17 | Sidebar `rep_road` band advances from "Just hired" to next band by Day 6 |
| 18 | Diner hub shows new T1 button row Day 6+ that wasn't there Day 5 |
| 19 | Audit canvas word counts during authoring; nothing exceeds the doctrine cap |
| 20 | `confabulation.md` populated as authoring proceeds; zero entries with "no payoff" disposition at slice ship |

For each dev button, also verify that force-advancing renders the correct stage cascade branch without error.

**Exit criteria for the slice:** all 20 mechanism rows pass; the 9-day natural-progression walkthrough lands at end-state F2 R1 J2 within ±1 stage of expectation (some divergence acceptable based on chance rolls); no console errors; no stuck states; no flags-without-payoff in `confabulation.md`.

---

## 15. What this plan does NOT cover

- **The rewrite of the existing `the_long_summer/` content.** This slice is parallel — it doesn't migrate Phase 1 canvases or touch `toml_phases_v2/`.
- **Voice register polish.** Doctrine density caps must hold; literary register polish is a follow-up pass.
- **Round 2 of `02_NPC_Stage_Chains.md`** (full Ryan/Jake/Diana/Cookie chains in the doctrine doc). The slice lifts master spec §6 inline but doesn't update the doctrine doc itself.
- **Confabulation registry (`04_Confabulation_Registry.md`)** as a global Phase 2 artifact. Slice keeps its own local `confabulation.md`; promotion to global comes later.
- **Phase 2+ content stubs** (Diana arc, shadow layer, calendar events, etc.) — explicitly deferred per §2B `Game_Redesign.md`.

---

## 16. Effort estimate

Engine = 0 hours (already shipped). Authoring breakdown:

| Block | Hours |
|---|---|
| Concept doc + slice metadata | 0.5 |
| §12 engine wiring TOML (daily_tick, stage_helpers, arc_stages, sidebar adds, hints) | 1.5 |
| 10 hubs (50–300 chars each) | 2 |
| 8 scenes with stage cascades (Frank kitchen is the heaviest at ~600 words; others 200–400) | 8 |
| 11 activities with fixed prose + image-block search_queries | 4 |
| 5 one-shots | 2 |
| 9 dev canvases | 1 |
| Compile + browser playtest run + 20-row validation | 3 |
| Two additional play variants (neglect Jake; aggressive Frank push) | 2 |
| Doc passes (confabulation registry; playtest log) | 1 |

**Total: ~25 hours.** Spreadable across 3–4 focused sessions.

---

## 17. Cross-references

- **`00_TLS_Phase2_Diagnosis_and_Direction.md`** — diagnosis this slice is the corrective playtest for.
- **`01_Repeatable_First_Doctrine.md`** — vocabulary + doctrine checklist every authored canvas honors.
- **`02_NPC_Stage_Chains.md`** — Frank chain lifted directly; Ryan/Jake chains lifted from the master spec inline in §5.
- **`04_Scene_Cascade_Pattern.md`** — every scene in §7.2 follows this shape (single-node multi-group, stage outermost → band → tier).
- **`08_Engine_PRD_Phase2_Additions.md`** — E9/E10/E11 implementation cited as the wiring contract for §12.
- **`archive_02_TLS_Rewrite_Spec_2026-04-29.md` §6** — Ryan/Jake stage tables source.
- **`book_phases/2b_systems_budget.md`** — income channels (§11), hint voice (§10), sidebar stagger math (§9).
- **`apps/game_generation/games_toml_files/engine_prd_phase2_2026_04_29.toml`** — the minimal Phase 2 fixture this slice scales up from.

---

## 18. What this doc is not

It is not the implementation. It is not TOML. It is not the prose for any canvas — every authored cascade body gets written during execution, against the doctrine's density caps. It is not a player-facing slice spec — dev shortcuts, pre-seeded state, and unstripped meta will all be in the compiled output.

It is the production order, scope decision, and validation checklist for the first non-trivial Phase 2 fixture. When the slice ships and all 20 mechanism rows pass, the doctrine has been validated end-to-end; the way is clear for Phase 2 vertical-slice authoring of the real game.

---

End of plan.
