# The Arc — what happens between the introduction and the loop

## Why this file exists

Every v2 game builds the same thing for every character: a meeting, a hub to talk at, one
repeatable sex surface, and a few walk-ins. Nothing sits between the meeting and the surface.

The field builds a **numbered arc of one-time steps that ends by turning into that surface**,
and the first third of the arc has no sex in it at all. We author the last step and skip the
six that earn it.

This was read, not counted. Five arcs end to end in three of the corpus's female-lead games —
`course-of-temptation` (rank 5), `zaras-school-life` (22), `family-ties` (24), which per
`~/Documents/Female_PC_Craft_Study_20260823/gender_verdicts.md` are the only clean female-PC
games in the top thirty.

⚠️ **Two things this file is NOT, because both were proposed in the session that produced it
and both were wrong.**

- **It is not about how much sex a game has.** Degrees of Lewdity, the game every founding
  commitment was measured on, has the **lowest** explicit share in the 25-game field — 4.8% of
  passages against our median 9.3%. The field's own spread is 5%–62%. There is no house ratio,
  and a volume target is exactly what SKILL.md's "ask what a tired author would build" rules out.
  ⚠️ **Volume has its own instrument and it is deliberately not a gate** — `lint_explicit_volume`
  prints the count and the rate against the field on two bases and judges neither. **This file is
  not that lint's doctrine and does not point at it as a target.** A game can be short of explicit
  screens because it has no arcs, and adding screens without arcs is the failure the lint was
  built as a lint to avoid.
- **It is not a claim that the field keeps sex rare inside an arc.** Course of Temptation's
  harasser runs 111 passages with 20 explicit; Zara's five detentions are 15 passages and all
  15 are explicit. Same shape, opposite density. **The shape is the finding; the density is a
  house decision.**

## What this file owns, and what it does not

| the question | the file |
|---|---|
| **what happens between meeting someone and the repeatable surface** | **this file** |
| which screen a piece of content lives on | `the-surfaces.md` |
| how the prose reads once they click | `register.md` |
| the introduction itself, and the first hour | `the-first-hour.md` |
| which meters exist, and what the climb costs | `the-meters.md` |
| what a release has to clear before it ships | `the-release.md` |

`the-surfaces.md` R3c is the nearest neighbour and it stops one step short — it is the ladder
across visits of a surface that already exists. This file is how that surface came to exist.
R3c's own closing line about the scene where she explains the pause is *"Nothing else in this
skill has a name for that scene."* A2 and A3 below are that name.

⚠️ **Pronouns here are `she/her` because `want.player` defaults to `female`. They are
downstream of that declaration — swap them if the game declared otherwise.**

⚠️ **How to read the evidence blocks.** Every rule states its **shape** first, as a set to
choose from. The quotation under it is fenced as EVIDENCE and names the game it came from.
This is not decoration: `templates/board.toml` shipped `airer` and `£5` and put five games in a
dialect the genre does not use, and its example rung of 15 was copied by all sixteen declared
tiers across five games. **Every word in an example is being taught too.** Take the mechanism.
Leave the furniture.

---

## A1 · An arc is a numbered ladder of one-time steps that ends by converting into a repeatable

**The shape:** N one-time steps, each gated on the flag the step before it set · the last step
turns the act into something she can simply do · doing *that* repeatedly opens the next act.

The repeatable surface is the **reward for finishing the arc**, not the starting position.

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** `family-ties` (rank 24) ships its own quest log for the
> husband's-brother arc. Nine steps, and steps 7 and 8 are the conversion:
>
> - 7 — *"Now you can wank to \[him] just by approaching him and chatting. Jerk him off again
>   if your corruption is above 60."*
> - 8 — *"Now you can give \[him] a blowjob. Keep sucking on him to move on."*
>
> `course-of-temptation` (rank 5) closes the same way — *"after you follow one of these paths
> to its conclusion, The Classroom Harasser will become like any other character and your
> relationship can evolve in whatever direction you'd like."*

**Ours, measured 2026-09-01 across twelve built games and 1,396 canvases: zero arcs.** No
character has a second thing that happens, a third, or a fourth. Every hub and every act loop
in this repo is authored in its converted state on day one.

