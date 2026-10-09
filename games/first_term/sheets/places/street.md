# [READY] Place — Your Street

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08 against the system sheets. Id `street`.

| row | answer |
|---|---|
| kind | thoroughfare |
| ENTERED FROM (S2) | nothing: the ground, the only root |
| labels — what kind of place | `zone:street`, `outdoors`, `public` |
| hours | always |
| closed text | none: always open |
| hidden until | no |
| fill — word budget (S3) | 1,500 words (ledger, unchanged) |
| door | no |
| dress code or wanted state | none |

## On entering

| auto-fires | who is here, and when | things to do alone | ways out |
|---|---|---|---|
| first evening, 18:00–22:00: Vance on his porch (the meeting) | nobody stays here | none needed: a thoroughfare | **Home** (the house; it opens in the hall) |
|  |  |  | **Campus** (the college area) · **Town** (café, clothes shop, Zoe's flat, the party house) |
|  |  |  | on the street itself: Vance's house (0 min), the park (10 min, its own cost), the corner shop (0 min) |

**Areas and the walk** (LO's note, 2026-10-08: travel takes time). The street is the ground and is no
area. Home, Campus and Town are areas: time is charged once, when she crosses **into** one, and
leaving is free. Into Home 10 minutes, Campus 15 (a walk), Town 15 (the bus, no fare). Moves inside an area cost
nothing extra (LO, 2026-10-08, questions 43–46).

## Rows (`serves`)

| row | kind | system | cost and effect, with op (S4) | BRAKE (S9) | on a screen? |
|---|---|---|---|---|---|
| walk | — | the map | the area's time, charged on the way in: Home 10, Campus 15, Town 15 · no effect | none needed | a walk line by her clothes |
| home, late (22:00 or later) | work | parties · the curfew | `came_home_late` set true (read for 4 hours; her bed clears it); "Home" lands her in the hall | once a night | yes: the dark house, one line |

**Coming home late** (LO, 2026-10-08): only the street's way home into the hall, at 22:00 or later, sets `came_home_late`. Walking into the hall from her room or the kitchen never does. The act has its own short screen, so it is not a silent exit.

## Moving and waiting (LO's picks 1 and 2, 2026-10-08)

**Travel takes time** (round 11, commute 8/12): into Home 10 minutes, Campus 15 on foot, Town 15 on the
bus (no fare), the park 10 (its own cost). The engine charges an area's minutes without a screen and
does **not** print them on its button (only a room's own cost shows, as "10m"), so this street's
description says them once: *"Campus is fifteen minutes on foot. Town is the bus, fifteen. Home is
ten."* (LO, 2026-10-08, question 65).

**The wait button** (round 11, wait 8/12): it lives in the sidebar, under the clock, on every screen.
The engine ships three steps: **10 minutes, 1 hour, 1 day**. It moves only the clock; nothing else
changes, and no need refills (LO, 2026-10-08, question 62: kept for 0.1; the two engine notes are logged in DECISIONS).

## Random events in town (LO's pick 5, pool `town_event`)

Rolled 1 in 4 when she comes out onto the street, one a day (round 11, town events 7/12). When nothing
rolls, nothing shows.

| event | when | Good Girl | Curious · Daring | raise |
|---|---|---|---|---|
| the wind and her skirt | a skirt on, 07:00–22:00 | she grabs the hem, too late | she lets it blow | exhibitionism add +1 at Daring |
| a car slows, a guy whistles | Daring clothes, 07:00–22:00 | she walks faster | she turns and lets him look | exhibitionism add +1 at Daring |
| Vance on his porch | 18:00–22:00 (his row) | "Evening." He watches her past. | she slows down for him | Vance's Want add +2 (his sheet) |
| a jogger looks back | 07:00–10:00 | she pretends not to see | she looks back | none |
| the street, quiet | any time | "Nothing happens. A dog barks two gardens down." | | none |

## Why she's late (LO's play note, 2026-10-08)

Each outing sets its own flag when she leaves it, so Laura's catch, Ryan at night and Mark late say the
true reason. The street's way home after 22:00 still sets `came_home_late` (question 35).

| flag | set by | Laura's catch says |
|---|---|---|
| `late_party` | leaving Zoe's flat or the party house after 22:00 | smoke, someone's cologne: "Zoe's again?" |
| `late_shift` | leaving the café after Tom's close, 22:00–23:00 | "Tom kept you late again?" |
| `late_date` | Jake's goodnight at the front door | "Was he any good?" (Laura C 5's line, only after it) |
| none of them | a walk, the park until 22:00 | "Where were you?" She doesn't know, and the line doesn't guess |

**Cleared every night, two ways** (question 69): each is read only for 4 hours after it is set (hours
since the flag), and her bed sets them all false, with `came_home_late`. So a flag never lasts into
the next night.

## Rows a gate needs

| row | gate |
|---|---|
| the street is the only root | the map is a place |
| home late sets `came_home_late` on a screen | Laura's catch fires · an act is never a toast |
| Vance's meeting in his hours | a meeting fires where they are |

## Why — the source of each key choice

| key choice | source |
|---|---|
| `came_home_late` on the way home only | LO, 2026-10-08 (question 35, B) |
| the street shows "Home", not "Hall" | LO's play note, 2026-10-08 (sweep A1-35) |
| areas Home, Campus, Town; the walk charged on the way in | LO's play note, 2026-10-08 · `the-map.md` "Navigation — area, building, room" |
| street as the ground | `the-map.md` R3 · the board |
| Vance met on the first evening walk | LIVES §6 |
| the walk line by her clothes | guess · the wardrobe sheet |
| travel shown in the description; the wait button; town events | LO, 2026-10-08 (picks 1, 2, 5) · questions 62, 65 · events and the 1 in 4 guess |
| a flag per outing, cleared every night | LO's play note, 2026-10-08 · question 69 · sweep A1-17, A2-01, A2-02 |
