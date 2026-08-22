# The Economy — the only system that can say no

Money is the one thing in a sandbox that makes the player **choose**. Everything else expands. If
money never says no, every arc gated behind it becomes optional scenery.

> **This file is measured across a field, not a single game.** 18 shipped browser sandboxes,
> ~62,000 passages, parsed 2026-08-12. Corpus, method and limits: `DOCTRINE_GAPS.md` Appendix B.
> The reference game this skill was originally derived from carries **738 money movements and 372
> money gates** — and none of that was ever measured, which is why this file exists.

> Measured failure it prevents: a shipped game with **zero** conditions reading money, zero items,
> one sink, and an uncapped free income loop. Its own spec said *"one bad week forces the ask."* No
> week forced the ask, so the whole ladder of its most important character was content the player
> was never pushed toward.

---

## The four measured rules

### R1 · Money must gate content

**Field: a median 67.3 conditions read the currency per 1,000 passages.** Every sandbox in the
corpus does it. The only two games at zero are a scripted time-slot game and a very small one —
neither is a sandbox.

A currency nothing reads is a number that goes up. Gate 16 checks for at least one.

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

Three things make it work, and they are cheap:

- **A date.** It converts *"you could work"* into *"Monday, $120, or else."*
- **A face.** Someone collects. The pressure becomes social as well as arithmetic.
- **Armed after income exists.** Pressure before she has a way to earn is a scripted loss, not a
  choice.

> ⚠️ **AND A PRICE THAT IS ACTUALLY TAKEN. Declare it as a number, not only as prose.**
>
> ```json
> "economy": { "currency": "money",
>              "obligation": "The Friday settle-up with Nunn on the forecourt…",
>              "obligation_amount": 245 }
> ```
>
> **Measured failure, and it is the worst kind — the mechanic the game is named after.** A shipped
> game declared *"£200 a week back, plus £45 for the caravan"*, printed *"Have the two hundred and
> forty-five"* on its quest card, and wrote the scene of handing money through a car window. The
> settle-up canvas carried **no cost and no money effect.** Played live with £300: before £300,
> after £300 — and repeatable without limit, in both directions, making it a free relation faucet.
> The game's entire money outflow was 11 optional purchases totalling £90 against £70 a night of
> income, so nothing in it ever squeezed.
>
> Gate 16 passed it, because nine *other* canvases gate on money. That is the presence-gate failure
> mode: *"at least one exists"* cannot see that the important one does not. **Gate 24** closes it —
> declare the obligation and its amount, and something must charge at least that much.
> An obligation declared with no `obligation_amount` fails: a price nobody can check is how this
> shipped.

> ⚠️ **AND THE OTHER HALF OF THAT STORY, WHICH TOOK A SECOND LOOK TO FIND.** The same game had
> `[settings.rent]` enabled at `amount = 245`, and it **worked** — verified live, 300 → 55 on the
> Friday rollover. So the obligation *was* charged, by the engine, and the authored canvas was a
> **duplicate** of it: a second settle-up, free, repeatable, and the one with the writing in it.
> Two consequences, and both are now doctrine:
>
> - **If `[settings.rent]` is doing the charging, do not also author a canvas that narrates the
>   payment.** Write the scene beside it instead — the evening after, the ask before. `engine.md` §26
>   has the full mechanism, including the fact that it arms at MIDNIGHT on `due_day`, not at the
>   hour the collector's schedule row puts him in front of the player.
> - **Gate 24 reads `[settings.rent]` as a charge channel.** It used to walk canvases only, so it
>   failed a game whose obligation was charged correctly. A check that fails a game for obeying the
>   doctrine is a bug in the check.
>
> It also used to count `op = "subtract"` as an outflow. That op does nothing (`engine.md` §21b), so
> the gate was crediting a charge that never happens — the exact failure it exists to catch,
> rebuilt inside the gate. It now counts `costs` entries and `op = "add"` with a negative value.

⚠️ **And the half that gets forgotten.** An obligation that cannot be paid is a scripted loss — but
an obligation that is *trivially* paid is not pressure either, and only the first failure is
usually guarded against. **Price it against the income channels in both directions.** Count what a
week actually earns before setting the amount, then check that a bad week hurts.

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
> choice.** Measured: a game shipped a rung paying £2 per 25 minutes, uncapped and repeatable,
> behind `standing >= 35` — against a £20 weekly obligation. Gate 18 saw it, printed
> `4 gated rungs are uncapped too`, and passed, exactly as instructed. Once the tier landed the
> economy was off. **A gate in front of a printer delays the printer.** Struck 2026-08-16; gate 18
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

