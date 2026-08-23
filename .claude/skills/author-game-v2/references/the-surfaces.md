# The Surfaces — where content attaches

`SKILL.md` names three kinds of content by **when they fire**: STANDING, TRIGGERED, MILESTONE.
That is one axis. This file is the other one, and without it a game can obey every other rule in
this skill and still be unplayable:

> **Which screen does this live on, and what is it FOR?**

> Measured failure this exists to prevent. A game authored entirely to v2 doctrine put **23 choices
> on its front desk, 19 on its street, 19 in its changing room** — one paragraph and then a wall of
> buttons, at every location, with 109 of its 216 doors open on day one. It scored **18/18**.
> Nothing in the skill said a location page had a shape, so the author invented one.
>
> ⚠️ **The first fix for that was wrong, and this file is its second draft.** The answer written in
> 2026-08-10 was *declare the objects in the room and hang a choice off each one.* That produced
> `the_allowance`, whose kitchen offers **Look round the kitchen · Sit out on the back step · Come
> down in what you slept in · Get the washing in off the airer · Ask for more than you need** — five
> buttons, three of which have a free duplicate inside the first, in a game that scored 26/27. LO
> read that list cold and said *"objects in a room, and then things can be done in that room, will
> always end up with a mess like this, which means nothing."* He was right. The rest of this file is
> the correction, and it is measured against 25 shipped sandboxes rather than reasoned from first
> principles.
>
> *(An **airer** is a folding clothes-drying rack. That gloss is here because this file quotes the
> label four more times and `register.md` now requires a word like it to be taught on first use —
> including by the skill itself. The button text is left verbatim: it is what the game shipped.)*

---

## What a room is for, measured

Full HTML of the top-30 mopoga corpus is on disk at
`~/Documents/Mopoga_Twine_Sandbox_Research_20260724/gamehtml/`. Every link label in 25 of those
games, 64,594 of them, sorted by what the button does:

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
  day), and each branch offers two or three links: `Have Breakfast` · `Fuck Karen` · `Back`.
- **Degrees of Lewdity** — its farm kitchen is **341 bytes**: a line saying what is in stock,
  `<<kitchenDisplay>>` (a 40 KB cooking system shared by every kitchen in the game), `Leave`.

**Not one of them browses an object.** A kitchen in the field is a **hunger station**, a **person
magnet**, and an **event stage**.

### The worked example this file used to print, read correctly

This file previously showed DoL's bedroom as *"what correct looks like"* and read it as *choices hang
off objects in the prose*:

```
Your bed takes up most of the room.
   Strip and get in bed
Your clothes are kept in the creaky wardrobe.
   Wardrobe
   Mirror
```

Read the actual passage and the standing links are:

| link | what it really is |
|---|---|
| `Strip and get in bed` | **the sleep machine** — how the day advances |
| `Masturbate in bed` | **the solo feeder** |
| `Wardrobe` | **the clothing system** |
| `Sex toys` | **a system** |
| `Mirror` | **the body / appearance system** |

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
which is where the airer and the burn on the table and his chair at the end were always meant to
live — read in context, not scanned in a menu.

### Why this sizes itself, and why the cap stopped being the control

**A body needs about five things. A room contains fifty nouns.**

That is the whole difference between a tight menu and a wall of buttons. Needs are a **closed** list;
objects are an **open** one. The count falls out of a set that cannot grow, so there is nothing left
to cap.

Both previous attempts to control size failed for the same reason — they capped an open list instead
of closing it:

- **Gate 20's ceiling of 8** (study 6): a game built after the cap existed put **19 of its 30 screens
  at exactly 8** and shipped the *same 213 choices* as the 23-choices-on-one-desk game the cap was
  written to fail. It redistributed the menu and pushed the median *up* from 7 to 8.
- **R2b's "derive the count from the objects"**: `the_allowance` declared six objects in its kitchen
  and got a six-choice browse screen **on top of** four activities that already covered the same
  things. Nine near-verbatim duplicate pairs across five rooms.

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
  **No game in this repo has ever used it.** `references/the-clock.md` C5 owns the rule; this is the
  surface it lands on.

**R3 · The walk-in — one activity deepens, the room does not widen.**

