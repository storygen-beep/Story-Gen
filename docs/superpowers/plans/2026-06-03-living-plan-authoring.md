# Living-Plan Sequential Authoring Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace blind one-shot game generation with an interactive `/author-game` skill that runs a one-time skeleton/roadmap setup, then authors the game one beat at a time with validate-after-every-beat, backed by a persistent ledger.

**Architecture:** A Claude Code skill at `.claude/skills/author-game/` orchestrates two modes (setup, continue) using `AskUserQuestion` for steering and on-disk state. State lives in three artifacts per game: `design_book.md` (intent), `authoring_state.json` (the ledger — plan + structure registry + bookkeeping), and the existing `toml_phases/*.toml` (built content). A small stdlib-only Python helper (`ledger.py`) owns all ledger reads/writes and the reconcile/anti-drift logic; everything else is prose (skill + restructured `prompts_v2` corpus). The existing `merge_toml_phases.py` + `package_from_toml` build pipeline is reused unchanged.

**Tech Stack:** Python 3.12 (stdlib `json` + `tomllib` only for the helper), pytest for the helper tests, Markdown for the skill + corpus, existing Django `package_from_toml` management command + `scripts/merge_toml_phases.py` for builds.

**Spec:** `docs/superpowers/specs/2026-06-03-living-plan-authoring-design.md`

**Prerequisite for every task:** the repo venv is active —
```bash
cd /Users/a0000/Desktop/Desktop_Archive_Backup/story_gen/story_gen_web_app/story_gen_django
source venv/bin/activate   # Python 3.12.11
```

---

## File Structure

**New — the skill:**
- `.claude/skills/author-game/SKILL.md` — the orchestration skill (frontmatter + mode dispatch + setup + continue).
- `.claude/skills/author-game/references/ledger-schema.md` — documented `authoring_state.json` shape.
- `.claude/skills/author-game/references/setup-interview.md` — the setup question set + how to ask.
- `.claude/skills/author-game/references/beat-authoring.md` — the per-beat loop + the doctrine self-audit checklist.
- `.claude/skills/author-game/scripts/ledger.py` — stdlib-only ledger ops (init/load/save/add_structure/add_beat/mark_beat/reconcile).
- `.claude/skills/author-game/scripts/test_ledger.py` — pytest tests for `ledger.py`.

**Modified — the corpus (`prompts_v2/`):**
- `prompts_v2/stages/01_game_book_prompt.md` — refit as the setup-interview spec.
- `prompts_v2/stages/02_toml_generation_prompt.md` — refit as the per-beat authoring spec.
- One doctrine file gains a short structure-discipline note (chosen in Task 6).
- `prompts_v2/COMPREHENSIVE_SYSTEM_REFERENCE.md` — regenerated.

**Created at runtime per game (not in this plan, but the schema is fixed here):**
- `games/<slug>/design_book.md`, `games/<slug>/authoring_state.json`.

---

## A note on running the helper tests

`ledger.py` is stdlib-only and has no Django dependency, but the repo root registers `pytest-django`. Run the helper tests with the Django plugin disabled so no settings/DB setup is attempted:

```bash
python -m pytest .claude/skills/author-game/scripts/test_ledger.py -p no:django -q
```

---

## Phase 1 — Ledger schema + helper (TDD)

### Task 1: Ledger schema reference doc

**Files:**
- Create: `.claude/skills/author-game/references/ledger-schema.md`

- [ ] **Step 1: Write the schema doc**

Create the file with this exact content:

````markdown
# authoring_state.json — ledger schema (v1)

The ledger is the living source of truth for the **plan** and for **what structure exists**.
It is rewritten every authoring turn by `scripts/ledger.py`. Never hand-edit it during a run;
use the helper so reconcile/anti-drift stays correct.

```jsonc
{
  "game_slug": "late_shifts",       // matches games/<slug>/
  "schema_version": 1,
  "book_revision": 1,               // bumped when design_book.md is amended
  "plan": [                         // the living roadmap; ordered, reorderable
    {
      "id": "beat_0001",            // stable, zero-padded, monotonic
      "type": "npc_intro",          // npc_intro|location_reveal|arc_escalation|
                                    //   cross_npc|economic|story_turn|capstone
      "title": "Hank hires the player at the diner",
      "desc": "One-line summary of the beat.",
      "status": "planned",          // planned|active|authored|validated
      "deps": [],                   // beat ids / flags that must exist first
      "target_phase": "5_scenes.toml",
      "introduces": { "locations": [], "npcs": ["hank"], "flags": ["hired_at_diner"] },
      "produced_canvas_ids": [],    // filled when authored; reconcile checks these exist
      "decided_at": null            // turn number when LO chose/locked it
    }
  ],
  "structure_registry": {           // what EXISTS; every amendment is checked against this
    "locations": [], "npcs": [], "flags": [], "schedules": []
  },
  "next_up": [],                    // ordered beat ids proposed next
  "decisions_log": [                // human-readable trail
    { "turn": 1, "note": "...", "book_revision": 1 }
  ]
}
```

**Statuses:** `planned` → `active` (being authored this turn) → `authored` (canvases written)
→ `validated` (passed merge + schema/flag-chain + doctrine self-audit).

**Anti-drift invariant:** nothing in the TOML may reference a location/NPC/flag absent from
`structure_registry`, and adding one is an explicit `add_structure` call (logged). `reconcile`
flags any `validated`/`authored` beat whose `produced_canvas_ids` are missing from the merged TOML.
````

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/author-game/references/ledger-schema.md
git commit -m "docs(author-game): add ledger schema reference"
```

---

### Task 2: `ledger.py` — init / load / save

**Files:**
- Create: `.claude/skills/author-game/scripts/ledger.py`
- Test: `.claude/skills/author-game/scripts/test_ledger.py`

- [ ] **Step 1: Write the failing test**

Create `test_ledger.py`:

```python
import json
from pathlib import Path

