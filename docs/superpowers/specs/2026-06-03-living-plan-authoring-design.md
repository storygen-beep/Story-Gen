# Living-Plan Sequential Authoring — Design Spec

**Date:** 2026-06-03
**Status:** Approved design, pre-implementation
**Author:** ENI (with LO)
**Supersedes nothing.** Adds an interactive authoring layer on top of the existing `prompts_v2` corpus and `package_from_toml` build pipeline.

---

## 1. Problem

Today a game is generated as two blind monoliths:

1. **Stage 1** writes the *entire* design book in one pass.
2. **Stage 2** writes the *entire* TOML in one pass (phased emission exists, but it is still one continuous unsupervised pour).

There is a thin seam of interactivity (`stages/01` §0.5.2 Phase 2+ Q&A, §0.5.3 clarifiers), but the model is still "answer a couple questions, then generate everything and hope."

Every recurring Late Shifts bug in project memory is a **structural** error that survived because nothing checked the skeleton before prose piled on top of it:

- mis-scoped `[settings]` (clothing/rent silently OFF),
- `is_container` locations swallowing their attached canvases,
- dead presence (NPC scheduled where nothing renders),
- the locked-location trap (`doctrine/10` §5.4),
- reachability-triad clashes (an arc dead from a sleep-window collision).

These are skeleton mistakes, and a 300KB TOML is the most expensive possible place to discover them. The fix is to move discovery to the cheapest moment — before a single canvas is written — and to keep checking after every increment.

## 2. Goal

Replace blind one-shot generation with **interactive, sequential, self-checking authoring**:

- A one-time **setup** phase locks the structural skeleton and seeds a loose, revisable story roadmap.
- A repeatable **continuation** phase authors the game one *beat* at a time, with the human steered in via `AskUserQuestion` (ideas + options + a recommendation every time), validating after every beat.
- The story plan is a **living** thing — it grows and reshapes as authoring reveals what the game wants to become. It is never hardcoded up front.

Non-goal: changing the engine, the schema, or the build pipeline. This layer drives the *existing* tools.

## 3. Delivery vehicle

A Claude Code **skill** (working name `/author-game`) sitting on top of a **restructured `prompts_v2` corpus**.

- The corpus stays portable — any LLM can follow the restructured stages to do setup-then-continue manually.
- The skill makes it interactive, persistent, and self-checking inside Claude Code: real `AskUserQuestion` turns, on-disk state, resume across sessions, validate-each-beat wiring.

Two modes: **setup** (first time for a game) and **continue** (every session after).

## 4. State model — three artifacts, clean roles

| Artifact | Role | Mutability |
|---|---|---|
| `design_book.md` | **Intent.** Premise, player, economic engine, time model, cast + arc shapes, location graph, and the loose end-to-end roadmap. | Stable. Changes only via an explicit "amend the book" action, logged in the ledger. |
| `authoring_state.json` (the **ledger**) | **Plan + bookkeeping.** The living beat list, a structure registry, the next-up queue, a decisions log. | Living. Rewritten every turn. |
| `toml_phases/*.toml` | **Built content.** Setup writes the scaffold (settings, metadata, locations, npcs, schedules). Continuation appends canvases. | Append + checked amendment only. |

**Sources of truth:** ledger = *plan*; TOML = *built*; book = *intent*. On resume the skill reads the ledger (cheap), reconciles it against the TOML (what is actually built), and reports exactly where things stand.

### 4.1 Ledger schema (sketch — finalized in implementation)

