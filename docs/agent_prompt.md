# Agent Prompt: Authoring TOML Templates for twee_comprehensive v1

Purpose: A concise, copy‑pasteable prompt/checklist for any agent (or human) authoring game TOML files that feed the Django models and the twee_comprehensive v1 generator.

Scope: Template v0.2 — project/time, player, NPCs, locations (world designer), and story canvases (triggers, schedules, nodes, exit blocks). Everything here reflects the actual v1 generator and model rules.

---

## 1) Template Schema (TOML v0.2)

- Top‑level keys: `schema_version`, `project`, `time`, `player`, `npcs[]`, `locations[]`, `starting_canvas?`, `canvases[]?`.
- Identifiers:
  - All `id` values are lowercase `snake_case`, unique within their section.
  - Use short, stable slugs — these become stable references.
- Project
  - `project.id` (slug), `project.title`, `project.description`.
- Time
  - `enabled` (bool), `starting_hour` 0–23, `starting_day` in Monday..Sunday, `starting_week` ≥1.
- Player
  - `id`, `name`, `description`, `core_traits` (dict of numbers), `flag_keys` (string list).
- NPCs
  - Array of `{ id, name, description, core_traits, flag_keys }`.
- Locations (World Designer)
  - `{ id, name, description, is_container, parent, entry_from, default_entry, navigation_order[] }`.
- Story (optional)
  - `starting_canvas`: slug of a canvas from `canvases[]` to set as the project starting canvas.
  - `canvases[]`:
    - `id`, `name`, `description?`
    - `trigger?`:
      - `location`: location slug (must exist)
      - `is_active?` (bool, default true)
      - `is_repeatable?` (bool, default true)
      - `max_triggers_per_day?` (int|null)
      - `conditions?`: conditions v1.0 (see §5)
      - `schedules[]?`: `{ weekdays: [0..6], start_time: "HH:MM", end_time?: "HH:MM" }`
    - `nodes[]`:
      - `id`, `name`, `blocks[]` (BlockNote), `exit_block` (see §4)
    - `connections[]?` (used by `exit_block.type = "location"`): `{ source: nodeId, target: nodeId, connection_type?: "default" }`

---

## 2) World Designer Rules (Django models)

Think in terms of containers (can hold child locations) and normal locations.

- Parent/Hierarchy
  - `parent` references the container which owns this location, or empty for top‑level.
  - Parenting defines what is “inside” a container and sets hierarchy.
- Single‑entry navigation via `entry_from`
  - A location is entered from exactly one other location using `entry_from`, or empty if selectable from the global Navigation.
- default_entry (containers only)
  - If a container has `default_entry`, entering the container auto‑redirects to that child.
  - The default entry location MUST NOT define `entry_from` (automatic container entry).
- Cross‑container rule (strict)
  - Disallows `entry_from` that crosses container boundaries unless:
    1) The target is the parent’s default entry location, or
    2) It’s an “outer connection” to a container that has a default entry and the child is NOT a descendant (rare; use hub patterns instead).
- Descendant restriction
  - If a container has a `default_entry`, none of its descendants may set `entry_from` to that container. Descendants must route via the default entry or other siblings in the same container.

---

## 3) Story Canvases (Triggers, Nodes, Connections)

- Inclusion
  - v1 includes: starting canvas; any canvas with a trigger; canvases referenced via `choices[].targetType = "node"`.
- Triggers (location + gate)
  - `trigger.location` ties a canvas to a world Location page. Triggers also inherit up container hierarchy (a child can show triggers defined on its parent containers).
  - Schedules: v1 evaluates the first schedule only (OR across multiple is not implemented in v1).
  - Conditions: v1.0 format (see §5) checked against `$player` and `$npcs`.
  - Repeatability: `is_repeatable`, `max_triggers_per_day` enforced with a per-day history.
- Nodes
  - BlockNote `blocks[]` supported types: `heading`, `paragraph`, `dialog` (props: `speaker`, `npcName`), `image` (props: `url`, `alt`, `caption`), `video` (props: `url`, `poster?`).
  - Each node becomes a passage. For the first node, v1 records the trigger as fired.
- Connections
  - Used only when `exit_block.type = "location"`. v1 follows the first outgoing connection to decide the next node; if none, it returns to the trigger location or a specific location per config.

---

## 4) Exit Blocks (Choices, Effects, Conditions)

- `exit_block.type`: `"location" | "choices"` (default `"location"`).
- Location type
  - `text`: link label (default "Continue").
  - `config.destinationType`: `"trigger"` (return to trigger location) or `"specific"` + `config.locationId` (location slug).
  - `config.time_progression_minutes?`: minutes to advance; default 3 if missing/invalid.
  - If a connection exists, v1 follows the first outgoing connection; otherwise it uses `destinationType`.
