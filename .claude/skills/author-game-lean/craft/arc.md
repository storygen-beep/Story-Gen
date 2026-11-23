# craft/arc.md — one person's story, from meeting to where it stops

Read this before you plan a person's steps or write a card for one of them. Checked against Course of Temptation (CoT) and the top games (LO, relayed 2026-11-23: "Confirm it with top games and CoT."). Each rule says where CoT and the field agree, and where they split. Other files own the rest, and this one doesn't repeat them:
- the first meeting, and how a person talks after: `craft/people.md`;
- her goal card: `craft/want.md`;
- how hot each step is: `craft/heat.md`;
- what a meter pays: `craft/meters.md`;
- a person's repeat menu: `craft/people.md` rule 10.

## Must read

The card's `Craft:` line cites each one, or says in one line why it skips it. `when` and `judge` are the labels in `SKILL.md`, "Rule labels".

| id | what it asks | the failure it stops | when | judge |
|---|---|---|---|---|
| C180 | every step pays the one before and opens the one after, and the text says so | P13 reader pass 6: Ryan's step ended on "He says it to the floor." and opened nothing after it | a one-time step | reader |
| C160 | central people get a long chain, the rest shorter: a shape, not a quota | — | the plan | note |
| C120 | every step adds a new witness, risk or kind of yes; two flat steps in a row, cut one | L18 | a one-time step | reader |
| C109 | each step carries a leak (his want, shown before) and a promise (the line it ends on) | P13's Ryan leered and never covered (`craft/opening.md`, C601) | a one-time step | reader |
| C115 | his move: what he wants for his own reason, shown before, and what he does about it | — | a one-time step | note |
| C162 | information the player earns is a step; information the game narrates is exposition | — | a one-time step | note |
| C146 | a big moment is a one-time step, not a repeatable | — | a one-time step, a repeatable | note |
| C151 | the repeatable stays short: one spoken line and one visible want | — | a repeatable | note |
| C148 | each scene goes one step further than the last | — | a one-time step | note |
| C149 | each scene points at what comes next | P13 reader pass 6: Ryan's scene didn't point at what comes next with him | a scene's last screen | reader |
| C198 | an arc runs on one step counter, not a pile of flags | — | the plan | note |
| C131 | every dependency is written down: another person's step, a window, a place | — | the plan | note |
| C174 | a person's next arc step comes before any dice | — | the plan | note |
| C212 | a story step fires the first time it can, never by luck | — | the plan | note |
| C124 | slow is fine if his card says what to do; bored is fine, lost is not | L80 | a goal card is shown | reader |
| C164 | an ordinary no is parked: the step comes back after a wait | — · kept blocking: LO's choice (2026-11-24) | a one-time step | reader |
| C165 | a final no is only on a button that says so, and closes his story, not the person | — · kept blocking: LO's choice (2026-11-24) | a one-time step | reader |
| C166 | never a final no on the main arc's first step, or in the opening | P13's "(ends his path)" | a one-time step, the opening | reader |
| C121 | the release's top step is a payoff; a talk or a locked door is not a top step | L18 | the plan | reader |
| C127 | something still happens after the top step | — | the plan | note |
| C140 | each arc's last card says where it stops and what comes next, and it's true | — | a goal card is shown | note |
| C215 | an arc that stops at the build's edge says so on its card ("for now"), never "Arc complete" | — | a goal card is shown | note |
| C217 | a step's ✓ reads a flag the step sets on its way out | P13 reader pass 6: goal 1's ✅ read met_mark, set on the way into the rent screen, not on the step's way out | a goal card is shown | reader |
| C171 | an arc ends by pointing at another | — | the plan | note |

## The engine (cited; `v2.py` is `apps/game_generation/twee_comprehensive/generators/v2.py`)

