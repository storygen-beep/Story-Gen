# Steam — review ledger

Opened 2026-08-12, the day it was authored. Steam is the **validation game** for `author-game-v2`:
built in a clean session, by a reader of the skill, with no context carried over from the session
that wrote the doctrine. That was the point — the previous game was authored by the same person who
wrote the rules, so it proved nothing.

It scores **18/18, exit 0.** It also has the problems below. That combination is the finding.

**Same conventions as `games/back_home/REVIEW.md`:** severity `BLOCKER`/`HIGH`/`MED`/`LOW`/`OPEN`/
`DEFERRED` · layer `GAME` (this build) / `SKILL` (doctrine taught it wrong or not at all) /
`ENGINE` · every claim carries a measurement or a `file:line`.

Current count: **10 open**, 0 fixed.

---

# 0 · Read this before the defect list

**The prose is good, and it fixes a defect we were chasing elsewhere.**

The repeatable sex surfaces escalate one step per beat, stay on the body, and put the interiority in
its own beat afterwards. `loop_casper_slab`: the money goes down on the marble → clothes off → oil
and an oiled fist → she blows him → she climbs on → she comes, then he does → she picks the thirty
dollars back up in front of him. `loop_warren_corner` runs the same seven-rung shape and lands its
whole characterisation on *"He puts his glasses back on. That is always the moment it comes back."*

This is exactly the incremental build that was flagged as **missing** in another game in this repo,
where a scene went straight to the act. **Steam does not have that defect.** Whatever is wrong here,
the writing is not it — and no fix below should touch the prose.

The cold writing holds up too: *"A man at the counter at four on a Wednesday who has driven from
somewhere and who asks the question badly."*

---

# 1 · Structure — the defect that produced most of the others

### S1 · Every location is one mega-menu
**severity** BLOCKER · **layer** SKILL · **status** **DOCTRINE FIXED 2026-08-12; game untouched**

**The skill-side fix shipped the same day.** `references/the-surfaces.md` is new — the missing axis,
*which screen does this live on* — `engine.md` §19's unscoped sentence is now scoped, and **gate 20
("a place is not a catalogue") fails this game on all nine offending screens**, measured at a ceiling
of 8 against a field median of 2 links per screen. Steam now scores **18/19**.

The game itself is unchanged and every number below still stands.

```
24 located canvases   ·   203 triggerless link-target rungs
```

Almost nothing is a surface of its own. The player's experience at a location is one paragraph and
then a wall of buttons:

| hub | choices | ungated | opener blocks |
|---|---|---|---|
| `hub_front_desk` | **23** | 7 | 1 |
| `hub_spring_street` | **19** | 15 | 1 |
| `hub_changing_room` | 19 | 13 | 2 |
| `hub_attic_night` | 18 | **17** | 3 |
| `hub_scrub_room` | 17 | 5 | 2 |
| `hub_boiler_day` | 16 | 6 | 2 |

`spring_street` contains exactly **one canvas** — that hub. `the_front_desk` contains three.

The front-desk list also mixes three unrelated kinds of action at identical weight: free texture
(*Look up at the board*), major economic commitments (*Put Del on a written wage. (240)*), and a
top-tier unlock (*Take the chain off the stairs*, house 55). Nothing signals which matters.

**Cause is D1.** The author was following the skill.

### S2 · Half the game is available on turn one
**severity** HIGH · **layer** GAME + SKILL · **status** OPEN

**109 of 216 choices carry no condition at all.** `hub_attic_night` offers 17 of 18 immediately;
`hub_spring_street` 15 of 19.

The three ascent tiers exist and all gate upward (steam 33+/0−, service 20+/0−, house 11+/4−) — they
are simply gating a minority of the doors. With no staggering there is no progression to feel, and
the wall of choices in S1 is at its worst on day one, when the player knows least.

### S3 · Ten of eighteen menus sit on a single static block
**severity** MED · **layer** GAME · **status** OPEN

The opener does not move with state. Re-enter that location on day 40 and it is the identical
paragraph above the identical list. This is the re-readability failure the register doctrine exists
to prevent, occurring one level above the sentence — and these are the most re-entered screens in
the game.

---

# 2 · Heat — a consequence of the structure, not of the writing

