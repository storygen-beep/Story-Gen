# author-game-v2 — the complete picture, and where we stand

*Status document. Originally written 2026-08-11 as a plan file; moved into the skill and
refreshed against a live run the same day. **Rewritten 2026-08-23** — the previous version
described a world of ten gates and one test game, and had gone materially wrong.*

> **Every number below was verified by running the scoreboard, not from memory.** When this
> document and the scoreboard disagree, the scoreboard is right. Re-verify with:
>
> ```bash
> PYTHONHASHSEED=0 python3 .claude/skills/author-game-v2/scripts/gates.py the_season
> PYTHONHASHSEED=0 python3 .claude/skills/author-game-v2/scripts/gates.py vesper
> ```
>
> **Last verified: 2026-08-23** — all 27 game directories re-scored in one pass.

---

# PART 1 — WHY v2 EXISTS

## The problem

v1 authored games as stories with chapters. The genre does not work that way: a sandbox is a
**never-ending release stream**, and everything follows from that — one ascent meter that buys
access, locations filled before new ones open, explicit content living in the surfaces the player
returns to, and every release ending on a visible locked door.

## The commitment that has held

**Nothing in this skill is taste.** Every threshold traces to a measurement, and the measurement is
inline in the script beside the number. When a threshold could not be defended it was demoted to a
lint or deleted — that has now happened five times, and each demotion is recorded where the rule
used to be.

---

# PART 2 — WHAT IS BUILT

⚠️ **No line counts in this table, deliberately.** They were quoted here until 2026-08-24 and went
stale three separate times in a single day — including once inside the same session that wrote them,
because two changelog entries were added after the number. A count of a file this skill edits every
session is wrong by the end of that session. Run `wc -l` if you need one.

```
.claude/skills/author-game-v2/
  SKILL.md                             entry point, EXPLICIT-INVOKE ONLY
  scripts/gates.py                     the scoreboard — 42 gates + 17 lints
  scripts/genre_words.txt              the field's own vocabulary, for the word lint
  references/engine.md                 37 verified engine facts, each with file:line
  references/register.md               how the prose reads once they click
  references/the-surfaces.md           which screen each piece of content lives on
  references/the-meters.md             which meters exist and who owns them
  references/the-first-hour.md         the opening, first meetings, first visits
  references/the-board.md              the world, its fill rules, the rotating slot
  references/the-clock.md              the time promised vs the time the engine keeps
  references/the-economy.md            what money is for
  references/the-voice.md              how the game talks about itself
  references/the-map.md                the world as a place someone could draw
  references/state.md                  v2_state.json schema
  references/the-release.md            the unit of work
  references/agents.md                 the roster (described, NOT built)
  references/the-want.md               the spec re-read every release
  templates/board.toml                 fillable. ⚠️ does NOT parse as-is — `<tier_1> = 0` is a
                                       placeholder, not TOML. This line read "parses" until
                                       2026-08-24; it was never true. Same for first-hour.toml's
                                       `<…>` fields, which happen to sit in string values and so
                                       do parse.
  templates/first-hour.toml       249   the opening shapes — a MENU, delete what you don't use
  templates/want.md               133   fillable
  DOCTRINE_GAPS.md             1,589   the studies, with their instruments and their errors
  CHANGELOG.md                     —   the full trail — every edit, dated, with how it was verified
                                       (no line count: it grows every turn, and quoting one guarantees
                                        this inventory is wrong by the end of the same session)
  STATUS.md                       —    this file
```

## The scoreboard — 45 gates, 28 lints

**A gate scores. A lint prints a list and refuses to score.** The split is the discipline: if a
threshold cannot be defended against a measurement, it does not get to fail a game.

`n/a` is **not** a pass — a gate with nothing to judge is excluded from the tally, because an
absence flattering an empty game is how v1's numbers lied.

Five thresholds have been demoted or deleted for failing their own evidence:

| what | why it fell |
|---|---|
| location floor (≥10,000 words/room) | the reference game failed it **24 times out of 25** |
| meter ceiling | wrong twice |
| R5 (ungated-choice ceiling) | at 50% one game passes at 50.0% and another fails at 52% — noise being scored |
| R6 (opener variation) | measured a practice nobody follows; the reference game's openers are *never* conditional |
| the v1 dialogue rule | killed by a **broken instrument** — a quote-counter that could not see `<<say>>`. Re-measured properly, restored |

