# SP1 · Time — Probation

> [REVIEW] · drafted 2026-09-29 · **amended 2026-09-29: needs LO's re-sign** (was signed 2026-09-29)
> A decision record, ≤ 400 words. The rules: `references/the-spine.md` SP1 · `the-clock.md` · `engine.md` §28.

| decision | answer |
|---|---|
| starting day and hour | **Tuesday, 12:00**: Tobin fits the band, then Delgado at two. *Amended by LO's ruling; the engine starts on the hour (`v2.py:1476`, minute 0).* `[time] starting_day = "Tuesday"`: the engine stores the day as a name (`v2.py:1477`, `engine.md` §24.2) |
| a day in play is about | **15 minutes** of play (intent: no instrument yet) |
| canvases that run past midnight | **Rae's laundry, 02:00–04:00**, every day. The window starts after midnight and does not wrap, so it is one row with all seven days (`engine.md` §6) |
| the day counter | **`review_days`**: a player trait, +1 a night from `[engine.daily_tick]` `traitEffects` (`v2.py:6066-6085`). The reviews read it. Not clamped; the tick's clamp defaults to false (`v2.py:6083`) |
| the reviews | the first **Tuesday** on or after `review_days` 30, then 60, then 90. Review 1 falls on **day 36** (Tuesday, `review_days` 35) |
| the week's fixed hours | Tuesday: Tobin 12:00–13:00, Delgado 14:00–16:00 · Friday: the sheet at Marty's, 18:00–19:00 · every day: home by eight |

**The overnight list**: what `[engine.daily_tick]` clears or moves while she sleeps:

| flag or trait | what happens overnight | why |
|---|---|---|
| `review_days` | `add` 1 | the monthly reviews read it |
| `*_today` flags on day-capped hub choices (e.g. `shift_today`) | `unset` | the cap pattern in `engine.md` §28; the flags are named on the sheets |
| `rest` · `food` · `wash` | fall by their daily rate | declared in `board.needs`. The mechanism (`[player.trait_decay]`) is checked in the board phase, not here |
| `battery` | **nothing** | it is spent by the hour away from the dock, not decayed by the day (`board.needs`, `board.systems`) |

**Open:** the engine also keeps `time_state.day` (`v2.py:1479`). No condition is known to read it,
so the reviews use `review_days`, the path that is verified.
