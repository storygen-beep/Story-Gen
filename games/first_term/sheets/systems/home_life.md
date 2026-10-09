# [READY] System — home_life

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> New 2026-10-08: LO's everyday picks 3, 4, 6, 9, 10, 11, 13, 14, 16 and 17 (LO, 2026-10-08), from
> round 11. One card for the everyday at home, so every home row names its system (question 53, LO: yes).
> Every number marked "guess" is new here and waits for your yes.

| row | answer |
|---|---|
| id · name | `home_life` · Life at home |
| place and hours | the house: kitchen, living room, garage, garden, her room, the hall · each item keeps its own hours, below |
| cost | time on every item · a little energy on the chores · no money |
| one ladder or two | one: the person who is there sets the rung |
| people | Laura, Mark, Ryan: only where their rows put them |
| pool | `home_event` (the random events at home) · `daily = true` |
| memory | each item's "done" flag, read by hours since it was set · `room_tidy` for the week |
| growth | climbs, through the person who is there |
| sink and deadline | none: home costs no money |
| feeds | Laura's Warmth · Ryan's Warmth and Want · Mark's Want · Exhibitionism · Corruption (Bold only) · energy |
| reads | who is home (their rows) · her two stages · each person's step · what she wears |
| what drives it (S8) | the person in the room picks the version; her stage picks the choices; her clothes pick their line |
| link into the hook | the house is where the people live: every small raise here feeds the next step on their ladder |
| leads to | Laura, Ryan, Mark |
| day 1 | yes: breakfast with Laura is the opening's; from day 2 every item is open |
| BRAKE (S9) | each item, once a day per person: its flag is set on use and read as "not set, or set 12 hours ago or more" (hours since a flag; nothing to clear overnight) |

## The rule for every item (LO, 2026-10-08, from round 11)

- **Alone, it is plain.** One short screen, the time passes, a need moves. No raise.
- **With a person there, it raises that person by a small step:** Laura's Warmth add +1, Ryan's
  Warmth add +1 (plain) or Want add +1 (a tease), Mark's Want add +1.
- **From her stage, it can turn.** Curious or Daring: a tease. Bold or Showing: a touch, but never
  past what that person's own steps have reached. The sex versions wait for Hungry (SP2: "the taboo act
  at home"), so in 0.1 each locked choice shows "Needs Hungry".
- **One canvas per person per room and hour.** The engine shows one repeatable scene per person, place
  and window, so an item with a person in it is a **choice inside that person's hub there**, never a
  second scene. Alone, it is its own row.
- **Every line names only who is there.** A person is in a line only in the hours their row puts them
  in that room.

## Who can be there (from the ledger rows)

| item | place | when it is open | Laura | Mark | Ryan |
|---|---|---|---|---|---|
| 6 breakfast | kitchen | every day 06:30–10:00 | Mon–Fri 06:30–08:00 | Sun 08:00–10:00 (after the count) | — (he showers, then work) |
| 6 dinner | kitchen | every day 18:00–20:00 | Mon, Tue, Thu, Fri, Sun 18:00–19:00 | Mon, Tue, Thu, Fri 18:00–19:00 · Wed (he cooks) · Sun | Mon, Tue, Thu, Sun 18:00–19:00 |
| 9 help cook | kitchen | 17:30–19:00, when someone cooks | Mon, Tue, Thu, Fri, Sun 18:00–19:00 | Wed 18:00–19:00 | — |
| 14 dishes | kitchen | 19:00–21:00 | Mon, Tue, Thu, Fri, Sun | Wed · Sun | — |
| 11 coffee | kitchen | 06:30–11:00 | Mon–Fri 06:30–08:00 | Sun 08:00–11:00 | — |
| 11 a drink | kitchen with Laura 20:00–22:00 · living room with Mark 22:00–02:00 | after Laura C 3 (the wine) | Mon, Tue, Thu, Fri, Sun | Sun–Fri 22:00–00:00 · Mon–Sat 00:00–02:00 | — |
| 3 TV | living room | 07:00–02:00 | Sat 22:00–00:00 | Sun–Fri 22:00–00:00 · Mon–Sat 00:00–02:00 | Sat, Sun 14:00–18:00 |
| 10 movie night | living room | 19:00–00:00, two hours | Sat 22:00–00:00 (she waits up with a film on) | late nights, as TV | Sat, Sun 14:00–18:00 |
| 13 laundry | garage (the washer) · garden (the line) | 07:00–21:00 | — | garage Mon, Tue, Thu, Fri 19:00–22:00 · Sat 09:00–17:00 | — |
| 16 tidy her room | her room | any time | Laura checks at Sunday dinner | — | — |
| 17 the garden | garden | 07:00–21:00 | — | Sat 09:00–17:00, from the garage door | Sat, Sun 07:30–18:00, from his window |
| 4 random events | hall, kitchen, living room, bathroom | on entering, once a day | by her rows | by his rows | by his rows |

## Costs and what each pays (guesses)

