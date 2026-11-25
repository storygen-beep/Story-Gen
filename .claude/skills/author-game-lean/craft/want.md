# craft/want.md — her situation, her start choice and her storylines on the Quests page

Read this before you write a card for the start (her situation, the creation screen, the start choice) or for a goal and its storyline on the Quests page (`[[story_hints]]`, `[[walkthroughs]]`). Checked against Course of Temptation (CoT) and the field (LO, relayed 2026-11-22: "yes, send it"). The plan-level want (the Want page, the premise, the hold and its face) is `plan.md` §2, which cites C25, C26 and C28. C6, C24, C27 and C29–C31 aren't cited in the skill yet; they belong to §2 when it's next revised, not here. The opening's screens are `craft/opening.md`; the bill's numbers are `craft/economy.md`.

## Must read

On a card with a `Does:` block (every card from 2026-11-24 on), the rows that apply come from `check.py --rules`, which lists each with its craft file; the card has no `Craft:` line (`piece.md` step 2). On a card from before 2026-11-24, the `Craft:` line cites each one, or says in one line why it skips it. `when` and `judge` are the labels in `SKILL.md`, "Rule labels".

| id | what it asks | the failure it stops | when | judge |
|---|---|---|---|---|
| C54 | her situation at minute zero is concrete: a job, a debt, a room, a reputation | — · kept blocking: LO's choice (2026-11-24) | the first screen | reader |
| C43 | give her the premise and a choice at minute zero | — | the first screen, the start choice | note |
| C44 | the start choice is a memory, not a slider, and sets a flag | P13 reader pass 7: the start choice was a wish about the future ("Good grades. I'll make you proud."), not a memory | the start choice | reader |
| C46 | a start-choice flag nobody reads is fake freedom | — | the plan | note |
| C48 | ask on a creation screen only what you print back | P13 reader pass 11: "Your name" was asked and never printed back | the plan | script + creation |
| C51 | a creation screen is about three fields | — | the plan | note |
| C1619 | the first objective is a storyline on the Quests page with steps: what's done and what's next | LO played P13's sums screen (2026-11-23): goal 1's card was one run-on line with stray stars, no steps to read ("What is this??"; fixed in 324ae159) | a goal card is shown | reader |
| C1628 | never spend the first screen on a systems lecture | — | the first screen | note |
| C430 | every step says how the player finds the next one | — · kept blocking: LO's choice (2026-11-24) | a goal card is shown | reader |
| C598 | see `craft/people.md` |  |  |  |
| C952 | see `craft/economy.md` |  |  |  |
| C992 | see `craft/economy.md` |  |  |  |
| C34 | the goal has no date | — · kept blocking: LO's choice (2026-11-24) | a goal card is shown | reader |
| C35 | a goal that can end names the next goal | — · kept blocking: LO's choice (2026-11-24) | a goal card is shown | reader |
| C36 | each goal names the flag set when it's met | — · kept blocking: LO's choice (2026-11-24) | a goal card is shown | reader |
| C37 | a goal whose end is in a later release says which release | — · kept blocking: LO's choice (2026-11-24) | a goal card is shown | reader |
| L172 | each hint entry and walkthrough a card builds is a screen on its Does:, so the goal-card rules reach it | the goal-card rules fired only on story screens with ✅ or ➜, and P46's ladders were read only because the game session put them in the reader brief by hand | a goal card is shown | script + does |
| C2176 | every flag a hint step reads is set by some canvas | — · kept blocking: LO's choice (2026-11-25, LO's "Go ahead") | a goal card is shown | script + pages |
| C433 | say the current ceiling honestly: "for now" | — · kept blocking: LO's choice (2026-11-24) | a goal card is shown | reader |
| C32 | keep the promise alive after the hold goes quiet | — | the plan | note |
| C56 | a bill is one hold of nine; an ambition she picked is the commonest for a female lead | — | the plan | note |
| C72 | a real recurring bill is rarer for a female lead, behind an ambition | — | the plan | note |
| C63 | her appetite is a destination, not where she starts | — | the plan | note |
| C64 | what she becomes is access: rising widens what she can reach | — | the plan | note |
| C65 | the ascent is a sentence about doors | — | the plan | note |

## The measures

