# Skill changes owed — do not apply yet

**Written under LO's instruction: do not update `author-game-v2` until the experiment proves out.**
It has. `night_desk` 0.0.1 was built on 2026-08-31 — 39/40 gates, 35/35 canvases — and the promotion
pass ran the same day.

**Status: 10 of 12 applied.** Open: §6 (coverage by simulated play) and §7 (media identity). Both are
real findings with **no mechanism**, and a rule with nothing that runs it is another line nobody
checks. They stay here until there is a script.

| | | |
|---|---|---|
| §1 the opening is a floor read as a design | ✅ applied | `the-first-hour.md` F2b |
| §2 no review artifact of any kind | ✅ applied | **NEW** `the-sheets.md` + a `sheets` phase |
| §3 the reference game's own writer rules | ✅ applied | `the-board.md` |
| §4 the discipline has no name here | ✅ applied | `SKILL.md` |
| §5 minimum viable mass | ✅ applied | `the-release.md` § Minimum viable mass |
| §6 coverage by simulated play | ⬜ open | no mechanism |
| §7 the instrument is inverted (media) | ⬜ open | no mechanism |
| §8 agent review is ~a third wrong | ✅ applied | `the-sheets.md` workflow — the writer is not the implementer |
| §9 a summary must be derived, not composed | ✅ applied | `the-sheets.md` § Summaries |
| §10 the opening is prose, never screens | ✅ applied | `the-first-hour.md` F2b |
| §11 the explicit floor's denominator | ✅ applied | `gates.py` G2, 2026-08-31 |
| §12 a sheet can call a beat explicit and be wrong | ✅ applied | `the-sheets.md` S1 |

⚠️ **§12 is applied as doctrine and NOT as a check.** LO's call was docs only, so `the-sheets.md` S1
tells an author to measure with the instrument and ships no instrument for sheets. The next thing
this file is owed is `gates.py --sheets`.

---

## 1 · How a game starts — F4 is a floor presented as a design ⚠️ THE ONE LO CALLED OUT

**Skill today:** `the-first-hour.md` F4 — *"For every system switched ON… either a named beat in the
first hour arms it, or it sits on the sidebar at value-zero."*

**What we concluded:** that is a **minimum**, not a shape, and reading it as the design is how you
get a game that never explains itself. The opening should carry a **dedicated mechanics beat** that
names the game and states every live system as a plain list — what it is, and what moves it.

**Change owed:** F4 gains the stronger shape above it, and the boot's beat order gets stated —
**setup, mechanics, the one choice, handover.** F2 currently describes what boot and capstone are
*for* and never says what goes in them in what order.

**Two supporting rules that also need writing, because neither exists anywhere:**

- **The opening may be denser than the rest of the game.** The flat-prose rule exists because rooms
  are re-entered forty times and density rots. The opening is seen **once** — the same argument that
  already lets a one-time capstone spend prose. It is the one place a list beats a paragraph, and
  the skill currently has no sentence permitting it.
- **Naming the game is what makes a mechanics beat legal.** Breaking frame deliberately, with a real
  `heading` block, then closing it again. The skill says nothing about frame at all.

---

## 2 · The review apparatus — the skill has no review artifact of any kind

**Skill today:** 46 gates and 31 lints, all reading `7_final_game.toml` after the fact. The author
writes TOML; nothing is reviewed by a human before it exists.

**What we concluded:** a sandbox in this engine **cannot be reviewed by playing it** — Ashwell 2015,
on the two patterns our games are built from: *"Reviewers may miss narrative content if exploration
becomes tedious"* (Open Map) and *"Reviewers struggle to assess completeness"* (Floating Modules).
So the review surface must be **generated, not experienced**.

**Change owed:** the sheet formats in [`FORMAT.md`](FORMAT.md) — place, person, scene, decision, opening —
promoted into the skill, plus the workflow they sit in (`[REVIEW]` → `[READY]` → `[GAME-READY]`,
the writer not being the implementer).

---

