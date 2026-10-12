# Vesper — 0.2.4: THE TRANSFER

> Design record for **0.2.4**. Story level only. This is the review surface; the blueprint (scene list,
> gates, placement, numbers) comes after LO signs the story off.
>
> **Status:** story agreed with LO in conversation, 2026-10-11 → 2026-10-12; open calls answered
> 2026-10-12. Nothing built.
> LO's calls, verbatim where they were given:
> - *"No sex in this new body I say, this is a machine have different weapons and powers."*
> - *"vega body can be used to get that memory part, post that, vega body might get destroyed by the other
>   machine attacks. From there cain and bastien can collect vega and put wren back to wren body again and
>   might use vega body to modify wren further that can be in the next release."*
> - *"taking the memory needs to be a bit difficult. She might figure out where the memory is and then
>   actually use the weapons attack and kill people. Get the memory on the run, contacts cain and bastien,
>   they are not here yet, but these two other weapons attacks vega. Somehow bastien and cain saves her and
>   takes her back."*
> - *"it is important that in next release wren body can have some of its weapons that will be decided in
>   that features."*
> - Weapons: **yes, all three new ones** (blade, armour, signal). Lyra and Nova: **driven off**. The save:
>   **"yess sacrifice of the main men"** — Dace.
> - *"Currently they dont know about vega so kess and cain first study her body weapons and see how they can
>   put wren in vega."* Then: *"Not 6 nights 3 nights and add wren studying too with a bit of grind like 3
>   grind unlocks new things."*
> - *"vega finds out that the company and the scientist has successfully build a new weapon. And now starting
>   a production unit that can build many at a time."* → **Empty bodies.** The scientist is **Sabin** — *"the
>   one in the company that new scientist they hired"*, not the man in the Reach.
> - The last night: *"She is afraid. Wren and Cain cuddle no sex."*
> - *"she also studies the company where the memory is, where things are."*
> - *"No new sex is fine."*
> - The open calls, answered 2026-10-12: the memory shows **"everything, this also connects and completes. She
>   gets full flash back who she was, what happened, she was being experimented on by her own father and
>   cain."** · *"Vance tower have memory but she can also search for it first in this rise."* · *"She figures
>   out where it is and then they make a plan where she will collect the memory and take it to that place.
>   They came not because of contact simply because they thoughts she is late and they should go check on
>   her."* · *"nothing around her old cover this is the new body she have."*

---

## Why

0.2.3 ended one breath before this. Vega's shell lies in the second cradle at the Site, Cain said
*"Not tonight,"* and the end card points at the door. Cain also said the plan out loud on Kess's table: the
third piece is inside the company, and *"we cannot walk in as we are,"* so she goes in as one of theirs.

This release walks through that door and pays three things the game planted and never spent:
- **The third piece** — the memory with Cain in it, which the Chairman holds.
- **Lyra and Nova** — standing in a line with Vega in the game's opening scene, never used since.
- **Sabin's job** — he took *"an enormous retainer to solve an interesting problem"* and never asked what
  for (`design_whose_hand.md` §4). This release shows what the problem was.

It ends by opening the next one: the wreck of Vega on Kess's table, and the parts of it that can go into Wren.

---

## What already stands (shipped, and read)

- **Kess killed Vega on the table** (`cap_the_table`, `5_scenes.toml`): he opened the seam and *"takes out
  what keeps her running, and Vega stops for good."* So her shell is whole but has no power and no mind.
  Nobody has seen what it does when it runs. That is why the study is needed.
- **The method is already in Wren's head.** Cain on the table: *"The method is in your head, from Sabin's
  piece. The two cradles are in your father's lab. Kess has the hands."* Kess: *"I have opened you twice. I
  can open her. I have never put anybody back into anything."* Cain: *"Marrow did. Twice."*
- **Cain has already promised to guard her body.** *"Stays in his lab, in the other cradle. I will sit with it
  until you come back for it."*
- **Vega said *"This unit will be reported lost."*** Kess: *"Nobody is reporting anything."* The company
  has not heard from Vega since the take.
- **Vega's powers and weak spots** (`design_the_hunt.md` "Vega — what she is", LO "keep all"): stronger and
  faster than Wren, no pain, never forgets a fight, tracks, untouched by the drain, burns power fast, the
  seam at the base of the spine.
- **The units:** *"Vega, Lyra, Nova run the hunt head-on"* (`2_one_shots.toml:152`); in the opening, four of
  them stand in a line in Mercer's office.
- **The memory split** (`design_whose_hand.md` §5): piece 1, the childhood, came from Grier; piece 2, the
  making, came from Sabin, who was given it *"to copy the method"*; piece 3, Cain, is the Chairman's.
- **Why there were so few units.** Kess, reading Wren's chip: everything was dressed back by hand, *"which is
  what you do when you're making eleven of a thing and not eleven thousand."*