| item | cost, with op (S4) | pays, with op | alone | brake |
|---|---|---|---|---|
| 6 breakfast | 15 min | energy add +10 | plain: toast at the counter | `ate_breakfast` · 12 h |
| 6 dinner | 30 min | energy add +15 | plain: a plate alone | `ate_dinner` · 12 h |
| 9 help cook | 30 min · energy add −5 | the person: +1 | (she doesn't cook alone: no row) | `helped_cook` · 12 h |
| 14 dishes | 20 min · energy add −5 | the person: +1 | plain: she does them alone | `did_dishes` · 12 h |
| 11 coffee | 10 min | energy add +5 | plain | `had_coffee` · 12 h |
| 11 a drink | 30 min | the person: +1 · `drinks_boost` on (one drink) | (no drinking alone at home) | `had_drink_home` · 12 h |
| 3 TV | 60 min | energy add +5 | plain: the channels | `watched_tv` · 12 h |
| 10 movie night | 120 min | energy add +5 · the person: +2 | plain: a film alone | `movie_night` · 12 h |
| 13 laundry | 30 min · energy add −5 | the person: +1 | plain | `did_laundry` · 12 h |
| 16 tidy her room | 30 min · energy add −5 | `room_tidy` set true | plain | once a week: Sunday dinner reads and clears it |
| 17 the garden | 60 min | energy add +5 · exhibitionism add +1 at Daring, seen | plain: the sun | `sunned` · 12 h |
| 4 random events | none | by the event | "Nothing happens." written out | one per day, rolled 1 in 4 on entering (question 59) |

## Lewd ladder (`lewd_ladder[]`) — what each person turns it into

| rung | gate | Laura | Ryan | Mark |
|---|---|---|---|---|
| 1 · Good Girl · Covered | none | talk; she reads what @player wears (her line per clothing state) | talk; he looks and looks away | talk; he counts her hem |
| 2 · Curious · Daring | her stage 20 · and their step: Laura C 1 · Ryan A 4 · Mark A 3 | a tease: she fixes @player's hair, her hand stays; @player lets her look | a tease: her feet in his lap on the couch, his eyes on her ass | a tease: she bends to the dishwasher and lets him watch |
| 3 · Bold · Showing | her stage 40 · and their step: Laura C 7 · Ryan A 8 · Mark A 7 | a touch: Laura's hands on her waist at the stove, then her hips | a touch: his hands under the blanket (his 0.1 repeat) | the look he pays for: "twenty and you can look" (his 0.1 price) |
| 4 · Hungry · Watched | later: "Needs Hungry" | later | later | later |

**Crude words** (SP2, a ceiling, never a floor): Laura early body, chest · middle tits, nipples.
Ryan early ass, tits · middle cock, wet. Mark early legs, ass · middle tits, cock.

## The meters it writes and reads (`board.meters[]`)

| meter id | kind | key | fed at | read by |
|---|---|---|---|---|
| room_tidy | sourced | `room_tidy` | `home_ella_room` | Laura at Sunday dinner: praise, or a mess she finds |
| laura's Warmth · ryan's Warmth and Want · mark's Want | sourced | their own keys | kitchen, living room, garage, garden | their step gates |
| energy | sourced | `energy` | kitchen, living room, garden | every lock energy shuts |

## More items with a person at home (batch 3)

| item | where · when | alone | with a person | cost and pay, with op | brake |
|---|---|---|---|---|---|
| 15 the grocery run | Laura asks at dinner (her evenings) · the corner shop 07:00–22:00 · back to Laura in the kitchen | — | Laura: "Could you get these? Here's twenty." money add +20, `grocery_list` set · delivered at her next evening: Warmth add +2, `grocery_list` and `groceries_bought` set false · not done after 24 hours: "Where's my shopping?" `laura_suspicion` add +2 | 15 min at the shop · money add −20 there | one list at a time |
| 7 study at the kitchen table | kitchen · Laura's evenings 19:00–22:00 | (her desk, her room: plain) | Laura reads over @player's shoulder: Warmth add +1 · Curious: her hand on @player's neck while she reads | 60 min · energy add −10 · the grade add +1 | `studied_home`, 12 h |
| 12 hair and make-up with someone | master bedroom · Sat 17:00–18:30 (Laura dressing) · Zoe's Living Room · Fri 18:00–19:00 | her mirror: plain | Laura does @player's hair: Warmth add +1 · Zoe does @player's face before the party: "Lips. Open." | 20 min · `made_up` set true | `made_up`, 10 h |

Round 11 cards: groceries 3/12 · study at home 5/12 · getting ready 3/12.

## Rows a gate needs

| row | gate |
|---|---|
| a meal every day at home | a need can be met every day |
| each item with a person leads to that person | leads to a person |
| each item has its brake on the way in | an act is never free |
| the random events write "nothing happens" | random events say so |

## Why — the source of each key choice

| key choice | source |
|---|---|
| the ten items | LO, 2026-10-08 (the 17 everyday picks) |
| alone plain, with a person a small raise, a tease or more by stage | LO, 2026-10-08 · round 11, key point 4 |
| meals are scenes, food refills energy, no hunger | LO, chat (SYSTEMS §5) |
| a person's item is a choice in their hub | the engine's one-scene-per-person-place-hour rule |
| sex waits for Hungry | SP2 §1 ("the taboo act at home") |
| brakes by hours since a flag | guess: avoids adding flags to SP1's overnight list |
| every time, energy and raise number | guess |
| round 11 cards | TV 7/12 · random events at home 6/12 · meals 5/12 and the household table 4/12 · cooking 4/12 · movie night 4/12 · coffee or a drink 4/12 · laundry 3/12 · garden 3/12 · dishes 2/12 · room cleaning 1/12 |
| dinner hour and Ryan's TV afternoons | LO, 2026-10-08 (questions 54, 55) |
| questions 53–61 | LO, 2026-10-08: as recommended |
| items 7, 12, 15 with a person | LO, 2026-10-08 (picks) · numbers guess |
