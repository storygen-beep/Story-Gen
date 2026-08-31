# The Sheets — reviewing a game before it exists

Read this in the **board** phase, after the world files and **before a line of TOML**. The board
phase used to end in TOML. It ends here now: in documents LO reads, argues with and signs, and only
then does anything become a game.

> **Why this exists.** A sandbox in this engine cannot be reviewed by playing it. Ashwell 2015, on
> the two patterns our games are built from: *"Reviewers may miss narrative content if exploration
> becomes tedious"* (Open Map) and *"Reviewers struggle to assess completeness"* (Floating Modules).
> The review surface has to be **generated, not experienced**.

> ⚠️ **This file is the output of one experiment, and every rule below is an incident.** `night_desk`
> 0.0.1 was designed in 29 sheets, signed off, and only then built. The sheets caught ten design
> defects before a line of TOML existed — an introduction two players in three would never have seen,
> a corruption on-ramp behind a door locked two nights in three, a room in two places at once.
>
> **And ten more defects were invisible from inside the format**, found only when the thing ran. The
> full comparison is `games/night_desk/iterations/001/BUILD_VS_SHEET.md`; the numbered rules here are
> its second half. **A rule with no incident behind it does not go in this file.**

---

## The workflow

```
[REVIEW]  →  LO reads and edits  →  [READY]  →  built  →  [GAME-READY]
```

Status lives **in the document title**, not in a separate tracker. Taken from the reference game's
own Writer's Workflow: the document is argued over first, and whoever implements it is not whoever
wrote it. That separation is the point — an author who implements their own sheet fills its gaps
from memory without noticing there was a gap.

**The verdict has four parts**, from the same game's submission rubric:
**Character · Coherence · Correctness · Convenience.**

---

## Five sheet types, and they never merge

| | what it carries | one per |
|---|---|---|
| **place** | what the player sees on entering a room: doors, auto-fires, who is here, things to do, ways out | location |
| **person** | the ladder — rungs, both gates, where and **when** they are reachable, refusals | character |
| **scene** | one rung: branch map, node bodies, exits, and every explicit beat written out | rung |
| **decision** | what is locked forever, what is expensive, what is cheap — blocked by reversibility | game |
| **opening** | the funnel, screen by screen, from the age gate to the first open door | game |

**They never merge**, and the reason is an incident: a person's ladder was written into a place's
choice list, and it read fine until somebody asked whether every row was a location link. A place is
what is on a screen. A person is a ladder that shows one rung at a time. Those are different
documents because the engine renders them differently.

---

## The rules

## S1 · A BEAT IS A NODE

**The unit on every sheet is the unit `gates.py` uses, or the sheet says which unit it is using and
prints both.**

> **The incident.** Every `night_desk` scene sheet said things like *"5 beats · 1 explicit"*, and
> those beats were **paragraphs**. `gates.py`'s `Beat` is one **node** — 52 nodes, 52 beats, exactly.
> A node holding three explicit paragraphs is ONE explicit beat, not three. The design reported 75
> beats; the build had 52. Mid-session the same game read **6 explicit** by the sheet and **3** by
> the instrument, and both numbers were given to LO in chat as if they measured the same thing.

**This is the rule the other nine are special cases of.** A number written on a sheet is a
**promise**. It becomes a measurement when an instrument produces it and not before.

⚠️ **There is no `--sheets` mode.** `gates.py --beat <path>` will measure loose prose, and nothing
reads a sheets folder. Until something does, every count on a sheet belongs on the **intent** side of
the measured/intent split, however carefully it was counted.

## S2 · A PLACE SHEET SAYS WHAT IT HANGS OFF

Every place sheet carries an **`ENTERED FROM`** row. The decision sheet carries the map **archetype**
and names the **exterior**.

> **The incident.** Seven rooms, each described correctly, and the map as a set was wrong: the
> exterior was one of five exits off the anchor — a leaf, which `the-map.md` R3 forbids and gate 28
> fails. The place sheet has a `WAYS OUT` block listing doors and **no row for which door is the way
> in**, so nothing could see it.

A map can be right room-by-room and wrong as a whole. Only the way *in* makes it a tree.

## S3 · A PLACE SHEET DECLARES ITS WORD BUDGET, AT DESIGN TIME

A `fill` row on every place sheet, written **before** the prose.

> **The incident.** The format declares a count of *things to do* and never a word count, so
> `v2_state.json`'s `board.locations[].fill` had to be invented after the prose existed. `gates.py`
> noticed on its own and printed **`[declared budget is post-hoc — judged on the backstop]`**.

Gate 1 checks each location against **the author's own declaration**, and the whole force of that is
that moving the number means changing the design. A budget written afterwards is a description.

## S4 · EVERY COST AND EFFECT NAMES ITS OP

`+energy` is not a specification. The sheet says the trait, the op and the value.

> **The incident.** Nine canvases shipped `op = "sub"`, which parses, imports and **silently does
> nothing** (`engine.md` — `applyTraitEffect` runs `add` and `set` only). Every energy cost in the
> game would have been free. Caught by the importer's validator; the sheets implied a mechanism they
> never specified, so the author filled it from memory and was wrong the same way nine times.

## S5 · A PERSON SHEET IS A SCHEDULE GRID

Place × hours × days. Not a list of places.

