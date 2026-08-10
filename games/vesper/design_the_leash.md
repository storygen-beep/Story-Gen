# Vesper — Locked Design: THE LEASH (Act 2 · 1b)

> **What this doc is.** The authoritative design for the chapter after *The Archive 1a* — the chunk the
> shipped 0.1.7 end card promises the player by name ("cracking the key — cutting your leash, opening the
> file, and finally reading what you are — plus what becomes of Mercer loose in the Reach", `5_scenes.toml:7465`).
> It **supersedes** the three-bullet sketch at `design_beat_archive_v2.md` §12 ("Handoff to 1b — The Deal"),
> which is banner-marked in place. It keeps that sketch's *destinations* — the file read, the controller,
> Vane fled, Bastien waiting, the Chairman inbound to the arc beyond — and replaces its *shape*: there is no
> "deal" scene and no controller-trade, because the trade already happened in the 1a close. What replaces it
> is a repair grind on her own hardware, a man with a new name, and three failures.
>
> **Status:** ✅ **DESIGN LOCKED 2026-08-09** with LO, in conversation. **NO TOML yet.** `design_book.md` +
> `authoring_state.json` folded the same turn (rev 112); the plan is seeded `beat_0068`–`beat_0086`,
> all `status=planned`. Build one verified increment per turn, green at each.
>
> **Provenance.** Locked with LO across one design conversation, 2026-08-09. Two shapes I proposed were
> **reversed by LO and are recorded here as rejected**, because both are tempting and would come back:
> (1) *Mercer as a test bench* — she keeps serving him so Kess can take readings. Rejected: the 1a close
> ends *"the deal's paid; they're quits"*, so going back to serve him for free un-spends the one thing she
> bought, and it makes him equipment rather than a person. (2) *Mercer as the physical lock* — the key needs
> his living hand on it mid-act. Rejected: it contradicts Wren's own closing thought (`5_scenes.toml:7402`,
> *"Keyed to him, sure — until a man who takes machines apart for a living gets it under a light"*), which
> already told the player Kess is the solver. LO's shape restores Kess as the solver and makes Mercer a man
> with a life she visits.
>
> **Engine claims.** Reused verbatim from shipped systems (the `equipped_weapon`/`drain_charge` loadout, the
> triggerless drain + control canvas, the banded `[group]` chain, the `_drains_done` trait-counter pattern,
> the coin economy, `entry_from` locations, `[[npcs.schedules]]` → portrait hub). Two claims marked
> **⚠️ verify at build**: the exact reload/idle semantics of a second loadout-shaped trait, and whether a
> `[group]` chain banded on a 0→4 counter renders correctly at every band.

---

## 1. What this chapter is (the fantasy)

She has spent the whole game unable to do one thing.

Not forbidden. Not afraid. **Unable** — a piece of hardware older than her frame, seated under her core, that
makes her weapon refuse to fire on the man whose name is on her papers. Kess found it in Salvage and told her
what it was (`5_scenes.toml:5108-5115`): *"There's a man you can't point your teeth at… That's this."*
She has never asked why. The not-asking is so complete she has never noticed it has a shape.

This is the chapter where she takes it out.

The fantasy is **not** revenge and it is not escape. It is narrower and worse than that: she goes back to the
man who owned her, on her own feet, and lets him have her exactly the way he always did — because that is
where the test has to happen. Three times it fails, and she has to finish, and smile, and leave. The fourth
time it holds.

The charge lives in the gap between what the scene *looks* like and what it *is*. Every attempt looks
identical to two years of her life: a bored man using a thing he owns. What has changed is that this time
she came on purpose, and there is something hidden in her chest that she is trying to fire while he moves
on top of her, and he will never once look at her closely enough to notice.

**And the win is a trap.** The drain finally fires, she takes her owner apart in ten minutes he will never
remember — and what she extracts is that the key only ever spoke for one name. She isn't free. She's carrying
a hall pass with his name on it. That is what makes the extraction the real ending.

---

## 2. Starting state (where 1b picks up — the shipped 0.1.7 end-state)

`cap_1a_close` (`5_scenes.toml:7361`) leaves her:

- **On `underworld_strip`**, alone. Mercer walked off into the dark. `archive_1a_done` + `controller_held` set.
- **Holding two locked objects**: her sealed build file, and the controller for the governor. Mercer handed
  the controller over sneering — *"It's keyed to me, girl — my hand, my print, it's a dead lump of metal to
  anyone else alive."*
- **Sealed out of the Spire permanently.** Both rides up are dead (`3_activities.toml:102-110`, `:180-186`),
  and `penthouse` + `vance_securities` are locked (`1_metadata_and_locations.toml:524-530`, `:576-580`).
- **With `Core: Locked` still lit** — `core_sealed` from the Salvage verdict; the sealed partition only the
  Site opens.
- **Owing `kess_debt`**, paid down in `coin`.
- **With no bed and no charger.** Every Charge restore in open play is at `cradle` (`3_activities.toml:260`,
  `:291`), which is four rooms deep inside the sealed Spire. So is the wash, the drill bench, the weapon
  swap, the wardrobe rack, and the memory store. **This is a live defect in the shipped build** — the fix was
  written (`08ec2e1`) and then cut with 1b (`187f521`). Increment 1 of this chapter is that fix.

What she still carries and can use: the drain (`equipped_weapon = 1`), the emitter, `coin`, `fighting`,
`stealth`, and the whole underworld — the Undertow, the House, the Pit, the market, the crew's rooms.

---

## 3. The berth — rent, the feed line, and the first door that is hers

She goes to Kess because he is the only person down here who knows what she is made of, and because the
close already pointed her at him.

She gives him the file and the controller and asks for somewhere to live. He points at his feed line and
names his price: **she pays per night, in coin.** *"Coin dries up, so does the arrangement."*
**That feed line is her charger now.**

This is the load-bearing inversion of the chapter and it should be written flat, not underlined: up top she
was maintained for free, because she was equipment and equipment gets serviced. Down here she pays to stay
alive. The cradle was the company's. The feed line is a bill.

**What the coin buys:**
- A curtained bunk over the line — a night on the feed (full Charge, day advance, drain reload), 10 coin.
- **The floor:** *crash rough* — free, partial Charge, no day advance, no reload. The player can never brick
  themselves, and coin **never** blocks the mainline.
- **And it buys Kess's time.** A paid night keeps him working on the key for a few days. Stop paying for
  nights and he stops touching it — not out of spite; he is a tradesman and she is not a charity. That is
  what makes the House and the Pit stop being idle side-earning: she is fucking strangers for money to pay a
  man to cut her leash.

The upkeep is an **authored coin sink**, not the engine `[settings.rent]` system — and that is now a
*verified* call, not a stylistic one. The engine's rent hard-redirects every location and the navigation
screen to its RentDay passage while a payment is due (`v2.py:15245-15255`), which blocks her from *acting*;
this design forbids that. It also charges `money`, not `coin`. And `backfillStateDefaults` has no
`game_state` branch, so switching rent on in a shipped title leaves every carried save silently rent-free
forever while fresh players get it.

