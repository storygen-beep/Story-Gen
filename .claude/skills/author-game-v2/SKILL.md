---
name: author-game-v2
description: EXPLICIT-INVOKE ONLY — the experimental v2 of game authoring, run when the user asks for "/author-game-v2", "author-game v2", "v2 on <slug>", or "start a v2 game". Authors adult sandbox games as a never-ending release stream rather than as a story with chapters: one ascent meter that buys access, locations that must be filled before new ones open, explicit content living in the surfaces the player returns to, and every release ending on a visible locked door. Ships a runnable scoreboard (scripts/gates.py) whose thresholds came from measuring a top game's own source and, for the world/guidance/economy/prose gates, a field of 18 shipped sandboxes. Do NOT use for a plain "start a new game" / "continue writing <game>" / "add an NPC or beat to games/<slug>" request; those belong to the incumbent author-game skill until the user promotes this one.
---

# author-game v2 — the release stream

**v1 designs a story and then builds it. v2 designs a world and then feeds it forever.**

That is the whole change, and it came out of measurement, not taste. Ten snapshots of
Degrees of Lewdity's own source (2018-11 → 2026-07, 25 → 61 locations, 254k → 2.24M words)
measured against our own shipped game on one frozen instrument.

## The four commitments

Every one is a measured number, not an opinion. The evidence lives inline in
`scripts/gates.py`; the short version:

1. **The product never ends.** Endings *inside* the game are normal — DoL ships seven
   terminal fail-states — but the game itself does not close. On a subscription the revenue
   is an integral over months, and nothing anywhere pays for a finished browser sandbox.

2. **Fill before you widen — as a distribution, not a floor.** DoL's seed put 116,540 words
   across 25 locations: **mean 4,661, median 3,154**, and **one anchor** (`school`) holding
   **30% of all location prose**, with a long tail down to a 302-word bus station. Thin
   satellites are fine; a world with no centre is not. By 2026 the mean had risen to 24,564
   while locations only went 25 → 61 — depth outpaces breadth, every year.

3. **Heat lives where the player returns.** 7.5–9.3% of beats carry three or more explicit
   words — a ratio DoL held across eight years and twelve-fold growth — and the majority of
   them sit in re-enterable content. The measured failure case is the opposite: 95% of one
   game's explicit prose sealed inside a room with no exits, while every one of its nine
   repeatable sex loops scored zero.

4. **A release adds events, not places.** One full six-week DoL cycle: +196 units,
   +24,388 words, **zero** new locations, and all ten of its content commits were events at
   an existing place with an existing character. 55.6% of its commits were fixes.

## The three kinds of content

Named from what those release commits actually do, so the vocabulary owes nothing to
anything earlier:

- **STANDING** — a place or person she can go to and act on, repeatedly. The main surface.
  Carries the explicit floor.
- **TRIGGERED** — fires when her state matches. DoL's own commit language: *"during the
  weekends"*, *"when exposed"*, *"at high stress"*. For a female protagonist this is the
  main heat engine, not a garnish.
- **MILESTONE** — fires once at a threshold, then opens standing content.

**Every milestone names the standing content it turns on.** A milestone that opens nothing
is a dead end, and `gates.py` will say so.

⚠️ **Those three answer WHEN content fires. They do not answer WHICH SCREEN IT LIVES ON, and that
is a separate question with its own file — `references/the-surfaces.md`.** Ask *who is this aimed
at*: a person → their hub · the room or herself → its own located canvas · her, done to her → a
substitution. They never share an exit block, and a repeatable location screen caps at 8 choices.
A game that obeyed every other rule here shipped 23 choices on one front desk and scored 18/18,
because nothing said a location page had a shape.

## Dispatch

Resolve the game slug from the request, then read `games/<slug>/v2_state.json`:

