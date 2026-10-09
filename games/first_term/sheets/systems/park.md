# [READY] System — park

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08 from SYSTEMS §14 and the ledger's `park` card.
> Every number marked "guess" is new here and waits for your yes.

| row | answer |
|---|---|
| id · name | `park` · The park |
| place and hours | `park` · every day, 07:00–22:00 · the dark park after 22:00 is later |
| cost | time · running costs energy · a bench gives a little back |
| one ladder or two | one |
| people | Zoe, running Saturday and Sunday 08:00–10:00 · Ryan and Jake later |
| pool | `park_walk`, `park_run`, `park_watch_the_couple`, `park_hidden` · `daily = true` |
| memory | each first she has had there · what she wore on the run |
| growth | climbs |
| sink and deadline | none: the park costs no money |
| feeds | Exhibitionism, energy |
| reads | what she wears, Corruption, Exhibitionism |
| what drives it (S8) | her clothing state and her two stages · walk events rotate, seen ones weighted down |
| link into the hook | what she does in public; later, a regular may be goal 3's man from town |
| leads to | `park_watch_the_couple` · Zoe |
| day 1 | yes: walk, rest and run at stage 1 |
| BRAKE (S9) | each row once a day, on its trigger · the run's energy cost too |

**Its own place, not a walk to campus.** She can walk, rest and run there.

## The rows

| row | effect, with op | lands on a screen? |
|---|---|---|
| Walk | one event from the walk pool | yes: who she passes, what they see |
| Run | energy add −10 (guess) · Exhibitionism add +1 if Daring clothes (guess) | yes: who looks, by what she wears |
| Rest on a bench | energy add +5 (guess) | yes, short: her body, never a toast |
| the next locked act | shown with what it needs | yes, one line |

## Running is about clothes, not fitness

There is no fitness meter. What she wears changes who looks and what happens.

| level | what she runs in | how the game checks it |
|---|---|---|
| normal | leggings and a top | covered |
| Daring | a sports bra only, or no bra under a thin top | `sports_bra` worn, or no bra |
| later | shorts that show everything | a later item |

## Lewd ladder (`lewd_ladder[]`)

| rung | gate | acts |
|---|---|---|
| 1 · Good Girl · Covered | none | walk, rest, run · the wind and her skirt · a jogger turns to look |
| 1, the first explicit scene | none | she walks into the couple in the bushes, and runs |
| 2 · Curious · Daring | Corruption or Exhibitionism gte 20 | she watches the couple |
| 2, continued | Exhibitionism gte 20 | a flash for Zoe on her run (Zoe's dare) · running in the sports bra |
| 3 · Bold · Showing | Corruption gte 40 | naked or touching with Zoe, somewhere hidden |
| 4 · Hungry · Watched | locked in 0.1; the button says "Needs Hungry" | strangers see her on purpose · groping in a crowd |
| 5 · Shameless · On Display | locked in 0.1; the button says "Needs Shameless" | public sex with someone she knows or brings |

**A no always works.** Groping, when it comes, has a labelled no on the same screen, and the no holds.

**The top step has a face.** Public sex is with Ryan, Jake or Zoe, or later a park regular. In 0.1 only Zoe comes;
Ryan and Jake joining her wait for a later release (LO, 2026-10-08). A regular is a
new person: a written age, your yes and an SP5 re-sign.

## Pool (`pool[]`)

| canvas | what it is | explicit? | what drives it | brake |
|---|---|---|---|---|
| `park_walk` | who she passes on the path | no | her clothes · rotates | once a day |
| `park_run` | a run; who looks | no | her clothes | once a day, energy on the trigger |
| `park_watch_the_couple` | a couple in the bushes: she walks into them; later, she watches | yes | her stage | once a day |
| `park_hidden` | Zoe, somewhere hidden, after their run | yes | Corruption gte 40 · Zoe is there | once a day |

`park_watch_the_couple` is the early first explicit beat (LO, 2026-10-08): strangers, an accident at stage 1.

## The meters it writes and reads (`board.meters[]`)

| meter id | kind | key | fed at | read by |
|---|---|---|---|---|
| exhibitionism | sourced | `exhibitionism` | here, among others | every stage choice · leaving a room |
| followers | sourced | `followers` | her room, the park | campus talk, new messages, offers (each needs a 0.1 reader) |
| energy | a need | `energy` | her bed; a bench here | the shift, Focus, the party |

## Rows a gate needs

| row | gate |
|---|---|
| leads to the couple scene, which is explicit | leads to a person or a sex scene (blocks a ship) |
| the bench refills energy every day | a need can be met every day |
| `followers` read in 0.1 | a meter is read |
| `sports_bra` read three times | every clothing state is read three times |
| a destination with something to do alone | a destination is never open and exit-only |
| `park_hidden` explicit and repeatable | explicit in repeatable · traversal heat |

## Why — the source of each key choice

| key choice | source |
|---|---|
| a park, not the walk to campus | LO, 2026-10-08 |
| the stage table; stages 1–3 in 0.1 | LO, 2026-10-08 (SYSTEMS §14) |
| running is about clothes; no new meter | LO, 2026-10-08 (SYSTEMS §14) |
| a no always works | LO, 2026-10-08 · SP2 §3 |
| hours 07:00–22:00 | LO, 2026-10-08 (SP1) |
| energy and follower numbers | guess |
| `park_hidden` | LO, 2026-10-08 |
| Zoe in the park, weekend mornings | LO, 2026-10-08 · the hours are a guess |
| the park couple as the first explicit beat | LO, 2026-10-08 |
| the feed and the selfie live on the phone only | LO's play note, 2026-10-08 (sweep A1-34, K6) |
