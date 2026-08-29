# The roster — one skill, many agents

The split is not by task. It is by **what has to be remembered**.

> Test: can you write this job's complete input on one page?
> **Yes** → an agent. **No** → the Owner keeps it.

The evidence for this shape is our own history. Fifteen-plus agent runs are recorded in a
previous game's ledger, some as large as 25 and 27 agents. **Every one was read-only** — audit,
verify, diagnose, grade — and they repeatedly caught real defects, including a chunk-fatal
blocker found before a line of code existed. There was exactly one attempt to fan out
*authoring*; that build had the doctrine and still went naive, invented a framing the doctrine
had explicitly abolished, and was deleted in full.

**Agents look. The Owner decides.** The two exceptions below are deliberate and narrow.

---

## The Owner — the main loop

Holds the world. Owns the Want, the Board, the wiring, the gates, and **every write to disk**.

Anything where *why* matters more than *what* stays here: which arc feeds which economy, what
a release must leave behind, what a milestone opens. These cannot be paged into a fresh
context, which is exactly why they cannot be delegated.

---

## Pitchers — 3, parallel, deliberately uncorrelated

**Job:** three takes on the next release subject.

Run them with **no shared context**. This is the one place where not sharing is the feature —
common context yields three shades of one idea, and the point is genuinely different options.

Each returns: the subject, which line of the Want it serves, which existing places and people
it touches, what it opens, and roughly what it costs.

LO picks one. The Owner develops it.

> This is the capability the incumbent system most visibly lacks. It is a correctness
> pipeline — engine tables, traps, gates — which is a different muscle from "here are three
> ideas worth building."

---

## The Attack Panel — before the build, never after

**Job:** try to break the *design*, while changing it is still cheap.

Lenses, each drawn from a run that caught something real:

`soft-lock` · `grind` · `gate-parity` · `numbers` · `timing` · `prose-vs-mechanic` · `canon` ·
`flag chains` · `clamp/bounds` · `render buckets`

**Every finding gets an adversarial verify.** Measured survival rates from our own runs: one
audit returned 4 confirmed against 6 refuted; another 17 survived against 2 refuted. Roughly
half of raw findings are noise, and the verify pass is what makes the rest usable. A previous
review recorded "no false-gap spam" as a quality marker — that is the bar.

Give each verifier a **distinct lens** rather than running N identical skeptics. Diversity
catches failure modes that redundancy cannot.

---

## The Prose Maker — narrow on purpose

**Job:** one beat, from a spec it cannot argue with, hitting one measurable target.

This exists because of a specific, documented pattern: the register rule was the most
carefully written rule in the previous system and was broken in **every** game it shipped.
That is not a knowledge failure — the rule was right there. It is an **attention** failure.
When one agent is simultaneously holding flags, placement, media, tiers and save-safety,
prose is what slips.

Its spec: the beat, the character, the tier, the explicit ceiling from the Want, and the
target. Its output: the prose. It does not choose placement, gates, or media.

---

## The Player — measures heat, does not judge it

> ✅ **BUILT 2026-08-29 — and it was mostly already written.** The harness is
> `scripts/playtest.py`; the agent is `.claude/agents/v2-player.md`, callable as
> `subagent_type: "v2-player"`. This section described a job still to be designed while
> **seven hand-written play-tests** were already running in `games/` — five in `mrs_vance`,
> one each in `steam` and `forty_miles`, 1,000+ lines — sharing a `check()` collector and
> four helpers almost verbatim, and cited exactly once in this whole library
> (`the-meters.md:445`). They found what no source gate could: an effect op the runtime does
> not implement, an obligation that was checked as payable and never as taken, a character
> deleted at midnight by a day-specific overnight row.
>
> ⚠️ **The case for making it shared code is measured, not aesthetic.** Run on 2026-08-29,
> `steam`'s script reported two failures and **both were the harness** — it called
> `applyTraitEffect` with one options object where the engine takes seven positional
> arguments, and asked `pickQuestsCards` for a scope that returns `[]` by construction.
> Two of two raw reds were noise, in a corpus of scripts written by people who knew the
> engine. Every signature the harness wraps is one nobody re-derives.

**Job:** play the build and report numbers.

- clicks and words to the first explicit beat
- whether high-traffic locations are erotic on entry
- whether repeatable loops clear the explicit floor
- where it soft-locks, where it drags

**It measures. LO judges.** This distinction is load-bearing: in a thirty-game study, the
three games that were actually *played* produced every single heat finding in the corpus, and
the twenty-seven that were only parsed produced none. A green build has never once detected
appeal.

### How it must assert — non-negotiable

**Assert on `SugarCube.State.variables`. Never on rendered page text.**

Text assertions have a measured record here: **four false alarms and zero real findings.** The
rendered label is not the string that was authored — icons, spacing, cost suffixes and state
decoration are added at render — so a selector matching author-side text fails on a working build
and the Player reports a defect that does not exist.

The same applies to finding things to click: locate by passage and canvas id, not by visible label.

**Before it can assert at all it needs `engine.md` §24** — four facts about reading a built game,
each of which otherwise produces a false alarm indistinguishable from a real defect. Two of the four
have already cost this project a session apiece.

⚠️ **The ban is on LABELS, and the line matters** — stated absolutely above, and one shipped script
sits the other side of it. `playtest_standing.py` asserts on **body prose** to decide which ladder
rung rendered, and it proved six rebuilt ladders live (`mrs_vance/REVIEW.md:721`). The distinction
the record actually supports: a *label* is decorated at render — icons, spacing, cost suffixes — so
matching author-side text against it fails on a working build; a *beat's prose* is not. So: prose may
answer **which variant rendered**; only state may answer **whether the mechanic fired**. The harness
enforces exactly that split — it ships `sv()` and `body()` and deliberately no `assert_text`.

**Every red is a hypothesis until its cause is found in `v2.py` or the game's TOML, quoted as
`file:line`.** This is the Player's version of the Attack Panel's verify pass, and it is not
optional: of the four raw reds this harness has produced across nine games, **three were the
harness** and one was real.

---

## What is NOT an agent

**Media finding.** That belongs to the `find-media` skills. This skill declares slots —
`pool_dir`, `pool`, the tier suffix, the search vocabulary — and stops there.

**Anything that writes game TOML.** One attempt, one deleted build.

---

## Calling them

Use the Agent tool with a schema when you want structured output; run independent work in a
single message so it goes in parallel. Keep each prompt to one page — if it will not fit, the
job belongs to the Owner.

Load only the references an agent actually needs. The library is addressable on purpose: a
Prose Maker needs the Want's register section and nothing else; the Attack Panel needs the
Board and the gates.
