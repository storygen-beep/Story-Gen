# [REVIEW] System — parties

> A draft for LO to place. Written 2026-10-08 from SYSTEMS §4, SP4, the party scout card and the ledger's `parties` card.
> Every number marked "guess" is new here and waits for your yes.

| row | answer |
|---|---|
| id · name | `parties` · Parties (Friday at Zoe's) |
| place and hours | `zoe_apartment` · Friday 19:00 to Saturday 02:00 · riskier choices after 23:00 |
| cost | the Friday evening · arriving: energy add −15 (guess) · drinks and food free |
| one ladder or two | one |
| people | Zoe, always · Jake, from Jake B 1 until midnight · classmates by chance |
| pool | `party_chat`, `party_drink_offer`, `party_dare` · `daily = false` (weekly) |
| memory | tonight: drinks, the boost, who she turned down · kept: she went, a heavy night |
| growth | climbs |
| sink and deadline | none: no money at a party |
| feeds | `campus_talk`, Corruption, Exhibitionism, `laura_suspicion` |
| reads | energy, the curfew, what she wears |
| what drives it (S8) | her stage picks the dares · a drink lifts choices one stage · guests rotate |
| link into the hook | what she brings home late: Laura on the stairs, Ryan at 3 a.m. |
| leads to | Zoe, Jake, Laura, Ryan |
| day 1 | no: it starts on the first Friday |
| BRAKE (S9) | Friday only · arriving costs energy · `party_went` is read by hours since set |

## Getting in

| check | what she is told | the way out |
|---|---|---|
| the curfew | *"Laura said no. Not this Friday."* | wait out the week, or lift the grade |
| under 20 energy (guess) | *"You're asleep on your feet."* | sleep; the party runs to 02:00 |
| something short to wear | Zoe: *"Not in that. Borrow mine."* | Zoe's dress, in her bedroom |

## Inside a party

| row | effect, with op | lands on a screen? |
|---|---|---|
| arriving | `party_went` set true · `drinks_tonight` set 0 | yes: who is here tonight |
| take a drink | `drinks_tonight` add +1 · `drinks_boost` on for 3 hours | yes, one line |
| the third drink | `heavy_night` set true | yes |
| take a dare | Exhibitionism add +1 · `campus_talk` add +1 | yes, always: her body |
| refuse a dare | `party_cool_<npc>` set true · costs nothing else | yes: one more push, and her no holds |
| refuse a drink | nothing moves; the no always works | yes, one line |
| leave | to the street; the way home after 22:00 sets `came_home_late` | yes |

**The next morning.** After a heavy night, her Saturday bed scene takes energy add −30 and sets
`heavy_night` false.

## Pool (`pool[]`)

| canvas | what it is | explicit? | what drives it | brake |
|---|---|---|---|---|
| `party_chat` | who is here and what they say | no | who came tonight · rotates | once an hour (guess) |
| `party_drink_offer` | someone hands her a drink | no | `drinks_tonight` under 3 | three a night (guess) |
| `party_dare` | Zoe's dare, people watching | yes at Curious: the bra off | her stage · the boost | two a night (guess) |
| `party_hookup` | a hookup with someone she knows | yes | Corruption gte 40 | once a night |

## Lewd ladder (`lewd_ladder[]`)

| rung | gate | acts |
|---|---|---|
| 1 · Good Girl · Covered | none | Zoe's dress, borrowed · a dare she can refuse: "Not tonight, Zo" |
| 2 · Curious · Daring | Corruption and Exhibitionism gte 20 | a dare kiss, Jake or Zoe · bra off through the sleeve (Zoe A 2) |
| 3 · Bold · Showing | Corruption gte 40 | topless with Zoe alone, friends gone in (Zoe A 3) · a hookup |
| 4 · Hungry · Watched | later; the button says "Needs Hungry" | Zoe's bedroom, door open (Zoe A 5) · strangers watching |

**The drinks boost** opens one choice a stage early. Steps ignore it: every step's gate says the boost
is off.

## The meters it writes and reads (`board.meters[]`)

| meter id | kind | key | fed at | read by |
|---|---|---|---|---|
| drinks_tonight | sourced | `drinks_tonight` | `zoe_apartment` | the heavy night, at 3 |
| campus_talk | sourced | `campus_talk` | `canteen` (and here) | who approaches her · feed posts |
| exhibitionism · corruption | sourced | her two meters | here, among others | every stage choice |
| laura_suspicion | sourced | `laura_suspicion` | `home_hall` | home late: add +5 at Laura's catch; read by her catch and the curfew |

## Rows a gate needs

| row | gate |
|---|---|
| no party under 20 energy | a need shuts a door |
| refusing a dare and a drink | she can say no |
| leads to Zoe and Jake | leads to a person |
| the third drink sets `heavy_night`; a scene clears it | a flag that never resets (a lint) |
| `party_hookup` explicit and repeatable | explicit in repeatable · traversal heat |

## Why — the source of each key choice

| key choice | source |
|---|---|
| Friday at Zoe's, to 02:00 | LO, 2026-10-06/07 (SYSTEMS §4, SP1) |
| riskier choices after 23:00 | LO, 2026-10-07 (SYSTEMS §4) |
| dares: one push, her no holds | LO, 2026-10-07 · scout card, dares row |
| drinks: the no always works | LO, 2026-10-07 · scout card, drinks row |
| the boost: 3 hours, one stage, choices only | LO, 2026-10-07 (SP4) |
| heavy night: 3 drinks, 30 energy | LO, 2026-10-07 (SP4) |
| free drinks and food | LO, 2026-10-07 · scout card, amounts row |
| arriving costs 15 energy; the caps per night | guess |
| `party_hookup` | LO, 2026-10-08 |
| Zoe A 3: her friends leave the hot tub first | LO, 2026-10-08 |
