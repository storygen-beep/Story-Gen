# craft/clock.md — time, hours and what a button costs

Read this before you write a card that spends time, gives a place or a person hours, or names a time in prose. Checked against Course of Temptation (CoT) (LO, relayed 2026-11-22: "yes, send it"). A place's screen is `craft/places.md`; this file owns its hours.

## Must read

On a card with a `Does:` block (every card from 2026-11-24 on), the rows that apply come from `check.py --rules`, which lists each with its craft file; the card has no `Craft:` line (`piece.md` step 2). On a card from before 2026-11-24, the `Craft:` line cites each one, or says in one line why it skips it. `when` and `judge` are the labels in `SKILL.md`, "Rule labels".

| id | what it asks | the failure it stops | when | judge |
|---|---|---|---|---|
| C889 | a label never promises a clock time and states no duration either; the real spend still equals the costs (LO, 2026-11-24: "Beside choice i dont want to show time and energy show money if needed"; "Room buttons too") | — | the clock moves | note |
| C906 | "till one" is a promise the engine can't keep; leave the time off the label | — | the clock moves | note |
| C926 | the clock moves only by minutes; nothing sends it to a named hour | — | the clock moves | note |
| C900 | a beat never says what time it is; a repeatable canvas fires at any minute of its window. Make it a rule on a sign | P13 reader pass 6: the wake screen said "Monday, seven in the morning." | the clock moves | reader |
| C902 | the test: read the line at the last minute of its window; is it still true? | — | the clock moves | note |
| C903 | a repeatable names a weekday only behind a weekday condition, on its trigger or a group around the line, that makes it true on every visit | — · kept blocking: LO's choice (2026-11-24) | the clock moves | reader |
| C904 | the field names a clock time about 1.1 times per 10,000 words | — | the plan | note |
| C892 | the hour goes on the door, not in the act | — | the clock moves | note |
| C910 | a button or a reply says no time and no energy; it states money only when the act costs money, one form across the game (LO, 2026-11-24: "Beside choice i dont want to show time and energy show money if needed"; "Room buttons too") | — | the clock moves | note |
| C929 | travel time is tagged on the nav card by the engine; an activity's time is tagged nowhere, and its label doesn't carry it either: the clock and the energy bar show the spend (LO, 2026-11-24: "Beside choice i dont want to show time and energy show money if needed"; "Room buttons too") | — | the clock moves | note |
| C897 | put time on crossing an area, never on every room | — | the clock moves | note |
| C924 | travel cost is what makes a schedule matter | — | the clock moves | note |
| C920 | a hop inside an area (between rooms, or to a place next door) costs nothing; time is spent on the moves between areas, like a bus to town at 20 minutes. The engine charges only the destination's entry cost, so a cost on a hop is charged one way only | P13 reader pass 7: the same move inside the house was "(10 min)" on one screen and "(5 min)" on another; P05a1-c1: quad to Café 5 minutes, Café to quad 0; P02b1-c2: the free house moves FAILED the old wording | the clock moves | reader |
| C913 | a thing with hours publishes them: a shut activity stays as a dimmed line | — · kept blocking: LO's choice (2026-11-24) | the clock moves | reader |
| C930 | without `show_when_blocked`, windowed work vanishes out of hours | — | the clock moves | note |
| L167 | different hours on different days are one row with a `group` condition, never one row per day kind; it greys with `show_when_blocked` and a `cooldown_message` naming the full hours | first_term_lean P10: six café rows, and the weekday row greyed beside the live weekend row | the clock moves | reader + sheet |
| C914 | a row shows its hours only when the clock alone shut it | — · kept blocking: LO's choice (2026-11-24) | the clock moves | reader |
| C916 | hours go on what she chooses; an event that happens to her stays hidden when shut | — · kept blocking: LO's choice (2026-11-24) | the clock moves | reader |
| C915 | people's hours go on the schedule page; places with hours get closed text | — | the plan | note |
| C921 | a schedule window may wrap past midnight; no end time means one hour | — | the plan | note + sheet |
| C927 | an exit with no time still costs 3 minutes | — | the clock moves | note + sheet |
| C928 | the clock can be shown in the HUD, not printed into prose | P13 reader pass 6: the same line printed the clock into prose | the clock moves | reader |
| C931 | `time_of_day` is re-read every time, end exclusive, and wraps like schedules | — | the clock moves | note + sheet |
| C890 | the clock repeats, like a bill or a weekly count; it isn't a deadline | — · kept blocking: LO's choice (2026-11-24) | the plan | reader |

