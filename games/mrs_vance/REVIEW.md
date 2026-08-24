# Mrs. Vance — review ledger

Opened 2026-08-25, the day after v0.1 shipped (`a77058d`). Mrs. Vance is the **first game authored
under the complete `author-game-v2` doctrine** — after all eleven sections of the field study
closed — and the **first v2 game to take every gate**: `41/41 judged, 1 n/a`.

It is also the first v2 game to ship `block_pool`, and the first whose explicit prose clears the
pivot rule end to end. Neither of those is in the tally. Neither is what follows.

**The scoreboard is green and the scoreboard is not the review.** Same finding as `steam` and
`forty_miles` before it: the instrument is 42 checks wide and the game is wider. Six items below
are invisible to all 42 — and all 42 read the source only. Not one of them opens the built game
(`grep -cE 'output/|index\.html' gates.py` → **0**), which is its own item now: B2.

**Same conventions as `games/steam/REVIEW.md`, `games/forty_miles/REVIEW.md` and
`games/off_season/REVIEW_1.md`:**

| field | values |
|---|---|
| **severity** | `BLOCKER` · `HIGH` · `MED` · `LOW` · `OPEN` (an unresolved question for LO, not a defect call) |
| **layer** | `GAME` (this build) · `SKILL` (doctrine taught it wrong or never taught it) · `ENGINE` (the substrate) |
| **evidence** | a `file:line`, a measurement, or a live observation. Anything without one is marked *opinion* |
| **status** | `OPEN` · `FIXED (<rev>)` · `WONTFIX (<reason>)` |

Per `CLAUDE.md`: fix the skill too wherever a correct skill would have prevented the item, or it
ships again next game. Two of the six qualify — §10.

**Method.** `7_final_game.toml` parsed with a real TOML parser, never grep. The canvas graph walked
for reachability, broken targets and dead nodes. `scripts/gates.py` captured before and after and
diffed. A clean non-`--dev` build made to scratch for comparison. Then the built game **live-played
in headless Chromium**: through the age gate and the whole opening funnel, plus targeted
`Engine.play` probes with `setup.commitMoment()` for the finish bands, the pool cycling, the money
clamp, the sleep landing and the quest page. Every structural claim was checked in the built game,
not inferred from source. §11 has the full list.

**Two instruments, kept apart.** `§1`–`§10` were found by **reading and probing** the game. `§12`
was found by **LO playing the built game** — a different instrument that finds a different class of
defect, and the two are not merged so it stays visible which found what. Same split
`off_season/REVIEW_1.md` records in its own header.

