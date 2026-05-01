# 09 — Future Polish & Nice-to-Have Items

> **Created 2026-04-29.**
> Sibling to `08_Engine_PRD_Phase2_Additions.md`. Backlog, not commissioned work.
> None of the items here block the Phase 2 doctrine. The redesign ships without any of them.

---

## §0 What this doc is

A captured list of polish items that were considered for inclusion in the Phase 2 PRD (`08_Engine_PRD_Phase2_Additions.md`) and explicitly left out per the user-locked "Phase 2 doctrine items only" scope decision. Each one would make Phase 2 noticeably better in a specific way — but no one of them is required for the doctrine to function.

This is a wishlist, not a plan. Use it as the menu of fixes when Phase 2 playtest reveals friction in a specific spot, or when there's bench time after E9–E11 ship.

The PRD covers the items the doctrine *demands*. This doc covers the items the doctrine would *appreciate*.

---

## §1 Player-facing polish

### Live NPC location sidebar
*(E3 from the original PRD, currently deferred.)*

Today the player sees each NPC's traits in the sidebar but has to open the Schedule Page to see where every NPC is right now. RtS's right-sidebar roster — "Frank: Office | Diana: Kitchen | Ryan: Yard" — is one of the things that made it actually playable, because the player could plan their day at a glance.

**Why beneficial.** Turns the schedule from a reference page you check sometimes into a planning tool you read every turn. Makes "I should head to the office now while Frank's there" a thirty-second decision, not a Schedule-Page detour.

**Cost estimate.** Medium. Was scoped at P2 in 03; the rendering primitive (sidebar widget) exists, the data primitive (NPC schedule lookup) exists. Wiring is the work.

### Toast notifications on stage transitions

When a stage flag flips (e.g., `frank_stage` 1 → 2), fire a small sidebar toast: "Things have shifted with Frank." E11 (in the PRD) already puts the named stage in the sidebar; this celebrates the *moment* of change so the player notices it instead of finding out three days later when a new button appears at a hub.

**Why beneficial.** Makes flag movement feel like a story beat instead of a silent state shift. The whole doctrine relies on "the player sees state move" — toasts close the loop on the rare moments when state moves dramatically.

**Cost estimate.** Low. The notification primitive exists (used today for trait changes). Hook into the stage-advancement code path (which E9 already touches).

---

## §2 Engine plumbing polish

### `[[npcs.arc_stages]]` as a first-class TOML schema

✅ **Shipped 2026-04-30** in commit `906869b`. Un-deferred during Phase 2 implementation planning to give E9/E10/E11 a registry-based foundation rather than a regex fallback over `^[a-z_]+_stage$`. Shipped form is simpler than the version originally proposed in this doc: `arc_stages = ["Suspicious", "Warm", ...]` — just the label array. Advancement logic stays in `[[engine.stage_helpers]]` and effects, not in the schema. See `08_Engine_PRD_Phase2_Additions.md` §11.2 for the as-built spec.

### StagesPage in dev mode

A debug page listing every NPC + current stage + last advancement day + which specific conditions are blocking the next transition. Today this information is scattered across StatsPage, FlagsPage, and a mental cross-reference of helper definitions.

Sample render:
```
Frank — Stage 2 (Restrict)
  Last advanced: Day 12
  Next transition (Stage 3): blocked
    ✓ corruption ≥ 50  (54)
    ✓ frank_restrict_declared  (true)
    ✗ frank.tease_count ≥ 5  (currently 2)
    ✓ frank.arousal ≥ 30  (33)
```

**Why beneficial.** When playtesting reveals "Frank's stuck at Stage 1," you see *why* in one place. Saves hours of debugging per playtest session — and Phase 2's vertical slice will need many playtest sessions.

**Cost estimate.** Low–medium. New passage rendered in dev mode only; reads from existing helper definitions and stage flags.

### Hint system completeness (PRD 09)

✅ **Shipped 2026-05-01** as PRD 09 batch (E14, E15, E16, E17, E18, E20, E21, E22, E23). Closes the recurring authoring drift pitfalls captured in `11_Hint_Authoring_Guide.md` and the Ryan-class stuck-state bug surfaced during the Long Summer Test Slice playtest.

8 engine extensions covering: precise multi-gate transitionals (E14), cross-NPC prerequisites (E22), global hint rendering (E15), cleared-but-not-triggered detection (E17), counter sidebar bars (E18), decay warnings (E20), cooldown opt-in (E21), build-time hint linter (E23). E16 (visual split for hint text) shipped slightly earlier in the same arc.

See `12_Engine_PRD_09_Hint_System_Completeness.md` for the as-built record (per-feature implementation notes, slice usage audit, known limitations).

---

## §3 Authoring polish

### Confabulation registry

From `00_TLS_Phase2_Diagnosis_and_Direction.md` Part 4 — a small file listing every invented background detail in the prose (mile distances, mug origin stories, neighbor families) with a disposition:

| Detail | Where it appears | Disposition |
|---|---|---|
| "three hundred and twenty miles" | `event_arrival_at_franks` | flag-bind to `mayas_drive_distance = 320` |
| "the chipped Hayes Hardware mug" | `arrival`, `kitchen_with_frank` | decorative — never reference again |
| "by the seventh shift" | rewrite drafts, removed | pure confabulation; no payoff possible — cut |

The doctrine pushes the writing toward terser prose, which actually makes confabulation drift *more visible* — but it doesn't audit itself. The registry catches invented details before they compound.

**Why beneficial.** Prevents "fiction debt" — the situation where prose has implied a payoff that the engine has no flag to redeem. Either the payoff gets authored or the implication gets cut. The registry forces the decision instead of letting the implication accrete.

