# Doctrine gaps — what v2 never learned about building a good game in this engine

v2 was derived one way: by measuring ten snapshots of one reference game's source. That method
produced four commitments that are correct and that refuted the incumbent skill on **shape**. It
also has a hard structural limit:

> ⚠️ **SUPERSEDED IN PART, 2026-08-18.** Study 5's *"every choice hangs off a named object in the
> prose"* — the finding that became `the-surfaces.md` R2b and gate 22 — **was read backwards.** The
> worked example it rests on (DoL's bedroom) is not choices hanging off objects; its standing links
> are `Strip and get in bed` (the sleep machine), `Masturbate in bed` (the solo feeder), `Wardrobe`
> (the clothing system), `Mirror` (the body system). **Each "object" is the door to a system that
> spans the whole game.** Measured afterwards across 25 shipped sandboxes: `sleep` 773 uses in 19
> games, `eat` 430 in 17, `wash` 224 in 16 — while *"look around / examine"* appears 232 times and
> is one-off quest objects everywhere, never a per-room browse menu. Gate 22 and its lint are
> deleted; the rule is now **needs + work + people** (`the-surfaces.md` R2). The R2/R2b sections
> below are kept as the record of what was believed and why.

> **A doctrine derived from measuring one game cannot contain anything that game lacks** — even
> when our engine ships the feature, and even when our own previous skill taught it.

Quests fell through that hole first. `templates/board.toml:26` ships `quests_engine = "v2"`, which
lights up a sidebar entry and a "What's Next" page, and across all 1,367 lines of v2 doctrine there
is **zero** instruction on authoring a quest and **zero** quest check in `gates.py`. A game built
exactly to spec ships an empty guidance page. `games/back_home` did.

This file closes the rest of the hole. It is the inventory of what v2 must teach, plus one study
per item.

---

## The method — and the constraint that shapes it

The incumbent `author-game` skill carries 38 reference files and 9,672 lines, most of it craft
knowledge this engine paid for the hard way. v2 has 7 files and 1,367 lines — **14%**.

**v2 does not link to, reference, or import any v1 file. It never will.** That is not tidiness,
it is a structural requirement:

- v1's references are welded to v1's pipeline. `step-5-blueprint.md` says "Step N" 24 times,
  `step-3-casting.md` 16, `content-framework.md` 15. v1 is a chapter-shaped process — design the
  story, then build it. v2 is `want` → `board` → `release`, a stream with no end. Importing a v1
  file imports v1's shape into the one skill whose thesis is that the shape was wrong.
- v1 is actively maintained and changing. A live dependency drifting under v2 is invisible to v2.
- Precedent: v2 was already divorced from the `prompts_v2` corpus, which taught false engine facts.
  Depending on a corpus you do not own reproduces that failure.

So each item is **studied, not copied**. v1 is evidence about the problem, not the answer.

**And v1 is not the good version.** Its craft files coexisted with a game scoring **1/10** on this
skill's own instrument — 95% of its explicit prose sealed in a room with no exits, all nine of its
repeatable sex loops scoring zero. The picture is exact complements:

| | craft | shape |
|---|---|---|
| **v1** | strong | wrong |
| **v2** | absent | measured, right |

So "where v1 is wrong" is real work in every study, not a courtesy paragraph.

### Every study ends in a check, not a paragraph

This is what makes the output v2's doctrine rather than v1's advice reworded.

Prose gets skipped. Measured, on this project: the register pivot defect was authored **three
increments running, each time immediately after re-reading the rule against it.** The paragraph
never once caught it. The per-beat scorer caught it every time.

v1 knows this about itself and says so. `location-design.md:14` — *"The engine never checks any of
this — a wrong, dead, or incoherent map builds GREEN."* And then, in its own audit list at `:257`,
the confession that settles the argument:

> Every locked location's unlock flag has a real setter … *(Shipped twice: v1's Dining Room, then
> again in the rebuild written to prevent it.)*

**A checklist written to prevent a bug, followed by the same bug.** That is the case for gates,
made by the checklist.

So every study's last section asks: *what can `gates.py` decide mechanically?* An honest "nothing,
and here is why" is an acceptable answer. A vague one is not.

---

## The study format

Five sections, identical every time:

1. **What it is, and what breaks without it** — cited to a `games/back_home/REVIEW.md` finding
2. **How v1 teaches it** — a real quote, not a summary
3. **Where v1 is wrong** — dated, pipeline-bound, incomplete, or mistaken
4. **What v2 says instead** — written in v2's phases, owing nothing to v1's structure
5. **The check** — what `gates.py` can decide, or an honest nothing

A finished study graduates into a real v2 reference file. Until then it lives here.

---

## The inventory

### Tier 1 — proven broken in `back_home`, blocks building a new game

| # | item | what it owns | evidence | status |
|---|---|---|---|---|
| **1** | **Map & space** | the graph, floors, exteriors, travel, what a room is for | `REVIEW.md` W1 W3 W4 W6 | ✅ **GRADUATED** → `references/the-map.md` |
| **2** | **How the game talks to the player** | quests, guidance, labels, room names, locked-door text, meter band words | G1 ~~G2~~ W5 W7 | ✅ **GRADUATED** → `references/the-voice.md` |
| **3** | **Money & pressure** | sources, sinks, what forces a choice | E1 | ✅ **GRADUATED** → `references/the-economy.md` |
| **4** | **How the prose is written** | RTS-flat, dialogue, thought, the 90% of prose that is not an explicit beat | — | ✅ **GRADUATED** → `references/register.md` (expanded) |

> **Tier 1 is closed.** The four studies below are the trail, not the doctrine — the doctrine now
> lives in the reference files above and the checks live in `scripts/gates.py`. Read a study when you
> want to know *why* a rule exists or what v1 got wrong; read the reference file to author.
>
> **One study output was withdrawn on contact with the engine.** Study 2's R4 proposed a gate
> requiring every locked door to carry `locked_text`. Built, it fired on 7 of 8 doors in a real game
> — and `references/engine.md` §15 already rules the other way, deliberately: omitting `locked_text`
> shows the greyed *action*, a want the player can name, which is what sells the next release.
> **A check that fails a game for obeying the doctrine is a bug in the check.** No gate shipped, the
> rule was rewritten as "the wall shows the want, the card shows the route", and
> `games/back_home/REVIEW.md` G2 was withdrawn as not-a-defect. Recorded because it is the clearest
> case in this exercise of verifying before asserting, and it was caught only by building the thing.

### Tier 2 — proven weak

| **5** | **Meters & the HUD** | what is displayed vs what is actually read | E2 E3 E4 | ✅ **ADDRESSED 2026-08-19** → `the-meters.md` W1–W6, gates 33/34 |
| **6** | **Onboarding** | the first hour | `off_season/REVIEW_1.md` O1–O4 N1–N2 | ✅ **ADDRESSED 2026-08-22** → `the-first-hour.md` F1–F9, gates `the opening opens a door` · `every hub is met first` · `the anchor introduces itself`, lint `named before met` |
| **7** | **The daily loop** | time costs, energy, what an ordinary day is | `off_season/REVIEW_1.md` T1–T3 | ✅ **TIME HALF ADDRESSED 2026-08-22** → `the-clock.md` C1–C6, gate `the label keeps its time`, lints `the clock in the prose` · `the time cost is not on the button`. Energy and "what an ordinary day is" remain in `the-meters.md` M8–M10 + gate 29 |
| **8** | **Ladder shape** | rung spacing, ceilings, when an arc is finished | | ✅ **ADDRESSED 2026-08-19** → `the-meters.md` W4 + the meter-ladder lint |

> ### ⛔ SUPERSEDED 2026-08-19 — "three layers, three or four ratcheting tiers" was n = 1
>
> `the-board.md` §3 and `STATUS.md` derived v2's meter architecture from **one game's seed source**
> and presented it as the shape. Measured across the same 25-game corpus the prose study used
> (SugarCube passage source, clamp guards excluded — Appendix C trap 5), counting player-owned
> ascent meters with ≥4 real content gates:
>
> ```
> 0 meters   14 games        1 meter   7 games        2 meters   2 games
> 8 meters   family-ties     9 meters  degrees-of-lewdity          median 0
> ```
>
> **Fourteen of 25 shipped sandboxes have no player ascent tier at all**, and only two carry three
> or more — one of which is the reference game itself. The largest unclassified meter in each of the
> 14 zeroes was hand-checked: resources, story counters, levels. No hidden tiers.
>
> Where the field's gating actually lives is **per character** — 285 per-character meters against
> 101 player-owned ones — and it **splits into two schools with nothing between 15% and 65%**:
> 8 roster games at 65%+, 9 ladder games at 13% or less. All five v2 games sit at 19–29%, inside a
> band no shipped game occupies, because v2 dropped v1's "Who climbs?" question
> (`author-game/references/content-framework.md`) and one template answered it five times.
>
> **Not deleted:** three-or-four tiers remains a correct answer for a `who_climbs = "player"` game,
> and the reference game's own figures stand. What is retired is treating it as the default.
> Superseding doctrine: `references/the-meters.md` W1. Checks: gates 33 and 34.

### Tier 3 — untested here, v2 still has nothing

| **9** | Clothing / wardrobe as a system |
| **10** | Sex-loop shape |
| **11** | Pre-ship discipline — **still open, and it must NOT be built as a checklist.** §3a of this file already rules on that: *"checklists do not hold… v2 must not inherit the checkbox"*, with v1's 13-point audit followed by the very bug it was written to prevent. **Half of it closed 2026-08-23**: `the-release.md` loop step 5 now says the nineteen lints get read as well as the gates passing, and step 6 records the figures shipped with in `v2_state.json` — a tracked number rather than a box. Cause: Off Season shipped **37/38 with 67 flagged words**, two of which reached LO on a button. What remains open is everything the lints do not cover, and it arrives as instruments or not at all. |
| **12** | Optional systems — phone, customization |
| **13** | **Prose that copies a field** — a price, a window, a room name written into a beat is a duplicate of the TOML with no link back, and it goes stale the day the field moves. v1 carried a whole file on this (`author-game/references/prose-truth.md`, 121 lines); a grep of the v2 skill for `prose is a copy \| re-price \| stale prose` returns **nothing**. Found 2026-08-22 while closing the currency item, which is the first measured instance of it. |
| **14** | **Who the player is** — gender, blank-slate vs written, and whether the player chooses anything about her at minute zero. **✅ ADDRESSED 2026-08-27 → Study 7, applied.** v1 asked this first of anything (`author-game/references/step-0-1-seed.md:17`); v2 answered it by grammar instead — `templates/want.md` said `she/her` **21 times and `he/him` zero** — and eight games shipped one protagonist nobody chose (LO: *"just happened"*). Now a **declaration**: `want.player` in `state.md`, a §1 in `templates/want.md` and `references/the-want.md` that is answered before she is described, and gate **`the start choice is read`**. ⚠️ **The female default STAYS and is evidenced** (49 corpus comments for a female lead against 11 opposed) — what was broken was that it was never a question. ⚠️ **The gate fails only on ZERO**; the read-count floor was refused at n = 1. Shipped only after `mrs_vance` (`f34dc3b`) built it first — the opposite order to P0, refused the same day. |
| **15** | **What she owns** — whether anything the player buys stays bought and opens doors, whether a repeatable she pays for deposits anything, and whether a door may close. **✅ ADDRESSED 2026-08-28 → Study 8, applied.** ⚠️ **Not a discovery — an ADOPTION.** The 2026-07-24 field report already ranked this as its critique **#3 (no meta-loop of accumulation — *"the deepest structural difference"*), #4 (repetition doesn't pay) and #6 (the world never pushes back)** and none of the three was ever carried into this inventory. Measured: **nine of 25 corpus games sell the player a THING and all four of the most-engaged sandboxes do** (a company gating 114 condition sites, a car 46, five bedrooms 21/20/16/16/16), while **money bought exactly one thing across our eight games** — `mrs_vance`'s truck, and it shipped out of the economy pass with no doctrine behind it. Now `the-economy.md` **R1b** (what money buys has to stay bought) and **R1c** (a repeatable she pays for deposits something), `the-surfaces.md` **R6**'s pool note, a scope on `the-want.md`'s additive-only rule, gate **`what money buys opens a door`** and a deposit-rate lint. ⚠️ **The gate fails only on ZERO** and its first red was found in shipped work: `the_season` sells $20 boots nothing reads. ⚠️ **The expensive form of `freedom` is explicitly out** — the corpus's own contrast case is College Daze, excluded for branch explosion. |
| **16** | **The release boundary** — what separates a test build from a published one, and whether anything holds it. **✅ ADDRESSED 2026-08-28 → `mrs_vance/REVIEW.md` B2, applied.** The rule is LO's and it is right — *dev mode and missing media block RELEASE, not testing* — and it lived **only as a comment on a JS object literal** (`games-data.js:44-49`), restated by hand in **nine of twenty-eight portal entries in three wordings**. `gates.py` had **zero lines that read a built game**; `the-release.md`, 164 lines and named for this, never mentioned `--dev`, `--debug` or a build. ⚠️ **Every gate in this skill measures the SOURCE, and a release is the one moment the ARTEFACT is what is judged** — which is why the drift was already shipped: **`the_inheritance` sits in the published grid carrying a full `--dev --debug` build with 115 missing files**, and `forty_miles` reads portal `0.1` / `[project] 0.1.2` / archives `{0.1, 0.1.1, 0.1.2}`. Now `the-release.md` **§ Shipping the build** (six steps lifted from the JS comment, not invented, plus the rule the schema never stated: **`dev: true` and `version` are mutually exclusive**) and `gates.py --release`. ⚠️ **B2's own proposed instrument was CORRECTED, not adopted** — the `[IMAGE MISSING]` markers it named are `--debug`-only (`v2.py:12403`), so the grep would have passed `under_one_roof` with **183 missing files**; the check reads the flags-init map and `MissingMediaPage` instead. ⚠️ **Byte-equality against the archive is printed and never judged** — vesper's differ, and vesper is the one game whose triangle is whole. **Baseline: 0 of 29 builds clean.** |

### Parked

**Save safety.** Handled as its own piece of work, not as a study here. Noting why it matters more
for v2 than it ever did for v1: v2's founding commitment is that **the product never ends**, so
every release after the first lands on players holding live saves. v1 built games that finished and
could afford to be casual about it. v2 cannot, and v2 is the version that has nothing — the topic
appears exactly once, at `references/engine.md:501`, under the heading **"Unverified — do not cite
until read"**. This has already cost us once: Vesper's 0.1.4 saves were stranded by a one-shot
burn and needed an idempotent re-grant to heal.

### Item 4's boundary, settled

Items 2 and 4 divide all player-facing text between them, and the line is **what job the text is
doing**, not where it sits:

| category | job | rule | owner |
|---|---|---|---|
| **interface text** — room names, activity labels, quest cards, meter band words, locked-door text | tell the player what this is / what clicking does | plain, functional, unambiguous | **item 2** |
| **scene prose** — paragraphs, dialogue, thought bubbles | still be good on the fiftieth read | RTS-flat | **item 4** |
| **in-scene choice lines** — *Stop pretending it's a favour* | a choice inside a conversation, with the scene already on screen | voice; leave them alone | **item 4** |

So naming is **not** an RTS-flat problem. Naming is a button. RTS-flat governs everything the
player reads *after* clicking — and v2 currently has 111 lines on it against v1's 735, of which
v2's cover exactly one topic: how to write an explicit beat, and one recurring defect in doing so.
The other 90% of the prose in a game is undocumented.

---
---

# Study 1 — Map & space

## 1 · What it is, and what breaks without it

The map is the set of places, how they connect, and what each is for. It is the only system in the
game the player touches on **every single turn**, and the engine validates almost none of it.

`back_home` shipped 10/10 on `gates.py` with a map that does not describe a building. Four findings,
all from `games/back_home/REVIEW.md`:

**W1 — there is no outside.** `the_shop` carries `entry_from = "the_front_room"` and sits in the
front room's `navigation_order` between the kitchen and the landing. No street, no front door, no
town. Walking to work is the same action as walking into the kitchen. The location's own description
says *"ten minutes' walk away"*; the graph puts it one step from the sofa.

**W3 — the fiction and the graph disagree.** `rung_ray_garage_bench` is written around the garage
being *"the only room in the house with a door to the outside."* The garage's `navigation_order` is
`[]` and its only exit is back to the kitchen.

**W4 — three of four men have no bedroom.** Ray, Dean and Cal are scheduled only in the bathroom,
front room, garage and kitchen. Two bedrooms exist in a house holding four adults, and the landing's
own description counts *"Four doors"* — one of which opens on nothing. The Want compounds it:
`the_want.md:41` sells **"her father's room"** as one of three rewards for topping out `nerve`. It
was never built.

