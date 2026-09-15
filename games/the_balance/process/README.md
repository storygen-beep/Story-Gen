# How this game is run

**Audience: the agent working on `the_balance`, including future sessions. Not LO.**
Written 2026-09-11, during the want→board handoff.

This file exists because `the_balance` does not run the way `author-game-v2` describes, and a
session that reads only the skill will do the wrong thing confidently. Every difference below was
argued with LO and has its reason attached — **a decision without its reason gets undone by the
next session being helpful.**

---

## 0 · The rule about this file

**The skill wins everywhere except the overrides listed in §4.** This is not a parallel copy of the
process. If something is not named here, `author-game-v2` governs it, unchanged.

**Read this at the top of every block** (§2), not once per session. It is the same anti-drift rule
the Want carries, and for the same reason: the documented failure in this repo is a specification
written once and never opened again.

**How you got here:** `v2_state.json` carries a top-level `process_doc` pointer. The skill's
dispatch reads that file first on every arrival, which is the only guaranteed read in the pipeline.
If you are reading the skill and have not read this, you have already diverged. Keep the pointer
alive in every edit to `v2_state.json`.

**Do not promote any of this into the skill.** LO said so explicitly on 2026-09-11: *"I don't want
to update the skill. For this game alone, let's have separate docs in the game folder itself."*
Promotion is decided after 0.1 ships — see §6.

---

## 1 · Where the game is

```
phase          sheets         v2_state.json is authoritative. want -> sheets on 9-15, and the
                              `board` block was written the same turn: it had never existed, and
                              six gates silently degrade to backstops without it
built          SLICE 8, 9-15  games/the_balance/output/index.html · 19 locations, 10 people,
                              43 canvases, 6,300 words. 31 gates pass, seven walks clean,
                              harness 10/10, 10 of 10 explicit beats register with zero pivots.
                              ✅ EVERY ROW OF sheets/RELEASE.md's "what's in" IS BUILT.
                              slice 1 the opening and asking for the job · slice 2 THE WORKING
                              CAFE (the shift as the first repeatable surface, the first two
                              customer steps, the counter, the closing shift as a locked door) ·
                              slice 3 FRIDAY (sleep, the chore list, the $150) · slice 4 THE
                              SHOWER AND THE PHONE (clean could only go DOWN before it; going
                              live is the second road to Friday) · slice 5 THE HOUSE AND THE
                              TWO DOORS (@nate, Tasha and Lynn; his door costs a week of the
                              stream, hers is spent at the Friday table) · slice 6 CLASS IS
                              REAL (four subjects, @cara and Sam — and `rest` finally has a
                              door) · slice 7 THE CROWD (Jules, Bree and Paige, the random
                              picking-on, both dares — and the world interrupts her for the
                              first time) · slice 8 FINISHING IT (dinner, in by ten, talk, the
                              classroom walk-in) · slice 9 THE PHONE (@cara's messages, the
                              first 8_phone.toml in this repo) and the stream block that was
                              telling her the wrong reason. CONTENT-COMPLETE, not yet shipped
written        WANT.md · v2_state.json · DECISIONS.md · sheets/RELEASE.md
               sheets/OPENING.md · sheets/SYSTEMS.md
               systems: money · the_week · the_phone · her_meters · college
                        being_known · walking_in · talk · being_picked_on · the_dares
                        the_move_up · the_two_doors · the_house_day
               RELEASE.md is [READY] — LO ticked the first build on 9-15. No more design pages
               places:  the_house · the_cafe · the_campus
               people:  the_cast
next           NOT another content slice. The question is now shipping, and the three
               things between here and it: MEDIA (no image on disk, 19 locations and
               10 people declare slots), `every hub is met first` 0/10 (every portrait
               is live on turn one — a real pre-ship pass), and a version + portal
               entry. LO has asked for a straight account of that, with real numbers
not started    campus entirely · the phone and the stream · the dares · the two house doors ·
               Cara, Sam, Jules, Tasha, Nate, Hale, Reyes — nine of the eleven cast
```

