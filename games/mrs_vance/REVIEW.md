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

**Current count: 7 open, 17 fixed** — 0 blockers, **0 high**, 2 med, 4 low, 1 open question, and
**P1, Q1, Q2, C1, C2, D1, M1, M2, R1, W1, S1a, S1b, S2, L1, L2, L3 and T1 FIXED**. M1 and M2 were closed, **reopened**
after LO rejected a game-layer fix the field disagreed with (§0a **N12**), and closed properly on
2026-08-26 by the engine work they always needed. **No HIGH items remain.** S1 was **split** on 2026-08-27 into S1a (the meter is
read in one room — prose, payable now) and S1b (the meter decides nothing, on a field figure that
does not hold up — a design question). **Both were paid the same day.** S1a in two instalments — the
fourth `work_counter` rung, then the bank and the bar. S1b by pointing the meter at the Lane 3
dispatcher: below `standing` 40 the four nameless walk-ins fire more often, and the meter stays
one global number on purpose. `standing` reads **4 → 22**, in **1 canvas → 6**. **Two** items are now decisions for LO rather than defect
calls: E1 (the obligation's size) and G1 (whether the Want file's one shape is the genre). S1b's
two questions are both answered in §5 — it delivers people, and it stays global — but its fourth
possible shape, **pricing the world by band**, is deliberately left for LO because it lands on E1. L4 is history and cannot be edited; the correction of record is in §7. Plus **twelve places
this review was itself wrong**, recorded first in §0a — six caught before writing, and six (N7–N12)
caught only after they had shipped in this file, one of them as its single blocker and one as a
whole fix that shipped green and was reverted. `v2_state.json` is no longer untouched: R1's pools
grew two locations past their declared `fill`, and both were corrected to what is built, still
inside their `fill_finished`. The remaining SKILL-layer items (C2, Q1, W1, G1, half of D1, and the
first-visit gate in §10) are recorded for LO to schedule.

---

# §0a · ⚠️ What this review got wrong

`forty_miles/REVIEW.md:31` puts its own corrections ahead of its defect list, because a review that
hides its misses is worth less than one that does not. Seven claims made during this review were
narrowed or overturned by checking them. **Six were caught before anything was written down**, which
is the only reason they are corrections and not defects in this file. **N7 through N10 were not** —
all four shipped in this file and were overturned afterwards: N7 by LO the day after, and N8, N9 and
N10 by the work of actually repairing the items they belonged to. They are the four most instructive
entries in the section for exactly that reason, and the last four say the same thing four times:
**a defect's diagnosis does not survive contact with its repair.** Four items in a row were diagnosed
wrong and repaired right — every repair attempted so far — which is an argument for repairing sooner,
not for reviewing harder. Twice the truth was only in the **built game** and could not have been read
out of the source at all (N7, N11).

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

### ⚠️ N10 · C2's "the gate has a one-word hole" is wrong — it was reading 62% of the buttons

**The fourth correction to ship in this file, and the third found by repairing the item.**

C2 as written: the clock gate is correct in intent and *"has a one-word hole"* — `to` missing from
`_CLK_PREP`. Adding `to` would have caught **1 of the 23** clock-naming labels in this repo.

`_clk_choices`, whose docstring is *"Every … label the player can read on a button"*, iterated
`exit_block.choices` only. A node's exit is **either** a `choices` array **or** a single `exit_block`
that IS the button. **1,225 of the repo's 3,214 labels are the second kind — 38% — and 22 of the 23
clock-naming labels were in that half**, using `at` and `before`, prepositions the gate has always
known.

So `act_sleep` was never read at all. The gate reporting `0 label(s) name a clock time` on this game
was not a near miss; it was a check that had not looked at the button.

**Why the first pass got it wrong.** It read `_CLK_PREP`, found `to` absent, tested the string
against the regex in isolation, and stopped. It never asked whether the label reached the regex.
**Testing a pattern is not testing an instrument** — the question is always what the instrument is
pointed at, and this is the second item in this file where that was the whole defect (P1/N8's G38 was
aimed at the runtime path that does not read the field).

### ⚠️ N12 · M1's fix followed the skill instead of the field, and the skill gates on a device one game in twenty-six uses

**The sixth correction to ship in this file, and the first that shipped a whole fix and took it back
out again.**

Nine first-visit arrival canvases were written for M1, passed `41/41`, were proved live and were
**reverted the next day** on LO's verdict: *"the place name is description and what was going in
that place should be able to tell the whole story."*

**He is right, and the evidence was already in hand when the fix was chosen.** First-visit devices
across the 26-game corpus: `degrees-of-lewdity` 258, `realm-of-corruption` 12, five games with 2,
and **eighteen games with none at all** — including `destroyer`, `become-someone`,
`course-of-temptation`, `the-company` and `friends-of-mine`. One game in twenty-six.

**Why it was picked anyway, which is the part worth keeping.** It was pure TOML, it needed no engine
work, and **`the-first-hour.md` F9 teaches it** — citing `degrees-of-lewdity`, the single outlier, as
its worked example. Cheap-and-doctrinal was chosen over what the measurements said. That ordering is
the defect, not the prose.

**And it is not only taught — it is GATED.** `the anchor introduces itself` fails a game whose
anchor location has no non-repeatable canvas bound to it. **A gate enforcing a device that eighteen
of twenty-six top games do not use.** That is a skill-layer finding and it is recorded in §10.

**Three things survive the revert:**

- **M2's grouping half stays refuted.** Zone headers above travel links: field median 0%. That
  measurement is independent of the arrival and remains true.
- **`somebody speaks` came out better than it went in** — 4.9:1 before the pass, **4.4:1 after** —
  because R1's pooled dialogue stayed when the arrivals went. The gate had been sitting 2% under a
  5:1 ceiling and nobody had noticed.
- **A first visit has a floor cost the board phase does not budget for.** Nine arrivals of three or
  four beats took five locations outside their declared `fill_finished`; the Bank's is 200 words and
  an arrival costs about 150. Moot for this game now, but true for the next one that tries it.

---

### ⚠️ N11 · D1 proposed stripping ten lines that C5 exists to require — and they were already dead

**The fifth correction to ship in this file, and the fourth found by repairing the item.** Four for
four now.

D1's fix note said *"drop `show_when_blocked` from the 10 cooldowns"*. `the-clock.md` **C5** is a
whole section arguing the opposite: an activity whose window has closed and simply vanishes *"reads
as a broken game, not a schedule"*, against a top-30 study where **lostness, not grind, is this
genre's disease** — 4.7% of player complaints against 0.9%. Five of the ten publish hours that
appear nowhere else outside the schedule page. **Answering LO's D1 that way would have worsened his
M1/M2**, from the same play-report.

**And the reason nobody noticed they were good is that they were never on screen.** C5's own TOML
example puts both keys in `[canvases.trigger.metadata]`; the importer reads them from the trigger
table itself (`template_import.py:1929-1930`) and *writes* them into metadata afterwards
(`:6980-6981`). The game copied the example, so all ten imported as `False` and reached the built
HTML **zero** times — valid TOML, green build, 41/41 gates.

**Two lessons, and the second is the general one.**

1. A review item that says *"strip this"* has to check what the thing is **for** before it checks how
   much of it there is. D1 counted 32 sites and bucketed them by mechanism; it never asked which
   doctrine section each bucket answered.
2. **A feature can be authored, documented, gated and completely dead.** Nothing in the source or
   the scoreboard could have told the difference — only rendering the room at the wrong hour and
   looking. That is the third time in this file the answer was in the built game and not in the
   TOML (B1/N7, P1's live capture, and now this).

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

# §2 · A button promised an hour, and the gate was reading 62% of the buttons

### C1 · `act_sleep` said "(to six)" and landed anywhere from 05:00 to 11:45
**severity** HIGH · **layer** GAME · **status** **FIXED** — now `Sleep. (8h)`, and the gate verifies it

`act_sleep`'s exit carried `text = "Sleep. (to six)"` and `time_progression_minutes = 480` — a flat
eight hours — on a canvas open 21:00–04:00, seven hours wide. Live, driving the clock and clicking:

```
sleep at 21:00 Monday    ->  wakes 05:00 Tuesday
sleep at 22:00 Tuesday   ->  wakes 06:00 Wednesday      <- the only correct case
sleep at 23:30 Wednesday ->  wakes 07:30 Thursday
sleep at 01:00 Thursday  ->  wakes 09:00 Thursday
sleep at 03:45 Thursday  ->  wakes 11:45 Thursday
```

True for **one entry minute of a 420-minute window**, and not only cosmetic: `work_counter` runs
07:00–13:00 and takes six hours, so sleeping at 03:45 makes the game's largest income surface
unreachable that day.

`the-clock.md` C3 (`:192`) forbids exactly this and prescribes the swap: *"state the DURATION
instead"*. Field basis: **84,009 action labels across 27 parseable sandboxes**, 24 of which name an
absolute clock time and **not one** promises a clock time as the outcome of a repeatable action.

#### Fix

```toml
text = "Sleep. (to six)"     ->     text = "Sleep. (8h)"
```

`(8h)` is true at every entry minute, matches the game's own tag format (`work_counter` is `(6h)`,
`act_wash_house` is `(25m)`), and — unlike a bare `Sleep.` — it states the fact the label was
reaching for: **sleeping costs eight hours, so sleeping at three in the morning costs the morning
shift.** It is also now *checked*: G36's duration half reads the exit's own
`config.time_progression_minutes` and confirms 480, taking the game from 25 to 26 verified tags, and
`lint · the time cost is not on the button` goes from `1 of 14 silent` to `all 14 long clicks state
their duration`.

