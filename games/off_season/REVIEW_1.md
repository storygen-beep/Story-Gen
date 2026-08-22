# Off Season — review 1

Opened 2026-08-22, after v0.1 shipped **31 of 32** on `scripts/gates.py`. The report that opened
this file came from LO playing the built game:

> *the language being used here is tough to get. what is arcade?? No NPC introductions.*
>
> *Had a choice: Open up and work the counter canvas had a choice: Work the counter till one
> (2h 30m). One is 1 pm or am whatever it is, but we dont mention work till one or time, there is
> something wrong going on. Its content also have shutter up at eight and more, WTF is this?? Time
> is dynamic it is a sandbox game, time could be 2 pm or whatever then everything here makes no
> sense.*
>
> *What does Feed the Meter (GBP 3) means??*
>
> *In the start canvas, should it be like this, why couldnt we use simpler language, are we trying
> to ramp things up too fast, and it also does nt even have the NPC intros. I think we still havent
> learnt how the game should be started.*

Every complaint is real. Every one of them is invisible to the scoreboard.

**Why this file exists.** `gates.py` runs 32 checks and 31 are green. The only failure is
`location fill`, a word-budget miss. Nothing in the instrument measures whether a stranger can
read the prose, whether the anchor location's *function* is ever stated, whether the cast is
introduced, or whether the game keeps the promises it makes about the clock. This file covers what
the instrument does not, and Appendix A records the field research that says what the answers
should be.

Off Season is the **first v2 game a human has read end to end**, and the first authored under the
2026-08-19 meters doctrine. Three doctrine passes now carry the caveat *"nothing here is proven by
a built game."* This review is that proof arriving, and it is not flattering.

---

## How to read an item

| field | meaning |
|---|---|
| **severity** | `BLOCKER` · `HIGH` · `MED` · `LOW` · `OPEN` (unresolved question) · `DEFERRED` (parked by LO) |
| **layer** | `GAME` = one-off TOML · `SKILL` = the doctrine taught it wrong or never taught it · `ENGINE` = the substrate. Per `CLAUDE.md`: fix the skill too whenever a correct skill would have prevented it, or it ships again next game. |
| **evidence** | a `file:line`, a measurement, or a command. Anything without one is marked *opinion*. |
| **status** | `OPEN` · `FIXED (<rev>)` · `WONTFIX (<reason>)` |

Current count: **1 open · 41 fixed · 1 partly fixed · 2 wontfix** (45 total). The **skill** half
of items 1–5 landed first; then eight repair batches, 2026-08-22/23 — **batch 1 "the wiring"**
(D1–D4, O5, G2, G4), **batch 2 "what the screen says"** (M1, M2, T1–T7, G5), **batch 3 "the
first hour"** (L2, O1–O4, N1, N2), **batch 4 "the people who are already there"** (P1, P2, P4,
O7), **batch 5 "the act loops"** (G1), **batch 6 "the words the player has to already own"**
(L1, L3, M3, G3), **batch 7 "the bottom of the ladder"** (W1, W2), **batch 8 "the walk-in"**
(V1–V4) and **batch 9 "the act loops"** (H1–H3). Batches 7 to 9 were found by the batch reading the
game against the skill, not by LO's read. Scoreboard **31/37 → 37/38**.

**What is left is one item and two with reasons.** §P3 `location fill` is the declared
thin-to-thick word budget and is the only red gate. §O6's sidebar doubling is engine-shaped and
is LO's call. §G6 was never a defect — it is a record of two lint false positives.
See the Log. Field research in Appendix A; the causal lines in the skill in Appendix B.

**Sections 1-5 came from LO playing the built game. Sections 6-13 came from reading the game against
the corrected skill on 2026-08-22**, once all five doctrine passes had landed — a different
instrument, so they find a different class of defect: throttles that do not throttle, rooms with
nothing in them, and lines that are false at the minute they render. Two of them
(D2, T7) are **skill or instrument** faults the game exposed, not game faults.

**Standing decisions from LO, 2026-08-22:** the game will use a **neutral `$`** and no real-world
currency anywhere; the doctrine calls it *"the currency"*. Off Season is fixed **after** the
doctrine lands, as the proof. The `location fill` shortfall is **planned content, not a defect** —
the game is being built thin-to-thick and the budget was declared before the prose (§P3).

---

# 1 · The language assumes a reader we do not have

---

### L1 · Locale-locked vocabulary at 120× the field's rate
**severity** HIGH · **layer** GAME + SKILL · **status** FIXED (0.1-fix6)

> **Fixed word by word, not by purge** — the lint's own docstring forbids chasing the number:
> *"the rate does not discriminate… what separates them is what the words ARE."* The list went
> **94 words / 203 uses → 63 / 121**, and what moved was the ~30 words a reader outside the UK
> cannot resolve and is never told:
> ```
> false friends   vest -> T-shirt · jumper -> sweater        they do not LOOK like jargon
> swapped         settee/telly/mam/hoover/eiderdown/hob/fortnight/snooker/rota/lodger
> glossed         immersion heater · extractor fan · chandlery ("the shop that sells boat
>                 parts") · coin mechanism — taught once, then earned
> ambiguous       half three -> half past three
> ```
> **Player-visible hits remaining: zero**, checked with the lint's own `_player_visible_text`.
>
> **`tea` survives on the list and it is a false positive** — 11 of its 12 uses are the drink
> (*"two teas in the two mugs he owns"*, *"take her a tea"*, *"a tea towel"*). Only
> *"they all go home for their tea"* was the meal, and that one moved. The lint warns to expect
> exactly this: *"a false friend is by definition a common word."*
>
> **The 63 words left are the expected noise and are named so nobody "fixes" them:** number
> words the corpus never spells, proper nouns the fiction teaches (`kesh`, `judith`), coinages
> (`un-know`, `three-bar`), plain English the 25 games happen not to use (`arithmetic`, `diesel`,
> `barometer`, `kettle`), and the four glossed terms at their post-gloss repeats.

The prose leans on British household and trade nouns that carry no meaning for a reader outside
Britain, and it never glosses one of them: *immersion, fryers, extractor, chandlery, forecourt,
holdall, eiderdown, airer, biro, bedsit, lodger, mech, the front, at the wall, the electric, went
inside, pitch* (for rent), *float, change bag*.

Measured against the 25-game corpus (Appendix A.1), locale-locked terms per 10,000 words:

```
FIELD (25 games)          0.8
vesper (v1)               1.3
the_inheritance (v1)      1.4
late_shifts (v1)          7.3
──────────────────────────────
steam                     9.4
seventh_day              15.3
back_home                45.3
forty_miles              52.7
the_allowance            58.5
OFF SEASON               95.6      ← 120× the field
```

Eleven of the words we use appear in **zero of 25 games across 10.6M words**: `airer, anorak,
bedsit, biro, chandlery, chippy, forecourt, fryers, holdall, lodger, wellies`.

**The distinction that matters.** The field *does* use rare words — `orphanage`, `slaver`, `mage`,
`shillings`. Those are invented or generic, and the fiction defines them by context on first use.
Ours are real-world regional objects the prose assumes the reader already owns. They look defined
and are not.

**This is a v2-era drift.** The four v1 games sit at or near the field rate. Something changed
between the two skills, and Appendix B says what.

**Two further classes, found in the 2026-08-22 audit pass and worse than the above.** An unknown
word costs the reader a beat; these cost them the scene without telling them:

- **Ambiguous — `half <hour>`.** *"at half nine"* is 9:30 here and 8:30 across much of Europe, and
  American English does not use the construction. Off Season: **8 uses**. Across our games: **157,
  against 4 uses of the unambiguous `half past`.**
- **False friends — `vest`, `tea`, `jumper`.** Off Season uses `vest` ×9, `tea` ×8, `jumper` ×6.
  *"Stay past the tea"* is a **quest card** — so the ambiguity is in the UI, not just the prose.
  Sibling evidence: `forty_miles` writes *"You get the vest up over your tits"* inside an explicit
  beat, where an undershirt and a waistcoat are very different pictures.

Neither class came from the skill — `vest`, `tea`, `bonnet` and `half seven` return **zero** hits
across every reference file and template. These are author habit, not inherited doctrine.

---

### L2 · The anchor is never named as the kind of place it is
**severity** HIGH · **layer** GAME + SKILL · **status** FIXED (0.1-fix3)

> **Fixed by `canvas_first_arcade`**, a 189-word first visit at the anchor. It says the words the
> game had never once said to a player: *"This is an amusement arcade. Slot machines down both
> walls. Four coin pushers in the middle… Two driving cabinets. A crane with nothing in it worth
> the money."* LO's *"what is arcade??"* now has an answer on the second screen.

LO's *"what is arcade??"* is answerable: the game never says.

`amusement arcade`, `slot machine`, `penny arcade`, `coin pusher` appear **nowhere in
player-visible prose**. They exist only in `image_search_queries` (author metadata) and in image
`description`, which the engine renders as the `alt` attribute (`v2.py:13750`) — invisible to a
sighted player, and with **0 of 44 media files on disk** (§14) not rendered at all.

The location description does render (`v2.py:9620`) and reads:

> `1_metadata_and_locations.toml:108` — *"KESH AMUSEMENTS in eight-foot letters over the door, and
> under them forty machines, half of them off at the wall to save the electric."*

Forty machines of what kind is never said. And the opening uses the bare word *"the arcade"*
(`2_one_shots.toml:68`) before the player has ever seen that description.

**What the field does.** friends-of-mine: *"you now live in a suburban town called **Onegaron** in
south-eastern Canada."* corpo-life: *"I just got accepted into Chase-Bank, one of the most
prestigious banks in New York city."* Both name the *kind* of thing in the plainest available
words, immediately.

---

### L3 · Every readability instrument we own says this prose is easy
**severity** HIGH · **layer** SKILL · **status** FIXED (0.1-fix6)

> **Closed: the instrument this item asked for exists, and this batch is its proof.** `sentence
> length` still reports *median 10, ceiling 14* and still passes — it is measuring syntax, which
> was never the problem. The `own_words` lint built alongside it measures the thing that was:
> it named 94 words, and reading its list is what produced every edit above.
>
> It also stayed honest about its own limits, which is why it works — it flagged `tea`, `diesel`
> and `arithmetic`, all false positives, and says so in its own footer. A list a human reads
> beat a score a human could not.

Not a defect in the game — a defect in the scoreboard, recorded here because it is why L1 and L2
shipped.

`gates.py` gate `sentence length` reports **median 10 words across 593 sentences, ceiling 14** →
PASS. Flesch Reading Ease computed on real sentences (Appendix A.1):

```
                     Flesch   grade
FIELD median          78.0     5.5
OFF SEASON            86.8     5.0     ← easier than 24 of the 25 field games
```

**The prose is short-sentenced, short-worded, and unreadable anyway.** Difficulty here is
*referential*, not syntactic: nouns the player does not hold, and people named before they are met
(§3). No instrument in the skill measures either, and the one we have measures a proxy and passes.

---

# 2 · The opening does a long opening's job in a short opening's space

---

### O1 · 279 words, six people named, none present, nobody speaks
**severity** HIGH · **layer** GAME + SKILL · **status** FIXED (0.1-fix3)

> **Fixed by picking a shape and committing** (F1). `canvas_opening` is now a **cold open**:
> two nodes, **159 words, zero characters named**. It carries her situation and the pressure —
> the cold flat, the empty meter, twenty-two against ninety due tonight, KESH AMUSEMENTS over her
> own door, everyone she is related to inside four hundred yards, and nothing open until April.
>
> **The cast was not cut, it was moved to where a person can be met:** the building and the ninety
> to `canvas_first_arcade`, and the four of them to `canvas_meet_*`, each on screen and speaking.
> The reversal — *the pitch does not go to a landlord* — is now said by **Ewan, in his own yard**,
> instead of asserted at a player who has met nobody.

`canvas_opening` (`2_one_shots.toml:27-77`) is three nodes and 279 words across 22 sentences. In
that space it carries: her age at marriage and at first birth, the building and its name, the
weekly pitch of 90, who holds the lease, the meter, the season, four locations, and **six people**
— Ewan, Tam, "your sister's girl", "your brother", "your mother", "his father".

Not one of them is on screen. `gates.py` states it flatly:

> `canvas_opening: 278 words, no dialog block anywhere`

Measured against the field (Appendix A.2):

```
FIELD median opening                774 words
FIELD, when a name appears        ~229 words per named character
OFF SEASON                          46 words per named character, 0 on screen
```

**The field is bimodal and both shapes are coherent.** Either a *cold open* that names nobody
(corpo-life 64 words, DoL 193, the-company 126 — the cast arrives later as content), or a *staged
open* that spends 700–2,600 words putting people on screen one at a time (patriarch 2,619,
new-life-project 1,558, friends-of-mine 1,377).

**Off Season wrote a cold open and gave it a staged open's payload.** That is the defect, stated
precisely — not "the prose is too dense".

