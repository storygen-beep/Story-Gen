# The Voice — how the game talks to the player about itself

Everything the player reads that **is not the story**: room names, the labels on activity links,
the guidance page, the words under a meter, the text on a door that will not open.

This is a different job from prose. `references/register.md` governs what the player reads **after**
a click. This file governs **everything else** — and its whole requirement is that it be
unambiguous on a first read, by someone who has never seen the game.

> **The game's own voice is plain. It names a thing or an action, and it never performs.**

**The loud voice stops at the edge of the story.** The story text is written loud
(`register.md`, "The voice — say it loud"): feelings said, drama pushed, her thoughts on screen.
None of that crosses into labels, buttons, room names or guidance cards. A button reads
*Take a shift*, never *Drag yourself to another miserable shift*.

**One exception, and it runs the other way:** the opening's last screen may carry plain tutorial
sentences in this file's voice — *"You need money. Take shifts at the bar, or find another way."* —
as part of the story text (`the-first-hour.md` F1b). Plain, short, and after the player has met the
people and the problem, never as a lecture on the first screen.

---

## The six rules

### R1 · A label answers "what happens if I click"

Room names and activity links are **navigation**. The register lives in the paragraph the click
produces, never in the button.

| works | does not |
|---|---|
| *Do the laundry* · *Eat breakfast* · *Call your sister* · *Knock on his door* · *Walk to the bus stop* | *Make peace with it* · *Let the evening settle* · *The window seat* · *The usual crowd* · *Something left unsaid* |

Failure kinds: *Make peace with it* = abstract phrase · *The window seat*, *The usual crowd* = bare
noun · *Let the evening settle*, *Something left unsaid* = register-flavoured / literary.

**A button never hides the act** *(LO decided, D11)*. A paid visit to a man's room is labelled as a
visit to his room, never as waiting or being asked; a soft name for a sex act or for sex work is the
failure.

**Location names are UI too.** A name a player cannot resolve is a navigation bug wearing register's
clothes. Keep the setting's voice in every paragraph; make the words on the nav buttons parseable by
anyone. *The Undercroft* becomes *The Basement* and says what the place is in one word anybody owns.

> ⚠️ **When you write a cure, run it through the same instrument that caught the disease** —
> `scripts/genre_words.txt`, one grep. On a button the in-corpus word wins outright.

**The word on a label is `register.md`'s, and it has no gloss.** A button cannot explain itself:
there is no sentence on it to carry one, and the player reads it *before* the prose behind it. So
a room name, a canvas `name` and a room-list choice take the **plain word**, however well the
paragraph downstream glosses it. A sex trait's genre word (*Corruption*) counts as a plain word
*(LO decided, D3b)*. `references/register.md`, "The words the player has to already own" — the label
sub-rule.

**A character's name is navigation too, and it is not a label until the player owns it.** Before a
character has been met, name them by their **role** and where they are — *"your landlady"*,
*"the bartender at the Anchor"*, *"can be found at the docks at night"*. After, the name
alone is enough. `references/the-first-hour.md` F7 owns this and the `named before met` lint lists
the misses.

**Exempt, and deliberately so: a choice's `text` INSIDE a scene** — *Don't answer him*, *Let it
go quiet*, *Say the number first*. These arrive with the scene already on screen, they are choices in
a conversation, and evocative is correct there. Changing them is a regression.

> ⚠️ **The exemption is scoped to a choice's `text`. It has never covered a canvas `name`.** A canvas
> `name` is what renders in the room's activity list — it is a *button on a menu*, judged by the
> table above, not by this paragraph.

**Inside a loop, the label NAMES THE ACT.** The act-menu exits are not navigation and not
atmosphere — they are the ladder, and they are the only thing on the screen that tells the player
what the next click does to her. The field ships them bare and crude at the character's ceiling:

```
in-her-own-hands  Let James finger you · Give James a blowjob · Let James eat you out · Have sex
shady-deals       Tease him · Grope him · Ride him
```

A loop whose exits say *Continue* or *Go on* has thrown away the only readable thing about it. This
does not soften the room-list rule above — a room button stays plain; an act button is inside a
scene the player already chose to be in. `the-surfaces.md` R3b.

