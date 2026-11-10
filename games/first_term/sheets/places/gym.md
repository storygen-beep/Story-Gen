# [READY] Place — Gym (on Your Street)
> Changed 2026-11-10 (DECISIONS 227): one shared shower room for men and women replaces the women's showers, the walk-in and the men's-showers dare (LO: "make a common shower for men and women, she doesnt have any choice to bath here"; "Not money they offer"). New section at the end; it replaces DECISIONS 226's men's room and walk-in split. Re-signed by LO 2026-11-10 ("Sign them").
> Changed 2026-11-10 (DECISIONS 226): a fourth room, the men's locker room and showers (LO: "I say as men's locker room too and shower too. Sauna stays same for both."; the pitch: "Yes i like it"), and the shower walk-in split in two by her level. New section at the end. Re-signed by LO 2026-11-10 ("Sign them").

> New 2026-11-10 (DECISIONS 225). Signed by LO 2026-11-10 ("Sign them").
> LO, 2026-11-10: "I want gym outside college in the streets. A gym membership too. Gym clothes are to be required for
> workouts. And some more room gym can have. Gym trainer too." Then: "We want to shift campuss gym to street gym. Not
> have both." · "Dont count hrs count days" · "Only locker room and showers and. Sauna and gym thats it" · prices "1yes" ·
> hours "gym can run in the day time all day till 9 pm ... independent of campuss or ither systems" · "yes she can walk
> in gym cloths in streets" · the sports bra alone on the street: "Yes, from 20".
> This sheet replaces `campus_gym.md`. Everything the campus gym had moves here (the table "What moves from campus").

