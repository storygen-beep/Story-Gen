# The sheet format — locked 2026-08-31

The review artifact for this experiment. **Not in the skill.** It lives here until the loop proves
out; if it does, it gets promoted and this file gets deleted.

## Why this shape

A sandbox in this engine cannot be reviewed by playing it — that is a published property of the
structure, not a failure of attention. Sam Kabo Ashwell, *Standard Patterns in Choice-Based Games*
(2015), on the two patterns our games are built from:

> **Open Map** — "Reviewers may miss narrative content if exploration becomes tedious or
> unmotivating."
> **Floating Modules** — "Reviewers struggle to assess completeness; grinding for stat changes may
> obscure narrative quality."

So the review surface has to be **generated, not experienced**. These sheets are that surface.

The workflow is copied from the reference game's own Writer's Workflow: a document is written,
marked `[REVIEW]`, argued over, marked `[READY]`, and only then implemented — by someone who is not
the writer. Status lives on the artifact so a folder listing shows the state of everything.

<pre>
[REVIEW]  →  LO reads and edits  →  [READY]  →  built  →  [GAME-READY]
</pre>

## Three sheet types, and they never merge

| sheet | answers | one per |
|---|---|---|
| **place** | what is this room | location |
| **person** | how far does this go | character |
| **scene** | what happens when you click | canvas |

A place sheet lists what is on the location screen. A person sheet lists their ladder — which is
**one click deeper**, because the engine renders a character as a single clickable portrait, not as
a menu (`renderNpcPortraits`, `v2.py:5114`).

Mixing them is the error this format exists to prevent: content aimed at a person lives on their
hub, content aimed at the room lives on the room, and they never share an exit list.

## Place sheet

Sections are in the order the engine renders them (`_generate_simple_locations`, `v2.py:9695`).

<pre>
<NAME>                                          id: <slug>
release N · authored <n> · player sees <a>–<b> · cap 8

DOOR         <entry cost> · <lock, or "always open">

INSTEAD OF THE SCREEN
  <canvas>              <when it fires>

THE ROOM SAYS
  base            <the description>
  ~ <condition>   <the variant>

WHO IS HERE
  <Name>    <hours, and how often>              → see <Name> sheet   (<cost badge>)

THINGS TO DO
  <label>                          <time>  <effect>
      ~ <condition>   <how the label changes>
  🔒 <label> — "<the reason, in the game's own voice>"

WAYS OUT
  → <Place>       <travel cost>   <who is visible there> · <NEW>
  → <Place>       🔒 "<in-world reason>"
</pre>

### Reading it

| mark | means |
|---|---|
| **indent** | only appears when the line above it is true. Conditions nest. |
| **`~`** | always there, but says something different — a **variant**, not a lock |
| **🔒** | visible and locked, with the reason the player is shown |
| **`[new]`** | added this release |
| **`[chg]`** | existed; its words, gate, cost or target moved — **the mark that breaks saves and stale prose** |
| **`[gone]`** | removed |
| unmarked | untouched, shown for context |

**Show the whole screen every time, not just the delta.** A game shipped 23 choices on one front
desk and scored full marks, because every release only ever showed its own additions and nobody ever
looked at the total. The field median for things-to-do-at-a-place is **3**; the engine's backstop is
8. The count line at the top is what you approve.

**`~` is not decoration.** Of 27,505 conditions wrapped around an action in 26 shipped sandboxes,
**35% select a variant where every branch offers something and only 23% refuse anything.** A
notation that can only draw locks teaches an author to build a game made of locks. That is not a
guess — a rung table sitting in a template taught all five v2 games to start their meters at 15.

**Only sheets this release touches go in a proposal.** Otherwise every proposal is the whole game.

## Person sheet

<pre>
<NAME>                                     at: <locations>
<meter> 0→N · <n> rungs authored · showing 1 at a time

  <rung>   <what she does>                  <time>  <effect>
  <rung>   (<a conversation — unlocks nothing>)
  🔒 <rung> — "<the reason>"
</pre>

Three or so rungs on a full ladder should be **conversations that unlock nothing** — her explaining
why not yet, placed immediately under the next escalation. That is the field's own answer to "how
does she get from no to yes", and nothing in our skill has a name for it.

## Scene sheet

One file per scene. **Map first**, then the short summary, then the nodes. Map entries are links to
the node sections in the same file, so the map doubles as the table of contents.

