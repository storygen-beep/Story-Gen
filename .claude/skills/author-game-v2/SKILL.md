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

## The fifth commitment — the machinery colours far more than it locks

Added 2026-08-24, and it is the one thing eleven field-study sections agree on without any of
them saying it. Each measured a different subsystem and each came back with the same answer:

```
reputation refuses                ~10% of branch arms (13 games)          the-meters.md W5b
the body refuses          median  10%  of its reads                       the-meters.md W7
her willingness gates              6%  of act links                       the-meters.md W6
act links with no gate at all     47%  of 7,598                           the-surfaces.md R3b
refusals that render nothing      71%  of 16,167                          the-surfaces.md R5c
conditionals around an action     35%  select a variant · 23% refuse      the-surfaces.md R5
```

⚠️ **Colours-more-than-it-locks is not decides-nothing.** The reputation row was `2% of 644 read
sites` until 2026-08-27; that figure was three games with 95% of it in one, and it taught
`mrs_vance` to build a meter written 25 times and read 4. Re-measured over 13 games, a **median
41% of reputation reads change something mechanical** — by delivering a person, modifying a roll
or scaling a rate, none of which prints a refusal. Read `the-meters.md` W5b before using this row.

**A meter's main job in this genre is to select text, not to bar a door.** Reputation does not stop
her walking into the bar — it changes what the barman says. The body does not lock the room — it
changes the sentence. The lock is the exception, and it is the *cheap* half: it costs one condition
and buys one refusal, where the same meter read as a colour buys a different line on every visit
forever.

⚠️ **Ours have been built the other way round, and it is measurable.** Every condition in our
21 scorable games, against every condition in the 26-game field, on one instrument
(`findings_K_mirror.md` §2):

| | field | ours |
|---|---|---|
| **equality** — which step are you on | **53%** | **4.5%** |
| **threshold** — is your number big enough | 31% | **56%** |
| boolean — is this switch on | 9% | **37%** |

Threshold and boolean are both locks. Two things already known separately fall straight out of it:
**gate 42 exists** because our locked doors are mute, and **`block_pool` — the primitive for writing
many versions of one line — is documented in four places and used by zero v2 games.**

**What to do with it.** Before adding a condition, ask which of the two it is. If the answer is
*"it stops her"*, ask what the other branch says, because the field would usually have written one
(`the-surfaces.md` R5 and R5d, `the-meters.md` W5b). **This is a frame, not a quota** — no section
measured a defensible ratio and nothing here is gated.

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
his** (Dr. Angela has the clinic; Dean Mea has the school; Romi has the shop and Ell and Gigi), and
by **a place and an hour where he is the only one there**. Write five good voices and then schedule
all five into the same room every evening and the player still cannot tell them apart — which is
exactly what `the_season` did (`the-surfaces.md` R8, `register.md` S3, `the-meters.md` W6).

⚠️ **This used to say "declare the objects in the room and hang every choice on one" and it was
wrong** — deleted 2026-08-18 along with gate 22. See the operating rule about tired authors below.

**A canvas advances in one of two ways, and the content kind picks which** (`the-surfaces.md` R3b):
a **cascade** appends below what is on screen, so it suits a one-time scene whose text should build;
**node routing** swaps the passage, so it suits a repeatable act surface where the picture has to
change with the act.

⚠️ **A surface the player re-enters needs its text to VARY, and no v2 game has ever made it.**
Counted across every `toml_phases/*.toml` here: `block_pool` — which picks a different one of N
blocks on every render — runs **46 times in the_long_summer, 14 in under_one_roof, 6 in vesper, and
0 times in every v2 game.** v1 had a numbered rule for it; v2 lost it in the divorce from the old
corpus (`engine.md` §35). Three of the four top
female-PC games in the corpus build every repeatable sexual surface out of such pools, and none of
them writes one as a paragraph. Two ways to do it, and they are siblings: **`block_pool` for
undirected variety** (a die), **stacked `group` bands for directed variety** (state) — DoL writes
one sentence whose first clause is his arousal and whose second is hers. `engine.md` §35 ·
`the-surfaces.md` R6 mechanism 5 · `register.md` "the two-halves sentence".

