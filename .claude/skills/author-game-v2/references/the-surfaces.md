# The Surfaces — where content attaches

`SKILL.md` names three kinds of content by **when they fire**: STANDING, TRIGGERED, MILESTONE.
That is one axis. This file is the other one, and without it a game can obey every other rule in
this skill and still be unplayable:

> **Which screen does this live on, and what is it FOR?**

> A location page has a shape. It is not one paragraph and then a wall of buttons, and the field
> below is what the shape is.

---

## What a room is for, measured

Full HTML of the top-30 mopoga corpus is on disk at
`~/Documents/Mopoga_Twine_Sandbox_Research_20260724/gamehtml/`. Every link label in 27 of those
games, 84,009 of them, sorted by what the button does. (25 games and 64,594 labels until the
2026-08-24 recheck; the counts below are the 25-game measurement, and every one of its
*in how many games* figures rises on 27 — the ordering does not change.)

| what the button does | uses | in how many games |
|---|---|---|
| **sleep / go to bed** | 773 | 19/25 |
| **work / take a shift / earn** | 564 | 18/25 |
| **get dressed / wardrobe** | 487 | 14/25 |
| **eat / breakfast / dinner** | 430 | 17/25 |
| **wash / shower / bathe** | 224 | 16/25 |
| exercise / train | 122 | 16/25 |
| dishes / laundry / tidy | 51 | 11/25 |
| fridge / cupboard / stock | 44 | 13/25 |
| cook | 27 | 8/25 |
| *"look around / examine"* | 232 | 14/25 |

**The browse row is the one to read carefully.** Sampled, it is not a room menu anywhere: the most
common are *"examine the cash register"* (16, one quest), *"look around"* (9), *"examine the sleeping
area"* (8). Scattered adventure-game objects, never a per-room browse list.

Four kitchens read in full, because the kitchen is the room this skill got wrong:

- **Apocalyptic World** — `Approach <her>` (only if a woman is assigned to cook here, 08:00–22:00) ·
  `Eat` (needs food in the pack **and** 30 free minutes; sets hunger 100, drops 1 food) ·
  `Talk with Blair` (only if Blair is here) · `Back`. Behind it, five random events gated on time,
  weather and who is around.
- **Become Someone** (3,277 passages) — `Have Breakfast` (06:00–11:59, once a day) · `Eat with your
  family` (evening, once a day) · `Wash the dishes` (once a day) · a portrait row of whoever is in
  the kitchen. When all three are spent: *"You don't feel hungry right now."*
- **Corpo Life** — the whole kitchen is one `if/elseif` on (who you are partnered with × time of
  day), and each branch offers two or three links: breakfast, an act with that partner, and back.
- **Degrees of Lewdity** — its farm kitchen is **341 bytes**: a line saying what is in stock,
  `<<kitchenDisplay>>` (a 40 KB cooking system shared by every kitchen in the game), `Leave`.

**Not one of them browses an object.** A kitchen in the field is a **hunger station**, a **person
magnet**, and an **event stage**.

### A bedroom, read correctly

Course of Temptation's dorm room (`YourDorm`) reads like a list of objects. Read the links and
each is the door to a system:

| link | what it really is |
|---|---|
| `Sleep` | **the sleep machine** — how the day advances |
| `Masturbate in bed` | **the solo feeder** |
| `Clothes` | **the clothing system** |
| `Food stash` | **hunger** |
| `Quickly cross hall to showers` | **hygiene, and exposure on the way** |

**The bed is not an object affording a choice. It is the door to the machine that runs the game.**
The old rule copied the shape of the sentence and threw away what was behind it. Every "object" in
that room is the entrance to something that spans the whole game.

---

## The question to ask about every piece of content

A room's menu is **exactly three kinds of thing, and nothing else.**

| kind | what it is | how many |
|---|---|---|
| **a need** | the body's clock — sleep, eat, wash, plus whatever the premise adds. Declared in `board.needs[]`, ruled by `the-meters.md` M8–M10 | one per need this room serves |
| **work** | where money comes from | one per job done here |
| **a person** | that character's hub | one per schedule row — location × window |

Anything that is none of the three does not belong on the room's list. It belongs **inside a beat**,
which is where the drying rack and the burn on the table and his chair at the end were always meant to
live — read in context, not scanned in a menu.

### Why this sizes itself, and why the cap stopped being the control

**A body needs about five things. A room contains fifty nouns.**

That is the whole difference between a tight menu and a wall of buttons. Needs are a **closed** list;
objects are an **open** one. The count falls out of a set that cannot grow, so there is nothing left
to cap.

The earlier attempt to control size failed because it capped an open list instead of closing it:

- **Gate 20's ceiling of 8** (study 6): it redistributed the menu instead of shrinking it.

Gate 20 stays as a backstop against the pathological case. It is no longer the sizing rule.

### Still true: the object test, for HUB choices only

Read a choice that is going into a **character hub's** exit block. **Is a person the object of the
verb?**

- *"Pour her coffee"* · *"Ask him for the rent"* · *"Sit closer than you need to"* → a hub rung ✓
- *"Count the till"* · *"Take a shift"* · *"Work the door"* · *"Stock the soap"* → **not a hub rung.**
  Each is work, and work is its own surface at that location.

The 23-choice failure had a hub binding **no NPC at all**, and none of its choices had a person as
its object. Every one was a work surface wearing a menu item's clothes.

---

## A place is not a catalogue

**Measured two ways. Playing five games (study 5), counting only the things you can actually DO at a
place — excluding onward travel and standing affordances like *wait for a bus*:**

```
things to do at a location ..... median 3 · max 6
```

**And parsing 18 shipped sandboxes, counting every link on a screen:**

```
median screen ......................... 2 links
median p90 ............................ 4 links
screens offering more than 12 ......... ~2% (median across the field)
```

The typical screen in a real game — the one the player is on most of the time — is **small**, and
needs + work + people lands there without being told to.

Big screens do exist. **But look at what they are: shops, wardrobes, character creation, DoL's recipe
list. Catalogues.** A catalogue is legitimately long, because its job is to list. A place you return
to every day is not one.

---

## The rules

