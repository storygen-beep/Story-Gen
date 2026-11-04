# [READY] Scene — mark_06_our_arrangement
> Signed by LO: LO, 2026-11-04.

> Changed 2026-11-04 to match the build; signed by LO 2026-11-04. her_line row and the `keep` thought: what the build says; the paying and losing-count lines are gone (Q6).

> Changed 2026-11-04 to match the build; signed by LO 2026-11-04. "Middle of the night." is "Late."

> Changed 2026-11-03 to match the build (third alignment pass); signed by LO 2026-11-04. the buttons as built; his card line, no locked button; the step row. file and line cites cut.

> **Changed 2026-11-01, signed by LO 2026-11-01 ("Signed")** (DECISIONS 99–115): Mark's release-1 ladder (`sheets/people/npc_mark.md`, signed). Reworked as his step 4 of 4, the top step. Changed: the reason (he saw her come out of Ryan's room; the paid couch is cut), the gate, the lines that named the couch; her voice row; the locked button after it.

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08. Every Mark step is written twice, by his Power: his terms (M) or hers (E).

| row | answer |
|---|---|
| person · step | `npc_mark` · 4 of 4, top step (was 6, Mark A 6; the canvas id stays) |
| where · when | the garage, `home_garage` · Mon, Tue, Thu, Fri 19:00–22:00 (his person sheet's row) |
| gate | `mark_step` eq 3 · `ryan_step` gte 4 (Ryan's feet-in-his-lap night done) · the boost off (was Corruption 40 · his Want 50) |
| want | he can't hold her look at the Sunday table (the leak); the built "since the couch" line is cut |
| next step | it becomes a deal: each holds the other's secret |
| hook | "So we each keep one." The Sunday table changes after it · his card's last line: "Mark, later. (After the house is yours.)" |
| what she wears here | not named |
| which version | Power 50 or more (guess): his version · under 50: hers |
| explicit? | no: a talk |
| who notices | Mark knows about Ryan; she knows about Vance |
| what she risks | Mark telling Laura |
| her_line_low · her_line_high | low: none built · high, as built: her button "Vance's letter is in the drawer." | The built thought on `keep` ("Your secret for his. He thinks it's even, but it isn't.") is the high side. |
| top step, declared not a payoff | taste rule 2: Mark's release-1 ladder is the rent (LO, no sex with Mark this release) |

## The step row (filled from the build, 2026-11-03)

**Kind · stage:** a talk: his top step, declared not a payoff (no sex with Mark this release).

| the moment | who sees or knows | what she risks | how she says yes | his move | does it finish | what changes after |
|---|---|---|---|---|---|---|
| they trade secrets: Ryan's door for Vance's letter | Mark knows about Ryan; she knows about Vance | Mark telling Laura | "Vance's letter is in the drawer." · "Wait for him to answer." | "I saw you come out of Ryan's room." | not a sex act, declared (LO: no sex with Mark this release) | `mark_arrangement`; the Sunday table's new lines |

## Branch map — one row per screen

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op |
|---|---|---|---|---|
| `start`, his version (Power 50+) | M: "I saw you come out of Ryan's room. Late." Then: "Our arrangement. Your mother has enough to worry about." | no | "Vance's letter is in the drawer." → `keep` (his Power −3) · "There's no arrangement." → `no` (parked) | none |
| `start`, hers (under 50) | E: he says what he saw; she names Vance's letter first: "Vance's letter is in the drawer. So we each keep one." | no | "Wait for him to answer." → `keep` | none |
| `no` | "There is now, @player. Since Ryan's door." | no | "Leave him to the radio." → the hall | his Power add +2 |
| `keep` | he wipes his hands on a rag and nods | no | "Deal." → the hall | Mark's Want add +10 · `mark_step` set 4 · `mark_06_done` set · `mark_arrangement` set |

**The parked no** ("There's no arrangement."): as built, his Power +2, the step waits 3 days; its line changes (below).

## The lines that change (mine, signed by LO 2026-11-01; the rest stand as built)

| where | built line | new line |
|---|---|---|
| `start`, first line | "He's been off with you at dinner since the couch, eating with his eyes on his plate." | cut; the line ends "Mark's at his workbench with the radio on and his hands black with oil. He hears you come in and doesn't turn round." |
| `start`, both versions, new first line | — | Mark, still facing the bench: "I saw you come out of Ryan's room. Late." |
| `start`, hers | "Vance's letter is in the drawer. And your hand was on my leg. So we each keep one." | "Vance's letter is in the drawer. So we each keep one." |
| `no` | "There is now, @player. There has been since the couch." | "There is now, @player. Since Ryan's door." |

"Late" and not "at midnight" or "middle of the night": his step 4 runs 22:00–00:00, so she can leave by 22:20.

## After it
- His guidance card ends on: "Mark, later. (After the house is yours.) His Want still counts: every look you give him is kept for the next release." No locked button (DECISIONS 132).
- The Sunday table changes (`mark_sunday_table.md`).
- `mark_arrangement` is stored for a later release (Mark at Ryan's door); nothing else reads it this release.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene, both versions | the arc ideas, Mark A 6 |
| `mark_arrangement` as a key | guess |
| the new reason, the gate, the locked button | `proposals/MARK_R1_LADDER.md`, step 4 reworked (signed 2026-11-01) |
