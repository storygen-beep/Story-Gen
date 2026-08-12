# Back Home — review ledger

A living list of what is wrong with this game. Opened 2026-08-12, after v0.1 shipped 10/10 on
`gates.py`. Items get added as they are found and struck as they are fixed; nothing is deleted.

**Why this exists.** `gates.py` measures ten things and every one of them is green. None of the
ten measures whether the game is legible, whether the economy has teeth, whether the player knows
what to do, or whether the world can grow. This file covers what the instrument does not.

---

## How to read an item

| field | meaning |
|---|---|
| **severity** | `BLOCKER` · `HIGH` · `MED` · `LOW` · `OPEN` (unresolved question) · `DEFERRED` (known, parked by LO) |
| **layer** | `GAME` = one-off TOML · `SKILL` = the doctrine taught it wrong or never taught it · `ENGINE` = the substrate. Per `CLAUDE.md`: fix the skill too whenever a correct skill would have prevented it, or it ships again next game. |
| **evidence** | a `file:line`, a measurement, or a command. Anything without one is marked *opinion*. |
| **status** | `OPEN` · `FIXED (<rev>)` · `WONTFIX (<reason>)` |

Current count: **21 open**, 0 fixed.

---

# 1 · The world does not make sense as a place

The report that opened this file, from LO, looking at the location graph:

> *What is landing, why shop is in the house??*

Both halves are real, and the second one is worse than the diagram suggested.

---

### W1 · There is no outside. The shop is a room in the house.
**severity** HIGH · **layer** GAME + SKILL · **status** OPEN

`1_metadata_and_locations.toml:121` gives `the_shop` an `entry_from = "the_front_room"`, and
`:55` lists it in the front room's `navigation_order` alongside the kitchen and the landing.
There is no street, no front door, no town, no outside node of any kind. Structurally, walking
to work is the same action as walking into the kitchen.

The fiction knows better and says so — the location description reads *"ten minutes' walk away"*,
and there is a whole canvas about the walk (`activity_the_walk`, `3_activities.toml`). But the
walk is **content inside the shop**, not a place. The twenty minutes each way that the Want calls
*"the one stretch of the day nobody in the game can see her"* happen at her workplace.

**Consequences, in order of size:**

1. **`exposure` has nowhere to pay outside the house.** It is the most gameable tier in the game
   and its entire consequence surface is four adults who already live with her.
2. **There is no supply of new people.** The only renewable character slot is the box room. A
   world with no exterior can only ever recycle its interior.
3. **The map reads as nonsense**, which is how this was found.

**Fix shape:** the world needs a `the_street` (or `the_close`, or whatever it is called) between
the front room and the shop — and that node is where the outside layer eventually hangs. It is
also the correct answer to *"what does release 41 add"* (see N1).

**Skill angle:** `references/the-board.md` §1 asks for each location's dramatic job, who is
there, and what she does repeatedly. It never asks **whether the set of locations is a coherent
space**. Every location in this game passes §1 individually and the graph is still wrong. This
is the same root cause already logged in memory as *location-design root-cause — the skill treats
PLACE as backdrop; the fix is a `map_design` step*. It recurred. That is the definition of a
skill-layer defect.

---

### W2 · "The Landing" is unexplained, and there are no stairs
**severity** MED · **layer** GAME · **status** OPEN

A landing is the upstairs hallway of a British terraced house. The game never says so. Its
description (`1_metadata_and_locations.toml:79`) opens *"Four doors and a airing cupboard"* —
which assumes the reader already knows where they are standing, and also contains a typo
(*"a airing"*).

Compounding it: **the front room connects straight to the landing.** No stairs, no hall. So even
a player who knows the word gets no signal that they have gone up a floor, and the one physical
fact the room is built on — *"the boards give you away halfway along"* — has no spatial setup.

**Fix shape:** either name the vertical movement in the navigation ("Go up") or add a hall/stairs
node. The cheaper half — rewriting the description's first sentence to orient the player and
fixing `a airing` → `an airing` — costs nothing.

---

### W3 · The map has no floors, and the fiction contradicts the graph
**severity** MED · **layer** GAME · **status** OPEN

Eight locations in a flat graph with no up/down anywhere. Two specific contradictions found:

- `rung_ray_garage_bench` is written around the garage being *"the only room in the house with a
  door to the outside"*. That door does not exist in `navigation_order` — the garage's only exit
  is back to the kitchen (`:73`, `navigation_order = []`).
- The bathroom and the box room are upstairs in the prose, the garage is downstairs, and nothing
  in the navigation communicates either.

**Fix shape:** decide the house's real plan once, write it into the ledger, and make the graph
match it. Cheap now, annoying after another 20k words are hung on it.

---

### W4 · Three of the four men have no bedroom, and the Want promises one that was never built
**severity** HIGH · **layer** GAME · **status** OPEN

Every location in the game, and where each character is ever scheduled:

```
locations   the_front_room  the_kitchen  the_garage  the_landing
            her_room  the_bathroom  the_box_room  the_shop

Ray    ->   bathroom, front room, garage
Dean   ->   bathroom, front room, garage, kitchen
Cal    ->   bathroom, front room, kitchen
Marek  ->   box room, kitchen
```

**Ray, Dean and Cal do not sleep anywhere.** Two bedrooms exist in a house with four adults in
it, and the landing's own description (`1_metadata_and_locations.toml:79`) says *"Four doors and a
airing cupboard"* — her room, the bathroom, the box room, and a fourth door that opens on nothing.
A player will notice this on day one, because the landing is the room they cross most.

Worse, the Want depends on the missing rooms. `the_want.md:41`, defining what the top of the
ladder actually buys:

> The garage, the box room, **her father's room** — places she had no business in — are simply
> places she goes.

Ray's bedroom is one of three named rewards for reaching the top of `nerve`, and it does not
exist. `gates.py` cannot see this: gate 8 checks that authored *gates* reach each meter's top
band, not that the Want's *prose promises* were built.

**Fix shape:** Ray's room is the one that has to exist, because the Want sold it. Dean's and Cal's
doors should stay shut and be **named locked doors on the landing** — which is exactly the shape
`the-release.md:78` wants every release to end on, and it makes the "four doors" line true
immediately at zero cost.

---

### W5 · Location names are British interior jargon being used as UI
**severity** MED · **layer** GAME + SKILL · **status** OPEN

The navigation buttons are the only words in the game a player *must* parse correctly to move,
and two of eight are terms a non-British player has no way to resolve:

| current | what it actually is | proposed |
|---|---|---|
| **The Landing** | the upstairs hallway | **Upstairs** |
| **The Box Room** | a small spare bedroom, here rented out | **The Lodger's Room** |
| The Front Room | the living room | keep — guessable, and the description names the sofa and telly |
| The Garage · The Kitchen · The Bathroom · Her Room · The Shop | — | keep |

The rule this comes from, worth writing into doctrine: **a location name is UI; the prose is
voice.** Keeping *ta*, *telly*, *the good sofa*, *sort it by next Monday* across 36,000 words is
the register working. Making a player guess which floor they are on is not register, it is a
navigation bug wearing register's clothes.

`references/the-board.md` §1 specifies `id`, `name`, `description`, `image`, `entry_from` and
`navigation_order` and says nothing about the name being legible to someone outside the setting.

---

### W6 · Six prose references to rooms and exits that are not in the graph
**severity** MED · **layer** GAME · **status** OPEN

Counted across the three authored phase files:

| phrase | occurrences | exists as a location? |
|---|---|---|
| *the hall* | **6** | no |
| *front door* | 2 | no |
| *the street* | 1 | no |
| *outside the house* | 1 | no |

The prose has already built the world the graph is missing — it refers to a hall six times. The
map is not merely incomplete against reality; it is incomplete against **this game's own
paragraphs**.

---

### W7 · Activity labels are written as voice, but they are doing the job of UI
**severity** MED · **layer** GAME + SKILL · **status** OPEN

Found the way these things should be found: LO read the location menu and asked *"there is an
activity something like sit with it, what is it, sit on sofa or what actually it is??"*

He was looking at `activity_evening`, whose name is **"Sit with it"** and whose first line is
*"You sit on the end of the good sofa with your feet up under you and let the telly happen at
you."* It is the game's pass-time action: +90 minutes, −5 energy, no gate, and by its own author's
note *"the click that makes every other schedule reachable, so it is also the single most-repeated
screen in the game."* The most-clicked button in the game does not say what it does.

