# World Navigation Model Migration (Entries, Exit, Default Entry)

This document describes the complete replacement of `LocationConnection` with three per‑location navigation fields and the corresponding API and frontend updates.

- Entries: `Location.entry_connections` (ManyToMany to `Location`)
- Exit: `Location.exit_connection` (FK to `Location`)
- Default Entry: `Location.default_entry_location` (FK to `Location`, container‑only, must be a direct child)

## Goals
- Replace per‑edge `LocationConnection` CRUD with per‑location operations (entries/exit/default entry).
- Expose the new navigation fields from the API.
- Render edges on the frontend directly from per‑location fields with distinct colors and semantics.
- Provide a smooth, backwards‑compatible transition (derived connections list) and then clean up deprecated code.

---

## Backend Changes

### Files
- `apps/world/serializers.py`
- `apps/world/views.py`
- `apps/world/urls.py`
- (Later cleanup) `apps/world/admin.py`, `apps/world/models.py` (`LocationConnection` removal post‑migration)

### Location Serializer
Expose read‑only fields on `LocationSerializer`:
- `entry_connection_ids: string[]`
- `exit_connection_id: string | null`
- `default_entry_location_id: string | null`

Ensure `to_representation` returns consistent defaults and fills `entry_connection_ids` from the M2M.

### World Overview
- Prefetch `entry_connections` to avoid N+1 queries.
- Stop reading `LocationConnection` for the overview.
- Return:
  - `locations`: with the new navigation fields.
  - `connections` (compat only): derive from the new fields.
    - Entries → blue `#3b82f6`, solid, `connection_type: "path"`, arrow: bidirectional.
    - Exit → green `#10b981`, dashed, `connection_type: "exit"`, arrow: unidirectional.
    - Default entry (hint) → purple `#8b5cf6`, dotted, `connection_type: "default_entry"`, arrow: unidirectional.
  - `connection_count`: size of the synthesized list.

### New Endpoints
Replace `/world/connections` CRUD with the following:

- Add Entry
  - `POST /api/v1/projects/{project_id}/world/locations/{id}/entries/{to_id}`
  - Validations: same project, no self‑link.

- Remove Entry
  - `DELETE /api/v1/projects/{project_id}/world/locations/{id}/entries/{to_id}`

- Set Exit
  - `PUT /api/v1/projects/{project_id}/world/locations/{id}/exit`
  - Body: `{ "exit_location_id": "<uuid>" }`
  - Validations: same project, no self‑link; single exit (overwrites).

- Clear Exit
  - `DELETE /api/v1/projects/{project_id}/world/locations/{id}/exit`

- Set Default Entry
  - `PUT /api/v1/projects/{project_id}/world/locations/{id}/default-entry`
  - Body: `{ "entry_location_id": "<uuid>" }`
  - Validations: container only; target must be a direct child of the container.

- Clear Default Entry
  - `DELETE /api/v1/projects/{project_id}/world/locations/{id}/default-entry`

### Deprecation & Cleanup
- Mark `/world/connections` endpoints as deprecated.
- Keep read compat via synthesized `connections` in overview during transition.
- After FE migration, remove:
  - `/world/connections` endpoints
  - `LocationConnection*Serializer`, admin registration, and the `LocationConnection` model (post data migration).

### Data Migration (Optional)
If legacy `LocationConnection` data exists:
- For each `A→B`, add `B` to `A.entry_connections`.
- Leave `exit_connection` null unless you have deterministic inference rules.

### Errors & Auth
- Reuse existing JWT + project ownership checks.
- 400 on invalid operations (self‑link, default entry not a child), 403/404 on access issues, 500 otherwise.

---

## Frontend Changes

### Files
- `src/services/worldService.ts`
- `src/components/world/ReactFlowCanvas.tsx`
- `src/components/project/ProjectWorldTab.tsx`
- (UI cleanup) `src/components/world/ConnectionPropertiesPanel.tsx`

### Types & Service Layer
Extend `WorldLocation` to include:
- `entry_connection_ids?: string[]`
- `exit_connection_id?: string | null`
- `default_entry_location_id?: string | null`

Add new methods to `worldService`:
- `addEntry(projectId, fromId, toId, token)` → `POST /entries/:to_id`
- `removeEntry(projectId, fromId, toId, token)` → `DELETE /entries/:to_id`
- `setExit(projectId, id, exitId, token)` → `PUT /exit { exit_location_id }`
- `clearExit(projectId, id, token)` → `DELETE /exit`
- `setDefaultEntry(projectId, containerId, childId, token)` → `PUT /default-entry { entry_location_id }`
- `clearDefaultEntry(projectId, containerId, token)` → `DELETE /default-entry`