**W6 — the prose built the world the graph didn't.** Counted across the authored phase files: *the
hall* ×6, *front door* ×2, *the street* ×1, *outside the house* ×1. None are locations.

**The consequences are not cosmetic.** `exposure` is the most gameable meter in the game and its
entire consequence surface is four adults who already live with her. There is no source of new
characters, because a world with no exterior can only recycle its interior — which is also why the
box room is the only renewal mechanism the game has (`REVIEW.md` N3).

## 2 · How v1 teaches it

v1 owns this in two files: `references/location-design.md` (274 lines, the design vocabulary) and
`references/step-2b-map-design.md` (76 lines, the generative step that runs it). Between them they
carry the best map doctrine this project has produced.

**On why the step exists** — `step-2b-map-design.md:9`, and it is a verbatim prediction of W1,
written months before v2 committed it:

> Without it, locations are a backdrop: enumerated as scenes demand them, then emitted at authoring
> by **copying a reference game's shape**. A premise whose geography differs from that reference
> ships incoherent and gets fixed by hand, pass after pass.

**On defaulting to a house** — `location-design.md:45`:

> The genre floor is a **multi-zone town** (zone → venue → room), NOT a single building… Choose the
> shape from the premise; don't default to "a house."

`back_home` is a house. v2 had no such rule, so nothing objected.

**On exteriors** — `location-design.md:77`, which is precisely the missing street:

> **Two roots, bridged by walk activities.** A home-exterior root and a town root are SEPARATE
> top-level locations with no `entry_from`, connected by walk-activity canvases… Keep the private
> unit, the shared building it sits in, and the town outside as distinct layers.

**On sizing, and a failure mode we have already lived** — `location-design.md:65`:

> Sizing is TWO axes: scale AND aliveness… the failure is **drifting** into a lifeless scene-holder
> because no one asked "how alive?" (Vesper's first map shipped "utilitarian, not a living world"
> exactly this way — the anti-sprawl rule followed off a cliff.)

**On rooms earning their place** — `location-design.md:225`, the room-content floor:

> every navigable location must host at least one canvas… A reachable, **empty-dead** room (no plot
> AND no ambient — the player walks in and bounces off) is the failure.

And it closes with a **13-item pre-ship audit** covering container traps, `navigation_order`
reciprocity, the locked-location unlock contract, reachability, and naming consistency.

## 3 · Where v1 is wrong

Four things, and the first is the one that matters most.

**a · It is a checklist, and checklists do not hold.** v1 states the problem itself at
`location-design.md:14` — *"The engine never checks any of this — a wrong, dead, or incoherent map
builds GREEN and only reveals itself in play."* Its answer is thirteen manual checkboxes. The
evidence that this does not work is in the same file, at `:257`, describing the locked-flag-with-no-
setter bug: **"Shipped twice: v1's Dining Room, then again in the rebuild written to prevent it."**
v2 must not inherit the checkbox; it must inherit the finding and turn it into a gate.

**b · Nobody has to sleep anywhere.** 274 lines about maps, and no rule that a character who lives
in a dwelling needs a room in it. **`back_home`'s W4 passes v1's entire 13-point audit** — every
location has a job, every schedule row is categorised, naming is consistent, and three adult men
still have no bed. This is a real hole in v1, not just in v2.

**c · The prose and the graph are never reconciled.** W6 — six references to a hall that does not
exist — also passes v1's audit clean. v1 checks the graph against the *design*; it never checks the
graph against the *written game*.

**d · It mixes design doctrine with engine minutiae, which v2 structurally forbids.** `SKILL.md:66`
is unambiguous: *"Engine facts are in `references/engine.md` — and **only** there."* v1's file
interleaves `auto_exit = false`, container double-printing, `navDestBlockedReason`, and passage-entry
guards with the design argument. Splitting the two is a requirement of v2's layout, not a preference.

**e · The archetype claim carries no number.** *"The genre floor is a multi-zone town"* is asserted
with example games and no measurement. It may well be true — a sandbox-nav survey behind it exists —
but v2's standard is that a threshold arrives with the count that produced it. Either the number
comes with the claim into v2, or the claim does not come.

## 4 · What v2 says instead

Map design belongs to the **`board` phase**, before any character is placed and before a word of
prose is written. It produces a decision recorded in `v2_state.json`, and the gates check the built
game against the game's own declaration.

### The four rules

**R1 · The map is a place, not a list of rooms.** Before locations are declared, name what kind of
place it is and write the graph down as something a person could walk. The test is not "does every
room have a job" — every room in `back_home` has a job. The test is: **could someone who has never
seen the game draw this building from the graph?**

**R2 · A dwelling houses its residents.** Every character the board declares as living in the
world's primary dwelling gets a `home` location recorded in `v2_state.json`. If a character sleeps
off-screen — a lodger on nights, a neighbour — that is declared too, explicitly, not by omission.
A game where the cast has nowhere to sleep is a set, not a house.

**R3 · If she travels, there is something to travel through.** Any destination the fiction places
away from the dwelling requires a connecting exterior location. This is not decoration: it is where
the ascent meters get a consequence surface outside the household, and it is the only renewable
source of new characters a domestic premise has.

**R4 · The graph owes the prose.** Nothing the writing treats as a place may be missing from the
map. When a paragraph says *hall*, either the hall exists or the paragraph is wrong. Both are
cheap fixes on the day and expensive twenty thousand words later.

### The engine capabilities v2 did not know it had

Verified against source during this study; all four are absent from `references/engine.md` and must
be added there with these citations before any of this ships.

| capability | field | citation |
|---|---|---|
| **travel friction** — a per-entry cost on a location, in time and any player trait | `costs = { time = 20, energy = 5 }` on `[[locations]]` | `template_import.py:170` (dataclass), `:1778` (parse); `v2.py:4681` (*"A location's per-entry cost lives in `setup.locations[slug].entry_costs`"*), `:15276` `has_location_costs` |
| **locked location** — visible but blocked, with in-world prose on the greyed card | `entry_conditions` + `blocked_message` | `template_import.py:159-160`, `:1775-1776`; `v2.py:6590` |
| **off-screen location** — a schedule label with no nav card | `offscreen = true` | `template_import.py:154` — *"Non-navigable 'away' location… no nav card, no hub, exempt from presence floor + reachability"* |
| **pure-nav wrapper** | `is_container` + `default_entry` | `template_import.py:153`, `:3968` |

`travel friction` is the direct mechanical answer to *"the shop is ten minutes' walk away."* Right
now that sentence is decoration, because arriving costs nothing. A `costs = { time = 20 }` on the
bridge is what makes a schedule bite — if crossing to work burns twenty minutes each way, then who
is home at which hour becomes a real constraint rather than a lookup table.

### What the board phase records

Extends the existing `board` block in `v2_state.json`, which already holds `locations` with a `job`
per entry:

```
board.map = {
  "shape":      "one dwelling + a street + one workplace",
  "exterior":   "the_street",
  "dwelling":   "the_house",
  "homes":      { "npc_ray": "rays_room", "npc_marek": "the_box_room", … },
  "bridges":    [ { "from": "the_street", "to": "the_shop", "costs": { "time": 20 } } ]
}
```

Declared once, in the board phase, before content. Then the gates check the game against it.

## 5 · The check

Four candidates. Two are hard gates; two are lints, and they are marked as lints because a check
that fires on correct work is worse than no check.

**Gate A · every location reachable from the start.** Walk `entry_from` / `navigation_order` from
`project.starting_canvas`'s location. Any location not reached, and not marked `offscreen = true`
or deliberately sealed (`auto_exit = false`), is a fail. Fully decidable from the merged TOML.

**Gate B · every declared resident has a home that exists.** Read `board.map.homes` from
`v2_state.json`; every value must be a real location id, and every character in `board.characters`
must appear as a key or carry an explicit off-screen declaration. This is the check that catches
W4, and it catches it **because the board had to state the answer first** — the gate compares the
game to its own design rather than guessing intent.

*This is the pattern worth generalising to later studies: where a property cannot be inferred from
the TOML, have the board phase declare it and gate the game against the declaration.*

**Lint C · building-part nouns with no location.** Scan authored prose for a small frozen list —
`hall`, `stairs`, `landing`, `street`, `front door`, `back door`, `garden`, `yard`, `attic`,
`cellar`, `porch`, `drive` — and report any that appear without a matching location. A lint, not a
gate: *"he came through the hall"* in a game that deliberately has no hall location is a judgement
call, not an error. It would have caught W6 on the first build.

**Lint D · declared exits that do not exist.** Report a location whose description or prose asserts
an exit (*"a door to the outside"*) that has no counterpart in the graph. Same frozen-phrase
approach as C, same lint status, catches W3.

**Deliberately not a gate: "is the map a coherent place."** It is the most important rule in this
study and it is not mechanically decidable. R1 stays a design rule that a human signs off in the
board phase. Pretending otherwise would produce a check that measures the wrong thing and lets the
real failure through — which is exactly how `back_home` shipped 10/10.

---
---

# Study 2 — How the game talks to the player

## 1 · What it is, and what breaks without it

Everything the player reads that **is not the story**: the room names on the nav, the labels on
activity links, the guidance page, the words under a meter, the text on a door that will not open.
It is the game speaking about itself, and it is a different job from prose — it has to be
unambiguous on a first read, by someone who has never seen the game.

No skill owns this category. Four findings, one cause.

**G1 — the guidance page is empty, and the nav links to it.** `0_systems_spec.toml:19` declares
`quests_engine = "v2"`, which emits the V2 QuestsPage (`v2.py:14711` dispatches on that key). The
authored table is `[[quest_cards]]` (`template_import.py:2462`). `back_home` declares **zero** across
all five phase files; the built game carries `setup.quests_cards = []`. So the sidebar shows
**Quests 📋**, and behind it a page headed *"What's Next"* with nothing under it.

**G2 — seven of eight locked doors say nothing.** Only `hub_cal_frontroom` carries `locked_text`.
`v2.py:13146` falls back to the choice text (`locked_text or choice_text`), so the other seven render
as a greyed copy of themselves. `locked_text_threshold` (`v2.py:13185-13186`), which prints an explicit
*"Requires …"*, is used **zero** times.

**W5 — two of eight room names are unresolvable.** *The Landing* is British for an upstairs hallway
and the game never says so; *The Box Room* is a small spare bedroom, here rented out.

**W7 — activity labels are written as voice.** *Sit with it* is the most-clicked link in the game —
the pass-time action, +90 minutes — and does not say what it does. *See to it yourself*, *The bench*,
*The regulars*, *Someone's in there*. Found the correct way: LO read the menu and asked what one of
them meant.

**What this costs, concretely.** Three chains exist that a player has no way to discover:

- `exposure ≥15` opens her mother's boxes, the only source of `worn_corruption ≥4`, the only key to
  `triggered_caught_in_passing`
- one specific kitchen choice at `exposure ≥35` sets `dean_open`, the sole unlock for Dean's entire
  late-night hub
- Ray is in the garage weekdays 18:00–20:00; Dean weekends 14:00–17:00

Against the measured genre failure: across a top-30 sandbox study, **lostness is the dominant player
complaint at a 4.7% median share of all comments, against grind's 0.9%.** Players quit lost, not
bored. `back_home` is a pure specimen — 97 canvases, 8 locked doors, three interlocking meters, and
no statement anywhere of what to do first.

## 2 · How v1 teaches it

v1's `references/quests.md` (285 lines) is the strongest single file in either corpus on this, and
its central rule is the one v2 needs most.

**On what a guidance line is for** — `quests.md:81`:

> **The label is a walkthrough line — place + person + verb (+ window).** "Flash him at the depot"
> passes; "Prove yourself to Renner" fails (no place, no clickable verb)… Atmosphere lives in the
> card's `text`; the label is load-bearing navigation.

**On what the player actually cannot see** — `:91`, and this is the rule that answers `back_home`
directly:

> **A meter-gated rung names its FEEDER, not just its number.** … not "she isn't ready" but "she
> won't go further until the lessons do — bring her a new word (her room, evenings)". **The HUD
> already shows the number; the ROUTE to raising it is what the player can't see.**

**On the page as a designed thing** — `:3`: *"The Quests page is a designed surface, not a pile of
per-beat cards."* Two tiers, free from the engine: a card with no `npc_id` goes to a top section, a
card with one goes to that character's own section, one live at a time by `priority`.

**On the ladder shape that fits a meter-driven game** — `:118`, the stepped trait-band ladder: one
card per exclusive band, gated `gte X` + `lt Y`, so exactly one matches and the card swaps as the
meter crosses. Proven live on Vesper's Renner across 28 checks.

**On two traps that produce silence** — `:137` and `:147`. A card whose numeric goal is met, with no
`ready_canvas` and not `terminal`, matches none of the three render frames and returns empty. Worse,
if an arc's last card retires with nothing behind it, the character's whole section **disappears** at
the exact moment they become permanent sandbox content. *(Measured: Renner's heading vanished and
nobody noticed for eleven beats.)*

## 3 · Where v1 is wrong

**a · It is a mechanics file wearing a voice file's title.** Of 285 lines, the overwhelming majority
are engine mechanics — render frames, picker symbols, condition evaluators, line numbers. The rule
about how a label should *read* is **one paragraph**. For the thing LO actually asked for — *"same
info, told better"* — v1 is thinnest exactly where we need it thickest.

**b · It does not recognise the category.** `quests.md` covers quest cards. Room names live in a
different file (`location-design.md §3`). Activity labels, `locked_text`, and the words under a meter
are covered **nowhere**. Four surfaces doing one job, split across two files and two gaps, so nothing
enforces a consistent voice across them. That is why `back_home` can have a careful naming style and
still be unreadable — each surface was written to its own instinct.

**c · Writing it down did not make it happen.** The file exists *because* Vesper reworked its quest
page five times — and then, with the file in place, Renner's section still disappeared for eleven
beats. Doctrine caught neither.

**d · Its top tier assumes a game v2 does not build.** `quests.md:173` lays out the top section as
*"the Story-Goals column — from the desire ladder: the mission's current want + next action, plus any
mission investigation threads."* **A v2 game has no mission and no ending.** The per-character tier
transfers cleanly; the mission spine does not, and copying it would smuggle a story shape into a
release stream. v2 needs a different answer for the top of that page.

**e · Pipeline-bound.** *"Read this at Step 5 … at Step 7 … at Step 6."*

## 4 · What v2 says instead

One category, one voice, five rules. This is the skill's **second voice** — `register.md` governs
what the player reads *after* clicking; this governs everything else.

> **The game's own voice is plain. It names a thing or an action and it never performs.**

**R1 · A label answers "what happens if I click."** Room names and activity links are navigation.
*Sleep*, *Wash*, *Take a shift*, *Listen through the wall* already work in this game; *Sit with it*
does not. **The register lives in the paragraph the click produces, not in the button.** In-scene
choice lines inside a hub are exempt and stay as voice — they arrive with the scene already on
screen.

**R2 · Every ascent tier carries a visible ladder.** v2 has no mission, so the top of the guidance
page is not a story spine — it is **the tiers themselves**. One `[[quest_cards]]` card per band of
each ascent meter, using the stepped trait-band shape, so the page always answers *what is the next
rung and what raises it.* This is the v2-native replacement for v1's Story-Goals column, and it falls
out of v2's own architecture rather than being borrowed.

**R3 · Name the feeder, not the number.** The HUD already prints `exposure 22`. What the player
cannot see is **which repeatable click moves it**, and in a game where every gate is a meter that is
the whole of navigation. Every card names a place, a person where there is one, and a verb.

**R4 · Every wall states its own key.** A choice rendered `show_when_locked` without `locked_text` is
a defect, not a style choice. The skill's own release doctrine already says it —
`the-release.md:93`: *"An honest wall is a promise; a silent one is a bug report."* Eight strings
would have converted eight dead grey lines into eight advertisements for the next release.

**R5 · Nothing retires into silence.** v1 found this trap; **v2 owns it far harder, because a v2
product never ends.** Every character becomes permanent sandbox content the moment their ladder tops
out, which is exactly when a badly-shaped chain makes them vanish from the page. Every arc needs one
card that still matches after the last rung.

### Engine facts to move into `engine.md`, with citations

None of this is in v2's engine reference. Verified this turn.

| fact | citation |
|---|---|
| the table is **`[[quest_cards]]`**, flat, not nested under `quests` | `template_import.py:2456-2462`; `class QuestsCard` `:997`, parser `:1068` |
| requires `quests_engine = "v2"` in project metadata or the overlay is not emitted | `v2.py:14711` |
| three render frames, exactly one per card: ✓ terminal / 🔓 `ready_canvas` / 🎯 unmet goals | `v2.py:14964` `renderQuestsGoalBlock` |
| card selection: `pickQuestsCards(scope)` for the top tier, `pickQuestsCard(slug)` returns the single highest-`priority` match per character | `v2.py:14837`, `:14065` |
| **quest conditions use a different evaluator and do NOT fail open** — never paste `version = "1.0"` onto a card | `v2.py:14878` `checkQuestsCondition` |
| the sidebar next row calls the identical functions — there is no separate "sidebar quest" | `v2.py:15454-15456` |
| a locked choice with no `locked_text` falls back to the choice text | `v2.py:13146` |
| `locked_text_threshold` prints an explicit "Requires …" hint | `v2.py:13185-13186` |

