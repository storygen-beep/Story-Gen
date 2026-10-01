# The Arc — what happens between the introduction and the loop

## Why this file exists

The field builds a **numbered arc of one-time steps that ends by turning into a repeatable sex
surface**, and the first third of the arc has no sex in it at all.

This was read, not counted. Four arcs end to end in two passing female-lead games —
`course-of-temptation` (the harasser, the best friend, the roommate's partner) and
`in-her-own-hands` (Shaun) — with Cupid's Way and Shady Deals supplying single mechanisms. Where a
rule has no passing example, the evidence is a failing game's structure, named and labelled
"numbers only": its scenes are never used.

⚠️ **Two things this file is NOT, because both were proposed in the session that produced it
and both were wrong.**

- **It is not about how much sex a game has.** Degrees of Lewdity (numbers only), the game every
  founding commitment was measured on, has the **lowest** explicit share in the 25-game field — 4.8% of
  passages. The field's own spread is 5%–62%. There is no house ratio,
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
This is not decoration: an example is copied, words and numbers included. **Every word in an
example is being taught too.** *(LO decided.)* Take the mechanism. Leave the furniture.

---

## A1 · An arc is a numbered ladder of one-time steps that ends by converting into a repeatable

**The shape:** N one-time steps, each gated on the flag the step before it set · the last step
turns the act into something she can simply do · doing *that* repeatedly opens the next act.

The repeatable surface is the **reward for finishing the arc**, not the starting position.
After the sex step, the arc's phone thread becomes the repeatable invite (`the-phone.md` P9).

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

**Length: one or two long chains, 8–15 steps, for the game's central people; shorter chains for
the rest.** The field's figure is the **longest** chain per game: a median of about 15, and 12 of
26 corpus games have one of 15+ steps (numbers only; the corpus includes failing games). Course of
Temptation runs 10, 9 and 12 steps for three people; In Her Own Hands runs 14 for Shaun. **This is a
shape, not a quota** — no gate reads it. Run `lint · the arc ladder` to see each person's chain.

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
That is `the-clock.md` and `the-map.md` doing arc work. An arc opening needs no new systems. Night
one's explicit beat comes from outside the arc: a stranger or a one-off (A15).

---

## A3 · Saying no — parked by default, final only when the button says so

**One rule** (LO decided, D6; R2 K7):

- **An ordinary no is parked.** The step comes back after the author's wait (`retry_after_days` on the
  no, with the step's trigger set to `consume_on = "exit"`, `engine.md` §49), and his next line may remember it:
  a pushy man says so, a nice man drops it.
- **A final no exists only on a button that says so** — "(ends his path)" — and sets `final = true`.
  It closes his story, never the person: he stays in the world.
- **Where a game gives him feelings** (`the-meters.md` W1), a no may cost Warmth, never Want (R5).

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** In-scene lines from the passing games:
>
> - the nice man drops it — In Her Own Hands [ShaunBRTalk4D]: *"I get it," Shaun said quickly. "It's
>   totally cool."*
> - the pushy man asks again — Cupid's Way [damien13]: *"Haha, alright."*, and the same ask is back
>   on her City screen as soon as she leaves;
> - he remembers — In Her Own Hands [JamesCoffeeShop2E]: *"my texts and calls seemed to vanish into
>   thin air"*; [DevDadDiner1]: *"You haven't called. Naughty girl . . ."*;
> - the final no is labelled — the same passage: *"End the conversation and get back to work (ends
>   path)"*.

Remembering a no in his words is **thin**: 2 men in 1 game of 4 (R2 K7). None of the four passing
games routes a refusal to a new person, so a no never hands her on. **The one thing a no never does
is stay silent about which kind it is.**

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
> Two refinements have one example, in one game (`family-ties`, numbers only), on top of the +1
> unit (`the-meters.md` W1b-i): the grant is scaled by where she already is (+5 below 30, +10
> above), and the raise stops at the next threshold, so she cannot climb past a rung by repeating
> the one below it.

Two exits per page is the whole navigation of a five-page scene. Compare the act-menu figures
in `the-surfaces.md` R3b — field median 2 options, span 1. **The same narrowness, applied down
the page instead of across the menu.**

⚠️ **The locked-door text here is the `a locked door says why` gate's subject** (`engine.md`
§15, §36 · `the-surfaces.md` R5c). Course of Temptation and Cupid's Way (*"Drive with him
$corruption/20"*) print the bar and the number.

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

