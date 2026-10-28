# Way-up audit — First Term, iteration 002

> Written 2026-10-13, after LO's play to day 4 (Corruption 0, Exhibitionism 3). Read-only: nothing in the game
> was changed. Source: the new gate **every stage has a way up** (`gates.py`, `the-arc.md` A4d), run on
> `toml_phases/7_final_game.toml` as built, and checked against a hand count of all 36 Corruption raises.
> The rule it applies is DECISIONS 78: only her choice pays; every stage needs acts that pay.

## How to read it

- **Pays sober:** a repeatable act whose exit adds to the meter, reachable by a player standing at the stage's
  floor with every other meter at 0, with no drink's boost. The requirement is read through the trigger, the way
  in from other scenes, and every choice on the path to the exit that pays. A flag or a step counter counts only
  if something reachable at that stage sets it. Each is counted once a day.
- **Only while a drink's boost is on:** opens only with Tipsy's +20 (3 hours). Its raise is kept, but it isn't a
  way up.
- **Needs another meter first:** pays on this meter at this stage, but needs the other meter above 0 as well.
- **Days** is 20 points ÷ the daily points, a floor; clothes, hours, NPC numbers and energy all make it slower.

## Corruption

| stage | pays sober (a day) | days | the acts | only with a drink | needs Exhibitionism first |
|---|---|---|---|---|---|
| Good Girl 0–19 | **0** | **never** | — | park couple (+1, +2), touch in bed, shower, toilet (+1 each) | — |
| Curious 20–39 | 5 | about 4 | park couple +2, touch bed/shower/toilet +1 | desk guy, party hookup | Ryan 3, Ryan 5 |
| Bold 40–59 | 2 | about 10 | desk guy +1, party hookup +1 | — | Gary's booth, garden sun, Hale 4, Hale's Thursdays, Jake's gym, Laura's kitchen and couch, Ryan's couch, Laura 7, Mark 5, Tom 4 and 6, Zoe 3 |

Bold's "about 10 days" assumes Exhibitionism at 0. Most Bold acts also need Exhibitionism, so with both meters
climbing together, Bold pays more than this.

## Exhibitionism

| stage | pays sober (a day) | days | the acts | one-time here | only with a drink |
|---|---|---|---|---|---|
| Covered 0–19 | 3 | about 7 | park selfie, park run cool-down, the dress-code warning | Laura's blue dress +3, Zoe's first party +3 | the four classes' front-row choices, garden sun, gym, Jake's gym, Zoe's lap |
| Daring 20–39 | 12 | about 2 | the four classes, dress code, garden sun, gym, couch, park run, selfie, toilet mirror, stairs | the art exam +1, Laura's dress +3, Tom 2 +3, Zoe's party +3 | Jake's gym, Zoe's lap, party dare, the two street events, Zoe's park dare |
| Showing 40–59 | 13 | about 2 | as Daring, plus the party dare | as Daring | Jake's gym, Zoe's lap, the two street events, Zoe's park dare |

## What the Quests page promises, beside what pays

| the card says | what pays at that stage |
|---|---|
| Reach Curious: parties, the café, the park, touching yourself | **nothing** |
| Reach Bold: Gary's booth, Zoe's hot tub, his hand under the desk | the women's toilet, the bathroom, her room, the park (Gary's booth and the hot tub need Bold already; the desk guy pays only from 40) |
| Reach Daring: selfies, the couch, the café uniform | the lecture hall, the park (the couch needs Daring already; nothing pays for wearing the uniform) |
| Reach Showing: dares, the park run, the tables at home | campus gym, women's toilet, garden, hall, living room, lecture hall, park (the dares need Showing; the tables at home need Bold) |

## What this says

1. **Corruption has a wall at Good Girl.** Every act that pays is gated at 20, including the park scene's own
   watching screen. The only bridge is a drink, and no card names it.
2. **Exhibitionism at Covered works, but thinly**: about 3 points a day, about a week, plus Laura's dress and
   Zoe's party if the player finds them.
3. **Above stage 1 the climb is fast**: Daring and Showing take about 2 days each, and Curious about 4. The
   difference between stage 1 and the rest is the shape of the problem, not just its size.
4. **All four Quests goal cards name sources that don't pay at the stage they're shown in.**
5. **The ledger's `fed_at` for Corruption** (lecture hall, Zoe's, the café) doesn't match: none of them pays at
   Good Girl, and the café pays nothing at all until Bold.

## Input for step 4 (LO's call)

Under DECISIONS 78, Good Girl needs about 3 sober acts a day, each +1 capped at 19, so the stage takes about a
week like Covered. The candidates already on the table are:
- a linger button on the park couple;
- the existing home accidents (towel, robe), which today raise only the man's number;
- LO's new walk-ins: Mark and Laura in the master bedroom, and Ryan alone in his room;
- Ryan and Kayla through the wall at Good Girl. Today it is only Ryan's step 4, at Curious and Showing.

The goal cards need rewriting to name what pays.
