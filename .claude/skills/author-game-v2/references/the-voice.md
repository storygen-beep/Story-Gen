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
anyone. *The Box Room* becomes *The Back Room* and says where it is in two words anybody owns.

> ⚠️ **This example has now been wrong twice, in opposite directions, and both are worth keeping.**
> It read *The Lodger's Room* until 2026-08-22 — `lodger` is used by **zero** of the 27 field
> games, and `steam` and `off_season` both shipped a location copied from this line. The cure
> written that day was *The Tenant's Room*, and **`tenant` is under the corpus bar too.**
>
> It is not a second `lodger` — the plural `tenants` **is** in-corpus, so `tenant` is standard
> English that happens to fall under a frequency threshold, and it stays everywhere this skill
> uses it to describe a *role* to an author (`the-board.md`, `the-map.md`, `state.md`). But a room
> name is a **button**, and on a button the in-corpus word wins outright. Off Season had already
> got there on its own: it shipped **The Back Room**, and `back` and `room` are both in-corpus.
>
> The lesson is not about these two words. **When you write a cure, run it through the same
> instrument that caught the disease** — `scripts/genre_words.txt`, one grep. Neither replacement
> here was ever checked, and the file taught a defect it had just finished diagnosing.

**The word on a label is `register.md`'s, and it has no gloss.** A button cannot explain itself:
there is no sentence on it to carry one, and the player reads it *before* the prose behind it. So
a room name, a canvas `name` and a room-list choice take the **plain word**, however well the
paragraph downstream glosses it. `references/register.md`, "The words the player has to already
own" — the label sub-rule.

**A character's name is navigation too, and it is not a label until the player owns it.** Before a
character has been met, name them by their **role** and where they are — *"your closest friend,
Felix Morin"*, *"a student at your school"*, *"can be found at the docks at night"*. After, the name
alone is enough. `references/the-first-hour.md` F7 owns this and the `named before met` lint lists
the misses.

**Exempt, and deliberately so: a choice's `text` INSIDE a scene** — *Don't answer him*, *Let it
go quiet*, *Say the number first*. These arrive with the scene already on screen, they are choices in
a conversation, and evocative is correct there. Changing them is a regression.

> ⚠️ **The exemption is scoped to a choice's `text`. It has never covered a canvas `name`.** A canvas
> `name` is what renders in the room's activity list — it is a *button on a menu*, judged by the
> table above, not by this paragraph.
>
> **This distinction leaked, and it is why LO found the defect.** The three examples printed here
> until 2026-08-18 were *Stop pretending it's a favour*, *Make him wait* and *Come down in what you
> slept in* — and **every one of them exists in `back_home` twice**:
>
> ```
> back_home/5_scenes.toml:983    text = "Come down in what you slept in."   ← a choice. exempt. correct.
> back_home/5_scenes.toml:1093   name = "Come down in what you slept in"    ← a CANVAS NAME = a button
> ```
>
> The exemption was written off the choice and read off the button, and the pattern was copied into
> `the_allowance` as a top-level room-list entry. An example outranks the rule beside it
> (`SKILL.md`), so the three above were replaced with strings that can only ever be choices.

**Inside a loop, the label NAMES THE ACT.** The act-menu exits are not navigation and not
atmosphere — they are the ladder, and they are the only thing on the screen that tells the player
what the next click does to her. The field ships them bare and crude at the character's ceiling:

```
destroyer   Keep blowing · Pound her ass · Pound her pussy · Cum · Go back
vesper      Keep him in your mouth · Turn over — give him your ass · Let him finish inside you
corpo-life  Kiss Her · Handjob · Cum in mouth · Fuck Her
```

A loop whose exits say *Continue* or *Go on* has thrown away the only readable thing about it. This
does not soften the room-list rule above — a room button stays plain; an act button is inside a
scene the player already chose to be in. `the-surfaces.md` R3b.

**Measured against the field.** 84,009 action link labels across the 27 parseable sandboxes
(`~/Documents/Mopoga_Twine_Sandbox_Research_20260724/gamehtml/`):

```
FIELD           median 3 words          21% are 6 words or longer
```

> ⚠️ **The long share read 10% until 2026-08-24 and was never reproducible.** Rebuilt on the
> original 25 games the label count reproduces to 0.29% and the median reproduces exactly at 3, but
> the share at six-plus words is **16%** — and no filter yields 10% at a median of 3. The median is
> the number this rule actually leans on, and it has not moved. `findings_RECHECK.md` §1.