### R6 · The same test applies to any trait a condition reads

This file protects the currency. In most v2 games **the currency is not what buys the content** —
the ascent tiers are, and per-NPC relation is. A game can obey every rule above and still hand its
entire ladder away, because nothing here ever priced a meter.

An income loop and an ascent rung are the same defect wearing different clothes: *a repeatable
surface that grants a number some gate reads, with no brake on how often it can be clicked.*

Judged by **gate 26** and owned by `references/the-meters.md` M1. It is named here so that a reader
who arrives at R5 by way of a money bug does not leave thinking money was the whole question.

---

## And one rule about what the player reads

### R7 · One currency, declared once, and the engine set to it

> **Measured failure, and it is not a typo.** A shipped game wrote the price of a single click
> **six different ways**, and half of them the author never typed
> (`games/off_season/toml_phases/3_activities.toml:83-108`):
>
> ```
> room-list button   Feed the meter (GBP 3)                       author
> the choice         Put three pounds in (GBP 3, 5 min).          author
> the paragraph      Six fifties … Three pounds gets you …        author
> when she is short  Requires 3 Money (you have 1)                engine  v2.py:4680
> the sidebar        money: 12 / 100                              engine  v2.py:16215 · :16241
> rent day           $90                                          engine  v2.py:1190
> ```
>
> The author had declared `[[traits.labels]] key = "money", label = "Change bag"` and expected the
> sidebar to use it. It does not: `trait_bar` reads `_item.label || trait_key` and never consults
> the trait labels at all (`engine.md` §33.3).

**The field's mechanism is one printer.** Measured across the 25-game corpus, the games with a real
economy do not type a symbol next to a number. They store one integer and render it in one place:

```
degrees-of-lewdity   money held in PENNIES; <<printmoney>> -> formatMoney()
corpo-life           formatUSD($money) — one Intl.NumberFormat call
the-hellfire-club    <<printmoney>> — guineas / shillings / pence, divisors 252 and 12
new-life-project     StoryCaption prints  £$money
```

Three unrelated economies, one architecture. The symbol is applied at a single site, so it cannot
drift. That is why the field's consistency is high and ours is not:

```
                                        FIELD            OURS
one notation, share of money refs        92% median       82% median   (field min 56%)
priced link labels using the SYMBOL      94.0%            see below
       …using a spelled-out unit          5.2%
       …using a currency CODE             0.8%   (5 labels, all corpo-life)
a money WORD carrying an EXACT amount     20%             51%
```

**We have no printer**, so every price is retyped by hand and the engine adds notations of its own.
`[settings.rent] currency_symbol` is the closest thing to one, and of the sixteen sites where the
generator prints a money figure it governs **four — all on the rent-day screen**. Nine hardcode `$`
and three print no notation at all (`engine.md` §33 carries the full census). A shipped game proves it: `forty_miles` declares
`currency_symbol = "£"` with the author's own comment *"the pages hardcoded `$` before this key
existed"* — and its released build still ships
`You have: <strong>$<<print $player.core_traits.money>></strong>` on `RentDay_Short`
(`v2.py:16000`), the screen the player sees **when she cannot pay**.

#### The rule, in four parts

**1 · Declare it.** `board.economy.symbol` in the ledger, beside the currency trait. This works
whether or not rent is enabled, and it is the same declare-then-check pattern this file already
uses for `board.economy.currency` — the gates infer when nothing is declared, and an inference is a
guess.

**2 · Set the engine to it.** If `[settings.rent]` is on, `currency_symbol` must equal the declared
symbol. Left out, it defaults to `"$"` (`v2.py:1190`) and the rent card contradicts every button in
the game. Eight of our ten built games enable rent; two declare a symbol.

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
> symbol-then-number (`"Pay " + _cur + _rent`, `v2.py:15929`). An invented unit that reads as a
> suffix — `10 coin`, `1000 caps` — is legitimate and the field ships it, but it cannot go through
> `currency_symbol`. **If rent is enabled, the notation has to be a prefix.**

