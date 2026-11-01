# [READY] Scene — tom_03b_not_by_the_window

> **New 2026-11-01, signed by LO 2026-11-01 ("Signed")** (DECISIONS 99–116). From Tom's signed release-1 ladder
> (`sheets/people/npc_tom.md`, step 3, the top step; `proposals/TOM_R1_LADDER.md`) and the café system
> (`sheets/systems/job.md`). Canvas id `tom_03_not_by_the_window`. No explicit screen; the lines are mine.

| row | answer |
|---|---|
| person · step | `npc_tom` · 3 of 3 (new, top step) |
| where · when | the back room, `cafe` · Mon–Sat 14:30–22:00, at the end of a shift |
| gate | `tom_step` eq 2 · `cafe_footfall` gte 15 · `cafe_name` lte −5 · she chose "let it" in a level-3 café scene this shift (`cafe_let_it` set, under 1 hour ago; flag name mine, set by the café scene) · the boost off |
| want (test 1) | his look follows the customer's hand (the leak, in the level-3 café scene: one line, Tom at the counter, watching) |
| next step (test 2) | he names what it's doing to his café, and draws one line |
| hook (test 3) | the window rule · his card ends on "Tom, later. (Needs Corruption 60.)" |
| who notices | Tom; the room behind the door |
| what she risks | her job, his café's name |
| what she wears here (test 8) | the café uniform (as worn) |
| explicit? | no: a talk (under 3 list words) |
| her_line_low · her_line_high (rule 7) | low: "He's your boss. Do the job." · high: "You felt that second. So did he." Worded for this screen: low "Say sorry. Keep the job." · high "He watched. He didn't stop it." |
| his move | the line he draws, and that he doesn't stop it |
| does it finish | yes |
| top step, declared not a payoff | taste rule 2: Tom's lust is a later release (LO); the payoff this release is the café's |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `back` | Tom waits in the back room with the door shut: "Reputation's going. The tables are full." | no | "Say it, Tom." → `line` · "Not now, Tom." → the café (parked) | none |
| `line` | "Not by the window." | no | "Then where?" → `where` · "Yes, boss." → `yes` · "It's my tips." → `tips` | none |
| `where` | "Anywhere the street can't see. That's all I'm saying." | no | "Okay." → the café | the step's pay (below) |
| `yes` | he nods once and opens the door for her | no | → the café | the step's pay |
| `tips` | "Then keep them. Not by the window." | no | → the café | the step's pay · his Power add −3 |

**The step's pay:** `tom_window_rule` set · `tom_step` set 3 · `tom_03b_done` set. The proposal names no meter pay
for it; confirmed by LO 2026-11-01 ("Signed").
**The parked no** ("Not now, Tom."): the step waits for her next level-3 "let it" shift; nothing pays. Mine; confirmed by LO 2026-11-01 ("Signed").

## The lines (mine, for signed by LO 2026-11-01)

**`back`:** "When you come off the floor Tom is in the back room, leaning on the shelf by the tip jar, and he shuts the door behind you." · "You can still feel where the man's hand was." · Tom: "Reputation's going. People talk. And the tables are full." · "He doesn't sound angry. He sounds like he's done the sums."

**`line`:** Tom: "I'm not stopping you. I saw. I didn't stop it." · "He looks at the door, at the front of the café behind it, the big window on the street." · Tom: "Not by the window."

**`where`:** Tom: "Anywhere the street can't see. That's all I'm saying." · *(thought, low)* "Say sorry. Keep the job." / *(high)* "He watched. He didn't stop it."

**`yes`:** "Tom nods once, and opens the door for you, and doesn't look at you while you go past him."

**`tips`:** Tom: "Then keep them. Not by the window." · "His ears go red, the way they did at the tip jar."

The thoughts on `where` show by her stage (Corruption under 20 the low, 20 and over the high; she is 20 and over by
the gate's level-3 shift, so in practice the high line shows; the low is kept for a reset).

## What changes after
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
