# 001 · No gate asks whether a canvas is reachable

**Found:** 2026-08-30, in `games/commuter` at v0.1
**Status:** OPEN
**Layer:** skill / scoreboard (`.claude/skills/author-game-v2/scripts/gates.py`)

## What happened

Six of `commuter`'s seven explicit act loops — `loop_ray`, `loop_cole`, `loop_gail`, `loop_doyle`,
`loop_trevor`, `loop_vic` — were fully written, at their declared per-character ceilings, and were
**not in the built game at all**. No `[canvases.trigger]`, so no location; and no choice anywhere
in the game targeted them.

The scoreboard was green over all of it. It read:

```
[PASS]  explicit floor              27.3% of 88 beats carry 3+ explicit words (floor 7.5%)
[PASS]  explicit in repeatable      95.8% of 24 explicit beats are re-enterable (floor 50.0%)
[PASS]  an explicit beat carries a clip   24/24 (100%)
```

Every one of those numbers counted prose the player could never reach.

## Why the engine drops them

The generator builds its canvas set in two moves:

1. **Seed** — canvases carrying `trigger.location_id`
   (`apps/game_generation/twee_comprehensive/generators/v2.py:420-423`).
2. **Closure** — pull in anything a seeded canvas points at with a choice whose
   `targetType == "node"`, plus Lane-3 substitution targets
   (`v2.py:642-682`, the graph path a plain `package_from_toml` takes; the ORM twin at `:563-640`
   does the same thing).

A canvas in neither set never becomes a passage. `loop_three` survived only because
`act_back_bedroom` happened to carry a choice pointing at `loop_three.entry`.

## What it cost

The game's entire per-character sexual spine, silently, through 46 gates, a validator and a build.
`location fill` read **5,809** words; the moment the loops were wired it read **8,414** without a
word being written. The scoreboard had been measuring a game that did not contain its own sex.

## It is the SECOND consecutive game with unreachable act loops

`the_route`, listed the day before, carries this in its own portal entry
(`games-data.js`, the `the_route` block):

> ⚠️ FOUR DEFECTS THE 46 SOURCE GATES COULD NOT SEE, all found by the build and the live run:
> `targetType = "canvas"` is not a valid choice target (importer takes trigger|location|node —
> **both act loops were unreachable**) …

Different cause — a mistyped `targetType` there, a missing link here — **same symptom, same blind
spot, two games running.** That moves this from a one-off to a bug class, and it is the class that
costs the most: the act loops are where the explicit content lives, so the failure mode is always
"the game shipped without its porn in it" and always scores green.

## Why the existing gates cannot see it

Every gate in `gates.py` parses `7_final_game.toml`. Reachability is not a property of the source —
it is a property of what the generator decides to emit. The one mode that reads an artefact,
`gates.py --release`, checks the build for dev flags and missing media, not for canvas presence.

## Proposed fix

Add a check that reads the **built HTML**, not the TOML — so it belongs with `--release`, or in a
new `--build` mode, and it must exit non-zero:

> every canvas declared in `7_final_game.toml` has at least one `Canvas_<id>_Node_` passage in
> `output/index.html`

That is a `grep -c` per canvas and it would have caught this in one second. A source-side
approximation is possible (walk the seed-plus-closure in Python) but it re-implements engine logic
the engine already ran — read the artefact instead.

**Second, smaller fix — a doctrine gap and a stale citation in `references/engine.md` §8:**

§8 already teaches the right pattern — *"a triggerless canvas is a SAFE node-link target … it is how
every sub-menu and every sex loop in this codebase is reached"* (`engine.md:184-190`). What it never
says is the consequence of writing one and **not** linking it: the canvas is not merely unreachable,
it is **pruned out of the build entirely**, so it costs nothing at compile time and shows up in no
error. Add one line to §8:

> ⚠️ A triggerless canvas that nothing links to is DELETED from the build, silently. The seed set is
> canvases with `trigger.location_id` (`v2.py:420-423`); everything else has to be pulled in by a
> `targetType = "node"` choice or a substitution target (`v2.py:642-682`). Write the link in the same
> edit as the canvas.

§8 also cites `v2.py:3177` for `setup.getCanvasById`. The function is at **`v2.py:3317-3331`** — the
citation has drifted 140 lines. Worth a sweep of §8's neighbours while the file is open.

## The tired-author test

A check that only asks "is this canvas well-formed" manufactures well-formed orphans. A check that
asks "is it in the build" cannot be satisfied except by wiring it in. Passes.
