# Reference 04 — RTS HUD = World Model (Sidebar Doctrine)

**Sources:** Doc 56 P10 (HUD = world model principle); `game_explorations/rts-arc-trace/ui_map.json`; Doc 64 PRD (Sidebar NPC Location Radar — held); Doc 49 (body-state vs progression distinction); Doc 68 §8 (per-arc-shape sidebar visibility).
**Authority:** Reference. P10 evidence base.
**Purpose:** Document the RTS sidebar as the canonical "HUD = world model" UI surface — what it surfaces continuously, what TLS needs to mirror, what the per-arc-shape visibility doctrine is.

This file is the source-of-truth for `doctrine/01_rts_principles.md` P10 + `doctrine/04_authoring_rules.md` D56-R4 (sidebar surfaces NPC state) + `doctrine/09_trait_catalog.md` §8 (per-arc-shape visibility defaults).

---

## §1 — The HUD is the world model (P10)

Doc 56 P10:

> The player has to be able to SEE the world. Where every NPC is. What time it is. What clothes they're wearing. What money they have. The right sidebar IS the world surfaced to the player. **Without this radar, Lane 3 stops working entirely** (the room doesn't tell you the NPC is here; the sidebar does).

The HUD does the heavy lifting (P1). Each click is light in prose because the player's brain is loaded by what the sidebar continuously surfaces, not by what the scene reads like.

### §1.1 — Why P10 is load-bearing for Lane 3

Lane 3 = dispatcher substitution = "Maya was doing X and NPC happened" (`doctrine/02_three_lanes_plus_capstone.md` §4). The whole "you're doing X and he happened" texture depends on the player having situational awareness to choose X knowing it might collide with him.

Without per-NPC location radar, the player can't answer:
- "If I shower now, will Frank walk in?"
- "Should I wash dishes now or wait until Frank's home?"
- "Frank's in the kitchen — should I make tea?"

**Lane 3 becomes undiscoverable.** Players who don't check the sidebar can't plan against the dispatcher. The mechanism still works (dice roll inside the chore), but the player can't predict it without the HUD telling them where the NPC is.

### §1.2 — Live verification (Doc 56 P10 evidence)

> Right sidebar continuously renders Time (Early Morning, Monday, Clear weather), Quest pin, and per-NPC rows (Stepfather: Kitchen / Arousal / Corruption / Stepbrother: Bathroom / Arousal / Corruption / Stepgrandfather: Bedroom / Arousal / Corruption). Updates every tick. No menu click required to check NPC state.

Captured live across multiple RTS sessions. Per-NPC location radar is the most load-bearing single piece of UI for an RTS-shape sandbox.

---

## §2 — What the RTS sidebar continuously surfaces

Per `game_explorations/rts-arc-trace/ui_map.json` + live observation. The right sidebar renders:

### §2.1 — Top section: time + chrome

- **Time band:** "Early Morning" / "Morning" / "Afternoon" / "Evening" / "Night" / "Late Night"
- **Day:** "Monday" / "Tuesday" / ... / "Sunday"
- **Weather:** "Clear" / (other bands when implemented)
- **Chrome buttons:** 📕 Walkthrough / ⚙️ Settings / 🎁 Gallery / 🎯 Quests / 👤 Cheats (dev)

### §2.2 — Middle section: Maya stats (the "selectable list")

| Stat | Display | Notes |
|---|---|---|
| Beauty | "Beauty: 50" (integer) | Accumulating |
| Intelligence | "Intelligence: 12" | Accumulating |
| Fitness | "Fitness: 8" | Accumulating |
| Exhibitionism | "Exhibitionism: 15" | Accumulating |
| Corruption | banded: "Pure" / "Lewd" / "Slutty" / "Whore" + raw points hidden | Banded display (Doc 68 Q2 lock for TLS — 0-100 + 4 bands) |
| Arousal | bar 0–10 | Visual meter |
| Energy | bar 0–100 | Visual meter |
| Money | "$80" | Numeric |
| Outfit | "Casual jeans" | String, derived from `clothing.equipped` |

