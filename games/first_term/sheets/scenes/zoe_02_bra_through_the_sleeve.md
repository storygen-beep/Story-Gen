# [READY] Scene — zoe_02_bra_through_the_sleeve

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08.

| row | answer |
|---|---|
| person · step | `npc_zoe` · 2 (Zoe A 2) |
| where · when | Zoe's balcony, a Friday party · 21:00–00:00 |
| gate | Corruption 20 · Exhibitionism 20 · the boost off |
| want (test 1) | she keeps her eyes on the bra strap |
| next step (test 2) | a dress dare with the room behind the glass |
| hook (test 3) | "Nope. Mine now." And: "There's a hot tub Saturday. Just us." |
| what she wears here (test 8) | the dress in a group on `zoe_party_dress` worn; the bra comes off here |
| explicit? | no: a dare (under 3 list words) |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `balcony` | Zoe: "Bra off. Through the sleeve." | no | "Watch me." → `sleeve` · "Not tonight, Zo." → the party (parked) | none |
| `sleeve` | she works it out through her sleeve; nipples tight; a guy inside whistles | no | "Give it back." → `mine` | her bra slot emptied · exhibitionism add +3 |
| `mine` | Zoe tucks it in her back pocket: "Nope. Mine now." Then: the hot tub, Saturday | no | "Saturday." → the party | `zoe_step` set 2 · `party_house_invite` set |

This step sets `party_house_invite`, which opens the party house (nothing set it before).

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Zoe A 2 (heat 10-06) |
| the invite flag here | guess (fix 1, the flag check) |