- Choices type
  - `config.default_time_progression?`: default minutes per choice.
  - `choices[]` entries:
    - `text`: link label (default "Continue").
    - `targetType`: `"trigger" | "location" | "node"`.
    - If `location`: `locationId` = location slug (import rewrites to UUID).
    - If `node`: `nodeId` = node slug — allow `canvasId.nodeId` or local `nodeId`.
    - `time_progression_minutes?`: override minutes.
    - `effects[]` (traits): `{ targetType: "player"|"npc", npcId?, trait, op: "add"|"set", value, clamp?, cap? }`.
    - `flagEffects[]` (flags): `{ targetType: "player"|"npc", npcId?, flag }` (sets true).
    - `conditions?`: conditions v1.0 (see §5). If present, the choice link is wrapped in a runtime `<<if>>`.

---

## 5) Conditions v1.0 (exact evaluator in v1)

- Structure: `{ version: "1.0", logic: "AND"|"OR", items: [ ... ] }`.
- Items:
  - Flag: `{ type: "flag", subject: "player"|"npc", flag_key, operator: "exists"|"is_true"|"is_false", character_id? }`.
  - Trait: `{ type: "trait", subject: "player"|"npc", trait_key, operator: "eq"|"ne"|"gt"|"gte"|"lt"|"lte"|"in"|"not_in"|"contains"|"not_contains", value, character_id? }`.
- Notes:
  - Missing or different `version` is treated as satisfied.
  - Numeric operators coerce values to numbers; string/array operators supported for `contains` variants.

---

## 5.1) Strict Trait Declaration Rule (UI + Import)

- Always declare any trait you reference in triggers or choice effects in the character’s `core_traits` with a default value.
  - Example: if a trigger checks `player.study > 10` or an effect adds to `study`, include `study = 0` in the Player’s `core_traits`.
  - For NPC trait conditions/effects, ensure the referenced NPC defines that trait key in its `core_traits`.
- Why: The web UI builds trait pickers from the character’s declared `core_traits`. Missing keys render as blank in the editor and are rejected by import validation.
- Enforcement: The template import now fails validation if a trait is used in conditions/effects but not declared on the corresponding character.

---

## 6) Generator Behaviors (twee_comprehensive v1)

- Default entry redirect
  - If a container has `default_entry`, you never see the container page; you land on the default entry’s page.
- Destinations list
  - On any location page, the “Available destinations” list only shows locations where `entry_from == current_location`.
  - It does NOT list destinations of the parent container.
- Exit link (leaving containers)
  - A location shows an “Exit [container]” option only under these conditions:
    - Container has NO default entry: any child with `entry_from = container` can exit.
    - Container HAS default entry: ONLY the default entry location can exit back to the container’s `entry_from` target.
  - If the container itself is a default entry of its parent, it cannot have `entry_from`, so its default entry has no Exit link — plan hub flows accordingly.

---

## 7) Authoring Patterns (Do This)

- Hub‑as‑default (recommended for switching siblings)
  - Make the container’s default entry a hub page that lists sibling destinations.
  - Example: Mall — Entrance is default; floors have `entry_from = mall_entrance`; entrance lists both floors in `navigation_order`.
- Floor/Area default with inner content
  - If you choose a floor as the default entry, it should lead to inner content (shops, rooms) where each child sets `entry_from` to the floor’s default entry.
  - You won’t see sibling floors here; switching requires exiting to a hub.
- Nested containers
  - For a nested container with default entry (e.g., building → floor → atrium), route within the same parent. Default entries never set `entry_from`.
- navigation_order
  - List only direct destinations where `entry_from == this`.
  - Unlisted valid destinations still appear (appended) — `navigation_order` just controls order.

---

## 8) Anti‑Patterns (Don’t Do This)

- Don’t set `entry_from` on a default entry location (will fail validation).
- Don’t set `entry_from` on descendants to their ancestor container if that ancestor has a default entry — route via the default entry instead.
- Don’t cross container boundaries via `entry_from` unless it’s the allowed outer connection to a container with a default entry (rare — use hubs).
- Don’t put unrelated destinations in `navigation_order` — each must have `entry_from == this`.

---

## 9) Minimal Examples (World)

- Top‑level hub → destinations
```toml
[[locations]]
id = "town_square"; name = "Town Square"; is_container = false
parent = ""; entry_from = ""; default_entry = ""
navigation_order = ["inn", "market"]

[[locations]]
id = "inn"; name = "Inn"; is_container = false
parent = ""; entry_from = "town_square"; default_entry = ""; navigation_order = []
```

