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
                              9-15 THE JOINT PASS — 46 narration blocks rewritten after LO read
                              the build and found the prose packed facts together without
                              saying how they related. `but` ran at 0.14 per 1,000 words
                              against a field MINIMUM of 2.46, and zero in narration. Now
                              2.79. See §5b — the rule and the numbers live there
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
| O12 | **This game's checks live in `process/`, not the scratchpad** | `.claude/agents/v2-player.md:75-79` says probe scripts go in the scratchpad and *never* into `games/`. That rule is right about throwaway probes and wrong about a regression suite: eight walkthrough scripts were written during slices 1–8, lived in the scratchpad, and were wiped. **A check that dies with the session is not a check.** `process/joints.py`, `process/tokens.py` and `process/walks.py` are checked in. Run all three before calling a slice done |
| O11 | **Anything the PLAYER reads obeys §5b and §5c** | §5b is how a sentence is joined; §5c is when an `@token` is a bug. The skill's `register.md` governs length, density and the explicit pivot, and nothing in it governs how two clauses are joined. The first build ran `but` at 0.14 per 1,000 words against a field **minimum** of 2.46 — zero in narration. Run `process/joints.py` before calling prose done |
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

## 5a · WHY the prose keeps coming out compressed

**Read this before §5b.** §5b says what to do. This says what you are fighting, and a session that
does not know why will re-derive the same shortcuts and call them craft.

**The evidence that a note alone is not enough:** §5b was written on **2026-09-15**. On
**2026-09-16** the opening shipped reading *"Your mum doesn't know he paid."* — a pronoun pointing at
nobody, on the game's first screen — out of the same session that wrote §5b. That is why §5a has a
script attached (`process/readable.py`) and §5b did not.

Three forces push every beat the same way. Nothing in the build pushes back.

### 1 · Every writing threshold is a maximum. There is no minimum.

`gates.py:7390` is the whole thing in one line:

```python
gate("sentence length", ... med_sent <= SENTENCE_CEILING, ...)
```

**It passes more comfortably the shorter you write.** A median of three words clears it by the widest
margin available. Same direction for every other threshold that touches prose — `DASH_CEILING`,
`NARRATION_DIALOGUE_CEILING`, `MENU_CEILING`, `FIELD_NEGATION_MAX`.

⚠️ **Say this precisely.** The claim is *no floor on sentence-level readability*, **not** "no floors
at all." `EXPLICIT_BEAT_FLOOR` and `EXPLICIT_BEAT_MEDIA_FLOOR` are real floors — they are about
explicit content and media volume. `MEDIAN_LOCATION_WORDS` is a volume target, and 3,000 words of
fragments clears it. Grep `gates.py` for `too short`, `sentence_floor`, `min_words`, `finite verb` or
`antecedent`: **nothing comes back.** That is the actual gap.

Cutting a word always makes the score better or leaves it flat. **Nothing in the build has ever told
this repo it went too far.**

### 2 · The beat budget makes grammar the cheapest thing to cut

~35–40 words per beat is correct and measured (`register.md:387`). But when you shop for words to
lose, the subject and the verb are the cheapest, because they carry no *information*:

```
"You turned eighteen last month."   5 words, 1 fact
"Eighteen last month."              3 words, 1 fact   ← saves 2, loses the sentence
```

The fact survives the cut. The sentence does not. **Nothing measures the sentence.** The budget is
not the bug; the absence of anything noticing what the budget was paid for is.

### 3 · Caveman ultra bleeds from chat into the beat

`CLAUDE.md:60` puts this repo's **chat** in a register that drops articles and likes fragments.
`CLAUDE.md:86` draws the line itself:

> **A beat is persisted text.** Compression has never governed a beat and must not start.

The prose is written in the same session as the chat, and it leaks. ***"Eighteen last month."* is
caveman ultra** — the chat register, rendered to a player. The boundary is already written down. It
was crossed anyway, which is what a boundary with no instrument behind it does.

### The standing instruction

> Before writing any beat, **read it as someone who has played nothing.** Every sentence needs a
> subject and a verb. Every pronoun needs somebody on the same screen to point at. The word budget is
> never paid for by deleting grammar.

### The instrument

