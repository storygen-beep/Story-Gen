# [REVIEW] SP1 · Time — First Term

> Changed 2026-11-04 to match the build; waits for LO's re-sign. Padding cut: the flag names are in `[engine.daily_tick]`.
> Changed 2026-11-04 to match the build; waits for LO's re-sign. The overnight counts: 127 flags, 42 of them walk-in caps.
> Changed 2026-11-04: the overnight list adds Zoe's and Jake's patience and two flags (Q5); Mark's table counts nothing (Q6). Waits for LO's re-sign.
> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign.
> [REVIEW] (was [READY]) · drafted 2026-10-03 · updated 2026-10-08 (the clock in hours) · signed by LO: LO, 2026-10-08
> A decision record, ≤ 400 words. Rules: `the-spine.md` SP1 · `the-clock.md` · `engine.md` §28.

| decision | answer |
|---|---|
| start | Monday 07:00, her first morning of college; the only hour the prose may name |
| a day in play | 15–20 minutes |
| past midnight | Zoe's parties (to 02:00), Ryan's room late: a second schedule entry next weekday |
| the clock (LO, 2026-10-08) | night 22:00–07:00 · early 06:30–08:00 · classes 08:30–10:00, 10:15–11:45, 13:00–14:30 · lunch 11:45–13:00 · afternoon 14:30–18:00 · evening 18:00–22:00 · late 22:00–00:00 |
| hours that are rules | café Monday–Saturday 08:00–22:00 (Tom to 23:00) · park 07:00–22:00 · party Friday 19:00 to Saturday 02:00 · three classes a weekday, one on Friday |
| rent | the engine takes it Sunday 00:00, once Mark's rent scene has run; his table scene comes after and counts nothing (Q6) |
| prose and time | a beat never reads the clock; a closed row shows its hours |

**The overnight list** — `[engine.daily_tick]` at midnight: 127 flags cleared, three traits moved.

| what | overnight |
|---|---|
| `curfew_days` | −1, never below 0 (Laura's curfew counts down) |
| `zoe_patience` · `jake_patience` | +1 each, up to 6 and 3: a no-show or an ignored invite empties it, and her next invite waits until it is full (Q5) |
| 42 walk-in caps | cleared: `walkin_<canvas>_today`, one per walk-in canvas, so each walker comes once a day |
| 60 day caps | cleared: the `_today` flags |
| 25 once-a-day flags | cleared |
| `hygiene` | falls 10 (`[player.trait_decay]`); with hygiene off nothing reads it |
| not on the tick | `energy` (her bed refills it) · `drinks_boost` (ends 3 hours after the last drink) · `rent_short` (set each short Sunday, cleared only by a full payment) · `laura_rule_ryan_first` · every meter and step counter |

All 127 names are in `[engine.daily_tick]` in the TOML.

**A flag that must cross midnight is never on the tick** (LO, 2026-10-07); it is read by hours since it was
set. The party sets `party_went` and its late part reads hours since it, so midnight never splits one party.

Not decided here: her needs (energy and hygiene, no hunger) and Ella's meters (SP2).