- **A step is a one-time canvas.** A canvas is repeatable unless it says `is_repeatable = false` (read at v2.py:15065; `apps/projects/services/template_import.py:833`).
- **What opens the next step** is the step's own conditions: the last step's flag, a window, money, a meter. A gap in days is a `days_since_flag` condition, counted from the day the flag was set (v2.py:5167-5180).
- **The no:** `consume_on = "exit"` on a one-time step uses it up only on the yes (`consumes`). A warned no (`final`) closes it and sets `<canvas>_closed`. A `retry_after_days` choice parks it for N days, and leaving mid-scene parks it for 1 (v2.py:5436-5445; `apps/projects/services/template_import.py:924-931`).
- **The card's end:** a quest card with `terminal = true` reads "Arc complete" unless `terminal_text` says otherwise (v2.py:19970-19974; `apps/projects/services/template_import.py:1405-1411`). An arc that stops at the build's edge sets `terminal_text`.

## The measures

CoT's quest log (`setup.storyhints.db`, in `~/Documents/Process_Review_20260925/round1_evidence/scripts/_cot_js.txt`), read 2026-11-23:
- **The first hint names a place and an hour:** "Hang out in <<pp 'The Best Friend'>> dorm room in the evening." (line 83664).
- **A wait always comes with something to do:** "Wait for a favor to be called in, or go to the quad party on Hanna Road South on Friday night." (line 83665).
- **The last hint is open, not "complete":** "A line was crossed. What you make of it now is up to you." (line 83669). The story-hint page ends a line with "You have reached the end of this storyline... for now! But there may still be recurring events." (`StoryHintWidgets.txt`, line 123, in the CoT corpus).

