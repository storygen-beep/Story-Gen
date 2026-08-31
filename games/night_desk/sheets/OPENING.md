# [REVIEW] The opening — night one

## In short

- **Twelve screens** from the age gate to the first quiet hour, **~830 words** on screen. The
  previous draft was three beats and 175 words, and it never said how many screens that was.
- **Four one-shot canvases in a flag chain** — boot → capstone → Del → the first check-in.
- **The first two screens are the engine's, not ours.** The age gate and the Customize screen both
  carry hard-coded text we do not write, and one of those strings is bad. See below.
- **Her name moved off a prose beat and onto the engine's own character screen**, which is where
  the engine already puts it. That removes a beat and adds a screen.
- **The funnel now ends by doing rather than by telling** — a guided first check-in, with a real
  choice in it that refuses nothing.
- **The quiet stretch moved.** It used to fall in the middle of the opening; it now falls after the
  funnel closes, which is where quiet is allowed to be.
- **Both open calls are now closed** — the check-in stays, and the explicit floor was fixed in
  the scenes rather than here. What is left at the bottom is one note, not a question.

---

## Review view 1 — the screen walk

**The view that cannot be faked.** A screen either exists or it does not. The timeline says what it
is like to sit through and the checklist says what nobody was told; only this one says what the
player's hands actually do.

<pre>
  #  canvas · node                 what is on the screen                    the button
 ────────────────────────────────────────────────────────────────────────────────────────────────
  0  Start            <b>engine</b>      title card · age gate                    ✓ I am 18 or older - Enter Game
  1  CustomizeCharacters <b>engine</b>   "Your Character" · one text field        Continue to Game
 ────────────────────────────────────────────────────────────────────────────────────────────────
  2  boot · the_deal              who she is · three weeks · the $80       Count what you have.
  3  boot · the_bus               the bus, Tuesdays and Fridays · $400/60  Go down to the desk.
     ── location exit ──►  <a href="places/the_desk.md">the_desk</a>, 21:55 · sets flag <b>booted</b>
 ────────────────────────────────────────────────────────────────────────────────────────────────
  4  capstone · the_game          <b>Night Desk</b> — earn / climb / body       Clock on.
  5  capstone · first_minutes     the room, the tubes, twelve hooks        Start the shift.
     ── location exit ──►  <a href="places/the_desk.md">the_desk</a>, 22:00 · sets flag <b>shift_started</b>
 ────────────────────────────────────────────────────────────────────────────────────────────────
  6  del_handover · he_comes_out  the man who owns the place               Wait for the rest of it.
  7  del_handover · the_keys      twelve keys · the ice machine · monitor  Ask what else.
  8  del_handover · the_books     two to four, and the drawer balances     Get on with it.
     ── location exit ──►  <a href="places/the_desk.md">the_desk</a>, 22:10 · sets flag <b>met_del</b> · +10m
 ────────────────────────────────────────────────────────────────────────────────────────────────
  9  first_checkin · headlights   a station wagon, badly parked            <b>2 choices</b> — room 4 or room 9
 10  first_checkin · the_key      $38, the plate on the card, the look     Hand him the key.
 11  first_checkin · the_first_six  five rooms · thirty at midnight        Back to the desk.
     ── location exit ──►  <a href="places/the_desk.md">the_desk</a>, 23:00 · sets flag <b>first_checkin_done</b> · room 9 occupied
 ────────────────────────────────────────────────────────────────────────────────────────────────
     <b>THE FUNNEL ENDS.</b> Five things live on the desk, the audit at 02:00, Marek at 00:20 if she walks.
</pre>

**Twelve screens. Two of them are not ours.** Ten authored, ~830 words on screen, one choice.

---

## ⚠️ The two screens the engine writes, and one of them is bad

This is the finding the screen walk exists to produce, and no other view could have.

**Screen 0 — the age gate.** `Start` initialises state and renders a title screen; the starting
canvas is only reached through `[[✓ I am 18 or older - Enter Game->StartingCanvas_…]]`
(`engine.md` §12). Free, correct, nothing to do.

**Screen 1 — Customize Characters.** Declaring `[player] customizable = true` plus one
`[[player.customization_fields]]` builds a `CustomizeCharacters` passage, **and the age gate then
links there instead of the starting canvas** (`v2.py:1065`, `v2.py:9251`). Its text is hard-coded:

<pre>
  &lt;h2&gt;Customize Characters&lt;/h2&gt;
  &lt;p class="customize-intro"&gt;Personalize the characters in your story.&lt;/p&gt;
  &lt;h3 class="customize-section-title"&gt;Your Character&lt;/h3&gt;
  [[Continue to Game-&gt;StartingCanvas_…]]
