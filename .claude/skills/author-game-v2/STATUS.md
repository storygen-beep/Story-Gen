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
  scripts/gates.py                     the scoreboard — 40 gates + 17 lints
  scripts/genre_words.txt              the field's own vocabulary, for the word lint
  references/engine.md                 36 verified engine facts, each with file:line
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
  templates/board.toml                 fillable, parses
  templates/first-hour.toml       249   the opening shapes — a MENU, delete what you don't use
  templates/want.md               133   fillable
  DOCTRINE_GAPS.md             1,589   the studies, with their instruments and their errors
  CHANGELOG.md                     —   the full trail — every edit, dated, with how it was verified
                                       (no line count: it grows every turn, and quoting one guarantees
                                        this inventory is wrong by the end of the same session)
  STATUS.md                       —    this file
```

## The scoreboard — 40 gates, 17 lints

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
| **W5b** — the audience meter: it rises, and it refuses at 2% of 644 field read sites | `the-meters.md` |
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
| **`block_pool` in practice** | Now documented in four places and used by **zero** v2 games. Doctrine without a worked example is a suggestion. |
| **Three engine facts** | Still on the do-not-cite list in `engine.md`. |
| **Eight study sections** | See PART 7. |

## Promotion criteria — still NOT met

The description stays **EXPLICIT-INVOKE ONLY**.

The original criterion — *"one game passes all the gates"* — was satisfied by a game with 21
defects, and then again by `the_season` at 39/40 that a player could not navigate socially.

> **The binding criterion is now: a human played it end to end and it held up.** It has not
> happened yet.

---

# PART 7 — WHAT IS NEXT

## A · The eight open study sections

Eleven were scoped; LO picked three. **A (the want), C (the loop) and D (the writing) are done.**

| | section | state |
|---|---|---|
| **B** | the first fifteen minutes | **partly** — A ate most of it. Missing: what day one *refuses* to let her do, and how it says no |
| **E** | how she gets from no to yes | **partly** — D found the refusal costs and Zara's consent fork. Missing: the systematic view |
| **F** | going further | **partly** — C found the two shapes (menu grows vs. event escalates internally). Missing: rungs and spacing |
| **G** | the people | **DONE 2026-08-24** — `findings_G_people.md`. The field's answer is a UI component fired tens of thousands of times (a speaker macro is the **#1 macro in the whole game** in 7 of 25 — face + name + colour on every line), a label that encodes the relation (Stepmom · Aunt · Granny · Dr. Angela), **one term of address per person** (5–18% of their lines, never shared), and **a corner of the world each person owns**. `the_season` writes the voices well and then schedules **all four men into the camp every night** |
| **H** | does the world know? | **DONE 2026-08-23** — `findings_H_known.md`. Reputation refuses almost nothing (14 of 644 field read sites, 2%); it is read constantly and swaps ~25-word lines. `the_season`'s `known` has **7 read sites in 111 passages** |
| **I** | the body as a machine | **untouched** — clothes, arousal, hygiene, pregnancy: which are systems and which are decoration |
| **J** | what players say | **DONE 2026-08-23** — `findings_J_players.md`. ⚠️ This row previously read *"untouched"* and **that was wrong**: the 2026-07-24 mopoga study already read 22,622 comments across 31 games and published F1–F10 from them. J was narrowed to testing *this week's* doctrine against 3,479 comments on the four study games |
| **K** | the mirror | **untouched, and must be last** — it is the synthesis, not a section |

**Four are done: A, C, D, H, J and G.** The J-then-H recommendation that used to sit here is
deleted — it was written before either ran, both are finished, and the order ended up reversed
because checking the data first showed J was largely a re-run.

**G ran next because LO had already found its defect by playing** — *"I don't know who is who"* is
the section's question in a player's words, and it was the only complaint about `the_season` that
came from a human rather than a gate.

**Left: B, E and F (each partly answered by A/C/D), I (untouched), and K (the synthesis, last).**
**I** is the one genuinely untouched system question — clothes, arousal, hygiene, pregnancy, and
which of them are systems rather than decoration.

## B · The other work, unchanged in priority

1. **`the_season`'s fill.** Its one red gate. 4,412 of 15,500 words.
2. **Build the agents.** Still the largest architectural gap. Pitchers first — three independent
   takes with no shared context, the capability v1 most visibly lacks. For the Player agent's spec,
   learned expensively: **forbid page-text assertions outright**, bake in that the clock is
   `game_state.time_state`, that a repeatable canvas renders as a clickable action rather than an
   auto-fire, and that there are *two* per-day ledgers.
3. **A release that adds zero locations.** Never demonstrated, and it is what the release model
   claims to be for.
4. **A worked `block_pool`.** The doctrine is written; nothing has been authored against it.

## The operating rule that outranks all of the above

**LO plays it.** Every real advance in this skill's history came from him clicking through a game
for an hour, not from the scoreboard. Twice now the scoreboard has been green while the game was
not good. Plan for a third.
