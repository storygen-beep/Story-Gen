# Step 2b — map design: lay out the world as a designed spatial graph (before casting)

Between top-level design (Step 2) and casting (Step 3) sits the step the pipeline used to skip: **design
the map.** Step 2 fixed the engine, economy, and machine; casting needs *stages* to place characters on.
This step produces those stages as a deliberate, reviewed artifact — the spatial graph, the naming, the
locks, the travel — so that by the time scenes get placed, the geography was *designed*, not invented
room-by-room to hold whatever scene needed a home.

**Why this step exists.** Without it, locations are a backdrop: enumerated as scenes demand them, then
emitted at authoring by copying a reference game's shape. A premise whose geography differs from that
reference ships incoherent and gets fixed by hand, pass after pass. The map is a system; it earns a
design pass like the cast and the machine do. (The full root-cause + the design knowledge live in
`references/location-design.md` — read it first; this step *runs* it.)

`pipeline_phase = "map_design"`.

## Inputs
Step 2's premise + cascade + economy + frontier + machine (the world's *jobs*) · the rough cast idea
(who will need to live somewhere) · **`references/location-design.md`** (the archetypes, the engine
model, the naming contract, the room-content floor, the nav-learnings — the whole design vocabulary).

## What it writes
A **`## Spatial graph & location model`** section in `design_book.md` and a seeded
`structure_registry.locations` preview in the ledger. **Plain language, no TOML** — the user reviews the
geography as a map they can picture, not as field syntax.

## The work — five moves (propose-first; see Interaction)

1. **Pick a topology archetype** (`location-design.md §2`) from the premise — nested-zones (default for
   a town + home), two-hub, map-image-hotspots, street-graph, or the time-slot anti-map. Name it and say
   *why this premise wants this shape*. **Size it two ways:** *scale* (add zones the cast needs) AND
   *aliveness* — a tight mission-slice (only what beats need) vs a living city (extra ambient zones), a
   content-budget fork you set on purpose (`location-design.md §2`; lean living for a sandbox).
2. **Lay out the spatial graph.** The roots (top-level, no `entry_from`), the containment + layering
   (private unit ≠ shared building ≠ town), and the travel graph (which `entry_from` chains connect
   what; which roots are bridged by walk activities). Draw it as a small tree/list the user can read down
   as a real place. Multi-floor / multi-building is just named hubs + `entry_from` — design the real
   geometry, don't cap it.
3. **Give each location its dramatic job + access model.** For every place, one line: *"this exists so
   the player can ___"* (the room-content floor — if you can't name it, the room doesn't ship; this is
   `content-framework.md §5A` made a gate). Then its access: reachable now / locked-until-a-beat
   (visible-but-blocked, with the unlock beat named) / offscreen "away" label.
4. **Name it** to one consistent contract (`location-design.md §3`) — bare-noun public, possessive
   private, hierarchy in the header not the label; pick the game's register and hold it.
5. **Decide travel friction** (`location-design.md §5`): does crossing a zone cost time/energy (so
   schedules bite)? If yes, put the cost on the *bridges* and add a fast-travel release valve. If no,
   say "free movement by design."

Then seed `structure_registry.locations` (id + category reachable/locked/offscreen) and run the
room-content + reachability lines of the §6 self-audit against the graph you just drew.

## Interaction — propose, don't just draw (per `run-mode.md`)
The **archetype, the roots/layering, AND how alive the world should feel** are identity-setting — they change
how the whole game feels to move through. Surface them **Mode A** (2–4 options + a recommendation): "a two-root
town-and-home nested map, or a single two-hub home/work? — and a tight mission-slice, or a living city?" The routine rooms (the bedrooms, the obvious venues) are
**Mode B** — name them in a line and move on. Propose the shape, explain *why* in plain words, settle
the real forks together, then write the section. Never commit the map silently; never ask about every
room.

## Self-check before casting
- The topology is one named archetype; **scale AND aliveness are chosen on purpose** (mission-slice ↔ living
  city, `location-design.md §2`), not drifted into; roots + layering are coherent.
- Every location has a one-line dramatic job (the room-content floor holds — no dead rooms planned).
- Every place is one access category, and every locked place has a named, reachable unlock beat.
- Naming is one consistent contract.
- Travel friction is a deliberate choice (costed bridges + fast-travel, or "free by design").
- `structure_registry.locations` is seeded; the §6 reachability/room-content lines pass on paper.
- No TOML written (that's authoring).

**Ledger:** when the section is written and reviewed, set `pipeline_phase = "casting"`.

## Cross-references
`references/location-design.md` (the design vocabulary this step runs) · `step-2-toplevel.md` (the
inputs) · `step-3-casting.md` (next — casts onto these stages) · `content-framework.md §5` (the world
questions; Step 4 §5 later imagines each place's *story* against this graph) · `run-mode.md` (the
propose-first rhythm) · `ledger-schema.md` (the `map_design` block + `structure_registry`).
