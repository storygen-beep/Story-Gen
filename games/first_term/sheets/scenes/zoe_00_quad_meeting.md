# [READY] Scene — zoe_00_quad_meeting
> Signed by LO: LO, 2026-11-04.

> Changed 2026-11-03 to match the build (third alignment pass); signed by LO 2026-11-04.

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08 (fix 1). Zoe's meeting: nothing set `zoe_met` before, so her
> apartment, the parties, Zoe A 1 and Jake B 1 could never open.

| row | answer |
|---|---|
| person · step | `npc_zoe` · her meeting (a one-time scene, not a ladder step) |
| where · when | the quad · Tue, Thu, Fri 14:30–18:00 (her row), the first time she's there |
| gate | `opening_done` · `zoe_met` false · Tue, Thu, Fri 14:30-18:00 on the quad |
| priority | high: it fires before her hub can show |
| want | she picks @player out: someone to drag to her party |
| next step | her name, her number, and Friday |
| hook | "Friday. My place. Wear something short." (her thread, then Zoe A 1) |
| what she wears here | not named |
| explicit? | no |
| role before name | "the girl from Biology", then "Zoe" once she says it |

## The step row (as built, 2026-11-03)

The seven columns, filled from what the build does.

**Kind · stage:** an invite, nothing she does · stage 1 (no gate)

| the moment | who sees or knows | what she risks | how she says yes | his move | does it finish | what changes after |
|---|---|---|---|---|---|---|
| Zoe on the quad: a party Friday; she types her number into Ella's phone | Zoe; the quad | none: step 0, it can be an accident | "Sit with her." then "Party?" (or "Can't...", she shouts the address) | the invite; her number | yes | `zoe_met`, `zoe_number`: the Friday party opens |

## Branch map — as built (2026-11-03)

One row per exit. Read from the build; it replaces the drafted map.

**`zoe_00_quad_meeting`** — Quad · Tue/Thu/Fri 14:30-18:00 · needs `opening_done` · not `zoe_met` · one time

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `wave` | The girl from your Biology class, the one who whispers through the slides, is lying on … | no | "Sit with her." → `zoe` | — |
| | | | "Can't, I've got a shift." (`cafe_job`) → `later` | — |
| | | | "Can't, I've got class." (not `cafe_job`) → `later` | — |
| `zoe` | You sit. | no | "Party?" → `friday` | `zoe_met` set |
| `friday` | She takes your phone out of your hand without asking and types her number into it, … | no | "Friday." → Quad | `zoe_number` set |
| `later` | She shouts the address after you across the whole quad. | no | "Wave without looking back." → Campus | `zoe_met` set · `zoe_number` set |

## The nudges, so she isn't missed

> Drafted before the build and kept as the signed record. Where it differs, the branch map and the beats above say what the build does.

| where | what | sets |
|---|---|---|
| Biology, Mon 13:00 and Tue 10:15 | the girl beside her whispers through the slides: "Quad after?" | nothing |
| her card under People, from the day the opening ends, while `zoe_met` is false (LO 2026-11-02; was a Story Goals card, hidden all week one behind the "Week one" card) | "The girl from your Biology class hangs out on the quad in the afternoons." · tip "The quad, Tuesday, Thursday or Friday, 14:30 to 18:00" | nothing |

## Why — the source of each key choice

| key choice | source |
|---|---|
| met on the quad in week 1 | LIVES §6 · LO, 2026-10-08 (fix 1) |
| her quad hours | LIVES §3 (Tue, Thu, Fri afternoons) |
| the meeting fires in her window | `the-first-hour.md` F5 (a meeting fires where they are) |
| her seat in Biology | LO, chat 2026-10-07 (SYSTEMS, seating) |
| the nudges, the lines, `zoe_number` | guess |
| fix from the false-line sweep | sweep A4-43 (2026-10-08) |