import ledger


def test_init_ledger_has_v1_shape():
    led = ledger.init_ledger("demo")
    assert led["game_slug"] == "demo"
    assert led["schema_version"] == 1
    assert led["book_revision"] == 1
    assert led["plan"] == []
    assert led["next_up"] == []
    assert led["decisions_log"] == []
    assert led["structure_registry"] == {
        "locations": [], "npcs": [], "flags": [], "schedules": []
    }


def test_save_then_load_roundtrips(tmp_path):
    led = ledger.init_ledger("demo")
    ledger.save_ledger(tmp_path, led)
    assert (tmp_path / "authoring_state.json").exists()
    back = ledger.load_ledger(tmp_path)
    assert back == led


def test_saved_file_is_pretty_json(tmp_path):
    led = ledger.init_ledger("demo")
    ledger.save_ledger(tmp_path, led)
    text = (tmp_path / "authoring_state.json").read_text()
    assert text.endswith("\n")
    assert json.loads(text)["game_slug"] == "demo"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest .claude/skills/author-game/scripts/test_ledger.py -p no:django -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'ledger'` (or collection error). The test imports `ledger`; add this to the top of `test_ledger.py` BEFORE `import ledger` so the sibling module resolves:

```python
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
```

Re-run; now it should FAIL with `AttributeError`/missing functions.

- [ ] **Step 3: Write minimal implementation**

Create `ledger.py`:

```python
"""authoring_state.json operations for the /author-game skill. Stdlib only."""
import json
from pathlib import Path

LEDGER_NAME = "authoring_state.json"
SCHEMA_VERSION = 1


def ledger_path(game_dir) -> Path:
    return Path(game_dir) / LEDGER_NAME


def init_ledger(game_slug: str) -> dict:
    return {
        "game_slug": game_slug,
        "schema_version": SCHEMA_VERSION,
        "book_revision": 1,
        "plan": [],
        "structure_registry": {
            "locations": [], "npcs": [], "flags": [], "schedules": []
        },
        "next_up": [],
        "decisions_log": [],
    }


def load_ledger(game_dir) -> dict:
    return json.loads(ledger_path(game_dir).read_text())


def save_ledger(game_dir, led: dict) -> None:
    ledger_path(game_dir).write_text(json.dumps(led, indent=2) + "\n")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest .claude/skills/author-game/scripts/test_ledger.py -p no:django -q`
Expected: PASS (3 passed)

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/author-game/scripts/ledger.py .claude/skills/author-game/scripts/test_ledger.py
git commit -m "feat(author-game): ledger init/load/save"
```

---

### Task 3: `ledger.py` — structure registry (add + dup-guard)

**Files:**
- Modify: `.claude/skills/author-game/scripts/ledger.py`
- Test: `.claude/skills/author-game/scripts/test_ledger.py`

- [ ] **Step 1: Write the failing test**

Append to `test_ledger.py`:

```python
import pytest


def test_add_structure_appends():
    led = ledger.init_ledger("demo")
    ledger.add_structure(led, "flags", "hired_at_diner")
    ledger.add_structure(led, "locations", "loc_diner_front")
    assert led["structure_registry"]["flags"] == ["hired_at_diner"]
    assert led["structure_registry"]["locations"] == ["loc_diner_front"]


def test_add_structure_rejects_duplicate():
    led = ledger.init_ledger("demo")
    ledger.add_structure(led, "flags", "hired_at_diner")
    with pytest.raises(ValueError, match="already registered"):
        ledger.add_structure(led, "flags", "hired_at_diner")


def test_add_structure_rejects_unknown_kind():
    led = ledger.init_ledger("demo")
    with pytest.raises(KeyError, match="unknown structure kind"):
        ledger.add_structure(led, "widgets", "x")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest .claude/skills/author-game/scripts/test_ledger.py -p no:django -q`
Expected: FAIL — `AttributeError: module 'ledger' has no attribute 'add_structure'`

- [ ] **Step 3: Write minimal implementation**

Append to `ledger.py`:

```python
def add_structure(led: dict, kind: str, name: str) -> dict:
    reg = led["structure_registry"]
    if kind not in reg:
        raise KeyError(f"unknown structure kind: {kind!r}")
    if name in reg[kind]:
        raise ValueError(f"{kind} {name!r} already registered")
    reg[kind].append(name)
    return led
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest .claude/skills/author-game/scripts/test_ledger.py -p no:django -q`
Expected: PASS (6 passed)

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/author-game/scripts/ledger.py .claude/skills/author-game/scripts/test_ledger.py
git commit -m "feat(author-game): structure registry with dup-guard"
```

---

### Task 4: `ledger.py` — beats (add / get / mark / next_up)

**Files:**
- Modify: `.claude/skills/author-game/scripts/ledger.py`
- Test: `.claude/skills/author-game/scripts/test_ledger.py`

- [ ] **Step 1: Write the failing test**

Append to `test_ledger.py`:

```python
VALID_TYPES = {
    "npc_intro", "location_reveal", "arc_escalation",
    "cross_npc", "economic", "story_turn", "capstone",
}


def test_add_beat_assigns_padded_id_and_queues():
    led = ledger.init_ledger("demo")
    b = ledger.add_beat(led, type="npc_intro", title="Meet Hank",
                        desc="d", target_phase="5_scenes.toml")
    assert b["id"] == "beat_0001"
    assert b["status"] == "planned"
    assert led["plan"][0]["id"] == "beat_0001"
    assert led["next_up"] == ["beat_0001"]
    b2 = ledger.add_beat(led, type="economic", title="Buy home",
                         desc="d", target_phase="0_systems_spec.toml")
    assert b2["id"] == "beat_0002"


