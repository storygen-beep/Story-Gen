# craft/clothes.md — her clothes, dressing, and who notices

Read this before you write a card that dresses her, gives or sells her a garment, gates a door or a button on what she wears, or has someone notice her clothes. Checked against Course of Temptation (CoT) mostly, and the top games (LO, relayed 2026-11-23: "Yes" to the example below, with one change to A). A moment where she's undressing or dressing is also a body moment: `craft/body-moments.md`. The shop's screen is `craft/places.md`; its prices are `craft/economy.md`.

## Must read

The card's `Craft:` line cites each one, or says in one line why it skips it. `when` and `judge` are the labels in `SKILL.md`, "Rule labels".

| id | what it asks | the failure it stops | when | judge |
|---|---|---|---|---|
| C719 | a button does something: no "get dressed" that moves no garment | first_term_lean's "Back in your room, dressed" | she dresses or undresses | reader |
| C1158 | the clothes the prose names are backed by a condition, an earlier equip, or the beat that equips her; undressing in an act is backed by the act | the opening's dressing line failed this row and passed rule 4 (P13 reader pass 8) | a garment is named | reader + sheet |
| C1206 | prose never names a garment she may not be wearing | — · kept blocking: the truth rule | a garment is named | reader + sheet |
| C1166 | the opening arms the wardrobe, with the outfit choice on the screen where she dresses | — · kept blocking: LO's choice (2026-11-23) | the opening | reader |
| C1167 | release 1's minimum: one number the world reads, one gate with a notice, leave rules, one event, one line where a person notices | — | the plan | note |
| C1204 | release 1: cheap clothes, one number, one gate on day 1, the leave rules, one event, one line | — | the plan | note |
| C1183 | the unit is the state, not the item: design states first, then items | — | the plan | note |
| C1171 | each clothing state and key item is read in 3+ places | — | the plan | note |
| C1169 | a clothing read is armed only if something she can get satisfies it | — | the plan | note + reach |
| C1150 | every garment has a way into the wardrobe: initial, a shop price over 0, or `wardrobeEffects` | — | the plan | note |
| C1201 | few items is fine if each moves a state; an item nothing reads is a defect | — | the plan | note |
| C1173 | clothing doors are few and loud: gate at the door, say why at the door, offer the change | — | a place is entered | note |
| C1184 | the refusal says what's missing, in her voice | — | a place is entered | note |
| C1198 | a refusal always offers the way out: change, or what to buy | — | a place is entered | note |
| C1185 | a dress code checks coverage, not style | — | a place is entered | note |
| C1220 | a dress code's breach plays ClothingBlock: "Go back", plus "Change clothes" only where she can change | first_term_lean P07: the front door showed only "Go back" | a place is entered | reader |
| C1221 | a dress-code exception names everything it allows, `dress` unequipped included | first_term's dress slipped through | a place is entered | reader + reach |
| C1177 | exposure is outfit plus place plus audience: bare in her bedroom is nothing, on the street it's the event | — | a garment is named | note |
| C1176 | clothing reads belong on streets and open places, not on sex scenes | — | something sexual shows | note |
| C1189 | people notice: one line per state worth noticing, in their own manner | — | a person is on screen | note |
| C1197 | changing is cheap: one or two clicks, whole outfits | — | she dresses or undresses | note |
| C1200 | place clothes only where the place's activity asks for them | — · kept blocking: LO's choice (2026-11-23) | a place is entered | reader |
| C1207 | the wardrobe screen works on a phone | — | she dresses or undresses | note |

## The engine (cited; `v2.py` is `apps/game_generation/twee_comprehensive/generators/v2.py`)