> **⚠️ Cadence corrected 2026-08-10 (rev 114, at beat_0069).** This section said *"a **weekly** rent"* at the
> fold. The beat_0068 build then put the terms in Kess's mouth as **per night** — *"You pay per night, in
> coin"* (`5_scenes.toml:5214`) and *"rented by the night"* (`:5216`) — and the cot's paid tier and quest card
> E ("Keep the cot paid") both shipped on that cadence. Rather than write a second, weekly bill the terms
> scene never named, **the paid night IS the upkeep**: one 10-coin night on the line buys three days of his
> time. Same pressure, one fewer canvas, and the fiction and the mechanic finally say the same thing.

---

## 4. The cast (Kess · Mercer · Bastien — and who is deliberately absent)

**Kess** — the spine. Shipped register: clinical and consensual, *operated not desired*, reads a body the way
a mechanic reads an engine. He is not a friend and not a lover; he is a man who wants coin and the
interesting problem, and she is the most interesting problem that has ever been on his cradle. He never
learns Cain's name and never asks.

**Mercer** — landed on his feet. A **new name**, a stall in the black market selling **Spire paper** (clean
identities, badge histories, manifests — the one craft he actually has, since he *signed for her*), and a
back room better than anything she can afford. He keeps inviting her for a drink *for old times' sake*.

He remembers owning her **fondly**. That is the whole character and it must not be softened: he is not lonely
for *her*, he is lonely for **himself** — for the man who had a penthouse and an asset. She is a souvenir of
his better days. He never suspects anything, never grows, never finds out. He is wrong to the end.

**Bastien** — still runs the Undertow. The one man alive who knows what she is **and where she carries it**:
he stripped her drain when he took her (`design_captivity_the_room.md:61`) and gave it back on release
(`:193`). So his hands go over her at the door, every visit, in front of his own bar.

**Deliberately absent:** Cain (still off-page; his entrance is not spent here) · the Chairman (named dread
only) · Calloway and Vane (the Spire is sealed; Vane fled and is not picked up this chunk) · Colm, Sol, Rue,
Marsh (standing underworld content, untouched).

---

## 5. The file — what Kess can read and what he can't

He reads the **shape** and stops.

They are **build documents**. Not one person's — a **programme**, with many subjects, and dates in two
columns: one for made, one for the other thing. Eleven years of it. He can read the format, the tooling
notes, the revisions.

**Her own page is sealed**, and it is sealed in the same hand as the controller.

That is the join the whole chapter hangs on: **the file and the key are one lock.** Whatever opens one opens
the other. So the read isn't a reveal that lands and passes — it is the thing that makes cutting the leash
and learning what she is the *same* problem, and it means the chapter's biggest beat (her page) can be held
back to the very end without feeling withheld.

What she takes out of the read is not information. It is that there were a lot of them, and most of the
second column is filled in.

---

## 6. The spine (the full flow)

1. **She moves in.** File + controller to Kess. His price named — per night, in coin. The feed line is her
   charger, and a paid night is also a few days of his time on the key.
2. **He reads the file.** The shape, the programme, the many subjects — and her page sealed in the same hand
   as the key.
3. **He needs the owner's hand print.** The key won't wake for anyone else. She has to go find Mercer.
4. **Mercer resurfaces.** At the Undertow, under a new name. He is delighted. Then, quieter: *please, not
   that name here.* She doesn't stop.
5. **The drink ladder.** She humours him. He pours, he tells the story about the penthouse, he gets his hands
   on her the way he always did — and she lets him, because he cannot conceive of a version of her that says
   no. She takes the print.
6. **The print is a start, not a solve.** It gets Kess *a bit of an idea*. He can't crack it clean. He has to
   build, and the only way to test a build is to point her at the one man she cannot touch.
7. **THE LOOP.** Buy a part → Kess plants it in her → she goes to Mercer, lets him have her, tries to fire
   the thing hidden inside her while he's on top → it fails → the part burns → she finishes, smiles, leaves →
   earn more coin → repeat.
8. **Three failures, then the win** (§9). Each fails *differently*, and the difference is what Kess learns.
9. **The first fire.** She has stopped expecting anything; it catches. The drain fires on her owner. Control
   canvas. And the payload is the bad news: **the key only ever spoke for one name.**
10. **Bastien.** From the third failure she knows the governor isn't keyed to a man but to a **set of names**
    — and Bastien is on it. That is why she goes back down to the man who kept her in a room.
11. **The extraction.** Kess takes the chip out. Her page opens with it.

---

## 7. Mercer — the man with a new name

### The entrance (auto-fire, `underworld_bar`)

She walks into the Undertow with an errand and he is sitting there.

**Order matters.** He is *delighted first* — genuine pleasure, no defensiveness, the warmth of a man seeing a
piece of his old life walk in. Only a beat later, lowered voice, half-apologetic, does he ask her to stop
using the name Mercer down here.

**And she doesn't stop.** No defiance, no smirk, no line about it. She says it again in the very next breath
as if he hadn't spoken.

That is the first thing she has ever refused him, and it reads as **nothing**. He can't even get properly
angry, because she isn't defying him — she just hasn't changed. Which is exactly what she has always been to
him: a thing that does what it does.

**He asks three times across the visits, and gets quieter each time.** First it's a joke. Then a request.
**Then he stops asking.** That third one is where the player understands he has lost something he used to be
able to command. Three lines across three scenes; no commentary.

**She never uses the new name.** Not once, not in narration, not in dialogue.

**Her interior gets exactly one thought about it, once,** and it is flat: she notices she didn't stop, files
it, and doesn't look at it. If she gets a moment of satisfaction the character breaks.

### Why he keeps her close

Two engines under the invitations, and only the first is one he'd admit to:

1. **Nostalgia.** She is proof he was once a man who had an asset.
2. **She is a walking security hole in his new life.** He cannot afford her wandering his own bar saying that
   name. He would never put it to himself that way — he'd say she's fond of him, she's used to him.

So **she has a leash on him and neither of them has said so.** She never has to threaten him. The threat is
structural.

*(Held, not spent: her saying the name in front of someone else — Sol, a trader, one of Bastien's people.
That is the loaded version of the same beat. Keep it private this chunk.)*

### The meter

`npc_mercer.relation` goes live for the first time in the game — **re-cut as nostalgia**, not affection. It
measures how much of his old life he feels he has back in the room, and it gates **hospitality access**, not
register: take the drink → come back to his place → let him have you like he used to.

**It is not an escalation ladder.** He is at his ceiling from beat one and he never climbs; doctrine
(`trait-design.md:45`) says a static owner gets no climbing meter, and this is the exception's justification:
the meter buys *access*, never *heat*. His use-scenes differentiate by **what each one violates** — her time,
her money, her body, her patience — not by pose.

---

