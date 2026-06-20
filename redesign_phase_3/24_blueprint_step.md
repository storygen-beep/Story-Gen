# The BLUEPRINT step — splitting STORY (Step 4) from STRUCTURE (Step 5)

The pipeline gained a step. The old jump from a loose story design straight to TOML hid every structural
decision — which lane, what gate, where it fires, the flag wiring, the scene order — inside a rushed
"seed the plan" action at the top of authoring. That jump is now its own deliberate step: **Step 5 — Blueprint**.
The four content steps tile by verb — **imagine (4) → decide (5) → grade (6) → emit (7)**.

**Status:** wired into the skill 2026-06-13. The pipeline is now **8 steps** (was 7). Pre-restructure snapshot:
`redesign_phase_3/_skill_snapshot_2026-06-13_pre_blueprint/` (restore = copy `author-game/` back). Operational
artifact = `references/step-5-blueprint.md`. Extends `23` (the content-question framework); relates to `22` (the
machine — now wired at Blueprint), `09` (desire ladder), `16` (`run-mode.md`).

---

## The problem this solves
The user authored *the inheritance* with the 7-step skill and felt the work "move too fast" at the jump from
design to TOML. Two faults, one root cause:
1. **No per-NPC scene list, read as a descent.** The story brief described an arc as prose; the concrete
   lane-tagged scene list (the thing you read down the page to feel whether the fall lands) was buried in one
   under-specified line of the R7 brief and never reviewed as a list.
2. **Step 4 mixed story and mechanism.** Lane/gate/threshold jargon polluted the creative seat, and the actual
   structural decisions leaked into authoring — making `run-mode.md`'s promise ("the design book is the review
   surface; authoring is faithful translation") a half-truth, since authoring secretly re-decided every lane.

## The fix: a deliberate STRUCTURE step between STORY and REVIEW
- **Step 4 — Design** is lightened to **STORY ONLY**: end-state, voice, the descent as lived experience. The
  four tripwire words — *lane, threshold, flag, placement* — are banned from a Step-4 brief.
- **Step 5 — Blueprint** (NEW) takes the story and **decides the structure**: the discrete, named,
  lane-tagged, ordered, gated, placed scene list, written to the design book (never TOML), plus the seeded
  ledger `plan`. It is the **one step allowed to ask/mention structuring** (a deliberate `run-mode.md`
  relaxation — deciding lanes/order/gates well is its whole job). Ten jobs, run subject by subject
  (player → NPCs → world) then a holistic wiring/order/opening pass.
- **Step 6 — Feedback** (was 5) is purely the examiner: grade the blueprint, suggest fixes.
- **Step 7 — Authoring** (was 6) translates the blueprint to TOML + prose, re-deciding nothing. The
  plan-seeding it used to rush at entry moved up into Blueprint.

This makes the design-book-as-review-surface contract finally **true**: by the time authoring runs, there is
nothing left to decide — only to build.

## The four-verb seam (the razor lines that prevent step-overlap)
- **Story ↔ Blueprint:** Step 4 names moments as prose; Blueprint turns them into a list with ids/lanes/gates.
  Blueprint *structures* the story, never *extends* it — a thin spot bounces UP to Step 4.
- **Blueprint ↔ Feedback:** Blueprint OWNS the DAG build + feeder count (generate-time); Feedback CONFIRMS
  them whole-game (review-time), never re-builds. (The `content-framework.md` owner/defer firewall, preserved.)
- **Blueprint ↔ Authoring:** Blueprint decides the plan + gates + spine; authoring emits, re-deciding nothing.
  Authoring's "read the brief, don't drift it" became "read the **blueprint**, don't re-decide it"; its D6
  engine-limit bounce now lands on the blueprint section.
- **Trait-spine handoff (gap-risk, closed):** the spine decision (odometer vs throttle, which trait by shape)
  moved *totally* to Blueprint — Step 4 says nothing about which trait gates; authoring reads the chosen spine.

## What also shipped
- A **simple-language communication rule** (`run-mode.md` Law 2 + a `SKILL.md` pointer): every note, proposal,
  and question to the user uses plain everyday words, jargon glossed on first use. Generalizes the user's
  repeated "explain in simple words."
- The ledger gained an additive **`blueprint` block** `{ player, npcs, world, wiring }` (same supply→demand→
  stage ordering as `deep_design`); `pipeline_phase` gained `"blueprint"`; `schema_version` stays **2**.
- The now-false invariant "`plan` stays empty until authoring" was corrected — `plan` is seeded by Blueprint.

## Self-check (the restructure is coherent)
- The renumber (Feedback 5→6, Authoring 6→7) is applied across all 8 affected files; a grep for stale tokens
  (`step-5-feedback`, `7-step`, `Steps 1–5`, `# Step 6 — authoring`) returns only the one intentional historical
  mention of the old "content roster."
- The phase chain reads consistently end to end: `casting → deep_design → blueprint → feedback → authoring`.
- Backward-compatible: the inheritance sits at `authoring` (terminal) and is byte-unchanged; phase aliases for
  old `npc_arcs`/`roster` ledgers are intact; `schema_version` unchanged.
- Step 4 is net **shorter** (184 → 139 lines — it lost the mechanism half); SKILL.md 116 < 120;
  `step-5-blueprint.md` 145.

## Cross-references
`references/step-5-blueprint.md` (the new step) · `references/step-4-deep-design.md` (lightened to story) ·
`references/step-6-feedback.md` (renamed) · `references/beat-authoring.md` (Step 7; plan-seeding moved out) ·
`references/ledger-schema.md` (the `blueprint` block) · `references/run-mode.md` (the relaxation + the
simple-language rule) · `references/content-framework.md` (the three touches). Extends `23`; relates to `22`.