```markdown
# <Person> · <rung> — "<the button text that reaches it>"

## Map
  enter ──► [base] ──┬──► [base]        "Stay where you are"    (loop)
                     ├──► 🔒 rung 15    exhibitionism 15 · "not yet"
                     └──► the_desk      "I should get the desk"

## In short
- <what it is · where · how long · repeatable or not>
- <n> beats · <n> explicit · speaks <n> ways · <n> clips · <n> words (budget <n>)
- <what it moves, and where it caps>
- <where it can go from here, and what is locked>

## base — <what this node is>
  1  <beat>
  2  <beat>              ~ <variant>
```

**A scene is referenced everywhere by its button text, with a link to its file.** A place sheet or a
person sheet never restates a scene's contents — it points at it. That keeps the sheets stable:
adding beats to a scene does not touch the room it hangs in.

**When an exit opens a sex loop, the map names it and lists the acts on the menu.** A loop never
hides behind one word:

<pre>
  enter ──► [approach] ──► [LOOP · what you do to him] ──┬──► [finish · mouth]
                                                         ├──► [finish · inside]
                                                         └──► <a href="sheets/places/the_office.md">the_office</a>

  LOOP · what you do to him              menu, re-entered until she finishes
      Take him in your mouth                  → [act_mouth]
      Turn around and let him behind you      → [act_behind]
      🔒 Let him finish inside you            exhibitionism 20 · "he hasn't earned that"
</pre>

## Decision sheet — the from-scratch phase

The Want and the Board arrive as one long document and nobody can review 400 lines of equal-weight
prose. So they are re-sorted by **what it costs if the decision is wrong**, never by topic:

| block | meaning |
|---|---|
| **A · LOCKED FOREVER** | changing it after the first release breaks every save in the wild |
| **B · EXPENSIVE** | changing it rewrites content that already exists |
| **C · CHEAP** | change it any time |

Each decision carries **what it is · the pick · why · what it costs if wrong**, and the ones the
author is least sure of are named at the top. Block A gets argued properly; block C gets skimmed.

## Every document is layered — three depths

The top two are in **plain words**: short sentences, no jargon, key points.

| depth | where it lives | how long |
|---|---|---|
| **short** | the top of the file itself | 30 seconds |
| **long** | its own file, only when the thing is big enough to need one | ~2 minutes |
| **detail** | the body of the file — evidence, citations, numbers | as long as it takes |

⚠️ **A summary has two halves and they stay visibly apart.**

- **measured** — counts, rungs, words written against budget, what is locked. Generated from the
  source. Cannot flatter.
- **intent** — what it is for and what it should feel like. Written by the author, and marked as
  the author's.

**Read the measured half first.** If those numbers are wrong, the prose does not matter. A summary
written alongside the work describes what was *intended*; the whole reason this loop exists is that
one game's landing was 112 words against a declared 1,400 and every check was green over it.

## The folder

<pre>
games/<slug>/
  README.md            the index — every file, one line, its status
  FORMAT.md            this file
  DECISIONS.md         the from-scratch decisions
  DECISIONS_LONG.md    the same, plainly

  sheets/              ← LIVING. always current. overwritten every release.
    places/   <a href="sheets/places/the_desk.md">the_desk</a>.md · <a href="sheets/places/the_corridor.md">the_corridor</a>.md · ...
    people/   del.md · marek.md
    scenes/   del_12_behind_you_at_the_monitor.md · ...

  iterations/          ← FROZEN. what each release did, and why.
    001/  SHORT.md · LONG.md · CHANGES.md
</pre>

⚠️ **Living and frozen must never mix.** A folder per release means *"what is the desk right now"*
has no single answer — you reassemble it out of three folders, which is the exact problem the
whole-screen rule above exists to kill. **Sheets are what the game is. Iterations are what we did.**

## Opening sheet

The opening is the only part of the game with a fixed order and no wandering, so **dead air is fatal
there and nowhere else.** It is not a screen — it is roughly the whole first session, and no place,
person or scene sheet can see across it.

### What an opening contains — nine things

From `the-first-hour.md` F1–F10:

1. **The boot** — the `starting_canvas`. One-shot, high priority, `is_repeatable = false`. Puts her
   where she starts and begins the chain. **It does not carry the cast.**
2. **The capstone** — a second one-shot at the same place, gated on the flag the boot sets. Where
   the prose is allowed to spend. Both auto-fire; the flag is what guarantees the order.
3. **One shape, committed to** — **cold open** (names nobody) or **staged open** (each person on
   screen and speaking). *The defect is the middle*: a short opening naming four people the player
   cannot picture. ⚠️ The word ranges this rule used to carry were deleted 2026-08-24 as
   non-reproducible. It is a **consistency** rule — the cast load and the word budget must agree.
