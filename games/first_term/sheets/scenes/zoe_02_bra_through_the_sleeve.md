# [READY] Scene — zoe_02_bra_through_the_sleeve

> **Changed 2026-11-02** (reader fails a3, signed by LO 2026-11-02, DECISIONS 131): seen by the readers, the `sleeve` button "Give it back." became "Ask for it back." (Zoe doesn't have the bra yet when it shows; `zoe.py`).

> **Changed 2026-11-01, signed by LO 2026-11-01 ("Continue")** (DECISIONS 99–118): Zoe's release-1 ladder (`sheets/people/npc_zoe.md`, signed). Changed: the gate is Curious **or** Daring (`meters.md` rule 5: a showing yes and a doing yes on one screen); a doing yes added, "Dare me something else.", which plays the dares' kiss screen; her voice row.

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08.

| row | answer |
|---|---|
| person · step | `npc_zoe` · 2 (Zoe A 2) |
| where · when | Zoe's balcony, a Friday party · 21:00–00:00 |
| gate | Corruption 20 **or** Exhibitionism 20 · `zoe_step` eq 1 · the boost off · each yes by its own meter: "Watch me." needs Exhibitionism 20, "Dare me something else." needs Corruption 20 |
| want (test 1) | she keeps her eyes on the bra strap |
| next step (test 2) | a dress dare with the room behind the glass |
| hook (test 3) | "Nope. Mine now." And: "There's a hot tub Saturday. Just us." |
| what she wears here (test 8) | the dress in a group on `zoe_party_dress` worn; the bra comes off here |
| explicit? | the showing path no (under 3 list words, as built); the doing path yes (the kiss, `zoe_dares` `low_do`) |
| who notices | the room behind the glass |
| what she risks | strangers seeing |
| her_line_low · her_line_high (rule 7) | low: "It's a dare. It doesn't count." · high: "You want her to dare you something worse." (the person sheet's pair) | |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `balcony` | Zoe: "Bra off. Through the sleeve." | no | "Watch me." → `sleeve` (Daring) · "Dare me something else." → `kiss` (Curious) · "Not tonight, Zo." → the party (parked) | none |
| `kiss` | Zoe: "Fine. Kiss the cocky guy. Properly." Then the dares' `low_do` beat (`zoe_dares.md`), the room behind the glass watching | yes | "Saturday?" → `saturday` | corruption add +3 |
| `saturday` | Zoe, flushed: "There's a hot tub Saturday. Just us." | no | "Saturday." → the party | `zoe_step` set 2 · `party_house_invite` set |
| `sleeve` | she works it out through her sleeve; nipples tight; a guy inside whistles | no | "Ask for it back." → `mine` | her bra slot emptied · exhibitionism add +3 |
| `mine` | Zoe tucks it in her back pocket: "Nope. Mine now." Then: the hot tub, Saturday | no | "Saturday." → the party | `zoe_step` set 2 · `party_house_invite` set |

This step sets `party_house_invite`, which opens the party house (nothing set it before).

**The two yeses** finish the same step (`meters.md` rule 5). The doing path doesn't take her bra, so "Nope. Mine now." shows only on the showing path.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Zoe A 2 (heat 10-06) |
| the invite flag here | guess (fix 1, the flag check) |

> Changed 2026-11-02 (reader a3, older rows; DECISIONS 131; LO: "fix the older ones too"): in Zoe's dress the bra slides out through the armhole, not a sleeve.


## Changed 2026-11-03 (LO: "Go"; DECISIONS 133)

- Not the night of step 1: the balcony waits 24 hours after `zoe_01_done`.
- Only with a yes on screen: Daring (Exhibitionism 20) for the bra; or Curious (Corruption 20) under Daring with Jake's
  teammate at the party, where "Dare me something else." is the only yes (its own copy, `zoe_02_balcony_curious`).
- "You chickened out on me last time." now reads her no on this balcony (`zoe_balcony_refused`), not her no at the
  first party. The balcony's no moves `zoe_refused` +1.
- The card adds the goal "Reach Daring (Exhibitionism 20), or Curious (Corruption 20) with Jake's teammate at the party".
