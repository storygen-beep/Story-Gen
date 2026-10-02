# Card — Reputation (meters until the gossip engine exists)

> **A worked card, not a template.** Take the shape, leave the furniture. Every line cites a traced game:
> round 10, `round10/cards/gossip.md`, `round10/traces/cot_gossip.md` and `round10/traces/cot_reads.md` (CoT read in
> code), with `round10/traces/sd.md` for the door. The model is **Course of Temptation (CoT)**: each person remembers
> what he saw her do, and tells it in a scene she is in. **Shady Deals (SD)** is the model for the door a bad name
> closes. Fill your own card on `templates/sheets/system.md`; record it in `board.meters[]`, **never**
> `board.systems[]`.
>
> ⚠️ **Meters, not a system, until the gossip engine exists.** What our engine lacks is **memory of who saw
> what**, not a background spread: CoT has none either. Today's build is two pieces, both existing:
> **one trait for the audience** (the score) **plus one NPC-scoped flag per thing a person saw** (the memory).
> "Our engine today", below, shows both.

## What it is, in one paragraph
Each person remembers what he personally saw her do, or did with her. One who saw it, and doesn't like her, says
it out loud in a scene **she is in**; the people around him now know a weaker version. That is the only spread:
**one hop, in her scenes**, never off-screen, and a rumour heard second-hand is never retold. Her friends and lovers
never tell, and shut the teller down. The audience's score is the share of that audience who knows. It opens
strangers' offers, insults and feed posts, and one refusal. Nothing fades.

| field | the model (CoT; SD where it differs) | cite |
|---|---|---|
| place and hours | **written** wherever she is seen: everyone at the place is a witness. **Spread** only in 4 social hubs she is at: the campus walk, the classroom, the quad party, the River Rat bar | `cot_40_events.js:1384`; `traces/cot_gossip.md` §3 |
| cost | being seen. With a mask, strangers keep **no memory at all** (only people who already know her do), and 10 of 29 gated events also need no mask. A spread scene costs her humiliation, and friendship with every hearer (−15) and the teller (−25) | `cot_40_events.js:1540-1543`, `:181`; `traces/cot_gossip.md` §3 |
| one ladder or two | one lewd ladder, no pay. SD: one global score that prices the world (bribes, gig pay), plus four faction heats | `cards/gossip.md`; `traces/sd.md` |
| lewd ladder | exhibitionism rungs 50 / 175 / 200 / 250 / 500; promiscuity 100 / 110 / 125 / 150 / 175 / 200 / 250 / 400 — "per mille of the audience who knows". At 250 a student on the walk asks her to flash; at 100 she is groped at the party, at 200 offered a threesome, at 250 her number is on a stall wall; at 400–500 the feed calls her a slut | `cot_40_events.js:102-103`; `traces/cot_reads.md` |
| people | **witnesses**: everyone present. **Tellers**: someone with first-hand memory who isn't her friend or lover. **Hearers**, by passage: the teller's close friends present (3 of 6 spread passages), one student, or a quarter of the people present who dislike her. **Defenders**: her friends, lovers and would-be dates tell the teller off and don't take it in | `cot_53_people.js:3057-3077`; `traces/cot_gossip.md` §3 |
| pool | 6 spread passages. Reads: 29 gated events (12 exhibitionism, 12 promiscuity, 3 studious, 1 kind, 1 mean) and 27 inline reads; 6 entries read **one person's own knowledge** ("I saw her naked"); 1 refusal | `traces/cot_reads.md` §1 |
| memory | per person: what he saw (in person, photo, video), sex acts with her, and heard rumours as a bare strength per kind (0–1000). No time, place or source; a heard rumour loses the act | `cot_40_events.js:1708-1755`; `cot_53_people.js:5215-5255` |
| growth, way down | rises when a person sees her, sleeps with her or hears. **No decay** — the fantasy is that it sticks. Down only by opposite acts (refusing a flash writes reservedness) and friends defending her | `cot_53_people.js:5243-5252` |
| the refusal | *"You sleep around too much for my liking"*: a Chaste man turns down a date at promiscuity ≥500 — **waived by closeness** (friendship ≥1000, lust ≥800 or romance ≥600) | `cot_53_people.js:2133-2155` |
| the door | SD: a faction's heat at ≥80 shuts its place — *"Word is, you ain't welcome here"* — and she gets back in with a bribe, or charm and sex for a cheaper one. A setback, never a dead end | `traces/sd.md` |
| feeds · reads | every person's liking for her reads **his own audience's** promiscuity, kindness and meanness. The player sees words, per audience ("pretty exhibitionist among the students"), and in scenes the act said aloud | `cot_53_people.js:1767-1829`, `:5118-5188` |
| leads to | flash request → she flashes → more witnesses → more spread scenes → the slut posts. The loop feeds itself | `traces/cot_gossip.md` §1 |

