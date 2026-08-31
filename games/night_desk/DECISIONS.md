# [READY] Night Desk — the fifteen decisions

<pre>
Status: [READY]         Format: FORMAT.md        Written: 2026-08-31
Block A signed off by LO in chat, 2026-08-31. B and C remain changeable.
</pre>

Ordered by **what it costs if it's wrong**, not by topic. Argue with block A properly. Skim block C.

---

## In short — 30 seconds

- She works the night desk at a twelve-room motel on a highway. **10pm to 6am, alone.**
- **She cannot leave.** The world drives in. That is the whole game.
- **Two men are there every night.** Del owns the place and sleeps in the back office. Marek has
  lived in room 6 for eleven weeks.
- **Two numbers on her.** `exhibitionism` — what she lets be seen. `corruption` — what she will do.
  Both 0 to 100. **Two on each man** — `relation`, whether he is willing, and `corruption`, what he
  asks for. The gap between hers and his is where the refusals live.
- **The new thing:** every line she speaks exists three ways — meek, bratty, neutral. Her story is
  fixed. How she carries herself is the player's.
- **Each man has a mood that flips.** Del depends on whether the motel was full that week. Marek
  depends on whether he thinks he is leaving. Every scene gets written both ways.
- **She picks her hours.** The motel runs all day. Night is quiet and private; daylight pays more
  and has people who can see her — so **the hour is the difficulty.**
- **Money.** She is paid per room filled. She owes $80 a week for her own room. A quiet week does
  not cover it, and the gap becomes debt to Del.
- **Friday is the hinge** — her pay, his mood and his decision all land on the same day.
- **The bathroom is shared and not split by sex** — the cheap rooms and staff use it, Marek
  included. So washing is public, and **the need is what pushes her into the risky room.**
- **Corruption unlocks; exhibitionism spends.** Corruption opens an option, doing it in public is
  what climbs. The camera monitor is the free on-ramp.
- **Seven rooms and nothing else exists.** Everything hangs off the desk, so every need pulls
  her away from where the money is.

**Five decisions can never be changed once we ship. Nine can.**

