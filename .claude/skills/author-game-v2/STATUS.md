# author-game-v2 — the complete picture, and where we stand

*Status document. Originally written 2026-08-11 as a plan file; moved into the skill and
refreshed against a live run the same day.*

> **Every number below was verified by running the scoreboard, not from memory.** When this
> document and the scoreboard disagree, the scoreboard is right. Re-verify with:
>
> ```bash
> python3 .claude/skills/author-game-v2/scripts/gates.py back_home
> python3 .claude/skills/author-game-v2/scripts/gates.py vesper
> ```
>
> **Last verified: 2026-08-11.**

---

# PART 1 — WHY v2 EXISTS

## The problem

We had a working authoring skill (`author-game`) built from thorough research into top-ranked
adult sandbox games. It produced games that were structurally correct and did not land. Two
specific complaints drove this work:

1. **It pitches games with endings**, while top games never end and are continuously updated.
2. **Vesper reads as dark noir rather than an adult game**, despite explicit content.

## What the research found

A clean-sheet study (13 agents, forbidden from reading the old skill) plus first-hand
measurement of Degrees of Lewdity's source produced four findings that overturned prior belief.

**"Start narrow" is wrong.** DoL's earliest retrievable build already had **25 locations** — the
same width as Vesper's 26. It started wide. What differed was fill.

**Density falls as a game matures; the beat ratio does not.** DoL's sex-word share dropped
3.00% → 1.16% over eight years as systems and UI outgrew prose. But the share of scene units
carrying 3+ explicit words held at **7.5–9.3%** across eight years and twelve-fold growth. That
stability makes it the only usable heat measure.

**Vesper's defect was located precisely.** Sexual prose exists in **17 of 25** DoL locations
versus **1 of 21** Vesper locations — and that one is a sealed cell with no exits. **18 of
Vesper's 19 explicitly-worded prose blocks sit in a room the player can never re-enter**, while
all nine of its repeatable sex loops score zero. The premise was never the problem; the crude
register was quarantined in one-time content.

**A release is not a chapter.** One measured six-week DoL cycle: **+196 units, +24,388 words,
zero new locations**, and every one of its ten content commits was an event at an existing place
with an existing character. 55.6% of its commits were fixes.

## The commitments that follow

1. **The product never ends.** Endings *inside* the game are normal (DoL ships seven terminal
   fail-states); the game itself does not close. Subscription revenue is an integral over months.
2. **Fill before you widen** — as a *distribution*: one anchor holding ≥25%, median ≥3,000,
   mean ≥4,500.
3. **Heat lives where the player returns.** The explicit floor, and the majority of it in
   re-enterable content.
4. **A release adds events, not places.**

---

# PART 2 — THE ARCHITECTURE

## One skill, many agents

Settled after examining fifteen prior agent runs in Vesper's ledger. **Every one was read-only**
— audit, verify, diagnose — and they repeatedly caught real defects. The single time authoring
was fanned out, that build was deleted: it had the doctrine and still went naive.

> **Agents look. The owner decides.**

Two rules govern the seam:

- **Split by what must be REMEMBERED, not by what must be DONE.** If a task's complete input fits
  on one page → agent. If not → the owner keeps it.
- **Skills are memory. Agents are attention.** One doctrine library, many attention units.

## The pipeline

| phase | what happens |
|---|---|
| `want` | one page: who she is, the appetite that never fills, the ascent as *access*, the charge, why each person is wanted, the register |
| `board` | the world — locations with fill budgets, characters with surfaces and schedules, three ratcheting tiers |
| `first_release` | v0.1 builds the board; every gate green on the day it ships |
| `release` | forever: pick subject → pitch → attack → write → gate → ship → log |

## Three kinds of content

Named from what DoL's release commits actually do:

- **STANDING** — she can go there and act, repeatedly. Carries the explicit floor and the crude
  register.
- **TRIGGERED** — fires when her state matches (*"when exposed"*, *"at high stress"*). For a
  female protagonist this is the main heat engine at low tiers.
- **MILESTONE** — fires once, then opens standing content. Every one names what it turns on.

## The meters — three layers, measured

Corrected mid-build when DoL's source refuted our first draft. It does **not** run one axis:

| layer | evidence |
|---|---|
| **ratcheting tiers** (3–4) | promiscuity 22 raises / 1 lower, 206 gate sites · deviancy 20/0 · exhibitionism 12/1 · rungs at **15/35/55/75** |
| **volatile state** | arousal — 277 sets, moves both ways constantly |
| **per-character** | love + lust + disposition, light |

