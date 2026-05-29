# Doc 59 — Jake Design Brief

**Session:** 2026-05-25
**Branch:** `feature/prd-48-quests-engine-v2-bundled` (off `main`, unpushed)
**Author:** ENI (with LO)
**Status:** Design brief — applies to Jake's authoring across current TLS slice + Phase 2+ continuation
**Supersedes:** nothing. First formal brief for Jake.
**Sibling of:** Doc 31 (Frank brief — adjacent shape: family/ambient), Doc 53 (Marge brief — service), Doc 58 (Ryan brief — peer/dating)
**Triggered by:** Doc 56 R7 / Doc 57 R7 precondition. Jake skeleton ships in slice (1 activity with stage cascade + 2 transitions + 1 catch_drawing capstone + 3 quest cards). Deeper Jake authoring requires this brief first.

---

## §1 — The question this doc answers

You're authoring more Jake content (more capstones, Lane 2 ambients, 1–3 Lane 3 substitutions). Decide:

- What arc shape is Jake? *Slow-burn family — distant family member, discrete revelation beats.*
- What's the per-lane budget? *Per Doc 57 §5 slow-burn row + slice scope (Stage 2 ceiling).*
- What's the vocabulary ceiling? *Full ladder, slice scope to Stage 2 (peek/draw reveal); Stage 3+ consummation = Phase 2+.*
- What flags drive the dual-path Stage 0→1 + linear 1→2 chain? *Full inventory below.*

---

## §2 — Arc shape

**Slow-burn family** (Doc 30 §4.2 — *"sibling incest, slow-burn, secret-from-the-house"*).

Jake is family-by-living-arrangement but emotionally distant — confined to his room, working on his sketchbook, doesn't enter the rest of the house much. The arc moves on **discrete revelation beats** rather than daily ambient saturation. Frank's family/ambient shape saturates Maya's daily life with daily proximity; Jake's slow-burn family shape concentrates intensity into a few key moments separated by long quiet stretches.

**Anti-pattern to avoid: Frank-cloning.** Authoring Jake with 4–7 Lane 3 substitutions like Frank would betray the slow-burn register — Jake doesn't show up while Maya washes dishes; he stays in his room. The 1–3 Lane 3 budget below is reserved for HIGH-stakes walk-ins (Maya in Jake's room mid-something, or Maya home alone with Jake).

**Reference shape:** RTS Brother arc (Doc 13 §16) is family/ambient. Jake is its slow-burn cousin — fewer canvases, denser per-canvas significance, dual-path Stage 0→1 entry.

---

## §3 — Per-lane budget (Doc 57 §5 slow-burn family row)

| Lane | Tier 1 (early) | Tier 2 (mid) | Tier 3 (late) | Capstones |
|---|---:|---:|---:|---:|
| L1 (hub-button) | 0 | 0–1 (charged room visit) | 1 (consummation hub, Phase 2+) | — |
| L2 (ambient) | 0–1 (hallway pass-by glance — already shipped via activity) | 0–1 (charged corridor moment) | 0 | — |
| L3 (substitution) | 0 | 1 (Jake walks in while Maya in his room) | 1–2 (high-stakes walk-ins, Phase 2+) | — |
| Capstones (Lane 4) | 2 (transition via_beauty + via_glance — shipped) | 1 (catch_drawing — shipped) | 1–2 (admit-it beat, Phase 2+) | 3–5 |
| **Per-shape total** | — | — | — | **10–15 canvases** |

**L3 budget = 1–3 (NOT 0).** Slow-burn family DOES get Lane 3 substitutions per Doc 57 §5 — but sparse, keyed to specific arc moments. The walk-in IS the beat. Don't pad with Frank-style daily walk-ins.

