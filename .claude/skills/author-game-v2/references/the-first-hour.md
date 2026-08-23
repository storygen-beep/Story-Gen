# The First Hour — the opening, and the people in it

Everything between the title screen and the moment the player is on their own: the opening funnel,
the first time each character is met, and the first time each place is entered.

This file owns **one rule** with three faces, and every section below is that rule applied:

> **The game does not use a name until it has earned it.** People, places, things. Before the
> player has met it, the game says what it *is* and where. After, it says the name.

> Measured failure this exists to prevent: a shipped game whose opening spent **278 words naming
> six people, none of them on screen and none of them speaking**, then handed the player an open
> world at **07:36** where the only place they could go opened at **08:00**. Every one of its four
> characters was standing in a room from turn one with no meeting, and the location the design had
> declared at **27% of the whole game** was never once described as the kind of place it is. The
> game scored **31 of 32** on the scoreboard while doing all of it.

**Why this file exists at all.** v1 carried two files that did most of this job —
`author-game/references/onboarding.md` (269 lines) and `npc-intro.md` (146 lines). v2 shipped
without either, and the loss is legible in the output: counting non-repeatable canvases that fire
at a character's location, the four v1 games run **24 · 13 · 7 · 0** and all six v2 games run
**zero**. This is `DOCTRINE_GAPS.md` Tier 2 row 6, and it was the last row in that table with an
empty status column.

Engine claims here carry a `file:line` into
`apps/game_generation/twee_comprehensive/generators/v2.py`, per `SKILL.md` operating rules.

## Contents
1. F1 · The opening picks one shape and commits
2. F2 · Boot and capstone are two canvases
3. F3 · The opening hands over into an open door
4. F4 · Every live system gets one beat
5. F5 · Every character's hub sits behind a meeting
6. F6 · A meeting is small, and somebody speaks
7. F7 · Role before name
8. F8 · One flag per character
9. F9 · The anchor introduces itself
10. What the scoreboard checks
11. Cheat sheet

---

## F1 · The opening picks one shape and commits

The field runs **two** opening shapes and nothing in between. Measured across 25 shipped sandboxes
(`~/Documents/Mopoga_Twine_Sandbox_Research_20260724/gamehtml/`), walking each game from its
`startnode` down the navigation spine:

| shape | words | cast | examples |
|---|---|---|---|
| **cold open** | 60–300 | **nobody** | corpo-life 64 · the-company 126 · degrees-of-lewdity 193 · destroyer 285 |
| **staged open** | 700–2,600 | one at a time, each on screen and speaking | friends-of-mine 1,377 · new-life-project 1,558 · patriarch 2,619 |

**Ten of twenty openings name nobody at all.** When a field opening does name people, it spends
**~229 words per named character** (values 132, 174, 217, 229, 1055, 1558, 1633).

corpo-life's whole cold open, in full — who, job, place, why poor, what is at stake, zero characters:

> *"My name is [X]. I just got accepted into Chase-Bank, one of the most prestigious banks in New
> York city. After graduating from Stanford, I applied into the Management Trainee program and
> rented a small apartment near my office and am living frugally in order to live in this concrete
> jungle."*

**The defect is the middle.** A cold open carrying a staged open's payload names people the player
cannot picture, at a density the prose cannot support. The measured case ran **46 words per named
character** — a fifth of the field's rate — and put none of them on screen.

**Pick one:**
- **Cold open** — name the player's situation and the pressure. Name **nobody**. The cast arrives
  later as content, each through F5's meeting. ~150 words.
- **Staged open** — spend the words. One person enters at a time, is described, **speaks**, and
  states what they want. 700+ words, and F6's craft bar applies to each entrance.

⚠️ **This is not a word-count rule.** It is a *consistency* rule: the cast load and the word budget
have to agree. A 200-word opening that names four people fails it; a 200-word opening that names
none passes.

⚠️ **Named in passing is not met.** An offstage boss, a dead parent, a landlord who never appears —
these are world-building and they cost the reader a name to hold. Two of the six people named in
the measured failure **are not in the game at all**. If the player can never go and meet them, ask
whether the name is doing work, or delete it.

---

## F2 · Boot and capstone are two canvases