**Current count: 18 open, 3 fixed** — 0 blockers, 4 high, 7 med, 6 low, 1 open question, and **P1,
Q1 and Q2 FIXED**. Three of the twenty-one are decisions for LO rather than defect calls: E1 (the
obligation's size), D1 (how much locked content should explain itself) and G1 (whether the Want
file's one shape is the genre). Plus **nine places
this review was itself wrong**, recorded first in §0a — six caught before writing, and three (N7,
N8, N9) caught only after they had shipped in this file, one of them as its single blocker.
`v2_state.json` is deliberately untouched; the remaining SKILL-layer items (C2, Q1, W1, G1, half of
D1) are recorded for LO to schedule.

---

# §0a · ⚠️ What this review got wrong

`forty_miles/REVIEW.md:31` puts its own corrections ahead of its defect list, because a review that
hides its misses is worth less than one that does not. Seven claims made during this review were
narrowed or overturned by checking them. **Six were caught before anything was written down**, which
is the only reason they are corrections and not defects in this file. **N7, N8 and N9 were not** —
all three shipped in this file and were overturned afterwards: N7 by LO the day after, N8 and N9 by
the work of actually repairing the items they belonged to. They are the three most instructive
entries in the section for exactly that reason, and the pattern in the last two is the same —
**a defect's diagnosis does not survive contact with its repair.**

### ⚠️ N1 · The clock-gate hole is one missing preposition, not "it cannot read spelled-out numbers"

First stated as: *the gate looks for digits, so "six" walked past it.* **False.** `_CLK_WORDNUM`
(`gates.py:2718`) contains `one|two|…|twelve`, and the gate reads spelled-out hours perfectly well.

The real hole is one word. `_CLK_PREP` (`gates.py:2727-2730`) fires on
`at|till|until|by|before|after|past|from|gone` followed by an hour. **`to` is not in that list.**
Run against the instrument itself:

```
"Sleep. (till six)"   ->  ['till six)']      CAUGHT
"Sleep. (until six)"  ->  ['until six)']     CAUGHT
"Sleep. (to six)"     ->  []                 not caught
"Sleep. (to 6)"       ->  []                 not caught
```

`till six` would have failed the build. `to six` shipped. This matters for the fix: it is a
one-token addition to an alternation, not a redesign of the extractor.

### ⚠️ N2 · "The player grinds Isaac to 66 and finds nothing" is false

First stated as: *Isaac's terminal quest card sets a goal of `want 66`, nothing exists at 66, so
the player grinds toward a destination that is not there.* The premise is right and the conclusion
is wrong, because **the player never sees that goal.**

`renderQuestsGoalBlock` (`v2.py:14970`) renders **exactly one** frame per card, in the order
`✓ terminal → 🔓 ready_canvas → 🎯 unmet goals`. `terminal` wins. Verified on the live quest page:
with Isaac at `want 38` the card prints `✓ Arc complete` and the 66 is never drawn.

Checking it turned up a worse defect in the same place, which is §3. The lesson is the ordinary
one: a claim about what a player sees has to be checked against what renders, not against the TOML.

### ⚠️ N3 · Dorn's meter climbs 5 a day, not 8

First stated as *8/day across two raise sites*. Both sites — `walkin_room_dorn` (+3) and
`hub_dorn_kitchen` (+5) — gate on **the same day-cap flag**, `dorn_rung_today`, and both set it. So
it is one or the other, never both, and the ceiling is **+5 on a day he is home**. He is home three
nights of seven, so `want 55` is roughly three to four weeks of play, not one.

### ⚠️ N4 · `loop_act` is guarded, and the trap is narrower than first described

First stated as *a shared global with no guard*. It is shared — one player trait across all six
loops — but it is guarded twice. Every one of the five NPC loops **sets it at entry** before any
band can be read, and five of six also **reset it to 0** on the `finish` exit-block config
(`Get your jeans.`, `Do your shirt up.`, and so on). The residual is real but small, and is filed
at its true size in §8.

The next two came out of investigating LO's play-report (§12) and are recorded here for the same
reason: both are conclusions someone would otherwise reach again from scratch.

### ⚠️ N5 · "No location declares a single connection" is false — the key is `navigation_order`

First stated, while investigating LO's *"couldn't understand the world"*, as: *every location has
`connections: []`, so there is no adjacency data anywhere.* **The script grepped the wrong key.**
Adjacency is declared as **`navigation_order`**, every location has one, and together they form a
complete two-level tree under `the_yard` (§12 M2). The engine appends the way back itself —
`[[Leave <name>->...]]` at `v2.py:19807` — which is why the authored graph looks one-way and the
game plays fine.

**The map data is correct and the gate `world reachable 14/14` is honest.** M1 and M2 are about what
the player is *shown*, not about what is declared.

### ⚠️ N6 · "`requires_npc` is read from `trigger.metadata`, so the presence gate is dead" is false

First stated, on reading `v2.py:11508` — `requires_npc = trigger.metadata.get("requires_npc")` —
against a game that declares the key at `trigger.requires_npc` with `metadata` empty: *the presence
gate is off game-wide.* **The importer moves it.** `template_import.py:6990` writes
`"requires_npc": c.trigger.requires_npc or None` into that metadata dict, and the built HTML carries
**25 non-null `requiresNpc` values** — exactly the 25 canvases that declare it.

Walk-ins, hubs and meetings are genuinely presence-gated. The defect is only in the ambients, which
declare nothing at all (§12 P1). Recorded because "the generator reads a key the author does not
write" is a plausible and wrong conclusion that a grep alone supports.

### ⚠️ N7 · "The `--dev` build is a blocker a player meets on the first screen" is false — and this one shipped

**The only correction in this section that was not caught before writing.** It went into the file as
§1, as the review's single `BLOCKER`, and LO overturned it the next day: *"it being in dev mode is
the blocker for release, media missing is the blocker for release, not for testing."*

He is right, and the repo is further along than his framing. The portal **already** separates the two
and this game is already on the correct side of the line:

- `games-data.js:10` — `dev (optional) — true → renders in the "Dev / test builds" section, "Open" affordance`.
- `mrs_vance` carries `dev: true` and **no `version` field**, so it renders in the dev grid, not the
  main one, and nothing is published.
- `games-data.js:44-49`, the comment on this game's own entry, already states the situation and the
  exit from it: *"Current output/ is a `--dev --debug` build, **so the art shows labelled debug
  placeholders rather than silent gaps.** Run find-media, rebuild output/ WITHOUT `--dev --debug`,
  add `version`, archive to `games/mrs_vance/releases/`, and drop `dev: true` in the same commit."*

So the dev build is not a slip. For a game whose media has never been harvested it is the **better**
artefact: `--debug` (`package_from_toml.py:104`, *"Show placeholder blocks for missing videos with
filename and description"*) is what turns 34 silent holes into 34 labelled ones. The fix §1
originally prescribed — rebuild clean, today — would have destroyed authoring information and
published nothing.

**What survives is the opposite item.** The rule *blocks release, does not block testing* is correct
and **nothing enforces it**: no gate reads the artefact, and `the-release.md` never mentions the act
of publishing a build. That is B2, and it is the finding this correction produced.

**The lesson, and it is the general one.** Every other correction here came from re-checking a claim
about the code. This one came from a claim about **intent** — what a file is *for* — and no amount of
measuring the file would have caught it. The measurement in §1 was right in every digit. Severity is
not a property of an artefact; it is a property of an artefact **and the phase it is in**, and the
review knew the first and assumed the second.

### ⚠️ N8 · P1's own census was wrong in four numbers and three verdicts

**The second correction that shipped in this file.** It was found by repairing P1 — reading all 36
ambients end to end instead of matching character names in prose, which is what the first pass did.

| §12 P1 as written | measured |
|---|---|
| "21 random ambients" | **36**. 21 is the subset in which a cast member *speaks* — the right number under the wrong label |
| "roughly thirteen" need gating | **16** gated, **1** left open as a writing call |
| "Eight of the twenty-one are NOT defects", table listing 6 | **3** genuinely leave-alone, plus **1 already gated** |
| "No gate reads `requires_npc` at all" | `gates.py` reads it **12 times**; G38 (`:5109-5172`) is built entirely on it |
| the fix is `requires_npc` | it binds **exactly one** NPC and has no absence form. Two canvases needed `npc_at_location` (`engine.md:561`, §20) |

**Three of that table's six rows were wrong the same way**: the prose narrates *one* character's
absence while a *second* is silently assumed present. `amb_office_phone` — Dorn is on the telephone,
but **Cade comes through the hatch** and takes the receiver. `amb_kitchen_five_adults` — Sherrod's
arrival is narrated, but **Booth is already at the table** and speaks. `amb_bunk_two_of_them` — the
*player* is on the stairs, which is what the first pass read; **Isaac and Tobin are both in the
room**.

**Why the instrument failed.** The first census matched character names in narration. Half these
scenes never name the man — `amb_office_close` says only *"He says it like he is agreeing to
something"* — and the actual signal was structural all along: a `dialog` block carries
`props.npcId`, so *who speaks* is a fact in the data and not a reading of the prose. The corrected
census counts those, and it is what the new lint counts too.

**The general shape.** A prose-matching heuristic used where a structural one was available, and it
was wrong in both directions at once — it missed scenes that place a man without naming him, and it
convicted scenes that name a man who is deliberately elsewhere. §11's *"parsed with a real TOML
parser, never grep"* was the right rule and this pass broke it one level down.

### ⚠️ N9 · Q1's "gated at the SAME value as the content" is wrong on three of five

**The third correction to ship in this file**, found the same way as N8 — by repairing the item.

Q1 as written: *"the card the player climbs to is gated at the **same** value as the content, so the
✓ lands on the same click as the unlock."* True for Isaac and Sherrod. For the other three the badge
fires **before the door opens at all**:

```
tobin    terminal at want gte 30, door at want gte 70      40 points early
cade     terminal at trust gte 26, door at want gte 42     a DIFFERENT meter
booth    terminal at trust gte 30, door at want gte 50     a DIFFERENT meter
```

Cade's and Booth's badges are gated on `trust` while their doors read `want` — two meters that move
on different surfaces — so the ✓ could arrive at `want 0`. "Same click" understated it.

**Why the first pass missed it.** It read the quest cards and stopped. The door values live on the
**hub choices**, not on the cards, and the two were never put side by side — A.6 had the door values
written down in the same file the whole time. **Comparing two tables the review already contained
would have caught this**, which is a cheaper instrument than anything used to find it.

Q1's fix note also said *"raise each terminal card's `when` above its loop gate"*. That would have
exposed three goal thresholds nothing in the game reads (`isaac.want 66`, `sherrod.want 62`,
`tobin.want 30`) as live instructions to grind for nothing. The right fix was to stop gating the
badge on a meter at all.

---

# §1 · The dev build is right for this phase, and the release boundary is unguarded

### B1 · The committed HTML is a `--dev --debug` artefact — correct for now, blocks release
**severity** LOW — *downgraded from BLOCKER, see §0a N7* · **layer** GAME · **status** OPEN, at release only

Every measurement below held on re-check (2026-08-25). Only the severity and the prescription were
wrong.

`games/mrs_vance/output/index.html` is git-tracked and was built with two opt-in flags, which are
separate and do separate things:

| flag | `package_from_toml.py` | what it puts in the build |
|---|---|---|
| `--debug` | `:104` *"Show placeholder blocks for missing videos with filename and description"* | the 34 labelled media markers |
| `--dev` | `:136` *"Enable dev mode with stat adjustment controls in sidebar"* | the banner, the jump panels, the meter adjusters |

Committed file against a clean rebuild into scratch:

```
                                    committed        clean rebuild
"DEV MODE"                                2                    0
[IMAGE MISSING]                           2                    0
[VIDEO POOL MISSING]                     32                    0
bytes                             1,833,785            1,538,629
```

What is in it: a red **`[DEV MODE]`** banner at the top of the sidebar; **`⏩ DEV JUMPS`**,
**`📋 Review Canvases`** and **`⚠️ Missing Media`** panels; **`+/-` adjusters on every meter** —
`money`, plus `want`/`trust` for all six characters, which makes the entire ascent clickable; and on
the second screen of the opening, inside the prose, `[IMAGE MISSING] scenes/dorn_leaving_t1.jpg`
with its author-facing description and both raw search queries as clickable links.

**Why this is not a defect today.** Every one of those is an authoring instrument, and the game is in
authoring. `mrs_vance` carries `dev: true` and no `version` in `games-data.js`, so the portal files it
under **Dev / test builds** and nothing is published. The `--debug` markers are the *point*: media has
never been harvested for this game, so the choice is 34 labelled holes or 34 silent ones. Rebuilding
clean today would delete the labels and publish nothing. Full reasoning and quotes in §0a N7.

### Fix

Nothing now. **At release**, the procedure already exists — written on this game's own portal entry
at `games-data.js:44-49`, and it is four steps in one commit:

1. Run find-media and harvest the 29 cycling pools, the fixed plates and the portraits.
2. Rebuild `output/` with **neither** flag:
   ```bash
   python3 manage.py package_from_toml \
       --file games/mrs_vance/toml_phases/7_final_game.toml \
       --output games/mrs_vance/output --gen-version v2
   ```
   Verified in scratch already: the clean build boots with zero page errors, zero console errors, and
   no missing-media markers anywhere.
3. Archive that exact build to `games/mrs_vance/releases/v<version>.html` and add `version` to the
   portal entry.
4. Drop `dev: true`, in the **same** commit — that is the line that moves the game into the main grid.

### B2 · Nothing enforces the release boundary — it lives in one hand-written comment per game
**severity** MED · **layer** SKILL + TOOLING · **status** OPEN

B1 is only safe because someone remembers. The rule LO states — *dev mode and missing media block
**release**, not testing* — is right, and there is no instrument anywhere in the repo that holds it.

```
gates.py lines reading output/ or index.html                              0
  (it knows dev_mode_enabled only as a TOML marker, gates.py:2193-2199)
the-release.md hits for --dev / dev mode / debug / placeholder /
  missing media / release checklist / "before you ship"                   0
  (8 headings, all about what a release ADDS as content)
```

So the entire release procedure for this game exists as a **comment on a JavaScript object literal**
(`games-data.js:44-49`) that no tool reads and nothing checks. And not only for this game: **nine of
the twenty-eight portal entries restate the same procedure by hand**, in at least three different
phrasings — *"drop `dev: true`"* on five of them, *"drop the dev flags"* on `steam`, *"Flip
`dev: true` if it should sit in the dev section until then"* on `forty_miles`. Nine hand-copies in
three wordings is the signature of doctrine living in the wrong file.

The drift it allows is already visible. `forty_miles` carries **`version: "0.1"` and `dev: true` at
the same time**, and the schema declares no relationship between the fields — `version` is defined
as *"the PUBLISHED release currently live at `games/<slug>/output/`"* while `dev: true` files the
game under builds that are not published. Both are defensible readings of that entry. Nothing can
adjudicate, because nothing was ever told which combination is legal.

That comment is genuinely good, and that is the problem: it is doctrine that was discovered once,
written in the one file where it could not be enforced, and never lifted into the skill. The header
of `games-data.js` (`:11-15`) even carries the sharpest sentence anyone has written about this —
`version` *"must track what actually shipped — NOT whatever is currently half-built in the working
tree"* — which is a release-gate specification in a data file's comment block.

**Why no check caught it.** The whole 42-check instrument is aimed at `7_final_game.toml`. That is
the right target for authoring and it is structurally incapable of seeing a build. A release is the
one moment when the artefact, not the source, is the thing being judged, and that moment has no
instrument at all.

#### Fix

Two pieces, and the first is small.

**A release section in `the-release.md`.** The file is named for this and does not cover it. What
separates a test build from a published one, as one list: media harvested, built without `--dev` and
without `--debug`, archived to `releases/v<version>.html`, `version` set, `dev: true` dropped, and
`v2_state.json` promises reconciled. Lift it from `games-data.js:44-49` rather than inventing it —
the procedure is already correct, it is only in the wrong place.

**A `--release` mode on `gates.py`** that reads the built artefact and hard-fails on any of: a
`DEV MODE` marker, an `[IMAGE MISSING]` or `[VIDEO POOL MISSING]` marker, `dev: true` still set on
the portal entry, or a missing/stale `version`. It stays **off** for every ordinary run, so nothing
about authoring changes — which is precisely LO's rule expressed as code instead of as memory.

---

# §2 · A button promises an hour the engine cannot reach

### C1 · `act_sleep` says "(to six)" and lands anywhere from 05:00 to 11:45
**severity** HIGH · **layer** GAME · **status** OPEN

`act_sleep`'s exit block carries `text = "Sleep. (to six)"` and
`time_progression_minutes = 480` — a flat eight hours. The canvas window is 21:00–04:00, seven
hours wide. Live, driving the clock and clicking the button:

```
sleep at 21:00 Monday    ->  wakes 05:00 Tuesday
sleep at 22:00 Tuesday   ->  wakes 06:00 Wednesday      <- the only correct case
sleep at 23:30 Wednesday ->  wakes 07:30 Thursday
sleep at 01:00 Thursday  ->  wakes 09:00 Thursday
sleep at 03:45 Thursday  ->  wakes 11:45 Thursday
```

The label is true for **one entry minute of a 420-minute window**.

It is not only cosmetic. `work_counter` runs 07:00–13:00 and takes six hours. Sleep at 01:00 and
two of those hours are gone before the player is awake; sleep at 03:45 and the counter — the
largest income surface in the game at +74 — cannot be started at all.

This is precisely what `the-clock.md` C3 (`:192`) forbids: *"A label is a promise about what the
click does. The engine cannot deliver a clock time (C1), so a label naming one is a promise it
cannot keep."* Against a field re-measurement of **84,009 action labels across all 27 parseable
sandboxes**, of which 24 name an absolute clock time and **not one** promises a clock time as the
outcome of a repeatable action.

### C2 · The gate that enforces C3 has a one-word hole
**severity** MED · **layer** SKILL · **status** OPEN

Gate G36, *the label keeps its time* (`gates.py:5209`), exists, is correct in intent, and reported
`0 label(s) name a clock time` on this game. The cause is N1: `to` is absent from `_CLK_PREP`'s
preposition alternation (`gates.py:2727-2730`).

Four v1 games and two v2 games already pass this gate, so the bar is one shipped work has cleared —
which makes the miss a hole rather than a threshold problem.

### Fix

**Game.** Turn the reading into a rule, the grammatical turn C2 of the same doctrine already
prescribes: `Sleep the night.` The clock stays engine business. If the hour genuinely has to be
named, C3 says that is a window problem — narrow `act_sleep`'s schedule until the claim is true —
and that there is no third option.

**Skill.** Add `to` to `_CLK_PREP`, re-run the census across the 22 scorable games, and record what
moves. Expect false positives on `to` where it is not temporal (`to the yard`); the existing
`_CLK_OK_NEXT` / `_CLK_BAD_NEXT` machinery is what handles that and will need the same treatment
the other prepositions got.

---

# §3 · The badge arrived before the content, on five of six

### Q1 · The ✓ was gated on a meter, and on three characters it landed before the door opened
**severity** HIGH · **layer** GAME + SKILL · **status** **FIXED** — six ladders rebuilt, proved live

**⚠️ This item's own diagnosis was wrong on three of the five.** §0a **N9** records it. The corrected
picture is below; the first draft's *"gated at the same value as the content"* should not be quoted.

Every character's second card was `terminal = true`, and Frame 1 fires on `card.terminal === true`
**alone** (`v2.py:15404`), ahead of the ready and goal frames, with nothing checking achievement.
Against the value that actually opens each loop (A.6):

| character | the badge fired at | the door | what the player saw |
|---|---|---|---|
| `npc_isaac` | `want gte 38` | `want gte 38` | ✓ on the same click as the unlock |
| `npc_sherrod` | `want gte 34` | `want gte 34` | ✓ on the same click as the unlock |
| `npc_tobin` | `want gte 30` | `want gte 70` | **✓ forty points of climbing early** |
| `npc_cade` | **`trust gte 26`** | `want gte 42` | a **different meter** — ✓ possible at `want 0` |
| `npc_booth` | **`trust gte 30`** | `want gte 50` | same |

So it was not one defect but two: a badge landing *on* the door, and a badge landing *before* it on a
meter the door does not read.

**Three goals were numbers nothing in the game reads.** Every `gte` threshold any canvas condition
uses, per character trait, against what the cards asked for:

```
booth.trust  5, 30    booth.want  50        cade.trust  6, 26    cade.want  42
isaac.want   6, 38    sherrod.want 5, 34    tobin.want  5, 70

asked for and never read:   isaac.want 66 · sherrod.want 62 · tobin.want 30
```

They were invisible only because the terminal frame outranked the bullets. **Removing `terminal`
without touching them would have made the game worse** — the ✓ replaced by a live instruction to
climb 28 points for nothing. That is the trap in this repair and the reason the fix was not "raise
the threshold".

**And the game never used Frame 2 at all.** `🔓 Ready` + `📍 <location>` + `🕒 <schedule>` needs a
`ready_canvas`, and the key appeared **zero** times. The guidance page had two states, *climbing* and
*done*, and never *the door is open, here is where and when* — which is half of what LO could not
work out about the world (§12 M1/M2).

### Q2 · Dorn's card drew no frame at all, then a badge on an empty arc
**severity** LOW · **layer** GAME · **status** **FIXED**

His first card was `when want lt 55` with goal `want gte 12`. Between 12 and 54 every goal was met,
there was no `ready_canvas`, and Frame 3 requires `!allMet` — so it returned `""`. The card rendered
its text and 💡 tip **with nothing ticked**, which is precisely the trap `engine.md` §23 was written
about. At 55 it flipped to `✓ Arc complete` for a character with one hub, one walk-in and no ladder.

### Fix

**The badge is no longer gated on a meter.** It is gated on a flag the loop sets on its way out, so
it means *you have played this* rather than *you have ground past it*. Three states per character:

| card | `when` | `goals` | `ready_canvas` | frame |
|---|---|---|---|---|
| climb | `<meter> lt DOOR` | the door, with its label | — | 🎯 live progress |
| ready | `<meter> gte DOOR` + `<x>_loop_played` `is_false` | *(none)* | `hub_<x>` | 🔓 Ready 📍 🕒 |
| done | `<x>_loop_played` `is_true` | *(none)* | — | ✓ + `terminal_text` |

Card *ready* carries no goals on purpose: *"When `goals` is empty, the card has no climbing phase
(`goalState.allMet` is vacuously true)"* (`template_import.py:1078`), so Frame 2 fires the moment the
card matches. 14 cards became 21.

⚠️ **`ready_canvas` points at the HUB, never at the loop, and this is a trap not an aesthetic.**
`lookupCanvasBySlug` (`v2.py:15371`) walks `help_data.locationCanvases`, keyed by location UUID. The
loops are triggerless, so they are **not in that index** — verified in the built HTML:
`hub_cade_office` is present with `hasSchedules: true`, `loop_cade` is absent. `ready_canvas =
"loop_cade"` returns `null`, Frame 2 does `if (!found) return ""`, and the card would have rendered
**no frame at all**.

**Five flags**, one `flagEffects` entry on each loop's `finish` exit
(`4_story_arc.toml`, the idiom from `2_one_shots.toml:274`). Bailing out of a loop mid-scene
deliberately does **not** tick the badge — the `act` node's exit to the room stays open and sets
nothing, which is the correct reading of "played it".

**The three phantom thresholds are cut.** Tobin's fake mid-rung at 30 collapses into his real single
rung, 5 → 70; Isaac's 66 and Sherrod's 62 are gone.

**Dorn** keeps two cards — `want lt 12` climbing, then terminal at 12 with the honest marker. The 55
is gone, and with it the window that drew no frame.

**All six now carry `terminal_text`**, which `engine.md:744` forbade. See §10 — the cap is correct
for a finished game and wrong for a v0.1, and `the-release.md:109` already asks for *"a plain marker
at the top of each track"*.

### Proved live

`games/mrs_vance/playtest_quests.py` — 23/23, zero page errors. It drives `pickQuestsCard` →
`renderQuestsGoalBlock`, the same two functions the page and the sidebar both call
(`v2.py:15454-15456`, *"there is no separate sidebar quest"*), so a pass covers both surfaces.

```
per character, three states
  below the door        🎯 To advance: … — 34 / 42          ✓ absent
  at the door, unplayed 🔓 Ready · 📍 Office · 🕒 …          ✓ absent
  played                ✓ As far as this build goes         "Arc complete" absent

then all five loops played through to their finish node
  cade · booth · isaac · sherrod · tobin      <x>_loop_played  False -> True
```

The Ready assertion checks for the **📍**, not merely a non-empty string — a `ready_canvas` that
fails to resolve returns `""`, and non-emptiness would not have caught it.

### Why no check caught it

Nothing measured **what the badge was climbing to**. `gates.py`'s G15 *"no chain ends in silence"*
(`:3877`) asks only that each character keeps a terminal card, which this game always did.

**`lint_badge_before_content`** now measures it, and the corpus result is the finding:

```
mrs_vance     8 findings before this repair, 0 after
forty_miles   6 of 6 - every badge at exactly the door value
seventh_day   1 badge on the door + 5 goals 25 points past anything the game reads
the_season    4 of 5
the_allowance 3 of 5
vesper        0 of 5   <- the v1 game engine.md §23 was written from is clean
```

**Four other v2 games ship the same defect and the game the doctrine came from does not.** That is
what makes this SKILL-layer rather than an author slip, and it is why the fix went into `engine.md`
in the same commit.

---

# §4 · The six repeatable sex loops are frozen

### R1 · 39 variant pools in the game, zero in the loops
**severity** HIGH · **layer** GAME · **status** OPEN

First, the thing that is going right, because it is the reason this item is sharp rather than
routine. **Mrs. Vance is the first v2 game to ship `block_pool`.** Census across all 22 scorable
games:

```
mrs_vance      39
vesper (v1)     6
every other      0
```

39 blocks across 35 canvases, with 2–4 variants each (21 pools of 3, 11 of 4, 7 of 2), no nesting,
no single-variant pools, and **verified cycling live** — six renders of `hub_cade_office` produced
three distinct middle paragraphs.

**Two different things share the word "pool" and only one of them is missing.**

| | what it is | in this game |
|---|---|---|
| `block_pool` | a **prose** pool — the engine picks one of N text blocks on every render (`v2.py:14572`) | 39, none in a loop |
| `pool_dir` + `pool` | a **media** pool — a folder of clips, one per visit | 34, correctly declared on every explicit surface |

So the sex scenes do vary their video. What repeats verbatim is the writing.

**Not one prose pool is in a loop.** Of the **20** nodes across `loop_cade`, `loop_isaac`,
`loop_booth`, `loop_sherrod`, `loop_tobin` and `loop_solo`:

```
loop_cade      entry  act_hand  act_mouth  act_desk  finish(3 group bands)
loop_sherrod   entry  act                            finish(2 group bands)
loop_isaac     entry  act                            finish
loop_booth     entry  act                            finish
loop_tobin     entry  act                            finish
loop_solo      base   act                            finish
```

**18 of 20 carry no variation mechanism at all.** Only Cade's and Sherrod's `finish` nodes vary,
and they vary on `loop_act` — which act the player chose — not on re-entry. Isaac's 136-word act
node, Booth's 96, Tobin's 82 and the solo scene's 81 render identical prose on visit 1 and visit
50.

These are the surfaces the game's own design document commits to. `WANT.md` §7:

> **Where the crude register lives:** the Office after close, the Wash Bay, the Bunk Room, the Back
> Row, the Shop Floor. Every one of them is a surface she re-enters. **Not one of them is a
> one-time scene.**

They are re-enterable. Their prose is not re-readable, and it is where a returning player spends
most of their clicks.

**The field.** `engine.md` §35: **three of the top four female-PC games in the corpus build every
repeatable sexual surface this way, and none of them writes such a scene as a flat paragraph.**

| game | mopoga rank | mechanism | scale |
|---|---|---|---|
| Course of Temptation | 5 | `<<switch setup.rir(0, 3)>>` | 164 named acts × 3 phrasings |
| Degrees of Lewdity | 7 | deterministic grid on two meters | 99 `actions*` widgets |
| Family Ties | 24 | `either("…", "…", …)` | 12 poses × ~10 narration + ~10 dialogue |

And v1 carried a numbered rule for it — Rule 17, *Block Pools for Repeatable Activities* — naming
the failure exactly: *"the **same text every morning** problem… the group block system handles
phase changes, but **WITHIN each phase, the text is frozen.**"*

**Why no check caught it.** `lint · the act nodes` measures the *heat* of the thinnest band a node
renders and reported this game correctly: median 4 explicit words, 12 of 14 beats explicit. A frozen
beat and a varied beat score identically. Nothing in the 42 counts how many different things a
surface can say.

### Fix

Three-variant `block_pool`s on each act and finish paragraph, at the register the rest of the game
already holds — RTS-flat, 35–40 words, on the body for the beat's whole length. Roughly 18 nodes.
The two `[group]` finishers keep their bands and gain pools inside them; `engine.md` §35 confirms a
pool nests inside a group (depth cap 4) though **not** inside another pool.

One authoring note from §35 worth carrying into the work: children may sit at the block's own
`blocks` key **or** at `props.blocks`, and this game already uses the top-level form throughout, so
copy what is here rather than the `props` form the doctrine used to show.

---

# §5 · The colour meter is read in one room

### S1 · `standing` moves 25 times and is read 4 times, all in the same canvas
**severity** MED · **layer** GAME · **status** OPEN

```
standing   raised at 25 sites
           read at  4 sites  — all four inside work_counter
```

The four reads are a correctly-bounded three-band ladder on `work_counter.nodes[0].blocks[6..8]`
(`gte 40` / `gte 15 AND lt 40` / `lt 15`), and it works: probed live at standing 5 and 25 the
counter narrates two different rooms. That part is good work.

Everywhere else, the meter is inert. `the_bank`: zero reads. `the_bar`: zero reads. `WANT.md` §3
declares:

> **Counterweight:** `standing` — how much of the Vance name is actually hers… **It is read
> constantly and refuses almost nothing** — the bank clerk's tone, whether a driver at the counter
> talks to her or asks for a man, what the bar already knows.

Three examples are named. **One is built.** The other two are locations that exist, with canvases
in them, that do not look at the meter.

`board.colour_meter` reinforces it: *"Read constantly to swap ONE line."* Against the field figure
quoted in the same note — reputation read at 644 sites across the corpus — four is not a colour
meter yet, it is a meter with one customer.

**Why no check caught it.** Gate *a meter is read* asks whether a raised meter is read by any
condition, cost or quest goal. It is: `7/7`. Nothing asks how often, and nothing compares the
reads against what the game said it would do with them.

### S2 · The gap is legitimate to defer and is not written down
**severity** MED · **layer** GAME · **status** OPEN

Building thin and thickening is the method, and adding reads to rooms that already exist is
literally what `v2_state.json`'s own fill promise describes — *"every release until it closes adds
words to existing rooms, not rooms."* So S1 is not a defect of ambition.

It is a defect of record. `promises[]` holds six entries and this is not one of them.
`the-release.md:107,110`:

> Log every promise in the state file, and pay or cut it. […] **An honest wall is a promise; a
> silent one is a bug report.**

The same applies to a fourth thing not in `promises[]` — see L3.

### Fix

Two or three `standing` band reads in `the_bank` and `the_bar`, on the lines the Want already
specifies (the clerk's tone; what the bar already knows), and a promise entry naming the rest.

---

# §6 · The obligation has no teeth

### E1 · The week's income is roughly four times the week's demand
**severity** OPEN — a design question for LO, not a defect call · **layer** GAME · **status** OPEN

```
income surfaces (each day-capped by a *_done_today flag cleared in [engine.daily_tick])
   work_counter    +74   the_office        07:00-13:00  Mon-Fri   6h   18 energy
   work_trailer    +62   the_wash_bay      11:00-14:00  Mon-Fri   3h   24 energy
   work_parts_run  +34   the_shop_floor    08:00-17:00  Mon-Fri   2h   12 energy
   work_books      +22   the_office        untimed               2h   10 energy
   work_walkround  +16   the_back_row      22:00-00:30  daily     1h    8 energy
                  ----                                                 --
                  +208 / day                                           72 energy
obligation        260 / week, Friday, [settings.rent], grace 1
```

The counter alone across four weekdays is 296. Energy is the real brake and it is tuned well —
sleep restores +70 against a 22/day decay and a 72-energy full day, so a complete day is right at
the edge — but it brakes *how much* she earns, not *whether* she clears 260.

That matters because of what failure is wired to. `eviction_mode = "flag_set"` sets `cade_covered`,
and the economy note calls it the mechanised centre of the whole premise:

> *"The reversal, mechanised: she holds the drawer and is not on the account… Money failure feeds
> the cast meters instead of ending the game."*

As built, that branch is reachable only by deliberately not working. The most interesting outcome
in the economy is the one the economy makes hardest to reach.

Recorded as an **open question** rather than a defect because the numbers may be exactly what LO
wants for a first release — a player who cannot pay rent in week one abandons the game, and every
gate here passes. The question is whether 260 should rise, the sources fall, or the drawer count
gain a demand the player cannot see coming.

---

# §7 · The ledger records four things that are not true

Three are in `games/mrs_vance/v2_state.json` and one is in the shipping commit. They are low
severity and high consequence: the ledger is the to-do list the next release reads, and the commit
message is what anyone reads first.

### L1 · "Six external files referenced and not copied" — it is 22, plus 34 directories
**severity** LOW · **layer** GAME · **status** OPEN


`releases[0].promises` says *"Six external files referenced and not copied."* The real inventory,
walked over every file-shaped string in the TOML:

```
locations[].image     14   MISSING
npcs[].portrait        6   MISSING
blocks[].props.file    2   MISSING            <- scenes/dorn_leaving_t1.jpg, scenes/first_office_t1.jpg
                      --
                      22   fixed references, 0 on disk
pool_dir              34   distinct directories, 0 on disk
```

The **6** is the packager's own warning — *"6 external media file(s) referenced but NOT copied"* —
which counts NPC portraits only. The ledger copied the number without checking what it counted, so
the 14 location images and 2 scene images are invisible to the promise that is supposed to track
them.

### L2 · "npc_dorn gates nothing — deliberate" — he gates two quest cards
**severity** LOW · **layer** GAME · **status** OPEN


`lints_shipped_with.cast_meters` says *"npc_dorn gates nothing — deliberate. He is the clock, not a
ladder."* The design intent is right and the statement is not: `npc_dorn.want` is read by two quest
cards, at `gte 12` and `gte 55`. It gates no *canvas*, which is what the lint measured and what the
note meant. Worth stating precisely, because Q2 lives in the gap.

### L3 · Four ladders are declared to a top the build does not reach, and no promise says so
**severity** LOW · **layer** GAME · **status** OPEN


`board.cast_meters.rungs` declares the full ladder; the build gates far below it:

```                declared top   highest gate built
npc_cade                    82                   42
npc_booth                   74                   50
npc_isaac                   66                   38
npc_sherrod                 62                   34
npc_tobin                   70                   70   <- built to its top
```

Deferring the upper half is correct for a v0.1 release stream. But `promises[]` has six entries and
none of them is *"the top half of four ladders"*, so the same silent-wall problem as S2 applies —
and here it is compounded, because Isaac's and Sherrod's terminal quest cards carry goals at 66 and
62, values nothing in the build sits on.

### Fix

Three edits to `v2_state.json` and two new `promises[]` entries. Not done in this pass — see §12.

### L4 · The shipping commit counts 46 `block_pool`s; there are 39

**severity** LOW · **layer** GAME · **status** OPEN

`a77058d`, under *"Firsts for this repo"*, says:

> *"`block_pool` in a v2 game at all — 46 pools, against zero in every v2 game before this and 46 in
> the_long_summer"*

Both numbers are wrong, and the claim they support is right.

```
type = "block_pool" in 7_final_game.toml          39     <- the real count
raw `grep -c block_pool` on the same file          41     <- 39 + two mentions inside comments
raw `grep -c block_pool` on the_long_summer        49     <- not 46
```

The parsed count is the one this review uses everywhere (§4, A.2). 46 matches nothing measurable —
neither the grep nor the parse, in either game. The **first** claim stands unharmed: 39 is still more
pools than every other v2 game combined, and every other v2 game is still zero.

This is L1's failure repeated in a different document — a number written from an impression rather
than from a command, in the one artefact that gets read before the code. Recorded because the commit
cannot be rewritten and the correction has to live somewhere.

#### Fix

Nothing to edit; history stands. The counts here are the correction of record.

---

# §8 · Latent, not live

### T1 · `loop_act` is one shared trait across six loops, and `loop_solo` never writes it
**severity** LOW · **layer** GAME · **status** OPEN

`player.loop_act` is a single trait carrying "which act is happening" for every loop in the game.
`loop_cade` writes 1/2/3, `loop_sherrod` 1/2, `loop_isaac`, `loop_booth` and `loop_tobin` write 1.
Two `finish` nodes read it as exclusive bands.

Per N4 this is **guarded and correct today**: every NPC loop sets it at entry before any band can be
read, and five of six reset it to 0 on the `finish` exit. Probed live through
`loop_sherrod entry → act → finish` from a cold start, the right band rendered.

The residual is `loop_solo`, which sets `loop_stage` and never touches `loop_act`. It is safe only
because its `finish` has no bands. Add one — and adding variation to the loops is exactly what §4
asks for — and it will read whatever the last NPC loop left in the variable.

### Fix

Either set `loop_act` at `loop_solo.base` the way the other five do, or split the trait per loop.
The first is one line and matches the existing pattern.

---

# §9 · Checked and cleared — do not re-investigate

The most valuable section in a file like this. Each row was suspected, checked, and found correct;
each carries the evidence so nobody spends the hours again.

### The `engine.md` 27 clamp truncation does not bite

`v2_state.json` carries a live worry: *"a `costs` deduction is hard-clamped and truncates a balance
above 100 — keep priced rungs cheap and the balance low, or she loses money on a purchase."* That
mitigation is impossible to honour here, because clearing a 260 obligation *requires* a balance
above 100. So it was tested rather than assumed. Live, on the clean build:

```
buy_propane ($26)     money  50 -> 24     99 -> 73     120 -> 94     300 -> 274
buy_gas     ($20)     money  60 -> 40                              300 -> 280
work_counter (+74)    money  95 -> 169
```

No truncation at any balance, and income past 100 is fine. **The worry should be closed, not
carried.**

### `drawer_key` is not a dead write

A flag audit flags it: set once in `open_dorn_leaves`, read by zero conditions. It is read by
`[settings.rent] start_after_flag = "drawer_key"` — the rent engine, which no condition walk sees.
Confirmed in the built HTML. Any future flag audit will re-flag it; this note is why it should not
be deleted.

### The past-midnight schedules are correct

The trap in `schedule_past_midnight_two_entries` is that a day-specific overnight row needs **two**
rows while an all-days row needs **one**. This game gets both right:

```
npc_dorn    day-specific   [4,5,6] 22:30-23:59  +  [5,6,0] 00:00-05:30      TWO rows  ✓
npc_isaac   all days       [0..6] 21:00-01:00                                ONE row  ✓
npc_booth   all days       [0..6] 22:00-01:30                                ONE row  ✓
npc_sherrod all days       [0..6] 23:30-06:00                                ONE row  ✓
npc_tobin   all days       [0..6] 22:00-00:30                                ONE row  ✓
```

Every character has non-zero presence on every weekday except Dorn, who is absent Tue/Wed/Thu by
design — *"three nights his truck is in the lot and four nights it is not."* `v2_state.json` records
a live probe of the split; it holds.

### The three adjacent `[group]` bands in `loop_cade.finish` are correct

`adjacent_groups_merge_one_chain` warns that adjacent `[group]` blocks merge into one if/elseif
chain, so a second ladder placed next to a first is dead. Here the three adjacent groups are one
ladder — `loop_act eq 1` / `eq 2` / `eq 3`, mutually exclusive — and an if/elseif chain is exactly
the right compilation. Probed live at each value: all three bands render their own paragraph. Not
the trap.

### Missing media degrades gracefully in a clean build

Zero of 22 fixed references and zero of 34 pool directories are on disk, and it costs the player
nothing on a non-`--dev` build: no broken `<img>`, no console errors, no page errors. The media
block simply does not render. (The committed build is a different story — B1.)

### The pivot rule is clean, end to end

`CLAUDE.md` names this as the defect that shipped three increments running: *"read the beat's last
sentence; if it is about what the moment MEANS rather than what is HAPPENING, the beat has
pivoted."* Every explicit paragraph across all six loops was read for it. **Zero pivots.** Two are
worth naming as correct handling rather than luck:

- **Booth's finish** pivots mid-paragraph to meaning — *"when he says the title out loud, twice, and
  does not hear himself say it either time"* — and returns to the body to close: *"Your tits are in
  his face and both his hands are locked on your ass."*
- **Isaac's act** carries a meaning beat, *"Two words. It is the most he has said to you in eleven
  weeks"* — as **its own beat, after** the act beats, which is exactly what the doctrine licenses,
  and it still ends on the body.

Beat lengths in act nodes run 25–46 words against a 35–40 target. Finish paragraphs run 55–65 —
long, and defensible as terminal beats.

### The structure is clean

```
0  broken choice targets            0  canvases unreachable (no trigger, no inbound link)
0  nodes with no inbound link       0  references to a non-existent NPC
0  trigger locations that do not exist
0  conditions missing version="1.0"  (the conditions_version_failopen trap)
0  flags read but never set          0  traits read but never raised
13 day-cap flags, all set somewhere, all cleared in [engine.daily_tick]
```

### The crude ceilings — three exact, two open

`WANT.md` §7 declares a per-character vocabulary ceiling. Three are executed precisely:

- **Booth** — declared *"none — he cannot make himself say any of it"* and *"still calling her Mrs.
  Vance while he does."* Shipped: `"Mrs. Vance —"`, `"Mrs. Vance — Mrs. — I can't, if you keep —"`,
  and the finish narrating *"he says the title out loud, twice, and does not hear himself say it
  either time."*
- **Isaac** — *"mostly in narration — he still barely talks."* Shipped: a two-word line, and the
  narration that makes it the point: *"Two words. It is the most he has said to you in eleven
  weeks."*
- **Tobin** — *"full — and he is the only one using her name."* Shipped: `"Rilla. Get in."`,
  `"Rilla. Rilla. Look at me."`, and *"every stroke he says your name."*

**Cade and Sherrod are the open question.** Both ceilings are about crude *speech* — Cade's tier 3
is *"full — cum, and he says all of it out loud"*, Sherrod's tier 1 opens at *"cunt, tits — he
opens here, he never pretended"*. Neither carries a single crude word in any dialog line. Their
narration is fully crude; only their mouths are not.

Recorded as **open** rather than as a defect because both loops sit mid-ladder — `loop_cade` opens
at `want 42` of a declared 82, `loop_sherrod` at 34 of 62 — so tier 3 may be deliberately
unreleased. It needs LO's call, and it is the one place `CLAUDE.md`'s *"writing under the ceiling is
a defect"* may or may not apply.

### 22 shown-locked choices, but 5 doors

Gate *ends on an opening* reports `22 choices render visible-but-locked`, all 22 with a stated
reason, and the locked text is good work throughout. The 22 are three different things:

```
 6  day-caps and needs      "The book is straight for today."  "Get clean first."
11  within-loop ladder      "Let him cum — he is nowhere near it yet."
 5  the release's doors     the five loop entries, at want 42 / 50 / 38 / 34 / 70
```

`v2_state.json` says five and is right. Recorded so the gate's 22 is not read as 22 doors.

### ONE ASSET, ONE BLOCK is honoured

No `pool_dir` and no `file` is reused across two blocks — the rule from `one_asset_one_block_rule`,
which exists because media review dedupes by file and would return one verdict for two beats. Every
one of the 34 pools also carries `search_queries`, so the game is ready for find-media as it
stands.

### Walk-ins, hubs and meetings ARE presence-gated

25 canvases declare `requires_npc` — **6 one-shots, 8 `substitution_only` walk-ins, 11 portrait
hubs** — and all 25 reach the built HTML as non-null `requiresNpc`.

**⚠️ But `requires_npc` is not what holds 17 of them up, and this matters if anyone ever tidies the
file.** The field is consumed in exactly two runtime functions — `checkRandomEncounters`
(`v2.py:5245`) and `checkAndSubstituteCanvas` (`v2.py:5318`). The 6 one-shots and 11 hubs go through
`selectAutoFireCanvasForLocation` → `isCanvasValid` (`v2.py:4559`), which reads schedules, conditions
and repeatability and **never reads `requiresNpc`** (`gates.py:5114-5121` carries the trace).

They are correct anyway, and by the better mechanism: **all 17 carry both `trigger.schedules` and
`trigger.conditions`**, and each schedule mirrors that character's own rows — `hub_cade_office` is
06:30–09:00 and 18:00–20:30 Mon–Fri, which is exactly Cade's two office rows. The `requires_npc` on
them is belt-and-braces. **Do not delete those schedules on the theory that `requires_npc` covers
it.** The 8 walk-ins are `substitution_only`, which *is* one of the two consuming paths, so there the
field is load-bearing.

### The map data is complete, and `world reachable 14/14` is honest

Adjacency is `navigation_order`, not `connections` (§0a N5). All 14 locations declare theirs, the
graph is a connected two-level tree, and the engine supplies the return edge. A script that looks
for `connections` or `exits` will find nothing and be wrong.

### `ready_canvas` must name a canvas with a LOCATION, or Frame 2 renders nothing

`lookupCanvasBySlug` (`v2.py:15371`) walks `help_data.locationCanvases`, which is keyed by location
UUID, so a **triggerless** canvas is not in that index at all. Verified against the built HTML:
`hub_cade_office` is present with `hasSchedules: true`; `loop_cade` is absent. A card pointing
`ready_canvas` at a loop gets `null` back, Frame 2 does `if (!found) return ""`, and the card renders
**no frame** — text and 💡 tip with nothing ticked. All five in this game point at the hub, which is
also where the loop's door actually is. Do not "simplify" them to the loop slug.

### The portal already separates dev builds from releases, and this game is filed correctly

`games-data.js` has a `dev` field (`:10`) that renders a game under **Dev / test builds** with an
"Open" affordance instead of the main grid's "View", and a `version` field (`:11`) that names the
published build. `mrs_vance` has `dev: true` and no `version`: nothing about it is published. Do not
re-derive this — it is what makes B1 a release item rather than a blocker (§0a N7). What is *missing*
is enforcement, not the concept (B2).

---

# §10 · What this says about the skill

The `CLAUDE.md` test is *"would a correct author-game skill have prevented this?"* **Seven of the
twenty-one answer yes** — P1, C2, Q1, W1, G1 and B2 outright, D1 in part. **One of the seven is
fixed** (P1); the rest are recorded for LO to schedule.

### C2 · yes — and the fix is one token

`the-clock.md` C3 is correct, well-evidenced, and gated. The gate has a hole the size of the word
`to`. Nothing about the doctrine needs rethinking; the instrument needs one alternation extended
and a re-census. **This is the cheapest skill fix in the file and it ships again next game if it is
not made.**

Pattern worth naming: this is the third instrument hole of the same shape recorded in this skill —
`_band_texts` knowing `group` and not `block_pool`, `genre_words.txt` being structurally blind to
false friends, and now `_clk_refs` missing a preposition. In every case the doctrine was right and
the check was narrower than the doctrine.

### Q1 · yes — and the fix is shipped, in `engine.md` and in four other games' future

§23 warned that `terminal` is not computed from progress and gave the rule that follows — *terminal
belongs on a card the player has to CLIMB TO*. It never said **climb to what**, and every v2 game
answered the same wrong way. Measured across the repo:

```
mrs_vance     5 of 6 - two ON the door, three BEFORE it
forty_miles   6 of 6 - every badge at exactly the door value
seventh_day   1 badge on the door + 5 goals past anything the game reads
the_season    4 of 5
the_allowance 3 of 5
vesper        0 of 5   <- the v1 game §23 was WRITTEN FROM
```

**Four v2 games and not the one the section came from.** The doctrine did not fail; the sentence that
would have prevented this was never written. §23 now carries it — a meter is the wrong thing to gate
a badge on, put the ✓ on a flag the content sets on its way out — plus the goal-nobody-reads warning
and the `ready_canvas` trap. `lint_badge_before_content` reports all three.

**And the one-`terminal_text` cap was right for a different game.** `CHANGELOG.md` 2026-08-13 records
it coming from `vesper` 0.1.8, a **finished** build where four arcs genuinely had ended and
*"Arc complete"* was true of them. In a v0.1 nothing is closed, so the cap forced five tracks into a
**stronger and falser** claim than the string it was rationing — and `the-release.md:109` already
asked for *"a plain marker at the top of each track"*. The cap is now on the **claim**, not the field.

This is the second time in this file a rule turned out to be correct but scoped to the wrong phase —
B1/N7 was the first. Worth naming: **a rule measured on a finished game is not automatically a rule
about a first release.**

### W1 · yes — and this is the second game to draw the same sentence from LO

`the_season` was reported with *"I don't know who is who"*, and Mrs. Vance was reported with *"for
many npcs, it still sounds unclear like who is who."* Two games, two casts, the same complaint. The
skill has a 7-step npc-intro and nothing at all about **keeping** a name attached to a person once
the introduction is over — no rule that prose re-anchors a relationship, no check that counts
whether it does. 31 kin words in 10,298 is what "no rule" looks like.

### G1 · yes — and it is the largest of the five

`the-want.md` has no step comparing a new premise against the games already in the repo, and its §2
mandates a single shape. Seven of eight shipped appetites open with the same four words. This one is
not a Mrs. Vance defect at all; it decides what the *next* game can be.

### D1 · partly — right about doors, over-applied everywhere else

Gate 42 and `the-release.md:110` are correct that a locked door must say why, and the five real doors
here are good work. Neither doctrine says anything about the other 27 sites, so an author with no
guidance applied the door rule to cooldowns and to mid-scene arousal gates. The rule needs a scope,
not a reversal.

### P1 · yes — and the fix is shipped

The narrowest instrument hole in the file, and the one that had the most already written about it.
`gates.py:5114-5121` states outright that `requires_npc` is consumed on exactly two paths, and G38
then judges the third. Nothing looked at the path that reads the field.

`lint_ambient_presence` now does (`gates.py`, next to `lint_dialogue_attribution`). On this game it
would have reported **20/21** before the repair and reports **4/21** after. It is the fourth
instrument hole of this shape recorded here — `_band_texts` knowing `group` and not `block_pool`,
`genre_words.txt` blind to false friends, `_clk_refs` missing a preposition, and now G38 aimed at the
wrong runtime path. **In all four the doctrine was right and the check was narrower than the
doctrine**, which is worth naming as a pattern rather than fixing four times.

One thing the lint says about the corpus rather than this game: `mrs_vance` is the **only** v2 game
with a speaking character in a random ambient. The other seven ship 46 random canvases between them
and **not one** has a voice in it. Their ambients are weather; this game's are people. That is a real
difference in what the game is, it is the reason this defect could only appear here, and it is worth
knowing before the next game decides which kind of ambient to write.

### B2 · yes — and it is the one the skill is named for

`the-release.md` is the file called *The Release* and it describes a release as a **unit of authored
content** — what a release adds, how the loop runs, what cadence to hold. It says nothing about the
**act of publishing a build**, which is the other half of the same word. So the procedure had to be
invented somewhere, and it was: nine times, by hand, in a data file's comments (B2).

This is a different shape from the other four. C2 and Q1 are a correct doctrine with a narrow
instrument. This is a **doctrine-shaped hole** — no one taught it wrong, no one taught it at all, and
the authors kept solving it locally and correctly without anywhere to put the answer. Those are the
ones that stay invisible longest, because every individual game looks fine.

### The rest are GAME-layer

B1 is a build command, and per §0a N7 the right one for this phase. R1 had the doctrine — `engine.md` §35 is three pages long and names the
field games — and the author read it and pooled 35 canvases; the loops were a judgement, not an
ignorance. S1/S2 and L1–L3 are ledger discipline the skill already teaches in `the-release.md`. E1
is a design question. M1/M2 sit
between: `the-first-hour.md` F7/F9 teach the first visit and the lint prints the list, so the
doctrine is there and was not followed — but nothing in the skill teaches showing the player the
*shape* of a map. **The skill taught most of these right.**

---

# §11 · Method

Recorded so the file is reproducible rather than believed.

**Source.**
- `scripts/merge_toml_phases.py games/mrs_vance` re-run and the result diffed against the committed
  `7_final_game.toml` — byte-identical, so the build and the source agree.
- ⚠️ **One census in this file was built on prose-matching and was wrong in both directions** — see
  §0a N8. Character names in narration are not who is *present*; a `dialog` block's `props.npcId`
  is. Where a fact about a canvas exists structurally, read the structure.
- `7_final_game.toml` parsed with `tomli`, never grep. The canvas graph walked for reachability,
  broken targets, dead nodes, NPC references and condition versions. Flags and traits counted by a
  generic recursive walk with a path, after a first pass using assumed key names produced a
  false "21 flags read but never set" — `flagEffects` is a separate key from `effects`.
- `PYTHONHASHSEED=0 python3 .claude/skills/author-game-v2/scripts/gates.py mrs_vance` captured
  before and after the review and diffed: identical, so nothing here moved what it measures.

**Build.**
- A clean `package_from_toml … --gen-version v2` to scratch, with no `--dev`, for the B1 comparison.

**Live.** Headless Chromium against both builds:
- The age gate and the whole opening funnel, click by click: `open_boot` → `open_dorn_leaves`
  (three nodes) → `first_office` → `meet_cade` → the Office location screen → `hub_cade_office`.
- `block_pool` cycling: six renders of `hub_cade_office`, three distinct variants.
- The finish bands: `loop_cade.finish` at `loop_act` 0/1/2/3, and `loop_sherrod` walked
  entry → act → finish from a cold start.
- The money clamp: four balances through `buy_propane`, two through `buy_gas`, one income click.
- The sleep landing: five start times through `act_sleep`, reading `game_state.time_state` before
  and after.
- The quest page at all-meters-zero and at every-door-open.
- `standing` bands in `work_counter` at 5 / 25 / 60.

**⚠️ One probe trap, paid for here so it is not paid for again.** Player traits live at
`State.variables.player.core_traits.*`. Writing to `State.variables.player.*` silently creates a
stray key, the condition reads the real one, and **the screen renders as though the band were
broken.** The first pass at the finish bands produced a convincing false defect this way — "no
explicit paragraph renders at any `loop_act` value" — that survived until the variable tree was
dumped. SugarCube globals are also not on `window` directly in a page-eval context; reach them
through `window.SugarCube.{State,Engine,setup}`.

---

# §12 · Found by LO playing the build

Opened 2026-08-25, from LO's play-report on the shipped v0.1. Five reports, investigated the same
day. Three are defects, one is a doctrine question the skill and LO disagree on, and one is a gap in
the skill that has nothing to do with this game. The investigation also produced §0a's N5 and N6.

---

### P1 · Fifteen random ambients put a speaking character in a room the panel says he is not in
**severity** HIGH · **layer** GAME + SKILL · **status** **FIXED** — 16 gated, proved live, 1 open writing call

> LO: *"in the navigation panel where I see npc present or not, it doesn't shows up and it
> automatically fires up."*

**⚠️ This item's own census was wrong in four numbers and three verdicts.** It was rebuilt by reading
all 36 ambients rather than matching names in prose; §0a N8 records what moved and why. The
corrected figures are below and the ones in the first draft should not be quoted.

#### What is actually there

```
91 canvases
 ├─ 36  random ambients        trigger_mode = "random"
 │       ├─ 21  a cast member SPEAKS in it   <- the population that can lie about presence
 │       └─ 15  unpeopled texture            <- nothing to misplace
 ├─ 25  declare requires_npc   6 one-shots · 8 substitution_only walk-ins · 11 portrait hubs
 └─ 30  other
```

Of the 21 that put a man on screen, **one** was gated — `amb_kitchen_friday`, and it was gated
correctly, with the primitive the other twenty needed. The remaining twenty carried no
`requires_npc`, no `conditions` and no `schedules` of their own.

The runtime is explicit (`v2.py:5260`):

```javascript
if (!canvNpc.requiresNpc) {
    afterNpcGate.push(canvNpc);   // no gate = always allowed
    continue;
}
```

So `amb_office_close` — Cade bringing the roller door down at six — sat in the eligible pool at
02:00, when `setup.getNpcLocation('npc_cade')` returns `null`. `amb_bunk_radio` put Isaac on his bed
at 10:00 against an 08:00–11:00 shop-floor row. The three `sherrods_room` ambients were eligible at
noon against a 23:30–06:00 row. The navigation panel reads presence from the same schedules and was
right every time — which is the mismatch LO saw, and why it matters more than one wrong scene: a
panel that is wrong once stops being read, and the panel is how a sandbox is navigated.

#### `requires_npc` was the wrong tool for two of them

`requires_npc` binds **exactly one** NPC and has no absence form (`engine.md:561-580`, §20, verified
live in a built game). Two canvases need more than that, and `amb_kitchen_friday` already showed how:

```toml
conditions = { version = "1.0", logic = "AND", items = [
  { type = "npc_at_location", location_id = "the_kitchen", npc_id = "npc_dorn", operator = "is_present" },
] }
```

#### The fix, as applied

**15 canvases gained one line of `requires_npc`**, each on the character who has to be in the room,
and each with a window in that character's own schedule so nothing is gated into never firing:

| canvas | location | gate | the NPC's own rows there |
|---|---|---|---|
| `amb_booth_room_talk` · `amb_booths_door` | `booths_room` | `npc_booth` | 22:00–01:30 daily |
| `amb_sherrod_history` · `amb_sherrod_owed` · `amb_sherrod_stairs` | `sherrods_room` | `npc_sherrod` | 23:30–06:00 daily |
| `amb_bunk_radio` · `amb_bunk_stairs` · `amb_bunk_two_of_them` | `the_bunk_room` | `npc_isaac` | 21:00–01:00 daily |
| `amb_row_late` | `the_back_row` | `npc_tobin` | 22:00–00:30 daily |
| `amb_shop_hatch` | `the_shop_floor` | `npc_tobin` | 08:00–17:00 Mon–Fri |
| `amb_shop_morning_talk` | `the_shop_floor` | `npc_cade` | 09:00–17:30 Mon–Fri |
| `amb_office_close` | `the_office` | `npc_cade` | 18:00–20:30 Mon–Fri — the hour its prose names |
| `amb_kitchen_five_adults` | `the_kitchen` | `npc_booth` | 16:00–19:00 Mon–Fri |
| `amb_bay_after` | `the_wash_bay` | `npc_isaac` | 11:00–14:00 Mon–Fri |
| `amb_yard_wash_car` | `the_yard` | `npc_booth` | 13:00–17:00 Sat–Sun — *"That's Saturday here"* |

**Gate on the one who has to be there, not everyone named.** Tobin speaks in both bunk-room scenes
and **has no bunk-room row at all**, so gating on him would have killed both. In `amb_yard_wash_car`
his yard row is Saturday 09:00–12:00 against Booth's 13:00–17:00 — they never overlap. Isaac and
Booth are the residents; they are the gate. Tobin standing there is a writing question, not a
mechanical one.

**`amb_office_phone` gained the two-item condition**, because it is the case that proves the
primitive:

```toml
conditions = { version = "1.0", logic = "AND", items = [
  { type = "npc_at_location", location_id = "the_shop_floor", npc_id = "npc_cade", operator = "is_present" },
  { type = "npc_at_location", location_id = "the_office",     npc_id = "npc_dorn", operator = "is_absent"  },
] }
```

Dorn has to be **away** — he is calling from a lay-by — and Cade has to be **in a different room**
from the canvas, because the scene says *"He's in bay two"* before he comes through the hatch. One
NPC by absence and one by a foreign location: `requires_npc` can express neither.

#### Three left alone, and the reason is in the prose

| canvas | why it is already correct |
|---|---|
| `amb_bathroom_water` | Booth *"says it through the door on his way past and does not stop walking"* |
| `amb_bathroom_landing` | *"Two of them are on the landing"* — the scene **is** being overheard through a gap the bolt will not close |
| `amb_office_wrecker` | the small hours, and *"He is dressed. He has come from somewhere that is not a bed"* — the off-schedule arrival is the whole scene |

The live check below catches `amb_office_wrecker` firing 70 times at 02:00 with Cade nowhere on the
property, which is exactly what it is written to do.

#### One left open — a writing call, not a gate

**`amb_kitchen_house`.** Booth is in the kitchen at night — *"you come down for water in what you
sleep in"* — but his kitchen row is 16:00–19:00 on weekdays and his night row is his own room.
Gating him would move the scene to teatime and contradict its own first sentence. Three honest
answers: leave it, narrate his arrival the way `amb_kitchen_five_adults` narrates Sherrod's, or give
Booth a short late row in the kitchen. Not decided here because all three touch authored prose or
the world model, and neither is what this pass was for.

#### Proved live, which the first draft could not do

The first draft recorded *"the mechanism is certain; a captured instance is not in hand"*, because
ambient chances run 0.26–0.35 and a walker rarely catches one. Driving
`setup.checkRandomEncounters()` directly, 400 times per hour, settles it in both directions:

```
the_bunk_room, Monday 10:00   isaac -> the_shop_floor
    amb_bunk_radio 0 · amb_bunk_stairs 0 · amb_bunk_two_of_them 0
    amb_bunk_partition 122          <- the ungated control, same 400 rolls
the_bunk_room, Monday 22:00   isaac -> the_bunk_room
    radio 68 · stairs 78 · two_of_them 85 · partition 84

the_office, Monday 02:00      cade -> null
    amb_office_close 0              <- gated out
    amb_office_wrecker 70           <- deliberately ungated, and correct
the_office, Monday 19:00      cade -> the_office
    amb_office_close 69 · amb_office_phone 0    <- cade is in the office, not bay two
the_office, Monday 10:00      cade -> the_shop_floor
    amb_office_phone 95             <- both condition items true
```

Zero page errors, zero console errors, 10/10 checks. **The harness is committed** —
`games/mrs_vance/playtest_presence.py`, the same shape as `games/forty_miles/playtest.py`, so the
claim is re-runnable rather than believed. It takes a build path because `output/` is still the
pre-P1 artefact and stays that way until release (§1 B1).

`amb_bunk_partition` is the control that makes the first block mean something: nobody speaks in it,
so it is ungated by design, and it firing 122 times at the same hour the gated three fire zero is
what shows the gate did the silencing and not some unrelated filter.

#### Why no check caught it — and this is the skill half

The first draft said *"No gate reads `requires_npc` at all."* **That is false and is corrected in
§0a N8.** `gates.py` reads the field 12 times and G38 *"a meeting fires where they are"* is built
entirely on it.

The real miss is narrower and worse. `gates.py:5114-5121` already carries the trace:

> `requires_npc` **DOES NOT DO THIS** … `isCanvasValid` (`v2.py:4559`) reads schedules, conditions
> and repeatability and **NEVER reads requiresNpc**. Repo-wide the field is consumed in exactly two
> functions — `checkRandomEncounters` (`v2.py:5245`, `trigger_mode="random"`) and
> `checkAndSubstituteCanvas` (`v2.py:5318`, `substitution_only`).

G38 then skips both of those and judges the auto-fire path — the one that does not read the field.
**The single path that consumes `requires_npc` had no check on it.** The doctrine was right and the
instrument was pointed at the wrong path, which is the failure shape `SKILL.md` names.

#### The skill fix, shipped in the same commit

`lint_ambient_presence` in `gates.py`, next to `lint_dialogue_attribution` which it extends: every
`trigger_mode = "random"` canvas with a `dialog` block carrying an `npcId` and none of
`requires_npc`, an `npc_at_location` condition, or its own `trigger.schedules`.

It splits the finding into the two different jobs, which is the point — `gate it on <name>` when the
speaker has rows at that location, `or narrate the arrival — no row here to gate on` when he does
not, because there a gate would strand the canvas forever.

```
mrs_vance BEFORE   20/21 ambients where somebody speaks carry no presence gate
mrs_vance AFTER     4/21   — bathroom_water · bathroom_landing (or narrate)
                             kitchen_house · office_wrecker    (gate it)
```

A LIST and never a gate: an ambient may legitimately place someone off-schedule, and only the author
can tell that from the defect. Both verdicts are exercised in that four-row output.

**It is ahead of the corpus, not a no-op.** Across every v2 game, `mrs_vance` is the **only** one with
a speaking character in a random ambient — 46 random canvases in the other seven games, **zero** with
a speaker. It reports nothing on them because there is nothing there, and it bites the moment a
second game puts its cast inside its texture. `41/41 judged gates pass` before and after; the lint
touches no tally.

#### One thing this did not fix, recorded

`amb_kitchen_friday` says *"on a Friday"* and its Dorn condition admits Friday **and** Saturday, since
Dorn's kitchen row is 19:00–22:00 on both. A one-day slippage, far smaller than the first draft
implied. `amb_yard_wash_car` had the same shape — *"That's Saturday here"* — and the Booth gate
closed it, because his only yard row is Sat–Sun.

---

### D1 · The "why it is locked" text runs to 32 sites across three systems
**severity** MED · **layer** GAME + SKILL — a question for LO, not a defect call · **status** OPEN

> LO: *"I didn't liked showing the why text for locked choices."*

```
10  show_when_blocked + cooldown_message    greyed on the ROOM screen, re-read every day
11  show_when_locked, inside the sex loops   "Let him cum — he is nowhere near it yet."
 6  show_when_locked, day-caps and needs     "The book is straight for today."
 5  show_when_locked, the loop entries       the release's five actual doors
```

**The five doors should keep their reason.** `SKILL.md:70` says gate 42 exists *"because our locked
doors are mute"*, and `the-release.md:110` is *"An honest wall is a promise; a silent one is a bug
report."* Strip those and the player climbs a meter with nothing telling them what it buys.

**The other 27 are the noise, and the 11 inside the loops are the worst of them.** A locked choice
mid-scene — *"Let him cum — he is nowhere near it yet"* — is the machinery explaining its own
arousal threshold at the one moment the fiction should be the only thing on the screen. The 10
room-screen cooldowns are re-read daily and say nothing a greyed-out item would not.

Recorded as a question rather than a defect because it is a scope decision on a rule that is right
where it was aimed. The skill never gave the door rule a boundary, so it got applied to everything
that can be locked.

#### Fix

Split it: keep `locked_text` on the five loop entries, drop `show_when_locked` from the 11 in-loop
ladder gates, and drop `show_when_blocked` from the 10 cooldowns. Then give the doctrine the missing
scope sentence — a *door* says why, a *cooldown* does not.

---

### M1 · Thirteen of fourteen locations never say what kind of place they are
**severity** HIGH · **layer** GAME · **status** OPEN

> LO: *"couldnt understand the world, the map, locations."*

The gate reports `5/14 locations carry one` and passes. Split by what the covering canvas actually
does:

```
the_office       first_office                  <- the ONLY canvas that describes a PLACE
the_office       meet_cade, meet_sherrod          a person, who happens to stand there
the_shop_floor   meet_tobin                       "
the_wash_bay     meet_isaac                       "
the_kitchen      meet_booth                       "
your_room        open_dorn_leaves                 "
9 locations      nothing at all
```

So the honest number is **one**. Four of the five "covered" locations are covered by a character
introduction that happens to be sited there; walk into the wash bay before meeting Isaac and nothing
has ever told you it is a place where trailers get hosed out.

**`the_yard` is among the nine with nothing** — the exterior, the root of the map, and the screen
the player crosses more than any other. Its `description` is good and carries the entire geography:

> *"Gravel from the back step of the house to the roller door of the shop, wide enough to turn a rig
> on… The county road goes past the gate and everything on this property opens onto this."*

A description renders under the room title on every visit. It is wallpaper, not an arrival, and
`the-first-hour.md` F7/F9 is about the moment of arriving.

#### Fix

First visits for the nine, starting with `the_yard`, `the_bunk_room` and `the_back_row` — the three
carrying the most prose with no introduction. `v2_state.json` already promises this; it is unpaid.

---

### M2 · The map is a two-level tree and the player is never shown its shape
**severity** MED · **layer** GAME + SKILL · **status** OPEN

What is declared, via `navigation_order` (§0a N5):

```
the_yard ─┬─ the_office ─── sherrods_room
          ├─ the_shop_floor ─┬─ the_bunk_room
          │                  └─ the_wash_bay
          ├─ the_kitchen ─┬─ your_room
          │               ├─ the_bathroom
          │               └─ booths_room
          ├─ the_back_row
          └─ kerr_crossing ─┬─ the_bank
                            └─ the_bar
```

Correct `nested_zones`, and mechanically sound — the engine adds the `Leave <name>` edge back up, so
every room is reachable and the gate's `14/14` is true.

What the player sees is a flat list of bare nouns. From the Yard: `Office · Shop Floor · Kitchen ·
Back Row · Kerr Crossing`. No grouping into house / shop / outside / town. **Six locations never
appear on any list the player is looking at**, because they are one level further down. Getting from
`your_room` to `the_wash_bay` is four moves through two parents and nothing anywhere says so.

`board.map.shape` already contains the sentence that would fix it — *"a diesel repair yard on a
county road: gravel between a house and a four-bay shop, a row of overnight trucks at the far end,
and a crossroads twenty minutes down the road"* — and it exists only in the ledger, where no player
will ever read it.

**Skill layer:** `the-map.md` specifies archetypes and the graph. Nothing in it asks how the player
learns the shape, so a correct `nested_zones` map can ship completely illegible.

#### Fix

Group the travel list by zone, or put the shape into the yard's first visit (M1) so the player is
told once that the house, the shop and the back row all hang off this gravel.

---

### W1 · Six men, and the prose says who they are 31 times in 10,298 words
**severity** HIGH · **layer** GAME + SKILL · **status** OPEN

> LO: *"For many npcs, it still sounds unclear like who is who."*

Every kin word in the game's canvas prose:

```
husband 8 · brother 8 · wife 6 · father 4 · son 2 · youngest 2 · eldest 1     = 31
```

The `npcs[].relationship` strings are excellent and land it in six words — *"Your husband's eldest,
29"*, *"Your husband's middle son, 24"*, *"Your husband's brother, 51"*. **They live on the cast
page.** In the prose the player reads, the six are Cade, Booth, Isaac, Sherrod, Tobin and Dorn: six
men, five surname-shaped first names, no ages, no nicknames, four of them Vances and two of those
interchangeable on the page (Isaac 24 and Cade 29 are both grown sons who work the yard).

The game owns the perfect device and does not spend it. **They call her Mrs. Vance; she calls them
nothing.** The title is the premise, it is asymmetric, and *"your husband's eldest"* is three words
that could ride in every Cade ambient without costing the register anything.

**Skill layer, and the load-bearing half:** `the_season` drew the same sentence from LO — *"I don't
know who is who."* Second game, same failure, so it is the instruction set and not the author. The
skill teaches a 7-step npc-intro and says nothing about **keeping** a name attached after the
introduction, and no gate or lint counts whether prose re-anchors a relationship.

#### Fix

A kin-anchor in the recurring surfaces, not the one-shots: each character's hub and ambients carry
their relation once. Then a lint that reports kin-words per character per 10k words, so the next game
cannot ship at 31.

---

### G1 · Eight games, one Want shape — and nothing checks a new premise against the repo
**severity** MED · **layer** SKILL · **status** OPEN

> LO: *"when it suggests some ideas, it goes and check the existing v2 games and made sure that new
> game doesnt matches the current ones."*

**No such step exists.** `the-want.md` has six sections and a closing test, and none asks whether the
repo already contains this game. The only differentiation language anywhere in the skill is about
meters *within* a game (`the-want.md:48`, `the-board.md:250`).

Mrs. Vance is **not** a repeat. Its appetite — *to be wanted by men who have to call her by a title
she did not earn* — is genuinely its own. The pattern is one level up:

```
back_home      24   "To be wanted — not looked after, not tolerated, not managed..."
forty_miles    26   "To be wanted by men who have nowhere else to be at 3am"
off_season     39   "To be wanted -- not needed, not thanked, not worried about..."
seventh_day    21   "To be wanted by the men whose entire authority over her is telling her no"
the_allowance  19   "To be wanted by the people who set her price"
the_season     23   "To be wanted by men she shares a wall with"
mrs_vance      27   "To be wanted by men who have to call her by a title she did not earn"
steam          31   "To be necessary to people at the moment they have nothing on"
```

**Seven of eight open with the same four words.** All eight are a woman aged 19–39 held in place by
money she cannot reach. Three of eight are a rural compound where she is the young woman among men.

The fictions differentiate; the shape does not — because `the-want.md` §2 mandates it. The section is
titled *"the appetite that never fills."* So the check LO describes would not have caught anything
about this game's premise. It would have caught this, which is larger and decides what the next game
can be.

#### Fix

Two separate things, and only the first is small: a step in `the-want.md` that reads the other games'
`v2_state.json` want blocks before a premise is proposed; and a decision about whether §2's shape is
the genre or merely the first shape measured. That second one is not a fix, it is a study.

---

---

# Appendix A · The measurements

Everything quoted above, in one place.

### A.1 · The scoreboard

```
41/41 judged gates pass · 1 n/a (no [[clothing]] catalog declared)
location fill      14 locations · 10,298 words vs 11,400 declared · 14/14 on budget · anchor 27%
explicit floor     14.0% of 107 beats carry 3+ explicit words (floor 7.5%)
explicit repeat    100.0% of 15 explicit beats are re-enterable (floor 50%)
narration:dialogue 4.9:1 — 1,760 spoken of 10,298 (ceiling 5:1) · field median 2.93:1
sentence length    median 9 words across 796 sentences (ceiling 14) · field median 10
speakers named     212/212 dialog and thought_bubble blocks
traversal heat     14/14 locations carry a cycling explicit pool
```

### A.2 · The prose pools

```
39 block_pool blocks across 35 canvases
   variants:   21 pools of 3   ·   11 of 4   ·   7 of 2
   children:   32 paragraph    ·   13 dialog   (6 pools mix the two — importer WARNs, builds)
   nesting:    0 pools inside pools           depth cap is 4 (template_import.py:6143)
   in loops:   0 of 20 loop nodes

cross-game census, 22 scorable games:   mrs_vance 39 · vesper 6 (v1) · all others 0
```

### A.3 · The economy

```
sources (+/day, all day-capped)   counter 74 · trailer 62 · parts 34 · books 22 · walkround 16
                                  = 208/day, 72 energy
sinks                             propane 26 · gas 20 · drink 16 · parts 14 · wash-bay supplies 2
obligation                        260/week, Friday, grace 1, eviction_mode = flag_set -> cade_covered
starting money                    18
energy                            start 55 · decay 22/day · sleep +70 (cap 100)
clean                             start 30 · decay 18/day · house wash +55 free · bay +45 for $2
```

### A.4 · The meters

```                     set   read      declared rungs                 highest gate built
player.standing         25      4      —                              —
player.arousal          42      8
player.loop_stage       25      3
player.loop_act         20      5
player.clean            14      2
player.energy            6      3
player.money             5      0 conditions / 5 cost sites
npc_isaac.want          10      4      5, 18, 38, 66                  38
npc_booth.want           8      1      6, 16, 30, 50, 74              50
npc_tobin.want           8      2      8, 30, 70                      70
npc_booth.trust          7      3
npc_cade.trust           7      4                                     26
npc_sherrod.want         7      2      4, 15, 34, 62                  34
npc_cade.want            6      1      5, 14, 26, 42, 60, 82          42
npc_dorn.want            2      0 conditions / 2 quest cards   12, 55        —
```

### A.5 · Presence

```                minutes covered per weekday (0 = Mon)
npc_cade      810 810 810 810 989 209  30      zero days: none
npc_booth     390 390 390 390 390 450 450      zero days: none
npc_isaac     600 600 600 600 600 240 240      zero days: none
npc_sherrod   600 600 600 600 600 390 390      zero days: none
npc_tobin     690 690 690 690 690 330 150      zero days: none
npc_dorn      435   -   -   - 269 599 419      zero days: Tue, Wed, Thu  (by design)
```

### A.6 · The five doors, and where the badge used to sit

```
hub_cade_office     -> loop_cade      npc_cade.want gte 42
hub_booth_room      -> loop_booth     npc_booth.want gte 50
hub_isaac_bay       -> loop_isaac     npc_isaac.want gte 38
hub_sherrod_office  -> loop_sherrod   npc_sherrod.want gte 34
hub_tobin_row       -> loop_tobin     npc_tobin.want gte 70
```

All five `show_when_locked` with a written reason. `loop_solo` is ungated.

⚠️ **Put beside the quest cards, this table is Q1.** The whole defect was visible from two tables
this file already contained, and nobody put them side by side (§0a N9):

```
character   the door          the badge fired at      after the repair
cade        want   gte 42     trust gte 26  (!)       flag cade_loop_played
booth       want   gte 50     trust gte 30  (!)       flag booth_loop_played
isaac       want   gte 38     want  gte 38            flag isaac_loop_played
sherrod     want   gte 34     want  gte 34            flag sherrod_loop_played
tobin       want   gte 70     want  gte 30  (!!)      flag tobin_loop_played
dorn        (no door)         want  gte 55            want gte 12, the wall stated
```

Every `gte` threshold any canvas condition reads, which is what "content" means here:

```
booth.trust  5, 30     booth.want   50        cade.trust  6, 26     cade.want  42
isaac.want   6, 38     sherrod.want 5, 34     tobin.want  5, 70     dorn        none

asked for by a card and read by nothing:  isaac.want 66 · sherrod.want 62 · tobin.want 30
```

### A.7 · The presence gate

⚠️ **Re-measured 2026-08-25 while repairing P1; the first version of this table was wrong.** See
§0a N8. The signal is a `dialog` block's `props.npcId`, not a character name in the narration.

```
91 canvases
 ├─ 36 random ambients   trigger_mode = "random"
 │      ├─ 21  a cast member SPEAKS in it        <- can lie about presence
 │      └─ 15  unpeopled texture
 ├─ 25 declare requires_npc   6 one-shots · 8 substitution_only walk-ins · 11 portrait hubs
 │      all 25 reach the built HTML as a non-null "requiresNpc"
 └─ 30 other

the 21 that put somebody on screen        BEFORE      AFTER
  requires_npc                                 0         15
  npc_at_location condition                    1          2
  own trigger.schedules                        0          0
  ---------------------------------------------------------
  no presence gate of any kind                20          4
                                                          ├─ 2 "or narrate" — no row at that location
                                                          └─ 2 "gate it"    — 1 open writing call,
                                                                              1 deliberate (the 02:00 arrival)

which runtime path reads requires_npc
  checkRandomEncounters      v2.py:5245  trigger_mode = "random"        YES
  checkAndSubstituteCanvas   v2.py:5318  substitution_only              YES
  isCanvasValid              v2.py:4559  one-shots and hubs             NO   <- schedules hold those up
  the gate itself            v2.py:5260  no requiresNpc = always allowed

live, 400 forced rolls per hour (chance is 0.26-0.35, so a walker will not catch these)
  the_bunk_room  Mon 10:00  isaac -> the_shop_floor   radio 0 · stairs 0 · two_of_them 0 · partition 122
  the_bunk_room  Mon 22:00  isaac -> the_bunk_room    radio 68 · stairs 78 · two_of_them 85 · partition 84
  the_office     Mon 02:00  cade  -> null             office_close 0 · office_wrecker 70
  the_office     Mon 10:00  cade  -> the_shop_floor   office_phone 95
  the_office     Mon 19:00  cade  -> the_office       office_close 69 · office_phone 0
```

### A.8 · The map, as declared by `navigation_order`

```
the_yard          -> the_office, the_shop_floor, the_kitchen, the_back_row, kerr_crossing
the_office        -> sherrods_room
the_shop_floor    -> the_bunk_room, the_wash_bay
the_kitchen       -> your_room, the_bathroom, booths_room
kerr_crossing     -> the_bank, the_bar
(the other 8      -> leaf)
```

Every edge is authored one-way; the engine adds the return (`v2.py:19807`). Root is `the_yard`, which
nothing lists — it is reached only by leaving a child. Max depth 2.

### A.9 · Kin words in canvas prose

```
husband 8 · brother 8 · wife 6 · father 4 · son 2 · youngest 2 · eldest 1   = 31 in 10,298 words
```

### A.10 · The eight v2 want-lines, opening clause

```
back_home      24    "To be wanted — not looked after, not tolerated, not managed"
forty_miles    26    "To be wanted by men who have nowhere else to be at 3am"
off_season     39    "To be wanted -- not needed, not thanked, not worried about"
seventh_day    21    "To be wanted by the men whose entire authority over her is telling her no"
the_allowance  19    "To be wanted by the people who set her price"
the_season     23    "To be wanted by men she shares a wall with"
mrs_vance      27    "To be wanted by men who have to call her by a title she did not earn"
steam          31    "To be necessary to people at the moment they have nothing on"
```

### A.11 · The lock sites

```
show_when_blocked  (room screen, greyed)   10
show_when_locked   inside the sex loops    11
show_when_locked   day-caps and needs       6
show_when_locked   the loop entries         5
                                          ---
                                           32
```

---

# Log

**2026-08-25 — opened.** Thirteen items, all `OPEN`: B1 (blocker), C1/Q1/R1 (high), C2/S1/S2
(med), Q2/T1/L1/L2/L3 (low), E1 (open question). Four self-corrections recorded in §0a before anything else
was written. `v2_state.json` and the skill deliberately untouched — this pass records, it does not
repair.

**2026-08-25 — §12 added, from LO playing the build.** Six items: P1/M1/W1 (high), D1/M2/G1 (med;
D1 and G1 are questions rather than defect calls). Two further self-corrections, N5 and N6, appended
to §0a — the map data and the presence gate were both wrongly called broken in chat before being
read properly, and both are correct. §9 gained the two matching cleared rows so neither is
re-investigated. Count 13 → 19. Still nothing repaired.

**2026-08-25 — L4 added.** Reconciling §4's pool count against the shipping commit before committing
this file showed the commit's "46 pools" matches neither the grep (41) nor the parse (39), and its
"46 in the_long_summer" is 49. Filed with L1–L3 as the same defect class. Count 19 → 20.

**2026-08-25 — Q1 and Q2 FIXED, and Q1's own diagnosis corrected.** The badge is no longer gated on
a meter. Repairing it overturned Q1's *"gated at the same value as the content"* — true for Isaac and
Sherrod, but Tobin's ✓ arrived 40 points early and Cade's and Booth's were gated on a **different
meter** from the one their door reads, so the tick could land at `want 0`. Recorded as **N9**, found
by putting the cards next to A.6's door values — two tables this file already contained.

It also turned up **three goal thresholds no condition in the game reads** (`isaac.want 66`,
`sherrod.want 62`, `tobin.want 30`), invisible only because the terminal frame outranked the bullets.
Q1's original fix note — *raise each terminal card's `when`* — would have turned all three into live
instructions to grind for nothing.

**Applied.** Six ladders rebuilt to three states, 14 cards → 21: climb (🎯 with live progress), ready
(🔓 + 📍 + 🕒 off the **hub**, never the triggerless loop), done (✓ on a `<x>_loop_played` flag five
`flagEffects` entries now set on each loop's `finish` exit). The three phantom thresholds are cut.
Dorn keeps two cards and loses the 55 that left him rendering no frame at all between 12 and 54.
All six carry the same plain wall marker.

**Proved live**, `games/mrs_vance/playtest_quests.py`, 23/23, zero page errors: three frames per
character in the right order, the Ready frame asserted on its **📍** rather than on non-emptiness
(a `ready_canvas` that fails to resolve returns `""`), and all five loops played through to their
finish node with each flag going `False -> True`.

**Skill fix in the same commit.** `engine.md` §23 gains the sentence that would have prevented it —
*a meter is the wrong thing to gate a badge on* — plus the goal-nobody-reads warning and the
`ready_canvas`/`locationCanvases` trap, and the one-`terminal_text` cap is rescoped to a finished
game. `lint_badge_before_content` reports all three: **8 findings on this game before, 0 after**, and
across the corpus `forty_miles` 6/6, `seventh_day` 6, `the_season` 4/5, `the_allowance` 3/5 — and
**`vesper` 0/5**, the v1 game the section was written from. `41/41 judged gates pass` throughout.
Count 20 open → 18.

**2026-08-25 — P1 FIXED, and its own census corrected.** The first repair in this file. Repairing it
meant reading all 36 ambients instead of matching names in prose, and that overturned four of P1's
numbers and three of its verdicts — recorded as **N8**, the second correction to ship in this file
before being caught. Corrected shape: 36 random ambients, **21** with a speaking cast member, of
which **one** (`amb_kitchen_friday`) was already gated and twenty were not.

**Applied.** `requires_npc` on 15, each on the character who has to be in the room and each with a
window in that character's own schedule; a two-item `npc_at_location` condition on
`amb_office_phone`, which needs one NPC by absence and one in a *different* room and so cannot use
`requires_npc` at all. Three left alone because the prose already says the man is not in the room.
One, `amb_kitchen_house`, left open as a writing call rather than decided unilaterally.

**Proved live**, closing the gap the first draft admitted to (*"a captured instance is not in
hand"*): driving `setup.checkRandomEncounters()` 400 times per hour in headless Chromium, the three
gated bunk-room ambients return **0** at Monday 10:00 while the ungated control returns 122, and all
four return at 22:00. `amb_office_phone` fires at 10:00 and not at 19:00. 10/10 checks, zero page
errors.

**Skill fix shipped in the same commit** — `lint_ambient_presence` in `gates.py`, the check for the
one runtime path that consumes `requires_npc` and had nothing aimed at it. 20/21 before, 4/21 after.
`41/41 judged gates pass` throughout; the lint touches no tally. Count 21 open → 20 open, 1 fixed.

**2026-08-25 — B1 downgraded, B2 opened.** LO overturned this file's only blocker: *"it being in dev
mode is the blocker for release, media missing is the blocker for release, not for testing."* Checked
and he is right — `games-data.js` already carries a `dev` field that files the game under **Dev / test
builds**, `mrs_vance` has it set with no `version`, and the entry's own comment says the `--debug`
placeholders are deliberate while media is unharvested. §1 rewritten: B1 `BLOCKER` → `LOW`, status
`OPEN at release only`, and its Fix replaced with the four-step release procedure instead of a rebuild
that would have destroyed authoring information. The correction is recorded as **N7** — the only entry
in §0a that was written down before it was caught, and the only one that came from a wrong reading of
*intent* rather than of code. The surviving half became **B2**: no gate reads the built artefact
(`grep -cE 'output/|index\.html' gates.py` → 0) and `the-release.md` never mentions publishing one, so
nine portal entries restate the procedure by hand in three phrasings. §9 gained the matching cleared
row and §10 a B2 subsection. Count 20 → 21; blockers 1 → 0.
