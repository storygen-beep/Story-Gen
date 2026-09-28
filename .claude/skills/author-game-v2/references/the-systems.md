# The Systems — what the game keeps track of, decided before the rooms

## Why this file exists

`the-surfaces.md` R2c says *"the room list cannot be written before the systems list is."*

**There was no systems list.** The phrase appeared three times in this skill and was defined
nowhere — no field in `v2_state.json`, no sheet, no board step, no check. And `the-release.md`
never uses the word *system* at all: a release adds events to surfaces that already exist, so a
system can only be born in the board phase, which had no place to be born in.

A room needs a system that describes her, or it has nothing to be about. Course of Temptation reads what she is like
(`has_inclination`) in **218** of its 5,294 passages; SY1 carries the evidence.

Read out of the female-lead set — `family-ties` (rank 24), `zaras-school-life` (22),
`course-of-temptation` (5), `new-life-project` (16), with `degrees-of-lewdity` as reference —
the set `~/Documents/Female_PC_Craft_Study_20260823/gender_verdicts.md` settled on. Study and
scripts: `~/Documents/Systems_Study_20260902/`.

⚠️ **Nothing here is ported from the incumbent skill.** `author-game/references/system-patterns.md`
carries nine authored system recipes and `systems.md` an engine index. Both were read and
**deliberately excluded** — LO's call, 2026-09-02. They are cookbooks written from taste, and this
skill's standard is that nothing is taste. Every rule below is read out of a shipped game.

## What this file owns, and what it does not

| the question | the file |
|---|---|
| **what the game keeps track of about her, and what kind of place each room is** | **this file** |
| which screen a piece of content lives on, and how long a room's list is | `the-surfaces.md` |
| which meters exist, who owns them, and what the climb costs | `the-meters.md` |
| what happens between the introduction and the repeatable surface | `the-arc.md` |
| the world as a place someone could draw | `the-map.md` |
| how the prose reads once they click | `register.md` |

The nearest neighbour is `the-meters.md` W1, and the line between them is real: **W1 asks who
climbs, this file asks what the game is keeping track of at all.** A meter is one kind of system.
A skill she practises, a wardrobe, a tally of what she has done, a place's own reputation — those
are systems too, and none of them is an ascent tier.

⚠️ **Read this file BEFORE `the-board.md` §1.** The location count is derived from what a place is
for, and that derivation is circular unless the systems exist first: ask *"what would she do in
this room"* and the answer is a job description.

⚠️ **Pronouns are `she/her` because `want.player` defaults to `female`, and they are downstream of
that declaration — swap them if the game declared otherwise.**

⚠️ **How to read the evidence blocks.** Every rule states its shape first, as a set to choose from.
The quotation under it is fenced as EVIDENCE and names the game it came from. This is not
decoration: `templates/board.toml` put the games built from it into a dialect the genre does not use, and its
example rung of 15 was copied into their declared tiers. **Every word in an
example is being taught too.** Take the mechanism. Leave the furniture.

---

## SY1 · A system is something the game keeps track of about her, and there are two kinds

**Ambient** — fed by nearly every room. Time, money, tiredness, hunger, how clean she is. These
are the texture of an ordinary day.

**Sourced** — fed in one or two places, read all over the game. What she looks like, what she can
do, what she owns, what she has already done.

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** `course-of-temptation` reads `has_inclination` in **218**
> of its 5,294 passages — [ClassroomMenu] `<<if $pc.has_inclination("Knowledge from the Deep")`
> is one. What she is like is checked all over the game.

**A room needs a system about who she is.** An ambient system is fed by every room, so it cannot
make any room special — which is exactly what it is for, and exactly why it is not enough.

⚠️ **The split is not universal.** An earned resource such as money legitimately runs
write-heavy. **The read-heavy ones are the systems about who she is** — and those are the ones a
room can be built around.

⚠️ **Both kinds are required.** This is not an argument against ambient systems: the body's needs
are ambient, and `the-meters.md` M8–M10 owns them. The rule is that
ambient systems alone cannot furnish a world.

---

## SY2 · A sourced system has ONE place that feeds it and many that read it