</pre>

⚠️ **"Personalize the characters in your story" is the second thing a player of this game reads.**
It is a template string in a product voice, sitting one click in front of a motel on a state
highway at ten at night. **Seven of our fifteen built games ship that screen** and no sheet has ever
shown it, because no sheet has ever had a row for a screen we did not author.

The one thing we *can* write on it is `player_description`, which renders above the fields
(`v2.py:9509`). Proposed:

> Nineteen, three weeks at the Wayside, and tonight you are on the desk by yourself.

**One field only** — `id = "name"`, type `text`, which the generator maps to `$player.name`
(`v2.py:9522`). No build, no hair, no body type. She is authored, not assembled, and that was
Block A decision 2.

---

## Screen by screen

### 2 · boot · `the_deal`

> You are nineteen and you have been at the Wayside three weeks. You came with what fitted in a car,
> and two weeks ago you sold the car. Twelve rooms on a state highway, forty minutes from anywhere
> in either direction. Del owns it, sleeps in the back office, and takes eighty dollars a week out
> of your pay for room twelve.
>
> Tonight is the first night they have left you on the desk alone.

*Button:* **Count what you have.**

⚠️ **"First night alone" is structural.** Three weeks in the building is why corruption at zero is
honest and why she knows where things are. Tonight being her first shift by herself is what makes a
handover scene natural rather than remedial.

### 3 · boot · `the_bus`

> There is a bus that stops at the crossroads on Tuesdays and Fridays at ten past six in the
> morning, twenty minutes after your shift ends. A seat on it as far as the coast is four hundred
> dollars.
>
> You have sixty, folded flat in the lining of your bag, and you count it more often than you need
> to.

*Button:* **Go down to the desk.** → <a href="places/the_desk.md">the_desk</a>, 21:55, sets `booted`

**The want, stated in the boot and never mentioned again by the game.** The gap between 60 and 400
is the whole objective and it is now visible on the second authored screen.

### 4 · capstone · `the_game`

> ### Night Desk
>
> **What you earn.** Six dollars for every room with someone in it at midnight. Twelve rooms, so a
> full night is seventy-two, and a full night has not happened since June. Eighty a week goes back
> to Del for your own.
>
> **What you climb.** *Exhibitionism* — what you will let be seen. *Corruption* — what you will do.
> Neither of them starts anywhere. The second one is what opens the first.
>
> **What your body needs.** You get tired, you get hungry, and you get dirty. There is one bathroom
> for rooms one to six and the staff, in the back hall behind the desk, and it does not lock from
> the inside.

*Button:* **Clock on.**

⚠️ **Denser than the game's normal beat, deliberately.** This screen is seen once, which is the
argument that already lets a one-time capstone spend prose. A list beats a paragraph here and
nowhere else in the game.

⚠️ **The last line is load-bearing.** The shared bathroom is stated as a condition of the job before
she ever walks into it, so the first time somebody is already in there it reads as a consequence
rather than a coincidence. It is also <a href="people/marek.md">Marek</a>'s whole on-ramp.

### 5 · capstone · `first_minutes`

> The office door is shut and there is light under it. Out past the glass the lot holds four cars
> and the road holds nothing at all, and it will hold nothing at all for most of the next eight
> hours.
>
> Two fluorescent tubes over the register. One of them ticks. Twelve keys on twelve hooks, four of
> them missing, which means four rooms are honest tonight. The monitor cycles four cameras at eight
> seconds each — corridor, lot, ice machine, the back hall — and comes round to the corridor again.
>
> Twenty-two hundred. You have eight hours.

*Button:* **Start the shift.** → <a href="places/the_desk.md">the_desk</a>, 22:00, sets `shift_started`

**This is the capstone doing what a capstone is for.** The mechanics screen breaks frame; this one
closes it again and hands her the room in the game's own voice. It also names the four cameras,
which is the setup for **Watch the monitor** being the corruption on-ramp.

### 6–8 · `del_handover`

Three screens. He is **"the man who owns the place"** for all three and `del` afterwards.

> The office door opens and the man who owns the place comes out with his shirt untucked and a mug
> he does not offer to share. He is fifty-eight and he has the walk of a man who has already decided
> how the night goes.
>
> "You're on your own tonight."
>
> It is not a question, so you do not answer it.

*Button:* **Wait for the rest of it.**

> He puts twelve keys on the counter and pushes them across in a heap rather than hanging them.
> "Ice machine's out. It's been out. Don't call anybody about it, and if they ask, tell them it's
> out."
>
> He taps the monitor with one knuckle, twice, and the picture does not change.
>
> "That stays on. I don't care if it bothers you."

