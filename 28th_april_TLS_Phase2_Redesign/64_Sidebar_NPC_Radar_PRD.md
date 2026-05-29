# Doc 64 — Sidebar NPC Location Radar PRD

**Session:** 2026-05-25
**Branch:** `feature/prd-48-quests-engine-v2-bundled` (off `main`, unpushed)
**Author:** ENI (with LO)
**Status:** Engine PRD — implementation spec; NOT shipped. Doctrine locked in Doc 56 R4 / P10; sidebar item type locked here.
**Supersedes:** nothing
**Sibling of:** Doc 62 (Guide Field PRD), Doc 63 (Validator Extension PRD)
**Triggered by:** Doc 56 R4 + P10 alignment audit found 🔴 High-severity gap — TLS sidebar currently shows Maya state only; doesn't surface NPC location continuously. RTS sidebar (verified live-play) shows every family NPC's location + arousal + corruption per tick. Without this radar, Lane 3 dispatcher substitutions are undiscoverable; players can't plan against NPC state.

---

## §1 — The problem this PRD solves

Doc 56 P10 — *"the HUD is the world model."* The sidebar IS the radar by which players know where NPCs are, when activities will collide with which NPC, and what's worth doing this turn.

Verified RTS sidebar (live-play): continuously renders Stepfather/Stepbrother/Stepgrandfather rows showing location + arousal + corruption per tick. This is what makes RTS playable — without the radar, "go to the kitchen" is a blind guess; with the radar, "Brother is in the kitchen, his arousal is 2, my activity might collide with him" is a planned move.

TLS currently has Maya-state sidebar (corruption, arousal, hygiene, energy, passes, inventory) — 5 sidebar items per agent inventory. NPC state is invisible until the player opens a menu or guesses.

This PRD adds a new sidebar item type `npc_location` (and optionally `npc_trait_radar`) that surfaces in-scope NPC state continuously. **First sidebar item type that calls a runtime function** (rather than reading a trait value) — the API precedent for future function-calling sidebar items.

---

## §2 — Required surfaces

Per Doc 56 R4: *"sidebar must surface NPC state (location + key stats) for in-scope NPCs."*

Concretely for TLS slice:

| NPC | Surface | Render shape |
|---|---|---|
| Frank | Location + arousal | "Frank — Kitchen / 🔥 2" or "Frank — Away" |
| Diana | Location + awareness band | "Diana — Bedroom / 👀 Knowing" |
| Marge | Location (during shift hours only) | "Marge — Diner" (hidden off-shift) |
| Ryan | Location + trust | "Ryan — Yard / Trust 8" |
| Jake | Location (always his room) + stage indicator | "Jake — Room" or "Jake — Working" |

Cookie deliberately excluded per Doc 61 scope-out (no schedule, no surface needed).

---

## §3 — New sidebar item types

### Type 1 — `npc_location` (primary, this PRD's core ship)

Renders the NPC's current location with optional label prefix and away-fallback.

**Schema (TOML shape):**

```toml
[[sidebar_items]]
type        = "npc_location"
npc_id      = "npc_frank"
label_prefix = "Frank"          # optional, defaults to NPC's display name
show_when_away = true            # optional, defaults to true; if false, hide row when NPC has no schedule entry for current time
away_text   = "Away"             # optional, default "Away"
```

**Runtime behavior:**
- Calls `setup.getNpcLocation(npc_id)` (v1.py:2758) each render
- If returns null OR off-schedule: render `"{label_prefix} — {away_text}"` (or hide row if `show_when_away = false`)
- If returns location object: render `"{label_prefix} — {location_display_name}"`
- Uses `setup.locations[location_uuid].name` to resolve display name (already cached)

**Engine work:**
- New validator block in `template_import.py` modeled on `trait_status_text` validator at template_import.py:2527
- Runtime emission in v1.py — extend the sidebar item renderer to dispatch on `type = "npc_location"` and call `getNpcLocation`
- Cache-friendly: re-evaluate each `<<UpdateScreen>>` call (consistent with existing sidebar items)