**Measured against the field.** 84,009 action link labels across the 27 parseable sandboxes
(`~/Documents/Mopoga_Twine_Sandbox_Research_20260724/gamehtml/`):

```
FIELD           median 3 words          21% are 6 words or longer
```

**Long labels are mostly a symptom, not the disease.** A need
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

**Money is the one that is gated** (gate 21) — **a spend price stays on the button**: about 8 of 15
games print it there. A price the player cannot see is a plan they cannot make, and they are budgeting
against a bill that comes back. **Pay she earns does not go on the button** *(LO decided, D11)*: 0 of
the 4 passing games put it there. It is said in the scene that first offers the work, kept on the
guidance card, and the toast shows it after the click. Spend and income are two rules, kept apart. **And the notation is gated too** — the
amount on the button has to be written in the game's one currency, the same one
`[settings.rent] currency_symbol` prints on the rent card (gate `the price is in one currency`).
`references/the-economy.md` R7 owns this; `engine.md` §33 lists every place the engine prints money
and the four the setting reaches.

Stamina-type costs are *not* gated: two corpus games label them and the reference game does not, so
a rule there would be invented rather than measured.

**Time is the other half of that sentence, and it has its own file.** A label may never promise a
*clock time* — the engine has no absolute-time advance at all, so `Work the counter till one
(2h 30m).` is a promise it cannot keep (gate `the label keeps its time`). A label that spends the
clock should state the *duration*, in one form held across the game, and that duration has to be
the real spend. `references/the-clock.md` C3 and C4 own both, and C4 carries the reason the
duration half is a lint rather than a gate.

### R2 · Every step carries a card line; every ascent tier keeps its card

**A person's cards come from their ladder, one per step, and each says where and when.** The
field's best guidance is one line per character step naming the place and the time; a card keyed to
a meter band tells the player a number, not a place (Round 3 §2.5; being lost is the top complaint,
15.5% of Round 1 comments). Each declared ladder step (`board.characters[].ladder`) names its place
and window, so `scripts/guidance_from_ladder.py <slug>` writes the cards; the author writes the lines.
The tip may be in her voice (*"I wonder what he's into…"*, In Her Own Hands) if the place and time
stay in it. `--ship` reports any step without such a card.

A v2 game has **no mission and no ending**, so Story Goals is the **ascent tiers**: each
keeps one card (the `guidance exists` gate), gated `gte X` + `lt Y` so exactly one matches.

**A card as TOML.** `[[quest_cards]]` is flat and top-level —
**not** `[[quests]]`, which is an unrelated table (`engine.md` §23):