**The window was deliberately not narrowed.** C3's other option is to shrink the schedule until the
claim is true; here that would leave a player who is up at 03:00 with no bed. Sleeping late costing
the morning is correct simulation. Only the label was lying.

### C2 · The gate did not have a one-word hole — it was reading 62% of the buttons
**severity** MED · **layer** SKILL · **status** **FIXED** — both halves, and four other games go red

**⚠️ This item's diagnosis was wrong.** §0a **N10** records it. It said G36 has *"a one-word hole"*,
the missing preposition `to`. Adding `to` alone would have caught **1 of the 23** clock-naming labels
in this repo.

`_clk_choices` — docstring *"Every … label the player can read on a button"* — read only
`exit_block.choices`. A node's exit is **either** a `choices` array **or** a single `exit_block` that
**is** the button (`{type: "location", text: "…", config: {…}}`). `act_sleep` is the second kind, so
G36 never saw the label at all:

```
choice labels the gate read           1,989
single-exit labels it did not         1,225      <- 38% of every button in this repo

clock-naming labels hiding in the unread half:
  steam         7    'Open at eight.' x4 · 'Get out at one.' · 'Sort her out at six.'
  seventh_day   6    'Down the ladder at four.' · 'Down the step before eight.' …
  the_allowance 6    'Out before six.' · 'Go up at eleven.' · 'Get up before three.'
  back_home     3    'Be gone before seven.' · 'Get up before four.' · 'In before six.'
  mrs_vance     1    'Sleep. (to six)'
```

Twenty-two of the twenty-three use `at` or `before`, prepositions the instrument has always known.
**They were invisible because nothing looked, not because the pattern was narrow** — and they are not
marginal: **21 of the 23 sit on canvases with no schedule window at all**, so the hour is true for at
most one minute in 1,440. Mrs. Vance's, on a 420-minute window, was one of the two least wrong.

#### Fix — both halves

**The reader.** `_clk_choices` now yields the `exit_block` itself when a node has no `choices`. It
already carries `config.time_progression_minutes`, the first key `_clk_spent_minutes` reads, so C4's
duration half started working on those labels with no further change. It yields a fourth field naming
the shape, and G36 reports how many findings came from the newly-read surface so a jumped count is
not misread as prose having changed. `lint_time_cost_on_button` shares the helper and got the same
widening.

**The preposition, in a narrow form.** Bare `to` is a false-positive machine. Against **81,264 action
labels** from the 27-game corpus:

```
`to` in the shared alternation .......... +8, ALL false   "Change to 0" · "Update to 0.3"
`to` + a spelled-out hour ............... +1 false        "restrict myself to one?"
`to` + a spelled-out hour, NOT `one` .... +0              <- shipped
```

Excluding `one` loses no reading (`at one` and `till one` stay covered by the existing branch) and it
is the same idiom trap `_CLK_BAD_NEXT` was built for — 312 corpus hits of *"at one point"*. On our own
prose the narrow form adds **21 hits across six games, every one a real "Twenty to eight"** the lint
had been missing.

#### What it costs the other games, stated plainly

```
                    now                was (the-clock.md, 2026-08-22)
steam               FAIL 16            FAIL  9
seventh_day         FAIL  8            FAIL  2
the_allowance       FAIL  6            PASS      <- a false pass
back_home           FAIL  3            PASS      <- a false pass
forty_miles         FAIL  1            FAIL  1
mrs_vance           PASS               PASS
```

Two games that were passing had never been measured on 38% of their own buttons. That is the check
starting to work, not a regression, and per the standing rule their 22 labels are **not** repaired
here. `the-clock.md`'s per-game table has been re-run.

⚠️ **No published constant was restated.** `the-clock.md` publishes *84,009 labels* and `gates.py` a
prose median of *0.8 / p75 1.8*; the re-implementation used for the delta above gives 81,264 and
0.45 / 0.91. The delta is trustworthy — same instrument both sides — the absolute level is a
different instrument's. See §9.

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
**severity** HIGH · **layer** GAME · **status** **FIXED** — 17 pools, prose and speech, proved live

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

#### What shipped

**17 `block_pool`s, three or four variants each, across all six loops** — twelve on act and finish
body paragraphs, five inside the `[group]` bands of Cade's and Sherrod's finishers (a pool nests
inside a group; never inside another pool; max depth reached is 3 against a cap of 4).

**And the speech was as frozen as the prose.** Every act node repeated one line forever — *"Slower.
You're not doing the books now."* on every render, for the life of the save. Eight existing dialog
blocks are now pools of three or four, and five nodes gained a spoken beat the prose had already
promised and never delivered: Sherrod's act narrated *"He talks while you suck him"* and carried
**no dialog block at all**.

The act nodes roughly doubled in crude density — whole-node explicit counts `act_hand` 5 → 12,
`act_mouth` 5 → 11, `act_desk` 6 → 12, `finish` 6 → 24; Sherrod 6 → 12 and 6 → 20; Isaac 5 → 11 and
4 → 11; Booth 3 → 9 and 5 → 13; Tobin 4 → 11 and 4 → 11; solo 4 → 10 and 4 → 10.

⚠️ **The one thing that can break a gate here is a thin variant**, because `gates.py:1666` reads a
pool as an AXIS and scores the thinnest band a node can render. One Tobin variant landed on two
explicit words and took `the act nodes` from 2-of-14 under 3 to 3-of-14; one word fixed it. The
lint is back at **2 of 14**, the same two pre-existing finisher bands as before this pass.

Proved live, 24 renders each: `loop_isaac.act` showed **3 of 3** body variants, `loop_cade.act_hand`
**4 of 4** of his lines.

---

# §5 · The colour meter is read in one room

### S1a · `standing` moves 25 times and is read 4 times, all in the same canvas
**severity** MED · **layer** GAME · **status** **FIXED** 2026-08-27 — 6 → 18 reads, 1 → 3 rooms, proved live

> **Split note.** S1 was filed as one item: *the meter is under-read*. Measuring the field
> (`Player_Legibility_Study_20260825` §44) showed it is two, with different fixes and
> different sizes. **S1a is the count** — the meter is read in one room, and the repair is
> prose in rooms that already exist. **S1b is the premise** — the meter changes nothing
> the player can do, and it was designed that way on a field figure that does not hold up.
> S1a can be paid any time. S1b is a design question for LO.

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

`board.colour_meter` reinforces it: *"Read constantly to swap ONE line."* Against the field
median — 31 passages carry a read, re-measured 2026-08-27 — four is not a colour meter yet, it is a
meter with one customer. (The 644-site figure this paragraph used to cite is withdrawn; see S1b.)

**Why no check caught it.** Gate *a meter is read* asks whether a raised meter is read by any
condition, cost or quest goal. It is: `7/7`. Nothing asks how often, and nothing compares the
reads against what the game said it would do with them.

**Field comparison, measured 2026-08-27** (13 of 26 corpus games carry a reputation meter;
`mrs_vance` measured through our own `applyAndNotifyTrait` / `trait_key` syntax, which the
field regex cannot see):

```
                   reads  writes   r:w   passages carrying a read   rungs
field median          62      28   2.3            31                  9
mrs_vance              4      25   0.2             1                  2
```

Every game in the set except `zaras-school-life` reads its meter **more often than it
writes it**. We are the only one writing five times per read.

**The first payment is shipped — the fourth band.** ✅ 2026-08-27. The sidebar declared
four bands and the prose ladder had three arms, so at `standing` 75 the sidebar read *"You
are the one they come to"* and `work_counter` played the scene it played at 40. The top
band was a promise on an always-on surface that nothing read.

`work_counter` now runs four rungs, and the top one **inverts the bottom one exactly** —
at `lt 15` he waits for a man rather than take her; at `gte 70` he waits for her rather
than take a man:

> The one with the tank trailer waits for you with Cade standing right there free, and when
> Cade offers he says he'll wait, and the two behind him hear him say it and stay where they
> are.

⚠️ The four arms are **one merged if/elseif chain** — adjacent `[group]` blocks merge — so
the new rung had to go **first** and the old `gte 40` arm needed a `lt 70` ceiling, or 70
would never have fired. Verified in the built HTML: six conditions, four arms, highest
first.

`standing` reads: **4 → 6**, still all inside `work_counter`.

**The second payment closes it — the bank and the bar.** ✅ 2026-08-27. The two rooms
`WANT.md` §3 names each got the same four-rung chain, on the repeatable ambient in each that
already **wrote** the meter and never read it:

```
                      standing writes   standing reads
the_bank  amb_bank_dee        -3              0  ->  4 rungs
the_bar   amb_bar_regulars     —              0  ->  4 rungs
          (plus buy_drink +6, hub_cade_bar -2, amb_bar_yard_drinks -4/+3, all read-free)
```

Both ladders change **tone, never fact**. Dee's account and the three years do not move at
any band; what moves is how she says them — at `lt 15` she writes Dorn's name on the slip
before you have said which account, and at `gte 70` she turns the screen a few degrees so
you can see the figure, which she is not supposed to do. In the bar the room settles the
question with one word and stops looking at `lt 15`, and at `gte 70` your name arrives down
there ahead of you.

`standing` reads: **6 → 18**, across **3 canvases in 3 rooms** — `work_counter`,
`amb_bank_dee`, `amb_bar_regulars`. Against the field's median of 31 passages carrying a
read we are still short, but the meter is no longer one room's private ladder, and all three
of `WANT.md` §3's named examples are now built.

