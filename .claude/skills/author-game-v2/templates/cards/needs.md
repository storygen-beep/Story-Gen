# Card — Needs (a system)

> **A worked card, not a template.** Take the shape, leave the furniture. Every line cites a traced game:
> round 9b, `round9b/cards/needs.md` and `round9b/traces/needs.md`. The model is **Course of Temptation
> (CoT)**. Fill your own card on `templates/sheets/system.md`; record it in `board.systems[]`.
>
> ⚠️ **Hygiene only, by default (LO, WS-D5).** One need: hygiene. Its refill places always roll an event
> (the shared shower). Low hygiene has a cost, never a game over. Give it an off switch (a start choice).
> Add hunger only when the premise needs it. Like every system it must lead to a person or a sex scene.
> Why needs exist at all, in CoT's own code: *"needs are a thing the player must balance, necessitating time
> management and pushing the player to do things that lead to events (like venturing into co-ed showers to
> get clean)"* (`cot_27_database_needs.js:2-3`).

| field | the model (CoT hygiene) | cite |
|---|---|---|
| place and hours | the dorm's co-ed shower room, any hour (no opening hours); a quiet gym locker shower with the gym; a restroom "Wash up" | [ResidenceShowers]; [ShowerStall]; [GymShower] |
| cost | 15 minutes for a full refill (wash-up: +25 in 5 minutes); leaving the stall needs Exhibitionism by what she is wearing | [ShowerStall]; [ExitShower] |
| one ladder or two | **one**: a need never pays; the lewd ladder is the refill place's event pool | round 9b `cards/needs.md` |
| pay ladder | none. Hygiene does not even gate work (5 other needs do) | `cot_50_needs.js:490-493` |
| lewd ladder | the shower pool, opened by kink toggles and her inclinations: a peeker, a laugh from the next stall, an almost-walk-in, stolen underwear, a fuck-buddy joining, a roommate's-partner chain; crossing the hall rolls a hall-dash pool when more than 3 people are there | round 9b `traces/needs.md` §1.5 |
| people | whoever is there; and hygiene changes every NPC's liking: under 200 cuts every friendship, lust and romance gain to 1/10; at 500/250/100/0 it adds 1/2/3/4 to dislike | `cot_53_people.js:684-688`; `cot_53_people.js:1803-1809` |
| pool, daily | shower pool 20 entries (14 distinct passages), 9 kink-gated; "Uneventful" holds 3.5% of the weight (heuristic) | round 9b `cards/needs.md` |
| memory | hygiene at 0 unlocks the "Natural Odor" inclination; event memory per passage | `cot_50_needs.js:22-28` |
| growth | decay only: full to empty in 36 hours, 18 in dirty clothes; an options multiplier scales all decay | `cot_68_time.js:7`; `cot_50_needs.js:117-120`; round 9b `traces/needs.md` §1.2 |
| sink and deadline | not a money system: the sink is time (15 minutes a day); the soft deadline is the 200 line where people stop warming to her | `cot_53_people.js:684-688` |
| feeds · reads | feeds every NPC's liking and the relationship rule "good hygiene" · reads what she wears (dirty clothes double the drain) | `cot_50_needs.js:117-120`; round 9b `traces/needs.md` §1.3 |
| link into the hook | getting clean means getting naked in a co-ed room | [ShowerStall] |
| leads to | the peeker, the joiner, the fuck-buddy in the stall | [ResidenceShowers] |

## The rest of CoT's needs (the measured model, not the default)
- 8 needs + 5 fleeting meters, 0–1000. Full to empty: Food 20 h, Bladder 24 h, Rest 32 h, Hygiene 36 h,
  social 60 h, Release 8 days. `cot_27_database_needs.js:5-51`; `cot_68_time.js:7`.
- At 0, 5 needs block work and 3 block fast travel (`cot_65_storyfunc.js:3480-3493`). Bladder, Rest and Food at
  0 roll a Willpower check on room moves (+2 difficulty per repeat, then 2 free moves); a fail is a blackout
  into the clinic or a public accident with witnesses. [BladderFailure]; [Passout]; [TotalBladderFailure].
- Hunger refills always roll an "eat" pool (24 and 22 entries at two counters). [QuickieBurger].
- A pure budget bar (one energy bar, 6 actions a day) remembers nothing: it is the game's clock, not a system.
  Round 9b `cards/needs.md`.

## Measured floors (directions, never gates)
- A 20–36 hour drain means about one visit a day: enough to route her, not enough to grind. Round 9b `cards/needs.md`.
- Refills take 3–15 minutes. Every refill place that matters rolls an event; the co-ed shower pool is 20. Round 9b `cards/needs.md`.
- Zero is a scene, never a game over. [Passout].

## What players say
- Needs are a quiet topic: 294 judged units, bug 47, complain 21; only 6 of 242 grind complaints name needs.
  Round 9b `cards/needs.md`.
- The real failure is a stuck sleep loop: *"I can only stay in room and sleep"* (CW, mopoga#112704); *"can't
  move after sleeping"* (CoT, mopoga#50909/r2). When sleep is the day's only advance, a broken sleep passage kills the game.

## Our engine today (round 9b §6)
- Decay toward a value exists (`v2.py:6706`) and a daily tick runs effects at day rollover
  (`template_import.py:744`); there is no sleep primitive and no event roll tied to a refill.
- The skill's hygiene rule lives in `engine.md` §30.1 (WS-D5: hygiene for routing only).