- **Seven slots:** bra, underwear, top, bottom, dress, legwear, shoes (`apps/projects/services/template_import.py:278`).
- **A garment goes on with `wardrobeEffects`** on a choice or an exit: `add`, `equip`, `unequip`, `remove`, plus `remember_outfit` / `restore_outfit` (v2.py:18219-18236). `equip` also adds it.
- **A dress takes the top and bottom off, and the other way round** (`setup.equipItem`, v2.py:1760-1766). An item whose own `conditions` fail doesn't go on, and nothing says so (v2.py:1757-1758). So an outfit choice equips every slot it names, and a card says which slots.
- **A dress code** is `clothing_rules` on the place she's going to; the first rule whose conditions hold decides (`setup.clothingCheckForLocation`, v2.py:2189-2200). A breach plays `ClothingBlock`: its message, then "Change clothes" and "Go back" (v2.py:21051-21078). With `wardrobe_anywhere = false`, "Change clothes" is wrapped in `<<if setup.canChangeClothesHere()>>` (v2.py:21003-21009), which is true only in a `wardrobe_location` room (v2.py:2234-2238). Away from her wardrobe, the block shows only "Go back". There is no leave-the-room hook, so a leave rule is the dress code on the place outside the door (C1223).
- **A button that needs certain clothes greys out with its reason.** Put `show_when_blocked = true` and `locked_text` on the trigger, beside `cooldown_message` (parsed at `apps/projects/services/template_import.py:2598`, carried at `apps/projects/services/game_graph.py:357`, emitted as `lockedText` at v2.py:15183-15185). When the clock alone shut the row, it greys with `cooldown_message` and its hours. When anything else shut it (clothes, money, a meter, a flag), it greys with `locked_text`, as text, not a link (v2.py:6689-6697). With no `locked_text` it stays hidden, and so does a row for a person who isn't there (v2.py:6685). It renders as "<name> — <locked_text>" (v2.py:6741-6748). Tests: `apps/game_generation/tests/test_blocked_row_hours.py`. (LO, 2026-11-23: "yes, do the engine fix".)
- **Settings:** `wardrobe_anywhere` (default on), `wardrobe_change_on_refusal`, `saved_outfits` (v2.py:1196-1198); `[ui] clothes_layout = "room"` (v2.py:1202, 12332-12339).
- **Conditions that read clothes:** `clothing_slot`, `clothing_item`, `worn_exposure`, `worn_type` (v2.py:9511, 9521, 9579, 9595).

## The measures

CoT, read 2026-11-23 (`/Users/a0000/Documents/Player_Legibility_Study_20260825/corpus/course-of-temptation/passages`):
- **Dressing in the opening.** `Prologue6c.txt`: "You go back to your room and look over your wardrobe, picking out something in your usual style." Then `<<pickstartingoutfit>>`, then "Once dressed, you head out the door". The widget (`PrologueWidgets.txt`, lines 6-18) is a short list of whole starting outfits, with "Default" already picked. It is not the full wardrobe.
- **Whole outfits, one click.** `Wardrobe.txt`: "You decide to change into your $pendingoutfit outfit." A garment that's gone is named: "You couldn't find … in your closet."
- **The leave rule, in her voice, naming the price.** "It would be daring to go out like this, but you feel too self-conscious. (Need Exhibitionism N)", in 5 files (`MainHall.txt`, line 107; also `GymShower.txt`, `GreekHouseWidgets.txt`, `RiversideMotelRoom.txt`). Leaving the shower: "Leave the shower like this? You've seen other students do it, but... you're not sure you have the confidence." (`ExitShower.txt`). A changing room: "You can't walk out of here like this." (`DressingRoom.txt`, line 5).
- **Someone can see her change.** `<<maybechangingwitnessedbyadmirer>>` runs inside the wardrobe (`Wardrobe.txt`); 3 files call it.
- **Dress checks** (`clothes_ok`) are in 30 passages.

Field-measured, from `lists/COVERAGE.md`'s evidence column and not re-run today: C1167 and C1204 (Shady Deals' first release), C1185 (CoT dress code in 78 of 126 places, a different count from today's 30 `clothes_ok` files: that row counts location passages with any dress logic), C1189 (CoT's daring lines; IHOH's roommates), C1197 (CoT; IHOH's 5 saved sets), C1201 (CoT 29% and IHOH 65% of items unread).

## The shape

Each rule is marked **measured** or **LO's choice**.

