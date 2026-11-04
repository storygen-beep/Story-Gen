# [REVIEW] Scenes — the sex scenes in the cold places (A1-A7)

> Changed 2026-11-04 to match the build; waits for LO's re-sign. The built-differently items are confirmed, DECISIONS 170.

> New 2026-11-03 (third alignment pass), written from the build; waits for LO's sign. The plan: `proposals/FIRST_TERM_HEAT_PROPOSAL_20261103.md`, part A (signed by LO 2026-11-03, DECISIONS 147: A1-A7 yes, A8 and A9 no; built in DECISIONS 149).

Each act in the build: an offer screen with a written no that pays nothing, then a shuffle bag of beats with a clip, paying her +1 capped at the stage top, once a day. Built differently from the proposal (DECISIONS 149), confirmed, DECISIONS 170: A6 and A7 hours are conditions, not schedules; A1 runs 16:30-16:45, A3 to 11:30, A2 to 12:45; A2 and A3 need the short skirt; A5's exit is "Slip out while she sleeps."

## A1 · `hub_jake_gym`

| row | answer |
|---|---|
| who | Jake |
| where · when | the gym, Tue/Thu after training, from "Wait for him after training." (16:30-16:45) |
| gate | after `jake_first_time` (his step 4) · Corruption 40; "Against the lockers." Corruption 60 |
| want | "Locker room's empty for ten minutes. Get in here." |
| next step | her mouth (Bold), or him fucking her against the lockers (Hungry) |
| hook | none in the build: the act repeats the next day |
| BRAKE | once a day (`jake_lockers_today`) |
| the written no | "Not here, Jake." → "Later, then. When Coach isn't next door." pays 0 |
| pays | Bold: +1 cap 59 · Hungry: +1 cap 79 · Jake has no meter |

**`hub_jake_gym`** — Gym · Jake there · needs `jake_number` · repeatable

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `a1_offer` | Training ends. | no | "Get on your knees." (Corruption 40+ · not `jake_lockers_today`) → `a1_mouth` | Corruption +1 (cap 59) · Hygiene -10 · `jake_lockers_today` set · costs Energy 10 |
|  |  |  | "Against the lockers." (Corruption 60+ · not `jake_lockers_today`) → `a1_lockers` | Corruption +1 (cap 79) · Hygiene -10 · `jake_lockers_today` set · costs Energy 10 |
|  |  |  | "Not here, Jake." → `a1_no` | — |
| `a1_mouth` | Jake kicks the locker-room door shut behind you. | yes | "Wipe your mouth. Go." → Campus | — |
|  |  |  | "Leave him to his shower." → Campus | — |
| `a1_lockers` | Jake spins you round and pushes you face-first into the lockers. | yes | "Go, before Coach comes." → Campus | — |
|  |  |  | "Leave him to his shower." → Campus | — |
| `a1_no` | He grins, slaps the door frame and jogs off after the team. | no | "Later." → Campus | — |

## A2 · `hub_zoe_canteen`

| row | answer |
|---|---|
| who | Zoe (Nadia or two Biology girls across the table) |
| where · when | the canteen at lunch, from "Slide in next to Zoe." (11:45) |
| gate | after `zoe_together` (her step 5) · Corruption 60 · a short skirt |
| want | "I said not here. I lied. Hold still, babe." |
| next step | her fingers under the skirt while the table talks |
| hook | none in the build: the act repeats the next day |
| BRAKE | once a day (`zoe_table_today`) |
| the written no | "Not here, Zo." → "Later, babe." pays 0 |
| pays | +1 cap 79 |

**`hub_zoe_canteen`** — Canteen · Zoe there · needs `zoe_met` · repeatable

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `a2_offer` | You slide in beside Zoe on the bench, close enough that her thigh is hot against … | no | "Let her." (Corruption 60+ · in short skirt · not `zoe_table_today`) → `a2_fingers` | Corruption +1 (cap 79) · Hygiene -10 · `zoe_table_today` set · costs Energy 10 |
|  |  |  | "Not here, Zo." → `a2_no` | — |
| `a2_fingers` | Zoe keeps eating fries with her left hand. | yes | "Finish your lunch." → Canteen | — |
|  |  |  | "Leave her to her lunch." → Campus | — |
| `a2_no` | She takes her hand back and steals a fry off your tray instead, grinning. | no | "Finish your lunch." → Canteen | — |

## A3 · `hub_jake_quad`

| row | answer |
|---|---|
| who | Jake and the team |
| where · when | the quad, from "Sit in his lap." (his quad hours) |
| gate | after `jake_first_time` · a short skirt · Exhibitionism 60; "Let him in." also Corruption 60 |
| want | "Forget later. Guys. Look at her." |
| next step | he shows her off; "Let him in.": his fingers in her |
| hook | none in the build: nothing reads `team_saw_quad` |
| BRAKE | once a day (`jake_quad_today`) |
| the written no | "Not in front of them." → "Later, then. When it's just us." pays 0 |
| pays | show: Exhibitionism +1 cap 79 · in: both +1 cap 79 · Campus talk +1 |

