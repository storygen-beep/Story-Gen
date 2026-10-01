# Card — Streaming (a system)

> **A worked card, not a template.** Take the shape, leave the furniture. Every line cites a traced game:
> round 9b, `round9b/cards/streaming.md` and `round9b/traces/streaming.md`. Model: **Course of Temptation (CoT),
> Niche.tv then CollegeCams**; contrast: **In Her Own Hands (IHOH)** and **Shady Deals (SD)**. Fill your own card on
> `templates/sheets/system.md`; record it in `board.systems[]`.

| field | the model (CoT) | cite |
|---|---|---|
| place and hours | her own room, on a computer or phone; viewers follow the hour (0.2 at 6–7am, 1.0 from 8pm to 1am); rounds stop at 22:00 (24:00 Fri–Sat) | [NetNicheTV]; [NetCollegeCams] |
| cost | SFW round 60 min, Rest −15; cam round 30 min, Rest −15; registering 60 min. Gear caps viewers: phone 100, cheap laptop kit about 280, top kit about 1,010 | round 9b `traces/streaming.md` |
| one ladder or two | **one**: each lewder rung has a higher tip range, popularity multiplies it, and doing the act raises the skill that opens the next rung | round 9b `cards/streaming.md` |
| pay ladder | SFW tips net of the 30% cut: about $7/h at 10 viewers, $27/h at 1,000. Cam ambient tips $1.6–6.2 per 30 min; **priced requests are the money**: $0.7–22.8 an act by rung, face reveal $16–32, the pizza dare $32–81 | round 9b `traces/streaming.md` |
| lewd ladder | SFW stream · accidental exposure (41 of 95 events need a clothing state) · invite to the cam site (popularity 500, or 250 if she has shown skin) · flash, remove top, bra, underwear · spit, spank, play with tits, finger herself, toys · cum, lick cum, dominate · strip tease · partner strip, oral, sex · face reveal · library stealth stream · pizza-delivery dare. **16 skill rungs** over 36 requests | [CollegeCamsStreamPrep]; [EventStreamingXSuggestLibrary]; round 9b `traces/streaming.md` |
| people | generated chatters (supportive 20, troll 10, unfunny 10 weights); an exhibitionist partner she invites; a fan (popularity 300, face known); an e-girl streamer (50); classmates who recognize her (250) | round 9b `cards/streaming.md` |
| pool, daily | 95 stream events, 26–28 per type when her face shows; cams 5 round events + 36 requests; an event seen this stream drops to 0.2× | `cot_40_events.js:461`; round 9b `cards/streaming.md` |
| memory | screen names, streams and popularity (0–1000) per platform, strikes and ban, anonymity, what she has shown, money and hour totals | round 9b `cards/streaming.md` |
| growth | +10 to +40 per stream of 3+ rounds (cap 40/30/20/10 by band; a second stream that day ×0.25): **54–100 streams** to max. **No decay**. 3 strikes = a 3-day ban, −1 strike per clean week. Face shown once = known forever | round 9b `traces/streaming.md` |
| sink and deadline | gear (raises the viewer cap) and the weekly bill | [WeeklyDebtPayment]; round 9b `cards/streaming.md` |
| feeds | money; her skills (Exhibitionism and others); being known on campus | round 9b `cards/streaming.md` |
| reads | gear quality, what she wears, her skills, popularity, whether her face is known | round 9b `cards/streaming.md` |
| link into the hook | the invite arrives as a campus-walk encounter; once her face is known, classmates and the fan find her in person | [EventStreamingXInvite]; `cot_20_database_events.js:6905` |
| leads to | the cam site; partner on cam; the library dare | [CollegeCamsStreamStart]; [CollegeCamsStreamPrep]; [EventStreamingXSuggestLibrary] |

## Measured floors (directions, never gates)
- One audience meter she can see. Round 9b `cards/streaming.md`.
- 4 or more rungs (IHOH: lingerie, nude, masturbation, toys). [Cam_StartShow]
- 2 or more acts per rung; 20 or more events per pool if the click repeats daily. Round 9b `cards/streaming.md`.
- Pay grows with both the rung and the audience. Round 9b `cards/streaming.md`.
- Show the missing skill on a locked request, so the next rung is visible (CoT `hintskillgate`). [NetCollegeCams]
- A SFW stream alone is grind; ship it only with the exit (accidents and the invite). Round 9b `cards/streaming.md`.

## What players say
- *"it takes too long to progress in jobs and streaming"* (CoT, mopoga#117541).
- *"being pointed out by strangers when walking in public"* (CoT, mopoga#52889): fame should leak into her life.
- Only 5 complaints in 146 judged streaming comments across 15 games.

## Our engine today (round 9b §6)
- Missing as a system: no viewers, tips or stream session. A follower count exists as a plain player trait
  (`v2.py:2964`, `act.counter_trait || 'followers'`), so `trait_decay` can decay it.
- No computed tips (`v2.py:15899`, "only 'random' is supported"); author tip bands per rung instead.
