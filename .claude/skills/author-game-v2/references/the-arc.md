# The Arc — what happens between the introduction and the loop

## Why this file exists

Every v2 game builds the same thing for every character: a meeting, a hub to talk at, one
repeatable sex surface, and a few walk-ins. Nothing sits between the meeting and the surface.

The field builds a **numbered arc of one-time steps that ends by turning into that surface**,
and the first third of the arc has no sex in it at all. We author the last step and skip the
six that earn it.

This was read, not counted. Four arcs end to end in two passing female-lead games —
`course-of-temptation` (the harasser, the best friend, the roommate's partner) and
`in-her-own-hands` (Shaun) — with Cupid's Way and Shady Deals supplying single mechanisms. Where a
rule has no passing example, the evidence is a failing game's structure, named and labelled
"numbers only": its scenes are never used.

⚠️ **Two things this file is NOT, because both were proposed in the session that produced it
and both were wrong.**

- **It is not about how much sex a game has.** Degrees of Lewdity (numbers only), the game every
  founding commitment was measured on, has the **lowest** explicit share in the 25-game field — 4.8% of
  passages against our median 9.3%. The field's own spread is 5%–62%. There is no house ratio,
  and a volume target is exactly what SKILL.md's "ask what a tired author would build" rules out.
  ⚠️ **Volume has its own instrument and it is deliberately not a gate** — `lint_explicit_volume`
  prints the count and the rate against the field on two bases and judges neither. **This file is
  not that lint's doctrine and does not point at it as a target.** A game can be short of explicit
  screens because it has no arcs, and adding screens without arcs is the failure the lint was
  built as a lint to avoid.
- **It is not a claim that the field keeps sex rare inside an arc.** Course of Temptation's
  harasser runs 111 passages with 20 explicit; in one game (`zaras-school-life`, numbers only) five
  incidents at one place are 15 passages and all 15 are explicit. Same shape, opposite density. **The shape is the finding; the density is a
  house decision.**

## What this file owns, and what it does not

| the question | the file |
|---|---|
| **what happens between meeting someone and the repeatable surface** | **this file** |
| which screen a piece of content lives on | `the-surfaces.md` |
| how the prose reads once they click | `register.md` |
| **whether there is any prose once they click** | `the-surfaces.md` R9 — added 2026-09-02. This row did not exist, and a choice that produced no screen at all fell between all three of the rows above it |
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

The same split governs the prose (added 2026-09-24): the full loud version of a moment — the
reveal, the conversation, the hook — belongs on the one-time step, and the repeatable it converts
into stays short but still speaks. `register.md` L3.

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** `in-her-own-hands` runs Shaun as fourteen steps, and the
> thirteenth converts: once it is done, the ordinary repeatable flirt grows a new button, *"Take it
> up a notch . . ."*.
>
> `course-of-temptation` (rank 5) closes the same way — *"after you follow one of these paths
> to its conclusion, The Classroom Harasser will become like any other character and your
> relationship can evolve in whatever direction you'd like."*

**Ours, measured 2026-09-01 across twelve built games and 1,396 canvases: zero arcs.** No
character has a second thing that happens, a third, or a fourth. Every hub and every act loop
in this repo is authored in its converted state on day one.

**Length.** Course of Temptation runs 10 steps (the harasser), 9 (the best friend) and 12 (the
roommate's partner); In Her Own Hands runs 14 (Shaun). Each is one character. **This
is a shape, not a quota** — nothing in the field supports a required number and no gate reads
it. What is not defensible is zero.

---

## A2 · The first third has no sex in it — it buys access and information

**The shape:** the opening steps teach the player two things and nothing else — **when this
person is alone**, and **what they are vulnerable about**. Both are things the player then uses.

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** The opening steps, verbatim from the games' own quest logs:
>
> - `course-of-temptation`, the best friend: *"Stop by [his] dorm, in Chicory Hall, any evening
>   between 18:00 and 23:00."* The talk that matters is offered only while his roommate is out.
> - `course-of-temptation`, the roommate's partner: *"Take a shower some Saturday, Sunday, or
>   Monday, between 6:00 and 11:00."*
> - `in-her-own-hands`, Shaun, in her own voice: *"I wonder what Shaun does when he gets home from
>   the club . . ."* — the one slot he is alone is the kitchen at 2 a.m. on Sunday.
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

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** `course-of-temptation` records a refusal as a step of the
> arc, in the quest log — *"\[He] snuck into your shower, but you made your feelings clear."*
>
> The counted form, in the same game: each dare the roommate's partner sets and she refuses adds
> one to a count (`$rmpbully.resisted++`). At three he asks her straight, and the two buttons say
> in plain words what each answer does — *"(… will stop giving you challenges)"*. In Her Own Hands
> warns the same way: *"(Caution: This will be your final answer on the subject.)"*
>
> The routing half has one example, in one game (`zaras-school-life`, numbers only): the fourth
> refusal of one man starts **a different character's introduction three days later.**

Three rules fall out, and the first two already exist elsewhere in weaker form:

- **The refusal is free and in character.** `the-surfaces.md` R5b already says it is written at
  full length. This adds: it is also *remembered*.
- **A door may close, but out loud.** `the-want.md` §1 already carries this from
  `the-company`'s *"If a choice locks you into a sub route, tell me that."* That warning is
  the strongest version in the corpus names what is being forfeited, not only the fact that
  something is.
- **A refusal routes.** This one is new to the skill. Saying no is not a dead end and not a
  punishment; it is a fork that hands the player a different person.

**Ours:** across every v2 game, no refusal is counted, nothing warns that a door is closing,
and no refusal opens anything. `night_desk` is the closest — it authors refusal nodes and an
NPC whose mood colours his rungs — and its refusals are **his**, not hers.

### A3b · And the default refusal is PARKED, not closed — the game names where to go back

Added after a second reading round. A3 above was built on the one case in the corpus where a
refusal is permanent, and read as a whole rule it is too harsh. **The field's ordinary refusal
costs nothing, changes nothing, and tells the player the address at which it can be reversed.**

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** Two passing games, the same shape:
>
> - `course-of-temptation`: *"That could be the end of everything. Of course, they'll probably
>   be at it every weekend **if you ever change your mind**."*
> - `cupids-way`: *"Alright, I won't push. **If you change your mind just message me.**"*
>
> - `course-of-temptation`, the best friend: *"You don't have to go any further, but if you want to
>   then you can try again another night."*

So the two shapes sit at opposite ends and an arc picks one deliberately:

| | the refusal | when to use it |
|---|---|---|
| **parked** | free, reversible, and the game prints the place and the hour | the default. Most offers |
| **counted** | tracked, warned with the content named, and finally closed | when the closing is itself content — A3's counted case |

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

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** `course-of-temptation`, the night she overhears her roommate
> and his partner — one scene, five pages. Each page offers **exactly two buttons**: one step
> further, gated on a skill (*Listen in* at Voyeurism 1, *Sneak a look* at 2, *Touch yourself* at
> Disinhibition 2, *Finish yourself off* at 4), or stop (*"Rein it in!"*, a willpower check).
> Taking the gated step raises the skill that gated it, so listening is what makes her able to
> look. Where she is short, the game prints the bar: *"(Need Exhibitionism 4)"*. `shady-deals`
> states a locked door the same way: *"You can't launch an orgy, you need more girls working in
> here."*
>
> Two refinements have one example, in one game (`family-ties`, numbers only): the grant is
> scaled by where she already is (+5 below 30, +10 above), and the raise stops at the next
> threshold, so she cannot climb past a rung by repeating the one below it.

Two exits per page is the whole navigation of a five-page scene. Compare the act-menu figures
in `the-surfaces.md` R3b — field median 2 options, span 1. **The same narrowness, applied down
the page instead of across the menu.**

⚠️ **The locked-door text here is the `a locked door says why` gate's subject** (`engine.md`
§15, §36 · `the-surfaces.md` R5c). Course of Temptation and Cupid's Way (*"Drive with him
$corruption/20"*) print the bar and the number. Ours run 100%
mute where they show a locked row at all.

### A4b · "The number" is wider than a meter — a practised skill and a bought preparation both count

Added after a second reading round, because A4 as written assumes the only key is a meter the
scene itself raises. **The field's keys come in three kinds**, and an arc usually spends more
than one:

| kind | what the player does to get it | example gate |
|---|---|---|
| **a meter the scene feeds** | repeat the scene at the bottom of it | A4 above |
| **a skill practised elsewhere** | go and do the act somewhere it is already allowed | *Exhibitionism 2* |
| **a preparation bought and endured** | buy the object, then spend days using it | *three nights of a bought preparation* |

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** `course-of-temptation` gates the best friend's next step on a
> skill earned anywhere but with him: *"You need to be more confident in showing off your body.
> Wear more revealing clothing, and look for chances to show off your body."* (Exhibitionism 2).
> The same skill gates four other arcs, which is why practising it is worth the time. A bought key:
> in `shady-deals` a taser opens an exit and is used up, and without it the row reads *"If only you
> had a taser..."*.
>
> The endured preparation has one example, in one game (`family-ties`, numbers only): a step that
> is not a scene until a bought item has been used for three nights, and a practice ladder whose
> only purpose is to feed three other arcs.

Note what that second one does to the economy: **money buys the key to a rung, not a stat.**
That is `the-economy.md` R1b — what money buys has to stay bought and be read — arriving from
the arc side rather than the ledger side. A shop that sells an arc's prerequisite is doing more
work than a shop that sells a meter point.

⚠️ **A skill ladder that feeds nothing is a chore.** A practised skill is only worth the time
because other arcs read the number. Build the reader first.

### A4c · The field's meters are READ, ours are WRITTEN — and the gate cannot see the difference

The same seam from the outside. Measured on each side's own instrument (the first three rows
are failing games, numbers only; Shady Deals counted on its passage source):

