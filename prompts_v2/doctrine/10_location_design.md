# Doctrine 10 — Location Design + Reachability

**Sources:** Late Shifts build session (2026-05-29/30) — 7 location/reachability bugs that all shipped a GREEN build; TLS gold-standard location graph (`games/the_long_summer_test/toml_phases/1_metadata_and_locations.toml`); engine code `apps/game_generation/twee_comprehensive/generators/v2.py` + `apps/world/models.py`.
**Authority:** Doctrine. How to lay out a game's locations so navigation is geographically coherent AND every canvas is actually reachable in play.
**Purpose:** Close the single largest corpus gap. The validator checks *static* facts (a flag has a setter, a trait is declared) but NEVER checks *dynamic reachability* (can this canvas fire given location type, NPC schedule, time window, player presence). Six of the seven Late Shifts location bugs were invisible to the build — caught only by live-play. This file makes them authoring-time rules.

Cross-reference: `schema/02_toml_schema.md` §4 (location TOML fields); `schema/01_engine_capabilities.md` §5 (schedule/presence primitives); `doctrine/03_arc_shapes.md` (per-shape location footprint).

---

## §1 — The two things a location author must get right

1. **Geography** — the nav graph must read like a real place. Leaving the street should not drop you inside a private bedroom.
2. **Reachability** — every canvas attached to a location must be able to *fire* there. A canvas can be perfectly valid TOML and still be permanently dead.

Both are silent: a wrong location graph builds GREEN and only reveals itself in play. Treat this file as a pre-ship gate, not a style guide.

---

## §2 — The engine model (three independent fields — do not conflate them)

Per `apps/world/models.py` + `v2.py`:

| Field | What it controls | NOT |
|---|---|---|
| `entry_from` | **Navigation.** "You can reach me from here." The **"Leave X" link always points to `X.entry_from`** (`v2.py:17437`). Child destinations at a hub = every location whose `entry_from` points here (`models.py:301` `get_navigable_locations`), ordered by `navigation_order`. | not hierarchy |
| `parent` (`parent_location`) | **Structure only** — canvas inheritance + visual grouping. | NOT used for nav links. A location's `parent` and `entry_from` may differ. |
| `is_container` + `default_entry` | A **pure-nav wrapper**: auto-redirects into a child, holds no content of its own. | NOT a place that can host canvases (see §3). |

**The one rule that matters most:** the player walks the **`entry_from` chain**. `parent` is bookkeeping. A top-level location (no `entry_from`) emits **no "Leave" link** — it is a *root*, reached only via a walk-activity bridge (see §5). Nesting is supported up to 20 levels (`models.py:289`).

---

## §3 — `is_container` SWALLOWS attached canvases (Late Shifts bug B1)

**Rule: never attach a canvas (activity / ambient / capstone / portrait-hub) to an `is_container = true` location.**

Why: the passage generator branches on container status (`v2.py:8800`). A container passage emits **only** child-navigation — it never calls `getStoryCanvasRedirect` (auto-fire capstones), `renderNpcPortraits` (NPC hubs), or `renderSoloActivities` (solo activities). Any canvas whose `trigger.location` is a container is **silently dead**, and the container double-renders its nav (text links + card grid).

In Late Shifts both hubs were containers with the walk-home activity + the entire Pam arc + Cole's walk attached → town-trap soft-lock + a dead arc, all GREEN.

**Two correct patterns:**

- **A — Standing hub (preferred for game-specific hubs):** a NON-container location that carries `navigation_order` for its children AND hosts canvases. Children reach it via `entry_from`; `isCanvasValid`/`get_navigable_locations` resolve children by `entry_from` independent of container status. This is what Late Shifts uses post-fix.
- **B — Thin wrapper + arrival child (TLS gold standard):** an `is_container` wrapper with `default_entry` → auto-redirect to a NON-container arrival child that holds the canvases. TLS: `loc_property` (container) → `loc_front_porch` (arrival, standing) → `loc_hallway` (interior hub, standing). The container is pure routing; all content lives on the standing children.

Pick A by default. Use B only when you want the wrapper-level auto-redirect.

