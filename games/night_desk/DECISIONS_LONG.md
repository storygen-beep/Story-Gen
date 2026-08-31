# Night Desk — the fifteen decisions, in plain words

The longer read. Still key points, still simple. **About two minutes.**

Full detail and the evidence behind each one is in [`DECISIONS.md`](DECISIONS.md).

---

## Block A — these five can never be changed

Once the first version is out, players have save files. Change any of these and their saves break
and there is nothing we can do about it.

### 1 · The game says "you", not "she"

*"You slide the register across."*

The player is inside her, not watching her. Most good games in this genre do it this way. It also
matters for the three-way speech thing — "you say" carries an attitude, "she says" only reports one.

### 2 · She is a woman, and we tell you who she is

**She is a written character, not a blank one.** The setup says whatever the game needs it to say.
What the player controls is **how she carries herself** — not who she is.

- **Her name** — the player picks it.
- **Nineteen.**
- **Why she is broke** — she left where she was living in a hurry with what fitted in a car, and then
  sold the car.
- **Why she cannot leave** — no family to fall back on, and no car any more. The bus is the only way
  out, and it costs money she does not have.
- **Three weeks in** — long enough to know the building, new enough that she really is at zero.
- **The game opens on her first shift alone.** Three weeks of days and company; tonight nobody else
  is here.
- **Why she lives in room 12** — she answered an ad. The room was part of the pay, and the eighty a
  week comes back out of it.
- **What she wants** — out. **$400 and a seat on a bus**, always one good week further away.

**Selling the car is the fact everything hangs on.** It is why she is broke, why she cannot leave,
and why $400 is the number. One sentence of setup does all three jobs.

**Why a woman:** the players say so. Out of 22,000 comments, 49 asked for a female lead and 11
objected — and the objectors got shouted down. One put it plainly: with a female lead you get to the
good part faster.

**Why written and not blank.** Most good games in this genre leave the character blank and let the
player fill her in. Two reasons we do not:

1. **We use real performers.** One specific woman's face is on screen. A blank person with a fixed
   face does not work.
2. **The freedom is bought somewhere better.** Meek, bratty or neutral on every line she speaks
   gives the player her personality through playing, instead of through a set-up screen at the
   start. **The player decides how she carries herself, not who she is.**

⚠️ **I pushed the other way earlier today and was wrong to lean on it so hard.** The "80% of players
are on blank-slate games" number is a correlation across thirty games with a lot else going on — it
does not show that blank *causes* it.

**This is settled — your call, 31 August.** The earlier "thin" version is dropped.

### 3 · It is called *Night Desk* ⚠️

Not checked yet. We have hit name clashes on the game sites before. **Somebody has to search for it
before we ship**, because the title is baked into save files too.

### 4 · The internal names

Rooms: [`the_desk`](sheets/places/the_desk.md) · [`the_corridor`](sheets/places/the_corridor.md) · [`the_office`](sheets/places/the_office.md) · [`room_6`](sheets/places/room_6.md) · [`the_lot`](sheets/places/the_lot.md) · [`the_kitchen`](sheets/places/the_kitchen.md) ·
[`the_bathroom`](sheets/places/the_bathroom.md)

People: [`del`](sheets/people/del.md) · [`marek`](sheets/people/marek.md)

Her numbers: `exhibitionism` · `corruption`
His numbers, on each man: `relation` · `corruption`
Her body: `energy` · `hunger` · `hygiene`

Plain nouns. Rename one later and every save standing in that room lands nowhere — and **no check we
have can see it happen.**

### 5 · Every number goes 0 to 100

Nine steps on each, **close together at the bottom and spread out at the top** — 2, 6, 12, 20, 30,
45, 60, 78, 95.

**Why 100.** It is what most real games use — six of the eighteen we measured land exactly there.
It is also the only range our engine likes: it caps every meter at 100 automatically, and its own
notes say meters should keep that cap.

**I had this wrong until today.** It said 0 to 24, because I tried to squeeze "nine steps" into the
ceiling itself. Those are two different things:

- the **scale** is what the number counts up to
- the **steps** are where the locked doors sit on it

You can have nine steps on a 0-to-100 number perfectly well. The biggest game in the genre runs its
exhibitionism up to 500, and **most of its content sits below 40.**

