# craft/meters.md — her climb meters and the acts that move them

Read this before you write a card that defines a meter, or an act that pays one.

## Must read

The card's `Craft:` line cites each one, or says in one line why it skips it. `when` and `judge` are the labels in `SKILL.md`, "Rule labels".

| id | what it asks | the failure it stops | when | judge |
|---|---|---|---|---|
| C285 | five stages of 20 on each climb meter; a game may move a row, never drop the order | — (the table) | the plan | note |
| C294 | a release that writes stages up to N caps every pay at N's top, shows no button for an unwritten stage, names the next stage only on a card | P01 | the plan | reader |
| C295 | small rungs at 5, 10, 15 inside each 20: a small step of the same kind, never the next stage's kind | P01 cited C294 and missed this | a meter is shown or paid | reader |
| C381 | a small rung may show greyed as a preview of the next bolder act | P01 | a meter is shown or paid | reader |
| C188 | three "not yet" talks just below each line: she says why not yet; they raise and unlock nothing | P01 | a meter is shown or paid | reader |
| C330 | a repeatable act caps at the top of the stage above the one it opens in | P01 | a repeatable, a meter is shown or paid | reader |
| C1401 | a daily cap per band; about 2–3 paying acts a day at every stage; flag a stage over 14 days | P01 | the plan | reader |
| C210 | crossing a stage is a one-time moment that pays nothing | P01 | a meter is shown or paid | reader |
| C338 | an accident pays him, never her; the button where she goes further pays her; the way out pays nothing and is always there | first_term's accidents raised only the man (L68) | a meter is shown or paid | reader |
| C1366 | the Quests page names only places that pay at her stage | first_term's four cards named places that paid nothing at stage 1 (L68) | a goal card is shown | reader |
| C388 | a locked door says why: a number lock shows the engine's need, a story lock carries `locked_text` | first_term's "(Needs Hungry)" (L116) | a meter is shown or paid | reader |
| C541 | after a choice, his reaction line opens the next node and the engine's toast stays; never print a +X for a stat that isn't shown | P13 reader pass 9: after "Fix the knot first" the next screen didn't open on Ryan's reaction | a meter is shown or paid | reader |
| L68 | every stage, the first included, has acts that pay; only her choice pays | first_term stood at 0 on day 4 | the plan | reader |
| L69 | an act capped at its own stage's top can never cross it; 1-a-day caps made 20-day stages | first_term stuck at 39 | the plan | reader |
| L70 | the first gain on each climb meter is open at 0, not behind a 1-in-4 walk-in | first_term's Exhibitionism sat at 0 behind a 1-in-4 walk-in | a meter is shown or paid | reader |
| L116 | a lock names the meter and a number the player knows, never a stage word | "(Needs Hungry)" read like food | a meter is shown or paid | reader |

## The engine (cited; `v2.py` is `apps/game_generation/twee_comprehensive/generators/v2.py`)

- **An act's `cap` stops the meter there.** `if (next > capNum) next = Math.max(current, capNum)` (`v2.py:7377`). An act capped at 19 can never carry her past 19.
- **The daily cap per band** is `[engine.daily_caps.<trait>]`, read at `v2.py:1282-1283`. Each band is `{ below, cap }`: the most the meter may rise in one day while it is under `below` (`setup.dailyCapAllow`, `v2.py:7506-7522`). `hold_band_while` keeps her inside her band while a listed modifier is on.
- **`first_gain_message`** shows once, on the first rise (`v2.py:7547-7549`).

## The shape

1. **The table.** Five named stages of 20 per climb meter, each with a word the sidebar prints.
2. **A way up from 0.** Each stage, the first included, has at least two repeatable acts that pay. At least one is open at 0.
3. **Only her choice pays her.** An accident pays him. The button where she goes further pays her. The way out pays nothing and is always on the screen.
4. **Pay across the line.** A repeatable act caps at the top of the stage above the one it opens in, so repeating it carries her over.
5. **Small rungs.** At 5, 10 and 15 inside a stage, a small step of the same kind opens. It may show greyed as a preview.
6. **"Not yet", out loud.** Three talks just below each line, in her voice, paying nothing.
7. **Pace.** Daily caps by band, so a stage takes about 7–14 days at 2–3 paying acts a day.
8. **Locks and the Quests page.** A lock reads "(Needs <meter> <number>)". The meter's card names only places that pay at her stage.
9. **The crossing.** A one-time scene, paying nothing: the stage's name, who she is now, new things she might say yes to.
10. **A partial release.** Pay caps at the top of the last written stage, no button for an unwritten one, and the next stage is named only on a card.