| | conditions reading it | sites writing it |
|---|---|---|
| `zaras-school-life` `$PlayerCorruption` | **2,117** | 4 |
| `new-life-project` `$corrupt` | **247** | 2 |
| `new-life-project` `$inhib` (inverted — LOW opens things) | **105** | 2 |
| `shady-deals` `$p_depravity` | **244** | 2 |
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
> - **hers** — `course-of-temptation`, the roommate's partner: the overheard night is gated on her
>   own skills alone, and one way out is hers — *"If you manage to ignore everything, you can stop
>   all of this."*
> - **theirs** — `in-her-own-hands`, Shaun: what opens the kitchen flirt is **his** attraction
>   reaching 10, not anything of hers.
> - **a contest** — `course-of-temptation` (rank 5): *"pursuing either path will make the other
>   more difficult as it's a question of control."*

**Declare which one an arc is before writing its first step**, because it decides who the
refusals belong to. A3's counted refusal is hers in one direction and *his* in another —
`night_desk` already ships refusals that are his, and until now nothing in this skill said that
was a legitimate shape rather than a slip.

⚠️ **One template, stamped per person, is a normal way to build a cast.** In Her Own Hands stamps
Bobby and Shaun from one template (chat, flirt, four talks, each with branches). They differ at the
third talk: Bobby refuses and Shaun sets a limit. **The saving is real and so is the risk**: two
people built from one shape read as one character twice unless their acts, refusals and aftermaths
differ. See `the-surfaces.md` R8 — a person owns a
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
> The same game's town walk moves the odds without changing the event: in a skirt that can flip,
> and with the nerve for it, the breeze at the crossing flashes her half the time
> (`State.random() lte 0.5`); in anything else, never. In Her Own Hands does the rung half: the
> club night will not start until she is in the dress — *"Aren't you going to get ready?"*
>
> One game (`zaras-school-life`, numbers only) moves the floor of the roll instead: dressed
> ordinarily, something happens **36%** of the time; dressed provocatively, **71%**. Same scenes.
> Twice as much world.

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

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** `in-her-own-hands`, TV with Shaun in the living room: a roll of
> one to twelve, and ten of the twelve are the quiet *"Come watch with me."* — an hour on the
> sofa that pays friendship +2 and attraction +1. `course-of-temptation`'s town walk does it
> without anyone there: *"You pause and bend down to pet the dog. It wags its tail."*
> (Composure +25, Relaxation +25).
>
> One game (`zaras-school-life`, numbers only) measures it: **64%** of ordinary visits to one
> place come up quiet, drawn from five written versions, each paying 30 minutes and +15 energy.