## 5 · The check

**Gate C · guidance exists.** At least one `[[quest_cards]]` card per ascent tier declared in
`board.ascent_tiers`, and at least one per character in `board.characters`. Fully decidable from the
merged TOML plus `v2_state.json`. Catches G1 on the first build — and note it would have fired on
`back_home` at the moment the board phase ended, long before 36,000 words were written.

**Gate D · every wall states its key.** Every choice with `show_when_locked = true` carries a
non-empty `locked_text` or `locked_text_threshold`. Fully decidable. Catches G2. Eight failures today.

**Gate E · no chain ends in silence.** For each `npc_id` appearing in `quest_cards`, at least one of
its cards is `terminal = true`, or is goal-less and `ready_text`-less (the end-of-content shape).
Decidable for the shape v1 documents; it does not prove every condition path, and the study says so
rather than overclaiming.

**Deliberately not a gate: whether a label reads well.** *The bench* is a plain noun and clear in
context; *Sit with it* is a plain phrase and is not. No rule separates them mechanically. This stays
a human sign-off in the board phase, alongside study 1's "is the map a coherent place."

**The pattern holds.** Gates C and E read the board's declaration and check the game against it —
the same move as study 1's Gate B. Where a property cannot be inferred from the TOML, the board
phase declares it and the gate compares. That is now two studies out of two, and it should be
written into the skill as the standard shape rather than rediscovered each time.

---
---

# Study 3 — Money & pressure

**This is the first study built on primary measurement of more than one game.** 18 shipped browser
sandboxes were pulled and parsed — the corpus, the method and its limits are in Appendix B.

## 1 · What it is, and what breaks without it

Money is the only system in a sandbox that can make the player *choose*. Everything else expands;
money is the one thing that says no. If it never says no, every arc gated behind it becomes optional
scenery.

`back_home`'s state, from the merged TOML:

```
conditions anywhere that read money ...... 0
items declared ........................... 0
sinks besides the engine's rent .......... 0
canvases carrying a real `costs` block ... 2   (both at the shop)
```

Against £120/week rent, income is £42/day from two once-daily surfaces — plus
`activity_shop_regulars` at £10 per 2 hours, **uncapped and free**. So money is not merely
sufficient, it is **unbounded**.

The design intent is stated at `0_systems_spec.toml:33`: *"120/week is four shifts — most of her
week, survivable, and one bad week forces the ask."* **No week forces the ask.** Ray's entire
front-room ladder is gated on `need` at 15/35/45/55/75, and nothing ever pushes the player toward
any of it — while the Want's own check names Ray as the character a player would most miss.

## 2 · How v1 teaches it

v1's `references/rent.md` (278 lines) is a good file about **one mechanism**. It is verified against
live code, it names the engine's key set exactly, and it gets three things right that v2 should keep:

**Rent is a clock, not a tax** — `rent.md:5`:

> Rent is the simplest mechanical engine for the "I Need Money" opener: it converts "you could work"
> into **"Friday, $125, or else."**

**Give the obligation a face** (§6, `collector_npc`) — a person collects, so the pressure is social
as well as arithmetic. `back_home` does this correctly: Ray collects, in the kitchen, and hates it.

**Arm it after income exists** (§7, `start_after_flag`) — pressure before the player has a way to earn
is a scripted loss, not a choice.

And its budget rule, §8:

> **Rule: `amount` must be clearable by the first post-arm due date with margin** — tune it against the
> income channels, not in a vacuum. Rent that can't be paid isn't pressure, it's a scripted loss.

## 3 · Where v1 is wrong

**a · It only guards the downside.** §8's entire safety rule is *don't make it unpayable.* There is
**no corresponding rule against making it trivially payable**, and no measurement of what the ratio
should be. `back_home` followed v1's rule exactly — rent is clearable with enormous margin — and the
pressure evaporated. A rule with a floor and no ceiling produces exactly this failure, and the
corpus below shows the missing half is measurable.

**b · It is scoped to rent, and rent is one mechanism.** §1 waves at alternatives — *"a savings goal,
a debt, or purchase-gated progression"* — and develops none of them. There is no general doctrine of
**sinks**: what money should be for, how many ways to spend there should be, whether prices move.
That is why `back_home` ships **zero items** and one sink.

**c · Nothing connects money to the ascent tiers.** In a v2 game every meaningful gate is a meter,
and money's job is to be the thing that makes a meter-raising choice cost something. v1 treats money
as a survival subsystem sitting beside the arcs rather than as the pressure that drives them.

**d · Pipeline-bound**, like the rest.

## 4 · What v2 says instead — the measured rules

Every number below is measured across 18 shipped games (Appendix B). Where the corpus is ambiguous,
the study says so rather than inventing a threshold.

### R1 · Money must gate content

**Measured: median 67.3 conditions reading the currency per 1,000 passages.**

| | gates/1k | | gates/1k |
|---|---|---|---|
| shady_deals | 605.6 | destroyer | 66.3 |
| generic_porn_game | 327.2 | become_someone | 55.1 |
| back_to_freedom | 262.0 | zaras_school_life | 44.4 |
| life_at_university | 156.2 | road_to_success | 29.5 |
| new_life_project | 95.1 | the_company | 26.0 |
| galactic_outlaws | 91.4 | **degrees_of_lewdity** | **23.8** |
| better_sit_home | 70.4 | course_of_temptation | 15.1 |
| apocalyptic_world | 68.3 | gakko | 4.8 |
| | | **back_home** | **0.0** |

The only games at zero are `emilie` and `lustbound` — a scripted time-slot game and a small one.
**Every sandbox in the set gates on money.** `back_home` sits with the two that are not sandboxes.

### R2 · Sinks outnumber sources

**Measured: median spend-site : earn-site ratio = 2.2 : 1**, across the 14 games with enough flow to
measure. `the_company` 48:1 · `back_to_freedom` 4.8:1 · `destroyer` 3.4:1 · **`degrees_of_lewdity`
1.76:1** · `become_someone` 1.3:1. Only three games invert it, and all three are the small ones.

**The floor v2 adopts is 1:1** — generous against a 2.2 median, and it still catches `back_home`,
which has three sources and one sink.

### R3 · The obligation is near-universal, and it is not optional furniture

**Measured: 14 of 19 games carry real recurring-obligation vocabulary** (rent / debt / loan / bill /
tuition, ≥10 mentions). `back_to_freedom` says *debt* 142 times. **`degrees_of_lewdity` says *rent*
130 times.** `road_to_success` 57.

`back_home` has the obligation and gets this one right. It is the only part of its economy that works.

### R4 · Prices should move with state

**Measured: a median 24% of money movements carry a computed rather than a literal amount** — 86% in
`life_at_university`, 57% in `shady_deals`, **21% in DoL**. Real games price things off the player's
situation, not off a constant.

`back_home`: every grant is a hardcoded literal. This is the softest of the four rules — the corpus
range is wide — and v2 states it as guidance, not a gate.

### R5 · No free, uncapped income

Not from the corpus — from the failure. A repeatable surface with **no daily cap and no `costs`
block** that grants currency makes every other rule void, because the player can print money. This is
mechanically checkable and it is the single line that would have caught `back_home`'s `E1`.

### And the finding that justifies the whole exercise

**DoL carries 738 money movements, 372 money gates, and says *rent* 130 times.** v2 derived every one
of its ten thresholds from this game's source — word counts, location counts, explicit-word ratios —
and **never once measured its economy.** The blind spot is not theoretical.

## 5 · The check

**Gate F · money gates something.** At least one condition in the merged TOML reads the currency
declared in `board.need_engine`. A floor, not a target — the corpus median is 67 per 1,000 passages
and our games are far smaller, so a rate threshold would be noise. Catches `back_home` at 0.

**Gate G · sinks ≥ sources.** Count distinct canvases granting the currency vs distinct canvases or
conditions consuming it, engine rent included. Floor 1:1 against a measured median of 2.2:1.

**Gate H · no free uncapped income.** Fail any repeatable canvas that grants the currency while
carrying neither `max_triggers_per_day` nor a `costs` block. Fully decidable. One rule, and it is the
one that broke this game.

**Deliberately not a gate: whether the pressure is felt.** Whether £120 against a £42 day *squeezes*
is a play question. The three gates above establish that a squeeze is possible; only a playthrough
establishes that it happens. Third study running that refuses to gate the thing it cares most about,
and the reason is unchanged — a proxy check is how `back_home` shipped 10/10.

---

## Appendix B · The economy corpus — method and limits

**What was pulled.** 18 shipped browser sandboxes, ~62,000 passages, obtained 2026-08-12 as complete
single-file SugarCube source. Game URLs came from this project's own prior live-play sessions in
`game_explorations/`; `mopoga.com/<slug>` landing pages carry the real file URL in a
`data-game-url` attribute, and those `/embed/` URLs serve the full compiled game with `tw-storydata`
intact.

The set: `degrees_of_lewdity` (15,626 psg) · `course_of_temptation` (5,294) · `destroyer` (5,236) ·
`gakko_no_monogatari` (4,836) · `become_someone` (3,287) · `back_to_freedom` (2,252) ·
`the_company` (2,075) · `new_life_project` (1,683) · `apocalyptic_world` (996) ·
`life_at_university` (890) · `zaras_school_life` (788) · `shady_deals` (710) · `lustbound` (673) ·
`emilie_finds_a_way` (619) · `galactic_outlaws` (525) · `road_to_success` (373) ·
`generic_porn_game` (327) · `better_sit_home` (142).

**Two extraction bugs found and fixed before any number here was trusted.** Recorded because the
first pass produced a confident, wrong table:

1. **Passage bodies are HTML-escaped in a compiled Twine file.** `<<set $money += 5>>` is stored as
   `&lt;&lt;set …&gt;&gt;`, so every macro regex silently matched nothing. DoL initially read as
   *"0 spending sites"* next to 372 gates — obviously impossible, which is what exposed it.
2. **Money mostly moves through per-game widgets, not raw `<<set>>`.** DoL uses `<<money -350000
   "farmUpgrades">>`; `life_at_university` uses `<<addmoney 10>>` / `<<redmoney $taxiprice>>`;
   `shady_deals` uses `` <<money `$junk_price`>> ``. The final extractor discovers each game's money
   widgets from its own `<<widget>>` definitions and counts call sites by argument sign.

**Also corrected:** the currency variable is now chosen by **how it is used** (arithmetic + gate
occurrences) rather than by name frequency, after `road_to_success` initially resolved to the decoy
`$game.randomMoney` instead of `$player.money`.

**Known limits, stated rather than hidden:**

- **`back_home`'s earn/spend counts are not comparable** and are excluded from R2's median. Our engine
  represents effects as JSON data, not as inline macros, so a macro-scanner cannot see them. Its
  **gate count of 0 is comparable and is independently confirmed** from the TOML: zero conditions
  anywhere read money.
- `back_to_freedom` is not a standard Twine compile (no `tw-passagedata`); its passage count comes
  from a `<div>` container and its per-1k figures are softer than the rest.
- Obligation vocabulary is a keyword count. It shows an obligation is *present and load-bearing*, not
  how hard it bites.
- Everything here measures **structure, not feel.** No number in this study says whether a game's
  economy is enjoyable — see the refusal in §5.

**A second use for this corpus.** Those 62,000 passages are also the first real prose sample this
project has held. **Study 4 (how the prose is written) should measure against it rather than assert**,
which would make it the second study grounded in more than one game.

---
---

# Study 4 — How the prose is written

Measured on the same 18-game corpus as study 3, scored with **`gates.py`'s own frozen explicit
regex** so the field and our game sit on one instrument. Limits in Appendix C — read them before
quoting any number here, because two of the four measurements do **not** transfer to our engine.

## 1 · What it is, and what breaks without it

Everything the player reads after clicking: paragraphs, dialogue, thought. It is the bulk of the
game and v2 barely mentions it.

```
v1  references/rts-flat-prose.md .... 735 lines — the largest file in either corpus
v2  references/register.md .......... 111 lines
```

And v2's 111 cover **one topic**: how to write an explicit beat, and one recurring defect in doing
so. Sentence length, dialogue, how an ordinary non-sexual paragraph should read, how thought is
handled — none of it is written down anywhere in v2.

## 2 · How v1 teaches it

`rts-flat-prose.md:12` states the register as three things, and only the first is length:

> 1. **Few words PER CLICK.** ~35–40 words per beat — **flat across every tier.** You escalate a
>    scene by adding *beats*, not by fattening paragraphs.
> 2. **SPOKEN, not narrated.** RTS runs **0.73 narration words : 1 dialogue word** — more dialogue
>    than narration, including in its sex scenes. Every game this skill has shipped runs 5:1 to
>    19:1 the other way. **This is the drift.**

Plus Rule 6 (`:311`) — crude is the default at the sexual register, with a per-NPC ceiling — and
Rule 9 (`:360`), added after the diagnosis that a game can satisfy every other rule and still read
as *"a cold literary thriller that happens to contain sex."*

## 3 · Where v1 is wrong — and the one place it cannot be judged

**a · Its most load-bearing claim rests on one game — the same error v2 made.** The 0.73:1
narration-to-dialogue ratio is measured from *Road to Success* alone and then used to declare every
game this project ships "drifted." One game is a hypothesis, not a norm.

**b · And I could not test it.** *Road to Success* is built almost entirely from HTML/CSS interior
markup — its passages are laptop UIs and styled panels — so only **31 of its 373 passages** survive
prose extraction. **v1's headline number is untestable from the compiled artifact**, and this study
does not claim it is wrong. It claims it is unverified, which for a rule that calls everything else
"drift" is its own problem.

~~What the corpus *can* say: the field median is **33:1 narration:dialogue**, and the two most
prose-dense games in it are the two most dialogue-heavy — **DoL at 2.7:1**, `course_of_temptation`
at 3.8:1. So dialogue-forward writing at scale is real and the direction of v1's instinct survives;
the specific number does not transfer.~~

> ### ⛔ SUPERSEDED 2026-08-18 — the 33:1 was the instrument, not the field
>
> Struck rather than deleted, because the trail is the point: this paragraph is why
> `register.md` demoted v1's dialogue rule to *"a direction, not a threshold"*, and the demotion
> stood for six days.
>
> **The measurement counted text inside `"quote marks"`. 20 of the 25 games in the corpus do not
> use them.** They render speech as a UI component — `<<speech>>`, `<<say>>`,
> `<<nm "Karlee" "…">>`, `<<chat portrait "…">>`, `<div class="npctextbox">`, or one container
> macro per character (`<<Mc>>`, `<<AmyBd>>`). A quote-counter sees none of that and reports the
> game as pure narration.
>
> Re-measured 2026-08-18 on the same corpus, one rendered path per passage, with each game's own
> speech convention read out of its source first:
>
> ```
> game                 quotes only    + its own speech UI
> corpo-life               584.9:1               0.30:1
> sluttown-usa             762.0:1               0.63:1
> become-taxi-driver       142.1:1               0.72:1
> family-business            >999:1               1.15:1
> destroyer                 71.7:1               1.44:1
> apocalyptic-world        120.6:1               1.83:1
> the-company              290.1:1               2.69:1
> degrees-of-lewdity         3.6:1               3.62:1   <- unchanged
> course-of-temptation       4.6:1               4.57:1   <- unchanged
> patriarch                  2.9:1               2.93:1   <- unchanged
> MEDIAN                    65.3:1               2.93:1
> games at <=2:1                  0             10 of 25
> ```
>
> The three that do not move are the three that punctuate speech with quote marks — **DoL and
> course_of_temptation among them.** This study did not find the two most dialogue-heavy games in
> the corpus; it found the two whose dialogue its instrument could see. The most dialogue-dominant
> game in the set, `corpo-life` at 0.30:1, was read as 585:1 narration.
>
> **The corrected finding: field median 2.93:1, ten of twenty-five games at or under 2:1.** v1's
> Rule 4 was right in direction and too extreme in number — its 0.73:1 came from one game. The rule
> is restored as **gate 32 · somebody speaks**, ceiling 5:1, with the derivation in the
> `NARRATION_DIALOGUE_CEILING` constant. `references/register.md` S3.
>
> Item 4's other three findings (sentence length, second person, the reference game is the coldest)
> re-measure unchanged and stand.

**c · The 35–40 words-per-beat figure cannot be checked from a compiled game either.** A Twine
passage is not a beat, and our own engine emits a whole canvas as **one** passage — `back_home`'s
median passage is 429 words against a field median of 175, which measures architecture, not
register. Appendix C.

