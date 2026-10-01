# The Map — the world as a place, not a list of rooms

Read this in the **board** phase, before a character is placed and before a word of prose is
written. The map is infrastructure, not a system (`the-systems.md` SY1), and the only one the player
touches on **every single turn**; the engine validates almost none of it.

> ⚠️ **Root the world outdoors, in more than one zone.** The passing games do: Shady Deals'
> [City Map] links five districts (`data-passage="Downtown Road"`, Harbor, Suburbs, Outskirts,
> City Center), and Course of Temptation's [Maps] splits into `<<tab Campus>>` and `<<tab Town>>`.
> A world of one house plus a row of shops is not that shape, however many gates it passes, and
> that holds for every fantasy. In a taboo-at-home game (`want.fantasy_shape = "taboo_at_home"`) the
> house is her hub, the place she returns to; the world outside is what makes the house risky.
> *(LO decided.)*
> **An example outranks every rule beside it: a rule is read, an example is copied.** So this file
> teaches a *menu* you must choose from and carries no picture you can copy. See `SKILL.md`,
> operating rules.

---

## R0 · Pick the SHAPE before you count anything

**The genre floor is a multi-zone world — zone → venue → room — not a single building.** Choose the
shape from the premise. **Do not default to a house.**

That sentence is carried over from `author-game/references/location-design.md` §2, where it was
measured against five named shipped games.

| `archetype` | the shape | fits |
|---|---|---|
| **`nested_zones`** *(the default to beat)* | district → venue → interior room; each zone lists its children | most life-sims: a town or campus **plus** a home |
| **`two_hub`** | two strong anchors — home and work — fanning to rooms, joined by a commute | a premise anchored to two places |
| **`map_hotspots`** | a drawn map with clickable districts | a large, replay-heavy world, 10+ zones |
| **`street_mesh`** | named streets, each listing its neighbours and its venues | a city that should feel real without a drawn map |
| **`time_slot`** *(the anti-map)* | no geography at all — a fixed Morning → Work → Evening chain; the one exception to the zone rule, and each slot still carries a thread of her life, with its people and its link to the hook | heavily scripted content where a map is friction |

**Record the pick in `board.map.archetype`. Gate 28 fails a board that has not chosen.**

> ⚠️ **This list is five entries long because five is what was measured, not because five is what
> exists.** If the premise genuinely fits none of them, add a sixth **with its evidence** — a named
> game that runs it. Forcing a premise into the nearest of five is the same mistake as copying one
> example, only slower.

**Then size it on two axes, and they are independent:**

- **Scale** — how many zones. Match it to the threads of her life (`the-want.md` §6), not to the
  cast size: each thread needs its place, and two threads may share one.
- **Aliveness** — how lived-in. A *tight slice* holds only what the content needs; a *living world*
  carries ambient traffic, routines and events the player did not trigger. This is a
  **content-budget fork, not a quality dial** — every ambient zone is content you have to fund.
  A tight slice is legitimate **when chosen out loud**. The failure is drifting into one because
  nobody asked. For a sandbox, lean toward alive: **a small dense world beats a wide thin one.**

⚠️ **The count is derived, but only INSIDE the shape you chose.** `the-board.md` §1 says to derive
the location count from where your cast's rosters go. That is right, and on its own it is circular:
the premise fixes the cast, the cast fixes the map, and a family of five who live in one house
returns a house every time. **The shape is the input that breaks the circle**, so it is picked
first on the board (`board.map.archetype`), before a room is derived from anyone's roster.

---

## The rules

### R1 · A map is a place, not a list of rooms

The test is not *"does every room have a job"* — a room-by-room checklist passes a world with no
outside and no beds. The test is:

> **Could someone who has never seen the game draw this place from the graph?**

Write the graph down in the board phase as something a person could walk, and check it against that
question before declaring a single location.

⚠️ **Answer R0 first.** Before this question can mean anything you have to have chosen a *shape*.
R1 asks whether the world you picked hangs together. It cannot tell you that you never picked one.

### R2 · If someone lives there, they have a room

Every character the board declares gets a **`home`** recorded in `v2_state.json`. If a character
sleeps off-screen — a neighbour, a tenant on nights who is simply gone — that is declared too,
explicitly, as `"offscreen"`.

This cannot be inferred and must not be guessed. A tenant working nights legitimately has no night
schedule row; a shopkeeper legitimately has no bed in the player's house. Only a declaration
separates *lives elsewhere* from *was never given a room*. Gate 12.

**A home is laid out like a house.** The defect this stops: the kitchen as the house hub, the
people who live there homed in it, the bathroom folded into a landing.

