# [READY] Scene — college_dean_office

> **New 2026-11-01, signed by LO 2026-11-01 ("Continue")** (DECISIONS 99–120). From the signed college system (`sheets/systems/college.md`, "The first college day";
> `proposals/R1_SYSTEM_COLLEGE_DAY.md`). An onboarding scene, not a heat step. No explicit screen; the lines are mine.

| row | answer |
|---|---|
| system · place | the college day · `dean_office` (faculty floor) |
| where · when | Monday of week one, straight from the opening's "Go to campus." (the opening's last screen, `toml_phases/2_one_shots.toml`, `card`; the button walks her here, 15 minutes) · once (`dean_met`) |
| gate | `opening_done` · `dean_met` false |
| who | the dean, 55, "to be obeyed" (`npc_dean.md`) |
| the dean's hours | his row is Mon–Fri 09:00–17:00; this scene runs before 09:00 on day 1. His schedule gains **Mon 07:30–09:00** (every Monday, so it is true every week). Mine; confirmed by LO 2026-11-01 ("Continue") |
| what she wears here (test 8) | the short-skirt line only in a group on her short-skirt state (his signed line) |
| who notices | the dean; then the full lecture hall turning round (Hale's step 1) |
| what she risks | being late on day one; the dean's second visit |
| what changes after | she has the timetable; the dean knows her name; the complaint rule is live (`complaints`, two and she's back) |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `wait` | he doesn't look up for a while; then he does, and takes his time over her | no | "Good morning." → `rules` | `dean_met` set |
| `rules` | the rules, his way: classes aren't optional; two complaints and she's back here | no | "I understand." → `timetable` | none |
| `timetable` | he hands her the timetable | no | "Look at it." → opens the timetable screen (Monday, Psychology "Next") and → `late` | `has_timetable` set |
| `late` | "Psychology. Lecture hall. You're already late." | no | "Go to Psychology." → `lecture_hall` | none |

## The lines (mine, signed by LO 2026-11-01)

**`wait`:** "The dean's office smells of carpet and old coffee. He's writing. He doesn't look up, and he doesn't ask you to sit, so you stand." · "When he does look up, he takes his time. Your face, then down, then back up, slowly, like he's reading a form." · in a short skirt: Dean: "Is that what you wore to class?" · otherwise: Dean: "You're the new one. @player."
**`rules`:** Dean: "Classes are not optional. Your grades come to me. Complaints come to me." · "He taps a folder with one finger." · Dean: "Two complaints and you're back in this office. I don't like seeing a student twice."
**`timetable`:** "He slides a printed sheet across the desk and keeps two fingers on it a second before he lets go." · Dean: "Your timetable. Learn it."
**`late`:** "He's already looking back at his writing." · Dean: "Psychology. Lecture hall. You're already late."

## Why — the source of each key choice

| key choice | source |
|---|---|
| the four screens, his lines, the timetable, the walk to Psychology | `college.md`, "The first college day" (signed 2026-11-01) |
| "Is that what you wore to class?" | `npc_dean.md` (signed 2026-10-08) |
| the timetable button | the engine: `setup.openTimetable(day)` (DECISIONS 112); how a canvas button runs it is checked at build (`college.md`) |
| his Monday 07:30 row, `has_timetable` | mine, confirmed by LO 2026-11-01 ("Continue") |