## Worked example

Roles, not a world: one meter, **Nerve**. Stages: Careful 0–19 · Curious 20–39 · Daring 40–59 · Bold 60–79 · Reckless 80–100. The numbers are filler.

| act | opens at | kind | pays her | pays him | cap | how often |
|---|---|---|---|---|---|---|
| let a look go on, at the café | 0 | stage 1, her choice | +1 | — | 39 | daily |
| don't fix the top that slipped, at the bus stop | 0 | stage 1, her choice | +1 | — | 39 | daily |
| the lodger walks in on her towel | 0 | accident | 0 | Want +2 | — | once |
| that walk-in's button "Don't grab it" | 0 | her choice inside it | +1 | — | 39 | once |
| hold the stretch a beat longer, at the gym | 5 | small rung, same kind | +1 | — | 39 | daily |
| the not-yet talk with the neighbour | 16 | talk | 0 | — | — | once |
| her first chosen tease for one man she knows | 20 | stage 2 | +3, set once | — | — | once |

```toml
[engine.daily_caps.nerve]
bands = [ { below = 20, cap = 3 }, { below = 40, cap = 3 }, { below = 60, cap = 2 }, { below = 80, cap = 2 }, { below = 101, cap = 2 } ]
first_gain_message = "Someone looked, and you let them. Nerve goes up when you don't hide."
```

At 3 a day she crosses 20 in about 7 days. The two 0-acts and the rung at 5 give her three ways to spend each day's 3.

**The tease's button before she reaches 20** (a number lock, C388):
> Lean on his doorframe and let him look *(Needs Nerve 20)*

Never *(Needs Curious)*: she has never seen that word on a lock.

**Nerve's card on the Quests page at Careful** (C1366):
> *Let people look at you. At the café, at the bus stop, at the gym. Don't cover up.*

All three places pay at Careful. The neighbour's doorframe isn't named until she's Curious.

**The walk-in, after "Don't grab it"** (C338, C541):
> The towel slides to your waist, and you don't grab it. One second. Two. His eyes are on your tits, and he doesn't even pretend.
> "Jesus. Sorry." He backs out and pulls the door shut.
> Your face burns. You didn't grab it.

His line opens the screen, and the engine's toast shows the +1. No "+1 Nerve" is printed in the text.

**The not-yet talk** (at 16, pays nothing):
> The neighbour leans on the doorframe. "You keep coming back here, and you keep going home."
> "Because I'm not that girl yet."
> "Yet," he says, and smiles like he's already won.
> Your cheeks go hot. You said yet.

**The crossing** (one time, at 20, on the morning after, pays nothing):
> You catch yourself in the bathroom mirror, and you don't fix your top. A month ago you would have.
> Your face goes warm, and you still don't fix it.
> You're Curious now. There are things you might say yes to.

## Not this

- A card that cites the stage table and none of the rungs, talks or pace. A meter card cites every row above. (P01; NOTES skill gap 2026-11-20)
- Stage 1 acts that all need 20 already. Two acts pay at 0. (L68)
- An accident that pays her. It pays him; her button inside it pays her. (C338)
- An act capped at its own stage's top, so she stands at 19, then 39, forever. Cap at the stage above. (L69; `v2.py:7377`)
- A cap of 1 a day, so a stage takes 20 days. 2–3 a day. (L69; C1401)
- The first gain behind a chance walk-in. The first rise is open at 0, every day. (L70)
- A card that sends her to places that pay nothing at her stage. Name only the paying ones. (C1366; L68)
- "(Needs Curious)" on a lock. Write the meter and the number. (C388; L116)
- A crossing scene that pays. It pays nothing; she has already crossed. (C210)
- A "+2 Nerve" printed for a meter the screen doesn't show. Show the reaction line and the engine's toast. (C541)
