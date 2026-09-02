# OPENING — Orientation  `[READY]`

**Shape: STAGED OPEN** (`the-first-hour.md` F1). Three people enter one at a time, each described,
each **speaking**, each stating what they want. Committed to — not a cold open, and not the middle,
which is the defect: a cold open carrying a staged open's payload names people the player cannot
picture. The measured failure named **six people, two of whom are not in the game at all**, and put
none of them on screen.

**Consistency rule, not a word count.** The cast load and the word budget have to agree. F1 published
word counts until 2026-08-24 and Section K deleted every one of them — eight of twenty-five opening
walks move once the extractor can see setter links, and three rebuild methods disagree with each
other by four to seven times. The axis that survives is **who is named**, which you check by opening
the first passage and reading it.

---

## The screen walk

One row per screen, in order, with the button **quoted**. A screen either exists or it does not.

```
  #  canvas · node                what is on the screen                        the button
 ──────────────────────────────────────────────────────────────────────────────────────────────────
  0  Start                ENGINE  title card · age gate                        "✓ I am 18 or older
                                                                                 - Enter Game"
  1  CustomizeCharacters  ENGINE  her name · what Ray is to her ·              "Continue to Game"
                                  what Wes is to her · player_description
 ──────────────────────────────────────────────────────────────────────────────────────────────────
  2  arrival_night.base           the avenue, the car, the house.              "Let him take the
                                  RAY on the step. He speaks.                   heavy one."
  3  arrival_night.kitchen        the kitchen. DEE in scrubs,                  "Tell her you're fine."
                                  going out the door. She speaks.
  4  arrival_night.wes            WES in the doorway with a plate.             "Ask which one's the
                                  He speaks.                                    bathroom."
  5  arrival_night.the_question   her room — the office with the shelves       ── THE START CHOICE ──
                                  still on the wall. Wes leans in and          "I had a 4.0 and nobody
                                  asks what she was at her old school.          to talk to."
                                                                               "I was always with
                                                                                people older than me."
                                                                               "Nobody there knew my
                                                                                name."
  6  arrival_night.lights_out     the answer lands. Three bands on the         ── location exit ──►
                                  flag. She sets an alarm for six.
 ──────────────────────────────────────────────────────────────────────────────────────────────────
     THE FUNNEL ENDS  ►  the_avenue, 07:20, MONDAY
                         sets  met_ray · met_dee · met_wes · past_top|past_crowd|past_nobody
```

⚠️ **Rows 0 and 1 go in even though we do not author them.** Leaving them off is how a sheet ends up
describing an opening the player never has. **The player's first screen is never beat 1.**

⚠️ **Row 1's headings and button are hard-coded** — *"Customize Characters"*, *"Personalize the
characters in your story"*, *"Continue to Game"* (`v2.py:1065`, `v2.py:9251`). The **only** authored
text on that screen is `player_description` (`v2.py:9509`). Seven of fifteen built games ship the
default, in a product voice, as the second thing a player reads. Ours:

> *You have been in this house four hours. Nobody in it has a read on you yet.*

⚠️ **`[player] customizable = true` repoints the age gate at row 1.** And `v2.py:9294` emits a name
textbox for **every** customizable NPC unconditionally, so Ray and Wes are both player-renameable:
**every line of prose about them uses `@ray` / `@wes`, never a typed name.** Dee, Simone and
Halloran stay fixed.

---

## What is on each screen

**One node is one screen.** Three beats in one node is ONE screen carrying all three. The break
between screens is a written button in the game's voice — never "Continue".

### Screen 2 · `arrival_night.base` — RAY
The avenue, the car still ticking, two suitcases. He comes down off the step and takes one without
being asked. **He speaks first**, and what he wants is stated: he wants this to go well, and he says
so in a way that puts the cost on her.

### Screen 3 · `arrival_night.kitchen` — DEE
Already in scrubs, keys in her hand, leaving. **She speaks**, and what she wants is the thing that
makes the whole game cost something: *be good to him, he's paying for it.* She is out of the door
inside her own beat. `the_kitchen` 17:00–21:00 is her only window, and she is gone by 21:15.

### Screen 4 · `arrival_night.wes` — WES
A plate in one hand, already eating off it. **He speaks**, and what he wants is to know what she is
going to be on his campus, because it is his and now it is also hers.

### Screen 5 · `arrival_night.the_question` — THE START CHOICE
**A memory, not a slider.** The scene is already asking it. No stat screen, and nothing is shown to
the player as a number.

| button | flag | what it buys — REACH, not flavour |
|---|---|---|
| *"I had a 4.0 and nobody to talk to."* | `past_top` | Halloran hands her the reader's key in week one; the late lab is reachable before anyone else's |
| *"I was always with people older than me."* | `past_crowd` | Simone walks her past the sign-in book; the upstairs is not a stranger |
| *"Nobody there knew my name."* | `past_nobody` | she is not clocked where she should not be, and `reputation` climbing from zero is worth more |

**Five read sites each. ADDITIVE ONLY** — every original rung keeps every number it had and gains
`<flag> is_false`, so a save made before the choice shipped reads exactly what it read yesterday.

