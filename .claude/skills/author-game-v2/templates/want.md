# The Want — <game title>

> One page, five parts. Doctrine: `references/the-want.md`.
> **Re-read this before every release.** Bump `want.last_read_at_release` in `v2_state.json`.
> The detail tables live later: the crude words per rung on SP2, rung numbers, needs and the map shape on
> the board (`templates/board.toml`), and the fantasy and the promise on the idea page (`templates/idea.md`).

---

## 1. Who she is

<Her situation at minute zero. Concrete: a job, a debt, a room, a reputation.>

**The places she knows:** <name each> → `want.places[] = [{id, name}]`, so `--words` reads them as names.

**What she has to lose:** <the thing that makes the first transgression cost something>

**The player:** `female` · `male` · `picked` — `written` · `blank` — start choice: <what she is asked at
minute zero, or `none`>. Record in `want.player`, with the start choice's flags in
`want.player.start_choice` (`references/the-want.md` §1: the default and the evidence).

## 2. What holds her

<The hold, in her nouns, with a face and a moment it comes due.>

Money is written in the currency, house default `$`; no real-world currency in the prose
(`references/the-economy.md` R7). Every number on this page agrees with every other — one span is never said two
ways — and the reader checks it.

**Hold kind:** `ambition` · `bill` · `order` · `body` · `subsistence` · `appetite` · `job` · `erosion` ·
`displacement` → `want.hold_kind` (counts in `references/the-want.md` §1b).

The hold and the fantasy shape (idea page) are **separate choices**. `order`, `job` and `displacement` fit
any shape: an order can drive a fall by need, a job can drive a rise by want. These are ledger keys, never
player words.

## 3. What she wants

<What she wants, phrased so it can never be finished: where she lands, not where she starts.>

**The charge:** reversal · taboo · transformation → `want.charge` (`references/the-want.md` §4).

## 4. How she climbs

**Early:** <what she will do, and where, near the bottom — in words>
**Late:** <what she will do, and where, near the top — in words>

No numbers here. Tiers and rung values are set on the board (`references/the-board.md` §3b).

## 5. The people

| person | age | what she wants from him | what he visibly wants, each visit | what he keeps score of |
|---|---|---|---|---|
| `npc_<id>` | | | | |

Every person is 18 or older, and the age is written (`shape.py` fails a missing one). What he keeps: a step
counter + memory flags, Want + Warmth, or Want + Power (`references/the-meters.md` W1); LO approves each.
Record as `want.cast[] = {id, age, keeps}`, and what she wants from him as `want.why_this_person`.

---

## Before you leave this page

1. What can she reach at the top that she cannot at the bottom? (§4)
2. Which person would a player miss if deleted, and what does he want back? (§5)
3. Run the vocabulary check and read the list — a list, never a score:

   ```
   python3 scripts/gates.py --words games/<slug>/WANT.md
   ```

**Then:** create `games/<slug>/v2_state.json` with `phase = "want"` per `references/state.md`, and move to
`templates/idea.md`.