| row | answer |
|---|---|
| kind | an area: `is_container`, three rooms (below); the Gym page opens on the gym floor (`default_entry`) |
| ENTERED FROM | street · 5 minutes on foot (`crossing_costs` time 5, guess) |
| labels — what kind of place | `zone:street`, `public` |
| hours | every day 06:00–21:00, on its own clock: no tie to campus or any other system |
| closed text | "The gym's shut. Opens at six." |
| hidden until | no |
| fill — word budget | 2,500 words (the campus gym's 1,500, plus the locker room and the sauna) |
| door | no: the desk is inside, on the floor |
| dress code or wanted state | to walk there: the street's rules, plus the sports-bra row (below) · to work out: gym clothes (below) · the sauna: a towel |

## The membership (a pass, counted in days)

The engine's own pass counts days: buying one stores `expires_day = today + days` (`v2.py:5741`), and the condition
`pass is_active` reads it (`v2.py:5324`). No hours, no flag timer.

| pass | price | lasts | where she buys it |
|---|---|---|---|
| day pass (`gym_day`) | $5 | today only (0 days: ends at midnight) | the desk, on the gym floor |
| 30 days (`gym_month`) | $40 | 30 days, the day she buys it plus 30 | the desk |

- With no pass active, the floor shows only the desk: "Buy a day pass ($5)" and "Buy 30 days ($40)". The desk line says
  what she needs: "Members only past the desk. Five for today, forty for the month."
- With a pass active, the desk line says the days left: "You're good for another 12 days." On its last day: "Last day
  on your card. Forty when you want the next month."
- She can't buy a second pass while one is active (the button hides), so a pass is never wasted.
- Rent is $75 to $100 a week and café shifts make about $205–245 (`money_pressure.md`), so $40 a month is a real cost,
  not a wall.

## Gym clothes (what "Work out" needs)

"Work out" shows only with a pass active **and** a gym top **and** a gym bottom on. Otherwise one greyed line:
"Not in jeans. Change in the locker room." (it names what she has on: jeans, a skirt, a dress).

| slot | counts as gym clothes |
|---|---|
| top | gym tank · T-shirt · the sports bra with nothing over it |
| bottom | track pants · leggings · tiny gym shorts · sheer leggings |

Each piece is checked by item (`clothing_item ... equipped`), because `worn_type` reads only the main garment
(`v2.py:2029`); `college.py:990` already checks the tank this way.

**On the street in gym clothes.** A tank or tee with any gym bottom already passes the street's rules. The sports bra
with nothing over it gets a new street row: from Exhibitionism 20 the sports bra counts as her top (only the sports bra,
not any bra); below 20 she needs a tank or tee over it: "Not in just the sports bra. Not yet. (Needs Exhibitionism 20.)"
The street's other rows stand.

## The three rooms

### Gym floor (`gym_floor`, default entry)

| auto-fires | who is here, and when | things to do alone | ways out |
|---|---|---|---|
| none | Dex: Mon–Sat 10:00–20:00 (his sheet) · Jake and his team: Tue, Thu 15:00–17:00, once she has Jake's number | the desk (passes) · work out | the locker room · the sauna · Your Street |

| row | kind | system | cost and effect, with op | BRAKE |
|---|---|---|---|---|
| the desk | work | money | money add −5 or −40 · the pass | hidden while a pass is active |
| work out | work | wardrobe | 60 min · energy add −15 · the five clothing steps (below) | pass active · gym clothes · `worked_out`, once a day |
| Dex | person | Dex's ladder | inside his portrait (his sheet) | his steps' own |
| Jake, training | person | Jake's ladder | inside his portrait, as before (`npc_jake.md`) | `jake_gym_today`, once a day |
| Find someone for Zoe's party | work | Zoe's crowd | as before (below) | once a day |

### Locker room and showers (`gym_locker`)

Needs a pass active. Without one: "Members only. The desk's out front." (`entry_conditions`, `blocked_message`).

| auto-fires | who is here, and when | things to do alone | ways out |
|---|---|---|---|
| none | other members (walk-ins) · Jake, after training (his locker-room act) · Dex, after closing (his step 5) | change clothes · shower | the gym floor |

| row | kind | system | cost and effect, with op | BRAKE |
|---|---|---|---|---|
| change clothes | need | wardrobe | the wardrobe (`wardrobe_location`) | none needed |
| shower | need | hygiene | 15 min · hygiene add +50 | `gym_shower_today`, once a day (guess) |
| a woman walks in on her | — | exhibitionism | a walk-in on the shower, 1 in 4, Exhibitionism 20: "Keep washing." +1, cap 39 · cover up 0 | once a day |

### Sauna (`gym_sauna`)

Needs a pass active, and a towel: "Towel only in there." Leaving it, she dresses again in the locker room (the
park's towel rule stays: no street in a towel).

| auto-fires | who is here, and when | things to do alone | ways out |
|---|---|---|---|
| none | two older regulars, any open hour · Dex at his step 4 | sit in the sauna | the locker room |

| row | kind | system | cost and effect, with op | BRAKE |
|---|---|---|---|---|
| sit in the sauna | need | energy | 20 min · energy add +10 | `sauna_today`, once a day |
| the towel slips | — | exhibitionism | an accident on sitting, 1 in 4: "Fix it fast." 0 · from Exhibitionism 60 "Let it slip." +1, cap 79: three seconds of her bare tits before she pulls it up | `gym_accident_today`, one gym accident a day |

**No public topless** (DECISIONS memory, 2026-11-08): the slip is a flash, three seconds, then the towel goes back up.
She never sits there topless.

**After closing (Dex's step 5).** The gym shuts at 21:00 for her. Only Dex's after-hours button takes her into the
locker room 21:00–22:00, from his text (`npc_dex.md`); the building's hours stay 06:00–21:00. The build checks how the
engine lets a scene stay in a closed room (a scene she is already in, entered before 21:00, or a room hours row gated
on `dex_step`), and says which before writing it.

## What moves from campus

| on campus now | goes to | what changes |
|---|---|---|
| Work out, the five clothing steps, the mirror wall | gym floor | needs a pass and gym clothes; the lines stay |
| the three accidents (see-through leggings, the strap, the shorts) | gym floor | none |
| changing clothes (the locker room) | locker room | `wardrobe_location` moves to `gym_locker` |
| Jake's team training, Tue/Thu 15:00–17:00 | gym floor | his line: "Coach moved us off campus. Better weights." |
| Jake in the locker room (A1) | locker room | none |
| the team walk-in (Tue/Thu 15:00–15:15) | gym floor | none |
| Zoe's crowd ask at the gym | gym floor | "from the gym" stays; the flag key `crowd_campus_gym` stays so old saves keep it |
| the desk guy's warning "This is a college gym." | gym floor | "Hey. Watch it. People bring their kids in here." |
| the gym on the campus list | — | gone; campus keeps its other rooms |
| the four looks' repeat lines (DECISIONS 209, 211) | gym floor | none |

**Campus talk** still pays at the gym: the students train here, Jake's team among them. Lines that say "on campus" or
"college gym" are rewritten to "the gym".

The five clothing steps and three accidents, as signed in `campus_gym.md` (DECISIONS 198, 203, 205), unchanged:

| step | what she trains in | lock to wear | her button, pay |
|---|---|---|---|
| Normal | track pants and a T-shirt | none | Work out, 0 |
| Cute | leggings, or the gym tank | none | under 20, in leggings: "Squat facing the mirror wall." +1, cap 19 |
| Showy | the sports bra with nothing over it | the garage hold only | at 20: "Work out, and let them look." +1, cap 39, campus talk +1 |
| Slutty | tiny gym shorts | Exhibitionism 40 | at 40: "Stretch on the mats facing the rack." +1, cap 59, campus talk +1 |
| Slutty+ | sheer leggings | Exhibitionism 60 | at 60: "Do your squats anyway." +1, cap 79, campus talk +1 |

## Rows a gate needs

| row | gate |
|---|---|
| work out, every open hour, with a pass | a destination is never open and exit-only (the desk is always there) |
| Dex's and Jake's rows have a hub | standing surface |
| Dex's steps are inside his portrait | a person's scene is inside their portrait (DECISIONS 224) |

## Why — the source of each key choice

| key choice | source |
|---|---|
| one gym, on the street; the campus gym gone | LO, 2026-11-10 |
| three rooms: floor, locker room and showers, sauna | LO, 2026-11-10 |
| a pass counted in days, $5 a day and $40 for 30 | LO, 2026-11-10 ("Dont count hrs count days", "1yes") · the engine's pass (`v2.py:5732`) · `templates/cards/gym_body.md` (a membership is a pass) |
| open 06:00–21:00 every day | LO, 2026-11-10 · CoT's gym runs 6–22 (`gym_body.md`) |
| gym clothes needed to work out | LO, 2026-11-10 · IHOH needs leggings or yoga pants (`gym_body.md`) |
| the sports bra alone on the street from 20 | LO, 2026-11-10 ("Yes, from 20") |
| the walk 5 minutes; the shower once a day; the sauna's energy +10 | guess |
| the trainer is Dex | LO, 2026-11-10 ("you can decide one"; then "Yes, go ahead") · `npc_dex.md` |

## Built 2026-11-10 (DECISIONS 225): where the build differs from this sheet

Each one was forced by the engine or a gate, and each keeps what the row above asked for.

- **The day pass is a check-in, not a pass.** Every room past the desk reads one flag, `gym_in_today` (cleared at
  midnight), so the desk sets it two ways: "Show your card." while the 30-day pass is active, or "Buy a day pass ($5)."
  (money −5). Conditions have no OR, and two passes would have doubled every button. The 30 days are the engine's pass
  `gym_month` ($40, counted in days).
- **Days left show in the sidebar** ("Gym: 12d"), not in the desk's words: a line can't print the number. The desk
  says "Card? Cheers. You're in." while the card is good and "Your card's run out." after.
- **Not in gym clothes is a line on the Work out screen**, by what she has on ("Not in jeans.", "Not in a dress.",
  "Not in that top." …), with only "Not today." under it. Not a greyed button: a greyed button can't say which piece
  is wrong.
- **The sauna's door is in the locker room**, not on the floor: she goes in a towel, and the floor's rules don't allow
  a towel. The locker room has no dress rules (she strips and showers there).
- **The locker room has "Strip down to a towel."** (2 minutes) so the sauna is one step away; the wardrobe still works.
- **Zoe's crowd flag** is `crowd_gym_floor` now: the ask names its flag after its room. A save from before the move
  loses the "Gym girl!" line at the party; nothing else.

## The men's locker room, and the shower walk-in split (2026-11-10, DECISIONS 226)

LO, 2026-11-10: "I say as men's locker room too and shower too. Sauna stays same for both." Then, on the pitch: "Yes i
like it". The gym has four rooms now. The women's locker room stays hers; the sauna stays mixed.

### Men's Locker Room (`gym_mens_locker`)

A door off the floor, beside the women's. Benches, lockers, a row of open showers. The door shows on the floor; below
the gate it's blocked: "That's the men's."

| auto-fires | who is here, and when | things to do | ways out |
|---|---|---|---|
| none | men showering, any open hour · Jake's team, Tue and Thu after training (17:00 on) | Jake's locker-room act · the dare · Dex's repeat, one variant | the gym floor |

| row | kind | system | cost and effect, with op | BRAKE |
|---|---|---|---|---|
| Jake in the locker room (A1) | person | Jake's ladder | moves here from the women's: as signed (Bold "Get on your knees." +1 cap 59 · Hungry "Against the lockers." +1 cap 79 · "Not here, Jake." 0) | as before, once a day |
| "Walk through the men's showers." | work | exhibitionism | Watched (Exhibitionism 60), in a towel, checked in: six or so men under the showers stop and look; halfway the towel slips (a flash, then it's back up; never naked the whole way) · exhibitionism +1, cap 79 · campus talk +1 (the team trains here) | once a day (`mens_walk_today`) |
| Dex, when it's empty | person | Dex's repeat | one more variant of "Go to the locker room with him." (`npc_dex.md`) | his repeat's own |

**Who's in there when she walks through:** Tue and Thu 17:00–18:00, Jake's team ("Coach'll kill us." · Jake, if his row
has him, says her name); any other open hour, strangers.

**Who sees it:** a group of men seeing her in a towel that slips is stage 4, Watched (the-heat-ladder.md H1). No
public topless: the slip is a flash, the towel goes back up (first_term rule, 2026-11-08).

### The shower walk-in, split by her level

| her answer | gate | pay |
|---|---|---|
| "Turn to the wall and cover up." | none | 0 |
| "Keep washing." She doesn't cover up, but keeps her back to her: the woman gets her ass and the water running down it | Exhibitionism 20 (Daring) | +1, cap 39 |
| "Turn round and let her look." She faces her, naked, and soaps her tits slowly while she watches | Exhibitionism 60 (Watched) | +1, cap 79 |

Why: a stranger seeing her full front, by her choice, is Watched (60) on the heat ladder (the scene reader, 2026-11-10);
standing naked in the women's showers is ordinary, so 20 still gets its own act, back turned.

**Built 2026-11-10 (DECISIONS 226), where it differs:** the men's door is on the back corridor off the women's locker
room, beside the sauna's, not off the floor: she walks there in a towel, and the floor allows no towel. Below the gate
the engine hides the door rather than showing "That's the men's." (the line is its blocked message, for a save that
lands there).

## The shared shower room (2026-11-10, DECISIONS 227)

LO, 2026-11-10: "we can remove this and make a common shower for men and women, she doesnt have any choice to bath here";
"it isnt being complete naked on streets. She is taking shower in a bathroom for both men and women"; "they can also
offer her things, she can accept and give them her hand and body too. Here she can have multiple mens or one men too or
a couple or a women or multiple women"; "Not money they offer"; the plan: "Yes".

**This replaces** the women's showers, the woman who walked in on her (DECISIONS 226's split), the men's-showers dare and
the men's locker room as a room she enters. The women's locker room is for changing only. The men's locker room stays in
Jake's lines; the team showers in the shared room.

**The room (`gym_showers`):** off the back corridor, beside the sauna, entered from the women's locker room in a towel,
checked in. "Everyone showers together. It's that kind of gym." The only showers in the gym. Hygiene +50, 15 minutes,
once a day. A bathroom, not the street: being naked here is not public topless (LO, 2026-11-10).

**While she showers, by her level** (Exhibitionism; a look that happens to her is stage 1, her bare body to strangers by
choice is stage 4, the-heat-ladder.md H1):

| her level | what she does | pays |
|---|---|---|
| Covered (0) | showers fast, facing the wall, an arm over her tits | 0 |
| Daring (20) | stops covering, her back to the room | +1, cap 39 |
| Showing (40) | turns round and faces them while she rinses | +1, cap 59 |
| Watched (60) | soaps herself slowly for them | +1, cap 79 |

The men's lines get bolder with her level: looking away, staring, "Need a hand with that?".

**Someone hits on her** (1 in 3 showers, once a day). Who: one man, one woman, a couple, two men, two women, or a group.
Nobody pays (LO: "Not money they offer"); what they offer is themselves.

| what they want, and her yes | gate | pays |
|---|---|---|
| "No." | none | 0 |
| they wash her: their hands on her back, then her tits | Bold (Corruption 40) | +1 corruption, cap 59 |
| her hand on him or her, the room otherwise empty | Bold (Corruption 40) | +1 corruption, cap 59 |
| her body, one person | Hungry (Corruption 60) | +1 corruption, cap 79 |
| a couple, or two of them, with others watching | Corruption 60 and Exhibitionism 60 (a mixed act, H1) | +1 to each, cap 79 |
| a group | stage 5 | locked: "(Next release)" |

**LO's calls on the reader's two heat points (2026-11-10, "Go ahead with your picks"):** "Turn round and face them."
stays at Exhibitionism 40 (a shared shower, where everyone is naked: his bathroom ruling). Being washed by a couple, two
of them or a group, with the room watching, needs Corruption 40 and Exhibitionism 40 and pays both (+1 each, cap 59);
alone with one person it stays Corruption 40.
