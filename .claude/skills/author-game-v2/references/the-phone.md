# The Phone — the second screen, and what it is allowed to know

Every app, thread, feed, post, profile and notification. What goes on the phone, what stays off
it, how a message is written, and how the phone is wired to the rest of the game.

This file owns **one rule**, and every section below is that rule applied:

> **The phone is a door into the world, not a room of its own. It reads state the world already
> keeps, and everything it offers costs the world something.**

> The failure this exists to prevent: **live arcs with no phone.** Every game this skill copies
> carries its arcs on threads — In Her Own Hands' 10 senders are all arc people, Shady Deals calls
> only contacts she met in scenes (round 9a, `ROUND9A_REPORT.md` §2). A game whose people never text
> her between meetings has a world that stops when she leaves the room. (The older failure, a feed
> she cannot post to, is P6.)

**Why this file exists.** `DOCTRINE_GAPS.md` Tier 3 row 12 — *"Optional systems — phone,
customization"*. The phone is a channel — infrastructure, not a system (`the-systems.md` SY1): it
carries other systems' threads. Before this file, a grep of the whole v2 skill for `phone` returned four hits,
all incidental: the gap row itself, one economy example listing "her phone" as a bill, and two
`engine.md` table rows. The engine has shipped eight phone app types since doc 45 and the skill
never said a word about any of them.

Evidence: `~/Documents/Phone_System_Study_20260829/` — 27 shipped sandbox games (22.5M words of
extracted passage text) and 22,622 player comments, of which 622 mention the phone.

Engine claims here carry a `file:line` into
`apps/game_generation/twee_comprehensive/generators/v2.py` and
`apps/projects/services/template_import.py`, per `SKILL.md` operating rules.

## Contents
1. P1 · Every person she is involved with has a thread
2. P2 · Build the channel, never the hub
3. P3 · A message is 3–7 words — the phone is its own register
4. P4 · Every text is caused by a scene and timed — the phone keeps no state of its own
5. P5 · Everything on the phone costs something — and ignoring costs most
6. P6 · If she can be looked at, she has to be able to post
7. P7 · No hidden phone gate; a locked app names what unlocks it
8. P8 · One thing at a time, delivered by pull
9. P9 · After the sex step, the thread becomes the loop invite
10. P10 · Every thread ends in a booking she can see
11. P11 · Never a battery
12. P12 · She can open the same doors herself

---

## P1 · Every person she is involved with has a thread

**The default is a phone, with a chat thread for every person she is involved with** (LO, WS-D7).
Every game this skill copies has one, and its threads carry the arcs: Cupid's Way's Damien thread
opens at a lunch scene and runs to sex at her place (round 9a §1a). The phone is how a person she is
involved with reaches her between the times she can reach him in person.

**A thread follows the person.** List the live arcs first. Each gets a thread when its first scene
sets the flag that causes a text (P4); a person she has not met has none. A phone with no live arc
has nothing to say, so a release with no arc running yet leaves `[phone]` out.

**Every app is a door to sex, money or people, or it isn't there.** In Her Own Hands ships 15 apps,
and 6 pay nothing; Cupid's Way's followers buy nothing; neither drew praise for them (round 9a §0).
Course of Temptation's Findr ends in a booty call; In Her Own Hands' OnlyGirlz pays the bank on the
1st. An app that cannot end in a person, a sex scene or money is cut.

**A thin phone is still worse than none.** An app with a single item in it reads as a broken
feature, and 18% of the field's phone comments are players asking how to make an empty-looking
phone work. Build what the live arcs and one door app use, and nothing else (round 9a §4).

**The card:** `templates/cards/phone.md` — the steps, amounts, chains, first-release minimum and failure
list, from the four games. Declare the phone in `board.infrastructure[]` (`kind = "channel"`), never in
`board.systems[]`; each thread goes on its person's sheet (`templates/sheets/person.md`).

⚠️ **A declared channel must exist in the built game.** If `0_systems_spec.toml` says the phone is
ON, the built `7_final_game.toml` has to carry its block — `[phone]` for the phone — or the spec has
to change. Nothing checks this: no script in `scripts/` compares the spec with the build.