R2c says a system earns its place *"by being read in more than one room, by more than one kind of
content."* That is right, and it is only half the shape: **it says nothing about where a system is
FED,** and the natural reading of it — build the thing in three rooms — describes an ambient system.

The field's answer is the opposite on the write side: one place feeds the system, and the rest of
the game checks it.

**So the payoff of a thin room is not thinness. It is being the only source of something.** A room
with two rows that feeds a system read in fifty places is doing more work than a room with eight
rows that feeds nothing.

**Write the reader first.** A source with no readers is `the-meters.md` W3's dead meter wearing a
new hat, and the arc file already says it in its own words — *"a skill ladder that feeds nothing is
a chore"* (`the-arc.md` A4b). Build what checks the number, then build the place that raises it.

---

## SY2b · The shape is not enough — a system describes her, it does not bookmark the plot

⚠️ **This rule exists because SY2 above is satisfied perfectly by a bookmark.** Written 2026-09-02
from `~/Documents/Load_Bearing_Systems_Study_20260902/`, a study run independently of SY1–SY2 and finished a few hours before them. Reproduced here before it was
believed: its field tables, its `worn_exposure` count and its DoL passage count were re-run and
match row for row.

> **A value that flips once and then means the same thing forever is a bookmark, not a system.
> Build the value that keeps moving — her body, what she is wearing, her disposition, the other
> person mid-act — and then write the ordinary scenes twice against it.**

**The field's set** — filter: read in ≥5 units, ≥10:1 read-to-write, ≥80% of readers do not
write it. `zaras-school-life` carries 9 and six of them
describe her — `PlayerCorruption` **376 read / 3 writ**, `PlayerClothes` 188/6, `PlayerEnergy`
185/11, `PlayerFitness` 33/3, plus two set-once traits, each written **once at character
creation and read forever**. `new-life-project` carries 8 and six describe her — `period` 195/15,
`corrupt` 164/2, `inhib` 75/2, `makeupAmount` 28/1, `allure` 24/2, `gender` 30/0.
`degrees-of-lewdity` runs `speech_attitude` at **1,914 reads against 5 writes** and `exposed` at
**586 reads across 119 places**.

`worn_exposure` shipped 2026-08-28 — an engine predicate (`v2.py:4459`), a derived aggregate, its own lock text, and a section in
`engine.md` §17 — built precisely so a scene could ask *"is she covered?"*, which `worn_corruption`
cannot answer because `getWornStatMax` skips empty slots and returns the same value for naked and
plainly dressed. DoL reads its equivalent 586 times in 119 places, most of them in the street
rather than in sex scenes.

### What to actually do about it — and it is never a new mechanic

**Go back to scenes that already exist and give each a second version.** The system is already
declared; what is missing is the content that consults it. Adding another meter is the wrong move
and makes the ratio worse.

> ⚠️ **ILLUSTRATION, NOT EVIDENCE — written for this file and not measured.** One system, read
> inside a scene that has nothing to do with clothes.
>
> ```
> exposure 0 (dressed)
>   You walk the corridor. 4B's TV is on. Nobody looks up.
>
> exposure 1 (underwear)
>   You walk it fast, arms crossed. 4B's TV is on. You hear the chair
>   creak, and you don't turn around to check.
>
> exposure 2 (bare)
>   You don't walk it. You count doors and pick the shortest line to
>   yours. The chair creaks. It creaks again, closer.
> ```
>
> No new mechanic, no new number, no new location. **The corridor got written three times, and the
> clothing system is now in the corridor.**
>
> ⚠️ **EVIDENCE — NOT A TEMPLATE.** `course-of-temptation` does exactly this on a campus walk,
> [EventCampusWalkBreezeStrong]: the same breeze is written *"whipping at your clothes"* or
> *"cutting at your bare skin"*, on `$pc.is_part_covered`. That check sits in **104** of its
> 5,294 passages.
> The engine primitive for this is stacked `[group]`
> bands on one key — `engine.md` §35, `the-surfaces.md` R6 — which is the same machinery the
> register file calls directed variety.

⚠️ **The brake, and it is not optional.** This is not a licence to declare more systems. R2c's
mirror-image failure is twenty declared systems and twenty dead ones, and SY3's own warning applies
here unchanged: **a system that describes her and is read in one place is worse than a plot flag
read in nine, because it cost a meter and bought nothing.** The instruction above is to write
content against what is already declared, not to declare more.