⚠️ **The budget moved, and it had to.** Only one rung renders per visit, but `location fill`
counts authored words, so both rooms went over their declared budget the moment the ladders
landed — `the_bank` 300 → delivered 455, `the_bar` 400 → 548. This is the same growth R1's
`block_pool`s caused in two other locations. `board.locations[].fill` raised to **500** and
**600**, and `fill_finished` to **700** and **800**, in round numbers with headroom above
what is built — the gate rejects a budget written from the delivered count
(`gates.py:3744`, *"a budget that cannot be wrong is not a budget"*). `the_bank`'s
`fill_finished` was **200 against a `fill` of 300**, the only inverted pair on the board, and
that is corrected in the same edit.

**Verified.** `playtest_standing.py` now drives **three** ladders, twelve bands, and asserts
**exactly one** rung renders at each — probing inside each band rather than on its boundary,
and with all twelve phrases unique across the three so a rung leaking from the wrong room
cannot read as a pass. `5 → 25 → 55 → 80` in each of `work_counter`, `amb_bank_dee` and
`amb_bar_regulars`: **12/12 PASS**, sidebar word agrees at 80.
⚠️ The harness's first run against `work_counter` reported the lowest band empty; that was
the probe, not the game — `work_counter` carries a 30% Lane 3 substitution
(`walkin_office_driver`) that replaced the whole canvas on that roll. It retries past it, and
the retry is harmless in the two ambients, which have no substitution and land first time.
Gates **40/40, 0 FAIL**; `location fill` 12,317 → 12,627 words against 12,829 declared,
**14/14 locations on their own budget**, anchor `the_office` 31%. `playtest_presence.py` 10/10, `playtest_quests.py` 23/23.

---

### S1b · The meter is read to colour and never to decide, on a field figure that does not hold
**severity** OPEN — a design question for LO, not a defect call · **layer** GAME + SKILL · **status** **FIXED** 2026-08-27 — it delivers people now, and it stays global

`0_systems_spec.toml` declared `standing` a meter that *"refuses almost nothing"* and cited
*"the field reads reputation at 644 sites and refuses at 2% of them."*

**The 644 is three games.** `findings_H_known.md` §1: degrees-of-lewdity 610, zaras-school-life
23, course-of-temptation 11 — and that source flags the third as instrument-blind, not low.
**95% of the figure is one game.** The study was honest about its sample; `the-meters.md`
W5b generalised it to "the field" and `SKILL.md`'s fifth-commitment table hardened it into
a one-line law.

Re-measured across all 13 corpus games that carry a reputation meter:

```
1,944 references · ~10% of branch arms carry a link (not 2%)
MEDIAN 41% of reads change something mechanical
```

**"Rarely refuses" survives. "Therefore it only swaps a line" does not.** Three
consequential uses the three-game sample could not see:

| game | what the meter does | shape |
|---|---|---|
| `patriarch` | `Reputation gt 5` → Marlene knocks · `gt 9` → Luna · `gt 14` → Ana | **delivers people** |
| `destroyer` | `_roll1 to _roll + $Respect` in every pickup and fight | **modifies a roll** |
| `corpo-life` | 8-rung band read at 308 sites, `(Relationship +1 from prestige)` | **scales a rate** |

None of the three is a lock. All three are mechanical. The doctrine collapsed *"does not
refuse"* into *"does nothing"*, and `standing` was built to the collapsed version.

**What we are already ahead on, and should not lose in any fix:** every write fires
`setup.showEffectNotification()`, so the player is told the moment it moves — most of the
field shows only the state. And `standing` is negative-capable (`-3.0`, `walkin_shop_tobin`);
several field games are monotonic.

**The open question for LO — answered 2026-08-27, both halves.**

**1 · Does it decide anything? Now yes: it delivers people.** That is `patriarch`'s shape and
it was the cheapest of the four, because the machinery was already in the game and nobody had
pointed it at the meter:

```
13 substitution rules across 7 hosts · 12 walk-ins · exactly ONE carried conditions
```

The line drawn is **the nameless walk-ins**. `standing` is the audience meter, so it governs
the men with no name attached — the driver who asks for somebody who knows, the cup at the
wired glass, the length of the shop past whoever is working, the phone light that goes off in
the fourth cab. The five **named** walk-ins run on `trust` and `want` and are untouched: Cade,
Isaac, Tobin, Booth and Dorn are relationships, not an audience.

```
below standing 40 -- the title is not holding -- the strangers come more often
  work_counter    walkin_office_driver   0.30 -> 0.45
  act_wash_bay    walkin_bay_seen        0.20 -> 0.35
  work_parts_run  walkin_shop_watched    0.25 -> 0.40
  work_walkround  walkin_row_cab         0.25 -> 0.40
at or above 40, every rate is exactly what it was
```

**Direction matters and it is deliberate.** A rising audience meter that unlocked *more* sex
would be backwards here: `WANT.md` §4 makes the fantasy the title being stripped —
*"each flip is a man deciding out loud that the title does not apply to him."* High `standing`
is the title **holding**. So the meter buys respect at the counter and costs traffic in the
yard, and that is a trade the player can run in either direction. Nothing is locked at any
value; every walk-in is reachable at every band.

⚠️ **Appended, never prepended, and this is the whole engineering of it.** Rules in an
`exclusive_group` share one dice over cumulative buckets (`v2.py:5345`), and a slot the dice
claims whose conditions fail **falls through to solo rather than promoting the next rule**
(`v2.py:5378`). Appending takes a bucket that already fell to solo, so at `gte 40` the world is
bit-for-bit what it was. Prepending would have taken the bucket in *front* of an NPC walk-in
and quietly cut Cade's and Tobin's rates at every band.

⚠️ The condition set on each bonus rule is **copied from the rule above it** with the standing
item added. A bonus rule that dropped the presence gate would still claim its slot and still
fail — on the wrong reason, looking identical from outside.

**2 · Global or scoped? Global, and this is a deliberate refusal of the field pattern.**
Eight of thirteen scope it. `family-ties` scopes because `uni` fame and `onlyfans` fame are
different audiences who do not talk to each other. This game's premise is the opposite, and
`amb_bank_dee` says so on screen:

> "She knows about the paper. **Everybody at this crossroads knows about the paper.**"

One crossroads, one audience, one number. Scoping would have imported a field pattern whose
cause we do not have.

**Where `standing` stands now:**

```
             reads  writes   r:w   canvases carrying a read
before S1        4      25   0.2            1
after  S1b      22      25   0.9            6
field median    62      28   2.3           31
```

**Not done, and it is still LO's call: the meter does not price anything.** `patriarch`'s
fourth shape — weekly income by band — maps cleanly onto `work_counter`'s flat `+74`, and it
would pull on **E1** (the week's income is four times the week's demand) at the same time.
That is an economy change, E1 is filed as LO's decision, and it is not smuggled in here.

**Verified.** `playtest_walkins.py` (new) drives `setup.checkAndSubstituteCanvas` 6,000 times
per band per host — the function that owns the dice, so the distribution is measured rather
than one draw of it sampled. All four lifts land between +0.141 and +0.163 against a declared
+0.15, the plain canvas absorbs the mirror of each, and **every named walk-in is flat to within
0.009** across the two bands. Gates **40/40, 0 FAIL**; `playtest_standing.py` 12/12,
`playtest_presence.py` 10/10, `playtest_quests.py` 23/23.
⚠️ Two holes in the harness were found and closed before it was trusted, both of which would
have made its *second* half vacuous while it still printed PASS. It first ran at an hour where
no named walk-in could fire, so "flat" was comparing 0.000 to 0.000; and `requires_npc` is
checked as *is that NPC where the **player** is* (`v2.py:5340`), so with `player.current_location`
left at its initial `""` every named walk-in returned null regardless of the clock. The hours
and the player's room are now part of the declared setup, with the reason written beside them.

**Skill layer.** *Would a correct `author-game` skill have prevented this?* **Yes** — the
game inherited the number from W5b. `the-meters.md` W5b, `SKILL.md`'s commitment table and
`STATUS.md`'s index line are corrected in the same pass; see the skill `CHANGELOG.md` entry
for 2026-08-27.

### S2 · The gap is legitimate to defer and is not written down
**severity** MED · **layer** GAME · **status** **FIXED** — the promise is written; S1a/S1b stay open

Building thin and thickening is the method, and adding reads to rooms that already exist is
literally what `v2_state.json`'s own fill promise describes — *"every release until it closes adds
words to existing rooms, not rooms."* So S1 is not a defect of ambition.

It is a defect of record. `promises[]` holds six entries and this is not one of them.
`the-release.md:107,110`:

> Log every promise in the state file, and pay or cut it. […] **An honest wall is a promise; a
> silent one is a bug report.**

The same applies to a fourth thing not in `promises[]` — see L3.

### Fix

**The promise is written** — `promises[]` gained an entry naming the measurement (25 writes across
23 canvases, 4 reads all inside `work_counter`), the two rooms the Want names and the build does not
read in (`the_bank`, `the_bar`), and the field figure to aim at. Six promises became eight.
**Amended 2026-08-27:** the figure that entry named — 644 read sites — is withdrawn as a
three-game sample and replaced with the 13-game medians. See S1b.

**S1a stays open**, and deliberately: it wants two or three `standing` band reads written into
`the_bank` and `the_bar`, on the lines the Want already specifies — the clerk's tone, what the bar
already knows. That is prose, and it belongs with the M1/M2/W1 pass rather than with a ledger
correction. S2 was only ever *"the gap is not written down"*; it is now.

