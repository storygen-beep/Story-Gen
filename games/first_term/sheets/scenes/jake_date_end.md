# [READY] Scene — jake_date_end

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign.

> The signed plans behind this page: `proposals/COPY_FIXES_A.md`.

> **Changed 2026-11-01, re-signed by LO 2026-11-02** ("Signed, go ahead and build"; DECISIONS 124, the heat ladder a2): its gate or pay changes; the row is in `sheets/HEAT_LADDER_A2.md`.

> **New 2026-11-01, signed by LO 2026-11-01 ("Continue")** (DECISIONS 99–119). Jake's hot repeatable, "The end of a date", from his
> signed release-1 ladder (`sheets/people/npc_jake.md`). Reworks the built canvas `jake_saturday_date`
> (`iterations/002/build_scripts/jake.py:114`; its sheet is marked reworked). Five entries by `v2-prose`, measured.

| row | answer |
|---|---|
| where · when | the front door after a date, Wed and Sat 22:00-00:00, once a day |
| want | his hand on her knee all the way home |
| next step | the car, by her stage; after step 4, "Come up." (Saturday) |
| hook | "Goodnight, gorgeous. Saturday?" (or "Wednesday?"): the next date |
| gate | his step 3+ · a date tonight · the car by Corruption: 40-59 the kiss, 60 his hand or hers |
| tiers | **Curious** (Corruption under 40): `car_low` · **Bold** (Corruption 40), before his step 4: two yeses, `car_his` · `car_hers` · **after step 4**: "Come up." → `sneak` (a two-entry pool, `memory = "seen"`, `seen_weight = 0`) |
| pays | the kiss: Corruption +1, Exhibitionism +1 (cap 39) · hands: each +1 (cap 79) · the sneak: Corruption +1 (cap 59) |
| the near-catch | after step 4, one night in four: the `door` exit rolls `jake_catch_roll` (random 1–8); 1: Laura's door opens across the landing · 2 (Ryan's knock code set, `ryan_knock_code`): two knocks on the wall. Each is one line after the `sneak` entry; they don't stop |
| the no | "Goodnight, Jake." → he walks backwards down the path |
| locked | none: the build shows no locked button; his card ends "Jake, further. (Next release)" |
| the crude-word ceiling | the car: his middle column (ass, tits, cock) with plain anatomy (nipples, clit, wet, thighs, balls) · `sneak`: Jake's late column: cock, fuck, cum (signed with the proposal, LO 2026-11-01), with ass, tits and plain anatomy (nipples, clit, wet, thighs) · no pussy, cunt |
| truth | weekly: no "first time", no "again", no counting (`sneak` a: "He knows which stair creaks", true after step 4 only, where it shows) |
| her_line_low · her_line_high | low: "He's normal. This is normal." · high: "You want Ryan to hear every second of it." | The low line sits in `car_low`. |

## The car, and two truth fixes

- **Mark's TV:** the proposal's car scene has "Mark's TV light in the window". Mark sleeps Saturday 22:00–00:00
 (`npc_mark.md`, schedule); it is Laura waiting up in the living room (`npc_laura.md`, Sat 22:00–00:00). The beat says Laura.