1. **States first, then items** (C1183, C1171). Name the states the world reads (dressed, in a dress, in underwear, in a towel), then give each one at least 3 readers: a door, a line, an event. Release 1 reads one number, `worn_exposure` (C1167, C1204). *Measured in the field.*
2. **Every garment has a way in** (C1150, C1169): what she owns at the start, a shop price over 0, or a `wardrobeEffects` on a button (borrowing from someone's room is an `add`). An item nothing reads is cut (C1201). *Measured in the field.*
3. **The opening dresses her.** Her usual clothes go on in the beat, by `wardrobeEffects`, and the screen offers a short list of 2–3 whole outfits to switch to. The full wardrobe stays in her bedroom (C1166, C719). *Measured:* CoT's `<<pickstartingoutfit>>` with "Default" picked; *LO's choice* for the list.
4. **Text names only what she's wearing** (C1158, C1206). The beat that equips her may name it; a later line names a garment only behind a clothing condition. *LO's rule* (the truth rule).
5. **Changing is cheap:** whole outfits, one or two clicks (C1197). *Measured:* CoT's "change into your … outfit".
6. **A leave rule is a dress code on the place outside the door** (C1173, C1185, C1220). It checks coverage. The refusal says what's missing in her voice and offers the way out: "Change clothes" or "Go back" (C1184, C1198). "Change clothes" shows only where she can change: everywhere by default, but with `wardrobe_anywhere = false` only in her `wardrobe_location` rooms (v2.py:21003-21009), so at a front door the way out is "Go back", and the line says where to change. An exception names everything it allows, `dress` unequipped included (C1221). *Measured:* CoT's "It would be daring to go out like this…"; the engine's ClothingBlock.
7. **A button that needs certain clothes says so, greyed on the room menu:** `show_when_blocked = true`, the clothes in its conditions, and a `locked_text` naming what's missing: "Needs leggings and a sports top" (C1200). It never just vanishes. *LO's choice.*
8. **People notice, one line each, where she's seen** (C1189, C1176, C1177): her street, the campus mirror, a housemate in the hall. The line belongs to the person and their manner. In release 1 it sets a flag only. *Measured in the field.*
9. **A garment of someone else's is theirs in the text.** Borrowed from Mom's wardrobe, it's still Mom's, and Mom can say so. *LO's choice* (first_term_lean's plan, Laura's wardrobe).

## Worked example

Roles: her mom; her bedroom; the hall. LO approved these words (relayed 2026-11-23: "Yes", with A's buttons changed to the short list). No meter moves.

**A · The dressing beat after the opening's shower** (one-time; 44 words). The exit from the bathroom equips her usual: plain bra, panties, jeans, T-shirt, sneakers.
> Back in your room, you shut the door and let the towel drop. The air's cold on your wet skin, and your nipples go tight. You pull a plain bra and panties from the drawer, then your jeans, a T-shirt and sneakers. Your usual.

Picture, right after the towel drops: *Her, 18, in a small bedroom, towel on the floor, stepping into jeans. still.* `_t4`, pool 1 (`craft/body-moments.md`).

Buttons: Go down to the kitchen (5 min) · Wear the sundress instead · Wear the leggings and sports top instead. Each "instead" equips every slot of that outfit, then goes down.

**B · Leaving the house without a top and a bottom, or a dress.** A dress code on her street.
> You're not going out like this. You need a top and a bottom, or a dress.

Buttons: Go back. (This game changes in her bedroom only, `wardrobe_anywhere = false`, so the front door has no "Change clothes"; v2.py:21003-21009.)

**C · A noticing line,** when she goes out in Mom's short skirt, once a day, while Mom's rows put her in the hall (15 words).
> Mom's eyes drop to the skirt. "Is that mine?" She doesn't wait for an answer.

Sets a flag only.

**D · The run, one click.** The room button "Go for a run (45 min)" needs her leggings and sports top. Without them it shows greyed: "Go for a run — Needs leggings and a sports top".

```toml
[canvases.trigger]
show_when_blocked = true
locked_text = "Needs leggings and a sports top"

[canvases.trigger.conditions]
version = "1.0"
logic = "AND"

[[canvases.trigger.conditions.items]]
type = "clothing_item"
item_id = "<leggings id>"
operator = "equipped"

[[canvases.trigger.conditions.items]]
type = "clothing_item"
item_id = "<sports top id>"
operator = "equipped"
```

`equipped` is the operator for "wearing it" (v2.py:5236-5243; also `unequipped`, `owned`, `not_owned`).

## Not this

- "Back in your room, dressed." A dressing that moves no garment (C719).
- A line about her skirt when she might be in jeans (C1158).
- "You can't go there." A refusal that doesn't say what's missing, or offers no way out (C1184, C1198).
- A room button gated on clothes that just vanishes. Give it `show_when_blocked` and a `locked_text` (rule 7).
- A garment she can't get, with a door that needs it (C1169).
- Ten garments nobody reads (C1201).