## 4 · What v2 says instead — three measured, one inherited

### R1 · Sentences run short. Ours do not.

**The one length measure that transfers**, because a sentence is a sentence regardless of how
passages are cut.

| | median sentence |
|---|---|
| field median (17 games) | **10 words** |
| degrees_of_lewdity | **9 words** |
| course_of_temptation · destroyer | 10 · 9 |
| **`back_home`** | **16 words** |

`back_home` writes sentences **60% longer than the field and nearly double the reference game's**,
and is third-longest of eighteen. This is the first hard, measured confirmation that our prose is
denser than the genre — the thing "RTS-flat" was always reaching for, now with a number.

### R2 · Second person is the genre standard

**13 of 17 games are second-person dominant.** `back_home` is at 94% *you/your* — the highest in the
corpus, alongside `shady_deals` and `course_of_temptation` at 90 and DoL at 84. Third person is a
minority position held by three games.

v2's `narration_person` setting and its second-person default are **validated by the field**. This
is the one piece of v2 prose doctrine the corpus confirms outright.

### R3 · The reference game is the coldest game in its own genre

Scored on `gates.py`'s frozen regex, percentage of prose passages carrying 3+ explicit words:

```
zaras_school_life  72.2      destroyer          43.1      new_life_project  28.0
become_someone     60.4      gakko              37.8      road_to_success   22.6
emilie             56.0      apocalyptic_world  37.2      better_sit_home   18.4
the_company        48.1      generic_porn_game  33.3      galactic_outlaws  17.9
life_at_university 46.2      lustbound          31.7      shady_deals       14.8
back_home          43.4                                   course_of_temptation 10.0
                                                          degrees_of_lewdity    7.5
                              FIELD MEDIAN 33.3%
```

**DoL is last. Every other game in the corpus is hotter, and the median is more than four times it.**

Note what DoL's 7.5% is: `gates.py` sets `EXPLICIT_BEAT_FLOOR = 7.5`, derived from this game. This
run reproduces that derivation independently on a different unit — and shows the number is **a
property of DoL, not of the genre.**

So v2 took its heat floor from the coldest game in the field and adopted it as the standard. As a
*floor* it is still valid and still discriminating (the measured-cold game scores 4.7%). As anything
resembling a target it is badly miscalibrated.

**And this closes the `back_home` heat worry for the second time, from a second direction.**
`REVIEW.md` O1 already showed the 27.8% was measured on a different denominator. Now the field
comparison says the same thing outright: at **43.4%, `back_home` sits mid-pack with five games above
it.** It is not too hot. It never was.

### R4 · Crude at the sexual register, with a per-character ceiling — inherited, not re-measured

v1's Rule 6 and Rule 9 stand. Nothing in this corpus contradicts them and this study did not attempt
to measure "is it arousing," which is not a countable property. Carried into v2 on v1's evidence,
flagged as inherited rather than measured.

## 5 · The check

**Gate I · median sentence length.** Computable directly from the merged TOML's prose blocks, no
declaration needed. The field says 10 and the reference says 9; a **ceiling of 14** is generous
against both and still fails `back_home` at 16. The first gate in this whole exercise that measures
*writing* rather than structure.

**Not a gate · explicit density.** `gates.py` already has one, and this study's finding is that its
threshold is a **floor derived from an outlier** — the fix is to say so in the header, not to add a
second check. Raising it toward the field median would be inventing a target the evidence does not
support.

**Not a gate · narration person.** Already an authored setting, already validated. Nothing to check.

**Not a gate · dialogue ratio.** v1's number is untestable from a compiled game and the field spread
runs 2.7:1 to 500:1 — far too wide to threshold. It belongs in doctrine as a direction, not a gate.

**Deliberately not a gate: whether the writing is good.** Fourth study running.

---

## Appendix C · The prose corpus — method and the six traps

Same 18 files as Appendix B, plus `back_home`'s built HTML through the identical script.

**Prose passages are isolated** by dropping any passage tagged `widget` / `script` / `stylesheet` /
`init` / `startup` / `header` / `footer`, any body containing a `<<widget>>` or `<<script>>`
definition, anything under 20 words after stripping, and — the load-bearing filter — **anything whose
stripped text is under 40% of its raw length**, which removes CSS-and-markup passages that survive
tag-stripping as word-like fragments.

**Six extraction traps, all found by a result being obviously wrong:**

