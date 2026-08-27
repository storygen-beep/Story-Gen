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

### 1. Who the player is — settled before she is described

**Added 2026-08-27. Its absence is the single largest measured defect in this skill.**

Eight v2 games shipped one protagonist: a woman 19–39, held in place by money she cannot reach, in
second person, in a small town. Asked whether that was deliberate, LO said **"just happened."** It
did, and this file is why:

| | |
|---|---|
| `templates/want.md` — `she/her/hers` vs `he/him/his` | **21 vs 0** |
| this file — same count | **16 vs 0** |
| whole v2 skill — `male pc` · `blank.slate` · `self.insert` · `character creation` | **0 hits** |

**The grammar answered before the author arrived.** v1 asked the question first of anything —
`author-game/references/step-0-1-seed.md:17`, *"Pick the PROTAGONIST POV first — it decides which
fantasies even work"*, with female-PC and male-PC as named forks — and v2 deleted it. `vesper` is the
control: authored before this file existed, `narration_person = "third"`, none of the shape.

So three things are **declared** here, into `v2_state.json` → `want.player`, before §1b writes a
single line about her.

#### Who is the player? — `female` · `male` · `picked`

⚠️ **The default is `female` and the evidence is FOR it, not merely permissive.** Across ~22,600
corpus comments: **49 asking for a female lead (364 likes) against 11 opposed (124 likes)**, and the
opposed get argued down in their own threads. The top-30 count — 20 male, 6 picked, 4 female — is a
**supply** figure; a player in that corpus did the arithmetic himself at *"44 games with the Female
Protagonist tag and 100 with the Male Protagonist tag."* Do not read `4 of 30` as a verdict. The
sharpest practical argument is also a player's: *"as a guy I like to play female mc since we can get
to the spicy part quicker and not grind around like in male mc games."*

What this section is fixing is not the answer. **It is that the answer was never a question.**

#### Written character, or blank slate? — `written` · `blank`

Field: **19 blank to 10 written**, and blank carries **80.4%** of the top-30's engagement. All eight
v2 games are `written`, and no ledger records the choice being made. `written` is defensible — it is
what real-porn media and a named cast pull toward — but an undeclared default is not a decision.

#### What does the player choose about her at minute zero?

**`freedom` is the largest single thing this field is loved for.** Classifying reason (1) of every
top-30 game's *"why players love it"*, weighted by comment count:

```
freedom 25.9% · performers 22.0% · systems 15.8% · volume 15.6%
story 7.3% · characters 7.0% · cadence 5.4% · kink 0.8%

premise 0.0%   <- not one game in thirty is loved for its setup
```

The #1 game's #1 reason is *"farmer, slave merchant, bounty hunter, cage fighter, Cannibal? You can
be whatever you want."* **The choosing is the product; the premise is not.** That is also why the
first fix proposed for this — a step checking a new premise against the repo — was dropped.

**The rule: a memory, not a slider** (`~/Documents/Female_PC_Craft_Study_20260823/findings_A_want.md:93`).
Course of Temptation never shows a stat screen; it asks what kind of teenager she was and initialises
thirteen skills the player never sees. Ask something the scene is **already asking**, and set a flag
from the answer.

> **Worked example — `mrs_vance`, the only one that exists.** Its opening already asked the player
> four questions and **discarded every answer**: both choices on `open_dorn_leaves.base` and both on
> `.the_book` shared one target, carried no effects, and differed in no way. Nothing had to be
> invented — the ledger scene already implies *have you done this before?*, so `the_book`'s two inert
> choices became three, setting `past_books` / `past_road` / `past_counter`. Read at **5 sites each**:
> a three-band ladder on the three daily work surfaces, plus a paired privilege rung on each.
>
> The `past_road` rung is the one that shows what a start choice is *for*: she takes the truck key off
> the board herself, which is the bottom rung of this game's own declared ascent — *"she asks Cade for
> the truck to leave the property at all."* **A start choice buys reach, not flavour** (§3).

⚠️ **ADDITIVE ONLY.** Each original rung keeps every number it had and gains `<flag> is_false`, so the
pair is mutually exclusive, no door closes, and a save made before the choice shipped carries no flag
and reads exactly what it read yesterday. **A start choice that takes content away is the version
players punish.**

⚠️ **THE PLACEMENT TRAP, AND IT FAILS SILENTLY.** Adjacent `[group]` blocks merge into ONE if/elseif
chain (`v2.py:14637`) and first match wins. Drop a past-ladder next to a surface's existing ladder and
**that ladder becomes unreachable for every player carrying a past** — no error, no build warning, the
prose simply stops appearing. Both surfaces this was first built on already had one: `work_books` a
Cade-trust band, `work_counter` a four-band `standing` ladder. Separate the two chains with any
non-`group` block.

**The check.** Gate **"the start choice is read"** walks the game for reads of the declared flags. It
reports `n/a` when nothing is declared — *which is not a pass* — and **fails only on zero**, because
declared-and-never-read is the fake-freedom failure by definition and needs no threshold. It prints
the count rather than judging it: one game is not a distribution, and this skill has already had to
supersede one doctrine built at n = 1.

### 1b. Who she is
Her situation at minute zero, and what she has to lose. Concrete: a job, a debt, a room, a
reputation. The thing that makes the first transgression cost something.

### 2. The appetite that never fills
What she wants, phrased so it can never be finished. "Get revenge on X" finishes. "Be wanted
by people who shouldn't want her" does not.

This is the line that decides whether the game can run forty updates. Test it: *what does
release 41 do?* If you cannot answer, the appetite terminates and needs rewriting.

### 3. What she is becoming — stated as ACCESS
The ascent. For the `female` protagonist declared in §1 — the default, and the case this was
measured on — this is **not money and not status**; it is reach.

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
