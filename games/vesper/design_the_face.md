# Vesper — Locked Design: THE FACE (Act 2 · 1c)

> **What this doc is.** The authoritative design for the chapter after *The Leash* — the chunk the shipped
> 0.1.8 end card promises the player without naming him (`5_scenes.toml:10702`: *"There's a man who came
> through the far door of that cell a year ago, in a hurry, and wouldn't say why he cared, and he doesn't
> have a name yet — he's the next chapter"*). It **supersedes** the shelf file's own restore instructions
> (`games/vesper/shelf/bastien_present_day.toml`, header §"TO RESTORE AT 0.1.9"), which describe a paste
> plus three reversals. That instruction was written under a leash that no longer exists and is wrong in
> its premise; what actually survives the shelf is itemised at §7.
>
> **Status:** ✅ **DESIGN LOCKED 2026-08-16** · ✅ **BUILT 2026-08-16, beats 0094–0110, revs 145–160**
> (0110 = the post-build audit; three defects found and fixed — see **§21**).
> The chapter is content-complete at 179 canvases / 28 locations and every beat is `validated` in the
> ledger. **The release is not cuttable yet** — every explicit media slot is empty and find-media has not
> run. Four things came out different from the design below; all four are recorded in **§20 AS BUILT**
> rather than being edited back into the sections they contradict.
>
> **Provenance.** Locked with LO across one design conversation, 2026-08-16. Four shapes I proposed were
> **reversed by LO and are recorded here as rejected**, because each is tempting and would come back:
>
> 1. *Bastien sold her file to an anonymous buyer for cash.* This is what the shelved
>    `bastien_drain_canvas` actually says — *"Never got a name. Money came through three hands."* LO
>    reversed it: Bastien collects Vance documents **for Cain**, and the money trade is his cover. LO is
>    right and the shelf drifted: the design book's own casting brief has read *"Bastien — docks dealer,
>    **Cain's supply line**"* since Step 3, with *"Bastien's alignment with Cain"* listed as the saved
>    bombshell. The shelf spent the bombshell on a payday.
> 2. *Cain put the chip in her.* I asserted this from `design_book.md:144` (*"Left the chip for her"*).
>    **The built game says otherwise and the built game wins.** What Cain does in `captivity_cain` is
>    re-seat her **drain** — *"her weapon back in her spine"*. The chip is company hardware: Kess finds it
>    *"wired deeper than the rest of you — under the core, not in it. Older, too"* (`salvage_chip_snag`),
>    and when it comes out it opens the seal on her Vance file because *"whoever built one built the other.
>    Same hand"* (`cap_extraction`). LO caught this. The Step-1 intent was never built and is retired here.
> 3. *Cain stays off-page; she gets his name off a document.* Rejected by LO — Cain appears, in person, at
>    the raid. My objection was that the reunion gets spent in a firefight and that she ends the release
>    being carried out by a man again, which is what happened in the cell. LO's shape answers both: Cain
>    **fails** at everything he came for, and the release ends with her holding a weapon on him.
> 4. *She pitches herself to Bastien as a woman who will do anything for money.* Reversed to a job at the
>    bar. LO's instinct was the bar; my objection to the "anything for money" pitch stands and is recorded
>    at §5 — it is the most ordinary offer in that district, it duplicates The House, and it takes the
>    door-search scene's charge away.
>
> **Engine claims.** Reused verbatim from shipped systems (the `entry_from` / `auto_exit = false`
> nav-invisible interior, `[[npcs.schedules]]` → portrait hub, the triggerless sex loop + finisher + drain
> canvas rig, the banded `[group]` chain, the coin economy, the `[[clothing]]` cover + `player_portrait`
> outfit rule, quest-card tiers). Two claims marked **⚠️ verify at build**: whether a clothing-change
> surface can live on a canvas rather than the engine-injected rack, and whether a nav card can be added to
> a location that shipped with `auto_exit = false` without tripping the list-every-location fallback.

---

## 1. What this chapter is (the fantasy)

For two acts her motive was the company's. The Leash ended that — *"nothing in you answers to anybody"* —
and left the game with no engine. She has no owner, no handler, no order, and nothing to do.

**This is the chapter where she wants something and has to pay for it.**

The want is small and it is entirely hers: she has read her own page and she still does not know who
sealed it. The programme closed, and eight months later a hand on none of the sign-offs came back and shut
one page — hers. Nobody assigned her that question. Nobody will thank her for answering it.

**The verb is: she takes a job and earns her way through a door.** Distinct from every verb on the roster
— seduce-in (Renner) · scheme-and-serve (Marsh) · she-is-taken (the cell) · supplicant-at-the-bench
(Salvage) · belief-lever (Calloway) · the cold underworld use (Colm) · keep-a-mark-warm (The Leash). Here
she is **staff**: a new hire on a bar floor with no leverage, working up. The promotion **is** the
seduction, and it is his call every rung.

Underneath it, a second verb: **she waits.** She is not hunting Cain. She is stationed where he turns up.

**The charge lives in a double blindness.** She goes to work in a bar owned by the man who kept her in a
cell, and he does not know her, because she is wearing a face she bought. And the reason she had to buy
one is that the whole district quietly closed against her — on Cain's word, to protect her, which she
reads as the world turning its back. Every person she meets is being kind to her in a way that looks
exactly like rejection.

**And the win is a trap, again.** She gets the answer, and getting it puts three machines through the
door and a man on the floor. The release ends with her in a room she was invited into, holding a weapon on
the one person alive who knows her real name, and hearing him say it.

---

## 2. Starting state (the shipped 0.1.8 end-state)

- `leash_cut` + `file_read` true. The chip is **out and left on Kess's bench** — `cap_extraction` has her
  walk out with the file and never touch the chip (*"She does not touch it. Two years of her life is on
  the bench and it is a grey speck."*).
- Home is `kess_berth` (`berth_home`). The upkeep is the feed line: the 10-coin tier of
  `activity_kess_cot` gives +100 Charge, advances the day 540 min, reloads **drain and emitter**, and sets
  `feed_line_days = 3`.
- Reachable: the Reach (`the_waterfront`, `the_anchor`, `renner_depot`, `renner_burned_yard`,
  `kess_berth`) and the underworld (`underworld_gate`, `_strip`, `_brothel`, `_pit`, `_market`,
  `underworld_bar`, `mercer_room`). **The Spire is sealed** by the 1a close — `penthouse`, `atrium`,
  `wren_floor`, `wren_room`, `cradle`, `docs_department` are all route-cut.
- Standing cast: Kess (berth, 10:00–22:00) · Mercer (the Lockup, 23:00–08:00, drained, arc badged
  complete) · Sol (Undertow, 10:00–23:59, no arc, unused) · Colm (Undertow, 19:00–23:59) · Rue and Marsh
  (The House) · Renner (depot/anchor, arc badged complete).
- **She cannot change clothes.** The only wardrobe rack is the engine-injected one at `wren_room`, inside
  the sealed Spire. She is still wearing `company_grays` — Vance company issue, `initial = true`, and the
  player portrait's default image — months after she stopped working for Vance.
- Weapons: `equipped_weapon` 1 = drain, 2 = emitter (`0_systems_spec.toml:231-235`). **One core, one
  weapon** — the game says so on the page: *"One core, one weapon — it feeds the drain inside her or the
  thing in her hand, never both at once."*
- The emitter is **not** a gun. It is an arousal field: *"Whoever's in reach goes stupid with it inside a
  breath — pupils blown, breath ragged, the gun forgotten in a slack hand."* Nobody gets hurt.
- ⚠️ **`hub_kess_berth` is stale.** Its one always-available rung is *"Ask how the work's going,"* and
  every band on the canvas crosses `feed_line_days` × `part_held` × `mercer_attempts`. **No band reads
  `leash_cut`.** After the chip comes out, he answers about a job that finished. Beat 2 repairs this.

---

## 3. The three tests any beat here must survive

1. **Does it survive her not being ordered to do it?** Every beat in this chapter has to be motivated by
   something she wants. The moment a beat leans on an assignment, it belongs to the old game.
2. **Does the double blindness hold?** He does not know who she is; she does not know why the district
   shut. A beat that lets either slip early spends the chapter's whole engine.
3. **Is it on the body, or is it about the body?** The heat pass is the release's structural debt (§11).
   Any explicit beat whose last sentence is about what the moment *means* has pivoted and scores zero.

---

## 4. The cast

| Who | Role this chapter | State |
|---|---|---|
| **Kess** | Opens the chapter. Has had the chip on his bench since she left it there and has poked at it, because he cannot help himself. Tells her what a ship-breaker can and refuses to guess the rest. **No arc change; no exposure to the raid.** | built |
| **Sol** | **Promoted from set-dressing to the man who hires her.** A fully-built NPC with a 14-beat hub and no arc — *"Bring him a dead man's name and he knows who ran it and where the survivor still turns up."* He runs the floor, trains her, and does not know her in the bought face. | built, unused |
| **Bastien** | The spine. **He owns the Undertow.** Keeps the back room 20:00–23:59, every day. Does not know the new girl is his old property. | shelved |
| **Colm** | Drinks there nightly and has slept with Wren. **Does not see through the face** (LO's call). Open: whether he reacts to a stranger getting the back room he used to have. | built |
| **Cain** | Off-page until the raid. He put the word out to leave Wren alone — which is why the district shuts on her and why he has never once approached her himself. **First and only appearance is the last scene.** | new |
| **Vega · Lyra · Nova** | The raid. Planted in the opening scene of the game and never used since: *"Vega, Lyra, Nova run the hunt head-on. You're useless with a gun — but you're the one asset I have that a man wants to keep close"* (`2_one_shots.toml:97`). | planted |
| **Mercer** | Untouched. Still at the Lockup, still pouring, still doesn't know. | built |

**Deliberately absent — do not spend:** the Chairman · the Spire · the lab scientist · `the_site` · the
other names on her index · Bastien's fate (§10).

### Bastien owns the Undertow — and the game already left the hole

Three shipped lines, none of which needed changing:

- The location: *"It runs cleaner than a place this deep has any right to, and **it plainly belongs to
  someone; nobody says who.**"* (`1_metadata_and_locations.toml:982`)
- Sol, in narration: *"He's outlasted every owner this place has had — and it's had a few, though **the
  one it answers to now never shows his face.**"* (`5_scenes.toml:9580`)
- Sol, aloud: *"Bar's owned by somebody now who never comes down to look at it. Suits me. An owner you
  never see is an owner who never asks questions you can't answer."* (`5_scenes.toml:9618`)

**What Sol knows:** he knows Bastien as a man who uses the back room. He has no idea Bastien holds the
deed. That keeps both shipped lines literally true and gives her something to find out.

---

## 5. The bar — the ladder

Four rungs, each one his decision, each more exposed. The same shape that worked on Renner (hired cheap →
noticed → the office), transposed onto a location she already visits every night.

| Rung | Surface | What it is |
|---|---|---|
| 1 | **The floor** | Glasses, tables, invisible. Repeatable paid work. **Pays less than The House.** |
| 2 | **The counter** | Sol trains her on the taps. She is where everything gets said. |
| 3 | **The floor, in less** | His call, relayed through Sol. Public, semi-sexual, repeatable. |
| 4 | **The back room** | Serving him directly, through the door with no handle on the bar side. |

**Why not "she'll do anything for money."** LO's first pitch, and it is the right flavour in the wrong
place. Four reasons it is rejected as the *entrance*: (i) it is the most ordinary offer in that district
and Bastien has heard it a hundred times — it puts her in the queue, not the room; (ii) it duplicates
`underworld_brothel_work`, which already exists and pays better; (iii) it takes away his best quality —
he is an ownership man, and the charge is him deciding week by week that he owns a bit more of a woman
who came in to work, which requires that she came in to *work*; (iv) it defuses the door search, which
lands because she is staff and he is establishing that he may search staff anyway. **She can absolutely
tease — as leverage once she is inside, never as the pitch at the door.**

**Why she takes a worse-paying job.** Because it puts her ten feet from a door. Say it once, in her own
voice, and never again. It is the beat where the player learns she has stopped chasing coin.

**What the face costs her.** Sol has decided he likes Wren — *"mostly,"* in his own shipped line. Now he
is polite to her the way a man is polite to new staff. The one person down there who liked her does not
know her. Play it once. Do not underline it.

---

## 6. The spine

1. **Kess and the chip.** It has sat on his bench. It is old — older than the rest of her — and
   company-made, the same hand as the seal on her file. Past that he is out of his depth; he breaks ships,
   and he says so. The answer is in the documents, and the documents were going to Bastien.
2. **Every door shuts.** She asks around the Reach as herself. Sol is polite and useless. Colm forgets
   things on purpose. Rue has nothing. The market will not sell her a name. Nobody explains.
3. **She buys a face.** She earns the coin, buys an identity at the black market — a place whose own
   description already reads *"weapons, gear, and people, penned at the far end like the rest of the
   stock"* — and changes at the cot. She stops being Wren.
4. **Sol hires her.** Floor work.
5. **Bastien notices**, from a chair aimed at that door, four hours a night.
6. **The climb.** Counter, then less, then through the door.
7. **The back room.** The search. The hub. The loop.
8. **The drain.** §8.
9. **She waits, works, and buys a taser.** §9.
10. **The night.** The raid, the overheard argument, the taser, the mole, the run, the units' line.
11. **The lab.** *"Now put down the weapon, Wren."* **End of release.**
12. **After.** She walks out. Two new things on the map.

---

## 7. Bastien — what survives the shelf

`games/vesper/shelf/bastien_present_day.toml` is 1,274 lines. Its header describes the restore as a paste
plus three reversals. **That is wrong**, because it assumes she arrives as Wren with a leash on. Itemised:

| Shelved canvas | Verdict |
|---|---|
| `cap_bastien_walks_in` | **CUT.** Its entire premise is that he finds her and calls her by the file Mercer keeps her under. He is now avoiding her on Cain's word, and she arrives in a face he has never seen. The prose cannot be salvaged; the scene is replaced by rung 2 (he notices a new girl). |
| `bastien_door_search` | **KEEP — structure and prose survive intact.** Re-band only: its three routes were `controller_seated` × `stealth`, and re-cut to **`taser_held` × `stealth`**. Stronger than the original, because now the search has something real to find. |
| `hub_bastien` | **KEEP, re-band.** Bands were `controller_through` + `leash_cut is_false`; re-band on the promotion rung and whether she has drained him. |
| `loop_bastien_backroom` | **KEEP the rig, REWRITE the prose.** This is the heat pass (§11) and the release's largest single beat. |
| `loop_bastien_finisher` | **KEEP, re-cut exits** onto the new state. |
| `bastien_drain_canvas` | **REWRITE the payload.** See §8. |
| `kess_seat_controller` | **DELETE.** Orphan — it existed only to beat the door search, and the controller thread closed at `leash_cut`. |
| `bastien_backroom` (location) | **KEEP unchanged until the raid.** Nav-invisible by design: no `entry_from` **and** `auto_exit = false`. Both halves are load-bearing — dropping `entry_from` alone leaves an empty nav grid, which trips the list-every-location fallback and lets the player walk from his back room to the Spire. |
| `npc_bastien` schedule row | **KEEP** — `bastien_backroom`, all days, 20:00–23:59, *"keeping the back room."* |
| Quest cards K / L | **REWRITE.** |

⚠️ **Do not give Bastien a schedule row at `underworld_bar`.** The in-room portrait card is canvas-gated
(`v2.py:4998-5008`) but the nav-card badge is **not** (`getNpcsPresentAtLocation`, `v2.py:4773`), so a
public row parks his face on the Undertow card for every player — including one who is mid-Act-1 and
currently being kidnapped by him. The back room's lack of a nav card is what solves this, and it is why
the door search must remain the only route in.

### The rhythm the schedules already impose

Kess keeps 10:00–22:00. Bastien keeps 20:00–23:59. They share two hours and the berth-to-bar trip eats
them. So the chapter splits into **days at the berth and the market, nights at the bar**, without our
inventing a clock. This is already true in the build; do not add a second one.

---

## 8. The drain — the new payload

Played as Q&A **in his own dialogue**, not narrated — the control-canvas carriage rule, executed properly
for the first time at `cap_first_fire` (six of her questions against thirteen of his answers, and the
reason that canvas holds the best narration-to-dialogue ratio in the game). Target the same shape.

What he gives up:

- The paper trade is real and it is his **cover**. The money is not why.
- **Cain is why.** He has been feeding him Vance technical documents for years.
- **Cain is an early model — one of the first, and weak.** He cannot go at Vance as he is. He has been
  rebuilding himself out of what Bastien brings him.
- **Nobody knows where he lives.** Bastien least of all. He stays under.
- **But he comes here whenever he likes.** ⚠️ *This is the line that keeps the chapter alive after the
  drain* — it is why she goes on working a bar she has already emptied of secrets.
- He has known for a year exactly who came through his far door and took her out of that cell.
- He still does not know **why Cain wanted that one.**

⚠️ **Cain is not named on the page here.** Bastien can describe a friend, an arrangement and a reason
without handing over a name; the name lands in Cain's own scene, where it is worth something. Her one
interior beat reaches for the four words that came through the wall of the cell and still cannot hold
them — which keeps `captivity_cain`'s shipped closing line true (*"four words she cannot hold, and cannot
stop reaching for"*) instead of quietly retconning it.

⚠️ **The captivity argument now reads better, not worse.** In `captivity_cain` she hears two men through
a wall: Bastien, *"flat, unhurried, reasonable"*, and a furious voice she has never heard. The one word of
Bastien's that reaches her is *"an ownership word, said the way you'd say the price of a thing."* Under
LO's canon that is two friends falling out over her — Cain saying give her to me, Bastien naming a price.
Nothing in the shipped scene needs touching.

---

## 9. The night

**The weapon problem, and why it is hers.** She has an emitter. She cannot bring it: one core, one weapon,
and she needs the drain live for Bastien — and company hardware does not survive a pat-down from a man
who checks the seam under the arm. So she buys a taser at the market. Cheap, anonymous, the kind of junk
anyone carries. **It runs off nothing.** That is the point mechanically (it does not compete with the
drain) and the point dramatically: when the night comes, she has nothing *because of a choice she made
earlier that evening.*

**The sequence.**

1. She is on shift. The attack starts.
2. Cain is there — he came for Bastien, not for her.
3. She overhears them. **Nothing expository** (LO's steer): *"Cain, you're late."* The shape of two men
   who know each other, mid-crisis. It is enough for her to know who he is.
4. Bastien tries to move her out of the way.
5. **She tasers him**, because she needs Cain in the room and Bastien is between them.
6. Cain sees the mole on her neck and knows her. He cannot save Bastien now. He takes her.
7. **They run**, and the units say the thing that tells her the company knows she is alive.
8. **The lab.** She still has the taser on him, which is why the line works.
9. *"Now put down the weapon, Wren."* End of release.

**Did Cain know?** He knew a stranger had been working Bastien. He had **no idea it was her.** That is why
the mole lands the way it does, and it is the only reading in which his year of keeping the district off
her is not simply incompetence.

**Why the mole and not the face.** He does not recognise her face — he recognises her body. That is more
intimate, more unsettling, and it tells the player he was close to her once, without a word of backstory.

**Cain fails at everything he came for.** He does not save Bastien, he does not save the place, and he
does not get the documents. He gets one person out, and it is the one he was not there for. That is the
version of this scene that does not cost the arc: she ends the release armed, standing, and asking.

---

## 10. THE SECRET — Bastien is not dead

They took him. He is being taken apart in a room somewhere for what he knows about Cain's supply chain.
**The player must not learn this until the next release.** Three rules, not optional:

- **Never state that he is dead.** Not in narration, not on the Quests page, not in a tip. A stated fact
  later withdrawn is a cheat and players are right to hate it.
- **Let her assume it.** She tasers him, the room goes to hell, Cain hauls her out, and the last thing she
  sees is Bastien on the floor. She assumes. Everyone assumes. The game never confirms.
- **Leave exactly one quiet detail:** no body is ever found in the wreckage. Said once, in passing, never
  underlined.

**This is what makes the taser matter.** He was down and could not run. That is *why* they got him. She
believes she watched a man die; what she actually did was hand him over.

⚠️ **Second secret, same rule:** Cain already holds the useful documents. Not stated this release.

---

## 11. THE HEAT PASS — non-negotiable

`loop_bastien_backroom` must ship as **the hottest repeatable surface in the game.** Bastien was shelved
at rev 141 precisely because his surfaces never got the pass revs 138–140 gave Mercer.

**The measurement, whole game, on `gates.py`:**

```
explicit floor          7.0% of 558 beats carry 3+ explicit words   (floor 7.5)
explicit in repeatable  20.5% of 39 explicit beats are re-enterable (floor 50.0)
traversal heat          9/26 locations carry a cycling explicit pool (floor 60)
```

**Per canvas, and this is the real number:** every repeatable sex loop in the game scores **0 or 1** hot
beats — Colm's back room 0/10, Renner's office 0/8, Calloway 0/8, `mercer_serve` 0/7, the brothel 1/7. The
best in the game is `loop_mercer_lockup` at 2/15, and that one *received* the pass. `mercer_drain_canvas`
scores **0 in 54 beats**, entered off an anal finish. Against that, the one-shot `cap_owner_print` scores
8/28. The heat is in content the player sees once; the surfaces they re-enter are cold.

**The defect in the game's own prose.** Colm's anal pose is the entire node:

> *Bent over the stacked cases with his cock in her ass, his hands white-knuckled on her hips. He's
> forgotten the door, the room, the job — everything but the fact that she let him.*

One sentence of act, then a sentence about what it means. Renner's is worse — half of it is a rules
explanation (*"This is the act that hands her the keys"*). Post-pass Mercer runs eight beats that stay on
the body the whole way and give the meaning its own beat afterwards.

**Targets for every pose node in Bastien's loop:**

- **3–5 beats per pose**, not one paragraph. He starts, it changes, it escalates, he finishes.
- **3+ frozen-list words per beat.**
- **Every beat ends on the act.** Interiority gets its own beat, after. Read the last sentence: if it is
  about what the moment means rather than what is happening, it has pivoted.
- **He talks while he does it.** Bastien has the strongest ownership voice in the game already.
- **~35–40 words per beat, flat.** Escalation is beat *count*. A pose page is re-opened 4–6 times a visit
  and the measured house size is video plus one ~36-word paragraph.

**Scope: Bastien only** (LO's call). Colm, Renner and Calloway stay cold and are logged as debt.

---

## 12. Register & ceilings — two rows owed

Bastien's row is signed (declared rev 62, re-spec'd rev 64): *maximum from the first scene, hot and
degrading, full crude, ownership-as-curiosity underneath.* **That row was written for a captive in a
cell.** Two clauses are owed before a hot beat is written, and nothing hot ships without them:

**(a) Bastien outside the cell, on a woman he does not own.** He does not know she is his old property,
so the cataloguing subtext has nothing to attach to. What is left is a man who owns the building and takes
what walks into it, unhurried, because nobody has told him no in his own bar. **Full crude stands.** The
degradation turns **proprietary rather than jeering** — she is staff, and he is establishing that staff is
a category he owns.

**(b) The bar floor — a new light row.** Rungs 1–3 are public, semi-sexual and repeatable: exposure and
handling, not sex. Un-crude at rungs 1–2; crude only where a hand actually lands. The game has never
written this register and it must be declared before it is spent. **Open: how far rungs 3 and 4 go in
public, in front of Sol and Colm and a room of men.**

**Cain** — no sexual content this chapter, so N/A on the vocabulary ceiling. His **voice** still needs a
spec: the design book reserves warmth for him alone, and this is its first spend.

---

## 13. Systems

| System | What | Notes |
|---|---|---|
| **Wardrobe at the cot** | A change-clothes surface at `kess_berth`. | **A blocker, not a nicety** — the only rack is the engine-injected one at `wren_room`, inside the sealed Spire, so she currently cannot change clothes at all. ⚠️ verify at build whether a canvas can do this or whether the rack has to be re-homed. |
| **The bought face** | A new `[[clothing]]` cover in the `dress` slot + a new `type` + a matching `[[player_portrait.outfits]]` rule + portrait image. | The build warns if a type has no rule. Precedents: `cover_dockhand` (type `cover`), `cover_analyst` (type `cover_analyst`). Gate content on the **item id**, not the type. |
| **The new default outfit** | Company grays retired for something civilian. | **⚠️ Touches shipped content — LO asked to mark it and brainstorm separately when we reach it.** Grays are `initial = true` and are the portrait's `default_image`. |
| **The taser** | An **item**, not a third `equipped_weapon` value. | Keeps it off the one-core-one-weapon axis, which is the whole design point. `taser_held` gates a door-search band and the raid. |
| **Bar work** | Repeatable paid work at `underworld_bar`, paying under The House. | Copy the shape of `underworld_brothel_work`. |
| **The lab** | New location; entered by canvas, exited by canvas. | Needs **both** no `entry_from` **and** `auto_exit = false`, per the `bastien_backroom` precedent. |
| **The burned back room** | `bastien_backroom` post-raid: re-skinned, **gains a nav card** off `underworld_bar`, becomes a small crawl. | The one thing left to do after the credits (§15). ⚠️ verify at build. |

---

## 14. Engine realities (verified in this repo, and each has bitten before)

- `conditions` must carry `version = "1.0"` or the engine returns true — the gate **fails open**, with no
  build error.
- **Adjacent `[group]` blocks merge into one if/elseif chain.** Two ladders on one node means one chain and
  a dead second.
- **Auto-fire hard-refuses a repeatable canvas** (`v2.py:4454`). Anything repeating is triggerless or a link.
- **Exit-block effects fire on render; choice effects fire on click.** State belonging to a decision rides
  the choice.
- **`requires_npc` is inert on the auto-fire path** — presence gating needs an `npc_at_location` clause.
- **Trait conditions compare a trait to a literal only** (`v2.py:3948`). No trait-to-trait form; derive a bit.
- **Schedule rows carry no conditions** and resolve first-match-wins in declaration order.
- **A triggerless canvas sets traits, not flags** — the flag-chain validator hard-fails a flag whose only
  setter has no location.
- **`[group]` blocks are display-only** and carry no effects.
- **Quest spine:** any capstone that closes the last live Story-Goal card ships its replacement in the same
  beat, or the page goes blank. **Exactly one card in the game names the build boundary**; moving it is a
  two-step edit and the check is a grep of the whole table from both sides, never a read of the card in
  front of you. Card M holds it now, with `terminal_text`, and both will need re-cutting.
- **Media: one asset, one block.** Never reuse a `file` or `pool_dir` across blocks. Anything repeatable and
  explicit is a **pool** (`files = [...]`), never a fixed single clip.
- **Edit by canvas span, never by a bare label index.** Rev 136 wrote one capstone's payload into another
  because they shared a beat label, and the build stayed green.

---

## 15. The ending, and what is left open

**The release ends inside the lab, on the line.** LO's call, and it is the right last beat.

The consequence is that the story finishes with nothing new to do — the same defect 0.1.8 has, where
`cap_extraction` sets two flags and opens no standing content. The mitigation, agreed:

- **She walks out of the lab freely.** Cain lets her; he has been leaving her alone for a year. The next
  release picks up immediately after, in the same scene.
- **The units take the useful documents.** What is left scattered in the burned back room is the junk paper
  Bastien sold for cash — mostly worthless, but one or two pieces carry names that match the index on her
  own page. That is the next release's material, generated for free.
- So the map ends the release with **two** new things on it: a burned room she can crawl, and a lab she has
  been inside once and cannot get back into yet.

---

## 16. Build sequence — one verified increment per beat

Each beat = build + targeted live suite + ledger entry. Full 17-suite run **once** at the end (10–15 min).

| # | Beat | Ships |
|---|---|---|
| 1 | **Systems + geography** | Wardrobe at the cot · the bought-face clothing item + portrait rule · `taser_held` · the lab location · new traits and flags declared. |
| 2 | **Kess opens the chapter** | The chip on the bench; what he found, what he will not guess. Re-band `hub_kess_berth` off the parts loop. Story-Goal card N. |
| 3 | **The wall** | Three or four refusals across built surfaces. Nobody explains. |
| 4 | **The face** | The black-market purchase · the change at the cot · the first walk into the Undertow as a stranger, and Sol not knowing her. |
| 5 | **Hired** | Sol's hire scene + `activity_bar_work`, rung 1. |
| 6 | **Noticed** | Bastien notices from the back room (auto-fire capstone). Rung 2. |
| 7 | **The climb** | Rungs 3 and 4. |
| 8 | **The door** | `bastien_door_search` restored, re-banded on `taser_held` × `stealth`. `hub_bastien` restored and re-banded. |
| 9 | **The loop — the heat pass** | `loop_bastien_backroom` + `loop_bastien_finisher` rewritten at the crude floor. **The release's largest beat.** |
| 10 | **The drain** | `bastien_drain_canvas` rewritten. New payload. The warm-tap repeat. |
| 11 | **The wait + the weapon** | The taser purchase; the one-core-one-weapon consequence stated on the page; the reason to keep working the bar. |
| 12 | **The night** | The raid · the overheard argument · the taser · the mole · the units' line. |
| 13 | **The lab** | The walk, the room, the line, the exit. |
| 14 | **After** | The burned back room as a crawl · the Quests page read end to end, both tiers · the boundary card moved. |
| 15 | **Media pass** | `find-media` for every new slot. Pools, not single clips, on anything repeatable. |
| 16 | **Clean ship** | No `--dev`, no `--debug`. Free and paid builds, portal deploy, release archive. |

---

## 17. Open items — decisions still owed

1. **Ceiling signatures (a) and (b), §12.** Blocking for beats 6–10. Nothing hot is written until signed.
2. **The bar ladder's exposure line.** How far rungs 3 and 4 go in public. Sets row (b)'s ceiling.
3. **Does Colm react?** He does not see through the face (settled), but a stranger is getting the back room
   he used to have. One scene, or nothing?
4. **The overheard argument.** LO's steer is *"Cain, you're late"* and nothing expository. Needs its beat.
5. **The new default outfit.** Marked for separate brainstorm; touches shipped content.
6. **Nights between the drain and the raid.** Long enough that the loop gets used, short enough that the
   wait does not go slack.
7. **Kess's exposure.** No change this release — confirmed deliberate, logged here so it is a decision and
   not an oversight.

---

## 18. Reserved — do NOT spend

**Cain's lab beyond the one room** · the **Chairman** · the **Spire** · **`the_site`** (still the one
read-never-set flag in the game) · the **other names on her index** · **Bastien's survival** (§10) ·
**Cain already holding the documents** (§10) · the **units' individual characters** — they are three
machines and a line, not a cast, this release.

---

## 19. What this supersedes

- The shelf file's **"TO RESTORE AT 0.1.9"** header instructions (`shelf/bastien_present_day.toml`) — the
  paste-plus-three-reversals restore assumed a leash that no longer exists. §7 replaces it.
- `design_book.md:144`'s **"Left the chip for her"** — Step-1 intent, never built; the chip is company
  hardware and `captivity_cain` gives Cain the drain instead. Retired.
- The shelved `bastien_drain_canvas` payload — the anonymous buyer, the three hands, and the *"same man"*
  realisation. Replaced by §8.

---

## 20. AS BUILT (beats 0094–0109, revs 145–159)

Every beat is `validated` in the ledger. The chapter is content-complete at **179 canvases / 28 locations**.
Four things came out different from the design above, and each is recorded here rather than quietly
retconned into the sections it contradicts.

### Amendment 1 — §8 said Cain would not be named. He is.

The clause was written before LO's canon change was carried all the way through. The *shelved* Bastien could
withhold the name honestly, because he genuinely did not have it — a middleman paid through three hands who
never saw the buyer's face. Under LO's canon Bastien is Cain's **supply line of eleven years** and knows the
name the way a man knows his oldest customer, and **a drained man cannot be evasive** — that is the whole
premise of the weapon, established across three chapters. Withholding would have broken the mechanism to
protect a reveal.

Spending it is also the better trade. She was built and pointed at that name, so it lands on the one person
it means most to, and it collapses three men into one: the buyer of her paperwork, the man who carried her
out of the cell, and her target. The release's last line does not need it, because the shock in the lab is
not *who he is* — it is that **he knows her**.

### Amendment 2 — she recognises him, and it is canon rather than a choice

§1 assumed the chapter's tension was the disguise holding. Reading the cell content changed it. **Four
shipped canvases say, unprompted, that Bastien never looked at her face** — *"he watches the number, not
her"* · *"he doesn't look at her face once"* · *"not her face — her face has never been the thing"* · *"not
at her face, at the read-out"*. He was reading the gauge in her chest, and the gauge is dark now.

So the asymmetry was already written before this chapter existed: **she knows him instantly, he cannot know
her, and the bought face is the smallest part of why.** The buyer question is therefore answered at
`cap_bastien_notices` instead of being strung out, and what replaces it is worse — she knows exactly whose
stack she needs and what reaching it will cost, and every rung after that is hers.

### Amendment 3 — the wardrobe was broken, not misplaced

§13 called the cot wardrobe a blocker on the strength of the design read. It was worse and cheaper than
that. The rack is a **single injected link** emitted into the one location whose slug equals
`settings.wardrobe_location` (`v2.py:9601`, `:9649`), and it pointed at `wren_room`, route-cut since the 1a
close. **The player has had no wardrobe page at all since The Archive** — no equip, no unequip, and the four
equipped-based undress portraits unreachable. One key fixed it.

### Amendment 4 — "a day after the drain" is a second drain, not a day counter

§9 asked for a night's gap. `bastien_drains_done gte 2` *is* that gap: one evening is one visit, so a second
drain cannot happen on the first night. No new counter, nothing that can desync, and it guarantees the
heat-passed loop runs at least twice before the room burns.

### The heat pass, measured

| | 0.1.8 | 0.1.9 |
|---|---|---|
| explicit in repeatable | **20.5%** | **34.0%** |
| explicit floor | 7.0% | 6.5% |
| `loop_bastien_backroom` | — | **5/5 hot** |

`loop_bastien_backroom` is now the hottest repeatable surface in the game (heat-passed Mercer is 3/5; Colm,
Renner, Calloway and `mercer_serve` are 0/4 each). **The fix was not longer pages** — rev 139 cut Mercer's
pose pages for exactly that, so this is one screen per pose at house size with 3+ real words each, and the
escalation is the ladder plus one extra anal node.

⚠️ **Measure with `gates.Beat`, never per block.** A Beat is one node's *folded* text — `[group]` variants
fold in, only cascade beats split. A per-block first pass read the finished loop at 2/20 when it is 5/5.

⚠️ **The explicit floor fell, and it is arithmetic rather than craft.** The chapter added ~166 beats of
mostly non-sex story, so the denominator grew faster than the numerator. **The number that clears both
gates is the backlog LO deferred**: Colm, Renner and Calloway are three loops at 0/4, about twelve potential
hot beats, which would take the floor past 7.5% and the repeatable share toward 50% in one pass.

### What is blocked

- **The ship build.** Every explicit slot is empty — 8 video pools, 1 file-list pool, 8 stills, 2 wardrobe
  assets. Ship discipline is `IMAGE/VIDEO MISSING == 0` in both builds. Work-list:
  `games/vesper/media_manifest_the_face.json`.
- **`games-data.js` stays at 0.1.8** — the portal describes what is deployed; it bumps with the real build.
- **The 17-suite live run** needs a media-complete build and a browser. A `--debug` build bakes MISSING
  widgets whose anchors land inside `#passage` and break `link_texts` assertions (the rev-141 finding).

### Open items from §17, resolved or still open

1. **Ceilings (a) and (b)** — signed by instruction 2026-08-16 and spent as written. **Resolved.**
2. **The bar ladder's exposure line** — set at rung 3: hands land, never hard, and every man checks the back
   door before he takes his hand back. **Resolved.**
3. **Does Colm react?** — **still open.** He does not see through the face; nothing was written for him.
4. **The overheard argument** — written to LO's steer, nothing expository. **Resolved.**
5. **The new default outfit** — **still open and still marked.** Touches shipped content.
6. **Nights between drain and raid** — one, via `gte 2`. **Resolved.**
7. **Kess's exposure** — no change, confirmed deliberate. **Resolved.**

---

## 21. POST-BUILD AUDIT (beat_0110, rev 160) — three defects, all mine, all fixed

A read-only audit after the chapter was content-complete found three real defects. **The cause is identical
in all three and that is the useful part:** each came from a claim I wrote down confidently and did not check.

### 1 — the wall refusals never closed

Gated only on `chip_read` + their own asked-flag. `cap_the_wall` fires at **3 of 4** by design, so a live
fourth refusal is the designed-for case — and with no closer it stayed armed through the face, the bar job,
the back room and the raid. The likeliest path was the worst: take the third refusal, cross the strip,
`cap_the_wall` fires, walk into the market to buy the face with `wall_market` still waiting — then play a
scene where a man who knows her treats her as Wren, in the bought face, one beat after the capstone that
establishes nobody recognises her.

**Fixed:** `wall_understood is_false` on all four. Chosen over `face_bought` because `cap_the_wall` ends on
*"So the question is dead… Dead is her asking it"*.

**And the header lied about its own code.** It called them "flat solo links (the `bastien_door_search` /
`mercer_end_table` shape)" — **both cited precedents are `is_repeatable = true`**, and
`selectAutoFireCanvasForLocation` skips with `if (c.isRepeatable) continue;`, so a non-repeatable
location-triggered canvas is an **auto-fire**. Kept as auto-fires — doors shutting on her unbidden is the
better shape — but the header now says so.

### 2 — the raid spoiled itself in its first image

`cap_the_raid` opened on the room already burning, directly above *"An evening like the other ones"*, with
the fire at beat 15 of 18. That is the defect LO caught in the shipped build, and the rule it produced is one
**quoted in this very document two sections earlier**.

**Fixed:** lead is `locations/bastien_backroom.jpg` (the room as she has known it — sanctioned establishing
reuse); the burning image moved into the `"Go."` beat where the prose names the fire.

### 3 — the ruin crawl collapsed to one click

`activity_sift_the_ruin` banded on **`yard_depth`**, which is the **Burned Yard's own odometer** and is
already at 3 when this chapter begins (that crawl is mandatory Act-1 content producing `crew_known`). Band 1
could never render, and the first sift took 3→4 straight onto the **terminal** band. The release's only
post-credits content was one screen. My header defended the reuse as *"the same shape of thing"* — a counter
is not a shape; it has a live value, and that one was full.

**Fixed:** dedicated `ruin_depth`, declared in both sites, thresholds unchanged. Verified by walking from 0:
band 1 twice, band 2 twice, terminal after. `yard_depth` untouched.

### Also — the pivot, in two of five pose pages

`base_anal_bastien` ended on *"the drain sits in the contact and waits"*; `base_anal_hard_bastien` on *"the
rest is the price of the hand"*. Both are the failure CLAUDE.md names as **the one that recurs**, written the
same week the rule is quoted at the top of §11 here. The seat still has to be communicated, so it **moved to
the top of each page** rather than being cut. All five pages now end on the act, and the loop holds **5/5 hot**.

### Verified after the fixes

Build green at 179 canvases / 28 locations · all four refusals close · the raid's lead carries no fire and the
fire is in-beat · zero `yard_depth` conditions in the ruin crawl · `loop_bastien_backroom` 5/5 hot ·
`explicit in repeatable` holds at **34.0%** · quest spine still exactly one card in all eleven states, one
boundary claim, five terminal badges.

### Left open for LO

- **Sol's and Colm's hubs run nightly at a bar the game says is shut.** Not a gate: Colm's hub carries
  `loop_colm_backroom`, one of only three standing sex loops, so a `raid_done` clause would *remove* content.
  Wants post-raid **bands** — a writing beat.
- `cap_bastien_notices` opens on the ajar door with the seated man visible (same class as defect 2, far lower
  stakes).
- `activity_berth_wardrobe` is a phantom row in `design_book.md`'s blueprint table — correctly implemented as
  the one-key `wardrobe_location` change; the table was never updated.

---

## 22. THE ELAPSED-TIME SWEEP (beat_0113, rev 164)

LO read one line — `rung_bar_promotion_4`'s *"You've had three weeks and you've turned up every one of
them"* — and asked whether it meant she had worked there three weeks, because if so it does not reflect
correct data. It did, and it was a **class, not a line: 26 sites across 13 canvases and 4 quest cards.**

### Why it happened, structurally

**A chapter gated on a METER has no floor and no ceiling in days.** The bar ladder gates on
`npc_bastien.relation` 6/12/18 at +2/+3/+3 a shift, so:

- floor ≈ **7 shifts ≈ 4 in-game days** under the 2/day cap
- a paid **cheat-page grant** (+6 relation) collapses it to **zero shifts worked**
- a slow player can take **months**

"Three weeks" is wrong at the floor, wrong on the cheat path, and wrong in the tail. **There is no number
that is right.** The claims also contradicted each other — `rung_bar_promotion_4` ("three weeks") fires
*before* `bastien_door_search` ("four weeks"), and three canvases all said "four weeks" at points separated
by multiple visits.

### And the same beat carried an economy error

`cap_the_raid`'s hinge thought — the beat the chapter turns on — read *"Four thousand coin of face and
shifts."* **The face costs 120; a shift pays 15.** Written for rhythm, never checked against an economy
built two beats earlier.

### What replaced them

Anchors to events the game guarantees: *"since she started"*, *"since Kess closed her up"*, *"every night
since"*, *"all this time"*. Most read better — Bastien is not a man who counts aloud.

Two worth recording: `hub_bastien`'s *"Your fourth shift"* became *"I know which night it was"* — **the
precision is the character**, so the fix keeps the counting and drops the count. And *"the first time in
three weeks"* became *"the first time she has **ever**"*, which is truer and stronger.

### Kept, deliberately

Backward-looking canon (eleven years, three months in that cell, a year ago at the far door, fifteen years,
the thirty/twenty-year careers, four months in the Reach) · in-scene beats · rotas ("six nights a week") ·
forward consequences · and Cain's *"Could be a fortnight. Could be tonight"*, a hypothetical about his
unpredictability and one of the better lines in the chapter.

### The bug class is killed in the skill

`references/rts-flat-prose.md` **Rule 10 — never assert elapsed time the player's pace controls**, with the
meter reasoning, the four exempt classes, a replacement table, and two sub-rules: keep precision where it is
character, and the same check catches invented **economy** figures. Logged in the skill CHANGELOG.

---

## 23. THE FACE LEAVES THE CLOTHING SYSTEM (beat_0116, rev 167)

LO, across three turns: *"the face cover becomes something else… like a link to wear the face or not in the
cot. From the bar bathroom she can only change to dress or her prev dress no new"* — and: taking it off
should be **a deliberate act with prose weight**.

### The root error was an unchecked engine claim

My own note at beat_0094 read: *"the portrait resolver has exactly one axis, the dominant dress item's type,
so the garment has to carry the face. **That is a deliberate compression.**"*

**It is not one axis.** The outfit loop takes `worn_type`, `corruption` **and `flag`** in a single `when`,
each checked independently (`v2.py:1664`). The face never had to be clothing. Collapsing *who she looks
like* into *what she is wearing* cost two live defects:

- **The bar dress existed only in prose.** `rung_bar_promotion_3` narrated her changing in a cellar passage
  that appeared in one sentence and nowhere else, with no `wardrobeEffects` anywhere.
- **It could not be made real**, because a `dress`-slot garment would replace the face-carrying kit and
  **silently delete her job** — six gates read that item.

### The separation

`face_worn` is a flag. `cover_stranger` goes back to being the plain kit she physically bought (its `type`
dropped, so no orphan on either side of the portrait audit). `dress_undertow` is a new garment. The portrait
rule re-keys onto the flag and sits first, so one portrait covers every outfit she can be seen in while
disguised. Six trigger gates re-point from `clothing_item` to `flag`.

### The two directions are deliberately asymmetric

**Putting it on** is routine — the small competent act it has become. **Taking it off is the beat**: the one
moment in the chapter where she chooses to be Wren again, at her own bunk because it is the only room where
nobody is watching. The game **does not explain why she wanted to**, because she has no reason that would
survive being said out loud — which is the chapter's argument in one line.

⚠️ **And the off-band states the mechanical cost in her voice.** Sol does not know her, the floor is not her
floor, the rota does not have her on it. Six surfaces vanish, and nothing else in the game would connect
that for a player who takes it off and finds the Undertow empty.

### The bathroom is not a second wardrobe

`wardrobe_location` is a **scalar** — one full rack, and it stays at the cot where her own things are and
where the undress portraits fire. `underworld_bar_bathroom` is two `equip` effects behind two choices;
`equipItem` replaces whatever holds the slot, so each is a straight swap and no unequip is needed (the
emitter supports only `add` and `equip`). The dress choice is gated on the face with a `locked_text` that
gives the reason: Sol hired a stranger.

### Recorded as decisions, not oversights

**Bar work is not gated on the dress** — only the face gates work, and gating the costume would rebuild the
exact "job silently vanishes" trap this removes. **No face-by-outfit portrait matrix.**

---

## 24. THE BEAT SHE NEVER HAD (beat_0117, rev 168)

LO asked whether anything tells her she needs a weapon. **Nothing in the fiction did** — the only prompt was
one clause at the end of card T's tip.

### It is the rev-143 defect again

LO's report then: *"there is nothing that she tells kess like that part failed, she just goes on to buy the
second part out of the sudden."* The diagnosis was that **the order was inverted** — purchase first,
justification after, four cycles running.

The taser was identical. Bastien's drain ends on *"Could be a fortnight. Could be tonight."* **She had no
reaction to it at all**, and a market card then explained why the emitter was not an option — reasoning the
player only read *after* going shopping.

**And it was a stall, not only a craft problem.** `cap_the_raid` is hard-gated on `taser_held`, so a player
who skimmed that clause would keep walking into the back room to find an ordinary evening, indefinitely,
with nothing on screen connecting the two.

### A problem, not a plan — a deliberate deviation from LO's phrasing

He said *"when Cain comes in she will have to somehow get him."* What the beat gives her instead is a list of
things she does not know: whether the drain opens on a thing built the way she is built (she has fired it at
nine men and never once at something with a core in it), whether he fights, whether he would look at her
once and walk back out — **and the one she stops on and does not pick back up, which is whether she wants to
do anything to him at all.**

She has never made a plan against a person in this game; she has been *pointed* at people, which is a
different verb. The only thing she decides in advance is the part that does not need him in it.

**And that is what makes the raid land.** She uses the taser on **Bastien**, on the spot. *"I cannot be
empty-handed"* reads as improvising with the one thing she had; *"I'll get Cain"* would read as a plan going
wrong.

### Two calls worth keeping

**Not gated on the face being off** — a safety call over a thematic one. She would take it off first, and the
cot is now where that happens, but a player who never does would never see the beat, never get the taser and
never reach the raid.

**The one-core-one-weapon rule moved out of a quest tip and into her head**, where it is reasoning rather
than instructions. Card T went back to being a pointer.

### Verified by simulating the state space

Across every combination of `bastien_drains_done` × `plan_made` × `taser_held`: **zero states** where the
taser is buyable while `plan_made` is false, and the chain drain 1 → `cap_the_wait` → taser → drain 2 → raid
is reachable at every step.

---

## 25. THE QUESTS-PAGE AUDIT (beats 0118–0119, revs 169–170)

LO: *"analyze thoroughly, and check if we have updated the quests page properly"* — read-only first, then
*"fix all of them properly."* The spine came back **clean**: a state simulation across all thirty-nine story
states found exactly one Story card live in every one of the chapter's eleven, no blank, no double, the
terminal badge on card U and nowhere else. Everything below is what the audit found *around* that.

### 25.1 The blocker the page exposed — no wardrobe from the opening to `berth_home`

Cards A and I tell the player to *"wear the dock-work coveralls from your room"* and *"wear the
junior-analyst kit from your room."* **Neither was possible.**

`wardrobe_location` is a scalar and the generator injects `[[Change Clothes->WardrobePage]]` into exactly the
one location whose slug matches (`v2.py:9601`, `:9649`). The built HTML carried **one** such link, inside
`Location_the_cot` — entry-gated `berth_home is_true`. Every cover is granted `wardrobeEffects add` and none
carries `initial`. So between the opening and `berth_home` **nothing could be equipped at all**, and Renner's
entire hub gates on `clothing_item cover_dockhand equipped`: **Mission 1 was uncompletable from a cold
start.** Invisible in play because every dev jump equips a cover directly and nobody replays Act 1.

Introduced at rev 145 when the rack left `wren_room`. **This chapter widened it**: rev 166 moved the rack
`kess_berth` → `the_cot`, and `berth_home` is strictly later than `salvage_entered`, so The Archive's
`cover_analyst` joined the list.

**The rack does not move again.** Unequip exists only on the WardrobePage, and the four equipped-based
undress portraits depend on it, so the rack has to live in the room those belong to. Act 1 gets a second,
targeted surface instead — `activity_wren_change`, the `activity_bar_change` pattern from rev 167: equip
only, no browsing, choices gated `clothing_item <id> owned` with `show_when_locked` so nothing silently
vanishes. `cap_1a_close` re-equips `company_grays` on the way out of the sealing Spire, so she is not
stranded in a Vance kit for the whole 1b handoff with the portrait resolver showing the analyst face.

Proven live from the exact cold-start state, not from a green build: the card renders at `wren_room`,
`dress` swaps `company_grays` ↔ `cover_dockhand` both ways, and both the `equipped` and `unequipped` gates
flip correctly. Cards A and I are now literally true and needed no rewording.

⚠️ **Two tips I had flagged were not stale after all.** *"your bench in your room"* and *"drill at your
room"* point at `activity_swap_weapon` and `activity_train`, both still at `wren_room` and live through
Act 1. Only the two *wearing* instructions were unfollowable.

### 25.2 Card T was one card doing four states' work

`bastien_drains_done gte 1` + `raid_done is_false` spanned drain 1 / plan made / taser bought / drain 2
behind byte-identical text, and was wrong in three of them: it asserted *"you already worked out the rest of
it lying on the cot"* from the instant the first drain landed — **before `cap_the_wait` can have fired** (the
rev-162 elapsed-time defect in a new place); it went on saying *"go and buy the thing"* after she was
carrying it; and it never mentioned that the raid needs a **second** drain.

Split on `plan_made`. **T1** covers the un-thought state and its only goal is to send her home. **T2** puts
the two tasks in live bullets — `bastien_drains_done gte 2` and `taser_held gte 1`, which are the two clauses
of `cap_the_raid`'s own gate — so the page can no longer disagree with the engine, plus `ready_canvas` and a
`ready_text` for when both land. The tip keeps only the evergreen half, because **there is no `ready_tip`**:
one string serves the card's whole life, so an instruction to go shopping would have gone stale exactly the
way the single-card version did.

### 25.3 Progress goals — the chapter shipped with none

Cards M–U carried no `goals` at all while `yard_depth` and `mercer_attempts` set the precedent, and the
chapter has four countable ladders. The cheap engine fact that made this quick: **a card with no goals
evaluates `allMet` vacuously true**, so `ready_canvas` alone renders the 🔓 frame with a 📍 pin.

| card | added |
|---|---|
| M | `ready_canvas` → 📍 The Berth |
| N | `wall_refusals gte 3` — four refusals across four presence windows, and three are needed |
| O | `coin gte 120` (the face's own price) + 📍 The Black Market once she can afford it |
| P | `face_worn` flag bullet + 📍 The Undertow — buying and *wearing* have been different acts since rev 167 |
| R | `bar_rung gte 4` — the longest grind in the chapter |
| S | `ready_canvas` → 📍 The Back Room (no goal: a `gte 1` bullet would close the card the moment it was met) |

**Q stays goal-less on purpose.** Its only countable axis is `npc_bastien.relation`, and naming him on the
page before `cap_bastien_notices` fires would spoil the hinge.

⚠️ **📍 renders, 🕒 does not.** `_formatCanvasSchedule` reads the *canvas's own* `scheduleParams`;
`hub_bastien` has none — its 20:00–23:59 window comes from `npc_bastien`'s schedule row through
`requires_npc`. Verified live, after the comments had already claimed otherwise.

### 25.4 Bastien had no section

Cards per NPC at ship: Renner 10, Calloway 5, Colm 5, Mercer 3, **Bastien 0** — for the chapter's own
conquest, who carries a four-rung ladder and the hottest repeatable loop in the game. The rev-141 shelving
was right for 0.1.8 (its own rule was that his section starts when he becomes somebody she can act on) and
stopped being right here. Four new cards, placed after Mercer's so the section renders last, which is
chronologically correct — NPC sections come from the cards themselves, so that is the whole wiring.

**B4 takes the plain ✓ badge.** Card U remains the one card in this game permitted to set `terminal_text`
and to name the future. And B4 keeps the secret: it says they carried him out, never that he is dead and
never that he can be found.

### 25.5 Verified

Live headless walk of all eleven chapter states plus the cold-start wardrobe flow: every card, counter and
pin correct at the moment it renders, all five `ready_canvas` slugs resolving (an unresolved one blanks the
block silently), Bastien's section appearing and retiring on cue, and **zero page errors**. Heat unmoved at
`explicit floor` 6.3% / `explicit in repeatable` 34.0% — the deferred Colm/Renner/Calloway backlog, untouched
by this pass.

---

## 26. THE LOCKED TOILET (beat_0120, rev 171)

LO, playing: *"bar bathroom can remain unlocked right?? there is no reason for it to be locked??"*

Half right, and the half he was right about had a better reason than the one he gave.

### The lock was visible

`underworld_bar_bathroom` carries `entry_from = "underworld_bar"`, and **a blocked location does not hide.**
The generator emits a greyed `location-card-locked` with `blocked_message` as its subtitle. So from **Act
1b** — the Sol/hunt leg, long before this chapter exists — the Undertow's nav grid carried a greyed *"The
Bathroom — nothing in it she needs."* The game was explaining a toilet in order to keep her out of one.

That is the shape this book already rejected one door further in: `activity_sift_the_ruin` was built as a
**card rather than a location** specifically so a locked "The Back Room" would not sit on that grid from Act
1 onward. The same argument applies here and had simply not been made.

### And the clause was doing no work

`activity_bar_change` is the room's **sole** occupant and carries `bar_rung gte 3` on its own trigger. An
open door therefore reaches nothing early — she walks into an empty toilet, which is what a bar toilet is.
What the open door buys back is the **NEW badge**: `locationHasNewCanvases` now lights the card at exactly
the moment the change surface unlocks, which is a better pointer to the dress than a greyed card ever was.

### The other clause stays, and this is the part worth recording

`activity_bar_change` has **no `raid_done` clause of its own.** The room lock is the only thing keeping
*"change into the dress he sent down"* out of a bar that burned with its owner dragged through the wall —
the rev-157 defect (a standing surface that survives the fire and contradicts the ending), one door deeper.
Dropping both clauses because one was pointless would have shipped it.

`blocked_message` was rewritten to match: it now renders **only** post-raid, where *"nothing in it she
needs"* is plainly wrong — the room did not stop being useful, the building burned. The new line is the
tape and Sol's bucket, in the voice `activity_sift_the_ruin` and card U already established.

### Verified live, all four states

Open and empty in Act 1b (enterable, no change card, exit resolves) · open with both equip choices at rung 3,
dress landing in the `dress` slot · shut again post-raid with the new message on the greyed card. Counts
unchanged at 186 canvases / 30 locations. Zero page errors.
