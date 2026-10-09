# first_term 0.1 — iteration 002 report (part 7, the whole game)

2026-10-09. The build from the signed sheets, in seven parts, each one played and accepted by LO
(parts 1–6). Part 7 runs every check on the whole game. Nothing is committed, nothing is shipped, no
media harvest was run, and no skill or engine file was touched. The day-by-day log is `BUILD_LOG.md`;
the reader's tables are in `reader/`.

## Part 10 (2026-10-09): the last fix pass — final state

| check | part 9 | part 10 |
|---|---|---|
| `gates.py` · `--ship` | 61/88 · 8 BLOCK red | 61/88 · the same 8 |
| shape · playtest · rows · ladders | 22/0 · 10/10 · 0 · 43/44 (44/44 with C 1's flag) | the same |
| reader FAILs | 70 (46 waived, 24 left) | **67 (47 waived, 20 left)** |

**Fixed:** the eight older lines on `laura_catch`, `hub_laura_kitchen`, `hub_tom_cafe`, `hub_gary_booth` and
`hub_zoe_apartment` (`BUILD_LOG.md` "Part 10"). All pass on the re-read.

**New on the re-read: listed, not fixed (LO's rule for this pass):**
- `hub_tom_cafe`, truth: "Back to work." (open to 21:30, 30 minutes) can land her at 22:00, where the opening
  line ("keeping an eye on the room") and "The sign's turned to CLOSED" render together, and out of uniform
  "Day off? Then you're a customer" shows under the CLOSED sign.
- `hub_laura_kitchen`, the written no (craft, waived): "Leave her to it." answers "Come upstairs after"
  with nothing; "Could you get these? Here's twenty." has only "Pocket it.".
- `hub_zoe_apartment`, the written no (craft, waived): the bare "Stay a while." / "Go." after "Sit. You're
  next. Lips first."; "Paint my nails" and "Dare me something" have no answer on the canvas.

**The 20 left:**
- **17 kind C** (the 16 under Part 8 plus `jake_03`), for the lead and your sign.
- **2 edge minutes:** `laura_05`, `tom_06`.
- **1 new:** `hub_tom_cafe` at 22:00.

The other BLOCK reds are yours or the lead's (Part 7's list): the ledger lag and Hale's 08:30–08:45, your
playtest sign, the release build, the men's toilet (waived, no field), the `home_life` card, and the gate-gap
lines (waived, no field).

## Part 9 (2026-10-09): my last slips — where it stands now

| check | part 8 | part 9 |
|---|---|---|
| `gates.py` · `--ship` | 61/88 · 8 BLOCK red | 61/88 · the same 8 |
| shape · playtest · rows | 22/0 · 10/10 · 0 | 22/0 · 10/10 · 0 |
| reader FAILs | 72 (47 waived, 25 left) | **70 (46 waived, 24 left)** |

**Fixed:** the five slips on `laura_catch`, `hub_laura_kitchen`, `hub_tom_cafe` and `hub_zoe_apartment`;
all pass on the re-read. `laura_08` passes now (the punishment rule is built). `jake_03`'s "Nobody," is the
signed beat (`jake_03_my_boyfriend.md:34`) against Laura's Saturday row: kind C, moved there.
Hale B 1/2/5 stay at 08:30–08:45; Vance's promise stays out.

**The 24 left:**
- **Kind C, 17 verdicts** (the 16 listed under Part 8, plus `jake_03`), for the lead and your sign.
- **Edge minutes, 2:** `laura_05`, `tom_06`.
- **Found by the part 9 read, 5 verdicts on lines earlier reads passed (mine, not fixed: outside this
  part):**
  - `laura_catch`: "Kiss her goodnight." still shows locked at laura_step −1, against "Nothing else".
  - `hub_laura_kitchen`, four lines:
    - the breakfast line after she's eaten;
    - "Dinner in ten" after dinner;
    - Ryan "wet from the gym" on Sunday;
    - "while she cooks" at 21:00.
  - `hub_tom_cafe`: "Back to work." at 21:59 runs past the 22:00 close, and the work lines show in the shut
    room during Tom's 22:00 row.
  - `hub_gary_booth`: "Ten minutes, when you've got them." on Friday evening and out of uniform, when his
    ten minutes can't be taken.
  - `hub_zoe_apartment`: "What's tonight's dare?" when no dare can fire (Exhibitionism under 40, or no
    party tonight).
- Craft, waived: `hub_zoe_apartment`'s "Dare me something" has no written answer.

## Part 8 (2026-10-09): the reader's fixes — where it stands now

LO's call after part 7: fix the kind-A slips, build the three kind-B lines, re-read the changed canvases;
waive "no empty rooms" for the men's toilet and the lines the gate gaps cause (lead items 6, 7, 9); waive
the kind-D craft FAILs for 0.1 and keep the list; leave the ledger and the sheets alone. Details:
`BUILD_LOG.md` "Part 8".

| check | part 7 | part 8 |
|---|---|---|
| `gates.py` | 61/88 | 61/88 |
| `gates.py --ship` | 8 BLOCK red | 8 BLOCK red (the same eight) |
| ladder static problems | 24 | 27 (+3: Hale B 1/2/5 now fire 08:30–08:45, a time condition the ledger's window doesn't hold) |
| `shape.py --finish` | 22/0 | 22/0 |
| `playtest.py` | 10/10 | 10/10 |
| every ladder step played | 43/44 (44/44 with Laura C 1's flag) | same |
| who is where vs the ledger | 0 mismatches | 0 |
| reader FAIL verdicts | 135, 0 waived | **72**: 47 craft waived (LO), **25 left** |
| placeholders · "kid" | 43 · 0 | 43 · 0 |

**Read three times.** The 77 canvases part 8 changed were re-read (31 FAIL). I fixed six more of mine
from that read; the 12 canvases they touched were read a third time (12 FAIL, 9 of them craft). Each
deeper read found a few lines the earlier one passed, so I stopped there rather than loop; what is left
is below.

**Kind B:**
- **Built:** Laura's final no: after it, every catch is the punishment (`laura_catch` offers only "Take
  what's coming.").
- **Built:** Ryan's final no: his door goes back to one knock, and he opens it like you're a guest.
- **Not built: Vance's "I'll knock a little off his number".** No sheet gives the number or what it comes
  off, so I took the promise out of my line instead of inventing an economy. Your call below.

**The waivers.**
- **47 craft FAILs** are in `release_page.reader_waivers`, which the gate reads; the list is
  `reader/reader_all_p8.json` and `reader/reader_*.md`.
- **The men's toilet and the gate-gap lines** have no waiver field anywhere in `gates.py`. Only the
  reader row reads one (lead item 11). So "no empty rooms", "a named person is where the line says"
  (the building-gap lines), "nobody is woken" and the `when_also` items stay red, waived by you, as
  written here.

### The 25 reader FAILs left

**Kind C: a signed sheet line against another sheet or the ledger (the lead's, for your sign), 16 verdicts on 15 canvases:**
- `ryan_01` the opening's clock (OPENING.md 07:15–07:40 vs Ryan's and Mark's Monday rows)
- `vance_meeting` (his porch row starts only at `vance_met`)
- `zoe_00` "the girl from your Biology class"
- `laura_curfew_call` "Home by eleven" vs late at 22:00
- `laura_07` Mark's radio in the garage / Laura at breakfast on Saturday
- `mark_03` "Not the shirt this time"
- `mark_05` "on this couch tomorrow night" on a Saturday
- `mark_sunday_table` "one more twenty yourself" vs the +20
- `hale_04` the top button in any top, and Claire's knock at 18:40 vs "half past seven"
- `hub_jake_quad`, `hub_jake_canteen`, `hub_jake_class`, `hub_jake_gym` "Everyone was looking at you
  tonight" by day
- `tom_03` "Busy night?" at 14:30
- `tom_05` "Goodnight, Tom." at 14:35

**Stale verdict, 1:** `laura_08` "she punishes you. Nothing else." was FAIL because it wasn't built. It is
built now in `laura_catch`, but `laura_08` itself didn't change, so it wasn't re-read.

**Edge minutes, 2:** `laura_05` (a visit at 23:59 renders at 00:12) and `tom_06` (renders at 23:09, after
Tom's row ends at 23:00). The scene runs past the end of the person's row.

**Mine, still open, 6 verdicts on 5 canvases:**
- `hub_laura_kitchen`: "Don't tell Mark" while Mark is at the table, and "ten minutes" over 25 minutes.
- `hub_tom_cafe`: "Back to work." on a day off; the palm line without a booth-four visit that day.
- `hub_zoe_apartment`: "Still here?" Saturday 00:00–02:00 without `party_went`.
- `laura_catch`: the date line and the "tell me where you were" lines both show at suspicion 30+.
- `jake_03`: "Nobody," while Laura's Saturday row has her awake downstairs.

A fourth pass would take these; each one is a gate or a line of mine.

## Part 7 (kept for the record)

### Where it stood after part 7

| check | result |
|---|---|
| `gates.py first_term` | 61/88 pass, 27 fail |
| `gates.py --ship first_term` | **SHIP: NO**. 28 BLOCK rows: 19 green, 8 red, 1 n/a (no earlier release to load saves from) |
| `shape.py first_term --finish` | 22 pass, 0 fail |
| `playtest.py first_term` | 10/10 |
| every ladder step played (`playtest.reach_step`, `build_scripts/reach_all.py`) | 43/44 as the ledger declares it; 44/44 once Laura C 1 declares `laura_dress_invite` (tested on a scratch copy, ledger not edited) |
| who is where vs the ledger (every 5 minutes, all week) | 0 mismatches |
| the reader (`v2-reader`, all 193 canvases) | 193/193 read; 135 FAIL verdicts on 105 canvases |
| placeholders | 43, each marked `PLACEHOLDER —` in the TOML with its sheet line; table in `BUILD_LOG.md` |
| "kid" in the TOML | 0 |

To play it: `games/first_term/output/index.html` (a `--dev` build, with the jump list in the sidebar).

### The BLOCK rows that are red, and why (still the same eight)

1. **Each step fires when unlocked (24 static problems, "not played yet").** The game reaches every step
   (44/44 above); the gate compares each canvas's conditions with the ledger's ladder, and the ledger lags
   the scene sheets. The problems are:
   - The scene sheets ask for things the ledger's ladders don't declare: Laura C 1's
     `laura_dress_invite`; Laura C 2's `came_home_late` read by hours (4 h); Laura C 5's and Jake 3/4's
     `jake_date_went` read by hours; Mark A 4 and A 5's "not home late" and Mark A 5's bare legs;
     the presence checks (Laura in bed for Ryan A 5 and Mark A 4/A 5, Mark in the living room for Ryan A 5,
     Laura in the living room for Laura C 5).
   - Mark A 5 and Zoe A 4 have a second window (`when_also`, ledger L26 and L29), and the gate reads only
     the first one (lead item 7).
   Fix: the ledger takes the scene sheets' gates (your sign), and the lead fixes the `when_also` read.
2. **LO signed the playtest.** Yours: play every person on the release page from a new game to the door,
   then sign `release_page.signed_by_lo` / `signed_at`.
3. **The build is a release build.** Four parts: built with `--dev` (as the brief says), 82 media files
   missing (no harvest was allowed), and the portal entry still has `dev: true` and no `version`. All four
   are steps for the day you decide to ship.
4. **No empty rooms.** `college_mens_toilet` is open 07:00–22:00 with nothing to do. You chose to build it
   empty (DECISIONS 76). The gate offers three ways: a solo row, close it by hours, or mark it a
   thoroughfare.
5. **Every system has a card (6/7).** The `home_life` card in the ledger has no `sink` or `deadline`. The
   signed `home_life.md` says home costs no money; the card's cost reads "no money", and the gate counts
   the word "money" as money, so it asks for both. Fix: write `sink = "none"` and `deadline = "none"` on
   the ledger's card (your sign).
6. **A named person is where the line says (12 lines).** None is a person standing somewhere the rows
   don't allow. They are:
   - the gate's building gap (lead items 6 and 9): Ryan in his doorway (`jake_03`) and Laura at the mirror
     (`laura_01`);
   - sounds and voices through a wall (`ryan_05` wall/listen) and a calendar on the fridge
     (`mark_08` "Ryan's in green");
   - lines at the edge of a row: `ryan_05` hall at 06:00–06:45, `zoe_03` and `party_hookup` at the end of
     the party, `mark_05`'s start at 00:00, and the TV muttering downstairs in `touch_bed`;
   - Gary in booth four on `tom_04`, which is where she meets him. A presence check there made the step
     unreachable (found by `reach_all.py`), so it was taken back out.
7. **Nobody is woken (2).** `laura_01` and `laura_04`: Laura is in the kitchen at both hours. The gate
   thinks each house room is its own building (lead item 6). A presence check doesn't satisfy it, and on
   `laura_01` it also blocked the step, so the checks were taken back out.
8. **The reader passed (135 FAILs, 0 waivers).** See the next section.

### The reader after part 7: 135 FAILs on 105 of 193 canvases

| test | FAILs |
|---|---|
| true on every visit it can render on | 76 |
| the numbers and the clothes agree | 15 |
| hook | 14 |
| the written no | 12 |
| her voice at her level | 4 |
| next step | 4 |
| a solo button is a real act | 4 |
| want | 3 |
| who notices | 3 |

By area: Ryan and Laura 15, Mark and Vance 24, home 14, college 39, café/Zoe/Jake 31, pools/town/rest 12.
Each FAIL quotes its line in `reader/reader_<area>.md`. They sort into four kinds:

**A. Build slips. Mine to fix, no design call needed** (most of the 76 truth FAILs and the clothes FAILs).
These are lines false at some hour, day or outfit the canvas allows, where a condition or a shorter window
fixes it. Examples:
- **Class windows run to the last minute of the class.** About 20 college canvases (classes, first
  meetings, midterms, class hubs, the dress-code and desk-guy events) can fire at 09:59 and then speak of
  "before the class starts" or spend 90 minutes.
- **Tom's afternoon lines fire until 22:00:** "first tray of the afternoon" in `tom_01`, and Gary's
  booth on Saturday in `tom_02`.
- **Pools with no gate:** `hub_tom_cafe` "You're late", `hub_zoe_canteen` fries, and Zoe's party photos
  in `zoe_kitchen_quiet` / `zoe_bedroom_look` before any party.
- **Lines spoken before her choice:** `canteen_eat` "You eat it all" before "Not hungry", and
  `park_selfie` "You post that one" before "Delete them all".
- **Missing outfit or time checks:** "a skirt" on `park_walk` in jeans, and "the sun" on `park_rest` at
  21:00.
- **My own text against WANT:** `hub_vance_porch` "He'd sell me the house back" and `debt_offer` "Mark
  borrowed against it". The family rents from Vance.
- **Bad gates and buttons:** `garden_sun` opens Ryan's rungs one step early (`ryan_step gte 3/7`, his
  steps are A 4 and A 8). Solo buttons that do nothing: `door_dean_notice`, `vance_house_look`,
  `zoe_bedroom_look`, and `ryan_05` "headphones" / "Sleep".

**B. Signed lines the build didn't make.**
- Laura's final no: "Every catch after is a strict-mom punishment" (`npc_laura.md:72`). `laura_catch`
  still offers "Tell her the truth" after it.
- `ryan_08`'s screen says he opens to one knock after his path ends, but his door still offers "Two knocks."
- `hub_vance_porch` promises "I'll knock a little off his number" and builds nothing.
None of these needs a sex scene. They are buildable within the brief.

**C. Sheet lines that disagree with another signed sheet or the ledger.** The sheets are law, so these
are yours:
- `npc_laura.md:135` "Home by eleven." But SYSTEMS.md:498 makes coming home after 22:00 late, so eleven
  is still late.
- `zoe_00_quad_meeting.md`: "the girl from your Biology class". It can fire before she has been to any
  Biology class.
- `laura_07_dark_stairs.md`: "Mark's radio plays out in the garage". On Friday 18–19 Mark's row has him
  in the kitchen. "In the morning she'll be in the kitchen at breakfast": on Saturday morning Laura's row
  is elsewhere.
- `mark_03_shorts.md` "Not the shirt this time". No flag records the shirt.
- `mark_07_twenty_and_you_can_look.md` "You lay one more twenty on top of it yourself" vs the +20 toast
  (the count of whose twenty is whose).
- `npc_jake.md` / `laura_05`: "Everyone was looking at you tonight". On `hub_jake_quad`,
  `hub_jake_canteen` and `hub_jake_gym` it shows in the morning and afternoon.
- From part 6: Mark's rent text "$75." (`npc_mark.md`) after the rent rises; `npc_tom.md:46` Mon–Sat vs
  Friday (the lead fixes it for your sign).

**D. Craft verdicts.** Hook 14, written no 12, next step 4, want 3, who notices 3, her voice 4. Examples:
- a hub with no line pointing ahead (`hub_mark_garage`, `hub_jake_gym`, `hub_zoe_park`);
- a refusal that moves nothing (`party_drink_offer`, `hale_thursdays` "Not tonight", `garden_sun` "Not
  today");
- a bare "Go." as the only answer to an offer (`hub_art_office`, `hub_business_office`, `hub_jake_gym`);
- a pool line with no meter gate (`bathroom_shower`, Mark's hub thought).
Some sheets don't give these lines. Writing them means picking words the sheets don't hold, and that is
asking-mode territory. Each is either a line you give me, or a waiver in `release_page.reader_waivers`.

### What part 7 changed

- Named-person lines behind presence (Mark, Laura, Ryan lines at home; the garden rungs; `master_asleep`).
- Presence checks on `ryan_04` and `laura_05`.
- One-time lines lifted out of `mark_05` and `hale_04`.
- Two checks taken back out after `reach_all.py` showed they blocked steps (Laura in the kitchen on
  `laura_01`/`laura_04`, Gary on `tom_04`).
- The reader's verdicts are saved in `v2_state.json` `release_page.reader` (+ `reader_read_at`). That is
  the field the gate reads; no signed field was changed.

Full list: `BUILD_LOG.md` "Part 7".

## For the lead

`BUILD_LOG.md` "For the lead", items 1–10. New in part 7:
- **9.** The `default_entry` building gap also reaches the named-person gate.
- **10.** `playtest.reach_step` doesn't know the starting canvas's `StartingCanvas_` passages.

The building gap (items 1, 6 and 9) causes 4 of the red lines above on its own.

## LO's calls — paste only the lines you agree with

Answered on 2026-10-09: Parts 8, 9 and 10 (done above), Vance's promise (left out), Hale B 1/2/5 at 08:30–08:45 (the lead writes the ledger), the men's toilet (waived), the gate-gap lines (waived), the
kind-D craft FAILs (waived for 0.1), the ledger and sheets (the lead writes them for your sign).

Paste only this: `Ledger: take the scene sheets' gates into the ladders (Laura C 1, C 2, C 5; Mark A 4, A 5; Ryan A 5; Jake 3, 4) and Hale B 1/2/5's 08:30–08:45 — lead writes, I sign.`

Paste only this: `home_life card: sink = none, deadline = none (home costs no money) — lead writes, I sign.`

Paste only this: `Kind-C sheet lines (the 16 under Part 8 and jake_03 under Part 9, plus Mark's "$75" text and npc_tom.md:46): the lead fixes them in the sheets for my sign.`

Paste only this: `Laura's curfew: "Home by ten".` — or — `Laura's curfew: late starts at 23:00.`

Paste only this: `Gates: the lead adds a waiver field for BLOCK rows other than the reader (BUILD_LOG lead item 11).`

Shipping steps, for the day you decide to ship (not before): sign the playtest, rebuild without `--dev`,
run the media harvest (your call; 82 missing), set the portal entry's `version` and drop `dev: true`.
