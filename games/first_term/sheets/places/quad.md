# [READY] Place — Quad
> Changed 2026-11-09 (DECISIONS 210, LO: "Go ahead"): showing off to get something, new section at the end. Signed by LO 2026-11-09 ("Sign them").
> Signed by LO: LO, 2026-11-04.

> Changed 2026-11-03 to match the build (third alignment pass); signed by LO 2026-11-04. New section: what the heat proposal built here. Points at the copy fixes it took.

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08 against the system sheets. Id `quad`.

| row | answer |
|---|---|
| kind | destination |
| ENTERED FROM | campus |
| labels — what kind of place | `zone:campus`, `outdoors`, `public` |
| hours | every day 07:00–22:00 |
| closed text | "The quad is dark and empty." |
| hidden until | no |
| fill — word budget | 3,000 words: 2,500 plus the 500 that were the campus page's (question 43) |
| door | no |
| dress code or wanted state | none |

## On entering

| auto-fires | who is here, and when | things to do alone | ways out |
|---|---|---|---|
| Zoe's meeting, first visit in her hours (`zoe_00_quad_meeting`) | Jake: Mon, Wed, Fri 08:30–11:45 | sit on the grass and hear what campus says | campus |
|  | Zoe: Tue, Thu, Fri 14:30–18:00 |  |  |

## Rows (`serves`)

| row | kind | system | cost and effect, with op | BRAKE | on a screen? |
|---|---|---|---|---|---|
| Jake | person | Jake's ladder | Jake B 2 here · his look (colour) | once per window, on the trigger | yes |
| Zoe | person | Zoe's ladder | her want shown first: her head in @player's lap | once per window, on the trigger | yes |
| sit on the grass | work | college · `campus_talk` | none · what she overhears reads `campus_talk` | none needed: it writes nothing | yes |

## Built from the heat proposal (signed 2026-11-03)

The plan: `proposals/FIRST_TERM_HEAT_PROPOSAL_20261103.md`. What the build has here:

**Walk-ins.** Her activity rolls on entry (1 in 4 at her lowest band, more higher up); on a hit someone walks in. A man's pay sits on the moment; her cover pays 0.

| who walks in | her activity | when | his pay, on the moment | her bolder answers |
|---|---|---|---|---|
| Jake's team | Sit on the grass | Mon, Wed, Fri 08:30–08:45 | none: no meter | "Leave it." Exhibitionism +1, cap 19 |
| Zoe | Sit on the grass | Tue, Thu, Fri 14:30–14:45 | none: no meter | "Leave her there." Corruption +1, cap 19; "Let her hand slide up your thigh." Corruption +1, cap 39 |

**Acts, rungs and pools.**

| what | where | buttons and pays |
|---|---|---|
| Jake shows her off (A3) | his quad hub | "Let him show them." Watched 60, Exhibitionism +1, cap 79 · "Let him in." both at 60, both +1, cap 79 · "Not in front of them." pays 0 |

## Rows a gate needs

| row | gate |
|---|---|
| `campus_talk` read here | a meter is read |
| the grass at every hour | a destination is never open and exit-only |

**Copy:** lines here were rewritten from `proposals/COPY_FIXES_B.md` (signed with the a2 sheets, DECISIONS 125).

## Why — the source of each key choice

| key choice | source |
|---|---|
| Zoe met here, week 1 | LO, 2026-10-08 (fix 1) |
| Jake's mornings, Zoe's afternoons | LIVES §3 |
| Zoe's leak on the quad | ARC_IDEAS, Zoe A step 0 |
| the grass row reads campus talk | LO, 2026-10-08 |
| the campus page's 500 words land here | LO, 2026-10-08 (question 43) |

## Zoe's crowd (2026-11-09, DECISIONS 210)

Row "Find someone for Zoe's party", every day 08:00-20:00, once a day: a guy on the grass by the path. Zoe texts once she has been to one of her parties and is Daring (Exhibitionism 20): bring her ten people (`phone.py` `zoe_crowd`; a no lets the text come back in a week, ignoring it costs her patience). After a yes, the quad, the gym and the canteen each have one ask a day, "Find someone for Zoe's party", until ten are coming (hidden count `zoe_crowd`). Asking plainly always gets a no and counts nothing. A show at her stage gets a yes: close (20, pays to 39); her panties under a short hem, or a stretch on the gym mats (40, pays to 59, campus talk +1); her bare tits for three seconds (60, pays to 79, campus talk +1). The screen after each yes says the count in that place's words. Source: `iterations/002/build_scripts/goals.py`.
