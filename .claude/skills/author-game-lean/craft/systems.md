# craft/systems.md — energy, daily limits, and the things she repeats

Read this before you write a card that costs or refills energy, caps how often she can do something, or adds an activity she repeats (a run, a workout, study, a shift). Checked against Course of Temptation (CoT) and the top games (LO, relayed 2026-11-23: "confirm system rules files with the top games and CoT"). Each rule says where CoT and the field agree, and where they split. Other files own the rest, and this one doesn't repeat them:
- money, the bill, prices and pay: `craft/economy.md`;
- her climb meters, their caps and pace: `craft/meters.md`;
- the time on a button, and hours: `craft/clock.md`;
- a clothes gate on a button: `craft/clothes.md`;
- a person's once-a-day menu: `craft/people.md` rule 10.

## Must read

On a card with a `Does:` block (every card from 2026-11-24 on), the rows that apply come from `check.py --rules`, which lists each with its craft file; the card has no `Craft:` line (`piece.md` step 2). On a card from before 2026-11-24, the `Craft:` line cites each one, or says in one line why it skips it. `when` and `judge` are the labels in `SKILL.md`, "Rule labels".

| id | what it asks | the failure it stops | when | judge |
|---|---|---|---|---|
| C1446 | a system repeats, has rules, remembers, changes, touches money, body, people or sex, she chooses it, and it has a place or action | — | the plan | note |
| L166 | a repeat activity is open whenever its place is open and its people are there; fixed times only when it really happens at a time, said on the card; never placed around another activity to avoid a clash | first_term_lean P10: café shifts locked to weekdays at 2pm, after the 9–1 lectures, and weekends at 10am and 3pm | a repeatable | reader |
| C1386 | a meter lives inside a system: the system writes it and reads it | — | the plan | note |
| C1303 | every need is read by a condition; a refill that gates nothing buys nothing | — | a repeatable | note |
| C1337 | energy moves both ways and isn't a climb, but it must be read | — | a repeatable | note |
| C1431 | a need falls, she refills it, and while it's empty something is shut | — · kept blocking: LO's choice (2026-11-24) | a repeatable | reader |
| C1432 | a need declares what drains it, what refills it (place, activity, minutes), what it costs, and what it shuts | — · kept blocking: LO's choice (2026-11-24) | a repeatable | reader |
| C1438 | a need decays over time or is spent by use; never neither | — · kept blocking: LO's choice (2026-11-24) | a repeatable | reader |
| C1342 | each need can be refilled from some room's list, or it is a countdown to a wall | L45 | a repeatable | reader |
| C1433 | an energy-type need shuts a door while empty | — | a repeatable | note |
| C1434 | an empty need sends her to the refill place, and that place has something happen | — | a repeatable | note |
| C1313 | a repeatable refill carries a substitution, or its room holds an event | — | a repeatable | note |
| C1428 | energy is the wrong lock on a person ("too tired to seduce him"), a fine throttle elsewhere | — · kept blocking: LO's rule (2026-11-23) | a repeatable | reader |
| C1345 | the brake goes on the way in: trigger costs, a cap per day, or a day-cap flag | — | a repeatable | note |
| C1423 | a gate that's worth something costs something to pass: a cost, a daily cap, or real time | — | a repeatable | note |
| C1425 | four levers pace a repeat: spacing, a time cost, a daily cap, a resource cost; none works alone | — | a repeatable | note |
| C1427 | a time cost bites only when sized against the window it sits in | — | a repeatable | note |
| C1360 | a locked choice shows greyed with its action as the label; a number lock lets the engine print the need | — | a repeatable | note |
| C1421 | when something's out of reach, the requirement is told | — | a repeatable | note |
| C1441 | a number-only result is for work (a shift); a step about a person or her body gets a scene | — | a repeatable | note |
| C1369 | every live system is armed in the first hour, or sits readable on the sidebar | — | the plan | note |
| C1403 | players mind grind in jobs and money, not a slow sexual climb | L80 | the plan | reader |
| C2199 | a page she is given in the story (her timetable) is not in the sidebar before she has it: the scene that gives it opens it (a `type = "timetable"` block, `open = true`), and the sidebar button waits on the flag that scene sets (`[ui] timetable_button_when`) | first_term_lean: the Timetable button sat in the sidebar from the first minute, and the dean who hands her the timetable printed it as a paragraph. LO, typed in main-lean 2026-11-26: "Timetable is only in the sidebar / Should first open in the deans office", then "Go ahead" | the plan | reader |

