# The Want — the one page every release is checked against

## Why this exists

A fantasy specification written once and never read back does nothing. So the rule here is
mechanical, not aspirational:

> **The Want is an input to every release. A release that cannot name which line of the Want
> it serves does not ship.** *(LO decided.)*

Write it before the world. Re-read it before every release. Amend it deliberately and log the
amendment — never let it quietly stop being true.

## The form

Keep it to one page. Longer means vaguer.

### 0. The fantasy, the model to beat, and the promise — settled first

**For a female lead, the premise matters.** In the fifteen core female-lead games of the Great Games
Study (`~/Documents/Great_Games_Study_20260926/`), players name the premise when they say why they stay:
her first year away from her parents, with a bill to send home (Course of Temptation); a girl
embracing new freedom, slowly (In Her Own Hands); *"become rich… Create an Empire of Sin"* (Shady
Deals); a sheltered girl's slow corruption (Cupid's Way). Each game sits in one of four shapes, and each shape has its own engine:

| shape | what she feels | what drives each step |
|---|---|---|
| **fall by need** | alone, broke, and the world prices her body | rent, and a price list for acts |
| **rise by want** | she chose it, for status, freedom or power | her own goal, a rival, a clock |
| **taboo at home** | the house, and who is in the next room | the chance of being walked in on |
| **mystery** | she investigates while something works on her | secrets she buys, clues that pay out |

Pick one, or name the mix, and write in one sentence what the player comes to feel.

**Name the model to beat.** The developers in the study took the premise from their own taste plus one
game, show or film to copy or beat — one wanted another game done better, with a real story and an
end in sight (`zaras-school-life`, paraphrased). No premise came from players or a poll; players chose the order of ideas
the developer already owned (`round4b/ROUND4B_REPORT.md` §1–2).

**Keep the promise alive.** Players praise a game with a goal (*"The goal is to become rich"*, Shady
Deals) and punish one without a spine: *"no driving plot or even a MacGuffin"* (Course of
Temptation), updates that add *"unnecessary sounds"* instead of *"continuing the story"* (Shady
Deals). §1b's hold starts her and §3's meters carry her; **the
goal or the mystery is what pulls the player.** It stays alive after the hold goes quiet, and the
guidance page (`engine.md` §23) carries it. Declare the goal with a date, the mystery with a rough
payout, and the rival.

**Name the moment kinds the game promises.** Five recur in what players remember: her firsts · being
seen · her body as the price for something she needs · taboo at home · a consequence she lives with.

All of it goes under `want` in `v2_state.json` (`references/state.md`). Every key is optional, so a game
written before this section scores exactly as it did.

### 1. Who the player is — settled before she is described

Three things are **declared** here, into `v2_state.json` → `want.player`, before §1b writes a
single line about her.

#### Who is the player? — `female` · `male` · `picked`

⚠️ **The default is `female` and the evidence is FOR it, not merely permissive.** Across ~22,600
corpus comments: **49 asking for a female lead (364 likes) against 11 opposed (124 likes)**, and the
opposed get argued down in their own threads. The top-30 count — 20 male, 6 picked, 4 female — is a
**supply** figure; a player in that corpus did the arithmetic himself at *"44 games with the Female
Protagonist tag and 100 with the Male Protagonist tag."* Do not read `4 of 30` as a verdict. The
sharpest practical argument is also a player's: *"as a guy I like to play female mc since we can get
to the spicy part quicker and not grind around like in male mc games."*

#### Written character, or blank slate? — `written` · `blank`

Field: **19 blank to 10 written**, and blank carries **80.4%** of the top-30's engagement. `written` is defensible — it is
what real-porn media and a named cast pull toward — but an undeclared default is not a decision.

#### What does the player choose about her at minute zero?

**The choosing matters, and so does the premise.** On the male-heavy top 30, `freedom` is the largest
single thing a game is loved for (25.9% of reason (1), weighted by comment count); its #1 game's #1
reason is *"You can be whatever you want."* For a female lead, §0 holds as well. Give her both.

**The rule: a memory, not a slider** (`~/Documents/Female_PC_Craft_Study_20260823/findings_A_want.md:93`).
Course of Temptation never shows a stat screen; it asks about her past and initialises
thirteen skills the player never sees. Ask something the scene is **already asking**, and set a flag
from the answer.