**`hub_jake_quad`** — Quad · Jake there · needs `jake_met` · repeatable

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `a3_offer` | Jake pulls you down into his lap on the grass, sideways, right in front of the … | no | "Let him show them." (Exhibitionism 60+ · in short skirt · not `jake_quad_today`) → `a3_show` | Exhibitionism +1 (cap 79) · Campus talk +1 · Hygiene -10 · `jake_quad_today` set · costs Energy 10 |
|  |  |  | "Let him in." (Exhibitionism 60+ · Corruption 60+ · in short skirt · not `jake_quad_today`) → `a3_do` | Corruption +1 (cap 79) · Exhibitionism +1 (cap 79) · Campus talk +1 · Hygiene -10 · `jake_quad_today` set · costs Energy 10 |
|  |  |  | "Not in front of them." → `a3_no` | — |
| `a3_show` | His hand slides up under your skirt and lifts the hem with his wrist, so the … | yes | "Get up off his lap." → Quad | `team_saw_quad` set |
|  |  |  | "Leave him to the guys." → Campus | `team_saw_quad` set |
| `a3_do` | Jake's hand stays under your skirt. | yes | "Get up off his lap." → Quad | `team_saw_quad` set |
|  |  |  | "Leave him to the guys." → Campus | `team_saw_quad` set |
| `a3_no` | He lets you up, grinning, and the team jeers at him while you walk off across … | no | "Later." → Campus | — |

## A4 · `shop_try_on`

| row | answer |
|---|---|
| who | her alone (the assistant outside the curtain) |
| where · when | the clothes shop changing room, from "Look at yourself in the mirror." |
| gate | Corruption 20 |
| want | "Everything all right in there? Shout if you need another size." |
| next step | she touches herself in the mirror; C5 (Exhibitionism 10): "Leave the curtain where it is." |
| hook | C5 on the same screen: "Leave the curtain where it is." |
| BRAKE | once a day (`shop_touch_today`, `shop_curtain_today`) |
| the written no | "Not here." pays 0 |
| pays | touch: Corruption +1 cap 39 · curtain: Exhibitionism +1 cap 19 |

**`shop_try_on`** — Clothes Shop · repeatable

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `changing_room` | The changing room is a curtain that doesn't reach the wall on one side. | no | "Hang them back up." → Clothes Shop | — |
|  |  |  | "Leave the curtain where it is." (Exhibitionism 10+ · not `shop_curtain_today`) → `curtain` | Exhibitionism +1 (cap 19) · `shop_curtain_today` set |
|  |  |  | "Look at yourself in the mirror." (Corruption 20+ · not `shop_touch_today`) → `mirror` | — |
| `mirror` | You're alone behind the curtain with the mirror and whatever you're halfway into. | no | "Touch yourself." (Corruption 20+ · not `shop_touch_today`) → `touch` | Corruption +1 (cap 39) · `shop_touch_today` set |
|  |  |  | "Not here." → `touch_no` | — |
| `touch` | You face the mirror with your back to the curtain. | yes | "Fine, thanks." → Clothes Shop | — |
|  |  |  | "Hang them back up." → Clothes Shop | — |
| `touch_no` | You catch your own eye in the mirror and laugh at yourself. | no | "Hang them back up." → Clothes Shop | — |
| `curtain` | You don't tug the curtain any further. | no | "Step back from the gap." → Clothes Shop | — |
|  |  |  | "Hang them back up." → Clothes Shop | — |

## A5 · `hub_zoe_bedroom`

| row | answer |
|---|---|
| who | Zoe |
| where · when | Zoe's bedroom, from "Get into her bed." (22:00-23:45) |
| gate | after `zoe_together` · Corruption 40; her mouth or her fingers Corruption 60 |
| want | "Stay over. I'm not asking twice." |
| next step | in her bed (Bold); her pick of the act (Hungry) |
| hook | none in the build: the act repeats the next day |
| BRAKE | once a day (`zoe_bed_today`); exits to Town ("Slip out while she sleeps.") |
| the written no | "Not tonight, Zo." → "Fine. Ask me again when you're brave." pays 0 |
| pays | Bold: +1 cap 59 · Hungry: +1 cap 79 |

**`hub_zoe_bedroom`** — Zoe's Bedroom · Zoe there · needs `zoe_met` · repeatable

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `a5_offer` | Zoe lifts the edge of her duvet without looking up from her phone. | no | "Get in with her." (Corruption 40+ · not `zoe_bed_today`) → `a5_bold` | Corruption +1 (cap 59) · Hygiene -10 · `zoe_bed_today` set · costs Energy 10 |
|  |  |  | "Her mouth. Down there." (Corruption 60+ · not `zoe_bed_today`) → `a5_lick` | Corruption +1 (cap 79) · Hygiene -10 · `zoe_bed_today` set · costs Energy 10 |
|  |  |  | "Your fingers in her." (Corruption 60+ · not `zoe_bed_today`) → `a5_hers` | Corruption +1 (cap 79) · Hygiene -10 · `zoe_bed_today` set · costs Energy 10 |
|  |  |  | "Not tonight, Zo." → `a5_no` | — |
| `a5_bold` | You get under the duvet with her. | yes | "Slip out while she sleeps (1h)." → Town | — |
|  |  |  | "Kiss her goodnight (1h)." → Town | — |
| `a5_lick` | You're naked under her duvet before she's put her phone down. | yes | "Slip out while she sleeps (1h)." → Town | — |
|  |  |  | "Kiss her goodnight (1h)." → Town | — |
| `a5_hers` | You push Zoe onto her back and drag her T-shirt up over her tits. | yes | "Slip out while she sleeps (1h)." → Town | — |
|  |  |  | "Kiss her goodnight (1h)." → Town | — |
| `a5_no` | She drops the duvet and goes back to her phone, but she's smiling at it. | no | "Leave her to sleep." → Zoe's Living Room | — |