**Current slice fill:** 0 L1 + 0 L2 (the walk-past activity is Lane 3, not Lane 2) + 1 L3 (the activity's stage cascade) + 3 capstones + 2 transitions = **6 canvases**. Target for readable depth: 10–12.

---

## §4 — Vocabulary ceiling

**Slice scope: full ladder authorized through Stage 2 (peek/draw reveal capstone). Stage 3+ consummation deferred to Phase 2+.**

**Full-ladder ceiling: incest sex permitted at Stage 3+.** Doc 30 §4.2 commits the fantasy — *"sibling incest, slow-burn, secret-from-the-house."* The slow-burn register doesn't soften the consummation; it just paces it across more time. Stage 3 = tease/charged-physical, Stage 4 = consummation.

**Tier-3 carve-out per `feedback_tls_scene_body_style` 2026-05-03 update + Doc 57 §6:** Jake's capstones earn Tier-3 literary prose because they're once-only revelation beats. The shipped `scene_jake_caught_drawing` is exemplary — *"He doesn't slap it shut, which is somehow worse. He just watches you see it — the one before it your hands, the one before that your mouth, twenty pages of you he was never going to show anyone."* (line 7865).

**Slice scope decision:** Stage 0→1→2 ladder shipped. Stage 2→3 admit-it beat = Phase 2+ continuation. Stage 3 sex = Phase 2+. This brief commits to NOT authoring Stage 3+ content in current slice scope. LO call to amend if priority shifts.

---

## §5 — Tier flags + flag-set chain

**Stage trait** (verified `npc_jake_stage`):
- 0 = Hostile (Jake closed off, room door barely open)
- 1 = Noticed (he's seen Maya, registers her)
- 2 = Peek/Draw (he draws her secretly; she catches him)
- 3 = Tease *(Phase 2+ — no canvas in slice)*
- 4 = Caught *(Phase 2+ — no canvas in slice)*

**Quest-gate flags** (verified per agent inventory):
- `jake_first_glance_noticed` — set by walk-past activity's first-glance sub-branch (sets via Stage 0→1 glance path)
- `jake_peek_draw_revealed` — set by walk-past activity's branch when `peek_count >= 3 AND corruption >= 30` (Stage 1→2 gate)
- `jake_caught_drawing_done` — set by `scene_jake_caught_drawing` exit (Stage 2 closure)
- `jake_tease_open` — Phase 2+ flag (Stage 2→3 enabler)
- `jake_caught` — Phase 2+ flag (Stage 3→4 climax)
- `jake_hand` — Phase 2+ flag (specific moment, undocumented)
- `jake_keep_route_*` — Phase 2+ branch variant flags

**Daily resets:**
- `walked_past_jakes_today` — once-per-day cap on the walk-past activity

**Counter:**
- `jake_peek_count` — incremented by walk-past activity each pass. Internal-to-activity. Triggers `jake_peek_draw_revealed` flag at count ≥ 3 with corruption ≥ 30.

**Stage 0→1 dual-path** (Doc 57 §9 engine-constraint exemption per OR-logic ban in stage_helpers):
- **Path A — beauty:** `transition_jake_to_1_via_beauty` fires when `beauty >= 50` + stage 0 + glance flag is_false
- **Path B — glance:** `transition_jake_to_1_via_glance` fires when `jake_first_glance_noticed is_true` + stage 0

Both canvases ship identical body prose per the engine-constraint duplicate-prose exemption. Quest card J1 points at `transition_jake_to_1_via_beauty` (the more predictable path) per Doc 50 R1 convention.

**Chain continuity (Doc 50 R4):**
```
[start] → activity_walk_past_jakes_door (repeats, increments peek_count)
       → transition_jake_to_1_via_beauty OR _via_glance (capstone, sets stage 1)
       → activity branch (peek_count >= 3 + corruption >= 30 → sets jake_peek_draw_revealed → stage 2)
       → scene_jake_caught_drawing (capstone, gated on stage 2 + revealed flag, sets caught_drawing_done)
       → [Phase 2+ continuation]
```

**Verified consistent** with Doc 50 R4 chain continuity post-2026-05-25 fixes (J1 capstone, J2 mechanic with unlocks-comment, J3 terminal).

---

## §6 — Current state inventory (verified)

| Canvas | Lane | Status | Notes |
|---|---|---|---|
| `activity_walk_past_jakes_door` (line 2102) | L3 hub-routed activity with stage cascade | ✅ shipped | Contains Stage 0/1/2 inline branching at line 2174. Increments `jake_peek_count`. Sets `jake_first_glance_noticed` on Stage 0 sub-branch. Sets `jake_peek_draw_revealed` + writes `npc_jake_stage = 2` on Stage 1 progression branch. |
| `transition_jake_to_1_via_beauty` (line 2828) | Lane 4 capstone, Type A | ✅ shipped | Fires at beauty ≥ 50. Duplicate-prose-with-via_glance per engine-constraint exemption. |
| `transition_jake_to_1_via_glance` (line 2866) | Lane 4 capstone, Type A | ✅ shipped | Fires at `jake_first_glance_noticed is_true`. Duplicate-prose-with-via_beauty. |
| `scene_jake_caught_drawing` (line 7838) | Lane 4 capstone, Type A | ✅ shipped | Tier-3 literary. Gates: stage ≥ 2 + revealed + not done. Sets `jake_caught_drawing_done`. |
| Quest card J1 (line 2672) | Capstone mode | ✅ fixed 2026-05-25 | `ready_canvas = "transition_jake_to_1_via_beauty"` + goals beauty ≥ 50. |
| Quest card J2 (line 2681) | Mechanic mode | ✅ fixed 2026-05-25 | `# unlocks: jake_peek_draw_revealed via activity_walk_past_jakes_door` comment. |
| Quest card J3 (line 2689) | Terminal | ✅ fixed 2026-05-25 | Slice closes here. Phase 2+ continuation deferred. |

**Voice register verified:** `scene_jake_caught_drawing` is Tier-3 literary (appropriate per Doc 57 §6 — capstones earn Tier-3). The walk-past activity stage cascade body uses RTS-flat + specific detail (appropriate per Doc 56 R2 for repeatable content).

---

## §7 — Gap to readable depth

To bring Jake to slow-burn-family readable depth (Doc 57 §5 target ~10–15 canvases), the following authoring is missing:

### Tier 2 — Mid arc (2–3 new canvases)

- **Lane 2 — Hallway charged-corridor moment** (new): once-per-arc Lane 2 ambient firing in hallway at evening, post-Stage 1. Maya passes Jake's door; their eyes meet through the gap. Low chance, daily cap, requires `npc_jake_stage >= 1`. Tier 1 prose register (RTS-flat + specific detail).
- **Lane 3 — Jake walks past while Maya in living room sketching** (new, Tier 2 walk-in): substitution on a Maya-solo "sketch in the living room" activity (if exists) OR "read on couch" activity. Jake passes; charged moment. Stage ≥ 1, daily cap. Tier 2 escalation intensity (charged but not explicit at Stage 1; gets more explicit at Stage 2).
- **Lane 4 capstone — Stage 2 admit beat** (new, Type A): Maya goes back to Jake's room after catch_drawing fired; he admits / they have a charged conversation about the drawings. Tier-3 prose. Sets `jake_admitted_drawings` flag.

### Tier 3 — Late arc (3 new canvases, all Phase 2+)

- **Lane 4 — Stage 2→3 tease unlock** (Phase 2+): Jake initiates physical contact. Tier-3.
- **Lane 4 — Stage 3 hand/charged scene** (Phase 2+): mid-arc tease beat, possibly Type B (Accept fork = continued physical / Refuse = pull back).
- **Lane 4 — Stage 4 consummation** (Phase 2+): incest sex scene. Tier-3 literary, full vocabulary ceiling, possibly framed around the sketchbook as the through-line.

### Total target after authoring: 6 current + 3 new (Tier 2 slice scope) = **9 canvases for slice-complete Jake**

Phase 2+ adds 3–4 more capstones to reach ~12–13 canvases total. This sits in the middle of the §3 target range (10–15).

---

## §8 — Per-lane authoring plan

### Lane 2 — Hallway charged-corridor moment

Single Lane 2 ambient at `loc_hallway`. Trigger: `npc_jake_stage >= 1` + `walked_past_jakes_today is_false` + evening time band (e.g., 19:00–22:00) + chance 0.30 + daily cap 1. Body: 2-beat encounter — Maya passes the door (now open wider than usual), their eyes meet, Jake doesn't look away, Maya doesn't either. R2-compliant ending: internal stop ("neither of you steps back"). Tier 1 RTS-flat prose. Stat effect: `npc_jake.arousal +1`, `jake_peek_count` NOT incremented (this is a separate Lane 2 encounter, not the walk-past activity).

### Lane 3 — Jake walks past while Maya solo-activity

Substitution on a Maya-solo living room activity. Could substitute on `activity_read_on_couch` (if exists) or `activity_sketch_in_living_room` (new). Gated on `npc_jake_stage >= 2` + Jake in his room (which is always, per Jake's schedule). Chance 0.30. Body: 2-tier — T0 (Stage 2): Jake passes by, sees Maya's sketches, lingers; T1 (Stage 3, Phase 2+): Jake stays, asks to see them.

### Lane 4 capstone — Stage 2 admit beat

Type A capstone. Trigger: `loc_jakes_room` entry, gated on `jake_caught_drawing_done is_true` + `jake_admitted_drawings is_false` + sequential daily-pace gate (e.g., 2+ in-game days after caught_drawing). Body: Tier-3 literary scripted scene. Maya returns to Jake's room; he's expecting her. The conversation about the sketchbook becomes the admission. Sets `jake_admitted_drawings` flag.

---

## §9 — Pre-ship checklist (Doc 57 Appendix A applied to Jake)

**Before authoring each new Jake canvas:**
- [ ] Doc 56 R7 — this brief lock is the precondition. ✓ DONE (this doc)
- [ ] Doc 57 R7 — same. ✓
- [ ] Doc 57 §5 — canvas slot fits slow-burn family budget (sparse L3, dense per-canvas significance)
- [ ] Doc 30 §7.5 — vocabulary ceiling honored (Stage 3+ deferred to Phase 2+ per §4)

**Per new canvas:**
- [ ] Doc 56 R1 — if hub canvas, ONE opener (constant within canvas, no T0/T1/T2 prose). Jake currently has 0 hubs; if Stage 3+ hub authored, follow R1.
- [ ] Doc 56 R2 — if tier-routed, T0/T1 endings on in-fiction interruption. Lane 3 charged walk-ins benefit from this most.
- [ ] Doc 56 R5 — `guide` field present (once C1 schema lands)
- [ ] Doc 57 R1 — if capstone, trigger fingerprint correct
- [ ] Doc 57 R2 — default Type A; Type B only for real divergence (Stage 3 hand/charged scene MAY be Type B if hand-or-pull-back fork is structural)
- [ ] Doc 57 R3 — quest card pointer for every priority-9+ capstone (Jake's chain has clean coverage via J1/J2/J3 cards post-2026-05-25)
- [ ] Doc 57 R5 — schedule + location match slow-burn fiction (Jake's room is the gravity; the rest is "Maya passes near")
- [ ] Doc 57 §6 — capstones Tier-3; Lane 2 / Lane 3 walk-ins RTS-flat + specific detail
- [ ] Doc 57 §9 engine-constraint exemption — duplicate-prose between via_beauty + via_glance is sanctioned; don't diverge

**Per slice:**
- [ ] Doc 56 R4 — Jake location surfaced in sidebar radar (once C3 PRD lands). Jake is always in his room — sidebar would render "Jake — His room" continuously.
- [ ] Doc 56 R6 — no `txt_only` quest cards (J1/J2/J3 verified compliant post-2026-05-25)

---

## §10 — Open questions / scoped-out

- **Stage 3+ ceiling timing.** Currently slice ends at Stage 2 caught_drawing. LO call if Stage 3 admit-it should ship IN slice (would add 1–2 capstones). Stage 4 consummation = Phase 2+ regardless.
- **Pregnancy retrofit.** If Doc 65 Phase 2+ decision opens pregnancy in scope, Jake's Stage 4 sex scene authoring needs the pregnancy-variant framing (per Doc 30 §7.3.1). All current Jake content is bareback-compatible (no contraception language).
- **Cross-NPC reads.** Diana's awareness might rise when Maya spends time in Jake's room — currently not implemented. Future decision per Doc 65 scandal/awareness scope.
- **The sketchbook as through-line.** `scene_jake_caught_drawing` establishes the sketchbook as the arc's narrative center. Phase 2+ authoring should keep returning to it (admit beat about pages; Stage 3 Jake brings new pages; Stage 4 the sketchbook becomes the seduction prop).
- **Sibling status canon.** Doc 30 §4.2 says "sibling incest" — confirm Jake's relationship to Maya in TLS canon. (Marge "Diana's girl" suggests Maya is Diana's daughter; Jake is Diana+Frank's son → stepbrother by Frank's marriage to Diana.) The relational vocabulary in capstone prose should reflect this — *"your stepbrother"* not *"the kid in the next room."*

---

## §11 — References

### Sibling and ancestor docs

- **Doc 30** — TLS Test Redesign PRD (§4.2 fantasy, §5 NPC roster, §7.5 vocabulary ceiling, §8.2 NPC scope)
- **Doc 31** — Frank Arc Design Brief (adjacent shape: family/ambient)
- **Doc 50** — Quest Card Shape Doctrine (R3, R4 quest card pointers for Jake capstones)
- **Doc 53** — Marge Redesign Brief (sibling brief, service NPC)
- **Doc 56** — RTS Principles & TLS Alignment Doctrine
- **Doc 57** — Capstone Doctrine (Lane 4 R1–R5 + §9 engine-constraint exemption for duplicate-prose capstones)
- **Doc 58** — Ryan Design Brief (sibling brief, peer/dating)

### Memory entries

- `doc-56-rts-alignment-doctrine` — parent doctrine
- `doc-57-capstone-doctrine` — Lane 4 mechanism + engine-constraint exemption
- `feedback_tls_scene_body_style` — voice register

### Live TLS reference (verified during session)

- `games/the_long_summer_test/toml_phases/7_final_game.toml:2102` — `activity_walk_past_jakes_door` with stage cascade
- `games/the_long_summer_test/toml_phases/7_final_game.toml:2828` — `transition_jake_to_1_via_beauty`
- `games/the_long_summer_test/toml_phases/7_final_game.toml:2866` — `transition_jake_to_1_via_glance`
- `games/the_long_summer_test/toml_phases/7_final_game.toml:7838` — `scene_jake_caught_drawing`
- `games/the_long_summer_test/toml_phases/7_final_game.toml:2672–2694` — quest cards J1/J2/J3 (post-2026-05-25 fixes)

### Engine references

- `npc_jake_stage` trait — declared in NPC traits block
- `loc_jakes_room` location declaration (per Doc 30 §3 / TOML line ~691)
- Walk-past activity's stage cascade at line 2174 — internal Stage 1→2 transition trigger