⚠️ **ADDITIVE ONLY WHEN RETROFITTING.** Each original rung keeps every number it had and gains
`<flag> is_false`, so it and the rung the start choice adds are mutually exclusive, no door closes,
and a save made before the choice shipped carries no flag and reads exactly what it read yesterday. **A start choice that takes
content away from an existing save is the version players punish.**

⚠️ **THAT IS A SAVE-SAFETY RULE, NOT A DESIGN RULE, AND THE SCOPE WAS ADDED 2026-08-28.** Read as
*"never close a door"* it contradicts the field, and the contradiction is measurable. `the-company`'s
single most-liked reason for love is choice-consequence ownership — *"it only does that if you allow
it to"* (39 likes), *"That's only because of your choices"* (27) — and it hard-locks a dom/sub route.
Its single most avoidable complaint is that the lock is **silent**: *"If a choice locks you into a
sub route, tell me that."*

So in a game being designed, doors may close. **The rule is that they close out loud.** The corpus's
best example is `become-taxi-driver`, whose gate is five terms —
`$lya.friend >= 130 and $mia.friend >= 95 and $neptuno.friend >= 90 and $car.fase >= 2 and $car.body >= 3`
— and whose refusal text names **every unmet term separately, with directions**: *"You need more
friendship with Lya"*, *"You need a better car (From the city, go to 'Get in the car' and then
'Street Race'…)"*. `the-voice.md` owns that half; `the-economy.md` R1b owns the asset the lock hangs
on. Measured in `~/Documents/Accumulation_Study_20260828/` §4.

⚠️ **THE PLACEMENT TRAP, AND IT FAILS SILENTLY.** Adjacent `[group]` blocks merge into ONE if/elseif
chain (`v2.py:14637`) and first match wins. Drop a past-ladder next to a surface's existing ladder and
**that ladder becomes unreachable for every player carrying a past** — no error, no build warning, the
prose simply stops appearing. Separate the two chains with any
non-`group` block.

**The check.** Gate **"the start choice is read"** walks the game for reads of the declared flags. It
reports `n/a` when nothing is declared — *which is not a pass* — and **fails only on zero**, because
declared-and-never-read is the fake-freedom failure by definition and needs no threshold. It prints
the count rather than judging it: one game is not a distribution, and this skill has already had to
supersede one doctrine built at n = 1.

#### The other mechanism — the creation screen, and what it is for

Everything above is the **diegetic** question: ask what the scene already asks, set a flag, gate
content on it. The engine also ships a literal creation screen —
`[[player.customization_fields]]`, three field types (`text`, `select`, `image_select`) plus
`sets_portrait` — and until 2026-08-29 the skill's only instruction about it was *"set it `false`
unless you are actually shipping the fields."*

Measured against the field (13 top-30 games with a creation step, 22,614 comments; instruments in
`~/Documents/Customization_Study_20260829/`):

**W1 · If you ask, print it back.** The field reads every created field a median of **four** times
after creation, and the median game leaves **none** of them unread. That is the whole rule; there is nothing subtler under it.

**W2 · The payload is a word, not a gate.** Only **1.8%** of the field's reads of a created value
are conditions. **82%** of its creation controls are free text and **0%** are numeric — and a typed
value cannot be gated on, only printed. So do not design branches on what she picked. Our engine's
condition types cannot read the `$player.<field_id>` namespace, and on this evidence **they should
not learn to** — the gap is worth 1.8% of what the mechanism is for.

⚠️ **This corroborates "a memory, not a slider" from a new direction.** The corpus's creation
screens carry **zero** stat fields. Nobody out there builds the stat screen this section already
tells you not to build.

**W3 · Three fields, not thirty.** Field median is **3**. **No threshold, deliberately.** The largest creation screen in the corpus is 59 fields and
it is the only one anyone asked to skip, at one comment and one like. That is n = 1 and a ceiling
read off it would be invented, per the P0 refusal.

**W4 · The distinctive axis is the cast, not the player — and it is already built.** The field's
creation screens ask the player to fill in each person's relation to her. The player names the household and the kinship inside it, which in this
genre is the setting. We ship this already: `npcs[].relationship_options` renders a picker on the
same screen, the pick lands on the NPC, the cast page prints it, and prose has a token for it —
**`@<npc>.rel`**. See `engine.md` for the field
reference.