4. **A meeting per character** — every `npc=` hub sits behind a non-repeatable scene that names
   them, ~100–170 words, and somebody speaks. It must fire **where they are**: `requires_npc` does
   not gate auto-fire, so without a schedule window the introduction plays to an empty room.
5. **Role before name** — "the man who owns the place" until the meeting flag is set, "Del" after.
6. **One flag per character** — `met_del`, `met_marek`. One flag opening the whole cast is the
   cold-spawned hub in a coat.
7. **The systems, taught as a set.** ⚠️ **This is where this project departs from the skill.**
   `the-first-hour.md` F4 offers a **floor** — one beat per system, or a sidebar row at zero. The
   shape used here is stronger and deliberate: **a dedicated mechanics beat that names the game and
   states every system, plainly, as a list.**
8. **It refuses nothing** — teach the price, do not charge it. Measured: **12 of 14 top-thirty
   openings contain zero spoken refusals**, and the largest in the corpus runs 78 passages and
   8,057 words with seven conditionals and not one refusal. Refusals begin where the funnel ends.
   **Any recurring charge is armed here and fires later.**
9. **It hands over into an open door** — the last click lands on a real location, at a clock time,
   with something actually open. A random ambient is not a door. A `substitution_only` walk-in is
   not a door.

### What the nine leave out — how it is DELIVERED

The nine above come from `the-first-hour.md`, and every one of them is about **what the opening
says**. Not one is about **what the player does with their hands.** That hole shipped straight into
this game's first opening sheet: three beats were specified, and nothing said whether they were one
screen or three, what was written on the button between them, or what the player saw before any of
it.

**Four engine facts settle it, and all four belong on the sheet.**

1. **Screen one is the age gate, and we get it for free.** `Start` initialises state and renders a
   title screen; the starting canvas is reached only through
   `[[✓ I am 18 or older - Enter Game->StartingCanvas_<canvas>_Node_<node>]]` (`engine.md` §12).
   **The player's first screen is never beat 1.** A sheet whose timeline opens on the first prose
   beat is describing the second screen and calling it the first.
2. **There may be a character screen in front of the game, and it is not ours.** `[player]
   customizable = true` with one `[[player.customization_fields]]` builds a `CustomizeCharacters`
   passage **and repoints the age gate at it** (`v2.py:1065`, `v2.py:9251`). Its headings and its
   button are hard-coded — *"Customize Characters"*, *"Personalize the characters in your story"*,
   *"Continue to Game"*. **Seven of our fifteen built games ship that screen.** The only authored
   text on it is `player_description` (`v2.py:9509`). A field with `id = "name"` writes
   `$player.name`; anything else writes `$player.<id>` (`v2.py:9522`).
3. **One node is one screen.** The engine plays a node chain back one screen at a time
   (`the-first-hour.md:170`). Three beats in one node is ONE screen carrying all three; three nodes
   is three screens. Those are different things to sit through, and the sheet has to say which.
4. **The break between screens is a written button.** A mid-funnel node exits through
   `exit_block.type = "choices"` carrying a single choice whose `text` is the button — a line in the
   game's voice, not "Continue". `seventh_day`'s reads *"Get up before the others."* The last node
   exits through `exit_block.type = "location"`, whose `config` carries `locationId`,
   `time_progression_minutes`, `flagEffects` and `effects` — so **the handover is also where the
   opening sets its flags and pays its first money.**

**Measured across every opening we have built** — nodes, and words in them:

<pre>
  seventh_day      5 screens  420 w        commuter         1    93
  the_allowance    5          535          last_call        1    60
  back_home        4          468          late_shifts      1    45
  forty_miles      3          339          mothers_place    1   101
  steam            3          285          mrs_vance        1   100
  off_season       2          160          the_inheritance  1    31
  vesper           2           89          the_route        1   136
                                           the_season       1   119
</pre>

**Eight of fifteen are a single screen**, then the sandbox opens. The largest true opening in the
field corpus is Course of Temptation's at **78 passages and 8,057 words** (`the-first-hour.md` F4b).
Length is a decision the author makes; what this format requires is that the decision be **visible**
rather than arrived at by default.

### The shape this project uses

<pre>
0 · Start                    <b>engine</b>   title card and age gate. Free, and always first.
1 · CustomizeCharacters      <b>engine</b>   only if declared. THE ONE CHOICE lives here —
                                      she is named in a form field, not in a prose beat.
                                      The only text we write on it is player_description.

BOOT · the starting canvas · small, and it does not carry the cast
  screen 2   SETUP, stated flat      who · how old · where · what the deal is. No scene-setting.
  screen 3   THE WANT                what she is saving for, and what she has. One screen.
  ──── location exit ────►  the anchor, at a clock time · sets the boot flag