**Both earlier open questions are now closed** — she is written (#2, LO's call), and the debt
becomes visible in the night audit rather than as an invented bill (#13).

**One thing to check first:** whether another game is already called *Night Desk*.

*Longer version in plain words: [`DECISIONS_LONG.md`](DECISIONS_LONG.md). Everything below is the detail, with the
evidence.*

---

# A · LOCKED FOREVER

Change any of these after the first release and every save in the wild breaks. The engine's
migration seam repairs *additions* and nothing else.

### 1 · Narration person — **second**

*"You slide the register across."*

**Why.** The field splits *the body* 19 / *the camera* 10, and second person is the body. All eight
of our games are the body, so this is the one place our default matches the field's majority rather
than fighting it. It is also the person the three-way speech variants read best in — *"you say"*
carries a manner; *"she says"* reports one.

**If wrong:** every line of prose in the game gets rewritten.

### 2 · Who the player is — **female, and written**

**She is a written character, not a blank one.** The setup states whatever the game needs stated.
What the player controls is **how she carries herself**, not who she is.

| | |
|---|---|
| name | the player's, chosen at the start |
| age | **19** |
| why she is broke | she left where she was living in a hurry, with what fitted in a car — **and then sold the car** |
| why she cannot leave | no family to fall back on, and no vehicle. The bus is the only way out and it costs money she does not have |
| how long she has been here | **three weeks** — long enough to know the building, new enough that corruption at 0 is honest |
| the night the game opens | **her first shift on the desk alone.** Three weeks of days and company, and tonight nobody else is here. It is what makes a handover scene natural and why she is only now learning half the job |
| why she lives in room 12 | she answered an ad. The room was part of the pay, and the eighty a week comes back out of it |
| what she wants | **out.** $400 and a seat on a bus. It is always one good week further away |

**Selling the car is the load-bearing fact.** It is why she is broke, why she cannot leave, and why
$400 is the number. Everything the premise needs, in one sentence of setup.

**Why female.** Not a coin toss and not the field's shape — the field's top ranks are male-PC games
where women are the content. It is the *players'* verdict: across 22,622 comments, **49 asking for a
female lead (364 likes) against 11 opposed (124 likes)**, and the opposed get piled on. One argues
it mechanically at 14 likes — *"as a guy I like to play female mc since we can get to the spicy part
quicker."* Real-performer media makes the same case.

**Why written, against the field's 19-blank-to-10-written split.** Two reasons, and the second is
the real one:

1. **The media is real-performer.** One specific woman's face and body are on screen. A blank slate
   with a fixed face is a contradiction.
2. **The freedom is bought somewhere better.** `meek` / `bratty` / `neutral` hands the player her
   manner on every line she speaks — the field's single largest love-reason, delivered through play
   rather than at a character creator. **The player controls how she carries herself, not who she
   is.**

⚠️ **The "80% of engagement is blank-slate" figure is a correlation across thirty games with a great
deal else going on. It does not show that blank *causes* engagement, and I leaned on it harder than
it can carry.**

⚠️ **LO's call, in chat, 2026-08-31**, against my own recommendation the same day: *"i dont like
keeping her blank, we should tell whatever is required to set the game up."* The earlier "written but
thin" compromise is **withdrawn**. This is no longer an open question.

**If wrong:** the whole cast's dialogue is written to the wrong person.

### 3 · The title — **Night Desk**

**⚠️ Not verified.** The distribution research found two name collisions on the portals for previous
games. This one has not been checked and must be before first release — the title is a save join
key, so it cannot be changed afterwards.

### 4 · Every id and slug

<pre>
locations   <a href="sheets/places/the_desk.md">the_desk</a> · <a href="sheets/places/the_corridor.md">the_corridor</a> · <a href="sheets/places/the_office.md">the_office</a> · <a href="sheets/places/room_6.md">room_6</a> · <a href="sheets/places/the_lot.md">the_lot</a> ·
            <a href="sheets/places/the_kitchen.md">the_kitchen</a> · <a href="sheets/places/the_bathroom.md">the_bathroom</a>
people      del · marek
hers        exhibitionism · corruption
his (each)  relation · corruption
needs       energy · hunger · hygiene
other       money
</pre>

**Why these.** Bare nouns, no articles in the slug, readable at 3am in a stack trace. [`room_6`](sheets/places/room_6.md) is
the room, not the man — if Marek leaves, the room stays.

**If wrong:** renaming one strands every save that was standing in it, and no gate can see it.

### 5 · The scales — **every meter 0 → 100**

<pre>
hers   exhibitionism  0 → 100        nine rungs:  2 · 6 · 12 · 20 · 30 · 45 · 60 · 78 · 95
       corruption     0 → 100        same shape
his    relation       0 → 100
       corruption     0 → 100
</pre>

**Why 100.** It is the field's modal ceiling — six of eighteen measured stat scales land there,
against 2, 3, 9, 10, 10, 50, 180, 200, 300, 500, 999 and 1000 elsewhere. It is also the engine's own
range: `clamp` is a hard **0–100 and defaults to true** (`v2.py:5928-5930`), and the engine's note
says outright that meters *"want the clamp and should keep it."* A scale above 100 fights the
runtime; a scale below it wastes the room.

**Why everything on one scale.** Mixing 0–10 and 0–100 means *"is he at 8?"* needs you to remember
which meter it is. One scale, one mental model.

**Why the rungs are separate from the scale.** ⚠️ This section said `0 → 24` until 2026-08-31 and
that was an error — it tried to encode "nine rungs" into the ceiling. They are different things: the
**scale** is what the number counts to, the **rungs** are where the gates sit on it. The field runs
**8–17 rungs starting low** on scales that are usually 100. `degrees-of-lewdity` runs exhibitionism
to 500 and its **median gate is 40** — most content sits low on a big scale.

**Why generous now.** Because we will want more rungs later, and **rescaling a meter is one of the
two changes that strands every save in the wild and that no gate we own can see** — the key never
moves, so nothing flags it. At 100 there is room for thirty more rungs without touching the scale.

**If wrong:** rescaling is invisible to every gate we have and silently moves every gate site in the
game.

---

# B · EXPENSIVE

Changing these rewrites content that already exists.

### 6 · The cast — **two standing, and the traffic**

Two named people, both deep. Everyone else who comes through the door is generated and unnamed.

**Del** — 58. Owns the Wayside, sleeps in the back office, watches four cameras cycle at eight
seconds each. Certain about the building and about nothing else.

> **Why she wants him:** he holds her shortfall and has never once acted like it buys him anything —
> which is exactly why she keeps testing whether it does.
>
> **His axis — the week was full, or the week was empty.** Driven by occupancy (#11). Full, and he
> is expansive, generous, buys the coffee himself. Empty, and he is at the monitor at 4am, short
> with her, counting. **Every scene that can fire in both states is written twice.**

**Marek** — thirties. Room 6, eleven weeks, pays cash on Fridays. He has unpacked, and that is the
thing about him.

> **Why she wants him:** he has no power over her whatsoever, which is why he is the only one who
> says it out loud.
>
> **His axis — going, or staying.** Every Friday he either extends or announces he is leaving.
> Going, he is honest and reckless. Staying, he is careful and evasive. **Both versions, every
> scene.**

**The traffic** — guests arrive, argue about the rate, take a key, leave. Generated, unnamed,
untracked, no meters. They are the world moving, and they are why the lot is worth walking.

**Why only two named.** The field's own division is a few deep and many light — the reference game
gives its rich two-meter model to three housemates and runs its other fourteen characters light.
And a release adds a body to a hub that already exists, so a third named person is what 0.2 is for.

**Why each one needs a declared axis.** ⚠️ This is the reference game's hard rule for its writers
and we have never had it. Every one of its main characters carries a named state the writer must
cover — Robin cheerful or traumatised, Kylar shy or obsessive, Sydney pure or corrupt: *"Scenes that
can trigger at any level of trauma need variants to cover both."* Without it a repeatable surface
says the same thing on the fiftieth visit, which is the measured defect in **every** one of our
games — `block_pool` runs 46 times in one v1 game and **zero times in every v2 game.**

**Friday is the hinge.** Her pay is reckoned Friday, Del's mood is set by the week that just ended,
and Marek decides on a Friday whether he is leaving. One day a week when all three move at once.

**If wrong:** every scene in the game is written for the wrong people.

### 7 · Who climbs — **four meters, four jobs, and the gap between them is content**

| meter | job |
|---|---|
| **her `exhibitionism`** | what she will let be **seen** — no bra, no panties, flashing, being caught on purpose |
| **her `corruption`** | what she will **do**, and how she thinks about it |
| **his `relation`** | whether he is **willing** |
| **his `corruption`** | what he will **ask for** |

**The split that makes it worth having.** Her corruption is what she will do; his is what he will
ask. A scene needs both — he has to propose it and she has to agree — so content falls out of the
**gap** between them:

- **his high, hers low** → he asks and she refuses. A real refusal, written at full length. The
  field puts one on a click in fifty and **79% of them lead somewhere the yes does not**; we have
  never written one.
- **hers high, his low** → she is ready and he will not. Careful, protective, or frightened of what
  he would become.
- **his `relation` low, `corruption` high** → he will ask for anything and does not care about her.
  A different man entirely, from the same two numbers.

**Why two per person, when nine of thirteen field games give everyone exactly one.** The rule that
covers it says do it here: *"reserve the rich two-meter model for the one or two arcs that carry the
game."* We have exactly two characters and both carry it. Field practice backs the word too —
corruption is a **per-NPC** meter in six of 28 games (`$adrianacorruption`, `$alettacorruption`).

⚠️ **The risk, and the rule that contains it.** Each character now carries two numbers plus a mood
(#6), which is **eight versions of every scene** if everything varies on everything. Our own doctrine:
*"gold-plating every character dilutes the core and triples the authoring."*

**So: every scene declares the ONE axis it varies on.** Usually one, occasionally two, never four. A
scene gated at corruption 60 needs no low-corruption variant — it cannot fire there. That is the
reference game's rule read properly: variants are owed only where a scene *can* fire in both states.

⚠️ **The two ladders are not independent, and this is the spine of the game.**

<pre>
corruption  ──unlocks──►  an exhibitionism option
                              │
                              ▼
                        she does it  ──raises──►  corruption
                              │
                              ▼
                      raises exhibitionism
</pre>

**Corruption is the gate. Exhibitionism is what climbs by doing.** Corruption never raises
exhibitionism directly; it opens a door and nothing more.

**And each has a job the other cannot do:**

- **corruption** says *she would consider this*
- **exhibitionism** says *she will do it where someone can see*

Going without a bra unlocks at corruption 12. At low exhibitionism she only does it on the 4am shift
with the lot empty; at high exhibitionism she does it at 2pm with a queue at the desk. **Same act —
corruption buys it, exhibitionism spends it in public**, and the payoff is in the spending. Without
that split exhibitionism is a counter nothing reads, which gate `a meter is read` fails a game for.

**The corruption ladder.** Old sources never disappear — the list gets **longer**, never different.

| corruption | what is available |
|---|---|
| **0–20** · passive, no risk, nobody knows | **the camera monitor**, and sometimes there is something on it · a curtain not closed on the property walk · what is in the sheets in the laundry |
| **20–45** · she stays instead of moving on | shower while someone else is in there · watch instead of walking past · turn a room with the guest's things still out |
| **45–78** · she is in it | shower with men and not cover up · let a check-in look · be the one on the monitor |
| **78+** · she arranges it | make sure someone is watching |

⚠️ **The monitor is the on-ramp, and it must be day-capped.** It is free, safe, on screen from the
first night and needs no nerve at all — which is exactly why a player would grind it. The mechanism
is `[engine.daily_tick]` plus a `_today` flag on the choice (`engine.md` §28). **Three or four
sources at every tier, never one**, or the early game is *"watch the monitor twenty times"* — the
genre's second-largest complaint after lostness.

**The player's manner is the fifth axis and it is not a meter** — `meek` / `bratty` / `neutral`, set
by which speech option she takes, read every time she speaks. It gates nothing. It colours
everything.

**If wrong:** every gate site in the game moves.

### 8 · The anchor — **the front desk**

It carries the largest single block of prose in the game, deliberately.

**Why.** DoL's seed put **30% of all location prose in one anchor** (`school`), with a long tail
down to a 302-word bus station. A world with thin satellites is fine; a world with no centre is not.
Eight of nine of our v2 games rooted on a worksite or a household and then spread the prose evenly,
which is how you get five rooms nobody has a reason to stand in.

**If wrong:** the budget for every room is wrong.

### 9 · The map — **seven rooms, closed, one hub**

<pre>
                          <a href="sheets/places/the_desk.md">the_desk</a>  ◄── anchor, the hub
             ┌────────┬───────┼────────┬──────────┐
      <a href="sheets/places/the_corridor.md">the_corridor</a> <a href="sheets/places/the_office.md">the_office</a> <a href="sheets/places/the_lot.md">the_lot</a> <a href="sheets/places/the_kitchen.md">the_kitchen</a> <a href="sheets/places/the_bathroom.md">the_bathroom</a>
             │
          <a href="sheets/places/room_6.md">room_6</a>
</pre>

**Everything hangs off the desk, and that is mechanical, not tidy.** Every need pulls her away from
the desk, and being away from the desk is how she misses an arrival — which is how she loses money
(#11). The map shape is what gives the needs teeth.

**Why closed, and why the outside is a spoke.** Our own map doctrine says the exterior should be the
ground, never a room off the kitchen. **This deliberately breaks that**, and the premise is the
reason: the lot is the *edge of the world*, not a route out of it. There is no town, no bus, no
elsewhere. She is here until 06:00.

That is the whole design. If the map lets her leave, the game has no pressure at all.

**If wrong:** every location's connections and every travel cost change.

### 10 · The charge — **confinement, then transformation**

- [x] **Confinement (primary)** — eight hours, two men, one building, and she cannot go anywhere.
      Everything that happens, happens because there is nowhere to walk to.
- [x] **Transformation (secondary)** — she starts as the girl who takes the last bus and ends as the
      reason both of them arrange their nights around a shift they do not have to be awake for.
- [ ] **Taboo — deliberately not the spine.** ⚠️ This is a real trade. Taboo is the genre's engine
      and nine of our games use it. But players name the tired package precisely: *"It is literally
      the same game as all the other games. Young guy step family and school."* No family here, and
      the cost is that the charge has to come from the situation instead of the relationship.

**If wrong:** every scene is aimed at the wrong feeling.

### 11 · The money — **pay rides on occupancy, and Del holds the shortfall**

| | |
|---|---|
| she earns | **$6 per occupied room per night** — twelve rooms, so $0–72 a night |
| typical night | four rooms · **$24** |
| she owes | **$80 a week**, for room 12, deducted from pay before she sees it |
| a slow week | does not cover it, and **the shortfall rides as debt to Del** |
| the sink | a bus ticket out. $400. It is always further away than one good week |

**Why not rent.** Nine of nine v2 games ran a rent-or-debt hook charged at a window. Here the number
is the same shape but the *mechanism* is the premise: **filling rooms is how she gets paid**, so
cars arriving in the lot is both the content engine and the economy. And the person holding her
shortfall is one of the two people she is climbing toward, which is what makes his ladder mean
something.

**⚠️ The risk, named:** this may fail our own `the obligation is charged` gate, because nothing
charges her at a window — it is netted out. If it does, the fix is a visible weekly line on the
desk screen, not a redesign. **Your call whether to pre-empt that or let the gate tell us.**

**If wrong:** every price and every earn rate in the game moves.

---

### 12 · The clock — **she picks her hours, and the hour is the difficulty**

The motel runs 24 hours. She lives in room 12. **Nothing makes her stop working**, and nothing makes
her start.

| | |
|---|---|
| a shift | any block she chooses to stand at the desk |
| night | 22:00–06:00 — empty highway, little traffic, **little money**, and both men to herself |
| day | more arrivals, more money, **and people who can see her** |
| the cost | hours worked are hours not slept, and `energy` does not forgive |

**Why this and not a day that gets skipped.** ⚠️ A day-as-menu was proposed on 2026-08-31 and
**withdrawn the same day**. Three reasons this is better:

1. **The hour becomes the difficulty dial for `exhibitionism`.** At 4am the lot is empty and the
   highway is dead — working with nothing on under the shirt costs her nothing. At 2pm there is
   traffic and a checkout queue. **The same act is free at night and real in daylight**, which is a
   difficulty curve built out of something already in the game.
2. **It makes the money a choice.** More hours is a closer ticket and a worse next shift.
3. **It sharpens the confinement rather than softening it.** She lives there and may work as much as
   she likes. Nobody makes her stop. That is a worse trap than a fixed shift.

**The cost, named:** the world now needs real schedules across 24 hours, not eight. Del has to sleep
sometime. That is more schedule work — and it is also what stops the place feeling like a set.

**Scope for 0.0.1:** the night shift **plus one day shift**, so the mechanic exists and is proven
without writing twenty-four hours of content.

**If wrong:** the clock, the economy and the exhibitionism curve all move together.

### 13 · What the job actually is — **the duties are the engines**

| duty | what it actually is |
|---|---|
| **take a check-in** | the money — $6 a room — and a stranger at the counter looking at her |
| **run the audit** · 02:00–04:00, once a night | the drawer, the day's totals, Del's money and hers |
| **walk the property** | how she gets out of the desk — past twelve doors, past room 6, into the lot |
| **the laundry** | other people's sheets, a warm room, nobody around |
| **turn a room** | a key, and a guest room with the guest gone |
| **the phone** | ambient, and a booking is a filled room |

**Hand out keys, walk past doors, count the money.** Each is one of the game's engines:

- **keys** are access
- **walking past doors** is how she sees things — **the corruption engine is a job duty**, so she
  never has to go looking. She is *supposed* to walk past.
- **counting the money** is the debt, and Del

And the exhibitionism engine is that **she stands behind glass and people come to her.** She never
has to seek an audience; the job delivers one every hour or two.

⚠️ **The audit is where the deduction becomes visible** — the open question on #11. She reconciles
the drawer at 3am and the $80 line sits in the day's totals in Del's handwriting. No invented bill
and no extra screen: a real duty of the real job, exactly where the fiction already puts it.

**Dropped, because they pass time and do nothing:** breakfast setup, cleaning the lobby, wake-up
calls.

**If wrong:** the choice list of every room is wrong.

# C · CHEAP — change any time

### 14 · Needs — **three: `energy`, `hunger`, `hygiene`**

A declared need that gates nothing is a chore, so each one is given a door it shuts, and each door
is something the game already cares about.

| need | falls | fills | what it shuts |
|---|---|---|---|
| `energy` | across the shift, and overnight | room 12 · the office cot · coffee | under the band she cannot take anything costing 30 minutes or more, so the night ends early and she misses whoever comes in at 3am |
| `hunger` | across the shift | **the kitchen** — something on the table (fast, small) or the fridge (slower, real) | under the band she has to leave the desk to eat, and **while she is in the kitchen she is not taking check-ins** — a missed arrival is an unfilled room, and an unfilled room is $6 she does not get |
| `hygiene` | daily, faster across a shift | **the shared bathroom** | under the band **she will not let anyone look at her.** Every `exhibitionism` rung is closed until she has washed |

⚠️ **`hygiene` is the best need in the game, because the bathroom is shared.** She *has* to wash,
the shower is communal, and who is in there depends on the hour. **A need that forces her into the
risky room is worth far more than one that empties a bar** — it is the difference between a chore
and a mechanic, and it is the strongest argument for declaring needs at all.

The whole chain: **hygiene falls → she must wash → the shower is shared → someone is in there →
corruption rises → corruption unlocks an exhibitionism option → exhibitionism decides whether she
does it where she is seen → being seen raises corruption.** Every meter feeds another, and a *need*
is what starts the engine.

**`hygiene` is the one that matters most here, and it is not a chore.** This whole game is about
being looked at. A need that shuts *being looked at* is the need aimed directly at the game's own
meter — not a bar that empties beside it.

**`hunger` is priced in money, not in a refusal.** It does not say no. It takes her off the desk,
and the desk is where the money is. That is the field's own division — a condition should *change*
something far more often than it *removes* something.

**The two new rooms.**

- **the_kitchen** — staff kitchen behind the desk. Something on the table, and a fridge. Del uses it
  too, which makes it a place they collide at 3am rather than a vending machine.
- **the_bathroom** — ⚠️ **shared, and not split by sex.** The Wayside is old: rooms 1–6 are the
  cheap half and share the bathroom in the back hall behind the desk, and so does staff. **Marek is in room
  6**, so he and she wash in the same room from day one.
  ⚠️ **It is a walk-in surface by construction**: our own rule is that a room where she is alone
  with someone scheduled carries a walk-in, and a man who holds keys to every door in the building
  is the strongest version of that in the game.

**No prep need.** Three that shut real doors beats four where one decorates the sidebar.

### 15 · The crude ceilings — per person, per tier

A **ceiling, never a floor.** Writing under it is a defect.

| | tier 1 | tier 2 | tier 3 |
|---|---|---|---|
| **Del** | tits, ass, hard | cock, cunt, wet, fuck | cock, cunt, cum, throat, hole — and what her body does back |
| **Marek** | tits, ass, hard, cock | cunt, wet, fuck, cum | the coarsest register in the game, nothing withheld — he has nothing to protect and no reason to be careful |

**Where the crude register lives:** the repeatable rungs. The office at 1am, the corridor, room 6.
**Not** a capstone. If the crudest writing in this game ends up somewhere the player sees once, the
game is cold and the release does not ship.

### 16 · The character screen — **declared, with exactly one field** `[new] 2026-08-31`

`[player] customizable = true` plus a single `[[player.customization_fields]]` entry:
`id = "name"`, `type = "text"`. The generator maps `id = "name"` to `$player.name`
(`v2.py:9522`); any other id would write `$player.<id>` and nothing reads those here.

**Why declare it at all**, when the alternative is asking her name in a prose beat:

- **The engine already has the form.** Seven of our fifteen built games ship this screen.
- **A free-text question inside a prose beat is a second screen doing the first one's job.**
- It moves the game's only piece of chargen out of the funnel, so the boot can be two clean screens.

**Why exactly one field.** Decision 2 locked her as *female and written*. A build/hair/body-type
select would let the player assemble somebody the prose then contradicts. **One field is the whole
of it, and this is the ceiling, not a starting point.**

⚠️ **The cost, and it is real.** Declaring the screen **repoints the age gate at it**
(`v2.py:1065`, `v2.py:9251`), and its text is hard-coded in the generator:

> Customize Characters · *Personalize the characters in your story.* · Your Character · Continue to Game

That product-voice string becomes the second thing a player of this game reads. The only authored
text on the screen is `player_description` (`v2.py:9509`), which we set to:

> Nineteen, three weeks at the Wayside, and tonight you are on the desk by yourself.

**The trade, stated plainly:** one generic sentence bought in exchange for the name question leaving
the prose. **Reversible** — dropping the declaration sends the age gate straight back to the boot,
and the name goes back to being a beat.

---

---

## What I want from you

~~The two I flagged~~ — **both are now closed.** #2 was decided in chat; #11 is answered by #13's audit. Formerly **#2** and **#11** (netted debt vs a charged window).
Those are the two where I would not argue hard if you went the other way.

Everything in block A needs a yes, because after the first release it is not a decision any more.