**R1 · One canvas per (who it's aimed at × when).** A location where she both deals with a person
and does her own work is **at least two canvases**, plus a walk-in if anyone can interrupt her.
Never put work inside a character's hub.

**R2 · A room's list is needs, work and people — nothing else.**

Write the room's job first: *what does her body need here, what work is done here, who is scheduled
here.* Those three answers are the menu. A candidate that is none of the three is either a beat
inside one of them, or it belongs on a different surface entirely.

- **A need on this list is a real need**, declared in `board.needs[]` and holding a door shut when it
  goes unmet (`the-meters.md` M8/M9). A restore that gates nothing is a chore, and a chore is not a
  reason to build a screen.
- **Work is where money comes from.** One per job, not one per till-shaped noun.
- **A person is a hub**, one per schedule row, and it is judged by the object test above.
- **A menu item with HOURS says so when it is shut.** A canvas whose schedule window has closed
  simply disappears from the list — no greyed line, no reason, no hours — which reads as a broken
  game rather than a timetable. `show_when_blocked = true` plus a `cooldown_message` keeps the entry
  as a dimmed line carrying the author's own words (`v2.py:11055`, rendered at `v2.py:5143`).
  `references/the-clock.md` C5 owns the rule; this is the
  surface it lands on.

**R2c · Each row is a SYSTEM surfacing in this room — so the room list cannot be written before
the systems list is.**

Added 2026-09-01. R2 above is a **sizing** rule and it works: needs, work and people is a closed
set, so a room cannot sprawl. What it does not say is what an individual row IS.

**Read an anchor room in a shipped game and every row is a different system of the game,
appearing where that system lives:**

> ⚠️ **EVIDENCE — NOT A TEMPLATE.**
>
> `course-of-temptation` · her dorm room — *Sleep* (sleep) · *Masturbate in bed* (arousal) ·
> *Clothes* (clothing) · *Exercise* (fitness) · *Study* (grades) · *Internet* (online) · *Food
> stash* (hunger) · *Quickly cross hall to showers* (hygiene) · *Sneak out into hall* (exposure).

Nine rows because nine systems live in her room. **The count is not chosen; it falls out of the systems list, which is R2's closed-set
logic one level up.**

**The rows come from systems that describe her.** Course of Temptation reads
`has_inclination` in 218 of its 5,294 passages, so what she has become changes what a room
offers — [ClassroomMenu] `<<if $pc.has_inclination("Knowledge from the Deep")`.

⚠️ **The brake, and it is not optional.** Read carelessly, R2c invites the mirror-image
failure: declare twenty systems, get twenty rows, ship twenty dead meters —
which is `the-meters.md` W3's defect at scale, and exactly what SKILL.md's *"ask what a tired author
would build"* rules out. So:

> **A system earns its place by being read in more than one room, by more than one kind of content.**

One system that surfaces in three rooms beats three that surface in one each. **The test is not how
many systems the game has; it is whether a room has anything of its own to show.**

**No gate and no lint.** A count is satisfied by declaring traits. If a check is ever built here
it is a matched instrument first, on its own, verified against three games before any doctrine
cites it.

> ### ✅ COMPLETED 2026-09-02 — where a system is FED, and where the list itself lives
>
> Everything above stands. Two things were missing from it, and both now live in
> **`references/the-systems.md`**, which is the file R2c's opening sentence was pointing at and
> which did not exist when R2c was written.
>
> **1 · The earn-test above is about READS, and says nothing about WRITES.** Its natural reading —
> build the thing in three rooms — describes a system fed by every room, which is the kind that
> *cannot* make a room special. Measured in `family-ties`, all 50 room passages parsed: piercings
> are fed in **2** rooms and read in **117** passages, clothes **1 → 53**, the skill ladder
> **1 → 19**, while time is written by **49 of 50** rooms and the body's needs by 14.
> `the-systems.md` **SY1** names the two kinds and **SY2** carries the write side.
>
> **2 · The matched instrument this note asked for was built**
> (`~/Documents/Systems_Study_20260902/matched2.py`): field median **82** distinct leaf names at
> ≥25 references.
>
> ⚠️ **Still no gate**, and this note does not change that. What shipped is one **lint** —
> `the labels and the systems agree` — which reports and never scores, and which is safe only
> because declaring more makes its output worse rather than better.

**R3 · The walk-in — one activity deepens, the room does not widen.**

This is the largest content bucket in the field and the one v2 shipped without.
`author-game/references/lanes.md` sizes the same mechanism at ~47% of its densest arc shape.

What it looks like in the field — one game's bath (`degrees-of-lewdity`, structure only; it fails
the adults-only rule) is **one** activity with twelve outcome passages, dispatched on entry: a
person's branch when that person is there, a rare strange branch on a meter and a die, a group
barging in by day on a die, and otherwise she just washes.

And the branches are **cheap**: two of them are under 500 bytes and hand off to one shared act
engine that **1,742 other passages also call**. The richness is combinatorial, not authored.

**The same pattern is authorable in our engine** with the keys the importer already reads
(`template_import.py:2305-2325`):

```toml
# "Stock the shelves" @ the_storeroom — the odds ride the same trait as the content
substitutions = [
  { target_canvas_id = "walkin_storeroom", chance = 0.10, conditions = { … corruption lt 20 } },
  { target_canvas_id = "walkin_storeroom", chance = 0.35, conditions = { … corruption gte 20, lt 40 } },
  { target_canvas_id = "walkin_storeroom", chance = 0.70, conditions = { … corruption gte 40 } },
]
# target: ONE canvas, three [group] bands on the same trait —
#   the lowest band watches, the middle band touches, the top band acts
```

Same button. The world leans harder on it as the trait climbs. **Nothing new was needed to build that.**

> This example is deliberately a *mechanism*, not a world: what an author copies from it is three
> chance bands riding the same trait as the content, which is the thing to copy. Its ids are
> invented; it encodes no map, no cast and no room, and there is nothing in it to inherit a shape
> from.

**Three parts:**

```
the router    trigger.substitutions on the ACTIVITY — chance × conditions, rolled on entry
the branch    ONE canvas, substitution_only = true, [group] bands on the axis the odds ride
the payoff    routes into the rung that already exists, instead of authoring new content
```

**⚠️ The payoff canvas must declare a `location`.** `setup.getCanvasById` (`v2.py:3177-3191`) builds
its lookup **only** from `help_data.locationCanvases`, which is populated only for canvases carrying
`trigger.location` (`v2.py:10986-11138`). Point a substitution at a triggerless rung and it
**silently never fires** — no error, no red build, the branch just never happens.

The working shape, **verified live 2026-08-18** (probe build, three-way reachability, zero JS
errors):

```toml
[canvases.trigger]
location          = "the_kitchen"   # so getCanvasById can find it
substitution_only = true            # so it stays OUT of the room's list (v2.py:4523)
```

That canvas is then reachable **both** as a substitution target **and** from a hub choice pointing at
`<canvas_id>.<node_id>` — which is what makes the payoff shared instead of rewritten per activity.

**Where walk-ins come from is a JOIN, not a judgement.** Cross the solo activities at a location
against the `[[npcs.schedules]]` rows at that same location. She irons in the kitchen 07:00–09:00 and
Hal is in the kitchen 07:00–09:00 — *someone can walk in on her*. Nobody decides that; it is
already true in the board. The skill prints the list; the author picks from it.

**Floor: one per qualifying ROOM, not one per pair.** Filling the raw cross-product would rebuild the wall of buttons one layer
down, which is the objects mistake in a new coat.

**The branch is thin, and the size is stated because it will not hold otherwise.** DoL's are **458–473 bytes**. Target: **a tier band is one or two paragraphs plus a media
pool** — beats the length of the model beats in `register.md`, not a scene. The temptation is to write a
full encounter every time because that feels like more care; it is how this rule dies.

> ⚠️ **Do NOT try to build DoL's engine.** Its 683 KB of shared machinery — 229 KB of prose bank,
> organised **by body part** (hand / mouth / vagina / anus / penis / feet) rather than by scene —
> exists *because* it is a 51 MB text game with no video. **Our variation engine is the media pool.**
> Measured on Destroyer: its chore repeatables ship **100% identical text** and the entire variation
> budget goes to re-rolled clip pools. Copy the structure, not the word count.

**The floor is ONE branch. The rule is many.** `the walk-in floor` is an existence gate — one
substitution rule in a room and the room is covered — and that is deliberate: which pairs get built
is the author's call. But the floor is not the rule. **`Bath` is one activity with twelve outcomes**,
and that is where the "combinatorial, not authored" richness actually comes from. A host that can
produce exactly **one** outcome makes the roll decide only whether the branch or the host renders.
`lint · dispatch depth` prints it. **Three to five outcomes per host is the shape to build; one is a coin
flip.**

**⚠️ Which dice, and it is invisible in the TOML.** Two rules on one activity behave completely
differently depending on one optional field:

| | **Pattern A** — no `exclusive_group` | **Pattern B** — `exclusive_group = "<name>"` |
|---|---|---|
| the dice | **one roll per rule**, in declaration order, first match wins (`v2.py:5382-5391`) | **ONE roll**, split into cumulative buckets (`v2.py:5361-5379`) |
| substitution rate | `1 − ∏(1 − pᵢ)` — it compounds | `Σ pᵢ` — it is what you wrote |
| five branches at 0.12 | the host renders **53%** | the host renders **40%** |
| use it for | bands where **one** condition can be true at a time | a menu of outcomes that all **could** fire |

A multi-outcome dispatch wants Pattern B, because with Pattern A the odds you wrote are not the odds
that run and the room's own work gets pushed off its own screen by its texture. Bands that are
mutually exclusive by condition want Pattern A, and **must actually be exclusive** — a band reading
`ease lt 20` beside another reading `want gte 22` is two live rules, not two bands.

