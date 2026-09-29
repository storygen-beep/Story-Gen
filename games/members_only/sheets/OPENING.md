# [READY] Opening — Members Only
> Signed by LO 2026-09-29, the day it was drafted — LO bypassed the day-after rule for this test.

> The funnel, screen by screen, from the age check to the first open door. A staged opening: one
> person at a time, each on screen and talking. It starts Tuesday 17:00 and hands over at the Bar
> at 18:01, when her shift is open.

## Needs you first

| # | question | my recommendation | why it matters |
|---|---|---|---|
| 1 | Noor's locker scene is a one-time scene in the Dressing Room, which is also the wardrobe room. The engine can hide the wardrobe link while a one-time scene there hasn't fired. | Check it in the first build; if it hides the link, move the wardrobe to the Staff House. | She could lose "Change Clothes" for her first nights. |

## The screen walk

| # | where · screen | what is on the screen | the button(s) |
|---|---|---|---|
| 0 | engine · title | title card, age check | "✓ I am 18 or older - Enter Game" |
| 1 | engine · character screen | one field: her first name. Headings are the engine's. Our one line: "Dana's little sister. Twenty-four. Nobody here knows your name yet." | "Continue to Game" |
| 2 | Staff House · arrival (boot) | **setup and problem, in her voice** — written in full below | "Knock on the staff door" · "Skip the opening" |
| 3 | Staff House · Noor | **the first person.** Noor opens the door, cigarette in hand. "You're the sister. God, you look like her." She pushes: "Julian said you'd come. So why'd you and your sister stop talking?" | "We fought over a man." · "She walked out on me." · "I walked out on her." |
| 3a–c | Staff House · her answer | **the first choice lands as a reaction line:** a man — Noor laughs, "Course you did." · she left — "She did that." · you left — Noor goes quiet, "Then why are you here?" | "Walk up to the club with her" |
| — | exit to the Club, 25 min | sets `arrived` · one of `past_same_man` / `past_she_left` / `past_you_left` | — |
| 4 | Club · Julian (capstone) | **the conflict.** Julian: "Evening, Dana." A pause. "Miss. Forgive me." He names the tab: "Your sister left this club in debt. Three hundred dollars, every Sunday, to me." He holds up a black dress: Dana's, from her last photo. "Hers fit. Let's see if yours does." | "Change in front of him" · "Tell him to turn around" |
| 4a–b | Club · the dress | **the temptation.** In front of him: he watches all of it and says nothing. `shown` add 1 · Turn around: he turns, and in the mirror she sees him watching anyway | "Follow him onto the floor" |
| 5 | Club · the floor | **the rest of the cast, met.** Ade behind the bar pours her a drink before she asks: "Welcome, new girl." Kessler at his table holds a page an inch from his face, then lowers it to look at her. "Dana's sister. Library. After close." Two members at the bar stop talking as she passes. | "Take your tray" |
| 6 | Club · how it works | **the plain lines, in the game's voice:** "Work shifts at the Bar for tips. Dana's tab is $300, every Sunday, to Julian. Kessler is in the Library after close, and he has something of Dana's. Your bed is in the Staff House, down the path." | "Start your shift" |
| — | exit to the Bar, 15 min · **18:01** | sets `opening_done` · Dana's black dress into her wardrobe, worn · arms the Dana card | — |
| | **THE FUNNEL ENDS** | the Bar at 18:01: the shift is open (18:00–22:00); Ade, Noor and Julian are here; Kessler at 19:00 | |

**Clock:** 17:00 → three screens at 3 min → 25 min up the path → 17:34 · four screens → 17:46 · 15 min
→ **18:01**. **The skip** on screen 2 sets every flag above, gives the dress, arms the card, and lands
at the Bar at 18:01.

## Screen 2, in full

> You're twenty-four, you're broke, and your sister Dana hasn't answered you in eight months. She
> worked at the Linden, the members' club on the cliff above this town. In May she stopped writing.
> Her last letter said four words: Don't come looking. So you came looking. You took her old job,
> because it was the only door into the club. Tonight is your first shift. You're scared of what
> you'll find up there. You're more scared of what you won't. The staff house is halfway up the
> cliff path, and the light is on.

*94 words · median sentence 9 · no dashes · measured with `gates.py --beat`.*

## The card it arms — "Dana"

| goal | done when |
|---|---|
| Work your first shift at the Bar | `first_shift_done` |
| Find Kessler in the Library after close | `kessler_stage` ≥ 1 |
| Pay Julian on Sunday | the tab is paid |

**The Sunday charge starts only after the first shift** — the opening costs her nothing.

## Every live system gets a beat

| system | where the opening arms it |
|---|---|
| her past | screen 3 — the question |
| what she has on | screen 4 — Dana's dress, in front of Julian |
| money | screens 4 and 6 — the tab, the tips |
| her look · energy | the sidebar words, from screen 2 on |
| the pages | screen 5 — Kessler's page |
| the talk | screen 5 — two members stop talking as she passes |

**Nothing in the opening says no to her.** Julian turns around when she asks; Noor's question has no
wrong answer.
