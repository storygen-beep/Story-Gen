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

- **A date.** It converts *"you could work"* into *"Monday, £120, or else."*
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

## And one rule from failure, not from the field

### R5 · No free, uncapped income

A **standing** surface — one the player can simply click — that grants currency with neither a
per-day cap nor a `costs` block is a money printer, and **every other rule here is void beside it**.
One such loop makes rent irrelevant, which makes the trade tier irrelevant, which makes the arc
gated behind it unreachable by design.

Give an income surface a `max_triggers_per_day`, a real `costs` block, or both.

*A triggerless rung reached through a gated hub choice is held to a weaker standard — it is not
free, only farmable. Gate 18 reports those and fails only the standing ones; R2 is what judges
whether the game simply has too many ways to earn.*

---

## What the board phase records

```jsonc
"board": {
  "economy": {
    "currency":   "money",
    "obligation": "rent — Monday, from the landlord, in person",
    "obligation_amount": 120,
    "sinks":      ["rent", "the boiler", "the bus fare", "her phone"]
  }
}
```

Declaring the currency is strictly better than letting the gates infer it from
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
| **Gate 18 · no free uncapped income** | no standing surface grants currency without a cap or a cost |
| **Gate 21 · a price is on its label** | every choice that spends currency names the amount in its text |
| **Gate 24 · the obligation is charged** | if `board.economy.obligation` is declared it must carry an `obligation_amount`, and something must charge at least that much — either an authored charge (a `costs` entry, or `op = "add"` with a negative value) or `[settings.rent]` |
| **Gate 25 · effects use a live op** | no effect uses an `op` the engine discards — the economy's deductions in particular |

**Whether the pressure is actually felt is deliberately not a gate.** Whether £120 against a £42 day
*squeezes* is a play question. These five establish that a squeeze is possible; only a playthrough
establishes that it happens.

---

## ⚠️ Two ways these gates read the wrong thing — both found 2026-08-14, both fixed

**A `costs` block is a gate.** The engine refuses a choice the player cannot afford
(`v2.py:12556`), but gate 16 was built from *conditions* only. A game that prices its choices
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
