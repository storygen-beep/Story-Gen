# The Sheets — reviewing a game before it exists

Read this in the **board** phase, after the world files and **before a line of TOML**. The game's
decisions are on the spine (`the-spine.md`); the sheets carry place, person and scene for the build. The board
phase used to end in TOML. It ends here now: in documents LO reads, argues with and signs, and only
then does anything become a game.

> **Why this exists.** A sandbox in this engine cannot be reviewed by playing it. Ashwell 2015, on
> the two patterns our games are built from: *"Reviewers may miss narrative content if exploration
> becomes tedious"* (Open Map) and *"Reviewers struggle to assess completeness"* (Floating Modules).
> The review surface has to be **generated, not experienced**.

> ⚠️ **What goes in this file.** Every rule here is one LO decided, or one the field shows. A rule
> with neither behind it does not go in.

---

## The workflow

```
[REVIEW]  →  LO reads and edits  →  [READY]  →  built  →  [GAME-READY]
```

Status lives **in the document title**. Taken from the reference game's own Writer's Workflow: the
document is argued over first, and whoever implements it is not whoever wrote it. That separation is
the point — an author who implements their own sheet fills its gaps from memory without noticing
there was a gap.

⚠️ **Sheets are mirrored to Notion.** `scripts/notion_sheets_sync.py` mirrors every sheet to a Notion board so one
can be read and signed away from the repo — sign-off is the only step in the pipeline that is pure
judgement and needs no terminal, and it was chained to the machine the repo is on. The rules that
keep the mirror from becoming a second source of truth:

- **The H1 on disk is authoritative.** The mirror pushes content one way and reads back only
  `Status`, the four-part verdict and comments. It never writes a sheet body.
- **A body change re-opens the row and voids the verdict**, because the verdict was given on the old
  body. Git detects it — the diff is anchored to the commit the sheet was signed at, not to a
  timestamp — and the page opens with that diff on top.
- **A commit is the trigger, never a file save.** A save is not a sign-off, and a watcher left
  running would clear a verdict while it is being given.

It makes drift **visible**; it does not detect it. S1's finding is untouched.

**The verdict has four parts**, from the same game's submission rubric:
**Character · Coherence · Correctness · Convenience.**

---

## Six sheet types, and they never merge

| | what it carries | one per |
|---|---|---|
| **system** | what the game keeps track of about her: `ambient` or `sourced`, the key it keeps, where it is fed, what reads it, which room labels it attaches to | system |
| **place** | what the player sees on entering a room: auto-fires, who is here, things to do, ways out — **what kind of place it is** (its labels), and whether it has a DOOR | location |
| **person** | the ladder — rungs, both gates, where and **when** they are reachable, refusals | character |
| **scene** | one rung: branch map, node bodies, exits, and every explicit beat written out | rung |
| **decision** | what is locked forever, what is expensive, what is cheap — blocked by reversibility | game |
| **opening** | the funnel, screen by screen, from the age gate to the first open door | game |

Each type has a one-page template in `templates/sheets/` — slots only, no example prose.

⚠️ **The system sheets are written FIRST and the place sheets are written against them**
(`the-systems.md` SY1–SY3). A room's rows come from the systems that describe her — Course of Temptation reads
`has_inclination` in 218 of its 5,294 passages, e.g. [ClassroomMenu]
`<<if $pc.has_inclination("Knowledge from the Deep")`. A place sheet whose rows
name no system is the finding, and the labels line is where it shows.

**They never merge**, and the reason is an incident: a person's ladder was written into a place's
choice list, and it read fine until somebody asked whether every row was a location link. A place is
what is on a screen. A person is a ladder that shows one rung at a time. Those are different
documents because the engine renders them differently.

---

## The rules

## S1 · A BEAT IS A SCREEN

**The unit on every sheet is the unit `gates.py` uses, or the sheet says which unit it is using and
prints both.**

`gates.py`'s `Beat` is **one screen**: a node, plus one more for each beat of a cascade in it. Group
variants and paragraphs fold into the screen they sit on (`scripts/gates.py:408`, `class Beat`, and
`:479`, *"cascade: each beat is its own screen"*). A node holding three explicit paragraphs is ONE
explicit beat, not three. A sheet that counts paragraphs as beats and a build that counts screens
report different numbers for the same scene.

**A scene sheet with a named person carries three rows: want · next step · hook** (`register.md`,
"What a scene contains").

**This is the rule the others are special cases of.** A number written on a sheet is a
**promise**. It becomes a measurement when an instrument produces it and not before.

