# Step 6 — feedback: review the whole blueprinted game against the framework (before authoring)

Step 5 **BLUEPRINTED** the structured scene list. Step 6 **REVIEWS** it. Run the §1–§5 question set
(`references/content-framework.md`) against the finished `design_book.md` as a checklist — **every NO is a gap;
fix it before authoring.** This is the completeness gate the old "content roster" never was: when this pass ran
on `the_inheritance` it surfaced **8 real content gaps**.

It runs off the **same question set the blueprint was built against**, so design and review can't drift. **No
roster is produced** — the design book already holds every scene in the blueprint (the player blueprint, the
per-NPC scene lists, the world blueprint); the old roster was a re-listing, so there's nothing to re-list.

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
- **Supply-vs-demand balance (§2E).** The *count* is OWNED by Step 5 Blueprint (generate-time). Here you **confirm
  it whole-game**: every NPC seduction floor is reachable from the player's feeder supply through ordinary play
  (no starvation). Don't re-count — confirm.
- **The machine / DAG verify (§4E).** Inherently a whole-game check (you can't DAG-check until every arc
  exists). Trace the F1 cross-reads: **core loop closed** · **every core NPC placed** (no island) · **DAG, no
  cycle** (every arc cold-start-reachable — D2) · **no arc ENTRY gated** (D1) · **every cross-gate telegraphed**
  naming the gating arc (D3). **A cycle is a deadlock the build won't catch.**
- **Day-breadth (§2F).** Walk a representative mid-game day and count the DISTINCT threads the player can choose
  that aren't the main-NPC grind (solo self-care · exhibition · a capability/skill ladder · a second economy · an
  exploration crawl · ambient walk-ins). A day that is **one chore + one NPC** is a thin-day gap **even when each
  is fused** — it passes every per-item row below, so it's caught only here. Bites even when §2E is vacuous (an
  inverted protagonist with no feeder economy still needs a day worth living). **But check thin-on-purpose first:**
  a *declared* lean thread (a §1B still-point protagonist, a deliberately quiet valley) is a design choice, not a
  gap — only an unintended thin day is flagged. Floor ~2–3 live threads; fix with
  the day-depth menu (`references/system-patterns.md` §7).

## Surfacing & fixing gaps (the navigation)
**Propose the gaps as choices** (`run-mode.md` → "Navigation at junctions"): which gap to fix first — **Mode A**
on any gap whose fix changes the game's identity (e.g. "no fail-state was declared — wire a soft-fail clock, or
declare no-failure on purpose?"), **Mode B** for routine fixes. A fix **bounces UP** to the blueprint (Step 5),
the story (Step 4), or to Step 2 — it's never silently patched into TOML. Log each to `feedback.open_gaps` with a
status; a gap deliberately deferred past the frontier is logged as a **telegraphed locked-visible seed**, never
a silent cut.

## Self-check before authoring
- **Both tracks present** — there IS a player/world feeder catalog (incl. reactive-world rows), not only NPC
  arcs. *(The blind-spot test.)*
- **The daily loop is live, not décor** — every repeated self-care/chore at a location an NPC shares hosts
  ≥1 NPC walk-in OR a player-lewd feeder branch (the fused unit, `references/lanes.md` Lane 3); none ship as a
  bare restore (the dead-bath / dead-kitchen gap). ≥1 body-stat (hygiene/energy) *triggers* a routine, not
  just colors prose (`references/trait-catalog.md`). A self-care chore that hooks into nothing where someone is home —
  or a housemate's home block left offscreen so nothing can collide with it — is a gap.
- **No unclamped banded stat (the vanishing-HUD lint)** — every `op=add` on a banded body-need/resource stat
  (`energy`/`hygiene`/`charge`/`coin`) clamps or caps into its band range; unbounded, the value leaves its bands
  and the sidebar card silently disappears (`references/trait-catalog.md` §4). Reads as a *missing* HUD element,
  not a wrong number — this bug shipped twice before the lint existed.
- **Shared-private-space (occupancy) beats are built right** (`references/lanes.md` Lane 3 shared-space) — for a confirmed
  shared room (a bathroom): (a) the room stays **enterable** (NO hard `entry_conditions` unless genuinely
  sealed — a hard lock makes a dead-end screen); (b) occupancy gates the **activities** (bath `is_absent`,
  peek `is_present`), and the **peek lives ON the room canvas**, not a hallway; (c) the room has a **dynamic
  occupant description**; (d) caught = **catch-then-react** on the shower (chance, gated who's-home, **not** a
  fixed time window); (e) **register is RTS-flat** — peek/caught base beats ≈35–40 words per beat, the player's read in
  one `thought_bubble`, **no interior-monologue aphorisms on a daily-repeat surface** (`references/rts-flat-prose.md`);
  dialog + density only at the once-per-arc deepest tier.
