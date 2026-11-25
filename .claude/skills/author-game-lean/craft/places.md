# craft/places.md — a place's screen

Read this before you write a card that builds or changes a place: its description, who is shown there, its buttons. Checked against Course of Temptation (CoT) and the top games (LO, relayed 2026-11-22: "Confirm each with the top games and CoT mostly", then "yes, send it"). What she walks into at a place is `craft/walk-ins.md`; the dress rule at a place's door is the clothes file's, when it exists; the picture is `craft/media.md`; its hours, its closed line and the time on its buttons are `craft/clock.md`.

## Must read

On a card with a `Does:` block (every card from 2026-11-24 on), the rows that apply come from `check.py --rules`, which lists each with its craft file; the card has no `Craft:` line (`piece.md` step 2). On a card from before 2026-11-24, the `Craft:` line cites each one, or says in one line why it skips it. `when` and `judge` are the labels in `SKILL.md`, "Rule labels".

| id | what it asks | the failure it stops | when | judge |
|---|---|---|---|---|
| C769 | a place says what it is and what happens there in its own description | — | a place is entered | note |
| C794 | the identity sentence is the same on every visit | — | a place is entered | note |
| C795 | re-entry changes come from the faces of who is there, the crowd, the menu, and events; never a room-text line per person. LO's choice (LO, 2026-11-24: "We can drop it one line per person rule. Yes go ahead"), with CoT (rule 2) | — | a place is entered | note |
| C804 | places have people: who is there shows as their faces (and an unnamed crowd line, if wanted), not as a line per person in the room text. LO's choice (LO, 2026-11-24: "We can drop it one line per person rule. Yes go ahead"), with CoT (rule 2) | first_term: 16% of places had people | a place is entered | reader |
| L106 | a line claims someone is there whom their rows don't put there | first_term's `master_asleep` snored while Mark was in the living room | a place is entered, a person is on screen | reader + presence |
| C776 | the menu holds three kinds of thing: a need, a system, a person | — · kept blocking: LO's choice (2026-11-24) | a place is entered | reader |
| C777 | anything else goes inside a beat, not on the menu | — · kept blocking: LO's choice (2026-11-24) | a place is entered | reader |
| C773 | top games' room buttons are sleep, work, dress, eat, wash; never a browse list of objects | — · kept blocking: LO's choice (2026-11-24) | a place is entered | reader |
| C758 | labels run short: median 3 words | — | a place is entered | note |
| C953 | the label carries a money cost before the click, and never time or energy (LO, 2026-11-24: "Beside choice i dont want to show time and energy show money if needed"; "Room buttons too") | — | a place is entered, a price or pay is shown | note |
| C954 | see `craft/economy.md` |  |  |  |
| C738 | a thoroughfare only routes; a destination has one thing to do alone, or hours and a closed line | — · kept blocking: LO's choice (2026-11-24) | the plan | reader |
| C762 | "Nothing happens." is banned | L150; first_term_lean: 15 places said "Nothing to do here right now" | a place is entered | reader |
| L147 | see `craft/walk-ins.md` |  |  |  |
| L170 | a place hidden until a flag has the step that sets the flag pointed at by a hint | the Faculty Offices stayed hidden until `met_walsh`, so missing her class hid them for good (P04, P16) | a place is entered | script + pages |
| C808 | root the world outdoors, in more than one zone | — | the plan | note |
| C811 | the map shapes: nested zones by default, a street or quad as each zone's hub | — | the plan | note |
| C770 | the field's room screen: median 82 words a visit | — | a place is entered | note + length |
| C771 | a first-visit screen is rare (DoL only); never a place's only introduction | — | a place is entered | note |
| C707 | world fill: one anchor holds about 30% of place prose | — | the plan | note |

## The measures (re-run 2026-11-22)

CoT's 126 passages tagged `location` in `/Users/a0000/Documents/Player_Legibility_Study_20260825/corpus/course-of-temptation` (`index.tsv` tags; `passages/<name>.txt`), counted by grep as files matching. Many rooms call a widget for their body, so every count is a floor.

| what | CoT |
|---|---|
| words a screen, markup stripped | median 64.5, p75 112 (field median 82, C770) |
| button labels | 285 read; median 3 words ("Grab a coffee", "Study", "Do a yoga routine") |
| a cost shown (`<<dtime>>`, `<<dalterneed>>`) | 97 of 126 |
| a planned date or an opportunity can start here (`<<godate>>`, `<<opportunities>>`) | 62 of 126 |
| the crowd read (`$peopleatlocation`) | 19 of 126 |
| an activity draws an event pool (`setup.Events.passage`) | 29 of 126 |
| a clothes check at the door (`clothes_ok`) | 22 of 126 |
| pictures (any image or video markup) | 0 of 126 |

## The shape

Each rule is marked **measured** or **LO's choice**.