1. **HTML-escaped macro bodies** (study 3) — `<<set>>` never matched.
2. **Money moves through per-game widgets** (study 3), not raw `<<set>>`.
3. **Speech is a UI COMPONENT, not punctuation** (added 2026-08-18 — the trap that superseded this
   study's dialogue finding). 20 of 25 games render dialogue through `<<speech>>`, `<<say>>`,
   `<<nm "Name" "…">>`, `<<chat portrait "…">>`, a `class="npctextbox"` div, or one container macro
   per character. **Read each game's own convention out of its source before counting anything as
   narration.** The quote-only instrument reported `corpo-life` — 70% spoken — as 585:1 narration.
4. **Static source counts branches the player never sees** (added 2026-08-18). `destroyer:ginablow`
   is eight `<<if>>` branches printing the same four words over a different image. **Collapse
   if/elseif/else chains to one branch before measuring length**; doing so moves the corpus median
   from 115 words to 88 and brings DoL's median from 82 to 54, in line with its known figure.
5. **A clamp guard is not a gate** (added 2026-08-19, meter study). `<<if $lust lt 0>>` followed by
   `<<set $lust to 0>>` is the author bounding a variable, not gating content — and `corpo-life`
   carries **2,889** of them on one variable. Counting them reported that meter at 3,235 gates when
   the real figure is **346**, and would have made a 0–100 arousal bar look like the most gated thing
   in the corpus by an order of magnitude. **Count only comparisons against a threshold strictly
   inside the meter's own range.** Same family as trap 3: the instrument did not report a smaller
   number, it reported the wrong one.
6. **The longest "prose" passages are widget libraries and CSS.** Before the tag filter, the longest
   passage in `back_home` was the engine's widget library, in DoL a combat widget, in
   *Road to Success* a styled laptop UI. This inflated every median and poisoned every denominator —
   the first-pass table showed a field median of 138 words and DoL "8.0% hot" against a denominator
   stuffed with combat text. **Nothing in this study is quoted from that pass.**

**What does not transfer, stated plainly:**

- **Passage length.** Our engine emits a whole canvas as one passage; a Twine game cuts a passage
  per click. `back_home`'s 429-word median vs a 175-word field median measures architecture. The
  35–40-words-per-beat rule is **neither confirmed nor refuted here.**
- **v1's 0.73:1 dialogue ratio.** Untestable — only 31 of *Road to Success*'s 373 passages survive
  extraction. *(But the field figure it was compared against was wrong; see the superseded block in
  item 4 §3b. Corrected field median 2.93:1.)*
- **`back_home`'s prose sample is small** — 122 passages against DoL's 10,215. Its sentence-length
  and person figures are stable at that size; its hot% is noisier than the field's.
- Everything here measures **shape, not quality.**

---
---
---

# Study 5 — What the field actually does in play

## 1 · What it is, and what breaks without it

Every measurement in studies 1–4 was a **parse**. Link counts, word counts, sink counts, gate
counts. Nobody had opened one of these games.

This skill's own `references/agents.md` indicts that method: *"in a thirty-game study, the three
games that were actually played produced every single heat finding in the corpus, and the
twenty-seven that were only parsed produced none."*

Three rules had already shipped into `gates.py` and the reference files as **inferences that had
never been observed**: the 8-choice cap (gate 20), guidance-must-exist, and sinks-must-be-spread.
This study played the field to see whether they survive contact.

**Five games, 198 recorded turns**, driven through `.claude/skills/twine-game-explorer/scripts/live.js`.
Every turn logged to `game_explorations/<slug>/study_turns.jsonl`: passage, visible choices, explicit
hits scored with `gates.py`'s own frozen `EXPLICIT` regex, engine state snapshot, in-game clock.

| game | turns | why this one |
|---|---|---|
| `degrees_of_lewdity` | 74 | the reference the whole skill derives from — measured ten ways, never played |
| `course_of_temptation` | 61 | ships literal in-game hint cards. The guidance exemplar |
| `generic_porn_game` | 29 | the parse's menu outlier — median 18 links/screen. The decisive test of the cap |
| `shady_deals` | 17 | heaviest money-gating in the field (605 gates/1k) |
| `destroyer` | 17 | ~151 one-line staged hints in NPC voice — guidance done a second way |

## 2 · How v1 teaches it

It does not. v1 has no play-derived doctrine at all; `lanes.md`, `rts-flat-prose.md` and the
mechanism audits are all readings of source. This study has no v1 counterpart to quote — which is
itself the point, and the reason the same blind spot reached v2 intact.

## 3 · Where the parse is wrong

**Three of the four headline parse figures did not survive being looked at.**

**The GPG outlier does not exist.** The parse put GPG at a median of 18 links/screen with 55% of
screens over 12 — the single strongest argument that our cap of 8 was too low. Live, its house hub
is **five buttons**, its city map **ten**, its mall **eight**. The parse was counting `<img>` tags
inside image-button hubs as links. GPG's real median is **4**.

**"Screens over 8 are common" is an artifact of mixing screen kinds.** Across all five games, every
screen above ~12 choices is a **builder, roster, wardrobe or tracker** — CoT's appearance builder
(99), destroyer's quest tracker (151 portrait tiles, most locked), DoL's wardrobe (35), CoT's class
picker (30). Separate those out and the play surfaces are:

```
game                play screens   median   max   over 8
degrees_of_lewdity        35          5      12     11
course_of_temptation      39          3      15      2
generic_porn_game         11          4      10      1
shady_deals               10          3      10      1
destroyer                 16          1       6      0
```

**And the last denominator seam — the fourth in this project.** DoL is the only game with many play
screens over 8, and all eleven are streets. Split one:

```
Cliff Street ......... 12 links
  onward travel ...... 4   (glossed: "Barb Street (0:05) (Studio)")
  travel affordances . 4   (bus, loiter, alleyways, manhole — identical on every street)
  things to do here .. 4   (Watch pillory, Mayor's Office, Beach, Cafe)
```

Across all eight street screens sampled: **things-to-do-here has a median of 3 and a max of 4.**
The rest is a navigation frame the player learns once and never reads again.

> **The fourth denominator mismatch is in this comparison, not in the gate.** Ruled 2026-08-13 by
> reading the code instead of reasoning from the play log: **259 of 259 choices in `steam` and
> `back_home` carry `targetType = "node"`.** Our engine renders location-to-location navigation as
> engine chrome, not as canvas choices, so gate 20 *already* counts only decisions local to the
> place. A DoL street's 12 links are 4 exits + 4 travel affordances + 3–4 decisions; the same street
> authored here would present 3–4 choices and eight pieces of chrome. The failure case's front desk
> was 23 choices *of which 23 were decisions*, eleven of them purchases — correctly failed.
>
> So the mismatch was **our-authored-decisions vs DoL's-total-on-screen-links**, which is a fault in
> the paragraph above, not in `gates.py`. **The ceiling of 8 stands.** Field local-decision counts
> run 1–6 (max: the cafe, 6), so 8 keeps the same slack over the observed maximum that the original
> derivation used. Dropping to 6 would invent precision five games on one route each cannot carry —
> the exact failure that demoted R5 and R6.

## 4 · What v2 says instead

### The verdicts required by the plan — confirmed, refuted, or untested

| shipped rule | verdict | evidence |
|---|---|---|
| **Gate 20 · 8-choice cap** | **upheld** (first read "refuted" — see §3) | 11 DoL play screens exceed it, but only as *total links*. Separating exits and travel affordances puts field screens at 1–6 *decisions*, and our engine never authors exits as choices — so the gate was already comparing like with like |
| **Guidance must exist** | **confirmed, 4/4 games that have a hub** | four different mechanisms, all always-reachable — below |
| **Sinks must be spread** | **not established by this study** | `shady_deals` was cut short at 17 turns before its sink map was walked. Its top-level objective *is* a cash threshold, which supports R1, not R2 |
| **`the-surfaces.md` R5/R6 (lints)** | **still untested** | needs the free-play hour; DoL's bedroom does contract 10→6 on state, which is R6 evidence in the choice list rather than the prose |

### R1 · A location screen is exits + affordances + **at most four things to do here**

The count that matters is **decisions local to this place**. Field median 3, max 4, across five
games. Onward travel and standing affordances are frame, not menu.

### R2 · Every choice hangs off a named object in the prose

Three games independently, and it is the single most consistent shape in the corpus. CoT's dorm:

```
Your dorm room cot is against one wall.
🛏️[1] Sleep
💦[2] Masturbate in bed   Disinhibition 1

Past the end of your bed is a small closet and shelf set.
👕[4] Clothes
```

DoL's bedroom and `shady_deals`' Downtown do the same. **The wall of buttons is not caused by the
count — it is caused by choices that float free of the prose.** Eight anchored choices read as four
sentences; eight unanchored ones read as a menu.

### R3 · The label carries its own cost, gate and consequence

Measured on every game that has costs. Not one made the player click to find out:

```
Buy coffee (0:02 £2)                  DoL — time and money
Flirt | Promiscuity 1                 DoL — which meter it feeds, and the tier
Long Sleep (10:00) Rest >>>>>         CoT — duration and magnitude
Take a walk (-0.5 energy)             GPG
Move to secluded area with him.[2]    shady_deals — plus an inline risk gloss
  Very unlikely thats your life is in danger, he's just horny.
```

Measured label length across 1,009 rendered labels: **median 1–3 words, p90 1–7, max 12.** Our
own games are not out of band here — this is the Tier 1 item 4 answer, and it is about *content*,
not length.

### R4 · The label keeps the want; the reason sits next to it

Four games, four refusals, and **the reason is never on the label in place of the action**:

```
DoL     label on the street:  Strip club (0:01)              ← the plain want
        behind the door:      The strip club is closed. A sign reads:
                              "Opening hours: 18:00 - 06:00"
                              The lock looks beyond your ability to pick.
                              Skulduggery required: D
CoT     label:                [1] Strip                       ← the plain want
        body after clicking:  On second thought, you don't feel comfortable being
                              that undressed here. (Need Exhibitionism 2)
shady   label:                Check the local stroll.[7]      ← the plain want
        adjacent prose:       It's under Street Gangs control.
GPG     label:                Enter (CLOSED)                  ← want PLUS state suffix
```

> ⚠️ **Correction, ruled 2026-08-13.** This section first read *"a closed door states its own
> requirement"* and concluded that `engine.md` §15 was *"contradicted by every game in the corpus
> that has a gate."* **That was wrong, and it is worth keeping the reason visible.**
>
> §15 governs `locked_text`, which **replaces** the action label — set it and *"the player never
> sees what the action was called."* Its ruling is *"prefer the want unless the gate is genuinely
> obscure."* Every game above **keeps the want on the label** and puts the reason somewhere else:
> adjacent prose, a state suffix, or the passage behind the door. **That confirms §15's preference;
> it does not contradict it.** The comparison was between a label-replacement rule and evidence
> about where reasons are *placed* — two different axes.
>
> **§15 stands unchanged, and the withdrawn locked-door gate stays withdrawn.** What the field adds
> is a separate, additive rule §15 never spoke to: *the reason should be reachable adjacent to the
> want* — before the click as prose or suffix, or immediately after it. Not gated: which of the
> three placements is right is an authoring judgement.

### R5 · Guidance is always-reachable, and it names a place and a verb

Four mechanisms, all present, none requiring the player to have paid attention earlier:

- **DoL** — a persistent sidebar line on *every* screen (*"You have school tomorrow"*), plus a
  JOURNAL with a dated **Time-Sensitive** section: *"Bailey wants £100 on Sunday."*
- **CoT** — categorized hint cards with In Progress / Completed states, each ending in a route:
  *"Go to Summit Market (next to your residence hall) and apply for a job."*
- **destroyer** — a per-NPC card, one line, in that character's voice: *"My bedroom. You need to
  start pulling your weight around here."*
- **shady_deals** — a numbered whiteboard where each goal carries its own route: *"Own a warehouse.
  The warehouse district is located at the harbor."* Plus a diegetic NPC Q&A at chargen with a
  literal *"What do you recommend me to do first?"*

**All four name a place. Three name a verb. None is a bare percentage.** That confirms
`the-voice.md` R4 as written and is the strongest single result in this study.

### R6 · The world moves on its own — and this is where our games are thinnest

M4, measured as engine-state movement per turn:

```
degrees_of_lewdity   93% of turns   median 16 variables moved   max 25
destroyer           100%            median  2                   max  3
generic_porn_game    68%            median  2                   max  6   (nav bookkeeping only)
shady_deals          62%            median  2                   max 10
course_of_temptation 60%            median  1                   max  7
```

The raw percentage is a poor discriminator — the **magnitude** is the signal. DoL moves an order of
magnitude more state per turn than anything else in the corpus, and it is felt: in 74 turns it fired
**four unrequested events** (an assault on leaving the orphanage at 07:02, a street-seduction prompt
in transit, a friendly-stranger encounter on Loiter, and a soaking that forced an exposure chain
through the orphanage).

The contrast is the finding. **GPG: six consecutive identical loiters at the mall, zero state
movement, zero events, byte-identical prose.**

### M1 · Time to first heat

| game | first screen at 3+ explicit words | reached by |
|---|---|---|
| `degrees_of_lewdity` | **turn 9 · 07:02, two in-game minutes** | walking out the front door |
| `course_of_temptation` | turn 11 (backstory picker), turn 16 first playable | prologue |
| `generic_porn_game` | **none in 29 turns / 4 in-game hours** | — |
| `shady_deals` | none in 17 turns | — |
| `destroyer` | none in 17 turns | — |

DoL's first heat is **not sought — it is triggered**, and it is a *repeatable system* (combat), not a
one-shot scene. That reframes the measure: the reference game's answer to "when does the player meet
the content" is *before they have made a single meaningful choice, via a mechanic they will meet
hundreds of times.*

**No threshold is proposed from this.** Three of five games produced no heat at all in a first
session, so a "turns to first heat" gate would fail most of the field. Tier 1 item 1 stays open, and
this study says why: **the placement is the finding, not a number.**

### R7 · Re-entry variation — the free hour's finding, and it corrects `the-surfaces.md` R6

A second unstructured DoL session (43 turns, `game_explorations/dol_free/`) revisited the same
surfaces repeatedly and diffed the rendered prose. This is the measurement the R6 lint was explicitly
waiting on.

```
passage              visits   distinct bodies   distinct FIRST lines
Ocean Breeze Work        8            5                  5
Ocean Breeze             6            5                  2
Barb Street              3            2                  1
Domus Street             3            2                  1
Orphanage                3            2                  1
```

**A DoL location's opening sentence is byte-identical on every visit.** Six visits to the cafe, six
times *"You are in the Ocean Breeze Cafe."* The variation is real and it is dense — but it is not in
the opener, and it is not banded on an ascent tier. Four separate mechanisms:

1. **A condition clause appended to the identity sentence** — *"...No one is sitting outside due to
   the rain"* becomes *"The cafe is busy, and despite the strong winds some people are sitting..."*.
   Weather and crowd, not progression.
2. **One presence line per NPC actually there** — *"You see Sam attending to the customers."* appears
   only once you hold the job; *"Gwylan sits alone on the exterior balcony"* only when she is present,
   and that is the visit where the choice count jumps 8 → 9.
3. **The choice list itself moves** — 5 → 9 → 8 across six visits at one location, as the job
   replaces the on-ramp and NPCs arrive and leave.
4. **An event replaces the whole screen** — two consecutive Barb Street visits rendered a street
   harassment scene *instead of* the location menu, then the third rendered the menu normally.

And on the repeatable **action** rather than the room, variation is a scenario draw: eight cafe
shifts produced **five distinct scenarios**, each with its own choices, one carrying a visible skill
check — *"Take them all out at once | Dance: Impossible"*, which states not just the requirement but
whether you currently pass it.

> **`the-surfaces.md` R6 is wrong about the mechanism.** It says *"A hub re-entered daily whose first
> paragraph never changes is a dead screen. Band it on whichever tier the location serves."* In the
> reference game the first paragraph **never changes**, and it is the least dead game in the corpus.
> This also explains the seam that forced R6 to become a lint: our TOML test asked whether the opener
> carries a conditional block, which is a thing DoL does not do — so our games scored 0/22 against a
> practice nobody follows.

## 5 · The check

| | |
|---|---|
| **Gate 20 · ceiling unchanged, denominator hardened** | 8 stands. One 2-line change made: choices with `targetType = "location"` are excluded from the count, so the gate measures decisions rather than navigation. A **no-op on every current game** (259/259 choices are `node` targets), taken so the gate cannot be tripped by a future game that authors exits as choices — `v2.py:13252` shows the engine supports them |
| **R7 · re-entry variation** | R6's lint should count the four observed mechanisms — condition clause, presence lines, choice-list movement, event replacement — not conditional openers. `the-surfaces.md` R6 rewritten accordingly; still a lint, still no threshold |
| **R2 · anchoring** | not gateable. Whether a choice hangs off a named object is a judgement a parser cannot make — same class as R1/R2 in `the-surfaces.md` |
| **R3 · cost-in-label** | **✅ GRADUATED 2026-08-14 as gate 21** (`a price is on its label`), into `the-voice.md` R1 and `the-economy.md`. Money only — the field is split on stamina costs, so gating those would invent a threshold. Fires on vesper 3/7. **This extends item 2** (interface text), which was already graduated; it closes nothing, since Tier 1 closed on 8-12. The plan that commissioned this study called the label rule "Tier 1 item 4" — that was wrong, item 4 is scene prose |
| **R4 · reason sits next to the want** | not gateable, and **`engine.md` §15 is untouched** — the study's first reading of it was wrong, corrected in §4 above |
| **R5 · guidance** | already gated (study 2's output). **Confirmed, not changed** |
| **R6 · world movement** | not gateable from source — it is a runtime property. Belongs with the R5/R6 lints |

**Nothing in this study has been applied to `gates.py` or the reference files yet.** Two of its six
outputs contradict shipped decisions (gate 20's denominator, `engine.md` §15), and this skill's own
standing rule is that a contradiction between a study and a shipped rule is surfaced, not silently
resolved.

---

## Appendix C · Play-study method and limits

- **Instrument.** `live.js` per turn, plus a per-turn probe reading visible `a`/`button` elements
  inside the passage container only. Sidebar chrome is excluded — it is identical on every screen,
  so counting it would put the same floor under every game.
- **Two instrument bugs were found and fixed mid-study, and both would have inverted a finding.**
  (1) A text-only link count read GPG's image-button hubs as one-choice screens. (2) `live.js`'s own
  `variables_diff` is rebaselined by the `eval` calls this study makes between turns, so it reported
  **0/59 turns with state movement** for a game whose arousal meter was visibly climbing. M4 is
  scored only over the 14 DoL turns after the fix, and in full for the other four games.
- **Session lengths are uneven** — 74, 61, 29, 17, 17. The two 17-turn sessions are enough for
  structure and guidance, **not** for M1 or for `shady_deals`' sink map. Marked untested above
  rather than reported thin.
- **Explicit scoring is per screen, not per beat.** It fires on config screens: DoL's body-settings
  page hit on "nipple". Screen-level heat % here is **not** comparable to `gates.py`'s beat-level
  floor — the same denominator caution as `REVIEW.md` O1.
- **One player, one route, one session each.** These are existence proofs and shape measurements,
  not coverage.

---

---

# Study 6 — The number becomes the spec

## 1 · What it is, and what breaks without it

Studies 1–5 produced numbers, and `gates.py` now checks nineteen of them. This study asks the
question none of the previous five asked:

> **When a rule states a reason in prose and a number in a check, which one does the author build to?**

It matters because the skill almost always has both. `the-surfaces.md:23` states the causal rule for
how many things a room offers — **"as many as the room has things to do"** — and then R3 states the
number, *caps at 8*. Only the number is checked. The prompting question came from LO, on reading a
game that passes gate 20 on every screen and still reads as a wall of menus: *"there should be a
genuine reasoning on how it should be decided, not just numberify it."*

The failure this exists to name: **a spec that can be satisfied by generating N of something is a
quota, and an author under a green-board incentive will generate N of something.** The count stops
being a consequence of the design and becomes an input to it.

## 2 · Where the skill already has the reasoning

This is not a case of missing doctrine. In every instance below the causal rule is written down,
often in the same file, sometimes in the same sentence:

| the number | the reason, already written |
|---|---|
| R3 · *caps at 8 choices* | `the-surfaces.md:23` — *"as many as the room has things to do"*; R2b — *"write the room's paragraph first, naming what is in it, then attach each choice to the thing that affords it"* |
| *6–8 locations* | `the-release.md:128` — *"Treat the count as a judgement, the distribution as evidence"* |
| *mean ≥4,500 · median ≥3,000* | `the-board.md:20` — *"Budget them as a shape, not a flat quota"* |
| *3 ascent tiers* | `the-want.md:45` — *"several parallel ascents, so a player who doesn't want one can climb another"* |

The reasoning is present, correct, and load-bearing. **It is also, in every case, the half that is
not checked.**

## 3 · The measurement — three games converged on the numbers, not on their worlds

Three v2 games, authored in separate sessions, on different premises — a family home, a bathhouse,
a truckstop:

```
                        back_home    steam    forty_miles     what the skill says
locations                     8         8          8          "6-8" (explicitly a judgement)
ascent tiers                  3         3          3          ASCENT_TIERS = 3
NPCs                          4         6          6          —
quest cards                   0        24         24          —
total location words     36,035    36,019     37,450          example arithmetic: "a 36,000-word target"
mean words per location   4,504     4,502      4,681          floor 4,500
```

**Two of the three landed within four words of the mean floor.** All three chose the top of the
"6–8" range — the range the skill had already flagged, in prose, as not evidence-based. And the
36,000-word total is not a spec anywhere: it appears once, at `the-board.md:79`, as illustrative
arithmetic — *"At a 36,000-word target the anchor owes 9,000"*. Three games shipped to the example.

### The asymmetry that explains it

Scoring `forty_miles` against every threshold, split by direction:

```
                          direction   threshold   game      margin
explicit beat %             floor          7.5    14.8      +97%
explicit in repeatable %    floor           50    97.1      +94%
locations with heat %       floor           60     100      +67%
location median words       floor        3,000   4,081      +36%
anchor share %              floor           25      28      +12%
location mean words         floor        4,500   4,681       +4%
sinks : sources             floor          1.0     1.0        0%
─────────────────────────────────────────────────────────────────
menu size                  CEILING           8       8        0%    (19 of 30 screens AT the cap)
sentence median words      CEILING          14      14        0%
```

**Six of the seven floors are cleared with room. Both ceilings are hit exactly.**
(The seventh, `sinks : sources`, lands on its floor at 1.0 — an integer ratio with little room to
land anywhere else, but the sentence should not claim more than the table shows.)

The mechanism is simple and worth stating in one line: **a ceiling makes "pass" and "maximise" point
the same way.** A floor makes them point in opposite directions, so an author who wants a green
board has to overshoot it and stop. An author facing a ceiling has to approach it and stop — and
nothing tells them where to stop short of it, because the only feedback the check gives is a PASS
that arrives at the boundary.

### The consequence, measured

`gate 20` was written to fix Steam's 23-choice front desk. Against the game it was written for:

```
                            steam        forty_miles
repeatable located screens     22             29
TOTAL choices on them         214            213      unchanged
choices per screen      median  7      median  8      went UP
                           max 23         max  8
open on day one          107 (50%)      147 (69%)     got worse
```

**The same number of menu items, redistributed.** The cap removed the outliers and pulled the median
up to itself. Meanwhile R2b — the causal half, unchecked — drifted to **41% of hub choices anchored
to a named object.** The checked half was satisfied perfectly and the unchecked half decayed, in the
same game, on the same screens.

## 4 · What follows

**R1 · A spec that can be satisfied by generating N things is a quota, and will be.** Before writing
a number into a reference file, ask: *can an author satisfy this without consulting their own
design?* If yes, the number is doing the deciding.

**R2 · State the derivation, then the number as a consequence.** The shape that works is already in
the skill — `the-surfaces.md:23` and R2b. A room's choice count is not chosen; it *falls out of*
writing the room's paragraph and hanging every choice on something named in it. A sparse room ends up
small and a rich one ends up larger, and neither number is a target. The number's only job is to
catch the pathological case.

> ⚠️ **Say it as many-to-one, and check that you did.** The first draft of this rule — and of three
> reference files written from it — said *"one choice per thing that affords one"*, which is a quota
> wearing a derivation's clothes: it pushes an author to invent an object to justify a choice, or to
> cap a rich object at one. It also contradicted the worked example three lines above it in
> `the-surfaces.md`, where a bed affords two choices and a wardrobe two more. **The only hard
> direction is that no choice may hang on nothing.** Caught on re-reading, one day after shipping.

**R3 · A prose caveat does not survive contact with a number.** `the-release.md:128` says in as many
words that the location count is a judgement and not evidence. Three of three games took the top of
the range anyway. If a number should not be built to, it cannot be stated as a bare range beside
numbers that should.

**R4 · Never put illustrative arithmetic in the same file as a threshold.** The 36,000 at
`the-board.md:79` exists only to demonstrate that the anchor ratio must be budgeted forward. It was
read as the size of a game.

**R5 · Where a ceiling is unavoidable, the check must report the distribution, not the verdict.**
"0 screens over 8" and "19 of 30 screens at exactly 8" are the same PASS and completely different
games. The scoreboard currently cannot tell them apart — which is why `steam` at 18/18 and
`forty_miles` at 20/20 both read as solved while sharing the defect.

**R6 · Iterate the GAME and look the declaration up. Never iterate the declaration.**

Measured across all 23 gates, and it partitions them cleanly:

```
walks the game, looks the declaration up   ->  the declaration can only make it STRICTER
walks the declaration                      ->  declaring LESS shrinks the obligation
```

`residents have homes` walks the game's six NPCs: declare no homes at all and it fails 0/6.
`guidance exists` walked `board.characters`: truncate the declared cast to one and it reported
*"24 quest cards for 3 ascent tiers and 1 characters"* — and passed. `ascent tiers expand the world`
was worse than gameable, it was **narrowed by declaring**: with nothing declared it guesses the
top-gated traits, so naming only your healthy tiers hid a descent-shaped meter from the gate whose
entire job is to catch one. `declared objects are real` had the same hole — one safe object per
room, game byte-identical, scored 20/21 green.

The tell is grammatical: `for x in declared` is the bug, `for x in game` is the fix. Where the
declaration genuinely holds information the game cannot (a *price*, a *home*, a *budget*), walk the
game's entities and demand the declaration cover each one.

**R7 · A presence gate cannot see that the important one is missing.**

Four gates ask *does at least one exist* — and **both blockers in the most-audited game in this
repo hid in exactly that class**:

- `money gates something` passed on nine *other* canvases while the declared £245 weekly obligation
  charged nothing at all. The game's whole outflow was 11 optional purchases, largest £35.
- `repeatable explicit media cycles` and `traversal heat` both report **100%** on 68 declared pools
  with **zero files on disk**. No gate in the file touches the filesystem.

A presence gate is fine for *"the guidance page is not empty."* It is worthless for anything the
game is actually built on. When something matters, name it in the board and check **that** thing —
which is what gate 24 now does for the obligation.

## 5 · The check — SHIPPED 2026-08-15

Reporting changes alone turned out not to be enough: the reason R2b drifted is that nothing checked
it, and no amount of better *printing* fixes that. So this shipped as one new gate, one rewritten
gate, and the reporting change:

| | |
|---|---|
| **Gate 22 · declared objects are real** ⚠️ **DELETED 2026-08-18 — see the note at the head of this file** | declare-then-check against `board.locations[].objects`: every declared object is written into the room's prose AND affords a choice; a room with screens must declare objects (or the denominator is author-controlled); a declared id must be a real location. Scoped to location-only hubs — on an NPC hub the anchor is the person. **This is the half of R2b a parser can judge.** |
| **Lint · choices hang off the room** ⚠️ **DELETED 2026-08-18 with gate 22** | the share of room choices naming something their own screen's prose said. **Built as part of the gate and demoted within the week** — see below. |
| **Gate 1 · location fill** *(rewritten)* | judges each location against its **own** declared `fill`; the global mean/median/anchor constants demote to a backstop used only when no ledger exists, and the headline says which ran. |
| **Gate 20 · menu size** | prints `median · N of M screens at the cap`, and warns when the majority sit on it. A game at median 3 and a game at median 8 no longer print the same line. |
| **Gate 19 · sentence length** | prints its margin and the field median. |
| **Floor gates** | unchanged — they keep printing a verdict. The asymmetry in §3 is the whole reason the two are treated differently. |

### Why the anchoring half is a LINT — the third rule in this file to be demoted

It was shipped as part of the gate and taken back out two days later, on the same evidence that
demoted R5 and R6. Run the strict word-match against **the worked example printed at the top of
`the-surfaces.md`** — measured from a shipped game, and used to teach what *correct* looks like:

```
Your clothes are kept in the creaky wardrobe.
   Wardrobe   -> matches
   Mirror     -> FAILS. "mirror" is not in that paragraph.
```

The mirror belongs to the cluster the sentence sets up; a reader sees it, a matcher cannot. **One in
four of the canonical example's real decisions fails.** On a real game the ceiling is ~74% even
matching against the whole room's prose, against 55% for the strict per-screen rule.

A gate demanding zero failures could therefore never be cleared — and this project has twice
recorded what happens next: *"a gate whose number is invented fails correct work and gets ignored."*
No number was invented here; a **zero** was, which is worse, because it looks rigorous. The
percentage is genuinely useful and is now reported as one, with the worst screens ranked.

**Generalises past this case:** *check the halves separately.* A rule usually has a part a parser can
decide (did you write the thing you declared) and a part only a reader can (does this sentence make
that choice feel like it belongs). Gating both together makes the gate unreachable; gating neither
makes the rule rot. Split them.

### What building it found — a budget that cannot be wrong is not a budget

Gate 1's declared-vs-delivered check passed **8/8 on all three games immediately**, which was the
tell. Every declared figure is an exact post-hoc word count:

```
back_home    9,607 · 4,936 · 3,514 · 1,963 · 3,927 · 4,746 · 4,381 · 2,961
steam       10,413 · 4,345 · 3,565 · 4,167 · 4,614 · 2,649 · 3,316 · 2,950
forty_miles 10,295 · 5,086 · 4,191 · 3,902 · 4,081 · 3,540 · 3,395 · 2,960

round to the nearest 100:  0 of 24
```

Nobody plans a room at 9,607 words. `board.locations[].fill` was being written **from the delivered
prose**, so the declaration recorded the outcome instead of constraining it — declare-then-check
degenerating into check-nothing. **A declaration only works if it can be wrong.** Gate 1 now detects
a mostly-non-round budget, refuses to credit it, and falls back to the backstop; the doctrine asks
for round numbers written at board phase, before the prose.

This is the same defect as the study's headline, one level up: the *form* of the good pattern was
present and the *substance* was not, because nothing checked the difference.

### Result

```
forty_miles   20/20  ->  19/21     (fill: post-hoc budget · gate 22: declaration incomplete)
steam         17/19  ->  16/19     (fill)
back_home     13/18  ->  12/18     (fill)
```

Gate 22 **discriminates rather than merely firing** — `hub_stock_room` flags 2 floating choices,
`hub_stock_room_dawn` flags 5, matching the by-hand measurement in `games/forty_miles/REVIEW.md`,
and every flagged line is a genuinely unanchored noun (*the hasp, the wastage sheet, the first
Tuesday*). A check that fails everything would have been as useless as one that passes everything.

**Deliberately not gated:** none of R1–R4 is mechanically decidable. Whether a choice count *fell
out of* a room or was *filled to* a number is not visible in the TOML — the same eight choices are
produced either way. This is the same honest state as R2b, and for the same reason: the check can
see the artifact, never the process that made it.

## Appendix D · Method and limits

Thresholds enumerated from `scripts/gates.py:55-119`; measured values from `gates.py <slug>` on all
three v2 games; menu shape parsed from each `7_final_game.toml` with a real TOML parser.

**Two limits, both real:**

1. **The three games share an author in the sense that matters.** Different sessions, but the same
   model reading the same skill. This measures *how this skill is read*, which is the question — but
   it is not evidence about authors in general.
2. **Convergence is not proof of causation.** Eight locations and 36,000 words may be independently
   reasonable for a v0.1. What moves it past coincidence is the *margin* pattern in §3: the same
   games that clear floors by 12–97% sit on both ceilings at exactly 0%, and 19 of 30 screens land
   on the cap rather than distributing around it.

# Study 7 — Who the player is

> **✅ APPLIED 2026-08-27, in the order the study argued for.** §4 and §5 shipped only *after* one
> real game was built to the doctrine (`mrs_vance`, commit `f34dc3b`) — which is the whole point, and
> the difference between this and the P0 refusal on the same day.
>
> - **§4 → `templates/want.md` §1 and `references/the-want.md` §1**, plus `want.player` in
>   `references/state.md`. The protagonist is now a declaration, not a pronoun.
> - **§5 → gate `the start choice is read`.** Built, and deliberately weaker than first drafted:
>   **it fails only on zero.** See §5 for why the floor was refused.
> - **Scoped, not rewritten:** `SKILL.md:92`, `the-release.md:81` and `the-want.md` §3 said *"For a
>   female protagonist"* as a given; each now points at the declaration. **The measured guidance
>   under them is unchanged** — the female default is evidenced, and de-gendering the prose would
>   have destroyed a finding to launder an assumption.

## 1 · What it is, and what breaks without it

`games/mrs_vance/REVIEW.md` **G1** — eight v2 games, one Want shape. Their appetite lines:

```
back_home      "To be wanted — not looked after, not tolerated, not managed..."
forty_miles    "To be wanted by men who have nowhere else to be at 3am"
off_season     "To be wanted -- not needed, not thanked, not worried about..."
seventh_day    "To be wanted by the men whose entire authority over her is telling her no"
the_allowance  "To be wanted by the people who set her price"
the_season     "To be wanted by men she shares a wall with"
mrs_vance      "To be wanted by men who have to call her by a title she did not earn"
steam          "To be necessary to people at the moment they have nothing on"
```

G1 read that as a **premise** problem and proposed a repo dedup step. **Measured, it is not a
premise problem, and the dedup step is dropped** — §3 of the correction in `REVIEW.md` N13.

Six axes are locked across all eight, and the skill fixes four of them:

| axis | across the eight | fixed by v2? |
|---|---|---|
| protagonist | woman, 19–39 | **yes — by pronoun, see §3** |
| `narration_person` | `second`, 8/8 | **yes** — `templates/want.md` §7 pre-fills it |
| the trap | money she cannot reach | no |
| appetite verb | "to be wanted" ×7 | the *shape* is mandated by `the-want.md` §2 |
| ascent sentence | *"Bottom: she asks / knocks / waits… Top: she is…"* | **yes** — §3, "a sentence about doors" |
| charge | reversal and/or taboo ×7; transformation primary in **one** (`steam`) | §4 offers three; the corpus of eight uses two |

⚠️ **LO's own call, recorded, because it decides what this study is for:** asked whether the shape
was deliberate, he answered **"Just happened."** So this is drift, not house style, and the question
is what produced it.

**Vesper is the control.** It predates the Want file, and it has none of the shape:
`narration_person = "third"`, a company-owned protagonist, a dock district, no rent and no debt
(`games/vesper/design_book.md`, "World setup"). Games authored **before** the Want file do not
converge; the eight authored **through** it do.

## 2 · How v1 teaches it

v1 asks the question outright, as the first gate of its whole pipeline —
`author-game/references/step-0-1-seed.md:17`:

> **(1) Pick the PROTAGONIST POV first — it decides which fantasies even work.**
> - **Female PC** → self-corruption / rise-via-seduction / becoming-the-one-in-power (madam,
>   queen). This is **cascade-native** … **Default here.**
> - **Male PC** → acquisition / power / harem. A male-PC harem fantasy on a female PC (or
>   vice-versa) is *wrong-shaped*, not just weak.

And it carries the second axis explicitly — `author-game/references/customization.md:213`:

> **Player** — name + build + look, when the protagonist is a blank-ish self-insert (**the RTS
> default**). **Don't** sweep `@player` across a written, named protagonist whose prose leans on
> third-person narration by name…

So v1 names both forks this study measures: **which gender**, and **blank-slate vs written**.

## 3 · Where v1 is wrong

⚠️ **It is not wrong here. It is thin and unmeasured, and that distinction is the finding** — the
template for these studies invites a v1 defect and there is not one to report. Manufacturing one to
fill the section would be the naivety this file exists to avoid.

What v1 actually lacks: it *names* the female/male fork and gives **no rule for choosing**, beyond
"Default here." Its split is asserted from craft intuition, never measured against the field. The
blank-vs-written line lives in a **customization** file — filed as a plumbing concern, not as a
design decision — so an author who never opens optional systems never meets it.

**v2's error was different and larger: it deleted a thin question instead of measuring it.**

| evidence | figure |
|---|---|
| `templates/want.md` — `she/her/hers` vs `he/him/his` | **21 vs 0** |
| `references/the-want.md` — same count | **16 vs 0** |
| whole v2 skill — `male pc` · `blank.slate` · `self.insert` · `character creation` · `protagonist gender` | **0 hits** |
| `the-want.md:34` · `SKILL.md:92` · `the-release.md:81` | *"For a female protagonist"* — stated as a **given**, never a fork |
| `templates/want.md` §1 heading | **"Who she is"** — a finished person, not a set of choices |

**The template decides before the author arrives.** Nobody chose a woman eight times; the grammar
of the page chose, twenty-one times per fill. That is the mechanism behind LO's "just happened", and
it is why a dedup check could never have caught it — a dedup check compares outputs, and this is
upstream of the output.

### What the field actually rewards

Corpus: the 30-game mopoga study of 2026-07-24, re-interrogated 2026-08-27. Its own ten findings
are all mechanism — lostness, grind, cheats, escalation, beat economy, parameterization, media
identity, onboarding, consequence, cadence — and none of them uses the `protagonist` or `premise`
fields. Scripts and the full method:
`~/Documents/Mopoga_Twine_Sandbox_Research_20260724/premise_study_20260827/`.

⚠️ **A prior study covered part of this, and it is a better instrument on one axis.** The **Female PC Craft Study of 2026-08-23** (`~/Documents/Female_PC_Craft_Study_20260823/`, eleven findings files, linked from `STATUS.md:186`) settled the gender question by **reading each game's opening** — following `<tw-storydata startnode>` into the first passages — which beats classifying a note field, and it says so of its own probe: it *"was wrong twice"*. **Its verdicts are adopted here and they moved a number:** `new-life-project` is *"Character creation — Gender assigned at birth: **Girl | Guy**"*, so it is selectable, not a fixed female PC. Its `findings_A_want.md` also already carries the mechanism this study's §4 proposes, under a better name — **"character creation is a memory, not a slider"** (Course of Temptation asks what kind of teenager she was and initialises thirteen skills the player never sees). And its `findings_J_players.md` §0.1 already documented the 500-comment cap. **What is additive here is the other half**: what carries a game across all thirty (that study read four in depth), the pronoun mechanism inside our own template, the field-wide comment counts, and the correction to G1.

**Reason (1) of each game's `why_players_love_it`, weighted by mopoga comment count:**

```
freedom      4 games  25.9%      story        5 games   7.3%
performers   6 games  22.0%      characters   3 games   7.0%
systems      5 games  15.8%      cadence      2 games   5.4%
volume       4 games  15.6%      kink         1 game    0.8%

premise      0 games   0.0%
```

**Not one game in thirty is loved for its premise.** The #1 game's #1 reason is
*"farmer, slave merchant, bounty hunter, cage fighter, Cannibal? You can be whatever you want."*

**The three axes, ours against the field:**

```
                  field                                        our 8
gender      male 20 · pick 6 · female 4                        female, 8/8
player is   the body 19 · the camera 10                        the body, 8/8
who she is  blank slate 19 · written 10   (blank = 80.4%)      fully written, 8/8
```

Games matching **all three** of our choices: **3 of 30** — `zaras-school-life` #21, `family-ties`
#23, `cupids-way` #27 — **3.1% of the top-30's engagement.** (`cupids-way` is note-derived; the 8-23
study never adjudicated it. `new-life-project` was in this list until its verdict was adopted.)

**⚠️ The gender axis is NOT the finding, and must not be read as one.** Across all 22,622 comments:
**49 asking for a female lead (364 likes) against 11 opposed (124 likes)**, and the opposed get
piled on by other players. One comment does the arithmetic — *"There are 44 games with the Female
Protagonist tag and 100 with the Male Protagonist tag"* — and another gives a mechanical argument
for it at 14 likes: *"as a guy I like to play female mc since we can get to the spicy part quicker
and not grind around like in male mc games."* Real-porn media makes the same case. **The female lead
is supported by the evidence. The axis we are furthest from the field on is `freedom`.**

**And the risk G1 sensed is real, one level up from where it looked.** GrowUp RP, 34 likes:

> *"It is literally the same game as all the other games. Young guy step family and school. You may
> or may not have magic but it doesn't matter."*

Players do name a repeated package, and they name it at exactly the grain ours shares —
*young woman, money problem, small town.* Not the premise. The **recognisable whole**.

### ⚠️ Convergence, not discovery

The 2026-06-17 non-linear-RPG research already named **"no PLAYER-IDENTITY axis"** as its single
critical gap — *"Every player walks one monotonic corruption spine to the same destination. No
dom/sub, no willing/coerced, no pure-vs-corrupt route"* — and closed *"analysis only, nothing
changed… awaiting his call on scope."* That was v1, from theory. This is v2, from field measurement,
arriving at the same place by a different road. **It is the second time this gap has been written
down. Recording that so it is not derived a third time.**

## 4 · What v2 says instead — ✅ APPLIED 2026-08-27

**P1 · The Want asks who the player is, before it describes her.** `templates/want.md` §1 becomes a
fork, not a portrait. The pronoun comes out of the template's own prose so the page stops answering
its first question by grammar.

**P2 · Declare the blank-vs-written position, and pick it on purpose.** The field runs 19 blank to
10 written. Ours are 8/8 written with no record that it was ever a choice. Both are legitimate; an
undeclared default is not.

**P3 · One real choice at the start, and it changes reach.** *Freedom* is the field's largest
bucket, and reach is already the shape `the-want.md` §3 uses for the ascent — *"a sentence about
doors."* The proposal is that a slice of that ascent is **player-selected at minute zero** rather
than wholly authored: what she was before, and therefore what she can do that another playthrough
cannot.

⚠️ **The failure mode is fake freedom, and it is the field's own #1 disease.** Study 5 and F1/F3 of
the 7-24 report both land on it: numeric gates with no content behind them generate nothing but
cheat-code demand. **A creation screen whose answers nothing reads is worse than no screen** — it
promises reach and delivers a label. Hence §5.

**P4 · Do not change the gender.** Recorded as doctrine, with the count, so it is not relitigated by
a later reader who sees `female 4 of 30` and draws the obvious wrong conclusion. It is a **supply**
figure, and the 8-23 study reached the same verdict independently: *"the genre's top ranks are mostly
male-PC games where women are the content."*

## 5 · The check — ✅ BUILT 2026-08-27, and weaker than it was drafted

Candidate gate: **a start-of-game choice does not ship unless real content reads it.** Every flag or
trait written by the opening fork must be read by at least *k* gating sites elsewhere in the game,
counted the way the flag-chain validator already counts a located setter
(`apps/projects/services/template_import.py`). Mechanically decidable from `7_final_game.toml`
alone; no judgement call.

✅ **BUILT — as gate `the start choice is read`, after `mrs_vance` gave it something to run
against.** And it ships **weaker than the sentence above**, which is the honest outcome rather than
the tidy one:

> **It fails only on ZERO.** Undeclared → `n/a` (*not* a pass). Declared and read zero times → FAIL.
> Anything else → PASS, **printing the count without judging it.**

⚠️ **The `k` in "at least *k* gating sites" was refused, and the reason is n = 1.** One game cannot
support a floor. This skill has already had to supersede an entire meter doctrine derived that way
(`the-meters.md` W1, 2026-08-19, *"three layers, three or four ratcheting tiers was n = 1"*).
Declared-and-never-read needs no threshold — it is the defect by definition — so that is all the gate
asserts. The counts accumulate in the headline until a real distribution exists to read a floor off.

Measured on the day it shipped: `mrs_vance` 3 flags × 5 reads → PASS. The other seven v2 games → `n/a`.
The FAIL branch was exercised on purpose, with a fourth flag nothing reads, rather than assumed —
this project has twice shipped a gate whose first real contact was with correct work.

⚠️ **Not built here, and the reason is on this file's own record.** Study 2's R4 proposed a gate
requiring `locked_text` on every locked door; built, it fired on 7 of 8 doors in a real game because
`engine.md` §15 rules the other way deliberately. **A check that fails a game for obeying the
doctrine is a bug in the check.**

⚠️ **That precedent took a second scalp the same day this study was written, from a different
study, and the pattern now has a name.** The Female PC Craft Study's **P0** — count a `block_pool`
as one variant for word count, to ship *"first, alone"* — was measured on 2026-08-27 and **refused**:
it would have scored `mrs_vance` **4 of 14 locations on budget instead of 14 of 14**, because `fill`
is a budget for prose *written* (`the-board.md:92`) and pooled variants are written. It was
specified when **no v2 game used a pool**, so there was nothing to run it against. The full record is
on `Beat` in `scripts/gates.py`.

> **A rule specified before its doctrine has a real game to run against will fail correct work.**
> Three times now — study 2's R4 (built, withdrawn), study 6's anchoring check (built, demoted to a
> lint), and P0 (specified, refused before building). The cheapest of the three is the one that was
> never built, and the difference was having a game that used the feature.

This is why §4 above is a proposal and this section builds nothing. **Step 2 — retrofit one opening
in `mrs_vance` — is not optional throat-clearing before the gate; it is the thing that makes the
gate safe to write.** This gate cannot be written before the doctrine it enforces exists
(§4 is a proposal), and it must be run against a real build before it is trusted — which is Step 2:
retrofit one opening in `mrs_vance` and see whether the choices can be made to change anything at
all. If they cannot, §4 is hollow and this study's conclusion is wrong, and we learn that for the
price of one scene rather than eight games.

**What is NOT checkable:** whether the choice is *interesting*. A fork between two equally dead
starting skills passes every count. That half stays a reader's job, and this file's standing rule
applies — check the halves separately, and say which is which.

## Limits

1. **No top-30 game shows a Want on screen.** Extracting each `startnode` from `tw-storydata`
   returns title cards, version numbers, age disclaimers and Patreon links; only
   `wasteland-lewdness` puts a premise line on its splash. **So nothing here grades the Want file's
   format** — there is no field equivalent to compare against. What is graded is what the field
   *chooses*, not how it writes it down.
2. **No developer in the top 30 has two entries**, so "does repeating yourself cost a developer" is
   untestable from this corpus. The 34-like GrowUp comment is about the *field* repeating, not one
   author.
3. **Nothing here attributes an outcome to sameness.** The complaint exists and is liked. That is
   not the same as it having cost anyone a player.
4. **The three axes and the reason-(1) buckets are hand-classified** (`axes.py`, `loved.py`), because
   a regex mis-sorts the mutable rows — and those are the rows the question turns on.
5. ⚠️ **`comments/*.json` caps at 500 replies per game.** The first version of the axis table was
   computed over those counts, returned identical medians on all three axes, and was **thrown away.**
   Engagement is from `report.md`'s ranked list only. Recorded because it is this study's own
   instance of the measurement trap Appendix B and Appendix C both warn about.
6. **Our own players: n = 2 reviews.** Not a sample, and not evidence for anything here.

---

# Study 8 — What she owns

> **✅ APPLIED 2026-08-28.** §4 → `the-economy.md` **R1b** and **R1c**, `the-surfaces.md` **R6**'s
> pool note, and a scope on `the-want.md`'s ADDITIVE-ONLY rule. §5 → gate
> **`what money buys opens a door`**, which fails only on zero, and lint
> **`what a paid repeatable leaves behind`**, which prints a rate.
>
> ⚠️ **This is an ADOPTION, not a discovery.** The 2026-07-24 field report already ranked this
> critique of us at **#3, #4 and #6 of eight**, thirty-five days before it was measured, and it was
> never carried into this file's inventory. What is new here is the mechanism and the arithmetic.

## 1 · What it is, and what breaks without it

Study 7 closed the minute-zero slice of `freedom` — the field's largest bucket at **25.9%** of top-30
engagement, against `premise` at **0 of 30**. But the four games in that bucket are not loved for
their opening question:

```
apocalyptic-world   "you can be whoever you want"
become-someone      career/path variety and open-world freedom
new-life-project    zero-to-hero money/career fantasy
the-company         choice-consequence ownership
```

**All four are ongoing.** A start choice is ten seconds of a thing the field runs for forty updates.

Without this, our games are what the 7-24 report called them: *"NPC arcs and quests on a map"* where
*"nothing visibly compounds — money is rent-pressure, not a snowball; no owned asset grows."*

## 2 · How v1 teaches it

**It does not, and neither did v2.** A grep of the whole v2 skill before this study:

```
"meta-loop"     0 hits        "snowball"       0 hits
"owned asset"   0 hits        "closes a door"  0 hits
"irreversible"  0 hits        "locks you"      0 hits
```

`the-surfaces.md` **R4** said *"Money is not a scene. A purchase is not a rung"* — correct about
placement, silent about whether the purchase survives the transaction. `the-economy.md` **R1** was
satisfied by a price on a cup of coffee.

## 3 · Where v1 is wrong

**No finding.** v1's economy material is thin and this ground is not in it. Inventing a v1 defect to
fill the section is the failure this file exists to avoid, and §3 has been left empty once before
(Study 7) for the same reason.

## 4 · What v2 says instead — ✅ APPLIED 2026-08-28

Measured over 25 corpus games / ~55,000 passages, structurally and then hand-read
(`~/Documents/Accumulation_Study_20260828/`).

**Nine corpus games sell the player a THING, and all four of the most-engaged sandboxes do.**

| game | rank | owned | price | condition sites gated |
|---|---|---|---|---|
| become-someone | 4 | a company, `$startup.level` 1→4 | 20k / 50k / 100k | **114** |
| become-taxi-driver | 12 | `$car.body` 0→3 | shop | **46** |
| destroyer | 2 | five room levels | 30k / 60k | 21 · 20 · 16 · 16 · 16 |
| corpo-life | 9 | `$home` tier | four tiers | 79 |
| apocalyptic-world | 1 | a church 0→5 | 50 wood + 80 energy + 8h per stage | 8 |

**The discriminator is structural, and it is the whole reason this is checkable:**

```
owned thing   FEW write sites, MANY read sites
meter         many write sites, many read sites
```

**One asset closes three of the 7-24 report's eight critiques of us.** `become-someone`'s company is
an accumulation (#3), it is what the work deposits into (#4), and missing its weekly payroll calls
`<<Bankruptcy>>` and takes it away, recoverable for $500 (#6). Three problems, one object.

**The mechanism costs no new surfaces**, which is the only reason it is affordable here.
`destroyer`, rank 2: `<<if $sisbedroomlevel is 1>> _sceneOptions to [1,2,3] <<elseif gt 1>>
[3,4,5,6,7,8,9]`. **Buying the room takes its random pool from three to seven** — same room, same
link, no branch. Scene 3 is in both pools, so nothing is taken away. Authorable here today: a
`[group]` with `conditions` wrapping a `block_pool` is live in `mrs_vance` at `loop_cade.finish`
(5 instances), and consecutive groups become one chain at `v2.py:14634-14640`.

⚠️ **The expensive version of `freedom` is what we must NOT build**, and the corpus says so itself:
**College Daze** — 2,248 engagement, researched then excluded — *"branch explosion collapsed its
cadence"*, ~1 year stale. *"The freedom players loved is what a sandbox delivers via reusable
state-gated systems instead."*

⚠️ **A contradiction inside our own file, found and scoped rather than deleted.** `the-want.md`
said ADDITIVE ONLY — *no door closes*. Correct for retrofitting into live saves; read as design law
it inverts the field. `the-company`'s most-liked reason for love is choice-consequence ownership
(*"it only does that if you allow it to"*, 39 likes) on a hard route-lock, and its most avoidable
complaint is that the lock is silent. **The rule is close them out loud** — `become-taxi-driver`'s
five-term gate names every unmet term with directions.

## 5 · The check — ✅ BUILT 2026-08-28, one gate and one lint

**Gate `what money buys opens a door`.** A flag set by a choice costing the currency, surviving the
night, read zero times → **FAIL**. Sells nothing → `n/a`, *which is not a pass*. Otherwise PASS with
the door counts **printed, not judged** — one house with one asset is not a distribution, exactly the
restraint G44 ships with.

⚠️ **The FAIL branch was found in shipped work, not constructed.** `the_season` sells boots that fit
for **$20** (`has_boots`) and fuel for **$5** (`truck_fuelled`) and reads neither flag anywhere. The
player pays and the game never mentions it again. Its scoreboard moves 39/41 → **39/42**, and that
red is correct.

⚠️ **Day caps are excluded, not failed.** A flag `[engine.daily_tick]` wipes overnight is a day cap,
and `off_season` legitimately prices four of them in coins. Same carve-out `_holder_day_capped`
makes for gate 18.

**Lint `what a paid repeatable leaves behind`.** The 7-24 report's critique #4 said *"every
repeatable should deposit into something"*; shipping that sentence would have failed correct work,
because counting every repeatable surface (67% granting nothing) sweeps in ambient prose that is
supposed to grant nothing. Narrowed to choices the player pays for: **51.7% across the eight**,
`forty_miles` at 10 of 10, `mrs_vance` at 1 of 47. **A pure sink is not a defect; a game made only of
pure sinks is.** Never a gate — the spread is 0% to 98% and any threshold between is invented. Fourth
time this file has printed a distribution instead (after R4 withdrawn, study 6's anchoring check
demoted, and P0 refused).

**Not built, deliberately:** any check on the pool-widening pattern. No v2 game gates a pool on an
owned thing, and *a rule specified before its doctrine has a real game to run against will fail
correct work* — the lesson §5 of Study 7 states in those words.

**Also not built:** a `board.holdings` ledger field. The gate reads the asset out of the TOML and
needs nothing declared; adding a field with no use would have produced eight new "not declared"
reports and told no one anything.

## Limits

1. **A per-NPC act flag and a possession are structurally identical** — monotonic, bought with time,
   gating content. `zaras-school-life`'s `$dad.blowjob` (57 reads) and `inseminator`'s
   `$girl.analXp` (12) pass every automatic filter. The table in §4 is hand-separated and a
   different reader would move rows.
2. **`doors` counts condition sites, not content.** One `<<if>>` guarding a hub and one guarding a
   sentence count the same.
3. **Five corpus games have no extracted passages**, so their zeroes are partly instrument.
4. **Prices are not normalised against income.** $100,000 and $2,600 are not compared.
5. **No player of ours has seen an owned asset.** The truck shipped 2026-08-27 and no build carrying
   it has reached anyone. Every claim about how it plays is a claim about code.
6. **Two probes over-collected before the third worked**, and both are kept in the study directory
   rather than deleted: variables declared once in `StoryInit` look exactly like possessions, and
   passages that spend the clock while a story counter ticks look exactly like shops.

---

## Log

| date | what |
|---|---|
| 2026-08-28 | **The release boundary — the first instrument in this skill that reads the ARTEFACT instead of the source.** `mrs_vance/REVIEW.md` B2. LO's rule (*dev mode and missing media block RELEASE, not testing*) was correct and held by **nothing**: it lived as a comment on a JS object literal (`games-data.js:44-49`), **hand-copied into nine of twenty-eight portal entries in three wordings**, while `gates.py` had **zero lines reading a built game** and `the-release.md` — 164 lines, named for this — never said `--dev`, `--debug` or *build*. Every one of the 43 gates measures `7_final_game.toml`, which cannot see an artefact. **The drift was already shipped:** parsing the flags-init map and `MissingMediaPage` out of all 29 builds, **`the_inheritance` is in the published grid as a full `--dev --debug` build with 115 missing files**, `the_long_summer` carries `--debug` with 122, `under_one_roof` ships **183 missing** silently, and `forty_miles` holds `dev: true` **and** `version: "0.1"` on one entry while its TOML prints `0.1.2` to the player and three archives exist. ⚠️ **B2's own fix was corrected rather than adopted** — the `[IMAGE MISSING]` / `[… POOL MISSING]` markers it specified are emitted **only under `--debug`** (`v2.py:12403`, `:14753`, `:14903`), so a clean build renders silent gaps and the grep passes it: the proposed instrument detects scaffolding, not missing media, and would have passed the 183. Read instead: the build's own flags-init map (`v2.py:1077`, `:1081-1082`) and `MissingMediaPage`, *"always generated, but button only shows in debug mode"* (`v2.py:216`). SHIPPED: `the-release.md` **§ Shipping the build** — six steps **lifted from the JS comment, not invented**, the three-places-that-say-what-shipped table, and the relationship the schema never declared (**`dev: true` and `version` are mutually exclusive**) — plus **`gates.py --release <slug>`**, six checks, off for every ordinary run, **exiting non-zero** where `words_mode` deliberately never does. ⚠️ **Two things NOT gated, each stopped by a measurement:** byte-equality against `releases/v<n>.html` (vesper's differ, and vesper is the only whole triangle — the fourth time this skill has printed instead of judged, after R4, study 6's anchoring check and P0), and any repo-wide sweep (nine legacy entries carry no `version`; failing all nine on day one is noise). ⚠️ **The media count is a build-time snapshot**, so a red is fixed by a REBUILD, never a file copy. **Baseline recorded as the number that has to come down: 0 of 29 builds clean**, best 5/6. Verified with every branch driven — the reds on real shipped work, the fixture-only branches (`dev`+`version` together, no build, no portal entry, no `games-data.js` → **n/a, not a pass**) on a fixture root — and **0 verdicts and 0 tallies moved across all 22 scorable games**; six games' two nondeterministic headline lines proved inherent by running the identical file twice. No game rebuilt or modified. |
| 2026-08-28 | **Study 8 — what she owns. The largest thing the field is loved for turned out to cost almost nothing to build, and we had adopted none of it.** `freedom` is 25.9% of top-30 engagement and Study 7 closed its first ten seconds; the four games in that bucket are loved for what runs all game. Measured over 25 corpus games / ~55,000 passages: **nine sell the player a THING and all four of the most-engaged sandboxes do** — `become-someone`'s company gates **114** condition sites, `become-taxi-driver`'s car **46**, `destroyer`'s five bedrooms 21/20/16/16/16. **The discriminator is structural** — an owned thing has FEW write sites and MANY read sites; a meter has many of both — which is what makes it checkable at all. ⚠️ **This is an ADOPTION, not a discovery:** the 2026-07-24 report ranked the same defect at #3, #4 and #6 of eight, thirty-five days earlier, and no inventory item was ever opened. **One asset closes three of them** — become-someone's company accumulates (#3), is what work deposits into (#4), and missing payroll calls `<<Bankruptcy>>` and takes it away, recoverable for $500 (#6). **The mechanism is free at our scale:** `destroyer` buys a bedroom and its random pool goes `[1,2,3]` → `[3,4,5,6,7,8,9]` — same room, same link, no branch, and scene 3 stays in both so nothing is removed; a `[group]` wrapping a `block_pool` is already live in `mrs_vance` (5 instances). ⚠️ **The expensive form is refused on the corpus's own evidence** — College Daze, 2,248 engagement, excluded for branch explosion. ⚠️ **A contradiction in our own file was scoped, not deleted:** `the-want.md`'s ADDITIVE ONLY is a save-safety rule; read as design law it inverts `the-company`, whose most-liked reason for love is a hard route-lock and whose most avoidable complaint is that the lock is silent. **Close doors out loud.** SHIPPED: `the-economy.md` R1b + R1c, `the-surfaces.md` R6's pool note, the-want.md scope, gate **`what money buys opens a door`** (fails only on zero; sells-nothing reports n/a, which is not a pass; day caps carved out as gate 18 does) and lint **`what a paid repeatable leaves behind`** (a RATE — 51.7% of our paid repeatables deposit nothing, `forty_miles` 10 of 10, and any threshold between that and mrs_vance's 98% is invented). ⚠️ **The FAIL branch was found in shipped work rather than constructed:** `the_season` sells boots that fit for **$20** and fuel for **$5** and reads neither flag anywhere — 39/41 → **39/42**, and that red is correct. ⚠️ **Nothing was built ahead of its doctrine:** no check on pool-widening (no v2 game does it) and no `board.holdings` field (the gate needs nothing declared). Verified: **one new row per game and no pre-existing verdict moved across all 12 scorable games**; `mrs_vance` 42/42 → **43/43**, 1 n/a. Scripts and method: `~/Documents/Accumulation_Study_20260828/`. |
| 2026-08-27 | **E1 answered, and the answer was not the number — `the-economy.md` gains R3b and R3c, plus two lints and no new gate.** `REVIEW.md` E1 asked whether Mrs. Vance's 260 rent should rise against a week earning four times it. A pass over 19 field games and our own ten (`~/Documents/Economy_Pressure_Study_20260827/`) said **no**. Measured: **seven of our ten rent-enabled games have ZERO conditions reading money** against a field median of 67.3 per 1,000 passages where every sandbox has some; **four price nothing in money at all**; **eight of ten clear the whole week's obligation in under one day** of the best job (median 0.48). ⚠️ **The rule that would have caught it was already in the file** — R3's *"price it against the income channels in both directions"*, warning emoji and all — and **nine of ten authors did not do it**; the one that did wrote the sum in a prose comment because the ledger had no field. *An instruction with no field is a wish.* **R3b** — an obligation that does not MOVE is soft at any value — carries the three field shapes and which collector each needs, and records that **nothing in `degrees-of-lewdity` is gated on `$rentstage`** (five uses, none content): a bare ratchet buys the player nothing and works only because it is delivered in a believed predator's mouth at the moment of payment. **R3c** — if the demand rises the income must rise with it, or the ratchet IS *"here u still grind for nothing"*, the corpus's four-word verdict on its angriest economy. ⚠️ **Both new checks are LINTS**: `forty_miles` runs 70% and `back_home` 25%, so any threshold between them fails a game for obeying the doctrine — the third time this skill has printed a distribution instead of inventing a floor at n≈10 (after R4 withdrawn and study 6's anchoring check demoted). ⚠️ **Built first, taught second**, as with Study 7: `mrs_vance` shipped the truck, its upkeep, the scaling haul and a live `cade_covered` before a word was written here. ⚠️ **No engine change, and the staged-rent feature was deliberately not built** — `[engine.daily_tick] traitEffects` already carries a condition gate and notifies, and a stage array would have made a `trait_bar max` and a quest goal lie. ⚠️ **One research claim withdrawn in the same pass**: `wasteland-lewdness`'s `$slaverent` is income, not an obligation. Verified: mrs_vance **42/42, 1 n/a**, money conditions **0 → 5**, `cade_covered` 2 → 10 hits; all 22 games re-scored with **no gate count changed anywhere**; the lint's declared / undeclared / no-obligation paths each exercised on a real game; live 14/14 in headless Chromium. |
| 2026-08-27 | **Study 7 APPLIED — the protagonist becomes a declaration, and item 14 closes.** Shipped only after `mrs_vance` built the thing first (`f34dc3b`), which is the deliberate opposite of P0's order on the same day. **§4 →** `templates/want.md` §1 and `the-want.md` §1 now ask *who is the player* **before** she is described, with `want.player` recorded in `state.md`; the drift cause is named in both (this file wrote `she/her` 21 times against `he/him` 0, so the grammar answered before the author arrived, and v1 had asked the question first of anything at `step-0-1-seed.md:17`). ⚠️ **THE FIX IS A DECLARATION, NOT A DE-GENDERING** — rewriting 21 pronouns would have destroyed a measured finding (*"for a female protagonist the ascent is reach, not accumulation"*) to launder an assumption, and the female default is **evidenced**: 49 corpus comments asking for a female lead against 11 opposed, with `female 4 of 30` a supply figure. Three lines that stated it as a given (`SKILL.md:92`, `the-release.md:81`, `the-want.md` §3) were **scoped**, not rewritten. **§5 →** gate **`the start choice is read`**, and it ships weaker than drafted: **it fails only on ZERO**, because a read-count floor cannot be defended at n = 1 — the exact error that cost this skill its meter doctrine (W1, 2026-08-19). Undeclared reports `n/a`, which is not a pass. ⚠️ **The FAIL branch was exercised, not assumed** (a fourth flag nothing reads → red, naming it); this project has twice shipped a gate whose first contact with reality was correct work. Verified: `mrs_vance` **42/42** with 3 flags × 5 reads, seven other v2 games `n/a`, and **0 pre-existing verdicts moved across all 22 scorable games**. |
| 2026-08-27 | **P0 measured and REFUSED — the third rule in this project taken out or turned down, and the first turned down before it was built.** The Female PC Craft Study's P0 (`~/Documents/Female_PC_Craft_Study_20260823/proposal_for_skill.md`) said `gates.py` must count a `block_pool` as one representative variant, to ship *"first, alone"*, because otherwise *"the scoreboard will punish authors for using it."* P1–P6 shipped 2026-08-24; P0 never did. It was specified when **no v2 game used a pool** — `mrs_vance` now ships **69 pools / 221 variants**, so it became testable. Scored three ways with `_collect` patched: `location fill` reads **12,509 words / 14-of-14 on budget** under both folding (today) and splitting, and **8,706 / 4-of-14 under P0**. ⚠️ **P0 would have failed ten locations of a game that did exactly what the doctrine asked** — `the-board.md:92` defines `fill` as *"its word budget — in round numbers, written now, before the prose"*, a plan for prose **written**, and pooled variants are written. The field-baselined gates barely move either (explicit floor 13.9→14.1%, sentence median 9→9, G43 19.2→19.2/10k) because they are rates. ⚠️ **And the one gate that looked like the real defect was an artifact of my own probe:** `an explicit beat carries a clip` swung 100% → 9% under splitting only because splitting orphaned each variant from the node's sibling media — counted against the source, **32 of 32 explicit pool variants sit under a shared-node clip and 0 render dry**, so the 100% is honest. **No change to word counting.** The refusal is recorded on `Beat`; gate 1 now *reports* `N pools, M words per pass` alongside the budget it judges, the same reporting-not-judging move gates 19/20 and G43 already make. Verified: **0 verdicts moved across all 22 scorable games**, exactly 2 headlines changed. ⚠️ **Found in passing and NOT fixed (out of scope):** `sinks >= sources` is **nondeterministic** — three runs on unchanged code and input named `harbour_end`, `the_lets` and `the_arcade`. Headline only; no verdict depends on it. |
| 2026-08-27 | **Study 7 (who the player is) written — the first study here whose subject is the skill's own grammar.** Item 14 opened. Prompted by `mrs_vance/REVIEW.md` G1 (eight v2 games, one Want shape) and by LO answering the prerequisite: the shape was **never chosen**. Re-interrogated the 30-game 7-24 corpus, whose own ten findings are all mechanism and never touch the `protagonist` or `premise` fields. ⚠️ **NOT virgin ground, and this was caught during verification, not before:** the **Female PC Craft Study of 2026-08-23** (`STATUS.md:186`) had already read the openings of the female-PC games. Its gender verdicts are **adopted** and moved a headline — `new-life-project` is selectable (*"Gender assigned at birth: Girl | Guy"*), so games matching all three of our choices are **3 of 30 / 3.1%**, not 4 / 5.2%; its `findings_A_want.md` already carries this study's §4 mechanism as **"character creation is a memory, not a slider"**; and its §0.1 already documented the 500-cap. Headline: **no game in the field is loved for its premise, 0 of 30**, so G1's proposed dedup step is **dropped**; the largest bucket is `freedom` at **25.9%**, and all eight v2 games let the player choose nothing. Cause is citable and upstream of any output check: `templates/want.md` writes `she/her` **21 times against `he/him` zero**, `the-want.md` 16 vs 0, and a grep of the whole skill for `male pc` / `blank.slate` / `self.insert` / `character creation` returns **0 hits** — v1 asked the question first of anything (`step-0-1-seed.md:17`) and v2 deleted it. ⚠️ **§3 reports no v1 defect**, because there is not one to report — v1 is thin and unmeasured here, and inventing one to fill the section is the failure this file exists to avoid. ⚠️ **The gender is not the finding**: 49 comments for a female lead against 11 opposed. ⚠️ **One measurement trap hit and thrown away** — `comments/*.json` caps at 500 per game, so the first axis table's medians were an artefact. ⚠️ **Converges with the 2026-06-17 research's *"no PLAYER-IDENTITY axis"***, so this is the second recording of the same gap. **§4 and §5 are `PROPOSAL — NOT APPLIED`**: no reference file, template or gate changed, and the candidate gate ("a start-of-game choice does not ship unless real content reads it") is explicitly **not built**, per this file's own Study 2 R4 precedent. Scripts and method: `~/Documents/Mopoga_Twine_Sandbox_Research_20260724/premise_study_20260827/`. |
| 2026-08-16 | **Whole-skill audit — the declaration hole was a CLASS.** Reviewed all 23 gates, 11 reference files and 1,618 lines of `gates.py`. **R6 added:** a gate that walks the GAME and looks a declaration up cannot be weakened; a gate that walks the DECLARATION can. `guidance exists` owed one card when the declared cast was truncated to one; `ascent tiers expand the world` was *narrowed by declaring* — naming only healthy tiers hid a descent meter from the gate built to catch one. Both now walk the game. **R7 added:** all four PRESENCE gates are blind to the important instance missing — which is where BOTH of `forty_miles`' blockers hid. **Two new gates close them: 23 · speakers are named** (147/145/79 blocks missing `props.speaker` across the three v2 games — three for three, because the skill mentioned `thought_bubble` once and never showed its shape) and **24 · the obligation is charged** (a declared obligation must carry an `obligation_amount` and some choice must take it). `engine.md` §25 written and `speaker = "unknown"` promoted out of *Unverified* — it had been read during the review and left there. Also: the stale "recompute the fill" instruction had a second home in `state.md`; **nine gates were documented in zero reference files**, now indexed in `SKILL.md` (23/23 findable); and `the-surfaces.md` called gate 20 by a name the board never prints. Scores: forty_miles 19/23, steam 15/21, back_home 11/19. |
| 2026-08-16 | **Third audit — gate 22 could be passed by declaring LESS.** Measured: one safe object per room, game byte-identical, **20/21 with the gate green**. The declaration checks verify the board is honest about what it declares and cannot see that it declared almost nothing — and the *lint* demoted the day before turned out to be the half that **cannot** be gamed, because it never consults the declaration. The cheatable half was the gate; the honest half was the lint. Fixed with **check 3: every thing the choices act on must be declared**, computed from the game (an anchored choice hooks onto a word its screen wrote; if no declared object covers it, an affordance is missing) — the same shrink now scores 59 undeclared against 16 for the honest declaration. Its first cut was half noise, which exposed a real bug: `_content_words` filtered stopwords on the RAW word before stemming, so every inflection walked through (`gets` survived while `get` was stopped); 30 findings became 16. **Three denominators were on one board** — gate 20 and the screen-shape lint over 213 choices (rooms AND character hubs), the anchoring lint over 166 (rooms only). Gate 20 now splits them, and it matters: **rooms are 18/22 at the cap (82%)** where the blended figure read 19/29 (66%) — the well-shaped hubs were diluting the number meant to expose the rooms. Anchoring restated as **55%** (rooms) and **51%** (like-for-like against the by-hand 41%). Scores unchanged. |
| 2026-08-16 | **Study 6 audited twice; gate 22 split.** Second pass found the anchoring check **unreachable as a gate** — run against this file's own worked example it fails *"Mirror"* under a paragraph about a wardrobe, one in four of that example's real decisions, with a ~74% ceiling on a real game. Demoted to a lint, making it the third rule here taken back out after being built as a gate; the generalisation added is **check the halves separately** — the part a parser can decide, and the part only a reader can. Gate 22 keeps the declarable half (**every declared object is written AND affords a choice**), and gained three closures: a room with screens must declare objects (the denominator was author-controlled — declaring one room shrank the check from 166 choices to 84), phantom location ids are reported, and NPC hubs are excluded on `requires_npc` as well as `npc`. ⚠️ **Root cause of the fake budgets found, and it was ours:** `templates/board.toml` said `fill = 0 # recomputed by gates.py — do not hand-maintain` and `state.md` said anything recomputable does not belong in the ledger, so three authors back-filled it. Both corrected. Also: the post-hoc detector false-positived a legitimate 250-granularity plan (now `% 50`); `DECLARED_FILL_TOLERANCE` labelled as the one invented number and why it is defensible here but was not in R5/R6; and §3's *"every floor is cleared with room"* corrected to six of seven. Scores unchanged: forty_miles 19/21, steam 16/19, back_home 12/18. |
| 2026-08-15 | **Study 6 APPLIED.** New **gate 22 · choices hang off the room** — declare-then-check against a new `board.locations[].objects`, three consistency tests and no threshold of its own, scoped to location-only hubs. **This finally gates `the-surfaces.md` R2b**, the rule that file called its highest-value ungated one, which had drifted to 55% in a 20/20 game. **Gate 1 rewritten** to judge each location against its OWN declared `fill`, with the three global constants demoted to a backstop. **Gate 20 and 19 now print the distribution and the margin** — `median 8 · 19/29 at the cap` reads differently from `median 5 · 0/12`, where before both printed the same PASS. Doctrine rewritten in `the-surfaces.md` (R3 derives from R2b; 8 named as a backstop), `the-board.md` (location count derived from the cast's rotas; the 36,000 example deleted), `the-release.md` ("6-8 locations" removed), `state.md` and `templates/board.toml`. ⚠️ **Building it found a second-order case of the same defect:** every game's declared `fill` was an exact post-hoc word count — 0 of 24 round to 100 — so the declared check passed 8/8 everywhere and proved nothing. *A budget that cannot be wrong is not a budget*; gate 1 now detects and refuses to credit it. Results, run not asserted: **forty_miles 20/20 → 19/21**, steam 17/19 → 16/19, back_home 13/18 → 12/18, and gate 22 discriminates (2 floating on the exemplary screen, 5 on the worst). `forty_miles`' board backfilled with `objects`; **no game content touched.** |
| 2026-08-15 | **Study 6 (the number becomes the spec) written**, prompted by LO on reading `forty_miles`: *"there should be a genuine reasoning on how it should be decided, not just numberify it."* Headline: **three v2 games converged on the skill's numbers rather than on their own worlds** — all three ship exactly 8 locations (the top of a range `the-release.md:128` explicitly flags as a judgement, not evidence), all three ship 3 ascent tiers, and two land within **four words** of the 4,500 mean-location floor. Total prose came in at 36,035 / 36,019 / 37,450 against a **36,000 that is not a spec anywhere** — it is illustrative arithmetic at `the-board.md:79`. The mechanism is an asymmetry: `forty_miles` clears every FLOOR by 12-97% and sits on both CEILINGS at exactly 0% margin, with 19 of 30 screens at the gate-20 cap — because a ceiling makes *pass* and *maximise* point the same way. Consequence measured against the game gate 20 was written for: **steam 214 choices / 22 screens vs forty_miles 213 / 29** — the cap redistributed the menu and raised the median from 7 to 8, while R2b (the causal half, unchecked) drifted to 41% anchored. Five rules, **no new gates** — the fix is reporting `median · count-at-cap` on ceiling gates, because "0 over 8" and "19 at exactly 8" currently print the same PASS. Nothing applied to `gates.py` or the reference files yet. |
| 2026-08-12 | Opened. Inventory of 12 items + parked save-safety. Study 1 (map & space) written. Four engine capabilities verified against source and flagged for `engine.md`. Nothing in the skill's reference files changed yet. |
| 2026-08-12 | Study 2 (how the game talks to the player) written. Eight more engine facts verified and flagged for `engine.md`. Confirmed the authored table is `[[quest_cards]]`, not `[[quests]]` — `games/back_home/REVIEW.md` G1 corrected to match. The declare-then-check pattern now holds in both studies and is proposed as the skill's standard shape. |
| 2026-08-12 | **Tier 1 graduated.** Studies 1–4 converted into `references/the-map.md`, `the-voice.md`, `the-economy.md` and an expanded `register.md`; 7 new gates + 1 new lint in `scripts/gates.py`; `engine.md` §22–23; `state.md` and `templates/board.toml` extended with `board.map` / `board.economy`. `back_home` now scores **12/17, exit 1** — the ten original gates still pass and every new failure is a defect it shipped with. One study output withdrawn (study 2 R4, the locked-door gate) after it contradicted `engine.md` §15. |
| 2026-08-12 | Study 4 (how the prose is written) written on the same corpus, scored with `gates.py`'s own explicit regex. Three measured rules, one inherited, one gate. Headline: **DoL is the coldest game in its own genre** (7.5% vs a 33.3% field median), so v2's heat floor came from an outlier — which closes the `back_home` heat worry a second time, from a second direction. `back_home`'s sentences run **16 words against a field median of 10**. Second person confirmed as the genre standard, 13/17. A third extraction trap found and fixed: widget libraries and CSS were being counted as prose, poisoning the first pass entirely. |
| 2026-08-13 | **Study 5 (what the field does in play) written — the first study in this skill grounded in playing rather than parsing.** Five games, 198 recorded turns through `twine-game-explorer`; logs in `game_explorations/study_*/study_turns.jsonl`. Headline: **the `generic_porn_game` menu outlier does not exist** (the parse counted `<img>` tags in image-button hubs; its real median is 4, not 18), and **gate 20 counts the wrong quantity** — a DoL street is 12 links of which 3–4 are decisions, the rest being onward-travel exits and a standing travel frame. Field median for *things-to-do-here* is **3, max 4**. Guidance-must-exist **confirmed 4/4**, four different mechanisms, all naming a place. `the-economy.md` R2 marked **not established** — `shady_deals` was cut short before its sinks were walked. M4 baseline established: **DoL 93% of turns, median 16 variables moved**, against a corpus median of 2. Two instrument bugs found and fixed mid-study, both of which would have inverted a finding. **Nothing applied to `gates.py` or the reference files** — two outputs contradict shipped decisions (gate 20's denominator, `engine.md` §15's locked-door ruling) and are surfaced for LO rather than resolved. |
| 2026-08-12 | Study 3 (money & pressure) written — **the first study grounded in primary measurement of more than one game.** 18 shipped sandboxes pulled, ~62,000 passages, method and limits in Appendix B. Four measured rules + one from the failure; three gates proposed. Two extraction bugs found and fixed before trusting any number. Side result: DoL's real source settled `REVIEW.md` O1 — the reference "unit" is a whole-source passage (15,587 of them, matching `gates.py:7`'s "15.6k units"), so the explicit-floor band was never on the same scale as our location-prose measure. |