---

# PART 3 — HOW WE MOVED

The arc matters more than any single number, because it repeats.

### 1 · Derived from ONE game → 10 gates

v2's doctrine came from measuring the seed source of Degrees of Lewdity. `games/back_home` was
built against it and scored **10/10**.

### 2 · LO played it → 21 defects the scoreboard could not see

The corner shop was one step from the sofa. Three of four men had no bedroom. The guidance page was
empty behind a live sidebar entry. Money was unbounded against the one obligation in the game.

> **Root cause: a doctrine derived by measuring one game cannot contain anything that game lacks.**

### 3 · Widened to a field of 18 shipped sandboxes

Four studies in `DOCTRINE_GAPS.md`. The checkable half became gates. 10 → 17.

### 4 · Widened again to 25 mopoga sandboxes

58,163 passages. Produced register.md's six screen kinds, the media floors, the narration:dialogue
ratio, and the sentence ceiling. Two instrument corrections had to be made first, and **both are
recorded, because they are why earlier studies of the same corpus got it wrong**.

### 5 · `the_season` built with all of it → 39/40

The most-instrumented game we have ever authored.

### 6 · LO played it → *"I don't know who is who"*

**The same failure as step 2, one level up.** Nothing on a 40-gate scoreboard asked whether a new
player knows who these people are. What followed came from him playing, not from a number:

- a **cast page** — shipped as an engine feature, revealed by the same quest-card gate as the
  guidance page, so there is no second gate to keep in sync
- **quest cards gated on having met the person** — no more spoilers on turn one
- the fake *"✓ Arc complete"* killed — it was `terminal` alone, never computed from progress
- **five introductions that fired in empty rooms.** Root cause was not the author: the TOML schema
  comment told authors to delete the schedule, and the skill's own doctrine said the opposite. The
  schema wins, because the schema is what is open while you type. Now gate G38.

### 7 · LO asked how we measure a *good* game

The honest answer: **we do not.** We measure "broken in a way we have seen before." Forty gates
catch old mistakes and have never once found a new one.

### 8 · Stopped counting. Started READING.

Four top female-PC games read **in source** — Course of Temptation (mopoga rank 5), Degrees of
Lewdity (7), Zara's School Life (22), Family Ties (24).
`~/Documents/Female_PC_Craft_Study_20260823/`

**The shape of the whole arc:** the evidence base keeps widening (1 game → 18 → 25) *and* the
reading keeps deepening (counted → read). **Neither has ever replaced LO playing it.** Assume it
never will.

---

# PART 4 — THE GAMES

Re-scored 2026-08-23, one pass over every game directory.

| game | score | note |
|---|---|---|
| **the_season** | **39/40** | newest, v2, 0.1 shipped. Only red: `location fill` — 4,412 words against 15,500 declared |
| **off_season** | **39/40** | v2 |
| the_allowance | 30/38 | |
| seventh_day | 29/38 | |
| forty_miles | 25/36 | |
| steam | 18/35 | |
| last_call | 17/30 | v1 |
| the_inheritance | 16/29 | v1 |
| the_long_summer_test | 16/32 | |
| back_home | 15/33 | the original 10/10 game |
| late_shifts | 13/31 | v1 |
| **vesper** | **12/32** | v1, **shipped and released**. LO's standing rule: *never* updated here |

Seven games carry a `v2_state.json` ledger: `back_home · forty_miles · off_season · seventh_day ·
steam · the_allowance · the_season`.

⚠️ **A high score is not a good game, and the two 39/40s prove it.** `the_season` scored 39/40 while
a new player could not tell who anyone was.

---

# PART 5 — WHAT THE FIELD STUDY FOUND (2026-08-23)

Full findings: `~/Documents/Female_PC_Craft_Study_20260823/`
— `findings_A_want.md` · `findings_C_loop.md` · `findings_D_writing.md` ·
`gender_verdicts.md` · `per_game/course-of-temptation.md` · `proposal_for_skill.md`

## Step 0 — the corpus is not what we assumed

**There are only three clean female-PC games in the mopoga top 30**, plus one
selectable-with-female-default. **The genre's top ranks are mostly male-PC games in which women are
the content.** Any plan that says "study the top 30 female-protagonist games" is planning against a
set that does not exist.

## The finding that landed