**And the real reason to be generous now:** we will want more steps later. Changing a number's scale
after people have save files **breaks every one of them, and no check we own can see it happen** —
the name stays the same, so nothing complains. The game just quietly means something different than
the save does.

At 100 there is room for thirty more steps without ever touching it.

---

## Block B — these eight are expensive to change

Not fatal. But changing them means rewriting scenes that already exist.

### 6 · Two people, and everyone else is traffic

**Del**, 58 — owns the motel, sleeps in the office, watches the camera monitor all night. She wants
him because he holds her debt and has never once acted like it buys him anything, which is exactly
why she keeps testing whether it does.

**Marek**, thirties — room 6, eleven weeks, pays cash. He has unpacked, and that is the thing about
him. She wants him because he has no power over her at all, which is why he is the only one who says
anything out loud.

**Everyone else** — guests who arrive, argue about the rate, take a key and go. Not named, not
tracked. They are just the world moving.

**The important part:** each man has **a mood that flips**, and every scene that can happen in both
moods gets written twice.

- **Del** — was the motel full this week, or empty? Full and he is generous and easy. Empty and he
  is at the monitor at 4am, short with her, counting.
- **Marek** — does he think he is leaving? Going, he is honest and reckless. Staying, he is careful
  and evasive.

This is the rule the biggest game in the genre gives its writers, and **we have never had it.** It
is the direct fix for our worst habit: our games say the exact same words on the fiftieth visit as
on the first.

**And it produced Friday.** Her pay is counted Friday. Del's mood is set by the week that just
ended. Marek decides on Friday whether he is going. One day a week where all three move together —
that fell out of writing the moods down.

### 7 · Four numbers, and the gap between them is the good part

- **Her exhibitionism** — what she will let be **seen**. No bra, no panties, flashing, getting caught
  on purpose.
- **Her corruption** — what she will **do**, and how she thinks about it.
- **His relation** — whether he is **willing**.
- **His corruption** — what he will **ask for**.

**Here is why that is worth having.** Her corruption is what she will do. His is what he will ask.
A scene needs both — he has to ask, and she has to say yes. So the interesting stuff is in the gap:

- **he is far gone, she is not** → he asks and she says no. A real refusal, written properly.
  Good games put one of those on about one click in fifty, and **79% of them lead somewhere the yes
  does not.** We have never written one.
- **she is ready and he is not** → he is being careful, or protective, or frightened of himself.
- **he barely likes her but will ask for anything** → a completely different man, out of the same
  two numbers.

**The danger.** Each man now has two numbers plus a mood, which is **eight versions of every scene**
if we let everything vary on everything. So the rule is: **every scene picks the one thing it varies
on.** Usually one. Never four.

**How the two numbers on her work together — this is the spine of the game.**

**Corruption unlocks. Exhibitionism spends.**

She cannot flash anyone on night one. Going without a bra is not on the menu until corruption says
she would consider it. Corruption opens the door — it never raises exhibitionism by itself.

Then: **corruption says she would consider it, exhibitionism says she will do it where someone can
see.** The same act at low exhibitionism happens at 4am with the road empty. At high exhibitionism
it happens at 2pm with a queue at the desk. That is where the payoff is.

And doing it feeds back — every exhibitionist act raises corruption, which unlocks the next one. It
is a spiral, which is the right shape for this.

**What raises corruption, and it changes as she climbs.** Nothing ever drops off the list — the list
gets longer.

- **Early, 0–20** — safe things nobody knows about. **Watching the camera monitor**, and sometimes
  there is something on it. A curtain not closed when she walks the property. What is in the sheets
  in the laundry.
- **20–45** — she stays instead of moving on. Showering while someone else is in there. Watching
  instead of walking past. Turning a room with the guest's things still out.
- **45–78** — she is in it. Showering with men and not covering up. Letting a check-in look. Being
  the one on the monitor.
- **78+** — she arranges it. Making sure somebody is watching.

**The monitor is the way in.** Free, safe, on screen the first night, needs no nerve at all. Which is
exactly why it has to be **limited to once or twice a night**, and why every level needs three or
four things to do and not one — otherwise the early game is "watch the monitor twenty times", and
grinding is the second thing players complain about most.

