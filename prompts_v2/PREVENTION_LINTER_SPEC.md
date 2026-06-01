# Prevention Linter — Spec (NOT yet implemented)

**Status:** Specification only. No engine code written. This documents the build-time checks that would CATCH the "valid TOML, dead in play" class of bugs that the prompts_v2 corpus can only WARN about.

**Why this exists:** The Late Shifts build (2026-05-29/30) shipped 6 silent-runtime bugs on a GREEN build (full list in the project memory + `doctrine/10`). The current validator (`apps/projects/services/template_import.py` `validate()`, ~line 2880+) checks STATIC facts — a flag has a setter, a trait is declared, a project id is snake_case, nav_order points somewhere. It never checks DYNAMIC REACHABILITY — can a canvas actually fire given location type, NPC schedule, time window. Corpus rules (doctrine/10, stages §10/§11) tell the author what to avoid; only a linter makes the mistake impossible to ship.

**Where it lives:** extend `template_import.py validate()` (alongside the existing project / flag-chain / container-default-entry checks, ~line 3360+). Severity: most are ERRORS (block the build); a couple are WARNINGS (computed heuristically). The v2 flag-chain validator (`v2.py:~10699`) is the model for the flag checks.

---

## Checks (each maps to a Late Shifts bug + a doctrine rule)

### L1 — Canvas attached to a container location (ERROR) — bug B1, doctrine/10 §3
For every canvas with a `trigger.location`: if that location has `is_container = true`, error:
`canvas '<id>' is attached to container location '<loc>' — containers render only child-nav and SWALLOW canvases. Attach to a non-container standing hub.`
Container passages (`v2.py:8800`) never call getStoryCanvasRedirect/renderNpcPortraits/renderSoloActivities.

### L2 — `requires_npc` location not in that NPC's schedule (ERROR) — bug B2, doctrine/10 §5.1
For every canvas with `requires_npc = npc_X`: assert the canvas's `trigger.location` appears in at least one of `npc_X`'s `[[npcs.schedules]]` entries. Else error:
`canvas '<id>' requires npc '<X>' at '<loc>', but '<X>' is never scheduled there — it can never fire (getNpcLocation is schedule-only, fail-closed).`

### L3 — Portrait hub NPC not schedule-present (ERROR) — bug B3, doctrine/10 §5.2
For every canvas that is a Lane-1 portrait hub (`npc =` set, `trigger_mode` manual/default, repeatable): assert that NPC is schedule-present at the hub's location (same test as L2 but keyed on `npc`, not `requires_npc`). Else error — the portrait won't render (`renderNpcPortraits` `v2.py:4295` has its own presence gate), so the hub is unreachable.

### L4 — Reachable-setter for is_true gates (ERROR) — bug A4/B2, extends existing flag-chain check
The existing flag-chain validator checks a setter EXISTS. Extend it: the setter canvas must itself be reachable — i.e. it must pass L1/L2/L3 (not on a container, requires_npc/portrait schedule satisfiable). A setter that exists but can never fire = the flag is effectively unset. (Late Shifts: `hank_first_contact`'s only setter was L2-dead → the whole chain stalled, build GREEN.)

### L5 — Dev-only flag required by a shipping canvas (ERROR) — bug D1, doctrine/10 + stages/02 §10.16
Classify canvases as "dev" (gated on `dev_mode_enabled` is_true, or in the dev phase) vs "shipping". If a flag's ONLY setter is a dev canvas, no shipping canvas may require it (`is_true`). Else error — stripping dev breaks the chain.

### L6 — Included Phase-2+ trait with no setter (ERROR) — bug B5, doctrine/09 §6 + stages/02 §12.12
If the project opts a Phase-2+ trait in (the design book / a marker says `pregnancy = include`, etc.), assert ≥1 canvas effect sets that trait (`{ targetType="player", trait="pregnancy", op="set"/"add" }`). Else error: included system is dormant. (Validator currently checks flags, not traits.)

### L7 — Timing dead-zone (WARNING) — bug B4, doctrine/10 §5.3
Where computable, for each NPC ambient/capstone compute NPC-schedule ∩ canvas-window (`[[canvases.trigger.schedules]]`), cross-midnight aware. If empty, warn. (Player-presence is hard to model statically → WARNING not ERROR; the corpus checklist carries the manual triad check.)

### L8 — Peer/dating capstone-only NPC (WARNING) — bug B6, doctrine/03 §5 + doctrine/10 §6
For each peer/dating NPC: if it has a first-night/consummation capstone but no repeatable ongoing hub at the partner's location, warn — the arc has no Stage-4 surface.

---

## Notes on detection inputs
- Arc shape / Phase-2+ inclusions: not in the TOML today. Either add a lightweight `[meta]` marker emitted by Stage 2, or infer (peer/dating ≈ NPC with a `<slug>_stage` ladder + a `*_first_night`-style capstone). L6/L8 may need a marker; L1–L5 work off pure TOML + schedules.
- Cross-midnight windows (22:00–07:00) must split into [22:00,24:00)+[00:00,07:00) before overlap tests — the Late Shifts audit script got false positives until this was handled.

## Out of scope here (verification-tooling notes, F1–F4)
Not linter checks — operator notes for whoever live-plays via the twine-game-explorer skill:
- **F1:** the explorer's `passage_body_text` includes BOTH branches of an `<<if>>` — to confirm which variant renders, eval `document.querySelector('.passage').innerText`, not body_text.
- **F2:** the explorer's `clickables` / a naive `data-passage` scrape pick up the global NPC-status widget (NPC portraits + their current locations) on EVERY screen — read `[[Leave→Location]]` links or the `location-nav-grid`/`location-nav-exits` divs to see a location's real nav children.
- **F3:** macOS has no `timeout` — don't prefix explorer commands with it.
- **F4:** kill stale explorer daemons (by PID) + clear `.live/daemon.json` before a fresh session; collisions serve stale HTML and produce misleading empty/`opts: []` reads.

---

**End of spec.** Implementing L1–L6 (the ERRORS) would convert the entire Category-B bug class from "caught only by live-play" to "caught at build." That is a separate engine task; this corpus pass only WARNS via doctrine/10 + the stage checklists.
