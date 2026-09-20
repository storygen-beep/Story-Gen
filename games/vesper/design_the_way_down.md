# Vesper 0.2.2 — THE WAY DOWN (Bastien's rescue)

> Design record for the release after *Whose Hand* (0.2.1, shipped 2026-09-10).
> Every engine claim below was read out of the shipped build, not remembered.
>
> **Status:** design locked with LO in conversation, 2026-09-16 → 2026-09-18. This file is authoritative
> for the chapter. The story folds into `design_book.md` (the review surface) and the beat list seeds
> `authoring_state.json` when LO says so — neither has been touched yet.

---

## Context — why this release, and why this shape

**Where the game is.** 0.2.1 shipped 2026-09-10: 233 canvases, 35 locations, 17 NPCs, 114,825 words,
zero build errors, 0 missing media of 350. It ended on two memory pieces of three seated, the Chairman
holding the third, and two standing loops open (Grier, Sabin).

**The measured problem this release starts paying down.** The v2 scoreboard
(`python3 .claude/skills/author-game-v2/scripts/gates.py vesper`) against the shipped file:

| gate | now | floor / field |
|---|---|---|
| explicit floor (repeatable beats carrying 3+ explicit words) | **4.7%** | 7.5% |
| explicit in repeatable | **36.0%** | 50.0% |
| explicit screens per 1,000 words | **0.52** | field median 1.24, p25 0.95 |
| traversal heat (locations with a cycling explicit pool) | **12/35** | 60% |

The cause is named in the game's own record, a release before it was measured —
`design_the_face.md:361`: *"Scope: Bastien only (LO's call). Colm, Renner and Calloway stay cold and are
logged as debt."* and `:908` blames that release's heat numbers on *"the deferred Colm/Renner/Calloway
backlog, untouched."* At The Face the figures were 6.3% / 34.0%. Two releases later they are 4.7% / 36.0%.
**The floor fell while the game grew.**

**Why this release helps.** It is built on **Renner** — the largest cold asset in the game. His rig is
fully live (see Engine facts), his meters are the richest of any NPC (25 gates on `npc_renner` corruption
against Calloway's 8 and Grier/Sabin's 0), and all three of his places hang off `the_waterfront`, the
district she already lives in. The release gives the player a reason to walk back into a loop that has
been cold since Act 1, and adds a fourth rung to a crawl that currently dead-ends with nothing to find.

---

## Scope of THIS build

**Build to the rescue, and stop there.** LO's call, stated twice: this is **build order, not a release
cut** — the cot ladder continues after, in the same stream. Whether 0.2.2 ships at the rescue or after
the ladder is decided when we see where it lands, not now.

- **IN:** the news, the coveralls, the Renner drain, the yard crawl depth 4, Kess's build, the break-in,
  the rescue, Cain's extraction, Bastien delivered to the cot.
- **OUT of this build:** **no sex at the cot.** Bastien arrives and that is all. The repair ladder is the
  next chunk.
- **OUT of this release entirely:** the Chairman on screen, the Spire, the third memory piece, `the_site`.
  Nothing here opens any of them.

**What is standing when this build stops:**
- Renner's office loop and his drain — live, and now with a reason to be walked back into.
- The burned-yard crawl with a fourth depth in it.
- Bastien at the cot as a visible locked door (present, not yet usable).
- Everything that already stood: Grier, Sabin, the Rise day job, the Undertow, the House, the pit.

⚠️ **The consequence of the two calls together** (bunker closes after the rescue, no cot sex this build):
the break-in's route, guards and emitter scenes die with the bunker and nothing repeatable replaces them
in-build. The standing content this build adds is **Renner's**. Accepted and recorded, not argued.

---

## The story

1. **Cain learns Bastien is alive**, where he is held, and that the company is hurting him **to draw Cain
   out**. He has just found out — he has not been sitting on it.
