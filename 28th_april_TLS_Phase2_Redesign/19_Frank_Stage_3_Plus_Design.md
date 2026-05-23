# 19 — Frank Stage 3+ Design (Phase-2-learnings-aligned)

> **Status:** Design spec, not implementation. Authored 2026-05-04 after a Stage-3 hint cliff in live play surfaced that Frank has no authored content past Stage 2 in the Quests UI — even though canvas content for Stage 3 (`scene_office_after_crack`) and fragments for Stage 4 already exist. Triggered a deliberate ignore-prior-iterations design pass: docs 02 and 18 are treated as iteration work; only the **portable Phase 2 learnings** carry forward. This doc supersedes doc 02 §"Frank — full chain" Stage 4 and lifts doc 18 §D3. Implementation comes in subsequent plans, ordered per §8.

---

## §1 Purpose & relationship to docs 02 / 16 / 18

This is a **fresh capstone-and-texture design for Frank from Stage 3 onward**, written by applying Phase 2's portable learnings rather than extending the prior iteration designs. It deliberately discards two specific prior designs:

- **Doc 02 §"Frank — full chain" Stage 4 spec** (4 keep-routes — `romantic`, `arrangement`, `rupture`, `power_inverted` — each with per-route bedroom branches, route flags, and a route-selection mechanism). **Dropped.** Per the single-digit one-shot doctrine (doc 01) and sandbox-emergent-not-pre-authored doctrine (doc 15), 4 pre-authored routes is infrastructure-heavy capstone work that produces a branching tree of content where state-driven internal cascades would produce the same emergent variety more cheaply.
- **Doc 18 §D3 ("Stage 3→4 deferred").** **Lifted.** D3 was a *slice-budget* call (10-day window), not a design call against Stage 4. With slice scope reframed as a longer build, Stage 4 is now in scope as a single capstone moment + a new bedroom surface, not a 4-route system.

What stays preserved from prior docs:
- **Doc 16 §2 voice rules** — Frank stays terse, sensory, no academic vocabulary, no apologizing. Voice is invariant across stages; only the *register* shifts.
- **Doc 18 §5/§6** — Stage 2→3 crack moment + `scene_office_after_crack` Tier-3 anchor. Already-shipped baseline; this doc augments rather than rewrites.
- **Doc 16 D1** (RTS-flat default + Tier-3 carve-out for stage capstones) — **preserved**. New Stage 4 bedroom canvas qualifies for the carve-out as a stage-flag capstone.
- **Doc 16 D2** (existing scenes = polish, not full rewrite) — **preserved**. Stage 0/1/2 prose stays untouched.

**Scope:** Frank only. Stage 3 surface expansion + Stage 3→4 transition capstone + Stage 4 register & bedroom unlock. **No Stage 5** — Stage 4 is terminal until summer-end (the global terminal event, not a Frank-arc decision). Ryan and Jake get analogous redesigns in subsequent docs on the same template.

---

## §2 Phase 2 learnings applied (the design lens)

Ten learning categories from Phase 2 docs 00 / 01 / 04 / 13 / 14 / 15 / 16 / 17, applied here as:

- **Capstone vs daily-texture layer separation** (doc 15 §5, doc 02 §"Update 2026-05-03"). Stage 4 entry = capstone (one-shot bedroom invitation). Stage 4 ongoing = daily texture (5 surfaces' register shifts). The two layers do not share authoring infrastructure.
- **Repeatable + internal cascade > new canvases** (doc 01 §"Same passage, different stage"). Stage 3 surface expansion adds `[group]` blocks inside existing canvases; Stage 4 adds *one* new canvas (bedroom) and otherwise also augments existing surfaces with new groups.
- **Single-digit one-shot ledger** (doc 01). Frank's one-shot count after this design = 4 (see §7). Doctrine-compliant.
- **Tier discipline** (doc 13 §9, doc 16 §4). Stage 3 expansion is 5 T2 vignettes — *no* new T3 at Stage 3. Stage 4 adds 1 T3 (bedroom anchor) + 1 T3 (the transition capstone) + 3-4 T2 group blocks. T3 ratio for new content stays within the 23-30% RTS budget.
- **Voice doctrine** (doc 16 §2). Terse, names things not feelings. Stage 3+ register escalation does not change voice — Frank still says "Sit." not "Please be seated." The register lives in *what* he says, not how he says it.
- **Surface multiplexing via `[group]` blocks** (doc 04 "Precedence order: Stage → Time-band → Tier"). Every stage flag should be expressed across kitchen / office / living room / back porch surfaces; failure to multiplex (current Stage 3 only landing in the office) is the bug this doc fixes.
- **Sandbox lens** (doc 15 §6). Variety emerges from state moving and internal cascades, not from pre-authored choice trees. This is why Stage 4 is one transition with one outcome, not a 4-route fork.
- **Walkthrough transparency** (doc 13 §6, doc 14 S3). Every stage threshold publishes in the Quests/Walkthrough panel. Stage 3→4 gate becomes legible to the player as a counter ("Frank office visits: 2 / 3"), not a hidden trigger.
- **Anti-patterns to avoid** (doc 00). No establishment sequences (Continue / Continue / Continue). No flag-without-payoff (every new flag is consumed). No monolithic literary tics (don't repeat the "kitchen smelled like burnt coffee" construction 8× in new content).
- **Single-source counters** (doc 18 §3 lesson). New counter `frank_office_visits` increments only at `scene_office_after_crack` choice exits. Pattern matches retired `frank_bookkeeping_count` discipline — no opaque per-NPC counters.

---

## §3 Stage 3 surface expansion — daily texture layer

Stage 3 currently lands on exactly one surface that *does* anything: `scene_office_after_crack` (T3 evening sex, repeating). Every other location either reads at Stage-2 register or shows a 1–2 line stub. This violates the cascade pattern (doc 04) and the daily-texture doctrine (doc 15 §5).

The fix is **5 T2 vignettes inside existing canvases** as new `[group]` blocks gated `npc_frank_stage = 3`. No new canvases. No new T3.

| Surface | Time band | Register intent | Tier (target words) | Internal-branch conditions |
|---|---|---|---|---|
| **Kitchen morning** (`scene_kitchen_with_frank_morning`) | M (06:30-08:30) | Frank watches Maya cross the kitchen, says less than usual, the new charge sits between them. Bookkeeping pretense holds in the daytime register. | T2 (~80) | Branch on `frank_office_first_sex_done` (different beat first morning after the office vs subsequent mornings). |
| **Kitchen evening** (`scene_kitchen_with_frank_dinprep`) | DINPREP (17:00-19:00) | Frank close in the kitchen pre-dinner, instructional in a way that's not about food. Diana-aware (silent accumulator ticks). | T2 (~60) | None — single beat. |
| **Office daytime** (~~`scene_franks_office_supervised` daytime band, NEW group~~ — **DEFERRED 2026-05-04**) | weekday 10:00-16:00 | Door open. Bookkeeping is still bookkeeping during the day. No charge. Negative space is currently expressed by the absence of any daytime office canvas. | T2 (~50) | **Deferred** — `scene_franks_office_supervised` is gated to evenings (19:00-21:30) only and the engine has no time-of-day condition support inside `[group]` blocks. Expanding the schedule would also surface Stage 2 daytime register (wrong). The natural fix is a small new daytime canvas, but that violates the §3 "no new canvases" rule. Negative space (no daytime office content) achieves the design intent — the player learns that Stage 3 office is evening-only by trying daytime and finding the room empty. Re-evaluate during Step 6 if a daytime register beat is needed. |
| **Living room evening** (existing canvas at `loc_living_room`) | E (19:00-22:00) when Maya isn't in the office | Frank on the chair, Maya passes through, his eyes don't leave her. Brief. | T2 (~40) | Branch on `talked_to_frank_today` (one variant if Maya already had her office evening, another if she's heading there). |
| **Back porch dusk** (existing back porch canvas) | DUSK (18:00-19:00) | Frank smoking. *"Coming back inside?"* — the question is the invitation. | T2 (~50) | None — single beat. |

Implementation pattern is the standard `[group]` block per doc 04. Each group has `conditions = { items = [{ type = "trait", trait_key = "npc_frank_stage", operator = "eq", value = 3 }, ...optional time/flag refinements ] }` and a `blocks = [...]` array of paragraph + dialog primitives.

**Diana-awareness:** the kitchen evening and living room vignettes write `+1 diana_awareness` (silent accumulator per doc 16). No visible UI tick — it accumulates against future Diana-arc gates.

---

## §4 Stage 3→4 transition — the new capstone

The Stage 2→3 crack was Frank breaking his own rule (doc 18 §5). Stage 3→4 is **Frank deciding the office is too small for what they're doing now.** It is *his* call, not Maya's — the player can't grind their way to it; Frank has to be ready.

### Trigger

Branch-inside-shell at `scene_office_after_crack`. After the office sex finishes, before the choice exits, a one-time guard fires when:

```
AND:
  frank_office_first_sex_done is_true
  frank_invited_to_bedroom is_false       # one-time guard
  Frank.corruption >= 25                  # he's the gate, not Maya
  frank_office_visits >= 3                # 3 prior office sessions
  talked_to_frank_today is_false          # fresh evening visit (not same-day re-entry)
```

`frank_office_visits` is a **new counter** introduced specifically for this gate. Single-source: increments only via the choice exits in `scene_office_after_crack`. No opaque per-NPC counter ambiguity (doc 18 §3 lesson preserved).

### Branch content

Tier-3 capstone, ~250-300 words. Branch fires after the existing climax paragraphs but before the standard choice exits. Frank doesn't dismiss her — he stands instead. Voice spec:

- Terse. No explanation, no soft-pedal. Frank initiates.
- Names the venue and the time. *"Not in here next time. Upstairs. Same hour."*
- Acknowledges Diana exists without making her the subject. The beat is between Frank and Maya; Diana is the room next door.
- One Maya line max. One paragraph of body language. Frank's last line is the door he closes behind himself.

### Choice exits

Two exits, both write the same effects (`frank_invited_to_bedroom + npc_frank_stage = 4`). Branching at choice level expresses Maya's *register*, not her *route*:

1. **"Yes."** — terse acceptance. Effects: `frank_invited_to_bedroom = true + npc_frank_stage = 4 + Maya.corruption +3`.
2. **"What about Diana."** — names the elephant. Effects: same advancement + Frank line ("She knows what she needs to know.") + `Maya.calculation +1`. No route divergence.

Both exits route to `Navigation`. The next office evening visit no longer fires `scene_office_after_crack` (gate update — see §5).

### Locked anti-patterns

- **No 4 keep-routes.** Doc 02's `frank_keep_route in {romantic, arrangement, rupture, power_inverted}` design is dropped.
- **No Stage 4 sub-route flags.** One transition, one outcome. Variety at Stage 4 emerges from Frank's stat drift and internal cascades (per sandbox doctrine), not from pre-authored route flags.
- **No second Stage 3→4 path.** Dev-button shortcut still exists for testing; no second natural gate.

### New helper

```
frank_stage_4 = AND(
  npc_frank_stage == 3,
  frank_invited_to_bedroom is_true
)
```

Counter + corruption are gates on the *transition canvas trigger*, not on the stage helper itself (helper stays minimal — single source of truth for "is the player at Stage 4 or higher" once the flag is set).

Transition canvas: a thin `transition_frank_to_4` watcher canvas (matching the `transition_frank_to_3` pattern) that fires when `frank_stage_4` clears, writes `npc_frank_stage = 4`, routes back. Per doc 18 §3 helper-driven pattern.

---

## §5 Stage 4 design — register cascade + bedroom anchor

**Register intent at Stage 4:** the bookkeeping pretense survives the daytime (Frank still has the books, Maya still does the columns), but the evening venue moves upstairs. Diana-aware tension is now real — Diana's room is in the same hallway. Frank doesn't need to close the office door anymore because evenings aren't in the office anymore.

### Surface roster

| Surface | What changes from Stage 3 | Tier | Notes |
|---|---|---|---|
| **Kitchen morning** | Existing Stage 4 fragment (`scene_kitchen_with_frank_morning` line 2432-2470) — already polished per doc 16 §6. Keep verbatim. | T3 (existing) | No work needed. |
| **Kitchen evening** | NEW T2 `[group]` block. Internal branch on whether Maya went to the bedroom last night (read `talked_to_frank_today` snapshot or a new `frank_bedroom_last_night` flag set by bedroom canvas exits, decayed at daily tick). | T2 (~60) | Brief register shift, Frank assured. |
| **Office evening** | `scene_office_after_crack` trigger update: gate to `npc_frank_stage = 3` only. At Stage 4 it stops firing — evenings route upstairs. Daytime office stays bookkeeping (the Stage-3 daytime vignette from §3 carries over). | trigger update | Resolves §10 open question by recommendation: evening venue is exclusive. |
| **Bedroom (NEW canvas)** | `scene_franks_bedroom_evening`. T3 anchor. Detail spec below. | T3 (~400, NEW canvas) | The single new canvas in this design. |
| **Living room evening** | NEW T2 `[group]` block. Frank in the chair, Maya passes through, the dynamic is now public-within-the-house. Diana-aware register. | T2 (~40) | `+1 diana_awareness` |
| **Hallway** (passing the bedroom door) | Optional NEW T2 `[group]` block. Passing Frank's bedroom door at the right hour, the door is closed, the lamp is on inside. | T2 (~30) | Optional — author can defer if the surface doesn't carry weight in playtest. |

### `scene_franks_bedroom_evening` — canvas spec

- **Trigger:** `loc_franks_bedroom`, weekday E band 21:00-23:00, repeatable, priority 9, daily cooldown via `talked_to_frank_today is_false`.
- **Conditions:** AND `npc_frank_stage >= 4 + frank_invited_to_bedroom is_true + talked_to_frank_today is_false`.
- **Pays $0.** The pretense is the bookkeeping; the bedroom is post-pretense. Money flows during the day in the office (chores, daytime bookkeeping). Bedroom is the dynamic, not the wage.
- **T3 anchor (~400 words).** Voice per doc 16 §2. The bedroom is its own room — the desk imagery from the office doesn't carry over. New sensory ground: bed, lamp on the nightstand, hallway sounds, the closeness of Diana's wall.
- **Effects:** `Maya.corruption +2 + Frank.arousal -3 + Frank.corruption +2 + frank_bedroom_last_night = set + talked_to_frank_today = set + diana_awareness +1` (Diana-tick is the meaningful background change for this surface).
- **Two choice exits** (both write the same effects, branch on register):
  1. *"Stay through."* — Maya stays in his bed past climax. Brief epilogue paragraph. `+1 Frank.trust`.
  2. *"Back to my room before Diana wakes."* — leaves before dawn. `+1 Maya.calculation`.

The choice exits are register, not route. State drift from accumulated `Maya.calculation` vs `Frank.trust` over many bedroom visits emerges as character texture without per-route authoring.

> **Update 2026-05-06 — Body rewritten as S7 cascades.** The bedroom anchor is now the validating pilot for the S7 (linkreplace-drip cascade) + S8 (thought_bubble) engine work. The two existing mutually-exclusive `[group]`s (first-night / subsequent-nights) now wrap `[cascade]` blocks instead of flat paragraph lists. The first-night cascade is **Pattern D** (5 beats, mid-cascade stat gate at Beat 3 — `corruption ≥ 25` → "Cross to him." vs locked sibling "Hesitate at the door."; per-beat effect `Frank.arousal +2` on Beat 2's "Close the door." click + thought bubble `💭 Frank is thinking: She came.`); the subsequent-nights cascade is **Pattern E** (4 beats, no in-scene gate, pure linear). All original prose preserved verbatim — only the pacing changed. Choice exits unchanged. See plan `lets-plan-a-game-wobbly-snail.md` and the S7/S8 implementation in `apps/game_generation/twee_comprehensive/generators/v1.py` (`_render_cascade` near line 10573).

### Stage 4 terminal posture

Stage 4 is **terminal** — there is no Stage 5 helper, no Stage 5 content. The arc closes when the calendar closes. Summer-end is a global event (handled separately at the project level), not a Frank-arc trigger. Until then, Stage 4 daily texture loops with internal cascade variety.

---

## §6 Hint + walkthrough integration

Per doc 13 §6 transparency doctrine and doc 14 S3 counter-surfacing.

### Stage 3 hint rewrite

Current Stage 3 hint (shipped 2026-05-04) reads as atmosphere without a verb. Replace with a hint that names an action:

```
text = "He needs me in the office after seven now. Bookkeeping with extra duties."
tip  = "Frank's office, weekday evenings 7-9:30 PM. Once a day. After a few visits something might shift between us."
auto_goal = false
condition = { stage_npc = "npc_frank", stage_op = "eq", stage_value = 3 }
```

Names: the verb (he needs me), the venue (office), the time (after seven), the cooldown (once a day), the future (something might shift). Tip line names the Stage 3→4 promise without spoiling the bedroom mechanism.

### Stage 4 hint

```
text = "Upstairs after eleven now. The office stays for the books."
tip  = "Frank's bedroom, weekday evenings 9-11 PM. Diana's down the hall."
auto_goal = false
condition = { stage_npc = "npc_frank", stage_op = "eq", stage_value = 4 }
```

### Walkthrough column

Per doc 14 S3 counter surfacing. The `frank_office_visits` counter and `Frank.corruption` threshold for the Stage 3→4 transition publish in the Quests panel as legible progress:

```
Frank — bedroom invitation
  Office visits: 2 / 3
  Frank corruption: 18 / 25
  Status: locked — keep visiting his office evenings
```

The counter and threshold appear once Maya has reached Stage 3. They unlock when both gates clear (the next office visit fires the §4 capstone branch).

---

## §7 One-shot ledger (post-design)

Frank's one-shot canvases / branches after this design:

1. **Bookkeeping offer** (Stage 0→1) — branch in `scene_kitchen_with_frank_morning`, sets `frank_offered_bookkeeping`.
2. **Catch** (Stage 1→2) — branch in `scene_living_room_evening`, sets `frank_caught + frank_restrict_declared + npc_frank_stage = 2`.
3. **Crack** (Stage 2→3) — `scene_office_crack` (separate canvas per doc 18 §5), sets `frank_cracked + npc_frank_stage = 3`.
4. **Bedroom invitation** (Stage 3→4, NEW per §4) — branch in `scene_office_after_crack`, sets `frank_invited_to_bedroom + npc_frank_stage = 4`.

**Total: 4 one-shots.** Within the single-digit ceiling for the entire game per doc 01 doctrine. (For comparison, doc 02's design would have produced 4-7 Frank-alone one-shots: catch, crack, plus 1 keep-route-selection scene + per-route bedroom intros.)

---

## §8 Implementation order + effort

Six steps, ordered for incremental shippable value. Each step is independently completable and produces visible game state.

| # | Step | Effort | Visible result |
|---|---|---|---|
| 1 | **Hint rewrites** (Stage 3 + Stage 4 + walkthrough entries per §6) | ~30 min | Quests page reads with verb-first hints; walkthrough exposes the Stage 3→4 thresholds. **Shipped 2026-05-04.** |
| 2 | **Stage 3 T2 vignettes** (4 group blocks per §3 — office daytime deferred) | ~3 hr | Stage 3 register lands on kitchen morning (split pre/post first office sex), kitchen evening, living room afternoon (radio canvas), back porch dusk — not just the office sex scene. **Shipped 2026-05-04.** |
| 3 | **Stage 3→4 capstone branch** (T3 inside `scene_office_after_crack` per §4) + `frank_office_visits` counter wiring | ~2 hr | After 3 office visits + Frank.corruption ≥ 25, the bedroom invitation fires; Stage 4 entered. **Shipped 2026-05-04.** |
| 4 | ~~`frank_stage_4` helper + `transition_frank_to_4` watcher canvas~~ — **N/A 2026-05-04** | — | Step 3's branch-inside-shell pattern writes `npc_frank_stage = 4` directly in both capstone choice exits (matching the catch at `scene_living_room_evening` which writes `npc_frank_stage = 2` the same way). A helper-driven transition canvas would only be useful if some other system needed to read "is the bedroom-invitation gate satisfied without the stage being committed yet" — nothing does. The Stage 4 hint condition reads `npc_frank_stage = 4` directly, no helper required. Step 4 is redundant infrastructure. |
| 5 | **Bedroom canvas** (`scene_franks_bedroom_evening` T3 anchor per §5) + `loc_franks_bedroom` schedule wiring + `frank_bedroom_first_done` flag | ~3 hr | Stage 4 evenings route upstairs; daily Tier-3 anchor scene playable. **Shipped 2026-05-04.** Note: design tweak — used `frank_bedroom_first_done` (one-time guard) instead of speced `frank_bedroom_last_night` (daily-decay flag). The "last night" pattern would require a state-snapshot mechanism that doesn't exist in the engine; the first-time-guard pattern is the same shape Stage 3 morning split uses, and serves the same narrative purpose (first-night vs established register). |
| 6 | **Stage 4 T2 vignettes** (kitchen evening + living room + back porch + optional hallway per §5) + `scene_office_after_crack` trigger gate update | ~2 hr | Stage 4 register multiplexes across surfaces; office evening retires gracefully. **Shipped 2026-05-04.** Kitchen evening, living room afternoon, back porch dusk landed (3 of 4); hallway optional vignette deferred per design. Office trigger tightened from `npc_frank_stage gte 3` → `eq 3` so Stage 4 evenings route exclusively to bedroom. |

**Total: ~11 hours.** Roughly one focused authoring day. Each step is independently shippable — the Quests page is no longer broken after step 1; Stage 3 feels alive after step 2; Stage 4 is reachable after step 4; Stage 4 is fully textured after step 6.

---

## §9 What this design deliberately does NOT do

Listed explicitly so future readers don't misread the scope:

- **No 4 keep-routes.** Doc 02 §"Frank — full chain" Stage 4 spec is dropped — see §1.
- **No new helpers per route.** One `frank_stage_4` helper. No `frank_keep_route_*` flags.
- **No second new T3 canvas at Stage 3.** Office-after-crack remains the sole T3 anchor at S3; everything else is T2 group blocks inside existing canvases.
- **No Stage 5.** Stage 4 is terminal until summer-end (a global event).
- **No prose drafted.** This doc is design only. Step 1 in §8 is the first prose-writing step.
- **No changes to Stage 0/1/2 content.** Doc 16 D2 still preserved.
- **No changes to the existing Stage 3 office sex scene.** `scene_office_after_crack` body stays verbatim; only its trigger gates and one new mid-scene branch (the §4 capstone) change.
- **No engine work.** All required engine features (E1 cascade, E4 helpers, E5 daily tick, branch-inside-shell pattern) are already shipped.

---

## §10 Open questions / future work

- **Diana-awareness ticking at Stage 4 living-room and bedroom vignettes** — recommend yes (silent accumulator pattern, gates Diana-arc Phase 2+ content). Confirm during implementation step 6.
- **Bedroom canvas choice exits — branching on player initiative vs Frank's lead** — current §5 spec uses register-level branching (stay through / leave before dawn). Alternative: branch on a secondary internal cascade reading `Frank.arousal` snapshot (e.g., if Frank.arousal ≥ 70 the exit changes). Defer until playtest reveals whether the register branch carries the weight.
- **Office evening retirement at Stage 4** — §5 recommends gating `scene_office_after_crack` to `npc_frank_stage = 3` only. Alternative: leave it firing as a "sometimes the office, sometimes upstairs" variety mechanism. Recommend retire (cleaner narrative; one venue per stage).
- **Ryan / Jake analogous Stage 3+ designs** — same template (capstone + texture cascade) should apply, but each NPC has different register and different surfaces. Out of scope for this doc; flag as next-doc territory (doc 20 = Ryan, doc 21 = Jake).
- **Full game terminal event** — Stage 4 is terminal until summer-end. The summer-end mechanism itself is not spec'd here; it's a project-level concern.

---

## §11 Cross-reference index

| Cited doc | Sections referenced |
|---|---|
| `00_TLS_Phase2_Diagnosis_and_Direction.md` | Anti-patterns (Problem 2 establishment sequences, Problem 3 monolithic literary tics, Problem 5 metadata bloat). One-shot ledger discipline. |
| `01_Repeatable_First_Doctrine.md` | Repeatable-first doctrine. "Same passage, different stage" pattern. When-to-one-shot rule (single-digit ceiling). |
| `02_NPC_Stage_Chains.md` | Stage chain contract. **§"Frank — full chain" Stage 4 spec — superseded by this doc §4-§5.** |
| `04_Scene_Cascade_Pattern.md` | `[group]` block precedence (Stage → Time-band → Tier). NPC schedule enforcement. |
| `13_Road_to_Success_Reference.md` | §6 walkthrough doctrine. §9 tier budget (T1/T2/T3 ratios). §16 passive trait drift, interior thought bubbles. |
| `14_Engine_PRD_Sandbox_Additions.md` | S3 counter surfacing in walkthrough. |
| `15_Sandbox_Pivot_Direction.md` | §6.3 daily texture vs capstone layer separation. §6.7 NPC progression patterns (deterministic / ambient / metric+wait). |
| `16_Frank_Scene_Library_Design.md` | §2 voice rules (preserved). §4 tier discipline (preserved). D1 / D2 (preserved). D3 (lifted by §1). |
| `18_Frank_Arc_Redesign.md` | §1 D1/D2 preserved, **D3 lifted**. §3 single-source counter discipline (preserved). §5/§6 Stage 2→3 + Stage 3 explicit content (preserved as already-shipped baseline). |

---

End of design.