Our own `starting_canvas` sizes, measured across ten built games:

```
v1   the_inheritance 144 · late_shifts 155 · last_call 214 · vesper 687      median 184
v2   off_season 278 · steam 285 · forty_miles 339 · back_home 465
     the_allowance 534 · seventh_day 726                                     median 402
```

v2's openings are **more than double** v1's, and the reason is structural, not stylistic: v1 split
the opening into a small **boot** and a separate **capstone**, and v2 collapsed both into one
canvas that then had to carry everything.

The shape:

- a small **boot** one-shot — the `starting_canvas`, high `priority`, `is_repeatable = false`.
  It puts the player at the start location and begins the chain. It does not carry the cast.
- a separate **capstone** one-shot at the same location, gated on the flag the boot sets, where the
  prose is allowed to spend.

Both auto-fire on entry through `selectAutoFireCanvasForLocation`, which picks the highest-priority
valid **non-repeatable** canvas and skips every repeatable (`v2.py:4453-4471`). The flag gate is
what guarantees order — no schedule is needed.

⚠️ **This is not a size cut.** Build the opening at full designed size; the engine plays a node
chain back one screen at a time. "Two canvases" is about *what each one is for*, not about brevity.

---

## F3 · The opening hands over into an open door

The last click of the funnel puts the player somewhere, at a clock time, and that place has to have
something live in it **at that minute**.

The measured failure, computed exactly the way the gate computes it:

```
[time] starting_hour = 7                                  07:00
node -> node, no time declared -> default 3 min           07:03      v2.py:13200
node -> node, no time declared -> default 3 min           07:06
exit: time_progression_minutes = 30, to the_arcade        07:36

at the_arcade, 07:36:
  work_arcade_morning      schedule 08:00-13:00     CLOSED
  work_arcade_afternoon    schedule 13:00-19:00     CLOSED
  work_arcade_after_close  schedule 21:00-01:00     CLOSED
  walkin_arcade_counter    substitution_only        never renders on its own
  amb_arcade_damp          trigger_mode = random    not guaranteed
  amb_arcade_denny         trigger_mode = random    not guaranteed
```

**The player's first free act in that game is pressing a wait button.** This is v1's §2.7
dead-window bug — its own words, *"a needed NPC is only present at a time the player can't reach"*
(`author-game/references/onboarding.md:119`) — widened from a character to a whole room, and landing
in the one place it does the most damage.

Three ways to fix it, all fine:
1. move the handover time (start later, or spend fewer minutes in the funnel);
2. widen the landing location's schedule window so it is open on arrival;
3. hand over somewhere else — a location whose content has no schedule at all.

⚠️ **A random ambient does not count.** `trigger_mode = "random"` rolls a chance; it can legitimately
produce nothing. The first screen of the open world cannot be a coin flip.

⚠️ **Neither does a walk-in.** `substitution_only = true` means the canvas only ever appears as a
substitution inside another canvas's trigger (`v2.py` PRD 25 §5.5, filtered in
`selectAutoFireCanvasForLocation` and `selectNpcPortraitCanvasesForLocation`). It has no door of
its own.

---

## F4 · Every live system gets one beat

Carried forward from v1's `onboarding.md` §2.3, unchanged, because it was right and nothing
replaced it:

> **A system the player never sees taught is a system you might as well not have wired.**

For every system switched ON in `0_systems_spec.toml`, either a named beat in the first hour arms
it, or it sits on the sidebar at value-zero where the player can read it. One row per system, none
cold.

Measured failure: a game shipped `clothing_enabled = true` and `wardrobe_location = "the_flat"`, and
across the whole merged TOML the strings `wardrobe` and `clothing` appear **once each**, while
`get changed` and `change into` appear **zero** times. The system is live, costed, and invisible.

The sidebar is the other half and it is permanent: a banded stat reading near-empty against its
ceiling **is** the "there is a climb ahead" read, on frame one, with no teach screen. See
`the-meters.md` and `the-voice.md` for what goes on it.

⚠️ **The rent clock is armed, not fired.** Use `[settings.rent] start_after_flag` pointed at a flag
the opening raises, so the first session is pressure-free — no charge lands before the player has
been told the rules.

---

## F5 · Every character's hub sits behind a meeting

