# [READY] Scene — college_class_figure
> Signed by LO: LO, 2026-11-04.
> Changed 2026-11-04, writing pass: lines brought to the build (fresh text per room, her voice by level, the reader's fixes); signed by LO 2026-11-04.

> Changed 2026-11-03 to match the build (third alignment pass); signed by LO 2026-11-04.

> The signed plans behind this page: `proposals/COPY_FIXES_B.md`.

> **Changed 2026-11-02** (reader fails a3, signed by LO 2026-11-02, DECISIONS 131): rows 25–26, the risky slot names one watcher: the button is "Lean into your easel and let him look.", the class line is "The guy at the next easel has stopped drawing the model. What you're wearing is doing its job.", the screen is titled "Let him look" (the build `meet_figure` copies it).

> Changed 2026-11-04 to match the build; signed by LO 2026-11-04. The 2026-10-29 locked-button note (DECISIONS 90) is corrected: "Needs Corruption 60" and "Needs Exhibitionism 60" are no longer in the game, because the buttons for scenes this release does not write were removed (DECISIONS 132). Any line below that still names one is superseded by that row.

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08. The figure-drawing class canvas (`college_class_figure`): the class draws a nude model (a woman, 25).

| row | answer |
|---|---|
| system · pool | college · `college_class_figure` |
| where · when | the lecture hall · Tue, Thu 08:30 · Wed 13:00 (starts in its first 15 minutes) |
| gate | `opening_done` · the first class (`meet_figure`) meets the lecturer, the model, the cocky guy |
| who | the model, the art lecturer, Zoe, Jake, the cocky guy · Zoe's sentence ("Zoe kicks your ankle") shows only after `zoe_met`; before it she is "the girl at the next easel" |
| want | the cocky guy at the next easel draws her, not the model |
| next step | "Lean into your easel and let him look." (Exhibitionism 20) |
| hook | his midterm price, his party hookup, Zoe's dares with him |
| what she wears here | not named; no dress code for her |
| BRAKE | once a day, on the trigger |
| raises | none: it is a class (her grade moves by her row choice) |
| the crude-word ceiling | tits, nipples, ass, naked · no cock, cunt, pussy, fuck, cum (LO, 2026-10-08) |

## Branch map — as built (2026-11-03)

One row per exit. Read from the build; it replaces the drafted map.

**`college_class_figure`** — Lecture Hall · Tue/Thu 08:30-08:45 · Wed 13:00-13:15 · needs `opening_done` · repeatable · 1 a day

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `class` | The model drops her robe on the platform and steps up naked under the lamp. | yes | "Focus. (90 minutes, 10 energy)" (Energy 20+) → `focus` | Figure drawing grade +2 · Intelligence +1 · costs Energy 10 |
| | | | "Chat." → `chat` | — |
| | | | "Doze." → `doze` | Energy +5 (cap 100) |
| | | | "Lean into your easel and let him look." (Exhibitionism 20+) — 2 versions, by clothes → `risky` | Exhibitionism +1 (cap 39) |
| | | | "Skip it." → Campus | Figure drawing grade -2 |
| `focus` | You draw for ninety minutes without looking up. | no | "Pack up (1h 30m)." → Lecture Hall | — |
| `chat` | You draw with one hand and whisper with the girl at the next easel. | no | "Pack up (1h 30m)." → Lecture Hall | — |
| `doze` | The lamp is warm and the room is quiet except for charcoal on paper. | no | "Wake up (1h 30m)." → Lecture Hall | — |
| `risky` | You lean into your easel, slow, and your tits hang heavy against what you're wearing, your … | yes | "Pack up, slowly (1h 30m)." → Lecture Hall | — |

**`meet_figure`** — Lecture Hall · Tue/Thu 08:30-08:45 · Wed 13:00-13:15 · needs `opening_done` · not `art_lecturer_met` · one time

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `first` | Easels in a horseshoe round a platform with a stool on it, and a woman in … | no | "Set up your easel." → `easel` | — |
| `easel` | The guy at the next easel is in a team jacket: Jake's teammate, the cocky one. | no | "Find your charcoal." → `class` | `art_lecturer_met` set · `cocky_guy_met` set · `figure_model_met` set |
| `class` | The model drops her robe on the platform and steps up naked under the lamp. | yes | "Focus. (90 minutes, 10 energy)" (Energy 20+) → `focus` | Figure drawing grade +2 · Intelligence +1 · costs Energy 10 |
| | | | "Chat." → `chat` | — |
| | | | "Doze." → `doze` | Energy +5 (cap 100) |
| | | | "Lean into your easel and let him look." (Exhibitionism 20+) — 2 versions, by clothes → `risky` | Exhibitionism +1 (cap 39) |
| | | | "Skip it." → Campus | Figure drawing grade -2 |
| `focus` | You draw for ninety minutes without looking up. | no | "Pack up (1h 30m)." → Lecture Hall | — |
| `chat` | You draw with one hand and whisper with the girl at the next easel. | no | "Pack up (1h 30m)." → Lecture Hall | — |
| `doze` | The lamp is warm and the room is quiet except for charcoal on paper. | no | "Wake up (1h 30m)." → Lecture Hall | — |
| `risky` | You lean into your easel, slow, and your tits hang heavy against what you're wearing, your … | yes | "Pack up, slowly (1h 30m)." → Lecture Hall | — |

## The explicit beats, as built (2026-11-03)

Every screen the build counts as explicit (3+ words from the frozen list), word for word, with its measurement. It replaces the drafted text.

**`college_class_figure` · `class`** — 177 words · 8 counted: naked, tits, nipple, ass, nipple, tits, nipple, cock · ceiling: tits, nipples, ass, naked

> The model drops her robe on the platform and steps up naked under the lamp. She sits on the stool and turns her shoulder to the room. Her tits are heavy. They sway when she settles. Her nipples are dark and tight in the cold air. Your charcoal follows the curve of her ass where it spreads on the stool. You draw her thighs, pressed together, and the soft crease between them. You can't stop looking. Your face burns. Your own nipples go hard. The lecturer walks the rows behind you.
>
> Look at the weight of her.
>
> She says.
>
> Draw that.
>
> Zoe kicks your ankle under the easel.
>
> The girl at the next easel kicks your ankle and grins.
>
> You keep drawing the heavy swing of the model's tits, but it's your nipples that ache.
>
> At the next easel, the cocky guy isn't drawing the model. He's drawing you.
>
> Too tired to hold the charcoal straight. Doze, or skip.
>
> The guy at the next easel has stopped drawing the model. His stare crawls over you, and your nipples go tight.

**`college_class_figure` · `risky`** — 164 words · 4 counted: tits, nipple, nipple, tits · ceiling: tits, nipples, ass, naked

> You lean into your easel, slow, and your tits hang heavy against what you're wearing, your nipples showing through it. The guy at the next easel gives up on the model completely.
>
> You lean into your easel, slow, and your skirt rides up the backs of your thighs. The guy behind you gives up on the model completely.
>
> The lecturer stops behind you, looks at your drawing, looks at you.
>
> Clothes stay on in my class, @player. Unless you're on the platform.
>
> I'm supposed to be drawing her. I've drawn you three times.
>
> Then draw me properly.
>
> Hold still, then. Don't move. God, don't move.
>
> Like this?
>
> Exactly like that. Keep your legs exactly like that.
>
> Your face burns. Anyone watching could tell you did that on purpose, and your nipples are hard anyway.
>
> You liked that. You'll do it again next class, and give them a little more.
>
> That was nothing. You want to be looked at properly, tits and all, and soon.

**`meet_figure` · `class`** — 177 words · 8 counted: naked, tits, nipple, ass, nipple, tits, nipple, cock · ceiling: tits, nipples, ass, naked

> The model drops her robe on the platform and steps up naked under the lamp. She sits on the stool and turns her shoulder to the room. Her tits are heavy. They sway when she settles. Her nipples are dark and tight in the cold air. Your charcoal follows the curve of her ass where it spreads on the stool. You draw her thighs, pressed together, and the soft crease between them. You can't stop looking. Your face burns. Your own nipples go hard. The lecturer walks the rows behind you.
>
> Look at the weight of her.
>
> She says.
>
> Draw that.
>
> Zoe kicks your ankle under the easel.
>
> The girl at the next easel kicks your ankle and grins.
>
> You keep drawing the heavy swing of the model's tits, but it's your nipples that ache.
>
> At the next easel, the cocky guy isn't drawing the model. He's drawing you.
>
> Too tired to hold the charcoal straight. Doze, or skip.
>
> The guy at the next easel has stopped drawing the model. His stare crawls over you, and your nipples go tight.

**`meet_figure` · `risky`** — 164 words · 4 counted: tits, nipple, nipple, tits · ceiling: tits, nipples, ass, naked

> You lean into your easel, slow, and your tits hang heavy against what you're wearing, your nipples showing through it. The guy at the next easel gives up on the model completely.
>
> You lean into your easel, slow, and your skirt rides up the backs of your thighs. The guy behind you gives up on the model completely.
>
> The lecturer stops behind you, looks at your drawing, looks at you.
>
> Clothes stay on in my class, @player. Unless you're on the platform.
>
> I'm supposed to be drawing her. I've drawn you three times.
>
> Then draw me properly.
>
> Hold still, then. Don't move. God, don't move.
>
> Like this?
>
> Exactly like that. Keep your legs exactly like that.
>
> Your face burns. Anyone watching could tell you did that on purpose, and your nipples are hard anyway.
>
> You liked that. You'll do it again next class, and give them a little more.
>
> That was nothing. You want to be looked at properly, tits and all, and soon.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the class draws a nude model; a woman | LO, chat 2026-10-07 (SYSTEMS, decided item 1) |
| her own posing waits | SYSTEMS §1 · SP7 call 1 |
| the prose | `v2-prose`, measured by `gates.py --beat`, 2026-10-08 |
| she meets the cocky guy at her first Figure drawing | LIVES §6 (met at their first class) · ledger change 26 |
| fix from the false-line sweep | sweep A5-13 (2026-10-08) |