**Ours** (`gates.py` lint · dispatch depth, 2026-09-01): the deepest dispatching activity in
the repo turns into **5** different things (`off_season`, `work_arcade_morning`); most turn into
1–3; and in `night_desk` and `the_route` **every** dispatching activity has exactly one
outcome, so the roll decides only whether the branch fires, never which branch it is. The
field's own reference figure in that lint is DoL's Bath at 12 (numbers only).

A quiet outcome is what makes the loud one worth waiting for. A place where something always
happens has no tension in the click.

---

## A8 · A pending arc beat pre-empts the dice

**The shape:** before rolling for a random incident, check whether an arc is waiting for its
next step. If it is, and its conditions hold, it fires. Arc content does not queue behind chance.

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** `in-her-own-hands`, the kitchen: it rolls one of twenty-five
> ordinary scenes, but a `SPECIAL EVENTS` chain above the roll checks Shaun's next arc beats first
> — the place, the hour (before 3 a.m.) and the flags — and only if none holds does it fall
> through to the standard scenes.

**This is available here, and precisely.** Entry-time auto-fire redirects the passage before the
location screen renders (`getStoryCanvasRedirect`, `v2.py:4921`), and among the candidates
`selectAutoFireCanvasForLocation` (`v2.py:4622`) takes the **highest `priority`**
(`v2.py:4633-4634`) — already how `off_season`'s `canvas_meet_tam` beats `canvas_tam_saw_you`. So
an arc beat is a one-shot at the location, priced above the other one-shots that could fire there.