**The forbidden shape:** a repeatable canvas with `npc =` set whose base node *is* the
introduction. The player walks into a room and the character is simply there, the hub's first
paragraph standing in for a meeting.

All six v2 games ship this for their entire cast. Checked directly:

```
hub_ewan_yard        conditions: NONE
hub_tam_flat         conditions: NONE
hub_roan_house       conditions: NONE
hub_nessa_back_room  conditions: NONE
```

**The field's answer.** 16 of 25 shipped games carry per-character meeting state, and the strongest
one carries it on effectively its whole navigable cast — degrees-of-lewdity keeps a first-time flag
on **24 of its 27 registered NPCs** (`C.npc.<Name>.init`, plus older `_intro`/`_seen` flags for the
rest), read in conditions 150 times. become-someone gates **presence**, not just dialogue:
`<<if $has.metkate is 1 && $kate.loc is "Beach">>` — she is not in the world until she has been met.
the-company sets `player.met.sophie` in a passage named `Intro-MeetSophie`.

**The shape to build:**

| | |
|---|---|
| the meeting | `is_repeatable = false` · high `priority` · location-bound · sets one flag on exit |
| the hub | `is_repeatable = true` · `npc =` set · gated on that flag · a **different** `name` |

**Where a character has several hubs**, the meeting flag belongs on the **first** one — the hub
the player reaches first. A later rung can be gated on something downstream instead (`aud_sexloop`
on `audrey_stage gte 3`, `canvas_marcus_arrangement` on `marcus_drinks_done`) and that is correct
work. What is never correct is a hub with **no conditions at all**: it puts that character's
portrait on a location screen from turn one, however well the first hub is gated. Two shipped games
carry exactly one of those each — `the_inheritance/hub_richard` and `vesper/hub_sol_undertow`.

A non-repeatable canvas renders **no portrait** — `selectNpcPortraitCanvasesForLocation` skips
`if (!c.isRepeatable) continue` (`v2.py:4482-4487`) — so the meeting cannot leak onto the location
screen as a face, and the hub cannot appear before the meeting has fired.

> ### ⚠️ `requires_npc` does NOT gate the auto-fire path. This corrects v1.
>
> `npc-intro.md` §1.3 says to set `requires_npc` so the meeting *"fires where the NPC is."* Traced
> in the engine, that is **false** for a canvas that auto-fires:
>
> ```
> getStoryCanvasRedirect              v2.py:4921
>   -> selectAutoFireCanvasForLocation    v2.py:4453
>     -> isCanvasValid                    v2.py:4573
>        checks: schedules · conditions · repeatability.  requiresNpc is never read.
> ```
>
> `requiresNpc` is emitted at `v2.py:11104` and consumed in exactly two places — `v2.py:5259`
> (the random-encounter selector) and `v2.py:5332` (substitution rules). **Neither is auto-fire.**
>
> Consequence, in a shipped game: `vesper/cap_renner_hired` is bound to `the_anchor` with
> `requires_npc = "npc_renner"`, and Renner's schedule puts him there 19:00-23:00. The canvas
> auto-fires whenever the player walks in with the other conditions met — so the prose can
> introduce him in an empty bar at ten in the morning.
>
> **Gate the meeting on a `schedules` window that matches where the character actually is, or on a
> flag the player can only hold by having been there.** Keep `requires_npc` as well — it is free,
> it is correct on the paths that read it, and it documents intent — but never rely on it alone.

> **Gated as `a meeting fires where they are` (G38).** Measured across every game in the repo,
> 2026-08-23 — 69 canvases in scope, and **zero carry a window that misses their character's own
> hours**, so the check never nags a game that did the work:
>
> ```
> last_call 11/11 clean · off_season 8/8 · the_long_summer_test 1/1
> the_season 0/5      · the_inheritance 0/24 · vesper 0/13 · late_shifts 6/7
> ```
>
> ⚠️ **The rule above was correct and present, and a game still shipped 0/5 — because a second
> document said the opposite.** `template_import.py`, the file an author reads to learn the TOML
> schema, described `requires_npc` as something that *"lets authors drop per-canvas location+time
> gates"*, with no scope on the claim. True for the two Lane 2/3 functions; false for every meeting
> canvas. `the_season` was written twelve hours after this reference and its template landed, with
> both open, and its five introductions played to empty rooms. **When doctrine and the schema
> disagree, the schema wins, because the schema is what is open while you type.** The comment is
> corrected; the gate is why it cannot come back.