CoT, re-read 2026-11-22 (`/Users/a0000/Documents/Player_Legibility_Study_20260825/corpus/course-of-temptation/passages`):
- **Minute zero.** `Prologue.txt`: the acceptance letter, "finally you can say you're going to college!", and the school's "a bit of a reputation as a party school". `Prologue14.txt`: "for the first time in your life, you're truly on your own."
- **Start choice as a memory.** `Prologue.txt` ends on "Think back..." into `PrologueHighSchool.txt`, which tells her high-school years and asks through `<<pickstartingtrait>>`. Four of those run across the prologue: popularity, relationship, relationship type and hobbies.
- **The first objective, in the story.** `Prologue16.txt`: "Tomorrow it'll be time for adventures like... figuring out co-ed showers. And maybe finding out who's hiring."
- **Done and next.** `StoryHints.txt` and `StoryHintWidgets.txt` list each storyline with a ✅ when it's done and a "Hint:" line for the next step.
- **The honest end.** `StoryHintWidgets.txt`: "You have reached the end of this storyline... for now! But there may still be recurring events."
- **What not to copy.** `PrologueFinal.txt` is a systems lecture: "Keep an eye on your left-hand side panel, particularly on your Needs bars". CoT does it; C1628 says don't.

Field-measured, from `lists/COVERAGE.md`'s evidence column and not re-run today:
- C48 and C51: a median of 3 creation fields, each read back about 4 times (13 games);
- C43: freedom is 25.9% of the reasons players love a game;
- C56 and C72: an ambition she picked is more common than a real bill in female-lead games;
- C1619: 21 of 26 games print "what next";
- C32, C63 and C64;
- C598: CoT hides people she hasn't met.

## The shape

Each rule is marked **measured** or **LO's choice**.

1. **A concrete situation at minute zero, and the problem has a face** (C54; the face is `plan.md` §2 and C1003). *Measured:* CoT's acceptance letter and "on your own"; *LO's choice* for the face.
2. **A start choice that's a memory, read later** (C43, C44, C46). A person on screen asks it, about her past (`craft/opening.md` rule 3); the answer is who she already is, not what she hopes for. A flag nobody reads is fake freedom. *Measured:* CoT's "Think back..." and its four `<<pickstartingtrait>>` picks.
3. **The first objective arrives in the story, not in a lecture** (C1619, C1628). *Measured:* CoT's "maybe finding out who's hiring"; its own systems lecture is the "not this".
4. **Each storyline is a `[[story_hints]]` entry: a ladder whose last passed step says plainly what's next** (C1619, C430), naming only people she has met (C598). A long storyline also gets a `[[walkthroughs]]` entry, whose steps show ✅ done and ➡️ to do. Each entry is a screen, `story_hints.<slug of its title>` or `walkthroughs.<id>`, and the card that builds it names it on its `Does:` with `a goal card is shown` (L172). Every flag a step reads is set by some canvas (C2176). The `[[quest_cards]]` stay: they decide who is met and give the tip in the People view, and they are not on the page. *Measured:* CoT's story hints (`StoryHints.txt`, `StoryHintWidgets.txt`); the engine is `[ui] quests_layout = "hints"` (`.claude/skills/author-game-v2/references/engine.md:1094-1120`).
5. **Every amount agrees with the ledger** (C952), and **the goal has no date** (C34). A bill that falls due every Sunday is a repeat, not a deadline. *LO's choice.*
6. **An honest "for now" end that names the next goal** (C35, C37, C433), and the goal names the flag that ends it (C36). *Measured:* CoT's "for now!"; the rest is *LO's choice.*
7. **A creation screen of about three fields, each printed back** (C48, C51). *Measured in the field.*

## Worked example

Roles: her step-father, and the café across from campus. LO approved these words, with the names swapped for roles. The amount is filler (C992).

Each storyline is one entry; the Quests page draws it. Only the last step whose `when` passed shows, after "Hint:"; "end" prints CoT's "You have reached the end of this storyline... for now! But there may still be recurring events."

**The storyline**
```toml
[[story_hints]]
title       = "Paying Your Way"
category    = "Storyline 📖"
description = "Your step-father wants your share every Sunday."
when        = [{ flag = "goal1_shown", op = "is_true" }]
walkthrough = "paying_wt"
hints = [
  { when = [], text = "Your step-father collects the rent at the kitchen table on Sunday mornings. Find the money before then." },
  { when = [{ flag = "cafe_hired", op = "is_true" }], text = "Work shifts at the café, and pay him every Sunday morning." },
  { when = [{ flag = "rent_paid_once", op = "is_true" }], text = "end" },
]
```

**Its walkthrough, as it reads after the job**
> ✅ Your step-father told you the rent.
> ✅ You got the café job.
> ➡️ Pay your step-father at the kitchen table on Sunday morning.

On the card, its `Does:` line: `story_hints.paying_your_way | a goal card is shown, the clock moves` (the step names a time of day).

## Not this

- A step that names someone she hasn't met. Until the meeting, "the café across from campus" (C598).
- A dated goal: "Make the rent by Friday" (C34).
- A card that lies about the amount (C952).
- A storyline step reading a flag no canvas sets: it never passes (C2176).
- A goal written as a ✅/➜ card in a story screen when the game has the Hints page: the storyline is a `[[story_hints]]` entry.
- A first screen that's a systems lecture: "Keep an eye on your left-hand side panel…" (CoT's `PrologueFinal.txt`; C1628).
