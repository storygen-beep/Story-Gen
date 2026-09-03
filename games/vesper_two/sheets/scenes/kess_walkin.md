# SCENE · Kess — the walk-in  `[READY]`

`walkin_kess_berth` · **`substitution_only = true`** · target of `trigger.substitutions` on
`bench_kess`

⚠️ **Gate `the walk-in floor` reads this room** — she is on a bench alone and Kess is scheduled.
Vesper scored **2 of 10**.

```
the router    trigger.substitutions on bench_kess, chance x conditions, rolled on entry
the branch    ONE canvas, substitution_only = true, [group] bands on `seated`
the payoff    routes back into bench_kess, a rung that already exists
```

| band | chance | what happens |
|---|---|---|
| `seated lt 2` | 0.10 | A customer comes in for a part and Kess does not cover her. |
| `seated 2-3` | 0.30 | The customer stays to watch and Kess answers his questions about the frame. |
| `seated gte 4` | 0.60 | Kess lets the man put a hand in the seam to feel what he means. |

**Same button. The shop gets less private as she gets more open.** The odds ride `seated`, which is
the trait the content is about — that is the whole mechanism, and it is 458–473 bytes per branch in
the field.

⚠️ **The low band is not an act node**, so the 3+ floor does not reach it. The high band routes back
into `bench_kess`, whose three bands carry the floor by construction.

⚠️ **The target MUST declare a `location`** — `getCanvasById` indexes only location-bound canvases
(`v2.py:3177`), so a triggerless rung silently never fires.