- **The Rise** is Vance's half-built building: twenty floors going up, eight working. It has `atrium`,
  `the_rise_floor` and `sabin_lab`, and Wren worked there under cover during Whose Hand.
- **Decided at 0.2.3 for this release** (`design_the_hunt.md:255`): the transfer is temporary, her feeling
  travels with her, and in Vega's body she loses her own weapon.

---

## Part one — THE STUDY (two tracks side by side)

The transfer opens only when **Kess and Cain's three nights and Wren's first two unlocks** are done (her third
unlock comes later, in part five). Between study nights the player is in Wren's own
body in free play: every loop, person and place she already has keeps running.

### Kess and Cain — three nights at the Site
Each night Kess puts a little power back into one part of the shell and they watch what it does.

1. **The blade and the armour.** The forearm splits and a blade comes out on its own, and nearly takes Kess's
   hand. Cain puts his knife to the skin and it barely marks it. Whatever Vega was built for, it was not
   only bringing people in.
2. **The power cell and the signal.** Kess gives the shell a cell of its own and times how fast it drains. It
   drains fast, which gives the mission a clock and tells the player how long she has before she goes in.
   Then the signal: the moment the shell has power, it tries to call home. Kess muffles it just in time. Now
   they know two things: the company has never heard from Vega since the take, and if that signal ever gets
   out, the company will come straight to wherever she is.
3. **The way in.** The method is in Wren's head, from Sabin's piece: the memory of her own making. She walks
   Kess through it at the two cradles, piece by piece, while he works out how to do it with his hands. It's
   the hardest night for her, because she is reliving what was done to her so that it can be done again.
   Kess still has never put anybody back into anything. Cain is in the chair. The transfer is set for the
   next night.

### Wren — her own study, with a little grind
A repeatable activity at the Site: she reads what Vega recorded, because Vega never forgot anything. **Every
three sessions unlocks one new thing, nine sessions in all.**

1. **The weapons.** How the blade and the armour move, from inside Vega's own fights. She learns to use them
   as Vega did.
2. **The Rise.** The building as Vega saw it: the floors Wren never reached, the doors, the guard rotations,
   which lifts go where, and Sabin's lab. This is where she will start looking for the memory.
3. **Vance Tower.** *(Opens only after the Rise, in part four, tells her the memory is in the Tower.)* The
   Tower as Vega knew it: the units' quarters, the floors, the guards, and the route up to the Chairman's
   floor. This is the plan she takes in.

The transfer opens with all three nights and the first two unlocks. The third is part of the plan. Each
unlock pays off inside the company: she uses what she learned.

---

## Part two — THE LAST NIGHT

The night before. **She is afraid.** Of the cradle, of being put into the thing that hunted her, of not
coming back to her own body.

She and Cain lie together. **No sex.** He holds her and she lets him. It is the first quiet closeness between
them since the Site, where she learned he killed her father. Neither of them fixes that tonight. It is just
two people holding on.

This scene is the only warm one in the release and it should stay short.

---

## Part three — THE TRANSFER

Kess runs the lines. Her own body goes still in Marrow's cradle and Cain sits down beside it. She wakes up in
Vega.

**No sex in this body.** It is a machine. What's new is what it can do, and that **it feels.** Vega never
felt anything. The first thing Wren notices in the strongest body she has ever had is that she is still
afraid. The feeling came with her.

### What the Vega body has
From the game already:
1. **Stronger and faster than Wren.** She can kill a man with her bare hands.
2. **No pain.** Good in a fight, and the reason the body keeps going until it breaks.
3. **Perfect memory.** It records everything.
4. **Tracking.** Inside the company it reads the building like a map.
5. **The power cell drains fast.** This is the mission clock, and it's how she loses the last fight.

New in this release (LO, yes to all three):

6. **The arm blade.** It comes out of the forearm. This is her killing weapon inside the company.
7. **Armour** under the skin. Blades and bullets barely mark her.
8. **The company signal.** Doors open and cameras ignore her. Kess muffled its call home, but it is still
   the company's own signal, and the company can shut it off once they know something is wrong.

What she loses: **her own weapon**, the drain, which belongs to her own body. In here, none of the old ways
work.

---

## Part four — THE RISE: the search

Her first trip out in the new body. She walks into the Rise wearing the one face the company trusts on
sight. Nobody there is looking for anyone else; to every door and every guard she is Vega. *(Her old cover
plays no part: this is the new body, LO 2026-10-12.)*

She searches with what she learned from Vega's records: the floors, the doors, Sabin's lab. **The memory is
not here.** In Sabin's lab she finds where his piece came from, the record of her own making that the
Chairman gave him to copy: it came out of a vault in **Vance Tower**, on the Chairman's own floor. The third
piece is kept in the same place.

### The production floor
On the way out she passes the unfinished floors, and they aren't unfinished. **Rows of empty bodies.** A line
moving, building them many at a time.

This is what **Sabin** was paid for. Only a handful of units ever existed because each one was dressed back
by hand: eleven of a thing, not eleven thousand. Sabin was given the record of how Wren was made to copy the
method, and he solved it. The eleven thousand is in this room.

