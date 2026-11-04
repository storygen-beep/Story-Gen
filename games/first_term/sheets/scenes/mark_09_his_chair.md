# [CUT] [REVIEW] Scene — mark_09_his_chair

> Changed 2026-11-04 to match the build; signed by LO 2026-11-04. Still cut and not built. Her line telling Mark to count is gone from the map (Q6), and the Sunday table row says what the build does.

> **CUT 2026-11-01** (DECISIONS 113): Mark's paid route is cut: no sex and no money for her body (`npc_mark.md`). Kept on disk as the record; not built in release 1.

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08. Every Mark step is written twice, by his Power: his terms (M) or hers (E).

| row | answer |
|---|---|
| person · step | `npc_mark` · 9 (Mark A 9) · goal 1's body route |
| where · when | the kitchen · Wednesday 18:00–22:00, Laura late, Ryan out |
| gate | Corruption 40 · Exhibitionism 40 · his Want 80 |
| want | his chair, pulled out; he waits for Wednesday and she sees it |
| next step | she takes his chair and sets the terms |
| hook | "His lap waits." Step 10 is later; the table is hers now |
| what she wears here | not named |
| which version | Power 50 or more (guess): his version · under 50: hers |
| explicit? | no: power (under 3 list words) |

## Branch map — one row per screen

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op |
|---|---|---|---|---|
| `chair` | she sits in his chair, legs crossed, Sunday's rent counted out of her purse in front of her, then back in it | no | → `m` or `e` | none: no money moves on a Wednesday |
| `m` | M: "My chair." | no | her line telling him to count → `count` · her refusal → parked (both lines cut with the route; nobody counts the rent twice, Q6) | none |
| `e` | E: he stands; she fans Sunday's money on the table, then takes it back, with the same cut line | no | → `count` | none |
| `count` | he counts standing, hard under his jeans | no | "Good." → the hall | Mark's Want add +10 · `mark_step` set 9 · `pays_her_own_way` set |

**Goal 1 ends here** (the body route): `pays_her_own_way`. The twist's offer scene follows; her answer stays parked.

## The repeat it turns into — the Sunday table (`mark_sunday_table`, one sheet row)

| row | answer |
|---|---|
| where · when | the kitchen, Sunday 08:00–12:00 |
| what happens | he looks at her and counts nothing (Q6), in two versions, his terms or hers, by his Power |
| priced options | none: the paid exits are cut (`mark_sunday_table.md`) |
| explicit? | no: he looks (`mark_sunday_table.md`) |
| BRAKE | once a Sunday, on the trigger |

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene; goal 1's body route | the arc ideas, Mark A 9 · IDEA §2 |
| the twist offer after | LO, 2026-10-07 (SP7 call 3) |
| the table as the repeat | SP2 (After) |
| fix from the false-line sweep | sweep A3-34 (2026-10-08) |