## 3 · Everything from the reference game's own Writer's Guide

Read 2026-08-31 from `gitgud.io/Vrelnir/degrees-of-lewdity.wiki.git`. **We have measured that game
ten ways and never read its instructions to its own writers.** Four rules it has that we do not:

- **The three-way personality check is mandatory.** *"It is essential you include all three checks
  when the player speaks up."* Meek / bratty / neutral on every player line. This is the mechanism
  behind the field's largest love-reason (freedom, 25.9%, against premise at 0.0%) and our eight
  games have no player-identity axis at all. It is `block_pool`, which **zero v2 games use.**
- **Per-character mood axes are enumerated and required.** Robin cheerful↔traumatised, Kylar
  shy↔obsessive, Sydney pure↔corrupt. *"Scenes that can trigger at any level of trauma need variants
  to cover both."* We have per-NPC meters and no rule that a scene must cover their range.
- **A required exit matrix on every encounter** — fights him off / makes him finish / asks him to
  stop, the first two *required for all encounters*. Our `she can say no` fails only on zero across
  a whole game.
- **Character bibles are one line.** *"Bailey: The caretaker. Rules the orphanage with an iron fist.
  Extorts the orphans for what they're worth. Confident and pragmatic."* Ours run pages.

Their submission rubric is four categories — **Character · Coherence · Correctness · Convenience** —
and worth adopting as the shape of a review verdict.

---

## 4 · The discipline this architecture belongs to — zero mentions in 21,831 lines

`storylet` 0 · `quality-based` 0 · `QBN` 0 · `salience` 0 · `Failbetter` 0 · `Ashwell` 0 ·
`Emily Short` 0.

Our games are **Loop and Grow + Open Map + Floating Modules**, and each of those has published
failure modes that match defects we have already shipped — including *"writers tend to rebound
quickly to a more unified structure"* (the arc pull, a known property of the structure, not
indiscipline) and *"requires substantial content; collapses into linearity otherwise."*

**Change owed:** name the structure in the skill, with its published weaknesses beside our matching
defects.

---

## 5 · Minimum viable mass — nowhere in the skill

Three independent lines agree this architecture has a floor below which nothing works:

- DoL's **seed** was 116,540 words across 25 locations — mean 4,661 per location
- Ashwell: Floating Modules *"requires substantial content; collapses into linearity otherwise"*
- Failbetter's own StoryNexus retrospective: *"time-to-bootstrap… making a minimally playable
  experience took ages because one had to create quite a number of storylets"*

Ours open 8–14 locations at roughly 1,000 words each. **The skill's release cadence — "+196 units,
zero new locations" — was measured from a mature 2.24M-word DoL and adopted as our construction
method.** Ten v2 games, median lifespan two days, nine with zero archived releases.

**Change owed:** the skill must state a seed size before the release stream begins, and must say
that its cadence figures describe maintenance, not construction.

---

## 6 · The review method for this architecture — coverage by simulated play

Emily Short, on validating a QBN/salience system: *"run a few thousand randomized playthroughs and
use some visualization tools to see whether there were sequences that never got hit and whether
there were some that seemed to be overused."*

We have `playtest.py` (drives a browser) and `--release`'s `every canvas is a passage`. We do not
have the loop: N randomized runs → what never fired, what fired too much, what was thin on arrival.

**Both our worst shipped defects were coverage failures** — six sex loops written and deleted from
the build, and commuter's landing at 112 words of a declared 1,400. Neither is visible in the TOML.

---

## 7 · What the audience actually reviews — our instrument is inverted

Measured across 22,615 comments on 31 games:

| what a comment judges | comments | likes | our gates |
|---|---|---|---|
| media — images, video, AI, models | 423 | 2,128 | **2**, both presence-only |
| progression with a named person | 213 | 1,178 | ~9 |
| content volume | 146 | 904 | **1** |
| **prose quality** | **25 (0.11%)** | **127** | **4** + 1,207 lines of `register.md` |