### A4c · The field's meters are READ far more often than they are WRITTEN — and the gate cannot see the difference

The same seam from the outside. Counted as textual occurrences in built HTML (the first three rows
are failing games, numbers only; Shady Deals counted on its passage source):

| | conditions reading it | sites writing it |
|---|---|---|
| `zaras-school-life` `$PlayerCorruption` | **2,117** | 4 |
| `new-life-project` `$corrupt` | **247** | 2 |
| `new-life-project` `$inhib` (inverted — LOW opens things) | **105** | 2 |
| `shady-deals` `$p_depravity` | **244** | 2 |

**Why the scoreboard is quiet about this.** Gate `a meter is read` asks, per meter, whether it is
read *at all* — it fails only a meter that is read zero times. It finds **dead**
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

**Two routes on one person are two arcs; inside a system, ladders follow `the-systems.md` SY8's touch rule.**

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
refusals belong to. A3's no is hers in one direction and *his* in another — a
refusal that is his is a legitimate shape, not a slip (the **theirs** line above: In Her Own Hands
[K_LateShaun1A] opens on `$xr.sh.rel.at gte 10`, his number).

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

**Remind her before the key is needed.** A garment the arc needs is named where she will see it
before its window opens. In Her Own Hands reminds her of the date dress in two rooms; its gala gown
has no reminder, so a player who is not wearing it gets a silent gala night (round 9a,
`traces/ihoh_wardrobe.md`). A key garment is one reader among many: the wardrobe is designed as
states first, then items (`engine.md` §17).

The gate `the wardrobe is read` asks only whether a declared `[[clothing]]` catalog is read
*anywhere*. The rule is stricter: every declared state and key item is read in ≥3 places (planned
gate: `every clothing state is read three times`). This says where it earns its keep: on a rung,
and on a rate. `the-meters.md` W7 and
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

The field's reference figure for dispatch depth (`gates.py` lint) is DoL's Bath at 12
(numbers only).

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
location screen renders (`getStoryCanvasRedirect`, `v2.py:5341`), and among the candidates
`selectAutoFireCanvasForLocation` (`v2.py:5039`) takes the **highest `priority`**
(`v2.py:5050-5051`). So
an arc beat is a one-shot at the location, priced above the other one-shots that could fire there.

⚠️ **It is the auto-fire queue it wins, not the dice.** That selector skips
`triggerMode == "random"` and `substitutionOnly` canvases outright (`v2.py:5047-5048`); random
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

**It is the cheapest thing in this file to build.** Thirty-two words and one choice, on a
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
| **refusing** | at the door, before anything | whether she wants this at all — parked or final, A3 |
| **stopping** | mid-scene, with it already happening | how he takes being stopped; in a paid scene it costs part of the pay (A15, thin) |
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

This is also the cheapest content in the file. An abort beat's median is **23 words**; A10's
aftermath median is 32. The unit of work is a sentence and a half.

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** `course-of-temptation` [EventWalkPartnerQuickieAbort], a
> quickie she stops once it has started. The partner gets the lines: *"Not feeling it?"* … *asks,
> looking confused. "What's wrong?"* — her answer is *"Just... maybe now isn't the time."* — and
> the beat ends on him: *"I guess I'll see you later."*

That is the rule executed correctly — **the beat is about his reaction, not her exit.**

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

Scoped to a person with a ladder; a stranger or one-off (A15) passes if the same canvas shows his want
before the act.

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
- **A "no" parks the step** (A3); only a labelled final no closes his path, never the person.
- **A pitch is a step on a named relationship, or a step in a declared thread** (`the-release.md`, "The next step").

---

## A15 · Her climb into paid sex — the lewd ladder of a money system

*(LO decided, D7; evidence R1, `~/Documents/Skill_Test_Research_20260929/R1_HER_CLIMB.md`. Gate `her climb`.)*

Paid sex is a money system (`the-systems.md` SY8), and this climb is its lewd ladder: each rung opens
an act and better pay. **The model is Shady Deals' stroll:** the price is built from her stats
(charm × 10–24, plus 0–120, plus sluttiness × 10–25), the corner picks the act, and the price is on
screen before she agrees ([Spot Work]). **The failure is Course of Temptation's gloryholes:** 38
passages, and none pays a cent (round 9b, `cards/sex_for_pay.md`; `templates/cards/sex_for_pay.md`).

