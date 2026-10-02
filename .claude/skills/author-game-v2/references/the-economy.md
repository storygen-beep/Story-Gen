# The Economy — the only system that can say no

Money is the one thing in a sandbox that makes the player **choose**. Everything else expands. If
money never says no, every arc gated behind it becomes optional scenery.

> **This file is measured across a field, not a single game.** 18 shipped browser sandboxes,
> ~62,000 passages, parsed 2026-08-12. Corpus, method and limits: `DOCTRINE_GAPS.md` Appendix B.
> The reference game this skill was originally derived from carries **738 money movements and 372
> money gates** — and none of that was ever measured, which is why this file exists.

---

## The four measured rules

### R1 · Money must gate content

**Field: a median 67.3 conditions read the currency per 1,000 passages.** Every sandbox in the
corpus does it. The only two games at zero are a scripted time-slot game and a very small one —
neither is a sandbox.

A currency nothing reads is a number that goes up. Gate 16 checks for at least one.

**And here is one, because until 2026-08-29 there was not one anywhere in this skill.** Counted
across every reference file: **zero worked blocks contained a condition on a currency.** The only
money example the skill has ever shown is `engine.md` §27's `costs` block — which is the *other*
channel, the one the lint below this section says everyone over-uses. **The skill showed the
habit it complains about and never showed the alternative.** That is `register.md`'s *"nothing
outranks an example that was never written"* — the failure is an absence, not a bad example, and
`## Show the mechanism. Never show the world.` there is the rule this block is written under.

The shape: **one object, several rungs, and the prose under it changes as she saves toward it.**
This is R1 and `R1b`'s showing-the-purchase clause in the same block — the thing is on screen long
before it is affordable, and the screen reports her progress at it.

```toml
# ⚠️ ORDERED HIGHEST-FIRST, and that is not style. Adjacent [group] blocks compile
#    into ONE exclusive if/elseif chain, so a low-first ladder is DEAD below its
#    first rung — the `lt` case would match forever and nothing after it renders.
blocks = [
  { type = "paragraph", content = "<the object, as it always looks — the line every rung sits under>" },

  { type = "group", conditions = { version = "1.0", logic = "AND", items = [
      { type = "flag", subject = "player", flag_key = "<thing>_bought", operator = "is_true" },
    ] }, blocks = [
    { type = "paragraph", content = "<she owns it — what stands where it used to stand>" },
  ] },

  { type = "group", conditions = { version = "1.0", logic = "AND", items = [
      { type = "trait", subject = "player", trait_key = "<currency>", operator = "gte", value = 400 },
    ] }, blocks = [                                                          # = <full_price>
    { type = "paragraph", content = "<she has the whole price — and what is missing is not money>" },
  ] },

  { type = "group", conditions = { version = "1.0", logic = "AND", items = [
      { type = "trait", subject = "player", trait_key = "<currency>", operator = "gte", value = 200 },
    ] }, blocks = [                                                          # = <full_price> / 2
    { type = "paragraph", content = "<halfway, counted in a unit she can name — weeks, shifts, Fridays>" },
  ] },

  { type = "group", conditions = { version = "1.0", logic = "AND", items = [
      { type = "trait", subject = "player", trait_key = "<currency>", operator = "lt", value = 200 },
    ] }, blocks = [
    { type = "paragraph", content = "<the price, and how far away it is from here>" },
  ] },
]
```

⚠️ **The numbers are the one thing not to copy.** `400` and `200` are filler and their only
doctrine is the *relationship* — a full price and its half. What the price should actually be
against a week's income is **R3c**, below, and it is derived per game. *An example outranks every rule
beside it* — do not copy these.

⚠️ **Conditions need `version = "1.0"` or they FAIL OPEN** — the engine returns true for any
`conditions{}` without it, with no build error, so a ladder missing it renders every rung at once.
`engine.md` §2. Note that a **quest card** takes the opposite form and must never be given this
key; `the-voice.md` R2 shows the two side by side.

### R1b · What money buys has to STAY bought

R1 is satisfied by a price on a cup of coffee. That is not what the field sells.

> **Measured 2026-08-28** over 25 corpus games, ~55,000 passages
> (`~/Documents/Accumulation_Study_20260828/`). Selection was structural, never by name, and every
> figure below was then hand-read in the passage — the parent study's `$slaverent` error is the
> reason for both halves of that sentence.

**Nine of the corpus games sell the player a THING, and the four most-engaged sandboxes in the field
all do.** A company, a car, five bedrooms, a home tier, a church, a lab, a farm, a bike, a hotel
room, a rack of servers.

An owned thing is not a meter, and the difference is structural:

```
owned thing    FEW write sites, MANY read sites    bought once; gates content forever after
meter          many write sites, many read sites   every scene nudges it
```

