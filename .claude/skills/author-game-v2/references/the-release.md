# The Release — the unit of work

The game is never the unit. The **release** is, and it repeats, release after release.

---

## Where a release happens

Measured on one six-week cycle of a mature game (DoL): +196 scene units, **zero new locations**, and
every content commit an event at an existing place. That is a **maintenance-cycle observation**, and it
stays the default for WHERE a release happens: zero new places. What a release adds is rungs and
people (`SKILL.md` commitment 4). It does not say what a release is ABOUT. The next section does.

---

## The next step — before, her moment, leads to

A pitch is **the next step on a named relationship**, never a moment on its own. The loved arcs in
the field run 9–14 steps over weeks, and every step pays one before it and opens one after
(Great Games Study, round 6; `the-arc.md` A13–A14). A pitch has three parts.

**Before — what it pays.** A scene, a flag or a line already shipped on this relationship, named
from the pack's RELATIONSHIPS. If nothing comes before it, the pitch says it is **step 1** and
shows his want first.

**Her moment — eight lines, one sentence each.** Taken from what the top female-lead games do and
what their players quote:

1. **The fantasy.** The game's own shape, from the Want §0. Keep it; a pitch serves the fantasy the
   game already promised, and a thread step serves it through the thread's link into the hook.
2. **The temptation, and his want before it.** What is offered, by whom, and why she wants or needs
   it. Who moves first and why: a pressure type moves first and names the act; a nice type waits,
   so she moves; or he wants her from scene one. And **the leak** — one small, repeatable line or
   look on his hub that shows his want, tied to his number.
3. **Her answers, and his "no" branch.** Three to five, graded. The **no** is written too: it is
   **parked** (the step comes back after a wait) or **final** (the button says "(ends his path)")
   (`the-arc.md` A3). Pressure: he asks again, and the button says Submit, not Agree — and every
   pressure arc offers an opt-out somewhere. Nice: the no costs nothing, and he may be the one who
   says no.
4. **Her voice at her level.** A low line and a high line for the same moment, so the player hears
   how far she has come.
5. **Who notices.** Somebody sees or hears of it, and does something differently afterwards.
6. **What sticks, and he remembers.** A flag, a meter, a line that changes — never silent. A later
   line of his names what she did. **His move never fires on a dice roll alone**: the scene that
   triggers it says why now.
7. **The moment to remember.** Which of the five kinds — her firsts · being seen · her body as the
   price for something she needs · taboo at home · a consequence she lives with — and the line a
   player would quote.
8. **The door it opens, and the clip we can get.** A door for a later release hangs on a meter rung
   this release cannot reach, never on a flag nothing sets: the build refuses a gate on a flag no
   canvas sets (`validate_flag_chains()`, `v2.py:14094`). The live goal, mystery or rival beat it moves,
   and a clip that exists or can be found for it — at the idea stage, `intent` (what to look for) is
   enough, and it is found later. A moment with no clip is a moment the game cannot show.

**Leads to — what it opens.** The next step, named; the promise line this step ends on; and **how
the player finds the next step** — the guidance card line. Being lost is the field's top complaint
about its best relationships: 87 of 182 player comments on four loved arcs are "how do I / I'm
stuck".

Then, and only then, Where / Who / Keys to / Opens / Cost / Not.

The field's moments, ten per kind, are in `references/moment-library.md`. Take the **kind** from it,
never an entry.

---

## The loop

**1. Read the Want.** Not optional, not skimmable. Name the line this release serves. If you
cannot, the release is unfocused — pick again.

**2. Pitch — three, independent.** Three Pitcher agents, no shared context. Two are each given one
of the two most-owed relationships, from the pack's RELATIONSHIPS; the third is given a declared
thread of her life (THREADS, `the-want.md` §6), pitches a step in it, and may add one new person who
belongs to that thread (name, age, thread). The assignment is the relationship or the thread; the
moment kind is a hint, and each pitch names its kind. LO picks one. Independence is the point: shared context produces three shades of one idea.
See `references/agents.md`.

