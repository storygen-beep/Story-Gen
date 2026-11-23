# craft/clock.md — time, hours and what a button costs

Read this before you write a card that spends time, gives a place or a person hours, or names a time in prose. Checked against Course of Temptation (CoT) (LO, relayed 2026-11-22: "yes, send it"). A place's screen is `craft/places.md`; this file owns its hours.

## Must read

The card's `Craft:` line cites each one, or says in one line why it skips it.

| id | what it asks | the failure it stops |
|---|---|---|
| C889 | a label never promises a clock time; it states the duration, equal to the real spend | — |
| C906 | "till one" is a promise the engine can't keep; keep only the duration | — |
| C926 | the clock moves only by minutes; nothing sends it to a named hour | — |
| C900 | a beat never says what time it is; a repeatable canvas fires at any minute of its window. Make it a rule on a sign | — |
| C902 | the test: read the line at the last minute of its window; is it still true? | — |
| C903 | the same for the weekday: a named day on a repeatable canvas is usually wrong | — |
| C904 | the field names a clock time about 1.1 times per 10,000 words | — |
| C892 | the hour goes on the door, not in the act | — |
| C910 | a button that spends time says how much, one form across the game | — |
| C929 | travel time is tagged on the nav card; an activity's time is tagged nowhere, so the label carries it | — |
| C897 | put time on crossing an area, never on every room | — |
| C924 | travel cost is what makes a schedule matter | — |
| C920 | a move costs a few minutes; a bus to town 20 | — |
| C913 | a thing with hours publishes them: a shut activity stays as a dimmed line | — |
| C930 | without `show_when_blocked`, windowed work vanishes out of hours | — |
| C914 | a row shows its hours only when the clock alone shut it | — |
| C916 | hours go on what she chooses; an event that happens to her stays hidden when shut | — |
| C915 | people's hours go on the schedule page; places with hours get closed text | — |
| C921 | a schedule window may wrap past midnight; no end time means one hour | — |
| C927 | an exit with no time still costs 3 minutes | — |
| C928 | the clock can be shown in the HUD, not printed into prose | — |
| C931 | `time_of_day` is re-read every time, end exclusive, and wraps like schedules | — |
| C890 | the clock repeats, like a bill or a weekly count; it isn't a deadline | — |

## The engine (cited; `v2.py` is `apps/game_generation/twee_comprehensive/generators/v2.py`)

- `window.advanceTime(minutes)` is the only way the clock moves (v2.py:7010). Nothing sets an hour (C926), so "till close" can't be kept.
- An exit's time is `time_progression_minutes`, and 3 when it's left out (v2.py:17936) (C927).
- `setup.isCurrentTimeSlot` handles windows past midnight, and an end time left out is start + 60 minutes (v2.py:4770-4790) (C921). A `time_of_day` condition uses the same function (v2.py:5283-5285) (C931).
- Entering a place spends its `time` cost (`setup.deductLocationCosts`, v2.py:6226-6233), and the nav card shows it as a tag like "30m · 10 Energy" (`setup.getLocationCostTag`, v2.py:6236) (C929). A button's own time shows nowhere unless the label says it.
- `show_when_blocked` with `cooldown_message` keeps a shut activity on screen as a dimmed line with its message (read at v2.py:15104-15108, drawn at v2.py:6740-6748) (C913, C930). That's only when the clock alone shut it. A row shut by something waiting can't fix (clothes, money, a meter, a flag) greys out with its `locked_text` instead, or stays hidden without one (v2.py:6689-6697; `craft/clothes.md`).
- A place shut by its hours says "Closed. Opens at …" (`setup.locClosedReason`, v2.py:11772-11779), and its `closed_text` shows at the door (v2.py:11444-11447).
- People's hours have their own Schedules page (`:: SchedulePage`, v2.py:24399) (C915).
- No token prints the current time into prose (C928): a grep of v2.py for `@time` finds none.

## The measures (re-run 2026-11-22)

All 5,294 passages in `/Users/a0000/Documents/Player_Legibility_Study_20260825/corpus/course-of-temptation/passages`, with macros and tags stripped: 425,667 words.

| what | CoT | field |
|---|---|---|
| clock times in prose (`\d{1,2}(:\d\d)? ?(am\|pm\|o'clock)`) | 26, 0.61 per 10,000 words | 1.1 (C904) |
| weekday names | 61, 1.43 per 10,000 words | — |
| files with closed or opening text | 65 | — |
| `<<advtime N>>` sizes, most common | 1 (180), 5 (114), 20 (76), 60 (74), 10 (72), 30 (38) | — |
| hours as a rule on a sign | "A sign says it's open between 7am and midnight"; also 7am–10pm, 5am–10pm, and "%openhour and %closehour" | — |
| a person's hours | a "Nightlife Schedule" section on the person's page (`DisplayNPCWidgets.txt`, line 816) | — |

Every option prints its time with `<<dtime N>>` after the link. The bus back to campus is `<<advtime 20>>` and `<<dtime 20>>` (`RiversidePlaza.txt`, line 110). CoT's crowds are generated per place; its passages show no fixed per-person schedule rows. Fixed rows come from other top games (IHOH, C892) and from our engine.

## The shape

Each rule is marked **measured** or **LO's choice**.

1. **Every button shows its time cost** (C910, C929). *Measured:* CoT prints `<<dtime>>` on its options; the commonest costs are 1, 5, 20 and 60 minutes.
2. **Time is spent on travel between areas; moving inside an area is cheap** (C897, C924, C920). *Measured:* CoT's bus is 20 minutes; going into a building is 1.
3. **No clock times in story text.** An hour that matters goes on a sign, as a rule: "A sign says it's open between 7am and 9pm" (C900). The test is the last minute of the window (C902). *Measured:* CoT 0.61 per 10,000 words, the field 1.1 (C904).
4. **A closed place stays visible, dimmed, and says when it opens** (C913, C914). An event that happens to her stays hidden when shut (C916). *LO's choice,* and our engine does it ("Closed. Opens at …").
5. **People's hours go on their page** (C915). *Measured:* CoT's "Nightlife Schedule"; our engine's Schedules page.
6. **Durations, never "till X"** (C889, C906, C926). *Measured in the field:* 24 of 84,009 labels name a clock time (C906); the engine only adds minutes.
7. **No named weekday on a repeatable screen** (C903). *LO's choice;* CoT names a weekday 1.43 times per 10,000 words.
8. **The clock repeats** (C890): a weekly bill, a weekly count, not a deadline. *LO's choice, stated.*

## Worked example

Roles: the café owner. LO approved these words, with the name swapped for a role.

**Café**
> A narrow café across from campus: six tables, a chalkboard menu, a coffee machine that screams. Students camp here with laptops. A sign by the door says it's open between 7am and 9pm.

Presence, from his rows: "The owner's behind the counter, wiping the same spot."

Buttons: Buy a coffee ($3, 10 min) · Ask about the Help Wanted sign (once) · Walk to the quad (5 min).

Closed, seen from the street: "Café", dimmed, "Opens at 7am".

## Not this

- "It's nine in the morning and the café is quiet." A repeatable screen shows at any minute of its window (C900, C902).
- "Work till close." The engine only adds minutes. Write "Work a shift (4 hours)" (C889, C926).
- A button with no time on it (C929).
- A shut place that just disappears. It stays, dimmed, with when it opens (C913, C930).