Several tiers rather than one, because each names a *different* kind of going-further, so a
player who does not want one can climb another.

---

# PART 3 — WHAT IS BUILT

```
.claude/skills/author-game-v2/
  SKILL.md                    111   entry point, EXPLICIT-INVOKE ONLY
  scripts/gates.py            605   the scoreboard — 10 gates + 1 non-scoring lint
  references/engine.md        501   21 verified engine facts, each with file:line
  references/the-board.md     285   the world, its fill rules, and the rotating slot
  references/the-release.md   138   the unit of work
  references/state.md         116   v2_state.json schema
  references/agents.md        114   the roster (described, NOT built)
  references/register.md      111   how to write an explicit beat, and how to sweep
  references/the-want.md      102   the spec re-read every release
  templates/board.toml        163   fillable, parses
  templates/want.md            90   fillable
  CHANGELOG.md              1,492   the full trail
  STATUS.md                     —   this file
```

## The ten gates

Every threshold traces to a measurement, inline in the script.

| gate | threshold | source |
|---|---|---|
| location fill | anchor ≥25%, median ≥3,000, mean ≥4,500 | DoL seed: 30.2% / 3,154 / 4,661 |
| explicit floor | ≥7.5% of beats carry 3+ explicit words | DoL held 7.5–9.3% over 8 years |
| explicit in repeatable | >50% | Vesper's failure: 95% sealed away |
| repeatable explicit media | pools, never single files | DoL re-rolls 26- and 56-item pools |
| traversal heat | ≥60% of locations carry a cycling pool | DoL seed: 17 of 25 (68%) |
| standing surface | every character findable and scheduled | Vesper: `npc_bastien`, 88 refs, nowhere |
| milestones open something | transitive, random ambients excluded | — |
| meter ceiling | every band boundary must buy content | — |
| ends on an opening | ≥1 `show_when_locked` | wants sell updates, questions don't |
| ascent tiers expand | declared tiers must gate upward | Vesper's meter contracted the world |

Three gates were **corrected during the build** when they proved wrong against their own
evidence — the location floor (DoL failed it 24/25), the meter ceiling (twice), and vacuous
passes on empty games. A gate that cannot be re-derived from the measurements does not belong.

**Plus one lint, deliberately non-scoring.** Dialogue attributed to a character the canvas
neither binds nor names in its id. It returns **3 on `back_home`** (two are the known-good
opening; one is `shift_change_frontroom`, which renders correctly but is misnamed by house
convention) and **28 on `vesper`**, clustered on the same `npc_bastien` the standing-surface
gate already fails it for. A warning that can move a gate is a gate, so it never scores.

---

# PART 4 — WHAT USING IT PROVED

## The pipeline runs end to end

Want → Board → TOML → merge → validate → package → **a playable HTML game**, driven headlessly
through the age gate, an opening chain, schedule-gated hubs and applied trait effects.

## Twenty engine facts, six of which break builds silently

The most valuable single artefact. Highlights:

- **An invented TOML key is silently ignored.** `clothingEffects` parsed, validated, built green
  and granted nothing. The real key is `wardrobeEffects`. Nothing in the pipeline catches this —
  the only defence is grepping the importer.
- **`is_repeatable` defaults to TRUE** when absent (`v2.py:10937`, `:11010`).
- **Three key asymmetries:** conditions say `trait_key`/`npc_id`, effects say `trait`/`npcId`.
- **A flag read by a trigger *or a choice* must be set from a LOCATED canvas**, or the build
  hard-fails. Hit twice — and the fix is to **move** the setter, never to duplicate it.
- **Exit blocks need section syntax**; multi-line inline tables are a parse error.
- **`worn_corruption` is a MAX aggregate, not a sum** — one loaded garment sets the tier.
- **One repeatable canvas per location + NPC + time window** (§19). A second one is a *warning*,
  not an error: it looks correct in TOML and is unreachable in play. Treat the warning as an error.
- **`npc_at_location` takes an optional `npc_id`** (§20) — omit it and the predicate tests whether
  the room is occupied by anybody. Verified live, not read.

## A doctrine file that measurably changed authoring

Four times, new explicit content scored near-zero and had to be rewritten after the gate caught
it. Investigating why revealed the skill said *where* the crude register lives and *which words*
were allowed — and **nothing about how to write the beat**.

`references/register.md` states the rule and the diagnostic:

> An explicit beat stays on the body for its whole length. If its last sentence is about what the
> moment *means* rather than what is *happening*, it has pivoted and will fail.

**Every increment written against it raised the floor rather than diluting it** — 9.4% → 10.0%
→ 10.1% → 10.8%, then **15.9%** when the rule was finally applied *backwards* to the three
repeatable sex loops that had shipped before it existed. All three opened explicit and scored
zero on their tails; the fix added no gratuitous nouns, it just kept the camera on the body to
the last sentence. First evidence in this project that a written rule changes output.

**Two words that are NOT on the frozen list:** `wet`, and `come` — the latter excluded on purpose
because it matches "come downstairs". Beats that lean on both can read filthy and still score 2.

## Bugs only live play could find

- A **soft-lock**: the opening landed at 17:18, sleep was gated 21:00+, and navigation does not
  advance the clock — every scheduled window in the game was unreachable, forever.
- A **cold start**: two characters used the bathroom on weekdays only while the game began on a
  Friday, leaving the core mechanic dead for three in-game days.
- A **mis-attributed dialogue** block that would have rendered the wrong character's name.
- **The documented build command was wrong** in two files and had shipped that way since the
  first release. A skill that cannot build the game it authored is a broken skill.

For whoever writes the next harness: `State`/`Engine` are not bare globals (use
`SugarCube.State`, `SugarCube.Engine`, `SugarCube.setup`); `$flags` is an **object**, not an
array; player traits live at `player.core_traits`.

## And a property of ratio gates

The anchor requirement **tightens as you work elsewhere**. Held at a fixed size while six other
rooms were written, the anchor's share fell **53% → 34%** without a word being removed. Phase 1
then took the front room 5,123 → 9,607 words, budgeting it against the *finished* 36,000-word
total rather than the current one — and the share went to **51%**, with room to survive the
remaining fill. Budget the anchor against the finished total, or you write it twice.

---

# PART 5 — WHERE THE TEST GAME STANDS

> **2026-08-11 — `back_home` v0.1 is GREEN. 10 of 10 gates, exit code 0.** The section below this
> banner is the record of how it got there and is left standing; the numbers in it are superseded by
> the table immediately following.

`games/back_home` — **97 canvases, 8 locations, 4 characters, 36,035 words** of location prose,
12,515 lines of TOML. `phase` is now **`release`**.

| gate | |
|---|---|
| location fill | **PASS** mean 4,504 · median 4,381 · anchor `the_front_room` 27% |
| explicit floor | **PASS** 27.8% of 270 beats |
| explicit in repeatable | **PASS** 100% of 75 |
| repeatable explicit media | **PASS** 49 pooled, 0 fixed |
| traversal heat | **PASS** 7/8 (88%) — `the_shop` cold by design |
| standing surface | **PASS** 4/4 |
| milestones open something | **PASS** 4/4 |
| meter ceiling | **PASS** |
| ends on an opening | **PASS** 8 locked rungs |
| ascent tiers expand | **PASS** all three |

Vesper, the control, still scores **1/10** on the same instrument.

**Six fill increments, +17,153 words, and three of them changed the skill rather than the game:**
the `clamp` bug that made the rent unpayable (`engine.md` §21), *a category name is not a sweep*
(`register.md`), and *the rotating slot must be split by content lifetime* (`the-board.md`).

**Still open:** the explicit-floor denominator question (28% against a band whose denominator may
not match ours), media (47 declared `pool_dir` slots, zero files), and the agents.

---

## The historical record — how it looked mid-run

`games/back_home` — 66 canvases, 8 locations, 4 characters, 14 schedule rows, 9 wardrobe items,
**18,882 words** of location prose, 8,207 lines of TOML across the phase files.

**9 of 10 gates pass.**

| | |
|---|---|
| explicit floor | **PASS** 15.9% of 176 beats |
| explicit in repeatable | **PASS** 100% of 28 |
| repeatable explicit media | **PASS** 28 pooled, 0 fixed |
| traversal heat | **PASS** 7/8 (88%) — `the_shop` is the cold one, by design |
| standing surface | **PASS** 4/4 |
| milestones open something | **PASS** 4/4 |
| meter ceiling | **PASS** |
| ends on an opening | **PASS** 4 locked rungs |
| ascent tiers expand | **PASS** all three gated |
| **location fill** | **FAIL** — mean 2,360 (need 4,500), median 1,496 (need 3,000) |

Vesper, as the control, scores **1/10** on the same instrument: 27 locations, 42,684 words, mean
1,581, median 674, anchor 26%, explicit floor 4.7% of 578 beats, and only 14.8% of its explicit
beats re-enterable.

