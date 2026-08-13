# author-game-v2 — changelog

The skill-level ledger. Every edit to any file in this skill gets a dated bullet here in the
same turn: what changed, why, and how it was verified.

---

## 2026-08-14 — **The field's most consistent shape was in a study file the authoring path never reads**

`references/the-surfaces.md` gains **R2b · every choice hangs off a named object in the prose**, with
a worked comparison at the top of the file, and `SKILL.md`'s surfaces callout now names it inline.

**Why this was urgent.** Study 5 found this in three of five played games independently, and called
it *"the single most consistent shape in the corpus"* — but it lived only in `DOCTRINE_GAPS.md`,
which this skill's own inventory calls **"the trail, not the doctrine."** Nothing on the authoring
path pointed at it. An author following the dispatch table would have produced correct *counts* with
no anchoring: eight choices in a flat list rather than eight choices under four sentences. That is
precisely the difference between the failure case's front desk and the reference game's bedroom, so
the rule that best predicts whether a location reads as a room was unreachable from the phase that
builds locations.

Found while sanity-checking whether a **bare** prompt — `/author-game-v2 new game, female
protagonist, give me a few ideas` — would be a fair test of the skill. It would not have been: the
skill could not have taught the rule, and a loaded prompt would have tested the operator instead.

**Also moved:** study 5's play-measured figure for how much a location offers — **median 3 things to
do, max 6**, counting only decisions and excluding onward travel and standing affordances. It now
sits beside the existing 18-sandbox parse figures with a note reconciling them, since the two count
different things and disagree by a factor of three otherwise.

R2b is **not gated and says so**, with the reason: a parser can see that a choice exists and that a
paragraph exists, but not whether the paragraph names the thing the choice acts on. It is flagged in
the file's checked-table as the highest-value ungated rule there.

**No gate, no threshold, no code changed. Scores untouched:** steam 17/19, back_home 13/18.

---

## 2026-08-14 — **Gate 21 graduates study 5's one gateable rule — and finds two economy gates reading the wrong channel**

Study 5 named exactly one output as gateable: *a choice with a declared cost whose label omits it is
checkable against the TOML.* Graduating it turned up two pre-existing defects in the economy gates
that had nothing to do with study 5, and both were silently wrong on a shipped game.

**`scripts/gates.py` — gate 21, `a price is on its label`.** Every choice that spends the currency
must name the amount in its text. Measured by playing: every corpus game that charges money puts the
price on the button, and the player is budgeting against a stated deadline. **Money only** —
stamina-type costs are counted in the headline and never judged, because two corpus games label them
and the reference game does not, and a rule there would be an invented threshold, which is the
failure that demoted R5/R6. Fires on vesper: **3 of 7 coin choices hide their price**, all three
purchases (`Pay the toll.` at 5, `Buy a weapon` at 40, `Buy infiltration gear` at 30) while four
others name it — the same game contradicting itself is the tell.

**Bug 1 — a `costs` block is a gate, and gate 16 could not see it.** The engine refuses a choice the
player cannot afford (`v2.py:12556`), but `reads` is built from *conditions* only (`gates.py:349`).
A game that prices its choices rather than condition-gating them read as *"nothing in the game reads
the currency"*. Vesper spends coin on seven choices and scored **zero**. Gate 16 now counts either
channel and says which.

**Bug 2 — the currency inference took the first name match, and vesper has two real currencies.**
`money` is Credits, company-visible; `coin` is hers and hidden, *"the company can't see"*. `money`
is used once, `coin` eighteen times — and the gates were judging `money`. Worse, `CURRENCY_HINT` had
no entry for `coin` at all, so a currency by that name was invisible outright. **This is the same bug
class already fixed once in the corpus extractor**, where a decoy `randomMoney` beat the real
currency on name alone; the fix never came back to `gates.py`. Selection is now by usage, the hint
list gained `coin|gold`, and gate 16 prints the chosen currency and its runners-up so a wrong guess
is visible rather than silent. Declaring `board.economy.currency` skips the guess entirely.

**Doctrine.** `references/the-voice.md` R1 gains the cost clause (with the shape worth stealing —
DoL's *"Take them all out at once | Dance: Impossible"*, a label that states the check **and whether
you currently pass it**, where failing still paid). `references/the-economy.md` gains gate 21 in its
checked table plus a warning section on both bugs. `DOCTRINE_GAPS.md` study 5 R3 marked graduated —
and corrected: it extends **item 2** (interface text), which was already closed on 8-12. The plan
that commissioned the study called the label rule "Tier 1 item 4"; item 4 is scene prose.

**Verified.** steam **17/19** and back_home **13/18**, both unchanged. Vesper **6/17 → 6/18** — the
price gate now judges instead of reading n/a, and its economy gates moved from the wrong currency to
the right one: `money gates something` FAIL→PASS on the costs fix, and the new gate fails on three
real hidden prices.

---

## 2026-08-13 — **Study 5: the field, played rather than parsed — and gate 20 counts the wrong thing**

`DOCTRINE_GAPS.md` gains Study 5 and Appendix C. This is the first study in the skill grounded in
playing games rather than reading their source, which the skill's own `references/agents.md` had
already argued for: *"the three games that were actually played produced every single heat finding
in the corpus, and the twenty-seven that were only parsed produced none."*

**What changed.** `DOCTRINE_GAPS.md` only — Study 5, Appendix C, and a Log row. **No reference file
and no gate was touched**, deliberately: two of the study's six outputs contradict decisions already
shipped, and resolving those is LO's call, not a silent edit.

**Why.** Three rules were live in `gates.py` and the reference files as inferences nobody had ever
observed — gate 20's 8-choice cap, guidance-must-exist, and `the-economy.md` R2's spread requirement.

**What it found.**

- **The `generic_porn_game` menu outlier does not exist.** The corpus parse put it at a median of 18
  links/screen, which was the single strongest argument that our cap was too low. It builds its hubs
  out of image buttons, and the parse counted the `<img>` tags. Real median: **4**.
- **Gate 20 counts the wrong quantity.** Every screen above ~12 choices in the corpus is a builder,
  roster, wardrobe or tracker. Among play surfaces, only DoL's streets exceed 8 — and a 12-link DoL
  street is 4 onward-travel exits + 4 standing travel affordances + **3–4 actual decisions**. Field
  median for things-to-do-here is **3, max 4**. Fourth denominator mismatch in this skill's history.
- **Guidance-must-exist confirmed 4/4**, by four different mechanisms, all always-reachable, all
  naming a place.
- **`the-economy.md` R2 marked *not established*** — the `shady_deals` session ended at 17 turns,
  before its sinks were walked. Recorded as untested rather than reported thin.
- **`engine.md` §15 is now contradicted by four games.** Every corpus door states its own
  requirement, including the exact tier (*"Skulduggery required: D"*, *"(Need Exhibitionism 2)"*).
  The locked-door gate was withdrawn on 8-12 *because* §15 ruled the other way; it is re-opened here
  on evidence that did not exist then, and flagged for revision rather than re-added.
- **M4 baseline**, which we had no number for at all: DoL moves state on **93% of turns, median 16
  variables**, against a corpus median of 2. `generic_porn_game` ran six identical mall loiters with
  zero state movement and byte-identical prose.

**How verified.** 198 turns across five games through `.claude/skills/twine-game-explorer/scripts/live.js`,
every turn logged to `game_explorations/study_*/study_turns.jsonl` with passage, visible choices,
engine state snapshot and explicit hits scored by `gates.py`'s own frozen `EXPLICIT` regex. Two
instrument bugs were caught and fixed mid-study, both of which would have inverted a finding — a
text-only link count that read image-button hubs as one-choice screens, and `live.js`'s
`variables_diff` being rebaselined by this study's own `eval` calls, which reported 0/59 turns of
state movement for a game whose arousal meter was visibly climbing. Scores unchanged (nothing in
`gates.py` was edited): **steam 17/19, back_home 13/18, vesper 6/17.** (Vesper read 5/17 on one
mid-session run and 6/17 before and after — a concurrent session is editing that game. Neither
number is attributable to anything here.)

**Free-play follow-up, same day.** A second unstructured DoL session (43 turns,
`game_explorations/dol_free/`) revisited surfaces repeatedly and diffed the rendered prose — the one
measurement `the-surfaces.md` R6 said it was waiting for: *"A threshold arrives when the play study
does."*

**`references/the-surfaces.md` R6 rewritten.** It said *"A hub re-entered daily whose first paragraph
never changes is a dead screen. Band it on whichever tier the location serves."* Measured: a DoL
location's opening sentence is **byte-identical on every visit** — six visits to one cafe, six times
the same first sentence — and it is the least dead game in the corpus. The variation is real and
dense but lives in four other places: a condition clause appended to the identity sentence (weather
and crowd, not progression), one presence line per NPC actually there, movement in the choice list
itself (5 → 9 → 8 across six visits), and events that replace the whole screen. On a repeatable
*action* rather than a room, variation is a scenario draw — eight cafe shifts produced five distinct
scenarios.

This also explains the seam that forced R6 to become a lint on 8-12: our TOML test asked whether the
opener carries a conditional block, so our games scored **0/22, 2/12, 11/29** against a practice the
reference game does not follow. R6 stays a lint with no threshold; what changed is that we now know
what to count. `DOCTRINE_GAPS.md` study 5 gains section R7 with the visit-diff table.

Also observed and worth keeping: DoL's labels state not just a requirement but whether you currently
meet it — *"Take them all out at once | Dance: Impossible"* — and failing that check still pays
(£8.50, minus respect). Free play surfaced it; a cost-in-label checklist would not have asked.

**Ruling on the two flagged items, same day — and both inverted on reading the source.**

**`engine.md` §15 stands unchanged. The study's claim that it was contradicted was wrong.** §15
governs `locked_text`, which **replaces** the action label — *"the player never sees what the action
was called"* — and prefers the want. Re-read against the four field doors: DoL's street label is
`Strip club (0:01)` with the opening hours on the passage *behind* it; CoT's is `[1] Strip` with the
Exhibitionism requirement in the body *after* clicking; shady's is `Check the local stroll.[7]` with
the gate in *adjacent* prose; GPG's `Enter (CLOSED)` is want **plus** suffix. **All four keep the
want on the label**, which is what §15 asks for. The study had compared a label-replacement rule
against evidence about where reasons are *placed* — a different axis, and the same denominator error
in new clothes. The withdrawn locked-door gate stays withdrawn. `DOCTRINE_GAPS.md` R4 rewritten with
the correction kept visible rather than edited away.

**Gate 20's ceiling of 8 stands; its denominator was never the problem.** The decisive fact came
from the code, not the play log: **259 of 259 choices in `steam` and `back_home` carry
`targetType = "node"`** — our engine renders location-to-location navigation as chrome, so gate 20
already counted decisions rather than links. The "12 links vs 23 choices" mismatch was in the
study's own comparison. `scripts/gates.py` G20 changed anyway, two lines: choices with
`targetType = "location"` are excluded, and the gate now reports "decisions" rather than "choices".
A **no-op today**, taken because the engine does support location targets (`v2.py:13252`). The
ceiling was **not** lowered to the field maximum of 6 — five games on one route each cannot carry
that precision, which is the failure that demoted R5 and R6.

**Verified:** scores identical before and after the code change — **steam 17/19, back_home 13/18,
vesper 6/17** — and G20 still fires on steam with its wording updated
(`9 location screens offer more than 8 decisions · hub_scrub_room @the_scrub_room: 17 decisions`).

---

## 2026-08-13 — **A goal-less card draws no frame, and that is how a finished arc ends up looking live**

`references/engine.md` §23 documented the three render frames in the right order and stopped there,
which left the most consequential case unstated: a card with no `goals` and no `terminal` matches
**none** of the three. That is not a blank row — the card still renders its `text` and its 💡 tip, so
it reads as an objective with nothing ticked yet.

Measured on `vesper` 0.1.8: at the end state the guidance page drew five sections, **four of them
closed arcs**, every one of them shaped like live work. The author walked the build to its final beat,
opened the page, and could not tell the game had ended.

Section 23 now states the trap, the fix (`terminal = true` on the last card of every arc), and the new
`terminal_text` override with its file:line pair — plus the cap that matters: **exactly one card per
game may set `terminal_text`**, since it promises future content and a closed-forever arc must not.
The full authoring rule, including the arc-complete-is-not-surface-closed split, lives in the
`author-game` skill's `references/quests.md` §7, updated the same turn.

Verified: green build, 5 `terminal` + 1 `terminal_text` in the built HTML, new 49/49 live suite, and
the two suites that read the guidance page (`live_beat_0084` 82/82, `live_rev141_bastien_cut` 73/73)
unchanged.

## 2026-08-12 — **Two gates built, both demoted to lints, and the measurement is why**

`the-surfaces.md` R5 (ungated doors) and R6 (frozen openers) are real rules that a real game
ignored, and the plan was to make them gates — the whole lesson of this project being that
paragraphs get skipped and only checks hold. **Both were built. Neither threshold survived the
check.**

**R5 — the ceiling had to be invented.** Set at 50%, Steam sits at exactly 50.0% and passes while
vesper fails at 52%. That is noise being scored. There is no field number, because "does this link
carry a condition" is not separable from engine plumbing in someone else's compiled game.

**R6 — not field-comparable at all, and the check nearly shipped backwards.** Measured on our TOML
(does the opener carry a conditional block?) our games look catastrophic: **steam 0/22 menus vary,
back_home 2/12, vesper 11/29.** Measured on the field's only available instrument — `<<if>>` present
in a built screen's text — the field median is **86%**, and re-measuring *our* built games the same
way gives **back_home 84%, steam 89%**, i.e. at or above the field median.

Both cannot be true. They are not measuring the same thing: in compiled output `<<if>>` wraps gated
choices, media and presence checks as well as authored prose banding, and the two cannot be told
apart in a game whose source we do not have. **A gate shipped on the first number would have failed
every game this project has built, on evidence that does not support it.**

> **Third time in this skill's construction that a measurement compared two different denominators**
> — after the explicit floor (whole-source units vs location beats) and the sentence ceiling (built
> HTML vs authored TOML). Assume the seam is there until it is ruled out.

Both are now `lint_screen_shape()` — printed every run, never scored:

```
steam       107/214 choices open on turn one · 22/22 standing menus never change their prose
back_home    12/57                           · 10/12
vesper       65/124                          · 18/29
```

Those numbers are real and worth reading. What is missing is any basis for a pass/fail — and
**whether a room's narrative actually changes on re-entry is a question only playing answers**,
which is what the play study agreed this session exists to settle. Scores unmoved: steam 17/19,
back_home 13/18, vesper 5/17.

---

## 2026-08-12 — **Presence is not placement: the economy gate rebuilt, and the heat floor made to admit what it is**

Two gates were giving false green on Steam. Both fixed; Steam drops **18/19 → 17/19**.

### Gate 17 — counting sinks was never the question