**Length.** Family Ties runs 9 steps, Course of Temptation 10. Both are one character. **This
is a shape, not a quota** — nothing in the field supports a required number and no gate reads
it. What is not defensible is zero.

---

## A2 · The first third has no sex in it — it buys access and information

**The shape:** the opening steps teach the player two things and nothing else — **when this
person is alone**, and **what they are vulnerable about**. Both are things the player then uses.

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** `family-ties`, steps 0–3, verbatim from its quest log:
>
> - *"Go to the kitchen on any weekend at 7 a.m."*
> - *"Go to the living room at any time, when \[he] is at home and when your husband is not at home."*
> - *"Talk to him about the incident in the bathroom."*
> - *"Keep watching him in the living room when your husband is not home or sleeping."*
>
> `course-of-temptation`, harasser steps 1–3: get invited to the Media Production Lab → visit
> any evening in its window → keep visiting on successive days → *"You've learned that \[he] is
> here on a scholarship."*

The scholarship is the whole dominant route's leverage and the game does not hand it over. It
is paid for with three visits. **Information the player earns is a rung; information the game
narrates is exposition.**

Note what steps 0–3 are made of: a **place**, an **hour**, and **who else is in the building**.
That is `the-clock.md` and `the-map.md` doing arc work. An arc opening needs no new systems.

---

## A3 · The refusal is a written step — counted, warned about, and routed

**The shape:** the refusal writes a counter · a threshold prints, in plain words, exactly what
will close · the last refusal opens something else. Three parts, and the third is the one
nobody builds.

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** `family-ties` step 4 is a refusal the game *authors for
> her*, not one it offers:
>
> *"\[He] caught you caressing your pussy while watching him and invited you to join in. **You
> refused and left**, but you understand that he will continue to do so in the hope that next
> time you will not refuse…"*
>
> `zaras-school-life`, `bench event5`. Declining costs nothing and sets `$cooldownDick`,
> `$dick.rejectDay = $dayCount`, `$dick.rejectTimes += 1`. On the third:
>
> *"Warning: This is the last time you can reject this NPC, after this, they will be locked
> forever. Things you will miss: Park bench events, FFM events with cucking, money making
> system and several quests."*
>
> And the fourth sets `$lisaDaysLeftForIntro = 3` — **refusing him starts a different
> character's introduction three days later.**

Three rules fall out, and the first two already exist elsewhere in weaker form:

- **The refusal is free and in character.** `the-surfaces.md` R5b already says it is written at
  full length. This adds: it is also *remembered*.
- **A door may close, but out loud.** `the-want.md` §1 already carries this from
  `the-company`'s *"If a choice locks you into a sub route, tell me that."* Zara's warning is
  the strongest version in the corpus — it **names the four systems being forfeited**, not the
  fact that something is.
- **A refusal routes.** This one is new to the skill. Saying no is not a dead end and not a
  punishment; it is a fork that hands the player a different person.

**Ours:** across every v2 game, no refusal is counted, nothing warns that a door is closing,
and no refusal opens anything. `night_desk` is the closest — it authors refusal nodes and an
NPC whose mood colours his rungs — and its refusals are **his**, not hers.

### A3b · And the default refusal is PARKED, not closed — the game names where to go back

Added after a second reading round. A3 above was built on the one case in the corpus where a
refusal is permanent, and read as a whole rule it is too harsh. **The field's ordinary refusal
costs nothing, changes nothing, and tells the player the address at which it can be reversed.**

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** `family-ties` (rank 24), two separate arcs, from its own
> quest log:
>
> - *"You said no to shooting amateur porn, but **if you change your mind later, just talk to
>   your husband in the bedroom when he's there**."*
> - *"Your husband caught you two having some fun and offered a threesome, but you said no.
>   **If you change your mind, just talk to him any time when they are both at home**."*

So the two shapes sit at opposite ends and an arc picks one deliberately:

| | the refusal | when to use it |
|---|---|---|
| **parked** | free, reversible, and the game prints the place and the hour | the default. Most offers |
| **counted** | tracked, warned with the content named, and finally closed | when the closing is itself content — A3's Zara case |