> **The incident, three parts.** Del was declared 22:00–02:00 at the desk on one sheet and
> 22:00–02:00 in the office on another — he cannot be in both. Marek was declared in the corridor
> 00:20–01:30 and in the bathroom 00:00–01:00, forty minutes of overlap. Both are two sheets each
> correct about one room, with **nothing in the format reading across them**.
>
> ⚠️ **And the third part is worse.** A rung needed him at the monitor at four in the morning. No
> sheet had him at the desk at that hour, so the rung was authored and **unreachable**. It was found
> by writing schedule rows, not by reading sheets.

The person sheet is the one artifact that can see across rooms. Its header was a list of four places
and no hours.

## S6 · NOTHING A GATE REQUIRES MAY BE DEFERRED BY A SHEET

> **The incident.** A bathroom sheet said of its walk-in: *"Not authored this release. Named here so
> it is not forgotten."* Honest, deliberate, signed off — and `the walk-in floor` is a **gate**, which
> failed 0/5. A deferral is not a pass.

A sheet has to know which of its rows are load-bearing, which means **the sheets are reconciled
against the gate list before sign-off**, not after the build.

## S7 · THE DECISION SHEET AND `v2_state.json` ARE ONE DOCUMENT WRITTEN TWICE

Either the sheet generates the ledger, or the sheet carries the exact keys the gates read:
`board.map` · `board.characters` · `board.locations[].fill` · `board.economy` · `board.ascent_tiers`
· `board.needs`. See `state.md`.

> **The incident.** The first ledger was written to a schema nothing consumes. **Six gates silently
> degraded to backstops** and one printed *"[top-3 guess — no v2_state.json]"* while the file sat
> there being read by a different gate.

## S8 · A NAMED SYSTEM POINTS AT ITS MECHANISM

A sheet that names a system names the meter or flag that drives it — or says in the open that it is
rotation.

> **The incident.** Every scene sheet said *"she speaks 3 ways"* — meek / bratty / neutral, the
> reference game's own mandatory personality check. **The game has no personality axis.** All
> thirty-three lines shipped as `block_pool`: they rotate at random instead of reading identity. The
> format let a mandatory-sounding rule be written with nothing underneath it, three times a scene,
> eleven scenes deep.

## S9 · THE BRAKE IS ON THE WAY IN

Every repeatable surface carries a **`BRAKE`** row naming what stops it, and the brake is on the
**trigger**: `trigger.costs`, `trigger.max_triggers_per_day`, or a day-cap flag condition on the
trigger whose setter sits on a choice inside.

> **The incident.** Person sheets said *"caps at 44"* and *"+2 a visit, caps at 10"*, which reads as a
> property of the rung. `_is_free` disagrees — *"one unbraked door makes the whole rung farmable, no
> matter how well priced the other doors are."* Three rounds of adding costs to inner choices moved
> nothing; moving the same costs to the triggers fixed five meters at once.

## S10 · GUIDANCE HAS A ROW

One quest-card row per ascent tier on the decision sheet, one per character on the person sheet.

> **The incident.** `quests_engine = "v2"` lights a sidebar entry and a page, and with no cards
> renders a heading and nothing. **No sheet in the format mentioned a quest card.** Nine were written
> from scratch after the first gate run. Lostness is the genre's dominant complaint — a 4.7% median
> share of player comments against grind's 0.9%.

---

## The opening sheet is a SCREEN WALK

One row per screen, in order, with the button quoted. It is the only view a design cannot satisfy by
intent: a screen either exists or it does not. `the-first-hour.md` carries the shape and the two
screens the engine writes for us.

---

## Summaries: the measured half is GENERATED

Three depths — 30 seconds, two minutes, and the full read — and in every one of them the **measured**
block is produced from the source and kept **visibly apart** from the **intent** block.

> **The defect this exists against**, and the one that started the whole thread: a summary written by
> the session that wrote the content describes what was *intended*. One release declared a
> 1,400-word landing, shipped **112 words**, and passed **46 green gates** with a summary over it
> saying the landing was built.

⚠️ **And it recurred inside the review artifact built to prevent it** — see S1. Assume you are doing
it.

---

## The folder

```
games/<slug>/
  DECISIONS.md          [READY] once signed — blocked A/B/C by reversibility
  FORMAT.md             optional, per-game notes on the shape
  sheets/               LIVING — always current, overwritten each release
    OPENING.md
    places/  people/  scenes/
  iterations/00N/       FROZEN — SHORT · LONG · CHANGES, and after a build
                        BUILD_LOG · BUILD_VS_SHEET
```

`sheets/` is the design as it stands. `iterations/` is what each release did, and never changes
again.

## What is deliberately not in a sheet

The prose. A sheet carries labels, gates and consequences — not the paragraphs. One rung per proposal
is written out in full as a **voice sample**, so the shape and the writing are approved separately
and neither hides the other.

**One exception: every explicit beat is written out where it sits.** The pivot rule — *read the
beat's last sentence; if it is about what the moment MEANS rather than what is HAPPENING, it has
pivoted* — is a reading test, and no label answers it. Each carries its own measurement line: word
count, the counted words in it, and which ceiling it sits at.

> ⚠️ **The incident.** Three beats were labelled `[explicit]` and scored **0, 0 and 1** against the
> gate's own word list. `hard` and `wet` are not on it — it is anatomy and acts, not states. Two of
> them were also **coy**: one said *"what looking at you has done to him"*, which gestures at his
> cock rather than saying it. The word list caught a craft failure, not an arithmetic one.
