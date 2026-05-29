# Doc 51 — Marge Design Brief

> **⚠️ SUPERSEDED 2026-05-24** by Doc 53 — Marge Redesign Brief.
> The implementation against this brief shipped 3 passes + voice-tightening and was stripped same day. Doctrine violations: Lane 1 over-weighted (10 hub items per Doc 24 §10.3 menu-game anti-pattern), Lane 2/3 forced onto a service NPC that has no escalation register to carry charged ambient/walk-in content (Doc 30 §7.5 deferred Phase 3+), voice authored as literary prose where TLS demands RTS-flat (per `feedback_tls_scene_body_style` memory). Doc 53 is the doctrine-faithful redesign. **Read Doc 53 first**; this doc remains as a record of what was tried.

**Session:** 2026-05-24
**Branch:** `feature/prd-48-quests-engine-v2-bundled` (off `main`, unpushed)
**Author:** ENI (with LO)
**Status:** Design brief — design-only. Implementation deferred to a separate phase.
**Sibling of:** Doc 31 (Frank Arc Design Brief). Same section discipline, different arc shape — Frank pure capstone, Marge pure mechanic.
**Mode (per Doc 50 §2):** PURE MECHANIC. Post-hire arc has zero scripted-scene capstones in slice scope. Every threshold cross is the unlock.
**Triggered by:** Phase 2 NPC redesign push, 2026-05-24. With Frank's slice complete and Doc 50 codified, the doctrine itself needs testing against the two card-modes Frank doesn't exercise. Marge = the pure-mechanic test. Jake (separate brief) = the hybrid test.
**Scope:** post-hire only. The hire (`canvas_marge_interview`) is canon and untouched. Thursday-key + workplace-seduction content stays Phase 3+.

---

## §1 End-state fantasy (slice scope, Day 10)

Maya is one of Marge's. The apron lives on a hook with her name pencilled above it. Cookie says her name when she walks in instead of nodding. The bank deposit goes in Maya's hands twice a week and Marge doesn't watch her count it. Money comes in steady — not a lot, enough for rent and a little float. The whole arrangement is professional, not warm — Marge isn't a smiler — but it's an arrangement, and arrangements in this town take weeks to earn.

What this is NOT: not flirtation, not seduction, not the Thursday key. Marge has read Maya inside thirty seconds and she's seen this register before. The slice scope is the climb from *Diana's girl* (the hire) to *one of hers* (the close-out). That's the whole arc.

---

## §2 Marge's voice spec

Already locked in NPC description (`7_final_game.toml:528`). Expanding here for the implementation phase.

**Register:** matriarch, dry, broad, no theatre. Late forties, southern owner-operator. Honest about the wage, the floor, the customer tier. Never raises her voice; never has to.

**What she WILL say** (in slice scope):
- Wage arithmetic. *"Five hours, four-fifty an hour, you keep your tips."*
- Floor instructions. *"Two coffees at the truckers' booth before they ask."*
- Customer reads. *"Mr. Hollis tips on the cash, not the card. Run it cash for him."*
- Kitchen politics. *"Cookie's having a day. Don't reach for the spatula."*
- Tip arithmetic at end of shift. *"You're light eight off the cards but heavy nine on the float, call it a wash."*

**What she WON'T say** (slice scope — Phase 3+ opens these):
- Flirtation, double-meaning, anything sexual. Strictly professional.
- Comments on Maya's appearance beyond the practical (the shoes, the hands — the up-and-down a woman who's hired forty waitresses does, never the up-and-down a man does).
- Anything implying she doesn't see what's happening at the house. She sees. She doesn't say.
- Soft cues, encouragements, *"you're doing great."* Marge doesn't give those. The reward is more responsibility, not warmer words.

**Example line per tier** (locks the register):

- **T0 hire-week:** *"You're either on the floor or you're a customer, hon. Which one today."* (already in TOML at line 7828)
- **T1 trusted-on-floor:** *"There she is. Coffee's fresh if you're not here to work for once."* (already in TOML at line 7835)
- **T2 reliable:** *"Bank bag's on the desk. You don't need me looking over your shoulder to count it."* (NEW for T2 — to be authored)

