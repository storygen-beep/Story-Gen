# [READY] Scene — tom_03b_not_by_the_window

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign.

> The signed plans behind this page: `proposals/COPY_FIXES_C.md`.

> **New 2026-11-01, signed by LO 2026-11-01 ("Signed")** (DECISIONS 99–116). From Tom's signed release-1 ladder
> (`sheets/people/npc_tom.md`, step 3, the top step; `proposals/TOM_R1_LADDER.md`) and the café system
> (`sheets/systems/job.md`). Canvas id `tom_03_not_by_the_window`. No explicit screen; the lines are mine.

| row | answer |
|---|---|
| person · step | `npc_tom` · 3 of 3 (new, top step) |
| where · when | the back room, the café · Mon-Sat 14:30-22:00, within 3.5 hours of "Let it." |
| gate | his step 2 · regulars 15+ · the café's name -5 or less · `cafe_let_it` · the boost off |
| want | his look follows the customer's hand (the leak, in the level-3 café scene: one line, Tom at the counter, watching) |
| next step | he names what it's doing to his café, and draws one line |
| hook | the window rule · his card ends "Tom, later. (Next release)" |
| who notices | Tom; the room behind the door |
| what she risks | her job, his café's name |
| what she wears here | the café uniform (as worn) |
| explicit? | no: a talk (under 3 list words) |
| her_line_low · her_line_high | low: "He's your boss. Do the job." · high: "You felt that second. So did he." Worded for this screen: low "Say sorry. Keep the job." · high "He watched. He didn't stop it." |
| his move | the line he draws, and that he doesn't stop it |
| does it finish | yes |
| top step, declared not a payoff | taste rule 2: Tom's lust is a later release (LO); the payoff this release is the café's |

## The step row (as built, 2026-11-03)

The seven columns, filled from what the build does.

**Kind · stage:** the rule he draws after watching a customer touch her · no meter gate (the café's counters)

| the moment | who sees or knows | what she risks | how she says yes | his move | does it finish | what changes after |
|---|---|---|---|---|---|---|
| in the back: "Not by the window." | Tom; the café behind the door | her job; his café's name | "Then where?" · "Yes, boss." · "It's my tips." | he watched and didn't stop it; now he draws the line | yes | his step 3; `tom_window_rule`; his card: "Tom, later. (Next release)" |

## Branch map — as built (2026-11-03)

One row per exit. Read from the build; it replaces the drafted map.

**`tom_03_not_by_the_window`** — Café · Mon/Tue/Wed/Thu/Fri/Sat 14:30-22:00 · Tom there · needs Tom's step = 2 · `cafe_job` · drinks boost off · Café regulars 15+ · The café's name -5 or less · `cafe_let_it` · under 3.5h since `cafe_let_it` · one time

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `back` | When you come off the floor Tom is in the back room, leaning on the shelf … | no | "Say it, Tom." → `line` | — |
| | | | "Not now, Tom." → Café | back in 1 days |
| `line` | He looks at the door, at the front of the café behind it, the big window … | no | "Then where?" → `where` | — |
| | | | "Yes, boss." → `yes` | — |
| | | | "It's my tips." → `tips` | — |
| `where` | Anywhere the street can't see. | no | "Okay." → Café | Tom's step = 3 · `tom_window_rule` set · `tom_03b_done` set |
| `yes` | Tom nods once, and opens the door for you, and doesn't look at you while you … | no | "Back to the floor." → Café | Tom's step = 3 · `tom_window_rule` set · `tom_03b_done` set |
| `tips` | His ears go red, the way they did at the tip jar. | no | "Back to the floor." → Café | Tom's step = 3 · Tom's Power -3 · `tom_window_rule` set · `tom_03b_done` set |

## The lines (mine, for signed by LO 2026-11-01)

> Drafted before the build and kept as the signed record. Where it differs, the branch map and the beats above say what the build does.

**`back`:** "When you come off the floor Tom is in the back room, leaning on the shelf by the tip jar, and he shuts the door behind you." · "You can still feel where the man's hand was." · Tom: "Reputation's going. People talk. And the tables are full." · "He doesn't sound angry. He sounds like he's done the sums."

**`line`:** Tom: "I'm not stopping you. I saw. I didn't stop it." · "He looks at the door, at the front of the café behind it, the big window on the street." · Tom: "Not by the window."

**`where`:** Tom: "Anywhere the street can't see. That's all I'm saying." · *(thought, low)* "Say sorry. Keep the job." / *(high)* "He watched. He didn't stop it."

**`yes`:** "Tom nods once, and opens the door for you, and doesn't look at you while you go past him."

**`tips`:** Tom: "Then keep them. Not by the window." · "His ears go red, the way they did at the tip jar."

The thoughts on `where` show by her stage (Corruption under 20 the low, 20 and over the high; she is 20 and over by
the gate's level-3 shift, so in practice the high line shows; the low is kept for a reset).

## What changes after

> Drafted before the build and kept as the signed record. Where it differs, the branch map and the beats above say what the build does.
- **The window rule** (`tom_window_rule`): level-3 café scenes stop using the window seats (`job.md`, "After Tom's step 3").
- **His counter line** changes (`tom_01_the_apron.md`, his counter, `tom_step` eq 3).
- **His card** ends on the locked line: "Tom, later. (Needs Corruption 60.)"

## Why — the source of each key choice

| key choice | source |
|---|---|
| the step, the three answers, the window rule, the locked line | `proposals/TOM_R1_LADDER.md`, step 3 (signed 2026-11-01) |
| footfall 15, name −5 | `sheets/systems/job.md`, the café keeps score (signed) |
| the shift's "let it" as the trigger | the proposal: "after she's let a customer touch her" · the flag name, mine |
| the parked no, no meter pay | mine, confirmed by LO 2026-11-01 ("Signed") |
