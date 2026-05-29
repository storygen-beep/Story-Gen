# Doc 55 — Honest Location-Nav Indicators

**Status** — Shipped 2026-05-25, live-verified GREEN.
**Author** — ENI (with LO).
**Purpose** — Codify the three-rule doctrine that landed this session (🔓 deleted, NEW capstone-only, NPC presence schedule-only) and record the engine architecture + verification evidence behind it.
**Extends** — Doc 24 §10 (three lanes). Composes with the `[[npcs.schedules]]` primitive (Phase B, 2026-05-14).
**Sibling docs** — Doc 50 (Quest Card Shape, capstone Frame 2 ↔ NEW badge surface), Doc 54 (Marge Redesign Session Lessons, Appendix A pre-authoring checklist gets a schedule item).
**Source artifacts** — `apps/game_generation/twee_comprehensive/generators/v2.py` (edits this session), `game_explorations/tls-nav-indicators-verify/` (live-play verification artifacts).

---

## §1 The problem

User report (May 23 entry in `games/under_one_roof/issue.md` line 459):

> *location sometimes shows lock / new / npc presence or more if there are anything else, but on entering location we found nothing.*

Three indicators on each location nav card — `NEW`, `🔓`, NPC portrait — over-promised content. Player saw a face on the Yard card, walked in, found an empty hub. Saw `NEW` on the Kitchen, walked in, the next passage delivered a generic Maya-solo activity, not a story event. The 🔓 indicator was the noisiest of the three, lighting up at locations whose only "unlocked" surfaces were Lane 3 substitutions the player couldn't directly enter.

The location-screen renderer was honest about what walking in delivers; the nav-card badges were not. The two layers ran on different selection logic and drifted apart.

---

## §2 Root-cause audit

The 2026-05-07 patch fixed the `NEW` badge by routing it through three new pure helpers (`selectAutoFireCanvasForLocation`, `selectNpcPortraitCanvasesForLocation`, `selectSoloActivityCanvasesForLocation`) that already applied the four filters the renderer cared about. But Badges 2 and 3 stayed on the legacy `selectCanvasByPriority` path, which is missing four filters and is non-idempotent.

### §2.1 Filter divergence (Badges 2 + 3)

| Filter | Renderer applies? | `selectCanvasByPriority` applies? | Symptom when missing |
|---|---|---|---|
| `substitutionOnly` | yes | **no** | Lane 3 sub canvases trigger badges but are unreachable from location screen |
| Cost-affordability | yes (routes to blocked bucket) | **no** | Cost-blocked canvases trigger badges → click in, find greyed-out gate |
| Schedule-presence (`getNpcLocation`) | yes (NPC path) | **no** | NPC's declared schedule places them elsewhere; portrait still appears on this card |
| Idempotence | n/a (rendered with dice) | **rolls dice per call** | Random-mode canvases flicker between visits — badge promise changes per nav refresh |

### §2.2 Coverage gap on Badge 1

Even Badge 1 (`NEW`) — already routed through the pure helpers — was missing the renderer's downstream schedule-presence filter (`v2.py:4365–4374`). So `NEW` could fire on a location whose only candidate canvas was an NPC scheduled elsewhere; the renderer would then drop that NPC from the portrait grid, leaving the player to walk into a location where `NEW` was promised but no NPC was visible to click.

---

## §3 The three changes (the doctrine layer)

### §3.1 🔓 unlocked-choices indicator → deleted everywhere

The 🔓 chip was meant to signal "this canvas has an unlocked-but-unvisited conditional choice". Two problems:

1. **Structurally entangled with `selectCanvasByPriority`.** The location-level wrapper `setup.locationHasNewUnlockedChoices` inherited all four divergences from the legacy path. Fixing it cleanly required routing it through the same pure helpers — at which point the per-portrait `!` chip on the location screen was the more honest surface anyway (sits directly on the click target).