Maya stats are arranged for player planning. The player looks at this column to answer "can I do X right now?" (energy + outfit gates).

### §2.3 — Per-NPC rows (the radar)

Each in-scope NPC has a row:

```
Stepfather:    Kitchen    🔥  Corruption: 5
Stepbrother:   Bathroom   🔥🔥  Corruption: 12
Stepgrandfather: Bedroom  🔥🔥🔥  Corruption: 18
```

Three fields per row:
- **Location:** current location name (derived via `getNpcLocation(npcId)`)
- **Arousal:** emoji-tier (🔥 = 1-3, 🔥🔥 = 4-6, 🔥🔥🔥 = 7-10) OR integer band
- **Corruption:** integer

**Updates every tick.** No menu click required to check NPC state. The radar is the player's situational awareness for planning Lane 3 attempts + capstone triggers.

### §2.4 — Quest pin

The current active quest title + 1-line summary. Single quest at a time in RTS (with `📜 Quests` button to open the full quest journal).

---

## §3 — Per-NPC location radar (the core P10 surface)

The single most load-bearing piece of UI.

### §3.1 — Why location-only suffices for some NPCs

Antagonist arcs (Diana per `doctrine/03_arc_shapes.md` §7): **location only** surfaces. Awareness/scandal accumulator stays HIDDEN — dramatic surprise depends on the player NOT seeing how close confrontation is.

Why location is enough: the player needs to plan around Diana ("is Diana home? then this is risky") without knowing her current awareness level. The location radar suffices.

### §3.2 — Why location + stats is required for family/ambient

Family/ambient arcs (Brother per RTS; Frank per TLS): **location + arousal + corruption + relation** all surface.

Why all three: the player plans Lane 3 attempts (arousal), Lane 1 escalation (corruption), late-game intimacy (relation). All three are mechanically relevant; all three need to be visible.

RTS verified: Brother / Dad / Grandpa all show arousal + corruption (relation is always 0 for family arcs, so not surfaced).

### §3.3 — Per-arc-shape visibility doctrine (Doc 68 §8)

Per-arc-shape sidebar defaults:

| Arc shape | Sidebar surfaces (default) | Rationale |
|---|---|---|
| **Family/ambient** (Frank, Brother) | location + arousal + corruption + relation | Player plans L3 (arousal), L1 (corruption), late-game (relation). All three mechanically relevant. |
| **Slow-burn family** (Jake) | location + arousal + relation | Corruption stays low in slow-burn arcs by design; surfacing it would mislead the player. |
| **Peer/dating** (Ryan, Marcus) | location + relation | Dating chain is relation-driven. Arousal is bounded + less player-controllable. Corruption isn't meaningful for peer arcs. |
| **Service** (Marge) | location + relation only | Workplace bond is the operative axis. Arousal/corruption don't apply to service register. |
| **Antagonist/witness** (Diana) | location only | Awareness/scandal stays HIDDEN — dramatic surprise depends on player NOT seeing how close confrontation is. |
| **ALL arc shapes** | `stage` NEVER surfaces | Per LO Q1 + Doc 68 §9 — stage is internal-only across all NPCs. |

### §3.4 — Override mechanism

The brief can override the default with reason (per `doctrine/06_design_brief_template.md` §3.2). E.g., a family/ambient NPC whose arousal stays constant by design could hide it. But the override must be documented in the brief.

---

## §4 — Body-state vs progression-state surfacing (Doc 49)

Two distinct stat axes have different surfacing rules.

### §4.1 — Body-state (energy + hygiene) — MUST surface

Per Doc 49 + `doctrine/09_trait_catalog.md` §3.3 + §3.4:

- **`energy`** — render as `trait_status_text` with bands (Exhausted / Tired / Fine / Rested) OR `trait_bar` 0-100
- **`hygiene`** — render as `trait_status_text` with bands (Filthy / Dirty / Fresh / Clean)

