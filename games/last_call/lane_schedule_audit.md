# Last Call — Lane / Schedule Coverage Audit

*Recorded 2026-06-04 (turn 12). A snapshot audit of what's built vs the doctrine + the
RTS scene catalog (`prompts_v2/reference/02_rts_scene_catalog.md`). Findings, not intent —
the design intent lives in `design_book.md`. Use this to prioritize remaining work.*

State at audit: 8 beats validated (0001/0002/0015/0009/0005/0006/0004/0003). 4 NPCs fully
on-ramped (Sal, Dee, Marcus, Rosa); Collector presence built. 21 canvases total.

---

## §1 — Per-NPC lane coverage (canvases actually authored)

Legend: Meet = one-time intro · L1 = hub menus · L2 = location-entry random ambients ·
L3 = walk-ins inside a solo activity · L4 = capstones.

| NPC | shape | Meet | L1 hubs | L2 | L3 | L4 | Budget remaining |
|---|---|---|---|---|---|---|---|
| Sal | peer/dating | 1 | 1 hub (`sal_hub`, 17–02) | 1 (`bar_ambient`) | 0 *(empty, honest)* | 1 of 4 (meet = capstone 1) | +3 capstones, after-close rungs |
| Dee | peer/dating | 1 | **2** (`dee_hub` depot + `dee_cellar_hub`) | 1 (`dee_ambient`) | 0 *(empty)* | 0 of 3 | all 3 capstones |
| Marcus | peer/dating | 1 | 1 (`marcus_hub`) | 1 (`marcus_ambient`) | 0 *(empty)* | 0 of 3 | all 3 capstones |
| Rosa | service | 1 | 1 (`rosa_hub`) | 0 *(empty, honest)* | 0 *(empty)* | **1 of 1** ✅ | none — arc complete |
| Collector | antagonist | — | **0** (rent modal stands in) | 2 (`collector_pressure`, `collector_word`) | 0 own | 2 (`shark_summons` + `shark_place`) | +1 L2, the final reckoning |

Shared / not NPC-bound: `work_shift` (solo L3 host), `work_walkin` (generic L3 walk-in),
`first_night` (boot), `sleep` (day-cycle router).

**Empty cells that are CORRECT (honest, not gaps):** peer/dating → no L3; service Rosa →
no L2/L3. Filling these would be the failure, not the omission.

---

## §2 — Schedule findings (verified against `1_metadata_and_locations.toml`; weekday index 0=Monday, confirmed v2.py:2784)

**F1 — Dee cellar days are wrong. [RESOLVED turn 13 → `[1,4]` Tue/Fri in both metadata + hub.]**
Cellar drop is `weekdays=[2,5]` = **Wed + Sat**, but the
design book intends **Tue/Fri** (`[1,4]`) and a TOML comment says "Sat cellar drop." The
cellar hub (`dee_cellar_hub`) mirrors `[2,5]`, so hub-and-schedule agree with *each other*
but both disagree with intent. **Fix:** set both the metadata cellar row and the hub schedule
to `[1,4]` (or whatever 2 days are intended) — keep them in lockstep.

**F2 — Dee weekend gap. [RESOLVED turn 13 → added `loc_dee_place` `[5,6]` 00:00–23:59 weekend row.]**
Dee's offscreen "away" block is `[0,1,2,3,4]` (Mon–Fri only). On
**Sunday** he has no row at all; Saturday only the (mis-dated) cellar drop. The Schedule page
shows blanks for him on weekends. **Fix:** extend his offscreen `loc_dee_place` block to cover
Sat/Sun (or add a weekend away row) so his day is complete.

**F3 — Sal: 2 reachable rows, 1 hub (presence OK, exposure under-used). [RESOLVED turn 15 →
split into `canvas_sal_hub` (service 17–22) + `canvas_sal_afterhours_hub` (private 22–02) + the
first-kiss capstone in beat_0010.]** Sal has rows
`loc_bar 17–22` (service) + `loc_bar 22–02` (after close) — contiguous, both covered by the
single `sal_hub` (17–02). Presence floor satisfied. BUT the two windows are meant to be
*different exposure tiers* (service = public/talk+flirt; after close = private/kiss+upstairs).
One hub currently treats them the same. **Fix:** in `beat_0010`, split into a service hub +
a separate **after-close hub** (22:00–02:00) carrying the private rungs (the doctrine
"period-split hub" pattern). Folded into beat_0010.