2. **Cain can go, but quiet is better.** Him walking in is what the trap was built for.
3. **She goes for two reasons only: Cain wants it, and she is why Bastien is in there.** She tasered him,
   he was down, he could not run. That is how they got him (`design_the_face.md` §10). Nothing
   instrumental — no angle, nothing in it for her. It costs her weeks she would rather spend on the
   Chairman, and she goes anyway.
4. **Cain has the address. He does not have the inside** — the layout, the plant, the way down.
5. **Renner fitted the inside.** She does not ask him. She puts the Act 1 coveralls back on, works him,
   and **drains him**. He never learns why she came.
6. **She needs a piece of his salvaged kit** from the burned yard — the matching hardware for what Kess
   is building.
7. **Kess builds her a way to reach Cain from underground.** Nothing gets a signal out of there.
8. **The break-in.** Five turns, learned from Renner's own mouth. Three emitter shots. No reload down
   there.
9. **She finds Bastien. He cannot walk.**
10. **She calls Cain in** — the one thing the whole trap exists for. He comes anyway. They get out.
11. **The company does not find out until they are long gone.** The bunker closes behind them.
12. **Bastien is at the cot.** Broken, will not drink, does not want to be alive. *(The ladder is the next
    chunk.)*

### Why he is broken the way he is
Months of being hurt, and **he knows why** — he was a message to Cain, and he believes Cain read it and
stayed away. That is what broke him, not the pain. And the person who walks in is the woman who put him
there.

### The site — THE FACILITY, and the underside that did not burn
`facility_ruins` — *"What's left of the Vance asset-facility Cain burned to the ground… Something in the
wreckage is going to look like it belongs to her."* Already in the game, `entry_from = "the_waterfront"`,
no entry conditions, reachable today.

Renner supplying it is **already canon, not invented**:
- `npc_renner.description` — *"The equipment supplier whose gear outfitted the facility Cain burned down.
  **Though he never knew what it was for.**"*
- The burned yard's shallow find (`yard_find_1`) — *"shipments to the Facility — Renner moved more than
  he knew."*

So: his yard shipped the gear, into that building, which Cain then burned. **He built all of it.** The
underside survived and is still running, which is why a man can be held in a building that officially
does not exist any more.

**Rejected alternatives, recorded so they do not come back:**
- **Under Renner's own burned yard** — requires inventing that the company sited a black room under a
  broke blacklisted contractor's land, and deciding whether he knows. Bigger invention, collides with his
  character.
- **`the_site`** — reserved for Cain / the chip. Do not spend.
- **The Rise** — rejected by LO. A company does not hold a man in a building where it is also hiring
  casual staff off the street.

---

## Cast — four people, no new NPC

| who | what they do | state today |
|---|---|---|
| **Cain** | brings the news + the address; comes in at the end and carries Bastien out | 1 schedule row, **0 bound canvases** — a scheduleless speaker by design (`beat_0139`, the badge trap at `1_metadata:1449`) |
| **Renner** | the route and the inside, taken by drain; the yard is his | fully live, cold since Act 1, arc badged complete at "Drained" |
| **Kess** | builds the thing that reaches Cain from underground; paid, as always | live — landlord, the feed line, the paid night |
| **Bastien** | the rescue; arrives at the cot | all present-day surfaces dead on `raid_done` |