## 8. THE LOOP — buy, plant, try, burn (the heart of the chapter)

One cycle:

> **Buy a part** at the black market (coin) → **Kess plants it in her** at the bench, at the same seam
> Bastien's men opened to disarm her → **she goes to Mercer**, lets him have her the way he always did, and
> **tries to fire the thing hidden inside her while he is on top of her** → **it fails** → **the part burns
> out** → she has to finish, smile and leave with him none the wiser → **go earn** → repeat.

**The rules that keep it from being grind:**

- **The part burns on failure.** No free retries. She has to go earn between attempts, which is what makes
  the House and the Pit part of the spine instead of side-earning.
- **Three failures, then the win.** Three is a shape; five is the grind review this game already took once.
- **Each failure fails differently**, and the difference is the content (§9).
- **She has to hide it.** Every attempt is a scene where something is happening inside her that the man
  inside her must not notice. On the second one, that gets genuinely hard.
- **Emotional shape: nothing → pain → tease → win.** Not a counter.

**Engine shape:** the four attempts are **one canvas with an exclusive banded `[group]` chain** on the
attempt counter (`gte` + `lt` bands), not four canvases — adjacent `[group]` blocks merge into a single
if/elseif chain, so non-exclusive bands ship dead. The "part" is a **trait counter, never a wardrobe or
inventory item**: the save backfill covers flags and traits but has no wardrobe branch, and an item added in
a later release than the beat that grants it never reaches an existing save (the `cover_analyst`
post-mortem, `save-safety.md:87-112`).

**Built at `beat_0075` — the supply side, and three corrections to the shape above.** (1) There are **three**
counters, not four: `part_held` (bought, in her pocket — the arm, the shipped `repair_armed` shape),
`part_installed` (seated and live), and `mercer_attempts`. The planned `part_gen` is **dropped** — it counted
the same thing `mercer_attempts` counts, they move in lockstep by construction, and two counters for one fact
is a desync waiting to happen. (2) The install is a **triggerless** canvas reached from a hidden rung on
`hub_kess_berth`, not an auto-fire: it has to run four times and the auto-fire path hard-refuses a repeatable
canvas (`v2.py:4454`), so the only auto-fire shape that repeats is Salvage's twelve one-shots. (3) The buy is
gated `part_held lt 1` **and** `part_installed lt 1` — one part at a time, no stockpiling, which is what turns
"the part burns" from a promise into a rule.

**Built at `beat_0076` — the spend side, and a fourth correction.** (4) The four attempts are **one canvas
with per-generation NODES**, not one canvas with a banded `[group]` chain. The canvas count is unchanged and the
reason for it is unchanged; what changed is how the generations differ inside it. A `[group]` band is the right
tool for a one- or two-line variant — that is what Kess's build talk is, and those stay bands — and the wrong
tool for a variant that is four to six beats with its own cascade, because §7 check 2 folds the whole node lead
into beat 0's measured unit and four multi-beat bands there measure as a single ~250-word beat. So the evening is
shared and the failures are sibling nodes reached by mutually exclusive **choice** conditions on
`mercer_attempts`. Two consequences worth carrying: **the burn and the bump ride the routing choice**, because a
choice's effects fire on click while an exit block's fire on render, which puts the state on the reach rather
than on her arrival; and **the rung's gate widens one notch per beat** (`lt 1`, then `lt 2`, then `lt 3`) so the
loop can never route into a failure node that has not been written yet.

**Closed at `beat_0078`.** The last try node landed, so `lt 3` is the final value that clause ever takes: at
`mercer_attempts = 3` the rung goes dark permanently and the fourth evening arrives on its own, because scene 15
(`cap_first_fire`) is an **auto-fire** gated `mercer_attempts gte 3` + `part_installed eq 1`. "The rung is
absent" stopped being an in-progress fence and became a **terminal** state, which is how the live tests now
phrase it. One claim from `beat_0076` is **withdrawn** in the same pass: the argument for nodes-over-bands used
to add *"and try 3 needs a different exit anyway (it arms the Bastien thread)"*. It does not — the arming is the
counter reaching 3 and that rides the routing choice, so `.try3` exits to `mercer_room` at +30 minutes exactly
like its siblings. The rest of the argument (check 2 folds the node lead into beat 0) is the real reason and
stands.

---

## 9. The three failures and what each one teaches

**Try 1 — nothing at all.**
Dead silence. He has her face-down over the end of the bed with a thing at the base of her spine doing
absolutely nothing, and she has to finish and leave and smile. *(Built at `beat_0076`. Two details of the
sketch above were overtaken by what got built and are corrected here rather than left to contradict the game:
the part sits at **the seam at the base of her spine**, not in her chest — `beat_0075`'s install put it where
the drain sits — and she is **not on her back**, because the reach rides his anal finish, which is the one act
where her own drain has always come up empty on him.)*
*Kess learns:* it isn't a lock. It's **listening** for something, and he guessed the wrong channel.

**Try 2 — it bites back.**
Something answers, and the governor **clamps down**. Her body locks up **at the hold, with him still inside
her**, and she has to get through it without him noticing. *(Built at `beat_0077`. The sketch said **mid-fuck**
and that is corrected here: the shared evening node ends with him finishing and holding, and the reach IS the
routing click, so nothing can land earlier without banding the shared node — the shape `beat_0076` struck. The
hold is the better moment regardless: while he is fucking her he is moving and loud and self-absorbed; at the
hold he is still and quiet and against her.)*
**And she gets away with it because he misreads it.** The half of the clamp he can feel is her gripping down on
him — the one thing he has always wanted from her — so he takes it for her finally responding and is delighted.
She only has to hide the rest. The near-miss is him noticing she is shaking and accepting *"it's cold in here"*,
because looking at her face would cost him an effort he has not spent in two years. That is what makes it a
concealment scene rather than a pain scene, which is what the ceiling row requires.
*Kess learns:* it **defends itself**. It isn't a safety feature, it's a guard — and a guard means somebody is
still using it, which is the hinge into try 3.

**Try 3 — it works, for a second.**
The leash lets go. She *feels* it go — and it snaps back before she can do anything. The cruellest one,
because now she has tasted it. *(Built at `beat_0078`, 7 beats / 6 clicks, no media. Three things the build
settled.* **(1) What she tastes is ownership, not arousal.** *The leash suppresses her* **drain**, *not her
body, so the node speaks in the game's shipped instrumental lexicon — "the old pull… on him it catches", and
on the way back "Nothing catches. Cold socket, dead as before." For one second she has the beginning of a man
belonging to her, which is exactly what `mercer_finisher` canonises she has never once had off him. The live
suite asserts both halves: no arousal vocabulary anywhere, and the shipped vocabulary present.* **(2) It does
not snap — it re-checks.** *Something goes down a list, hits a gap, and shuts the door on the way back. She
feels a count and cannot tell what it counted.* **(3) Mercer notices nothing at all,** *which is canon rather
than a choice — a drained man is "emptied and none the wiser". So unlike try 2 there is nothing to conceal;
the charge is* **loss**, *and he talks about a stove he keeps not buying while the one second of her life
happens.)*
*Kess learns:* it was never keyed to a **man**. It's keyed to a **set of names**, and he has only ever been
spoofing one of them. *(Band 3, built at `beat_0078`:* "Not a man — a set of names. I've been spoofing one.
There's three more. Two I can't place. One's Bastien." *The hinge is deliberately* **split across two
surfaces and neither is a new canvas**: *she gets the sensation, he gets the diagnosis. That is §14's rule
that she never narrates a plan or a diagnosis, and it is why the 21-word band is enough.)*