---

## §4 — Geographic layering (Late Shifts bug C1)

**Rule: a private dwelling, the shared building it sits in, and the town outside are SEPARATE locations. Never collapse "my apartment" and "the building corridor" into one hub.**

The Late Shifts original had one `loc_apartment_hallway` playing both Maya's private foyer AND the building's shared corridor — so the street opened into the bedroom hallway and a neighbor spawned beside the bedrooms. The fix layered it:

```
rooms (bedroom, kitchen, bath, laundry…)
  → loc_mayas_apartment      PRIVATE unit hub (only household members)
  → loc_building_hallway     SHARED corridor (neighbors, mailboxes, stairwell-ready)
  → loc_building_front       EXTERIOR root (top-level; the steps)
  → [activity_walk_to_town] → loc_main_street   TOWN root (top-level)
     → diner / park / shops…
```

Each "Leave" crosses one real threshold (room → unit → corridor → street → town). Authoring consequences:

- **Household NPCs** (live-in family) belong inside the private unit. **Neighbors / witnesses** belong in the shared building layer (corridor, front steps, laundry IF shared) — never inside the private unit.
- **Two top-level roots** (home-exterior + town), each with NO `entry_from`, **bridged by walk-activity canvases** (`activity_walk_to_town` / `activity_walk_home`), NOT by an `entry_from` link. (TLS + Late Shifts both do this.)
- **Laundry placement is a per-game call:** in the private unit = a chore room, no neighbor crossings; in the shared building = a neighbor-encounter surface. Decide based on whether you want it to host neighbor scenes.
- **`navigation_order` ↔ `entry_from` coupling (bug A5):** a slug listed in a location's `navigation_order` MUST have its `entry_from` pointing back at that location, or the validator rejects it ("not a destination"). Keep the two in sync.

Don't over-build: one floor / one unit is right for a small cast. The chain extends trivially for more floors (`loc_building_stairwell` off the corridor → `loc_building_hallway_2` …) — note it in a comment, don't author it speculatively.

---

## §5 — The Reachability Triad (Late Shifts bugs B2 / B3 / B4)

**A canvas fires only when all three overlap:**

> **(1) the NPC is present** (per `[[npcs.schedules]]`, schedule-only + fail-closed via `getNpcLocation`)
> **∩ (2) the canvas's own time-window** (`[[canvases.trigger.schedules]]`)
> **∩ (3) the player is actually there and awake** (not asleep, not at work — where the loop puts them).

If the intersection is empty, the canvas is dead and the build won't tell you. Three distinct failure modes, all seen in Late Shifts:

### §5.1 — `requires_npc` location ∉ that NPC's schedule (B2)
A canvas with `requires_npc = npc_X` only fires when `getNpcLocation(X) == its location`. If the canvas's location is not one of X's `[[npcs.schedules]]` entries, it **never** fires. Late Shifts: `scene_hank_first_contact_kitchen` + 3 Hank subs sat at `loc_diner_back`, but Hank was scheduled front-of-house + office only → the sole setter of `hank_first_contact` was unreachable → Hank's whole Stage 2→5 chain dead, the office permanently locked.
**Fix (faithful):** schedule the NPC into the location (give Hank a kitchen-check window) rather than relocating intimate scenes to a public floor.
**Fix (walk-ins where the NPC genuinely can't be scheduled there):** DROP `requires_npc` and time-gate with the substitution target's OWN `[[canvases.trigger.schedules]]` — `isCanvasValid` (`v2.py:4005`) enforces a sub target's own schedule + conditions. The prose ("he'd knocked, she hadn't heard") carries the implied presence.

### §5.2 — Portrait hub needs the NPC schedule-present (B3) — distinct from §5.1
`renderNpcPortraits` (`v2.py:4295`) has its OWN presence gate (`getNpcLocation(npc) === locationId`), independent of `requires_npc`. A Lane-1 portrait hub (`npc =` set) renders **no portrait** — i.e. is unclickable / unreachable — if that NPC isn't scheduled at the hub's location, even with no `requires_npc`. Late Shifts: Cole's new apartment hub showed nothing until Cole was given a `loc_cole_apartment` schedule window. (Auto-fire capstones with no `npc=` are NOT portrait-gated, so they fired regardless — only the manual portrait HUB needed the schedule.)

### §5.3 — Timing dead-zone (B4)
Even when NPC + location agree, the player must be there *and awake*. Late Shifts Pam: all her scenes sat at a hallway window of 09:00–11:00, but Maya **sleeps 07:00–14:00** off the night shift → empty intersection, confrontation could never fire. Fix: anchor the canvas to where the player *actually crosses the NPC* (Pam → the front steps in the evening, the mandatory pre-shift waypoint). Mind cross-midnight windows when you check overlap (22:00–07:00 wraps).

**Authoring rule for every NPC ambient/capstone:** anchor it where the player *actually crosses the NPC during the daily loop* — not where the fiction first imagines them. Then sanity-check the triad by hand.

---

## §6 — Per-arc-shape location footprint (Late Shifts bug B6)

- **Family/ambient + slow-burn family:** live-in; canvases attach to shared-household standing locations the player already frequents.
- **Peer/dating (Ryan-shape):** needs an **ongoing Stage-4 repeatable hub at the partner's location**, not only a first-night capstone. Late Shifts shipped Cole with ONLY the one-shot `scene_cole_first_night` and no repeatable hub — so once consummated, the arc had no surface and pregnancy/ongoing content had nowhere to attach. The partner's home is access-gated on the relationship flag (e.g. `cole_date_done`), and the ongoing hub is gated on the consummation flag (`cole_first_night_done`) at a priority below the first-night capstone so the capstone fires first, then the hub takes over. The hub NPC must be schedule-present there (§5.2).
- **Service:** workplace location only; no home surface.
- **Antagonist/witness:** shared/public space where the player crosses them (steps, corridor) — NOT the player's private space.

Cross-ref `doctrine/03_arc_shapes.md` §5 for the peer/dating distribution (now including the ongoing hub).

---

## §7 — Pre-ship location self-audit (run before delivery)

- [ ] No canvas's `trigger.location` is an `is_container = true` location (§3).
- [ ] Geography layered: private-unit ≠ shared-building ≠ town; two top-level roots bridged by walk activities (§4).
- [ ] Every `navigation_order` slug has `entry_from` pointing back here (§4).
- [ ] Every `requires_npc` canvas: its location ∈ that NPC's `[[npcs.schedules]]` (§5.1).
- [ ] Every portrait hub (`npc =` set): that NPC is schedule-present at the hub's location (§5.2).
- [ ] Every NPC ambient/capstone passes the triad: NPC-schedule ∩ canvas-window ∩ player-likely-present-and-awake is non-empty, accounting for sleep/work/cross-midnight (§5.3).
- [ ] Every peer/dating NPC has an ongoing Stage-4 hub, not just a first-night capstone (§6).
- [ ] Household NPCs are inside the private unit; neighbors/witnesses are in shared/public space, never the private unit (§4).

If any fail: fix BEFORE delivery. None of these are caught by the build validator today (see `PREVENTION_LINTER_SPEC.md` for the proposed engine-side catch).

---

## §8 — Cross-references

- `schema/02_toml_schema.md` §4 — `[[locations]]` field reference (`entry_from`, `parent`, `default_entry`, `is_container`, `navigation_order`).
- `schema/01_engine_capabilities.md` §5 — `getNpcLocation`, schedule presence (schedule-only, fail-closed).
- `doctrine/02_three_lanes_plus_capstone.md` — lane mechanisms (what attaches where).
- `doctrine/03_arc_shapes.md` §5 — peer/dating ongoing-hub footprint.
- `stages/01_game_book_prompt.md` §4 Step 3/4 — locations + schedules authoring.
- `stages/02_toml_generation_prompt.md` §10/§11 — anti-patterns + quality gate.
- `PREVENTION_LINTER_SPEC.md` — the build-time reachability checks that would catch §3 + §5 automatically.

---

**End of file.** A location graph that passes §7 is geographically coherent AND fully reachable. The build won't verify either for you — this checklist is the gate.
