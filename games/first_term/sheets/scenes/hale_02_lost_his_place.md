# [READY] Scene — hale_02_lost_his_place

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign.

> The signed plans behind this page: `proposals/COPY_FIXES_B.md`.

> **Changed 2026-11-01 after the build, signed by LO 2026-11-01 ("Signed, build them")** (the reader's FAILs; LO's picks in chat): a no in any clothes, not only a skirt.

> **Changed 2026-11-01, signed by LO 2026-11-01 ("Continue")** (DECISIONS 99–117): Hale's release-1 ladder (`sheets/people/npc_hale.md`, signed). Changed: the gate is Daring only (Exhibitionism 20; Corruption 20 dropped) and his step 1; her voice row. The screens stand as built.

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08.

| row | answer |
|---|---|
| person · step | `npc_hale` · 2 (Hale B 2) |
| where · when | the lecture hall · Mon, Wed, Fri, starts 08:30-08:45 |
| gate | Exhibitionism 20 (Daring) · his step 1 · the boost off |
| want | his eyes on the front row since the pen |
| next step | her chosen flash; he loses his sentence |
| hook | after class: "Thursday." His office hours |
| what she wears here | no panties: the step's own choice, Daring, this step only (LO, 2026-10-08) |
| explicit? | no: a flash under her stage's words |
| crude words | Hale's early column: legs, ass (stage 2) |
| who notices | Hale; the guy beside her |
| what she risks | being seen by the row |
| her_line_low · her_line_high | low: "He's your professor. He's married." · high: "You want to know what he'd do next." (the person sheet's pair) | |

## The step row (as built, 2026-11-03)

The seven columns, filled from what the build does.

**Kind · stage:** a chosen flash for one person she knows · Daring (Exhibitionism 20)

| the moment | who sees or knows | what she risks | how she says yes | his move | does it finish | what changes after |
|---|---|---|---|---|---|---|
| front row: she uncrosses her legs, no panties, and he loses his place | Hale; the class around her | being seen by the row | "Uncross your legs, slowly." (or hem, or waistband, by what she wears) | after class he waits for the room to empty | yes | his step 2; Exhibitionism +3 (cap 79); Thursday office hours open |

## Branch map — as built (2026-11-03)

One row per exit. Read from the build; it replaces the drafted map.

**`hale_02_lost_his_place`** — Lecture Hall · Mon/Wed/Fri 08:30-10:00 · Dr. Hale there · needs Hale's step = 1 · Exhibitionism 20+ · drinks boost off · 08:30-08:45 · one time

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `legs` | Front row again. | no | "Uncross your legs, slowly." (in short skirt) — 2 versions, by clothes → `flash` | — · varies: `hale02_took_them_off` cleared, `hale02_took_them_off` set, unequip plain panties |
| | | | "Pull your waistband down an inch." (not in short skirt · no dress) — 2 versions, by clothes → `flash` | — · varies: `hale02_took_them_off` cleared, `hale02_took_them_off` set, unequip plain panties |
| | | | "Inch your hem up." (dress on) — 2 versions, by clothes → `flash` | — · varies: `hale02_took_them_off` cleared, `hale02_took_them_off` set, unequip plain panties |
| | | | "Fix your skirt (1h)." (in short skirt) → Lecture Hall | back in 2 days |
| | | | "Sit up straight." (not in short skirt) → `straight` | — |
| `flash` | You went to the toilets before class and took your panties off and put them in … | no | "You lost your place, Dr. Hale." (1h)" → `after` | Exhibitionism +3 (cap 79) |
| `after` | After class he waits until the room has emptied before he speaks to you. | no | "Thursday." → Campus | Hale's step = 2 · `hale_02_done` set |
| `straight` | You sit up straight and keep your eyes on your notes. | no | "Sit through the lecture (1h)." → Lecture Hall | back in 2 days |

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Hale B 2 (heat 10-06) |
| no panties at Daring, this step only | LO, 2026-10-08 (question 18) |

## Changed after the build (2026-11-01), signed by LO 2026-11-01

| node | the no (new, when she isn't in a skirt) | the reply (mine, signed by LO 2026-11-01) |
|---|---|---|
| `legs` | "Sit up straight." | "You sit up straight and keep your eyes on your notes. Dr. Hale finds his place, and doesn't look at the front row again until the end." The step waits two days, as "Fix your skirt." does. |
