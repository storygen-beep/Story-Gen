# [READY] Place — Home (the house, a building)

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> New 2026-10-08, from LO's play note: "Home" is a building, so the street shows "Home" and inside it
> shows the rooms. Id `home` (new). It holds no scene of its own; it is the wrapper the rooms sit in.

| row | answer |
|---|---|
| kind | a building: `is_container`, no content of its own |
| ENTERED FROM (S2) | street |
| opens into (`default_entry`) | `home_hall` — clicking "Home" on the street lands her in the hall |
| the rooms inside it | hall, kitchen, living room, front door, garage, bathroom, her room, Ryan's room, the master bedroom, the garden (question 49) |
| area | Home is its own area: the walk home, 10 minutes, is charged once on the way in (`crossing_costs` time 10, question 44) |
| labels — what kind of place | `zone:home` |
| hours | none: a building can't close; each room keeps its own |
| hidden until | no |
| fill — word budget (S3) | 0 words: a building has no screen of its own |
| door | no: the doors in the house are on Ryan's room and the master bedroom |
| dress code or wanted state | none |

## On entering

| auto-fires | who is here, and when | things to do alone | ways out |
|---|---|---|---|
| none: she lands in the hall | — | — | inside: the hall's list of rooms · out: the hall's "Exit Home" to the street |

## What the player sees

- **On the street:** one button, "Home". Never "Hall".
- **In the hall:** the rooms of the house, and one way out to the street.
- **In any other room of the house:** a way back to the hall.

## Rows a gate needs

| row | gate |
|---|---|
| Home hangs off the street; the street stays the only root | the map is a place |
| nobody's home is the building or the hall | residents have homes |

## Why — the source of each key choice

| key choice | source |
|---|---|
| a "Home" building over the rooms | LO's play note, 2026-10-08 · `the-map.md` R2 ("its hub is the hall … named for the home") |
| it opens in the hall | `the-map.md` R2 and R3 (the hall is the hub) |
| a building holds no content | engine: a container swallows any scene put on it; hours on it do nothing |
| the id `home` | guess: new, no old id is renamed |
