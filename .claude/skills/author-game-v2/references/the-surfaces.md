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

## Every choice hangs off a named object in the prose

**This is the most consistent shape in the field, and it is the difference between a room and a
menu.** Measured by playing five shipped games (`DOCTRINE_GAPS.md` study 5): three of them do this
independently, and the two that read worst are the two that do not.

A location's prose names a thing, and the choices that thing affords sit under it:

```
Your bed takes up most of the room.
   Strip and get in bed
   Wear pyjamas and climb in bed

Your clothes are kept in the creaky wardrobe.
   Wardrobe
   Mirror

The hallway outside connects to the rest of the orphanage.
   Bathroom · Kitchen · Main hall · Leave
```

Against the same eight choices as a flat list:

```
   Strip and get in bed
   Wear pyjamas and climb in bed
   Wardrobe
   Mirror
   Bathroom · Kitchen · Main hall · Leave
```

Identical content, identical count. **The first reads as four sentences about a room. The second
reads as a button list.** A third corpus game does it with the objects made explicit —
*"Your dorm room cot is against one wall."* / sleep · *"Past the end of your bed is a small closet
and shelf set."* / clothes.

> **The wall of buttons is not caused by the count. It is caused by choices that float free of the
> prose.** A screen that fails this cannot be fixed by deleting choices, and a screen that passes it
> can carry more than you would guess.

**How to author it:** write the room's paragraph first, naming the things in it. Then attach each
choice to the thing that affords it. A choice with nothing to attach to is a sign the room's prose
is missing an object — or that the choice belongs on another surface entirely (see the object test
above).

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

The two agree once you know what each is counting — a corpus street shows 12 links, of which 4 are
exits to other streets, 4 are travel affordances repeated on every screen, and **3–4 are decisions.**

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

**R2b · Every choice hangs off a named object in the prose.** Write the room's paragraph first,
naming what is in it; then attach each choice to the thing that affords it. A choice with nothing to
attach to means either the prose is missing an object or the choice belongs on a different surface.
**This is the rule that decides whether a screen reads as a room or as a menu**, and no count fixes
a screen that fails it. See the worked comparison at the top of this file.

**R2b is now MEASURED, and half of it is gated — which is the reason R3 could stop being a quota.**
Declare each room's affordances on the board:

```json
"board": { "locations": [
  { "id": "the_stock_room",
    "objects": ["the roll cages", "the cold store", "the CCTV recorder and its screen",
                "the eleven feet of corridor", "the padlocked door", "the shelves"] }
] }
```

`objects` are **the things the room's prose names AND the player can act on** — not every noun.
Atmosphere belongs in the prose, not in this list.

**Gate 22 · declared objects are real** — a hard gate, because both halves are pure consistency
against your own declaration and both are reachable:

1. every declared object is actually written into the room's prose
2. every declared object affords at least one choice — a named thing she cannot act on is texture,
   so either give it an affordance or take it out of the list
3. **every thing the choices actually act on is declared.** Computed from the GAME, not the board:
   if a choice hooks onto a word its screen really did write, and no declared object covers that
   word, the board left a real affordance out
   *(plus: a room that has screens but declares no objects fails; a room that declares objects but
   has no repeatable screen fails; and a declared id that is not a real location fails.)*

> ⚠️ **Check 3 exists because without it the gate was passable by declaring LESS.** Measured: one
> safe object per room, game byte-identical, scored **20/21 with gate 22 green**. The completeness
> half has to be computed from what the choices do, or a declaration check just rewards a short
> declaration. Same shrink now scores 59 undeclared affordances against 16 for the honest one.

**Lint · choices hang off the room** — the third check, *no choice names something its own screen's
prose has not put in the room*, is reported as a **percentage, not a verdict.**

> ⚠️ **It was built as a gate and demoted the same week, and the reason is worth keeping.** Run
> against the worked example at the top of this file — measured from a shipped game, printed here to
> show what *correct* looks like — a word-match fails **"Mirror"** under *"Your clothes are kept in
> the creaky wardrobe."* The mirror belongs to the cluster that sentence sets up; a human sees it and
> a matcher cannot. One in four of that example's real decisions fails, and the ceiling on a real
> game is ~74%, against 55% for the strict per-screen rule. **A gate demanding zero failures could
> never be passed, and this file has already
> demoted two rules for exactly that.** The number is worth reading; the pass/fail line was not.