- **A home is a bedroom:** a room of the person's own (a couple shares one). Never the hub, a
  thoroughfare, the kitchen, a hallway or a landing.
- **The house is entered through its entry.** Its hub is the hall or front door, named for the home
  ("Home", "The House"), and the street's button shows that name. The kitchen, the bathroom and the
  bedrooms are rooms off it, never the hub.
- **One room, one job:** a shared bathroom is its own room (R6c), not part of a hallway.
- **Plain names** a player reads at a glance: "Upstairs", not "The Landing".

⚠️ **A room the Want promises must exist.** If the Want sells access to somewhere as a reward for
topping out a tier — *her father's room*, *the office*, *upstairs* — that location is owed. Nothing
else in the scoreboard can see this: the meter-ceiling gate checks that authored **gates** reach a
meter's top band, never that the Want's **prose promises** were built.

### R3 · The exterior is the GROUND, not a room off the kitchen

Any destination the fiction places away from her home base requires a connecting **exterior**
location. This is not decoration:

- it is where the ascent meters get a consequence surface **outside** the household, and
- it is the only renewable source of new characters a domestic premise has. A world with no
  exterior can only ever recycle its interior.

**And it is not enough for the exterior to exist. It has to be the thing everything else sits on.**

```
✅  the yard  ──┬── the house ── the rooms          the world contains the home
                ├── the barn
                └── the market

❌  the kitchen ─┬── the rooms                       the home contains a bit of world
                 └── the shops
```

Inside the house, the same shape one level down (R2):

```
✅  the street ── Home (the hall) ─┬── the kitchen        the hall is the hub
                                   ├── the bathroom
                                   └── Upstairs ─┬── her room
                                                 └── a bedroom for each other resident

❌  the street ── The Kitchen ─┬── the landing           the kitchen is the hub; the bathroom
                               └── her room              and his room are the landing
```

**The declared `exterior` must be a root** — no `entry_from` — with the home base among the
things that hang off it. Where the fiction wants two separate grounds (a home and a town that are
genuinely apart), make them **two roots joined by a travel canvas**, not one nested inside the other,
and list both in `board.map.roots[]`. Gate 11 walks on foot, so it exempts the second root only when
that root is marked `offscreen` or sealed (entered only by a canvas exit).

The diagram above is the topology. This is what it is in keys, and it is the whole of the
difference — one field, present or absent, on the location the board names as `exterior`:

```toml
# ❌ inverted — the ground hangs off a room, and gate 28 fails
[[locations]]
id         = "<exterior_location_id>"
entry_from = "<an_interior_location_id>"     # ← this line is the defect

# ✅ a root — nothing is its parent, and everything else hangs off it
[[locations]]
id = "<exterior_location_id>"
# no entry_from at all
```

> ⚠️ **No example world here, and there still will not be one** — see the note under *What the
> board phase records*. A mechanism is safe to show and a floor plan is not: a mechanism copied
> verbatim produces a correct game, and a world copied verbatim produces the same world again.
> *(LO decided.)* That is why this shows one key and no rooms.

**Gate 28 checks this mechanically**, off `entry_from`. It is the half of R1 a parser can actually
see. Declare the exterior in `board.map.exterior`; the cost of crossing it goes on the area as
`crossing_costs` (`engine.md` §22).

⚠️ **A missing map fails too.** A game that declares no `board.map` block fails both `the map is a
place` and `residents have homes`. An undeclared board is undone work, and the gates report it as
red rather than `n/a` precisely so it cannot pass as an absence.

### R4 · Names are navigation, and a name is not house style's business

A location name is a **button**. `the-voice.md` R1 owns the principle — *a name a player cannot
resolve is a navigation bug wearing register's clothes* — and this is where it bites hardest,
because a room name is read on every single turn.

**The contract, carried from `author-game/references/location-design.md` §3, measured across the
field's strongest games:**

| kind | form | example |
|---|---|---|
| public venue | **bare plain noun**, no article | `Market` · `Gym` · `Bar` · `Police Station` |
| private / owned interior | **possessive** | `Your Room` · `Joss's Room` · `Your Parents' Room` |
| hierarchy | rides the **page you are on**, never the label | `Bar`, not `Hotel — Bar` |
| flavour and branding | lives in the **description**, never the button | label `The Bar`; the prose calls it the Underworld Lounge |

**Consistency beats flattening.** An articled house style is a legitimate register, not a bug — the
only real defect is being inconsistent, some children prefixed and some bare.

