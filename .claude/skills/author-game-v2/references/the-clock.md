# The Clock — the time the game promises and the time the engine keeps

Every sentence, label and card that says *when*. The hour a beat claims it is, the hour a button
promises to reach, the hours a place is open, and the days a line says have gone by.

This file owns **one rule**, and every section below is that rule applied:

> **Name a time only where the engine pins it. The engine pins exactly one moment in a whole
> game: the first screen.**

> Measured failure this exists to prevent: a shipped game offering **"Work the counter till one
> (2h 30m)."** on a canvas open 08:00–13:00, in an engine with **no absolute-time advance at all**.
> Enter at 08:00 and the click lands at 10:30. Enter at 12:55 and it lands at 15:25, inside the
> afternoon band. The label is right for **one minute** of a five-hour window. Two paragraphs
> above it, the same canvas opens **"Shutter up at eight"** — true for 1 minute of 300 — while the
> paragraph beside it, *"Nobody comes in before eleven in February,"* is true at every minute of
> every day. Same screen, same author, one line a fact and one a guess.

**Why this file exists at all.** v1 carried **Rule 10 — "Never assert elapsed time the player's
pace controls"** (`author-game/references/rts-flat-prose.md:360`), with an exemption list, a
replacement table, and the note that where precision *is* the character you keep the precision and
drop the number. v2's `register.md` shipped without it and without any rule about time: a grep of
every v2 reference file for `clock|o'clock|name a time|absolute time|time of day` returns only
engine mechanics. And Rule 10 only ever governed **days and weeks** — it never mentions the clock,
which is the half that broke. This is `DOCTRINE_GAPS.md` Tier 2 row 7.

Engine claims here carry a `file:line` into
`apps/game_generation/twee_comprehensive/generators/v2.py`, per `SKILL.md` operating rules.

## Contents
1. C1 · The engine pins one moment, and it is the first screen
2. C2 · A beat may not say what time it is — turn the reading into a rule
3. C3 · A label may not promise a clock time
4. C4 · A label that spends the clock says how much
5. C5 · If a thing has hours, publish them
6. C6 · Never assert elapsed time the player's pace controls
7. What the scoreboard checks
8. Cheat sheet

---

## C1 · The engine pins one moment, and it is the first screen

`[time] starting_hour` is the only clock reading in the game that is guaranteed. Everything after
it is the player's pace.

```
grep -E 'target_hour|advance_to|until_time|time_target' v2.py     0 hits
```

`advanceTime(minutes)` (`v2.py:5400`) adds minutes to `time_state` and rolls the day when the hours
pass 24. That is the whole time API. There is **no way to send the clock to a named hour**, and no
way to print the current one into prose either — `_resolve_at_references` (`v2.py:14027`) resolves
`@player` and `@<npc>` and nothing else, so there is no `@time` token to fall back on.

A node exit that declares nothing still moves the clock: the default is **3 minutes**
(`v2.py:13200`, `config.get('default_time_progression', 3)`; the exception fallback at `:13388`
emits the same). So a player walking a four-node opening has already drifted 9 minutes before
their first real choice.

The clock is not hidden — `<<timeDisplay>>` sits at the top of `StoryCaption` in every build
(`v2.py:15663`, `:15679`), rendering a live 12-hour reading through `<<timeFormatted>>`
(`v2.py:16043`) — and it carries **wait buttons**: `>` is 10 minutes, `>>` is an hour, `>>>>>` is a
day (`v2.py:16115-16135`, `waitTime` at `v2.py:5442`). The player can always see the time and can
always move it. That is exactly why the prose must not compete with it.

**What C1 licenses.** The opening's first node, before any exit has fired, may state the starting
hour. `off_season` declares `starting_hour = 7` and opens *"You wake at seven with your breath
going up in front of you"* — correct, and the only correct instance of its kind in that game.

---

## C2 · A beat may not say what time it is — turn the reading into a rule

A repeatable canvas fires at any minute of its window. Measured across all ten games in this repo:

```
canvas schedule windows          median width 149–540 minutes per game
windows 60 minutes or narrower   5, in the entire repo
                                 (forty_miles 1 · back_home 1 · last_call 3)
```

At those widths **no beat in any game shipped here can honestly state the current hour.** A
sentence that reads as a clock is wrong for almost the whole window it fires in.

**The move is grammatical, not editorial.** A reading becomes a rule and the fact survives intact:

| ❌ a reading — false for most of the window | ✅ a rule — true at every minute |
|---|---|
| "Shutter up at eight and the light comes in about four feet and stops." | "The shutter goes up at eight and the light comes in four feet and stops." |
| "You wake at ten to seven and you do not have to be downstairs until eight." | "You wake before the house does. Nobody wants you downstairs until eight." |
| "Twenty past nine and the front door goes." | "The front door goes. That is the bus, and that is your mother." |
| "It is twenty past six." | "Three pegs still have clothes on them. Three people are still in the water." |
| "You count them at one o'clock out of habit." | "You count them every time you pass, out of habit." |

The right-hand column is not a compromise. Every one of them is **more specific**, because the hour
was doing the work a detail should have been doing.

### What is exempt, and it is most of what looks like a violation

These name an hour and are correct at any minute. Do not sweep them:

- **A rule of the world** — *"Nobody comes in before eleven in February."* · *"She is asleep behind
  it from eight until three."* · *"The light over the door is on most nights until one."* A shift
  pattern, an opening time, a bus. Carried forward from v1 Rule 10's *"job descriptions, not elapsed
  play."*
- **Backward canon fixed by a prior chapter** — *"twenty-one years in this room"*, *"eleven years
  behind that counter"*. The player cannot move them.
- **In-scene relative time** — *"a minute later"*, *"all night"*, *"by the time she is done"*.
- **A forward consequence** — *"the room will be cold again by six."*

**The test, in one question:** *if the player reads this line at the last minute of the canvas's
window, is it still true?* Rule → yes. Reading → no.

### The same test runs on two more axes, and the lint sees neither

C2 is written about the **hour** because that is where it was found. The test is not about hours.

**The day of the week.** A repeatable canvas fires on every weekday its schedule allows, so a named
day is a reading with a six-in-seven chance of being wrong:

| ❌ a reading | ✅ a rule |
|---|---|
| *"Forty-one sixty. The pitch is ninety. It is Thursday."* — an all-days canvas | *"…it is not ninety. It has not been ninety since the clocks went back."* |
| *"It's not Monday. What's gone wrong?"* — said by a character whose rota includes Monday | *"You don't come down here. What's gone wrong?"* |

Both of those shipped. The second is worse than it looks: it is the **first line the player reads**
on that character's hub, and it was wrong once a week from the day it was written.

**A figure the state already holds.** Money, energy, a relation — if the sidebar is printing it,
the prose may not also assert it. *"Forty-one pounds sixty"* is a number the player can see is
wrong, in a game whose entire pressure is counting toward the rent.

> **The general form: a beat may not state anything the engine is already tracking.** The hour, the
> day and the money are the three this repo has been caught on; the rule covers whatever is next.

⚠️ **`the clock in the prose` cannot see either of these.** It scans hours. The day axis and the
state-held figure are **read by a human or not at all** — check them when you check the list.

### How often the field names an hour at all

One instrument over 25 shipped sandboxes, 11.0M words
(`~/Documents/Mopoga_Twine_Sandbox_Research_20260724/`), and our ten:

```
FIELD median 1.1 clock references per 10,000 words          p75 2.1
─────────────────────────────────────────────────────────────────────────────────────
last_call        v1    0.0        the_inheritance v2    9.4
mothers_place    v2    0.0        late_shifts     v1   13.9
vesper           v1    2.9        back_home       v2   17.9
                                  seventh_day     v2   19.4
                                  the_allowance   v2   27.1
                                  forty_miles     v2   34.4
                                  steam           v2   36.7
```

