# The First Hour — the opening, and the people in it

Everything between the title screen and the moment the player is on their own: the opening funnel,
the first time each character is met, and the first time each place is entered.

This file owns **one rule** with three faces, and every section below is that rule applied:

> **The game does not use a name until it has earned it.** People, places, things. Before the
> player has met it, the game says what it *is* and where. After, it says the name.

**Why this file exists at all.** v1 carried two files that did most of this job —
`author-game/references/onboarding.md` (269 lines) and `npc-intro.md` (146 lines). v2 shipped
without either, and this file puts that job back. This is `DOCTRINE_GAPS.md` Tier 2 row 6, and it
was the last row in that table with an empty status column.

Engine claims here carry a `file:line` into
`apps/game_generation/twee_comprehensive/generators/v2.py`, per `SKILL.md` operating rules.

## Contents
1. F1 · The opening picks one shape and commits
1b. F1b · The opening's shape (setup → … → gameplay)
1c. F1c · A returning player can skip the opening
2. F2 · Boot and capstone are two canvases
3. F3 · The opening hands over into an open door
4. F4 · Every live system gets one beat
4b. F4b · The opening refuses nothing
5. F5 · Every character's hub sits behind a meeting
6. F6 · A meeting is small, and somebody speaks
7. F7 · Role before name
8. F8 · The flag belongs to a scene that meets them
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

**This is a consistency rule, not a word count.** The cast load and the word budget have to agree,
and the axis that separates the two shapes is the cast, which is checkable by opening the first
passage and reading it. `findings_K_mirror.md` §4.

corpo-life's whole cold open (structure only; it fails the adults-only rule) is one paragraph: who
she is, the job, the city, why money is tight, what is at stake — and zero characters.

**The defect is the middle.** A cold open carrying a staged open's payload names people the player
cannot picture, at a density the prose cannot support, and puts none of them on screen.

**Pick one — and the default is staged.** Since 2026-09-24 the skill writes in the loud voice
(`register.md`, "The voice — say it loud"), and that voice needs people on screen talking. The
opening is a **staged open** unless there is genuinely no person to put on screen.
- **Staged open (default)** — spend the words. One person enters at a time, is described,
  **speaks**, and states what they want. F6's craft bar applies to each entrance. The shape is F1b
  below.
- **Cold open** — only where no person is on screen: name the player's situation and the pressure,
  name **nobody**, and let the cast arrive later through F5's meeting. Around 150 words is a
  sensible target; it is an authoring figure, not a field measurement. The loud voice still
  applies — her situation said plainly, her feeling about it said out loud.

⚠️ **This is not a word-count rule, and after 2026-08-24 it does not carry a word count at all.** It
is a *consistency* rule: the cast load and the word budget have to agree. A 200-word opening that
names four people fails it; a 200-word opening that names none passes.

---

### F1b · The opening's shape — setup, problem, person, conflict, choice, temptation, objective, play

Added 2026-09-24. LO chose it on 2026-09-23 over the old shape, after reading a comparison of 26
top games' openings: the top games tell the player who she is, what the problem is and what to do,
put people on screen who want things, and end on a question. The old opening shape was *wake up → routine → leave → the job*, and it ended on a quiet
literary line. The new one:

```
setup → problem → character interaction → conflict → choice → temptation → first objective → gameplay
```

**What each piece has to do:**

1. **The first screen states it plainly:** who she is, the problem, what she wants, and her voice.
   Said, not implied (`register.md`, the voice, rule 1). F2b's field figures still hold for its
   length: median 144 words. **"Loud is not long" applies to every other screen:** when a screen
   has to carry several jobs, split it into two screens rather than write one wall.
2. **The first person on screen talks, pushes, and wants something from her.** Someone speaks →
   she answers → they push → she thinks. Who they are, what they want and how they feel about her
   in the first lines.
3. **A first choice inside that first character scene**, not after the opening. Its consequence
   is **visible as a reaction line** plus the engine's toast, or as a real flag named on the button —
   never a `+X` for a stat that does not exist (`the-meters.md`, "What the player is shown"). **How it is built:** the reaction is the first
   line of the node the choice leads to. When the reactions differ, each choice gets its own short
   node that opens on its reaction and then rejoins the scene. That costs the player one click per
   choice, and it is the shape: the engine has no other place to print a line after a click.