⚠️ **There is also a cap of 8 (gate 20), and it is a backstop, not a size.** Two games prove why it
must be read that way: one shipped 23 choices on a front desk and scored 18/18 because nothing said a
location page had a shape — and the game built *after* the cap existed put 19 of its 30 screens at
exactly 8, shipping the same 213 total choices as the first. A ceiling makes "pass" and "maximise"
point the same way. The field median for things-to-do-at-a-place is **3**.

## Dispatch

Resolve the game slug from the request, then read `games/<slug>/v2_state.json`:

| `phase` | do this | reference |
|---|---|---|
| *(no state file)* | write the Want, create the state file | `references/the-want.md` |
| `want` | lay down the world | `references/the-board.md` + `the-map.md` + `the-economy.md` + `the-meters.md` |
| `board` | build v0.1 | `references/the-release.md` (§ first release) + `the-voice.md` |
| `release` | run the loop — pitch, attack, write, gate, ship, log, and keep the prose true to the fields it quotes | `references/the-release.md` + `the-returning-player.md` |

**The world files, all read in the board phase:** `the-board.md` (fill, meters, cast) ·
`the-map.md` (the world as a place someone could draw) · `the-surfaces.md` (which screen each
piece of content lives on) · `the-economy.md` (what money is for) · **`the-meters.md` (WHICH meters
exist and who owns them, what the climb costs, and how the player reads it off the sidebar)** ·
`the-voice.md` (how the game talks to the player about itself) · `register.md` (how the prose reads
once they click) · **`the-first-hour.md` (the opening, the first meeting with each character, and
the first visit to each place)** · **`the-clock.md` (the time the game promises and the time the
engine keeps)**.

**From the second release onward, `the-returning-player.md` is not optional.** It owns what may not
CHANGE once players hold saves — ids, flag and trait keys, stat ranges, the title — against
`the-release.md`, which owns what a release has to clear before it ships. Renaming an id is invisible
to every gate in this skill and strands every save in the wild; the engine's own migration seam
(`engine.md` §40) repairs additions and nothing else. v2 shipped without this file entirely until
2026-08-29.

**One optional file, read only if the game declares the system:** `the-phone.md` (whether this game
needs a phone, what goes on it, and how it is wired to the world). **Its P1 is a refusal question —
most games should not have one**, and a thinly-filled phone is worse than none. Read it before
writing `[phone]`, not after.

**Read `the-first-hour.md` before you author a single canvas.** It is the only one of these that
governs content the player meets in a fixed order, and it is the one v2 shipped without: all six v2
games put their entire cast in a room with no introduction, against four v1 games that did not.
`templates/first-hour.toml` carries the shapes — and it is a **menu**, so delete the opening you
are not using.

**The first question of the board phase is `the-meters.md` W1 — does the PLAYER climb or does the
CAST?** The field splits 8 roster / 9 ladder with nothing between them, and all five v2 games landed
in the empty middle because nobody asked. Declare `board.who_climbs` before naming a meter.

The agent roster for each phase is in `references/agents.md`. The state schema is in
`references/state.md`. Engine facts are in `references/engine.md` — and **only** there.

## The scoreboard — what fails, and where to read about it

`python3 scripts/gates.py <slug>`. **When a gate fails, look it up here.** Nine of these used to be
documented nowhere but in the script's own comments, so an author who hit one had nothing to read.

