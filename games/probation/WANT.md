# The Want — Probation

> Re-read before every release. Bump `want.last_read_at_release` in `v2_state.json`.
> Doctrine: `.claude/skills/author-game-v2/references/the-want.md`.

---

## 1. Who the player is — answered before she is described

**Who is the player?** `female`.

**Written character, or blank slate?** `written`.

Declared, not defaulted. The field runs 19 blank to 10 written and blank holds 80.4% of the
top-30's engagement, so `written` is the minority answer and needs its reason on the record: this
game's hold is a criminal record. The record is a specific thing a specific person did, it is read
out loud to her in the first scene, and a blank slate would have to keep it vague — which is the
one thing the premise cannot afford. She is named, she is 24, and the file has her in it.

**What does the player choose about her at minute zero?** What she went down for.

The intake scene already asks it. Delgado has the folder open on the desk and reads the top sheet
back to her, the way he does with everyone, and she can let him read it or she can say it first.
Three answers, one flag each — **a memory, not a slider**, and no stat screen anywhere:

| flag | what she says | what it buys her — reach, never flavour |
|---|---|---|
| `past_wheel` | she drove | she can drive. Marty lets her take the van on deliveries, which is the only legitimate way to touch the edge of the zone in week one |
| `past_paper` | checks that were not hers | she can keep books. Marty's ledger is hers by week three, and the hours sheet is a document she understands how to alter |
| `past_hands` | she hit someone, and it stuck | nobody in the block leans on her twice. Opens the refusal side — rungs where she is the one who is not afraid |

Read at five sites each: the three daily work surfaces at Marty's, plus a paired privilege rung on
two of them. **Additive only** — every original rung keeps its numbers and gains `<flag> is_false`,
so nothing closes and a save made before this shipped reads what it read yesterday.

⚠️ Separate each past-band from the surface's existing ladder with a non-`group` block. Adjacent
`[group]` blocks merge into one if/elseif chain and first match wins (`v2.py:14637`) — drop a past
ladder next to the standing-band ladder and the standing band goes silently unreachable.

## 1b. Who she is

**Cass Ridley, 24.** Eighteen months of it belonging to somebody else, four weeks served. A rented room over a
laundry on the east side, a monitor on her left ankle, and a job at a hardware and pawn shop
because the shop is one of two places in the zone that will sign an hours sheet.

**What she has to lose:** the fourteen months she is not doing. A violation is not a fine and not a
conversation — it is custody, and the game says so in plain words on the first screen.

**What holds her here:** `order`. Not a bill. Nobody wants money from her; four people want her
*located*.

It has a face and it has a date. **Delgado, Tuesdays at two, at the county office**, with the sheet
due Friday and her signature under his. And it has a second enforcer that is not a person at all —
the box, which does not care what she has decided about anything: a radius drawn around this room,
home by eight, and a battery that holds eighteen hours.

`hold_kind = order` · `hold_collector = npc_delgado`

⚠️ §4a: he holds the obligation and he is **not** the pipe the porn comes down. The field's
collector carries 0.4–3.8% of a game's explicit passages and is never the top figure. Delgado is
built as a man who could want her and mostly does not act, and he arrives late.

## 2. The appetite — where she lands, not where she starts

**To be in a room nobody can place her in, and to be wanted while she is in it.**

It cannot be finished, and the reason is structural rather than poetic: every room she gets into
becomes a room she is known in. The box logs a point every sixty seconds. Marty knows her hours.
Rae knows when she comes down the stairs. Delgado has all of it on one page every Tuesday. So the
appetite renews itself out of its own successes — the more ground she takes, the more of it is
accounted for, and the thing she wants moves one room further out.

**Where the hold stops being the reason:** the week the box comes off. She has the paperwork in her
hand, nobody is owed anything by anyone, and at 19:45 she walks the same route to the same back
room. The act does not change. Only the reason does.

## 3. What she is becoming — as ACCESS

**Bottom.** Six streets. Her room, the laundry under it, Marty's shop, the county office, the
lot behind the shop, the bus stop where the line runs. Home by eight. Every door she walks through
is a row in a log somebody else reads on Tuesday.

**Top.** The far side of the river after midnight, in rooms that are not in any zone, with people
who sign her sheet without reading it — and the box on the desk at home, saying she is asleep.

### The ascent tiers

Three, and each is a **different kind** of going further, so a player who will not climb one can
still climb another.

⚠️ **The rungs deliberately do not start at 15.** All sixteen declared tiers across five v2 games
put their lowest rung at exactly 15, because `templates/board.toml` shipped that table and a
placeholder in a template is an example. The field runs **8–17 rungs starting near 5**.

**`radius` — how far from the home point she is when it happens.** Space. Its rungs open *map*.
```
 5  the lot behind the shop, which is inside the zone and feels like it is not
12  the laundry after it closes — downstairs, still home on the log
20  the bus stop, the last address the box is comfortable with
30  the near approach to the bridge; the line is painted down the middle of it
45  across, briefly, and back before the log is pulled
60  across, and staying
80  the yards on the far side, with the box at home on the desk saying otherwise
```

**`hours` — how late, and how long she will stay.** Time. Its rungs open *the clock on rooms that
already exist* — which is what release 41 is made of.
```
 5  she is home by eight because she is home by eight
15  home by eight, and the last forty minutes of it spent somewhere she did not plan
25  through eight o'clock and back before the check
40  the diner at two, which is the only lit thing on this side
55  the whole night, somewhere, and Rae sees her come up the stairs at six
70  a day and a night, covered
85  gone, and the log says she never moved
```

