# SP1 · Time — Members Only

> [READY] · drafted 2026-09-29 · signed by LO: 2026-09-29 (same day — LO bypassed the day-after rule for this test)
> A decision record, ≤ 400 words. The rules: `references/the-spine.md` SP1 · `the-clock.md` · `engine.md` §28.

| decision | answer |
|---|---|
| starting day and hour | Tuesday, 17:00 — she arrives at the staff door an hour before her first shift, so the opening lands on a place that is open (the bar floor, 18:00). |
| a day in play is about | 10–15 minutes of play (intent, not measured) |
| canvases that run past midnight | **none, on purpose.** The club floor runs 18:00–22:00, the library and the bar after close 22:00–23:59. She is in bed by midnight, so every window sits inside one weekday. |

**The week** (the shape every ladder window below uses):

| day | what is open |
|---|---|
| Tue–Sat | the bar floor 18:00–22:00 (her shift); the library and the bar after close, 22:00–23:59 |
| Sun | the Sunday count at Julian's desk, 12:00–14:00; the club is shut to members |
| Mon | the club is dark; the docks and the town; Ade's day off |

**The overnight list** — what `[engine.daily_tick]` clears or moves while she sleeps:

| flag or trait | what happens overnight | why |
|---|---|---|
| `worked_shift_today` | unset | one shift a day; the floor's day-cap (`engine.md` §28) |
| `upstairs_today` | unset | at most one paid visit upstairs a day (SP4's income ceiling) |
| `read_for_kessler_today` | unset | one page a night; a step never fires twice in one evening |
| `sleep` | not on the tick — she restores it in her bed at the staff house | a need is refilled by an act, not by the clock (`the-meters.md` M8) |

Dana's tab is **not** on the tick: it is charged by `[settings.rent]` on Sunday (SP4).