**Her manner** — meek, bratty, neutral — is separate and is not a number. It locks nothing. It
colours everything.

### 8 · The front desk is the centre

It gets more writing than any other room, on purpose. Good games in this genre put about a third of
all their writing in one place and let the rest be thin. Ours spread it evenly, which is how you get
five rooms nobody wants to stand in.

### 9 · Seven rooms, and no way out

The desk is the middle. The corridor, the office, the lot, the kitchen and the bathroom all hang off
it. Room 6 hangs off the corridor.

**The bathroom is shared, and not split by sex.** The Wayside is old — rooms 1 to 6 are the cheap
half and share the bathroom in the back hall behind the desk, and staff use it too. **Marek is in room 6**,
so he and she wash in the same room from the first day.

**Everything hanging off the desk is the point, not tidiness.** Every need drags her away from the
desk, and away from the desk is how she misses an arrival — which is how she loses money. The shape
of the map is what gives the needs teeth.

**The lot is the edge of the world, not a road out of it.** No town, no bus, nowhere else. Our own
rules say the outdoors should be the ground floor of a map, and this deliberately breaks that,
because if she can leave there is no pressure at all.

### 10 · What the game is about: being stuck, then changing

**Stuck** — eight hours, two men, one building, nowhere to walk. Everything that happens, happens
because there is nowhere to go.

**Changing** — she starts as the girl who takes the last bus and ends as the reason both of them
arrange their nights around a shift they do not need to be awake for.

**Not a family story, on purpose.** ⚠️ That is a real cost — taboo is what powers this genre and
nine of our games use it. But players say the tired version out loud: *"It is literally the same
game as all the other games. Young guy step family and school."* So the charge has to come from the
situation instead.

### 11 · Money — she is paid by how full the motel is ⚠️

- **$6 for every room filled**, every night. Twelve rooms, so $0 to $72.
- A normal night is four rooms — **$24**.
- **She owes $80 a week** for her own room, taken out before she sees it.
- A quiet week does not cover it, and **the gap becomes debt to Del.**
- What she is saving for: a bus ticket out. **$400.** Always one good week further away.

**Why this instead of rent:** all nine of our games so far used a rent bill. Here the same pressure
comes out of the premise itself — filling rooms is how she gets paid, so cars pulling into the lot
are both the story and the money. And the man holding her debt is one of the two she is climbing
toward, which is what gives his ladder teeth.

**The risk, and it is the second thing I am unsure about:** nothing sends her a bill. It is a
deduction. Our own checks may fail that. The fix would be showing a weekly line on the desk screen —
not a redesign. Your call whether we do it now or wait to be told.

---

### 12 · She picks her own hours

The motel is open all day. She lives in room 12. **Nothing makes her stop working, and nothing makes
her start.**

- **Night, 10pm to 6am** — empty road, few arrivals, **little money**, and both men to herself.
- **Daytime** — more arrivals, more money, **and people around who can see her.**
- **The cost** — hours worked are hours not slept, and tiredness does not forgive.

**Why this is better than skipping the day.** I proposed skipping it earlier today and then dropped
that, for three reasons:

1. **The hour becomes the difficulty.** At 4am the road is dead — going without a bra costs her
   nothing. At 2pm there is traffic and a queue at the desk. **The same act is free at night and
   real in daylight.**
2. **The money becomes a choice.** More hours is a closer ticket and a worse next shift.
3. **It makes the trap worse, not better.** She lives there and can work as much as she likes.
   Nobody stops her. That is a harsher cage than a fixed shift.

**What it costs us:** the world needs proper schedules across the whole day, not just eight hours.
Del has to sleep sometime. That is more work — and it is also what stops the place feeling like a
stage set.

**For the first version:** the night shift plus one day shift. Enough to prove it works without
writing twenty-four hours.

### 13 · What the job actually is

Her duties are not a backdrop. They *are* the three engines.

- **Take a check-in** — the money, $6 a room. And a stranger at the counter, looking at her.
- **Run the audit**, 2am to 4am — the cash drawer and the day's totals. Del's money, and hers.
- **Walk the property** — how she gets away from the desk. Past twelve doors, past room 6, into the
  lot.