| game | rank | what she owns | price | condition sites it gates |
|---|---|---|---|---|
| become-someone | 4 | a company, `$startup.level` 1→4 | 20k / 50k / 100k | **114** |
| become-taxi-driver | 12 | a tuned car, `$car.body` 0→3 | shop | **46** |
| destroyer | 2 | five room levels | 30k / 60k | 21 · 20 · 16 · 16 · 16 |
| corpo-life | 9 | a home tier | four tiers | 79 |
| apocalyptic-world | 1 | a church, 0→5 | 50 wood + 80 energy + 8h **per stage** | 8 |

**Three shapes, and any of them is a correct answer:**

1. **The level ladder** — one thing that upgrades. `become-someone`'s company at 20k → 50k → 100k.
2. **The instalment build** — one thing bought in repeated payments. `apocalyptic-world`'s church:
   five stages, each 50 wood and 80 energy and eight hours, with the progress on screen as a
   percentage. This is why that game has **zero grind complaints in 820 comments** while running a
   resource economy: the repetition is building something, and it says so every time.
3. **The one-off possession** — bought once, kept. `destroyer`'s bedrooms.

#### The four things the field does with it that we do not

**a · The gate is COMPOUND.** Money alone never buys the next tier.

```
level 2 -> 3   $50,000  and at least TWO employees hired
level 3 -> 4  $100,000  and at least FIVE
```

So grinding one channel cannot skip the arc. `become-taxi-driver` goes further and requires the
asset *and* three separate relationships:
`$lya.friend >= 130 and $mia.friend >= 95 and $neptuno.friend >= 90 and $car.fase >= 2 and $car.body >= 3`.

**b · The asset is a SECOND AXIS on the people, not a parallel game.** Every one of
`become-someone`'s asset gates is ANDed with someone's ladder —
`$startup.level gte 4 && $tiffany.trust gte 15`, `$tammy.questmain gte 5 && $tammy.corr gte 40 &&
$startup.level gte 4`. **An owned thing that only gates its own arc has been built as a side game.**

**c · The locked state names its own price, and the finished state says it is finished.**

```
"You need $50,000 and at least two employees in order to upgrade the office"   red
"Your office is fully upgraded!"                                               green
```

Which is `the-voice.md`'s locked-door rule, executed by the field's #4 game, on an asset gate. Our
engine has this: `show_when_locked` + `locked_text`, and a cost-blocked choice already renders
*"(Requires N Money (you have M))"* on its own.