`venv/bin/python games/the_balance/process/readable.py` — **a list, never a score**, same contract as
`joints.py` and `tokens.py`. It refuses to score compression, because `register.md:1041-1043` measured
fragment density across the field and **refused a threshold** (5.3%–58.6%); fragments are legitimate
writing. It finds three things that are *facts* instead:

- **A · a pronoun with nothing to point at** — gender-aware, which is the whole point: *"your mum"*
  is present on screen one and is exactly who *"he"* is not. Canvases with an `npc` on their trigger
  are exempt, because the player clicked that person's name to get in.
- **B · short sentences carrying no finite verb**, one-shot screens first. Approximate by design and
  printed for a human, never judged.
- **C · a line about an event the player was never given** — *"the thing on Tuesday"*, *"you know
  which one"*, *"You were in late Tuesday"* — with nothing in scope that proves it happened. This is
  A one level out: a pronoun points at a **person**, this points at an **event**.

**What makes C usable is what it refuses to flag.** A weekday on its own is not a hit — her shifts
really are Tuesday and Sunday, Friday really is the payment. It wants a reference to a *specific past
occasion*, and it clears one three ways: a **flag** (the thing is recorded), a **trait** (a meter can
encode an occurrence — `attend_3 < 40` means she really did skip it), or an **exact schedule** (a
canvas that fires only on Friday may say *"on a Friday"*). Three phrases are not clearable by a meter
at all, because they claim the player **remembers** — *"you know which one"*, *"the thing on"*, a bare
*"what happened"*. No threshold establishes a memory. And a second, softer list catches what gating
alone misses: **the event is proved but the DAY is not**.

⚠️ `opening_done` counts as **no gate**. It is set on screen three and never unset, so a canvas gated
only on it is ungated for this purpose.

Each check is regression-tested against the bug that caused it — see the file's own docstring for the
two commands. Check A must flag `canvas_opening / wake` at `5f8424a`; check C must find **five** at
`1c9837c` and **zero** at HEAD. **A check that cannot catch the defect it was written for is
decoration.**

---

## 5b · Writing what the player reads

§5 governs the documents LO signs. This governs the prose on the other side of a click, and it
exists because the two are different voices and only one of them had a rule.

> **The incident, 2026-09-15.** LO read the first build and said the writing was *"very short and
> compressed and several pieces of information were packed together without clear grammatical
> relationships."* Measured against the 25-game field corpus, one number was outside the
> distribution entirely, and it was not the one I first blamed:
>
> ```
>                          field, 25 games        the_balance
>   but per 1,000 words    2.46 – 8.44 (med 4.68)     0.14      BELOW THE FIELD MINIMUM
>   and per 1,000 words    9.3  – 41.1 (med 22.8)    41.8       above the field maximum
>   coordination : subordination   0.95 – 3.89        3.17      inside
> ```
>
> Not below the median — below the **minimum**. Zero of the 25 games come in under 0.5. In narration
> alone the game ran a flat **zero** across 5,775 words: the two uses in the whole build were both
> spoken by characters. The house carries it too — `vesper` 1.19, `vesper_two` 0.28, all three
> outside the field's range on the low side.

### The rule

**The joint between two clauses is a choice, and two of the available joints carry no information.**
`and` and a bare full stop both mean *here is the next thing*. When they do most of the joining, the
reader is handed the facts and left to work out how they relate.

**If the reader has to supply the relationship, the sentence is not finished.**

**`but` is the one to watch.** A narrator that never contradicts itself is the tell, because nothing
it says is ever *against* what it just said. Every fact arrives as an addition.

### The ladder, in order

1. **Cut.** The clause was often doing nothing, and the fact beside it was already carrying the beat.
2. **Split.** Two sentences, if neither clause needs the other.
3. **Name the relationship** — `but`, `because`, `so`, `though`, `while`, `then`.

**Never a comma.** Swapping the mark leaves the joint in place. **Never "add a clause"** — see the
trap below.

#### ⚠️ Split is the rung that bites back

**Split takes one over-joined sentence and can hand back two under-joined ones.** That is a lateral
move, not a fix, and the 2026-09-15 pass made it on the last line of the game's opening:

> *Early for nothing in particular, which is still better than late.* (one sentence, 14 words)
> → *Early for nothing in particular. Still better than late.* (two fragments, 5 and 4)

The gloss died and the compression got worse. **Split only when both halves keep a finite verb and
the relationship survives the cut.** Otherwise the rung you want is 3, not 2.

