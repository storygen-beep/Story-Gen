# [READY] System — park
> Signed by LO: LO, 2026-11-04.
> Changed 2026-11-04, LO's answers: the run pays Exhibitionism +1, cap 39 (F); signed by LO 2026-11-04.

> Changed 2026-11-04 to match the build; signed by LO 2026-11-04. The run pays Exhibitionism +1, cap 19, with no bra or no top.

> Changed 2026-11-03 to match the build (third alignment pass); signed by LO 2026-11-04. File and line cites removed. The selfie keeps a photo and posts nothing.

> Changed 2026-11-04 to match the build; signed by LO 2026-11-04. The 2026-10-29 locked-button note (DECISIONS 90) is corrected: "Needs Corruption 60" and "Needs Exhibitionism 60" are no longer in the game, because the buttons for scenes this release does not write were removed (DECISIONS 132). Any line below that still names one is superseded by that row.

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
| what drives it | her clothing state and her two stages · walk events rotate, seen ones weighted down |
| link into the hook | what she does in public; later, a regular may be goal 3's man from town |
| leads to | `park_watch_the_couple` · Zoe |
| day 1 | yes: walk, rest and run at stage 1 |
| BRAKE | each row once a day, on its trigger · the run's energy cost too |

**Its own place, not a walk to campus.** She can walk, rest and run there.

## The rows

| row | effect, with op | lands on a screen? |
|---|---|---|
| Walk | one event from the walk pool | yes: who she passes, what they see |
| Run | energy add −10 · Exhibitionism add +1, cap 39, with no bra or no top (LO, 2026-11-04) | yes: who looks, by what she wears |
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
| 4 · Hungry · Watched | locked in 0.1; the button says "Needs Corruption 60" | strangers see her on purpose · groping in a crowd |
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

## Changed 2026-11-02 (reader a3, `READER_FAILS_A3.md`, signed by LO 2026-11-02; DECISIONS 131)

- Row 44 + 67 (`park_run`). The run now opens on the gates ("You stretch against the park gates…") with "Run the loop. (10 energy)" and "Walk it instead."; the run text shows only after "Run the loop." The walk has its own short screen: a man on the bench watching her legs and tits. The run ends on a hook: "Zoe runs here weekends. She'd make you go further." once `zoe_met` ("Zoe's still out on the loop somewhere…" while she is in the park), otherwise "Same time tomorrow."
- Row 61 (`park_selfie`). The plain "Keep the best one." (was "Post it.") needs Exhibitionism 20 and posts nothing; no followers. Under it only "Delete them all." shows, with her thought "Put yourself up where anyone can look? Not yet."
- Row 62 (`park_walk`). In the skirt under Exhibitionism 40 she grabs the hem and holds it down; "You let it be a problem." shows from 40.