⚠️ **There is no `--sheets` mode.** `gates.py --beat <path>` will measure loose prose, and nothing
reads a sheets folder. Until something does, every count on a sheet belongs on the **intent** side of
the measured/intent split, however carefully it was counted.

> ⚠️ **A sheet-versus-build diff is not built:** it needs sheets in one format, each row naming its
> canvas.

## S2 · A PLACE SHEET SAYS WHAT IT HANGS OFF

Every place sheet carries an **`ENTERED FROM`** row. The decision sheet carries the map **archetype**
and names the **exterior**.

> **The incident.** Seven rooms, each described correctly, and the map as a set was wrong: the
> exterior was one of five exits off the anchor — a leaf, which `the-map.md` R3 forbids and gate 28
> fails. The place sheet has a `WAYS OUT` block listing doors and **no row for which door is the way
> in**, so nothing could see it.

A map can be right room-by-room and wrong as a whole. Only the way *in* makes it a tree.

**It also carries a `DOOR` row** — added 2026-09-02. Yes or no, and if yes, the options and what
each is gated on (`the-map.md` R6). It is a row rather than an afterthought because the answer is
usually **no**: a door is a handful per game and it belongs to a person's home, while a shared room
takes occupancy-gated rows instead (R6c). A sheet that never asks the question gets the default by
accident, which is how a person's room shipped a threshold with nothing behind it.

**And every row says whether it lands on a SCREEN** — added 2026-09-02, `the-surfaces.md` R9. A row
that changes her and shows nothing resolves the act into a 2-second toast; the sheet is where that is
cheap to catch, because the answer is one column and the alternative is finding it in the build. A
*work* row may resolve to a toast. A row aimed at a person, or at her own body, may not.

**It also carries a `LABELS` row** — what kind of place this is, from the menu in `the-systems.md`
SY3, and **every row on the sheet names the system it belongs to.** Added 2026-09-02. A sheet whose
rows name no system is the thing to catch here, and it is catchable at design time for the price of
one column. Course of Temptation keys a room's options off its labels —
[Wardrobe] `<<set _stripallowed to $lastloctags.includes("stripallowed")>>`.

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

> **The incident, three parts.** One person was declared 22:00–02:00 at the desk on one sheet and
> 22:00–02:00 in the office on another — he cannot be in both. Another was declared in the corridor
> 00:20–01:30 and in the bathroom 00:00–01:00, forty minutes of overlap. Both are two sheets each
> correct about one room, with **nothing in the format reading across them**.
>
> ⚠️ **And the third part is worse.** A rung needed him at the monitor at four in the morning. No
> sheet had him at the desk at that hour, so the rung was authored and **unreachable**. It was found
> by writing schedule rows, not by reading sheets.

The person sheet is the one artifact that can see across rooms. Its header was a list of four places
and no hours.

**Each step row also carries two cells:** the **leak** — the small line or look that shows his want
before this step happens (`the-arc.md` A13) — and the **promise**, the line this step ends on, which
the next step pays (A14). A step row with neither is a step with nothing before it and nothing after.

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

One guidance card per ladder step, on the person sheet — what `--ship` checks.
`scripts/guidance_from_ladder.py` writes the cards from the ledger's ladder. Each ascent tier keeps its
own card too (`the-voice.md` R2).

> **The incident.** `quests_engine = "v2"` lights a sidebar entry and a page, and with no cards
> renders a heading and nothing. **No sheet in the format mentioned a quest card.** Nine were written
> from scratch after the first gate run. Lostness is the genre's dominant complaint — 15.5% of player
> comments against grind's 0.9% (Process Review, Round 1).

---

## S11 · A SHEET IS READ BY A PERSON, NOT BY A GATE

**The reader is LO, on a phone, deciding.** Every rule above says what a sheet must *contain*.
None of them said whether the person signing it can get through it, and the omission is not
neutral — an author satisfying S1–S10 produces a document written in the ledger's voice, because
that is the only voice the rules describe.

**This is SKILL.md's "two voices" rule finding its third voice.** `register.md` owns what the
player reads after a click. `the-voice.md` owns labels, room names and guidance cards. **Neither
owns the document a human signs**, and until now nothing did.

Four things, and they cost nothing:

- **No `file.md` §-citations, no `v2.py:` line numbers, no rule ids.** The evidence belongs in
  `WANT.md` and `v2_state.json` `decisions[]`, which is where it already is. Duplicating it into
  the review surface is what makes the review surface unreadable. One pointer at the bottom.
- **A statistic only appears when the number IS the decision.** *"$150 a week against $220 earned"*
  stays. *"19 blank to 10 written, 80.4% of top-30 engagement"* goes — it justifies a call that has
  already been made, and LO is not re-deriving it.