- **The car home:** the built date walks her home (the build , "walks you the long way home", "You walk home
 through the park"). For the car to be outside the house, those two lines become "drives you home the long way" and
 "He drives you home through the park, slowly." Mine; confirmed by LO 2026-11-01 ("Continue").

## Branch map — as built (2026-11-03)

One row per exit. Read from the build; it replaces the drafted map.

**`jake_saturday_date`** — Front Door · Wed/Sat 22:00-00:00 · Jake there · needs `jake_date_went` · under 6h since `jake_date_went` · Jake's step 3+ · repeatable · 1 a day

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `door` | All the way home Jake's hand has been on your knee, and it's still there as … | no | "Kiss him." (Corruption 40+ · Corruption under 60 · Jake's step 3+) → `car_low` | — |
| | | | "Your hand. Now." (Corruption 60+ · Jake's step 3+) → `car_his` | Hygiene -10 · costs Energy 10 |
| | | | "Lean back." (Corruption 60+ · Jake's step 3+) → `car_hers` | Hygiene -10 · costs Energy 10 |
| | | | "Come up." (Jake's step 4+ · Sat) → `sneak` | A close call rolls 1-8 |
| | | | "Goodnight, Jake." → `night` | — |
| `car_low` | Jake kills the engine outside your house and reaches for you across the seats. | yes | "Goodnight, gorgeous." → Hall | Corruption +1 (cap 39) · Exhibitionism +1 (cap 39) · `jake_date_booked` cleared · `late_date` set · `came_home_late` set |
| `car_his` | Jake kills the engine outside your house and the street lamp lights the whole car. | yes | "Goodnight, gorgeous." → Hall | Corruption +1 (cap 79) · Exhibitionism +1 (cap 79) · `jake_date_booked` cleared · `late_date` set · `came_home_late` set |
| `car_hers` | Jake parks outside your house and kills the engine under the street lamp. | yes | "Goodnight, gorgeous." → Hall | Corruption +1 (cap 79) · Exhibitionism +1 (cap 79) · `jake_date_booked` cleared · `late_date` set · `came_home_late` set |
| `sneak` | You go up the stairs in the dark with Jake right behind you. | yes | "Let him out before dawn (5h)." → Your Room | Corruption +1 (cap 59) · `jake_date_booked` cleared · `late_date` set · `came_home_late` set |
| `night` | He kisses your hand like an idiot and walks backwards down the path. | no | "Go in." → Hall | `jake_date_booked` cleared · `late_date` set · `came_home_late` set |

## The entries, written

Written by `v2-prose` and measured by `gates.py --beat`, 2026-11-01. Fixes after: "cums" / "cum" as a verb became "comes" / "come" (as Ryan's batch); her high line in `bed` came back as speech and is now her thought; both re-measured.

**`car_low`** (Curious) · 131 words · explicit words 5 · median sentence 11 · act rungs: hands

> Jake kills the engine outside your house and reaches for you across the seats. His mouth is on yours, hungry, his tongue pushing in. His big hand finds your tits through your top and squeezes. Your nipples go hard under his thumb. "God, you're gorgeous," he says into your neck. Across the lawn the living-room window glows blue, where Laura waits up with the TV. You look at it once. He's normal. This is normal. Then both his hands slide down to your ass and haul you half into his lap. His cock is hard in his jeans, pressed up under your thigh. You grind down on it and he groans into your mouth. The windows fog. His fingers dig into your hips and pull you down tighter on his cock.

**`car_his`** (Bold) · 131 words · explicit words 4 · median sentence 9 · act rungs: hands. The tool flags its last sentence as carrying no list word ("fingers", "thighs"); it is on the body

> Jake kills the engine outside your house and the street lamp lights the whole car. "C'mon, gorgeous. Right here." His big hand pushes down inside your clothes, flat on your belly, then lower. Two fingers find your clit and rub it fast. Then they slide inside you, deep. You gasp and grab his shirt. His other hand shoves up under your top and squeezes your tit, his thumb rolling your nipple. "God, you're so wet." His fingers pump harder. Your thigh jams against the door. Your hips buck off the seat into his palm. You come on his hand, shaking, your moan pressed into his shoulder. A car rolls past and its headlights sweep over you both. His fingers are still inside you, and your thighs clamp tight around his wrist.

**`car_hers`** (Bold) · 136 words · explicit words 5 · median sentence 9 · act rungs: none named ("stroke", "comes" are not on the list)

> Jake parks outside your house and kills the engine under the street lamp. You lean back, then reach over and open his jeans. His cock is already hard when you pull it out. "Hands on the wheel," you tell him. He grabs it. You stroke him slow, base to tip, until his hips lift off the seat. "@player," he says. "Oh god, @player." One hand leaves the wheel to find your tits under your top. He squeezes, his thumb dragging over your nipple. You let him, but you go faster. A man walking a dog stops on the pavement and looks in. You don't stop for him. Jake's thighs shake. His balls pull tight. He groans, head back on the seat, and comes hot over your hand. You keep stroking his cock slow while he pants.

**`sneak` a** (after step 4) · 133 words · explicit words 6 · median sentence 9 · act rungs: hands, vaginal, finish

> You go up the stairs in the dark with Jake right behind you. He knows which stair creaks and steps over it. Your door clicks shut. He bends you over your bed and pulls your clothes down to your thighs. His jeans hit the floor. His hands grip your hips, and his cock pushes into you from behind, slow, then all of it. "Quiet, gorgeous," he whispers, grinning. Then he starts to fuck you hard. You bite your pillow so you don't moan. Your headboard knocks the wall, and Ryan's room is right on the other side. His hand slides round to your clit and rubs. You come with your face in the pillow, shaking. He grabs your ass, holds you down and comes deep inside you. His cum runs down your thighs.

**`sneak` b** · 140 words · explicit words 9 · median sentence 11 · act rungs: vaginal, finish

> You shut the door and push Jake down on your bed in the dark. He's grinning before his back hits the sheets. You climb on, already wet, and sink down onto his cock. You ride him slow, rolling your hips. His big hands find your tits, and his thumbs drag over your nipples. "Fuck, gorgeous," he says, way too loud. You clamp a hand over his mouth and ride him harder. The headboard knocks the thin wall. His hands drop to grip your ass and pull you down on every stroke. You grind your clit against him until your thighs shake. You come on his cock with your palm still over his mouth. He groans into your hand and holds your hips down hard. His cock pulses deep, and his cum fills you while you shake on top of him.

## The near-catch lines (mine, signed by LO 2026-11-01)

- **1, Laura's door:** "Across the landing a door opens. Light under yours. You both stop breathing. Then Laura's slippers go to the bathroom, and back, and her door shuts." · Jake, into your neck: "Your mom?" · @player: "Shh."
- **2, Ryan's knock:** "Two knocks on the wall. Slow. Ryan's code." · Jake: "What was that?" · @player: "Nothing. The pipes."

## The explicit beats, as built (2026-11-03)

Every screen the build counts as explicit (3+ words from the frozen list), word for word, with its measurement. It replaces the drafted text.

**`jake_saturday_date` · `car_low`** — 245 words · 9 counted: tits, nipple, tits, nipple, tits, nipple, ass, cock, cock · ceiling: the car: Jake's middle (ass, tits, cock) · the sneak: his late (cock, fuck, cum)

> Jake kills the engine outside your house and reaches for you across the seats. His mouth is on yours, hungry, his tongue pushing in. His big hand finds your tits through your top and squeezes. Your nipples go hard under his thumb.
>
> God, you're gorgeous.
>
> He says into your neck.
>
> Jake kills the engine outside your house and reaches for you across the seats. His mouth is on yours, hungry, his tongue pushing in. His big hand finds your tits through your dress and squeezes. Your nipples go hard under his thumb.
>
> God, you're gorgeous.
>
> He says into your neck.
>
> Jake kills the engine outside your house and reaches for you across the seats. His mouth is on yours, hungry, his tongue pushing in. His big hand finds your tits through your dress and squeezes. Your nipples go hard under his thumb.
>
> God, you're gorgeous.
>
> He says into your neck.
>
> Across the lawn the living-room window glows blue, where Laura waits up with the TV. You look at it once.
>
> He's normal. This is normal. Then both his hands slide down to your ass and haul you half into his lap. His cock is hard in his jeans, pressed up under your thigh. You grind down on it and he groans into your mouth. The windows fog. His fingers dig into your hips and pull you down tighter on his cock.
>
> The whole street can see the windows fogging up.
>
> Then stop breathing so hard.

**`jake_saturday_date` · `car_his`** — 409 words · 12 counted: clit, tit, nipple, moan, clit, tit, nipple, moan, clit, tit, nipple, moan · ceiling: the car: Jake's middle (ass, tits, cock) · the sneak: his late (cock, fuck, cum)

> Jake kills the engine outside your house and the street lamp lights the whole car.
>
> C'mon, gorgeous. Right here.
>
> His big hand pushes down inside your clothes, flat on your belly, then lower. Two fingers find your clit and rub it fast. Then they slide inside you, deep. You gasp and grab his shirt. His other hand shoves up under your top and squeezes your tit, his thumb rolling your nipple.
>
> God, you're so wet.
>
> His fingers pump harder. Your thigh jams against the door. Your hips buck off the seat into his palm. You come on his hand, shaking, your moan pressed into his shoulder. A car rolls past and its headlights sweep over you both. His fingers are still inside you, and your thighs clamp tight around his wrist.
>
> Jake kills the engine outside your house and the street lamp lights the whole car.
>
> C'mon, gorgeous. Right here.
>
> His big hand pushes down inside your clothes, flat on your belly, then lower. Two fingers find your clit and rub it fast. Then they slide inside you, deep. You gasp and grab his shirt. His other hand shoves up under your dress and squeezes your tit, his thumb rolling your nipple.
>
> God, you're so wet.
>
> His fingers pump harder. Your thigh jams against the door. Your hips buck off the seat into his palm. You come on his hand, shaking, your moan pressed into his shoulder. A car rolls past and its headlights sweep over you both. His fingers are still inside you, and your thighs clamp tight around his wrist.
>
> Jake kills the engine outside your house and the street lamp lights the whole car.
>
> C'mon, gorgeous. Right here.
>
> His big hand pushes down inside your clothes, flat on your belly, then lower. Two fingers find your clit and rub it fast. Then they slide inside you, deep. You gasp and grab his shirt. His other hand shoves up under your dress and squeezes your tit, his thumb rolling your nipple.
>
> God, you're so wet.
>
> His fingers pump harder. Your thigh jams against the door. Your hips buck off the seat into his palm. You come on his hand, shaking, your moan pressed into his shoulder. A car rolls past and its headlights sweep over you both. His fingers are still inside you, and your thighs clamp tight around his wrist.
>
> You're soaked. Right here under the street lamp, and you're soaked.
>
> Don't stop. Let them look.

**`jake_saturday_date` · `car_hers`** — 423 words · 16 counted: cock, tits, nipple, balls, cock, cock, tits, nipple, balls, cock, cock, tits, nipple, balls, cock, fuck · ceiling: the car: Jake's middle (ass, tits, cock) · the sneak: his late (cock, fuck, cum)

> Jake parks outside your house and kills the engine under the street lamp. You lean back, then reach over and open his jeans. His cock is already hard when you pull it out.
>
> Hands on the wheel.
>
> You tell him. He grabs it. You stroke him slow, base to tip, until his hips lift off the seat.
>
> @player.
>
> He says.
>
> Oh god, @player.
>
> One hand leaves the wheel to find your tits under your top. He squeezes, his thumb dragging over your nipple. You let him, but you go faster. A man walking a dog stops on the pavement and looks in. You don't stop for him. Jake's thighs shake. His balls pull tight. He groans, head back on the seat, and comes hot over your hand. You keep stroking his cock slow while he pants.
>
> Jake parks outside your house and kills the engine under the street lamp. You lean back, then reach over and open his jeans. His cock is already hard when you pull it out.
>
> Hands on the wheel.
>
> You tell him. He grabs it. You stroke him slow, base to tip, until his hips lift off the seat.
>
> @player.
>
> He says.
>
> Oh god, @player.
>
> One hand leaves the wheel to find your tits under your dress. He squeezes, his thumb dragging over your nipple. You let him, but you go faster. A man walking a dog stops on the pavement and looks in. You don't stop for him. Jake's thighs shake. His balls pull tight. He groans, head back on the seat, and comes hot over your hand. You keep stroking his cock slow while he pants.
>
> Jake parks outside your house and kills the engine under the street lamp. You lean back, then reach over and open his jeans. His cock is already hard when you pull it out.
>
> Hands on the wheel.
>
> You tell him. He grabs it. You stroke him slow, base to tip, until his hips lift off the seat.
>
> @player.
>
> He says.
>
> Oh god, @player.
>
> One hand leaves the wheel to find your tits under your dress. He squeezes, his thumb dragging over your nipple. You let him, but you go faster. A man walking a dog stops on the pavement and looks in. You don't stop for him. Jake's thighs shake. His balls pull tight. He groans, head back on the seat, and comes hot over your hand. You keep stroking his cock slow while he pants.
>
> Fuck. That guy saw. That guy totally saw.
>
> Good. Now he knows whose you are.

**`jake_saturday_date` · `sneak`** — 328 words · 16 counted: cock, fuck, moan, clit, ass, cum, cock, tits, nipple, fuck, ass, clit, cock, cock, cum, fuck · ceiling: the car: Jake's middle (ass, tits, cock) · the sneak: his late (cock, fuck, cum)

> You go up the stairs in the dark with Jake right behind you. He knows which stair creaks and steps over it. Your door clicks shut. He bends you over your bed and pulls your clothes down to your thighs. His jeans hit the floor. His hands grip your hips, and his cock pushes into you from behind, slow, then all of it.
>
> Quiet, gorgeous.
>
> He whispers, grinning. Then he starts to fuck you hard. You bite your pillow so you don't moan. Your headboard knocks the wall, and Ryan's room is right on the other side. His hand slides round to your clit and rubs. You come with your face in the pillow, shaking. He grabs your ass, holds you down and comes deep inside you. His cum runs down your thighs.
>
> You shut the door and push Jake down on your bed in the dark. He's grinning before his back hits the sheets. You climb on, already wet, and sink down onto his cock. You ride him slow, rolling your hips. His big hands find your tits, and his thumbs drag over your nipples.
>
> Fuck, gorgeous.
>
> He says, way too loud. You clamp a hand over his mouth and ride him harder. The headboard knocks the thin wall. His hands drop to grip your ass and pull you down on every stroke. You grind your clit against him until your thighs shake. You come on his cock with your palm still over his mouth. He groans into your hand and holds your hips down hard. His cock pulses deep, and his cum fills you while you shake on top of him.
>
> Downstairs the TV goes quiet. Laura's feet on the stairs. You both stop breathing. They stop halfway up, and go back down.
>
> Your mom?
>
> Shh.
>
> Two knocks on the wall. Slow. Ryan's code.
>
> What was that?
>
> Nothing. The pipes.
>
> Your bed's so loud. How is your bed this loud?
>
> Then fuck me quieter. Don't stop.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the tiers, the pays, one night in four | `proposals/JAKE_R1_LADDER.md`, "His hot repeatable" (signed 2026-11-01) |
| Laura, not Mark, in the window | the schedules (`npc_mark.md`, `npc_laura.md`) |
| the car home, the near-catch lines, the 1–8 roll | mine, confirmed by LO 2026-11-01 ("Continue") |
