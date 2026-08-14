# The Voice — how the game talks to the player about itself

Everything the player reads that **is not the story**: room names, the labels on activity links,
the guidance page, the words under a meter, the text on a door that will not open.

This is a different job from prose. `references/register.md` governs what the player reads **after**
a click. This file governs **everything else** — and its whole requirement is that it be
unambiguous on a first read, by someone who has never seen the game.

> **The game's own voice is plain. It names a thing or an action, and it never performs.**

> Measured failure this exists to prevent: a shipped game whose most-clicked link — the pass-time
> action, ninety minutes, the click that makes every schedule reachable — was labelled **"Sit with
> it"**. The author found out it was unreadable when the player asked what it did. In the same game
> the upstairs hallway was called *The Landing*, the guidance page was empty behind a sidebar entry,
> and seven of eight locked doors gave no reason.

---

## The five rules

### R1 · A label answers "what happens if I click"

Room names and activity links are **navigation**. The register lives in the paragraph the click
produces, never in the button.

| works | does not |
|---|---|
| *Sleep* · *Wash* · *Take a shift* · *Listen through the wall* · *Stand on the landing* | *Sit with it* · *See to it yourself* · *The bench* · *The regulars* · *Someone's in there* |

Same game, same author. The left column loses nothing.

**Location names are UI too.** A name a player cannot resolve is a navigation bug wearing register's
clothes. Keep the setting's voice in every paragraph; make the words on the nav buttons parseable by
anyone. *The Box Room* becomes *The Lodger's Room* and says who and why in two words.

**Exempt, and deliberately so: choice lines inside a scene.** *Stop pretending it's a favour*, *Make
him wait*, *Come down in what you slept in*. These arrive with the scene already on screen, they are
choices in a conversation, and evocative is correct there. Changing them is a regression.

**And the label carries its own cost.** Measured by playing five shipped games — every one that
charges the player states the charge on the button, before the click:

```
Buy coffee (0:02 £2)                  time AND money
Flirt | Promiscuity 1                 which meter it feeds, and the tier
Long Sleep (10:00) Rest >>>>>         duration and magnitude
Take a walk (-0.5 energy)
Take them all out at once | Dance: Impossible      ← the check, and whether you pass it
```

That last one is the shape worth stealing: the label names the skill check **and its current
verdict**, so a player never spends a turn discovering they were never eligible. Failing it still
paid £8.50 — the cost is information, not a wall.

**Money is the one that is gated** (gate 21). A price the player cannot see is a plan they cannot
make, and they are budgeting against a stated deadline. Stamina-type costs are *not* gated: two
corpus games label them and the reference game does not, so a rule there would be invented rather
than measured.

### R2 · Every ascent tier carries a visible ladder

A v2 game has **no mission and no ending**, so the top of the guidance page is not a story spine —
it is the **tiers themselves**. One card per band of each ascent meter, so the page always answers
*what is the next rung, and what raises it.*

Use a stepped trait-band shape: gate each card `gte X` + `lt Y` so exactly one matches, and the
picker swaps it as the meter crosses.

```
nerve  < 15            "Stop covering up around them"      goal -> 15
nerve  >= 15  < 35     "Let it happen and don't move away"  goal -> 35
nerve  >= 35  < 55     "Start it yourself"                  goal -> 55
nerve  >= 55  < 75     "Make it routine"                    goal -> 75
nerve  >= 75           flag rung, or terminal               (see R5)
```

### R3 · Name the feeder, not the number

The sidebar already prints `exposure 22`. **What the player cannot see is which repeatable click
moves it** — and in a game where every gate is a meter, that is the whole of navigation.

Every guidance line names a **place, a person where there is one, and a verb**. *"Flash him at the
depot"* works. *"Prove yourself to Renner"* fails — no place, no clickable action. If the step is
schedule-gated the window rides along: *"Catch him in the garage — weekday evenings."*

Atmosphere belongs in the card's narrative line. The goal label is load-bearing navigation.

### R4 · A wall shows the want; the card shows the route

A locked choice renders greyed. By default **leave `locked_text` off** — the row then shows the
action itself (*"Ask him where the bench went"*), which is a want the player can name, and a want is
what sells the next release. Setting `locked_text` **replaces** that with a reason (*"Not yet — he
still thinks he's getting away with it"*): clearer about the gate, weaker as a door. Prefer the want
unless the gate is genuinely obscure. `engine.md` §15 has the verified render behaviour.

**So a greyed action line is not silent — it states the want.** What it cannot state is the
**route**, and that is R3's job on the guidance card. The two work as a pair: the door advertises,
the card directs.

⚠️ *This rule is written the way it is because the opposite was drafted first, made into a gate, and
fired on seven of eight doors in a real game — every one of which was following `engine.md` §15
correctly. A rule that fails a game for obeying the skill is a bug in the rule. There is
deliberately no gate here; "guidance exists" already covers the real gap.*

### R5 · Nothing retires into silence

The card picker returns the **single highest-priority match** per character. When a ladder's last
card retires with nothing behind it, that character's whole section **disappears from the page** —
at the exact moment the arc closes and they become permanent sandbox content the player can still go
and use.

**v2 owns this harder than a finite game does, because a v2 product never ends.** Every character
tops out eventually. Every arc therefore needs one card that still matches afterwards: a terminal
card, or a goal-less end-of-content card that reads forward (*"his trail is logged; the hunt picks up
in a future update"*).

Never dangle a live goal bullet that cannot flip in this build. That is a fake objective, forever.

---

## Two traps worth knowing before you author a card

- **Quest conditions use a different evaluator from canvas conditions, and do NOT fail open.** Never
  paste `version = "1.0"` onto a card.
- **The sidebar next-row and the guidance page call the identical renderer.** There is no separate
  "sidebar quest" — edit one card and both surfaces move together. A character with no card renders
  a blank next-row.

**R1's cost clause is gated as gate 21** (`a price is on its label`) — a choice that spends the
currency must name the amount. The rest of R1 is not gateable: whether *The bench* is resolvable is a
judgement a parser cannot make.

Field reference and citations: `references/engine.md`.

---

## What is checked, and what is not

| | |
|---|---|
| **Gate 13 · guidance exists** | ≥1 card per declared ascent tier and per declared character |
| **Gate 15 · no chain ends in silence** | every character ladder keeps a card that matches after its last rung |

**R4 has no gate on purpose** — see the warning under it.

**R1 is deliberately not a gate.** *The bench* is a plain noun and clear in context; *Sit with it* is
a plain phrase and is not. No rule separates them mechanically. It stays a human sign-off — read the
location page as a stranger would, before shipping.
