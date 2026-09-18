# THE RINGS — guarding the bunker in layers

**Vesper 0.2.2 addendum · rev 226 · beat_0191 · built 2026-09-18**

---

## Why

LO, playing the shipped 0.2.2: *"when wren gets to bastien there is no gaurds inside."* Then, after a first
answer that read him too narrowly: *"It is about guards guarding him at the different level as security for
hideout."*

He was right about something bigger than an empty plant room. Measured against the built game:

- The bunker held five men and **not one of them was guarding anything**. A flask on a break, a man washing
  his arms, a canteen table, a workbench, a desk — and all five in **wrong-turn** rooms.
- The correct path cost **10 Charge and 15 minutes a turn and nothing else**.
- So every mechanic 0.2.2 built — the one quiet exit, `fighting`, the emitter and its 10-coin-and-a-day
  reload — was reachable **only by getting a door wrong**. A player who remembered Renner's five clauses
  touched none of it, and walked into the plant room through an unguarded door.

The design book had already named the budget — *"four survivable mistakes per run"* — and the correct path
never drew on it once.

## What ships

Posted men at three depths. Renner's route gets her through the **geography**; these are what stop her.

| ring | where | who | how it is beaten |
|---|---|---|---|
| 1 | the slab, above ground (`bunker_descent.base`) | two men walking a round, 20:00–23:59 | pick the hour, or lie up four hours and let it finish |
| 2 | the far gate, between `t3` and `t4` | one man on a stool, the wedge is his | quiet (stealth 45) or fight (50) |
| 3 | his level, between `t5` and the room | a walker, a door man, a clerk | 55/60 · 60-if-silent/70/emitter · 35/40 |

`t5` stopped being a door and became **the scout**: she looks through the wired glass that has been in that
node doing nothing since beat_0172, and counts three.

### Three things it buys for free

- **The five loafers are now the off-shift of these men.** Nothing already written is contradicted — it is
  simply what they were always doing.
- **The hook stays a hook.** Bastien's own line is that the room is baited and cast. Bait has to look
  reachable, so the outer rings are thin on purpose and the weight is on his level, where a rescuer has
  already committed.
- **The budget became a decision.** `bunker_stealth_used` is no longer "the one free back-out"; it is **the
  one quiet thing per run**, and the correct path now draws on it. Slip out of g2 and the far gate has to be
  paid for in noise. Slip past the far gate and the door man has to be paid for in a shot.

### Two new pieces of state

- **`bunker_noise`** — per-run, zeroed on the way in beside `bunker_stealth_used`, +1 for every body left on
  the correct path. Read by exactly one gate: the door man is dozing at `lt 1`. It deliberately **survives**
  a caught room's restart, because the run continues and the floor is hot behind her.
- **`bunker_seen`** (flag) — persists across runs, set the first time she leaves a body on the correct path.
  Read only by the slab: after it, waiting out the round stops working.

So a loud run costs her twice — once below, in the man who is now sitting up, and once above, on every
night after.

### Why a ring lets her walk on when a wrong room does not

A wrong room is the crew's own space and their mates are next door, so the alarm goes up and the fight and
the shot buy the **room**, not the run. A posted man is alone at his post and nobody expects to hear from
him for an hour. She clears him and continues, and the cost is carried forward instead.

## Decisions, and what they cost

**The door man is emitter-or-grind, and that is deliberate.** Three ways past him, but the clean one needs a
silent run *and* an unspent budget, so in practice the answer is the emitter (10 coin and a day at the feed
line) or `fighting 70`. That ties the release's weapon to the release's capstone through an economy that
already existed. It does gate the rescue behind that economy. **Flagged to LO; his to flip.**

**The round runs 20:00–23:59.** Night, so she has to go early or late rather than at the obvious hour. A
daylight watch would push every run into the dark and delete the choice. **Flagged to LO; his to flip.**

**The wait is 240 minutes, not 120, and the number is forced.** The round is four hours. A two-hour wait
started at 21:00 ends at 23:00, still inside it — the player would pay ten Charge to read the same
paragraph again. Four hours from anywhere inside a four-hour window always lands outside it.

**Nothing inside the plant room.** `bunker_bastien` is once-only Tier-3 and its spine is his voice: the
washing one comes Tuesdays, the wrong boots, a hundred and nineteen. A fight in there spends the capstone on
the wrong thing, and she is about to take the whole weight of a man who cannot walk. She opens that door to
him alone, because she cleared the way.

**Nothing at the extraction.** LO's standing call: the company finds out after they are gone. Guards there
would spring the trap and end the release in a firefight instead of on the dread that it **worked**.

**Thresholds sit on the shipped ladder** (g1–g5 = 20/25 … 60/65). Ring 2 at 45/50 and the corridor man at
55/60 are posted men, so above the loafer at the same depth. The door man at 60/70 is the only man in the
building who outranks Loder. The clerk at 35/40 is **not** a slip — he is a man with a book and his back
turned, and a wall there, after the emitter has already been spent on the door, would be a cruel one.

## Prose truth the build forced

Two lines became false the moment the rings existed, and both were fixed in place:

1. `bunker_bastien.base` said he had been awake *"the whole time she has been standing in the doorway."* She
   is no longer standing in a doorway; she has just dealt with a man three feet inside it.
2. `cap_the_extraction` had Cain walking in without a foot wrong. He may now be stepping over men she left.
   One band, gated on `bunker_noise gte 1`, because on a silent run there is nothing to step over and the
   line would be the lie instead.

## Media

**One new pool**: `sex/bunker_door_t5`, pool = 4 — the door man taken with the emitter. The far gate has no
emitter branch precisely to hold it at one. Media debt for 0.2.2 goes **7 slots to 8**.

## Measured

| | before | after |
|---|---|---|
| explicit floor (floor 7.5%) | 9.4% | **10.2%** |
| explicit in repeatable (floor 50%) | 58.4% | **61.0%** |
| authored nodes reachable | 465/465 | **474/474** |
| judged gates passing | 21/40 | 21/40 |

Per-beat, against `gates.py`'s frozen list: the four act beats of `door_taken` score 3, 5, 4, 4 at 37–43
words. The fifth beat scores 0 and is the reflective beat, which is correct doctrine — interiority gets its
own beat, after.

## Guards

- `games/vesper/tests/check_bunker_route.py` **§11** — shape: the ring cannot be walked round, cannot trap a
  run, the door man cannot be passed for free, every quiet answer is budgeted **and spent**, noise is zeroed
  on the way in and paid on the way past, and the two clock windows tile the day to the minute.
  Negative-tested eight ways; all eight caught. §1 taught the ring at t3, §3 the sixth pool, §10 the canvas.
- `games/vesper/tests/live_rings.py` **(new)** — behaviour, in the built game, driven through the real
  engine. Three of the rings' rules cannot be read statically: the slab's clock band, the four-hour wait
  arithmetic, and the door man's `bunker_noise` gate. 36 checks.

## Not done

The media harvest. `sex/bunker_door_t5` joins the seven slots 0.2.2 already owes.
