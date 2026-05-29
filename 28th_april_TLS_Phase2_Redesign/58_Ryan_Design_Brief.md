# Doc 58 — Ryan Design Brief

**Session:** 2026-05-25
**Branch:** `feature/prd-48-quests-engine-v2-bundled` (off `main`, unpushed)
**Author:** ENI (with LO)
**Status:** Design brief — applies to Ryan's authoring across current TLS slice + Phase 2+ continuation
**Supersedes:** nothing. First formal brief for Ryan. Doc 30 §4.2 + §5 + §8.2 names the fantasy and rough scope; this brief commits the per-lane budget + tier flags + vocabulary ceiling per Doc 56 R7 + Doc 57 R7.
**Sibling of:** Doc 31 (Frank brief, gold standard for escalation NPC), Doc 53 (Marge brief, gold standard for service NPC)
**Triggered by:** Doc 56 R7 / Doc 57 R7 precondition — no canvas authored for Ryan beyond current 4 until brief lands. Current slice ships Ryan as skeleton (1 activity + 1 transition + 1 first-date capstone + 3 quest cards). Deeper Ryan authoring requires this brief first.

---

## §1 — The question this doc answers

You're authoring more Ryan content (Lane 2 ambients, additional Lane 4 capstones, possibly a Lane 1 hub at his workplace or home). Before any canvas ships, decide:

- What arc shape is Ryan? *Peer/dating, per Doc 30 §4.2.*
- What's the per-lane budget? *Per Doc 57 §5 peer/dating row + slice scope (Stage 2 ceiling).*
- What's the vocabulary ceiling? *Open question — committed below.*
- What flags drive the chain? *Stage 0→4 trait + 8+ flag dominoes — full inventory below.*

---

## §2 — Arc shape

**Peer/dating** (Doc 30 §4.2, §5).

Ryan is a separate household — the handyman across the lawn / the yard partner. He's NOT in your kitchen at 6am. The arc lives in: Maya visiting his work surfaces, scheduled date events, and a paced relationship climb. No daily ambient saturation like Frank; no service-register flatness like Marge.

Reference per Doc 13 §5: Marcus arc in RTS is the canonical peer/quest-chain shape — deterministic chance=100% scenes with narrative prereqs ("Have at least 15 relationship points"). Ryan operates on the same logic: trust → flag → next scripted beat.

**Anti-pattern to avoid:** Frank-cloning. Authoring Ryan with 13 Lane 2 ambients and 7 Lane 3 substitutions to match Frank's distribution would betray the peer register (peer doesn't stalk Maya through her chores).

---

## §3 — Per-lane budget (Doc 57 §5 peer/dating row)

| Lane | Tier 1 (early) | Tier 2 (mid) | Tier 3 (late) | Capstones |
|---|---:|---:|---:|---:|
| L1 (hub-button) | 1 (visit shop / yard work) | 0–1 (date intro) | 0–1 (commit moment) | — |
| L2 (ambient) | 1 (yard encounter — already shipped) | 0–1 (drops by porch, low density) | 0 | — |
| L3 (substitution) | **0** | **0** | **0** | — |
| Capstones (Lane 4) | 1 (transition stage 0→1 — shipped) | 1 (first date — shipped) | 1–2 (second date, partner-commit) | 3–5 |
| **Per-shape total** | — | — | — | **8–12 canvases** |

**L3 = 0 by doctrine.** Peer/dating NPCs do not interrupt Maya's private chores. If a Ryan scene reads as "he walked in on me washing dishes," it's authored wrong — re-classify as Lane 1 (Maya visited his location) or Lane 2 (ambient yard encounter). The dispatcher-walk-in framing belongs to family/ambient shapes only.

**Current slice fill:** 1 L1 (activity) + 0 L2 + 0 L3 + 2 capstones + 1 transition = 4 canvases. Target for readable depth: 8–10 canvases.

---

## §4 — Vocabulary ceiling

**Slice scope: peer/dating register through Stage 2 (partner status). No Tier-3 sexual capstone in slice.**

**Full-ladder ceiling (Phase 2+): consummation permitted at Stage 3+ in peer/dating register.** The arc CAN reach explicit content — but the register stays peer-register (mutual, sincere, dating-shaped) rather than Frank's daddy-controlling cuckold register.

**Decision rationale (grounded):** Doc 30 §4.2 fantasy = *"First-boyfriend / wholesome corruption — dating chain leading to relationship."* This signals peer-shaped escalation. Doc 30 §7.5 vocabulary ceiling table (per agent inventory cite) committed to maximum-explicit for all in-scope arcs as default. Ryan's slice ceiling defers to *partner status* not consummation; full-ladder defers consummation to Phase 2+ when authored.