Deprecate and remove callers of:
- `createConnection`, `deleteConnection` (prior `/world/connections`)

### Edge Rendering
Build edges client‑side from locations (preferred), or consume backend‑derived `connections` while transitioning:
- Entries → `from → entry` edge: blue `#3b82f6`, solid, bidirectional arrows.
- Exit → `from → exit` edge: green `#10b981`, dashed, unidirectional arrow.
- Default entry → purple `#8b5cf6` dotted hint edge from container → default child, or show a container badge “Default: ChildName”.
- Deduplicate edges with a `Set` (e.g., `from-to` keys).

### Interaction Modes
Add a toolbar mode selector:
- Entry (default): drag A→B → `addEntry(A, B)`
- Exit: click source A then target B → `setExit(A, B)`; clear via context action.
- Default Entry: context action on a child (or container inspector dropdown) → `setDefaultEntry(container, child)`; provide clear action.

Edge deletion mapping:
- Entries → `removeEntry(from, to)`
- Exit → `clearExit(from)`
- Default entry → `clearDefaultEntry(container)`

### UI Cleanup
- Remove or repurpose `ConnectionPropertiesPanel.tsx` (per‑edge visuals/metrics no longer persisted).
- Add a legend explaining colors and semantics for entries/exit/default entry.

### Validation (FE Hints)
- Prevent self‑links on entries and exits.
- Default entry only to direct child; show a warning/toast on invalid target.

---

## Example Payloads

### World Overview (truncated)
`GET /api/v1/projects/<pid>/world`

```
{
  "project_id": "...",
  "locations": [
    {
      "id": "...",
      "name": "...",
      "entry_connection_ids": ["...", "..."],
      "exit_connection_id": "...",
      "default_entry_location_id": "..."
    }
  ],
  "connections": [
    {
      "id": "<from>__to__<to>",
      "from_location_id": "...",
      "to_location_id": "...",
      "connection_type": "path|exit|default_entry",
      "line_style": "solid|dashed|dotted",
      "line_color": "#3b82f6|#10b981|#8b5cf6",
      "arrow_style": "bidirectional|unidirectional"
    }
  ],
  "location_count": 1,
  "connection_count": 1
}
```

---

## Testing

### Backend
- Unit tests for each new endpoint (happy paths + validations):
  - add/remove entry
  - set/clear exit
  - set/clear default entry (child constraint)
- Integration test for world overview with new fields and derived connections.

### Frontend
- Unit tests for `worldService` methods (mock fetch).
- Edge builder tests: locations → edges (type, color, arrow style).
- E2E tests:
  - Drag to create entry → blue edge → persists after reload.
  - Set exit → green dashed edge → only one exit per location.
  - Set default entry → purple dotted hint or badge → invalid target shows warning.

---

## Rollout Plan

### Phase 1 (Compatibility)
- API returns new fields and derived `connections`.
- FE adds new service methods and switches create/delete flows to new endpoints.
- FE may still render edges from `connections` while builder from `locations` is introduced.

### Phase 2 (Finalize)
- FE renders edges entirely from `locations` fields (ignore `connections`).
- Remove or repurpose the per‑connection properties panel.

### Phase 3 (Cleanup)
- Remove old `/world/connections` endpoints and serializers.
- Remove `LocationConnection` model/admin after data migration.

---

## Acceptance Criteria
- Entry create/delete calls new endpoints and correctly updates edges (blue, solid, bidirectional) and persists.
- Exit set/clear calls new endpoints and correctly updates edges (green, dashed, unidirectional) and persists; only one exit allowed.
- Default entry set/clear calls new endpoints and shows dotted purple hint (or container badge) and persists; only direct child allowed.
- World overview `locations` include `entry_connection_ids`, `exit_connection_id`, `default_entry_location_id`.
- No FE usage of `/world/connections` remains.
- Docs and legends reflect new semantics and colors.

---

## Open Questions
- Do we need persisted per‑edge visuals/metrics? If yes, introduce a through‑model (e.g., `LocationEntry`) to hold them; otherwise, keep visuals client‑only and defaulted by type.
- Preferred visualization for default entry: dotted hint edge, container badge, or both (toggleable)?

