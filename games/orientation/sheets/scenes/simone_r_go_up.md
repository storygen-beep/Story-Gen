# SCENE · `the_pledge_house` · *Go up*  `[READY]`   **REPEATABLE ACT SURFACE**

The anchor's act surface, and **the crudest writing in the game** (Want §7). Re-entered, not seen
once — which is the correction this whole system exists for.

| | |
|---|---|
| **canvas** | `act_pledge_upstairs` · `is_repeatable = true` |
| **opened by** | `simone_open` — set by `simone_06`, the last step of her arc |
| **window** | Thu/Fri/Sat 21:00–02:00 (Simone rows 2+3) |
| **advance** | **node routing**, not a cascade — the picture has to change with the act |

⚠️ **Node routing, deliberately.** A cascade appends below what is on screen and suits a one-time
scene whose text builds; node routing swaps the passage and suits a repeatable act surface. The
content kind picks the mechanism.

---

## BRAKE — on the way IN

```
trigger.costs                rest 15
day-cap flag                 went_up_today    ← SET ON THE CHOICE, cleared in [engine.daily_tick]
schedule window              Thu/Fri/Sat 21:00-02:00
```

⚠️ **The flag is set on the CHOICE, not the node exit.** This window crosses midnight, which is
exactly the trap: `advanceTime` rolls the day inside itself (`v2.py:5411-5414`) and the tick clears
`_today` flags there (`v2.py:5552`), so an exit-set cap would start the new day already capped.

⚠️ **One unbraked door makes the whole rung farmable** no matter how well priced the others are.

---

## The branch map

```
act_pledge_upstairs.base   ── "Go up with her."          ──►  .stairs      [explicit]
                           ── "Stay where you are."      ──►  (room screen, no penalty)

.stairs                    ── "Let her put you on the bed." ─►  .bed       [explicit]
                           ── "Stop."                    ──►  .stop        A11
.bed                       ── "Stay when the door opens."──►  .three       [explicit]
                           ── "Enough."                  ──►  .stop        A11
.three                     ──────────────────────────────►  .after        A10
```

**Two exits per screen, all the way down.** Field median for an act menu is **2 options, span 1** —
the same narrowness applied down the page instead of across the menu.

---

## The beats, written out, with their measurement lines

> ⚠️ **A number on a sheet is a PROMISE until an instrument produces it.** These four were run
> through `gates.py --beat`, which uses the same thresholds the build does. **`hard` and `wet` are
> not on the word list** — it is anatomy and acts.

### `.stairs` — [explicit]
> She has your top off at the top of the stairs. Her mouth goes to your tits and she sucks hard
> enough to mark you. Two fingers push into your cunt while she is still standing. You moan into
> her shoulder and she does not slow down.

`47 words · explicit 4 (registers) · median sentence 11 · rungs: hands, oral · body by sentence 0 2 1 1`

### `.bed` — [explicit]
> She puts you on the bed and shoves your skirt up. Her tongue works your clit in flat slow
> strokes. She licks you until your thighs shake and holds them open when you try to close them.
> You come with her mouth still on your cunt.

`46 words · explicit 3 (registers) · median sentence 11 · rungs: oral · body by sentence 0 1 1 1`

### `.three` — [explicit]
> You are on your knees on the carpet. She has your hair in her fist and his cock in your mouth.
> She works two fingers into your cunt while you suck him. Your jaw aches. She pushes your head
> down until his cock is in your throat.

`50 words · explicit 4 (registers) · median sentence 11 · rungs: hands, oral · body by sentence 0 1 2 0 1`

⚠️ **This beat's last sentence was rewritten.** The first draft ended *"and she pushes your head down
anyway"* and `--beat` flagged it: **the last sentence carried no body word.** The pivot rule is a
reading test and no regex decides what a sentence is *about*, but the body-words-by-sentence shape
catches the drift off the body that precedes a pivot. Read the beat's last sentence: if it is about
what the moment MEANS rather than what is HAPPENING, it has pivoted and will score 0–1.

### `.after` — **A10 aftermath, deliberately NOT explicit**
> She finds your top and hands it over. She is already talking to somebody in the doorway. You are
> still on the carpet with your skirt around your waist. Come Thursday, she says.

`33 words · explicit 0 · median sentence 9`

⚠️ **Scoring 0 here is correct, not a miss.** The aftermath is *after* the act and it is the one
place in a sex surface where interiority is the point rather than the pivot defect. **23 of 23
finish nodes across six v2 games have an empty `exit_block`** — the act completes and the canvas
stops. This one does not: three moves in thirty-three words — she is already gone, she notices being
left, and the loop asks whether she is coming back.

**Exit block on `.after`:** *"Go back down."* · *"Stay a minute."*

---

## Variation on re-entry

**`block_pool` on `.stairs` and `.bed`** — 4 blocks each, undirected variety. **Stacked `group` bands
on `nerve`** for directed variety: at 30 she is being taken up, at 70 she is the one on the stairs
first.

⚠️ **`block_pool` runs 46 times in `the_long_summer` and ZERO times in every v2 game.** v1 had a
numbered rule for it; v2 lost it in the divorce from the old corpus. A repeatable surface written as
one paragraph is dead by the third visit.

⚠️ **Separate the `nerve` bands from any other `[group]` on these nodes with a non-`group` block**
(`v2.py:14637`).

## Media

`sex/pledge_upstairs_t5` · **pool 6** — never a single `file`. Each explicit node carries **its own**
clip, on the beat the player is reading.

## Ceiling
Simone tier 3 — *full: cunt, cum, slut, and the words she uses about Josie to men.* A ceiling, never
a floor.