Only three field games sit as high as ours. **Our own largest game already sits inside the field's
band**, so this is a bar shipped work has cleared.

> ⚠️ **These numbers were re-measured 2026-08-22 and they went UP for us and not for the field.**
> The instrument had three blind spots — `half nine`, `<hour> in the morning` with no preposition,
> and an hour followed by `the` (*"by nine **the** whole flat…"*, killed by the stoplist entry that
> was there to catch *"at one point"*). Closing them moved the **field** from 1.0 to 1.1 on a single
> true positive, and moved **ours by a quarter to a half**: off_season 20.1 → 26.4, steam 29.2 →
> 36.6, forty_miles 22.6 → 34.4.
>
> **The blind spots were hiding our defects and almost none of the field's**, because the
> constructions they missed are ones our authors reach for and the corpus does not. Two of the four
> readings it newly caught in off_season were **one-shots that open a milestone** — *"Half nine and
> the flat is at twenty-four degrees"*, *"Half eleven and the telly has been on mute"* — which no
> earlier pass had ever listed.
>
> Dropping the stoplist altogether was tested and **rejected**: it inflates the field to 1.2 / 2.6,
> which is noise being scored. The instrument deliberately under-counts rather than over-counts —
> the safe direction for a list nobody scores.

> ⚠️ **Two explanations for that gap were tested and both failed. Do not repeat them.**
>
> **"The field keeps hours out of prose because its clocks are coarse."** False. Classifying every
> field game by what its state actually mutates: minute-clock games median **2.4** per 10k,
> hour-clock **4.9**, slot-clock **1.1**, no-clock **1.4**. Every bucket sits between 1 and 5.
> `degrees-of-lewdity` tracks minutes across 2.1M words and names an hour **0.4** times per 10k.
> Resolution does not predict it, so **do not coarsen the clock** — a fine clock is fine, and it
> belongs in the interface, which is where ours already is.
>
> **"The field puts hours in timetables; we put them in beats."** Also false. A sentence-level
> instruction-versus-narration split came back **33.0% field / 33.5% ours** — no separation at all.
> The difference is **volume**, not placement.

---

## C3 · A label may not promise a clock time

A label is a promise about what the click does. The engine cannot deliver a clock time (C1), so a
label naming one is a promise it cannot keep.

```
❌  Work the counter till one (2h 30m).       enter 08:00 → 10:30 · enter 12:55 → 15:25
✅  Work the counter (2h 30m).                true at every entry minute
```

The fix is deleting two words. What remains is the only part the engine can honour.

**The field is close to unanimous.** Across **92,226 link labels** in the same 25 games:

```
    2  name a clock time     "Wait until 21:00" · "Wait until 20:00"     both explicit WAIT actions
    0  promise a clock time as the OUTCOME of an action
```

Both survivors are buttons whose entire purpose *is* to reach that hour, which the player is
choosing to spend. Ours: **13 clock-time labels across four v2 games** (steam 8, off_season 2,
seventh_day 2, forty_miles 1) and **zero across all four v1 games**.

Even a game that *can* do it does not. `lust-for-life` ships an absolute-time primitive
(`$time.setTime(23, 55)`) and calls it **270 times** — and the labels sitting next to those calls
read *"Back home"*, *"Leave"*, *"Go to the SPA"*. The hour is engine business; the button says what
you are doing.

**If a rung genuinely needs to end at a named hour, it is a window problem, not a wording problem.**
Narrow the canvas's schedule until the claim is true across it, or drop the hour. There is no third
option, because there is no absolute advance to reach for.

---

## C4 · A label that spends the clock says how much

The engine is already inconsistent with itself here, and the author is the one who pays.

- **Travel time is tagged automatically.** `getLocationCostTag` (`v2.py:4724`) renders `20m` on the
  navigation card from `[[locations.costs]] time`, used at `v2.py:19353` and `:19370`.