---

## F6 · A meeting is small, and somebody speaks

Measured across 696 passages named intro/meet in 18 field games:

```
median 101 words · quartiles 57 / 101 / 194 · 66% under 150 words · 64% carry spoken dialogue
```

Narrowing to passages named *meet* only (158 of them): median **166**, **55%** spoken. Both
instruments land in the same band.

the-company's entire first meeting with the player's employer is **80 words**:

> *"Your new employer stands and leans forward to shake your hand. This close you notice her
> piercing violet eyes as she appears to size you up behind a sincere yet cunning smile."*

Role, then the look, then a beat. That is the whole thing.

**Our own worked example is already correct.** `the_inheritance/canvas_meet_audrey` — 125 words,
4 `dialog` blocks, one node, priority 10, location-bound, conditions gated. Mirror its shape.

**Where the player cannot yet know the name**, set `speaker = "unknown"` on the `dialog` block and
the engine prints **"Stranger:"** (`v2.py:14600-14606`); switch to the NPC speaker once names have
been exchanged.

⚠️ **A meeting with no `dialog` block is not a meeting.** The person is in the room. If they do not
say anything, the player has been handed a description, not an introduction. This is `register.md`
S3 applied at the one moment it matters most.

---

## F7 · Role before name

The field's ordering, in the two clearest cases:

> *"This is your closest friend, **Felix Morin**; a rather shy young man who you've known almost
> since the day you've moved here… including his older sister, **Chloe**."* — friends-of-mine

> *"one of your father's favourite girls, Ana"* — patriarch

**Relationship label first, then the name.** The label is what the player can hold; the name is
what they will need later.

The measured failure inverts it: *"It goes to Ewan"* — the name arrives with no role attached, and
that sentence never says who Ewan is.

**The strongest form of this rule is mechanical, and it is worth stealing.** degrees-of-lewdity
swaps the description for the name once the meeting flag is set, so the game literally cannot use a
name the player has not earned:

```
deliver a letter to <<if $wren_intro is undefined>>a <gender> named Wren.  <He> can be found at
  Remy's estate in the moor, or at the docks at night<<else>>Wren<</if>>.

Kylar<<if C.npc.Kylar.init isnot 1>>, a student at your school<</if>>.
```

Ours has the same primitive: a `[group]` block with `conditions` on the meeting flag, or a
`cascade`. Use it where the reference is load-bearing — a quest card, a guidance line, a location
description that sends the player somewhere.

⚠️ **Honest limit.** The naming swap is heaviest in one game (64 blocks in degrees-of-lewdity;
course-of-temptation 9, amore 2). It is the strongest game's mechanism, not a field-wide norm — so
it is a **tool to reach for**, not a bar the gates hold you to. The **flag** is the norm; the swap
is what a good author does with it.

⚠️ **NOTHING ENFORCES THIS AT THE MEETING ITSELF, which is the one place it matters most.** The
`named before met` lint asks only whether a character's name appears in the opening, a quest card
or a room description *before* they have a meeting — and it skips anyone who has one outright
(`gates.py`, `if n["id"] in has_meeting: continue`). It never reads the meeting's own text. So a
meeting that opens on a bare name passes every check in this skill.

`the_season/meet_emmett` opened *"Emmett is on the belt…"* and no line in that canvas ever said he
was her brother — the one character in that cast who is hardest to read, arriving unlabelled, while
Wade, Boyd and Prine all opened on the role.

**And a check for it was tried and rejected**, which is worth recording so it is not re-attempted
blind: a kinship-word detector run over every game fires on ten of `last_call`'s meetings (its cast
is not family, so the word was never going to be there), eighteen of `the_inheritance`'s, and three
of `off_season`'s that are mid-arc canvases rather than introductions. Most of its hits are wrong.
**Read the first line of every meeting yourself.** It is five lines of reading per game.

---

## F8 · One flag per character

The dodge this rule exists to kill: gate the whole cast on **one** flag the opening sets, and every
hub is technically "behind a meeting" while the cast still arrives as a block.

