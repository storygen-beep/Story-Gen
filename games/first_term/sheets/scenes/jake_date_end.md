# [READY] Scene — jake_date_end

> **Changed 2026-11-01, re-signed by LO 2026-11-02** ("Signed, go ahead and build"; DECISIONS 124, the heat ladder a2): its gate or pay changes; the row is in `sheets/HEAT_LADDER_A2.md`.

> **New 2026-11-01, signed by LO 2026-11-01 ("Continue")** (DECISIONS 99–119). Jake's hot repeatable, "The end of a date", from his
> signed release-1 ladder (`sheets/people/npc_jake.md`). Reworks the built canvas `jake_saturday_date`
> (`iterations/002/build_scripts/jake.py:114`; its sheet is marked reworked). Five entries by `v2-prose`, measured.

| row | answer |
|---|---|
| where · when | outside the house after a date, Sat 22:00–00:00, once a week (as built: `jake_date_went` tonight) |
| gate | `jake_step` gte 3 (was gte 4) · the date tonight · the car by stage (DECISIONS 124): the kiss Corruption 40–59, cap 59; his hand or hers Corruption 60, cap 79 |
| tiers | **Curious** (Corruption under 40): `car_low` · **Bold** (Corruption 40), before his step 4: two yeses, `car_his` · `car_hers` · **after step 4**: "Come up." → `sneak` (a two-entry pool, `memory = "seen"`, `seen_weight = 0`) |
| pays | `car_low`, `car_his`, `car_hers`: corruption add +1 · exhibitionism add +1 (seen: the street, Laura's window; `meters.md` rule 3) · `sneak`: corruption add +1 (behind her door) · each under her stage cap |
| the near-catch | after step 4, one night in four: the `door` exit rolls `jake_catch_roll` (random 1–8, `v2.py:7328`); 1: Laura's door opens across the landing · 2 (Ryan's knock code set, `ryan_knock_code`): two knocks on the wall. Each is one line after the `sneak` entry; they don't stop |
| the no | "Goodnight, Jake." (as built: "Goodnight, gorgeous. Same time next week.") |
| locked | "Jake, further. (Needs Corruption 60.)" (the built side-of-the-house button, said as the number, DECISIONS 90) |
| the crude-word ceiling | the car: his middle column (ass, tits, cock) with plain anatomy (nipples, clit, wet, thighs, balls) · `sneak`: Jake's late column: cock, fuck, cum (signed with the proposal, LO 2026-11-01), with ass, tits and plain anatomy (nipples, clit, wet, thighs) · no pussy, cunt |
| truth | weekly: no "first time", no "again", no counting (`sneak` a: "He knows which stair creaks", true after step 4 only, where it shows) |
| her_line_low · her_line_high | low: "He's normal. This is normal." · high: "You want Ryan to hear every second of it." | The low line sits in `car_low`. |

## The car, and two truth fixes

- **Mark's TV:** the proposal's car scene has "Mark's TV light in the window". Mark sleeps Saturday 22:00–00:00
  (`npc_mark.md`, schedule); it is Laura waiting up in the living room (`npc_laura.md`, Sat 22:00–00:00). The beat says Laura.
- **The car home:** the built date walks her home (`jake.py:103-104`, "walks you the long way home", "You walk home
  through the park"). For the car to be outside the house, those two lines become "drives you home the long way" and
  "He drives you home through the park, slowly." Mine; confirmed by LO 2026-11-01 ("Continue").

## Branch map — one row per screen

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op |
|---|---|---|---|---|
| `door` | Jake parks outside the house, engine off | no | Curious: "Kiss him." → `car_low` · Bold, before step 4: "Your hand. Now." → `car_his` · "Lean back." → `car_hers` · after step 4: "Come up." → `sneak` · "Goodnight, Jake." → `night` · locked: "Jake, further. (Needs Corruption 60.)" | after step 4, "Come up.": `jake_catch_roll` set random 1–8 |
| `car_low` / `car_his` / `car_hers` | below | yes | "Goodnight, gorgeous." → the hall | the pay |
| `sneak` | one of a, b; then the near-catch line on a roll of 1 or 2 | yes | "Let him out before dawn." → her room | corruption add +1 |
| `night` | as built | no | "Go in." → the hall | `jake_date_booked` set false (on every exit) |

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

## Why — the source of each key choice

| key choice | source |
|---|---|
| the tiers, the pays, one night in four | `proposals/JAKE_R1_LADDER.md`, "His hot repeatable" (signed 2026-11-01) |
| Laura, not Mark, in the window | the schedules (`npc_mark.md`, `npc_laura.md`) |
| the car home, the near-catch lines, the 1–8 roll | mine, confirmed by LO 2026-11-01 ("Continue") |
