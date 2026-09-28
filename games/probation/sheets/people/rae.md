# PERSON — Rae  `[REVIEW]`

**Role:** `owns the building`
**Bible, one line:** Runs the laundry, owns the building, up at four. Notices everything and says
almost none of it.
**Home:** `the_laundry` — the back flat behind the machines. Same location, declared. Not an
enterable room in 0.1 and named as deferred on `DECISIONS.md`.
**Meeting flag:** `met_rae` · opens her hub only. Fires two days after Marty's third refusal, or on
the first `hours ≥ 25` night, whichever comes first.
**Meter:** `trust` 0–100 · **3 rungs — 5 / 30 / 60** (field median per person is 3)
**Direction (A5b):** **HERS.** Rae never asks for anything. What climbs is how far Cass will go
with someone whose good opinion she does not want to lose.

## Schedule grid

<pre>
                    Mon    Tue    Wed    Thu    Fri    Sat    Sun
  the_laundry     12-14  12-14  12-14  12-14  12-14  12-14  12-14
  the_laundry     22-04  22-04  22-04  22-04  22-04  22-04  22-04   ← overnight, ONE row
  the_stairwell   04-05  04-05  04-05  04-05  04-05  04-05  04-05   ← added with the stairwell
  the_diner       05-06  05-06  05-06  05-06  05-06  05-06  05-06
</pre>

**4 rows, no overlap.** The stairwell row sits exactly in the gap between the laundry night and the
diner hour — verified, not eyeballed. ✅ **The overnight row is legal as ONE row because it covers every
weekday** — `weekdays = [0,1,2,3,4,5,6]`, `22:00–04:00`. `isCurrentTimeSlot` handles the wrap
(`v2.py:3784`); the weekday check runs first and against **today** (`v2.py:3596-3597`), which is
what breaks a day-specific overnight window. Both halves verified; an older project note claiming
overnight always needs two rows is half right and would double this row for nothing.

## The ladder

| # | rung | canvas | where · when | gate | screen? |
|---|---|---|---|---|---|
| 1 | She hands Cass the keys to the machines and goes back to the flat | `rae_01_keys` | `the_laundry` · 22:00–04:00 | `trust ≥ 5` · `hours ≥ 25` | ✅ |
| 2 | The night sit — Rae pays cash to have somebody in the room | `rae_02_sit` | `the_laundry` · 22:00–04:00 | `trust ≥ 30` | ✅ |
| 3 | **explicit** · after two, with the machines running | `rae_03_after_two` | `the_laundry` · 02:00–04:00 | `trust ≥ 60` · `hours ≥ 40` · `arousal ≥ 20` | ✅ |

**Effects, ops named:** rung 2 grants `money` **`add`** `+18`, **`clamp = false`** — money is a
QUANTITY, not a 0–100 meter, and a clamped grant is the failure where a scene declared `+120`, state
went 0 → 100, and the eviction branch became the only reachable outcome.

## Refusals
Hers, both **PARKED**: *"She is down there every night from ten."* There is nowhere else to be, and
the game says so rather than pretending the offer expired.

## The repeatable
`the_laundry` after two · node-routed · act menu 2 wide.
**BRAKE, on the trigger:** `schedules = [{ start = "02:00", end = "04:00", weekdays = all }]` +
`max_triggers_per_day = 1`. The window is the brake — two hours a night, and she has to still be
awake.
**Media:** `pool_dir = "sex/laundry_night_t5"`, `pool = 4`.
**Aftermath:** Rae goes back to folding. What Cass is left holding is that Rae has still never asked.

## Guidance
`card_rae`, behind `met_rae`.