**And that finding is the fork into the second thread.** The set is older than she is, and it has underworld
names on it. **Bastien is on it.** She never even tried to drain the man who kept her in that cell — now she
knows why. If a list written before she existed has a dockside crime owner on it, then it was never the
company's list, and she wasn't *fitted* with a leash — **she was built around one that was already there.**

**Try 4 — it holds.**

---

## 10. The first fire — the drain on her owner, and the bad news

By the fourth time she has stopped expecting anything. She goes through the motions out of habit, and it
**catches**.

The scene must not be *"the part worked."* It is her doing the same thing she has done three times, and the
floor giving way.

**The control canvas** runs to the standing carriage rule — Q&A **in his own dialogue**, his voice under her
command, never narrated summary. What she takes:

- Who signed above him, and what that man was told she was.
- What Mercer himself was told she was (and how little that was).
- That **he never had the faintest idea what the governor was for.** He carried the key for two years as a
  perk, not a duty.
- **The bad news:** it only ever spoke for him. One name, out of a set. She isn't free; she's carrying a hall
  pass.

He wakes ten minutes later remembering nothing, on his own bed, and asks if she wants another drink.

**The act it ends on:** her owner emptied out and asleep with her still in the room, and her walking out into
the market holding one name off a list she has only just learned exists.

**BUILT at `beat_0079` (rev 124) as `cap_first_fire`** — an auto-fire Tier-3 capstone at `mercer_room`, 18
beats / 17 clicks, **0.93 : 1**. Four things settled in the build that this section did not specify:

- **The name above him is Halloran, Vance Asset Services**, and he is deliberately **not on the set**. Keeping
  him off it leaves Kess's two unplaced names unspent for Bastien and beyond, and it makes the bad news land
  harder — Mercer's authority over her was never the top of anything, it was one entry. He never met the man.
- **The Q&A is genuinely played**, six of her questions against thirteen of his answers, which is the first
  time in the game the standing carriage rule has actually been executed rather than narrated past. Her
  questions are all four words or fewer; the payload never appears in narration, only in his mouth.
- **The part is NOT burned.** §9's own heading is *"Try 4 — it holds"*, so the build works and keeps working.
  That closes the parts economy on its own and it is load-bearing for `beat_0080`, whose scene-17 fix reads
  `part_installed gte 1`.
- **It exits to `underworld_market`**, which kills the auto-fire chain and is this section's own closing image
  at the same time.

**And blueprint scene 16 — `loop_mercer_warm_tap` — was built in the same beat**, because §17's sequence gives
it no turn of its own, because `mercer_drains_done` is a constant without a repeat, and because his room would
otherwise go flat at the exact moment the chapter says she owns him.

---

## 11. Bastien — the name on the set, and the smuggling problem

This is **not** optional side content. His name came off her own leash; that is the reason she goes down there.

**The question:** why was Bastien buying her build file? (Vane copied → Colm carried → Bastien bought — the
pipe 1a established.)

**The mechanic:** he strips her at the door. Not violence — a search, unhurried, in front of his own bar,
because he is establishing in public that he still may. So the arc is **not seduction, it's smuggling — and
her body is the bag.** Worse than it would have been a chapter ago, because now she has to get **two** things
past him: the drain *and* the controller. And she needs both, because the drain alone does nothing on a name
that's on the set.

**Routes past the search** (one per capability she already owns): market gear + `stealth` — which finally
gives stealth a second customer in the entire game; a Kess-made carry that reads as ordinary hardware; or
seated inside her already, which means she takes his hands with it in her and cannot flinch while he checks.

**BUILT at `beat_0081` (rev 126) as `bastien_door_search`** — a flat solo link at the bar, repeatable so it
plays every visit, and its exit is the only route into `bastien_backroom`. Four things the build settled:

- **THREE routes, not four — the Kess-made carry collapsed into "seated inside her."** They were the same
  idea wearing two hats, and the seated one is the one the chapter is about: the thing that will free her
  goes back inside the seam Bastien's own men cut open to disarm her. It is `kess_seat_controller`, the same
  bench and the same register as the parts loop.
- **⚠️ NO FAIL BRANCH, and it is the load-bearing call.** He is *establishing that he still may*, so this is
  not a challenge she can lose — a fail state would make it a lock-picking minigame and turn the beat into
  pain-as-spectacle, which the rev-122 governor row already named as the failure mode. **She always gets in.
  What varies is whether what she needs got in with her.** Route C (found) is not a punishment: the thing
  goes on his desk, he hands it back at the door, and the cost is a wasted evening — which is real, because
  the drain alone does nothing on a name that is on the set.
- **The room is NAV-INVISIBLE** (no `entry_from`, plus `auto_exit = false`), which is what makes the search
  unskippable and simultaneously stops his schedule leaking a portrait badge onto the Undertow card.
- **Stealth's threshold is 30**, the same band the burned yard's top guard check uses, so route B is a real
  investment rather than a rounding error.

**His lever is curiosity, not desire.** He is not a cruel man, he is an *interested* one — the cell was a lab
and he took numbers. A standard seduction ladder bounces off him; he'd enjoy it and give nothing. What he has
never been permitted is being read himself. That is why the drain destroys him and a ladder wouldn't.

**The payload:** he was buying it **for Cain**. The man she was built to kill has been trying to find out
what they did to her.

⚠️ **RESOLVED AT `beat_0082` (rev 127), because this paragraph and §15 could not both be built.** §15 reserves
Cain: *"not on page, not named by Bastien beyond 'a man who wanted to know what they did to you.'"* **§15 wins,
and the beat is bigger for it.** Bastien **does not know the name either** — the money came through three
hands, and the man who came through his far door a year ago never turned round. What the drain takes is the
thing he has never said aloud and **works out while she has him open: they were the same man.** The buyer
wanted *what was done to her*, not what she can do, and asked one question twice — *was she made, or was she
taken.*

That is this paragraph's content in full with only the **label** withheld. It keeps Cain's entrance whole for
the chapter that opens it, it pays off Bastien's own year-long question (`beat_0080`: *"the only thing I've
ever wanted and not got"*) **inside** the drain rather than beside it, and it hands the name to §12, where her
page opens. **And she does not supply it either:** `captivity_cain` says the four words are a thing she
*"cannot hold"*, so her one `thought_bubble` reaches for the name and finds *a shape where a word should be*.
Having her produce it here would have quietly retconned that line.

