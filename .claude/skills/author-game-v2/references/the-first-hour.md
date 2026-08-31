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
4b. F4b · The opening refuses nothing
5. F5 · Every character's hub sits behind a meeting
6. F6 · A meeting is small, and somebody speaks
7. F7 · Role before name
8. F8 · One flag per character
9. F9 · A place says what it is, in its own description
10. F10 · The role stays attached after the introduction
11. What the scoreboard checks
11. Cheat sheet

---

## F1 · The opening picks one shape and commits

The field runs **two** opening shapes, and they are separated by **who is named**, not by how long
they run.

| shape | cast | examples |
|---|---|---|
| **cold open** | **nobody** — her situation and the pressure, and no people at all | corpo-life · the-company · degrees-of-lewdity |
| **staged open** | one person at a time, each on screen and **speaking** | friends-of-mine · new-life-project · patriarch · destroyer |

> ### ⚠️ This table published word counts until 2026-08-24. Section K deleted them.
>
> It read *"cold open 60–300 words · staged open 700–2,600"*, with the empty band between them
> offered as a finding, and it carried two more figures from the same source — *"ten of twenty
> openings name nobody"* and *"~229 words per named character."* **None of them is re-derivable, and
> now none of them ever will be.**
>
> What happened, in order. The 2026-08-24 recheck found that the extractor behind the original walk
> could not see setter links `[[label|Target][$x += 1]]` or raw `<a data-passage>` anchors, so
> **eight of the twenty-five opening walks move** once it can:
>
> ```
> growup                26w  ->  8,132w        realm-of-corruption    7w -> 2,099w
> amore                  6w  ->    709w        wasteland-lewdness  1,004w -> 6,516w
> destroyer            531w  ->  3,272w        the-hellfire-club     681w -> 1,728w
> inseminator          305w  ->    582w        zaras-school-life   1,173w -> 1,482w
> ```
>
> `destroyer` was listed here as a **285-word cold open**. Those 285 words are its legal
> disclaimer — *"I am not the owner of any of the media or pictures used in this game…"* — and the
> walk stopped there because that passage leaves through `<a data-passage="intro1">`. Walked
> properly it is **eleven passages and roughly 3,300 words**, naming the father, the grandfather
> (who speaks, at length), the stepmother and the school bullies. A staged open by this table's own
> definition — and it moves the *cast* count as well as the *word* count, which is why the cast
> figure goes with them.
>
> Section K then tried to rebuild the walk three ways — stop at the first branch, greedy first link,
> and breadth-first to depth three — against the six openings this table used to name:
>
> ```
> game                        published  branch-stop   greedy    bfs-3
> corpo-life                         64           26     1586     9992
> the-company                       126          145     1056      985
> degrees-of-lewdity                193          197      197      197
> friends-of-mine                  1377          351     6677     2649
> new-life-project                 1558          202     2763     1551
> patriarch                        2619         2720     4409      704
> ```
>
> **Each lands on two or three of the six and misses the rest by four to seven times, and they do
> not agree with each other either.** The original walker is not on disk. A number no instrument can
> reproduce is not a measurement, and this skill has demoted five thresholds for less.
>
> **The rule loses nothing, because it never rested on the numbers.** It is a *consistency* rule —
> the cast load and the word budget have to agree — and the axis that separates the two shapes is
> the cast, which is checkable by opening the first passage and reading it. `findings_K_mirror.md` §4.

corpo-life's whole cold open, in full — who, job, place, why poor, what is at stake, zero characters:

> *"My name is [X]. I just got accepted into Chase-Bank, one of the most prestigious banks in New
> York city. After graduating from Stanford, I applied into the Management Trainee program and
> rented a small apartment near my office and am living frugally in order to live in this concrete
> jungle."*

**The defect is the middle.** A cold open carrying a staged open's payload names people the player
cannot picture, at a density the prose cannot support. Our own measured failure named **six people,
two of whom are not in the game at all**, and put none of them on screen — that count comes from
reading our own TOML, not from the field walk, and it stands.

**Pick one:**
- **Cold open** — name the player's situation and the pressure. Name **nobody**. The cast arrives
  later as content, each through F5's meeting. Around 150 words is a sensible target; it is an
  authoring figure, not a field measurement.
- **Staged open** — spend the words. One person enters at a time, is described, **speaks**, and
  states what they want. F6's craft bar applies to each entrance.