It passed Steam at **21 sinks : 20 sources** while **twelve of those sinks sat on one front desk**:
the water test, the advert, the electric, two wages, the frontage, the occupancy fee — in the same
undifferentiated list as *"Look up at the board."* That is a shop counter, not an economy. Money
leaves the player in one place, by one gesture, and no room in the world is ever the reason for it.

Now resolves each sink to its location and fails when **more than half land on one** — applied only
once a game has five or more sinks, below which concentration is meaningless. Steam fails at 12 of
21; `back_home` is unaffected (one sink, under the threshold) and still fails on the 1:12 ratio.

**The galling part:** this is the exact distinction the explicit-in-repeatable gate has made since
day one — *where content sits, not how much of it there is* — and the economy gate was built a
fortnight later without it. `the-economy.md` R2 now carries the placement half: **a sink belongs
where the thing being bought lives**, so the room it improves is the reason she needs the money.

### Gate 2 — a bare pass now says it is a bare pass

Steam cleared the explicit floor by **0.1 points** (7.6% against 7.5%) and printed a clean PASS.
That floor is the reference game's own 7.5–9.3% band — and that game is the **coldest of the 18
sandboxes** measured on this same word list, against a field median of 33.3%. So a game can sit
inside the reference's historical range, be four times colder than its genre, and read as green.

The threshold is unchanged, because there is no honest field-comparable number yet: the field was
measured on built HTML and this gate reads authored beats. What changed is that a pass between the
floor and 12% now prints **`← BARE PASS`** with the reason — *clearing this floor is not evidence
of heat; it is evidence of not being empty.*

**A calibrated heat threshold remains open work**, and it needs our own built games measured on the
field's instrument to exist at all. Recorded rather than guessed.

### Gate 3 — checked, and it was fine

Flagged in review as hiding volume behind a percentage. It was not: it already prints the absolute
count (*"93.8% of 65 explicit beats"*). The number was visible and the reader — me — treated the
percentage as the headline. **No change made.** Noted because a fix applied here would have been a
fix to nothing, and the review claim was wrong.

---

## 2026-08-12 — **`engine.md` §24: the facts that fake a broken game — promoted only after verifying them**

Steam's session could not find what it needed in `engine.md`, worked six things out by trial and
error, and wrote `games/steam/ENGINE_NOTES.md`. **Two of the six this project had already paid for**
— the day-name fact and the entity-encoding trap — both logged in *this changelog* rather than in a
reference file, so a fresh session lost time rediscovering them.

> **A changelog is a diary. Nobody reads it before starting work. If a fact is needed to do the job,
> it belongs in a reference file.** That is the whole reason for this entry.

### The verification came first, on LO's instruction, and it earned its keep

LO's call before promoting anything: *"these were written by the same agent building the game, so
they might be true or might be not."* Correct. Checked all six against source:

| claim | verdict |
|---|---|
| `State`/`Engine` on `window.SugarCube` | ✅ true — `window.SugarCube=` with `State:State`, `Engine:Engine`, in the built file |
| `current_day` is a day NAME | ✅ true — `v2.py:3273` `[…].indexOf(timeState.current_day)`, plus `:3444 :3588 :3643 :3706` |
| `setup.getNpcsPresentAtLocation(slug)` | ✅ true — `v2.py:4773`; the engine's own nav badges call it at `:19297`, `:19321` |
| `pickQuestsCards` takes one scope | ✅ true, and **understated** — `v2.py:14838` `if (scope !== "story_goals") return [];` |
| Playwright text selectors break | ⚠️ true, but **tooling, not engine behaviour** |
| page source is entity-encoded | ✅ true — **663** `&lt;&lt;set` against **3** literal in one build |

**Five promoted, one rejected.** The Playwright note went to `references/agents.md` under The
Player, not into `engine.md`: that file's value is that every line carries a source citation, and a
tooling observation cannot. Putting it there is how the file stops being trustworthy.

### And verifying exposed an error in §23, written the same morning

`§23` described `pickQuestsCards` as *"returns every matching top-tier card"* and **never mentioned
the scope guard** — which is the function's **first line**. Authored from source, and still missed
it. Corrected in place with the guard quoted, and the correction says so rather than being tidied
away: a wrong scope string produces an empty guidance section, silently.

### What §24 is, and why it is framed the way it is

**"Reading a built game from outside — four facts that each FAKE A BROKEN GAME."** Not a reference
list. Every one produces a false alarm indistinguishable from a real defect: bare `State` reads as a
dead build · a numeric `current_day` empties every room and reads as broken presence · hand-rolled
presence drops overnight windows and reads as an absent character · grepping the page for literal
`<<set` returns zero and reads as missing content. **The entity-encoding trap has now cost this
project twice** — once on a built game, once on an 18-game corpus where it produced a confident and
completely wrong measurement table.

### New operating rule in `SKILL.md`

**A note written by the agent that did the work is a CLAIM, not a fact.** Verify against source with
a `file:line` before promoting. Six claims checked: five held, one was misfiled, and the check
exposed a defect in a same-day reference section. Trusting the handback would have shipped both.

`games/steam/ENGINE_NOTES.md` keeps its content and gains a header pointing at §24, so the
game-local copy is not mistaken for the source of truth. Worth recording that the session had
already labelled its own notes **"LIVE-VERIFIED, NOT SOURCE-CITED"** — an honest handback is what
made the check cheap.

**Verified:** every promoted citation re-grepped against `v2.py` immediately before writing; scores
unmoved by a docs-only change — `steam` 18/19, `back_home` 13/18, `vesper` no crash.

---

## 2026-08-12 — **The missing axis: `the-surfaces.md`, and the sentence of mine that caused Steam**

`games/steam` was authored in a clean session by a reader of this skill, with no context carried
over — the honest validation `back_home` could never be. **It scored 18/18, and its front desk has
23 choices on one screen.** Full findings: `games/steam/REVIEW.md`. This entry is the fix.

### The cause was a sentence I wrote, with no scope on it

`engine.md` §19's *rule* is narrow and correct: two repeatable canvases binding **the same NPC** at
the same location with overlapping windows collide, and only one renders. Steam's `hub_front_desk`
and `hub_spring_street` **bind no NPC at all**, so it never applied to them.

But the paragraph attached to it read *"The fix is the engine's own advice, **and it is also the
better design**: make the second canvas a triggerless rung and hang it off the existing hub as a
CHOICE."* No scope, and it calls itself the better design. A careful author applies that everywhere
— and did. §19 now scopes the advice explicitly and points at the new file.

### What v2 was missing, stated properly

`SKILL.md`'s three content kinds — STANDING / TRIGGERED / MILESTONE — all answer **when content
fires**. **None answers which screen it lives on.** That axis simply did not exist in v2, so the
author invented one and picked the shape the loose sentence pointed at.

**New: `references/the-surfaces.md`.** The question is *who is this aimed at* — a person → their
hub, one per schedule row · the room or herself → its own located canvas · her, done to her → a
substitution. They never share an exit block. Carries the **object test** (is a person the object of
the verb? then it is a hub rung; *"Count the till"* is not), **money is not a scene** (11 of Steam's
23 desk choices are purchases sitting beside *"Look up at the board"*), ungated choices are the
minority, and the opener moves.

*(The incumbent skill solves this with a four-lane model and states the same separation at
`lanes.md:96`, including a pronoun-in-the-verb test and the observation that "all Lane 1 =
transactional menu game". v2's version is organised by **who the content is aimed at** rather than
by who decides it fires, because that is the question an author can answer while writing, and
because v1's lane budgets are keyed to arc shapes v2 does not have. Studied, not copied.)*

### Gate 20 · a place is not a catalogue — **measured, not asserted**

Re-pulled the 18-game corpus and counted player-facing links per non-system screen:

```
median screen ..................... 2 links
median p90 ........................ 4 links
screens offering more than 12 ..... ~2% (field median)
```

**Ceiling set at 8** — double the field's ninetieth percentile — for any repeatable,
location-bound canvas. Triggerless rungs are exempt; they are link targets, not screens.

The nuance that stopped this being a flat cap: **big screens do exist in good games.** The reference
game runs 2.9% of its screens above 20 links — and they are *catalogues*: shops, wardrobes,
character creation. A catalogue is legitimately long. **A place the player returns to daily is not
a catalogue**, and Steam's error was merging one into the other.

**Verified:** `steam` **18/19** — the gate names all nine offending screens (23, 19, 19, 18, 17, 16,
14, 12, 12) · `back_home` **13/18**, passes at a max of 7 · `vesper` 5/17, no crash.

### And the thing Steam proved about how doctrine has to be written

Everything encoded as a **required field** came back correct and unprompted: `board.map` with 6/6
real homes, `board.economy`, `board.guidance`, 24 quest cards, 6/6 ladders with end cards, all
locations reachable. Everything encoded as **advice** was not: the heat guidance added that same
morning (*"clear it, do not aim at it"*) produced a game sitting on the floor at 7.6%.

**Second game running.** Declarations and gates hold; paragraphs do not. Every future doctrine
change should ask which of the two it is before it is written.

---

## 2026-08-12 — **Tier 1 graduated: four studies become doctrine, and the scoreboard grows teeth**

The four studies in `DOCTRINE_GAPS.md` are now reference files, and their checkable half is now in
`gates.py`. **`back_home` scores 12/17, exit 1** — the ten original gates all still pass, and every
new failure is a defect the game shipped with. That is the intended outcome: LO's call was one
scoreboard, not a second unscored tier, because a check that cannot fail is exactly the failure v1
documented against itself.

**New reference files** — self-contained, no cross-reference to the incumbent skill, written in
`want / board / release` vocabulary:

- **`references/the-map.md`** — the map is a place, not a room list · residents have homes ·
  if she travels there is something to travel through · the graph owes the prose · travel friction.
- **`references/the-voice.md`** — the game's own voice, plain and never performing: labels answer
  "what happens if I click", every ascent tier carries a visible ladder, name the feeder not the
  number, nothing retires into silence.
- **`references/the-economy.md`** — money must gate content · sinks outnumber sources · the
  obligation is real and has a face · prices move with state · no free uncapped income.
- **`references/register.md`** expanded — sentences run short, second person is the genre standard,
  dialogue as a direction not a threshold.

**`gates.py`: +7 gates, +1 lint, and a header that now names two measurement bases.**

```
11 world reachable          12 residents have homes      13 guidance exists
15 no chain ends in silence 16 money gates something     17 sinks >= sources
18 no free uncapped income  19 sentence length (ceiling 14)
lint · the prose names places the map does not have
```

**The declare-then-check pattern is now an operating rule**, added to `SKILL.md`: where a property
cannot be inferred from the TOML, the board declares it and the gate checks the game against its own
declaration. `state.md` and `templates/board.toml` gain `board.map` (shape, dwelling, exterior,
**homes**, bridges) and `board.economy` (currency, obligation, **sinks**). A gate with no declaration
to check against reports **n/a**, never a pass.

**`engine.md` §22–23** — twelve verified facts v2 never had. Locations can charge a per-entry
`costs = { time, energy }` (`template_import.py:170`, `:1778`; `v2.py:4681`, `:15276`) — the
mechanical answer to a premise that says *"ten minutes' walk away"* while arriving costs nothing —
plus `entry_conditions`/`blocked_message`, `offscreen`, `is_container`. And the guidance table is
`[[quest_cards]]` (`template_import.py:2456-2462`), gated on `quests_engine = "v2"`
(`v2.py:14711`), whose **conditions use a separate evaluator with no fail-open** (`v2.py:14878`) so
`version = "1.0"` must never be pasted onto a card.

### ⚠️ One study output was WITHDRAWN on contact with the engine, and it is the most useful thing here

Study 2's R4 proposed a gate requiring every locked door to carry `locked_text`. It was built. It
fired on **7 of 8 doors in `back_home`** — and then `references/engine.md` **§15, which already
existed**, turned out to rule the other way and rule deliberately:

> omit `locked_text` and the greyed row shows the action ("Stop pretending it's a secret") — a *want*
> the player can name, which is what sells the next release … **Prefer the want unless the gate is
> genuinely obscure.**

Every one of those seven doors was following the skill correctly. **A check that fails a game for
obeying the doctrine is a bug in the check**, so no gate shipped; R4 was rewritten as *"the wall
shows the want, the card shows the route"*, and `games/back_home/REVIEW.md` **G2 was withdrawn as
not-a-defect**. Also added to `SKILL.md`'s operating rules, because the same trap will recur:
**when a gate you just wrote fails a game, check the skill before blaming the game.**

### Two other corrections the build forced

- **`back_home` has twelve money sources, not three.** `REVIEW.md` E1 counted only the clean shop
  income; the gate counted every canvas that grants money, including nine transactional rungs.
  1 sink : 12 sources. The defect is worse than first recorded, and it was found by counting what
  the game does rather than what the author remembered.
- **The sentence-length figure is instrument-dependent and the constant now says so.** The field
  medians come from parsing built HTML; the gate reads authored beat text from the TOML. The same
  game measures 16 on the first and **13** on the second, so it passes the ceiling of 14. The
  threshold spans a seam and is APPROXIMATE — it catches drift, it does not certify a match. Closing
  that gap would need the field re-measured on TOML we do not have.

**Verified:** `gates.py back_home` → 12/17 exit 1, every new FAIL cross-checked against a
`REVIEW.md` finding · `gates.py vesper` → 5/18 exit 1, does not crash, `residents have homes`
correctly **n/a** with no ledger present, and it independently caught **18 of vesper's 27 locations
unreachable on foot** · `--json` parses with 17 gates and both lint keys.

---

## 2026-08-12 — **`DOCTRINE_GAPS.md` opened: what v2 never learned about building a good game here**

New file, `DOCTRINE_GAPS.md`, next to `STATUS.md`. No reference file changed.

**The trigger.** LO played `back_home` and asked why it has no quests. Traced it: `templates/board.toml:26`
ships `quests_engine = "v2"`, which lights up a sidebar entry and a "What's Next" page, and across all
1,367 lines of v2 doctrine there is **zero** quest instruction and **zero** quest check in `gates.py`.
Verified: `setup.quests_cards = []` in the built game. A game built exactly to spec ships an empty
guidance page.

**The root cause, and it is bigger than quests.** v2's doctrine was derived solely by measuring one
reference game's source. That game has no quest log. **A doctrine derived from measuring one game
cannot contain anything that game lacks** — even when our engine ships the feature and the incumbent
skill teaches it. Measured: the incumbent carries 38 reference files / 9,672 lines; v2 carries 7 /
1,367, or **14%**. Nearly every finding in `games/back_home/REVIEW.md` maps to a file v2 does not have.

**The decision (LO's, this session): v2 never links to or imports a v1 file.** Not tidiness — v1's
references are welded to v1's pipeline (`step-5-blueprint.md` says "Step N" 24×, `step-3-casting.md`
16×, `content-framework.md` 15×), so importing one imports v1's chapter shape into the skill whose
thesis is that the shape was wrong. Same failure as the `prompts_v2` dependency. Each item is studied,
not copied, and every study ends in a **check** rather than a paragraph — the case for which is made by
v1 against itself at `location-design.md:257`, on a locked-flag bug that *"shipped twice: v1's Dining
Room, then again in the rebuild written to prevent it."*

**Contents:** a 12-item inventory over three tiers, save-safety parked as separate work (and argued to
matter more for v2 than v1, since a never-ending product lands every release on live saves), the
item-2/item-4 boundary settled (interface text is plain and functional; RTS-flat governs everything
read *after* a click), and **study 1 — map & space** in the five-part format.

**Study 1's substantive output:** four engine capabilities verified against source that `engine.md`
does not carry and must — location travel-friction `costs = { time, energy }`
(`template_import.py:170`, `:1778`; `v2.py:4681`, `:15276`), `entry_conditions` + `blocked_message`
(`template_import.py:159-160`, `:1775-1776`; `v2.py:6590`), `offscreen` (`template_import.py:154`),
and `is_container` + `default_entry` (`:153`, `:3968`). Travel friction is the mechanical answer to a
premise that says *"ten minutes' walk away"* while arrival costs nothing.

Also recorded: **`back_home`'s missing-bedrooms defect passes v1's entire 13-point location audit** —
274 lines of map doctrine with no rule that a resident needs a room — so v1 is evidence about the
problem, not the answer.

### Study 2 — how the game talks to the player *(same day, format approved by LO after study 1)*

Names the category no skill owns: **everything the player reads that is not the story** — room names,
activity labels, the guidance page, meter band words, locked-door text. Four `REVIEW.md` findings
(G1 G2 W5 W7) with one cause. v1 splits this across two files and two gaps: `quests.md` covers cards,
`location-design.md §3` covers room names, and activity labels, `locked_text` and meter words are
covered nowhere — which is how a game can hold a consistent naming style and still be unreadable.

**Where v1 is wrong, beyond the split:** of `quests.md`'s 285 lines, the rule about how a label should
*read* is one paragraph; the rest is engine mechanics. And its top tier is a **mission spine** — *"the
Story-Goals column… the mission's current want"* (`:173`) — which a v2 game does not have. Copying it
would smuggle a story shape into a release stream, so v2 needed its own answer: **the top of the
guidance page is the ascent tiers themselves**, one card per band via v1's stepped trait-band shape.
That falls out of v2's architecture instead of being borrowed.

**Carried over from v1 because it is measured, not asserted:** the label is a walkthrough line —
place + person + verb (`quests.md:81`); and **a meter-gated rung names its FEEDER, not its number**
(`:91`) — *"the HUD already shows the number; the ROUTE to raising it is what the player can't see."*
That is the single most load-bearing rule for v2, whose every gate is a meter.

**One rule v2 owns harder than v1 did:** an arc whose last card retires with nothing behind it makes
the character's whole section disappear. v1 found it (Renner's heading, unnoticed for eleven beats).
In v2 it is worse by construction — a product that never ends turns every topped-out character into
permanent sandbox content at the exact moment the chain goes silent.