---

## P2 · Build the channel, never the hub

Measured across the 27-game corpus, counting passages that carry each signal, once per passage:

| what is on the phone | games with it |
|---|---|
| messaging | **24 / 27** |
| a social feed | 20 / 27 |
| a contacts list | 18 / 27 |
| camming or streaming | 17 / 27 |
| a porn app | 15 / 27 |
| a gallery | 15 / 27 |
| selfies | 14 / 27 |
| a paid-subscriber app (OnlyFans-shape) | 13 / 27 |
| **a dating app** | **7 / 27** |
| a bank | 7 / 27 |
| **a job board** | **4 / 27** |
| a shop | 2 / 27 |
| **a map or GPS** | **0 / 27** |

**The phone is where she talks to people and where she is looked at.** It is almost never where
she banks, shops, navigates or finds work.

**Build in this order: messaging, then the thing that makes her looked at, then anything else.**

⚠️ **Two of the engine's eight app types are the rarest things in the genre.** `fast_jobs` and
`bank` both exist (`v2.py:2739`, `:2740`) and both are legitimate — `new-life-project` ships a phone
bank *and* a phone GPS (numbers only). But an author who reads the app-type list and
builds down it will build the 4-of-27 thing before the 24-of-27 thing. Read the table, not the list.

⚠️ **Nobody puts a map on a phone.** Zero of 27. Navigation belongs to `the-map.md`.

---

## P3 · A message is 3–7 words — the phone is its own register

**1–3 bubbles of 3–7 words.** Course of Temptation's texts run a median of 4 words for the one he
sends and 3 for her reply; Cupid's Way's run a median of 5, three lines to a thread (round 9a §2;
the CoT figure is a regex count). Course of Temptation's booty call is three bubbles: *"Hey <pet
name>"*, *"Feel like hooking up? I could use it"*, and the address. The phone study's three games
whose markup marks a bubble ran longer, a median of 11–16 words over 369 bubbles (`the-company`,
`patriarch`, `family-ties`; numbers only).

**Long talk goes to a call or a meeting.** In Her Own Hands' texts are one line or an image; the
talking happens in its calls, which run 300–500 words (round 9a §6). No text tells a story; the
meeting it books does. Until the engine has a call type, write the call as the scene the text books.

**It is a WARN, never a block** (planned gate: `a chat is short and timed`). A two-word *"you up"* is
right; the warning is for the twenty-word paragraph.

**The worked example.** Cupid's Way, `[Message from Damien]`: he opens with *"hey $name, what
you up to?"*, and the thread goes on in the same hand:

```toml
[[phone.conversations.blocks]]
type = "message"
sender = "player"
content = "nothing much really, u?"

[[phone.conversations.blocks]]
type = "message"
sender = "npc"
content = "send me something"
```

Three bubbles counting the opener, 6 / 4 / 3 words. Note what it does not do: no capital letters, no full stops, no
paragraph. **A message is typed by a person on a phone, and it looks like it.**

Two more, written to the same rule, for the two registers a thread runs in:

> **her, testing the water** — *"you up"*
>
> **him, three days after she stopped answering** — *"ok. i'll stop asking."*

And a reply menu, which is where the register most often slips. The choices are what **she** types,
so they are her words, not a description of her intent — this is `the-voice.md` R6 arriving on the
phone:

```toml
[[phone.conversations.blocks]]
type = "reply"
round = 1
choices = [
  { text = "come over" },
  { text = "not tonight" },
  { text = "who else is there" },
]
```

⚠️ **A reply choice is not a beat and not a stage direction.** `"Tell him you'll think about it"`
is wrong twice: it is an instruction rather than a message, and nobody types eight words to say no.

---

## P4 · Every text is caused by a scene and timed — the phone keeps no state of its own

**Every text is caused by a flag a scene set.** In Her Own Hands' 46 of 46 texts sit behind trigger
flags; 77 of Cupid's Way's 79 thread entries read an arc stage; Course of Temptation picks the sender
by relationship and switched off its one random "hi" (round 9a §5 class c). A text with no cause is
filler, and players ignore it. Random *timing* is fine; a random sender or topic is not.