The same pass then over-corrected the other way: joining every clause pushed the opening to a median
of **18 words** a sentence against `SENTENCE_CEILING = 14` (`gates.py:133`, field median 10). Naming
a relationship does not mean welding the facts into one sentence. Two joined sentences beat one long
one. **The target is that no fact arrives unattached — not that no sentence ends.**

### ⚠️ The trap: do not trade `and` for `, which is`

The game already over-used the one subordinator it had — the `, which is` clause that explains the
fact just written. The skill's `register.md` load rule L1 bans it outright, the field runs a median
of 0.06 against our 3.46 per 1,000 words, and a pass that adds relationship words can very easily
add glosses instead.

**`but` and `because` join two facts. `, which is` appends an opinion about one of them.** Where a
judgment is worth keeping, give it its own sentence — that is L1's own prescription:

> *Jules does not join in and does not stop her, and that is the arrangement they have.*
> → *Jules does not join in and does not stop her. That is the arrangement they have.*

### What is NOT a defect

Named explicitly, because the obvious over-correction is worse than the original.

- **Short sentences and fragments.** The skill measured fragments across the field and **refused** a
  threshold — the range is 5.3% to 58.6% and nothing survives it. *"Six hours. You had two seconds."*
  is correct: the contrast is unmissable without a conjunction.
- **`and` joining a real sequence** of physical actions, which is most of what an explicit beat is,
  or two properties of one subject.
- **The coordination ratio.** Ours sits inside the field's range and always did. This is about
  recoverability, not length — and `register.md:640` still says escalate by adding beats, never by
  lengthening sentences.

### ⚠️ A pronoun is a joint too, and it needs something to point at

The sharpest compression defect in the first build was not a conjunction. It was `he`.

Screen one of the game ended *"Your mum doesn't know he paid."* — and **the player had met nobody.**
No name, no role, no antecedent anywhere on the screen. The reader cannot assemble the sentence at
all, which is the complaint that started this whole pass in its purest form.

The cause is a misread of the design sheet. `sheets/OPENING.md` says *"nobody is named yet"* — and
its own bullets say *"her **step dad** paid her tuition"*. **"Nobody is named" withholds the NAME.
It does not mean nobody is identified.** The author dropped the role along with the name and left a
pronoun pointing at nothing.

**The fix is `@gil.rel`, and it is the exact opposite of §5c's fix.** §5c is about surfaces the
engine does not resolve, where the text must need neither name nor relationship. Canvas block prose
is a surface that **does** resolve (`v2.py:15483`), and `@gil.rel` emits
`<<print $npcs["npc_gil"].relationship>>` (`v2.py:14976`). `CustomizeCharacters` is the start
passage (`v2.py:1075`), so the player has already picked the relationship before the opening renders,
and `relationship = "step dad"` is seeded in the TOML so an untouched listbox still prints a word.
Verified live under two choices: *"Your step dad paid"* and *"Your uncle paid"*.

**So: strip a token off a label, put one into prose.** Before using a pronoun on an early screen,
find its antecedent on that same screen. If there isn't one, the pronoun is the defect.

### ⚠️ A NAMED DAY IS A CLAIM, AND THE GAME HAS TO BE ABLE TO BACK IT

LO, 2026-09-16, reading the college scenes: *"What happened on Tuesday?? People are talking about it
in college??"* Nothing had happened on Tuesday. Three characters referred to it anyway, on the first
morning of the game.

This is the **same defect as the dangling pronoun one section up**, one level out. A pronoun points at
a person; *"the thing on Tuesday"* points at an **event**. Both fail the same way: the prose assumes a
memory the player was never given.

**The test.** For every specific a line names — a weekday, *"the thing on X"*, *"you know which one"*,
*"what happened"* — ask: **can the state prove it?**

- ✅ **Earned** — a standing fact the game declares. Her shifts *are* Tuesday and Sunday, Friday *is*
  the payment, classes *are* Monday/Wednesday and Tuesday/Thursday. Say those days freely.
- ✅ **Earned** — gated on the thing itself. Cara's *"Where were you Thursday?"* sits under
  `attend_3 < 40`, so she really did miss it.
- ❌ **Unearned** — a specific past event with no flag or trait behind it. *"He knows about Tuesday"*,
  *"Neither of you says anything about Tuesday night"*, *"a Tuesday, and you know which one."*

