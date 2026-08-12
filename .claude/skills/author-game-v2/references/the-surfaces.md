# The Surfaces — where content attaches

`SKILL.md` names three kinds of content by **when they fire**: STANDING, TRIGGERED, MILESTONE.
That is one axis. This file is the other one, and without it a game can obey every other rule in
this skill and still be unplayable:

> **Which screen does this live on?**

> Measured failure this exists to prevent. A game authored entirely to v2 doctrine put **23 choices
> on its front desk, 19 on its street, 19 in its changing room** — one paragraph and then a wall of
> buttons, at every location, with 109 of its 216 doors open on day one. It scored **18/18**.
> Nothing in the skill said a location page had a shape, so the author invented one.

---

## The question to ask about every piece of content

**Who is this aimed at?** Three answers, three homes, and they never share an exit block.

| aimed at | lives on | how many |
|---|---|---|
| **a person** | that character's hub | one hub per schedule row — location × window |
| **the room, or herself** | its own located canvas | as many as the room has things to do |
| **her** — it happens *to* her | a substitution hung on a solo surface | as many as the room's traffic earns |

### The object test

Read the choice. **Is a person the object of the verb?**

- *"Pour her coffee"* · *"Ask him for the rent"* · *"Sit closer than you need to"* → **a hub rung** ✓
- *"Count the till"* · *"Take a shift"* · *"Work the door"* · *"Stock the soap"* → **not a hub rung.**
  Each is its own solo surface at that location.

The failure case had a hub binding **no NPC at all** and 23 choices, none of which had a person as
its object. Every one of them was a solo surface wearing a menu item's clothes.

---

## A place is not a catalogue

**Measured across 18 shipped sandboxes:**

```
median screen ......................... 2 links
median p90 ............................ 4 links
screens offering more than 12 ......... ~2% (median across the field)
```

The typical screen in a real game — the one the player is on most of the time — is **small**.

Big screens do exist. The reference game has 2.9% of its screens above 20 links. **But look at what
they are: shops, wardrobes, character creation. Catalogues.** A catalogue is legitimately long,
because its job is to list.

> **A place you return to every day is not a catalogue.** If a room's menu has grown to twenty
> items, either it is doing several jobs that want separate screens, or a shop has been merged into
> a room.

Both were true of the failure case: eleven of the front desk's 23 choices were **purchases** —
the water test, the advert, the electric, two wages, the frontage — sitting in the same undifferen-
tiated list as *"Look up at the board."*

**Money is not a scene.** A purchase is not a rung. Sinks belong where the thing being bought lives
— the boiler upgrade at the boiler, the paint at the frontage — or on one dedicated ledger surface
reached from the desk. Never scattered through a room's texture at equal weight.

---

## The rules

**R1 · One canvas per (who it's aimed at × when).** A location where she both deals with a person
and does her own work is **at least two canvases**, plus a substitution if anyone can walk in on
her. Never put solo work in a character's hub.

**R2 · Apply the object test to every choice** before it goes in a hub's exit block.

**R3 · A repeatable location-bound canvas caps at 8 choices.** Field median is 2 and p90 is 4, so 8
is already double the ninetieth percentile. Above that, split by what the choices are aimed at —
the split is always available, because R1 already tells you the seam. Gate 20.

**R4 · Money is not a scene.** Purchases live with the thing bought, or on one ledger surface.

**R5 · Ungated choices are the minority.** If most of a location's doors open on day one, the
ascent tiers are decoration and the wall of choices is at its worst on the day the player knows
least. The failure case ran 109 of 216 ungated.

**R6 · The opener moves.** A hub re-entered daily whose first paragraph never changes is a dead
screen. Band it on whichever tier the location serves. Ten of the failure case's eighteen menus sat
on a single static block.

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

---

## What is checked

| | |
|---|---|
| **Gate 20 · menu size** | no repeatable location-bound canvas offers more than 8 choices |

**R1, R2 and R4 are deliberately not gated.** Whether *"Turn somebody away"* is aimed at a person
or at the room is a judgement a parser cannot make, and a proxy check for it would pass exactly the
game that failed. They are a board-phase and authoring-time discipline, and R3's cap is the
measurable shadow they cast — a hub that violates R1 almost always violates R3 as well, which is
how the failure case would have been caught on its first build.
