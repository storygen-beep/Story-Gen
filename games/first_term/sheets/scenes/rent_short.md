# [REVIEW] Scene — rent_short_1, rent_short_2, rent_short_3

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign. the three read `rent_short`, not `rent_carried`; the fee's key; "Next week."; want, next step and hook rows. file and line cites cut.

> **New 2026-11-01, signed by LO 2026-11-01 ("Continue")** (DECISIONS 99–120). From the signed rent system (`sheets/systems/money_pressure.md`, "What a short Sunday costs").
> Three Sunday-morning canvases at the kitchen table, before or as part of Mark's count. No explicit screen; the lines are mine.

| row | answer |
|---|---|
| system · place | the rent · `home_kitchen`, Sunday 08:00–12:00, Mark at the table |
| order | each plays **before** `mark_sunday_table` that morning (higher priority), then hands to it |
| reads | `rent_short_weeks` (the engine's count, DECISIONS 112) and `rent_short` (set every short Sunday, cleared by a full payment; read within 12 hours; DECISIONS 144) |
| want | Mark's: the money, and her key, her fee, her clothes as the price |
| next step | a third short week takes a garment each week |
| hook | Vance at the door after a short Sunday |
| no sex for money | what a short week buys is pressure, not an offer |

## `rent_short_1` · the key (`rent_short_weeks` eq 1 · `rent_short`) · once

| node | what happens | exits | effects |
|---|---|---|---|
| `key` | Mark: "Then it's owed. Vance doesn't wait, so I don't." He holds his hand out for her bedroom key | "Here." → the kitchen | `her_door_unlocked` set · Mark's Power add +5 |

Lines: "Mark doesn't count it twice. He counts it once, and it's short, and he puts the envelope down." · Mark: "Then it's owed. Vance doesn't wait, so I don't." · "He holds out his hand, palm up." · Mark: "Your door key. You get it back when you're square." · *(thought)* "Anyone can open your door now. Anyone in this house."

## `rent_short_2` · the late fee (`rent_short_weeks` eq 2 · `rent_short`) · once

| node | what happens | exits | effects |
|---|---|---|---|
| `fee` | Mark at the table: Vance is coming tonight, and Vance charges late | "How much?" → the kitchen | `rent_late_fee` add +15 · Mark's Power add +5 |

Lines: Mark: "Twice now. Vance comes round tonight, and Vance charges late. Fifteen." · "He writes it on the envelope under the rest, in pencil, and underlines it." · Mark: "That's yours, not mine." · The knock that evening is the built `vance_knock` (its Power +10 stays); Vance says the fee to her face: "Fifteen on top, Miss. That's how it works." (`npc_vance.md` calls her "Miss").

## `rent_short_3` · the garage (`rent_short_weeks` gte 3 · `rent_short`) · each short week

| node | what happens | exits | effects |
|---|---|---|---|
| `take` | Mark names the first she owns of the skirt, the sheer blouse, the sports bra (that order), and takes it to the garage | "That's mine." → the kitchen · "Next week." when she owns none of the three, or all are held (his Power +5) | `garage_holds_<item>` set · that garment unequipped and locked in her wardrobe (🔒); if she had it on, she changes into her plain one (jeans, T-shirt, plain bra; pass 4 reader) · Mark's Power add +5 |

Lines: Mark: "Three times." · "He doesn't shout. He gets up, goes down the hall, and comes back with the <item> over his arm. The one you bought." (worn: "He holds his hand out across the table for the <item> you've got on, and waits until you go and change and put it in his hand. The one you bought.") · Mark: "Garage. On the table, then you get it back." · "Through the kitchen window you watch him hang it on the nail by his workbench, where you'll see it every time you walk past." · In her wardrobe, the item shows 🔒 with "In the garage. (Pay what you owe.)"

## Paying it back (the count, any Sunday)

When `owed` reaches 0 at Mark's count: the key comes back first (`her_door_unlocked` false; Mark: "Key." and he slides it across the table), then each held item (`garage_holds_<item>` false; "It's on the nail. Take it."). The streak starts that Sunday.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the three costs, their order, the pays, paying it back | `money_pressure.md` (signed 2026-11-01) |
| the hold mechanism | the engine: a garment's conditions lock it, and the wardrobe shows the 🔒 (DECISIONS 112) |
| the lines, the wardrobe lock text | mine, confirmed by LO 2026-11-01 ("Continue") |