---

## §3 Trust ladder (3 tiers, pure mechanic)

`npc_marge.trust` is the persistent climb. Climbs via every worked shift (+1 per `scene_diner_t0_shift`, +1.5 per `scene_diner_t1_shift`). No decay. Three tiers in slice scope:

| Tier | `marge.trust` band | Marge's read of Maya | What it *means* |
|------|--------------------|----------------------|------------------|
| T0   | 0–19  | New hire, untrusted        | Boss-employee. Marge runs the floor. Maya takes orders. |
| T1   | 20–39 | Reliable, can run the floor | Marge leaves the counter sometimes. Kitchen opens up. Cookie greets by name. |
| T2   | 40+   | Trusted, one of hers       | Close-out access. Bank deposit. Marge stops watching. |

**Important naming clash to flag:** the existing shift canvases use "T0/T1" in their *names* (`scene_diner_t0_shift`, `scene_diner_t1_shift`) — but those refer to **shift quality**, gated by Maya's `corruption + rep_road + beauty`, NOT by `marge.trust`. The shift T0/T1 and the Marge trust T0/T1 are independent axes:
- **Shift T0/T1** = what Maya is willing to do on the floor (Maya-stat-driven)
- **Marge T0/T1/T2** = how much Marge has come to trust Maya (relational-driven)

Both axes climb at the same time but unlock different things. The brief uses "T0/T1/T2" for Marge tiers exclusively from here forward. Shift names stay as the TOML has them.

---

## §4 Per-tier content menu (LOAD-BEARING — author's deliverables list)

Each tier names the concrete deliverables. The implementation phase reads this section, authors the listed canvases, wires them in.

### T0 — New hire (`marge.trust` 0–19)

Available immediately post-hire. Pre-existing surfaces stay as-is; new content listed below.

**Lane 1 (hub menu items at `scene_marge_diner_hub`):**
- ✅ EXISTING: "Take a shift" → routes to `scene_diner_t0_shift` (or `scene_diner_t1_shift` if Maya stats unlock it). No change.
- ✅ EXISTING: "Talk to Marge" → simple chat node.
- 🆕 NEW: "Sit at the counter for a coffee" — 30-min activity, no pay, +0.5 `marge.trust`, +1 energy. Available all hub hours. Marge says one of 3 weather/customer lines.
- 🆕 NEW: "Ask Marge about a regular" — 15-min, gossip about one of 3 named regulars (Mr. Hollis / the truckers / the Wednesday lunch ladies). +0.5 `marge.trust`. Marge gives a customer-read line per regular.

**Lane 2 (ambient at `loc_diner_front`):**
- 🆕 NEW ambient 1: Marge counting tickets at the register, doesn't look up. One-line greeting. Chance 20% on entry, daily-once cooldown.
- 🆕 NEW ambient 2: Marge on the phone with a supplier. Short overheard line. Chance 15% on entry, daily-once cooldown.

**Lane 3 (substitution rules):**
- 🆕 NEW: when Maya does a Maya-solo activity at `loc_diner_front` (e.g., "wipe down a booth on a slow afternoon" — needs new solo activity authored too, or hook into existing solo activities), Marge wanders in to wipe the counter and exchange a line. ~25% chance.

### T1 — Trusted on the floor (`marge.trust` 20–39)

Unlocks at trust ≥ 20. NEW menu items appear inside `scene_marge_diner_hub`. Cookie kitchen access opens.

**Lane 1 (NEW hub menu items, gated by trust ≥ 20):**
- 🆕 "Help Cookie prep in the kitchen" — 60-min, $0, +1 `marge.trust`, +1 `cookie.trust` (new trait? or shared with cookie texture). Opens the kitchen as a sub-surface. Cookie says one of 3 banter lines.
- 🆕 "Ask Marge about a regular's tab" — 15-min, learn customer-specific tipping pattern. +0.5 `marge.trust`, +1 `rep_road` (small).
- 🆕 "Take a long shift" — 6h variant of `scene_diner_t0_shift`, slightly better pay. Opens at trust 20.