**3. Attack, before writing.** The panel runs on the *design*, not the build. Every cheap
catch in our history happened here; every expensive one happened after shipping. Same agents,
different timing, an order of magnitude in value.

**3b. The excitement read.** Before LO reads the three pitches, one `v2-attack` instance with the
`excitement` lens reads each. It scores nothing: it returns the pitch with a one-line note beside
each line. Its only rejections are the two instant fails — a big turn forced on her with no warning
or way round, and sex used only as a punishment — each quoting the line. LO judges.

**4. Write.** Events on existing surfaces. Default to **zero new locations** (*Where a release
happens*, above); a thread's new person arrives at a place she already has. If this release opens a
location, it arrives filled, not as a promise.

> ⚠️ **If this release moves a field that prose already quotes — a price, an amount, a
> window, a parent location, a label — it is an amendment, not an addition.** See *The prose
> quotes the fields* below, and grep the prose for the OLD value **spelled out**, not only as
> a digit.

**5. Gate — and read the lists.** `python3 scripts/gates.py <slug>` green, or fix it. That same
command prints **its lints below the tally** — `gates.py --selfcheck` gives the count, from the
script's own registry of printed `lint ·` labels (`_emitted_names`) — and they are the half of the
instrument that judges nothing. Lints never touch the tally (`gates.py:13374`), so a game
can be green on every gate with the lints full, and a flagged word nobody reads ships on a button.

> ⚠️ **This is a step in the loop, not a checklist, and the difference is deliberate.**
> `DOCTRINE_GAPS.md` §3a: *"It is a checklist, and checklists do not hold… v2 must not inherit the
> checkbox."* v1's thirteen-point pre-ship audit was followed by the exact bug it was written to
> prevent. So there is no box to tick here. There is one command you already run, output you are
> already looking at, and a rule about what leaving it means: **anything left in a list is left on
> purpose, named in the ledger, with the reason.** A lint you cannot explain leaving is a lint you
> have not read.

**5b. Check what you MOVED, not just what you added.** Every release after v0.1 lands on people
holding saves, and the whole scoreboard above is blind to them: renaming a canvas id passes every
gate and strands every save in the wild. `references/the-returning-player.md` owns that half — ids,
flag and trait keys, stat ranges, the title, and the one-shot grant a carried save has already
burned. The engine repairs *additions* on its own (`engine.md` §40) and nothing else.

```bash
python3 scripts/gates.py --saves <slug>
```

One command, like step 5 and like `--release`, and for the same reason: four greps in a row would be
a checklist, and §3a already ruled on those. It needs the archive step 3 keeps — no archive, no diff,
and it exits 2 rather than pretending.

**6. Build, and cross the boundary.** Everything above judges the SOURCE. A release is the one
moment the **artefact** is what is judged. The six steps — media harvested, rebuilt without `--dev` or `--debug`, archived,
`version` set in both places, `dev: true` dropped in the same commit, ledger promises reconciled —
are in **§ Shipping the build** below, and they end on one command:

```bash
python3 scripts/gates.py --release <slug>
```

> ⚠️ **The rule is LO's and it is not the obvious one: dev mode and missing media block RELEASE, not
> testing** — a test build with labelled placeholders and a jump list is a *good* test build.

**6b. Read** *(LO decided, D12)*. Run `v2-reader` on every canvas **touched** this release: its id is
new, or its TOML table differs from the one in the last shipped release's `7_final_game.toml`, read at
`releases[].commit`. With no shipped release, every canvas is touched. Save its verdicts in
`release_page.reader` and LO's waivers in `release_page.reader_waivers`; a FAIL with no waiver blocks the
release (`--ship` row *the reader passed*). The reader can be wrong either way, and LO's playthrough is the final say.

**7. Log.** Record in `v2_state.json`: the subject, what it added, **what it
opened**, the gate scores, and **the lint figures you are shipping with** — at minimum the
own-words count and anything you consciously left. A number in the ledger is one that has to come
down next time; a number only in a terminal is one nobody is holding. This is the same mechanism
the anchor share already runs on, and the reason the anchor gets budgeted and the word list does
not is only that one of them was written down.