**Every text is timed: a delay after the cause, and an hour window.**
- **The delay** is the next day by default, +2 to +3 days between the steps of a slow burn. Cupid's
  Way sets "+1 day" in 150 of its 210 delay setters; its Damien waits 2 (round 9a §1a).
- **The hour window:** In Her Own Hands gates 43 of its 46 texts on the hour; Course of Temptation's
  booty call comes only 18:00–22:00.

Both are conditions on the conversation's trigger, beside the cause:

```toml
[[phone.conversations]]
id     = "dana_the_morning_after"
npc    = "npc_dana"
notify = "📱 Dana"

[phone.conversations.trigger]
conditions = { version = "1.0", items = [
  { type = "flag",            subject = "player", flag_key = "met_dana_at_the_bar", operator = "is_true" },
  { type = "days_since_flag", subject = "player", flag_key = "met_dana_at_the_bar", operator = "gte", value = 1 },
  { type = "time_of_day",     start_time = "10:00", end_time = "21:00" },
] }
```

`version = "1.0"` is not optional: without it the conditions fail open and the text arrives at once.
`time_of_day` is `HH:MM`, 24-hour, end exclusive, and wraps midnight the way NPC schedules do
(`v2.py:4983`, `engine.md` §39); omit `end_time` and the window is one hour.

⚠️ **On a conversation, `time_of_day` is checked once, at delivery.** The trigger is a latch:
`ps.triggered_conversations[conv.id]` is written the first time every condition passes and is never
re-read (`v2.py:2546`). So the window means *"deliver this the first time she is awake between ten
and nine"*, not *"this thread exists only then"*. A thread that must be reachable only inside an hour
band belongs on a canvas the phone links to, where the condition is read fresh every time. (A chat
with `repeat_after_days` reads its trigger again each time it comes back: `engine.md` §51.)

**The phone keeps no state of its own.** How the phone study's 27 games decide what a phone shows:
a meter 22 / 27, an hour window 20 / 27, a per-NPC stage 13 / 27, a past stamp plus a wait 3 / 27, a
stored appointment 1 / 27. Every one but the last is state the map and the hubs already read. Phone
conversations, posts and profiles go through `setup.triggerConditionsSatisfied` (`v2.py:4728`), the
evaluator canvases use, so every condition a canvas can gate on, a thread can:

```
clothing_item  clothing_slot  corruption_level  days_since_flag  flag  item  modifier
npc_at_location  pass  quest  stage  time_of_day  trait  worn_beauty  worn_corruption
worn_exposure  worn_type
```

A phone that keeps private variables nothing else reads is the bolted-on phone, and it goes stale.

---

## P5 · Everything on the phone costs something — and ignoring costs most

**Ignoring a text costs more than saying no.** Course of Temptation's booty call charges −20
friendship and −20 romance for "Ignore it", and only −2 / −3 for "no thanks" (round 9a §1a). A
thread she can leave unread for free is a thread she will leave unread.

**A no-show costs.** The reply books a meeting; missing it costs Course of Temptation −25 romance,
−25 lust and −25 friendship. The booking and its reminder are P10.

**Using the phone costs too.** Five of the phone study's games charge for phone actions — minutes off
the clock, energy, or a late hour that refuses (numbers only). A refusal is **a sentence in her
voice**, not a greyed-out control (`the-voice.md`).

⚠️ **Nothing on our phone costs anything, and nothing charges for silence.** `setup.sendDailyChat`
(`v2.py:2737`) applies trait effects and returns; phone actions spend no time; there is no hook for
"unanswered by day X". Until the engine has them:
- **ignoring:** a one-time canvas on her next visit home, gated on the cause flag, `days_since_flag
  ≥ 2` on it, and a flag every reply choice sets still `is_false`, applies the cost;
- **a no-show:** the same shape, on the booked flag and the meeting's flag;
- **using:** `daily_cap` on a post action, `cooldown = "per_topic"` on a daily topic, and a
  `corruption_min` she has to have become. Never a free infinite button (P11).

---

## P6 · If she can be looked at, she has to be able to post

**This is the field's single most common phone porn mechanic.**