**Lane 2 (NEW ambient, trust ≥ 20):**
- 🆕 Marge giving Cookie a smoke break and Maya covers the counter for ten minutes. Texture, no progression.
- 🆕 Marge counting the till at close of dinner rush and inviting Maya to watch the math. Texture + one practical observation.

**Lane 3 (NEW substitution rules, trust ≥ 20):**
- 🆕 When Maya is doing late-night solo activity at the diner (e.g., refilling sugar caddies after close), Marge stays past her hours to keep her company. ~25% chance. Cookie may also appear here as texture.

**R5 unlock comment on M2 quest card (T0 → T1 climbing card):**
```toml
# unlocks at marge.trust >= 20:
#   - hub menu items: "Help Cookie prep", "Ask about a regular's tab", "Take a long shift"
#   - Lane 2 ambient: marge_cookie_smoke, marge_till_math
#   - Lane 3 substitution: marge_late_company on Maya-solo late-diner dispatcher
```

### T2 — Reliable, one of hers (`marge.trust` 40+)

Unlocks at trust ≥ 40. NEW menu items + close-out access + the terminal flag.

**Lane 1 (NEW hub menu items, gated by trust ≥ 40):**
- 🆕 "Close out the diner with Marge" — 45-min, late-night, high tip rate, +2 `marge.trust`. **This is the canvas that sets `marge_reliable_reached`** when used the first time at T2. Subsequent uses just give the pay/trust.
- 🆕 "Run the late shift solo" — late-shift variant, +$15 over base, higher fatigue cost, +1 `marge.trust`. Marge isn't on the floor.
- 🆕 "Sit with Cookie after close for coffee" — 30-min, after-hours, Cookie talks more freely. +0.5 `marge.trust`, +1 `cookie.trust`.

