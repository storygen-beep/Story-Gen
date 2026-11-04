# [REVIEW] Scene — mark_01_count_it_slowly

> Changed 2026-11-04 to match the build; waits for LO's re-sign. The screens and buttons as built: he looks at her, not the money (Q6); "I'm saying it."; no stairs (Q7); her clothes come back on "Let me get dressed first."

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign. the count's two buttons; the Sunday count on both ways out; the step row.

> **Changed 2026-11-01, signed by LO 2026-11-01 ("Signed")** (DECISIONS 99–115): Mark's release-1 ladder (`sheets/people/npc_mark.md`, signed). Changed: her voice row only. The screens, the gate and the pay (his Want +10, stored for a later release) stand as built.

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08. Every Mark step is written twice, by his Power: his terms (M) or hers (E).

| row | answer |
|---|---|
| person · step | `npc_mark` · 1 (Mark A 1) |
| where · when | the kitchen table · her first Sunday, 08:00–12:00 |
| gate | `rent_starts` (set at breakfast, day 1) |
| want | none before: step 1. His eyes go to her legs ("bare" only when they are: shorts, a skirt, the sleep shirt) and stay |
| next step | the envelope: she sits with it sealed, and he looks at her instead |
| hook | "The rest waits a week, but Vance doesn't." Next time: "And not the shirt, next time." |
| what she wears here | her sleep shirt: only in a group on her worn state (guess) |
| which version | Power 50 or more (guess): his version · under 50: hers |
| explicit? | no: he only looks |
| her_line_low · her_line_high | low (under the stage): "He's Mom's husband. Pay him and go." · high (over it): "You want him to lose count." (the person sheet names none; worded by me, signed by LO 2026-11-01) | The built thought on `short` ("He looked at you longer than he ever looked at the money.") is the low side. |
| what changes after | the Sunday table, every week (`mark_sunday_table.md`) |

## The step row (filled from the build, 2026-11-03)

**Kind · stage:** a look that happens to her at the table (Good Girl · Covered).

| the moment | who sees or knows | what she risks | how she says yes | his move | does it finish | what changes after |
|---|---|---|---|---|---|---|
| Mark sits her at his table with the sealed envelope, his eyes on her legs | Mark | empty: step 1 | empty: step 1 | he makes her sit and look at it when she's short | not a sex act: he only looks | the Sunday table, every week |

## Branch map — one row per screen

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op |
|---|---|---|---|---|
| `table` | Mark at the table with the envelope: "Sit. Every Sunday, you sit at my table while this goes in Vance's envelope." | no | "Here." → `count` · "Let me get dressed first." → `dressed` (parked) | none; "Let me get dressed first." gives back what she wore before (`remember_outfit`, `restore_outfit`) |
| `count` | he doesn't open the envelope. Short, she sits and looks at it with him: "Seventy-five, I said." Paid up: "It's all there, Mark. Take your time." and his eyes leave it for her legs | no | "Can you just — say it?" (she's short) · "Let him look." (she isn't) → `short` | none |
| `short` | "I'm saying it." A short goes on the back of the envelope: "The rest waits a week, but Vance doesn't." Paid up: "That's the week. Same again Sunday." | no | "Fine." → the hall | Mark's Want add +10 · `mark_step` set 1 · the Sunday count: a full week adds 1 to her streak, his Power −3; a short or covered week resets it, his Power +3 |
| `dressed` | "Suit yourself." She puts clothes on and comes back; he has sealed the envelope without her. Short: "Short. The rest waits a week." | no | "Go back to your room." → the hall | `mark_step` set 1 and the same Sunday count; no Want |

Who notices: nobody. Ryan's in his room till 14:00 on Sunday; his door is shut. A full week (she isn't short) plays the same scene in her version: "It's all there, Mark. Take your time."

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Mark A 1 (heat 10-06) |
| "she knows, and she's still short" | LO, 2026-10-07 (SYSTEMS, decided item 2) |
| the Power edge at 50 | guess |
| fix from the false-line sweep | sweep A3-06, A3-20 (2026-10-08) |
