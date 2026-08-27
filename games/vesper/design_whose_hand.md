# Vesper — Locked Design: WHOSE HAND (Act 2 · 1d)

> **What this doc is.** The authoritative design for the release after *The Face* — the content release the
> 0.2.0 ledger asks for in its own words: *"NEXT: content. The Face closed on the raid and
> `activity_sift_the_ruin` is the only standing surface after it (ruin_depth bands at 2 and 4, pure texture)
> — the next release needs a real door behind that wall."* (`authoring_state.json` → `_active_beat`.)
>
> It answers the question the game has been asking since its first hour and has never touched: **whose hand
> was on the back of her neck.** The title is Wren's own thought-bubble from `activity_captive_wait`'s
> Glitch III — *"Whose hand."* — and this release answers it, incompletely, and the incompleteness is the
> ending.
>
> **Status:** ✅ **DESIGN LOCKED 2026-08-26** with LO, in conversation. **Amended the same day** with the
> CAIN → GRIER → SABIN reorder (§18.6) and THE RISE (§18.7), and §19 rebuilt as a real lane/place/gate
> blueprint. **NO TOML yet.** `design_book.md` and `authoring_state.json` are **not** folded yet — that is the
> next turn's work and needs LO's word. Build one verified increment per beat, green at each.
>
> **Provenance.** Locked with LO across one design conversation, 2026-08-26. **Five shapes I proposed were
> reversed by LO and are recorded here as rejected**, because each is tempting and would come back:
>
> 1. *The third piece is stored inside one of the units (Vega / Lyra / Nova).* I argued the units are the
>    perfect vault because they cannot feel what is in them. **LO rejected it outright.** Recorded because it
>    is seductive and because the reasoning that produced it — "an empty box is the safest place" — will
>    regenerate the idea if it is not written down as closed.
> 2. *She condemns a unit with falsified paperwork so the company scraps it and it comes down the pipe to
>    Kess's bench.* **LO: "It won't sound logical to me."** He is right and the failure is instructive: a
>    working field asset does not get binned over a bad line in a maintenance log, and a junior hire on
>    forged papers has no authority to sign one. Recorded as a warning about plans that are thematically
>    pretty and operationally impossible.
> 3. *The third piece is inside Mercer, and that is why the drain has never worked on him.* Mechanically
>    elegant — the owner holds the key — and **LO rejected it**: *"Not Mercer, he is alive but not him."*
>    The boss-immunity mystery therefore **remains unspent** and is still owed a payoff.
> 4. *The old machinist built her.* Reversed by LO: he was an **assistant**, he did not build her, and he
>    never knew whose memory he was carrying. This is load-bearing — his ignorance is what makes the first
>    errand work.
> 5. *The new scientist knows a third piece exists and has been refused it, and that is how she finds out.*
>    Reversed by LO: **Grier** is the one who knows. The reveal comes from the Reach, from a person, at the
>    end — not from office complaint in the middle.
>
> **Engine claims.** Everything structural here is reused from shipped systems and was read in this repo
> during the design conversation: the `[[clothing]]` cover items + the `face_worn` flag split
> (`3_activities.toml:2672`, beat_0116), `show_when_locked` + `locked_text` on a travel choice
> (`3_activities.toml:106`), the portrait-hub → rung → triggerless loop → finisher → drain-canvas rig
> (`hub_colm_undertow` / `loop_colm_backroom` / `loop_colm_finisher` / `colm_drain_canvas`), the
> `_drains_done` trait-counter pattern, the `npc_at_location` presence gate that actually bites where
> `requires_npc` is inert on the auto-fire path, `[[npcs.schedules]]` → portrait hub, banded `[group]`
> chains, and the coin economy. **Three claims are marked ⚠️ verify at build** and are called out where
> they land: the memory-store relocation, the conditional drain, and the two-token cover gate.

---

## 1. What this release is (the fantasy)

*The Face* was the chapter where she wanted something and had to pay for it. She got her page, she got a
name for the man behind the far door, and she ended it holding a weapon on him with nothing new to do.

**This is the release where she gets a self back, and finds out the best part of it belongs to somebody
else.**

The want is the same want, one turn deeper. She has read her own page. She knows a hand came back eight
months after the programme closed and sealed it. What she does not have is any memory of ever having been a
person. She has four leaks — the tears, two glitches at the cradle, and the hand in Bastien's cell — and no
way to reach any of them.

Cain has one thing she needs and it is not the truth. **It is the method.**

The release's inversion, and the thing that makes it different from the three before it: **she is hired for
her mind.** Every cover she has ever worn has been a body cover — dockhand, analyst, barmaid, whore. She was
built as an intelligence-extraction weapon, she is measurably brilliant, and in two acts not one person has
ever wanted her for what is between her ears. The first time a man asks her opinion and then waits for the
answer, she has no protocol for it.

**And the release's cost:** the last step out of being used is going all the way back down into it, on
purpose, because she chose it. The first time it was done to her. This time she asks.

---

## 2. Starting state (the shipped 0.2.0 end-state)

Read from the build, not from memory.

- **She is on `underworld_strip`**, having walked out of `cap_the_lab` on the choice `text = "Don't."` She
  never lowered the taser. `lab_seen` is set and `cain_lab` is sealed behind her — a door she has been
  through once and cannot open.
- **`raid_done` is set.** The Undertow burned. `hub_bastien`, `bastien_door_search`,
  `activity_bar_work`, `underworld_bar_bathroom` and `activity_bar_change` are all shut.
- **`activity_sift_the_ruin` is the only standing surface the last release opened** — a card at
  `underworld_bar`, `ruin_depth` bands at 2 and 4, pure texture, no body.
- **Standing repeatable sex surfaces that survive:** Renner's office (`loop_renner_office_sex`), Mercer's
  room (`loop_mercer_lockup`), Colm's back room (`loop_colm_backroom`), Calloway's file room
  (`loop_calloway_sex`), The House (`underworld_brothel_loop`).
- **Income that survives:** The House (finisher pays coin), the pit (`+8` / `+20` on a Fighting check),
  `work_depot_haul` (Renner, needs `cover_dockhand`), `work_the_case` (Calloway, needs `cover_analyst`).
  `activity_bar_work`'s 15-coin shifts are gone with the fire.
- **She owns the face.** `face_bought` is set; `activity_the_face` at `the_cot` toggles `face_worn` on and
  off, repeatable, forever. This is the single most important asset she carries into this release and the
  last chapter built it to get into a bar.
- **The Spire is sealed.** `activity_travel_to_spire`'s ride-up choice is greyed with
  *"The Spire's sealed to her now — sweeps on every floor, her face on every camera at the curb."* The
  penthouse, `wren_room`, `wren_floor`, `vance_securities`, `docs_department` and `docs_vault` are all
  behind that seal.
- **⚠️ `canvas_chip_view` — the memory store, the empty FRAGMENT 01 slot — is at `cradle`, which is behind
  that seal.** The UI this entire release fills is currently unreachable. §16.2 fixes it.
- **⚠️ Sol and Colm are still standing in the burned bar.** `hub_sol_undertow` and `hub_colm_undertow` sit
  at `underworld_bar` with **no `raid_done` clause**, and both `[[npcs.schedules]]` rows are unconditional
  (Sol 10:00–23:59, Colm 19:00–23:59). Post-raid, Sol tends a bar with a hole in the wall and Colm takes her
  into the back room of it. Same bug class as the rev-157 fix, one door further out. §16.1 fixes it.

---

## 3. The three tests any beat here must survive

1. **Does it stay on the body?** An explicit beat stays on the body for its whole length. Read the beat's
   last sentence: if it is about what the moment *means* rather than what is *happening*, it has pivoted and
   it scores zero. Interiority gets its own beat, after.
2. **Would it still be true on the twelfth visit?** Both new surfaces here are repeatable. A line that lands
   once and rots by the third read is a defect, not a flourish. Escalation is beats and rungs, never fatter
   paragraphs.
3. **Does anyone in it know what they are holding?** This is the release's whole argument. Grier does not
   know whose memory is in his drawer. Sabin does not know what he is studying. The Chairman is the only
   person in the story who knows exactly what he owns, and that is why he is the ending.

---

## 4. The cast

### New — **Sabin** (the scientist)

Hired four months ago. Not from this city. Mid-thirties, competent, quick, mildly bored, and **completely
amoral about who is paying.** He is not cruel and he is not a fanatic. He took an enormous retainer to solve
an interesting problem and he does not ask what it is for, because asking is not in the fee.

He was seeded in `design_book.md`'s Step-3 cast and never built: *"The Lab scientist (name TBC — seeded for
Act 2) — Vance's in-house roboticist who maintains and upgrades the assets… and **could recognize her build
— the thread to what she is.** Phase-1 role is light."* This release is that thread, and the name is now
**Sabin**.

**What makes him dangerous is not malice. It is competence.** He is the one man in the tower whose job is
noticing anomalies, and she is the largest anomaly in the building.

### New — **Grier** (the old machinist)

Nine years ago he was an assistant on the programme. Skilled hands — he dressed parts back by hand, which is
exactly what Kess read off the chip and could not source: *"Everything's cut a shade wide and then dressed
back by hand, which is what you do when you're making eleven of a thing and not eleven thousand… Nobody's
dressed a part by hand in this city for ten years."* (`cap_chip_read`.) Kess described this man without
knowing it.

He opened a memory to catalogue it and there was a child in it. He stole what was in the room he had keys to
— **all of Cain's, and one of hers** — and ran. He got Cain's to him in the dark, gave no name, and never
came back.

**It cost him everything.** No work: nobody hires the man who walked out of that programme. Nine years, a
room in the Reach, and a bottle. His hands shake now.

**And he hates Cain.** Not for anything Cain did — for what it cost. He burned his whole life for a man who
took what he needed and never once came back to see whether it had been worth it. The part he will never say
out loud is that he would do it again. That is why he drinks.

### Returning

- **Cain** — installs every piece. Refuses to explain. Cracks exactly once, at the end.
- **Kess** — unchanged this release. He priced the last one and he will price this one. No exposure.
- **Vane** — forges the credential. His second use, and better than the badge idea he was built for.
- **Sol, Colm** — **not** moved; both stay in the ruin and the ruin is written (§16.1). Colm gains a reason
  to still be there and a dead trade; no arc change to either.
- **The Chairman (Aldous Vance)** — **off-page.** A signature on Sabin's contract and, at the very end, a
  name in two other men's mouths. He does not appear.

---

## 5. THE SPLIT — the three pieces

**They did not cut her memory into three arbitrary chunks. They cut it by kind, so that no single stored
piece could ever wake anybody up.**

| # | What is in it | Who has it | Why they have it |
|---|---|---|---|
| **1** | **The childhood.** Who she was before any of this. | **Grier** | He stole it. It is what broke him. |
| **2** | **The making.** What was done to her — the lab, the years, the process. | **Sabin** | The Chairman gave it to him **to copy the method.** |
| **3** | **Cain.** Who she loved. | **The Chairman** | The leash. **NOT this release.** |

Feeling with no picture is a mood. A picture with no feeling is a room. A name on its own is just a name.
**It is a prison built out of filing** — you can hold any one part forever and never wake anyone.

**And it is why the split existed operationally:** three parts, three places, three sets of keys, so that no
one person could ever take all of her. Grier proved the design worked. He got away with a third of her and
that was the most anyone could have taken.

**⚠️ It is also why the Chairman kept part three.** He is not holding "the most important bit." He is
holding **who she loved.** He can let the rest of her be reassembled and still own the one thing that would
make it matter — and hand it over on the day he needs her pointed at Cain and needs it to stick. He is not
hiding it. He is waiting for her.

### The second gut-punch, and it is free

Piece two is **the record of her own construction**, and it is what Sabin has been given to study.

**He is sitting in a lab studying a memory of Wren being made, while Wren sits at the desk next door reading
files for him.** She walks past her own life every working day. Nothing has to be written to make that true;
it simply is, once the split is set.

---

## 6. The way in — the cover

### The building — THE RISE

**Locked 2026-08-26, LO's call.** Vance is still building it: twenty floors going up, eight of them working,
the rest bare concrete and cable.

**Where it stands.** The edge of the Reach, on cheap ground — **a short walk from Grier**, which is what turns
the chain in §8 into a walk instead of a commute. **From its upper floors the Spire is visible.** She looks at
the building that sealed her out, from the building that replaced it, every time she goes up. Say it once.
Never remark on it again.

**Why forged papers work here.** Nothing in it is finished, and that includes the security. They are hiring
fast and checking slow because Sabin needs readers now. That is the whole answer and it does not need a
second one.

**The three rooms.**

| id (working) | Name | Its job |
|---|---|---|
| `the_rise_floor` | **The Floor** | Open work floor, twenty hires at screens. Her day job (`work_the_archive`). Track B's suspicion meter climbs here. The consulted beat (§7). |
| `sabin_lab` | **Sabin's Lab** | Four floors up. Glass, over-lit, one bench, nobody else on the level. The ladder, the loop, the drain. |
| `the_dry_store` | **The Dry Store** | Samples signed in and out. Piece two is in here. The swap (§9) happens here. |

**The empty building pays for the silence.** §9 requires that she cannot make a sound in his lab. A tower with
nothing in it gives that a physical cause — sound carries in a building with nothing to stop it — instead of
leaving it an assertion the player has to accept.

**Rejected alternatives** (recorded so they do not regenerate): *The Annex*, a dead finance tower Vance bought
with the old company's name still cut over the door — its one advantage, closeness to Grier, was stolen by
siting The Rise on the Reach's edge. *The Works*, a purpose-built showroom whose ground floor demonstrates
units to buyers — cut because it spends **the units as scenery** and the units are on §17's reserved list.

### The three tokens

Three shipped cover items already exist (`cover_dockhand`, `cover_analyst`, `cover_stranger`), and beat_0116
split the *face* out of the clothing system entirely: `face_worn` is a flag toggled at `the_cot`, the
garment is an item. **Same shape here, no new engine work.**

**⚠️ THE COVER IS BOUGHT LATE, NOT FIRST.** Under the 2026-08-26 reorder (§8) the release opens on Grier,
who is in the Reach and needs nothing. She buys her way into The Rise only after piece one is in her hand and
Grier has named the place. **This is deliberate:** the spend gets a reason and a moment, and the release no
longer opens by asking the player for coin before anything has happened.

She needs three things, and **The Rise** will not open until she has all of them:

1. **A forged credential.** Vane makes it. Smart people are hired on papers and she has none.
2. **The face she already owns.** `face_worn`. The new tower has never seen it — this is the first time in
   the game the bought face is pointed at the thing it is actually good for.