It is not alone. The located canvases render their `name` as the link text on the location page,
and several are opaque out of context:

| label as it renders | what the click actually does |
|---|---|
| **Sit with it** | sit on the sofa, pass 90 minutes |
| **See to it yourself** | masturbate |
| **The bench** | her father's weight bench, in her room |
| **The regulars** | serve customers at the shop |
| **Someone's in there** | the bathroom is occupied — wait, knock, or walk in |
| **The walk down** | walk to work |

And the ones that already work, in the same game, with no loss of register: *Sleep* · *Wash* ·
*Take a shift* · *Listen through the wall* · *Stand on the landing* · *Do something about the
door*.

**The rule, and it is the same one as W5 one layer down:** the words on a **location page** are
UI and must name an action; the words **inside a scene** are voice. The register lives in the
paragraph the player gets after clicking, not in the button.

**Explicitly not in scope:** the rung names inside a hub — *Stop pretending it's a favour*, *Make
him wait*, *Come down in what you slept in*, *Ask him where the bench went*. Those are choices in
a conversation, they arrive with the scene's context already on screen, and evocative is correct
there. Changing them would be a regression.

**Skill angle:** `references/the-board.md` §1 and `the-release.md` describe what a surface must
*do* and never mention what it must be *called*. Nothing in the skill distinguishes a navigation
label from a choice line, so an author writing in one register writes both the same way. This
defect and W5 are the same missing rule, and it should be written once, covering both.

---

# 2 · The economy has no teeth

Four findings, and the first one is the largest single defect in the game.

---

### E1 · Money is effectively unlimited, so the `need` tier never has to rise
**severity** BLOCKER · **layer** GAME + SKILL · **status** OPEN

Measured on the merged TOML:

```
items declared ............................ 0
conditions anywhere that read `money` ..... 0
canvases carrying a real `costs` block .... 2   (activity_shift 25 energy, activity_stock_hour 15)
```

So the only thing in the entire game that consumes money is the engine's rent system —
**£120 a week** (`0_systems_spec.toml:45`).

Against that, the income:

| surface | pay | time | cap |
|---|---|---|---|
| `activity_shift` | 30 | 6h | once/day |
| `activity_stock_hour` | 12 | 1h | once/day |
| `activity_shop_regulars` | **10** | 2h | **none, and no energy cost** |

£42/day from the two capped surfaces alone covers £120/week in three days. And
`activity_shop_regulars` is an uncapped, cost-free £10 loop, so money is not merely sufficient,
it is **unbounded**.

**Why this is the top item.** The Want (`the_want.md:51`) defines `need` as *"what she'll trade,
and how openly"*, and `0_systems_spec.toml:33` states the design intent explicitly: *"120/week is
four shifts — most of her week, survivable, and one bad week forces the ask."* **No week forces
the ask.** Which means:

- Ray's entire front-room ladder is gated on `need` (15 / 35 / 45 / 55 / 75) and the player is
  never pushed toward any of it —
- and Ray is the answer to the Want's own check 3: *"Which character would a player miss? Ray —
  the whole charge is the proud one watching her come down."*

The emotional centre of the game is behind a meter with no pressure driving it.

**Now measured against the field, 2026-08-12.** 18 shipped browser sandboxes were parsed
(~62,000 passages; corpus and method in `.claude/skills/author-game-v2/DOCTRINE_GAPS.md` Appendix B):

| | the field | `back_home` |
|---|---|---|
| conditions reading money, per 1,000 passages | **median 67.3** — every sandbox in the set gates on money | **0** |
| spend-sites : earn-sites | **median 2.2 : 1** (DoL 1.76:1) | **1 sink : 12 sources** |
| carries a recurring obligation | 14 of 19 — DoL says *rent* **130** times | yes — the one part that works |
| money movements with a computed amount | median 24% | 0% — every grant is a literal |

The only two games at zero money gates are `emilie` and `lustbound` — a scripted time-slot game and a
small one. **`back_home` is sitting with the games that are not sandboxes.**

⚠️ **Corrected 2026-08-12 by the gate built for this.** This entry originally said "three sources",
counting only the clean shop income. Counting every canvas that grants money — the nine transactional
rungs included — the game has **twelve** ways to earn against **one** sink. The defect is worse than
first recorded, and the gate found it because it counted what the game does rather than what the
author remembered.

