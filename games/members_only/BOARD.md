# The Board — Members Only

> The world, declared before any prose. The ledger (`v2_state.json` → `board`) is the record; this
> page is the readable copy. Doctrine: `references/the-systems.md`, `the-board.md`, `the-map.md`,
> `the-economy.md`, `the-meters.md`. **Not a sheet** — the sheets are the next phase and LO's.

## The map — `nested_zones`

A harbor town at the bottom of a cliff. A path climbs from the town, past the staff house, to the
club at the top; the club's rooms open off its front hall.

```
Town (the ground, outdoors)
├── Docks
└── Cliff Path            — 10 min from the town, 10 min on to the club
    ├── Staff House       — her bed (home base); Noor lives here too
    └── Club              — the front hall
        ├── Bar           — THE ANCHOR
        ├── Dressing Room
        ├── Terrace       — the pool
        ├── Library
        ├── Julian's Office   — a door: it belongs to Julian
        └── Upstairs      — the members' rooms
```

**Where everyone sleeps:** Noor — the staff house · Kessler — upstairs (he keeps a room) · Julian
and Ade — in town, offscreen. **Map sign-off:** LO's, not mine — still open.

## The places — what each is for, and its word budget

| place | why she goes there | needs · work · people | budget |
|---|---|---|---|
| **Bar** (anchor) | her shift: trays, tables, tips, being looked at | work: the evening shift · Ade, Julian, Noor, Kessler | 7,000 |
| Upstairs | a paid visit when a member books her; the service stairs if she goes alone | work: paid visits · Kessler | 4,000 |
| Library | Kessler's chair after close; the pages | Kessler | 3,000 |
| Dressing Room | hair, makeup, the dress; Dana's locker | need: look · Noor | 2,000 |
| Terrace | the pool; members watch whoever swims | Noor | 2,000 |
| Staff House | her bed; nobody books her here | need: energy · Noor | 1,500 |
| Julian's Office | the Sunday count; the members' book is in here | Julian | 1,500 |
| Docks | the boats; where Dana left from | Ade (Monday) | 1,000 |
| Club | the front hall; Julian checks her over | Julian | 800 |
| Town | the shop, the street, where the talk reaches | — (the ground) | 800 |
| Cliff Path | seen on the walk in whatever she has on | — (a corridor) | 500 |

**Total 24,100; the Bar holds 29%** (the anchor rule wants 25% or more). Seven of eleven places carry
heat (the floor is 60%); Town, Docks, Club and Julian's Office are cold on purpose.
**Walk-ins:** the dressing room (Noor or Julian, while she changes) and the staff house (Noor).

## What the game keeps track of about her — the systems

| system | kind | fed at | read by |
|---|---|---|---|
| `look` — hair, makeup, the dress done | sourced | Dressing Room | Julian lets her on the floor and upstairs; members and Kessler comment |
| `worn_exposure` — what she has on | sourced | Dressing Room | every public room's line; the tables she gets; Kessler step 2 |
| `kessler_stage` — the pages she has read | sourced | Library | Julian's tab figure; Ade's and Noor's lines; the doors the pages name |
| `reputation` — who knows she goes upstairs | sourced | Upstairs | staff, Ade, members, the town — changes the words, rarely a door |
| her past (three start flags) | sourced, set once | Staff House | Ade, Julian, every page |
| `money` | ambient | Bar, Upstairs | the Sunday tab; the shop; the charger |
| `energy` | ambient | Staff House | under 20: no shift, no upstairs |

**Room labels (cut down to what these read):** public · private · outdoors · has_mirror ·
she_can_undress · she_can_sleep · home_base.

## Her body — the two needs

| need | falls | fills | shuts |
|---|---|---|---|
| `energy` | 10 a day; 30 a shift; 20 a visit upstairs | Staff House · Sleep · 8 hours | under 20 Julian sends her home: no shift, no upstairs |
| `look` | 20 a day; 40 a shift; 50 a visit upstairs | Dressing Room · Hair and makeup · 30 min | under 40 she is not allowed on the floor or upstairs |

## The meters

**Who climbs: both.** Her three tiers — `shown`, `favour`, `nerve` — are the floor; each person's
counter is the spine of his arc. `reputation` is an audience meter (W5b), not a tier. `arousal`
throttles the act loop upstairs and resets at the finish. Rung numbers are still provisional
(`SKILL_TEST_FINDINGS.md` #19).

## The cast — schedules and the label under each name

| person | label | where and when |
|---|---|---|
| Julian (46) | manager | front hall Tue–Sat 17:30–18:30 · the bar 18:30–22:00 · his office Sun 12:00–14:00 |
| Ade (34) | bartender | the bar Tue–Sat 17:00–23:00 · the docks Mon 11:00–14:00 |
| Noor (27) | hostess | staff house daily 09:00–16:30 · dressing room Tue–Sat 17:00–18:00 · the bar 18:00–22:00 · the terrace Sat 22:00–23:59 |
| Kessler (63) | member | his table at the bar Tue–Sat 19:00–22:00 · the library 22:00–23:00 · his room upstairs 23:00–23:59 |

## Money — what it is for

- **Earned:** tips on the shift; paid visits upstairs (see SP4).
- **Taken:** Dana's tab, Sunday, by Julian ($300, rising to $500 as the pages come in).
- **Bought, and it stays bought** (R1b): a charger for Dana's phone ($40, opens her messages) · a
  dress of her own from the shop ($150, opens a member's table) · a boat to where Dana went
  ($1,000, the next goal — a door past v0.1).

## The shortcuts page (SY7)

Free, no code: money · skip to morning · the next step now (one per ladder step) · ask again
(Kessler step 4's counted no). Written into `[ui.cheat_page]` when the TOML is built.

## Open questions for LO

1. **The map sign-off** — yours.

*Settled 2026-09-29: the currency is **"$"**, the skill's house default, and the prose names no
real-world currency (`the-economy.md` R7). Changed from $ in the Want, the idea page, SP4 and here.*