1. **The identity line is the same every visit.** It says what the place is and who uses it. *Measured:* CoT's BangCoffee opens "You're inside BangCoffee: a preppy coffeehouse that serves baked goods, desserts and overpriced coffee. Some students like to study here, preferring the atmosphere here to their dorms or the library." (C769, C794)
2. **A person at a place is their face, never a room-text line** (C795, C804). The engine draws the faces of who is there (`present_faces`, and the badges on the nav cards), read from their rows; the room text does not add a line per person. An unnamed crowd line is allowed, not required. An open place with nobody there still says why ("Nobody's behind the counter."). Any line that names someone names only who `scripts/who_is_where.py` puts there at that minute (L106). *LO's choice* (LO, 2026-11-24: "We can drop it one line per person rule. Yes go ahead"), backed by L5 (LO: "scenes over room text"). *Measured in CoT:* no room carries a line per named person. 19 of 126 location passages read the unnamed crowd (`$peopleatlocation`; BangCoffee's barista is "checking their phone." under 8 people and "looking harried." from 8), named people are met through menus (`DiningHallMenu.txt`, `ParkSocialMenu.txt`, `BarTableMenu.txt`, all via `setup.people.sort_for_socialization`), and one special room, `BFFDorm.txt` (line 6), says whether the roommate is there.
3. **The menu holds only needs and systems; a person is their face on the screen** (C776, C777). A person's actions are not room buttons: they sit in that person's own menu, behind their face (`craft/people.md` rule 10). *Measured:* BangCoffee's menu is coffee and "Use restroom" (needs; `<<bathroom>>`, defined in `GlobalWidgets.txt`), "Study" and "Use laptop" (systems). Its `<<godate>>` starts a date she planned earlier (`HangoutWidgets.txt`, lines 1-26); it is not a talk button. CoT's people come from the People Here list (`StoryCaption.txt`, lines 585-596), then the person's card with "Talk to her" (`DisplayNPCWidgets.txt`, lines 33-68). Never a browse list of objects (C773). *LO's choice* for faces, not buttons (relayed 2026-11-23).
4. **Short labels; money shown when it's a spend, never time or energy** (C758, C953). Pay she earns stays off the button (C954). *Measured:* median 3 words; CoT shows a cost in 97 of 126, time included. Leaving time and energy off is *LO's choice* (LO, 2026-11-24: "Beside choice i dont want to show time and energy show money if needed"; "Room buttons too").
5. **"Not now" says why.** A button that can't be used says what's missing: "You really aren't that thirsty right now." (CoT, BangCoffee). Never "Nothing to do here" (C762). *Measured* in CoT; *LO's choice* for the rest.
6. **Every open place has one thing she can do alone** (`plan.md` §6). This is stricter than C738, which allows "nothing to do here right now" in an open empty room. *LO's choice* (L147).
7. **Streets or quads are hubs; places sit off them,** and a thoroughfare only routes (C738, C808, C811). *Measured:* CoT's streets are places of their own ("You are on Emerson Road. A large academic building is here…"), and the buildings open off them (Emerson Road, Bancroft Lane, Hallowell Road).
8. **Short screens,** around CoT's median of 65 words. *Measured.*
9. **Two rules from DoL only, not CoT:** a first-visit screen only for something true once (C771), and one anchor place that holds about 30% of the place prose (C707, C739). *Measured in DoL;* CoT is not their source.
10. **A place hidden until a flag is pointed at** (L170). A place with `hidden_until = { flag = … }` stays off the menu until the flag is set, so the step that sets it is pointed at on the Quests page: the flag itself, or a flag set on the same choice (`met_zoe` beside `zoe_place_known`), is a `when` on a hint step. `check.py`'s `pages` check is red otherwise. *LO's choice* (LO, typed in main-lean 2026-11-25: "Go ahead").

The picture of a place comes from `craft/media.md` (one picture of her, tier 0), measured across the top games as 41% of room screens (C1249). CoT is not its source: its location screens carry none.

## Worked example

Roles: her mom and her step-father. LO approved these words, with the names swapped for roles.

**Kitchen**
> The kitchen: a small table, a stove where only two rings light, your step-father's mug always by the sink. Everyone ends up in here sooner or later.

Who is there: Mom's and the step-father's faces, by their rows; no line for either in the room text (rule 2).
- Nobody: "Nobody's here. The fridge hums."

Buttons: Eat something · Do the dishes · Leave the kitchen. (Eating still takes 20 minutes and gives 15 energy; the label says neither.) When Mom is here, her face is on the screen, and it opens her menu (`craft/people.md`).
After three meals, Eat something says: "You're not hungry right now."

## Not this

- "Nothing to do here right now." Every open place has one thing she can do alone (L147; first_term_lean).
- A room-text line per person: "Mom's at the stove, humming." She is her face (rule 2; LO, 2026-11-24).
- Any line naming someone whose rows don't put them there (L106).
- A browse list of objects: "Look at the fridge", "Look at the window" (C773).
- A Talk button per person on the room menu. The person is their face; Talk is inside their menu (`craft/people.md` rule 10).
- A label that prints time or energy: "Eat something (20 min, +15 energy)" (C953; LO, 2026-11-24).