**Body-state MUST surface.** The player needs to know when to sleep/shower. Hiding body-state means the player can't plan basic self-care.

### §4.2 — Progression-state — banded or hidden

- **`corruption`** — render as `trait_words` (banded: Pure / Lewd / Slutty / Whore). Raw 0-100 number HIDDEN.
- **`arousal`** — render as `trait_bar` (0-10 visual meter) with optional bands (Calm / Warm / Aroused / Hot / Burning — RTS-faithful: Calm 0 / Warm 1–2 / Aroused 3–5 / Hot 6–7 / Burning 8–10).
- **`money`** — render as numeric ("$80") or `trait_words` if banded.
- **`exhibitionism` / `fitness` / `intelligence` / `beauty`** — Tier 2 traits. Render only when the game's arc/setting uses them. `trait_bar` 0-100 OR hidden.

### §4.3 — Internal-only (NEVER surface)

- **`stage`** — per Doc 68 §9. Stage NEVER renders. Engine should not even know how to render it. Player feels stage progression through what the world DOES (new menu items appear, NPC behavior shifts, location access opens), NOT through a stage number.
- **Antagonist `awareness`** — per Doc 30 §6 + Doc 68 §8. Hidden by design.

### §4.4 — Sidebar item type doctrine

Per `schema/01_engine_capabilities.md` §8:

| `type` | Use case |
|---|---|
| `"trait_words"` | Banded prose label (4 named bands for corruption). Raw number hidden. |
| `"trait_bar"` | Numeric bar with optional band-text overlay + color tiers. For arousal, fitness, beauty, exhibitionism (when game uses them). |
| `"trait_status_text"` | Banded body-state text (Filthy/Dirty/Fresh/Clean). Renders nothing when no band matches. For energy + hygiene. |
| `"trait_decay_warning"` | Amber warning when a decaying trait dropped today + within range of a band gate. Sibling of `trait_status_text`. |

---

## §5 — TLS sidebar — current state (2026-05-28 slice)

Per `doctrine/01_rts_principles.md` §3 audit, TLS sidebar currently has:

1. **Arousal trait_bar** (Maya) — ✅ shipped
2. **Hygiene trait_status_text** (Maya) — ✅ shipped
3. **Energy trait_status_text** (Maya) — ✅ shipped
4. **Passes** (Maya inventory) — ✅ shipped
5. **Inventory** (Maya items) — ✅ shipped

**Zero NPC state surfaced.** This is the P10 misalignment (`doctrine/01_rts_principles.md` §3 audit row: 🔴 High severity).

### §5.1 — What's missing

- **Per-NPC location radar** for Frank / Diana / Jake / Ryan / Marge / Cookie
- **Per-NPC arousal + corruption + relation** per arc-shape doctrine (§3.3 above)
- **Time-band display** (currently shows 24-hour clock; RTS-style band display deferred)
- **Quest pin** (TLS V2 Quests engine shipped per-NPC quest cards but no single-pin sidebar item)

### §5.2 — Engine primitive already exists

`setup.getNpcLocation(npcId)` at `v2.py:2923` already computes NPC location from the NPC's `[[npcs.schedules]]` block. The engine surface is ready; sidebar authoring just needs to call it.

**SHIPPED (2026-06-06):** the `npc_panel` sidebar item type does exactly this — it calls
`setup.getNpcLocation` for the location row, so the per-NPC radar is now real.

---

## §6 — `npc_panel` sidebar card (SHIPPED — was Doc 64 PRD)

The per-NPC HUD radar shipped as the `npc_panel` sidebar item (renderer in `v2.py`/`v1.py`
`sidebarItems` widget; validation in `template_import.py`). It replaces the old PRD's proposed
`npc_location` type — **author `npc_panel`, not `npc_location`**.

### §6.1 — Schema

