# PLACE · Cain's Lab  `[READY]`

| | |
|---|---|
| **id** | `cain_lab` |
| **ENTERED FROM** | `underworld_strip` — visible from it, never entered in v0.1 |
| **WAYS OUT** | none authored |
| **DOOR** | **YES** — and it never opens this release |
| **LABELS** | `zone:reach` |
| **fill** | 300 `[INTENT]` — the smallest budget in the game, on purpose |
| **heat** | cold |

## What this place is FOR

**This is the door v0.1 closes on.** `the-release.md`: every release ends on a visible locked door,
and gate 9 reads it.

Cain is named in the Want, seen once, and out of reach. He is **not** in `[[npcs]]` this release —
he is a threshold, not a character, which is also why gate 6 (`standing surface`) never has to
answer for him. He is carried in `v2_state.json` `promises[]` as unpaid.

## The list

| # | row | canvas | kind | system | gate | effect | screen |
|---|---|---|---|---|---|---|---|
| 1 | "Try the door." | `TBD` | door | `drain` | `drain gte 100` — never reachable in v0.1 | — | yes |

## The refusal

⚠️ **A locked door says why** (gate 42, `the-surfaces.md` R5c). This one carries a
`locked_text_threshold`: it names the tier and the number, because the whole job of this screen is
to tell the player what the next release is about. The field hides a refusal or explains it; **2%
ship a dead greyed label** and vesper shipped 30%.

The refusal is **one short line and it is allowed to be the same line every time** — the field runs
a median of **8 words** and reuses the same sentence 44 times. Ours run 22 and are bespoke. Spend
the words on the far side of the door, in a later release.
