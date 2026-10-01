# Card — Sex for pay (a system)

> **A worked card, not a template.** Take the shape, leave the furniture. Every line cites a traced game:
> round 9b, `round9b/cards/sex_for_pay.md` and `round9b/traces/sexpay_sd_stroll.md`. Model: **Shady Deals (SD),
> the street stroll**. Fill your own card on `templates/sheets/system.md`; record it in `board.systems[]`.

| field | the model (SD stroll) | cite |
|---|---|---|
| place and hours | 3 corners (Old Downtown, Suburbs, Harbor), later a 4th at her club; the link "Whore yourself." shows only 18:00–04:00; by day the corner tells her when to come back | [Downtown Butterfly Corner]; [Suburbs Butterfly Corner]; [Harbor Butterfly Corner]; [NightClub PC] |
| cost | 30 min per wait; "Deal!" costs 1 of 6 daily actions plus 30 min; at 0 stamina she is too tired | [Spot Work] |
| one ladder or two | **one**: sluttiness is both the chance a client comes and a term in his price. The climb on top is ownership, not lewder acts | [Spot Work] |
| pay ladder | price = charm × (10–24) + (0–120) + sluttiness × (10–25), +175–350 with the "whore" trait, **shown before she agrees**. Examples: $10–144 at charm 1 / slut 0; $150–490 at 5/10; $300–860 at 10/20. The pimp takes 25% until she owns the corner (his line says 40%) | [Spot Work] |
| lewd ladder | a client comes 29% of the time at sluttiness 0, 52% at 5, 71% at 9, 100% at 15; below 9 the screen says more skin brings clients. The act is set by place, not by rung: Downtown BBC, BBC duo, outdoors; Suburbs pool, motel, BBC; Harbor car, anal at his home, motel. A Timid client gets vanilla, a Kinky one rough sex and anal | [Spot Work]; [Spot Motel Quickie] |
| people | generated men of 2 types (Kinky, Timid), each with his own line; the corner's pimp, whose lines change with the hour and with sluttiness 8+; later her own girls. A named regular: not in the model | [Spot Work] |
| pool, daily | 4 corners × 3 setups = 12 slots, **9 act passages** × 2 client types; at most 6 clients a day; depravity +2 counts only twice a day | [Spot Motel Quickie]; [Spot Limo Quickie]; [Cooldowns] |
| memory | `$stat_prostitution` (22 sites), oral, partner and vanilla or rough counters, depravity; as boss each act costs reputation; jail counts 0.5 per act | [Cooldowns]; round 9b `traces/sexpay_sd_stroll.md` |
| growth | her stats raise the price; taking the corner removes the cut; then up to 7 girls per corner (+4 with an upgrade, 15 at the club) earn daily; rivals can block it | [Downtown Spot Combat]; [Earnings and Spendings NewDay] |
| sink and deadline | businesses, crew, heists; no deadline in the model | round 9b `cards/sex_for_pay.md` |
| feeds | money, depravity, reputation, jail time, and porn: with a camera every act becomes a sellable video tagged "Prostitution" (9 of 9 acts) | [RAW Widgets] |
| reads | sluttiness (her outfit), charm, the "whore" trait, actions left, boss status | [Spot Work] |
| link into the hook | the outfit decides whether a man stops; the camera turns each act into porn | [Spot Work]; [RAW Widgets] |
| leads to | the corner fight; running girls; the video shop | [Band Creation]; [Downtown Spot Combat] |

## Measured floors (directions, never gates)
- The price is on screen before she says yes. [Spot Work]
- 2 or more client types, each with his own line and act mix. [Spot Work]
- 9 or more act scenes per venue (SD stroll 9). Round 9b `cards/sex_for_pay.md`.
- A cap on how often (SD 6 a day). Round 9b `cards/sex_for_pay.md`.
- A climb that is more than more of the same (SD: take the corner, then run it). [Earnings and Spendings NewDay]
- SD's weak spot: the men never return. Give her a named regular. Round 9b `traces/sexpay_sd_stroll.md`.

## What players say
- *"there's a whore trait, but you cannot go whoring yourself on purpose. It's just random"* (CoT, mopoga#99537).
  Make it a chosen link at a place with hours.
- *"Still getting no payment for serving the gloryhole."* (CoT, mopoga#118229). CoT's gloryholes pay $0 in 38
  passages; SD shows the price before "Deal!".
- Three SD players asked where the brothel is: say where and when on screen.

## Our engine today (round 9b §6)
- Missing as a system: no client pool, venue or price formula. Composable from canvases, `block_pool` and money effects.
- A price from one stat is a stat-based value (`{type = "trait"}`, `setup.resolveEffectValue` (`v2.py:6846`)); a price from several stats is
  bands per sluttiness tier. The value is worked out when it applies, so the price on the label is authored.