CAPSTONE · a second one-shot at the same place, gated on that flag · where prose may spend
  screen 4   THE MECHANICS           a `heading` naming the game, then every system as a
                                     short list — what it is, and what moves it.
                                     ⚠️ GROUP them once there are more than three:
                                     what you earn · what you climb · what your body needs
  screen 5   THE ROOM                closes the frame the mechanics screen broke. The anchor,
                                     in the game's own voice, at the hour it starts.

MEETINGS · one per character, each their own one-shot, each where that person actually is

THE JOB, DONE ONCE                   the funnel's last piece. She does the thing the game is
                                     about, guided, with a choice that colours and refuses
                                     nothing, and the money lands in her hand.
</pre>

⚠️ **Boot and capstone are two canvases and the flag is what orders them.** Both auto-fire through
`selectAutoFireCanvasForLocation`, which takes the highest-priority valid **non-repeatable** canvas
and skips every repeatable one (`v2.py:4453-4471`) — no schedule is needed or wanted.
`the-first-hour.md` F2 measures the cost of collapsing them: v2's openings run **more than double**
v1's (median 402 against 184) *because* one canvas ended up carrying everything.

⚠️ **The name belongs on the engine's form, not in a prose beat.** If the game declares a character
screen at all, a free-text beat asking the same question is a second screen doing the first one's
job.

⚠️ **The mechanics beat is deliberately denser than the game's normal beat, and that is correct.**
The flat-prose rule exists because rooms are re-entered forty times and density rots on re-read. The
opening is seen **once**, which is the same argument that already lets a one-time capstone spend
prose. It is the one place in the game where a list beats a paragraph.

⚠️ **Naming the game is what makes the mechanics beat legal.** Once the screen has said
*"<Title> — the game runs on these numbers"*, a list of meters is expected rather than jarring. The
frame is broken on purpose, the piece is said, and the frame closes again. Use a real `heading`
block so it is visually separate from the prose either side.

### How an opening is reviewed — three views, all needed

**The screen walk** — one row per screen, in order, with the button on it. **This is the view that
cannot be faked**, and it is the one this format shipped without. A screen either exists or it does
not; intent cannot satisfy a row. The other two views describe an opening, and an opening that was
never broken into screens will pass both of them.

<pre>
  #  canvas · node                 what is on the screen                    the button
 ────────────────────────────────────────────────────────────────────────────────────────────
  0  Start            <b>engine</b>      title card · age gate                    ✓ I am 18 or older - Enter Game
  1  CustomizeCharacters <b>engine</b>   "Your Character" · the fields declared    Continue to Game
 ────────────────────────────────────────────────────────────────────────────────────────────
  2  boot · <i>node</i>                  …                                        "…"
     ── location exit ──►  the anchor, at a clock time · sets <b>flag</b>
 ────────────────────────────────────────────────────────────────────────────────────────────
  4  capstone · <i>node</i>              …                                        "…"
 ────────────────────────────────────────────────────────────────────────────────────────────
  6  <i>meeting</i> · <i>node</i>               …                                        "…"
 ────────────────────────────────────────────────────────────────────────────────────────────
     <b>THE FUNNEL ENDS.</b>  what is live on the screen it hands over to
</pre>

⚠️ **Rows 0 and 1 are written in even though we do not author them.** They are the screens the
player actually sees first. Leaving them off is how a sheet ends up describing an opening the player
never has — and it is how *"Personalize the characters in your story"* becomes the second thing
somebody reads in an atmospheric game without anyone noticing.

⚠️ **Every button is quoted, not summarised.** "the player continues" is not a row; the line the
button carries is the row. If it has not been written, the screen is not finished.

**The timeline** — what it is like to sit through. Clock down the left, dead air marked. The screen
walk says what exists; this says how it feels in sequence.

<pre>
NIGHT 1

  —     screen 0   age gate                          <b>engine</b>      no choice
  —     screen 1   Customize · her name              <b>engine</b>      1 field
21:50   screen 2   who she is · three weeks · $80                 no choice
21:55   screen 4   the game names itself — five systems           no choice
22:00   screens 6–8  the handover                              <b>← MEET DEL</b>
22:40   screens 9–11 the first check-in                       <b>← THE FIRST MONEY</b>
23:00   <b>── THE FUNNEL ENDS ──</b>
23:00   ⚠ nothing arrives until 00:20 — about 80 minutes
00:20   Marek comes down for ice                              <b>← MEET MAREK</b>, if she walks
06:00   clock out · corruption 0→2 if she watched the monitor
</pre>

