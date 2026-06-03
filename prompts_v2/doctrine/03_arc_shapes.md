# Doctrine 03 — Arc Shapes + Per-Shape Canvas Distribution

**Sources:** Doc 56 §5 (per-arc distribution table); Docs 31 (Frank), 53 (Marge), 58 (Ryan), 59 (Jake), 60 (Diana), 61 (Cookie scope-out).
**Authority:** Doctrine. Every NPC in every RTS-shape sandbox picks ONE arc shape from the five below. The shape determines the mechanical rhythm of the arc + the per-lane canvas budget.
**Purpose:** Replace the legacy 7-driver NPC-archetype system (per `00_LEGACY_IGNORE.md` §3.3). Each shape comes with a worked-example NPC + canvas distribution table + voice register guidance + budget bounds.

Cross-reference: `doctrine/02_three_lanes_plus_capstone.md` for the lane mechanisms this distribution sits inside. `doctrine/04_authoring_rules.md` R3 + R7 for the rules that operationalize shape selection.

---

**Scope-mode note (read before §2 budget tables):**

The per-arc-shape canvas budgets in §2 are **FULL-ARC targets** — they describe the complete shipped game across all phases, not a slice. Authoring at:

- **`scope_mode: full_game`** (default) — author up to the full budget per shape. All Stage 0→4 content. Full capstone chains.
- **`scope_mode: slice`** — author a subset (typically 30–50% of budget) + locked-visible rungs telegraphing the deferred remainder.

RTS is the existence proof — Brother (family/ambient) shipped at 15–16 distinct canvases (cluster-merged from a larger surface), landing inside the 25–35 full-arc budget. See `reference/02_rts_scene_catalog.md` for the per-NPC count evidence. The budget table is not aspirational; it's RTS-validated.

---

## §1 — The five arc shapes

Every NPC in an RTS-shape sandbox runs ONE of these five rhythms. The shape is declared in the R7 design brief BEFORE any canvas is authored (Doc 54 §2.3 + Doc 56 R7).