**Lane 2 (NEW ambient, trust ≥ 40):**
- 🆕 Marge handing Maya the closing paperwork without looking up. One-line texture. The arrangement made canon.
- 🆕 Cookie inviting Maya outside for a real cigarette (Maya can refuse — she doesn't smoke — but the invitation is the beat).

**Lane 3 (NEW substitution rules, trust ≥ 40):**
- 🆕 When Maya is doing solo close-out activity (refilling caddies / wiping booths after hours), Marge stays back to talk about a customer who tipped strange — texture, no progression.

**R5 unlock comment on M3 quest card (T1 → T2 climbing card):**
```toml
# unlocks at marge.trust >= 40:
#   - hub menu items: "Close out the diner", "Run the late shift solo", "Sit with Cookie after close"
#   - Lane 2 ambient: marge_paperwork_handoff, cookie_real_cigarette
#   - Lane 3 substitution: marge_late_talk on Maya-solo close-out dispatcher
#   - terminal flag setter: "Close out the diner with Marge" canvas sets marge_reliable_reached
```

---

## §5 Lane-by-lane content map (cross-tier compact view)

Single table indexing every Marge surface across all three tiers. Implementation grep target.

| Lane | Tier | Slug (proposed) | Trigger / Surface | Chance | Effects (rough) |
|------|------|-----------------|-------------------|--------|-----------------|
| 1    | T0   | hub_marge_shift (existing) | hub menu, all hours | 100% (pick) | $45 base shift, +1 trust |
| 1    | T0   | hub_marge_coffee | hub menu, all hours | 100% (pick) | +0.5 trust, +1 energy, -10 hygiene drain |
| 1    | T0   | hub_marge_regular_chat | hub menu | 100% (pick) | +0.5 trust, customer-read |
| 2    | T0   | ambient_marge_tickets | `loc_diner_front` entry | 20% | texture |
| 2    | T0   | ambient_marge_supplier | `loc_diner_front` entry | 15% | texture |
| 3    | T0   | sub_marge_wipe_counter | Maya-solo diner activity | 25% | texture + one line |
| 1    | T1   | hub_marge_cookie_kitchen | hub menu, trust ≥ 20 | 100% (pick) | $0, +1 marge, +1 cookie |
| 1    | T1   | hub_marge_regular_tab | hub menu, trust ≥ 20 | 100% (pick) | +0.5 trust, +1 rep_road |
| 1    | T1   | hub_marge_long_shift | hub menu, trust ≥ 20 | 100% (pick) | $60, +1.5 trust, 6h |
| 2    | T1   | ambient_marge_smoke_cover | entry, trust ≥ 20 | 20% | texture |
| 2    | T1   | ambient_marge_till_math | entry, trust ≥ 20 | 15% | texture + practical |
| 3    | T1   | sub_marge_late_company | late-diner solo, trust ≥ 20 | 25% | texture |
| 1    | T2   | hub_marge_close_out | hub menu, trust ≥ 40, after 21:00 | 100% (pick) | $80, +2 trust, sets `marge_reliable_reached` first use |
| 1    | T2   | hub_marge_late_solo | hub menu, trust ≥ 40, late hours | 100% (pick) | $60 + tips, +1 trust |
| 1    | T2   | hub_cookie_after_coffee | hub menu, trust ≥ 40, after close | 100% (pick) | +0.5 trust, +1 cookie |
| 2    | T2   | ambient_marge_paperwork | entry, trust ≥ 40 | 15% | texture, "one of hers" beat |
| 2    | T2   | ambient_cookie_real_smoke | entry, trust ≥ 40 | 15% | texture |
| 3    | T2   | sub_marge_late_talk | close-out solo, trust ≥ 40 | 25% | texture |

Total NEW deliverables: ~16 canvases + 1 new flag + 1 NPC schedule block.

---

## §6 Capstones (slice scope)

**Slice has exactly ONE capstone in Marge's arc: the hire.**

- `canvas_marge_interview` (TOML:1595+) — already exists. One-shot. Priority 9. Gates `hired_at_diner is_false`. Sets `hired_at_diner` on the only choice exit (Marge doesn't wait for an answer; the apron slides across).
- This is the *entry point* to Marge's arc. The pure-mechanic chain begins after this fires.

**All post-hire content is pure-mechanic.** No `ready_canvas` anywhere in M2/M3/M4 quest cards. Threshold cross IS the unlock.

**Deferred capstones (Phase 3+ — flagged here so future authors know the arc has growth room):**
- **Thursday key** (`first_ambient_tilt`) — week-3 minimum per Doc 30 §8.2. The moment Marge hands Maya the key to the diner. Would be a capstone in a longer slice; deferred.
- **Workplace seduction** — Marge as dominant matriarch per Doc 30 fantasy notes. Phase 3+ register. Out of slice scope.
- **Cookie pairing** (lesbian first-fling) — separate arc, Cookie's own brief when she gets one.

---

## §7 Quest card chain (applying Doc 50)

Four cards total. All under Frank's NPC section pattern but with `npc_id = "npc_marge"`. The pure-mechanic shape this exercises is the core Doc 50 test.

| Card | `when` | `goals` | `ready_canvas` | Mode | Doc 50 rule applications |
|------|--------|---------|----------------|------|--------------------------|
| **M1** Pre-hire | `hired_at_diner is_false` | — | `canvas_marge_interview` | Capstone | R1 ✓ (hire covered), R4 ✓ (chain root) |
| **M2** T0 climbing | `hired_at_diner is_true` + `marge.trust lt 20` | trust ≥ 20, label "Marge trust" | — (none) | Pure mechanic | R2 ✓ (climb visible), R5 ✓ (`# unlocks:` comment for T1), R6 ✓ (label in voice) |
| **M3** T1 climbing | `marge.trust gte 20` + `marge.trust lt 40` | trust ≥ 40, label "Marge trust" | — (none) | Pure mechanic | R2 ✓, R5 ✓ (T2 unlocks), R6 ✓ |
| **M4** Terminal | `marge_reliable_reached is_true` | — | — | Terminal | R3 ✓ (last card), R4 ✓ (predecessor M3 climbs into the unlock canvas that sets this flag) |

**Worked prose (illustrative — locks voice, not final copy):**

**M1 — Pre-hire:**
```
text         = "Marge's the only place in town hiring on a Monday. I need to walk in there before the dinner rush."
ready_text   = "She's at the register. Now or never."
tip          = "Walk into the diner. Don't wait for an invitation."
npc_id       = "npc_marge"
ready_canvas = "canvas_marge_interview"
when         = [{ flag = "hired_at_diner", op = "is_false" }]
```

**M2 — T0 climbing toward T1:**
```toml
text   = "I'm on Marge's floor now. She watches everything. Long shifts come when she stops watching."
npc_id = "npc_marge"
when = [
  { flag  = "hired_at_diner",                 op = "is_true" },
  { trait = "trust", subject = "npc", npc_id = "npc_marge", op = "lt", value = 20 },
]
goals = [
  { trait = "trust", subject = "npc", npc_id = "npc_marge", op = "gte", value = 20, label = "Marge trust" },
]
# unlocks at marge.trust >= 20:
#   - hub menu items: hub_marge_cookie_kitchen, hub_marge_regular_tab, hub_marge_long_shift
#   - Lane 2 ambient: ambient_marge_smoke_cover, ambient_marge_till_math
#   - Lane 3 substitution: sub_marge_late_company
```

**M3 — T1 climbing toward T2:**
```toml
text   = "She's started leaving me with it. The kitchen, the till some afternoons. Keep showing up."
npc_id = "npc_marge"
when = [
  { trait = "trust", subject = "npc", npc_id = "npc_marge", op = "gte", value = 20 },
  { trait = "trust", subject = "npc", npc_id = "npc_marge", op = "lt",  value = 40 },
]
goals = [
  { trait = "trust", subject = "npc", npc_id = "npc_marge", op = "gte", value = 40, label = "Marge trust" },
]
# unlocks at marge.trust >= 40:
#   - hub menu items: hub_marge_close_out, hub_marge_late_solo, hub_cookie_after_coffee
#   - Lane 2 ambient: ambient_marge_paperwork, ambient_cookie_real_smoke
#   - Lane 3 substitution: sub_marge_late_talk
#   - terminal flag setter: hub_marge_close_out sets marge_reliable_reached on first use at T2
```

**M4 — Terminal:**
```toml
text     = "She handed me the close-out without looking up. I'm one of hers now."
npc_id   = "npc_marge"
priority = 1
terminal = true
when     = [{ flag = "marge_reliable_reached", op = "is_true" }]
```

Every card complies with Doc 50. Walked once in §7's last paragraph:
- R1 capstone coverage — hire is covered by M1; no other capstones in slice.
- R2 climbing-bullet — M2 and M3 both have `goals` blocks for visible climbs.
- R3 terminal placement — M4 is last; `marge_reliable_reached` is the latest flag in the chain.
- R4 chain continuity — every "post-X" requirement has a predecessor card setting it up.
- R5 mechanic-tier `# unlocks:` — present on M2 and M3.
- R6 labels in voice — *"Marge trust,"* not `marge.trust`.

---

## §8 Cross-arc state writes / reads

**Marge writes (other arcs read):**
- `hired_at_diner` — set by `canvas_marge_interview`. Read by phone activation (`phone_active`), economic loop (rent payment), Story Goal SG1.
- `marge.trust` — climbs via worked shifts + hub menu items. No other slice arc reads it.
- `marge_reliable_reached` — NEW flag. Set by `hub_marge_close_out` first use at T2. Read by M4 terminal card.

**Marge reads (other arcs write):**
- `player.hygiene` — diner shifts dock tips below 40 (TOML:1499 hygiene line). Existing mechanic. Brief does NOT change this — it's named here so the wiring is visible.
- `player.energy` — shifts cost energy. Standard.
- `player.corruption + rep_road + beauty` — gate `scene_diner_t1_shift` (Maya-stat axis, not Marge-trust axis). Existing. Brief does NOT change.
- `cookie.trust` (proposed new trait if Cookie ever leaves texture status) — would be written by `hub_marge_cookie_kitchen` + `hub_cookie_after_coffee`. **For slice: treat as texture-only.** If Cookie gets her own brief, this is where the wire lives.

**No coupling to Frank / Ryan / Jake / Diana arcs.** Marge is structurally isolated. By design — pure-mechanic test wants no cross-arc coupling that would muddy the doctrine read.

---

## §9 Anti-patterns (what NOT to write for Marge)

Lifted from Doc 31 §7 patterns and adapted to Marge's register + Doc 50 rules.

- **No flirtation / double-meaning lines.** Slice scope. Marge is strictly professional. Phase 3+ opens the seduction register. If a line in any T0/T1/T2 surface reads as flirty, rewrite it.
- **No scripted scenes between hire and Thursday-key.** Post-hire arc is pure-mechanic by design. If a content beat wants a scripted scene, it's wrong for this arc — either author it into Lane 2 ambient (no flag set) or push to Phase 3+.
- **No `ready_canvas` on M2 / M3 / M4.** M2 and M3 are mechanic-tier; threshold cross IS the unlock. M4 is terminal. Putting `ready_canvas` on any of them violates the pure-mechanic test.
- **No Cookie standalone surfaces.** Cookie texture lives inside Marge's hub menu items + Lane 2 ambients. Cookie does not get her own hub, schedule, or quest cards in slice. If she does in a future phase, that's a new brief.
- **No daily-flag latches dressed as permanent milestones.** `talked_to_marge_today` exists as a daily-reset (cleared in `[engine.daily_tick]`). It does NOT gate trust climb or unlock content. Doc 49 anti-pattern.
- **No labels using raw trait keys.** `label = "marge.trust"` is wrong. `label = "Marge trust"` is right. Doc 50 R6.
- **No collapsing the shift T0/T1 with Marge T0/T1.** They're independent axes. Shift quality is Maya-stat-gated; Marge tier is trust-gated. Mixing them confuses both mechanics.
- **No "+trust" effects on non-Marge-context activities.** Trust climbs only via Marge-touching surfaces: worked shifts at her diner + hub menu items at her hub. Maya helping at the church doesn't bump `marge.trust`, even if it's "nice."

---

## §10 Acceptance criteria (E-checkpoint)

Implementation phase is complete when ALL of these land:

1. **NPC schedule** — `[[npcs.schedules]]` declared for `npc_marge` (Mon–Sat 09:00–22:00 at `loc_diner_front`). Closes the existing validator warning.
2. **Hub T2 group** — `scene_marge_diner_hub` extended from 2 tiers to 3. T2 group added (trust ≥ 40 greeting + menu access).
3. **Lane 1 — 9 new hub menu items** (3 per tier × 3 tiers).
4. **Lane 2 — 6 new ambient canvases** (2 per tier × 3 tiers) at `loc_diner_front`.
5. **Lane 3 — 3 new substitution rules** wired into Maya-solo diner dispatcher activities. (May require authoring 1–2 new Maya-solo dispatcher activities if existing ones don't cover diner surfaces.)
6. **Quest cards** — M1–M4 authored in `7_final_game.toml`, ordered after Frank F6 and before Ryan R1.
7. **Flag declared** — `marge_reliable_reached` added to the flag list in `0_systems_spec.toml` or wherever flag declarations live for the slice.
8. **Build clean** — no NEW warnings. The pre-existing scene_franks_bedroom_evening/_setter + scene_marge_diner_hub schedule-without-NPC-schedule warnings should both be resolved (the Marge one drops once §10.1 lands).
9. **Live-play smoke test** — full chain reachable:
   - Day 1: hire fires (M1 → terminal-ish for hire flow, M2 activates).
   - Worked shifts climb trust to 20 → M3 activates, T1 menu items + ambients + sub all surface live.
   - Worked shifts climb trust to 40 → M3 ready-frame shows, T2 menu items surface.
   - Use "Close out the diner with Marge" → `marge_reliable_reached` sets → M4 terminal frame.
10. **Voice audit** — every new prose line passes §2 voice spec. No flirtation, no double-meanings. A reviewer reads §2, then reads every new authored line, then signs off.

---

## §11 Cross-references

### Sibling and ancestor docs
- **Doc 30** — TLS Test Redesign PRD §8.2 (Marge minimum contract, sets the slice scope)
- **Doc 31** — Frank Arc Design Brief (template for this brief)
- **Doc 50** — Quest Card Shape Doctrine (R1–R6 applied throughout §7)
- **Doc 49** — Story Goals vs Sidebar Doctrine (anti-pattern cross-check)
- **Doc 24** — RTS Three Lanes (Lane 1/2/3 taxonomy in §4 and §5)
- **Doc 47** — Quests Page Unified Card Design (§7 quest cards conform to the unified shape)

### Memory entries
- `feedback_hint_narrative_no_time_or_location` — Maya-voice text discipline
- `quest_card_shape_doctrine` — Doc 50 memory
- `feedback_rts_objective_quest_doctrine` — Story Goals doctrine (anti-pattern reference)

### Live TLS reference
- **NPC def:** `7_final_game.toml:524–532`
- **Hire canvas:** `7_final_game.toml:1595–1626` (`canvas_marge_interview`)
- **Hub canvas:** `7_final_game.toml:7798–7837` (`scene_marge_diner_hub`)
- **Existing T0 shift:** `7_final_game.toml:8993+` (`scene_diner_t0_shift`)
- **Existing T1 shift:** `7_final_game.toml:9062+` (`scene_diner_t1_shift` — Maya-stat-gated)
- **Diner location:** `7_final_game.toml:749+` (`loc_diner_front`)
- **Hygiene-tip wire:** `7_final_game.toml:1499` (existing economic feedback loop)

### Implementation tooling
- Validator: `apps/projects/services/template_import.py` (will warn about missing NPC schedule until §10.1 lands)
- Generator: `apps/game_generation/twee_comprehensive/generators/v2.py` (renders pure-mechanic cards via `renderQuestsGoalBlock` — no engine change needed)

---

## Appendix A — Implementation phase ordering (when scheduled)

Suggested 3-pass order, mirroring Frank's slice authoring rhythm:

**Pass 1 — Schedule + T0 surfaces (~3 hours)**
- Add `[[npcs.schedules]]` for Marge.
- Author 3 T0 hub menu items + 2 T0 ambients + 1 T0 substitution.
- Author M1 + M2 quest cards.
- Build + smoke-test hire + T0 climbing card visibility.

**Pass 2 — T1 surfaces + Cookie kitchen access (~3 hours)**
- Author 3 T1 hub menu items + 2 T1 ambients + 1 T1 substitution.
- Wire `hub_marge_cookie_kitchen` as the Cookie-texture entry point.
- Author M3 quest card.
- Build + smoke-test trust climb to 20 + T1 unlock surface.

**Pass 3 — T2 surfaces + terminal + audit (~3 hours)**
- Author 3 T2 hub menu items + 2 T2 ambients + 1 T2 substitution.
- Add T2 group to `scene_marge_diner_hub`.
- Add `marge_reliable_reached` flag declaration.
- Wire `hub_marge_close_out` flag setter on first use at T2.
- Author M4 quest card.
- Build + full live-play smoke test.
- Voice audit pass per §10.10.

Total estimate: ~9 hours across 3 sessions. Comparable to a Frank slice phase.

---

## Appendix B — Pre-ship checklist (per Doc 50)

Before merging Marge implementation:

- [ ] **Mode declared.** All M2–M4 are pure-mechanic per §7. M1 is capstone (the hire).
- [ ] **R1 capstone coverage.** Hire canvas referenced by M1. No other priority-9 one-shot flag-setting canvases in scope.
- [ ] **R2 climbing-bullet.** M2 + M3 both have `goals` blocks.
- [ ] **R3 terminal placement.** M4 is the last card. No card requires a flag set after `marge_reliable_reached`.
- [ ] **R4 chain continuity.** Every "post-X" card has a sibling "pre-X" card pointing at X's setter.
- [ ] **R5 mechanic comment.** M2 and M3 carry `# unlocks:` comments matching §4.
- [ ] **R6 label voice.** "Marge trust" not `marge.trust`.
- [ ] **§5 narrative voice.** No place names, schedules, numbers, or jargon in card prose.
- [ ] **§9 anti-patterns.** No flirtation, no scripted-scene capstones post-hire, no Cookie standalone surfaces.
- [ ] **Doc-canvas alignment.** Lane content map in §5 matches the canvases that actually shipped.
