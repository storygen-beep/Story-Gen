# The Phone — the second screen, and what it is allowed to know

Every app, thread, feed, post, profile and notification. What goes on the phone, what stays off
it, how a message is written, and how the phone is wired to the rest of the game.

This file owns **one rule**, and every section below is that rule applied:

> **The phone is a door into the world, not a room of its own. It reads state the world already
> keeps, and everything it offers costs the world something.**

> Measured failure this exists to prevent: **`under_one_roof` ships a social feed with 34 posts on
> it that she cannot post to** — `post_actions` is empty, so the app is a wall she reads. And
> **`mothers_place` declared `phone ON (8_phone.toml)` in `0_systems_spec.toml:7`, and shipped with
> no `8_phone.toml` and no `[phone]` block at all.** Neither was noticed by anything.

**Why this file exists.** `DOCTRINE_GAPS.md` Tier 3 row 12 — *"Optional systems — phone,
customization"*. Before this file, a grep of the whole v2 skill for `phone` returned four hits,
all incidental: the gap row itself, one economy example listing "her phone" as a bill, and two
`engine.md` table rows. The engine has shipped eight phone app types since doc 45 and the skill
never said a word about any of them. Consequence, measured across all thirty games in `games/`:
**`post_actions` has been authored zero times and `scheduleEffects` zero times**, and three of the
five games that have a phone at all give it a single app.

Evidence: `~/Documents/Phone_System_Study_20260829/` — 27 shipped sandbox games (22.5M words of
extracted passage text) and 22,622 player comments, of which 622 mention the phone.

Engine claims here carry a `file:line` into
`apps/game_generation/twee_comprehensive/generators/v2.py` and
`apps/projects/services/template_import.py`, per `SKILL.md` operating rules.

## Contents
1. P1 · Whether this game has a phone at all
2. P2 · Build the channel, never the hub
3. P3 · A message is fifteen words — the phone is its own register
4. P4 · The phone reads the world; it keeps no state of its own
5. P5 · Everything on the phone costs something
6. P6 · If she can be looked at, she has to be able to post
7. P7 · A locked app names what unlocks it
8. P8 · One thing at a time
9. P9 · A repeatable thread is built out of today, and needs a null branch
10. P10 · A plan the player cannot see is worse than no plan
11. P11 · Never a battery

---

## P1 · Whether this game has a phone at all

The phone is not free. It is a second map of the same world, and it goes stale the moment the
world outgrows it.

**The prerequisite is people, not features.** A phone is worth building when there are characters
the player wants to reach *between* the times they can reach them in person. If every character is
always findable at a known place and hour, the phone has nothing to add and will read as a menu.

**Ask three questions before declaring `[phone]`:**

1. **Is there someone she cannot get to right now?** If the cast is four people in one house, no.
2. **Does anything in this world happen while she is elsewhere?** A phone's whole value is that it
   is the channel for offscreen life. A game with no offscreen life has no use for it.
3. **Is she looked at by anyone she is not in the room with?** That is the other half — see P6.

If the answer to all three is no, do not declare a phone. Declaring one and filling it thinly is
strictly worse than not having one: an app with a single item in it reads as a broken feature,
and 18% of the field's phone comments are players asking how to make an empty-looking phone work.

⚠️ **A declared system must exist in the built game.** `mothers_place` wrote *"Systems: clothing
ON, customization ON, phone ON (8_phone.toml)"* into its systems spec and shipped `7_final_game.toml`
with no `[phone]` block. If the spec says a system is on, the built TOML has to carry it or the spec
has to change.

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
`bank` both exist (`v2.py:2464`, `:2465`) and both are legitimate — `new-life-project` ships a phone
bank *and* a phone GPS and is a well-liked game. But an author who reads the app-type list and
builds down it will build the 4-of-27 thing before the 24-of-27 thing. Read the table, not the list.

⚠️ **Nobody puts a map on a phone.** Zero of 27. Navigation belongs to `the-map.md`.

---

## P3 · A message is fifteen words — the phone is its own register

This is the highest-confidence measurement in the study and the one most likely to be got wrong,
because every other surface in this skill says 35–40.

Measured on the three corpus games whose markup marks an individual bubble, in two languages:

| game | bubbles | median | mean | p90 |
|---|---|---|---|---|
| `the-company` | 194 | 16 w | 14 w | 21 w |
| `patriarch` | 163 | 11 w | 13 w | 23 w |
| `family-ties` | 12 | 15 w | 15 w | 21 w |
| **pooled** | **369** | **11–16 w** | **13–15 w** | **~22 w** |

**A text message is under half a beat, and nine in ten are under 22 words.** This is a rate over
word count, so unlike most corpus figures it survives the HTML/TOML change of basis and can be
read against our own TOML directly.