**His ceiling stays scoped** — see §14. The Undertow is not the cell.

**OPENED at `beat_0080` (rev 125) as `cap_bastien_walks_in`** — blueprint scene 17, an auto-fire Tier-3
capstone at `underworld_bar`, 15 beats / 14 clicks, **0.79 : 1**, the best canvas ratio in the game. Four
things the build settled that this section did not specify:

- **He did not release her — he LOST her.** `captivity_cain` (`beat_0042`) is the fact this whole arc rests on
  and it was nearly missed: a man came through his far door, argued him to a stop, put the drain back in her
  socket and carried her out. So he is not looking at a returning asset, he is looking at **a thing that was
  taken off him, walking and repaired** — and he has a question of his own he has carried since. That is what
  makes him sit down, and it is why the scene needs no threat to be frightening.
- **Cain stays reserved (§15) and the canvas is greppable for it.** Bastien gets *a man who came through my far
  door*, and nothing else — no name, no guess, no history.
- **The search is promised, not played.** It lands in his own mouth as **his rule** — *nobody comes into my
  room carrying, I check, I don't make exceptions* — which plants scene 18's gate as a fact about him rather
  than as a mechanic handed to the player, and keeps this canvas clear of the unsigned ceiling row.
- **The reversal is the last line.** She came down here to find him; he thinks she has come back.

⚠️ **And an engine-forced shape was found before it could be built wrong — see the blueprint's row 18.**
Bastien must **not** get a schedule at `underworld_bar`: a row at a *public* location parks his portrait badge
on the nav card, and that card has been visible since Act 1. He gets a **locked location behind the bar** at
`beat_0081`, and **the door-search becomes its entry gate** — which is what this section wanted anyway.

---

## 12. The extraction — and her own page

Even after the first fire she is not free. She is carrying a **device**: something she has to switch on
mid-act, that draws power off her core, that speaks for exactly one name, and that anyone who searches her
can find. That is a hall pass, not freedom — and the chapter has to say so plainly, because otherwise the
extraction reads as the same win twice.

So Kess takes the chip out.

He can do it now and couldn't before: a live key means he can hold the governor quiet while he cuts, which is
the thing his Salvage line ruled out (*"pull it blind and it takes you with it, and I don't do wakes"*).

**And her page opens with it** — the same hand, the same lock. The last beat of the chapter is her reading
what she is: the Vance humanoid programme, eleven years, many subjects, and her at the centre of it. Mercer
never knew he had sent her to steal herself.

Tier-3, once, and her interior stays rationed even here — the horror is on the page, not in her head.

**BUILT at `beat_0083` (rev 128) as `cap_extraction`** — 18 beats / 17 clicks, **1.30 : 1**, and the chapter's
last content beat. Four things the build settled:

- **⚠️ CAIN DOES NOT LAND HERE, reversing what `beat_0082` recorded.** That beat said the name would be handed
  to scene 20. §15 says his entrance is a whole chapter, and spending it on the last page of a release that
  then goes quiet buys a gasp and costs the door. **What the page gives her is what this section actually asks
  for — what she is:** the programme's real size, her designation *four years older than she is*, the word
  **BUILD** she could never read past, and the two date columns from `cap_file_shape` — the second filled most
  of the way down, **and hers is blank.** The hook names nobody: the programme **closed**, and her page was
  sealed eight months later **by a hand on none of the sign-offs.**
- **She reads it aloud, and that was a correction at measure time.** The first draft carried the reveal as
  **182 words of unbroken narration** and the canvas measured **2.31 : 1** — the exact defect folded into the
  skill one beat earlier, committed by its author. Kess is three feet away having said he would rather not
  know, so what she reads goes somewhere, and his holding to it two beats later lands harder for it.
- **The feed line is deliberately not gated.** The chapter's closing beat is not blocked behind an upkeep
  meter, and the live suite asserts it fires with the line lapsed.
- **The last line is the door**, with no name in it: *"Somewhere out there is a man who came through a door for
  her and would not say why he cared. He does not have a name yet."*

---

## 13. The controller as a carried switch (the loadout rules)

Once it works, the controller is **an item with a state**, mirroring the shipped `equipped_weapon` /
`drain_charge` loadout:

- She **carries** it or she doesn't.
- She **brings it up** — *on = the controller is running = the leash suppressed*. Off is idle.
- Running it **costs power**, reloaded at Kess's bench (which feeds rent).
- **It only ever surfaces on blocked targets.** Renner, Calloway, Colm, Marsh and the brothel were never
  blocked and get **no new step**. Adding a toggle to shipped content would tax the whole game for one
  chapter's mechanic.

After the extraction the switch is gone and the block is gone with it — there is nothing to carry and nothing
to run.

⚠️ **THAT SENTENCE IS A BUILD TASK, NOT A FLOURISH — and at `beat_0083` it turned out to be hiding a live
dead-end.** `loop_bastien_finisher`'s drain exits required `controller_state gte 1`, and `controller_state` is
0 for the rest of the game from the moment the chip comes out. So **every future anal finish would have routed
to the nothing-happens branch, permanently**: the player would own the man and get nothing, with no way back
and nothing on screen to show it, because when no choice passes the engine emits a `console.warn` and a bare
Continue. **Five surfaces read the retired state and all five are handled at `beat_0083`:** the finisher (four
exits to six, partitioned on `leash_cut`) · the anal pose (a fourth band, and the switch retires) ·
`bastien_door_search` (a fourth band and route — *he searches her, finds nothing, and says it was never about
what she was carrying*) · `hub_bastien`'s bands · the seat-the-key rung. **The Bastien loop stays playable**;
the key stops being the price of admission. The general form of this hazard went into the skill
(`lanes.md` — terminal-flag sweep).

**BUILT at `beat_0082` (rev 127) — the switch shipped, ⚠️ THE CHARGE ECONOMY WAS CUT.** `controller_state`
(0 idle / 1 running) is real and lives where §13 said it should: a **choice at the anal pose**, because
bringing it up is something she does *mid-act*. It is zeroed by every loop entry and every finisher exit, so
she never leaves it running between visits — which is what survives of the power cost in fiction.

**What was cut, and why it is recorded rather than dropped:** the **charge meter and the bench reload**. It is
an economy with exactly **one customer** — the chapter has one blocked target and the switch dies at the
extraction — so it would buy one more errand in a cycle that already runs bar → door → room, against §8's own
rule that the loop must not read as errands. §13 specified it when the chapter still imagined more blocked
targets than it ended up having. The *carry* axis survives separately and is real: `controller_seated` and
`controller_through` (`beat_0081`).

**And the switch is the second half of a two-condition contract**, which is the shape that makes it teach
itself: the shipped loop already teaches *only the anal finish opens the drain*; Bastien adds *and only with
the key running*. Get it wrong and the finish lands on the shipped cold-socket nothing — **no fail screen, no
lost progress, just a wasted evening.**

