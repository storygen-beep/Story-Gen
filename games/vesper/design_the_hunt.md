# Vesper — 0.2.3: HER FATHER'S HOUSE and THE HUNT

> Design record for **0.2.3**. Story level only. This is the review surface; the scene list with gates and
> placement (the blueprint) comes after LO signs the story off.
>
> **Status:** story agreed with LO in conversation, 2026-10-02 → 2026-10-03. Nothing built.
> LO's calls, verbatim where they were given:
> - *"First D, cain takes her to the place where marrow made them, this was the main scientist it was wren's
>   father himself. So she remembers his photo there. This gets her only a bit closer to cain not much."*
> - *"the face can be from her childhood memory, she says its her father."*
> - *"the other machine can start hunting her … she tries again and again to beat her, they are on a hunt in
>   the underworld itself. She can beat her with the fight or bastien the way he kidnapped wren earlier in the
>   game … but that would require him getting back to the strong men that he was."*
> - *"they can hide, but they want to get the next piece so the plan they have is to get one of the machine and
>   transfer wren to it … kill her, dismantle her. Transfer wren to her … she can now use that machine's power
>   and get in the company."*
> - The hunter is **Vega**. Her **feeling travels with her** into the machine, and the transfer is
>   **temporary**. She **learns at the site that Cain killed her father**. **0.2.3 = the site + the hunt**;
>   the transfer is **0.2.4**.

---

## Why

*Whose Hand* gave her a childhood memory with no face in it and a name, Vesper, in someone else's voice. The
Way Down and The Count were Bastien's chapters. The story has been waiting since on two things it planted and
never paid: **where she came from**, and **the company knowing she is alive** (the units' line at the raid).

This release pays both, and it sets up the climb to the third piece without opening the Spire.

---

## What already stands (shipped, and read)

- **`the_site` exists and is locked.** A greyed card off `underworld_strip`, gated on `the_site_open`, which
  nothing sets (`1_metadata_and_locations.toml:1228`). Its blocked message: *"Past the strip the city goes dark
  and deep, and that's where he is."* This release opens it.
- **The memory has no face.** Her own words to Cain: *"No face. I turned to look and there was nothing there.
  Not a blur, not a shadow. An absence with a person's shape in it"* (`5_scenes.toml:18214`). No shipped line
  says whose face it is, so the site can fill it without changing a word of an older release (LO, 2026-10-03:
  *"no changes to the older releases for the face"*).
- **She does not know Cain killed Marrow.** The backstory says he did, at Marrow's request (`design_book.md`
  World setup, iceberg 3–4). No scene in the game tells her.
- **Vega is planted and never used.** The opening line-up: *"Vega, Lyra, Nova. Chrome-perfect, hands at their
  sides, nothing moving behind their eyes"* (`2_one_shots.toml:30`); Mercer: *"Vega, Lyra, Nova run the hunt
  head-on. You're useless with a gun"* (`2_one_shots.toml:152`). Complete machines, no human base, no feeling
  (`design_book.md` Cast).
- **Bastien knows how to take a machine.** His crew took her with a bag, a knee in the back, *"hands that know
  exactly how much pressure a body takes"*, and someone who found *"the seam at the base of her spine"* and
  worked it until it gave (`5_scenes.toml`, `hunt_the_grab`). The room he kept her in still exists:
  `captive_room` + `captive_door`.
- **Bastien is coming back.** The Count ends with him counting money on her blanket, back in business from her
  bunk, with Rue at the House carrying his notes. He has money. He does not yet have his men.
- **Sabin's piece is "the making"** — the process itself, which the Chairman gave Sabin to copy the method
  (`design_whose_hand.md:180`). She carries it now. That is the method the transfer will use.