⚠️ **It is the auto-fire queue it wins, not the dice.** That selector skips
`triggerMode == "random"` and `substitutionOnly` canvases outright (`v2.py:4630-4631`); random
ambients and substitutions are a separate selector on the location screen. The redirect happening
first is what gives the same effect as that pre-empt — the player never reaches the roll — but
the two are different mechanisms and the caveats do not carry across.

---

## A9 · The incidents at one place are different setups, not different acts — and they span the whole meter range

**The shape:** one place carries several one-time or occasional incidents. What differs between
them is **not which act is on offer**. It is the setup — who holds power, who moves first, and
what the pretext is. And their gates spread wide enough that the same place still has something
to give at the top of the game.

**The menu to choose from** — every one of these is attested in the games below, and the
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

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** `course-of-temptation` runs **151** `EventCampusWalk*`
> passages on one walk between buildings, and they are setups, not acts: a stranger demands a
> toll (`TollDemanded`, with pay, refuse, flash and escape branches) · she is caught showing
> (`CatchExhib`) · she spots two people having sex (`SpotSex`) · a friend-with-benefits wants a
> quickie (`FBQuickie`) · a partner who owns her inspects her (`DomInspect`) · someone breaks up
> with her (`Breakup`).
>
> Their gates spread from *"Give a flirty look"* at Disinhibition 1 to a flash at Exhibitionism 5:
> the same walk serves a first-day player and an end-game player with completely different
> content.

⚠️ **A cheap in-fiction cause can buy an early rung:** a plot object that arouses her before she
has decided anything lets a scene sit low on the meter. That is `register.md`'s reason axis — *she decided* against *her body decided* —
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

### A11b · And this is where the field spends its words — 2.5× more than on finishing

Counted 2026-09-03 in the same game, by passage-name suffix:

```
she did NOT go through with it   183   (113 Abort + 65 Refuse + 5 Chicken)
she did                           74   (Post)
```

**Course of Temptation writes two and a half times more prose about stopping, refusing and backing
out than about the act completing.** Whatever the intuition says about where authoring effort goes
in this genre, that is the measurement.

