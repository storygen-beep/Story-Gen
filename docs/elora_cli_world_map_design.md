# Elora CLI — World Map Design (Alignment with `twee_comprehensive`)

Status: Draft
Owner: TBD
Last Updated: {auto}

## Summary
Elora CLI currently creates `Location` and `LocationConnection` records but doesn’t reason about world graphs (adjacency, hubs, entry routing) or validate connectivity. The `twee_comprehensive` generator v1 also ignores `LocationConnection`, listing all locations globally.

This doc defines how to make Elora CLI a true world designer, and how to minimally evolve the generator to respect the world map — while keeping backward compatibility and avoiding schema changes.

## Goals
- Graph-aware world building in CLI (adjacency, hubs, degree ≥ 1 policy).
- Entry routing semantics: entering a container goes to its default interior (e.g., Home → Living Room).
- Neighbor-only navigation during play (respect `is_bidirectional`).
- Continue to surface location-triggered canvases with optional schedules.
- Validator-driven UX: detect isolated nodes, missing starting/entry locations.

## Non-Goals
- No schema changes (use `Location.properties` for extra flags/ids).
- No global refactor of unrelated systems.
- No complex simulation (keep simple and deterministic).

## Current State & Gaps
- CLI: CRUD only; lacks world-graph reasoning and validator.
- Generator v1: Shows a global location list; doesn’t use connections; no entry routing.
- No bootstrap policy for the “first location”.

## Proposed Changes

### 1) CLI: New Tooling (ORM-backed)
Add high-value tools (idempotent where possible):
- `get_world_graph()`
  - Returns nodes/edges, degrees, connected components, container→child map.
- `get_neighbors(location_id)`
  - Returns adjacent locations from outgoing edges; respect `is_bidirectional`.
- `ensure_location(name, description?, type?, container_parent_id?)`
  - Create or return existing location; supports nesting (validates container parent).
- `ensure_bidirectional_connection(from_id, to_id, connection_type='path')`
  - Upsert one row with `is_bidirectional=True`; no reverse row.
- `set_starting_location(location_id)`
  - Marks project entry (and uses it for generation defaults).
- `set_default_entry(container_id, child_id)`
  - Stores `default_entry_child_id` in `Location.properties`.
- `validate_world_graph()`
  - Returns issues (see Validation Rules) with severity and quick-fix suggestions.

Notes:
- Use existing models (`apps.world.models`) and JSON `properties` fields. No migrations needed.

### 2) Agent Prompt: World-Graph Playbooks
Augment Elora’s system prompt with explicit design rules:
- Start with discovery → graph extraction → create/connect → validate → canvases → generate.
- Maintain degree ≥ 1 for non-intentionally-isolated locations.
- If creating an exterior/interior pair (e.g., Home + Living Room): set `default_entry_child_id` and connect them.
- When user says “enter X”: if X is a container with a default entry child, route to that child.
- Prefer hubs (hallway, lobby, square) for connecting multiple leaves.

### 3) Generator v1: Minimal Neighbor-Aware Navigation (Phase 2)
- Replace global location list with neighbor-only links from the player’s current location.
- Honor `is_bidirectional` (one-way edges navigate only in allowed direction).
- Entry routing: if arriving at a container with `properties.default_entry_child_id`, auto-redirect to that child passage.
- Fallback: If the graph has 0 connections, keep current global list for navigation (back-compat).

## Bootstrap Policy (First Location)
- Allow degree 0 for the first (and only) location: report as Info, not Error.
- Auto-suggest: set as `starting_location` if none exists.
- If the user intends a container pattern (e.g., “Home”), offer to create an interior (e.g., “Living Room”) and connect them (ask before applying).
- Once `total_locations ≥ 2`, enforce degree ≥ 1 for non-intentional isolates.

## Validation Rules
Severity tiers returned by `validate_world_graph()`:
- Info
  - Single unconnected location in project (bootstrap case).
- Warning
  - Containers without `default_entry_child_id`.
- Error
  - Isolated locations when `total_locations ≥ 2`.
  - Missing starting location.
  - Cross-project connections.
  - One-way mistakes (e.g., intended bidirectional adjacency left one-way).

Quick-fix suggestions include:
- “Connect <leaf> to <hub> via door/path.”
- “Set default entry child for <container> to <child>.”
- “Set starting location to <location>.”

## Data Model Usage
- `Location.properties.default_entry_child_id` (UUID string) — default interior for containers.
- Optional flags: `properties.is_hub = true` for hubs (purely advisory).
- Do not create reverse connection rows; use `is_bidirectional` column.

