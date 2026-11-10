# [READY] Place — Bathroom

> **Changed 2026-11-10** (LO's playtest; DECISIONS 223):
> - Touching herself in the shower needs the room empty, so it no longer plays while Laura (or Mark) is in.
> - 2026-11-10, DECISIONS 224 (LO: "an option while she is taking shower not a separate option"): touching herself is a choice inside the shower, "Touch yourself." on the shower's first screen (Curious). The separate bathroom link `touch_shower` is gone. Its ways out are the shower's own, with Corruption +1 and 10 more minutes.
> - Laura has her own door screen, `hub_laura_bathroom` ("Laura's in there"). It pays nothing; the shower gap still takes her face when it's open.
> Signed by LO: LO, 2026-11-04.

> Changed 2026-11-03 to match the build (third alignment pass); signed by LO 2026-11-04. New section: what the heat proposal built here. Points at the copy fixes it took.

> **Changed 2026-11-01, re-signed by LO 2026-11-02** ("Signed, go ahead and build"; DECISIONS 124, the heat ladder a2): its gate or pay changes; the row is in `sheets/HEAT_LADDER_A2.md`.

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08 against the system sheets. Id `home_bathroom`.

| row | answer |
|---|---|
| kind | destination |
| ENTERED FROM | home_hall |
| labels — what kind of place | `zone:home`, `private`, `has_shower`, `she_can_undress` |
| hours | always |
| closed text | none: always open |
| hidden until | no |
| fill — word budget | 5,000 words (ledger, unchanged) |
| door | no: a shared room. Who is inside is a row, not a door |
| dress code or wanted state | none |

## On entering

| auto-fires | who is here, and when | things to do alone | ways out |
|---|---|---|---|
| Ryan A 2: his phone on the sink, weekday 07:00–07:30 | Ryan: weekdays 06:45–07:30 (he showers first) | shower · a quick look in the mirror | the hall |
| Ryan A 6, Saturday morning (from his room) |  |  |  |

## Rows (`serves`)

| row | kind | system | cost and effect, with op | BRAKE | on a screen? |
|---|---|---|---|---|---|
| shower | need | hygiene | hygiene add +50 (guess) · 20 minutes | once a day, on the trigger | yes: her body, never a toast |
| someone walks in | person | hygiene · wardrobe | rolled on the shower: Ryan, Kayla, Mark | once a day | yes |
| touch herself | work | her stage · Corruption | Curious: corruption add +1, first time each day (guess) | once a day, on the trigger | yes: explicit, her body |
| Ryan's in there | person | — | none · "Ryan's in there." weekday mornings | his window | yes, one line |

## Built from the heat proposal (signed 2026-11-03)

The plan: `proposals/FIRST_TERM_HEAT_PROPOSAL_20261103.md`. What the build has here:

**Walk-ins.** Her activity rolls on entry (1 in 4 at her lowest band, more higher up); on a hit someone walks in. A man's pay sits on the moment; her cover pays 0.

| who walks in | her activity | when | his pay, on the moment | her bolder answers |
|---|---|---|---|---|
| Ryan | Take a shower | Sun, Mon, Tue, Wed, Thu 19:00–00:00; Sat, Sun 07:30–14:00 | his Want +2 | "Don't grab it straight away." Exhibitionism +1, cap 19; "Keep washing." Exhibitionism +1, cap 39; "Turn round." Exhibitionism +1, cap 59 |
| Kayla | Take a shower | Fri 18:00–22:00 | none: no meter | "Don't grab it straight away." Exhibitionism +1, cap 19; "Keep washing." Exhibitionism +1, cap 39; "Turn round." Exhibitionism +1, cap 59 |
| Mark | Take a shower | Sat 14:00–17:00 | his Want +2 | "Don't grab it straight away." Exhibitionism +1, cap 19; "Keep washing." Exhibitionism +1, cap 39; "Turn round." Exhibitionism +1, cap 59 |

**Acts, rungs and pools.**

| what | where | buttons and pays |
|---|---|---|
| the unlocked door (C4) | the shower | "Leave the door unlocked." Exhibitionism 5, +1, cap 19; it stays unlocked until "Lock it again."; the walk-in odds rise to 0.5–0.9 |

## Rows a gate needs

| row | gate |
|---|---|
| the shower, every day | a need can be met every day |
| a walk-in on the shower | the walk-in floor |

**Copy:** lines here were rewritten from `proposals/COPY_FIXES_A.md` (signed with the a2 sheets, DECISIONS 125).

## Why — the source of each key choice

| key choice | source |
|---|---|
| touching herself, from Curious | LO, 2026-10-08 (question 13) |
| the shared bathroom, an event roll | LO, chat 2026-10-06 (SYSTEMS §6) |
| Ryan showers first | IDEA §4 (Laura's rule) |
| hygiene +50 | guess |
