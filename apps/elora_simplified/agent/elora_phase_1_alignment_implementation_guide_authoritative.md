# Elora Phase‑1 Alignment — Implementation Guide (Authoritative)

**Purpose:** Align the codebase **exactly** to Phase‑1 of the Elora ReAct workflow. No extra features. Implement only what is specified below.

---

## 0) Phase‑1 Surface Area (Authoritative)

**Canonical tools (exactly 4):**
1. `describe_canvas` — **read_only**
2. `search_nodes` — **read_only** (must be **canvas‑scoped**)
3. `create_node` — **low_write** (Phase‑1 rule: **one node per canvas**, overwrite flow)
4. `delete_canvas` — **high_write** (preview via **dry‑run** prior to execution)

> All other legacy tools remain available in the app but **must be hidden from the Planner** in Phase‑1.

**TAU thresholds (fixed):**
- `TAU_LOW = 0.60`
- `TAU_HIGH = 0.80`
- `ASK_MAX_QUESTIONS = 2`

---

## 1) Component Responsibilities (Must Match)

- **Planner** (`apps/elora_simplified/services/planner.py`)
  - Single owner of **tool selection** *and* **argument formation**.
  - Uses Tool Manifest for arg validation/defaults and destructiveness (read from manifest; do **not** infer).
  - Performs **read‑first entity resolution** using grounded context (never regex→UUID shortcuts).
  - Consumes optional `tool_candidates` hints to restrict selection (still validated by manifest + context).

- **Policy Engine** (`apps/elora_simplified/services/phase1_policy_engine.py`)
  - **Safety decisions only**; no tool selection, no arg changes.
  - Deterministic decision table: `read_only→proceed`, `low_write→confirm`, `high_write→dry_run`.
  - Applies ASK cap (`ASK_MAX_QUESTIONS`).

- **Tool Manifest Registry** (`apps/elora_simplified/services/tool_manifest_registry.py`)
  - **Single source of truth** for tool schemas and destructiveness.
  - Returns **only** the Phase‑1 tools to the Planner.

- **ReAct Workflow** (`apps/elora_simplified/agent/react_workflow.py`)
  - Orchestrates phases: `GROUND_CONTEXT → PLAN_STEP → SAFETY_GATE → EXECUTE_STEP → VALIDATE → SYNTHESIZE_RESPONSE` (finish) with `ASK_USER` / `AWAIT_CONFIRMATION` branches as needed.
  - Executes **dry‑run preview** when Policy verdict is `dry_run` (workflow concern, not a tool arg).

- **Tool Adapters** (`apps/elora_simplified/services/phase1_tool_adapters.py`)
  - Implement the 4 canonical tools with Phase‑1 constraints (one‑node rule, trigger metadata, etc.).

---

## 2) Tool Manifest — Exact Schemas & Visibility

**Visibility:** `get_available_tools()` **must** return *only* these four.

### 2.1 `describe_canvas` (read_only)
- **Args schema**: `{ "canvas_id": "string?" }` (optional)
- **Semantics**:
  - No args → return **project summary**: list of canvases with trigger metadata (location, weekdays, start_time, end_time) and `node_count`.
  - With `canvas_id` → return **detail** for that canvas with the same trigger fields and `node_count`.

### 2.2 `search_nodes` (read_only, **canvas‑scoped**)
- **Args schema**: `{ "canvas_id": "string", "query": "string" }` (**both required**)
- **Semantics**: hybrid search **within the given canvas only**; return ranked nodes with `{node_id, title, content?, score}`.

### 2.3 `create_node` (low_write)
- **Args schema**:
  ```json
  {
    "canvas_id": "string",
    "title": "string",
    "content": "string",
    "overwrite_confirmed": { "type": "boolean", "default": false }
  }
  ```
- **Semantics**: Enforce **one node per canvas** in Phase‑1.
  - If node exists and `overwrite_confirmed=false`: return `requires_overwrite=true` + `dry_run_info` (preview of change).
  - After user confirms, Planner re‑issues with `overwrite_confirmed=true` to execute overwrite.

### 2.4 `delete_canvas` (high_write)
- **Args schema**: `{ "canvas_id": "string" }`
- **Semantics**: Deleting a canvas removes the canvas, its single node (if any), the 1:1 trigger and schedules. Preview is produced by **workflow dry‑run path**, not via tool arg.

> **Do not** expose `dry_run` as a public tool argument in Phase‑1.

---

## 3) Planner — Deterministic Selection & Arg Formation

### 3.1 Deterministic Routing Table (code, not prompts)
Implement in `planner.py`:

| Pattern (normalized) | Preconditions (from grounded context) | Tool | Arg Formation | Confidence |
|---|---|---|---|---|
| `^show|list|describe|explain` + canvas ref | `canvas_id` resolved via §3.2 | `describe_canvas` | `{canvas_id}` | 0.85 (exact), 0.75 (single fuzzy) |
| `^show|list|describe|explain` (no ref) | none | `describe_canvas` | `{}` | 0.70 |
| `^create|add|write` + (node|story|content)` | `canvas_id` resolved; check canvas has 0 or ≥1 nodes | `create_node` | if 0: set `{canvas_id, title, content}`; if ≥1: same + rely on adapter to return preview | 0.82 |
| `^delete|remove` + canvas ref | `canvas_id` resolved | `delete_canvas` | `{canvas_id}` | 0.80 |
| `^search|find|look for` + text | `canvas_id` resolved | `search_nodes` | `{canvas_id, query}` | 0.78 |
| fallback | none | `describe_canvas` | `{}` | 0.65 |

- The Planner **may** receive `tool_candidates` (restrictor). If present, selection must be from that subset **and** still satisfy the preconditions above. If no match, fallback to `describe_canvas {}`.

### 3.2 Entity Resolution (read‑first, cache‑based)
**Never** use regex→UUID or direct DB lookup from the Planner.

1. **Use grounded cache** from `GROUND_CONTEXT` (`describe_canvas {}` ran already, unless first turn). Cache includes canvas list `{id,name}`.
2. Normalize: lowercase, trim, collapse spaces, drop trailing word `canvas`.
3. Ladder:
   - **Exact** normalized match → accept (confidence ≥ `TAU_HIGH` 0.80).
   - **Single fuzzy** (startsWith/contains) → accept but set confidence < `TAU_HIGH` (e.g., 0.75) → Policy may ASK.
   - **>1 candidates** → prepare ASK with at most 5 names.
   - **0 candidates** → proceed with summary, or ASK once if user’s phrasing strongly implies a specific target.
4. If cache missing/stale: plan `describe_canvas {}` first, then resolve next step.
5. When resolved, **always pass `canvas_id`** to tools.

### 3.3 Argument Formation & Validation
- Apply manifest defaults (e.g., `overwrite_confirmed=false`).
- Validate types and required fields via manifest before returning `StepPlan`.
- Set `StepPlan.destructiveness = manifest.get_destructiveness(tool)` (do **not** infer).

### 3.4 Confidence & ASK discipline
- Exact match → ≥0.80; single fuzzy → 0.70–0.79; heuristic/no entity → ≤0.75.
- The Planner **does not** ASK; it returns a plan with confidence. Workflow/Policy handles ASK vs proceed using TAU + ASK cap.

---

## 4) Policy Engine — Safety Only

Location: `services/phase1_policy_engine.py`

- Deterministic decision table:
  - `read_only` → `proceed`
  - `low_write` → `confirm`
  - `high_write` → `dry_run`
- Enforce `ASK_MAX_QUESTIONS = 2` (workflow tracks the count; Policy/Workflow decide to proceed or synthesize after cap).
- No tool selection, no argument mutation.

---

## 5) ReAct Workflow — Phases & Transitions

Location: `agent/react_workflow.py`

### 5.1 Phase Order
`GROUND_CONTEXT → PLAN_STEP → SAFETY_GATE → EXECUTE_STEP → VALIDATE → SYNTHESIZE_RESPONSE (finish)`

- `ASK_USER` branch when Policy requires clarification/confirmation.
- `AWAIT_CONFIRMATION` branch for confirm/dry‑run approvals.

### 5.2 GROUND_CONTEXT
- Call `describe_canvas {}` (if cache empty/stale) to build `state.conversation_context.canvas_summary`.
- Persist `{id,name}` + trigger summary (location, weekdays, start_time, end_time) + `node_count`.

### 5.3 SAFETY_GATE
- Use Policy decision table.
- `dry_run` verdict: execute **preview** path (see 5.5) and wait for user confirmation.

### 5.4 VALIDATE
- Basic success/failure check.
- For **writes**, run trigger consistency checks (weekday 0–6, start<end, location exists). Record warnings (do not block unless hard error).
- Gate to `SYNTHESIZE_RESPONSE` if confidence ≥ `TAU_HIGH` or if result is final by nature (e.g., delete/overwrite completed).

### 5.5 Dry‑Run Preview Path (workflow concern)
- On `dry_run` for `delete_canvas` (and overwrite preview via `create_node` adapter response):
  - Show preview payload (impacted items: canvas, node, trigger, schedules) and ask for confirmation.
  - On approval: re‑plan or continue with the same plan to **execute**.
  - On denial: return to `PLAN_STEP`.

### 5.6 SYNTHESIZE_RESPONSE (Phase‑1 finish)
- After successful **read** with confidence ≥ `TAU_HIGH`, or after **write** that completed, synthesize and **finish the turn**. Do not loop again.

---

## 6) Tool Adapters — Required Behaviors

Location: `services/phase1_tool_adapters.py`

### 6.1 `describe_canvas(canvas_id?: str)`
- No args: project **summary** list with `id,name,node_count,trigger{location{name},weekdays[],start_time,end_time}`.
- With `canvas_id`: **detail** object with the same fields for that canvas.

### 6.2 `search_nodes(canvas_id: str, query: str)`
- Enforce **canvas‑scoped** search; do not return nodes from other canvases.

### 6.3 `create_node(canvas_id: str, title: str, content: str, overwrite_confirmed: bool=false)`
- If canvas has 0 nodes → create and return success.
- If ≥1 node and `overwrite_confirmed=false` → return `{success:false, requires_overwrite:true, dry_run_info:{existing_title, existing_excerpt, new_title, new_excerpt, canvas_name}}` plus a short `ask_question` string.
- If ≥1 node and `overwrite_confirmed=true` → overwrite existing node and return success.

### 6.4 `delete_canvas(canvas_id: str)`
- Real deletion when workflow authorizes execution.
- Provide an internal helper to generate **impact preview** (used by workflow on `dry_run`): list of items to be deleted (canvas, node, trigger, schedules) with counts/ids.

---

## 7) Entity Resolution — Contract

- Resolution is always via **grounded read data** (cache from `describe_canvas {}`), never regex→UUID shortcuts.
- Planner must always pass **IDs** to tools once resolved.
- ASK only when multiple candidates or none; cap total ASK at 2.

---

## 8) Minimal Logging (Phase‑1)

- Log: phase transitions, selected tool + args (validated), policy verdict, tool result success/failure, and preview payloads.
- Avoid verbose token/cost logs in Phase‑1 alignment tasks.

---

## 9) Acceptance Criteria (must pass)

1. **Describe All Canvases** → Planner selects `describe_canvas {}`; response lists canvases with trigger metadata.
2. **Explain Specific Canvas** → Entity resolution via cache → `describe_canvas {canvas_id}`; confidence ≥ `TAU_HIGH` on exact match; workflow synthesizes and finishes.
3. **Create Node on Empty Canvas** → Planner selects `create_node`; success on first attempt; synthesize and finish.
4. **Create Node Overwrite Flow** → First call returns preview (requires_overwrite); confirmation leads to overwrite; synthesize and finish.
5. **Delete Canvas Flow** → Planner selects `delete_canvas`; Policy→`dry_run`; preview → confirm → delete; synthesize and finish.
6. **Search Within Canvas** → Planner selects `search_nodes {canvas_id, query}`; results are canvas‑scoped.
7. **Planner Confinement** → No legacy tools invoked by Planner; only the 4 canonical tools appear in logs.

---

## 10) Code Diffs Checklist (Do These Exactly)

- **Manifest** (`tool_manifest_registry.py`)
  - `describe_canvas.args_schema = {"canvas_id": "string?"}` (remove `canvas_name`).
  - `search_nodes.args_schema` requires both `canvas_id` and `query`.
  - Keep `create_node.overwrite_confirmed` with `default=false`.
  - `delete_canvas.args_schema = {"canvas_id": "string"}`.
  - `get_available_tools()` returns only the 4 canonical tools.

- **Planner** (`planner.py`)
  - Implement routing table (Section 3.1) and entity resolution ladder (Section 3.2).
  - Always pass IDs after resolution.
  - Apply manifest defaults and validate args before returning `StepPlan`.
  - Respect `tool_candidates` when provided.

- **Policy** (`phase1_policy_engine.py`)
  - Keep deterministic table; enforce ASK cap; no tool/arg mutation.

- **Workflow** (`react_workflow.py`)
  - Ensure `GROUND_CONTEXT` runs `describe_canvas {}` when cache missing/stale.
  - Implement `dry_run` preview handling in workflow (not as tool arg).
  - Gate `SYNTHESIZE_RESPONSE` on `confidence ≥ TAU_HIGH` for reads or on successful writes.

- **Adapters** (`phase1_tool_adapters.py`)
  - Implement exact behaviors in Section 6, including overwrite preview and delete impact preview helper.

---

## 11) Out‑of‑Scope (Do Not Implement in Phase‑1)

- No character/trait tools.
- No global (project‑wide) node search; `search_nodes` is canvas‑scoped only.
- No additional tools, no metrics dashboards, no learning/telemetry loops.
- No multi‑step batch planning; Planner plans **one step** at a time.

---

## 12) Ready‑to‑Implement Summary

1) Update **Manifest** to the exact schemas and visibility.
2) Implement **Planner** routing + resolution + arg validation per manifest.
3) Keep **Policy** safety‑only with ASK cap.
4) Ensure **Workflow** handles dry‑run previews and finishes after synthesize.
5) Make **Adapters** enforce Phase‑1 rules (one‑node, previews, canvas‑scoped search).
6) Run the 7 acceptance tests; all must pass without adding any extra features.

**End of Authoritative Phase‑1 Alignment Guide.**