**Three of the four build every repeatable sexual surface out of a pool of one-sentence variants,
and none of them writes such a scene as a paragraph.**

| game | mechanism | scale |
|---|---|---|
| Course of Temptation | `<<switch setup.rir(0, 3)>>` | 164 named acts × 3 phrasings, one passage of 194,874 chars |
| Family Ties | `either("…", "…", …)` | 12 poses × ~10 lines, plus ~10 of his dialogue |
| Degrees of Lewdity | a **deterministic** grid on two meters | 99 `actions*` widgets |

**Our engine has had the same primitive since v2 shipped** — `block_pool` (`v2.py:14572`) — and
the audit found something worse than "we never knew": **the_long_summer 46 · under_one_roof 14 ·
vesper 6 · every v2 game 0.** v1's corpus carried **Rule 17** for it and named the failure exactly
(*"the same text every morning problem"*). v2's skill mentioned it once, in a list of block types,
for its whole life — it was lost when the skill was divorced from a corpus that taught false engine
facts, and nothing checked what was in the discarded half.

> Their act prose is **thinner** than ours and they rank higher. Their variety is structural; ours
> is manual. Structure survives the fiftieth visit; effort cannot afford to.

## What shipped into the skill

| change | file |
|---|---|
| **§35 `block_pool`** — the variant pool, fully cited | `engine.md` |
| **The reason axis** — *the same act, reached two ways, is written two ways, and the difference is WHY she is doing it, not how hot it is* | `register.md` |
| **The two-halves sentence** — his meter writes the first clause, hers the second; nine outcomes from six clauses | `register.md` |
| **Lines by personality, not by person** | `register.md` S3 |
| **R6 mechanism 5** — variant pools, the mechanism the field leans on hardest | `the-surfaces.md` |
| **R5b** — the decline branch is written at full length and paid | `the-surfaces.md` |
| **W5b** — the audience meter: it rises, it rarely refuses, and it still decides things (corrected 2026-08-27; the old 2%-of-644 was a three-game sample) | `the-meters.md` |
| **R5b.2** — a refusal that can never fail is a menu item | `the-surfaces.md` |
| **R6 mechanism 6** — reputation as a casting filter: who is standing there | `the-surfaces.md` |
| **§36 `rejection_node`** — the locked choice that stays clickable, used by 0 games | `engine.md` |
| a self-contradiction removed (adjacent-`[group]` merging was "unverified" in one file and fact in another) | `engine.md` |
| **R8** — a person owns a corner of the world, **and the schedule has to agree** | `the-surfaces.md` |
| **S3 · one term of address per person** — the stated exception to "lines by personality, not by person" | `register.md` |
| **W6 · the meter is a trade, not a bonus** — plus the W5 / W5b / W6 cross-pointer | `the-meters.md` |
| **§34 `[[npcs]] tags`** — the four-word cast-card line. **The one ENGINE change**: new field, capped at 4, shipped via `setup.npc_tags` | `engine.md` + `template_import.py` + `game_graph.py` + `v2.py` |
| **§34 · the colour we do not ship** — recorded as a known difference, deliberately unbuilt | `engine.md` |
| **H and G converge** — differentiation is many small swaps (139 / 84 / **114** chars), not few large branches | `SKILL.md` |
| **A per-NPC field has TWO write sites** — `game_graph.py` is the one the default build takes | `SKILL.md` + `engine.md` §34 |
| three stale citations corrected — `v2.py:14631`→`:15003`, `engine.md` §29→§34, `v2.py:1027`→`:1031` | `engine.md`, `the-first-hour.md` |

**No gate was added. `gates.py` was not touched.**

⚠️ **The verification count is 21, not 27 or 28.** Both earlier numbers were wrong and the error is
the same each time: `games/` holds **28** directories with a `toml_phases/`, but only **21** carry a
merged `7_final_game.toml`, and `gates.py` needs that file. The other seven (`jacks_world`,
`media_testbed`, `new_in_town`, `test_customize`, `the_long_summer`, `two_weeks`,
`under_one_roof`) have never been merged. **Count the merged file, not the directory.**

## What the study REFUSED to add

- **No rule about opening length.** The range is 109,714 characters (rank 5) to one paragraph of
  safety instructions (rank 7). **Two of the top seven at opposite extremes.** Any rule would be invented.