**`vouch` — how many people are lying for her, and what they take for it.** People. Its rungs open
*the cast*, and this is the tier the sex economy runs on: what a signature costs.
```
 5  Marty signs the sheet without reading it
15  Marty signs hours she did not work
30  somebody says a sentence to Delgado's face that is not true
45  somebody puts a hand on the box
60  somebody alters a log that has already been filed
80  a name that is not hers, on a sheet that is not hers
```

**Counterweight:** `clean` — the fourteen months. It starts full and every rung above spends some.
It is a **brake, not the dominant meter**: the world never contracts as it falls, it only gets
louder about what it is going to cost. At zero, the hearing, which is a terminal state the game
ships on purpose and does not pretend is an ending for the product.

**What does release 41 add?** Asked of `hours`: a night band on a room that already exists. The
laundry at 02:00 is not the laundry, and the shop with the shutter down is not the shop.
Eleven locations times the `hours` ladder is the content schedule, and it needs no new ground.

## 4. The charge

**Reversal**, primary. Every adult in her life holds a signature over her — the officer, the
employer, the woman who owns the building, the one who can make the box say anything. The
ascent is her collecting those signatures one at a time, and each one she collects is a person who
now has something to lose.

**Transformation**, late and secondary. The box comes off and she walks the route anyway. §2's
last line is this charge stated as a moment; the two are written to agree.

## 5. The world

**Where does this happen?** The east side of a river city. One zone she is allowed in, a bridge with
a painted line on it, and a far side that is thirty seconds' walk and eighteen months away.

**What is outside the door she wakes up behind?** The stairwell, and then the street. The laundry
is directly below her room and is open to anyone at any hour, so the world can put a stranger under
her floor without asking her to travel. The interior can never be the whole game.

**How far can she get, and what stops her?** The box. Not money, not time, not permission — a
distance, measured continuously, that raises an alarm at somebody else's desk. This is the cheapest
honest stop in any of the ten premises and it is why this one was picked.

**Which shape is this?** `nested_zones` — zone → venue → room, plus a home. Chosen over
`map_hotspots`, which the circle argues for: hotspots wants 10+ drawn districts and this game opens
with six streets, so it would ship a map that is mostly locked pictures. The radius is expressed as
the **gate on the zone**, not as a drawing. Re-check against `the-map.md` R0 in the board phase.

**What her body needs, and what each one shuts:**

| need | what it does | what it SHUTS |
|---|---|---|
| sleep | falls through the day | under 25 she will not take an evening shift; the box check is missable |
| food | falls faster on work days | under 30 no work surface at Marty's renders |
| wash | falls on shift days | under 40 she will not go to the county office, and missing Tuesday is a violation |
| **battery** | the box holds 18 hours; the dock is 90 minutes and it is in her room | under 20% she cannot leave the zone at all · under 5% the alarm goes to Delgado's desk |

`battery` is the premise as a meter — the BOX's battery, never hers. It is the reason 19:45 in somebody else's back room is a scene
and not a decision.

**How alive?** Living world. Rae is downstairs at four in the morning whether or not the player went
looking, and the log is being read on Tuesday whether or not the player thought about it.

## 6. Why *this* person

| character | why she wants them, or why being wanted by them lands |
|---|---|
| `npc_marty` | 50s, owns the shop, wife works nights. The first person since the sentence who treats her as an employee instead of a case number — and she can feel exactly what it costs him to keep doing it. Being wanted by him is being wanted by the one man who has read the file and hires her anyway. |
| `npc_tobin` | 26, services the boxes out of the county office, bored out of his skull. He holds the only thing she actually wants and treats it as nothing. Being wanted by him is the cheapest transaction in the game and she knows it while it is happening. |
| `npc_rae` | Runs the laundry, owns the building, up at four. The only person who has never once asked what Cass did — and therefore the only person whose good opinion Cass could still lose. |
| `npc_delgado` | The officer. Knows every true thing about her and is scrupulously correct about all of it, which is what makes any slip the loudest event in the game. Arrives late, on purpose. |

## 7. Register

- **`narration_person` = `second`.** Declared once, immutable after the first release ships.
- **Crude-vocabulary ceiling** — the actual words, per character, per tier. A ceiling described
  abstractly gets written around. It is a **ceiling and never a floor**; writing under it is a
  defect.

| character | tier 1 | tier 2 | tier 3 |
|---|---|---|---|
| `npc_marty` | tits · ass · hard · his cock through his work trousers | cock · cunt · wet · suck · fuck | full — cunt, cock, cum, throat, fuck, come in her |
| `npc_tobin` | tits · dick · hard · his hand on her ankle | cock · cunt · fingers in her · fuck | full — cum, throat, ass |
| `npc_rae` | tits · ass · wet · what Rae calls her when nobody is in the laundry | cunt · fingers in her · mouth on her | full — cunt, cum, fuck |
| `npc_delgado` | nothing at tier 1 or 2 — the whole point of him is that he does not | — | one surface only, late, and it is `vouch 60`: cock, cunt, cum |

- **Where the crude register lives** — the repeatable surfaces, not the one-time scenes:
  - the back room at Marty's, 19:45–20:30, while the box is under 15%
  - the laundry after two, with the machines running
  - the lot behind the shop
  - Tobin's bench at the county office, Tuesdays, before the two o'clock

---

## The four checks

1. **What does release 41 add?** A night band on an existing room, gated on `hours`. Answered
   against a named tier, not against the appetite.
2. **What can she reach at the top that she cannot at the bottom?** The far side of the bridge,
   after midnight, with the box at home saying she is asleep.
3. **Which character would a player miss if deleted?** Marty. He is the only one who loses something
   real by wanting her, and every rung of `vouch` is priced in what it costs him.
4. **Which repeatable surface carries the crudest writing?** The back room at Marty's, 19:45, on the
   battery window — which is a surface the player re-enters nightly, not a scene she sees once.