⚠️ **Do not turn this into a floor or a ceiling.** It is the shape of the thing. A three-word
message is correct; `the-company` ships *"Love you Diana!"* Length varies with what is being said,
the way it does in a real thread.

**The worked example.** This is `under_one_roof`, which already writes at the right length — the
only thing about our phones that is not a defect:

```toml
[[phone.conversations.blocks]]
type = "message"
sender = "npc"
content = "hey"

[[phone.conversations.blocks]]
type = "message"
sender = "npc"
content = "sorry about this morning"

[[phone.conversations.blocks]]
type = "message"
sender = "npc"
content = "the lock is broken I keep telling dad"
```

Three bubbles, 2 / 4 / 8 words. Note what it does not do: no capital letters, no full stops, no
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

## P4 · The phone reads the world; it keeps no state of its own

How the corpus decides what a phone shows:

| gate | games |
|---|---|
| a **meter** — relationship, corruption, trust ≥ N | **22 / 27** |
| an **hour window** — only between X and Y o'clock | **20 / 27** |
| a **per-NPC stage number** | 13 / 27 |
| a **past stamp plus a wait** — "last seen day 9, wait two days" | 3 / 27 |
| a **stored future appointment** | **1 / 27** |

**Every one of those except the last is state the map and the hubs already read.** A phone thread
gated on her relationship meter is the same thread the world is gating its own scenes on. A phone
that owns private variables nothing else can see is the bolted-on phone, and it is the one that
goes stale — a player comment on `college-daze`: *"Most of the characters stats on the phone
profile don't actually mean anything anymore."*

**We are well placed here.** Phone conversations, posts and profiles are evaluated by
`setup.triggerConditionsSatisfied` (`v2.py:2204`) — **the same evaluator canvases use**
(`v2.py:3888`). Every condition type a canvas can gate on, a phone thread can gate on:

```
clothing_item  clothing_slot  corruption_level  days_since_flag  flag  item  modifier
npc_at_location  pass  quest  stage  time_of_day  trait  worn_beauty  worn_corruption
worn_exposure  worn_type
```

**`time_of_day` was built for this file** (2026-08-29, `v2.py:4128`, `engine.md` §39). It was the
one gate in the field's list this engine could not express, and it is second only to a meter:

```toml
{ type = "time_of_day", start_time = "22:00", end_time = "06:00" }
```

`HH:MM`, 24-hour, **end exclusive**, and it wraps midnight correctly because it delegates to the
same function NPC schedules use. Omit `end_time` and the window is one hour.

⚠️ **But a conversation's trigger is a latch, not a filter, and `time_of_day` does not change
that.** `ps.triggered_conversations[conv.id]` (`v2.py:2202`) is written the first time the condition
passes and never re-read. A thread is *delivered* once and then stays. So on a **conversation**,
`time_of_day` means **"deliver this the first time she is awake at 2am"** — not **"this thread only
exists at 2am"**, which is what `family-ties` does, re-checking its noon-to-six window every time the
app opens. On a **canvas trigger**, which is evaluated fresh every read, it means the second.

**So put the window where it will be re-read.** A thread that must only be reachable inside an hour
band belongs on a canvas the phone links to, not on the conversation's own trigger. A conversation
trigger is the right place for *when this arrives*, which is what most threads want anyway.

---

## P5 · Everything on the phone costs something

Six corpus games, the same instinct in six forms:

| game | what it charges |
|---|---|
| `family-ties` | `$time.min += 1; $you.arousal += 2` **per scroll** — an infinite feed as an arousal loop |
| `family-ties` | `$time.min += random(2, 3)` to open a message |
| `the-company` | `passTime()` on every text sent |
| `patriarch` | Energy < 1 → *"You're too tired to text anyone"*; late → *"Better not text anyone this late.."* |
| `destroyer` | every phone event needs `$Energy > 19`, most also N days since the last beat |
| `new-life-project` | memes before the evening only → *"It's too late to watch memes. Get some rest!"* |

**Read the register of those refusals.** A locked phone action in this genre is **a sentence in her
voice**, not a greyed-out control. That is `the-voice.md`'s territory and it applies here unchanged.

⚠️ **Nothing on our phone costs anything.** `setup.sendDailyChat` (`v2.py:2375`) applies trait
effects and returns. Grepped the whole phone block (`v2.py:2180–3140`): the only occurrence of
`advanceTime` or `passTime` is a comment at `v2.py:3096`. Our phone is a free action, repeatable
without limit inside a day except where a `daily_cap` happens to exist.

**Until the engine can charge for a phone action, charge in the fiction and in the gates you do
have.** `daily_cap` on a post action, `cooldown = "per_topic"` on a daily topic, and a
`corruption_min` that makes the rung cost something she has to have become. What you may not do is
ship a phone that is a free infinite button — that is the *"use the app, wait, use the app, wait"*
complaint, quoted in P11.