- **The laundry** — other people's sheets, warm room, nobody around.
- **Turn a room** — a key, and a guest room with the guest gone.
- **The phone** — a booking is a filled room.

**Hand out keys. Walk past doors. Count the money.**

Keys are access. Walking past doors is how she sees things — **so the corruption engine is a job
duty.** She never has to go looking for it; she is supposed to walk past. And counting the money is
the debt, and Del.

The other half is that **she stands behind glass and people come to her.** She never has to go
looking for an audience either. The job brings one every hour or two.

**And the audit answers the money question.** She reconciles the drawer at 3am and the $80 line is
sitting in the day's totals in Del's handwriting. No invented bill, no extra screen — a real duty of
a real job, exactly where the story already puts it.

**Dropped** because they pass time and do nothing: setting up breakfast, cleaning the lobby, wake-up
calls.

## Block C — these two, change whenever

### 14 · Three needs, and each one closes a real door

A need that does not close a door is just a chore. So each of these takes something away.

**Tired.** Drops across the shift. Too low and she cannot do anything that takes half an hour or
more — the night ends early and she misses whoever comes in at 3am. She sleeps in room 12, or on the
cot in the office. Coffee holds it off.

**Hungry.** Drops across the shift. **The kitchen** fixes it — something on the table if she is in a
hurry, the fridge if she has time. What it costs her: **she has to leave the desk to eat.** Nobody
is at the desk while she is in the kitchen, so a car that pulls in gets no key — and an empty room
is six dollars she does not get.

It never says no to her. It just costs money.

**Dirty.** Drops daily, faster over a shift. **The shared bathroom** fixes it. What it costs her:
**she will not let anyone look at her.** Every step of the climb that is about being seen is shut
until she has washed.

⚠️ **This is the best need in the game, and it is because the bathroom is shared.** She *has* to
wash. The shower is communal. Who is in there depends on the hour.

**A need that pushes her into the risky room is worth far more than one that just empties a bar.**
The whole chain: she gets dirty → she has to wash → the shower is shared → somebody is in there →
corruption goes up → corruption unlocks something on the exhibitionism list → exhibitionism decides
whether she does it where she will be seen → being seen puts corruption up again.

That is the one that matters most. The whole game is about being looked at, so a need that closes
*being looked at* is aimed straight at the heart of it, instead of being a bar that empties next to
it.

### 15 · How crude each man gets

A **ceiling, not a target** — writing softer than the ceiling is a mistake, not caution.

- **Del** starts at *tits, ass* and ends at the full crude vocabulary.
- **Marek** is coarser earlier and ends coarsest in the game. He has nothing to protect and no
  reason to be careful.

**The crude writing lives in the repeatable scenes** — the office at 1am, the corridor, room 6. Not
in a big one-off finale. If the filthiest writing in this game is somewhere the player sees once,
the game is cold and it does not ship.

---

## What I need from you

**Everything in Block A needs a yes**, because after we ship it is not a decision any more.

**Both things I was unsure about are now closed:**

- **#2** — she is a written character. Your call, 31 August.
- **#11** — the debt does not need an invented bill. She sees it in the night audit (#13), which is
  a real duty of the real job.

### 16 · The screen where she gets her name `[new] 2026-08-31`

The engine has a built-in character screen. If we switch it on, the player sees it right after the
age warning and before the story starts, and it holds whatever fields we ask for.

**We are switching it on, with one field: her name.** Nothing else — no hair, no build, no body
type. She is a written person, and letting the player assemble someone the writing then argues with
is how a character stops being a character.

**The good part:** the name question stops being a paragraph in the middle of the opening and
becomes a form field, which is what it always was.

**The bad part, and it is genuinely bad:** the screen's own words are baked into the engine and we
cannot change them. It says *"Customize Characters"* and *"Personalize the characters in your
story"* — a software voice, on the second screen of a game about a motel at night. The one line we
do control is the description above the field, and it reads: *"Nineteen, three weeks at the Wayside,
and tonight you are on the desk by yourself."*

If that trade turns out to be the wrong one, turning the screen off puts everything back the way it
was. Nothing else depends on it.
