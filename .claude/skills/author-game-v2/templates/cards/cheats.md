# Card — Cheats (infrastructure: a view)

> **A worked card, not a template.** Take the shape, leave the furniture. Every line cites a traced game:
> round 9b, `round9b/cards/cheats.md` and `round9b/traces/cheats.md`. Models: **Course of Temptation (CoT)**
> (an options checkbox) and **Shady Deals (SD)** (a man in the harbor). IHOH and Cupid's Way have none.
>
> **Infrastructure, not a system** (`the-systems.md` SY1): declare it in `board.infrastructure[]` as
> `{ "name": "cheats", "kind": "view" }`, never in `board.systems[]`. It carries or shows other systems; it
> has no ladder of its own. It is a settings and difficulty view.
>
> **The rule is already written:** `the-systems.md` SY7 (the cheat page is free where it saves time) and
> `engine.md` §48 (`[ui.cheat_page]`). This card only shows the models.

| field | the models | cite |
|---|---|---|
| what it is | CoT: Options, Difficulty, an "Enable Cheats" checkbox that adds a Cheats tab; SD: a harbor place reached from the alleys | [OptionsWidget]; [DifficultyOptions]; [CheatGuy]; [Dark Alleys] |
| what it shows | CoT: restore or reduce each of 8 needs, money ±$100 / $1,000 / $10,000, freeze new relationships, freeze breakups; SD: number boxes for 12 values, the top car | [Cheats]; [CheatGuy] |
| where else | CoT: cheat buttons in 9 other screens, among them NPC friendship, lust, romance and control bars and "Grant" on inclinations | [DisplayNPCWidgets]; [InclinationsList] |
| difficulty | CoT sliders, always on: skill gain, weekly debt, relationship gain, need decay, fertility, pregnancy length, out-of-character penalty | [DifficultyOptions] |
| rules: cost | CoT none; SD a trip to the harbor, and ironman mode forbids it | round 9b `cards/cheats.md` |
| how found | SD's Red Phone hints: "Look for a bright red hand symbol somewhere in the harbor. Only in time of need." | [Red Phone] |
| memory | none of its own, it writes other systems' meters; SD ironman remembers the mode and a 21-day cooldown | [CheatGuy] |
| the systems it serves | money, needs, skills, NPC relationship meters (CoT); money, reputation, heat, stats (SD) | round 9b `cards/cheats.md` |
| repair | SD: save patches for 11 versions (16–25) | [CheatGuy] |
| sizes | CoT 8 needs + 3 money steps + 2 toggles + 9 screens; SD 12 number boxes | round 9b `cards/cheats.md` |

## Measured floors (directions, never gates)
- Ship it in the first release: CoT launched without one and drew 7 WANT and 1 WHERE cheat units in its first
  10 days (round 9b `cards/cheats.md`).
- Make it visible: 50 of CoT's 101 cheat units ask or answer where the switch is.
- Money, needs or energy, the main meters and NPC relationship meters are the levers asked for.

## What players say
- *"The Developer has listened to our pleas! A cheat Menu!"* (CoT, mopoga#52259), two weeks after launch.
- *"Too much grind and you can't cheat your way through. There is hardly any tip on how to progress"* (IHOH,
  mopoga#88664).

## Our engine today (round 9b §6)
- `[ui.cheat_page]` exists; see `engine.md` §48 for the free rows and the three time-savers.