## The engine (cited; `v2.py` is `apps/game_generation/twee_comprehensive/generators/v2.py`)

- `window.advanceTime(minutes)` is the only way the clock moves (v2.py:7021). Nothing sets an hour (C926), so "till close" can't be kept.
- An exit's time is `time_progression_minutes`, and 3 when it's left out (v2.py:17947) (C927).
- `setup.isCurrentTimeSlot` handles windows past midnight, and an end time left out is start + 60 minutes (v2.py:4770-4790) (C921). A `time_of_day` condition uses the same function (v2.py:5283-5285) (C931).
- Entering a place spends its `time` cost (`setup.deductLocationCosts`, v2.py:6248-6256), and the nav card shows it as a tag like "30m · 10 Energy" (`setup.getLocationCostTag`, v2.py:6259) (C929). Only the destination's cost is charged, on a real move into a different place (`setup.travelMoveSlug`, v2.py:20490-20497; charged at v2.py:20512), so leaving a place costs nothing (C920). A button's own time shows nowhere, and by LO's rule its label doesn't say it either (C910).
- `show_when_blocked` with `cooldown_message` keeps a shut activity on screen as a dimmed line with its message (read at v2.py:15115-15119, drawn at v2.py:6751-6759) (C913, C930). That's only when the clock alone shut it. A row shut by something waiting can't fix (clothes, money, a meter, a flag) greys out with its `locked_text` instead, or stays hidden without one (v2.py:6700-6708; `craft/clothes.md`).
- A place shut by its hours says "Closed. Opens at …" (`setup.locClosedReason`, v2.py:11783-11790), and its `closed_text` shows at the door (v2.py:11455-11458).
- **A condition item can be a group:** `{ type = "group", logic = "AND"|"OR", items = [...] }`, read with its own logic, recursively; an empty group, or one nested deeper than 3, is false (v2.py:5405-5413). A group made only of clock items counts as the clock, so its row greys with its `cooldown_message` instead of hiding (`setup.onlyTheClockShut`, v2.py:6076). Tests: `apps/game_generation/tests/test_condition_groups.py`.
- People's hours have their own Schedules page (`:: SchedulePage`, v2.py:24410) (C915).
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