`DECISIONS.md` is mirrored to Notion. Board 3d7dbced-ee38-810c-a5ce-fc37be76b8b0, via
`python3 scripts/notion_sheets_sync.py push --game the_balance`.

---

## 1b · What the Want is, and the one test

**`WANT.md` is six things and about 600 words. It holds nothing the game can count.**

| | | |
|---|---|---|
| 1 | Who she is | a situation |
| 2 | The appetite | a desire |
| 3 | The world, one line | a setting |
| 4 | The charge | why it is hot |
| 5 | The eight people, one line each | identity |
| 6 | Written as "you" | a voice |

**The test, and it is LO's:**

> **If the game can count it, it is a system. The Want holds what the game IS.**

Run it on anything proposed for that page. A debt is a number. Meters are systems by definition. A
rung is a number. A word budget is a number. All of them belong to a block.

> **The incident, 2026-09-11.** The Want was written at **4,203 words across 10 sections** — against
> the format's own *"keep it to one page; longer means vaguer"*, and twice the length of the blank
> template describing how to write one. LO cut it across eight rounds, one section per round. He was
> right every time, and twice I defended something and then had to concede it was countable: the
> debt, and the meter names.
>
> **The cause was not the Want.** Decisions had nowhere else to live, so they went there and were
> then defended one at a time. `process/` was created after most of the Want was already written.

⚠️ **`WANT.md` and `v2_state.json` are NOT the same document.** The ledger keeps keys the Want does
not — `hold_kind`, `hold_collector` — because the `collector is also the target` lint reads them.
**The ledger is what instruments read; the Want is the human compass.** Do not sync one to the other.

⚠️ **Everything cut is in `process/CARRIED.md`**, each row tagged with the block that owns it.
**Consume those rows. Do not re-derive them**, and do not treat the file as a source of truth — a row
is deleted the turn its block takes it, and the file is deleted when the last row goes.

---

## 2 · The work runs as STEPS, and a step is agreed before it is filled

**The skill's board phase is one lump: lay the whole world down, write every sheet, then LO signs
all of it at once.** This game does not do that. It runs the loop LO set on 2026-09-12:

```
1  agree what the step holds, and what it does not          <- a few lines in chat, not a document
2  write The Balance's version of it                        <- ONE page, in sheets/
3  LO ticks the two boxes
4  next step
```

**Our step says WHAT. The skill says HOW.** A step page names the room, the hour, the person and
the choice — the decisions only this game can make — and then points at the skill for how it gets
built.

⚠️ **Never copy the skill's rules into this folder.** The first draft of step 2 was five items and
every one of them was the skill's own checklist reworded — screens, buttons, the handover check. A
copy rots the moment the skill changes, and it makes LO read an engine checklist to review a story
decision. LO killed it in one line: *"it simply says how the game starts and then tell it to follow
the skill rule."*

### How the next step is picked — and it is a rule, not taste

```
1  what is BLOCKED — something already written cannot be built without it
2  if several are blocked, whatever the most other things are waiting on
3  if nothing is blocked, whatever the player sees next
```

**Leftover questions live at the tail of the page that raised them**, under *what it hands to the
steps after it*. **That tail is the queue.** No separate to-do file: a question parked somewhere
nobody reads is a decision the next session makes by accident.

Worked once already: the opening page ended on *a chore has to pay something*, which blocked its own
first choice, so money was step 3 — not because money is important in general.

⚠️ **The order is per-game. It is not part of the method.** Another game's opening blocks on
something else and money lands fifth. What carries between games is the loop, this rule, the tail,
and one page per step. **The one step order worth defaulting: *how the game starts* comes first after
the Want**, because every game has an opening, it is always the most concrete question, and it drags
the first rooms and people into existence.

⚠️ **Where does the step list END?** Open, deliberately, at LO's call on 2026-09-12 — *"no end is
fine for now."* The honest risk is on the record: with no finish line there is always one more
sensible page to write, and nine of ten v2 games died with pages and no build. Do not close this
quietly; it is his to close.