**W5 · Refusing costs nothing.** Half the corpus ships no creation step at all, including the
second-ranked game. Across 22,614 comments the entire subject runs at **0.12%** — against lostness
at 4.7% and grind at 0.9%. Six comments ask for more customization; two ask for a skip button.

⚠️ **This is NOT `the-phone.md` P1's refusal rule, and must not be written as one.** P1 could say
*"most games should not have a phone"* because the corpus returned a verdict — 24 likes to 0.
**Here there is no verdict in either direction.** Nobody is asking for a creation screen and nobody
resents one. So the rule is conditional, not prohibitive: **have one or don't; if you have one,
read it back.**

**The two syntaxes, because one of them is easy to miss.** A field's value lands at
`$player.<field_id>` — or `$player.name` for the reserved id `name` — and the house form for
reading it in prose is the `@` token: `@player` for her name, `@player.<field_id>` for anything
else. Both work. **The token is what authors actually type**, and two separate passes of this
study's own instrument reported a false zero by knowing only the raw form.

**The check.** Gate **"what she picks is read"** counts both syntaxes across the built game and
**fails only on zero**, the same shape as the start-choice gate above. A game declaring no
customization reports `n/a`, which is not a pass. ⚠️ **`sets_portrait = true` counts as a read** —
an `image_select` field writes `$player.portrait`, which the stats page renders, so a gate without
that exemption fails every game using the feature correctly.

### 1b. Who she is
Her situation at minute zero, and what she has to lose. Concrete: a job, a debt, a room, a
reputation. The thing that makes the first transgression cost something.

> **Prefer a hold with a face and a date over a situation.** *"She has no money"* is a mood;
> *"Friday, $260, and the landlord counts it at the desk"* is a machine. That half is right and it is the
> half worth keeping — a hold of any kind needs somebody who notices and a moment when it comes due.

⚠️ **A bill is one hold of at least nine,** and the field this skill is written for does not reach for it
first.

**Measured 2026-09-04, `~/Documents/Female_Hold_Study_20260904/`** — 23 female-lead sandboxes read
in source, the hold hand-read out of each opening with the settling line recorded in `verdicts.md`:

```
ambition      5    she picked the thing herself and the world charges for it
bill          4    a recurring money demand                (+1 with DoL as control = 5 of 24)
order         3    an institution, a sentence or a mission
body          3    what she is turning into
subsistence   3    the place will not feed her
appetite      2    no hold at all, and one of the two says so on purpose
job · erosion · displacement    1 each
```

**The bill is fourth by frequency in the field and was first by position in this file.** Independently,
`probe_a.py` looks for the MECHANISM rather than the vocabulary — an obligation variable written and
read in three or more conditions — and finds it in **6 of 23 (26%)**, against R3's **14 of 19 (74%)**
on the male-heavy corpus, using the same regexes. One of the six is `shady-deals`, where reading it
settles that **she is the creditor**: a money system is not a money hold.

> **And the obligation is not what carries the game anyway.** `the-economy.md` R3d measured DoL's
> `$rent*` at **57 of 91,814** condition sites against **1,336** on the tier rungs, and both top games
> cap the ratchet by hand. Whatever hold you pick, §3's meters are what still gate content at
> release 41. Pick the hold that starts her; do not expect it to carry her.

**Declare the shape** as `want.hold_kind` in `v2_state.json` (`references/state.md`), and if a person
enforces it, `want.hold_collector`. The lint **`the collector is also the target`** reads both.

⚠️ **Then read §4b before you write the hold.** It says, measured 36 scenes to 5, that she wants it
and goes and gets it — so **design what stops her, not a reason for every act.** A hold chosen as a
justification machine contradicts §4b, and §4b is the one with the numbers. `the-economy.md` **R3–R3d**
still own the money mechanism for the games that pick `bill`.

### 2. The appetite — where she lands, not where she starts
What she wants, phrased so it can never be finished. "Get revenge on X" finishes. "Be wanted
by people who shouldn't want her" does not.

**The appetite is not a content schedule.** What decides whether release 41 has anything in it is the
**meters** — §3 — and the gap is not close:

| in `degrees-of-lewdity` | condition sites |
|---|---|
| the rent — the obligation the whole opening runs on | **57** of 91,814, and they are *is it due* / *can she pay* |
| the tier rungs — `<<promiscuity3>>`, `<<exhibitionism5>>` | **1,336** |

So the four parts of this page divide the game between them, and each does one job:

- **§0 — the promise pulls the player.** The goal or the mystery stays alive after the hold goes quiet.
- **§1b — the hold starts her.** It has to be there in week one, when nothing else is.
- **§3 — the meters carry her.** They are what still gates content at release 41.
- **§2 — the appetite is what she arrives at.** The hold goes quiet (`the-economy.md` R3d for the
  `bill` case) and the act does not change; the *reason* does.

That last sentence is **§4's Transformation charge stated mechanically** — see it, and write the two
to agree.

⚠️ **Write it as a destination and the field agrees; write it as her opening position and you have
copied the weakest example in the corpus.** Of the four female-lead games read in source, three open
on a bill, a threat or an erosion. The one that opens on her own appetite is the one measured as
*"an appetite with no obstacle at all — the weakest want of the four"*
(`~/Documents/Female_PC_Craft_Study_20260823/findings_A_want.md`).

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

> **The release-41 test lives here.** *What does release 41 add?* It is asked of the **tiers**, not
> of the appetite, because the tiers are what still gate content that far out — 1,336 rung-gated
> sites in the reference game against 57 conditions that read its rent (§2). If you cannot answer
> it against a named tier, the tier is decorative and release 41 has nothing to hang on.

### 4. The charge
One of — or a deliberate combination of:

- **Reversal** — someone with power over her loses it, or gains more of it than they should
- **Taboo** — the relationship itself is the transgression
- **Transformation** — she becomes something she would not have recognised

Name which. "It's hot" is not a charge; it is the absence of one.

#### 4a. The person who holds the obligation is not automatically the person she fucks

Added 2026-09-04. It had never been written down anywhere in this skill, and its absence is what
produced ten pitches in a row where a man collects money and the sex is how the money gets settled.

**Nothing here teaches that.** Grepping `references/`, `SKILL.md` and `templates/` for
`prostitut|sex work|escort|paid sex|sex for money|instead of money` returns **zero hits**. It is
emergent: §1b used to ask for a collector, §4's first charge is *"someone with power over her"* — the
collector already is that — and `the-surfaces.md` requires the repeatable surface be explicit. Three
defensible rules compose into one architecture, and nobody chose it.

**Measured, `probe_c.py`.** In every field game with a bill and a named collector, the share of the
game's explicit passages that name him:

```
life-at-university   2.1%      course-of-temptation   0.4%
life-choices         3.8%      degrees-of-lewdity     1.4%     (the first and last: numbers only)
in-her-own-hands     —  no person collects it; the rent is a system
```

And the scale check is the finding (`life-at-university`, numbers only; it fails the adults-only
rule):

```
life-at-university, 238 explicit passages
   uncle       14   5.9%
   Professor   12   5.0%
   Mrs. Love    5   2.1%   <- the collector
```

**The collector carries fewer explicit passages than two other people**, and the reference game
shows the same split (its collector 1.4%, numbers only).

> **The field builds the hold and the porn as two separate systems.** Write the collector as a real
> character who can want her, but the obligation is not the pipe the porn comes down. If settling
> the hold *is* the repeatable surface, the game has one idea, and the ceiling on it is however many
> ways she can pay.

⚠️ **This is a default, not a ban.** Collector-as-target is a legitimate design and one of the
biggest games in the field ships it deliberately. The defect is doing it *without noticing*, in
every game, because the fields were laid out in that order. The check is a **lint** for exactly that
reason — `the collector is also the target` prints his share and never fails a build.

#### 4b. The default is that she wants it and goes and gets it

Added 2026-09-03, because the opposite was assumed and it is measurably wrong. Classifying every
act scene in `zaras-school-life` (numbers only; it fails the adults-only rule) by whether she
states a plain want or gives herself a practical reason:

```
DIRECT — "she just wants him"      36 scenes    median gate corruption 25    lowest 5
EXCUSE — a practical reason         5 scenes    median gate corruption 60    highest 80
```

**Seven to one in favour of direct, and direct starts at 5** — no problem to solve, no
appointment, no justification. The passing games say it the
same way: *"I really want this, Bobby. Please don't stop"* (In Her Own Hands).