---

## 14. Register (owned by the author-game skill)

Person: **third**, unchanged, whole-game immutable. Lanes 1/2/3 flat at ~35–40 words per beat; Lane-4
capstones are **more beats (10–20), not thicker beats**.

**The dialogue ratio is a hard target for this chapter.** ≤ 1.5 : 1 narration-to-dialogue in any scene with a
present NPC; > 3 : 1 is a fail. Vesper currently runs 7.25 : 1 — the longest-standing defect in the corpus.
Mercer's scenes are the natural place to fix it: he *talks*, constantly, about himself, and every line of it
is characterisation.

⚠️ **The single largest move on that ratio came from a rule nobody had been following** (`beat_0079`, rev 124).
`design_book.md` has carried a standing **control-canvas carriage rule** since the Renner drain: the extraction
is *played as a Q&A in HIS own dialog, not narrated summary*. Measured at this beat, **all three shipped drain
payloads break it** — `loop_renner_finisher.drain`, `calloway_drain_canvas.d0`, `colm_drain_canvas.d0`, with
**zero** player dialog blocks between them. `cap_first_fire` plays it instead and lands at **0.93 : 1**, the
best canvas in the game, moving the whole-game figure 2.80 → **2.72 : 1** in one beat. The lesson is not about
Mercer: **a drain scene is a conversation, and writing it as narration throws away the cheapest dialogue in the
game.** Bastien's back-room drain at `beat_0082` inherits this directly.

**Her interior stays rationed** — one `thought_bubble` per scene. **She never narrates a plan.** The player
knows what she is doing; the moment she is seen being clever about it, the character breaks. The three
attempts are written as things happening *to* her body, not as a heist she is executing.

**Ceilings needing declaration before any hot beat ships** (see `design_book.md` → *Content register &
ceilings*):

- **Kess — the install work. ✅ SIGNED rev 120** (LO's call at `beat_0075`; the authoritative text is
  `design_book.md` → *Content register & ceilings*). Extends the shipped clinical/consensual row: her body
  opened at the seam and hardware seated in her, **no degradation and no "she wanted it"** — she is
  *operated*, not desired. New relative to Salvage: invasive, repeated, and she is awake for it. And, added at
  signature, **(iii) the install is explicit and it is NOT sexual** — the Salvage row's *"explicit at the
  ceiling"* was written for scenes with sex in them and this one has none, so the precision is anatomical and
  surgical rather than erotic, with **no arousal on either side, no pain and no comfort**. She is *handled*,
  and the horror is that it is routine and quieter than the cell. The words stay on **her body**, never on the
  hardware (Rule 9).
- **Mercer — the visits and the inversion. ✅ SIGNED rev 119** (LO's call at `beat_0074`; the authoritative
  text is `design_book.md` → *Content register & ceilings*). Three things his shipped ownership-degradation
  row doesn't cover: (i) the **nostalgia warmth** — fond, generous, entirely about himself, never affection
  *for her*; (ii) the **inversion** at the drain — for ten minutes it is his body answering with his will
  never consulted, the exact sentence the game has used about her since beat one; (iii) added at signature,
  the **underworld use-scenes run warm and crude in the same breath** — he uses her exactly as he always did,
  full anatomical words, and he is pleased the whole way through, talking about the penthouse while he is
  inside her. No name-calling, no escalation of cruelty; the obscenity is that he is having a nice evening.
  **Anal is held** for the loop and the first fire, where the immunity and the drain live.
- **The governor acting on her body, outside the cell. ✅ SIGNED rev 122** (LO's call at `beat_0077`; the
  authoritative text is `design_book.md` → *Content register & ceilings*). A **new row**, because every other
  row governs a person's register — Mercer's what he does, Kess's what his hands do, Bastien's what he says —
  and none of them reaches her body acting on its own, which is the entire content of tries 2 and 3. Measured
  before it was drafted: the whole scenes file held exactly two pieces of pain-register prose, the cell's
  overflow (scoped to `captive_room`) and the install saying explicitly that what she feels is *not* pain —
  damage to her outside that room had never shipped. (i) The clamp is **damage and not sexual**: no forced
  orgasm, no arousal, no ecstasy-as-damage; the governor is *design, not damage*, and a guard bites the way a
  machine bites. (ii) The **captivity re-spec is not widened** — one event, once; no pack, no restraint;
  Tier-3 zero. (iii) The **charge is concealment, not pain** — the camera is on what she does to hide it and
  on him being pleased and oblivious; pain as spectacle is the failure mode, and there is no fail branch,
  though it must read as very nearly failing. (iv) One `thought_bubble`, and it observes; Kess does the
  diagnosing on the next bench. ⚠️ **Read at `beat_0078` and NOT re-signed.** Clauses (i) and (iii) are worded
  around try 2's clamp, and try 3 has neither a clamp nor anything to conceal — so try 3 spends **less** of
  this row than try 2 did. **A ceiling is a maximum, not a quota**, so that is coverage rather than a breach;
  the clauses that bind there are (i)'s no-arousal-on-either-side, (ii)'s Tier-3 zero, and (iv).
- **Bastien — outside the cell. ✅ SIGNED rev 126** (LO's call at `beat_0081`; the authoritative text is
  `design_book.md` → *Content register & ceilings*) — **the last row in the game to be signed, so nothing in
  this chapter is blocked on a signature any more.** **NOT widened**, and it gained two clauses at signature:
  **(i) he never learns what she is** — the drain takes his answers and nothing goes the other way; he may be
  closer than anyone in the game has been and still end the chapter not knowing, because if he works it out
  there is no Bastien left for the next chapter — and **(ii) she is never shown enjoying it**: the back room
  is **work**, the charge is what she is carrying, and there is no arousal register on her side in the chunk. The captivity re-spec stays scoped to `captive_room`. The Undertow back room runs at the
  ordinary owned-slave floor with his crude, degrading diction on top. The charge there is the search and the
  smuggling, not the pack. ⚠️ **Scope clarified at `beat_0080` (rev 125):** the row governs the **search at
  the door** and the **back room** — scenes 18 and 19 — and does **not** reach scene 17, the reveal, which
  shipped with nothing explicit in it and the search promised in his own mouth rather than played (the
  `rung_mercer_hands_on` precedent). **`beat_0081` is the first beat this row actually gates**, and per
  `kink-ceilings.md` §2 it cannot ship until the row is signed. Two clauses on offer at signature, not added
  otherwise: that **he never learns what she is** (the drain takes his answers, not the reverse), and that
  **she is never shown enjoying it** — the back room is work, and the charge is what she is carrying.

---

## 15. Reserved / kept (do NOT spend)

- **Cain.** Not on the set of names this chunk, not on page, not named by Bastien beyond *"a man who wanted
  to know what they did to you."* His entrance is a whole chapter and this one does not get to open it.