> **An answer is now on the table, unticked.** `sheets/RELEASE.md` proposes the finish line: the
> steps left are the ones its six *what's in* rows need, and nothing else. **It is a proposal until
> LO ticks the two boxes on that page.** Until he does, this stays open.

### The steps, and they are not a fixed list

```
done    1  the Want              what the game IS. Six things, nothing countable
done    2  how the game starts   her bedroom, the hallway, the kitchen at seven thirty
done    3-13 the world           money · the house · the week · the cafe · the phone · her meters
                                 the cast · the campus · college · being known · walking in
                                 everything it tracks · talk
REVIEW  14 the first build       four weeks, and what waits — sheets/RELEASE.md
then       scenes                every remaining tail row is a step, a scene or a line
```

**Step 14 is where the picking rule ran out**, and that is a signal rather than a failure. Rule 1 is
*what is BLOCKED*; by step 13 nothing was, because every open row had become the same kind of work.
When the tails all read alike, the next question is not another page of design — it is **what goes in
the build and what waits.**

**Why the opening went first.** It was **block 4** in this file until 2026-09-12, sitting behind
systems, map and people, on the reasoning that the funnel walks past rooms and characters that have
to exist first. LO inverted it and he is right: the opening is the most concrete question in the
game, and it **creates** the rooms and people it needs instead of waiting for them. An abstract step
drifts vague — S1 as written asked for *everything the game tracks* before one thing had been
decided, which is the Want's own failure repeating one layer down.

### What replaced the four-stop cap

Every step now ends in a review, so counting stops means nothing. Two guards instead:

- **One page per step. Hard.** LO could not read a 1,727-word decision sheet; five unreadable pages
  is not an improvement on one.
- **`CARRIED.md` rows have to keep falling.** Five steps with no row consumed means we are talking,
  not building.

The stall risk is unchanged and it is the reason both guards are cheap ones: ten v2 games exist,
nine shipped nothing, median life two days. The disease in this repo is **not finishing**.

### Coverage — the one thing a step order loses

A question only reaches what it reaches. Reyes, the police station and the hospital may never come
up on their own. **`CARRIED.md` and the Want's eight people are the checklist:** when the steps run
out, whatever is still on those two lists is what nothing ever needed. Cut it, or ask a question
that reaches it. Do not let it drift into the build unexamined.

### When the systems step comes up, split it by kind

`night_desk` declared six systems and all six were **ambient** — fed by every room, so no room had
anything of its own, and all six place sheets came out as chore lists: *walk the property · fix the
sign · hit the ice machine · start a load*. One bad decision, six bad sheets, caught only after the
build.

**Six things in a list looks like enough; six of the same kind is the defect, and you only see it
sorted by kind.** The field's split is the evidence:

```
corruption   written 18x   read 376x     sourced — fed in one place, read everywhere
clothes      written  6x   read 188x     sourced
money        written 27x   read  13x     ambient
```

The read-heavy ones are the systems about **who she is**, and those are the ones a room can be built
around. The order inside that step still holds — system pages first, place pages written against
them, a person page is a place x hours grid so it needs its places, a scene is one rung of a person.

### Where the pages live

`sheets/`, as ordinary sheets — `sheets/OPENING.md`, `sheets/systems/*.md`, and so on. They reach
Notion; a new folder would not, because the mirror only collects `sheets/**` and `DECISIONS.md`.
`process/` is for the agent. `sheets/` is for LO.

## 2b · Every step page opens with the rules it can break

Not a copy of the rulebook — the three or four rules that are live **at that moment**, at the top of
the page where the mistake would be made. This is where two rules cut from the Want landed, and it is
a better home than either the Want or this file.