- **Activity time is not tagged at all.** A choice's `time_progression_minutes` emits a bare
  `<<script>>advanceTime(150);<</script>>` at the bottom of the passage body (`v2.py:12733`) with
  nothing on the label.

So a door says `20m` and a two-and-a-half-hour shift says nothing. The sidebar clock jumps and the
player is not told why — and that is where the temptation to write the hour into the prose comes
from in the first place.

**Put the duration in the label, in one form, and hold that form across the game.**

```
Work the counter (2h 30m).
Do the float and the change bags (40m).
Buy coffee (0:02 £2)                    the field's own form — the-voice.md R1
```

`the-voice.md` R1 already carries that last example and already says *"every one that charges the
player states the charge on the button, before the click"* — but only the **money** half is gated
(`gates.py` gate `a price is on its label`). This rule is the time half of the same sentence.

**A stated duration must be the truth.** `off_season` gets this right and it is worth copying: the
label states the duration on the **choice**, and the engine charges it on the **target node's
exit** — `Work the counter (2h 30m).` targets `rung_arcade_take_am.base`, whose exit carries
`time_progression_minutes = 150`. All eight of that game's duration tags match their real spend.
The gate walks that same path, so a tag that drifts from its spend fails.

> **Honest limit.** Duration-tagging is **one game's convention**, not a field norm: 4,219 of the
> corpus's 4,260 duration tags are `degrees-of-lewdity`'s, and among the five field games with a
> minute-resolution clock only that one does it. It is the corpus's largest and most-played
> sandbox, which is a reason to follow it — but it is a **recommendation with a lint**, not a gate,
> and `gates.py:2825` already refuses to invent exactly this kind of threshold for stamina costs.

---

## C5 · If a thing has hours, publish them

An activity whose window has closed **vanishes**. No greyed line, no reason, no hours. The player
who worked the counter yesterday morning arrives at two in the afternoon and the button is simply
gone — which reads as a broken game, not a schedule.

The engine has the surface for this and **no game in this repo has ever used it**:

```toml
[canvases.trigger]
location         = "the_arcade"
is_repeatable    = true

[canvases.trigger.metadata]
show_when_blocked = true
cooldown_message  = "<one line saying when this is available>"
```

`show_when_blocked` and `cooldown_message` are read at `v2.py:11055-11059` and emitted as
`showWhenBlocked` / `cooldownMessage` (`v2.py:11100-11101`). When `isCanvasValid` returns false —
and it returns false on a **schedule miss** first of all (`v2.py:4573-4580`) — the renderer keeps
the entry as a dimmed, non-clickable line carrying the author's message instead of dropping it
(`v2.py:5093`, `:5099`, `:5143`).

That line is the right home for an hour. It is a rule, it is in the interface rather than the
prose, and it is the one place the player can act on it.

**People already have this surface; places and activities do not.** `SchedulePage`
(`v2.py:18964`) publishes every declared `[[npcs.schedules]]` row as a Time / Location / Activity /
Days table, and it is the only screen in the game that tells the player when to come back. A place
with hours and no `cooldown_message` is a schedule the player can only learn by losing a day to it.

⚠️ The top-30 mopoga study found **lostness, not grind, is this genre's disease** — 4.7% of player
complaints against 0.9%. A hidden window is lostness with a clock on it.

---

## C6 · Never assert elapsed time the player's pace controls

v1's Rule 10, restored. **Read every duration in a beat and ask whether the player can make it
false.** If they can, it is a defect, not a preference.

A sandbox makes this worse than it looks, because a chapter gated on a **meter** has no floor and
no ceiling in days: a ladder gating at 6/12/18 with +2/+3/+3 a shift bottoms out around four
in-game days, a paid grant can collapse it to zero, and a slow player can take months. There is no
number that is right for all three.

| ❌ asserts what the engine cannot keep | ✅ true at any pace |
|---|---|
| "Four weeks on my floor and not one glass" | "All this time on my floor and not one glass" |
| "You've had three weeks and you've turned up every one" | "You've had every night since, and you've turned up for every one" |
| "quiet for eleven days" | "quiet since she closed it up" |
| "Fourth shift." | "Another shift." |