⚠️ **Re-measured while writing the promise, and the review's numbers hold.** A first pass of that
re-measurement reported standing being read at 27 sites across 23 canvases — including the bank and
the bar — and it was wrong: it matched on `trait == "standing"` with *any* `op`, so it counted every
`add` **effect** as a read. Conditions compare (`gte`/`lt`); effects assign (`add`/`set`). Separating
them gives 25 writes and 4 reads, exactly as first recorded. Noted because it is the same
prose-versus-structure slip as N8 and it nearly overturned a correct finding.

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

# §7 · The ledger recorded four things that are not true

Three were in `games/mrs_vance/v2_state.json` and one is in the shipping commit. Low severity and
high consequence: the ledger is the to-do list the next release reads, and the commit message is what
anyone reads first. **The three in the ledger are fixed; the fourth is history and stands corrected
here.**

### L1 · "Six external files referenced and not copied" — it is 22, plus 34 directories
**severity** LOW · **layer** GAME · **status** **FIXED**


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
**severity** LOW · **layer** GAME · **status** **FIXED**


`lints_shipped_with.cast_meters` says *"npc_dorn gates nothing — deliberate. He is the clock, not a
ladder."* The design intent is right and the statement is not: `npc_dorn.want` is read by two quest
cards, at `gte 12` and `gte 55`. It gates no *canvas*, which is what the lint measured and what the
note meant. Worth stating precisely, because Q2 lives in the gap.

### L3 · Four ladders are declared to a top the build does not reach, and no promise says so
**severity** LOW · **layer** GAME · **status** **FIXED**


`board.cast_meters.rungs` declares the full ladder; the build gates far below it:

```                declared top   highest gate built
npc_cade                    82                   42
npc_booth                   74                   50
npc_isaac                   66                   38
npc_sherrod                 62                   34
npc_tobin                   70                   70   <- built to its top
```

Deferring the upper half is correct for a v0.1 release stream. But `promises[]` had six entries and
none of them was *"the top half of four ladders"*, so the same silent-wall problem as S2 applied —
and it was compounded at the time, because Isaac's and Sherrod's terminal quest cards carried goals
at 66 and 62, values nothing in the build sits on.

**Q1's repair removed those goals**, which makes the promise more necessary rather than less: 66 and
62 — and Dorn's second rung at **55** — now live in `board.cast_meters.rungs` and **nowhere else in
the game**. A declared rung the build does not reach is fine; a declared rung nothing anywhere
mentions is a number that has quietly stopped meaning something.

### Fix

Applied to `v2_state.json`: L1's promise rewritten with the walked inventory, L2's lint note made
precise, and **two new `promises[]` entries** — the four ladder tops (this item) and the colour
meter's reads (S2). Six promises became eight. Two `decisions[]` entries were added at the same time:
one recording that 0.1 is being repaired in place rather than in a 0.1.1 (because `output/` is still
the test artefact and nothing is published — §1 B1/N7), and one recording the `loop_act` call (T1).

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

### T3 · A Lane 2 ambient takes the whole room screen, so the description never renders on that visit
**severity** LOW · **layer** ENGINE · **status** OPEN — **built, reverted and left open by LO 2026-08-26**

When a random ambient rolls on entry the room `<<goto>>`s to it. The player gets the ambient and
nothing else: **no room title, no description, no NPC portraits, no solo activities, no exits.** On
that visit the room's own prose — base or `description_variant` — does not render at all.

**The field does it narrower.** `destroyer`'s room screens put the encounter and the room's own prose
in the two branches of one `<<if>>` **in the description position**, and print the affordance bar and
the exits either way:

```
<<if _scene is 0>>      <img …>  an encounter
<<elseif _scene > 0>>   <img …>  "Your neighborhood. Quiet, sunny area…"
<</if>>
<div class="staff-bar"> … </div>      ← renders EITHER WAY
… exits …                              ← render EITHER WAY
```

**A fix was built and reverted.** `[settings] ambient_render = "inline"` gave the ambient the
description slot only and left the rest of the room standing. It worked — proved live, 40/40 gates,
six other games byte-identical — and LO called it back on 2026-08-26 after the four render buckets
were laid out for him. **Left open deliberately, not abandoned.**

