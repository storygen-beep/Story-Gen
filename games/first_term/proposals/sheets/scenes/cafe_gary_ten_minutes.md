# [REVIEW] Scene — cafe_gary_ten_minutes

> A draft for LO to place. Written 2026-10-08. The repeat Tom B 4 turns into: one entry of the shift-event pool
> (`cafe_shift_events`). An explicit pool scene, so its beats are written out here.

| row | answer |
|---|---|
| system · pool | the café job · `cafe_shift_events` |
| where · when | booth four, a weekday shift 14:30–18:00, when Gary is in |
| gate | `gary_ten_minutes_open` (Tom B 4) · Corruption 40 · Gary present |
| the price on the button | "$20 — Tom takes half" · money add +10 |
| two voices | reluctant: Corruption 40–49 (guess) · eager: 50 or more |
| what she wears here (test 8) | her café uniform: the café's dress rule |
| BRAKE (S9) | once a shift, on the trigger |
| raises | corruption add +1, until she is past Bold (repeat raise) |
| the crude-word ceiling | Tom's middle column: tits, cock · early: ass, tits · no cunt, cum, fuck |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `ask` | Tom at the counter: "Gary's in." One line | no | "Sit with him. ($20 — Tom takes half)" → `ten` · "No." → the shift | none |
| `ten` | reluctant or eager, by her Corruption | yes | "Time." → the shift · "That's enough, Gary." → the shift | money add +10 (or +5 if stopped) · corruption add +1 |

No history words on either voice: the screen repeats (`register.md`, the truth rule).

## The two voices, written

**Reluctant** · 87 words · explicit words 4 (cock, nipple ×2, tits) · median sentence 11 · Tom's middle column: tits, cock · early: ass, tits · no cunt, cum, fuck

> Gary pats the seat in booth four. "Ten minutes, sweetheart." You sit down stiffly and start counting. His hand lands on your bare thigh under the table, warm and heavy. His other hand stays flat on the tabletop, where your rule keeps it. His eyes drop to your tits and stay there. His cock is hard in his slacks, pressed against your hip. You don't want it, but your nipples tighten against your uniform. His thumb strokes your thigh, and your nipples stiffen harder under his stare.

**Eager** · 90 words · explicit words 4 (cock ×2, nipple, tits) · median sentence 9 · act rung: hands · Tom's middle column: tits, cock · early: ass, tits · no cunt, cum, fuck

> You take Gary's hand and put it on your bare thigh yourself. You slide closer in booth four and lean in slow, so your tits push at your uniform under his nose. His cock strains his slacks. You smile at it. Your nipples are hard, and he stares at them. "Sweetheart," he breathes. His other hand lifts off the table, but you tap it back down. His palm creeps up your thigh. You stop it at the very top with your own hand, and his cock jerks against his slacks.

Both last sentences stay on the body; `--beat` flags neither.

## Why — the source of each key choice

| key choice | source |
|---|---|
| a paid repeatable with two voices and a stop | `the-arc.md` A15 · gate "her climb" |
| Gary's ten minutes as a shift event | the job sheet (LO, 2026-10-08) |
| the prose | `v2-prose`, measured by `gates.py --beat`, 2026-10-08 |
| the voice edge at 50, the half pay on a stop | guess |