⚠️ **This is not a word-count rule, and after 2026-08-24 it does not carry a word count at all.** It
is a *consistency* rule: the cast load and the word budget have to agree. A 200-word opening that
names four people fails it; a 200-word opening that names none passes.

⚠️ **Named in passing is not met.** An offstage boss, a dead parent, a landlord who never appears —
these are world-building and they cost the reader a name to hold. Two of the six people named in
the measured failure **are not in the game at all**. If the player can never go and meet them, ask
whether the name is doing work, or delete it.

---

### The worked opening — cold open, naming nobody

The shape above, written out. Thirty-eight words: the situation, the pressure, and the thing to do
about it. No name, because nothing has earned one yet, and the cast arrives later through F5.

> The room came furnished, which means somebody else chose the curtains and then left in a hurry.
> Rent is due in nine days. There is a card on the fridge for a bar that is hiring, and the
> handwriting on it is not yours.

The last sentence is the hand-over: it is a door, and the player can walk at it on the next click.
Note what the beat spends its softeners on — *which means*, *in a hurry*, *not yours* — and see
`register.md` **How far is far enough** for why stripping them flattens the screen.

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

## F2b · The opening is SCREENS, and two of them are not ours

`[new] 2026-08-31.` **F1 through F10 are all about what the opening SAYS. Not one is about what the
player does with their hands.** That hole shipped straight into the first design built with
`the-sheets.md`: three beats were specified, and nothing said whether they were one screen or three,
what was written on the button between them, or what the player saw before any of it.

**Four facts settle it, and all four belong on the opening sheet.**

**1 · Screen one is the age gate, and we get it for free.** `Start` initialises state and renders a
title screen; the starting canvas is reached only through
`[[✓ I am 18 or older - Enter Game->StartingCanvas_<canvas>_Node_<node>]]` (`engine.md` §12). **The
player's first screen is never beat 1.** A sheet whose timeline opens on the first prose beat is
describing the second screen and calling it the first — which is exactly what the first draft did.

**2 · There may be a character screen in front of the game, and its words are not ours.**
`[player] customizable = true` with one `[[player.customization_fields]]` builds a
`CustomizeCharacters` passage **and repoints the age gate at it** (`v2.py:1065`, `v2.py:9251`). Its
headings and button are hard-coded — *"Customize Characters"*, *"Personalize the characters in your
story"*, *"Continue to Game"*. **Seven of fifteen built games ship that screen.** The only authored
text on it is `player_description` (`v2.py:9509`); an author who does not know that ships the
default, in a product voice, as the second thing a player reads.

**3 · One node is one screen.** The engine plays a node chain back one screen at a time (F2 above,
"this is not a size cut"). Three beats in one node is ONE screen carrying all three; three nodes is
three screens. Those are different things to sit through and the sheet has to say which.

**4 · The break between screens is a written button.** A mid-funnel node exits through
`exit_block.type = "choices"` carrying a single choice, and that choice's `text` is the button — a
line in the game's voice, not "Continue". `seventh_day`'s reads *"Get up before the others."* The
last node exits `type = "location"`, whose `config` carries `locationId`,
`time_progression_minutes`, `flagEffects` and `effects` — so **the handover is also where the opening
sets its flags and pays its first money.**

### The screen walk — the review view that cannot be faked

One row per screen, in order, with the button quoted. A screen either exists or it does not; intent
cannot satisfy a row. The timeline and the checklist both describe an opening, and **an opening never
broken into screens passes both of them.**

<pre>
  #  canvas · node                 what is on the screen                    the button
 ─────────────────────────────────────────────────────────────────────────────────────────
  0  Start            <b>engine</b>      title card · age gate                    ✓ I am 18 or older
  1  CustomizeCharacters <b>engine</b>   the fields declared, if any              Continue to Game
 ─────────────────────────────────────────────────────────────────────────────────────────
  2  boot · <i>node</i>                  …                                        "…"
     ── location exit ──►  the anchor, at a clock time · sets <b>flag</b>
  4  capstone · <i>node</i>              …                                        "…"
  6  <i>meeting</i> · <i>node</i>               …                                        "…"
 ─────────────────────────────────────────────────────────────────────────────────────────
     <b>THE FUNNEL ENDS.</b>  what is live on the screen it hands over to
</pre>

⚠️ **Rows 0 and 1 go in even though we do not author them.** Leaving them off is how a sheet ends up
describing an opening the player never has.

⚠️ **Every button is quoted, not summarised.** "the player continues" is not a row. If the line has
not been written, the screen is not finished.

### Measured: every opening we have built