The single most-endorsed judgement in the whole corpus is *"the ai visuals ruined the game"* at 138
likes, with three more of the top four also about media. **We cannot see media *fit* at all** — only
presence.

**Change owed:** a media-identity check, and an honest note that `register.md`'s weight is
disproportionate to what players judge.

---

## 8 · Agent-generated review is about a third wrong

`mrs_vance/REVIEW.md`: 43 findings, **14 self-corrections** in its own §0a. `forty_miles/REVIEW.md`:
4 findings, 3 corrections.

**Change owed:** any review artifact the skill produces needs a verification pass built in before it
reaches LO, and the skill should say plainly that an agent review is a first draft, not a verdict.

---

## 9 · A summary must be derived, not composed

The failure that started this whole thread: a summary written by the same session that wrote the
content describes what was **intended**. Commuter's would have said *"the landing is built."* It was
112 words of 1,400, with 46 green gates over it.

**Change owed:** wherever the skill produces a summary, the **measured** half is generated from the
source and kept visibly apart from the **intent** half.

---

## 10 · The opening is specified as prose and never as SCREENS

**Skill today:** `the-first-hour.md` F1–F10 specify a boot, a capstone, a meeting per character, the
systems taught as a set, and a handover into an open door. **Every one of them is about what the
opening SAYS.** Nothing in the skill asks how many screens that is, what is written on the button
between two of them, or what the player sees before the first one.

**What we concluded:** an opening sheet can satisfy every rule in F1–F10 and still not be buildable,
because the author has not decided whether three beats are one screen or three. It happened here on
the first draft, and the timeline and checklist views both passed it.

**Change owed — a screen-walk view**, one row per screen with the button quoted, promoted alongside
the timeline and the checklist. Plus four engine facts the skill does not carry anywhere:

- **The age gate is screen 0.** `engine.md` §12 has it, and `the-first-hour.md` never refers to it,
  so every opening the skill has ever specified began one screen late.
- **`[player] customizable` inserts a whole screen and repoints the age gate at it**
  (`v2.py:1065`, `v2.py:9251`). **Seven of fifteen built games ship it.** The skill does not mention
  it in the opening reference at all, and its headings and button are hard-coded — *"Personalize the
  characters in your story"* lands on the player's second screen in whatever voice the game has.
  The only authored text is `player_description` (`v2.py:9509`), and an author who does not know
  that ships the default.
- **One node is one screen**, and mid-chain exits are `exit_block.type = "choices"` with a single
  choice whose `text` is the button. `the-first-hour.md:170` states the first half in passing while
  arguing something else; the button is stated nowhere.
- **The last node's `exit_block.type = "location"` config is where the opening sets its flags and
  pays its first money** — so the handover is a mechanical event, not just a destination.

**And one design rule that is not in the skill in any form:** *the funnel should contain the job,
done once.* Ours are narration plus a name box; the field's largest openings are funnels the player
acts inside. Course of Temptation's 78-passage prologue carries **seven conditionals and not one
refusal** (F4b) — it is full of choices, all of which colour and none of which gate.

**Would a correct skill have prevented this?** Yes. This is a class defect, and the measurement says
so: **eight of our fifteen built openings are a single screen**, then the sandbox opens.

---

## 11 · The explicit floor divides by the wrong denominator — ✅ APPLIED 2026-08-31

