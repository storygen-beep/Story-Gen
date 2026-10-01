# Card — Reputation (meters until the gossip engine exists)

> **A worked card, not a template.** Take the shape, leave the furniture. Every line cites a traced game:
> round 9b, `round9b/cards/reputation.md` and `round9b/traces/reputation.md`. The models are **Course of
> Temptation (CoT)** (built from what each person saw) and **Shady Deals (SD)** (one score that buys titles,
> with heat pushing back). Fill your own card on `templates/sheets/system.md`; record it in `board.meters[]`,
> **never** `board.systems[]`.
>
> ⚠️ **Meters, not a system, until the engine's gossip piece (E9c) exists.** Until then reputation is one
> trait per audience, built from existing pieces: trait conditions, sidebar bands, `[[traits.labels]]`,
> daily-tick decay, and the cast page's `show_traits`. The table below is the target shape, not today's build.

| field | the model (CoT; SD where it differs) | cite |
|---|---|---|
| place and hours | everywhere: read wherever events fire (walks, parties, the bar, the social feed); rebuilt every night | `cot_68_time.js:1087` |
| cost | exposure: being seen naked or having sex in front of people. A mask blocks most of it (10 of 29 gated events need `not anonymous`). SD: titles cost 15–40 reputation a day | round 9b `traces/reputation.md` A.12; [The Code] |
| one ladder or two | CoT: **one** — no pay; the lewd ladder is the reputation ladder. SD: two (status tiers for pay, depravity for sex) that meet only at the Slut Boss title | round 9b `cards/reputation.md` |
| pay ladder | CoT none. SD: tiers Nobody → Crime Legend at 300 to 30,000; rewards ×1/×2/×3/×4 at 0/3k/7k/20k | [Character]; [Scales] |
| lewd ladder | Exhibitionism 175: rumors said to her face; 200: social-feed posts; 250: strangers ask her to flash, call her a slut; 400–500: slut posts, underwear theft. Promiscuity 100: groped at parties; 110: rumors; 150–175: called a slut; 200: threesome offers; 250: her number on a stall | [EventCampusRepRumor]; [EventQuadPartyCalledSlut]; round 9b `cards/reputation.md` |
| people | every NPC holds what they saw and heard; a rumor passes to friends (association ≥ 0.7) at ×10 strength; friends and lovers never spread | [EventCampusRepRumor] |
| pool, daily | 29 gated events (12 exhibitionism, 12 promiscuity, 3 studious, 1 kind, 1 mean) + 24 inline reads | round 9b `traces/reputation.md` A.8–9 |
| memory | per NPC: parts seen (in person, photo, video), sex acts, rumor strengths 0–1000; a global table of 7 types × 3 audiences (students, townies, faculty) | round 9b `traces/reputation.md` A.2–3 |
| growth | only grows; opposites cancel (promiscuity and reservedness, kindness and meanness); popularity drifts back after 14 days unmet; rumors never decay. SD: title drain, heat losses | round 9b `traces/reputation.md` A.6, A.11 |
| sink and deadline | not a money system. SD's counter-meter: heat 0–125; at 100 or more on a new day, one of 5 losses | [Player NewDay]; [Heat Widgets] |
| feeds · reads | feeds who approaches her and what they want: promiscuity reputation / 100 goes into each NPC's date and rival wishes · reads exposure and sex memories; shown as words ("pretty exhibitionist among the students"), never numbers | [Reputation]; round 9b `traces/reputation.md` A.7, A.10 |
| link into the hook | gates the random-encounter pool (9 gated campus-walk events) and NPC desire | round 9b `cards/reputation.md` |
| leads to | the stranger who asks her to flash, the party grope, the threesome offer | [EventQuadPartyCalledSlut] |

## Measured floors (directions, never gates)
- At least 2 lewd types (exposure, sex) × 2 audiences, so the same act on campus doesn't make her known in town.
  Round 9b `cards/reputation.md`.
- At least 4 rungs per type; CoT uses 11 distinct thresholds, 25–500, median 200. Round 9b `cards/reputation.md`.
- At least 3 events per rung; CoT's 29 over ~11 rungs is 2.6, thin. Round 9b `cards/reputation.md`.
- One spread rule (who tells whom) and one way to lower it (a mask, opposites, heat). Round 9b `cards/reputation.md`.

## What players say
- No risk: *"I can go out anywhere in the world and NOTHING happens to me"* (CoT, mopoga#183006/r2). Give it at
  least one loss path; SD's heat is the model.
- Fame should cross over: *"a fame Inclination since she is known at bar, live stream etc"* (CoT, mopoga#119006).
  CoT's reputation never reads stream popularity.

## Our engine today (round 9b §6)
- No reputation or audience primitive: "reputation" has 0 hits in `v2.py`. Build one player trait per audience by hand.
- `[[traits.labels]]` give a trait player-facing words (`template_import.py:541`), and the cast page shows the
  traits a person lists in `show_traits` (`template_import.py:168`).