⚠️ **Dead air is fatal inside the funnel and legitimate after it.** Where the quiet falls matters
more than how long it is. A gap between two funnel screens is a defect; the same gap after the
handover is the open game teaching the player what quiet feels like.

**The checklist** — what the opening owes, against when each lands. This is the view that catches
what nobody told the player.

<pre>
what the opening owes                        when it lands
──────────────────────────────────────────────────────────
she is named                                 screen 1   (the engine's chargen, if declared)
the hours are stated out loud                21:50
what she is saving for                       21:52
every live meter named and explained         21:55
any link between two meters stated           21:55
the body's needs named                       21:55
each character met, in their own scene       22:00 · 00:20
the job is done once, not just described     22:40
the money is felt, not stated                23:00
nothing is refused during it                 ✔ no locked door and no failed check
any recurring charge armed, not fired        ✔ first deduction is Friday
ends on a door that is open                  23:00 → the anchor, things live
──────────────────────────────────────────────────────────
</pre>

**A row with no time against it is the finding.** On the first draft of this design three rows were
empty and the game explained none of its own systems. On the second, the two rows that came out of
the screen walk were empty — *the job is done once* and *the money is felt* — because the player
reached the end of the funnel having pressed nothing but Continue.

## What the format must not lose

Eight engine facts, all read from source, that a looser sheet would drop:

1. **Auto-fire replaces the screen.** A due canvas means the room never renders
   (`getStoryCanvasRedirect`, `v2.py:5091`). It is not something *on* the page.
2. **No declared schedule, no portrait — silently.** Presence needs `[[npcs.schedules]]` *and*
   `getNpcLocation` to agree (`v2.py:5114`).
3. **One canvas per person per room.** Highest `priority` wins; the rest are invisible. A person
   sheet shows a ladder, and the player sees one rung of it at a time.
4. **Four greyed states, and they differ.** Cost-blocked is still clickable with a cost tag;
   cooldown-blocked is dead text and only renders if the author opted in with `show_when_blocked`
   plus a `cooldown_message`; a locked exit is a greyed card with an in-world reason; a locked
   choice inside a canvas uses `locked_text`.
5. **Exits carry information** — travel cost, a NEW badge, and portraits of who is there. The nav
   badge uses a *different* presence rule than the portrait, so a person can show on the door with
   nothing clickable inside.
6. **The room's own text can vary.** `description_variants` is a first-match chain with the base as
   the else (`_render_location_description`, `v2.py:9848`).
7. **The player's first two screens may not be ours.** The age gate always precedes the starting
   canvas (`engine.md` §12), and a declared `[player] customizable` inserts `CustomizeCharacters`
   between them with hard-coded headings and button (`v2.py:1065`, `v2.py:9251`).
8. **One node is one screen, and the break carries a written button.** A node chain plays back one
   screen at a time (`the-first-hour.md:170`); mid-chain exits are `exit_block.type = "choices"`
   with a single choice, and the last is `type = "location"` whose `config` sets the flags and
   pays the money.

## What is deliberately not in a sheet

The prose. A sheet carries labels, gates and consequences — not the paragraphs. One rung per
proposal is written out in full as a **voice sample**, so the shape and the writing get approved
separately and neither hides the other.

### The one exception — every explicit beat is written out where it sits

`[new] 2026-08-31`

**An explicit beat is the one thing a label cannot carry.** The rule it has to satisfy is a reading
test and nothing else: *read the beat's last sentence — if it is about what the moment MEANS rather
than what is HAPPENING, the beat has pivoted and it scores 0–1.* No summary answers that. `[explicit]
what her body does back` is a promise, and a promise is exactly what the measured-versus-intent split
exists to catch.

So the label stays in the beat list **and** the beat is written out in full underneath it, with its
own line of measurement:

<pre>
`42 words · tits · ass · hard — 3 frozen-list words · Del tier 1 ceiling, exactly at it`
</pre>

Three things that line has to show, because all three are floors the build checks or the design
declares:

- **the word count** — the beat target is ~35–40 words, flat across every tier
- **the frozen-list words in it** — 3+ per explicit beat is the measured floor
- **which person's ceiling it sits at, and that it is not above it** — the per-NPC ceilings are a
  ceiling, never a floor, and writing under one is a defect

⚠️ **This does not reopen the voice sample.** The sample is one *whole rung* written out so the
scene's shape and its writing can be judged apart from each other. This is narrower: the explicit
beats only, wherever they are, because they are the ones that cannot be reviewed any other way.
