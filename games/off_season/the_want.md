# The Want — Off Season

> The spec every release is checked against. Re-read it before each one and bump
> `want.last_read_at_release` in `v2_state.json`.
> Doctrine: `.claude/skills/author-game-v2/references/the-want.md`

---

## 1. Who she is

**Marnie Kesh, 39.** Her name is on the front of the building in eight-foot letters — KESH
AMUSEMENTS, Ellinbay seafront — and it has been her name since she was seventeen and married
into it. She had Ewan at fifteen, before the name, before any of it. The town has never once
let her forget which order those two things happened in.

Denny Kesh has been inside four years. What he did, he did in the arcade's back room with the
arcade's money, and the arcade is what was left standing when they took him. She lives in the
flat over it. Two rings on the hob, an immersion that costs three pounds to run, and a window
that looks at a sea nobody comes to see between October and April.

She is the only person in this town who is somebody's mother, somebody's sister, somebody's
aunt and somebody's landlord all inside four hundred yards.

**What she has to lose:** the version of her that everyone here agreed on years ago — the one
who held it together, who is *coping*, who is fine. It is the only thing she owns outright and
every hour she spends being wanted instead of relied on spends some of it.

## 2. The appetite that never fills

**To be wanted — not needed, not thanked, not worried about — by the people she raised or
reared.**

It cannot complete. There is no amount of being wanted that settles it, no villain, no door at
the end. The direction is what matters: at the start she goes to them, and every rung is one of
them coming to her instead. That inverts forever and never resolves, because each of them can
come one notch further in.

**What does release 41 add?** Another door on the front. Another relative back for the winter
because the season went badly somewhere else. Another hour of the day that belongs to her.
A dead seaside town in February is a machine for producing people with nowhere to be.

## 3. What she is becoming — as ACCESS

**Bottom.** She goes to them. She turns up at the yard with a flask because Ewan will not stop
for lunch. She climbs the stairs over the chip shop and knocks and waits. She keeps her coat on
in her own flat because the meter is at three pounds and she is saving it for when someone
visits. Everything she does in this town, she does on her way somewhere else.

**Top.** They come to her. The arcade after close is where they end up, and the flat above it
is where they stay. She does not knock at the terrace house any more and Roan does not lock the
back door. The meter runs. Whatever she is doing when they arrive is what they walk into, and
she stops covering it up.

**The ascent is per-person, not global — and that is a declared fork, not an oversight.**
`the-meters.md` W1: the field splits cleanly into ladder games (the player climbs) and roster
games (the cast does), with nothing in between, and family games sit on the roster side. This
game declares `who_climbs = "cast"`. There is no corruption bar. **The four ladders are the
four people**, and each one is a different kind of going-further so that a player who does not
want one can still climb another:

| person | the meter | what going further MEANS with him |
|---|---|---|
| **Ewan** | `hold` | how much of her he is allowed to decide — priced, never courted |
| **Tam** | `ease` + `want` | how long he can be in a room with her without a reason |
| **Roan** | `bond` | how much of who she was before is allowed back |
| **Nessa** | `trust` → `want` | how much of the flat above the arcade is hers to walk into |

**Anti-pattern this avoids, measured:** a dominant meter rising toward failure while the world
contracts to a sealed room. Every rung here opens a place, an hour, or a door that was shut.

## 4. The charge

**Taboo and Reversal, deliberately combined, and the reversal is the load-bearing half.**

The taboo is what they are to her. The reversal is the direction of care: she is the one who
fed them, drove them, sat up with them, took the phone call about their father — and the whole
game is that machine running backwards. Someone with power over them loses it. Someone who had
none takes more than he should.

Ewan holds the lease and the books. Tam is nineteen and has nothing and is the only one who
still turns up for no reason. Roan came home broke to their mother's house and is the only
person alive who remembers her before the letters went up over the door. Nessa pays her rent in
cash on a Friday and has started leaving the back-room door open.

"It's hot" is not a charge. This one is: **everyone in this game owes her, and every rung is
one of them stopping paying it back and starting to collect instead.**

## 5. Why *this* person

- **Ewan, 24** — she had him at fifteen and they raised each other. He took the books off her
  the month after Denny went in, and he was right to, and she has not been allowed a decision
  about her own building since. Being wanted by him means being *un*-managed, which is the one
  thing she cannot ask for.
- **Tam, 19** — the one who never left and never grew out of her. He comes up the stairs for
  nothing, sits where he always sat, eats what is in the pan. He is the only person in Ellinbay
  who treats her as company rather than as a situation. He has no idea that is what he is doing
  and she has started to.
- **Roan, 36** — her brother, five years behind her, back in their mother's terrace after
  whatever it was in Bristol collapsed. He was twelve when she got pregnant and he watched the
  whole town decide who she was in about a fortnight. He is the only witness. Being wanted by
  him is being told the verdict was wrong.
- **Nessa, 21** — her sister's girl, came for a summer job and did not go back. Sleeps in the
  arcade's back room and pays forty a week for it. Marnie was exactly her age with two kids, and
  Nessa is what she would have been. She cannot stop watching her, and Nessa has noticed.

## 6. Register

- **`narration_person = "second"`.** Per-game and immutable once 0.1 ships. Second person is the
  genre standard — 13 of 17 measured games — and the exemplar for a female protagonist.

- **Crude-vocabulary ceiling, written as the words themselves, per person.** A ceiling described
  abstractly gets written around.

  | person | permitted at 0.1 | opens later |
  |---|---|---|
  | **Tam** | cock, cunt, tits, wet, hard, suck, fuck | cum, come in / on, arse |
  | **Ewan** | cock, tits, hard, fuck, hold still | cunt, cum, arse, choke |
  | **Roan** | cock, tits, cunt, wet, fuck, want | cum, come inside |
  | **Nessa** | cunt, tits, wet, tongue, lick, fingers, come | fuck, hold her down |

  **Crude is the default at the sexual register, not a mode.** No euphemism, no "between her
  legs", no fade. The ceiling is a ceiling and never a floor — writing under it is the defect.

- **Where the crude register lives: the repeatable surfaces, named.** This is the correction the
  whole system exists for — the measured failure sealed 95% of its explicit prose in a room the
  player could never re-enter while every one of its nine repeatable loops scored zero.

  The crudest writing in this game is in the **act loops** on the four hubs, and above all in
  **Tam's pose ladder over the chip shop** — the surface a player will re-enter more than any
  other. Not in the milestones. Not in the one-shots.

---

## The test before leaving this file

1. **What does release 41 add?** A door on the front, a relative back for the winter, an hour of
   the day. The town supplies them indefinitely and nothing in the premise runs out.
2. **What can she reach at the top that she cannot at the bottom?** At the bottom every room in
   Ellinbay except her own flat belongs to somebody else and she visits it. At the top the
   arcade after close, the yard loft, the back room and the terrace house are all places she
   walks into without knocking, and the flat over the arcade is where people end up.
3. **Which character would a player miss?** Tam. He is the only one who comes to her before the
   game gives him a reason to, which is the appetite in a single person, and he is the spine of
   0.1.
4. **Which repeatable surface carries the crudest writing?** Tam's act loop in the flat over the
   chip shop.