4. **An early temptation** in the first few scenes: attraction, tension, a look, a suggestive
   choice. The player should know within minutes that sex is what this game is about. A hot moment
   here comes from a stranger or a one-off, never the paid route or the main man (`the-arc.md` A15). 15 of 26 top
   games put something tempting in the opening and 3 put explicit sex there; 8 put nothing
   (measured 2026-09-24 in the 26 games' own source).
5. **The first objective is a quest card with goal steps.** Not a tip alone: `goals`, so the page
   prints what is done and what is next (`the-voice.md` R3b). 21 of 26 top games give "what next"
   text, and progression questions are the players' number-one comment topic: 8.4% of all comments,
   in 30 of 30 games (measured 2026-09-24). Lint `the opening arms a card with goals`. The goal
   shape is `engine.md` §47's: `flag` or `trait`, with `subject`, `op`, `value` and `label`. A
   `type` key is ignored by the importer (`template_import.py:1278-1315` never reads it).
6. **Plain tutorial lines on the last screen**, in the game's own plain voice (`the-voice.md`):
   money, work, exploring, people, choices. *"You need money. Take shifts at the bar, or find
   another way."* This is the one place the story text may explain a system directly. F2b's warning
   about the developer talking is about screen one and patch notes, not this. **These lines are the
   game's voice, not a scene**, so the voice's rule 5 (more dialogue than narration) does not apply
   to them. Give them their own screen, or put them under the card, rather than inside a scene that
   has to talk.
7. **It ends on a hook:** a money problem + the objective + a mystery + a person + a choice. Not a
   quiet last line.

**Meeting several people in one opening.** A staged opening often meets two or three people in
one scene. One flag for the group is enough when the scene names each of them (F8).
`requires_npc` takes one person, so a meeting with several people leaves it off, and uses the
trigger's schedule window to put the scene where they all are.

⚠️ **A walk-out is not a refusal.** F4b still holds: nothing in the opening says no to her. A
button that lets her leave the job offer is her choice, and the offer stays open.

### The worked opening — staged open

The shape above, as screens. Every person is a role, every number is filler, and none of it is a
world to copy (`register.md`, "Show the mechanism. Never show the world."). Each screen was scored
with `gates.py --beat`; the numbers are under it.

**Screen 1 — setup, problem, her voice.**

> You're nineteen, you just moved to a city where you know nobody, and rent is due on Friday. You
> have a tenth of it. You're broke, and everybody in this building can tell.
>
> *This is fine. This is totally fine.*

*40 words · median sentence 6 · gloss 0 · history 0.*

**Screen 2 — the first person, the conflict, the first choice.**

> The landlord is waiting on the stairs like he's been counting the minutes.
>
> "Friday. All of it. I don't do sob stories."
>
> "You'll get it."
>
> "With what?" He looks you up and down, slow. "You've got a job I don't know about?"
>
> *Here we go.*

| button | what is printed after the click |
|---|---|
| **Tell him you'll find work today** | *He grunts. It's almost approval.* |
| **Tell him it's none of his business** | *His face goes hard. He writes something on the back of an envelope.* · sets `<landlord_crossed>` |
| **Say nothing and go past him** | *He watches you all the way down the stairs.* |

*45 words · 49% spoken · median sentence 5. The reactions are lines, not stats. The one that
matters later sets a real flag, and only that one.*

**Screen 3 — the temptation.**

> The guy from across the hall comes out in a towel and nothing else. He sees you and stops dead.
>
> "Oh. You're the new one."
>
> He takes a long look at your legs before he remembers where your face is. You caught it. He knows
> you caught it.
>
> *He's a mess. So why is your face hot?*

*57 words · median sentence 6. The tension is named (rule 8), and the question she asks herself is
the hook for that person.*

**Screen 4 — objective, tutorial, hook.**

> You need the rent by Friday. The bar downstairs is hiring.
>
> And the manager just offered you double for a shift in the back room. He wouldn't say what
> happens in the back room.

The card it arms, with goal steps:

```toml
[[quest_cards]]
id = "card_rent"
text = "Make the rent by Friday."
when = [ { flag = "opening_done", op = "is_true" } ]
goals = [
  { flag = "<took_first_shift>", subject = "player", op = "is_true", label = "Take a shift at the bar" },
  { flag = "<asked_about_back_room>", subject = "player", op = "is_true", label = "Find out what the back room is" },
]
tip = "The bar opens at six. The manager is behind the counter."
```

And the plain lines on the same screen: *You need money. Take shifts at the bar, or find another way.
People are in different places at different hours. What you say changes how they treat you.*

*34 words of story · median sentence 9. Money problem, objective, mystery, person and a choice in
two sentences each side of the card.*

## F1c · A returning player can skip the opening

Put one choice on the opening's first screen — *read it* or *skip it*. Fifteen of 26 top games offer a
skip (Process Review, Round 1, numbers only), and all four passing games do: In Her Own Hands
[SkipPreface] (*"No, skip the Preface"*), Course of Temptation [QuickstartMenu], Shady Deals' "Custom
Start", Cupid's Way's "Skip Prologue". The skip sets every flag the opening sets and lands where the
opening hands over, so nothing downstream — `the opening opens a door` included — can tell the difference.

## F2 · Boot and capstone are two canvases

The checker and the template both assume this shape. Gate `the opening opens a door`
(gates.py:9424) judges the handover at the end of the capstone the funnel walks into (`_capstone_at`,
gates.py:5086), and `templates/first-hour.toml` A1 is the boot and sets `opening_done`.

The shape:

- a small **boot** one-shot — the `starting_canvas`, high `priority`, `is_repeatable = false`.
  It puts the player at the start location and begins the chain. It does not carry the cast.
- a separate **capstone** one-shot at the same location, gated on the flag the boot sets, where the
  prose is allowed to spend.

Both auto-fire on entry through `selectAutoFireCanvasForLocation`, which picks the highest-priority
valid **non-repeatable** canvas and skips every repeatable (`v2.py:5755-5776`). The flag gate is
what guarantees order — no schedule is needed.

**The checker follows the boot into the capstone.** Since 2026-09-25, `gates.py` walks the
funnel from the starting canvas, through its location exit, into a one-time canvas at that location
whose trigger flags the funnel has set, and judges the handover at the end of *that*. Before, it
stopped at the boot's exit and judged the hop to the capstone as if it were the handover. Node ids in
the funnel may be bare (`"hall"`) or qualified (`"canvas_opening.hall"`); the engine keeps the last
segment (`v2.py:14610`), and so does the walk.

⚠️ **This is not a size cut.** Build the opening at full designed size; the engine plays a node
chain back one screen at a time. "Two canvases" is about *what each one is for*, not about brevity.

---

## F2b · The opening is SCREENS, and two of them are not ours

`[new] 2026-08-31.` **F1 through F10 are all about what the opening SAYS. Not one is about what the
player does with their hands** — whether three beats are one screen or three, what is written on
the button between them, or what the player sees before any of it.

**Four facts settle it, and all four belong on the opening sheet.**

**1 · Screen one is the age gate, and we get it for free.** `Start` initialises state and renders a
title screen; the starting canvas is reached only through
`[[✓ I am 18 or older - Enter Game->StartingCanvas_<canvas>_Node_<node>]]` (`engine.md` §12). **The
player's first screen is never beat 1.** A sheet whose timeline opens on the first prose beat is
describing the second screen and calling it the first.

**2 · There may be a character screen in front of the game, and its words are not ours.**
`[player] customizable = true` with one `[[player.customization_fields]]` builds a
`CustomizeCharacters` passage **and repoints the age gate at it** (`v2.py:1130`, `v2.py:10033`). Its
headings and button are hard-coded — *"Customize Characters"*, *"Personalize the characters in your
story"*, *"Continue to Game"*. The only authored
text on it is `player_description` (`v2.py:854`); an author who does not know that ships the
default, in a product voice, as the second thing a player reads.

**3 · One node is one screen.** The engine plays a node chain back one screen at a time (F2 above,
"this is not a size cut"). Three beats in one node is ONE screen carrying all three; three nodes is
three screens. Those are different things to sit through and the sheet has to say which.

**4 · The break between screens is a written button.** A mid-funnel node exits through
`exit_block.type = "choices"` carrying a single choice, and that choice's `text` is the button — a
line in the game's voice, not "Continue". The
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

### How long the opening is

The largest true opening in the field
corpus is Course of Temptation's at **78 passages and 8,057 words** (F4b below). Length is the
author's decision; what the format requires is that the decision be **visible** rather than arrived
at by default.

⚠️ **The funnel should contain the job, done once.** The
field's largest openings are funnels the player *acts* inside — Course of Temptation's carries seven
conditionals and not one refusal. A choice that colours and gates nothing is legal here and is the
only thing that teaches by doing.

### What the field's FIRST screen actually is — 2026-09-02

Walked all 25 parseable games from their declared `startnode`; the scaffolding/fiction boundary was
**read**, not scored, because the auto-classifier called `sluttown-usa`'s 1,999-word **changelog**
"fiction". 19 resolve; 6 chains end inside character creation.

> **Median 2 screens of scaffolding** (range 1–8) before any fiction · **first fiction screen median
> 144 words** (range 29–8,404) · **median 2 links** · **11 of 19 end on a real choice**, 8 on a
> single Continue.

**Two openings worth copying.** The reference game (numbers only) spends **141 words** putting an
obligation that comes back on the player: the debt, the term and the threat, then a free first
choice. `the-hellfire-club` spends **144** on year, city, why she is
there, who she is meeting, *ten shillings in your pocket* — and ends on **three** ways to cross
London. Both are inside the median. Neither explains a system.

⚠️ **The most common way a top game wastes its first screen is the developer talking.**
`apocalyptic-world` (#1, 7,861 comments) opens on a version number, a request for forum feedback, and a
systems lecture — *"Reputation… People… you can acquire people in several ways"*. `become-someone`
opens on patch notes; `family-business` and `sluttown-usa` on changelogs. **This is prevalent and it
is still wrong** — on the FIRST screen, before any fiction, in the developer's voice. Being common
in the field is not an argument; `the-clock.md` C2 and `the-economy.md` R3 both already refuse a
field majority where the reasoning is against it.

⚠️ **Narrowed 2026-09-24.** This warning used to be read as "never explain a system anywhere in the
opening". It does not cover F1b's plain tutorial lines on the opening's **last** screen — short,
in the game's own plain voice, after the player has met the people and the problem. What stays
wrong is the version number, the forum request, the patch notes and the systems lecture standing
where the story should start. F4 still asks for a beat that arms each system; the tutorial line
says what the beat just showed.

⚠️ **But the long backstory prologue is a genuine shipped shape, and the #2 game is one.**
`destroyer` (7,686; numbers only) opens on **ten screens, ~2,900 words, one link each** before the
world opens. `patriarch` runs four; `family-ties` opens on an
8,404-word prologue. So F1's short cold open is a *default*, not a law. What no game does is **both**
a prologue and a systems explainer. Study:
`~/Documents/Opening_And_Introduction_Study_20260902/`.

---

## F3 · The opening hands over into an open door

The last click of the funnel puts the player somewhere, at a clock time, and that place has to have
something live in it **at that minute**.

The failure, computed exactly the way the gate computes it:

```
[time] starting_hour = 7                                  07:00
node -> node, no time declared -> default 3 min           07:03      v2.py:15596
node -> node, no time declared -> default 3 min           07:06
exit: time_progression_minutes = 30, to the_diner         07:36

at the_diner, 07:36:
  work_diner_breakfast     schedule 08:00-13:00     CLOSED
  work_diner_afternoon     schedule 13:00-19:00     CLOSED
  work_diner_late          schedule 21:00-01:00     CLOSED
  walkin_diner_counter     substitution_only        never renders on its own
  amb_diner_rain           trigger_mode = random    not guaranteed
  amb_diner_regular        trigger_mode = random    not guaranteed
```

**The player's first free act in that walk is pressing a wait button.** This is v1's §2.7
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

The phone is a channel, and it is armed the same way: by the first scene flag that causes a text
(`the-phone.md` P4). Its first thread arrives because a scene happened, not because `[phone]` exists.

The field arms its wardrobe inside the opening. Course of Temptation's [Prologue6c] has her *"look
over your wardrobe, picking out something in your usual style."* and puts the outfit picker on
that same screen.

The sidebar is the other half and it is permanent: a banded stat reading near-empty against its
ceiling **is** the "there is a climb ahead" read, on frame one, with no teach screen. See
`the-meters.md` and `the-voice.md` for what goes on it.

> ### ⚠️ Arming a system is not the same as putting a door to it on the screen — and for the wardrobe the engine already put one there.
>
> Declaring `wardrobe_location` renders `[[Change Clothes->WardrobePage]]` on that location's screen
> unconditionally (`v2.py:11209`, and `:11141` for the entry-gated variant); `shop_location` does
> the same with `Browse Clothes` (`:11214`, `:11146`). It is above the portrait row and above the
> activity list, on every visit, needing nothing from you.
>
> So an authored canvas called *"The wardrobe"* at that same location is a **second door beside the
> engine's**, and it will be the one that does not work: its exit has to route somewhere, and
> nothing you write reaches `WardrobePage` the way the engine's own link does. Do not author one.
>
> **What F4 asks for here is the wardrobe's first-release minimum, not a door.** Round 9a's
> smallest wardrobe that does not feel empty is Shady Deals' early shape — cheap clothes, a style
> number, one gate reachable on day 1:
>
> 1. **one number** the world reads: `worn_exposure`, with the states read through it
>    (`the-meters.md` W7);
> 2. **one gate reachable on day 1, with a notice**: set it at what day-1 clothes can reach (Shady
>    Deals' gate of 10 is exactly the best day-1 score from the cheapest shop), and the block says why;
> 3. **the leave rules**: a daring price to go out in each revealing state, carried by the
>    destinations' `entry_conditions` (`engine.md` §17);
> 4. **one event** fired from a revealing state;
> 5. **one line**: a person who notices what she has on.
>
> Then grow by adding readers, not items: Shady Deals' log shows about 13 wardrobe entries over 20
> versions, each one a new reader (round 9a §4). The reads belong in ordinary places, not in sex
> scenes (W7). The gate that measures the floor is `the wardrobe is read`.
>
> ### ⚠️ And a read is only armed if something she can GET satisfies it.
>
> A clothing condition that names a property only unobtainable garments carry is dead, and so is
> everything gated behind it — an arc step that can never be entered, and every step after it.
> The shop only lists a garment that is not `initial` and has `price > 0` (`v2.py:2333`).
>
> **So the check is two-part:**
>
> ```
> 1. something in the world reads the wardrobe
> 2. something she can OBTAIN satisfies that read
> ```
>
> Part 2 means one of: the property lives on an `initial = true` garment; or `[settings]
> shop_location` names a **declared location** and the garment has `price > 0`; or a
> `wardrobeEffects = [{ item_id = "…", action = "add" }]` grant exists on a choice or an
> `exit_block.config`. Those are the only three routes the engine has. `shop_location` is never
> validated — a typo is as silent as an omission — so after a build, check
> `grep -c "Browse Clothes" <output>/index.html`. The gate is `a declared garment can be got`
> (`the-meters.md` W3).
>
> ### ⚠️ Nothing non-repeatable may live at the `shop_location` or the `wardrobe_location`.
>
> Both injected links are emitted **inside** the `<<if _autoFire>><<goto _autoFire>><<else>>`
> branch (`v2.py:11158` and `:11225`), and `getStoryCanvasRedirect` fires on a non-repeatable canvas
> *or* a `trigger_mode = "random"` one. Put a one-shot meeting or a random walk-in in that room and
> the door to the wardrobe or the shop is invisible until it has fired. Pick a room with neither —
> and note that most corpus shop locations are bare rooms for exactly this reason.

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
$100/week in a conversation at the family dinner table, and degrees-of-lewdity's entire opening
(structure only) is a rules briefing that locks nothing.

Section A found the same thing from the other side and it is stated there once: *state the pressure
in the first minutes, as a scene, not as a rule.* This rule is the constraint that follows —
**a locked door in the first hour is a door the player never learned they wanted.**

What this does **not** say: that the opening should be short, or that nothing in it may be
conditional. F1's two shapes still stand, and a conditional that picks which version of a beat to
show is not a refusal — see `the-surfaces.md` R5c, where 35% of the field's action-conditionals turn
out to be variant selectors. Nor is a button that lets **her** walk out (F1b): the choice is hers,
and the door stays open behind her.

---

## F5 · Every character's hub sits behind a meeting

**The forbidden shape:** a repeatable canvas with `npc =` set whose base node *is* the
introduction. The player walks into a room and the character is simply there, the hub's first
paragraph standing in for a meeting. The field does the opposite: Shady Deals' [Car Mechanic]
opens on `<<if $met_mechanic == 0>>`, so the first visit is the meeting.

**The field's answer.** 17 of 27 shipped games carry per-character meeting state, and the strongest
one carries it on effectively its whole navigable cast — degrees-of-lewdity keeps a first-time flag
on **24 of its 27 registered NPCs** (`C.npc.<Name>.init`, plus older `_intro`/`_seen` flags for the
rest), read in conditions 150 times. become-someone gates **presence**, not just dialogue:
`<<if $has.metkate is 1 && $kate.loc is "Beach">>` — she is not in the world until she has been met.
the-company sets `player.met.sophie` in a passage named `Intro-MeetSophie`.

**Re-measured 2026-09-02 over the 25 parseable games, and the second figure is the one that
settles it.** 14 games keep an explicitly-named per-character first-contact flag — **9 of the top
10 by engagement** — across **209 characters, 188 of them (90%) read inside a condition**:
degrees-of-lewdity 78, become-someone 31, corpo-life 30, wasteland-lewdness 20, patriarch 10,
lust-for-life 9, destroyer 7, zaras-school-life 7. Conventions differ and the mechanism does not
(`$amanda.intro`, `$janet.metFlag`, `$meet_megan`, `$metellie`, `$crowlemet`, `$gwylanSeen`).

> ### ⚠️ Not one character in the field is met at turn one.
> Every meeting flag in all 14 games, swept for an initialisation to true before play: **zero**.
> Three look like exceptions and none is — `become-someone`'s sits in `Start up Interviews`
> (mid-game), `corpo-life`'s in `CFO Dinner Init` (a scene), and `degrees-of-lewdity`'s in
> `Widgets variablesVersionUpdate`, the **save-migration** widget that back-fills old saves.

**And the field gates PRESENCE on it, not just dialogue** — which is the half our engine is missing.
`become-someone`'s Beach passage is a location screen listing who is there, and every row asks two
questions:

```
<<if $nami.intro   && $nami.loc   is "Beach">>
<<if $amanda.intro is 1 && $amanda.loc is "Beach">>
<<if $nicole.intro && $nicole.loc is "Beach">>
```

`renderNpcPortraits` (`engine.md` §42) does the **located** half and nothing else. `met AND located`
is the shape; the meeting flag on the hub's `trigger.conditions` is how you write the other half here.

`zaras-school-life` (numbers only) stages the meetings rather than opening them all at once, and
the trigger is a counter rather than a door: one meeting waits for the fourth time she has done a
routine, another for day 5 **and** a reputation of 10.

**The shape to build:**

| | |
|---|---|
| the meeting | `is_repeatable = false` · high `priority` · location-bound · sets one flag on exit |
| the hub | `is_repeatable = true` · **`[canvases.trigger] npc =`** set (F5b — the nesting is load-bearing) · gated on that flag · a **different** `name` |

> ### The second shape: the hub can hold its own first contact
>
> Two canvases is the shape to reach for, not the only one the field ships. **`corpo-life`**
> (1,464 comments) opens *Mia Office Interaction* with `<<if $metmia is 0>>` and gates everything
> after on `$metkaren is 1` — **one canvas: the first visit is the meeting, every visit after is
> the hub.** `become-taxi-driver` and `amore` do the same.
>
> The rule underneath both is **first contact is gated and happens once**. The canvas count was
> never the point. Use the two-canvas shape by default — it keeps the meeting's prose off a screen
> the player re-enters forty times, which is `register.md`'s whole argument — and use the one-canvas
> shape when the meeting is two lines and a door.
>
> ⚠️ **The gate cannot see the second shape, and this is the honest statement of that.** A detector
> was built and reverted the same hour: the only rule available to it — *"the canvas branches on a
> flag it also sets"* — is satisfied by **every day cap** and every arc rung as well. Nothing in
> the TOML distinguishes *first contact* from *third rung*: both read a flag `is_false` and set it
> on the way out. A lenient check would silently pass
> games that really are cold-spawning, which is worse than under-reporting. **So if you build the
> one-canvas shape, `every hub is met first` will under-count you — record it in the ledger and
> move on.** Field study: `~/Documents/Opening_And_Introduction_Study_20260902/`.

**Where a character has several hubs**, the meeting flag belongs on the **first** one — the hub
the player reaches first. A later rung can be gated on something downstream instead (`nora_loop`
on `nora_stage gte 3`, `canvas_paul_arrangement` on `paul_drinks_done`) and that is correct
work. What is never correct is a hub with **no conditions at all**: it puts that character's
portrait on a location screen from turn one, however well the first hub is gated.

A non-repeatable canvas renders **no portrait** — `selectNpcPortraitCanvasesForLocation` skips
`if (!c.isRepeatable) continue` (`v2.py:5793`) — so the meeting cannot leak onto the location
screen as a face, and the hub cannot appear before the meeting has fired.

> ### ⚠️ `requires_npc` does NOT gate the auto-fire path. This corrects v1.
>
> `npc-intro.md` §1.3 says to set `requires_npc` so the meeting *"fires where the NPC is."* Traced
> in the engine, that is **false** for a canvas that auto-fires:
>
> ```
> getStoryCanvasRedirect              v2.py:6305
>   -> selectAutoFireCanvasForLocation    v2.py:5755
>     -> isCanvasValid                    v2.py:5919
>        checks: schedules · conditions · repeatability.  requiresNpc is never read.
> ```
>
> `requiresNpc` is emitted at `v2.py:13596` and read on the random-encounter selector
> (`v2.py:6648`), the substitution rules (`v2.py:6727`), and — through `setup._npcPresentForCanvas`
> (`v2.py:5889`) — the solo lane (`v2.py:5830`, `:6479`) and the launcher (`v2.py:3663`).
> **None of them is auto-fire.**
>
> Consequence: a meeting bound to a bar with `requires_npc`, whose character's schedule puts him
> there only in the evening, auto-fires whenever the player walks in with the other conditions
> met — so the prose can introduce him in an empty bar at ten in the morning.
>
> **Gate the meeting on a `schedules` window that matches where the character actually is, or on a
> flag the player can only hold by having been there.** Keep `requires_npc` as well — it is free,
> it is correct on the paths that read it, and it documents intent — but never rely on it alone.

> **Gated as `a meeting fires where they are` (G38).**
>
> ⚠️ **When doctrine and the schema comment disagree, the schema wins, because the schema is what
> is open while you type.** `template_import.py` once described `requires_npc` as something that
> *"lets authors drop per-canvas location+time gates"*, with no scope on the claim — false for
> every meeting canvas. The comment is corrected (`template_import.py:817`); the gate is why it
> cannot come back.

---

## F5b · The portrait is the presence gate, and the key that makes it is `[canvases.trigger] npc`

F5 says the hub carries `npc =`. **It goes at the top level of `[canvases.trigger]`, and the
nesting is the whole rule.**

```toml
[[canvases]]
id   = "hub_theo_garage"
name = "Sit with him"
# npc = "npc_theo"        ← WRONG. Silently discarded.

[canvases.trigger]
location = "the_garage"
npc      = "npc_theo"     # ← RIGHT.
```

`TemplateCanvas` has four content fields and `npc` is not one of them
(`template_import.py:965-972`), and it is built with named arguments only
(`:2423-2431`), so a canvas-level `npc` key is dropped with **no error, no warning, and a green
build**. The field the engine reads is `TemplateTrigger.npc` (`:684`), carried through
`game_graph.py:311` into trigger metadata, out at `v2.py:13513`, and emitted as `npcId`
(`v2.py:13588`).

**Three things ride on that one key, and all three fail together.**

1. **The face.** `renderNpcPortraits` and its selector both bail on `if (!c.npcId) continue`
   (`v2.py:6354`, `v2.py:5797`). No `npcId` anywhere in a game means `renderNpcPortraits` returns
   the empty string at every location, for every hour, for the whole run.
2. **The presence gate.** The portrait renderer is where a character's hours are actually enforced:
   it reads their declared `[[npcs.schedules]]` and compares `getNpcLocation` to where the player is
   standing (`v2.py:6389-6398`). Lose the portrait and you lose the check — the surface stays
   clickable in an empty room at any hour.
3. **The label.** A canvas with no `npcId` falls through to the solo path, which does not skip it
   (`v2.py:5915`) and writes the canvas's own `displayName` straight into the link
   (`v2.py:5946`). The portrait path would have written the resolved character name. So the title
   you wrote for the author's benefit becomes the words on the player's screen — `@` tokens and all,
   because `name` is not a field the engine resolves tokens in (`engine.md` §43).

> ### ⚠️ `requires_npc` is a different field. It gates the row; it does not draw the face.
>
> **Corrected 2026-09-03.** It is now read on three paths — `trigger_mode = "random"`,
> `substitution_only`, and **the solo lane**, through `setup._npcPresentForCanvas`. A solo-lane row
> carrying it renders only while that character is standing where the player is. It still does
> **not** gate the auto-fire path (`engine.md` §31), and it still draws no portrait.
>
> A hub carrying `requires_npc` and no `npc` still has no face and no portrait window. Where a
> person-bound surface genuinely should not be a portrait — an activity that happens in a place
> while somebody is around, rather than a surface on that person — `requires_npc` now does the
> presence half on its own, and `trigger.schedules` remains what narrows it to a *time*.

A game with `npc` on `[[canvases]]` for every character surface ships with zero portraits: every
character renders as a text link carrying the canvas's own name, and every character's hours are
enforced nowhere. The copyable block in `templates/first-hour.toml` carries `npc` under
`[canvases.trigger]`; the only other `npc =` example in the skill is `[[phone.daily_topics]]`,
where it genuinely is a top-level key.

> **Gated as `no canvas key is discarded`.** Fails on any key sitting on `[[canvases]]` that is not
> one of the seven `TemplateCanvas` fields (`template_import.py:1069-1075`). It invents no threshold
> and cannot produce a false positive: such a key does nothing at all, so writing one is never
> correct.
>
> ⚠️ **The class is the placement, not the key.** `substitution_only` one level too high fails the
> same way: the walk-in renders as a clickable activity instead of a dispatcher-only target. So the
> gate checks every key, not `npc` alone.
>
> The companion lint **`bound to a person, no face`** carries the softer case — a repeatable
> `requires_npc` canvas with no `trigger.npc` — as a **list, never a score**. A walk-in, or a scene
> that happens in a place while somebody is around, legitimately has this shape, often already
> windowed by its own `trigger.schedules`; a gate here would fail games for obeying the doctrine.

⚠️ **One location shows one canvas per character.** The renderer collects every valid repeatable
canvas for an NPC and keeps the highest `priority`, preferring affordable over cost-blocked
(`v2.py:5781-5814`). Three surfaces for one person in one room is not three rows — it is one face
showing whichever ranks highest right now. That is the intended shape and it composes with the
tier ladder, but decide the priorities on purpose: a hub at 6 sitting under an escalation at 7 means
the escalation replaces it whenever its conditions hold.

### So a second surface for the same person in the same room is a NODE INSIDE THE FIRST.

Written as its own canvas, a talk screen cannot take `npc` without the hub swallowing it (the
selector keeps one canvas per character, `v2.py:5804-5807`), so it lands in the solo lane — the one
that holds Sleep and Shower and attaches no name to anything — with its button text as its only
identity. Folding it into the hub does not bury it: **a node has no priority.** Priority ranks
canvases competing for one face. A node is reached by a choice.

```toml
# on the hub's base exit_block — no effects, no clock. It is a door, not an act (the-surfaces.md R7)
[[canvases.nodes.exit_block.choices]]
text       = "Ask him about the car."
targetType = "node"
nodeId     = "talk"
```

⚠️ **And when a HIGHER-priority canvas for the same character owns that room, the branch retires
with the hub unless something links to it.** `act_garage_late` (p7) replaces `hub_theo_garage` (p6)
the moment its arc flag sets, so the pool folded into the hub goes dark exactly when the player has
most reason to want it. A **qualified** nodeId reaches across canvases —
`nodeId = "hub_theo_garage.talk"` — resolved globally at import (`template_import.py:8166-8172`,
validated at `:4678-4698`). One line on the escalation's base, and the two surfaces share the pool
instead of duplicating forty lines of dialogue.

⚠️ **Check which phase file the surface lives in before you decide it is safe.**
`merge_toml_phases.py` drops `6_dev_shortcuts.toml` **by name** on `--no-dev` (`:62`), which is the
release setting (`:80`). Anything authored there is gone from the released game.

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

**Where the player cannot yet know the name**, set `speaker = "unknown"` on the `dialog` block and
the engine prints **"Stranger:"** (`v2.py:17586-17593`); switch to the NPC speaker once names have
been exchanged.

⚠️ **A meeting with no `dialog` block is not a meeting.** The person is in the room. If they do not
say anything, the player has been handed a description, not an introduction. This is `register.md`
S3 applied at the one moment it matters most.

---

## F7 · Role before name

The field's ordering, in the clearest case:

> *"Your new employer stands and leans forward to shake your hand."* — the-company

**Relationship label first, then the name.** The label is what the player can hold; the name is
what they will need later.

**The strongest form of this rule is mechanical, and it is worth stealing.** degrees-of-lewdity
swaps the description for the name once the meeting flag is set, so the game literally cannot use a
name the player has not earned:

```
deliver a letter to <<if $wren_intro is undefined>>a <gender> named Wren.  <He> can be found at
  Remy's estate in the moor, or at the docks at night<<else>>Wren<</if>>.
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

**And a check for it was tried and rejected**, which is worth recording so it is not re-attempted
blind: a kinship-word detector fires on every cast that is not family, where the word was never
going to be there, and on mid-arc canvases that are not introductions. Most of its hits are wrong.
**Read the first line of every meeting yourself.** It is five lines of reading per game.

---

## F8 · The flag belongs to a scene that meets them

The dodge this rule exists to kill: gate the whole cast on one flag set by a scene that meets
**none** of them (`doors_open`), and every hub is technically "behind a meeting" while the cast
still arrives cold.

**A meeting flag counts for a character only if the one-time scene that sets it names them** —
binds them, or gives them a line. A group scene that meets three people and sets one flag meets all
three. A flag set by a scene that names nobody meets nobody. A character named in the **forced**
opening — bound to the starting canvas or a capstone it reaches, or speaking on its first screen —
is met by playing the game, and their hub needs no gate.

*(LO decided, 2026-09-28.)* Three of the four passing games meet every character before their hub
is reachable: Shady Deals (a trio met in one scene, on one flag), Cupid's Way (the office tour) and
In Her Own Hands. Course of Temptation does it differently: its generic "Talk to" works on
strangers. So this rule is a choice backed by field evidence, not a universal law.

⚠️ **Sequence the cast in waves.** Not everyone is reachable on day one. Stage the entrances so each
arrival is a punctuation mark. For a character who arrives mid-game, **withhold their schedule until
the meeting fires** — `getNpcsWithSchedules` (`v2.py:4395`) surfaces every declared NPC on the
Schedule page from day one regardless of any gate, so a schedule given early spoils the entrance.

### The same flag belongs on that character's quest cards

F5 through F8 gate the **canvases**. They say nothing about the **guidance surface**: a Quests page
that lists every character on click one — names, the room each stands in, the hour they are there —
spoils every meeting in the game. The field keeps the name back until the meeting: In Her Own
Hands' [Progress_Hints_Base], behind `<<if not $xr.ab.m>>`, gives only *"I should check out some of
the local shops . . ."*

**A character's `[[quest_cards]]` carry that character's meeting flag in `when`.**

```toml
when = [ { flag = "met_wade", subject = "player", op = "is_true" },
         { trait = "want", subject = "npc", npc_id = "npc_wade", op = "lt", value = 40 } ]
```

The engine already does the rest. `QuestsPage` wraps each character's section in `<<if _card>>`
(`v2.py:18245`) and `setup.pickQuestsCard` returns `null` when no card's `when` matches
(`v2.py:17870`), so an unmet character renders **no heading and no section** — the roster fills in
as the player meets people, which is what the field ships (the-company's cast table is
`<<if $player.met[_char.id]>>` per row).

Three things to get right:

- **A `when` item sets `flag` *or* `trait`, never both** — the importer rejects an item carrying
  both (`template_import.py:5765`). The meeting flag is its own item beside the trait band.
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

**The field names the function on the room screen itself.** Shady Deals' [Pawnshop] renders, on
every visit, *"Pawnshop might buy various electronics and jewelry."* — what the place is, and what
the player does there, in one line.

⚠️ **This is `register.md`'s "words the player has to already own", one level up.** There the unit
was a word; here it is a whole place. A location whose *function* is only implied is an unglossed
noun the size of a room.

### The field's device is the room screen, and it changes

Measured across the 26-game corpus:

```
                                    field median
room prose the player sees per visit   82 words
variant branches per room screen           10
rooms that rotate their text              22%
rooms that vary by hour                   17%
an event renders ON the room screen       yes
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
is aimed at is permanent. LO ruled on exactly that ground:

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

**Lint `the role stays attached`** (gates.py:5519) takes each character's anchor words from his own
`npcs[].relationship` line and counts how often his own canvases use them, per 10k words. It prints a
list, thinnest first, with no bar. It counts every canvas bound to him, so a re-entered surface and a
one-shot count the same. Reading which is which is yours.

**Where it goes: the surfaces the player RE-ENTERS.** A hub, an ambient, a walk-in. Not the one-shot
that introduced him — that one is already doing its job.

**Both, never one instead of the other.**

> *"Relation and name both are important and both can't be replaced with another. We are not calling
> out for replacing one with another."*

⚠️ **Do not swap the name out for the relation on the speaker line.** `destroyer` does
(`<<speech "teagan" "Stepsister">>`) and it is the only game in the 26-game corpus that does — it
survives it by having **exactly one of each relation**. Relation words on buttons run at **field
median 0.4%, max 2.0%**. `sluttown-usa` is a family premise with 37,408 speaker labels and uses **names only**. Swapping does not remove the memory tax,
it moves it: the player now has to remember who "Stepsister" is.

The cheap form is three words riding in prose that was going to be there anyway: name and relation on
the same line, at the point of use, and the register does not move.

**Put it in a `block_pool` variant rather than in the always-renders text.** A hub pool cycles, so
the anchor recurs periodically instead of arriving every single visit, which is how a reminder turns
into nagging.

### The mechanical half — `npcs[].role`

Prose anchors recur every few visits. The **dialogue box** carries it every time somebody speaks:

```
[face]  Wes
        stepbrother               <- npcs[].role
        "<his line>"
```

```toml
[[npcs]]
id           = "npc_wes"
name         = "Wes"
relationship = "Your stepbrother, 26. He works nights at the depot…"   # the cast page's sentence
role         = "stepbrother"                                          # the label under the name
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

> ### ⚠️ The label answers WHO THIS PERSON IS. A place or a timeslot is not an answer.
>
> The "no kin word" row above is the one that misleads, and it misled the author of this
> paragraph. `housemate, top floor` works because **housemate** is the who and *top floor* only
> separates him from the other one. `the canteen` and `the night shift` work only where the game
> has already made that shift into somebody's whole identity — as a general pattern they are a
> trap.
>
> The field names the person: Course of Temptation's [Prologue10] has *"your roommate is somebody
> named"*, and Shady Deals' [Car Mechanic] has *"I'm Brody, your car mechanic, nice to meet you."*
> A label that names the hour he lectures at is not an answer to anything.
>
> **The test:** read the label alone, with no name and no scene, and ask *"is this a person?"*
> `mother` · `professor` · `stepfather` · `runs the corner bar` · `housemate, top floor` pass.
> `the nine-thirty` · `pays the rent` · `the back room` do not — they name a time, a fact and
> a place. The label is the answer to *"who is this"*, which is the standing question this whole
> rule exists to keep answered.

⚠️ **Author it.** An empty `role` renders no line at all (`v2.py:17637-17644`), which is the safe
default.

⚠️ **`role` is not a swap for the name.** `destroyer` replaces the name with the relation
(`<<speech "teagan" "Stepsister">>`) and is the only game of 26 that does — it survives on having
exactly one of each relation. Swapping does not remove the memory tax, it moves it: the player now
has to remember who "Stepsister" is.

> ### ⚠️ For a renameable character the label is the PLAYER'S, and `role` takes an @-token
>
> `[[npcs]] customizable = true` with `relationship_options` renders a listbox: the player decides
> whether this man is her stepfather, her father or her uncle. **Write `role = "@<npc>.rel"`.** It
> resolves to `<<print $npcs["…"].relationship>>` (`engine.md` §43), so the box prints the option
> they picked and follows it if they change it.
>
> A hard-coded label contradicts the player's pick or has to dodge it. The label exists to say what
> he is to her, and that is the one thing the picker already knows. The generator resolves tokens
> in this field (escape first, then resolve, `v2.py:17641`; `.rel` at `v2.py:17038-17039`), and the
> lint `the label under the name` flags a hard-coded label on any character the player can rename.
>
> A **fixed** character still takes a plain string — `mother`, `professor` — and a
> `relationship` written as a sentence (*"Your mother."*) must not be tokenised into the label,
> because the label carries a colon in CSS and a full stop lands in front of it. Both, at the point of use.

---

## What the scoreboard checks

Two gates and three lints. `python3 scripts/gates.py <slug>`.

| | |
|---|---|
| gate · **the opening hands over into an open door** | F3. Walks the funnel's clock and asks whether anything at the landing location is open at that minute. **n/a** when the landing location cannot be resolved. |
| gate · **every hub is met first** | F5 + F8. Per character: **one** hub gated on a flag a non-repeatable canvas naming them sets, and **no** hub left with zero conditions — or a line in the forced opening. A group scene naming several people meets them all. |
| lint · **the place says what it is** | F9. Lists every location by how much prose happens there, against how long its own description is. **Whether a description names the function is a reading, not a measurement**, so this is a list to read and never a score. It replaced a gate that required a first-visit canvas at the anchor — a device eighteen of twenty-six top games do not use. |
| lint · **named before met** | F7. Lists every character named in the opening, a quest card or a room description who has no meeting anywhere in the game. A list to read, never a score. |
| lint · **the opening arms a card with goals** | F1b step 5. The quest cards visible once the starting canvas's handover flags are set, and whether any of them carries `goals`. A list, never a score (added 2026-09-24). |

⚠️ **Nothing checks that the guidance surface waits for the meeting.** The `named before met` lint
does read `[[quest_cards]]` — every string field on every card, beside the opening and the room
descriptions (`gates.py:5424-5426`) — but it skips any character who has a meeting anywhere
(`gates.py:5453`). So a game can pass every gate above with its Quests page still naming the whole
cast on turn one. Read the page yourself at turn one. A gate here needs a second game before its shape is honest.

**The bar is the field's, not an invented number.** Shady Deals' [Car Mechanic] opens on
`<<if $met_mechanic == 0>>`, so the first visit is the meeting (F5), and 14 field games keep a named
first-contact flag per character (F5, "Re-measured 2026-09-02").

> ⚠️ **The gate asks for a meeting on ONE hub, not every hub** — later rungs are gated downstream of
> the meeting, and that is correct work. It bans the **cold spawn** (a hub with no conditions at
> all) on every hub.

---

## Cheat sheet

- **The game does not use a name until it has earned it.** People, places, things.
- **Pick one opening shape, and staged is the default** — staged open puts each person on screen
  and lets them speak; cold open names nobody and is only for an opening with no person in it. The
  middle is the defect. (The word ranges this line used to carry were deleted 2026-08-24 — F1.)
- **The staged open runs setup → problem → person → conflict → choice → temptation → objective →
  play** (F1b): first screen says who she is, the problem, the want; a choice inside the first
  person's scene with a reaction line; something tempting early; a quest card with goal steps;
  plain tutorial lines on the last screen; a hook, not a quiet last line.
- **Boot and capstone are two canvases.** The boot starts the chain; the capstone spends the prose.
- **Hand over into an open door.** A random ambient is not a door. A `substitution_only` walk-in is
  not a door.
- **Every live system gets one beat or one sidebar row.** A system never taught is a system wasted.
- **Every `npc=` hub sits behind a non-repeatable meeting** that names that character —
  the flag on the first hub, and **no** hub anywhere left with zero conditions.
- **Gate the meeting on a schedule or a flag — `requires_npc` does not gate auto-fire**
  (`v2.py:5919`).
- **A meeting is ~100–170 words and somebody speaks.**
- **Role before name.** Swap description for name on the meeting flag where the reference matters.
- **The flag belongs to a scene that meets them.** `doors_open`, set by a scene that names nobody, is the cold-spawn hub in a coat.
- **A place says what it is in its own `description`**, which the player reads on every visit — the
  function first, then the flavour. A first-visit canvas is a minority device: take one only for
  something true once.