| step | its header rule |
|---|---|
| **S1** | A game of only *ambient* systems produces a chore list. You need systems fed in one place and read everywhere |
| **S2** | Going further means she can **reach more** — more places, more people, more hours. **Never a bigger number.** A meter that climbs while the world stays the same size is decoration |
| **S3** | The obligation is an **ignition, not a tax.** It buys the opening hours and then goes quiet. Price it against a real week: eight of our ten prior games let a player clear a full week in under half a day |
| **places** | A room that answers none of *needs / work / people* is not a location yet |
| **people** | A character with no reason she wants them has no reason to exist. Cut them or write it |
| **how it starts** | The last click of the funnel must land somewhere actually open at that hour. ✅ written, `sheets/OPENING.md` |
| **the first build** | What a player can *finish*, not what has been designed. Ten games were started this way and nine handed over nothing, with pages written for all of it. ✅ written, `sheets/RELEASE.md` |
| **scenes** | The crude writing goes on surfaces she **returns to**, not on scenes she sees once. And a re-entered surface must **vary** — `block_pool`, used 0 times in every v2 game |

---

## 3 · The verdict boxes are replaced

The skill's four — **Character · Coherence · Correctness · Convenience** — came from Degrees of
Lewdity's rubric for reviewing writing submitted to *that* game. `the-sheets.md:50-51` names them
and **defines none of them.** Verified 2026-09-11 by grep across the whole v2 skill, the Notion PRD,
the sync script and `~/Documents`: no definition exists. The only definition of any of the four
anywhere in this repo is in the **v1** skill, `author-game/references/step-3-casting.md:97` —
*"Coherence: every NPC serves the core fantasy — no off-theme character"* — which is a casting rule,
not a review verdict.

LO's objection, 2026-09-11: two of the four are not his job.

He is right, and the underlying fault is that the four mix two different questions — *is this what I
want* and *is this built right*. **A human ticking "Correctness" is certifying something he cannot
check**, which is `the-sheets.md` S1's own failure — *a number on a sheet is a promise until an
instrument produces it* — wearing a checkbox.

**This game uses:**

| | who answers | how |
|---|---|---|
| **Do I want this?** | LO | checkbox |
| **Does everyone belong?** | LO | checkbox — nobody present only for realism |
| built right, will run | the agent | a reported figure, never a box |
| will players get lost | the agent measures, LO feels | a reported figure + his read |

The Notion database still carries the four original checkbox properties. **Not renamed** — renaming
Notion properties is a schema change against three other live games. The sheet header names the two
that are LO's; the other two boxes are ignored.

---

## 4 · Overrides — every place this game differs from the skill

| | override | why, and what breaks without it |
|---|---|---|
| O1 | **Board runs as five reviewed blocks** | §2 |
| O2 | **Two verdict boxes, not four** | §3 |
| O3 | **Tier rungs start at 5, not 15** | `templates/board.toml` ships a band table starting at 15 and **all sixteen declared tiers across five v2 games copied it.** The field runs 8–17 rungs starting around 5. A session that opens the template will write 15 |
| O4 | **`DECISIONS.md` written at the WANT phase** | The skill puts it at sheets. Its A block — what cannot be undone — is decided at the Want, and putting it in front of LO later means it is already spent. The file says in its own header that it is partial and re-issued in full at sheets |
| O5 | **Anything LO reads obeys §5** | §5 |
| O6 | **A wide map with a red fill gate is accepted** | 29 locations, ~116,200 words budgeted. `location fill` reads red until the prose catches up. `the-board.md` says treat every location as a debt; the red is the backlog. Do not "fix" it by shrinking the declared world |
| O8 | **The Want is six things and holds nothing countable** | §1b. It was 4,203 words and became 586. Cut material is in `CARRIED.md` against its owning block |
| O9 | **No start choice.** Deleted, not deferred | `CARRIED.md` §13. The gate reports n/a forever, which is a declared absence and not a pass. Do not rebuild it |
| O10 | **The board runs as steps, agreed one at a time, opening first** | §2. Our step says WHAT, the skill says HOW. Guards are one page per step and `CARRIED.md` rows falling — not a stop count |
| O7 | **Gil is collector and target at once, deliberately** | `the-want.md` §4a's default is that they are different people. Taken knowingly. The four constraints in `DECISIONS.md` are what keep it from eating the economy — do not quietly drop one |

---

## 5 · Writing anything LO reads

