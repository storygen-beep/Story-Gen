# Vesper — THE COUNT (Bastien at the cot, from the bunk back to himself)

> Design record for the second half of **0.2.2**, after the rescue in *The Way Down*. **Same release, not 0.2.3**
> — LO, 2026-09-19: *"this isnt 0.2.3 release, it is in the 0.2.2 just the build order."* Every engine claim below was read out of the
> code or the shipped TOML in the design session, and carries its file and line.
>
> **Status:** design locked with LO in conversation, 2026-09-18 → 2026-09-19, and **BUILT 2026-09-19, rev 230,
> beats 0194–0203** on LO's go ("start implementing each beats one by one, until everything is done, after each
> beat thoroughly review it"). The media harvest (beat_0204) is authored and pending. The sections above are the
> design as locked, with the build's corrections marked in place; the BUILT section at the end is the record.

---

## Why

LO, after the rescue shipped: *"we have brought back bastien but now we have to make him normal."*

The Way Down stopped on purpose at the arrival — LO's call, verbatim: *"Bastien at the cot dont add sex yet
thats the build order."* The arrival's own banner (`5_scenes.toml:20052`) named what comes next: *"The repair
ladder — her sleeping with him to bring him back — is the NEXT chunk."* This is that chunk.

It also pays a debt the game owes out loud. At the arrival he tells her: *"in about a week you are going to
work out what you have actually got on that bed and you will wish you had left it bolted to a wall."*
(`cap_bastien_at_the_cot`, `5_scenes.toml:20069`). A line like that is a promise to the player, and it has to
land.

## LO's five calls

Proposed in chat, answered with *"Go ahead with your picks, write the full design"*:

1. **She leads while he is weak, and he takes back over as he heals.**
2. **He stays at the cot at the end.** The company knows the bar is his, so he runs things from her bunk.
3. **"About a week" is paid as *he is dangerous again*.** The company coming looking is held for later.
4. **About a week of game days**, start to finish.
5. **Kess's brace costs coin.**

---

## What already stands (shipped, and read)

- **The arrival** (`cap_bastien_at_the_cot`, `5_scenes.toml:20069`). He turns his head away from the cup:
  *"No."* Then: *"I did not ask anybody to take me off it."* She sits on the floor with her back against the
  bunk because there is nowhere else to sit.
- **The standing card** (`amb_bastien_cot`, `5_scenes.toml:20138`). His portrait hub: repeatable, pri 2, the
  only repeatable canvas for him at the cot. He faces the wall, runs hot, the cup goes down some days and not
  others, and he is awake at night with his eyes open. Its one exit is *"Leave him."*
- **What broke him** (`5_scenes.toml:19799`): *"The number he has been keeping is the number of days a man did
  not come for him."* In the plant room the number was a hundred and nineteen.
- **What he does not know, and never will** (`5_scenes.toml:19797`: *"The player knows. He never will."*). He
  never looked at her face in the cell, and she worked his floor in a bought face. He does not know she is
  the woman he read numbers off, or the one who put him on the floor with a taser.
- **Cain is off-page.** His last words at the cot: *"I will come when I can. Which will not be often and will
  not be soon."*
- **He owns the House.** `npc_bastien.description`: *"The bar and The House both."* Rue's own introduction
  (`5_scenes.toml:1897`): *"I run this house. Not the muscle, not the owner."* The game has been holding that
  unnamed owner since Act 2. Rue keeps `underworld_brothel` from 08:00 to 03:00.
- **Kess** keeps `kess_berth` from 10:00 to 22:00 and builds for coin. The shape is a rung on
  `hub_kess_berth` into a `substitution_only` canvas, with the coin on the inside choice
  (`kess_makes_the_link`, `3_activities.toml:4520`, 40 coin). He carried Bastien down the boards past his own
  bench and did not ask one question.
- **The anal finish is the drain** (the signed *Leash — Bastien, outside the cell* row, `design_book.md`), and
  `drain_charge` is one shot.

