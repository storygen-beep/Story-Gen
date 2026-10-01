# Card — The wardrobe (states first, then items)

> **A worked card, not a template.** Take the shape, leave the furniture. Every line cites a traced game:
> round 9a, `round9a/ROUND9A_REPORT.md` §1b–§6 and `round9a/traces/` (`cot_wardrobe.md`, `ihoh_wardrobe.md`, `sd.md`
> §2, `cw.md` §3). Model: **In Her Own Hands (IHOH), states and the leave rules**; with **Course of Temptation
> (CoT), the miniskirt**, for dress codes, events and shop text, Shady Deals (SD) for the one number and the day-1
> gate, and Cupid's Way (CW), the office outfit, for a key garment and for what a thin wardrobe looks like.
>
> **The rules:** `references/engine.md` §17 (states, the catalog, dress codes, the gaps), `the-meters.md` W7 (read
> cheaply and often, gate only at doors that say why) and W3, `the-arc.md` A6 (key garments and their reminder),
> `register.md` "The truth rule" rule 5 (prose names her clothes only where a condition backs it).

| field | the model | cite |
|---|---|---|
| the unit | the **state**, not the item. IHOH reads naked 47 times, no bottom 38, no top 26, towel 20, skirt 18, no bra 14, no panties 14; 20 of its 31 items are read 0 times | `traces/ihoh_wardrobe.md`, the headline |
| leave the room | IHOH bedroom: no panties, underwear only or a towel need inhibition < 325; naked < 150. Apartment: no panties < 350, no bra < 400, naked never. CoT: Exhibitionism 0 with panties, 3 without, 5 wet and light | [BR_Leaving]; [LR_Locations]; CoT [Wardrobe] |
| the refusal says why | *"I can't leave the apartment without panties!"* (IHOH); *"You don't feel comfortable being this undressed here. (Need Exhibitionism N)"* and no Leave link (CoT) | [LR_Locations]; CoT [Wardrobe] |
| dress codes | CoT checks **coverage, not style**: town, campus and dorm codes, a pool that wants swimwear only; 78 of 126 location passages enforce one (61.9%). A breach blocks her and names the reason: *"You can't go out like this!"* | `traces/cot_wardrobe.md` §4; ROUND9A §2 |
| a place that wants revealing | IHOH's club: not in the dress, *"Aren't you going to get ready?"* with a link back to the wardrobe. CW's club door wants a dress. SD's stroll: *"You're not dressed slutty enough for the stroll."* | [ShaunClubLeaving]; CW [Club]; SD [Spot Work] |
| events from a state | CoT gates 184 of 1,710 events (10.8%) on clothing: malfunction 50, naked 28, underwear showing 25; a skirt puts 14 flip events in the pool 80% of the time. IHOH: a 1-in-5 wind gust on a walk in a skirt, exhibitionism +1. SD: sluttiness ≥ 10 opens 7 stranger events | `traces/cot_wardrobe.md` §6; [Walking]; `traces/sd.md` §2 |
| an event pays | CoT at work: *"Just keep cleaning"* (Exhibitionism 2/3) gives favor +2/+3, the raise currency. SD's limo stranger pays 300–600 × charm | [EventQuickieBurgerSkirtFlip]; `traces/sd.md` §2 |
| people notice | CoT's "daring" dialogue tag: 5 lines (friendly, shy, slut-shaming, chaste). IHOH's roommates in the kitchen: underwear only, *"Well, hello there"*; naked, *"Well, fuck, that's a view"*. SD's crew on her heels | `traces/cot_wardrobe.md` §9; [KBoysBase]; `traces/sd.md` §2 |
| one number | SD: each worn item adds stylishness and sluttiness; each stat gives +0 to +4 charm in bands at 7/14/21/28; at ≥ 10 she reads *"You may attract unwanted attention by dressing like that…"*. CW: looks feed a `hot` stage read by 97 conditions | `traces/sd.md` §2; `traces/cw.md` §3 |
| the day-1 gate | SD's gate of 10 is exactly the best score day-1 clothes from the cheapest shop can reach | `traces/sd.md` §2, design note |
| key garments | IHOH: the dress for Mr. Jones' Friday date, reminded in two rooms (*"I need to wear a dress for my date with Mr. Jones!"*); the gala gown has no reminder, so a player not in it gets a silent night. CoT: the black QuickieBurger uniform. CW: the office outfit, +15 looks and the office door | `traces/ihoh_wardrobe.md` §1 row 10; ROUND9A §1b; `traces/cw.md` §3 |
| the shop tells the rules | CoT: *"Significant chance of accidental upskirts. Easy access. Cool."*, *"Appropriate to wear at QuickieBurger (if solid black)."* SD: descriptor words per item (Trendy, Flirty) | `traces/cot_wardrobe.md` §1; `traces/sd.md` §2 |
| tiers over time | SD: T1 on day 1 ($80–450), T2 at reputation 5000 ($750–4,000), T3 at 20000 ($12,500–63,700). CW: purchase gates on corruption and looks | `traces/sd.md` §2 amounts; `traces/cw.md` §3 |
| taken away | CoT: clothes stolen in the shower start a 9-passage best-friend chain; laundry. SD: a failed robbery in the limo costs her heels | ROUND9A §1b; `traces/sd.md` §2 |
| sex scenes strip it | CoT's `[Makeout]` strips the real worn items | ROUND9A §1b |
| changing is cheap | CoT: one click for a favourite outfit, "yesterday's clothes". IHOH: 5 saved outfit sets | ROUND9A §5, class e |

## Steps in order
1. **Design the states, then the items.** Dressed, skirt, no bra, no panties, underwear only, towel, topless, naked.
   An item matters through the state it makes. In our engine a state is a `worn_exposure` value or a
   `clothing_slot` row (`engine.md` §17).