Ours, and the drift tracks build date:

```
late_shifts   v1   3w /  7%        back_home      v2   4.5w / 35%
the_inherit.  v1   3w / 10%        the_allowance  v2   5w   / 36%
last_call     v1   4w / 15%        steam          v2   5w   / 47%
vesper        v1   4w / 17%        forty_miles    v2   6w   / 50%
                                   seventh_day    v2   6w   / 57%
```

**Long labels are mostly a symptom, not the disease.** Our own need-shaped canvases are already short
in the same files — `Wash up` · `Power down` · `Charge up` · `Drill` · `Change` · `Wash`. A need
names itself in one or two words; a described fiddle with a noun needs seven (*"Get the washing in
off the airer"*). Fix the room's list per `the-surfaces.md` R2 and most of this corrects itself.

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
make, and they are budgeting against a stated deadline. **And the notation is gated too** — the
amount on the button has to be written in the game's one currency, the same one
`[settings.rent] currency_symbol` prints on the rent card (gate `the price is in one currency`).
A shipped game put `Feed the meter (GBP 3)` on a button, *"Three pounds"* in the paragraph behind
it and `$90` on the rent card, because nothing had been declared. `references/the-economy.md` R7
owns this; `engine.md` §33 lists every place the engine prints money and the four the setting
reaches.

> ⚠️ **That button carried TWO defects and this line only ever saw one.** `meter` is a false
> friend — a coin-fed prepayment box here, a stat bar to most players, and the game renders four
> stat bars in its own sidebar. The currency pass quoted the button *in order to fix it*, fixed the
> notation, and left the unreadable word sitting in the quote, where it stayed until LO clicked it
> in the built game and asked what it meant.
>
> `SKILL.md`'s **"an example outranks every rule beside it"**, in its sharpest form yet: not an
> example that taught a defect by accident, but one held up *as* a defect, with a second defect
> inside it that survived the edit. **When you quote a broken line, read the whole line.** Stamina-type costs are *not* gated: two
corpus games label them and the reference game does not, so a rule there would be invented rather
than measured.

**Time is the other half of that sentence, and it has its own file.** A label may never promise a
*clock time* — the engine has no absolute-time advance at all, so `Work the counter till one
(2h 30m).` is a promise it cannot keep (gate `the label keeps its time`). A label that spends the
clock should state the *duration*, in one form held across the game, and that duration has to be
the real spend. `references/the-clock.md` C3 and C4 own both, and C4 carries the reason the
duration half is a lint rather than a gate.

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

**That ladder as TOML, which this file has never shown.** `[[quest_cards]]` is flat and top-level —
**not** `[[quests]]`, which is an unrelated table (`engine.md` §23):

```toml
# One rung of an ascent ladder. A card with npc_id renders in that character's
# section; a card without one renders under "Story Goals".
[[quest_cards]]
priority = 90
npc_id   = "<npc_id>"
text     = "<where she is on this ladder, in the fiction — two or three sentences>"
tip      = "<the route: a PLACE, a PERSON where there is one, and a VERB. R3.>"
when     = [ { trait = "<meter>", subject = "player", op = "gte", value = 15 },
             { trait = "<meter>", subject = "player", op = "lt",  value = 35 } ]
goals    = [ { trait = "<meter>", subject = "player", op = "gte", value = 35, label = "<the next rung, named as an action at a place>" } ]
```

⚠️ **An inline table may not span lines.** The `when` array above wraps because an *array* can; each
`{ … }` inside it is whole on its own line. Break one of those across two lines and the build stops
at a TOML parse error.

⚠️ **`group` and `npc_id` do not go together.** `group` collapses several **Story Goal** cards to
one — the crisis variant of a goal and its ordinary form, sharing a slot — and is **ignored on an
NPC card, with a validator warning** (`template_import.py:1105`). A character's section already
renders one card per NPC per render; that is what `priority` is for.

⚠️ **A quest card is NOT a canvas condition and the two forms are different.** Everything else in
this engine reads `flag_key` / `trait_key` + `operator`, inside a `conditions` object carrying
`version = "1.0"`. A card reads **`flag` / `trait` + `op`**, in a bare `when` array, and takes no
`version` at all. Compare against `the-economy.md` R1's ladder — the same author writing the same
idea in the other form.

Writing the canvas form on a card is **caught at build time**, so it is noisy rather than dangerous:
the parser reads neither key, and the validator errors with
`trait condition op must be gte/lte/gt/lt/eq, got ''` (`template_import.py:5509`). A stray
`version` inside a `when` item is simply dropped.

⚠️ **The silent one is `ne`, and it is silent by design.** Cards are evaluated by a *third*
evaluator — `setup.checkQuestsCondition` — whose switch has **no `ne` case and falls through to
`return false`**. So the card validator's whitelist deliberately excludes `ne`
(`template_import.py:5501-5509`): widening it would let an author write a routing condition that is
always false, and a card that never matches leaves a blank row rather than an error. Canvas
conditions are a different path and do support it. `engine.md` §37.

⚠️ **`gte X` + `lt Y` on every rung, so exactly one matches.** An `lt`-only gate is a *window*: the
card vanishes the moment the meter passes it and the character's row goes blank. A `gte`-only
ladder matches every rung at once and the picker's priority order silently decides the game.

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

**The card that catches them, at the bottom of every ladder:**

```toml
[[quest_cards]]
priority      = 10                            # lowest — every live rung outranks it
npc_id        = "<npc_id>"
terminal      = true
terminal_text = "<what ENDED — an arc, or this build. The default says 'Arc complete'.>"
text          = "<where they stand now, written forward: still here, still usable>"
when          = [ { trait = "<meter>", subject = "player", op = "gte", value = 75 } ]
# no goals: a terminal card is not climbing. See the warning below.
```

⚠️ **`terminal = true` is the whole mechanism, and leaving it off is how a finished arc ends up
looking live.** `renderQuestsGoalBlock` emits exactly one frame per card, in order:
✓ terminal → 🔓 `ready_canvas` → 🎯 unmet goals. A **goal-less, non-terminal** card matches all
three tests and draws **none** of them — so the card still renders its `text` and `tip` and reads as
an objective with nothing ticked, forever. `engine.md` §23.

⚠️ **`terminal_text` needs `terminal` set or the string is dead** (the validator warns). It exists
because a finished *arc* and a finished *build* are different endings and the default label can only
say the first. In a **v0.1 nothing is closed** — every track stops at a build boundary — so the
one-`terminal_text`-per-game guidance written from a finished build is the wrong rule there, and
following it produces the worse outcome.

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
| **Lint · noun-only buttons** | the share of room-list labels opening on a determiner and naming no verb |
| **Lint · label length** | median words per label and the share at 6+, with the field's 3 / 10% printed alongside |
| **Lint · she permits or she acts** | the share of choices opening `let`, overall and inside sex loops, against the field's 1.01%. R6 |

**R4 has no gate on purpose** — see the warning under it.

**R6 has no gate either, and two things were tested and refused before it was written.** A rate
floor on act-words cannot be defended: the field runs 9.2% and a third of its own explicit-surface
buttons are `continue` or `leave`, so any threshold between those fails games that are doing it
right. And the SHAPE of the surface — menu against single-exit chain — was correlated with
engagement across 16 games and predicts nothing (−0.13 and +0.09). Two further findings from the
same study were withdrawn rather than shipped: that loops folding back on themselves do better
(+0.52, still +0.34 controlling for size — but **only two games in the corpus loop at all**, and the
two most-engaged loop 7% and 3%, so a rank correlation was being carried by two points), and that
more explicit content does better (+0.61, but **+0.18** once total game size is held constant, which
means it was mostly "bigger games collect more comments"). Recorded so neither is re-proposed.

**R1 is deliberately not a gate, and the numbers say why.** *The bench* is a plain noun and clear in
context; *Sit with it* is a plain phrase and is not. No rule separates them mechanically. Measured,
the noun-only share of room-list buttons is:

```
last_call 0%  ·  late_shifts 0%  ·  the_allowance 0%
vesper 24%  ·  back_home 32%  ·  the_inheritance 38%
seventh_day 84%  ·  forty_miles 87%  ·  steam 92%
```

**Three shipped games sit at 0%, so the target is reachable** — but any threshold in the gap between
38% and 84% would be invented, and this skill has demoted two rules for exactly that. The lint prints
the percentage and names the offending labels. Read it; it stays a human sign-off — read the location
page as a stranger would, before shipping.