**Fix shape (design, needs LO's call):** cap or cost `activity_shop_regulars`; give money a second
sink that is not rent (the boiler, the council letter, her phone, a bus fare once W1 exists); make
one bad week actually happen — a missed shift, cut hours, a bill. The lever the engine already
supports for free is `[settings.rent]` plus real `costs` blocks.

**Skill angle:** `the-board.md` §4 says *"write down what an ordinary day is… sleep, eat, wash,
earn, spend"* and stops there. There is no step that asks **whether the earn and the spend are in
tension**, and no gate that measures it. A game can pass all ten gates with an economy that does
nothing. That is a missing gate, not just a missing paragraph.

---

### E2 · Every ascent tier can be ground with a free, uncapped +1 click
**severity** HIGH · **layer** GAME + SKILL · **status** OPEN

Repeatable surfaces with no daily cap and no cost that grant ascent points:

| canvas | grants | minutes | rate |
|---|---|---|---|
| `activity_the_bench` | nerve +1, exposure +2 | 25 | **7.2 pts/hr** |
| `activity_his_room` | need +1, exposure +1 | 20 | 6.0 |
| `activity_the_landing` | exposure +1 | 15 | 4.0 |
| `triggered_the_slot` | need +1 | 20 | 3.0 |
| `activity_the_wall` | nerve +1 | 30 | 2.0 |
| `activity_alone` | nerve +1 | 30 | 2.0 |
| `activity_frontroom_late` | exposure +1 | 60 | 1.0 |

A tier is 75 points. At the best rate that is **ten in-game hours of clicking one link** — less
than a single waking day. The ladders are therefore paced by patience, not by the fiction, and a
player who notices will skip the content the points were supposed to buy.

Note this is *not* the same complaint as "the game is grindy". The mopoga top-30 study logged in
memory found lostness (4.7% of comments) beats grind (0.9%) as the genre disease. The defect here
is that **a repeatable texture surface and a load-bearing escalation surface pay the same
currency at different prices**, so the cheap one dominates.

**Fix shape:** ascent points should come from the surfaces that are *about* going further —
peeps, walk-ins, rungs — and texture surfaces should pay 0. Or every uncapped one gets
`max_triggers_per_day = 1`, which is one line each.

---

### E3 · `energy` and `hygiene` are decorative
**severity** MED · **layer** GAME · **status** OPEN

Zero conditions in the game read either trait. `hygiene` decays 10/day and `activity_wash` grants
+45 — a number that goes down and comes back up and is never asked about by anything. `energy`
is read by exactly two `costs` blocks, both at the shop.

They occupy two labelled rows in the sidebar (`0_systems_spec.toml:127-137`), which means the
player is being shown state that does not affect play. That is worse than not having them.

**Fix shape:** either gate something on them (a low-hygiene reaction from Dean is free content and
exactly the TRIGGERED shape the skill wants) or stop displaying them.

---

### E4 · `pride` gates exactly one thing, and it hides a whole thread behind itself
**severity** MED · **layer** GAME · **status** OPEN

`pride` appears in 17 conditions. Sixteen are prose bands inside four canvases
(`activity_evening`, `activity_shop_regulars`, `activity_frontroom_late`, `triggered_hannah_again`).
**One** is a real access gate: `canvas_someone_who_knew` requires `pride lt 60`.

Two problems fall out:

1. As designed (`the_want.md:53`, *"It buys nothing; it is what she is paying with"*) pride is a
   price with no purchase. Nothing ever costs more because it is low. It is a number that falls.
2. That single gate is load-bearing in a way nothing flags. `canvas_someone_who_knew` is the only
   setter of `seen_from_outside`, which is the sole gate on `triggered_hannah_again`. **A player
   who never asks anyone for money never drops below 60 pride and never sees the Hannah thread at
   all** — the entire outside-world thread, invisible, behind an optional meter falling.

**Fix shape:** decide whether pride is a resource or a readout. If a resource, something has to
charge for it. Either way, `seen_from_outside` should not be reachable only by spending it.

---

# 3 · The player is not told anything

---

### G1 · The game ships zero quests, and a nav link to an empty page
**severity** BLOCKER · **layer** GAME · **status** OPEN

`0_systems_spec.toml:19` declares `quests_engine = "v2"`. The authored table is **`[[quest_cards]]`**
(`template_import.py:2462`, parsed into `class QuestsCard` at `:997` — *not* `[[quests]]`, which is a
different, unrelated table). `back_home` declares **zero** of them across all five phase files, and the
built game confirms it:

```
games/back_home/output/index.html:   setup.quests_cards = [];
```

`v2.py:14711` dispatches the V2 QuestsPage on that metadata key, so the game renders a sidebar
entry **Quests 📋** leading to a page headed *"What's Next"* with nothing beneath it. Every card
section and the Story Goals block are inside `<<if>>` guards on an empty array.

The player's only guidance is the auto-inferred `setup.help_data`, which is generated from canvas
effects and lists activities by name — not a directive, not a goal, not an order of operations.

Against the mopoga top-30 Twine study in memory: **lostness is the genre disease at a 4.7% median
share of comments, five times grind's 0.9%.** This game has the disease in its purest form — 97
canvases, 8 locked doors, three interlocking meters, four hidden flag chains, and no statement
anywhere of what to do first.

Concrete chains the player currently cannot discover:

- `exposure ≥15` opens her mother's boxes, which is the only source of `worn_corruption ≥4`,
  which is the only key to `triggered_caught_in_passing`.
- `exposure ≥35` on *one specific kitchen choice* sets `dean_open`, the sole unlock for Dean's
  entire late-night front-room hub.
- Ray appears in the garage only on weekdays 18:00–20:00, Dean only on weekends 14:00–17:00.

None of that is stated in the game.

**Fix shape:** author `[[quests]]` cards per the quest-card ladder doctrine in memory (stepped
bands on exclusive trait ranges, each card naming a directive and a milestone). This is the single
highest-value release the game could ship and it adds no locations.

---

### G2 · ~~Seven of eight locked doors say nothing about what opens them~~ — **WITHDRAWN 2026-08-12. Not a defect.**
**severity** ~~HIGH~~ · **layer** — · **status** WITHDRAWN

**This finding was wrong, and the game was right.** `references/engine.md` §15 already rules on
`locked_text` and rules the *other way*:

> omit `locked_text` and the greyed row shows the action ("Stop pretending it's a secret") — a *want*
> the player can name, which is what sells the next release. Set it and the row shows the reason
> instead — clearer about the gate, weaker as a door. **Prefer the want unless the gate is genuinely
> obscure.**

So the seven doors were following v2's own verified doctrine. A greyed row reading *"Ask him where
the bench went"* is not silent — it states the want, which is the thing that sells an update.

Caught while building a gate for it: the gate fired on 7 of 8 doors, all of them compliant. **A check
that fails a game for obeying the skill is a bug in the check**, so no gate was shipped.

What survives is narrower and belongs to G1: a door advertises the *want*, and the *route* is the
guidance card's job — which back_home does not have, because it has no cards at all. One finding,
not two.

*(Original text kept below for the record.)*

**severity** HIGH · **layer** GAME · **status** OPEN

All eight doors set `show_when_locked = true` (gate 9 passes on the count). Only one has
`locked_text`:

| canvas | door | locked_text |
|---|---|---|
| `hub_cal_frontroom` | Stop pretending it's a secret. | *"Not yet — he still thinks he's getting away with it."* |
| `hub_ray_frontroom` | Ask him for it in front of the others. | — |
| `hub_ray_garage` | Ask him where the bench went. | — |
| `hub_dean_late` | Let him do it where someone could come down. | — |
| `hub_marek_boxroom` | Tell him what it costs now. | — |
| `bath_occupied` | Stop waiting for the room to be empty. | — |
| `activity_the_door` | Take the door off the hinges. | — |
| `triggered_caught_in_passing` | Stop getting dressed to come down. | — |

`v2.py:12747` falls back to the choice text when `locked_text` is absent
(`escaped_locked = (locked_text or choice_text)`), so those seven render as a greyed copy of the
choice with no explanation. The engine also supports `locked_text_threshold` (`v2.py:12786`),
which prints an explicit *"Requires …"* hint — **used zero times in this game.**

This contradicts the skill's own doctrine, `references/the-release.md:93`: *"state the current
ceiling honestly… An honest wall is a promise; a silent one is a bug report."*

**Fix shape:** eight `locked_text` strings. Under an hour of work, and it converts eight dead
grey lines into eight advertisements for the next release.

---

# 4 · The game cannot grow the way the doctrine intends

---

### N1 · The Want defines release 41 as an exhaustible list
**severity** HIGH · **layer** GAME (spec) · **status** OPEN

`the_want.md:32`:

> **What does release 41 add?** Another rung on someone who is already in the house, another
> routine turned, or a new body in the box room.

Three ladders that each terminate at a single 75 door, plus one rotating slot. That is the
narrowest possible reading of the skill's fourth commitment, and it is written into the document
every future release is checked against.

The doctrine does not require it. `SKILL.md:26` records the reference game going **25 → 61
locations and 254k → 2.24M words over eight years**; `the-board.md:29` sets the widening rate at
**6–8 locations per year, never faster than fill**. *"A release adds events, not places"* is a
per-release default measured off one six-week cycle of a mature game — not a lifetime ban on new
places, people, or plot.

**Fix shape:** rewrite Want §2 so the appetite names an engine rather than a list. Drafted and
awaiting LO's go-ahead; not started.

---

### N2 · Nothing can go wrong. There are no terminal states.
**severity** LOW · **layer** GAME · **status** OPEN · *design call, not clearly a defect*

`SKILL.md:19` notes the reference game ships **seven** terminal fail-states while remaining a
never-ending product. This game ships zero. `eviction_mode = "flag_set"` is explicitly a soft
landing (`0_systems_spec.toml:49`), and it is the only failure the game models.

A world where the worst outcome is that the terms change is a world with no downside, which
flattens every choice that is supposed to feel expensive.

---

### N3 · Only one renewal mechanism exists
**severity** HIGH · **layer** GAME · **status** OPEN

The box room. That is the whole list. Cal, Dean and Ray terminate; the house has no more rooms;
there is no outside (W1) and therefore no source of new people. Once the four 75 doors are paid,
the content stream has nowhere to come from except replacing the lodger over and over.

Depends on W1. Fixing the map is the prerequisite for fixing this.

---

# 5 · Smaller items

### C1 · Dialogue attribution — 2 unbound speakers in the opening
**severity** LOW · **layer** GAME · **status** OPEN

`gates.py` lint: `canvas_arrival#ray` and `canvas_arrival#dean` speak in a canvas that neither
binds nor names the speaker. Needs one live look at what name renders above each line.

### C2 · Typo in a location description
**severity** LOW · **layer** GAME · **status** OPEN

`1_metadata_and_locations.toml:79` — *"Four doors and a airing cupboard"*. Should be *an*.

### C3 · Ladder depth is uneven across hubs
**severity** LOW · **layer** GAME · **status** OPEN

`hub_cal_kitchen` and `hub_marek_kitchen` carry three rungs each; `hub_marek_boxroom` and
`hub_ray_frontroom` carry seven. Not wrong, but the thin ones are the two most-passed-through
windows in the day.

### M1 · 53 media slots, zero files
**severity** DEFERRED · **layer** GAME · **status** PARKED by LO 2026-08-11

49 `pool_dir` + 4 fixed, all rendering as labelled placeholders. `find-media` has never run.
Parked until after LO's first playthrough.

---

# 6 · Open questions — not yet defects

### O1 · Is 27.8% explicit far too hot, or is the denominator wrong? — **RESOLVED 2026-08-12: the denominator was wrong.**

**The comparison was never valid, and back_home is not "3× too hot."**

Settled by pulling the reference game's actual source for the first time (49.2 MB, obtained during
the study-3 economy research). `gates.py:7` states its provenance as *"1.7k → 15.6k **units**"*. The
file contains **15,587 `<tw-passagedata>` passages** — so the reference "unit" is **a passage in the
whole source**, combat, systems and UI included.