**d · It can be LOST, and losing it is recoverable.** `become-someone` runs a weekly payroll widget;
fail it and `<<Bankruptcy>>` takes the company. `Bank Recover Company` buys it back for **$500**. Two
of the nine assets carry upkeep at all (the other is `sluttown-usa`'s `$serverRent = $runningServers * 50`),
so **upkeep is optional** — but where it exists it is the same object delivering the pressure, not a
second system bolted on.

#### ⚠️ The failure this rule exists to prevent

**The player buys something and the game never mentions it again.** The purchase, the flag and the
price are all built; the doors are never cut. This is Study 7's fake-freedom defect in its economic
form — *asked to choose, answer discarded* becomes *asked to pay, purchase discarded* — and the same
zero-based test catches both.

**The check.** Gate **`what money buys opens a door`** — a flag set by a choice that costs the
currency, read zero times, is a FAIL. It fails only on zero, for the same reason
`the start choice is read` does: one house with one asset is not a distribution, and a floor invented
at n = 1 is how this skill lost its meter doctrine. The door counts print unjudged.

#### ⚠️ The till's own gate is not a door — and for a year it was counted as one

The gate counted a bought flag's reads as *the flag appearing in any condition anywhere*. But a
purchase always gates **itself**, in one of two places, and neither is content the money opened:

```
<flag> is_false  on the BUYING CHOICE            stops selling the same thing twice
<flag> is_false  on that canvas's TRIGGER        retires the row once it is owned
```

Every carefully-written purchase therefore collected a free `+1` and could never reach zero, so a
purchase that opened nothing passed.

**A second failure R1b does not name: she pays and never receives the thing at all.** R1b's shape is
*she pays and the game forgets*. This one is worse: the money leaves the wallet, a flag is set, and
the wardrobe is untouched — because a choice's `flagEffects` cannot put a garment in a wardrobe.
Only the engine's shop (`shop_location`) or a `wardrobeEffects` grant can. So the price buys a flag,
the flag gates nothing, and the garment it names is unobtainable. See `the-meters.md` W3 and the
gate `a declared garment can be got`.

**Both self-gate forms are excluded.** The trigger form is excluded in advance: it is exactly what
`<flag> is_false` on `[canvases.trigger]` produces, and an author writing it would silently re-open the hole. The exclusion is restricted to `is_false` — an
`is_true` test on the choice that sets the flag can never fire, so it is dead code either way.

**`the start choice is read` does not need the exclusion.** A start choice is
set once in the funnel and has no "don't ask twice" pressure to make its setter gate on it.

### R1c · A repeatable she PAYS for deposits something

A repeatable she pays for with time, energy or money should deposit something. Course of
Temptation's [GymCardio] costs her the session and pays it back every visit: `<<raiseskill
Physical 4>>`, then *"Your workout goes well and you make good progress."*

A **paid repeatable** is a choice on a repeatable canvas costing money or energy, or 30 minutes or
more.

> ⚠️ **A pure sink is not a defect. A game made only of pure sinks is.** Nothing in this file
> distinguished them. R2 asks whether money leaves; R1c
> asks whether anything remembers that it left.

⚠️ **The rule is about PAID repeatables, not every repeatable.** Ambient prose fires for free, and an
ambient is supposed to grant nothing; a rule over every repeatable surface would fail correct work,
which is the error that withdrew R4 and demoted study 6's anchoring check. **This is a lint —
`what a paid repeatable leaves behind`. It prints the rate and does not judge it.**

### R2 · Sinks outnumber sources

**Field: a median 2.2 spend-sites : 1 earn-site.** The reference game runs 1.76:1. The highest in
the corpus is 48:1. Only three games invert it and all three are the small ones.

**v2's floor is 1:1** — generous against that median, and it still catches a game with twelve ways to
earn and one way to spend. Gate 17.

Count both sides honestly: a rung that pays her for something is a **source**, not a scene. A game
whose only sink is rent has one sink no matter how many ways it pays out.

### …and they are SPREAD. Counting them is not enough.

**A sink belongs where the thing being bought lives.** The boiler upgrade at the boiler. The paint at
the frontage. The soap in the scrub room. Then the room *is* the reason she needs the money, and
earning it is aimed at somewhere she goes.

Pile them all at one counter and you have a **shop**, not an economy: money leaves the player in one
place, by one gesture, and no room in the world is ever the reason for it.

> Measured failure: a game passed this gate at **21 sinks : 20 sources** while **twelve of those
> sinks sat on a single front desk** — the water test, the advert, the electric, two wages, the
> frontage, the occupancy fee — in the same undifferentiated list as *"Look up at the board."*
> The first version of this gate counted them and said PASS.

Gate 17 now fails when **more than half the sinks resolve to one location** (applied once a game has
five or more, below which concentration is meaningless). It is the same distinction the heat gates
already make and this one was built without it: **presence is not placement.**

### R3 · The obligation is real, recurring, and has a face

**Field: 14 of 19 games carry a recurring obligation** — rent, debt, a loan, bills, tuition. The
reference game says *rent* 130 times.

> ⚠️ **NAME THE CORPUS, because it is not the one this skill writes for.** That 14 of 19 was
> measured on `~/Documents/Economy_Pressure_Study_20260827/`, whose table holds **17 games, of
> which two are female-led** (`course-of-temptation`, `zaras-school-life`). The 27-game field
> behind most of this skill is **20 male · 6 picked · 4 female** (`the-want.md` §1). So R3
> describes the **male-lead** economy accurately and says nothing about the default protagonist.
>
> Re-measured on the female-lead field 2026-09-04 with these same regexes
> (`~/Documents/Female_Hold_Study_20260904/probe_a.py`): a mechanically-real recurring obligation
> is **6 of 23 — 26%**, against 74% here. And a hand-read of all 23 puts the bill **fourth** among
> nine hold shapes, behind an ambition she picked herself.
>
> **R3–R3d are not wrong and nothing below changes.** They are the mechanism for a game that picks
> `bill`, and they are the best-evidenced pages in this file. What moved is upstream: `the-want.md`
> §1b no longer tells every author to pick one. If yours does, everything from here down applies.
>
> ⚠️ That study's own `obligation.py` carries a false friend this one found and fixed:
> `\w*rent\w*` matches *cu-RRENT* and *pa-RENT*, `\w*bill\w*` matches *BILL-iards*. Its per-game
> `vars:` column is contaminated; its headline — the ratchet, read out of DoL's `rentpay` widget by
> hand — does not depend on the regex and stands.

Three things make it work, and they are cheap:

- **A date.** It converts *"you could work"* into *"Monday, $120, or else."*
- **A face.** Someone collects. The pressure becomes social as well as arithmetic.
- **Armed after income exists.** Pressure before she has a way to earn is a scripted loss, not a
  choice.

> ⚠️ **AND A PRICE THAT IS ACTUALLY TAKEN. Declare it as a number, not only as prose.**
>
> ```json
> "economy": { "currency": "money",
>              "obligation": "Friday rent, paid to the landlord at the door…",
>              "obligation_amount": 200 }
> ```
>
> *(That example said **forecourt** until 2026-08-23 — one of the eleven words used by zero of the
> 25 field games, sitting in a JSON snippet, which is the highest-copy form this skill has. Found
> by the verification step of the pass that added `meter`, `float`, `pitch` and `chemist` to the
> false-friend list: after editing the skill, re-sweep the skill. `register.md`, "The examples are
> the register".)*
>
> Gate 16 is a presence gate: *"at least one exists"* cannot see that the important one does not.
> **Gate 24** closes it — declare the obligation and its amount, and something must charge at least
> that much. An obligation declared with no `obligation_amount` fails.

> ⚠️ **`[settings.rent]` is itself a charge.** The engine takes the amount on its own, so a canvas
> that also narrates the payment is a **duplicate** of it: with no cost it is a second settle-up,
> free and repeatable; with one, she pays twice.
>
> - **If `[settings.rent]` is doing the charging, do not also author a canvas that narrates the
>   payment.** Write the scene beside it instead — the evening after, the ask before. `engine.md` §26
>   has the full mechanism, including the fact that it arms at MIDNIGHT on `due_day`, not at the
>   hour the collector's schedule row puts him in front of the player.
> - **Gate 24 reads `[settings.rent]` as a charge channel**, beside `costs` entries and
>   `op = "add"` with a negative value. It does not count `op = "subtract"`: that op does nothing
>   (`engine.md` §21b).

⚠️ **And the half that gets forgotten.** An obligation that cannot be paid is a scripted loss — but
an obligation that is *trivially* paid is not pressure either, and only the first failure is
usually guarded against. **Price it against the income channels in both directions.** Count what a
week actually earns before setting the amount, then check that a bad week hurts. Course of
Temptation does the sum in both directions: [WeeklyDebtPayment] caps the debt at 200 with the
comment *"must be removed someday once money is easier"*, and [EventCampusHomeworkBuyOffer] prices
a side job off the debt itself, `<<set _cash to Math.floor($weeklydebt * 0.15)>>`.

> **Declare `week_income` beside `obligation_amount`.** This file asked for arithmetic, and an
> author with nowhere to put the sum does it in a prose comment or not at all. An instruction with
> no field is a wish.

### R3b · An obligation that does not MOVE is soft at any value

**This is the rule E1 was really about, and the number was not the answer.** A constant obligation
against an income that rises is soft by construction: raising it moves the week it stops mattering
and does not change the shape. Every field game whose economy stays live moves the number.

**Three shapes, all measured 2026-08-27. Pick the one your collector can justify.**

| shape | mechanism | who ships it |
|---|---|---|
| **imposed ratchet** | the number climbs on its own as she earns | `degrees-of-lewdity`, `course-of-temptation` |
| **cost follows holdings** | she bought something; it costs to keep | `sluttown-usa`, `the-hellfire-club`, `inseminator` |
| **the tier you chose** | the number is a function of what she is living in | `corpo-life` |

**1 · The imposed ratchet, and the thing that makes it work.** `degrees-of-lewdity` (numbers
only), `Widgets_Rent`: one widget takes the payment, sets the next week's figure from a fixed ladder
— `[10000,30000,50000,70000,100000,150000,200000][Math.clamp($rentstage,1,6)]` — has the collector
say the new number out loud, and advances the stage.

Money is in pennies (the widget says so: *`<!-- (amount in pennies…) -->`*, cross-checked against a
link reading `£15` that charges `<<money -1500>>`), so that is **£100 → £2,000 over seven
payments.** `rentmod` multiplies it by a **player-facing 10–300% slider** and doubles it if she took on a
second debt.

⚠️ **`$rentstage` is read in exactly five places and NOTHING in that game is gated on it. She gets
nothing for the rise.** It works because the rise is **delivered in the collector's mouth at the
moment of payment** — the same widget that advances the stage prints the next number, so the player
is never surprised, and the collector is a believable threat. `course-of-temptation` does the identical
thing through her mother (*"the interest is killing us… next week we're going to need $X"*).

**On this engine the ratchet is `[settings.rent] stages` with `stage_lines`** (`engine.md` §26): the
payment that moves the stage shows the collector's line with the new number, the same moment DoL uses.

**So: a bare ratchet needs a person whose motive the player already accepts.** If the money is
already owed to the household — a wage handed over, a till counted — a number that climbs on its own
reads as the author turning a dial, and the shape below is the honest one.

**2 · Cost follows holdings — the shape that needs no collector.** `sluttown-usa` charges
`$serverRent = ($runningServers * 50)` every Friday. She built the servers; they cost. The rise is
*hers*, it is legible, and nobody has to justify it.

**3 · The tier you chose, and the end state worth stealing.** `corpo-life` — the corpus game with
**zero grind complaints** — sets rent from where she lives (`StoryCaption`):

```
Rented Small Apartment 200 · Spacious 800 · Luxury 10,000 · Penthouse 30,000
Owned  (all eight tiers)  → 0
```

A 150× spread, and **owning zeroes the obligation.** Buying your way out of rent entirely is the
economy's ending. Its extra apartments cost $1,000 and $20,000 a week and **buy content** —
`Nene_Dinner_8` offers *"Why don't we go to my place?"* only when `$rent_studio_apart is 1`.

### R3c · If the demand rises, the income has to rise with it

⚠️ **Otherwise the ratchet is the corpus's single most-punished design.** The two field games that
deliberately made money bite are the two whose players are angriest about it, and one of the devs
answers in-thread that he is undoing it.

**Grind is not the complaint. Grind that buys nothing is.** `course-of-temptation`'s answer is to
denominate the payouts in the obligation itself — its homework jobs pay
`Math.floor($weeklydebt * 0.15)` — so a rising debt is a **difficulty curve** and never more
clicking.

**This holds for every money system, not only the obligation.** Each system that pays names its sink
and its deadline on its card (`board.systems[]`, `the-systems.md` SY8), and its pay ladder rises with
the bill it answers to. The price is shown before she agrees — gate 21, below.

**The engine can compute an effect value from her stats** (`{type = "trait", …}`, `engine.md` §3); when a game doesn't use it, do it with a band: gate a better-paying variant of
an existing rung on the same flag that turned the obligation up, and keep the original behind the
flag's `is_false`. Worked example, invented numbers: buying a van adds `-20/day` on the
day hook (`+140`/week of obligation) and turns a $30 errand into a $120 haul (`+450`/week over five
runs). The week's demand goes 260 → 400, she is 310 better off, and **both of those are her doing.**

**Two engine routes, both notified.** The bill itself rises with `[settings.rent] stages` (R3b,
`engine.md` §26); a cost that follows holdings is a daily upkeep: `[engine.daily_tick]` takes
`traitEffects` with a per-effect condition gate (`template_import.py:755`), applied through
`setup.applyAndNotifyTrait` (`v2.py:7291`). Either way the player is told. A silent charge meter is
the one economy device the corpus universally hates (`sluttown-usa` is the counted case).
⚠️ With `stages`, never write the rent into a `trait_bar max` or a quest goal: `_traitMax` is static
(`v2.py:19512`), so the number there stops being true at the first stage.

**A short week is carried, not a game over** *(LO decided, D8d; R4 found 3 of 9 bill games do end
it)*: `on_short = "carry"` (`engine.md` §26).

### R3d · The obligation is an ignition, not a tax — and it is allowed to go quiet

**R3b says make it move. This says where it is going, and that it is allowed to stop.** Measured
2026-09-01, `~/Documents/Ignition_Study_20260901/` (`probe.py` regenerates all of it).

**Both top games build the ratchet and then cap it by hand.** This is not decay or neglect; it is
an author reaching in and switching it off.

```
degrees-of-lewdity   [10000,30000,50000,70000,100000,150000,200000][Math.clamp($rentstage,1,6)]
                     seven rungs written, SIX reachable — £100 to £2,000, then flat forever

course-of-temptation $weeklydebt is 100 and $debtpaid gte 500   ->  += 50
                     $weeklydebt is 150 and $debtpaid gte 1000  ->  200
                     false and $weeklydebt is 200 and $debtpaid gte 3000    <- disabled
                     false and $weeklydebt is 250 and $debtpaid gte 8000    <- disabled
                     $weeklydebt gt 200 -> to 200                           <- hard cap
```

Five rungs authored, **three shipped**, the top two killed with a literal `false and`. The author
left his reason in the build: `/* !!!! must be removed someday once money is easier */`.

**Why capping it is correct: the obligation gates almost no content.** In `degrees-of-lewdity`,
**57 of 91,814** condition sites read `$rent*` — and reading them settles what they are: 20 are
*`$renttime lte 0`* (is it due), 10 are *`$money gte $rentmoney`* (can she pay), four are one story
thread, and the rest are save migration. Against that, **1,336** sites are gated on tier rungs.

**So the bill's job is the opening hours, and only those.** It has to be there in week one, when
she has no standing, no capability and no ladder — that is what buys the first transgression. Once
the meters gate content, the bill going soft is the system working, not the system failing.

⚠️ **This does NOT license a flat number.** R3b still holds for the stretch where the bill is doing
its job: a constant against a rising income goes soft *before* the meters are ready to take over,
which leaves a gap where nothing is pulling. Ratchet it through the ignition, then let it plateau.
**A plateau is fine, but the deadline persists:** the bill stops climbing; it does not stop coming due.

⚠️ **And it does not license squeezing.** R3c owns that half and the corpus is unambiguous. The
opening should be uncoverable by *clean work* — never uncoverable. The transgressive route has to
be open, obvious and well paid on day one, or the ratchet is a wall instead of a door.

**Not a gate.** Four corpus games carry a recurring obligation; a threshold read off four games
would be invented.

### R4 · Prices move with state

**Field: a median 24% of money movements carry a computed rather than a literal amount** — 86% at
the top, 21% in the reference game. Real games price things off the player's situation.

The corpus range is wide, so this is **guidance, not a gate**. But a game where every grant and
every price is a hardcoded constant has an economy that cannot respond to anything.

---

## And two rules from failure, not from the field

### R5 · No free, uncapped income — and "behind a gate" is not a cap

A surface the player can simply click that grants currency with neither a per-day cap nor a `costs`
block is a money printer, and **every other rule here is void beside it**. One such loop makes rent
irrelevant, which makes the trade tier irrelevant, which makes the arc gated behind it unreachable
by design.

> ⚠️ **This rule used to carry an exemption and the exemption swallowed the whole architecture.**
> It read: *"a triggerless rung reached through a gated hub choice is held to a weaker standard — it
> is not free, only farmable."* **Every rung in a v2 game is a triggerless rung behind a hub
> choice.** **A gate in front of a printer delays the printer.** Struck 2026-08-16; gate 18
> now fails on any uncapped income rung, gated or not.

**The tools, and which ones actually work here.** `max_triggers_per_day` is read off the *trigger*
(`engine.md` §27–§28) — a triggerless rung has none, so on the rung this architecture is built from
it does nothing. What works:

| tool | applies to |
|---|---|
| `costs` on the hub choice | any rung. Engine-enforced — an unaffordable choice is not offered (`engine.md` §27) |
| a `_today` flag cleared in `[engine.daily_tick]` | any rung (`engine.md` §28) — use a **flag**, not a counter trait |
| `max_triggers_per_day` | only a canvas that has a `[canvases.trigger]` block |

The full menu, and why one brake alone is brittle, is `references/the-meters.md` M3–M5.

**Both brakes on one choice, which is what a paying rung actually looks like:**

```toml
[[canvases.nodes.exit_block.choices]]
text                     = "<the act, and the duration in the game's one form> (2h)"
targetType               = "location"
locationId               = "<where she ends up>"
time_progression_minutes = 120
costs                    = [ { trait = "energy", value = 10 } ]
conditions               = { version = "1.0", logic = "AND", items = [
  { type = "flag", subject = "player", flag_key = "<rung>_done_today", operator = "is_false" },
] }
flagEffects      = [ { targetType = "player", flag = "<rung>_done_today", op = "set" } ]
show_when_locked = true
locked_text      = "<why it is closed, in the fiction — and that it reopens tomorrow>"
effects = [
  { targetType = "player", trait = "<currency>", op = "add", value = 22, clamp = false },
]
```

```toml
[engine.daily_tick]
flagEffects = [
  { targetType = "player", flag = "<rung>_done_today", op = "unset" },
]
```

⚠️ **This template is for WORK, and 2026-09-02 is when that stopped being implicit.** It resolves the
act into a 2-second numeric toast and returns the player to the room, which is right for a shift —
nobody needs a paragraph about stacking shelves. It is **not** right for a rung aimed at a person, or
at her own body: `the-surfaces.md` R9 owns that split, and nothing in this file drew it.

Six rules are carried by that one choice:

1. **`costs` is the brake the engine enforces for you.** An unaffordable choice is not offered, and
   the engine appends the requirement to the greyed row *with no authoring* — `Requires 15 Energy
   (you have 6)`. `engine.md` §27.
2. **The day flag is set in `flagEffects` on the CHOICE, never on a node exit.** A choice runs
   `flagEffects` *before* `advanceTime`; a node exit runs `advanceTime` first, which is where the
   day rolls and this hook clears. A rung that crosses midnight with an exit-set cap starts the new
   day **already capped**, and a sleep rung that runs overnight is never offered before midnight
   again from the second night. `engine.md` §28.
3. **A flag, not a counter trait.** A counter trait with an `lt` condition works and reads to
   gate 10 as a meter that only ever closes. `the-meters.md` M5.
4. **`clamp = false` on the money grant**, or the engine caps the balance at 100 (`engine.md` §21).
   ⚠️ And know the asymmetry: a **canvas or location `costs` deduction is clamped to 0–100** and
   cannot be unclamped, so above 100 it truncates the balance. A choice's `costs` is not clamped. §27.
5. **`show_when_locked` + `locked_text`** — a shown-locked row with no reason is mute, which is the
   gate `a locked door says why`. A cost-only choice is exempt, because the engine writes its own
   reason; a *flag*-locked one is not (a number lock gets the engine's line, `engine.md` §15).
6. **The duration is on the label**, in one form held across the game, and it is the real spend.
   A label may never name a clock time — the engine has no absolute-time advance.
   `the-clock.md` C3/C4.

⚠️ **Every flag cleared in `[engine.daily_tick]` must be SET somewhere.** Two of the three parts
validates nothing on its own: a `_today` flag that is cleared and never set throttles nothing, and
one that is set and never cleared closes the rung permanently on day two. Gate `a day-cap closes`
checks the first.

### R6 · The same test applies to any trait a condition reads

This file protects the currency. In this architecture **the currency is not what buys the content** —
the ascent tiers are, and per-NPC relation is. A game can obey every rule above and still hand its
entire ladder away, because nothing here ever priced a meter.

An income loop and an ascent rung are the same defect wearing different clothes: *a repeatable
surface that grants a number some gate reads, with no brake on how often it can be clicked.*

Judged by **gate 26** and owned by `references/the-meters.md` M1. It is named here so that a reader
who arrives at R5 by way of a money bug does not leave thinking money was the whole question.

---

## And one rule about what the player reads

### R7 · One currency, declared once, and the engine set to it

> **It is not a typo.** Without one printer, the price of a single click reaches the player in as
> many as six notations, and half of them the author never types:
>
> ```
> room-list button   Buy a coffee (GBP 3)                         author
> the choice         Pay three pounds (GBP 3, 5 min).             author
> the paragraph      … three pounds gets you …                    author
> when she is short  Requires 3 Money (you have 1)                engine  v2.py:5820
> the sidebar        money: 12 / 100                              engine  v2.py:19539
> rent day, short    $90                                          engine  v2.py:19276
> ```
>
> A `[[traits.labels]] key = "money"` label does reach the sidebar: `trait_bar` reads
> `_item.label || setup.traitLabel(_tbKey)` (`v2.py:19513`), and `setup.traitLabel` reads the trait
> labels (`v2.py:4701`, `engine.md` §33.3).

**The field's mechanism is one printer.** Measured across the 25-game corpus, the games with a real
economy do not type a symbol next to a number. They store one integer and render it in one place:

```
degrees-of-lewdity   money held in PENNIES; <<printmoney>> -> formatMoney()
corpo-life           formatUSD($money) — one Intl.NumberFormat call
the-hellfire-club    <<printmoney>> — guineas / shillings / pence, divisors 252 and 12
new-life-project     StoryCaption prints  £$money
```

Three unrelated economies, one architecture. The symbol is applied at a single site, so it cannot
drift. That is why the field's consistency is high:

```
                                        FIELD
one notation, share of money refs        92% median   (field min 56%)
priced link labels using the SYMBOL      94.0%
       …using a spelled-out unit          5.2%
       …using a currency CODE             0.8%   (5 labels, all corpo-life)
a money WORD carrying an EXACT amount     20%
```

**We have no printer**, so every price is retyped by hand and the engine adds notations of its own.
`[settings.rent] currency_symbol` is the closest thing to one, and of the sixteen sites where the
generator prints a money figure it governs **five — all on the rent pages**. Eight hardcode `$`
and three print no notation at all (`engine.md` §33 carries the full census). A game that declares
`currency_symbol = "£"` gets `£` on every rent screen and `$` on its shop, phone bank and job board.

#### The rule, in four parts

**1 · Declare it.** `board.economy.symbol` in the ledger, beside the currency trait. This works
whether or not rent is enabled, and it is the same declare-then-check pattern this file already
uses for `board.economy.currency` — the gates infer when nothing is declared, and an inference is a
guess.

**2 · Set the engine to it.** If `[settings.rent]` is on, `currency_symbol` must equal the declared
symbol. Left out, it defaults to `"$"` (`v2.py:1201`) and the rent card contradicts every button in
the game.

**3 · A price on a button is a figure in that notation.**

```
✅  Feed the meter ($3).            ✅  Buy it (£25).            ✅  Add 1000 caps
❌  Feed the meter (GBP 3).         ❌  Put three pounds in (GBP 3, 5 min).
```

Gate 21 already forces the *amount* onto the label. This adds only that the *notation* beside it be
the game's one notation.

**4 · Spelling it out belongs in a mouth, not on a button.** *"Three hundred, Friday, and don't make
me ask"* is right and the field agrees — 80% of its money words carry no exact figure at all. What
is wrong is spelling a price on a **button**, because a button is interface and interface has to
match what the engine prints two screens later. v1 found this exact trap and scoped it to one line:
`author-game/references/prose-truth.md` §2 — *"an authored override is a literal string"* — a game
that sets `amount = 125` and writes *"Hundred and twenty-five"* is correct today and contradicts its
own UI the day it re-prices. **The same debt is carried by every hand-typed price in the game, not
just the rent greeting.**

#### The house default is `$`, and this file calls it *the currency*

Not taste. Two measurements:

- **`$` is the only symbol the engine renders consistently.** Nine of its money print sites
  hardcode it (`engine.md` §33.1). Declare anything else and the shop, the bank, the job board and the
  rent-short screen still say `$`.
- **The field agrees anyway** — of 16 corpus games with a real economy, 10 use `$`, 2 `£`, 1 a
  currency code, 3 an invented unit.

Name no real-world currency in the prose. A game set in a specific place still has a landlord, a
price and a wage; it does not need the word *pounds* to have them.

> ⚠️ **The symbol is a PREFIX, and the engine has no suffix form.** All four rent prints concatenate
> symbol-then-number (`"Pay " + _cur + _rent`, `v2.py:17542`). An invented unit that reads as a
> suffix — `10 coin`, `1000 caps` — is legitimate and the field ships it, but it cannot go through
> `currency_symbol`. **If rent is enabled, the notation has to be a prefix.**

> ⚠️ **The ledger is player-invisible and it drifts anyway.** A `board.economy` that records
> `GBP 200` while the settings declare `£` is a design record that disagrees with the game, and that
> is how a re-price goes wrong later. Write the declared symbol there too: the money lint compares
> `board.economy.symbol` with the prose's unit (`scripts/gates.py:6162-6166`).

#### Why one is a gate and two are lints

**Gated:** *does the game use more than one currency?* Collect every notation on a canvas name, a
choice text and the engine's own symbol; map a symbol to its unit (`$`≡dollars, `£`≡pounds) so a
game is not failed for using both forms of one currency; fail on two units. Pure string work, no
judgement.

**Not gated:** *is a price spelled out rather than figured?* `zaras-school-life` writes every price
in words across 905k words and is perfectly consistent; `apocalyptic-world` ships `Add 1000 caps`.
A rate gate would fail both for obeying
the rule. Both rate checks print and never move the tally.

---

## What the board phase records

```jsonc
"board": {
  "economy": {
    "currency":   "money",
    "symbol":     "$",
    "obligation": "rent — Monday, from the landlord, in person",
    "obligation_amount": 120,
    "week_income": 430,
    "obligation_moves": "the boiler she bought — 15/week from the day it is in",
    "sinks":      ["rent", "the boiler", "the bus fare", "her phone"]
  }
}
```

**`week_income` is R3's arithmetic, given somewhere to live.** What a full week of the income rungs
actually pays, written down where the obligation is — not an estimate of what a player will earn,
the honest maximum, with the working. Declare it and the lint prints the ratio beside the two
numbers; leave it out and the lint says so.

⚠️ **This is a LINT and never a gate.**

`symbol` is the notation every button, every paragraph and `[settings.rent] currency_symbol` must
agree with (R7). Declaring the currency is strictly better than letting the gates infer it from
`player.core_traits` — the headline says which was used, and an inferred currency on a game with two
of them will pick the wrong one.

**Listing the sinks in the ledger is the useful part.** It is the question *what is money actually
for in this game* asked at the point where it is still cheap to answer. Each money system's own sink
and deadline live on its card (`board.systems[].sink`, `.deadline`; `templates/sheets/system.md`).

---

## What is checked, and what is not

| | |
|---|---|
| **Gate 16 · money gates something** | ≥1 condition reads the currency, **or** ≥1 choice prices itself in it |
| **Gate 17 · sinks >= sources** | at least as many ways to spend as to earn |
| **Gate 18 · no free uncapped income** | **no** surface grants currency without a cap or a cost — gated rungs included (R5, reworded 2026-08-16) |
| **Gate 21 · a price is on its label** | every choice that spends currency names the amount in its text |
| **Gate 24 · the obligation is charged** | if `board.economy.obligation` is declared it must carry an `obligation_amount`, and something must charge at least that much — either an authored charge (a `costs` entry, or `op = "add"` with a negative value) on a **recurring, non-dev** canvas (on `board.economy.settle_canvas` if declared), or `[settings.rent]`. **Since 2026-09-26:** a week must be able to pay it — the average weekly income the build can bring in (best exit per capped canvas, × days) must reach the obligation unless `obligation_moves` signposts when it will; and a declared `week_income` above what the build can pay FAILS as stale |
| **Gate 25 · effects use a live op** | no effect uses an `op` the engine discards — the economy's deductions in particular |
| **Gate 26 · the climb is paid for** | R6 — every trait a condition reads has a brake on the rungs that raise it (`the-meters.md` M1) |
| **Gate · the price is in one currency** | R7 — every notation on a button, plus the engine's own `currency_symbol`, resolves to ONE currency. A symbol and its spelled-out unit count as the same one |
| **Gate · what money buys opens a door** | R1b — a flag set by a choice that costs the currency, surviving the night, must be READ somewhere. **Fails only on ZERO**; a game that sells nothing reports `n/a`, which is not a pass. Day-capped flags are carved out, as gate 18 does |
| **Lint · money gates content, or only prices it** | R1 — gate 16 passes on either channel and cannot tell them apart. A CONDITION on the currency means content money OPENS; a `costs` block only means a thing can be bought |
| **Lint · what a paid repeatable leaves behind** | R1c — the share of paid repeatable choices that deposit anything. A pure sink is not a defect; a game made only of pure sinks is. A rate, never a score |
| **Lint · the currency in the prose** | the game's dominant-notation share against the field's 92% median, and its exact-amount-in-words rate against the field's 20% |
| **Lint · the price is spelled out** | the form of every priced label — symbol / word / code — against the field's 94 / 5 / 1 |
| **Lint · the obligation against the week** | R3 — `obligation_amount` over `week_income`, printed, never judged. Says so when `week_income` is not declared |

**Whether the pressure is actually felt is deliberately not a gate.** Whether $120 against a $42 day
*squeezes* is a play question. These five establish that a squeeze is possible; only a playthrough
establishes that it happens.

---

## ⚠️ Two ways these gates read the wrong thing — both found 2026-08-14, both fixed

**A `costs` block is a gate.** The engine refuses a choice the player cannot afford
(`v2.py:5058` filters it out, `:5202` is the check — `engine.md` §27), but gate 16 was built from
*conditions* only. A game that prices its choices
instead of condition-gating them therefore read as **"nothing in the game reads the currency"**. Gate 16 now counts either channel.

**Declare your currency, or the inference will pick one.** With `board.economy.currency` unset the
gates guess from trait names, and until 2026-08-14 they took the *first* name match, so a game
running **two real currencies** could have every economy gate judging the wrong one. The hint list also had no
entry for `coin`, so a currency by that name was invisible outright.

Selection is now by **usage**, and the chosen currency plus the runners-up are printed on gate 16's
line so a wrong guess is visible rather than silent. **Declaring `board.economy.currency` skips all
of this** — the declare-then-check pattern exists precisely because inference is a guess.
