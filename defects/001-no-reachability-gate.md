# 001 · No gate asks whether a canvas is reachable

**Found:** 2026-08-30, in `games/commuter` at v0.1
**Status:** FIXED 2026-08-30
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

⚠️ **The three citations below were WRONG when this file was written and are corrected here**
(2026-08-30, re-read against source). The mechanism was right; the line numbers and the naming of
the two implementations were not. The original said `420-423` / `642-682` "the graph path a plain
`package_from_toml` takes" / `563-640` "the ORM twin" — which calls the copy the original and the
original the copy, and misses a second seed site entirely.

The generator builds its canvas set in two moves:

1. **Seed** — canvases carrying `trigger.location_id`. **Two sites, not one:**
   `apps/game_generation/twee_comprehensive/generators/v2.py:420-424` (the no-DB graph path) and
   `:447-451` (the ORM path).
2. **Closure** — pull in anything a seeded canvas points at with a choice whose
   `targetType == "node"` (`:615` ORM, `:676` graph), plus Lane-3 substitution targets
   (`:596`, `:663`). The **primary** implementation and sole entry point is
   `_compute_included_canvases` (`v2.py:564-640`); it delegates at `:566-568` to its own no-DB
   twin `_compute_included_canvases_graph` (`:642-691`), whose docstring at `:643-644` says so
   outright.

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

---

## Fixed — 2026-08-30

**1 · `gates.py --release` gained a seventh check, `every canvas is a passage.`** Every canvas id in
`7_final_game.toml` must appear as a `<tw-passagedata>` declaration in `output/index.html`. It reads
the artefact, because reachability is not a property of the source.

Three things the proposed `grep -c` above would have got wrong, each caught by running the check
against every build in the repo before shipping it:

- **A bare substring match returns a false PASS on a dangling link.** A canvas that is *linked to*
  but never *emitted* still has its name in the HTML, inside the link text of the passages pointing
  at it — on `loop_ray`, 17 of 23 raw matches are link references and only 6 are declarations. The
  matcher anchors on `<tw-passagedata … name="`.
- **The opening canvas emits as `StartingCanvas_<id>_Node_…`.** Without that prefix the check
  false-fails *every game in the repo*.
- **Node ids are not portable across generator eras** — `mothers_place` emits `_Node_1`, current
  games `_Node_base` — so the check is canvas-level, never node-level.

**Two exemptions were tested and deliberately NOT added**, per `gates.py:2785-2809` on how R4,
study 6 and P0 were withdrawn for exactly this:

- dev-gated canvases need none — `vesper` carries 11 in a **non-dev** build and
  `the_long_summer_test` 9, both at zero missing;
- file mtime discriminates nothing — 11 of 13 games have a TOML newer than their build, including
  every game at zero missing, because `merge_toml_phases` rewrites `7_final_game.toml` routinely.

**The discriminator is the canvas's own trigger**, and the message names which of the two causes it
is, or the author hunts for a link that was never the problem: a canvas carrying `trigger.location`
is in the seed set by construction and can only be absent because *the build predates it* →
**rebuild**; one with no location was never pulled into the closure → **write the link**.

**Measured before shipping:** 1,895 canvases across 23 builds, one red — `mrs_vance`, missing
`ask_papers` and `see_truck`, both carrying a location, correctly reported as a stale build. That
red is deliberate (LO's call, 2026-08-30); rebuilding that game is separate work. Sensitivity proved
by synthetic injection in an isolated tree: a triggerless unlinked canvas → FAIL, correct cause,
exit 1.

**2 · `engine.md` §8 now states the consequence**, which was net-new — a full-file search of all
2,319 lines confirmed nothing said a triggerless unlinked canvas is pruned. The stale `v2.py:3177`
in the same section was re-anchored to **`v2.py:3317-3331`**.

**3 · `SKILL.md:289`** updated from six release checks to seven.