- **The fighting ladder tops out at 70** (`5_scenes.toml:19764`, the bunker's top gate).

---

## Part one — HER FATHER'S HOUSE

### The trip
Cain takes her past the strip to the site, the place where Marrow worked, a long way down and a long way
out. He doesn't say much on the way. He has been here before; she can tell from how he walks it.

### The photo
In the lab, among what the company didn't think worth taking, there is a photo of Marrow. She looks at it
and the hole in her memory fills in: the afternoon light, her hands too small for the knot, the person behind
her not fixing it, the hand on the back of her neck with the thumb along the seam that was not there yet, the
voice that said *Vesper, you have got all afternoon*. **The face that was missing is this face. It was him.
He was her father.** She says it out loud, and the scene must make the link plain: the photo, then the memory
replayed with his face in it, then her line naming him. The player should never have to work it out.

The shipped memory already supports this: *"the seam that is not there yet"* is a father touching the place
where he will later build into his own daughter.

So the man who built her was the man who raised her. He made his own daughter into a machine, made as a
companion for Cain.

### What Cain says
She asks how Marrow died. Cain tells her the truth, plainly and once: **he killed him, because Marrow asked
him to.** He doesn't defend it.

And there is the beat that stays with him. When she came back from *Whose Hand* and said "no face", Cain
hoped the face was his. That is why he asked *"You don't remember me at all?"* Here he finds out it was
never him. It was the man he killed.

### Where it leaves them
**Only a little closer.** She knows who she was and where she came from. She knows Cain was there. And she
knows he killed her father. She doesn't hate him, but she doesn't move toward him either. Cain, for his part,
has to watch her grieve a man he loved too and he killed.

### What she sees in the lab — the plant for 0.2.4
The equipment Marrow used is still there: the frame, the cradle, the lines. She doesn't know what it's for
yet. The player will.

### The trip has a cost
**The site is watched.** Going there trips something the company left behind, and the company finally sends
something after her. That is how the hunt begins: she caused it by going home.

### Sex in part one
**None between her and Cain.** The design book keeps the warmth between them for the very end, and this part
is grief. The part's job is story; it should stay short. *(LO can flip this.)*

---

## Part two — THE HUNT

### It opens with the attack (LO, 2026-10-03)
Part two starts the moment they leave the site. Vega is waiting. She hits them on the way back, and Cain and
Wren run, getting away only just, both badly damaged. That is the player's first sight of what Vega is, and the
first trip to Kess for repair.

### Vega comes into the underworld
A company unit doesn't knock. She walks down the strip in daylight. People get out of her way without knowing
why. She asks about Wren in places Wren has worked: the House, the market, the pit, the Undertow.

**Her orders are to bring Wren in whole.** She doesn't want to kill her. That is what keeps losing survivable.

### Why the weapon is no use
The weapon fires on a man's climax. Vega has none. Wren can't seduce her, drain her or command her. For the
first time in the game, the one thing that is hers doesn't work. She has to win another way.

### The loop — she tries again and again
**Where Vega finds her: the underworld streets** (LO, 2026-10-03). Never at the cot, never in a hideout. Out
on the strip and the lanes, between the places Wren goes, Vega can step out in front of her. They fight. Wren
loses. Vega comes again another day.

**What a loss costs (LO: *"she has to run off"* · *"lost day but not hideouts"*):** when Vega beats her, Wren
breaks off and runs. She gets away on her own, every time; nobody rescues her. **She loses the day:** she
spends it hiding until it's safe to come out. Her places all stay open; the cot, Bastien and her work are
still there the next morning. Never a game over. Each loss also teaches her one of Vega's habits.

**Vega damages her, and Kess repairs her** (LO, 2026-10-03). Every fight with Vega leaves damage in Wren's
body, and it stays until it is fixed. She goes to Kess at his berth, pays coin, and he repairs her over one or
more sessions. Badly damaged, she fights Vega worse, so the hunt has a rhythm: fight, lose, run, lose the day,
get repaired, try again. This is the same shape as the Salvage repair the game already ships (Kess's paid
sessions at the berth, `salvage_repair_hub`, 10 coin a session), on a new damage meter of its own; the old
`core_strain` keeps its meaning. The numbers are set in the blueprint.

This copies *The Leash*'s "three failures and a win" shape: each failure moves the story on.

### Vega — what she is (LO, 2026-10-03: "keep all")
Built on what the game already says about the units: complete machines, better hardware than Wren, nothing
inside (`design_book.md` Cast), and Mercer's line *"Vega, Lyra, Nova run the hunt head-on"*
(`2_one_shots.toml:152`).

**Her powers**
1. **Stronger and faster than Wren.** She can kill a man with her bare hands.
2. **She feels no pain.** Hurting her doesn't slow her; only real damage to her frame counts.
3. **She never forgets a fight.** She records everything, so a trick that worked once never works twice.
   Every attempt has to be different.
4. **She tracks.** She reads the underworld like a map. That is how she keeps finding Wren on the streets.
5. **The weapon and the emitter do nothing to her.** No human part, so nothing to arouse.
6. **She holds back on Wren.** Her orders are to bring Wren in whole. On men she holds nothing back.

**Her weak spots**
1. **She always makes the smart move.** No instinct, only calculation, so in the end she is predictable.
   Wren is half-human and can do the stupid, unexpected thing. The game's theme in one fight: the human part
   is the edge.
2. **She burns power fast.** At full strength she can only last so long before she has to slow down. That is
   what "wearing her down" means: Wren has to last long enough.
3. **The seam at the base of her spine.** Same build family as Wren, same seam. A hand on it and she goes
   down. That is how Bastien's men finish the take.
4. **She won't kill Wren.** So Wren can take risks Vega never will.

### How Wren learns to fight her
1. **Losses on the streets.** Each time Vega beats her, Wren learns one of her habits: how she opens, which
   way she cuts off escape, when she slows.
2. **Cain trains her** at night. He has fought the units before. The one rule he teaches: *"She'll always do
   the right thing. You have to do the wrong one."*
3. **Kess shows her the seam on her own body** while he repairs her. Now she knows exactly where it is on
   Vega.
4. **Pit fights** push her fighting past 70.

**What the take needs, all at once:** fighting high enough, enough of Vega's habits learned, her damage
repaired, and Bastien's men ready. Wren fights Vega until her power runs low, turns her, and the men take her
by the seam. Some of them die doing it. *(Numbers at the blueprint: likely a new counter for habits learned,
fed by losses and by Cain's training.)*

### Beating her takes both — the fight AND Bastien's men (LO, 2026-10-03)
Neither way works alone.

- **Wren alone can't finish it.** Even trained, she can only stand with Vega long enough to hurt her, not to
  bring her in.
- **Bastien's men alone can't do it either.** They caught Wren because Wren was easy to catch. Vega is not.
  She is physically stronger than any of them and can kill a man with her hands. Send the crew at her alone
  and she goes through them.

So it takes both:

**1. Wren learns to fight her** (see "How Wren learns to fight her" above). Cain's training gives him a
place in the hunt without making them closer; it is work, not warmth.

**2. Bastien gets his men back** (next section). Without the crew there is no one to close in.

**3. The take.** Wren draws Vega out and fights her, long enough and hard enough to wear her down. When Vega
is slowed, the men close in the way they once took Wren: a bag, a knee in the back, hands that know how much
pressure a body takes, and a man who knows where the seam is. Even then she is strong enough to cost them.
**Some of the men die in the take** (LO, yes). Vega can kill a man, and it shows, and it costs Bastien again
right after he got his men back. Bastien holds her in
the same room he kept Wren in.

### Bastien comes back to the man he was
This is the ladder (LO, 2026-10-03). Bastien has some money from The Count. What he doesn't have is his
place or his men. The Undertow, the bar his back room sat behind, was burned in the raid; Sol is still in it
most days with a shovel. His men scattered, and many of them died that night.

**1. Rebuild the bar.** The Undertow has to stand again before anyone will come back to it. Clearing it,
rebuilding the back, renovating the floor. It costs money, so Wren puts coin into it alongside Bastien's.
Each stage shows on the place itself: ash and tape, then bare walls, then a working bar.

**2. Hire the men back.** With the bar standing, Bastien offers pay. The men won't come: *why go back to that
bar, when so many men died there?* Money isn't enough.

**3. The main man.** One of them speaks for the rest. Wren talks to him. He'll bring about ten men back, and
he names the price: her, with all of them, at once.

**4. The night.** She pays it: one group scene, the men and her together, in the rebuilt bar. In the
morning they're Bastien's again.

As his crew comes back, Bastien changes at the cot: more himself, more the man who once owned the building,
more the man who once had her in that room. His loop gets harder as he gets stronger. *(This extends the
HIMSELF band The Count already ships.)*

**5. Ready.** With the bar standing and the men back, Bastien has a crew again. It still can't take Vega
without Wren; see "Beating her takes both" above.

### The end — the table
Vega ends up on Kess's table. Cain lays out the plan there, plainly:

They can keep hiding, but the third piece is inside the company, and they can't reach it as they are. So:
take one of the company's own machines, empty it, and put Wren inside. The method is in her own head now,
from Sabin's piece. The equipment is in her father's lab. Kess has the hands.

**Vega is killed and taken apart.** She shows nothing as it happens, because there is nothing in her to show.
Wren is the one who feels it.

The release ends with the body ready on the table and the way into the company open for the first time. The
locked door: **the transfer.**

---

## What this release adds to the story (no older release changes)

1. **The face in her childhood memory is Marrow's, her father's.** The shipped memory left the face blank;
   the site fills it. No line in any older release changes. **The third piece is unchanged:** the Chairman
   holds the memories with Cain in them.
2. **Marrow is her biological father.** The design book said her human origin "stays buried." This release
   unburies it, as LO's call.
3. **She knows Cain killed Marrow.** From the site onward, that is part of everything between them.

---

## Decided for 0.2.4 (not built here, but this release must not contradict it)

- **The transfer is temporary.** Her own body sleeps in Marrow's lab while she wears Vega's, and Cain watches
  over it. That is a real step of trust between them.
- **Her feeling travels with her.** It lives in her, not in her body. The machine body feels for the first
  time, which is exactly what the Chairman has been killing to achieve. If the company ever learns the
  transfer works, they won't need her body any more. They'll only need her.
- **The trade:** in Vega's body she loses her weapon, which belongs to her own body. She gains the unit's
  strength and the one face the company trusts on sight.

---

## Deferred — do NOT spend here

The transfer itself · walking into the company · the Chairman on screen · the Spire · the third piece ·
Lyra and Nova as people · who came back eight months after the program closed and sealed one page · the
other unstopped name on her index · the Chairman's wife.

---

## Ceiling row to sign — THE CREW NIGHT, Dace's ten (drafted at beat_0214)

| scene | who | what is on the page | vocabulary | held out |
|---|---|---|---|---|
| `cap_the_crew_night` | Wren and about ten of Bastien's old men, Dace first | group sex in the rebuilt bar after hours: stripped, oral (hands and mouth), from behind over the counter, turns, on the floor, two at once, finishes on and in her, a second round | the game's maximum: cock, cunt, tits, cum, fuck | anal (the anal finish fires her weapon); anything she has not said yes to (her yes opens the scene, in her own words, and Dace offers the no twice) |

**Status:** drafted, not signed. LO signs or changes it.

## LO's answers to the open calls (2026-10-03)

1. **No sex between Wren and Cain at the site.** Yes.
2. **A loss to Vega:** she runs off, on her own, every time, and loses the day. No hideouts are lost. Vega
   catches her on the underworld streets.
3. **Bastien's comeback:** not through the weapon. Rebuild and renovate the Undertow (money, hers too), offer
   the men pay, they refuse because so many died there, the main man brings about ten back for one night with
   her and all of them at once.
4. **The site is watched,** so going home is what brings Vega. Yes.
5. **Cain trains her for the fight route.** Yes.
6. **Beating Vega takes both** the fight and Bastien's men: Wren wears her down, the crew takes her. Neither
   works alone, because Vega is stronger than any man and can kill one. Some men die in the take (LO, yes).
7. **Part two opens with Vega's attack** as they leave the site; Cain and Wren run off badly damaged.
8. **Vega's powers, weak spots, and how Wren learns to fight her:** as written in "Vega — what she is". Keep all.

---

## BLUEPRINT (LO "go", 2026-10-03)

Proposed in conversation and agreed. LO, on the sex count: *"no on both. low sex scenes is fine here"* — so
Kess's repairs carry **no** test scene and the crew does **not** become a repeatable surface. The defaults
below that LO did not speak to are marked **(default — flip-able)**.

Engine facts this rests on, read this session:
- The underworld is a hub: every place hangs off `underworld_strip` ("The Underground"). Walking anywhere
  down there passes through it, so **"the streets" = `underworld_strip`**.
- A Lane-2 random scene is `trigger_mode = "random"` + `chance` + `is_repeatable`, capped by
  `max_triggers_per_day` (`engine-reference.md:99-105`).
- **There is no "skip to morning" effect.** Time only moves by click minutes (`time_progression_minutes`,
  `engine-reference.md:253`). Losing the day is a fixed jump; the game already uses 540 minutes in five places.
- **One repeatable card per person per time window** (the overlap warning the build prints for Kess today).
  So the repair is a **choice on `hub_kess_berth`**, never a second Kess card.
- The existing drills stop at fighting 70 (`3_activities.toml:640-700`, the `gte 50 lt 70` band).
- `days_since_flag` fails **closed** when a flag has no `set_day` (`5_scenes.toml:6644`, v2.py:3979). Spine gates
  here never use it; "the next morning" is the clock (`time_of_day`) instead.
- `requires_npc` is inert on auto-fire; presence on a one-time scene is an `npc_at_location` condition
  (`engine-reference.md:112`, `:152`).
- Cain has **no schedule at all** today. Bastien sits at `the_cot` around the clock (plus `bastien_backroom`
  20:00–24:00). Kess is at `kess_berth` 10:00–22:00. Sol is at `underworld_bar` 10:00–24:00.

### The numbers (new state — all extend-only, safe for old saves)

| key | kind | range | what moves it | shown? |
|---|---|---|---|---|
| `vega_damage` | trait | 0–100, clamped | +60 at the ambush · +35 per street loss · −25 per Kess repair | **yes**, a banded sidebar row (Fine / Hurt / Badly hurt) so the player knows when to see Kess |
| `vega_habits` | trait | 0–4, clamped | +1 per street loss | hidden; the quest card names how many she has |
| `undertow_build` | trait | 0–3 | +1 per paid rebuild stage | hidden; the bar's own card shows the stage |
| `fighting` | existing trait | now to **85** | Cain's training, +1 a session, only from 70 to 85 | existing row |

Flags (all set by a located one-time scene): `site_offered` · `the_site_open` (the existing lock) ·
`marrow_known` · `site_ambushed` (the hunt is on) · `seam_known` · `crew_asked` · `undertow_open` (bar rebuilt) ·
`crew_refused` · `dace_met` · `crew_back` · `vega_taken` · `vega_dismantled`.

**The numbers (default — flip-able):** fighting 85 · 4 habits · 540 minutes lost per defeat · +35 damage per
fight · −25 per repair at 10 coin · rebuild stages 40 / 60 / 80 coin · street-encounter chance 0.35, once a day.

### New people
- **`npc_vega`** — portrait, **no schedule** (she appears only inside her own scenes, like Cain does today).
  Dialogue as `npc_vega`. Media: `portraits/vega.jpg` — chrome-perfect, a woman-shaped unit, nothing behind the
  eyes (matches the opening line-up, `2_one_shots.toml:30`).
- **`npc_dace`** — the main man of Bastien's old crew **(name: default — flip-able)**. Schedule:
  `underworld_pit` 18:00–24:00, where the scattered crew drinks now. One-time scenes only; no hub, no loop.
  Media: `portraits/dace.jpg`.
- **Cain gets a schedule:** `the_site` 21:00–03:00 once `the_site_open` is set **(default — flip-able)**. His
  first standing place in the game.

### Part one — HER FATHER'S HOUSE (4 one-time scenes)

| # | id | kind | where | fires when | sets | media |
|---|---|---|---|---|---|---|
| 1 | `cap_cain_comes` | auto-fire one-shot, pri 11 | `the_cot` | `bastien_back` is_true + `time_of_day` morning + `site_offered` is_false | `site_offered`, `the_site_open`; exits to `the_site` | reuses Cain's portrait |
| 2 | `cap_the_site` | auto-fire one-shot, pri 11, **Tier-3 cascade** (the chapter's big written scene) | `the_site` | `site_offered` + `marrow_known` is_false | `marrow_known` | `scenes/the_site_lab.jpg` (a dead lab, equipment under dust) · `scenes/marrow_photo.jpg` (a man's photo, middle-aged, kind) |
| 3 | `cap_the_ambush` | auto-fire one-shot, pri 11 (*built located, see beat_0209*) | `underworld_strip`, on the walk back | `marrow_known` + `site_ambushed` is_false | `site_ambushed`; `vega_damage` = 60; exits to `kess_berth` | `scenes/vega_ambush.jpg` |
| 4 | `cap_kess_seam` | auto-fire one-shot, pri 10 | `kess_berth` | `site_ambushed` + `seam_known` is_false + Kess present (`npc_at_location`) | `seam_known`; first repair free (`vega_damage` −25) | reuses Kess |

**#2, in order:** the lab · the photo · the memory replayed **with his face in it** (the afternoon, the knot,
the hand, the thumb on the seam that was not there yet, *"Vesper, you have got all afternoon"*) · her line,
out loud: it was him, her father · she asks how he died · Cain: he killed him, because Marrow asked · Cain
learns the face was never his · the equipment, seen and not explained. No sex (LO).

**#1's lock:** `the_site`'s existing `blocked_message` keeps telling the truth until #1 fires; from then on the
card is open. A player who walks out of #1 without going still finds the Site open on the strip.

### Part two — THE HUNT (repeatable)

| id | kind | where | fires when | does | media |
|---|---|---|---|---|---|
| `rand_vega_street` | **Lane-2 random**, chance 0.35, `max_triggers_per_day` 1 | `underworld_strip` | `site_ambushed` + `vega_taken` is_false | the fight; she **always loses** (the take is the only win); `vega_damage` +35, `vega_habits` +1, exit `time_progression_minutes` 540 to `the_cot`. **Four bands on `vega_habits`** (0 / 1 / 2 / 3+), each a different fight and a different habit learned: how she opens · which side she cuts off · when she slows · that she will not finish Wren | `scenes/vega_street_t1.jpg` … `_t4.jpg`, one per band (one asset, one block) |
| repair choice on `hub_kess_berth` | choice, repeatable | `kess_berth` 10:00–22:00 | `vega_damage` gte 1 | 10 coin, 60 min, `vega_damage` −25 | reuses Kess's |
| `activity_cain_trains` | Lane-1 portrait hub, repeatable | `the_site` 21:00–03:00 | `the_site_open` + `fighting` gte 70 + `vega_taken` is_false | 15 energy, 120 min, `fighting` +1 (to 85, clamped). First session carries the rule, once: *"She'll always do the right thing. You have to do the wrong one."* Below 70 he sends her back to the drills | `scenes/cain_training.jpg` |

**Why she always loses on the street:** the design says Wren alone can only hurt Vega, never bring her in. A
street fight she could win would skip Bastien's half. Losing is the content; the habits are the progress.

**Badly hurt:** at `vega_damage` gte 60 the street scene's band reads as a rout (she barely lands a hand) and
the take's choice stays greyed. Damage never blocks anything else.

### Bastien's comeback (one-time steps, in order)

| # | id | kind | where | fires when | sets | media |
|---|---|---|---|---|---|---|
| B1 | node in `amb_bastien_cot` | hub choice into a hub node, one-time | `the_cot` | `site_ambushed` + `crew_asked` is_false | `crew_asked` | reuses |
| B2 | `activity_rebuild_undertow` | repeatable card, three exclusive stage bands on `undertow_build` | `underworld_bar` (a non-NPC card, so it never collides with Sol's hub) | `crew_asked` + `undertow_build` lt 3 | 40 / 60 / 80 coin, 240 min each, `undertow_build` +1; stage 3 also sets `undertow_open` | `scenes/undertow_rebuild_1.jpg` / `_2` / `_3` — ash and tape, bare walls, a working bar |
| B3 | `cap_crew_refuses` | auto-fire one-shot | `underworld_bar` | `undertow_open` + `crew_refused` is_false | `crew_refused` — Bastien's offer, the men's *"why go back there, so many died there"* | `scenes/undertow_reopened.jpg` |
| B4 | `cap_dace_price` | auto-fire one-shot | `underworld_pit` | `crew_refused` + `dace_met` is_false + Dace present | `dace_met` — he will bring about ten; the price is her, with all of them at once | `portraits/dace.jpg` |
| B5 | `cap_the_crew_night` | auto-fire one-shot, pri 11, **Tier-3, the release's explicit capstone** | `underworld_bar` after hours (22:00+) | `dace_met` + `crew_back` is_false | `crew_back` | `sex/crew_night_t5.webm` (group, ~10 men, a bar after hours) — one file, a one-time screen |
| B6 | new top band on `loop_bastien_cot` | band inside the existing loop | `the_cot` | `crew_back` is_true | — his loop gets harder: the man who owned the building | `sex/bastien_cot_owner_t5.webm`, **one file on the intro** (*built: the intro plays once a session*) |

**Where the crew died (prose truth, found at beat_0206):** the shipped raid empties the bar before the units
arrive and shows no body on that floor; Bastien says *"Three of them came down the strip."* So the men died on
the strip, and the refusal is *why go back to the Undertow, after what came down the strip for it*, never
"they died in the bar".

**The Undertow's look:** the location's description is static, so the stage shows on the bar's own card (B2)
as banded text, and Sol's hub gains one line per stage. Sol is in the fiction already, shovelling.

### The take and the table (one-time)

| id | kind | where | fires when | sets | media |
|---|---|---|---|---|---|
| choice "Draw her out." on `underworld_strip_hub` | choice, `show_when_locked` with a voiced `locked_text` | `underworld_strip` | `fighting` gte 85 + `vega_habits` gte 4 + `vega_damage` lt 30 + `crew_back` + `seam_known` | routes into `cap_the_take` | — |
| `cap_the_take` | triggerless canvas, **Tier-3 cascade** | `underworld_strip`, then `captive_room` | reached only from the choice | `vega_taken`; teleports to `captive_room` (Bastien holds her where he held Wren) | `scenes/the_take.jpg` · `scenes/vega_in_the_room.jpg` |
| `cap_the_table` | auto-fire one-shot, pri 11 | `kess_berth` | `vega_taken` + `vega_dismantled` is_false + Kess present | `vega_dismantled` — Cain's plan, said plainly; Vega killed and taken apart; she shows nothing, Wren feels it | `scenes/kess_table_vega.jpg` |

**`cap_the_take`, in order:** she draws Vega out on ground she chose · the long fight, Wren doing the wrong
move every time Vega does the right one · Vega's power running low · the men closing · **men dying** (LO: yes)
· the seam · the bag · the Room.

**The locked choice's voice (default — flip-able):** *"Not yet. She has to know how Vega moves, be good enough
to stand with her, be in one piece, and have Bastien's men behind her."* The engine appends the number.

### Quest cards (one live at a time, linear)
- **H** (0.2.2's end card) loses `terminal` and its *"That is where this build ends"* tip — the same two-step
  edit The Count did to the card before it.
- **I** — *Cain is waiting* · goal `marrow_known` · when `site_offered` + `marrow_known` is_false.
- **J** — *She's hunting you* · goals: habits learned (`vega_habits` 4), fighting 85, damage repaired, crew back
  · when `site_ambushed` + `vega_taken` is_false. One card for the whole hunt, because the take needs all of
  it at once.
- **J1–J4** — Bastien's section: the bar (`undertow_build` 3) · the men (`crew_refused`) · Dace (`dace_met`) ·
  the night (`crew_back`), each live only while it's the next step.
- **K** — *The body on the table* · when `vega_taken` + `vega_dismantled` is_false.
- **L — the end card**, terminal: when `vega_dismantled`. Names what is standing: Bastien and his crew,
  Cain at the Site at night, Renner, Grier, Sabin, the House and the pit; and the door — the transfer.

### What stands after the release
Bastien's loop at the cot, now with the owner band · Cain's training at the Site (it closes on `vega_taken`;
his place stays) · Kess's repair choice (harmless at 0 damage) · everything that stood after 0.2.2.

### Media — 13 new slots
`portraits/vega.jpg`, `portraits/dace.jpg`, `scenes/the_site_lab.jpg`, `scenes/marrow_photo.jpg`,
`scenes/vega_ambush.jpg`, `scenes/vega_street_t1..t4.jpg` (4), `scenes/cain_training.jpg`,
`scenes/undertow_rebuild_1..3.jpg` (3), `scenes/undertow_reopened.jpg`, `scenes/the_take.jpg`,
`scenes/vega_in_the_room.jpg`, `scenes/kess_table_vega.jpg`, `sex/crew_night_t5.webm`,
`sex/bastien_cot_owner_t5` (pool 4). Every block carries `description` + `search_queries`. The harvest is
LO's to run.

### Order guard (auto-fire is not order-safe on its own)
Every one-time scene above is banded on the flag before it and `is_false` on its own, so none can fire early:
#1 → #2 → #3 → #4, B1 → B3 → B4 → B5, take → table. The two tracks (the hunt and Bastien's comeback) run in
parallel after #3 and meet only at the take's choice.

### Build order — one verified beat at a time (numbering continues from `beat_0205`)

| beat | writes |
|---|---|
| `beat_0206` | **BUILT 2026-10-03.** state + seams: the new traits, `npc_vega`, `npc_dace`, the damage sidebar row, the dev jump, `tests/check_the_hunt.py` red first. *Moved out, by the game's whole-amendment rule: Cain's schedule row to `beat_0211`, Dace's to `beat_0213`, card H's edit to `beat_0207`.* |
| `beat_0207` | **BUILT 2026-10-03.** #1 `cap_cain_comes` + card H's two-step edit + card I. *Gate tightened from the blueprint: also `days_since_flag bastien_back gte 1`, so it can never fire in the same breath as Counting again.* |
| `beat_0208` | **BUILT 2026-10-04.** #2 `cap_the_site` (Tier-3, 14 beats). *Written calls: she speaks the memory aloud as it returns; Cain did not know she was the daughter ("a girl at school in the north"); he tells only how and why Marrow died.* |
| `beat_0209` | **BUILT 2026-10-04.** #3 the ambush + #4 the seam and the repair choice on Kess's card + card J0 "Get to Kess". *The ambush is a located auto-fire on the strip, not chained off the Site: its flag is read by triggers, which a scene with no location cannot set legally.* |
| `beat_0210` | **BUILT 2026-10-04.** `rand_vega_street` + card J. *Five habit bands, not four (the 4+ band keeps the text true once she knows it all); five media slots. The cheat page's fighting cap went 70→85: the build refused 70 against the new 85 gate (LO's rev-227 stealth precedent).* |
| `beat_0211` | **BUILT 2026-10-04.** `activity_cain_trains` + fighting 70→85 + Cain's schedule rows at `the_site` (21:00–03:00, when the Site is open). *Below 70 and at 85 the training choice is absent and his line says why (lock-as-prose).* |
| `beat_0212` | **BUILT 2026-10-04.** B1 + B2, the rebuild, + Bastien cards 19–21. *Stage order: cleared → floor and counter → back wall and open, so the burned back room is fixed last and Colm's shipped lines stay true through stage 2 (his card, his loop intro and Sol's card all gained a band per stage). The ruin crawl closes when the clearing starts (flip-able). Sol learns whose money it is at stage 1.* |
| `beat_0213` | **BUILT 2026-10-04.** B3 + B4, the refusal and Dace + Dace's pit row (when-gated on the refusal) + Bastien cards 22–23. *Bastien is not in the bar: she makes his offer (his location stays secret). The refusal waits a day after opening, in the evening.* |
| `beat_0214` | **BUILT 2026-10-04.** B5, the crew night (Tier-3, 8 explicit beats) + card 24 + card J's crew goal. *Dace's pit row now ends at his scene (the scoreboard found it dead after).* |
| `beat_0215` | **BUILT 2026-10-04.** B6, Bastien's owner band (first in all four loop screens) + a crew-back band on his card. *The clip is one file on the intro, not a pool (the intro plays once a session).* |
| `beat_0216` | **BUILT 2026-10-04.** the take (Tier-3), as its own card `activity_draw_her_out` on the Underground (the blueprint's host card holds no choices) + Bastien card 25 + dev jump "ready for the take". *The Room is narrated, not entered (its door never opens); the greyed text names the action (a locked choice shows its text, not its label).* |
| `beat_0217` | **BUILT 2026-10-04.** the table + card K + end card L (the only terminal story card) + Bastien's closing card 26. *Cain says the temporary transfer as a plan; the feeling going with her is kept for 0.2.4.* |
| `beat_0218` | media blocks pass (descriptions + queries), guard green, live playthrough probe |

### Calls in this blueprint LO can flip
0. *(beat_0212)* The ruin crawl closes when the clearing starts; a player who never finished it loses its last bands.
1. The numbers (table above).
2. Dace's name.
3. Cain at the Site 21:00–03:00.
4. She always loses on the street; the take is the only win.
5. The damage row is the one number shown in the sidebar.
6. The locked choice's wording.

---

# BUILT — 2026-10-04, rev 240, beats 0206–0218

LO, before bed: *"Go Beat by Beat Until each beat is done (hold on to the media harvest at the end)… After each beat do a
thorough review on it."* Every beat was written test-first (`tests/check_the_hunt.py`, one section per beat, red then
green), built, probed in a real browser, and run against all six Vesper tests before the next one started. Nothing is
committed; LO commits.

## Where the build corrected the blueprint

| beat | blueprint said | built | why |
|---|---|---|---|
| 0206 | Cain's and Dace's rows, card H's edit here | rows at 0211 / 0213, H's edit at 0207 | a row badges a map card in every save from the moment it exists; "this build ends" stayed true until card I existed |
| 0207 | fire on bastien_back + morning | + `days_since_flag bastien_back gte 1` | otherwise it fires in the same breath as Counting again |
| 0209 | ambush chained off the Site's exit | a located auto-fire on the strip | its flag is read by triggers; a triggerless setter fails the flag-chain check |
| 0210 | four habit bands | five | at 4 habits the fourth band's text would lie |
| 0210 | — | cheat page fighting cap 70 → 85 | the build refused cap 70 against the new 85 gate; LO's rev-227 stealth precedent |
| 0212 | cleared / rebuilt / renovated | cleared / floor and counter / back wall and open | the burned back room is fixed last, so Colm's shipped lines stay true through stage 2 |
| 0214 | Dace's row stays | ends at `dace_met` | the scoreboard found it dead after his scene |
| 0215 | owner pool, 4 clips | one file on the intro | the intro plays once a session (LO's pool rule) |
| 0216 | a choice on `underworld_strip_hub` | its own card, `activity_draw_her_out` | that card is the single-exit "Exit Underworld" card and holds no choices |
| 0216 | port into the Room | the Room narrated | `captive_room`'s door never opens; a port would seal her in |

## LO's amendment — beat_0219 (2026-10-04, rev 241)

LO: *"who brought them there. Bastien should first get to know that the bar has been rebuilt, bastien still cant go
there but there has to be something."* — and: *"she carries it to Rue."* Between the rebuild and the men:
1. **"Tell him the bar is open."** — a one-time choice on Bastien's cot card. He tears a page out of his ledger and
   writes the names of his old crew, crossing out the ones who were on the strip that night. *"Take this to Rue.
   Nobody else… Not whose money. Not where I am."*
2. **Rue takes the list** at the House (`cap_rue_takes_the_list`): the girls tell every man through the door that the
   Undertow is open, the old crew is wanted, the money is good. *"Tomorrow night, they'll be at the counter."*
3. **The men come the next evening** (`cap_crew_refuses`, now gated on `crew_called`), and their first line answers
   her word: *"Rue said he wants us back. Rue said a lot of things."*

New flags `crew_list_held`, `crew_called`; Bastien cards 22a / 22b / 22 re-gated; all five dev jumps updated.

## LO's asks — beats 0220 and 0221 (2026-10-04, rev 242)

- **The plan (`cap_the_plan`, at the cot, the day after the crew night).** Cain comes; the three of them make the
  plan the take then plays: Bastien *where* (the strip at night, Dace's men in the stalls and doorways), Cain *how*
  (alone first, past the minute, the wrong thing; the men not until she is slow), Wren *the end* (the seam),
  Bastien *after* (the bag, his Room), Cain *then* (Kess). "Draw her out." now needs it.
- **The shell in the cradle (`cap_the_cradles`, at the Site, at night).** The release's last scene: Vega's empty shell
  laid in the second cradle beside the empty one waiting for her; Kess runs the lines; Cain sits by the empty
  cradle. *"Not tonight."* Her last thought: *"Two cradles. Now she knows why."* It stops one breath before the
  transfer on purpose — free play continues after the end card and every surface still describes Wren's body. The
  transfer is 0.2.4. End card L now follows this scene; card K2 points to it (Cain's hours).

## Media — 29 slots, all missing, the harvest is LO's

Portraits: `portraits/vega.jpg`, `portraits/dace.jpg`. Scenes: `scenes/the_site_lab.jpg`, `scenes/marrow_photo.jpg`,
`scenes/vega_ambush.jpg`, `scenes/vega_street_t1..t5.jpg`, `scenes/cain_training.jpg`, `scenes/undertow_rebuild_1..3.jpg`,
`scenes/undertow_reopened.jpg`, `scenes/the_take.jpg`, `scenes/vega_in_the_room.jpg`, `scenes/kess_table_vega.jpg`, `scenes/the_two_cradles.jpg` (beat_0221).
Clips (one file each): the crew night's eight, one per act beat (`sex/crew_night_t5.webm` on the knees beat, plus `sex/crew_night_strip_t5`, `_counter_t5`, `_turns_t5`, `_floor_t5`, `_finish_t5`, `_second_t5`, `_after_t5` — added 2026-10-04 at LO's ask), `sex/bastien_cot_owner_t5.webm`, `sex/colm_rebuilt_t4.webm`. Every
scene and clip block carries `description` + `search_queries`.

## Measured

- Whole chunk, end to end, in a real browser: `dev_jump_hunt_start` → end card L through real places and choices, 0 JS
  errors, about 60 game days (15 of street losses, 15 nights with Cain).
- `gates.py` against HEAD: the same 27 FAIL gates before and after; no new failing gate. Explicit floor 12.6% (floor 7.5%).
- Every 0.2.3 spoken screen at or under 2.14:1 narration:dialogue, measured per visit by the guard.

## Open — LO's

1. Commit (nothing is committed).
2. The media harvest (above).
3. Sign the crew-night ceiling row (above).
4. The paid guide: 0.2.3 chapters, and the fighting chapter's new gate at 85.
5. Release: version bump and the publish build (drop `--dev` / `--debug`).
6. The flip-able calls listed in this file.
7. Pre-existing, found and left alone: `mercer_end_table` has no raid gate (Mercer holds court in the burned bar since
   0.1.9); `underworld_bar`'s static description has been false since the raid (true again once it reopens).

## Next

LO reviews and commits; then the media harvest.
