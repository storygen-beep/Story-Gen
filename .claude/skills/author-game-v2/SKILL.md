---
name: author-game-v2
description: EXPLICIT-INVOKE ONLY — the experimental v2 of game authoring, run when the user asks for "/author-game-v2", "author-game v2", "v2 on <slug>", or "start a v2 game". Authors adult sandbox games as a release stream that never stalls — a goal can end and a new one opens — rather than as a story with chapters: one ascent meter that buys access, locations that must be filled before new ones open, explicit content living in the surfaces the player returns to, and every release ending on a visible locked door. Ships a runnable scoreboard (scripts/gates.py) whose thresholds came from measuring a top game's own source and, for the world/guidance/economy/prose gates, a field of 18 shipped sandboxes. Do NOT use for a plain "start a new game" / "continue writing <game>" / "add an NPC or beat to games/<slug>" request; those belong to the incumbent author-game skill until the user promotes this one.
---

# author-game v2 — the release stream

**v1 designs a story and then builds it. v2 designs a world and keeps it moving: when a goal ends, a new one opens.**

That is the whole change, and it came out of measurement, not taste. Ten snapshots of
Degrees of Lewdity's own source (2018-11 → 2026-07, 25 → 61 locations, 254k → 2.24M words)
measured on one frozen instrument. **Degrees of Lewdity is "the
reference game" wherever this skill says so. It fails the adults-only rule, so the skill uses
its structure and numbers, never its scenes.**

## The four commitments

Every one is a measured number, not an opinion. The evidence lives inline in
`scripts/gates.py`; the short version:

1. **The game never stalls; a goal can end and a new one opens.** Endings are normal — at least 9
   of the top 26 games have real ones, and two finished games still rank in the top 26. What loses
   players is a game with nothing next: when a goal ends, the next one opens in the same release.

2. **Fill before you widen — as a distribution, not a floor.** DoL's seed put 116,540 words
   across 25 locations: **mean 4,661, median 3,154**, and **one anchor location** holding
   **30% of all location prose**, with a long tail down to a 302-word bus station — *the reference
   game's 2018 seed, labelled*. The field has the shape at **district** scale (the top district holds a
   median 49.4% of prose; 22 of 26 games reach 25%) and **not at room** scale (the top room, a median
   13.1%; 6 of 26). Thin satellites are fine; a world with no centre is not. By 2026 the mean had risen to 24,564
   while locations only went 25 → 61 — depth outpaces breadth, every year.

3. **Heat lives where the player returns** — most explicit content sits where the player can go
   back. The gate counts **beats** (a beat is one screen): `explicit floor` wants **7.5% of repeatable
   beats** to carry three or more explicit words. The 7.5% is the reference game's band (7.5–9.3%,
   held eight years), not the genre's rate, and the field reads differently by unit:

   | unit | field median | the reference game's 7.5% |
   |---|---|---|
   | per passage — 18 shipped sandboxes | 33.3% | the lowest of the 18 |
   | per paragraph — 26 top games | 4.4% | reached by 8 of 26 |

   No field figure per beat exists yet, so a pass reads "not empty", never "hot" (`register.md`).

4. **A release adds events, not places.** One full six-week DoL cycle: +196 units,
   +24,388 words, **zero** new locations, and all ten of its content commits were events at
   an existing place with an existing character. 55.6% of its commits were fixes.
   **Open places early, add people over time.** Day 1 opens most places and few people: 42–98% of
   places and 0–38% of people, in 7 of 7 games (round 7, `ROUND7_REPORT.md`). Most systems are usable
   on day 1 at their bottom rung, 79–87% (round 9b, `ROUND9B_REPORT.md`). So a release adds rungs and
   people, and a new system only as the top of an existing ladder.

## The fifth commitment — the machinery colours far more than it locks

Eleven field-study sections agree on it. Each measured a different subsystem and each came back with the same answer:

```
reputation refuses                ~10% of branch arms (13 games)          the-meters.md W5b
the body refuses          median  10%  of its reads                       the-meters.md W7
her willingness gates              6%  of act links                       the-meters.md W6
act links with no gate at all     47%  of 7,598                           the-surfaces.md R3b
refusals that render nothing      71%  of 16,167                          the-surfaces.md R5c
conditionals around an action     35%  select a variant · 23% refuse      the-surfaces.md R5
```

⚠️ **Colours-more-than-it-locks is not decides-nothing.** Measured over 13 games, a **median
41% of reputation reads change something mechanical** — by delivering a person, modifying a roll
or scaling a rate, none of which prints a refusal. Read `the-meters.md` W5b before using this row.

**A meter's main job in this genre is to select text, not to bar a door.** Reputation does not stop
her walking into the bar — it changes what the barman says. The body does not lock the room — it
changes the sentence. The lock is the exception, and it is the *cheap* half: it costs one condition
and buys one refusal, where the same meter read as a colour buys a different line on every visit
forever.

⚠️ **The field's conditions mostly ask which step, not whether a number is big enough.** Every
condition in the 26-game field, on one instrument (`findings_K_mirror.md` §2):

| | field |
|---|---|
| **equality** — which step are you on | **53%** |
| **threshold** — is your number big enough | 31% |
| boolean — is this switch on | 9% |

Threshold and boolean are both locks. **`block_pool` is the primitive for writing many versions of
one line.**

**What to do with it.** Before adding a condition, ask which of the two it is. If the answer is
*"it stops her"*, ask what the other branch says, because the field would usually have written one
(`the-surfaces.md` R5 and R5d, `the-meters.md` W5b). **This is a frame, not a quota** — no section
measured a defensible ratio and nothing here is gated.

## The discipline this is, and its published failure modes

**Our games are storylets.** Quality-based narrative — Failbetter's term, Emily Short's and Max
Kreminski's literature — is the published discipline for exactly this architecture: content units
gated on state, selected by salience, re-entered rather than traversed. Measured 2026-08-31 across
this skill: `storylet` 0 · `quality-based` 0 · `QBN` 0 · `salience` 0 · `Failbetter` 0 · `Ashwell` 0 ·
`Emily Short` 0, in 21,831 lines. **We had been inventing the vocabulary of a solved problem.**

By Ashwell's taxonomy ours are **Loop and Grow + Open Map + Floating Modules at once**, and each of
those carries published weaknesses:

| the pattern | its documented weakness |
|---|---|
| Open Map | *"Reviewers may miss narrative content if exploration becomes tedious"* — and lostness is the genre's dominant complaint, 15.5% of player comments (per-game median 14.4%) against grind's 0.9% (Process Review, Round 1) |
| Floating Modules | *"Reviewers struggle to assess completeness"* |
| Floating Modules | *"requires substantial content; collapses into linearity otherwise"* |
| all three | *"writers tend to rebound quickly to a more unified structure"* — the arc pull, **a known property of the structure, not indiscipline** |

That last row is worth the whole table. The urge to make a sandbox into a story is documented
behaviour, not a failure of will, and a method that does not push back on it will lose to it.

## The three kinds of content

Named from what those release commits actually do, so the vocabulary owes nothing to
anything earlier:

- **STANDING** — a place or person she can go to and act on, repeatedly. The main surface.
  Carries the explicit floor.
- **TRIGGERED** — fires when her state matches. DoL's own commit language: *"during the
  weekends"*, *"when exposed"*, *"at high stress"*. For the `female` protagonist declared in
  `want.player` — the default, and the case this was measured on — this is the main heat
  engine, not a garnish.
- **MILESTONE** — fires once at a threshold, then opens standing content.

**Every milestone names the standing content it turns on.** A milestone that opens nothing
is a dead end, and `gates.py` will say so.

⚠️ **A milestone is rarely alone — in the field it is the LAST step of a numbered arc, and the
standing surface is what finishing that arc buys.** `course-of-temptation` runs ten steps before
the act becomes something she can simply do. Write one or two long chains for the central people
and run `lint · the arc ladder`. `references/the-arc.md`.

⚠️ **Those three answer WHEN content fires. They do not answer WHICH SCREEN IT LIVES ON, and that
is a separate question with its own file — `references/the-surfaces.md`.** Ask *who is this aimed
at*: a person → their hub · the room or herself → its own located canvas · her, done to her → a
substitution. They never share an exit block.

**How many choices a room has is not a number you pick — it falls out of what the room serves.**
A room's list is **needs + work + people**, and nothing else (`the-surfaces.md` R2). A body needs
about five things and a room contains fifty nouns, so the count falls out of a set that cannot grow.
That is what separates a room from a button list.

⚠️ **And "people" is not one bucket — each of them has to own a different part of the world.**
A character is separated from the others by the **subject he talks about and the people who are
his** (the doctor has the clinic; the administrator has the votes and the levy; one woman has the
shop and her two friends)
(`the-surfaces.md` R8, `register.md` S3, `the-meters.md` W6).

**A canvas advances in one of two ways, and the content kind picks which** (`the-surfaces.md` R3b):
a **cascade** appends below what is on screen, so it suits a one-time scene whose text should build;
**node routing** swaps the passage, so it suits a repeatable act surface where the picture has to
change with the act.

⚠️ **A surface the player re-enters needs its text to VARY.**
Three of the four top
female-PC games in the corpus build every repeatable sexual surface out of such pools, and none of
them writes one as a paragraph. Two ways to do it, and they are siblings: **`block_pool` for
undirected variety** (a die), **stacked `group` bands for directed variety** (state) — DoL writes
one sentence whose first clause is his arousal and whose second is hers. `engine.md` §35 ·
`the-surfaces.md` R6 mechanism 5 · `register.md` "the two-halves sentence".

⚠️ **There is also a cap of 8 (gate 20), and it is a backstop, not a size.** A ceiling makes
"pass" and "maximise" point the same way. The field median for things-to-do-at-a-place is **3**.

## Dispatch

Resolve the game slug from the request, then read `games/<slug>/v2_state.json`. **Stop at every phase
boundary and wait for LO's pick or signature** before starting the next phase's work.

| `phase` | do this | reference | the next phase is set when |
|---|---|---|---|
| *(no state file)* | **pitch the premise** — three premises, each a different shape | `the-want.md` §0 table | LO picks one (it becomes `want.fantasy_shape`) → write the Want |
| *(no state file)*, premise picked | write the Want, create the state file | `references/the-want.md` · `templates/want.md` | the Want is recorded → `want` |
| `want` | **write the idea page** (`games/<slug>/IDEA.md`) — fantasy, promise, the people who carry it, and the first step with one person: three `v2-pitcher`s, two on the main men and one on a thread of her life, no shared context | `templates/idea.md` · `the-want.md` §0, §6 · `moment-library.md` | LO picks one; the others become later steps → `idea` |
| `idea` | **write the spine** — seven short decision pages (time, ladders, dependencies, loop, cast, media, the release page), each pointing at its rule | `references/the-spine.md` · `templates/spine/` | every page [READY] and signed, and **`shape.py <slug> --finish` passes** (checkpoint A) → `spine` |
| `spine` | lay down the world — the base — **`the-systems.md` first**, then who climbs | `references/the-systems.md` → `the-board.md` + `the-map.md` + `the-economy.md` + `the-meters.md` | the board is written → `board` |
| `board` | **the sheets** — the design LO reads and signs, before any TOML. Where LO writes them, hand drafts over in `proposals/` (S13) | `references/the-sheets.md` S13 · `templates/sheets/` | every sheet is [READY] and signed → `sheets` |
| `sheets` | build v0.1 from the signed sheets — the build | `references/the-release.md` (§ first release) + `the-voice.md` | v0.1 ships → `release` |
| `release` | run the loop — pitch, attack, write, gate, read, ship, log, and keep the prose true to the fields it quotes | `references/the-release.md` + `the-returning-player.md` | — the checkpoint is `gates.py --ship` |