### S4 · 7.6% against a 7.5% floor, and the Want asked for better
**severity** HIGH · **layer** SKILL · **status** OPEN

```
explicit floor   7.6%   (floor 7.5% — cleared by 0.1)
65 explicit beats of 856   ·   29 canvases of 227 carry any heat
back_home        27.8% on the identical instrument
field median     33.3%
```

**This is not the author aiming low.** The Want explicitly says the right thing:

> *The crude register lives on the repeatable surfaces — the scrub room floor, the plunge, the
> private rooms — re-entered every in-game day. Nothing crude is saved for a one-time capstone.*

And it was followed: gate 3 reports **93.8% of explicit beats are re-enterable.** The placement is
correct. The volume is not.

**The arithmetic came from S1.** Nineteen buttons at a location needs nineteen things written. You
cannot put nineteen sex scenes at a front desk, so the slots fill with three-to-four-beat cold
texture rungs — roughly 200 of them against 29 with any heat. `back_home` used fewer, deeper
surfaces and landed **3.7× hotter** with the same author and the same doctrine.

**The shape set the ratio before a word was written.**

### S5 · The economy is a shop counter
**severity** MED · **layer** GAME + SKILL · **status** **GATED 2026-08-12; game untouched**

Gate 17 now measures **where** sinks are, not just how many: it fails when more than half resolve to
one location. Steam fails it at **12 of 21 at `the_front_desk`**, and the game drops to 17/19.
`the-economy.md` R2 gained the placement half — *a sink belongs where the thing being bought lives.*

Gate 17 passes at 21 sinks : 20 sources — but **eleven of those sinks are purchase buttons in one
menu at the front desk**: the water test, the paper advert, the electric, the frontage, Del's wage,
Ivo's wage, the occupancy fee, the note overpayment, and more.

That is a shop, not an economy. Money leaves the player in one place, by one gesture, at one desk.

---

# 3 · What this says about the skill and the instrument

### D1 · `engine.md` §19's prescription has no scope, and it caused S1
**severity** BLOCKER · **layer** SKILL · **status** OPEN

§19's *rule* is narrow and correct — two repeatable canvases binding **the same NPC** at the same
location with overlapping schedules collide, and only one renders. `hub_front_desk` and
`hub_spring_street` bind **no NPC**, so the rule never applied to them.

But the paragraph attached to it says:

> **The fix is the engine's own advice, and it is also the better design:** make the second canvas a
> triggerless rung and hang it off the existing hub as a CHOICE.

**No scope on that sentence, and it calls itself "the better design."** A careful reader applies it
everywhere. `back_home` did the opposite — nine separate canvases at one bedroom — and also scored
green. Two opposite architectures, both passing, and **the skill has no opinion about the shape of a
location page.** That is the gap; the loose sentence is what filled it.

### D2 · Six engine facts had to be rediscovered live — and one we already knew
**severity** HIGH · **layer** SKILL · **status** OPEN

The session wrote its own `games/steam/ENGINE_NOTES.md` because `references/engine.md` did not carry
what it needed. Checked: **none of the six appear in `engine.md`.**

| fact it had to learn live | in `engine.md`? |
|---|---|
| `State`/`Engine` hang off `window.SugarCube`, not bare globals | no |
| `time_state.current_day` is a day **NAME**, not an index | no |
| presence via `setup.getNpcsPresentAtLocation(slug)` | no |
| `pickQuestsCards` accepts exactly one scope, `"story_goals"` | no |
| Playwright text selectors break on rendered labels | no |
| **cascade-beat markup is entity-encoded in the page source** | no |

⚠️ **Two of these this project had already paid for.** The day-NAME fact is in the v2 `CHANGELOG.md`
from the `back_home` run. The entity-encoding trap is the same class that voided a whole measurement
pass during the economy research. Both were logged in a changelog and neither reached a reference
file, so a fresh session lost time rediscovering them.

> **A CHANGELOG is a trail, not doctrine. A fact logged there does not reach the next session.**
> Only reference files do. This is the same lesson as "declarations hold, paragraphs don't", one
> level up: it is not enough to write a fact down, it has to be written down *where the next reader
> looks*.