**Corrected while verifying:** the authored table is **`[[quest_cards]]`** (`template_import.py:2456-2462`,
`class QuestsCard` `:997`), *not* `[[quests]]`. `games/back_home/REVIEW.md` G1 said the wrong table name
and was fixed; the finding itself stands — zero `quest_cards` across all five phase files, and
`setup.quests_cards = []` in the built HTML.

**Eight more engine facts verified and flagged for `engine.md`**, including that **quest conditions use
a separate evaluator with no fail-open** (`v2.py:14878`) — so the `version = "1.0"` key that canvas
conditions require must *not* be pasted onto a quest card — and that the sidebar next row calls the
identical renderer as the page (`v2.py:15454-15456`), so there is no such thing as a separate sidebar
quest.

**The pattern now holds twice.** Both studies' load-bearing gates work by having the board phase
**declare** a property the TOML cannot express, then checking the built game against that declaration
(study 1 Gate B: where each resident sleeps; study 2 Gates C/E: which tiers and characters owe cards).
Proposed as the skill's standard gate shape rather than being rediscovered per study.

**Also held twice:** each study refuses to gate the thing it cares most about — *"is the map a coherent
place"*, *"does this label read well"* — because neither is mechanically decidable, and a check that
measures a proxy is how `back_home` shipped 10/10 with no street.

### Study 3 — money & pressure. **The first study measured on more than one game.**

LO's instruction: verify against real games, and *"not just 3 or 4 — get at least 10."* Pulled **18
shipped browser sandboxes, ~62,000 passages**, as complete single-file SugarCube source. URLs came from
this project's own prior live-play sessions in `game_explorations/`; a `mopoga.com/<slug>` page carries
the real file URL in `data-game-url`, and those `/embed/` URLs serve the full compiled game. Corpus,
method and limits recorded in `DOCTRINE_GAPS.md` Appendix B.

**Two extraction bugs found and fixed before any number was trusted**, both logged because the first
pass produced a confident wrong table: (1) passage bodies are **HTML-escaped** in a compiled Twine file,
so every `<<set>>` regex silently matched nothing — DoL read as *"0 spending"* against 372 gates, which
is what exposed it; (2) money mostly moves through **per-game widgets**, not raw `<<set>>` — DoL uses
`<<money -350000 "farmUpgrades">>`, `life_at_university` uses `<<addmoney>>`/`<<redmoney>>`. The final
extractor discovers each game's money widgets from its own `<<widget>>` definitions. Currency selection
was also changed to pick by **usage** rather than name frequency, after `road_to_success` resolved to the
decoy `$game.randomMoney`.

**The measured rules:** money gates content at a **median 67.3 conditions per 1,000 passages** (every
sandbox in the set does; `back_home` is at **0**, independently confirmed from its TOML) · **sinks
outnumber sources at a median 2.2:1** (DoL 1.76:1; `back_home` has three sources and one sink) ·
**14 of 19 carry a real recurring obligation** (DoL says *rent* 130 times — the one thing `back_home`
gets right) · a median **24% of money movements carry a computed rather than literal amount**. Plus one
rule from the failure rather than the corpus: **no free uncapped income**, the single line that would
have caught `E1`.

**Where v1 is wrong here, and it is a precise defect:** `rent.md` §8's safety rule guards only the
downside — *"rent that can't be paid isn't pressure, it's a scripted loss"* — with **no rule against
trivially payable**, and no ratio to tune against. `back_home` obeyed v1 exactly and the pressure
evaporated. v1 is also scoped to rent as a mechanism and develops no doctrine of sinks at all, which is
why the game ships **zero items**.

**And the finding that justifies the whole DOCTRINE_GAPS exercise:** DoL carries **738 money movements
and 372 money gates**. v2 derived all ten of its thresholds from this game's source — words, locations,
explicit ratios — and never once measured its economy.

**Side result: `games/back_home/REVIEW.md` O1 is resolved, not by argument but by holding the file.**
`gates.py:7` cites the reference as *"1.7k → 15.6k units"*; the pulled source contains **15,587
`<tw-passagedata>` passages**. So a "unit" is a whole-source passage — combat, systems and UI included —
while `gates.py` counts beats in **location prose only**. The two denominators were never the same, so
back_home's 27.8% against a 7.5–9.3% band was never a valid comparison and **no dilution pass is owed**.
`gates.py`'s header should say so, or this gets re-litigated a fourth time.

**Verified:** all 18 files confirmed SugarCube with non-zero passage counts before parsing; every rule
above recomputed after both extractor fixes; `back_home` run through the identical instrument, with its
non-comparable flow counts excluded from the medians and marked as such.

### Study 4 — how the prose is written. Same corpus, `gates.py`'s own explicit regex.

`v1/rts-flat-prose.md` is 735 lines, the largest file in either corpus; `v2/register.md` is 111 and
covers **one topic** — how to write an explicit beat. Sentence length, dialogue, how an ordinary
non-sexual paragraph reads: undocumented in v2.

**A third extraction trap, and it invalidated the entire first pass.** The longest "prose" passages in
every game are **widget libraries and CSS** — `back_home`'s was the engine's own widget library, DoL's a
combat widget, *Road to Success*'s a styled laptop UI. Fixed by dropping passages tagged
`widget`/`script`/`stylesheet`/`init`/`header`/`footer`, bodies defining widgets, and — the load-bearing
filter — **any passage whose stripped text is under 40% of its raw length.** Nothing in the study is
quoted from the polluted pass.

**R1 — the one length measure that transfers: `back_home`'s sentences are too long.** Median sentence:
**field 10 words, DoL 9, `back_home` 16** — third-longest of eighteen, 60% above the field. First hard
number confirming our prose is denser than the genre, which is what "RTS-flat" was always reaching for.
Proposed as **Gate I, ceiling 14** — the first gate in this exercise that measures *writing* rather than
structure.

**R2 — second person is the genre standard, 13 of 17 games.** `back_home` at 94% *you/your* is the
highest in the corpus. v2's `narration_person` default is **validated by the field** — the one piece of
v2 prose doctrine the corpus confirms outright.

**R3 — the reference game is the coldest game in its own genre.** Percentage of prose passages carrying
3+ frozen-list words: field median **33.3%**, `back_home` 43.4%, **DoL 7.5% — last of eighteen.** Note
`gates.py` sets `EXPLICIT_BEAT_FLOOR = 7.5`; this run reproduces that derivation independently on a
different unit and shows the number is **a property of DoL, not of the genre.** Valid as a floor, badly
miscalibrated as anything resembling a target. **This closes the `back_home` heat worry a second time,
from a second direction** — O1 showed the denominator was wrong; the field now says 43.4% is mid-pack
with five games above it.

**Where v1 is wrong — and the one place it cannot be judged.** Its headline claim, *"RTS runs 0.73
narration words : 1 dialogue word … every game this skill has shipped runs 5:1 to 19:1 the other way.
This is the drift"* (`rts-flat-prose.md:12`), rests on **one game** — the same methodological error v2
made with DoL. And it is **untestable from the compiled artifact**: *Road to Success* is built from
HTML/CSS interior markup, so only **31 of its 373 passages** survive prose extraction. The study does not
claim the number is wrong; it records that a rule calling everything else "drift" has never been checked.
What the corpus does support is the direction — the two most prose-dense games in it are the two most
dialogue-heavy (DoL 2.7:1, `course_of_temptation` 3.8:1) against a field median of 33:1.

**Explicitly not transferable, recorded in Appendix C:** passage length (our engine emits a whole canvas
as one passage — `back_home` 429w median vs field 175w measures architecture, so **the 35–40-words-per-beat
rule is neither confirmed nor refuted here**) and v1's dialogue ratio, above.

**Verified:** every figure recomputed after the tag/markup filter; `back_home` run through the identical
script; per-game sample sizes reported so the small ones (`road_to_success` 31 passages, `back_home` 122)
are visibly weaker than DoL's 10,215.

**Verified:** every engine citation above read from source this turn; the v1/v2 line counts from `wc -l`;
the quest counts from `grep` over the skill and from `setup.quests_cards` in the built HTML.

---

## 2026-08-11 — **v0.1 SHIPS: 10/10. The first green game this skill has ever produced.**

```
[PASS]  location fill        8 locations · 36,035 words · mean 4,504 · median 4,381 · anchor 27%
[PASS]  explicit floor       27.8% of 270 beats carry 3+ explicit words (floor 7.5%)
[PASS]  explicit in repeatable  100.0% of 75 explicit beats are re-enterable
[PASS]  repeatable explicit media cycles  49 pooled, 0 fixed single-clip
[PASS]  traversal heat       7/8 locations (88%) carry a cycling explicit pool
[PASS]  standing surface     4/4 characters findable and scheduled
[PASS]  milestones open something   4 of 4
[PASS]  meter ceiling        0 visible meters rise past their content
[PASS]  ends on an opening   8 choices render visible-but-locked
[PASS]  ascent tiers expand the world   nerve · exposure · need, all upward
────────────────────────────────────────────────────────────────
10/10 judged gates pass          EXIT CODE 0
```

`games/back_home` — **36,035 words of location prose, 8 locations, 4 characters, 270 beats,
75 explicit, 8 locked doors.** Nothing had ever passed all ten before; the promotion criteria in
`STATUS.md` require exactly this.

### The last room: the shop, and it stays cold

`the_shop` 654 → **2,952**, and **every beat in it scores 0 on the explicit floor, on purpose.** The
Want: *"the one room where no man wants anything from her, and that is its entire function."* It is
the counterweight to five rooms of heat, and `register.md` is explicit that a game far above the
floor is usually one that has stopped having non-sexual texture.

Four surfaces:

- **`activity_shift` 76 → 594.** The single most-repeated money click in the game was one paragraph.
  Banded on `need`: thirty pounds as pocket money, then as the four-shifts-is-the-rent arithmetic she
  cannot stop doing mid-transaction, then as *the only money in her life that arrives without a face
  attached to it.*
- **`activity_the_walk`.** Ten minutes each way is the only stretch of the day she is outside the
  house **and** outside the shop — the one part of the map nobody in the game can see her in.
- **`activity_stock_hour`.** The room's declared job is *money that is hers* and there was exactly
  **one** way to earn in this game. A second lever on `need` that is not a man is what makes the
  trades elsewhere a choice rather than the only road.
- **`triggered_hannah_again`** — pays the logged promise. Three bands on `pride` that are three
  different answers to the same question: the voice that means no, the drink that actually happens,
  and the standing fortnightly lie to the one person who thinks she is basically all right.

**No new location for the drink.** *A release adds events, not places* — it happens off-screen and
arrives back at the counter. And Hannah stays **narrated, never declared**: an `[[npcs]]` entry would
fail gate 6 on the spot, which is why she speaks in quoted prose rather than `dialog` blocks.

### Verified live, end to end — not just the new surfaces

- Age gate → opening chain plays with **no state forcing at all**; `arrival_done` set, player lands
  at `her_room`.
- The full schedule grid on a **weekday and a weekend**: Ray 06:30 bathroom → Dean 08:30 kitchen →
  Marek 10:30–14:30 box room → Cal 16:30 front room + Marek 16:30 kitchen → Ray 18:30 garage → Ray
  20:30 front room. Saturday differs correctly (Dean 14:30 garage, no Ray bathroom row).
- **All eight locations render** with actions at a mid-game state: 5 · 3 · 3 · 5 · 7 · 2 · 6 actions.
- **Zero JS errors** across the whole pass.

### v0.1 closed out

`phase` flipped **`board` → `release`** in `v2_state.json`, with a `releases[]` entry recording
subject, what it added, what it opened and the gate scores. Per `the-release.md`: *never build a
"chapter" again.*

**13 promises stay open, and that is deliberate rather than accumulated.** Eight of them **are** the
locked doors — that is what "every release ends on an opening" means, and closing them would be
closing the product. The other five are plants with content owed: the lodger leaving in spring,
`keep_unpaid` changing the terms with Ray, Dean's uncharged version, Cal's eight hundred and forty,
and Ray finding out where the rent money came from. Nothing is cut; every one is a release subject.

### What this run cost, and what it produced

Six increments, **+17,153 words**, and every one of them turned up something the instrument could
see and a reader could not:

