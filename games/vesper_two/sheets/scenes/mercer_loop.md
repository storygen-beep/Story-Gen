# SCENE · Mercer — the repeatable surface  `[READY]`

`loop_mercer` · `penthouse` 08:00–23:00 **and** `mercer_room` 23:00–08:00 · gate `mercer_open` ·
**is_repeatable**

⚠️ **BRAKE ON THE WAY IN** (S9): `trigger.max_triggers_per_day = 2` and
`trigger.costs = { charge = 10 }`, on the **trigger**.

---

## The bands are WHAT THE USE VIOLATES — not a ladder

This is the mechanism that separates him from every other character in the game. Renner's loop bands
on **arousal**, because he is climbing. Mercer is not climbing. **He is at his ceiling from beat
one**, so there is nothing for a rung to measure.

What changes is **who else is in the room and whether the door is open**, and the `[group]` chain
rides that instead:

| band | condition | beat | measured |
|---|---|---|---|
| routine | alone at the penthouse | He puts you over the desk without looking up. He works his cock into your cunt. He fucks you slowly with one hand flat between your shoulders. | `[MEASURED]` 27 words · **3 explicit** · median sentence 9 |
| seen | somebody waiting | A man sits by the window waiting on his meeting. Mercer bends you over the desk anyway. He puts his cock in your cunt and lets the man watch your tits move. | `[MEASURED]` 32 words · **3 explicit** · median sentence 10 |
| priced | at the stall, shutter half up | He does it against the crates with the shutter half up. Two men outside wait and one prices you out loud. His cock is still in your cunt when he answers them. Your tits are out in the cold. | `[MEASURED]` 39 words · **3 explicit** · median sentence 11 |

**Three bands, three frozen words each, and the act is identical in all three.** The escalation is
entirely in the audience. That is *"his use-scenes differentiate by what each violates, never by
pose"* built rather than asserted.

⚠️ **The `priced` band fires at `mercer_room`**, which is why this canvas is declared at both
locations. `check_people.py` confirms his grid covers 23:00–08:00 there.

## The act menu

**2 options**, the field median.

## Media

`mercer_lockup_*_t5` (7) · `mercer_print_*_t5` (6) · `mercer_serve_*_t5` (3) ·
`mercer_finish_*_t5` (3) — **16 pools, the deepest set in the game, all on disk.**

⚠️ **ONE ASSET, ONE BLOCK.** With sixteen pools and three bands the temptation to reuse one across
two blocks is highest here — review dedupes by file, and one verdict would silently cover two beats.