```
seventh_day      5 screens  420 w        commuter         1    93
the_allowance    5          535          last_call        1    60
back_home        4          468          late_shifts      1    45
forty_miles      3          339          mothers_place    1   101
steam            3          285          mrs_vance        1   100
off_season       2          160          the_inheritance  1    31
vesper           2           89          the_route        1   136
                                         the_season       1   119
```

**Eight of fifteen open on a single screen**, then the sandbox. The largest true opening in the field
corpus is Course of Temptation's at **78 passages and 8,057 words** (F4b below). Length is the
author's decision; what the format requires is that the decision be **visible** rather than arrived
at by default.

⚠️ **The funnel should contain the job, done once.** Ours have been narration plus a name box; the
field's largest openings are funnels the player *acts* inside — Course of Temptation's carries seven
conditionals and not one refusal. A choice that colours and gates nothing is legal here and is the
only thing that teaches by doing.

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

## F4b · The opening refuses nothing

F4 says teach every live system. This is the half F4 implies and never states: **teach it, and do
not gate on it yet.** The first hour states the price. It does not enforce one.

Measured across the fourteen games in the mopoga top thirty that carry an identifiable opening —
their own `intro` / `prologue` / `chargen` tags where they have them, anchored passage names
otherwise (`findings_B_refusal.md` §5):

| | openings | spoken refusals in them |
|---|---|---|
| course-of-temptation, degrees-of-lewdity, become-someone, destroyer, apocalyptic-world, become-taxi-driver, inseminator, the-hellfire-club, patriarch, college-daze, zaras-school-life, wasteland-lewdness | **12** | **0** |
| new-life-project | 1 | 6 — its `intro` tag covers the tutorial |
| free-cities | 1 | 9 — its `intro` tag covers the settings screens |

**Twelve of fourteen openings refuse nothing out loud**, and the two exceptions are both tags
covering something other than a prologue. The largest true opening in the corpus — Course of
Temptation's 78-passage, 8,057-word prologue — contains **seven conditionals and not one refusal**.
Walking outward from each game's `startnode`, the first spoken refusal appears at link-depth 3 to 6
where it is reachable at all. The funnel is unconditional; refusals begin where it ends.

**What the opening does instead is hand over a bill.** Course of Temptation's mother attaches
$100/week in a conversation at the family dinner table, and degrees-of-lewdity's entire opening is a
rules briefing that locks nothing:

> "If you want to avoid trouble, keep your allure low by dressing modestly and sticking to safe,
> well-lit areas. Nights are particularly dangerous." — `Start2`

Section A found the same thing from the other side and it is stated there once: *state the pressure
in the first minutes, as a scene, not as a rule.* This rule is the constraint that follows —
**a locked door in the first hour is a door the player never learned they wanted.**

What this does **not** say: that the opening should be short, or that nothing in it may be
conditional. F1's two shapes still stand, and a conditional that picks which version of a beat to
show is not a refusal — see `the-surfaces.md` R5c, where 35% of the field's action-conditionals turn
out to be variant selectors.

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

**The field's answer.** 17 of 27 shipped games carry per-character meeting state, and the strongest
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

## F9 · A place says what it is on the screen the player keeps coming back to

**The location's own `description` says what kind of place this is and what happens here.** Not a
scene that plays once. The description is the only surface the player sees on *every* visit,
including the twentieth, and "what is this place" is a standing question, not a first-entry one.

**The measured failure, which is a DESCRIPTION failure.** One game's anchor — the room its ledger
budgeted at **9,000 words, 27% of the whole game** — reads:

> *"KESH AMUSEMENTS in eight-foot letters over the door, and under them forty machines, half of them
> off at the wall to save the electric…"*

Forty machines of **what**. It never says slot machines, never says amusement arcade, never says
people put money in them — and the player is put behind its counter on turn one and asked to work
it. *"What is arcade??"* was the first thing the human reader asked. That description is long,
specific and well written. Length was never the problem. **It never names the function.**

⚠️ **This is `register.md`'s "words the player has to already own", one level up.** There the unit
was a word; here it is a whole place. A location whose *function* is only implied is an unglossed
noun the size of a room.

### The field's device is the room screen, and it changes

Measured across the 26-game corpus:

```
                                    field median   the game that prompted this
room prose the player sees per visit   82 words              68
variant branches per room screen           10                 2
rooms that rotate their text              22%                0%
rooms that vary by hour                   17%                0%
an event renders ON the room screen       yes      no — ours <<goto>>s away from it
```