---

## P6 · If she can be looked at, she has to be able to post

**This is the field's single most common phone porn mechanic and we have never once built it.**
`post_actions` appears in zero of the thirty games in `games/`.

`family-ties` runs Instagram and OnlyFans as **one system at two ceilings**:

| | Instagram | OnlyFans |
|---|---|---|
| rungs | plain selfie → underwear → topless | topless → naked → pussy → plug, then video |
| counters | one per rung, kept separately | one per rung, kept separately |
| subscribers | `$you.inst.sub` | `$you.onlyfans.sub` |
| income | monthly, recurring | monthly, recurring |
| daily cap | once | once |
| place gate | she must be at home | she must be at home |
| unlock | there from the start | `$app.onlyfans == 1` — earned |

**The free tier stops at topless. The paid tier has to be unlocked and goes further.** The
escalation ladder *is* the app list — which is a cleaner way to publish a ceiling than a number in
a design doc, and it matches `kink-ceilings.md`'s own logic.

The worked shape, in what our engine actually supports (`v2.py:2716` renders it, `v2.py:2771`
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

A locked rung renders as `🔒 <label>`; a spent one as `<label> ✓` (`v2.py:2728`, `:2730`).

⚠️ **`followers` must buy something.** A counter with no sink is the `college-daze` complaint
waiting to happen — a number on a screen that stops meaning anything. Give it a door, per
`the-economy.md` R1b: a rung of content, a character who only answers a girl with a following, a
price that drops. If nothing reads it, do not count it.

⚠️ **`post_actions` cannot gate on place or on clothing today.** It reads `corruption_min` and
nothing else (`v2.py:2779`). `family-ties`' *"You must be at home to take selfies!"* is not
expressible, and neither is checking what she is actually wearing — even though `worn_exposure`
exists (`v2.py:4111`) and is exactly the predicate for it. Until then, the rung labels carry the
whole meaning, so write them as acts (`the-voice.md` R6).

**The feed can also look back at her.** `course-of-temptation` generates its feed posts from her
reputation meters rather than authoring one per story beat — students post about her if she is
known as promiscuous, an enemy harasses her there, admirers post a tribute. That is a `posts` block
with a `trait` condition on its trigger, and it is the cheapest way to make a feed feel like a town.

---

## P7 · A locked app names what unlocks it

The two loudest phone threads in 22,622 harvested comments are the same question:

> *"How do you unlock the pornhub tab on the phone"* — `family-ties`, **50 net**, and again at **31 net**

And the worst case in the corpus is a phone locked behind a puzzle. `new-life-project` puts a PIN
on its phone and **seven separate high-scoring comments ask for it** — *"How do you get the code
for the old phone?"* (40), *"Old phone pin?"* (38), *"What's the password to the old phone?"* (36),
*"New Phone code?"* (32), *"What's the phones Pin?"* (30), *"Phone code and cheats?"* (27), *"phone
pin code?"* (21). Plus:

> *"I'm stuck in Silvergate, any way to get out? Haven't bought a phone yet"* — 13 net

**Showing a locked app is good. Showing it without saying what opens it is a support ticket.**
`family-ties` renders a locked app as a dead grey tile beside the live ones, which is the right
instinct — the player sees the ladder they are climbing — and then never says how.

⚠️ **Our engine has no per-app condition.** `setup.openPhone` (`v2.py:2425`) renders every declared
app unconditionally. There is one gate and it is whole-phone: `purchase_flag`
(`template_import.py:373`), which hides the sidebar button until a player flag is set — that is the
*acquisition* story, not the ladder. Until per-app gating exists, publish the ladder in the app
that is already open: a rung labelled `🔒` with its `corruption_min` is legible; a second app that
silently is not there is not.

---

## P8 · One thing at a time

`destroyer`'s phone is a single latch and fourteen guarded blocks:

```
<<set _activequest to true>>
<<if _activequest is true>><<if $taxistory is 1>><<if $Energy > 19>>
    <<set _activequest to false>><a data-passage="taxievent1">…</a>
<</if>><</if>><</if>>
… ×14, each clearing the latch when it fires
```

The first eligible event claims the slot and nothing below it renders. **The phone never shows the
player more than one thing to do.**

The mopoga field study named **lostness, not grind, as this genre's disease** — 4.7% of complaints
against 0.9%. The phone is the best place in a sandbox to answer *what now*, and the corpus's
players say so themselves, twice, unprompted:

> *"Check the phone in the game. It tells you who's playing who."* — `college-daze`, 20 net
> *"Check the in-game phone, it will tell you who plays who."* — `college-daze`, 14 net

`patriarch` does the same job in a different register — its `Make plans` screen names the **world**
blocker when the phone cannot help:

> *"Monique is ready for the procedure, but you still need to renovate the East Wing before you can
> move in your new breeder!"*

⚠️ **n = 1 for the latch specifically.** It is offered as a shape, not a rate, and nothing gates
it. What is measured is the disease it treats, not the frequency of this cure.

---

## P9 · A repeatable thread is built out of today, and needs a null branch

`become-someone` gives **8 NPCs their own daily thread** — 115 passages, 10,557 words. The whole
dispatcher:

```
<<if $jade.train is 1 && $jade.class is 1>>  ...pick one of the two at random
<<elseif $jade.train is 1>>  [[Talk about today training with Jade]]
<<elseif $jade.class is 1>>  [[Talk about today's class with Jade]]
<<else>>                     [[Exchange a few messages with Jade]]
```

Two things to copy.

**The topic comes from something they actually shared today.** She can text Jade about the training
only if the training happened. That is a `daily_topics` entry with a `conditions` block on the flag
the training sets — the same flag the world set, per P4.

**There is an explicit null branch.** When nothing happened, the game says so plainly — *"exchange
a few messages"* — instead of inventing a topic. A daily thread with no null branch either repeats
one line forever or lies about a day that had nothing in it.

**Budget, measured: ~1,300 words per NPC** to run a daily thread at production scale. Know that
number before agreeing to build one. Our own best is `under_one_roof` at 28 daily topics across its
cast; `the_inheritance` declares a chat app and zero daily topics, which is the thin end.

```toml
[[phone.daily_topics]]
id             = "mara_about_the_shift"
npc            = "npc_mara"
player_message = "you survived then"
npc_response   = "barely. ankle's still bad"
cooldown       = "per_topic"
conditions     = { version = "1.0", items = [
  { type = "flag", subject = "player", flag_key = "worked_with_mara_today", operator = "is_true" },
] }
```

⚠️ **`cooldown = "per_topic"` gives this topic its own once-a-day cap** (`template_import.py:349`).
Without it the cap is per-NPC and one topic starves the others.

---

## P10 · A plan the player cannot see is worse than no plan

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
That is P1's rule stated as architecture, and it is why that system does not read as bolted on.

**We have the primitive and have never used it.** A chat reply choice carries `effects`,
`flagEffects`, `questEffects` and **`scheduleEffects`** (`v2.py:2355`).
`setup.scheduleEvent({delayDays, action, flag, quest, conversation, step})` (`v2.py:6042`) pushes
onto `game_state.scheduled`; the day tick decrements `daysLeft` and fires at zero
(`v2.py:5687–5698`), where `setup.fireScheduledEvent` (`v2.py:6056`) can set a flag, start a quest,
or deliver a conversation. Usage across all thirty games: **zero**.

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
(`template_import.py:950`, `v2.py:7403`). One game uses it: `under_one_roof`, on five nodes.

---

## P11 · Never a battery

Seventeen of 27 corpus games mention a phone battery. The players are not divided about it. This is
the cleanest single verdict in the 622 phone comments and the highest ratio in the set:

> *"Can you just get rid of the charging the app thing altogether? It adds nothing to the game;
> just a repetitive process that everyone hates."* — `sluttown-usa`, **24 likes, 0 dislikes**

And on the loop it creates:

> *"The grind is unreal. It's just a time waster, use the app, wait, use the app, wait, use the
> app, wait. […] You use the app 10 times on a character and you get a kiss"* — `sluttown-usa`

**Upkeep is not pressure.** P5's costs are pressure because they trade the phone against something
else she could be doing with that minute. A battery is a second clock that governs only the phone,
and it buys nothing — it reads as a chore, and the field's own players say so.

⚠️ **This is the one place where corpus prevalence and player verdict point in opposite
directions**, and the verdict wins. Prevalence measures what authors built, not what worked. No
battery, no charging, no data plan, no phone bill as a repeating upkeep. (A one-off *price* to buy
the phone is a different thing and is fine — `destroyer` sells one for $500 — that is
`the-economy.md` R1b's territory, a thing that stays bought.)

---

## What is not gated here

Nothing in this file is checked by `gates.py` yet. Two candidates exist and both would fail only on
zero, in the G44 / G45 / G46 line:

- **the phone is not a decoration** — a declared phone whose apps hold no content, or a
  `social_feed` with empty `post_actions` in a game that has a corruption meter. `under_one_roof`
  is red on this today.
- **a specced system exists** — a system named ON in `0_systems_spec.toml` with no corresponding
  block in the built TOML. `mothers_place` is red on this today. Not phone-specific; it would catch
  any dropped system.

⚠️ **P3's fifteen words must not become a gate.** It is a shape, measured over 369 bubbles, and a
threshold on it would fail a correct three-word message. The precedent is explicit: R4, study 6's
anchoring check, P0 and the duplicate wardrobe gate were each withdrawn for inventing a number the
evidence did not carry.