Anything picking this up again starts from that commit (`3250226` reverts `01b8b38`'s ambient half)
and from three things learned building it:

- `getStoryCanvasRedirect` answers *"capstone? no? then ambient?"* in one call and the room `<<goto>>`s
  either. Splitting that question is the whole change.
- An ambient carrying **Lane 3** substitution rules injects a `<<goto>>` at its first node, which
  inside an `<<include>>` navigates away mid-render. Those have to keep the redirect.
- `<<include>>` appears **zero** times in the generator, so this introduces a rendering pattern the
  engine has never used.

---

### T2 · A room's picture cannot change with state — and it is not on the room screen at all
**severity** LOW · **layer** ENGINE · **status** OPEN — **deferred by LO 2026-08-26, noted for future**

`[[locations.description_variants]]` (shipped 2026-08-26, M1) swaps the room's **text** by state. LO
asked whether the **picture** could change with it. Two facts, both read out of the build rather than
assumed:

1. **A location's own `image` never renders on the room screen.** `locations/the_yard.jpg` is
   declared in `1_metadata_and_locations.toml` and appears in exactly **one** place in the built
   HTML — the Missing Media list. The room passage emits `<h2>`, the description, the portrait row
   and the nav grid, and no location image at any point (`v2.py:9640-9668`).
2. **Where it IS used is the travel CARD** — the tile you click in the parent room to come here
   (`_render_location_nav_card`: `background-image: url(<image>)`, with an inline SVG placeholder
   when the file is absent). One fixed image per location, chosen at build time.

So "make the picture change too" is **two** pieces of work, not one: put a location image on the room
screen at all, then let a `description_variant` carry an optional `image` beside its `text`.

⚠️ Not a media-harvest question. Under the standing rule a declared media block counts as present —
the file being unharvested is irrelevant here. **The room screen has no slot for it either way.**

---

### T1 · `loop_act` is one shared trait across six loops, and `loop_solo` never writes it
**severity** LOW · **layer** GAME · **status** **FIXED**

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

`loop_solo`'s entry choice now sets `loop_act = 1` alongside the `loop_stage = 0` it already set, and
its `finish` exit resets it to 0 — the pattern the other five follow. All six loops now write the
trait at both ends:

```
loop_cade     set 0,1,2,3      loop_booth   set 0,1
loop_sherrod  set 0,1,2        loop_tobin   set 0,1
loop_isaac    set 0,1          loop_solo    set 0,1     <- was: writes NONE
```

Kept shared rather than split per loop: every loop now brackets its own use, so a band can only read
what the live loop wrote, and one trait is the smaller surface. Recorded as a `decisions[]` entry so
the choice is not re-litigated.

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

### The prose texture is inside the field, measured against 25 shipped games

**2026-08-27.** Two players read a different game of ours and called its prose "an underpowered AI
whose 'mother language' isn't english." That prompted the first prose comparison this project has
ever run: our writing against the 25-game mopoga corpus, same instrument on both sides. The result
for this game is that **nothing needed changing.**

| | `mrs_vance` | field |
|---|---|---|
| dashes per 10k words | **25.4** | p50 0.99 · p90 17.5 · **p95 25.7** · max 35.4 |
| joints per sentence | 0.53 | 0.77 (better than field) |
| median sentence | 9 words | 12 |
| `you` as a share of words | 5.6% | 6.4% |

The dash rate sits on the field's **p95** and inside its range: `love-and-vice` runs 25.7 and
`apocalyptic-world` 35.4. The whole footprint is 32 dashes across 21 content blocks. By the
corpus's own evidence that is not a defect, and **no prose was edited.** The game the players were
reading runs 123.0 per 10k, which is 3.5× the corpus maximum, and is a different game and a
different session's call.

⚠️ **One finding from that session was published and then retracted, and it is recorded here so it
is not re-derived.** Measuring our games from `output/index.html` gave "sentences 4.75× more packed
than the field." That is an artifact of the built HTML: UI list blocks never reach a full stop, so
the splitter reads each as one enormous comma-filled sentence (10.6% of our HTML "sentences" are
those blocks, against the field's 1.5%). On authored beat text the direction **reverses** — see the
0.53 against 0.77 above. Do not re-run that measurement on built HTML and do not treat its number
as a finding.

The instrument this produced is **gate 43, "prose texture"** (`gates.py`, ceiling 35.0 = the corpus
maximum), so the tally for this game is now **41/41**. Its three companion numbers carry no field
figure by design; `references/register.md`, "Dashes stay rare" holds the doctrine.

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

### The ten `cooldown_message` lines are C5-mandated — do not "tidy" them

They publish the hours of an activity whose window has closed, which `the-clock.md` C5 requires and
which `off_season` is the only other game to do. Five of the ten carry hours that appear nowhere else
outside the schedule page. They live at the **top level of `[canvases.trigger]`** and must stay
there: `[canvases.trigger.metadata]` is a dead path the importer never reads (§0a N11), and that is
where they sat, unrendered, until 2026-08-25.

### The published field constants were NOT restated from this review's own extractor

`the-clock.md` publishes **84,009 action labels** across 27 sandboxes and `gates.py` a prose median of
**0.8 / p75 1.8**. The re-implementation written to measure the `to` branch gives **81,264** labels
and **0.45 / 0.91** — a simpler extractor (`[[…]]` and `<<link "…">>` only), so the gap is the
instrument, not the corpus.

**The delta is trustworthy and the level is not.** Every before/after figure quoted for C2 ran the
same extractor on both sides, which is what a delta needs; nothing licenses overwriting another
instrument's absolute number with this one. The published constants stand. Do not "correct" them from
these figures.

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
twenty-one answer yes** — P1, C2, Q1, D1, W1, G1 and B2. **Five of the seven are fixed** (P1, Q1,
C2, C1's half, D1); W1, G1 and B2 are recorded for LO to schedule.

### D1 · yes — twice, and the second one is the worst kind

**The instruction landed half a rule.** `engine.md` §15 was reversed on 2026-08-24 to *"set
`locked_text` by default"*, which is right. It says what a shown row must SAY and nothing about how
many to show, and the first game authored after it went to 22 of 22 against 13 of 171 across every
game before. The author followed the instruction exactly. §15 now carries the other half — the
field's 79%-silent default, the door-vs-refusal register split, and never-in-scene-on-a-self-moved
bar.

**And `the-clock.md` C5's worked example was the dead path.** It put `show_when_blocked` /
`cooldown_message` in `[canvases.trigger.metadata]`; the importer reads them from the trigger table
itself. The game copied the example and shipped **ten authored schedule lines that reached the built
HTML zero times** — the exact vanishing-activity failure C5 was written to prevent, caused by C5.

That second one is a class this file has not recorded before: **not a doctrine that taught the wrong
thing, and not an instrument that read the wrong surface, but a worked EXAMPLE that does not run.**
It is worse than either, because copying the example is what a correct author does. Standing
question to add to the one in C2's entry: *does the snippet in this section actually build?*

### C2 · yes — and it is the fifth instrument hole of the same family

`the-clock.md` C3 is correct, well-evidenced and gated. The gate was reading **62% of the buttons**:
`_clk_choices` iterated `exit_block.choices` and a node's exit is just as often a single `exit_block`
that IS the button. 1,225 labels unread, 22 clock-naming ones among them, four games affected.

Nothing about the doctrine needed rethinking. What needed it was the habit of checking a **pattern**
instead of an **instrument** — see §0a N10.

**This is the fifth of the same family recorded in this file**, and at five it stops being a run of
bad luck:

```
_band_texts          knew `group`, not `block_pool`
genre_words.txt      structurally blind to false friends
_clk_refs            missing a preposition
G38                  aimed at the runtime path that does NOT read requires_npc   (N8)
_clk_choices         read one of the two exit shapes                             (N10)
```

**In all five the doctrine was right and the check was narrower than the doctrine** — and in the last
two the check was pointed at the wrong surface entirely, which no amount of widening a pattern would
have fixed. The cheap standing question for any new check: *what fraction of its subject does it
actually read, and how would I know?*

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

### M1 · yes — and this one is a gate pointed at the wrong device

**Teeth test: would a correct `author-game-v2` have prevented it?** Yes, and more than prevented —
the skill actively *caused* the wrong fix.

`the-first-hour.md` **F9** teaches that a place introduces itself on first entry, and works its
example from `degrees-of-lewdity`'s `$forest_shop_intro` / `$gwylan_cafe_intro` family. Measured
across the whole 26-game corpus, that family is **one game**:

```
degrees-of-lewdity   258 first-visit branches, 117 flags
realm-of-corruption   12
five games             2 each
EIGHTEEN GAMES         zero
```

`destroyer`, `become-someone`, `course-of-temptation`, `the-company` and `friends-of-mine` — the
top of the field — have none. **F9 generalises from the single outlier.**

**And gate `the anchor introduces itself` enforces it**: a game whose anchor location carries no
non-repeatable canvas fails. A green board therefore requires a device eighteen of twenty-six top
games decline to use.

**What the field does instead is measurable and is not in the skill at all:**

```
                                   field median   mrs_vance
room prose per visit                 82 words       68
variant branches per room screen         10          2
rooms that rotate their text            22%         0%
rooms that vary by time of day          17%         0%
an event renders ON the room screen     yes    no — 100% of ours <<goto>> away
```

**Two engine gaps sit under it**: a location `description` is one static string (`v2.py:9629`), and
`getStoryCanvasRedirect` replaces the room screen rather than printing above it. So the skill cannot
currently teach the field's device even if it wanted to — there is nothing to author it with.

**FIXED 2026-08-26.** F9 rewritten so the rule is the description — the only surface the player sees
on every visit — with the first-visit canvas kept as a named minority device carrying its own
evidence. Gate `the anchor introduces itself` **deleted** and replaced by `lint · the place says what
it is`: every location by how much prose happens there against the length of its own description, a
list and never a score. Every game loses exactly one pass and one total (41/41 → 40/40, off_season
and the_season 39/41 → 38/40), so the gate was passing everywhere and no pass/fail state changed.

**The engine half is still open** and is why M1 stays open: a description cannot vary by state
(`v2.py:9629` — one static string; `_resolve_at_references` substitutes names only), and ambients
replace the room screen instead of printing above it.

---

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

### D1 · Eleven greyed rungs narrated the scene's own progress bar — and ten schedule lines were never on screen at all
**severity** MED · **layer** GAME + SKILL · **status** **FIXED** — 11 cut, 10 revived, proved live

> LO: *"I didn't liked showing the why text for locked choices."*

**⚠️ Two of the three things this item proposed to strip are correct work.** §0a **N11** records it.

Mrs. Vance is the **first game authored after `engine.md` §15 was reversed on 2026-08-24**, and it
followed the new instruction exactly: **22 of 22** shown-locked choices carried a reason, against
**13 of 171 (7%)** across every game before it. The instruction was right. Nothing said how many rows
to show at all, so it was applied to everything that can be locked.

#### What was actually there

`show_when_locked` is **22**, not 32; the other 10 are canvas-level `show_when_blocked` +
`cooldown_message`, a different surface. They split exactly by phase file:

| bucket | n | file | verdict |
|---|---|---|---|
| canvas `cooldown_message` | 10 | `3_activities` · `4_story_arc` | **were DEAD — revived** |
| the five doors | 5 | `5_scenes.toml` | kept |
| day-cap / need choices | 6 | `3_activities.toml` | kept |
| **in-loop ladder rungs** | **11** | **`4_story_arc.toml`** | **cut** |

#### The ten schedule lines were declared and never rendered

The worst thing in this item was invisible, and it is the reason it was invisible.

`the-clock.md` C5's own worked example put both keys in `[canvases.trigger.metadata]`. **That path is
dead.** The importer reads them from the **trigger table itself** (`template_import.py:1929-1930`)
and then writes them *into* metadata at `:6980-6981` for the generator to read back
(`v2.py:11484`). Authoring them in `metadata` skips the importer: valid TOML, green build, 41/41
gates, and `showWhenBlocked` reaching the built HTML **zero** times.

The game copied the example verbatim, so all ten were dead. Live, at 20:00 in the office:

```
before   Office · Do the books · Sherrod's Room · Leave Office
         (Work the counter simply GONE — the C5 failure, verbatim)
after    Office · Do the books · Work the counter — mornings, seven till one, and clean
         enough to stand at it · Sherrod's Room · Leave Office
```

C5 calls the vanishing activity *"a broken game, not a schedule"*, against a top-30 study where
**lostness, not grind, is this genre's disease — 4.7% of player complaints against 0.9%**. Five of
the ten publish hours that appear nowhere else outside the schedule page. **Stripping them, as this
item first proposed, would have answered D1 by worsening M1/M2** — the same play-report's *"couldn't
understand the world."*

Fixed by moving all ten to the top level of `[canvases.trigger]`, and trimmed to the house shape
while there: the engine renders `<row name> — <message>`, so *"Work the counter — The counter —
mornings, seven till one"* was doubling. `off_season`'s six are the exemplar — a bare lowercase
phrase, no restatement, no full stop.

#### The eleven that went

Every one is a rung inside a sex loop, gated on `arousal` or `loop_stage` — **meters that loop's own
nodes raise**. The row opens by itself in a click or two, so the text hands the player nothing to act
on, and it puts a UI label in the one place the register says the body is the only thing on screen.

Contrast `vesper`, which the field study calls *"the only game doing this properly"*: **8 in-scene
shown-locked choices and zero on a self-moved bar**. Its in-scene one reads *"Not like this — you're
filthy, and the cover won't hold"* — gated on something the player goes **elsewhere** and fixes.
That is a handle. Ours were a progress bar describing itself.

The field agrees on volume: **71% of 16,167 refusals render nothing**, per-game silent share median
**79%** across a 22–100% range. Cutting these takes the game from 0% silent to 50% — inside the
range, at the speaks-a-lot end, which is right for a game whose doors are its selling point.

#### What stayed, and why

**The five doors.** Gate 9 needs a visible locked door and `the-release.md` makes it the thing that
sells the next release. At ~20 words they match `vesper`'s median of 22 — and a **door is not a
refusal**: the field's 9-word UI label is right for *"already done"*, wrong for a release ceiling.

**The six day-caps.** *"The book is straight for today"* is the field's "already done" shape (18% of
spoken refusals) and it stops a wasted trip. Same lostness argument as the schedule lines.

#### Proved live

```
loop_cade.act_desk  arousal 0    zero span.locked-choice rendered
loop_cade.act_desk  arousal 95   "Let him cum inside you." live as a link
the_office          Monday 20:00 the greyed schedule row still there
```

4/4, zero page errors, and `playtest_presence.py` 10/10 + `playtest_quests.py` 23/23 unchanged.

#### The skill fix, same commit

`the-clock.md` C5's snippet corrected with the dead-path warning and the house register.
`engine.md` §15 gains the half it never had — the field's silence default, the door/refusal register
split, the never-in-scene-on-a-self-moved-bar rule, and a pointer that a blocked *window* is C5's
surface and not this one. New **`lint · which refusals are shown at all`** reports all three
measures; gate 42 is untouched and still passes.

```
                shown  in-scene  self-moved  median words
mrs_vance  was     22        11          11            15
mrs_vance  now     11         0           0            13
vesper             13         8           0            22
the_inheritance    27        15          10
off_season          4         4           4
```

⚠️ A first draft of that lint **crashed the whole scoreboard on `the_inheritance`** — an `effects`
list carrying string entries and an unguarded `.get()`. A lint must never be able to take the tally
down. Type-guarded, and clean across all fourteen games.

---

### M1 · Thirteen of fourteen locations never say what kind of place they are
**severity** HIGH · **layer** GAME + ENGINE · **status** **FIXED** — engine 2026-08-26, proved live

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

#### Fix — one was tried, and it was the wrong one

**A first-visit arrival canvas at each of the nine was written, shipped green and reverted the same
day.** LO's verdict: *"I think the place name is description and what was going in that place
should be able to tell the whole story."* He is right, and the field says so plainly.

**First-visit introduction devices across the 26-game corpus:**

```
degrees-of-lewdity          258 branches, 117 flags     the ONLY game doing it
realm-of-corruption          12
amore · patriarch · sluttown-usa · zaras · new-life-project     2 each
18 of 26 games                ZERO
destroyer · become-someone · course-of-temptation · the-company · friends-of-mine    ZERO
```

**One game in twenty-six.** The arrival is not this genre's device for telling a player what a
place is.

**What the field does instead is exactly what LO described** — the room screen itself carries it,
every visit, and it changes:

```
                                   field median    mrs_vance
room prose per visit                 82 words        68
variant branches per room screen         10           2
rooms that rotate their text            22%          0%
rooms that vary by time of day          17%          0%
an event renders ON the room screen     yes    no — ours <<goto>>s away, 100% of screens
```

**And the deeper reason the arrival could not have worked.** M1 is a *standing* confusion — *"couldn't
understand the world"* is not a first-visit complaint. A scene that plays once and never again
leaves the room screen exactly as dead as it was. The player who is lost on the twentieth visit is
still lost.

#### The fix, as shipped

**1 · `[[locations.description_variants]]`.** The description was one frozen string
(`v2.py:9629`, `:9676`). It is now the **else branch** of a first-match chain, each variant
`{conditions, text}`, evaluated by `setup.triggerConditionsSatisfied` — the helper the location
passage already called for `entry_conditions` a few lines above. No new runtime primitive.

The axis that matters turned out to be **`npc_at_location`**, which is LO's own phrasing — *what was
going in that place* — told by the room itself:

> *"Gravel from the back step of the house to the roller door of the shop, **and the roller door is
> up. Air tools go in bursts and stop. Somebody crosses the gravel with a part in his hands and does
> not look at the house.**"*

**Nine variants across seven rooms.** The Yard carries two, and the second states the shape of the
property — the sentence that lived in `board.map.shape` where no player could reach it. **That is
what closes M2.**

**2 · `[settings] ambient_render = "inline"` — BUILT, THEN REVERTED 2026-08-26 on LO's call.** It
gave a random ambient the description slot instead of the whole screen. It is gone; a Lane 2 ambient
`<<goto>>`s again and the room screen is not drawn on that visit. **M1 and M2 stand on the
description variants alone**, which is the half that was doing the work.

⚠️ **Three things the engine still cannot do, written down rather than implied.** There is **no
time-of-day condition** in the evaluator, so the field's 17%-vary-by-hour column is unauthorable;
presence is the axis to use instead. Per-visit **rotation** (the field's 22%) needs a counter like
`block_pool`'s and does not exist for descriptions. And **a random ambient still takes the whole
screen** — the setting that changed it was reverted, so the description does not render at all on a
visit where one rolls.

#### Verified

`40/40 judged gates pass` · `playtest_presence` 10/10 · `playtest_quests` 23/23 · two new engine
suites (12 + 11) inside a full app run of **244 passed** · **live 7/7**: the variant renders while
the shop is working, the base returns at 03:00, and with an ambient forced the description is
replaced while the exits and portraits and title all still render.

**Cross-game isolation** is the check that matters most here, because this touched the shared
engine: seven built games hashed before and after, and every authored passage in `vesper`,
`off_season`, `the_season`, `last_call`, `late_shifts` and `the_inheritance` is **byte-identical**.
The only delta anywhere is 25 lines of new runtime library.

---

### M2 · The map is a two-level tree and the player is never shown its shape
**severity** MED · **layer** GAME + ENGINE · **status** **FIXED** — by the Yard's variants; the other half refuted for good

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

#### Fix — half of it is refuted for good; the rest is M1's

This item offered two fixes. **The first has no support in the field and must not be attempted.**

Measured across every game in the 26-game corpus with eight or more travel screens
(`~/Documents/Player_Legibility_Study_20260825/`): a zone header standing above a run of travel
links runs at **field median 0%**, and a grouped travel list at **field median 8%**. Nothing groups
its travel list by zone. Grouping is not a convention this genre has.

**The second fix is the supported one and it is the same action as M1's**, and M1's engine work
closed it on 2026-08-26. The same study says why: the field teaches the shape of a world in **prose that places one
thing relative to another**, and on that axis this game already leads the corpus — **18.3 such
phrases per 10,000 words against a field best of 4.8 and a median of 1.8**. The geography was never
missing. It was rendering as wallpaper under a room title on every visit, which is what this item
said in its own first paragraph — and what the reverted arrival did not change, because it played
once.

The sentence that would carry it is already written, in `board.map.shape`, where no player will
ever read it:

> *"a diesel repair yard on a county road: gravel between a house and a four-bay shop, a row of
> overnight trucks at the far end, and a crossroads twenty minutes down the road"*

It belongs in the Yard's standing description, on every visit — not in a scene that plays once. It
is now in the Yard's second `description_variant`, the one that renders when somebody is out on the
overnight row:

> *"…the county road goes past the gate, and everything here — the house one side, the four bays the
> other, the row at the far end — opens onto this piece of ground."*

---

### W1 · Six men, and the prose says who they are 31 times in 10,298 words
**severity** HIGH · **layer** GAME + SKILL · **status** **FIXED** — prose + doctrine + a lint, 2026-08-26

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

#### Fix — SHIPPED

**LO demonstrated this item himself.** Having written every line of the game, he asked **"Who is
Sherrod?"** off a location button. If the author has to ask, a player reading that name on a travel
card has no chance.

**Measured per character**, with anchors taken from each man's own `relationship` string rather than
from a kin list:

```
                 before                          after
npc_cade      2 hits / 2,594 words   8 per 10k  ->  8 hits   30 per 10k
npc_booth     2 hits / 1,736 words  12 per 10k  ->  5 hits   29 per 10k
npc_tobin     3 hits                21 per 10k      unchanged
npc_sherrod   4 hits                25 per 10k      unchanged
npc_isaac     4 hits                29 per 10k      unchanged
npc_dorn      3 hits                35 per 10k  ->  4 hits   45 per 10k
```

**The spine of the game carried fourteen canvases and 2,594 words and said who he was twice.**

Five anchors added, all in **recurring** surfaces — `hub_cade_office`, `hub_cade_bar`,
`amb_kitchen_friday`, `hub_booth_kitchen`, `hub_booth_room` — and all inside `block_pool` variants,
so the reminder cycles instead of arriving every visit. Three words riding in prose already there:

> *"…which is as close as **your husband's eldest** comes to being off duty."*
>
> *"**Cade — your husband's eldest**, and the only one of them with a reason to be in this
> kitchen — comes up for ten minutes on a Friday…"*

⚠️ **Not a display-label field on the speaker.** That was proposed during this pass and is wrong. It
copies `destroyer`'s `<<speech "teagan" "Stepsister">>`, which **replaces** the name — and
`destroyer` is the only game of 26 that does it, surviving on having exactly one of each relation
where this game has three men in one. LO's ruling: *"Relation and name both are important and both
can't be replaced with another."* Live, 30 of 30 hub renders still show **Cade:** on the speaker
line with his portrait beside it. Both, at the point of use.

**And then a second, better fix on top — `npcs[].role`, 2026-08-26.** LO: *"I don't think this is
the proper solution for it. In the dialogue box, we do show the NPC portrait and name — below name
should also show another field."* The anchors recur every few visits; the dialogue box carries it
**every time somebody speaks**:

```
[face]  Cade
        husband's eldest
        "Slower. You're not doing the books now."
```

Six labels, each unique in the cast, none of them starting with "Your":

```
Dorn  husband   ·  Sherrod  brother-in-law   ·  Tobin  brother
Cade  husband's eldest  ·  Isaac  husband's middle son  ·  Booth  husband's youngest
```

⚠️ **Authored, never derived**, and this game is the argument: **five of its six `relationship`
strings contain "husband"** — him, his three sons and his brother. A first-clause derivation would
label five people `husband`, silently. `validate()` refuses two roles that match, which is the one
rule a machine can hold here.

**The prose anchors stay.** LO kept them — the two are complementary, one in the writing and one in
the interface.

**Skill layer — `the-first-hour.md` F10 and `lint · the role stays attached`.** F7 already gets the
role on screen at the meeting and F9 keeps a place saying what it is on every visit; nothing said the
same for people. The lint's instrument is the load-bearing part: **a kin-word detector was tried and
rejected** (F7 records it firing wrongly on ten of `last_call`'s meetings), so this one derives each
character's anchors from that character's own `relationship` line. `last_call`, `off_season` and
`the_inheritance` declare zero relationship strings and the lint is **silent** on all three — no
vocabulary, no false positives. It fires on `the_season` (Wade, 13 per 10k), **the other game that
drew "I don't know who is who" from LO**, and on `late_shifts` (Cole: 807 words, 0 anchors).

`40/40 judged gates` before and after · `somebody speaks` unmoved at 4.4:1 · app suite 255 passed ·
`playtest_presence` 10/10 · `playtest_quests` 23/23 · live 4/4.

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

⚠️ **Re-measured 2026-08-25 while repairing D1.** The first table counted two different surfaces
into one number and did not check whether either rendered.

```
                                          was   now
show_when_blocked  (room screen, greyed)   10    10   <- reached the build ZERO times
                                                        until moved out of trigger.metadata
show_when_locked   inside the sex loops    11     0   <- cut
show_when_locked   day-caps and needs       6     6
show_when_locked   the loop entries         5     5
                                          ---   ---
show_when_locked TOTAL                     22    11
```

Against the field (`findings_B_refusal.md`, 16,167 refusing chains):

```
silent share of refusals   field 71% overall · per-game median 79% · range 22-100%
                           mrs_vance was 0%, now 50% of its choice-level locks
spoken refusal length      field median  9 words  (n=4,540, names a price 37%)
                           vesper's doors median 22   <- "the only game doing this properly"
                           mrs_vance was 15, now 13

in-scene shown-locked / of those on a bar the scene itself moves
  mrs_vance  was 11 / 11      now 0 / 0
  vesper         8 /  0       <- in-scene, but every one a handle the player fixes elsewhere
  the_inheritance 15 / 10 · off_season 4 / 4 · the_allowance 3 / 3 · late_shifts 5 / 3
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

**2026-08-25 — the ledger pass: L1, L2, L3, S2 and T1 FIXED.** Nobody plays `v2_state.json`, but it
is the to-do list the next release reads, and it recorded three things that are not true.

**L1** said *"six external files referenced and not copied"* — that is the **packager's** warning and
it counts portraits only. The walked inventory is **22 fixed references, all missing** (14 location
plates, 6 portraits, 2 scene stills) plus **34 `pool_dir` directories, none on disk**. The 14 and the
2 were invisible to the promise meant to track them.

**L2** said `npc_dorn` *"gates nothing"*. He gates no **canvas** — which is what the lint measured and
what the note meant — and he does gate his own two quest cards at `want gte 12`.

**L3 and S2** were both silent walls, and `the-release.md:107` is *"log every promise and pay or cut
it"*. Two new promises: the **four ladder tops** the build does not reach (cade 82/42, booth 74/50,
isaac 66/38, sherrod 62/34; only tobin reaches its own at 70/70) and the **colour meter's reads**
(`standing` written 25 times, read 4, all inside `work_counter`, against a field figure of 644 read
sites for reputation). Q1's repair made the first one *more* necessary, not less: 66, 62 and Dorn's
55 now live in `board.cast_meters.rungs` and nowhere else in the game.

**T1** was the one game fix in the batch. `loop_solo` set `loop_stage` and never `loop_act` — safe
only while its finisher has no bands, and adding bands there is exactly what §4 asks for. All six
loops now set it at entry and clear it on finish. Kept shared rather than split, recorded as a
decision so it is not re-litigated.

Six promises → eight, fourteen decisions → sixteen, and one of the new decisions records that 0.1 is
being repaired **in place** rather than in a 0.1.1, because `output/` is still the test artefact and
nothing is published. `41/41` throughout. Count 15 open → 10.

⚠️ **A re-measurement written for S2's promise briefly overturned a correct finding** and was caught
before it reached the file: it reported `standing` read at 27 sites including the bank and the bar,
by matching `trait == "standing"` with any `op` — counting every `add` **effect** as a read.
Conditions compare, effects assign. The review's 25 writes / 4 reads is right. Same
prose-versus-structure slip as N8, one layer down.

**2026-08-25 — D1 FIXED, and two of the three things it wanted stripped were correct work.** The
eleven greyed rungs inside the sex loops are gone — every one gated on `arousal` or `loop_stage`,
meters the loop's own nodes raise, so the row opened by itself in a click or two and the text handed
the player nothing. `vesper`, the field study's exemplar, has 8 in-scene shown-locked choices and
**zero** on a self-moved bar; this game had 11 and all 11 were.

**The ten `cooldown_message` lines D1 also wanted cut turned out to be C5-mandated AND already
dead.** `the-clock.md` C5's own TOML example puts both keys in `[canvases.trigger.metadata]`; the
importer reads them from the trigger table itself and writes them into metadata afterwards. The game
copied the example, so all ten imported as `False` and reached the built HTML zero times — the
vanishing-activity failure C5 exists to prevent, shipped by the section that prevents it. Moved to
the top level, trimmed to `off_season`'s bare-phrase shape, and the office at 20:00 now carries
`Work the counter — mornings, seven till one…` where it carried nothing. Recorded as **N11**.

**Skill, same commit.** C5's snippet corrected with the dead-path warning; `engine.md` §15 gains the
half it never had (the field's 79%-silent default, the door-vs-refusal register split at 9 words
against vesper's 22, and never-in-scene-on-a-self-moved-bar); new `lint · which refusals are shown at
all`. Gate 42 untouched, `22 shown-locked · 22 with a reason` → `11 · 11`, still PASS.

**Verified.** 41/41 throughout; merged diff for the cut is 22 removed lines, 0 added, 0 unrelated;
live 4/4 (no greyed rung at arousal 0, a live link at 95, the schedule row present at 20:00);
presence 10/10 and quests 23/23. ⚠️ A first draft of the new lint crashed the whole scoreboard on
`the_inheritance` — unguarded `.get()` on a string in `effects`. Type-guarded. Count 16 open → 15.

**2026-08-25 — C1 and C2 FIXED, and C2's diagnosis was the wrong size.** C2 said the clock gate had
*"a one-word hole"*, the missing preposition `to`. It had a **1,225-label blind spot**: `_clk_choices`
read `exit_block.choices` and never the single `exit_block` that IS the button — 38% of every label
in this repo, with **22 of 23 clock-naming labels hiding in it**, using prepositions the gate already
knew. `to` alone would have caught one of them, ours. Recorded as **N10**.

**Applied.** `act_sleep` is now `Sleep. (8h)` — the duration swap C3 itself prescribes, true at every
entry minute of the 420-minute window, matching the game's own tag format, and it states the fact the
old label was reaching for: sleeping costs eight hours, so sleeping at three costs the morning shift.
The window was deliberately not narrowed; that would leave a player up at 03:00 with no bed.

**Skill, same commit.** `_clk_choices` yields the single exit too and names which shape a finding came
from; `_CLK_PREP` gains `to` in a narrow branch — `to` + a spelled-out hour that is not `one`, which
against 81,264 corpus labels adds **0** false positives where bare `to` adds 8. `the-clock.md`'s
scoreboard row and per-game table re-run.

**Verified.** The pre-fix TOML through the post-fix gate reports the sleep label; the repaired game
reports `0 label(s) name a clock time · 26 stated duration(s) all match the spend` (25 → 26, the new
tag is now *checked*), and `lint · the time cost is not on the button` goes `1 of 14 silent` → `all 14
state their duration`. Corpus regression 0 → 0. `41/41 judged gates pass`. Both live suites unchanged
at 10/10 and 23/23.

**What it costs elsewhere, and it is the point:** `the_allowance` and `back_home` were **passing this
gate on 38% of their own buttons** and now fail it, and `steam` 9 → 16, `seventh_day` 2 → 8. Not
repaired — standing rule. Count 18 open → 16.

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

**2026-08-25 — R1 fixed. M1 and M2 closed, then reopened the next day.**

**R1 · 17 pools, and the speech was as frozen as the prose.** Twelve on act and finish body
paragraphs, five inside the `[group]` bands of Cade's and Sherrod's finishers. Every act node had
been repeating one line for the life of the save — *"Slower. You're not doing the books now."* on
every render. Eight dialog blocks became pools of three or four, and five nodes gained a spoken beat
their own prose had already promised: Sherrod's act narrated *"He talks while you suck him"* and
carried **no dialog block at all**. Whole-node explicit counts roughly doubled across all six loops
(`act_hand` 5 → 12, `finish` 6 → 24, Booth 3 → 9, Sherrod 6 → 20). Live, 24 renders each:
`loop_isaac.act` showed 3 of 3 body variants, `loop_cade.act_hand` 4 of 4 of his lines.

⚠️ **A pool is an AXIS to `gates.py:1666`** — it scores the thinnest band a node can render, so one
thin variant took `the act nodes` from 2-of-14 under 3 to 3-of-14. One word fixed it. Back at 2 of
14, the same two pre-existing finisher bands as before.

**M1 and M2 · a fix shipped green and was reverted.** Nine first-visit arrival canvases took
`the anchor introduces itself` to 14/14 and cleared the first-visit lint entirely. LO rejected it:
*"the place name is description and what was going in that place should be able to tell the whole
story."* Checked against the corpus and he is right — first-visit devices are **one game in
twenty-six** (`degrees-of-lewdity` 258, eighteen games at zero), while the field's actual device is
a room screen that changes: 82 words against our 68, 10 variant branches against our 2, 22% rotating
and 17% time-varying against our 0%. And a scene that plays once cannot fix a standing confusion —
after the arrival, the room screen was exactly as dead as before.

Reverted in full: `2_one_shots.toml` and `v2_state.json` restored, then only the two locations **R1**
actually grew (`the_office` 3,000 → 3,845, `booths_room` 600 → 784, both inside their
`fill_finished`) recorded. M1 and M2 reopened, both now **GAME + ENGINE** — the location
`description` is one static string (`v2.py:9629`) and ambients replace the room rather than print on
it, so neither can be closed at the game layer. Recorded as §0a **N12**, and as a skill finding in
§10: **F9 teaches the outlier and `the anchor introduces itself` gates on it.**

**Three things survived the revert.** M2's grouping half stays refuted (zone headers: field median
0%). `somebody speaks` finished **better than it started**, 4.9:1 → 4.4:1, because R1's pooled
dialogue stayed — the gate had been sitting 2% under its ceiling unnoticed. And a first visit has a
floor cost no board budget carries: nine arrivals put five locations past their declared
`fill_finished`, the Bank's being 200 words against an arrival's ~150.

`41/41 judged gates pass` at every step. `playtest_presence.py` 10/10, `playtest_quests.py` 23/23.
Count 10 open → 9; R1 was one of the three HIGH items, so two remain.

**2026-08-26 — M1 and M2 closed by the engine work they always needed.**

Yesterday's game-layer attempt at M1 was reverted because the field disagreed with it. What was left
was two things no amount of writing could reach.

**`[[locations.description_variants]]`.** A location's description was emitted as one static string
at two byte-identical sites (`v2.py:9629`, `:9676`), and `_resolve_at_references` substitutes names
only — so a room read the same at 03:00 and 18:00, on day one and day ninety. It is now the else
branch of a first-match chain evaluated by `setup.triggerConditionsSatisfied`, the helper the
location passage already called a few lines above for `entry_conditions`. The two emit sites were
factored into one helper first, because byte-identical copies are how a change like this gets
half-applied.

The axis that matters is **`npc_at_location`** — the room describing itself differently when
somebody is in it, which is LO's *"what was going in that place"* told by the room rather than by a
scene. Nine variants across seven rooms; the Yard's second one states the shape of the property and
closes **M2**.

**`[settings] ambient_render = "inline"`.** A random ambient took the whole screen — no title, no
description, no portraits, no exits. It now takes the **description slot only**. A story one-shot
still redirects under both settings. `getStoryOneShotRedirect` is the new one-shot-only selector,
and `checkRandomEncounters` gained an `inlineOnly` flag that skips ambients carrying Lane-3
substitutions, because those inject a `<<goto>>` at node 1 that would navigate away mid-render.

⚠️ **Two engine limits are now written down instead of implied.** There is **no time-of-day
condition** in the evaluator, so the field's 17%-vary-by-hour column remains unauthorable — gate on
presence instead. And per-visit **rotation** (the field's 22%) needs a `block_pool`-style counter and
does not exist for descriptions.

⚠️ **The default build is the no-DB path.** `package_from_toml` without `--use-db` goes through
`apps/projects/services/game_graph.py`, not the DB writer in `template_import.py`. The first build of
this feature emitted the ambient wrapper and **zero variants** because only one of the two carried
the new property.

Skill updated the same day: F9's *"is not authorable"* paragraph replaced with the authoring shape,
the `version = "1.0"` fail-open warning, and the two limits above. `CHANGELOG.md` bullet alongside.

`40/40 judged gates pass` · `playtest_presence` 10/10 · `playtest_quests` 23/23 · 244 passed in the
app suite including two new engine suites · live 7/7 · and **every authored passage in the six games
that did not opt in is byte-identical**. Count 9 open → 7. **No HIGH items remain.**

**2026-08-26 (2) — W1 fixed. No HIGH items remain.**

LO demonstrated the item himself: he wrote the game and still asked *"Who is Sherrod?"* off a
location button. The `relationship` strings were always good and always on the cast page, one click
away and out of the scene.

**Game.** Five anchors into Cade's and Booth's **recurring** surfaces, inside `block_pool` variants
so the reminder cycles rather than nags. Cade 8 → 30 per 10k, Booth 12 → 29, into the band the rest
of the cast already occupied. Nobody fell.

**What it is not.** A display-label field replacing the name on the speaker line — proposed during
this pass, and wrong. `destroyer` is the only game of 26 that does it and gets away with it by having
one of each relation. Live: 30 of 30 hub renders still say **Cade:**, portrait beside it.

**Skill.** `the-first-hour.md` **F10** — F9's rule, for people. And `lint · the role stays attached`,
whose instrument matters more than its output: **a kin-word detector was already tried and rejected**
for firing on ten of `last_call`'s meetings, so this one takes each character's anchors from that
character's own `relationship` line. `last_call`, `off_season` and `the_inheritance` declare none and
the lint is silent on all three — by construction, not by luck. It fires on `the_season` (Wade, 13
per 10k), the other game that drew *"I don't know who is who"*, and on `late_shifts` (Cole: 8
canvases, 0 anchors).

`40/40 judged gates` · `somebody speaks` unmoved at 4.4:1 · 255 passed · playtests 10/10 and 23/23 ·
live 4/4. Count 7 open → 6. **Zero HIGH items.**

**2026-08-26 (3) — a dev jump into every sex loop, for testing R1.**

`6_dev_shortcuts.toml` (a phase `merge_toml_phases.py --no-dev` drops wholesale) gains one dev
screen with six choices — one per loop. Each arms that loop's state (arousal 55, `loop_stage` and
`loop_act` zeroed, the character's meters past every rung gate, the `met_` flag) and jumps straight
to the loop's entry node. Live 9/9: all six land in the right entry, and `loop_isaac.act` showed
**3 of 3** pool variants across 20 renders.

⚠️ **`_is_dev()` exists in `gates.py` and two gates do not consult it.** This cost two red gates and
is worth knowing before the next dev screen is written:

- **`the walk-in floor`** counts a location-bound repeatable dev canvas as a solo activity, then
  fails that room for having scheduled characters and no walk-in. Fixed by siting the screen at
  `the_bank` — the only location with **zero** scheduled characters besides `the_bathroom` and
  `kerr_crossing`.
- **`the climb is paid for`** reads six free meter-setting choices as a free route up `want`,
  `arousal` and `loop_stage`. Fixed with a 1-energy `costs` per choice and a
  `max_triggers_per_day`, exactly as `seventh_day`'s header prescribes — braking for a scoreboard,
  not design.

⚠️ **Dropping `location` to dodge both does not work.** A triggerless canvas nothing references by
node is never emitted (the generator only emits triggerless canvases the closure pass pulls in), so
the jump vanished from the build entirely. It needs a location; it just needs the right one.

`40/40 judged gates` · `playtest_presence` 10/10 · `playtest_quests` 23/23.

**2026-08-26 (4) — `ambient_render = "inline"` reverted. The description variants stay.**

> LO: *"Undo that change completely first."*

The half of the M1 engine work that changed **how a Lane 2 ambient renders** is gone. A random
ambient `<<goto>>`s again and owns the whole screen — no title, no description, no portraits, no
exits — exactly as it did before 2026-08-26 (2) and as it still does in every other game.

Removed: `setup.getStoryOneShotRedirect`, the `inlineOnly` parameter on `checkRandomEncounters` and
its substitution guard, `_location_autofire_line`, `_wrap_ambient_slot`, the `self.ambient_render`
read, the whole `ambient_render` path through `template_import.py`, the `[settings]` line in
`0_systems_spec.toml`, and `test_ambient_render_inline.py` (11 tests).

**`[[locations.description_variants]]` is untouched and M1/M2 stay FIXED.** It shipped in the same
commit but is a separate feature, and it is the half that closed both items. The two met in exactly
one place — `_render_location_description` called `_wrap_ambient_slot` — and that call was the seam.
`mrs_vance` still carries nine variants across seven rooms.

**What this puts back on the table.** On a visit where an ambient rolls, the room's description —
variant or base — does not render at all. That is now recorded in `the-first-hour.md` F9 as an
engine limit rather than as a setting, so no future ledger promises against it.

Verified: **244 passed, 7 skipped** · zero code references remain · seven games rebuilt with **six
byte-identical** and `mrs_vance` changed exactly as intended · `40/40 judged gates` ·
`somebody speaks` 4.4:1 · playtests 10/10 and 23/23 · **live 5/5** — a forced ambient lands on
`Canvas_amb_yard_crossing_Node_base` with 0 nav cards and no room description, while the shop-floor
variant still renders with 5 nav cards beneath it.

**2026-08-26 (5) — `npcs[].role`: the answer moves onto the dialogue box.**

> LO: *"I don't think this is the proper solution for it. In the dialogue box, we do show the NPC
> portrait and name — below name should also show another field."*

W1's prose anchors recur roughly one visit in five. A short authored label now sits **under the
name in the NPC dialogue box, every time somebody speaks** — portrait, name, role, line. Nothing is
replaced; `Cade:` is still on the line with his face.

```
Dorn  husband   ·  Sherrod  brother-in-law   ·  Tobin  brother
Cade  husband's eldest  ·  Isaac  husband's middle son  ·  Booth  husband's youngest
```

⚠️ **It is authored and never derived, and this game is why.** Deriving from `relationship`'s first
clause labels **five of these six "husband"** — him, his three sons, his brother. `the_season` has
two characters whose strings both begin *"Your brother"*, and that is the game that drew *"I don't
know who is who."* A silent wrong default is worse than a missing one. `validate()` refuses two
labels that match and refuses a label past five words.

⚠️ **The first build shipped `"role": ""` into `$npcs` for every NPC in every game** — a dead key in
every save, since the label is baked into passage HTML at build time and nothing reads it back. It
is now stripped alongside `customizable` and `relationship_options`. **Caught by hashing all seven
builds, not by a test** — the six games that declare no role now differ by twelve lines, the CSS
rule alone.

`40/40 judged gates` · `speakers are named` 253/253 · new suite `test_npc_role_label.py` (11) inside
a full app run of **255 passed** · playtests 10/10 and 23/23 · live: `Cade:` at y=382,
`husband's eldest` at y=406, same left edge, portrait to the left; `Stranger:` renders with no role.