### Type 2 — `npc_trait_status_text` (lower priority, optional in this PRD)

A specialization of existing `trait_status_text` for NPC traits — bands an NPC's arousal/awareness/trust value into a status string.

**Schema:**

```toml
[[sidebar_items]]
type        = "npc_trait_status_text"
npc_id      = "npc_frank"
trait_key   = "arousal"
bands = [
  { min = 1, max = 1, text = "🔥" },
  { min = 2, max = 2, text = "🔥🔥" },
  { min = 3, max = 3, text = "🔥🔥🔥" },
]
label_prefix = "Frank arousal"
```

**Runtime behavior:** identical to `trait_status_text` but reads `setup.npcs[npc_uuid].traits[trait_key]` instead of `setup.player.traits[trait_key]`.

**Note:** could alternatively extend existing `trait_status_text` to accept a `subject = "npc"` parameter. Cleaner schema; same outcome. PRD recommendation: extend the existing type rather than add a new type — less surface area.

### Type 3 — Combined `npc_radar_row` (deferred to follow-up)

A composite row showing location + key trait status in one line ("Frank — Kitchen / 🔥 2"). Composite of Type 1 + Type 2 rendered as one row. Cleaner UX; more schema. Deferred to a follow-up PRD if the per-component shape ships first and proves the surface.

---

## §4 — Implementation paths

### Schema validator hook (`template_import.py`)

Model on `trait_status_text` validator at template_import.py:2527. Add new validation block:

```python
elif si_type == "npc_location":
    # Validate npc_id present + resolvable
    if "npc_id" not in si:
        errors.append(f"{ctx}: npc_location requires 'npc_id'")
    elif si["npc_id"] not in [n["id"] for n in self.npcs]:
        errors.append(f"{ctx}: npc_location.npc_id '{si['npc_id']}' not found in [[npcs]]")
    # Validate optional fields
    if "label_prefix" in si and not isinstance(si["label_prefix"], str):
        errors.append(f"{ctx}: label_prefix must be string")
    if "show_when_away" in si and not isinstance(si["show_when_away"], bool):
        errors.append(f"{ctx}: show_when_away must be bool")
    if "away_text" in si and not isinstance(si["away_text"], str):
        errors.append(f"{ctx}: away_text must be string")
```

### Runtime emission hook (`v1.py`)

Find where sidebar items are rendered into HTML (likely a dispatch in v1.py that iterates `sidebar_items` and calls per-type renderers). Add:

```javascript
} else if (item.type === "npc_location") {
    var npcLoc = setup.getNpcLocation(item.npc_id);
    var labelPrefix = item.label_prefix || setup.getNpcDisplayName(item.npc_id);
    var awayText = item.away_text || "Away";
    var showWhenAway = item.show_when_away !== false;

    if (!npcLoc || !npcLoc.location) {
        if (showWhenAway) {
            html += '<div class="sidebar-row">' + labelPrefix + ' — ' + awayText + '</div>';
        }
        // else hide row entirely
    } else {
        var locName = setup.locations[npcLoc.location].name || npcLoc.location;
        html += '<div class="sidebar-row">' + labelPrefix + ' — ' + locName + '</div>';
    }
}
```

Coordinate with the existing `<<UpdateScreen>>` invalidation — sidebar items re-render on each turn, so the function-call cost is per-turn (small).

### Serializer hook (no change needed)

Sidebar items are emitted from `project.metadata["sidebar_items"]` (per agent inventory at template_import.py:4714). The TOML round-trip already includes any new fields on the dict. No serializer change required.

---

## §5 — TLS slice authoring plan

After schema lands, add sidebar items to the TLS TOML in the `[[sidebar_items]]` section:

