# SCENE · Renner — the walk-in  `[READY]`

`walkin_renner_depot` · **`substitution_only = true`** · target of `trigger.substitutions` on
`renner_depot`'s work row

⚠️ **This is the doctrine's own validated example, and it shipped in `games/vesper`.** What is
copied from it is the **mechanism** — three chance bands riding the same trait as the content — and
nothing else. It encodes no map, no cast and no room.

## The three parts

```
the router    trigger.substitutions on the ACTIVITY ("Haul."), chance x conditions, rolled on entry
the branch    ONE canvas, substitution_only = true, [group] bands on `service`
the payoff    routes into loop_renner_depot, a rung that already exists
```

| band | chance | what happens |
|---|---|---|
| `service lt 20` | 0.10 | He watches from the end of the aisle and does not come down it. |
| `service gte 20, lt 40` | 0.35 | He finds a reason to reach past you, and takes his time about it. |
| `service gte 40` | 0.70 | He backs you into the crates without a word, and you are already turning around for him. |

**Same button. The world leans harder on it as he rots.** DoL's equivalent branches are **458 and
473 bytes**; vesper's is 2.3 KB. The richness is combinatorial, not authored.

⚠️ **The low band is NOT an act node**, so the 3+ floor does not apply to it. The high band routes
into `loop_renner_depot`, whose act nodes carry the floor by construction (see `renner_loop.md`).

⚠️ **The target MUST declare a `location`** — `getCanvasById` indexes only location-bound canvases
(`v2.py:3177`), so a triggerless rung silently never fires.

⚠️ **A walk-in has no door of its own** and can never be the thing the opening hands over to
(`the-first-hour.md` F3).

## Media

`videos/sex/bar_floor_handled_t4/` is the wrong pool — that is the Undertow's. This canvas routes
into the loop and shows the loop's clips; the low and mid bands carry
`videos/locations/renner_depot.jpg`.