*Button:* **Ask what else.**

> "Books get done between two and four. Drawer balances before I'm up, and I'm up at six." He looks
> at you for slightly too long, the way you look at a thing you are not sure you should have bought.
> "You've been here three weeks. You know where everything is."
>
> Then he goes back into the office and shuts the door, and the light under it goes off about a
> minute later.

*Button:* **Get on with it.** → <a href="places/the_desk.md">the_desk</a>, 22:10, sets `met_del`

⚠️ **This canvas must fire on night one regardless of Del's usual odds.** He is at the desk about
one night in three ordinarily; an introduction gated on that would miss two players in three.
It carries its own window and is exempt from the schedule that governs him afterwards.

⚠️ **It also arms three systems by saying them out loud** — the monitor stays on, the ice machine is
dead, and the audit runs between two and four. All three were previously going to appear as buttons
she had never heard of.

### 9–11 · `first_checkin`

Fires at the desk at 22:40, gated on `met_del`. **The one place in the funnel where she does the job
instead of being told about it.**

> Headlights come off the road at twenty to eleven and swing across the glass, and a station wagon
> stops badly across two spaces. A man gets out and stands looking at the sign for longer than the
> sign is worth, then comes in with his wallet already open.
>
> "You got a room?"

*Choices — both work, neither refuses:*
- **Give him four. It's furthest from the road.**
- **Give him nine. It's closest to the light.**

> Thirty-eight dollars, cash, and he counts it twice because he does not trust himself. You write
> the plate on the card the way Del showed you three weeks ago, and you hang the tag on the hook and
> take the key off it.
>
> He is looking at you, and it is not rude, and it is not nothing either. It is the look of a man
> working out whether the girl behind the counter is part of what he is paying for.

*Button:* **Hand him the key.**

> He says thanks in a way that is mostly a nod, and goes back out, and the station wagon takes two
> tries to get into the space it is already in.
>
> Five rooms with someone in them now. At midnight that is thirty dollars, and thirty dollars is a
> night. Four hundred is thirteen more of these.
>
> The tube over the register ticks. The road does nothing.

*Button:* **Back to the desk.** → <a href="places/the_desk.md">the_desk</a>, 23:00, sets
`first_checkin_done`, room occupied

⚠️ **The last screen converts the whole economy into one number the player can hold** — thirteen
more nights like this one. That is the objective and the grind stated together, without a tutorial
voice.

⚠️ **The look on screen 10 is the game's first exhibitionism beat and nothing happens in it.**
Exhibitionism is 0, so the automatic variant keeps the counter between them. It is there to make the
axis legible before it is ever climbed.

---

## The four flags that hold the order

<pre>
  Start ─► CustomizeCharacters ─► boot ─────────► capstone ────────► del_handover ──► first_checkin
                                   sets booted     needs booted        needs           needs met_del
                                                   sets shift_started  shift_started   sets
                                                                       sets met_del    first_checkin_done
</pre>

**No schedule holds this order — flags do.** Every one of the four auto-fires through
`selectAutoFireCanvasForLocation`, which takes the highest-priority valid **non-repeatable** canvas
and skips every repeatable one (`v2.py:4453-4471`). The flag gate is the whole ordering mechanism.

⚠️ **All four sit at <a href="places/the_desk.md">the_desk</a>**, which means the desk's own screen
does not render until `first_checkin_done` is set. That is correct and it is worth stating: an
auto-fire canvas *replaces* the location screen, it is not something on it
(`getStoryCanvasRedirect`, `v2.py:5091`).

---

## Review view 2 — the timeline

<pre>
NIGHT 1

  —     screen 0   age gate                          <b>engine</b>      no choice
  —     screen 1   Customize · her name              <b>engine</b>      1 field
21:50   screen 2   who she is · three weeks · $80                 no choice
21:52   screen 3   the bus · $400, she has 60                     no choice
21:55   ── the desk ──  capstone fires
21:55   screen 4   <b>Night Desk</b> — five systems named             no choice
21:58   screen 5   the room, the tubes, the four cameras          no choice
22:00   ── the desk ──  Del fires
22:00   screens 6–8  keys · ice machine · the books at two     <b>← MEET DEL</b>
22:10   ── the desk ──  ten minutes live, then the car
22:40   screens 9–11 the first check-in · $38 · the look      <b>← THE FIRST MONEY</b>
23:00   <b>── THE FUNNEL ENDS ──</b>  five things live on the desk
23:00   ⚠ nothing arrives until 00:20 — about 80 minutes
00:20   <a href="people/marek.md">Marek</a> comes down for ice                   <b>← MEET MAREK</b>, if she walks
02:00   the audit opens
06:00   clock out · corruption 0→2 if she watched the monitor
</pre>

