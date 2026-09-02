# The Map — the world as a place, not a list of rooms

Read this in the **board** phase, before a character is placed and before a word of prose is
written. The map is the only system the player touches on **every single turn**, and the engine
validates almost none of it.

> Measured failure this exists to prevent: a game shipped with every gate green and a world where
> the corner shop was one step from the sofa, three of its four men had no bedroom, and the prose
> named a hall six times that the map did not contain. Every location in it individually had a
> stated job, a scheduled body, and something repeatable to do. **The set still wasn't a place.**

> ⚠️ **AND THEN IT HAPPENED AGAIN, BECAUSE OF THIS FILE.** Two games later a second world shipped
> at **26/26 gates** that was seven rooms of one house plus a row of shops — and it was recognised
> from the location list alone, by eye, as *"the same mistake we made in back home."* It was. Of the
> five v2 games, **the only two whose map starts indoors are those two.** The three that read as
> places all root the world outdoors.
>
> The cause was on this page. The one worked example this file used to carry was **the first
> game's own map** — its character ids, its box room — reconstructed with its two known bugs
> patched out and its **skeleton left intact**. Every map since inherited that skeleton.
> **An example outranks every rule beside it: a rule is read, an example is copied.** So this file
> now teaches a *menu* you must choose from and carries no picture you can copy. See
> `SKILL.md`, operating rules.

---

## R0 · Pick the SHAPE before you count anything

**The genre floor is a multi-zone world — zone → venue → room — not a single building.** Choose the
shape from the premise. **Do not default to a house.**

That sentence is carried over from `author-game/references/location-design.md` §2, where it was
measured against five named shipped games. v2 was built without it and produced two house-shaped
worlds in five attempts.

| `archetype` | the shape | fits |
|---|---|---|
| **`nested_zones`** *(the default to beat)* | district → venue → interior room; each hub lists its children | most life-sims: a town or campus **plus** a home |
| **`two_hub`** | two strong hubs — home and work — fanning to rooms, joined by a commute | a premise anchored to two places |
| **`map_hotspots`** | a drawn map with clickable districts and fast-travel | a large, replay-heavy world, 10+ zones |
| **`street_mesh`** | named streets, each listing its neighbours and its venues | a city that should feel real without a drawn map |
| **`time_slot`** *(the anti-map)* | no geography at all — a fixed Morning → Work → Evening chain | heavily scripted content where a map is friction |

**Record the pick in `board.map.archetype`. Gate 28 fails a board that has not chosen.**

> ⚠️ **This list is five entries long because five is what was measured, not because five is what
> exists.** If the premise genuinely fits none of them, add a sixth **with its evidence** — a named
> game that runs it. Forcing a premise into the nearest of five is the same mistake as copying one
> example, only slower.

**Then size it on two axes, and they are independent:**

- **Scale** — how many zones. Match it to the cast; a small cast does not need a city.
- **Aliveness** — how lived-in. A *tight slice* holds only what the content needs; a *living world*
  carries ambient traffic, routines and events the player did not trigger. This is a
  **content-budget fork, not a quality dial** — every ambient zone is content you have to fund.
  A tight slice is legitimate **when chosen out loud**. The failure is drifting into one because
  nobody asked. For a sandbox, lean toward alive: **a small dense world beats a wide thin one.**

⚠️ **The count is derived, but only INSIDE the shape you chose.** `the-board.md` §1 says to derive
the location count from where your cast's rosters go. That is right, and on its own it is circular:
the premise fixes the cast, the cast fixes the map, and a family of five who live in one house
returns a house every time. **The shape is the input that breaks the circle**, so it is picked
first — before the cast exists, in the Want.

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

The measured failure: a game declared an exterior, put a 25-minute travel cost on it, passed every
gate — and its exterior was **a leaf hanging off the kitchen**. You stepped out of a kitchen straight
into a row of shops. No front door, no street, no ground. The world did not contain the house; the
house contained a scrap of world, and it read as a floor plan for exactly that reason.

