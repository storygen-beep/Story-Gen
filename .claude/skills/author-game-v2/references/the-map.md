# The Map — the world as a place, not a list of rooms

Read this in the **board** phase, before a character is placed and before a word of prose is
written. The map is the only system the player touches on **every single turn**, and the engine
validates almost none of it.

> Measured failure this exists to prevent: a game shipped with every gate green and a world where
> the corner shop was one step from the sofa, three of its four men had no bedroom, and the prose
> named a hall six times that the map did not contain. Every location in it individually had a
> stated job, a scheduled body, and something repeatable to do. **The set still wasn't a building.**

---

## The four rules

### R1 · A map is a place, not a list of rooms

The test is not *"does every room have a job"* — a room-by-room checklist passes a world with no
outside and no beds. The test is:

> **Could someone who has never seen the game draw this building from the graph?**

Write the graph down in the board phase as something a person could walk, and check it against that
question before declaring a single location.

### R2 · If someone lives there, they have a room

Every character the board declares gets a **`home`** recorded in `v2_state.json`. If a character
sleeps off-screen — a neighbour, a lodger on nights who is simply gone — that is declared too,
explicitly, as `"offscreen"`.

This cannot be inferred and must not be guessed. A lodger working nights legitimately has no night
schedule row; a shopkeeper legitimately has no bed in the player's house. Only a declaration
separates *lives elsewhere* from *was never given a room*. Gate 12.

⚠️ **A room the Want promises must exist.** If the Want sells access to somewhere as a reward for
topping out a tier — *her father's room*, *the office*, *upstairs* — that location is owed. Nothing
else in the scoreboard can see this: the meter-ceiling gate checks that authored **gates** reach a
meter's top band, never that the Want's **prose promises** were built.

### R3 · If she travels, there is something to travel through

Any destination the fiction places away from the dwelling requires a connecting **exterior**
location. This is not decoration:

- it is where the ascent meters get a consequence surface **outside** the household, and
- it is the only renewable source of new characters a domestic premise has. A world with no
  exterior can only ever recycle its interior.

Declare the exterior in `board.map.exterior` and the routes across it in `board.map.bridges`.

### R4 · The graph owes the prose

Nothing the writing treats as a place may be missing from the map. When a paragraph says *hall*,
either the hall exists or the paragraph is wrong. Both are cheap on the day and expensive twenty
thousand words later. Reported as a lint, because *"he came through the hall"* in a world that
deliberately has no hall is a judgement call — but three uses of the same word is a place.

---

## The engine gives you more than `entry_from`

All four verified against source; full citations in `references/engine.md`.

| you want | the field |
|---|---|
| walking somewhere to **cost** time or a trait | `costs = { time = 20, energy = 5 }` on `[[locations]]` |
| a door that is **visible but shut**, with in-world prose on the card | `entry_conditions` + `blocked_message` |
| an "away" label for a schedule with **no nav card** | `offscreen = true` |
| a pure navigation wrapper holding no content | `is_container` + `default_entry` |

**Travel friction is what makes schedules bite.** A premise that says *"ten minutes' walk away"*
while arriving costs nothing has written a fact the player never experiences. Put twenty minutes on
the bridge and being in two places stops being free — which is the entire point of having authored
a schedule grid at all. Put the cost on **bridges between zones**, never on every room.

---

## What the board phase records

```jsonc
"board": {
  "map": {
    "shape":    "one dwelling + a street + one workplace",
    "dwelling": "the_house",
    "exterior": "the_street",
    "homes":    { "npc_ray": "rays_room", "npc_marek": "the_box_room", "npc_hannah": "offscreen" },
    "bridges":  [ { "from": "the_street", "to": "the_shop", "costs": { "time": 20 } } ]
  }
}
```

Declared once, before content. The gates then check the built game against **its own declaration**
rather than against a guess.

---

## What is checked, and what is not

| | |
|---|---|
| **Gate 11 · world reachable** | every location reachable on foot from the start, unless `offscreen` or deliberately sealed |
| **Gate 12 · residents have homes** | every declared character has a `home` that is a real location |
| **Lint · the prose names places the map does not have** | building-part nouns used three or more times with no matching location |

**R1 is deliberately not a gate.** Whether a map reads as a coherent place is not mechanically
decidable, and a check that measures a proxy for it is exactly how a world with no street scored
full marks. It stays a human sign-off in the board phase. Sign it off out loud, in the ledger.
