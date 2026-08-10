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

**5. Gate.** `python3 scripts/gates.py <slug>` green, or fix it.

**6. Ship, and log.** Record in `v2_state.json`: the subject, what it added, **what it
opened**, and the gate scores.

---

## The three kinds of content, and their rules

**STANDING** — she can go there and act, repeatedly.
Carries the explicit floor. This is where the crude register lives — not in the one-time
scenes. The measured failure inverted exactly this, sealing 95% of its explicit prose in a
room with no exits while its nine replayable loops scored zero.

**TRIGGERED** — fires when her state matches.
*"during the weekends"*, *"when exposed"*, *"at high stress"*. For a female protagonist this
is the main heat engine. The loudest complaint in a comparable game's comments was *"I can go
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

## § The first release (v0.1) — the one exception

v0.1 builds the Board instead of adding to it.

- **6–8 locations, shaped like the reference seed:** one anchor holding >=25% of the prose,
  median location >=3,000 words, mean >=4,500. That lands near 30-45k words of prose for a
  seven-location world. Satellites may be small; the anchor may not.
  *(The fill shape is measured from the reference seed. The 6-8 LOCATION COUNT is not: that
  build already had 25 locations, and the true v0.1 is unavailable — its repository begins
  five months after launch. Treat the count as a judgement, the distribution as evidence.)*
- **Every gate green on the day it ships.** v0.1 is not a slice with debt attached; the debt
  model starts *after* it.
- **The explicit floor is met from minute one**, including the traversal layer.
- **First explicit beat early.** The strongest-retained game in the comparison set is explicit
  on night one, two clicks from free roam.
- **It ends on a door**, like every release after it.

Then set `phase = "release"` in `v2_state.json` and never build a "chapter" again.