def test_add_beat_rejects_bad_type():
    led = ledger.init_ledger("demo")
    with pytest.raises(ValueError, match="invalid beat type"):
        ledger.add_beat(led, type="nonsense", title="t", desc="d",
                        target_phase="5_scenes.toml")


def test_get_beat_returns_same_object():
    led = ledger.init_ledger("demo")
    ledger.add_beat(led, type="npc_intro", title="t", desc="d",
                    target_phase="5_scenes.toml")
    got = ledger.get_beat(led, "beat_0001")
    assert got["title"] == "t"


def test_mark_beat_updates_status_and_dequeues_when_validated():
    led = ledger.init_ledger("demo")
    ledger.add_beat(led, type="npc_intro", title="t", desc="d",
                    target_phase="5_scenes.toml")
    ledger.mark_beat(led, "beat_0001", "active")
    assert ledger.get_beat(led, "beat_0001")["status"] == "active"
    ledger.mark_beat(led, "beat_0001", "validated")
    assert ledger.get_beat(led, "beat_0001")["status"] == "validated"
    assert "beat_0001" not in led["next_up"]


def test_mark_beat_rejects_bad_status():
    led = ledger.init_ledger("demo")
    ledger.add_beat(led, type="npc_intro", title="t", desc="d",
                    target_phase="5_scenes.toml")
    with pytest.raises(ValueError, match="invalid status"):
        ledger.mark_beat(led, "beat_0001", "done")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest .claude/skills/author-game/scripts/test_ledger.py -p no:django -q`
Expected: FAIL — `AttributeError: module 'ledger' has no attribute 'add_beat'`

- [ ] **Step 3: Write minimal implementation**

Append to `ledger.py`:

```python
BEAT_TYPES = {
    "npc_intro", "location_reveal", "arc_escalation",
    "cross_npc", "economic", "story_turn", "capstone",
}
BEAT_STATUSES = {"planned", "active", "authored", "validated"}


def _next_beat_id(led: dict) -> str:
    return f"beat_{len(led['plan']) + 1:04d}"


def add_beat(led, *, type, title, desc, target_phase,
             deps=None, introduces=None) -> dict:
    if type not in BEAT_TYPES:
        raise ValueError(f"invalid beat type: {type!r}")
    beat = {
        "id": _next_beat_id(led),
        "type": type,
        "title": title,
        "desc": desc,
        "status": "planned",
        "deps": list(deps or []),
        "target_phase": target_phase,
        "introduces": introduces or {"locations": [], "npcs": [], "flags": []},
        "produced_canvas_ids": [],
        "decided_at": None,
    }
    led["plan"].append(beat)
    led["next_up"].append(beat["id"])
    return beat


def get_beat(led: dict, beat_id: str) -> dict:
    for beat in led["plan"]:
        if beat["id"] == beat_id:
            return beat
    raise KeyError(f"no beat {beat_id!r}")


def mark_beat(led: dict, beat_id: str, status: str) -> dict:
    if status not in BEAT_STATUSES:
        raise ValueError(f"invalid status: {status!r}")
    beat = get_beat(led, beat_id)
    beat["status"] = status
    if status in ("authored", "validated") and beat_id in led["next_up"]:
        led["next_up"].remove(beat_id)
    return beat
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest .claude/skills/author-game/scripts/test_ledger.py -p no:django -q`
Expected: PASS (11 passed)

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/author-game/scripts/ledger.py .claude/skills/author-game/scripts/test_ledger.py
git commit -m "feat(author-game): beat add/get/mark + next_up queue"
```

---

### Task 5: `ledger.py` — reconcile against the merged TOML (anti-drift)

**Files:**
- Modify: `.claude/skills/author-game/scripts/ledger.py`
- Test: `.claude/skills/author-game/scripts/test_ledger.py`

- [ ] **Step 1: Write the failing test**

Append to `test_ledger.py`:

```python
def _write_toml(tmp_path, body):
    p = tmp_path / "merged.toml"
    p.write_text(body)
    return p


def test_collect_ids_walks_nested_tables(tmp_path):
    toml = _write_toml(tmp_path, """
[[canvases]]
id = "c_meet_hank"
[[canvases]]
slug = "c_diner_hub"
[settings]
title = "demo"
""")
    ids = ledger.collect_toml_ids(toml)
    assert ids == {"c_meet_hank", "c_diner_hub"}


def test_reconcile_ok_when_canvases_present(tmp_path):
    toml = _write_toml(tmp_path, '[[canvases]]\nid = "c1"\n')
    led = ledger.init_ledger("demo")
    ledger.add_beat(led, type="npc_intro", title="t", desc="d",
                    target_phase="5_scenes.toml")
    led["plan"][0]["produced_canvas_ids"] = ["c1"]
    ledger.mark_beat(led, "beat_0001", "validated")
    report = ledger.reconcile(led, toml)
    assert report["ok"] is True
    assert report["drift"] == []


def test_reconcile_flags_missing_canvas(tmp_path):
    toml = _write_toml(tmp_path, '[[canvases]]\nid = "c1"\n')
    led = ledger.init_ledger("demo")
    ledger.add_beat(led, type="npc_intro", title="t", desc="d",
                    target_phase="5_scenes.toml")
    led["plan"][0]["produced_canvas_ids"] = ["c_missing"]
    ledger.mark_beat(led, "beat_0001", "validated")
    report = ledger.reconcile(led, toml)
    assert report["ok"] is False
    assert report["drift"] == [{"beat": "beat_0001", "missing_canvas": "c_missing"}]


def test_reconcile_ignores_planned_beats(tmp_path):
    toml = _write_toml(tmp_path, '[[canvases]]\nid = "c1"\n')
    led = ledger.init_ledger("demo")
    ledger.add_beat(led, type="npc_intro", title="t", desc="d",
                    target_phase="5_scenes.toml")
    led["plan"][0]["produced_canvas_ids"] = ["c_not_yet"]  # still planned
    report = ledger.reconcile(led, toml)
    assert report["ok"] is True
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest .claude/skills/author-game/scripts/test_ledger.py -p no:django -q`
Expected: FAIL — `AttributeError: module 'ledger' has no attribute 'collect_toml_ids'`

