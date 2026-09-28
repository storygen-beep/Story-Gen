# PERSON — Tobin  `[REVIEW]`

**Role:** `services the boxes`
**Bible, one line:** 26, contractor at the county office, bored. Can make the box say anything and
is not interested in why.
**Home:** `offscreen`
**Meeting flag:** `met_tobin` · his own. Fires on her second Tuesday.
**Meter:** `trust` 0–100 · **3 rungs — 5 / 30 / 60**
**Direction (A5b):** **A CONTEST.** He holds the one thing she wants and does not care about it; she
holds nothing he wants until she does. Pursuing him slopes the `clean` route, and nothing slams.
**He is the `ankle` system.** Fed at exactly one bench, by exactly one person.

## Schedule grid

<pre>
                          Mon    Tue    Wed    Thu    Fri    Sat    Sun
  the_county_office         —   09-13    —    09-13    —      —      —
  the_diner                 —      —      —      —  23-23:59 23-23:59  —
  the_diner                 —      —      —      —      —   00-01  00-01
</pre>

**3 rows, and rows 2–3 are ONE window split on purpose.** A day-specific overnight window needs two
rows: `[4,5] 23:00–23:59` and `[5,6] 00:00–01:00`. Written as `[4,5] 23:00–01:00` he is on site
Friday night and **deleted at midnight**, because `todayIndex` is Saturday and Saturday is not in
the list. This is the exact trap `the-board.md` §2 names and it is invisible in a build.

## The ladder

| # | rung | canvas | where · when | gate | screen? |
|---|---|---|---|---|---|
| 1 | He runs the diagnostic and talks the whole time | `tobin_01_bench` | `the_county_office` · Tue/Thu 09:00–13:00 | `trust ≥ 5` | ✅ |
| 2 | He shows her what the log actually looks like | `tobin_02_log` | same | `trust ≥ 30` · `vouch ≥ 15` | ✅ |
| 3 | **explicit** · the bench, before the two o'clock | `tobin_03_bench` | `the_county_office` · Tue 12:00–13:00 | `trust ≥ 60` · `arousal ≥ 20` | ✅ |

**Rung 2 is the `ankle` feed:** `trait` `ankle` **`set`** `1` (loose). Rung 3 does **not** raise it —
the seal and the sex are two separate transactions and he prices them separately. `ankle 2` is
`vouch 60` content and is not in 0.1.

**`clean` cost, op named:** rung 2 is `trait` `clean` **`add`** `-6`. Rung 3 is `-2` — sleeping with
him is *cheaper* than letting him touch the box, which is the whole joke of the character.

## Refusals
Hers, **PARKED**. His, none — he does not care enough to refuse.

## The repeatable
`the_county_office` bench · **BRAKE on the trigger:** `schedules` Tue 12:00–13:00 only, plus
`max_triggers_per_day = 1`. One hour a week is the brake. It is the tightest window in the game and
it is deliberate — he is the cheapest transaction and he should be the hardest to *reach*.
**Media:** `pool_dir = "sex/office_bench_t4"`, `pool = 4`.
**Aftermath:** he is already talking to the next person. She is holding a printout she cannot read.

## Guidance
`card_tobin`, behind `met_tobin`.