## The engine (cited; `v2.py` is `apps/game_generation/twee_comprehensive/generators/v2.py`)

- **Energy is a player trait.** Nothing in the engine treats it specially (a grep of v2.py for `'energy'` finds nothing), so it falls only by costs and effects, and fills only by effects. Effects clamp at its range when `clamp = true`.
- **A cost goes on the trigger:** `costs = [{ trait = "energy", value = 15 }]`, parsed at `apps/projects/services/template_import.py:2593` and taken on entry (`setup.deductCostArray`, v2.py:6188-6195).
- **Too little energy greys the row, with its cost.** `setup.checkCostsAffordable` (v2.py:6158-6168) puts the row in the blocked list (v2.py:6726-6727). It's drawn dimmed with "(15 Energy)" (v2.py:6744-6758), and a click says "Requires 15 Energy (you have 6)" (`setup.getCostBlockedMessage`, v2.py:6203-6217).
- **A cap per day** is `max_triggers_per_day` on the trigger (read at v2.py:15086), checked by `setup.canTriggerActivity` (v2.py:5609). A capped row is hidden, or greyed with its `cooldown_message` when `show_when_blocked = true` (v2.py:6720-6723).
- **A cap on one choice** inside a screen is a `_today` flag set by the choice and checked by it, cleared by `[engine.daily_tick]` (v2.py:7182-7184; `.claude/skills/author-game-v2/references/engine.md:1458-1485`).
- **The day turns at midnight.** The hour wraps past 24 (v2.py:7041-7042) and the weekday moves on (v2.py:7078-7080). The cap's day key is week and day (`setup.getCurrentDayKey`, v2.py:5445-5452), so every cap resets at midnight, not at sleep.
- **A gate that waiting can't open** (clothes, money, a flag) greys with `locked_text` (`craft/clothes.md`).

## The measures

CoT, read 2026-11-23 (`/Users/a0000/Documents/Player_Legibility_Study_20260825/corpus/course-of-temptation/passages`):
- **A job button shows its cost.** QuickieBurger's "Work" is `<<dtime 60>> <<dalterneed Rest _rest>>`, with `_rest` = −20 (`QuickieBurger.txt`, lines 3 and 8-23).
- **The floor says why, in her voice.** With a need too low: "You really don't feel like working." (`QuickieBurger.txt`, line 6). The same shape appears for recording (3) and streaming (2).
- **A workout costs time and two needs.** `BlodgettGymInterior.txt`: yoga is 20 min, Rest −30, Hygiene −50, Relaxation +20 (line 34); cardio is 20 min, Rest −30, Hygiene −50 (line 43); weights are 20 min, Rest −40, Hygiene −40 (line 52). Each shows its costs on the button.
- **Eating is limited by the need, not by a count.** "You really aren't that hungry right now." (`ChamberlainHallInterior.txt`, line 20; also `SummitMarketInterior.txt`).
- **Once a day, by a day stamp.** A raise checks `$quickieburgerjob.lastdayworked isnot $gameday` (`QuickieBurger.txt`, line 18). A person's menu has 14 of its 38 links checked against `$interactionstoday` (`craft/people.md`).
- **A first time is its own scene:** "QuickieBurgerFirstShift" before the plain shift (`QuickieBurger.txt`, lines 15-17).