**And gating is only half of it — drop the invented day too.** @gil's dinner line was correctly gated
on `home_after_ten >= 1`, and still said *"on Tuesday"*. The meter counts that she came in late; it
has never recorded **which night**. If the state cannot name the day, neither can the character.

#### The mechanism: `block_pool` cannot be gated, at any depth

`block_pool` renders as `<<set _bp to random(0, N)>>` and an if/elseif chain of its members
(`v2.py:15088`). **It reads no conditions.** All three leaking lines were pool members — which is why
they could greet a player on day one.

**The fix is a ladder with a pool inside each rung.** Consecutive `group` blocks merge into one
`<<if>>/<<elseif>>/<<else>>` chain, a group with **no** conditions becomes the `<<else>>`, and a group
renders its children through the same converter — so a pool nests inside a branch and keeps its
variety:

```toml
[[canvases.nodes.blocks]]
type = "group"
props = { conditions = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "player", trait_key = "home_after_ten", operator = "gte", value = 1 },
] } }
blocks = [ { type = "block_pool", blocks = [ ...the lines that need the event... ] } ]

[[canvases.nodes.blocks]]
type = "group"                       # no conditions — this is the <<else>>
blocks = [ { type = "block_pool", blocks = [ ...the lines that are always true... ] } ]
```

⚠️ **Both halves get walked.** A rung that never fires is as wrong as one that always does, so
`walks.py crowd` samples sixteen screens on each side of the gate — once at `dare_chain 0` to prove
nobody mentions a dare, once after to prove somebody does. One visit proves nothing about a pool.

### ⚠️ A whole-game rate cannot see the screen that matters most

`joints.py` reports per 1,000 words over ~7,200 words. The opening canvas is under 300 of them, so
**it cannot move a single number on that page however badly it is written** — and it is the one
screen every player reads. It shipped at a median of 9 words a sentence against 13 for the rest of
the game, through a pass that was driven by those rates and came back green.

Worse: **a screen of pure fragments scores perfectly on `and per 1,000 words`**, because prose with
no joints has no joints to count. Under-joining is invisible to a joint rate by construction.

`joints.py` now prints a **per-canvas median sentence length** under the rates. Not a threshold — a
spread, so a canvas far from its own game's middle gets looked at. It found five more on its first
run: `wash` and `listen_union` at 7, `sam_talks`, `canvas_ask_owen` and `dare_1_offer` at 8.

### What the pass moved, 2026-09-15

46 narration blocks across `2_one_shots`, `3_activities` and `5_scenes`. Dialogue and phone messages
were left alone: speech already used `but` and people talk in fragments on purpose.

```
                         before    after     field
  and per 1,000 words      41.8     36.1     9.3 – 41.1     back inside
  but per 1,000 words      0.14     2.79     2.46 – 8.44    back inside
  coordination : subord.   3.17     2.63     0.95 – 3.89    inside throughout
  welded glosses             23       13     —              down, never up
  total words            7,197    7,171     —              the pass is word-negative
```

**Measure it with `venv/bin/python games/the_balance/process/joints.py`.** It prints the numbers
beside the field and grades nothing. It is a list, never a score: the field corpus is built HTML and
ours is authored TOML, so a rate over word count is comparable and anything per-sentence is not.

**Not fixed here:** `vesper` and `vesper_two` carry the same habit and were not rewritten. The skill
was not edited either — §0 of this file stands.

---

## 5c · An `@token` is right in prose and wrong in a label

**`npc_gil` and `npc_nate` are `customizable = true`** (`1_metadata_and_locations.toml:200`, `:271`).
The player can rename them, and a listbox lets them change the relationship too. That is why the
prose says `@gil` and must keep saying it.

**But the generator only resolves tokens where it calls a resolver.** Everywhere else the raw `@gil`
goes on screen.

| resolves — keep the token | never resolves — write text instead |
|---|---|
| canvas block `content`, canvas choice `text` | a location `name` |
| a location `description`, `blocked_message`, `description_variants[].text` | an npc `description`, `tags[]`, `relationship_options[]` |
| door `description`, door option `text` and `locked_text` | a quest card `text`, `tip`, `ready_text` |
| npc `role` | `traits.labels[].label` |
| every phone surface, and `story_arc` emotion ranges | a canvas choice `locked_text` |