The bodies are empty, like Vega. They can't feel. That is the one thing the Chairman has been killing to get,
and the one thing nobody but Wren has.

**Sabin is on the floor.** He looks at "Vega" a second too long: the way she moves, the way she stops at the
rows. Noticing anomalies is his job. He does not learn that the transfer works, and he says nothing to her.
But after she leaves, he reports that Vega came back wrong, and **that is why Lyra and Nova are at the
Tower** when she gets there.

She does not kill him. No sex; this is one look and one line. She gets out clean.

---

## Part five — THE PLAN

Back at the Site, still in Vega's body. Her own body stays asleep in the cradle; Kess has never put anybody
back, and they don't spend that until the end.

- Kess recharges the cell.
- She reads the Tower out of Vega's records: the third unlock of her study.
- The three of them make the plan. She goes into the Tower alone, takes the memory out of the Chairman's
  vault, and **carries it to a meeting place** where Cain and Bastien will be waiting, by a set time.
- She tells them what she saw at the Rise: the line, the empty bodies. Now all of them know what the company
  is building.

*While she is in Vega's body, only the Site is open.* Every other screen in the game describes Wren's own
body, so free play waits until she is home. Between trips this is a short, closed stretch.

---

## Part six — VANCE TOWER: the memory

She walks back into the building that owned her. The face opens the doors up to the Chairman's floor, but not
the vault. The signal was never cleared for it.

**Getting the memory is hard.** She breaks in with the blade, guards die, and the alarm goes off. She takes
the memory. **She carries it out: a stored thing, not opened.** The memory is not in her yet. She has to get
it home.

---

## Part seven — THE RUN, and THE FIGHT

She runs for the meeting place, with the memory and the clock on her power cell.

**Lyra and Nova** are already in the Tower, because of Sabin's report. They know Vega, and to them Vega is
broken. Their orders never said to bring Vega in whole. Wren was the one the units were told to spare, and
nobody gave that order about Vega. They hold nothing back. The company shuts her signal off.

The body has no pain and keeps going, so it takes damage it should have stopped for. The power cell runs
low. She is losing, and she does not reach the meeting place.

---

## Part eight — THE SAVE

**Nobody called them.** Cain and Bastien come because **she is late.** She should have been at the meeting
place, she isn't, and they go to find her.

They bring Bastien's men. They have done this before: the take of Vega taught them **the seam at the base of
the spine**, and Lyra and Nova are the same build family. Lyra and Nova don't know it, because Vega never
reported back.

**Lyra and Nova are driven off, not killed.** They stay for later releases.

**Dace dies** getting her out: Bastien's main man, whose ten held the crew night. Bastien gets one line about
it, after. It should cost him.

Vega's body is wrecked. They carry it out with her inside, and the memory with her.

---

## Part nine — HOME, THE FLASHBACK, and CAIN

The order at the end is LO's (2026-10-12): **out of Vega, back into her own body, then the memory goes in.**

1. **Out of Vega.** Back at the Site, Kess does what he has never done: he takes her out of the wreck and
   puts her back into her own body in Marrow's cradle. Cain is still in the chair. She wakes in her own skin
   and feels everything again.
2. **The memory goes in.** Kess puts the third piece inside her, the same way the other two came to her. It
   **completes the memory**: the childhood (Grier's piece) and the making (Sabin's piece) finally join with
   the third.

### The flashback
**She gets everything back.** Who she was. What happened to her. That she was experimented on, **by her own
father, Marrow, and by Cain.** The man she loved was in the room while it was done. And the man in the chair
beside her, who killed her father, was one of the two who did it.

**And she loved him.** The memory shows that too, in full: **sex with Cain, explicit**: kissing, her mouth
on his cock, and all of it, the way it was between them before the company took it out of her (LO
2026-10-12). It's told loud and on the body, as a scene, not as fragments. Both truths come back at once:
what he did to her, and what they were.

That is why the Chairman kept this piece: it isn't only who she loved, it's what he did. He was holding it
for the day he needed her pointed at Cain. **It fails:** she gets the whole truth and still chooses Cain. The
Chairman's leash breaks in her hands (no kill, LO 2026-10-12).

### Then for real
She wakes with all of it, and Cain is in the room. **They do it for real**, now, in her own body: the first
time in the game she chooses him, knowing everything. It's explicit, and it stays on the body for its whole
length. What it means gets its own beat, after.

The scene has to make the choice legible. She doesn't forget what he did; she remembers loving him at the
same time, and she picks him anyway. That's what makes it land instead of jar.

**The end card:** she knows everything, and she has chosen Cain. The company is building an army of empty
bodies that only need one thing to fill them, the thing only she has. The wreck of Vega lies on Kess's table.

---

## Decided for 0.2.5 (not built here, but this release must not contradict it)

