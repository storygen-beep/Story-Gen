# [REVIEW] Place — Kitchen

> Changed 2026-11-04 (LO's answer Q6: the rent page is the one count; Mark's Sunday table counts nothing). Waits for LO's re-sign.

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign. The drawer reads `rent_short`. New section: what the heat proposal built here. Points at the copy fixes it took.

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08 against the system sheets. Id `home_kitchen`.

| row | answer |
|---|---|
| kind | destination |
| ENTERED FROM | home_hall |
| labels — what kind of place | `zone:home`, `private` |
| hours | always |
| closed text | none: always open |
| hidden until | no |
| fill — word budget | 30,000 words (was 28,000): +2,000 for the meals, coffee, cooking and dishes · the anchor (question 51; COVERAGE settles it in batch 4) |
| door | no: a shared room. Who is inside is a row, not a door |
| dress code or wanted state | none required · what she wears to the Sunday table is read (Mark A 3) |

## On entering

| auto-fires | who is here, and when | things to do alone | ways out |
|---|---|---|---|
| Sunday 08:00–12:00, once: Mark's Sunday table (his step, or the table), after the rent page has taken the money; no second count (Q6) | Laura: weekdays 06:30–08:00 | the drawer: letters, Vance's after a short week | the hall |
| Laura's day 1 breakfast meeting | Laura: Mon, Tue, Thu, Fri, Sun 18:00–22:00 |  |  |
|  | Mark: Mon, Tue, Thu, Fri 18:00–19:00 (dinner) · Wednesday 18:00–22:00 · all Sunday 08:00–22:00 |  |  |
|  | Ryan: Mon, Tue, Thu, Sun 18:00–19:00 (dinner) |  |  |

## Rows (`serves`)

| row | kind | system | cost and effect, with op | BRAKE | on a screen? |
|---|---|---|---|---|---|
| Laura | person | Laura's ladder | Laura's Warmth add +2 a talk | once per window, on the trigger | yes |
| Mark | person | Mark's ladder · money and rent | Mark's Want read: how he looks at her (colour) | once per window, on the trigger | yes |
| the Sunday table | work | money and rent | as the money sheet: `paid_full_streak` add +1 or set 0 | Sunday morning, once | yes |
| the drawer | work | money and rent | none · reads `rent_short` and the letter · the letter says what Mark owes Vance only after `knows_mark_debt` (Mark A 2); before it, bills | none needed: it writes nothing | yes |

**The anchor.** 28,000 words: breakfast with Laura, Wednesday with Mark, the Sunday table in two versions, the family table, the wine.

## Everyday at home (system `home_life`)

Alone, each is its own plain row. With Laura or Mark there, it is a choice inside their hub here (their sheets carry the lines).

| row | kind | system | cost and effect, with op | BRAKE | on a screen? |
|---|---|---|---|---|---|
| breakfast | need | home_life · energy | 15 min · energy add +10 · with Laura (Mon–Fri 06:30–08:00) or Mark (Sun 08:00–10:00): their +1 | `ate_breakfast`, 12 h | yes: who is at the table |
| coffee | need | home_life · energy | 10 min · energy add +5 · with Laura or Mark, as breakfast: +1 | `had_coffee`, 12 h | yes, one line |
| dinner | need | home_life · energy | 30 min · energy add +15 · with Laura (Mon, Tue, Thu, Fri, Sun), Mark (Mon–Fri, Sun) and Ryan (Mon, Tue, Thu, Sun), 18:00–19:00, each +1 · Wednesday is Mark alone · Sunday dinner reads `room_tidy` and clears it | `ate_dinner`, 12 h | yes: who sits down |
| help cook | person | home_life | 30 min · energy add −5 · Laura (18:00–19:00, her evenings) or Mark (Wed): +1 | `helped_cook`, 12 h · only when someone cooks | yes |
| dishes | work | home_life | 20 min · energy add −5 · alone plain · with Laura or Mark: +1 | `did_dishes`, 12 h | yes |
| a glass with Laura | person | home_life · Laura's ladder | 30 min · Warmth add +1 · `drinks_boost` on · after Laura C 3 | `had_drink_home`, 12 h | yes |
| a random event | work | home_life | by the event (the hall sheet lists them) | one a day, 1 in 4 on entering | yes |

**The table tells the truth.** Weekday breakfast is Laura only; weekend breakfast is alone except
Sunday, when Mark is in here from 08:00. Dinner, 18:00–19:00: Laura, Mark and Ryan on Monday, Tuesday, Thursday and Sunday; Laura and Mark on
Friday (Ryan has Kayla); Mark alone on Wednesday (question 54).

## Built from the heat proposal (signed 2026-11-03)

The plan: `proposals/FIRST_TERM_HEAT_PROPOSAL_20261103.md`. What the build has here:

**Walk-ins.** Her activity rolls on entry (1 in 4 at her lowest band, more higher up); on a hit someone walks in. A man's pay sits on the moment; her cover pays 0.

| who walks in | her activity | when | his pay, on the moment | her bolder answers |
|---|---|---|---|---|
| Ryan | Make breakfast, Make a coffee | Sat 07:30–08:15; Sun 07:30–10:00 | his Want +2 | "Don't move." Corruption +1, cap 19/39 by her band; "Push back into him." Corruption +1, cap 59 |
| Mark | Make breakfast, Make a coffee | Sat 08:15–08:30 | his Want +2 | "Don't move." Corruption +1, cap 19/39 by her band; "Push back into him." Corruption +1, cap 59 |

## Rows a gate needs

| row | gate |
|---|---|
| 30,000 words, about 25% of the new total (COVERAGE, batch 4) | location fill |
| the drawer, at every hour | a destination is never open and exit-only |
| Laura and Mark rows each have a hub | standing surface |

**Copy:** lines here were rewritten from `proposals/COPY_FIXES_A.md`, `proposals/COPY_FIXES_C.md` (signed with the a2 sheets, DECISIONS 125).

## Why — the source of each key choice

| key choice | source |
|---|---|
| the kitchen is the anchor | the board, 2026-10-08 · `the-release.md` § The first release |
| Sunday count, Mark collects | LO, 2026-10-07 (SP4) |
| the drawer | LIVES §4 (Vance's letter, any night) |
| Warmth +2 a talk | guess |
| the everyday rows | LO, 2026-10-08 (the everyday picks) · system `home_life` · times and numbers guess |
| the dinner hour, 18:00–19:00 | LO, 2026-10-08 (question 54) |
| fix from the false-line sweep | sweep A1-13 (2026-10-08) |
