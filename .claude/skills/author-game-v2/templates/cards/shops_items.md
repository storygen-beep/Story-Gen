# Card — Shops and items (a system)

> **A worked card, not a template.** Take the shape, leave the furniture. Every line cites a traced game:
> round 9b, `round9b/cards/shops_items.md` and `round9b/traces/shops_items.md`. The model is **Course of
> Temptation (CoT)**'s upgrade ladders; **In Her Own Hands (IHOH)** shows items as keys, **Cupid's Way (CW)**
> items that raise Looks. Fill your own card on `templates/sheets/system.md`; record it in `board.systems[]`.
>
> **A shop is a menu; the item is the system.** What matters is what the item changes after it leaves the
> shelf. Design the ladders and the keys; let the shop be a menu.

| field | the model (CoT) | cite |
|---|---|---|
| place and hours | 57 shops: vending machines, the dining hall, a department store with 10 departments, boutiques, sex shops, mail order; median shop 7 entries, the largest 338 | `cot_33_database_shop.js:2–2730` |
| cost | 119 dorm items, $0–3,200, median $80 (11 starter-job hours at $7); 8 are free, given by events | round 9b `traces/shops_items.md` §1 |
| one ladder or two | CoT: **two on one item that never touch** (the price rung and a separate `x` stream column). IHOH and CW: **one** — buying the item is the lewd step (IHOH), or one item raises Looks and corruption together (CW) | round 9b `cards/shops_items.md` |
| pay ladder | beds: 4 rungs, $300/600/1,200/2,400 for 110/120/130/140 Rest an hour, each double the price for +10; the top bed gives 2.9 hours a night back. Cameras: $60/200/600/1,500 for stream quality 40/80/140/200 | `cot_19_database_dormstuff.js:8–38`; `cot_62_shop.js:507–510`; `cot_45_streaming.js:75–84` |
| lewd ladder | the DSLRs carry an `x` column (180, 260): the best camera pays most on the explicit stream; 77 sex-toy stock entries. IHOH: toys at $20–50 open masturbation menus and cam shows | [StreamingWidgets]; [BR_MasturbateChoices]; [Cam_StartShow] |
| people | 43 items are `gift: true` and go to NPCs; clerks are generic. IHOH: the arc person who asks for the item | round 9b `traces/shops_items.md` §1 |
| pool, daily | not a scene pool: 1,794 stock entries; food rotates by weekday | round 9b `traces/shops_items.md` §1 |
| memory | `$dormbed`, the dorm inventory, `$miscinventory`. IHOH: 32 `$inv` keys | `cot_62_shop.js:507–510`; round 9b `traces/shops_items.md` §2 |
| growth | upgrades replace (beds trade in); food and consumables are used up | round 9b `cards/shops_items.md` |
| sink and deadline | **sink:** the shelf itself (the bed ladder is $4,500). **deadline:** the weekly bill: with back debt the shop refuses all but food, outfits and underwear | [ShopItem] |
| feeds · reads | 53 of 119 items (44.5%) put a number into another system that the code reads (sleep, stream quality, travel, art, relaxation); only 7 (6%) are pure flavor. The bicycle cuts a campus move from 3 to 2 minutes and switches 16 event-pool entries · reads money and back debt | `cot_65_storyfunc.js:3050–3056`; round 9b `traces/shops_items.md` §1 |
| link into the hook | camera to the X stream pay; toys to sex scenes; gifts to people | [StreamingWidgets] |
| leads to | the explicit stream, her masturbation and cam scenes, the person who gets the gift | [Cam_StartShow] |

## Measured floors (directions, never gates)
- An upgrade ladder has 4 rungs; price rises ×2 to ×3.3 per rung. Round 9b `cards/shops_items.md`.
- About 45% of items feed a number another system reads; 6% are decoration. Round 9b `traces/shops_items.md` §1.
- 7 items state an effect nothing reads (chairs and monitors list stream quality nobody adds up). State the
  effect on the item and make sure the system reads it. Round 9b `traces/shops_items.md` §1.
- IHOH toys cost under one shift ($60–115). Round 9b `cards/shops_items.md`.

## What players say
- Shops are a lostness system: 804 judged units, how-to 227, bug 97, complain only 20. Nobody asks for more
  items; they ask what an item does and where it is. Round 9b `cards/shops_items.md`.
- *"How can I buy the 8 in her dildo for Abby's quest"* (IHOH, mopoga#98370): the key is sold only while one
  text is pending and she wears a skirt. Don't hide a key behind a quest state and an outfit.

## Our engine today (round 9b §6)
- The clothing shop has prices (`v2.py:2209`, `var price = item.price || 0;`).
- A general `[[items]]` entry has no price (`template_import.py:1006-1010`: id, name, icon, max_stack); buying a
  bed or a camera is a hand-built choice with `costs` and `itemEffects`.
- Any condition can read an item (`v2.py:5096`), so an owned rung can gate another system.