1. **A button or a reply says no time and no energy; it states money only when the act costs money** (C910, C929): "Buy lunch ($4)", "Pay him ($20)", never "Eat something (20 min, +15 energy)". The real spend still equals the costs. The engine's own tags stay: a greyed row's cost when she can't afford it, "(15 Energy)", which says why it is grey, and the nav card's travel tag, "45m · 10 Energy". This rule is about the words the author writes. *LO's choice* (LO, 2026-11-24: "Beside choice i dont want to show time and energy show money if needed"; "Room buttons too"). CoT does otherwise: it prints `<<dtime>>` on its options, most often 1, 5, 20 and 60 minutes.
2. **Time is spent on travel between areas; a hop inside an area costs nothing** (C897, C924, C920). A hop is a move between rooms, or to a place next door; a bus or a walk across town is a move between areas. The engine charges only the destination's entry cost (`setup.travelMoveSlug`, `v2.py:20490`; charged at `v2.py:20512`), so a cost on a hop inside an area is charged one way only: quad to Café 5 minutes, Café to quad 0. Put cost only on the moves between areas. *Measured:* CoT's bus is 20 minutes; going into a building is 1.
3. **No clock times in story text.** An hour that matters goes on a sign, as a rule: "A sign says it's open between 7am and 9pm" (C900). The test is the last minute of the window (C902). *Measured:* CoT 0.61 per 10,000 words, the field 1.1 (C904).
4. **A closed place stays visible, dimmed, and says when it opens** (C913, C914). An event that happens to her stays hidden when shut (C916). *LO's choice,* and our engine does it ("Closed. Opens at …").
5. **People's hours go on their page** (C915). *Measured:* CoT's "Nightlife Schedule"; our engine's Schedules page.
6. **Never "till X"** (C889, C906, C926). The engine only adds minutes, so the spend is a duration in the costs, and the label names neither a clock time nor the duration. *Measured in the field:* 24 of 84,009 labels name a clock time (C906).
7. **A repeatable names a weekday only where a weekday condition makes it true** (C903): "Saturdays" inside a Saturday group is fine; "See you Monday" on a screen any day reaches is not. *LO's choice;* CoT names a weekday 1.43 times per 10,000 words.
8. **The clock repeats** (C890): a weekly bill, a weekly count, not a deadline. *LO's choice, stated.*
9. **Different hours on different days are one row with a group** (L167): never one row per day kind. Out of hours it greys once, with `show_when_blocked` and a `cooldown_message` that names the full hours. *The failure:* P10's six café rows, and the weekday row greyed beside the live weekend one, so each button showed twice.

## Worked example

Roles: the café owner. LO approved these words, with the name swapped for a role.

**Café**
> A narrow café across from campus: six tables, a chalkboard menu, a coffee machine that screams. Students camp here with laptops. A sign by the door says it's open between 7am and 9pm.

Presence, from his rows: "The owner's behind the counter, wiping the same spot."

Buttons: Buy a coffee ($3) · Ask about the Help Wanted sign (once) · Walk to the quad. The coffee still takes 10 minutes and the walk is free (a hop inside the area, C920); the labels say neither.

Closed, seen from the street: "Café", dimmed, "Opens at 7am".

**One row, two kinds of day** (rule 9). Roles: the café, its manager. The hours are filler.
- Button: "Work an hour" (it costs 60 minutes and 10 energy; the label says neither). Weekdays 7am–9pm, weekends 10am–9pm. Out of hours it shows once, greyed: "Work an hour — The manager's behind the counter weekdays from 7am, weekends from 10am."

```toml
[canvases.trigger]
show_when_blocked = true
cooldown_message = "The manager's behind the counter weekdays from 7am, weekends from 10am."

[canvases.trigger.conditions]
version = "1.0"
logic = "AND"
items = [
  { type = "flag", subject = "player", flag_key = "<hired flag>", operator = "is_true" },
  { type = "group", logic = "OR", items = [
    { type = "group", logic = "AND", items = [{ type = "weekday", weekdays = [0, 1, 2, 3, 4] },
                                              { type = "time_of_day", start_time = "07:00", end_time = "21:00" }] },
    { type = "group", logic = "AND", items = [{ type = "weekday", weekdays = [5, 6] },
                                              { type = "time_of_day", start_time = "10:00", end_time = "21:00" }] } ] },
]
```

Before she's hired the flag shuts it and it hides; once hired, only the clock can shut it, so it greys. Its sheet row: "weekdays 07:00–21:00 / weekends 10:00–21:00".

## Not this

- "It's nine in the morning and the café is quiet." A repeatable screen shows at any minute of its window (C900, C902).
- "Work till close." The engine only adds minutes. Write "Work a shift", with its 4 hours in the costs (C889, C926).
- A label that prints its own time or energy: "Eat something (20 min, +15 energy)" (C910, C929; LO, 2026-11-24). The clock and the energy bar show the spend.
- A shut place that just disappears. It stays, dimmed, with when it opens (C913, C930).
- One row per kind of day for the same activity: a weekday "Work an hour" greyed on Saturday beside the live Saturday one (L167). One row, a group.
