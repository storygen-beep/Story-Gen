# [REVIEW] System — wardrobe

> Changed 2026-11-04 to match the build; waits for LO's re-sign. The hot tub's way out gives back what she came in; Laura's lace set is built.

> Changed 2026-11-04 (LO's answers Q7, Q11, Q12: the stairs event is the hall event; the tub strips and dresses her; Laura's black lace set is built). Waits for LO's re-sign.

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign. Key items: the sheer blouse needs Exhibitionism 15 (heat proposal C6); the sports bra is $25.

> **Changed 2026-11-01, re-signed by LO 2026-11-02** ("Signed, go ahead and build"; DECISIONS 124, the heat ladder a2): its gate or pay changes; the row is in `sheets/HEAT_LADDER_A2.md`.

> **Changed 2026-11-01, re-signed by LO 2026-11-01** ("Signed", DECISIONS 113; design DECISIONS 99–112): leaving a room now needs Corruption **or** Exhibitionism, wearing it out pays both, the two events pay by rule, and a bought item can be held in the garage. The rules live in `sheets/systems/meters.md` and `sheets/systems/money_pressure.md`.

> Changed 2026-11-04 to match the build; waits for LO's re-sign. The 2026-10-29 locked-button note (DECISIONS 90) is corrected: "Needs Corruption 60" and "Needs Exhibitionism 60" are no longer in the game, because the buttons for scenes this release does not write were removed (DECISIONS 132). Any line below that still names one is superseded by that row.

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
| what drives it | her clothing state, and Exhibitionism for leaving a room in it |
| link into the hook | at home, Ryan, Mark and Laura each react, by their numbers |
| leads to | Ryan, Laura |
| day 1 | yes |
| BRAKE | changing writes nothing, so none · each event once a day, on its trigger |

College clothes are her own outfits at three levels: normal, sexy, slutty. Never a "college uniform".

## The seven states

| state | how the game checks it | leaving a room in it needs | readers, planned (3+ each) |
|---|---|---|---|
| covered | nothing showing | nothing | the default line everywhere |
| short skirt | a short skirt on | Corruption 20 **or** Exhibitionism 20 (`meters.md` rule 1) | the hall event, Zoe's door, Mark's eyes |
| no bra | the bra slot empty | Corruption 20 **or** Exhibitionism 20 | the class risky slot, the park run, Ryan's line |
| no panties | the underwear slot empty | Corruption 40 **or** Exhibitionism 40 | the hall event, the class slot, Mark's table |
| underwear only | underwear, nothing over it | Showing 40, and only at home | Ryan's line, Mark's line, Laura's line |
| towel | a towel on | allowed at home from day 1 | the hall (Ryan A 1), the bathroom, Laura's line |
| naked | nothing on | her room and the bathroom only; outside is Watched, later | the bathroom, her room, the selfie (later) |

**One exception (LO, 2026-10-08):** Hale B 2's flash, no panties at Daring, inside that step only.

The door out says why and names both numbers: "Not in that skirt. Not yet. (Needs Corruption 20 or Exhibitionism 20.)" (`meters.md` rule 1).

**Wearing it out pays** (`meters.md` rule 2): the first day out in each level, Corruption +1 and Exhibitionism +1; each day after, Exhibitionism +1, once a day, through the street scene's witness.

**A held item** (`money_pressure.md`, the third short Sunday): `garage_holds_<item>` locks one bought garment (🔒) until the debt is paid.

## Key items

| item | how she gets it | readers, planned (3+ each) |
|---|---|---|
| `cafe_uniform_normal` | Tom gives it with the job | the café's dress rule · tips rung 1 · Tom's line |
| `cafe_uniform_sexy` | Tom B 2 sets `uniform_sexy` | tips rung 2 · Gary · Mark's "where's a waitress get twenties?" |
| `cafe_uniform_slutty` | after 0.1 | not a key item until its release (LO, 2026-10-08) |
| `laura_blue_dress` | Laura C 1, day 2 | Laura's line · Mark's eyes · Ryan's line |
| `zoe_party_dress` | Zoe A 1, borrowed | the party door · Jake · Laura waiting up in the dark hall |
| `sports_bra` | the clothes shop, $25 | the park run · Ryan's line · Laura's line (guess) |
| `thin_top` (sheer blouse) | the clothes shop, $20, from Exhibitionism 15 and while the garage doesn't hold it (C6 of `proposals/FIRST_TERM_HEAT_PROPOSAL_20261103.md`) | the scenes that read it worn |

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
| `wardrobe_event_stairs` ("Bend for your bag in the hall") | a short skirt or no panties in the hall; someone behind her | no | her clothing state · who is home | once a day |
| `wardrobe_event_dress_code` | a lecturer's warning in class | no | her clothing state | once a day |

Both events pay by `meters.md` rule 3 (no longer a guess): shown by her choice, Exhibitionism +1 and Corruption +1; an accident pays nothing.

## Lewd ladder (`lewd_ladder[]`)

| rung | gate | acts |
|---|---|---|
| 1 · Covered | none | covered · a towel in the hall (Ryan A 1) |
| 2 · Daring | Exhibitionism gte 20 | a short skirt · no bra |
| 3 · Showing | Exhibitionism gte 40 | no panties · underwear only at home |
| 4 · Watched | later; the button says "Needs Exhibitionism 60" | naked by choice outside her room · the slutty uniform |

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

| row | where | cost and effect, with op | BRAKE |
|---|---|---|---|
| "Post a selfie" | the phone, anywhere | Covered: `gate_trait` exhibitionism, min 0 · `followers` add +3 to +8 | once a day (the engine's daily cap) |
| "Post one in your bra" | the phone, anywhere | Daring: exhibitionism 20 or more · `followers` add +10 to +25 | once a day |
| "Post one topless" | the phone, anywhere | Showing: exhibitionism 40 or more · `followers` add +40 to +90 | once a day |

The engine gates a post only on one meter, not on what she wears or where she is, so each label names
the act, and a locked rung shows as "🔒 Post one in your bra" until she reaches the stage. A post moves
only `followers`.
| the feed | the phone | reads `followers` and, behind the flag that makes each true, posts about her (a party post only after `party_went`) | none needed: it writes nothing |

## A garment reaction is a line in a hub (LO's play note, 2026-10-08)

**Undressing with the scene** (LO, 2026-11-04, Q11): the hot tub's "Strip and get in." takes her clothes off, and every way out gives back what she came in (`remember_outfit`, `restore_outfit`, LO, 2026-11-04). **Laura's black lace bra and panties** are wardrobe items, put on and taken off by Mark's lingerie walk-in (Q12): built.

A person's line about what she wears ("his line: short skirt") is a line inside that person's existing
hub, read by her clothes, never its own button. It is true where it shows: a line that names another
person, a place or a time shows only in the hub where that holds (Laura's towel line differs between
the kitchen and the hall; Jake's "tonight" line only at the door after a date).

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