This is the largest content bucket in the field and the one v2 shipped without. **10 substitution
rules across 791 canvases in five games**, against `author-game/references/lanes.md`, which sizes the
same mechanism at ~47% of its densest arc shape.

What it looks like in the field — DoL's `Bath` is **one** activity with twelve outcome passages,
dispatched on entry:

```
if   Robin is here and not traumatised   → the Robin branch (forks on romance / dom / YOUR stats)
elif hallucinations >= 2 and dice        → the slime
elif daytime and dice                    → a group barges in
else                                     → you wash
```

And the branches are **cheap**. `Bath Molestation` is **458 bytes with zero prose** — six
configuration lines handing off to `<<actionsman>>`, the shared engine that **1,742 other passages
also call**. `Bath Robin Tease` is **473 bytes and three sentences**. The richness is combinatorial,
not authored.

**The same pattern already ships in our engine**, in `games/vesper`:

```toml
# "Work the floor" @ renner_depot — the odds ride the same trait as the content
substitutions = [
  { target_canvas_id = "walkin_renner_depot", chance = 0.10, conditions = { … corruption lt 20 } },
  { target_canvas_id = "walkin_renner_depot", chance = 0.35, conditions = { … corruption gte 20, lt 40 } },
  { target_canvas_id = "walkin_renner_depot", chance = 0.70, conditions = { … corruption gte 40 } },
]
# target: ONE canvas, 2.3 KB, three [group] bands on the same trait —
#   watches from the bottom of the ladder → finds reasons to touch her → backs her into the shelving
```

Same button. The world leans harder on it as he rots. **Nothing new was needed to build that.**

> This is a **validated** example and it is deliberately a *mechanism*, not a world: what an author
> copies from it is three chance bands riding the same trait as the content, which is the thing to
> copy. It encodes no map, no cast and no room. `SKILL.md`'s rule — an example outranks every rule
> beside it, so it goes in last, after it is validated, or not at all — is satisfied on both counts:
> it shipped and it was measured, and there is nothing in it to inherit a shape from.

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
Martin is in the kitchen 07:00–09:00 — *someone can walk in on her*. Nobody decides that; it is
already true in the board. The skill prints the list; the author picks from it.

**Floor: one per qualifying ROOM, not one per pair.** The raw cross-product is 40 pairs for
`the_allowance` and 49 for `seventh_day`. Filling it would rebuild the wall of buttons one layer
down, which is the objects mistake in a new coat.

**The branch is thin, and the size is stated because it will not hold otherwise.** Vesper's is
**2.3 KB**; DoL's are **458–473 bytes**. Target: **a tier band is one or two paragraphs plus a media
pool** — the same ~35–40 words per beat as everything else, not a scene. The temptation is to write a
full encounter every time because that feels like more care; it is how this rule dies.

> ⚠️ **Do NOT try to build DoL's engine.** Its 683 KB of shared machinery — 229 KB of prose bank,
> organised **by body part** (hand / mouth / vagina / anus / penis / feet) rather than by scene —
> exists *because* it is a 51 MB text game with no video. **Our variation engine is the media pool.**
> Measured on Destroyer: its chore repeatables ship **100% identical text** and the entire variation
> budget goes to re-rolled clip pools. Copy the structure, not the word count.

**The floor is ONE branch. The rule is many.** `the walk-in floor` is an existence gate — one
substitution rule in a room and the room is covered — and that is deliberate: which pairs get built
is the author's call. But the floor is not the rule. **`Bath` is one activity with twelve outcomes**,
and that is where the "combinatorial, not authored" richness actually comes from. Measured across
this repo on 2026-08-23, every host in three of the seven dispatching games could produce exactly
**one** outcome, so the roll only ever decided whether the branch or the host rendered. `lint ·
dispatch depth` prints it. **Three to five outcomes per host is the shape to build; one is a coin
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

The measured failure is what happens when the second is used for the first: a canvas hangs one clip
off its node lead, the player clicks down three beats to reach the act, and the clip they are looking
at is the one for the setup. `register.md` S1 has the numbers; this rule is the fix.

**The loop is a state machine, and it is the field's own repeatable shape.** `destroyer:ginablow` is
one clip from a pool of eight, four words of text, and five exits — *Keep blowing · Pound her ass ·
Pound her pussy · Cum · Go back*. The player drives the escalation. Six parts:

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

