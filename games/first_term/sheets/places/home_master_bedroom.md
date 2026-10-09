# [READY] Place — Master Bedroom

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08 against the system sheets. Id `home_master_bedroom`.

| row | answer |
|---|---|
| kind | destination |
| ENTERED FROM (S2) | home_hall |
| labels — what kind of place | `zone:home`, `private`, `has_mirror` |
| hours | always |
| closed text | none: always open |
| hidden until | no |
| fill — word budget (S3) | 4,000 words (ledger, unchanged) |
| door | yes: Laura or Mark answers · "Knock" · "Go in" when both are out |
| dress code or wanted state | none |

## On entering

| auto-fires | who is here, and when | things to do alone | ways out |
|---|---|---|---|
| Laura C 1, Tuesday evening, day 2 (from the kitchen) | Laura: nights 22:00–07:00 · Saturday 17:00–18:30, dressing | go through Laura's wardrobe while they're out | the hall |
|  | Mark: nights 02:00–07:00 · Saturday 22:00–00:00 | the mirror |  |

## Rows (`serves`)

| row | kind | system | cost and effect, with op (S4) | BRAKE (S9) | on a screen? |
|---|---|---|---|---|---|
| Laura, dressing | person | Laura's ladder | Laura C 6 here, Saturday | Saturday only | yes |
| Laura's wardrobe | work | wardrobe | try on her things · `laura_blue_dress` read | once a day, when both are out | yes: her body in Laura's mirror |
| ease the door open | person | Laura's and Mark's ladders | none · one line naming who is asleep, then back to the hall | night, when everyone inside is asleep | yes, one line |

## Who is in here, and what the door offers (LO's play note, 2026-10-08)

**Every person in here in a window has a face, and a line names only who is actually here.**

| window | who is here | the door offers | faces |
|---|---|---|---|
| Sun–Fri 22:00–00:00 · Mon–Sat 00:00–02:00 | Laura, asleep · Mark is downstairs | "Ease the door open" (question 58) | Laura, asleep |
| Sun 00:00–02:00 (Saturday night) · every day 02:00–06:30 · Sat, Sun 06:30–07:00 | Laura and Mark, asleep | "Ease the door open" | Laura, asleep · Mark, asleep |
| Mon–Fri 06:30–07:00 | Mark, asleep · Laura is at breakfast | "Ease the door open" | Mark, asleep |
| Sat 17:00–18:30 | Laura, dressing | "Knock" | Laura |
| Sat 22:00–00:00 | Mark, asleep · Laura is waiting up downstairs | "Ease the door open" | Mark, asleep |
| any other hour | nobody | "Go in" | — |

- **No knock on a sleeping room.** When everyone inside is asleep, the door shows "Ease the door open"
  instead of "Knock".
- **Ease the door open:** one screen, the room in the dark. The line names who is asleep: "Laura's
  asleep on her side. Mark's half of the bed is empty." Then back to the hall. Nothing else in 0.1;
  what she does at the bedside waits for Hungry ("Needs Hungry").
- **When `came_home_late` is set,** Laura is on the stairs 23:00–02:00, not in bed (her first row wins). In
  those hours the room is empty, or Mark only after 02:00, and the lines say so.
- **"They're asleep"** (the old row) names only who is asleep, by the table above.

## Rows a gate needs

| row | gate |
|---|---|
| her wardrobe when they're out | a destination is never open and exit-only |
| a door with a way back | lint: a door opens onto something |

## Why — the source of each key choice

| key choice | source |
|---|---|
| their room, shared | `board.map.shared_homes` |
| Laura's wardrobe while they're out | LIVES §4 |
| the door | LO, 2026-10-08 |
| a face for each person here; no knock at night; ease the door open | LO's play note, 2026-10-08 · question 58 |
