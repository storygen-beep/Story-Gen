# [READY] System — wardrobe

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08 from SYSTEMS §7 and the ledger's `wardrobe` card.
> Every number marked "guess" is new here and waits for your yes.

| row | answer |
|---|---|
| id · name | `wardrobe` · The wardrobe |
| place and hours | `home_ella_room`, always · the clothes shop, Monday to Saturday 10:00–18:00 (guess) |
| cost | 1–2 clicks to change · shop clothes cost money, the price shown first |
| one ladder or two | one |
| people | Ryan, Mark, Laura, Zoe |
| pool | `wardrobe_event_stairs`, `wardrobe_event_dress_code` · `daily = true` |
| memory | what she owns: her clothes, three uniforms, Laura's and Zoe's dresses, the sports bra |
| growth | climbs |
| sink and deadline | the clothes shop · no due day |
| feeds | Exhibitionism, `complaints` |
| reads | Exhibitionism, Corruption |
| what drives it (S8) | her clothing state, and Exhibitionism for leaving a room in it |
| link into the hook | at home, Ryan, Mark and Laura each react, by their numbers |
| leads to | Ryan, Laura |
| day 1 | yes |
| BRAKE (S9) | changing writes nothing, so none · each event once a day, on its trigger |

College clothes are her own outfits at three levels: normal, sexy, slutty. Never a "college uniform".

## The seven states

| state | how the game checks it | leaving a room in it needs | readers, planned (3+ each) |
|---|---|---|---|
| covered | nothing showing | nothing | the default line everywhere |
| short skirt | a short skirt on | Daring: Exhibitionism 20 | the stairs event, Zoe's door, Mark's eyes |
| no bra | the bra slot empty | Daring: Exhibitionism 20 | the class risky slot, the park run, Ryan's line |
| no panties | the underwear slot empty | Showing: Exhibitionism 40 | the stairs, the class slot, Mark's table |
| underwear only | underwear, nothing over it | Showing 40, and only at home | Ryan's line, Mark's line, Laura's line |
| towel | a towel on | allowed at home from day 1 | the hall (Ryan A 1), the bathroom, Laura's line |
| naked | nothing on | her room and the bathroom only; outside is Watched, later | the bathroom, her room, the selfie (later) |

**One exception (LO, 2026-10-08):** Hale B 2's flash, no panties at Daring, inside that step only.

The door out says why: *"Not like this. Not yet."* (guess) The block names the stage it needs.

## Key items

| item | how she gets it | readers, planned (3+ each) |
|---|---|---|
| `cafe_uniform_normal` | Tom gives it with the job | the café's dress rule · tips rung 1 · Tom's line |
| `cafe_uniform_sexy` | Tom B 2 sets `uniform_sexy` | tips rung 2 · Gary · Mark's "where's a waitress get twenties?" |
| `cafe_uniform_slutty` | after 0.1 | not a key item until its release (LO, 2026-10-08) |
| `laura_blue_dress` | Laura C 1, day 2 | Laura's line · Mark's eyes · Ryan's line |
| `zoe_party_dress` | Zoe A 1, borrowed | the party door · Jake · Laura on the stairs |
| `sports_bra` | the clothes shop, $25 (guess) | the park run · Ryan's line · Laura's line (guess) |

## Where the world asks for clothes

| place | what it asks | if she doesn't have it |
|---|---|---|
| the café | the uniform | *"Uniform, @player."* She changes in the back. |
| Zoe's party | something short | Zoe lends her dress |
| figure drawing | nothing for her; the model is nude | none |
| any class | nothing locks her out | a lecturer's warning; again, a complaint to the dean |

## Pool (`pool[]`)

| canvas | what it is | explicit? | what drives it | brake |
|---|---|---|---|---|
| `wardrobe_event_stairs` | a short skirt or no panties on the stairs; someone below | no | her clothing state · who is home | once a day |
| `wardrobe_event_dress_code` | a lecturer's warning in class | no | her clothing state | once a day |

Both events add Exhibitionism +1 the first time each day she is in that state (guess).

## Lewd ladder (`lewd_ladder[]`)

| rung | gate | acts |
|---|---|---|
| 1 · Covered | none | covered · a towel in the hall (Ryan A 1) |
| 2 · Daring | Exhibitionism gte 20 | a short skirt · no bra |
| 3 · Showing | Exhibitionism gte 40 | no panties · underwear only at home |
| 4 · Watched | later; the button says "Needs Watched" | naked by choice outside her room · the slutty uniform |

## The meters it writes and reads (`board.meters[]`)

| meter id | kind | key | fed at | read by |
|---|---|---|---|---|
| exhibitionism | sourced | `exhibitionism` | her room, among others | leaving a room · the uniforms · the selfies |
| complaints | sourced | `complaints` | `lecture_hall` | the dean: the warning, then the letter |
| money | ambient | `money` | `cafe` | the clothes shop's prices |

## Rows a gate needs

| row | gate |
|---|---|
| every state and item read three times | every clothing state is read three times (blocks a ship) |
| a line about her clothes checks she wears them | her clothes are backed (blocks a ship) |
| the sports bra sold with a price | a declared garment can be got · a price is on its label |
| the shop's items are read somewhere | what money buys opens a door |
| the wardrobe changes lines | the wardrobe is read |

## On the phone: the selfie and the feed (LO's play note, 2026-10-08)

The selfie and the feed live on the phone only; no room has a row that copies them.

| row | where | cost and effect, with op (S4) | BRAKE (S9) |
|---|---|---|---|
| "Post a selfie" | the phone, anywhere | Covered: `gate_trait` exhibitionism, min 0 · `followers` add +3 to +8 | once a day (the engine's daily cap) |
| "Post one in your bra" | the phone, anywhere | Daring: exhibitionism 20 or more · `followers` add +10 to +25 | once a day |
| "Post one topless" | the phone, anywhere | Showing: exhibitionism 40 or more · `followers` add +40 to +90 | once a day |

The engine gates a post only on one meter, not on what she wears or where she is, so each label names
the act, and a locked rung shows as "🔒 Post one in your bra" until she reaches the stage. A post moves
only `followers`.
| the feed | the phone | reads `followers` and, behind the flag that makes each true, posts about her (a party post only after `party_went`) | none needed: it writes nothing |

## A garment reaction is a line in a hub (LO's play note, 2026-10-08)

A person's line about what she wears ("his line: short skirt") is a line inside that person's existing
hub, read by her clothes, never its own button. It is true where it shows: a line that names another
person, a place or a time shows only in the hub where that holds (Laura's towel line differs between
the kitchen and the stairs; Jake's "tonight" line only at the door after a date).

## Why — the source of each key choice

| key choice | source |
|---|---|
| seven states | LO, chat (SYSTEMS §7) |
| no "college uniform"; three levels of her own | LO, chat (SYSTEMS §7) |
| leaving a room needs Exhibitionism | `templates/cards/wardrobe.md` · SYSTEMS §7 |
| the dress code never locks her out of class | LO, chat (SYSTEMS §7) |
| `sports_bra` | LO, 2026-10-08 (SYSTEMS §14) |
| which stage each state needs | guess, from SP2's heat table |
| shop hours, the bra's price | guess |
| the refusal line | guess |
| the feed and the selfie live on the phone only | LO's play note, 2026-10-08 (sweep A1-34, K6) |
| the selfie rungs gate on Exhibitionism, labels name the act | LO, 2026-10-08 (the engine reads only one meter for a post) |