In Her Own Hands' camera (`CameraMain`) runs selfies as a ladder — dressed → underwear → topless —
each rung gated on the room she is in, what she is wearing, and her inhibition, and a rung she is
not ready for refuses in her own voice: *"I can't take a selfie in just my bra and panties!"*

One counted game (`family-ties`, numbers only; it fails the adults-only rule) runs two apps as
**one system at two ceilings**: 3 rungs in the free app, 4 more and then video in a paid app she
has to unlock.

**The free tier stops at topless. The paid tier has to be unlocked and goes further.** The
escalation ladder *is* the app list — which is a cleaner way to publish a ceiling than a number in
a design doc, and it matches `kink-ceilings.md`'s own logic.

The worked shape, in what our engine actually supports (`v2.py:3005` renders it, `v2.py:3060`
sends it):

```toml
[[phone.apps]]
id    = "flaunt"
type  = "social_feed"
label = "Flaunt"
post_actions = [
  { label = "Post a selfie",        followers_min = 3,  followers_max = 8,  counter_trait = "followers", daily_cap = 1 },
  { label = "Post one in a towel",  followers_min = 10, followers_max = 25, counter_trait = "followers", daily_cap = 1, corruption_min = 20 },
  { label = "Post one with nothing on", followers_min = 40, followers_max = 90, counter_trait = "followers", daily_cap = 1, corruption_min = 45 },
]
```

A locked rung renders as `🔒 <label>`; a spent one as `<label> ✓` (`v2.py:3017`, `:3019`).

⚠️ **`followers` must buy something.** A counter with no sink is the `college-daze` complaint
waiting to happen — a number on a screen that stops meaning anything. Give it a door, per
`the-economy.md` R1b: a rung of content, a character who only answers a girl with a following, a
price that drops. If nothing reads it, do not count it.

⚠️ **`post_actions` cannot gate on place or on clothing today.** It reads `corruption_min` and
nothing else (`v2.py:3068`). A place rule ("only at home") is not
expressible, and neither is checking what she is actually wearing — even though `worn_exposure`
exists (`v2.py:4460`) and is exactly the predicate for it. Until then, the rung labels carry the
whole meaning, so write them as acts (`the-voice.md` R6).

**The feed can also look back at her.** `course-of-temptation` generates its feed posts from her
reputation meters rather than authoring one per story beat — students post about her if she is
known as promiscuous, an enemy harasses her there, admirers post a tribute. That is a `posts` block
with a `trait` condition on its trigger, and it is the cheapest way to make a feed feel like a town.

---

## P7 · No hidden phone gate; a locked app names what unlocks it

**No buy, carry or PIN step.** Hidden phone gates are 43 of the 194 player failures round 9a
classed (class b), 32 of them on one game's PIN (`new-life-project`, numbers only). In Her Own
Hands puts the phone in the menu from the first minute, with no step to get it, and draws 0 such
complaints; Cupid's Way also 0 (round 9a §5). Course of Temptation's "the phone needs a pocket"
rule is the one to never copy. So leave `[phone] purchase_flag` (`template_import.py:480`) unset:
it hides the whole phone until a flag is set.

**Showing a locked app is good; showing it without saying what opens it is a support ticket.** The
two loudest phone threads in the phone study's 22,622 comments ask how to unlock one locked app
(50 and 31 net, `family-ties`, numbers only).

⚠️ **Our engine has no per-app condition.** `setup.openPhone` (`v2.py:2788`) renders every declared
app unconditionally. Until per-app gating exists, publish the ladder in the app that is already
open: a rung labelled `🔒` with its `corruption_min` is legible; a second app that silently is not
there is not.

---

## P8 · One thing at a time, delivered by pull

**Deliver by pull: a badge, never a covering pop-up.** In Her Own Hands puts a line in its sidebar;
Cupid's Way marks the contact with ❕ and turns the Study button yellow while a text waits. Shady
Deals' phone covered the screen, drew 5 complaints, and was fixed in three steps: a hide button, a
glow on a call, the hidden state remembered (round 9a §5 class f, 8 failures). Our engine already
pulls: a delivered conversation raises the sidebar badge (`v2.py:3565`) and a three-second toast
(`v2.py:2308`) whose text is the conversation's `notify`.