```toml
# NPC location radar — Doc 56 R4 + P10
[[sidebar_items]]
type   = "npc_location"
npc_id = "npc_frank"

[[sidebar_items]]
type   = "npc_location"
npc_id = "npc_diana"

[[sidebar_items]]
type   = "npc_location"
npc_id = "npc_marge"
show_when_away = false  # hide off-shift; Marge isn't tracked outside diner hours

[[sidebar_items]]
type   = "npc_location"
npc_id = "npc_ryan"

[[sidebar_items]]
type   = "npc_location"
npc_id = "npc_jake"
```

5 sidebar items added. Cookie excluded per Doc 61.

If extending to `trait_status_text` with `subject = "npc"`, add per-NPC stat radar after location rows:

```toml
[[sidebar_items]]
type      = "trait_status_text"
subject   = "npc"
npc_id    = "npc_frank"
trait_key = "arousal"
bands     = [...]
label_prefix = "Frank"
```

Estimated authoring: ~30 min for the 5 location items + ~1 hour for selected per-NPC trait readouts (Frank arousal, Diana awareness band, Ryan trust). Per-NPC trait surface is lower priority; LO call on whether to ship in same pass.

---

## §6 — Engine work estimate

| Task | Estimated time |
|---|---:|
| Schema validator for `npc_location` | 30 min |
| Schema validator extension for `trait_status_text` with `subject = "npc"` | 30 min |
| Runtime renderer for `npc_location` (v1.py dispatch + getNpcLocation wiring) | 1 hr |
| `setup.getNpcDisplayName` helper (if not already present) | 15 min |
| `setup.locations[uuid].name` resolution check | 15 min |
| Tests — schema round-trip for `npc_location` (5 cases) | 1 hr |
| Tests — runtime emission against TLS slice fixture | 1 hr |
| Tests — getNpcLocation null-safety (off-schedule NPCs) | 30 min |
| Documentation in template_import.py docstring | 30 min |
| Total | **~5 hr** |

Small-to-medium PRD. The runtime work hinges on the dispatch-on-type pattern already used by existing sidebar item types — extending it is straightforward.

---

## §7 — Tests

In `apps/projects/tests.py`:

1. **Schema round-trip — `npc_location` minimal.** `{type: "npc_location", npc_id: "npc_frank"}` parses + serializes cleanly.
2. **Schema round-trip — `npc_location` with all options.** `{type, npc_id, label_prefix, show_when_away, away_text}` all preserved.
3. **Validator — missing `npc_id`.** ERROR emitted.
4. **Validator — invalid `npc_id` (not in [[npcs]]).** ERROR emitted.
5. **Validator — bad `show_when_away` type.** ERROR emitted.
6. **Runtime — Frank in kitchen schedule.** sidebar renders `"Frank — Kitchen"`.
7. **Runtime — Frank off-schedule + show_when_away = true.** sidebar renders `"Frank — Away"`.
8. **Runtime — Frank off-schedule + show_when_away = false.** sidebar omits Frank row.
9. **Runtime — NPC with no schedule entries.** sidebar uses away_text.
10. **Performance — 10 NPC sidebar rows + 60 game turns.** No noticeable per-turn cost (sub-millisecond getNpcLocation calls).

If extending `trait_status_text` for npc subject, add parallel tests for that path.

---

## §8 — Doctrine implications

### First function-calling sidebar item type

This PRD establishes the precedent: sidebar items CAN call runtime functions, not just read trait values. Future surfaces (per Doc 56 P10 / P1 decision pressure):
- `npc_schedule_next_window` — when does this NPC's next location window open?
- `world_clock_relative` — "2 hours till Diana's bedtime"
- `aggregate_arousal_status` — summed lewd-pressure across all NPCs

Each new function-calling sidebar type follows this PRD's pattern: schema validator + dispatch in renderer + function call. Don't bloat with non-essential surfaces; each one should solve a real Doc 56 alignment gap.