Applies to `DECISIONS.md`, every sheet, and every block review. Not to this file.

- **No `file.md` citations, no `v2.py:` line numbers, no rule ids.** The evidence lives in
  `WANT.md`, `v2_state.json` `decisions[]` and here. Duplicating it into the review surface is what
  made it unreadable.
- **A statistic only when the number IS the decision.** *"$150 a week against $220 earned"* stays.
  *"19 blank to 10 written, 80.4% engagement"* goes — it justifies a call already made.
- **Table cells under ~15 words.** A 70-word cell is a paragraph in a table's clothes.
- **Plain words.** *"trait keys are save join-keys; a rename strands every save"* →
  *"every saved game breaks."*
- **Open questions first**, above the settled material: the question, the recommendation, one line
  on why it matters.

> **The incident.** `DECISIONS.md` was pushed to Notion at 1,727 words, 13 citations, longest table
> cell 70 words. LO's response: *"hard to understand, I mean really hard."* Measured across all four
> decision sheets on disk — orientation 2,627w/32w-cell · probation 1,414w/37w · vesper_two
> 3,180w/39w · the_balance 1,727w/**70w** — the disease is systematic and this one was twice the
> worst on cell length. Rewritten same day to 1,195w · 0 citations · longest cell 18w, with no
> decision removed.

**The test:** could someone who has not read this skill say what they are being asked to decide?

---

## 6 · What a fresh session will get wrong

1. **`games/orientation` is off-limits.** It is the same premise — 18, step family, college, money
   — and it is 45-gates-green and sitting right there. LO ruled it out on 2026-09-10: *"ignore it
   like it was deleted."* Do not read it for structure, cast, map or prose. Nothing in `the_balance`
   is derived from it.
2. **British spellings fail this genre's vocabulary check.** Four were caught inside the Want:
   `cheque`→**check**, `recognising`→**recognizing**, `promotions`→**promotion** (plural fails,
   singular passes), `runners`→**joggers**. The genre also writes **step dad / step sister / step
   brother** as two words — the closed compounds are 0 of 27. Run `gates.py --words` on any new
   prose *while the nouns are being chosen*, not after.
3. **Also 0 of 27, already rejected:** undeclared · bursar · registrar · enrollment/enrolment ·
   assistantship · seminar · camgirl · livestream · laundromat · stockroom · carrel. `referrals` is
   0 of 27 too — legal in the ledger, never on a button.
4. **`block_pool` has never been used by any v2 game** — 46 uses in `the_long_summer`, 14 in
   `under_one_roof`, 6 in `vesper`, 0 across every v2 game. This game's three arcs are where that
   stops. A repeatable surface written as one paragraph is a defect here.
5. **The three arcs must stay arcs.** Nate's door, the master bedroom, the cafe floor — numbered
   one-time steps that *convert* into a repeatable. Across this repo: 1,396 canvases and no
   character anywhere has a second thing that happens. The pull toward authoring a hub in its
   finished state on day one is documented behaviour, not carelessness. Assume you are doing it.
6. **`notion_sheets_sync.py` was patched on 2026-09-11** so `write_review_order` creates
   `games/<slug>/sheets/` before writing. Before that, pushing a game whose only sheet was the
   root-level `DECISIONS.md` crashed *after* the Notion writes had succeeded.

---

## 7 · How this ends

After 0.1 ships, one of two things:

- **It worked** → propose promoting §2, §3 and §5 into `author-game-v2`. Not before; the skill's own
  rule is that a shape shipped in the format is copied harder than one shipped in a reference, and
  promoting an unproven process to every future game is the failure mode this file exists inside.
- **It did not** → this file dies with the game and the skill is unchanged.

⚠️ **One outstanding item.** `references/the-sheets.md` gained a rule **S11 · A sheet is read by a
person, not by a gate** on 2026-09-11, before LO said not to touch the skill, with a changelog entry
the same turn. §5 above is that rule's content, held per-game. **S11 is still live in the skill and
LO has not said whether to revert it.** Do not act on this without asking him.