**Status: in progress.** The one failing gate is location fill, and it is a fill problem rather
than a design problem. No location needs inventing and no character needs adding — the eight
rooms and four characters that exist need more written inside them.

**The anchor is no longer the constraint.** `the_front_room` sits at **51%** after Phase 1, well
clear of the 25% floor and budgeted to survive the rest of the fill. The work is now the seven
satellites, thinnest first:

| location | words | job |
|---|---|---|
| `the_shop` | 654 | money that is hers, and the world that does not know |
| `the_garage` | 801 | the private male space |
| `the_box_room` | 1,228 | the renewable slot — a stranger the other side of her wall |
| `the_landing` | 1,367 | the vantage; a corridor, legitimately thin |
| `her_room` | 1,496 | her base, half storage, the door catch broken |
| `the_kitchen` | 1,775 | the crossing point |
| `the_bathroom` | 1,954 | the occupancy engine — one bathroom, four adults |

Roughly **17,000 more words** closes gate 1 and makes this v2's first green game.

---

# PART 6 — WHAT IS NOT DONE

| | |
|---|---|
| **The agents** | Pitchers, attack panel, prose maker, player — all still prose in `agents.md`. No prompts, no schemas, no call sites. `scripts/` contains only `gates.py`. **Now the biggest hole by a distance.** |
| **Evals** | None. "v2 beats v1" cannot be scored. |
| **A cold reader** | Only one person has ever run the skill. |
| **Media** | 47 declared `pool_dir` slots on `back_home`, **zero files on disk.** Gate 4 judges declarations, so the game is green without them; it is not *playable-shippable* until they are stocked. Deferred by LO until after he plays it. |
| **The floor's upper comparison** | The game reads 28% against a reference band of 7.5–9.3%. `gates.py` measures **location prose only**; the reference figure cites whole-source unit counts. If those denominators differ, the two are not comparable at the top end — and no snapshot is on disk to check. Either re-derive it location-only or say plainly in `gates.py` that the floor is a floor. |
| **Four engine facts** | Still on the do-not-cite list in `engine.md`. |

*(Shipped off this list: the dialogue-attribution lint — `gates.py:605`; the
`shift_change_frontroom` rename; **and a green game.**)*

## Promotion criteria — **MET, 2026-08-11**

v2 replaces v1 when a game it built clears: location fill by the distribution rule, ≥7.5% of beats
at 3+ explicit words, majority of explicit content repeatable, and a release that adds zero
locations and still feels like a release.

| criterion | `back_home` v0.1 |
|---|---|
| location fill (distribution) | **mean 4,504 · median 4,381 · anchor 27%** ✅ |
| ≥7.5% beats at 3+ explicit | **27.8% of 270** ✅ |
| majority of explicit repeatable | **100% of 75** ✅ |
| a release that adds zero locations | ⏳ **not yet demonstrated** — v0.1 *built* the Board; the
first true release is the next increment, and it is the one criterion still outstanding |

**So: three of four, and the fourth is by definition unprovable until a release ships.** The
description stays **EXPLICIT-INVOKE ONLY** until that release lands and still feels like one.

---

# PART 7 — WHAT IS NEXT

v0.1 is green and `phase` is `release`. The paths have changed shape:

**A. LO plays it.** His call and the gate before everything else. Nothing in `gates.py` measures
whether the thing is any good to play, and one person clicking through it for an hour will find
more than the scoreboard can.

**B. Build the agents.** Now unambiguously the largest architectural gap. Pitchers first — three
independent takes with no shared context, which is the capability v1 most visibly lacks. Note for
the Player agent's spec, learned expensively across six increments: **forbid page-text assertions
outright**, bake in that the clock is `game_state.time_state`, that a repeatable canvas renders as
a clickable action rather than an auto-fire, and that there are *two* per-day ledgers.

**C. Ship release 0.2 — zero new locations.** The fourth promotion criterion, and the one thing
v0.1 by its nature could not demonstrate. There are five unpaid content plants in the ledger and
eight locked doors, so the backlog exists; per the operating rules, do **not** rank it by what is
cheap to build.

**D. Run the corrected gates against Vesper.** It shipped, it scores 1/10, and the scoreboard has
never been used to plan repairs on it.

**Recommendation: A, then B, then C.** The playthrough is cheap and changes what B and C should
contain; the agents are the capability everything after this depends on; 0.2 is what actually
closes promotion.