- **Every scene serves a WANT** (the desire ladder) — no meter-exercise content.
- **The player is the erotic subject, and the heat is on the page** (the arousal gate, `references/rts-flat-prose.md` Rule 9 + §7 check 7) — the everyday texture keeps the player aroused-and-acting (words on her body, not the room/plot/apparatus); no payoff or repeatable sex surface is elided to a closed door + a stat bump; the person/PC isn't an accidental third-person spectator (a declared still-point/owned PC per §1B is fine only if said on purpose). Catches the cold game that passes person/density/mode and still reads as noir — `vesper` (watched, plot-lexicon) and `the_inheritance` (clean ratio, every act skipped) both fail here.
- **The Quests page reads as one surface** (`references/quests.md`) — the Story-Goals spine + a section per arc'd
  NPC (each a one-live-at-a-time milestone or stepped-band chain) + an end-of-content card; **no card sits on a
  met numeric goal with no `ready_canvas`/`terminal`** (the Frame-3 blank-sidebar trap), no dangling fake
  objective, no dev-speak. The `npc_panel` `next` row mirrors it for free.
- **Tiers populated** — bootstrap (`corr 0`) + flash (`corr 15`) feeders exist, not just deep capstones.
- **Economy balanced** (§2E confirmed) — every NPC floor reachable through ordinary feeder play.
- **What compounds is declared** (§2C · Step 2 §4) — the growing owned thing is named with content-unlocking
  states, or "nothing compounds" is on the page as a choice · every progress-repeatable lands a deposit the
  player can SEE (`references/lanes.md` Lane 3) · the presence floor and Lane-2 texture stay exempt.
- **The machine verified** (§4E — a REAL check): core loop closed · every core NPC placed · DAG no cycle · no
  arc ENTRY gated · every cross-gate telegraphed.
- **Reactivity present & wired** (§4) — state-crossings, outfit reactions, and the **loses-ground** axis (§4F)
  all have consequences authored, not just declared.
- **Voice carriage (Rule 4)** — per NPC, are the hub + the hot/turning-point/capstone beats carried by the
  character's own `dialog` blocks, or narrated *about* them ("she asks, he says")? An arc that summarizes its
  exchanges at the beats that matter reads as monologue-about-the-NPC, not a scene with them — flag it, and
  hardest when a capstone or sex scene narrates the encounter. Exempt only where no one's present to speak
  (solo, unseen voyeur, a capstone's interior stretches); an ambient where the NPC is *present* should still
  give them a line.
- **Systems declared** (§1E) — every optional system is on/off on purpose; none half-wired.
- **Fail-state form named** (§1C) — if failure exists, its form is named (danger · debt · deadline · decay)
  and wired to bite (§4F); if it doesn't, "no fail-state by design" is on the page **with its cost stated**.
- **Onboarding teaches the machine** (`references/onboarding.md`) — the opening is a linear funnel that
  surfaces each live system once (a fiction beat or a value-zero sidebar item), names the next action on
  frame one, shows a reason on every greyed gate, and states the win/fail contract. HARD rows: every system
  surfaced · named next action · no reason-less gate · every condition `version="1.0"` · onboarding canvases
  off containers.
- **Every NPC has a real entrance** (`references/npc-intro.md`) — each navigable NPC's hub sits behind a
  dramatized auto-fire first-contact (pretext + name-on-page + hook-as-want, sets `<npc>_opened_up`); no bare
  cold-spawn hub (the Hank shape). Checked per NPC met after the opening.
- **Archetypes & places fit the premise** · **ceilings honored** (player-track rows touching an NPC sit at that
  NPC's `references/kink-ceilings.md` ceiling) · **forced content only where the place ceiling allows** (§5B).
- **No silent caps** — deferred content is a telegraphed locked-visible seed, counted and logged.

## What the inheritance validation found (the expected yield — proof this works)
Running this pass on `the_inheritance` surfaced 8 gaps — most usefully: a **MAJOR** one (the advertised
foreclosure clock and Margaret's scheme are never wired to actually bite — the whole negative axis was
decorative, caught by §1C + §4F), three **NOTABLE** (no real owned-item economy — §2C; the phone underdelivers
its own promise — §5F; three of four repeatable loops have no in-loop menu — §3G), plus the missing
sidebar/HUD (§5F). The point: each gap is a question the *game* couldn't answer. Fix before authoring.

## Cross-references
`references/content-framework.md` (the question set this pass runs) · `references/step-5-blueprint.md` (what
it reviews) · `references/run-mode.md` (the navigation-at-junctions contract). Set `pipeline_phase = "authoring"` when the gaps are
closed (or telegraphed as deferred seeds) — Step 7 = `references/beat-authoring.md`.