| gate | what it means | where it is argued |
|---|---|---|
| location fill | the world is a distribution — one anchor, budgeted rooms | `the-board.md` §1 |
| explicit floor | enough beats carry real heat | `register.md` · `gates.py` THRESHOLDS |
| explicit in repeatable | the heat is where the player returns, not sealed away | `gates.py` THRESHOLDS |
| repeatable explicit media cycles | re-entered surfaces cycle their clips instead of repeating one | `gates.py` THRESHOLDS |
| traversal heat | most locations carry something, not just the one hot room | `the-board.md` §1 |
| standing surface | every character is findable and scheduled | `the-board.md` §2 |
| milestones open something | a milestone that turns nothing on is a dead end | this file, "three kinds of content" |
| meter ceiling | the top of a bar buys something | `the-board.md` §3 · `state.md` |
| ends on an opening | the release closes on a visible locked door | `the-release.md` |
| ascent tiers expand the world | your meters open content; **and no player meter quietly closes it** | `the-board.md` §3 |
| world reachable · residents have homes | the map is a place someone could draw | `the-map.md` |
| **the map is a place** | a shape was CHOSEN, and the exterior is the ground rather than a room off the kitchen | `the-map.md` R0 · R3 |
| guidance exists · no chain ends in silence | the player is told where to go next | `the-voice.md` R2 |
| money gates something · sinks >= sources · no free uncapped income · a price is on its label · **the obligation is charged** | the economy can say no | `the-economy.md` |
| **she can say no** | at least one choice in the whole game DECLINES an offer — the field puts a real refusal on one click in fifty, and 79% of them lead somewhere the yes does not | `the-surfaces.md` R5b |
| **what money buys opens a door** | a thing bought with the currency that survives the night is READ somewhere — money that buys meter points buys nothing | `the-economy.md` R1b |
| a place is not a catalogue | the backstop on room size — **not** the target | `the-surfaces.md` R2 |
| **a need shuts a door** | every declared need is read by a condition — a restore that gates nothing is a chore | `the-meters.md` M8–M10 |
| **the walk-in floor** | a room where she works alone with someone scheduled carries a walk-in | `the-surfaces.md` R3 |
| **an explicit beat carries a clip** | the picture is on the beat the player is reading, not on the one above it | `register.md` S1 · `engine.md` §8 |
| **somebody speaks** | the game is not all narration — field median 2.93:1 | `register.md` S3 |
| **speakers are named** | every `dialog`/`thought_bubble` says whose it is | `engine.md` §25 |
| **effects use a live op** | no effect uses an `op` the engine silently discards | `engine.md` §21b |
| **the climb is paid for** | every meter a gate reads has a brake on the rungs that raise it | `the-meters.md` M1–M5 |
| **a day-cap closes** | every flag read `is_false` and cleared in `[engine.daily_tick]` is SET somewhere — a cap with two of its three parts validates and throttles nothing | `the-meters.md` M5 · `engine.md` §28.2 |
| **a spent day still has a door** | no screen whose every choice is day-capped or priced lacks one choice free of **both** `conditions` and `costs` — a spent cap renders nothing at all, not a greyed line | `the-surfaces.md` R7 · `engine.md` §28.3 |
| **a locked door says why** | every `show_when_locked` choice carries the reason — a `locked_text`, a threshold or a rejection node. The field hides a refusal or explains it; 2% ship a dead greyed label | `the-surfaces.md` R5c · `engine.md` §15 · §36 |
| **a meter is read** | every number the game raises is read by a condition, a cost or a quest goal — a raise with no reader is decoration | `the-meters.md` W3 |
| **the wardrobe is read** | a game declaring `[[clothing]]` reads it somewhere — she can dress and the world does not look | `the-meters.md` W3 · W7 · `engine.md` §17 |
| **the climb is where you said it is** | the game gates where `board.who_climbs` says it does | `the-meters.md` W1 · `state.md` |
| **a banded meter is not also a number** | a banded sidebar stat is `hidden` in `[[traits.labels]]` | `the-meters.md` M7 · `engine.md` §30 |
| **the opening opens a door** | the funnel's last click lands on a clock time when something at that location is actually open | `the-first-hour.md` F3 |
| **every hub is met first** | no character's portrait is live before a meeting has fired, and one flag never opens the whole cast | `the-first-hour.md` F5 · F8 |
| **a meeting fires where they are** | a one-shot naming a character carries a `trigger.schedules` window matching that character's own hours — `requires_npc` does not gate the auto-fire path, so without one the introduction plays to an empty room | `the-first-hour.md` F5 · `engine.md` §31 |
| **the start choice is read** | a choice the opening asks the player to make is read by real content later — fails only on ZERO, and a game that asks nothing reports n/a, which is not a pass | `the-want.md` §1 · `state.md` |
| **what she picks is read** | every `[[player.customization_fields]]` value is printed somewhere — `$player.<id>` or the `@player.<id>` token — fails only on ZERO, `sets_portrait` counts as a read, and a game declaring no customization reports n/a, which is not a pass | `the-want.md` §1 W1 |
| **the label keeps its time** | no button promises a clock time the engine cannot reach, and a stated duration is the real spend | `the-clock.md` C3 · C4 |
| **the price is in one currency** | every notation on a button, plus the engine's own `currency_symbol`, resolves to ONE currency | `the-economy.md` R7 · `engine.md` §33 |
| sentence length | the prose has not drifted dense | `register.md` |
| prose texture | the dash rate against the field — p50 0.99, p90 17.5, ceiling 35.0/10k. The other three texture figures print and are **not** judged | `register.md` — "Dashes stay rare" |

