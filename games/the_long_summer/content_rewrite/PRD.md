# TLS Content Rewrite — PRD

> **Master document for the multi-session content-rewrite project.**
> Built 2026-04-24 (Session 1).
> Plan source: `/Users/a0000/.claude/plans/go-with-your-recommendations-mighty-wadler.md`.

---

## ⏯ How to resume (read this first if you're a new session)

1. **Read this PRD's "Status" block** (next section) — see what tier we're on and what's next.
2. **Read `session_log.md`** — last session's notes; what was just done; any open issues.
3. **Read `priority_queue.yaml`** — pick the next canvas with status `not_started` from the active tier.
4. **Read the relevant style sheets** — `style_sheets/maya.md` always, plus `style_sheets/<npc>.md` for any NPC in the scene.
5. **Read `standards.md`** — 25 craft rules.
6. **Read `choice_label_patterns.md`** before writing any `exit_block.choices`.
7. **Read `corruption_band_register.md`** if the canvas has band-gated variants or the gate is at corruption ≥25.
8. **If this is your first time on TLS**, also skim `worked_example_ryan_beach.md` to internalize the target quality.
9. **Open the canvas** in `2_story_canvases.toml` or `3_activities.toml`.
10. **Rewrite** following the per-canvas workflow (below).
11. **Validate** with `package_from_toml --dry-run`.
12. **Self-check** against `qa_rubric.md`.
13. **Update** `priority_queue.yaml` (status, actual_words, notes) + append to `session_log.md`.

---

## Status

| Field | Value |
|---|---|
| **Project state** | Session 1 — infrastructure pass + 2 worked examples |
| **Total canvases** | 78 (+ 1 frozen Prologue = 79 total) |
| **Done** | 0 (will be 2 at end of Session 1) |
| **In progress** | ryan_beach, activity_mirror_look |
| **Last session** | See `session_log.md` |
| **Active tier** | A (after Session 1 finishes ryan_beach) and F (mirror_look special) |

Per-tier targets (from `priority_queue.yaml`):

- **Tier A** — 8 Cracks + Phase-1 close — multi-node Option B, 1500-2500 words each
- **Tier B** — 6 chapter milestones + arrival — Option A default, 800-1500 words
- **Tier C** — 14 arc-progression beats — Option A, 400-700 words, 2-3 char-revealing choices
- **Tier D** — 4 tiered diner shifts — Option A high-variation, rotating openings + rare events
- **Tier E** — 22+3 NPC repeatable activities — Option A, 300-500 words incl. variants
- **Tier F** — 21 solo + town dailies + mirror_look special — Option A, 150-300 words (mirror_look ~600)

---

## Why this exists

The Long Summer's design book (`final_book.md`, 35,515 words) and TOML game data (79 canvases / 94 nodes / 38 locations / 12 NPCs) are excellent in structure and locked in canon. But the **canvas prose and choice text are the wrong quality** outside the Prologue.

Three parallel research passes (mining 4 explored games, ruthless TLS canvas critique, web research across Ashwell / Short / Ingold / Kennedy / Failbetter / sub-Q / DoL / COG) converged:

- The Prologue (1 canvas × 9 nodes) is genuinely excellent novel-register prose with real branching and per-NPC voice.
- Everything after the Prologue collapses into sparse template prose. `@npc_xxx` tokens leak into the player-facing text. Activities are stat-vending-machines with no meaningful choices. Voice specs exist on paper but never on the page.
- Root cause: a Phase-4 instruction in `final_book.md` to keep beat prose tight at 150-300 words, interpreted as permission to skeletonize everything outside the Prologue.

This project rewrites all 78 non-Prologue canvases to match Prologue quality (where the design says it should) and Failbetter density (where the design says brevity is correct).

---

## Scope & non-goals

**In scope:**
- Body prose, variant prose, choice-label rewrite in `2_story_canvases.toml` and `3_activities.toml`
- Choice `effects` / `flagEffects` / `time_progression_minutes` adjustments **only where current values are broken** (e.g., Tier-D T0 identical payouts)
- Author media blocks (`type=image` / `type=video`) with `file`, `description`, `search_queries` — physical media retrieval out of scope
- Tier A Option-B node escalations, which touch `4_story_arc.toml`
- `6_final_game.toml` rebuild after each batch
- `package_from_toml --dry-run` validation per canvas