**LO call required if escalation timing changes.** If LO decides Ryan's Stage 3 sexual capstone should ship IN slice (not deferred to Phase 2+), this brief amends to add 1 Tier-3 capstone in §3 above.

---

## §5 — Tier flags + flag-set chain

**Stage trait** (verified `npc_ryan_stage`):
- 0 = Stranger
- 1 = Helper (yard partner)
- 2 = Partner (relationship status)
- 3 = Closer *(Phase 2+ — no canvas in slice)*
- 4 = After Beach *(Phase 2+ — no canvas in slice)*

**Quest-gate flags** (verified in TOML grep — agent inventory):
- `ryan_help_tier_open` — early-arc enabler
- `ryan_partner_open` — set by Ryan progression event when Maya reaches trust threshold; gates scene_ryan_first_date
- `ryan_first_date_done` — set by scene_ryan_first_date exit
- `ryan_big_deal_closed` — Phase 2+ flag (signals Ryan's narrative beat about the customer)
- `ryan_beach_proposal` — Phase 2+ flag (signals the after-beach turn)
- `ryan_keep_route_*` — 3 variant flags for Phase 2+ branch outcomes

**Daily resets:**
- `talked_to_ryan_today` — once-per-day conversation cap
- `watched_ryan_today` — once-per-day yard ambient cap

**Counter:**
- `ryan_help_count` — incremented by `activity_help_ryan_in_yard` exit (line 2078). Drives trust climb. Internal-to-activity, not surfaced on quest card.

**Trust:**
- `npc_ryan.trust` — primary climb variable. `trust >= 10` triggers `transition_ryan_to_1`.

**Chain continuity (Doc 50 R4):**
```
[start] → activity_help_ryan_in_yard (repeats, climbs trust)
       → transition_ryan_to_1 (capstone, sets npc_ryan_stage = 1)
       → [ryan_partner_open set by Ryan progression event downstream]
       → scene_ryan_first_date (capstone, gated on stage 1 + partner_open, sets ryan_first_date_done)
       → [Phase 2+ continuation]
```

**Verified consistent** with Doc 50 R4 chain continuity post-this-session's-fixes (R2 now correctly capstone pointing at first_date; R3 correctly terminal).

---

## §6 — Current state inventory (verified)

| Canvas | Lane | Status | Notes |
|---|---|---|---|
| `activity_help_ryan_in_yard` (line 2036) | L1/L3 (activity at his location) | ✅ shipped | Climbs `ryan_help_count` + `npc_ryan.trust`. Solo-with-Ryan-as-context activity. |
| `transition_ryan_to_1` (line 2770) | Lane 4 capstone, Type A | ✅ shipped | Fires once at trust ≥ 10. Tier-3 prose: *"Hey kid. Stick around. I got a guy comin' in."* Sets stage 1. |
| `scene_ryan_first_date` (line 7778) | Lane 4 capstone, Type A | ✅ shipped | Fires once at stage ≥ 1 + partner_open. Tier-3 dating prose. Sets `ryan_first_date_done`. |
| `scene_yard_with_ryan` (line 3198) | Lane 2 ambient (low density) | ✅ shipped | Yard random encounter. |
| Quest card R1 (line 2641) | Mechanic mode | ✅ fixed 2026-05-25 | Goals = trust ≥ 10. Climb toward stage 1. |
| Quest card R2 (line 2651) | Capstone mode | ✅ fixed 2026-05-25 | `ready_canvas = "scene_ryan_first_date"`. |
| Quest card R3 (line 2660) | Terminal | ✅ fixed 2026-05-25 | Slice closes here. Phase 2+ continuation deferred. |

Plus 3 dev shortcuts (`dev_open_ryan_partner`, etc.) at lines ~9892 — engine dev affordances, not player-facing.

**Cross-NPC reads:** Frank arcs read `npc_ryan_stage` in 3 places (Frank cascades reference Ryan stage for phase-gate logic — agent inventory lines 48, 156, 261). These reads are stable; this brief doesn't change them.

---

## §7 — Gap to readable depth

To bring Ryan to peer/dating readable depth (Doc 57 §5 target ~8–12 canvases), the following authoring is missing:

### Tier 1 — Early arc (1 new canvas)

- **Lane 1 — Visit Ryan at his workplace** (new): a daytime activity Maya can pick at his shop or workshop. Builds trust through conversation/help. Same activity-shape as `activity_help_ryan_in_yard` but at his location (not Maya's yard). Adds variety to the trust climb.

### Tier 2 — Mid arc (2 new canvases)

- **Lane 2 — Ryan drops by porch** (new, low density): once-or-twice across the arc, Ryan comes by with iced tea / something fixed / a small gift. Lane 2 random encounter on porch entry, low chance%, daily cap. Reads as "he's making an effort." Sets ambient texture without saturating.
- **Lane 4 capstone — Second date** (new, Type A): scripted dinner date or activity. Gated on `ryan_first_date_done` + a flag like `ryan_second_date_invited` (set by progression). Deepens the relationship.

### Tier 3 — Late arc (1–2 new canvases, dependent on Phase 2+ scope)

- **Lane 4 capstone — Partner commit** (new, Type B): real choice — *"Make it official"* / *"Keep it casual"*. Type B because the choice diverges downstream (committed-partner opens different content than casual-partner). Sets `ryan_partner_committed` flag.
- **Optional Lane 4 — Stage 3 consummation** (Phase 2+, deferred per §4 ceiling decision): peer/dating-register sex scene. Doc 30 §7.5 ceiling commit if LO opens slice scope.

### Total target after authoring: 4 current + 4 new (Tier 1+2) = **8 canvases for slice-complete Ryan**

Phase 2+ (Stage 3 + Stage 4 content) adds ~3–4 more canvases (commit fork + post-commit hub + sex scene + after-beach beat).

---

## §8 — Per-lane authoring plan

### Lane 1 — Visit at workplace

Single canvas at `loc_ryan_shop` (or wherever Ryan works during weekdays). Hub-style menu with 2–3 affordances (Help with the job, Talk a minute, Leave). Mirrors `activity_help_ryan_in_yard` shape but at Ryan's location, daytime schedule. Climbs trust via conversation rather than yard help.

### Lane 2 — Porch drop-by

Single Lane 2 random encounter. Trigger: `loc_porch` entry on weekday evening, chance 0.25, `talked_to_ryan_today is_false`, daily cap 1. Body: 2-beat encounter. Ryan brings iced tea / fixed something / a small token. Tier 1 prose register (RTS-flat + specific detail). Stat effect: `npc_ryan.trust +2`, `talked_to_ryan_today set`.

### Lane 4 — Second date capstone

Type A capstone. Trigger: `loc_yard` or `loc_residential_road`, schedule 18:00–22:00 weekday or weekend, gated on `ryan_first_date_done is_true` + `ryan_second_date_invited is_true` + `ryan_second_date_done is_false`. The `ryan_second_date_invited` flag is set by Ryan's progression (e.g., once trust ≥ 15 after first date). Body: scripted dinner or evening activity, Tier-3 prose, no fork (Type A simplicity preference per Doc 57 R2).

### Lane 4 — Partner commit capstone (Type B)

Type B capstone. Trigger: post-second-date, gated on `ryan_second_date_done is_true` + commit-eligible flag. Pattern F fork at terminal beat:
- **"Make it official"** → sets `ryan_partner_committed = true` + advances stage 2 → 3 → opens Phase 2+ continuation
- **"Keep it casual"** → does NOT set `ryan_partner_committed` → stays at stage 2 (slice terminal per R3 quest card)

Per Doc 57 F1: both branches must be playable in good faith. Per F2: real divergence in flag/downstream content. Per F4: refuse-path (Keep it casual) sets the alternative path's lock flag so the capstone can't re-fire.

---

## §9 — Pre-ship checklist (Doc 57 Appendix A applied to Ryan)

**Before authoring each new Ryan canvas:**
- [ ] Doc 56 R7 — this brief lock is the precondition. ✓ DONE (this doc)
- [ ] Doc 57 R7 — same. ✓
- [ ] Doc 57 §5 — canvas slot fits the peer/dating budget (no L3, light L2, capstone-driven)
- [ ] Doc 30 §7.5 — vocabulary ceiling honored (no Tier-3 sex in slice scope)

**Per new canvas:**
- [ ] Doc 56 R1 — if hub canvas, ONE opener (constant within canvas, no T0/T1/T2 prose)
- [ ] Doc 56 R2 — if tier-routed, T0/T1 endings on in-fiction interruption
- [ ] Doc 56 R5 — `guide` field present (once schema lands per Doc 62 PRD)
- [ ] Doc 57 R1 — if capstone, trigger fingerprint correct (is_repeatable=false OR is_repeatable=true+self-gate; priority ≥ 9; flag-setter on exit)
- [ ] Doc 57 R2 — default Type A; Type B only for real divergence (partner-commit capstone is the one legitimate Type B)
- [ ] Doc 57 R3 — quest card pointer for every priority-9+ capstone (Ryan's chain has clean coverage via R1-R3 cards post-2026-05-25 fixes)
- [ ] Doc 57 R5 — schedule + location match peer-register fiction (Ryan visits NOT at 3am, NOT at Frank's bedroom, etc.)
- [ ] Doc 57 §6 — capstones Tier-3; Lane 2 / activity scenes RTS-flat + specific detail (per `feedback_tls_scene_body_style` 2026-05-25 dual-register doctrine)
- [ ] Pattern F (if Type B) — F1-F5 per Doc 57 §7. Partner-commit fork is the only Type B in Ryan's slice; verify both branches at authoring time.

**Per slice:**
- [ ] Doc 56 R4 — Ryan location surfaced in sidebar radar (once C4 PRD lands)
- [ ] Doc 56 R6 — no `txt_only` quest cards (Ryan's 3 cards verified compliant post-2026-05-25)

---

## §10 — Open questions / scoped-out

- **Phase 2+ Stage 3+ ceiling commit.** Brief currently defers to LO: slice ends at Stage 2 partner, full ladder available in Phase 2+. If LO wants Stage 3 sex IN slice, brief amends §3 + §4.
- **Lane 1 hub at Ryan's home.** Currently only his workplace gets a Lane 1. If LO wants a home hub (Maya visits Ryan's place), add to §8 in a future brief amendment.
- **Beach proposal beat (Stage 4).** Doc 30 §4.2 references "After Beach" as Stage 4. The fiction of Ryan's beach proposal is sketched in Doc 30 but not authored. Phase 2+.
- **Ryan-as-cuckold framing.** Doc 30 §7.5 commits full cuckold ceiling for Frank. Ryan's slot in the cuckold dynamic (does Frank watch Maya date Ryan? Does Ryan know about Frank?) is currently undefined. Phase 2+ decision when cuckold content authored.
- **Cross-NPC arc transfer.** Per Doc 57 §10 cross-NPC transfer pattern (RTS `SellingMyStepsister`), no equivalent currently planned for Ryan. Phase 2+ open.

---

## §11 — References

### Sibling and ancestor docs

- **Doc 30** — TLS Test Redesign PRD (§4.2 fantasy, §5 NPC roster, §7.5 vocabulary ceiling, §8.2 NPC scope)
- **Doc 31** — Frank Arc Design Brief (gold-standard reference for escalation NPC brief shape)
- **Doc 50** — Quest Card Shape Doctrine (R3 + R4 quest card pointers for Ryan capstones)
- **Doc 53** — Marge Redesign Brief (sibling brief, service NPC)
- **Doc 56** — RTS Principles & TLS Alignment Doctrine (R1, R2, R4, R5, R6, R7 referenced above)
- **Doc 57** — Capstone Doctrine (Lane 4 R1–R5 + Pattern F F1–F5 referenced above)

### Memory entries

- `doc-56-rts-alignment-doctrine` — parent doctrine
- `doc-57-capstone-doctrine` — Lane 4 mechanism + per-arc budgets
- `feedback_tls_scene_body_style` — voice register (Lane 1/2/3 flat, Lane 4 Tier-3)
- `quest_card_shape_doctrine` — Doc 50 reference

### Live TLS reference (verified during session)

- `games/the_long_summer_test/toml_phases/7_final_game.toml:2036` — `activity_help_ryan_in_yard`
- `games/the_long_summer_test/toml_phases/7_final_game.toml:2770` — `transition_ryan_to_1`
- `games/the_long_summer_test/toml_phases/7_final_game.toml:3198` — `scene_yard_with_ryan`
- `games/the_long_summer_test/toml_phases/7_final_game.toml:7778` — `scene_ryan_first_date`
- `games/the_long_summer_test/toml_phases/7_final_game.toml:2641–2673` — quest cards R1/R2/R3 (post-2026-05-25 fixes)

### Engine references

- `npc_ryan_stage` trait — declared in NPC traits block (line ~321 per agent inventory)
- `getNpcLocation` (`v1.py:2758`) — used by future R4 sidebar radar to surface Ryan's location
- `triggerConditionsSatisfied` (`v1.py:2684–2952`) — predicate evaluation for Ryan capstone gates