## A6 · `keg_guy_counter`

| row | answer |
|---|---|
| who | the keg guy (no meter, no schedule) |
| where · when | Zoe's kitchen, party nights 22:00-02:00 |
| gate | after `keg_guy_dared` (her keg dare) · Corruption 60 · 6 hours after the last time |
| want | "Come round this side of the counter and find out." |
| next step | he bends her over the counter, the party through the door |
| hook | `keg_guy_went` holds him back 6 hours |
| BRAKE | once a day (`keg_counter_today`) |
| the written no | "Not tonight." → "You know where the keg is." pays 0 |
| pays | +1 cap 79 |

**`keg_guy_counter`** — Zoe's Kitchen · needs under 8h since `party_went` · 22:00-02:00 · `keg_guy_dared` · Corruption 60+ · 6h+ since `keg_guy_went` · repeatable

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `keg` | The guy from the keg is leaning on the counter with a red cup, right where … | no | "Let him bend you over the counter." (Corruption 60+ · not `keg_counter_today`) → `counter` | Corruption +1 (cap 79) · Hygiene -10 · `keg_counter_today` set · costs Energy 10 |
|  |  |  | "Not tonight." → `no` | — |
| `counter` | He turns you round and bends you over the counter between the bottles. | yes | "Back to the party." → Zoe's Living Room | `keg_guy_went` set |
|  |  |  | "Fix yourself up first." → Zoe's Living Room | `keg_guy_went` set |
| `no` | He lifts his cup at you and goes back to pouring. | no | "Back to the party." → Zoe's Living Room | — |

## A7 · `jake_party_bathroom`

| row | answer |
|---|---|
| who | Jake, the queue in the hall |
| where · when | Zoe's bathroom, Friday party 19:00-23:45, Jake in the living room |
| gate | after `jake_first_time` · Corruption 40; "Leave it unlocked." Corruption 60 |
| want | "Five minutes. Nobody will notice." |
| next step | sex against the sink, door locked (Bold) or unlocked (Hungry) |
| hook | none in the build: the act repeats the next day |
| BRAKE | once a day (`jake_bathroom_today`) |
| the written no | "Not at Zoe's." → "Later, then. Somewhere with a lock." pays 0 |
| pays | locked: +1 cap 59 · unlocked: +1 cap 79 |

**`jake_party_bathroom`** — Zoe's Bathroom · needs under 8h since `party_went` · Jake in Zoe's Living Room · `jake_first_time` · Corruption 40+ · Fri · 19:00-23:45 · not `jake_bathroom_today` · repeatable

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `door` | Jake catches your wrist at the bathroom door and backs you inside. | no | "Lock the door." (Corruption 40+ · not `jake_bathroom_today`) → `locked` | Corruption +1 (cap 59) · Hygiene -10 · `jake_bathroom_today` set · costs Energy 10 |
|  |  |  | "Leave it unlocked." (Corruption 60+ · not `jake_bathroom_today`) → `open` | Corruption +1 (cap 79) · Hygiene -10 · `jake_bathroom_today` set · costs Energy 10 |
|  |  |  | "Not at Zoe's." → `no` | — |
| `locked` | Jake locks the door and lifts you onto the sink. | yes | "Back to the party." → Zoe's Living Room | — |
|  |  |  | "Fix your face first." → Zoe's Living Room | — |
| `open` | You don't lock it. | yes | "Back to the party." → Zoe's Living Room | — |
|  |  |  | "Fix your face first." → Zoe's Living Room | — |
| `no` | He kisses your neck once and lets you go back out into the noise. | no | "Back to the party." → Zoe's Living Room | — |

## Explicit beats on this page

Not written out here (see the build); the build counts these screens as explicit: `hub_jake_gym` `a1_lockers`, `hub_jake_gym` `a1_mouth`, `hub_jake_quad` `a3_do`, `hub_jake_quad` `a3_show`, `hub_zoe_bedroom` `a5_bold`, `hub_zoe_bedroom` `a5_hers`, `hub_zoe_bedroom` `a5_lick`, `hub_zoe_canteen` `a2_fingers`, `jake_party_bathroom` `locked`, `jake_party_bathroom` `open`, `keg_guy_counter` `counter`, `shop_try_on` `touch`.

