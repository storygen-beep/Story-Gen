# [READY] Scene — hale_01_first_lecture

> **Changed 2026-11-01, signed by LO 2026-11-01 ("Continue")** (DECISIONS 99–117): Hale's release-1 ladder (`sheets/people/npc_hale.md`, signed). Reworked: his first move. She walks in late (the dean kept her); he puts her in the front row and drops his pen by her feet, and waits. The lines below are mine, signed by LO 2026-11-01.

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08.

| row | answer |
|---|---|
| person · step | `npc_hale` · 1 of 4 · meets Hale and Nadia (and the desk guy and the rival, as built: the flags are set here) |
| where · when | the lecture hall · Monday 08:30–10:00, day 1, from the dean's "Go to Psychology." (`college.md`, the first day) |
| gate | none: the first class |
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

## Branch map — one row per screen

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op |
|---|---|---|---|---|
| `late` | she comes in late; the room turns; he stops mid-sentence: "Late, on the first day. Front row, where I can see you." | no | "Sorry." → `front_row` | `hale_met`, `nadia_met`, `desk_guy_met`, `rival_met` set |
| `front_row` | the only seat is front row, next to Nadia; he goes on, and drops his pen; it rolls to her feet; he waits | no | "Pick it up." → `pen` · "Leave it." → `left` | none |
| `pen` | she bends for it; when she comes up with it he's looking, and he's hard behind the lectern, and doesn't hide it; he holds his hand out for it | no | "Here." → `nadia` | Hale's step counter set 1 · `hale_01_done` set |
| `left` | she doesn't move; the hall waits; he comes round the lectern and picks it up himself, at her feet, and looks up at her from there | no | → `nadia` | Hale's step counter set 1 · `hale_01_done` set |
| `nadia` | as built: "He does that. Last spring it was me." · his wife picks him up Thursdays | no | "After class." → campus | none |

## The lines (mine, signed by LO 2026-11-01)

**`late`:** "The lecture hall door is heavy and it bangs behind you. Two hundred heads turn. At the lectern a man in a tweed jacket stops in the middle of a sentence and looks at you, and lets the silence go on." · Dr. Hale: "Late, on the first day." · "He points with his pen at the front row." · Dr. Hale: "Front row. Where I can see you."
**`front_row`:** the built Nadia lines (`hale.py:42-43`) · "He goes back to his slide. Then his pen slips out of his fingers and rolls off the stage, and stops against your shoe. He doesn't bend for it. He waits."
**`pen`:** "You bend down for it, all the way, and when you come back up he's looking right at you. He's hard. You can see the line of it against his trousers from the front row, and he doesn't move to hide it." · "He holds his hand out for the pen." · Dr. Hale: "Thank you, @player."
**`left`:** "You don't move. The hall goes quiet, waiting to see who gives first. Dr. Hale comes down off the stage, crouches at your feet and picks the pen up, and looks up at you from there, slowly, all the way up." · Dr. Hale: "Noted."
The thought on `nadia` changes with the path: pen, the built "Your professor got hard looking at you, and the girl beside you thinks it's funny. Welcome to college." · left, "He made the whole room watch you. On purpose."

**Cut:** the built `pen` (her own pen rolling off), replaced by his.

## Why — the source of each key choice

| key choice | source |
|---|---|
| late, his order, his pen | `proposals/HALE_R1_LADDER.md`, step 1 (signed 2026-11-01) · `college.md`, the first day |
| Nadia, his wife's Thursdays | as built (`hale.py:57-58`) |
| the lines | mine, signed by LO 2026-11-01 |
