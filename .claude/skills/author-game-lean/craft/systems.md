# craft/systems.md — energy, daily limits, and the things she repeats

Read this before you write a card that costs or refills energy, caps how often she can do something, or adds an activity she repeats (a run, a workout, study, a shift). Checked against Course of Temptation (CoT) and the top games (LO, relayed 2026-11-23: "confirm system rules files with the top games and CoT"). Each rule says where CoT and the field agree, and where they split. Other files own the rest, and this one doesn't repeat them:
- money, the bill, prices and pay: `craft/economy.md`;
- her climb meters, their caps and pace: `craft/meters.md`;
- the time on a button, and hours: `craft/clock.md`;
- a clothes gate on a button: `craft/clothes.md`;
- a person's once-a-day menu: `craft/people.md` rule 10.

## Must read

The card's `Craft:` line cites each one, or says in one line why it skips it.

| id | what it asks | the failure it stops |
|---|---|---|
| C1446 | a system repeats, has rules, remembers, changes, touches money, body, people or sex, she chooses it, and it has a place or action | — |
| C1386 | a meter lives inside a system: the system writes it and reads it | — |
| C1303 | every need is read by a condition; a refill that gates nothing buys nothing | — |
| C1337 | energy moves both ways and isn't a climb, but it must be read | — |
| C1431 | a need falls, she refills it, and while it's empty something is shut | — |
| C1432 | a need declares what drains it, what refills it (place, activity, minutes), what it costs, and what it shuts | — |
| C1438 | a need decays over time or is spent by use; never neither | — |
| C1342 | each need can be refilled from some room's list, or it is a countdown to a wall | L45 |
| C1433 | an energy-type need shuts a door while empty | — |
| C1434 | an empty need sends her to the refill place, and that place has something happen | — |
| C1313 | a repeatable refill carries a substitution, or its room holds an event | — |
| C1428 | energy is the wrong lock on a person ("too tired to seduce him"), a fine throttle elsewhere | — |
| C1345 | the brake goes on the way in: trigger costs, a cap per day, or a day-cap flag | — |
| C1423 | a gate that's worth something costs something to pass: a cost, a daily cap, or real time | — |
| C1425 | four levers pace a repeat: spacing, a time cost, a daily cap, a resource cost; none works alone | — |
| C1427 | a time cost bites only when sized against the window it sits in | — |
| C1360 | a locked choice shows greyed with its action as the label; a number lock lets the engine print the need | — |
| C1421 | when something's out of reach, the requirement is told | — |
| C1441 | a number-only result is for work (a shift); a step about a person or her body gets a scene | — |
| C1369 | every live system is armed in the first hour, or sits readable on the sidebar | — |
| C1403 | players mind grind in jobs and money, not a slow sexual climb | L80 |

## The engine (cited; `v2.py` is `apps/game_generation/twee_comprehensive/generators/v2.py`)

- **Energy is a player trait.** Nothing in the engine treats it specially (a grep of v2.py for `'energy'` finds nothing), so it falls only by costs and effects, and fills only by effects. Effects clamp at its range when `clamp = true`.
- **A cost goes on the trigger:** `costs = [{ trait = "energy", value = 15 }]`, parsed at `apps/projects/services/template_import.py:2593` and taken on entry (`setup.deductCostArray`, v2.py:6168-6175).
- **Too little energy greys the row, with its cost.** `setup.checkCostsAffordable` (v2.py:6138-6148) puts the row in the blocked list (v2.py:6706-6707). It's drawn dimmed with "(15 Energy)" (v2.py:6724-6738), and a click says "Requires 15 Energy (you have 6)" (`setup.getCostBlockedMessage`, v2.py:6183-6197).
- **A cap per day** is `max_triggers_per_day` on the trigger (read at v2.py:15066), checked by `setup.canTriggerActivity` (v2.py:5590). A capped row is hidden, or greyed with its `cooldown_message` when `show_when_blocked = true` (v2.py:6700-6703).
- **A cap on one choice** inside a screen is a `_today` flag set by the choice and checked by it, cleared by `[engine.daily_tick]` (v2.py:7162-7164; `.claude/skills/author-game-v2/references/engine.md:1458-1485`).
- **The day turns at midnight.** The hour wraps past 24 (v2.py:7021-7022) and the weekday moves on (v2.py:7058-7060). The cap's day key is week and day (`setup.getCurrentDayKey`, v2.py:5426-5433), so every cap resets at midnight, not at sleep.
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
4. **Every repeat button shows its cost: time and energy, and money when it's a spend** (C1427; `craft/clock.md`; `craft/economy.md`). The cost is sized against the window: a 60-minute shift in a 4-hour opening can run 4 times; a 5-minute act in an all-day window is farmable. *CoT and the field agree:* CoT's buttons print `<<dtime>>` and `<<dalterneed>>`. *Measured.*
5. **The brake goes on the way in** (C1345, C1423, C1425). Pick one per activity, and name it on the card:
   - **by the need:** greyed by energy, as rule 2;
   - **by a count:** `max_triggers_per_day` with `show_when_blocked` and a `cooldown_message` in her voice ("You're not hungry right now.");
   - **by a choice's flag:** a `_today` flag for one option inside a screen.
   
   Every count resets at midnight. *CoT and the field split:* CoT limits eating by the need and the raise by a day stamp; SD by actions per day. Counts are *LO's choice* here (eat 3 a day, talk once a day), because there's one need, not thirteen.