### D3 · Two gates count presence and call it placement
**severity** HIGH · **layer** SKILL (instrument) · **status** OPEN

- **Gate 3** — 93.8% of explicit beats re-enterable. It measures where the **numerator** sits and
  never asks how small it is against the denominator. 65 of 856 can be perfectly placed and still be
  a film.
- **Gate 17** — 21 sinks : 20 sources. Counts sinks, never asks **where they live** (S5).

Both were built one turn after documenting that exact failure class. Gate 3 already solved it for
heat by asking a *placement* question; the newer gate did not inherit the idea.

### D4 · The explicit floor did no work
**severity** HIGH · **layer** SKILL (instrument) · **status** OPEN

7.6% against a 7.5% floor is a pass by 0.1. The floor is the **coldest game in an eighteen-game
field** (field median 33.3%), so as a discriminator between "has heat" and "is a porn game" it is
inert. `register.md` gained a *"clear it, do not aim at it"* paragraph the same morning this game was
authored, and the game landed on the floor anyway — which is D2's lesson again: prose does not hold.

---

# 4 · Smaller items

### M1 · Zero media, six broken portraits
**severity** DEFERRED · **layer** GAME · **status** PARKED

Six `[[npcs]]` portraits declared (`del.jpg`, `ivo.jpg`, `warren.jpg`, `june.jpg`, `casper.jpg`,
`nell.jpg`), 44 media pools declared, and `output/` contains only `index.html`. **This is the blank
vertical gap visible under the front-desk paragraph** — Del is scheduled there 08:00–11:00 daily, so
her portrait card renders as an empty box.

### L1 · The world-prose lint fired, and it is right
**severity** LOW · **layer** GAME · **status** OPEN

*yard* ×11, *hall* ×7, *front door* ×7 — none of them locations. The yard in particular is load-
bearing: *"four o'clock is the yard shift and the men's side goes from empty to…"*. The new lint
caught this on the first build of the first game it ever ran against.

### L2 · Dialogue attribution — 10 hits, and the session resolved the real one
**severity** LOW · **layer** GAME · **status** OPEN

Worth recording as a **win for the lint**: `ENGINE_NOTES.md` reports June had a `dialog` block at
`spring_street`, where she has no schedule row — *"she was speaking in a place the game never puts
her"* — now rewritten as reported speech. Nine of ten hits were noise; the tenth was a real bug the
build would never have flagged.

---

# 5 · Not defects — checked, and correct

- **The prose.** See §0. Escalation, body-focus, separated interiority, crude vocabulary at ceiling.
- **Every board declaration.** `board.map` with 6/6 real homes · `board.economy` with a named
  currency and listed sinks · `board.guidance` · ascent tiers and counterweight. Everything the
  doctrine encoded as a **required field** was produced correctly and unprompted.
- **Guidance authored, not merely switched on.** 24 quest cards across 3 tiers and 6 characters, and
  6/6 ladders carry a card that survives the arc closing.
- **All 8 locations reachable on foot.** Median sentence 12 words.
- **The Want is well-formed** — appetite that cannot complete, ascent stated as access, a per-NPC
  crude ceiling, and a deletion test (*"Cut Del and the game loses its standard"*).
- **18/18 gates, exit 0.** Recorded here as fact, not as praise: the point of this document is that
  it is possible.

---

# 6 · Open questions

### O1 · Does the mega-menu shape have a defensible version?
S1 is a defect at 19–23 choices. It is not obviously a defect at 6–8. Nothing measured here says
where the line is, and `back_home`'s alternative (nine separate located canvases at one room) has its
own cost — the location page becomes a list of links instead of a scene. **The skill needs a shape
for a location page and does not have one; neither of the two games built so far should be assumed
to be it.**

### O2 · Should the explicit floor be re-baselined?
D4 says the current floor is inert. The field median is 33.3%, but on a **different extraction basis**
(built HTML vs authored beats), so it cannot simply be adopted. The two games we can compare
like-for-like sit at 27.8% and 7.6% — enough to discriminate, not enough to set a threshold from.

---

## Log

| date | what |
|---|---|
| 2026-08-12 | Opened. 10 items from a read-only structural + prose review of the game as authored. Nothing changed. Steam scores 18/18 exit 0 with every item below open. |