**8. Listen.** About two weeks after a build is public, and before the next release's step 1, the
`v2-listener` agent reads the new comments since the release date: mopoga (`scripts/listen_mopoga.py
<slug> --since <date>`), F95 (thread and reviews, read-only in LO's Chrome), gamcore (by hand, or
recorded as "not read"). It writes `listen[]` in `v2_state.json` — what players praised, asked for,
complained about and got stuck on, each with a quote and a count. Then re-read the Want against it:
anything that would change the promise goes to LO as a question, never silently. **Players choose
the order and supply small ideas; they do not set the premise** (Great Games Study, round 4b).

---

### The loop's instruments, in the order they run

| step | command | what it can see |
|---|---|---|
| 5 | `gates.py <slug>` | the source — the gates, then the lints (`--selfcheck` prints both counts) |
| 5b | `gates.py --saves <slug>` | the difference between **two** releases — what a rename stranded |
| 6 | `gates.py --release <slug>` | the **built artefact** — dev mode, missing media, three version numbers |
| 8 | `listen_mopoga.py <slug> --since <date>` | what players said on mopoga since the release — sorted by likes, never scored |
| — | `gates.py --selfcheck` | this skill against its own scoreboard; needs no game |

⚠️ **Nothing checks that you ran them, and nothing can.** `DOCTRINE_GAPS.md` §3a rules out the
checkbox, and a check that an author read a list is the checkbox. What holds instead is step 7:
**anything left in a list is left on purpose, named in the ledger, with the reason.** A lint you
cannot explain leaving is a lint you have not read. That is a discipline, not a guarantee, and it
should not be written up as one.

---

## The three kinds of content, and their rules

**STANDING** — she can go there and act, repeatedly.
Carries the explicit floor. This is where the crude register lives — not in the one-time
scenes.

**TRIGGERED** — fires when her state matches.
*"during the weekends"*, *"when exposed"*, *"at high stress"*. For the `female` protagonist
declared in `want.player` — the default, and the case this was measured on — this is the main
heat engine. The loudest complaint in a comparable game's comments was *"I can go
out anywhere and NOTHING happens to me."* The consequence layer is not garnish.

**MILESTONE** — fires once, then opens standing content.
**Every milestone names what it turns on.** Gate 7. It may open through a chain — an opening
funnel legitimately runs one-shot to one-shot — but the chain must land on something standing.
A milestone whose only flag is its own once-guard is not a milestone and owes nothing.

---

## Every release ends on an opening

Not a cliffhanger. **A door.**