**Out of scope:**
- Engine changes
- Design canon changes (`final_book.md`, `Game_Redesign.md`)
- Structural redesign (new stats, NPCs, arcs, chapters)
- Media file retrieval / download / validation
- Git commits (user directive: batches in place, no commits)
- Prologue edits beyond typos (frozen as style exemplar)

---

## Bundle architecture

```
games/the_long_summer/content_rewrite/
├── PRD.md                           ← THIS FILE
├── priority_queue.yaml              ← per-canvas status, tier, word target
├── standards.md                     ← 25 craft rules as enforceable checklist
├── choice_label_patterns.md         ← label conventions + do/don't
├── corruption_band_register.md      ← 4 bands × prose specimens for Maya
├── style_sheets/
│   ├── maya.md
│   ├── frank.md
│   ├── ryan.md
│   ├── jake.md
│   ├── diana.md
│   ├── marge.md
│   └── cookie.md
├── worked_example_ryan_beach.md     ← before/after with line-by-line craft commentary
├── qa_rubric.md                     ← pass/fail "is this canvas done" checklist
└── session_log.md                   ← append-only, 1-3 lines per session
```

---

## Per-canvas workflow

For every canvas:

1. Read `priority_queue.yaml` — pick next `not_started` canvas in active tier
2. Read the canvas's current TOML block + its `4_story_arc.toml` node entry + the beat spec in `final_book.md`
3. Read relevant `style_sheets/*.md` (Maya always, plus every NPC in the scene)
4. Read `standards.md` + `choice_label_patterns.md`
5. Determine corruption band from trigger `conditions`. If band-gated variants apply, read `corruption_band_register.md` for the appropriate voice
6. Decide Option A vs Option B (default A; escalate to B only when the beat cannot breathe in a single node — Tier A scenes default to B per the queue)
7. Rewrite in order: body blocks → variant `group` blocks → choice labels → `exit_block` `effects`/`flagEffects` (preserve existing flag sets by default; modify only broken values)
8. Author media blocks for each new scene moment: `type=image` or `type=video` with `file = "{tier}/{canvas_id}/{node_id}_{tag}.{ext}"`, `description`, ≥3 `search_queries`
9. Strip every `@npc_xxx` token from paragraph and dialog `content` fields
10. If Option B: add sibling `[[canvases.nodes]]` entries; chain via `targetType = "node"`. Add or adjust `[[story_arc.nodes]]` in `4_story_arc.toml` only where a sub-beat is itself a story milestone deserving a journal entry
11. Rebuild `6_final_game.toml`:
    ```bash
    cd games/the_long_summer/toml_phases
    cat 1_metadata_and_locations.toml 0_systems_spec.toml 2_story_canvases.toml 3_activities.toml 4_story_arc.toml > 6_final_game.toml
    ```
12. Run `package_from_toml --dry-run`:
    ```bash
    cd /Users/a0000/Desktop/Desktop_Archive_Backup/story_gen/story_gen_web_app/story_gen_django
    source venv/bin/activate
    python manage.py package_from_toml \
      --file games/the_long_summer/toml_phases/6_final_game.toml \
      --owner-id <any-valid-uuid> \
      --output /tmp/tls_dryrun \
      --dry-run
    ```
    Must pass with expected counts (79 + N for added Option-B nodes; 94+ nodes; 38 locations; 12 NPCs). Zero new flag-graph errors. Sibling-canvas overlap warnings stay at 12.
13. QA self-check against `qa_rubric.md`
14. Update `priority_queue.yaml` — set `status: done`, fill `actual_words`, append to `notes`
15. Append 1-3 line entry to `session_log.md`

---

## Batch sizes per tier

Never mix tiers in one batch — register discipline requires staying in one register.

| Tier | Batch size |
|---|---|
| A | 1 canvas per batch (each ~2000 words multi-node) |
| B | 2-3 canvases per batch |
| C | 3-4 canvases |
| D | 4 (all together — they share structure) |
| E | 4-6 canvases |
| F | 6-8 canvases |

---

## Critical files (read-only references)

- `games/the_long_summer/book_phases/final_book.md` — design spec
  - `:402-489` — Maya profile + corruption-band voice evolution
  - `:493-571` — Frank voice + arc spec
  - `:575-651` — Ryan voice + arc spec
  - `:655-700+` — Jake voice + arc spec
  - `:1783-2811` — Phase 1 beat-by-beat specs (B1-B28)