```jsonc
{
  "game_slug": "late_shifts",
  "schema_version": 1,
  "book_revision": 3,              // bumped each time design_book.md is amended
  "plan": [                        // the living roadmap; ordered but reorderable
    {
      "id": "beat_0007",
      "type": "location_reveal",   // see beat types §6.1
      "title": "Unlock downtown after first paycheck",
      "desc": "Player can reach downtown once paid_once is set; adds loc_downtown + 2 hubs.",
      "status": "planned",         // planned | active | authored | validated
      "deps": ["beat_0003"],       // beats/flags that must exist first
      "target_phase": "1_metadata_and_locations.toml",
      "introduces": { "locations": ["loc_downtown"], "flags": ["downtown_unlocked"] },
      "decided_at": null
    }
  ],
  "structure_registry": {          // what EXISTS — every amendment is checked against this
    "locations": ["loc_diner_front", "loc_cole_apartment", "..."],
    "npcs": ["hank", "cole", "..."],
    "flags": ["hired_at_diner", "cole_date_done", "..."],
    "schedules": [{ "npc": "hank", "rows": 8 }]
  },
  "next_up": ["beat_0007", "beat_0008"],
  "decisions_log": [
    { "turn": 12, "note": "Deferred Diana confrontation branch B per LO; kept A.", "book_revision": 3 }
  ]
}
```

The **structure registry** is the anti-drift mechanism: nothing may reference a location/NPC/flag absent from the registry, and adding one is an explicit, logged amendment (§6 step 3).

## 5. Setup phase — the one-time "special set of things"

A doctrine-grounded interview, **one question at a time via `AskUserQuestion`, always with ideas + options + a recommendation** — never a blank prompt. It asks *only* decisions that fork the skeleton; anything with a safe doctrine default is defaulted and named, not asked (YAGNI on the intake).

Question set (order is a guide, not rigid):

1. Premise / setting / player character.
2. Economic engine + time model (defaults offered from doctrine).
3. Cast — skill proposes NPCs + arc shapes from the premise (grounded in `doctrine/03_arc_shapes.md`); LO reshapes.
4. Location graph — skill proposes from cast + premise (containers / hubs / locks); LO reshapes.
5. Phase 2+ decisions — pregnancy / scandal / gallery / tracker, per Doc 65.
6. Kink / vocab ceilings.
7. The **loose end-to-end roadmap** — skill drafts it from everything above; LO reorders / cuts / adds.

Setup then writes `design_book.md` + the ledger + the **scaffold TOML** (phase `0_systems_spec` settings + `1_metadata_and_locations` metadata/locations/npcs/schedules) and **runs the first validate + build to prove the skeleton is green** before any beat is authored.

Output of setup = a buildable empty game + a populated ledger whose `plan` is the loose roadmap, every beat `status: planned`.

## 6. Continuation phase — what "continue" does each turn

The unit of work is **the next beat in the living plan**. A beat is *any* story development, not just an NPC arc.

### 6.1 Beat types

- `npc_intro` — introduce a new NPC (schedule + on-ramp).
- `location_reveal` — discover/unlock a new location (def + lock + schedule wiring + unlock beat).
- `arc_escalation` — advance an existing NPC's lanes/stage.
- `cross_npc` — a beat spanning two+ NPCs (authorable once all endpoints have skeletons).
- `economic` — a money/progression milestone (buy a home, lose a job, debt comes due).
- `story_turn` — a narrative pivot / world event.
- `capstone` — a Doc 57 one-shot (`is_repeatable=false`, priority ≥9, flag-gated + flag-setting).

### 6.2 The loop

1. **Resume & report.** Read ledger, reconcile vs TOML, report "here's where we are, here's next up."
2. **Propose the beat — with ideas and options.** Pitch the next beat(s) from the roadmap *with concrete creative options and a recommendation*. LO picks, reshapes, or injects a brand-new beat. New/changed beats update the roadmap.
3. **Amend structure if needed, properly.** If the beat needs a new location/NPC/flag, add it *whole* (def + lock + schedule + unlock beat) and register it in `structure_registry`. Nothing dangles. **This is the load-bearing invariant: structure only changes through an explicit, checked amendment — never silent drift.**
4. **Author** the beat's canvases into the correct phase file (§8).
5. **Validate** (§7). Red → fix before the beat is marked done.
6. **Update ledger** — beat → `validated`; roadmap revised if new beats emerged; decision logged; `book_revision` bumped if the book changed.
7. **Build** the full HTML at milestones / session end / on demand.

The roadmap reshapes freely turn to turn; the hard structure grows only through step 3.

## 7. Validation — the safety net

After **every beat**, in order:

1. `python scripts/merge_toml_phases.py games/<slug> --validate` — assembles `7_final_game.toml`, parses it via `tomllib` (catches malformed TOML, e.g. multi-line inline tables).
2. `python manage.py package_from_toml --file games/<slug>/toml_phases/7_final_game.toml --owner-id <uuid> --output games/<slug>/output --dev` with schema + flag-chain validation — but see §7.1 on build cadence.
3. **Doctrine self-audit.** The skill runs the relevant `§7` audit checklists against what it just authored:
   - reachability triad (`doctrine/10` §5): NPC-schedule ∩ canvas-window ∩ player-present-and-awake,
   - dead-presence / D72 presence floor (`doctrine/02` §8.11–§8.15, D72-R6/R7/R8),
   - locked-location unlock contract (`doctrine/10` §5.4, Cases A/B/C),
   - `[settings]` scoping (clothing/rent/phone keys under `[settings]`, not bare),
   - `is_container` swallow (no activities/ambients/capstones attached to a container location).

   Red on any → fixed before the beat is `validated` in the ledger.

### 7.1 Build cadence

- **Validate every beat:** steps 1 + 3 always; step 2 in `--validate`-only / fast mode where practical.
- **Full HTML build at milestones:** end of an arc, end of a session, or on demand — to avoid paying full build cost + image-warning noise on every tiny beat.

### 7.2 Honesty note — the self-audit is not yet automated

The structural checks in step 3 are **not** automated linters today (`prompts_v2/PREVENTION_LINTER_SPEC.md` is still a spec, unbuilt). So the self-audit is *the skill reading the doctrine and checking against it* every beat — reliable but enforced by diligence, not by code. **Building the real linters is a natural follow-on, explicitly out of scope for this work** (§10).

## 8. Corpus restructure (`prompts_v2`)

- `stages/01_game_book_prompt.md` → a **setup-interview** spec: the §5 question set + the book/scaffold output contract. Preserves the existing doctrine cite-only sections.
- `stages/02_toml_generation_prompt.md` → a **per-beat authoring** spec: given one beat + book + ledger + current TOML, author that beat's canvases under the full lane/hub/schedule/lock doctrine. This is the reusable engine the continuation loop calls every turn (replacing the whole-game pour framing).
- A short **structure-discipline** doctrine note (stable-and-extensible structure; amendments; no silent drift) folded into existing doctrine — **no new rule number**.
- `COMPREHENSIVE_SYSTEM_REFERENCE.md` regenerated after the edits (`scripts/regen_comprehensive_reference.py`).

⚠️ `stages/01` §6/§7/§8 and `doctrine/10` §6/§7/§8 are externally referenced ~8x (PREVENTION_LINTER_SPEC, COMPREHENSIVE, cross-doc cites). Restructuring must preserve external anchors or update every referrer in lockstep.

## 9. File layout (per game)

```
games/<slug>/
  design_book.md            # intent (setup output, amended explicitly)
  authoring_state.json      # the ledger (living)
  toml_phases/
    0_systems_spec.toml         # settings  — written at setup
    1_metadata_and_locations.toml  # metadata/locations/npcs/schedules — setup + amendments
    2_one_shots.toml            # } continuation appends canvases
    3_activities.toml           # }   to the phase matching the beat type
    4_story_arc.toml            # }
    5_scenes.toml               # }
    8_phone.toml                # }
    6_dev_shortcuts.toml        # dev only
    7_final_game.toml           # GENERATED by merge — never hand-edited
  output/                   # built HTML (milestone builds)
```

Beat-type → phase-file routing (matching existing LS organization) is finalized in implementation; e.g. `arc_escalation`/`cross_npc`/`capstone` → `5_scenes.toml` or `4_story_arc.toml`, `economic` rent/phone → `0_systems_spec`/`8_phone`, `location_reveal` → `1_metadata_and_locations.toml`.

## 10. Out of scope

- **No engine change.** `entry_conditions`/`blocked_message`, schedules, settings all already exist.
- **No schema change.** The skill emits TOML valid against today's `template_import.py`.
- **No automated linters.** `PREVENTION_LINTER_SPEC` stays a spec; the self-audit is doctrine-read diligence (§7.2). Building the linters is a separate future effort that would harden this loop.
- **No RTS-style discovery-hiding** of locations (documented as a known evolution in `doctrine/10` §5.4; not built).
- **No migration** of existing games (Late Shifts etc.) into the new flow; they remain editable the old way. LS is the natural first *shakedown* target if desired, but not a required migration.