The field: `~/Documents/Great_Games_Study_20260926/ARC_CRAFT_STUDY.md` (CoT, In Her Own Hands (IHOH), Cupid's Way (CW), Shady Deals (SD); 22 arcs, one row per step in `arc_study/p2_*.md`). Ten of its cites were re-opened today in `round2/passages`, and each says what the study says:
- CoT 43682 and 45271 (the harasser's scholarship, used again later);
- CoT 65940 (the milkshake step's 25% roll);
- CoT 43690 (a filler step);
- IHOH 9556 (Shaun says where and when he's alone);
- IHOH 5667 and 15597 (the talks after a first);
- IHOH 12219 (a step gated on using the repeatable);
- CW 1231 ("why don't you move in with me?", after first sex).

What the field found:
- **Steps.** Central arcs run 7–18 steps with 3–8 firsts; side arcs 4–6 (§2.1, §2.4).
- **Length is four kinds of step** (§2.2): new firsts, information the player uses later, a talk after a big first, and an ask before a date. The rest is bridge: repeat pools, filler, and waits on a day floor, a meter or dice.
- **Players.** Drag complaints outnumber "too fast" about 30 to 1 on mopoga (§1). Stuck is the biggest code: CoT 236 of 411 comments about a person (§3, Q6).
- **Pace.** Central arcs reach their repeatable around day 20–55. The clock type sets the days, not the step count (§2.3).
- **The opening without sex** is 0–85% of an arc's steps, median 43% (§2.1).
- **After the sex.** "once you slept with one, the story seemed to completely stop with that guy" is the strongest F95 pattern, in all four games (§3, Q7).

## The shape

Each rule says what CoT and the field do, then whether it's **measured** or **LO's choice**.

1. **Count the steps from what's in them.** Count the firsts, plus the information she'll use later, plus a talk after each big first, plus an ask before each date. Central people come to about 7–18, side people 4–6 (C160). A step that only waits is a bridge: cut it, or give it something new. *CoT and the field agree:* CoT's best friend 7 or 8, the harasser 11 or 7, the roommate's partner 12; IHOH 5–14; CW 9–18; SD 4–8. *Measured.* COVERAGE's C156 says "the first third has no sex"; the field's median is 43%, ranging from 0% to 85%, so this file doesn't use it.
2. **Each step is one one-time scene you can tell apart in one line by what's new in it** (C120, C146, C148). Step 1 shows his want first, for his own reason (C109, C115). Each step pays the one before in the text and ends on a promise (C180, C149). *CoT and the field agree* (the study's Q1, Q3, Q5, all strong). *Measured.*
3. **What opens the next step:** the last step's flag, plus at most one more thing. That's a window where he is, a gap of days (`days_since_flag`), money, or her meter stage. Write each one on the card (C131, C198). The step fires the first time it can, before any dice (C174, C212). *CoT and the field split:* CoT itself uses dice (the milkshake's 25% a Friday) and a day floor (the roommate's partner after day 90), and those are exactly where its players say "making this take months". IHOH runs on a weekly grid, and CW on 1–2-day gaps. This file follows the players: no dice, and no bare day floor. *Measured* (players and games).
4. **Between steps, she does something with them.** Their own menu (`craft/people.md` rule 10), or a place they share, so the wait is play, not a timer (C124). *CoT and the field agree:* CoT's first hint is "Hang out in … dorm room in the evening."; the field's good case is IHOH's Shaun telling her he's in the kitchen at 2 a.m. after the club. *Measured.*
5. **The card says what's next, as a place and a time, in one line.** A wait always comes with something to do (C124, C149; the card's shape is `craft/want.md`). *CoT and the field agree:* "Wait for a favor to be called in, or go to the quad party … on Friday night."; stuck is the field's biggest complaint. *Measured.*
6. **Pace is set by the clock, not by the step count.** Most gaps are 1–4 days; a missed weekly slot costs 7. A central arc reaches its repeat around day 20–55. Write the days on the plan's arc table. *The field, measured* (CoT has no single clock).
7. **The no parks; a final no says so on its button** (C164, C165). There's no final no on a central arc's first step (C166). In the engine: `consume_on = "exit"` with `retry_after_days`, or `final`. *Measured in the field;* the first-step rule is *LO's choice.*
8. **Where it stops in a release:** on a payoff, not a talk or a locked door (C121, L18). The last card says it stops "for now" and what she can keep doing (C140, C215), and its ✓ reads the flag the last step sets (C217). *CoT and the field agree:* CoT's "for now!… there may still be recurring events". *Measured.*
9. **It doesn't die after the sex** (C127). Something still happens after the first sex, or after "boyfriend": a move, a rule, a new person, a cost. The arc can also hand over to another (C171). *CoT and the field agree* (Q7, strong; CW's Connor asks her to move in after first sex). *Measured.*
10. **Information she earns is a step; what's only narrated isn't** (C162). The harasser's scholarship comes back as his weak spot at the end. *CoT, measured;* the field's info steps agree.

Release 1, the skeleton, builds each person's first meeting only (`plan.md` §10). The plan holds only the arc's scaffold: its shape, direction and ending (`plan.md` §9). Each release designs its own steps in its pieces, never all at once (L91). The meeting's promise points at the arc's direction; step 2 is designed in the release that builds it.

## Worked example

Roles, not a world: a housemate's central arc. This is the table a release's pieces fill in, a few steps at a time; it is not written all at once in the plan (L91). Release 1 builds step 1. The steps show the shape and are filler.

| step | what's new (one line) | kind | opens when | the card says next |
|---|---|---|---|---|
| 1 | he looks one second too long in the hall, and catches himself | his want, shown | the opening | "He's in the kitchen most mornings before eight." |
| 2 | he says why he's home so much: he lost his job | info she'll use | step 1, and 2 days | "Keep him company in the kitchen in the morning." |
| 3 | she catches him with her underwear from the laundry | a first (seen) | step 2, and he's in his room at night | "His door's open at night." |
| 4 | the talk after: he asks her not to tell | a talk after a first | step 3, the next morning | "He's waiting for you in the kitchen." |
| … | … | … | … | … |
| top of release N | a payoff on the body | a first | its flag | "That's as far as this goes for now. He's still in the kitchen most mornings." |

Between steps, his menu in the kitchen is open every morning (`craft/people.md` rule 10). The table has no dice and no "after N days" with nothing to do.

## Not this

- A step that only waits: "after 7 days he texts you", with nothing to do until then (rule 3).
- The next step on a 25% roll (C212).
- A card that says "Keep talking to him" with no place or time (rule 5).
- The release's last step as a talk or a locked door (C121; L18).
- "Arc complete" on an arc that only stopped at the build's edge (C215).
- "Now she can do it whenever she likes", and nothing after (C127).