Lints sit below the tally and never move it: dialogue attribution · room-list labels ·
the browse share · screen shape · the prose names places the map does not have · **the ladder**
(where a scene starts and stops on it) · **talk screens** · **the act menu** · **the meter ladder**
(rungs per tier, and where the lowest one sits) · **the cast's meters** · **the counterweight** ·
**the words the player has to already own** (every word in the player's face that fewer than four
of the 27 field games use — **prose, choice labels AND location names**, because a word the player
cannot decode is undecodable on a button too; a list to read, never a score) · **dispatch depth** (how many different
things one activity can turn into, and how often the activity itself still renders) ·
**the act nodes** (body words on the thinnest band each act and finish node can render) ·
**named before met** (every character
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
over the declared `week_income` — a figure, never a score) · **what a paid repeatable leaves
behind** (how many surfaces she pays for deposit anything; a pure sink is not a defect, a game made
only of pure sinks is) · **the ambient puts him in the room** · **the badge arrives before the
content** · **the role stays attached** · **which refusals are
shown at all**.

## Operating rules

- **Parse, never grep.** Game state is TOML; read it with a parser. A grep-based pass on one
  game silently missed 24 `is_repeatable` lines and reported the opposite of the truth. The
  same discipline applies to every claim: measure it, don't eyeball it.
- **Every engine claim carries a `file:line`.** If `references/engine.md` doesn't have it,
  go read `apps/game_generation/twee_comprehensive/generators/v2.py` and add it with its
  citation. Never assert engine behaviour from memory.
- **Gates before ship.** `python3 scripts/gates.py <slug>` must be green. A gate that fails
  is either a real defect or a wrong threshold — fix one or the other, never skip.
- **The scoreboard has three other modes, and each answers something `<slug>` cannot.**

  | | |
  |---|---|
  | `gates.py --words <path>` | the vocabulary lint on any text file — run it on the WANT and the BOARD, while the nouns are still being *chosen*. Run on a built game it is one phase too late: every noun is already a room name and a button. Always exits 0; it is a list, never a score. |
  | `gates.py --release <slug>` | the **artefact**, not the source. Every gate above reads `7_final_game.toml` and none of them can see a build, which is why a game shipped to the published grid as a `--dev --debug` artefact with 115 missing files and nothing said so. Six checks, off for every ordinary run, **exits non-zero**. `the-release.md` § Shipping the build. |
  | `gates.py --saves <slug> [<ver> [<ver>]]` | **the only check that reads TWO releases.** Every other check here reads one snapshot, and a save break does not exist in a snapshot — renaming a canvas id produces a game that is correct on its own terms and strands every player holding a save. Diffs the current build's join keys (passage names, `$npcs` keys, flag keys, player and NPC meter keys, the story title) against the newest archived release; additions are counted and never judged, because the migration seam reaches them (`engine.md` §40). Needs `releases/v<version>.html` to exist — without an archive it cannot run. **Exits non-zero.** ⚠️ A rescaled stat and a burned one-shot grant are invisible to it and stay human: `the-returning-player.md` §4 and §6. |
  | `gates.py --selfcheck` | does this file still document every gate and lint the script emits, and does every rule the references POINT AT actually exist? Needs no game. The index went stale twice — the 2026-08-16 audit closed it and it reopened in twelve days — because nothing compared the script to the file that documents it. The rule half was added after `the-voice.md` R6 was recorded as shipped in two ledgers, cited by this script, listed in its own file's checks table, and never written: a qualified pointer at a rule with no section FAILS, while a bare in-file reference is listed to eyeball and never scored, because a withdrawn rule discussed as history is correct prose. |
- **`scripts/playtest.py <slug>` plays the build.** Every gate above reads the source; this drives
  the running game in a browser and is the only place some defects exist at all — `forty_miles` 0.1
  shipped 35 effects using an op the runtime does not implement, and the TOML, the validator, the
  build and every gate were green the whole way down. It is also what the `v2-player` agent runs.
  ⚠️ **A red is a hypothesis until its cause is quoted as `file:line`**: three of this harness's own
  first four reds were the harness, not the game. `references/agents.md`, The Player.