- **The Chairman.** Named dread only. Aldous Vance stays off-page.
- **Vane.** He fled into the Reach at the 1a close. He is not picked up here — he is the cheapest possible
  next chapter and spending him now costs that.
- **The Site / `the_site_open`.** Still the one read-never-set flag in the game. It is Cain's door, not this
  chapter's.
- **The Spire.** Sealed, and it stays sealed. No route back up.
- **Her corruption meter.** Frozen at 0 by design — the inversion. Nothing here touches it.

---

## 16. Engine & save-safety

Vesper is **shipped** (v0.1.7 public, free + paid), so this chapter is **ADD-ONLY**.

- **No renames.** No `id`, no live flag/trait key, no stat scale or tier threshold, no title.
- **New flags, traits, locations, NPCs, schedules and canvases are free** — the save backfill
  (`setup.backfillStateDefaults`, `v2.py:14549`) carries new flags and traits into old saves at their default.
- **The parts are a trait counter, not an item**, which sidesteps the one real hazard: the backfill has no
  wardrobe branch, so an inventory item added later than the beat that grants it never reaches a save that
  already passed that beat (`cover_analyst`, `save-safety.md:87-112`).
- **`kess_berth.entry_conditions`**: dropping the `salvage_done is_false` clause **opens** a door that is
  currently shut. It cannot strand anyone — it *heals* every 0.1.7 save currently stuck on the strip with no
  bed.
- **⚠️ A "paid through day N" trait is NOT AUTHORABLE** (found at beat_0069, rev 114 — bounced up here rather
  than worked around in TOML). Effect values are **literals only**: `_resolve_effect_value` (`v2.py:13519-13578`)
  takes a number or a `random` dict and raises on anything else, and the runtime path turns a string
  expression into `NaN` → `0` — **a silent no-op with no build error.** And **no condition type reads the
  clock**: of the 16 types in `triggerConditionsSatisfied` (`v2.py:3816`+), only `days_since_flag` touches
  `time_state.day` at all, and weekday gating exists only as a trigger *schedule*, never as a condition. So
  there is no way to write "set this to day + 7" or "is today past that."
  **The shape that works instead:** a **decaying counter** — `feed_line_days`, a hidden int set to a literal 3
  by the paid night, decremented 1 per day rollover by `[player.trait_decay]` (`template_import.py:1657-1666`
  → `v2.py:5532-5544`, floors at 0), and read by an ordinary `trait gte 1`. Every value is a literal, it
  charges `coin` (via `costs`, which both gates and deducts), it is save-safe (traits backfill), and it gates
  content without ever blocking a click. *(The alternative, `days_since_flag`, has shipped precedent in
  `games/jacks_world` but cannot surface a number for Kess to say aloud, reports as permanently-unmet in the
  quest-hint path, and leaves the never-paid state satisfying neither `lt` nor `gte`.)*
- **Returning-player recovery is mandatory.** The berth handoff must be gated `archive_1a_done is_true` +
  `berth_home is_false`, never on some new upstream flag, or every player who already finished 1a is locked
  out of the chapter forever. Same pattern the captivity chunk used.
- **Every new `conditions` block carries `version = "1.0"`** or it fails **open**.
- **Drains are TRAIT counters, not flags** — a triggerless drain canvas has no located setter and the
  flag-chain validator hard-fails (shipped precedent: `calloway_drains_done`, `colm_drains_done`).
- **Adjacent `[group]` blocks merge** into one if/elseif chain — bands must be mutually exclusive
  (`gte` + `lt`) or the later ones are dead. This governs Kess's build talk on `kess_install_part`, where each
  band is one line. It does **not** govern the attempts: those are sibling nodes routed by exclusive choice
  conditions (`beat_0076`, §8 correction 4), because a four-to-six-beat variant cannot live in a node lead.
- **⚠️ A choice's effects fire on CLICK; an exit block's fire on RENDER** *(verified in the built HTML at
  `beat_0075`; exit `effects`, `flagEffects` and `time_progression_minutes` are emitted as passage-level
  `<<script>>` below the body)*. Anything that should be **earned by finishing a canvas** has to ride a choice —
  which is where the loop's burn and bump live. And when no choice passes, the engine emits a `console.warn`, a
  `$flags.debug_mode` diagnostic, and a `[[Continue->…]]` escape that fires no effects (`v2.py:12890-12946`), so
  a conditional-routing exit is safe to author one branch at a time.
- **⚠️ Verify at build:** the reload/idle semantics of a second loadout-shaped trait alongside
  `equipped_weapon`/`drain_charge`. *(The other half of this item — that a chain banded on a 0→4 counter renders
  at every band — is discharged at `beat_0076` in the form it actually took: the install's `[group]` bands are
  live-verified exclusive at 0 and 1, and the attempts are choice-routed nodes instead of bands.)*

---

## 17. Build sequence (one verified increment per turn)

| # | Increment | Beats | Why here |
|---|---|---|---|
| 1 | **The home base** | `beat_0068`–`0069` | Near-free — restores the shelved `08ec2e1` blocks. **Kills the live post-ending dead-end in the shipped build.** Ship-worthy on its own. |
| 2 | **The file and the ask** | `beat_0070`–`0071` | Sets the chapter's want before any new geography. |
| 3 | **Mercer resurfaces** | `beat_0072`–`0074` | His entrance, his room, the drink ladder, the print. |
| 4 | **The loop** | `beat_0075`–`0079` | The heart. Systems beat first, then the three failures, then the fire. ✅ **CLOSED at rev 124.** The fire landed and took blueprint scene 16 (the warm tap) with it — that scene sat between this increment and the next and would otherwise never have got a turn. |
| 5 | **Bastien** | `beat_0080`–`0082` | Needs the third failure's finding to have a reason to exist. **STARTED at rev 125** — scene 17 (the reveal) landed and required no ceiling signature; ⚠️ **`beat_0081` onward is BLOCKED until the Bastien row in §14 is signed.** |
| 6 | **Extraction + ship** | `beat_0083`–`0086` | The chip out, the Quests page, media, clean build + deploy. **`beat_0083` CLOSED at rev 128** — scene 20 built, and with it the chapter's content. **`beat_0084` CLOSED at rev 129** — the Quests page, read end to end. Left: `beat_0085` (media, 22 slots) and `beat_0086` (clean ship). |

**⚠️ What the Quests pass found (`beat_0084`, rev 129) — recorded here because two of the three are
*chapter*-level facts, not card-level ones.**

1. **The spine is sound.** Ten cards, D through M, exactly one live at every reachable state from the 1a
   close to `leash_cut`, and M alone after the cut. The per-beat discipline of "each card's closer is the next
   card's opener" held all the way down without a single gap or overlap.
2. **But the boundary claim was left behind three times.** Cards E, F and G each still told the player *"that's
   where this build ends"* about a frontier the chapter had walked five rungs past — E naming the leash, the
   file and her own page as *the next release*, in the release that ships all three. The per-beat check ran
   every time and passed every time, because it asked whether the sentence was true **from that card's rung**.
   It is not a rung-level claim. Now: one card names it, and it is M.