- Container with default entry (hub‑as‑default)
```toml
[[locations]]
id = "mall"; name = "Mall"; is_container = true
parent = ""; entry_from = "town_square"; default_entry = "mall_entrance"; navigation_order = []

[[locations]]
id = "mall_entrance"; name = "Mall — Entrance"; is_container = false
parent = "mall"; entry_from = ""; default_entry = ""; navigation_order = ["floor1", "floor2"]

[[locations]]
id = "floor1"; name = "Mall — Floor 1"; is_container = true
parent = "mall"; entry_from = "mall_entrance"; default_entry = "floor1_atrium"; navigation_order = []
```

---

## 10) Minimal Examples (Story)

- Minimal canvas with trigger, nodes, choices
```toml
starting_canvas = "intro_canvas"

[[canvases]]
id = "intro_canvas"
name = "Welcome"

  [canvases.trigger]
  location = "town_square"
  is_active = true
  is_repeatable = false
  [[canvases.trigger.schedules]]
  weekdays = [0,1,2,3,4,5,6]
  start_time = "08:00"
  end_time = "22:00"

  [[canvases.nodes]]
  id = "n1"
  name = "Opening"
  blocks = [ { type = "paragraph", content = "You arrive..." } ]
  exit_block = { type = "choices", config = { default_time_progression = 5 }, choices = [
    { text = "Go to market", targetType = "location", locationId = "market" },
    { text = "Think", targetType = "node", nodeId = "intro_canvas.n2" }
  ] }

  [[canvases.nodes]]
  id = "n2"
  name = "Thinking"
  blocks = [ { type = "paragraph", content = "You ponder..." } ]
  exit_block = { type = "location", text = "Back", config = { destinationType = "trigger" } }
```

---

## 11) Validation & Import Checks

- Dry‑run (no DB writes):
  - `python manage.py create_project_from_template --file <path> --owner-id <UUID> --dry-run`
- Common validation errors and fixes:
  - “default_entry ... must not define entry_from” → clear `entry_from` on the default entry location.
  - “navigation_order includes X which is not a destination” → ensure `entry_from == this` for each listed slug.
  - “Cannot create entry from different container ...” → route via default entry, or use a hub.
  - “trigger.location not found” / bad schedule formats → fix slugs and times.
  - `choices[].nodeId` unresolved → use local `nodeId` or fully‑qualified `canvasId.nodeId`.

Importer guarantees:
- World: Parents are set and saved (validated) before `entry_from`/`default_entry`.
- World: `navigation_order` saved after all links are established.
- Story: Canvases → Triggers/Schedules → Nodes → Connections → Rewrite `exit_block` references (slugs → UUIDs).

---

## 12) Quick Checklist

- IDs: lowercase snake_case, unique.
- Default entries: no `entry_from`.
- Descendants of a container with default entry: never `entry_from` to the container; route via default entry or same‑parent siblings.
- `navigation_order`: only direct destinations.
- For multi‑sibling switching: use a hub page (often the container’s default entry) to list siblings.
- For story:
  - Trigger locations must exist; first schedule only is active in v1.
  - For `choices`: provide `locationId` (location slug) or `nodeId` (local or `canvasId.nodeId`).
  - Effects/flags use shapes listed in §4.
  - Conditions use v1.0 format from §5.

---

## 13) Glossary

- Container: A location that can contain child locations (`is_container = true`).
- Default entry: A child location a container auto‑redirects to when entered.
- Hub: A location (often default entry) whose `navigation_order` lists same‑parent destinations.
- Destination: A location whose `entry_from` equals the current location.
- Trigger: A canvas activation bound to a world location; may include schedules, conditions, repeat rules.
- Exit block: Node continuation rule; either a single location jump or a set of choices with effects/conditions.

---

## 14) Authoring Prompt (copy/paste for agents)

“You are authoring a TOML template for twee_comprehensive v1 (schema v0.2). Follow these rules strictly:
- Include: `project`, `time`, `player`, `npcs`, `locations`, and optionally `starting_canvas`, `canvases`.
- All ids are lowercase snake_case and unique.
- World:
  - Containers with `default_entry`: the default entry must not have `entry_from`.
  - Descendants of such containers never set `entry_from` to the container — route via the default entry or siblings.
  - On any location, only list `navigation_order` items that have `entry_from = this`.
  - Use hub pages to switch between sibling containers (e.g., mall entrance lists floors).
- Story:
  - Triggers: `trigger.location` must be a valid location; only the first schedule is considered in v1.
  - Nodes: author BlockNote `blocks[]` using supported types.
  - Exit blocks:
    - For `type = location`: use `config.destinationType = trigger|specific` (+ `locationId`).
    - For `type = choices`: each choice sets `targetType` and either `locationId` (location slug) or `nodeId` (local or `canvasId.nodeId`).
    - Use `effects`/`flagEffects` to update traits/flags, and `conditions` (v1.0) to gate choices.
- Validate with the management command in dry‑run mode and fix all reported issues before import.”