2. **The click target's own affordances communicate the same information.** When the player visits the location and clicks the NPC portrait or solo activity, the canvas renders with the unlocked choice present. The 🔓 badge was a list-level promise that became redundant once you entered. It also competed semantically with `NEW` — both implied "look here, something is queued" without the player being able to tell which.

Deleted in this session: location-level wrapper `setup.locationHasNewUnlockedChoices`, per-canvas helper `setup.canvasHasNewUnlockedChoices`, four nav-card emission sites, per-portrait `!` chip emission in `renderNpcPortraits`, and all supporting CSS (`.nav-unlocked`, `.nav-unlocked-badge`, `.npc-portrait-unlocked`, `.npc-badge-unlocked`).

Kept: `setup.isChoiceVisited` / `setup.markChoiceVisited` (may have non-badge call sites; cheap to leave).

### §3.2 NEW badge → capstone-only (non-repeatable auto-fire)

`NEW` now fires on a nav card iff `setup.selectAutoFireCanvasForLocation(locationId)` returns a canvas that has never been triggered. That helper already filters `!isRepeatable && triggerMode != "random" && !substitutionOnly && isCanvasValid` — exactly the capstone shape.

Per-portrait `NEW` chip (`.npc-badge-new` + `.npc-portrait-new` border) and per-solo `NEW` class (`.solo-activity-new`) were deleted in the same pass. Reasoning: those click targets are always repeatable activities — under the capstone-only doctrine, `NEW` can never legitimately fire on them.

The two semantic axes are now cleanly separated:

| Surface | What `NEW` means |
|---|---|
| Nav card | "A one-time story event is waiting for you at this door." |
| (Per-portrait / per-solo) | Removed. Repeatable click targets carry no `NEW` signal. |

### §3.3 NPC presence → schedule-only via `[[npcs.schedules]]`