So: **the declared `exterior` must be a root** — no `entry_from` — with the home base among the
things that hang off it. Where the fiction wants two separate grounds (a home and a town that are
genuinely apart), make them **two roots joined by a travel canvas**, not one nested inside the other.

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
> verbatim produces a correct game, and a world copied verbatim produced three games with the same
> box room. That is why this shows one key and no rooms.

**Gate 28 checks this mechanically**, off `entry_from`. It is the half of R1 a parser can actually
see. Declare the exterior in `board.map.exterior` and the routes across it in `board.map.bridges`.

⚠️ **The commoner failure is not an inverted map — it is no map at all.** Measured 2026-08-29,
`back_home` fails both `the map is a place` and `residents have homes` for one reason: it declared
no `board.map` block, with the full schema sitting in this file. **No example would have prevented
that.** An undeclared board is undone work, and the gates report it as red rather than `n/a`
precisely so it cannot pass as an absence.

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

> **The five games shipped before 2026-08-18 are grandfathered.** back_home, steam, forty_miles,
> seventh_day and the_allowance all run the articled style throughout and it is applied evenly. Do
> not rename them. This contract governs games authored from here.

⚠️ **But the readability test is not grandfathered, and it is the one that failed.** Two names
shipped that a player cannot resolve: **`The Parade`** — British, dated, and read by most people as
a procession rather than a row of shops — and **`The Box Room`**, which is
`the-voice.md` R1's own worked example of a bad name, *"The Box Room becomes The Tenant's Room and
says who and why in two words."* The game used the rule's own counter-example as a location name.
*(That example said **Lodger's** until 2026-08-22 — a word no field game uses, so the prescribed
cure carried the same defect as the disease. Two games copied it.)*
Say it out loud to someone who has not played: if they cannot tell you what is through the door,
it is a bad button no matter whose house style it matches.

**And a button cannot carry the explanation.** Where the name alone will not tell a stranger what
the place is FOR, the **location's own `description`** has to — it is the only surface the player
sees on every visit, so it says what kind of place this is and what happens here before it says
what it smells of. `references/the-first-hour.md` F9 owns that rule; `lint · the place says what it
is` reads it. Measured failure: a game declared its anchor at 27% of the whole word budget and its
description opened *"…and under them forty machines"* — forty machines of what — and the first thing
the human reader asked was what the place is. It was long, specific and well written.

⚠️ **The fix is not a first-visit scene.** That device is one game in twenty-six, and the gate that
required it was deleted 2026-08-26 after it sent an author to write nine arrivals that were reverted
the next day. Take one only when a place has a genuinely one-time thing to say. F9 carries the count.

### R5 · The graph owes the prose

Nothing the writing treats as a place may be missing from the map. When a paragraph says *hall*,
either the hall exists or the paragraph is wrong. Both are cheap on the day and expensive twenty
thousand words later. Reported as a lint, because *"he came through the hall"* in a world that
deliberately has no hall is a judgement call — but three uses of the same word is a place.

### R6 · A door belongs to a PERSON, not to a room

A **door** is a threshold screen the player lands on *instead of* the room: click Ray's Room and get
**knock** rather than walking straight in. `[locations.door]`, `engine.md` §44.

**It is rare, and rarity is not a style note — it is the rule.** `degrees-of-lewdity` carries **six
named doors** (47 `<<dooricon>>` sites over 30 passages) in a **15,626-passage** game.
`become-someone` has 54, and every one of them is a *person's house*. Measured 2026-09-02 across 27
shipped sandboxes; every figure here is reproducible from `~/Documents/Door_Study_20260902/`.

⚠️ **Presence is NOT the test.** **151 of 239 rooms across our own 18 games — 63% — ever hold a
scheduled person.** If "someone is sometimes in there" earned a door, two rooms in three would have
one and the game would be a knocking simulator. What earns a door is that the room **belongs to
somebody** and she is the visitor.

