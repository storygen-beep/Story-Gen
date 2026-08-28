# The Release — the unit of work

The game is never the unit. The **release** is, and it repeats forever.

---

## What a release actually is

Measured, from one full six-week cycle of the reference game (274 commits, 153 non-merge):

| | |
|---|---|
| new scene units | **+196** |
| new words | **+24,388** |
| **new locations** | **0** |
| new files | 2 (one of them a job at an *existing* location) |
| commits that were fixes | **55.6%** |
| commits that added content | **6.5%** — ten of them |

And here is every one of those ten content commits, in the developer's own words:

> peek on Bailey with a date at the flat, weekends · skin tone characteristic · expanded
> Bailey's combat speech · Whitney and friends visit you at the Hookah Parlor · exposed player
> meets an opportunistic bondage photographer on the town street · cliff street event at high
> stress · Kylar kidnap trigger · sprites · small additions

**Every single one is an event at an existing place with an existing character.** No new
location. No new character. No plot advancement. Three of the ten are keyed to player state.

That is the template. Copy its shape, not its subject.

---

## The loop

**1. Read the Want.** Not optional, not skimmable. Name the line this release serves. If you
cannot, the release is unfocused — pick again.

**2. Pitch — three, independent.** Three Pitcher agents, no shared context, three takes on the
subject. LO picks one. Independence is the point: shared context produces three shades of one
idea. See `references/agents.md`.

**3. Attack, before writing.** The panel runs on the *design*, not the build. Every cheap
catch in our history happened here; every expensive one happened after shipping. Same agents,
different timing, an order of magnitude in value.

**4. Write.** Events on existing surfaces. Default to **zero new locations** — if this release
opens one, it arrives filled, not as a promise.

**5. Gate — and read the lists.** `python3 scripts/gates.py <slug>` green, or fix it. That same
command prints **nineteen lints below the tally**, and they are the half of the instrument that
judges nothing: a game can be green on every gate with the lints full. Off Season shipped **37/38
with 67 flagged words in the player's face**, and the two the author never looked at reached LO on
a button.

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

**6. Ship, and log.** Record in `v2_state.json`: the subject, what it added, **what it
opened**, the gate scores, and **the lint figures you are shipping with** — at minimum the
own-words count and anything you consciously left. A number in the ledger is one that has to come
down next time; a number only in a terminal is one nobody is holding. This is the same mechanism
the anchor share already runs on, and the reason the anchor gets budgeted and the word list does
not is only that one of them was written down.

---

## The three kinds of content, and their rules

**STANDING** — she can go there and act, repeatedly.
Carries the explicit floor. This is where the crude register lives — not in the one-time
scenes. The measured failure inverted exactly this, sealing 95% of its explicit prose in a
room with no exits while its nine replayable loops scored zero.

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
- **Named but never paid.** Another dangled a character for years — *"Are we EVER going to
  talk to the university president?"* Log every promise in the state file, and pay or cut it.

And state the current ceiling honestly. The reference game prints a plain marker at the top of
each track so the player knows where the wall is. An honest wall is a promise; a silent one is
a bug report.

---

## Maintenance is the job, not a failure

**55.6% of the measured release was fixes.** Across eight years, the reference game's releases
run roughly 87% non-new content.

So a release that is half repair is *normal*. Budget it. Do not treat a high rework rate as a
defect to apologise for — under-shooting it is the more likely error.

---

## Cadence

Measured across the funded cohort: **~31 days** between versions, sustained four to eight
years. Slippage is the strongest single predictor of decline; pages holding cadence carried a
median 684 paying members against 176 for those slipping.

Posting volume predicts revenue (ρ = +0.58). Release *speed* does not (ρ = −0.09).

**Visible motion matters more than shipped volume.** Ship smaller, on time.

---

## § Shipping the build — the boundary nothing was holding

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

**`dev: true` and `version` are mutually exclusive.** One says not published; the other says this is
what is live. The schema never stated the relationship, which is why nothing could adjudicate
`forty_miles` carrying both.

### The three places that say what shipped

They drift, and nothing compared them until the check existed:

| | what it is | who reads it |
|---|---|---|
| portal `version` | what the storefronts are told | gamcore / mopoga / itch |
| `[project] version` | the sidebar footer (`engine.md` §38) | **the player, in the game** |
| `releases/v<n>.html` | the build that shipped | you, when a bug report names a version |

Measured 2026-08-28: `forty_miles` read `0.1` / `0.1.2` / `{0.1, 0.1.1, 0.1.2}` — the portal two
releases behind the number in the player's face. `vesper` was the only game where all three agreed.

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
`[… POOL MISSING]` placeholders are emitted **only under `--debug`** (`v2.py:12549`, `:14753`,
`:14906`). A clean build renders **silent gaps**, so grepping the HTML for those markers passes a
game with 183 missing files. The check reads the build's own flags-init map (`debug_mode`,
`dev_mode_enabled`) and the always-generated `MissingMediaPage` count instead.

⚠️ **The media count is a build-time snapshot.** Files added to disk *after* a build are not in it.
That is correct for a release gate — it judges what ships — and it means the fix for a red is a
**rebuild**, never a file copy.

⚠️ **The archive is reported, never judged.** `output/` is legitimately rebuilt after archiving, and
a byte-equality gate would have failed the one game whose versions agreed.

---

## § The first release (v0.1) — the one exception

v0.1 builds the Board instead of adding to it.

- **As many locations as your cast and your loop require, shaped like the reference seed.**
  Derive the count — the places your declared rosters visit, plus what the daily loop needs (sleep,
  earn, wash, cross) — then shape the set: one anchor holding **≥25%** of the prose, satellites
  free to be small. Each location declares its own word budget, in round numbers, before the
  prose; gate 1 checks the game against that rather than against a global figure. `the-board.md` §1.
  *(The fill SHAPE is measured from the reference seed. A location COUNT is not measurable from it:
  that build already had 25 locations and the true v0.1 is unavailable — its repository begins five
  months after launch. This bullet used to carry "6–8" with exactly that caveat attached, and all
  three v2 games shipped 8. A caveat in prose does not survive next to a number, so the number is
  gone. Study 6.)*
- **Every gate green on the day it ships.** v0.1 is not a slice with debt attached; the debt
  model starts *after* it.
- **The explicit floor is met from minute one**, including the traversal layer.
- **First explicit beat early.** The strongest-retained game in the comparison set is explicit
  on night one, two clicks from free roam.
- **The first hour is authored, not assumed** — `references/the-first-hour.md`. One opening shape,
  not both; the funnel hands over into something that is open at the minute it lands; every
  character is met before their portrait goes live; the anchor says what kind of place it is the
  first time she walks in. This is the half v2 shipped without, and it cost the first v2 game a
  human read end to end its whole first ten minutes.
- **It ends on a door**, like every release after it.

Then set `phase = "release"` in `v2_state.json` and never build a "chapter" again.