⚠️ **Correction to my first write of this entry.** I framed this as `the-first-hour.md` F4b fighting
the explicit floor. **That was wrong** — F4b is about *refusals* (*"teach it, and do not gate on it
yet"*), and says nothing about heat. What makes an opening cold is that the protagonist starts at
zero, not any rule. The problem is real but it lives in the metric, not in a rule conflict.

**Skill today:** `pct = 100 * len(expl) / max(len(all_beats), 1)` (`gates.py:4277`) — explicit beats
over **every beat in the game**, one-shots included.

**What we concluded:** that ratio answers *"what share of this game's text is explicit?"* The
question worth asking is *"when the player returns to a surface, is it hot?"* — and those two
diverge whenever a game contains legitimately cold content. The opening funnel is the largest such
block, and it is one the author is supposed to build well.

**Measured on night_desk**, same three explicit beats, two denominators:

<pre>
                                    3 explicit (today)   6 explicit (mislabelled beats fixed)
  over all 75 beats                     4.0%  FAIL            8.0%  pass, flagged BARE PASS
  over 50 repeatable beats              6.0%  FAIL           12.0%  clean pass
</pre>

**The same game reads "barely not empty" on one and "healthy" on the other.** The 25-beat opening is
the entire difference.

⚠️ **The companion gate does not cover this.** G3 `explicit in repeatable` computes
`rep_expl / len(expl)` (`gates.py:4287`) — *of the heat you wrote, how much is re-enterable.* The
missing measure is the inverse: **of your re-enterable surfaces, how much is hot.** That is the
question Vesper failed — nine repeatable sex loops at zero — and no gate asks it.

**✅ Option 1 applied, LO's call, 2026-08-31.** `gates.py` G2 now divides by repeatable beats and
prints the all-beats share beside it, unjudged. The two rejected options were exempting the starting
canvas from the denominator, and printing the dilution without acting on it.

**Verified by running the script before and after on all fifteen built games.** Thirteen verdicts
unchanged; **`steam` 7.6% → 7.2% and `the_allowance` 8.1% → 7.3% flip PASS → FAIL**, and both were
already flagged BARE PASS. `vesper` does not flip — it failed before and fails harder now. Full entry
in the skill's `CHANGELOG.md`.

⚠️ **The floor constant was not re-baselined**, so it is now lenient rather than strict. Recorded in
the gate's comment; it needs the reference game segmented by repeatability, which has never been
done.

**Would a correct skill have prevented this?** It would have prevented the wrong *response* to it —
which is the real risk here. An author who sees the floor drop after building a proper opening will
cut the opening, and that is the worst available move.

---

## 12 · A sheet can call a beat explicit and be wrong, and nothing checked

**What happened, 2026-08-31.** night_desk 0.0.1 reported 3 explicit beats and an explicit-floor score
in every summary it produced. Run against `gates.py`'s own word list (`gates.py:286`), those three
beats score **0, 0 and 1**. The release had **zero** countable explicit beats and had been reporting
a number for all of them.

**Why it happened.** `[explicit]` was a label an author put on a beat line, and the label was never
compared to the instrument. Two of the three beats *added* the same day made the identical mistake on
their first write — both leaned on `hard` and `wet`, and **neither word is on the list**, which is
anatomy and acts, not states.

**This is `defects/001` in a new place.** The commuter release declared a 1,400-word landing, shipped
112 words, and passed 46 gates. The fix for that was supposed to be a review artifact. **The review
artifact reproduced the defect** — a summary written by the session that wrote the content, reporting
intent as measurement.

**Change owed — three things, and the first is not optional:**

1. **Any sheet that claims an explicit beat must run the beat through the instrument.**
   `gates.py --beat <path>` already exists and is *"the only mode that measures prose not yet in a
   game"* (`SKILL.md`). It was never wired into the authoring loop. The number on the sheet must come
   from the script, not from the author.
2. **A `[label]` on a beat line is a promise and must be marked as one.** Where a sheet carries
   labels rather than prose, its explicit count is an *intent* figure and belongs on the intent side
   of the measured/intent split, never in the measured block.
3. **A per-NPC vocabulary ceiling built from words the gate does not count is unbuildable.**
   night_desk's decision 15 gives Del a tier-1 ceiling of *tits, ass, hard* — only two of the three
   count, so a tier-1 beat cannot clear the 3-word floor without repeating a word or exceeding its
   own ceiling. Wherever the skill teaches ceilings, it must say they are written from the counted
   list.

**Would a correct skill have prevented this?** Yes, and cheaply — the script already existed. This is
the strongest single argument in this file for the review loop being wired to the instrument rather
than to an author's judgement.