## Engine facts this rests on

- **`days_since_flag`** compares `flags_meta[flag].set_day` to `time_state.day` and **fails closed** when the
  flag was never set (`v2.py:4361-4393`).
- **Every `set` overwrites `set_day`** (`applyFlagEffect`, `v2.py:6312-6313`). A flag that is re-set each night
  therefore makes a clean "once per calendar day" gate.
- **The day counter** is incremented by `advanceDay` (`v2.py:5928-5936`) inside the daily tick.
- **Choice conditions go through the same evaluator** as triggers (`<<if setup.triggerConditionsSatisfied(...)>>`,
  `v2.py:13775`), so `days_since_flag` works on a choice. **A locked choice is hidden by default**
  (`show_when_locked` defaults False, `v2.py:14433`).
- **There is one repeatable canvas per NPC, location and time window.** Two repeatables bound to the same NPC
  at the same place warn at build. Everything else has to be a choice on the hub, a one-shot, or a
  triggerless canvas. The loop follows the shipped `hub_grier` → `loop_grier_room` shape
  (`5_scenes.toml:15561`).
- **The flag-chain validator** hard-fails a flag that a trigger or choice needs `is_true` when its only setter
  has no location. It scans `type = "flag"` items only. **Every milestone flag in this chunk is set on a
  located canvas** — the hub or an auto-fire — so the rule holds by construction.
- **An auto-fire whose NPC is absent is a known defect class** (open item 5 in the ledger). The Rue beat
  carries `npc_at_location … is_present`, the fix already proved on `cap_sabin_consults`.
- **Rev 228 proved the day-wait live**, not only in code: `tests/live_cot_decision.py` walks the real dev jump
  and news scene and watches a `days_since_flag` gate hold on day N and open on day N+1.

---

## The spine — the meter replaces his count

He counted the days a man did not come for him. At the cot he starts again: the days since Cain put him down
on her bunk and left. He scratches a tally into the bunk frame with a thumbnail, and his card shows it growing.

**The chunk has one meter, `bastien_mend`, and it counts the nights she comes to him.** It rises at most once
per calendar day. At 3 he stops counting days, because somebody comes every night.

**The mechanic is the story.** Sleeping with him is what brings him back — exactly what the shipped banner
promised — and the number the player is pushing up is the number that replaces his.

## The steps — seven one-time pieces, about a week

