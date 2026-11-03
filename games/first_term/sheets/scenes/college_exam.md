# [READY] Scene — college_exam

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign.

> The signed plans behind this page: `proposals/COPY_FIXES_B.md`.

> **Changed 2026-11-01, re-signed by LO 2026-11-02** ("Signed, go ahead and build"; DECISIONS 124, the heat ladder a2): its gate or pay changes; the row is in `sheets/HEAT_LADDER_A2.md`.

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08. The midterm (`college_exam`): one choice inside the exam.

| row | answer |
|---|---|
| system · pool | college · `college_exam` |
| where · when | the lecture hall · days 42-55 after the opening, each subject in its class slot, once |
| gate | Focus: none · the study guy (Business): Corruption 20 · the cocky guy (Figure drawing): Exhibitionism 20 to look, 40 to show |
| who sees the flash | the cocky guy (21) only: a flash for one person she knows |
| want | the cocky guy: "Show me and I'll tilt my paper." |
| next step | three seconds under the desk line for his answers |
| hook | `cocky_exam_deal`: at the party, "You still owe me for that exam." |
| what she wears here | not named; "pull everything up" |
| BRAKE | once per exam |
| effects | Focus: grade +6 (Intelligence 10+) or +1 · copying: grade +5 · the flash: Exhibitionism +1 (cap 59) |
| the crude-word ceiling | tits, nipples, ass, cock, wet, clit · no cunt, fuck, cum, pussy (LO, 2026-10-08) |

## Branch map — as built (2026-11-03)

One row per exit. Read from the build; it replaces the drafted map.

**`college_exam_psych`** — Lecture Hall · Mon/Wed/Fri 08:30-08:45 · Thu 13:00-13:15 · needs day 42+ since `opening_done` · before day 56 since `opening_done` · not `exam_psych_done` · one time

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `paper` | The Psychology midterm. | no | "Focus. Do it yourself (1h 30m)." — 2 versions, by meters → `result` | — · varies: Psychology grade |
| `result` | Pens down. | no | "Leave the hall." → Campus | `exam_psych_done` set · `midterm_done` set |

**`college_exam_business`** — Lecture Hall · Mon/Wed 10:15-10:30 · Tue 13:00-13:15 · needs day 42+ since `opening_done` · before day 56 since `opening_done` · not `exam_business_done` · one time

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `paper` | The Business midterm. | no | "Focus. Do it yourself (1h 30m)." — 2 versions, by meters → `result` | — · varies: Business grade |
| | | | "Flirt with the study guy for his paper." (Corruption 20+ · `study_guy_met`) → `study` | — |
| `study` | You catch the study guy's eye across the gap and bite your lip and look at … | no | "Copy (1h 25m)." → `result` | Business grade +5 · Campus talk +1 |
| `result` | Pens down. | no | "Leave the hall." → Campus | `exam_business_done` set · `midterm_done` set |

**`college_exam_bio`** — Lecture Hall · Tue/Thu 10:15-10:30 · Mon 13:00-13:15 · needs day 42+ since `opening_done` · before day 56 since `opening_done` · not `exam_bio_done` · one time

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `paper` | The Biology midterm. | no | "Focus. Do it yourself (1h 30m)." — 2 versions, by meters → `result` | — · varies: Biology grade |
| `result` | Pens down. | no | "Leave the hall." → Campus | `exam_bio_done` set · `midterm_done` set |

**`college_exam_art`** — Lecture Hall · Tue/Thu 08:30-08:45 · Wed 13:00-13:15 · needs day 42+ since `opening_done` · before day 56 since `opening_done` · not `exam_art_done` · one time

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `paper` | The Figure drawing midterm. | no | "Focus. Do it yourself (1h 30m)." — 2 versions, by meters → `result` | — · varies: Figure drawing grade |
| | | | "Look at the cocky guy." (Exhibitionism 20+ · `cocky_guy_met`) → `price` | — |
| `price` | Jake's teammate is at the next desk with his paper finished and his pen behind his … | no | "What?" → `flash_ask` | — |
| | | | "Look away (1h 29m)." → `result` | Figure drawing grade +1 |
| `flash_ask` | Show me and I'll tilt my paper. | no | "Show him." (Exhibitionism 40+) → `flash` | — |
| | | | "No." → `no` | — |
| `no` | He shrugs and turns his paper face-down, slow, so you watch it go. | no | "Back to your own paper (1h 27m)." → `result` | Figure drawing grade +1 |
| `flash` | The proctor sits at the front, reading. | yes | "Copy (1h 25m)." → `result` | Figure drawing grade +5 · Exhibitionism +1 (cap 59) · `cocky_exam_deal` set |
| `result` | Pens down. | no | "Leave the hall." → Campus | `exam_art_done` set · `midterm_done` set |

## The explicit beats, as built (2026-11-03)

Every screen the build counts as explicit (3+ words from the frozen list), word for word, with its measurement. It replaces the drafted text.

**`college_exam_art` · `flash`** — 102 words · 5 counted: tits, nipple, tits, breast, nipple · ceiling: strangers' words (DECISIONS 41): tits, nipples, ass, cock, wet, clit

> The proctor sits at the front, reading. Every head in the row is bent over a page. You check the room once. Then you pull everything up under the desk line, where only he can see. Your tits are bare in the cold hall air. Your nipples go hard at once, tight and aching. His pen stops mid-word. His eyes drop to your tits and stay there. One second. Two. Three. You yank everything down and cover your breasts. He slides his paper to the edge of his desk. Your nipples are still hard, and his stare is still on your chest.

## Why — the source of each key choice

| key choice | source |
|---|---|
| one choice inside the exam; the cocky guy's price | LO, chat 2026-10-06 (SYSTEMS §1) |
| a flash for one person she knows at Curious | SP2 §1 |
| the prose | `v2-prose`, measured by `gates.py --beat`, 2026-10-08 |
| +5 for copying | guess |
| fix from the false-line sweep | sweep A5-23 (2026-10-08) |
