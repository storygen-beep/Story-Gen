# 0.0.1 — the longer read

## The number that used to fail — closed, and the gate changed too

**12.0% of repeatable beats carry explicit content. The floor is 7.5%. It passes, and not
marginally** — `gates.py` flags anything under 12.0% as a BARE PASS, and this lands exactly on the
line rather than under it.

Six explicit beats, every one verified by running `gates.py`'s own regex rather than trusting a
label.

### Where they went

| scene | rung | the beat | counted words |
|---|---|---|---|
| [`del_12`](../../sheets/scenes/del_12_reach_for_the_top_shelf.md) | corruption 12 | what the reaching does to her shirt, and to him | ass · tits · nipples |
| [`del_30`](../../sheets/scenes/del_30_behind_you_at_the_monitor.md) beat 4 | corruption 30 | first contact, and he is not hard yet | cock · ass · tits |
| [`del_30`](../../sheets/scenes/del_30_behind_you_at_the_monitor.md) beat 5 | corruption 30 | what her body does back | cunt · ass · cock |
| [`marek_20`](../../sheets/scenes/marek_20_dont_cover_up.md) beat 2 | corruption 20 | she does not reach for the towel | naked · tits · cunt |
| [`marek_20`](../../sheets/scenes/marek_20_dont_cover_up.md) beat 3 | corruption 20 | he looks, and does not hurry it | tits · nipples · cock |
| [`marek_20`](../../sheets/scenes/marek_20_dont_cover_up.md) beat 4 | corruption 20 | she turns round | tits · cunt · cock |

**Three were added on your call. Three already existed and had to be rewritten**, because they were
labelled explicit and scored 0, 0 and 1. `hard` and `wet` are not on the gate's word list — it is
anatomy and acts, not states.

**All six are on repeatable surfaces**, which is where doctrine says heat has to live, and it is the
exact failure the field study found in our own back catalogue.

**All six are written out in full on their sheets.** A label cannot carry a pivot test — *does the
last sentence say what is happening, or what it means?* is a reading test, and nothing but the prose
answers it.

### What the rewrites were actually fixing

Two of the three old beats were not just miscounted, they were **coy**:

- `del_30` beat 4 said *"you feel him through his trousers, half hard against you."* What she feels,
  not what is touching her where. It now names his cock, her ass and her tits.
- `marek_20` beat 3 named her tits once and then went to *"what looking at you has done to him"* —
  a phrase that gestures at his cock instead of saying it. That is the flinch the register doctrine
  is written against, and it sat in the release's voice sample for the whole session.

**The gate's word list caught a craft failure, not just an arithmetic one.**

### And the gate itself changed

**`explicit floor` now divides by repeatable beats, not by every beat.** Applied to the skill on your
call, 2026-08-31.

The old denominator meant any legitimately cold block dragged the score down — and this game's
twelve-screen opening moved it from 12.0% to 8.0% **on identical prose**. That is a live incentive to
shorten an opening to move a number, which is the worst available response.

**Verified by running the script before and after on all fifteen built games:** thirteen verdicts
unchanged; `steam` 7.6% → 7.2% and `the_allowance` 8.1% → 7.3% flip PASS → FAIL, both already flagged
BARE PASS. `vesper` does not flip — it failed before and fails harder now.

⚠️ **The floor constant was not re-baselined on the new denominator**, so it is lenient rather than
strict. Recorded in the gate's comment block and in `CHANGELOG.md`.

⚠️ **A new diagnostic falls out of it, free.** The headline now prints both figures, and the
direction of the gap reads the game: repeatable share *above* all-beats means the cold content is in
one-shots where it belongs; *below* means the heat is in one-shots and the loops are cold. Measured:
`steam` −0.4, `the_allowance` −0.8, `forty_miles` −0.2, `vesper` −0.6. Every other game positive.

## The size problem, stated plainly

**~3,540 words. A seed is 116,540.**

Three independent sources say this architecture has a floor below which nothing works: DoL's own
first release, Ashwell's *"requires substantial content; collapses into linearity otherwise"*, and
Failbetter's time-to-bootstrap.

**This is not that, and must not be called a release.** It is a slice built to test whether the
review loop works — whether you can read a design, change it, and get what you approved. That is the
experiment. The game is the vessel.

## What the sheets caught before anything was built

Ten things, and not one of them would have been visible in TOML:

1. **Del's introduction was gated on his own schedule** — he is at the desk one night in three, so
   **two players in three would never have met him.** Found writing the opening's handover.
2. **The camera monitor was in a room locked two nights in three**, and it is the corruption
   on-ramp. Moved to the desk, where a clerk would actually watch it.
3. **The bathroom was in two places** — off the corridor in the prose, off the desk on the map.
4. **The opening never explained the audit**, which appears at 02:00 as a button she has never heard
   of. Del now names it in the handover.
5. **The opening never named the $400** — the game's entire objective, unstated, in a screen that
   explained five other systems.
6. **Seventy minutes of night one has nothing arriving.** Still open — it is now eighty, and it
   fell after the funnel rather than inside it, which is the half that mattered.

**Four more, from rewriting the opening as SCREENS rather than as beats:**

7. **The sheet described the second screen and called it the first.** The age gate always comes
   before the starting canvas (`engine.md` §12) and no sheet had a row for it.
8. **The engine has a character screen we had never mentioned** — `CustomizeCharacters`, shipped by
   seven of our fifteen built games. Declaring it repoints the age gate at it, and its text is
   hard-coded: *"Personalize the characters in your story"* would have been the second thing a
   player of this game read.
9. **The boot and the capstone were collapsed into one canvas** — the exact defect
   `the-first-hour.md` F2 names as the reason v2's openings run more than double v1's and still read
   thin.
10. **The funnel had no verbs in it.** Eleven screens of narration and a name box. The player
    reached 23:00 having pressed nothing but Continue.

## What the two ladders are doing

Same nine corruption rungs on both men. **Different relation gates** — Del needs 85 at the top,
Marek needs 50.

That single column is what makes them different people: Del is slow because he holds her debt, the
building and forty years on her, and all three make him careful. Marek is fast because room 6 is the
cheap half, so **the proximity is free** — they already share a bathroom before anything has
happened.

**Three rungs each are conversations that raise nothing and open nothing**, placed directly under an
escalation. That is the field's own device and our skill has never had a name for it.

**Two refusals are authored**, keyed to his corruption running ahead of hers. Del goes quiet for two
nights. Marek laughs and drops it. That one line is the difference between them.

## Register

One voice sample, written in full: [`marek_20_dont_cover_up`](../../sheets/scenes/marek_20_dont_cover_up.md). Both its explicit beats stay on the
body for their whole length and neither ends on what the moment means — the meaning is the next
beat, which is her speaking.

**Every line she speaks exists three ways.** That is the release's whole reason for existing and it
is in all eleven scenes.
