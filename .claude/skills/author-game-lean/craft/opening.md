# craft/opening.md — the opening

Read this before you write the opening's card. The opening is one piece (`plan.md`).

## Must read

On a card with a `Does:` block (every card from 2026-11-24 on), the rows that apply come from `check.py --rules`, which lists each with its craft file; the card has no `Craft:` line (`piece.md` step 2). On a card from before 2026-11-24, the `Craft:` line cites each one, or says in one line why it skips it. `when` and `judge` are the labels in `SKILL.md`, "Rule labels".

| id | what it asks | the failure it stops | when | judge |
|---|---|---|---|---|
| C520 | the staged opening: setup, the problem with a person, the temptation, the objective and its card; 34–57 words a screen is its target (stated, not measured) | P13 had no problem: a nice morning, then a towel | the opening | reader + length |
| C519 | loud is not long: split a screen with two jobs rather than fatten it | — (length) | always | note + length |
| C1626 | the field's first fiction screen: median 144 words (measured, 25 games) | — (the length ceiling) | the first screen | note + length |
| C1637 | a meeting is small and somebody speaks: median about 100 words, most under 150 (measured, 696 passages) | — (the length ceiling) | a first meeting | note + length |
| C1611 | staged open: one person at a time, on screen and speaking | P13's start choice was a narrator quiz | the opening | reader |
| C1613 | staged is the default; a cold open only when no person can be on screen | same | the first screen | reader |
| C327 | an opening of talk only is a failure; fill it with what her stage allows | P13's bathroom was one sentence | the opening | reader |
| C311 | a low-heat scene names a part of her body, writes his reaction, has a "not yet" or a price, and a hook | P13's hall | something sexual shows | reader |
| C314 | the low-heat failure is talk only: no body, no reaction | same | something sexual shows | reader |
| C601 | his leak shows on his body, she sees it; a man she lives with catches himself and covers | P13's Ryan leered and never covered | a first meeting, something sexual shows | reader |
| C109 | see `craft/arc.md` |  |  |  |
| C166 | see `craft/arc.md` |  |  |  |
| L71 | at stage 0–1 things happen to her; she doesn't choose to let him | P13's "And I'm standing here letting him" | something sexual shows | reader |
| C1604 | the cards showing at the hand-over carry goals | P13 left the goal card to P12 | the hand-over | reader |
| C1609 | the last screens may carry plain tutorial lines | same | the hand-over | reader |
| C1621 | the last screen ends on a hook: money problem, objective, mystery, person, choice | P13 ended on "go to breakfast" | the hand-over | reader |
| L171 | whatever the opening says is happening happens on day one, or a hint points at it | P13 promised "Today you start college" and no first-day scene existed; the old first_term's dean's-office first day was dropped | the opening | reader |
| C1631 | the hand-over lands where something is live at that minute | P13 landed in an empty kitchen | the hand-over | reader + sheet |

## The shape