`gates.py` measures **beats in location prose only**. Two different denominators, so the 7.5–9.3%
band and back_home's 27.8% are not on the same scale and never were.

**Consequences:** the worry recorded in the increment-5 plan and carried through three CHANGELOG
entries is void — no dilution pass is owed, and the garage was correctly not watered down to chase a
ratio. What survives is that **the gate is a floor, back_home clears it, and the discrimination test
still holds** (the measured-cold game scores 4.7% on the same instrument). `gates.py` should state in
its own header that the upper comparison is not meaningful, so this is not re-litigated.

*(Original wording of the open question, kept for the record:)*
`gates.py` reports **27.8% of 270 beats** carry 3+ explicit words against a reference band of
**7.5–9.3%**. The gate is a floor and it passes. But `register.md:78` warns that a game far above
the band has usually stopped having non-sexual texture.

**Why this is a question and not a finding:** `gates.py` counts **location prose only** (the
denominator was corrected on 2026-08-10 after it was found to include `base-combat` and
`base-system`), while the reference band was derived from **whole-source unit counts**. If the
reference denominator included combat, systems and UI passages and ours does not, the two
percentages are not comparable at the top end. No reference snapshot is on disk, so this cannot
be settled from here.

**Resolve by** either re-deriving the reference ratio on a location-only denominator, or stating
in `gates.py` that the floor is a floor and its upper comparison is meaningless.