Writing every refusal as permanent makes a game a minefield. Writing every one as parked makes
nothing matter. **The one thing neither shape does is stay silent about which it is.**

---

## A4 · The step raises the number that opens the step after it — and only while she is under it

**The shape:** the scene grants the meter it is gated on, capped at the next threshold, so
repeating a scene at the bottom walks the player up it. The climb is fed by the content it
opens, not only bought elsewhere.

`the-meters.md` M1–M5 owns the other half of this — every meter a gate reads carries a brake on
the rungs that raise it. **This is the same seam from the other side, and the two must be read
together or the result is either a free elevator or a wall.**

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** `family-ties`, `hisBroFapEvent1` — one scene, eleven pages.
> Each page:
>
> - scales its arousal grant by where she already is — `if corr < 30: arousal += 5, else += 10`
> - offers **exactly two buttons**: one step further, or leave
> - prints the number on the one she cannot take — `Req for corruption: 15`
> - and grants `corr += 1` **only while she is below the next threshold**
>
> Watching him is what makes her able to do more than watch. `zaras-school-life` states the
> locked door the same way: *"Zara does not have enough corruption to fuck him or is too
> tired… Required Corruption: 30. Required Energy: 20."*

Two exits per page is the whole navigation of an eleven-page scene. Compare the act-menu figures
in `the-surfaces.md` R3b — field median 2 options, span 1. **The same narrowness, applied down
the page instead of across the menu.**

⚠️ **The locked-door text here is the `a locked door says why` gate's subject** (`engine.md`
§15, §36 · `the-surfaces.md` R5c). Both field games print the bar and the number. Ours run 100%
mute where they show a locked row at all.

### A4b · "The number" is wider than a meter — a practised skill and a bought preparation both count

Added after a second reading round, because A4 as written assumes the only key is a meter the
scene itself raises. **The field's keys come in three kinds**, and an arc usually spends more
than one:

| kind | what the player does to get it | example gate |
|---|---|---|
| **a meter the scene feeds** | repeat the scene at the bottom of it | A4 above |
| **a skill practised elsewhere** | go and do the act somewhere it is already allowed | *blowjob skill 20* |
| **a preparation bought and endured** | buy the object, then spend days using it | *three nights with the plug in* |

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** `family-ties` (rank 24) gates its arc steps on
> `blowjob skill 20` and `40`, and `deepthroat 35`, `50` and `60`. **The deepthroat number has
> its own whole ladder whose only purpose is to feed three other arcs:** read tips on the
> internet → buy a dildo at the sex shop → practise in the bedroom while he is out → reach 35 →
> go to the bar toilets in the South District → look up better technique on a computer → at
> corruption 50, the last booth — *"Now you can practise your deepthroat skills in the bar's WC."*
>
> And its anal step is not a scene at all until the preparation is done: *"You need to go to the
> pharmacy to buy an enema and to the sex shop to buy lubricant and pick up an anal plug"* →
> *"use an enema and try on a butt plug. The bathroom should be free"* → *"Three days using an
> anal plug will be enough. **Go to sleep with the butt plug in, so the counter will be
> activated**"* → then talk to him between 21:00 and 23:00.

Note what that second one does to the economy: **money buys the key to a rung, not a stat.**
That is `the-economy.md` R1b — what money buys has to stay bought and be read — arriving from
the arc side rather than the ledger side. A shop that sells an arc's prerequisite is doing more
work than a shop that sells a meter point.

⚠️ **A skill ladder that feeds nothing is a chore.** The deepthroat line is only worth its seven
steps because three other arcs read the number. Build the reader first.

### A4c · The field's meters are READ, ours are WRITTEN — and the gate cannot see the difference

The same seam from the outside. Measured 2026-09-01 on each side's own instrument:

| | conditions reading it | sites writing it |
|---|---|---|
| `zaras-school-life` `$PlayerCorruption` | **2,117** | 4 |
| `new-life-project` `$corrupt` | **247** | 2 |
| `new-life-project` `$inhib` (inverted — LOW opens things) | **105** | 2 |
| `forty_miles` arousal | **0** | 52 |
| `steam` arousal | 2 | 55 |
| `back_home` arousal | 2 | 47 |
| `mrs_vance` want | 10 | 65 |
| `the_season` arousal | 6 | 24 |
| best of ours — `off_season` ease | 27 | 11 |