**The phone answers *what now*, one thing at a time.** Lostness, not grind, is this genre's disease
— 15.5% of player comments against grind's 0.9% (Process Review, Round 1) — and in the phone study
players point each other at the phone to find out what to do next (two comments, 20 and 14 net, in
a game that fails the adults-only rule; numbers only). One game shows only the first eligible phone
event and hides the rest (`destroyer`, numbers only; n = 1, a shape, not a rate).

---

## P9 · After the sex step, the thread becomes the loop invite

**A thread has no last text; it turns into a loop.** After the arc's sex step, the person invites
her again on a cooldown of 1–3 days (round 9a §6):
- Course of Temptation: every 3 days at the soonest, 18:00–22:00, rolled on her moves;
- In Her Own Hands' James: an incoming booty call at 2 in 70 per passage after 20:00, at most once a
  day — and she can call him whenever she wants (P12);
- Shady Deals: callers reset daily, and their own stats move them on to new kinds of call.

The arc names this thread as its loop (`the-arc.md` A1).

**Small talk that leads nowhere is filler.** Course of Temptation's phone menu has 13 links and 3
lead anywhere — hang out, date, booty call; its friendly texts only nudge attitude, at most ±10 once
a day (round 9a §1a). Every message on a thread serves a booking or the loop.

**Until the engine repeats a conversation, chain one-time ones.** A conversation delivers once,
ever: `ps.triggered_conversations[conv.id]` is written and never cleared (`v2.py:2556`). So each
invite is its own `[[phone.conversations]]` entry, caused by a flag the last link set and timed
with `days_since_flag`:

```toml
# invite 2 waits three days after the meeting invite 1 booked
[phone.conversations.trigger]
conditions = { version = "1.0", items = [
  { type = "flag",            subject = "player", flag_key = "dana_invite_1_met", operator = "is_true" },
  { type = "days_since_flag", subject = "player", flag_key = "dana_invite_1_met", operator = "gte", value = 3 },
  { type = "time_of_day",     start_time = "18:00", end_time = "22:00" },
] }
```

A link's cause flag may be set by an earlier conversation's reply, as long as the chain starts from
a scene (planned gate: `every chat is caused by a scene`). Author as many links as the release
needs.

---

## P10 · Every thread ends in a booking she can see

**Every text ends in a choice that books something, with a place and a time.** Course of
Temptation's booty call books a plan; In Her Own Hands' first call books Saturday; a Shady Deals
call books a meeting now. Warm and cold answers move the relationship. The meeting happens in the
world, and the player is reminded where she looks: Course of Temptation points to it from a
Reminders app, the calendar, a map marker and a wake-up line; In Her Own Hands from its hint journal
(round 9a §6). A plan the player cannot see is worse than no plan.

**One game in 27 stores a real appointment.** Twenty-six talk about making plans and keep none —
"meet me at the bar tomorrow" is prose, and the link under it goes there now.

The one that does it, `course-of-temptation`, is worth reading in full because the valuable part is
not the negotiation:

1. She proposes an activity. `react_to_activity_proposal` returns `[accepted, message]` — **the NPC
   can refuse, in their own words**, and the narrator answers *"Hmm. Well, that's a shame."*
2. If they accept: *"Okay, what time?"* Day activities open 11:00–20:00, night 18:00–24:00.
3. The player picks today/tonight or tomorrow.
4. **A second check runs against the chosen day** — they can want the activity and not that day.
5. Short notice reads differently: *"Short notice but... sure, I'm not doing much."*
6. Agreeing is **how she gets their number**.
7. It is pushed onto `$planneddate`. Cap: three a day.

**And then eleven different surfaces write into that same book** — texting them, asking face to
face, the dating app, a bar pickup, being invited after class, a reward inside a D/s scene — while
**six read it**: the morning wake-up, the persistent header, the map screen, the location itself,
and a cleanup that expires dates she did not attend.

**The phone does not own the date. The world owns a calendar and the phone is one door into it.**
That is this file's rule stated as architecture, and it is why that system does not read as bolted on.

