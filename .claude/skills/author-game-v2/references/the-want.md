# The Want — the one page every release is checked against

## Why this exists

A previous game had a fantasy specification written on its first turn. It was good. It named
its charge in three parts. It was then never opened again, and the game shipped reading as a
crime thriller with sex in it.

The defect was not the absence of a spec. It was that nothing in the process ever read it
back. So the rule here is mechanical, not aspirational:

> **The Want is an input to every release. A release that cannot name which line of the Want
> it serves does not ship.**

Write it before the world. Re-read it before every release. Amend it deliberately and log the
amendment — never let it quietly stop being true.

## The form

Keep it to one page. Longer means vaguer.

### 1. Who she is
Her situation at minute zero, and what she has to lose. Concrete: a job, a debt, a room, a
reputation. The thing that makes the first transgression cost something.

### 2. The appetite that never fills
What she wants, phrased so it can never be finished. "Get revenge on X" finishes. "Be wanted
by people who shouldn't want her" does not.

This is the line that decides whether the game can run forty updates. Test it: *what does
release 41 do?* If you cannot answer, the appetite terminates and needs rewriting.

### 3. What she is becoming — stated as ACCESS
The ascent. For a female protagonist this is **not money and not status** — it is reach.

> Measured: the market's male-protagonist games run accumulation ladders (shop worker to CEO,
> teacher to mayor). Its female-protagonist games run one global axis whose rise *expands what
> she can reach* — the description of the strongest example is literally "as her corruption
> rises, the gameplay expands."

Write the ascent as a sentence about doors: at the bottom she can do these things in these
places; at the top she can do these things in those places.

**Then split it into three or four kinds of going-further.** Measured: the reference game does
not run one corruption axis — it runs separate ratcheting tiers for *sleeping around*, *being
seen*, and *doing the strange thing*, each gating content at 15 / 35 / 55 / 75, plus a purity
counterweight. Several tiers means several parallel ascents, so a player who doesn't want one
can still climb another. One undifferentiated meter hands every player the same ladder.

Name your tiers here. They become the meters in `references/the-board.md`, and each one's rise
must open content or gates 8 and 10 fail.

**Anti-pattern, measured:** a protagonist whose dominant meter rises toward failure while the
world contracts to a sealed room. Rising must widen.

### 4. The charge
One of — or a deliberate combination of:

- **Reversal** — someone with power over her loses it, or gains more of it than they should
- **Taboo** — the relationship itself is the transgression
- **Transformation** — she becomes something she would not have recognised

Name which. "It's hot" is not a charge; it is the absence of one.

### 5. Why *this* person
One line per character. Not their role in a plot — **why she wants them, or why being wanted
by them lands.**

> Measured, and the strongest single finding in ~11,000 player comments: praise for the porn
> itself scores lowest of every theme, while performer identity and character attachment score
> highest. One game swapped its performers and its three most-liked comments were the revolt;
> another recast and died. **The person is the product.**

A character with no line here is a character with no reason to exist. Cut them or write it.

### 6. Register
Three declarations, made once:

- **`narration_person`** — recommend `second`. It is per-game and immutable after the first
  release ships, because changing it rewrites every line. (The measured exemplar for a female
  protagonist is second person.)
- **Crude-vocabulary ceiling** — the actual words that may appear, per character and per tier.
  Write the words down. A ceiling described abstractly gets written around.
- **Where the crude register lives** — and the answer is **the repeatable surfaces**. This is
  the correction the whole system exists for: the measured failure wrote its explicit register
  only into content the player sees once, and wrote its fifty-times-replayed loops as literary
  character study.

## The test before you leave this file

Answer these four out loud. If any answer is soft, the Want is not done.

1. What does release 41 add? *(if unanswerable, the appetite terminates)*
2. What can she reach at the top that she cannot reach at the bottom? *(the ascent)*
3. Which character would a player miss if you deleted them, and why? *(the product)*
4. Which repeatable surface carries the crudest writing in the game? *(the register, in the
   right place)*

Then run the fifth, which is not a judgement call:

```
python3 scripts/gates.py --words games/<slug>/WANT.md
```

**Read the list. It is a list and never a score** — a word on it is not automatically wrong, and
the question is only whether a player arrives already holding it.

**Why here and not at the end.** The same check runs against a built game, and that is one phase
too late: by then every noun is set into a room name, a button label and the prose behind it, and
changing one means renaming things. **The Want is where a game's nouns get chosen** — its rooms,
its work, its objects and its meters all come out of this page. Measured: a Want written by an
author who had committed, one message earlier, to avoiding exactly this class of word still
shipped two of them, and only a hand-rolled check caught it.

Run it again on the board's location names before leaving that phase too. A word the player
cannot decode is undecodable on a button.

## Then

Create `games/<slug>/v2_state.json` with `phase = "want"` and the Want recorded, per
`references/state.md`. Move to `references/the-board.md`.
