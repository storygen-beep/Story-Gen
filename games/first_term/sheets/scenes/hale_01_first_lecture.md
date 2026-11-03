# [REVIEW] Scene — hale_01_first_lecture

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign.

> The signed plans behind this page: `proposals/COPY_FIXES_B.md`.

> **Changed 2026-11-01, signed by LO 2026-11-01 ("Continue")** (DECISIONS 99–117): Hale's release-1 ladder (`sheets/people/npc_hale.md`, signed). Reworked: his first move. She walks in late (the dean kept her); he puts her in the front row and drops his pen by her feet, and waits. The lines below are mine, signed by LO 2026-11-01.

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08.

| row | answer |
|---|---|
| person · step | `npc_hale` · 1 of 4 · meets Hale and Nadia (and the desk guy and the rival, as built: the flags are set here) |
| where · when | the lecture hall · Monday 08:30, day 1 (starts 08:30-08:55), from the dean's "Go to Psychology." |
| gate | none in the build: his step 0, Hale in the hall |
| want | none before: step 1. His eyes on her from the lectern while he says good morning to the room |
| next step | his order, his pen, and his wait |
| hook | Nadia: "He does that. Last spring it was me." His wife's Thursdays |
| who notices | the whole hall |
| what she risks | the room's eyes, day one |
| what she wears here | a skirt line only in a group on her short-skirt state (as built) |
| her stage here | Good Girl |
| explicit? | no |
| her_line_low · her_line_high | low: "He's your professor. He's married." · high: "You want to know what he'd do next." (the person sheet's pair) | The low side here: "He's your professor. Everyone's watching." |
| what changes after | front row is her seat (Psychology's class canvas seats her there) |

## The step row (as built, 2026-11-03)

The seven columns, filled from what the build does.

**Kind · stage:** his look in front of the whole hall, nothing she chose · stage 1, Good Girl (no gate)

| the moment | who sees or knows | what she risks | how she says yes | his move | does it finish | what changes after |
|---|---|---|---|---|---|---|
| she walks in late; he seats her front row and drops his pen at her feet | the whole hall; Nadia beside her | the room's eyes on day one | "Pick it up." or "Leave it." (no yes asked) | the order to the front row; the dropped pen; his wait | yes: she hands it back, or he picks it up | his step 1; `hale_met`, `nadia_met`; Nadia: "Last spring it was me." |

## Branch map — as built (2026-11-03)

One row per exit. Read from the build; it replaces the drafted map.

**`hale_01_first_lecture`** — Lecture Hall · Mon 08:30-08:55 · Dr. Hale there · needs Hale's step = 0 · one time

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `late` | The lecture hall door is heavy and it bangs behind you. | no | "Sorry." → `front_row` | `hale_met` set |
| `front_row` | The only free seat in the front row is beside a girl with big glasses and … | no | "Pick it up." → `pen` | `nadia_met` set · `desk_guy_met` set · `rival_met` set |
| | | | "Leave it." → `left` | `nadia_met` set · `desk_guy_met` set · `rival_met` set |
| `pen` | You bend down for it, all the way, and when you come back up his eyes … | no | "Hand it back (1h)." → `nadia` | Hale's step = 1 · `hale_01_done` set · `hale_pen_picked` set |
| `left` | You don't move. | no | "Sit through the lecture (1h)." → `nadia` | Hale's step = 1 · `hale_01_done` set |
| `nadia` | The girl beside you leans over while the room packs up, and says it without looking … | no | "After class." → Campus | — |

## The lines (mine, signed by LO 2026-11-01)

> Drafted before the build and kept as the signed record. Where it differs, the branch map and the beats above say what the build does.

**`late`:** "The lecture hall door is heavy and it bangs behind you. Two hundred heads turn. At the lectern a man in a tweed jacket stops in the middle of a sentence and looks at you, and lets the silence go on." · Dr. Hale: "Late, on the first day." · "He points with his pen at the front row." · Dr. Hale: "Front row. Where I can see you."
**`front_row`:** the built Nadia lines · "He goes back to his slide. Then his pen slips out of his fingers and rolls off the stage, and stops against your shoe. He doesn't bend for it. He waits."
**`pen`:** "You bend down for it, all the way, and when you come back up he's looking right at you. He's hard. You can see the line of it against his trousers from the front row, and he doesn't move to hide it." · "He holds his hand out for the pen." · Dr. Hale: "Thank you, @player."
**`left`:** "You don't move. The hall goes quiet, waiting to see who gives first. Dr. Hale comes down off the stage, crouches at your feet and picks the pen up, and looks up at you from there, slowly, all the way up." · Dr. Hale: "Noted."
The thought on `nadia` changes with the path: pen, the built "Your professor got hard looking at you, and the girl beside you thinks it's funny. Welcome to college." · left, "He made the whole room watch you. On purpose."

**Cut:** the built `pen` (her own pen rolling off), replaced by his.

## Why — the source of each key choice

| key choice | source |
|---|---|
| late, his order, his pen | `proposals/HALE_R1_LADDER.md`, step 1 (signed 2026-11-01) · `college.md`, the first day |
| Nadia, his wife's Thursdays | as built |
| the lines | mine, signed by LO 2026-11-01 |