- **Table cells under ~15 words.** A 70-word cell is a paragraph wearing a table's clothes and it
  is unreadable on a phone. If the reason needs 40 words, it is a section, not a cell.
- **Plain words for internal vocabulary.** *"trait keys are save join-keys; a rename strands every
  save"* becomes *"every saved game breaks."* Same fact, no glossary.

⚠️ **Lead with what needs him.** A decision sheet's open questions are the only part that cannot be
read later, so they go **first** — question, your recommendation, one line on why it matters — above
the settled blocks.

**The test:** hand it to somebody who has not read this skill. If they cannot say what they are
being asked to decide, the sheet is not done, however complete it is.

## S12 · WHEN THE SKILL AND A SHEET DISAGREE, STOP AND ASK

**The rule:** when a rule in this skill and a line on the game's sheets point different ways, the
author does not pick one. Stop, quote both lines, and ask the owner which wins. Until the owner
answers, neither is built. **A signed spine page wins over an older sheet**: the sheet is updated to
match it.

**Two kinds of sheet line, and only one of them is asked about:**

| kind | examples | when it clashes with a skill rule |
|---|---|---|
| **a fact about the world** | who is in which room at what hour, the money, what someone knows, a person's age | the fact holds. The truth rule (`register.md`) is built on it. A clash here is the skill rule being applied wrong |
| **a design choice** | how the opening runs, how much a person says, when a character first shows what he wants | ask. The skill may have changed since the sheet was written, or the owner may have chosen against the skill for this game |

**Asking is not the same as recording.** Writing the conflict into a draft's notes and building the
cautious side is the failure this rule exists for. Ask first, then write.

## S13 · AN APPROVED PLAN LIVES IN THE GAME'S OWN PAGES

**The rule:** when the owner approves a plan for a game (a new opening, a changed character, a new
system), the plan goes into that game's sheets before anything is built from it. A plan that lives
only in a chat, a research folder or a document outside `games/<slug>/` is invisible to the next
session, because the next session reads the game.

- **The sheets are the owner's.** Where the owner has said the agent does not write them, the agent
  hands over the paragraph — as a draft sheet in `games/<slug>/proposals/` — and the owner places it,
  or the owner names the file and says to write it.
  Either way, the plan ends up on the page.
- **A sheet that an approved plan has replaced is marked**, so nobody builds from the old version
  while the new one is on its way. One line under the title is enough: *"Replaced by the plan approved
  on <date>. Do not build from this page."*
- **The skill holds no game's plan.** It holds the rules for every game, with placeholders instead of
  names (`register.md`, "Show the mechanism. Never show the world."). The game-specific version, with
  its people and its facts, only exists on the game's pages.

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
  DECISIONS.md          [READY] once signed — blocked A/B/C by reversibility.
                        MIRRORED, and it is order 1 — see below
  FORMAT.md             optional, per-game notes on the shape
  sheets/               LIVING — always current, overwritten each release
    OPENING.md
    REVIEW_ORDER.md     GENERATED by the mirror on every push. Never authored,
                        never mirrored back, never hand-edited
    places/  people/  scenes/  systems/
  spine/                SP1–SP7 (the-spine.md)
  proposals/            draft sheets handed over for the owner to place (S13)
  iterations/00N/       FROZEN — SHORT · LONG · CHANGES, and after a build
                        BUILD_LOG · BUILD_VS_SHEET
```

`sheets/` is the design as it stands. `iterations/` is what each release did, and never changes
again.

⚠️ **`DECISIONS.md` is a sheet and sits outside `sheets/`.** It is one of the six types and carries a
status marker like the rest, and because of where it lives the first version of the mirror could not
see it. Anything walking the sheets collects it explicitly.

### Review order is a property of the KIND

**Do not number the filenames.** 43 of 138 sheets already carry a two-digit number and it means the
**rung** — `ray_03_the_offer` — so a review-order prefix puts two numbers meaning two things in one
name. 80 cross-references between sheets are by filename and a rename breaks them.

The order is already fixed by the rules above, so it is derived instead:

**1** `decision` — everything reconciles against it (S6) · **2** `system` — written first, and the
place sheets are written against them (SY1–SY3) · **3** `place` · **4** `person` — a place × hours
grid, so its places must exist (S5) · **5** `scene` — one rung of a person · **6–9** `opening`,
`guidance`, `index`, `format`.

A gap in the numbering is a finding: a game with places and no system sheets built its rooms against
nothing, which is the SY1–SY3 defect.

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

---

**Then:** when every sheet is [READY] and LO has signed it, set `phase = "sheets"` and move to
`references/the-release.md`, § first release.
