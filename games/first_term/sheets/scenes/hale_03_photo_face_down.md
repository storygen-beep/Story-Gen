# [READY] Scene — hale_03_photo_face_down

> **Changed 2026-11-01, signed by LO 2026-11-01 ("Continue")** (DECISIONS 99–117): Hale's release-1 ladder (`sheets/people/npc_hale.md`, signed). Reworked as **Private coaching**: his office, the photo turned down, his offer, his hand on her shoulder. The canvas id stays. The lines below are mine, signed by LO 2026-11-01, except where marked built.

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08.

| row | answer |
|---|---|
| person · step | `npc_hale` · 3 of 4 (canvas `hale_03_photo_face_down`) |
| where · when | his office, the faculty floor · Thursday 18:00–19:30 (his office hour, from his email after step 2) |
| gate | Hale's step counter eq 2 · the boost off (was Corruption 20 · Exhibitionism 20) |
| want | "Not here. Office hours." He named the hour himself (step 2) |
| next step | his offer: coaching, and what he says it's for |
| hook | `hale_coaching_offered`; her grade only goes up if she comes back · Laura reads the grade on the portal |
| who notices | Hale; Laura, through the grade |
| what she risks | her grade; Laura reading it |
| what she wears here | the skirt line only in a group on her short-skirt state (as built) |
| explicit? | no: a non-sexual touch, the offer |
| her_line_low · her_line_high | low: "He's your professor. He's married." · high: "You want to know what he'd do next." (the person sheet's pair) | |

## Branch map — one row per screen

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op |
|---|---|---|---|---|
| `desk` | as built: his door open an inch, her paper, the wedding photo face-up; she sits on the corner of his desk | no | → `offer` | none |
| `offer` | he turns the photo face-down; "Your grade is a C…"; the speech; his hand on her shoulder, staying | no | "When?" → `when` · "That isn't coaching." → `isnt` · Walk out. → `out` | none |
| `when` | "Thursdays. Half past six. The door will be locked." | no | → `portal` | `hale_coaching_offered` set |
| `isnt` | "Then you'll stay at a C." He takes his hand away, and doesn't turn the photo back | no | → `portal` | `hale_coaching_offered` set |
| `out` | she takes her bag and goes; behind her: "Thursday, @player. The offer stands." | no | → `portal` | `hale_coaching_offered` set |
| `portal` | that week Laura reads the grade on the tuition portal (as built, its three lines by grade) | no | → the faculty floor | Hale's step counter set 3 · `hale_03_done` set |

**Every answer finishes the step** (the proposal: "does it finish: yes"); none raises the grade (the grade "goes up
only if she comes back"). The built "+2 a study session" on this step is dropped.

## The lines (mine, signed by LO 2026-11-01)

**`offer`:** "He reaches over without looking and turns the photo face-down." · Dr. Hale: "Your grade is a C, @player. I coach students who want to understand the material." · "He comes round the desk and stands behind you, and his hand settles on your shoulder, warm and heavy, and stays." · Dr. Hale: "Psychology starts with a person's sexuality. If you don't understand yours, you won't get past a C." · *(thought, low)* "He's your professor. He's married." · *(high)* "You want to know what he'd do next."
**`when`:** Dr. Hale: "Thursdays. Half past six. The door will be locked." · "His thumb moves once on your collarbone. Then he lets go."
**`isnt`:** Dr. Hale: "Then you'll stay at a C." · "He takes his hand away. He doesn't turn the photo back over."
**`out`:** "You pick up your bag and walk out without a word. His voice follows you into the corridor, calm, not raised." · Dr. Hale: "Thursday, @player. The offer stands."

**Cut:** the built `photo` exits ("Is that a no on my paper, or a yes?", "Just the paper.") and the `paper` no-node; the
`portal` keeps its three Laura lines (`hale.py:128-131`).

## Why — the source of each key choice

| key choice | source |
|---|---|
| the office, the photo, the speech, the hand, the three answers | `proposals/HALE_R1_LADDER.md`, step 3 (signed 2026-11-01); the speech is LO's words (2026-10-31) |
| no grade on this step | the same: "the grade goes up only if she comes back" |
| the portal kept | the same, "who sees or knows: Laura, through the grade" |
| "Half past six", the locked door | mine: his step 4 window starts 18:30 (`npc_hale.md`) |