**The quiet stretch is still there and it is longer, but it moved.** It used to sit *inside* the
opening, between the handover and Marek. It now sits *after* the funnel closes. Dead air is fatal in
a funnel and legitimate in an open game — the first quiet hour is the game teaching her what quiet
feels like, and the monitor, the property walk and the kitchen are all live through it.

⚠️ **Still your call.** If you want something arriving, the cheapest is a second car around 23:30
that does not check in — it turns round in the lot and leaves.

---

## Review view 3 — what the opening owes

<pre>
what the opening owes                        when it lands
──────────────────────────────────────────────────────────
she is named                                 screen 1   (engine's chargen)
the hours are stated out loud                21:50
what she is saving for                       21:52      $400, and she has 60
money named and explained                    21:55
exhibitionism named and explained            21:55
corruption named and explained               21:55
the two are linked — one opens the other     21:55
energy · hunger · hygiene named              21:55
the shared bathroom is stated                21:55
the monitor is armed                         22:00      Del: "that stays on"
the audit is explained before 02:00          22:00      Del: two to four
Del met, in his own scene                    22:00
Marek met, where he actually is              00:20      only if she walks
the job is done once, not just described     22:40      the guided check-in
the money is felt, not stated                23:00      thirty at midnight, thirteen more nights
nothing is refused during it                 ✔ no locked door and no failed check before 06:00
the $80 is armed, not charged                ✔ first deduction is Friday
ends on a door that is open                  23:00 → the desk, five things live
──────────────────────────────────────────────────────────
</pre>

**No empty rows.** Two of these are new this draft — *the job is done once* and *the money is felt* —
and both came out of writing the screen walk, because the walk made it obvious the player reached
23:00 having pressed nothing but Continue.

---

## What this sheet turned up

1. **The old sheet described the second screen and called it the first.** The age gate is screen 0
   and it always was.
2. **The engine has a character screen and we had never mentioned it.** Seven of fifteen built games
   ship one. Ours will now, with one field and a written description, because the alternative is
   the player's second screen reading *"Personalize the characters in your story."*
3. **The name was a prose beat and did not need to be.** It is a form field, and the engine has a
   form.
4. **The boot and the capstone were collapsed into one canvas** — the exact defect
   `the-first-hour.md` F2 names as the reason v2 openings run more than double v1's and still feel
   thin. They are two canvases now.
5. **The funnel had no verbs in it.** Eleven screens of narration and one name box. It now contains
   the job, done once, with a choice that colours and refuses nothing.

**Measured against every opening we have ever built:**

<pre>
  seventh_day      5 screens  420 w        commuter         1    93
  the_allowance    5          535          last_call        1    60
  back_home        4          468          late_shifts      1    45
  forty_miles      3          339          mothers_place    1   101
  steam            3          285          mrs_vance        1   100
  off_season       2          160          the_inheritance  1    31
  vesper           2           89          the_route        1   136
                                           the_season       1   119
  ──────────────────────────────────────────────────────────────────
  <b>night_desk      10 authored screens · ~830 w</b>   (12 including the engine's two)
</pre>

**Twice the screens of our largest opening and 1.6× its words; 2.1× our v2 median of 402.** The largest true opening in the field
corpus is Course of Temptation's at **78 passages and 8,057 words** (`the-first-hour.md` F4b), so we
remain an order of magnitude under the top of the genre. That is a decision, not an accident, and it
is the second thing I want your call on.

---

## What I want your read on

**1 · ~~The guided check-in~~ — KEPT. LO's call, 2026-08-31.**

Screens 9–11 stay as written, all three. It is the one piece of this funnel that doctrine never
asked for — F1–F10 specify a boot, a capstone, a meeting per character and a handover, and this is
none of them. It stays because the field's largest openings are funnels the player *acts* inside and
ours have been narration with a name box.

⚠️ **Recorded so it is not re-argued:** the cut that was on the table was dropping screen 10 and
keeping 9 and 11. Not taken. Screen 10 is the look across the counter, which is the only thing in
the whole funnel that points at what the game is about.

**2 · Is ~830 words enough?** We are half again our best on words, double it on screens, and a tenth of the genre's best. I did not
inflate to close that gap because padding the prose is not what makes Course of Temptation's
prologue work — it has a cast, a house and a set of obligations by the time it ends. Ours has one
man and a job. **If you want the funnel bigger, the honest way is a second night in it**, not more
words on these twelve screens.