A question ("who killed him?") can be answered by reading a thread. A want ("I want into that
room / I want her to say yes") can only be satisfied by playing. Wants sell the next release.

Mechanically: at least one choice rendered `show_when_locked = true`, attached to a person or
place the player already cares about. Gate 9.

Two measured failure modes to avoid:

- **Version-keyed stubs.** One game named its quests `intro / release2 / release3`; players
  reported finishing it in a minute. It is abandoned.
- **Named but never paid.** Another dangled a character for years, and players
  still ask when they will meet him (`sluttown-usa`, paraphrased). Log every promise in the state file, and pay or cut it.

And state the current ceiling honestly. The reference game prints a plain marker at the top of
each track so the player knows where the wall is. An honest wall is a promise; a silent one is
a bug report.

---

## Maintenance is the job, not a failure

**55.6% of the measured release was fixes.** Across eight years, the reference game's releases
run roughly 87% non-new content.

So a release that is half repair is *normal*. Budget it. Do not treat a high rework rate as a
defect to apologise for — under-shooting it is the more likely error.

**A quality problem goes to its layer.** Place it first — the skill, the game's process, CLAUDE.md,
or a one-off in this game (CLAUDE.md, "When a built game misbehaves") — and fix it at that layer. A fix
that needs a rebuild waits for the next release boundary and is listed on that release page
(`release_page.rebuild`): one planned rebuild, not one per fix.

---

## The prose quotes the fields, and a field that moves makes the prose lie

**Read this before changing a `costs`, a rent `amount`, a `due_day`, an `entry_from`, a schedule,
or a display label on content that already ships prose.**

**The model.** An authored line that states a fact a field encodes is a **copy of that field** — a
literal duplicate with no link back. `amount = 100` and the collector saying *"Rent. A
hundred."* are two independent strings that happen to agree today. Everything here **passes
the build**: the flag chain validates, no warning fires, nothing crashes. The damage is that the
game tells the player something untrue, and the player cannot grep, cannot diff, and has no way
to know.

**The engine will not save you, and the rent block is the sharpest case.** An authored `greeting`
*replaces* the default that would have interpolated the live number:

```
v2.py:19176   <<print _rt.greeting || "Rent. " + _cur + _rent + ". You know how this works.">>
v2.py:19180   <p>You have <<print _cur>><<print _money>>. Rent is <<print _cur>><<print _rent>>.</p>
```

Four lines apart. Re-price to 150 and the collector says *"A hundred"* directly
above *"Rent is $150."* **The NPC contradicts the UI in a single screenshot.**

The most fragile copies sit *inside the rent block, beside `amount`*.

**Keep writing the copy.** It is load-bearing: the player budgets against a stated number, and a
price only the UI knows is a plan they cannot make. What writing it creates is an obligation —
**the field and its prose are one edit, not two.**

### The four edits that carry this debt

**MOVE** an `entry_from` · **RE-PRICE** a `costs` or an `amount` · **RE-SCHEDULE** a window or a
`due_day` · **RENAME** a display label. All four change something that already has prose pointing
at it. Treat each as an amendment, not an addition.

### Before you commit one, grep the prose for the OLD value

```bash
git diff -U0 -- games/<slug>/toml_phases/ | grep -E '^-.*(amount|costs|entry_from|due_day|start_time)'
# then search the prose for the value that just left
```

⚠️ **Grep the WORDS, not just the digits — this is the step that gets skipped.** Prose spells
amounts out, in voice, as it should: a rent of `100` is written *"A hundred"*, and Course of
Temptation's [CampusClinicPregnancyCheckup] says *"the appointment will cost two hundred dollars"*
beside `<<spend 200>>`. A search for `100` finds neither. The digit search is the one that feels
thorough and is not.

### What already catches part of this, and what does not

| coupling | caught by |
|---|---|
| a price on a button vs the cost it charges | gate **a price is on its label** — it compares the amount |
| a place the prose walks through that the map lacks | lint **the prose names places the map does not have** |
| an hour a beat names against the window it fires in | lint **the clock in the prose** |
| a currency that is not the game's own | lint **the currency in the prose** |
| a house word that changed | lint **the words the player has to already own** |
| a `file:line` in this skill that moved | `scripts/cite_check.py` |
| **an amount spelled out in a beat or an NPC's line** | **nothing — this section is the whole guard** |

---

## Cadence

Measured across the funded cohort: **~31 days** between versions, sustained four to eight
years. Slippage is the strongest single predictor of decline; pages holding cadence carried a
median 684 paying members against 176 for those slipping.

Posting volume predicts revenue (ρ = +0.58). Release *speed* does not (ρ = −0.09).

**Visible motion matters more than shipped volume.** Ship smaller, on time.

**One thing per release** — one character, one place or one theme — on a fixed rhythm. The field's
developers plan it that way: In Her Own Hands' *"it was all about Abby!"* (Great Games Study, round 4b).
The ledger's `releases[].subject` is that one thing.

---

⚠️ **EVERY NUMBER ABOVE DESCRIBES A GAME THAT ALREADY EXISTS.** `[added 2026-08-31]` The ~31-day
figure, the +196-units-and-zero-new-locations shape, the whole ship-smaller-on-time argument — all of
it was measured off **mature** products, including a reference game of 2.24M words. It is a
maintenance rhythm, not a **construction** method.

A cadence rule cannot be followed by a game that has not been born yet, and "ship
smaller" applied to release one produces a thing too small to be a sandbox at all.

**Read this section only from v0.2 onward.** v0.1 is governed by the seed size below.

---

## § Minimum viable mass — the floor under v0.1

`[added 2026-08-31]` **This architecture has a size below which nothing works**, and three
independent lines say so:

| | |
|---|---|
| the reference game's own seed | **116,540 words across 25 locations** — mean 4,661 per location |
| Ashwell, on Floating Modules | *"requires substantial content; **collapses into linearity otherwise**"* |
| Failbetter's StoryNexus retrospective | *"time-to-bootstrap… making a minimally playable experience took ages because one had to create quite a number of storylets"* |

**Gate 1's backstop constants are the floor**: `MEDIAN_LOCATION_WORDS = 3000`,
`MEAN_LOCATION_WORDS = 4500`. A v0.1 that declares its own budgets is judged against those instead —
which is correct, and is not permission to declare small ones.

**A game is not started until the seed is sized.** Declare it in `v2_state.json` at
`board.locations[].fill`, in the board phase, before a word of prose. `the-sheets.md` S3.

---

## § Shipping the build — the boundary nothing was holding

**Before accepting any change to money, the ending or the release page, run
`scripts/shape.py <slug>`** (checkpoint A, `the-spine.md`), and have LO re-sign SP7: a spine that no
longer holds together is cheaper to fix in the ledger than in the build.

Everything above is about what a release **adds**. This is about the **artefact** — and its
companion is `references/the-returning-player.md`, which is about what a release must not **move**.
Until 2026-08-28 no instrument in this project could see a build: the whole scoreboard is aimed at
`7_final_game.toml`, which is structurally incapable of judging a build.

The rule is LO's and it is not the obvious one:

> **Dev mode and missing media block RELEASE, not testing.**

A test build with labelled placeholders and a jump list is a *good* test build. Nothing about
authoring changes. The boundary is the moment it reaches a player.

Six things separate a test build from a published one. Lifted from `games-data.js:44-49`, where
this procedure was discovered once, written correctly, and left in the one file no tool reads —
restated by hand in nine of twenty-eight portal entries in three different wordings, which is the
signature of doctrine living in the wrong place:

1. **Media harvested.** Every pool, plate and portrait.
2. **Rebuilt with neither `--dev` nor `--debug`:**
   ```bash
   python3 manage.py package_from_toml \
       --file games/<slug>/toml_phases/7_final_game.toml \
       --output games/<slug>/output --gen-version v2
   ```
3. **Archived** to `games/<slug>/releases/v<version>.html` — the build itself, kept.
4. **`version` set** on the portal entry **and matching `[project] version`** in the TOML —
   the field, the sidebar footer it renders and its four `file:line`s are `engine.md` §38.
5. **`dev: true` dropped, in the same commit** — that line is what moves the game into the main grid.
6. **`v2_state.json` promises reconciled** — paid or cut, per *Named but never paid* above.
6b. **The reader has run** on every touched canvas (loop step 6b), its verdicts saved.
7. **`gates.py --ship <slug>` exits 0** — run by `scripts/release_upload.py` before it packages
   anything, and by `scripts/hooks/pre-commit` when this commit stages the build or the portal
   entry without `dev: true`. The release page (`release_page` in `v2_state.json`) is signed by LO
   first; the check reads it. Every person it names needs a declared ladder
   (`board.characters[].ladder`, `state.md`): `--ship` checks each step against its canvas, checks
   each unlock can be earned, then plays the build with `playtest.reach_step` — which sets the
   clock and the place for each step and applies its declared gate, but never the step counter,
   so step 3 is reached only if steps 1 and 2 really moved it.
8. **`releases[]` gets `repeatables`, `ladder_steps` and `commit`** (the HEAD the build was made from,
   before the ship commit;
   the next release's step 6b diffs against it) — the lint *repeatables without a step*
   compares the next release against them.

**`dev: true` and `version` are mutually exclusive.** One says not published; the other says this is
what is live. `--release` fails an entry that carries both (`gates.py` ~10147-10150).

### The three places that say what shipped

They drift, and nothing compared them until the check existed:

| | what it is | who reads it |
|---|---|---|
| portal `version` | what the storefronts are told | gamcore / mopoga / itch |
| `[project] version` | the sidebar footer (`engine.md` §38) | **the player, in the game** |
| `releases/v<n>.html` | the build that shipped | you, when a bug report names a version |


### The check

```bash
python3 scripts/gates.py --release <slug>
```

Reads `games/<slug>/output/index.html` and the portal entry. **Off for every ordinary run** — this is
the one mode that judges the artefact — and it exits non-zero on a red, unlike every lint in this
skill.

> ⚠️ **The same warning as step 5 of the loop applies here and is sharper.** This is a **command**,
> not a checklist. `DOCTRINE_GAPS.md` §3a: v1's thirteen-point pre-ship audit was followed by the
> exact bug it was written to prevent. Six boxes to tick would have gone the same way; six checks a
> machine runs do not.

⚠️ **What the check reads, and why it is not the obvious thing.** `[IMAGE MISSING]` and
`[… POOL MISSING]` placeholders are emitted **only under `--debug`** (`v2.py:13346`, `:15641`,
`:15505`). A clean build renders **silent gaps**, so grepping the HTML for those markers passes a
game with missing files. The check reads the build's own flags-init map (`debug_mode`,
`dev_mode_enabled`) and the always-generated `MissingMediaPage` count instead.

⚠️ **The media count is a build-time snapshot.** Files added to disk *after* a build are not in it.
That is correct for a release gate — it judges what ships — and it means the fix for a red is a
**rebuild**, never a file copy.

⚠️ **The archive is reported, never judged.** `output/` is legitimately rebuilt after archiving.

**New BLOCK rules warn first (LO B, 2026-09-30).** A rule that makes a `--ship` BLOCK row stricter carries a
`since` date (`SHIP_SINCE` in `gates.py`). A game whose `v2_state.json` existed before that date
(`SHIP_GRANDFATHERED`: members_only, orientation, probation, the_balance, vesper_two) gets `[WARN] … blocks
from your next release` where only the new rule is red. It keeps warning until it records a release with
`shipped` on or after `since`; then the row blocks. A game started later is blocked from the start. Ordinary
gates are never grandfathered. Rows added since 2026-10-02, each warning first: every system has a card · every system leads to a person or a sex scene.

---

## § The first release (v0.1) — the one exception

v0.1 builds the Board instead of adding to it. **The first version is "0.1", never "1.0"** — the game
is never finished. *(LO decided.)*

- **As many locations as your cast and your loop require, shaped like the reference seed.**
  Derive the count — the places your declared rosters visit, plus what the daily loop needs (sleep,
  earn, wash, cross) — then shape the set: one anchor holding **≥25%** of the prose (the reference game's seed figure; the
  field reaches it by district, `the-board.md` §1), satellites
  free to be small. Each location declares its own word budget, in round numbers, before the
  prose; gate 1 checks the game against that rather than against a global figure. `the-board.md` §1.
  *(The fill SHAPE is measured from the reference seed. A location COUNT is not measurable from it:
  that build already had 25 locations and the true v0.1 is unavailable — its repository begins five
  months after launch. Study 6.)*
- **`gates.py --ship <slug>` exits 0 on the day it ships** *(since 2026-09-26, PRD WS6; it replaced
  "every gate green")*. The BLOCK list is green; the REPORT list is printed and LO judges it when he
  plays. A red REPORT row is not a reason to hold the release, and not a reason to ignore it either.
- **The explicit floor is met from minute one**, including the traversal layer.
- **First explicit beat early** — from a stranger or a one-off, never the paid route or the main man
  (`the-arc.md` A15). The strongest-retained game in the comparison set is explicit on night one,
  two clicks from free roam.
- **The first hour is authored, not assumed** — `references/the-first-hour.md`. One opening shape,
  not both; the funnel hands over into something that is open at the minute it lands; every
  character is met before their portrait goes live; the anchor says what kind of place it is the
  first time she walks in.
- **It ends on a door**, like every release after it.

Then set `phase = "release"` in `v2_state.json` and never build a "chapter" again.