- **Two parts of the wreck go into Wren: the arm blade and the perfect memory** (never forgetting a fight).
  Strength and armour don't fit her half-human frame, which is why she stays herself. *Final pick is LO's at
  0.2.5; LO: "that will be decided in that features."*
- **The new parts run on what her body already runs on: the climax that fuels her weapon**
  (`design_book.md:51`). Her body has no power cell like Vega's. That keeps the upgrades tied to the sex
  loop instead of making it optional.

## Deferred — do NOT spend here

The Chairman on screen (she reaches his floor and his vault, never him) · stopping the production line ·
Sabin learning the transfer works · Lyra and Nova as people (they fight, they don't talk) · what comes
after she chooses Cain (the two of them, not a turn against him: there is no kill) · the other unstopped name on her
index · the Chairman's wife · the boss-immunity mystery (why the drain never worked on Mercer).

**Spent here, which 0.2.3 had deferred:** walking into the company, Vance Tower (and so the Spire), the third
piece.

---

## Sex in this release

**None in the machine body** (LO). The last night before the transfer is a cuddle, no sex.

**Two explicit scenes with Cain at the end** (LO 2026-10-12): the flashback, which is sex inside the memory
(kissing, blowjob, and all), and then sex for real, after she wakes. These are the first sex scenes between
Wren and Cain in the game. Everything else explicit stays in the free-play loops that already ship.

⚠️ **This spends something the design book reserved.** The book keeps her warmth for **Cain at the very end**
and frames the game's end as **kill-or-love** (`design_book.md:96`, `:354`). Choosing him here, with sex,
moves the "love" side forward to 0.2.4, by LO's call. **And there is no "kill" (LO 2026-10-12: "No kill.").**
Kill-or-love is closed as love: she will never be turned against Cain, by the Chairman or anyone else. The
book's kill-or-love framing has to be rewritten to match. Record the book change at the blueprint.

**Ceiling to sign:** Cain has no vocabulary/act ceiling row yet. Draft one at the blueprint (the flashback's
acts and the real scene's) for LO to sign, like the crew-night row in 0.2.3.

*Flag for the blueprint:* measure the explicit-share check (`gates.py:51`, 7.5%) against the release.

---

## Open calls — answered (LO, 2026-10-12)

1. **What the memory shows:** everything. Who she was, what happened, experimented on by her own father and
   by Cain. It completes the three pieces. → part nine.
2. **The building:** the memory is in **Vance Tower**; she searches **the Rise** first and finds out where it
   is there. → parts four and six.
3. **How Cain and Bastien come:** not by a call. They come because she is late to the meeting place.
   → parts five and eight.
4. **Her old cover:** plays no part; this is the new body. → part four.

### Left for the blueprint
- **The meeting place.** A real location that exists, between the Tower and the Reach (for example where the
  Spire's travel link meets the Reach). Pick it at the blueprint from the map.
- **The closed stretch while she is in Vega.** Only the Site is open between the Rise and the Tower. The
  blueprint has to seal travel cleanly and give every locked place a reason.
- **The explicit-share check**, as above.

---

## Next

Story signed (LO "Go ahead", 2026-10-12). Blueprint and Cain's ceiling row signed (LO "Signed continue",
2026-10-12), every default and the three changes as written. Building from `beat_0223`.

---

## BLUEPRINT (LO signed 2026-10-12: "Signed continue")

### Reconcile before this blueprint (done 2026-10-12)
- `merge_toml_phases.py games/vesper --validate`: OK. The merge now carries the dev shortcuts again, because the
  0.2.3.1 release merge had used `--no-dev`. The release merge drops them again.
- Drift check: every id-shaped canvas the ledger lists is in the merged TOML, except `ma_renner_anal`, which
  beat_0015 dropped on purpose and recorded at the time. No real drift.
- Ledger hygiene: `_active_beat` and the 0.2.3 `next_up` line were stale (they still said uncommitted). Both
  fixed.
- Explicit share, measured with `author-game-v2/scripts/gates.py vesper`: **12.5% of 561 repeatable beats**
  (floor 7.5%), and 63.6% of the 110 explicit beats are re-enterable (floor 40%). This release adds about 4
  non-explicit repeatable beats and two one-time explicit scenes, so both stay well above their floors. One
  FAIL there predates this release and is not touched by it (repeatable explicit media: 62 single clips that
  could be pools).

### Engine facts this rests on (read this session)
- **The Spire is sealed** since the 1a blowup (the zone-seal plus a backstop lock on `penthouse`,
  `1_metadata_and_locations.toml`). Vance Tower has `spire_plaza`, `atrium`, `penthouse` and `cradle`, but no
  Chairman's floor and no vault.
- **A run of one-time scenes at one place can play without a gap.** Each one exits to `the_site`, and the next
  one auto-fires on arrival. 0.2.3 already does this: take, then table, then cradles (beat_0222, LO liked it).
- **`max_triggers_per_day` on a repeatable canvas = N uses per in-game day**, re-arming at midnight. The first
  use is immediate. A window that crosses midnight lets one sitting fire twice, so the window must not cross
  midnight (verified at Vesper's Colm hub, rev 85).
- **One repeatable card per person per place and time window.** `activity_cain_trains` is Cain's card at the
  Site, so anything new he's in at the Site is a one-time scene or a group inside a solo card, never a second
  Cain card.
- **Presence on a one-time scene is an `npc_at_location` condition**; `requires_npc` does nothing on
  auto-fire.
- **Schedules today:** Cain is at `the_site` 21:00–23:59 and 00:00–03:00 (gated `the_site_open`). Kess is at
  `kess_berth` 10:00–22:00. Dace's only row needs `dace_met` is_false, so he has been off the map since the
  crew deal. Sabin is on `the_rise_floor` 08:00–11:00 and in `sabin_lab` 11:00–22:00.
- **Time only moves by click minutes.** There is no "skip to morning"; a night is a fixed minute cost.

### Three places the blueprint changes the signed story (all flip-able)
1. **She reads the Tower before the transfer, not after the Rise.** Vega lived in the Tower, so its floors are in
   her records whether or not anyone knows the memory is there. That way the third study unlock comes before
   the transfer, the Rise tells her *the memory is in the building she already knows*, and the plan is one
   scene. **What it buys:** no stretch where she walks around in Vega's body with every other place closed.
   From the transfer to the moment she's home, it's one unbroken run of scenes at the Site, the same way 0.2.3
   ran take, table and cradles. The closed stretch in part five goes away. *(If LO wants the Tower read to
   happen after the Rise, it needs a sealed-Site stretch: every exit from the Site locked behind a flag, which
   is the leak-prone pattern we've hit before.)*
2. **The Rise and the Tower trips are scenes, not map visits.** Each trip is one multi-node scene played from
   the Site. The Spire stays sealed, the Chairman's vault never becomes a place on the map, and nothing
   already shipped at the Rise has to learn about Vega's body. The scenes still carry real choices (which
   weapon, which way), but no fail state: losing to Lyra and Nova is the story.
3. **Lyra and Nova have no NPC entries.** They fight and they don't talk (deferred: Lyra and Nova as people), so
   they're images and prose inside the fight scene. They get proper entries in the release where they speak.

### The numbers (new state, all extend-only and safe for old saves)

| key | kind | range | what moves it | shown? |
|---|---|---|---|---|
| `vega_records` | trait | 0–9, clamped | +1 per session reading Vega's records | hidden; the quest card names the count and the next unlock (3 weapons, 6 the Rise, 9 the Tower) |

Flags, each set by one located one-time scene: `study_blade` · `study_signal` · `study_method` ·
`last_night_held` · `transferred` · `rise_searched` · `tower_planned` · `memory_taken` · `units_fought` ·
`dace_dead` · `back_in_body` · `memory_whole` · `cain_chosen`.

**Defaults (flip-able):** reading costs 60 minutes and 15 Charge, at most **2 sessions a day** (so the nine take
at least five days). Each study night costs 360 minutes, which carries the clock past Cain's window, so it's one
study night per night.

### People
- **Kess gets a second row: `the_site` 22:00–23:59**, gated `cradles_ready` is_true + `back_in_body` is_false.
  It starts after his berth row ends at 22:00, so he's never in two places, and it stays before midnight. It's
  needed so the study nights and the transfer are true about who's in the room.
- **Cain:** no change to his rows. After `cain_chosen` his Site card gets a new band (see "Truth sweep").
- **Dace:** no row to remove, because he's been off the map since the crew deal. His death is a truth sweep
  over the lines that speak of him in the present tense.
- **Sabin:** one look and one line inside `cap_the_rise`, speaking as `npc_sabin`. His rows don't change.
- **Lyra and Nova:** no entries (above). Media: `scenes/lyra_and_nova.jpg`.

### Part one — THE STUDY

| scene | kind | where | gate | sets | media |
|---|---|---|---|---|---|
| `activity_read_vega` | Wren-solo repeatable card, pri 3, `max_triggers_per_day = 2` | `the_site` | `cradles_ready` + `transferred` is_false | `vega_records` +1; costs 60 min + 15 Charge; four bands of result (0–2 / 3–5 / 6–8 / 9), and the band she just reached names what she now knows | `scenes/vega_records.jpg` |
| `cap_study_blade` | auto-fire one-shot, pri 11 | `the_site` | `cradles_ready` + Cain and Kess present | `study_blade`; 360 min | `scenes/study_the_blade.jpg` |
| `cap_study_signal` | auto-fire one-shot, pri 11 | `the_site` | `study_blade` + both present | `study_signal`; 360 min | `scenes/study_the_signal.jpg` |
| `cap_study_method` | auto-fire one-shot, pri 11 | `the_site` | `study_signal` + both present | `study_method`; 360 min. Her walking Kess through her own making, Cain in the chair | `scenes/study_the_method.jpg` |

### Part two — THE LAST NIGHT

| scene | kind | where | gate | sets | media |
|---|---|---|---|---|---|
| `cap_last_night` | auto-fire one-shot, pri 11 | `the_site` | `study_method` + `vega_records` gte 9 + Cain present | `last_night_held`; ends in the morning (540 min). She's afraid; Cain holds her; no sex | `scenes/last_night_cain.jpg` |

### Part three onward — THE RUN (one unbroken chain, each scene exits to `the_site`)
The first scene needs both men present. Every scene after it fires on arrival with no presence gate, because the
two men are in the scene before it. That's the beat_0222 pattern.

| # | scene | gate | sets | what happens | media |
|---|---|---|---|---|---|
| 1 | `cap_the_transfer` | `last_night_held` + Cain and Kess present | `transferred` | Kess runs the lines; her body goes still; she wakes in Vega and is still afraid. The body's weapons named once, as she feels them | `scenes/the_transfer.jpg`, `scenes/wren_wakes_in_vega.jpg` |
| 2 | `cap_the_rise` | `transferred` | `rise_searched` | in through the doors on Vega's face; the search; Sabin's lab gives up where his piece came from (the Chairman's vault, Vance Tower); the production floor; Sabin's look and line; out clean | `scenes/the_rise_search.jpg`, `scenes/the_production_floor.jpg`, `scenes/sabin_looks.jpg` |
| 3 | `cap_tower_plan` | `rise_searched` | `tower_planned` | back at the Site: what she saw (the line, the empty bodies), the route out of what she read, the meeting place and the hour; Kess recharges the cell | `scenes/the_tower_plan.jpg` |
| 4 | `cap_the_vault` | `tower_planned` | `memory_taken` | into the Tower; the face opens every door but one; the blade, guards dead, the alarm; the memory, carried out unopened | `scenes/vance_tower_vault.jpg`, `scenes/the_blade_in_the_tower.jpg` |
| 5 | `cap_lyra_and_nova` | `memory_taken` | `units_fought` | the run; Lyra and Nova; the signal goes dead; no pain, so the body takes what it shouldn't; the cell runs low; she doesn't reach the meeting place | `scenes/lyra_and_nova.jpg`, `scenes/vega_breaking.jpg` |
| 6 | `cap_dace_falls` | `units_fought` | `dace_dead` | nobody called them: she's late, so they came; Bastien's men; the seam; Lyra and Nova driven off; Dace dies getting her out; Bastien's one line | `scenes/the_seam_again.jpg`, `scenes/dace_falls.jpg` |
| 7 | `cap_back_in_body` | `dace_dead` | `back_in_body` | Kess takes her out of the wreck and puts her back, the first time he's put anybody back; Cain in the chair; she feels everything again; Kess puts the third piece in | `scenes/back_in_her_body.jpg` |
| 8 | `cap_the_whole_memory` | `back_in_body` | `memory_whole` | **explicit**: the flashback. Who she was, the experiments by Marrow and Cain, and loving him, with sex inside the memory (kissing, her mouth on him, and the rest) | `sex/flashback_cain_kiss_t4.webm`, `sex/flashback_cain_blowjob_t5.webm`, `sex/flashback_cain_fuck_t5.webm` |
| 9 | `cap_cain_for_real` | `memory_whole` | `cain_chosen` | **explicit**: she wakes, knows everything, chooses him; sex for real in her own body; the meaning in its own beat, after; end card | `sex/cain_for_real_kiss_t4.webm`, `sex/cain_for_real_fuck_t5.webm`, `sex/cain_for_real_finish_t5.webm` |

The explicit scenes are one-time, so each beat carries one file, not a pool (the pool rule: a one-time screen is
one file).

### After the release — what stands
- **`site_the_cradles`** gets bands for after `back_in_body`: Vega's shell gone to Kess's table, her own cradle
  empty again. Its comment *"IT STAYS TRUE ALL THE WAY TO 0.2.4: nothing is transferred"* is retired with it.
- **New `kess_the_wreck`**: Wren-solo repeatable card at `kess_berth`, gated `back_in_body`. The wreck of Vega on
  Kess's table, and Kess already looking at the arm. It sets up 0.2.5. Media `scenes/the_wreck_on_the_table.jpg`.
- **Free play continues** after the end card, in her own body, as it did after 0.2.3.

### Truth sweep (lines that become false, fixed in the same build)
- `amb_bastien_cot`: *"Dace is very good"* is present tense. It needs a `dace_dead` band. Its `cradles_ready` band
  (*"She is in Marrow's cradle, then. Good."*) needs an after-`back_in_body` band.
- Bastien's terminal card 26 and the crew lines (`cap_1a_close` card text, *"His men are back, ten of them,
  Dace's"*) are read against `dace_dead`.
- `activity_cain_trains`: the after-the-take band (*"the transfer is the next hard part"*) needs a band for after
  `transferred` and one for after `cain_chosen` (they're lovers now).
- **Story card L** stops being the end: it gets `study_blade` is_false so the new cards take over.
- Every Kess line that talks about Vega lying in the cradle is read against `back_in_body`.

### Quest cards (one live at a time, linear)
- **M, *The study*** — when `cradles_ready` + `last_night_held` is_false. Goals: the three nights (`study_blade`,
  `study_signal`, `study_method`) and the records (`vega_records` gte 9). Tip: Cain and Kess at the Site
  22:00–23:59; read the records at the Site, twice a day at most.
- **N, *The last night*** — when all four goals are met + `last_night_held` is_false. Tip: the Site, Cain there at
  night.
- **O, the end card** (terminal) — when `cain_chosen`. *"Chapter complete. The story continues in the next
  release."* It names what stands: the wreck on Kess's table, the army being built, Cain.
- No card for the run itself: it plays as one chain without a gap.

### Order guard
Night 1 → 2 → 3, and the records to 9 alongside them → last night → transfer → Rise → plan → vault → Lyra and
Nova → Dace → back in her body → the memory → Cain. Every scene reads the flag of the one before it, so nothing
can fire out of order on an old save.

### Ceiling row to sign: CAIN (drafted 2026-10-12)

| scene | who | what is on the page | vocabulary | held out |
|---|---|---|---|---|
| `cap_the_whole_memory` | Wren and Cain, inside the memory, before the company took it | kissing; her mouth on his cock; him going down on her; fucking, more than one position; finishes in her | the game's maximum: cock, cunt, tits, cum, fuck | anal; anything that makes the experiments themselves sexual (the experiments are told plainly, and the sex is the love, never the lab) |
| `cap_cain_for_real` | Wren and Cain, now, in her own body at the Site | kissing; oral both ways; fucking; finishes in her; a second time | the game's maximum | anal (an anal finish fires her weapon, and she would drain him) |

**Status:** SIGNED by LO, 2026-10-12.

### The design book (bounces up, built as a beat)
`design_book.md` still frames the game's end as **kill-or-love** (`:96`, `:354` and elsewhere). LO 2026-10-12:
**"No kill."** The book gets rewritten to match: Cain's row and the end become love, and she is never turned
against him. That's a document change only, built as the first beat so nothing written after it can contradict
it.

### Build order (one verified beat at a time; numbering continues from `beat_0222`)

| beat | what |
|---|---|
| `beat_0223` | design book: kill-or-love → love (LO "No kill.") |
| `beat_0224` | the numbers + Kess's Site row + `activity_read_vega` + quest card M |
| `beat_0225` | `cap_study_blade` |
| `beat_0226` | `cap_study_signal` |
| `beat_0227` | `cap_study_method` + quest card N |
| `beat_0228` | `cap_last_night` |
| `beat_0229` | `cap_the_transfer` + card L un-terminaled |
| `beat_0230` | `cap_the_rise` |
| `beat_0231` | `cap_tower_plan` |
| `beat_0232` | `cap_the_vault` |
| `beat_0233` | `cap_lyra_and_nova` |
| `beat_0234` | `cap_dace_falls` + the Dace truth sweep |
| `beat_0235` | `cap_back_in_body` |
| `beat_0236` | `cap_the_whole_memory` (only after the Cain ceiling row is signed) |
| `beat_0237` | `cap_cain_for_real` + end card O |
| `beat_0238` | what stands after: `site_the_cradles` bands, `kess_the_wreck`, the Cain and Kess truth sweep |
| `beat_0239` | `tests/check_the_transfer.py` (one section per beat, negative-tested) + `tests/live_the_transfer.py` (the whole chapter in a real browser) |

Each beat: merge, validate, package, the guard section for that beat, and `gates.py` for the register checks
(dialogue share on scenes with someone present; explicit beats staying on the body).

### Media: 25 slots, the harvest is LO's
19 images (`scenes/…`) and 6 explicit clips (`sex/…`), all named in the tables above. Every block
carries a description and search words. Nothing is downloaded by the build; it's LO's harvest.

### Calls in this blueprint LO can flip
1. The Tower read before the transfer (change 1 above). The alternative is a sealed-Site stretch.
2. The trips as scenes, not map visits (change 2).
3. Lyra and Nova with no entries (change 3).
4. Reading the records: 60 minutes, 15 Charge, twice a day.
5. Kess at the Site 22:00–23:59.
6. No repeatable Cain sex loop after `cain_chosen`. This release ends on the one real scene; a loop would be a
   0.2.5 call.
7. The names: `cap_dace_falls`, `kess_the_wreck`, and the rest.

---

# BUILT — 2026-10-12, rev 244–260, beats 0223–0239

Built beat by beat from the signed blueprint, with each beat merged, packaged `--dev` into `output_dev/`, and
guarded before the next one. Nothing is committed; the release build has not been made (LO's call).

## Where the build corrected the blueprint
- **Card L was converted in place into card M (the study)**, instead of getting a `study_blade is_false` gate.
  Story-Goals cards all render when they match, so a terminal L next to a live M would have said "Chapter
  complete" over the next chapter. Until end card O (beat_0237) there was no terminal story card, which was the true
  state mid-build.
- **Card N became card M's `ready_text`.** A `when` cannot say "not every goal is met", so a separate N would have
  stood next to M. The engine draws `ready_text` once every goal is met ("One more night as yourself…").
- **Kess got a portrait card at the Site, `activity_kess_site`** (not in the blueprint). gates.py found him DEAD
  there: his 22:00–23:59 row put his badge on the map with no card of his. It is banded on the study state and
  closes with his row.
- **The run's minutes were retuned after the live test.** An exit's minutes apply when the scene renders, so each
  scene's sidebar shows the clock after its own minutes. At 600 minutes the Rise rendered at 11:10, which is past
  Sabin's floor hours and puts him in his lab while she searches it. The final values are transfer 480, plan 720,
  fight 120 and save 210. Measured live:
  - the Rise renders at 09:10 (Sabin on the floor 08:00–11:00, his lab empty);
  - the fight at 01:19, before three;
  - the save at 04:49, after three, which is why they came.
- **Smaller corrections:**
  - The meeting place is **the Waterfront**, where the car up to the Spire waits.
  - The Chairman's floor has "no number on the panel" and is never placed above the penthouse, which is the
    Tower's top floor.
  - The making memory has no faces, so on night 3 Cain is silent and nothing explains why.
  - No year counts appear: Grier's nine years and Bastien's eleven do not agree.

## Older guards amended on purpose (each one caught a real, intended change)
- `check_the_hunt.py`:
  - Kess's schedule rows now include `the_site`.
  - The cradles_ready card is non-terminal, with at most one terminal story card.
  - Cain's card now leads with the `cain_chosen` band.
- `live_the_hunt.py` and `live_the_hunt_end.py`: after the cradles, the Quests page shows card M, not an end card.

## Measured
- **Guards and live suites:**
  - Merge OK, package green, all flag chains valid.
  - `check_the_transfer.py` (one section per beat) passes, and was negative-tested at §0224. The hunt, count and
    bunker guards pass. The cascade-order guard passes; the render-bucket guard's one hit (`react_renner_threat`)
    predates this release.
  - `live_the_transfer.py` passes: the whole chapter in a real browser, from 0.2.3's take through to end card O and
    what stands after, including the twice-a-day cap on the Site's own card list and the vault's "wait" branch.
  - `live_the_hunt`, `live_the_hunt_end`, `live_the_count`, `live_rings` and `live_cot_decision` all pass.
- **Register gates (gates.py, against the pre-release baseline):**
  - No new failing gate.
  - Explicit floor 12.4% of repeatable beats (floor 7.5%).
  - Explicit in repeatable 58.8% (floor 40%).
  - Somebody speaks 2.7:1 overall.
  - The cradles_ready latch flag is reported, but the row's `back_in_body` clause ends it.
- **Narration:dialogue per scene:**

  | scene | ratio | note |
  |---|---|---|
  | blade | 1.26 | |
  | signal | 0.94 | |
  | method | 1.03 | |
  | last night | 1.29 | |
  | transfer | 1.29 | |
  | Rise | 7.39 | mostly solo; the Sabin stretch is dialogue |
  | plan | 0.38 | |
  | vault | 6.78 | solo action with guard lines |
  | Lyra and Nova | — | silent, nobody to speak |
  | Dace | 1.69 | |
  | home | 1.55 | |
  | the memory | 2.77 | capstone with interior |
  | Cain | 1.82 | |

- **Leak check:** no cheat word in any changed file.

## Media — 25 slots, the harvest is LO's
- **19 images:**
  - `scenes/vega_records`, `study_the_blade`, `study_the_signal`, `study_the_method`
  - `scenes/last_night_cain`, `the_transfer`, `wren_wakes_in_vega`
  - `scenes/the_rise_search`, `the_production_floor`, `sabin_looks`, `the_tower_plan`
  - `scenes/the_blade_in_the_tower`, `vance_tower_vault`
  - `scenes/lyra_and_nova`, `vega_breaking`, `the_seam_again`, `dace_falls`
  - `scenes/back_in_her_body`, `the_wreck_on_the_table` (all `.jpg`)
- **6 clips:**
  - `sex/flashback_cain_kiss_t4`, `flashback_cain_blowjob_t5`, `flashback_cain_fuck_t5`
  - `sex/cain_for_real_kiss_t4`, `cain_for_real_fuck_t5`, `cain_for_real_finish_t5` (all `.webm`)
- Every block carries a description and search words.

## Open — LO's
1. Review and commit (nothing is committed).
2. The media harvest: the 25 slots above.
3. The release: version bump, new cheat words, guide chapters for 0.2.4, the build without `--dev` and `--debug`,
   the snapshot, then uploads and posts.
4. The flip-able calls listed in the blueprint, which all stand as built.