The field, from `~/Documents/Great_Games_Study_20260926/` (not re-run today):
- `round8/ROUND8_REPORT.md` §2.5: needs are in 14 of 15 core games and 65% of 88 games. IHOH has a 150-point energy bar, with jobs at −10 an hour. SD gives 6 actions a day. CoT has 13 needs that drain over 20–36 hours. Needs exist "to route her into public or social spaces where events fire".
- `round9b/ROUND9B_REPORT.md` §2.6: at 0, 5 of CoT's needs block work. Refill places always roll an event. Needs cause bugs (stuck sleep loops), not grind: 6 of 242 grind complaints name needs.
- `round9b` §2.1: a job costs time and one need (CoT 60 min, Rest −20; IHOH −10 energy an hour).
- `round9b` §3: every system links to others, a median of 11 in CoT and 6–10 in IHOH and SD. A system that leads to neither sex nor people is a weak one.
- `round9b` §4: 79–87% of systems are usable on day 1 at their bottom rung.
- `round8` key point 6: grind is the #1 complaint (242).

## The shape

Each rule says what CoT and the field do, then whether it's **measured** or **LO's choice**.

1. **Each need is declared in full: what drains it, what refills it, what it costs, what it shuts** (C1431, C1432, C1438). A need is spent by use (energy here) or decays over time; it is never neither. *CoT and the field split:* CoT's needs decay by the hour (20–36 h); IHOH's energy and SD's actions are spent. Spent is *LO's choice* for energy, because the engine moves it only by costs and effects.
2. **Empty shuts work, says why, and never strands her** (C1433, C1342, C1421). A row she can't afford greys with its cost, and a click says what's needed. Her refill (sleep) costs nothing, so it's always open. *CoT and the field agree:* CoT's "You really don't feel like working."; 5 of CoT's needs block work. *Measured;* L45 is the stranded failure.
3. **The refill sends her somewhere something happens** (C1434, C1313). The kitchen has the family; the shower has the walk-in. *CoT and the field agree:* CoT's code says so, and its refill places always roll an event. *Measured.*
4. **Every repeat has a real cost, sized against its window, and its button shows only money, when it's a spend** (C1427; `craft/clock.md`; `craft/economy.md`): never time or energy. A 60-minute shift in a 4-hour opening can run 4 times; a 5-minute act in an all-day window is farmable. The clock and the energy bar show the spend, and a greyed row shows the engine's "(15 Energy)". *Measured:* CoT and the field print the cost on the button (`<<dtime>>`, `<<dalterneed>>`). Leaving time and energy off is *LO's choice* (LO, 2026-11-24: "Beside choice i dont want to show time and energy show money if needed"; "Room buttons too").
5. **The brake goes on the way in** (C1345, C1423, C1425). Pick one per activity, and name it on the card:
   - **by the need:** greyed by energy, as rule 2;
   - **by a count:** `max_triggers_per_day` with `show_when_blocked` and a `cooldown_message` in her voice ("You're not hungry right now.");
   - **by a choice's flag:** a `_today` flag for one option inside a screen.
   
   Every count resets at midnight. *CoT and the field split:* CoT limits eating by the need and the raise by a day stamp; SD by actions per day. Counts are *LO's choice* here (eat 3 a day, talk once a day), because there's one need, not thirteen.
6. **A repeated activity has six parts on its card:**
   - where and when (when is whenever the place is open and its people are there, rule 7);
   - how long;
   - what it costs;
   - what it gives;
   - its gate (clothes `craft/clothes.md`, money `craft/economy.md`), shown greyed with the reason;
   - what shows after: a scene for a body or a person, a number line only for work (C1441).
   
   The first time is its own scene, before the plain repeat. *CoT and the field agree:* CoT's gym (20 min, Rest and Hygiene) and its first shift; the field's job card. *Measured.*