**No fifth person.** Adding one turns the release back into the errand chain LO rejected twice. She does
not need a new earner either — the Rise floor, the brothel and the pit already pay. **Mercer is out of
this release entirely** (LO's call).

---

## Mechanics

### 1. The coveralls
`cover_dockhand` — "Dock-work coveralls", `slot = "dress"`, `type = "cover"`.

- Granted `add` in `canvas_opening_morning`, so every save that has reached 0.2.1 **owns it**.
- **8 canvases gate on it being `equipped`**, including both Renner hubs. `0_systems_spec.toml:96` states
  it plainly: *"Renner's whole hub gates on `clothing_item cover_dockhand equipped`."*
- The rack is at **`the_cot`** (`[settings] wardrobe_location = "the_cot"`), her own room, and it lists
  everything she owns — LO confirmed this in play at `beat_0167`.
- Portrait rule exists and resolves: `when = { worn_type = "cover" }` → `portraits/wren_cover.jpg`.
  File present on disk **and** in `games/vesper/output/videos/portraits/`.
- **Covers stay. Not retired.** LO's call, reversing the `beat_0167` note.
- One dress slot: wearing the coveralls means she is not in the research kit, so she cannot work the Rise
  while she is on Renner. Normal, not a defect.

**Story weight:** the coveralls are not a disguise any more. His arc's final stage is literally
**"Drained"** — he knows what she is and what she did to him. She walks into his depot dressed as the girl
who worked for him, and both of them know.

### 2. The drain — she takes, she does not ask
Existing chain, unchanged in shape:
`hub_depot_floor` → `loop_renner_office_sex` → ass finish → `loop_renner_finisher` →
`renner_control_canvas.intro` (first drain) or **`.again`** (repeat).

- Repeat drain requires `equipped_weapon = 1` (drain worn) **and** `drain_charge >= 1`.
- ⚠️ `loop_renner_finisher` is **NOT** closed by `archive_1a_done`. That flag only picks between two
  wordings of the empty-drain line. The file's own comment: *"RENNER IS THE ONLY CHARACTER IN THE GAME
  WHOSE DRAIN SPANS BOTH ERAS."* It was future-proofed on purpose.
- **The drain costs her nothing.** LO's call. She walks in, works him, takes it, walks out.
- **He never finds out why she came.** Recorded consequence: Renner stays *content*, not a thread. Chosen
  deliberately.

**What the drain can and cannot give.** The drain takes **what a man knows**. Renner knows what he
installed and where he put it. He does **not** know what the place was for, that anyone is down there, or
that Bastien exists — so none of that can come out of him.

### 3. What Renner names — and the rule that governs it
**Everything he names is a real thing in the build.** Not flavour. A level he names is a room; a door he
describes is a door with a real gate; the plant he fitted is a thing she can reach.

**Build-order rule, non-negotiable: write the inside FIRST, then write what Renner says.** If his speech
is written first we invent good-sounding details and then have to build them. If the rooms exist first,
his speech is a true description and there is nothing to reconcile.

**Turn one of the five is the door.** He installed the service entrance, so his route starts outside.
That closes the last open question in the design — there is no separate way-in puzzle.

⚠️ **Prose-truth hazard.** His drain scene and the bunker rooms are two separate pieces of TOML written at
different times. Change one and forget the other and the game lies with a green build
(`.claude/skills/author-game/references/prose-truth.md`). **Mitigation: a checker that every place, door
and level named in `renner_control_canvas` resolves to a real id in the build, run every release.**

### 4. The yard — depth 4
`yard_crawl` @ `renner_burned_yard`, already built:
- `yard_depth` 0→3, **15 energy per push**, three ways past each guard.
- Stealth thresholds **10 / 25 / 40**; fighting the parallel; the emitter route spends
  `arousal_charge -1` and sets `yard_caught_once`; the emitter scene uses `sex/yard_emitter_fire_t5`
  (pool of 4).
- All three finds are **spent**: `yard_find_1` (`yard_clue_seen`), `yard_find_2` (`has_arousal_weapon`),
  `yard_find_3` (`found_dead_men`).
- So it is currently a **pure sink** — the scoreboard flags all three pushes as costing 15 energy and
  leaving nothing behind.

**We add a fourth depth** carrying the piece of kit Kess needs. Cheapest live content in the game: the
guards, the routes, the meter, the pool and the costs all already exist.

### 5. Kess builds the link
She is going underground; nothing gets a signal out. Kess makes the salvaged part talk to the plant that
is already down there, so she can reach Cain from inside. Paid, his ordinary verb.

### 6. The break-in — the route
**Five turns.** Each room offers two or three ways on.

- **Right turn** → advance.
- **Wrong turn** → a room with a man in it. She knows instantly, because he is looking at her.
- **Stealth** — **one free mistake per run.** She hears him before he sees her and backs out with no loss.
- **Emitter** — three shots. Each one fucks a guard unconscious (`design_book.md` Reset & reload: *"she
  floods them with the field, **fucks** the one in her way, and he passes out"* — non-lethal, no memory)
  and sends her **back to the start of the route**.
- **Fighting** — high enough and she puts him down instead. Same restart, no shot spent.
- **Nothing left** → she runs. Out of the building, come back later.
- **Cost: Charge and time only.** No day lost. LO's call.
- **Budget: four survivable mistakes per run** (one stealth + three shots).

**The failure state is the content.** Getting caught is a sex beat. Players who get it wrong see more,
not less. That is the reason this mechanic is worth building.

**If the player forgets the route** — go back and drain Renner again. The repeat path already exists as
*"the short re-ask."* Costs a trip across the city and another session with him. **The route is NOT
printed on the Quests page** — that would kill the mechanic, and the re-ask makes it unnecessary.

**Media:** every caught-guard beat needs a **pool**, not a single clip. This will be seen many times.
One asset, one block — never reuse a `file`/`pool_dir` across blocks.

### 7. The real economy of the run — already built
The emitter's **only** reload in the current era is the paid tier of `activity_kess_cot` @ `the_cot`:

- **"Crash rough"** — free, +40 Charge, 120 min, no day advance. **No weapon reload.**
- **"A night on the feed line"** — **10 coin**, +100 Charge, **540 min (a day)**, reloads the drain **and**
  sets `arousal_charge = 3`, and sets `feed_line_days = 3`.

`activity_recharge_emitter` and `activity_recharge_drain` are at `cradle`, which is Spire-side and
route-cut since the 1a close. So: **three shots per night, 10 coin, one day.** The run itself is cheap;
getting the shots back is not. That is the throttle and it needs no new system.

### 8. The extraction
Bastien cannot walk. She calls Cain in — the one thing the trap exists for. He comes anyway. They get
out. The bunker closes behind them. **The company does not find out until they are long gone.**

---

## Engine facts this build must respect

Verified in the shipped build; do not re-derive, and do not contradict.

1. **`conditions` needs `version = "1.0"`** or the block **fails open** — no build error, the gate just
   passes.
2. **One weapon at a time.** `equipped_weapon` = 1 (drain) or 2 (emitter). The swap is at the rack. She
   **cannot** carry both. Drain is used above ground on Renner; emitter below. No stash, no field swap.
3. **Nav-invisible interior needs BOTH halves** — no `entry_from` **and** `auto_exit = false`. Dropping
   only `entry_from` leaves an empty nav grid, which trips the list-every-location fallback
   (`v2.py:19386`) and lets the player walk from a sealed room to the Spire. `bastien_backroom` and
   `cain_lab` are the pattern.
4. **A `[[npcs.schedules]]` row is unconditional and outlives its owner.** `npc_bastien`'s only row still
   points at `bastien_backroom`, all days, 20:00–23:59. **When he moves to the cot this row must be
   handled on purpose, not added to.** The nav-card badge is *not* canvas-gated
   (`getNpcsPresentAtLocation`, `v2.py:4773`), so a row at a public location parks his face on that card
   in every save.
5. **Inserting `[[npcs]]` between an NPC and its schedule silently re-attaches the schedule.** Append, do
   not splice.
6. **Adjacent `[group]` blocks merge into one if/elseif chain.** Two ladders on one node = one chain and
   the second is dead.
7. **Bastien's present-day surfaces are gated `raid_done is_false`** — `hub_bastien`,
   `bastien_door_search`, `bastien_drain_canvas`. They stay dead. Anything new gets new ids.
8. **`bastien_backroom` appears unreachable post-raid** — its only route in is `bastien_door_search`'s
   exit, which is gated `raid_done is_false`, and the room has no nav card. `bastien_backroom_offhours`
   sits in it. **Verify live before touching it**; out of scope for this build either way.
9. **Save-safety (shipped game, extend-only):** never rename an existing `id`, a live flag/trait key, a
   stat's scale or the title. Add freely.
10. **Media extension is a wish** — the build resolves `.webm` → `.gif`. Verify the built HTML, never the
    TOML.

---

## Build order — one verified increment per beat

Numbering continues from `beat_0168`. Every beat ends on a green build.

| # | beat | writes |
|---|---|---|
| 1 | **The news** — Cain at the cot: Bastien is alive, held, and where. The trap named once. | `5_scenes` |
| 2 | **She says yes** — the two reasons, nothing instrumental. Quest card opens. | `5_scenes` |
| 3 | **THE BUNKER ROOMS FIRST** — the five-turn map, the guards, the wrong-turn rooms, the dead ends. No prose from Renner yet. | `1_metadata` + `5_scenes` |
| 4 | **The route mechanic** — advance / wrong-turn / stealth-free-mistake / emitter / fighting / flee. Charge + time costs. | `5_scenes` |
| 5 | **The coveralls beat** — back to the rack at the cot, into the Act 1 kit. | `3_activities` |
| 6 | **The drain** — `renner_control_canvas` gains the route payload. **Written against beat 3's rooms, as a true description.** | `5_scenes` |
| 7 | **The re-ask** — `.again` carries the route for a player who forgot. | `5_scenes` |
| 8 | **Yard depth 4** — the fourth push, the fourth find, the piece of kit. | `5_scenes` |
| 9 | **Kess builds the link** — paid activity at the cot/berth. | `3_activities` |
| 10 | **The way in** — turn one, the service entrance, the first real use of the route. | `5_scenes` |
| 11–13 | **The inside** — the rooms with content in them, the caught-beats, the pools. | `5_scenes` |
| 14 | **Finding Bastien** — the state he is in, and that he knows why. | `5_scenes` |
| 15 | **The call** — she signals Cain, knowing what it is. | `5_scenes` |
| 16 | **The extraction** — Cain comes in, they get out, the bunker closes. | `5_scenes` |
| 17 | **He is at the cot** — arrival only. **No sex.** The cot's description bands on him being there. | `5_scenes` |
| 18 | **Quest cards + the seam** — what the page says at the start and end of this chunk. ⚠️ Read `beat_0165`: the last release's end-of-content card was guiding this release's opening. Check the boundary card **from both sides**. | `5_scenes` |
| 19 | **Dev jumps** — one seeding the chunk start, one seeding one beat short of the break-in. ⚠️ `beat_0140`: any jump that seeds a Bastien drain must set `plan_made`. | `6_dev_shortcuts` |
| 20 | **Media pass** — pools on every caught-beat, `find-media` every new slot. | media |
| 21 | **Reconcile + gate run** — `gates.py`, the route-name checker, save-safety diff vs 0.2.1. | — |

---

## Verification

**Per beat** — merge the phases, package, green build with zero errors.

**Whole chunk**

    python3 .claude/skills/author-game-v2/scripts/gates.py vesper

Baseline to beat (measured 2026-09-16 on the shipped 0.2.1 file):
- explicit floor **4.7%** · explicit in repeatable **36.0%** · explicit per 1,000 words **0.52** ·
  traversal heat **12/35**
- `somebody speaks` **2.7:1** and `every authored node is reachable` **425/425** are currently PASS —
  neither may regress.

**New checker (write it this chunk):** every place, door and level named in `renner_control_canvas`
resolves to a real location/node id in the build. The prose-truth guard for the route.

**Live play** — the route has to be walked, not parsed. Headless Playwright: set `State.variables`,
`Engine.play("Canvas_<id>_Node_<n>")`, click. Assertions must check `State.passage` against the exact
canvas node — `"cot" in text()` matches the location description and proves nothing (`beat_0140`).

Specifically assert:
- all five turns walkable with a correct route, zero shots spent
- a wrong turn at each of the five lands in a guard room
- stealth ≥ threshold gives exactly **one** free back-out per run, not per turn
- an emitter catch decrements `arousal_charge` and returns to turn one
- at `arousal_charge = 0` and fighting below threshold the only exit is flee
- a flee costs Charge and time and **does not** advance the day
- `activity_kess_cot` paid tier restores `arousal_charge` to 3 for 10 coin and one day
- the drain re-ask is reachable at `drains_done >= 1` with the drain worn and charged
- `cover_dockhand` equips from the rack at `the_cot` and opens both Renner hubs
- after the extraction the bunker is closed and no orphan node is reachable

**Regression suite** — ⚠️ the live suites have been lost from the scratchpad four times and are now 154
assertions. **Put them in `games/vesper/tests/` this chunk.** Standing recommendation in the ledger,
still LO's call, and this build adds the most test-worthy mechanic in the game.

---

## Open items

Carried in from `authoring_state.json → next_up`, still LO's call:
1. `cap_grier_met`, `cap_grier_gives`, `cap_sabin_hires` auto-fire with their NPC absent. One
   `npc_at_location … is_present` clause each; the fix is proved on `cap_sabin_consults`. Re-opens three
   validated beats.
2. The regression suite's home (above).
3. `template_import.py:5375` — `warnings.append` where `warnings` is the stdlib module.
4. The four Grier/Sabin rung pools: tags say `_t2`/`_t3` and the shipped prose says "clothed", but LO's
   note says the footage does not match. Needs eyes on the clips; the media block and the prose have to
   land together.

New, from this design — all answerable at beat 3:
5. How many rooms the bunker has beyond the five turns, and what is in them.
6. How Bastien is being held when she reaches him.
7. Whether the wrong-turn rooms are five distinct places or a smaller set reused.

---

## Deferred — do NOT spend here

The Chairman on screen · the Spire (the ride up, the atrium, the penthouse, `vance_securities`,
`docs_vault` — `vault_cleared` stays never-set) · the third memory piece · what Cain was to her ·
`the_site` · the rest of the set of names · the units as individuals · why the drain has never worked on
Mercer.

---

# BUILT — 2026-09-18, rev 222, beats 0169–0189

Twenty-one beats, every one ending on a clean build. This section is the record of where the **build
corrected the design**, because three claims above turned out to be wrong and one was unbuildable as
written. The sections above are left as they were written so the corrections are legible.

## What the release was for, measured

| gate | 0.2.1 | 0.2.2 | floor |
|---|---|---|---|
| explicit floor (repeatable beats carrying 3+ explicit words) | 4.7% | **9.4%** | 7.5% ✅ |
| explicit in repeatable | 36.0% | **58.4%** | 50.0% ✅ |
| judged gates passing | 19/40 | **21/40** | — |
| every authored node is reachable | 425/425 | **465/465** | ✅ held |
| somebody speaks | 2.7:1 | 2.8:1 | ceiling 5:1 ✅ held |

Both gates that flipped had been **failing since The Face**, and the floor had *fallen* between releases
while the game grew. They are the two this release existed to fix.

**Traversal heat did not move (12/35 → 13/35).** It counts *locations* carrying a cycling explicit pool,
and this release's heat lives in a node graph under one location. Not a defect in the work; a gate this
shape of release cannot move. Flagged rather than quietly ignored.

## Four corrections the build forced on the design

1. **Renner does not remember the drains.** §1 above says his arc stage "Drained" means "he knows what she
   is and what she did to him." It does not. `renner_control_canvas`'s own exit is *"Leave him to come back
   to himself"* and its description says he keeps none of it. The badge is the **player's** progress label.
   There is no shared secret in that depot, and beat_0174 was written on the true, smaller, better version:
   he remembers the fucking, he is glad she came, and she is about to do it to him again for a reason he
   will never be told.

2. **Bastien was her captor, and he has never seen her face.** The design above did not know this.
   `cap_bastien_notices` (`5_scenes:12355`) states it outright: *"she was face to face with him for the
   whole captivity… he never once looked at her face — he watched the readout under her sternum and wrote
   the number down."* Every present-day surface of his arc is also gated `face_worn is_true`. So LO's call
   that he is held *wired into Renner's equipment* lands as earned symmetry rather than invention: the man
   who read numbers off a body is in a frame with a readout on it, and she reads his number the way he read
   hers. **She does not tell him who she is** — that would be the one thing in this for her, and §3 of the
   design says there is nothing in this for her.

3. **The gate on `bunker_descent` had to arrive in three pieces.** The flag-chain validator hard-fails any
   flag a trigger requires whose setter has no location. `route_learned` and `link_built` could not be named
   at beat_0172 because their setters did not exist until 0175 and 0178. Same rule later forced a located
   trigger + `substitution_only` onto all four bunker canvases. Recorded because it is the single most
   likely thing to be re-broken by anyone adding a gate before its setter.

4. **`yard_crawl` is in `3_activities.toml`, not `5_scenes.toml`**, and the bunker takes **its own counter**
   rather than borrowing `yard_depth` — `activity_sift_the_ruin` already shipped that bug once
   (`3_activities:2747`).

## Two flags in the design were never created
`bunker_entered`, `bunker_closed` and `boss_met` are **not in the build**. `bastien_rescued` already closes
`bunker_descent`, and a second flag would ship an immutable key to say the same thing twice.

## Defect found in my own writing, and how
The first cut of the five caught-beats scored **4 explicit beats of 31** against the frozen `EXPLICIT` list
(`gates.py:286`) — the prose gestured at the act instead of staying on it. **It looked fine by eye.** It was
found by measuring per-beat density with the build's own regex, rewritten at density and to the 35–40 word
target, and lifted to **27/31**; the four remaining zeros are the deliberate reflective beats, which is the
doctrine, not a miss.

## The guard, and that it was made to fail
`games/vesper/tests/check_bunker_route.py` — **in the repo, not the scratchpad**, which discharges a
`next_up` escalation that has been open for four releases.

Its first cut **passed a deliberately broken route**: the prose-truth check asked whether each tell appeared
*anywhere* in Renner's node, so deleting "conduit" from the sentence that gives turn five still passed,
because the word occurs elsewhere. A guard that cannot fail is not a guard. It was rewritten to locate the
closing mnemonic line and require all five tells **in it, in order**, in both the drain and the re-ask.

Five deliberate breaks, all now caught: a mis-pointed route exit · mnemonic drift · a free emitter ·
a schedule row on `npc_loder` · a quest card printing the route.

## Reversed after ship — the decision is an auto-fire (rev 228, 2026-09-18)

`activity_go_after_him` shipped as a repeatable **link** on the cot, on the argument that an auto-fire would
mean the player was never asked. LO made the other call: *"Go and get him out can be the capstone like canvas
not link but automatically happening."* The link could be clicked the same minute Cain left; what keeps the
decision from reading as automatic is the **wait**. It now auto-fires on the first cot visit **one calendar
day** after the news (`days_since_flag` on `bastien_alive_known`), and the coveralls scene is its second node
instead of a second auto-fire straight after it. `cap_back_into_cover` is retired (`is_active = false`), not
deleted, so a save parked inside it still loads.

## The cot ladder ships in this release (2026-09-19)

The open question in *Scope of THIS build* — whether 0.2.2 ships at the rescue or after the ladder — is
answered. LO: *"this isnt 0.2.3 release, it is in the 0.2.2 just the build order."* The ladder was built as
**THE COUNT** (`design_the_count.md`, beats 0194–0203, rev 230) and is the second half of 0.2.2. "No sex at the
cot" below was this build's stopping point, not the release's.

## Outstanding — the one thing not done
**The media harvest. 7 slots, authored and empty:** `portraits/loder.jpg`, `scenes/the_plant_room.jpg`, and
`sex/bunker_g1_crate_t5` / `g2_water_t5` / `g3_table_t5` / `g4_bench_t5` / `g5_desk_t5` (`pool = 4` each).
Every block carries its `description` and `search_queries`. It needs the find-media pipeline. The built
game's MissingMediaPage reads 6 and the build prints one file-not-found; both are expected and both clear
when the harvest runs.

**And, by LO's explicit instruction: no sex at the cot.** Bastien is delivered, will not drink, and does not
know who she is. `amb_bastien_cot` is the standing surface and is deliberately not a rung. The repair ladder
is the next chunk.