| # | room | the finding |
|---|---|---|
| 1 | bathroom | two harness facts that faked a broken game (the clock lives at `game_state.time_state`; blind cascade-advance double-applies effects) |
| 2 | kitchen | **the `clamp` bug** — every money grant capped at 100 against a 120 rent, so the rent was unpayable. `engine.md` §21 |
| 3 | her room | **a category name is not a sweep** — the register rule had been applied to "the sex loops" instead of to everything under the floor. `register.md` |
| 4 | box room | **the rotating slot was never split by lifetime** — room-scoped content must name the occupant by role. `the-board.md` |
| 5 | garage | the explicit-floor comparison **checked instead of acted on** — the reference denominator may not match ours, so the room was not diluted to chase a ratio |
| 6 | shop | one-scene characters are narrated, never declared — gate 6 enforces it |

Three of the six produced doctrine changes to the skill itself. The register defect appeared in
**new prose in four consecutive increments**, written each time immediately after re-reading the
rule against it — which is the strongest evidence yet for `register.md`'s own claim that it
reasserts the moment it is not being actively fought, and for keeping the per-beat scorer in the
loop rather than trusting a read-through.

**Still open, and now the top of the list:** the explicit-floor denominator question (28% against a
band that may not be comparable), media (47 declared `pool_dir` slots, zero files — deferred by LO
until after he plays it), and **the agents**, which remain the skill's largest architectural gap.

---

## 2026-08-11 — v0.1 fill 5/6: the garage, and a deliberately cold surface

**What.** `the_garage` 801 → **3,514 words** — the thinnest room in the game and the last big add.
Files: `games/back_home/toml_phases/5_scenes.toml`, `3_activities.toml`, the game's `v2_state.json`.

### The room was Ray's and had 309 words of him in it

The Want gives Ray a specific mechanic: *"he is careful, so every inch is expensive and deniable —
which makes an inch feel like a mile."* The front room is his **money** surface (rent, the ask, the
arrangement); the garage is where the deniable register belongs, and his garage ladder **topped out
at exposure 15** while his front-room ladder ran to need 75.

Two rungs and a door, verified live:

| rung | gate | the mechanic |
|---|---|---|
| `rung_ray_garage_hold` | nerve 35 | **deniability as an engine.** Out here contact has a *job* — holding the other end of a board — so it can happen and still be about the board. Bands on his lust: he stops saying sorry, then there stops being a job, and there is a fresh plank on the trestles every evening that nobody comments on |
| `rung_ray_garage_bench` | exposure 55 + his lust 30 | explicit, and it happens in the one room with a door to the outside. Afterwards he says *"Right."* and holds the door and asks Dean whether the football is on |
| *locked* "Ask him where the bench went." | nerve 75 | the room's door |

```
nerve10           tea · [LOCKED] where the bench went
nerve40           + what you've got on · hold the other end · [LOCKED]
nerve60 lust35    + stay out here after he's finished · [LOCKED]
nerve80           the locked row goes live
```

Ray already owns a need-75 door in the front room; nerve 75 here is a different axis and a different
want, so it is not the same promise twice. Dean's weekend ladder went 2 → 3 rungs
(`rung_dean_garage_bar`, exposure 45 + his lust 25 — three hours, empty house, door up a foot).

### The bench-shaped absence

The room's defining detail is a **gap**: the weight bench in her bedroom came out of this garage, in
the same fortnight the desk went to the tip. There is a rectangle of clean concrete on an otherwise
filthy floor and nobody in the family has ever mentioned it. It is planted in three canvases now and
the nerve-75 door is where it finally gets named — **logged as a promise, not paid**, because the
answer is a scene and this increment did not write it.

### A surface written cold on purpose

`activity_the_garage` (512 words, room-scoped, names no NPC) has **zero explicit beats and that is
the design**, not an oversight: a garage with nobody in it is not erotic, and `register.md` says a
game far above the floor is usually one that has stopped having non-sexual texture. It carries the
biro height-marks on the door frame that stop the year the mother left, and the two mugs Ray has
been filling the kettle for without ever mentioning it.

Also banded the two remaining flat presence-floor rungs, `rung_ray_tea` (147 → 500) and
`rung_dean_weights` (148 → 327) — the same treatment the kitchen and box-room floors got.

### The floor question, checked rather than assumed

Last increment I called 26.3% "3× the reference band" and treated it as a looming problem. Before
letting it drive design I tried to check the comparison, and **it cannot be checked from here**:

- `gates.py` measures **location prose only** — that denominator correction was made to gate 1 on
  2026-08-10, when the word count was found to include `base-combat` and `base-system`.
- `EXPLICIT_BEAT_FLOOR`'s own header cites the reference at **1,772 → 15,629 units**, which look like
  whole-source unit counts. If that denominator included combat, systems and UI passages and ours
  does not, **the two percentages are not comparable at the top end.**
- No reference snapshot is on disk. This stays a hypothesis.

What survives either way: it is a **floor**, the game clears it, and the discrimination test holds
(the measured-cold game scores 4.7% on this same instrument). So the garage was **not** diluted to
chase a ratio — Ray's arc genuinely lives in that room — and the cold surface is cold for its own
reasons. **Open question for after v0.1:** either re-derive the reference ratio on a location-only
denominator, or say plainly in `gates.py` that the upper comparison is not meaningful.

### Tally

```
[FAIL] location fill   8 locations · 33,728 words · mean 4,216 · median 4,381 · anchor 28%
       · mean location 4,216 words (need 4,500)
```

Explicit floor **26.3% → 28.1%** of 267 beats; explicit beats 67 → **75**; doors 7 → **8**; every
garage beat that was under the floor (`rung_dean_spot` 1, `rung_ray_garage_cold` 1) now clears, and
so do the three that this increment's own new prose produced at 1–2. Zero JS errors.

**One room left.** The shop 654 → **2,950** (+2,296) lands the total at **36,024**: mean 4,503,
median 4,381, anchor 26.7%. That is gate 1 closed.

---

## 2026-08-11 — v0.1 fill 4/6: the box room and the landing, and the rotating slot was never split by lifetime

**What.** `the_box_room` 1,228 → **4,381**, `the_landing` 1,367 → **1,963**. Files:
`games/back_home/toml_phases/3_activities.toml`, `5_scenes.toml`, the game's `v2_state.json`, and
`references/the-board.md` — the finding is about the rotating-slot pattern, not about this game.

### The finding: the slot's economics were designed, its content was not filed to match

The box room is the premise's answer to never-ending — *a new character at an existing location
every few releases* — and the ledger records the intent that replacing the lodger **touches only his
`[[npcs]]` entry and his block in `5_scenes.toml`.**

That only holds if content is filed by **how long it lives**:

| scope | covers | file | survives rotation |
|---|---|---|---|
| **tenant** | his ladder, his register, his props | `5_scenes.toml` | no — dies with him, deliberately |
| **room** | the slot, the mattress, the wall, what the arrangement *is* | `3_activities.toml` | **yes** |

`activity_his_room` was room-scoped **by file** and tenant-scoped **by content**: a specific
submarine thriller, a bus ticket from a named town, a biscuit tin with a named amount in it. Every
one of those is Marek. The first rotation would have cost a rewrite *in the file the plan says it
will not open* — a cost that is free to avoid while writing and annoying afterwards.

**The rule that fixes it: room-scoped content names the occupant by ROLE, never by name.** Now in
`the-board.md` with the table above. The tenant-specific version of the bag moved to
`rung_marek_bag`, where it is supposed to die.

The room-scoped layer also turned out to be the more interesting half, because it is the only place
the slot is legible **as a slot**: the same mattress through four tenants, marks on the wall at three
different headboard heights, a name she has genuinely forgotten, and the fact that the terms get set
in the first fortnight by whoever is standing on the landing when the new one arrives.

### His ladder had a hole in the middle and nothing at the top

It ran *stand in the doorway* (no gate) → *ask what he's paying Ray* (need 15) → **the explicit
loop** (need 35 + exposure 55). Three rungs added, verified live at their gates:

| rung | gate | what it is |
|---|---|---|
| `rung_marek_watch` | need 25 + exposure 35 | the missing middle — he prices *looking*, in the voice he priced the room in |
| `rung_marek_bag` | his relation 45 | **pays the logged promise**: the packed bag, unopened since October. The only scene in his ladder with no transaction in it, which is why it costs him more than the loop does |
| `rung_marek_after` | `marek_arrangement` | Cal and Ray both had a post-arrangement rung; he had none, and his is a 09:00–16:00 empty house with nothing to get back to |

```
cold                    doorway · [LOCKED] tell him what it costs now
need30 exp40            + what he's paying Ray · what else he'd pay for
need60 exp60 rel50      + the bag · the offer · stay after · [LOCKED]
```

Every effect matched its declaration (`rung_marek_watch`: money +20, need +3, exposure +3, pride −3,
his lust +6). Zero JS errors.

### The sweep, again — and it caught the new content too

Seven beats across the two rooms scored 1 or 2 and were lifted: the Marek loop's actual sex beat
(**1 → 6**) and its finish (**1 → 3**), and six landing peep beats. The landing now reads
`3·3·3` / `3·4` / `3·7·4` / `4·4` where it read `3·3·1` / `3·2` / `1·7·1` / `2·2`.

**And the content written this increment did it again** — `rung_marek_watch` came out at 2 on its
middle beat and `triggered_lodger_home` at 2, both caught by the same per-beat pass. That is the
fourth consecutive increment where the defect appeared in *new* prose written immediately after
re-reading the rule. `register.md` is right that it reasserts itself the moment it is not being
actively fought.

### Tally

```
[FAIL] location fill   8 locations · 31,015 words · mean 3,877 · median 4,381 · anchor 31%
       · mean location 3,877 words (need 4,500)
```

Explicit floor **22.4% → 26.3%** of 255 beats; explicit beats 53 → **67**; doors still 7; anchor 31%.

⚠️ **Honest note on the floor.** 26.3% is roughly three times the reference game's measured 7.5–9.3%
band. The floor is a floor and the game is not failing anything — but `register.md` warns that a game
far above it is usually one that has stopped having non-sexual texture. The two rooms left are the
two coldest in the game (the garage, and the shop which is cold by design), so the ratio should come
down on its own. **If it does not, the next increment after v0.1 is texture, not heat.**

**+4,985 remain** — the garage and the shop, and they are the whole of it.

---

## 2026-08-11 — v0.1 fill 3/6: her room, and the backward sweep that was only half done

**What.** `her_room` 1,496 → **3,927 words**, and the median half of gate 1 now **passes**. Files:
`games/back_home/toml_phases/3_activities.toml`, the game's `v2_state.json`, and — because the
finding is about how the register rule gets applied, not about this game — `references/register.md`.

### The measurement that set the increment

The room where privacy structurally fails, containing the only surface in the game she initiates
alone, had **eleven beats and not one of them cleared the 3-word floor**:

| canvas | before | after |
|---|---|---|
| `activity_alone` — the solo sex surface | **1 · 1 · 0** | **7 · 3 · 0 · 0** |
| `activity_the_wall` | **2** | **9** |
| `activity_the_door` | **2** | **5** |
| `activity_get_dressed` | **1** | **3** |

Every one was the pivot: one body word, then off the body for the rest of the beat.

### The doctrine finding — a category name is not a sweep

Phase 1 applied this rule backwards and moved the game 10.8% → 15.9%. It did it to **"the three
repeatable sex loops"** — a *category* — rather than to everything the instrument scored under the
floor. These four canvases were written the day before the rule existed, were never in that
category, and sat under 3 through two further increments **while the headline number rose**.

> Score every beat, sort ascending, fix everything under 3. The instrument already prints per-beat
> scores; there is no reason to select by intuition.

Now in `register.md`, with the corollary that stops the over-correction: **a 0 next to a 4 is the
rule working** — the interiority beat *after* an explicit one is supposed to score 0. What you hunt
is the beat scoring **1 or 2**, which is a beat trying to be explicit and pivoting partway.

The new content proved the point immediately: the three intrusions came out at **2 · 2 · 2 · 0** on
their first pass and had to be lifted before they cleared — written by the same author, in the same
turn, directly after diagnosing it.

### The door had never once been come through

The room's declared thesis is a catch that does not reach the plate — *"the room privacy is supposed
to happen in, and does not"* — and six shipped canvases all had her alone in it with the door as
scenery.

No NPC is scheduled in `her_room`, so `npc_at_location` has nobody to find and `requires_npc` has
nobody to hold. The only pattern that works without a schedule is the bathroom's:
`substitution_only` canvases on the mandatory daily click.

| intrusion | parent | gate | the character in one gesture |
|---|---|---|---|
| `intrusion_cal_room` | `activity_get_dressed` | exposure 25 | knocks on a door that has already swung |
| `intrusion_dean_room` | `activity_get_dressed` | exposure 45 | does not knock, and pushes it to behind him |
| `intrusion_ray_room` | `activity_alone` | exposure 60 | stops in the doorway and says one flat sentence |

Ray's hangs on `activity_alone` **because of that parent's `arousal >= 30` gate** — he only ever
arrives at the worst possible moment, which is the whole difference between him and the other two.
It pays a logged promise outright: *"Ray stopped in the doorway and said nothing… his knowing has to
become content, not stay a stage direction."* Marked `paid_in: 0.1`.

### Two plants paid, one door added

`activity_the_bench` pays the Want's own line — *"her father's weight bench is where the desk was"* —
which had been scenery in six canvases. Three bands: an obstruction, then a thing she has started
using, then the piece of furniture the room is arranged around. And `her_room` had **no locked
rung at all**, so `activity_the_door` became a two-choice surface with *"Take the door off the
hinges"* at nerve 75 — the end of the two-pound-part running line, which until now was a joke with
nothing behind it.

**Verified live:** six standing surfaces render in the room; the door's locked row resolves into a
live choice at nerve 80 and is greyed at 40; every rung applied its declared effects exactly
(Ray: exposure +5, nerve +4, pride −7, his lust +6, relation +3); zero JS errors.

### Tally — gate 1 is down to one sub-check

```
[FAIL] location fill   8 locations · 27,266 words · mean 3,408 · median 3,927 · anchor 35%
       · mean location 3,408 words (need 4,500)
```

**The median check passes for the first time** (3,927 against 3,000) — gate 1 went from three
failing sub-checks to one. Explicit floor **18.1% → 22.4%** of 237 beats, explicit beats 40 → **53**,
locked doors 6 → **7**, anchor 35% and still clear.

⚠️ **Budget rebalance.** Three increments have each landed short of their row (754 + 64 + 573 =
1,391), so the remaining four rooms at their planned targets reach only ~34,600 against the 36,000
the mean needs. The box room goes to **4,700** and the garage to **3,900** to absorb it; that lands
36,016 with the anchor at 26.7% and the median at 4,700. **+8,750 remain.**

---

## 2026-08-11 — v0.1 fill 2/6: the kitchen, and `clamp` had made the rent unpayable