The place tells its own story every time you walk in, and it is not the same story twice.

### ⚠️ The first-visit canvas is a MINORITY device — do not reach for it first

This section previously taught the opposite, and worked its example from
`degrees-of-lewdity`'s `$forest_shop_intro` / `$gwylan_cafe_intro` family. Counted properly, that
family is **one game**:

```
degrees-of-lewdity   258 first-visit branches, 117 flags     the only game doing it
realm-of-corruption   12
amore · patriarch · sluttown-usa · zaras-school-life · new-life-project     2 each
EIGHTEEN OF TWENTY-SIX GAMES     zero
  — including destroyer, become-someone, course-of-temptation, the-company, friends-of-mine
```

It is a legitimate device and DoL builds a great deal on it. **It is not the default and it does not
substitute for a description that names the function**, because it plays once and the confusion it
is aimed at is permanent. A game shipped nine of them, went green, and had them reverted the next
day on exactly that ground:

> LO: *"I think the place name is description and what was going in that place should be able to
> tell the whole story."*

Reach for a first visit when a place has a **one-time** thing to say — a door that was locked and
now is not, a room whose meaning changes the first time you are let into it. Never as the place's
only introduction.

### Authoring the two halves

**State-variance — `[[locations.description_variants]]`, shipped 2026-08-26.** The base
`description` stays required and becomes the else; each variant is `{conditions, text}` and the
engine emits a first-match chain. Conditions are the ordinary ones, so the most useful axis is
**who is in the room** — which is the "what happens here" half of the rule, told by the room itself:

```toml
[[locations]]
id          = "the_yard"
description = "Gravel from the back step of the house to the roller door of the shop…"

[[locations.description_variants]]
conditions = { version = "1.0", logic = "AND", items = [
  { type = "npc_at_location", location_id = "the_shop_floor", operator = "is_present" },
] }
text = "…and the roller door is up. Air tools go in bursts and stop."
```

⚠️ **`version = "1.0"` is not optional.** `triggerConditionsSatisfied` returns **true** for any
`conditions{}` without it, so a variant missing it renders forever and the location's own
description is never seen again. The importer refuses it rather than building green.

⚠️ **There is no time-of-day condition.** The evaluator has `flag`, `trait`, `npc_at_location`,
`stage`, `quest`, `item`, `days_since_flag`, `corruption_level` and the clothing family — and
nothing that reads the hour. So the field's 17%-vary-by-hour column is still **not authorable**;
schedules gate canvases by time, not descriptions. Gate presence-variants on who is there instead,
which is where the hour shows up anyway.

⚠️ **A random ambient still takes the WHOLE screen, and that is an engine limit, not a choice.**
When a Lane 2 ambient rolls on entry the room `<<goto>>`s to it — no title, no description, no
portraits, no exits — so on that visit the description does not render at all. An `ambient_render =
"inline"` setting that gave the ambient the description slot instead was built and **reverted on
2026-08-26**; do not write doctrine or a ledger promise against it. `destroyer` renders its
encounter in the description position and keeps its affordance bar and exits either way, so the
shape is known and the gap is real — it is simply not available today.

### Rotation is still not built

The field's other column — 22% of rooms rotating their text between visits — needs a per-visit
counter like `block_pool`'s and does not exist for descriptions. Do not promise it in a ledger.

---

## F10 · The role stays attached after the introduction

F7 gets the role onto the screen at the meeting. **F9 says a place keeps saying what it is on every
visit. This is the same rule for people, and it is the one that was missing.**

"Who is this" is a **standing** question. A meeting answers it once, and the player then spends forty
visits in a hub where the man is a bare first name.

**The measured failure.** A game with six men: `npcs[].relationship` written well and landing each of
them in six words — *"Your husband's eldest, 29"*, *"Your husband's brother, 51"* — and **those
strings render on the cast page and nowhere else.** In the prose the player actually reads:

```
canvases   words   times his own surfaces say who he is
      14   2,594                 2          <- the spine of the game
      14   1,736                 2
```

Its author — who wrote every line of it — asked *"Who is Sherrod?"* off a location button. The other
game that drew *"I don't know who is who"* from the same reader had the same shape.

**Where it goes: the surfaces the player RE-ENTERS.** A hub, an ambient, a walk-in. Not the one-shot
that introduced him — that one is already doing its job.

**Both, never one instead of the other.**

> *"Relation and name both are important and both can't be replaced with another. We are not calling
> out for replacing one with another."*