## Rollout Plan
- Phase 1: CLI
  - Implement new tools (graph, ensure*, neighbors, validator).
  - Update agent system prompt with world-graph playbooks.
  - Keep generator unchanged (safe).
- Phase 2: Generator
  - Switch to neighbor-only navigation; add entry routing; maintain global fallback when no edges.
- Phase 3: Quality of Life
  - Add CLI shortcuts: `/design_home`, `/connect A to B`, `/set_starting X`.

## Testing Plan (pytest)
- Bootstrap
  - Single location: validator returns Info; generator navigates with global list.
- Connectivity
  - Two locations, bidirectional edge: neighbor lists reflect both ways.
  - One-way edge: only allowed direction appears.
  - Isolated node with `total_locations ≥ 2`: validator Error.
- Container Entry
  - Container + interior with `default_entry_child_id`: entering container redirects to interior.
- Schedules
  - Location-triggered canvases with schedules: appear only when active.
- Back-Compat
  - No connections present: generator behavior unchanged (global list).

## Open Questions
- Should we allow an explicit “intentionally isolated” flag to suppress errors for specific nodes?
- Do we want a default hub type (e.g., “Hallway”) created on demand when a user creates ≥2 interiors?
- Should the generator show breadcrumbs (e.g., “Back to Hub”), or keep pure neighbor links?

## Risks & Mitigations
- Risk: Breaking existing projects with no connections.
  - Mitigation: Keep generator global fallback when 0 edges exist.
- Risk: Over-creation by the agent.
  - Mitigation: Safety gate prompts and idempotent `ensure_*` tools.
- Risk: Confusion about containers vs non-containers.
  - Mitigation: CLI explicitly sets/reads `is_container` and default entry child.

## Quick Examples
- Home + Living Room (entry pair):
  1) `ensure_location("Home", type="residential", container_parent_id=None)` → `is_container=True`
  2) `ensure_location("Living Room", type="residential", container_parent_id=Home)`
  3) `ensure_bidirectional_connection(Home, Living Room, "door")`
  4) `set_default_entry(Home, Living Room)`

- School Wing (hub + labs):
  1) `ensure_location("Main Hallway", type="educational")`
  2) `ensure_location("Chem Lab", type="educational")`
  3) `ensure_location("Physics Lab", type="educational")`
  4) `ensure_bidirectional_connection(Hallway, Chem Lab, "door")`
  5) `ensure_bidirectional_connection(Hallway, Physics Lab, "door")`

- Secret Room (locked):
  1) `ensure_location("Library")`, `ensure_location("Hidden Study")`
  2) `ensure_bidirectional_connection(Library, Hidden Study, "door")` with `requires_key=True`, `unlock_conditions={"key":"Brass Library Key"}`

---
This plan keeps changes minimal, backward-compatible, and focused on user value: CLI becomes a graph-aware world designer; the generator honors the map when present and gracefully degrades otherwise.

## Phase 1 Tasks (CLI + Prompt)

- [ ] Implement `get_world_graph()` (nodes, edges, degree, components, container→children)
- [ ] Implement `get_neighbors(location_id)` (honor `is_bidirectional`/direction)
- [ ] Implement `ensure_location(name, description?, type?, container_parent_id?)`
- [ ] Implement `ensure_bidirectional_connection(from_id, to_id, type='path')`
- [ ] Implement `set_starting_location(location_id)`
- [ ] Implement `set_default_entry(container_id, child_id)` (via `Location.properties.default_entry_child_id`)
- [ ] Implement `validate_world_graph()` with severity and suggestions
- [ ] Update Elora system prompt with world-graph playbooks and bootstrap policy
- [ ] Add REPL helpers (optional) for quick flows (e.g., “design home”, “connect A to B”)

## Tool API (CLI)

- `get_world_graph() -> { nodes, edges, degrees, components, containers }`
  - nodes: `[ {id, name, is_container, parent_id?} ]`
  - edges: `[ {id, from_id, to_id, type, is_bidirectional} ]`
  - degrees: `{ location_id: {out: int, in: int, undirected: int} }`
  - components: `[ [location_id, ...], ... ]`
  - containers: `{ container_id: [child_id, ...] }`

- `get_neighbors(location_id: str) -> { outgoing: [ {id, name} ], incoming: [ {id, name} ], traversable: [ {id, name} ] }`
  - traversable = outgoing + (incoming if `is_bidirectional` on the matching edge)

- `ensure_location(name: str, description?: str, type?: str, container_parent_id?: str) -> { id, created }`
  - Idempotent on `(project_id, name)`; validates container parent if provided.