- **The pivot rule was tested and CONFIRMED, not loosened.** Zara's School Life folds heavy
  interiority into its acts and never leaves the body. Not a pivot by the rule's own definition.
- **A proposed instrument fix was tested and DROPPED.** The proposal said `gates.py` over-counts
  pooled variants. Measured across ten DoL location passages: **9,652 of 9,886 words (98%) of its
  location prose sits inside a conditional branch** (a ten-passage spot check, not a whole-game
  figure) — so folding *is* the apples-to-apples comparison against the baseline that set the
  threshold. Recorded in `engine.md` §35 so it is not re-proposed.

---

# PART 6 — WHAT IS NOT DONE

| | |
|---|---|
| **The agents** | Pitchers, attack panel, prose maker, player — all still prose in `agents.md`. No prompts, no schemas, no call sites. `scripts/` contains `gates.py` and a word list. **Still the biggest architectural hole.** |
| **Evals** | None. "v2 beats v1" cannot be scored. |
| **A cold reader** | Only one person has ever run the skill. |
| **`the_season`'s fill** | 4,412 words against 15,500 declared. Its one red gate, and the real problem with the game. |
| **`the_season`'s `known`** | Rises and repaints a quest card. **7 read sites in 111 passages**; zero in the locations, zero in the one-shots, and a median branch of 570 chars against the field's 84–139. Measured in `findings_H_known.md` §6. |
| **`block_pool` in practice** | ⚠️ **This row read *"used by zero v2 games"* until 2026-08-29 and was wrong.** Counted in phase files, merged output excluded: `the_long_summer` **152** · `mrs_vance` **77** · `under_one_roof` **14** · `vesper` **12** · `the_long_summer_test` **1**. `mrs_vance` is the v2 reference game, so the primitive did reach v2 — what is true is narrower: **five games of thirty**, and the doctrine still has no worked example of its own. |
| **One engine fact** | The do-not-cite list in `engine.md` is down to a single bullet — the cooldown count for random events. ⚠️ This row said **three** until 2026-08-29; the list held **two**, and one of those (*which identifiers orphan a live save when renamed*) had been answered on 2026-08-29 by `the-returning-player.md` §2–§5 and left sitting there. Struck, and the row recounted. |
| **`ne` — the canvas half is DONE; only quest cards are open** | ⚠️ **This row said the opposite until 2026-08-29, and the stale version was read back and acted on.** It carried *"three whitelist entries, no runtime work… not applied"* — the exact sentence `engine.md` §37 was rewritten on **2026-08-24** to correct, on the day it shipped the fix. A canvas condition's operator is not validated by the importer at all, so `ne` has always worked there; `setup.checkSingleCondition` got its case and `setup.formatCanvasConditions` got its `≠` the same day. **What is still open is one evaluator**: `setup.checkQuestsCondition` (`v2.py:15536`) has a five-case switch and quest cards reject `ne` at `template_import.py:5509`, deliberately and with a comment saying so. **Parked on evidence, not on nerve** — `ne` is legal on a canvas today and authored **zero** times across all thirty games, because until 2026-08-29 no doctrine file offered it. `the-board.md` now names the operator set; if a card then needs `ne`, the evaluator case and the whitelist go in together. |
| **The study's instruments** | Four of them published numbers and were then discarded — F1's opening walker, F's act-gate driver, and three of the recheck's rebuilds. Two of those numbers are now permanently unrecoverable. `probe_K.py` is on disk with a `main`; the earlier ones are not, and nothing enforces that they should be. |

## Promotion criteria — still NOT met

The description stays **EXPLICIT-INVOKE ONLY**.

The original criterion — *"one game passes all the gates"* — was satisfied by a game with 21
defects, and then again by `the_season` at 39/40 that a player could not navigate socially.

> **The binding criterion is now: a human played it end to end and it held up.** It has not
> happened yet.

---

# PART 7 — WHAT IS NEXT

## A · The eleven study sections — all closed

Eleven were scoped; LO picked three. **A (the want), C (the loop) and D (the writing) are done.**