- [ ] **Step 3: Write minimal implementation**

Add `import tomllib` to the top of `ledger.py` (next to `import json`), then append:

```python
def _walk_ids(node, acc):
    if isinstance(node, dict):
        for key, val in node.items():
            if key in ("id", "slug") and isinstance(val, str):
                acc.add(val)
            else:
                _walk_ids(val, acc)
    elif isinstance(node, list):
        for item in node:
            _walk_ids(item, acc)


def collect_toml_ids(merged_toml_path) -> set:
    data = tomllib.loads(Path(merged_toml_path).read_text())
    acc = set()
    _walk_ids(data, acc)
    return acc


def reconcile(led: dict, merged_toml_path) -> dict:
    ids = collect_toml_ids(merged_toml_path)
    drift = []
    for beat in led["plan"]:
        if beat["status"] not in ("authored", "validated"):
            continue
        for cid in beat.get("produced_canvas_ids", []):
            if cid not in ids:
                drift.append({"beat": beat["id"], "missing_canvas": cid})
    return {"ok": not drift, "drift": drift}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest .claude/skills/author-game/scripts/test_ledger.py -p no:django -q`
Expected: PASS (15 passed)

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/author-game/scripts/ledger.py .claude/skills/author-game/scripts/test_ledger.py
git commit -m "feat(author-game): reconcile ledger against merged TOML (anti-drift)"
```

---

## Phase 2 — Corpus restructure (`prompts_v2`)

> These tasks edit prose. There are no unit tests; acceptance = the stated grep/build checks pass, and external section anchors stay intact (spec §8).

### Task 6: Structure-discipline doctrine note

**Files:**
- Modify: `prompts_v2/doctrine/04_authoring_rules.md` (append a new top-level section at end of file; do NOT renumber existing sections)

- [ ] **Step 1: Confirm the insertion point**

Run: `grep -n '^## ' prompts_v2/doctrine/04_authoring_rules.md | tail -5`
Note the last `##` section number N. The new section is `## §<N+1> — Stable-and-extensible structure (no silent drift)`.

- [ ] **Step 2: Append the note**

Append to the end of `prompts_v2/doctrine/04_authoring_rules.md` (replace `<N+1>` with the real next number from Step 1):

```markdown
## §<N+1> — Stable-and-extensible structure (no silent drift)

Structure (locations, NPCs, flags, schedules, `[settings]` scoping) is **stable but
extensible**, not frozen. A game's story plan grows as it is authored; the structure it
rests on may grow with it — a new location can be discovered, a new NPC introduced, a new
flag added mid-authoring.

The invariant is not "structure never changes." It is: **structure only ever changes
through an explicit, checked amendment — never silent drift.**

- Adding a location means adding its full definition + lock + schedule wiring + the unlock
  beat that reaches it (the unlock contract, `doctrine/10` §5.4). Not a bare reference.
- Adding an NPC means adding its schedule + an open on-ramp where the player meets it
  (D72-R6, the presence floor). Not a portrait with nowhere to appear.
- Adding a flag means it has a reachable setter before anything gates on it.
- Nothing in the TOML may reference a location/NPC/flag that has not been added this way.

In interactive authoring this discipline is mechanical: the ledger's `structure_registry`
records what exists, and every amendment is a logged `add_structure` step. See
`docs/superpowers/specs/2026-06-03-living-plan-authoring-design.md` §4.1 and §6.
```

- [ ] **Step 3: Verify it landed and anchors are intact**

Run: `grep -n "Stable-and-extensible structure" prompts_v2/doctrine/04_authoring_rules.md`
Expected: one hit. Then confirm no earlier section numbers changed:
Run: `grep -n '^## §6' prompts_v2/doctrine/04_authoring_rules.md`
Expected: the pre-existing §6 line is unchanged (we appended, did not renumber).

- [ ] **Step 4: Commit**

```bash
git add prompts_v2/doctrine/04_authoring_rules.md
git commit -m "docs(prompts_v2): structure-discipline note (no silent drift)"
```

---

### Task 7: Refit `stages/01` as the setup-interview spec

**Files:**
- Modify: `prompts_v2/stages/01_game_book_prompt.md`

- [ ] **Step 1: Read the current head and the §0.5 interactive block**

Run: `sed -n '1,120p' prompts_v2/stages/01_game_book_prompt.md`
Confirm the existing §0.5.2 / §0.5.3 interactive Q&A blocks (the seam we are widening).

- [ ] **Step 2: Add a setup-mode banner after the title**

Insert immediately after the H1 title line (line 1), before `## §0`:

```markdown
> **Setup mode (interactive authoring).** When driven by the `/author-game` skill, this
> stage runs as a one-time **setup interview**, not a one-shot book dump. Ask the question
> set in §0.6 ONE AT A TIME (each with ideas + options + a recommendation), then emit the
> design book + the empty-but-buildable scaffold TOML (settings + metadata + locations +
> npcs + schedules) and prove it builds green. It does NOT author any canvases — those are
> authored beat-by-beat in `stages/02` (per-beat authoring). See
> `docs/superpowers/specs/2026-06-03-living-plan-authoring-design.md` §5.
```

- [ ] **Step 3: Add the §0.6 setup question set**

Find the end of the §0.5 block:
Run: `grep -n '^## §1' prompts_v2/stages/01_game_book_prompt.md | head -1`
Insert immediately BEFORE that `## §1` line:

```markdown
## §0.6 — Setup interview question set (setup mode)

Ask ONE AT A TIME. Skip any question whose answer is already in the concept input or has a
safe doctrine default (state the default, don't ask). Each question carries 2–4 concrete
options + a recommendation.

1. **Premise / setting / player character** — who the player is, where, the hook.
2. **Economic engine + time model** — money pressure + day/period structure (offer the
   doctrine default time model; only ask if the concept overrides it).
3. **Cast** — propose 4–6 NPCs with arc shapes from `doctrine/03_arc_shapes.md`; LO reshapes.
4. **Location graph** — propose hubs/containers/locks from cast + premise; LO reshapes.
   Apply the unlock contract (`doctrine/10` §5.4) to any locked location hosting a schedule.
5. **Phase 2+ decisions** — pregnancy / scandal / gallery / tracker (Doc 65; reuse §0.5.2).
6. **Kink / vocab ceilings.**
7. **The loose end-to-end roadmap** — draft an ordered, sketchy, fully-reorderable beat list
   (intro → first job → meet X → unlock downtown → buy home → … → endgame) from everything
   above; LO reorders / cuts / adds. This roadmap seeds the ledger `plan`; every beat starts
   `status: planned`. It is a hypothesis, not a contract (structure-discipline,
   `doctrine/04` structure note).

**Setup output:** the design book (existing §1.2 shape) PLUS the scaffold TOML (phases
`0_systems_spec` + `1_metadata_and_locations`) PLUS the seeded ledger. No canvases.
```

- [ ] **Step 4: Verify anchors intact**

Run: `grep -n '^## §6\|^## §7\|^## §8' prompts_v2/stages/01_game_book_prompt.md`
Expected: the pre-existing §6/§7/§8 lines are unchanged (external refs depend on them — spec §8).
Run: `grep -n '§0.6 — Setup interview' prompts_v2/stages/01_game_book_prompt.md`
Expected: one hit.

- [ ] **Step 5: Commit**

```bash
git add prompts_v2/stages/01_game_book_prompt.md
git commit -m "docs(prompts_v2): refit stages/01 as setup-interview spec"
```

---

### Task 8: Refit `stages/02` as the per-beat authoring spec

**Files:**
- Modify: `prompts_v2/stages/02_toml_generation_prompt.md`

- [ ] **Step 1: Read the head**

Run: `sed -n '1,60p' prompts_v2/stages/02_toml_generation_prompt.md`

- [ ] **Step 2: Add a per-beat-mode banner after the title**

Insert immediately after the H1 title line, before the first `## ` section:

```markdown
> **Per-beat mode (interactive authoring).** When driven by the `/author-game` skill, this
> stage authors ONE beat at a time, not the whole TOML. Inputs: the chosen beat (from the
> ledger `plan`), the design book, the ledger, and the current `toml_phases/*`. Output: the
> beat's canvases appended to the beat's `target_phase` file, plus any structure amendment
> the beat needs (done WHOLE per the structure-discipline note, `doctrine/04`). After
> authoring, run the per-beat validation in §<BEAT_VALIDATION> before marking the beat done.
> See `docs/superpowers/specs/2026-06-03-living-plan-authoring-design.md` §6–§7. The
> whole-game pour described below remains valid for non-interactive (one-shot) use.
```

- [ ] **Step 3: Add the per-beat authoring + validation section at end of file**

Run: `grep -n '^## ' prompts_v2/stages/02_toml_generation_prompt.md | tail -3`
Append at the end of the file (use the real next section number for `<M>`; replace the banner's `<BEAT_VALIDATION>` reference with `§<M>.2`):

```markdown
## §<M> — Per-beat authoring loop (interactive mode)

### §<M>.1 — Author one beat

1. Read the beat (`id`, `type`, `title`, `desc`, `introduces`, `target_phase`) + the book.
2. If `introduces` is non-empty, perform the structure amendment FIRST and WHOLE
   (`doctrine/04` structure note): location → def + lock + schedule + unlock beat; NPC →
   schedule + open on-ramp; flag → ensure a reachable setter. Register each via the skill's
   `add_structure` step.
3. Author the beat's canvases per the lane/hub/schedule/lock doctrine for the beat `type`:
   - `npc_intro` → Lane-1 hub at an open on-ramp (D72-R6).
   - `location_reveal` → the location + its hubs; honor the unlock contract (`doctrine/10` §5.4).
   - `arc_escalation` → next-rung canvases gated on the prior rung's flag.
   - `cross_npc` → a beat referencing two+ registered NPCs (all endpoints must already exist).
   - `economic` → money/progression wiring (rent/phone under `[settings]`, never bare keys).
   - `story_turn` → world/event canvases.
   - `capstone` → Doc 57 one-shot (`is_repeatable=false`, `priority>=9`, flag-gated + flag-setting).
4. Append canvases to the beat's `target_phase` file only. Record their ids as the beat's
   `produced_canvas_ids`.

### §<M>.2 — Per-beat validation (run before marking the beat validated)

Run, in order, and FIX red before the beat is `validated`:

1. `python scripts/merge_toml_phases.py games/<slug> --validate` — assembles + parses the TOML.
2. `python manage.py package_from_toml --file games/<slug>/toml_phases/7_final_game.toml --owner-id <uuid> --output games/<slug>/output --dev` — schema + flag-chain validation. (Fast/validate use per skill; full HTML build at milestones only.)
3. **Doctrine self-audit** — emit a pass/fail line for each, against what THIS beat authored:
   - reachability triad (`doctrine/10` §5): schedule ∩ canvas-window ∩ player-present-awake.
   - dead-presence / D72 floor (`doctrine/02` §8.11–§8.15; D72-R6/R7/R8).
   - locked-location unlock contract (`doctrine/10` §5.4, Cases A/B/C).
   - `[settings]` scoping (clothing/rent/phone keys under `[settings]`, not bare).
   - `is_container` swallow (no activity/ambient/capstone attached to a container location).
```

- [ ] **Step 4: Fix the banner cross-reference**

In the banner from Step 2, replace `§<BEAT_VALIDATION>` with the real `§<M>.2` you just used.

- [ ] **Step 5: Verify**

Run: `grep -n 'Per-beat authoring loop\|Per-beat validation' prompts_v2/stages/02_toml_generation_prompt.md`
Expected: two hits, no remaining `<M>` / `<BEAT_VALIDATION>` placeholders:
Run: `grep -n '<M>\|<BEAT_VALIDATION>' prompts_v2/stages/02_toml_generation_prompt.md`
Expected: no hits.

- [ ] **Step 6: Commit**

```bash
git add prompts_v2/stages/02_toml_generation_prompt.md
git commit -m "docs(prompts_v2): refit stages/02 as per-beat authoring spec"
```

---

### Task 9: Anchor-integrity sweep + regenerate COMPREHENSIVE

**Files:**
- Modify: `prompts_v2/COMPREHENSIVE_SYSTEM_REFERENCE.md` (regenerated)

- [ ] **Step 1: Verify no external anchor broke**

The spec (§8) flags `stages/01` and `doctrine/10` §6/§7/§8 as referenced ~8x. We appended rather than renumbered, but confirm:
Run: `grep -rn 'stages/01.*§[678]\|doctrine/10.*§[678]' prompts_v2/ --include=*.md | grep -v COMPREHENSIVE`
For each hit, confirm the cited section still exists at that number:
Run: `grep -n '^## §6\|^## §7\|^## §8' prompts_v2/stages/01_game_book_prompt.md prompts_v2/doctrine/10_location_design.md`
Expected: all cited sections still present. If any moved, fix the referrer before continuing.

- [ ] **Step 2: Regenerate COMPREHENSIVE**

Run: `python scripts/regen_comprehensive_reference.py`
Expected: prints the source count + new byte size, exits 0.

- [ ] **Step 3: Confirm new content is in the bundle**

Run: `grep -c 'Per-beat authoring loop\|Setup interview question set\|Stable-and-extensible structure' prompts_v2/COMPREHENSIVE_SYSTEM_REFERENCE.md`
Expected: 3 (each new section present once).

- [ ] **Step 4: Commit**

```bash
git add prompts_v2/COMPREHENSIVE_SYSTEM_REFERENCE.md
git commit -m "docs(prompts_v2): regen COMPREHENSIVE with setup/per-beat restructure"
```

---

## Phase 3 — The skill

> Prose orchestration. Acceptance = the skill files exist with the required sections and the
> shakedown (Phase 4) runs end-to-end. Keep instructions concrete and reference the helper by
> exact command.

### Task 10: `SKILL.md` — frontmatter + mode dispatch

**Files:**
- Create: `.claude/skills/author-game/SKILL.md`

- [ ] **Step 1: Write the skill skeleton**

Create `.claude/skills/author-game/SKILL.md`:

```markdown
---
name: author-game
description: Use when authoring an RTS-shape sandbox game in this repo interactively — runs a one-time setup interview (skeleton + roadmap), then authors the game one beat at a time with validate-after-every-beat. Use for "start a new game", "continue writing <game>", "add a beat/NPC/location/arc to <game>".
---

# Author Game — interactive sequential authoring

Drives game authoring as **setup once, then continue beat-by-beat**, backed by a persistent
ledger. Replaces blind one-shot generation. Full design:
`docs/superpowers/specs/2026-06-03-living-plan-authoring-design.md`.

## State (per game, under `games/<slug>/`)
- `design_book.md` — intent (premise/player/economy/time/cast/locations/roadmap).
- `authoring_state.json` — the ledger (plan + structure registry + next_up + log). Owned by
  `scripts/ledger.py`; never hand-edit mid-run.
- `toml_phases/*.toml` — built content (`7_final_game.toml` is generated by merge).

## Knowledge base
- `references/ledger-schema.md` — the ledger shape.
- `references/setup-interview.md` — setup mode (mirrors `prompts_v2/stages/01` §0.6).
- `references/beat-authoring.md` — continue mode + the per-beat self-audit checklist
  (mirrors `prompts_v2/stages/02` per-beat loop).
- `prompts_v2/COMPREHENSIVE_SYSTEM_REFERENCE.md` — all doctrine/schema.

## Mode dispatch
On invocation, determine the game slug from the request, then:
1. If `games/<slug>/authoring_state.json` does NOT exist → **setup mode**
   (read `references/setup-interview.md`).
2. If it DOES exist → **continue mode** (read `references/beat-authoring.md`); first
   resume + reconcile (see that file).

Always read the relevant reference file before acting. Ask the user, one question at a time,
via the AskUserQuestion tool — always with ideas, options, and a recommendation.
```

- [ ] **Step 2: Verify frontmatter parses**

Run: `head -4 .claude/skills/author-game/SKILL.md`
Expected: a `name:` and `description:` between `---` fences.

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/author-game/SKILL.md
git commit -m "feat(author-game): skill skeleton + mode dispatch"
```

---

### Task 11: `references/setup-interview.md`

**Files:**
- Create: `.claude/skills/author-game/references/setup-interview.md`

- [ ] **Step 1: Write the setup-mode reference**

Create the file:

```markdown
# Setup mode — the one-time interview

Goal: lock the structural skeleton + seed a loose, revisable roadmap, then emit a
buildable empty game + a seeded ledger. NO canvases are authored in setup.

## Steps

1. **Read** `prompts_v2/stages/01_game_book_prompt.md` §0.6 (the question set) and the
   relevant doctrine via `prompts_v2/COMPREHENSIVE_SYSTEM_REFERENCE.md`.
2. **Interview** — ask §0.6 questions ONE AT A TIME via AskUserQuestion. Each question:
   2–4 concrete options + a recommendation. Skip anything already answered or safely
   defaulted (state the default).
3. **Write `design_book.md`** to `games/<slug>/` using the §1.2 book shape (premise, player,
   economy, time model, cast + arc shapes, location graph, and the loose end-to-end roadmap).
4. **Write the scaffold TOML**: `0_systems_spec.toml` ([settings] incl. correct clothing/rent/
   phone scoping) and `1_metadata_and_locations.toml` (metadata, locations with locks, npcs,
   schedules). No `[[canvases]]` yet. Use `games/late_shifts/toml_phases/` as the structural
   reference for table shapes.
5. **Seed the ledger** with `scripts/ledger.py`:
   - `init_ledger("<slug>")`, then `add_structure` for every location/npc/flag the scaffold
     declares, then `add_beat(...)` for each roadmap beat (status stays `planned`), then
     `save_ledger`. (Drive these via a short `python -` heredoc that imports the helper.)
6. **Prove green** — run the per-beat validation sequence (see `beat-authoring.md` §Validation)
   once on the empty scaffold; it must build/validate clean before setup is "done".
7. **Report** the roadmap back and tell the user: "Setup complete — say *continue* to author
   the first beat."

## Anti-patterns
- Do NOT author canvases in setup.
- Do NOT ask questions with safe doctrine defaults — default and say so.
- Do NOT invent engine knobs; every option offered must be real (cite doctrine/schema).
```

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/author-game/references/setup-interview.md
git commit -m "feat(author-game): setup-mode reference"
```

---

### Task 12: `references/beat-authoring.md` (continue mode + validation)

**Files:**
- Create: `.claude/skills/author-game/references/beat-authoring.md`

- [ ] **Step 1: Write the continue-mode reference**

Create the file:

```markdown
# Continue mode — author one beat per turn

## Resume & reconcile (every continue turn, first thing)
1. `load_ledger(games/<slug>)` via `scripts/ledger.py`.
2. `merge_toml_phases.py games/<slug> --validate` to assemble `7_final_game.toml`.
3. `reconcile(led, games/<slug>/toml_phases/7_final_game.toml)` — if `ok` is False, STOP and
   report the drift (a validated beat's canvases are missing) before authoring anything new.
4. Report: where we are, the `next_up` queue, and what changed since last session.

## The beat loop
1. **Propose the next beat — with ideas + options.** Pull the head of `next_up` (or let the
   user pick / inject a new beat). Present via AskUserQuestion: 2–4 concrete ways to play the
   beat + a recommendation. New/changed beats → update the roadmap (`add_beat` / edit + log).
2. **Mark active** — `mark_beat(led, id, "active")`.
3. **Amend structure if needed, WHOLE** — for each item in the beat's `introduces`, do the
   full amendment (location: def+lock+schedule+unlock; npc: schedule+on-ramp; flag: reachable
   setter) and call `add_structure` for each. The dup-guard prevents silent drift.
4. **Author** the beat's canvases per `prompts_v2/stages/02` per-beat loop §<M>.1 for the beat
   `type`. Append to the beat's `target_phase` only. Record `produced_canvas_ids`.
5. **Validate** (below). Fix red BEFORE marking done.
6. **Mark validated + persist** — `mark_beat(led, id, "validated")`, append a `decisions_log`
   entry, `save_ledger`.
7. **Build at milestones** — full `package_from_toml` HTML build at end of an arc / session /
   on demand (not every beat).

## Validation (per beat — the safety net)
Run in order; emit a result line for each:
1. `python scripts/merge_toml_phases.py games/<slug> --validate`
2. `python manage.py package_from_toml --file games/<slug>/toml_phases/7_final_game.toml --owner-id 15b35759-e67f-4bab-be10-5a27dd7ddc7a --output games/<slug>/output --dev`
   (validate/fast at beat granularity; this also produces the milestone build when run in full.)
3. **Doctrine self-audit** — PASS/FAIL each, scoped to this beat:
   - reachability triad (`doctrine/10` §5)
   - dead-presence / D72 floor (`doctrine/02` §8.11–§8.15)
   - locked-location unlock contract (`doctrine/10` §5.4)
   - `[settings]` scoping (clothing/rent/phone not bare)
   - `is_container` swallow

Any FAIL → fix, re-run, then mark validated.
```

- [ ] **Step 2: Reconcile the §<M> reference**

The §<M>.1 number is set in Task 8 Step 3. Update the `§<M>.1` reference in this file to the real number:
Run: `grep -n 'Per-beat authoring loop' prompts_v2/stages/02_toml_generation_prompt.md`
Replace `§<M>.1` in `beat-authoring.md` with the matching `§<real>.1`.

- [ ] **Step 3: Verify no placeholder remains**

Run: `grep -n '<M>\|<slug>\|<real>' .claude/skills/author-game/references/beat-authoring.md`
Expected: `<slug>` is allowed (it's a runtime template); no `<M>` or `<real>` left.

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/author-game/references/beat-authoring.md
git commit -m "feat(author-game): continue-mode + per-beat validation reference"
```

---

## Phase 4 — Shakedown (first real run)

> This is the de-risk step (spec §11.5, §12). It exercises the whole loop on a throwaway game.
> If the rhythm is awkward, fix the skill/references and re-run before declaring done.

### Task 13: Setup a throwaway game → green scaffold

**Files:**
- Create at runtime: `games/_shakedown/` (design_book.md, authoring_state.json, toml_phases/)

- [ ] **Step 1: Run setup mode on a toy concept**

Invoke the skill: "Start a new game, slug `_shakedown`: a small night-shift convenience-store
premise, 2 NPCs, full_game scope." Answer the interview questions tersely (accept
recommendations) to drive it fast.

- [ ] **Step 2: Verify the scaffold built green**

Run: `python scripts/merge_toml_phases.py games/_shakedown --validate`
Expected: `validation: OK (parsed cleanly)`.
Run: `python manage.py package_from_toml --file games/_shakedown/toml_phases/7_final_game.toml --owner-id 15b35759-e67f-4bab-be10-5a27dd7ddc7a --output games/_shakedown/output --dev`
Expected: `✓ Validation passed`, `✓ All flag chains valid`, an `index.html` is produced.

- [ ] **Step 3: Verify the ledger seeded**

Run: `python -m json.tool games/_shakedown/authoring_state.json | head -40`
Expected: `plan` has the roadmap beats (status `planned`), `structure_registry` lists the
scaffold's locations/npcs/flags, `next_up` non-empty.

- [ ] **Step 4: Commit the shakedown artifacts**

```bash
git add games/_shakedown
git commit -m "test(author-game): shakedown setup — green scaffold + seeded ledger"
```

---

### Task 14: Author 3 varied beats → validate each → milestone build

- [ ] **Step 1: Author beat 1 (`npc_intro`)**

Invoke: "continue _shakedown". Accept the proposed first beat (the meet/on-ramp). Let the
loop author + validate. Confirm the per-beat output includes the §Validation result lines
(merge OK, package validated, 5 self-audit PASS lines).

- [ ] **Step 2: Author beat 2 (`location_reveal`)**

Invoke: "continue _shakedown" and steer toward a location-reveal beat (unlock a back room or
a second venue). Confirm the structure amendment is done WHOLE (the location gets def + lock +
unlock beat) and `add_structure` registered it (check `authoring_state.json`).

- [ ] **Step 3: Author beat 3 (`economic`)**

Invoke: "continue _shakedown" and steer toward an economic milestone. Confirm rent/phone-style
keys (if any) land under `[settings]`, not bare (the self-audit must PASS scoping).

- [ ] **Step 4: Milestone build + reconcile clean**

Run: `python scripts/merge_toml_phases.py games/_shakedown --validate`
Run: `python manage.py package_from_toml --file games/_shakedown/toml_phases/7_final_game.toml --owner-id 15b35759-e67f-4bab-be10-5a27dd7ddc7a --output games/_shakedown/output --dev`
Expected: green build.
Run the reconcile check:
```bash
python - <<'PY'
import sys; sys.path.insert(0, ".claude/skills/author-game/scripts")
import ledger
led = ledger.load_ledger("games/_shakedown")
print(ledger.reconcile(led, "games/_shakedown/toml_phases/7_final_game.toml"))
PY
```
Expected: `{'ok': True, 'drift': []}` — every validated beat's canvases are present.

- [ ] **Step 5: Commit**

```bash
git add games/_shakedown
git commit -m "test(author-game): shakedown — 3 beats authored, validated, reconciled clean"
```

---

### Task 15: Capture findings + decide keep/discard shakedown

- [ ] **Step 1: Note rhythm issues**

Append a short `## Shakedown findings` section to the spec
(`docs/superpowers/specs/2026-06-03-living-plan-authoring-design.md`): what felt smooth, what
was awkward, any skill/reference edits made during Phase 4. If edits were needed, they should
already be committed against the relevant Task files.

- [ ] **Step 2: Decide on `_shakedown`**

Ask the user: keep `games/_shakedown` as a regression fixture, or remove it. If remove:
```bash
git rm -r games/_shakedown
git commit -m "chore(author-game): remove shakedown fixture"
```

- [ ] **Step 3: Final commit (findings)**

```bash
git add docs/superpowers/specs/2026-06-03-living-plan-authoring-design.md
git commit -m "docs(author-game): shakedown findings"
```

---

## Self-Review (completed against the spec)

**Spec coverage:**
- §3 delivery (skill + restructured corpus) → Tasks 7–8 (corpus), 10–12 (skill). ✓
- §4 three-artifact state + §4.1 ledger schema → Task 1 (doc) + Tasks 2–5 (helper). ✓
- §5 setup phase (7-question interview, scaffold, prove-green) → Task 7 (§0.6) + Task 11 + Task 13. ✓
- §6 continuation loop + §6.1 beat types → Task 8 (per-beat loop), Task 12, Task 4 (beat types enum). ✓
- §6 step-3 anti-drift / structure-discipline → Task 6 (doctrine note) + Task 3 (registry dup-guard) + Task 5 (reconcile). ✓
- §7 validation + §7.2 self-audit (not-yet-automated, by checklist) → Task 8 §<M>.2 + Task 12 Validation. ✓
- §8 corpus restructure + anchor preservation + regen → Tasks 7, 8, 9. ✓
- §11 build decomposition → phases 1–4 mirror it. ✓
- §12 risks (loop rhythm de-risked in shakedown) → Phase 4. ✓

**Placeholder scan:** the only intentional templates are `<slug>` (runtime game name) and the
owner UUID (the repo's real owner id `15b35759-e67f-4bab-be10-5a27dd7ddc7a`, used verbatim in
runtime tasks). `<N+1>` / `<M>` are resolved within their own tasks with an explicit grep step,
and Task 8 Step 5 + Task 12 Step 3 assert no such placeholder remains in shipped files.

**Type consistency:** helper API is stable across tasks — `init_ledger`, `load_ledger`,
`save_ledger`, `add_structure(led, kind, name)`, `add_beat(led, *, type, title, desc,
target_phase, deps?, introduces?)`, `get_beat`, `mark_beat(led, id, status)`,
`collect_toml_ids`, `reconcile(led, path)`. Beat types/statuses match the schema doc (Task 1)
and the enum (Task 4). Phase-file names match the real `games/late_shifts/toml_phases/` listing.
```
