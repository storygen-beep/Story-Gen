# [REVIEW] Scene — hale_03_photo_face_down

> A draft for LO to place. Written 2026-10-08.

| row | answer |
|---|---|
| person · step | `npc_hale` · 3 (Hale B 3) |
| where · when | his office, the faculty floor · Thursday 18:00–19:30 |
| gate | Corruption 20 · Exhibitionism 20 · the boost off |
| want (test 1) | "Thursday, after six." He named the hour himself |
| next step (test 2) | his hand on her shoulder, staying; the photo turned down |
| hook (test 3) | her grade goes home on the portal; Laura reads it |
| what she wears here (test 8) | the same skirt only in a group on her short-skirt state |
| explicit? | no: a non-sexual touch (stage 2) |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `desk` | she sits on the corner of his desk; he reads her paper at her shoulder | no | → `photo` | none |
| `photo` | his hand on her shoulder, staying; he turns the wedding photo face-down | no | "A no on my paper, or a yes?" → `portal` · "Just the paper." (parked) | `grade_psych` add +2 (a study session, guess) |
| `portal` | that week, the tuition portal: "A C, @player? We're paying for this course." (Laura) | no | → the floor | Hale's step counter set 3 |

His study sessions lift the grade (LO, 2026-10-07, decided item 9). The portal line is Laura's, read at home.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Hale B 3 (heat 10-06) |
| his office on the faculty floor | LO, chat 2026-10-07 |
| +2 a session | guess |