**⚠️ Pattern B falls through to the HOST, never to the next bucket.** If the roll claims a slot whose
target, conditions or `requires_npc` fail, `checkAndSubstituteCanvas` returns null and the activity
itself renders (`v2.py:5374-5377`). A gated bucket therefore gives its share back to the host while
its gate is shut — it does not hand it on. That is the right behaviour and it has to be written for:
the player sees the room being quiet, not the next branch along. Note that **presence gets in twice**
— an `npc_at_location` condition on the rule, and `requires_npc` on the target, which `_tryRule`
resolves against the player's current location (`v2.py:5330-5336`).

**Groups are processed before independent rules** (`v2.py:5359`), so a group added beside existing
Pattern A bands takes its slice off the top and quietly cuts how often those bands fire. Declare new
independent rules **after** the bands instead if the bands are the headline content.

**R3b · Two machines, and the content kind picks which one.**

A canvas can advance in two physically different ways, and the difference is not a style
preference — it changes what the player is looking at.

| | **cascade** | **node routing** |
|---|---|---|
| on click | the beat **appends** below the last | the passage **swaps** |
| the previous clip | still there, scrolled up | gone |
| resolved | at runtime, nested `<<linkreplace>>` | at BUILD time (`engine.md` §8) |
| use it for | a one-time scripted scene, where the text should build | a **repeatable act surface**, where the picture must change |

> **A repeatable explicit surface is a node-routed loop. A one-time scene is a cascade.**

The failure is what happens when the second is used for the first: a canvas hangs one clip
off its node lead, the player clicks down three beats to reach the act, and the clip they are looking
at is the one for the setup. `register.md` S1 has the numbers; this rule is the fix.

**The loop is a state machine, and it is the field's own repeatable shape.** In Her Own Hands'
`JamesDate1FPOptions` is a menu she drives — *Let James finger you · Give James a blowjob · Let
James eat you out · Have sex* — each act raises her meter by `random(1,5)` and shows the menu again,
and whichever meter, hers or his, reaches 100 first routes to its finish. Six parts:

```
an ACT NODE per rung          its own media pool; the passage swap is what refreshes it
a SELF-LOOP link              stay on this act, raise a hidden meter by random(8,14)
SWITCH links                  change act, set the stage trait, both directions
a FINISH link                 gated on the meter; elects which finish; routes to a finisher node
the FINISHER                  [group] blocks per finish type, then resets every loop trait
the ENTRY rung                on the hub, gated, and it resets every loop trait on the way in
```

⚠️ **Loop state is hidden numeric traits, never flags.** A flag set inside a triggerless canvas has
no located setter and **hard-fails the build** (`engine.md` §16). Declare the traits in
`[player.core_traits]` and hide them in `[[traits.labels]]`.

⚠️ **Reset on entry AND on exit.** Forget either and the next run starts mid-climb.

**Pick a shape. There are three, and one good one beats four thin ones:**

```
single-act loop    one act node, a self-loop, a gated finish
                   the cheapest loop that is still a loop — right for a service NPC or a
                   surface whose ceiling is one act

pose ladder        3-5 act nodes with switch links both ways, one pool each
                   right for a full arc; the switch links ARE the escalation the player
                   drives, and each act node is one rung of the ladder (register.md S2)

paged service      a ladder behind a paid or anonymous venue — no NPC arc, no relationship
                   state. Gate the VENUE on access and coin; charge on the FINISH, never on
                   entry, or entering and bailing is a faucet
```

### How wide the menu actually is, and which shape the field actually picks

Added 2026-08-24 from Section F. The three shapes above were right and carried no numbers.

**An act menu is two options wide.** Measured across **2,292 act menus** in nineteen shipped
sandboxes — every passage whose clickable labels include two or more classifiable acts:

| | median | p75 | p90 | max |
|---|---|---|---|---|
| act options offered | **2** | 3 | 5 | 54 |
| **span** across `talk › watch › strip › touch › oral › sex › anal › rough › group` | **1** | 2 | 4 | 8 |
| carries a finish option | | | | **9%** |

Span 1 means the options sit **one step apart** — `touch` beside `oral`, never `talk` beside `sex`.
Checked against the obvious artifact: two options can only span 0 or 1, so it was recomputed by menu
size, and menus of four to five options still sit at span 0. The narrowness is real.

**And the field mostly ships the cheap shape.** Of **61 arc hubs** — menus offering ten or more acts
— the median reaches **three** intensities, and:

```
kinds reached:   1 ×17   2 ×11   3 ×10   4 ×9   5 ×8   6 ×4   7 ×1   8 ×1
                 └──────── 47 hubs ────────┘   └────── 14 hubs ──────┘
```

**47 of 61 run one to four intensities; 14 run five or more.** `degrees-of-lewdity`'s `Widgets Pub`
is 25 acts, every one of them `talk`. `free-cities`' `Neighbor Interact` is 21 acts, every one
`rough`.

> **The single-act loop is introduced above as "the cheapest loop that is still a loop." It is also
> the one the field mostly ships. The pose ladder is the minority shape.**

That matters for how this list gets read: a shape presented as the cheap option and a shape presented
as the target are chosen very differently by a tired author. Going further, in the field, mostly means
**more variations at the same intensity** — which is `register.md`'s finding that *what varies is the
reason, not the act*, arriving from the menu side.

**Not gated and not linted.** Menu width has a median of 2 and a max of 54 for good reasons in both
directions, and hub depth is a design choice the field splits 47/14. See *What is checked* below.

**The labels inside a loop name the act** (`the-voice.md` R1). *Keep him in your mouth* · *Turn over
— give him your ass* · *Let him finish inside you*. A loop whose exits say *Continue* has thrown away
the only thing that makes the menu readable.

**Reachability is not a trap here.** Node routing resolves to a real passage at build time
(`engine.md` §8), so a triggerless loop canvas is a safe target — unlike a *substitution* target,
which must declare a `location` or it silently never fires (R3 above). Two different mechanisms, two
different rules; do not carry one's caveat onto the other.

**Lint · the act menu** counts loops against one-shot cascades among repeatable explicit surfaces. A
count, never a target.

**R3c · The ladder across visits — the menu grows, and three rungs are conversations.**
Added 2026-08-24 from Section E. **R3b above is the ladder INSIDE one visit** — cascade versus node
routing, the 3–5 act-node pose ladder, what the player is looking at while one scene runs. This is
the ladder **across** visits: the same screen, re-entered for days, its menu getting longer as one
per-person meter climbs. Different axis, adjacent rule.

The shape is measured on `friends-of-mine`'s best arc (a male-lead game, so its numbers are kept
and its lines are not): **one screen, one per-person meter from 0 to 24, forty-nine gated actions**.
The same ladder from her side, on one man's screen — rung numbers the game's, labels ours:

```
 0  Flirt with him                    10  Strip for him / Watch him jerk off
 2  Ask about his hours               12  Hand him your vibrator / Use it on his cock
 4    → conversation                  14    → conversation
 5  Ask about his divorce             15  Suck his cock / Sit on his face
 7  Visit when he's alone             17  Ride him / Bend over for him
 9    → conversation                  20  Put your wrists in his hand
                                      22  Say yes to his friend
```

The first third has no sex in it (`the-arc.md` A2): rung 2 learns when he is alone, rung 5 what he
is touchy about, and rung 7 spends what rung 2 found.

**1 · Each act is written twice, then becomes furniture.** Every rung is gated `== N`, then `== N+1`,
then survives on `>= N+2`. It is fresh for exactly two visits and standing content afterwards —
new-content highlighting with no flag to maintain. **This is what `block_pool` is for** (`engine.md`
§35).

**2 · Doing the act is what raises the meter.** The first visit writes N+1 and the second N+2, which
opens the next act. Nothing else advances him. She is not being persuaded; she does the thing she
already said yes to, twice.

**3 · Give and take arrive on one rung.** Both oral variants at 15, both toy variants at 12. The
reciprocal pair is one step, not two.

**4 · Three rungs are not acts. They are the pause, said out loud.** The indented rungs — 4, 9, 14 —
raise nothing and unlock nothing. Each sits immediately *below* the next escalation, exactly where
the player would ask why it has not happened yet:

> The neighbour leans on the doorframe and looks you up and down. "So why won't you go further with
> me?" You laugh, and your face goes hot. "Because I want it too much. I'm not going to be that easy
> for you. Not yet." *Soon, if he keeps looking at me like that.*
> — rung 14, under the jump to oral at 15

**That is the whole answer to "how does she get from no to yes".** The act simply is not on the menu
yet, which is section B's silent 71%, and three times on the climb the game spends a scene letting
her say *why not yet*, in her own voice. A no parks; only a labelled final no closes his path (`the-arc.md` A3). In a
female-lead game, In Her Own Hands' `BRLaptopPorn` grows the same way on her own history: two
categories at first, the rest opened by her dates and by how often she has watched (5, 10, 30).

The rung carries a **cost** too, checked before anything else: an energy floor with a refusal line.
His willingness gates it; her day throttles it (`the-clock.md`, `engine.md` §27).

⚠️ **One game, one character — and the shape is the minority.** Of the corpus's 61 arc hubs,
**14 reach five or more intensities and 47 do not** (R3b above). `friends-of-mine` is rank 25 and
this is its best-built arc. The
per-person shape and the shared scale behind it are field measurements across twenty games
(`the-meters.md` W6); **this ladder is a worked example and nothing more.** Not a gate, and not a
lint — the field's rung spread is 1 to 25.

**R4 · Money is not a scene.** A purchase is not a rung. Sinks belong where the thing being bought
lives — the boiler upgrade at the boiler, the paint at the frontage — or on one dedicated ledger
surface. Never scattered through a room's texture at equal weight. Eleven of the failure case's 23
front-desk choices were purchases sitting in the same undifferentiated list as *"Look up at the
board."*

**R5 · Ungated choices are the minority.** If most of a location's doors open on day one, the
ascent tiers are decoration and the wall of choices is at its worst on the day the player knows
least. The failure case ran 109 of 216 ungated.

⚠️ **A condition on a choice is usually a VARIANT, not a lock, and R5 is not a licence to gate.**
Of 27,505 conditionals wrapped around an action in 26 shipped sandboxes, **35% are variant selectors
where every branch offers something** and only **23% refuse anything at all** (`findings_B_refusal.md`
§1). Read together with R5: put a condition on the choice, then let it *change* the choice far more
often than it removes one. This is the same law H measured on reputation (2% of reads refuse) and I
measured on the body (median 10%).

**R5b · An offer has graded answers, and the no is written and priced.** Give an offer three to five
answers running from eager to refusing; write every one, and let every one move something. Our
games do the opposite: a refusal that exists at all is usually a bare link back to the menu.

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** `course-of-temptation` `[BusGrope]`, a hand on her on the bus,
> five answers: *Encourage it* (arousal, and her Disinhibition rises) · *Ignore it* · *Push their
> hand away* · *Smack that hand* (Composure +25, his control −25) · *Yell for help* (Humiliation
> +100, the scene ends). `shady-deals` `[Nightclub Quickie Caught]`, caught dealing and offered a
> deal: go with him · pay him off in stock · use the taser · push him off (only if she is fit enough)
> · *"No way."*, which means a night in custody.

**The default no is PARKED: the step comes back after a wait** (`the-arc.md` A3). In Her Own Hands
offers the soft form in the scene itself: *"Excuse yourself to think more about it and say you'll be
in touch."*

**A final no closes his path, and only on a button that says so** (A3). In Her Own Hands labels that
answer before she clicks it — *"Say 'fuck you' and leave (ends path)"* — and the route closes; the
man stays in the world.