**What.** The kitchen 1,775 → **4,936 words**, and a shipped bug found by the effect diff rather
than by reading anything. Files touched: `games/back_home/toml_phases/3_activities.toml`,
`5_scenes.toml`, the game's `v2_state.json`, and — because the bug is an engine fact the skill never
recorded — `references/engine.md` (new **§21**).

### The bug: every money grant in the game was capped at 100, and the rent is 120

`rung_marek_kitchen_price` declares `money +120`. The live diff said **0 → 100**.

```
v2.py:5753   if (clampFlag === undefined || clampFlag === null) { clampFlag = true; }
v2.py:5754   if (clampFlag) { next = window._traitClamp(next, 0, 100); }
```

`clamp` is a hard **0–100 on every trait**, and it **defaults to true when the key is absent**. All
**ten** money effects in this game carried `clamp = true`. The shop pays 30 a shift and the weekly
rent is 120, so the player could work four shifts, hit the ceiling at 100, and **never once be able
to pay the rent** — the eviction branch was the only reachable outcome of a system the ledger
records as verified end to end.

It is invisible to everything we own: the TOML is valid, the validator passes, the build is green,
all ten gates score the same, and the sidebar shows a plausible number. **Only the live effect diff
against the declared value shows it.** The earlier rent verification missed it because that run set
`money = 200` directly in state and then tested the *deduction*.

Fixed by `clamp = false` on all ten. Verified after rebuild:

| | before | after |
|---|---|---|
| the rent scene, from 0 | 100 | **120** |
| start 12 + four 30-shifts | 100 | **132** |

The rent is payable by working for the first time since `[settings.rent]` shipped.

**Doctrine, new §21:** a trait used as a **quantity** — money, counts — must carry `clamp = false`
on every effect that writes it; meters (nerve, exposure, arousal, energy) want the clamp and keep
it. Would a correct skill have prevented this? Yes — so it is in the engine card, not just the game.

### The kitchen had no triggered layer, in the room named for one

The room is declared *"the crossing point — everyone passes through, nobody stays, so it is where
she is caught in passing"* and shipped three hubs and eight rungs, every one a menu she picks from.
`the-release.md` calls TRIGGERED the main heat engine for a female protagonist, and the room named
for it had none of it.

`triggered_caught_in_passing` is that layer: gated on the **any-NPC** form of `npc_at_location` plus
`worn_corruption >= 4`, so **the wardrobe is what makes it fire** — what she carried downstairs
decides whether the room turns. It binds no NPC, which is both the content (she does not get to pick
who comes through) and the structural guarantee that nothing in it can be mis-attributed.

Verified live: with `sleep_vest` (corruption 2) the surface is absent; with `mothers_slip` (7) it
appears, `getWornCorruption()` reading 7. Its menu steps exposure 10 → 40 → 80, and the locked door
resolves into a live choice at 80 rather than merely un-greying.

Distinct from `triggered_crossing_the_room` on purpose: that one is her crossing into a room one of
them is sitting in; this is the opposite, and it is what *crossing point* means — she is already
here, the kitchen has two doors, and the whole house comes through it one at a time.

### One rung on each ladder, each written to that character's own ceiling

Cal topped out at exposure 15, Dean at 35, Marek at need 25, while the meters band at 55 and 75.

| rung | gate | verified |
|---|---|---|
| `rung_cal_kitchen_late` | nerve 45 + his lust 20 | appears at 45, absent at 20 |
| `rung_dean_kitchen_counter` | exposure 55 + his lust 30 | appears at 55, absent at 40 — fills the band the meter-ceiling gate names |
| `rung_marek_kitchen_price` | need 55 | appears at 55, absent at 30 |

Every effect matched its declaration (Dean: exposure +6, nerve +3, pride −5, his lust +10,
relation +3). Zero JS errors. Also banded the two thinnest rungs in the game —
`rung_cal_breakfast` (120w) and `rung_marek_eat` (146w), each its ladder's always-available presence
floor and each one flat paragraph — and gave the room a solo surface, `activity_kitchen_night`
(23:00–03:00, banded on `need`, deliberately **not** explicit).

**The door belongs to the room, not to a man.** Checking first changed the plan: Cal already owns
nerve 75, Ray need 75, Dean exposure 75 and Marek need 75 elsewhere, so three of the four obvious
choices would have been the same promise twice — and one of them was a ledger promise already made.
*"Stop getting dressed to come down."* hangs on the NPC-less surface instead.

### Two more harness facts

There are **two** per-day ledgers, and clearing one is not enough:
`game_state.trigger_history` keyed by canvas id (`v2.py:4187`) and
`game_state.activity_trigger_history` keyed by canvas **name** (`v2.py:4223`, used when the canvas is
offered as a location action). With only the first cleared, the second probe of a once-per-day
surface reads exactly like a gate that does not work. Also: an NPC-bound hub renders under the
**NPC's** name, not the canvas name — `hub_cal_kitchen` ("Cal (breakfast)") appears as *Cal*.

### Tally

**9/10 holds.** Fill 21,674 → **24,835**. Explicit floor **17.7% → 18.1%** of 221 beats — fourth
increment running that raised it. Explicit beats 35 → 40. Locked doors 5 → 6. Anchor **44% → 39%**,
still clear of 25% and still inside the 36,000–38,400 landing window.

Kitchen came in **64 short** of its 5,000 row; with the bathroom's 754 that is 818 carried.
**+11,172 words remain** across her room, the box room, the garage, the shop and the landing.

---

## 2026-08-11 — v0.1 fill 1/6: the bathroom gets the three quarters of its job it never shipped

**What.** The bathroom 1,954 → **4,746 words** and the room's declared job finally built. Files
touched: `games/back_home/toml_phases/3_activities.toml` (the contention hub plus six triggerless
rungs), `5_scenes.toml` (one rename), and the game's `v2_state.json`. Nothing in the skill's doctrine
changed — this is the first of six fill increments closing gate 1.

### The room was declared for four things and shipped one

`v2_state.json` describes `the_bathroom` as *"the occupancy engine — contention, waiting, walking
in, being walked in on."* What existed was four walk-in substitutions — **being walked in on** — and
a 57-word `bath_occupied` that said the room was busy and sent her back to the landing. Contention,
waiting and walking in had no content at all. The room was named for a machine and shipped the one
part where she does nothing.

`bath_occupied` is now the contention hub: a nerve-banded opener (15/35/55) and a menu. Six rungs
hang off it — wait, knock, walk in on Cal, on Dean, on Ray, and get in with him.

### The hour picks the man; she only picks whether the door opens

The three walk-in choices are gated on `npc_at_location(the_bathroom, npc_X, is_present)` and
nothing else identifies them, so the ladder is the morning queue: Ray 06:30, Cal 07:00, Dean 07:40.
Same click, three different men, three different registers off the Want's per-character ceiling —
Cal borrowing words badly, Dean crude *to* her, Ray one flat sentence that costs more than anything
Dean says all week.

**Verified live, which is the only way this could be checked** — a choice condition is evaluated at
render, so it cannot be read out of the TOML:

| clock | occupant | menu |
|---|---|---|
| Mon 06:45 | `npc_ray` | wait · knock · **walk in on Ray** · locked door |
| Mon 07:20 | `npc_cal` | wait · knock · **walk in on Cal** · locked door |
| Mon 07:50 | `npc_dean` | wait · knock · **walk in on Dean** · **get in with him** · locked door |
| Mon 08:30 | — | hub does not fire |

At `nerve` 0 the menu is *wait* and the locked door only; Cal's rung appears at 25, Dean's at 35,
Ray's at 40, and the shared shower at 55/55. Every rung applied its declared effects exactly
(Cal: nerve +4, exposure +3, pride −3, arousal +25, his lust +8, relation +3). Zero JS errors.

### Two harness facts, both of which faked a broken game

1. **The clock is `game_state.time_state`** — `current_day` as a day *name*, plus `current_hour`
   and `current_minute` (`v2.py:3272-3276`). Setting `game_state.day` / `.hour` writes a field
   nothing reads: every schedule then evaluates as unoccupied and the whole game looks dead. The
   first run of this increment's harness reported an empty presence grid at all five times.
2. **Stop clicking when the passage leaves the canvas.** Advancing blindly to the end of a cascade
   walks on through the exit into the location page and back into the hub, applying a second scene's
   effects. That read as Cal's rung granting +8 nerve against a declared +4 — a doubling that looks
   exactly like an engine bug and is the harness.

Both are the same lesson the Player agent's spec already owed: this is the second increment running
where the only defects found were in the test harness, not the game.

### The lint's one actionable hit, paid

`shift_change_frontroom` → **`rung_dean_shift_change`**, per house convention that a rung's id names
its speaker. Two occurrences, both in `5_scenes.toml`; verified live that the renamed canvas is still
reachable from `hub_dean_late` and still applies its effects. The dialogue-attribution lint drops
**3 → 2**, and the two that remain are `canvas_arrival`, the known-good opening where Ray and Dean
both speak.

### Tally

**9/10 holds.** Fill 18,882 → **21,674**. Explicit floor **15.9% → 17.7%** of 198 beats — the third
consecutive increment where new explicit content *raised* the floor rather than diluting it, which
is `register.md` continuing to hold. Explicit beats 28 → 35, all re-enterable. Locked doors 4 → 5.

⚠️ **The anchor fell 51% → 44% without losing a word**, exactly as `the-board.md:59` says a ratio
gate does. It has room — 25% of the 36,000-word target is 9,000 and it sits at 9,607 — but the
budget only works if the finished total lands in **36,000–38,400**. Above that the front room needs
another instalment.

The room came in **754 short of its 5,500 budget row** and that debt carries rather than being
quietly written off: **+14,333 words remain** across the kitchen, her room, the box room, the
garage, the shop and the landing.

---

## 2026-08-11 — `STATUS.md`: the status doc moves into the skill, and was wrong in four places

**What.** New file `STATUS.md`, moved from `~/.claude/plans/continue-nested-acorn.md` and refreshed
against a live scoreboard run. The plan file is removed; this is now its only home. Nothing else in
the skill changed.

**Why move it.** Plan files live outside the repo and are not git-tracked, so the single most useful
document in the project — the one that catches a reader up on why v2 exists, what the ten gates
measure, and where the test game stands — had no history and could not travel with the skill. It now
sits beside the `CHANGELOG.md` it summarises.

**Why it needed refreshing.** Every number in it was written before Phase 1 and the lint landed. Four
sections had drifted:

| section | said | actually |
|---|---|---|
| Part 3 — file inventory | `gates.py` 524, `engine.md` 403, `CHANGELOG` 792, `SKILL.md` 107 | **605 / 468 / 923 / 111** |
| Part 4 — engine facts | "Eighteen engine facts" | **twenty** (§19 canvas-shadowing, §20 `npc_at_location`) |
| Part 5 — the game | 62 canvases, 14,398 words, 10.8% of 148 beats, mean 1,800 | **66 · 18,882 · 15.9% of 176 · mean 2,360** |
| Part 6 — not done | the lint "worth adding" | **shipped** |

**The one that mattered.** Part 5 said the anchor had fallen to **34%** and was the next thing to
write. Phase 1 had already taken it to **51%**. A reader following that document would have written
the one room that no longer needed it. The satellites are the work — seven of them, ~17,000 words,
listed thinnest-first in the new Part 5.

**Guard added.** The document now opens with a `Last verified` stamp and the two commands that
regenerate its numbers, plus the rule that the scoreboard wins any disagreement. This file went stale
inside a day; a status doc that cannot be checked against a command will do it again.

**Verified.** Numbers taken from `python3 scripts/gates.py back_home` (9/10, location fill the only
failure) and `… vesper` (1/10) run immediately before writing; counts from
`grep -c '^\[\[canvases\]\]'` and `wc -l` on the live files.

---

## 2026-08-11 — `scripts/gates.py`: the dialogue-attribution lint, specced 2026-08-10, now real

**What.** `lint_dialogue_attribution()` plus a `_dialog_blocks()` walker in
`scripts/gates.py`, reported below the tally and **never scored**. A warning that can move a
gate is a gate, and a gate has to be re-derivable from a measurement.

Flags any `dialog` block whose `npcId` names a character the canvas neither **binds**
(`npc` / `requires_npc`) nor **names in its id**. It walks into cascades and groups, so it sees
the dialogue that only exists three levels down inside a `beats` array.

**Results, measured:**

| game | hits |
|---|---|
| `back_home` | **3** |
| `vesper` | **28** |

**The spec said 2, and 2 was right when it was written.** Of today's three: two are
`canvas_arrival`, the known-good opening where Ray and Dean both speak — exactly the pair the
original measurement found. The third is `shift_change_frontroom`, which **this project
introduced yesterday** in the Phase-1 anchor increment. It renders correctly (verified live —
only `Dean` appears), but it is a triggerless rung whose id does not name its speaker, so it is
precisely the shape the lint exists to surface. The house convention would call it
`rung_dean_shift_change`; that rename is the cheap fix and is left for the next pass rather than
smuggled into a tooling commit.

**One hit per canvas + speaker, not per line.** The first cut counted blocks and returned 7 on
`back_home` and 200+ on `vesper` — unusable. A canvas that renders the wrong name renders it
wrong on *every* line it speaks, so a per-line count measures how talkative a scene is rather
than how many defects exist. The per-canvas count is the defect count; `lines` is carried in the
JSON for anyone who wants the volume.

**Vesper's 28 are not noise.** They cluster on `cell_*` canvases speaking as `npc_bastien` —
the same character the standing-surface gate already fails it for: referenced everywhere,
findable nowhere. Two independent checks landing on one character is the useful kind of
agreement.

`--json` output is now `{"gates": [...], "lints": {...}}` rather than a bare gate array.
**Anything parsing the old top-level list needs updating.**

**Verified.** `back_home` still reports 9/10 and `vesper` its existing score — the lint changed
no gate, which is the property that matters most about it.

---

## 2026-08-11 — v0.1 Phase 1: the anchor, 5,123 → 9,607, and three engine facts it cost

**What.** The front room taken from 5,123 words to 9,607 in one pass — the anchor budgeted
against the *finished* 36,000-word total (where it owes ~9,000) rather than the current one,
because the ratio tightens every time any other room grows and topping it up later means
writing it twice. Files touched: `games/back_home/toml_phases/5_scenes.toml` and
`3_activities.toml`, plus `references/engine.md`, `SKILL.md` and the game's `v2_state.json`.

Gate 1 still fails, as expected and as planned — mean 2,360 against 4,500, median 1,496 against
3,000. It closes when the seven satellites are filled. What this bought is the right to fill
them without the anchor sliding under 25% on the way.

### The register rule was written from this game's own failures and never applied to it

`references/register.md` quotes, as pivot target #3, the sentence *"…and the arithmetic does not
come out the way it is supposed to."* That sentence was still sitting at the end of
`loop_ray_arrangement`, and the beat carrying it scored **zero**. Measured per beat, all three
repeatable sex loops failed the same way in the same place — their *tails*:

| | beat 1 | beat 2 | beat 3 | beat 4 |
|---|---|---|---|---|
| `loop_ray_arrangement` | 4 | 1 | **0** | 0 |
| `loop_dean_late` | 3 | 1 | **0** | **0** |
| `loop_cal_sex` | 4 | 3 | **0** | 0 |

Every loop opened explicit and then left the body exactly when the act got closest. The fix was
the one the doctrine already prescribes — keep the camera on the body to the last sentence, and
give the interiority its own beat *after* — and it moved the whole game **10.8% → 15.9%** of
beats at 3+ explicit words, without one gratuitous noun.

**Two words worth knowing are NOT on the frozen list:** `wet` and `come` (the latter excluded
deliberately, since it matches "come downstairs"). Three finishing beats rewritten to be
relentlessly physical still scored 2, because they leaned on both. The list is the instrument;
write to the body and check the number.

### Three engine facts, each caught by a build that refused to run

1. **The documented build command was wrong** — in `SKILL.md` *and* `references/engine.md`.
   `package_from_toml` takes named, required `--file` and `--output`; the positional-plus-
   `--output-dir` form both files carried exits 2 and builds nothing. `python` may not be on the
   path either. Both files corrected. A skill that cannot build the game it authored is a broken
   skill, and this had been shipped since the first release.
2. **Move a flag setter — never duplicate it.** `cal_arrangement` was set on the located hub
   choice *and* left on the triggerless loop. The validator resolved it to the one without a
   location and hard-failed with `MISSING HINT`, naming the loop's canvas name (`Take him
   upstairs`), which reads exactly like the hub choice of the same wording. §16 sharpened.
3. **One repeatable canvas per location + NPC + time window.** The two-men scene was written as
   a located canvas and the build warned that `hub_dean_late` already owned `npc_dean` at the
   front room. It is a *warning*, not an error — a canvas shadowed this way looks correct in
   TOML and is unreachable in play. New §19; treat the warning as an error.

### `npc_at_location` promoted from "known" to "verified live" (new §20)

`generators/v2.py:4131-4145` and `:7791`. **`npc_id` is optional — omit it and the predicate
tests whether the room is occupied by anybody.** Confirmed in the built game rather than read:
the two-men choice rendered at 23:10, where Ray's 20:00–23:30 row overlaps Dean's 23:00–01:30,
and was gone at 23:45 with identical player state.

That single fact carried the increment's two new content kinds. Conditions on a *choice* are
evaluated live at render, so the scene the engine refused as a canvas works better as a rung on
the existing hub. And the any-NPC form let the TRIGGERED piece — she crosses the room in what
she sleeps in and does not look to see which of them is in the chair — bind **no NPC at all**,
which is both the content and a structural guarantee that no dialogue can be mis-attributed.

### Live-testing this engine, for whoever writes the next harness

Static parsing cannot see a passage that errors. Three things about the built game are not what
a reasonable person would guess, and each cost a run:

- `State` and `Engine` are **not** bare globals. Use `SugarCube.State`, `SugarCube.Engine`,
  `SugarCube.setup`.
- `$flags` is an **object** keyed by flag name, not an array. `.includes` throws.
- Player traits live at `player.core_traits`, not `player.traits`.

All fourteen new or rewritten passages then rendered clean: no JS errors, every cascade
advancing, and no speaker outside the four declared characters.

**9/10 holds.** Nothing else moved: explicit-in-repeatable 100%, standing surface 4/4,
milestones 4/4, meter ceiling clean, four locked doors still shut. Three new promises logged
(Dean's uncharged version, Ray's knowing, Cal's £840). The stray `Wren-solo` labels — Vesper's
protagonist used as a pattern name in a game about June — are gone.

**+17,100 remain**, all of it in the seven satellites.

---

## 2026-08-10 — v0.1 increment 2e-4: the box room and the shop, and a bug in my own prose

**What.** Box room 908 → 1,228, shop 76 → 654. Two new promises logged.

### The bug, and the structural reason behind it

Hannah Beckett — a woman June sat next to for two years, walking into the shop — was written as
a `dialog` block attributed to **`npcId = "npc_marek"`**, because she is a walk-on with no NPC
record. It would have rendered **"Marek:"** over her line in the built game.

Fixed by making it quoted prose. But the interesting part is *why it can't be fixed the obvious
way*: declaring Hannah as an `[[npcs]]` entry would immediately **break gate 6**, which requires
every declared character to have a standing surface and a schedule row.

**The gate is right.** A character with a name and no way to find them is exactly the defect it
exists to catch — Vesper's `npc_bastien`, referenced 88 times and reachable nowhere. So
**one-scene characters are narrated, never declared.** That is a real constraint the gate
imposes on authoring, and it is a good one.

### A lint worth adding to `gates.py`

> Flag any `dialog` block whose `npcId` names a character the canvas neither **binds**
> (`npc` / `requires_npc`) nor **names in its id**.

Run over `back_home` it returns exactly **2** hits — both `canvas_arrival`, which legitimately
has Ray and Dean speaking in the opening — and it **would have caught the Hannah bug**.

The naive version (flag dialogue on any unbound canvas) returns **30 false positives**, because
every triggerless rung is unbound by design and correctly carries its own character's voice.
Worth noting how much narrower the useful check is than the obvious one.

### The shop is the mirror

The regulars are banded on `pride`, so the same six hours read as humiliation, then as rest,
then as camouflage. And `canvas_someone_who_knew` is the reversal made visible **from outside the
house** — the only vantage it can be seen from. From out there the story is short and finished:
*June went, June came back, June is at the shop.* The house is the only part still moving.

**9/10 held.** Fill 12,496 → 13,394. Explicit floor 10.1% → **9.6%**, an expected dip: this was
deliberately the least explicit increment in the game, because the shop is the one room where no
man wants anything from her and that is its entire function. Still comfortably above 7.5%.

⚠️ **Anchor at 34% and drifting down** — the trap from last increment is live. The front room
needs its next instalment before much more is written elsewhere.

**+22,606 remain.**

---

## 2026-08-10 — v0.1 increment 2e-3b: the anchor trap, and the last empty schedule row

**What.** The garage (309 → 801) and an anchor instalment on the front room (4,020 → 4,556).
Added the fill-in-step rule to `references/the-board.md` and corrected §16 of
`references/engine.md`.

### The anchor trap — a ratio gate tightens while you work elsewhere

Gate 1 wants the anchor at **≥25% of all location prose**. That is a ratio, so every word written
anywhere else lowers it. The front room sat at 4,020 through six increments of building other
rooms, and its share fell **53% → 46% → 40% → 39% → 35%** without a single word being removed.

Held there, it crosses below 25% **within one more increment** — the game going 9/10 → 8/10
while getting objectively better.

**Budget the anchor against the finished total, not the current one.** At a 36,000-word target
the anchor owes 9,000, so its share is planned into every increment rather than topped up at the
end. Now doctrine in `the-board.md`.

### The flag-chain rule was recorded too narrowly

Hit it a second time with `ray_arrangement`:

```
✗ ray_arrangement   required by choice 'Sit with him after.',
                    set by 'Stop pretending it's a favour' but no location/schedule
```

The validator refuses a flag set in a triggerless rung when it is read by a **choice**, not only
by a trigger. Same fix both times — move the `flagEffects` up onto the located hub choice.
`engine.md` §16 now reads "a TRIGGER **or a CHOICE**".

### The last empty schedule row is filled

Dean was present in the garage 14:00–17:00 at weekends with **zero content** — the only scheduled
row in the game with nothing on it. Verified live at Saturday 15:00. He now carries three
surfaces. The scene is the one version of him with no audience: *he cannot do the funny voice
under a bar*, so between the fourth and fifth rep he is straightforward for the first time since
they were children.

### Scope honesty

The plan named three targets and this increment hit two. **The box room was not touched** and
remains at 908; it carries into the next increment rather than being quietly dropped.

**9/10 held.** Fill 11,468 → 12,496; anchor back to **36%**; explicit floor **10.0% → 10.1%** —
the second consecutive increment where new content raised it rather than diluting it, which is
`register.md` continuing to hold. **+23,504 remain.**

---

## 2026-08-10 — `references/register.md`, and the first increment that RAISED the explicit floor

**What.** Wrote the skill's missing prose doctrine, then authored the kitchen against it. Kitchen
698 → 1,775. Linked from `SKILL.md`'s operating rules.

### The gap

Checking why the same defect had recurred three times explained it: **the skill said *where* the
crude register lives and *which words* were permitted, and nothing at all about how to write the
beat.** There was no prose reference. The Want template's §6 is entirely placement and vocabulary
ceilings.

### The rule, and its test

> **An explicit beat stays on the body for its whole length.**
> **Diagnostic:** if the beat's last sentence is about what it *means* rather than what is
> *happening*, it has pivoted and will score 0–1.

`register.md` names the three pivot targets — *he knows* / *she is ashamed* / *what this says
about her* — so they are catchable while writing, and puts the interiority in **its own beat,
after**. Cascade beats are free, so splitting costs nothing and sacrifices none of the
psychology, which is the part that makes the game good.

It also states what the fix is **not**: not word-stuffing, and not loosening the frozen wordlist.
The list has been challenged twice and was right both times.

**The test:** doctrine written first, kitchen authored against it, gate run after.

| | before | after |
|---|---|---|
| beats | 106 | **120** (+14) |
| explicit beats | 10 | **12** |
| explicit floor | 9.4% | **10.0% — up** |

**For four consecutive increments new content dropped the floor and had to be rewritten after the
gate caught it. This time it went up, on the doctrine's first use.** That is the strongest
evidence in this project that a written rule can actually change what gets authored — but only
once the rule says *how*, not merely *where*.

### The kitchen

Four surfaces against the schedule already built: Cal 07:40–08:00 (twenty minutes, cannot look at
her, and the mugs are on the shelf above his head), Dean 08:00–09:00 (down from the bathroom she
watched him in — the entire scene is the not-mentioning), Marek 16:00–17:30 (the only hour the
two of them are the only adults in the house, and the only meal anybody eats sitting down). Marek
and Cal now carry two surfaces each.

**9/10 held.** Fill 10,391 → 11,468; median 1,367 → 1,496. **+24,532 remain.**

---

## 2026-08-10 — v0.1 increment 2e-2: the morning queue, and the register defect is *mine*

**What.** Dean given a bathroom row; two new peeps; two new walk-ins; the wall paid off. Bathroom
845 → 1,517, landing 681 → 1,367.

### The finding that matters more than the content

The new scenes added **sixteen beats and zero explicit ones.** Every one scored 0 or 1 against
the 3-word floor, dropping the game to exactly **7.5%** — the boundary.

The pattern is identical every time: **name a body part once, then pivot the next beat to
psychology** — he knows, her face is burning, what it means. The heat sits in the situation and
never in the words.

This is the defect diagnosed in Vesper, reproduced by the author who wrote the doctrine against
it, **for the third time — twice after writing it.** That is the actual finding:

> **It is not a lapse. It is a default that reasserts itself the moment it is not being actively
> fought, and the gate is the only thing that catches it.**

**The fix is not word-stuffing.** It is to stay on the body *through* the beat rather than
referencing it once and moving on. Eleven targeted rewrites took the floor **7.5% → 9.4%**,
which sits at the *top* of the reference game's measured 7.5–9.3% band rather than scraping it.

### The morning queue

Dean had **no bathroom row at all**, so he could neither be peeped nor walk in on anything.
Adding 07:40–08:00 weekdays makes the grid step cleanly — verified live:

```
06:45  ['npc_ray']    07:20  ['npc_cal']    07:50  ['npc_dean']    08:30  []
```

Three men through one bathroom in ninety minutes. Each of the four peeps is offered only while
its own man is in its own room, including Marek's box-room peep — which needed no new schedule
row, because his door was already established as half open.

### Planted facts, paid

All three night-one details now carry content: the gap down the hinge side (four peeps), the
extractor that makes her deaf (three walk-ins on `activity_wash`'s substitutions at rising
`exposure`), and the eighteen-inch wall (`activity_the_wall`, banded on `nerve` — at the bottom
she is trying not to hear it, at the top she is timing herself to it).

### Tally

**9/10 held.** Fill 8,752 → 10,391; median 845 → 1,367. **+25,609 remain.**

Play-test friction now stands at **four false alarms from page-text assertions and zero real
bugs found by them** — this time a filter that searched for "gap" and "forty" against a canvas
named *"Cal takes his time."* Every real defect this session came from asserting on
`SugarCube.State.variables`. The Player agent's spec should forbid text assertions outright.

---

## 2026-08-10 — v0.1 increment 2e (part 1): the wardrobe, and a silent-failure class

**What.** A 9-item `[[clothing]]` catalog, and her room built out from 68 words — the boxes,
the dressing scene, the door that does not shut, and the solo surface. Added §17 to
`references/engine.md`.

**The most dangerous failure class this project has hit.** To grant the two garments I wrote:

```toml
clothingEffects = [ { itemId = "mothers_slip", op = "grant" } ]
```

The TOML parsed. The validator passed. **The build went green and nothing was ever granted** —
the top tier of the wardrobe would have been permanently unreachable, with no error anywhere in
the pipeline. The real key is `wardrobeEffects = [{ action = "add", item_id = "…" }]` on
`exit_block.config`.

**Nothing catches an invented key.** Not the parser, not the validator, not the build, not the
gates. The only defence is to grep `template_import.py` for any key not personally seen in a
shipped game — zero hits means it does not exist, however plausible it looks. That rule is now
in the engine card.

**The wardrobe is real, not decorative** — the plan's decisive check, and it passes. Verified
live: seven initial garments equip at start; the boxes grant `mothers_sundress` and
`mothers_slip`; equipping the slip moved **`worn_corruption` 2 → 7**; and the dressing scene
rendered its tier-3 band in response.

`worn_corruption` is a **MAX aggregate, not a sum** — one loaded garment sets the reading on its
own. So a catalog does not need to be large to reach a tier; it needs one item per tier. That
makes clothing a genuine gate source for `exposure` rather than a UI ornament.

**Her room** went 68 → 1,215 words, and its four surfaces are all *standing* — which is where
the crude register belongs. The room's thesis is the broken catch: the same action reads as
three different decisions as `exposure` climbs, ending at *"It is a two-pound part. You know
exactly where the hardware shop is."*

**Gates: 9/10 held.** Fill 7,605 → 8,752. Explicit floor 8.9% across 90 beats — still clear as
the denominator grows. **+27,248 words remain** for the last gate.

---

## 2026-08-10 — v0.1 increment 2d: Marek. **9 of 10 gates pass**

**What.** Marek's hub and three rungs added to `5_scenes.toml`. Six open promises logged in
`v2_state.json`.

**The rotating slot is proven.** He is the premise's structural answer to never-ending: Ray
rents the box room to cover the shortfall, so every few releases a new stranger lives in the
house — **a new character at an existing location**, which is the measured release shape built
into the fiction rather than bolted onto it. Replacing him next release should touch only his
`[[npcs]]` entry and his block in `5_scenes.toml`, and nothing about the world.

His window is deliberate: **09:00–16:00, when the house is empty.** The one slot no family
member competes for, and the reason his ladder needs no privacy management at all. He also
carries the only register in the game that is transactional from the first line — no build, no
history, no ceiling to break — which is what makes him legible against three men she is
related to.

**Verified live.** Present in the box room at Tuesday 11:00; all three rungs render with the
fourth locked; the explicit rung applied money 0→50, need 40→45, exposure 60→64, pride 100→94,
his lust 0→8, `marek_arrangement` set. Zero JS errors.

**Gates: 9/10.**

| | |
|---|---|
| standing surface | **4/4** — every character findable and scheduled |
| traversal heat | **5/8 (62%)** — over the 60% floor |
| meter ceiling | clear — every band boundary now buys something |
| ends on an opening | **4** locked rungs |
| ascent tiers | all three gated — nerve 4+, exposure 6+, need 7+ |
| explicit floor | 9.9% across 81 beats |

**The one remaining failure is location fill** — 7,605 words against ~34,000, median 698
against 3,000, mean 951 against 4,500. No location is empty any more; this is not a design
problem, it is the writing a first release costs.

**Six promises logged.** Marek leaving in spring (the slot must be *refilled*, not left empty),
the `keep_unpaid` line *"we'll sort it another way"*, and the four locked 75-rungs. Each is now
tracked and must be paid or explicitly cut — the measured failure mode is a character dangled
for years while players ask *"are we EVER going to…"*.

---

## 2026-08-10 — v0.1 increment 2c: Dean. 6/10 → 7/10, and a build-breaking engine rule

**What.** Dean's two hubs and five rungs added to `5_scenes.toml` — the kitchen at 08:00 (verbal,
daylight) and the front room at 23:00–01:30 (dark, physical). Same man, two registers. Added §16
to `references/engine.md`.

**An engine rule that hard-fails the build, learned by hitting it.**

```
❌ Flag Chain Validation Failed:
   ✗ dean_open
     Required by: Dean (late)
     Issue: MISSING HINT - set by 'Come down in what you slept in' but no location/schedule