## The size of one person (the dial)
The score is a plain average, so the audience size sets the speed. CoT has 180+ students: one who saw her topless
moves the score ≈ +2.8. **Our casts are 5–30 people**, so the same sum jumps 30–200 points per person. Give the
audience **an unnamed crowd**: the named people are part of it, a one-person scene moves the score a little, and
a crowd scene (the party, the bar) moves it a lot. HAND/HEURISTIC, `cards/gossip.md`.

## The minimum (measured; directions, never gates)
- **2 kinds: exposure and sex.** CoT's two lewd kinds hold 24 of its 29 gated events. A kind nothing reads
  shouldn't exist (CoT writes `troublemaking` 4 times and never reads it).
- **1 audience to start, with its unnamed crowd.** CoT's events and passages read only the students; townies and
  faculty reach play only through the tab. Add a second audience in a later release, when a second place has its
  own reads.
- **≥4 rungs per kind** (CoT: 5 and 8).
- **≥2 reads per rung**: at least one offer, and one line that names what she did. CoT has ≈1.8 — the floor
  is a direction, above the model.
- **≥3 spread scenes in ≥2 hubs** (CoT: 6 in 4).
- **≥2 reads of one person's own knowledge**: a man says the exact act; a man asks because he heard.
- **1 refusal, waived by closeness.**
- **1 door it can close, with a way back** (SD's heat): lie low, earn trust or pay. A setback, never a dead end.
- **1 way down**, and **friends who won't spread it**.
- **No decay.** Say so on the card.
- **No price effects yet**: item prices exist, but a price is a fixed number and can't read a stat yet. Pay
  can already read it (a value worked out from her stats, `references/engine.md` §3).

The smallest version that feels alive: she is seen → the people who saw remember that act → one of them who
doesn't like her says it in a hub while she's there → his friends know, hers refuse to → a word on her status page
moves → by the next rung strangers act on it, and one man who heard says it to her face.

## What players say
- No risk: *"I can go out anywhere in the world and NOTHING happens to me"* (CoT, mopoga#183006/r2). CoT's reads
  only add encounters. Keep the refusal, the door, and one cost scene per rung.
- They barely see it: 2 of 26 matching CoT comments are about reputation, one asking for a "gossip column"
  (mopoga#183006). Surface it: name the teller, what he told, and who heard.
- Fame should cross over: *"a fame Inclination since she is known at bar, live stream etc"* (CoT, mopoga#119006).

## Our engine today
No gossip piece: nothing stores "who saw what" for the audience, and nothing spreads. Build both halves by hand:
- **The memory: an NPC-scoped flag per thing a person saw.** The scene she is seen in sets it on each named
  witness — `flagEffects = [ { targetType = "npc", npcId = "npc_jake", flag = "saw_topless" } ]` (written by
  `applyFlagEffect`, `v2.py:7199`) — and his line is gated on it:
  `{ type = "flag", subject = "npc", npc_id = "npc_jake", flag_key = "saw_topless", operator = "is_true" }`
  (`v2.py:4972`). A spread scene sets `heard_topless` on the hearers present the same way, and adds to the score.
- **The score: one player trait for the audience**, with words through `[[traits.labels]]` and a banded sidebar
  item (`references/engine.md` §30), and on the cast page through `show_traits` (`template_import.py:168`). Size
  each write by who saw: a one-person scene adds a little, a crowd scene a lot. Give it no `trait_decay`.
- **The teller and the defenders are conditions**: the spread scene needs a teller whose flag is set and whose
  closeness to her is low; a friend present gets a line that shuts him down, and is never given the flag to pass.
- **The refusal and the door are a closeness check and a score check**: the score above a rung and his closeness
  below a line refuses; a place's entry or a person's yes is gated on the score below a line, with a way back
  (a `costs` payment, a lie-low scene that lowers it).
