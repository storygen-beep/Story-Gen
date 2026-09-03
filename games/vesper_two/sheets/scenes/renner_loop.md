# SCENE · Renner — the repeatable surface  `[READY]`

`loop_renner_depot` · `renner_depot` · 09:00–18:00 · gate `renner_open` · **is_repeatable**

**The reward for finishing the arc, not the starting position.** Node-routed (not a cascade),
because the picture has to change with the act.

⚠️ **BRAKE ON THE WAY IN** (S9): `trigger.costs = { charge = 15 }` and
`trigger.max_triggers_per_day = 2`, on the **trigger**, not on a choice inside. *"One unbraked door
makes the whole rung farmable, no matter how well priced the other doors are."* Three rounds of
adding costs to inner choices moved nothing; moving the same costs to the triggers fixed five
meters at once.

---

## 1 · The opener — the REASON AXIS

The same act reached two ways is written two ways, and the difference is **why she is doing it**,
not how hot it is. **Neither is hotter.**

| route | flag | opener |
|---|---|---|
| she came for it | `renner_entry_chose` | She walks the aisle to where he is working and waits until he looks up. |
| the walk-in put her here | `renner_entry_caught` | She is still bent over the crate he backed her into and he has not moved. |

Built as a `group` chain on the entry flag. ⚠️ Adjacent `group` blocks merge into ONE if/elseif
chain and first match wins (`v2.py:14561-14568`), so the two arms are mutually exclusive.

⚠️ **This is NOT R6's banned move.** R6 forbids rewriting a *hub's* first sentence per stat band.
This varies the **act's** intro by which route opened it; the hub opener stays constant.

## 2 · The act nodes — the TWO-HALVES SENTENCE

**One sentence, two people's meters.** His arousal writes the first clause, hers the second. Nine
outcomes from six written clauses, and nothing random — read it twice at the same arousal and it is
the same sentence.

**HIS half** — nested `group` on `npc_renner.arousal`:

| band | clause | frozen |
|---|---|---|
| low | He works his cock into your cunt slow, like his mind is elsewhere. | `cock` `cunt` |
| mid | He fucks your cunt hard enough to move the shelving. | `fucks` `cunt` |
| high | He rams his cock into your cunt like he wants through you. | `cock` `cunt` |

**HER half** — nested `group` on `arousal`:

| band | clause | frozen |
|---|---|---|
| low | You brace on the shelf and let his cock do the work. | `cock` |
| mid | You push back into it until his balls hit you. | `balls` |
| high | You push back onto him, chasing your own orgasm. | `orgasm` |

⚠️ **EVERY COMBINATION SCORES 3+, BY CONSTRUCTION.** Each HIS clause carries two frozen words and
each HERS carries one. That is the point of counting **the BAND, not the node** — a player sees
exactly one band, and one game's finisher scored 6 folded together while every band it could render
put **two** words on the screen.

**The three same-band combinations, each re-measured as the player would see it:**

| band | the rendered pair | measured |
|---|---|---|
| low | He works his cock into your cunt slow, like his mind is elsewhere. You brace on the shelf and let his cock do the work. | `[MEASURED]` 25 words · **3 explicit** · median sentence 13 |
| mid | He fucks your cunt hard enough to move the shelving. You push back into it until his balls hit you. | `[MEASURED]` 20 words · **3 explicit** · median sentence 10 |
| high | He rams his cock into your cunt like he wants through you. You push back onto him, chasing your own orgasm. | `[MEASURED]` 21 words · **3 explicit** · median sentence 12 |

⚠️ **Three of nine are sampled, not all nine.** The construction guarantees the other six — two
frozen words in every HIS clause plus one in every HERS — but a guarantee is an argument, and only
these three have been through the instrument.

## 3 · The finish nodes — banded, and each band scores on its own

| finish | beat | measured |
|---|---|---|
| inside | He shoves his cock in to the root and holds. You feel him jerk and his cum go into you in pulses. He stays inside until he softens and your cunt is full of it. | `[MEASURED]` 35 words · **3 explicit** · median sentence 12 |
| on her | He pulls out and finishes on your ass in three thick ropes. He wipes his cock clean on your hip. His cum sits there and starts to run. | `[MEASURED]` 28 words · **3 explicit** · median sentence 8 |

⚠️ The `on her` beat scored **2** on its first draft and was rewritten, not excused. *"When prose
scores low, the prose is what is wrong."*

## 4 · The act menu

**2 options**, which is the field median (span 1). Not a wall — `the-surfaces.md` R3b.

## Media

`renner_loop_t5` · `renner_loop_oral_t5` · `renner_loop_vaginal_t5` · `renner_loop_doggy_t5` ·
`renner_finish_inside_t5` · `renner_finish_facial_t5` · `renner_finish_anal_t5` — **7 pools on
disk**, all `pool_dir` + `pool`, cycling via `$game_state.media_cycle`.

⚠️ **ONE ASSET, ONE BLOCK.** Never reuse a `pool_dir` across two blocks in this canvas — review
dedupes by file and one verdict would silently cover two beats.