```toml
[[sidebar_items]]
type   = "npc_panel"
npc_id = "npc_frank"
label  = "Frank"                                  # optional → NPC name
rows   = ["arousal", "corruption", "location", "next"]    # ordered subset
# optional: arousal_bands, corruption_max_value/_label, away_label, show_when
```

Renders an RTS House-card:
```
Frank
  🔥 Arousal:    🔥🔥
  🫦 Corruption:  12        (or "MAX" at/above corruption_max_value)
  📍 Location:    Kitchen   (from setup.getNpcLocation — same source as the Schedule page)
  ── next (mirrors the Quests goal block) ──
  🎯 To advance:           (while climbing)
  ◯ My corruption — 12/20
  …or when ready…
  🔓 Ready
  📍 Kitchen                (the ready_canvas's location)
  🕒 every day 22:00–02:00  (the ready_canvas's schedule)
```
arousal → band glyph (default 0/1/2/3 → ❄️/🔥/🔥🔥/🔥🔥🔥); location is null-safe (`away_label`,
default "Away"); respects `hidden=true` traits. The **`next`** row reuses `setup.renderQuestsGoalBlock`,
so it shows the Quests-page goal block in full — `🎯 To advance` + ◯ live progress while climbing,
`🔓 Ready / 📍 / 🕒` when ready, `✓ Arc complete` when terminal — **identical to the Quests page**, minus
the flavor/tip prose.

### §6.2 — Authoring discipline

Emit `npc_panel` items for the NPCs whose state the player must read to plan (per the arc-shape
table in §3.3 — family/ambient + slow-burn). Surface only the rows that are live for that NPC
(e.g. a slow-burn NPC whose corruption stays 0 → `rows = ["arousal","location"]`). `stage` and
antagonist `awareness` still NEVER surface.

---

## §7 — What TLS borrows vs differs from RTS HUD

### §7.1 — TLS borrows

