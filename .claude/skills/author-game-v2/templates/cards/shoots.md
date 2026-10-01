# Card — Shoots (a system)

> **A worked card, not a template.** Take the shape, leave the furniture. Every line cites a traced game:
> round 9b, `round9b/cards/shoots.md` (no separate trace). Model: **Cupid's Way (CW), the modelling studio and the
> porn studio**; contrast: **Course of Temptation (CoT)** and **Shady Deals (SD)**, whose cameras record sex the game
> already has. Fill your own card on `templates/sheets/system.md`; record it in `board.systems[]`.

| field | the model (CW modelling) | cite |
|---|---|---|
| place and hours | a photo studio in the city, closed at night (`$time>2`) | [Lance photography] |
| cost | half a time slot per session | round 9b `cards/shoots.md` |
| one ladder or two | **one**: each tier is a nudity step, and the tier sets the pay. Shoots open the next tier | round 9b `cards/shoots.md` |
| pay ladder | fashion 20 + Looks, lingerie 100 + Looks, erotic 250 + Looks; **paid at most once per 3 days**, and the studio says so: sessions in between are "for free to practice". Then the porn studio: $500 a scene | [Lance photography]; [porn options] |
| lewd ladder | fashion, then lingerie (model skill 7), then erotic (skill 14 and corruption stage 1, i.e. corruption 20+); then 3 porn scenes, each $500 and +1 corruption, one a day | [bbc1]; [bbc2]; [white1]; [porn options] |
| people | the photographer; a customer roll and story gigs (round 8) | [Lance photography]; round 9b `cards/shoots.md` |
| pool, daily | photo sets **9 / 7 / 8** per tier; porn studio one request a day | round 9b `cards/shoots.md`; [porn options] |
| memory | `$model` skill: +1 to 7, then +0.5 on fashion; +1 to 14 on lingerie; +1 to 21 on erotic; pop-ups at 7, 14 and 100 | round 9b `cards/shoots.md` |
| growth | climbs, no decay | round 9b `cards/shoots.md` |
| sink and deadline | clothes and beauty; no deadline in the model | round 9b `cards/shoots.md` |
| feeds | money; corruption (porn scenes; a $50 blowjob offer after a shoot, +1 corruption) | [porn options]; round 9b `cards/shoots.md` |
| reads | Looks (in the pay), model skill and corruption (the tier gates) | round 9b `cards/shoots.md` |
| link into the hook | the post-shoot offer and the porn studio turn modelling into sex | round 9b `cards/shoots.md` |
| leads to | the porn studio | [porn options] |

## Measured floors (directions, never gates)
- 3 tiers, about 7 shoots per tier, pay rising about ×2–5 a tier (20 / 100 / 250). Round 9b `cards/shoots.md`.
- 7–9 image variants per tier (CW 9 / 7 / 8). Round 9b `cards/shoots.md`.
- If pay has a cooldown, say it on screen before the shoot. [Lance photography]
- Authored studios stay small (CW porn 3 scenes, CoT's studio 4 shoots at $1,000–1,200). Only the recorder shape
  scales: SD tags 116 sites in 91 passages with 28 tags, 3 trending; CoT sells any recorded encounter at
  views × price × 0.7 a day, views falling by (days+1)^−0.5. Round 9b `cards/shoots.md`.

## What players say
- Asks: *"Porn option?"* (CoT, mopoga#71942); *"why not add porn role, and modeling options"* (CoT, mopoga#118678).
- Lost or broken: *"How to go to the modelling job on test day"* (CW, mopoga#124811); *"Modeling catwalk doesn't
  exist after sauna"* (CW, mopoga#82433). Only 11 quotable comments match shoots at all.

## Our engine today (round 9b §6)
- Missing as a system (the skill has 0 hits for shoots); build it from canvases with tier conditions.
- Pay of tier + Looks reads two traits, and a stat-based value reads one (`{type = "trait"}`, `setup.resolveEffectValue` (`v2.py:6825`)):
  author one value on Looks per tier.