⚠️ **The readability test applies to every game.** A name has to resolve for a stranger: Shady
Deals' [City Map] names its districts *Downtown*, *Harbor*, *Suburbs*, and Course of Temptation's
[SummitMarket] opens *"a building which contains the eponymous market"*. A dated or regional word
(*The Parade*, read by most people as a procession) fails it, and so does `the-voice.md` R1's own
counter-example, *The Undercroft*.
Say it out loud to someone who has not played: if they cannot tell you what is through the door,
it is a bad button no matter whose house style it matches.

**And a button cannot carry the explanation.** Where the name alone will not tell a stranger what
the place is FOR, the **location's own `description`** has to — it is the only surface the player
sees on every visit, so it says what kind of place this is and what happens here before it says
what it smells of. `references/the-first-hour.md` F9 owns that rule; `lint · the place says what it
is` reads it.

⚠️ **The fix is not a first-visit scene.** That device is one game in twenty-six, and the gate that
required it was deleted 2026-08-26. Take one only when a place has a genuinely one-time thing to say. F9 carries the count.

### R5 · The graph owes the prose

Nothing the writing treats as a place may be missing from the map. When a paragraph says *hall*,
either the hall exists or the paragraph is wrong. Both are cheap on the day and expensive twenty
thousand words later. Reported as a lint, because *"he came through the hall"* in a world that
deliberately has no hall is a judgement call — but three uses of the same word is a place.

### R6 · A door belongs to a PERSON, not to a room

A **door** is a threshold screen the player lands on *instead of* the room: click someone's bedroom and get
**knock** rather than walking straight in. `[locations.door]`, `engine.md` §44.

**It is rare, and rarity is not a style note — it is the rule.** `degrees-of-lewdity` carries **six
named doors** (47 `<<dooricon>>` sites over 30 passages) in a **15,626-passage** game.
`become-someone` has 54, and every one of them is a *person's house*. Measured 2026-09-02 across 27
shipped sandboxes; every figure here is reproducible from `~/Documents/Door_Study_20260902/`.

⚠️ **Presence is NOT the test.** If "someone is sometimes in there" earned a door, the game would be
a knocking simulator. What earns a door is that the room **belongs to
somebody** and she is the visitor.

**The refusal is one short line, and it is allowed to be the same line every time.** The field runs
a **median 8 words**, and it is the *same sentence 44 times* — *"You knock on the door, but nobody
came."* The value of the screen is its **structure**, not its prose;
spend the words on the far side of the door.

> **One authored departure, recorded as a departure.** The field never offers *knock* and *go in*
> side by side — `become-someone`'s `katehouse` offers only *Knock*, and entering is what knocking
> earns. LO's call, 2026-09-02: on a door that is *open*, both may be live, because an open door is
> a fact about the person behind it. That is ours, not the field's, and it is written here so the
> next author knows which is which.

### R6b · The door always renders. What is conditional is whether the door EXISTS

**Do not build a rule that skips the threshold when it has nothing to say.** It is the first thing
anyone designs and the field does not do it: `become-someone` ships **54 door screens — 50 gating on
occupancy, 46 on occupancy AND time of day, median 14 words, 53 of 54 carrying a way back** — and
not one of them is skipped.

What the field makes conditional is the **door's existence**. The reference game (numbers only) puts
one character's flat on the street only once that character's stage reaches 3; from then on the
screen always renders.

**So rarity is the answer to the two-click tax, not skipping.** A door on eight rooms is a speed
bump on every one of them. A door on one room is the room.

⚠️ **This rule exists because the skip was designed, argued for, and only then measured.** It was in
the plan, it sounded obviously right, and one probe killed it. Assume the same about the next
obvious refinement.

### R6c · A shared room gets no door

A bathroom, a kitchen, a front room — she walks in. **Occupancy is a row INSIDE the room**, not a
threshold in front of it.

`become-someone`'s `Bathroom` is the room itself with a conditional chain in it: walk in on one
character at one hour, on another at another, and *"the door is locked… you hear the shower… you
leave, needing to wait your turn"* written as prose **inside the room** rather than as a blocked
card on the map. A locked bathroom is a sentence, not a screen.

**The engine has the primitive** (`npc_at_location`, per-NPC or any-NPC, operator `is_present` or
`is_absent`). The shape is a pair of rows in the one room — `activity_bathe` gated `is_absent` beside
`bathroom_occupied` gated `is_present` — and a row in someone's room gated on that person being out.

**And his room while he is out is content** — in *his* room, as occupancy, not a destination left
with nothing to do (`the-board.md` §1, two kinds of place). Where the field has a door it usually also
has *going through their things while they are out* — 260 such labels across 15 of 27 games. `new-life-project` (structure only) shows
the best shape of it: the row is there, and the game names who is inside, in red, beside the
option to search anyway. Occupancy as a stated risk, not a lock.