7. **A repeat activity is open whenever its place is open and its people are there** (L166, C1446: she chooses it). Fixed times only when the activity really happens at a time (a class, a party), and the card says why. Never place one activity around another to avoid a clash; when two compete for the same hours, that's the player's choice. Different hours on different days are one row with a `group` condition (`craft/clock.md` rule 9; L167). *Measured in CoT:* QuickieBurger's "Work" link checks that she holds the job, her need, and how she looks (the dress code, being cleaned up), and no hour; each click is one hour (`<<dtime 60>>`), and only her need stops it ("You really don't feel like working.") (`QuickieBurger.txt`, lines 4-30). Classes do run at their times: `setup.School.current_class` builds each block's day, hour and length and marks her early or late; she attends by being at the class's place in its block (`setup.School.is_pc_at_class`), and attendance is counted per course (`$classesattended`, in `setup.School.attend_class`) (`~/Documents/Process_Review_20260925/round1_evidence/scripts/_cot_js.txt`, lines 126098-126104, 126175-126181, 126249-126264). She attends by going; nothing makes her go. The failure: first_term_lean's café shifts (P10) were set at weekdays 2pm, after the lectures, and weekends at 10am and 3pm.
8. **Every system links to at least one other, and to people or sex** (C1446, C1386, C1303, C1337). Energy is read by every cost. The workout drains energy and sends her to the shower. A shift pays toward the bill. What a system raises is read somewhere, or it's cut. *CoT and the field agree:* median 6–11 links; CoT's gym drains Hygiene into the co-ed shower. *Measured.* While release 1's meters are still, an activity links to a need, money or a flag, never to a meter (`craft/meters.md`).
9. **Energy throttles work and body care, never a person** (C1428). No "too tired to talk to her". A person's menu is capped by its own once-a-day flag (`craft/people.md`). *LO's rule, not measured.*
10. **Open it on day 1, at its bottom rung,** and arm it in the first hour or show it on the sidebar (C1369). *CoT and the field agree:* 16 of 19 CoT systems are usable on day 1; 79–87% across four games. *Measured.*
11. **Keep the job short of grind** (C1403). Grind complaints are about jobs and money; needs cause only 6 of 242. A shift pays enough that the first bill is reachable working clean (`craft/economy.md` rule 9). *Measured in the field.*

- **Her timetable, given in a scene.** A content block `{ type = "timetable", props = { label = "<link text>", open = true } }` draws a link that opens the Timetable dialog (`setup.openTimetable`), and with `open = true` the dialog also opens by itself once the screen shows (v2.py `_convert_blocks_to_game_html`, the `timetable` branch). `[ui] timetable_button_when = "<flag>"` puts the sidebar button behind that player flag (the `TimetableWidgets` passage). The importer refuses a timetable block in a game with no `[[ui.timetable]]` rows, and a `timetable_button_when` without `timetable_button = true` (`apps/projects/services/template_import.py`, `_validate_timetable`). (C2199)

## Worked example

Roles, not a world: her bedroom, the kitchen, the park, the café. The numbers show the shape and are filler (C992); the game's own come from its plan.

**Kitchen: eat, capped by count**
- Button: "Eat something" (20 minutes, +15 energy, neither on the label). Three a day; after the third, greyed: "Eat something — You're not hungry right now."

```toml
[canvases.trigger]
max_triggers_per_day = 3
show_when_blocked = true
cooldown_message = "You're not hungry right now."
```

**Her bedroom: the refill, never capped**
- Button: "Sleep" (8 hours), which fills energy to the top. No cost, so it's always there.

**Park: a run, a repeat with a clothes gate**
- Button: "Go for a run" (45 minutes, −15 energy, neither on the label). Without her running clothes it greys: "Go for a run — Needs leggings and a sports top" (`craft/clothes.md`). With energy under 15 it greys with "(15 Energy)".
- The first run is its own scene: her body, her breath, someone on the path. After that, one short line per run from a pool, and she comes home needing a shower.

**Café: a shift, energy and pay**
- Button: "Work a shift" (4 hours, −30 energy, neither on the label), open whenever the café is open and the manager is there, not at a set hour (rule 7). The pay is said in the scene that offered the job, never on the button (`craft/economy.md`). After a shift, one number line: what she earned. With energy under 30, it greys with "(30 Energy)", and a click says "Requires 30 Energy (you have 12)".

What links: the run and the shift drain energy, and the kitchen and the bed refill it, where the family is. The run sends her to the shower, and the shower has the walk-in. The shift pays the Sunday bill.

## Not this

- "You're too tired to talk to her." Energy throttles work and body care, never a person (C1428).
- A need with no refill she can reach. It's a countdown to a wall (C1342; L45).
- A button that just vanishes when she's short. It greys with its cost or its reason (C1421).
- An activity that raises a number nothing reads (C1303).
- A 5-minute repeat in an all-day window with no cap. It's farmable (C1427, C1345).
- An activity that leads nowhere: no person, no place where something happens, no bill (rule 8).