> **The incident, 2026-09-16.** The first build shipped **nine** leaks. The character-creation
> screen — the very first screen — read *"@gil's son, twenty, a senior at your college."* And
> `locations[nate_room].name = "@nate's Room"` printed on **nine** surfaces: the nav card, the nav
> link, the room heading, the back and leave links, the Quests 📍 line, the Cast 📍 line and the
> schedule table. It survived nine slices because those are the two screens nobody tests.

### The fix is the ROLE, and not even that

⚠️ **Do not write "Gil".** A hardcoded name breaks the moment a player renames him, which is the
entire reason the token exists. And **do not write "your step dad" either** — the relationship is a
listbox too (`["step dad", "mum's husband", "dad", "uncle"]`).

**On a non-resolving surface, write text that needs neither the name nor the relationship.**
`@nate's Room` became **`His Room`**. *"@gil's son, twenty"* became *"Twenty, a senior at your
college, and he has lived in this house longer than you have."* Most of them read better afterwards:
*"in @nate's year"* became *"in the year above"*, which is clearer than the name ever was.

⚠️ **On the character screen a resolved token would be wrong anyway** — nobody has been named yet
when it renders. `0_systems_spec.toml:52` already says so about the player's own description.

**Check it with `venv/bin/python games/the_balance/process/tokens.py`.** `gates.py` has this lint
too, but it scans eight hardcoded keys, top-level only, and drops any value that is not a string
(`gates.py:1292`) — which hides every list field, and that is where three of the nine were.

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
4. **`block_pool` cannot be gated, and that is how three lines about a Tuesday that never happened
   shipped.** It is `random(0, N)` and nothing else (`v2.py:15088`) — no conditions, at any depth. A
   pool member is a line that can fire on the first morning of the game. See §5b. And separately:
   **`block_pool` has never been used by any v2 game** — 46 uses in `the_long_summer`, 14 in
   `under_one_roof`, 6 in `vesper`, 0 across every v2 game. This game's three arcs are where that
   stops. A repeatable surface written as one paragraph is a defect here.
5. **The three arcs must stay arcs.** Nate's door, the master bedroom, the cafe floor — numbered
   one-time steps that *convert* into a repeatable. Across this repo: 1,396 canvases and no
   character anywhere has a second thing that happens. The pull toward authoring a hub in its
   finished state on day one is documented behaviour, not carelessness. Assume you are doing it.
6. **A location's `costs` block is a toll on the ROOM, not on the ROAD — never put one on a hub.**
   The engine charges a destination's entry cost on *any* move into it (`v2.py:16267`), and it
   cannot tell arriving from town apart from walking back out of one of that place's own rooms.
   `the_quad` carried the bus fare, so leaving a lecture re-charged $2 and forty minutes, on a hub
   with six rooms hanging off it. **And at $0 the failure was a coin flip, not a clean refusal:**
   the intercept runs on `passagestart` and its `return` does not cancel navigation, so the
   destination still rendered — a random ambient firing there took the screen and she got in free
   and uncharged, and when nothing fired the queued `Engine.play("TravelBlock")` won and its only
   link went back where she came from. Both branches verified on the pre-fix build.
   The fare now lives on choices inside `catch_the_bus` / `bus_back_quad` / `bus_back_strip`, which
   is where `v2_state.json` `board.map.bridges` always put it — *an edge between two places*.
   ⚠️ Two engine facts to keep: `navigation_order` **hard-fails** the validator if it names anything
   that is not a real child, and a location's `parent` makes it **inherit the parent's canvases**
   (`v2.py:20660`), so neither is a way to hide a nav card.
7. **No instrument walks the map by clicking, except `walks.py travel`.** Every other route here
   teleports with `stand_at` + `goto`, and `playtest.py`'s *every location resolves* only proves a
   passage renders — a one-way room renders perfectly. If you change the shape of the map, that
   route is the check.
8. **`gates.py` G11 *world reachable* now FAILS this game, and the fail is expected.** The gate
   floods `entry_from` + `navigation_order` on foot and exempts a sealed zone's *entrance*
   (`auto_exit = false`) but not the rooms behind it, so the six campus and strip interiors read as
   stranded. They are not: `walks.py travel` proves every one can be left, broke. Fixing the gate
   means editing the skill, which is LO's call and has not been made — see §0.
9. **`notion_sheets_sync.py` was patched on 2026-09-11** so `write_review_order` creates
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
