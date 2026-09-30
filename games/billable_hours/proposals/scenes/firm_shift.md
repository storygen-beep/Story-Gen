# [REVIEW] Scene — firm_shift (repeatable, "Work a shift") + walk-in

| row | answer |
|---|---|
| where · when | firm · Mon–Fri 09:00–17:00 · repeatable |
| BRAKE | `worked_today` (on the trigger); energy gte 20 |
| pays | money add +70; energy add −30; time 240 |
| walk-in | one canvas, four bands on nerve: 0–9 an associate's remark · 10–19 Theo's leak (Mon, Wed) or Ethan at the copier · 20–29 Callahan asks her to stay late (v0.2 hook) · 30+ the associate in the copy room (B10, explicit) |

| node | what happens | explicit? | exits | effects, with op |
|---|---|---|---|---|
| shift | filing, the copier, Diane's "Lunch, sweetheart?" | no | "Clock out." → firm | money add +70 · energy add −30 · `worked_today` set |
| walk-in (0–9) | an associate: "Callahan likes the short ones." | no | "Ignore him." → firm | office_talk add +1 |
| walk-in (10–19) | Theo checks his watch / Ethan leans on the copier | no | "Get back to work." → firm | office_talk add +1 |
| walk-in (20–29) | Callahan: "Stay tonight. I want to see how you work late." | no | "Say you'll think about it." → firm | office_talk add +1 · sets `callahan_asked_late` (read in v0.2) |
| walk-in (30+) | **B10** below | **yes** | "Button your blouse and go back to your desk." → firm | office_talk add +1 · nerve add +1 |

## Explicit beats (written by v2-prose; re-measured by the author on its own file)

**B10**

> The copier is running when the door clicks shut. The associate presses in behind you. "Callahan likes the short ones. So do I." He pops your blouse open and grabs your tits, thumbs dragging over your nipples. His cock is hard through his trousers, shoved into your ass. You push back and grind on it. He squeezes your tits harder and ruts against your ass while the copier spits out warm pages.

*Measured: 72 words · 6 explicit (ass, cock, nipple, tits) · median 9 · last sentence on the body · ceiling: role:an associate (cock, tits, ass).*