## 11. Build decomposition (for the implementation plan)

Five fairly independent pieces; rough dependency order:

1. **Ledger schema** — finalize `authoring_state.json` shape (§4.1). Foundational; everything depends on it.
2. **Corpus restructure** — split `stages/01` + `stages/02`, add the structure-discipline note, regen COMPREHENSIVE (§8). Careful — external anchors.
3. **The skill** — `/author-game` with setup + continue modes, `AskUserQuestion` orchestration, on-disk persistence, resume/reconcile (§5, §6).
4. **Validation harness** — wire merge + `package_from_toml --validate` + the doctrine self-audit into the per-beat loop (§7).
5. **Shakedown** — run end-to-end on a fresh throwaway concept (setup → ≥3 beats of varied types → green build) to prove the rhythm. This is the first real run; there is no separate prototype.

## 12. Risks

- **Loop rhythm.** The whole idea rests on the continuation loop *feeling* smooth. We are de-risking it in the shakedown (§11.5) rather than a separate prototype — if the rhythm is awkward, expect to revise the skill before declaring done.
- **Self-audit reliability.** Until linters exist, structural correctness depends on the skill faithfully running the checklists. Mitigate by making the checklist a literal step the skill must emit results for, per beat.
- **Corpus anchor breakage.** §8's external references must be preserved or updated in lockstep; verify with a grep sweep post-edit.

## 13. Shakedown findings (2026-06-03)

First real run, on the game **Last Call** (inherited dive bar + loan-shark weekly payment; female
owner; 5 NPCs; 9 locations). Scope run: setup → 2 continue beats (`npc_intro`, `location_reveal`).

**What worked (the design is validated):**
- **Setup mode** produced `design_book.md` + a seeded `authoring_state.json` + a scaffold
  (`0`/`1`/`2` phases) that built green first try — `✓ validation`, `✓ all flag chains valid`,
  `index.html`. The minimal boot canvas (gap-test fix C) was necessary and sufficient.
- **Continue loop rhythm is smooth** — propose-with-options (AskUserQuestion) → author → validate →
  ledger update → reconcile, twice, each ending green with `drift: []`. This retires the §12 "loop
  rhythm" risk.
- **The whole-amendment anti-drift discipline holds.** beat_0009 added `loc_shark` + its lock +
  unlock flag + a reachable setter + content, all in one move, and the locked-location flag chain
  validated. Deferring `loc_shark` out of the scaffold (introduced at its reveal beat) kept setup green.
- **Patterns-only ledger works** — the JSON is hand-edited each turn; reconcile is a ~12-line inline
  snippet. No helper module missed.

**The one real gotcha (now hardened in the skill):**
- **Don't gate a canvas trigger on an engine-set flag.** beat_0009 first gated the summons canvas on
  `bar_seized` (the rent `eviction_flag`). `package_from_toml` failed: `✗ bar_seized NEVER SET`. The
  flag-chain validator (`v2.py:_build_flag_unlock_map` / `validate_flag_chains`) only adds
  *canvas-set* (and phone-reply) flags to the unlock map; engine-set flags (rent `eviction_flag`,
  `[engine.daily_tick]` flags) are invisible to it. LS sidesteps this by gating its `rent_evicted`
  content in a **phone thread** (delivery conditions aren't flag-chain-validated), not a canvas
  trigger. Fix applied: gate on a canvas-set flag (`debt_explained`) + the Collector's presence.
  Added as a 6th `beat-authoring.md` self-audit check. **Possible future engine improvement:** the
  validator could allowlist the configured `rent_eviction_flag` (it's a known engine-provided flag).

**Outcome:** the system works end-to-end. Last Call is a real game kept on disk (`games/last_call/`,
gitignored like all games); 11 beats remain `planned` in its ledger for future continue sessions.
The deferred Phase-2 corpus restructure (stages/01+02 setup/per-beat split) is still pending LO's
in-flight `prompts_v2` WIP settling.
```