- `games/the_long_summer/concept.md` — 1-page pointer
- `games/the_long_summer/session_state.yaml` — game-level state
- `games/the_long_summer/toml_phases/2_story_canvases.toml:71-431` — **Prologue (FROZEN — DO NOT EDIT)** — style exemplar
- `19th_april_UOR_Redesign_Session/Game_Redesign.md` — full redesign doc
- `19th_april_UOR_Redesign_Session/Future_Considerations.md` — what's deferred to Phase 2+

---

## Files modified by this project

- `games/the_long_summer/toml_phases/2_story_canvases.toml` — 28 Phase 1 story canvases (Prologue locked)
- `games/the_long_summer/toml_phases/3_activities.toml` — 50 repeatable activities
- `games/the_long_summer/toml_phases/4_story_arc.toml` — nodes for Tier A Option-B escalations only
- `games/the_long_summer/toml_phases/6_final_game.toml` — rebuilt after every batch
- `games/the_long_summer/session_state.yaml` — bump `last_updated` and add `content_rewrite:` subsection

---

## Key technical anchors (verified during planning)

**Variant encoding:** Multiple `{ type = "group", blocks = [...], conditions = {version="1.0", logic="AND", items=[...]} }` blocks in sequence inside `canvases.nodes[].blocks`. See `3_activities.toml:576-601` (`activity_breakfast_frank` 4-variant pattern).

**Media blocks:** `{ type = "image" | "video", props = { file = "...", description = "...", search_queries = [...] } }`. See `2_story_canvases.toml:120` (Prologue N2 video), `:201` (Prologue N5 image). **Files do NOT need to exist on disk** for TOML validity or `--dry-run` to pass.

**Choice block:** `exit_block = { type = "choices", choices = [ { text, targetType, locationId?, nodeId?, time_progression_minutes, effects, flagEffects, conditions? } ] }`. See `2_story_canvases.toml:554-578` (`first_ryan_encounter`).

**Option B node-chaining:** Use `targetType = "node"` with `nodeId = "<canvas_id>.<node_id>"` to chain sub-nodes inside a single canvas. See Prologue (`2_story_canvases.toml:71-431`) for the multi-node pattern.

**6_final_game.toml concat order:** `1 + 0 + 2 + 3 + 4` (Phase 1 root scalars before Phase 0 arrays-of-tables, per TOML spec).

---

## Risks & mitigations (in force; refer when in doubt)

| Risk | Mitigation |
|---|---|
| Voice drift across sessions | Style sheets must be read every time; specimen lines memorized |
| Scope creep into redesign | Design is locked. PRD supersedes book.md only on craft rules; never on canon |
| Flag graph regression | Dry-run after every canvas. Preserve existing flag sets by default |
| Prologue contamination | Prologue (`2_story_canvases.toml:71-431`) FROZEN. Typo fixes only |
| QA fatigue | Binary rubric. "Mostly good" fails. Every 5th canvas full re-read |
| Silent register drop to RtS quality | Rubric enforces token-strip, choice-set differentiation, variant tonal-shift |
| Option B story_arc breakage | Verify downstream `requires_nodes` resolves; dry-run |
| `6_final_game.toml` rebuild drift | Use the exact concat command above. Don't manually edit 6 |

---

## Done definition

A canvas is `done` when:
- All 25 standards rules satisfied
- All `qa_rubric.md` boxes ticked
- `priority_queue.yaml` updated with status + actual_words + notes
- `session_log.md` appended with the entry

A tier is done when:
- All canvases in tier are `done`
- Word count totals roughly match tier targets
- 3 random canvases re-read against rubric and pass

A session is done when:
- Either: a planned batch is complete (most sessions)
- Or: a clean handoff point reached (mid-batch — note explicit pickup state in `session_log.md`)

---

## Open future work (not Session 1 scope)

- Media retrieval pipeline — once TOML media blocks are authored, build a separate workflow to fetch images/videos via search_queries
- After Tier A complete: consider full game build (`package_from_toml` without `--dry-run`) and human playtest of one Crack scene in browser
- After Tier D complete: replay-test the diner cycle for staleness — does the rotating-openings + rare-event injection actually work
- After all 78 canvases complete: write a "TLS Content v2 retrospective" doc summarizing what the rewrite changed and how the QA rubric held up