```

**A flag read by a TRIGGER must be set from a canvas that has a location.** A triggerless rung
has none, so the game cannot tell the player where to go and earn it. The fix is to move the
`flagEffects` onto the **hub choice** that opens the rung — the choice lives on a located
canvas, the semantics are identical, and the chain resolves. Flags that nothing reads in a
trigger are unaffected.

This is the fourth build-breaking convention found by authoring rather than by reading, after
the section-syntax requirement, the positive-decay rule and the children-only navigation order.

**Verified live on both surfaces.** Kitchen hub appears at Monday 08:30. Front-room hub appears
at Monday 00:30 with `getNpcsAtLocation('the_front_room')` returning `['npc_dean']` — **the
overnight-wrap row holds in live presence, not just in a schedule dump.** That is the first
end-to-end proof of the midnight-wrap finding; until now it had only been read out of the
source and seen in a schedule listing. The late loop applied dean lust 30→38, relation 0→3,
player exposure 40→45, nerve 0→4, pride 100→96. Zero JS errors.

**`meter ceiling` now PASSES.** Exposure gates at 15 (Ray's garage), 35 (Dean's kitchen morning)
and 75 (Dean's locked late rung) fill the bands the gate had been naming as empty promises.
Marek takes 55.

**Gates: 7/10.** Three fails left, and they are three views of one thing — Marek is unbuilt
(standing surface 3/4), his box room is the last empty location (traversal heat 4/8), and
location fill is at 6,697 of ~34,000. Explicit floor holds at 9.9% across 71 beats even as the
denominator triples, which is the floor doing its job rather than drifting.

---

## 2026-08-10 — v0.1 increment 2b: Ray, and the keep. The `need` tier gets an engine

**What.** Added `[settings.rent]` to `0_systems_spec.toml` and Ray's two hubs plus five rungs to
`5_scenes.toml`. Corrected the meter-ceiling gate in `scripts/gates.py`.

**The `need` tier had no engine, and the platform already ships one.** She could earn at the
shop but nothing ever demanded money, so "what she'll trade for" had nothing to bite on.
`[settings.rent]` (`apps/projects/services/template_import.py:2564-2573`) is a first-class
recurring demand with `amount`, `due_day`, `collector_npc`, `grace_periods` and an eviction
mode. It is also **exactly the mechanic the reference game's seed uses** — its `loc-home` file
carries authored `Rent Intro` / `Rent Pay` / `Rent Refuse` / `Rent Fight` passages.

Tuned to bite: **120/week against a shop paying 30/shift** is four shifts — most of her week,
survivable, and one bad week forces the ask. Ray collects, which makes the demand a father
invoicing his stepdaughter, and neither of them has anywhere to put that.

**`eviction_mode = "flag_set"`, not the default `"game_end"`.** A product that never ends must
not ship a lose-state that stops play. **Verified live, end to end:**

| | result |
|---|---|
| pay | money 200 → 80, exactly 120 deducted |
| first miss | `warnings` 0 → 1, grace consumed, authored warning prose |
| second miss | `keep_unpaid` set, soft-eviction prose, **game continues** — still playable, back at `Location_her_room` |

The engine's own fallback line for this mode is *"You're still here. But the terms have
changed."* Zero JS errors.

**Gate corrected — meter ceiling.** Once top bands were correctly left unbounded, the old check
read the *second* band's `max` as the ceiling and produced nonsense ("exposure shown up to 74").
The truer semantic: **every band boundary is a promise** — a meter showing 15/35/55/75 tells the
player something is different at each. The gate now compares the highest authored gate against
the **top band's `min`** and names the empty bands:

> `exposure: bands promise something at 35/55/75, but the highest authored gate is 15`

Vesper unchanged at 1/10 (its `hygiene` finding now reads more clearly for the same reason).

**Gates: 6/10.** `ascent tiers expand the world` now **passes** — all three declared tiers have
gated content for the first time (`nerve` 4+, `exposure` 1+, `need` 4+), which was the design
gap Ray existed to close. `ends on an opening` is up to 2 locked rungs. Remaining: location fill
(5,436 of ~34,000), traversal heat 3/8, standing surface 2/4, and the exposure bands above —
all of which Dean and Marek carry.

**Authorial note recorded rather than ruled on.** Ray's top rung **omits** `locked_text`, so the
greyed row shows the action — *"Ask him for it in front of the others"* — a want the player can
name. Cal's shows the reason instead. Both are in the build deliberately; compare them and pick
one house style before ship.

---

## 2026-08-10 — v0.1 increment 2a: Cal's ladder. 4/8 → 6/10 gates, all ten now judged

**What.** Authored `games/back_home/toml_phases/5_scenes.toml` — the first standing hub and its
full rung ladder (talk → let him look → contact → the explicit loop → a locked top rung).
Merged, built, live-played. Added §13–§15 to `references/engine.md`.

**Cal's ladder verified live.** The hub appears at `the_front_room` only inside his 16:00–19:30
weekday rows (`requires_npc` doing the presence work, no hub schedule needed). At `nerve` 60 /
his `lust` 35 all four rungs render, and clicking *Sit closer* moved **cal lust 35→41,
relation 0→2, player nerve 60→63, exposure 0→2, pride 100→98** — exactly the declared effects,
zero JS errors. The fifth rung rendered as `SPAN.locked-choice`, so gate 9 is real and the
release has a visible door.

**Three engine facts learned, all by breaking something.**

1. **Exit blocks must use SECTION syntax** — `[canvases.nodes.exit_block]` plus
   `[[canvases.nodes.exit_block.choices]]`. A multi-line inline table is a TOML parse error and
   a conditional choice list is unavoidably multi-line. The shipped game does this 199 times; I
   wrote it inline and the merge failed. `conditions = { … items = [ … ] }` *may* span lines
   because newlines are legal inside an array — two levels of nesting is where it breaks.
2. **Third instance of the key-asymmetry trap.** Conditions say `trait_key` / `npc_id`; effects
   say `trait` / `npcId`. Same concept, different key, silent when wrong.
3. **`locked_text` REPLACES the action label**, it does not annotate it. Recorded as an
   authorial trade-off rather than a rule: showing the action names a *want* the player can
   chase, which is what sells the next release; showing the reason is clearer about the gate but
   weaker as a door.

**The meter-ceiling gate caught a real lie.** `nerve` displayed a 75–100 top band while the
highest authored gate was 75 — the top 25 points bought nothing and the sidebar was promising
content that did not exist. Fixed by making the top band **unbounded** (`min = 75`, no `max`) on
all three tiers, which is honest and which the gate correctly skips as promising nothing.

**Gates: 6/10, and no gate is n/a any more** — every one now has something to judge. Passing:
explicit floor 13.2%, explicit in repeatable 100%, media pools, milestones, meter ceiling, ends
on an opening. Remaining four are all unbuilt work: location fill (3,795 of ~34,000 words),
traversal heat 2/8, standing surface 1/4, and `exposure` / `need` have no gated content yet
because Cal's ladder gates only on `nerve`. Ray carries `need`, Dean and Marek carry `exposure`.

**Anchor discipline held without intervention** — `the_front_room` is back to 56% once Cal's
2,125 words landed, against a 25% floor.

---

## 2026-08-10 — v0.1 increment 1: the daily loop and the bathroom. 0/4 → 4/8 gates

**What.** Authored `games/back_home/toml_phases/3_activities.toml` — the solo loop (sleep, wash,
shift, and a pass-time evening) plus the bathroom's triggered layer (occupancy, two peeps, a
walk-in). Merged, built, and live-played the lot.

**Doctrine finding — the build order flips, and this belongs in `references/the-release.md`.**
Gate 2 wants ≥7.5% of beats explicit, but `nerve` / `exposure` / `need` all start at **0**. A
standing seduction ladder at tier 0 is absurd. The reference game resolves this the same way:
its early heat is not chosen by the player at all — her promiscuity sits at zero while the world
still acts on her.

> **The TRIGGERED layer carries the explicit floor while every tier is still cold. The STANDING
> ladder stays cold until she has climbed it.** So the triggered layer is built *first*, not
> third.

**The gate caught the author.** The first draft of the peep and walk-in scenes scored **0.0%**
on the explicit floor *despite being explicit content*, because the prose named the act
obliquely — "hard", "comes", "finishes" — instead of naming bodies. That is precisely the defect
diagnosed in the previous game, reproduced by me, one increment after writing the doctrine
against it.

Rewriting seven beats in a crude register moved the floor **0.0% → 12.0%** and flipped **three
gates** in one pass. The wordlist was **not** loosened to accommodate the prose: "come" would
match "come downstairs" everywhere, so its exclusion is correct and the writing was the thing at
fault.

**Two bugs only live play could find. Neither is visible to any static check.**

1. **Soft-lock.** The opening lands at 17:18; sleep was gated 21:00+; the shift needs the shop;
   and **navigation does not advance the clock**. Every scheduled window in the game was
   unreachable, forever. Fixed with `activity_evening` at the front room (+90 min) — which also
   feeds the anchor's word count — plus widening sleep to 20:00.
2. **Cold start.** Ray and Cal used the bathroom on weekdays only, and the game started Friday
   evening, so the core mechanic was dead until Monday — three in-game days. That was mechanical
   scheduling rather than fiction: people wash at weekends. Added weekend rows (Ray 09:30–10:15,
   Cal 11:00–11:50) and moved the start to Sunday so Monday morning is day 2.

**`npc_at_location` verified end to end.** At Monday 06:48,
`SugarCube.setup.getNpcsAtLocation('the_bathroom')` returns `['npc_ray']`; the landing offers
*"The gap in the door"* only while he is in there; entering applies all four effects
(`nerve` 0→3, `exposure` 6→10, `pride` 100→97, `arousal` 0→20), with zero JS errors.

**Engine fact learned:** a **repeatable** canvas at a location renders as a *clickable action*,
not an auto-fire — auto-fire is for non-repeatable priority canvases. My harness matched the
canvas title in a link and reported the scene as "fired" when it had never been entered. Also
`setup` is not a page global; it is `SugarCube.setup`.

**Gates: 4/8 judged pass (2 n/a), up from 0/4.** Passing: explicit floor 11.5%, explicit in
repeatable 100%, media pools clean, milestones 2/2. Remaining failures are all unbuilt work —
location fill (2,284 of ~36,000 words), traversal heat, standing surfaces, and no locked door
yet. All four land with the hubs in increment 2.

**Running tally of play-test friction:** three wrong selectors, one false-positive "fired"
check, one silent click failure that corrupted a walk, and two engine conventions learned the
hard way. Every one of these is a fact a reusable Player agent would hold and an ad-hoc script
does not. This is the strongest evidence yet for what Part C should build first.

---

## 2026-08-10 — `back_home` builds and plays; four engine facts learned from doing it

**What.** Authored `toml_phases/2_one_shots.toml` (the arrival chain + the first night), merged,
built, and **live-played the result headlessly**. Added §10–§12 to `references/engine.md`.

**It builds and it runs.** `package_from_toml … --gen-version v2 --debug` produces a 908KB
`index.html` with 32 compiled passages. A Playwright walk through the age gate, the four-node
opening and into the bathroom confirms:

- opening chain plays end to end; `arrival_done` set; player lands at `her_room`
- the first-night canvas **auto-fires on entering the bathroom**, correctly gated on
  `arrival_done is_true` + `first_night_done is_false`
- cascade beats advance; `exposure` moves **0 → 6**; `first_night_done` set
- **zero JS errors** throughout

Only warning is 4 uncopied media files — expected, `find-media` has not run.

**Four engine facts learned by doing, now in `engine.md` with citations.** Three of them broke
the build or the test first:

1. **`navigation_order` lists CHILDREN only.** The validator rejects listing the parent. The
   return link is generated from `entry_from` and renders as **`Leave <Location Name>`** — so a
   leaf room with `navigation_order = []` is not a dead end. I diagnosed `her_room` as a dead
   end before looking at the DOM; it was fine.
2. **`trait_decay` values must be positive magnitudes.** `hygiene = -10` is rejected with
   *"must be >= 0"*.
3. **`customizable = true` requires `[[player.customization_fields]]`.** Deferred to `false`
   for v0.1 and logged.
4. **`Start` is an age gate, not the game.** The starting canvas is reached through
   `[[✓ I am 18 or older…]]`, and `player.current_location` is `""` until then. Also: rendered
   links are `a.link-internal` inside `#story` — a bare `text=` selector matches the embedded
   `<tw-passagedata>` source and resolves to an invisible element.

**Process note worth keeping.** Facts 1 and 4 both made me *misdiagnose a working game as
broken*, and I rewrote the play-test selector three times before reading the DOM. That is the
argument for the Player being a **reusable agent with the engine's conventions baked in**
rather than an ad-hoc script rewritten per session — and it is the first concrete piece of
evidence for what Part C should build, produced exactly as intended by using the skill for real
rather than reasoning about it.

**Current state of `back_home`:** 885 words, 10 beats, 2 canvases. Gate 1 reads
`mean 111 · median 0 · anchor the_front_room 53%` — the anchor share is real but everything
else is the expected debt of a world with one scene in it.