Three of the six v2 games shipped exactly this:

```
seventh_day   rota_running   opens 2 hubs
steam         doors_open     opens 2 hubs
back_home     arrival_done   opens 4 hubs
```

**A meeting flag opens hubs for one character and no other.** One flag opening a single character's
talk hub *and* their sex hub is fine — that is one character. One flag opening four people's doors
is the cold-spawn hub with a coat on.

⚠️ **Sequence the cast in waves.** Not everyone is reachable on day one. Stage the entrances so each
arrival is a punctuation mark. For a character who arrives mid-game, **withhold their schedule until
the meeting fires** — `getNpcsWithSchedules` (`v2.py:3537`) surfaces every declared NPC on the
Schedule page from day one regardless of any gate, so a schedule given early spoils the entrance.

### The same flag belongs on that character's quest cards

F5 through F8 gate the **canvases**. They say nothing about the **guidance surface**, and that gap
shipped: `the_season` gated every hub correctly and its Quests page still introduced all five
people on click one — names, the room each stands in, and the hour they are there — before the
player had met anybody. Every meeting in the game was spoiled by the page that exists to help.

**A character's `[[quest_cards]]` carry that character's meeting flag in `when`.**

```toml
when = [ { flag = "met_wade", subject = "player", op = "is_true" },
         { trait = "want", subject = "npc", npc_id = "npc_wade", op = "lt", value = 40 } ]
```

The engine already does the rest. `QuestsPage` wraps each character's section in `<<if _card>>`
(`v2.py:15371`) and `setup.pickQuestsCard` returns `null` when no card's `when` matches
(`v2.py:15050`), so an unmet character renders **no heading and no section** — the roster fills in
as the player meets people, which is what the field ships (the-company's cast table is
`<<if $player.met[_char.id]>>` per row).

Three things to get right:

- **A `when` item sets `flag` *or* `trait`, never both** — the importer rejects an item carrying
  both (`template_import.py:5285`). The meeting flag is its own item beside the trait band.
- **Put it on *every* card in that character's ladder**, not just the first. A gap means the
  character reappears at the band whose card you missed.
- **Flag names are not validated against anything.** Nothing checks that `met_wade` exists; a typo
  hides that character's guidance forever and no build error says so. Read the name off the
  meeting canvas's own `flagEffects`, not off memory.

⚠️ **This flag is load-bearing twice.** The cast page (`[ui.cast_page]`, `engine.md` §34) lists a
character exactly when `pickQuestsCard` returns a card for them, so one flag reveals both surfaces
and they cannot fall out of step. The cost is worth stating plainly: **a character with no quest
card can never appear on the cast page.** `guidance exists` already requires every `[[npcs]]` entry
to carry one, so this cannot happen in a game that passes its own scoreboard.

**Story-goal cards — the ones with no `npc_id` — are never gated this way.** They are the
always-live "Story Goals" section, and a guidance page whose every card is gated renders
"No active quests." on turn one.

---

## F9 · The anchor introduces itself

A place gets the same treatment as a person: the first time the player walks in, the game says what
kind of place it is and what happens there. After that, it can just be the name.

The field does this with the same flag family it uses for people — degrees-of-lewdity carries
`$forest_shop_intro`, `$gwylan_cafe_intro`, `$prison_intro`, and swaps the reference the same way:

```
find a snow globe at <<if $forest_shop_intro is 1>>Gwylan's shop<<else>>the shop on the
  outskirts of the forest<</if>>.
```

It extends past places to **knowledge**: become-someone's `$has.auntaddress` gates whether the
player can travel to the aunt's house at all. Same primitive, three kinds of thing.

**Ours needs no new engine work** — a non-repeatable canvas bound to the location auto-fires on
first entry and never again (`v2.py:4453`).

**The measured failure.** That game has a first-visit canvas at **5 of its 10 locations** — and the
anchor is not one of them. The anchor is the room the ledger declared at **9,000 words, 27% of the
game**. Its `description` reads:

> *"KESH AMUSEMENTS in eight-foot letters over the door, and under them forty machines, half of them
> off at the wall to save the electric…"*