**The labels inside a loop name the act** (`the-voice.md` R1). *Keep him in your mouth* · *Turn over
— give him your ass* · *Let him finish inside you*. A loop whose exits say *Continue* has thrown away
the only thing that makes the menu readable.

**Reachability is not a trap here.** Node routing resolves to a real passage at build time
(`engine.md` §8), so a triggerless loop canvas is a safe target — unlike a *substitution* target,
which must declare a `location` or it silently never fires (R3 above). Two different mechanisms, two
different rules; do not carry one's caveat onto the other.

**Lint · the act menu** counts loops against one-shot cascades among repeatable explicit surfaces. A
count, never a target.

**R4 · Money is not a scene.** A purchase is not a rung. Sinks belong where the thing being bought
lives — the boiler upgrade at the boiler, the paint at the frontage — or on one dedicated ledger
surface. Never scattered through a room's texture at equal weight. Eleven of the failure case's 23
front-desk choices were purchases sitting in the same undifferentiated list as *"Look up at the
board."*

**R5 · Ungated choices are the minority.** If most of a location's doors open on day one, the
ascent tiers are decoration and the wall of choices is at its worst on the day the player knows
least. The failure case ran 109 of 216 ungated.

**R5b · The choice to decline is written at full length, and it pays.** Not a gate — four games is
not a field — but it is unanimous across the four, and our games do the opposite: a refusal that
exists at all is usually a bare link back to the menu.

Zara's School Life writes a family dinner the player re-enters (`meal event1`, 78,621 chars) with
six corruption rungs inside it. The branch where she declines is a full paragraph and **grants
`+60 Energy`**:

> "Zara gave a small, almost imperceptible shake of her head, as if to physically dislodge the
> intrusive fantasy. She took a slow, deliberate sip of water… The dangerous thoughts were sealed
> behind a mental door, leaving only the taste of food and the sound of ordinary laughter around
> the table. **For now, the fantasy remained just that.**"

Course of Temptation charges in the other direction. Walking into an occupied shower uninvited and
being refused costs `friendship -50 -60` and `Arousal -100`, and the scene has to be walked out of:

> "'What the hell are you doing in here?! Get out!' […] It seems prudent to beat a hasty retreat.
> 'Um, sorry!' you say, backing out into the dressing area. You hastily put your clothes back on and
> duck out of the stall. **That certainly backfired.**"

**Read together: saying no is content, and pushing and being refused is content.** A "no" that
returns the player to an unchanged menu is a door that was never really open.
(`~/Documents/Female_PC_Craft_Study_20260823/findings_D_writing.md`)

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

- **No refusal at all** is why they leave — *"I lost interest in playing it after only 2 hours
  because at almost every step there is a man who wants to use my body, and all I can do is try to
  hit him or cover my holes and hope"* (`degrees-of-lewdity`, 5 likes).
- **A refusal that always works** is why they get bored — three separate comments mourn a *removed*
  failure case: *"did they remove npc's not listening when you resist? ... i really enjoyed that"*
  (8 likes), *"they'd usually ignore your resistance, but now they just relent"* (6 likes).