3. **A new cover garment.** `cover_research` (working id), gating the tower's surfaces the way
   `cover_dockhand` gates `work_depot_haul` and `cover_analyst` gates `work_the_case`.

**⚠️ THE TOWER IS A NEW TOWER, NOT THE SPIRE.** This matters and it is the reason the release is possible:
the Spire's lock is *her face on every camera at the curb*, and a building that has never seen her face does
not carry that lock. **The Spire stays sealed.** Nothing in this release opens the ride up, the atrium, the
penthouse, `vance_securities` or `docs_vault`. Those are Act 3.

**⚠️ verify at build (claim 1 of 3):** a gate reading `clothing_item cover_research equipped` **AND**
`face_worn is_true` is a two-token gate on one surface. Both tokens are shipped and both are read
independently elsewhere (`activity_bar_work` reads `face_worn`; six gates read `cover_stranger`), but the
conjunction has not shipped. Prove it on the first tower surface before building the rest.

---

## 7. Hired for her mind

The job is real and she is good at it. Sabin needs help reading eleven years of archive and she is the
fastest reader he has ever employed.

**The beat this earns, and it should be small and never repeated:** he asks her what she thinks, and then
stops talking and waits.

She has no protocol for that. She has protocols for being ordered, used, dismissed, and inspected. There is
nothing in her for *being consulted*. She stands there. He waits. And then she answers, and she is right, and
he says so, and moves on, and it costs him nothing at all.

**Do not underline it.** One beat, flat, and the game never mentions it again.

---

## 8. GRIER — the ladder (Piece One)

### How she finds him — Cain tells her

**Locked 2026-08-26, LO's call. The chain of the whole release is CAIN → GRIER → SABIN, and every link is a
person's mouth, not a document.**

Cain knows exactly who Grier is, because **Grier is where Cain got his own memories back.** Nine years ago
that man walked out of the lab with Cain's memories and a third of hers, and Cain spent the nine years after
it finding him.

**Why Cain cannot go himself.** Helping Cain cost Grier everything, and Grier has spent nine years deciding
whose fault that was. He landed on Cain. He would give that man nothing, ever again, on any terms — which is
also why the ladder in this section runs on spite.

**And Cain does not tell her that up front.** He gives her the name and the district and lets her find out for
herself how the door opens. It is a small dishonesty and it is the first one he tells her. Do not underline
it; the player should notice it later, not now.

**What the reorder costs — and where it went.** The manufacture-record route dies, and with it the beat where
she is better at something than anyone else in the room. **That beat is not lost. It moves to Sabin**, where
§7 already stages it properly: he asks her what she thinks, and then stops talking and waits.

### The first meeting

She walks in wearing the face she bought in the Undertow — **no company kit, no forged papers, none of that
exists yet** — and **he clocks her in two seconds.** He is the one man in
this city who would — he had his hands inside things like her for years.

No threat. No fear. No interest in the face. He says it flat and bored and goes back to his drink:

> *"They're still making you, then."*

**He does not know she is the girl in the jar.** He never knew whose it was. He never saw her face nine years
ago and he does not see it now, because she is not wearing it.

### The ladder runs on spite, not desire

**He does not want her because she is beautiful. He wants her because she is one of them.** A company thing.
The exact category of object that took his life apart. Getting one of *those* on her knees in his room is the
only power he has had in nine years and he takes all of it.

Every rung is her accepting more of that. **He is rude the whole way up and it never turns into affection.**
That is the point, and it is the register: sour, mean, unhurried, and completely unimpressed.

### ⚠️ THE WALL — he cannot finish

**Nine years of drink.** The drain fires on an anal finish and most nights he cannot get there at all. She can
suck him, ride him, take him however he wants it, and fire nothing.

**So the shortcut is closed.** She cannot drain the answer out of him and walk away in one night. She has to
work him the long way, repeatedly, and the ladder's actual goal is **getting a ruined man to finish.**

When it finally fires, the drain gives her everything at once.

**⚠️ CLAIM 2 OF 3 — PROVED LIVE AT BEAT 4, 2026-08-26, AND THE PARAGRAPH BELOW WAS WRONG. AMENDED.**

The original text called a state-gated ass finish *"a **new shape**"* and offered two candidate
implementations to choose between. **It is not a new shape. `loop_mercer_finisher` already ships it**, and it
is the largest exit block in the game (`5_scenes.toml:7288`): one climax node, banded by `sex_finisher_type`,
whose anal exit forks on the story chain to a node that drains **nothing** (`.cold`), to three nodes where
she reaches and **gets nothing** (`.try1/2/3`), or to the drain (`.d0`/`.d1`).

Measured in the built game, same choice, one flag apart:

| state | the exit that renders | where it goes |
|---|---|---|
| `controller_off is_false` | *"Reach for it."* | `Canvas_mercer_drain_canvas_Node_cold` — **no drain** |
| `controller_off is_true` | *"Reach for it at the finish."* | `Canvas_mercer_drain_canvas_Node_d0` — **the drain lands** |

That is Grier's wall exactly, already built, already played, already carrying its own failed-night prose.
**Beat 5 copies `loop_mercer_finisher` and does not invent anything.** Candidate (b) — `show_when_locked`
plus `locked_text` — is dropped: it would hide the failure behind a greyed label instead of writing it.

### What she walks out with

The child. A small physical part in her hand — the shape of the chip on Kess's bench, *"smaller than a coin
and it does not look like anything."*

**He is glad to be rid of it.** He never learns what it was.

### And the name of the next place

**This is the second half of the same visit, not a second trip.** He is spent, she has the piece, and he has
nothing left to hold over her — so she asks one more question.

He is the one man who knows the work never stopped; it is the first thing he ever said to her —
*"They're still making you, then."* **He was in the room when they split her**, so he knows there were three
parts and he knows one was kept back for study. She asks where study happens now. He tells her: a half-built
tower on the edge of his own district, hiring readers.

**This is what buys the cover.** Only now does she have a door worth forging papers for, and only now does she
go to Vane.

### He survives

**Locked, LO's call.** He is alive at the end of the release and his loop stays open.

---

## 9. SABIN — the two tracks (Piece Two)

### Track A — the body

She works him the ordinary way and the ladder is the shipped one: portrait hub → rungs → first explicit →
triggerless loop → finisher → drain canvas.

**This is the release's main repeatable surface** and it must be live from the middle onward, not saved for
the end. Clean, over-lit, quiet, and she cannot make a sound up there — a completely different register from
Grier's room, and the contrast is the point.

**What the drain gets her:** he is four months in. He does not know what anything *means*. But he knows
**where everything is kept** — building, floor, shelf, reference. He wakes clean and remembers nothing, so
the loop stays open forever.

### Track B — the work

Her day job. Reading the archive is how she finds the **references** that tell her what to ask for.

**And it is the reading that exposes her, not the sex.** A second, independent meter climbs on the work
track: what Sabin suspects about her build. Same shape as `case_progress` on `work_the_case` — a trait bumped
by the work canvas, driving banded reveals.

**The two tracks never touch.** She can be fucking him in the lab and still be one careless answer away from
him working out what she is. Do not tangle them; the tension is that they run in parallel.

### Taking the piece

She cannot simply steal it. It is the sample his entire research rests on; the morning it is gone he knows
exactly what was taken and who has been in the room. **It is a swap or a con, not a robbery** — and it is the
one place in this release where her mind, not her body, does the work a second time.

---

## 10. THE MIDDLE — nothing happens, twice

She takes piece one to Cain. He seats it. **Nothing.**

She takes piece two to Cain. He seats it. **Nothing again.**

**This is deliberate and it is the release's spine.** Two anticlimaxes are what make the third landing mean
anything. But it needs one thing or the player reads it as a bug:

> **Something happens — just not to her. Cain does.**

- **First install:** he seats it, she feels nothing, he says nothing. Flat.
- **Second install:** he seats it, she feels nothing — **and he stops.** Two seconds too long. Does not look
  at her. Then carries on.

She does not know what she just saw. **The player does.**

**And the UI must move.** `canvas_chip_view` visibly fills — FRAGMENT 01 goes from `LOCKED` to a part-filled
state after each install. The store proves the work is landing even while she cannot feel it. Without this,
two dead installs read as a broken flag chain.

---

## 11. THE SCENE — the Tier-3 capstone

### Cain tells her what it takes

He has known since the first one. He said nothing because he was hoping he was wrong.

> *"They're both in you. They're not coming up because you never stop."*

### Why she cannot feel them

The one time a memory ever surfaced on its own was Glitch III, in Bastien's cell: *"She lies on her back and
stops doing anything at all, and listens to herself the way she listened to the door."* Stillness, captivity,
and nothing left of her.

**She has never once been fucked without working.** Always a cover on, a target in front of her, a weapon to
fire, something to get. In two acts she has never been in a bed without an objective.

**The memory only opens when there is nobody home.**

**⚠️ This is the answer to the obvious player objection** — *she has been fucked in every room of this game,
why has this not happened already* — and it must be **stated in Cain's mouth**, once, plainly, or the scene
reads as arbitrary.

### What he does

**He takes her somewhere and hands her over.** Strangers. No name, no cover, no plan, nothing to gain. Used
like an animal by men who want nothing from her and will not remember her.

**⚠️ NOT The House.** Rue's brothel is a place where she *works* and *earns* — she is an operator there, and
`underworld_brothel_loop` already ships the anonymous-john register. This scene needs somewhere she has never
been and will never go back to, and she is not told where it is. Preserving The House as a standing surface
is the second reason; the first is that the scene must be singular.

**⚠️ Cain leaves and comes back.** He does not watch. Staying makes him a spectator and makes the scene about
him; leaving makes it hers. And he comes back for her, which is the one thing he has already proven he does.

### She fails the first time

**This is the best beat in the release.** She cannot help it. She starts working the room out of pure reflex —
reads the man, finds the lever, angles for the finish, reaches for the weapon out of nine years of habit.
Two acts of climbing from *used* to *user* and her body will not let her stop.

**Nothing fires. She has to go back.**

### She chooses it

Second time she lets go, properly, and it fires.

**The whole game has been her climbing out of being used. The last step back to herself is going all the way
down one more time — on purpose, because she asked for it.** The first time it was done to her.

**This is the hottest and the hardest scene in the game and it carries the release.** Full crude, no fade, no
flinch. It is Tier-3 and once-only, so the prose can spend — but every beat stays on the body for its whole
length and the interiority gets its own beat, after.

---

## 12. WHAT SHE GETS — the name

Both pieces fire together. She gets **a childhood, and the theft of it, in the same moment.**

### The memory

**An ordinary afternoon. Nothing important. That is why it hurts.**

Late light on one side of her face. She is small. She has been given something to do with her hands and she
is doing it badly. Somebody behind her, watching, not correcting. **A hand comes to rest on the back of her
neck — not steering, just there. The thumb moves once along the seam.** No fear anywhere in her, and not the
permitted absence of fear — the other kind, the kind that is simply not there because nothing in the room
could hurt her.

This is the same memory that has been leaking all game: the warmth on the side of her face and the voice
with her name folded in it (opening night, Glitch I), *loved once, completely, by someone, before all of
this* (Glitch II), and the hand on her neck (Glitch III). **Four leaks, one memory, seen from different
angles.** The release joins them.

### ⚠️ AND THE VOICE SAYS HER NAME, AND IT IS NOT WREN

**This is the release's payoff and it is a large spend. It is deliberate.**

`design_book.md` has carried *"Fixed identity — not player-named (Wren / **buried Vesper**)"* since Step 2.
The game is named for a name nobody in it has ever said.

**She gets it back here.** Two pieces buys her a childhood and a name, and it does not buy her the person who
was in the room. That asymmetry is exactly right: **the release that gives her a self does not give her the
one she loved.** And it sharpens the Chairman — she has the name; he has the person.

**Handling rules:**
- It is said **once**, in the memory, in somebody else's voice.
- The game does **not** rename her. Every surface, every card, every portrait stays *Wren*. She does not
  start calling herself Vesper and neither does the narration. **She has a name she cannot use and does not
  yet know how to want.**
- Nobody else says it for the rest of the release. Not Cain, not Grier, not Sabin.

### And there is no face in it

No Cain. No name for who was glad to be looking at her. **That is piece three.**

---

## 13. THE ENDING

### She tells Cain

She is **pleased.** She got what she went through all of that for and she wants to tell him. She describes
the whole thing — the light, the hands, the neck, the name.

**And he is not in any of it.**

He listens to every word of it, and then it falls out of him — not as information, as a man being hurt out
loud:

> *"You don't remember me at all?"*

**First crack in Cain in the entire game.** He has held the *told-is-not-felt* line through two dead installs
and everything that happened in that room, and it goes in one question he did not mean to ask.

### She goes back to Grier

Not for a part. **She asks about the man he hates.**

And he has nine years of things to say — and one of them is the answer: **there was a third. He knew. He
could never get near it. It went up.**

### The last scene — she brings Cain

Nine years. The man he ruined himself for, standing in his room.

**Cain says almost nothing.** He does not do gratitude out loud and he is not going to start.

