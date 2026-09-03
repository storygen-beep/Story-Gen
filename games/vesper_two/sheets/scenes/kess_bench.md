# SCENE · Kess — the bench  `[READY]`

`bench_kess` · `kess_berth` · 10:00–22:00 · gate `kess_open` · **is_repeatable** · **no sex, ever**

⚠️ **BRAKE ON THE WAY IN** (S9): `trigger.costs = { coin = 10 }` and
`trigger.max_triggers_per_day = 1`, on the **trigger**. One unbraked door makes the whole rung
farmable no matter how well priced the others are.

---

## The three bands — `[group]` on `seated`

⚠️ **This is the surface the whole pass was written to test.** It is **repeatable**, so its beats
land in the `explicit floor` denominator (`gates.py:4927` — the denominator is REPEATABLE beats,
changed 2026-08-31). A sex-free repeatable surface drags that ratio directly, and the honest options
were to accept the cost or to write him a sex scene his ceiling forbids.

**Neither was necessary. Anatomy alone clears the floor.**

| band | beat | measured |
|---|---|---|
| `seated 1-2` | You undress and get on the bench naked. He opens the seam and works. The cold gets at your tits. | `[MEASURED]` 20 words · **3 explicit** · median sentence 6 |
| `seated 3-4` | You lie back naked and he goes in past the wrist. Your cunt is bare under the lamp. He is not looking at it, and your tits move when he pushes. | `[MEASURED]` 31 words · **3 explicit** · median sentence 11 |
| `seated 5` | He has four things in you now. A clamp holds the seam open. His hand is inside to the forearm. You lie naked with your tits tight and your cunt clenching on nothing each time he seats one. | `[MEASURED]` 38 words · **3 explicit** · median sentence 7 |

**Three bands, three frozen words each, zero sexual acts.** `naked` · `undress` · `tits` · `cunt`
are anatomy, and the list does not care whether anybody is enjoying anything.

⚠️ **Count the BAND, not the node.** A player sees exactly one of these. One game's finisher scored
6 folded together while every band it could actually render put **two** words on the screen.

## What the bands are FOR

Not escalation of pleasure — **escalation of access**. Band 1 is two fingers, band 3 is a forearm
and a clamp, and the difference the player feels is how much of her is open and how routine it has
become. `seated` is read in seven places elsewhere; this is the one place it is written.

## Exits

| label | effect | screen |
|---|---|---|
| "Let him seat another." | `seated` `add` `+1` (cap 5) · → `post_kess` | yes |
| "Just the night, then." | `charge` `set` `100` · `clean` `set` `100` · → `post_kess` | yes |
| "Stop." | → `stop_kess` | yes |

⚠️ **A spent day still has a door** (gate 31): the second row carries no `conditions` beyond the
trigger's, so the screen can never render empty.

## Media

`videos/portraits/wren_naked.jpg` · `wren_topless.jpg` · `wren_underwear.jpg` — **8 states on
disk**, and this surface is the reason the state-reactive portrait is worth wiring at all.