⚠️ **Bookmarks are not banned and this rule does not say to delete one.** `met_<npc>` gating an
introduction is correct and `the-first-hour.md` F5 requires it. What is wrong is a game whose
*only* well-read values are bookmarks.

⚠️ **Instrument limits, to be restated wherever these numbers are cited.** The ≥10:1 / ≥80% / ≥5
bar is **invented** — it exists to sort systems into two piles so the sides can be compared, and
the field's own spread (3 to 121 systems clearing it) means no threshold drawn from it is
defensible. An object read as a unit counts as one system, which inflates DoL and
`course-of-temptation`; **`zaras-school-life` and `new-life-project` use plain scalars and are the
fair comparison** — and they still carry 9 and 8, six descriptive each. `family-ties` routes
everything through page variables, so its top-by-reads is plumbing rather than systems. Condition
reads are counted structurally, never evaluated: a condition that can never be true still counts.

**No gate and no lint.** The bar is invented, which rules out a gate on the precedent that retired
four checks in this project. And a lint could only report *"this value is a flag written once"* —
which is true of correct introduction bookmarks too, so it would fail things for obeying
`the-first-hour.md`. **What a parser cannot decide is whether a value describes her**, and building
a check that pretends otherwise is the `objects` / gate-22 failure in a new suit.

---

## SY3 · A room declares what kind of place it is

Not prose, and not its menu. A short list of properties: what is in it, who can see her, when it is
open, whether she may undress there.

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** `course-of-temptation`, 126 rooms carrying **349 distinct tags,
> median 9 per room**. By family: description class 169 · room type 136 · zone 121 · opening hours
> and closed-redirects 114 · then the affordances — `outdoors` 24 · `hasmap` 23 · `greekhouse` 21 ·
> `campuswalk` 15 · `hasdressingroom` 7 · `allowsnack` 6 · `nobodyhere` 6 · `study` 5 ·
> `athleticwear` 5 · `bathroom` 5 · `stripallowed` 4 · `shower` 3 · `sleep` 3 · `homebase` 3 ·
> `notalk` 3. Even the room's sidebar icon is a tag.

**The menu — cut it down, never keep it.** These are the questions the field's tags answer, with
the field's own vocabulary written plain. A game takes the handful its systems actually read.

| what the label says | shape |
|---|---|
| where it is | `outdoors` · `street` · `zone:<name>` |
| who is around | `public` · `private` · `nobody_here` |
| what it has | `has_bed` · `has_mirror` · `has_shower` · `has_toilet` · `has_washer` · `sells_food` |
| what she may do here | `she_can_undress` · `she_can_sleep` · `she_can_study` · `she_can_wash` |
| when it is open | `opens_at` · `closes_at` · `closed_goes_to` |
| where her things are | `home_base` |

**The other shape, and it is a real option rather than a rival.** `degrees-of-lewdity` does not
keep a list per room. It stamps **one coarse kind** on each screen — 2,760 room screens across
**69 place types** (`home`, `cafe`, `park`, `pub`, `pool`, `arcade`, `brothel`…) — and
**616 passage sites** key off that one value. A list is more expressive; a single kind is cheaper
to keep true. Pick one and say which in the ledger.

**Half of these are navigation, and that is the point.** Opening hours, zone, where you are sent
when a place is shut — the map reads those. `homebase`, `stripallowed`, `study`, `has_bed` — the
systems read those. A few are read by both: `outdoors` decides whether weather applies *and*
whether being seen counts as public. **One declaration, two layers.** Do not keep two lists.

⚠️ **`labels` is not `serves`.** `the-surfaces.md` R2's `serves` is the room's *menu* — needs, work,
people, what happens here. `labels` is what kind of place it *is* — what would let anything happen
here at all. A room with `has_mirror` and no mirror row is a room whose systems have not arrived
yet, which is a finding, not an error. **Do not merge the two fields.**

⚠️ **Declaring more labels is worse, not better.** The label list is not a score, and the check
below runs the same direction: a label nothing uses is dead weight and gets printed as such. Write
the labels a system reads, and stop.

---

## SY4 · Systems attach to the label, not to the room — and OUR ENGINE CANNOT DO THIS