- **Right-side persistent sidebar** (TLS uses left + right; right is the world-model panel)
- **Banded `trait_words`** for corruption (Doc 68 Q2 lock — Pure/Lewd/Slutty/Whore for player corruption 0-100)
- **`trait_bar`** for arousal (Doc 40 lock — 0-10 with bands)
- **`trait_status_text`** for body-state (Doc 49 — energy + hygiene)
- **Per-arc-shape visibility** (Doc 68 §8 — refinement of RTS's flat "show everything for family")
- **Time + day chrome** (TLS shows day + 24-hour time; RTS uses 6-band model)

### §7.2 — TLS differs (intentional)

- **TLS hides stage trait.** Per Doc 68 §9 — internal-only.
- **TLS hides antagonist awareness.** Per Doc 30 §6 + Doc 68 §8 — dramatic surprise.
- **TLS banded corruption (0-100, 4 bands).** RTS uses 0-200 with 5-band points→level derivation. Doc 68 Q2 simplified for TLS.
- **TLS per-arc-shape stat visibility.** RTS surfaces all stats for all family NPCs flat; TLS differentiates per arc shape per Doc 68 §8.
- **TLS uses 24-hour clock** in slice. RTS uses 6-band model (EM/M/A/E/N/LN). Doc 30 §4.3 open question: keep 24-hour or migrate to bands.

### §7.3 — Per-NPC radar (SHIPPED via `npc_panel`)

- **Per-NPC location radar** — load-bearing per P10; now available as the `npc_panel` `location` row.
- **NPC arousal display per arc-shape default** — family/ambient (Frank) gets arousal surfaced; service (Marge) doesn't.
- **Tick-frequency updates** — every passage transition, not just hourly.

---

## §8 — Sidebar item authoring checklist

For each new TLS slice / prompts_v2 generated game, the sidebar block should declare:

### §8.1 — Maya state (mandatory)

- [ ] `trait_words` for corruption (banded Pure/Lewd/Slutty/Whore)
- [ ] `trait_bar` for arousal (0-10 with bands)
- [ ] `trait_status_text` for energy (banded Exhausted/Tired/Fine/Rested)
- [ ] `trait_status_text` for hygiene (banded Filthy/Dirty/Fresh/Clean)
- [ ] Numeric display for money (with currency symbol)

### §8.2 — Tier 2 stats (declare only if game uses them)

- [ ] `trait_bar` for fitness (if exercise/gym mechanic exists)
- [ ] `trait_bar` for exhibitionism (if flash/cam arcs exist)
- [ ] `trait_bar` for intelligence (if school/study mechanic exists)
- [ ] `trait_bar` for beauty (typically hidden — derived from worn_beauty)

### §8.3 — Per-NPC radar — `npc_panel` (SHIPPED)

For each in-scope NPC whose state the player must read to plan:

- [ ] `npc_panel` item with `npc_id`
- [ ] `rows` per arc-shape (subset of arousal/corruption/location/next):
  - Family/ambient: `["arousal", "corruption", "location", "next"]`
  - Slow-burn family: `["arousal", "location"]`
  - Peer/dating + service: `["location"]` (+ relation via a `trait_owner="npc"` trait_bar if wanted)
  - Antagonist: `["location"]` (awareness NEVER surfaces)

### §8.4 — DO NOT surface

- [ ] No `stage` sidebar items for ANY NPC
- [ ] No `awareness` / `scandal_level` for antagonist NPCs
- [ ] No flags directly (use `trait_words` bands derived from flags if needed)

---

## §9 — Why HUD discipline is hard

The HUD's job is to surface state continuously. The temptation is to show everything — but Doc 68 §8 + the per-arc-shape doctrine specifies what NOT to surface:

- Stage as opaque progression (player feels it through content, not numbers)
- Antagonist awareness (the surprise IS the dramatic engine; surfacing it ruins the arc)
- Internal author-side metadata (which canvases are still locked, etc.)

**The HUD is the world model — but the world model the PLAYER experiences, not the world model the AUTHOR knows.**

Authoring discipline: when adding a new sidebar item, ask:

1. Does the player NEED this to plan their next action? → surface
2. Does surfacing this spoil dramatic surprise? → hide
3. Is this player-facing progression or author bookkeeping? → if bookkeeping, hide
4. Does this match the per-arc-shape default? → if not, document the override in the brief

---

## §10 — Cross-references

### Sibling reference files

- `reference/01_rts_overview.md` §6.3 — sidebar surface (broad context)
- `reference/03_rts_walkthrough_panel.md` — companion surface (Walkthrough = published catalog; HUD = world model)

### Sibling doctrine files

- `doctrine/01_rts_principles.md` P10 — HUD = world model principle
- `doctrine/04_authoring_rules.md` D56-R4 — sidebar must surface NPC state for in-scope NPCs
- `doctrine/09_trait_catalog.md` §8 — per-arc-shape sidebar visibility doctrine
- `doctrine/09_trait_catalog.md` §9 — stage trait special-handling (NEVER surface)

### Source

- `28th_april_TLS_Phase2_Redesign/56_RTS_Principles_and_TLS_Alignment_Doctrine.md` P10 — principle source
- `28th_april_TLS_Phase2_Redesign/64_Sidebar_NPC_Radar_PRD.md` — engine work to ship per-NPC location item (held per Doc 66 §10)
- `28th_april_TLS_Phase2_Redesign/49_Story_Goals_vs_Sidebar_Doctrine.md` — body-state vs progression-state distinction
- `28th_april_TLS_Phase2_Redesign/68_Trait_Catalog.md` §8 — per-arc-shape visibility table source

### Engine source

- `setup.getNpcLocation(npcId)` (`v2.py:2923`) — computes NPC location from schedules; ready for sidebar consumption
- `game_explorations/rts-arc-trace/ui_map.json` — RTS HUD chrome catalog (P10 evidence)
- `template_import.py:2382-2547` — sidebar item validator (rejects undeclared traits with hard error)

---

**End of file.** Next: `schema/03_example_toml.md` for the TLS Frank slice canonical TOML examples.