### NPC location radar = P1 + P2 + P10 alignment

This single sidebar surface closes three Doc 56 alignment gaps simultaneously:
- **P1 (decision pressure):** player can plan against NPC-presence collisions per turn
- **P2 (transparent gating):** Lane 3 substitutions become discoverable (player sees "Frank — Kitchen" + knows kitchen activities might collide)
- **P10 (HUD = world model):** the radar surface is the world model

Catalog UI (Doc 56 P2 future PRD) is the second half of P2; sidebar radar is the cheaper, higher-impact half.

---

## §9 — Out of scope (intentional)

- **Composite `npc_radar_row` type** combining location + trait. Deferred per §3 Type 3 note. Can ship if/when per-component types prove insufficient.
- **Click-to-jump-to-NPC affordance** — clicking the sidebar row routes the player to the NPC's location. Real Doc 56 P10 alignment but additional UX work. Future PRD.
- **NPC mood / dialog-status surface.** Some games show "Frank: Annoyed" or "Frank: Hungry" — currently TLS doesn't track per-NPC mood. Deferred per Doc 65 strategic scope (if NPC mood becomes a Phase 2+ engine system, this PRD amends).
- **Animation / transitions on sidebar updates.** Doc 56 P10 says "continuously surfaces" — instant re-render per turn is sufficient.
- **Mobile / responsive sidebar layout.** Existing sidebar layout handles responsiveness; new item type inherits. No change.
- **Per-game sidebar configuration (which NPCs to track).** Currently TLS author commits the in-scope NPCs via `[[sidebar_items]]`. Other games author their own list. No engine-level config.
- **Cookie sidebar row.** Excluded per Doc 61 scope-out. Cookie has no schedule + no slice-scope arc; surfacing her location would be misleading.

---

## §10 — References

### Sibling and ancestor docs

- **Doc 13** — Road to Success Reference (§HUD live-play observations — RTS sidebar precedent)
- **Doc 56** — RTS Principles & TLS Alignment Doctrine (P1 + P2 + P10 + R4 source)
- **Doc 62** — Canvas guide field PRD (sibling engine PRD)
- **Doc 63** — Validator Extension PRD (sibling engine PRD)
- **Doc 65** — Phase 2+ Strategic Scope (NPC mood / scandal system implications)

### Live engine references (verified)

- `apps/projects/services/template_import.py:320` — `sidebar_items` field on GameTemplate
- `apps/projects/services/template_import.py:2383-2609` — sidebar item type validation block
- `apps/projects/services/template_import.py:2527` — `trait_status_text` validator (model for new type)
- `apps/projects/services/template_import.py:4714` — sidebar_items persistence in project metadata
- `apps/projects/services/template_import.py:7285-7325` — `_auto_emit_counter_sidebar_items` (auto-emission pattern reference)
- `apps/game_generation/twee_comprehensive/generators/v1.py:2758-2782` — `setup.getNpcLocation` (runtime API)

### Live TLS reference

- `games/the_long_summer_test/toml_phases/7_final_game.toml` — `[[sidebar_items]]` section (current 5 items: arousal trait_bar, hygiene trait_status_text, energy trait_status_text, passes, inventory)
- `games/the_long_summer_test/toml_phases/7_final_game.toml:467+` — NPC declarations (npc_frank, npc_diana, npc_marge, npc_ryan, npc_jake, npc_cookie)
- `games/the_long_summer_test/toml_phases/7_final_game.toml:414-520` — NPC schedule entries (Frank full, Diana bedroom, Marge none, Ryan none, Jake none — agent inventory)

### Schedule gap note

Marge, Ryan, Jake, Cookie currently have no `[[npcs.schedules]]` entries (only Frank + partial Diana). For the radar to render meaningfully, those NPCs need at least minimal schedule entries — OR the radar falls back to "Away" for them. Either is OK; LO call when authoring §5 sidebar items.