**F4 — Collector: no Lane 1 hub (intentional, documented).** Only `loc_bar Mon 18–20`, no away
block. The engine rent modal + 2 L2 ambients carry his presence. Antagonist exception per the
brief; defensible. Optional: a light collection-night hub for strict D72-R6 compliance.

Clean: Sal (rows correct), Marcus (1 reachable + offscreen), Rosa (1 reachable + offscreen).

---

## §3 — The real structural gap vs RTS: Lane 3 + solo-activity count

Grounded in `reference/02_rts_scene_catalog.md` (40-surface audit of 4 RTS NPCs):

- **RTS's family NPC (Brother): Lane 3 is the LARGEST bucket — 47% (7 of 15 surfaces).** The 7
  walk-ins piggyback on **4 solo activities** (Study ×3, Play Videogame ×2, Shower ×1, Wash
  Dishes ×1). The catalog: *"RTS's primary mechanism for the NPC being everywhere in your
  day-to-day without overstuffing menus."*
- **Last Call has ONE solo activity (`work_shift`) with ONE generic walk-in.** The thinnest
  possible version of RTS's richest lane.
- **Why:** every LC NPC is shaped peer/dating, service, or antagonist — the three shapes our
  budget gives **L3 = 0**. No family/ambient or slow-burn NPC exists, so the budget said build
  ~none, and we did.
- **Caveat the RTS data exposes:** even RTS's *peer* NPC (Marcus) has activity-triggered
  content — `StudyWithMarcus`, `MarcusClassSex`, `MarcusBathroomEncounter` — delivered as
  Pattern E *events* at locations (qualify → full scene) rather than random walk-ins inside the
  player's chores. So "peer = zero activity content" is stricter than RTS actually plays.

**Implication / options to close it:**
1. Add solo activities the player does at the bar/home (e.g. *clean up after close*, *restock
   the cellar*, *count the till*, a *shower* upstairs). Each becomes a Lane 3 host.
2. Then either (a) reclassify whoever should be Lane-3-active so NPC walk-ins fire inside those
   activities, or (b) give peers location *events* the RTS-Marcus way (Pattern E at a location
   + time, not a hub menu).

**Lane 2 is NOT the gap.** RTS Lane 2 is a minority even for family (Brother 20%); peer ≈ 1.
Our counts (peer 1 each, antagonist 2, service 0) match the per-shape budget and are roughly
RTS-proportional. Leave Lane 2 as is.

---

## §4 — Prioritized backlog (recommendation)

| # | Item | Size | Why |
|---|---|---|---|
| P1 | ✅ **DONE (turn 13)** — Dee schedule (F1 cellar days `[1,4]` + F2 weekend away) | tiny | Real bug; fixed in metadata + hub |
| P2 | ✅ **DONE (turn 15)** — beat_0010 — Sal service/after-close hub split (F3) + first-kiss capstone. Capstones #3 (upstairs)/#4 (backbone) → beat_0017/0018. | medium | Unblocked Sal's private ladder via the period-split pattern |
| P3 | ✅ **DONE (turn 14, scope "Utility + antagonist")** — beat_0016 — 3 utility activities (shower fixes the hygiene hole + clean-up + restock) + Collector floor-walk Lane 3 cross-appearance (pre/post-seizure). Peers stay L3=0 by design (doctrine). | medium (scoped) | Fixed the hygiene hole + added daily texture + the one doctrine-sound NPC-in-activity piece |
| P4 | **Escalation beats 0008 (Marcus) / 0011 (Dee)** | medium each | Build the dating/leverage ladders on the hubs that now exist |
| P5 | **Collector light hub (F4) + final reckoning (0013)** | small / medium | Optional strictness + the antagonist payoff |
| — | Remaining planned: 0007 dress-for-tips, 0012 collision, 0014 endgame | — | Later |

**ENI's read:** P1 now (trivial correctness), then **P3 before P4** — establish the solo-activity
/ Lane 3 substrate first so the escalation beats can hook walk-ins into it instead of being
retrofitted later. P2 (beat_0010) slots naturally alongside P3 since both touch the bar's
activity surfaces.
