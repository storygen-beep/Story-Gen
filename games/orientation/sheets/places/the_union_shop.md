# PLACE · The Union Shop  `[READY]`

| | |
|---|---|
| **id** | `the_union_shop` · button `The Union Shop` |
| **ENTERED FROM** | `the_quad` |
| **FILL** | 500 words |
| **cycling pool** | no |

## What kind of place this is
The one room on campus that only sells. Two aisles and a rail by the door — the lab kit the reading
list said was included, coffee it carries down from the counter, and the dress the row wears on a
Thursday at sixty dollars.

⚠️ **This was `act_quad_shop`, a canvas on open ground.** Its node was already titled *The union
shop*; the row was named after one of the three things it sold, and it went on saying *"Buy the lab
kit"* for the rest of the game after the kit was bought. The game's own player-facing prose named
this place twice before it existed — Halloran's `locked_text` (*"twenty-eight dollars at the union
shop"*) and `simone_05`'s beat (*"off a rail by the door of the union shop"*). Same promotion
`the_row` got on 2026-09-02.

## The list
| row | system |
|---|---|
| **Browse Clothes** | **not a canvas** — the engine renders it off `[settings] shop_location`. Sells `row_dress` $60 and `black_set` $35 |
| **Buy the lab kit ($28)** | money — a one-time purchase that **retires its own row** on `has_lab_kit`, and opens the late lab (R1b) |

## The shop screen is the engine's
`shop_location = "the_union_shop"` renders `[[Browse Clothes->ShopPage]]` here, above the activity
list, on every visit (`v2.py:9902`, `:9949`). **Do not author a "browse the rail" canvas beside it**
— that is the mistake `act_room_wardrobe` made at the `wardrobe_location` and was deleted for.

It stocks only `initial = false` **and** `price > 0` (`v2.py:2105`), tiered by
`getCorruptionThreshold`, which reads the *garment's own `conditions`* and not its corruption stat
(`v2.py:1999`). Neither garment here has conditions, so both sit in the always-open **Basic** tier —
correct, because this game has no `corruption` meter.

⚠️ **The shop screen is an info page, so buying costs no game time.** The dress used to cost 20
minutes as a hand-rolled choice. Noted as drift, not repaired.

## ⚠️ Nothing non-repeatable and nothing `trigger_mode = "random"` may ever live here
The shop link is emitted **inside** the `<<if _autoFire>><<goto _autoFire>><<else>>` branch, and
`getStoryCanvasRedirect` fires on a non-repeatable canvas (`v2.py:4696`) or falls through to
`checkRandomEncounters` (`v2.py:5211`). Either redirects the screen before the link is drawn. One
one-shot meeting or one random walk-in placed here and **the shop is invisible until it has fired**.
`act_shop_kit` is repeatable and manual for exactly this reason.

## Why this room exists at all
Until 2026-09-03 there was no `shop_location`, and `row_dress` / `black_set` — the only garments in
the game with `exposure = 1` and `type = "going_out"` — could not be obtained by any route. All four
clothing conditions in the game read one of those two properties, so `simone_05` could not be
entered, `simone_06` never set `simone_open`, and `act_pledge_upstairs` was sealed. One missing
settings line, one dead arc. Gate `a declared garment can be got` exists because of it.

## Walk-in
None. Nobody is scheduled here.

## Ways out
`the_quad`