| Shape | Mechanical rhythm | RTS reference | TLS reference |
|---|---|---|---|
| **Family/ambient** | Daily proximity + saturated chore presence + escalating intimacy. The dense shape. | Stepbrother (15 scenes, 47% Lane 3) | Frank |
| **Slow-burn family** | Family but distant; discrete revelation beats; Lane 3 walk-ins ARE the milestones | (no direct RTS analog — slow-burn-incest is rare in RTS catalog) | Jake |
| **Peer/dating** | Scheduled visits; quest-chain progression; relation-driven; no walk-ins | Marcus (5 scenes, all deterministic chance=100%, quest chain) | Ryan |
| **Service** | Workplace register; relation-driven; arousal/corruption don't apply | (no direct RTS analog; Marge designed against RTS service-NPC absence) | Marge |
| **Antagonist/witness** | Silent awareness accumulator; confrontation capstone; no own Lane 3 (appears as interruptor in others') | (no direct RTS analog; Diana modeled on mother-discovers-affair drama) | Diana |

**Why five and not more:** these five cover the mechanical rhythms RTS uses + the slot mechanics the TLS engine supports natively (Lane 1/2/3 + Lane 4 capstones). Adding a sixth requires either an engine extension OR doctrine extension; both are out of scope until a load-bearing use case arises.

---

## §2 — Per-shape canvas distribution (Doc 56 §5)

The reference table for what each shape's canvas distribution should LOOK like. Cell values are guidelines, not quotas — the R7 brief commits to specific numbers within these ranges.

| Lane / Tier | Family/ambient (Frank) | Slow-burn family (Jake) | Peer/dating (Ryan) | Service (Marge) | Antagonist (Diana) |
|---|---|---|---|---|---|
| **L1 / T1** | 1–2 base + 1–2 self-display | 1 (room visit) | 1 (visit at workplace) | 1 (workplace base) | 0–1 (shared-space neutral) |
| **L1 / T2** | 1–2 mid escalation | 0–1 (charged moment) | 0–1 (date intro) | 0 | 0 (no escalation register) |
| **L1 / T3** | 1–2 explicit | 0–1 (consummation if vocab allows) | 0–1 (commit beat) | 0 | 0 |
| **L2 / T1** | 1–2 morning/passing | 0–1 (corridor) | 1 (workplace ambient) | 1 (workplace texture) | 1–2 (presence beats) |
| **L2 / T2** | 2–3 evening/charged | 0–1 (charged corridor) | 0–1 (low density) | 0–1 | 1–2 (charged presence) |
| **L2 / T3** | 1–2 late-night/explicit | 0 | 0 | 0 | 0–1 (confrontation precursors) |
| **L3 / T1–T3** | 4–7 walk-ins on chores | 1–3 (discrete revelation walk-ins) | 0 | 0 | 0 own (appears in others' L3) |
| **Capstones** | 4–6 (catch, declare, first-night, sleepover, Diana confrontation) | 3–5 (transitions + revelation + relationship turn) | 3–4 (dating chain) | 1–2 (hire + escalation if vocab allows) | 1–2 (confrontation, resolution) |

**Total canvas budget by shape:**

| Shape | Range | Notes |
|---|---|---|
| Family/ambient | **25–35** | The dense shape; Frank is the gold standard |
| Slow-burn family | **10–15** | Sparse but focused; slow-burn-incest works because each beat is concentrated |
| Peer/dating | **8–12** | Quest-chain progression; capstones do the heavy lifting |
| Service | **6–10** | Bounded by workplace register + Phase 2+ deferrals |
| Antagonist/witness | **6–10 standalone** + cross-appearances in others' arcs | Diana standalone count is low; her presence saturates Frank's lanes |

**Empty cells are honest.** If the shape has 0 in a cell, the brief commits to 0. Filling empty cells with relational/atmospheric texture is the Doc 54 Marge failure mode — soft drift toward "fill the world" that violates the shape.

**The L1 cells above count *escalation* rungs, not hubs.** The number of Lane 1 **hubs** is set separately by presence: one hub per distinct `[[npcs.schedules]]` row (location × window) — D72-R6, `doctrine/04` §6.1. An NPC scheduled across 5 windows has 5 hubs even if the escalation budget is small; the extra hubs are *light* (base + talk + leave, exposure-tier-capped per D72-R7), not extra escalation. "Empty cells are honest" governs L2/L3 *escalation* surfaces — it does NOT excuse a missing presence hub: even service/antagonist NPCs get a light hub at each scheduled location. Presence floor (a hub) and escalation register (the rungs on it) are independent axes.

---

## §3 — Family/ambient (Frank — the dense reference)

### §3.1 — Mechanical rhythm

Maya and the NPC share a household. Daily proximity. Saturated chore presence. Escalating intimacy from neutral co-existence → first sexual contact → declared partnership → terminal-state routine.

**Lane 3 is the dominant lane.** Brother in RTS = 47% Lane 3 (7 of 15 scenes). The shape requires that Maya can't get through her chores without encountering the NPC — that's what makes the world feel alive with them.

### §3.2 — Canvas distribution (Frank slice, post-Phase E1 redesign)

| Lane | Tier | Canvas count | Examples |
|---|---|---|---|
| L1 | T1 | 2 base + 2 self-display | `frank_kitchen_morning_hub`, `frank_kitchen_dinner_hub`, `tease_kitchen_general`, `flash_kitchen_general` |
| L1 | T2 | 2 mid | `loop_franks_bedroom_finisher` partial, hub variants |
| L1 | T3 | 2 explicit | `loop_franks_bedroom_finisher` deep loop, related |
| L2 | T1 | 2 morning | `ambient_kitchen_morning_chat`, `ambient_kitchen_coffee_alone` |
| L2 | T2 | 3 evening | `ambient_livingroom_paper`, `ambient_livingroom_tv`, `ambient_kitchen_dinprep_grope` |
| L2 | T3 | 1 late-night | `ambient_kitchen_late_night_raid` |
| L3 | T1–T3 | 7 substitutions | `scene_frank_passes_kitchen_door`, `scene_frank_arrives_during_coffee`, `scene_frank_joins_porch`, `scene_frank_joins_couch`, `scene_frank_at_kitchen_sink_behind`, `scene_frank_at_open_bathroom_door`, `scene_frank_walks_in_shower` |
| Capstones | — | 5 | `scene_livingroom_catch` → `scene_franks_bedroom_evening` → `scene_frank_declaration` → `scene_frank_sleepover` → `scene_diana_confrontation` |

**Total Frank canvases: ~28.** Within the 25–35 range.

### §3.3 — Per-NPC stat ladder

Frank uses the universal corruption-tier model (Doc 30 §4.4):

| Tier | Maya corruption | Capstone gate | Content type |
|---|---|---|---|
| 0 | 0+ | none | Brushed contact / accidental |
| 1 | 5+ | none | Tease / Flash (visual only) |
| 2 | 15+ | none | Fondle / explicit physical (clothed) |
| 3 | 25+ | post-catch | Explicit sex acts (oral / partial sex) |
| 4 | 35+ | post-cracked | Full sex |
| 5 | 50+ | post-first-night | Routine intimacy / sleepover / breeding |

### §3.4 — Sidebar visibility (Doc 68 §8)

Family/ambient default: **location + arousal + corruption + relation** all surface. Player needs to plan Lane 3 attempts (arousal), Lane 1 escalation (corruption), late-game intimacy (relation). RTS surfaces all three for family NPCs (Stepbrother/Stepfather/Stepgrandfather) — verified live.

Stage NEVER surfaces (Doc 68 §9).

### §3.5 — Voice register

- Lane 1/2/3: RTS-flat default. ~30-word caption density. Direct/crude diction per per-arc vocab ceiling (`doctrine/08_kink_vocab_ceilings.md`).
- Lane 4 capstones: Tier-3 earned. Interior monologue + layered sensory detail + character-distinguishing diction.

### §3.6 — Doc 31 design brief (Frank) — gold standard

`28th_april_TLS_Phase2_Redesign/31_Frank_Arc_Design_Brief.md` is the R7 reference for family/ambient. Read it when authoring a new family/ambient NPC.

---

## §4 — Slow-burn family (Jake)

### §4.1 — Mechanical rhythm

Family by relation but distant by interaction. Stage 0–4 ladder: Hostile → Noticed → Peek/Draw → Tease → Caught. The arc is sparser than Frank because each beat is concentrated — slow-burn-incest works because each revelation is a moment, not a routine.

Lane 3 walk-ins ARE the milestones — not 7 routine substitutions like Frank, but 1–3 discrete revelation beats keyed to specific arc moments.

### §4.2 — Canvas distribution (Jake slice — Doc 59 brief)

| Lane | Tier | Canvas count | Examples (planned per Doc 59) |
|---|---|---|---|
| L1 | T1 | 1 (room visit) | `jake_room_visit` |
| L1 | T2 | 0–1 (charged moment) | Stage 2 admit (Type A capstone) |
| L1 | T3 | 0–1 (Phase 2+ consummation) | Phase 2+ |
| L2 | T1 | 1 (corridor) | `ambient_jake_corridor_passing` |
| L2 | T2 | 1 (charged corridor) | `ambient_jake_hallway_glance` |
| L2 | T3 | 0 | — |
| L3 | T1–T3 | 1–3 (revelation beats) | `scene_jake_walks_in_change`, `scene_jake_maya_solo_sketch` |
| Capstones | — | 3–5 | Transition reveal + charged consummation + relationship turn |

**Total Jake canvases: ~10–12.** Within the 10–15 range.

### §4.3 — Stage ladder + dual-path 0→1 (Doc 57 §9)

Jake's Stage 0→1 transition is dual-path: via `transition_jake_to_1_via_beauty` (Maya wears the right outfit) OR `transition_jake_to_1_via_glance` (Maya catches him looking). Both share verbatim body prose — the engine constraint (OR-logic in stage_helpers is banned) forced two-canvas pattern; the narrative moment is one beat.

This is NOT an anti-pattern. The duplicate-prose engine exemption (Doc 57 §9) covers this: when an engine constraint forces multiple canvases for a single narrative moment, identical body prose across the duplicates is acceptable. Mark with a comment naming the constraint.

### §4.4 — Sidebar visibility (Doc 68 §8)

Slow-burn family default: **location + arousal + relation.** Corruption stays low in slow-burn arcs by design; surfacing it would mislead the player. Arousal + relation are the player-relevant dimensions.

### §4.5 — Voice register

Same Lane 1/2/3 vs Lane 4 split as family/ambient, but per-arc vocab ceiling is FULL INCEST CALLOUTS (per Doc 30 §7.5) — "brother" / "sis" / "little sister" callouts during sex; explicit reference to taboo ("this is so fucking wrong," "my own brother"). Incest IS the kink — named and dwelt on at all tiers.

### §4.6 — Doc 59 design brief (Jake)

`28th_april_TLS_Phase2_Redesign/59_Jake_Design_Brief.md`. Stage 0–4 ladder, dual-path transition, per-lane budget L1 1–2 + L2 1–2 + **L3 1–3** (slow-burn DOES get walk-ins, unlike peer/dating) + capstones 3–5.

---

## §5 — Peer/dating (Ryan)

### §5.1 — Mechanical rhythm

Separate household. Scheduled interactions. Relation-driven. Quest-chain progression — Stage 0 (meet) → Stage 1 (notice) → Stage 2 (partner) → Stage 3 (consummation, Phase 2+) → Stage 4 (relationship beat).

**Lane 3 budget = 0.** Peer doesn't interrupt private chores. The arc lives in Lane 1 visits + Lane 2 workplace ambient + capstone dates.

**Ongoing Stage-4 hub (required — Late Shifts B6).** A peer/dating arc needs a REPEATABLE Lane-1 hub at the partner's location for the post-consummation (Stage 4) state — not just a one-shot first-night capstone. Without it, the arc has no surface after consummation: nothing to revisit, and Phase-2+ content (e.g. pregnant variants) has nowhere to attach. Pattern: the partner's home is access-gated on the relationship flag (e.g. `cole_date_done`); the ongoing hub gates on the consummation flag (e.g. `cole_first_night_done`) at a priority BELOW the first-night capstone (so the capstone fires first, then the hub takes over). The hub's NPC must be schedule-present at that location, or the portrait won't render (`doctrine/10` §5.2). Late Shifts shipped Cole with only the first-night capstone — the missing ongoing hub surfaced only when authoring pregnant variants.

### §5.2 — Canvas distribution (Ryan slice — Doc 58 brief)

| Lane | Tier | Canvas count | Examples |
|---|---|---|---|
| L1 | T1 | 1 (visit at workplace/yard) | `visit_ryan_at_yard`, `activity_help_ryan_in_yard` |
| L1 | T2 | 0–1 (date intro / charged) | `ryan_porch_chat` |
| L1 | T3 | 0–1 (commit beat) | `scene_ryan_partner_commit` (Phase 2+) |
| L2 | T1 | 1 (workplace ambient) | `scene_yard_with_ryan` |
| L2 | T2 | 0–1 (low density) | (sketchy slot — deferred) |
| L2 | T3 | 0 | — |
| L3 | — | **0** | Peer doesn't interrupt private chores |
| Capstones | — | 3–4 | `transition_ryan_to_1`, `scene_ryan_first_date`, second-date (Type A), partner-commit (Type B) |

**Total Ryan canvases: ~8–10.** Within the 8–12 range. Doc 58 surfaces ~3–4 new canvases needed beyond current 6 (workplace L1, porch L2, second-date Type A, partner-commit Type B).

### §5.3 — Sidebar visibility (Doc 68 §8)

Peer/dating default: **location + relation only.** Dating chain is relation-driven. Arousal is bounded + less player-controllable. Corruption isn't meaningful for peer arcs (most peer NPCs cap low).

### §5.4 — Voice register

Lane 1/2 RTS-flat; capstones Tier-3 earned. Per-arc vocab ceiling: open question per Doc 58 §3 — does Ryan's arc include a sexual tier, or is it Stage-2 wholesome dating only? Phase 2+ scope.

### §5.5 — Doc 58 design brief (Ryan)

`28th_april_TLS_Phase2_Redesign/58_Ryan_Design_Brief.md`. Per-lane budget L1 2–3 + L2 1–2 + **L3 = 0** + capstones 3–4. Slice scope = Stage 2 partner. Phase 2+ = Stage 3+ consummation.

---

## §6 — Service (Marge)

### §6.1 — Mechanical rhythm

Workplace register. Maya hired into a service position; the NPC is the employer/manager/colleague. Bond builds via shifts worked + workplace conversations.

**Lane 3 budget = 0.** Workplace-only register; private space is not their setting. No walk-ins.
**Lane 1 = bounded.** Hub menu items are workplace verbs (Pour coffee, Talk a minute) — Maya-with-NPC interactions, not work-tasks (work-tasks live as separate solo-activity canvases parallel to the hub per `doctrine/02_three_lanes_plus_capstone.md` §8.2).

### §6.2 — Canvas distribution (Marge slice — Doc 53 brief, applied lessons)

| Lane | Tier | Canvas count | Examples |
|---|---|---|---|
| L1 | T1 | 1 (workplace base) | `scene_marge_diner_hub` |
| L1 | T2 | 0 | Empty (service register; no escalation in slice) |
| L1 | T3 | 0 | Empty (Phase 3+ workplace seduction scoped out per Doc 30 §8.2) |
| L2 | T1 | 1 (workplace texture) | `scene_diner_t0_shift` (location-triggered shift) |
| L2 | T2 | 0–1 | (slot reserved for Phase 3+) |
| L2 | T3 | 0 | — |
| L3 | — | **0** | Service register doesn't fit walk-ins |
| Capstones | — | 1–2 | `canvas_marge_interview` (hire) — Type A; mid-arc escalation TBD Phase 3+ |

**Total Marge canvases: ~6–8.** Within the 6–10 range.

**Locked-visible escalation ladder** (Doc 54 §4.5): Marge's hub ships with locked-visible Phase 3+ rungs from day 1, even though those rungs are not yet authored. The locked rungs ARE the slice — they telegraph the workplace-seduction matriarch-dom trajectory without requiring Phase 3+ content to ship.

### §6.3 — Sidebar visibility (Doc 68 §8)

Service default: **location + relation only.** Workplace bond is the operative axis. Arousal/corruption don't apply to service register.

### §6.4 — Voice register

Lane 1/2: RTS-flat WITH service-NPC specifics — short dialogue (Marge's "hon" / Marge's brevity). NOT Tier-3 prose for shift descriptions. Doc 54 §5.1 case study: literary prose in `node_shifts` + `node_talk` is preserved canon but represents a register-split violation; future maintenance pass should rewrite to RTS-flat.

Capstone (canvas_marge_interview) earns Tier-3 specifics ("the up-and-down a woman who had hired forty waitresses did. The shoes. The hands.") — 1,900 chars total.

Per-arc vocab ceiling for Marge: TBD Phase 3+ (Doc 30 §7.5 row left blank = out of scope for slice).

### §6.5 — Doc 53 design brief (Marge)

`28th_april_TLS_Phase2_Redesign/53_Marge_Redesign_Brief.md` (supersedes Doc 51 — Doc 51 is the historical record of the failed initial design). §1 codifies service-NPC arc adaptation of Doc 24's 3-lane doctrine (Lane 2+3 empty in slice for non-escalation NPCs). 4 deliverables only: schedule + 1 hub item + T1 shift + 2 trust effect + 2 quest cards (M1/M2, no terminal). Voice spec §2 locks RTS-flat per feedback memory.

---

## §7 — Antagonist/witness (Diana)

### §7.1 — Mechanical rhythm

Silent awareness accumulator. Diana's `awareness` trait climbs 0–100 across Maya's actions (visible-from-window beats, scandal-adjacent choices); confrontation capstone fires at threshold cross.

**No arc_stages.** Diana doesn't have discrete stage milestones in slice — she has a single threshold-driven confrontation. Her sub-state lives as bands on the awareness trait (cold / suspicious / knowing / shut-out).

**Lane 3 = 0 own + appears as INTERRUPTOR in others' Lane 3 endings.** The "Diana's floorboard" pattern in Frank's late-night kitchen ambient — Diana's footstep stops the cascade. This is what Diana does mechanically across the slice.

### §7.2 — Canvas distribution (Diana slice — Doc 60 brief, partial)

| Lane | Tier | Canvas count | Examples |
|---|---|---|---|
| L1 | T1 | 0–1 (shared-space neutral) | `diana_kitchen_passing` (very low density) |
| L1 | T2/T3 | 0 | No escalation register |
| L2 | T1–T2 | 1–2 (presence beats) | `ambient_kitchen_diana_call`, `ambient_diana_phone_kitchen` |
| L2 | T3 | 0–1 (confrontation precursors) | (sketchy slot — feeds capstone) |
| L3 | — | **0 own** | Appears as interruptor in Frank's L3 endings |
| Capstones | — | 1–2 | `scene_diana_confrontation` (Type B Pattern F — kicked_out + brought_in branches in slice; blackmail + matriarch deferred Phase 2+) |

**Total Diana canvases: ~4–6 standalone** + cross-appearances in Frank's lanes. Within the 6–10 range when cross-appearances counted.

### §7.3 — `awareness` trait (Tier 3 per-game; OFF-LIMITS at global scandal level per `00_LEGACY_IGNORE.md` §3.4 + Doc 65)

```toml
[npcs.core_traits]
awareness = 0   # silent accumulator 0–100
relation = 5    # mother-Maya baseline
```

Modifiers (per Doc 60 brief): visible-from-window beats +N; outdoor sexual beats +N; scandal-adjacent choices +N. No daily decay (one-way climb).

Bands (internal-only — NOT surfaced to sidebar):
- cold (0–24) — baseline
- suspicious (25–49) — confrontation precursors eligible
- knowing (50–74) — confrontation primed
- shut-out (75–100) — confrontation imminent

### §7.4 — Sidebar visibility (Doc 68 §8)

Antagonist default: **location only.** Awareness/scandal accumulator stays HIDDEN — dramatic surprise depends on player NOT seeing how close confrontation is. Doc 30 §6 + Doc 60 lock this.

### §7.5 — Voice register

Lane 1/2: RTS-flat with Diana's specific voice (clipped, observational, motherly with edge).
Capstone (confrontation): Tier-3 earned. Pattern F branching with high-stakes branch consequences (the resolution branches reshape multiple arcs — kicked_out / brought_in are mutually exclusive end-states).

Per-arc vocab ceiling: FULL CUCKOLD FRAMING (Doc 30 §7.5) — Diana watches / listens / participates; explicit cuckold dialogue ("watch your husband fuck me," "your wife is my second wife"); cuckold IS the resolution kink for the brought_in branch.

### §7.6 — Doc 60 design brief (Diana) — 🔴 BLOCKED

`28th_april_TLS_Phase2_Redesign/60_Diana_Design_Brief.md`. Antagonist/witness; NO arc_stages — silent awareness accumulator 0-100 (bands cold/suspicious/knowing/shut-out). Confrontation Type B Pattern F (2/4 branches scripted: kicked_out + brought_in; blackmail + matriarch deferred Phase 2+). 4 Q3 sub-questions surfaced for LO (Q3a canonical good path? Q3b cuckold sex in slice? Q3c blackmail+matriarch phase scope? Q3d post-confrontation hub?).

---

## §8 — Picking the shape (decision rule)

When the design book proposes a new NPC, run this 4-question check. Stop at the first match.

1. **Does the NPC share a household with Maya AND have a daily-proximity register the player will want to escalate?**
   → **Family/ambient** (Frank). Budget 25–35 canvases.

2. **Does the NPC share a household with Maya BUT the register is sparse + revelation-keyed, not saturated?**
   → **Slow-burn family** (Jake). Budget 10–15 canvases.

3. **Does the NPC live in a separate household, schedule-driven, relation-progression?**
   → **Peer/dating** (Ryan). Budget 8–12 canvases.

4. **Does the NPC have a workplace register Maya enters as employee/customer/colleague?**
   → **Service** (Marge). Budget 6–10 canvases.

5. **Does the NPC function as the threat/cost-of-other-arcs, with a confrontation as their primary scripted beat?**
   → **Antagonist/witness** (Diana). Budget 6–10 standalone + cross-appearances.

If none of the above match, the proposed NPC is outside the current 5-shape taxonomy. Surface to LO; don't author against an undefined shape.

---

## §9 — Shape adaptation: empty cells are honest

The Marge case study (Doc 54) cost ~8 hours partly because doctrine designed for escalation NPCs (Frank's distribution) was forced onto a service NPC. The corrected doctrine (Doc 53) declared empty Lane 2/3 cells.

**Same principle generalizes:** each shape has its own canvas distribution. Forcing Frank's distribution across every NPC produces Frank-clones with wrong-feel arcs. Skeletal under-distribution loses Principle 4 (mix arc shapes).

**Empty cells in the distribution table are honest, not gaps.** Service NPC at Lane 2 T2 = 0. Don't author 3 Lane 2 T2 scenes "to fill out the world" — that's the Doc 54 §3.4 failure mode. The empty cell is the design decision.

The R7 brief (Doc 56 R7 + `doctrine/04_authoring_rules.md`) commits to specific cell values for the NPC. Overages flag as drift. Under-shoots are acceptable when documented.

---

## §10 — Adapting to scope mode (slice vs full_game)

### §10.1 — At `scope_mode: slice`

**Slice scope ≠ full arc.** A slice ships the minimal viable canvases that telegraph the arc shape; the full arc is the eventual delivery. The locked-visible escalation ladder bridges the two — locked rungs visible from day 1 promise the arc's future without requiring future content to ship.

| Slice element | What ships | What stays locked-visible |
|---|---|---|
| L1 hub menu | Stage 0 unlocked items | Full ladder visible (Tease/Flash/Suck/Sex with their gates) |
| L1 menu items | Currently-tier-unlocked items | Locked rungs greyed + threshold-published |
| L2 ambients | Stage 0 + Stage 1 ambients | (later-stage ambients author when stage transitions) |
| L3 substitutions | Per slice scope | (later-stage subs author when stage transitions) |
| Capstones | Capstones up to slice scope's end-state | (next-chain capstones author when triggered) |

Phase 2+ content is NOT shipped in slice — but the slice's locked-visible rungs telegraph it (Doc 54 §3.6). The doctrine bridges slice + full arc via the locked-visible pattern, not via "ship Phase 2+ stubs."

**Locked-visible across locations (optional, D72-R8).** The locked-visible pattern can also bridge *exposure* tiers, not just stages: an arc NPC's public/semi-private hubs may show the higher (private-only) rungs greyed, so the ladder reads consistently at every hub, unlocking only where exposure allows (`doctrine/04` §6.2–§6.3). This is taste, not a requirement — the default is to simply omit out-of-tier rungs (context-scaled ladder).

### §10.2 — At `scope_mode: full_game`

All budgeted canvases are authored. Stage 0→4 ships in full; capstone chains run end-to-end; per-shape Lane 3 budgets fill to their upper bound where the arc demands it.

**Locked-visible escalation ladder still applies** — it's a UI/pacing device, not slice-specific. Even at full scope, the L1 hub menu shows future-tier rungs from day 1 with threshold text; rungs unlock as stat/stage gates pass. RTS Brother's hub shows ALL rungs from day 1 (Talk + Tease at Stage 0, Sex/Sleep visible-locked at higher corruption); rungs unlock organically. The difference vs slice is content existence behind each rung, not the UI shape.

| Full-game element | What ships | UI/pacing affordance |
|---|---|---|
| L1 hub menu | Full ladder authored | Locked-visible rungs still gate by stat/stage from day 1 |
| L2 ambients | All Stage 0→4 ambients per shape budget | Per-stage filtering via canvas conditions |
| L3 substitutions | Per-shape full budget (family 4–7, slow-burn 1–3, peer 0, service 0, antagonist 0 own) | Per-stage gating per substitution rule |
| Capstones | Full chains per Doc 57 (Type A/B/C) | Chain steps gate by predecessor flags |
| Phase 2+ inclusions | Pregnancy / scandal / gallery / tracker per LO decisions surfaced at Stage 1 §0 Q&A | Per Doc 65 — engine entry points + ripple |

**Anti-pattern:** pre-unlocking the entire L1 ladder at full_game because "everything ships." Locked-visible exists at any scope to telegraph progression — don't strip it. See `doctrine/07_anti_patterns.md` §8.X (full-game scope anti-patterns).

---

## §11 — Anti-patterns

### §11.1 — Frank-cloning a non-family-ambient NPC

Copying Frank's 28-canvas distribution onto Ryan's peer/dating shape produces 13 Lane 2 ambients + 7 Lane 3 substitutions where neither belongs. The shape mismatch produces the wrong "feel" — Ryan's quest-chain shape is meant to be sparse + relation-driven; saturating his lanes with ambients dilutes the few moments that should land.

### §11.2 — Filling empty cells in the distribution table

When the shape says 0 in a cell, the brief commits to 0. The Marge service shape has empty Lane 2 + Lane 3 in slice — that's correct, not a gap. Adding 6 Lane 2 ambients + 3 Lane 3 substitutions to "fill out the world" violates the shape (Doc 54 §3.4 case study — 9 surfaces authored that doctrine memory says shouldn't exist).

### §11.3 — Mixing escalation registers within a slice

A slice that has 4 family/ambient NPCs all at Frank-depth produces register sameness — every arc reads the same. The cast functions because shapes contrast (Principle 4 mix arc shapes). Slice scope should include 1 family/ambient + 1 slow-burn family + 1 peer/dating + 1 service + 1 antagonist (or similar combinatorial spread), not 5 family/ambient NPCs.

### §11.4 — Authoring against a shape that doesn't have a doctrine brief

If the design book proposes an NPC whose shape isn't in the 5-shape table (e.g., "AI assistant NPC" or "ghost NPC"), surface to LO before authoring. Don't improvise a 6th shape — the doctrine for budget + Lane 3 budget + sidebar visibility + voice register doesn't exist yet for that shape.

### §11.5 — R7 brief skipping

Doc 56 R7: no canvas for a new NPC ships before the NPC has a written design brief declaring arc shape + per-lane canvas budget + vocab ceiling + tier flags. Marge cost 8 hours to skip this step (Doc 54 §2.4).

### §11.6 — Shape declared but distribution drifts

A brief commits to peer/dating shape (Lane 3 = 0) but authoring produces 4 Lane 3 substitutions. Either the brief is wrong OR the additions don't belong. Overages flag as drift; surface to LO + audit.

---

## §12 — Cross-references

### Sibling doctrine files

- `doctrine/01_rts_principles.md` — P4 (mix arc shapes); P9 (per-arc vocab ceiling)
- `doctrine/02_three_lanes_plus_capstone.md` — lane mechanism distribution sits inside
- `doctrine/04_authoring_rules.md` — R3 (per-arc-shape Lane 3 budget); R7 (design brief precedes authoring); F1–F5 (capstone Pattern F)
- `doctrine/06_design_brief_template.md` — R7 brief structure
- `doctrine/08_kink_vocab_ceilings.md` — per-arc vocab ceiling table
- `doctrine/09_trait_catalog.md` §8 — sidebar visibility per arc shape

### Source briefs

- `28th_april_TLS_Phase2_Redesign/31_Frank_Arc_Design_Brief.md` — family/ambient gold standard
- `28th_april_TLS_Phase2_Redesign/53_Marge_Redesign_Brief.md` — service shape gold standard
- `28th_april_TLS_Phase2_Redesign/58_Ryan_Design_Brief.md` — peer/dating brief
- `28th_april_TLS_Phase2_Redesign/59_Jake_Design_Brief.md` — slow-burn family brief
- `28th_april_TLS_Phase2_Redesign/60_Diana_Design_Brief.md` — antagonist brief (🔴 BLOCKED on Open Q #3)
- `28th_april_TLS_Phase2_Redesign/61_Cookie_Phase3_Scope_Out.md` — formal Phase 3+ deferral record (Doc 57 R7 compliance)

### Source doctrine

- `28th_april_TLS_Phase2_Redesign/56_RTS_Principles_and_TLS_Alignment_Doctrine.md` §5 — distribution table source
- `28th_april_TLS_Phase2_Redesign/54_Marge_Redesign_Session_Lessons.md` — failure-mode case study

---

**End of file.** Next: `doctrine/04_authoring_rules.md` for the rule layer (R1–R7 + R1–R6 + R1–R5 + F1–F5).