Forty machines of **what**. The description never says slot machines, never says amusement arcade,
never says people put money in them — and the player is put behind its counter on turn one and asked
to work it. *"What is arcade??"* was the first thing the human reader asked.

⚠️ **This is `register.md`'s "words the player has to already own", one level up.** There the unit
was a word; here it is a whole place. A location whose *function* is only implied is an unglossed
noun the size of a room.

---

## What the scoreboard checks

Three gates and one lint. `python3 scripts/gates.py <slug>`.

| | |
|---|---|
| gate · **the opening hands over into an open door** | F3. Walks the funnel's clock and asks whether anything at the landing location is open at that minute. **n/a** when the landing location cannot be resolved. |
| gate · **every hub is met first** | F5 + F8. Per character: **one** hub gated on a flag a non-repeatable canvas naming them sets, **no** hub left with zero conditions, and no such flag opening a second character's door. |
| gate · **the anchor introduces itself** | F9. The anchor declared in `v2_state.json` `board.locations[].fill` has a non-repeatable canvas bound to it. **n/a** with no ledger. |
| lint · **named before met** | F7. Lists every character named in prose the player can reach before that character's meeting can fire. A list to read, never a score. |

⚠️ **Nothing checks the guidance surface.** The `named before met` lint reads *prose canvases* and
does not look at `[[quest_cards]]`, so a game can pass every gate above with its Quests page still
naming the whole cast on turn one — which is exactly what `the_season` did. Read the page yourself
at turn one. A gate here needs a second game before its shape is honest.

Where each stood when the checks landed, 2026-08-22 — read off the shipped gates, not a
prediction:

```
                    open door   hubs met   anchor
off_season             FAIL        0/4      FAIL
the_allowance          PASS        1/5      FAIL
seventh_day            PASS        0/6      PASS
forty_miles            PASS        0/6      PASS
steam                  PASS        1/6      PASS
back_home              PASS        0/4      FAIL
the_inheritance (v1)   PASS        4/5      n/a
last_call       (v1)   PASS        4/4      n/a
vesper          (v1)   n/a         6/9      n/a
late_shifts     (v1)   PASS        0/5      n/a
```

**One v1 game already passes the meeting gate at 100%**, and a second misses by a single hub, so
the bar is one shipped work has cleared rather than an invented number. The six v2 games sit at
0–1 of their cast, which is the same v1/v2 fingerprint the first-contact count shows.

> ⚠️ **The first version of the meeting gate was wrong, and the correction is worth keeping.** It
> demanded that *every* hub of a character carry the meeting flag, and read `the_inheritance` as
> 3/5 — failing it for `aud_sexloop`, gated on `audrey_stage gte 3`, and `last_call` for
> `canvas_marcus_arrangement`, gated on `marcus_drinks_done`. Both are **later rungs**, gated on
> something downstream of the meeting, and both are correct work. That is `SKILL.md`'s *"a check
> that fails a game for obeying the doctrine is a bug in the check"*, caught by running it before
> writing it up. The shipped rule asks for a meeting on **one** hub and bans the **cold spawn** —
> a hub with no conditions at all — on every hub, which is what `the_inheritance/hub_richard` and
> `vesper/hub_sol_undertow` are.

---

## Cheat sheet

- **The game does not use a name until it has earned it.** People, places, things.
- **Pick one opening shape** — cold open names nobody, staged open spends 700+ and puts them on
  screen. The middle is the defect.
- **Boot and capstone are two canvases.** The boot starts the chain; the capstone spends the prose.
- **Hand over into an open door.** A random ambient is not a door. A `substitution_only` walk-in is
  not a door.
- **Every live system gets one beat or one sidebar row.** A system never taught is a system wasted.
- **Every `npc=` hub sits behind a non-repeatable meeting** that names that character —
  the flag on the first hub, and **no** hub anywhere left with zero conditions.
- **Gate the meeting on a schedule or a flag — `requires_npc` does not gate auto-fire**
  (`v2.py:4573`).
- **A meeting is ~100–170 words and somebody speaks.**
- **Role before name.** Swap description for name on the meeting flag where the reference matters.
- **One flag per character.** `doors_open` for the whole cast is the cold-spawn hub in a coat.
- **The anchor introduces itself** the first time the player walks in.