### O2 · Should the shop stay cold?
It is the one location without a traversal heat pool (7/8, gate 5 floor is 60%) and the Want
declares it *"the one room where no man wants anything from her, and that is its entire
function."* Deliberate today. Revisit only if W1 lands and the shop stops being the only exterior.

---

# 7 · Not defects — checked, and correct

Recorded so they are not re-litigated.

- **`activity_wash` requires the bathroom empty; `bath_occupied` requires it occupied.** Inverted
  presence conditions on one location, and both are right.
- **All 41 flag conditions, 193 trait conditions, 18 presence conditions and 7 wardrobe conditions
  carry `version = "1.0"`.** Zero fail-open blocks — the failure mode logged in memory as
  *conditions need version="1.0" or FAIL OPEN* does not occur here.
- **No orphaned canvases.** All 97 are reachable: 48 are located, and all 49 link-target canvases
  are referenced by a choice or a substitution.
- **Trailing interiority beats scoring 0 next to explicit beats scoring 4+.** That is
  `register.md` working as designed, not a defect.
- **All ten `gates.py` gates pass, exit 0.** Re-verified 2026-08-12.

---

## Log

| date | what |
|---|---|
| 2026-08-12 | Opened. 17 items from a read-only audit of the merged TOML, the built HTML, and `v2.py`. No files changed. |
| 2026-08-12 | +W4 (no bedrooms for Ray/Dean/Cal; the Want sells an unbuilt room), +W5 (location names as UI), +W6 (six prose references to a hall that is not in the graph). Count 17 → 20. Still read-only. |
| 2026-08-12 | +W7 (activity labels written as voice while doing the job of UI — found by LO asking what "Sit with it" does). Count 20 → 21. Still read-only. |