6. **A repeated activity has six parts on its card:**
   - where and when;
   - how long;
   - what it costs;
   - what it gives;
   - its gate (clothes `craft/clothes.md`, money `craft/economy.md`), shown greyed with the reason;
   - what shows after: a scene for a body or a person, a number line only for work (C1441).
   
   The first time is its own scene, before the plain repeat. *CoT and the field agree:* CoT's gym (20 min, Rest and Hygiene) and its first shift; the field's job card. *Measured.*
7. **Every system links to at least one other, and to people or sex** (C1446, C1386, C1303, C1337). Energy is read by every cost. The workout drains energy and sends her to the shower. A shift pays toward the bill. What a system raises is read somewhere, or it's cut. *CoT and the field agree:* median 6–11 links; CoT's gym drains Hygiene into the co-ed shower. *Measured.* While release 1's meters are still, an activity links to a need, money or a flag, never to a meter (`craft/meters.md`).
8. **Energy throttles work and body care, never a person** (C1428). No "too tired to talk to her". A person's menu is capped by its own once-a-day flag (`craft/people.md`). *LO's rule, not measured.*
9. **Open it on day 1, at its bottom rung,** and arm it in the first hour or show it on the sidebar (C1369). *CoT and the field agree:* 16 of 19 CoT systems are usable on day 1; 79–87% across four games. *Measured.*
10. **Keep the job short of grind** (C1403). Grind complaints are about jobs and money; needs cause only 6 of 242. A shift pays enough that the first bill is reachable working clean (`craft/economy.md` rule 9). *Measured in the field.*

## Worked example

Roles, not a world: her bedroom, the kitchen, the park, the café. The numbers show the shape and are filler (C992); the game's own come from its plan.

**Kitchen: eat, capped by count**
- Button: "Eat something (20 min, +15 energy)". Three a day; after the third, greyed: "Eat something — You're not hungry right now."

```toml
[canvases.trigger]
max_triggers_per_day = 3
show_when_blocked = true
cooldown_message = "You're not hungry right now."
```

**Her bedroom: the refill, never capped**
- Button: "Sleep (8 hours)", which fills energy to the top. No cost, so it's always there.

**Park: a run, a repeat with a clothes gate**
- Button: "Go for a run (45 min, −15 energy)". Without her running clothes it greys: "Go for a run — Needs leggings and a sports top" (`craft/clothes.md`). With energy under 15 it greys with "(15 Energy)".
- The first run is its own scene: her body, her breath, someone on the path. After that, one short line per run from a pool, and she comes home needing a shower.

**Café: a shift, energy and pay**
- Button: "Work a shift (4 hours, −30 energy)". The pay is said in the scene that offered the job, never on the button (`craft/economy.md`). After a shift, one number line: what she earned. With energy under 30, it greys with "(30 Energy)", and a click says "Requires 30 Energy (you have 12)".

What links: the run and the shift drain energy, and the kitchen and the bed refill it, where the family is. The run sends her to the shower, and the shower has the walk-in. The shift pays the Sunday bill.

## Not this

- "You're too tired to talk to her." Energy throttles work and body care, never a person (C1428).
- A need with no refill she can reach. It's a countdown to a wall (C1342; L45).
- A button that just vanishes when she's short. It greys with its cost or its reason (C1421).
- An activity that raises a number nothing reads (C1303).
- A 5-minute repeat in an all-day window with no cap. It's farmable (C1427, C1345).
- An activity that leads nowhere: no person, no place where something happens, no bill (rule 7).