**The refusal is one short line, and it is allowed to be the same line every time.** The field runs
a **median 8 words**, and it is the *same sentence 44 times* — *"You knock on the door, but nobody
came."* Ours run 22 and are bespoke. The value of the screen is its **structure**, not its prose;
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

What the field makes conditional is the **door's existence**. `degrees-of-lewdity` puts Whitney's
flat on the street only once `$whitney_home_stage gte 3`; from then on the screen always renders.

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

**We already do this correctly and did not notice.** `back_home` ships **13 occupancy-gated rows** —
`activity_wash` gated `is_absent` beside `bath_occupied` gated `is_present`, and
`activity_his_room` gated on the lodger being out. The engine has had the primitive all along
(`npc_at_location`, per-NPC or any-NPC). `orientation` simply did not use it, which is how Ray's
Room shipped one row of 31 words against a declared 3,000.

**And the empty room is content.** Where the field has a door it usually also has *going through
their things while they are out* — 260 such labels across 15 of 27 games. `new-life-project` shows
the best shape of it: the row is there, and the game says **"Tyson is in there."** in red beside
*"Search anyways"*. Occupancy as a stated risk, not a lock.

---

---

## The engine gives you more than `entry_from`

All five verified against source; full citations in `references/engine.md`.

| you want | the field |
|---|---|
| walking somewhere to **cost** time or a trait | `costs = { time = 20, energy = 5 }` on `[[locations]]` |
| a place that is **shut and inert** — the mall at midnight, a story gate | `entry_conditions` + `blocked_message` (a greyed, unclickable card) |
| a door she can **stand at and knock on**, whether or not she may enter | `[locations.door]` — R6, `engine.md` §44 |
| an "away" label for a schedule with **no nav card** | `offscreen = true` |
| a pure navigation wrapper holding no content | `is_container` + `default_entry` |

**Travel friction is what makes schedules bite.** A premise that says *"ten minutes' walk away"*
while arriving costs nothing has written a fact the player never experiences. Put twenty minutes on
the bridge and being in two places stops being free — which is the entire point of having authored
a schedule grid at all. Put the cost on **bridges between zones**, never on every room.

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
    "bridges":    [ { "from": "<location_id>", "to": "<location_id>", "costs": { "time": 0 } } ],
    "r1_signoff": "<WHO signed it and WHEN, then what they saw. 'the author' is not a name.>"
  }
}
```

> ⚠️ **There is no example world here and there will not be one.** This block used to carry a filled-in
> map, and that map was the first game's own — its `npc_` ids, its box room — with its two known bugs
> patched out. Three games copied its shape. **An example outranks every rule beside it**, so the
> shape is taught as R0's menu, which you must choose from, and the schema is shown as fields, which
> you cannot copy a world out of.
>
> If a validated map is ever promoted to an example here, it is **one per archetype or none** — a
> single good example recreates the same failure with a nicer floor plan.

Declared once, before content. The gates then check the built game against **its own declaration**
rather than against a guess.

**`home_base` was called `dwelling` until 2026-08-18.** The word presumed a house before any
decision had been made, and it was already wrong for two shipped games — a truck stop and a
bathhouse. The five existing ledgers still carry the old key; nothing reads it (`gates.py` reads
only `board.map.homes`), so they are stale, not broken.

---

## What is checked, and what is not

| | |
|---|---|
| **Gate 11 · world reachable** | every location reachable on foot from the start, unless `offscreen` or deliberately sealed |
| **Gate 12 · residents have homes** | every declared character has a `home` that is a real location |
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

> ⚠️ **And the human sign-off failed the first time it mattered.** One game's ledger reads
> *"SIGNED OFF by LO in chat, board phase, 2026-08-16"* — a person, a place, a date. The next reads
> *"Signed off in the board phase."* No name. No date. **The map signed off its own map**, and that
> is the game that shipped seven rooms of a house at 26/26.
>
> So `r1_signoff` records **who** and **when**. A sign-off by the author of the thing being signed
> off is not a sign-off, and a gate cannot tell the difference — which is exactly why it is written
> down here instead.