- **An example outranks every rule beside it, so it goes in LAST — after it is validated, or not
  at all.** A rule is read; an example is copied. `the-map.md` shipped a worked example on day one
  that was the first game's own map — its character ids, its box room — with its two known bugs
  patched out and its skeleton intact. Three games inherited that skeleton, and the second
  house-shaped world scored **26/26** before anyone noticed. Where a shape has to be taught, teach a
  **menu the author must choose from**, never one picture they can copy. If a validated example is
  ever promoted, it is **one per option or none** — a single good example reproduces the failure
  with a nicer floor plan. *(Every other reference file carrying a worked example has the same
  exposure; that audit is open.)*
- **The examples are also the REGISTER, not just the shape.** Same rule, third instance, and the
  one nobody saw coming: no line in this skill ever said "write British", but its worked examples
  used `airer` ×9, `lodger` ×8, `immersion` ×3 and shipped `costs = "£5 for the immersion"` in
  `templates/board.toml`. Five games came out written in a dialect the genre does not use — the
  field runs locale-locked nouns at **0.8 per 10,000 words**, our v2 games at **9.4–95.6**, and the
  v1 games, whose skill happened not to carry those examples, sit at the field's rate. **Every word
  in an example is being taught too.** `references/register.md`, "The words the player has to
  already own".
- **A shape that ships in `templates/` is copied harder than one that ships in `references/`.** A
  reference file is read; a template is *filled in*, so whatever is already sitting in the slot is
  the answer unless the author actively fights it. `the-board.md` said *"their rungs sit at
  15/35/55/75 — copy that shape"* and `templates/board.toml` carried the matching band table:
  **all 16 declared tiers across five games put their lowest rung at exactly 15**, against a field
  that runs 8–17 rungs starting at ~5. The same file's volatile block said *"NEVER gate an arc on
  these"* and omitted what a throttle IS for, and five games shipped **232 arousal raises against 4
  reads**. This is the "an example outranks every rule" rule one level worse: in a template, even a
  *placeholder list* is an example. Ship a menu the author must cut down, never a set they can keep.
- **Ask what a tired author would build to satisfy a check, and make sure that is the thing you
  want.** A check does not measure quality; it **manufactures** whatever it can see. `objects` /
  gate 22 was green on all five games while forcing nine duplicate room screens into existence,
  because it computed affordances from `exit_block.choices` and could not see a canvas at all — so
  an entire canvas about the airer counted as zero, and the only way to pass was a second screen
  re-listing what was already there. That is worse than no check, because it ships green. It was
  deleted 2026-08-18 and replaced by `the-surfaces.md` R2: a room's list is **needs + work +
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
  *how much of it there was* or *what it cost*. `ends on an opening` was `locked > 0` and passed a
  game running 78% of its choices open on turn one. `ascent tiers expand the world` tests
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
  built for locked doors fired on seven of eight and every one was following `engine.md` §15
  correctly. A check that fails a game for obeying the doctrine is a bug in the check. Measured
  again 2026-08-16: gate 24 failed a game whose obligation *was* charged, because the gate walked
  canvases and the charge lived in `[settings.rent]`.
- **A vocabulary the engine does not recognise fails SILENTLY, and nothing else in this system
  does.** `op = "subtract"` is not an engine op — `applyTraitEffect` runs `add` and `set` and
  returns on anything else (`v2.py:5742-5751`). Two v2 games shipped 105 effects that do nothing,
  because this skill's own `engine.md` discussed the op as though it worked. Valid TOML, green
  build, green gates, and a clean play-through, because **a number that never changes looks exactly
  like a number the player has not moved yet.** When you write an unfamiliar key or value, find the
  line that consumes it before you write a hundred of them. Gate 25 and the importer now both
  refuse it; the next one of these has no gate yet.
- **Twice now, the missing feature was already built.** `block_pool` (§35) and `rejection_node`
  (§36) are both fully wired in the engine, both solve a defect this skill kept finding in its own
  games, and both were used by **zero** v2 games because nothing here wrote them down. The tell is
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
  state, the field's answer is almost always a small branch per site instead** — and ours default to
  the opposite: `the_season`'s seven `known` read sites have a median of 570 characters.
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