In the field a system is written once and turns up wherever its label is.

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** `course-of-temptation`, of 126 rooms: jobs and opportunities
> inject a row into **50**, a planned date into **22**, the restroom shelf into **12**, the three
> skill widgets into **10 / 9 / 7**, attend-class **9**, the dressing room **9**, and toys · drying
> wet clothes · a pregnancy test into **5** each. `new-life-project`, 59 hubs: trauma **8**, the
> pet **6**, quest letters **6**, work counters **5**, masturbation **5**.
>
> And the injection carries per-room settings: `<<exhibitionism "park">>`; `<<pregnancyTest
> "Bedroom">>` — where to return to; a kitchen naming its own allowed ingredients; a gym naming its
> own practisable sports.

**⚠️ WE CANNOT EXPRESS THIS. A canvas belongs to exactly one room.** `TemplateTrigger.location` is
a single string — `location=_require_str(trig_def, "location", "")`, `template_import.py:2137` —
and there is no plural form. A row wanted in three rooms is authored three times.

**Priced honestly: at our size, that is fine.** They have 126 rooms, or 2,760.
Copying a row into the three rooms that carry a label costs less than the machinery would.
**Revisit past roughly thirty locations**, where the copies start outnumbering the declaration.

**So the labels are a design tool here, not a wiring mechanism.** That is not a lesser thing. The
room that declares *public · no bed · open all night · she cannot undress here* has told the author
what belongs in it before a line is written. Course of Temptation's rooms carry such labels and
its systems read them — [Wardrobe] `<<set _stripallowed to $lastloctags.includes("stripallowed")>>`.
**Nothing in this file asks you to design against machinery we do not
have.**

⚠️ **One precedent exists and is worth knowing.** `clothing_rules` already sits on a location and
the clothing system reads it (`template_import.py` `TemplateLocation`). One system, hard-wired,
never generalised. If the general form is ever built, that is the shape it grows from.

---

## SY5 · A blocked row says a sentence

Every game in the set writes the refusal rather than hiding the row.

> ⚠️ **EVIDENCE — NOT A TEMPLATE.**
> *"You don't really need the bathroom at the moment."* — `course-of-temptation`
> *"You can't sleep yet, it's only \<evening\>!"* — `new-life-project`
> A named staffer who refuses her in person, rather than a greyed label — `new-life-project`
> (structure only)

**This rule is a cross-reference, not new doctrine.** `the-surfaces.md` R5c owns the locked door
that says why, R7 owns the screen that keeps one door when the day's caps are spent, and
`the-clock.md` C5 owns the menu item with hours. SY5 exists so that a file about systems does not
read as though it disagrees with them: **a system that refuses is a system that speaks.**

The systems angle it adds: the sentence is where the label pays off. *"You can't cook in the dark"*
is only writable because the kitchen knows it is a kitchen and the clock knows it is night.

---

## SY6 · The notice — ⚠️ SPECIFIED, NOT BUILT

**Do not author against this. It does not exist in the engine.** It is recorded here because it is
the one mechanism in this study worth asking for, and because a spec written down is how the ask
survives to whoever builds it.

**What it is.** `degrees-of-lewdity` calls one widget on **2,736 of its 2,760 room screens**.
Whichever system has something pending prints one short line into whatever room the player is
standing in.

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** Its body is JavaScript rather than a passage —
> `function effects()` in the corpus HTML — and it appends lines of this kind: *you're very cold and
> about to get hypothermia · your rented book is due* — one line per live condition, and the rest of
> its list is the town's calendar for the day.

**Why this one and not SY4's machinery.** It does not scale with room count. It works the same in
a ten-room game as in a three-thousand-room one, and it answers lostness — the genre's dominant
complaint at a 4.7% median share of player comments against grind's 0.9%.

**The proposed shape.** Game-level, not per-room, so one declaration reaches every room it matches
— which is also how it steps around SY4 rather than needing it:

```toml
[[notices]]
text       = "…"                  # one short line, room-agnostic
conditions = { version = "1.0", items = [ … ] }
labels     = ["home_base"]        # optional — only where this label is present
locations  = ["…"]                # optional — or these rooms specifically
priority   = 0
```