⚠️ **Ours is zero on the numerator** — 23 of 23 `finish`/`climax`/`cum`/`end` nodes ship an empty
`exit_block` (A10), and every `Stop.` outside `commuter` routes at a reset node and prints nothing.
So the ratio is not "we are a bit light here." There is no half of it built at all.

This is also the cheapest content in the file. An abort beat's median is **23 words**; A10's
aftermath median is 32. The unit of work is a sentence and a half.

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

## A13 · Their wanting is shown before it is acted on

**The shape:** before he acts, the player has already seen that he wants her — a small line or
look on his hub, tied to his number, repeated on every visit. Then 3–5 small steps on separate
days, each ending on a promise. And when she teases him, **it comes back in his mouth** later.

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** Three loved arcs read in order (Great Games Study, round 6):
>
> - **the leak** — the best friend in `course-of-temptation`: *"I kinda... try not to stare."*
>   [EventBFFDormSexChatBreasts]. Shaun in `in-her-own-hands` sits a little closer each visit
>   [ShaunBRFlirt1].
> - **the tease that returns** — the roommate's partner, one step later: *"I know you were watching
>   us."* [EventShowerRMPBarge2].

**The failure it names:** a tease that only fills a hidden meter, which later fires as his move on
a dice roll with no line linking it to anything she did. Players call that "random" and "out of
nowhere". Nobody in the three arcs complained that a man was too eager; they complained when his
move came from nowhere.

A pressure type moves first and names the act; a nice type waits, so she moves. Both show the want
first.

## A14 · A relationship is a chain of steps

**The shape:** every step pays one before it and opens one after it, and the text says so. The
loved arcs run 9–14 steps over weeks of play, and all three remember:

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** *"All the flirting, the furtive glances, stolen kisses, and
> sucked dick had led to this."* — `in-her-own-hands` [ShaunKitchenLateSexStart_Club].

Four rules follow:

- **A step with nothing before it is step 1, and says so** — and shows his want first (A13).
- **The next step is findable.** The guidance card names it. Being lost is the top complaint about
  the field's best relationships: 79 of 162 player comments on the three arcs are "how do I / I'm
  stuck", and 0 are about his character.
- **A "no" parks the step; it never locks the relationship for good.** The two permanent lockouts
  in the three arcs — one push-away in `course-of-temptation`, one refused invitation in
  `in-her-own-hands` that nothing clears — are the worst-remembered moments.
- **A pitch is a step on a named relationship** (`the-release.md`, "The next step").

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
  condition predicates (`engine.md` §17; `worn_exposure` is the only one that reads an empty
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
   gated on a flag the previous one sets, printed beside the field's figures (`course-of-temptation` 9, 10 and 12,
   `in-her-own-hands` 14). A number, never a bar — four arcs in two games, and no threshold is
   defensible from them.
3. **`an act ends on something`** — every `finish`-class node whose `exit_block` carries no
   choices. **23 of 23 today**, so it is a list of the whole repo and therefore useless as a
   verdict; it becomes worth building the moment one game writes an aftermath.
4. **`a step with nothing before it`** — one-time canvases on a person whose trigger reads no flag
   that person's earlier steps set (A14). A list, never a score; not built yet.

⚠️ **A11 is the first rule here with a precedent game, and that changes the build order.**
`commuter` already writes a stop beat on all seven of its loops. Every other rule in this file
has zero examples in the repo, so **A11's check is the first that can honestly ship** — it would
read "1 of 11 games" rather than "0 of 11", which is a distribution rather than an indictment.
Build order is therefore A11's lint first, then whichever of the three above a release earns.

⚠️ **This file will be skipped.** That is not pessimism, it is this project's measured history:
the register pivot defect was authored three increments running, each time by someone who had
just re-read the rule against it, and only the per-beat scorer ever caught it. Until the lints
exist, an arc is authored on discipline alone, and the honest place to record that is
`the-release.md`'s log step — name in `v2_state.json` which of A1–A14 the release built and
which it skipped, with the reason.
