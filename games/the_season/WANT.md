# The Want — THE SEASON

> Doctrine and the reasoning behind each field: `.claude/skills/author-game-v2/references/the-want.md`.
> **Re-read this before every release.** Bump `want.last_read_at_release` in `v2_state.json`.

---

## 1. Who she is

**Cass Renfro, 23.** The crew is her father **Boyd**, her brothers **Wade** and **Emmett**, her
uncle **Prine**, and four men who are not family. They follow the picking — nine weeks at the
Halbrook place, then the next one, then the next. They live in two vans and a camp trailer parked
on the packing yard, forty feet from the shed where the peaches get weighed.

The crew is paid by the bin, and the whole crew's take goes through Boyd, because Boyd's name is
the one on the contract. Cass has picked six seasons. **She has never held her own money.**

**What she has to lose:** the back bunk in the trailer. She is the only woman on this crew and
that arrangement exists because her father says it does. No car, no money, and nine miles of dirt
road between the gate and the highway.

## 2. The appetite that never fills

**To be wanted by men she shares a wall with, in a place with nowhere at all to do it.**

It cannot finish. Every notch further is also a notch more visible; the crew is always twenty feet
away; and the season ends and starts again somewhere else with two of the same faces and two new
ones. There is no state of affairs that settles this — there is only how far in she is when the
trucks load out.

**What does release 41 add?** A new man on the crew, a new building on the property, or an hour of
the day she stops working. **The crew turns over between seasons — two faces change and the blood
does not**, so the cast is renewable without the taboo ever resetting.

## 3. What she is becoming — as ACCESS

**Bottom.** She works the rows. She sleeps in the back bunk with her brothers on the other side of
a wall she can hear through. She washes at the camp showers with a towel and somebody standing at
the gate. There is not one place on this property where she can be alone with anyone for two
minutes, and everything she does, she does on her way to somewhere she is expected.

**Top.** She has the cooler key and the shed after the scale is shut. The truck cab. The loft over
the barn. The cooler is the only lock on this farm and she is the one holding it. She decides who is in the trailer at night,
and the crew works around where she is instead of the other way round.

### The ascent tiers

`who_climbs = "both"` — **two player tiers as the FLOOR, per-character meters as the SPINE.**

Deliberately **not** 15/35/55/75. The field runs 8–17 rungs with the lowest at a median of **5**;
all sixteen tiers across our five earlier games put the lowest at exactly **15**, which means the
first fifteen clicks of the game change nothing.

| tier key | what going further means on this axis | rungs | ceiling |
|---|---|---|---|
| `nerve` | the floor on **where** — what she will do in a place with that much cover, with that many people that close | 4 · 8 · 12 · 18 · 25 · 33 · 42 · 55 · 70 · 85 | 100 |
| `known` | the floor on **who knows** — whether it stays between two people, or the crew starts acting on it | 5 · 10 · 16 · 24 · 34 · 46 · 62 · 80 | 100 |

`known` **rises and widens.** The crew acting on what it knows is content, not punishment — a
player meter that quietly closes doors fails the ascent gate.

**Counterweight: none.** Deliberate. One game in twenty-five has a counterweight that gates
anything, and four of our five shipped one that gates almost nothing.

**Throttle: `arousal`** — declared *with* the first node-routed act loop and never before it. Its
only job is gating the **act menu** on that loop. Our five earlier games raise arousal 232 times
and read it 4 times; in the field a sexual-state meter is the #1 or #2 most-gated thing in half the
corpus.

### The cast's meters — four different shapes across five people

| character | the relationship is | what gates the rungs |
|---|---|---|
| `npc_boyd` | leverage / transactional | **the book** — what she owes against bins not yet picked, and what he is holding back. Not affection |
| `npc_wade` | slow burn / escalation | **willingness**, warmed by the throttle. Rich arc #1 |
| `npc_prine` | slow burn / escalation | **willingness**, warmed by the throttle. Rich arc #2 |
| `npc_emmett` | antagonist / witness | a **hidden accumulator** of what he has seen. Never surfaced |
| `npc_rae` | the standard | **no climbing meter.** Presence and one opened flag. She is the mirror, not a conquest |

Only Wade and Prine get the rich two-meter model. Gold-plating the whole cast dilutes the core and
triples the authoring.

## 4. The charge

- **Taboo — PRIMARY, and proximity *is* the transgression.** Not a locked room and a secret: two
  vans, a trailer, a wall she can hear through, and a crew that is never further away than the
  yard. The thing that makes it transgressive is the thing that makes it nearly impossible, and
  they are the same wall.
- **Transformation — secondary.** She arrives as somebody's daughter on the crew list, a body the day
  moves from the rows to the scale to the bunk. She becomes the reason the crew arranges itself.
- Reversal is *not* claimed. Boyd's hold on the money is real and it does not flip; it gets
  **used**, which is a different thing and belongs to his book.

## 5. The world

**Where does this happen?** The Halbrook place — a peach farm nine miles off the highway, worked
nine weeks a season by a crew that does not own any of it.

