# [READY] Scene — zoe_01_first_party
> Signed by LO: LO, 2026-11-04.
> Changed 2026-11-04, writing pass: lines brought to the build (fresh text per room, her voice by level, the reader's fixes); signed by LO 2026-11-04.

> Changed 2026-11-03 to match the build (third alignment pass); signed by LO 2026-11-04.

> The signed plans behind this page: `proposals/COPY_FIXES_B.md`.

> **Changed 2026-11-01, re-signed by LO 2026-11-02** ("Signed, go ahead and build"; DECISIONS 124, the heat ladder a2): its gate or pay changes; the row is in `sheets/HEAT_LADDER_A2.md`.

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08.

| row | answer |
|---|---|
| person · step | `npc_zoe` · 1 (Zoe A 1) = `npc_jake` · 1 (Jake B 1): one canvas |
| where · when | Zoe's bedroom, then the party · Friday 19:00–23:00 |
| gate | her step 0 and Jake's step 0 · the kiss needs Corruption 20 |
| want | Zoe: her head in @player's lap · Jake: he watches her, not Zoe |
| next step | her first party, Zoe's first dare, and Jake across the room; a no leaves her step 0 |
| hook | Jake's number; Zoe's dares go on (A 2) |
| what she wears here | Zoe's party dress: the scene adds and equips it |
| her stage here | Good Girl can only refuse the dare; the kiss opens at Curious |
| explicit? | no |

## The step row (as built, 2026-11-03)

The seven columns, filled from what the build does.

**Kind · stage:** a dare and a kiss at a party · Curious (Corruption 20); the no stays open at Good Girl

| the moment | who sees or knows | what she risks | how she says yes | his move | does it finish | what changes after |
|---|---|---|---|---|---|---|
| Zoe's dress on her, Zoe's kiss dare, and Jake across the room | Zoe; the party; Jake | the party's eyes | "Kiss Zoe." or "Kiss the guy who's staring." | the dress, the dare | yes | her step 1 and Jake's; a no: step 0, `zoe_01b_kiss_again` a later Friday |

## Branch map — as built (2026-11-03)

One row per exit. Read from the build; it replaces the drafted map.

**`zoe_01_first_party`** — Zoe's Living Room · Fri 19:00-23:00 · Zoe there · needs Zoe's step = 0 · Jake's step = 0 · one time

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `dress` | Zoe drags you straight past the music into her bedroom and shuts the door. | no | "Change in front of her." → `change` | — |
| | | | "Turn around, Zo." → `change_no` | — |
| `change` | You change in front of her. | no | "Zoe! Eyes up here." → `party` | add zoe party dress · equip zoe party dress |
| `change_no` | "Turn around, Zo. I mean it." Zoe: "Boo. Fine. My eyes are shut." You change facing the wall. | no | "You looked." → `party` | add zoe party dress · equip zoe party dress |
| `party` | The flat is packed: half of campus, the bass coming up through the floor, red cups … | no | "Not tonight, Zo." → `no_dare` | Times you told Zoe no +1 · `party_went` set · `zoe_kiss_refused` set |
| | | | "Kiss Zoe." (Corruption 20+) → `kiss_zoe` | Corruption +3 (cap 39) · Exhibitionism +3 (cap 79) · `party_went` set |
| | | | "Kiss the guy who's staring." (Corruption 20+) → `jake` | Corruption +3 (cap 39) · Exhibitionism +3 (cap 79) · `party_went` set · `jake_kissed` set |
| `no_dare` | She steals your drink instead and dances off into the crowd. | no | "Look back at him." → `jake` | — |
| `kiss_zoe` | You turn your head and kiss her, right there on the couch. | no | "Look back at him." → `jake` | — |
| `jake` | He's been watching you since you came in: tall, a team jacket, a beer he isn't … | no | "Here's my number." — 4 versions, by flags, hour → Zoe's Living Room | Jake's step = 1 · `jake_met` set · `jake_number` set · varies: Zoe's step, `came_home_late` set, `late_party` set, `zoe_01_done` set |
| | | | "Not tonight." → `jake_no` | — |
| `jake_no` | He grins and goes back to his team, but he looks over every time you laugh. | no | "Back to the party." — 4 versions, by flags, hour → Zoe's Living Room | Jake's step = 1 · `jake_met` set · varies: Zoe's step, `came_home_late` set, `late_party` set, `zoe_01_done` set |

**`zoe_01b_kiss_again`** — Zoe's Living Room · Fri 19:00-23:00 · Zoe there · needs Zoe's step = 0 · `zoe_kiss_refused` · Corruption 20+ · under 8h since `party_went` · 24h+ since `zoe_kiss_refused` · one time

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `ask` | Zoe finds you on the couch, drops into your lap sideways and hooks an arm round … | no | "Kiss Zoe." → `kiss_zoe` | Corruption +3 (cap 39) · Exhibitionism +3 (cap 79) |
| | | | "Kiss the guy by the speakers." → `kiss_guy` | Corruption +3 (cap 39) · Exhibitionism +3 (cap 79) |
| | | | "Not tonight, Zo." → `no` | — |
| `kiss_zoe` | You turn in her lap and kiss her. | no | "Back to the party." — 2 versions, by hour → Zoe's Living Room | Zoe's step = 1 · `zoe_01_done` set · varies: `came_home_late` set, `late_party` set |
| `kiss_guy` | You get up, cross the room to a guy by the speakers you've never seen before, … | no | "Back to the party." — 2 versions, by hour → Zoe's Living Room | Zoe's step = 1 · `zoe_01_done` set · varies: `came_home_late` set, `late_party` set |
| `no` | She slides off your lap and goes to dance. | no | "Let her go and dance." — 2 versions, by hour → Zoe's Living Room | Times you told Zoe no +1 · back in 7 days · varies: `came_home_late` set, `late_party` set |

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Zoe A 1 and Jake B 1 (heat 10-06) |
| Good Girl refuses only; the kiss at Curious | LO, 2026-10-04 (the fixes) |
| the dress equipped by the scene | the truth rule · guess for the mechanism |


## Changed 2026-11-03 (LO: "I think dare refusal shouldn't be counted as done", then "Go"; DECISIONS 133)

- "Not tonight, Zo." still meets Jake (his number or his "Not tonight."; `jake_step` 1) but is no longer Zoe's step 1:
 `zoe_step` stays 0 and `zoe_kiss_refused` is set.
- New screen `zoe_01b_kiss_again` ("Same dare"): a later Friday party, 7 to 11 PM, at least 24 hours after the no, only
 from Curious. Zoe: "You chickened out on me last time. Same dare. Kiss someone. I told you I'd keep asking." From the
 second no only, also: "That's twice you've said no, babe. I'm counting." Yes: "Kiss Zoe." or "Kiss the guy by the
 speakers." (Exhibitionism +3, her step 1). No: "Boo. Next Friday, then. I'm not giving up on you." (`zoe_refused` +1,
 back in a week). Lines mine, signed by LO 2026-11-03 ("Signed").
- Her card while she waits: "You said no to her kiss dare. She said she'd keep asking." · goal Reach Curious (Corruption 20).
