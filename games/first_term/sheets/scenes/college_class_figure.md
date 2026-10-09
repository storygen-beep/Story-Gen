# [READY] Scene — college_class_figure

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08. The figure-drawing class canvas (`college_class_figure`): the class draws a nude model (a woman, 25).

| row | answer |
|---|---|
| system · pool | college · `college_class_figure` |
| where · when | the lecture hall · Tue, Thu 08:30 · Wed 13:00 |
| gate | none: every figure-drawing class |
| who | the model, the art lecturer, Zoe, Jake, the cocky guy · Zoe's sentence ("Zoe kicks your ankle") shows only after `zoe_met`; before it she is "the girl at the next easel" |
| what she wears here (test 8) | not named; no dress code for her |
| BRAKE (S9) | once per class window |
| raises | none: it is a class (her grade moves by her row choice) |
| the crude-word ceiling | tits, nipples, ass, naked · no cock, cunt, pussy, fuck, cum (LO, 2026-10-08) |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `pose` | the model drops her robe and poses; she draws her | yes | the class rows: Focus · Chat · Doze · Skip | as the college sheet · first class: `cocky_guy_met` set |
| locked | posing nude for the class herself | — | "Pose for the class." Needs Hungry | — |

## The explicit screens, written

**`pose`** · 124 words · explicit words 7 (ass, naked, nipple, tits) · median sentence 9 · every class

> The model drops her robe on the platform and steps up naked under the lamp. She sits on the stool and turns her shoulder to the room. Her tits are heavy. They sway when she settles. Her nipples are dark and tight in the cold air. Your charcoal follows the curve of her ass where it spreads on the stool. You draw her thighs, pressed together, and the soft crease between them. You can't stop looking. Your face burns. Your own nipples go hard. The lecturer walks the rows behind you. "Look at the weight of her," she says. "Draw that." Zoe kicks your ankle under the easel. You keep drawing the heavy swing of the model's tits, but it's your nipples that ache.

No history words on any screen: each one repeats.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the class draws a nude model; a woman | LO, chat 2026-10-07 (SYSTEMS, decided item 1) |
| her own posing waits | SYSTEMS §1 · SP7 call 1 |
| the prose | `v2-prose`, measured by `gates.py --beat`, 2026-10-08 |
| she meets the cocky guy at her first Figure drawing | LIVES §6 (met at their first class) · ledger change 26 |
| fix from the false-line sweep | sweep A5-13 (2026-10-08) |