---

## Appendix A · What fixing the map costs, in gate arithmetic

Computed so the map discussion is not blocked by a vague fear of gate 1. Adding a location tightens
**both** the mean and the anchor ratio at once, so the street cannot be added alone.

Current: 8 locations, 36,035 words, anchor `the_front_room` 9,607 (26.7%).

**Adding one location (The Street):**

```
9 locations, mean >= 4,500      ->  total >= 40,500
anchor >= 25% of 40,500         ->  anchor >= 10,125   (+518 on the front room)
street  = 40,500 - 36,035 - 518 ->  ~3,950 words
median  = 5th smallest of 9     ->  3,947  (floor 3,000)  PASS
```

**Total cost: ~4,470 words** — inside the historical per-increment range of +1,028 to +4,484. One
release. The gate is not the obstacle.

**Adding two (The Street + Ray's Room):**

```
10 locations, mean >= 4,500  ->  total >= 45,000
anchor >= 11,250             ->  +1,643 on the front room
two new rooms                ->  ~3,660 words each
median = 6th smallest of 10  ->  3,927  PASS
```

**Total cost: ~8,965 words** — two releases.

**Recommendation:** the street alone, first. It resolves W1 and W3 (the garage's fictional outside
door becomes a real exit onto it), gives `exposure` its first consequence surface outside the
house, and is the prerequisite for N3. Ray's room is the release after, because the Want already
sold it (W4).
