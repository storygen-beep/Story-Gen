# [READY] Place — Hall

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign. The quiet event is gone (DECISIONS 136). New section: what the heat proposal built here. Points at the copy fixes it took.

> **Changed 2026-11-02, signed by LO 2026-11-02** ("Signed, go with your recs, skip the play check"; DECISIONS 131, `sheets/READER_FAILS_A3.md`, Home): rows 11-13, the random events. `home_event_laura_robe`: "her robe slips open over her tits" (was "at the front"). `home_event_mark_reach`: under Corruption 40 (where "Lean back into him." can't show) he steps back fast, hips turned away, the mug low in front of his jeans: "Mind yourself, @player.". `home_event_ryan_towel`: the Curious and Bold screens end on Ryan's "Not here. Mom's up." (the event runs inside Laura's weekday kitchen row, so it is true every visit; added as a hook in `writer.py`, the screen files untouched).

> **Changed 2026-11-01, re-signed by LO 2026-11-02** ("Signed, go ahead and build"; DECISIONS 124, the heat ladder a2): its gate or pay changes; the row is in `sheets/HEAT_LADDER_A2.md`.

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08 against the system sheets. Id `home_hall`.

| row | answer |
|---|---|
| kind | thoroughfare |
| ENTERED FROM | the street, through "Home": the hall is where the Home building (`home`, new) opens |
| labels — what kind of place | `zone:home` |
| hours | always |
| closed text | none: always open |
| hidden until | no |
| fill — word budget | 2,000 words (ledger, unchanged) |
| door | no: the house's hub; everyone passes through |
| dress code or wanted state | none |

## On entering

| auto-fires | who is here, and when | things to do alone | ways out |
|---|---|---|---|
| Ryan A 1, day one only: out of the bathroom into Ryan | Laura, 23:00–02:00, only when she came home late | check what she is wearing on the stairs | the rooms of the house: kitchen, living room, front door |
| from the street, 22:00 or later: the dark house (sets `came_home_late`) |  |  |  |
| Laura's catch on the stairs (Laura C 2, then her repeat) |  |  | her room, Ryan's room, master bedroom |
| the stairs event: short skirt or no panties, someone below |  |  | bathroom, garage, the garden (back door) · out: "Exit Home" to the street |

## Rows (`serves`)

| row | kind | system | cost and effect, with op | BRAKE | on a screen? |
|---|---|---|---|---|---|
| Laura, on the stairs | person | Laura's ladder | `laura_suspicion` read: how hard she asks (colour) | only when `came_home_late` is set | yes |
| the stairs event | work | wardrobe | exhibitionism add +1, the first time each day | once a day, on the trigger | yes: her body |
| check your clothes in the hall mirror | work | wardrobe | none · the line reads her state | none needed: it writes nothing | yes, one line |

## Random events at home (system `home_life`; one a day, flag `home_event`)

Rolled 1 in 4 when she enters the hall, kitchen, living room or bathroom, at most one a day (question
59). Each event shows only when its person's row puts them there. When nothing rolls, nothing shows.
His Want is paid on the moment, never on her answer.

| event | where · when (their row) | Good Girl | Curious | Bold | raise |
|---|---|---|---|---|---|
| Ryan out of the shower | hall · Mon–Fri 06:45–07:30 | He steps out in a towel; they both say "Sorry." | "Walk past slowly" | "Let him look" (after Ryan A 4) | Ryan's Want +2 |
| Laura's robe | kitchen · Mon–Fri 06:30–08:00 | Her robe slips at the counter; she ties it, pink. | @player doesn't look away. | — | Laura's Warmth +1 |
| Mark reaching past | kitchen · Sun 08:00–22:00 | He reaches over @player for a mug, close. | @player leans back into him. | — | Mark's Want +2 |
| Mark asleep, TV on | living room · Mon–Sat 00:00–02:00 | She turns the TV off; he doesn't wake. | His hand catches her wrist, eyes still shut. | — | Mark's Want +1 |
| Ryan's door, a hand's width | hall · every night 22:00–00:00 · after Ryan A 7, Kayla not over | Light under the door, music low. | She stops and looks in; he's watching the door. | — | Ryan's Want +1 |

## Built from the heat proposal (signed 2026-11-03)

The plan: `proposals/FIRST_TERM_HEAT_PROPOSAL_20261103.md`. What the build has here:

**Walk-ins.** Her activity rolls on entry (1 in 4 at her lowest band, more higher up); on a hit someone walks in. A man's pay sits on the moment; her cover pays 0.

| who walks in | her activity | when | his pay, on the moment | her bolder answers |
|---|---|---|---|---|
| Ryan | Check your clothes in the hall mirror | Sat, Sun 07:30–14:00; Sun, Mon, Tue, Wed, Thu 19:00–00:00 | his Want +2 | "Stay at the mirror." Exhibitionism +1, cap 19/39/59 by her band |
| Mark | Check your clothes in the hall mirror | Mon, Tue, Wed, Thu, Fri, Sat 01:30–02:00 | his Want +2 | "Stay at the mirror." Exhibitionism +1, cap 19/39/59 by her band |

**Acts, rungs and pools.**

| what | where | buttons and pays |
|---|---|---|
| a media pool (A12) | the stairs, no-panties screen | a `_t4` pool, no new prose |

## Rows a gate needs

| row | gate |
|---|---|
| the room Home opens into, hub of the house | the map is a place |
| Laura there only with the flag set | standing surface |

**Copy:** lines here were rewritten from `proposals/COPY_FIXES_A.md`, `proposals/COPY_FIXES_C.md` (signed with the a2 sheets, DECISIONS 125).

## Why — the source of each key choice

| key choice | source |
|---|---|
| the hall is the house's hub | the board, 2026-10-08 · the map's shape |
| inside the Home building; the street shows "Home" | LO's play note, 2026-10-08 (sweep A1-35) |
| Laura's gated stairs row | LO, 2026-10-08 (LIVES) |
| a hall mirror | guess |
| the random events at home | LO, 2026-10-08 (pick 4) · round 11, random events at home 6/12 · the events and the 1 in 4 guess |

> Changed 2026-11-02 (reader a3, older rows; DECISIONS 131; LO: "fix the older ones too"): the robe, Mark reach and towel events each end on a forward thought; the robe's "She knows you know it." needs `laura_04_done`.