3. **The chapter never had an NPC tier, and Act 1a's had gone stale underneath it.** Mercer and Bastien — the
   two conquests this chapter is built on — had no section at all, while Calloway's ladder and half of Colm's
   end card went on pointing at the Spire that §-one's close hard-seals, and Renner's section *vanished* on his
   own drain even though his office stays open for the rest of the game. Nine cards fix all of it. The general
   rule went into the skill (`quests.md` §10): a card is a **direction**, so it is coupled to reachability, and
   sealing a region is a whole-table sweep.

**Kess deliberately gets no section.** He is the bench, not an arc, and the only thing a Kess card could carry
is the cot and the feed line — which is upkeep, and upkeep lives on the HUD (`quests.md` §8). The Story-Goal
tips already say "keep the cot paid" at every rung that needs it.

Total ≈ **30–36 canvases**. Against `lanes.md` budgets: Kess ~9 (Service 6–10) · Mercer ~12 (static owner
6–12, **at the ceiling**, and only because the four attempts collapse into one banded canvas) · Bastien ~9
(antagonist 6–10).

---

## 18. Open items — decisions still owed

**Answered with LO's approval of the fold plan (freely editable — each is one string in one place):**

1. **The programme's age — eleven years.** Old enough that the second column reads as a graveyard, and it
   leaves room for her to be late in the cohort.
2. **"On" = the controller is running = the leash suppressed.** She *brings it up*; it's *live*.
3. **What Mercer sells — Spire paper.** Clean identities, badge histories, manifests.
4. **Mercer's new name — Dell.** One syllable, forgettable, sounds picked off a manifest. She never uses it.
5. **Cain is not on the set of names.** Bastien alone carries the beat.
6. **Bastien's ceiling stays cell-scoped.**
7. **Kess's ceiling — a new row**, as drafted in §14. ⚠️ **Clarified at `beat_0075` (rev 120).** This item was
   read as a signature when the ceiling came due, and it isn't one — what it settled is the *structural*
   question, that Kess gets his own row rather than stretching the shipped Salvage clinical/consensual row over
   the install work. The row's contents were still drafted-and-unsigned, which is why `design_book.md` kept
   banging its UNSIGNED banner and §14's bullet carried no ✅ while Mercer's did. **The contents were signed at
   `beat_0075`, with clause (iii) added at signature.** The reading to carry forward: an entry in this list
   answers a decision, and a ceiling is only signed by `design_book.md`'s Content register saying so.
8. **The upkeep is an authored coin sink**, not the engine `[settings.rent]` system — see §3 for the verified
   reasons (the rent intercept blocks navigation; it charges `money`; it is silently dead on carried saves).
9. **Cadence = per night, not weekly** (rev 114, at beat_0069) — the paid night IS the upkeep. See §3.
10. **The upkeep meter is a DECAYING COUNTER, not a paid-through date** (rev 114) — see §16.

**Still genuinely open (non-blocking, decide at the beat):**

- ~~The exact weekly rent figure~~ — **settled at beat_0069:** 10 coin a night (already shipped on the cot)
  buys **3 days**, so a week runs ~23 coin against a brothel finisher at +10, the pit at +8/+20 and Marsh at
  +15. One pit win and a client covers it. The crash-rough fraction stays at +40 Charge (it clears the
  15-Charge action floor, so a broke player can always scrape back to functional).
- ~~Whether Kess's three findings ride the install canvas or get their own short bench beats.~~ — **settled at
  `beat_0075`: they RIDE THE INSTALL**, as bands 1/2/3 of `kess_install_part`'s exclusive `[group]` chain on
  `mercer_attempts`. Three reasons, in order of weight. (1) A separate bench beat would be a **second auto-fire
  at `kess_berth`** sitting behind the install, which is exactly the chaining trap beat_0074 found live. (2)
  The install is where he already has his hands in her and is already talking, so the finding costs no new
  words and pays into the chapter's ratio target instead of against it. (3) It keeps the player's cycle to
  **four surfaces** — buy, install, attempt, earn — instead of six, and §8's rule is that the loop must not
  read as errands. Blueprint scene 14 is struck; the bands land at beats 0076/0077/0078 alongside the failures
  that produce them.
- ~~How many other names Kess reads off the set before the extraction~~ — **settled at `beat_0078`, at the
  recommended answer: two he can't place plus Bastien** — enough to be a list, not enough to be a roster. It
  ships as band 3 of `kess_install_part`: *"Not a man — a set of names. I've been spoofing one. There's three
  more. Two I can't place. One's Bastien."* Twenty-one words, which is the band ceiling exactly, and he does
  not explain how he read them — a tradesman revises rather than explains, the pattern bands 1 and 2 set.

- ~~Who signed above Mercer, and whether that man is on the set~~ — **settled at `beat_0079`: Halloran, Vance
  Asset Services, and he is NOT on the set.** A man Mercer never met, who signed a transfer and was told she
  was *sensitive recovery, one of theirs, on loan* — four lines. Keeping him off the set is the load-bearing
  half: it leaves Kess's two unplaced names unspent for Bastien and beyond, and it makes the bad news land
  harder, because Mercer's authority over her was never the top of anything. It is one editable string in one
  place. §15's reserved names are untouched — Cain is not on the set, Aldous Vance stays off-page, Vane is not
  picked up here.

**✅ CLOSED at `beat_0080` (rev 125) — the fix went in as the gate, not as a patch, because the canvas was
authored for the first time in that beat. It works only because `beat_0079` does not burn the fourth part.**
~~Opened at `beat_0078` (an ordering hazard, recorded rather than patched early):~~ blueprint scene 17
(`cap_bastien_walks_in`) is gated `mercer_attempts gte 3`, annotated *"the set is known"* — and that is now
**off by one install**. The counter hits 3 the instant try 3's routing choice is clicked, but the set is not
*known* until Kess speaks band 3, which needs her to buy a fourth part and go back to the bench. A `[group]`
sets nothing, so no "finding 3 heard" flag exists and none can be added there. **Fix at `beat_0080`: add
`part_installed gte 1`** — the same shape scene 15's gate already uses, and it needs no new state.

---

## 19. What this supersedes

- **`design_beat_archive_v2.md` §12 "Handoff to 1b"** — banner-marked in place, not deleted. Its destinations
  survive (file read, controller, Bastien, Chairman inbound); its shape does not. There is no "deal" scene:
  the controller trade already happened in the 1a close, so the chapter's engine is the *repair*, not a
  negotiation.
- **The rev-96 "go to Kess" quest card** shelved at `187f521` — replaced by the full berth on-ramp.
- **The rev-52 parked reconcile** ("Bastien's flip/drain = next chunk") — discharged here, in the form his
  casting row always promised: capture-and-flip, and the flip is her walking back in on her own feet.

Nothing in the shipped 0.1.7 build is renamed, re-gated shut, or removed.