**Why it is cheap, and the precedent to build it from.** `_render_location_description`
(`v2.py:9848`) already emits a conditional chain onto the room screen using
`setup.triggerConditionsSatisfied` — the same helper the location passage calls for
`entry_conditions`. The notice is that path with two changes: **every** match prints rather than
first-match, and it appends after the description rather than replacing it.

⚠️ **That function is emitted from BOTH location paths** — with and without `entry_conditions` —
and its own docstring records that they were byte-identical copies and that this is exactly how a
change of this kind gets half-applied. Build it in one place.

**What exists today and why it does not serve.** `[[story_arc.hints.templates]]` is a conditional
hint engine with priorities and specificity sorting (`v2.py:6625`-`6650`), but it filters on
`tpl.npc_id !== npcSlug` — one character at a time, never a system — and it is the **v1** guidance
path, superseded by `[[quests.cards]]` for `quests_engine = "v2"` (`template_import.py:48`, `:424`),
which every game here uses. It cannot be repurposed without changing what it is.

---

## SY7 · The cheat page is free where it saves time

The most-liked comment on 8 of the study's 13 core mopoga pages asks for a cheat or a code, and a
phone player cannot open a console (*I'll Never Leave This Town*). So every game ships
`[ui.cheat_page]`, and four rows are **free** (`free = true`, plain buttons, no code):

- **money** — a trait row, `clamp = false`;
- **skip to morning** — `kind = "next_day"`, the real rollover, so the daily tick runs;
- **the next step now** — `kind = "play"`: it **plays** the step's own one-time scene, through
  its own conditions. It never sets the counter, because a jumped counter skips the scene forever;
- **ask again** — `kind = "reopen"`: unsets a refusal flag a trigger reads `is_false`. A game
  whose every "no" parks (the-arc A14) may need none.

Cut what the game cannot use; anything sold stays behind a code. Rows and rules: `engine.md` §48.

## What the board phase records

In `v2_state.json`, before locations are written (`state.md` carries the schema):

```jsonc
"board": {
  "systems": [
    { "id": "…", "kind": "sourced" | "ambient", "key": "…",
      "fed_at": ["location_id"], "labels": ["…"],
      "read_by": "one line — what changes because of it" }
  ],
  "locations": [ { "id": "…", "labels": ["…"] } ]
}
```

**`kind` is the SY1 fork and it is answered per system, not per game.** A game needs both.

**`fed_at` on a `sourced` system should usually be ONE location.** If it is five, ask whether the
thing is actually ambient — that is the SY2 test, and it is cheaper to answer in the ledger than
after the prose exists.

---

## The check

**One lint ships with this file. No gate, and the reason is in the skill's own history.**

`lint · the labels and the systems agree` — a declare-then-check over the ledger, modelled on the
`a need shuts a door` gate. It prints three lists and **moves no score**:

1. a label on a room that no declared system names — dead weight
2. a label a system names that no room carries — the system has nowhere to live
3. for each `sourced` system: whether `key` is written by a canvas at a `fed_at` location and read
   by at least one canvas somewhere else

⚠️ **Why a lint and not a gate.** A count is satisfied by declaring more, which is why R2c shipped
with nothing and why `objects` / gate 22 had to be deleted after it manufactured nine duplicate room
screens. This one runs the other way — **declaring more labels makes the output worse, not better**
— which is what makes it safe to build at all. It still gets no threshold, because no defensible
ratio was measured and inventing one is how four checks in this project were withdrawn.

⚠️ **P0 applies and is respected: never build a check for a state nothing is in.** A gate here
would be measuring the doctrine's age rather than the games. The lint is safe under
that rule precisely because it cannot fail anything — it reports *"no `board.systems[]` declared"*
and moves on.

**The candidates deliberately not built**, to be revisited once one game has used this file:

1. **`a source is alone`** — for each sourced system, how many rooms write it, printed against the
   field's own figures (1–2). Needs a game that has declared one; a distribution over zero games is
   not a distribution.
2. **`the room has something of its own`** — locations carrying no sourced system at all. This is
   the missing system about who she is, stated as a number, and it is the most useful check in this file. It is
   not built because it needs the declaration to exist first, and because "how many is enough" has
   no measured answer.