**Cost estimate.** Tiny — it's a markdown table maintained alongside the rewrite. The benefit comes from the discipline of maintaining it.

### Phase 1 → Phase 2 migration helper script

A small script that reads Phase 1's `2_story_canvases.toml` + `3_activities.toml` and emits a stub `toml_phases_v2/` skeleton with each Phase-1 canvas tagged for conversion:

- *collapse to branch* — fold into a flag-gated branch inside an existing repeatable shell
- *preserve as one-shot* — keep `is_repeatable = false` for genuine one-shots
- *archive* — Phase 1 content with no Phase 2 home

Today this is a manual audit across 218 canvases.

**Why beneficial.** Turns weeks of audit work into hours of script-then-review. The script can't make the design decisions — but it can pre-populate the conversion table and flag obvious patterns (high-priority non-repeatable canvas that auto-fires at a location → almost certainly a "collapse to branch" candidate; canvas that fires at midnight on a specific day → likely a one-shot to preserve).

**Cost estimate.** Low. ~150–250 lines of Python reading the existing TOML schema and emitting a CSV/markdown audit. One-time-use, but valuable enough to justify the build.

---

## §4 Items deliberately skipped (even if bench time appears)

These came up during Phase 2 planning and were rejected, with rationale. They stay rejected unless something material changes in the redesign.

### Random integer setter for scene-internal RNG

The doctrine's anti-staleness mechanism is **image rotation** per master spec §2.4, plus stage cascades for content variety. Adding scene-internal RNG would enable prose-pool rotation, which is explicitly *not* a verified RtS pattern. The author would reach for it the moment it existed; the doctrine would erode.

**Stays skipped unless:** playtest specifically reveals that image rotation + stage cascades aren't enough variety for high-traffic ambient activities (sleep, shower, eat). Even then, more stage branches is the doctrine answer, not RNG.

### `auto_fire = false` field on canvases

Sugar over existing `priority` semantics. The doctrine works fine with current priority arithmetic — high-priority one-shots pre-empt hubs; low-priority repeatables yield. Making the intent explicit at the canvas level doesn't change behavior; it only changes readability.

**Stays skipped unless:** a real authoring bug surfaces where someone meant "don't pre-empt the hub" and got the priority wrong. So far that hasn't happened.

### Schema deprecation of `linked_canvas`

Both `linked_canvas` and `linked_flag` work in the engine. `detectStoryPosition` (v1.py:4070) checks both. Forcing a migration adds churn for zero functional gain — Phase 2 TOMLs use `linked_flag`; Phase 1 TOMLs continue working with `linked_canvas`.

**Stays skipped indefinitely.** Schema cruft has a real cost (more docs, more validator paths) but a deprecation has a higher cost (breaking change, save migration concerns). Net: leave both fields supported.

### Hub-first rendering posture as engine primitive

The doctrine wants hubs to render every visit, with first-time content as a flag-gated branch *inside* the hub. Today this is achieved by setting `is_repeatable = true` on the hub and `is_repeatable = false` only on genuine one-shots. The doctrine works without an engine primitive for "hub-first."

**Stays skipped unless:** the rewrite reveals an authoring pattern where this would catch a class of bugs. So far the doctrine + priority semantics handle it cleanly.

---

## §5 Suggested priority order

If polish items get scheduled, this is the rough sequence:

| Order | Item | Why first |
|---|---|---|
| 1 | StagesPage in dev mode | Pays back during every playtest session of the rewrite |
| 2 | Live NPC location sidebar (E3 revisit) | Player-facing, biggest single UX upgrade |
| 3 | Phase 1 migration helper script | Pays back during the rewrite — useful before Phase B starts |
| 4 | Toast on stage transitions | Player-facing, low effort, signals matter |
| 5 | Confabulation registry | Process discipline; ongoing |

Items 1 and 3 are roughly engineering / authoring tooling. Items 2 and 4 are player UX. Item 5 is a discipline that pays back over the full rewrite.

None of this is on the critical path. All of it is real value.

---

## §6 Cross-references

- **`08_Engine_PRD_Phase2_Additions.md` §5** — explicitly excluded items (some of which appear here as "future polish," some as "deliberately skipped").
- **`03_Engine_Changes_PRD.md` §E3** — the live NPC location sidebar item, deferred there, tentatively revived here as polish.
- **`00_TLS_Phase2_Diagnosis_and_Direction.md` Part 4** — confabulation diagnosis that motivates the registry.
- **`02_NPC_Stage_Chains.md`** — stage chain artifact now formalized in the shipped `[[npcs]].arc_stages` schema (see `08_Engine_PRD_Phase2_Additions.md` §11.2).
- **`archive_02_TLS_Rewrite_Spec_2026-04-29.md` §9** — migration plan for existing canvases (recommends parallel rebuild); the migration helper script supports that approach.
- **`11_Hint_Authoring_Guide.md`** — author-facing convention guide; updated 2026-05-01 to reflect the engine support shipped in PRD 09.
- **`12_Engine_PRD_09_Hint_System_Completeness.md`** — as-built record of the PRD 09 batch (E14–E23) referenced in §2 above.

---

## §7 Status

This is a backlog document. None of the items here are committed work. They sit at "🟦 Captured, not commissioned" until decided otherwise.

When an item gets picked up, move it from this doc into a real PRD addendum (or a small standalone spec) and mark it 🟦 / 🟡 / ✅ there. Don't update this doc to track in-flight work — that's what the PRDs are for.

---

## §8 What this doc is not

It is not a PRD. It is not a roadmap. It is not a commitment.

It is a captured list of items the redesign would benefit from, kept in one place so they don't get re-discovered (or re-rejected) every few sessions. If Phase 2 ships and feels great without any of these — perfect. If a specific friction surfaces, this is the first place to look for an existing answer.