| | section | state |
|---|---|---|
| **B** | the first fifteen minutes | **DONE 2026-08-24** — `findings_B_refusal.md`. **Day one refuses nothing**: 12 of 14 identifiable openings carry zero spoken refusals, Course of Temptation's 78-passage prologue included. Field-wide, only **23%** of the 27,505 conditionals wrapped around an action refuse anything — 35% are variant selectors. Of refusals, **71% render nothing**; the 28% that speak run a **median 9 words** and **60% name a handle** (price 37%, place 2%). ⚠️ The section's real find is that **`engine.md` §15 taught the opposite** — *"prefer the want"* — which is why **13 of our 176 shown-locked choices carry a reason**. §15 is reversed and gate 42 landed |
| **E** | how she gets from no to yes | **DONE 2026-08-24** — `findings_E_yes.md`. The willingness meter is **per-person in 16 of 20 games**, and the field gives the whole cast **one word on one scale** — become-someone `trust` on 62 of 64, patriarch `like` on 37 of 38 — differentiating people by **modifiers** on it, not by vocabulary. **Median 1 meter per person, median 3 rungs, 88% of thresholds shared across the cast**, and `+1` is the increment. ⚠️ **W6 taught the opposite** — a different meter per relationship type — which is why `off_season` ships four characters with four vocabularies. W6 is reframed and the meter-ladder lint's cast branch now gets a per-character comparator instead of the player-ascent 8–17 |
| **F** | going further | **DONE 2026-08-24** — `findings_F_further.md`. An act menu is **2 options wide, one step apart** (2,292 menus), and **9%** carry a finish. Of 61 arc hubs, **47 run one to four intensities and 14 run five or more** — going further mostly means *more variations at the same intensity*. And escalation is barely gated: **47%** of 7,598 act links carry no condition, her willingness gates **2%**, the player's ascent meter **13%** against her **6%**. ⚠️ **No spacing number exists** — only two arcs in the corpus space acts along a meter, and the honest answer is that the field does not build escalation as a spaced ladder |
| **G** | the people | **DONE 2026-08-24** — `findings_G_people.md`. The field's answer is a UI component fired tens of thousands of times (a speaker macro is the **#1 macro in the whole game** in 7 of 27 — face + name + colour on every line), a label that encodes the relation (Stepmom · Aunt · Granny · Dr. Angela), **one term of address per person** (5–18% of their lines, never shared), and **a corner of the world each person owns**. `the_season` writes the voices well and then schedules **all four men into the camp every night** |
| **H** | does the world know? | **DONE 2026-08-23** — `findings_H_known.md`. Reputation refuses almost nothing (14 of 644 field read sites, 2%); it is read constantly and swaps ~25-word lines. ⚠️ **Sample corrected 2026-08-27** — those 644 are three games, 95% degrees-of-lewdity; over 13 games it is ~10% link-bearing and a median 41% of reads are mechanical. Superseded by `Player_Legibility_Study_20260825` §44. `the_season`'s `known` has **7 read sites in 111 passages** |
| **I** | the body as a machine | **DONE 2026-08-24** — `findings_I_body.md`. The strongest evidence is negative: `degrees-of-lewdity` **built hygiene and switched it off** — 1,273 writes, one read site, a seven-band widget nothing calls, and `<<set $hygieneenabled to 0>> /* unused */` in its own initialiser. Corpus-wide the body gates a median **10%** of its reads (H's reputation: 2%), and a system either stays small and gates or grows large and colours. Ours: **102 garments across 10 games, 47 reads**, and four wardrobes read zero times |
| **J** | what players say | **DONE 2026-08-23** — `findings_J_players.md`. ⚠️ This row previously read *"untouched"* and **that was wrong**: the 2026-07-24 mopoga study already read 22,622 comments across 31 games and published F1–F10 from them. J was narrowed to testing *this week's* doctrine against 3,479 comments on the four study games |
| **K** | the mirror | **DONE 2026-08-24** — `findings_K_mirror.md`. The synthesis, and the first section to point the study's own instrument at **us**. Every condition in the 26-game field against every condition in our 21 scorable games, one classifier, one denominator: the field gates on **equality 53% / threshold 31% / boolean 9%**, we gate on **threshold 56% / boolean 37% / equality 4.5%**. **The field's most common way to gate anything is our rarest.** Its equality is a **stage counter** — one variable that counts — at 24.8% of all its conditions in **26 of 26 games**; ours is 0.7% in 6 of 21. ⚠️ And our **v1** games do it the field's way (`vesper` 10%, `the_long_summer_test` 11%) while our **v2** games do not (0–2%) — **the second doctrine lost in the v1 → v2 divorce, lost exactly the way `block_pool` was.** Shipped as `the-surfaces.md` R5d, `SKILL.md`'s fifth commitment, `engine.md` §37. **No gate, no lint** |

**All eleven are done: A, B, C, D, E, F, G, H, I, J and K.** (This line read *"Four are done"* over a
list of six until 2026-08-24, and *"Ten are done"* until K landed the same day.) The J-then-H recommendation that used to sit here is deleted — it was written
before either ran, both are finished, and the order ended up reversed because checking the data
first showed J was largely a re-run.

**G ran next because LO had already found its defect by playing** — *"I don't know who is who"* is
the section's question in a player's words, and it was the only complaint about `the_season` that
came from a human rather than a gate.

**Nothing is left. The study is closed.** K landed 2026-08-24 on top of the recheck, and both of the
inputs its row used to name are answered: section F's unnamed 48% collapsed to a **0.4% residue** once
classified by shape, and `the-first-hour.md` F1's 300-to-700-word band was **deleted** rather than
re-derived, because three rebuilt walkers disagree with the published table and with each other.

⚠️ **What the study did NOT produce, and it is the question that started it.** PART 3 step 7 asked how
we measure a *good* game. Eleven sections later the answer is still **we do not** — every one of them
measured what the field *does*, and the two things that ever moved this skill's quality both came from
LO playing a game. K adds a frame, not a score.

### ✅ The recheck is done — `findings_RECHECK.md`

The corpus is **27** parseable games, not 25. `tw.py` only knew `<tw-passagedata>`; three games ship
the older `<div id="store-area"><div tiddler=…>` container and parsed to zero. Two are now readable
(`college-daze`, `free-cities`); `confined-and-horny` is an engine-only file with no passage data at
all and is correctly excluded from both counts. Section B found two further faults under the same
corpus — undecoded store-area escapes, and a `tw.links()` that dropped setter links
`[[label|Target][$x += 1]]` and raw `<a data-passage>`.

Eighteen shipped field numbers were re-measured. **Every instrument was first re-run on the original
25 and checked against the figure that shipped**, because the 2026-08-18/19/22 scripts are not on
disk and a moved number is otherwise unattributable. Five reproduced exactly or near-exactly; three
did not and were used only to measure movement.

| | |
|---|---|
| **moved** | `FIELD_MEDIAN, FIELD_P75` (clock references) **1.1 / 2.1 → 0.8 / 1.8** — the one gate constant the recheck re-baselined, and it moves *against* our games |
| **was wrong all along** | `FIELD_LABEL_LONG_SHARE` shipped as **0.10**; the basis and the median reproduce but the share is **16%** on 25 and **21%** on 27, and no filter yields 10% at a median of 3 |
| **held** | `NARRATION_DIALOGUE_CEILING` · `FIELD_METER_RUNGS` / `FIELD_METER_FIRST_RUNG` · `FIELD_DOM` / `FIELD_EXACT` · `EXPLICIT_BEAT_MEDIA_FLOOR` — numerators unchanged, denominators 25 → 27 |
| **rebuilt** | `scripts/genre_words.txt` **18,043 → 20,555**, a union with the old list; the corpus is **14.7M words**, not 10.6M |
| **strengthened** | the eleven locale words are still used by **zero of 27** games; `off_season` is easier than **26 of 27**; the cast page is in **18 of 27** |
| **corrected** | `the-clock.md` C2's clock-naming label count **2 → 24** (its load-bearing zero survives) |

⚠️ **The one open item the recheck produced: `the-first-hour.md` F1's empty band.** `destroyer` was
listed as a 285-word cold open; those 285 words are its legal disclaimer and the walk stopped there
because the passage leaves through `<a data-passage>`. It is an eleven-passage, ~3,300-word staged
open, and it has been moved. **Eight of twenty-five opening walks move once the extractor can see
setter links and raw anchors.** So the two named shapes are sound but **the 300-to-700-word gap
between them is unverified**, and it is not silently repaired because F1's own walker is not on
disk. **K closed this by deleting the band** — see the K block below.

⚠️ **Sections B, E, F and I needed no recheck** — they ran after the fixes, and their own text proves
it (W6 already names `college-daze` and `free-cities`; F4b already counts fourteen openings including
both). Section C's in-degree table reproduces exactly on three of four games; only
`zaras-school-life` moves, and its conclusion survives. **That table never shipped into the skill.**

**What the recheck did NOT re-measure**, and which therefore still carry a 25-game basis. None is a
gate constant; each is a prose figure whose instrument was not recoverable in the time available:

- `the-economy.md:195` — the money-printer census across "the 25-game corpus"
- `the-clock.md:142` — the day-length instrument, "25 shipped sandboxes, 11.0M words"
- `the-surfaces.md:21` — the R-series preamble's basis line
- `register.md:259` — the 2026-08-18 provenance line (58,163 passages). Its *derived* figures were
  all re-checked and updated; only the line naming the original run still says 25, which is correct
  as history.
- `the-surfaces.md`'s room-verb table itself — the shipped keyword lists are not recorded, so it
  could not be reproduced. Re-run with equivalent lists, **every category's game count rises on 27
  and the ordering is unchanged**, so the table's conclusion holds even though its cells are stale.
- **added by K 2026-08-24** — `the-meters.md` W5's counterweight census (*"one game in 25"*), and its
  copy in `templates/board.toml:88`. Never on the recheck's list, and stale on both sides equally, so
  it is a residue rather than a contradiction.
- **added by K 2026-08-24** — the `gates.py` comments that carry the same 25-game bases as the two
  reference lines above: `:2702` and `:2707` (the clock instrument, with `the-clock.md:142`) and
  `:3100` and `:3157` (the currency census, with `the-economy.md:195`). **List the twin, always.**
  Three of K's four contradictions exist because a number was updated on one side only.

### ✅ K closed the recheck's open item, and found five numbers arguing with themselves

Every number the recheck moved was swept for a second copy that did not move with it. **Five sites
were carrying a superseded figure while its twin carried the new one:**

| the stale copy | the live one |
|---|---|
| `gates.py:1917` *"easier than 24 of the 25 field games"* | `register.md:544` *"easier than 26 of the 27"* |
| `gates.py:5180` *"2 in 92,226 across 25 sandboxes"* | `the-clock.md:403` *"24 in 84,009"* — which names the old figure explicitly |
| `templates/board.toml:80` *"14 of 25 field games have none"* | `the-board.md:243` *"15 have no player ascent tier"* of 27 |
| `SKILL.md:215` *"fewer than four of the 25 field games"* | `gates.py:1769` and `genre_words.txt`, both rebuilt on 27 |
| `genre_words.txt:11`, `gates.py:1776`, `register.md:640` — *"rebuilding on 27 ADDED 1,976 words"* | the file's own line count: 18,043 → 20,555 is **+2,512**. 1,976 is the sub-figure from the two newly-readable games, quoted as the total |

All five are fixed and each records what it used to say. **`templates/` was never swept at all by the
recheck**, which is how the third one survived; it is swept now. The fifth is arithmetic — it was
checkable against the file the whole time, and nobody counted the file.

**The rule this adds, and it is cheap: when a number moves, grep the number, not the file.** Three of
the five exist because one side of a pair was edited and the other was not.

⚠️ **And the inventory in PART 2 was wrong about `templates/board.toml`.** It said *"fillable,
parses"*. It does not parse and never did — `<tier_1> = 0` is a placeholder, not TOML — and the claim
predates the recheck entirely. Corrected above.

## B · The other work, unchanged in priority

1. **`the_season`'s fill.** Its one red gate. 4,412 of 15,500 words.
2. **Build the agents.** Still the largest architectural gap. Pitchers first — three independent
   takes with no shared context, the capability v1 most visibly lacks. For the Player agent's spec,
   learned expensively: **forbid page-text assertions outright**, bake in that the clock is
   `game_state.time_state`, that a repeatable canvas renders as a clickable action rather than an
   auto-fire, and that there are *two* per-day ledgers.
3. **A release that adds zero locations.** Never demonstrated, and it is what the release model
   claims to be for.
4. **A worked `block_pool`.** The doctrine is written and five games use the primitive
   (`mrs_vance` 77 among them) — what is missing is a worked example inside the skill, not usage
   in the field. Corrected 2026-08-29; this line previously said nothing had been authored.

## The operating rule that outranks all of the above

**LO plays it.** Every real advance in this skill's history came from him clicking through a game
for an hour, not from the scoreboard. Twice now the scoreboard has been green while the game was
not good. Plan for a third.