- **Introduced first.** Someone raises it in a one-time scene before the activity appears — the
  activity's version of "every hub is met first" (`the-first-hour.md` F5). 4 of 5 games do (R1:76).
- **A first time before every paid repeatable:** his want → her hesitation → a price named or
  bargained → the act → her feeling after, as its own beat. Then the repeatable opens (R1:138).
- **The repeatable changes with her level:** two voices per act, reluctant and eager, split on her main
  sex trait (**thin**, R1:170), and a menu that grows as the acts open one by one (`the-surfaces.md`
  R3c).
- **The start matches the Want's bottom.** Nothing paid is reachable on a new save before its
  introduction and first time; the minimum path is introduced → at least one step → first time. No day
  count (R1:268).
- **Night one** may carry one hot moment from a stranger or a one-off — never the paid route and never
  the main man. 3 of 5 games have a day-one scene of that kind (R1:296).
- **Always a no before** (5 of 5, R1:228). "Stop him" at each stage of a paid scene costs part of the
  pay (**thin**: only one game does it fully, R1:218-228). The route ends only through a labelled final
  no (A3).

---

## The engine, verified

Every line here was read on 2026-09-01. `engine.md` remains the only file that may carry engine
facts; these are the ones this doctrine leans on, and they are repeated here only as pointers.

- **A step is recorded on a counter.** Each step is a one-shot canvas gated on the person's
  counter (`<npc>_stage eq n-1`) that sets it to `n`, and the final step opens the repeatable surface —
  the `counter` of `board.characters[].ladder` (`state.md`; `the-spine.md` SP2).
- ⚠️ **The native primitive exists and is not wired.** `setup.selectCanvasByPriority`
  (`v2.py:5400`) implements A1 exactly — canvases sharing a `name` form a group, unvisited tiers
  play in ascending `priority`, and once all are seen it returns the highest-priority one
  forever. **Nothing calls it.** In a built game's `output/index.html` the symbol appears
  three times and is invoked zero times. The live path is `renderSoloActivities`
  (`v2.py:5662`), which drops every non-repeatable canvas (`if (!c.isRepeatable) continue`) and
  does no progression at all. **Do not point an author at it.** Wiring it is an open engine
  decision, not a thing this file may assume.
- **A8 is available** — highest `priority` wins on the auto-fire path (`v2.py:5050-5051`).
- **A6 is available** — `worn_exposure`, `worn_type`, `worn_corruption` and `worn_beauty` are
  condition predicates (`engine.md` §17; `worn_exposure` is the only one that reads an empty
  slot). Two gaps: no effect removes or unequips a garment, and there is no "leave the room" hook,
  so a price to go out in a state lives in each destination's `entry_conditions`.
- **A4's grant-while-under-threshold** is an ordinary `[group]` band on the meter plus an
  `add` effect. ⚠️ Adjacent `[group]` blocks merge into one if/elseif chain and first match
  wins (`engine.md` §35) — separate the grant band from any other ladder on the same node with
  a non-`group` block, or the ladder below it goes silently unreachable.

---

## The check

**One gate ships here: `her climb` (A15, LO decided D7).** For A1–A14 two precedents hold. **P0** —
never build a check for a state nothing is in. And **"a check that fails a game for obeying the doctrine
is a bug in the check"**.

The candidates below are **lints**, not gates, and each is built only once one game has built
the thing — the order that produced `the start choice is read` (shipped after a game built
it first) rather than the order that produced P0.

1. **`a refusal is remembered`** — superseded by A3's rule and its check (gate `a no has content`).
2. **`the arc ladder`** — BUILT. Per person: the one-time steps written, how many are switched
   off, and the longest chain where each step's trigger reads what the one before sets; the
   game's longest beside the field's (median ~15). A list, never a bar.
3. **`an act ends on something`** — every `finish`-class node whose `exit_block` carries no
   choices. Until a game writes an aftermath it lists every finish node and is useless as a
   verdict; it becomes worth building the moment one game writes one.
4. **`a step with nothing before it`** — one-time canvases on a person whose trigger reads no flag
   that person's earlier steps set (A14). A list, never a score; not built yet.

⚠️ **Log which rules a release skipped.** *(LO decided.)* Until the lints
exist, an arc is authored on discipline alone, and the honest place to record that is
`the-release.md`'s log step — name in `v2_state.json` which of A1–A14 the release built and
which it skipped, with the reason.
