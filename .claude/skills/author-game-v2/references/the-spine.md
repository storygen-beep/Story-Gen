# The Spine — the game's decisions, one short page each

Read this in the **spine** phase: after the idea page is picked, before the board. The spine is
where the game's own answers are written down once, so the board, the sheets and every release build
on the same decisions.

**A spine page is a decision record, never a copy of the doctrine.** Each page is a table of this
game's answers and a pointer to the file that carries the rule. If a page starts explaining *why*, it
is repeating a reference — cut it and point.

## Page rules

- **Seven pages, SP1–SP7**, each from its template in `templates/spine/`, saved in
  `games/<slug>/spine/`. Tables first.
- **≤ 400 words a page**, counting words, not table pipes or dashes. Longer means a rule is being
  restated.
- **[REVIEW] → [READY]**, the same workflow as `the-sheets.md`. LO signs each page when LO has read
  it **(LO decided, D13)**.
- **One home per decision.** A page records the answer and names the ledger key that holds it
  (`references/state.md`); the ledger does not copy the page. `spine.pages[]` holds only each page's
  status and sign-off.
- **The spine changes only between releases**, as a reach-back change that lists every page and
  reader it touches.
- **Places on the spine are provisional until the board names rooms.** SP2's `where` and SP7's places
  are written before the map exists; re-pointing them to the board's rooms is a board edit, not a
  re-sign.
- The `SP` ids are the spine's own. `the-sheets.md` S1–S13 and `register.md` S1–S4 are other rules.

## SP1 · Time

The clock this game runs on: the starting day and hour, how long a day is in play, and **the overnight
list** — every flag and trait `[engine.daily_tick]` clears or moves while she sleeps. Rules:
`the-clock.md` C1–C6; `engine.md` §28 for the tick. Ledger: `[time]` and `[engine.daily_tick]` in the
TOML.

## SP2 · The ladders

Per person, one table: **who climbs** (`the-meters.md` W1 — the player, the cast, or both), the
**counter** the steps read and set, **at most two meters** beside it, and the **steps**. Each step
carries `where` (provisional, above), `when`, `gate`, and one **hint line** for the guidance page (`the-voice.md` R2;
`scripts/guidance_from_ladder.py` generates the cards from it). Four optional fields a step may carry:

| field | what it records | rule |
|---|---|---|
| `her_line_low` · `her_line_high` | her own thought at a low and a high level | `the-meters.md` W1b |
| `who_notices` | who reacts to what she did, or nobody | `the-meters.md` W5b |
| `refusal` | `parked` (the step comes back after a wait) or `final` (the button says "(ends his path)") | `the-surfaces.md` R5b · `the-arc.md` A3 |

Arc rules: `the-arc.md` A1–A14. Ledger: `board.who_climbs`, `board.ascent_tiers`,
`board.characters[].ladder`. `lint · the arc ladder` prints each person's longest chain.

## SP3 · Dependencies

A step that cannot fire until something else has happened: **another person's step**, **a window**
(a day and hours), or **a place** being open. One row each —
`{from: {npc, step}, needs: {npc, step} | {window} | {place}}`. A dependency written nowhere is found
the first time a player stalls on it. Ledger: `dependencies[]`.

## SP4 · Loop and pressure

The week's sums: what a full week of the income rungs pays, the obligation and its day, and whether the
obligation moves. Rules: `the-economy.md` R3, R3b, R3c; `the-want.md` §1b for a hold that is not money.
Ledger: `board.economy`.

## SP5 · The cast

How many people this release carries, and **the rule for adding one** — what a new person must bring
(a thread of her life, or a part in one she has; a ladder; a reason she wants them; `the-want.md` §6) before the cast grows. Ledger:
`board.cast{width, adding_rule}`.

## SP6 · Media and platform

Where the game is published and played (a phone first or not), the clip policy — which beats carry a
clip (`register.md` S1) — and **her face**, which is recorded once on the idea page (`want.face`,
`engine.md` §34b). Ledger: `board.media{platform, clips}`.

## SP7 · The release page

What this release is: the people in it, each person's top step, the places, **the door** it ends on,
its size, and the `--ship` BLOCK and REPORT lists (`the-release.md`, § Shipping the build). Three rows every release
page carries:

- **The promise, kept alive** — which beat in this release keeps the goal or the mystery alive
  (`want.promise`; `the-want.md` §0).
- **Scenes replay-ready: yes / no.** Decide it at the start — a scene is replayable when it is driven by
  flags and has no side effects — and build the gallery whenever. *(LO decided.)* The Process Review
  (`ROUND2_HOW_GAMES_GROW.md` §5) found replay is cheap to decide early and expensive to retrofit.
- **Signed** — by LO, with the date.

Ledger: `release_page` (`--ship` reads `door`, `people`, `signed_by_lo`, `signed_at`; the rest is
recorded, not gated).

## Checkpoint A — `scripts/shape.py`

The spine is finished when every page is signed and `shape.py <slug> --finish` passes. It reads the
ledger only and FAILS on: a step at an undeclared place (once the board declares places), hours that
are not a window, a trait the ledger never declares, a dependency on a missing step or in a cycle,
pressure the release's weeks cannot pay without a declared `shortfall`, a release person with no
ladder, a step with no `hint`, a door that is not a declared step, a promise with no beat on the
release page, a READY page unsigned, a gate the start (his meter's, or `board.player_start` for hers) plus the `raises` before it cannot reach (a trait in `board.daily_raises` or `board.repeat_raises` is not judged), a person with no age or
under 18 (in every mode), a thread whose person is not in the cast, a `keeps` outside the three or
`none — <why>`, and (strict) a system with no card. With `--finish`, or once the
phase is `spine` or later, a missing piece is a FAIL: an empty ledger never finishes the spine. Flags
in a step's gate are listed, not judged. Run it again before accepting any change to money, the
ending or the release page.

## What is not a spine page

- **Places** — the place sheets (`the-sheets.md`) and `board.map` are the record.
- **Saves** — `the-returning-player.md` is a rule for every game, not a choice this one makes.
- **Cheats** — the `[ui.cheat_page]` block in `templates/board.toml` is the record (`the-systems.md` SY7).

---

**Then:** when every SP page is [READY] and LO has signed it, set `phase = "spine"` in
`v2_state.json` and move to `references/the-systems.md`, then `templates/board.toml`.