**The board phase ends in SHEETS, not in TOML.** A sandbox in this engine cannot be reviewed by playing it (Ashwell 2015, on the two
patterns our games are built from: *"Reviewers may miss narrative content if exploration becomes
tedious"* and *"Reviewers struggle to assess completeness"*), so the review surface has to be
generated. `references/the-sheets.md` carries the sheet types, the `[REVIEW] → [READY] →
[GAME-READY]` workflow, and the rules — **every one of them one LO decided, or one the field
shows**.

⚠️ **Its first rule is the one the others are special cases of: a number on a sheet is a PROMISE
until an instrument produces it.** A sheet that counts paragraphs and `gates.py`, which counts
nodes, report different numbers for the same design. There is no `--sheets` mode yet, which means
every count on a sheet sits on the intent side of the measured/intent split.

**The world files, all read in the board phase — `the-systems.md` before any of them:**
**`the-systems.md` (WHAT THE GAME KEEPS TRACK OF, and what kind of place each room is — read
first, because every other file below derives from it)** · `the-board.md` (fill, meters, cast) ·
`the-map.md` (the world as a place someone could draw) · `the-surfaces.md` (which screen each
piece of content lives on) · `the-economy.md` (what money is for) · **`the-meters.md` (WHICH meters
exist and who owns them, what the climb costs, and how the player reads it off the sidebar)** ·
`the-voice.md` (how the game talks to the player about itself) · `register.md` (how the prose reads
once they click) · **`the-first-hour.md` (the opening, the first meeting with each character, and
the first visit to each place)** · **`the-clock.md` (the time the game promises and the time the
engine keeps)** · **`the-arc.md` (what happens between that first meeting and the repeatable
surface — the steps that earn it)**.

**From the second release onward, `the-returning-player.md` is not optional.** It owns what may not
CHANGE once players hold saves — ids, flag and trait keys, stat ranges, the title — against
`the-release.md`, which owns what a release has to clear before it ships. Renaming an id is invisible
to every gate in this skill and strands every save in the wild; the engine's own migration seam
(`engine.md` §40) repairs additions and nothing else.

**One optional file, read only if the game declares the system:** `the-phone.md` (whether this game
needs a phone, what goes on it, and how it is wired to the world). **Its P1 is a refusal question —
most games should not have one**, and a thinly-filled phone is worse than none. Read it before
writing `[phone]`, not after.

**Read `the-first-hour.md` before you author a single canvas.** It is the only one of these that
governs content the player meets in a fixed order, and it is the one v2 shipped without.
`templates/first-hour.toml` carries the shapes — and it is a **menu**, so delete the opening you
are not using.

**The first question about the meters — after the systems — is `the-meters.md` W1: does the PLAYER
climb or does the CAST?** The field splits 8 roster / 9 ladder with nothing between them. Declare `board.who_climbs` before naming a meter.

**The agent roster is in `references/agents.md`, and all six are BUILT** —
`v2-player` (plays the build), `v2-pitcher` (three per release, no shared context: two on the
most-owed relationships, one on a thread of her life), `v2-prose` (one beat against `gates.py --beat`), `v2-attack` (one lens per
instance, before the build; the `excitement` lens reads each pitch), `v2-listener` (loop step 8,
what players said, via `scripts/listen_mopoga.py`), `v2-reader` (the nine scene tests in
`register.md`, "What a scene contains", required on every touched canvas; its verdicts gate). The Panel has no instrument of its own (`agents.md`).
The state schema is in
`references/state.md`. Engine facts are in `references/engine.md` — and **only** there.

## The scoreboard — what fails, and where to read about it

`python3 scripts/gates.py <slug>`. **When a gate fails, look it up here.**

**The tally counts every gate that judged something**: `29/49 gates pass · 15 fail · 3 parked,
not judged · 2 too few to judge · 4 n/a`; only n/a leaves the denominator. A share (floor below
100%) passing on under 5 cases is **too few to judge**; an all-or-nothing gate passes on 3/3; a
FAIL stays a FAIL. **Parked**: `games/<slug>/parked/**/*.toml`, always read, plus the ledger's
`parked.files`, is merged into a copy and re-gated; a gate it would judge counts as not passing.
A fragment that will not parse is printed. Under `--ship` both are red. **Switched off**
(`is_active = false`, not a substitution target — `engine.md` §46.3) stays in the TOML, so the gates
also run on what actually plays: a gate that passes only with those canvases counted is a FAIL marked
**[off]**, a gate n/a only because they are off is *switched off, not judged*, and the tally line says
how many fails are [off].

| gate | what it means | where it is argued |
|---|---|---|
| location fill | the world is a distribution — one anchor, budgeted rooms | `the-board.md` §1 |
| explicit floor | enough **repeatable** beats carry real heat — the denominator is re-enterable beats, not every beat, so a well-built opening cannot drag the score down. The all-beats figure prints beside it, unjudged. | `register.md` · `gates.py` THRESHOLDS |
| explicit in repeatable | the heat is where the player returns, not sealed away | `gates.py` THRESHOLDS |
| repeatable explicit media cycles | re-entered surfaces cycle their clips instead of repeating one | `gates.py` THRESHOLDS |
| traversal heat | ~60% of destinations hold a sex scene (3+ explicit words or `_t4`/`_t5` media) | `the-board.md` §1 |
| explicit pools by place | the old heat count: cycling explicit pools | `the-board.md` §1 |
| her climb | a paid repeatable is introduced, then a step, then a first time; it is shut on a new save; each act node has two voices on a declared tier and a stop exit | `the-arc.md` A15 |
| a no has content | a `consume_on` step's exits that leave it unused park, are a labelled final, or reach a reply that changes something | `the-arc.md` A3 |
| the men's numbers are read | each trait a man keeps is shown on the cast page (hidden and counters aside) and read by a gate and a line | `the-meters.md` W1 |
| one name per trait | every trait an effect moves has a `[[traits.labels]]` label, and a sidebar item's own `label` matches it | `engine.md` §30 |
| a destination is never open and exit-only | each open hour has something to do alone, from the room's first opening | `the-board.md` §1 |
| standing surface | every schedule row has something in the room on each of its weekdays; no portrait is stranded or day-capped on its trigger | `the-board.md` §2 |
| milestones open something | a milestone that turns nothing on is a dead end. A read that is only `is_false` does not count as opening | this file, "three kinds of content" |
| ladders move forward | every step declared in `board.characters[].ladder` matches its canvas — place, hours, trigger conditions, the counter it reads (true at N−1, false at N) and sets (N), and the person is there — and every unlock on it can be earned before the step (the day roll's `traitEffects` count). The door's step skips the earnable check; a `fires_from = "opening"` step skips place, hours, person and counter read. n/a until a ladder is declared | `references/state.md` |
| meter ceiling | the top of a bar buys something | `the-board.md` §3 · `state.md` |
| ends on an opening | the release closes on the door declared in `release_page.door` (else `board.door`): locked at the start, openable later | `the-release.md` |
| the door can be seen again | the door's canvas is repeatable, or `consume_on = "exit"` with the door choice not consuming — a one-time canvas shows the door once | `the-release.md` |
| ascent tiers expand the world | your meters open content; **and no player meter quietly closes it** | `the-board.md` §3 |
| world reachable · residents have homes | the map is a place someone could draw | `the-map.md` |
| **every authored node is reachable** | no node outside a canvas's entry has zero inbound edges — a screen nothing links to is content the player can never open | `the-surfaces.md` R9 |
| **the map is a place** | a shape was CHOSEN, and the exterior is the ground rather than a room off the kitchen | `the-map.md` R0 · R3 |
| guidance exists · no chain ends in silence | the player is told where to go next | `the-voice.md` R2 |
| money gates something · sinks >= sources · no free uncapped income · a price is on its label · **the obligation is charged** | the economy can say no | `the-economy.md` |
| **she can say no** | at least one choice in the whole game DECLINES an offer — the field puts a real refusal on one click in fifty, and 79% of them lead somewhere the yes does not | `the-surfaces.md` R5b |
| **what money buys opens a door** | a thing bought with the currency that survives the night is READ somewhere — money that buys meter points buys nothing | `the-economy.md` R1b |
| a place is not a catalogue | the backstop on room size — **not** the target | `the-surfaces.md` R2 |
| **a need shuts a door** | every declared need is read by a condition — a restore that gates nothing is a chore | `the-meters.md` M8–M10 |
| a need can be met every day | each declared need has something that raises it live on every weekday — its trigger's days, narrowed by the place's `hours` | `the-meters.md` M8–M10 |
| **the walk-in floor** | a room where she works alone with someone scheduled carries a walk-in | `the-surfaces.md` R3 |
| **an explicit beat carries a clip** | the picture is on the beat the player is reading, not on the one above it | `register.md` S1 · `engine.md` §8 |
| **somebody speaks** | the game is not all narration — field median 2.93:1 | `register.md` S3 |
| **speakers are named** | every `dialog`/`thought_bubble` says whose it is | `engine.md` §25 |
| **effects use a live op** | no effect uses an `op` the engine silently discards | `engine.md` §21b |
| **the climb is paid for** | every meter a gate reads has a brake on the rungs that raise it | `the-meters.md` M1–M5 |
| **a day-cap closes** | every flag read `is_false` and cleared in `[engine.daily_tick]` is SET somewhere — a cap with two of its three parts validates and throttles nothing | `the-meters.md` M5 · `engine.md` §28.2 |
| **a spent day still has a door** | no screen whose every choice is day-capped or priced lacks one choice free of **both** `conditions` and `costs` — a spent cap renders nothing at all, not a greyed line | `the-surfaces.md` R7 · `engine.md` §28.3 |
| **a locked door says why** | a pure number lock shows the engine's need and no `locked_text` (doubled, J1); a story lock, mixed ones included, carries a `locked_text`, a threshold or a rejection node, and is never doubled. 2% of the field ships a dead greyed label | `the-surfaces.md` R5c · `engine.md` §15 · §36 |
| **a goal says what it wants** | every quest-card goal bullet renders WORDS, not a raw key. The goal renderer falls back `label → trait → flag` (`engine.md` §44), so a flag goal with no `label` prints `step_05_done` to the player under 🎯 To advance. The importer requires `label` on trait and counter goals only, so flag goals fall straight through; trait goals are already safe and already print `label — current / target`. Invents no threshold — a card is compared against its own declared goals | `the-voice.md` R3 · `engine.md` §47 |
| **a meter is read** | every number the game raises is read by a condition, a cost or a quest goal — a raise with no reader is decoration | `the-meters.md` W3 |
| **the wardrobe is read** | a game declaring `[[clothing]]` reads it somewhere — she can dress and the world does not look | `the-meters.md` W3 · W7 · `engine.md` §17 |
| **a declared garment can be got** | every `[[clothing]]` entry has a route into the wardrobe — `initial`, a shop purchase (`v2.py:2077` lists only a non-`initial` garment with `price > 0`), or `wardrobeEffects`. A garment with no route is dead, and so is every condition that reads a property only it carries — an arc step gated on wearing it can never be entered | `the-meters.md` W3 · `engine.md` §17 |
| **the climb is where you said it is** | the game gates where `board.who_climbs` says it does | `the-meters.md` W1 · `state.md` |
| **a banded meter is shown once** | a banded sidebar stat is `in_dump = false` in `[[traits.labels]]`, and its item prints the number (`trait_words` + `show_value`, or `trait_bar`) | `the-meters.md` M7 · `engine.md` §30 |
| **the opening opens a door** | the funnel's last click lands on a clock time when something at that location is actually open | `the-first-hour.md` F3 |
| **every hub is met first** | no character's portrait is live before a meeting has fired; a flag set by a scene that meets nobody opens nobody's hub | `the-first-hour.md` F5 · F8 |
| **a meeting fires where they are** | a one-shot naming a character carries a `trigger.schedules` window matching that character's own hours — `requires_npc` does not gate the auto-fire path, so without one the introduction plays to an empty room | `the-first-hour.md` F5 · `engine.md` §31 |
| **no canvas key is discarded** | every key on a `[[canvases]]` table is one of the seven `TemplateCanvas` reads. Anything else — a **trigger** key written one level too high, `npc` or `substitution_only` — is dropped silently, and the TOML still says what the author meant. Invents no threshold and cannot false-positive: a key outside the seven does nothing on any path | `the-first-hour.md` F5b · `engine.md` §42 |
| **the start choice is read** | a choice the opening asks the player to make is read by real content later — fails only on ZERO, and a game that asks nothing reports n/a, which is not a pass | `the-want.md` §1 · `state.md` |
| **what she picks is read** | every `[[player.customization_fields]]` value is printed somewhere — `$player.<id>` or the `@player.<id>` token — fails only on ZERO, `sets_portrait` counts as a read, and a game declaring no customization reports n/a, which is not a pass | `the-want.md` §1 W1 |
| **the label keeps its time** | no button promises a clock time the engine cannot reach, and a stated duration is the real spend | `the-clock.md` C3 · C4 |
| **the price is in one currency** | every notation on a button, plus the engine's own `currency_symbol`, resolves to ONE currency | `the-economy.md` R7 · `engine.md` §33 |
| sentence length | the prose has not drifted dense | `register.md` |
| prose has room | the first floor under the writing: `but` ≥ 2.88 per 1,000 words (field p10) and `and` ≤ 41.1 (field max) — compressed prose drops its joints | `register.md` — "Joints" |
| prose texture | the dash rate against the field — p50 0.99, p90 17.5, ceiling 35.0/10k. The other three texture figures print and are **not** judged | `register.md` — "Dashes stay rare" |

Lints sit below the tally and never move it: dialogue attribution · **the labels and the systems
agree** (`the-systems.md` SY1–SY3 — every declared system against every room label: a label no
system claims, a system whose label is on no room, and a `sourced` system that is not fed where it
says or is read nowhere else. ⚠️ Declaring more labels makes it worse, not better, which is the only
reason it is checked; a count that can be optimised upward is the `objects`/gate-22 failure) ·
room-list labels ·
the browse share · screen shape · the prose names places the map does not have ·
**the guidance page says nothing** (`the-voice.md` R3 — every quest card that renders its
flavour text and then nothing at all: no `goals`, no `ready_canvas`, not `terminal`, which makes
the goal renderer return an empty string. ⚠️ A LINT because the engine's own comment calls that
shape intentional for transitional cards between capstones, so one mute card cannot be a defect;
the row worth reading is a character **all** of whose cards are mute, whose section of the page
therefore never says what to do. That is the corpus's most-punished failure — `in-her-own-hands`
ships 136 passages for one character behind hints reading *"complete another task"*, and its
players quote the text back at it) ·
**a door opens onto something** (`the-map.md` R6–R6c — every `[locations.door]`: one no option
can ever open, one whose only option is `enter` (a room with an extra click), a knock gated on
somebody no schedule puts there, and a door on a room the whole cast passes through. ⚠️ Silent
on a game that declares no door, because a door is meant to be RARE — six in a 15,626-passage
game — and declaring another makes this worse, not better) · **the ladder**
(where a scene starts and stops on it) · **talk screens** · **the act menu** · **the meter ladder**
(rungs per tier, and where the lowest one sits) · **the cast's meters** · **the counterweight** ·
**the words the player has to already own** (every word in the player's face that fewer than four
of the 27 field games use — **prose, choice labels AND location names**, because a word the player
cannot decode is undecodable on a button too; a list to read, never a score) · **dispatch depth** (how many different
things one activity can turn into, and how often the activity itself still renders) ·
**the act nodes** (body words on the thinnest band each act and finish node can render) ·
**the sentence explains itself** (every
`, which is` / `, which means` — a fact welded to a gloss of the fact; field MAX 0.24 per 1,000
words over 27 games) · **what did not
happen** (the share of sentences whose claim is a negation, and every canvas over the field's
maximum of 25.76% — narration-only baseline. ⚠️ A measurement only (`register.md` L2),
because the loud voice negates on purpose) · **history on a repeatable screen** (backstory on a canvas the player
re-enters — `is_repeatable` only, because a one-time canvas is where the doctrine says to PUT it;
elapsed time, NOT clock time, which is `the-clock.md` C2) · **a repeatable claims a past**
(*last night · yesterday · this week · again · every time* on a repeatable canvas, outside a `group`
gated on the flag that records it — the truth rule's rule 2, `register.md`) · **a printed stat is
real** (every `+X` / `−X Name` in prose or a button whose name is no declared trait or flag —
`the-meters.md`, "What the player is shown") · **a one-time step speaks** (every one-time
canvas bound to a person with no `dialog` block in it) · **the arc ladder** (per person: one-time steps written, how many switched off, and the longest
chain where each step reads what the one before sets; `the-arc.md` A1) · **a scene ends on nothing** (a one-time
scene with a person and no choice anywhere, so its hook must be its last line) · **a person who never
speaks** (a repeatable scene bound to a person who has no line in it) · **thoughts outweigh speech** (every canvas
bound to a person where `thought_bubble` words outnumber spoken ones — the voice's rule 3, thoughts
beside dialogue, never instead) · **the opening arms a card with goals** (`the-first-hour.md` F1b —
the cards visible once the opening hands over, and whether any carries `goals`) · **named before met** (every character
named before the game has introduced them) · **she permits or she acts** (the share of
choices that open `let` — the act on the button against the act in the prose; `the-voice.md` R6) · **the place says what it is** (every location by how
much prose happens there against how long its own description is — read whether each one names the
FUNCTION, which is what replaced the gate that required a first-visit canvas) ·
**the clock in the prose** (every hour a beat names, with the window it has to survive) ·
**the time cost is not on the button** (every click that moves the clock an hour or more in
silence) · **the currency in the prose** (every line that names a currency other than the game's
own, and whether the rent pages agree with it) · **the price is spelled out** (the form of every
priced label against the field's 94% symbol) · **money gates content, or only prices it** (a
CONDITION on the currency means content money opens; a `costs` block only means a thing can be
bought, and gate 16 passes on either) · **the obligation against the week** (`obligation_amount`
over the declared `week_income` — a figure, never a score) · **the collector is also the target**
(who enforces the hold, against who owns the explicit repeatable surfaces — a RANK, never a score.
The field's collector carries 0.4–3.8% of a game's explicit passages and is never the top figure;
`the-want.md` §4a) · **what a paid repeatable leaves
behind** (how many surfaces she pays for deposit anything; a pure sink is not a defect, a game made
only of pure sinks is) · **repeatables without a step** (repeatables added since the last
`releases[]` entry when no declared ladder step was added — a LIST, never a score; a first release
prints its baseline) · **a flag that never resets** (a `*_today`/`*_week` flag, or one in
`board.resetting_flags`, set somewhere and unset nowhere — not even `[engine.daily_tick]`; a LIST) · **a cheat page exists** (which of the four `the-systems.md` SY7 basics are free, and any time-saver sold behind a code; a LIST) · **toggles declared** (each `want.toggles` flag and how many canvases read it; n/a when none is declared; a LIST — `the-surfaces.md` R5b.4) · **how much explicit content is in here** (the ABSOLUTE count and the rate
per 1,000 words against the field's 1.24 — every other heat check is a share with a hand-picked
denominator; reads the built HTML
on the field's own word list, and prints both the matched and the generous basis) · **the ambient
puts him in the room** · **the label under the name** (`npcs[].role` — the 1-3 word label the engine
prints under the name in EVERY dialogue box, against `relationship`, which is the cast page's
sentence and renders nowhere else. Absent is legal; the lint exists because the field was invisible
rather than declined — 6 of 88 characters in 17 games, all six in one game) · **bound to a person, no face** (every repeatable canvas that names a
character via `requires_npc` and carries no `trigger.npc` — it renders as a link, not a portrait,
and has no presence check at all. A list because an activity that happens in a place while somebody
is around is a legitimate shape; the hard version of the failure is the gate above) ·
**a token the engine never resolves** (`@player` / `@npc` in any field the engine emits verbatim,
nested lists included; `engine.md` §43 has the table. A player-facing one is the `--ship` BLOCK row
*no raw token on screen*) · **the joints** (the coordination ratio, `, which is` glosses, the
shortest-sentence screens) · **adjacent groups** (dead `group` blocks) · **a pronoun with nobody to point at** · **a past event the player
was never given** · **short lines with no verb** (the last three from `scripts/readable.py`) · **the badge arrives before the
content** · **the role stays attached** · **which refusals are
shown at all** · **the act between the click and the number** (`the-surfaces.md` R9 — location
exits that fire effects and show no screen, with the game-time they burn. A LIST: the field runs
0-68%, so any threshold would fail a game for obeying the doctrine).

## Protected — do not regress

Each of these is taught in one place and holds up much of the rest. Change one only as its own item,
with LO's yes — never as a side effect of another edit. *(LO decided.)*

- **The arc** — `references/the-arc.md` A1–A14: numbered one-time steps that convert into a loop.
- **The world reacts** — `the-meters.md` W5b (who knows about her) and W8 (what sticks);
  `register.md`, "What a scene contains", test 5 (who notices).
- **Doors close out loud** — `the-want.md` §1, `the-arc.md` A3, `the-meters.md` W8.
- **The hold kinds** — `the-want.md` §1b.
- **The meter stops at each step** — `the-meters.md` M1–M5; gate `the climb is paid for`.
- **The money file** — `references/the-economy.md`.
- **One-table schedules** — `the-sheets.md` S5.
- **The staged opening** — `the-first-hour.md` F1b.
- **The loud voice and the truth rule** — `register.md`, "The voice — say it loud" and "The truth rule".
- **Stop and ask; an approved plan lives in the game's pages** — `the-sheets.md` S12, S13.
- **The tools** — the scripts in `scripts/`, above all `gates.py` and `shape.py`.

## Operating rules

- **What may enter this skill.** *(LO decided.)* An engine fact revealed by a game bug may enter the
  skill; a craft rule needs field evidence or LO's decision. Skill changes land between releases, not
  in the middle of one.

- **The register is the loud voice, the opening is the staged shape, and the truth rule covers
  every screen.** Since 2026-09-24: story text says it, spells out the feeling, puts people talking
  on screen and her thoughts beside them (`references/register.md`, "The voice — say it loud");
  the opening runs setup → problem → person → conflict → choice → temptation → objective → play
  (`references/the-first-hour.md` F1b); and every claim a screen makes is true on every visit it can
  render on (`references/register.md`, "The truth rule"). Labels and guidance stay plain
  (`references/the-voice.md`).

- **When this skill and a game's sheets disagree, stop and ask.** A fact on a sheet holds; a design
  choice on a sheet that clashes with a rule here is a question for the owner, asked before building,
  never settled quietly and never only noted afterwards (`the-sheets.md` S12). **And an approved plan
  goes onto the game's pages before it is built** (S13): a plan kept outside `games/<slug>/` is one
  the next session will not read.

- **A number is a promise until an instrument produces it.** `the-sheets.md` S1. A sheet that
  counts paragraphs and `gates.py`, which counts nodes, disagree about the same design. Anything not emitted by `gates.py`, `playtest.py` or a build belongs on the INTENT
  side of a summary, however carefully it was counted.
- **Parse, never grep.** Game state is TOML; read it with a parser, never grep. *(LO decided.)* The
  same discipline applies to every claim: measure it, don't eyeball it.
- **Every engine claim carries a `file:line`.** If `references/engine.md` doesn't have it,
  go read `apps/game_generation/twee_comprehensive/generators/v2.py` and add it with its
  citation. Never assert engine behaviour from memory.
- **Ship on `--ship`.** `python3 scripts/gates.py --ship <slug>` decides whether a build may reach a
  player, and it is the one mode wired to stop a publish: `scripts/release_upload.py` refuses to
  package on a red, and `scripts/hooks/pre-commit` refuses to commit a non-dev portal build of a
  v2 game. It **BLOCKS** only what makes a build broken, unfinishable
  or untrue — no past claim on a repeatable · a printed stat is real (only an unreal `+X` blocks) · no raw token on screen · a one-time step with a person
  speaks · the opening's card has goals · each step fires when unlocked, and each unlock is
  earnable (every person on the release page has a declared ladder, it passes *ladders move
  forward*, and `playtest.reach_step` climbs it in the build — the clock and place are set per
  step, the counter never is) · LO signed the playtest (`release_page.signed_by_lo`) · the build
  exists and is a release build (`--release`) · the last release's saves load (`--saves`) · the
  declared door works · the pressure can be paid or is signposted · no empty rooms (+ exit-only) · the build
  matches the release page · the reader passed (each touched canvas with a named person or an explicit beat has verdicts; a FAIL needs a waiver — `the-release.md` 6b). **Everything else is REPORTED** for LO to judge when he plays —
  dialogue share, every hub met first, clips on explicit beats, the explicit floor, location fill,
  the walk-in floor, traversal heat, explicit pools by place, sentence length, a card per ladder step that says where and
  when, and every other gate. `gates.py <slug>` still
  prints the whole scoreboard; a red there is a real defect or a wrong threshold, and it is fixed at
  the layer that caused it, never skipped. `the-release.md` § Shipping the build.
- **The scoreboard has three other modes, and each answers something `<slug>` cannot.**

  | | |
  |---|---|
  | `gates.py --words <path>` | the vocabulary lint on any text file — run it on the WANT and the BOARD, while the nouns are still being *chosen*. Run on a built game it is one phase too late: every noun is already a room name and a button. Always exits 0; it is a list, never a score. |
  | `gates.py --beat <path>` | **the only mode that measures prose not yet in a game.** Blank-line separated blocks are beats. Reports the explicit count against the 3+ the `explicit floor` gate uses, median sentence against the 14 ceiling, dash rate, which act rungs the text names, the joints (`but` and `and` per 1,000 against the field figures `prose has room` uses — printed, and "too short to judge" under 500 words), and **where the body words fall across the sentences** — the pivot as a shape, because `register.md`'s rule is a reading test and no regex decides what a sentence is *about*. Every threshold is one this script already used; none is new, so the Prose Maker cannot optimise for a private scale the build never checks. ⚠️ **No verdict on length**: `register.md "S1 · The clip rides the beat"`'s 37 words is per *screen*, and a non-cascade node is one `Beat` here that can hold several. Always exits 0 — a paragraph outside its canvas cannot be failed. |
  | `gates.py --release <slug>` | the **artefact**, not the source. Every gate above reads `7_final_game.toml` and none of them can see a build. Seven checks, off for every ordinary run, **exits non-zero**. One of them, `every canvas is a passage`, is the only thing in the skill that can see a canvas the generator DROPPED: two consecutive games shipped their act loops written and absent, with 46 green gates over them, because gates parse the source and reachability is decided at build time (`defects/001`). `the-release.md` § Shipping the build. |
  | `gates.py --saves <slug> [<ver> [<ver>]]` | **the only check that reads TWO releases.** Every other check here reads one snapshot, and a save break does not exist in a snapshot — renaming a canvas id produces a game that is correct on its own terms and strands every player holding a save. Diffs the current build's join keys (passage names, `$npcs` keys, flag keys, player and NPC meter keys, the story title) against the newest archived release; additions are counted and never judged, because the migration seam reaches them (`engine.md` §40). Needs `releases/v<version>.html` to exist — without an archive it cannot run. **Exits non-zero.** ⚠️ A rescaled stat and a burned one-shot grant are invisible to it and stay human: `the-returning-player.md` §4 and §6. |
  | `gates.py --ship <slug>` | **may this build reach a player?** The BLOCK list above, then the REPORT list. Calls `--release` and `--saves` rather than re-implementing them. **Exits non-zero on any red BLOCK row** — the only mode wired into publishing (`release_upload.py`, the pre-commit hook). |
  | `gates.py --selfcheck` | does this file still document every gate and lint the script emits, does every rule the references POINT AT actually exist, and does any doc hand-write a gate or lint count that has gone stale? Needs no game. Docs point here for the counts rather than writing them. A qualified pointer at a rule with no section FAILS, while a bare in-file reference is listed to eyeball and never scored, because a withdrawn rule discussed as history is correct prose. |
  | `shape.py <slug>` | **checkpoint A** — do the spine's decisions hold together? Reads the ledger only: this release's places, hours and traits a step names, dependencies, the pressure sums (a rising bill walked by stage), a ladder per release person, a hint per step, the door, the promise's beat, the goal chain (no date; a goal that ends names `next`), every READY SP page signed, the person is there at the step's hour (`board.characters[].schedule`), a step's gate can be reached from the `raises` before it, and every person is 18+ (`want.cast[].age`, FAILS in every mode); a person's meter written as a bare string WARNS (`{type, min, max}`). Lenient while the spine is written; **strict** with `--finish` or once the phase is `spine` or later, where a missing piece FAILS. Flags in a gate are listed, not judged. `--ship` prints it as a REPORT row. `the-spine.md` |
- **`scripts/playtest.py <slug>` plays the build.** Every gate above reads the source; this drives
  the running game in a browser and is the only place some defects exist at all. It is also what the `v2-player` agent runs.
  ⚠️ **A red is a hypothesis until its cause is quoted as `file:line`**: three of this harness's own
  first four reds were the harness, not the game. `references/agents.md`, The Player.
- **`scripts/guidance_from_ladder.py <slug> --out <scratch>` writes a person's quest cards from
  their ladder**, one per step with place and window, for the author to fill in (`the-voice.md` R2). It never writes into `games/`.
- **`scripts/pitch_pack.py <slug> --person <npc> --kind <moment_kind>` is the world a Pitcher may
  pitch into.** It opens with the promise, the moment kinds already shipped, that kind's slice of
  `references/moment-library.md`, the clips on disk, and RELATIONSHIPS — each person's steps so far,
  what they set and whether anything reads it, sorted by who is most owed — and THREADS, her life
  (`--thread <id>` for the third Pitcher). The loop (`the-release.md` step 2)
  runs three Pitchers with **no shared context** — that is the design, and its unpaid cost is that
  a Pitcher with no context does not know what the game already contains and will name a location
  that exists or a character who does not. The pack is that context, generated instead of
  remembered: places, people, the meters and flags a pitch can key to, the money, the Want
  verbatim, what already shipped, and which promises are still open. It is what the `v2-pitcher`
  agent reads first. **It scores nothing and always exits 0** — same rule as `--words`, and for a
  harder reason: *"this location is too thin"* is an opinion. With no TOML it reads the ledger, `WANT.md`
  and `IDEA.md`; only releases with a `shipped` date count.
- **An example outranks every rule beside it, so it goes in LAST — after it is validated, or not
  at all.** *(LO decided.)* A rule is read; an example is copied. Where a shape has to be taught, teach a
  **menu the author must choose from**, never one picture they can copy. If a validated example is
  ever promoted, it is **one per option or none** — a single good example is still one picture,
  copied just the same. *(Every other reference file carrying a worked example has the same
  exposure; that audit is open.)*
- **The examples are also the REGISTER, not just the shape.** Same rule, applied to words: an
  example's vocabulary is copied along with its shape, so an example written in a dialect teaches
  that dialect. **Every word in an example is being taught too.** *(LO decided.)* The field runs
  locale-locked nouns at **0.8 per 10,000 words**; `references/register.md`, "The words the player
  has to already own".
- **A shape that ships in `templates/` is copied harder than one that ships in `references/`.** A
  reference file is read; a template is *filled in*, so whatever is already sitting in the slot is
  the answer unless the author actively fights it. A band table in a template becomes the declared
  tiers, whatever the field runs (8–17 rungs starting at ~5). This is the "an example outranks every
  rule" rule one level worse: in a template, even a *placeholder list* is an example. Ship a menu the
  author must cut down, never a set they can keep. *(LO decided.)*
- **Ask what a tired author would build to satisfy a check, and make sure that is the thing you
  want.** A check does not measure quality; it **manufactures** whatever it can see. `objects` /
  gate 22 forced duplicate room screens into existence, because it computed affordances from
  `exit_block.choices` and could not see a canvas at all — so an entire canvas about one object
  counted as zero, and the only way to pass was a second screen
  re-listing what was already there. That is worse than no check, because it ships green. It was
  replaced by `the-surfaces.md` R2: a room's list is **needs + work +
  people**, a CLOSED set that sizes itself, instead of objects, an OPEN one that never can.
- **An instrument that cannot see a thing reports its ABSENCE, not its rarity.** Before a
  measurement is allowed to retire a rule, ask what the measurement is blind to. v1's dialogue rule
  was dropped because a field study counted speech by looking for `"quote marks"` and found a
  median of 33:1 — but 20 of 27 games render speech as a UI component (`<<speech>>`, `<<nm>>`, a
  chat bubble, one macro per character), so the instrument read the most spoken game in the corpus
  as **585:1 narration**. Re-measured with each game's own convention: median **2.93:1**, ten games
  under 2:1. The two games the study named as the dialogue-heavy outliers were simply the two whose
  dialogue it could see. Same failure family as gate 22 above, one level up: there, a check could
  not see a canvas; here, a study could not see a sentence.
- **A check that measures EXISTENCE has not measured anything.** Every defect found on
  2026-08-16 had passed a gate that asked whether a thing was present, when the question was
  *how much of it there was* or *what it cost*. `ends on an opening` was `locked > 0`, so a single
  locked choice passed it. `ascent tiers expand the world` tests
  direction only, so a tier gating 4 choices scores like a tier gating 40. The media gates report
  100% coverage against pools with zero files behind them. **Every check either carries a
  denominator or prints its magnitude beside the verdict** — and where a threshold cannot be
  honestly set, print the number and demote it to a lint rather than inventing one.
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
- **A note written by the agent that did the work is a CLAIM, not a fact.** Session notes, handback
  summaries, a game's own `ENGINE_NOTES.md` — verify each line against source with a `file:line`
  before it is promoted into a reference file. Measured: six such claims were checked, **five held,
  one was a tooling note misfiled as engine behaviour**, and the check also exposed an error in a
  reference section written that same day from the same function. Trusting the handback would have
  put both into doctrine.
- **When a gate you just wrote fails a game, check the skill before blaming the game.** A gate
  built for locked doors fired on games that were following `engine.md` §15 correctly. A check that fails a game for obeying the doctrine is a bug in the check. Measured
  again 2026-08-16: gate 24 failed a game whose obligation *was* charged, because the gate walked
  canvases and the charge lived in `[settings.rent]`.
- **A vocabulary the engine does not recognise fails SILENTLY, and nothing else in this system
  does.** `op = "subtract"` is not an engine op — `applyTraitEffect` runs `add` and `set` and
  returns on anything else (`v2.py:6245-6251`). This skill's own `engine.md` once discussed the op
  as though it worked. Valid TOML, green
  build, green gates, and a clean play-through, because **a number that never changes looks exactly
  like a number the player has not moved yet.** When you write an unfamiliar key or value, find the
  line that consumes it before you write a hundred of them. Gate 25 and the importer now both
  refuse it; the next one of these has no gate yet.
- **Twice now, the missing feature was already built.** `block_pool` (§35) and `rejection_node`
  (§36) are both fully wired in the engine, and nothing here wrote them down. The tell is
  identical each time: a rule that says *"our games do the opposite"* and offers no mechanism.
  **When you catch yourself about to say the engine cannot do something, grep
  `template_import.py`'s dataclasses first** — the field's mechanism is often already sitting there
  unused.
- **Differentiation is many small swaps, not a few large branches.** Two sections measured this
  independently and landed in the same place. Section H: reputation is read in one-line swaps,
  median **139** characters (degrees-of-lewdity) and **84** (zaras-school-life). Section G:
  personality is read the same way — **896** `if` branches gated on an inclination in
  course-of-temptation, median **114** characters, deciles 30/37/50/72/**114**/153/204/284/448.
  Roughly twenty words. One sentence, swapped. **When a system feels like it needs a big branch per
  state, the field's answer is almost always a small branch per site instead.**
- **A system is read to change the words, not to refuse the action.** The same law, arriving a fourth
  time from a fourth instrument. Section H: reputation gates **2%** of its 644 read sites and colours
  the other 98% — ⚠️ *corrected 2026-08-27: that is three games, 95% of it degrees-of-lewdity. Over
  13 games it is ~10% link-bearing, and a median 41% of reads change something mechanical without
  ever refusing. The law survives; "colours" must not be read as "does nothing." See W5b.* Section G: differentiation is many small swaps, above. Section I: the body —
  clothes, arousal, hygiene, pregnancy — gates a median **10%** across 25 measured systems, 17 of
  them under 25%. Section B reaches it from the *choice* side rather than the meter side: of **27,505**
  conditionals wrapped around an action, **35% are variant selectors where every branch offers
  something** and only **23% refuse anything at all**. The exceptions are all *small* systems, which is the rule underneath it:
  **a system either stays small and gates, or grows large and colours; nothing in the field is
  both.** When you are designing a meter and reaching for gates, you are probably building the
  wrong kind (`the-meters.md` W7).
- **A per-NPC field has TWO write sites and the default build uses the second.**
  `template_import.create_project_from_template` is the `--use-db` path; `game_graph.build_game_graph`
  is the one a plain `package_from_toml` takes. Add a field to only the first and it reaches the
  database and never reaches a game, silently, with no error at import, build or runtime
  (`engine.md` §34).
- **An explicit beat stays on the body for its whole length** — `references/register.md`. If the
  beat's last sentence is about what it *means* rather than what is *happening*, it has pivoted
  and will fail the floor. Assume you are doing it.

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