**Length.** One job per screen is the hard rule: a screen with two jobs becomes two screens (C519). Aim for 34–57 words (C520's target, stated). A screen up to about 150 words still passes, the field's measured ceiling (C1626, C1637); over 150 is too long. (LO's call, 2026-11-20, relayed: "One job, up to ~150.")

1. **Setup.** Who she is, where she is, what she has, in her voice.
2. **The problem, carried by a person.** Someone says the hold out loud: an amount, a day, a condition. Someone who could help says nothing, and the screen says what that silence means.
3. **The start choice, asked by a person.** A person on screen asks about her past, and her answer is a memory of who she already is, not a wish (`craft/want.md` rule 2, C44; CoT's "Think back..."). The person asks because of something happening right then (the bill just said, the first day, a worry), never out of nowhere; a question about her past with no reason in the scene reads as random. Each answer costs or earns something with that person: a reaction line, and a flag only on the one that matters later.
4. **The build-up.** The room works against her (a lock, thin walls, one towel), then the interruption.
5. **The temptation, at her stage.** It happens to her. The screen stays on her body and his reaction: a named part of her, his eyes on it, his leak, and (a man she lives with) his cover. His spoken line can be about anything; the screen around it is about her body. There's a price or a "not yet" (the towel slipping). She reacts on her body (her face, her breath, her nipples), never in an italic thought (`craft/voice.md`). No button is a final no; staying a beat is allowed.
6. **Objective and card.** The hold becomes the first storyline on the Quests page (a `[[story_hints]]` entry, `craft/want.md` rule 4), with plain tutorial lines under it; the last screen says where to find it ("If you want some hints on what to do next, try the Quests button.").
7. **The hand-over, on a hook.** The last click lands where a person is doing something at that minute. The screen ends on money, the objective, a mystery, a person and a choice.
8. **The opening delivers what it promises** (L171). Whatever it says is happening ("Today you start college") happens on day one as a scene, or a hint step points at it with its place and time. A promise with nothing behind it is the failure: P13 promised college and no first-day scene existed. The old first_term had one, its dean's-office first day (`games/first_term/toml_phases/5_scenes.toml:35251`). *LO's choice* (LO, typed in main-lean 2026-11-25: "Go ahead").

## Worked example

Roles, not a world: a rented room, a landlord, his wife, another lodger. Word counts are for the story text.

**1 · Setup** (44 words)
> You're nineteen, it's your first morning in a rented room above somebody else's kitchen, and you have forty dollars to your name. The bed sags, the window sticks, and the door doesn't lock.
> Your stomach's tight, and you're smiling anyway. Nobody here knows you.

**2 · The problem, carried by a person** (57 words)
> The landlord is at the bottom of the stairs with a mug, like he's been waiting for you.
> "Rent's a hundred a week. Friday. I said it on the phone, and I'm saying it again."
> His wife is at the stove behind him. She doesn't turn round.
> Your face goes hot. You have forty. She heard it.

**3 · The start choice, asked by a person** (39 words)
> He doesn't move off the bottom step.
> "Last girl in that room left owing me three weeks. What makes you any different?"
> He asks like your answer decides how much slack you get on Friday.
> Your mouth goes dry.

| button | the first line after the click |
|---|---|
| "I've worked every summer since I was fourteen. You'll have it Friday." | *He nods once. "We'll see."* |
| "I've talked my way out of worse than you." | *His mouth goes thin. He writes something on the calendar by the phone.* · sets `landlord_crossed` |
| "I left worse than this behind." | *He snorts, but he steps aside.* |

**4 · The build-up** (54 words)
> The bathroom at the end of the landing is shared, and the bolt only goes in halfway. The radio comes up through the floor. You get the water hot and give yourself one minute.
> Then the handle rattles.
> "Some of us work for a living!"
> You knot the towel under your arms. It's short.

**5 · The temptation** (55 words)
> The other lodger is on the landing in his work shirt. His eyes drop to your wet thighs, where the towel ends, and climb slow to your chest.
> He catches himself, stares at the wall, and holds his jacket low over his jeans.
> "Morning. Sorry."
> The knot is slipping.
> Your face burns. Don't look back.

Buttons: "Hold the towel and get past him" · "Say good morning back" · "Wait for him to go first". Each opens on one line of his reaction. None closes anything.

**6 · Objective and card** (40 words)
> A hundred by Friday. Forty in your purse.
> The café on the corner has a sign in the window. And on the stairs the landlord said there are "other ways to make rent in this house." He didn't say what.

The card it arms: *Pay your own way: rent every Friday.* Goals: *Ask at the café* · *Find out what he meant.*
Plain lines under it: *You need money. Take shifts, or find another way. People are in different places at different hours. What you say changes how they treat you.*

**7 · The hand-over, on a hook** (53 words)
> His wife is at the stove, alone now, and this time she looks right at you.
> "He told you Friday." She turns the gas down. "He'll tell you a lot of things. Sit. Eat something before you go looking."
> Your stomach drops. You can't tell if that was a warning or an offer.

Buttons: "Sit with her" · "Go and find work". Both lead into the live kitchen, where she is.

## Not this

- A morning and a towel with no hold in it. The problem comes before the temptation, said by a person. (P13, failure 1)
- "So what do you want?" in the narrator's voice. A person asks it, and the answer costs something with them. (P13, 2)
- One sentence of bathroom before the hall. Build the room and the interruption first. (P13, 3)
- He looks and keeps looking. A man she lives with catches himself and covers. (P13, 4; C601)
- A screen that drifts off her body into talk. His line may be about her day; the screen stays on her body and his eyes. (C311, C314)
- Her choosing it ("and I'm letting him") below the stage that opens a choice. She reacts, on her body. (P13, 5; L71)
- An italic thought on any screen ("*Did he just... no.*"). Her reaction goes on her body (`craft/voice.md`). (P13)
- "You give yourself five minutes." The shower and the towel are body moments: on her body, with a picture of her (`craft/body-moments.md`). (P13)
- "(ends his path)" on his first step. The opening says no to nobody. (P13, 6; C166)
- A last screen that ends on an errand ("go to breakfast"). End on the hook. (P13; C1621)
- A hand-over into an empty room, waiting for a later piece. The last place has a person in it at that minute. (P13, 7; C1631)