The shape the good ones use, read in full (Appendix A.2): world rules before any name → one person
at a time → each is present and speaks → **relationship label before the name** (*"your closest
friend, Felix Morin"*, *"one of your father's favourite girls, Ana"*) → a named next action → then
the hub. Off Season inverts the third and fourth of these: `2_one_shots.toml:56` reads *"It goes to
Ewan"* — the name first, the relationship never stated in that sentence at all.

---

### O2 · Two of the six people named in the opening are not in the game
**severity** MED · **layer** GAME · **status** FIXED (0.1-fix3)

> **Fixed with O1.** A cold open names nobody, so *"your mother's house"* and *"his father"* went
> with the rest. The husband survives once, in the arcade's first visit, as *"the month your
> husband went inside"* — a role in her own history, not a name the player is asked to hold.

`[[npcs]]` declares four: `npc_ewan`, `npc_tam`, `npc_roan`, `npc_nessa`. The opening also names
*"your mother's house"* and *"his father"* (Denny). Neither is an NPC; neither ever appears. A
third of the opening's cast load buys the player nothing.

---

### O3 · The funnel hands over into a dead half-hour
**severity** MED · **layer** GAME + SKILL · **status** FIXED (0.1-fix3)

> **Fixed, and the introduction does the waiting.** `canvas_first_arcade` is what is live in the
> gap — a non-repeatable, unscheduled, non-random canvas auto-fires on entry (`v2.py:4453`), which
> is also exactly what `_fh_live_at` counts. Its own exit spends 30 minutes:
> ```
> 07:00 start · 07:03 node->node · 07:33 the arcade, first visit fires · 08:03 the counter is open
> ```
> Verified live: the player comes out of the introduction at **08:03** with
> *Open up and work the counter* on the screen. The first free act is no longer a wait button.

`[time] starting_hour = 7` (`0_systems_spec.toml:41`). Node-to-node choices default to **3 minutes**
(`v2.py:13200`, `config.get('default_time_progression', 3)`), and the funnel's exit adds 30
(`2_one_shots.toml:71`):

```
07:00  →  07:03  →  07:06  →  07:36, at the_arcade
work_arcade_morning opens at 08:00   (3_activities.toml:306-309)
```

The player's first act in the open world is pressing a wait button. The only other things live at
the arcade at 07:36 are two `trigger_mode = "random"` ambients (`3_activities.toml:567`, `:596`) —
not guaranteed.

v1's `author-game/references/onboarding.md` §2.7 names this exact bug — *"the dead-window bug where
a needed NPC is only present at a time the player can't reach"* — in a file v2 does not have (§15).

---

### O4 · Clothing is switched on and never taught
**severity** MED · **layer** GAME + SKILL · **status** FIXED (0.1-fix3)

> **Closed by evidence, not by work.** The defect was a system that was **live** and untaught.
> Batch 1 switched `clothing_enabled` off after verifying the game has zero `clothing_slot` /
> `clothing_item` / `worn_*` conditions, so there is no longer a live untaught system to teach.
> The first-hour requirement it came from (F4 — every live system gets one beat, or sits on the
> sidebar at value-zero) is satisfied by the four banded sidebar rows and the change bag.
> **Re-opens the day a wardrobe surface is authored**, and `v2_state.json` says so.

`0_systems_spec.toml:47-48` sets `clothing_enabled = true` and `wardrobe_location = "the_flat"`.
Across the whole merged TOML, the strings `wardrobe` and `clothing` appear **once each**, and
`get changed` / `change into` appear **zero** times. A player is never told the system exists.

This is the one item v1's hard-gate rubric would have caught unassisted: *"Every live system is
surfaced once — for each system declared ON there is either a named opening beat that arms it or a
sidebar item at value-zero on frame one."*

---

# 3 · Nobody is introduced

---

### N1 · All four portrait hubs are live from turn one; the game has no meeting state
**severity** HIGH · **layer** GAME + SKILL · **status** FIXED (0.1-fix3)

> **Fixed. `every hub is met first` 0/4 → 4/4.** Four new one-shots — `canvas_meet_ewan`,
> `canvas_meet_tam`, `canvas_meet_roan`, `canvas_meet_nessa` — 119–135 words each, one node, four
> `dialog` blocks, built to the worked shape `the_inheritance/canvas_meet_audrey`. Each sets **one
> flag of its own** (F8: not one flag for the cast, which is what `rota_running`, `doors_open` and
> `arrival_done` were), and each hub is gated on it.
>
> **The node name is the role and the hub's is the name** (F7): *Your eldest* → *Ewan*, *Your
> youngest* → *Tam*, *Your brother* → *Roan*, *Your sister's girl* → *Nessa*. Lint
> `named before met` goes **3 people → 0**.
>
> **No waves, and that is a call.** F8 prefers staggered entrances; this game's premise is that
> all four live inside four hundred yards and she is related to every one of them, so gating them
> by day would be an invented lock on the one thing the world is about.

Every `npc=` hub, checked directly:

```
hub_ewan_yard        conditions: NONE
hub_tam_flat         conditions: NONE
hub_roan_house       conditions: NONE
hub_nessa_back_room  conditions: NONE
```

And no meeting flag exists anywhere — all 19 flags the game reads are `season_shut`,
`tam_saw_you`, `nessa_saw_her`, `lease_called`, `first_warm_done`, `*_rung_today`,
`*_talk_today`, `roan_back_door`, `counter_done_today`, `borrowed_from_ewan`,
`turnaround_done_today`, `slept_today`, `meter_fed_once`.

The player walks into the boat yard and Ewan is simply there, the hub's first paragraph standing in
for a meeting. v1 names this shape and forbids it:

> **§3. The forbidden shape — the bare cold-spawn hub.** A repeatable hub (`is_repeatable=true`,
> `npc=` set) whose base node is the de-facto introduction, with no first-contact one-shot gating
> it. […] **Never ship this.**
> — `author-game/references/npc-intro.md:104-113`

**The field, measured (Appendix A.3):** 16 of 25 games carry per-character meeting state, median 11
flags, 1,200 gate reads across the corpus. It gates *presence*, not just dialogue —
`become-someone` runs `<<if $has.metkate is 1 && $kate.loc is "Beach">>`: she is not in the world
until she has been met. `zaras-school-life` uses `$janet.metFlag eq false` to gate the meeting and
`eq true` to gate all 46 subsequent events. `the-company` has a passage literally named
`Intro-MeetSophie`.

**Ours — and the split is the finding.** Portrait hubs vs hubs gated on a meeting with *that*
character:

```
off_season      0 / 4        vesper (v1)            3 / 12
the_allowance   0 / 5        last_call (v1)        16 / 20
seventh_day     0 / 6        late_shifts (v1)       2 / 19
forty_miles     0 / 7        the_inheritance (v1)   7 / 10
steam           0 / 10
back_home       0 / 9
```

**Every v2 game is at zero. Every v1 game is not.** The skill that carries `npc-intro.md` produced
games with introductions; the skill that dropped it produced six games without a single one.

Off Season and forty_miles gate no hub at all; the other four v2 games gate their entire cast on
**one** flag — `rota_running` opens all six of seventh_day's, `doors_open` opens all eight of
steam's, `arrival_done` opens back_home's. The cast arrives as a block, not as people, which passes
a casual look and is the same defect wearing a coat.

---

### N2 · The four one-shots that look like introductions are mid-arc milestones
**severity** LOW (supporting evidence for N1) · **layer** GAME · **status** FIXED (0.1-fix3)

> **Fixed both halves.** They are still mid-arc milestones — that is correct, and the four new
> meetings are what was missing. What *was* a defect is that each was bound to a location with
> **no schedule and no `requires_npc`**, so it could auto-fire with its character absent and
> narrate them into an empty room. All four now carry their character's window and
> `requires_npc`. Verified live: `canvas_first_borrow` does **not** fire in the boat yard at 22:00
> with Ewan gone, and does at 10:00 with him there.
>
> ⚠️ `requires_npc` alone would not have fixed it — `isCanvasValid` (`v2.py:4573`) never reads that
> field on the auto-fire path. **The schedule is the gate**; `requires_npc` documents the intent
> and is correct on the two paths that do read it.

`canvas_first_borrow`, `canvas_tam_saw_you`, `canvas_roan_back_door`, `canvas_nessa_saw_her` are
non-repeatable and per-character, so they read like first contacts. They are not:
`canvas_first_borrow` is gated on `npc_ewan.hold >= 18`. These fire well after the player has
already been using the hub.

---

# 4 · The game names clock times it cannot keep

---

### T1 · "Work the counter till one (2h 30m)" — the engine cannot reach a clock time
**severity** HIGH · **layer** GAME + SKILL · **status** FIXED (0.1-fix2)

> **Fixed.** Both labels lose three words — `Work the counter (2h 30m).` and
> `Work the counter (3h).` The eight duration tags were already accurate, so nothing was
> re-costed. Gate `the label keeps its time` **FAIL → PASS**.

`3_activities.toml:331`. Three engine facts, all verified:

1. The sidebar renders a **live 12-hour clock**, updated on every time advance
   (`v2.py:5625-5637`, `updateTimeDisplay`).
2. `time_progression_minutes` is a **relative delta only**. `advanceTime(minutes)`
   (`v2.py:5400`) adds minutes; a grep of `v2.py` for `target_hour`, `advance_to`, `until_time`,
   `time_target` returns **zero hits**. There is no absolute-time advance in the engine.
3. There is no `@time` token — `_resolve_at_references` (`v2.py:14027-14072`) resolves `@player`
   and `@<npc>` and nothing else. An author cannot print the clock either.

The canvas window is 08:00–13:00 and the rung costs 150 minutes, so:

```
enter 08:00  →  10:30      "till one" wrong by 2h30
enter 10:30  →  13:00      correct, for one minute of the five-hour window
enter 12:55  →  15:25      wrong, and now inside the afternoon band
```

**Field basis (Appendix A.4):** across **117,453 link labels in 25 games**, 4,335 name a *duration*
— `(7 min)`, `(0:30)`, `(1 hr)` — and only **19 name a clock time**, every one of them either a
requirement (`Req: After 5pm`) or an explicit wait action (`Wait until 21:00`). **Not one label in
the corpus promises a clock time as an action's outcome.**

The skill already ships the right example — `the-voice.md:98`, `Buy coffee (0:02 £2)` — and no rule
behind it. Correct label: `Work the counter (2h 30m).`

**Same bug in two sibling games:** steam ships *"Work eight till six."*, *"Work the slab eleven till
four."*, *"Stay in bed until eight."*; forty_miles ships *"Hold the whole site until six."*;
seventh_day ships *"Be up here when he comes up at one."*

---

### T2 · "Shutter up at eight" is a fixed past inside a five-hour window
**severity** MED · **layer** GAME + SKILL · **status** FIXED (0.1-fix2)

> **Fixed — fourteen readings turned, not nine.** The nine listed here plus **four the lint
> could not see until T7 corrected it** (`canvas_tam_saw_you`, `canvas_roan_back_door`,
> `rung_roan_later`, `amb_terrace_nights`) and one more found while grepping the build.
> Every turn is grammatical and the fact survives: *"Shutter up at eight"* → *"The shutter
> goes up at eight"*; *"Half nine and the flat is at twenty-four degrees"* → *"The flat is at
> twenty-four degrees"*. **Fourteen references remain and every one is a rota or a rule** —
> read the lint's list and check: no reading is left in the game.

`3_activities.toml:323`, inside a canvas scheduled 08:00–13:00. The sentence is true at the
window's first minute and false for the remaining 299. Arrive at 12:40 and the game narrates what
you did at eight.

---

### T3 · The game writes absolute time more often than relative time
**severity** MED · **layer** SKILL · **status** FIXED (0.1-fix2)

> **Fixed, and the target was never the rate.** The skill half landed as `the-clock.md` C1–C6;
> the game half is T1/T2 above. The rate is **17.6 per 10k against a field median of 1.1** and
> that is the correct end state, not a remaining defect: this game runs on rotas — a chip shop,
> a boat yard, an arcade with opening hours — and C2 exempts a rule by design. What changed is
> that **every one of the surviving references is a rule and none is a reading.** The lint is a
> list; the list now reads clean.

The class behind T1 and T2, measured (Appendix A.4):

```
                    clock refs / 10k words     relative : absolute
FIELD median               1.3                       5.6 : 1
vesper (v1)                2.0                      12.0 : 1
the_inheritance (v1)       6.4                       6.6 : 1
────────────────────────────────────────────────────────────────
back_home                 23.7                       1.1 : 1
seventh_day               30.0                       0.9 : 1
OFF SEASON                33.0                       0.7 : 1
the_allowance             38.8                       0.6 : 1
steam                     47.5                       0.6 : 1
forty_miles               47.9                       0.9 : 1
```

The field writes *"morning"*, *"after dark"*, *"late"* 5.6× more often than it names an hour.
**Every v2 game names hours more often than it uses relative time.** Both v1 games sit with the
field. The v2 skill has no rule about naming a time at all.

---

# 5 · The money has three notations and none of them is declared

---

### M1 · "GBP 3" — a currency code the field never uses
**severity** MED · **layer** GAME + SKILL · **status** FIXED (0.1-fix2)

> **Fixed.** Six priced labels and two canvas names now carry `$`.
> Lint `the price is spelled out`: **symbol 0% → 100%**, code 75% → 0%, word 25% → 0%
> (field 94 / 0.8 / 5).

`3_activities.toml:85` (`Feed the meter (GBP 3)`), `:345` (`Buy a coin mech off the chandlery
(GBP 25)`). Across the corpus: **`$` 1,417 uses · `£` 459 (3 games) · `€` 0 · currency codes 0**,
and always flush against the digits — `$100`, `£25`, `$2500`.

---

### M2 · No `currency_symbol` is declared, so the engine's rent card renders `$`
**severity** HIGH · **layer** GAME + SKILL · **status** FIXED (0.1-fix2)

> **Fixed.** `[settings.rent] currency_symbol = "$"`, matching `board.economy.symbol`. All
> fifteen prose money references lose the unit name and keep the number, which is the style the
> rent text already used (*"Right. Ninety."*). Lint `the currency in the prose`: **no beat names
> a currency**, and both ⚠ mismatch warnings are gone. A **third** currency went with it —
> `amb_lets_drawer`'s *"two euros"* → *"two coins from somewhere else"*, which keeps the beat it
> was there for. Gate `the price is in one currency` **FAIL → PASS**: one currency across 8
> places, declared.
>
> ⚠️ **`RentDay_Short` agrees with us by luck, not by wiring.** It hardcodes `$`
> (`v2.py:16000`) and never reads the key. That is invisible while the decision is `$` and
> would break the moment it was anything else.

`[settings.rent]` (`0_systems_spec.toml:72-81`) enables rent at 90 and declares no
`currency_symbol`, so `self.rent_currency_symbol` falls back to `"$"` (`v2.py:1190`) and the card
renders **$90**. Three notations coexist in one game:

```
$90        the rent card the engine draws
GBP 3      the choice labels
"ninety"   the prose
```

**Not local to this game:** 8 of our 10 built games run `[settings.rent]`, and only seventh_day and
forty_miles declare a symbol. Six games render `$` by accident.

**Under LO's 2026-08-22 decision** the target is a neutral `$`, declared, used everywhere, and
never a real-world currency name or code — which also retires the `£` in seventh_day and
forty_miles.

---

### M3 · "Feed the meter" is an unglossed referent, and its explanation adds a second one
**severity** MED · **layer** GAME · **status** FIXED (0.1-fix6)

> **Fixed at the source — the location description**, which is where a player first meets both
> words. `the_flat` now reads *"a kettle, and an immersion heater for the hot water with a coin
> meter screwed to the wall beside it, **which is how you pay for heat in a building like this**"*.
> The referent is taught before the button that spends it, so *Feed the meter ($3)* lands.

> **Deliberately NOT fixed in the currency batch.** The `GBP 3` on the label is gone, but this
> item is not about the notation — it is about *meter* and *immersion*, two locale-locked
> referents a reader outside the UK cannot resolve. That is §L1's class and it belongs to the
> language batch, with the other 70 words on the `own_words` list.

The choice label names a UK coin prepayment meter with nothing to identify it. The paragraph behind
the click does explain it — *"Six fifties out of the change bag into the slot on the wall, and the
immersion starts up behind the plaster"* — but a label is what the player decides from, and the
explanation introduces *immersion*, a second unglossed term (L1).

---

# 6 · Three daily limits, and one of them was never switched on

Opened 2026-08-22 by a full read of the game against the five doctrine passes. These are defects
LO's play session did not reach and the scoreboard cannot see.

---

### D1 · The four talk screens are uncapped — the flag that gates them is never set
**severity** HIGH · **layer** GAME · **status** FIXED (0.1-fix1)

> **Fixed.** `flagEffects` added to all four talk choices (`5_scenes.toml`, on the choice per D2).
> Live: the talk is offered on the first visit, `tam_talk_today` is set, and the row is gone on the
> second visit the same day. The new gate `a day-cap closes` (D4) now holds it.

Every hub carries a talk choice gated on a `_today` flag being false, and `[engine.daily_tick]`
clears all four. **Nothing anywhere sets them.**

```
5_scenes.toml:82,474,699,925     read as is_false            the gate
0_systems_spec.toml:207-210      op = "unset"                the clear
                                 op = "set"                  ← does not exist
```

A flag no canvas sets is permanently false, so `is_false` fails open and the choice is available
every minute of every day. Verified by a full setter/reader census of the merged TOML: each of
`ewan_talk_today`, `tam_talk_today`, `roan_talk_today`, `nessa_talk_today` has **one** touch point
and it is the rollover unset.

What that costs. Each talk grants +2 on a cast meter for 3 energy and 20 minutes
(`talk_tam_dad` +2 `ease`, `talk_ewan_folder` +2 `hold`, `talk_roan_fortnight` +2 `bond`,
`talk_nessa_summer` +2 `trust`). Against the rung it was designed to sit *below*:

```
                     meter   energy   minutes   per energy   per minute   day-capped
rung_tam_tea          +4        6        60        0.67        0.067          yes
talk_tam_dad          +2        3        20        0.67        0.100          NO
```

Equal per energy and **50% faster per minute**, with no cap. The intended shape — one rung per
character per day — is not what the game does.

**Why nothing caught it.** The flag-chain validator only fails a flag that a trigger requires to be
**true** and nothing sets; a never-set flag read as `is_false` is legal and silent. `the climb is
paid for` still passes because `energy` is a real cost on the route in. The build is green, the
scoreboard is green, and the throttle does not exist.

`the-meters.md` M5 and `engine.md` §28 both teach all three parts correctly — set on the exit, gate
the choice, clear in the tick. Two of three shipped. **This is an author slip, not a doctrine gap**,
but it is silent-and-green, which is the class this skill has repeatedly promoted to a gate. See
D4 below.

---

### D2 · A rung that crosses midnight sets its day-cap on the *following* day
**severity** HIGH · **layer** GAME + SKILL · **status** FIXED (0.1-fix1)

> **Fixed, both halves.** All 14 rung day-caps moved from the rung's `exit_block.config` onto the
> hub choice that reaches it — placement scan: exit-set **15 → 0**, choice-set **0 → 18** (14 rungs
> + D1's four talks). `act_flat_sleep` lost `slept_today` entirely: it is a LOCATED canvas, so its
> `max_triggers_per_day = 1` is a real cap and `markCanvasTriggered` stamps the day key *before*
> `advanceTime` (`v2.py:4290`). Live: sleep at 21:00 Monday → 06:00 Tuesday, and Sleep is offered
> again at 21:00 on Tuesday.
>
> Skill half: `the-meters.md` M5's worked example now sets the flag on the choice and carries the
> 78-vs-40 measurement; `engine.md` §28 rewritten with §28.1 (the two emit orders) replacing the
> warning that was stated backwards.
>
> **`the_allowance` carries the same defect ×20 and was not touched** — out of scope by LO's
> standing instruction. Recorded here so it is not mistaken for fixed.

The generator composes a location exit in a fixed order — `v2.py:13085-13088` (and `:13049-13050`):

```python
f"{time_progression}\n{trait_effects}\n"
f"{flag_effects}\n{wardrobe_effects_code}\n"
```

`advanceTime()` rolls the day inside itself (`v2.py:5411-5414`, `while current_hour >= 24 →
advanceDay()`), and `advanceDay()` is where `[engine.daily_tick]` clears every `_today` flag
(`v2.py:5552`). So on a midnight-crossing exit the clear happens **first** and the set happens
**after** it. Straight from the built passage:

```
<<script>>advanceTime(540);<</script>>                                          ← rolls the day, tick clears
<<script>>setup.applyAndNotifyTrait("player", null, "energy", "add", 85.0, …)<</script>>
<<script>>setup.applyAndNotifyFlag("player", null, "slept_today", "set");<</script>>   ← set AFTER the clear
```

`act_flat_sleep` (`3_activities.toml:42`, window 21:00–06:00, 540 minutes) crosses midnight on every
entry before 15:00, so:

```
Mon 21:00  sleep  →  Tue 06:00      tick fires mid-sleep, then slept_today := true
Tue 21:00–23:59   Sleep NOT OFFERED  (slept_today still true)
Wed 00:00         tick clears it     Sleep reopens
```

**After the first night the player can never go to bed before midnight again** — the steady state
is sleeping at ~00:30 and waking at 09:30. Four other rungs sit in the same trap because their hub
window runs late: `rung_roan_stay` (100 min, Roan present to 23:00), `rung_roan_later` (70 min),
`rung_nessa_tea` (40 min) and `rung_nessa_curtain` (60 min, Nessa present 22:00–08:00). A late
visit silently costs the whole of the next day with that person.

⚠️ **`engine.md:989` states this hazard backwards.** Its words are *"a rung whose
`time_progression_minutes` rolls the clock past midnight triggers the tick itself, so a
midnight-crossing rung must not use a daily cap as its only brake"* — i.e. the cap gets **cleared**
and the rung becomes re-clickable. Given the emit order that cannot happen. The real failure is the
opposite: the flag is set on the far side of the tick and **locks the next day out**. The sentence
needs replacing, and this is the skill half of the item.

---

### D3 · The two counter shifts share one day-cap, and the morning one is strictly worse
**severity** MED · **layer** GAME · **status** FIXED (0.1-fix1)

> **Fixed by two numbers, not by restructuring.** One take a day across both bands is the author's
> stated design and is kept. The morning choice cost goes 8 → 6 energy and `rung_arcade_take_am`'s
> exit −8 → −6, so the morning pays **1.75 per energy** against the afternoon's 1.45 while still
> losing on time. Short on energy, work the morning; short on hours, work the afternoon. The
> canvas description, which still said "roughly two takes a day", was corrected to match.

`rung_arcade_take_am` and `rung_arcade_take_pm` both set `counter_done_today`
(`3_activities.toml:1229`, `:1251`) and both hub choices gate on it (`:336`, `:416`), so the two
windows share **one** take per day rather than offering two. That part is deliberate and is written
in the canvas description. What is not deliberate:

```
              money   energy (choice + exit)   minutes   per energy   per minute
morning take   +21           8 + 8 = 16          150        1.31         0.140
afternoon take +29          10 + 10 = 20         180        1.45         0.161
```

The afternoon take wins on **both** rates. Once a player notices, `work_arcade_morning`'s money
rung is dead content and the 08:00–13:00 window collapses to the float and the coin mech.

---

### D4 · Proposed gate — a day-cap that never closes
**severity** MED · **layer** SKILL · **status** FIXED (0.1-fix1)

> **Shipped as gate `a day-cap closes`.** Judged set 37 → 38. Predicted with a standalone script
> before it was written and reproduced exactly: `off_season` FAIL (4 flags); `last_call`,
> `late_shifts`, `mothers_place`, `seventh_day`, `the_allowance`, `the_inheritance`, `vesper` and
> `the_long_summer_test` PASS; `back_home`, `forty_miles`, `steam` n/a (no `[engine.daily_tick]`).
> No game is failed for obeying the doctrine.

D1 is fully mechanical to detect and nothing in the toolchain looks for it:

> Every flag that is (a) read with `is_false` in any condition **and** (b) unset in
> `[engine.daily_tick]` must have at least one `op = "set"` site somewhere in the game.

No judgement, no threshold, no field measurement needed — a throttle with two of its three parts is
a throttle that does not exist. Candidate for the next gate pass.

---

# 7 · Five rooms have nothing in them, and the board already says what goes in them

---

### P1 · Three locations carry no clickable content at all; three more carry only a person
**severity** HIGH · **layer** GAME · **status** FIXED (0.1-fix4)

> **Fixed. Every location in the game now has something to click, and every one of the twelve
> `[[npcs.schedules]]` rows has a surface** — a hub for nine of them, a walk-in join for the three
> the board always intended to serve that way (Tam in the flat, Tam and Roan at the lets).
>
> Six new portrait hubs: `hub_roan_front`, `hub_ewan_slip`, `hub_tam_row`, `hub_nessa_booth`,
> `hub_ewan_counter`, `hub_nessa_asleep` — twelve rungs between them. The three rooms that had
> **zero** clickable content of any kind now return content at the hour their person is there.
>
> **The declared anchor became the real one.** `location fill` had been naming
> `the_chip_shop_flat` as the anchor-as-built against a ledger that declared `the_arcade`; with
> both of the arcade's people finally given surfaces it now reads
> **`anchor the_arcade 18%`**. The room the plan budgeted largest is at last the room the game is
> largest in.

Computed by taking every location-bound canvas that actually renders in a room's list — repeatable,
not `substitution_only`, not `trigger_mode = "random"`, not a portrait:

| location | clickable activities | portrait hub | dead time |
|---|---|---|---|
| **the_front** (the root) | **0** | — | always |
| **harbour_end** | **0** | — | always |
| **terrace_row** | **0** | — | always |
| the_boat_yard | 0 | Ewan 08:00–18:00 Mon–Sat | **64% of the week** |
| the_terrace_house | 0 | Roan 17:00–23:00 daily | **75% of every day** |
| the_back_room | 0 | Nessa 13h/day | 46% of every day |
| the_arcade (anchor) | 3, all schedule-windowed | — | 19:00–21:00 and 01:00–08:00 |

A random ambient is not content the player can choose — `trigger_mode = "random"` rolls a chance
and can legitimately produce nothing, which is the same reason `the opening opens a door` refuses
to count one (§O3).

**The instrument cannot see this.** `a place is not a catalogue` has a **ceiling** of 8 decisions
and no floor, so it passes at *"rooms median 2, 0/7 at the cap"*. The `screen shape` lint prints
*"median 1 ROWS render on a screen at turn one"* and flags three locations as `[one lever]`, but
the headline reads as a shape note, not as *three rooms are empty*.

---

### P2 · Five declared `serves.people` entries have no surface — two of them at the anchor
**severity** HIGH · **layer** GAME · **status** FIXED (0.1-fix4)

> **Fixed, and nothing was invented to do it** — `v2_state.json` `board.locations[].serves` had
> already named the person for every one of the five. The build simply never delivered them:
> Roan on the front, Ewan at the slip, Tam on the row, and **both** of the anchor's people.
>
> The nav-card half is what made it worse than an empty room —
> `getNpcsPresentAtLocation` (`v2.py:19350`) advertises a portrait badge for every scheduled NPC
> whether or not anything is clickable, so the player saw Ewan's face on the Harbour End card,
> paid the 15-minute walk, and arrived at a coin-flip ambient. The badge now tells the truth.

`v2_state.json` `board.locations[].serves` records what each room is for. Crossed against
`[[npcs.schedules]]` and the built canvases:

```
the_front       serves.people = [npc_roan]              Roan walks it 09:00-11:00 daily     no surface
harbour_end     serves.people = [npc_ewan]              Ewan there 07:00-08:00 daily        no surface
terrace_row     serves.people = [npc_tam]               Tam there 07:00-08:00 daily         no surface
the_arcade      serves.people = [npc_nessa, npc_ewan]   Nessa Fri/Sat 12-17, Ewan Mon 19-20:30   no surface
```

Eight of the thirteen schedule rows have no interaction surface. Three of those are deliberate —
Tam at the lets, Tam in the flat, Roan at the lets are the walk-in joins and they work. The five
above are not.

**It is worse than invisible.** Every nav card renders a portrait badge for each NPC scheduled at
the destination (`v2.py:19350`, `:19374`), and that badge is schedule-occupancy, not canvas
availability — the generator's own comment says the two *"intentionally differ … for hub-less
occupancy rooms"*. So the player sees Ewan's face on the Harbour End card, pays the 15-minute
travel cost, and arrives at a room with a coin-flip ambient in it.

**The anchor is the sharpest case.** `the_arcade` is budgeted at 9,000 words, has both of its
declared people standing in it on a schedule, and carries **no portrait hub for either**. That is
why it delivered 1,064 words — 12% of its budget — and why the built game's anchor is
`the_chip_shop_flat` instead.

---

### P3 · This is where the location-fill shortfall actually lives
**severity** OPEN (planned content, not a defect) · **layer** GAME · **status** OPEN

> **Still open by agreement, and moving.** Delivered has gone **7,963 → 9,974** across four repair
> batches, and the shape of the remainder changed more than the number did: the seven surfaces
> this item named as holding 67% of the debt are now built, so what is left is *depth in rooms
> that work* rather than *rooms that do not exist*. The gate stays RED and it is still measuring
> an unpaid debt, not a mistake.

The `location fill` gate reports 7,963 delivered against 33,300 declared. **LO's standing position,
2026-08-22: that shortfall is more game to write, not a bug — the game is being built thin-to-thick
and the budget was declared up front, before the prose.** Recorded here because the *distribution*
is the useful part:

```
the_arcade          9,000 - 1,064  =  7,936      anchor, no hub for either declared person
the_lets            3,500 -   373  =  3,127
the_boat_yard       4,000 - 1,118  =  2,882      portrait only
the_flat            4,000 - 1,214  =  2,786
the_chip_shop_flat  4,000 - 1,479  =  2,521
the_terrace_house   3,500 - 1,166  =  2,334      portrait only
the_back_room       3,000 -   917  =  2,083      portrait only
the_front             900 -   302  =    598      nothing
harbour_end           700 -   148  =    552      nothing
terrace_row           700 -   182  =    518      nothing
                                     ───────
                                      25,337
```

The three empty rooms, the three portrait-only rooms and the anchor account for **16,903 of the
25,337 — 67%**. The thick pass is not spread evenly across ten rooms; it is concentrated in the
seven surfaces P1 and P2 name, and the board's own `serves` field already says what goes in them.

---

### P4 · `show_when_blocked` is used zero times, here and in the whole repo
**severity** MED · **layer** GAME · **status** FIXED (0.1-fix4)

> **Fixed — and this is the primitive's first use anywhere in this repo.** All five windowed solo
> activities now carry `show_when_blocked` and a `cooldown_message` of their hours:
> ```
> Open up and work the counter — mornings, eight till one
> Work the counter            — afternoons, one till seven
> Cash up after close         — after the shutter comes down, nine till one
> Take a turnaround           — the agency's key, nine till five
> Sleep                       — after nine at night
> ```
> Verified live: at 14:00 the arcade shows the morning band **dimmed with its hours** beside the
> live afternoon one, and at 03:00 all three publish their hours instead of vanishing. A room
> whose content disappears reads as a broken game; a room that says when to come back is a
> timetable. `the-clock.md` C5 · `the-surfaces.md` R2.

Six canvases in this game carry a schedule window. When the window closes they **vanish** from the
room's list with no line and no reason, which is what makes the arcade read as broken at 07:36
(§O3) and at 20:00. `show_when_blocked = true` plus `cooldown_message` keeps the entry as a dimmed
line carrying the author's own words (`v2.py:11055-11059`, rendered at `v2.py:5143`).

`the-clock.md` C5 and `the-surfaces.md` R2 both now require it. Usage across all ten games in this
repo: **0**. Off Season's repair is the first real instance, exactly as C5 says.

---

# 8 · Lines that are false at the moment they render

`the-clock.md` C2 makes this test: *read the line at the last minute of the canvas's window — is it
still true?* C2 covers the **hour** only. Every item below is the same failure on an axis C2 does
not name.

---

### T4 · "It's not Monday" is said to her on Mondays
**severity** MED · **layer** GAME · **status** FIXED (0.1-fix2)

> **Fixed.** → *"You don't come down here. What's gone wrong?"* Same beat — she never visits —
> without a claim about the day. Verified live on a Monday.

`5_scenes.toml:453` — `hub_ewan_yard`'s opener:

> *"It's not Monday. What's gone wrong?"*

Ewan's yard row is `weekdays = [0, 1, 2, 3, 4, 5]` (`1_metadata_and_locations.toml:255`) and
weekday 0 is Monday — his arcade row is `weekdays = [0]` with the comment *"Monday evening at your
counter"*. The hub is repeatable and renders on every day he is present, so on one day in six the
first thing he says is wrong.

---

### T5 · "It is Thursday" fires on all seven days, beside a hardcoded take
**severity** MED · **layer** GAME · **status** FIXED (0.1-fix2)

> **Fixed.** → *"Whatever the figure is, it is not ninety. It has not been ninety since the
> clocks went back."* All three faults go at once: the currency name, the day that was wrong six
> times in seven, and the figure the sidebar was already printing correctly beside it.

`3_activities.toml:480` — `work_arcade_after_close`, `weekdays = [0…6]`, window 21:00–01:00:

> *"Forty-one pounds sixty. The pitch is ninety. It is Thursday."*

Two failures in one sentence. The day is a reading, false six days in seven. And **forty-one pounds
sixty is a number the game is already tracking** — the player's `money` trait is on screen in the
sidebar while the prose asserts a different figure.

**This is the half of C2 the doctrine does not state.** The rule is written about the clock; the
same test applies to the day of the week and to any quantity the state actually holds. The
`the clock in the prose` lint scans hours only, so neither half of this line is visible to it.

---

### T6 · One hub covers both of Nessa's windows and narrates the wrong one
**severity** MED · **layer** GAME · **status** FIXED (0.1-fix2)

> **Fixed by windowing the hub** to `12:00-15:00`, her waking row. A portrait hub honours a
> schedule — `selectNpcPortraitCanvasesForLocation` runs every candidate through `isCanvasValid`
> (`v2.py:4482-4498`). Verified live: her hub renders at 13:00 and does not at 02:00.
>
> ⚠️ **Known gap, and it is deliberate.** Her arc is now reachable in a 3-hour daily window and
> her 22:00–08:00 presence has **no surface at all**. That is `the-surfaces.md` R1 — one canvas
> per (who × when) — saying a canvas is *missing*, not that this one should widen. **The night
> hub is content and belongs with §P1/§P2**, and it is the first thing the rooms batch should
> write. A true line in a short window beats a false one in a long one.

`hub_nessa_back_room` carries no schedule of its own, so it renders on **both** of her rows:

```
22:00-08:00   "asleep behind the curtain with the arcade humming through the wall"   10 hours
12:00-15:00   "sat on the mattress on her phone with the curtain half back"           3 hours
```

The opener (`5_scenes.toml:903`) says *"She is on the mattress with her back against the wall and
her phone up"* and she speaks — *"I've got the forty. It's in my jacket."* Wrong for 10 of the 13
hours she is present.

**There is no fix inside one canvas.** The engine has no time-of-day condition type — the complete
set is `trait`, `flag`, `item`, `pass`, `npc_at_location`, `clothing_slot`, `clothing_item`,
`worn_corruption`, `worn_beauty`, `worn_type` (`v2.py:7736-7844`) — so a `[group]` block cannot band
an opener on the clock. The repair is two canvases with `schedules` windows, which is
`the-surfaces.md` R1 (*one canvas per who × when*) verbatim. A portrait hub **can** carry a
`schedules` window: `selectNpcPortraitCanvasesForLocation` runs every candidate through
`isCanvasValid` (`v2.py:4482-4498`), which checks schedules.

---

### T7 · The clock lint has three blind spots, and one of them is the game's most re-entered surface
**severity** MED · **layer** SKILL · **status** FIXED (0.1-fix2)

> **Fixed, and it was four, not three.** `half [past] <hour>` (as a standalone pattern too, so
> *"Half nine and the flat…"* is caught), a part-of-day pattern, `quarter past|to`, `"the"`
> moved from the stoplist to the allow-list — plus a counting bug: matches are now **deduped by
> span**, because *"at half nine in the morning"* was being counted twice.
>
> **The measurement is the finding.** Re-run over the 25-game corpus, the correction moves the
> **field** from median 1.0 to 1.1 — one game, one true positive — and moves **ours** by a
> quarter to a half (off_season 20.1 → 26.4, steam 29.2 → 36.6, forty_miles 22.6 → 34.4).
> **The blind spots were hiding our defects and almost none of the field's.** It found four
> readings on its first run that no earlier pass had listed, two of them the opening line of a
> milestone one-shot.
>
> Dropping the allow-list entirely was tested and **rejected**: it inflates the field to
> 1.2 / 2.6, which is noise being scored. `FIELD_MEDIAN` / `FIELD_P75` updated to 1.1 / 2.1 and
> `the-clock.md`'s published table re-measured with the shipped function.

`_CLK_PREP` (`scripts/gates.py:2117`) requires a preposition before the hour, and `"the"` sits in
`_CLK_BAD_NEXT` (`:2128`) to kill the *"at one point"* idiom that made a first draft 90% noise. Both
choices have costs. An independent scan of every beat found four real readings the lint does not
report:

```
2_one_shots.toml:105   "By nine the whole flat is above freezing"      "the" is in _CLK_BAD_NEXT
2_one_shots.toml:128   "The immersion clicks off at half nine"         "half" is not in _CLK_WORDNUM
5_scenes.toml:272      "at half nine in the morning"                   same
3_activities.toml:1101 "Seven in the morning and the fryers…"          no preposition at all
```

`5_scenes.toml:272` is the **entry node of `loop_tam_bed`** — the surface `the_want.md` names as the
crudest and most re-entered in the game, off a hub whose presence window is 08:00–15:00. Its first
sentence states a clock time true for one minute in 420.

`half <hour>` is already on the `own_words` lint's ambiguous list (8 uses, *"7:30 here, 6:30 across
much of Europe"*), so the two instruments are looking at the same string and neither counts it as a
clock. Three fixes, all cheap: add `half` to the hour vocabulary, allow an hour at a sentence start,
and replace the blanket `"the"` exclusion with a check that the following words are not a duration
noun.

---

# 9 · Systems switched on and left empty

---

### O5 · The wardrobe renders a live link to an empty page, first in the room
**severity** MED · **layer** GAME · **status** FIXED (0.1-fix1)

> **Fixed by switching the system off.** `clothing_enabled = false`; `wardrobe_location` commented
> out beside it. Verified safe first: off_season has **zero** `clothing_slot` / `clothing_item` /
> `worn_*` conditions, so nothing depended on it. Live: no `Change Clothes` link anywhere in the
> flat. Re-arm it in the release that authors a wardrobe surface and a beat that teaches it
> (`the-first-hour.md` F4). **§O4 stays OPEN** — this closes the broken link, not the missing
> system.

Extends §O4, which recorded the clothing system as *untaught*. It is worse than untaught: it is
**visible**. `clothing_enabled = true` and `wardrobe_location = "the_flat"`
(`0_systems_spec.toml:47-48`) make the generator emit a wardrobe link on that location's passage
unconditionally (`v2.py:9601-9602`), and the built game carries it:

```
<h2>Your Flat</h2>
<p>Up the inside stair from the arcade floor…</p>
[[Change Clothes->WardrobePage]]<br>              ← first link on the screen
<<= setup.renderNpcPortraits("the_flat")>>
<<= setup.renderSoloActivities("the_flat")>>
```

`setup.clothing_data = []` in the same build. The first clickable thing in her own flat is a link to
a page with nothing on it.

---

### O6 · Money prints twice in the sidebar, both times as the raw key, one against a fake ceiling
**severity** MED · **layer** GAME + ENGINE · **status** PARTLY FIXED (0.1-fix1) — the doubling stands

Three separate misses stacking on one trait:

1. **The doubling.** `hiddenTraits = ["warmth", "hunger", "energy", "arousal", "loop_stage"]` in the
   build — `money` is not in it, so the auto Traits dump prints it (`v2.py:15557` in dev,
   `:15604` in a release build) **and** the authored `trait_bar` prints it.
   `engine.md` §30 exactly; gate 27 misses it because gate 27 only checks *banded* items and money
   is deliberately unbanded.
2. **The label never appears.** `[[traits.labels]] key = "money", label = "Change bag"`
   (`0_systems_spec.toml:156`) is read only by `_labelForTrait` for condition text. The `trait_bar`
   takes its label from `_item.label || _tbKey` (`v2.py:16215`) and the dump prints `<<print _k>>`,
   so both rows read **`money`**. `engine.md` §33.3.
3. **The fake maximum.** The sidebar item (`0_systems_spec.toml:150`) declares no `max`, and
   `_traitMax` defaults to 100 (`v2.py:16214`). The bar renders **`money: 22 / 100`** at 22% fill —
   against a currency with no ceiling whose weekly obligation alone is 90.

The board file's comment says *"Countable resource: the exact figure, NO bands."* The intent is
right and none of it reached the screen.

> **Fixed: 2 and 3.** `label = "Change bag"` and `max = 90` are now on the sidebar item.
> The bar renders **`CHANGE BAG: 22 / 90`**, and 90 is not invented — it is
> `[settings.rent] amount`, so the bar reads as how much of Monday she has.
>
> **NOT fixed: 1, the doubling — and it was tried.** `hidden = true` on `money` does
> suppress the second row, and it costs more than it saves: `hidden` is one switch driving
> **two** surfaces (`v2.py:1220-1226`, *"playerTraits/npcTraits widgets + Stats page"*), and
> money is the only unhidden player trait in this game. Built and read both ways in a
> release build:
>
> ```
> hidden = true    sidebar    a permanent box headed "Traits" with no rows in it
>                  StatsPage  "You (Marnie)" with nothing under it, beside four listed NPCs
> hidden = false   sidebar    CHANGE BAG: 22 / 90   +   Traits | money 22
>                  StatsPage  You (Marnie) | money 22
> ```
>
> A redundant row beats two empty boxes, so the doubling stays. **The real fix is an ENGINE
> change** — `<<playerTraits>>` is unconditional in `StoryCaption` (`v2.py:15672`, `:15687`)
> and renders its header even with zero visible rows; it should skip the widget when every
> `core_trait` is hidden. Two lines, and LO's call, not this batch's.

---

### O7 · Three dead flags and one sink that was never built
**severity** LOW · **layer** GAME · **status** FIXED (0.1-fix4)

> **The sink is built.** *"diesel for the van — harbour_end — $12"* is now
> `rung_ewan_diesel`, a choice on the new slip hub. It could not exist before because harbour_end
> had no canvas that could spend anything.
>
> It is a choice on a **hub** rather than a solo activity on purpose: a solo repeatable canvas
> plus a scheduled NPC makes a location qualify for the walk-in floor (`_walkin_join`), and a
> portrait hub carries `npc` and does not. It is also the only rung in the game where **money buys
> a meter**, and for Ewan that is exact — `the_want.md` gives him `hold` alone, *"priced, never
> courted"*. Verified live: $50 → $38, and it burns the day's Ewan rung.

From a full setter/reader census of the merged TOML:

```
arrival_done          set at 2_one_shots.toml:73    read by nothing
nessa_curtain_open    set at 2_one_shots.toml:331   read by nothing   (declared in her flag_keys)
tam_stayed            set at 5_scenes.toml:412      read by nothing   (declared in his flag_keys)
```

`the-meters.md` W3 — *a number nothing reads is not a meter* — is written about traits; the board
file records two traits cut for exactly this reason (`takings_today`, `tenant_slot`). The same test
was not run over the flags.

And `v2_state.json` `board.economy.sinks` declares six. Five are built. **`"diesel for the van —
harbour_end — GBP 12"`** is not, and cannot be: `harbour_end` has no canvas that can spend anything
(§P1).

> **`arrival_done` deleted** (`2_one_shots.toml`). It duplicated `season_shut`, which does the
> arming, and nothing read it.
>
> **`tam_stayed` and `nessa_curtain_open` KEPT, deliberately.** Both are arc flags on a
> character's declared `flag_keys`, set once by a milestone, and both are the natural hook for
> the 0.2 content their arcs are heading toward. They cost nothing at runtime and deleting them
> buys a re-add. Recorded in `v2_state.json` as declared hooks so they read as intent rather
> than as debris — which is the difference between this and `arrival_done`.
>
> **The diesel sink is deferred to the rooms batch,** where `harbour_end` gets a surface that
> can spend anything at all (§P1, §P2). Deleting it from the ledger now would hide the debt.

*Checked and NOT a defect:* `lease_called` is read four times and set by no canvas. That is correct
— the **engine** sets it when the payment is missed past grace (`v2.py:16006`) and registers itself
as the setter so the flag-chain validator does not raise (`v2.py:11504-11512`).

---

# 10 · What the plan promised and the build did not deliver

---

### G1 · `the_want.md` promises act loops on four hubs; one shipped
**severity** HIGH · **layer** GAME · **status** FIXED (0.1-fix5)

> **Fixed. Four hubs, four loops.** `rung_ewan_caravan`, `rung_roan_stay` and
> `rung_nessa_curtain` are now `loop_ewan_caravan`, `loop_roan_stay` and
> `loop_nessa_curtain` — node-routed pose ladders with R3b's full six parts: an act node per
> rung with its own pool, a self-loop, switch links **both** ways, an arousal-gated finish, a
> finisher electing on `loop_stage`, and a reset on entry and on both exits. The lint reads
> **2 loops / 6 cascades → 5 loops / 3 cascades**.
>
> **The cascade prose was the raw material, not scrap** — the beats already were the rungs, so
> converting meant re-cutting them into act nodes rather than rewriting them.
>
> **The three cascades left are left on purpose.** `walkin_flat_stairs` is a router branch that
> R3 sizes at *"one or two paragraphs plus a media pool"*; `work_arcade_after_close`'s floor beat
> is solo texture at a location whose solo loop already exists upstairs; `rung_tam_nothing` is
> the stair **to** Tam's loop. R3b's own warning — *"one good loop beats four thin ones"* —
> cuts against converting them.
>
> **And the game reached its ceiling for the first time.** `the_want.md` §6 puts `fuck` in the
> **0.1** column for Tam and Roan and `cunt` in Ewan's **later** column; the build had no
> penetration anywhere, which is CLAUDE.md's *"writing under the ceiling is the defect"*. Roan's
> and Tam's ladders now top out at penetration, Ewan's at her mouth (his ladder is one-directional
> in 0.1 because he does not reach her), and Nessa's at fingers and tongue. **A hand audit of
> every crude term in all four loops against her own 0.1 column: zero breaches.**

`the_want.md` §6, and `v2_state.json` `want.crude_register_lives_in` verbatim:

> *"The act loops on the four hubs, and above all Tam's pose ladder in the flat over the chip shop
> — the surface a player will re-enter more than any other."*

Built: **`loop_tam_bed` only.** Ewan, Roan and Nessa each got a fixed five-beat cascade instead —
`rung_ewan_caravan` (`5_scenes.toml:611`), `rung_roan_stay` (`:834`), `rung_nessa_curtain`
(`:1026`). Each is repeatable, day-capped and re-enterable, and each replays **identical prose**
every time; only the media pool re-rolls.

`the-surfaces.md` R3b: *"a repeatable explicit surface is a node-routed loop; a one-time scene is a
cascade."* The `act menu` lint already counts it — *"2 act-menu loops and 6 one-shot cascades across
8 repeatable explicit surfaces"* — and prints it as a count, not a miss. Read against the want, it
is a miss: three of four characters have no player agency inside their sex surface.

The prose itself is not the problem. The cascades hold the register — crude, on the body, interiority
in its own `"After."` beat, a clip per beat — and are the best writing in the game. What they lack
is the machine.

---

### G2 · Two locked doors unlock onto themselves
**severity** MED · **layer** GAME · **status** FIXED (0.1-fix1)

> **Fixed by making the lock hold.** Both `npc_tam.want` grants capped at 60 —
> `rung_tam_nothing` (+5) and `loop_tam_bed.finish` (+6) are the only two effects in the game that
> write it — so `want >= 65` is unreachable and the pair stays visible-and-locked, which is what
> `promises[0]` says they are. Live: want 58 + 5 clamps to 60, and *Get on top of him* still
> renders greyed at want 60.
>
> **A debt with a due date, recorded against the promise, not just here:** 0.2 must raise the cap
> **in the same change** that builds the content behind those doors.

`5_scenes.toml:324` and `:372`, inside `loop_tam_bed`:

```toml
text             = "Get on top of him."      nodeId = "hands"    show_when_locked = true
conditions       = npc_tam.want gte 65

text             = "Sit on his cock."        nodeId = "mouth"    show_when_locked = true
conditions       = npc_tam.want gte 65
```

Both target **their own node**. As advertising for 0.2 that is correct and it is on the promise
ledger (`v2_state.json` `promises[0]`, `paid_in: null`) — but `want` has no `cap` and rises +6/day
(`rung_tam_nothing` +5 and `loop_tam_bed.finish` +6 share `tam_rung_today`), so 65 arrives in about
eleven days of ordinary play. When it does, the player clicks *"Get on top of him"* and is served
the handjob node they were already on.

A locked door is only a promise while it stays locked. Either cap `want` below 65 for this build,
gate the pair on a flag 0.2 sets, or route them somewhere real.

**Candidate check, mechanical:** a `show_when_locked` choice whose `nodeId` resolves to the node it
sits on is always either a self-loop or a dead promise.

---

### G3 · The hub→rung split made two pairs of screens narrate the same action twice
**severity** MED · **layer** GAME + SKILL · **status** FIXED (0.1-fix6)

> **Fixed by giving the two screens different jobs.** The hub is now the **decision** and the rung
> the **outcome**:
> ```
> act_flat_meter   the slot, shoulder height, coins only, a card taped under it in her
>                  husband's handwriting saying what three buys
> rung_flat_meter  six coins in, the heater starting behind the plaster, three days of it
>
> act_chip_eat     there is always something in the pan and always four to put through the
>                  hatch, and neither of them has called that an arrangement out loud
> rung_chip_eat    what he made at four, warmed through on the one ring that works
> ```
> Gate 26 forced the split and nothing told the author the screens then differ. `work_arcade_morning`
> → `rung_arcade_take_am` had always done it right; these two now match it.

Gate 26 correctly forced the grants off the room-reachable canvas and onto a triggerless rung — the
board file records the reasoning. Nothing told the author that the two screens then have different
jobs, so both narrate the same beat back to back:

```
3_activities.toml:98    act_flat_meter   "Six fifties out of the change bag into the slot on the
                                          wall, and the immersion starts up behind the plaster…"
3_activities.toml:1284  rung_flat_meter  "Six fifties into the slot and the immersion starts up
                                          behind the plaster…"

3_activities.toml:796   act_chip_eat     "…because he makes it at four in the morning coming off
                                          the fryers and never finishes it."
3_activities.toml:1450  rung_chip_eat    "Whatever he made at four in the morning, warmed through
                                          on the one ring that works…"
```

`work_arcade_morning` → `rung_arcade_take_am` does it right: the hub is the room, the rung is what
happened. The rule the skill is missing in one line: **when a brake forces a hub→rung split, the hub
is the decision and the rung is the outcome; they may not both narrate the act.**

---

### G4 · Two loop labels say "Keep going."
**severity** LOW · **layer** GAME · **status** FIXED (0.1-fix1)

> **Fixed.** `loop_flat_solo.act` → *"Keep working your clit."*; `loop_tam_bed.hands` → *"Keep
> working his cock."* Each names the act its own node is on and matches the sibling label in the
> same loop.

`3_activities.toml:1339` (`loop_flat_solo.act`) and `5_scenes.toml:305` (`loop_tam_bed.hands`).

`the-voice.md` R1: *"A loop whose exits say Continue or Go on has thrown away the only readable
thing about it."* The sibling node in the same loop gets it right — `loop_tam_bed.mouth` ships
*"Keep him in your mouth."* Both misses are one self-loop label each.

---

### G5 · Two accuracy slips
**severity** LOW · **layer** GAME · **status** FIXED (0.1-fix2)

> **Both fixed.** *"a day and a half"* → *"about three days"* in both meter screens (+45 warmth
> against a decay of 12/day from a base of 18). And `the_want.md` §6's crude ceiling moved to
> match what shipped — *cum / come in* was sitting in the **opens later** column for Tam and
> Ewan while the prose was already there. **The prose was right and the table was stale**, so
> the table moved, in `the_want.md` and in `v2_state.json` `want.crude_ceiling`. A ceiling that
> lags what shipped is worse than no ceiling, because the next release reads it and writes
> under it.

- **The meter's stated duration.** Both meter screens say three pounds buys *"about a day and a
  half"* of warmth. The grant is +45 capped at 100 (`3_activities.toml:1287`) against a decay of 12
  a day (`1_metadata_and_locations.toml:82`) and a gate at 30 — from her starting 18 that is
  **about three days**, not a day and a half.
- **The crude ceiling.** `the_want.md` §6 puts *cum / come in* in Tam's and Ewan's **"opens later"**
  column, and the build ships *"he comes in your mouth"* (`loop_tam_bed.finish`) and *"He comes over
  your knuckles"* (`rung_ewan_caravan`). Either the table is stale or the scenes overshot; the want
  is the spec each release is checked against, so the two need to agree. **Not a register defect** —
  the writing is correct and under no other ceiling.

---

### G6 · The map lint's two hits are false positives — recorded so they are not re-investigated
**severity** LOW · **layer** SKILL · **status** WONTFIX (nothing to fix — it is a record)

> Filed OPEN by mistake: this item never described a defect. `"hall"` and `"stairs"` are
> interior features of locations that exist, both sentences are correct, and the lint's own
> either/or (*"either the location is missing, or the sentence is wrong"*) is a false dichotomy —
> a room has parts. Teaching the lint that would cost more than it saves. Closed as a record.

`the prose names places the map does not have` reports `"hall" ×4` and `"stairs" ×3`. Both are
**interior features of locations that exist** — the hall in `the_terrace_house`, the stairs inside
`the_flat` and up to `the_chip_shop_flat`. Neither is a missing location and neither sentence is
wrong. The lint's own note (*"either the location is missing, or the sentence is wrong"*) is a
false dichotomy: a room has parts, and naming one is not a map claim.

---

# 11 · The ladders had no bottom

---

### W1 · Six meters, and the first thing any of them does sits four to eight clicks away
**severity** HIGH · **layer** GAME + SKILL · **status** FIXED (batch 7)

> `the-meters.md` **W4**: *"A meter that carries a game has eight or more rungs, and the lowest one
> sits around 5."* Field: **8–17 rungs, densest at the bottom, lowest rung at a median of 5**, and
> the rule's own sentence for the failure is *"the opening of a v2 game is fifteen clicks in which
> nothing the player does changes anything."*

Measured on the repaired build, before this batch:

```
meter              rungs  lowest   thresholds
npc_tam.ease           1      20   [20]                <- ONE rung
npc_nessa.trust        2      20   [20, 40]
npc_nessa.want         2      18   [18, 30]
npc_ewan.hold          3      18   [18, 25, 40]
npc_roan.bond          3      12   [12, 25, 38]
npc_tam.want           3      22   [22, 45, 90]
```

Every lowest rung sat at **12–22** against a field median of 5. Grants run 2–7, so that is four to
eight interactions with a person before anything they say or do changes — in a game whose whole
declared shape is *the cast climbs, not the player*. Two of the hub descriptions had already
written the correct answer and the build never had it: `hub_roan_house` said *"Small rungs at
4/12/25/42"* while the first gate sat at 12, and `hub_nessa_back_room` said *"trust rungs at 5/20"*
while the 5 did not exist.

**Fixed:** 18 new rungs, so every meter has a bottom at 4–5 and a dense lower half.

```
npc_ewan.hold      6 rungs  [5, 10, 18, 25, 32, 40]
npc_nessa.trust    5 rungs  [5, 10, 20, 30, 40]
npc_nessa.want     5 rungs  [5, 12, 18, 24, 30]
npc_roan.bond      7 rungs  [4, 8, 12, 18, 25, 32, 38]
npc_tam.ease       4 rungs  [4, 8, 12, 20]
npc_tam.want       5 rungs  [22, 30, 38, 45, 90]
```

Two shapes, both of which keep the player to **one interaction per person per day** — this deepens
the climb without inflating it:

- **Four banded talk screens**, one per character (`talk_tam_step`, `talk_ewan_bench`,
  `talk_roan_bristol`, `talk_nessa_hum`). The same question at three or four bands of the meter,
  and a different person answering it. Each shares the existing `<npc>_talk_today` cap with the
  talk screen already on that hub, so the hub gains a *way to spend* the day's conversation, not a
  second one. `register.md` S4's content kind — the talk-screen share moves **6% → 10%** (vesper
  26%, field 29%). *(Batch 8 then added 19 canvases and diluted that back to 8% without removing a
  single talk screen — the count is 9 either way. Read the count, not the share.)*
- **Six banded hub openers** — `hub_tam_row`, `hub_roan_front`, `hub_ewan_counter`,
  `hub_nessa_booth`, `hub_nessa_asleep`, `hub_nessa_back_room`. One `[group]` ladder per node, so
  the most re-entered screens in the game change under the player rather than repeating. These cost
  **no choices at all**: `a place is not a catalogue` still reads character hubs at a median of 2.

`somebody speaks` **improves** for the first time in seven batches — **4.8:1 → 3.9:1** against a
5.0 ceiling — which is the test of whether the new screens are really talk screens.

**Left standing, deliberately:** `npc_tam.want` keeps its lowest rung at 22, so the ladder lint
still prints *"1 of 6 meters change nothing below 22"*. `want` is a second meter that cannot move
at all until `tam_saw_you`; the low feedback for Tam lives on `ease`, which now starts at 4. The
lint has no way to know that, and a rung at 5 on a meter that is pinned at 0 for the first act
would be theatre.

---

### W2 · The ladder lint implemented one side of a fork the doctrine declares
**severity** MED · **layer** SKILL · **status** FIXED (batch 7)

`lint_meter_ladder(game, state)` returned before measuring anything:

```python
tiers = ((state or {}).get("board") or {}).get("ascent_tiers") or []
if not tiers:
    return "", []
```

…and `_meter_rungs` skipped per-character meters by construction (`node.get("subject") == "npc"`).
`the-meters.md` **W1** makes *who climbs* a **declared fork** — a ladder game where the player
climbs, or a roster game where the cast does — and off_season is the only roster game in the repo
(`who_climbs = "cast"`, `ascent_tiers = []`). It was therefore the only game the ladder lint
printed **nothing** for:

```
back_home / forty_miles / seventh_day / steam / the_allowance   3-4 tiers measured
off_season                                                      SILENT
```

Same shape as §T7 (the clock lint's blind spots) and batch 6's currency sub-units: **the doctrine
was right and the check covered part of it**. Fixed by `_cast_meter_rungs`, chosen off
`board.who_climbs`, printing `N cast meters` where the ladder games print `N declared tiers`.

**One instrument bug found while running it red.** Three of the six meters reported a rung at
**110** — batch 5's declared 0.2 doors, deliberately unreachable against grants capped at 100. A
gate above the meter's ceiling is a locked door (`the-release.md` G9), not a step anything can
climb to, and counting it credited the game with a rung it can never reach. `METER_MAX = 100` now
drops them on **both** sides of the fork.

Verified red-first, and byte-identical for the five ladder games (`PYTHONHASHSEED=0` — three games
carry pre-existing tie-break noise unrelated to this change). **No gate moved on any of the twelve
games.**

---

# 12 · The walk-in was one branch deep

---

### V1 · Five dispatching activities, and not one could produce a second outcome
**severity** HIGH · **layer** GAME + SKILL · **status** FIXED (batch 8)

> `the-surfaces.md` **R3**: *"The walk-in — one activity deepens, the room does not widen… this is
> the largest content bucket in the field and the one v2 shipped without."* DoL's `Bath` is **one**
> activity with **twelve** outcome passages. *"The richness is combinatorial, not authored."*

Measured across every game in the repo that dispatches at all — rules, and **distinct outcomes per
host activity**:

```
game                  hosts  rules  distinct outcomes per host   max
back_home                 3      7  [4, 2, 1]                      4
vesper                    5     10  [1, 1, 1, 1, 4]                4
last_call                 1      3  [3]                            3
the_allowance             1      3  [3]                            3
late_shifts               9      9  [1 x9]                         1
the_long_summer_test      7      7  [1 x7]                         1
off_season                5      7  [1 x5]                         1   <- every host, one outcome
```

Off Season's three rules on `solo_flat_warm` are the same walk-in at three chance bands. Everywhere
else the roll decided **whether** the branch or the host rendered, never **which** branch — a coin
flip wearing a dispatcher's coat.

It landed hardest on the anchor. `the_arcade` is declared 9,000 words — 27% of the game — and held
**1,957 (-78%)**, so the built world's deepest room was the chip shop flat and `location fill`
printed *"the world has no centre"*.

**Fixed:** 7 hosts, 29 rules, **`[3, 5, 5, 4, 3, 4, 3]`** — the deepest dispatch in the repo, past
vesper's 4. Thirteen new `substitution_only` branches, every one location-bound (`getCanvasById`
indexes only location-bound canvases, `v2.py:3177`) and day-capped at 1.

```
work_arcade_morning     1 -> 5   the tenant · the pusher · the damp · the dog man · Ewan for the book
work_arcade_afternoon   1 -> 5   + Roan in out of the wind · the name over the door
work_arcade_evening     -  -> 4   NEW HOST — see V2
work_arcade_after_close 0 -> 3   the hum stopping · somebody tries the shutter · Tam at the side door
work_lets_turnaround    1 -> 4   number two has been slept in · the agency rings · the salted lock
act_chip_eat            1 -> 3   Lee rings about the nights · the fryers going on below
solo_flat_warm          1 -> 3   the meter going · the floor going quiet
```

Every one of them is **Pattern B** except the flat, which keeps Pattern A on purpose: groups are
processed before independent rules (`v2.py:5359`), so a group there would take 22% off Tam's band
before it rolled, and him coming up the stairs is the flat's headline content. The two new branches
are declared **after** his bands and only roll on the nights he does not come up.

**The anchor is now the centre of the world.** `the_arcade` 1,957 → **3,640**, and *"no anchor as
built — the world has no centre"* is gone from the gate output for the first time since the game
shipped. `location fill` still fails on the word budget: **12,118 → 14,472** of 33,300.

---

### V2 · The last two hours the building is open had no surface
**severity** MED · **layer** GAME · **status** FIXED (batch 8)

The counter ran **08:00–13:00** and **13:00–19:00**; the shutter comes down at nine and after-close
starts at **21:00**. Between them, every day of the week, the arcade was open and had nothing in it
but a 90-minute Monday hub. `the-surfaces.md` R1 — one canvas per (who × when) — naming a hole.

`work_arcade_evening` is the fourth band of the **same job**, not a second till (R2: *"one per job,
not one per till-shaped noun"*). It shares `counter_done_today` with the other two, so there is still
exactly one take a day, and it is the smallest of the three.

---

### V3 · The walk-in gate counts branches; the rule is about how many
**severity** MED · **layer** SKILL · **status** FIXED (batch 8)

`the walk-in floor` passes **4/4** on `subs[loc] > 0` (`gates.py:1604`) and says so in its own
comment: *"one walk-in per qualifying room; the rest is the author's call."* That is a defensible
floor and it is not the rule. Nothing in the instrument had ever printed how deep a dispatch goes.

Fourth time this shape has appeared — §T7 (the clock lint), batch 6 (currency sub-units), §W2 (the
ladder lint's half-fork), and now a gate that tests for **one** of a thing whose whole point is
**many**.

`lint · dispatch depth` now prints hosts, rules, distinct outcomes, and — because the mechanism is
invisible in the TOML — **the host's own survival odds**. Two corrections were needed before it
shipped, both to stop it printing a wrong number: it first multiplied every rule's chance (right for
`back_home`'s four cumulative `exposure` rules, wrong for bands where one can pass), and it then
picked the largest co-satisfiable set, which made the answer depend on declaration order. Both are in
the skill `CHANGELOG.md`.

**And it immediately found a latent defect in this game.** `solo_flat_warm`'s three bands are
described as one-of-three and the first one never said so — `ease lt 20` alone is satisfied at the
same time as `want gte 22`, so a player at low ease and high want had **two of the three live** and
the canvas rendered itself 11% of the time. Fixed by adding `want lt 22` to the first band. Nobody
found that by reading it; the instrument found it.

---

### V4 · Read, not fixed — the flat's solo canvas renders 16% of the time at the top band
**severity** LOW · **layer** GAME · **status** WONTFIX (authored intent)

The depth lint prints `solo_flat_warm @the_flat: 5 independent rule(s) — the host renders 16% of the
time`. That is the **worst** case and it is the `want >= 22` band, where Tam comes up the stairs 80%
of the time by design (batch 1) and the two new branches take 22% of what is left. Read the line, not
the number: at the lower bands the canvas renders 55–70% of the time, and at the top the substitution
IS the content. Recorded so it is not "fixed" later.

---

# 13 · The act loops were written warm

---

### H1 · The four character loops carried one explicit beat each; the two solo loops carried three
**severity** HIGH · **layer** GAME + SKILL · **status** FIXED (batch 9)

> `the_want.md` §6, this game's own spec: *"The crudest writing in this game is in the **act loops**
> on the four hubs, and above all in Tam's pose ladder over the chip shop — the surface a player will
> re-enter more than any other."* And: *"Crude is the default at the sexual register, not a mode…
> The ceiling is a ceiling and never a floor — writing under it is the defect."*

Measured, act node by act node, with the game reading a comfortable `explicit floor` pass:

```
loop_arcade_floor    bare=5  glass=7   finish=4          <- the two SOLO loops
loop_flat_solo       act=6   act_deep=4 finish=3
loop_tam_bed         hands=1 mouth=3   astride=2 finish=3
loop_ewan_caravan    hands=4 mouth=1   finish=0
loop_roan_stay       hands=2 fingers=2 fuck=1   finish=5
loop_nessa_curtain   hands=2 fingers=2 mouth=3  finish=1
```

**10 of 21 act and finish beats were under 3** — the count `register.md` needs to call a beat
explicit at all. Nine of the ten are in the four **character** loops. The solo loops, written by the
same hand in the same week, are twice as crude as the ones with a person in them.

The worst was `loop_ewan_caravan.finish`: **zero body words on 127**. Three paragraphs of a man
coming — *"he comes in your mouth"*, *"comes over your knuckles"* — and not one of them names a
cock, a fluid or a body. Then its last two beats are about **the desk**. That is `register.md`'s
pivot, in the finisher of a whole arc.

`loop_roan_stay.fuck` was a penetration node whose only body word was *"fucks"*. `loop_tam_bed.hands`
scored 1 on 47 words, on the ladder the want names as the crudest surface in the game.

**Fixed: 10 act beats and 9 finisher bands rewritten IN PLACE, not extended.** The beats were already
the right length; they were hedged. Each stays on the body for its whole length, and the interiority
stays where it already was — its own beat, afterwards, correctly scoring zero.

```
                        before          after
explicit floor          9.6% BARE PASS  15.3%          (17 -> 27 explicit beats of 177)
explicit in repeatable  88.2%           92.6%
an explicit beat clip   88%             93%            (field 91%)
act/finish under 3      10 of 21        0 of 21        on the THINNEST band each renders
somebody speaks         4.2:1           4.3:1          in-place rewrite, so it barely moved
own_words               67              67             no new locale-locked term
```

Every rewrite stays inside that person's `the_want.md` §6 column and touches nothing from their
*opens later* one — no `cunt` for Ewan, no `fuck` for Nessa, no `cum` for Roan, no `arse` for Tam —
**checked live**, with the choice labels stripped out, because those same words are the text of the
0.2 doors and a locked door is a signpost, not content (`the-voice.md` R4).

---

### H2 · A game-wide heat share cannot see the screen the player is on
**severity** MED · **layer** SKILL · **status** FIXED (batch 9)

`explicit floor` is a percentage of every beat in the game. A game can clear it while every act node
is warm, and averaging is precisely how the measured failure hid: 95% of one game's crude prose
sealed in a room with no exits, all nine repeatable loops at zero, and a passing scoreboard.

`lint · the act nodes` reads the act nodes of every act-menu loop and its finisher — the screen in
front of the player while the thing is happening. It discriminates: `vesper` reads **median 1, 17 of
25 act beats under 3**, which is the same game the 2026-08-10 measurement caught.

Fifth instance of this shape — the clock lint, the currency lint, the ladder lint, the walk-in gate,
and now a floor that measures the game instead of the act.

**⚠️ Two corrections, and PLAY found the first one.** The lint first read `Beat.explicit`, which folds
a node's `[group]` bands together by design. The live probe then failed on nine finisher **bands**
that the lint had just passed — `loop_nessa_curtain.finish` scored 6 folded and put **two** body
words on screen whichever band fired. A finisher is banded by definition, so the lint now reports the
thinnest band a node can render.

---

### H3 · 158 groups of prose were invisible to every beat-based gate
**severity** HIGH · **layer** SKILL · **status** FIXED (batch 9)

Found while chasing why the new lint printed nothing for one game. `_collect` read a `[group]`
block's children only at the block's own `blocks` key. The importer accepts them **there or** inside
`props.blocks` and normalises to the latter (`template_import.py:6062-6086`); the generator renders
`props.blocks` (`v2.py:13770`). **Both shapes ship. The instrument understood one.**

```
the_long_summer_test    4,979 -> 9,429 words    its anchor location changes; 2 gates flip
late_shifts             5,095 -> 6,017
last_call               4,478 -> 5,017
the_inheritance        12,975 -> 13,045
```

Four games were being scored against roughly half their prose — words, explicit beats, dialogue
split, sentence length, vocabulary, clock references, all of it. **Off Season is not one of them**
and its output is byte-identical; five games write the first shape. Recorded here because it is the
largest single correction the instrument has taken, and because it was found by a lint returning
empty rather than by anyone reading the code.

---

# 14 · State of the build, recorded not filed

- **44 media slots declared, 0 files on disk.** Normal for a game that has not had a `find-media`
  run; noted so the gates' media passes are read correctly.
- `gates.py` **at the time this file opened**: 31/32, the single failure `location fill` — 7,963
  words delivered against 33,300 declared, and no anchor as built (`the_chip_shop_flat` holds 18.6%
  where the plan said `the_arcade` at 27%).
- `gates.py` **as of 2026-08-22**, after the five doctrine passes added five gates: **31/37**. The
  game was byte-identical at that point; the instrument grew. Six failures:

  ```
  location fill                    7,963 of 33,300 · 0/10 on their own budget      §P3 (planned)
  the price is in one currency     `pound` x9 vs the engine's `$`                  §M1-M3
  the opening opens a door         hands over 07:36, nothing open until 08:00      §O3
  every hub is met first           0/4 characters introduced                       §N1
  the anchor introduces itself     the_arcade has no first visit                   §L2 / §N2
  the label keeps its time         "till one" · "till seven"                       §T1
  ```

  Seventeen lints run alongside, none of them scored. The three read as **lists, not numbers** —
  `own_words`, `named_before_met`, `clock_in_prose` — are §L1, §N1 and §T2/§T7.
- `gates.py` **after repair batch 1** (2026-08-22): **32/38**. One gate added — `a day-cap closes`,
  §D4 — and it passes; the six failures above are unchanged, because batch 1 touched none of them.
  The score moved by exactly the one gate the batch was built around.
- `gates.py` **after repair batch 2** (2026-08-22): **34/38**. `the price is in one currency` and
  `the label keeps its time` both flip to PASS and nothing else moves. Four failures remain, and
  all four are content the later batches write:

  ```
  location fill                  7,961 of 33,300 · planned, thin-to-thick        §P3
  the opening opens a door       hands over 07:36, nothing open until 08:00      §O3
  every hub is met first         0/4 characters introduced                       §N1
  the anchor introduces itself   the_arcade has no first visit                   §L2
  ```
- `gates.py` **after repair batch 3** (2026-08-22): **37/38**. The three first-hour gates all
  flip. **`location fill` is the only failure left in the game**, at 8,517 of 33,300, and it is
  the one the doctrine and LO both agree is a debt rather than a defect (§P3).
- `gates.py` **after repair batch 4** (2026-08-22): **37/38** held while the game grew by 1,457
  words and 18 canvases. No gate moved — which is the batch behaving — and two numbers inside
  the surviving failure did:

  ```
  location fill   8,517 -> 9,974 delivered
  anchor as built  the_chip_shop_flat 19%  ->  the_arcade 18%   <- the DECLARED anchor, at last
  ```

  ⚠️ **Batch 2's gate caught batch 4 on the way in.** `the label keeps its time` failed a new
  hub choice reading *"Don't turn the machines off at nine."* — a clock time on a label, which
  is exactly what C3 forbids and exactly what that gate was built for two batches earlier. Three
  words deleted. This is the second time a gate written in an earlier batch has caught a defect
  in a later one.
- `gates.py` **after repair batch 5** (2026-08-22): **37/38** held again. The batch is scored by
  the lints rather than the gates:

  ```
  the act menu      2 loops / 6 cascades  ->  5 loops / 3 cascades
  ends on an opening       1 visible-locked  ->  4, one 0.2 door per character
  location fill      9,974 -> 10,564 delivered
  ```

  ⚠️ `somebody speaks` reached **exactly 5.0:1 against a 5.0 ceiling** mid-batch — act nodes had
  gone voiceless, which `register.md` S3 forbids (*if a person is in the room, they speak*).
  Eight act nodes were given a line each and it settled at 4.8:1. Worth keeping: a batch of pure
  explicit prose is the one that pushes that ratio, and the ceiling caught it.
- `gates.py` **after repair batch 6** (2026-08-22): **37/38** held, and `location fill` is the
  only red gate left in the game. Scored by the lints again:

  ```
  own_words          94 words / 203 uses  ->  63 / 121 · ambiguous 3 -> 0 · false friends 3 -> 1
  currency in prose  caught a REGRESSION first, then went clean
  ```

  ⚠️ **Batch 3 tripped a gate on its way in, and the gate was right.** `milestones open something`
  failed the new `canvas_first_arcade` the moment it existed: a one-shot that sets no flag opens
  nothing. Widening the gate to excuse "first visits" was measured first and **rejected** — a
  blanket *sets-nothing* exemption would have excused **10 canvases across four games**,
  including six mid-arc capstones in `the_inheritance` and three in `vesper` it is correctly
  catching. The canvas was changed instead, and the change is better game design: the three
  arcade work bands used to gate on `season_shut`, **a flag set upstairs in her flat**, so the
  counter was workable in a building whose shutter was still down. They now gate on `shutter_up`,
  set by the first visit. The funnel is a real chain and the gate went green on its own terms.
- **What the 38 gates still cannot see:** a room with nothing in it (§P1 — the catalogue gate has a
  ceiling and no floor), a schedule row with no surface (§P2), a line that is false on six days in
  seven or that asserts a figure the state holds (§T4/§T5 — `the clock in the prose` scans hours
  only, and says so), a system switched on with nothing in it (§O5), a meter printed twice (§O6 —
  gate 27 checks banded items only), and a locked door that unlocks onto itself (§G2). §D1 and §D2
  **are** now visible — that is what `a day-cap closes` is — and §T2's readings are visible in the
  lint's list, which is what T7 bought.

---

# 15 · Root cause — what the skill did and did not teach

Full detail in Appendix B. In one table:

| # | mechanism | evidence |
|---|---|---|
| 1 | **v1 asked it, v2 dropped it.** `author-game/references/onboarding.md` (269 lines, engine-cited, with a hard rubric) and `npc-intro.md` (146 lines) have **no v2 counterpart**. A grep of the whole v2 skill for `introduc\|first meeting\|on-ramp\|onboard` returns one permissive clause in `the-release.md:70` and nothing else. | `DOCTRINE_GAPS.md:124` — Tier 2 row **6 · Onboarding · the first hour** is the **only** row in the table with an empty status column. |
| 2 | **A shape in `templates/` outranks every rule beside it.** Third recurrence, after `15/35/55/75` and the volatile list. | `templates/board.toml:147` ships `costs = "£5 for the immersion"` — a UK currency symbol and a UK-only noun in six words. |
| 3 | **The scoreboard measures a proxy.** `sentence length` stands in for readability and passes a game nobody can read. | §L3 |
| 4 | **NEW — the skill's worked examples *are* the register.** No line in the skill says "write British". Its examples said it instead. `SKILL.md` already carried *"an example outranks every rule beside it"*; it had only ever been applied to **shapes**, never to **words**. | Counted with word boundaries across the live reference files: **27 locale-locked terms in 11 files** — `airer` ×9, `lodger` ×8, `immersion` ×3, `rota`/`rotas` ×3, `fortnight` ×2, `forecourt` ×1. `templates/board.toml:147` shipped `costs = "£5 for the immersion"`. |

**Scope, stated honestly:** v1's two files would have caught **2 of LO's 6 complaints** — the
untaught clothing system (O4) and the cold-spawn hubs (N1). The dialect (L1, L2), the clock (T1–T3),
the currency (M1, M2) and the compressed opening (O1) are ground **neither skill has ever
covered**. This is a rebuild informed by the field, not a port of v1.

---

# 16 · Not defects — checked, and correct

Recorded so they are not re-investigated:

- **All 86 condition blocks carry `version = "1.0"`.** No fail-open gates (`v2.py:3534`).
- **Neither start location is a container**, so no onboarding canvas is swallowed
  (`template_import.py:3506`).
- **14 quest cards ship, and one is ready at turn one** — the `npc_tam.ease lt N` card fires at 0.
  The player is not handed an empty hub.
- **Rent is armed correctly** via `start_after_flag = "season_shut"`, so turn one is pressure-free
  — exactly v1's §2.3 rule, followed without the file being present.
- **The rent transaction is not authored as a canvas**, correctly leaving it to `[settings.rent]`.
- **`the_arcade`'s location description does render** (`v2.py:9620`); L2 is about what it says, not
  whether it is shown.

---

# Appendix A · The field research

**Corpus.** `~/Documents/Mopoga_Twine_Sandbox_Research_20260724/gamehtml/` — 28 HTML files, 25 of
which parse as Twine stories (college-daze, confined-and-horny and free-cities carry no
`tw-passagedata`). **10.6M words** of passage prose after macro/markup stripping. Same corpus used
by the 2026-08-18 meters study, so the figures are comparable across passes.

**Method note.** Prose extraction strips SugarCube macros, HTML, `$variables` and temp variables,
and keeps link *labels* (they are player-visible words). Readability is computed on sentences of
5–60 words that are not majority-capitalised, which removes menu and title fragments from both
sides of every comparison.

## A.1 · Readability and vocabulary

Flesch Reading Ease, field vs ours — **higher is easier**:

```
                     Flesch   grade   w/sent   syl/word
sluttown-usa          87.8     4.0
degrees-of-lewdity    83.2     4.1
patriarch             78.8     5.5
FIELD MEDIAN          78.0     5.5     12.9      1.36
friends-of-mine       77.0     6.5
zaras-school-life     69.5     7.3
lust-for-life         57.7     8.9      (field floor)
────────────────────────────────────────────────────
seventh_day           88.0     4.6
OFF SEASON            86.8     5.0     15.3      1.24
the_allowance         84.7     5.4
forty_miles           83.5     5.6
back_home             81.3     7.0
vesper (v1)           86.8     4.8
the_inheritance (v1)  87.4     4.0
```

Locale-locked vocabulary, uses per 10,000 words — the table in §L1. Terms with **zero** uses across
the entire corpus: `airer, anorak, bedsit, biro, chandlery, chippy, forecourt, fryers, holdall,
lodger, wellies`. Near-zero: `immersion` (2 games / 2 uses), `rota` (1 / 1), `fortnight` (1 / 3),
`telly` (1 / 2), `mech` (1 / 1), `tenner` (1 / 1), `hob` (1 / 1), `eiderdown` (1 / 1).

Genre-relative rarity (a word in ≤3 of 25 games), per 1,000 words: field median **18.6**, off_season
**24.4** — inside the field's range. **The raw rarity rate is not the signal; what the rare words
*are* is.** The field's are inventions and setting words the fiction defines (`elven`, `orphanage`,
`slaver`, `shillings`, `gunpowder`); ours are real-world regional objects assumed known.

## A.2 · The opening

Openings walked from `startnode` along the navigation spine (including `<<goto>>`, `<<include>>`,
`<<display>>` and `<<link "L" "T">>`) until the first passage with ≥6 outbound targets. Two rows
were discarded as artefacts after inspection — sluttown-usa's and family-business's walks land in a
**changelog**, not an opening.

```
FIELD median opening                          774 words
openings naming NOBODY                       10 of 20
when a name appears: median names                    4
when a name appears: words per named char    ~229  (values 132, 174, 217, 229, 1055, 1558, 1633)
OFF SEASON                                    279 words · 6 named · 0 on screen · 46 w/name
```

The two coherent shapes, read in full:

- **Cold open** — corpo-life, 64 words: *"My name is [X]. I just got accepted into Chase-Bank, one
  of the most prestigious banks in New York city. After graduating from Stanford, I applied into
  the Management Trainee program and rented a small apartment near my office and am living
  frugally in order to live in this concrete jungle."* Who, job, place, why poor, what is at stake.
  Zero characters. Also DoL (193 w), the-company (126 w), destroyer (285 w).
- **Staged open** — patriarch, 2,619 words over 8 passages: 281 words of world rules with no names
  → *"one of your father's favourite girls, Ana"* on screen and speaking → the father, on screen,
  553 words of dialogue → Audrey arrives with a pretext (*"a gift from your father"*), described,
  named, stating her own function in her first line. friends-of-mine is the flattest version:
  *"This is your closest friend, **Felix Morin**; a rather shy young man who you've known almost
  since the day you've moved here… including his older sister, **Chloe**."* — relationship label,
  then name (bolded on first mention), then a one-line read, then a named next task, then the hub.

## A.3 · The first meeting

Per-character meeting state, counted as variables matching `player.met.<name>` / `met<Name>` /
`<name>Met` / `<name>metFlag` / `<name>_intro` / `<name>Recruit`, with `helmet|gourmet|meter|metal|
method|geometr|symmetr|metabol|comet|magnet` excluded:

```
16 of 25 games carry per-character meeting state
median where present: 11 flags · 22 <<if>> reads
field total: 1,200 gate reads

degrees-of-lewdity  113 flags / 436 reads      become-someone  38 / 241
sluttown-usa         47 / 111                  love-and-vice   31 /  73
the-company          21 /  30                  zaras           15 / 151
realm-of-corruption  12 /  15                  lust-for-life   11 /  71
```

Worked shapes: `become-someone` gates **presence** (`<<if $has.metkate is 1 && $kate.loc is
"Beach">>` at five locations); `zaras` gates the meet on `false` and 46 later events on `true`;
`the-company` sets `player.met.sophie` in a passage named `Intro-MeetSophie` whose prose is a
staged handshake with the role named (*"Your new employer stands and leans forward to shake your
hand"*).

Ours — hubs gated on a meeting **with that character**, over total portrait hubs. A meeting counts
only when the flag is set by a **non-repeatable** canvas that binds or requires that same
character:

```
v2:  off_season 0/4 · the_allowance 0/5 · seventh_day 0/6 · forty_miles 0/7 · steam 0/10 · back_home 0/9
v1:  vesper 3/12 · last_call 16/20 · late_shifts 2/19 · the_inheritance 7/10
```

**All six v2 games are at zero; all four v1 games are not.** v1's `npc-intro.md` is doing real work
in the games built under it, and its removal is legible in the output.

## A.4 · Time

```
117,453 link labels across 25 games
  4,335 name a DURATION       (7 min) · (0:30) · (1 hr) · (3 months) — in 7 of 25 games
     19 name a clock time     in 4 games — all of them "Req: After 5pm" or "Wait until 21:00"
      0 promise a clock time as an action's OUTCOME
```

Prose clock references per 10,000 words and the relative:absolute ratio — the table in §T3. Field
median **1.3** refs/10k and **5.6 : 1** relative-to-absolute. (`family-ties` is a 3,733-word outlier
at 37.5 and is excluded from the median as small-n.)

## A.5 · Currency

```
FIELD symbols:  $ 1,417  ·  £ 459 (degrees-of-lewdity, new-life-project, the-hellfire-club)  ·  € 0
FIELD currency CODES (GBP/USD/EUR) on labels or in prose: 0     ← WRONG, corrected 2026-08-22
label form: always flush against the digits — $100 · £25 · $2500 · $1,000,000
```

> ⚠️ **Correction, 2026-08-22.** The code count above is wrong. **`corpo-life` uses `USD` 109
> times**, including on a link label — `Buy a set of Bespoke suite (USD 15,000)` — and uses it
> *consistently*: 94% of its money references. Re-measured on the same corpus, the field's priced
> link labels break down **symbol 94.0% · spelled-out unit 5.2% · currency code 0.8%** (654
> labels), and a game's dominant notation carries a **median 92%** of its money references
> (minimum 56%). So the rule the doctrine took from this is **one** notation, not a particular
> one — M1's framing of *"a currency code the field never uses"* is not what makes off_season
> wrong. What makes it wrong is using a code, a spelled-out unit and the engine's `$` at once.

Ours: off_season `GBP` ×4 and no symbol; the_allowance / seventh_day / forty_miles `£`; steam spells
`dollars` ×106; the_inheritance `$`. Rent enabled in 8 of 10 games, `currency_symbol` declared in 2.

---

# Appendix B · What the skill taught, line by line

| the defect | the line that taught it |
|---|---|
| L1 · the dialect | `templates/board.toml:147` `costs = "£5 for the immersion"` · `references/the-surfaces.md:17, :106, :423, :446, :447` (the airer, 5×) · `references/the-economy.md:73` (the forecourt) · `references/state.md:68` and `the-board.md:327` (the immersion, again) · skill-wide, word-boundary counted: **27 terms across 11 live files** (`airer` ×9, `lodger` ×8, `immersion` ×3, `rota`/`rotas` ×3) |
| L2 · the unnamed anchor | nothing. `the-map.md` and `the-board.md` never require a location's *function* to be stated in the prose that first names it. |
| L3 · the blind instrument | `SKILL.md:129` registers `sentence length` as the register gate; no vocabulary or referent-load instrument exists |
| O1, O3, O4 · the opening | nothing. The v2 skill's only mention of an opening is `the-release.md:70-71` — *"an opening funnel legitimately runs one-shot to one-shot"* — a rule about milestone chains, not about what an opening must teach. `DOCTRINE_GAPS.md:124` records the gap and has never been closed. |
| N1 · the cold-spawn hubs | nothing in v2. v1 forbids it explicitly at `author-game/references/npc-intro.md:104-113`, with a 7-step template and a hard rubric at `:112-131`. |
| T1–T3 · the clock | nothing. A grep of the v2 references for `clock\|o'clock\|name a time\|absolute time\|time of day` returns only engine mechanics. `the-voice.md:98` ships the correct *example* (`Buy coffee (0:02 £2)`) with no rule behind it. |
| M1, M2 · the currency | `templates/board.toml:147`, `state.md:68`, `the-board.md:327` all ship `£`. Nothing anywhere requires `[settings.rent].currency_symbol` to be declared, and `v2.py:1190` silently defaults to `$`. |

Neither skill has ever carried a comprehension rule. A grep of both for
`gloss\|jargon\|dialect\|regional\|unfamiliar\|first use\|comprehen` returns nothing on point.

---

## Log

- **2026-08-23 — REPAIR BATCH 9 · "the act loops". H1–H3.** **1 open, 41 fixed.** Scoreboard
  **37/38 held**; `location fill` 14,472 → **14,681** and still the only red gate. Batch 8 closed
  saying it had bought variety, not heat, and that the next batch should push the other way. This is
  that batch.

  `explicit floor` read a comfortable pass at 9.6%. Underneath it, **10 of the game's 21 act and
  finish beats carried fewer than 3 body words** — nine of them in the four **character** loops,
  while the two **solo** loops ran 5–7. `loop_ewan_caravan.finish` scored **zero on 127 words**:
  three paragraphs of a man coming, none of which named a body, and a last beat about the desk.
  `the_want.md` §6 had already declared those four loops the crudest writing in the game.

  ```
                          before          after
  act/finish under 3      10 of 21        0 of 21    on the thinnest band each renders
  explicit floor          9.6% BARE PASS  15.3%      17 -> 27 explicit beats
  explicit in repeatable  88.2%           92.6%
  an explicit beat clip   88%             93%        field 91%
  somebody speaks         4.2:1           4.3:1      rewritten IN PLACE, so it barely moved
  own_words               67              67
  ```

  **Why nobody caught it:** a game-wide percentage averages the act away, which is exactly how the
  measured failure hid — 95% of one game's crude prose sealed in one room, nine loops at zero, and a
  passing scoreboard. `lint · the act nodes` reads the screen the player is on. It discriminates:
  vesper reads median 1 with 17 of 25 act beats under 3.

  **⚠️ PLAY found the lint's own defect.** The first version read `Beat.explicit`, which folds a
  node's `[group]` bands together by design — and the live probe promptly failed on nine finisher
  **bands** the lint had just passed. `loop_nessa_curtain.finish` scored 6 folded and put **two**
  body words on screen whichever band fired. A finisher is banded by definition, so the lint now
  reports the thinnest band a node can render, and nine bands were rewritten on top of the ten beats.

  **And the lint returning empty for one game exposed the largest instrument correction yet.**
  `_collect` read a `[group]`'s children only at the block's own `blocks` key; the importer accepts
  them there **or** in `props.blocks` and normalises to the latter. **158 groups across four games
  were invisible to every beat-based gate** — `the_long_summer_test` was being scored on 4,979 of its
  9,429 words. Off Season is unaffected and byte-identical; see §13 H3.

  **289 live checks green** across eight play-tests (16/13/26/23/35/105/36 + **35 new**), no JS
  errors. The new probe reads what is on the page at every act node and at every finisher band, and
  checks each person's `opens later` vocabulary never renders — with the choice labels stripped,
  because those words are also the text of the 0.2 doors and a locked door is a signpost, not
  content. **One probe bug fixed in the probe:** batch 8's dispatcher test compared two predictions
  0.056 apart at n=400, which the sample straddled about one run in five; n is now 1,500.

  **The rewrite was in place, not additive** — the beats were already the right length, they were
  hedged. That is why 19 rewritten beats moved `somebody speaks` by 0.1 and the vocabulary list by
  nothing.

- **2026-08-23 — REPAIR BATCH 8 · "the walk-in". V1–V4 — found by the batch, not in LO's read.**
  **1 open, 38 fixed.** Scoreboard **37/38 held**; `location fill` moves 12,118 → **14,472** of
  33,300 and stays the only red gate — but its *structural* complaint is gone: **the anchor is the
  centre of the world for the first time since the game shipped.**

  `the-surfaces.md` R3 — *"one activity DEEPENS, the room does not widen"*, whose worked example is
  DoL's `Bath`, **one activity with twelve outcomes**. Off Season had five dispatching activities and
  **not one of them could produce a second outcome**: the roll only ever decided whether the branch
  or the host rendered.

  ```
  before   5 hosts,  7 rules,  outcomes per host [1, 1, 1, 1, 1]
  after    7 hosts, 29 rules,  outcomes per host [3, 5, 5, 4, 3, 4, 3]   deepest in the repo
  ```

  Thirteen new branches, all `substitution_only`, all location-bound, all day-capped. Six of the
  seven hosts converted to **Pattern B** (`exclusive_group`), which is the difference between the
  odds you wrote and the odds that run: five branches at 0.12 leave the activity on screen 53% under
  Pattern A and 40% under Pattern B. The flat keeps Pattern A on purpose — groups are processed
  first, so a group there would quietly cut how often Tam comes up the stairs.

  **The anchor.** `the_arcade` **1,957 → 3,640**, and the gate line *"no anchor as built — the world
  has no centre"* is gone. One new canvas, and only one: `work_arcade_evening`, because the last two
  hours the building is open had no work surface on any day (R1's who × when). The after-close
  cascade became `loop_arcade_floor`, a node-routed act loop — `an explicit beat carries a clip`
  moves **78% → 88%** and the act-menu lint drops a one-shot cascade.

  **Why nobody caught it:** `the walk-in floor` is an existence gate and says so in its own comment.
  Fourth instance of this shape — clock lint, currency lint, ladder lint, and now a gate that tests
  for one of a thing whose whole point is many. `lint · dispatch depth` now prints it, and it needed
  **two corrections before it shipped** (it multiplied chances that cannot co-occur; then it picked
  a co-live set by size, which made the answer depend on declaration order). It immediately found a
  latent defect in this game's own `solo_flat_warm` bands — see §12 V3.

  **254 live checks green** across seven play-tests (16/13/26/23/35/105 + **36 new**), no JS errors.
  The new probe drives `checkAndSubstituteCanvas` 400 times per host and reads the distribution:
  every ungated bucket reachable, the observed rate tracking **Σ p** and not 1 − ∏(1 − p), and a shut
  bucket handing its share back to the host rather than to the next bucket. **Two probe bugs, fixed
  in the probe:** the day cap made 400 rolls produce five hits, and presence gets in two ways —
  `npc_at_location` on the rule *and* `requires_npc` on the target.

  **Four words caught by batch 6's own instrument before the batch closed** — `mech` (which
  un-taught the gloss batch 6 wrote for *coin mechanism*), `rota` (a word batch 6 removed from this
  game), `takeaway` and `Whitsun`. The list ends at **67**, two above batch 7, both plain English.

  **`somebody speaks` 3.9:1 → 4.2:1** against a 5.0 ceiling, and `explicit floor` 11.2% → 9.6%: 17
  new beats of texture with no bodies in them. Both still pass; both are the cost of a batch that
  buys variety rather than heat, and the next batch should push the other way.

- **2026-08-23 — REPAIR BATCH 7 · "the bottom of the ladder". W1 and W2 — found by the batch, not
  in LO's read.** **1 open, 35 fixed.** Scoreboard **37/38 held**; `location fill` moves 10,571 →
  **12,118** of 33,300 and stays the only red gate.

  REVIEW_1 was exhausted, so this batch measured the repaired game against the deepest content rule
  the skill has — `the-meters.md` **W4**, *"a meter that carries a game has eight or more rungs, and
  the lowest one sits around 5"*. Six cast meters, **every lowest rung at 12–22**, one of them with
  a single rung. Against grants of 2–7 that is four to eight clicks with a person before anything
  about them changes, which is W4's own sentence describing this game.

  ```
  before                                        after
  npc_tam.ease       1 rung   [20]              4 rungs  [4, 8, 12, 20]
  npc_nessa.trust    2 rungs  [20, 40]          5 rungs  [5, 10, 20, 30, 40]
  npc_nessa.want     2 rungs  [18, 30]          5 rungs  [5, 12, 18, 24, 30]
  npc_ewan.hold      3 rungs  [18, 25, 40]      6 rungs  [5, 10, 18, 25, 32, 40]
  npc_roan.bond      3 rungs  [12, 25, 38]      7 rungs  [4, 8, 12, 18, 25, 32, 38]
  npc_tam.want       3 rungs  [22, 45, 90]      5 rungs  [22, 30, 38, 45, 90]
  ```

  **Why nobody caught it: the lint implemented one side of a declared fork.** `lint_meter_ladder`
  read `board.ascent_tiers` and returned early when it was empty, and off_season is the only roster
  game in the repo (`who_climbs = "cast"`, `ascent_tiers = []`). It was the only game the ladder
  lint printed nothing for. Third time this shape has appeared — the clock lint (§T7), the currency
  lint (batch 6), and now this: **the doctrine was right and the check covered part of it.**

  **18 new rungs in two shapes, both keeping one interaction per person per day.** Four banded talk
  screens sharing the existing `<npc>_talk_today` cap, and six banded hub openers that cost no
  choices at all. `somebody speaks` **improves for the first time in seven batches — 4.8:1 → 3.9:1**
  against a 5.0 ceiling, which is the test of whether the new screens really are talk screens.
  Talk-screen share **6% → 10%** (vesper 26%, field 29%).

  **Three words were caught by batch 6's own instrument and rewritten before the batch closed** —
  `bilge`, `takings` and `tally`, real objects that look defined and are not. `clunk` and
  `subtitles` stayed: one is its own definition, the other is a television. The list ends at 65,
  two above where batch 6 left it, with **no new locale-locked term**.

  **218 live checks green** across six play-tests (16/13/26/23/35 + **105 new**), no JS errors. The
  new probe proves what a rung count cannot: at every band boundary the screen swaps, and **exactly
  one band renders** — 82 assertions on that alone. **No gate moved on any of the other eleven
  games**, and the extended lint prints byte-identical output for the five ladder games.

  **Left open on purpose:** `npc_tam.want` keeps its bottom at 22 and the lint still says so. `want`
  is pinned at 0 until `tam_saw_you`; Tam's low feedback lives on `ease`, which now starts at 4.

- **2026-08-22 — REPAIR BATCH 6 · "the words the player has to already own". L1, L3, M3 and G3
  closed.** **6 open → 1 open, 33 fixed.** Scoreboard **37/38 held**, and `location fill` is now the
  only red gate in the game.

  This was **LO's first complaint and the last one still open** — *"the language being used here is
  tough to get… why couldnt we use simpler language"*. §L2 answered *"what is arcade"* in batch 3;
  this is the rest.

  **A word-by-word judgement, not a purge**, because the lint's own docstring forbids chasing the
  number: *"the rate does not discriminate… what separates them is what the words ARE."* The list
  went **94 words / 203 uses → 63 / 121**:
  ```
  false friends   vest -> T-shirt · jumper -> sweater      they do not LOOK like jargon
  swapped         settee telly mam hoover eiderdown hob fortnight snooker rota lodger
  glossed         immersion heater · extractor fan · chandlery ("the shop that sells boat
                  parts") · coin mechanism — taught once on first use, then earned
  ambiguous       half three -> half past three                        3 -> 0
  ```
  **Player-visible hits remaining: zero**, checked with the lint's own `_player_visible_text` rather
  than a grep of the file — the media `description` fields still say *settee* and *jumper*, and
  should: they are find-media search hints, not prose.

  **`tea` stays on the list and it is a false positive.** Eleven of its twelve uses are the drink
  (*"two teas in the two mugs he owns"*, *"a tea towel"*); only *"they all go home for their tea"*
  was the meal, and that one moved. The lint warns to expect exactly this.

  **The 63 words left are named so nobody "fixes" them later:** number words the corpus never
  spells, proper nouns the fiction teaches, coinages, plain English the 25 games happen not to use
  (`arithmetic`, `diesel`, `barometer`, `kettle`), and the glossed terms at their post-gloss repeats.

  ⚠️ **The triage found a currency regression, and I wrote most of it.** Batch 2 declared a neutral
  `$` and stripped `pounds`/`quid`/`euros`; batches 4 and 5 put British *coin* units back — `fifties`
  ×6, *"sixty pence"*, *"the two-pence one"*, *"to the penny"*, three of them in canvases written for
  this repair. Six fifties for a $3 charge is arithmetic nonsense. **And the lint said "no beat names
  a currency" the whole time**, because `_CUR_UNIT` knew `pound`, `dollar` and `euro` but **no
  sub-units**. Both halves fixed: the words are gone, and the lint learned `pence`/`penny`/`cent`
  with a `per cent` guard — measured first, because without it `steam`'s *"the trade is down forty
  per cent"* false-positives. Run red before green: the lint caught the regression, then went clean.

  **`The Lodger's Room` is finally `The Back Room`.** `the-voice.md:43` has recorded this as
  off_season's own defect since 2026-08-22 — *"`lodger` is used by ZERO of the 25 field games… the
  cure was written in the same dialect the rule exists to catch"* — and the board file was **still
  carrying the retracted rule as an authoring comment**. Both fixed, and Nessa's `arc_stages[0]` went
  *The lodger* → *Your tenant* with them.

  **G3** — the hub is the decision and the rung is the outcome now, instead of both narrating the
  same beat two clicks apart. Gate 26 forced those splits and nothing told the author the screens
  then differ; `work_arcade_morning` → `rung_arcade_take_am` had always done it right.

  **Verified.** 37/38, no gate moved on any of the twelve games, `sentence length` still 10 and
  `somebody speaks` still 4.8:1. All five play-tests re-run: 16/16, 13/13, 26/26, 23/23, 35/35 — one
  probe was updated rather than the game, because two swapped words sat on choice labels.

- **2026-08-22 — REPAIR BATCH 5 · "the act loops". G1 closed; `promises[0]` paid.**
  **7 open → 6 open, 29 fixed.** Scoreboard **37/38 held**. This batch is scored by the lints, not
  the gates: **`the act menu` 2 loops / 6 cascades → 5 loops / 3 cascades**, and
  `ends on an opening` **1 visible-locked choice → 4**, one 0.2 door per character.

  `the_want.md` §6 says where the crude register lives — *"the act loops on the four hubs"* — and
  **one of the four existed.** Ewan, Roan and Nessa each had a five-beat cascade instead: a scene
  that replays identically on a surface the player is meant to live in. `the-surfaces.md` R3b:
  *"a repeatable explicit surface is a node-routed loop; a one-time scene is a cascade."*

  All three are now pose ladders with R3b's six parts — an act node per rung with its own pool, a
  self-loop, switch links **both ways**, an arousal-gated finish, a finisher electing on
  `loop_stage`, and a reset on entry and on both exits. **The cascade prose was the raw material,
  not scrap**: the beats already were the rungs.

  **The game reached its declared ceiling for the first time.** `the_want.md` §6 puts `fuck` in the
  **0.1** column for Tam and Roan and `cunt` in Ewan's **later** column — and the build had no
  penetration anywhere, which is CLAUDE.md's *"writing under the ceiling is the defect"*. Read as
  what the acts reach, the table answers every design question in the batch:
  ```
  Tam    0.1 has cunt + fuck   -> tops at penetration      0.2 door: arse
  Ewan   `cunt` is LATER       -> the ladder is what she does to HIM     0.2 door: his hand on her cunt
  Roan   0.1 has cunt + fuck   -> penetration, not inside  0.2 door: come inside
  Nessa  `fuck` is LATER       -> fingers and tongue       0.2 door: let her fuck you
  ```
  **`promises[0]` is paid rather than deferred again.** Tam's two locked doors *were* penetration,
  which his 0.1 column permits. Batch 1 capped his `want` at 60 to hold them shut and wrote into the
  ledger: *"0.2 MUST RAISE THE CAP IN THE SAME CHANGE that builds the content behind those doors."*
  This was that change — cap 60 → 85, both doors route into a real `astride` act node, and a stage-3
  finish band came with it.

  **Two hand audits no gate performs, both clean:**
  ```
  CEILING   every crude term in all four loops vs that character's own 0.1 column -> 0 breaches
  PIVOT     the last sentence of all 25 explicit beats -> 25 on the body, 0 pivots
  ```
  The ceiling audit also found the **doors** were inconsistent — Tam's named its act plainly while
  the other three hedged (*"what is in the bottom of your wardrobe"*). A locked door is a signpost,
  not content, and `the-voice.md` R4 wants the greyed row to state the want. All four now name it.

  **Verified live — 35 checks, zero JS errors.** For each loop: entry resets the state, the self-loop
  raises arousal, switch links move `loop_stage` **both** directions, the top act sets stage 3, and
  **both** the finisher and the stop node wipe `arousal` and `loop_stage` — R3b's *"forget either and
  the next run starts mid-climb"*. All four 0.2 doors render visible and stay locked with the meter
  forced to 100.

  ⚠️ **`somebody speaks` hit exactly 5.0:1 against a 5.0 ceiling mid-batch.** The act nodes had gone
  voiceless, which `register.md` S3 forbids outright. Eight of them were given a line each and it
  settled at 4.8:1. Worth keeping: a batch of pure explicit prose is precisely the one that pushes
  that ratio, and the ceiling is what caught it.

  **One probe was updated rather than the game.** Batch 1's play-test asserted *"want 58 + 5 clamps
  to 60"* and a locked *"Get on top of him"*. Both were true only because of a cap that existed to
  hold a promise this batch paid. The probe now asserts the new cap (85) and the new door (`arse` at
  want ≥ 90). Batches 2–4 re-run untouched: 13/13, 26/26, 23/23.

- **2026-08-22 — REPAIR BATCH 4 · "the people who are already there".** P1, P2, P4 and O7 closed.
  **10 open → 7 open, 28 fixed.** Scoreboard **37/38 held** while the game grew by 1,457 words and
  18 canvases — no gate moved, which is the batch behaving as scoped.

  One rule applied: **every `[[npcs.schedules]]` row that puts somebody in a room gets a surface, or
  the row is a lie the nav card tells.** It *was* telling it — `getNpcsPresentAtLocation`
  (`v2.py:19350`) advertises a portrait badge for every scheduled NPC whether or not anything there
  is clickable, so the player saw Ewan's face on the Harbour End card, paid the 15-minute walk, and
  arrived at a coin-flip ambient.

  **Six new portrait hubs and twelve rungs**, one per unserved row. Nothing invented:
  `board.locations[].serves` had already named the person for five of the six.
  ```
  hub_roan_front      the promenade, 09:00-11:00   the ROOT location's first clickable content
  hub_ewan_slip       the slip, 07:00-08:00        + the diesel sink, built at last (O7)
  hub_tam_row         terrace row, 07:00-08:00     the interactive half of amb_terrace_nights
  hub_nessa_booth     the arcade, Fri/Sat 12-17    the ANCHOR's first person surface
  hub_ewan_counter    the arcade, Mon 19:00-20:30  the ANCHOR's second — and no money moves
  hub_nessa_asleep    the back room, 22:00-08:00   the gap batch 2 opened and recorded
  ```

  **The declared anchor became the real one.** `location fill` had been naming
  `the_chip_shop_flat` as the anchor-as-built against a ledger declaring `the_arcade`. With both of
  the arcade's people finally given surfaces it now reads **`anchor the_arcade 18%`**.

  **`hub_ewan_counter` is the one that could have created an economy bug**, and it does not.
  `the-economy.md` R3's measured failure is a second settle-up beside a working `[settings.rent]` —
  free, repeatable, and the one with the writing in it. Verified rather than assumed that the
  evening is *beside* the money: `is_due` is set at **midnight** (`v2.py:5464`) and the RentDay page
  intercepts on the next `Location_` passage (`v2.py:15258`), so the ninety changes hands on Monday
  **morning**. The hub carries no cost and no money effect and narrates no hand-over — confirmed
  live, 22 → 22.

  **P4 · the first use of `show_when_blocked` anywhere in this repo.** All five windowed solo
  activities publish their hours instead of vanishing. Live: at 14:00 the arcade shows the morning
  band dimmed — *"Open up and work the counter — mornings, eight till one"* — beside the live
  afternoon one, and at 03:00 all three publish. A room whose content disappears reads as a broken
  game; a room that says when to come back is a timetable.

  **Verified live — 23 checks, zero JS errors**, plus batches 1–3 re-run (15/15, 13/13, 26/26).
  Every one of the six hubs renders in its window and is gone outside it; the three formerly dead
  rooms return content; the diesel charges $12 and burns the day's Ewan rung.

  ⚠️ **Batch 2's gate caught batch 4 on the way in.** `the label keeps its time` failed a new hub
  choice reading *"Don't turn the machines off at nine."* — a clock time on a label, which is
  precisely what C3 forbids and precisely what that gate was built for two batches earlier. Three
  words deleted. **Second time a gate from an earlier batch has caught a defect in a later one**,
  after batch 3's `milestones open something`.

  **Two calls recorded rather than buried.** The `_rung_today` day-cap flags are shared per
  *character*, not per surface, so going to Ewan at the slip at seven spends the same day as going
  to the yard at noon — one interaction with a person per day across all their places, which is the
  pacing rather than an oversight. And `traversal heat` stays at **7/10**: no cycling explicit pool
  was forced onto a promenade at ten in the morning, and 70% clears the 60% floor honestly.

- **2026-08-22 — REPAIR BATCH 3 · "the first hour". The first batch that writes prose.**
  L2, O1–O4, N1 and N2 closed. **17 open → 10 open, 24 fixed.** Scoreboard **34/38 → 37/38**, and
  `location fill` is now the only failure left in the game.

  Aimed at the ten minutes LO actually played — *"No NPC introductions… I think we still havent
  learnt how the game should be started."* **A redistribution, not an addition: +565 words net.**

  **The opening picked a shape and committed** (F1). `canvas_opening` is a cold open now: two nodes,
  **159 words, zero characters named**, carrying her situation and the pressure and nothing else. The
  cast was not cut — it moved to where a person can be met. The reversal (*the pitch does not go to a
  landlord*) is now said by **Ewan, in his own yard**, instead of asserted at a player who has met
  nobody.

  **`canvas_first_arcade` does three jobs in 189 words.** It says what the place is —
  *"This is an amusement arcade. Slot machines down both walls. Four coin pushers in the middle…"* —
  which the game had never once said anywhere (§L2, and LO's *"what is arcade??"*). It catches the
  building and the ninety that came out of the opening. And it closes the dead half-hour by being
  what is live in it:
  ```
  07:00 start · 07:03 node->node · 07:33 the arcade, first visit fires · 08:03 the counter is open
  ```
  The introduction does the waiting, which is what a first hour is for.

  **Four meetings, four flags** (F5–F8). 119–135 words each, one node, four `dialog` blocks, built to
  `the_inheritance/canvas_meet_audrey`. Node name is the **role**, hub name is the **name** — *Your
  eldest* → *Ewan*. Each carries its character's schedule window, because `requires_npc` does **not**
  gate the auto-fire path (`v2.py:4573`), and the same windows went onto the four existing milestone
  one-shots, which could previously narrate a character into a room they had left. `named before met`
  goes **3 people → 0**.

  **Verified live — 26 checks, zero JS errors**, plus batch 1's 15 and batch 2's 13 re-run and still
  green:
  ```
  the opening names nobody · the handover lands in the arcade and it introduces itself
  out of the introduction at 08:03 with the counter offered · shutter_up set
  each meeting: NOTHING out of window, fires in window, sets its flag, hub portrait then renders
  canvas_first_borrow does NOT fire at 22:00 with Ewan gone, and does at 10:00 with him there
  ```

  **The batch tripped a gate on its way in, and the gate was right.**
  `milestones open something` failed `canvas_first_arcade` the moment it existed — a one-shot that
  sets no flag opens nothing and owes an explanation. The tempting fix was to widen the gate to
  excuse "first visits". **Measured first, and rejected:** a blanket *sets-nothing* exemption would
  have excused **10 canvases across four games**, including six mid-arc capstones in
  `the_inheritance` and three in `vesper` that it is correctly catching. A narrower
  "exempt whatever `the opening opens a door` counted as the door" variant was also measured and
  would still have wrongly excused `the_inheritance/marg_move_staff`.

  **So the canvas changed instead, and the change is better game design.** The three arcade work
  bands gated on `season_shut` — **a flag set upstairs in her flat** — so the counter was workable in
  a building whose shutter was still down. They now gate on `shutter_up`, set by the first visit.
  The funnel became a real chain (flat → arcade → the counter opens) and the gate went green on its
  own terms rather than by exemption. `work_lets_turnaround` keeps `season_shut`: the holiday lets
  are not behind that shutter, and the *season* being shut is what makes turnarounds her winter work.

  **No skill change was needed.** `the-first-hour.md` F1–F9 taught every shape this batch built, and
  building it turned up nothing wrong in the doctrine — the first pass where that has been true.

  **Two things left where they are, on purpose.** O4 is closed by *evidence* rather than work — the
  system it named is off, so there is no live untaught system — and it re-opens the day a wardrobe
  surface is authored. And four locations still carry no first visit (harbour_end, terrace_row,
  the_front, the_lets); they are corridors and a workroom, and they belong to the rooms batch with
  §P1/§P2.

- **2026-08-22 — REPAIR BATCH 2 · "what the screen says".** Every place the game told the player
  something untrue: the money, the clock, and the instrument that should have caught the clock.
  **M1, M2, T1–T7 and G5 closed; M3 left open on purpose. 27 open → 17 open, 17 fixed.**
  Scoreboard **32/38 → 34/38** — `the price is in one currency` and `the label keeps its time` both
  flip, and nothing else moves.

  **The currency, declared once.** `[settings.rent] currency_symbol = "$"` (it had none, so the
  engine fell back to its default and the rent card printed a currency the game never declared),
  matching `board.economy.symbol`. Six priced labels and two canvas names take `$`; fifteen prose
  lines lose the unit name and keep the number — the style the rent text already used, *"Right.
  Ninety."* A **third** currency went with it: `amb_lets_drawer`'s *"two euros"* → *"two coins from
  somewhere else"*, which keeps the beat it was there for.
  ```
  the price is spelled out    symbol 0% -> 100%,  code 75% -> 0%,  word 25% -> 0%   (field 94/0.8/5)
  the currency in the prose   "no beat names a currency"; both mismatch warnings gone
  ```

  **The clock.** Two labels stop promising an hour the engine has no primitive for. **Fourteen
  readings turned into rules** — nine listed here, four the lint could not see until T7 corrected
  it, one more found grepping the build. Every turn is grammatical and the fact survives:
  *"Shutter up at eight"* → *"The shutter goes up at eight"*. Fourteen references remain in the game
  and **every one of them is a rota or a rule**; no reading is left.

  **T7 is the finding worth keeping.** The lint had four blind spots, not three, and correcting them
  moves the **field** from median 1.0 to 1.1 — one game, one true positive — while moving **ours by
  a quarter to a half** (off_season 20.1 → 26.4, steam 29.2 → 36.6, forty_miles 22.6 → 34.4). **The
  blind spots were hiding our defects and almost none of the field's**, because the shapes they
  missed are ones our authors reach for and the corpus does not. On its first run it found four
  readings nobody had listed, two of them the opening line of a milestone one-shot. Dropping the
  allow-list altogether was tested and rejected — it inflates the *field* to 1.2 / 2.6, which is
  noise being scored.

  **Verified live** (13 checks, zero JS errors, on top of batch 1's 15 re-run and still green):
  ```
  the rent card prints $90, and so does the can't-pay card
  Feed the meter ($3)  ·  Put it in the slot ($3, 5m)  ·  Work the counter (2h 30m).
  Ewan on a MONDAY no longer says it is not Monday
  Nessa's hub renders at 13:00 and does NOT at 02:00
  ```

  **Three things deliberately not done.**
  **(1) M3 stays open** — the `GBP` is gone from that label but the item is about *meter* and
  *immersion*, two locale-locked referents. That is §L1's class and it belongs to the language batch.
  **(2) T6 makes the game smaller before the rooms batch makes it bigger** — Nessa drops from a
  13-hour window to 3, and her night presence now has no surface at all. That is R1 saying a canvas
  is *missing*; the night hub is the first thing the rooms batch should write.
  **(3) `RentDay_Short` hardcodes `$`** (`v2.py:16000`) and never reads the setting. It agrees with
  us by luck. Invisible while the decision is `$`, and the one place it would break if it were not.

  **And one correction to the skill's own published numbers**, because a measurement that flatters is
  as bad as one that hides: `FIELD_MEDIAN` / `FIELD_P75` for the clock lint move 1.0 / 2.0 →
  **1.1 / 2.1**, and `the-clock.md`'s field table was re-measured with the *shipped* function rather
  than a copy of it.

- **2026-08-22 — REPAIR BATCH 1 · "the wiring". First fixes ever made to this game.** Nine
  sub-items: D1, D2, D3, D4, O5, G2, G4 closed; O6 and O7 partly. **36 open → 27 open, 7 fixed, 2
  partial.** Scoreboard **31/37 → 32/38** — one gate added and passed, and *no other gate moved*,
  which is the batch behaving exactly as scoped.

  Batch 1 was every defect where a mechanism was broken and the repair needed no new prose. Two
  button labels are the only player-visible words that changed.

  **The engine fact the batch turns on**, read rather than assumed — a choice and a node exit emit
  in opposite orders:
  ```
  choice     flagEffects -> costs -> … -> advanceTime      v2.py:12648-12733
  node exit  advanceTime -> traitEffects -> flagEffects    v2.py:13085-13088 · :13049-13050
  ```
  `advanceTime` rolls the day inside itself (`v2.py:5411-5414`) and that is where
  `[engine.daily_tick]` clears every `_today` flag (`v2.py:5552`). So all 14 rung day-caps moved
  from the rung's exit onto the hub choice: **exit-set 15 → 0, choice-set 0 → 18** (14 rungs plus
  D1's four talks). `act_flat_sleep` lost `slept_today` altogether — it is a LOCATED canvas, so
  `max_triggers_per_day = 1` is a real cap and `markCanvasTriggered` stamps the day key *before*
  `advanceTime` (`v2.py:4290`).

  **Verified live, not by inspection.** Fifteen checks in a headless build of the repaired game,
  all passing, zero JS errors:
  ```
  sleep 21:00 Monday -> 06:00 Tuesday, and Sleep is OFFERED AGAIN at 21:00 Tuesday   <- D2
  talk screen offered once, tam_talk_today set, gone on the second click same day    <- D1
  entering Tam's loop and bailing via "Stop." still burns the day's rung             <- D2
  want 58 + 5 clamps to 60; "Get on top of him" still renders greyed at 60           <- G2
  sidebar reads CHANGE BAG: 22 / 90; no Change Clothes link in the flat              <- O6, O5
  ```

  **The skill half shipped with it**, because M5's worked example is where D2 came from —
  `the-meters.md` M5 now sets the flag on the choice, `engine.md` §28 is rewritten (its old warning
  at `:989` said the cap gets *cleared*, which the emit order makes impossible), and gate
  **`a day-cap closes`** is new. Predicted before it was written and reproduced exactly: off_season
  FAIL (4 flags), seven games PASS, three n/a. The measurement that settles the placement:
  **78 day caps in this repo already sit on the choice against 40 on an exit, and 35 of those 40
  belong to `off_season` and `the_allowance` — the two games written under that example.**

  **Two things were deliberately NOT done, and both are on the record rather than quietly dropped:**
  **(1)** `hidden = true` on `money` would end the sidebar doubling and was **built and read both
  ways** — it also empties the "Traits" box *and* the "You (Marnie)" half of the Stats page, because
  `hidden` drives both surfaces (`v2.py:1220-1226`) and money is this game's only unhidden player
  trait. A redundant row beats two empty boxes; the real fix is an engine change and is LO's call
  (§O6). **(2)** `the_allowance` carries D2 twenty times over and was not touched, per LO's standing
  instruction on the other games.

  **A near-miss worth keeping:** `lease_called` reads as a broken flag chain — four readers, no
  canvas setter — and is not one. The engine sets it when the payment is missed past grace
  (`v2.py:16006`) and registers itself as the setter (`v2.py:11504-11512`). It is in §16 so nobody
  chases it, and the new gate is scoped to `is_false` reads so it cannot false-positive on it.

- **2026-08-22 — sections 6-10 opened: the game read against the corrected skill.** With all five
  doctrine passes landed, the whole game was read once more — board, five TOML phases, the built
  HTML, and the generator wherever a claim needed proof. **21 new sub-items, count 15 -> 36.** None
  of them came from playing; they came from crossing the build against the doctrine that now exists.
  The scoreboard moved 31/32 -> **31/37** on an unchanged game, because the instrument grew (§14).

  The five that matter most:
  ```
  D1  four *_talk_today day-caps are READ and CLEARED and never SET — the four talk
      screens are uncapped meter faucets, and the gate fails open so nothing catches it
  D2  advanceTime() runs BEFORE flagEffects on every exit (v2.py:13085-13088), so a
      midnight-crossing rung sets its _today flag on the NEW day — the player can never
      go to bed before midnight after night one
  P1  three locations carry no clickable content at all; three more carry only a
      portrait that is live part of the day. The catalogue gate has a ceiling, no floor
  P2  five declared serves.people entries have no surface — including BOTH people at
      the 9,000-word anchor — while the nav card still shows their faces
  G1  the_want.md promises act loops on four hubs. One shipped; three characters got a
      cascade that replays identical prose every day
  ```

  Three findings are **skill or instrument faults the game exposed**, and they are the half to fix
  in `.claude/skills/author-game-v2/` rather than here:
  **(1)** `engine.md:989` states the midnight day-cap hazard **backwards** — it warns the cap gets
  cleared, when the emit order means the flag is set on the far side of the tick and locks the next
  day out (§D2);
  **(2)** `the-clock.md` C2 is written about the **hour** only, and the same reading-versus-rule
  test applies to the **day of the week** and to any figure the state already holds — `"It is
  Thursday"` beside a hardcoded take, in a canvas that runs all seven days (§T5);
  **(3)** the `clock_in_prose` lint has three blind spots — an hour followed by `"the"`, `half
  <hour>`, and an hour at a sentence start — and one of the four lines it misses is the entry
  sentence of `loop_tam_bed`, the surface the want names as the most re-entered in the game (§T7).

  One new gate is proposed and is fully mechanical: **a flag read `is_false` and unset in
  `[engine.daily_tick]` must have at least one `op = "set"` site** (§D4). D1 is silent, green in the
  build, green on the scoreboard, and deletes a throttle the whole climb was costed against.

  **LO's correction, recorded:** the `location fill` shortfall is **not a defect** — it is planned
  content, the game is being built thin-to-thick, and the 33,300 budget was declared before the
  prose (verified: the gate's post-hoc-budget branch does not fire on this game). What §P3 adds is
  where the 25,337 words actually sit: 67% of them are in the seven surfaces §P1 and §P2 name, and
  `board.locations[].serves` already says what goes in each one.

  Nothing in the game was changed. Six earlier items were checked and stand unaltered.

- **2026-08-22 — item 5 (§5, the money), the SKILL half done; the game half still open.** The
  doctrine landed as `references/the-economy.md` **R7** ("One currency, declared once, and the
  engine set to it"), plus `engine.md` **§33**, one gate and two lints. **M1–M3 stay OPEN** — the
  game is unchanged, which is the agreed order.
  ```
  gate · the price is in one currency   FAIL   2 currencies: `pound` x9 vs the engine's `$`
  lint · the currency in the prose             89% in `pound`; ⚠ the rent pages print "$"
  lint · the price is spelled out              8 priced labels — symbol 0%, code 75%, word 25%
                                               (field 94% / 0.8% / 5.2%)
  ```
  Score moves 31/36 → **31/37**. Findings the review did not have:
  **(1)** the defect is **six notations for one click**, not three — the sidebar prints
  `money: 12 / 100` (`v2.py:16215`, `:16241`, and it ignores `[[traits.labels]] label = "Change
  bag"` entirely), and an unaffordable choice prints `Requires 3 Money (you have 1)`
  (`v2.py:4680`);
  **(2)** `currency_symbol` reaches **four of the sixteen sites** where the engine prints money —
  `RentDay_Short` hardcodes `$` and does not even set `_cur` (`v2.py:16000`), which is why
  `forty_miles` declares `£` and still ships `$` on the screen shown when the player cannot pay;
  **(3)** off_season carries a **third** real-world currency nobody had noticed —
  `amb_lets_drawer`, *"A hairgrip, two euros, and a paperback"*.
  Appendix A.5's claim that the field never uses a currency code is **corrected above**:
  `corpo-life` uses `USD` 109 times, consistently. The correction is what shaped the rule — the
  requirement is one notation, not a particular one — and it is why the label-form check ships as
  a lint rather than a gate.

- **2026-08-22 — item 4 (§4, the clock), the SKILL half done; the game half still open.** The
  doctrine landed as `.claude/skills/author-game-v2/references/the-clock.md` (C1–C6), one gate and
  two lints. `DOCTRINE_GAPS.md` Tier 2 row 7 is closed for its time half. **T1–T3 stay OPEN** — the
  game is unchanged, which is the agreed order.
  ```
  gate · the label keeps its time    FAIL   "Work the counter till one (2h 30m)."
                                            "Work the counter till seven (3h)."
                                            · 8 stated durations all match the real spend
  lint · the clock in the prose             20.1 refs / 10k words — 20x the field median
                                            work_arcade_morning, window 08:00–13:00 (300 min):
                                              "Shutter up at eight…"                 a reading
                                              "Nobody comes in before eleven…"       a rule
  lint · time cost not on the button        7 of 11 clicks moving the clock 1h+ say nothing
  ```
  Score moves 31/35 → **31/36**. Three findings the review did not have:
  **(1)** the engine has **no absolute-time advance at all** — `grep -E
  'target_hour|advance_to|until_time|time_target' v2.py` returns zero, so `till one` was never
  reachable by any authoring choice (`references/engine.md` §32.1);
  **(2)** off_season's eight duration tags are **all accurate** — `(2h 30m)` really is
  `time_progression_minutes = 150` on `rung_arcade_take_am`'s exit — so T1's whole fix is deleting
  two words, not re-costing the rung;
  **(3)** the engine already tags **travel** time on a nav card (`v2.py:4724`, "20m") and tags
  **activity** time nowhere (`v2.py:12733`), which is where the pressure to write the hour into the
  prose comes from — and the surface that would fix it, `show_when_blocked` + `cooldown_message`
  (`v2.py:11055`), is used by **zero of the ten games** in this repo.
  Two field hypotheses were tested and **failed**, and are recorded in the skill changelog so they
  are not retried: clock *resolution* does not predict how often prose names an hour (minute-clock
  games median 2.4/10k, slot-clock 1.1), and the field does **not** place its hours differently from
  us (33.0% vs 33.5% instruction-shaped). The difference is volume alone.
- **2026-08-22 — items 2 and 3, the SKILL half done; the game half still open.** The doctrine for
  §2 (the opening) and §3 (introductions) landed as
  `.claude/skills/author-game-v2/references/the-first-hour.md` (F1–F9) plus
  `templates/first-hour.toml`, three gates and one lint. `DOCTRINE_GAPS.md` Tier 2 row 6 is closed.
  **O1–O4 and N1–N2 stay OPEN** — none of them is fixed in this game, which is the agreed order.
  Off Season now fails all three new gates:
  ```
  the opening opens a door       FAIL   hands over 07:36 at the_arcade, nothing open until 08:00
  every hub is met first         FAIL   0/4 characters introduced before their hub opens
  the anchor introduces itself   FAIL   the_arcade, declared 9,000 words, has no first visit
  lint · named before met               Ewan and Tam named in the opening, no meeting anywhere
                                        The Arcade: 1,064 words of prose, nothing says what it is
  ```
  Score moves 31/32 → **31/35**. Three new findings the review did not have:
  **(1)** the anchor is the ONE room of the ten with no first-visit canvas — five others have one;
  **(2)** the four one-shots that look like introductions do not carry `requires_npc` at all, so
  `canvas_first_borrow` can fire in an empty boat yard; **(3)** `requires_npc` would not have saved
  it either — the engine never reads that field on the auto-fire path (`v2.py:4573`,
  `references/engine.md` §31).
- **2026-08-22 — item 1 (§1, the language) doctrine landed.** `register.md` gained "The words the
  player has to already own", `gates.py` gained the `own_words` lint and `scripts/genre_words.txt`,
  and the skill's own dialect examples were rewritten. **L1–L3 stay OPEN** — the game is unchanged.
- **2026-08-22 (correction)** — the first draft of §15 (then §7) and Appendix B reported `rota` ×44,
  `lodger` ×13 and `airer` ×13 in the skill. Those were **substring** counts: *p·rota·gonist*,
  *rota·ting* and *rota·tion* all contain `rota`. Recounted with word boundaries, and excluding
  the history files (`CHANGELOG.md`, `STATUS.md`, `DOCTRINE_GAPS.md`), the live skill carried
  **27 locale-locked terms across 11 files**, of which `rota`/`rotas` is **3**. The defect is real
  and a quarter the claimed size, and the main offenders are `airer` (9) and `lodger` (8), not
  `rota`. Kept on the record because a measurement that inflates a defect fourteen-fold is the same
  class of error as one that hides it.
- **2026-08-22** — opened. 15 items from LO's read of the built v0.1, plus the field research in
  Appendix A (25 games, 10.6M words) and the causal trace in Appendix B. LO's decisions recorded:
  neutral `$`, no real-world currency; Off Season is fixed **after** the doctrine lands, as its
  proof. No fixes made.