⚠️ **This is not a licence to hide a dice roll.** The same players resent RNG (*"the rng aspects of
this game should be seriously toned down"*), and the field's answer is that the odds are **printed
next to the choice before it is clicked** — 314 rendered `skillcheck` labels. Our engine has no
per-choice roll anyway: the mechanism is `rejection_node`, a locked choice that stays clickable and
routes to its own failure node with its own price (`engine.md` §36, and it is used by **zero**
games today). **State the bar with `locked_text_threshold`; never fail silently.**

Still **not a gate** — three games is not a field, the same bar that stopped a gate last cycle.
(`~/Documents/Female_PC_Craft_Study_20260823/findings_J_players.md` §4)

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

Counted across every `toml_phases/*.toml` here: **the_long_summer 46 · under_one_roof 14 ·
vesper 6 · every v2 game 0.** The primitive shipped with the engine, v1's corpus carried a numbered
rule for it that named this exact failure — *"the same text every morning problem"* — and v2 lost it
(`engine.md` §35).

The difference between mechanisms 4 and 5 is worth keeping straight. **A random event replaces the
screen; a variant pool changes a sentence inside it.** The first is how a room stops being the same
room; the second is how a scene survives its tenth read. A surface the player enters fifty times
needs the second, and no amount of the first substitutes for it.

**Confirmed from the player side 2026-08-24, and this one is unusually direct.** The complaint is
the top-liked criticism of `zaras-school-life`:

> *"The biggest problem with this game its so boring doing the same thing every day too much loop no
> nothing new — **same gifs every time you do same things every single time**"* (13 likes)

and it is named precisely in two other games — *"the game is pointless if you just use the **same
scenes for every character**"* (`family-ties`, 6 likes), *"a school day can be 50 inputs with **~48
of those being repeat dialogue**"* (`degrees-of-lewdity`, 6 likes).

**Zara's developer answers it in the thread**, which is as close to a controlled result as this
study gets. A player asks for *"originally written encounters instead of ones based on a format with
names changed"*; the reply:

> *"whenever you see 'improvement' in the changelog, assume i have done what you suggested above,
> **trying to give every single scene a different text**."*

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

**Mechanism 6 — who is standing there.** Added 2026-08-24. The five above change what the screen
*says* or *offers*. Course of Temptation has one that changes **who the player finds**: whether an
NPC has something on her is a term inside the person-selection predicate —
`(!rumor || setup.people.juiciest_rumor(person))` — so a reputation decides which characters turn up
in a scene rather than which options appear in it.

That is worth naming separately because it costs no new prose at all. The same hub, the same list,
a different person leaning on the doorframe, and one of them knows. Ours can express it with a
per-NPC condition (`engine.md` §8, `subject = "npc"`) — every game in this repo already uses per-NPC
conditions, and none uses one this way.
(`~/Documents/Female_PC_Craft_Study_20260823/findings_H_known.md` §3)

**The one permitted exception, and it is narrow** (`lanes.md:154-160`): banding a base node on a
**recoverable state** — paid up vs lapsed, carrying the part vs not, the copper lit vs cold — is a
*read-out*, not a tier. It reports something the player can change this minute rather than tracking
arc progress, and it is the standard place to put the reason a hidden rung is missing. Keep such
bands mutually exclusive: adjacent `[group]` blocks merge into ONE `if/elseif` chain and first match
wins.

**Mechanism 4 is the one games actually drop.** Measured across the field 2026-08-16:

| | vesper (v1) | back_home | steam | forty_miles | seventh_day |
|---|---|---|---|---|---|
| `trigger_mode = "random"` canvases | **14** | 0 | 0 | 8 | **0** |
| conditional (`group`) blocks | 138 | 102 | 91 | 0 | **0** |

**Floor: every location carries at least one `trigger_mode = "random"` event.** It is the cheapest of
the four to author, it is the only one that can replace the whole screen, and it is engine-cooled per
location so it cannot spam (`references/engine.md` §7).

> ⚠️ **R5 and R6 are reported as LINTS, not gates, and the reason is worth keeping.** Both were
> built as gates first. Neither threshold survived being checked:
>
> - **R5's ceiling had to be invented.** At 50% one game passes at exactly 50.0% while another
>   fails at 52% — that is noise being scored, not a measurement.
> - **R6 was measuring a practice nobody follows.** The original rule said *"band the opener on
>   whichever tier the location serves"*, and our TOML test asked whether the opener carries a
>   conditional block. Our games scored **0/22, 2/12, 11/29** — against a reference game whose
>   openers are *never* conditional. The 86% field figure from built HTML was `<<if>>` counting
>   engine plumbing, so neither number measured what the rule claimed.
>
> The four mechanisms above are what to look for instead. Still a lint, still no threshold —
> what changed is that we now know **what** to count.

**R7 · Every screen keeps one door. A day cap is spent every day — that is the point of it.**

R5 says most doors are gated. This is the floor under it: **one** choice on every screen carries
neither `conditions` nor `costs`, so the screen still works on the day everything else is shut.

Not a defensive habit — a consequence of how the engine renders. A choice whose conditions fail is
wrapped in `<<if setup.triggerConditionsSatisfied(…)>>` (`v2.py:12806`) and renders **nothing**: no
greyed line, no reason, no hours. And a **cost-bearing** choice counts as conditional too
(`v2.py:12827-12836`), so a screen whose only affordance costs $3 is equally empty to a player at
$0. When nothing is left the engine emits a bare `[[Continue->…]]` that fires no effects, and the
player cannot tell a spent day from a broken build.

> ⚠️ **THE CAP IS PER PERSON. THE HUBS ARE PER ROOM.** This is what makes it certain rather than
> unlucky. `off_season` gave Ewan three hubs — the yard, the harbour, the arcade counter — all
> reading one shared `ewan_rung_today`. Spending it at the yard at 09:00 emptied the other two for
> the rest of the day, and their entire list was that one flag. Ten of its ten hubs did this, and
> its author walked into one and could not tell whether his own game was broken (2026-08-23).

The fix is one line, and every other game in this repo already ships it — eleven day-capped hubs
across `last_call` and `mothers_place`, eleven leave-links:

```toml
[[canvases.nodes.exit_block.choices]]
text                     = "Leave him to it."
targetType               = "location"
locationId               = "the_chip_shop_flat"   # the node's own location
time_progression_minutes = 5
```

Write it to **close the beat**, not to bail out of it: the NPC has just spoken, so *"Say it can wait,
and go."* answers him and *"Leave"* does not.

> ⚠️ **NOT every all-conditional screen is a dead end**, and `author-game/references/engine-reference.md:297`
> is right that you should not add a fallback "just in case" — it would double-render. That advice is
> scoped to conditional **routing**, where the branches are exhaustive by construction
> (`stealth gte 10` / `lt 10 + fighting` / `lt 10` catch-all) and one always passes. Vesper ships 11
> such nodes and needs no door in any of them. The rule here is for **independent budgets that
> deplete together**, which is what a day cap and a price both are.

**R8 · A person owns a corner of the world — and the schedule has to agree.** Added 2026-08-24 from
Section G, after `the_season` shipped and the one defect a player reported was *"I don't know who is
who."*

Twenty-five field games were read in source to find what actually separates one character from
another. A log-odds pass over each speaker's dialogue answers it, and the answer is **not diction**:

| `destroyer` — the words that are theirs and nobody else's | |
|---|---|
| **Dr. Angela** | donate · patient · donor · treatments · sample · semen · recovery |
| **Dean Mea** | vote · levy · detention · discipline · students · punishment · class |
| **Stepmom** | ranch · house · dinner · hire |
| **Aunt** | thousand · investment · shopping |

`sluttown-usa` splits the same way, and it splits **twice** — each person has their own subject
*and their own supporting cast*: Romi has Ell, Gigi and Elliot and talks about fashion, the store,
jeans and stock; Leah has Eve, Nina and Joss and talks about classes, the pole, dancing and the
club; AJ has Brad and talks about the professor, tutoring and the test.

**A character is not a temperament with a name on it. He is a different part of the world, and he
talks about the part he is in.** A trait system cannot buy this; only the design can.

> ### ⚠️ The prose half is the easy half. The schedule is where it gets taken back.
>
> `the_season` **passes** the writing test. Every man genuinely owns a subject — Boyd speaks in
> numbers (*"Forty-one."* · *"The number is not an opinion."* · *"I have weighed eleven years of
> it."*), Prine in water and distance (*"You had water today? Not coffee. Water."* · *"Nobody comes
> down this far."*), Emmett in binary rules (*"You're on the rows or you're on the belt. Not
> both."*), Wade to an audience (*"Watch the top of the tree, boys."*).
>
> And its sixteen schedule rows collapse the whole cast into two places:
>
> ```
> the_camp   19:00–00:30   Wade, Prine, Emmett, Boyd    <- all four men, every night
> the_rows   05:30–12:00   Prine, Boyd, Wade            <- three of four, every morning
> ```
>
> **He is never the only man in the room, so he never gets to be a particular man.** Only Emmett
> (the shed) and Rae (the yard, the window) have somewhere that is theirs.

So the rule has two halves and **both are required**:

1. **His own subject and his own people** — a domain he talks about that nobody else talks about,
   and at least one named person offscreen who belongs to him and not to the crew.
2. **A place and an hour where he is the only one there.** Check it the way the defect was found —
   bucket every `[[npcs.schedules]]` row by `(location, start_time, end_time)` and read the rows
   with more than one name in them.

**Where the tag line fits.** `[ui.cast_page]`'s `tags` field (`engine.md` §34) is the four-word
compression of half of this — *"Manipulation | Attention | Writing | Oriental Food"* tells you what
Chloe is about before you have met her. It is a **summary of a corner she already owns**, not a
substitute for owning one. Four words on a card cannot rescue a man who has no domain.

---

## What this costs, and why it is worth it

Splitting one 23-choice hub into six surfaces is not more writing — it is the **same** writing on
six screens instead of one. What changes is that each screen can then have its own opener, its own
banding, and its own gate, which is the whole reason the engine has located canvases at all.

And it fixes a problem that looks unrelated. A location that must fill 19 buttons gets 19 *small*
things, because nobody can write nineteen substantial scenes at a front desk. The failure case
ended up with roughly 200 three-beat texture rungs and 29 surfaces carrying any heat at all — a
**7.6% explicit floor against a 27.8% sibling game** built by the same author under the same
doctrine. The menu shape set that ratio before a word was written.

**Wide and thin is a structural choice, not a writing outcome.** This file is where it gets made.

**The needs layer buys something the object layer never could: a reason to be in the room.** A player
walks into a kitchen because they are hungry, not because there is an airer in it. And a need that
shuts a door — *filthy means she cannot take the car* — turns a chore into a plan.

---

## What is checked

| | |
|---|---|
| **Gate 20 · a place is not a catalogue** | the backstop against the pathological case: no repeatable location-bound canvas offers more than 8 decisions. **No longer the sizing rule** — R2's closed list is |
| **Gate 29 · a need shuts a door** | every entry in `board.needs[]` is read by at least one condition somewhere in the game. `the-meters.md` M9 |
| **Gate 30 · the walk-in floor** | a location with at least one repeatable solo activity **and** at least one NPC schedule row carries at least one `substitutions` rule. R3 |
| **Gate 37 · a spent day still has a door** | no screen whose every choice is day-capped or priced lacks one choice free of **both** `conditions` and `costs`. Mirrors the engine's own `has_unconditional_choice`, so the gate and the runtime cannot disagree. R7 |
| **Lint · noun-only buttons** | the share of room-list labels that open on a determiner and name no verb. A number, not a bar — `the-voice.md` R1 |
| **Lint · the browse share** | the share of repeatable room canvases whose entire click changes nothing but the clock |
| **Lint · the act menu** | repeatable explicit surfaces split into node-routed loops and one-shot cascades. A count, never a target — R3b |

**R1, R2's judgement half, R4, R5b and R8 are deliberately not gated.** Whether *"Turn somebody away"* is
aimed at a person or at the room is a judgement a parser cannot make, and a proxy check for it would
pass exactly the game that failed. They stay a board-phase and authoring-time discipline. R5b joins
them for a different reason: it rests on four games read in source, which is an observation, not a
field.

**R8 joins them for a third reason, and it is the strongest of the three: the field disagrees with
itself.** `degrees-of-lewdity` is rank 7 with 15,626 passages, and its NPC record reads `penis`
2,198 times against `name_known` **27** — `lefthand`, `righthand`, `stance` and `distance` are a
limb-by-limb struggle machine. Its people are not characters at all; they are bodies in a physical
simulation, and that is a second working answer to the same problem. A gate mandating that
characters be differentiated *as people* would fail the seventh-ranked game in the corpus. **The
schedule-collision half of R8 is trivially checkable and a lint for it was considered and
declined** — half a rule enforced is worse than a whole rule taught.

> ⚠️ **What a checked-and-wrong rule costs, kept as the standing warning.** `objects` / gate 22 was
> the previous occupant of this section and it was **green on all five games** while forcing nine
> duplicate screens into existence. The mechanism: `_room_objects` computed affordances from
> `exit_block.choices` and **never read a canvas name**, so *"Get the washing in off the airer"* —
> an entire canvas about the airer — counted as **zero**. Strip the nine `room_*` screens from
> `the_allowance` and the gate reported **34 of 39 declared objects unusable**, naming objects that
> had a dedicated canvas standing in the same room.
>
> A check that cannot see the shape of the thing it is judging does not measure quality — it
> **manufactures** whatever it can see. That is worse than no check, because it ships green.
>
> Two rules in this file were demoted for having invented thresholds; this one was deleted for
> measuring the wrong object. Before adding a gate here, ask what an author would build to satisfy
> it if they were tired, and check that the answer is the thing you actually want.