**The engine has the primitive.** A chat reply choice carries `effects`,
`flagEffects`, `questEffects` and **`scheduleEffects`** (`v2.py:2716`).
`setup.scheduleEvent({delayDays, action, flag, quest, conversation, step})` (`v2.py:7147`) pushes
onto `game_state.scheduled`; the day tick decrements `daysLeft` and fires at zero
(`v2.py:6762-6763`), where `setup.fireScheduledEvent` (`v2.py:7161`) can set a flag, start a quest,
or deliver a conversation.

```toml
[[phone.conversations.blocks]]
type = "reply"
round = 1
choices = [
  { text = "tomorrow then", scheduleEffects = [
      { delayDays = 1, action = "set_flag", flag = "mara_expects_her_at_the_yard" } ] },
  { text = "i can't" },
]
```

⚠️ **Three things are missing next to `$planneddate`, and the author has to cover all three by
hand.**

- **No time of day** — `delayDays` only. "Tomorrow at six" is not expressible.
- **Nobody can refuse.** `scheduleEvent` always succeeds. If the plan should be refusable, the
  refusal is a second reply branch you write; the engine will not produce one. This is R5b and G46
  arriving on the phone — *the surface that cannot say no is not a relationship.*
- **The player cannot see it.** `game_state.scheduled` is written, ticked and fired, and **rendered
  nowhere**. There is no morning summary, no header line, no calendar. So a `scheduleEffect` that
  nothing else surfaces is a plan the player will not turn up for. **If you schedule something, the
  flag it sets must be read by something the player meets** — a quest card, a hub line, an ambient
  on waking. One of the three, minimum.

⚠️ **`linked_phone` is the other direction** — a canvas node completed by a phone conversation
(`template_import.py:1002`, `v2.py:7898`).

---

## P11 · Never a battery

Seventeen of 27 corpus games mention a phone battery. The players are not divided about it. This is
the cleanest single verdict in the 622 phone comments and the highest ratio in the set: the
battery comment against it scored **24 likes, 0 dislikes** (`sluttown-usa`, numbers only; it fails
the adults-only rule).

**Upkeep is not pressure.** P5's costs are pressure because they trade the phone against something
else she could be doing with that minute. A battery is a second clock that governs only the phone,
and it buys nothing — it reads as a chore, and the field's own players say so.

⚠️ **This is the one place where corpus prevalence and player verdict point in opposite
directions**, and the verdict wins. Prevalence measures what authors built, not what worked. No
battery, no charging, no data plan, no phone bill as a repeating upkeep, and no price to buy it either (P7).

## P12 · She can open the same doors herself

**Every door a thread opens, she can open from her side too.** In Her Own Hands' James calls her
for a booty call, and she can call him for one whenever she wants; Course of Temptation's
[PhoneText] texts a contact for a booty call and offers *"Tonight"* or *"Tomorrow night"*. In at
least 10 of the 17 top games with a phone, a call or a text starts a scene without travelling
(Process Review, Round 1, numbers only). The failure is a phone that only holds Patreon, Discord
and credits links.

**In this engine** the phone's `launcher` app is the door (`setup._renderLauncher`, `v2.py:3475`):
an option plays only when she is already in that canvas's room (`v2.py:3492`), and a canvas that
requires him present needs him there. So a summon is a launcher option pointing at a canvas in
**her** room, with no presence requirement on him — he arrives in the scene. `daily_topics` are
player-sent too, but they only move traits; give one a `conditions` block on a flag the world set,
and `cooldown = "per_topic"` for its own once-a-day cap (`template_import.py:434`) — without it the
cap is per NPC and one topic starves the others.

---

## What is not gated here

Nothing in this file is checked by `gates.py` yet. Two planned gates will read it:

- **planned gate: `every chat is caused by a scene`** (a block): every conversation's trigger holds
  a `flag` set by a canvas, or by a reply in a conversation that is itself caused this way (P4, P9).
  A game with no phone passes.
- **planned gate: `a chat is short and timed`** (a warn, never a block — a block would fail a
  correct two-word message): 3–7 words a bubble, at most 3 bubbles, and every trigger carries a
  delay and an hour window (P3, P4).
