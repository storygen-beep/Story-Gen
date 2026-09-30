# SP1 · Time — Billable Hours

> [READY] · drafted 2026-09-30 · signed by LO: LO, 2026-09-30
> A decision record, ≤ 400 words. The rules: `references/the-spine.md` SP1 · `the-clock.md` · `engine.md` §28.

| decision | answer |
|---|---|
| starting day and hour | Monday, 07:00: her first day at Callahan Reed, in her room at the house (`[time] starting_hour = 7`; C1: the first screen is the only clock reading the engine pins) |
| a day in play is about | 10 minutes of play (intent; no instrument yet) |
| canvases that run past midnight | none in v0.1. The Velvet Room's windows close at 23:59 |
| the week's fixed points | Mon–Fri 09:00–17:00: the firm is open. Friday: the payment arms at 00:00 (`engine.md` §26, `v2.py:6168`). Friday 19:00–22:00: Martin's study |

**The overnight list:** what `[engine.daily_tick]` clears or moves while she sleeps.

| flag or trait | what happens overnight | why |
|---|---|---|
| `worked_today` | unset | caps the firm's paid shift at one a day; the flag goes on the hub choice (`engine.md` §28.1) |
| `breakfast_today` | unset | caps Martin's breakfast talk, which raises his want (+1, stops at his next step's threshold, `the-arc.md` A4) |
| `nerve` | nothing | her tier; it never decays (`the-meters.md` W4) |

Each flag here has a setter and an `is_false` reader, or the gate `a day-cap closes` fails (`engine.md` §28.2). The board confirms both.