So do not design a reason for every act. **Design what stops her**, and let the meter be how far
she will go (`the-meters.md` W1b).

⚠️ **Deniability is a late tool for the target she cannot face.** The five excuse-shaped scenes —
a slipped top, a door left open — gate at **45–80**, every one behind that game's hardest unlock. She notices half a second too late, every time, which lets
her escalate without deciding to and lets the player enjoy it without her becoming a cartoon.

**Use it for the one or two people the charge makes unapproachable — under Reversal, the person
with power over her — and use it late.** Spending it on the ordinary cast inverts the ladder: it
makes the easy targets read as harder than the forbidden one.

⚠️ **The elaborate route is one shape among several, not the house style.** Problem → practical
offer → her own justification → appointment → preparation → the preparation is seen — that is
one quest in that game, and it is how you build the *hard* approach. Reaching for it by default is what the
author of this section did first, and the game it was read from does the opposite 36 times out
of 41.

### 5. The world
Root it outdoors, in more than one zone — `the-map.md` R0 — unless the fantasy is taboo at home,
where the house is the point.

### 6. Why *this* person
One line per character. Not their role in a plot — **why she wants them, or why being wanted
by them lands.**

> Measured, and the strongest single finding in ~11,000 player comments: praise for the porn
> itself scores lowest of every theme, while performer identity and character attachment score
> highest. One game swapped its performers and its three most-liked comments were the revolt;
> another recast and died. **The person is the product.**

A character with no line here is a character with no reason to exist. Cut them or write it.

**The companion** — a friend one step ahead who leads her, or one step behind whom she leads. In Her
Own Hands' Abby [AbbyDBDareStart1]: *"I'm here to push you out of the nest, baby bird."* Cupid's
Way's Jasmin sets up her dating app [Download Finder]. Record as `want.companion`.

**The pressure-man** — one man whose demand drives her choices release after release. The no has a
stated price and there is an opt-out somewhere (`the-release.md`, the pressure type). Cupid's Way's
Mr. Brown: *"Send it and I'll remove the penalty."* Shady Deals' Romano, over a casino debt:
*"you'll have to pay me back... one way or another."* Record as `want.pressure`.

**Her face** — one performer or one look, kept across the game. In Her Own Hands keeps one woman
through four profile images that change with her inhibition [Statistics]; a Shady Deals player
faults its *"ZERO actress consistency"* (F95, second-hand). Record as `want.face`; build it with
`[player_portrait]` (`engine.md` §34b).

### 7. Register
Three declarations, made once:

- **`narration_person`** — recommend `second`. It is per-game and immutable after the first
  release ships, because changing it rewrites every line. (The measured exemplar for a female
  protagonist is second person.)
- **Crude-vocabulary ceiling** — the actual words that may appear, per character and per tier.
  Write the words down. A ceiling described abstractly gets written around.
- **Where the crude register lives** — and the answer is **the repeatable surfaces**.

## The test before you leave this file

Answer these five out loud. If any answer is soft, the Want is not done.

1. What does release 41 add? *(ask it of a named §3 tier. If no tier can answer it, the tier is
   decorative — the appetite was never what scheduled content)*
2. What can she reach at the top that she cannot reach at the bottom? *(the ascent)*
3. Which character would a player miss if you deleted them, and why? *(the product)*
4. Which repeatable surface carries the crudest writing in the game? *(the register, in the
   right place)*
5. What is the promise, and which release pays the mystery's next clue? Which moment kinds does this
   game keep delivering? *(§0)*

Then run the last, which is not a judgement call:

```
python3 scripts/gates.py --words games/<slug>/WANT.md
```

**Read the list. It is a list and never a score** — a word on it is not automatically wrong, and
the question is only whether a player arrives already holding it.

**Why here and not at the end.** The same check runs against a built game, and that is one phase
too late: by then every noun is set into a room name, a button label and the prose behind it, and
changing one means renaming things. **The Want is where a game's nouns get chosen** — its rooms,
its work, its objects and its meters all come out of this page.

Run it again on the board's location names before leaving that phase too. A word the player
cannot decode is undecodable on a button.

## Then

Create `games/<slug>/v2_state.json` with `phase = "want"` and the Want recorded, per
`references/state.md`. Move to `references/the-board.md`.