`setup.getNpcsWithCanvasesAtLocation` was rewritten to intake from `selectNpcPortraitCanvasesForLocation` (the renderer's affordable+valid pick set) and gate hard on:
1. NPC has declared `[[npcs.schedules]]` entries (`setup.npcSchedules[slug]` present), AND
2. `setup.getNpcLocation(slug)` returns this location at the current time.

No canvas-derived fallback. NPCs without declared schedules are suppressed entirely.

The renderer's pre-existing schedule filter at `v2.py:4365–4374` was flipped from fail-open (`return true` for NPCs without declared schedules) to fail-closed (`return false`). Nav-card badge and renderer now make identical promises.

---

## §4 Engine architecture — pure-helper source of truth

### §4.1 The three pure helpers

| Helper | Path | Filters applied | File |
|---|---|---|---|
| `selectAutoFireCanvasForLocation` | Path 1 — non-repeatable auto-fire on entry | `!isRepeatable`, non-random, `!substitutionOnly`, `isCanvasValid` | `v2.py:3839` |
| `selectNpcPortraitCanvasesForLocation` | Path 2 — NPC portrait click | `isRepeatable`, non-random, `!substitutionOnly`, `npcId`, `isCanvasValid`, daily cap, cost-affordable | `v2.py:3868` |
| `selectSoloActivityCanvasesForLocation` | Path 3 — solo activity click | `isRepeatable`, non-random, `!substitutionOnly`, `!npcId`, `isCanvasValid`, daily cap, cost-affordable | `v2.py:3900` |

These are pure — no side effects, no marking, no RNG. They're the answer to: "what content will the player encounter when they walk in?" Both the renderer and the nav-card badge are expected to consult them; anything that doesn't is by definition diverging.

### §4.2 `getNpcLocation` — the presence-truth function

`setup.getNpcLocation(slug)` at `v2.py:2898` is schedule-first:

- **Path 1** — walks declared `setup.npcSchedules[slug]` entries. First match wins. Returns `null` if a declared schedule exists but no current entry matches (NPC is explicitly "gone" right now).
- **Path 2** — canvas-derived fallback. Only reached for NPCs without declared schedules.

The schedule-only badge bypasses Path 2: it tests `if (!schedules[slug]) continue;` *before* calling `getNpcLocation`. So `getNpcLocation` never returns a Path-2 answer to the badge, and an unschedule-d NPC is suppressed even if their canvases imply a location.

This is intentional. Path 2 stays in the engine for any non-badge caller that still wants soft presence, but the indicator system treats it as not-a-truth-source.

### §4.3 The lockstep rule

Nav-card badge logic and location-screen renderer logic must call the same pure helpers. Any new indicator added later that re-implements selection from scratch will diverge — the four-divergence audit in §2 happened precisely because two badges were built on a legacy path that the renderer had since superseded.

Concretely:
- `getNpcsWithCanvasesAtLocation` (nav badge) calls `selectNpcPortraitCanvasesForLocation` + `getNpcLocation`.
- `renderNpcPortraits` (renderer) calls `selectNpcPortraitCanvasesForLocation` + the same `getNpcLocation` filter.

Both surfaces produce identical NPC sets for any (location, time, state) tuple.

---

## §5 Schedule-only NPC presence — the editorial lever

### §5.1 The rule

NPCs without `[[npcs.schedules]]` entries declared in the TOML do not appear in:
- nav-card NPC portraits (any location)
- location-screen portrait grids (any location)

NPCs with declared schedules appear iff `getNpcLocation(slug)` resolves to the current location at the current time.

### §5.2 Why no canvas-derived fallback

The fallback ("show the NPC at any location where a canvas references them") over-fires. A typical TLS NPC has canvases distributed across 3–4 locations (kitchen, living room, yard, bedroom). Under the fallback, the NPC's portrait would appear on all 4 nav cards simultaneously, regardless of whether they're actually there. Walking into 3 of the 4 yields a hub with no NPC interaction available — the symptom we're closing.

Schedule-only forces the author to commit to a single location-per-time-window answer. The badge and the runtime answer the same question with the same data.

### §5.3 The forcing function

Per option (b) shipped this session: missing schedules visibly suppress NPC portraits everywhere until authored. This is the intended pressure on the next NPC redesign passes — see §9 for the punch-list.

### §5.4 How an author declares a schedule

Frank's 7-entry schedule (`games/the_long_summer_test/toml_phases/7_final_game.toml:414–461`) is the gold-standard template:

```toml
# Bedroom asleep, full week, overnight
[[npcs.schedules]]
location = "loc_franks_bedroom"
weekdays = [0, 1, 2, 3, 4, 5, 6]
start_time = "23:00"
end_time = "06:00"
activity = "asleep"

# Kitchen morning coffee, full week
[[npcs.schedules]]
location = "loc_kitchen"
weekdays = [0, 1, 2, 3, 4, 5, 6]
start_time = "05:30"
end_time = "09:00"
activity = "morning coffee"

# ... 5 more entries covering yard 14:00–17:00, kitchen dinner prep,
# living room evening, bedroom winding down, weekend hallway pass.
```

Properties to know:
- `weekdays` — array of day indices (0=Monday). Empty = all days.
- `start_time` / `end_time` — `HH:MM` strings, 24-hour. Overnight wraps (`23:00`–`06:00`) handled by the runtime.
- `activity` — human-readable label, surfaces in `getNpcLocation` return for any caller that wants to display "Frank is at the kitchen (morning coffee)".
- Non-overlapping by design. First-match-wins, so overlap silently picks whichever entry comes first in the TOML.

Single-entry schedules are fine for service NPCs (Marge: diner front 09:00–22:00) or single-window NPCs (Diana current state: bedroom 21:30–23:30). Just understand the time windows where the NPC visibly disappears from nav cards.

---

## §6 Capstone-only NEW doctrine

### §6.1 The rule

`NEW` appears on a location nav card iff `selectAutoFireCanvasForLocation(locationId)` returns a canvas with `isCanvasNew === true` (never triggered). That helper filters to non-repeatable, non-random, non-substitution, currently-valid canvases — the capstone shape.

### §6.2 Why not on repeatables

Repeatable click targets always carry their own affordance — the NPC portrait or the solo button — that the player sees when they enter the location. Slapping a `NEW` chip on the click target conflates two questions:

1. "Has this *tier* unlocked since I last tried this activity?" — repeatable-tier progression
2. "Is a one-time *story event* queued at this location?" — non-repeatable auto-fire

These are different player-facing signals. Bundling them under one badge produces the symptom the user reported: a `NEW` on the Kitchen card that turned out to be a tier-2 repeatable Maya activity, not the dramatic Diana scene they expected.

The capstone-only restriction frees `NEW` to mean exactly one thing: "a one-time story event is sitting at this door."

### §6.3 Composition with Doc 50 (Quest Card Shape)

A queued auto-fire capstone is, by definition, the slice's next capstone scene. The capstone quest card (Doc 50 §2 Frame 2 — `🔓 Ready 📍 location 🕒 schedule`) and the nav-card `NEW` badge are two surfaces of the same fact. They appear together; they disappear together (auto-fire triggers, capstone consumes itself, both surfaces flip).

---

## §7 Implementation log

### §7.1 Function map (before → after)

| Function | Before this session | After this session |
|---|---|---|
| `setup.locationHasNewCanvases` | 3 paths (auto-fire + NPC + solo) | Path 1 only (`selectAutoFireCanvasForLocation` + `isCanvasNew`) |
| `setup.locationHasNewUnlockedChoices` | existed, called `selectCanvasByPriority` | DELETED |
| `setup.canvasHasNewUnlockedChoices` | existed, used by location wrapper + per-portrait check | DELETED |
| `setup.getNpcsWithCanvasesAtLocation` | called `selectCanvasByPriority`, returned all NPCs with valid canvases | rewritten to `selectNpcPortraitCanvasesForLocation` + `setup.npcSchedules` gate + `getNpcLocation` check |
| `renderNpcPortraits` schedule filter | fail-open for undeclared schedules (`return true`) | fail-closed (`return false`) |
| `renderNpcPortraits` per-portrait NEW + 🔓 emissions | `isNew` / `hasUnlocked` calcs + `indicatorClass` branches + span emissions | DELETED |
| `renderSoloActivities` per-solo NEW class | `isNew` calc + `solo-activity-new` class | DELETED |
| Nav-card 🔓 emissions | 4 sites in `_generate_hierarchical_navigation` + fallback nav | DELETED |
| CSS rules | `.nav-unlocked`, `.nav-unlocked-badge`, `.npc-portrait-new`, `.npc-portrait-unlocked`, `.npc-badge-new`, `.npc-badge-unlocked`, `.solo-activity-new` | DELETED |

### §7.2 Files modified

- `apps/game_generation/twee_comprehensive/generators/v2.py` — only file modified.
- `v1.py` is frozen per file header — not touched.
- No TOML changes. No new migrations. No new tests added (no dedicated tests existed for these functions pre-session per Phase 1 audit).

### §7.3 Build artifact

Built to canonical TLS test output with `--dev --debug` flags. Build clean — only pre-existing warnings (Frank's bedroom canvas overlap, trait-extract type errors, `thrift_store.jpg` missing asset). No new warnings introduced.

### §7.4 Pytest regression

`pytest apps/game_generation/` — 5 failures, all confirmed pre-existing via `git stash` comparison. Zero regressions from this PR.

---

## §8 Live-play verification evidence

Captured 2026-05-25 in `game_explorations/tls-nav-indicators-verify/`. Session resumable; notes preserved.

### §8.1 Removed-pattern grep on rendered HTML

Eight patterns greppeed across four live location passages (Home hub at 06:00, Home hub at 14:30, Back Porch, Back Yard, Kitchen):

| Pattern | Hits |
|---|---|
| `nav-unlocked` | 0 |
| `npc-badge-unlocked` | 0 |
| `npc-portrait-unlocked` | 0 |
| `npc-badge-new` | 0 |
| `npc-portrait-new` | 0 |
| `solo-activity-new` | 0 |
| `locationHasNewUnlockedChoices` | 0 |
| `canvasHasNewUnlockedChoices` | 0 |

Clean. None of the removed surfaces survive in the runtime HTML.

### §8.2 `setup.npcSchedules` keys at runtime

```js
Object.keys(setup.npcSchedules) === ["npc_frank", "npc_diana", "npc_marge"]
```

Three keys. Matches the three NPCs with `[[npcs.schedules]]` declared in `7_final_game.toml`. No others.

### §8.3 `getNpcLocation` at Day 1 06:00 Monday

| NPC | Return | Why |
|---|---|---|
| `npc_frank` | `{location: <kitchen UUID>, activity: "morning coffee"}` | 05:30–09:00 slot active |
| `npc_diana` | `null` | Only declared slot is 21:30–23:30; current time outside |
| `npc_marge` | `null` | Diner schedule starts 09:00; current time before window |
| `npc_ryan` | `null` | No `[[npcs.schedules]]` declared |
| `npc_jake` | `null` | No `[[npcs.schedules]]` declared |
| `npc_cookie` | `null` | No `[[npcs.schedules]]` declared |

### §8.4 Schedule transition test

Time bumped from 06:00 → 14:30 via dev eval. State observed at Home hub:

| Location card | Indicators at 06:00 | Indicators at 14:30 |
|---|---|---|
| Kitchen | Frank portrait | (empty) |
| Back Porch | (empty) | (empty) |
| Frank's Bedroom | (empty) | (empty) |
| (all other Home sub-cards) | (empty) | (empty) |

Walked into Back Porch at 14:30 — Back Yard sub-card shows Frank's portrait. Walked into Back Yard — `location-npcs` portrait grid contains `[('Frank', '')]`. Class string is empty (no stale `npc-portrait-new`, `npc-portrait-unlocked`, etc. fragments).

Renderer parity verified end-to-end: Frank's portrait flips with his schedule, and both surfaces (nav badge + portrait grid) point at the same location at the same time.

### §8.5 Capstone NEW audit

At Day 1 06:00 Mon, looped through all 12 indexed locations:

- **Exactly 1 location** has `locationHasNewCanvases === true`: the diner front (UUID `5a96…`).
- That location's `selectAutoFireCanvasForLocation` pick: `Marge — interview`, `isRepeatable: false`.
- All 11 other locations: no `NEW` (either no capstone queued, or capstone already visited in earlier session).

Capstone-only doctrine confirmed: `NEW` fires for the single non-repeatable story event queued in the slice, not for any of the dozens of repeatable activities scattered across locations.

---

## §9 Slice impact + punch-list (option-b forcing function)

The visible-gap forcing function shipped this session: NPCs without declared `[[npcs.schedules]]` are suppressed from nav cards and portrait grids until their schedule is authored.

| NPC | Schedule status | Visible effect now | Action item for next NPC pass |
|---|---|---|---|
| Frank | 7 entries, full-day coverage | Truthful nav presence (verified §8.4) | (done) |
| Marge | 1 entry, Mon–Sat 09:00–22:00 diner front | Truthful — portrait shows on diner during shift | (done) |
| Diana | 1 entry, 21:30–23:30 her bedroom | Kitchen morning + livingroom evening presence vanishes from nav AND portrait grid | Author kitchen morning + livingroom evening schedule entries to restore her day-time presence |
| Ryan | 0 entries | Portrait absent from all nav cards + Back Yard portrait grid (despite yard description naming his work area) | Author full-day schedule per future Ryan redesign brief |
| Jake | 0 entries | Portrait absent from all nav cards (despite his keyboard audible in Home description) | Author full-day schedule per future Jake redesign brief (Doc 52 reserved) |
| Cookie | 0 entries | Portrait absent from diner kitchen card during her shift | Author diner shift schedule per future Cookie redesign brief |
| Unknown | 0 (intentional) | n/a — phone-only contact, no location presence by design | — |

The Diana entry is the only "regression" in literal terms — her single-entry schedule was previously enough to surface her at her bedroom but not her morning/evening kitchen and livingroom appearances (which were canvas-driven, now suppressed). Author two extra entries to bring those back; not blocking the doctrine ship.

---

## §10 Authoring guidance for the next NPC redesign brief

Three rules to apply at the start of any future NPC redesign:

1. **`[[npcs.schedules]]` is load-bearing, not decorative.** Treat it as a required field in the NPC TOML block. Without it, the NPC has no nav-card or portrait-grid presence regardless of how many canvases reference them.

2. **Use Frank's 7-entry schedule (TOML:414–461) as the structural template.** Non-overlapping entries, full-day coverage, human-readable `activity` field for each entry. Single-entry schedules are valid for service NPCs (Marge) — just understand the time-of-day windows where the NPC visibly disappears.

3. **Canvas-derived presence is no longer a soft fallback.** Don't author canvases at a location expecting the NPC's portrait to surface automatically. Wire the schedule entry that puts the NPC at that location at that time, then author the canvases.

The pre-authoring checklist in Doc 54 Appendix A should now include a step: *"Confirm `[[npcs.schedules]]` declared for this NPC before authoring any location-resident canvases."*

---

## §11 Cross-references

### Doctrine docs

- **Doc 24 — RTS Three Lanes** — Lane 1 hub canvases compose with schedule-driven NPC presence. The hub's "this NPC is here" framing now derives from `[[npcs.schedules]]`, not from "an NPC has a hub canvas at this location".
- **Doc 49 — Story Goals vs Sidebar Doctrine** — Orthogonal axis; no overlap. Quest goal text doesn't reference NPC presence directly.
- **Doc 50 — Quest Card Shape Doctrine** — Frame 2 (capstone Ready 🔓 📍 🕒) is the quest-card surface of the same fact the `NEW` nav badge surfaces. Both should appear simultaneously when a capstone is queued.
- **Doc 54 — Marge Redesign Session Lessons** — Appendix A pre-authoring checklist needs an additional item per §10 above. Follow-up edit on next NPC redesign session.

### Source code (post-session line numbers)

- `apps/game_generation/twee_comprehensive/generators/v2.py:2898` — `setup.getNpcLocation` (schedule-first, canvas-derived fallback for non-badge callers)
- `v2.py:3839` — `setup.selectAutoFireCanvasForLocation` (Path 1, capstone-shape filter)
- `v2.py:3868` — `setup.selectNpcPortraitCanvasesForLocation` (Path 2)
- `v2.py:3900` — `setup.selectSoloActivityCanvasesForLocation` (Path 3)
- `v2.py:3928` — `setup.locationHasNewCanvases` (capstone-only NEW badge — this session)
- `v2.py:4078` — `setup.getNpcsWithCanvasesAtLocation` (schedule-only NPC presence — this session)
- `v2.py:4249` — `setup.renderNpcPortraits` (fail-closed schedule filter — this session)
- `v2.py:4373` — `setup.renderSoloActivities` (per-solo NEW class removed — this session)

### TOML reference

- `games/the_long_summer_test/toml_phases/7_final_game.toml:414–461` — Frank's 7 schedule entries, gold-standard template.
- `7_final_game.toml:514` — Diana's single bedroom entry.
- `7_final_game.toml:535` — Marge's single diner entry.

### Live-play verification artifacts

- `game_explorations/tls-nav-indicators-verify/notes.md` — three timestamped verification entries (removed-pattern grep, schedule-only presence audit, capstone NEW audit).
- `game_explorations/tls-nav-indicators-verify/play_log.jsonl` — full command trail.
- `game_explorations/tls-nav-indicators-verify/saves/` — daemon state preserved; session re-runnable.

### v1.py status

Frozen per file header. v2.py is canonical. No parity work in this session.
