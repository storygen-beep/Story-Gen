# [READY] Place — Library
> Changed 2026-11-09 (DECISIONS 210, LO: "Go ahead"): showing off to get something, new section at the end. Signed by LO 2026-11-09 ("Sign them").
> Signed by LO: LO, 2026-11-04.

> Changed 2026-11-03 to match the build (third alignment pass); signed by LO 2026-11-04. New section: what the heat proposal built here. Points at the copy fixes it took.

> Signed by LO: LO, 2026-10-08. Re-signed 2026-10-29 ("sign all", in chat).

> Placed in sheets/ 2026-10-08. Written 2026-10-08 against the system sheets. Id `library`.

| row | answer |
|---|---|
| kind | destination |
| ENTERED FROM | campus |
| labels — what kind of place | `zone:campus`, `public`, `she_can_study` |
| hours | Mon–Fri 08:00–20:00 |
| closed text | "The library is closed." |
| hidden until | no |
| fill — word budget | 1,500 words (ledger, unchanged) |
| door | no |
| dress code or wanted state | none |

## On entering

| auto-fires | who is here, and when | things to do alone | ways out |
|---|---|---|---|
| none | Nadia: Mon, Tue, Wed, Fri 14:30–18:00 | study | campus |

## Rows (`serves`)

| row | kind | system | cost and effect, with op | BRAKE | on a screen? |
|---|---|---|---|---|---|
| study | work | college | energy add −10 · `intelligence` add +1 | twice a day, on the trigger | yes, short |
| Nadia sits down | person | college · Hale's ladder | one line about Hale | once a day, her window | yes |
| find a book in the back stacks | sex scene | the way up (DECISIONS 79) | `library_back_stacks`: the couple pays nothing · "Stay behind the shelf." corruption add +1, cap 19 | once a day | yes: explicit |

> Changed 2026-10-29 (the back-stacks row, LO's pick of 2026-10-29); re-signed by LO 2026-10-29.

## Built from the heat proposal (signed 2026-11-03)

The plan: `proposals/FIRST_TERM_HEAT_PROPOSAL_20261103.md`. What the build has here:

**Walk-ins.** Her activity rolls on entry (1 in 4 at her lowest band, more higher up); on a hit someone walks in. A man's pay sits on the moment; her cover pays 0.

| who walks in | her activity | when | his pay, on the moment | her bolder answers |
|---|---|---|---|---|
| Nadia | Study | Mon, Tue, Wed, Fri 14:30–14:45 | none: no meter | a line only, no pay |

**Acts, rungs and pools.**

| what | where | buttons and pays |
|---|---|---|
| one aisle closer (C1) | the back stacks | "Move one aisle closer." Corruption 5; she stays hidden |

## Rows a gate needs

| row | gate |
|---|---|
| study at every open hour | a destination is never open and exit-only |
| Nadia walks in on her study | the walk-in floor |
| `intelligence` fed here | a meter is read (exams read it) |

**Copy:** lines here were rewritten from `proposals/COPY_FIXES_B.md` (signed with the a2 sheets, DECISIONS 125).

## Why — the source of each key choice

| key choice | source |
|---|---|
| the library feeds intelligence | LO, chat (SYSTEMS §1) |
| Nadia's afternoons | LIVES §3 |
| hours | LO took the guess, 2026-10-08 |
| the study cap | guess |

## His notes (2026-11-09, DECISIONS 210)

Row "Sit with the study guy", weekdays 08:00-19:30, once a day. The study guy trades his Business notes in the library, one chapter a day, weekdays, from her fourth week until the Business midterm, once she is Daring (Exhibitionism 20). Asking nicely gets a no. A show at her stage gets a chapter: sitting on his notes (20, pays to 39); her panties under the table (40, pays to 59); a flash in the back stacks (60, pays to 79). Each chapter: hidden count `study_notes` +1, Intelligence +1, his hidden `want` +1 (his lines change with it). Five chapters open "You know his notes by heart." at the Business midterm (grade +8, more than copying); at his want 5 one look gets his paper. Source: `iterations/002/build_scripts/goals.py`, `college.py`.