> ⚠️ **The ledger is player-invisible and it drifts anyway.** `off_season`'s `board.economy` records
> `GBP 90`, `GBP 3`, `GBP 25`; `forty_miles`' records `GBP 200` while its settings declare `£`. A
> design record that disagrees with the game is how a re-price goes wrong later. Write the declared
> symbol there too.

#### Why one is a gate and two are lints

**Gated:** *does the game use more than one currency?* Collect every notation on a canvas name, a
choice text and the engine's own symbol; map a symbol to its unit (`$`≡dollars, `£`≡pounds) so a
game is not failed for using both forms of one currency; fail on two units. Pure string work, no
judgement.

**Not gated:** *is a price spelled out rather than figured?* `zaras-school-life` writes every price
in words across 905k words and is perfectly consistent; `apocalyptic-world` ships `Add 1000 caps`;
`vesper` prices ten labels `10 coin` and never varies. A rate gate would fail all three for obeying
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
    "sinks":      ["rent", "the boiler", "the bus fare", "her phone"]
  }
}
```

`symbol` is the notation every button, every paragraph and `[settings.rent] currency_symbol` must
agree with (R7). Declaring the currency is strictly better than letting the gates infer it from
`player.core_traits` — the headline says which was used, and an inferred currency on a game with two
of them will pick the wrong one.

**Listing the sinks in the ledger is the useful part.** It is the question *what is money actually
for in this game* asked at the point where it is still cheap to answer.

---

## What is checked, and what is not

| | |
|---|---|
| **Gate 16 · money gates something** | ≥1 condition reads the currency, **or** ≥1 choice prices itself in it |
| **Gate 17 · sinks >= sources** | at least as many ways to spend as to earn |
| **Gate 18 · no free uncapped income** | **no** surface grants currency without a cap or a cost — gated rungs included (R5, reworded 2026-08-16) |
| **Gate 21 · a price is on its label** | every choice that spends currency names the amount in its text |
| **Gate 24 · the obligation is charged** | if `board.economy.obligation` is declared it must carry an `obligation_amount`, and something must charge at least that much — either an authored charge (a `costs` entry, or `op = "add"` with a negative value) or `[settings.rent]` |
| **Gate 25 · effects use a live op** | no effect uses an `op` the engine discards — the economy's deductions in particular |
| **Gate 26 · the climb is paid for** | R6 — every trait a condition reads has a brake on the rungs that raise it (`the-meters.md` M1) |
| **Gate · the price is in one currency** | R7 — every notation on a button, plus the engine's own `currency_symbol`, resolves to ONE currency. A symbol and its spelled-out unit count as the same one |
| **Lint · the currency in the prose** | the game's dominant-notation share against the field's 92% median, and its exact-amount-in-words rate against the field's 20% |
| **Lint · the price is spelled out** | the form of every priced label — symbol / word / code — against the field's 94 / 5 / 1 |

**Whether the pressure is actually felt is deliberately not a gate.** Whether $120 against a $42 day
*squeezes* is a play question. These five establish that a squeeze is possible; only a playthrough
establishes that it happens.

---

## ⚠️ Two ways these gates read the wrong thing — both found 2026-08-14, both fixed

**A `costs` block is a gate.** The engine refuses a choice the player cannot afford
(`v2.py:4496` filters it out, `:4625` is the check — `engine.md` §27), but gate 16 was built from
*conditions* only. A game that prices its choices
instead of condition-gating them therefore read as **"nothing in the game reads the currency"** —
which is how a game with seven priced choices scored zero. Gate 16 now counts either channel.

**Declare your currency, or the inference will pick one.** With `board.economy.currency` unset the
gates guess from trait names, and until 2026-08-14 they took the *first* name match. A game running
**two real currencies** — one company-visible, one hidden and hers — had every economy gate judging
the wrong one, the one used once instead of the one used eighteen times. The hint list also had no
entry for `coin`, so a currency by that name was invisible outright.

Selection is now by **usage**, and the chosen currency plus the runners-up are printed on gate 16's
line so a wrong guess is visible rather than silent. **Declaring `board.economy.currency` skips all
of this** — the declare-then-check pattern exists precisely because inference is a guess.