- `ensure_bidirectional_connection(from_id: str, to_id: str, type='path') -> { id, created }`
  - Single row with `is_bidirectional=True`; do not create reverse row.

- `set_starting_location(location_id: str) -> { updated: bool }`
  - Updates `Project.starting_canvas` only if we have one; else stores starting location in `Project.settings` or uses location to guide initial navigation (implementation-specific; see generator plan).

- `set_default_entry(container_id: str, child_id: str) -> { updated: bool }`
  - Writes `Location.properties.default_entry_child_id`.

- `validate_world_graph() -> { has_errors: bool, issues: [ {severity, code, message, fix?} ], stats }`
  - Codes: `FIRST_LOCATION_UNCONNECTED (info)`, `MISSING_START (error)`, `ISOLATED_NODE (error)`, `CONTAINER_NO_DEFAULT_ENTRY (warn)`, `CROSS_PROJECT_EDGE (error)`, `UNIDIRECTIONAL_SUSPECT (warn)`.

## Prompt Addendum (to insert in Elora CLI system prompt)

“World-Graph Rules:
- Start with discovery: list locations, extract the graph, identify hubs and containers.
- Maintain degree ≥ 1 for all non-intentionally-isolated locations once there are ≥ 2 locations.
- If creating an exterior/interior pair (e.g., Home + Living Room), connect them bidirectionally and set the container’s default entry child.
- Treat ‘enter X’ as moving to X, or to its default interior if X is a container.
- Prefer hubs (hallway, lobby, square) to anchor multiple rooms.
- Before finishing a change, run `validate_world_graph()` and address errors.”

Bootstrap Policy:
- If total locations == 1, allow degree 0 and set a starting point; treat as Info, not Error.

## Phase 2 Tasks (Generator)

- [ ] Derive neighbor list per location from `LocationConnection`
- [ ] Respect `is_bidirectional`: only show traversable neighbors
- [ ] Auto-redirect to `default_entry_child_id` when arriving at a container
- [ ] Maintain fallback (global list) when 0 edges exist
- [ ] Keep schedule-aware canvas triggers as-is (already supported)

Suggested structure changes in `twee_comprehensive/generators/v1.py`:
- In `_generate_simple_locations()`, replace “other locations” section with neighbors for each location:
  - Query edges once; build adjacency map `{loc_id: [neighbor_ids...]}`
  - Render links only to neighbors for that location
- On arriving at a location, if it’s a container and `default_entry_child_id` is set, route: `[[Enter->{Location_<child_name>}]]` (implicit redirect) before listing neighbors.
- If no connections at all, keep existing global list navigation.

## Admin UX Note

- Current inline shows only outgoing edges (`fk_name = 'from_location'`).
- Optional improvement: Add an “Incoming Connections” inline (`fk_name = 'to_location'`) or a combined read-only block that lists both.
- Keep single-row edge semantics with `is_bidirectional=True` (do not duplicate edges).

## Edge Cases

- Single location: allowed unconnected; generator uses global list fallback.
- Parallel areas (disconnected components): traversal is local to each component; validation warns only if nodes are unintentionally isolated.
- One-way edges: show only allowed direction in navigation.
- Locked edges: keep link hidden or disabled unless unlock conditions are met (future enhancement; present as descriptive note in content).
- Containers without default entry: warn; still allow entering container passage without redirect.

## Acceptance Criteria

- Creating a new interior under a container sets `default_entry_child_id` and connects rooms bidirectionally (when requested).
- `validate_world_graph()` reports:
  - Info for single unconnected location
  - Error for isolated nodes when total locations ≥ 2
  - Warning for container missing default entry
- Generator shows neighbor-only navigation when ≥ 1 edge exists; otherwise global list.
- Arrival to a container with `default_entry_child_id` redirects to that child.
- Admin page for a location clearly shows connections both ways (either via two inlines or a combined display).

## Logging & Telemetry (optional)

- Log creation/update of connections with from→to, `is_bidirectional`, and resulting degrees of both endpoints.
- Log validation summaries (counts by severity, component sizes).

## Work Breakdown & Files

- CLI: `apps/elora_simplified/management/commands/elora_cli.py`
  - Add world-graph tools; update prompt text; optionally add REPL helpers.
- Generator: `apps/game_generation/twee_comprehensive/generators/v1.py`
  - Neighbor-aware navigation, container entry routing, fallback mode.
- Admin (optional): `apps/world/admin.py`
  - Add incoming-connections inline or combined display.