2. **Give each revealing state a daring price to leave**, and a refusal that says what is missing (IHOH, CoT).
3. **Put the states to work at places:** a dress code that refuses and says why, and a place that *wants* a
   revealing state. A refusal always offers the way out: change, or what to buy.
4. **Fire events from states**, and make each event pay: favor at work, exhibitionism, money (CoT, IHOH, SD).
5. **Let people notice:** one line per state worth noticing, in a `[group]` on that state (CoT, IHOH, SD).
6. **Feed one number other systems read**, and set its first gate at what day-1 clothes reach (SD).
7. **Make a few garments keys to an arc, and remind her before the key is needed** (IHOH's date dress; its
   gown is the failure).
8. **Tell the rules in the shop:** where an item counts and what it risks (CoT).
9. **Open tiers over time** by money or reputation (SD, CW).
10. **Let the world take clothes away** (CoT, SD). Ours: `wardrobeEffects` `unequip` and `remove`.
11. **Keep changing cheap:** 1–2 clicks (CoT, IHOH). Ours: one click per slot, or a saved outfit (`saved_outfits = true`).

## Amounts (directions, never gates)
- 4–6 states, each read in at least 3 places: a leave rule, a place, an event or a line (planned gate: `every
  clothing state is read three times`).
- At least one enforced dress code, and one place that wants a revealing state.
- One event per revealing state.
- One line per state worth noticing.
- One key garment per arc that uses clothes, with its reminder.
- Few items is fine if each one moves a state or the number. An item nothing reads is a defect; CoT carries 29%
  of those and IHOH 65%, and both are larger games that can afford it (ROUND9A §2, readers per item).

## Touchpoints per state or item
Buy (with the rule text) · wear · leave the room (the daring price) · place codes · events · lines · the number
it feeds · key use · taken away · sex scenes strip it.

## Chains (pick at least one per release)
- outfit → daring gate → event → exhibitionism → a lower gate (IHOH: inhibition falls → out braless → a park
  dare → exhibitionism rises → inhibition falls; the loop feeds itself).
- outfit → stat → paid event → money → better clothes (SD: item → sluttiness → stranger event → money).
- uniform → job → malfunction → favor → raise (CoT: skirt → 80% flip pool → flash at work → favor → $7 → $9 → $11).
- outfit → stream → viewers → tips (CoT, with the risk of a strike).
- key garment → the arc's night → pay (IHOH: Jasmynn's +$200 → buy the gown → wear it at the hour → the gala → $500).
- reputation → a call → a shop tier (SD: reputation 5000 → T2; 20000 → T3).

## First release
- Cheap clothes, **one number** (`worn_exposure`, with the states read through it), **one gate reachable on day 1
  with a notice**, **the leave rules**, **one event**, **one line** (SD v0.2.0's shape; `the-first-hour.md`).
- Grow by adding readers, not items: SD's log shows about 13 wardrobe entries over 20 versions, each a new reader
  (crew lines on heels, street attention, stroll pay, the bikers).

## Failure checklist
- [ ] Every block says why and offers the change (class a, 41 of 194 failures).
- [ ] Every declared state and key item is read in at least 3 places outside the wardrobe.
- [ ] A key garment is reminded before its window.
- [ ] The shop text says where an item counts.
- [ ] Changing takes 1–2 clicks (class e, 23 failures).
- [ ] Prose never names a garment she may not be wearing (`register.md`, the truth rule, rule 5).
- [ ] The wardrobe screen works on a phone screen (class h, 15 failures).

## What players say
- A gate that does not say what it wants: *"It keeps saying I have to be in uniform, so I get into the swim uniform
  though then can't leave the locker room"* (CoT, mopoga#161067, +5).
- Clothes nobody reads: *"Why does this matter when you never get to actually SEE what you're wearing?"* (CoT,
  mopoga#66525, +11); *"What do we do with the underwear collection?"* (CoT, mopoga#142638, +2).
- Too many clicks: *"wish there was an option to put random clothing items together into an outfit"* (CoT,
  mopoga#101477, +5).
- A small screen: *"Can't access wardrobe in beginning of game I'm on iPhone what I do?"* (CW, mopoga#75373, +9).

## Our engine today (round 9a §8; `references/engine.md` §17)
- States: `worn_exposure` (0/1/2, reads an empty slot) and `clothing_slot`; one `type` per item for `worn_type`;
  7 fixed slots. No tag list, so a garment cannot be both "skirt" and "wet".
- The price to put a garment on: its `conditions`. There is no "leave the room" hook: a price to go out in a state
  lives in each destination's `entry_conditions`.
- A dress code (`clothing_rules`) checks coverage and offers "Change clothes", from anywhere unless
  `wardrobe_anywhere = false`. A place that wants a revealing state (`entry_conditions` with `worn_*`) offers
  "Go back", plus "Change clothes" with `wardrobe_change_on_refusal = true`.
- Events from states: `worn_*` on a canvas trigger, with `trigger_mode = "random"`. No per-item malfunction chance.
- Lines: a `[group]` band on a `worn_*` condition.
- The number: `worn_exposure`; `worn_beauty` and `worn_corruption` are readable, but pay cannot be computed from them.
- Key garments: `clothing_item` conditions; the reminder is a hand-written band (a hub line, a quest card).
- `wardrobeEffects` add, equip, unequip and remove. One wardrobe room (planned: more than one
  wardrobe room). Saved outfits behind `saved_outfits = true`.
- The shop groups by corruption tiers, shows no "approved for" text, and there is one shop (planned: item
  prices and a general shop).