The per-screen scope is deliberate: matching a choice against the room's *whole* declared list would
make the measure vacuous — a room declaring seventeen things would accept almost anything. R2b is
about the paragraph *in front of the player* naming the thing the choice acts on. Read the lint by
looking at **which screens contribute several floaters**, not at the total.

**R3 · A room's choice count is not chosen. It falls out of R2b.**

Write the room's paragraph, naming the things in it that she can act on. Hang every choice on one of
them. **That is the count** — it was not decided in advance and it is not a target.

**The relation is many-to-one, never one-to-one.** One object may afford several choices: the bed in
the worked example at the top of this file affords *strip and get in* and *pyjamas and climb in*, and
the wardrobe affords *wardrobe* and *mirror*. Read the other way round it becomes a quota again —
inventing an object to justify a choice, or capping a rich object at one, are both the disease in a
new coat. The only hard direction is that **no choice may hang on nothing.**

> ⚠️ **Do not read the 8 below as the size of a room.** It is a backstop for the pathological case
> and nothing else. Measured, study 6: a game built after this file existed put **19 of its 30
> screens at exactly 8** and shipped the *same 213 choices* as the 23-choices-on-one-desk game the
> cap was written to fail — the cap redistributed the menu instead of shrinking it, and pushed the
> median *up* from 7 to 8. **A ceiling makes "pass" and "maximise" point the same way.** The field
> median for things-to-do-at-a-place is **3**.

**The backstop:** a repeatable location-bound canvas fails above **8** decisions (gate 20). Field
median is 2 links and p90 is 4, so 8 is already double the ninetieth percentile — if you are near
it, the screen is doing several jobs and R1 already tells you where the seam is. Gate 20 now prints
`median · N of M screens at the cap`, so building to the number is visible on the scoreboard
instead of reading as a clean pass.

**R4 · Money is not a scene.** Purchases live with the thing bought, or on one ledger surface.

**R5 · Ungated choices are the minority.** If most of a location's doors open on day one, the
ascent tiers are decoration and the wall of choices is at its worst on the day the player knows
least. The failure case ran 109 of 216 ungated.

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
distinct scenarios**.

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

---

## Why two of these six have no gate, and that is the honest state

Four of these rules are enforceable and one (R3) is measured against a field. Two are not, and were
demoted after the thresholds were tested rather than before. That is the discipline working: **a
gate whose number is invented fails correct work and gets ignored, which is worse than a lint that
gets read.**

It is also the third time in this skill's construction that a measurement turned out to be comparing
two different denominators. Assume the seam is there until it is ruled out.

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
| **Gate 20 · a place is not a catalogue** | the backstop: no repeatable location-bound canvas offers more than 8 decisions. Prints `median · N at the cap` — a game built to the number reads differently from one built to its rooms |
| **Gate 22 · declared objects are real** | declare-then-check against `board.locations[].objects`: every declared object is written into the prose and affords a choice; every room with screens declares objects; no declared id is a phantom location |
| **Lint · choices hang off the room** | the share of room choices naming something their own screen said. A percentage to compare, never a bar to clear — see R2b for why it is not a gate |

**R1, R2 and R4 are deliberately not gated.** Whether *"Turn somebody away"* is aimed at a person or
at the room is a judgement a parser cannot make, and a proxy check for it would pass exactly the game
that failed. They stay a board-phase and authoring-time discipline.

> **R2b used to be on that list, and moving it half-off is the point.** It was described here as
> *"the highest-value ungated rule in this file… the one no check will ever catch for you"* — and it
> then drifted to **55% of choices anchored** in a game that scored 20/20, while gate 20 (the checked
> half of the same rule) was satisfied perfectly on 18 of its 22 rooms at exactly the cap. **What the skill
> wrote down and checked, held; what it wrote down and did not check, rotted.**
>
> The half that a parser *can* judge — did you write the object, can she use it — is now gate 22,
> because the board declares what the room has and the check compares the game against the author's
> own statement. **The half that needs a reader stayed unjudged**, and became a percentage instead:
> the original sentence was right about that part, and the first attempt to gate it failed the
> worked example printed at the top of this very file. Two rules in this file were demoted for that
> reason before; do not make it three.