| `phase` | do this | reference |
|---|---|---|
| *(no state file)* | write the Want, create the state file | `references/the-want.md` |
| `want` | lay down the world | `references/the-board.md` + `the-map.md` + `the-economy.md` |
| `board` | build v0.1 | `references/the-release.md` (§ first release) + `the-voice.md` |
| `release` | run the loop — pitch, attack, write, gate, ship, log | `references/the-release.md` |

**The world files, all read in the board phase:** `the-board.md` (fill, meters, cast) ·
`the-map.md` (the world as a place someone could draw) · `the-surfaces.md` (which screen each
piece of content lives on) · `the-economy.md` (what money is for) · `the-voice.md` (how the game
talks to the player about itself) · `register.md` (how the prose reads once they click).

The agent roster for each phase is in `references/agents.md`. The state schema is in
`references/state.md`. Engine facts are in `references/engine.md` — and **only** there.

## Operating rules

- **Parse, never grep.** Game state is TOML; read it with a parser. A grep-based pass on one
  game silently missed 24 `is_repeatable` lines and reported the opposite of the truth. The
  same discipline applies to every claim: measure it, don't eyeball it.
- **Every engine claim carries a `file:line`.** If `references/engine.md` doesn't have it,
  go read `apps/game_generation/twee_comprehensive/generators/v2.py` and add it with its
  citation. Never assert engine behaviour from memory.
- **Gates before ship.** `python3 scripts/gates.py <slug>` must be green. A gate that fails
  is either a real defect or a wrong threshold — fix one or the other, never skip.
- **The Want is an input, not an artifact.** Re-read it every release. A release that cannot
  name which line of the Want it serves does not ship. The failure this prevents is a spec
  written once at the start and never consulted again.
- **Never rank the backlog by what is cheap to build.** This is the documented root cause of
  the previous system's output: a pipeline sorted by buildability re-derives the same
  skeleton forever, no matter how much more it studies.
- **The person is the product.** Across ~11,000 player comments, praise for the porn itself
  scored lowest of every theme; what players praise is content volume, who the performer is,
  and attachment to a character. Swapping a performer has killed games.
- **Where a property cannot be inferred from the TOML, the BOARD DECLARES IT and the gate checks
  the game against its own declaration.** This held in all four doctrine studies and is now the
  standard shape — where each character sleeps, which tiers owe guidance cards, what the currency
  is. Do not build a gate that guesses intent; build a field that states it. A gate with no
  declaration to check against reports **n/a**, never a pass: an absence is not a pass.
- **Two voices, and they are different jobs.** `references/register.md` governs what the player
  reads **after** a click. `references/the-voice.md` governs everything else — room names, button
  labels, guidance cards, the words under a meter. A label is UI and must say what clicking does;
  the register lives in the paragraph the click produces. Writing both in the same voice is how a
  game ends up with a most-clicked button nobody can parse.
- **When a gate you just wrote fails a game, check the skill before blaming the game.** A gate
  built for locked doors fired on seven of eight and every one was following `engine.md` §15
  correctly. A check that fails a game for obeying the doctrine is a bug in the check.
- **An explicit beat stays on the body for its whole length** — `references/register.md`. If the
  beat's last sentence is about what it *means* rather than what is *happening*, it has pivoted
  and will fail the floor. This defect recurred three times in three increments, authored each
  time by someone who had just written the doctrine against it. Assume you are doing it.

## Build

```
python3 scripts/merge_toml_phases.py games/<slug>
python3 manage.py package_from_toml \
    --file games/<slug>/toml_phases/7_final_game.toml \
    --output games/<slug>/output --gen-version v2
```

`--file` and `--output` are named and required; the positional/`--output-dir` form this file
used to carry exits 2 and builds nothing.

Never hand-edit `7_final_game.toml` — it is generated by the merge.

## Status

Experimental. The incumbent `author-game` skill keeps every ordinary request until this one
is promoted. Promotion criteria: a game v2 built clears the four commitments on measurement.
The ledger of what changed and why is `CHANGELOG.md`, next to this file — every edit to any
file in this skill gets a dated bullet there in the same turn.
