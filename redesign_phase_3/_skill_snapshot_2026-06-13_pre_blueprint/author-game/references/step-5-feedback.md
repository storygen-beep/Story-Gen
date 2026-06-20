# Step 5 — feedback: review the whole designed game against the framework (before authoring)

Step 4 **GENERATED** the game subject by subject. Step 5 **REVIEWS** it. Run the §1–§5 question set
(`references/content-framework.md`) against the finished `design_book.md` as a checklist — **every NO is a gap;
fix it before authoring.** This is the completeness gate the old "content roster" never was: when this pass ran
on `the_inheritance` it surfaced **8 real content gaps** (see `redesign_phase_3/23`).

It runs off the **same artifact Step 4 generated against**, so design and review can't drift. **No roster is
produced** — the design book already holds every scene in its subject briefs (the player thread, the per-NPC
R7 briefs, the world brief); the old roster was a re-listing, so there's nothing to re-list.

## The method (walk all five subjects)
For each subject's question clusters (§1–§5), read the design book and return a **verdict + the fix**:
- **held** — the game answers it richly; move on.
- **refine** — a partial/weak answer; note what's thin.
- **gap** — no real answer. A good question with no answer is a **content hole**, in plain language, not a gate
  dump. Most "gaps" mean the *game* is empty on that axis (not that the question is wrong).

Record progress in the ledger `feedback` block: `subjects_reviewed` + `open_gaps[]` (so the review and the
gap-fixing are resumable). Honor the framework's **owner/defer pointers** — review each cluster at its owner,
not twice.

## The two whole-game checks (the good part of the old roster step, re-homed here)
These were the load-bearing parts of the old Step 5; they survive as framework clusters:
- **Supply-vs-demand balance (§2E).** The *count* is OWNED by Step 4 Pass 1 (generate-time). Here you **confirm
  it whole-game**: every NPC seduction floor is reachable from the player's feeder supply through ordinary play
  (no starvation). Don't re-count — confirm.
- **The machine / DAG verify (§4E).** Inherently a whole-game check (you can't DAG-check until every arc
  exists). Trace the F1 cross-reads: **core loop closed** · **every core NPC placed** (no island) · **DAG, no
  cycle** (every arc cold-start-reachable — D2) · **no arc ENTRY gated** (D1) · **every cross-gate telegraphed**
  naming the gating arc (D3, `14` L7). **A cycle is a deadlock the build won't catch.**

## Surfacing & fixing gaps (the navigation)
**Propose the gaps as choices** (`run-mode.md` → "Navigation at junctions"): which gap to fix first — **Mode A**
on any gap whose fix changes the game's identity (e.g. "no fail-state was declared — wire a soft-fail clock, or
declare no-failure on purpose?"), **Mode B** for routine fixes. A fix **bounces UP** to the relevant subject
brief (Step 4) or to Step 2 — it's never silently patched into TOML. Log each to `feedback.open_gaps` with a
status; a gap deliberately deferred past the frontier is logged as a **telegraphed locked-visible seed**, never
a silent cut.

## Self-check before authoring
- **Both tracks present** — there IS a player/world feeder catalog (incl. reactive-world rows), not only NPC
  arcs. *(The blind-spot test.)*
- **Every scene serves a WANT** (the desire ladder) — no meter-exercise content.
- **Tiers populated** — bootstrap (`corr 0`) + flash (`corr 15`) feeders exist, not just deep capstones.
- **Economy balanced** (§2E confirmed) — every NPC floor reachable through ordinary feeder play.
- **The machine verified** (§4E — a REAL check): core loop closed · every core NPC placed · DAG no cycle · no
  arc ENTRY gated · every cross-gate telegraphed.
- **Reactivity present & wired** (§4) — state-crossings, outfit reactions, and the **loses-ground** axis (§4F)
  all have consequences authored, not just declared.
- **Systems declared** (§1E) — every optional system is on/off on purpose; none half-wired.
- **Archetypes & places fit the premise** · **ceilings honored** (player-track rows touching an NPC sit at that
  NPC's `doctrine/08` ceiling) · **forced content only where the place ceiling allows** (§5B).
- **No silent caps** — deferred content is a telegraphed locked-visible seed, counted and logged.

## What the inheritance validation found (the expected yield — proof this works)
Running this pass on `the_inheritance` surfaced 8 gaps — most usefully: a **MAJOR** one (the advertised
foreclosure clock and Margaret's scheme are never wired to actually bite — the whole negative axis was
decorative, caught by §1C + §4F), three **NOTABLE** (no real owned-item economy — §2C; the phone underdelivers
its own promise — §5F; three of four repeatable loops have no in-loop menu — §3G), plus the missing
sidebar/HUD (§5F). The point: each gap is a question the *game* couldn't answer. Fix before authoring. Full
list: `redesign_phase_3/23`.

## Cross-references
`references/content-framework.md` (the question set this pass runs) · `references/step-4-deep-design.md` (what
it reviews) · `references/run-mode.md` (the navigation-at-junctions contract) · `redesign_phase_3/23`
(the framework rationale + the inheritance validation). Set `pipeline_phase = "authoring"` when the gaps are
closed (or telegraphed as deferred seeds) — Step 6 = `references/beat-authoring.md`.