**Grier says everything** — including that he has been fucking her, and he watches Cain's face while he says
it. **(LO's call, locked.)** It is the only weapon he has and he has been sharpening it for nine years.

**No reconciliation.** He does not forgive him. He gives them the answer anyway, because he was a good man
once and this is the last of it he has got. Then he watches them leave and pours another one.

### The arithmetic

- **Cain knows who is in the third piece.**
- **Grier knows where it went.**

Neither could ever have worked it out alone and neither would ever have found the other. **She is the reason
they are in the same room.**

The answer lands not as a shock but as arithmetic: **the Chairman has the part with Cain in it, and he has
been waiting for her to come and get it.**

### Last beat

She now knows a man was in her life and was cut out of it, and that a stranger owns him.

And Cain is standing there in pieces over a question **she cannot even hold**, because she has no idea who he
is.

**The release ends on that silence.** Not a cliffhanger. A room where one person is hurt and the other
genuinely does not understand why.

---

## 14. Register & ceilings

**This is a porn game and this release carries two repeatable explicit surfaces plus a Tier-3 capstone.**

- **Default register:** RTS-flat, ~35–40 words per beat, flat across every tier. Escalate by adding beats,
  never by fattening paragraphs. Third person throughout; `narration_person = "third"` is immutable.
- **Crude is the default at the sexual register.** Real terms — cock, cunt, tits, ass, cum. Not euphemism,
  not "between your legs," not a fade. Writing under the ceiling is a defect.
- **Every explicit beat stays on the body for its whole length.** If the last sentence is about what the
  moment means rather than what is happening, the beat has pivoted. Interiority gets its own beat, after.

### Row (a) — Sabin's loop

**Full crude. Clean, quiet, controlled.** He is not cruel and he is not degrading her; the coldness is the
room, not the man. She cannot make noise up there and that constraint is the register — everything held down,
nothing said, hands over mouths, doors that do not lock. Oral / vaginal / anal on the shipped `sex_stage`
ladder, `loop_npc_pleasure` climbing, climax-elect at the threshold, the ass finish routing to the drain.

### Row (b) — Grier's loop

**Full crude, and the degradation is proprietary rather than jeering.** He is sour and mean and unhurried.
He is not performing contempt — he genuinely holds it. The room is filthy, he is often half-drunk, and
**most nights end without him finishing**, which is content, not a gap: the failed nights are written and
they are part of the ladder. She is never shown enjoying it. His room is work.

### Row (c) — the capstone

**The hardest scene in the game.** Anonymous, plural, nothing owed. The whole point is that she has no role
in it — no cover, no target, no angle, nothing to extract. **Full crude, no fade, no flinch.** Once-only, so
the prose can spend on beat count; the per-beat word target does not move.

**The failed attempt is written explicitly too.** Watching her run the operator's reflex — reading the man,
angling for the finish — inside a scene whose entire requirement is that she stop, is the release's best
writing opportunity and it must not be summarised.

---

## 15. What is standing when it is over

**Two new repeatable sex surfaces that feel nothing alike:**

- **Sabin's loop** — the tower, clean and quiet, plus the day job that feeds it. Repeatable, open forever.
- **Grier's loop** — the Reach, filthy and mean, with a wall in it that stays interesting after it is beaten.

Plus everything that survives from before: Renner, Mercer, Colm, Calloway, The House, the pit.

**This is the fix for three releases ending with nothing to do.** The last card must point at something the
player can still play.

---

## 16. Fixes owed — not optional

### 16.1 The burned bar — ✅ SHIPPED AT BEAT 1, AND THE FIX BELOW WAS WRONG

**The defect was real.** `hub_sol_undertow` and `hub_colm_undertow` carried no `raid_done` clause, so
post-raid Sol tended a bar with a hole in its wall for an owner who had been dragged out through it, and
Colm took her into a back room that had burned.

**The prescription was wrong, and LO killed it with one question: *if Bastien is kidnapped, how could Sol
run the bar?*** He cannot. Sol is staff, the owner is gone, and **nobody has the standing to reopen
anything.** The shipped game already said so at `3_activities.toml:2613`:

> *"The Undertow does not open in the evenings any more. Sol is in it most days with a shovel and a bucket
> and no particular plan, and he lets her past the tape because she is the only one of the staff who came
> back at all."*

**Sol is not running a bar. He is clearing one.** The original prescription — *"One new small room, Sol
reopens, Colm moves with him, schedules and hubs re-pointed"* — would have contradicted shipped prose to buy
a scene the release does not need.

**Two engine facts closed the other doors.** `[[npcs.schedules]]` carries **no `conditions` field**
(`engine-reference.md:483`), so an NPC cannot be here before the raid and elsewhere after it without two
permanently-live rows — and a second row parks that NPC's portrait badge on a nav card they are not standing
at, in every save, from the moment the destination unlocks. **Relocating anybody costs a lie.**

**What shipped instead: nobody moves, and the loss is written.**

- **`hub_sol_undertow`** — base node banded on `raid_done`. Pre-raid verbatim. Post-raid: dry taps, the
  counter under a sheet, a man moving burned timber from one side of the room to the other. His bio line
  finally cashes, and bitterly — he has outlasted this owner too, and it is the first time that has left him
  with nothing to do. **He gets a spoken line, which this node never had.**
- **`hub_colm_undertow`** — **three** new bands ahead of the four originals (adjacent groups are one
  if/elseif chain and first match wins, so the originals needed no edit; one of them is a **post-raid MEET
  band**, because reaching the raid without having found Colm is a reachable cold start). He does **not**
  relocate: he keeps turning up because **the bar is the only address anybody has for him, and a courier who
  cannot be found is a courier nobody hires.** That is his own careful-man logic, it costs no schedule row,
  and it tells no lie.
- **The raid ended his trade, not just his local.** Bastien was his principal. That is a free escalation
  nothing had spent: *"Man I carried for went out through that wall. Nobody's said his name since."*
- **The loop needed no relocation at all** — `loop_colm_backroom` is **triggerless**, so where they go is
  purely prose. Its intro is banded, and the entry choice is two era-gated siblings pointing at one node:
  *"Take him in the back."* becomes *"Take him through the tape."*

**⚠️ THE ONE THING THAT ALMOST BROKE.** `hub_sol_undertow.carrier` is the **only** setter of `colm_found`
in the game (`5_scenes.toml:9727`). Gating Sol's hub off post-raid — the obvious first move — would leave
any player who reached the raid without asking Sol about a carrier **permanently unable to find Colm.** The
release would have opened by deleting an arc. His asks are deliberately unbanded, and there is a live
cold-start test holding that.

**What we did NOT do:** no new location · the Undertow never reopens · **The House needs nothing** (Bastien
owned it too, but Rue fronts it and the raid never went near it) · the bathroom stays locked.

**Verified:** green build, both guards clean, **26/26 live** across both eras including the cold start.

### 16.2 The memory store

`canvas_chip_view` triggers at `cradle`, which is behind the Spire seal. **The UI this release fills is
currently unreachable.**

**Fix: move it to `the_cot`.** The canvas's own text supports it — *"She opens **the store the company gave
her** for what it calls recovered assets."* The store was never a thing in that room; it is in her. The
cradle was only where she was still enough to open it.

**And it buys a beat for free:** the first time she opens it somewhere that is not the cradle is the proof it
came with her. They stripped her floor, sealed the building, and never took the store, because it was never
in the building.

**⚠️ CLAIM 3 — TESTED 2026-08-26 AT BEAT 1, AND THE MOVE IS WRONG. AMENDED.**

`the_cot` is gated `berth_home is_true` (`1_metadata_and_locations.toml:1160`), an Act-2 flag. `cradle` is
reachable from the game's first hour. **So re-pointing the shipped canvas would delete the memory store from
the whole of Act 1** — the four leaks would still fire and the UI they point at would not exist yet. The move
is not a move.

**Amended shape: PAIR, do not move.**

- **`canvas_chip_view` stays at `cradle`, untouched.** It is Act 1's store, and post-raid the Spire seal
  retires it on its own. Its id is shipped and does not change.
- **`canvas_chip_view_cot` is a NEW canvas at `the_cot`**, gated `berth_home is_true`, carrying the bands.

**This is better than the move, not a consolation.** The free beat §16.2 wanted — *the first time she opens it
somewhere that is not the cradle is the proof it came with her* — only works if there were an earlier place,
and the pairing is what preserves it. Adding a canvas is save-safe; re-pointing a shipped trigger is the kind
of change a carried save can land on the wrong side of.

**The bands** run on one hidden counter, `pieces_seated` (0–3), rather than the two separate flags the ledger
first sketched — one source of truth for a number three beats read:

| band | when | what it says |
|---|---|---|
| A0 | `pieces_seated lt 1` **AND** `store_carried_seen is_false` | They sealed the building and never took this, because it was never in the building. **One-shot** — the realisation gets a flag, or it rots by the third read (§3 test 2). |
| A1 | `pieces_seated lt 1` **AND** `store_carried_seen is_true` | The routine line. Empty, FRAGMENT 01 greyed, and she opens it more often than any task log would justify. |
| B | `pieces_seated eq 1` | The slot is **lit**. The data is intact and reading it does nothing at all. |
| C | `pieces_seated gte 2` | Two lit. The second has no label, because nobody gave her a night quiet enough to write one. |

**Bands B and C are what make §10 survivable.** Two installs that change nothing read as a bug unless the
player can *see* the store fill. The fiction stays cold; the UI does the confirming.

**⚠️ The third slot is NOT shown here.** She learns a third piece exists at beat 17, from Grier. A store that
displays an empty third slot at install two spoils the ending two beats early.

---

## 17. Reserved — do NOT spend

**The Chairman on screen** · **the Spire** (the ride up, the atrium, the penthouse, `vance_securities`,
`docs_vault` — `vault_cleared` stays never-set) · **what Cain was to her** · **`the_site`** · **the other
names on her index** · **the units as individuals** · **why the drain has never worked on Mercer** (still
unspent after LO rejected the Mercer piece — it is still owed a payoff and it is not this one) ·
**Bastien's survival** (§18.4).

---

## 18. Decisions taken this conversation

### 18.1 Names — **Sabin** and **Grier**

House style is bare, clipped surnames (Mercer, Renner, Calloway, Kess, Sol, Colm, Rue, Vane, Marsh, Cain).
**Sabin** reads as an outsider who came for the money and sits beside the corporate names without becoming
one. **Grier** sits beside Kess in the Reach and carries the wear without being cute about it.

### 18.2 Marrow stays the sole author

`design_book.md`'s locked backstory is that Marrow built Cain first and then built her second, **as a
companion for Cain** — which is the entire reason the game ends in kill-or-love. LO's *many scientists*
refinement is kept and reconciled: **Marrow led it and authored the method; many hands worked under him.**
The team that failed on Cain before Marrow cracked it was one of those hands, and Grier assisted them before
moving to the team that built her. **One author, many hands.** The kill-or-love link survives untouched.

**Grier was present for the extraction** — LO's own settled sequence — and ran immediately after. The earlier
"already gone before Wren" sketch does not work, because he could not otherwise have stolen her piece, and it
is superseded here.

### 18.3 The childhood memory — an ordinary afternoon, and the name

Settled at §12. **Nothing dramatic in it.** The spend is the name, and the name is **Vesper**, said once, in
somebody else's voice, and never used again in this release.

### 18.4 Bastien — **next release, one line here**

He is alive and held, and *The Face* §10 reserved exactly one quiet detail for it: **no body was ever found
in the wreckage.** This release is already larger than *The Face*, and Bastien alive is a whole thread — where
he is held, who has him, what she does about it.

**Decision: he does not land here.** Instead the reserved detail gets said **once**, in passing, in somebody
else's mouth — Sol's or Colm's, in the moved bar — and is never underlined. The promise stays alive, the
scope stays sane, and it is written down here so it cannot be quietly lost.

### 18.5 Also settled

- **The capstone does not happen at The House** (§11).
- **Cain leaves and comes back** (§11).
- **She fails the first attempt** (§11).
- **Grier never softens** — civil by the end, never warm (§13).
- **Grier tells Cain he has been fucking her** (§13).
- **Grier survives** (§8).

### 18.6 The chain is CAIN → GRIER → SABIN — added 2026-08-26

LO's call, and it reorders the release. Cain names Grier; Grier names The Rise. **Every link is a person's
mouth, not a document** (§8). Three things follow:

1. **Grier moves to the front.** He is in the Reach and costs nothing to reach.
2. **The cover is bought at beat 7, not beat 3** — after piece one, once there is a door worth forging papers
   for. The release stops opening with a bill.
3. **The manufacture-record route dies**, and the beat it carried moves to Sabin (§7).

It is also nearly forced by the backstory already locked: **Cain recovered his own memories from Grier**, so
he knows the man precisely — and Grier hates him for what helping him cost, which is why Cain sends her
instead of going.

### 18.7 The tower is THE RISE — added 2026-08-26

Half-built, on the edge of the Reach, the Spire visible from its upper floors. Three rooms — **The Floor**,
**Sabin's Lab**, **The Dry Store** (§6). Chosen over two alternatives, both recorded in §6 as closed. The
deciding reason: **an unfinished tower pays for the silence rule §9 already required**, and its three rooms
are exactly the release's three jobs with nothing spare.

---

## 19. BLUEPRINT — the gated, placed, lane-tagged build order

**Reordered 2026-08-26 to CAIN → GRIER → SABIN (§8).** Grier is in the Reach and costs nothing to reach, so
the release opens on him; the cover is bought at beat 7, once he has named The Rise.

Each row = one turn: build + targeted live suite + ledger entry. Full suite once at the end.
Gate keys are **working names** — they become real at beat 1 and are immutable after ship.

| # | Beat | Lane | Where | Gate | What she wants |
|---|---|---|---|---|---|
| 1 | **Systems + fixes** ✅ | — | — | — | *(structure only — no scene)* |
| 2 | **Cain opens the release** ✅ | 4 · auto-fire one-shot ×2 | `the_cot` **→** `cain_lab` | `lab_seen` | To be told what she is |
| 3 | **Grier — found** ✅ | 4 · npc-intro + 1 · hub + guard | `grier_room` (nav-invisible) | `cain_named_grier` | The man who touched her memory |
| 4 | **Grier — the ladder** ✅ | 1 · portrait hub + rungs | Grier's room | `relation` bands 6 / 12 / 20 → sets `grier_opened_up` | To be worth using |
| 5 | **Grier — the wall breaks · PIECE ONE · he names The Rise** ✅ | 1 · loop → finisher → 4 · drain → 4 · auto-fire | Grier's room | `grier_opened_up` · `grier_nights gte 3` | To make a ruined man finish |
| 6 | **Install one — nothing** ✅ | 4 · auto-fire one-shot ×2 | `the_cot` **→** `cain_lab` | `piece_one_held` + `pieces_seated lt 1` | To feel it land |
| 7 | **The way in** ✅ | 3 · solo | `underworld_market` — the row, not Vane | `rise_named` + `cover_research not_owned` | A door |
| 8 | **Hired** ✅ — *the floor only; the other two rooms ship with the beats that open them* | 4 · npc-intro + 3 · day job + 3 bounces | `the_rise_floor` | `cover_research` equipped **+** `face_worn` | To be inside |
| 9 | **Sabin — the ladder** ✅ — *plus §7's consulted beat, which is the door* | 4 · one-shot + 1 · portrait hub + rungs | `the_rise_floor` **→** `sabin_lab` | `archive_worked` → `sabin_consulted` → `relation` bands 6 / 12 / 20 → sets `sabin_opened_up` | Reach into the store |
| 10 | **Sabin — the loop + the drain** ✅ — *plus §9's Track B, the suspicion meter* | 1 · triggerless loop → 4 · drain · 3 · banded work ladder | `sabin_lab` · `the_rise_floor` | `sabin_opened_up` → the ass finish → `sabin_drains_done` | Where it is kept |
| 11 | **PIECE TWO — the swap** ✅ — *plus §21 open items 2 and 3, both closed* | 3 · solo ×3 + 4 · one-shot | `kess_berth` **→** `the_dry_store` | `sabin_drains_done gte 1` → `decoy_made` → sets `piece_two_held` | The piece, without him knowing |
| 12 | **Install two — and Cain stops** ✅ | 4 · auto-fire one-shot ×2 | `the_cot` **→** `cain_lab` | `piece_two_held` + `pieces_seated lt 2` | To feel it land |
| 13 | **Cain names the price** ✅ — *and it happens at the COT, not the lab; see below* | 4 · auto-fire one-shot | `the_cot` | `pieces_seated gte 2` → sets `price_named` | To know why nothing comes |
| 14 | **The capstone — the failure** ✅ — *open item 1 closed* | 3 · solo on-ramp + 4 · one-shot | `the_cot` **→** `room_no_name` | `price_named` → sets `capstone_failed` | To stop working |
| 15 | **The capstone — the fire · THE NAME** ✅ | 4 · Tier-3, 20 beats | `room_no_name` | `capstone_failed` → sets `vesper_named` | To let go on purpose |
| 16 | **The question** ✅ — *at the cot; §19 row 16 corrected, see below* | 4 · auto-fire one-shot | `the_cot` | `vesper_named` → sets `cain_absent_confirmed` | To give it back to him |
| 17 | **Back to Grier** ✅ | 1 · rung on the standing hub | Grier's room | `cain_absent_confirmed` → sets `third_located` | The third piece |
| 18 | **The two men** ✅ — *one NPC present, one scheduleless speaker* | 3 · solo on-ramp + 4 · one-shot | `the_cot` **→** Grier's room | `third_located` → sets `two_men_done` | *(nothing — she watches)* |
| 19 | **After** ✅ — *the boundary MOVED; §18.4 spent; two dev jumps* | — | whole game | — | *(quests · boundary card · Bastien line · both loops open)* |
| 20 | **Media pass** | — | — | — | *(pools on everything repeatable)* |
| 21 | **Clean ship** | — | — | — | *(ship-gate · save-safety diff · one build)* |

### ⚠️ Two things beat 1 was told to build and correctly did not

**Recorded 2026-08-26, at beat 1, from reading the build.**

**1 — The Rise's three locations belong to beat 8, not beat 1.** `the_waterfront` is the Reach's street hub
and travel anchor (`1_metadata_and_locations.toml:893`) and it is **reachable in Act 1**. A locked location
still renders a **greyed nav card carrying its `blocked_message`**, so declaring The Rise early parks a
greyed *"The Rise"* on the Waterfront grid from the game's first hour — the shape `beat_0120` deleted from
the Undertow, and the shape `activity_sift_the_ruin` was built as a card to avoid. It also breaks the
whole-amendment rule: a location ships with **the beat that opens it**. The frontier telegraph is already
designed and is better than a card — **Grier names the place at beat 5**.

**2 — The ladder counters must not be named until the beats that decide them.** Vesper is shipped and a
trait key is **immutable** (`save-safety.md` §2). Colm's ladder runs on plain `relation` with no counter at
all, so whether Grier needs `grier_rung` is a **beat 4** decision, and whether Sabin's two tracks want one
trait or two is **beats 9–10**. `pieces_seated` was declared at beat 1 only because its axis was already
decided — three surfaces read it. Each counter is declared in `[player.core_traits]` **and**
`[[traits.labels]]` when its beat arrives; core_traits is what carries it into old saves.

*(Flags need no declaration at all in this game — there is no `[[flags.labels]]` block, and the engine's
flag-setter check inspects only `stage_helpers` and warns rather than errors.)*

---

### ⚠️ SHE CANNOT GO BACK TO THE LAB — found at beat 2, and it built a route the release reuses

**Recorded 2026-08-26.** §19 said beat 2 sat at `cain_lab` and the ledger said *"she goes back."* The
shipped game forbids it in `cap_the_lab`'s own first line (`5_scenes.toml:13424`):

> *"She does not know where it is. Twenty minutes with her head down and two changes of direction, and then
> a door, and then this."*

`cain_lab` has **no `entry_from`** and `auto_exit = false` — there is no route and there never was.

**So he comes and gets her**, which is already the relationship: he found her in a cell, and Bastien
supplied him for eleven years without ever having an address.

**And that makes the pickup a REUSABLE ROUTE, not a one-off.** Beats 6 and 12 are both *"Cain seats the
piece"* and both need her in that room, and she still will not know where it is. The shape is:

`cain_comes_for_her` (auto-fire @`the_cot`) → exits into `cain_lab` → `cap_cain_opens` (auto-fire there,
gated on the flag the pickup set) → exits to `underworld_strip`.

**Beats 6 and 12 reuse it with their own gates.** Cain always comes to her; she never finds him. That is now
a rule of the release, and it costs nothing because the last release already built the way out —
`cain_lab_offhours` (`beat_0114`, repeatable, **priority 1**, gated `lab_seen`), whose own header predicted
this beat: *"the next release opens on that scene and will likely add a way back."* Priority 1 is exactly
why a new canvas at 11 wins the auto-fire and the guard catches her afterwards.

**Where he finds her: `the_cot`.** The last chapter gave her *"the first place in her life that nobody
signed for"* and the first thing this chapter does is prove it is not private either. That transgression is
what earns her refusal.

---

### ⚠️ A LOCKED ROOM ALWAYS SHOWS A GREYED CARD — so Grier's room is not a map location

**Recorded 2026-08-26 at beat 3.** `_render_location_nav_card` emits
`<<if navDestUnlocked>>open<<else>>locked_card<</if>>` (`v2.py:19829`) and **there is no hide path.** A
location with `entry_from` renders a card in every save from the moment its parent is reachable.
`the_waterfront` is reachable in Act 1, so a normal locked room would have parked a greyed *"Grier's Room"*
on the Reach grid for two acts — the shape `beat_0120` deleted from the Undertow, and the reason
`activity_sift_the_ruin` was built as a card rather than a location.

**So Grier's room reuses the route beat 2 built:** nav-invisible (`auto_exit = false`, no `entry_from`) ·
`activity_go_to_grier` at `the_waterfront` is the door, gated `cain_named_grier` · `grier_room_offhours`
(priority 1) is the way out. **This is the same pattern as `cain_lab`, now used twice — and it is what
The Rise should use at beat 8 too**, for exactly the same reason.

**Two bands on the door card** — the finding (once; Cain gave a name and a district, never an address) and
the walk (every time after). It answers *how did she get there* without spending a beat on a fetch quest.

**The intro ends with her thrown out, and that is the design.** He does not know what he is holding, so
there is nothing to buy and no trade to offer. She asks one straight question, it costs her the afternoon,
and the closing thought names the only route left. **Without that beat, beat 4's ladder reads as grind with
no stated reason.**

**The off-hours guard is not tidiness.** `grier_room` is nav-invisible, so its passage carries an empty
navigation div and the portrait hub is the only way out — and the hub stops rendering when he is out of
window. Sitting with him at 23:30 costs 60 minutes and seals her in at 00:30. That is `bastien_backroom`'s
`beat_0114` soft-lock, one room over.

---

### ⚠️ THE LADDER'S AXIS IS PLAIN `relation`, AND NO NEW TRAIT KEY SHIPPED — decided at beat 4, from the build

**Recorded 2026-08-26.** §19 carried `grier_rung` as a working name and beat 1 correctly refused to declare
it. Reading the build says **do not declare it at all**, and the deciding evidence is a grep, not a taste:

- **It is the shipped ladder shape.** `hub_colm_undertow` (`5_scenes.toml:9789`) runs its whole ladder on
  bare `relation` — talk +2 / drink +3 / kiss at `gte 12` / the back room at `gte 24` — and **retired** its
  own `colm_drinks` / `colm_kisses` counters to do it (`1_metadata:104`).
- **`relation` in this game is access, not affection.** `1_metadata:114` reads it as *"trust/access"*.
- **⚠️ AND IT CANNOT PRINT A WARM WORD ANYWHERE.** That was the one real argument for a separate key and it
  does not survive the code. `setup.interpretNpcState` (`v2.py:6294`) builds a `relationship_summary` only
  from traits present in `story_arc.emotion_mappings`; Vesper's built map holds exactly **one** key,
  `affection`, which no NPC in this game has. So `trait_interpretations` returns empty, the summary is `""`,
  and the journal's `<<if _state.relationship_summary>>` (`v2.py:19404`) renders nothing. A climbing number
  on Grier has no surface on which to read as him warming to her.
- **`bar_rung`'s argument does not transfer.** It exists because *"a chain wants one axis to compare"*
  (`0_systems_spec:431`). The chain's axis here is already `relation`.

**Beat 4 therefore ships ZERO new immutable keys against a live game** — one flag, `grier_opened_up`, and
nothing else. **The wall's counter is a different fact** — how many nights he was worked and did not finish
is not how far up the ladder she is — and it is **beat 5's to declare, in the beat that bumps it.**

**The same question is still open for Sabin** (beats 9–10) and the same test applies: name a counter only
when the chain cannot be expressed on an axis that already exists.

### ⚠️ A CASCADE ALWAYS EATS ITS FIRST BEAT'S LABEL, AND FOLDING THE BEAT AWAY DOES NOT HELP

**Found at beat 4 by measuring, after the suite disagreed with the count in the plan.**

A cascade renders its **first beat's blocks with the node lead** and **drops that beat's `advance_text`** —
the first link on the page carries beat **one**'s label. So `visible clicks = beats − 1`, which was already
known, but the consequence was not: **beat 0's `advance_text` is never seen by any player.**

The obvious tidy — fold beat 0's blocks into the node lead and delete the beat — **makes it worse.** The
engine simply promotes the next beat into the same position: the lead swallowed a second beat, the node
opened on two beats of explicit content before the player had clicked anything, and a *different* label went
dark. Reverted.

**Author beat 0 knowing its label is decorative.** Do not spend a good line on it and do not try to remove it.

### ⚠️ THE WALL HAD TO BE TOTAL, AND THAT BROKE A SHIPPED CONTRACT — built at beat 5

**Recorded 2026-08-26.** Every other loop in this game ships the same rule: a facial or a finish inside works
normally and **only the ass finish drains**. Grier cannot use it. §8 says in its own words that she can suck
him, ride him, take him however he wants it *and fire nothing* — so a facial that worked while the ass finish
did not would be a wall the player can disprove on night one, with a green build.

**So `loop_grier_finisher`'s first band catches every `sex_finisher_type` while `grier_nights lt 3`.** Below
the break nothing finishes at all and the type she elected only decides which way it failed; above it the
shipped three-way contract resumes exactly. It is the only loop in the game that does this and the header
says why, so a later reader does not "fix" it back.

### ⚠️ THE THREE FAILED NIGHTS ARE THE EXPOSITION, NOT A TAX IN FRONT OF IT

`wall1` he blames the bottle and will not look at her. `wall2` he says what he used to have his hands inside
for eleven years — **and that he blames nobody but himself for the drink**, which is the grievance in §8
surfacing sideways without naming Cain. `wall3` he says he has had *"one of you open on a table with the
whole of it laid out in trays"* and does not notice he has said it.

**That is why the grind is worth having.** Each attempt buys a piece of the backstory that no other surface
in the release delivers, so a player who does the work is paid in story rather than in a counter.

### ⚠️ WHY THE FORWARD FLAGS GET THEIR OWN LOCATED CANVAS — and a correction to how I have stated this

`colm_drain_canvas`'s header calls it a rule — *"no flag on a triggerless canvas"* — and I have been
repeating it as a **build gate**. It is not one. I looked: the flag-setter coverage check
(`template_import.py:5159`) inspects only `stage_helpers` and **warns**, and the hard-fail variant (`:4931`)
needs a `4_story_arc.toml`, which this game does not have.

**The real reason is runtime.** `setup.computeHintGoal` resolves a flag by looking up **the canvas that sets
it** (`template_import.py:1044`, `:6198`), so a flag whose only setter is triggerless has nowhere to point a
player. Hence: `grier_nights` and `grier_drains_done` are **traits** on the triggerless finisher, and
`piece_one_held` / `rise_named` are set by **`cap_grier_gives`**, a located Lane-4 auto-fire in `grier_room`
that `grier_drain_canvas.d0` walks her into at **zero minutes** — the third use of beat 2's port-in route,
and the thing that makes §8's *"second half of the same visit, not a second trip"* literally true.

**The fiction is better for it, which is the tell that the constraint was right.** The drain tells her he has
it; he still has to open the drawer and put it in her hand.

### ⚠️ EXIT EFFECTS FIRE ON RENDER, NOT ON CLICK — measured at beat 6

`template_import.py:1968` is the documented rule and the build agrees with it: `pieces_seated` was already
**1** while she was still standing in the frame, before the player had clicked *"Out."*

**Harmless here** — the canvas is one-shot, the store it lights is three districts away, and there is no
other way out of that room. **Not harmless in general:** never put an exit effect on a **repeatable** node
whose own gate reads the value it writes, or the node re-scores itself while the player is still on it. Put
that kind of bump on a **choice**, which fires on click.

### The two anticlimaxes — what beat 6 established and what beat 12 must not repeat

§10 asks for two dead installs and one reaction. **Beat 6 spends nothing.** Cain is not surprised, not
disappointed, offers no reason and no reassurance, and his only answer is true and empty — *"It is supposed
to be in there. It is in there."* The narrator does not console the player either; the closing thought is a
flat refusal to feel cheated, not a summary of the disappointment.

**That leaves beat 12 the entire reaction** — the two seconds too long, the not-looking-at-her — and it only
reads if nothing here has softened the first one. **A later edit that has Cain explain why she feels nothing
kills beat 13**, where he finally does.

**And the UI carries the proof, exactly as §16.2 planned.** `canvas_chip_view_cot` band B was built at beat 1
and has been waiting since; the install's only mechanical job beyond the scene is `pieces_seated` 0 → 1.
Card Z then sends the player to look at it, because a UI that moves and is never opened has not moved.

### ⚠️ VANE IS NOT THE ONE SELLING IT — §6 corrected at beat 7

§6 says *"A forged credential. **Vane makes it.**"* The shipped game says where Vane went. The last thing he
says to her, at the end of *The Leash* (`5_scenes.toml:10508`), is:

> *"I'm gone tonight. The Reach, then further. You should be too."*

He is a fugitive with one marketable skill, and restaging him is a **full NPC amendment** — location,
schedule, on-ramp — which does not fit a beat budgeted as a Lane-3 solo, and which would open a thread this
release has no room to close (§20).

**So the seller is the woman at the far end of the row — the one who made her face** — and **Vane's hand is
named once, in her mouth, and never underlined**: *"There is a man down here now who came out of the towers
last winter with nothing on him but what he knew about paper."* Wren does not ask. The name is never
printed. That is exactly the discipline §18.4 sets for the Bastien line, applied to a second thread.

**Vane properly restaged is good material for the release after this one.** It is written down here so it
cannot be quietly lost.

### ⚠️ A QUEST CARD CANNOT READ THE WARDROBE — found at beat 7

`setup.checkQuestsCondition` handles **`flag` and `trait` only**. There is no clothing clause in a card's
`when`, so the Quests page cannot ask whether she owns the kit and would have gone on telling her to buy
papers she was already carrying.

**That is the entire reason `papers_bought` exists**, and the header says so in the file: it is a
**display-only** flag. The card reads it; nothing in the world does.

### ⚠️ AND THE GRANT GATES ON OWNERSHIP, WHICH IS BETTER THAN THE SHAPE §19 POINTED AT

§19 said to copy `activity_buy_face` — repeatable screen, so an unaffordable visit cannot kill the card.
Half of that shape is right and half is not. `activity_buy_face` is repeatable **but its trigger gates on
`face_bought is_false`**, so the card does vanish the moment the flag is set. That was survivable only
because the face shipped in the same release as its gate.

`cover_research` does not get that luxury — it is a **progression gate in a live game**, the exact
0.1.5.1 class. So the trigger reads **`clothing_item cover_research not_owned`**. It cannot burn: if the kit
is ever missing, for any reason, the card is simply back at the stall.

**Proved live**: the suite deletes the item from a save that still has the flag set — the shape that
soft-locked 0.1.4 → 0.1.5 — and the card comes back and re-grants. Beat 8 still owes the second half of §5:
an idempotent `wardrobeEffects add` on the point-of-need reaction at the tower.

### ⚠️ A REPEATABLE CANVAS CAN NEVER AUTO-FIRE — measured at beat 8

`selectAutoFireCanvasForLocation` opens with **`if (c.isRepeatable) continue;`** (`v2.py:4471`). Priority is
irrelevant: a repeatable canvas renders as a **card** on the location page and the player clicks it. Only
one-shots auto-fire, and the highest-priority eligible one wins.

I designed The Rise's three bounces as high-priority auto-fires so the save-safety heal would land the
instant a stranded player set foot on the floor. **It cannot work that way** — and it does not need to:
save-safety §5's own worked example, `react_calloway_precover`, is `is_repeatable = true` for exactly this
reason. The priority still earns its keep by ordering the cards above the day job and the stairs.

### ⚠️ THE HEAL HAD TO SPLIT ON `papers_bought`, OR THE PURCHASE WAS SKIPPABLE

`unequipped` is **true for an item she does not own** (`v2.py:4033`) — the evaluator tests membership of
`player.equipped` and nothing else. That ambiguity is what save-safety names as the thing that made 0.1.5
undiagnosable, and a single healing bounce would have inherited it in the worst direction: **a player who
had never been near the market would have been handed `cover_research` free**, because the road up is gated
on `rise_named` alone. Sixty coin you can skip by walking into a lobby is not a price.

So there are two kit bounces, split on `papers_bought`: the unpaid one turns her around and points at the
row, the paid one carries the idempotent `wardrobeEffects add`. **Both cases are asserted live** — the
unpaid player leaves with nothing, the stranded player leaves healed, and a second pass is a silent no-op.

### The Rise ships ONE room, not three

§19 row 8 says the building is built here and §6 lists three rooms. **Only `the_rise_floor` opens in this
beat.** `sabin_lab` ships with the ladder and `the_dry_store` with the swap, because that is the rule beat 1
derived when it moved the whole building out of the release's opening: **a location ships with the beat that
opens it.** Shipping all three now parks two greyed cards carrying `blocked_message`s that promise content
one and three beats away.

**And the frontier telegraph is better than the cards would have been.** Sabin names both rooms himself, in
the interview, as places she is not to go — *"You do not come up to the lab. You do not sign anything out of
the dry store."* — and the closing thought is that it has not crossed his mind this is information. Same
move as Grier naming The Rise instead of a nav card doing it.

### One honest deviation from the npc-intro contract, at step 1

The contract wants the name planted upstream. **Nobody upstream knows it** — Grier named the building and
said *"whoever is up there"*, which is all he has. So the upstream plant is the **role and the place**, and
the name lands in the first paragraph, which is step 4 doing step 1's job. Every other step is followed
exactly.

### ⚠️ `requires_npc` DOES NOT GATE AN AUTO-FIRE CANVAS — measured at beat 9, and it is not only this beat's

**Recorded 2026-08-26.** `cap_sabin_consults` was authored with `requires_npc = "npc_sabin"`, the shape every
one-shot in this release uses. It fired anyway with him four floors up.

**Measured, not read.** With Sabin at `sabin_lab` at 13:00,
`setup.selectAutoFireCanvasForLocation("the_rise_floor")` returned `cap_sabin_consults`.

**Why.** `requiresNpc` is present in the built canvas record and is enforced in exactly **two** places, and
neither is the auto-fire path:

- `setup.checkRandomEncounters` (`index.html:2933`) — the Lane-2 random-ambient selector.
- the Lane-3 substitution picker (`:3006`).

The auto-fire path is `selectAutoFireCanvasForLocation` (`:2104`) → `setup.isCanvasValid` (`:2224`), which
checks **schedules, conditions and repeatability** and never looks at `requiresNpc`.

**The fix is one line, and it is already house style.** A presence *condition* — which `isCanvasValid` does
evaluate — on the trigger:

```toml
{ type = "npc_at_location", location_id = "<loc>", npc_id = "<npc>", operator = "is_present" },
```

`requires_npc` stays as well: the render-bucket guard reads it, and so does anybody reading the file.

**⚠️ AND THREE CANVASES IN THIS RELEASE ARE STILL WRONG.** Of the 17 non-repeatable canvases in the game that
lean on `requires_npc`, **nine already carry the explicit clause** (all of Kess's and Mercer's — so this was
learned once before and not written down), and **eight do not.** Probed live:

| canvas | probe | result |
|---|---|---|
| `cap_grier_met` @`grier_room` | 03:00, Grier absent | **fires** |
| `cap_grier_gives` @`grier_room` | 03:00, Grier absent | **fires** |
| `cap_sabin_hires` @`the_rise_floor` | 16:00, Sabin in the lab | **fires** |
| `cap_sabin_consults` @`the_rise_floor` | 16:00, Sabin in the lab | fixed at beat 9 — does not fire |

All three are reachable: `activity_go_to_grier` and the Rise travel choice are both ungated on time. The
remaining five are older shipped content (`cap_first_penthouse_service`, four Renner canvases) and are
**not** this release's to touch. **This is open item 5 — LO's call, because it re-opens three validated beats.**

### ⚠️ THE END OF A SCHEDULE SLOT IS EXCLUSIVE — which is what makes two rows on one NPC safe

**Recorded 2026-08-26 at beat 9.** Sabin now has two rows: `the_rise_floor` 08:00–11:00 and `sabin_lab`
11:00–22:00. `setup.isCurrentTimeSlot` returns `currentTotal >= startTotal && currentTotal < endTotal`
(`v2.py:3820`), so the first row covers 08:00–10:59 and the second picks him up at 11:00 sharp. There is no
minute where `getNpcLocation`'s **first-match-wins** walk (`v2.py:3463`) has two rows to choose between, and
no minute where he is nowhere. Asserted live at 07:59 / 08:00 / 10:59 / 11:00 / 21:59 / 22:00.

**Write adjacent windows end-to-start, never with an overlapping minute.** An overlap is not an error the
build catches — it silently resolves to whichever row was declared first.

### ⚠️ AN AUTO-FIRE ONE-SHOT NEEDS A "SHE HAS DONE THE THING" GATE, not just a "she has met him" gate

**Recorded 2026-08-26 at beat 9.** §7's beat is a man asking a reader **he has been reading** what she
thinks. `cap_sabin_hires` exits into `the_rise_floor` at +30 minutes, still inside his 08:00–11:00 window,
and the auto-fire selector re-runs on arrival — so gated on `sabin_met` alone, the interview and the consult
would have landed back to back in one morning, and §7's beat would have been about a stranger.

`archive_worked`, set by `work_the_archive`'s exit, is what puts a worked shift between them. **Any time two
one-shots share a location and a window, the second one needs a gate the first one cannot satisfy on its
way out.**

### The consulted beat is the door, and that is why it is not decoration

**Built at beat 9.** §7 asks for something *"small and never repeated"* and warns *"do not underline it."*
Shipped as: he asks what she would **do** with a run of the archive; **she waits for the rest of the question
and there is no rest of it**; she answers; she is right; he says so once and moves on — *"and it has cost him
nothing at all to have asked her"* — and in the same breath he moves her off the floor.

**The underline is what is absent.** There is no paragraph anywhere in the scene explaining that nobody has
ever asked her opinion. The suite asserts six phrasings of that sentence are **not** in the built text. The
one `thought_bubble` is about **the four seconds she spent not answering**, because a pause is a thing people
notice — her operator's reflex, intact.

**And the door it opens is a staffing decision.** He is reallocating a resource he has just measured. If it
read as a reward or as a pass, the beat would be about him.

### ⚠️ THE LADDER'S AXIS IS PLAIN `relation` FOR SABIN TOO — the body track decided at beat 9

**Recorded 2026-08-26.** §19's note left the two tracks open for beats 9–10. The body track is **plain
`relation` on `npc_sabin`**, no counter, for beat 4's reasons plus one that is specific to him: **with Sabin,
access is literal.** What climbs is how far into his building she is allowed to stand — the ladder and the
meter are the same fact, which is the one condition under which a bare `relation` ladder is honest.

**The work track's key is still undeclared** and belongs to beat_0131 with the suspicion meter.
`work_the_archive` was written at beat 8 so a band could be added to it without moving it.

### The two ladders share the arithmetic and differ in register — on purpose

Sabin's rungs are 0 / 6 / 12 / 20 and pay +2 / +3 / +4 / +4, exactly Grier's. **A player who learned that
rhythm one NPC ago should not be re-taught it**, and the difference the release is actually claiming (§15 —
two repeatable surfaces that feel nothing alike) is carried by what happens on the rungs, not by the numbers.

Two things did have to change:

- **Rung 3 is a kiss, and she starts it.** Grier's ladder was body-inspection the whole way up because he is
  a machinist reading build quality off a part. Repeating that shape would have made two ladders read as one
  ladder written twice.
- **Every rung exits to `the_waterfront`, out of the building.** Exiting to `the_rise_floor` would have left
  her one card and five minutes from the next rung on the same evening. Grier's rungs are routed away from
  his room for the same reason, and here the door up is far cheaper than his 30-minute walk, so the routing
  has to do more of the work.

### The silence is a property of the LEVEL, not of the hour

§9 requires that she cannot make a sound up there; §6 gives it a physical cause. Written as the **level** —
open ceiling, no partitions, no carpet, no doors that shut — it reads the same at three in the afternoon as
at nine at night, which is what a room used across an eleven-hour window has to do. It is established in
rung 1 (`late`), where nothing else happens, so that by the time rung 3 needs it, it is a rule of the room
rather than an assertion made at the moment it becomes convenient.

### One room again, and the frontier is still a man's mouth

`sabin_lab` ships here; `the_dry_store` waits for beat 11. Same rule as beat 8. The telegraph was already
spent and it was better than a card: Sabin forbade both rooms out loud at the hire.

**Its display name is "Sabin's Lab" and that is a collision, not a preference** — `cain_lab` is already
`name = "The Lab"`, and the two rooms in question are the two labs in a game about who built her.

### ⚠️ AND I MEASURED THE REGISTER WITH A BROKEN SCRIPT FIRST — worth writing down

The first ratio script I wrote at beat 9 read a `group` block's children from `props.blocks`. In this file
they sit on the block itself, so **every band in every hub was silently dropped from the count** — which is
most of the dialogue in the game, since bands are where NPCs talk. It reported 2.135; the correct walker
reports 2.106.

**The historical running total is fine** — reconstructing the file without beat 9's canvases reproduces
**2.110** exactly on the correct instrument. The bug was mine, today, and it nearly went into this document
as a regression that had not happened.

### ⚠️ SABIN NEEDS NO CAP CANVAS, AND `store_located` DIED UNUSED — decided at beat 10, from the build

**Recorded 2026-08-27.** Grier's rig is `hub → loop → finisher → drain canvas → **located cap**`. Sabin's is
the same minus the last link, and the reason is mechanical rather than aesthetic.

`cap_grier_gives` exists because `piece_one_held` and `rise_named` are **flags**, and a flag whose only setter
is a triggerless canvas has nowhere for `setup.computeHintGoal` to point (`template_import.py:1044`). Sabin's
forward gate is *"she knows where the sample lives"* — and the house had already solved that shape without a
flag: **rev 92 retired `vane_confirmed` and pointed all five of its gates at `colm_drains_done gte 1`**
(`1_metadata:104-109`).

So **`sabin_drains_done gte 1` is beat 11's gate**, §19's `store_located` working name is dead, and the rig is
one canvas shorter. The fiction is better for it too: **there is nothing for Sabin to hand over.** Grier knows
he has something and chooses to give it up; Sabin does not know he gave her anything, and a cap canvas would
have had to invent a moment where he did.

### ⚠️ NO WALL, AND THAT IS THE WHOLE CONTRAST — built at beat 10

Grier's loop departs from the shipped facial/inside/ass contract because §8 requires that **nothing** finishes
below the break. **Sabin's does not depart from anything.** Everything works the first time it is asked to,
the ass finish is simply the only one that pays, and the switchboard is three bands and five exits instead of
four and eight.

That asymmetry is §15's claim — *two repeatable surfaces that feel nothing alike* — and it is carried by the
men, not by the machinery. The suite asserts the facial finishes on the very first visit and that no wall
prose appears anywhere in it.

### The seat is his hand over her mouth, and that is why beat 9's rung mattered

A drain needs skin on skin. Grier's is her hand shut on his wrist. Sabin's is **her mouth open against his
palm** — the gesture `hub_sabin.bench` established as the room's own answer to the silence (§6, §9), now
load-bearing. *The thing that keeps her quiet is the thing the drain sits in.* One square inch doing both
jobs, and it cost nothing because beat 9 had already paid for it.

### What the drain gives, and the two things it deliberately does not

**§9: he is four months in, he does not know what anything MEANS, but he knows where everything IS.** So the
payload is a filing memory — a courier in April, a signature taken one-handed with a mug in the other, a cold
cabinet two floors under the lab, **rack four, second shelf**, and an eleven-character reference he knows by
heart and has never once been curious about.

- **It does not open piece two.** *The making* is spent at the capstone (§12), the same discipline that kept
  the childhood out of `grier_drain_canvas.d0`.
- **It does not conclude the swap.** It ends on the door: the store logs, the item is signed for, and the man
  who signs for it checks a temperature and nothing else — *she cannot take it off that shelf, she can only
  put something else on it.* That is §9's *"a swap or a con, not a robbery"* arrived at by her, inside the
  payload, instead of announced by a card.
- **§5's second gut-punch lands once**, in one thought bubble, and the suite asserts it appears exactly once.

### ⚠️ TRACK B SHIPPED WITH ITS TOP BAND DELIBERATELY UNWRITTEN

`sabin_suspects` is a hidden trait, **+1 per shift on `work_the_archive` and nowhere else** — §9 puts the
exposure on the reading, not the sex, and a second setter inside the loop would tangle the two tracks that the
whole design says never touch. Three bands: he is glad she is fast · he starts asking *how* she reads and
writes something down · he puts a page in front of her that is not from her range and she answers it in four
seconds.

**The third band stops at the edge and concludes nothing out loud**, because **§21 open item 2 is still open**
— *how close does he get, and what does the last band say* — and that is the beat that spends it (`beat_0132`)
deciding, not this one filling a ladder to look finished.

**And it gates nothing.** The day job is optional and the swap rides `sabin_drains_done`, so a player who
never takes a shift is never locked out. Proved live: every drain assertion in the suite runs at
`sabin_suspects = 0`.

### The register fix was five conversions, and the loop still landed under the baseline

The new scenes came in at **3.548 : 1** — `sabin_drain_canvas.done` alone was 8.11 and `d0` was 6.04 — which
took the file from 2.106 to **2.126**. Fixed the only legitimate way: **the fact moved into his mouth.**
*"Eleven times out and eleven times back"* is a line now instead of a narrated sentence, he gives the stool an
instruction, he tells her to stop holding her breath, and he says out loud that he keeps talking because it is
the only way he can tell she is all right when she will not make a sound. The `done` node lost a paragraph
because a node hit a dozen times should not run three.

**File: 2.106 → 2.102. New scenes: 3.548 → 1.939.**

### ⚠️ THE SUITES DID NOT SURVIVE AGAIN — third time, and it changed how they are written

Beats 5 through 10's suites and the cross-beat regression were all gone at the start of this beat. The work
was rebuilt as **`_harness.py` + two thin suites** so the next loss costs one file instead of seven, and the
regression now covers the whole release (schedules, both ladders, Grier's wall, the Rise's auto-fire order,
beat 8's three bounces, the day job, and the card chain end to end) rather than one beat's diff.

**This is the third time. The standing recommendation — `games/vesper/tests/` — is still LO's open call.**

### ⚠️ OPEN ITEM 3, CLOSED — and beat 10 had already answered it

**Recorded 2026-08-27.** *"What the swap for piece two actually is"* needed no invention. `beat_0131`'s drain
put every constraint in Sabin's own mouth: **the door logs · the item is signed for · he checks a temperature
range and nothing else** (*"Nothing else about it interests me"*).

So the con is a blank of the same physical type, carrying the same eleven characters, that will hold a
number. Kess builds it in two hours off a hull he stripped in the spring, and the specification is one line
long because the specification really is one line long.

**And the log is the reason it must be a swap.** A theft turns that book into a confession — a reader who
went in the morning something vanished. A swap makes the same book harmless: she went in, she came out,
nothing is missing. **The swap is what makes signing in safe**, and she signs it in her own cover name, which
is the boldest thing she does in the release.

**Her one clever move is that a dial has no memory.** The cabinet does not record that it was opened; it
reports what it is reading *now*. There is no window to be quick inside of — there is a needle, and the needle
is slower than her hands. That is §9's *"her mind, not her body, does the work a second time"*, and it is a
real deduction from a fact the player already has.

**The clock is Kess's line, and it is the release's last standing door.** *"That'll hold a dial forever. It
holds a man exactly until the day one of them opens it up and reads it."* Sabin wants the **method**, which is
in how the capture was taken and not in what it says — nobody reads a thing they already know how to copy. The
card does not date it, because nobody knows.

### ⚠️ OPEN ITEM 2, CLOSED — how close Sabin gets is ALL THE WAY, and he stops on purpose

**Recorded 2026-08-27.** The suspicion meter's fourth band, at `sabin_suspects gte 9`, is him saying the whole
list out loud and then putting it down:

> *"You read a notation you have never been taught. You correct my arithmetic in your head and then decide
> whether to mention it. Nine hours and you do not get tired, and you do not eat. I have been keeping a list.
> I am going to stop keeping it. Whatever you were before this and whoever is paying for it is not in my fee."*

**The answer is his character and not luck.** §4 built him out of one sentence — *"completely amoral about who
is paying… he does not ask what it is for, because asking is not in the fee"* — and a man made of that does
not fail to notice. He notices everything and declines to own it, because knowing would cost him a job he is
paid enormously to keep. **That is colder than being fooled**, and it is the only ending this character had.

**§19 row 11's "first real bite" lands on the player, not on the mechanics.** Nothing locks and nothing turns
hostile. What lands is that he saw all of it.

**And the meter still gates nothing** — the promise `beat_0131` made. The door into the store reads
`decoy_made`, never `sabin_suspects`. Nine shifts is a lot of floor and this is optional content.

⚠️ **Band 3 had to be bounded `lt 9` in the same edit.** Adjacent `[group]` blocks merge into one if/elseif
chain and first match wins, so an unbounded `gte 6` above the new band would have made it dead code with a
green build — the `beat_0122` trap, third appearance.

### The Rise is finished, and all three of its rooms are nav-invisible

`the_dry_store` closes the building §6 specified: floor at beat 8, lab at beat 9, store here — **a location
ships with the beat that opens it**, three times, no greyed cards. The regression asserts all three render an
empty navigation div.

### ⚠️ THE REGISTER MEASURE HAS A CASE IT CANNOT READ, AND THIS BEAT IS IT

`5_scenes.toml` went **2.102 → 2.123**, and the entire delta is one canvas: **`cap_the_swap` is 330 paragraph
words and zero dialogue words, because there is nobody in the room.** Measured directly — the file without
that one canvas reads 2.102 exactly.

The metric is a proxy for *"did you narrate something that should have been played."* Here §9 requires an
empty room, and the beat is her thinking. **The check that actually applies is the per-beat word target, and
that one was failing**: the scene came in at 55 words a beat and was tightened to 33 / 40 / 39 / 61 / 42 / 30 /
41 against a 35–40 target, with the reasoning moved out of paragraphs and into `thought_bubble`, which is the
unit for a mind working and is excluded from both sides of the ratio.

**2.123 is reported, not gamed.** Moving `kess_makes_the_blank` into `5_scenes` would have "fixed" the number
by relocating a file, and it belongs in `3_activities` with `activity_buy_papers`, whose shape it copies.

### THE PAUSE — built at beat 12, and the mirror had been waiting for it since beat 6

**Recorded 2026-08-27.** §10's one concession is *"She does not know what she just saw. The player does."*
Shipped as: she says *"Nothing again,"* and **in the glass his hands stop.** Both of them, over the tray,
holding nothing. He does not look up. About two seconds. Then they start again and put the tray straight.

**The mirror is why there is a beat here at all, and it was planted two beats earlier.** `cap_cain_opens`
put it in that frame *"so a man working on himself can see what his own hands are doing"*, and
`cap_install_one` had her watch the whole first seating in it. She is facing the wrong way; the glass is the
only reason she sees anything. Nothing had to be staged.

**Her reading of it is wrong, and the misreading is the mechanism.** She takes it for a man who thinks he has
botched the seating — *"He thinks he has done it wrong. He has not done it wrong — she would have felt
that."* §11 is where it turns out he had known since the first one and was hoping he was wrong. **The prose
never explains the pause**, and the suite asserts five explanatory phrasings are absent from the built text,
alongside the seven reassurance phrasings `beat_0127` established.

**He says LESS than he did at the first install, not more.** Install one gave her *"It is supposed to be in
there. It is in there"* — true and empty. Here his entire answer to *"What was that"* is **"Get your arms out
of the cradles."** An instruction, not a refusal and not an answer.

### The three pickups are a diminishing sequence, and that is the design

| | beat | what it spends | length |
|---|---|---|---|
| 1 | `cain_comes_for_her` (beat 2) | the transgression — he is inside the one room nobody signed for | full scene |
| 2 | `cain_comes_again` (beat 6) | she has stopped being surprised by it | 3 beats, 2 clicks |
| 3 | `cain_comes_third` (beat 12) | **nothing is left to spend** — so it carries the clock instead | 2 beats, 1 click |

**The third one's content is Kess's warning, in her mouth, to the only person she can say it to — and Cain is
not interested in it.** He asks her nothing about the tower, the room, the man or the log. It reads as a man
who is unbothered; it is a man who already knows the thing that matters is not on any shelf in that building.
**That is the first crack and `beat_0134` is where it opens.** Nothing here spends it.

### No scene image on either canvas, and an `img` count is not a media check

`scenes/wren_in_the_frame.jpg` belongs to `cap_install_one` (one asset, one block), and a second
near-identical slot would be media debt bought for a scene whose point is that this has happened before —
the call `cain_comes_again` already made.

⚠️ **Worth knowing for every suite from here:** a `dialog` block with an `npcId` renders that NPC's **speaker
portrait**, so `cap_install_two` serves `./videos/cain.jpg` with no media block anywhere in the canvas. An
assertion that counts `<img>` elements is not testing what you declared; test for the `scenes/` path.

### ⚠️ THE REGISTER IS CREEPING, AND THE LAST THREE BEATS EXPLAIN WHY

**2.102 → 2.123 → 2.127**, against a **2.14** ceiling. Nothing here is a defect and every step was measured:

- **beat 11** added a solo con with nobody in the room to speak (330 paragraph words, zero dialogue).
- **beat 12** added a scene whose only event is a man saying nothing for two seconds.

Both were tightened rather than accepted — `cap_install_two` came down from **8.71 : 1** to **5.24 : 1** on
five edits, four of them trims and one a real conversion (Cain's flat *"Both of them in. That is the whole of
the mechanical part and it is done"* where there had been another paragraph of her waiting).

**And a correction to how I have been reading the target.** The ~35–40 words figure is a **prose-unit**
target, not a hard per-beat cap: shipped cascade beats that carry a paragraph *and* a line of dialogue run
60–70 words each (`hub_grier.knees`, measured). Beats of 41–66 here are in line with the corpus, and
over-tightening them was making the prose worse, not better.

**`beat_0134` should pull the number back down on its own** — Cain finally saying the thing is the most
dialogue-dense scene left in the release. If it does not, that is the signal to look hard at the trend rather
than at one beat.

### ⚠️ BEAT 13 HAPPENS AT THE COT, NOT THE LAB — §19 row 13 corrected by the build

**Recorded 2026-08-27.** All three pickups are consumed one-shots (`cain_comes_for_her`,
`cain_comes_again`, `cain_comes_third`), and `beat_0133` established that the sequence has nothing left to
spend — the third was already down to one click. A lab scene would have needed a **fourth knock** that could
only repeat itself.

**It also does not need the lab.** The lab is where work happens and there is nothing to install. So the
route was not rebuilt: **the pattern is broken, and the break is the content.** Every previous visit ended
with her walking somewhere with him. This one ends with him leaving and her still sitting there.

**And he is sitting down**, which is the tell — three visits, three times standing at the feed line with his
coat on, ready to go. A man who sits down has not come to collect anybody.

### §11's answer is in his mouth, once, and she is the one who raises the objection

§11 names the risk exactly: *"she has been fucked in every room of this game, why has this not happened
already"* — and requires the answer from Cain or *"the scene reads as arbitrary."*

**She raises it, with the shipped rooms named** — a depot office, a penthouse, a back room under a bar, a
bench in the Reach and a bench in a tower. His answer is one question:

> **"Name one of them where you were not working."**

She goes down the list and cannot. A cover in most of them; in the rest a mark, or a weapon, or a thing she
is there to take out of the back of a man's head, and in two of them all three at once. *"You have never once
been fucked without a job on, and a body doing a job does not put anything down. It cannot. That is what it
is for."*

**And the diagnosis is verbatim from §11**, in his mouth: *"They are not coming up because you never stop."*

### The evidence is Glitch III, and it had to be banded

The one time anything ever surfaced on its own is `activity_captive_room`'s **hold_still** verb — *"She lies
on her back and stops doing anything at all"* — and that verb is **repeatable with the Tier-3 spend behind
`glitch_iii_seen`**. A player can finish captivity without ever holding still.

So the cell is named either way (on her back, nothing left in her, nothing in that room to get — canon
regardless), and only **the hand** is banded on the flag. Both branches asserted live.

**Cain does not ask her what it was.** Not one question, from a man who asks about everything, and it goes
past both of them untouched. §17 reserves what he was to her and §12 reserves the name — **his tell is the
silence**, which is now the second thing he has failed to say, after `beat_0133`'s two seconds.

### He promises nothing, and he asks for no answer

*"I told you the mechanical part was done. It was done. It got you nothing and I am not doing that to you a
second time."* Then he stands up, puts the chair back, and goes — **without asking her for an answer, because
he has not asked her a question.** The beat ends on the price **named and not taken**; accepting it is
`beat_0135`'s on-ramp, and that room is still §21 open item 1.

### ⚠️ THE REGISTER CREEP REVERSED, AND THE PREDICTION HELD

**2.127 → 2.090**, the lowest the file has been all release. `cap_the_price` runs **0.56 : 1** — 219
paragraph words against 392 of dialogue — because it is a man talking, which is what `beat_0133`'s note
predicted would fix the trend without anyone having to intervene.

**So the creep was content-shaped, not craft-shaped**: two consecutive beats that were a wordless con and a
wordless pause, followed by one that is nothing but speech. Worth remembering the next time the number moves
two beats in a row — check what the beats *are* before tightening prose.

### ⚠️ OPEN ITEM 1, CLOSED — the room is called **"Somewhere"**, and the name is the design

**Recorded 2026-08-27.** §11 requires a place she has never been, never returns to, and **is never told the
location of**. The fiction can leave it unnamed; the engine cannot. So the id is `room_no_name` (greppable)
and the **display name is "Somewhere"** — the honest answer to *where is this*, and in a list of The Cot /
The Berth / The Undertow it reads as a hole where a place should be.

**"The Room" was not available** — `captive_room` owns it, and the cell is the wrong echo entirely: that room
is where things were done to her by people who wanted something. This one is the exact inverse.

Nav-invisible on the `cain_lab` shape, and here the no-way-back is *correct in a way it is nowhere else in
this game*: she is not driving and does not know where she is. `activity_leave_somewhere` is him taking her
home, because being brought home is the only exit that room ever had.

### ⚠️ AND THE OTHER HALF OF OPEN ITEM 1 — how she says yes, when he asked her nothing

`cap_the_price` deliberately ended without her answering: he asked no question and said he would not.
**She cannot reach him** — four cards across this release have now said *"he finds you"* — so a message was
never available.

**So the answer is the theme arriving as a mechanic: she stops.** No shift, no tower, no lane, no bench. She
stays in, the second day is worse than the first, and on the second night he is at the feed line.

> *"Two days. I gave it three before I came and looked."*

The price is being somewhere that stopping is all there is left, and **the way she buys it is by stopping.**
It costs two days of clock, and the card says so. Repeatable, not a one-shot — a two-day scene a mistimed
click can lose is a scene nobody should be able to lose.

### The drain comes off at the door, and that is what makes the reflex land

§11 requires *nothing to gain*, and Cain enforces it physically: he holds his hand out and names why.

> *"You will not need it, and you will reach for it, and I would rather you reached into a pocket that was
> empty than found it there and used it."*

Forty minutes later her hand goes back and down to the flat of her own hip, closes on cloth, and **she had
not told it to.**

⚠️ **`equipped_weapon` is NOT touched.** Four gates in this game read it as `eq 1` or `eq 2` — both drain
finishers and the emitter fires — and zeroing it would strand every one of them for a player who walks out
of that room and back into a loop. He gives it back on the drive home; the header is the contract.

### She fails twice, and the second failure is the one a lesser scene would miss

The first is the hand. **The second is that she then tries to stop** — hands slack, hips still, eyes shut,
holding it deliberately — and catches herself *counting how long she has managed it, and checking, and
pleased with the number.* **Deciding to stop is a task.** She sets herself the job of having no job and does
it well.

And `beat_0134` warned her, in his own mouth: *"You cannot decide to stop. Nobody can."* **So this is her
failing a warning she was given**, which is the only version that does not read as a bug.

### The men are indifferent, not cruel — and indifference had to be AUDIBLE

§14 row (c): anonymous, plural, nothing owed. The first draft gave them two lines in twelve beats and
measured **7.36 : 1**. The fix was not trimming: **men talking over her about nothing is colder than a silent
room.**

> *"She the one he rang about?" · "Does it matter."*
>
> *"Is there anything left in that bottle or did you finish it."* — said while she is still on the mattress.

Four added lines and three trims took the scene to **5.76 : 1**, and it is a better scene for it.

⚠️ **The anonymous speaker is `speaker = "unknown"`, not an invented npc id.** `npc_unknown` does not exist,
and a dialog block whose `npcId` does not resolve **drops the speaker silently** (the `beat_0122` defect
class). The shipped convention is Kess's own intro — *"Stranger:"* — and it is exactly right here: these four
men never acquire names, in the fiction or in the file.

### ⚠️ A SECOND STRUCTURAL CASE THE REGISTER MEASURE CANNOT READ

**2.090 → 2.112.** Two beats in this release have now moved the number for the same reason: **beat 11 was a
room with nobody in it, and beat 14 is a room where nobody engages with her.** Both are §-mandated.

The levers that were honest were both used — voices for the men, and interiority moved out of paragraphs and
into `thought_bubble`, which is the unit for a mind working and is excluded from both sides. What was NOT
done is inventing warmth to buy a decimal.

**The pattern to carry forward: an explicit scene whose partners are indifferent is structurally
narration-heavy, exactly like a solo scene.** Check what the beat *is* before treating the number as a defect.
`beat_0136` is the same scene with her present in it, and should read differently.

### WHAT MAKES THE SECOND TIME WORK IS NOT EFFORT — and `beat_0135` is what made that the only option

**Recorded 2026-08-27.** The failed attempt already proved that **trying is another job**: she held still,
counted how long she managed it, and was pleased with the number. So the turn here had to be the opposite of
effort, and it is — **she stops wanting it to work.**

> *"Not the working. The wanting. Nothing is going to come up out of her tonight and she is going to be here
> anyway, and that is the end of it."*

The operator goes quiet because it has nothing left to be for. That shape only exists because the failure
shipped first, which is the whole argument for §10's structure.

**And she asked.** `activity_say_yes` band B is three words — *"Take me back."* §11's sentence in full: the
game has been her climbing out of being used, and the last step back to herself is going all the way down one
more time **on purpose, because she asked for it.** The first time it was done to her.

### The memory joins four shipped leaks, and nothing happens in it

Late light on one side of her face (opening night, `2_one_shots:157`) · the same fragment longer and almost
holding (glitch I recurrence, `:276`) · *loved once, completely, by someone, before all of this* (glitch II,
`:310`) · the hand at the back of the neck with the thumb along the seam (glitch III, `3_activities:2202`).

**Four angles, one afternoon.** She is small, she cannot get a knot, and *nothing whatever has happened as a
result of failing at it.* Somebody behind her, watching, **not correcting.** That is the entire event, and it
is why it hurts.

### The name — §12's handling rules, all four, asserted live

> **"Vesper. You have got all afternoon."**

- Said **once**, inside the memory, in somebody else's voice (`speaker = "unknown"` — there is no face and
  therefore no npc to attach it to).
- **The game does not rename her.** Every location, every card, every portrait still reads *Wren*, and the
  suite walks four rooms asserting the word does not appear on any of them.
- **Nobody else says it** — not Cain, not Grier, not Sabin. The word occurs three times in the whole scene:
  the voice, her own thought, and her own thought again at the end.
- **She does not tell him.** *"It is the first thing in nine years that is hers and she is not putting it down
  where somebody else can pick it up."*

**And there is no face.** She turns to look and finds *"an absence with the exact shape of a person, the way a
file reads when the field was never written."* The game never says why. That is piece three, and the Chairman
has it.

### ⚠️ THE CEILING WAS BREACHED, AND THE FIX WAS NOT A SHAVE

**First draft: `cap_capstone_fire` at 18.79 : 1, and the file at 2.160 against a 2.14 ceiling — the only
breach of the release.**

It was **not** purely structural, and that is the finding. `beat_0135` had already proved that indifferent men
talking over her is colder than a silent room, and this scene gave five men **one line in nineteen beats**.
It under-used a lever it had already been taught. Three passes, all of them genuine craft:

| pass | what changed | scene |
|---|---|---|
| voices | five more flat lines between the men, and *"says something that is not about her"* converted into the actual line | 18.79 → 9.41 |
| units | the turn, the quiet and the fear moved out of paragraphs into `thought_bubble` — a mind working, not narration — plus one flat line from Cain on the landing | → 6.84 |
| fat | five wordy paragraphs tightened; the lead's second sentence was her framing and became a thought | → **5.93**, file **2.140** |

**File: 2.112 → 2.140, exactly at the ceiling and not over it.** The last thousandth came from a real
misplacement, not from hunting a decimal — *"The difference is entirely on her side of it"* is her thought and
was sitting in a narration block.

**The lesson to keep:** when the number goes over, check the levers the release has already established
before concluding the scene is structurally exempt. Beats 11 and 14 genuinely were. This one was not.

### ⚠️ THE SCRATCHPAD WAS LOST A FOURTH TIME — AND THE FIRST TIME MID-SESSION

Every suite and the harness vanished **during** this beat, not at a session boundary. Rebuilt as
`_harness.py` plus one whole-release regression (84 assertions covering beats 3–15: schedules, both ladders,
Grier's wall, Sabin's no-wall, all four Rise rooms, the auto-fire orders, the day job and its four suspicion
bands, the store's bands, the three-install chain, the capstone route, and the whole card chain Z → AJ).

**Per-beat suites are no longer worth writing** — they are deleted before they earn out. One consolidated
regression plus the current beat's suite is the shape from here. `games/vesper/tests/` remains LO's call and
is now costing work rather than just tidiness.

### HER GENEROSITY IS THE WEAPON — and nothing in the scene has to be cruel

**Recorded 2026-08-27.** §13's engine is one word: **she is pleased.** She got what she went through all of
that for and she wants to tell him, and §19's want column says it plainly — *"to give it back to him."*
**This is the first time in two acts she has wanted to give somebody something rather than get something out
of them**, and it is what does the damage.

She spends a day on the strip asking after a man she cannot describe, fails, comes home, and he is already on
the end of her bunk — as he has been every single time. She is halfway through the first sentence before the
door is shut, and **she talks fast, which she has never once done in this game.**

**She says the name out loud**, in her own room, to the only person she would say it to. §12's rule survives
intact: *nobody else* says it for the rest of the release, and she is not somebody else — she is the person it
belongs to. **He does not repeat it.** The word occurs twice in the whole scene and both are hers.

### The first crack in Cain, and she does not understand it

He asks about the face twice, carefully — *"Nothing at all. Not a build, not a height. Not a hand you had seen
before."* — and she is still pleased, and says the word *perfect*, and means it about the file.

> **"You don't remember me at all?"**

Asked once. Not as information — as a man being hurt out loud. He has held the told-is-not-felt line through
two dead installs, a pause at `beat_0133` he thought she could not see, and a question at `beat_0134` he
deliberately declined to ask. It goes in one sentence he did not mean to say.

**And she answers it accurately, because that is what she does with questions:** *"It is a childhood — it
would not have you in it."*

**He does not explain, and neither does the prose.** §17 reserves what he was to her, and the suite asserts
five confirming phrasings are absent. Standing up takes him two goes, and she has never seen anything take him
two goes, and she files that and cannot solve it. §13's last line, built: *a room where one person is hurt and
the other genuinely does not understand why.*

**He leaves her the third piece instead of himself** — *"Go and ask the old man what went out of that room in
the third tray."* That is `beat_0138`'s gate in his own mouth, which is how every link in this release has
been handed over.

### ⚠️ §19 ROW 16 CORRECTED — the cot, and this time it is not a fallback

`beat_0134` already moved row 13 off the lab because all three pickups are spent one-shots. The same is still
true, but the argument here is positive rather than forced: **the cot has an arc and this beat completes it.**

| beat | what the room is |
|---|---|
| 2 | he is inside the one room nobody signed for |
| 6 | she has stopped being surprised by it |
| 12 | there is nothing left to spend, so she brings him the clock |
| 13 | he sits down, says the price, and leaves without her |
| **16** | **he comes, she talks, and he breaks** |

**The lab is where he is a technician. This is the room where he is a person**, and §13 needs the second one.

### The register fell on its own again, exactly as predicted

**2.140 → 2.121.** `cap_the_question` runs **1.17 : 1** — 394 paragraph words against 336 of dialogue —
because it is two people in a room talking, and `beat_0136`'s note said this is what the metric does. Third
confirmation that **the number tracks what the beat is**: it climbs for rooms where nobody speaks to her and
falls hard whenever the beat is a conversation.

### THE FIRST CHOICE ON `hub_grier` GATED ON A FLAG RATHER THAN ON `relation` — and that is the content

**Recorded 2026-08-27.** Every rung on that hub is access bought by climbing. **This one is not a rung.** She
has been climbing him for a chapter and this is the one thing she has ever come down that lane to *ask* for,
so it takes no `relation` clause going in (proved live at relation 0, where every ladder rung above it is
shut and this one is open) and pays +2 coming out — he tells her a thing he has never told anybody, and trust
in this game is `relation`.

It sits at the bottom of the choice list, under the loop, because it is **a different errand in the same
room**. And it closes on `third_located` while **his loop stays open** — `beat_0126` locked that he survives
and that nothing may read as a goodbye, and the suite asserts all four ladder rungs and the loop entry are
still there afterwards.

### She asks the wrong question on purpose

§13: *"Not for a part. She asks about the man he hates."* So she asks about **Cain**, gets nine years of
grievance, and the thing she actually came for **falls out sideways in the middle of a sentence that was
going somewhere else** — *not offered, spilled.* Same move as Sabin naming two rooms while forbidding them.

**She does not take her coat off**, and he notices before she reaches the chair, because in four months she
has never once come into that room and stayed dressed. That is the whole staging: every other visit was a
transaction with her clothes in it.

### What Grier knows, and the four things he must never say

He knows there were **three trays**, that he walked out with two, and that the third **went up** — a man came
down for it in a case with a lock on it, spoke to nobody, and took it up the tower. He spent four years
looking: *"Every road I put a hand on went up and stopped, and the two that did not stop, stopped me."*

He does **not** know whose any tray was. `beat_0126`'s drain established he had two in his arms and never
once looked up, **and he still does not know the one he took was hers.** The suite asserts four leak
phrasings absent, plus: §17 held (he has no idea what Cain was to her — nobody does, including Cain's own
mouth one beat ago), the Chairman never named, and nothing about what is *in* the third piece.

**She already knew there were three** — `beat_0126`'s payload showed her the trays and her own thought said
*"three, by kind, exactly what Cain said."* **The new fact is where the third went**, and that is §13's
arithmetic exactly: **Cain knows who is in it. Grier knows where it went.** Neither could have reached the
other's half and neither will ever be in the other's room.

### The last errand is hers, and she works it out herself

> *"One of them knows what is in that tray. The other one knows where the tray went. They have been forty
> minutes' walk apart for nine years and neither will ever put a foot in the other's room, and she is the
> only thing in this city that is welcome in both."*

Nobody instructs her to bring them together. `beat_0139`'s on-ramp is a conclusion, which is the same shape
as `beat_0132`'s swap — she is handed constraints and finds the move.

### The register, fourth confirmation

**2.121 → 2.082, the lowest of the release.** `hub_grier.the_third` runs **0.35 : 1** — 137 paragraph words
against 388 of dialogue — because it is a man who has not been asked a question in nine years, being asked
one. The rule holds without exception now: **the number tracks what the beat is.**

### TWO VOICES IN ONE CANVAS NEEDED NOTHING NEW

**Recorded 2026-08-27.** Grier is present the ordinary way — `requires_npc` plus the `npc_at_location`
clause `beat_0130` proved an auto-fire actually needs. **Cain has no schedule row and never will**
(`1_metadata:1449` — `getNpcsPresentAtLocation` is not canvas-gated and he is the reserved reveal of the
whole game), so he speaks as a **scheduleless speaker**, the `cap_mercer_resurfaces` shape he already uses in
`cap_the_lab`. Two men talk in one room and the engine did not have to be asked for anything.

### The last on-ramp is an ASK, and he refuses first

Every pickup is a spent one-shot and card AL ends on *"put them in one"*, so the errand had to be a surface
she takes. She tells him where it went; he says **"No."** — *"Not an argument, not a reason — a door closing,
and she has watched enough men close enough doors to know she is not getting this one open by pushing on it."*

**So she does not push. She reframes it** — *"I am not asking you to talk to him. I am asking you to stand in
his room while he talks to me, because he has the half you have not got and you have the half he will never
get, and I am the only thing either of you will let through a door."* He picks his coat up, which is his
entire answer. That is the payoff of `beat_0137`: two acts of asking for nothing, and now this.

### §13's four locked parts, all asserted live

- **Cain says almost nothing.** No gratitude, no apology — five phrasings asserted absent. The only mention
  of forgiveness in the scene is its refusal.
- **Grier says everything, including the sexual weapon**, crude, aimed at Cain and never at her, and he
  watches Cain's face the whole way through: *"Look at me while I say it. I have waited a very long time to
  say it and you are going to look at me."*
- **No reconciliation.** *"nobody in the room mistakes it for forgiveness."* He gives them the answer anyway,
  because he was a good man once and this is the last of it he has got.
- **He pours another one** before they are through the door, and the neck of the bottle goes against the
  glass twice, because his hand is not steady.

**And Grier survives the release**, which `beat_0126` locked. The regression asserts his hub and his loop are
both still standing after the last scene.

### The answer is a conjunction, and Grier is the one who says what it means

Grier knows the third tray was **filled last** — they finished the other two, shut them, and went back into
her for it, and it took another hour nobody in that room enjoyed. **Cain asks whether it was filled last**,
and that is the tell.

> *"Nobody asks that. Nobody on this earth asks which one was filled last unless he already knows what went
> into it. Look at him, girl."*

**Grier says it, not the narrator.** He is savage and clever and has spent the whole scene watching that
face, and putting the deduction in his mouth keeps the prose out of it entirely.

### She learns there was a man. She does not learn which one.

§13 exactly: *"she now knows a man was in her life and was cut out of it, and that a stranger owns him."*
Cain gives her that and refuses the rest **to her face** — *"That is all of it you are getting from me
today."* §17 holds: five confirming phrasings asserted absent, and the Chairman is implied by *"whoever is at
the top of that tower"* and never staged.

**The player has now had three tells and she has had none of them land** — `beat_0133`'s two seconds,
`beat_0137`'s question, and this face. She even notices the pattern: *"Twice in a week. That is the second
time she has watched that happen to him and she has no name for it either time, and she names things for a
living."*

### The release ends on a silence, and the last line is hers

> *"There is a man in a box at the top of a tower who was in her life, and a stranger has had him for nine
> years. And there is a man walking beside her who has not spoken since a machinist told him what she does on
> a bench twice a week, and she cannot work out what is wrong with him. She has never once failed to work out
> what is wrong with anybody."*

Not a cliffhanger. A room where one person is hurt and the other genuinely does not understand why.

### The register, fifth and final confirmation

**2.082 → 2.047, the lowest of the release.** `cap_the_two_men` runs **0.82 : 1** — two men who have not
spoken in nine years, in one room. The rule held across every beat of this chapter without a single
exception: **the number tracks what the beat is.**

### The proofs, and when they are due

| Claim | Due before | Fallback if it fails |
|---|---|---|
| ~~**The two-token gate**~~ **✅ PROVED at beat 8** — `cover_research` equipped **AND** `face_worn is_true` on `cap_sabin_hires`, all four combinations asserted live; `work_the_archive` is the second surface carrying it | beat 8 | *(not needed)* |
| ~~**The conditional drain**~~ **✅ PROVED at beat 4** — the ass finish is present but fires nothing until a state flips | beat 5 | *(not needed — it is the shipped `loop_mercer_finisher` fork, measured `.cold` vs `.d0`; §8)* |
| **The memory store** — `canvas_chip_view` moves to `the_cot` and gains a part-filled band | beat 1 | Keep it at the cradle and cut the store from the release |

**Engine-forced changes bounce UP to this doc and get surfaced. They are never patched into TOML quietly.**

### Save-safety rules for this release (Vesper is live)

- **`cover_research` is a progression gate.** Its grant rides on a **repeatable shop screen** — the same
  shape as `activity_buy_face`, which is repeatable and whose venue (`underworld_market`) survives the raid.
  Never a one-shot handout: that is the 0.1.5.1 soft-lock, and it is the same item class.
- **Moving the bar and moving the store are MOVE amendments.** Every line of prose quoting the old place is
  re-read in the same turn. Green build, lying game, otherwise.
- **`canvas_chip_view` keeps its id** after it moves. Renaming any shipped id orphans saves.
- **New flags and traits are safe to add** — the backfill carries them into old saves. Items are not.

### The register target, measured

Vesper's narration-to-dialogue ratio, measured 2026-08-26 with the skill's own script:

| file | ratio | read |
|---|---|---|
| `3_activities.toml` | 51.6 : 1 | **correct** — she is alone, nobody is there to speak |
| `2_one_shots.toml` | 10.1 : 1 | worth a look; some are interior by design |
| `5_scenes.toml` | **2.14 : 1** | **the number that matters** — this is where people share a room |
| whole game | **2.70 : 1** | target is ≤ 2:1 |

Every beat in this release lands in `5_scenes.toml`. **Hold 2.14 : 1 or improve it. If it climbs, the beat
narrated a scene that should have been played.** Re-run at every build and report the number.

**Running total:** 2.140 at beat 1 · 2.106 at beat 2 · 2.109 at beat 3 · 2.106 at beat 4 · 2.103 at beat 5 ·
2.106 at beat 6 · 2.106 at beat 7 · 2.110 at beat 8 · 2.106 at beat 9 · 2.102 at beat 10 ·
2.123 at beat 11 · 2.127 at beat 12 · 2.090 at beat 13 · 2.112 at beat 14 · 2.140 at beat 15 · 2.121 at beat 16 · 2.082 at beat 17 · **2.047 at beat 18**, the lowest of the release. The number
tracks WHAT THE BEAT IS — it rises for rooms where nobody speaks to her (11, 14) and falls hard for a beat that is a man
talking (13). Beat 15 BREACHED at 2.160 on the first draft and was brought back to exactly 2.140 by three
craft passes, not by shaving. Ceiling 2.14: touched once, never crossed in a shipped build (which lands in `3_activities.toml`, where 43.9 : 1 is the correct
number — she is alone at a stall and the only other voice is a woman with no NPC id). The metric is
`paragraph` words : `dialog` words in `5_scenes.toml`; `thought_bubble` is excluded from both sides. Beat 4's
own new content ran **1.950 : 1**, which is what pulled the file back down — Grier talks, and the rungs let
him say the thing rather than having the narrator explain it (Rule 4).

*(`design_book.md` still records this as 7.25 : 1 — a July figure, corrected by The Leash and The Face. Fix
that line at the fold.)*

## 20. Size — the honest note

**This is bigger than *The Face*.** Two full ladders, a Tier-3 capstone with a written failure in front of
it, and the Cain beats.

**If it has to shrink, the give is Grier's ladder — three rungs instead of five.** Sabin is the release's
main repeatable; Grier is the sharp one and he works short.

**Do NOT cut:**
1. **Grier's wall** (he cannot finish). It is what makes his grind unlike every other grind in the game.
2. **The failed first attempt at the capstone.** It is the best beat in the release.
3. **The second install where Cain stops.** Without it, two dead installs read as a bug.

---

### ⚠️ THE BUILD-BOUNDARY BADGE WAS A LIE FOR THE WHOLE PRE-RELEASE WINDOW — found at beat 19

**Recorded 2026-08-27.** §19 row 19 asked for a boundary card. What the audit actually found is that the
game already had one and it had been pointing at the wrong build for eighteen beats.

`terminal_text` is the one field in this game that names a **build** boundary rather than an **arc** ending
(rev 142, card M; moved to card U at beat_0095). Card U reads:

> **Chapter complete — the story continues in the next release**

`beat_0123` noticed half of the problem and fixed that half: it gave card U a closer on `cain_named_grier`
so the badge could not survive *into* WHOSE HAND. What it did not consider is the window *before*. Card U
opens on `raid_done`, which THE FACE sets at its last beat, and `cain_named_grier` is not set until
`cain_comes_for_her` auto-fires — **and that is an auto-fire at the cot**, so it waits for her to go home.
In between the player can run the ruin crawl, work The House, fight the pit, and burn days of game time
with a green check on the Quests page telling them the story continues in a release they already own.

Two sentences of prose carried the same false claim: *"That is where this build ends"* and *"Whatever Cain
was going to say next, you will hear it when this picks up."*

**The fix is the rev-129 two-step, third time in this game:** strip `terminal`, `terminal_text` and the
boundary prose off card U in the same edit that adds them to card AM, then **grep the whole table from both
sides** — never read the card in front of you, because a boundary claim is a statement about the whole
build and cannot be evaluated from the rung that carries it. Verified live at four states plus the end:
zero badges anywhere until `two_men_done`, exactly one after it, and it is card AM.

Card U keeps its Support-Us ask (the card-D precedent: a prior card keeps the ask, only the boundary CLAIM
can go false) and now says the true thing in place of the false one — *there is no lab you can walk to, so
go about your business and let him find you at the cot*, which is the sentence card V opens with anyway.

### ⚠️ AND THE BOUNDARY CARD NAMED A SURFACE THAT IS SHUT — caught by reading the trigger

The first cut of card AM's tip listed the standing surfaces from §15 and included *"the store is still two
floors under him."* It is not. `activity_into_the_store` is gated `decoy_made is_true` **+ `piece_two_held`
is_false** — it is the front door of a nav-invisible room and it closes the instant the swap lands, which
is a state card AM cannot render in without.

That is exactly the failure this row of §19 exists to prevent, and it was caught the way it has to be: by
reading the trigger rather than the design book. **The card now says the store is shut**, in the same
sentence as the sealed tower, because a boundary card that only lists what is open is half a boundary.

What it does name, with hours, is what a player can actually still play: Grier from ten in the morning,
Sabin on the floor at eight and in the lab from eleven, the reading at fifteen a shift, and everything that
was already hers. §15's promise — *the fix for three releases ending with nothing to do* — asserted live
after the last scene: both loops open, the day job open, the stairs still there, the store gone.

### §18.4 IS SPENT — one ask, in Sol's mouth, and Wren does not react

The reserved detail is **no body was ever found**, and it lands on shipped canon exactly: `cap_the_raid`'s
last look at that room is *"a chair, a coat, and nothing she can see"*, and card U's header forbids any edit
that resolves it either way before the next release. She left him tasered on boards that were burning and
has assumed the obvious thing ever since.

**Built as a one-shot ask on `hub_sol_undertow`**, gated `raid_done is_true` + `bastien_no_body is_false`,
setting its own flag on the exit. Not a band (a band repeats, and repetition *is* underlining), not an
ambient (a dice roll could land it three times), not a scene (that would make it the thing the release is
about). Sol rather than Colm because Sol's own post-raid band already ends on *"I find I have got no idea
what a man does about it"* — this is the answer to that sentence, from the same mouth, and what he is
describing is a funeral he cannot have rather than a mystery he has noticed.

**And nobody in the scene concludes anything.** The company wrote down everything in the building and there
was nothing on the list to have a service over; Sol has stopped asking because the asking was becoming his
whole day; Wren says she is sorry, and goes. The word *alive* never appears and neither does the noun
*body*. The player holds it alone — the same discipline `cap_the_two_men` and card AM end on.

### The dev jumps, and the one flag that was missing from both

Two, not one. `dev_jump_whose_hand` seeds the complete 0.2.0 end-state and lands at the cot with
`cain_named_grier` unset, so `cain_comes_for_her` fires on arrival and the release opens — which also makes
both of its one-shots replayable for the first time. `dev_jump_whose_hand_end` seeds through beat 13 and
lands one beat short of the capstone; because `price_named` cannot be true unless both loops were beaten,
it necessarily seeds **both standing surfaces open**, which is what beat 20's media pass and any hand
playtest actually need.

**Both were wrong on first build and the suite caught it.** `cap_the_wait` is an auto-fire one-shot at the
cot gated `bastien_drains_done gte 1` + `plan_made is_false`, and both jumps seed the drain counter at 2.
Without `plan_made`, the end jump landed on a scene from two releases ago instead of the on-ramp, and the
start jump had `cap_the_wait` and `cain_comes_for_her` **both eligible at priority 10 on the same arrival**.
`dev_jump_0_1_9_start` does not carry the flag and correctly does not need it — it seeds the counter at 0.
**Any future jump that seeds a Bastien drain must set `plan_made`.**

The assertions that caught it are worth keeping in shape: the first cut checked `"cot" in text()`, which
matches the location description and proves nothing. Checking `State.passage` against the exact canvas node
is the only version of that test that can fail.

### The register, nineteen beats in

`5_scenes.toml` **2.047 → 2.038**, the lowest of the release, against a 2.14 ceiling. Sixth confirmation
that the number tracks what the beat *is*: the only prose this beat added is two men talking about a
funeral, and it is 48 words of narration against 95 of dialogue.


## 21. Open items — decisions still owed

~~1. The new tower's name and its interior locations.~~ **CLOSED 2026-08-26 — THE RISE, three rooms (§6).**

~~1. **The capstone room has no name.**~~ **CLOSED 2026-08-27 at beat 14** — `room_no_name`, displayed as
   **"Somewhere"**, nav-invisible, reachable only by him taking her. And its other half, how she answers a man
   who asked her nothing, closed with it: she stops. See the findings above.
~~2. **The suspicion meter's end state.**~~ **CLOSED 2026-08-27 at beat 11** — band 4 at
   `sabin_suspects gte 9`: he says the entire list out loud and then declines to own it, because asking is not
   in his fee. He gets all the way and stops on purpose. See the finding above.
~~3. **What the swap for piece two actually is.**~~ **CLOSED 2026-08-27 at beat 11** — a blank that
   holds a temperature and eleven characters, built by Kess; the log is why it must be a swap, and a dial has
   no memory. Every constraint came out of beat 10's drain. See the finding above.
4. **Whether Cain goes to Grier's room a second time**, off-screen, after the release ends. Not content —
   a decision about what the next release inherits.
5. **⚠️ The three `requires_npc` auto-fires that fire with nobody there** — `cap_grier_met`,
   `cap_grier_gives`, `cap_sabin_hires`. One line each (`npc_at_location … is_present`), proved on
   `cap_sabin_consults`. It re-opens three validated beats, so it is LO's call and not mine. Five older
   canvases outside this release have the same hole and are explicitly **not** in scope here.