**What is outside the door she wakes up behind?** The packing yard. She steps out of the trailer
onto the ground the whole game sits on: camp and vans to one side, the shed and the cooler to the
other, the rows running uphill behind, the owner's house across the gravel, the barn at the far
end, one dirt road out. **The yard is the root and everything hangs off it** — the world contains
the camp, never the other way round.

**How far can she get, and what stops her?** Nine miles to the store and the highway, and she has
no car, no license on her, and no money that is hers. The truck goes when somebody with keys says
it goes.

**Which shape is this?** — `nested_zones`. A property *plus* a camp, zone → venue → room.

**What does her body need here, and what stops when it goes unmet?**

| need | falls | shuts |
|---|---|---|
| `energy` | with every bin | below 25 she cannot take a row or get up the ladder |
| `hygiene` | in the heat and the dust, fast | below 35 Rae turns her out of the canteen and two men will not be near her |
| `thirst` | fastest of the three, and only in the rows | below 20 the row choices are gone — she has to come down to the yard |

**How alive?** Living world. The crew has a working day she did not start and does not stop:
weigh-out happens whether she is at the scale or not, and the yard has traffic at hours she is not
in it.

## 6. Why *this* person

| character | why they are wanted |
|---|---|
| `npc_boyd` — her father, 47 | His name is on the contract, so every dollar she has ever earned passed through his hand before it reached hers. Being wanted by the man who holds the book is the only way the book stops being the whole of what is between them. |
| `npc_wade` — her brother, 26 | The loud one. He has been crude about her to the crew, where she can hear, since she was nineteen, and has never once been told to stop. He is already saying it; the climb is him saying it *to* her. |
| `npc_emmett` — her brother, 20 | They were close and then in March he stopped talking to her and will not say why. He is the one who sees things. Being wanted by him means finding out what he already knows. |
| `npc_prine` — her uncle, 48 | Boyd's brother, third van, sleeps alone, takes no days off in nine weeks. Patient in a way that reads as safe right up until it doesn't, and she is the one who keeps mistaking one for the other. |
| `npc_rae` — runs the canteen and the scale, 50s | Twenty crews. She names what the men are doing before Cass has words for it, and she does not soften any of it. Cass wants to be told she is handling it — by the only person on the property qualified to say so. |

## 7. Register

- **`narration_person` = `second`** — declared once, **immutable** after 0.1 ships.
- **Crude-vocabulary ceiling.** The actual words, per character, per band of that character's own
  meter. A ceiling described abstractly gets written around. **This is a ceiling and never a
  floor** — writing under it is the defect.

| character | t1 | t2 | t3 |
|---|---|---|---|
| `npc_boyd` | nothing named — the shape of her, how she has filled out, what she wears to work in | tits, ass, wet, hard, cock — flat, once, the way he reads a weight off the scale | cunt, fuck her, come in her — stated, never performed |
| `npc_wade` | already crude *about* her, to the crew, where she can hear: tits, ass | crude *to* her: cock, wet, hard, suck, fuck | cunt, cum, choke, hold still, come on your tits |
| `npc_emmett` | nothing. He looks, and then he stops looking | hard, cock, tits — said badly, and he takes none of it back | cunt, fuck, cum, please |
| `npc_prine` | nothing named — how long she has been on, whether she has had water | cock, tits, wet, hard — unhurried, like he has all season | cunt, ass, fuck, cum in her — still unhurried, which is the worst of it |
| `npc_rae` | crude about the *crew*, as trade talk, never about herself: cock, tits, fuck, cunt | — | — |

- **Where the crude register lives — five surfaces, every one re-enterable, every one on the
  standing map from 0.1:**

  **the showers · the packing shed after the scale is shut · the truck cab · the far end of the
  rows · the trailer bunk at night.**

  Nothing crude is held back for a one-time capstone. The measured failure this game is built
  against wrote its explicit register only into scenes the player sees once and wrote its
  fifty-times-replayed loops as character study.

---

## The four checks

1. **What does release 41 add?** A new man on the crew, a new building on the property, or an hour
   of the day she stops working. The road supplies men and the season supplies hours; neither runs
   out.
2. **What can she reach at the top that she cannot at the bottom?** The cooler, the loft, the cab,
   the shed after the scale is shut, the one door that locks — and who is in the trailer at night.
3. **Which character would a player miss if deleted?** **Rae.** Cut her and nothing Cass does is
   measured by anyone who has seen twenty crews. Boyd is leverage and the brothers are appetite;
   Rae is the only read on this worth having, and the canteen is the game's only mirror.
4. **Which repeatable surface carries the crudest writing?** **The showers.** Communal, no lock,
   a gate instead of a door, entered daily from 0.1 onward.

---

## Amendments

**0.1 — `npc_halbrook` and `the_porch` deferred to 0.2.** A whole unit, cut before the writing,
never a thinning of everything. He was the only cast member with no ladder at 0.1 already, so the
deferral costs the least real content; `the_store` would have taken the economy's main sink and the
only renewable source of new faces with it.

**0.1 — the locking door is the COOLER.** The ascent used to promise *"the one door on this
property that locks"* and mean the porch. `the-map.md` R2: a room the Want promises must exist. It
also settles a contradiction the board shipped with — `intro_packing_shed` calls the cooler *"the
only lock on this farm"* while the porch said its own door locked too. Only one of those can be
true, and now one is.
