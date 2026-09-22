# The Balance — THE CHORES  `[READY]`

> **Signed and built, 2026-09-20. The money and the list came off 2026-09-23.**
> All nine are in the game, in their rooms, and none of them pays anything.
>
> **Two boxes are yours:** *Do I want this?* · *Does everyone belong?*
>
> **The rule this page is checked against:** every chore is in a room, at an hour, and costs her half
> an hour.
>
> Agreed in chat, 2026-09-19 and 20. What her mum's own hours offer is `people/her_mum_cards.md`.

---

## There is no list, and there is no money

**Standing rule, LO, 2026-09-23: *"Remove the Chores and payment / And fridge list. Chores are
simply available as it is."***

The chores are just there. She does each one in the room it happens in, in the hours it makes sense
in, and it costs her half an hour. Nobody dates one, nobody pays for one, and nothing counts how
many she has done.

## The nine chores

| chore | where | when |
|---|---|---|
| **Cook breakfast** | kitchen | seven on weekdays, eight on Sunday |
| **Breakfast dishes** | kitchen | after breakfast |
| **Cook lunch** | kitchen | twelve |
| **Lunch dishes** | kitchen | after lunch |
| **Cook dinner** | kitchen | six |
| **Dinner dishes** | kitchen | after dinner, about eight |
| **Laundry** | bathroom | once a day |
| **Bins** | the garage, then out to the street | once a day, in the morning |
| **Dusting** | front room | once a day |

The meal times are her mum's, from `people/her_mum.md`.

## What a chore costs

- **Half an hour.** That is the whole of it.
- **It pays nothing.** Not one of the nine, not the first one of the day, not ever.

**What that changes about the game:** chores used to be the floor under her money — about $35 a
week, small on purpose, there to stop the phone being a wall she got forced through. That floor is
gone. Until she has the cafe job she has **$10 and no way to earn**, and the first $150 Friday is
unpayable. Flagged, not fixed — it is the kind of thing the tips conversation settles.

## Who does them

- **Her mum** does whatever is left. Her hours are built around it.
- **Gil** does none of it, and never has.
- **Nate and Tasha** never do any.
- **The bins are only ever hers.**

## When her mum is doing one

Whatever her mum is working on, the player can:

1. **Help her.** They do it together. What she gets is time with her mum.
2. **Say "I'll do it."** She takes it over and her mum goes to sit down in the front room. That hour
   her mum spends sat down is the whole payment.
3. **Leave her to it.**

## When she does one alone

When her mum isn't on a chore, she can do it on her own — cooking included.

- **Cook breakfast** — Tuesday, Thursday, Saturday. Her mum is still on the ward.
- **Cook lunch** — Tuesday, Thursday, Saturday. Her mum is asleep.
- **Cook dinner** — Monday, Wednesday, Friday. Her mum is on the ward.
- **Dishes, laundry, dusting** — any hour her mum isn't on them.
- **Bins** — always.

**Dinner on a ward night.** If she cooks, there's dinner. If she doesn't, there's none, and nobody says
anything. *"Otherwise npcs ignore it."* On Friday she cooks, then hands Gil the $150 in the same
kitchen.

## Eating is not a chore

Eating is people at one table. That makes it a card — *sit down and eat with them* — the way the
opening already has *"Sit down and eat."* There is no hunger meter, so what eating gives her is the
people at the table.

## What it keeps track of

- **Done today**, one per chore. So a chore done once isn't there to do again that day.
- **It resets overnight.** Nothing here climbs, and nothing here counts.
- **`chore_paid_today` is gone**, along with the hour-instead-of-half-an-hour penalty a missed
  Friday used to put on every chore.

**Her mum's hours read it.** If the laundry is already done, or the player said *"I'll do it"*, her
mum's hour on it drops and she sits in the front room instead. The engine lets a schedule row depend
on a condition like this.

---

## What this page does not decide

Whether Gil says anything about chores that were skipped — *"Chores first"* stays as the house page
wrote it, and nothing enforces it yet · what her mum's card says (block 2) · who else sits down at
the table (round 3) · her using the tub herself — floated in chat, not agreed.

## The lines this page changes when it's built

Nothing below has been changed yet.

**On your pages:**

| where | the line now | what it becomes |
|---|---|---|
| `places/the_house.md:20` | the bathroom: *"the shower, and being clean enough to go live"* | the shower and the tub |
| `places/the_house.md:24` | the garage: *"the car, the bins, the laundry — where half the chores are"* | the car and the bins |
| `places/the_house.md:31` | *"Bins · laundry · dishes · the car."* | the nine chores above |
| `systems/the_house_day.md:59` | ward nights: *"no dinner, an empty evening"* | no dinner unless she cooks it |

**In the game:**

| where | what | what happens |
|---|---|---|
| `toml_phases/1_metadata_and_locations.toml:43` | the bathroom: *"The shower, the mirror, and a lock that works."* | the tub goes in |
| `toml_phases/1_metadata_and_locations.toml:51` | the kitchen: *"Bins, laundry, dishes, the car."* | the new list |
| `toml_phases/1_metadata_and_locations.toml:91` | the garage: *"the washing machine"* · *"Half the list on the fridge lives out here."* | both out |
| `toml_phases/3_activities.toml` | the `chore` scene, one button on the fridge | rebuilt from this page |
| `toml_phases/5_scenes.toml` | `gil_notices`, Gil in the doorway, which hangs off that button | moves with it |
| `toml_phases/2_one_shots.toml` | the opening's bins: *"Ten minutes"*, charged half an hour | matched to half an hour |