**Exempt:** backward canon fixed by a prior chapter · in-scene time ("a minute later", "all night",
"tomorrow night") · shift patterns and job descriptions ("six nights a week") · forward consequences ("that mark
will still be on the wall next week").

⚠️ **Where the precision IS the character, keep the precision and drop the claim.** A man who
counts is frightening because he counted — *"You looked at this door exactly once, and I know which
night it was"* keeps everything *"Your fourth shift"* was doing and claims nothing the engine has
to honour.

⚠️ **The same check catches invented economy figures.** A number the player can compare against
their own wallet is a number the game has to be right about.

---

## What the scoreboard checks

One gate and two lints. `python3 scripts/gates.py <slug>`.

| | |
|---|---|
| gate · **the label keeps its time** | C3 + C4. No choice label names a clock time; where a label states a duration, it equals the minutes that click actually spends (choice → target node → that node's exit). **n/a** when a game has no choice labels at all. |
| lint · **the clock in the prose** | C2. Every clock reference in a beat with its canvas's window width beside it, plus the game's rate against the field distribution. A list to read, never a score. |
| lint · **the time cost is not on the button** | C4. Every click that moves the clock 60 minutes or more without a duration on its label. |

Where each stood when the check landed, 2026-08-22 — read off the shipped gate, not a prediction:

```
                    label keeps its time
steam                   FAIL   8 labels
off_season              FAIL   2
seventh_day             FAIL   2
forty_miles             FAIL   1
the_allowance           PASS
back_home               PASS
vesper          (v1)    PASS
last_call       (v1)    PASS
late_shifts     (v1)    PASS
the_inheritance (v1)    PASS
```

**Six of ten pass, and that includes all four v1 games**, so the bar is one shipped work has
already cleared. `off_season`'s eight duration tags all match their real spend, so its only failure
is the two words `till one` and `till seven`.

> **Why C2 and C4 are lints and not gates.** A shift-driven world names hours as *rules* and should:
> `seventh_day`'s `rung_kitchen_rota` and `steam`'s shift board are correct work that a rate gate would
> fail. That is `SKILL.md`'s *"a check that fails a game for obeying the doctrine is a bug in the
> check"* — the trap that killed the proposed `locked_text` gate. And duration-tagging is one
> game's convention (see C4's honest limit), so gating it would be the invented threshold
> `gates.py:2825` already refuses. Both print their findings and neither moves the tally.

---

## Cheat sheet

- **Name a time only where the engine pins it.** It pins exactly one: `[time] starting_hour`.
- **There is no absolute-time advance** — `advanceTime(minutes)` is the whole API (`v2.py:5400`),
  and there is no `@time` token to print the clock either (`v2.py:14027`).
- **A beat may not say what time it is.** Windows here run 149–540 minutes wide; five in the whole
  repo are an hour or less.
- **Turn the reading into a rule.** *"Shutter up at eight"* → *"The shutter goes up at eight."*
  Same fact, no claim about now.
- **Exempt:** world rules and shift patterns · backward canon · in-scene relative time · forward
  consequences. Most of what looks like a violation is one of these.
- **The test:** read it at the last minute of the canvas's window — still true?
- **A label may not promise a clock time.** `till one (2h 30m)` → `(2h 30m)`. Field: 2 in 92,226,
  both explicit waits.
- **A label that spends the clock says how much**, in one form, held across the game. Travel time
  is tagged for you (`v2.py:4724`); activity time is not (`v2.py:12733`).
- **A stated duration must equal the real spend** — the gate walks choice → target node → exit.
- **If a thing has hours, publish them** — `show_when_blocked` + `cooldown_message`
  (`v2.py:11055`), the one surface where an hour belongs. Zero games have used it.
- **Never assert elapsed time the player's pace controls** — and where the precision is the
  character, keep the precision and drop the claim.
