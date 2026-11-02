# Design a game: premise, Want, idea, spine

`R` is `.claude/skills/author-game-v2/references/`, `T` is `.claude/skills/author-game-v2/templates/`,
and `DCHECK` is `python3 .claude/skills/author-game-v2-lean/scripts/design_check.py`.

Every phase here ends with LO choosing or signing. **You stop at every phase boundary and wait for
LO** (`.claude/skills/author-game-v2/SKILL.md` "Dispatch"). Read `games/<slug>/v2_state.json`
`phase` first and do only that phase's work. With no state file, start at the premise.

## Premise — no state file, and LO has not given a premise

Pitch three premises, each a different shape from the table in `R/the-want.md` §0. Each is two or
three lines: who she is, what holds her, what she wants. **Stop until LO picks one.**

## Want — LO has picked or given a premise

1. Write `games/<slug>/WANT.md` from `T/want.md`: one page, five parts (`R/the-want.md`, D16).
2. Create `games/<slug>/v2_state.json` with `phase = "want"` and the Want recorded in `want`, per
   `R/state.md`. Every person goes in `want.cast` with an age.
3. Run `DCHECK <slug>`.

Done when it prints `CLEAN`. Then tell LO the Want is ready to read, and **stop.**

## Idea — phase `want`, LO has read the Want

1. Run three `v2-pitcher` agents in one message, with no shared context: two on the main men, one
   on a thread of her life (`R/the-release.md` "The loop", step 2; `R/agents.md`).
2. Write `games/<slug>/IDEA.md` from `T/idea.md`. Name the model to beat: one of Course of
   Temptation, In Her Own Hands, Shady Deals or Cupid's Way, with what this game does better
   (`R/the-want.md` §0).
3. Show LO the three pitches. **Stop until LO picks one.** Then record the pick
   (`release_page.her_moment`) and set `phase = "idea"`.

## Spine — phase `idea`

1. Write the seven decision pages `games/<slug>/spine/SP1_…` to `SP7_…` from `T/spine/`, one at a
   time, each no more than 400 words and pointing at its rule (`R/the-spine.md`).
2. Mark each page `[REVIEW]` with `drafted_at`, and record it in `spine.pages[]` with
   `status = "REVIEW"`.
3. Run `DCHECK <slug>` after each page.

Done when every page you were asked for is written, `DCHECK` prints `CLEAN`, and LO has the pages.
**LO signs each page**: `[READY]`, `signed_by`, `signed_at`. When all seven are signed, run
`python3 .claude/skills/author-game-v2/scripts/shape.py <slug> --finish`. When it passes, set
`phase = "spine"`.

## Board and sheets — phase `spine` or `board`

Not covered here yet. Tell LO and use `/author-game-v2`.

## Footguns

- **Everyone is an adult, 18 or over.** If a premise gives someone a younger age, **write nothing
  and ask LO** whether to age them up or leave them out. It changes who is in the game, so it is
  LO's call (LO, 2026-10-04).
- **The goal has no date** (D8). "By day 60", "within 98 days", "by the end of her second year" and
  "week twelve" all broke this. If a premise puts a deadline on the goal, **resolve it yourself**:
  move the deadline into what holds her (section 2 of the Want), keep the goal undated (section 3),
  and tell LO what you moved (LO, 2026-10-04).
- **One phase per sitting.** Writing the spine while the phase was still `want` happened once
  (skill-test review G2). Each later page depends on LO's pick at the boundary before it.
- **Never sign for LO.** Not a spine page, a sheet or a release. A page you wrote is `[REVIEW]`.
- **Use only the model games that pass the adults-only rule**: the four named above.
- **A number said twice says the same thing.** If the Want gives a span or a price in two places, the
  two agree (`T/want.md`: "one span is never said two ways").