### Screen 6 · `arrival_night.lights_out` — the handover
Three `[group]` bands on the flag, so the last screen of the opening is already different depending
on what she just said. Then the alarm, and the exit.

⚠️ **Separate the three-band group from anything else on this node with a non-`group` block.**
Adjacent `[group]` blocks merge into ONE if/elseif chain and first match wins (`v2.py:14637`) — the
second ladder goes dark with no error and no build warning.

**Exit:** `type = "location"`, `locationId = "the_avenue"`, to **07:20 Tuesday**, carrying
`flagEffects` for the three met-flags and the chosen `past_*`.

---

## F3 · The handover lands on an open door

**07:20 Monday, `the_avenue`.** What is live at that minute:

| | |
|---|---|
| the bus | the bridge to `the_quad` — 40 min, $2. Always open |
| `@wes` | on the avenue with the car, **07:15–07:50** (his row 2). The ride would be 15 min and a **favour**, not a fare — ⚠️ **the canvas does not exist**; see `sheets/places/the_avenue.md` |
| walk back inside | **`the_hall`**, and `her_room` / `the_kitchen` / `the_bathroom` off it. The hall says who is in before she picks a door |

Gate *the opening opens a door* checks exactly this: that the funnel's last click lands on a clock
time when something at that location is actually open.

⚠️ **The ride is the game's thesis on the first screen after the funnel.** Two ways across: pay, or
ask a man. That is the bridge doing the work `the-map.md` gives it, and it is why this is `two_hub`
and not a nested world with a corridor.

---

## F4 · Every live system gets one beat

Nine systems are on in v0.1 and each is touched once inside the funnel, or on day one at the latest:

| system | where it is first felt |
|---|---|
| `rest` | screen 6 — she sets an alarm for six and the night is short |
| `clean` | screen 4 — Wes and the one bathroom, established before it matters |
| `fed` | screen 3 — Dee leaves food out; screen 4 Wes is eating it |
| `money` / the dues | **day one at `the_pledge_house`**, not in the funnel. The obligation is armed *after* income exists |
| `home_face` | screen 3 — Dee says *be good to him*, which is the meter stated in a person's mouth |
| clothing | day one, `her_room` wardrobe, before the first crossing |
| the phone | day one — the first thread arrives from `@wes` on the bus |
| `reputation` | day one at `the_quad` — the first line that changes because someone has already heard |
| the ascent tiers | first rung reachable day one, at `the_pledge_house` |

⚠️ **F4b — the opening refuses nothing.** No locked row, no greyed choice, no *you can't do that yet*
anywhere in screens 2–6. The first refusal the player meets is on day one, and it carries its reason.

---

## The two meetings that are NOT in the funnel

`the-first-hour.md` **F5**: no character's portrait is live before a meeting has fired, and **one
flag never opens the whole cast.** Five separate flags.

| character | met where | met when | flag |
|---|---|---|---|
| `npc_ray` | funnel, screen 2 | arrival night | `met_ray` |
| `npc_dee` | funnel, screen 3 | arrival night | `met_dee` |
| `npc_wes` | funnel, screen 4 | arrival night | `met_wes` |
| **`npc_halloran`** | `the_quad`, the eight o'clock | **Mon 08:00–09:30** | `met_halloran` |
| **`npc_simone`** | `the_pledge_house`, the sign-in book | **Mon 16:00–19:00** | `met_simone` |

⚠️ **Each meeting canvas carries a `trigger.schedules` window matching that character's own hours.**
`requires_npc` does **not** gate the auto-fire path, so a meeting without one plays to an empty room.
Gate *a meeting fires where they are* checks this.

⚠️ **F6 — a meeting is small, and somebody speaks.** Both of these are one screen with a line of
dialogue in it, not a scene. **F7 — role before name:** the player is told *the woman with the
sign-in book* and *the man who teaches the eight o'clock* before either is named, and **F10** keeps
the role attached afterwards.

---

## Where this ends

Day one closes with the dues named and not yet due, and **the row of houses visible from the quad
and locked** — `reputation` 85, which is the release-41 target. Every release ends on a door, and
v0.1 is no exception.

---

## ⚠️ Two conflicts this sheet had, found by reading it against the person grids

Recorded rather than silently fixed, because S5's whole point is that **the person sheet is the only
artifact that can see across rooms** and the incident behind it was two sheets each correct about
one room.

1. **Wes was in two places at one hour.** This sheet had him on `the_avenue` 07:10–07:45 while
   `people/wes.md` had him in `the_bathroom` 07:00–08:00 — thirty-five minutes of overlap, and he
   cannot be in both. Resolved on the person sheet: bathroom **06:40–07:10**, avenue
   **07:15–07:50**. The bathroom walk-in now costs her getting up before seven, which `rest`
   decides — a real price arriving from a scheduling fix.

2. **The handover landed on a Tuesday and there was no class.** Halloran teaches `[0,2,4]`
   Mon·Wed·Fri. A first day of college with no eight o'clock reads as a bug, and both day-one
   meetings would have had to wait. **`[time] starting_day` is SUNDAY**, the funnel runs the arrival
   night, and the handover is **Monday 07:20** — which puts Halloran's meeting at 08:00 and
   Simone's at 16:00 on the same day, each inside its own character's hours.