⚠️ **The two instruments are NOT the same and the magnitudes do not compare.** The field figures
count textual occurrences in built HTML, where a single centralised setter widget called from
everywhere reads as "4 writes"; ours count authored condition objects against authored effect
objects in the TOML. **What survives the difference is the direction**, and one row survives it
outright: `forty_miles` writes arousal 52 times and reads it zero.

**Why the scoreboard is quiet about this.** Gate `a meter is read` asks, per meter, whether it is
read *at all* — so it correctly fails `forty_miles` (4/8) and `steam` (6/7), and it passes
`the_season` 9/9 while that game's arousal sits at 6 reads against 24 writes. It finds **dead**
meters. It cannot see a **starved** one. `the-meters.md` W3 owns the gate; this is the note that
the gate's silence is not a pass.

---

## A5 · One incident, two ladders — and the routes read different meters

**The shape:** write the incident once. Her answer routes it. Two arcs share one trunk, and the
two arcs are gated on **different meters**, so one climb does not deliver both.

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** `course-of-temptation`. The harasser steals her homework,
> crosses out her name, writes his — *"You'll get a zero on the assignment if you let this
> happen."* One incident, two outcomes:
>
> - **allow it** → the submissive path, gated on `submissiveness ≥ 300` (*"You understand how
>   to be submissive"*), `exhibitionism ≥ 500`, `inhibition ≥ 300`, his Dominance `≥ 600`
> - **sabotage it, and complain to the professor** → the dominant path, gated on
>   **assertiveness**: *"It would be nice to do something about it. If only you were more
>   assertive…"* — plus *"publicly embarrass him"* three times
>
> Its walkthrough is honest about the geometry: *"You can follow both paths until you get
> almost to the end, but pursuing either path will make the other more difficult **as it's a
> question of control**."*
>
> And both ends arrive at the same handoff — *"He knows something about film production. You
> should talk to him about the offer from Smashers Studios."*

Three things worth taking:

- **A slope, not a lock.** Pursuing one route makes the other harder, and nothing slams. This is
  the fifth commitment arriving in arc form: a condition that *selects a branch* buys more than
  one that shuts a door.
- **A second meter is what makes a second route real.** Corruption alone cannot express *she
  will do anything and still cannot say no to him*. Read next to `the-meters.md` W1 — the
  question of who climbs — because two routes means two ladders to declare.
- **The arc ends by pointing at another arc.** Neither path terminates. Both hand over.

⚠️ **Blockers are declared in the same list as requirements.** Both CoT paths refuse to
conclude while she is wearing a chastity device; the submissive path also refuses while she is
in an exclusive relationship. A social or worn state that stops an arc is stated up front on
the same checklist as the numbers, never discovered at the last step.

### A5b · The ladder has three directions, and A5 describes only one of them

Added after a second reading round. A5 above is a *contest* — two routes fighting over control.
That is one of three shapes in the corpus, and the other two are more common:

| direction | what climbs | the question the arc asks |
|---|---|---|
| **hers** | her willingness | how far will she go |
| **theirs** | his or her willingness | how do I get them to agree |
| **a contest** | control, either way | who ends up owning whom |

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** All three, one line each:
>
> - **hers** — `family-ties` (rank 24): she watches, is caught, refuses, joins, and only then
>   does the act become available.
> - **theirs** — `zaras-school-life` (rank 22), and its quest journal says it in the same words
>   nine times: *"Zara attempts to unlock Kyle's mind to accept blowjobs from her."* She is the
>   aggressor throughout; what is gated is **his** consent, not hers.
> - **a contest** — `course-of-temptation` (rank 5): *"pursuing either path will make the other
>   more difficult as it's a question of control."*

**Declare which one an arc is before writing its first step**, because it decides who the
refusals belong to. A3's counted refusal is hers in one direction and *his* in another —
`night_desk` already ships refusals that are his, and until now nothing in this skill said that
was a legitimate shape rather than a slip.

⚠️ **One template, stamped per person, is a normal way to build a cast.** Zara runs
brother / father / mother × quest 1 · 2 · 3, with the act list swapped for the pairing (the
mother's three are fingering, oral and a strap-on) and an item requirement on the last —
*"Zara has to travel to Cox and Co. in the mall to buy a strap-on."* Nine arcs from one shape.
**The saving is real and so is the risk**: the three read as one character three times unless
each pairing's acts, refusals and aftermaths differ. See `the-surfaces.md` R8 — a person owns a
corner of the world.

---

## A6 · A garment is a rung, and clothing moves the odds the world acts

**The shape:** two jobs, and they are different. A garment can be **a step the arc will not pass
until she wears it**, and clothing can **change how often the world does something**, without
changing what it does.

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** `course-of-temptation`, submissive step 7. It asks her to
> do nothing at all. It asks her to *wear* something, and lists what qualifies with a
> checkmark each: *"Try wearing a skirt that can flip up."* · *"…a top that might expose your
> nipples."* · *"…a top that shows cleavage."* · *"…a top that shows off your muscles."*
>
> `zaras-school-life`, the park-bench dispatcher — clothing moves the floor of the roll, not
> the outcome:
>
> ```
> if wearing Slutty:  chance = random(50,100)
> else:               chance = random(1,100)
> if chance >= 65:    → an incident
> ```
>
> Dressed ordinarily, something happens **36%** of the time. Dressed slutty, **71%**. Same seven
> scenes. Twice as much world.

The gate `the wardrobe is read` asks only whether a declared `[[clothing]]` catalog is read
*anywhere*. This says where it earns its keep: on a rung, and on a rate. `the-meters.md` W7 and
`engine.md` §17 own the mechanism (`worn_exposure` is the predicate that reads an empty slot).

### A6b · Somebody else can set the dress code — and showing by accident is not showing on purpose

Added after a second reading round. A6 above assumes she picks what to wear. Two things it misses:

**A dress code can belong to an employer, and then it is a ladder she is put on rather than one
she climbs.** The arc content is her reaction to each rung, not the choosing of it.

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** `course-of-temptation` (rank 5), the bar job. The owner
> changes the uniform: **Traditional → Sporty → Classy → Sexy → Topless**. The first topless
> shift is its own scene, and it branches on whether she *liked* it — `FirstTimeToplessLike`,
> `FirstTimeToplessDislike`, `FirstTimeToplessFlaunt` — and a dislike branches again on whether
> she switches back (`DislikeYesSwitch` / `DislikeNoSwitch`).

**And the same reveal is two different events depending on whether she meant it.** Its streaming
job carries `showonstream` and `showonstreamaccident` as **separate widgets** (and each again for
underwear), and the workout stream alone ships six accident events — downblouse, sideboob,
underboob, upshorts, skirt flip, shirt burst.

That is `register.md`'s reason axis — *she decided* against *her body decided* — arriving on the
wardrobe. **The deliberate version and the accidental version of one reveal are two beats, not
one beat with a modifier**, because everything downstream differs: what she says, what they say,
and whether it counts as a rung.

---

## A7 · A dispatching place keeps a quiet outcome, and the quiet outcome pays

**The shape:** most visits to a place produce nothing, the nothing is written several ways, and
it returns something the player wanted anyway — rest, time, a small restore. Sitting down is a
real action that *might* turn into something.

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** `zaras-school-life`, the park bench. When the roll comes up
> short — **64% of ordinary visits** — it picks one of **five** written quiet benches, advances
> 30 minutes and grants `+15 energy`. Nothing happens, at length, five different ways, and the
> player is better off for having sat down.

**Ours** (`gates.py` lint · dispatch depth, 2026-09-01): the deepest dispatching activity in
the repo turns into **5** different things (`off_season`, `work_arcade_morning`); most turn into
1–3; and in `night_desk` and `the_route` **every** dispatching activity has exactly one
outcome, so the roll decides only whether the branch fires, never which branch it is. The
field's own reference figure in that lint is DoL's Bath at 12.

A quiet outcome is what makes the loud one worth waiting for. A place where something always
happens has no tension in the click.

---

## A8 · A pending arc beat pre-empts the dice

**The shape:** before rolling for a random incident, check whether an arc is waiting for its
next step. If it is, and its conditions hold, it fires. Arc content does not queue behind chance.

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** `zaras-school-life`, the same dispatcher, first lines,
> above the roll:
>
> ```
> if $dick.metFlag == false and $dick.rejectTimes <= 3
>    and $PlayerCorruption >= 10 and $cooldownDick == false
>        → goto "bench event5"
> ```
>
> Four terms: not yet met · has not run out of refusals · corrupt enough · off cooldown.

**This is available here, and precisely.** Entry-time auto-fire redirects the passage before the
location screen renders (`getStoryCanvasRedirect`, `v2.py:4921`), and among the candidates
`selectAutoFireCanvasForLocation` (`v2.py:4622`) takes the **highest `priority`**
(`v2.py:4633-4634`) — already how `off_season`'s `canvas_meet_tam` beats `canvas_tam_saw_you`. So
an arc beat is a one-shot at the location, priced above the other one-shots that could fire there.

⚠️ **It is the auto-fire queue it wins, not the dice.** That selector skips
`triggerMode == "random"` and `substitutionOnly` canvases outright (`v2.py:4630-4631`); random
ambients and substitutions are a separate selector on the location screen. The redirect happening
first is what gives the same effect as Zara's pre-empt — the player never reaches the roll — but
the two are different mechanisms and the caveats do not carry across.

---

## A9 · The incidents at one place are different setups, not different acts — and they span the whole meter range

**The shape:** one place carries several one-time or occasional incidents. What differs between
them is **not which act is on offer**. It is the setup — who holds power, who moves first, and
what the pretext is. And their gates spread wide enough that the same place still has something
to give at the top of the game.

**The menu to choose from** — every one of these is attested in the two games below, and the
list is a set to pick from, never a set to complete:

| setup | who moves first |
|---|---|
| she catches him doing something private | her |
| he catches her doing something she should not | him |
| a peer, nobody holding anything over anyone | either |
| someone worn out, sad, or humiliated — no threat at all | her, as help |
| she is caught looking | him, on her tell |
| she watches two other people, and one of them sees her | the third party |
| a stranger prices her out loud — a toll, a demand, a deal | him |

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** `zaras-school-life` runs seven incidents on one park bench
> and five in one detention room. The detentions are five *power* situations, not five acts:
> she catches a teacher · the coach catches her leaving · a peer arrives · an exhausted teacher
> needs help · she is caught staring at a married one. The benches include a man crying over a
> break-up, a man who scans her body from the feet up, and a couple she interrupts where **the
> woman locks eyes with her**.
>
> Their gates spread from **corruption 5** on the solo bench to **80** on the couple. One bench
> serves a first-day player and an end-game player with completely different content.

⚠️ **A cheap in-fiction cause can buy an early rung.** Zara's toll scene happens at corruption
10 because the boy sprays himself with something that makes her wet before she has decided
anything. That is `register.md`'s reason axis — *she decided* against *her body decided* —
built as a **plot object** rather than a paragraph of interiority. Used once it is a gift; used
on every rung it is the game apologising for its own content.

---

## A10 · The act ends on a written beat, and the beat is about who it was

**The shape:** after the act completes, one short beat, no sex in it — **how they leave · what
she is left holding · the offer to stay or go.** Written per partner, because the aftermath is
the only part of a repeatable act that can carry who the person was.

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** `course-of-temptation` (rank 5) ships **74 `*Post` passages,
> median 32 words** (range 10–122), and every partner type at one surface has its own —
> `GenericPost`, `HarasserPost`, `MeanPost`, `ServicePost`, `TowniePost`, `FilmPost`. The
> generic one, entire, at 60 words:
>
> *He pulls away and catches his breath for a moment. "Hell yeah. Thanks for that."*
> *"Don't mention... it..." you start to say, but trail off as you realize he's already gone.
> Sheesh, where's the fire?*
> *Once you've caught your breath and redressed, it's time to decide if you're done here now
> or not.*

Read what those sixty words do: **he is rude, she notices being left, and the loop asks whether
she is staying.** Three moves, one of them a small sting that belongs to that partner and no
other. Swap him for the one labelled `Service` and all three change.

⚠️ **This is the clearest gap in the repo and it is not a matter of degree.** Measured
2026-09-01 across six v2 games: **23 of 23 `finish` / `climax` / `cum` / `end` nodes have an
empty `exit_block`.** The act completes and the canvas stops. `commuter`'s finish beat is
seventeen words — *"The machine finishes its cycle and goes quiet, and the garage is only the
one light again"* — and nothing follows it anywhere.

**It is also the cheapest thing in this file to build.** Thirty-two words and one choice, on a
node that already exists.

⚠️ **The aftermath is not the climax.** A finish beat is the last beat *of* the act and is
written at the register the act was. The aftermath is *after* it, and A2's rule applies in
reverse — it is the one place in a sex surface where interiority is the point rather than the
pivot defect (`register.md`, "Where the interiority goes instead").

---

## A11 · Stopping partway is a written outcome, and it is not the same as saying no

**The shape:** three different exits, three different scenes.

| exit | when | what it is about |
|---|---|---|
| **refusing** | at the door, before anything | whether she wants this at all — A3 |
| **stopping** | mid-scene, with it already happening | how he takes being stopped |
| **chickening out** | after she already agreed | what she owes, and what it costs to renege |

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** `course-of-temptation` ships **113 `*Abort` passages**
> (median 23 words) and **5 `*Chicken`** passages, the latter reached only from a dare already
> accepted — `UltimatumChicken`, `UltimatumDefyChicken`, `ChattingDebateChicken`,
> `ChattingTNTLChicken`.

⚠️ **We already do this in one game, and nothing taught it.** `commuter` writes a stop beat on
all seven of its loops, at 27-59 words (median 29). The longest:

> *"You stop. He does not argue about it and he does not ask why, and he puts himself away and
> sits back down in the chair like the rest of it did not happen."*

That is the rule executed correctly — **the beat is about his reaction, not her exit.** One game
of eleven. Every other v2 game routes its `Stop.` choice at a reset node and prints nothing.

⚠️ **An earlier draft of this reading reported we had none of this. That was wrong**, and it is
recorded because the error has a shape: the instrument was a name search, `commuter` was found
only on a second pass, and a rule written from the first pass would have told an author to build
something they had already built.

---

## A12 · The reason she is there is a SYSTEM, not a sentence

**The shape:** one act, reached through genuinely different machinery. Each route brings its own
negotiation, its own refusal, its own aftermath — and they are not variants of one scene with two
opening paragraphs.

**The menu, all attested in one game:**

| the route in | what it is really about |
|---|---|
| **a wager she lost** | she agreed to the terms before knowing the outcome |
| **a price somebody paid** | it is a transaction and both of them know the number |
| **an anonymous service** | there is no person to be seen by |
| **a dare from a third party** | somebody else is watching who is not involved |
| **an accident she did not intend** | it happened *to* her |

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** `course-of-temptation`, the same act arriving three ways:
>
> - **a wager** — inside a kart-race minigame of 40+ passages: *"Make this interesting," he says.
>   "The loser orally services the winner."* And the body is a move in the race —
>   `DistractWithCleavage`, `DistractedByMuscles`.
> - **a price** — on a stream, from a stranger in chat: *"Out of nowhere, somebody in chat makes
>   you a lewd offer. Showing your tits on stream? Even for a big tip, that seems crazy."*
>   → Flash / Refuse.
> - **anonymously** — a gloryhole with seven partner types, each running offer → abort → do →
>   post. **Only 3 of its 50 passages register as explicit**; the rest is arriving, being asked,
>   backing out, and the aftermath.

**This is `register.md`'s reason axis promoted from a prose rule to a design rule.** That file
says the same act reached two ways writes two different openings, and it is right. This says the
*route itself* is worth building — because a wager needs a game to lose, a price needs a payer,
and an anonymous service needs a wall.

⚠️ **A venue can be a set of games, and the stake can be the content.** The same party ships
beer pong, strip poker, trivia, a kart race and an oral contest, and it **outputs a relationship**
— `AddFuckbuddy`, `AddHatefuck`, `AddBully`, `AddVictim`, `GainCrush`. An evening ends with a
person attached to her in a named role. That is a source of new cast that costs no new location,
which is commitment 4 (*a release adds events, not places*) with a mechanism under it.

---

## The engine, verified

Every line here was read on 2026-09-01. `engine.md` remains the only file that may carry engine
facts; these are the ones this doctrine leans on, and they are repeated here only as pointers.

- **A1 is authored with flags today.** Each step is a one-shot canvas gated on the flag the
  previous step set, and the final step sets the flag that opens the repeatable surface.
- ⚠️ **The native primitive exists and is not wired.** `setup.selectCanvasByPriority`
  (`v2.py:4980`) implements A1 exactly — canvases sharing a `name` form a group, unvisited tiers
  play in ascending `priority`, and once all are seen it returns the highest-priority one
  forever. **Nothing calls it.** In `games/the_season/output/index.html` the symbol appears
  three times and is invoked zero times. The live path is `renderSoloActivities`
  (`v2.py:5242`), which drops every non-repeatable canvas (`if (!c.isRepeatable) continue`) and
  does no progression at all. **Do not point an author at it.** Wiring it is an open engine
  decision, not a thing this file may assume.
- **A8 is available** — highest `priority` wins on the auto-fire path (`v2.py:4633-4634`).
- **A6 is available** — `worn_exposure`, `worn_type`, `worn_corruption` and `worn_beauty` are
  condition predicates (`engine.md:532`; `worn_exposure` is the only one that reads an empty
  slot).
- **A4's grant-while-under-threshold** is an ordinary `[group]` band on the meter plus an
  `add` effect. ⚠️ Adjacent `[group]` blocks merge into one if/elseif chain and first match
  wins (`engine.md` §35) — separate the grant band from any other ladder on the same node with
  a non-`group` block, or the ladder below it goes silently unreachable.
- **Measured, ours:** zero tier groups across twelve games and 1,396 canvases — no two canvases
  anywhere in this repo share a `name` with different priorities.

---

## The check

**Nothing ships with this file, and that is deliberate.**

Two precedents rule it out. **P0** — never build a check for a state nothing is in: all twelve
games would fail almost every rule here on the day it landed, which measures the doctrine's age
and not the games. And **"a check that fails a game for obeying the doctrine is a bug in the
check"** — until today nothing in this skill asked for any of this, so every red would be
retrospective.

The candidates below are **lints**, not gates, and each is built only once one game has built
the thing — the order that produced `the start choice is read` (shipped after `mrs_vance` built
it first) rather than the order that produced P0.

1. **`a refusal is remembered`** — for every declining choice (the `she can say no` gate already
   locates them), whether its effects write a key that is read anywhere else. A list, never a
   score. Zero across the repo today, which is the finding, not a failure.
2. **`the arc ladder`** — the longest chain of one-time canvases per character where each is
   gated on a flag the previous one sets, printed beside the field's figures (`family-ties` 9,
   `course-of-temptation` 10). A number, never a bar — the field's own two data points are one
   game each and no threshold is defensible from them.
3. **`an act ends on something`** — every `finish`-class node whose `exit_block` carries no
   choices. **23 of 23 today**, so it is a list of the whole repo and therefore useless as a
   verdict; it becomes worth building the moment one game writes an aftermath.

⚠️ **A11 is the first rule here with a precedent game, and that changes the build order.**
`commuter` already writes a stop beat on all seven of its loops. Every other rule in this file
has zero examples in the repo, so **A11's check is the first that can honestly ship** — it would
read "1 of 11 games" rather than "0 of 11", which is a distribution rather than an indictment.
Build order is therefore A11's lint first, then whichever of the three above a release earns.

⚠️ **This file will be skipped.** That is not pessimism, it is this project's measured history:
the register pivot defect was authored three increments running, each time by someone who had
just re-read the rule against it, and only the per-beat scorer ever caught it. Until the lints
exist, an arc is authored on discipline alone, and the honest place to record that is
`the-release.md`'s log step — name in `v2_state.json` which of A1–A12 the release built and
which it skipped, with the reason.