⚠️ **Do not swap the name out for the relation on the speaker line.** `destroyer` does
(`<<speech "teagan" "Stepsister">>`) and it is the only game in the 26-game corpus that does — it
survives it by having **exactly one of each relation**, where the failure above has three men inside
one. Relation words on buttons run at **field median 0.4%, max 2.0%**. `sluttown-usa` is a family
premise with 37,408 speaker labels and uses **names only**. Swapping does not remove the memory tax,
it moves it: the player now has to remember who "Stepsister" is.

The cheap form is three words riding in prose that was going to be there anyway:

```
before   He has taken his jacket off and hung it on the back of the chair, which is as close as
         THIS MAN comes to being off duty.
after    …which is as close as YOUR HUSBAND'S ELDEST comes to being off duty.

before   CADE comes up for ten minutes on a Friday and stands rather than sits.
after    CADE — YOUR HUSBAND'S ELDEST, and the only one of them with a reason to be in this
         kitchen — comes up for ten minutes on a Friday…
```

Name and relation on the same line, at the point of use, and the register does not move.

**Put it in a `block_pool` variant rather than in the always-renders text.** A hub pool cycles, so
the anchor recurs periodically instead of arriving every single visit, which is how a reminder turns
into nagging.

### The mechanical half — `npcs[].role`

Prose anchors recur every few visits. The **dialogue box** carries it every time somebody speaks:

```
[face]  Cade
        husband's eldest          <- npcs[].role
        "Slower. You're not doing the books now."
```

```toml
[[npcs]]
id           = "npc_cade"
name         = "Cade"
relationship = "Your husband's eldest, 29. He runs the yard…"   # the cast page's sentence
role         = "husband's eldest"                                # the label under the name
```

**Three rules, and the third is the only one a gate can hold:**

- **No "Your".** It is on every label, so it carries nothing and eats width in a small line.
- **One to three words.** A sentence belongs in `relationship`, which the cast page renders.
- **Unique in the cast.** `brother` is fine with one brother and useless with two. The importer
  **refuses two roles that match** — that is the whole reason the field is worth having.

When the relation word repeats, the label carries whatever actually separates them — birth order,
side of the family, or a place:

```
two brothers            elder brother · younger brother
three of his sons       husband's eldest · husband's middle son · husband's youngest
him and his brother     husband · brother-in-law
your brother + his      brother · brother-in-law
two uncles              father's brother · mother's brother
two housemates          housemate, top floor · housemate, back room
no kin word at all      the canteen · the night shift
```

⚠️ **Author it. Never derive it, not even as a default.** Deriving from `relationship`'s first
clause is the obvious idea and it collapses real casts: **five of one game's six relationship
strings contain "husband"** (the husband, his three sons, his brother), and another game has two
characters whose strings both begin *"Your brother"* — and that is the game whose reader said
*"I don't know who is who."* A silent wrong default is worse than a missing one, because nobody
would notice five people labelled `husband`. Empty renders no line at all, which is the safe default.

⚠️ **`role` is not a swap for the name.** `destroyer` replaces the name with the relation
(`<<speech "teagan" "Stepsister">>`) and is the only game of 26 that does — it survives on having
exactly one of each relation. Swapping does not remove the memory tax, it moves it: the player now
has to remember who "Stepsister" is. Both, at the point of use.

---

## What the scoreboard checks

Two gates and two lints. `python3 scripts/gates.py <slug>`.

| | |
|---|---|
| gate · **the opening hands over into an open door** | F3. Walks the funnel's clock and asks whether anything at the landing location is open at that minute. **n/a** when the landing location cannot be resolved. |
| gate · **every hub is met first** | F5 + F8. Per character: **one** hub gated on a flag a non-repeatable canvas naming them sets, **no** hub left with zero conditions, and no such flag opening a second character's door. |
| lint · **the place says what it is** | F9. Lists every location by how much prose happens there, against how long its own description is. **Whether a description names the function is a reading, not a measurement**, so this is a list to read and never a score. It replaced a gate that required a first-visit canvas at the anchor — a device eighteen of twenty-six top games do not use. |
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
- **Pick one opening shape** — cold open names nobody; staged open puts each person on screen and
  lets them speak. The middle is the defect. (The word ranges this line used to carry were deleted
  2026-08-24 — F1.)
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
- **A place says what it is in its own `description`**, which the player reads on every visit — the
  function first, then the flavour. A first-visit canvas is a minority device: take one only for
  something true once.