---

## 2026-08-10 — first real use: `back_home`, and the scoreboard flattered an empty game

**What.** Ran the skill against a real game for the first time. Authored
`games/back_home/the_want.md`, `toml_phases/0_systems_spec.toml`,
`toml_phases/1_metadata_and_locations.toml` and `v2_state.json` — the Want and the Board for an
incest / female-protagonist premise. Then fixed a bug the run exposed in `scripts/gates.py`.

**The bug.** On a Board with no content authored yet, the scoreboard reported **3 of 10 gates
passing**. All three passed *vacuously*: "0 of 0 milestones open standing content", "0 pooled,
0 fixed single-clip", "0 visible meters rise past their content". An absence is not a pass, and
a stick that flatters an empty world is worse than no stick.

`gate()` now takes three states — `True` / `False` / `None`, where `None` means *there was
nothing to judge*. Those report as `n/a`, are excluded from the tally, and never count as a
pass. Six gates are legitimately n/a at Board stage. The same Board now reads **0/4 judged
gates pass (6 n/a)**, which is the truth.

Vesper is unaffected (it has content everywhere, 0 n/a) and holds at **1/10**.

**What the Board proved works.**
- The merge produced a clean 16,894-byte game from two phase files; `tomli` parses it.
- All 11 schedule rows bound to the correct NPC — no silent re-parenting across the
  `[[npcs]]` / `[[npcs.schedules]]` boundary.
- Dean's `23:00–01:30` row survived as **one row**, confirming the overnight-wrap finding
  rather than relying on it.
- Gate 10 printed `[declared]` and judged `nerve` / `exposure` / `need` **by name**, reading
  `board.ascent_tiers` out of `v2_state.json`. The ledger→gate wiring works end to end.

**Design decisions logged in `v2_state.json`,** with their costs:
- The house is **rooms, not one location** — presence and occupancy are per-location, so
  room-level co-location only exists if rooms are locations. Cost: eight locations to fill.
- `the_landing` exists to be the **vantage** the bathroom is peeped from
  (`npc_at_location`, `generators/v2.py:3480`, `:4131-4146`). It is a corridor and is expected
  to stay thin.
- Anchor is `the_front_room`, not `the_bathroom`. The bathroom generates the most *charged*
  beats but they are short; the front room hosts the evening rotation. Gate 1 also wants an
  anchor the player can re-enter — the measured failure case had a 29% anchor inside a sealed
  room.
- **The rotating lodger** (`npc_marek`, `the_box_room`) is the premise's answer to
  never-ending: a new character at an *existing* location every few releases, which is the
  measured release shape built into the fiction rather than bolted on. He works nights, so he
  is home alone with her while the house is empty — a window no family member competes for.
- Family is written as family and **labelled step-**, per the distribution evidence. Open risk
  recorded: Patreon's own terms are not in our research, and Patreon is the money.

**Engine limit that shaped the cast.** `requires_npc` is a single string
(`apps/projects/services/template_import.py:606`) and portraits render one card per NPC
(`generators/v2.py:4939`), so **two interactive family members cannot share a scene**. Every
scene is her plus exactly one of them; a second body can be narrated in and flag-gated. This is
recorded in the Board file itself so it constrains authoring rather than being rediscovered.

---

## 2026-08-10 — gate 1 was wrong: location fill is a distribution, not a floor

**What.** Replaced gate 1 in `scripts/gates.py` and propagated the correction through
`SKILL.md`, `references/the-board.md`, `references/the-release.md`, `references/state.md` and
`templates/board.toml`.

**The error.** Gate 1 demanded **≥10,000 words in every location**, from a "10,187 words per
location" figure. That figure was computed as *total words ÷ locations* — and the numerator
included `base-combat` and `base-system`, which are engine code, not location prose.

Measured on location prose only, the reference game's seed is **116,540 words across 25
locations: mean 4,661, median 3,154, min 302 (bus station), max 35,218 (school)**. So **24 of
its 25 locations fall under 10,000 words**. The exemplar failed its own derived gate 24 times
out of 25. Its current build still has 23 of 61 locations under 10,000.

**The real shape** is one or two deep **anchors** plus many legitimately thin satellites —
`school` alone held **30.2%** of all location prose at seed. Gate 1 now checks three things:

| check | threshold | seed evidence |
|---|---|---|
| anchor share | ≥25% of location prose in one location | school = 30.2% |
| median location | ≥3,000 words | 3,154 |
| mean location | ≥4,500 words | 4,661 |

plus a report of every declared location with nothing placed in it.

**Discrimination test — the bar set for any format or threshold — passes.** The corrected gate
clears the proven world (30.2% / 3,154 / 4,662) and still condemns the measured failure
(Vesper: median 674, mean 1,466, five empty rooms). A gate that could not separate those two
would be worthless.

**A finding that fell out of it.** Vesper *does* pass the anchor check at 29% — and its anchor
is `captive_room`, the sealed room with no exits that the player can never return to. An
anchor the world cannot reach is not a centre, and `references/the-board.md` now says so.

**Also corrected while propagating:** `v2_state.json` grew `board.ascent_tiers` (a *named*
declaration, which gate 10 now prefers over its top-3 guess) and `board.ceilings`; per-location
`budget` was replaced by an `anchor` flag, since there is no per-room quota any more.

**Honest note on the record.** This is the second threshold in this skill that did not survive
being checked against its own source, and both were caught by re-measuring rather than by
review. The standing rule holds: every number in `gates.py` carries its measurement inline, and
any number that cannot be re-derived from the snapshots on disk does not belong there.

---

## 2026-08-10 — templates, and a doctrine correction the templates forced

**What.** Added `templates/want.md` and `templates/board.toml` — fillable forms rather than
prose to be interpreted. Corrected `references/the-want.md` §3, `references/the-board.md` §3,
and gate 10 in `scripts/gates.py`.

**The correction, and how it was caught.** The plan set a discrimination test for any worked
example: the format must be able to express a *proven* world (Degrees of Lewdity's seed) and
must still condemn a *measured failure* (Vesper). Running the first half of that test against
DoL's actual source refuted our own doctrine.

We had written "**exactly one** global ascent axis" for a female-protagonist game, on the
strength of a secondhand summary. The source says three layers:

| layer | measured in DoL's seed |
|---|---|
| **ratcheting ascent tiers** | promiscuity 22 raises / 1 lower (206 gate sites) · deviancy 20/0 (129) · exhibitionism 12/1 (167) · `purity` counterweight (58) |
| **volatile state** | arousal — 277 sets, 55 increments, 8 decrements; moves both ways constantly |
| **per-character tracks** | robin / whitney / eden each carry love + lust + dom |

The tiers gate at **15 / 35 / 55 / 75** — a four-rung ladder twenty points apart, consistent
across promiscuity and exhibitionism. Doctrine now teaches three or four tiers, each naming a
*different kind* of going-further, because a single undifferentiated meter collapses parallel
ascents into one ladder every player has to climb the same way.

**Gate 10 changed with it,** and this moved the scoreboard: it now judges the top
`ASCENT_TIERS = 3` gated meters rather than one, and it prefers a **declaration** over a
guess — reading `board.ascent_tiers` from `games/<slug>/v2_state.json` when that file exists,
falling back to the top-3 heuristic and labelling the headline `[top-3 guess — no
v2_state.json]` when it does not. Rationale: skills and resources legitimately gate downward
and are not the spine; only the author can say which traits are ascent.

⚠️ **The previous entry's claim that the scoreboard "still reports 2/10" no longer holds.**
Vesper now scores **1/10**: `stealth` (4 expanding / 11 contracting) sits in its top three
gated meters, so the ascent gate fails. That is a real signal — the measured disease of that
game is that survival systems out-gate desire (stealth + weapon + fighting = 90 gate
references against corruption's 66) — but it is a change to the measuring stick and is
recorded as one rather than presented as a constant.

**Template bug caught by its own machine test.** `templates/board.toml` first declared player
traits as a multi-line inline table (`core_traits = { … }` across several lines), which is a
TOML parse error — inline tables cannot span lines. Real games use the `[player.core_traits]`
*section* form, in `1_metadata_and_locations.toml` rather than `0_systems_spec.toml`, because
TOML scoping requires `[[npcs]]`, their schedules and the player traits to share one file. The
template now round-trips: placeholders substituted, `tomli.loads` parses, all seven sections
present, five bands, schedules correctly bound to their NPC.

**Deferred deliberately.** The worked example. Shipping an invented toy world would make the
exemplar a guess, and reconstructing DoL as the exemplar would teach cloning a specific game —
the exact "copy what they ARE instead of understanding what makes them WORK" error this skill
was built to avoid. The first real Board becomes the exemplar instead, written when the
premise is chosen.

---

## 2026-08-10 — the doctrine lands: `SKILL.md` + six references

**What.** The rest of the skill, written on top of the scoreboard: `SKILL.md` (entry point and
dispatcher) plus `references/the-want.md`, `the-board.md`, `the-release.md`, `agents.md`,
`engine.md`, `state.md`. 934 lines of doctrine over 462 lines of script.

**Shape.** The skill authors a **release stream**, not a story. Four phases — `want`, `board`,
`first_release`, `release` — dispatched from `games/<slug>/v2_state.json`. Content is named in
three kinds (STANDING / TRIGGERED / MILESTONE), derived from what the reference game's own
release commits actually do, so the vocabulary owes nothing to the incumbent skill.

**Anti-drift.** The failure this skill is built against is a fantasy spec written once and
never re-opened. Two mechanisms answer it directly: the Want is defined as an *input to every
release* ("a release that cannot name which line of the Want it serves does not ship"), and
`v2_state.json` carries `want.last_read_at_release`, which is behind the current version if
the Want was skipped.

**Verified.**

1. *No invented fields.* All **67** engine keys the doctrine instructs an author to write were
   checked against `games/vesper/toml_phases/7_final_game.toml` — every one occurs in a real
   game. Nothing aspirational shipped.
2. *Gate coverage.* All ten gates have doctrine feeding them. Gates 1, 4, 5, 6, 8 and 10 are
   decidable from the Board alone (so they can be fixed before content is hung on a broken
   frame); gates 2, 3, 7 and 9 are content-level and are fed by the Want and the Release loop.
3. *Scoreboard regression.* `gates.py vesper` still reports **2/10** — the doctrine did not
   move the measuring stick.
4. *Dispatch.* `SKILL.md` registers with an `EXPLICIT-INVOKE ONLY` description naming its
   triggers and explicitly routing plain "start a new game" / "continue writing `<game>`"
   requests to the incumbent, per the `find-media-v3` precedent.

**One correction made to our own record while writing this.** `references/the-board.md`
initially repeated a note from project memory claiming an NPC schedule window cannot cross
midnight and needs two rows. Reading the source refuted it — `setup.isCurrentTimeSlot` in
`generators/v2.py` handles the wrap explicitly (`if (endTotal < startTotal) return currentTotal
>= startTotal || currentTotal < endTotal;`, call sites `:3448`, `:3465`, `:3612`). The Board
and the engine card now state the verified behaviour and flag the contradicting memory for a
live check. This is the reason `engine.md` requires a `file:line` on every claim, and why it
keeps an explicit "unverified — do not cite until read" list at the bottom.

**Open.** No game has been built with this yet. The TOML layout question was settled by keeping
v1's `toml_phases/` convention, since changing it is engine surgery on
`scripts/merge_toml_phases.py` and does not advance the doctrine.

---

## 2026-08-10 — `scripts/gates.py` created (the scoreboard, built before any doctrine)

**What.** First file of the v2 skill: a ten-gate measuring script that scores a built game's
merged TOML. Run as `python3 scripts/gates.py <game-slug>` or against an explicit `.toml`
path; `--json` for machine output; exit code 0 only when every gate passes.

**Why first.** Build order is deliberate — the measuring stick exists before the doctrine so
the doctrine cannot quietly drift off it. Every threshold traces to a primary measurement
rather than to inherited opinion, and the header of the script carries the evidence inline.

**Where the numbers come from.** Ten snapshots of Degrees of Lewdity's own source, fetched
from `gitgud.io/Vrelnir/degrees-of-lewdity` (project id 8430) and measured on one frozen
instrument, spanning its earliest retrievable build (root commit `ef4a8067102a`, "Initial
import (v0.1.20.2)", 2018-11-28) to `0.5.11.9` (2026-07-28) — 25 to 61 locations, 1,772 to
15,629 units, 254,674 to 2,235,775 words.

- `WORDS_PER_LOCATION = 10_000` — DoL's thinnest year ever (10,187). Its words-per-location
  rose monotonically for eight straight years to 36,652; it never opens a place faster than
  it fills it.
- `EXPLICIT_BEAT_FLOOR = 7.5` — share of beats carrying 3+ explicit words held at 7.5–9.3%
  across eight years and 12x growth. Raw sex-word share is *not* usable (it fell 3.00% to
  0.96% as systems and UI outgrew prose); the beat ratio is the stable one, and it is robust
  to word-list choice.
- `EXPLICIT_IN_REPEATABLE = 50.0` — from the measured failure case: 95% of Vesper's explicit
  beats sit in a sealed room with no exits while all nine of its repeatable sex loops score
  zero.
- `LOCATIONS_WITH_HEAT = 60.0` — deliberately not 100%. DoL's seed had sexual passages in 17
  of 25 locations (68%); a police station is allowed to be cold.

**Verified.** Run against `games/vesper`: **2 of 10 gates pass**. Four correctness bugs were
found and fixed during that run, each by reading the source rather than assuming:

1. `is_repeatable` defaults to **true** when the key is absent — confirmed firsthand at
   `generators/v2.py:10937`, `generators/v2.py:11010`, and `apps/stories/models.py:355`. An
   earlier grep-based pass that assumed otherwise reported 33% repeatable when the majority
   is repeatable; the script parses TOML and never greps.
2. An **effect** names its trait `trait`, while a **condition** names it `trait_key`. Reading
   only `trait_key` silently missed every trait write in the game and produced false
   "opens nothing" findings on the trait-sequenced `salvage_session_*` chain.
3. Meter ceilings live in `sidebar_items[].bands[]`, not in `player.core_traits` (which is a
   flat `{key: initial}` map). A top band with no `max` is unbounded by design and is skipped
   rather than guessed at.
4. Three gates were stricter than the evidence and were relaxed to match it: traversal heat
   (to 60%), milestone payoff (made transitive, since an opening funnel legitimately runs
   one-shot to one-shot and only the end of the chain must land on standing content, and with
   random ambients and self-guard canvases excluded), and meter direction (judged on the
   single most-gated meter, because a female-protagonist game runs one ascent axis while
   skills and resources legitimately gate downward).

**Not yet present.** No `SKILL.md`, so the skill does not register or trigger — correct for
now, as it is not ready to be invoked. The description will carry `EXPLICIT-INVOKE ONLY` when
it lands, following the `find-media-v3` precedent, and the incumbent `author-game` skill keeps
every ordinary request until v2 is promoted.