Being refused is content too (`course-of-temptation`: friendship −50, arousal −100, *"That
certainly backfired."*). **A "no" that returns the player to an unchanged menu was never a door.**

> ⚠️ **Gate `she can say no` checks only that one exists** — it fails on zero and prints the rate
> beside the verdict (field: 2.09% of labels, 79% going somewhere the yes does not, median 262 words
> behind them). Whether a refusal is graded, written and priced is not gated.

**R5b.2 · A refusal that can never fail is a menu item.** Added 2026-08-24 after the field was
re-read on exactly this question. R5b above says the decline branch is written and paid; the field
carries a half we do not have at all.

Course of Temptation does not *grant* a refusal, it **resolves** one. *"Refuse to respond"* to a
groping in the street routes two ways off a Willpower check whose difficulty is read from the NPC
doing it (`EventWalkPassHF`) — and both branches are written, both are paid, and they move **one
meter in opposite directions**:

> **succeeds** — `Composure +25`, his `control` over her **−25**: *"It's good to know he can't get
> to you quite so easily."*
> **fails** — `Arousal +100`, `Humiliation +50`, his `control` **+25**: *"So easy."*

Not a special case: **464** skillcheck branch calls and **41** `*Resist*` passages in that game,
**360** struggle/resist/escape passages in Degrees of Lewdity.

Both ends of the range are defects, and players name both:

- **No refusal at all** is why they leave: a player quit a game after two hours because at every
  step all she could do was resist and hope (`degrees-of-lewdity`, 5 likes; paraphrased).
- **A refusal that always works** is why they get bored — three separate comments mourn a *removed*
  failure case: *"did they remove npc's not listening when you resist? ... i really enjoyed that"*
  (8 likes), *"they'd usually ignore your resistance, but now they just relent"* (6 likes) —
  `course-of-temptation`.

⚠️ **This is not a licence to hide a dice roll.** The same players resent RNG (*"the rng aspects of
this game should be seriously toned down"*), and the field's answer is that the odds are **printed
next to the choice before it is clicked** — 314 rendered `skillcheck` labels. Our engine has no
per-choice roll anyway: the mechanism is `rejection_node`, a locked choice that stays clickable and
routes to its own failure node with its own price (`engine.md` §36, and it is used by **zero**
games today). **A number bar is printed by the engine (`engine.md` §15); never fail silently.**

Still **not a gate** — three games is not a field, the same bar that stopped a gate last cycle.
(`~/Documents/Female_PC_Craft_Study_20260823/findings_J_players.md` §4)

**R5b.3 · An unchosen scene is warned, avoidable or opt-in.** Something may happen to her unchosen,
never silently: before it starts the game **warns** her in plain words, gives her **a way not to be
there**, or lets the player **switch it off**. Sex is never only a punishment. This is the rule behind
the excitement read's two instant fails (`agents.md`).

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** `course-of-temptation` tags its events by kind and gives the
> player five levels per kind; at *Warning* she is *"explicitly warned before heading into a
> particular type of content, with the option to break the event sequence"*, and the prompt reads
> *"The following passage(s) may have content falling under this tag… Do you wish to continue?"*
> (Proceed / Abort). Inside its dare-and-punish arc the man stops and asks: *"are you into doing
> these challenges, at all, on any level?"* `shady-deals`' blackmail has four other ways out, and its
> unchosen morning visit is opt-in twice over — a boss type chosen at character creation, and her
> own "with benefits" when she recruits him.

Players praise Course of Temptation as *"very consent base[d]"* and fault it because *"nothing
really bad can ever happen"*, so hard content is wanted. What they punish is a way out that does not
work: *"you're FORCED to be submissive regardless"*.

**In this engine:** gate it on a start-choice flag (R5b.4, `the-want.md` §1), say what is coming in
the choice text, and make the way out a real place with `rejection_node` (`engine.md` §36).

**R5b.4 · A content toggle is a start choice, and one kink must not crowd out the rest.** Added
2026-09-28 (IC13). The engine has no settings screen, so a toggle is a flag set on the start screen —
one per theme or per character — and every canvas of that kind reads it (the pregnancy choice in
`the-meters.md` W7b is one). Course of Temptation carries twelve kinds, each *No Warning · Aware ·
Warning · Block · Boost*; In Her Own Hands asks for a Red / Yellow / Green list of fifteen. A
passage-name recount finds a toggle in 15 of 26 top games (numbers only). Declare each in
`want.toggles[]` and put its flag in `want.player.start_choice.flags`, so `the start choice is read`
checks it; `lint · toggles declared` lists what reads each one.
- **One kink must not crowd out the rest.** Player evidence, second-hand (Round 2 quit reasons, F95):
  Cupid's Way is faulted because *"the corruption goes as far as 'white girl loves BBC' and that's
  literally it"*, and two failing games draw the same complaint (numbers only). A toggle that turns
  off the one kink a game rests on leaves nothing; spread the heat across kinds so each can be
  switched off and the game still stands.

**R5c · A locked door says why.** Added 2026-08-24. R5b.2 above reaches for
`locked_text_threshold` and `rejection_node` and stops one step short of saying what the row itself
should look like. This is that step, and it is the only rule in this file with a gate behind it.

The field's refusal has exactly two shapes and we ship a third that it does not
(`findings_B_refusal.md` §2–§4). Of 16,167 refusing conditionals:

- **71% render nothing.** The option is not there. This is the default, and it is legitimate — the
  corpus's deepest games are among its quietest.
- **28% speak**, in a **median of nine words**, and **60% of those name a handle** — a price (37%),
  *already done* (18%), a time (5%), a place (2%). Price is the field's answer; wayfinding is not.
- **2.26% show a dead label with nothing beside it**, and nearly all of that is settings and
  pagination chrome — `OptionsWidget` toggle states, `Widgets Outfits` "Previous"/"Next" greyed at
  the ends. **That third shape is what our engine renders for a story lock with no line** (`engine.md` §15).

**The shape, measured:** a refusal stands **where the action stood**, runs about **nine words**,
**names a handle**, and is **marked as the game's own voice**. Typography is a binary house
decision — patriarch italicises 86% of its refusals, zaras-school-life colours 89%,
the-hellfire-club marks none of its 631. Nobody marks a third of them.

One field game's cast page does all four at once (`patriarch`; it fails the adults-only rule, so the
shape is described and the page is not quoted). Each person is one row. While she is not available
the row holds an italic, parenthesised line saying where to find her instead; past a higher bar the
same row becomes a *different* link. The refusal occupies the row the link would have used, so the
roster never reflows and the eye learns one shape. Three states, one row, no dead end at any of them.

**Ours** *(LO decided, D2)*: a pure number lock needs nothing — the engine prints the need and her
value (`engine.md` §15), and a `locked_text` there doubles it. A story lock, mixed ones included (the
suffix never names a flag), takes `locked_text` (the reason),
`locked_text_threshold` (the bar, on click — `engine.md` §23), or `rejection_node` (a live link to a real failure node — §36, still used by zero
games). A choice gated only by `costs` needs none of them: the engine appends the requirement itself
(`engine.md` §27). Gate: **"a locked door says why"**.

⚠️ **This is the choice case only.** R2's last bullet owns the canvas-and-schedule case
(`show_when_blocked` + `cooldown_message`), and `the-clock.md` C5 owns the rule behind it. Same
instinct, different surface — do not author one where the other belongs.

**R5d · A gate asks one of two questions, and the field asks both in equal measure.** Added
2026-08-24 from section K. R5 says how *often* to gate; R5c says what a refusal *looks* like. This
is the third axis: what the condition actually tests.

Every condition in the field, classified by **shape** rather than by what the variable is about —
because every game invents its own names and a domain lexicon leaves half of them unnamed
(`findings_K_mirror.md` §1):

| shape | reads as | the field |
|---|---|---|
| **equality** | are you at this exact step — `$scene is 2` | **53%** |
| **threshold** | is your number big enough — `$lust gte 40` | **31%** |
| function | a helper decides — `visited(...)` | 13% |
| boolean | a bare flag — `!$greekroomunlocked` | 9% |
| random | a roll | 4% |

**It is the same split at both doors.** Measured over 16,167 *refusing* chains it is 45 / 40 / 17 / 7
/ 1 (`findings_B_refusal.md` §3); measured over 3,346 conditions gating an *escalation* it is 48 / 38
/ 13 / 8 / 2 (`findings_K_mirror.md` §1). Two populations, two questions, five days apart, one
distribution. **The flag chain and the meter are both load-bearing, together.**

**What this asks of an author.** An arc that runs in steps should be gated on **which step it is
on**, not on a pile of switches that each remember one thing. The field's equality is mostly a
**stage counter** — one variable that counts — and it is 24.8% of all its conditions, present in
**26 of 26 games**.

**The worked shape.** A `<npc>_loop_stage` key is set to `0 / 1 / 2 / 3` and read three ways —
`gte 3`, `eq 2`, `lt 2` — as the exclusive three-band chain that decides which ending a loop
renders. That is the field's shape. Copy it.

The cost of the flag pile is not that it breaks. Adjacent `[group]` blocks merge into one
`if/elseif` chain (`engine.md` §35), so exclusivity is enforced by the render. The cost is that
**the arc is not a thing you can read** — there is no single value to print on a card, hand to a
quest goal, or gate a later scene on. The set of flags is the only place its shape is written down.

⚠️ **And a counter nobody reads is worse than no counter.** A `<npc>_stage` key whose prefix names a
declared character is read by the engine's own stage-label system, and gate 33 carves those out on
purpose (`v2.py:5549-5554`). Any other counter written and never read by a condition — a bare
`sex_stage`, say — fails gate 33.

⚠️ **Not a gate, and not a quota.** No threshold here is defensible — a game can be built entirely on
thresholds and be correct. See "What is checked".

⚠️ **The negated form is legal on a canvas gate** — `operator = "ne"`, *"she is NOT at stage 3"*,
the shape the field writes as `$romance isnot 1`. It reads correctly in every evaluator as of
2026-08-24; before that it was true on the canvas and silently false in every hint that touched it.
**It is still rejected on a `[[quest_cards]]` condition, deliberately.** `engine.md` §37.

**R5e · A gate opens when she has earned it. An OFFER is there before she needs it.** Added
2026-09-01. R5b–R5d cover the choice she is refused and the choice she declines. This is the third
kind, the field leans on it hard, and **this skill had no word for it**.

**The defect is the offer gated on scarcity.** When taking on a burden is what opens a person, and
the choice is gated on her being short, a player who is doing fine never sees it. The field gates
the bigger burden on the opposite. Course of Temptation [WeeklyDebtPayment]: *"Then there are your
Greek house dues. You don't owe anything this week"* — shown under `!$firsttime.greekduespaid`,
never under being short.

**The field, measured 2026-09-01** (`~/Documents/Ignition_Study_20260901/`). Three of the four
corpus games that carry an obligation let the player **volunteer for a bigger one**, and **not one
of them gates it on scarcity**:

| game | the offer | what it is gated on |
|---|---|---|
| `degrees-of-lewdity` (numbers only) | take on a second person's debt — **doubles the weekly rent, permanently** | that she **knows** of the debt, never that she is short |
| `course-of-temptation` | join a Greek house — dues **plus** housing on the weekly bill, forever | `!$firsttime.greekduespaid` — that she has not yet |
| `corpo-life` | move up an apartment tier — rent 200 → 800 → 10,000 → 30,000 | that she does not own it yet |

The reference game's version (structure only) has every part doing a job. **The price is on the
button, in red** (*Doubles weekly payment*) — R5c's rule, applied to a door she is walking through
rather than one she is refused. The irreversibility is stated before she commits, which is Study
8's *close doors out loud*. And what the debt buys is **a person**: paying it opens that person's
own chain.

> **The test: can she take this when she doesn't need to?**
> If not, it is not an offer. It is a consolation prize, and she will only ever see it after she has
> already lost.

⚠️ **The obvious phrasing of this rule is wrong, so do not use it.** *"Never gate a grant on a lack"*
is false — a rescue **should** require needing rescue. The narrow claim is the one that holds: **if taking on a burden is what opens a
person, it has to be reachable while she is fine.**

**Not gated, and the measurement is why.** The mechanical signature is real —
*a choice gated on lacking X whose grant CLEARS the very lack that gated it* — but it needs two
exclusions before it discriminates at all — the ceiling pattern (`corruption +1` under
`corruption lt 40`) and once-only counters (`X lt 1 → X +1`) — and then it has almost no subject.
Unfiltered, it fires on correct work — the R4 failure exactly. The signature is recorded here so it can be built the
day it has a subject. It is not built now.

**R6 · The screen moves on re-entry — but the opener does not.** A location the player returns to
daily has to render differently each time. **It does not do this by rewriting its first sentence.**

Measured by playing the reference game and diffing repeat visits (43 turns, six visits to one cafe,
`DOCTRINE_GAPS.md` study 5 R7): the identity sentence is **byte-identical every single time**. Six
visits, six times *"You are in the Ocean Breeze Cafe."* Four other things carry the variation:

| mechanism | what it looks like |
|---|---|
| **a condition clause on the identity sentence** | *"...No one is sitting outside due to the rain"* → *"The cafe is busy, and despite the strong winds..."*. Weather and crowd — **not** progression |
| **one presence line per NPC actually there** | *"You see Sam attending to the customers."* only once you hold the job; *"Gwylan sits alone on the exterior balcony"* only when she is present |
| **the choice list itself** | 5 → 9 → 8 across six visits, as the on-ramp is replaced by the job and NPCs arrive and leave |
| **an event replacing the whole screen** | two consecutive street visits rendered a harassment scene *instead of* the location menu |

And on a repeatable **action**, variation is a scenario draw: eight cafe shifts produced **five
distinct scenarios**. R3's walk-in is mechanism 4 aimed at an activity instead of a room.

**Mechanism 5 — a pool of variants inside the beat — was missing from this list until 2026-08-23,
and it is the one the field leans on hardest.** `block_pool` picks a different one of N blocks on
every render (`engine.md` §35). Three of the four top female-PC games build **every** repeatable
sexual surface this way and none of them writes such a scene as a paragraph:

| game | its mechanism | scale |
|---|---|---|
| Course of Temptation (rank 5) | `<<switch setup.rir(0, 3)>>` | 164 named acts × 3 phrasings |
| Family Ties (rank 24) | `either("…", "…", …)` | 12 poses × ~10 lines, plus ~10 of his dialogue |

The primitive shipped with the engine, v1's corpus carried a numbered
rule for it that named this exact failure — *"the same text every morning problem"* — and v2 lost it
(`engine.md` §35).

The difference between mechanisms 4 and 5 is worth keeping straight. **A random event replaces the
screen; a variant pool changes a sentence inside it.** The first is how a room stops being the same
room; the second is how a scene survives its tenth read. A surface the player enters fifty times
needs the second, and no amount of the first substitutes for it.

**Confirmed from the player side, and unusually direct.** The top-liked criticism of
`zaras-school-life` is **the same pictures and the same scenes every day** (13 likes; paraphrased,
it fails the adults-only rule), and two other failing games draw the same complaint: the same
scenes for every character (`family-ties`, 6 likes), and a day made mostly of repeated dialogue
(`degrees-of-lewdity`, 6 likes).

**That game's developer answers it in the thread** (`zaras-school-life`, paraphrased), which is as
close to a controlled result as this study gets: a player asks for encounters written for each
person rather than one template with the names changed, and the developer replies that every
"improvement" in the changelog is exactly that — **giving every single scene its own text**.

⚠️ **The distinction that keeps this rule from being misread: repeating the LOOP is the genre,
repeating the WORDS is the defect.** Players defend the structure in the same breath as they attack
the text — *"this game is meant to be repetitive ... made to be played over and over again"*
(7 likes), *"Doesn't feel too repetitive, I'm actually **invested in the storylines**"* (5 likes).
Mechanism 5 varies the sentence inside a stable loop. It is not a licence to churn the routine, and
it never randomises what the player can reach (`engine.md` §35).

Measured across 3,479 comments on the four study games —
`~/Documents/Female_PC_Craft_Study_20260823/findings_J_players.md` §2.

⚠️ Still a **lint-side observation, not a threshold** — see the box below for why both of R6's gate
attempts failed. Four games is not a field.

**Read those four as a per-location checklist.** The finding shape is *"this location carries none
of the four"* — **not** *"this location's opener is constant."* A constant opener is correct; it is
what the reference game does on every visit. The incumbent skill says the same thing in stronger
words — `author-game/references/lanes.md:167`: *"The hub opener is ONE constant paragraph. Do NOT
tier the base node into T0/T1/T2 `[group]` blocks… Tiering the opener is a known failure"* — an arc
whose base node rewrites itself per stat band reads as N different scenes instead of one escalating
hub.

**⚠️ The pool itself can be a function of state, and the field's #2 game buys it.** Added
2026-08-28 from `~/Documents/Accumulation_Study_20260828/`. `destroyer`'s bedrooms are purchased
upgrades (30k, then 60k), and the first line of `Stepsister_s_bedroom.txt` is the whole mechanism:

```
<<if $sisbedroomlevel is 1>>     <<set _sceneOptions to [1, 2, 3]>>
<<elseif $sisbedroomlevel gt 1>> <<set _sceneOptions to [3, 4, 5, 6, 7, 8, 9]>>
```

**Buying the room takes its pool from three scenes to seven.** No new surface, no new link, no
branch — the room is where it always was and she reaches it the same way. `Stepmother_s_bedroom.txt`
is the same shape, `[1, 2, 3]` → `[3, 4, 5, 6, 7, 8]`.

Three things about that line carry the rule:

- **Scene 3 is in BOTH pools.** The upgrade is not a swap. Nothing the player had is taken away, and
  the overlap is how the field reconciles *a purchase must change something* with *never remove
  content*.
- **The room's picture changes with it** (`home/7.jpg` → `home/15.jpg`) — the purchase is visible
  before it is mechanical. Same finding as Course of Temptation's dorm, which describes her
  possessions rather than the room: *"You're the proud owner of a rock tumbler"*, four states, not
  sexual and not required (`findings_C_loop.md:75`).
- **The price carries a discount earned elsewhere** — `<<if $perk14 is true>><<set _price to _price * 0.8>>`.

⚠️ **This is authorable here today and needs no engine work** — a `[group]` carrying `conditions` can
wrap a `block_pool`, and consecutive `[group]` blocks become one `if/elseif` chain at `v2.py:14378`.
This is recorded as a measured field pattern with the engine verified, and **it is deliberately not gated**.
`the-economy.md` R1b owns the asset half.

**Mechanism 6 — who is standing there.** Added 2026-08-24. The five above change what the screen
*says* or *offers*. Course of Temptation has one that changes **who the player finds**: whether an
NPC has something on her is a term inside the person-selection predicate —
`(!rumor || setup.people.juiciest_rumor(person))` — so a reputation decides which characters turn up
in a scene rather than which options appear in it.

That is worth naming separately because it costs no new prose at all. The same hub, the same list,
a different person leaning on the doorframe, and one of them knows. Ours can express it with a
per-NPC condition (`engine.md` §8, `subject = "npc"`).
(`~/Documents/Female_PC_Craft_Study_20260823/findings_H_known.md` §3)

**The one permitted exception, and it is narrow** (`lanes.md:154-160`): banding a base node on a
**recoverable state** — paid up vs lapsed, carrying the part vs not, the copper lit vs cold — is a
*read-out*, not a tier. It reports something the player can change this minute rather than tracking
arc progress, and it is the standard place to put the reason a hidden rung is missing. Keep such
bands mutually exclusive: adjacent `[group]` blocks merge into ONE `if/elseif` chain and first match
wins.

**Floor: every location carries at least one `trigger_mode = "random"` event.** It is the cheapest of
the four to author, it is the only one that can replace the whole screen, and it is engine-cooled per
location so it cannot spam (`references/engine.md` §7).

> ⚠️ **R5 and R6 are reported as LINTS, not gates, with no threshold.** The four mechanisms above
> are what to look for.

**R7 · Every screen keeps one door. A day cap is spent every day — that is the point of it.**

R5 says most doors are gated. This is the floor under it: **one** choice on every screen carries
neither `conditions` nor `costs`, so the screen still works on the day everything else is shut.

Not a defensive habit — a consequence of how the engine renders. A choice whose conditions fail is
wrapped in `<<if setup.triggerConditionsSatisfied(…)>>` (`v2.py:13885`) and renders **nothing**: no
greyed line, no reason, no hours. And a **cost-bearing** choice counts as conditional too
(`v2.py:12827-12836`), so a screen whose only affordance costs $3 is equally empty to a player at
$0. When nothing is left the engine emits a bare `[[Continue->…]]` that fires no effects, and the
player cannot tell a spent day from a broken build.

> ⚠️ **THE CAP IS PER PERSON. THE HUBS ARE PER ROOM.** This is what makes it certain rather than
> unlucky. A character with a hub in three rooms, all reading one shared `<npc>_rung_today`, is
> spent in the first room the player visits — and a hub whose entire list is gated on that flag
> renders nothing in the other two for the rest of the day.

The fix is one line:

```toml
[[canvases.nodes.exit_block.choices]]
text                     = "Leave him to it."
targetType               = "location"
locationId               = "the_kitchen"   # the node's own location
time_progression_minutes = 5
```

Write it to **close the beat**, not to bail out of it: the NPC has just spoken, so *"Say it can wait,
and go."* answers him and *"Leave"* does not.

> ⚠️ **NOT every all-conditional screen is a dead end**, and `author-game/references/engine-reference.md:297`
> is right that you should not add a fallback "just in case" — it would double-render. That advice is
> scoped to conditional **routing**, where the branches are exhaustive by construction
> (`stealth gte 10` / `lt 10 + fighting` / `lt 10` catch-all) and one always passes.
> The rule here is for **independent budgets that deplete together**, which is what a day cap and a
> price both are.

**R7b · Two shapes, and a game needs both: a POOL at a place, a CHAIN on a person.** Added
2026-09-03, read in source.

`zaras-school-life` runs both at once (numbers only; it fails the adults-only rule), and neither
substitutes for the other.

**The POOL.** Fifteen incidents at one place look like a fifteen-step ladder and are not: **all
fifteen carry the identical gate**. They are fifteen *different situations at one place*, rolled;
the same game runs 16, 14, 10, 9 and 8 at five other places. Course of Temptation's walk between
buildings is the passing game's version: 151 `EventCampusWalk*` passages, setups rather than acts
(`the-arc.md` A9).

Inside each setup a band on her meter decides how she plays it, so twenty visits is *fifteen
situations × two or three bearings*. **No rung has to follow any other rung, which is why
a pool cannot flow stupidly** — there is no staircase to fall off. This is A9 of `the-arc.md`
seen from the surface side.

**The CHAIN.** The same game runs eight of them, 16 to 72 passages each; **274 quest passages** in
a 785-passage game. A chain is A1's numbered ladder, ending by converting into a repeatable surface.

> **A chain alone is a questline: finish it and the person is dead content. A pool alone is a slot
> machine: nothing builds. Both together, and the place keeps producing situations while the
> people keep advancing.**

⚠️ **A chain alone is half the answer** (`lint · the arc ladder` prints the chains). The pool is
the cheaper half — its unit is a *setup*, not an act, and A9 already says the setups span the
whole meter range. When a place is worth returning to and you cannot say why, it is usually
missing its pool.

**R7c · Four scene kinds the field keeps.** Added 2026-09-28 (IC13). A menu to pick from, never a
quota and never a gate. Field: a passage-name recount of 26 of the mopoga top 30 finds dates in 20,
flirting in 12, gifts in 9 and danger in 12 (numbers only).
- **A date.** He takes her somewhere, and the outing pays the relationship meter. Course of
  Temptation [EventFirstDateMutuallyGood]: *"This was a great first date!"* In Her Own Hands
  [JamesDate1] makes the getting-ready its own screen.
- **A tease that pays off inside the arc** (`the-arc.md` A13). The tease is a step, and a later step
  spends it. In Her Own Hands' Shaun: [LRSh_Sweatpants_Flirt1] *"You don't get to touch . . . yet."*
  counts `$xr.sh.swt`, and at 6 the chain turns into the standing [LRSh_Sweatpants_Flirt5]. Cupid's
  Way's Aiden: [aiden msg1] *"you here to tease me again?"*
- **A gift.** An item given or received that moves a meter by whether he likes it. Course of
  Temptation [GiveGiftResult]; In Her Own Hands [BobbyBRGift1]. Built with items and `itemEffects`.
- **Danger.** A random-trigger canvas with a threat and a written way out, and R5b.3 applies: warned,
  avoidable or opt-in. Shady Deals [Gangs Attack] (fight, seduce, or lose); Course of Temptation
  [EventCampusSneakCaughtAssault] *"Run while you can"*.

**R8 · A person owns a corner of the world.** Added 2026-08-24 from
Section G.

Twenty-five field games were read in source to find what actually separates one character from
another. A log-odds pass over each speaker's dialogue answers it, and the answer is **not diction**:

In `destroyer` (numbers only) each character's most distinctive words are the words of their
corner of the world: a doctor's are the clinic's, an administrator's are votes and levies, one
relative's are the house and dinner, another's are money and shopping. `sluttown-usa` (numbers
only) splits the same way and **twice** — each person has their own subject *and their own
supporting cast* of two or three people.

**A character is not a temperament with a name on it. He is a different part of the world, and he
talks about the part he is in.** A trait system cannot buy this; only the design can.

> ### What owning a subject sounds like — a boxing gym, four men
>
> Teodor speaks in numbers (*"Sixty-one point four, kid. You ate three hundred grams you didn't tell
> me about."* · *"Nine rounds on the pads, not eight. I counted. I always count."* · *"Every number on
> this wall belongs to somebody who lied to me once."*), Otis in water and distance (*"Bottle. Drink
> all of it before you tell me you're fine."* · *"Six miles to the harbor light and six back. Don't
> walk any of it."* · *"You sweated a litre in there. Where do you think it comes back from?"*), Ruben
> in binary rules (*"You're in the ring or you're off my floor. Nobody leans on my ropes."* · *"Gloves
> on, you listen. Gloves off, you go home."* · *"Either you want the fight or you want to be seen
> wanting it. Pick."*), Casimir to an audience (*"Everybody watching? Good. Watch her drop that right
> hand again."* · *"Half this room is here to watch you sweat, love. Give them the good side."* ·
> *"Louder! The back row paid to hear you hit something."*).

So the rule is **his own subject and his own people** — a domain he talks about that nobody else
talks about, and at least one named person offscreen who belongs to him and not to the crew.

**Where the tag line fits.** `[ui.cast_page]`'s `tags` field (`engine.md` §34) is the four-word
compression of this — *"Manipulation | Attention | Writing | Oriental Food"* tells you what
Chloe is about before you have met her. It is a **summary of a corner she already owns**, not a
substitute for owning one. Four words on a card cannot rescue a man who has no domain.

---

## What this costs, and why it is worth it

Splitting one 23-choice hub into six surfaces is not more writing — it is the **same** writing on
six screens instead of one. What changes is that each screen can then have its own opener, its own
banding, and its own gate, which is the whole reason the engine has located canvases at all.

And it fixes a problem that looks unrelated. A location that must fill 19 buttons gets 19 *small*
things, because nobody can write nineteen substantial scenes at a front desk.

**Wide and thin is a structural choice, not a writing outcome.** This file is where it gets made.

**The needs layer buys something the object layer never could: a reason to be in the room.** A player
walks into a kitchen because they are hungry, not because there is a drying rack in it. And a need that
shuts a door — *filthy means she cannot leave the house* — turns a chore into a plan.


---

**R9 · An act that returns her to an unchanged menu is an act that never happened.** Added
2026-09-02, from LO reading a build: *"Some exit choice have an action but does not have the follow
up node, it simply exit to the location."*

A choice with `targetType = "location"` that carries `effects` fires them, shows a **2-second numeric
toast** (`engine.md` §45), and puts the player back on the room screen. So the click has three parts
and the middle one is missing:

| | |
|---|---|
| before the click | written — he is at the counter, the radio is low, two mugs are out |
| **the act itself** | **nothing** |
| after the click | `+6 Dale's Relation · +120 Money`, for two seconds |

*"Ask him for the dues before you're short."* — she asks a man for money, he gives her £120, he wants
her more for it, and the game shows her a receipt.

**The seam is not the target, it is whether the choice does anything.** R7's leave-link is the same
TOML shape and it is correct: it fires **no effects**, it exists so a spent screen still has a door,
and it is navigation. A location exit that grants a trait, sets a flag or charges a cost is an **act
that happens to end in a room**, and an act needs a screen. Read the two rules together and the test
is one line: *does this choice change her?*

**This is the general case of two rules already written.** R5b says it about refusals — *"a 'no' that
returns the player to an unchanged menu is a door that was never really open"* — and `the-arc.md`
A10/A11 say it about the end of an act — a finish node with an empty `exit_block`, or a `Stop.`
choice that routes at a reset node and prints nothing. R9 is the same sentence with
*act* in place of *no*, and it is what those three were each seeing one corner of.

⚠️ **Nothing here owned it, which is why it shipped.** `the-arc.md`'s ownership table routes *which
screen* to this file, *how the prose reads* to `register.md`, and *the steps between* to itself.
**"Whether there is prose once they click" was in none of the three rows.**

**A WORK rung may resolve to a toast. A rung aimed at a PERSON, or at her own body, may not.**
`the-economy.md` R5 teaches this exact template as *"what a paying rung actually looks like"* and it
is right for work — nobody needs a paragraph about stacking shelves. It never drew the distinction,
the word *person* does not appear in that file, and so the job template got used on people. LO, on
being offered a carve-out for sleeping, washing and eating: *"Nope nothing should be skipped. Wash
bath are content in themselves."* The bath, the bed and alone-with-the-door-shut are **surfaces**.

### The repair is one node, and it is cheaper than it sounds

Route the choice at a node with `targetType = "node"`, write what happened, and exit from there.

- **Several gated choices can share ONE banded outcome node.** A work activity can route **four**
  rung-gated choices into a single `shift` node whose `group` bands render what the night was
  actually like. The reason is the engine's: *"Choice effects fire on CLICK and exit effects fire on
  RENDER, and per-rung pay/relation cannot live on a single shared exit at all."*
- **Where each thing sits.** `costs` → **the choice, always** (it is a gate as much as a price). Per-branch effects → the choice. Uniform
  payload and the clock → the target node's `exit_block.config`. A day-cap flag → the **located**
  choice, never inside the triggerless canvas, which has no located setter and hard-fails the build.
- **Staying fresh**, because most of these sit on repeatable surfaces: `group` bands keyed on the
  meter the surface climbs, plus a `pool_dir` pool — the house style. `block_pool` works too.
  ⚠️ **Node prose has no `text_variants`.** The key exists only on a **choice**, where it swaps the
  button label: a list of `{ text, conditions }`, first match wins, the base `text` otherwise
  (`template_import.py:2535-2573`; rendered as a `<<set _cv>>` chain at `v2.py:13920-13934`).
  Variant labels are static strings — an `@npc` token inside one does not resolve.
- **Video on outcome nodes, images on hubs.**

### The extreme case, which is a gate

⚠️ **A node nothing points at is built and cannot be reached.** A canvas that authors three nodes
and links one falls through to the engine's default `[[Continue->Location_…]]` from `base`, and the
other two are in the HTML with no way in.

**Every node you write gets an inbound edge in the same edit.** A node is reached by a
`targetType = "node"` choice, a `rejection_node`, or an `exit_block.config.destinationId` — and
**not** by `[[canvases.connections]]`, which parses, persists and is never read by the generator
(`game_graph.py:397`).

### What this costs

The field range is **0% to 68%** of choices, so there is no threshold here that would not fail a game
for obeying the doctrine. The general case
is therefore a **lint that cannot fail anything**; only the extreme case — a node nothing points at —
is a gate (`every authored node is reachable`).

## What is checked

| | |
|---|---|
| **Gate 20 · a place is not a catalogue** | the backstop against the pathological case: no repeatable location-bound canvas offers more than 8 decisions. **No longer the sizing rule** — R2's closed list is |
| **Gate 29 · a need shuts a door** | every entry in `board.needs[]` is read by at least one condition somewhere in the game. `the-meters.md` M9 |
| **Gate 30 · the walk-in floor** | a location with at least one repeatable solo activity **and** at least one NPC schedule row carries at least one `substitutions` rule. R3 |
| **Gate 37 · a spent day still has a door** | no screen whose every choice is day-capped or priced lacks one choice free of **both** `conditions` and `costs`. Mirrors the engine's own `has_unconditional_choice`, so the gate and the runtime cannot disagree. R7 |
| **Gate 42 · a locked door says why** | a number lock carries no `locked_text` (the engine prints its need); every other `show_when_locked` choice carries a `locked_text`, a `locked_text_threshold` or a `rejection_node`. A choice gated only by `costs` is exempt — the engine writes that message itself (`engine.md` §27). R5c |
| **Lint · noun-only buttons** | the share of room-list labels that open on a determiner and name no verb. A number, not a bar — `the-voice.md` R1 |
| **Lint · the browse share** | the share of repeatable room canvases whose entire click changes nothing but the clock |
| **Gate 46 · she can say no** | at least one choice in the whole game declines an offer. Fails only on zero — the rate is printed and never judged. R5b's existence half; its quality half stays ungated |
| **Lint · she permits or she acts** | the share of choices opening `let`, and the share inside sex loops. Reported against the field's verb profile, never judged |
| **Lint · the act menu** | repeatable explicit surfaces split into node-routed loops and one-shot cascades. A count, never a target — R3b |
| **Gate 48 · every authored node is reachable** | no node outside a canvas's entry has zero inbound edges. `world reachable` one level down: that asks whether a ROOM can be walked to, this whether a SCREEN can be opened. R9 |
| **Lint · the act between the click and the number** | location exits that fire effects and show no screen, with the game-time they burn. A LIST, never a score — the field runs 0–68% — R9 |

**What a tired author writes to satisfy gate 42 on a story lock, checked before it landed.** The answer is
`locked_text = "Not yet"` — a bare negative with no handle. That is a real shape in the field:
13% of its spoken refusals are exactly that, and it is still strictly better than the mute label,
which is 2.26% and almost entirely UI chrome. **The fig leaf here produces something the field
actually ships**, which is why this rule got a gate and R5b did not. What the gate cannot judge is
whether the nine words are any good; R5c above is the part that has to be taught.

**R3b's measured numbers join the not-gated list, and the reason is in the spread.** Act-menu width
runs from 2 to 54 and hub depth splits 47/14 across the field; both are design choices with working
games on either side. Section F recorded them and proposed no check.

**R5d joins the not-gated list too, and for the cleanest reason of the set: there is nothing to
fail.** A game built entirely on thresholds is not broken. The field's 53/31 split is a description of how the genre encodes state, not a target
share, and the moment it became a percentage to hit it would be an invented threshold. Section K
measured it and proposed no check.

**R1, R2's judgement half, R4, R5b and R8 are deliberately not gated.** Whether *"Turn somebody away"* is
aimed at a person or at the room is a judgement a parser cannot make, and a proxy check for it would
pass exactly the game that failed. They stay a board-phase and authoring-time discipline. R5b joins
them for a different reason: it rests on four games read in source, which is an observation, not a
field. ⚠️ **That last clause is now half-true and the half matters**: R5b's
quality half is still ungated for exactly this reason, but its existence half was re-measured across
all 25 corpus games on 2026-08-28 (84,458 labels) and IS gated — see the box under R5b above.

**R8 joins them for a third reason, and it is the strongest of the three: the field disagrees with
itself.** `degrees-of-lewdity` is rank 7 with 15,626 passages, and its NPC record reads `penis`
2,198 times against `name_known` **27** — `lefthand`, `righthand`, `stance` and `distance` are a
limb-by-limb struggle machine. Its people are not characters at all; they are bodies in a physical
simulation, and that is a second working answer to the same problem. A gate mandating that
characters be differentiated *as people* would fail the seventh-ranked game in the corpus.

> ⚠️ **Before adding a gate here, apply `SKILL.md`'s operating rule:** ask what a tired author would
> build to satisfy it, and check that the answer is the thing you actually want.