---

---

## The engine gives you more than `entry_from`

All five verified against source; full citations in `references/engine.md`.

| you want | the field |
|---|---|
| walking somewhere to **cost** time or a trait | `costs = { time = 20, energy = 5 }` on `[[locations]]` |
| a place that is **shut and inert** — a story gate | `entry_conditions` + `blocked_message` (a greyed, unclickable card) |
| a place **shut at set hours**, saying when it opens | `hours` + `closed_text` — `engine.md` §22 |
| a place **not listed until she finds it** | `hidden_until = { flag }` — `engine.md` §22 |
| a place she **only passes through** | `kind = "thoroughfare"` — `engine.md` §22 |
| time charged **once, on crossing into an area** | `crossing_costs` on the area's container — `engine.md` §22 |
| a door she can **stand at and knock on**, whether or not she may enter | `[locations.door]` — R6, `engine.md` §44 |
| an "away" label for a schedule with **no nav card** | `offscreen = true` |
| a pure navigation wrapper holding no content | `is_container` + `default_entry` |

**Travel friction is what makes schedules bite.** A premise that says *"ten minutes' walk away"*
while arriving costs nothing has written a fact the player never experiences. Put twenty minutes on
the bridge and being in two places stops being free — which is the entire point of having authored
a schedule grid at all. Put the cost on the **area** (`crossing_costs`), never on every room.

---

## What the board phase records

**The fields, and deliberately no world.**

```jsonc
"board": {
  "map": {
    "archetype":  "<nested_zones | two_hub | map_hotspots | street_mesh | time_slot>",
    "shape":      "<one sentence a stranger could draw from>",
    "home_base":  "<location_id — where she sleeps>",
    "exterior":   "<location_id — the ground everything else sits on. MUST be a root.>",
    "homes":      { "<npc_id>": "<location_id | offscreen>" },
    "roots":      ["<location_id>"],
    "scale":      "<one street · a district · a town>",
    "alive":      "<tight slice | living world>"
  }
}
```

> ⚠️ **There is no example world here and there will not be one.** *(LO decided.)* **An example
> outranks every rule beside it**, so the
> shape is taught as R0's menu, which you must choose from, and the schema is shown as fields, which
> you cannot copy a world out of.
>
> If a validated map is ever promoted to an example here, it is **one per archetype or none** — a
> single good example is still one world, copied just the same.

Declared once, before content. The gates then check the built game against **its own declaration**
rather than against a guess.

---

## Navigation — area, building, room

*(LO decided, D10.)*

- **Area → building → room.** Time is charged on crossing into another area (`crossing_costs`), not on
  every room inside it.
- **No fast travel**, for now.
- **Places she has not found are hidden** (`hidden_until`); **closed places show why**
  (*"Closed. Opens at 10:00 PM."*, `hours`; the clock prints 12-hour, `v2.py:4300`).
- **Guidance cards carry place, time and what is waiting**, and a travel link carries the engine's NEW
  mark when something new waits there.
- **Faces stay on travel cards.**

---

## What is checked, and what is not

| | |
|---|---|
| **Gate 11 · world reachable** | every location reachable on foot from the start, unless `offscreen` or deliberately sealed — a second root in `board.map.roots[]` needs one of the two |
| **Gate 12 · residents have homes** | every declared character has a `home` that is a real location or `offscreen`. Not checked yet (planned, K13): that the home is not the hub, a thoroughfare or a container, and is shared only by a declared couple (R2) |
| **Gate 28 · the map is a place** | `board.map.archetype` is one of R0's five, **and** the declared `exterior` is a root rather than a leaf off an interior room (R3) |
| **Lint · the prose names places the map does not have** | place nouns used three or more times with no matching location |
| **Lint · a door opens onto something** | every `[locations.door]`: one no option can ever open, one whose only option is `enter`, a knock nobody is scheduled to answer, and a door on a room the whole cast passes through (R6–R6c). Silent on a game that declares none |

**R1 as a whole is still not a gate.** Whether a world *reads* as a coherent place is not
mechanically decidable, and a check that measures a proxy for it is exactly how a world with no
street scored full marks.

**What changed on 2026-08-18 is that two pieces of it turned out to be decidable after all**, and
gate 28 takes both: *did you choose a shape* (a declaration), and *is the outside actually the
outside* (`entry_from`, which no ledger can talk its way out of). What is left for the human is the
part that genuinely needs eyes.

> The map is signed like every spine page: LO signs it once LO has read it (`the-spine.md`).
