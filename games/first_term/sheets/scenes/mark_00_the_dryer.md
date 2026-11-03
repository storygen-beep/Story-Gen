# [REVIEW] Scene — mark_00_the_dryer

> **New 2026-11-01, signed by LO 2026-11-02** ("Signed, go ahead and build"; DECISIONS 124, `the-heat-ladder.md` H2, H5, H6, H7): Mark's first
> accident at home. Every chosen act with him follows it (`mark_saw_her`). Written by the lead.

| row | answer |
|---|---|
| person · step | `npc_mark` · 0, an accident (not a card; it happens to her) |
| where · when | the garage, at the washer · Saturday 09:00–17:00, Mark in the garage (`npc_mark.md` schedule) · once |
| gate | `opening_done` · Mark in `home_garage` · `mark_saw_her` is false · auto-fires when she walks in |
| who | Mark; nobody else |
| what she wears here | not named; the soaked screen branches on her bra only (`clothing_slot` bra equipped / unequipped) |
| want | his leak, on his body, covered (H7, stage 1): he looks, catches himself, turns to the bench |
| hook | `mark_saw_her`; her bridge thought (H6) turns it into a wish; his step 3 and his teases read the flag |
| raises (H5) | the accident: his Want +5 and `mark_saw_her`, whatever she does · "Don't take it yet.": her Exhibitionism +1, cap 19 · "Take the towel.": nothing of hers |
| explicit? | no: an accident screen, wet clothes, no act |
| crude-word ceiling | Mark's early column: legs, ass (`SP2_ladders.md` §6); her own thought may say tits |

## Branch map — one row per screen

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op |
|---|---|---|---|---|
| `hose` | the washer hose jumps off its tap and soaks her from the neck down; Mark at the bench sees it | no | "Take the towel." → `covered` · "Don't take it yet." → `stay` | `mark_saw_her` set · Mark `want` add +5 (on both exits) |
| `covered` | she takes the towel; he goes back to his bench; her bridge thought | no | "Go and change." → `home_hall` | none |
| `stay` | she lets him see a moment longer; he turns away like it burns; her bridge thought | no | "Go and change." → `home_hall` | exhibitionism add +1, cap 19 |

**The no** ("Take the towel."): always there, pays her nothing; his Want and the flag stand (H5).

## The screens, written

**`hose_bra`** (wearing a bra)

> You're loading the washer when the hose jumps off the tap. Cold water hits you square in the chest and soaks you from the neck down. You gasp. Everything you have on clings to you, and your bra shows dark right through it. Mark looks up from his bench. His eyes go straight to your chest. They stay there one second, two. Then he catches himself, turns his back, and grabs a towel off the shelf. He holds it out behind him without looking. "Tap's loose. Here."

**`hose_nobra`** (no bra)

> You're loading the washer when the hose jumps off the tap. Cold water hits you square in the chest and soaks you from the neck down. You gasp. Everything you have on clings to you, and there's no bra under it. Your nipples stand up hard through the wet cloth. Mark looks up from his bench. His eyes go straight to your chest. They stay there one second, two. Then he catches himself, turns his back, and grabs a towel off the shelf. He holds it out behind him without looking. "Tap's loose. Here."

**`covered`**

> You take the towel and hold it over your chest. Mark is already bent over his bench again, screwing something that doesn't need screwing. His ears are red. *He looked. Mom's husband looked at your tits, and then he turned his back like they burned him.* You go up to change, fast, your face burning. *Mom's husband. Don't think about it.* You think about it all the way up the stairs.

**`stay`**

> You don't take it. Not yet. You stand there dripping, and you let him see you not take it. He doesn't turn round. His hand with the towel shakes, once. "@player. Take the towel." You take it, slowly. *He wanted to look. He made himself stop.* You go up to change, and your nipples are still hard under the wet cloth all the way up the stairs. *Next time, see if he stops.*

## Why — the source of each key choice

| key choice | source |
|---|---|
| a first accident with Mark before his chosen acts | `the-heat-ladder.md` H2 · the audit (`round12_tease/first_term_audit.md` §3) · DECISIONS 124 |
| the garage on Saturday | his schedule (`npc_mark.md`): Sat 09:00–17:00 in the garage, where the washer is (his laundry item) |
| water, not a garment | true in whatever she wears; branches only on her bra (truth rule) |
| his look, then his back turned | H7: at stage 1 he leaks and covers it |
| the pay | H5, LO 2026-11-01: the accident pays him; only her "Don't take it yet." pays her |
| her thought at the end | H6, the bridge from an accident to her choice |
