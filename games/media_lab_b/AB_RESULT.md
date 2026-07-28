# Q2 A/B — arm B run, 2026-07-28

Arm B (`find-media-b`) filled all ten `media_lab_b` slots. **Arm A is untouched**
(`game-review/load?game=media_lab` → 0 missing / 10 found).

- **Arm A** = `games/media_lab/`, `find-media`: gates + strip, then HEAT/SETTING/CRAFT ranks the install.
- **Arm B** = this game, `find-media-b`: gates + strip only. Install the FIRST candidate that
  passes, in `fetch_candidates.py` order. No scoring, no ranking, no taste.

Both arms judged the **identical candidate shelf** (arm A's `media_options.json`, copied), the
identical ten beats, descriptions and `search_queries`, and the identical gate lists (arm B's
scope briefs are arm A's with `intended_heat` and the setting axis stripped out — see
`.find-media/scope/`). **The judging rule is the only variable.**

## The comparison set

**0 of 10 slots are ties** — every arm-B install is a different file from arm A's. That makes
this a clean ten-way head-to-head: same beat, two picks, nothing to control for.

| slot | arm A | arm B |
|---|---|---|
| `lab_eyecontact_t5` | 1738K | 2023K |
| `lab_tease_t4` | 1001K | 542K |
| `lab_flash_t4` | 497K | 5537K |
| `lab_alley_t5` | 3053K | 1903K |
| `lab_finish_inside_t5` | 2570K | 5989K |
| `lab_finish_facial_t5` | 1901K | 982K |
| `lab_group_t5` | 2343K | 4956K |
| `lab_behind_t5` | 690K | 771K |
| `lab_passive_t5` | 5071K | 1995K |
| `lab_room` | 555K | 23K |

Play both and say which arm's picks you'd keep. A 6–4 split means nothing at n=10 with one
judge; only something lopsided does.

## What arm B cost, in numbers

- **31 strip kills** across the run — candidates that survived the fetch and died on the strip.
  Question 1 is doing real work in both arms; that number is not the thing under test.
- **1342 options** still on the shelf, unranked. Arm B stocks but makes no claim about order.
- `scores.jsonl` per slot records **every** rejection with a named gate reason, and marks
  everything after the install `not_examined` — arm B never sees what it skipped, by design.

## The gate rule I had to fix mid-run, stated so it can be audited

Two slots forced a decision the brief didn't settle: what to do when a `must_show` item is
simply **outside the frame** rather than visibly absent. The rule I settled on and then applied
uniformly to all ten slots:

> A `must_show` fails when the strip shows it ABSENT or CONTRADICTED. If the framing merely
> doesn't cover it, it is UNVERIFIED, not failed — **except** for gaze/affect items, which fail
> when their carrier is cropped out, because affect has exactly one carrier and a cropped face
> means the beat's content is absent, not merely unproven.

That is why `lab_eyecontact_t5/08` passed on unverifiable posture (POV is marked FINE for that
slot and the eyes — the carrier — are held in every frame), and why `lab_tease_t4/00` failed
(a covert downblouse whose face is never in frame, so "aware of the camera" can never be shown).
Apply the same rule to arm A's evidence if you want to check I was even-handed.

## Two things arm B installed that arm A's craft axis would likely have caught

Neither is a gate failure. Both are exactly the class of difference this experiment exists to
surface, so they are recorded rather than fixed:

- **`lab_group_t5`** — a **390×909 three-panel vertical composite**. Correct on every gate
  (3 men + 1 woman visible simultaneously in each panel), and a tall narrow triptych in the
  built page.
- **`lab_room`** — a **525×350 vecteezy thumbnail**. Correct on every gate; small.

## One known miss, and why it is NOT evidence about ranking

**`lab_finish_facial_t5`** — 16 of 16 candidates stripped, and **not one** shows his hand at the
back of her head. The men's hands are on themselves in every clip in the pool. Arm B installed
the least-bad (fewest gate violations, ties broken by fetch order) and flagged it
`POOL_GATE_UNSATISFIABLE`.

This is a **shelf/vocabulary** limit, not a ranking one: the gate is identical in both arms, so
whatever arm A installed there also failed it or the gate was applied unevenly. Discount this
slot when judging the A/B. Note it is also one of the three OLD-doctrine control slots, whose
queries (`bedroom tender facial cumshot gentle`, `loving facial girlfriend soft`) are already
measured to poison Google's intent class.

## Limitations — read these before drawing a conclusion

- **n = 10, one run, one judge, not blind.** Directional at best.
- **I know arm A's picks.** Mitigation: arm B's install involves no choice — first gate-survivor
  in a deterministic fetch order — so bias could only enter through a gate call, and every gate
  call is recorded with its reason in `scores.jsonl` for audit. I did not re-read arm A's
  `scores.jsonl` during the run; the file-level comparison above was run only after all ten
  installs were done.
- **The shelf was copied, not re-searched.** Deliberate: today's measurements showed large
  hour-to-hour variance in what Google returns, and a fresh harvest would have confounded the
  judging rule with search luck. The cost is that arm B never had a chance to find something
  arm A's search never surfaced.