There are two kinds of step. **His** moves are auto-fires: things that happen to her when she comes home.
**Hers** are choices on his hub card. **He opens the chunk and he closes it.** Steps 1 to 5 each wait at least
one calendar day after the one before (`days_since_flag … gte 1` on the previous step's flag). Steps 6 and 7 do
not: she carries the note and brings the envelope home on the same day, and a day's wait there would be a
wait for nothing.

### 1 — The water *(his; auto-fire @the_cot, one-shot)*
Gate: `bastien_at_cot` is_true + `days_since_flag(bastien_at_cot) gte 1`. Sets `bastien_drank`.

She comes home and the cup on the bench is empty, and he is holding it out, not looking at her. He drinks
because she stopped asking — his card already says mentioning it was the fastest way to make it stop going
down. She fills it. He drinks that too. He says nothing about it and neither does she.

### 2 — The washing *(hers; hub choice into a hub node)*
Gate: `bastien_drank` + `days_since_flag(bastien_drank) gte 1`. Sets `bastien_washed`. **First explicit beat.**

He cannot get to the tap, and nobody has washed him since the frame, where somebody did it on a rota every
Tuesday and did it properly (the plant room). She washes him on the bunk with the basin
and a rag, all of him, because there is no part of it she can leave. His cock answers before he does. He does
not stop her and he does not look at her, and he says one thing that means she can. She finishes him with her
hand. Afterwards he asks her name, once. She does not give it. Any name she has is either a lie or on a file
he read.

### 3a — The brace, bought *(hers; @kess_berth)*
A rung on `hub_kess_berth`, *"Ask him about something to stand in."*, gated `bastien_washed` is_true +
`brace_built` is_false, into a new `kess_makes_the_brace` (`substitution_only`, the `kess_makes_the_link`
shape exactly). **40 coin on the inside choice**, never on the trigger. Sets `brace_built`.

Kess watched the two of them bring him down his boards, so he knows what a long time off a man's feet does
to a knee. As always, he does not ask. *(Corrected at the whole-chunk review: the design said Kess carried him;
the shipped arrival has Kess watching them come down the boards.)*

### 3b — He stands *(hers; hub choice into a hub node)*
Gate: `brace_built` + `days_since_flag(bastien_washed) gte 1`. Sets `bastien_stood`.

She straps him in and he stands for as long as it takes to hate it, which is about a minute. Then he sits
down on the bunk harder than he meant to, and laughs at himself. *(Corrected at beat_0197: this first said "the
first time she has heard him laugh". It is not — in the cell he laughed at her, `cell_use_inventory`. So the
line became the true and better one: the last time she heard him laugh, it was at her.)*

### 4 — The first night *(hers; hub choice into a hub node; Tier-3, once-only, the chunk's capstone)*
Gate: `bastien_stood` + `days_since_flag(bastien_stood) gte 1` + **`time_of_day` 22:00–06:00** (added at the
beat_0198 review: the scene is a night — the berth quiet, Kess's torch off, him asleep in the dark at the end —
and it was reachable at noon). Sets `bastien_bedded` and `bastien_slept`, and adds `bastien_mend +1`. A cascade
of 16 beats — **more beats, not thicker beats**.

He cannot hold her weight, so she is on top and does all of it. **He read a number off her chest for weeks;
now her two fingers are on his pulse and she reads him.** There is one decision in the scene and it is hers:
the one way she knows to finish a man is the way that takes something from him, and she does not use it.
The capstone may spend its prose — that is what once-only buys — but every explicit beat stays on the body,
and the interiority gets its own beat, after.

### The loop opens
From here, each night on a new calendar day adds `bastien_mend +1` (see *The loop*, below).

### 5 — He stops counting *(his; auto-fire @the_cot, one-shot)*
Gate: `bastien_mend gte 3` + `bastien_himself` is_false + `days_since_flag(bastien_slept) gte 1`. Sets
`bastien_himself` and `bastien_note`. The day clause is a build-time correction (beat_0194): without it the
scene fired the moment she came back from the third night — the loop exits to the cot, and an auto-fire runs on
arrival — so "she comes home and he is sitting at her bench" would have happened while she was still getting
dressed.

She comes home and he is sitting at her bench in the brace with a pencil. The tally on the bunk frame has
stopped. He tells her the number, then that he is not keeping it any more. He has been writing. He folds a
note and asks her to take it to the House — *"to the woman who runs the floor. Do not read it."*

### 6 — The House *(auto-fire @underworld_brothel, one-shot)*
Gate: `bastien_note` is_true + `house_answered` is_false + **`npc_at_location underworld_brothel npc_rue
is_present`**. Sets `house_answered`.

Rue reads it standing, and then she sits down. Her own line comes back to her — not the muscle, not the owner
— and now the owner has a handwriting. She does not ask who Wren is; the underworld never does. She hands back
a sealed envelope for him.

### 7 — Counting again *(his; auto-fire @the_cot, one-shot; Tier-3, the chunk's last image)*
Gate: `house_answered` is_true + `bastien_back` is_false. Sets `bastien_back`.

He opens the envelope and counts money out on her blanket, unhurried, the way he used to count everything.
**This pays the arrival line.** What she has on that bed is the man who owns the underworld, back in business
from her bunk, and the first thing he does with it is count. The chunk ends on that image.

### Timeline, for a player who goes straight through

Arrival is day 0. Water on day 1 · washing on day 2 · he stands on day 3 (the brace can be bought any time
after the washing) · the first night on day 4 · two more nights on days 5 and 6 · he stops counting on day 7 ·
the House and the money the same day. **A week — and his line lands on schedule.**

A player can take one step at 23:50 and the next at 00:10, because the day counter turns at midnight. That is
accepted: it is still a calendar day on the clock, and the whole chunk still needs six midnights.

---

## The loop — `loop_bastien_cot` + `loop_bastien_cot_finisher`

Both are **triggerless**, so neither competes with his hub for the one-repeatable slot.

- **Reached from a hub choice, `"Go to him."`**, open from `bastien_bedded` on. Like `hub_grier`'s entry, the
  choice resets the loop traits.
- **The loop is open any time. The meter moves once a day.** The hub carries **two `"Go to him."` choices with
  the same label**, and only one is ever visible because locked choices hide by default:
  - `days_since_flag(bastien_slept) gte 1` re-sets `bastien_slept` and adds `bastien_mend +1`;
  - `days_since_flag(bastien_slept) lt 1` changes nothing.

  Step 4 sets `bastien_slept` first, so the flag always exists by the time these are read. Both setters sit on
  the located hub.
- **The shape is `loop_grier_room`'s:** pose nodes that loop back to themselves, `loop_npc_pleasure +8..14` per
  repeat, climax available at 50 or more, and a triggerless finisher.
- **Two bands on one if/elseif chain per node, keyed on `bastien_himself`:**
  - **WEAK** (before step 5): she leads. Two poses, **her mouth** and **on top of him**. He cannot lift his hips
    and she does the work.
  - **HIMSELF** (after step 5): he takes over. The same two poses, re-voiced: he holds her hips and drives up
    into her, and he tells her how. He also gets a third, **under him**, now that he can stand.
- **Finishes: inside her, or on her face.** **There is no anal pose and no anal finish in this loop.** The anal
  finish *is* the drain in this game's canon, and taking from him is the one thing this chunk never does. The
  loop never reads or writes `drain_charge`.
- **Costs and effects** use the game's existing sex-loop kit (energy, hygiene), matched to `loop_grier_room` at
  build time rather than invented here.

## His hub card — `amb_bastien_cot`, rewritten in place

The id and priority (2) do not change, so saves and the portrait wiring are untouched.

- **The base text is one if/elseif chain on the latest step reached:**
  1. facing the wall;
  2. the empty cup;
  3. sitting up, and clean;
  4. standing in the brace;
  5. after the first night;
  6. himself, at her bench, doing business.
- **The tally line** grows through the WEAK stretch and stops at step 5.
- **Its choices:** the next of her steps when its day has come · `"Go to him."` from step 4 on · `"Leave him."`
  as now.

---

## Register — the new ceiling row

**Bastien at the cot** *(drafted and SIGNED 2026-09-19 with this design; LO: "Go ahead with your picks").*
Full crude from the first hot beat: cock, cunt, cum, tits, mouth. **No anal**, because the anal finish is the
drain. **No restraint**, because he is the one who was bolted to a wall. **No pack.** His consent is in the
text: he never stops her, and he says one thing each scene that means yes.

- **WEAK band** (steps 2–4 and the loop before step 5):
  - His degradation diction is gone; he has none left.
  - **The humiliation runs on him**: needing to be helped, getting hard when he did not choose to.
  - Nothing degrading toward her.
  - His curiosity survives only as **watching**. He reads her like a readout, the one habit the wall did not
    take.
- **HIMSELF band** (after step 5):
  - The signed *Leash — Bastien, outside the cell* row returns for him, as written: proprietary, unhurried,
    crude and degrading diction toward her, and ownership-as-curiosity on top.
  - Its clause (i), *he never learns what she is*, stands.
  - **Its clause (ii), *she is never shown enjoying it*, is scoped to the back room.** The clause's own reason
    is that *"the back room is work"* and the charge is what she is smuggling past him. The cot is not work
    and there is nothing to smuggle.
- **Her side, in both bands:** her body is allowed to answer, because she is built to feel the sex she is in
  (the player description in `1_metadata_and_locations.toml`). **Her interior never claims the night as hers.**
  That is beat_0170's rule: there is nothing in this for her.
- **Tier-3 budget: two.** Step 4 (the first night) and step 7 (counting again). Everything else is RTS-flat at
  35–40 words a beat.
- **One `thought_bubble` per scene.** Narration to dialogue at most 1.5 to 1 wherever he is present. He is a
  talker — the ceiling rows' own shorthand is "Bastien's what he says".
- **The pivot rule applies.** An explicit beat stays on the body for its whole length, and is measured per beat
  against `gates.py`'s frozen EXPLICIT list (3+ hits), not eyeballed. The Way Down's first cut scored 4 of 31
  and looked fine by eye.

## Quest cards — one live at a time, linear

Every tip names a place and a time, in short sentences with no dashes (the `check_quest_cards.py` legibility
bar). No card carries an `npc_id`, so they stay on the main spine.

| card | when | tip, in gist |
|---|---|---|
| A | `bastien_at_cot`, not `bastien_drank` | Sleep. Go home to the cot tomorrow. |
| B | `bastien_drank`, not `bastien_washed` | He cannot get to the tap. The cot, tomorrow. |
| C | `bastien_washed`, not `brace_built` | Kess can build him something to stand in. The berth, ten till ten. 40 coin. |
| D | `brace_built`, not `bastien_stood` | Put it on him. The cot. |
| E | `bastien_stood`, not `bastien_bedded` | Go to him. The cot, tomorrow. |
| F | `bastien_bedded`, not `bastien_himself` | Go to him every night. Goal on `bastien_mend gte 3`. |
| G | `bastien_himself`, not `house_answered` | Take the note to the House. Rue, eight till three. |
| G2 | `house_answered`, not `bastien_back` | Take it home to the cot. |
| H (**terminal**) | `bastien_back` | End of chapter. Names what is still standing: the loop and his card. |

**Nine cards, not eight** (beat_0194). With eight, the walk home from Rue had no card live at all: G closed on
`house_answered` and H opened on `bastien_back`. G2 fills that gap and keeps the daisy.

⚠️ **The seam — the beat_0165 lesson.** The shipped 0.2.2 end card (`when bastien_rescued is_true`,
`terminal = true`) gets `bastien_at_cot is_false` added and **loses `terminal`**, and its tip becomes "Go home
to the cot." It is then live only between the extraction (which exits to `the_waterfront`) and the arrival.
**Check the boundary from both sides**, because last time the old release's end card was steering the new
release's opening.

## State — all extend-only

- **Trait:** `bastien_mend` — hidden, starts at 0.
- **Flags:** `bastien_drank`, `bastien_washed`, `brace_built`, `bastien_stood`, `bastien_bedded`,
  `bastien_slept`, `bastien_himself`, `bastien_note`, `house_answered`, `bastien_back`.
- **New canvases:**
  - one-shots: `cap_bastien_drinks`, `cap_bastien_stops_counting`, `cap_rue_reads_it`,
    `cap_bastien_counts_again`;
  - triggerless: `loop_bastien_cot`, `loop_bastien_cot_finisher`;
  - at the berth: `kess_makes_the_brace`, plus one rung on `hub_kess_berth`.
- **Rewritten in place:** `amb_bastien_cot`.
- **No renames, no deletions.**
- **No arc label — traced at beat_0194 and dropped.** `arc_stages` reaches the built game only as the
  `setup.npc_arc_stages` registry. The one renderer is the sidebar `stage_label` item, which reads a player trait
  named `<slug>_stage` (`v2.py:17649-17671`), and Vesper declares no such trait and no such item. Renner's
  "Drained" is in the registry and on no screen. Adding stages for Bastien would add words nobody can see.

## Media — seven new pools, four clips each (all named `sex/bastien_cot_*`)

- **The steps:** the washing (a handjob on a narrow bunk) · the first night (her on top, him flat on his back).
- **The loop poses:** her mouth · on top of him · under him.
- **The finishes:** inside · on her face.

**Visual brief for all seven:** a narrow bunk, a thin man, a small bare room. Each block carries a
`description` and `search_queries`, and no file or pool folder is reused across blocks (the one-asset,
one-block rule). This adds to the eight slots The Way Down still owes, which the harvest running now is working.

## Deferred — do NOT spend here

- The company coming looking (the other reading of "about a week").
- Cain at the cot.
- Bastien learning who she is (canon says never).
- His network as a repeatable courier job.
- The Chairman on screen, the Spire, the third memory piece, `the_site`, and the rest of the set of names.

---

## Build order — one verified increment per beat

Numbering continues from `beat_0193`. Every beat ends on a green build. Nothing is built without LO's go.

| # | beat | writes |
|---|---|---|
| 1 | `beat_0194` — systems + the seam: the `bastien_mend` trait · quest cards A–H and the old end card's seam · dev jump "0.2.2: Bastien on the bunk" · guard skeleton `tests/check_the_count.py`, written red first | `1_metadata` · `5_scenes` · `6_dev_shortcuts` · tests |
| 2 | `beat_0195` — step 1, the water | `5_scenes` |
| 3 | `beat_0196` — the hub rewrite (bands + the choice frame) · step 2, the washing | `5_scenes` |
| 4 | `beat_0197` — step 3: Kess's brace at the berth · he stands | `3_activities` · `5_scenes` |
| 5 | `beat_0198` — step 4, the first night (Tier-3) | `5_scenes` |
| 6 | `beat_0199` — the loop + finisher, WEAK band · the once-a-day `"Go to him."` pair | `5_scenes` |
| 7 | `beat_0200` — step 5, he stops counting · HIMSELF band on the loop and the hub | `5_scenes` |
| 8 | `beat_0201` — step 6, Rue at the House | `5_scenes` |
| 9 | `beat_0202` — step 7, counting again · end card H | `5_scenes` |
| 10 | `beat_0203` — dev jump "one night short" · `tests/live_the_count.py` · `gates.py` · reconcile | `6_dev_shortcuts` · tests |
| 11 | `beat_0204` — the media pass, seven pools | media |

**It ships in 0.2.2** — LO's call, 2026-09-19. The rescue and the cot ladder are one release; this is its second half.

## Verification

**Per beat:** merge the phases with `--validate`, package into `output` and `output_dev` with `--codes --dev
--debug`, and require validation passed with *all flag chains valid*.

**`tests/check_the_count.py`** (static), written red first and made to fail on purpose. It must catch:
- a meter that moves without the day check;
- a step with no `days_since_flag` on the step before it;
- an anal pose or finish anywhere in the loop;
- the Rue beat without `is_present`;
- a second repeatable canvas for him at the cot;
- the old end card still terminal.

**`tests/live_the_count.py`** (headless, in the built game, from the real dev jump), walked day by day:
- nothing advances twice on one calendar day;
- the loop stays open, and the meter moves once per day;
- `drain_charge` is unchanged across every loop visit;
- cards A to H appear one at a time, in order;
- the seam holds from both sides.

**Whole chunk:**
- `python3 .claude/skills/author-game-v2/scripts/gates.py vesper`: every authored node stays reachable, the
  explicit floor does not fall, and explicit-in-repeatable rises.
- `pytest` at the known pre-existing 6-failure baseline.

## Calls made in this design that LO can flip

Each one is small:

1. **Clause (ii) of the Leash row stays in the back room** and does not follow him to the cot.
2. **Rue sends an envelope back.** The step 7 image is money, not a reply.
3. **No anal at all in his loop**, not only no anal finish.
4. **The midnight straddle is accepted** rather than closed with a daytime window.

---

# BUILT — 2026-09-19, rev 230, beats 0194–0203

Ten beats, each on a green build, each with a guard section written red first, a live walk in the built game,
and a read-back against canon. Two independent read-only reviews: one on the first night, one on the whole chunk.

## What shipped

| step | surface | kind |
|---|---|---|
| 1 the water | `cap_bastien_drinks` | auto-fire @the_cot, one-shot |
| 2 the washing | `amb_bastien_cot.washing` | hub choice, explicit |
| 3a the brace, bought | `kess_makes_the_brace` + a rung on `hub_kess_berth` | @kess_berth, 40 coin |
| 3b he stands | `amb_bastien_cot.stands` | hub choice |
| 4 the first night | `amb_bastien_cot.first_night` | hub choice, Tier-3, 16 beats, 22:00–06:00 |
| the loop | `loop_bastien_cot` + `loop_bastien_cot_finisher` | triggerless, behind the once-a-day pair |
| 5 he stops counting | `cap_bastien_stops_counting` | auto-fire @the_cot, one-shot |
| 6 the House | `cap_rue_reads_it` | auto-fire @underworld_brothel, Rue present |
| 7 counting again | `cap_bastien_counts_again` | auto-fire @the_cot, Tier-3, 10 beats |

Plus: `bastien_mend` (hidden); nine quest cards A–H + G2 and the 0.2.2 card's seam; two dev jumps
(`dev_jump_count_start`, `dev_jump_count_one_short`); seven media pools, authored and unharvested.

## Where the build corrected the design

1. **Nine cards, not eight.** The walk home from Rue had no card live; G2 fills it.
2. **Step 5 waits for the morning** (`days_since_flag(bastien_slept) gte 1`), or it plays as she climbs off him.
3. **Steps 6 and 7 do not wait a day** — she carries the note and the envelope the same day.
4. **No arc label.** Vesper renders none; `arc_stages` only reach a registry nothing displays.
5. **He has laughed before.** In the cell, at her (`cell_use_inventory`). "The first time she hears him laugh"
   was false; now he laughs at himself, and the last time she heard him laugh it was at her.
6. **The washing contradicted the plant room.** He was washed on a rota, every Tuesday, "properly" — so he
   says so ("The one who washed me in the frame did all of it, every Tuesday, and never once looked at me").
7. **The first night is a night scene** and was reachable at noon — now 22:00–06:00, and card E says so.
8. **THE FACE — the largest correction, and a canon hole the design never saw.** `face_worn` is a toggle she
   works at this cot, and the bought face is the new girl off his floor who put a taser in him the night of the
   raid. Nothing stopped every scene of his playing while she wore it. Now every surface of his is gated
   `face_worn is_false`, his card's first band is the face-on band (only "Leave him." shows), and
   `activity_the_face` has bands for him being on the bunk — she changes out past the hull, where the bunk
   cannot see her. The shipped text is kept verbatim as each catch-all.
9. **The first night was rewritten on an independent review** — 24 findings, all verified against the TOML and
   fixed: three beats that pivoted to meaning or handed her something, a moan that contradicted the washing, a
   repeated simile, a clip brief that would have found choking footage, and more (ledger, beat_0198).
10. **The finisher's prose sits in a one-beat cascade.** Adjacent `[group]` blocks merge into one chain and
    nested groups have no precedent here, so clip groups and prose groups side by side would have become one.
11. **Three pools collided with The Face.** `sex/bastien_loop_oral_t5`, `_finish_facial_t5` and
    `_finish_inside_t5` were already Bastien's back-room loop (1c), clips on disk — the cot would have played the
    back room. All seven of THE COUNT's pools are now `sex/bastien_cot_*`, and the guard checks them against the
    whole game (found at the beat_0204 media audit; the chunk-local check had passed it).
12. **A second independent review, of the whole chunk, found 40 more — verified against the TOML and fixed.** The
    ones that mattered: step 5 could still fire straight after the third night when the loop crossed midnight
    (now also 06:00–22:00); the face bands put him at his bar "every night", but canon says he owns it and never
    visits — he had that face in his BACK ROOM; Kess "carried him down my boards" when the arrival has Kess
    watching; five surfaces disagreed about when he first looks her in the face (now: step 5, and the under pose
    is where he studies it); "There you are" in the under pose read as recognition; the plate's reason existed
    only in a comment (now on the page: "Half the Reach carries somebody's dead hardware"); the first night's
    decision was interiority inside an act beat (moved to the thought after it); "a week" stated as fact on
    surfaces a slower player reads beside `Day N`; three cards that promised what the scenes did not do (the
    number told, Rue standing, "priced it off what it meant"); the catch-all hub band's shipped lines described
    days that no longer happen; images lifted from the first night into the nightly loop; the finisher's clips
    and prose assumed she was on top after the under pose; and the brace scene's exit went to the berth while its
    prose walked her to the cot.

## Measured

| gate | 0.2.2 (rev 228) | THE COUNT (rev 230) | floor |
|---|---|---|---|
| explicit floor (repeatable beats with 3+ explicit words) | 10.3% | **13.3%** | 7.5% ✅ |
| explicit in repeatable | 61.0% | **68.6%** | 50.0% ✅ |
| every authored node is reachable | 475/475 | **489/489** | ✅ held |
| somebody speaks (game-wide) | 2.8:1 | **2.9:1** | ceiling 5:1 ✅ held |
| traversal heat | 13/35 | **14/35** | 60% (fails, as before) |
| judged gates passing | 21/40 | **21/40** | held |

Every explicit act beat in the chunk carries 3–4 of `gates.py`'s frozen EXPLICIT words, measured per beat.

⚠️ **One target this design set and the build did not meet: narration to dialogue.** The design asked for 1.5:1
wherever he is present. The chunk measures **3.6:1** (4,021 words). Where he is not having sex he talks as
designed — step 5 1.2:1, Kess 1.1:1, Rue 1.9:1 — but the act scenes are narration by nature (the first night 5.9:1
even after two added lines), and the water scene is deliberately silent. The game-wide measure held at 2.9:1,
under its 5:1 ceiling. Recorded, not hidden: if LO wants him louder in bed, that is more lines in the loop.

## Guards

- `games/vesper/tests/check_the_count.py` — eleven sections (§1–§10 + §7a), negative-tested **fifteen** ways
  (a terminal seam, two cards live, a jump not idempotent, the trait shown, a step without its day, a free meter,
  an anal finish, Rue without presence, a second repeatable for him, a face gate removed, the under pose
  ungated, the drain touched, stopping at two nights, the 0.2.2 card terminal, a pool shared with The Face) — all
  caught.
- `games/vesper/tests/live_the_count.py` — **165 checks**, the whole chunk from the real jump a calendar day at a
  time, then jump 2 from a fresh save. It also caught two bugs in itself, both recorded in it: a cascade walker
  that skipped any label containing "back" (fixed in `live_cot_decision.py` too), and a reload that kept a fired
  one-shot armed-off (a dev jump does not re-arm one-shots; take the jumps on a fresh save).

## Not done

- **The media harvest** — seven pools, 28 clips, on top of the eight slots 0.2.2 still owes.
- **The guide chapter** — the hand-written guide PDF gets a COUNT chapter at release (LO's).
- **Flagged, not fixed — a 0.2.2 hole the same face check exposed:** nothing in the bunker or the arrival gates
  on `face_worn`, so a player who wears the bought face into the rescue is carried home by a man who has seen
  that face. THE COUNT is safe from it (every surface of his waits for the face to be off); the rescue is not.