```toml
# An ascent-tier card: no npc_id, so it renders under "Story Goals". A person's
# cards carry npc_id and come from guidance_from_ladder.py.
[[quest_cards]]
priority = 90
text     = "<where she is on this tier, in the fiction — two or three sentences>"
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
NPC card, with a validator warning** (`template_import.py:1157`). A character's section already
renders one card per NPC per render; that is what `priority` is for.

⚠️ **A quest card is NOT a canvas condition and the two forms are different.** Everything else in
this engine reads `flag_key` / `trait_key` + `operator`, inside a `conditions` object carrying
`version = "1.0"`. A card reads **`flag` / `trait` + `op`**, in a bare `when` array, and takes no
`version` at all. Compare against `the-economy.md` R1's ladder — the same author writing the same
idea in the other form.

Writing the canvas form on a card is **caught at build time**, so it is noisy rather than dangerous:
the parser reads neither key, and the validator errors with
`trait condition op must be gte/lte/gt/lt/eq, got ''` (`template_import.py:5934`). A stray
`version` inside a `when` item is simply dropped.

⚠️ **The silent one is `ne`, and it is silent by design.** Cards are evaluated by their own
evaluator — `setup.checkQuestsCondition`, one of the four this engine runs and the only one
without `ne` — whose switch has **no `ne` case and falls through to `return false`**. So the card validator's whitelist deliberately excludes `ne`
(`template_import.py:5927-5934`): widening it would let an author write a routing condition that is
always false, and a card that never matches leaves a blank row rather than an error. Canvas
conditions are a different path and do support it. `engine.md` §37.

⚠️ **An `lt`-only gate is a *window*:** the card vanishes the moment the meter passes it and the row
goes blank. A `gte`-only set matches every card at once and priority silently decides.

### R3 · Name the feeder, not the number

The sidebar already prints `exposure 22`. **What the player cannot see is which repeatable click
moves it** — and in a game where every gate is a meter, that is the whole of navigation.

Every guidance line names a **place, a person where there is one, and a verb**. *"Flash him at the
depot"* works. *"Prove yourself to Tom"* fails — no place, no clickable action. If the step is
schedule-gated the window rides along: *"Catch him in the garage — weekday evenings."*

Atmosphere belongs in the card's narrative line. The goal label is load-bearing navigation.

**A card cannot name a person the player can rename.** `@` tokens resolve in block content, a
location's description and blocked message, choice text and an NPC's role, and nowhere else
(`engine.md` §43); a quest card's `text`, `tip` and goal `label` print the token raw. So on a card,
name a renameable person by role (*"your step dad"*) or by pronoun (*"he's in the kitchen at
six"*). The fixed name is fine for a person the player cannot rename. This is an engine gap, not a
style: cards resolving tokens would remove the rule.

#### R3b · And print the number — this is the defect the genre dies of

Measured 2026-09-03 across 23 female-lead games and 5,663 player comments: **being stuck is the
killer, and it is not grind.** The shape is always the same — content she can see, a requirement
she cannot. The corpus's single most-liked complaint of this kind asks which
level a locked room needs and what is needed to reach it (`den-of-infamy`, 52 likes; paraphrased,
it fails the adults-only rule).

⚠️ **Content and effort do not save you.** `in-her-own-hands` ships **136 passages for one
character** and an **881-word hint page** for him, whose locked state reads *"This hint is locked
until you have completed another task"* — while the condition sitting beside that line names three
exact requirements (a specific conversation, a flag, and exhibitionism ≥ 20). Its players quote the
text back: *"What task do i do to unlock shauns third task"* (13 likes). **A hint system whose
failure state is a shrug is worse than none**, because the player now knows the content is there.

Three attested ways to say it, all from the field:

| | |
|---|---|
| **in fiction** | *"You could ask him about his headquarters if you had a way to approach… **If only you've worked here, hm…**"* — `shady-deals`. Names the want, refuses her, and prints the key, in her own voice |
| **raw** | the button greyed with the number beside it — Cupid's Way, 38 of its 48 greyed buttons outside the Jack/Aaron routes |
| **term by term** | `become-taxi-driver` names **every** unmet term with directions — *"You need more friendship with Lya"*, *"You need a better car (From the city, go to 'Get in the car' and then 'Street Race'…)"* |

**Reach for a trait goal whenever a card gates on a number**, because the engine then prints
`label — 14 / 20` for you with no author involvement (`engine.md` §47.1). A flag goal prints
nothing but its label, and with no label it prints its raw key — which gate
**`a goal says what it wants`** now fails.

### R4 · A wall shows the want; the card shows the route

A locked choice renders greyed, with its action as the label (*"Ask him where the bench went"*) — a
want the player can name *(LO decided, D2)*. **A pure number lock** says the rest itself: the engine
prints the need and her value beside it (`engine.md` §15), so it gets no `locked_text`. **A story
lock** — a flag, or a flag beside a number — gets one short line, which replaces the label, because
the engine's suffix never names the flag.

**So a greyed line states the want and the bar.** What it cannot state is the **route**, and that is
R3's job on the guidance card. The door advertises, the card directs. Gate **a locked door says why**
checks both, and fails a `locked_text` only on a pure number lock, as doubled.

⚠️ **`guidance exists` checks only that a card exists; it never reads what the card says.** Two
checks cover the route: gate **`a goal says what it wants`** (a bullet renders words, not a raw key)
and lint **`the guidance page says nothing`** (a card that renders no requirement at all).

### R5 · Nothing retires into silence

The card picker returns the **single highest-priority match** per character. When a ladder's last
card retires with nothing behind it, that character's whole section **disappears from the page** —
at the exact moment the arc closes and they become permanent sandbox content the player can still go
and use.

**v2 owns this harder than a finite game does, because the game never stalls: when a goal ends, a new one opens.** Every character
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

### R6 · Inside an explicit surface, the button names what she does

R1 governs the buttons in a room. This is R1 inside a scene. It is not a register rule — `register.md` still owns every word that appears *after*
the click; this governs the word on the button.

**The field puts the act on the button.** Across **38,039 clickable labels on explicit screens** in
the corpus, **9.2% name an act** and **1.01% open with `let`**. In Her Own Hands
[JamesDate1SexOptions] puts the act on the button: *"Ride James's dick"*.

⚠️ **The field writes filler too.** **32%** of its explicit-surface
labels are transport (`continue`, `leave`, `next`). Everyone writes filler; this rule is about
the buttons that are *not* filler.

**The rewrite is already written, and it is in the beat.** A permitting label is almost always a
beat whose own prose names the action, with the action then left off the button:

| permitting label | what its beat already says | the button |
|---|---|---|
| *"Let him look at you."* | you stand naked on the bathroom tiles with the towel at your feet and your tits dripping, and he rubs his cock through his trousers and stares at your cunt | **"Don't pick up the towel."** |
| *"Let him take your top off."* | you pull your top off, he squeezes a tit in each hand and sucks a nipple into his mouth | **"Pull your top over your head."** |
| *"Let him bend you over."* | you are bent over the kitchen table, ass up, panties at your knees, and he fucks your cunt with his whole cock | **"Bend over the table."** |
| *"Let him finish in your mouth."* | you kneel with his cock in your mouth, suck until he comes, and swallow every drop of his cum | **"Swallow his cum."** |

⚠️ **Permitting is a legitimate button and the field writes it too** — 1.01%, about one label in a
hundred. In Her Own Hands [JamesDate1FPOptions] sets *"Let James finger you"* beside *"Give James a
blowjob"*. Keep it where **her not moving is the decision**: she holds still, she does not cover up,
she lets it happen and that is the choice. Even there the button names *her* — *"Don't pick up the
towel"*, not *"Let him see."* What the rule refuses is the permitting frame as the house default.

⚠️ **The SHAPE of the surface is not part of this rule and must not become one.** Menu against
single-exit chain was tested against engagement and predicts nothing; both machines ship. The
figures, and two further findings withdrawn from the same study, are under *What is checked, and
what is not*.

Source: `~/Documents/Sex_Loop_Study_20260829/shape.py`, and the label counts in the verb study of
2026-08-28.

---

## Adult wording — a college, never a school

Every character is 18+ and the game says so. **An adult college is allowed** (LO, WS-D6), modelled on
Course of Temptation only: a lecture timetable, grades that move money, professors as a door
(`templates/cards/college.md`). Use university words — lecture, professor, campus, dorm, term, major.

**Banned, as whole words or phrases, anywhere a player reads:** detention · homeroom · prom · "after
school" · "high school" · "middle school" · "junior high" · teen · teenager · schoolgirl · "school
uniform" · "class president" · "grade 9" through "grade 12". *Freshman* and *sophomore* are college
words and are allowed. A whole-word match: "eighteen" is not "teen".

## Two traps worth knowing before you author a card

- **Quest conditions use a different evaluator from canvas conditions, and do NOT fail open.** Never
  paste `version = "1.0"` onto a card.
- **The sidebar next-row and the guidance page call the identical renderer.** There is no separate
  "sidebar quest" — edit one card and both surfaces move together. A character with no card renders
  a blank next-row.

**R1's cost clause is gated as gate 21** (`a price is on its label`) — a choice that spends the
currency must name the amount. The rest of R1 is not gateable: whether *The window seat* is resolvable is
a judgement a parser cannot make.

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

**R4's gate is `a locked door says why`** — see R4.

**R6 has no gate either.** A rate floor on act-words fails games doing it right: the field runs 9.2%,
and a third of its explicit-surface buttons are `continue` or `leave`. The SHAPE of the surface predicts
nothing (−0.13, +0.09 across 16 games). Two further findings were tested and withdrawn, and are not to
be re-proposed: "loops do better" (only two games loop) and "more explicit does better" (+0.18 once
game size is held constant).

**R1 is deliberately not a gate.** *The window seat* is a plain noun and clear in context; *Make
peace with it* is a plain phrase and is not. No rule separates them mechanically, so any threshold on the
noun-only share would be invented, and this skill has demoted two rules for exactly that. The lint
prints the noun-only share of room-list buttons and names the offending labels. Read it; it stays a human sign-off — read the location
page as a stranger would, before shipping.
