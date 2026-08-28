# author-game-v2 — changelog

The skill-level ledger. Every edit to any file in this skill gets a dated bullet here in the
same turn: what changed, why, and how it was verified.

---

## 2026-08-28 — the register has no stopping point, and the skill had 419 words of example to steer by

**Why.** Six of nineteen posts on F95zone 312420 called `vesper`'s prose machine-made. Padding was
tested and refused earlier today. Broken English was tested and refused too: we run roughly **half
the field's malformed-word rate and a quarter of its duplicated-word rate**, and burstiness — the
most-cited machine-text signal — sits inside the field range. What survives measurement is a
register that has been swept in one direction with nothing telling anyone where to stop.

**⚠️ Read this before trusting any number in this entry: the study was wrong twice, and both
corrections are the useful part.**

1. **The basis.** Every figure first reported compared the field's **built HTML** against our
   **authored TOML**. A build carries labels, sidebar, quest cards and room lists — thousands of
   words with almost no modifiers — so the two do not compare. Redone with both sides read from
   `output/index.html`, 28 of ours against 25 of theirs. ⚠️ **This entry first claimed the gap was
   1.1x–2.4x; that figure was itself an artifact and is corrected below under G43.**
2. **The extraction.** A line-level pass over blockquotes reported "4,104 words of example prose
   across 11 files, every file off-field." A wrapped continuation line of an explanation does not
   begin with a warning marker and reads as narrative, so the count was mostly my own prose. At
   **block** level, whole-paragraph test: **419 words in 13 blocks.**

**⚠️ A headline was WITHDRAWN by correction 1.** Article density was reported as our largest and
most invisible habit — 101/1k against a field maximum of 86, "11 of 11 games outside". Read on one
basis we sit at **65.0 against a field median of 58.3**, inside the field's 33.3–86.0 with 3 of 28
builds above the maximum and 5 below the minimum — modestly above the middle, nowhere near outside. **There is no article finding.** It is recorded in `register.md` so it is
not re-proposed.

**What survived, on the matched basis.**

| per 1,000 words | field | ours | outside |
|---|---|---|---|
| `-ly` adverbs | 8.9 – 22.6 (p50 13.5) | 1.3 – 8.6 (p50 3.2) | **28 of 28 builds** |
| hedge words | 5.4 – 22.4 (p50 12.0) | 0.5 – 7.1 (p50 1.6) | **27 of 28 builds** |
| dashes /10k | 0 – 35.5 (p50 1.1) | 1.6 – 179.6 (p50 42.7) | 15 of 28 builds |

Every game this project has produced, under either skill, writes below the genre's floor on both
modifier markers. **`Sweeping backwards` says to replace the hedged clause with the specific one and
names no floor** — that is the cause, and it is a rule doing exactly what it says.

**What changed.**

- **`references/register.md` → `## How far is far enough`** — the stopping point the strip rule
  never had. Carries the table, the reader's own words for what it costs (*"impossible for the
  author to foreshadow or draw attention"*), the test that replaces a number (*read the beat and ask
  which sentence you were supposed to carry out of it*), a real over-stripped/weighted pair, the
  ⚠️ that this is **not** permission to pad, the seam warning, and the withdrawn article finding.
- **`references/register.md` → `## The model beats`** — four worked beats, one per kind in the
  file's own table: room card, reveal beat, talk screen, explicit repeatable. Correct as written,
  no before/after to un-learn.
- **`references/register.md` → `The examples are the register`** gains the **fourth instance**, and
  it is a different shape from the first three: those were things the skill *showed*, this is what
  it **failed to show**. 419 words of example against 185,575 words of instruction is 0.23%, so
  authors model the explanation — and with nothing anchoring them the games scatter, dash rates
  running **1.6 to 137 across builds from one skill**.
- **`references/the-first-hour.md`** — the worked cold open, 38 words, naming nobody, ending on a
  door.

**Verified.** The new example prose was measured before it shipped, which is the whole point of the
arc: **264 words, 0 dashes, `-ly` adverbs 18.9/1k and hedges 11.4/1k — both inside the field range**
(8.9–22.6 and 5.4–22.4) against our games' 0.9–5.4 and 0.4–4.0. `--selfcheck` green both directions,
44/44 and 27/27. **0 verdicts moved across all 22 scorable games**, which is trivially guaranteed:
`gates.py` has a zero-line diff. No game touched.

**Not done, and named rather than quietly skipped.**

- **No gate, no reporting, no constant.** A draft added article and adverb rates under G43 quoted
  against the field. It was **written, tested and reverted** when the basis test showed no marker
  survives the change of basis — quoting a field figure beside a TOML-derived rate is the seam error
  the gate's own header exists to warn about. There is no per-beat field number to write down,
  because the corpus exists only as built pages.
- **`back_home` FAILS G43 at 79.4/10k** — 284 dashes in 35,755 words, more than double the ceiling.
  Recorded as a number that has to come down. LO's call: name it, do not fix it.
- **⚠️ G43's calibration was investigated and NO DEFECT WAS FOUND — the alarm was mine.** This entry
  first reported that the gate reads authored TOML against a ceiling derived from the field's built
  HTML, and that the same measurement moves **1.11x to 2.43x** where `gates.py:6084` claims 7%. That
  spread was an artifact of the study script, not of the gate: its tag-stripping pattern was bounded
  at `<[^>]{1,200}>`, and this engine emits inline-styled `<img>` tags longer than 200 characters, so
  CSS tokens were counted as words on our side only — the field's short `[img[...]]` markup was
  unaffected, so only our rates were deflated. Unbounded, across six games, the move is **0.68x to
  1.27x**. The dash rate does survive the change of basis, which is exactly what the gate claims.
  `DASH_CEILING` stands and no line of `gates.py` was changed.

Scripts, data and both superseded measurements: `~/Documents/Prose_Machine_Sound_Study_20260828/`
and `~/Documents/Prose_Padding_Study_20260828/`.

---

## 2026-08-28 — padding measured and REFUSED: our prose is not fat, it is stripped, and 13 of 14 games sit below the field's floor

**Why.** Players on F95zone thread 312420 read `vesper` v0.2.0 and said the prose reads as
machine-written. The most-argued post says why: it is long but *"FAILS to communicate"*, it is
skimmed rather than read, and the cause named is padding — *"turn the one line you wrote into a
couple of paragraphs with an LLM."* Nothing in this file measures that. G19 measures sentence
LENGTH, which our games pass at the field median; G43 measures the dash rate, one habit. A
wordiness gate looked overdue, and was proposed to LO in exactly those terms.

**It was measured first, and the hypothesis is dead.** Five markers, each a rate per 1,000 words
because the G43 arc proved anything per-sentence does not survive the HTML/TOML seam. 25 field
games against our 14.

| marker | field range (p50) | ours p50 | our games outside the field |
|---|---|---|---|
| `-ly` adverbs | 8.87 – 22.57 (13.43) | **4.22** | **13 of 14 BELOW the field minimum**, 0 above |
| hedge words | 5.39 – 22.42 (11.99) | **2.96** | **10 of 14 BELOW the minimum**, 0 above |
| commas | 17.23 – 153.30 (50.97) | 44.50 | none outside |
| repeated trigrams | 155.49 – 649.74 (299.39) | 167.76 | 6 below, 0 above |
| vocabulary variety | 0.48 – 0.69 (0.59) | 0.56 | none outside |

`vesper` — the game those readers were reading — writes **3.01** adverbs and **4.00** hedges per
1,000 words against field floors of 8.87 and 5.39, and repeats phrasing **less** than the field
(210.71 against a p50 of 299.39). Its commas are field-normal, its sentences field-median length.
By every marker of padding it is **cleaner** than the games it competes with.

**⚠️ Round one of the measurement was contaminated, and the correction ran AGAINST the conclusion.**
The first pass leaked `degrees-of-lewdity`'s JavaScript block comments and `friends-of-mine`'s
`[img[...]]` markup into the field text. Both add non-prose WORDS, which dilutes a per-word rate
and pushes the FIELD figure DOWN — that is, it flattered the result. Cleaned before anything was
recorded: the field's adverb floor rose 6.16 → **8.87**, and `love-and-vice` fell from 23,687
words to 9,110, being 60% script. The finding survived the correction and got stronger.

**⚠️ NO GATE WAS BUILT, and that is the finding.** A padding ceiling set anywhere in the field's
range passes all fourteen of our games forever. That is the fourth check this skill has measured
and turned down — after R4, study 6's anchoring check and P0 — and the reason is the same each
time: a gate that cannot fail looks like coverage and is not.

**What the numbers do point at.** Set beside G43, the one marker where we are off-field on the
HIGH side: `vesper` writes **118.3 dashes per 10,000 words** where the corpus maximum is 35.41 and
the median is 0.99. Dash-joined, modifier-light, sentences at the field median. **That is a
texture, not a volume**, and it is a better fit for what those readers actually described than
padding is. It is also already measured and already failing, so no new instrument is needed to act
on it.

**⚠️ One claim checked and withdrawn before it was written down.** The leanness was about to be
blamed on `CLAUDE.md`'s filler ban leaking from chat into prose. That file scopes itself explicitly
— caveman governs chat and *"has never governed a beat"* — so the claim is false. What is true and
citable is that this file already prescribes the direction: `register.md:122`, *"Replacing the
hedged clause with the specific one."* Whether that was meant to put 13 of 14 games below the
field's floor is stated nowhere, and **no rule in this skill names a floor for either marker**. No
reader in the thread named modifiers either. So the numbers are recorded and nothing is prescribed.

**What changed.**

- **`references/register.md`, "What is not measured here"** — records that padding was measured on
  five markers and there is nothing to gate, with the direction, the counts, and the pointer to the
  study. It sits in the one section that already tells an author what the instrument cannot see.
- **`DOCTRINE_GAPS.md`** — a Log row. No inventory item: nothing is broken and nothing is owed.

**Verified.** `gates.py --selfcheck` green in both directions, 44/44. `mrs_vance` **43/43, 1 n/a**.
No gate, lint, threshold or constant touched, so no verdict can have moved. No game touched; the
skill's only new content is prose. Scripts, data and method:
`~/Documents/Prose_Padding_Study_20260828/` — `measure.py` reproduces the table, and the
contaminated first pass is kept beside it so the correction is inspectable.

---

## 2026-08-28 — a gate was deleted and seven surfaces went on teaching it, including both templates

**Why.** LO asked for an audit of everything the recent arcs shipped — *"go one by one confirm and
verify each and everything"* — and then said to fix what it found. It ran the checks rather than
reading the changelog: `--selfcheck`, `--release` on real builds, `gates.py mrs_vance`, `grep -n`
on every engine citation, `tomllib` on the templates.

**What passed, verified running and left alone.** Study 7 (`templates/want.md` §1, `the-want.md:22`,
`state.md:43-51`, the gate printing `3 start-choice flag(s) … read 5x` on `mrs_vance`) · E1 (R3b
`:254`, R3c `:312`, `week_income` and `obligation_moves` in `state.md`, both lints firing) · Study 8
(R1b, R1c, the pool note, the gate green on `mrs_vance` at `truck_bought (2600) opens 5` and **red on
`the_season` at `has_boots (20) opens 0`**, exactly as recorded) · `--release` (vesper 5/6 with the
archive note unjudged; `the_inheritance` **115 missing, `--dev --debug`, filed as published**, which
confirms the number SKILL.md quotes) · `engine.md` §38's `template_import.py` citations, exact.

**The finding, and it is one cause wearing five faces:** *a check changed and the places that
describe it did not.* `--selfcheck`, shipped the day before, is **one-directional** — script →
SKILL.md — so it is blind to a stale row, a row pointing at the wrong section, a reference file's own
checks table, and every template.

### 1 · G35 was deleted on 2026-08-26 and seven surfaces still taught it

`the anchor introduces itself` required a first-visit canvas at the anchor. It is **1 of 26 field
games** (DoL, 258 branches; **eighteen have none**), and it *"sent one author to write nine arrivals
that were reverted the next day"* — `gates.py:6233`. The instrument was cleaned up properly:
`lint_place_function` only **reports** a first visit and never asks for one. The doctrine was
rewritten to say the opposite: `the-first-hour.md:536`, *"The first-visit canvas is a MINORITY
device — do not reach for it first."* Everything else kept teaching the retired device.

```
templates/board.toml:249       THE ROOT. description = "<what she sees; what it smells of; who
                               is usually here>" — sensory scene-set, never the FUNCTION, which
                               IS the measured failure. Rewritten function-first. Neither
                               the-board.md nor the-map.md teaches this, so that placeholder was
                               the only prescription an author ever saw.
templates/first-hour.toml      section C rewritten: the description is the surface; the canvas is
                               demoted to the minority case, with the 1-of-26 count, the deleted
                               gate, and the reverted arrivals. Its paragraph placeholder said
                               "what kind of place this is" — that belongs in the description now,
                               so the block asks for the thing that is true ONCE.
SKILL.md                       the gate row deleted; `named before met` no longer claims a places
                               half; `the place says what it is` given its own description.
references/the-map.md          R4's tail prescribed the canvas and cited "the gate that checks it".
references/the-first-hour.md   contents line :38 and the cheat-sheet bullet still carried the old
                               title against a section heading that changed at :500.
scripts/gates.py               `named before met`'s docstring still described a PLACES half the
                               function has not had since 2026-08-26.
DOCTRINE_GAPS.md               item 6 listed the deleted gate among what closed onboarding.
```

⚠️ **This is the "a template is copied harder than a reference" rule catching us with our own
hands.** SKILL.md has carried that operating rule since 2026-08-24; `templates/board.toml:249` is a
fourth instance of it, and the worst kind, because the placeholder was not a bad example — it was a
*correct-sounding* one that asked for everything except the thing F9 exists to get.

### 2 · A row shipped the previous day pointed at the wrong section

`the wardrobe is read` → `engine.md` **§23**, which is the guidance page. The wardrobe is **§17**
(`:473`, gate named at `:515`). Mine, from the index arc, and logged rather than quietly patched.

### 3 · `the-economy.md`'s own "What is checked" table was missing three of its checks

Gate `what money buys opens a door` (R1b names it at `:116`; the table did not) · lint `what a paid
repeatable leaves behind` (R1c said *"This is a lint"* and never named it — it does now) · lint
`money gates content, or only prices it`, which appeared **nowhere** in the file that owns money.
E1's entry says *"the checks table gains the ratio lint"*, so the table is maintained by convention;
Study 8 skipped it and nothing noticed.

### 4 · Three engine citations were off, in four files each

| written | actual | what is really on the written line |
|---|---|---|
| `v2.py:216` | **217** | a blank line |
| `v2.py:12403` | **12404** | the docstring's closing `"""` |
| `v2.py:14903` | **14906** | a dict key, `'category'` |

Fixed in `the-release.md`, `gates.py`, and **in this file and `DOCTRINE_GAPS.md` too**: a `file:line`
is a pointer, not a claim about history, and the record of the correction is this entry. `:14753`,
`:1077`, `:1081-1082`, `:10332` were exact and were left. So was `template_import.py:1696-1697` /
`:6391-6392`. ⚠️ **A fourth was found by the verification step, in the block being rewritten** —
`templates/first-hour.toml` cited `v2.py:4453` for auto-fire; the function is
`setup.selectAutoFireCanvasForLocation` at **`:4459`**.

### 5 · `engine.md` §38's two ranges under-reached

*"joined with ` · `"* cited `16131-16133`; the join is at **16134**. *"called from `StoryCaption`"*
cited `16138-16141` and `16139-16141`; the widget is composed at `16139-16142` and the two
unconditional calls are at **`:16162` and `:16177`** — neither range contained a call site. Split
into three rows so each claim sits on the lines that show it.

### 6 · `--selfcheck` gains the reverse direction

Documenting five gates fixed the last stale index; this one was a two-day-old **deletion** nobody
propagated, and no check compared the table to the script in that direction. Every gate name in
SKILL.md's scoreboard table must still be emitted.

⚠️ **It invents no threshold and it was proved exact before it was written** — scoped to the one
table whose header row is `| gate |`, it read **45 documented against 44 emitted and named exactly
the one stale row**, zero noise in either direction. The unscoped version reads 8 false names off
SKILL.md's other tables; `_documented_gate_names` carries that measurement in its docstring, because
it is the whole reason for the scoping.

⚠️ **Lints are checked one way only.** They live in a wrapped prose paragraph with no exact
extraction; gates have a table. A reverse check on prose would fire on how a sentence was broken, and
a check that fires wrongly is what took R4, study 6's anchoring check and P0 back out.

**Verified.** `--selfcheck` **red before green on the new direction** — `44/45 still checked ·
documented but NOT emitted: the anchor introduces itself`, exit 1 → `44/44` both ways, exit 0. A
check whose first run is green has not been tested. **0 verdicts and 0 tallies moved across all 22
scorable games**, compared as verdict lists; three games differ only on the known nondeterministic
room named by `sinks >= sources`, `[PASS]` and identical counts on both sides. `ast.parse` clean;
`mrs_vance` **43/43, 1 n/a**. **All 20 engine citations touched re-read off the live source**, zero
failures. `templates/board.toml` still fails to parse on the identical statement at the identical
line (`<tier_1> = 0`, :94 — the edit is below it); `templates/first-hour.toml` **does** parse, before
and after. No game touched, nothing rebuilt.

**Not done, and named rather than quietly skipped.** Nine of the 44 gate names appear in no reference
file. Most are argued there under other wording — `meter ceiling` as *"the top of a bar buys
something"* — so a "every gate must be named in a reference" check would fail correct work, which is
the error this skill keeps taking rules back out for. The one with no home at all is `prose texture`:
`register.md:542` argues it thoroughly and calls it *"Gate 43"*, a number the scoreboard never
prints. Left as an observation.

---

## 2026-08-28 — the index reopened twelve days after it was closed, and now something watches it

**Why.** LO asked whether anything was left on the skill side of the recent arcs. Two things were,
and checking turned up a third that matters more than either.

⚠️ **A correction to what was reported in chat before this was measured.** I said **three** lints were
missing from `SKILL.md`. Against the 27 lint headlines the script prints it is **eight**, and five of
those predate the recent arcs. Same shape on the gates: I named the two new ones; **five** were
absent. The job was bigger than I described it, in the same direction.

**The finding underneath both.** `SKILL.md:177` is the index an author reads when a gate fails, and
it says so in its own words — *"When a gate fails, look it up here. Nine of these used to be
documented nowhere but in the script's own comments, so an author who hit one had nothing to read."*
The **2026-08-16 whole-skill audit closed exactly that** (*"nine gates were documented in zero
reference files, now indexed in `SKILL.md` (23/23 findable)"*). **It reopened within twelve days.**
Measured: the script emits **44 gates and 27 lint headlines**; the index carried 39 and 19, and named
**none of the three alternate modes**. Nothing anywhere would have said so.

**Shipped.**

- **`SKILL.md`** — the index brought to **44/44 gates, 27/27 lints, 3/3 modes**. Five gate rows added
  with the doctrine home for each verified rather than assumed (`the wardrobe is read` →
  `the-meters.md:195`; `a locked door says why` → `the-surfaces.md:597`; `prose texture` →
  `register.md:778`, `DASH_CEILING = 35.0`; `the start choice is read` → `the-want.md:121`;
  `what money buys opens a door` → `the-economy.md:116`), eight lints added to the paragraph below the
  table, and a modes table beside the **"Gates before ship"** operating rule — which until now named
  the only command that *cannot* see a build.
- **`scripts/gates.py`** — **`--selfcheck`**: every gate name and lint headline the script emits must
  be findable in `SKILL.md`. No game needed, exits non-zero on a gap. ⚠️ It **invents no threshold**,
  which is why it is safe where R4, study 6's anchoring check and P0 were not — it is a set difference
  over strings, and the names are read out of the script's own source. Proved exact before it was
  written: a static regex recovers **44 of 44** gate names with nothing extra in either direction,
  checked against `--json`. ⚠️ The haystack is **whitespace-collapsed**, because `SKILL.md` is wrapped
  prose and a lint named across a line break IS documented — without that the check sends the author
  to reflow a paragraph instead of writing the row that is actually missing. ⚠️ **Comparison is
  substring against the whole file, never cell-equality:** the index legitimately packs several gate
  names into one cell (`guidance exists · no chain ends in silence`), and a cell-wise diff reported
  fourteen false gaps on the first attempt.
- **`references/engine.md` §38** — `[project] version` / `release_date`, the sidebar footer.
  ⚠️ **Yesterday's `the-release.md` began requiring this field, and a grep of the entire skill —
  references, templates, scripts — returned ZERO mentions of it outside those two new lines.** The
  doctrine was asking for something the skill had never taught. Traced end to end:
  `template_import.py:1696-1697` → `:6391-6392` → `v2.py:16131-16133` → the `versionFooter` widget
  (`:16138-16141`), which is **always defined and renders nothing when both keys are empty** because
  SugarCube throws on an undefined widget call.
- **`templates/board.toml`** — `version` and `release_date` in `[project]`, with the file's own
  ⚠️-comment style, saying what the player sees and why it must match the portal entry.
- **`references/the-release.md`** — step 4 and the three-places table now point at §38 instead of
  naming a bare field.

⚠️ **A verification step in the plan was itself wrong, and is corrected here rather than dropped.**
It said to confirm `templates/board.toml` still parses as TOML. **It never has**, and cannot: it is a
fill-in-the-blanks skeleton whose placeholders (`<tier_1> = 0`) are invalid TOML by design. The real
check is that the edit does not make it worse — the parse fails on the **same statement**, shifted by
exactly the ten lines inserted (line 84 → 94, both `<tier_1> = 0`).

**Verified.** `--selfcheck` **went red before it went green** — 16 names on the first run (5 gates,
8 lints, 3 modes), 0 after; a check whose first run is green has not been tested. Ordinary runs
untouched: **0 verdicts and 0 tallies moved across all 22 scorable games**, compared as verdict lists
rather than totals. Five games differ on the two known nondeterministic headline lines (`also ranked:`
tie ordering, the room named by `sinks >= sources`) — it was six games last session on unchanged code,
which is the proof it is inherent. `ast.parse` clean. `mrs_vance` stays **43/43, 1 n/a**. No game
touched.

## 2026-08-28 — the release boundary: the rule was right, and nothing in the repo was holding it

**Why.** `games/mrs_vance/REVIEW.md` **B2** (MED, layer SKILL + TOOLING). LO's rule — *dev mode and
missing media block **release**, not testing* — is correct, and it existed **only as a comment on a
JavaScript object literal** (`games-data.js:44-49`), restated by hand in **nine of twenty-eight
portal entries in three different wordings**. Nine hand-copies in three wordings is the signature of
doctrine living in a file no tool reads. Measured before touching anything: **`gates.py` had zero
lines that read a built game** (its only knowledge of dev mode was a TOML trigger marker,
`:2621-2627`), and **`the-release.md` — 164 lines, 8 headings, named for this — never mentioned
`--dev`, `--debug`, a placeholder or a build.** The whole 42-check instrument is aimed at
`7_final_game.toml` and is structurally incapable of judging an artefact. A release is the one
moment the artefact, not the source, is the thing being judged.

**The drift was already shipped.** Parsing the flags-init map and `MissingMediaPage` out of all
**29 built games**:

| game | portal | `debug_mode` | `dev_mode_enabled` | missing at build |
|---|---|---|---|---|
| `the_inheritance` | *main grid, no `dev`, no `version`* | **true** | **true** | **115** |
| `the_long_summer` | *main grid* | **true** | — | **122** |
| `forty_miles` | `version: "0.1"` **and** `dev: true` | **true** | **true** | **78** |
| `under_one_roof` | *main grid* | false | — | **183** |
| `vesper` | `version: "0.2.0"` | false | — | 48 |
| `two_weeks`, `new_in_town` | *main grid* | false | — | 0 |

**`the_inheritance` sits in the published grid carrying a full `--dev --debug` build** — a sharper
instance than the one B2 names, and nothing could have reported it. And the version triangle was
stale where it existed at all: `forty_miles` reads portal `0.1` / `[project] 0.1.2` / archives
`{0.1, 0.1.1, 0.1.2}` — **the portal two releases behind the number printed in the player's face.**
`vesper` was the only game where all three agreed.

⚠️ **A CORRECTION TO B2'S OWN FIX, shipped with the claim rather than dropped.** B2 specified failing
on *"an `[IMAGE MISSING]` or `[VIDEO POOL MISSING]` marker"* in the built HTML. **Those markers are
`--debug`-only** — `v2.py:12404` (`if not self.debug: return ''`), `:14753`, `:14906` — so a clean
build renders **silent gaps** and the grep passes it. It would have passed `under_one_roof` with
**183 missing files**: the proposed instrument measures the presence of *scaffolding*, not the
absence of *media*. Two instruments survive a clean build and are read instead — the build's own
flags-init map (`v2.py:1077`, `:1081-1082`), which is its record of the flags it was made with, and
`MissingMediaPage`, which `v2.py:217` documents as *"always generated, but button only shows in
debug mode"*.

**Shipped.**

- **`references/the-release.md`** — new `## § Shipping the build`. The six steps **lifted from
  `games-data.js:44-49`, not invented** (the procedure was already correct, only in the wrong file),
  the three-places-that-say-what-shipped table, and the rule the schema never stated and therefore
  could not adjudicate: **`dev: true` and `version` are mutually exclusive.** Written as a command,
  not a checklist, with §3a's warning restated — v1's thirteen-point pre-ship audit was followed by
  the exact bug it was written to prevent.
- **`scripts/gates.py`** — `--release <slug>`, dispatched at the top of `main()` and short-circuiting
  exactly like the existing `--words` mode. Six checks: a build exists · built without `--debug` ·
  built without `--dev` · no missing media · not filed under `dev: true` · the version agrees across
  portal, `[project]` and archive. **Off for every ordinary run**, and it **exits non-zero**, which
  `words_mode` deliberately never does — a release is the one moment something can reach a player.
- **`DOCTRINE_GAPS.md`** — inventory item **16 · the release boundary** and a Log row; and
  **`games/mrs_vance/REVIEW.md`** B2 closed with the corrected instrument recorded in the section
  itself rather than silently dropped (**6 open / 18 fixed → 5 open / 19 fixed**; **B1 stays OPEN**,
  it is the rebuild and it needs media harvested first).

⚠️ **Two things deliberately NOT gated, each with the measurement that stopped it.**
**Byte-equality of `output/index.html` against `releases/v<version>.html`**: vesper's differ
(`bfd9f9bd…` vs `b038eb4c…`) and vesper is the one game whose version triangle is whole — a gate
there would fail the only correct case, which is how R4, study 6's anchoring check and P0 each ended.
It prints as a note and judges nothing. And **no repo-wide sweep**: `--release` is pointed at the
game you are about to ship, because nine legacy main-grid entries carry no `version` and failing all
nine on day one turns a release gate into noise.

⚠️ **The media count is a build-time snapshot** — files added to disk after a build are not in it.
That is correct for a gate that judges what *ships*, and it means the fix for a red is a **rebuild,
never a file copy**. Said in the docstring, in the doctrine and in the check's own output.

**Baseline, recorded as the number that has to come down: 0 of 29 builds are clean.** Best in the
repo is 5/6 — `vesper`, `two_weeks`, `new_in_town`.

**Verified.** Every branch exercised on real work rather than asserted: the debug/dev/media reds on
`the_inheritance` and `forty_miles`, the stale-triangle red on `forty_miles`, the whole-triangle PASS
on `vesper`, and the five-of-six clean-flag path on `two_weeks` / `new_in_town`. The branches no
shipped game reaches — `dev: true` **and** `version` on one entry, no build at all, a slug absent
from the portal, and `games-data.js` absent (which reports **n/a**, not a pass) — driven on a fixture
root. **Ordinary runs are untouched: 0 verdicts moved and 0 tallies moved across all 22 scorable
games**, diffed per-gate against the pre-edit file, not by comparing totals. ⚠️ Six games differ
run-to-run on two headline lines (`also ranked:` ordering and the room named by `sinks >= sources`) —
**proved inherent by running the identical file twice and getting the same wobble**, not caused by
this change; the `sinks >= sources` nondeterminism was already logged during P0 and is still open.
`ast.parse` clean. **`mrs_vance` stays 43/43, 1 n/a.** No game was rebuilt or modified.

## 2026-08-28 — what she owns: the biggest thing the field is loved for, and it costs us almost nothing

**Why.** Study 7 closed the minute-zero slice of `freedom` — the field's largest bucket at **25.9%**
of top-30 engagement against `premise` at **0 of 30**. Reading the four games in that bucket showed
the slice was small: *"you can be whoever you want"*, *career/path variety*, *zero-to-hero
money/career*, *choice-consequence ownership* — **not one of them is an opening question.** So a
study was run on the ongoing half (`~/Documents/Accumulation_Study_20260828/`, 25 corpus games,
~55,000 passages).

⚠️ **This is an ADOPTION, not a discovery, and that is the uncomfortable part.** The 2026-07-24 field
report already ranked this defect of ours at **#3 of eight** — *"No meta-loop of accumulation…
nothing in Vesper visibly compounds — money is rent-pressure, not a snowball; no owned asset grows.
This is the deepest structural difference"* — plus **#4 repetition doesn't pay** and **#6 the world
never pushes back.** Thirty-five days, and not one of the three was ever carried into
`DOCTRINE_GAPS.md`'s inventory. A grep of the whole skill before this: `meta-loop` 0 hits,
`owned asset` 0, `snowball` 0, `closes a door` 0, `irreversible` 0.

**What was measured.** Selection structural, never lexical, then hand-read in the passage — the
parent study's `$slaverent` error is why both halves of that sentence are there.

- **Nine of 25 corpus games sell the player a THING, and all four of the most-engaged sandboxes do.**
  `become-someone`'s company (`$startup.level` 1→4, 20k/50k/100k) gates **114** condition sites;
  `become-taxi-driver`'s `$car.body` **46**; `destroyer`'s five bedroom levels 21/20/16/16/16.
- **The discriminator is structural**, which is what makes any of this checkable: an owned thing has
  FEW write sites and MANY read sites; a meter has many of both.
- **One asset closes three of the report's eight critiques.** become-someone's company accumulates
  (#3), is what the work deposits into (#4), and missing its weekly payroll calls `<<Bankruptcy>>`
  and takes it away — recoverable for **$500** (#6).
- **It costs no new surfaces.** `destroyer`, rank 2: buying the bedroom takes its random pool from
  `[1,2,3]` to `[3,4,5,6,7,8,9]`. Same room, same link, no branch — and scene 3 is in both, so
  nothing is removed. **A `[group]` with `conditions` wrapping a `block_pool` is already live in
  `mrs_vance`** at `loop_cade.finish` and `loop_sherrod.finish`, 5 instances; consecutive groups
  become one chain at `v2.py:14634-14640`. No engine work.
- **The field also states its prices.** *"You need $50,000 and at least two employees in order to
  upgrade the office"* / *"Your office is fully upgraded!"* — the-voice.md's rule executed by the
  field's #4 game on an asset gate. And `become-taxi-driver`'s five-term gate names **every** unmet
  term with directions.
- **Our side:** money bought **exactly one** thing that opened anything across eight games —
  `mrs_vance`'s truck, 5 doors, shipped 2026-08-27 out of the economy pass as a sink with no doctrine
  behind it. **Five of the eight sell nothing at all.**

⚠️ **The expensive form of `freedom` is refused, on the corpus's own evidence.** More branches is the
obvious reading and it is wrong: **College Daze**, 2,248 engagement, researched then *excluded* —
*"branch explosion collapsed its cadence"*, ~1 year stale. *"The freedom players loved is what a
sandbox delivers via reusable state-gated systems instead."*

⚠️ **A contradiction inside our own file, scoped rather than deleted.** `the-want.md` said ADDITIVE
ONLY — *no door closes*. That is a **save-safety** rule for retrofitting, and read as design law it
inverts the field: `the-company`'s single most-liked reason for love is choice-consequence ownership
(*"it only does that if you allow it to"*, 39 likes) on a **hard route-lock**, and its single most
avoidable complaint is that the lock is silent — *"If a choice locks you into a sub route, tell me
that."* The rule is not *don't close doors*; it is **close them out loud.**

**Changed.**

```
references/the-economy.md   +R1b  what money buys has to STAY bought — the field table, the three
                                  shapes (level ladder / instalment build / one-off possession),
                                  the compound gate, the second-axis rule, the stated price, and
                                  upkeep as optional-but-load-bearing
                            +R1c  a repeatable she PAYS for deposits something
references/the-surfaces.md  R6    the pool itself can be a function of state — destroyer's
                                  [1,2,3] -> [3,4,5,6,7,8,9], why scene 3 is in both, and an
                                  explicit note that this is NOT gated because we have not built it
references/the-want.md      §1    ADDITIVE ONLY scoped to retrofitting; the design rule beside it
scripts/gates.py            +gate  `what money buys opens a door`
                            +lint  `what a paid repeatable leaves behind`
DOCTRINE_GAPS.md            Study 8 + inventory item 15 + Log row
```

**The gate ships as weak as G44 and for the same reason.** It **fails only on ZERO**: a flag bought
with the currency, surviving the night, read nowhere. A game that sells nothing reports `n/a`, *which
is not a pass*. Everything else prints its door counts **unjudged** — `mrs_vance`'s truck at 5 doors
is one house with one asset, not a distribution, and a floor invented at n = 1 is how this skill lost
its meter doctrine (`the-meters.md` W1).

⚠️ **Day caps are carved out, not failed.** A flag `[engine.daily_tick]` wipes overnight is a day
cap, and `off_season` prices four of them in coins perfectly legitimately — the same exclusion
`_holder_day_capped` already makes for gate 18.

⚠️ **The FAIL branch was found in shipped work rather than constructed.** `the_season` sells boots
that fit for **$20** (`has_boots`) and fuel for **$5** (`truck_fuelled`) and reads **neither flag
anywhere**. The player pays and the game never refers to it again — Study 7's fake-freedom defect
with a price on it. Its scoreboard moves 39/41 → **39/42** and that red is correct. Not fixed here:
it is another game and that is LO's call.

**The lint is a RATE and never a score**, and the report's own phrasing had to be narrowed to ship.
Critique #4 said *"every repeatable should deposit into something"*; counted that way, 67% of our
repeatable surfaces grant nothing — but that sweeps in ambient prose that fires for free and is
*supposed* to grant nothing. Shipping the sentence as written would have failed correct work, the
error that withdrew R4 and demoted study 6's anchoring check. Narrowed to choices the player pays
for: **51.7% across the eight**, `forty_miles` **10 of 10** deposit nothing, `mrs_vance` 1 of 47.
**A pure sink is not a defect; a game made only of pure sinks is.** Fourth distribution this file has
printed instead of inventing a floor.

**Not built, deliberately.** No check on the pool-widening pattern — no v2 game does it yet, and *a
rule specified before its doctrine has a real game to run against will fail correct work*. No
`board.holdings` ledger field — the gate reads the asset out of the TOML, and a field with no use
would have produced eight new "not declared" reports and told no one anything.

**Verified.**

```
mrs_vance      42/42 -> 43/43 judged, 1 n/a      truck_bought (2600) opens 5   PASS
off_season     39/41 -> 40/42 judged, 2 n/a      meter_fed_once (3) opens 1    PASS
the_season     39/41 -> 39/42 judged, 2 n/a      has_boots / truck_fuelled     FAIL  (correct)
forty_miles, seventh_day, steam, the_allowance, the_inheritance, vesper,
last_call, late_shifts                                                          n/a
```

**Every one of the 12 scorable games gained exactly one row and no pre-existing verdict moved** —
checked by diffing the full per-gate list against `git show HEAD:…/gates.py`, not by comparing
totals.

## 2026-08-27 — the obligation learns to MOVE, and money is asked whether it opens anything

**Why.** `REVIEW.md` E1 asked one question — Mrs. Vance's week earns roughly four times her 260
rent, should 260 go up? A research pass over 19 field games and our own ten
(`~/Documents/Economy_Pressure_Study_20260827/`) answered **no, and the number was never the
mechanism.** Three measurements:

- **Their money buys content; ours buys meter points.** Seven corpus games sell a person, a scene or
  an unlock — `degrees-of-lewdity`'s Robin (taking on his debt DOUBLES her rent and buys a love
  interest), `patriarch`'s Lilith behind Villa Garcia, `corpo-life`'s marriage behind a 1M apartment.
  Mrs. Vance's five purchases bought `clean +45`, `standing +4/+5/+6`, `trust +3/+4` at $2–$26
  against $208 a day, and **zero of its 55 trait conditions read `money`.** Seven of our ten
  rent-enabled games are the same; four price nothing in money at all.
- **A constant obligation is soft at any value.** Eight of our ten clear the whole week in under one
  day of the best job, median 0.48 days. Every field economy that stays live moves the number.
- **Squeezing harder is the corpus's most-punished move.** The two games that made money bite are
  the two whose players are angriest, one dev walking it back in-thread. The decisive complaint is
  four words: *"here u still grind for nothing."*

**⚠️ AND THE RULE THIS FILE ALREADY CARRIED DID NOT SURVIVE CONTACT WITH AN AUTHOR.**
`the-economy.md` R3 has said *"price it against the income channels in both directions"*, with a
warning emoji, since the file existed. **Nine of ten games did not do it.** The one that did
(`forty_miles`, 245 against ~350) wrote the sum **in a prose comment in its spec**, because the
ledger had no field for it. An instruction with no field is a wish — so R3 now has one.

**Changed.**

- **`references/the-economy.md`** — R3 gains the measured note that the rule was ignored nine times
  out of ten. Two new rules:
  - **R3b · an obligation that does not MOVE is soft at any value**, with the three field shapes and
    which collector each needs: *imposed ratchet* (DoL's `[10000…200000]` pennies, £100 → £2,000 over
    seven payments × a player-facing 10–300% slider × Robin's doubling × a per-child surcharge;
    `course-of-temptation`'s mother), *cost follows holdings* (`sluttown-usa`'s
    `$serverRent = $runningServers * 50`), *the tier you chose* (`corpo-life`'s 200/800/10,000/30,000
    where **owning sets rent to 0**). ⚠️ Records that **nothing in DoL is gated on `$rentstage`** —
    it is read in five places and none of them is content — so a bare ratchet buys the player
    nothing and works only because the rise is delivered in a believed predator's mouth at the
    moment of payment. Where the money is already owed to the household, that shape reads as the
    author turning a dial.
  - **R3c · if the demand rises, the income has to rise with it**, or the ratchet IS
    "grind for nothing". `course-of-temptation` denominates its payouts in the debt
    (`Math.floor($weeklydebt * 0.15)`); our engine has no computed effect values, so the same thing
    is done with a band on an existing rung.
  - The board block gains **`week_income`** and **`obligation_moves`**, and the checks table gains
    the ratio lint.
- **`references/state.md`** — the same two keys in the schema, with why each exists.
- **`scripts/gates.py`** — two LINTS, no new gate and no threshold:
  - **`money gates content, or only prices it`** splits gate 16's two channels. Gate 16 passes on
    either and that stays right — the price channel was added 2026-08-14 to fix a real false
    negative — but *money opens a door* and *money buys a thing* are different claims and the gate
    cannot tell them apart. Run across our games it prints `⚠ NOTHING is gated on money` for
    `forty_miles`, `the_season` and five others.
  - **`the obligation against the week`** prints `obligation_amount / week_income`. An undeclared
    week reports **NOT DECLARED, which is not a pass** — the same wording the climb and start-choice
    gates use, because an absence is not evidence. A declared `obligation_moves` suppresses the
    low-ratio note, because `week_income` is the BASELINE week by construction and nagging a game
    whose obligation grows would be the check failing a game for obeying the doctrine.

**⚠️ Why neither is a gate.** `forty_miles` sits at 70% and `back_home` at 25%; any threshold between
them fails a game for doing the right thing. That is the error that demoted study 6's anchoring check
(2026-08-15) and got P0 refused (2026-08-27), and it is the third time this skill has chosen to print
a distribution instead of inventing a floor at n≈10.

**Built first, taught second — again.** All of this ran in `mrs_vance` before a word of it was
written here: an aspirational sink (a 2,600 flatbed she legally cannot own, so it goes in her
brother's name), an upkeep that follows it (`-22/day` on `[engine.daily_tick]`), a haul that pays 125
instead of 34 once the truck is hers, and `cade_covered` — the eviction flag that was **set by the
engine and read by nothing**, two hits in the whole merged game — turned into a band, a rung, and an
ask she can make before Friday.

**⚠️ No engine change, and the staged-rent feature was deliberately NOT built.** `[engine.daily_tick]`
already takes `traitEffects` with a per-effect condition gate (`template_import.py:706`), applied
through `setup.applyAndNotifyTrait` (`v2.py:5586`) — so a daily upkeep **notifies** rather than
draining silently, which is the device `sluttown-usa` is hated for. A DoL-style stage array would
also have made two surfaces lie, since `_traitMax` is static (`v2.py:16702`): a `trait_bar max` set
to the rent, and any quest goal naming it. A daily upkeep leaves Friday at 260 and both stay true.

**Verified.** `mrs_vance` **42/42 judged, 1 n/a** — no pre-existing verdict moved; money conditions
**0 → 5**; `cade_covered` hits 2 → 10 with four of them real. All 22 scorable games re-scored, no
gate count changed anywhere (only lints were added), and the lint's three paths — declared,
undeclared, no-obligation — each exercised on a real game. Live in headless Chromium
(`games/mrs_vance/playtest_economy.py`, new): **14/14** — four bands render exactly one arm each,
every new rung is clickable only in its own state, the upkeep takes 22 on `advanceDay()` with the
truck and 0 without. Existing harnesses still green: quests 23/23, standing PASS, presence 10/10,
walk-ins PASS.

**⚠️ One research finding withdrawn in the same pass.** `FINDINGS.md` §2 listed
`wasteland-lewdness`'s `$slaverent` as a scaling obligation. It is **income** — the passage is
`Claim_your_weekly_profits`, *"Receive 20 grams of gunpowder per slave"*. The variable name matched
the pattern and the direction did not, which is the same error class as reading `<<spend 5>>` as
income. Corrected in place rather than deleted, because the claim had already been reported.

---

## 2026-08-27 — the protagonist becomes a declaration, and the start choice gets a gate that fails only on zero

**Why.** Study 7 measured that all eight v2 games hand the player a finished woman and no choices
about her, against a field whose largest single bucket is `freedom` (25.9% of top-30 engagement)
while `premise` is 0 of 30. The cause was **upstream of every author and it was this skill**:
`templates/want.md` wrote `she/her` **21 times and `he/him` zero**, `the-want.md` 16 vs 0, and a grep
of the whole skill for a protagonist fork returned nothing. v1 asked the question first of anything
(`author-game/references/step-0-1-seed.md:17`, *"Pick the PROTAGONIST POV first — it decides which
fantasies even work"*); v2 deleted it. LO, asked whether the shape was deliberate: **"just happened."**

**⚠️ SHIPPED ONLY AFTER ONE REAL GAME BUILT IT FIRST** (`mrs_vance`, `f34dc3b`) — the deliberate
opposite of P0's order, refused earlier the same day for being specified before any game used the
feature. That ordering is now written into Study 7 §5 as the reason it exists.

**⚠️ THE FIX IS A DECLARATION, NOT A DE-GENDERING, and the distinction is the whole design.**
Rewriting 21 pronouns to "they" would have been churn that destroyed a measured finding — *"for a
female protagonist the ascent is not money and not status, it is reach"* — in order to launder an
assumption. The drift mechanism was *the grammar answers before the author arrives*, so the fix puts
the question **in front of** the grammar. **The female default stays and it is evidenced**: 49 corpus
comments asking for a female lead (364 likes) against 11 opposed (124 likes), with the top-30's
`female 4 of 30` being a **supply** figure — a player in that corpus counted the tags at 44 female to
100 male. What was broken was never the answer. It was that the answer was never a question.

**What changed.**

- **`templates/want.md`** — new **§1 "Who the player is — answered BEFORE she is described"**: who the
  player is (`female`/`male`/`picked`), written vs blank slate (the field runs 19 blank to 10 written,
  blank holding 80.4% of engagement; **all eight v2 games are `written` and no ledger records anyone
  choosing it**), and what the player picks at minute zero. The old §1 becomes §1b, so **nothing
  renumbers** — only one citation to a Want section number exists anywhere and it is historical.
  One line names the pronoun the template is written in and says to swap it if you declared otherwise:
  **one line instead of twenty-one edits.**
- **`references/the-want.md`** — the doctrine and every figure behind it, plus `mrs_vance` as the
  worked example, plus two ⚠️ that cost real time to learn: **additive only** (each original rung keeps
  its numbers and gains `<flag> is_false`, so no door closes and an old save reads what it read
  yesterday), and **the placement trap** — adjacent `[group]` blocks merge into one if/elseif chain
  (`v2.py:14637`), so a past-ladder dropped beside an existing ladder makes that ladder unreachable
  for every player carrying a past, silently.
- **`references/state.md`** — `want.player` = `{ who, definition, start_choice{asked_at, flags} }`.
  Declare-then-check, the contract `board.who_climbs` and `locations[].fill` already use.
- **`scripts/gates.py`** — gate **`the start choice is read`** (42 judged gates now). Undeclared →
  `n/a` *which is not a pass*; declared and read zero times → **FAIL**, naming the flag; otherwise
  PASS printing reads-per-flag.
- **Scoped, not rewritten:** `SKILL.md:92`, `the-release.md:81`, `the-want.md` §3.

**⚠️ THE GATE SHIPS WEAKER THAN IT WAS DRAFTED, ON PURPOSE.** Study 7 §5 proposed "read at least *k*
gating sites". **The `k` is refused at n = 1** — one game cannot support a floor, and that is exactly
how this skill lost an entire meter doctrine (`the-meters.md` W1, 2026-08-19). Declared-and-never-read
is the fake-freedom defect *by definition* and needs no threshold, so that is all the gate asserts.
The counts accumulate in the headline until a real distribution exists.

**Verified.** `mrs_vance` **42/42 judged, 1 n/a** — 3 flags × 5 reads, counted from the game and not
from the ledger's say-so. Seven other v2 games report `n/a` with the "an absence is not evidence"
detail. ⚠️ **The FAIL branch was exercised rather than assumed** — a fourth flag nothing reads turned
it red and named it — because this project has twice shipped a gate whose first contact with reality
was correct work. All 22 scorable games re-scored: **0 pre-existing verdicts moved**, 22/22 gained the
new row. (`sinks >= sources` excluded from the diff: still nondeterministic, found during P0, open.)

---

## 2026-08-27 — P0 measured and REFUSED: pooled variants are words WRITTEN, and gate 1 is right to count them

**Why.** `~/Documents/Female_PC_Craft_Study_20260823/proposal_for_skill.md` opens with a **P0** to
ship *"first, alone"*: make `gates.py` count a `block_pool` as **one representative variant** for
word-count purposes, because *"if we teach `block_pool` today, the scoreboard will punish authors for
using it."* P1–P6 shipped on 2026-08-24 — `engine.md` §35 documents the primitive and `register.md`
and `the-surfaces.md` teach it. **P0 never shipped**, and looked overdue.

**The observation underneath is true.** A pool renders one of N (`v2.py:14572`), so counted words
exceed what one pass shows — `mrs_vance` counts 12,509 and shows 8,706, a 30% gap.

**⚠️ THE CONCLUSION DOES NOT FOLLOW, AND APPLYING IT WOULD HAVE BROKEN A CORRECT GAME.** P0 was
specified when **no v2 game used a pool**; there was nothing to run it against. `mrs_vance` now ships
**69 pools / 221 variants** (8 + 36 + 25 across its source phases), so it is finally testable. Scored
three ways with `_collect` patched in-process:

```
model              location fill words   locations on their own budget
fold (today)              12,509          14/14
split                     12,509          14/14   <- folding is not what sets this number
one variant                8,706           4/14   <- P0
```

`the-board.md:92` decides it: `fill` is *"its word budget — in round numbers, written now, **before
the prose**"* — a plan for what the author will **write**. Three pooled variants of 400 words *are*
1,200 words written. **P0 would have scored that author 4/14 for doing exactly what the doctrine
asked** — the Study 2 R4 failure the proposal itself cites two sections earlier.

The field-baselined gates barely move either, because they are **rates** and both halves move
together: explicit floor 13.9%/108 → 14.1%/326, sentence median 9 → 9, G43 19.2 → 19.2 per 10k. And
folding is deliberate — `Beat`'s docstring: *"folding keeps our numbers comparable to the DoL
baseline the thresholds came from."*

**⚠️ AND THE ONE GATE THAT LOOKED LIKE THE REAL DEFECT WAS AN ARTIFACT OF MY OWN PROBE.** `an
explicit beat carries a clip` read **15/15 (100%)** folded and **4/46 (9%)** split — a 91-point swing
that looked decisive. It was not: the split model made each pool child its own beat and **orphaned it
from the node's sibling media**. Counted against the source instead — of 32 explicit(3+) pool
variants in `mrs_vance`, **0 carry their own clip, 32 sit under a clip on the shared node, 0 render
dry.** The 100% is honest. Recorded because it is this increment's instance of the standing rule:
a number that moves 91 points is a reason to check the instrument, not to believe it.

**What changed.**

- **`scripts/gates.py`** — the refusal recorded in full on `Beat`, at the code P0 would have edited,
  with the three-model table and the 32/32 census. Without it the next reader re-derives P0 from the
  same true observation and ships it.
- **`scripts/gates.py`** — new `_pool_pass_words()`; gate 1's headline gains `· N pools, M words per
  pass`. **Reporting only** — no threshold, no constant, no verdict change. Same move gates 19/20
  make by printing their distribution, and G43 made on this date by reporting its narration/speech
  split instead of narrowing a verdict across a seam.
- **`DOCTRINE_GAPS.md`** — a Log row, and a note in Study 7 §5 naming the pattern: **a rule specified
  before its doctrine has a real game to run against will fail correct work.** Three times now — R4
  (built, withdrawn), study 6's anchoring check (built, demoted), P0 (specified, refused). The
  cheapest was the one never built, and the difference was having a game that used the feature. That
  is the argument for doing G1's Step 2 before its gate.

**⚠️ NOT CHANGED: how words are counted, how beats are built, `_collect` behaviour.** That is the
finding.

**Verified.** All 22 scorable games scored before and after: **0 verdicts moved** (`pass_`/`na`
identical everywhere), exactly **2 headlines changed** (`mrs_vance`, `vesper` — the two games with
pools). `mrs_vance` still **41/41 judged, 1 n/a**; `vesper` still **13/35**.

**⚠️ Found in passing, NOT fixed, out of scope.** `sinks >= sources` is **nondeterministic**: three
runs on unchanged code and input named `harbour_end`, `the_lets` and `the_arcade` for the same game.
Headline text only — no verdict depends on it — but a gate whose output changes run to run cannot be
diffed, which is exactly what this increment needed it for.

---

## 2026-08-27 — DOCTRINE_GAPS Study 7: the Want template picks the protagonist before the author does

**Why.** `games/mrs_vance/REVIEW.md` **G1** recorded that eight v2 games share one Want shape —
*woman 19–39 · small town · money she cannot reach · second person* — and proposed a step that
checks a new premise against the repo. Asked whether the shape was deliberate, LO answered
**"just happened."** That turned G1 from a housekeeping item into a question about this skill, so the
30-game mopoga corpus from 2026-07-24 was re-interrogated. Its own ten findings are lostness, grind,
cheats, escalation, beat economy, parameterization, media identity, onboarding, consequence and
cadence — all mechanism — and none of them uses the `protagonist` or `premise` fields.

⚠️ **A prior study covered part of this, and it is a better instrument on one axis.** The **Female PC Craft Study of 2026-08-23** (`~/Documents/Female_PC_Craft_Study_20260823/`, eleven findings files, linked from `STATUS.md:186`) settled the gender question by **reading each game's opening** — following `<tw-storydata startnode>` into the first passages — which beats classifying a note field, and it says so of its own probe: it *"was wrong twice"*. **Its verdicts are adopted here and they moved a number:** `new-life-project` is *"Character creation — Gender assigned at birth: **Girl | Guy**"*, so it is selectable, not a fixed female PC. Its `findings_A_want.md` also already carries the mechanism this study's §4 proposes, under a better name — **"character creation is a memory, not a slider"** (Course of Temptation asks what kind of teenager she was and initialises thirteen skills the player never sees). And its `findings_J_players.md` §0.1 already documented the 500-comment cap. **What is additive here is the other half**: what carries a game across all thirty (that study read four in depth), the pronoun mechanism inside our own template, the field-wide comment counts, and the correction to G1.

**⚠️ THE PROPOSED FIX IS DROPPED, ON EVIDENCE.** Classifying reason (1) of every game's
`why_players_love_it`, weighted by mopoga comment count: `freedom` **25.9%** · `performers` 22.0% ·
`systems` 15.8% · `volume` 15.6% · `story` 7.3% · `characters` 7.0% · `cadence` 5.4% · `kink` 0.8% ·
**`premise` 0.0% — not one game in thirty is loved for its setup.** A dedup check on premise strings
guards a door nobody uses. The defect is one level up and it is ours: **all eight games let the
player choose nothing about who she is**, against a field whose largest bucket is exactly that.

**The cause is citable, and it is upstream of any output check.**

| evidence | figure |
|---|---|
| `templates/want.md` — `she/her/hers` vs `he/him/his` | **21 vs 0** |
| `references/the-want.md` — same | **16 vs 0** |
| whole v2 skill — `male pc` · `blank.slate` · `self.insert` · `character creation` | **0 hits** |
| `the-want.md:34` · `SKILL.md:92` · `the-release.md:81` | *"For a female protagonist"* as a **given** |
| `templates/want.md` §1 heading | **"Who she is"** — a finished person, not a fork |

Nobody chose a woman eight times. The template's grammar chose, twenty-one times per fill — which is
also why a dedup step could never have caught it. **v1 asked the question first of anything**
(`author-game/references/step-0-1-seed.md:17`, *"Pick the PROTAGONIST POV first — it decides which
fantasies even work"*, with female-PC and male-PC as named forks) and carried the blank-vs-written
axis too (`customization.md:213`). v2 deleted both.

**⚠️ THE GENDER IS NOT THE FINDING, and the study says so twice** so a later reader who sees
`female 4 of 30` does not draw the obvious wrong conclusion — it is a supply figure, and the 8-23 study reached it independently: *"the genre's top ranks are mostly male-PC games where women are the content."* Across all 22,622 comments (nested
replies walked, against 12,953 top-level): **49 asking for a female lead / 364 likes** versus **11
opposed / 124 likes**, and the opposed get piled on. `Vesper` is the control — authored before the
Want file, `narration_person = "third"`, none of the shape.

**⚠️ §3 REPORTS NO v1 DEFECT, DELIBERATELY.** The study format's third section is *"Where v1 is
wrong"*, and here v1 is not wrong — it is thin and unmeasured, naming both forks and giving no rule
for choosing. Manufacturing a defect to fill the section is the naivety `DOCTRINE_GAPS.md` exists to
avoid, so the section says that plainly instead.

**⚠️ ONE MEASUREMENT TRAP HIT AND THROWN AWAY.** `comments/*.json` caps at 500 replies per game, so
the first axis table returned identical medians on all three axes — an artefact, not a result.
Rebuilt against `report.md`'s ranked engagement list. Written into `eng.py`'s docstring, not just the
prose, alongside the note that the axes are hand-classified because a regex mis-sorts the mutable
rows (`friends-of-mine` *"male start, mutable"*, `wasteland-lewdness` *"male only (female MC only
after completion)"*) — which are the rows the question turns on.

**⚠️ CONVERGENCE, NOT DISCOVERY.** The 2026-06-17 non-linear-RPG research already named *"no
PLAYER-IDENTITY axis"* as its one critical gap and closed *"analysis only, nothing changed."* Same
gap, v1 from theory and v2 from field measurement. Recorded as the **second** writing-down so it is
not derived a third time.

**What changed.**

- **`DOCTRINE_GAPS.md`** — new **Study 7 · Who the player is** in the mandatory five-section format,
  new inventory **item 14** under Tier 3, and a Log row.

**⚠️ NOTHING ELSE. `references/the-want.md`, `templates/want.md` and `scripts/gates.py` are
untouched**, and §4/§5 of the study are marked `PROPOSAL — NOT APPLIED`. The candidate gate — *a
start-of-game choice does not ship unless real content reads it* — is **explicitly not built**, per
this file's own Study 2 R4 precedent, where a gate written ahead of its doctrine fired on 7 of 8
doors in a real game for obeying `engine.md` §15. It gets built only after one real opening proves
the choices can change anything.

**Verified.** All four tables regenerated from
`~/Documents/Mopoga_Twine_Sandbox_Research_20260724/premise_study_20260827/tables.py` rather than
transcribed, and diffed against the study text. Pronoun and fork counts re-grepped at write time.
Every `file:line` citation opened. No build run and none needed — no TOML, engine or gate file
touched.

---

## 2026-08-27 — gates.py G43: report where the dashes live, and refuse to narrow the verdict

**Why.** G43 shipped counting every dash in a game. Applied to `mrs_vance` that produced a true but
misleading number: **24 of its 32 dashes were inside `dialog` blocks**, and every one of those is
speech breaking down — *"Mrs. Vance — Mrs. — I can't, if you keep —"*. The em-dash is the correct
English mark for an interruption, so **76% of the game's score was punctuation that is not a
defect.** An instrument that marks a game down for its stammers is measuring the wrong thing.

**The obvious fix was investigated and REFUSED.** Narrowing the verdict to narration needs a
narration-only *field* baseline, and the corpus cannot supply one: **14 of the 25 games put under 2%
of their words inside quote marks** (corpus median 1.3%), marking speech with italics, speaker
prefixes, or nothing at all. There is no reliable way to separate their narration from their
dialogue. Judging a narration-only measurement against an all-prose ceiling would be precisely the
seam error G43's own header exists to warn about — committed knowingly the second time. So the
verdict and `DASH_CEILING` are unchanged and the split is **reported** instead, joining the three
companion numbers already carried with no field figure.

**What changed.**

- **`scripts/gates.py`** — G43 gains a `_tex_split` walk over `canvases[].nodes[].blocks[]`
  (mirroring the traversal `_speaking_blocks` already uses for G23, including `props.beats[]` and
  nested `blocks`) that separates spoken text from narration and prints both rates. `thought_bubble`
  counts as spoken: it is a person's voice and stammers for the same reasons.
- **`DASH_CEILING`** gains a second ⚠️ recording that it counts speech on purpose, that this is a
  known cost, and the 14-of-25 measurement that makes narrowing it impossible.

⚠️ **The block walk must count braces.** A naive `\{ type = "(\w+)"(.*?)\}` stops at the first `}`,
which in a `dialog` block closes `props = { speaker = … }` — so `content` falls outside the capture
and **every dialogue dash reads as zero**. That bug produced a wrong count during this very
investigation and was caught only by printing the raw TOML.

**Verified.** `gates.py mrs_vance` **41/41**. The new line reads `narration 0.0/10k over 9,865 words
· speech 91.3/10k over 2,629 words` — which is the whole point: after the game's narration dashes
were fixed, every remaining dash is speech, and the gate now says so on one line instead of
implying the game still has a habit.

---

## 2026-08-27 — gates.py G43 + register.md: the first gate that measures how the writing SOUNDS

**Why.** Two players read a shipped v2-lineage game and said the prose "smacks of an underpowered
AI whose 'mother language' isn't english," and that this made the narrative hard to follow. That
put a standing claim in doubt, so the claim was tested rather than defended. Of the 42 gates then
in the file, exactly one looked at writing (G19, median sentence length) and the game in question
**passed it**, at 12 words against a field median of 12. The prose was field-normal on the only
axis measured, and far off-field on one that had never been measured. Separately: the 25-game
mopoga corpus had been on disk since 2026-07-24 and had only ever been asked structural questions.
Its prose had never once been compared with ours.

**⚠️ A finding was made, published in-session, and then RETRACTED. It is recorded here because the
retraction is the more useful half.** Measuring our games from `output/index.html` produced
"joints per sentence, ours 4.75x the field." That was an artifact. Our built HTML carries UI list
blocks that never reach a full stop, so the sentence splitter read each as one enormous
comma-filled sentence: 10.6% of our HTML "sentences" are those blocks, against the field's 1.5%.
Re-measured on authored beat text, the basis a gate actually reads, **the direction reversed** —
our prose is *less* packed than the field, `mrs_vance` 0.53 against 0.77. No packing gate was
built. This is the same family of error the `SENTENCE_CEILING` comment already documents, hit a
second time, and it is now written into G43's header so the third time is caught.

**What changed.**

- **`scripts/gates.py`** — new constant `DASH_CEILING = 35.0` beside `SENTENCE_CEILING`, and new
  gate **G43 "prose texture"** beside G19. Dashes per 10,000 words, read from `b.text` and never
  from built HTML. The ceiling is the corpus **maximum**, not its median: a shipped and
  heavily-commented game writes at 35.4, so a game at or under that cannot be called wrong without
  contradicting the field. The gate catches an author who has left the distribution, not one
  working at its edge. Corpus figures: p50 0.99 · p75 4.21 · p90 17.46 · p95 25.72 · max 35.41.
- The gate also prints joints per sentence, the share of `you`, and pronouns per name, explicitly
  **with no field figure and no threshold**. A first draft did quote field figures for all three
  and was wrong to: they come from HTML and the gate reads TOML, and `pronoun:name` moves from 0.87
  to 9.99 on the same game across that seam. Caught in verification, fixed before commit. The dash
  rate is quoted against the field precisely because it is the one that holds (27.2 HTML, 25.4
  TOML, a 7% move).
- **`references/register.md`** — new section **"Dashes stay rare"** after "Sentences run short",
  with the corpus table, the rule, and a real three-state worked example from `mrs_vance` prose:
  the original, the comma swap that is *not* the fix, and the split that is. Carries the ⚠️ that
  swapping a dash for a comma leaves the joint in place; measured across two of our own games, dash
  rate fell 3.5x while comma joints per sentence went **up**. That swap is what the `humanizer`
  skill's §14 prescribes, so it will be suggested again. Also notes that this is the file's first
  subtraction-shaped rule, against roughly five add-shaped rules for every cut-shaped one.
- **`references/register.md`, "What is not measured here"** — records that texture is now measured
  on exactly one marker, and that the three companion numbers are a trend line across our own games
  and not a score.

**Verified.** `gates.py mrs_vance` **41/41** (was 40/40), G43 passing at 25.4/10k, which reproduces
an independent measurement of the same game to the decimal. `the_season` 2.3, `off_season` 5.5,
`forty_miles` 1.8, all passing, no other gate's verdict moved in any of the four. `--json` parses
and carries the gate. **Negative control:** the ceiling is worthless if nothing fails it, so G43's
expressions were replicated read-only against `vesper`'s authored TOML, which reads **123.0/10k,
FAIL, 3.5x the corpus maximum**. The gate therefore discriminates: it clears the four games the
corpus says are normal and fails the one game human readers actually complained about.

**Not changed.** No prose in any game. `mrs_vance` sits at the field's p95 with 32 dashes in 21
content blocks, which the corpus itself says is inside normal, so it was measured and left alone.
`games/vesper/` was not touched at any point; it appears above only as the calibration case.

---

## 2026-08-27 — the-meters.md: how "it delivers people" is actually built on this engine

**Why.** The correction earlier today told authors that a rising audience meter *should* have
mechanical consequence and named the field's four shapes — delivers people, modifies a roll,
scales a rate, prices the world. It did not say how to build any of them here, and the first
author to try it (`mrs_vance` S1b) found that the answer is the **Lane 3 dispatcher** and that the
obvious way to write it is wrong. Doctrine that names a target and not a route is half a rule.

**What changed.** `references/the-meters.md` gains a subsection, *"How 'it delivers people' is
built on this engine"*, under **Rarely a lock is not the same as never mechanical**:

- A substitution rule already takes a per-rule `conditions` block (`v2.py:5337`), so banding a
  walk-in on a meter is one block — no engine work, no new primitive. Worked TOML included.
- ⚠️ **Append, never prepend.** Rules in an `exclusive_group` share one dice over cumulative
  buckets (`v2.py:5345`) and a claimed-but-failed slot falls to solo rather than promoting the
  next rule (`v2.py:5378`). Appended, the bonus rule takes a bucket that already fell to solo and
  nothing outside the band moves. Prepended, it silently cuts the rate of every rule below it —
  including NPC walk-ins that have nothing to do with the meter.
- ⚠️ Copy the conditions from the rule above and add the meter item; a bonus rule that drops the
  presence gate still claims its slot and still fails, on the wrong reason.
- ⚠️ Choose the meter's **direction** out loud. Delivering more as it rises is right when being
  known is the fantasy and backwards when the fantasy is the title being stripped.
- **Prove it with a distribution, not a playthrough** — and both halves, or the check is vacuous.
  Two traps that make it read PASS while proving nothing are recorded: measuring at an hour where
  no named walk-in can fire, and leaving `player.current_location` unset, because `requires_npc`
  is checked as *is that NPC where the player is* (`v2.py:5340`).

**Verified.** Every `v2.py` line reference read in the generator source before it was written
down. The pattern is shipped in `games/mrs_vance/toml_phases/3_activities.toml` (four hosts) and
measured by `games/mrs_vance/playtest_walkins.py` at 6,000 rolls per band per host: all four lifts
land between +0.141 and +0.163 against a declared +0.15, and every named walk-in is flat to within
0.009 across the bands. `gates.py mrs_vance` 40/40, 0 FAIL. Both harness traps above were live
failures found in that run, not hypotheticals.

⚠️ `the_season` also ships a `known` meter built on the pre-correction doctrine and is still
untouched — a different game and a different session's call.

---

## 2026-08-27 — W5b: the 644 was three games, and it taught a meter to decide nothing

**Why.** `mrs_vance` shipped `standing` written at 25 sites and read at 4, all four in one canvas.
Tracing where that design came from led to this skill, not to the game: `0_systems_spec.toml`
declared it *"a W5b audience meter … it refuses almost nothing. The field reads reputation at 644
sites and refuses at 2% of them."* The game inherited both the shape and the number from here.

### 1 · What the number actually is

`findings_H_known.md` §1 is explicit about its sample and this skill was not:

```
degrees-of-lewdity   610 read sites      <- 95% of the total
zaras-school-life     23
course-of-temptation  11   flagged by the source itself as INSTRUMENT-BLIND, not low
                     ---
                     644  written into W5b, SKILL.md and STATUS.md as "the field"
```

The study did nothing wrong. **W5b generalised three games to a field**, `SKILL.md`'s
fifth-commitment table compressed it to a one-line law, and a game then built to the law.

### 2 · Re-measured over thirteen games

`~/Documents/Player_Legibility_Study_20260825` §44, instruments `measure_reputation.py`
(`--selftest` pins 19 variable names), `measure_rep_use.py`, `measure_rep_final.py`:

```
1,944 references · 13 of 25 measured field games carry a reputation meter
link-bearing branch arms          ~10%   (not 2%)
reads that change something       MEDIAN 41%
passages carrying a read          median 31        rungs  median 9
```

**What survives:** it rises, it rarely locks a door, its commonest single use is a line swap.
**What does not:** *"therefore it only swaps a line."* That was one game's house style read as the
field's law. Three mechanisms the narrow sample could not contain, **none of which refuses the
player anything**:

| game | the meter | shape |
|---|---|---|
| `patriarch` | `gt 5` → Marlene knocks · `gt 9` → Luna · `gt 14` → Ana; and weekly income by band | delivers people · prices the world |
| `destroyer` | `_roll1 to _roll + $Respect` in every pickup and fight | modifies a roll |
| `corpo-life` | 8-rung `$prestige_level` read at 308 sites — `(Relationship +1 from prestige)` | scales a rate |

### 3 · ⚠️ A second error, in the opposite direction

W5b's example for *"the meter is optional"* was `family-ties` — *"267 distinct variables and not
one of them tracks reputation."* It carries **six**: `you_init` declares `uni`, `southCafe`,
`onlyfans`, `inst`, `model` and `pornhub`, each with its own `fame`, read 257 times. It is not the
field's example of a game without the meter, it is the field's best example of a **place-scoped**
one. The original error came from correctly withdrawing `$sexPose` as a false positive (it is the
sex *position*) and then concluding the game had nothing rather than looking again.

**The rule survives; the example is replaced** with ten games that genuinely carry none —
`friends-of-mine` (2,707 passages), `family-business` (2,318), `the-company` (2,078),
`wasteland-lewdness` (2,056) and six more. Twelve of twenty-five measured field games have no such
meter.

### 4 · Instrument holes closed before any figure was reported

- A `rep` substring match pulls in `$fireplace`, `$weddingprep`, `$replay`, `$repayment`,
  `$replaced`, `$karleeRepeat`, `$amyForeplay`. Fixed segmentally. **A first regex-boundary attempt
  failed silently because `re.IGNORECASE` makes `[A-Z0-9]` match lowercase** — the character class
  stopped being a boundary at all. `--selftest` now pins 19 names.
- `<<set $Reputation to $Reputation + 5>>` is the ordinary increment, not a dice roll. An
  arithmetic test mis-scored all 31 of patriarch's; the rule is that the assignment target must be
  a *different* variable. patriarch 31 → 0, destroyer 41 → 16 with the survivors verified.
- `become-taxi-driver` has **no** reputation meter — all 103 hits are `$rep_quest_<name>.{time,min,
  count,fase}` quest bookkeeping. `$standing_[1-4]` in `corpo-life` are **video filenames**.

### 5 · What changed

- `references/the-meters.md` — **W5b** retitled *"it rises, it rarely refuses, and it still decides
  things"*; a correction box at its head; the optional-example paragraph rebuilt on the ten
  zero-reputation games; a new section **Rarely a lock is not the same as never mechanical** with
  the four-row mechanism table and where the reads live (repeatable job and location surfaces, not
  the sidebar — surface reads are 0–16 per game against 7–934 in ordinary passages); the W5 pointer
  and the Section-H footer annotated; the 644 block now discloses its three games inline.
- `SKILL.md` — the fifth-commitment table's reputation row now reads `~10% of branch arms (13
  games)`, with a ⚠️ note that colours-more-than-it-locks is **not** decides-nothing; the Section-H
  citation further down annotated.
- `STATUS.md` — the W5b index row and the Section-H study row both carry the corrected sample.

**Not changed:** `the_season`, which also ships a `known` meter built on this doctrine. Flagged,
not touched — it is a different game and a different session's call.

### 6 · Verified

- Every excluded variable was **read before it was excluded**, not pattern-matched away; the four
  exclusions are named with their reasons in `measure_rep_final.py`'s docstring.
- `family-ties`' six fame meters confirmed against `you_init`'s literal declaration, not inferred
  from a name.
- `grep -rn 644` across the skill returns only the six sites above, each now carrying its sample.
- The companion figure in the same spec block — *"field runs 8-17 rungs on a player meter"* —
  was re-measured and **holds** (median 9 across 12 games). Only the 644 was bad.

---

## 2026-08-26 (5) — `npcs[].role`: the label under the name in every dialogue box

**Why.** LO, on the prose-anchor fix for W1: *"I don't think this is the proper solution for it. In
the dialogue box, we do show the NPC portrait and name — below name should also show another
field."*

The anchors recur every few visits. The dialogue box carries it **every time somebody speaks**:

```
[face]  Cade
        husband's eldest
        "Slower. You're not doing the books now."
```

### 1 · The field — `npcs[].role`

Short, authored, rendered under the name in the NPC dialogue box. `speaker = "player"` and
`speaker = "unknown"` take none. Plumbed through **both** build paths — `template_import.py` for
`--use-db` and `game_graph.py` for the default — using `npcs[].tags` as the precedent.

### 2 · ⚠️ Authored, never derived — and the repo is the argument

Deriving it from `relationship`'s first clause was the obvious idea. Measured before writing a line:

```
mrs_vance    5 of 6 relationship strings contain "husband"  (him, his three sons, his brother)
the_season   two characters whose strings both begin "Your brother"
```

A derived default labels five people `husband` and two people `brother` — **exactly the confusion the
field exists to remove**, and silently, because nobody would look. Empty renders no line, which is the
safe default.

### 3 · The one rule a gate can hold — uniqueness

`validate()` **refuses two roles that match** (case-insensitive, trimmed), and refuses a label past
five words. It cannot invent the words; it can refuse two people wearing the same one. `the_season`
would fail the moment it adopts the field with two `brother`s — which is correct, and it is the game
that produced the original complaint.

F10 gains the mechanical half: the TOML shape, the three rules, the worked table for hard casts
(`elder brother` / `younger brother`, `husband` / `brother-in-law`, `father's brother` /
`mother's brother`, `housemate, top floor` / `housemate, back room`), and the warning that this is
**not** a swap for the name — `destroyer` is the only game of 26 that swaps, and it survives on
having one of each relation.

### Verified

- New suite `test_npc_role_label.py` (11). Full app run **255 passed, 7 skipped**.
- `mrs_vance` authored six unique labels; **169 role spans** in the build.
- **Cross-game isolation.** Seven games rebuilt. The six that declare no role differ by **twelve
  lines — the CSS rule alone**, for a class none of them uses.
- ⚠️ It did not start that way. The first build put `"role": ""` into `$npcs` for **every NPC in
  every game** — a dead key in every save, since the label is baked into passage HTML at build time
  and nothing reads it back. Added to the existing strip list beside `customizable` and
  `relationship_options`. Caught by hashing all seven builds, not by a test.
- `40/40 judged gates` · `speakers are named` 253/253 · `playtest_presence` 10/10 ·
  `playtest_quests` 23/23.
- **Live:** the box renders `Cade:` at y=382 and `husband's eldest` at y=406, same left edge, with
  the portrait to its left. `Stranger:` still renders with no role.

---

## 2026-08-26 (4) — `ambient_render` reverted; `description_variants` kept

**Why.** LO, after the four render buckets were laid out for him: *"Undo that change completely
first."*

`[settings] ambient_render = "inline"` — which gave a Lane 2 random ambient the room's **description
slot** instead of the whole screen — is **gone**. A random ambient `<<goto>>`s again, exactly as it
did before 2026-08-26 (2) and as it always has in every other game.

Removed: `setup.getStoryOneShotRedirect`, the `inlineOnly` parameter on
`setup.checkRandomEncounters` and its substitution guard, `_location_autofire_line`,
`_wrap_ambient_slot`, the `self.ambient_render` read, `VALID_AMBIENT_RENDER` and the whole
`ambient_render` path through `template_import.py`, and
`apps/game_generation/tests/test_ambient_render_inline.py` (11 tests).

### ⚠️ `[[locations.description_variants]]` is NOT part of this and stays

It shipped in the same commit and is a **separate feature** — it is what actually closed M1 and M2.
The two touched in exactly one place (`_render_location_description` called `_wrap_ambient_slot`),
and that call was the seam. State-reactive room prose still works; `mrs_vance` still carries nine
variants across seven rooms.

`the-first-hour.md` F9's authoring note now records the ambient behaviour as an **engine limit**
rather than as a setting, with a line saying the setting was built and reverted so nobody promises
against it in a ledger.

### Verified

- `pytest apps/game_generation/tests/ -q` → **244 passed, 7 skipped** (255 minus the 11 deleted).
- Zero references to `ambient_render` / `getStoryOneShotRedirect` / `inlineOnly` /
  `_wrap_ambient_slot` / `_location_autofire_line` anywhere in code or game TOML.
- Seven games rebuilt: **six byte-identical**, `mrs_vance` changed in exactly the intended way —
  its room passages lost the `<<set _amb …>><<if _amb>><<include _amb>>` wrapper and kept the
  `<<if setup.triggerConditionsSatisfied(…)>>` variant chain.
- `40/40 judged gates` · `somebody speaks` 4.4:1 · `playtest_presence` 10/10 ·
  `playtest_quests` 23/23.
- **Live 5/5**: a forced ambient lands on `Canvas_amb_yard_crossing_Node_base` with **0 nav cards
  and no room description**; the shop-floor variant still renders with 5 nav cards below it; the
  base returns at 03:00.

⚠️ Two probe traps worth keeping, both of which produced a false FAIL first: the ambient's own prose
contains *"the roller door is up"*, which is also in the shop-floor variant — assert on a phrase
unique to the room. And `<<goto>>` **defers to after the current render**, so `State.passage` read
in the same `evaluate()` still says `Location_the_yard`.

---

## 2026-08-26 (3) — F10: the role stays attached after the introduction

**Why.** LO, who wrote `mrs_vance` himself, asked **"Who is Sherrod?"** off a location button. The
answer exists and is good — *"Your husband's brother, 51…"* — and renders on the cast page and
nowhere else. It is the second game to draw this from him; `the_season` got *"I don't know who is
who."*

Measured over each character's own canvases: the spine of the game carried **14 canvases and 2,594
words and said who he was twice.**

### 1 · `references/the-first-hour.md` — new rule **F10**

F7 gets the role on screen **at the meeting**. F9 says a place keeps saying what it is **on every
visit**. Nothing said the same for people, and "who is this" is a standing question that a meeting
answers once.

F10 puts the relation in the surfaces the player **re-enters** — hubs, ambients, walk-ins, not the
one-shot that already did its job — and says to put it in a `block_pool` variant so it recurs
instead of nagging.

⚠️ **It also writes down what NOT to do**, because I proposed it in the same session and was wrong:
do not swap the NAME out for the relation on the speaker line. `destroyer` does
(`<<speech "teagan" "Stepsister">>`) and is the **only game of 26** that does — it survives it by
having exactly one of each relation. Relation words on buttons run at field median 0.4%, max 2.0%;
`sluttown-usa` is a family premise with 37,408 speaker labels and uses names only. Swapping does not
remove the memory tax, it moves it. **Both, at the point of use.**

### 2 · `scripts/gates.py` — `lint · the role stays attached`

⚠️ **A version of this was tried and rejected, and F7 records why** — a fixed KIN-WORD list run over
MEETINGS fired wrongly on ten of `last_call`'s meetings, eighteen of `the_inheritance`'s and three of
`off_season`'s, because `last_call`'s cast is not family and the words were never going to be there.

This one takes its vocabulary from the game: **anchors are the content words of each character's own
`npcs[].relationship` string**, and it counts over that character's own canvases rather than over
meetings. A cast of colleagues yields its own words; a game that declares no relationships yields
nothing and is **skipped rather than failed**. A LIST with no threshold — there is no per-character
field baseline and inventing one is what this file refuses everywhere else.

### Verified — and the control is the whole point

```
last_call         silent   0 relationship strings declared — no vocabulary, no false positives
off_season        silent   0
the_inheritance   silent   0
the_season        FIRES    Wade 13 per 10k, the thinnest row in the game
late_shifts       FIRES    Cole, 807 words across 8 canvases, says who he is 0 times
```

**`last_call` is silent by construction** — the exact game the previous detector got wrong. And
`the_season` is the game that drew *"I don't know who is who"* from the reader; the lint found it
without being told.

`mrs_vance` fixed alongside: five anchors added to Cade's and Booth's recurring surfaces, taking them
from 8 and 12 per 10k into the 21–45 band the rest of the cast already sat in. `40/40 judged gates`
before and after, `somebody speaks` unmoved at 4.4:1, app suite unchanged at **255 passed**, and live
4/4 — the anchor appears in 4 of 30 hub renders while the speaker line says **Cade** in 30 of 30.

---

## 2026-08-26 (2) — the room can finally change, and an ambient stops taking the screen

**Why.** F9 was rewritten this morning to say the description carries the place. It then had to
admit, in its own text, that half of what the field does *"is not authorable"* — a location
`description` was one static string. LO: *"now do the engine work for M1."*

### 1 · `[[locations.description_variants]]` — state-reactive room prose

`description` stays required and becomes the else branch; each variant is `{conditions, text}` and
the generator emits a first-match `<<if>>/<<elseif>>/<<else>>` chain using
`setup.triggerConditionsSatisfied`, the helper the location passage already calls for
`entry_conditions`. No new runtime primitive.

The useful axis turned out to be **`npc_at_location`** — the room describing itself differently
when somebody is in it, which is the "what happens here" half of F9's rule told by the room rather
than by a scene.

⚠️ **The importer refuses a variant whose `conditions` lack `version = "1.0"`.** The evaluator
returns **true** for any conditions without it and raises no build error, so such a variant would
render forever and the location's own description would never be seen again — worse than having no
variants at all.

⚠️ **There is no time-of-day condition in the evaluator** — `flag`, `trait`, `npc_at_location`,
`stage`, `quest`, `item`, `days_since_flag`, `corruption_level`, clothing, and nothing that reads
the hour. F9 now says so instead of implying hour-variance is available. Rotation between visits is
also still unbuilt, and F9 says that too.

### 2 · `[settings] ambient_render` — `"redirect"` (default) | `"inline"`

Under `"redirect"` a random ambient `<<goto>>`s and owns the entire screen: the player walks into
the Yard and never sees the Yard. `"inline"` gives the ambient the **description slot only**, and
the title, NPC portraits, solo activities and the navigation grid all render around it — destroyer's
shape, where the encounter and the room's own prose are two branches of one `<<if>>` and the
affordance bar and the exits print either way.

A **story one-shot keeps the redirect under both settings**; a story beat owning the screen is
correct. `setup.getStoryOneShotRedirect` is the new one-shot-only selector, and
`checkRandomEncounters` gained an `inlineOnly` flag that skips ambients carrying Lane-3
substitutions — those inject a `<<goto>>` at node 1, which inside an `<<include>>` would navigate
away mid-render.

### Verified

- Two new suites: `test_location_description_variants.py` (12) and `test_ambient_render_inline.py`
  (11). Full app suite **244 passed, 7 skipped**.
- **Cross-game isolation, which is the load-bearing check.** Seven built games were hashed before
  and after. Every authored passage in `vesper`, `off_season`, `the_season`, `last_call`,
  `late_shifts` and `the_inheritance` is **byte-identical**; the only delta anywhere is 25 lines of
  new runtime library (an unused function and an unused parameter).
- `mrs_vance` opted in and authored nine variants across seven rooms. `40/40 judged gates pass`,
  `playtest_presence` 10/10, `playtest_quests` 23/23.
- Live in headless Chromium, 7/7: the shop-floor variant renders while the shop is working, the
  base returns at 03:00, and with an ambient forced the description is replaced **while the exits,
  the portraits and the room title all still render**.

⚠️ **The default build is the no-DB path.** `package_from_toml` without `--use-db` builds through
`apps/projects/services/game_graph.py`, not the DB writer in `template_import.py`. A property added
to only one of them reaches the generator in neither the way you expect — the first build of this
feature emitted the ambient wrapper and zero variants for exactly that reason.

---

## 2026-08-26 — F9 was teaching the outlier, and a gate was enforcing it

**Why.** LO, after nine first-visit "arrival" canvases were written for `mrs_vance`, shipped green
and reverted the next day: *"I think the place name is description and what was going in that place
should be able to tell the whole story."*

He is right, and the skill is what sent the author the other way.

### 1 · `references/the-first-hour.md` F9 — rewritten

F9 taught that a place introduces itself **the first time the player walks in**, and worked its
example from `degrees-of-lewdity`'s `$forest_shop_intro` / `$gwylan_cafe_intro` family. Counted
across the 26-game corpus, that family is one game:

```
degrees-of-lewdity   258 first-visit branches, 117 flags     the only game doing it
realm-of-corruption   12
five games             2 each
EIGHTEEN OF TWENTY-SIX     zero — destroyer, become-someone, course-of-temptation,
                           the-company, friends-of-mine among them
```

**The section's own worked example proves the point against it.** The failure it documents is an
anchor whose description ran long, specific and well written — *"forty machines, half of them off at
the wall to save the electric"* — and never said **amusement arcade**. That is a description that
does not name its function. A scene played once does not fix it, because *"what is this place"* is a
standing question and the description is the only surface the player sees on every visit.

F9's rule is now the description. The first-visit canvas is kept as a **named minority device** with
its evidence, for a place that has a genuinely one-time thing to say, and explicitly not as a
substitute for a description that names the function.

Added the field's real numbers (room prose per visit median 82 · 10 variant branches · 22% of rooms
rotating text · 17% varying by hour) **and the honest note that half of that is not authorable**: a
location `description` is one static string (`v2.py:9629`, `:9676`) and `_resolve_at_references`
substitutes names only, so it cannot vary by state. Filed as an engine gap so no ledger promises
against it.

### 2 · `scripts/gates.py` — gate G35 deleted, replaced by a list

`the anchor introduces itself` passed a game only if its anchor carried a non-repeatable canvas.
**A green board therefore required a device eighteen of twenty-six top games decline to use**, and
while it stood it sent one author to write nine arrivals that were reverted.

Replaced by `lint · the place says what it is` — every location ordered by how much prose happens
there, against the length of its own description, with a first visit noted as information rather
than as a requirement. A list and never a score, because whether a description names its function is
a reading. The `named before met` lint keeps only its F7 half (people); its places half moved here.

### Verified

`gates.py` parses; run against `mrs_vance`, `off_season`, `the_season` and `vesper`. Every game
loses **exactly one pass and one total** — 41/41 → 40/40, 39/41 → 38/40 — so the gate was passing
everywhere and no game's pass/fail state changed. The new lint on `mrs_vance` reads:

```
14 location(s) · median description 57 words · field room prose per visit, median 82
  · Office: 3,845 words happen here, described in 85 · has a first visit too
  · Back Row: 1,116 words happen here, described in 64
  · Booth's Room: 784 words happen here, described in 45
```

---

## 2026-08-25 — C5's own worked example was the dead path, and §15 answered half a question

**Why.** LO: *"I didn't liked showing the why text for locked choices."* `mrs_vance` is the first
game authored after §15 was reversed on 2026-08-24 and it followed the new instruction exactly —
**22 of 22** shown-locked choices carrying a reason, against **13 of 171** across every game before
it. Investigating which of those to cut turned up a second, worse thing.

### 1 · ⚠️ `the-clock.md` C5's TOML snippet put both keys in the wrong table

The section's example was:

```toml
[canvases.trigger.metadata]
show_when_blocked = true
cooldown_message  = "…"
```

**That path is dead.** The importer reads `trig_def.get("show_when_blocked")` and
`_require_str(trig_def, "cooldown_message")` — `template_import.py:1929-1930`, the **trigger table
itself** — and then writes them *into* metadata at `:6980-6981` for the generator to read back at
`v2.py:11484`. Authoring them in `metadata` skips the importer entirely: valid TOML, green build,
every gate passing, and `showWhenBlocked` reaching the built HTML **zero** times.

`mrs_vance` copied the example verbatim. **Ten authored schedule lines, none of them ever on
screen**, and the activity vanishing at the wrong hour exactly as C5's own paragraph warns — *"which
reads as a broken game, not a schedule"*, against a top-30 study where **lostness, not grind, is the
genre's disease (4.7% of complaints against 0.9%)**. Confirmed live: at 20:00 the office showed no
counter row at all before the fix and shows `Work the counter — mornings, seven till one…` after.

`off_season`, written **before** this section existed, has always declared them at the top level —
which is why its six work, and why the doctrine could be measured off it while the example was
wrong. Snippet corrected, warning added, and the house register recorded: the engine renders
`<row name> — <message>`, so the message is a bare lowercase phrase, never a sentence restating the
row (*"Work the counter — The counter — mornings…"* was the doubling).

### 2 · `engine.md` §15 — the other half of the reversal

§15 says what a shown row must SAY. Nothing said how many to show. Added, from
`findings_B_refusal.md`:

- **The field's default is silence** — 71% of 16,167 refusals render nothing; per-game silent share
  median **79%**, range 22–100%, which the study calls *"a house decision, not a genre norm"*. There
  is no number to hit, so this is a list and never a gate.
- **A door is not a refusal.** Field spoken refusals: n=4,540, **median 9 words**, flat and
  mechanical, naming a price 37% of the time. `vesper`'s nine doors: **median 22**, in-fiction, and
  the study calls it *"the only game doing this properly"*.
- **Never inside a scene when the scene moves the bar.** A rung gated on a meter the canvas's own
  effects raise opens by itself in a click or two. Measured: vesper has 8 in-scene shown-locked
  choices and **zero** self-moved; `mrs_vance` had 11 and **all 11** were `arousal` or `loop_stage`.
- **A blocked window is a different surface** — C5, not this one. Do not answer a noisy guidance
  screen by deleting the hours.

### 3 · `gates.py` — `lint_refusal_shape`

Reports the three: shown-locked count, the in-scene subset, the self-moved subset, and the
`locked_text` word-length median against 9 and 22. A **LIST, never a gate**. Gate 42 *a locked door
says why* is untouched and keeps passing.

```
                shown  in-scene  self-moved  median words
mrs_vance  was     22        11          11            15
mrs_vance  now     11         0           0            13
vesper             13         8           0            22   <- the exemplar: in-scene, none self-moved
the_inheritance    27        15          10
off_season          4         4           4
the_allowance       8         3           3
late_shifts        21         5           3             4
everything else   1-30        0           0
```

⚠️ **A first draft of this lint crashed the whole scoreboard on `the_inheritance`** — an `effects`
list carrying string entries, and an unguarded `.get()`. A lint must never be able to take the tally
down; every element is type-guarded now, and the run is clean across all fourteen games.

**Verified.**
- `41/41 judged gates pass` on `mrs_vance` before and after; gate 42 `22 shown-locked · 22 with a
  reason` → `11 · 11`, still PASS and still non-`n/a`.
- The merged diff for the cut is **22 removed lines, 0 added, 0 unrelated**.
- Live in headless Chromium: `loop_cade.act_desk` at `arousal 0` renders **no** `span.locked-choice`
  and at 95 offers the finish choice as a live link; the office at 20:00 still carries its greyed
  schedule row. 4/4, zero page errors.
- `playtest_presence.py` 10/10 and `playtest_quests.py` 23/23 on the same build.

---

## 2026-08-25 — the clock gate was reading 62% of the buttons (`gates.py`, `the-clock.md`)

**Why.** `mrs_vance` shipped a sleep button labelled **"Sleep. (to six)"** on a canvas that opens
21:00–04:00 and advances a flat 480 minutes — true for **one entry minute of 420**. G36 *the label
keeps its time* passed it. `REVIEW.md` diagnosed a missing preposition, `to`. **That was wrong**, and
the truth is bigger.

### 1 · `_clk_choices` read one of the two exit shapes

A node's exit is **either** a `choices` array **or** a single `exit_block` that is itself the button
(`{type: "location", text: "…", config: {…}}`). The helper — docstring *"Every … label the player can
read on a button"* — iterated `exit_block.choices` only.

```
choice labels it read           1,989
single-exit labels it did not   1,225      <- 38% of every button in this repo
```

**23 labels naming a clock time were sitting in the unread half, across five games.** Twenty-two use
`at` or `before` — prepositions this instrument has always known. They were invisible because nothing
looked, not because the pattern was narrow. And they are not marginal: **21 of the 23 sit on canvases
with no schedule window at all**, so the hour is true for at most one minute in 1,440.

Fixed by yielding the `exit_block` itself when a node has no `choices`. It already carries
`config.time_progression_minutes`, which is the first key `_clk_spent_minutes` reads, so C4's
duration half started working on those labels with no further change — `mrs_vance` 25 → 26 verified
tags, `off_season` 1 → 10. `_clk_choices` now yields a fourth field naming the shape, and G36 says how
many findings came from the newly-read surface so a jumped count is not misread as prose having
changed. `lint_time_cost_on_button` shares the helper and got the same widening.

### 2 · `_CLK_PREP` gained `to`, in a narrow form

Bare `to` is a false-positive machine. Measured against **81,264 action labels** from the 27-game
corpus:

```
`to` in the shared alternation .......... +8, ALL false   "Change to 0" · "Update to 0.3"
`to` + a spelled-out hour ............... +1 false        "restrict myself to one?"
`to` + a spelled-out hour, NOT `one` .... +0
```

Shipped as a separate branch with its own word-list, `_CLK_WORDNUM_NOT_ONE`. Excluding `one` loses no
reading — `at one` and `till one` stay covered by the existing branch — and `one` is the same idiom
trap `_CLK_BAD_NEXT` was built for (312 corpus hits of "at one point"). On our own prose it adds **21
hits across six games, every one a real "Twenty to eight" / "Ten to six"** the lint had been missing.

⚠️ **Neither number here restates a published constant.** `the-clock.md` publishes *84,009 labels* and
gates.py a prose median of *0.8 / p75 1.8*; this re-implementation of the extractor gives 81,264 and
0.45 / 0.91. The **delta** is trustworthy — the same instrument on both sides — the absolute level is
a different instrument's and was left alone rather than quietly overwritten.

### 3 · `the-clock.md` — the scoreboard row and the per-game table

C3 is correct doctrine and did not move. The gate's row now says it reads both exit shapes, and the
2026-08-22 per-game table was re-run, because two of its passes were an artefact of the blind spot:

```
                    now                was
steam               FAIL 16            FAIL  9
seventh_day         FAIL  8            FAIL  2
the_allowance       FAIL  6            PASS      <- a false pass
back_home           FAIL  3            PASS      <- a false pass
forty_miles         FAIL  1            FAIL  1
mrs_vance           PASS               PASS      (repaired the same day)
off_season          PASS               FAIL  2   (repaired since)
+ the_season · mothers_place · vesper · last_call · late_shifts · the_inheritance   PASS
```

Eight of thirteen pass, all four v1 games among them, so the bar is still one shipped work has
cleared. Per the standing rule the other games' 22 labels are **not** repaired here.

**Verified.**
- Corpus regression, shipped gate vs new, 81,264 labels: **0 → 0**. The `to` branch adds nothing false.
- The **pre-fix** `mrs_vance` TOML through the **post-fix** gate reports
  `act_sleep: "Sleep. (to six)" — the engine cannot reach a clock time (to six))`; the repaired game
  reports `0 label(s) name a clock time · 26 stated duration(s) all match the spend`.
- `41/41 judged gates pass` on `mrs_vance` before and after.
- `lint · the time cost is not on the button` goes `1 of 14 silent` → `all 14 long clicks state their
  duration`, because the repaired label states `(8h)` — the swap C3 itself prescribes, and the fact
  the player actually needs: sleeping at 03:00 costs the morning shift.
- Both live suites unchanged against a fresh build: `playtest_presence.py` 10/10,
  `playtest_quests.py` 23/23.

---

## 2026-08-25 — the badge arrives before the content, in five of eight games (`engine.md` §23, `gates.py`)

**Why.** `mrs_vance` printed **"✓ Arc complete"** on five of six characters at or before the click
that opened their content. §23 already warned that `terminal` is not computed from progress and gave
the rule that follows — *terminal belongs on a card the player has to CLIMB TO*. What it never said
is **climb to what**, and every v2 game answered the same wrong way: the badge sits on the threshold
that **opens** the loop rather than one above it.

**Measured across the repo, and this is the half that makes it doctrine:**

```
mrs_vance     5 of 6 - 2 landing ON the door, 3 BEFORE it (one 40 points early,
                       two on a DIFFERENT meter from the one the door reads)
forty_miles   6 of 6 - every badge at exactly the door value
seventh_day   1 badge on the door + 5 goals 25 points past anything the game reads
the_season    4 of 5
the_allowance 3 of 5
vesper        0 of 5   <- the v1 game §23 was WRITTEN FROM is clean
```

Four v2 games and not the one the section was written from. The doctrine did not fail; the sentence
that would have prevented this was never written.

### 1 · `engine.md` §23 — a meter is the wrong thing to gate a badge on

New warning under the climb-to rule: put the ✓ on a **flag the content sets on its way out**, so it
means *you have played this* rather than *you have ground past it*, with the three-card TOML worked
out (climb → ready → done). The v1 hint system had exactly that pairing —
`arc_closure_flag` + `arc_complete`, `template_import.py:1017-1023` — and the v2 card schema dropped
it without replacing it.

Also new: **a goal threshold no condition anywhere reads is a number the player climbs to for
nothing.** `mrs_vance` shipped three, `seventh_day` five. They stay invisible while the terminal
frame outranks the bullets — and become live instructions to grind for nothing the moment the badge
is fixed, so the numbers have to move in the same pass.

### 2 · `engine.md` §23 — `ready_canvas` on a triggerless canvas renders NOTHING

`lookupCanvasBySlug` (`v2.py:15371`) walks `help_data.locationCanvases`, keyed by location UUID. A
triggerless canvas — the usual shape for a sex loop — is not in that index, so the lookup returns
`null`, Frame 2 does `if (!found) return ""`, and the card falls through to no frame at all: the
exact failure the section's own goal-less-card warning describes. Point it at the **hub**. Verified
against a built HTML: `hub_cade_office` present with `hasSchedules: true`, `loop_cade` absent.

### 3 · `engine.md` §23 — the one-`terminal_text` cap is scoped to a FINISHED game

`CHANGELOG.md` 2026-08-13 records where the cap came from: `vesper` 0.1.8, where four arcs genuinely
had ended and `"Arc complete"` was **true** of them. In a v0.1 **nothing is closed**, so the cap
forces every track but one into `"Arc complete"` — **a stronger and falser claim than the string it
was rationing**. `the-release.md:107-110` already rules the other way: *"a plain marker at the top of
**each track**… An honest wall is a promise; a silent one is a bug report."* The section now caps the
**claim**, not the field.

### 4 · `gates.py` — `lint_badge_before_content`

Reports three things: a `[badge]` at or below the highest `gte` threshold any canvas condition reads
on that (character, trait); a `[goal]` above that ceiling; and a `[rung]` below it that no condition
reads at all. A **LIST, never a gate** — "content" is proxied by a canvas condition on the same
(character, trait), which is a reading. Wired into the call site, the `--json` payload as
`badge_before_content`, and the printed block.

**Verified.**
- `mrs_vance`: **8 findings before the repair, 0 after** — all five badges and all three phantom
  thresholds, including `tobin.want 30`, which is a `[rung]` below the ceiling that the `[goal]`
  check alone would have missed.
- Fires on four other v2 games with the counts in the table above, and **0 on `vesper`** — the
  strongest available evidence it measures the thing and not just fires.
- `41/41 judged gates pass` on `mrs_vance` before and after; G15 *"no chain ends in silence"* stays
  `6/6`. The lint touches no tally.
- Proved live in headless Chromium against the built game
  (`games/mrs_vance/playtest_quests.py`, 23/23): per character, the goal frame with live progress
  below the door, `🔓 Ready` **with a 📍** at the door and unplayed, and the ✓ with the authored
  string — never `"Arc complete"` — only after the loop has been played. The 📍 is asserted rather
  than mere non-emptiness precisely because of finding 2. Then all five loops played to their finish
  node, each setting its flag `False -> True`.

---

## 2026-08-25 — a lint for the ambient that puts a man in a room he is not in (`gates.py`)

**Why.** LO played `mrs_vance` — the first game to take all 41 gates — and found a character shutting
the roller door in a room the navigation panel had just shown him absent from. Fifteen random
ambients placed a speaking cast member with no gate of any kind. The build was green the whole way.

**The miss is the shape SKILL.md warns about: the doctrine was right and the instrument was aimed at
the wrong path.** `gates.py:5114` already carries the trace — `requires_npc` is consumed in exactly
two functions, `checkRandomEncounters` (`v2.py:5245`, `trigger_mode="random"`) and
`checkAndSubstituteCanvas` (`v2.py:5318`, `substitution_only`) — and G38 *"a meeting fires where they
are"* then explicitly skips both and judges the auto-fire path, which does not read the field at all.
The one path that consumes `requires_npc` had no check on it.

**What changed.** New `lint_ambient_presence(model, game)`, next to `lint_dialogue_attribution` which
it extends. It reports every `trigger_mode = "random"` canvas carrying a `dialog` block with an
`npcId` and declaring none of `requires_npc`, an `npc_at_location` condition, or its own
`trigger.schedules`. Wired into the call site, the `--json` payload as `ambient_presence`, and the
printed lint block.

**It splits the finding into two different jobs, which is the point.** The verdict is `gate it on
<name>` when the speaker has schedule rows at that location — the window exists and one line of
`requires_npc` is the fix — and `or narrate the arrival — no row here to gate on` when he does not,
because there a gate would strand the canvas forever and the fix is prose. Reported as a **LIST and
never a gate**: an ambient may legitimately place someone off-schedule (on the telephone, through a
door, arriving from somewhere the scene declines to name), and only the author can tell those from
the defect.

**Verified.**
- On `mrs_vance` before the repair it reports **20/21**; after, **4/21** — and the four are the three
  the author had already written as off-schedule plus one real open question, `amb_kitchen_house`.
- Both verdicts are exercised in that output: `amb_bathroom_water` and `amb_bathroom_landing` come
  back as *or narrate* (Booth has no bathroom row), `amb_kitchen_house` and `amb_office_wrecker` as
  *gate it*.
- Scoped across the whole repo: `mrs_vance` is the **only** v2 game with a speaking character in a
  random ambient — 46 random canvases across the other seven games, **zero** with a speaker. So the
  lint has an in-scope population of one game today. It is ahead of the corpus, not a no-op, and it
  bites the moment a second game puts its cast inside its texture.
- `41/41 judged gates pass` on `mrs_vance` before and after; the lint touches no tally.
- The gate itself proved live in headless Chromium against the built game, driving
  `setup.checkRandomEncounters()` 400 times per hour instead of waiting on a 0.26–0.35 roll: at
  Monday 10:00 the three gated bunk-room ambients return **0** while the ungated control returns 122;
  at Monday 22:00 all four return. `amb_office_phone`'s two-item `npc_at_location` condition fires at
  10:00 and not at 19:00, both directions correct.

---

## 2026-08-24 — `ne` reaches two of three evaluators, a lint learns the second container type, and two of section K's own claims are corrected

**Why.** Section K closed the field study and left two pieces of doctrine with nothing built against
them: `engine.md` §37 (`ne`, the negated form of the field's commonest gate shape) and `block_pool`
(the variant pool, documented in four places and used by zero v2 games). LO picked both. Researching
them corrected **three** things committed earlier the same day.

### 1 · `ne` — and §37 was wrong the day it shipped

§37 said the fix was *"three whitelist entries and no runtime work"* and named
`template_import.py:5414` as the line blocking `ne` on a canvas condition. **Both halves were
wrong**, and the truth is the section's real content:

| evaluator | backs | `ne` |
|---|---|---|
| `compare()` — `v2.py:3848`, reached at `:3956` | canvas / node / choice | already, since v2 shipped |
| `setup.checkSingleCondition` — `v2.py:7513` | hints, quest-goal bullets, `_findFlagSetterCanvas` | **added** |
| `setup.checkQuestsCondition` | `[[quest_cards]]` `when` / `goals` | **no, deliberately** |

**Canvas condition operators are not validated by the importer at all.** An unknown operator imports
clean, reaches the runtime JSON, and fails *closed* with no build error. So `ne` was always writable
on a canvas gate. What was broken is that the **same condition item** read through
`checkSingleCondition` fell through to `return false` — true on the canvas, false in every hint that
touched it. One line.

The second half was worse than cosmetic: the requirement-label formatter (`v2.py:7743`) mapped an
unknown operator to `"≥"`, so a `ne` gate rendered as *"Elena Affection ≥ 50"* — the game stating the
opposite of its own rule. Now `"≠"`.

⚠️ **A wrong edit was made and reverted, and the revert is the finding.** `template_import.py:5414`
was widened to accept `ne` before `setup.checkQuestsCondition` had been read. That evaluator's
`switch` has no `ne` case and falls through to `return false`, so the change would have let an author
write a quest-card condition that is **silently always false** — the same class as a `conditions`
block missing `version = "1.0"`. Reverted; the site now carries a comment saying why it stays closed
and what widening it correctly would require. Hint `trait_checks` (`:5227`), quest `stage_op`
(`:5154`) and the heuristic threshold reader (`:5782`) are untouched for the same reason, each named
in §37.

⚠️ **v1 rollback caveat.** `generators/v1.py` is frozen and carries its own `compare()` with `ne` but
not this `checkSingleCondition` fix, so a game using `ne` and rebuilt with `--gen-version v1` will
diverge — canvas gate holds, hints do not. Recorded, not patched.

**Tests.** `apps/projects/tests.py` gains `TraitConditionNeSchemaTests` and
`TraitConditionNeIntegrationTests` in the file's existing convention. The integration half asserts on
**both** evaluators, because their disagreement is the regression that matters; the schema half
asserts that a quest card still rejects `ne`, so the deliberate asymmetry cannot be "fixed" by
widening a whitelist alone. Seven tests, all passing.

⚠️ The first fixture used `targetType = "trigger"` with no resolving `trigger.location`, which fails
a different rule and **masked the operator error the fixture existed to test**. A test that fails for
the wrong reason is worse than no test.

### 2 · `gates.py` — a lint that knew one container type and met another

`_band_texts` special-cased `type == "group"` to emit one string per exclusive band, and a
`block_pool`'s variants fell through to the always-renders text and got concatenated. `lint · the act
nodes` takes a **minimum** over that list to report the thinnest thing a node can show, so a
three-variant pool would have reported the **sum** of all three — three one-word variants scoring as
a three-word band, in the flattering direction.

This is the same failure the file already warns about at the top of `_collect`, where 158 groups
across four games were invisible to every beat-based gate for exactly this reason. Rewritten so both
containers are **axes**: adjacent `[group]` blocks are one axis (they merge into one `if/elseif`
chain, `engine.md` §35), each pool is its own, and the renderable set is their cross product, capped
at 64 combinations.

⚠️ **The beat collector still folds every variant together and that is correct** — `engine.md` §35
argues why: it is the apples-to-apples comparison against the DoL baseline that set the threshold.

**Fixed before the first pool shipped**, so it changes nothing today. Verified two ways: output
byte-identical across all 21 scorable games (which is the proof `group` behaviour survived the
rewrite), and a direct check of `_band_texts` on four shapes — a pool, a two-group chain, a node
carrying both, and a plain node.

### 3 · R5d — measured by the wrong thing

R5d said our stage-counter use is *"0.7%, in 6 of 21 … the field's own pattern, used once each."*
That counts **`eq` operator occurrences**, which is the right unit for the shape census it sits in
and the wrong unit for *"do we build stage counters"* — read as the latter it says we barely do,
which is false.

Measured by **behaviour** — a trait `set` to two or more distinct integers, whatever it is called and
whatever operator reads it:

```
7 of 21 scorable games carry at least one
how those counters are READ  (n = 416)   gte 48%   eq 32%   lt 20%
```

The corpus-wide **4.5% equality figure stands and is not walked back** — it is dominated by meter
thresholds, which is a real difference from the field. But the gap is narrower and more specific:
**we do not read counters wrong, we build few of them.** `the_season`'s `wade_loop_stage` and
`prine_loop_stage` are set `0/1/2/3` and read `gte 3` / `eq 2` / `lt 2` as an exclusive three-band
chain — the field's shape, already built, in a v2 game. R5d now points at it.

The *"second doctrine lost in the v1 → v2 divorce"* line is softened to **survived in weakened
form** — present in two v2 games, absent from five — because that is what the numbers support and
`block_pool` at a true zero is the thing the stronger phrasing belongs to.

Added: **a counter nobody reads is worse than no counter.** Nine behavioural counters across four
games are written and never read by a condition. Most are legitimate — gate 33 carves out
`<npc>_stage` keys the engine reads itself (`v2.py:5549-5554`) — but `sex_stage` is set and never
read in three separate games, and **gate 33 already fails all three for it.** No gate hole; a
suspicion checked and found wrong, which is the fourth time this study.

### 4 · `engine.md` §35 — four authoring facts it never carried

Verified in `template_import.py:6210-6237`: children may sit at the block's own **`blocks`** key or
at **`props.blocks`** (§35 showed only the `props` form, which is the minority shape in our own
games); **a `block_pool` inside a `block_pool` is silently dropped** (`:6230`) where a `group` inside
a `group` is preserved (`:6218-6222`); mixed child types only **warn** (`:6235`); depth is capped at
**4** (`:6143`).

⚠️ **Six of the seven file:line citations first written into §35 were wrong.** They were taken from a
grep run **before** this session's own seven-line comment was added to `template_import.py`, which
shifted everything below it. Caught by re-reading every cited line instead of trusting the grep.
Yesterday's rule was *when a number moves, grep the number, not the file*; the addition is that **a
file:line taken before your own edit is stale by construction** — and §35 is a document whose entire
value is that its citations resolve.

### What is NOT in this entry

- **No worked `block_pool` in any game.** It was scoped for `the_season`'s two act loops and not
  written: those loops are the player character with her brother and her uncle, and that is content
  this author will not write. The mechanism therefore still has **zero** worked examples, and
  `STATUS.md` PART 6 keeps the row. The standing alternative, unbuilt and awaiting LO: the six
  repeatable non-family surfaces — `work_rows_picking`, `work_shed_hours`, `work_store_run`,
  `sleep_camp`, `wash_showers`, `eat_window` — 438 words the player re-reads daily, which is the
  case v1's Rule 17 named the feature for.
- **No gate, no lint, no threshold.** Distinct-gate union stays at **42**.
- **`generators/v1.py`** — frozen, untouched.
- **`issue.md` and `games/vesper/.find-media/*`** — a concurrent session's, never staged.

**Verified.** Baseline over all 21 scorable games captured before any edit and re-run after:
**byte-identical**, 328 PASS / 223 FAIL / 337 n/a, distinct-gate union 42. `pytest
apps/projects/tests.py` — 382 passed, 4 failed, and **all four fail at clean HEAD too**, confirmed in
a throwaway `git worktree` at `169685e`; they are pre-existing and were not touched.
`_band_texts` unit-checked on four shapes. Every file:line added to §35 and §37 re-read against the
current file after all edits were in.

---

## 2026-08-24 — Section K, the mirror: the field's most common gate is our rarest, and five numbers in this skill were arguing with themselves

**Why.** Ten study sections measured the field and asked what the skill teaches. **None of them
measured us on the same instrument** — each says so in its own closing list; section F's is typical:
*"Nothing measured about our own games."* K is the last section and it is the synthesis, so it has
the one job the others could not do: run one instrument over both sides with one denominator, and
then say what eleven sections add up to. Evidence:
`~/Documents/Female_PC_Craft_Study_20260823/findings_K_mirror.md`, instrument `probe_K.py` in the
same directory. **`probe_K.py` has a `main` with five sub-commands and every number below comes out
of one of them** — deliberately, because K's own process finding is that four instruments in this
study published numbers and were then thrown away.

**Method — reproduce before re-measuring, again.** Section F's act-gate census is K1's input and
**F's driver is not on disk** (`probe_arc.py` is a library; its caller was inline). Rebuilt, it
lands **2,306 act menus against F's published 2,292** (0.6%), median width **2** and median span
**1** exactly, and the maximum **not at all** (84 against 54). So K1's shape shares ship as a new
census and never as a correction to F's table. ⚠️ The dedupe convention turned out to be load-bearing
and F never recorded it: counting every label occurrence gives 2,516 menus and a maximum of 372.

### What was measured

**K1 · Section F's 48% residue, closed.** F classified act-gate conditions by *domain* — what the
variable is about — and left **48%** unnamed, because every game invents its own names. Classified
by **shape** instead, which is the move section B used, across **3,346 act-gating conditions in 24
games**: equality 48% · threshold 38% · function 13% · boolean 8% · random 2%, **residue 0.4%**.

The finding is the agreement with B. Measured over 16,167 *refusing* chains the split was 45 / 40 /
17 / 7 / 1; over 3,346 *escalation* gates it is 48 / 38 / 13 / 8 / 2. **Two populations, two
questions, five days apart, one distribution.** The flag-chain model and the meter model are both
load-bearing, together, at both doors.

**K2 · The mirror.** Every condition in the 26-game field (155,765) against every condition in our
21 scorable games (3,028), one classifier, one denominator:

| shape | field | ours |
|---|---|---|
| **equality** — which step are you on | **52.9%** | **4.5%** |
| **threshold** — is your number big enough | 30.7% | **56.1%** |
| function | 12.5% | 2.3% |
| **boolean** — is this switch on | 8.9% | **37.1%** |
| random | 4.1% | 0% |

**The field's most common way to gate anything is our rarest.** Its equality is mostly a **stage
counter** — one variable that counts — at **24.8% of all its conditions, in 26 of 26 games**. Ours
is **0.7%, in 6 of 21**, and those sites are `npc_jake_stage`, `loop_stage`, `wade_loop_stage` and
their kin: the field's own pattern, used once each.

⚠️ **The `random` row is an encoding difference and is labelled as one.** The field rolls dice
inside a condition; our engine rolls them in `trigger_mode`, a canvas `chance`, and `block_pool`.
Reading our 0% as a finding would be reading the schema.

⚠️ **Our v1 games do this the field's way and our v2 games do not** — `vesper` 10% equality,
`the_long_summer_test` 11%, `last_call` 7%, against `back_home` 0%, `off_season` 1%, `the_season`
2%. The TLS notes carry the rule in a line: *"sex-loop = numeric-enum state NOT flags."* **Second
doctrine lost in the v1 → v2 divorce, and lost exactly the way `block_pool` was** — v1's corpus
taught it, the corpus was discarded for teaching false engine facts, and nothing audited the half
that was true.

**K3 · `ne` runs in the engine and the importer will not let you write it.** The negated form of the
field's commonest gate is ordinary in the corpus (`$robinromance isnot 1`). Our runtime implements
it — `compare()` at `v2.py:3848`, reached by trait conditions at `v2.py:3956`, and already rendered
at `v2.py:1926` as *"label not N"*. The importer rejects it at `template_import.py:5414`, with a
second whitelist at `:5227` and an `op_map` at `:5969` that has no `!=`. **Three whitelist entries
and no runtime work.** Not applied — an engine change is LO's call, not a study section's.

**K3b · `the-first-hour.md` F1's opening band, deleted rather than re-derived.** The recheck opened
it; K could not close it. Three rebuilt walkers — stop-at-first-branch, greedy first link, and
breadth-first to depth three — each land on two or three of F1's six published openings and miss the
rest by four to seven times (`corpo-life` published 64, walkers return 26 / 1,586 / 3,026), **and
they disagree with each other.** The original walker is not on disk. So the word ranges are gone,
along with the two other figures from the same walk — *"ten of twenty openings name nobody"* and
*"~229 words per named character"*, the cast figure going because `destroyer` alone moves from
naming nobody to naming four. **The rule loses nothing**: it was always a consistency rule between
cast load and word budget, and the axis separating the two shapes is the cast, which a reader can
check by opening the first passage.

### What changed on disk

| file | change |
|---|---|
| `references/the-surfaces.md` | **R5d · a gate asks one of two questions** — new rule, K1's shape table, the stage-counter finding, the v1/v2 split, and the cost of the flag pile (the arc is not a value you can print). Plus a paragraph in "What is checked" saying why it is not gated |
| `SKILL.md` | **the fifth commitment — the machinery colours far more than it locks** — the synthesis, with the six field numbers behind it and K2's table |
| `references/engine.md` | **§37 · `ne`** — the runtime/importer mismatch, cited both ways, on the do-not-author list until the importer changes. Notes the same mismatch in miniature on flags (`exists`) |
| `references/the-first-hour.md` | F1 rewritten — table loses its `words` column, gains a block recording what was deleted and why, three-walker evidence inline. Cheat sheet line updated |
| `templates/first-hour.toml` | the A1/A2 menu loses `60-300` / `700+` and says the shapes are separated by who is named |
| `scripts/gates.py` · `scripts/genre_words.txt` · `references/register.md` · `templates/board.toml` | the five contradictions below |
| `STATUS.md` | K row → DONE; *"Ten are done"* → all eleven; the study declared closed; the recheck's residue list extended with the `gates.py` twins K found; a new block recording the four contradictions; PART 2's `board.toml` line corrected |

### ⚠️ Five numbers in this skill were arguing with themselves, and three were mine

Every figure the recheck moved was swept for a second copy that did not move with it.

| the stale copy | the live one |
|---|---|
| `gates.py:1917` *"easier than 24 of the 25 field games"* | `register.md:544` *"easier than 26 of the 27"* |
| `gates.py:5180` *"2 in 92,226 across 25 sandboxes"* | `the-clock.md:403` *"24 in 84,009"* — which names the old figure explicitly |
| `templates/board.toml:80` *"14 of 25 field games have none"* | `the-board.md:243` *"15 have no player ascent tier"* of 27 |
| `SKILL.md:215` *"fewer than four of the 25 field games"* | `gates.py:1769` and `genre_words.txt`, both rebuilt on 27 |
| `genre_words.txt:11`, `gates.py:1776`, `register.md:640` — *"rebuilding on 27 ADDED 1,976 words"* | the file's own line count: 18,043 → 20,555 is **+2,512**. 1,976 is the sub-figure from the two newly-readable games, quoted as the total |

The first three were introduced by the recheck the previous day: it updated the reference file and
missed the comment sitting beside the same number. **`templates/` was never swept by the recheck at
all**, which is how the third survived. The fifth is arithmetic and was checkable against the file
the whole time.

⚠️ **And PART 2's inventory claimed `templates/board.toml` "parses". It does not, and never did** —
`<tier_1> = 0` is a placeholder, not TOML, and it fails at HEAD too. That claim predates the recheck.

**The rule this adds, and it is cheap: when a number moves, grep the number, not the file.** Three of
the five exist because one side of a pair was edited.

### What K deliberately did NOT ship

- **No gate and no lint.** A colour-versus-lock lint was scoped, pitched, and cut on evidence: B's
  35% is measured over *conditionals wrapped around an action*, a strict subset, and our block-level
  prose conditions are not wrapped around actions at all. Building a comparator across two different
  populations would mean choosing the definition after seeing which way it points — the exact fault
  section F caught in itself (`findings_F_further.md` §0.5). **The distinct-gate union stays at 42.**
- **No engine change.** §37 is documented, not applied.
- **No claim that a stage counter is better than a flag pile.** It is what the field does; R5d names
  the one concrete cost of our version and stops there.
- **No claim that we gate too much.** No section measured a defensible ceiling and K adds none.
- **Nothing in `games/`.** `issue.md` and `games/vesper/.find-media/*` belong to a concurrent
  session and were not staged.

### The synthesis, which is what K was for

None of the eleven sections said this and all of them measured it:

```
reputation refuses                 2%  of 644 read sites                  H
the body refuses          median  10%  of its reads                       I
her willingness gates              6%  of act links                       F
act links with no gate at all     47%  of 7,598                           F
refusals that render nothing      71%  of 16,167                          B
conditionals around an action     35%  select a variant · 23% refuse      B
```

**The field's systems colour far more than they lock.** Reputation does not stop her entering the
bar; it changes what the barman says. Ours are the inverse — 56% threshold, 37% boolean, both
locks — and two things already known separately fall straight out of it: **gate 42 exists** because
our locked doors are mute, and **`block_pool` is documented in four places and used by zero v2
games**, because our doctrine has been building access control rather than variation.

⚠️ **What eleven sections did not produce.** PART 3 step 7 asked how we measure a *good* game. The
answer is still **we do not.** Every section measured what the field *does*; the two things that
ever moved this skill's quality both came from LO playing a game for an hour. K adds a frame, not a
score.

**Verified.** Fresh baseline over all 21 scorable games captured before any edit, re-run after:
**byte-identical**, 328 PASS / 223 FAIL / 337 n/a, and the distinct-gate union confirmed at **42**.
K touches only comments in `gates.py`, so any diff at all would have been a defect. `probe_K.py`
re-run end to end: 2,306 menus · 3,346 act gates · 155,765 field conditions · 3,028 of ours ·
the three-walker table. `templates/first-hour.toml` still parses; `templates/board.toml` still does
not, as it never did.

---

## 2026-08-24 — The end-of-study recheck: one constant moves, one shipped figure was never reproducible, and F1's opening table stood on truncated walks

**Why.** Every field number in this skill was measured on **25** of the mopoga corpus's 28 files.
Section B then found three faults underneath them: `college-daze` and `free-cities` ship the Twine 1
`<div id="store-area">` container and parsed to **zero** passages (the field is **27**); that
container's `\n` escapes were never decoded; and `tw.links()` dropped setter links
`[[label|Target][$x += 1]]` and raw `<a data-passage>`. LO deferred the recheck to the end of the
study, and K depends on it. This is that recheck. Evidence:
`~/Documents/Female_PC_Craft_Study_20260823/findings_RECHECK.md`, instruments `recheck.py` and
`dialogue.py` in the same directory. Neither is under git; this entry is their only record.

**Method — reproduce before re-measuring.** The 2026-08-18/19/22 measurement scripts are **not on
disk**; they were run inline and discarded. So each instrument was rebuilt from its own documented
description and **first re-run on the original 25 games against the number that shipped**. Without
that step a moved number cannot be attributed to the corpus rather than to the rebuild. Five
reproduce exactly or near-exactly — clock references (1.1 / 2.1, *exact*, using `gates.py`'s own
`_clk_refs`), speaker macro is the #1 macro (7 of 25, *exact*), renders dialogue through a speech UI
(20 of 25, *exact*), link labels (64,781 against 64,594), `genre_words` (18,574 against 18,043).
Three do not and were used only to measure **movement**, never to replace an absolute:
narration:dialogue, explicit-screen media, currency dominance.

### One gate constant moves

`lint_clock_in_prose`'s `FIELD_MEDIAN, FIELD_P75` — **1.1 / 2.1 → 0.8 / 1.8**. The old pair
reproduced *exactly* on 25 games with the same `_clk_refs`, so this is the corpus and not the
instrument. Both newly-readable games are clock-quiet (0.25 and 0.27 references per 10k). It moves
**against** our games: `off_season` at 26.4 was 24x the field median and is now 33x.

### One shipped figure was never reproducible under any filter

`FIELD_LABEL_LONG_SHARE` shipped as **0.10** against a stated basis of 64,594 labels on 25 games.
That basis reproduces to 0.29% and the median reproduces exactly at 3 — but the share at six or more
words is **16%**, and no filter tested yields 10% while also yielding a median of 3 (all-labels
gives 8.7% at a median of 2). Corrected to **0.21** on 27 games, with the non-reproduction recorded
in the constant's own comment. The likeliest reading: the median was taken on the 2+ set and the
long share on the whole set.

### Four gate constants hold

- `NARRATION_DIALOGUE_CEILING = 5.0` — both new games are narration-heavy (5.9:1, 9.7:1) and both
  sit above the ceiling, so **neither count moved**: 10 of 25 → 10 of **27**, 18 of 25 → 18 of 27.
- `FIELD_METER_RUNGS = 8` / `FIELD_METER_FIRST_RUNG = 5` — `free-cities`' `$rep` is a real player
  ascent meter at **17 rungs**, landing exactly on the existing maximum. Band and first rung
  unchanged; the constant reads rung COUNT, and `rep` runs 1000..12000 on the arcology's own scale.
- `FIELD_DOM` / `FIELD_EXACT` — `free-cities` names no currency, `college-daze` is 99.9% `dollar`.
- `EXPLICIT_BEAT_MEDIA_FLOOR = 50.0` — rebuilt per-screen share moved **up** (84% → 86%) and
  words-per-clip held (51 → 57). The floor stays generous.

`the-meters.md:553`'s body-system gate shares need no recheck: section I already read all 27.

### `scripts/genre_words.txt` rebuilt — 18,043 → 20,555

The list said "four or more of the **25** games … 10.6M words". On 27 the corpus is **14.7M words**
and 214,559 distinct words. Rebuilt as a **UNION with the old list, never a replacement** — a full
27-game rebuild would drop 5 words (`cola`, `gil`, `png'`, `sit-ups`, `upskirt`) on tokeniser noise,
and nothing has ever been removed from this file. **+2,512 words**, 1,976 of them vocabulary the two
unread games use that the lint was reporting as words the genre does not reach for. Visible in the
lint immediately: `off_season`'s flagged-word count fell 231 → 213, `the_season`'s 117 → 104.

**The curated list survives and gets stronger.** All eleven words `register.md` names as appearing
in zero of 25 games appear in **zero of 27 across 14.7M words** — checked directly against both new
games' prose, not inferred from a frequency table. `the-voice.md`'s `lodger` holds on the same
evidence.

### Counts whose numerator holds and whose denominator moves

`register.md` 20 of 25 → **20 of 27** (speech UI) · `engine.md` 7 of 25 → **7 of 27** (#1 macro) ·
`engine.md` 17 of 25 → **18 of 27** (cast page — `college-daze`'s `Check Contacts` is a phone
contact list, one row per person gated on 43 `$met_*` flags, with a `(*NEW!*)` badge; `free-cities`'
`Starting Girls` is a purchase screen and does not count) · `the-first-hour.md` 16 of 25 → **17 of
27** (meeting state) · `the-meters.md` 12 of 25 → **13 of 27** (sexual-state gate) · `state.md` 14
of 25 → **15 of 27** (no player ascent tier) · `register.md` easier than 24 of 25 → **26 of 27** ·
`the-surfaces.md` 64,594 labels → **84,009**.

`college-daze` is worth naming under the arousal row: its sexual-state meters are **per character**
— 29 of them, 179 read sites — and they gate at **51% and 88%**, far above section I's 14% field
median. They are also small. That is section I's own law arriving from a game section I never read:
**small and gating, or large and colouring.**

### `the-clock.md` C2 — the count shipped as 2 and it is 24

"Across 92,226 link labels in the same 25 games: **2** name a clock time, **0** promise one as the
outcome." Re-scanned across **84,009 action labels in all 27** with the corrected extractor: **24**
name an absolute clock time — 6 wait/alarm actions, 7 stated windows, 6 chapter markers in one
linear game, 5 narration fragments used as labels. **The load-bearing zero is unchanged**: not one
is a repeatable canvas promising to end at a named hour. Also recorded there: **a duration in
parentheses is not a clock time** — DoL prints `Bathe (0:30)` as the minute cost, which is C1 done
right, and a naive scan returns 4,282 instead of 24.

### The finding that matters — `the-first-hour.md` F1 rests on truncated walks

**`destroyer` was listed as a 285-word cold open. It is not one.** Those 285 words are its legal
disclaimer, and the walk stopped there because the passage leaves through
`<a data-passage="intro1">`. Walked properly it is **eleven passages, ~3,300 words**, naming the
father, the grandfather (who speaks at length), the stepmother and the school bullies — a **staged
open** by F1's own definition. Moved to the staged row.

It is not alone. Comparing extractors across all 25, **eight openings move and seventeen do not**:
`growup` 26w → 8,132w, `realm-of-corruption` 7w → 2,099w, `amore` 6w → 709w, `wasteland-lewdness`
1,004w → 6,516w, `destroyer` 531w → 3,272w, `the-hellfire-club` 681w → 1,728w, `inseminator`
305w → 582w, `zaras-school-life` 1,173w → 1,482w.

**So F1's two named shapes are sound and the EMPTY BAND BETWEEN THEM IS NOT RE-VERIFIED.** The
300-to-700 gap may be real or may be an artifact of early-terminating walks. This is stated in the
file rather than silently repaired, because **F1's own walker is not on disk** — the numbers above
come from a plain greedy first-link walk that returns 531 words for `destroyer` where F1 published
285, so it is evidence of movement and not a replacement measurement. F1's "ten of twenty openings
name nobody" carries the same caveat. **The rule F1 asks of an author — make the cast load and the
word budget agree — does not turn on the gap.**

### Section C's in-degree table — one row is wrong

Three of four rows reproduce **exactly** (`course-of-temptation` ShowerStall 41,
`degrees-of-lewdity` Hallways 259 / Farm Work 233 / Forest 198 / Orphanage 193, `family-ties`
hall 11 / south 11 / bathroom 9). `zaras-school-life` does not: `School` **46 → 120**, and `Park`
(44) is no longer its runner-up — `Living room` (58) and `Jecinda District` (52) both outrank it.
That game navigates through setter links; bracket links alone move `School` from **14 to 252**.
**C's conclusion survives** — `School` is still the returned-to screen and still a menu — but the
number was understated 2.6x and the second room was wrong. C's table lives in the findings file, not
in the skill, so nothing shipped carried it.

### Sections B, E, F and I needed no recheck

They ran **after** the parser fixes and their own text proves it: `the-meters.md` W6 already names
*"Only `college-daze` … and `free-cities` … run real stacks"*, and `the-first-hour.md` F4b already
counts fourteen openings including both.

⚠️ **And this was nearly filed as a correction.** The first draft of `findings_RECHECK.md` §5
asserted W6's conclusion "was drawn without this game" — it was not; W6 cites it by name. Caught by
reading the file before shipping the claim. **That is the third time in this study a doctrine
citation was suspected and turned out right** (`ginablow` in F, `block_pool` in E). The rule written
after the second one held again, with one clause added: **suspect the instrument, and then suspect
yourself, before the citation.**

A fourth word-boundary failure also nearly landed: the first ascent-meter scan of the new games used
a substring list containing `corrupt`, which does not match `$corr` — `college-daze`'s actual
corruption variable. Caught by dumping the variable census instead of trusting the filter. After
`$groom`, `heather_girlfriend` and `$PlayerCorruption`, this class of bug has now cost four
measurements in one study.

### Files touched

`scripts/gates.py` (six constants/comments plus five stale "of 25" strings) ·
`scripts/genre_words.txt` (rebuilt) · `references/register.md` (8 sites) · `references/engine.md`
(2) · `references/the-first-hour.md` (3) · `references/the-clock.md` (1) ·
`references/the-surfaces.md` (1) · `references/the-meters.md` (1) · `references/state.md` (1) ·
`references/the-voice.md` (1) · `STATUS.md` · this file.

**Verified.** Fresh `gates.py` baseline over all 21 scorable games before any edit, re-run after.
**Verdict tallies byte-identical: 223 FAIL / 337 n/a / 328 PASS, and no gate's verdict moved.** The
distinct-gate union holds at **42** — the recheck adds no gate. Every output diff is one of four
intended kinds: the narration comparator's `10 of 25` → `10 of 27`, the label lint's `10% at 6+` →
`21% at 6+`, the clock lint's `1.1 / 2.1` → `0.8 / 1.8` (and its recomputed multiple, e.g.
`off_season` 36x → 50x), and the genre-word lint flagging **fewer** words now that the list holds
the field's full vocabulary.

---

## 2026-08-24 — Section F lands: the field ships the cheap loop, and my instrument flattered my own conclusion

Section F asked how escalation continues once she says yes. C had answered half — the loop screen is
a menu and the menu options are the ascent ladder. What was open was the rungs and the spacing.
Evidence in `~/Documents/Female_PC_Craft_Study_20260823/findings_F_further.md`, new instrument
`probe_arc.py`.

### What the field does

```
act menu width      median 2 options   p75 3   p90 5   max 54     (n = 2,292 menus)
span across talk>watch>strip>touch>oral>sex>anal>rough>group   median 1   p90 4
carries a finish option                                         9%
arc hubs (10+ acts) n=61 · median 15 acts but only 3 KINDS
   1 kind x17  2 x11  3 x10  4 x9  |  5 x8  6 x4  7 x1  8 x1
   47 hubs run one to four intensities · 14 run five or more
```

**A menu offers two neighbouring things** — `touch` beside `oral`, never `talk` beside `sex`. Checked
against the counting artifact: recomputed by menu size, four-to-five-option menus still sit at span 0.

**And the field mostly ships the cheap shape.** `the-surfaces.md` R3b already offered exactly the
right three loop shapes and gave none of them a number; it introduces the **single-act loop** as *"the
cheapest loop that is still a loop"*. The measurement says it is also **the common one**, and the pose
ladder is the minority. That is the one change in this section that alters how a game gets built — a
shape presented as the cheap option and a shape presented as the target are chosen very differently by
a tired author. Going further mostly means **more variations at the same intensity**, which is
`register.md`'s *"what varies is the REASON, not the act"* arriving from the menu side.

### F explains E rather than contradicting it

Of **7,598** act links across thirteen games, **47% carry no condition at all** and **2% are gated on
the per-person willingness meter**. Among the conditions that do exist, the **player's own ascent
meter gates 13% and hers gates 6%**.

So E's per-person ladder can be three rungs deep because **it is not carrying the escalation** — the
player's meter is, at W4's 8–17. Her meter says whether this person is available; the player's says
how far the game has come. W6 gains that sentence; nothing else in the skill moved.

### ⚠️ The instrument was wrong twice, and the second fault biased toward this section's own conclusion

1. **A length filter ate the genre's most important label.** `labels()` ended with
   `len(x) > 3`. **"Cum" is three characters** — so are "sex", "eat", "beg", "yes", "no". **825
   dropped label instances** across six games, 73 of them `cum`.
2. **The act vocabulary was too narrow.** `\bblow\b` does not match "blowing"; `pussy`, `tits`,
   `pound` and `thrust` were absent entirely, so "Pound her pussy" classified as nothing. **A
   classifier that cannot see an act undercounts kind-diversity, which makes every hub look shallower
   than it is — the exact direction of the conclusion above.** It had to be tested before the
   conclusion could be trusted.

Re-measured with stems and the body nouns in:

```
                        narrow      widened
act menus visible        1,564   ->   2,292
menu width med / p90       2/5   ->     2/5     unchanged
span med / p90             1/3   ->     1/4     unchanged
arc hubs                    45   ->      61
median kinds per hub         2   ->       3
hubs reaching 5+ kinds  8 of 45  ->  14 of 61
```

**The conclusions survived; two numbers moved.** The doctrine landed on the widened figures.

### ⚠️ R3b was right where I thought it was wrong — the second such near-miss this session

R3b quotes `destroyer:ginablow` as *"five exits — Keep blowing · Pound her ass · Pound her pussy ·
Cum · Go back."* My extractor returned four labels with no `Cum`, and I was one step from filing a
citation correction. **The passage has all five, exactly as quoted.** The filter was dropping
`[[Cum|ginacum]]` and the vocabulary was failing to classify two of the other three. The quote is
kept verbatim and `ginablow` is now the instrument's regression test: 3 acts, 3 kinds, span 2.

Section E did the same thing to `engine.md` §35's `block_pool` census and had to un-correct it.
**Twice in one session a doctrine citation was suspected and turned out right. When a citation looks
wrong, suspect the instrument before the citation.**

### What changed

- **`references/the-surfaces.md` R3b** — a new subsection carrying the measured menu width, the
  61-hub depth distribution, and the sentence that the single-act loop is what the field ships. The
  `ginablow` quote is untouched.
- **`references/the-surfaces.md` R3c** — one line marking Gabby's eight-rung ladder as the minority
  shape it is: 14 of 61.
- **`references/the-meters.md` W6** — one paragraph: three rungs is enough because this meter gates
  6% of act links while the player's gates 13% and 47% are ungated.
- **`references/the-surfaces.md` "What is checked"** — R3b's numbers join the deliberately-not-gated
  list, with the spread as the reason.
- **`probe_arc.py`** — both faults fixed, each with the measurement inline. Outside the repo and not
  under git, so this is the only record.

### No gate, no lint

Nothing in section F defends a threshold. Menu width runs 2 to 54 and hub depth splits 47/14 with
working games on both sides. **Registry stays at 42 and `gates.py` output is byte-identical on all 21
games** — for this section any diff at all would have been a defect.

### Also

`STATUS.md`: F row → DONE with the headline; "Nine are done" → **"Ten are done"**; remaining is **K
alone**. The K row gains section F's one open input — the **48%** of act-gate conditions this
instrument could not name are each game's invented vocabulary, and classifying them by *shape* rather
than domain (section B's move, which took its own residue from 71% to 0.4%) would probably name most
of it.

**No spacing number was produced, deliberately.** Only two arcs in the entire corpus space acts along
a meter — `friends-of-mine`'s Gabby and her father. n=2 is not a field, and the honest answer to the
question `STATUS.md` had open is that **the field does not build escalation as a spaced ladder at
all.**

---

## 2026-08-24 — Section E lands: one word for the whole cast, and W6 had been teaching the opposite

Section E asked how she gets from no to yes. D had answered half — refusals cost money and standing.
What was open was the systematic view. Evidence in
`~/Documents/Female_PC_Craft_Study_20260823/findings_E_yes.md`, new instrument `probe_ladder.py`.

### The measurement

Across the twenty corpus games that carry a willingness meter, **sixteen track it per person** and
three run one global meter. What the field does with those per-person meters is the finding:

```
median meters per person, 13 games              1
become-someone   trust     62 of 64 people     patriarch        like      37 of 38
destroyer        relation  45 of 57            friends-of-mine  relation   5 of 5
median rungs per person                         3   (p25 2, p75 6)
threshold values used by two or more people    88%  (range 41-99)
`+1` share of raises, in the games that climb  71-76%
```

**One word for the whole cast, on one scale.** The difference between people lives in *modifiers* on
that number, not in giving them different vocabularies — `inseminator`'s six relationship traits are
coefficients on one affinity value, and `become-someone`'s shared nudge carries a gift that belongs to
one person (a locket for Kate, lingerie for Jade) on the `trust` all 62 of them share.

### ⚠️ W6 taught the opposite, and our newest games show the cost

`the-meters.md` W6 read: *"For a **roster** game it is the engine, and an identical pair on everyone
is the engine missing. Pick each character's gating meter from what the relationship is."*

That produced `off_season` — four characters, four vocabularies (`hold` · `ease+want` · `bond` ·
`trust+want`), nothing shared. It also made W6 contradict itself two paragraphs later, where it
correctly says to reserve the rich model for the one or two arcs that carry the game. `vesper` is the
shape that was always right: `relation` on eleven, the rich triple on four.

And it made W6 criticise `the_season` for the wrong thing. Wade and Prine **sharing** `{ease, want}`
is the field's own practice; `the_season`'s real defect is the W6 rule that stands — **Rae carries no
meter at all**.

LO's call was to **reframe, keeping the table**: it no longer picks a meter per character, it picks
the game's one word. The old conclusion is kept visible as superseded, per the §15 precedent. The
last table row survives as a genuine per-character exception — someone she already belongs to gets no
climbing meter.

### The lint was comparing cast meters to a player-ascent number

`lint_meter_ladder` forks on `board.who_climbs` exactly as W4 describes, then printed the **same**
comparator on both branches: `field 8-17 rungs, lowest at 5`. That 8–17 was measured on the one meter
that carries a game — `you.corr`, `feminine`, `lust`, `mc.dom` — and is the wrong yardstick for a
per-character meter, where the field's median is **3**.

`off_season`, the repo's only roster game, was being told its five-rung cast meters were three short
of eight when they are already above the field's per-character median. Fixed with a second set of
constants used only on the cast branch, measurement inline beside them (`gates.py:1594-1613`). W4's
prose gained the same split.

**No gate was added or changed.** Registry stays at 42. Diffed against a fresh baseline on all 21
games: **exactly one line moves, in exactly one game** —

```
- lint · the meter ladder — 6 cast meters · median 5 rungs · lowest rung 4 · field 8-17 rungs, lowest at 5
+ lint · the meter ladder — 6 cast meters · median 5 rungs · lowest rung 4 · field 2-6 rungs (median 3), lowest at 5
```

### `the-surfaces.md` gains R3c — the ladder across visits

R3b owns the ladder *inside* one visit; this is the ladder *across* visits, the same screen re-entered
for days with its menu growing. Worked example is `friends-of-mine`'s Gabby arc: one screen, one
meter, 0 → 24, forty-nine gated actions. Four mechanics — each act written twice then surviving on
`>=`; doing the act is what raises the meter; give and take arriving on one rung; and three rungs that
are not acts at all but **conversations in which she says why not yet**, each sitting immediately
below the next escalation.

That last one is the section's answer and nothing in this skill had a name for it. She never refuses
out loud — the act simply is not on the menu, which is section B's silent 71% — and three times on the
climb the game spends a whole scene letting her explain the pause.

Labelled a worked example, explicitly one game at rank 25. **No gate, no lint** — the field's rung
spread is 1 to 25 and nothing there defends a threshold.

### Four instrument failures, and two of them were mine on the same paragraph

1. **600 of become-someone's `.trust +=` writes are five cheat pages** bumping all 24 girls at once.
   In play the meter is written 152 times, not 617. Chrome is excluded everywhere.
2. **`$PlayerCorruption` was read as person "Player"**, which would have reported zaras-school-life —
   the corpus's clearest *global*-meter game — as per-person. `$heather_girlfriend` was read as
   person `heather_girl`. Fixed by excluding player prefixes and matching the willingness words
   longest-first.
3. **A bare `=` matched inside `==`**, reporting college-daze raising `love` at 3,408 sites against
   13 from the correct pass.
4. **The word list missed the abbreviation `corr`.** become-someone reads it 268 times and runs a
   genuine pair on 47 of 64 people; the first pass called it one meter. The corpus median is still 1,
   but the headline was wrong for the game it leans on hardest.

**Not fixed, stated:** three games hold the meter behind a pointer — `$activeSlave.devotion`,
`$girl.maxLove`, `$tmpGirl.relationship`. Per-person at runtime, one holder to a static reader.
`new-lust` is probably miscounted as global and free-cities' six holders are an undercount.

### ⚠️ engine.md §36 overstated §35, and my first correction of it was also wrong

§36 called `rejection_node` *"the same shape as `block_pool` (§35): a working primitive that nothing
taught, so nothing used."* **`block_pool` is authored 69 times across four games** —
`the_long_summer` 49, `vesper` 12, `under_one_roof` 7, `the_long_summer_test` 1.

I first wrote that this made §35 false. **It does not.** §35 says *"no **v2** game has ever used
it"*, and none of those four carries a `v2_state.json` — all four are v1-era, which is exactly why
§35 is phrased that way. What is wrong is §36 **dropping the qualifier**, turning a true narrow claim
into a false broad one. §36 corrected; §35 left alone.

Two failures in one paragraph, both mine: repeating a doctrine sentence as evidence without checking
the repo, then over-correcting because I checked against a paraphrase instead of §35's own words.
**Checking the repo is not enough if you then check it against a paraphrase.**

### Also

`STATUS.md`: E row → DONE with the headline; "Eight are done" → "Nine are done: A, B, C, D, E, G, H,
I and J"; remaining sections are now **F and K**. Gate count unchanged at 42.

Not proposed and deliberately so: `<<katetrust>>`-style named nudges — 147 widgets, 1,606 call sites,
each carrying base amount, the player's charisma, a per-person gift and its own player-facing line —
are a **tooling** observation, not a doctrine gap. Recorded in the findings only.

---

## 2026-08-24 — Section B lands: day one refuses nothing, and this skill taught the one shape the field never ships

Section B asked what day one refuses to let her do, and how it says no. Evidence in
`~/Documents/Female_PC_Craft_Study_20260823/findings_B_refusal.md`, with two new instruments,
`probe_gates.py` and `probe_open.py`.

### The method had to be rebuilt, because a refusal is not a phrase

The first pass swept passage prose for refusal words and matched **6,392 times in college-daze
alone**. Sampling killed it: `you need` is overwhelmingly dialogue (*"you need to be more responsible
and professional"*), and `refuse` is as often a changelog line or an NPC refusing a third party.
Same class of error as `$groom` in the-hellfire-club turning out to be a bridegroom.

**A refusal is a POSITION** — the branch of a conditional where the action would have been. Every
number below comes from finding that position and reading what is in it.

### The headline, and the fourth arrival of the same law

Across 26 shipped sandboxes, **27,505 conditionals wrap an action**:

```
swap        9,776  35%   every branch acts — a variant selector, nothing refused
silent     11,627  42%   a branch offers nothing and says nothing
spoken      4,540  16%   a branch offers nothing and says <=25 words in its place
alternate   1,562   5%   >25 words — different content, not a no
```

**Only 23% refuse anything.** Of the 16,167 that do, **71% render nothing at all** (per-game median
79%, range 22–100%); the 28% that speak run a **median 9 words** and **60% name a handle** — a price
37%, *already done* 18%, a time 5%, a place **2%**. Price is the field's answer; the refusal is not
where these games do their wayfinding.

That is H (reputation gates 2%), I (the body gates a median 10%) and G (differentiation is many small
swaps) reached a fourth time, and the first time from the **choice** side rather than the meter side.
`SKILL.md`'s convergence bullet updated from "a third time" to "a fourth time" with the 35/23 split.

**Day one refuses nothing.** Twelve of fourteen identifiable openings carry zero spoken refusals,
Course of Temptation's 78-passage, 8,057-word prologue among them (seven conditionals, no refusal).
The two exceptions are tags covering a tutorial and a settings screen. The opening hands over a bill;
it does not lock a door.

### ⚠️ The real finding is that this skill caused the defect it was about to gate

`engine.md` §15 read, until today:

> *"omit `locked_text` and the greyed row shows the action […] a want the player can name, which is
> what sells the next release […] **Prefer the want unless the gate is genuinely obscure.**"*

Our games obeyed it: **13 of 176 shown-locked choices across every merged game carry a reason — 7%.**
The field's answer is that a refusal is **either invisible (71%) or it speaks (28%)**, and a visible
**mute** label is **2.26%** of 4,513 spoken refusals — nearly all of it settings and pagination chrome
(`OptionsWidget` toggles, `Widgets Outfits` "Previous"/"Next"). §15 recommended the one shape the
field does not ship.

It also put this file in **direct conflict with `the-surfaces.md` R5b.2** — *"State the bar with
`locked_text_threshold`; never fail silently"* — written the same day. LO's call was to **reverse
§15**, not qualify it. The old advice is kept visible as superseded with the measurement beside it,
because it shipped with a live verification behind it and deleting it would hide why every game
scores the way it does. The two files now agree.

### What changed

- **`references/engine.md` §15 — reversed.** `locked_text` is the default; the bare label is a rare,
  argued exception. Keeps the verified render fact and adds what actually happens without it:
  `escaped_locked = (locked_text or choice_text)` (`v2.py:13171`), with the same string repeated into
  the `title` tooltip (`:13219-13220`), so the tooltip adds nothing.
- **`references/engine.md` §27 — scoped, not corrected.** Its claim that an unaffordable rung *"is
  not offered"* is true of the canvas pickers (`v2.py:4496`, `:4527`, `:4975`) but **not** of
  exit-block choices, which open `<<if setup.checkCostsAffordable(...)>>` (`v2.py:13014-13015`) and
  write an `<<else>>` that keeps the row greyed with the requirement appended by the engine
  (`v2.py:13159-13166`). **A priced choice explains itself with no authoring at all**; a condition
  does not. That asymmetry is the section's engine finding and had no home.
- **`references/engine.md` §36 — four stale citations fixed**, all of them wrong on the day §36 was
  written: `13146`→`13171` (label fallback), `13148`→`13173` (the Mode B comment, entered from
  `13172`), `13185-13186`→`13210-13217` (the threshold button), `template_import.py:811-812`→`:825-826`
  (class at `:806`, read at `:2204`). Also recorded that `rejection_node` **is** build-validated —
  `template_import.py:4616-4624` raises on a node outside its own canvas — which is stronger than
  §36's fail-open warning implied.
- **`references/the-first-hour.md` — new F4b, "The opening refuses nothing."** Beside F4 because it
  is the constraint F4 implies and never states: teach the system, do not gate on it yet. Carries the
  12-of-14 table with both exceptions named.
- **`references/the-surfaces.md` — new R5c, "A locked door says why,"** placed after R5b.2, which
  reached for `locked_text_threshold` and stopped one step short of saying what the row should look
  like. Carries the measured shape (stands where the action stood · ~9 words · names a handle ·
  marked as the game's own voice) and patriarch's `schoolgirls` roster verbatim, which does all four
  at once on a **cast page**. **R5 gained a qualifier** in the same pass: a condition on a choice is
  usually a variant, not a lock, and R5 is not a licence to gate.
- **`scripts/gates.py` — new gate 42, "a locked door says why."** Registry **41 → 42**.

### The gate

Categorical, not a ratio, and the measurement is why: the field's mute share is ~2% and it is UI
chrome, so there is no threshold to invent. `n/a` when a game authors no `show_when_locked` choices.
Accepts three reasons — `locked_text`, `locked_text_threshold` (the label becomes a `<<button>>`
firing `setup.queueGatedNotification(...)`, `v2.py:13210-13217`, so the reason is one click away) or
`rejection_node`. **A choice gated only by `costs` is never counted against a game**, because the
engine writes that message itself.

Verified against every game with a merged final, baseline diffed:

```
12 FAIL   forty_miles 30->0 · the_inheritance 27->0 · seventh_day 25->0
          the_long_summer_test 24->0 · vesper 13->9 · back_home 8->1
          the_allowance 8->0 · last_call 7->1 · steam 5->0 · off_season 4->0
          mothers_place 3->0 · the_season 1->0
 1 PASS   late_shifts 21->21   (all of it locked_text_threshold, v1-era)
 8 n/a    no show_when_locked choices authored
```

**No existing gate's verdict moved** — every remaining diff line is the tally denominator, plus
`late_shifts`'s numerator for its pass. `the_season` and `off_season` go 39/40 → 39/41.

Two predictions in the findings file were wrong and are left visible there with a correction block:
**`vesper` does not pass** (best in the repo at 9 of 13, still four mute rows, scored red and not
touched per the standing rule), and the floor was **not** argued from the 60% handle rate — that is
the share of *spoken* refusals naming a handle and says nothing about how often a refusal should
speak. The n/a count is **8, not the 13** a TOML scan implies, because `gates.py` reads only
`7_final_game.toml` and five games still carry a `6_final_game.toml` it never opens.

**B-5 was withdrawn.** It proposed recording that `rejection_node` is unused; `engine.md` §36 —
written earlier the same day — already censuses it at zero and names it as a primitive nothing
taught. Same call as I-2 folding into W3 last section. The findings file's `rejection_passage` was
also corrected throughout: that is the **generator's internal variable**, and the field an author
writes is `rejection_node`.

### Three doctrine claims were false and are corrected

`engine.md` §32.3, `the-clock.md` C5 and `the-surfaces.md` R2 all stated that **no game in this repo
has ever used `show_when_blocked`**. `off_season` uses it **six times**, with the hours written out
in its own words — *"mornings, eight till one"*, *"after nine at night"*, *"the last two hours,
before the shutter"*. Found by the cross-reference grep this section runs to check no two files claim
the same rule, verified with `tomllib`, and fixed in all four places. Not a stale line number — a
claim about the repo that had gone false and would have taught the next author wrong.

### The instrument was fixed twice more, underneath earlier sections

Both live in `~/Documents/Female_PC_Craft_Study_20260823/tw.py`, which is outside the repo and not
under git, so this is the only record:

1. **Store-area escapes were never decoded.** Twine 1 writes a newline as the two characters `\n`, a
   tab as `\t` and a backslash as `\s`. 9,221 `college-daze` passages carried **0 newlines and
   5,620 literal `\n` tokens**; every word count on that game and `free-cities` was inflated by the
   escape tokens, and any `[^\n]`-bounded regex ran the length of the passage. Decode order matters —
   `\s` last, or the backslash it produces is re-read. **Section I ran before this fix.**
2. **`tw.links()` dropped every setter link.** `\[\[([^\]]+)\]\]` cannot cross the `]` inside
   `[[Get out of bed|Room][$minute += 1]]`, so the link did not match at all and its target was lost;
   raw `<a data-passage="…">` navigation was invisible too. **This is what the in-degree hub ranking
   and `the-first-hour.md` F1's opening-funnel walk were built on.** Fixed with a balanced scan plus
   a `data-passage` pass.

`STATUS.md` records both under the deferred end-of-study recheck, which they widen.

### Also in `STATUS.md`

B row → DONE with the headline; `41 gates` → `42 gates` at both sites; "Seven are done" → "Eight are
done: A, B, C, D, G, H, I and J"; remaining sections are now **E, F and K (the synthesis, last)**.
`17 lints` left alone — this section did not measure it.

---

## 2026-08-24 — Section I lands: the body, and the field's answer is mostly "don't build it"

Section I asked which of clothes, arousal, hygiene and pregnancy are systems and which are
decoration. Evidence in `~/Documents/Female_PC_Craft_Study_20260823/findings_I_body.md`. Method was
section H's, deliberately, so the numbers are comparable: count writes (`<<set>>`), count reads
(`<<if>>`/`<<elseif>>`), then split every read by what its consequent does — **gate** (a link, a
`goto`, a button), **state** (only `<<set>>`), or **colour** (prose only).

### The headline is negative, and it is the strongest thing in the section

`degrees-of-lewdity` — rank 7, 15,626 passages, the game everyone points at for body simulation —
**built hygiene and switched it off.** It writes `$hygiene` 1,273 times, 1,207 of them the identical
`<<set $hygiene += 500>>` scattered through the world. It reads it at **one** site: a seven-rung
`if/elseif` ladder inside `<<widget "hygiene">>`. Nothing calls that widget. The string `speckless`
appears exactly once in the whole game — inside it. And the initialiser says so outright:

```
<<set $hungerenabled to 0>>  /* unused */
<<set $thirstenabled to 0>>  /* unused */
<<set $hygieneenabled to 0>> /* unused */
```

`free-cities`, the corpus's deepest body simulator, never modelled hygiene or arousal at all — its
slave objects carry `vagina`, `dick`, `boobs`, `anus`, `balls`, `butt`, `health`, `preg`, and its
two most-read properties are `devotion` (1,019) and `trust` (667), above every body part.
Corpus-wide hygiene is the rarest of the four: **234 read sites against arousal's 8,183**.

### Changed — `references/the-meters.md`

**New W7 · the body's meters are read to colour, not to refuse.** W5 is the counterweight, W5b the
audience meter, W6 the cast's gating meters; the body is a fourth shape and behaves like none of
them. Across 25 (subsystem × game) systems the median gate share is **10%** — clothes 8%, arousal
14%, pregnancy 7% — and 17 of 25 gate under 25%. The exceptions are named and they are all *small*
systems (`new-life-project` 91% of 43 reads, `wasteland-lewdness` 63% of 35, `patriarch` 47% of 34),
which is the rule underneath: **a system either stays small and gates or grows large and colours;
nothing in the corpus is both.** Carries the band-ladder mechanic — DoL's seven rungs written once
in a widget against `corpo-life` inlining the identical structure across 5,785 sites — and the note
that the bands say *"Soft boner"*, not `45/100`.

**W3 gains the case it cannot see.** `worn_beauty` / `worn_corruption` are **derived** from a
garment's own declaration, never raised by an `effects` entry, so gate 33 looks straight past a full
catalog. 102 garments in 10 of our games, 47 reads between them, four wardrobes read zero times.

### Changed — `scripts/gates.py`

**New gate · the wardrobe is read.** `n/a` when no `[[clothing]]` is declared; passes when any of
three reader families appears. Modelled on gate 33 and using the existing `_walk_paths` helper — no
new traversal code. Same fig-leaf risk as gate 33 and the same answer: no threshold is invented
(W7 measures the field's median gate share at 10%, so demanding *gates* would be wrong), and the
summary prints garments-against-reads so a thin pass is visible. **Scoreboard is now 41 gates.**

### Changed — `references/engine.md`

- **§17 gains `worn_beauty`.** It was missing from the verified condition-type list, it is real
  (`template_import.py:218`, `v2.py:4044`, `:7821`), and two games use it. The catalog field list
  was also short — `conditions`, `price` and `type` were undocumented.
- **§17 gains "the three ways a wardrobe gets read"**, including the `player_portrait` outfit
  override (`template_import.py:743-745`) named as a *display* reader.
- **§17 records what the wardrobe cannot do**: a worn stat can gate a choice and explain itself when
  it blocks one (`v2.py:7816-7823`), but cannot be a standing sidebar state, because
  `trait_status_text` takes a `trait` and these are derived. **Explicitly not a gap to close** — the
  field does not show the number either, it shows the world reacting.
- **New §30.1 · a hygiene system is a deliberate non-feature.** Placed under `trait_status_text`
  precisely because that primitive makes one authorable in an afternoon — its own spec comment says
  *"Use for hygiene/energy/hunger-style needs that recover on action"*
  (`template_import.py:3685-3690`). Carries DoL's `/* unused */`, free-cities' absence, the 2-of-27
  coverage, and the four of our own games whose `hygiene` trait is already in gate 33's dead list.
  Same register as the per-character dialogue colour in §34: a known difference, left unbuilt.

### Changed — `SKILL.md`

The law arrives a third time from a third instrument and is now stated as one: **a system is read to
change the words, not to refuse the action.** H 2%, G many-small-swaps, I median 10%.

### Changed — `STATUS.md`

I row → DONE. Gate count 40 → 41 in both places. Corpus corrected to **27 parseable games**.
Remaining sections are B, E, F and K. Also fixed a pre-existing line that read *"Four are done"*
above a list of six.

### The instrument was broken in four ways, and three would have shipped as doctrine

1. **An empty variable list matched every variable in the game.** `vp()` built
   `\$(?:' + "|".join(names) + ')\b`; with `names` empty that is `\$(?:)\b`, and the word boundary
   always fires because `$` is non-word and the next letter is not. Every theme specced as `[]`
   reported the whole game's totals — `growup` came out identical across all four subsystems,
   `become-someone` across three. **Caught only because those numbers are impossible.**
2. **⚠️ Three games had never been parsed by this study at all.** `tw.py` only knew
   `<tw-passagedata>`; `college-daze`, `free-cities` and `confined-and-horny` ship the older
   `<div id="store-area"><div tiddler="Name">` container and returned zero passages. **Sections A,
   C, D, G, H and J all ran on 25 games and reported it as the field.** `tw.py` now parses both,
   with a balanced `<div>` scan because a non-greedy `</div>` truncated one 235KB free-cities
   passage to nothing. This mattered most here: `free-cities` is a breeding simulator and
   `college-daze` is the only corpus game that puts a lust meter on every character.
3. **`confined-and-horny` is not a game file.** After the fix it still parses to zero: no
   store-area, no tiddlers, no passage data, **100% script bytes**. The download captured the
   SugarCube engine and none of the story. Excluded with a reason. **The corpus is 27 parseable
   games, not 25 and not 28.**
4. **`$groom` in `the-hellfire-club` is a bridegroom** — `<<set $groom = "Matthew">>` — not a
   grooming system, despite 82 sites. Its real hygiene variable is `$dirty`, at 8 reads. The same
   sweep matched `laptop` on `top\b`, `emailAddress` on `dress`, `barbra` on `bra\b` and
   `changingRoomGender` on `groom`. Every variable in the findings was read in source before it was
   counted.

### And I got our own side wrong, which is what produced the gate's design

The findings first reported *"104 garments, 23 reads"* and named `vesper` as a game that authors
eight garments and reads neither stat. **`vesper` reads its wardrobe 21 times — the most of any game
we have** — 19 through `type = "clothing_item"` and twice through a `player_portrait` override. Its
two `worn_corruption` mentions are *comments* saying it deliberately does not use that axis.

There are **three reader families and I had counted two.** Had the gate shipped on the first count
it would have failed `vesper` for doing the thing W7 had just finished establishing is the field's
dominant mode. Corrected in the findings file rather than quietly overwritten, and the gate counts
all three.

### Refused

- **No new `the-surfaces.md` rule.** The proposal was approved as one, and W3 already owns the law —
  a second statement in another file is the duplication section G's cross-reference pass exists to
  prevent. Folded into W3 plus the gate.
- **No `exposed` derived state.** DoL's is load-bearing because ~900 sites read it; ours would be
  read by nobody until the new gate has changed how games are authored. Right second move.
- **No hygiene system.** That is what §30.1 is for.
- **No lint-count change.** `STATUS.md` says 17 lints; a crude split of the report says 19. This
  task did not measure it properly, so the number was left alone rather than guessed at.
- **No game files touched** — not the four failing wardrobes, and not `vesper`.

### Verified

- Baseline captured for all 21 games before the change. After: **every diff line is either the
  tally line (denominator +1) or the new gate's own output.** No existing gate's verdict moved.
- The new gate lands as predicted: **4 FAIL** (`mothers_place` 6 garments/0 reads, `seventh_day`
  8/0, `steam` 8/0, `the_allowance` 9/0), **6 PASS**, **11 n/a**.
- `vesper` passes *via `clothing_item` ×19 + portrait ×2*, which is the case the first count got
  wrong. `last_call` passes on 1 read for 8 garments and the summary line shows exactly that.
- Distinct-gate union across all 21 games: **40 → 41**.
- `the_season` and `off_season` keep 39/40 — the gate is `n/a` for both, so no score moved.
- Cross-reference: W7 read against W5 / W5b / W6, and the W3 wardrobe paragraph against
  `the-first-hour.md:168` (which is about a system never *taught*, not never *read*).
- The `trait_status_text` citation was written as `engine.md` §34a, checked, and corrected to
  **§30** before it shipped.

---

## 2026-08-24 — Section G lands: the cast, and the first engine field this skill has ever added

**What.** `references/the-surfaces.md` (new **R8**, plus its entry and its reason in the
deliberately-not-gated list), `references/register.md` (**S3** gains the term-of-address rule),
`references/the-meters.md` (**W6** gains the trade rule and a W5 / W5b / W6 cross-pointer),
`references/engine.md` (**§34** gains the `tags` field and a recorded colour difference; three stale
citations fixed), `SKILL.md` (two lessons and a findability pointer), `STATUS.md`,
`references/the-first-hour.md` (one citation).

**And, for the first time in this skill's history, an engine change:**
`apps/projects/services/template_import.py`, `apps/projects/services/game_graph.py`,
`apps/game_generation/twee_comprehensive/generators/v2.py`, plus a new
`tests/test_npc_tags_field.py`.

**`scripts/gates.py` untouched. No new gate, no new lint, no threshold. No game file written** —
not `the_season`, and not `vesper` per the standing rule.

**Why now.** LO played `the_season` and reported one defect: *"I don't know who is who."* That is
Section G's question in a player's words, and it was the only complaint about the game that came
from a human rather than from the scoreboard. Nothing in the 40 gates measures it — all six
cast-adjacent gates (*somebody speaks*, *speakers are named*, *residents have homes*, *a meeting
fires where they are*, *every hub is met first*, *the anchor introduces itself*) are presence and
plumbing checks.

**Scope note.** G was **not** gated on the female-PC screening that shaped A/C/D/H/J. Those sections
are about *her*; G is about *the cast*, and a male-PC game with eight women in it is evidence about
cast craft in exactly the same way. All 25 readable corpus games were used.

### A proposal was made and WITHDRAWN. Recording it so it is not made again.

A 41st gate — *"a declared portrait must resolve to a file"* — was proposed on the strength of a
real finding: `games/the_season/` contains **zero image files**, so all 59 of its portrait `<img>`
tags fire `onerror` and render **one silhouette SVG, 59 times** (verified: `onerror fallbacks: 59,
distinct: 1`). Five men, one grey blob.

**LO refused it, correctly, on the grounds that it already exists.** Verified rather than assumed:
`api/v1/game_review.py:588` enumerates NPC portraits, `:590-604` enumerates the player portrait
including outfit and undress states, and `_extract_missing_media` splits them found/missing. And
`package_from_toml` itself prints the warning at build time — *"5 external media file(s) referenced
but NOT copied … Sidebar portraits / NPC / location images will be BROKEN in this build."*

**So `the_season` has an unrun tool, not a doctrine hole.** It has no `.find-media/`, no
`media_review.json` and no media pass in its history. The lesson generalises: **before proposing a
gate, check whether another surface already reports the thing.** A scoreboard is not the only place
a defect can be caught, and this skill's instinct is to reach for it first.

### The engine change — `[[npcs]] tags`

The field's best cast page is `friends-of-mine`'s Characterpedia: fifteen people, each with a
portrait, a counter, a 27–83-word bio, and **exactly four interests** — all fifteen, no exceptions,
in a consistent shape (how they operate · what they want · an aesthetic · something they consume),
with thirteen of fifteen ending on a food. That trivial fourth slot is what stops the entry reading
as a stat block. `TemplateNPC` had no field for it.

LO was given the fork — ride in `relationship` (doc-only) versus a new field (engine change) — and
chose the field. `relationship` was the wrong home on inspection: for a `customizable` NPC it must
match an entry in `relationship_options` (`template_import.py:4029`), so tags there would break the
player's relationship picker the moment anyone used it.

Shipped: `NPC_TAGS_MAX = 4`, a hard reject rather than a truncation, and delivery through a
**slug-keyed `setup.npc_tags` registry** copied from `setup.npc_arc_stages` — **not** through
`$npcs`, because `$npcs` is snapshotted into every history moment, which is the same reason
`description` is popped at `v2.py:1031`.

> ⚠️ **THE BUG THIS TASK ACTUALLY HIT, AND THE REASON IT IS IN `SKILL.md`.** `ai_behavior_config` is
> written in **two** places. `template_import.create_project_from_template` is the `--use-db` path;
> `apps/projects/services/game_graph.py` is the one a plain `package_from_toml` takes. The field was
> added to the first only, and the result was `setup.npc_tags = {}` in a build whose TOML plainly
> declared four tags — **no error at import, none at build, none at runtime.** It looked exactly
> like a game that had not authored the field. `tests/test_npc_tags_field.py` now locks the no-DB
> path specifically, with the failure message naming the cause.

### How it was verified

1. **`gates.py` output byte-identical across all games**, before and after. ⚠️ A **non-zero exit
   from `gates.py` means a red gate, not a crashed script** — the outputs are compared, never the
   exit codes.
2. **The engine change is inert when unused.** `the_season` rebuilt before and after and diffed:
   **13 lines, all three of them mine** — `setup.npc_tags = {};` with its two comment lines, the
   `.cast-card .cast-tags` CSS rule, and the two `<<if>>`-guarded render lines. Nothing else moved.
3. **The round-trip works when used.** A copy of `the_season`'s TOML with four tags on Boyd builds
   to `setup.npc_tags = {"npc_boyd": ["The book", "The scale", "Saturday", "Black coffee"]}`.
4. **The cap bites.** Five tags is refused at import: *"npcs[0].tags has 5 entries, max 4."*
5. **11 new tests pass** (`tests/test_npc_tags_field.py`).
6. **Every engine line re-read at write time**, and every citation in the new §34 text re-pinned
   *after* the v2.py edits shifted the file — the speaker default moved 14978→**15003**, the
   portrait render 15010→**15035**, the `dialog-npc` class 15017→**15042**.

### Instrument failures found in this section

Recorded because two of them would have shipped as doctrine, and one wasted a verification cycle.

- **`git stash` on a file that already had uncommitted changes reverts those too.** The first
  before/after build comparison stashed the two engine files to get a baseline — but both were
  *already* modified by earlier uncommitted work, so the "before" build was **HEAD**, not
  before-my-edit. The diff showed `CastPage` appearing out of nowhere and looked alarming. The
  correct baseline was built by programmatically reversing exactly the nine strings inserted.
- **A dialogue-share measurement returned 128%.** `tw.prose()` strips `<<...>>` macros wholesale, so
  the speech text was deleted from the denominator while being counted in the numerator. **Only an
  impossible number caught it**; a plausible-but-wrong 45% would have shipped. Corrected figures
  (13.8%–56.2%, five games) agree with the far better-provenanced `NARRATION_DIALOGUE_CEILING`
  already in `gates.py`, and **that constant remains the citable one.**
- **Degrees of Lewdity's 14 "traits" are BEAST traits.** A census returned `territorial`,
  `brooding`, `sociable`, `relaxed`, `cowardly`, `clever`, `clumsy` — a fine human-temperament
  vocabulary, and not one: they are set by `<<generate_beast_traits>>` in `Widgets Beast Generation`
  and gate fox and wolf encounters. Caught only by printing the surrounding source instead of
  trusting the count, which is the same discipline that caught `$sexPose` in Section H.
- **"the_season renders no portraits on dialogue" was wrong.** A grep for
  `dialog-block dialog-npc"><img` returned 0 of 59; the portrait `<div>` is on the *following* line.
  Re-matched across the newline: **54 of 59 do carry a portrait.** Nearly shipped as a headline
  defect.
- **`census.tsv` in the corpus is not a passage count.** It reports `degrees-of-lewdity` at 636
  passages and `the-company` at 40; parsed properly they are **15,626** and **2,078**. Do not cite
  it.

### The verification count was wrong twice, and is 21

`games/` holds **28** directories with a `toml_phases/`, but only **21** carry a merged
`7_final_game.toml`, which is the file `gates.py` needs. The seven that have never been merged are
`jacks_world`, `media_testbed`, `new_in_town`, `test_customize`, `the_long_summer`, `two_weeks` and
`under_one_roof`. Earlier entries said 27, then 28; both counted directories. **Count the merged
file.** `STATUS.md` now carries the correction where the claim is made.

### What was refused

- **No gate for R8.** `degrees-of-lewdity` is rank 7 with 15,626 passages, and its NPC record reads
  `penis` **2,198** times against `name_known` **27** — `lefthand`, `righthand`, `stance`,
  `distance` are a limb-by-limb struggle machine. Its people are bodies in a physical simulation,
  and that is a second working answer to the same problem. A gate mandating that characters be
  differentiated *as people* would fail the seventh-ranked game in the corpus.
- **No lint for the schedule half of R8**, even though it is trivially checkable — declined as scope
  creep, and recorded in `the-surfaces.md` so the choice stays visible rather than looking like an
  oversight.
- **The per-character dialogue colour is not built.** Seven of 25 field games make a speaker macro
  the single most-used macro in the whole game, each rendering face + name + colour; we ship the
  first two (`v2.py:15035`) and one shared class for the third (`v2.py:15042`). Recorded in §34 as a
  known difference so it is not rediscovered as a gap, and left unbuilt until a game asks.
- **The full `engine.md` citation audit.** Three citations were fixed because this task read the
  code around them. The other 114 remain unaudited and the task stays open — half an audit reported
  as a whole one is worse than none.

**Findings:** `~/Documents/Female_PC_Craft_Study_20260823/findings_G_people.md`.

---

## 2026-08-24 — the H and J doctrine lands: the audience meter, and a refusal that can fail

**What.** `references/the-meters.md` (new **W5b**, plus a pointer from W5 and a header line),
`references/the-surfaces.md` (new **R5b.2**, **R6 mechanism 6**, and player evidence added to R6
mechanism 5), `references/engine.md` (new **§36**, plus an authoring note on §35), `SKILL.md` (one
lesson). Doctrine only — **`scripts/gates.py` untouched, no new gate, no threshold**, and no game
file written.

**Why now.** Sections H and J (2026-08-23) each ended with a proposal rather than an edit. LO
approved four of the five and, on the fifth — the refusal rule — said *"do what top games do, if top
games do it, then lets do it too."*

**That fifth instruction was conditional, so it was measured before being written.** The field does
do it: Course of Temptation carries **464** `$pc.skillcheck()` branch calls and **41** `*Resist*`
passages, including an explicitly named `EventWalkPassHFResistFail`; Degrees of Lewdity carries
**360** struggle/resist/escape passages. The canonical shape routes *"Refuse to respond"* off a
Willpower check whose difficulty is read from the NPC doing it, and **both branches are written and
paid in opposite directions on one meter** — success `Composure +25` / his `control −25`
(*"It's good to know he can't get to you quite so easily"*), failure `Arousal +100`,
`Humiliation +50`, his `control +25` (*"So easy"*). Branches of 354 and 629 characters.

**The mechanism was already in the engine, untaught.** `TemplateChoice.rejection_node` /
`rejection_effects` (`template_import.py:792-830`) render a locked choice as a **live link** that
routes to its own failure node — the generator's own comment is *"Mode B: Clickable rejection"*
(`v2.py:13147`), resolution at `v2.py:13668-13673`, effects at `v2.py:13152-13165`. Census re-run at
write time: **`rejection_node` 0 uses in 0 games, and 0 mentions anywhere in this skill.**

⚠️ **Two claims in the approved plan were wrong and are corrected here.** The plan said these
fields had "0 mentions" in the skill — `locked_text_threshold` was in fact already documented at
`engine.md:759` and in `DOCTRINE_GAPS.md`; only `rejection_node` was undocumented. And the plan
implied the locked-choice pattern was unused: `show_when_locked` is used **176 times across 12
games**. Both were caught by re-running the census before writing, which is why verification step 3
exists.

**The honest difference, stated in §36 rather than smuggled.** CoT rolls dice; this engine has **no
per-choice random outcome** — `conditions` has no `random` type (the "flag/trait/random" list at
`template_import.py:3143` is a docstring, not a feature). Ours is deterministic. That is defensible
because the field publishes its odds anyway — `skillcheck_descriptor` prints
*certain/trivial/easy/moderate/demanding/hard/very hard/nearly impossible* next to **314** choice
labels — so a published threshold keeps the same promise as a published probability. §36 says to
state the bar with `locked_text_threshold` and never to simulate a roll.

**W5b — the audience meter.** W5 covers a meter that falls and shuts doors and explicitly fails to
cover one that rises. Field: **644 read sites, 2% refuse the player anything** (14 sites), 81%
colour prose, median branch 139 chars in DoL and 84 in Zara against `the_season`'s 570. W5b records
that it is **optional** (`family-ties`, rank 24, 267 variables, no reputation system at all), that
its content is a stranger already knowing, that branch size is the cause and read count the
symptom, that it should be split by *what* and ideally by *who*, and that positive kinds
(`$fame.good`/`.social`/`.scrap`) do real work. W5 now carries a pointer saying which rule owns
which case, so the two cannot be read as contradicting.

**R5b.2 and R6 mechanism 6.** R5b gains the half the field has and we do not — a refusal that can
never fail is a menu item, a scene with no refusal is why players quit — with both player quotes.
R6 gains a sixth mechanism in kind: reputation as a **casting filter**, changing who is standing
there rather than what is offered (`juiciest_rumor` inside CoT's person-selection predicate).

**R6 mechanism 5 gains its player evidence**, including Zara's developer answering the complaint in
public — *"trying to give every single scene a different text"* — and the distinction that keeps the
rule from being misread: **repeating the loop is the genre, repeating the words is the defect.**
§35 gains the matching authoring line: **randomise the words, never the content.**

**`STATUS.md`** gains the four new rules in its built-inventory table, and its per-file **line
counts were removed entirely** — they had gone stale three times in one day, the same bug already
fixed for `CHANGELOG.md` on 2026-08-23. A count of a file edited every session is wrong by the end
of that session.

**`SKILL.md`** records the pattern rather than the feature, because this is now the second
occurrence: `block_pool` and `rejection_node` were both built, both unused, both undocumented, and
both announced by a rule that said *"our games do the opposite"* while offering no mechanism.

**Verified.** `gates.py` run across all **28** games carrying `toml_phases/` before and after —
**byte-identical**, as it must be for a doc-only change (⚠️ compare output, never exit codes: a
non-zero exit means a red gate, not a crashed script). Census re-run at write time. W5/W5b checked
for contradiction.

**Every cited line was re-read against `v2.py` rather than trusted, and four of the first five were
wrong** — including two this skill had been carrying for some time:

```
rejection_node / rejection_effects   template_import.py:811-812   (cited the class range :792-830)
"Mode B: Clickable rejection"        v2.py:13148                  (cited 13147)
locked_text fallback                 v2.py:13146                  (cited 12747 — STALE IN SKILL)
locked_text_threshold                v2.py:13185-13186            (cited 12786 — STALE IN SKILL)
rejection_effects emit               v2.py:13152-13165            ✓
rejection_node resolution            v2.py:13668-13673            ✓
```

`engine.md:759` and `DOCTRINE_GAPS.md` both carried `:12747`/`:12786`; both corrected. §33.4 was
found stale in the same pass — it cited `v2.py:12597` and `:4680`, **both of which are now blank
lines** — and now cites `getCostBlockedMessage` at `v2.py:4656` and the locked-choice span at
`:13140`.

⚠️ **Systemic, and NOT fixed here.** `engine.md` carries **117** distinct `v2.py:NNNN` citations and
**7 of them point at a blank line** (3448 · 3820 · 4496 · 5140 · 14065 · 14970 · 19297). Blank-line
detection only catches the obvious ones; a citation that drifted onto a different non-blank line is
invisible to it. `v2.py` moves and nothing re-checks the references against it. **A citation audit
of `engine.md` is worth its own task** — recorded here rather than half-done inside this one.

## 2026-08-23 — field study sections H and J: reputation refuses almost nothing, and J was not untouched

**What.** `STATUS.md` PART 6 and PART 7 corrected. Two new study files outside the skill:
`~/Documents/Female_PC_Craft_Study_20260823/findings_H_known.md` and `findings_J_players.md`, plus
`probe_macros.py`. **No doctrine written yet** — both findings files end with a proposal for LO's
call, per the propose-before-writing rule. `scripts/gates.py` untouched; no new gate.

**Why H was run first, against the standing recommendation.** `STATUS.md` recommended J then H.
Checking the data before starting reversed it: H had far more field evidence than assumed, and J
was largely a re-run (below).

**Finding — reputation almost never shuts a door.** Across 644 measurable read sites in three field
games, **14 refuse the player anything (2%)**. The rest overwhelmingly swap a short line of
dialogue — median branch 139 chars in `degrees-of-lewdity`, 84 in `zaras-school-life`. The skill's
only rule touching this, `the-meters.md` W5, is about a counterweight that **shuts doors**; it does
not cover a rising audience meter, so `the_season` asserted its own doctrine
(`0_systems_spec.toml:100`) unaided. That gap is now measured, not guessed.

**Finding — `the_season`'s `known` is thin.** Same instrument over the built game: **7 read sites in
111 passages**, zero in the locations, zero in the one-shots, median branch **570 chars** against
the field's 84–139. Big branches are why there are only seven. Recorded in `STATUS.md` PART 6 beside
the fill problem.

**Finding — Course of Temptation does not use a meter at all.** Reputation is *derived from memory*
— the code comment on `alter_rumor_strength` reads *"things that create memories (sex, flashing)
build reputation with no need to call this"*. Rumors are per-person, typed, carry a sentence and a
strength (25 of them), spread between NPCs at ×10, and are suppressed by friendship. It also casts
scenes: `juiciest_rumor` sits inside the person-selection predicate.

**Engine check, because H's best idea needed one.** Per-NPC conditions are supported for **both**
traits (`engine.md:320`) and flags (`v2.py:3877`, `subject === 'npc'`), and are used by 19 shipped
games — `the_season` itself has 33. **The engine is not the gap; no game has used the primitive for
reputation.** Checked before proposing, so the proposal is not built on an assumption.

**Correction — J's row in `STATUS.md` was wrong.** It read *"untouched — and the data is already on
disk."* The 2026-07-24 mopoga study had already read **22,622 comments across 31 games** and
published F1–F10 from them; `digest_comments.py` had been run; the cheat-page engine feature came
out of F8. J was renarrowed to the only question July could not answer — whether players' words
support the doctrine written this week — over 3,479 comments on the four study games.

**J's verdicts.** Variant pools **confirmed** (a player names the defect, and Zara's developer
replies in-thread that he is fixing exactly it); S3 lines-by-personality **confirmed** (a 26-like
feature request restating the rule); R5b **confirmed and extended** (players also mourn a *removed*
failure case — a refusal that can never fail is a menu item); the reason axis **unsupported and
unrefuted** — recorded as a miss so silence is not later mistaken for confirmation. The pivot rule
gets no evidence either way.

**Convergence worth keeping.** J's most-liked content theme in Course of Temptation is the world
failing to react to state (32+22+9+7+5 likes), and a Zara player asks for *"even just a few lines of
dialogue ... right now it feels like a switch was just turned on somewhere."* That is H's finding
arriving from the player side, and it did not come from H.

**Three instrument failures, all caught and recorded** in `findings_H_known.md` §0 — a regex whose
`[^>]*` could not match a condition containing `>` (reported a false `set=0 read=0` for two games
that use `<<if>>` thousands of times); `$sexPose` in `family-ties` being a sex *position*, not "sex
expose", which withdrew 405 read sites from the evidence; and a window-based branch classifier whose
opens/colours split swung 11%→47% with the window, replaced by a balanced span scan. The stable
`blocks` figure is what the headline rests on.

**Verified.** `gates.py` re-run across **all 28 games** carrying `toml_phases/` — every one produces
its scoreboard. ⚠️ Two corrections to how this is checked: the count is **28, not the 27 quoted in
earlier entries** (`ls games` = 29, of which `quests_v2_smoke` has no `toml_phases/`), and **a
non-zero exit from `gates.py` means a RED GATE, not a crashed script** — a first pass here read the
exit code and reported all 28 as failures, which was the check being wrong, not the run.

The real claim is narrower and was verified by mtime: **this turn modified only `STATUS.md`
(20:42) and this changelog (20:43)**. `scripts/gates.py` is untouched since 15:43 and no game file
or engine file was written at all, so no scoreboard could have moved.

## 2026-08-23 — audit of the same day's work: three real defects, and block_pool turns out to be knowledge we LOST

**What.** Corrections to `references/engine.md` §35, `references/the-surfaces.md` R6,
`SKILL.md` and `STATUS.md`, after LO asked for a thorough check of what had just been implemented.
Everything else in the day's work stood up.

**Defect 1 — the census was wrong, and the truth is worse.** §35 shipped saying *"vesper (v1) 6 ·
every v2 game 0"* and *"the v1 game found it; this skill never wrote it down."* Re-counted across
every `toml_phases/*.toml`: **the_long_summer 46 · under_one_roof 14 · vesper 6 · every v2 game 0.**

More importantly, v1's corpus carried a **numbered rule** for it — `prompts/game_design_rules.md:1330`,
*Rule 17: Block Pools for Repeatable Activities* — which named the failure exactly: *"the 'same text
every morning' problem"*, and *"the group block system handles phase changes, but WITHIN each phase
the text is frozen."* That is the same mechanism-4-vs-5 distinction the field study arrived at
independently on 2026-08-23.

**So this was not a discovery. It was a recovery.** The knowledge was lost when the v2 skill was
divorced from `prompts_v2/` for teaching false engine facts: the wholesale cut took a true fact with
the false ones, and nothing checked the discarded half. §35 now records the loss and its cause,
because the lesson is about the divorce, not the primitive.

**A near-miss worth recording.** The audit first surfaced
`games/the_long_summer_test/toml_phases/3_activities.toml:7-9` — *"block_pool prose rotation is in
the schema but forbidden by the doctrine"* — which read as a standing prohibition against everything
shipped that morning. It is a **test-slice** decision; the same repo's full game uses the pattern 46
times. Recorded in §35 so the next reader does not re-flinch at it.

**Defect 2 — two authoring constraints were undocumented.** From
`prompts/toml_generation_prompt_v4.txt:1044-1053`: all child blocks must be the same type, and
`block_pool` cannot nest inside another `block_pool`. The nesting constraint is now written down
**as unverified**, explicitly not as an engine fact — the plausible mechanism is that both pools
emit the same `_bp` temp (`v2.py:14580`), but whether SugarCube's already-matched `if/elseif` chain
actually breaks was **not tested**, and asserting it would have been the exact failure this skill
exists to prevent.

**Defect 3 — a measurement was over-generalised.** §35 said *"98% of DoL's location prose sits
inside a conditional branch."* It was a **ten-passage spot check**, not a per-location total of the
kind `location fill` computes. Rescoped in `engine.md` and `STATUS.md`, with the ten passages named
and an explicit warning not to quote the figure as a whole-game property. The conclusion it supports
— that folding pooled variants is the correct comparison — is unaffected: 234 words out of 9,886 is
lopsided enough to settle that question.

**Also.** `STATUS.md`'s file inventory had already drifted three lines from the same day's later
edits and was refreshed — the precise failure mode that made the previous STATUS.md wrong.

**What the audit CONFIRMED, so it is not re-checked.**
- 139 distinct `file:line` citations across the new material — **0 point past end-of-file.**
- All four block_pool passages (`SKILL.md`, `STATUS.md`, `engine.md`, `the-surfaces.md`) now carry
  the identical census.
- `STATUS.md`'s numeric claims re-derived: **35** numbered engine sections, **40** distinct gate
  names, **17** lints.
- The earlier shipped work is intact: five `meet_*` canvases still carry their windows (2/2/2/1/1
  rows, Prine's midnight-crossing row unsplit), `CastPage` is present in the built game **and** in
  its rendered `info_pages_list`, and G38 passes 5/5 on `the_season`.
- Every markdown code fence in the skill balances.
- `gates.py` output byte-identical across all 27 games, checked again after the corrections.

⚠️ **Two probes cried wolf during this audit and both were the instrument, not the work** — a
`grep` for unpadded `id = "meet_prine"` against TOML that pads the key, and a `grep` for
`info_pages_list` against a build that only contains the rendered array. Both were re-run correctly
before anything was concluded. Same class as the earlier `cd`-drift false alarm: **check the probe
before believing the alarm.**

---

## 2026-08-23 — STATUS.md rewritten; it described ten gates and we have forty

**What.** `STATUS.md`, full rewrite. Previous version preserved at
`scratchpad/STATUS.md.pre-2026-08-23` for the session; the CHANGELOG remains the durable trail.

**Why.** LO asked for a comprehensive document covering what is implemented, how the work has
moved, and how it proceeds. That document already existed and had gone materially wrong — dated
*"Last verified: 2026-08-11"*, headed *"The ten gates"*, with `back_home` as the live test game and
`vesper` described as *"1/10"*. Writing a fourth overlapping document beside `SKILL.md`,
`DOCTRINE_GAPS.md` and this file would have made the drift worse, so the existing one was brought
current instead.

**What it now carries.** The 40-gate / 17-lint split and why `n/a` is not a pass · the five
thresholds demoted or deleted for failing their own evidence · a current file inventory · every
game re-scored in one pass · the eight open study sections with their real state · the promotion
criteria, still unmet.

**The part worth keeping.** PART 3 records the arc rather than a snapshot, because it repeats:
doctrine from ONE game → `back_home` 10/10 → LO played it → **21 defects the scoreboard could not
see** → widened to 18 games → widened to 25 → `the_season` **39/40** → LO played it → *"I don't
know who is who"*. The same failure, one level up, against four times the instrumentation. The
evidence base keeps widening and the reading keeps deepening, and **neither has ever replaced LO
playing it.**

**Verified.** Every figure re-derived this turn, not carried over: file line counts by `wc -l`; 40
distinct gate names and 17 lints parsed out of `gates.py`; all 27 game directories re-scored in one
pass; seven `v2_state.json` ledgers enumerated from disk.

---

## 2026-08-23 — the engine already had the field's main mechanism, and this skill had never named it

**What.** `references/engine.md` (new §35, the Unverified list, §32.2), `references/the-surfaces.md`
(R6 mechanism 5, new R5b), `references/register.md` (two new part-one rules, S3 subsection, header),
`SKILL.md` (one warning under the cascade/node-routing rule). **`scripts/gates.py` was NOT touched
— no new gate, no new threshold.**

**Why.** LO's question — *"how do we measure good games?"* — landed on the honest answer that the
scoreboard measures plumbing, not writing: The Season scores 39/40 and his first reaction to playing
it was *"I don't know who is who."* So four top female-PC games were read **in source**, not counted:
Course of Temptation (mopoga rank 5), Degrees of Lewdity (7), Zara's School Life (22), Family Ties
(24). Study at `~/Documents/Female_PC_Craft_Study_20260823/`.

Step 0 of that study is itself worth recording: **there are only three clean female-PC games in the
mopoga top 30**, plus one selectable-with-female-default. The genre's top ranks are mostly male-PC
games in which women are the content.

**The finding.** Three of the four build **every** repeatable sexual surface out of a pool of
one-sentence variants, and none of them writes such a scene as a paragraph — Course of Temptation
`<<switch setup.rir(0, 3)>>` over 164 named acts, Family Ties `either(...)` over 12 poses, DoL a
deterministic grid on two arousal meters. Our engine has had the same primitive since v2 shipped:
`block_pool` (`v2.py:14572-14591`) emits `<<set _bp to random(0, N)>>` and an if/elseif chain.
Counted in each game's built TOML: **vesper (v1) 6 · every v2 game 0.** The whole skill mentioned it
**once**, inside a list of valid block types. vesper's own ledger already described the pattern in
the author's words — *"block_pool of penthouse stories"* (`5_scenes.toml:6036`).

**What was proposed, tested, and DROPPED.** The proposal opened with a P0: fix `gates.py` first,
because folding a pool's variants into one beat would over-count words. **That was wrong.** `Beat`'s
docstring (`gates.py:298-306`) already gives the reason variants fold, and the claim was checked
rather than assumed — measured across ten DoL location passages, **9,652 of 9,886 words (98%) of its
location prose sits inside a conditional branch**. ⚠️ *Corrected the same day — see the audit entry
above: that is a ten-passage spot check, not a whole-game figure, and must not be quoted as one.
The conclusion it supports is unaffected.* The `location fill` threshold was derived from
that same source (116,540 words / 25 locations, this file 2026-08-10), so folding **is** the
apples-to-apples comparison; changing it would break the only baseline the gate has. Where folding
distorts it distorts conservatively — ten explicit variants fold to *one* explicit beat, making
`explicit floor` harder to reach, never easier. §35 records this so the next reader does not
re-propose it. It also records why this does **not** contradict `register.md`'s 25-game table
(*"count one rendered path, not every branch"*): different instrument, different question.

**The two new writing rules.**

- **The reason axis** — *the same act, reached two ways, is written two ways, and the difference is
  WHY she is doing it, not how hot it is.* Course of Temptation's `ShowerStall` gates masturbation
  behind a skill **and** behind arousal, and writes a different intro for each: *"ignoring how
  precarious your privacy is"* against *"you're desperate for relief"*. Zara's School Life does it
  inside one act with two interiority paragraphs — *"she owned this moment"* against *"her own body
  responded traitorously"*. Grepped `references/` for *reason*, *same act*, *volition*, *chose*,
  *driven* first: **no rule of this shape existed.** The file states explicitly that this is not
  R6's banned move — R6 forbids tiering a **hub's** opener and is right; this varies the **act's**
  intro by the route that opened it.
- **The two-halves sentence** — DoL's `actionsothermouthpenisthrust` is a 3×3 grid with nothing
  random in it: his arousal writes the first clause, hers writes the second. **Nine outcomes from
  six written clauses.** Buildable today with stacked `group` bands.

**Also.** S3 gains *write the lines by personality, not by person* (Course of Temptation's thirteen
`dirtytalk*` widgets pick by `shy`/`crude`/`dominant` crossed with what the NPC wants). R5b records
that all four games write the decline branch at full length and pay it — Zara's is a full paragraph
granting `+60 Energy`; Course of Temptation charges `friendship -50 -60` for pushing and being
refused. R5b is listed with R1/R2/R4 as **deliberately not gated**: four games is an observation,
not a field.

**A self-contradiction is gone.** `engine.md`'s Unverified list still carried *"adjacent `[group]`
blocks merging into a single if/elseif chain"* while `the-surfaces.md` R6 stated it as fact. Read
and promoted: `_render_group_chain` collects consecutive `group` blocks at `v2.py:14561-14568`.

**What was deliberately NOT changed.**
- **No rule about opening length.** The corpus range is 109,714 characters (Course of Temptation,
  rank 5) down to one paragraph of safety instructions (DoL, rank 7). Two of the top seven at
  opposite extremes; any rule here would be invented.
- **The pivot rule was tested and CONFIRMED.** Zara folds heavy interiority into its acts and never
  leaves the body — *"her pussy was clenching with need, dripping for him"* — which is not a pivot
  by the rule's own definition. `register.md` now records that it survived, and nothing about it
  moved.
- **No game files.** Not The Season; **not vesper**, which was read for evidence only.

**Verified.**
1. `gates.py` re-run across **all 27 games** in `games/`, before and after: **every output
   byte-identical.** (First run reported movement everywhere — that was a shell `cd` leaving a
   doubled relative path so the "after" runs could not find `gates.py`, not a real change. Re-run
   from the repo root with an absolute path: clean.)
2. Every line cited in §35 re-read after writing: `v2.py:14572-14591`, `v2.py:14561-14568`,
   `gates.py:298-306`, `gates.py:338-349`.
3. The `block_pool` claim checked against a **real build, not a synthetic one** —
   `games/vesper/output/index.html` contains **6** `_bp to random` emissions.
4. Grepped that no file still lists adjacent-group-merging as unverified.

---

## 2026-08-23 — the introductions played to empty rooms, and the cause was a comment in the schema

**`the_season`'s five meeting canvases carried no time window**, so each one auto-fired the moment
the player walked into the room whether the character was standing in it or not. Seen live, twice:
`meet_prine` fired at the camp at **06:10 on a Saturday** with Prine out in the rows, and
`meet_boyd` fired **on day 6** in the shed with his line reading *"That's low for you and it's
Monday."* Separately, `meet_emmett` opened on a bare name — *"Emmett is on the belt…"* — and no
line in that canvas ever said he was her brother.

### The cause, and it was not the author

Checked engine → doctrine → one-off, in that order.

- **The engine is correct.** `isCanvasValid` (`v2.py:4559-4574`) reads schedules, conditions and
  repeatability and never reads `requiresNpc`. Repo-wide the field is consumed in exactly two
  functions: `setup.checkRandomEncounters` (`v2.py:5245`) and `setup.checkAndSubstituteCanvas`
  (`v2.py:5318`). Neither is the auto-fire path.
- **The doctrine is correct, and it was already there.** `references/the-first-hour.md` F5 carries
  the traced warning and `templates/first-hour.toml:126-136` ships the schedule block with the note
  *"the SCHEDULE below is what actually stops this firing in an empty room."* Both files were
  **created** in `e0783a1` at **2026-08-23 01:29:49**. `the_season`'s TOML was written at
  **13:19:12** — twelve hours later, with both open.
- **The cause is `apps/projects/services/template_import.py`.** Its comment on
  `TemplateTrigger.requires_npc` said the field *"lets authors drop per-canvas location+time gates
  in favor of consulting the NPC's single source of truth."* Unscoped, and false for every meeting
  canvas. **The schema file and this skill said opposite things, and the schema is what is open
  while you write TOML.**
- **And nothing checked it.** `every hub is met first` tests flags and hub gating only.

### Changed — `scripts/gates.py`

**New gate `a meeting fires where they are` (G38)**, beside `every hub is met first`, which is its
other half: G34 asks whether a character is introduced before their hub opens, G38 asks whether that
introduction can only play in a room they are standing in.

- **In scope:** not `is_repeatable`, not `substitution_only`, not `trigger_mode = "random"`, and
  declares `requires_npc`. Those three exclusions are precisely the shapes that *do* read
  `requiresNpc`, so the gate never convicts a canvas the field actually protects.
- **Fails** a canvas with no `trigger.schedules` whose NPC declares `[[npcs.schedules]]` rows at
  that same location — a window was authorable and was not authored. Detail lines print the hours
  that were available to copy.
- **Skips** a canvas whose NPC has no rows there. Nothing to match; a different, weaker finding.
- Measured across every game the day it was written — 69 canvases in scope and **zero carry a
  window that misses their character's own hours**, so it never nags a game that did the work:
  `last_call` 11/11, `off_season` 8/8, `the_long_summer_test` 1/1 clean; `the_season` 0/5,
  `the_inheritance` 0/24, `vesper` 0/13, `late_shifts` 6/7.

### Changed — `references/the-first-hour.md`

- **F5** gains the measurement, the gate's name, and the finding above: the rule was correct and
  present and a game shipped 0/5 anyway, because a second document said the opposite.
- **F7 gains the honest admission that nothing enforces it at the meeting.** The `named before met`
  lint skips any character who *has* a meeting and never reads the meeting's own text, so a bare
  name in a first paragraph passes every check in this skill. **A check was tried and rejected**,
  recorded so it is not re-attempted blind: a kinship-word detector fires falsely on ten of
  `last_call`'s meetings (its cast is not family), eighteen of `the_inheritance`'s and three of
  `off_season`'s mid-arc canvases. The instruction is to read the five first lines yourself.

### Changed — `references/engine.md`

**§31.1** names the two consuming functions, states the three trigger shapes a check must exclude,
and records the contradicting schema comment so the next reader who finds one finds the other.

### Changed — `SKILL.md`

One gate-index row.

### Engine (outside this skill, logged here because §31.1 documents it)

`template_import.py`'s `requires_npc` comment rewritten: the claim scoped to the two functions that
read it, what actually does the work on every other path stated plainly, and the failure recorded
in place. **Comment-only** — `off_season` rebuilt and diffed against its committed build with zero
new differences.

### Verified

- **`the_season` gate diff:** the new gate appears and passes; `location fill` moves 4,411 → 4,412
  words, which is Emmett's sentence gaining one word. Nothing else moves — including
  `the opening opens a door`, whose 05:05 handover the `meet_rae` window had to keep open.
  **38/39 → 39/40.**
- **Every other game re-scored.** PASS and +1/+1 on `last_call`, `off_season`,
  `the_long_summer_test`; the gate fails on `late_shifts`, `the_inheritance` and `vesper` (true
  findings, not fixed — two are v1 games); **n/a with no change at all** on `back_home`,
  `forty_miles`, `mothers_place`, `seventh_day`, `steam`, `the_allowance`.
- **The bug itself, read live in the built HTML.** The camp at 06:15 → `meet_prine` does **not**
  fire; the camp at 20:25 → it does. The shed before noon → `meet_boyd` does **not** fire; 12:30 →
  it does. `meet_emmett` renders *"Your brother is on the belt…"*.
- **The chain still closes:** all five meetings reached in one ordinary day —
  05:15 Rae · 07:40 Wade · 07:55 Emmett · 13:05 Boyd · 21:15 Prine. No console errors.

---

## 2026-08-23 — the guidance page introduced the whole cast on click one, and there was no page to look anybody up on

**LO played the first testable build of `games/the_season` and could not tell who anyone was.** The
gates were at 38/39. Every hub was correctly gated behind a meeting. And the Quests page still
listed all five characters — names, the room each stands in, the hour they are there — on the
player's first click, before a single meeting had fired. Two of them, Boyd and Emmett, additionally
read **"✓ Arc complete"** on turn one.

Measured against the field rather than against our own doctrine
(`~/Documents/Mopoga_Twine_Sandbox_Research_20260724/gamehtml/`, all 25 parsed):

```
cast page (Characters / Notes / Journal / Dramatis Personae)   17 / 25
hints or guide page                                            17 / 25
of the 8 parsed top-ten, ones with a cast page                  7 / 8
games using a narrator to explain who somebody is               0 / 25
```

The one top-ten exception is degrees-of-lewdity, which carries the load in the prose instead —
description swapped for name on the meeting flag, 64 places. `the_season` did neither.

### The three defects, placed

- **Doctrine.** F5–F8 gate the *canvases* and say nothing about the *guidance surface*. A game can
  obey every rule in `the-first-hour.md` and still name its whole cast on the guidance page.
- **Doctrine.** `engine.md` §23 said *"set `terminal = true` on the last card of every arc"* — true,
  and not sufficient. It never said `terminal` is **not computed from progress**, so a character
  with a single terminal card on a `lt` band prints ✓ at value zero.
- **Engine.** There was nowhere to look a character up. `[ui.tips_page]` and `[ui.cheat_page]`
  existed; no cast page did.

### Changed — `references/the-first-hour.md`

- **New subsection under F8, "The same flag belongs on that character's quest cards."** The meeting
  flag goes in every one of that character's `[[quest_cards]] when`, as its own item beside the
  trait band. `QuestsPage` wraps each section in `<<if _card>>` (`v2.py:15371`) and `pickQuestsCard`
  returns null on no match (`v2.py:15050`), so the roster fills in as the player meets people with
  no engine change. Carries the three traps: an item sets `flag` **or** `trait` and never both
  (`template_import.py:5285`); the flag goes on *every* card in the ladder, not just the first; and
  **flag names are validated against nothing**, so a typo hides a character forever in silence.
- Story-goal cards (no `npc_id`) are explicitly excluded — gating those renders "No active quests."
- **Added to the scoreboard table:** nothing checks the guidance surface. `named before met` reads
  prose canvases only and does not look at `[[quest_cards]]`. Said out loud rather than left to be
  inferred from a gate list that looks complete.

### Changed — `references/engine.md`

- **§23** — the correction above: Frame 1 fires on `card.terminal === true` alone (`v2.py:15199`),
  nothing checks achievement. `terminal` belongs on a card the player has to **climb to**; an arc
  needs an open lower band and a terminal upper one.
- **New §34, `[ui.cast_page]`.** The block authors no content — name, `relationship`, live location
  and next step are all read at runtime. Records that **`relationship` is the only NPC string that
  survives to runtime**: `description` is popped before `$npcs` ships (`v2.py:1027`) because `$npcs`
  is snapshotted into every history moment, so a bio written there is an author note the player
  never sees. Records that who is listed is the quest cards' decision, and states the cost of that
  coupling plainly.

### Engine (outside this skill, logged here because §34 documents it)

`[ui.cast_page]` shipped: `TemplateCastPage` + parse + metadata write in
`apps/projects/services/template_import.py`; `_generate_cast_page` + `_cast_page_css` +
`<<castButton>>` in **both** `StoryCaption` branches + the `infoPages` allowlist in
`apps/game_generation/twee_comprehensive/generators/v2.py`.

### Verified

- **Every gate diffed before and after.** One line moved, and it is the two new cards:
  `guidance exists  13 → 15 quest cards`, still PASS. Score unchanged at **38/39**, `location fill`
  still the only red.
- **Read live, not inferred** (headless Playwright, the built HTML). Turn one: Story Goals plus Rae
  only — she is the one the opening meets — **zero "Arc complete"**, and The Crew page shows Rae
  with her relationship line and 📍 The Yard. After meeting Wade: both pages gain Wade and nobody
  else. All five met: five cards, right relationship lines, live locations, right tips.
- **Ladder**: at `owed`/`seen` 0 no ✓ anywhere; pushed to 30/25 the second cards take over and ✓
  appears exactly twice.
- **Rebuilt WITHOUT `--dev --debug`** and confirmed the button and page still render. A page wired
  into only the dev `StoryCaption` branch ships dev-only and no gate catches it.
- No console errors, no `pageerror`, in either build.

### Not done

No new gate. The card-gating rule needs a second game before a threshold is honest — a gate written
from one game is how `location fill` got a budget 3.5× its delivery.

---

## 2026-08-23 — the brake detector could not see a day cap, and said so out loud

**Two gates were reporting rungs as free that the engine will not serve twice in a day** — and
the mechanism they could not see is the one their own remediation text tells the author to use:
*"day-cap the rung with a flag cleared in `[engine.daily_tick]`."*

Found authoring `games/the_season` v0.1. `walkin_showers_wade` is guarded by
`wade_rung_today is_false`, sets that flag, and `[engine.daily_tick]` clears it. The player cannot
click it twice in a day. `the climb is paid for` said **"9 clicks, no cap."**

`_routes` already knew this pattern — but only for a choice routing into ANOTHER CANVAS, because it
keys on `nodeId`. A walk-in's own exit choice targets a **location**, so it produced no route at
all, `_is_free` fell through to the trigger, and every choice-level cap in the repo was invisible.

This is the family `_farmable`'s own docstring already documents twice, and it names the rule:
`SKILL.md`, *a check that fails a game for obeying the doctrine is a bug in the check.* Its two
earlier instances each produced "a real defect introduced purely to please a check" — a `costs`
block on a game's intro, and a 1-energy charge on every dev choice. The fix is in the check.

### What changed — `scripts/gates.py`

- **`_tick_cleared(game)`** — the flags `[engine.daily_tick]` unsets. The third part of a cap.
- **`_holder_day_capped(holder, cleared)`** — the three-part cap on ONE choice: its `conditions`
  read a flag `is_false`, its own `flagEffects` set it, and the tick clears it.
- **`_grants()` skips a day-capped holder.** A rung that shuts after one click grants nothing
  farmable.
- **`_is_free()` also recognises the SPLIT cap** — guard on the trigger, setter on a choice inside.
  The canvas stops rendering the moment the flag is set, and this is the *more* common shape,
  because a day cap usually covers a whole activity.
- **`no free uncapped income` skips a surface whose money grant nets to zero.** With every grant on
  it capped, the gate was still listing it at "+0" — a faucet with no water in it.
- **`_free_climb` returns None when `start >= top`.** A meter that already satisfies its gate at
  game start was never climbed. `vesper`'s `hygiene 100 → gate at 40` was being reported as
  *"entirely for FREE — 0 clicks, 0m of game time"*, which describes no climb at all. Zero clicks
  is a starting value, not farming. Same denominator error the gate's own comment says it exists to
  avoid.

### How it was verified

All **20 built games**, `--json`, `PYTHONHASHSEED=0`, pre-edit vs post-edit.

> ⚠️ **A zero-diff bar would have been the WRONG bar here**, unlike the `--words` refactor above. A
> correct fix to a check that was making false claims *must* move the games those claims were about.
> The bar is instead: **no game flips pass-state, and every dropped row is verifiably false.**

**Six games changed. Pass-state flips: ZERO.** Every change removes a row; none grants a pass.
Three spot-checked against their own source:

```
last_call        canvas_rosa_hub "Sit and listen" — +4 relation, sets talked_to_rosa_today,
                 guarded on it is_false, cleared in daily_tick.   Gate said "9 clicks, no cap."
the_inheritance  p_floor_private — trigger guards private_done_today is_false, three choices set
                 it, tick clears it.   Gate said "+5300 money every 180 min, no daily limit."
vesper           hygiene starts at 100 against a gate at 40.   Gate said "free in 0 clicks."
```

`the_season` moved 29/37 → 31/37, both gates green for the right reason.

---

## 2026-08-23 — the vocabulary check, one phase earlier

**The lint that catches a word the player cannot decode only ran against a BUILT GAME**, which is
one phase too late. By the time a game exists, every noun is already set into a room name, a
button label and the prose behind it, and changing one means renaming things.

Caught on `games/the_season`, authoring its Want. The author had, one message earlier, written out
the whole `airer`/`lodger`/`immersion` finding and committed to writing the game in neutral
vocabulary — and then put **`rota`** into the Want's own charge section, plus **`ledger`** as the
name of a mechanic. Both were found only because the check was hand-rolled against
`scripts/genre_words.txt` at the end of the phase. Nothing in the skill asked for that.

Applying the skill's own test — *would a correct author-game-v2 have prevented this?* — yes, and
the fix is in the skill.

### What changed

**`scripts/gates.py`**
- **`lint_own_words(model, game)` split into `own_words_report(text, declared_names, suppress,
  shown)` plus a two-line wrapper.** The hard part — sentence-aware proper-noun detection, literal
  possessives, `_CALENDAR`/`_NUM_WORD` filtering, false friends, the `half <hour>` check — is
  unchanged and is now reachable **without a parsed game**.
- **New CLI mode `python3 gates.py --words <path>`** — the same instrument on any text file, for
  the WANT and BOARD phases. Always exits 0; `register.md` is explicit that this is a list and
  never a score, so it must not be able to block a phase.
- **`_SKILL_META`** — this skill's own vocabulary, suppressed **only** in `--words`, because a
  design document legitimately says `tiers` and `ratcheting` and a report where 41 of 46 rows are
  the skill talking to itself is a report the author skims. The count is always printed.
  Deliberately small: `odometer`, `lint`, `rungs`, `slug`, `dispatcher` and `scoreboard` were
  **considered and rejected** — each can name a real thing in a porn sandbox, and for a
  list-only lint a false negative (a shipped word) costs more than a false positive (a skimmed
  row). Terms already in `genre_words.txt` are omitted as no-ops.
- **`shown` is now a parameter** (default 20, unchanged for games; `None` in `--words`). The cap
  was sized for a whole game and it **hid the exact word this mode was built to catch** — `rota`
  ×1 sorted into the unprinted tail behind twenty commoner ones. First run of the new mode
  reproduced the original defect, which is the correct thing for a check to do to its author.
- **`--words` reads the cast off `v2_state.json` beside the file** (`_words_declared_names`).
  Without it the cast topped its own report: five of the first six rows were the game's own
  people. Declare-then-check, same shape as everywhere else — nothing is guessed.
- **False friends are filtered by `suppress` too**, and `meter` is in `_SKILL_META` for that half
  only. In game prose it is a genuine false friend; in a design document it means the stat bar on
  purpose, so the warning was the check arguing with the vocabulary it is written in.

**`references/the-want.md`** — a fifth item under *"The test before you leave this file"*: the
command, why it belongs at the Want rather than at the end, and an instruction to re-run it on the
board's location names. **No example words**, per `SKILL.md`'s operating rule — a rule is read and
an example is copied, which is how `airer` and `£5 for the immersion` spread in the first place.

**`templates/want.md`** — the same check as item 5 in the checks block, where an author filling
the template actually hits it. A template is filled in; a reference is read.

### How it was verified

- **The refactor moves nothing.** All **20 built games** in the repo, `--json`, pre-edit file
  (`git show :`) vs post-edit, `PYTHONHASHSEED=0`: **0 diffs**.
- ⚠️ **The first comparison reported 5 regressions and every one was false.** Gate 10's
  *"also ranked"* list is built from a set, so its order varies between processes: the **same
  code, run twice, does not match itself**. Fixed the instrument (`PYTHONHASHSEED=0`) rather than
  the code. Worth carrying — a baseline diff on this script is meaningless without a pinned hash
  seed, and the next person to refactor here will hit it.
- **The new mode reproduces the defect that prompted it.** Against a pre-fix copy of
  `games/the_season/WANT.md` it prints `ledger ×4` and `rota ×1`; against the corrected file,
  neither.

### Two follow-ups, found by running it for real on the board phase

- **`--words` did not know the protagonist's name**, so `cass` topped her own report on every
  run — she is the player and is therefore not in `board.characters[]`. Added an optional
  top-level **`protagonist`** to `v2_state.json`, read by `_words_declared_names`, and documented
  in `references/state.md`. Same declare-then-check shape as everything else: nothing is guessed.
- **It caught a real one on the first board.** `games/the_season` shipped *"a hose bib on the
  outside wall"* — `bib` is precisely the `airer`/`immersion` class, a short common-looking word
  naming an object the reader must already own. Also `blacktop`. Both fixed before a line of
  prose existed, which is the entire point of moving the check earlier. What survived the pass
  and was kept on judgement: `tailgate ×5` (decodable in context), `peaches`/`crews` (plurals of
  in-corpus words).

### ⚠️ Open, NOT fixed here — the scoreboard hands out vacuous passes on an empty board

Running `gates.py` at board phase for the first time (a game with 9 locations, 6 characters and
**0 canvases**) returns **PASS** on checks that have nothing to measure — and one of them prints a
claim that is false:

```
[PASS]  a day-cap closes     7 day-cap flag(s) cleared in [engine.daily_tick], all of them set somewhere
```

Each of those seven flags occurs **exactly once** in the built TOML — the clear. Nothing sets
them and nothing reads them. `sinks >= sources` likewise passes at **1 : 0**, and
`a place is not a catalogue` and `a spent day still has a door` both pass across **zero screens**.

This is `SKILL.md`'s own rule turned on the instrument: *a check that measures EXISTENCE has not
measured anything*, and *an absence is not a pass* — these should report **n/a**, as the content
gates correctly already do. Left open deliberately rather than folded into this edit: it is a
separate change to a separate set of gates, and it is LO's call whether to spend it now.

---

## 2026-08-23 — the empty screen: a hub with nothing on it, and the gate that now says so

**LO walked into Ewan's yard in his own built game and got a portrait, a paragraph, a line of
dialogue and nothing to click.** He could not tell whether the game was broken. It was not: he had
spent that character's one rung and one talk for the day, every exit on the hub was gated, and a
choice whose conditions fail renders **nothing** — not a greyed line (`v2.py:12806`). The engine
printed its own diagnostic and offered a bare `Continue`. That code is identical in `v1.py:11590`,
so this was never a v2 generator regression.

### What was actually wrong, measured across all ten built games

Parsed every `7_final_game.toml`. `off_season` had **10 choice-nodes with no unconditional exit**;
every other game had **0**. Vesper's 11 all-conditional nodes are a different shape — conditional
routing, exhaustive by construction (`stealth gte 10` / `lt 10 + fighting` / `lt 10` catch-all) —
and cannot all-fail. Off Season's are independent daily budgets that deplete together, so all-false
is the guaranteed end of every day, not an edge case.

**The cap is per PERSON; the hubs are per ROOM.** Ewan had three hubs — yard, harbour, arcade
counter — all reading one `ewan_rung_today`. Spending it at the yard emptied the other two for the
rest of the day, and their entire list was that one flag. The built HTML carried **13** copies of
the engine's dead-end banner: those 10 hubs plus 3 screens whose only affordance costs money, which
are equally empty to a player at $0 because the engine counts a cost-bearing choice as conditional
(`v2.py:12827-12836`).

### Why every other game got this right without being told

**The leave-link was never a written rule anywhere.** `last_call` and `mothers_place` carry eleven
day-capped hubs and eleven leave-links (*"Leave him to it ↩️"*, *"Leave her alone."*); `seventh_day`
and `the_allowance` do the same. The only paragraph in either skill on the subject is
`author-game/references/engine-reference.md:297`, and it says you should **not** add an
unconditional fallback — correct for routers, wrong for day caps. **v2 carried nothing at all**: its
`engine.md` documented `exit_block` syntax and never mentioned the no-exits case, the `Continue`
fallback, or needing an always-live exit. The leave-link was a habit in the v1 corpus, and v2
inherited rules, not habits.

`a day-cap closes` was itself written from this game's own measured failure and checks only that a
cap has a **setter**. It never asked what the surface looks like once the cap is **spent** — which
is every day, by design. Half the problem gated; the other half invisible.

### Changed

- **`scripts/gates.py`** — new gate **`a spent day still has a door`** (G37), placed beside
  `a day-cap closes`, which is its other half. Fully mechanical, no threshold: a choice is a *door*
  only when it carries neither `conditions` nor `costs` — **mirroring the engine's own
  `has_unconditional_choice` (`v2.py:12827-12836`) rather than re-inventing it**, so the gate and
  the runtime cannot disagree. A choice is *shut* when its AND-conditions read a
  `[engine.daily_tick]`-cleared flag `is_false`, or when it spends `money`. Fail a node with no door
  all of whose choices are shut; `n/a` when the game declares no daily tick.
- **`references/the-surfaces.md`** — **R7 · Every screen keeps one door**, with the per-person /
  per-room mechanism, the TOML shape, and an explicit scoping note that the incumbent skill's
  "don't add a fallback" advice is about exhaustive **routers** and does not reach a day cap. Plus a
  row in *What is checked*.
- **`references/engine.md` §28.3** — the engine facts v2 never carried: a failed condition renders
  nothing unless `show_when_locked`; a cost counts as a condition; the three things the engine does
  when nothing passes; and that a leave-link pointed at the node's own location does **not** re-fire
  the hub, because a canvas with `npcId` renders as a clickable portrait (`v2.py:4919`), not an
  auto-fire.
- **`SKILL.md`** — the gate indexed beside `a day-cap closes`.

### Verified

- The new gate **fails with 13 findings** against the pre-fix TOML and **passes** after — and the
  detail lines name each screen and classify it *all day-capped* / *all priced* / mixed.
- **Zero false positives.** Run across all ten built games: 6 PASS, 3 n/a (no daily tick), **0
  FAIL** — including vesper's 11 routing nodes and `seventh_day`'s 18 cost-gated ones, which the
  scoping deliberately spares.
- `off_season` fixed in the same turn (one always-live exit per screen, 13 of them) and rebuilt:
  the built `index.html` went from **13** dead-end banners to **0**.
- Every existing gate diffed before and after on `off_season`: **one line moved**, and it is the
  expected arithmetic — `ends on an opening` from `52/142` to `52/155` choices as the 13 doors were
  added. Score **37/38 → 38/39**, `location fill` still the sole failure.

---

## 2026-08-23 — Off Season's word pass, and a false example this file was citing

**The game half of the pass above.** The instrument could see these words as of this morning;
nothing had fixed them. `games/off_season` now reads **55 flagged words / 121 uses**, down from
**67 / 148**, and **37/38 still passes with no gate moved on any of the 20 games.**

### The count was never the target, and proving that was most of the work

`register.md` says *"read the list, do not read the number"*, and this is what that looks like in
practice. Checked against `scripts/genre_words.txt`: `kettle`, `flats`, `winters`, `clocks` and
**`seafront`** are all "absent from the field" — and `seafront` is the word this skill explicitly
prescribes (*"the front → the seafront"*). Roughly two-thirds of the 67 were frequency artifacts:
proper nouns the filter missed, inflections the lint cannot lemmatise, and ordinary English 25 porn
sandboxes happen not to use. **Every one got a decision; about a third got an edit**, and the
reasons for the rest are now in `games/off_season/v2_state.json` rather than in someone's head.

### Where the word sits is what it costs

Measured before touching anything: the game has **9 room-list buttons in total**, and **2** carried
a flagged word. Canvas names on walk-ins and one-shots were checked against the built
`output/index.html` and **do not reach a player** — they appear only in JSON metadata, a
`dev-canvas-info` block and a review block. That scoped the label work to 2 buttons and 9 clickable
choice labels instead of the ~30 the lint implies.

```
"Feed the meter ($3)"   ->  "Put $3 in the heater"      <- the one LO clicked
"Take a turnaround"     ->  "Clean a flat for the agency"
```

Also killed at the source: **`Buy a coin mechanism off the chandlery ($25)`** — the line
`gates.py:1775` names as the measured trigger for the entire rule, still sitting in the game that
produced it.

### What changed in the game

`meter → the heater` / `the coin box` · `chandlery → the boat shop` · `float → the till` /
`the change bag` · `pitch → rent` (the game's central obligation, written in a word for a market
stall) · `extractor → the fan`, with the full name kept once at first contact · `immersion → water
heater` · `knickers → panties` (the `vest` precedent — a false-friend garment inside an explicit
beat; explicit-floor neutral, both are in the regex at `gates.py:252`) · `plasterboard → thin` ·
`hairgrip → hair clip` · `bin lorry → garbage truck` · `advert → commercial` · `draught → draft` ·
**`The Holiday Lets → The Holiday Flats`**, a nav button on every screen that the lint
**structurally cannot see**, because `_player_visible_text` folds every location name into its
proper-noun filter.

**Kept, and the reason matters more than the list.** `pusher` stays because the arcade's own first
visit already says *"Four coin pushers in the middle"* — the gloss rule working exactly as written.
`hull`, `fryers`, `cardigan` stay for the same reason: the sentence around each one carries it.

### ⚠️ This file was citing a false example, and it was about our own game

The false-friend row cited `off_season`'s *"Stay past the tea"* as the evening meal, on a quest
card, as UI. **It is not.** The scene it labels reads *"You make two teas in the two mugs he owns
and you do not leave when yours is finished."* It is the **drink**, and so are all nine uses in the
game, including the hunger band *"Running on tea."*

The word was read off the lint's output and never checked against the line it came from — the exact
failure the section exists to name, committed inside the section itself. **A false friend is a
judgement about a sentence, never about a word.** Citation removed, the correction kept on the
record beside it, and the game keeps its nine.

### How verified

- **No gate moved on any of the 20 games**; off_season holds **37/38**. All five exposed gates
  checked by name, not by total: `location fill` 14,681 → 14,689 words (the only FAIL, untouched),
  `somebody speaks` 4.3:1 against a 5:1 ceiling, `sentence length` median 10 against 14,
  `explicit floor` 15.3%, `a price is on its label` 0 misses.
- **The pass introduced zero new flagged words.** Diffed the rare-word set before and after — the
  55 remaining are a strict subset of the original 67. Batches 6 and 7 both had to fix words
  written *during* the batch; this one was checked after editing rather than before.
- **Read the buttons in the built HTML**, not the TOML: `Put $3 in the heater` and `Clean a flat
  for the agency` render; `Feed the meter`, `Take a turnaround`, `Holiday Lets`, `chandlery`,
  `immersion`, `knickers`, `plasterboard`, `hairgrip`, `bin lorry` return zero hits.
- **`games/off_season/v2_state.json` gained its first `releases` entry**, with the gate score and
  the lint figures shipped with — the first use of the release-loop amendment made this morning.

**Still open on this game, and named rather than quietly carried:** the anchor at 24.9%, the
`pound ×3` currency regression from batch 8, and the clock at 9× the field median. All three belong
to the fill batch, not to a word pass.

---

## 2026-08-23 — the words the doctrine named and the checker could not see

**Cause: LO opened the built Off Season, hit `Feed the meter ($3)`, and could not read it.**

> *"in her bedroom it says: Feed the meter — is she turning on her heater?? or wtf is this about??"*

It is a coin-fed prepayment meter for the flat's water heater. The word is accurate, the object is
real, and the reader has to arrive already owning it. **This was the second time** — the same
complaint on 2026-08-22 produced this section of `register.md`, the `own_words` lint, and the
cleanup of the skill's own examples. All three landed, and he hit the wall anyway, because three
separate things were still wrong.

### 1 · The checker was missing the words this file leads with

`gates.py`'s `_FALSE_FRIENDS` held nine terms. `register.md`'s section opens on *"**meter** (a
coin-fed prepayment meter), **jumper**, **eiderdown**"* and lists *pitch → rent* and *float → the
till money* among its required swaps. **`jumper` went into the dict on 2026-08-22. `meter`,
`pitch` and `float` did not.** A false friend is by definition a word four or more field games use,
so `genre_words.txt` is structurally blind to it: if the hand-built dict does not carry a word,
nothing in the instrument does. The word this section leads with was invisible to the whole skill,
and it reached a player on a button.

**Added**, after reading every hit in all 20 built games (269,421 player-visible words):
`meter` ×32 · `float` ×24 · `pitch` ×10 · `chemist` ×3.

**Measured and rejected, recorded in the code so it is not redone:** `front` ×334 and `inside`
×213 are noise; `tip` ×44 carries three real uses, a 7% signal rate that would train the reader to
skim; `boot` ×8 is footwear every time, not one car boot in the repo; `bill` ×7 and `purse` ×10
give a slightly wrong picture that does not cost the line. The bar is not *could be misread* — it
is *misreads badly enough to lose the line, often enough to be worth its false positives*.

### 2 · The rule fell through the seam between two files

`register.md` said *"gloss it in the sentence that first uses it, **or** use the plain word."*
**A button has no sentence.** The player reads a label *before* the prose that would explain it, so
on a label the choice collapses to one branch. `register.md` owns words, `the-voice.md` owns
labels, and neither said so.

Off Season's meter is glossed well — *"the slot is at shoulder height beside the water heater… a
card taped under it saying what three buys"* — and the only route to that sentence is clicking the
words the player could not read. **The gloss was downstream of the button the whole time.**

### 3 · Nothing in the release loop made anyone read the list

`the-release.md` step 5 said *"gates.py green, or fix it"* and said nothing about the nineteen
lints the same command prints. Off Season shipped **37/38 with 67 flagged words** and a scoreboard
that reads *excellent*.

⚠️ **Deliberately not a checklist.** `DOCTRINE_GAPS.md` §3a already ruled on this — *"checklists do
not hold… v2 must not inherit the checkbox"*, with v1's 13-point audit followed by the exact bug it
was written to prevent. So step 5 gained a rule about output already on screen (anything left in a
list is left on purpose, named with its reason), and step 6 records the lint figures in
`v2_state.json`, where a number has to come down — the mechanism the anchor share already runs on.

### What changed

- **`scripts/gates.py`** — four entries in `_FALSE_FRIENDS`, with the six rejects and their counts
  in the comment above it; **plural matching** in the lookup (`uses` is a bag of singular tokens,
  so `vests` ×2, `torches` ×2 and `biscuits` ×1 were invisible); and the **silent truncation**
  named — `ranked[:20]` printed 20 rows under a summary saying 67, swallowing 47.
- **`references/register.md`** — the label sub-rule; a **fourth** failure mode, *collides with our
  own UI* (a meter is a stat bar in this genre and off_season renders four in its sidebar — the
  clash is with our vocabulary, not a dialect; same exposure on `board`, `card`, `flag`, `state`,
  `tier`, `rung`); and a passage naming `_FALSE_FRIENDS` as the authority this file keeps in sync.
- **`references/the-voice.md`** — R1's example fixed and its history kept: it taught *The Lodger's
  Room* until 2026-08-22 and *The Tenant's Room* after, and **`tenant` is under the corpus bar
  too**. Not a second `lodger` — the plural `tenants` is in-corpus, so it is standard English under
  a frequency threshold and it stays wherever the skill describes a *role* to an author — but a
  room name is a button, and Off Season had already shipped **The Back Room**. Also annotated the
  `Feed the meter (GBP 3)` worked example at `:124`: it carried **two** defects and the currency
  pass that quoted it fixed one.
- **`references/the-release.md`** — loop steps 5 and 6, above.
- **`references/the-economy.md`** — `forecourt` out of the `"obligation"` JSON snippet, replaced
  with *out by the pumps*. **Found by this pass's own verification step**, not by design: one of
  the eleven zero-of-25 words, sitting in the highest-copy form the skill has.
- **`SKILL.md`** — the lint index now says the own-words lint reads choice labels and location
  names, not only prose. That is what `_player_visible_text` does and it is the seam that failed.
- **`DOCTRINE_GAPS.md`** — item 11 restated: half closed by the loop amendment, the rest open and
  barred from arriving as a checklist.

### How verified

- **No gate moved on any of the 20 built games.** Tallies diffed before and after with
  `PYTHONHASHSEED=0` (three games carry pre-existing tie-break noise): `off_season 37/38`,
  `the_allowance 29/37`, `seventh_day 28/37`, `forty_miles 25/36`, `steam 18/35`, `back_home
  15/33`, `vesper 11/30`, and the thirteen others unchanged. This was lint-only work and the diff
  is empty.
- **The new entries fire exactly where measured.** off_season `meter ×10 · pitch ×5 · float ×4`;
  the_allowance `meter ×3 · chemist ×3`; forty_miles `float ×7 · meter ×5 · pitch ×3`; back_home
  `float ×1`; steam `float ×10 · meter ×2`; vesper `meter ×11 · pitch ×2` — both vesper rows are
  expected false positives (a meter-reader's blank, a whine climbing pitch) and read as obviously
  so, which is the `torch` precedent.
- **Plurals now counted:** forty_miles `vest` 73→75 and `torch` 2→3, vesper `torch` 6→7, back_home
  `biscuit` 2→3.
- **Truncation announced:** off_season prints 20 rows and then *"and 47 more word(s), 56 use(s),
  not printed"*.
- **Re-swept the skill's own files** for ~50 locale-locked terms. `templates/` is clean — no
  locale-locked term in any file authors fill in. Every remaining hit in `register.md`,
  `the-surfaces.md`, `the-voice.md`, `SKILL.md` and `gates.py` is the doctrine naming a word in
  order to ban it. The three words this pass introduced — `prepayment`, `buoyant`, `chemist` —
  appear only in glosses and doctrine, never in a worked example.
- **The four new glosses read against the nine existing ones** and were rewritten once: the first
  draft of `meter` named another game inside a per-game finding and `float` carried corpus
  statistics. Both now match the house shape — *"X here, Y to most readers."*

**Not done here, on purpose.** Off Season's own 67 words — including `tea`, `immersion`,
`chandlery` and the `Feed the meter` button itself — are a game-side pass. The skill now catches
them; nothing has yet fixed them.

---

## 2026-08-23 — SKILL.md's lint index had gone stale

**What changed.** `SKILL.md`'s "Lints sit below the tally" list now names **dispatch depth** and
**the act nodes**, the two lints added on 2026-08-23.

**Why.** That paragraph is the only place the skill enumerates what the scoreboard prints. Two
lints shipped in `gates.py` without being added to it, so an author reading the skill would not
know they exist and would not know to read their rows. A check nobody is told about is a check
nobody acts on.

**How verified.** Read back against `gates.py`'s print block — every lint the script emits now
appears in the list, and every name in the list is emitted by the script.

---

## 2026-08-23 — a game-wide heat share cannot see the act the player is on

**What changed.** `scripts/gates.py` gains `lint_act_nodes` (with `_act_nodes`, `_node_has_prose`
and `_band_texts`), `_collect` learns the second group shape, and `references/register.md` gains the
act-node rule under "The measured targets".

**Why.** `explicit floor` is a percentage of all beats in the game, and a game can clear it while
every act node is warm. That is not hypothetical — it is the measured failure this whole doctrine
was written after: 95% of one game's crude prose sealed in a room with no exits, and all nine of its
repeatable loops scoring zero. A share cannot see that; it averages it away.

Measured on the game authored under the corrected skill, which was reading a comfortable pass:

```
loop_arcade_floor   bare=5 glass=7 finish=4      <- the two SOLO loops
loop_flat_solo      act=6  act_deep=4 finish=3
loop_tam_bed        hands=1 mouth=3 astride=2 finish=3
loop_ewan_caravan   hands=4 mouth=1 finish=0     <- three paragraphs of a man coming,
loop_roan_stay      hands=2 fingers=2 fuck=1 finish=5    not one body word in them
loop_nessa_curtain  hands=2 fingers=2 mouth=3 finish=1
```

**10 of 21 act and finish beats under 3** — and the cold ones are the four CHARACTER loops, which is
where that game's own `the_want.md` says the crudest writing in it lives. The solo loops, written by
the same hand, are twice as crude as the ones with a person in them.

⚠️ **Count the band, not the node — found by playing it, not by reading it.** The first version of
the lint read `Beat.explicit`, which folds a node's `[group]` bands together on purpose. The live
probe then found nine finisher BANDS under 3 on nodes the lint had just passed: one finisher scored
6 folded and put two body words on screen whichever band fired. `_band_texts` now reports the
thinnest band a node can render, and the lint prints `finish=6(band 2)` when those differ.

⚠️ **And it exposed a blind spot in the MODEL, not just the lint.** `_collect` read a group's
children only at the block's own `blocks` key. The importer accepts them there **or** inside
`props.blocks` and normalises to the latter (`template_import.py:6062-6086`); the generator then
renders `props.blocks` (`v2.py:13770`). Four games write the second shape, and **158 groups of
prose were invisible to every beat-based gate in this file** — not counted as words, explicit beats,
dialogue or sentences, while rendering perfectly well in the built game:

```
the_long_summer_test   4,979 -> 9,429 words   (its anchor location changes, and 2 gates flip)
late_shifts            5,095 -> 6,017
last_call              4,478 -> 5,017
the_inheritance       12,975 -> 13,045
```

That is a correction, not a regression: those four games were being measured against half their
prose. `off_season`, `back_home`, `steam`, `the_allowance` and `vesper` write the first shape and
their output is byte-identical.

**How verified.** Red first: the lint printed the table above before a word was rewritten, and it
discriminates — `vesper` reads median 1 with 17 of 25 act beats under 3, which is the same game the
2026-08-10 measurement caught. Then all twenty games run under `PYTHONHASHSEED=0`; the only movement
anywhere is the four games the `_collect` fix stopped under-reading. The game that exposed it now
reads **0 of 21 under 3 on the thinnest band each node renders**, verified live on the built page
with the choice labels stripped out — the `opens later` vocabulary is also the text of the 0.2
doors, and a locked door is a signpost, not content (`the-voice.md` R4).

---

## 2026-08-23 — the walk-in gate counted branches; the rule is about how many

**What changed.** `scripts/gates.py` gains `lint_dispatch_depth` (plus `_rule_bounds`,
`_rules_contradict`, `_dispatch_worst_case`), and `references/the-surfaces.md` R3 gains the depth
rule and the Pattern A / Pattern B engine table.

**Why.** `the walk-in floor` is an existence gate — `subs[loc] > 0` — and says so in its own comment.
R3's content is the branching (*"the richness is combinatorial, not authored"*, DoL's `Bath` = one
activity, twelve outcomes), and nothing had ever printed how deep a dispatch goes. Measured across
the repo:

```
game                  hosts  rules  distinct outcomes per host   max
back_home                 3      7  [4, 2, 1]                      4
vesper                    5     10  [1, 1, 1, 1, 4]                4
last_call / the_allowance 1      3  [3]                            3
late_shifts               9      9  [1 x9]                         1
the_long_summer_test      7      7  [1 x7]                         1
off_season                5      7  [1 x5]                         1
```

Three of seven games could not produce a second outcome from any activity. Fourth instance of the
same shape as the clock lint, the currency lint and the ladder lint: **the doctrine was right and the
check covered part of it.**

**The lint prints the host's own survival odds**, because the mechanism is invisible in the TOML.
Rules without `exclusive_group` each roll their own dice (`v2.py:5382-5391`) and compound; rules
sharing one share a single roll split into buckets (`v2.py:5361-5379`). Five branches at 0.12 leave
the activity on screen 53% one way and 40% the other, and an author reading only the TOML cannot see
which they wrote. It found `back_home`'s `activity_wash` renders itself **24%** of the time.

⚠️ **Two corrections made before it shipped, both to stop it printing a wrong number.**
1. It first multiplied every rule's chance. `back_home` stacks four `exposure >= 35/45/55` rules that
   are all true at the top of its game, so multiplying is right there — but `off_season` bands one
   walk-in `lt 20` / `gte 20 and lt 22` / `gte 22`, where exactly one can pass, and multiplying those
   reported 6% for a canvas that renders 70% of the time. Same TOML shape, two mechanisms, so
   `_rules_contradict` finds the impossible pairs first.
2. It then picked the **largest** co-satisfiable set, which made the answer depend on declaration
   order — two size-three sets left the host 55% and 16% of the time. It now picks the set that
   squeezes the host hardest. A number that moves when an author reorders their TOML is not a
   measurement.

**How verified.** Red first on all seven dispatching games, printing the table above before anything
was authored; then all twenty games run under `PYTHONHASHSEED=0` with **no gate moving anywhere** —
it is a lint. The fix in the game that exposed it took off_season to `[3,5,5,4,3,4,3]`, the deepest
dispatch in the repo, and the lint immediately found a latent defect in that game's own pre-existing
bands (see `games/off_season/REVIEW_1.md` §12). Verified live against the engine: 400 dispatcher
calls per host, every bucket reachable, the observed rate tracking `Σ p` and not `1 − ∏(1 − p)`, and
the fall-through handing a shut bucket's share back to the host rather than to the next bucket.

---

## 2026-08-23 — the ladder lint measured one side of a fork the doctrine declares

**What changed.** `scripts/gates.py`: `lint_meter_ladder` now chooses which meters to measure off
`board.who_climbs`, via a new `_cast_meter_rungs`. Ladder games (`ascent_tiers` non-empty) print
`N declared tiers` exactly as before; a roster game prints `N cast meters`, read off every
`subject = "npc"` trait predicate. `the-meters.md` **W1** makes *who climbs* a declared fork, and
the instrument only implemented the ladder side:

```
back_home / forty_miles / seventh_day / steam / the_allowance   3-4 tiers measured
off_season   (who_climbs = "cast", ascent_tiers = [])           SILENT — nothing measured
```

**Why it mattered.** The one roster game in the repo ran **six meters at 1–3 rungs each with every
lowest rung at 12–22**, against W4's field of 8–17 rungs and a lowest rung at a median of 5. With
grants of 2–7 that is four to eight interactions with a person before anything about them changes —
W4's own failure sentence, and the lint that exists to say so was the one lint that said nothing.

**Third instance of the same shape.** The clock lint had four blind spots (2026-08-22), the
currency lint had no sub-units (2026-08-22), and this one had half a fork. In all three the
doctrine was right and the check covered part of it, so the game passed while breaking the rule.

**A second bug, found by running it red.** Three of off_season's meters reported a rung at **110** —
`the-release.md` G9 doors, declared unreachable against grants capped at 100. A gate above the
meter's ceiling is a locked door, not a step anything climbs to, and counting it credits a game with
a rung it can never reach. `METER_MAX = 100` now drops those on **both** sides of the fork, and
`FIELD_METER_RUNGS` (which the old body computed and never used) is wired into the summary string
instead of the 8 being hardcoded beside it.

**How verified.** Red first, before a single rung was authored: the extended lint printed all six
off_season ladders as they stood. Then all twelve games run old-vs-new under `PYTHONHASHSEED=0`
(three games carry pre-existing tie-break noise that has nothing to do with this change) —
**off_season the only diff, and no gate moved anywhere.** The fix in the game that exposed it:
18 new rungs, every meter bottoming at 4–5, `somebody speaks` improving 4.8:1 → 3.9:1, and 105 new
live checks green (`games/off_season/REVIEW_1.md` §11).

---

## 2026-08-22 — the currency lint could not see a sub-unit, and a real regression sat behind that

**What changed.** `scripts/gates.py` `_CUR_UNIT` knew `pound`, `dollar`, `euro` and `yen` and **no
sub-units**, so `pence`, `penny` and `cent` passed straight through `_cur_units`. A game that had
declared a neutral `$` and then written *"she is out by sixty pence"* read as
**"no beat names a currency"** — a false green.

Added `pence` / `penny` / `pennies` → pound, `cent` / `cents` → dollar, `centime(s)` → euro,
`sen` → yen, with a **`per cent` guard** in `_cur_units`.

⚠️ **The guard was measured, not guessed.** Without it, `steam`'s *"the soap alone is up forty per
cent"* and *"the trade is down forty per cent"* both false-positive as money. Checked directly:

```
"the trade is down forty per cent"          -> []                              guarded
"She is out by sixty pence"                 -> [('pound','pence','word')]      caught
```

**What it was hiding.** `off_season` declared `$` in repair batch 2 and then reintroduced British
coin units in batches 4 and 5 — `fifties` ×6, *"sixty pence"*, *"the two-pence one"*, *"to the
penny"* — three of them in canvases written **during the repair itself**, matching the surrounding
British texture instead of the declared rule. Six fifties for a $3 charge is arithmetic nonsense,
and nothing in the toolchain said so for two batches.

Run red before green: with the fix the lint immediately printed both ⚠ mismatch lines
(*"the prose runs on `pound` and [settings.rent] currency_symbol is `$`"*), and went clean once the
words were gone.

**Repo-wide effect, checked before shipping:** it newly and correctly flags `forty_miles`
(*"the fifty-pence tube"* ×3). **No gate moved on any of the twelve games** — this is a lint.

⚠️ **Known limit, left alone:** `_CUR_WORD` requires whitespace between the number and the unit, so
a hyphenated *"fifty-pence tube"* is caught by the unit word but a bare *"50p"* is not. Pre-existing,
and widening the pattern is a bigger change than this defect justifies.

**Files:** `scripts/gates.py` (`_CUR_UNIT`, `_CUR_PERCENT`, `_cur_units`).

**Verified.** `games/off_season/REVIEW_1.md` batch-6 Log carries the game side; the game's currency
lint now reads "no beat names a currency" and means it.

---

## 2026-08-22 — the clock lint had three blind spots, and they hid our defects and not the field's

**What changed.** `scripts/gates.py` `_clk_refs` — the instrument behind `lint · the clock in the
prose` — could not see three shapes, and all three are ones our authors reach for:

```
"By nine the whole flat…"      "the" sat in _CLK_BAD_NEXT, to catch "at one point"
"at half nine"                 "half" was not in the hour vocabulary
"Seven in the morning and…"    no preposition, so the rule never fired
```

Four fixes, plus a counting bug: `half [past] <hour>` added to the vocabulary **and** as a
standalone pattern; a part-of-day pattern (`<hour> in the morning|afternoon|evening`, `at night`);
`quarter past|to <hour>`; `"the"` moved from the stoplist to the allow-list; and matches now
**deduped by span**, because several patterns legitimately hit the same phrase and counting *"at
half nine in the morning"* twice inflated the rate.

**Measured on the corpus before any of it was written** (25 games, 11.0M words):

```
                        FIELD median   FIELD p75      off_season   steam   forty_miles
shipped instrument           1.0           2.1           20.1       29.2      22.6
corrected instrument         1.1           2.1           26.4       36.6      34.4
```

**The field moves by one reference in one game — a true positive (*"gathered at half past six for
drinks"*). Ours moves by a quarter to a half.** The constructions the regex could not see are
British-inflected narrative idiom our games use and the corpus does not, so the blind spots were
hiding our own defects almost exclusively. `FIELD_MEDIAN` / `FIELD_P75` updated 1.0/2.0 → 1.1/2.1
and `references/the-clock.md`'s published table re-measured with it.

⚠️ **Rejected, with the number that killed it:** dropping the `_CLK_OK_NEXT` allow-list entirely is
the tidier rule and inflates the **field** to median 1.2 / p75 2.6 — noise being scored. The
allow-list stays. The instrument deliberately under-counts rather than over-counts, which is the
safe direction for a list nobody scores.

**It immediately earned it.** Run against `off_season` the corrected lint found **four readings no
earlier pass had listed**, two of them the opening line of a milestone one-shot:
*"Half nine and the flat is at twenty-four degrees"* · *"Half eleven and the telly has been on mute
for two hours"* · *"Half ten and your glass has been empty twenty minutes"* · *"Seven in the morning
and the fryers have been off an hour"*.

**`references/the-clock.md` C2 also gained the half it never had.** C2 was written about the
**hour**. The same reading-versus-rule test runs on two more axes it did not name, and both shipped
in `off_season`:

- **the day of the week** — *"It is Thursday."* in an all-days canvas; *"It's not Monday. What's
  gone wrong?"* as the first line of a hub whose character works Mondays;
- **a figure the state already holds** — *"Forty-one pounds sixty"* asserted in prose while the
  sidebar prints the real balance.

Stated generally: **a beat may not state anything the engine is already tracking.** The section says
plainly that the lint sees neither axis and a human has to.

**Files:** `scripts/gates.py` (`_clk_refs`, the new patterns, span dedupe, re-measured constants) ·
`references/the-clock.md` (C2's new subsection, field table re-measured).

**Verified.** Field re-measured with the *shipped* function, not a copy: median 1.1 / p75 2.1. No
gate moved on any of the twelve games; only the lint's printed numbers rise.
`games/off_season/REVIEW_1.md` §8 (T1–T7) carries the game side, which went 32/38 → **34/38**.

---

## 2026-08-22 — the day cap: three parts, on the choice, and one of them was optional in the example

**What changed.** `references/the-meters.md` M5 and `references/engine.md` §28 both taught the
day-cap flag on the **rung's exit**. That is the wrong half of an asymmetry in the generator, and it
is where a live, silent defect in `off_season` came from. Both are rewritten; one new gate ships
with them.

**The engine fact, read rather than assumed.** A choice and a node exit emit their effects in
opposite orders:

```
choice     flagEffects -> costs -> … -> advanceTime      v2.py:12648-12733
node exit  advanceTime -> traitEffects -> flagEffects    v2.py:13085-13088 · :13049-13050
```

`advanceTime` rolls the day inside itself (`v2.py:5411-5414`) and `advanceDay` is where
`[engine.daily_tick]` clears every `_today` flag (`v2.py:5552`). So an **exit**-set cap on a rung
that crosses midnight is written on the far side of the clear, and the new day starts already
capped.

**`engine.md:989` said the opposite** — it warned the cap gets *cleared* and the rung becomes
re-clickable, which the emit order makes impossible. Replaced by §28.1 with the table and the
citations, plus §28.2 on the two-of-three failure below.

**Measured in the game the example authored.** `off_season/act_flat_sleep` ran 21:00–06:00 and set
`slept_today` on its exit, so from night two onward Sleep was never offered before midnight again —
the player was pushed into a permanent post-midnight bedtime. Four more rungs sat in the same trap
on late hub windows (`rung_roan_stay`, `rung_roan_later`, `rung_nessa_tea`, `rung_nessa_curtain`).

**And the placement is not a taste call — the repo had already voted:**

```
day-cap flag set on a CHOICE   78    last_call 11 · late_shifts 15 · the_inheritance 15
                                     mothers_place 9 · seventh_day 4 · vesper 1 · TLS 23
day-cap flag set on an EXIT    40    off_season 15 · the_allowance 20 · late_shifts 1 · TLS 4
```

Choice-set is the dominant practice and every v1 game uses it. **The two games holding 35 of the 40
exit-set caps are `off_season` and `the_allowance` — the two written under this example.** Third
recurrence of `SKILL.md`'s "an example outranks every rule beside it", after `15/35/55/75` and the
volatile list.

**New gate · `a day-cap closes`** (`scripts/gates.py`, judged set 37 → 38). Every flag read with
`is_false` in any condition **and** unset in `[engine.daily_tick]` must have at least one
`op = "set"` site. A cap with two of its three parts validates and throttles nothing, and nothing
else in the toolchain can see it: the generator's flag-chain validator reports a never-set flag only
when a condition requires it `is_true` (`v2.py:11659`), so an `is_false` read on a never-set flag
fails open, silently.

Fully mechanical — no threshold, no field measurement, nothing to judge. Predicted with a standalone
script before the gate was written, and the shipped gate reproduced it exactly:

```
off_season       FAIL   4 flags — ewan/nessa/roan/tam_talk_today
last_call · late_shifts · mothers_place · seventh_day · the_allowance ·
the_inheritance · vesper · the_long_summer_test          PASS
back_home · forty_miles · steam                          n/a (no [engine.daily_tick])
```

In `off_season` those four caps meant the talk screens were re-clickable every twenty minutes at
+2 on a cast meter for 3 energy — equal per energy and 50% faster per minute than the day-capped
rung they were designed to sit below.

**One more fact recorded while verifying:** a **located** canvas needs no flag at all.
`max_triggers_per_day` is read off the trigger (`v2.py:11017`) and `markCanvasTriggered` stamps its
day key **before** `advanceTime` (`v2.py:4290`), so it is immune to the whole problem. The flag
pattern is for triggerless rungs only. Both files now say so.

**Files:** `references/the-meters.md` (M5 rewritten, worked example moved onto the choice) ·
`references/engine.md` (§28 rewritten, §28.1 and §28.2 added) · `scripts/gates.py` (one gate) ·
`SKILL.md` (scoreboard row).

**Verified.** Gate red before the game was touched (`off_season` 31/37 → 31/38), green after
(32/38), no other gate moved. Fifteen live checks in a headless build, including sleeping on two
consecutive evenings and clicking a talk screen twice in one day. `games/off_season/REVIEW_1.md`
§6 (D1–D4) carries the game side.

---

## 2026-08-22 — the currency: one notation, declared, and the engine set to it

**Cause: the same session, the same review, item 5.**

> *"What does Feed the Meter (GBP 3) means??"*

`games/off_season/REVIEW_1.md` §5, items M1–M3.

### What the research found

**The defect is three times the size the review recorded.** M2 reports three notations in one game.
Counting what the *engine* writes as well as what the author typed, **one click carries six**
(`games/off_season/toml_phases/3_activities.toml:83-108`):

```
room-list button   Feed the meter (GBP 3)                  author
the choice         Put three pounds in (GBP 3, 5 min).     author
the paragraph      Six fifties … Three pounds gets you …   author
when she is short  Requires 3 Money (you have 1)           engine  v2.py:4680
the sidebar        money: 12 / 100                         engine  v2.py:16215 · :16241
rent day           $90                                     engine  v2.py:1190
```

**v1 was stronger here, in two files, and v2 kept only one of them.**
`author-game/references/rent.md` (278 lines) taught the money *system* — §8's budget arithmetic, one
wallet, income as a corruption ladder — and v2 carried that forward as `the-economy.md` R1–R6.
`author-game/references/prose-truth.md` (121 lines) taught that **a price written into prose is a
copy of a TOML field with no link back**, and **v2 has no counterpart at all**: a grep of the whole
v2 skill for `prose is a copy | re-price | stale prose | prose-truth` returns nothing. Recorded as
`DOCTRINE_GAPS.md` Tier 3 row 13; the currency is its first measured instance, not the whole of it.

Note that v1 got the fiction half *right* and said so: `prose-truth.md` §2 approves spelling a price
out in a character's mouth (*"`125` never appears as a digit in that prose — it's spelled out, in
voice, as it should be"*). The field agrees. So R7 bans the spelled-out price on a **button**, which
is interface, and leaves it alone in speech.

**The field — 25 shipped sandboxes, 11.0M words of passage prose.** The mechanism first, because it
explains every number that follows: **the field uses one printer.**

```
degrees-of-lewdity   money held in PENNIES; <<printmoney>> -> formatMoney()
corpo-life           formatUSD($money) — one Intl.NumberFormat call
the-hellfire-club    <<printmoney>> — guineas / shillings / pence, divisors 252 and 12
new-life-project     StoryCaption prints  £$money
```

Three unrelated economies, one architecture: the symbol is applied at a single site, so it cannot
drift. Measured consequences:

```
                                            FIELD          OURS
one notation, share of money references       92% median     82% median   (field min 56%)
priced link labels using a SYMBOL             94.0%          off_season 0%
       …spelling the unit out                  5.2%
       …using a currency CODE                  0.8%
a money WORD carrying an exact amount          20%           51%
symbol, of 16 games with a real economy       $ 10 · £ 2 · CODE 1 · invented unit 3
persistent balance in a UI passage            12 of 16
```

⚠️ **A claim in `REVIEW_1.md` Appendix A.5 is wrong and is corrected here.** It records *"FIELD
currency CODES (GBP/USD/EUR) on labels or in prose: 0"*. **`corpo-life` uses `USD` 109 times**,
including on a link label — `Buy a set of Bespoke suite (USD 15,000)` — and uses it *consistently*
(94% of its money references). The correction improves the rule rather than weakening it: the
requirement is **one** notation, not a particular one, which is also why a gate on the *form* would
be wrong (see below).

**The engine — read, not assumed.** `[settings.rent] currency_symbol` (`v2.py:1190`) is the nearest
thing we have to a printer, and of the **sixteen sites** where the generator prints a money figure
it reaches **four** — all on the rent-day screen. Nine hardcode `$`; three print no notation at all.
Full census: `references/engine.md` §33. Three findings inside it that nothing in the skill recorded:

1. **`RentDay_Short` hardcodes `$` and does not even set `_cur`** (`v2.py:16000`). It is the branch
   taken when the player cannot pay. `games/forty_miles` declares `currency_symbol = "£"` with the
   author's own comment *"the pages hardcoded `$` before this key existed"* — and its released build
   still ships `You have: <strong>$<<print $player.core_traits.money>></strong>`. The key did not
   finish the job, and the author believed it had.
2. **The sidebar ignores `[[traits.labels]]`.** `trait_bar` reads `_item.label || trait_key`
   (`v2.py:16215`); `setup.trait_labels` is consumed only by `_labelForTrait` (`v2.py:6781`), which
   formats *condition* text. `label = "Change bag"` does not rename the readout. And `_traitMax`
   defaults to 100, so an uncapped currency renders as **`money: 12 / 100`** over a 12% fill bar.
3. **A choice's price is rendered only when the player cannot afford it** (`v2.py:12597` vs
   `:12747` + `:4680`) — the same asymmetry §32.2 records for time. So the visible price is authored
   prose in every normal case, which is why hand-typed notations are the norm rather than the slip.

`[[traits.labels]] unit` is imported (`template_import.py:2885`, stored `:6310`) and read by no
generator — a dead key, recorded so nobody reaches for it as a pluralisation lever.

### What changed

| file | change |
|---|---|
| `references/the-economy.md` | **new R7 · One currency, declared once, and the engine set to it** — under a new section heading, since R5/R6 are billed as "two rules from failure". The four parts, the house default and its two measured reasons, the prefix-only engine limit, the ledger-drift warning, and why one check is a gate and two are lints. Ledger example gains `"symbol": "$"`. Checks table gains the gate and both lints. |
| `references/engine.md` | **new §33** — the sixteen print sites in a table, the prefix limit (§33.2), the sidebar's `label`/`max` behaviour (§33.3), the affordable-vs-blocked asymmetry (§33.4), the dead `unit` key (§33.5). `:891` and `:931` examples moved off `£`. |
| `scripts/gates.py` | **gate `the price is in one currency`** (35 judged → 36) + **lints `currency_in_prose` and `price_spelled_out`** (15 → 17). Helpers `_CUR_UNIT` / `_cur_units` / `_cur_labels` / `_cur_setup` / `_cur_extra` / `_cur_exact_share`. |
| `SKILL.md` | scoreboard row; both lints added to the index. |
| `references/state.md` | ledger gains `board.economy.symbol`, with the key's meaning in the field notes. |
| `references/the-voice.md` | R1's cost paragraph gains the notation half beside the price half. |
| `templates/board.toml` | a currency-declaration warning above `[settings]`; the `[[needs]] costs` placeholder now says "in the game's ONE notation". |
| `DOCTRINE_GAPS.md` | Tier 3 row 13 — prose that copies a field, the missing v1 counterpart. |
| `games/off_season/REVIEW_1.md` | Log entry, and the Appendix A.5 correction above. |

**The `£` sweep.** 21 pound signs sat in live skill files, the same "an example outranks the rule
beside it" mechanism item 1 fixed for dialect (and one of them was in `the-clock.md`, shipped by me
last pass). The rule applied: **a quote of measured reality stays verbatim** — DoL's real cost tag
`(£12 1:00)`, a real game's declared `£200 a week`, the played-game label `Buy coffee (0:02 £2)` —
and an **invented teaching example moves to `$`**. Four qualified: `engine.md:891`, `engine.md:931`,
`the-economy.md` R3's *"Monday, £120, or else"* and its *"£120 against a £42 day"*.

### Why one gate and two lints

**Gated, because it is string work:** does the game use more than one *currency*? A symbol and its
own word are the same unit — `$` and *dollars* differ in form, not in currency, and the field ships
both in one game — so the check maps them together and fails only on two units. The engine's own
`currency_symbol` and the ledger's `symbol` are channels like any other.

**Not gated, because a rate gate would fail correct work:** `zaras-school-life` writes every price
in words across 905k words and never varies; `apocalyptic-world` prices in caps; `vesper` prices ten
labels `10 coin` and never varies. `SKILL.md` — *a check that fails a game for obeying the doctrine
is a bug in the check*.

### Two false positives found by running it before believing it

- **`+50 money` is not a price.** The first build added the currency *trait name* to the unit
  vocabulary, so `seventh_day`'s `[DEV] +50 money, refill energy` read as a second currency and
  failed the game. Generic money nouns (`money`, `cash`, `funds`, `wallet`, `balance`) are now
  excluded, and `_cur_labels` skips dev shortcuts via the existing `_is_dev` marker.
- **The lints and the gate disagreed on `vesper`.** The lints inferred the currency by first name
  match and got `money`; the gate used gate 16's usage ranking and got `coin`. The lints now use the
  same usage ranking — the exact bug `the-economy.md` already records for gate 16, rebuilt inside a
  new check.

### Verified

Ten games, before and after. Every denominator moves by exactly one and **no existing gate changed**:

```
                 base      new    the price is in one currency
off_season      31/36 →  31/37   FAIL  `pound` x9 (6 of them GBP) vs the engine's `$`
the_allowance   28/35 →  28/36   FAIL  `pound` x7 on buttons vs the engine's `$`
seventh_day     26/35 →  27/36   PASS
forty_miles     24/35 →  25/36   PASS
steam           17/34 →  18/35   PASS
back_home       14/32 →  15/33   PASS  no button states a price — the lint carries it
vesper           9/28 →  10/29   PASS  `coin` x10, consistent
last_call       13/26 →  14/27   PASS
late_shifts     10/27 →  11/28   PASS
the_inheritance 13/25 →  14/26   PASS
```

A standalone predictor written before the gate called all ten correctly on labels; it also predicted
`back_home` would fail, on prose. It does not, and that is deliberate — **the gate does not read
prose**, because a beat that mentions a foreign price is legitimate and a parser cannot tell it from
a defect. The prose lint carries it instead, naming the contradiction directly:
*"the prose runs on `pound` and `[settings.rent] currency_symbol` is `$`"*.

The prose lint also found something no one was looking for: `off_season`'s `amb_lets_drawer` reads
*"A hairgrip, two euros, and a paperback"* — a **third** real-world currency in the same game.

### Still open

- **Ten hardcoded `$` in `v2.py`.** A generator change, out of scope for this stream, and the reason
  the doctrine recommends `$` rather than merely requiring consistency. `engine.md` §33.1 carries
  the list so the decision is costed whenever it is taken.
- **Off Season is unchanged.** Doctrine first, the game as its proof — the agreed order.

---

## 2026-08-22 — the clock: the time the game promises and the time the engine keeps

**Cause: the same session, the same review, item 4.**

> *"Work the counter till one (2h 30m). One is 1 pm or am whatever it is, but we dont mention work
> till one or time, there is something wrong going on. Its content also have shutter up at eight
> and more, WTF is this?? Time is dynamic it is a sandbox game."*

`games/off_season/REVIEW_1.md` §4, items T1–T3. Closes the time half of `DOCTRINE_GAPS.md` Tier 2
row 7 ("The daily loop — time costs, energy, what an ordinary day is"), which was marked *partly*.

### What the research found

**v1 carried half of this and v2 dropped even that.**
`author-game/references/rts-flat-prose.md:360` is **Rule 10 — "Never assert elapsed time the
player's pace controls"**, with an exemption list, a replacement table and the note that where
precision *is* the character you keep the precision and drop the number. v2's `register.md` shipped
without it: a grep of every v2 reference for `clock|o'clock|name a time|absolute time|time of day`
returns only engine mechanics. And Rule 10 only ever governed **days and weeks** — it never mentions
the clock, which is the half that broke.

**The field — 25 shipped sandboxes, 11.0M words.** One instrument on both sides. The first draft of
that instrument was ~90% idiom ("at one point" ×312, "one by one", "after ten minutes") and was
rebuilt with a stoplist before any number below was trusted.

```
clock references per 10,000 words       FIELD median 1.0   ·   20 of 25 games at or under 2.0

last_call        v1    0.0        back_home       v2   13.5
vesper           v1    2.2        seventh_day     v2   17.5
the_inheritance  v1    5.8        off_season      v2   21.3
late_shifts      v1   13.7        forty_miles     v2   22.3
                                  the_allowance   v2   23.4
                                  steam           v2   31.1
```

**Two explanations were tested and both failed — recorded so they are not tried again.**

1. *"The field keeps hours out of prose because its clocks are coarse."* Classifying every field
   game by what its state actually mutates: minute-clock median **2.4** per 10k, hour **4.9**, slot
   **1.1**, none **1.4**. Every bucket sits between 1 and 5, and `degrees-of-lewdity` tracks minutes
   across 2.1M words at **0.4**. Resolution does not predict it — so the doctrine explicitly does
   **not** propose coarsening the clock.
2. *"The field puts hours in timetables; we put them in beats."* A sentence-level
   instruction-versus-narration split came back **33.0% field / 33.5% ours**. No separation. The
   difference is volume, not placement, and only the volume claim shipped.

**Buttons.** Of **92,226 link labels** across the 25 games, **two** name a clock time and both are
explicit waits (*"Wait until 21:00"*); **zero** promise an hour as the outcome of an action. Even
`lust-for-life`, which ships an absolute-time primitive (`$time.setTime(23, 55)`) and calls it 270
times, labels those buttons *"Back home"* / *"Leave"* / *"Go to the SPA"*. Ours: **13 clock-time
labels across four v2 games**, **zero across all four v1 games**.

**Duration tags are one game's convention, not a field norm** — 4,219 of the corpus's 4,260 are
`degrees-of-lewdity`'s, and of the five field games with a minute-resolution clock only that one
does it. That is why C4 shipped as a lint.

### The engine, read rather than assumed

- **No absolute-time advance exists.**
  `grep -E 'target_hour|advance_to|until_time|time_target' v2.py` → **0 hits**;
  `advanceTime(minutes)` (`v2.py:5400`) is the whole API. (`setTime` matches eight times and every
  one is `setTimeout`.) There is no `@time` token either — `_resolve_at_references` (`v2.py:14027`)
  resolves `@player` and `@<npc>` only.
- **Travel time is auto-tagged; activity time is not.** `getLocationCostTag` (`v2.py:4724`) renders
  `20m` on a nav card; a choice's `time_progression_minutes` emits a bare `advanceTime()`
  (`v2.py:12733`) with nothing on the label. A door announces twenty minutes and a 150-minute shift
  announces nothing.
- **`show_when_blocked` + `cooldown_message` exist and no game uses them.** Read at
  `v2.py:11055-11059`, rendered at `v2.py:5140-5145` when `isCanvasValid` fails — and it fails on a
  **schedule miss** first (`v2.py:4573-4580`). Usage across all ten games: **0**.
- **Windows are far too wide to pin an hour.** Median schedule-window width per game runs
  **149–540 minutes**; exactly **5 canvases in the entire repo** have a window of 60 minutes or
  less. No beat shipped here can honestly state the current hour.

### What changed

- **NEW `references/the-clock.md`** — C1 the engine pins one moment · C2 a beat may not say what
  time it is, turn the reading into a rule · C3 a label may not promise a clock time · C4 a label
  that spends the clock says how much · C5 if a thing has hours, publish them · C6 v1's Rule 10
  restored. The worked pair is Off Season's own canvas, which carries both halves on one screen:
  *"Shutter up at eight"* (true for 1 minute of 300) beside *"Nobody comes in before eleven in
  February"* (true always).
- **`scripts/gates.py`** — judged set **35 → 36**, lints **13 → 15**.
  - gate **`the label keeps its time`** — no choice label names a clock time, and a stated duration
    equals the minutes the click actually spends. The duration walk follows choice → target node →
    that node's exit, because Off Season states the tag where the player decides and charges it
    where they leave; reading only the choice would have scored all eight of its honest tags as
    unverifiable.
  - lint **`the clock in the prose`** — every hour a beat names, with the window it has to survive,
    sorted widest-window-first (a canvas with no schedule is treated as the full 1440, which is what
    "fires at any hour" means).
  - lint **`the time cost is not on the button`** — every click that moves the clock 60 minutes or
    more in silence.
- **`SKILL.md`** — world-file list, one scoreboard row, two entries in the lint index.
- **`references/register.md`** — the "what is not measured here" note now hands time to
  `the-clock.md`, and records that this is where v1's Rule 10 went.
- **`references/the-voice.md`** — R1's cost paragraph gains the time half of its own sentence; the
  money half was already gated, the time half never was.
- **`references/the-surfaces.md`** — R2's room-list rules gain the out-of-hours line (C5).
- **`references/engine.md`** — new **§32**, three subsections: no absolute advance and the 3-minute
  default; the travel-versus-activity tag asymmetry; `show_when_blocked`.
- **`DOCTRINE_GAPS.md`** — row 7 status, scoped to the time half.

### Why C2 and C4 are lints and not gates

A shift-driven world names hours as **rules**, and correctly: `seventh_day`'s `rung_kitchen_rota`
and `steam`'s shift board are good work a rate gate would fail. That is this skill's own *"a check
that fails a game for obeying the doctrine is a bug in the check"* — the trap that killed the
proposed `locked_text` gate. And gating duration tags would be the invented threshold `gates.py`
already refuses for stamina-type costs (G21's comment). Both print and neither moves the tally.

### How it was verified

The gate table was produced by a standalone script **before** the gate was written; the shipped gate
reproduces it exactly.

```
                base      new     Δpass   the label keeps its time
off_season      31/35 →  31/36      0     FAIL   2 clock labels · 8 durations all correct
the_allowance   27/34 →  28/35     +1     PASS
seventh_day     26/34 →  26/35      0     FAIL   2
forty_miles     24/34 →  24/35      0     FAIL   1
steam           17/33 →  17/34      0     FAIL   8
back_home       13/31 →  14/32     +1     PASS
vesper           8/27 →   9/28     +1     PASS
last_call       12/25 →  13/26     +1     PASS
late_shifts      9/26 →  10/27     +1     PASS
the_inheritance 12/24 →  13/25     +1     PASS
```

Every denominator moved by exactly one and no existing gate changed on any game. `--json` carries
36 distinct gates and 15 lints, lints outside the tally. Off Season's clock lint prints
`work_arcade_morning`'s rule and its reading side by side on the same 300-minute window and convicts
neither — which is the behaviour the lint exists to have.

### Still open

- **Off Season is not fixed.** Doctrine first, the game as its proof, per LO's standing order.
- **`advanceTime` has no absolute form.** A `time_target` / `advance_to` primitive would make
  *"work till one"* honest and let a work rung close its own window exactly. Surfaced for LO's call,
  not acted on — engine work is out of scope for this stream.
- **`show_when_blocked` has zero shipped instances.** Its first real use will be Off Season's
  repair; until then C5 is a verified capability, not established practice, and says so.

---

## 2026-08-22 — the first hour: the opening, the meetings, and the first visit

**Cause: the same session, the same review, items 2 and 3.**

> *"No NPC introductions… In the start canvas, should it be like this… are we trying to ramp
> things up too fast… I think we still havent learnt how the game should be started."*

`games/off_season/REVIEW_1.md` splits these into §2 (O1–O4) and §3 (N1–N2). The field research
says they are **one mechanism**, so they were done as one pass — LO approved that, 2026-08-22.
This closes `DOCTRINE_GAPS.md` Tier 2 row 6, the last row in that table with an empty status.

### What the research found

**v1 had it and v2 dropped it, and the loss is mechanical.** `author-game/references/onboarding.md`
(269 lines) and `npc-intro.md` (146 lines) have no v2 counterpart. Counting non-repeatable canvases
that fire at a character's location — v1's first-contact shape:

```
v1  the_inheritance 24 · vesper 13 · late_shifts 7 · last_call 0
v2  off_season 0 · the_allowance 0 · seventh_day 0 · forty_miles 0 · steam 0 · back_home 0
```

v2's `starting_canvas` runs a median of **402 words** against v1's **184**, because it has to do
all the introducing itself.

**The field, 25 mopoga games.** An introduction is small and somebody talks — 696 passages named
intro/meet across 18 games run **median 101 words, quartiles 57/101/194, 64% with spoken
dialogue**; narrowed to *meet* only (158) it is median 166 and 55% spoken. the-company's whole
first meeting with the player's employer is 80 words. Our own `the_inheritance/canvas_meet_audrey`
is 125 words and 4 `dialog` blocks — already the right shape.

**Openings are bimodal.** 10 of 20 name nobody (corpo-life 64 w, DoL 193); the rest spend
700–2,600 at ~229 words per named character. Off Season spends **46** and puts none on screen.

**The mechanism is one flag family covering three kinds of thing.** degrees-of-lewdity carries a
first-time flag on 24 of its 27 registered NPCs and uses it to change how the game *refers* to
things — `<<if $wren_intro is undefined>>a <gender> named Wren. <He> can be found at Remy's estate
in the moor<<else>>Wren<</if>>` — and the same family covers places (`$forest_shop_intro`) and
knowledge (become-someone's `$has.auntaddress`). 16 of 25 games carry per-character meeting state,
re-derived independently this pass and matching REVIEW_1's Appendix A.3.

**The finding that landed hardest.** Off Season has a first-visit canvas at 5 of its 10 locations
and **the anchor is not one of them** — the room its ledger declared at 9,000 words, 27% of the
game, whose description says *"forty machines"* and never says of what.

### ⚠️ An engine fact that corrects v1, verified before it was written down

`npc-intro.md` §1.3 says to set `requires_npc` so a meeting *"fires where the NPC is."* On the
auto-fire path that is **false**:

```
getStoryCanvasRedirect v2.py:4921 -> selectAutoFireCanvasForLocation v2.py:4453
  -> isCanvasValid v2.py:4573   (schedules · conditions · repeatability — requiresNpc is not read)
```

`requiresNpc` is emitted at `v2.py:11104` and consumed only at `v2.py:5259` (random encounters) and
`v2.py:5332` (substitutions). So `vesper/cap_renner_hired` at `the_anchor` fires whenever the
player walks in, though Renner drinks there 19:00–23:00. **A straight port of v1 would have shipped
that bug.** Recorded as `references/engine.md` §31; the doctrine tells authors to gate the meeting
on a `schedules` row or a flag instead. **The engine itself was not changed** — a one-line fix to
`isCanvasValid` would tighten every existing `requires_npc` one-shot including vesper's, which is
out of scope; surfaced for LO rather than acted on.

### What changed

- **`references/the-first-hour.md` — NEW, 430 lines.** F1 pick one opening shape · F2 boot and
  capstone are two canvases · F3 hand over into an open door · F4 every live system gets one beat ·
  F5 every hub sits behind a meeting · F6 a meeting is small and somebody speaks · F7 role before
  name · F8 one flag per character · F9 the anchor introduces itself. The rule underneath all nine:
  **the game does not use a name until it has earned it.**
- **`templates/first-hour.toml` — NEW.** Both opening shapes side by side with an instruction to
  delete one, plus the meeting and first-visit skeletons. A **menu**, per `SKILL.md`'s own rule
  that a template is filled in rather than read; every string is a `<placeholder>` and the file was
  checked against the `own_words` lint before it shipped.
- **`scripts/gates.py`** — three gates and one lint. 32 → **35 judged gates**, 12 → **13 lints**.
  Helpers `_fh_handovers` (a branching walk of the funnel's clock), `_fh_live_at`,
  `_fh_meeting_setters`, `_fh_cast_met`, `_fh_declared_anchor`, `_fh_first_visits`.
- **`SKILL.md`** — the three gates in the scoreboard table, the lint in the index, and
  `the-first-hour.md` added to the board-phase world-file list with "read it before you author a
  single canvas."
- **`references/the-release.md`** — a § first-release bullet.
- **`references/the-map.md`** R4 — a button cannot carry the explanation; where the name will not
  tell a stranger what the place is for, the place needs a first visit.
- **`references/the-voice.md`** R1 — a character's name is navigation too: role before name.
- **`references/engine.md`** §31 — the `requires_npc` finding above.
- **`DOCTRINE_GAPS.md`** — Tier 2 row 6 filled.

### The checks

| gate | what it asks |
|---|---|
| **the opening opens a door** | walk `starting_canvas` from `[time] starting_hour`, adding 3 min per undeclared exit (`v2.py:13200`); is anything at the landing location open at that minute? `n/a` when the chain cannot be walked |
| **every hub is met first** | per character: one hub gated on a flag a non-repeatable canvas naming them sets, no hub left with zero conditions, no flag opening a second character's door |
| **the anchor introduces itself** | the anchor declared in `v2_state.json` `board.locations[].fill` has a non-repeatable canvas bound to it; `n/a` with no ledger |
| lint · **named before met** | characters named in the opening / a quest card / a room description with no meeting, and rooms carrying prose with no first visit |

### ⚠️ The meeting gate was wrong on its first run, and the correction is the point

The first implementation demanded that **every** hub of a character carry the meeting flag. It read
`the_inheritance` as 3/5 — failing `aud_sexloop` (gated on `audrey_stage gte 3`) and `last_call`'s
`canvas_marcus_arrangement` (gated on `marcus_drinks_done`). Both are **later rungs**, gated on
something downstream of the meeting, and both are correct work. That is `SKILL.md`'s *"a check that
fails a game for obeying the doctrine is a bug in the check"*, sixth measured instance, caught by
running the gate before writing it up. The shipped rule asks for the meeting on **one** hub and
bans the **cold spawn** — a hub with no conditions at all — on every hub.

### Verified

- `templates/first-hour.toml` parses under `tomllib` — 3 canvases, triggers intact.
- `gates.py` parses; run against all ten games.
- **Every numerator moved only where predicted**, from a standalone predictor written before any
  gate existed:

```
                base     new     Δpass   the three new gates
off_season      31/32 → 31/35     +0     FAIL · 0/4 FAIL · FAIL
the_allowance   26/31 → 27/34     +1     PASS · 1/5 FAIL · FAIL
seventh_day     24/31 → 26/34     +2     PASS · 0/6 FAIL · PASS
forty_miles     22/31 → 24/34     +2     PASS · 0/6 FAIL · PASS
steam           15/30 → 17/33     +2     PASS · 1/6 FAIL · PASS
back_home       12/28 → 13/31     +1     PASS · 0/4 FAIL · FAIL
vesper           8/26 →  8/27     +0     n/a  · 6/9 FAIL · n/a
last_call       10/23 → 12/25     +2     PASS · 4/4 PASS · n/a
late_shifts      8/24 →  9/26     +1     PASS · 0/5 FAIL · n/a
the_inheritance 11/22 → 12/24     +1     PASS · 4/5 FAIL · n/a
```

  No existing gate changed on any game. `--json` carries 35 distinct gates and 13 lints.
- **One v1 game passes the meeting gate at 100% and a second misses by one hub**, so the bar is one
  shipped work has cleared rather than an invented number.
- Two lint bugs found by reading its output and fixed: an NPC named *The Collector* was searched as
  `The` and matched every sentence in `last_call` (titles and articles are now skipped), and rooms
  with zero prose were reported as lacking an introduction when the real defect is that they are
  empty and gate `location fill` already says so.
- **No game file was touched.** Off Season is repaired next, as the proof.

### Still open

- **The anchor gate is an existence check**, which `SKILL.md` warns is the weakest kind. Defensible
  only because the real question here genuinely is existence; the per-location coverage prints in
  the detail lines so it does not quietly become a box to tick. Noted in the code, not hidden.
- **The engine gap is unfixed** (see above) — LO's call.
- **Off Season is not fixed** by this pass. Doctrine first, game as proof.

---

## 2026-08-22 — the words the player has to already own, and the examples that taught the dialect

**Cause: LO played the built Off Season and could not read it.**

> *"the language being used here is tough to get. what is arcade?? … why couldnt we use simpler
> language, are we try to ramp things up too fast"*

The game scores **31 of 32** on `gates.py`. The full review, with all field measurements, is
`games/off_season/REVIEW_1.md` (15 items). This entry covers item 1 of that review only; the
opening, the NPC introductions, the clock and the currency are separate passes to come.

### What the research found

**Our prose is EASIER than the field's, and that is why no instrument caught it.** Flesch Reading
Ease on real sentences (5–60 words, not majority-capitalised, so menus are excluded from both
sides): field median **78.0 / grade 5.5**; off_season **86.8 / grade 5.0 — easier than 24 of the
25 field games**. Gate 19 `sentence length` passes at median 10 words against a ceiling of 14.
Difficulty here is **referential**, not syntactic, and nothing in the skill measured reference.

**The real axis — locale-locked common nouns per 10,000 words:**

```
FIELD (25 games)   0.8   ·   v1 games 1.3–7.3   ·   v2 games 9.4–95.6   ·   off_season 95.6
```

Eleven terms our games use appear in **zero of 25 games across 10.6M words**: `airer, anorak,
bedsit, biro, chandlery, chippy, forecourt, fryers, holdall, lodger, wellies`. The field uses rare
words freely — `orphanage`, `slaver`, `mage`, `shillings` — but those are **invented or generic and
the fiction defines them on contact**. A real regional object cannot be defined that way: it lands
with the reader or it does not, and the prose gets no signal either way.

**Corpus:** `~/Documents/Mopoga_Twine_Sandbox_Research_20260724/gamehtml/` — 28 files, 25 parsing as
Twine stories, 10.6M words of passage prose after macro/markup stripping. Same corpus as the
2026-08-18 meters study, so figures are comparable across passes.

### ⚠️ A measurement in the first draft was wrong by 14× and is kept on the record

The first count reported **`rota` ×44** in the skill. It was a **substring** grep: *p·rota·gonist*,
*rota·ting* and *rota·tion* all contain `rota`. Recounted with word boundaries, and excluding the
history files (`CHANGELOG.md`, `STATUS.md`, `DOCTRINE_GAPS.md`), the live skill carried **27
locale-locked terms across 11 files** — `airer` ×9, `lodger` ×8, `immersion` ×3, `rota`/`rotas` ×3,
`fortnight` ×2, `forecourt` ×1. The defect is real and a quarter the claimed size, and `rota` was
never the main offender. **A measurement that inflates a defect fourteen-fold is the same class of
error as one that hides it.** LO had already approved a `rota` → `roster` rename on the wrong
figure; the rename was still correct, just three edits rather than forty-four.

### Root cause: `SKILL.md` already had the rule, applied only to shapes

No line in this skill has ever said "write British." Its **examples** said it —
`templates/board.toml:147` shipped `costs = "£5 for the immersion"`, a foreign currency symbol and
a locale-locked noun in six words, in the file authors copy hardest.

`SKILL.md` already carried *"an example outranks every rule beside it"*, written after
`the-map.md`'s worked map skeleton reached three games and `15/35/55/75` reached all sixteen
declared tiers. **It had only ever been applied to shapes — a floor plan, a set of thresholds.
Nobody applied it to words.** Third instance of a known mechanism.

### Changes

- **`references/register.md` +77 lines** — new section **"The words the player has to already
  own"**, inserted after *"Sentences run short"*. Four rules: gloss it in the sentence that first
  uses it or use the plain word · name a place for what it is the first time you name it (the
  measured trigger: off_season never once writes *slot machine*, and `amusement arcade` existed
  only in `image_search_queries` and in image `description`, which renders as `alt`,
  `v2.py:13750`) · invented words are safe and real regional ones are the trap · and an explicit
  ⚠️ that **this is not an instruction to write generic** — *specificity the reader cannot decode is
  not specificity.* Second new section **"The examples are the register"**, carrying the correction
  above. Unnumbered `##` headings, matching the file's convention in that region: **nothing was
  renumbered and every `S1`–`S4` reference stays valid.**
- **`SKILL.md`** — the new lint registered in the lint index; the existing *"an example outranks
  every rule"* operating rule extended with the vocabulary instance.
- **De-dialected, prescriptive text only** — `templates/board.toml:147`, `state.md:68` and
  `the-board.md:327` (`"£5 for the immersion"` → `"$5 for the water heater"`, both halves, since
  LO has already settled the currency on a neutral `$`); `lodger` → `tenant` ×6 across `state.md`,
  `the-map.md` ×2, `the-board.md` ×2, `gates.py`; `rota`/`rotas` → `roster`/`rosters` ×3 across
  `the-board.md`, `the-map.md`, `the-release.md`; `fortnight` → `two weeks` ×2.
- **Deliberately NOT rewritten — quotations of real games are evidence.** `the-surfaces.md`'s five
  `airer` lines, `SKILL.md:174`, `the-voice.md:92` and `gates.py:841` all quote `the_allowance`'s
  real canvas *"Get the washing in off the airer"* (`the_allowance/7_final_game.toml:1163`).
  `the-economy.md:73` quotes `forty_miles`' declared obligation (`forty_miles/v2_state.json:376`).
  `gates.py:252`'s `knickers` is inside the frozen explicit lexicon — it exists to *detect* the
  word. Rewriting any of these would falsify the record, the same principle that kept
  `CHANGELOG.md` / `STATUS.md` / `DOCTRINE_GAPS.md` intact through the meters pass. Instead
  `the-surfaces.md` now **glosses `airer` once at first use** — the skill obeying its own new rule.
- **`scripts/genre_words.txt` — NEW, 18,043 words, 145KB.** Every lowercase word used by four or
  more of the 25 field games. Data, not taste: the lint needs no hand-maintained word list.
- **`scripts/gates.py` — one new lint, `lint · the words the player has to already own`.** Prints
  every word in the player's face that fewer than four field games use, ranked by use count.
  Scope is canvas prose **plus choice labels plus location text** — the measured trigger was
  *"Buy a coin mech off the chandlery"*, where both hard words are on a button. Filters are all
  deterministic: possessives, hyphenated number-words, calendar names, and **proper nouns**, the
  last detected as a token capitalised in >60% of its non-sentence-initial uses, plus every name
  the game declares in `[[npcs]]` and `[[locations]]`. Lint count **11 → 12**.

### Why it is a LINT and not a gate

The rate does not discriminate. With names, months and number-words filtered out: off_season 254
per 10k, forty_miles 245, steam 219, **vesper 190 — and vesper reads fine**, the_inheritance 169,
back_home 131. What separates them is what the words *are*, which is a judgement. **A word list
dressed as a threshold is `DOCTRINE_GAPS.md` Appendix C trap 5**, and this pass did not repeat it.
The check hands over the list; the author makes the call.

### Verified

- **All ten games re-scored, identical to the baseline captured before any edit** — `off_season
  31/32 · the_allowance 26/31 · seventh_day 24/31 · forty_miles 22/31 · steam 15/30 · back_home
  12/28 · vesper 8/26 · last_call 10/23 · late_shifts 8/24 · the_inheritance 11/22`. This pass adds
  no gate, so any movement would have meant a broken edit.
- `--json` intact: **32 gates, 12 lints**, `own_words` present, lints outside the tally.
- `templates/board.toml` parses, before and after, with each placeholder filled uniquely in key
  position and numerically in value position. *(Two earlier "parse failures" were bugs in the fill
  harness — collapsing `<tier_1>`/`<tier_2>` to one key, and leaving a bare identifier as a value.
  The template was never broken.)*
- Lint output read by eye on all ten. off_season returns `cardigan ×8 · fortnight ×8 ·
  immersion ×7 · extractor ×6 · fryers ×6 · jumper ×6 · fifties ×5 · chandlery ×4 · mech ×4`;
  vesper returns `sternum ×35 · emitter ×23 · readout ×15 · coveralls ×7`. **Both lists are
  correct, and only one of them is a defect** — which is the argument for a list over a score,
  visible in the output itself.
- One bug found and fixed by reading that output: `rstrip("'s")` strips *any* trailing `s`, so the
  first run reported `goe ×27`, `thi ×27`, `mattre ×12`. Replaced with a literal possessive strip.

### Known and accepted

- **The lint blocks nothing.** Correct for a judgement axis, and it also means a hurried author
  sails past it. The rule in `register.md` is the instrument; the lint only makes the words visible.
- **145KB of data in a skill folder** — the largest non-prose artefact this skill carries. Bought
  deliberately: it removes opinion from the check.
- **`forecourt` survives once** in `the-economy.md:73`, inside a quoted obligation. Left, per the
  evidence rule above.
- **No game file was touched.** Off Season is repaired in a later pass, as the proof — three
  doctrine passes now carry *"nothing here is proven by a built game"* and that is the one open
  caveat this work does not yet close.

---

### Audit pass, same day — what the first implementation got wrong, and two classes it missed

LO asked whether the same language problem sits elsewhere in the skill and whether the fix was
actually implemented properly. Both halves found real things.

**Four inaccuracies in the section as first written, all corrected:**

- *"Four of those words"* in the worked quote — there are **three** (`meter`, `jumper`,
  `eiderdown`). Now named individually rather than counted.
- The `0.8 vs 9.4–95.6` table was presented as **"Measured"** with no note that its instrument is a
  **curated list of ~40 regional terms**. It is a judgement and now says so, one line above the
  table.
- *"the building the player spends 27% of the game in"* — 27% was the **declared budget**. As built
  the arcade holds **13%**, and `the_chip_shop_flat` is the de-facto anchor at 18.6%. Corrected,
  with the built figure beside it.
- The section quoted **190 / 254 per 10k** from a scratch script, not from the shipped lint.
  The lint's own numbers across the ten games are **91–205**, v1 and v2 fully interleaved, with the
  lowest (`seventh_day` 91) and the highest (`off_season` 205) both v2 games. That is a *stronger*
  argument for a list over a score than the one first written, and it replaced it.

**One prescriptive example missed by the first sweep, found by searching case-insensitively:**
`the-voice.md:35` taught *"The Box Room becomes **The Lodger's Room** and says who and why in two
words"* — and `lodger` is used by **zero of the 25 field games**. `the-map.md:152-158` had already
caught that `The Box Room` was unreadable and **kept the locale-locked cure without noticing**.
**`steam` and `off_season` both ship a location literally named "The Lodger's Room."** Now *The
Tenant's Room*, in both files, each carrying a note about what it used to say.

**Two whole classes the original rule never covered, and they are worse than the one it did.**
A word can fail three ways, and the rule was written for the mildest:

| | the reader gets | measured |
|---|---|---|
| **unknown** (`airer`, `chandlery`) | a blank | the class the skill's examples taught |
| **ambiguous** (`half seven`) | **a confident wrong answer** — 7:30 here, 6:30 across much of Europe, not used at all in American English | **157 uses across six games** vs **4** of `half past` |
| **false friend** (`vest`, `tea`, `bonnet`) | **a confident wrong picture** | `forty_miles` *"You get the vest up over your tits"* — an undershirt here, a waistcoat to most readers, **inside an explicit beat**; `off_season` *"Stay past the tea"* — **on a quest card**; `seventh_day` *"under the bonnet"* |

**The skill is clean of both** — `vest`, `tea`, `bonnet`, `half seven` return zero hits across every
reference file and template. These came from the authors, not from the examples, which is a
distinction worth keeping: **not every language defect in a game traces back to the skill.** The
rule now covers all three classes anyway, because the rule is what has to stop it next time.

**The lint gained a second half, and it had to be curated.** A false friend is *by definition* a
common word — `vest`, `tea`, `bonnet` and `boot` are all in `genre_words.txt`, so the data-driven
half is **structurally blind** to exactly the worst class. The new half is a short hand-verified
list plus one regex for `half <hour>`, labelled `[ambiguous]` / `[false friend]` in the output and
flagged as curated in the footer. It discriminates where the data-driven half does not: **`vesper`
reports 0 ambiguous** and reads fine; `forty_miles` reports 43 and `vest` ×73.

**Explicitly out of scope, and said so in the rule: spelling.** *Colour*, *grey*, *realise*,
*behaviour* cost a reader nothing and were **not** swept — the skill and its games keep them. Only
`tyre`/`tire` and `kerb`/`curb` are named, because those change the word rather than its dress.
Sweeping spelling would be the "write generic" overreach the section's own ⚠️ warns against.

**Re-verified after the audit:** all ten scores still identical to the pre-edit baseline · 32 gates
· 12 lints · `templates/board.toml` still parses · `false friend` false-positive risk stated in the
footer, with `vesper`'s `torch` (a *cutting* torch, correct everywhere) named as the worked example
of one.

---

## 2026-08-19 — meters by OWNER: who climbs, what a throttle is for, and no number that nothing reads

**Cause: LO asked whether `the_allowance`'s four meters are how the top games are built.**

> *"Allowance defines nerve, seen, price, appetite — is this how mopoga top games are designed?? Also
> see how v1 does it?? … then share your honest thoughts on how our v2 should do it."*

They are not a design. They are a **template fill**. `templates/board.toml` handed the author three
blank `<tier_N>` slots, `purity = 100 # optional counterweight`, a fixed volatile list
(`arousal/energy/hygiene/money`), and `the-board.md` §3 instructed: *"their rungs sit at 15/35/55/75…
**copy that shape.**"* All five v2 games copied it, rungs included:

```
                 tier meters   lowest rung   NPC share of meter-gating
the_allowance    4 + standing       15                 20%
seventh_day      3 + grace          15                 22%
forty_miles      3 + count          15                 20%
steam            3 + propriety      15                 29%
back_home        3 + pride          15                 29%
```

**Root cause:** this skill documented **what a climb costs** (`the-meters.md` M1–M7) and **what a
need shuts** (M8–M10) and never documented **which meters should exist or who owns them.** The
decision that comes before both was missing, so a template made it five times.

### The corpus, and the correction that had to come first

25 mopoga sandboxes, SugarCube passage source,
`~/Documents/Mopoga_Twine_Sandbox_Research_20260724/gamehtml/` — the same corpus as the register
pass. Variables extracted per game: writes (`<<set>>` / `<<run>>`, including `+=`, `++` and
self-referencing `to $x + n`), reads (`<<if>>` / `<<elseif>>`), property-level (`$player.corruption`,
not `$player`), plus per-game sidebar passages.

> ⚠️ **A CLAMP GUARD IS NOT A GATE.** `<<if $lust lt 0>>` followed by `<<set $lust to 0>>` is the
> author bounding a variable. `corpo-life` carries **2,889** of them on one variable, and the first
> pass reported that meter at **3,235 gates** when the real figure is **346**. Every figure below
> counts only comparisons against a threshold strictly inside the meter's own range. Recorded in
> `DOCTRINE_GAPS.md` Appendix C as trap 5 — same family as the quote-only dialogue count that
> wrongly retired v1's Rule 4: **an instrument that cannot tell a guard from a gate does not report a
> smaller number, it reports the wrong one.**

**Player-owned ascent meters with ≥4 real content gates:**

```
0 meters   14 games   adam-and-gaia · become-taxi-driver · course-of-temptation · destroyer ·
                      growup · inseminator · love-and-vice · lust-for-life · new-life-project ·
                      new-lust · realm-of-corruption · sluttown-usa · wasteland-lewdness ·
                      zaras-school-life
1 meter     7 games   amore · apocalyptic-world · become-someone · corpo-life · family-business ·
                      patriarch · the-hellfire-club
2 meters    2 games   friends-of-mine · the-company
8 meters    family-ties          9 meters   degrees-of-lewdity          MEDIAN 0
```

The largest unclassified meter in each of the 14 zeroes was hand-checked — resources (`Wood`,
`gunpowder`, `groceries`), story counters (`indiastory`, `officestory`), levels. No hidden tiers.

**`the_allowance`'s shape is matched by 2 of 25 games, and one of them is DoL — the game v2's
three-layer model was derived from.** We generalised from n = 1 and built five games on it.

**Where the field's gating lives: on the CAST, and the distribution is BIMODAL.** 285 per-character
meters against 101 player-owned ones (2.8 : 1). Share of character-meter gating carried by
per-character meters:

```
ROSTER  zaras 100% · adam-and-gaia 100% · taxi 91% · become-someone 84% · hellfire 80% ·
        patriarch 79% · love-and-vice 73% · family-business 65%                        (8)
────────────────────────────────────────────────────────────────────────────────────────
LADDER  new-lust 15% · friends-of-mine 13% · corpo-life 12% · destroyer 12% · DoL 10% ·
        wasteland 5% · family-ties 0% · the-company 0% · sluttown-usa 0%               (9)
```

**Nothing between 15% and 65%.** Ours: 20 · 22 · 19 · 29 · 29 — all five inside a band no shipped
game occupies, because the question was never asked. v1 asks it
(`author-game/references/content-framework.md`, *"Who climbs?"*); v2 dropped it.

**Rung structure of the field's live ascent meters** (content gates only):

```
family-ties  you.corr      978 gates  17 rungs   5,10,15,20,25,30,33,35,40,45,50,60…
friends      feminine      443 gates   8 rungs   5,10,15,25,30,40,50,75
corpo-life   lust          346 gates  11 rungs   10,21,24,31,41,50,61,70,80,90,99
become-som.  mc.dom         96 gates   9 rungs   5,7,10,15,20,25,30,50,75
the-company  player.horny   24 gates  11 rungs   2,20,30,40,49,50,60,70,80,90,99
DoL          exhibitionism  21 gates  11 rungs   15,19,25,35,40,50,55,60,75,80,95
```

**8–17 rungs, lowest at a median of 5.** Ours: 3–4 rungs, and **all 16 declared tiers across five
games put their lowest rung at exactly 15** — fifteen free clicks before anything changes, against
M1's own measured finding that 12 clicks moved `cover` 4→16.

**The sexual-state meter is a real gate in 12 of 25 games**, and where it exists it is the #1 or #2
most-gated thing in the game (`corpo-life` lust, DoL arousal, `family-ties` you.arousal,
`friends-of-mine` excitement). Ours, grepped:

```
                arousal raises   arousal reads
the_allowance         25              0
seventh_day           53              0
forty_miles           52              0
steam                 55              2
back_home             47              2
                     232              4
```

**The cause is one line of this skill's own template.** `templates/board.toml` labelled the volatile
layer *"NEVER gate an arc on these"* — right about the ODOMETER, silent about what a THROTTLE is for
— and five authors read it as "never gate on it at all". Structurally it is the same defect the
register pass fixed: a throttle gates a repeatable act surface, v2 taught no such surface until
2026-08-18, so arousal had no job.

**Counterweights:** 1 field game in 25 ships one that gates (DoL `purity`, 84 sites). Ours: 4 of 5,
and three gate almost nothing — `count` 0 reads, `standing` 2, `grace` 5; `propriety` reads 25 times
and every one is a `[group]` prose band, which colours a paragraph and opens no door.

**What survived the corpus unchanged:** the three-layer frame itself, the HUD count (field median
4–5 meters shown against 20–260 gated; ours 4–7), and all of M1–M10.

### What v1 has that v2 never carried

`author-game/references/trait-design.md` (237 lines) + `trait-catalog.md` (248): spine-by-arc-shape
(including **no climbing meter at all** for someone she already belongs to), **odometer vs
throttle**, the **dead meter** as a named anti-pattern, reserve-the-rich-model-for-1–2-arcs, and
"Who climbs?" in `content-framework.md`. v1's own games measure roster-shaped: `vesper` has **zero**
player ascent gates and runs on per-NPC `corruption` (33 gates, 8 rungs) + `relation` (24).

### LO's decisions

- **2 hard gates + 3 lints** — hard-gate only what is deterministic or checkable against the
  author's own declaration; print the rest as numbers.
- **`who_climbs` is a DECLARATION checked against the game**, never a threshold invented across a
  bimodal population.
- **No game is touched.** Doctrine, template and `gates.py` only.

### What changed

**`references/the-meters.md`** (+248 lines, 277 → 521). New leading part, **"Which meters exist, and
who owns them"**, placed before M1 and numbered W1–W6 so every existing M-reference stays valid:

- **W1 · Who climbs** — the fork, the two schools with their populations, the table of what each
  answer looks like on a board, and the instruction to declare it.
- **W2 · A throttle's job, stated positively** — odometer vs throttle, what each may and may not
  gate, the 232 : 4 measurement, and the template line that caused it.
- **W3 · A number nothing reads is not a meter** — with the per-game dead lists.
- **W4 · The ladder** — 8+ rungs, lowest around 5, dense at the bottom; retires 15/35/55/75 and
  names where it came from.
- **W5 · A counterweight is rare, and it shuts doors.**
- **W6 · The cast's meters** — light or load-bearing, W1 decides which; v1's arc-shape table adapted,
  including the no-meter row.

**`references/the-board.md`** §3 rewritten (74 → 100 lines) — the teaching moved to `the-meters.md`;
§3a declares `who_climbs`; **"copy that shape" deleted**; the DoL tier table kept as evidence with
its provenance stated (2018 seed twee source, which is why it does not match a passage-level read of
the 2026 build); a note that band boundaries are the sidebar's business and are not the rung ladder.

**`templates/board.toml`** — the file that actually caused this. `15/35/55/75` gone from the band
block (bands are now `<band_N_top>` placeholders in the file's existing bare-token style, so there
are no numbers to copy); the fixed volatile list replaced by a **menu with a delete-what-you-cannot-
name instruction**, matching the treatment `needs` already had on the same page; the "NEVER gate an
arc" comment rewritten to carry both halves; `purity` commented out with the 1-of-25 figure; a
`who_climbs` header block; and the NPC `{ relation = 0, lust = 0 }` pair labelled as the ladder
school's answer with the roster school's shape beside it.

**`references/state.md`** — `board.who_climbs` and `board.characters[].meters` added to the schema
with field notes; the `ascent_tiers` note now says an empty list is legitimate.

**`scripts/gates.py`** — 2 gates + 3 lints. **30 → 32 gates, 8 → 11 lints.**

New helpers: `_walk_paths` · `_traits_read_anywhere` (three readers: conditions, `costs`, quest
`when`/`goals`) · `_player_trait_raises` (attributes each raise to its canvas) ·
`_engine_read_stage_traits` · `_school_split` · `_meter_rungs`. `_traits_read_by_conditions` is left
untouched so G29's verdict does not shift under it.

**G33 · a meter is read.** Deterministic. `costs` counts as a read — the engine filters an
unaffordable choice rather than letting it fail (`engine.md` §27), and calling that dead would fail a
game for using the engine's own resource gate. **`<npc>_stage` is exempt** when the prefix names a
declared character, because `applyAndNotifyTrait` is its reader (`v2.py:5549-5554`) — written in
advance rather than after a bug report, per SKILL.md's "check the skill before blaming the game".
`sex_stage` is **not** exempt; no character is called `sex`.

**G34 · the climb is where you said it is.** Declare-then-check against `board.who_climbs`; the
player side is whatever `board.ascent_tiers` names, so no keyword classifier decides what counts as
a meter. Quest-card reads excluded on both sides — a guidance card describes progress, it does not
gate access.

### Predictions, computed before the code was written — all reproduced exactly

```
                 G33 a meter is read                                    G34
the_allowance    7/9    dead: arousal · hygiene                  FAIL   n/a
seventh_day      14/16  dead: arousal · stress   (6 _stage exempt) FAIL  n/a
forty_miles      4/8    dead: arousal · count · energy · stress  FAIL   n/a
steam            6/7    dead: energy                             FAIL   n/a
back_home        6/8    dead: hygiene · money                    FAIL   n/a
vesper (v1)      36/41  dead: sex_stage · sex_entry_origin · +3   FAIL   n/a
last_call (v1)   10/15  dead: sex_stage · sex_reactions · +3      FAIL   n/a
late_shifts (v1) 3/7    dead: arousal · energy · hygiene · money  FAIL   n/a
the_inheritance  10/10                                           PASS   n/a
```

One game passes, and it is a v1 game — the gate discriminates rather than condemning everything. The
carve-out was verified both ways: `seventh_day`'s six `*_stage` keys are exempt, `vesper`'s
`sex_stage` (81 raises across 26 canvases, 0 reads) is not.

G34 reports **n/a nine times** — no game declares `who_climbs`. That is correct (`SKILL.md`: an
absence is not a pass) and it means **the gate fires on nothing until the next game is authored.**
Recorded plainly rather than counted as a green.

Two findings the failure lines surfaced that nobody was looking for:

- **`vesper` declares player `corruption` and never touches it** — all 8 raises and all 33 gates are
  `subject = "npc"`. Verified by direct parse.
- **`the_allowance` gives two of its five characters a full meter pair and zero gate sites**
  (`npc_denise`, `npc_col`).

### Lints, first run

**the meter ladder** — `the_allowance` 4 tiers, median 4 rungs, lowest 15 · `forty_miles` 3/3/15 ·
`seventh_day` 3/3/15 · `steam` median 4, lowest 15 · `back_home` median **9** rungs, lowest 15.

**the cast's meters** — every v2 game: **1 distinct meter shape across the entire cast.**
`the_allowance` 5 characters / 13 gate sites / 2 gate nothing · `seventh_day` 6 characters / 8 gate
sites total · `back_home` 4 characters / 50.

**the counterweight** — `count` 0 reads · `standing` 2 · `grace` 5 · `propriety` 25 · `pride` 17.
Heuristic (a player trait starting at 50+ whose effects mostly fall, declared needs and
`trait_decay` keys excluded), which is why it is a lint and not a gate.

### Scores

```
                before      after
back_home       12/27   →   12/28
steam           15/29   →   15/30
forty_miles     22/30   →   22/31
seventh_day     24/30   →   24/31
the_allowance   26/30   →   26/31
vesper           8/25   →    8/26
last_call       10/22   →   10/23
late_shifts      8/23   →    8/24
the_inheritance 10/21   →   11/22      ← the only game to GAIN one
```

### Also corrected, because they contradicted the new doctrine

- **`SKILL.md`** — the two gates and three lints registered; the board-phase dispatch now opens with
  W1; and a new operating rule earned by this pass: **a shape that ships in `templates/` is copied
  harder than one that ships in `references/`.** A reference file is read; a template is *filled in*,
  so whatever sits in the slot is the answer unless the author fights it. This is the
  "an example outranks every rule" rule one level worse — in a template, even a placeholder list is
  an example.
- **`DOCTRINE_GAPS.md`** — Tier 2 items 5 and 8 marked addressed; a **⛔ SUPERSEDED** block on the
  three-layer model recording that it was n = 1, kept rather than deleted because the trail is the
  point; Appendix C's traps 5 → 6 with the clamp guard.
- **`STATUS.md`** — carried the same three-layer table including the 15/35/55/75 rungs. Rungs
  removed from the row, correction block added. Left contradicting, it would have re-taught the
  thing this pass deleted.
- **`scripts/gates.py`** `ASCENT_TIERS` constant — annotated as an n = 1 fallback for guessing when
  `board.ascent_tiers` is absent, not a target.

### Honest credit, and it cuts against the summary

**`back_home` has the best meters we have built** — 8, 9 and 10 rungs on its three tiers, dense at
the bottom, and its per-character `lust` read 36 times. That is the closest thing we have to the
field shape, and it is a game previously written off as a failed test. The doctrine says so rather
than treating all five v2 games as equally wrong.

### Known and accepted

- **`the_allowance`'s `hygiene` is now counted twice** — by G29 (a declared need nothing reads) and
  by G33 (a raised meter nothing reads). Both are true and they ask different questions; it is one
  defect appearing on two lines, not two defects.
- **G33 can be satisfied cheaply and wrongly.** One throwaway `arousal >= 1` per dead meter and it
  goes green — the deleted gate 22's failure mode in a new coat. The check can only ask whether a
  reader exists; W2 is what says the reader has to be the act menu, and the meter-ladder lint prints
  the rung count beside it so a one-rung fig leaf shows.
- **The 60% / 25% cut points in G34 are judgement**, sitting inside a measured empty band. First
  thing to revisit if they fire on a game that reads well.
- **The counterweight lint is a heuristic**, because nothing in the TOML declares "counterweight".
- **Nothing in this pass is proven by a built game.** Third pass running with that caveat. The first
  game authored on these rules is the real test.

### Verified

`python3 scripts/gates.py <slug>` on all nine games — 32 gates, 11 lints, exit 1 throughout (gates
failed, not an error). `--json` emits all 11 lints. `templates/board.toml` still parses as TOML once
its placeholders are filled. Grep sweep: `15/35/55/75`, `copy that shape` and `NEVER gate an arc`
survive only inside the correction blocks that quote them. `git status` shows only
`.claude/skills/author-game-v2/`, plus the pre-existing `issue.md` and `games/vesper/.find-media/*`
this session did not create.

---

## 2026-08-18 (2) — register is SIX SCREEN KINDS: the clip rides the beat, the loop is a machine, people talk

**Cause: LO played `vesper` and named three things, all three real.**

1. *"a canvas that says blowjob shows its media on top and its content on the bottom… the third link
   is suck him, at that time it doesn't show that media, which it has already shown on top."*
2. *"For dialog, we have dialog blocks in each canvas/beats that can be used."*
3. *"there is a way repeated content is written and a way linear content is written even for sexual
   content… in a linear canvas one-time one, it doesn't set things up, instead it directly takes
   player to fuck/penetrate."*

Then: *"learn more from the top games, and not just see what was wrong on v1."*

**Root cause, one thing:** this skill wrote rules about "prose" in general when the property that
actually varies is **which kind of screen you are on**. `register.md` was 174 lines covering four
topics against v1's 779. The missing material was never judged and rejected — one rule was deleted on
a broken measurement (below) and the rest was simply never written.

### The corpus, and the two corrections that had to come first

25 mopoga sandboxes, **58,163 passages**, `~/Documents/Mopoga_Twine_Sandbox_Research_20260724/gamehtml/`.

- **Count one rendered path, not every branch.** `destroyer:ginablow` is eight `<<if>>` branches
  printing the same four words over a different image. Collapsing chains moves the corpus median
  from 115 words to **88**, and DoL from 82 to **54** — in line with its known figure.
- **Speech is a UI component, not punctuation.** 20 of 25 games render dialogue through `<<speech>>`,
  `<<say>>`, `<<nm "Karlee" "…">>`, `<<chat portrait "…">>`, `<div class="npctextbox">`, or one
  container macro per character (`<<Mc>>`, `<<AmyBd>>`). Each game's convention was read out of its
  own source before anything was counted.

**The six kinds** (n = 54,630 screens with content, one path each):

```
kind of screen             n      words   spoken   picture   clips   exits
room / hub             1,226         30       0%      41%       0       5
one-liner / stat tick  7,278         14       4%      21%       0       1
talk screen           15,774         55      65%      64%       1       1
ordinary scene        21,465         71      14%      36%       0       1
sex — act menu           164        107       8%      91%       1       5
sex — few exits        1,068        305      18%      86%       2       3
sex — one way on       7,161        228      28%      92%       3       1
a REVEAL BEAT          3,005         37        —      58%       1       —
```

### C1 · The clip does not ride the beat — and it is an engine fact

A cascade renders as nested `<<linkreplace>>` (`v2.py:13952`, `body_html` emitted inside the
linkreplace body): every beat **appends** and nothing is removed, so the node-lead clip illustrates
beat 0 and nothing after it. Node routing is the opposite — resolved at BUILD time
(`v2.py:13258`) into a real passage, so the screen **swaps**.

```
a click that reveals more content — does it bring its own clip?
FIELD   3,005 reveal beats, 58% (apocalyptic-world 64 · become-taxi-driver 71 · destroyer 79)
OURS    vesper 16/389 = 4% · back_home 0/169 · steam 0/623 · forty_miles 0/938
        · seventh_day 0/516 · the_allowance 0/39
```

Media in our games sits on **nodes** (20–54%) and never on beats, while v2 games moved nearly all
content into beats — `forty_miles` ships 938 beats against 259 nodes. Field density inside explicit
content: **one clip every 58 prose words** (IQR 25–104, n = 25,502 gaps); ours, one every 178–435.

### C2 · v1's dialogue rule was deleted by a broken instrument

`DOCTRINE_GAPS.md` Study 4 counted speech by looking for `"quote marks"`, reported a field median of
**33:1** and a spread *"far too wide to threshold"*, and `register.md` dropped v1's Rule 4 on that
basis. Re-measured on the same corpus with each game's own convention:

```
game                 quotes only    + its own speech UI
corpo-life               584.9:1               0.30:1
sluttown-usa             762.0:1               0.63:1
family-business            >999:1               1.15:1
destroyer                 71.7:1               1.44:1
the-company              290.1:1               2.69:1
degrees-of-lewdity         3.6:1               3.62:1   <- unchanged
course-of-temptation       4.6:1               4.57:1   <- unchanged
patriarch                  2.9:1               2.93:1   <- unchanged
MEDIAN                    65.3:1               2.93:1
games at <=2:1                  0             10 of 25
```

The three that do not move are the three that punctuate speech with quote marks — and DoL and
`course_of_temptation`, the two the study named as the dialogue-heavy outliers, are two of them. The
study found the two whose dialogue its instrument could see. The "over 400:1" that killed the rule is
`corpo-life`, which is **70% spoken**.

### C3 · The ladder, wrong in both directions

Field screens open on a rung evenly (touch 13 · strip 15 · hands 11 · oral 14 · vaginal 28 · anal 5
· finish 13) because a field screen is ONE rung and the ladder is chained across 3–4 of them. Ours,
measured by `gates.py`'s own ladder lint:

```
vesper       77% of explicit canvases OPEN at vaginal-or-above, 0% stop below oral
forty_miles   5% open at vaginal-or-above, 69% never reach oral
```

Vesper is the whole ladder with no stairs to it; forty_miles is all stairs and no ceiling. *Not* a
general rushing problem: our run-up is longer than the field's (59–207 words before the first
explicit word against 30) and 0% of our canvases open explicit against the field's 22–28%.

### C4 · The mechanism for repeatable acts exists, is engine-native, and no v2 game uses it

v1's sex-loop is the field's `ginablow` shape as a state machine — act node per rung with its own
pool, self-loop raising a hidden meter, switch links, a meter-gated finish, a `[group]` finisher, and
a reset at both ends. `vesper:loop_bastien_backroom` ships it. Verified engine support:
build-time node resolution (`v2.py:13258`), a dedicated HUD index for triggerless sub-menus
(`setup.sub_menu_parents`, `v2.py:3159`), and the flag-in-triggerless hard-fail that forces trait
state (`engine.md` §16).

```
self-loop choices:  vesper 22 · every other game 0
loop state traits:  vesper, last_call, the_long_summer only
```

v2 games use half of it — steam 203 triggerless canvases, forty_miles 214 cross-canvas node routes —
but every one is a rung: route in, play a cascade, leave.

### What changed

- **`references/register.md`** (174 → 362 lines). Kept the explicit-beat pivot rule, sentence length
  and second person unchanged. Replaced "the other ninety percent" with the six-kind table as the
  file's spine, and four rules under it: **S1** the clip rides the beat · **S2** one canvas is one
  rung · **S3** somebody speaks (carrying the two-instrument table so the artifact cannot be
  re-derived) · **S4** the talk screen is a content kind.
- **`references/the-surfaces.md`** — new **R3b · Two machines**: cascade appends and suits a one-time
  scene, node routing swaps and suits a repeatable act surface. The loop taught as six parts plus a
  **menu of three shapes** (single-act · pose ladder · paged service) — no copyable TOML, per
  `SKILL.md`'s teach-a-menu rule and LO's explicit choice this session.
- **`references/engine.md`** §8 — *"A node link SWAPS the screen. A cascade beat APPENDS to it"*,
  with both citations, the `sub_menu_parents` index, and the distinction that a triggerless canvas is
  a **safe node-link target and an unsafe substitution target**. §5 gained the corollary that a clip
  inside a beat renders at that beat.
- **`references/the-voice.md`** R1 — act-menu labels name the act and are crude at the ceiling
  (*Keep blowing · Pound her ass · Cum*), explicitly distinct from a plain room-list button.
- **`scripts/gates.py`** — two gates and three lints; `EXPLICIT_BEAT_MEDIA_FLOOR = 50.0` and
  `NARRATION_DIALOGUE_CEILING = 5.0`, each carrying its full derivation. Gate count 28 → 30, lints
  5 → 8.
- **`DOCTRINE_GAPS.md`** — Study 4 §3b struck through with a superseded block rather than deleted;
  Appendix C gained the two new extraction traps.
- **`SKILL.md`** — the leftover objects/gate-22 paragraph at `:59-64` deleted (it contradicted
  `:146-152` of the same file, which said both were removed); the two gates and three lints
  registered; new operating rule: **an instrument that cannot see a thing reports its absence, not
  its rarity.**

### The new checks, and every game measured against them first

```
                    an explicit beat carries a clip        somebody speaks
back_home            10/75   13%   FAIL                    24.1:1  FAIL
steam                 1/65    2%   FAIL                    18.7:1  FAIL
forty_miles           1/170   1%   FAIL                    31.1:1  FAIL
seventh_day           0/118   0%   FAIL                    62.0:1  FAIL
the_allowance        10/12   83%   PASS                    50.4:1  FAIL
vesper (v1)          43/47   91%   PASS                     2.8:1  PASS
last_call (v1)          n/a                                  6.6:1  FAIL
late_shifts (v1)      0/1     0%   FAIL                    15.3:1  FAIL
the_inheritance (v1)    n/a                                  1.5:1  PASS
```

Both gates were computed against all nine games **before** either was written, and both reproduced
their predictions exactly. The clip gate discriminates the way it should: it passes the two games
whose explicit content sits on nodes and fails the four that moved it into media-less cascades.

Lints, first run: talk screens — vesper 26% (field 29%), steam 5%, forty_miles 1%, back_home /
seventh_day / the_allowance **0%**. Act menu — vesper 8 loops against 8 one-shot cascades; every v2
game **0 loops** against 11–47 one-shot cascades.

### Scores

```
                before      after
back_home       12/25   →   12/27
steam           15/27   →   15/29
forty_miles     22/28   →   22/30
seventh_day     24/28   →   24/30
the_allowance   25/28   →   26/30
```

`the_allowance` gains a pass because its explicit beats already carry their clips. The other four
lose ground on both new lines, which is the point.

### Decisions and open items

- **LO chose two gates plus three lints**, not five gates: gate only what the corpus settles
  decisively, print the rest. And **the loop is taught as a menu of shapes, not a copyable skeleton.**
- **No game was touched.** vesper stays as authored; the other four stay as specimens.
- **The 5:1 ceiling is the one judgement call here.** The measured facts are a median of 2.93 and ten
  of twenty-five under 2:1; 5:1 is how much slack to allow. First thing to revisit if it ever fires
  on a game that reads well.
- **The clip gate can be satisfied cheaply and wrongly** — stapling one pool onto every beat passes
  it. That is the gate-22 failure mode in a new coat. The mitigation is in the rule, not the check:
  the clip must be the clip for *that* rung, and the ladder lint prints beside it.
- **Nothing here is proven by a built game.** Third pass running with that caveat, and it has been
  the honest one each time.

---

## 2026-08-18 — rooms serve NEEDS, activities carry WALK-INS, buttons carry VERBS

**Cause: LO opened `games/the_allowance` in the kitchen and read five buttons.**

```
Look round the kitchen · Sit out on the back step · Come down in what you slept in
Get the washing in off the airer · Ask for more than you need
```

*"All are a complete mess… what can be done in the kitchen, person can eat, cook, eat with the other
people… check the fridge for what is in stock."* And then the diagnosis: *"objects in a room, and
then things can be done in that room, will always end up with a mess like this, which means
nothing."*

He was right on every count, and it is measured rather than argued.

### The corpus this pass is measured against

Full HTML of 25 top-30 mopoga sandboxes, on disk at
`~/Documents/Mopoga_Twine_Sandbox_Research_20260724/gamehtml/`. Every link label extracted —
**64,594 of them**:

```
sleep / go to bed .... 773 uses, 19/25 games      wash / shower ....... 224, 16/25
work / shift / earn .. 564, 18/25                 exercise ............ 122, 16/25
get dressed .......... 487, 14/25                 dishes / laundry ..... 51, 11/25
eat / breakfast ...... 430, 17/25                 fridge / stock ....... 44, 13/25
                                                  cook ................. 27,  8/25
"look around" ........ 232, 14/25  ← and sampled, these are one-off quest objects
                                     ("examine the cash register" x16), never a room menu
```

Four kitchens read in full: **Apocalyptic World** (`Eat` needs food + 30 min, `Approach <her>`,
`Talk with Blair`, `Back`), **Become Someone** (breakfast / dinner / dishes, once each per day, in
windows, plus a portrait row), **Corpo Life** (one `if/elseif` on partner x time, two links a
branch), **Degrees of Lewdity** (farm kitchen = **341 bytes**: a stock line, `<<kitchenDisplay>>`,
`Leave`). **Not one browses an object.**

### Five causes, all verified

1. **The skill's worked example was read backwards.** `the-surfaces.md` printed DoL's bedroom as
   *"what correct looks like"* and read it as *choices hang off objects*. The real passage's standing
   links are `Strip and get in bed` (the **sleep machine** — how the day advances), `Masturbate in
   bed` (the solo feeder), `Wardrobe` (the clothing system), `Sex toys`, `Mirror` (the body system).
   **The bed is the door to the machine that runs the game.** We copied the sentence and dropped
   what was behind it.
2. **Gate 22 could not see a canvas, so it manufactured a duplicate menu.** `_room_objects`
   computed affordances from `exit_block.choices` and never read a canvas name. The four kitchen
   activities exit via `type = "location"` and carry no choices, so *"Get the washing in off the
   airer"* — an entire canvas about the airer — counted as **zero**. Proved by probe: strip the nine
   `room_*` screens from a scratch copy of the_allowance and the gate reports **34 of 39 declared
   objects unusable**, naming *"the airer"* and *"the back step"*. The only way to pass was a second
   screen re-listing what already existed; the author wrote that reasoning into
   `3_activities.toml:1280-1294` themselves. Result: **nine near-verbatim duplicate pairs across
   five rooms** — *"Two concrete steps down to a yard with a wheelie bin and a rotary line nobody
   uses"* / *"Two concrete steps to a yard with a bin and a rotary line nobody uses"*, one free and
   one charged.
3. **The needs layer was never built.** `the-board.md` §4 was five lines of prose — no field, no
   gate, no checklist — against `objects`, which had a declared field, a hard gate and a lint.
   Authors build toward what is measured. Consequence: `the_allowance` has **zero** eat / cook /
   meal / breakfast / dinner / food / fridge / sleep canvases in a game whose anchor room is a
   kitchen, and declares `[player.trait_decay] hygiene = 10` with four ways to wash and **zero
   conditions anywhere reading hygiene**. Contrast `games/vesper` (v1): 11 things drop hygiene by
   30, one restores it, `hygiene >= 40` gates *"Take the car"* — filthy means she cannot leave.
4. **The walk-in — the field's largest bucket — is absent.** DoL's `Bath` is one activity with
   twelve outcome passages dispatched on (who is here x dice x your own stats), and the branches are
   cheap: `Bath Molestation` is **458 bytes with zero prose**, six config lines handing off to
   `<<actionsman>>`, the shared engine **1,742 other passages also call**. `Bath Robin Tease` is
   **473 bytes, three sentences**. Our engine already ships the mechanism and Vesper already uses it
   correctly (`Work the floor` @ renner_depot: 10% / 35% / 70% on Renner's corruption, into one
   2.3 KB target with three bands on the same trait). **Across all five v2 games: 10 substitution
   rules in 791 canvases**, and four mentions of the word in the whole doctrine, with no rules.
5. **Labels drifted, through a leaked exemption.** Field: **median 3 words, 10% at 6+**. Ours:
   `late_shifts` 3w/7% · `the_inheritance` 3w/10% · `vesper` 4w/17% · `last_call` 4w/15% ·
   `back_home` 4.5w/35% · `the_allowance` 5w/36% · `steam` 5w/47% · `forty_miles` 6w/50% ·
   `seventh_day` **6w/57%**. `the-voice.md` R1 already stated the correct rule; its **exemption**
   named three examples as exempt scene-choices, and all three exist in `back_home` as canvas names
   too — `5_scenes.toml:983` is a choice `text` (exempt, correct), `:1093` is a canvas `name` (a
   room-list button, never exempt). The exemption was written off the wrong specimen and the pattern
   was copied into `the_allowance` as the top-level button LO read.

### Why not simply revert to v1

`games/vesper` is v1's own output. It proves v1's **unit** is right — every room a verb (`Drill ·
Fix the emitter · Switch weapon · Wash up · Change`), zero browse screens in 186 canvases — and that
v1 could **prove nothing**: 12 of its 30 locations are thin or dead, six completely empty, and its
own `Wash up` and `Power down` are bare restores with no branch and no walk-in, which is the exact
*"dead-bath gap"* v1 names and forbids in `content-framework.md:113`. v1 is 10,095 lines of
unenforced library; v2 is 3,450 with a working scoreboard. **v2's machine, v1's unit, and the one
structural idea from the field neither had.**

### Step 0 — the blocking verification, run first

`setup.getCanvasById` (`v2.py:3177-3191`) builds its lookup **only** from
`help_data.locationCanvases`, populated only for canvases carrying `trigger.location`
(`v2.py:10986-11138`). v2's rungs are triggerless by design, so pointing a walk-in at one would
**silently never fire**. Built a throwaway `games/_probe_walkin` and ran it live under Playwright:

```
TEST 1 · substitution_only hides the target from the room list ....... PASS
TEST 2 · it fires as a substitution target ........................... PASS  -> Canvas_rung_shared_Node_base
TEST 3 · a hub choice reaches the same canvas ........................ PASS  -> Canvas_rung_shared_Node_base
JS errors ............................................................ none
```

**The shared payoff is viable**, and the required shape is `location` **+** `substitution_only =
true` on the target. Probe deleted after the run.

### What changed

- **`references/the-surfaces.md`** — rewritten. Deleted the object test as the placement rule,
  *"every choice hangs off a named object"*, R2b and its gate-22 block, and R3's
  derivation-from-objects. **New R2: a room's list is needs + work + people, and nothing else.**
  **New R3: the walk-in** — router (`trigger.substitutions`) / branch (one canvas,
  `substitution_only = true`, `[group]` bands on the axis the odds ride) / payoff (routes into the
  rung that already exists), with the Step 0 engine trap stated in the open, the join that produces
  the worklist, the per-room floor, and the thin-branch size with its measured comparison. Carries
  the corpus evidence and the corrected reading of the DoL bedroom. R1/R4/R5/R6 kept. The object
  test is retained but **scoped to hub choices only**. Sizing is now structural — *needs are a
  closed list, objects are an open one* — with both prior cap attempts and why each failed.
- **`references/the-meters.md`** — new section **M8–M10, the body's meters**. M8: a need declares
  what falls, where it fills, what it costs, and **what it shuts**. M9: a need that shuts nothing is
  a chore (gate 29). M10: `[player.trait_decay]` is the clock, and decay-vs-spent is a deliberate
  fork. Needs are per game, never a fixed list.
- **`references/the-voice.md`** — R1's exemption **rescoped to a choice's `text`, explicitly not a
  canvas `name`**, with the `back_home:983` / `:1093` pair printed as the leak. Three examples
  replaced with strings verified (grep, 0 hits) never to appear as a canvas name. Field figures and
  the full drift table added. Two lints registered.
- **`references/the-board.md`** — §1's location count now derives from *needs served + work done +
  people scheduled* rather than the rota alone, with vesper's 12-of-30 dead rooms as the warning.
  §4 is now `board.needs[]` as a real declaration.
- **`references/state.md`** — `board.needs[]` schema, `board.locations[].serves` replacing
  `objects`. The `objects` key stays readable in the five shipped ledgers and **nothing reads it**,
  the same treatment `dwelling` got in the map pass.
- **`references/engine.md`** — §22's cross-reference no longer cites R2b/gate 22.
- **`templates/board.toml`** — a `[[needs]]` block with the five fields and a worked-through
  comment; the location block asks `serves` and the walk-in question.
- **`templates/want.md`** — §5 gains *what does her body need here, and what stops when it goes
  unmet*.
- **`scripts/gates.py`** — **removed** gate 22, `_room_objects` and `lint_choice_anchoring`.
  **Added** gate 29 `a need shuts a door` and gate 30 `the walk-in floor`,
  plus lints `room-list labels` (noun-only share + length vs the field) and `the browse share`.
  Gate 20's help text no longer points at the deleted rule. The model record now carries `raw` so
  the checks can see `name`, `substitutions` and `substitution_only`.
- **`SKILL.md`** — scoreboard index updated; new operating rule: **ask what a tired author would
  build to satisfy a check, and make sure that is the thing you want** — a check manufactures
  whatever it can see.
- **`DOCTRINE_GAPS.md`** — study 5's object finding marked superseded at the head of the file, with
  the corrected reading; the gate-22 and anchoring-lint rows marked deleted. The sections stay as
  the record of what was believed and why.

### Verified

Both new gates were validated against all nine games **before** being written, and reproduce those
numbers exactly:

```
                    walk-in floor          needs
back_home           1/5   rooms covered    no board.needs[]
steam               0/6                    no board.needs[]
forty_miles         0/5                    no board.needs[]
seventh_day         0/12                   no board.needs[]
the_allowance       1/6                    no board.needs[]
```

The need-reader was checked directly against the merged TOML of four games: `hygiene` is read by a
condition in **vesper** and in **none** of the_allowance, back_home or seventh_day.

**Scores move, and the totals are not comparable across this pass** — gate 22 was a *passing* gate
on all five games, so removing it costs a pass while the two new gates add two possible fails:

```
                before        after
back_home       12/23         12/25
steam           15/25         15/27
forty_miles     23/27         22/28
seventh_day     25/27         24/28
the_allowance   26/27         25/28
```

**No game was touched.** LO's decision: doctrine only, `the_allowance` stays the specimen exactly as
`seventh_day` did.

### Open

- **Nothing here is proven by a built game.** The first game authored on these rules is the real
  test, and the honest expectation is that it finds holes — that is how this pass and the map pass
  both began.
- The audit of every *other* reference file carrying a worked example is still open; this pass
  closed the one in `the-surfaces.md` by deleting the reading, not the example.

---

## 2026-08-18 — the map: the borrowed example deleted, the shape made a choice

**Cause: `games/the_allowance`, which shipped at 26/26 gates with a world that is seven rooms of one
house plus a row of shops.** LO read the location list — nothing else — and said *"I think we have
done the same mistake we have done in back home."* He was right, and it is measurable: **of the five
v2 games, the only two whose map starts indoors are back_home and the_allowance.** The other three
root the world outdoors and read as places.

**And the cause was this skill.** Four of them, all verified:

1. **`the-map.md`'s only worked example WAS back_home's map.** `npc_ray`, `npc_marek`,
   `the_box_room` — that game's own character ids and its own room, checked against
   `games/back_home/toml_phases/7_final_game.toml`. back_home never declared a `board.map` at all,
   so the example was a reconstruction of *what it should have written*: two bugs patched out (no
   street, no beds), **skeleton kept**. A second copy sat in `state.md`. The Allowance's declared
   shape — *"one terraced dwelling over two floors + a parade of shops one bus stop away"* — is the
   template with the nouns swapped.
2. **The vocabulary presumed a house before any decision was made.** R1 asked whether a stranger
   could draw this *building*; the required field was `dwelling`. Already wrong for a truck stop and
   a bathhouse.
3. **The location-count rule is circular.** `the-board.md` §1: *"do not pick, derive it from where
   the cast goes."* Premise → cast → map; a family of five who live in one house returns a house
   every time. And `templates/want.md`, the first document written for any game, asked **nothing
   about the world at all**.
4. **The one rule that would have caught it is not a gate, and it signed itself off.** seventh_day:
   *"SIGNED OFF by LO in chat, board phase, 2026-08-16."* the_allowance: *"Signed off in the board
   phase."* No name, no date. The map signed off its own map.

**LO's decisions:** delete the example rather than replace it — one validated example recreates the
same failure with a nicer floor plan. Teach v1's naming contract **for new games, grandfathering the
five shipped ones**. Make the shape a **declared field with a gate behind it**, not more prose.

- **`references/the-map.md` — rewritten.**
  - The worked example is **gone**, replaced by a fields-only schema whose placeholders cannot be
    mistaken for a world, plus a note saying why there will not be another one.
  - **New R0 · Pick the SHAPE before you count anything** — five archetypes adapted from
    `author-game/references/location-design.md` §2, where they were measured against five named
    shipped games. Its headline, which v2 never carried: *"the genre floor is a multi-zone world,
    NOT a single building — do not default to a house."* Plus v1's two sizing axes (scale and
    aliveness, a budget fork not a quality dial). Carries its own n=1 warning: five is what was
    measured, not what exists; add a sixth **with evidence** rather than forcing a fit.
  - **R3 rewritten — the exterior is the GROUND, not a room off the kitchen.** With the ascii of
    both shapes and the measured failure. This is the rule the_allowance breaks.
  - **New R4 · names are navigation** — v1's contract (public = bare noun, private = possessive,
    hierarchy rides the page not the label), **explicitly grandfathering the five shipped games**,
    plus the readability test that actually failed: `The Parade` (unresolvable) and `The Box Room` —
    which is `the-voice.md` R1's *own worked example of a bad name*.
  - `dwelling` → `home_base`; *building* → *place*; `r1_signoff` must record **who** and **when**.
- **`references/state.md`** — same example removed, `archetype` / `home_base` / `r1_signoff`
  documented, `exterior` prose de-housed with the root requirement.
- **`templates/board.toml`** — the map block now asks the shape FIRST, and names the circularity it
  breaks. **`templates/want.md`** — new **§5 The world**, placed before the cast section because the
  cast is derived from the world and not the reverse.
- **`scripts/gates.py` — new gate 28, "the map is a place."** Two tests, because a declaration alone
  is satisfied by typing a word: (1) `board.map.archetype` is one of the five; (2) **the declared
  exterior is a root, not a leaf off an interior location** — mechanical, off `entry_from`, and
  unfalsifiable in the ledger. Also: the gate-12 help string still named the retired `dwelling` key.
- **`SKILL.md`** — gate 28 indexed, and the operating rule this whole pass is about:
  **an example outranks every rule beside it, so it goes in last — after it is validated, or not at
  all.** A rule is read; an example is copied. If one is ever promoted: **one per option or none.**

**Verified.** Gate 28 run on all five games. Its mechanical half, isolated:

```
back_home      FAIL — no board.map
the_allowance  FAIL — leaf off the_kitchen
steam          pass — exterior is the ground
forty_miles    pass — exterior is the ground
seventh_day    pass — exterior is the ground
```

It fails exactly the two games LO named by eye and passes the three that read as places, with no
invented threshold. The Allowance's failure text names both locations: *"the exterior 'the_parade'
HANGS OFF 'the_kitchen' (The Kitchen) — it is a leaf, not the ground."*

⚠️ **All five games now fail gate 28 on the declaration half**, because none of them has an
`archetype` field. Expected, same shape as the 2026-08-17 pass, and the denominators move: totals
are now out of 27. Nothing was patched — `the_allowance` ships house-shaped with a red gate, as
`seventh_day` shipped as the specimen for the last pass.

⚠️ **Open, and it is bigger than the map: every other reference file carrying a worked example has
the same exposure.** That audit is not in this pass.

## 2026-08-17 — the price of the climb, and four rules carried over from v1

**Cause: `games/seventh_day`, authored 2026-08-16 and reviewed the same day.** It scored
**22/24** with the best prose in the repo and a correctly-shaped explicit ladder — every
penetrative scene behind a gate, tier-0 content solo. Five things were wrong with it and **none
was the author disobeying this skill.** Each was a place the skill said nothing, or said
something that granted an exemption. LO's call: **fix the skill only.** `seventh_day` is
untouched and is now the regression specimen.

The measurement that started it, live in the built game under headless Chromium:

```
12 clicks of one choice — "Read the fourth rule again."
cover 4 → 16 · energy 100 → 100 · money 2 → 2 · Monday 05:57 → 08:33
```

`+1 cover · 10 min · no cost · no cap · no daily limit · repeatable forever.`

- **⚠️ THE SKILL HAD NO DOCUMENT ABOUT METERS AT ALL.** Eleven reference files, none about
  traits, pacing or throttles; the word `cap` appeared in zero of them. The incumbent
  `author-game` skill has solved this for years — `trait-design.md` "The throttle menu",
  `rts-design-philosophy.md` P8, `trait-catalog.md` §4–§5 — and v2, built self-contained,
  never carried any of it over.

  **New `references/the-meters.md`**, adapted into v2's vocabulary rather than copied: M1 a
  meter that gates content must cost something to raise · M2 progress accrues over in-game
  **days** · M3 the four-lever throttle menu and why none works alone · M4 the recipe (spacing
  + at least one hard throttle + the rung pays visibly) · M5 **how to throttle a TRIGGERLESS
  rung**, which is what nearly every v2 rung is · M6 `cap` is a value ceiling, not a rate limit
  · M7 the sidebar doubling trap. Carries the measured field table for all five games.

- **⚠️ `the-economy.md` R5 CARRIED AN EXEMPTION THAT SWALLOWED THE ARCHITECTURE.** It read: *"a
  triggerless rung reached through a gated hub choice is held to a weaker standard — it is not
  free, only farmable."* **Every rung in a v2 game is a triggerless rung behind a hub choice.**
  Struck. Measured instance: a rung paying £2 per 25 min, uncapped, behind `standing >= 35`,
  against a £20 weekly obligation — gate 18 printed `4 gated rungs are uncapped too` and passed,
  exactly as instructed. R5 rewritten with the tools that actually work on a triggerless rung
  (`costs`, or a `_today` flag cleared in `[engine.daily_tick]`); **new R6** states that the same
  test applies to any trait a condition reads, not only to currency.

- **⚠️ `the-surfaces.md` R6's LINT COUNTED THE PRACTICE R6 REJECTS.** It reported *"N/N standing
  menus never change their prose"* — a conditional-**opener** count — while R6's own text says
  the reference game's identity sentence is byte-identical on all six visits, and
  `author-game/lanes.md:167` calls tiering an opener *"a known failure."* Its worst-ever score,
  `24/24 frozen`, was reported against openers that were **correct**. R6 now names its four
  mechanisms as a per-location checklist, records the field figures for mechanism 4
  (vesper 14 random events, forty_miles 8, the other three **0**), sets the floor *every location
  carries at least one*, and folds in v1's permitted exception — banding a base node on a
  **recoverable** state is a read-out, not a tier.

- **`scripts/gates.py` — two new gates, two rewrites, one blind spot closed.** New shared
  helpers `_routes` / `_is_free` / `_free_climb` resolve brakes **per route into a canvas**,
  which is where the brake actually lives in this architecture.
  - **New gate 26 · "the climb is paid for."** Walks every trait any condition reads — player
    traits *and* per-NPC relation, so it cannot be narrowed by declaring less — and simulates the
    cheapest **free** climb to the highest gate, from the declared starting value, one click at a
    time. Reports clicks and in-game minutes whether it passes or fails, because a `costs` of 1
    energy on a 10-minute rung satisfies any boolean version of this check and changes nothing.
    On `seventh_day`: `cover 0 → gate at 55, entirely for FREE — 45 clicks, 9h10m`.
  - **New gate 27 · "a banded meter is not also a number."** Deterministic, no invented
    threshold. Fails **4/4** on `seventh_day` *and* **4/4** on `forty_miles`, which had shipped
    the same defect through a full review nobody caught.
  - **Gate 18 rewritten.** It read `trigger.costs`, which is always empty for a triggerless rung,
    so every priced rung in every game read as unpriced — then it excused those rungs on the
    struck footnote. Two bugs pointing the same way. Now fails any uncapped income rung, gated or
    not: forty_miles 8, steam 20, back_home 10, seventh_day 2.
  - **Gate 9 given a denominator.** `locked > 0` stays the verdict — inventing a ratio ceiling is
    what demoted the-surfaces R5 — but the headline now prints gated-vs-total, which is how a game
    running 78% open on turn one used to pass this silently.
  - **Gate 10's hidden-trait blind spot closed**, as `games/seventh_day/ENGINE_NOTES.md` §3
    diagnosed correctly. Traits marked `hidden = true` are excluded from the descent test: hiding
    a trait also removes it from the sidebar, so it is not a meter the player can be lied to by.
    This keeps the anti-narrowing property — the exclusion is a declaration about *rendering*,
    not about which traits get judged.

- **`engine.md` — four new sections and ten corrected citations.** §27 `costs` on a choice
  (engine-enforced affordability, and the 0–100 hard clamp on the deduction the author cannot
  turn off) · §28 `[engine.daily_tick]` and why it is the only clean day-cap for a triggerless
  rung · §29 `cap` as a value ceiling, read out of `v2.py:5763-5769` — `Math.max(current, capNum)`
  means it never pulls a value down · §30 the banded-item / auto-dump collision and the vanishing
  card. **And fourteen `v2.py:NNNN` citations were drifted and are now fixed** (§7, §21, §21b ×4, §22, §23 ×2, §26 ×2)
  — the failure `ENGINE_NOTES.md` §4 measured at two of two; it was worse than that.

- **`SKILL.md`** — `the-meters.md` registered in the dispatch table and the world-files list;
  gates 26 and 27 added to the scoreboard index; new operating rule: **a check that measures
  EXISTENCE has not measured anything.**

**Verified:** `gates.py` run on all four v2 games. Every new failure was traced back to the TOML
by hand before being accepted — `forty_miles`' four unhidden banded meters and eight free income
rungs were confirmed in its source, not inferred. Route classification asserted against all 17
correctly-braked rungs across two games: **zero misclassified as free.** Gate 26's arithmetic
hand-checked against the live probe (cover +1/click, `relation` 20 in 5 clicks of `rung_job_know`).
Every `v2.py` line cited in this pass was opened and read.

**Scores after:** seventh_day 22/26 · forty_miles 23/26 · steam 15/24 · back_home 12/22.

⚠️ **Left open, deliberately:** the media gates still report 100% coverage for a game with 42
declared pools and **zero files on disk**. Same denominator disease, last open R7 item from
study 6, and a separate pass with filesystem work in it. Not fixed here; noted so it is not
mistaken for fixed.

⚠️ **A number LO reads changed meaning.** `lint · screen shape` no longer prints
*"N/N standing menus never change their prose."* It prints *"N/M locations render identically on
every visit"* and *"N/M carry a random event"* instead. Different population, different question.

---

## 2026-08-16 (later still — the fix that measured itself wrong)

- **⚠️ THE MENU FIX IN THE PASS BELOW DID NOT WORK, AND THE LEDGER SAID IT DID.** It gated 57
  room choices, moved *"choices open on turn one"* from 126/166 to 70/166, reported that as the
  fix, and left `show_when_locked = true` on every one of them. A locked choice with that flag
  **still renders** — greyed, but a line on the list. Counted afterwards, on the built game:
  **164 of 166 room rows still appeared on night one.** The player met the same wall with half
  of it grey, which is worse than leaving it alone. Found by LO playing the shipped build.

  This is the **denominator trap from study 6, committed by the author of study 6**, one day
  later. The number that was easy to move got moved; the number the player sees was never
  computed by anything in the file.

  - **`lint_screen_shape` now LEADS with `median N ROWS render on a screen at turn one (max M)`**
    and flags any screen rendering 8+. Rows = unlocked + `show_when_locked`. Every other figure
    in that lint counts something the player cannot see; this one is the wall.
  - Measured across the three games the moment it existed: forty_miles **median 8 → 4** after
    the repair, steam median 3 (max 17), back_home median 2.
  - **Doctrine, now explicit:** one visible locked door per screen, not five. Keep the
    lowest-threshold gate visible — that is the next thing the player earns, and it is what
    gate 9 counts — and hide the rest. Flag-gated choices stay hidden regardless: a discovery
    must not advertise itself.

---

## 2026-08-16 (later — the Forty Miles repair pass)

- **⚠️ `engine.md` §21 was teaching an op the engine does not run, and two games wrote 105 of
  them.** `references/engine.md:497` discussed `op = "subtract"` as authored behaviour. It is not
  one: `applyTraitEffect` runs `add` and `set` and falls through to *"Unknown op; do nothing"* +
  `return` on anything else (`v2.py:5742-5751`), and the string `subtract` appears nowhere in the
  generator or the importer. Proven live on a shipped build — `count` 100 stayed 100 through a
  `subtract 4`; `add -5` moved stress 20 → 15.
  - **Measured cost.** 35 dead effects in `forty_miles`, **70 in `steam`**. In the first, the
    counterweight its own spec called *"only ever falls"* never moved for the entire game (12 dead
    decrements), 20 activities never charged the energy they said they cost, and the only NPC
    penalty in the game never applied. Valid TOML, green build, all gates green, and an 11/11
    play-test — because a number that never changes looks exactly like a number nobody has moved.
  - **New §21b** in `engine.md` with the full op table per effect family (trait `add|set`, flag
    `set|unset|toggle`, quest `start|update|complete|cancel`), each cited.
  - **New gate 25 · effects use a live op** in `gates.py`. Fails `steam` at 70, passes `forty_miles`
    (repaired) and `back_home` (never had any) — it discriminates rather than just firing.
  - **`template_import.py` now hard-fails** on a dead op (same shape as the cheat-page grant check at
    `:3755`), so no future build can emit one. Verified: `games/steam` now exits 1 and produces
    nothing until its 70 are rewritten. Deliberate and recorded — a frozen record that is not
    rebuilt, and the failure is the point.
  - **⚠️ Two gates were reading direction from the op NAME.** `_currency_ops` appended the op string,
    so a deduction written the only way that works (`op = "add"`, negative value) counted as INCOME:
    `forty_miles` flipped from 11:11 to 10:12 the moment its dead effects were repaired correctly.
    Now classified by SIGN, with a `_effect_value_sign` helper that also handles the
    `{type = "random", min, max}` value form. Gate 24's `_outflows` had the same bug.

- **Gate 24 now reads `[settings.rent]`, and `engine.md` §26 documents that system for the first
  time.** The gate walked canvases only, so it **failed a game whose obligation was charged** —
  `[settings.rent]` was enabled at `amount = 245` and works end to end (verified live: 300 → 55 on
  the Friday rollover; `v2.py:5453-5464` arms it, `:15247-15259` intercepts, `:15925` charges).
  A check that fails a game for obeying the doctrine is a bug in the check.
  - §26 carries the whole mechanism, the `start_after_flag` rule, and the new doctrine line:
    **if the engine takes the money, do not also author a canvas that narrates the payment.** The
    measured failure is a game with two settle-ups where the free one had all the writing in it.
    `the-economy.md` R3 gains the same rule.
  - **`currency_symbol` added to `[settings.rent]`** (importer + generator), default `"$"` so no
    existing build moves. The three RentDay passages hardcoded `$` — one screen quoting dollars in a
    game whose every other price is written in pounds.

- **Gate 22's third check was reporting verbs as room objects.** *"choices hang off `sleep`"* (from
  the choice `"Sleep."`) and *"`start`"* (from *"the start of it"*) are not things a board can
  declare, and a check that demands nonsense in the ledger gets ignored. It now requires the hook to
  be a **noun phrase on both sides** — a determiner in front of it in the choice text AND in the
  screen's prose — plus a third `_OBJ_STOP` block for time spans and abstractions. Measured on
  `forty_miles`: 16 findings of which 6 were junk → 7, every one a real thing in the room that the
  board had genuinely left out.

- **New sidebar item `type = "quest_next"`** (generator + importer + CSS). A quest card has no
  `title` field, and there was no sidebar type for guidance at all — so a game could ship an
  excellent Quests page and nothing in the persistent rail but `trait_status_text` bands, which name
  a **state**, not a step. It renders `renderQuestsGoalBlock`, the same block as the page and as
  `npc_panel`'s `next` row, so the three surfaces cannot drift. Documented in `engine.md` §23, along
  with a **circular-label** warning: measured on a shipped game, all three cards of one ascent tier
  named a choice gated at the exact value the card was trying to reach.

- **`SKILL.md`** — gate 25 added to the scoreboard index; a new operating rule on silent-vocabulary
  failure, and the "check the skill before blaming the game" rule gains its second measured instance.

- **How verified.** `gates.py` on all three v2 games before and after; `package_from_toml` on
  `forty_miles` (builds) and `steam` (now correctly refuses); and a live pass in
  `twine-game-explorer` over the rebuilt game — the funnel end to end, `💭 You are thinking:`
  rendering in second person, `count` falling for the first time, RentDay charging £245 and printing
  £, a room hub at 4/8 open on night one and 8/8 at tier 55, three objectives in the sidebar, and
  all eight new random encounters firing on location entry at 13–24% with the three tier-gated ones
  correctly silent at zero.

---

## 2026-08-16

- **Whole-skill audit — the declaration hole was a CLASS, and both of the review's blockers are now
  gated.** Read-only pass over all 23 gates, 11 reference files and 1,618 lines of `gates.py`.

  - **⚠️ R6 · "declare less to owe less" was one rule broken in three places, not one bug.** The
    third audit fixed `objects` without noticing the shape generalised. Measured across every gate,
    it partitions them exactly: **a gate that walks the GAME and looks the declaration up cannot be
    weakened** (`residents have homes` — declare no homes, fail 0/6); **a gate that walks the
    DECLARATION can** (`guidance exists` — truncate `board.characters` to one and it reported *"24
    quest cards for 3 ascent tiers and 1 characters"*, and passed). `ascent tiers expand the world`
    was worse than gameable, it was **narrowed by declaring**: with nothing declared it guesses the
    top-gated traits, so naming only the healthy tiers hid a descent-shaped meter from the gate whose
    entire job is to catch one. Both fixed — guidance now owes a card for every `[[npcs]]` entry the
    game has, and the direction test now runs over **every player-subject trait in the game**,
    declared or not (NPC-subject traits excluded, since a per-character relation legitimately gates
    one way). Verified with a synthetic descent meter: `shame (0+/1-)` is now caught while undeclared.
  - **⚠️ R7 · Both blockers the review found had hidden in the PRESENCE class.** Four gates ask *does
    at least one exist*, and that question cannot see that the important one is missing.
    `money gates something` passed on nine *other* canvases while the declared £245 obligation charged
    nothing; the media gates report 100% on 68 declared pools with zero files (no gate in the file
    touches the filesystem at all — still true, still open).
  - **New gate 23 · speakers are named.** Every `dialog`/`thought_bubble` must carry `props.speaker`.
    Consistency, no threshold, always reachable, and there is no case where omitting it is correct.
    Measured across all three v2 games: **147, 145 and 79** blocks missing it — three for three,
    because the skill mentioned `thought_bubble` once and never showed its shape.
  - **New gate 24 · the obligation is charged.** `board.economy.obligation` must carry an
    `obligation_amount`, and some choice must charge at least that much. Declaring an obligation with
    no price now fails — *a price nobody can check is how a game shipped with its central mechanic
    missing.* Verified both ways: fails as shipped, passes once the settle-up takes £245.
  - **`engine.md` §25 written, and `speaker = "unknown"` promoted out of "Unverified — do not cite".**
    It had been read during the review (`v2.py:14640-14647`, renders *"Someone is thinking:"*) and
    left on the list — sitting directly beside the largest defect the review found. §25 now carries
    the default's `file:line` chain, all five authoring forms, the `dialog` vs `dialogue` trap, and
    the requirement that a player thought match the game's `narration_person` (62 of the 147 broken
    bubbles called the protagonist "she" in a second-person game, so re-attribution alone would have
    produced *"You are thinking: She has measured it now…"*).
  - **⚠️ The stale `fill` instruction had a SECOND home.** `state.md`'s Field-rules section still read
    *"words currently placed there — recompute from `scripts/gates.py`"*. Fixing `templates/board.toml`
    yesterday only got one of the two places telling authors the budget is computed.
  - **Nine of twenty-one gates were documented in zero reference files** — their evidence lived only
    in `gates.py` comments, so an author hitting a FAIL on "traversal heat" had nothing to read.
    `SKILL.md` gains a scoreboard index mapping every gate to the file that argues it; **23/23 gate
    names now appear in the docs**. Also fixed a naming mismatch: `the-surfaces.md` called it
    *"Gate 20 · menu size"* while the board prints *"a place is not a catalogue"*.
  - **`DOCTRINE_GAPS.md` study 6 gains R6 and R7**, since both are rules rather than one-offs.

  **Scores:** forty_miles **19/23**, steam **15/21**, back_home **11/19**. Every new failure is a real
  defect the games shipped with, and the two new gates fail all three games on the speaker field.

- **Third audit — the gate could be passed by declaring LESS, and three denominators were on one
  scoreboard.** Read-only pass, then applied.

  - **⚠️ Gate 22 was gameable, and the inversion is worth recording.** Measured: keep one safe object
    per room, change nothing in the game — **20/21, gate green.** The declaration checks verify the
    board is honest about what it declares and could not see that it declared almost nothing. Worse,
    the *lint* I had demoted for being unreachable is the half that **cannot** be gamed, because it
    never consults the declaration. So the cheatable half was the gate and the honest half was the
    lint — the opposite of how I had described the split. Fixed with **check 3: every thing the
    choices actually act on must be declared**, computed from the game rather than the board (an
    anchored choice hooks onto a word its screen wrote; if no declared object covers that word, the
    board left an affordance out). The same shrink now scores **59 undeclared affordances against 16**
    for the honest declaration, so under-declaring is strictly worse. Reachable, because it only asks
    the board to list what the game already acts on.
  - **Check 3's first cut was 50% noise, and fixing it exposed a real bug in `_content_words`.**
    It reported choices hanging off objects called *there*, *before*, *get* and *forty*. Two causes:
    stopwords were filtered on the RAW word and only then stemmed, so every inflection walked
    through (`gets` survived while `get` was stopped); and the list had no adverbs, ordinals,
    weekday names or bare numbers. Both fixed — 30 findings became **16**, and they are now nouns a
    reader would recognise (*the block*, *the window*, *the van*, *the road*). Also switched the
    comparison to `_names_any`, which had been reporting `padlock` as undeclared against a declared
    *"the padlocked door"*.
  - **Three denominators were printed on one board** — the trap this project has now hit six times.
    Gate 20 and the screen-shape lint counted 213 choices across rooms **and** character hubs; the
    anchoring lint counted 166, rooms only. Gate 20 now reports them separately, and the split
    matters: **rooms are 18 of 22 at the cap (82%)**, where the blended figure read 19 of 29 (66%) —
    the well-shaped character hubs were diluting the number meant to expose the badly-shaped rooms.
    The screen-shape lint now names its population inline.
  - **A location declaring objects but owning no repeatable screen** reported seven misleading
    "affords no choice" lines for one fact; it now reports that fact once, in the board's own terms.
  - **`_room_objects` memoised** — the gate and the lint each triggered a full walk, which is not
    just wasted work but two call sites that could drift.
  - **Figures moved by the stopword fix and corrected everywhere:** anchoring is **55%** over room
    screens (was reported 65%), and **51%** over the 213-choice population, which is the honest
    like-for-like against the by-hand 41% in `games/forty_miles/REVIEW.md`. The review now states
    both populations rather than reading as a before-and-after.

  **Verified:** cheat re-tested (fails, 59 undeclared) · matcher unit tests re-run after the
  stopword change (9/9 stem pairs, 6/6 match cases, and the doctrine's worked example still scores
  3/4 with "Mirror" failing by design) · all three games and the no-ledger path re-run. Scores
  unchanged: forty_miles 19/21, steam 16/19, back_home 12/18.

- **Second audit — gate 22 was unreachable, and the root cause of the fake budgets was in our own
  template.** Read-only pass at LO's request, after the first audit had already found six defects.

  - **⚠️ Gate 22's anchoring check could never be passed, so it is now a LINT.** Run against the
    worked example in `the-surfaces.md` — printed there, measured from a shipped game, to show what
    *correct* looks like — a word-match fails **"Mirror"** under *"Your clothes are kept in the
    creaky wardrobe."* One in four of that example's real decisions fails. On `forty_miles` the
    ceiling is **74%** even matching against the whole room's prose, against the 55% the strict rule
    scores. **A gate demanding zero failures fails correct work, which is exactly why R5 and R6 were
    demoted** — I had reproduced the documented mistake with a zero instead of an invented number,
    which is worse because it looks rigorous. Split: **gate 22 "declared objects are real"** keeps
    the two halves a parser can actually judge (every declared object is written; every declared
    object affords a choice), and **`lint_choice_anchoring`** reports the share as a percentage with
    the worst screens ranked.
  - **The gate's denominator was under the author's control.** A location declaring no `objects` was
    silently skipped, so declaring one easy room shrank what was checked from 166 choices to 84.
    Now a room that has screens and declares nothing is itself a failure.
  - **`_room_objects` extracted** as the shared analysis behind the gate and the lint, fixing three
    more latent bugs on the way: the location description is now read *outside* the canvas loop (a
    room whose only canvases bind an NPC previously had every object reported "never written");
    NPC hubs are excluded on `npc` **or** `requires_npc`, not `npc` alone (they are separate fields
    and a hub may set only one); and a board declaring a location id the game does not have is now
    reported instead of silently counted as unwritten.
  - **The post-hoc budget detector false-positived a real plan.** At `% 100`, a legitimate
    250-granularity plan (9,750 · 5,250 · 4,250 …) was flagged as back-filled — a false positive on
    exactly the careful author it is meant to reward. Now `% 50`, which accepts every plausible plan
    granularity and still scores the measured real case 0 of 8.
  - **⚠️ ROOT CAUSE of the fake budgets found, and it was ours.** `templates/board.toml` said
    `fill = 0  # recomputed by gates.py — do not hand-maintain`, and `state.md` opened with
    *"anything that can be recomputed from the TOML does not belong here"*. **The skill told three
    authors the field was computed, so all three filled it in afterwards.** Both corrected, with the
    distinction stated: *recomputed* means derived, not measured after the fact, and a declaration
    only works if it can be wrong.
  - **`DECLARED_FILL_TOLERANCE` labelled as the one invented number in the file**, with why an
    invented value is defensible here (it compares a game against itself, so it only has to be loose
    enough not to police variance) and unacceptable in R5/R6 (which had to discriminate between
    games). Any value in 0.2–0.4 behaves identically — the signature of a number not carrying the
    decision.
  - **`DOCTRINE_GAPS.md` overstatement corrected** — "every floor is cleared with room" was wrong;
    `sinks : sources` sits exactly on its floor. Six of seven.
  - Doctrine updated for the split: `SKILL.md`, `the-surfaces.md` (R2b, the checked table, the
    not-gated note), `the-board.md`, `state.md`, `templates/board.toml`, `games/forty_miles/REVIEW.md`.

  **Verified by construction, not inspection.** Each fix was exercised against a synthetic case:
  a phantom location id is reported; declaring one room only now fails with the other seven named;
  a 250-granularity plan passes; a `requires_npc`-only hub contributes 0 floats (correctly excluded);
  and a location whose every canvas binds an NPC still resolves 5 of 6 objects from its description
  alone. Scores unchanged — forty_miles 19/21, steam 16/19, back_home 12/18, no-ledger 18/18.

- **Audit of yesterday's study-6 work — four defects in it, all fixed.** Found by unit-testing the
  new helpers and re-reading the doctrine against itself, not by re-reading the diff.

  - **`scripts/gates.py` `_stem` was wrong for consonant+"es".** It stripped "es" from any word
    ending in it, so `cages`→`cag` while `cage`→`cage`. **5 of 16 common singular/plural pairs failed
    to meet**, including cubicle/cubicles and table/tables, both of which occur in a real board
    declaration. Now strips "es" only after a sibilant (`ses/xes/zes/ches/shes`) and "s" otherwise:
    13/14 pairs meet. The `shelf`/`shelves` irregular still misses and is documented rather than
    fixed — handling f→ves would make `curves`→`curf`, a new wrong answer.
  - **`_names_any`'s prefix fallback produced FALSE PASSES.** At a 5-character prefix, `count`
    matched `counter` — so *"Count Bev's float"* was credited to the shop counter, a different
    object. Raised to six. A gate that silently forgives an unanchored choice is worse than no gate,
    so the wrong-fail direction is the one to prefer here.
  - **Gate 22 double-reported one defect as two.** `afforded` was only recorded for choices that had
    already matched their screen's prose, so a choice naming an object the screen forgot to write was
    flagged as floating *and* its object flagged as unusable. Now recorded independently: unusable
    objects drop 11 → 8, and the 8 are real.
  - **`SKILL.md:57` still taught the cap as the rule** — *"a repeatable location screen caps at 8
    choices"* — in the file an author reads first, which would have undone the whole change. Rewritten
    to lead with the derivation and name 8 as a backstop, citing both games as evidence. Same fix
    applied to `engine.md:444`.
  - **The many-to-one relation was written as one-to-one** in `the-surfaces.md` R3, `the-board.md`,
    `state.md`, `templates/board.toml` and study 6's own R2 — *"one choice per thing that affords
    one"*. That is a quota wearing a derivation's clothes, and it contradicted the worked example
    three lines above it, where a bed affords two choices. All five corrected; study 6 R2 carries the
    correction visibly.

  **Also verified:** gate 1's round-number branch, which had never executed on any real game, was
  exercised against a synthetic honest plan — it PASSes a roughly-right plan, FAILs named locations
  that drift (`the_showers: declared 9,000, delivered 4,191 (-53%)`), and FAILs a flat plan with
  *"the PLAN has no centre"*. `_median` returns an int on both odd and even inputs, so gate 19's
  `:+d` margin format cannot crash. Stale figures from yesterday (64% → 65%, 11 → 8 unusable,
  106/166 → 108/166) corrected in `CHANGELOG.md`, `DOCTRINE_GAPS.md` ×2, `the-surfaces.md` and
  `games/forty_miles/REVIEW.md` ×3. Scores unchanged: forty_miles 19/21, steam 16/19,
  back_home 12/18.

## 2026-08-15

- **`DOCTRINE_GAPS.md` — Study 6 added: "The number becomes the spec."** Written after a full review
  of `games/forty_miles`, and prompted by LO's question on reading it: whether the skill states
  *reasoning* for its specs or only *numbers*. Measured across all three v2 games. Three of three
  ship exactly 8 locations and 3 ascent tiers; two land within four words of the 4,500 mean-location
  floor; total prose came in at 36,035 / 36,019 / 37,450 against a 36,000 figure that is not a spec
  anywhere — it is illustrative arithmetic at `the-board.md:79`. The mechanism is a floor/ceiling
  asymmetry: `forty_miles` clears every floor by 12-97% and sits on both ceilings at exactly 0%
  margin, with 19 of its 30 hub screens at the gate-20 cap. Verified by parsing each
  `7_final_game.toml` and by re-running `gates.py` on all three games; the menu comparison
  (steam 214 choices over 22 screens vs forty_miles 213 over 29) is the measured consequence.
  Five rules proposed, **no new gates** — the fix is reporting `median · count-at-cap` on ceiling
  gates, since "0 over 8" and "19 at exactly 8" currently print the same PASS. Nothing applied to
  `gates.py` or the reference files; surfaced for LO's call.

- **Study 6 applied — the numbers stop being the spec.** LO's call: hard gates immediately, and
  backfill `forty_miles`' board declaration only (no game content touched anywhere).

  - **`scripts/gates.py` — new gate 22, "choices hang off the room".** Declare-then-check per
    `SKILL.md:107` against a new `board.locations[].objects`. Three consistency tests, no threshold
    of its own: every declared object is written into some screen's prose, every declared object
    affords a choice, and no choice names something its own screen's prose has not put in the room.
    Scoped to **location-only** hubs — on an NPC hub the anchor is the person (R1/R2's object test),
    and the handover hub measures 0% on object-matching while being correct. Matching is a stemmed
    content-word overlap with a 5-char prefix fallback; `_stem`/`_content_words`/`_names_any` are
    new module-level helpers. **This is what makes `the-surfaces.md` R2b checkable** — the rule the
    file itself called "the highest-value ungated rule", which had drifted to 55% in a 20/20 game.
  - **`scripts/gates.py` — gate 1 now checks the author's own budget.** Reads
    `board.locations[].fill` (accepting `budget`, an observed key drift in `steam`) and judges each
    location against its own declared figure at `DECLARED_FILL_TOLERANCE = 0.25`; the three global
    constants are demoted to a backstop used only when no ledger exists, and the headline says which
    ran. ⚠️ **Found while building it:** all three v2 games declared *exact post-hoc word counts*
    (9,607 / 4,936 / 10,295 — 0 of 24 round to 100), so delivered-vs-declared matched 8/8 in all
    three and proved nothing. A budget that cannot be wrong is not a budget, so the gate detects a
    mostly-non-round declaration, refuses to credit it, and falls back to the backstop. All three
    games now FAIL gate 1 for this, correctly.
  - **`scripts/gates.py` — ceiling gates report the distribution, not the verdict.** Gate 20 prints
    `median · N of M screens at the cap` and warns when the majority sit on it; gate 19 prints its
    margin and the field median. Floor gates keep printing a verdict — the asymmetry is the finding.
    Same discipline as G2's existing marginal-pass headline.
  - **`references/the-surfaces.md`** — R3 rewritten so the derivation leads (the count falls out of
    R2b; 8 is named as a backstop, not a size). R2b gains the `objects` declaration, the three
    checks, and why check 3 is per-screen. R2b moved out of the not-gated list, with the reason it
    was there kept visible. Gate 22 added to the checked table.
  - **`references/the-board.md`** — §1 leads with deriving the location count from the cast's rotas
    and the daily loop; the "6–8" removed. `objects` and round-number `fill` added to the per-location
    record. The 36,000-word example deleted, with a note that three games shipped to it.
  - **`references/the-release.md`** — §"The first release": "6–8 locations" and "30-45k words"
    replaced by the derivation plus the shape.
  - **`references/state.md`**, **`templates/board.toml`** — `objects` documented; `fill` recorded as
    canonical and round-numbers-before-prose; `budget` noted as drift.
  - **`games/forty_miles/v2_state.json`** — `board.locations[].objects` backfilled for all eight
    locations, derived by reading what each room's prose actually names (not reverse-engineered from
    the choice lists, which would make the gate vacuous). Plus an `objects_note`. **No game content
    changed** — `toml_phases/`, `output/` and `releases/v0.1.html` untouched.

  **Verified by running, not asserted.** `forty_miles` **20/20 → 19/21** (fails fill and gate 22);
  `steam` 17/19 → 16/19; `back_home` 13/18 → 12/18 — every new failure is the post-hoc budget, which
  is true of all three. Gate 22 **discriminates rather than just firing**: `hub_stock_room` flags 2
  floating choices and `hub_stock_room_dawn` flags 5, matching the by-hand review measurement, and
  every flagged line is a real unanchored noun (*the hasp, the wastage sheet, the first Tuesday*).
  The no-ledger path was tested on a copy with no `v2_state.json`: gate 1 falls back and says so,
  gate 22 reports n/a, nothing crashes.

## 2026-08-14 — **The overnight-schedule rule was true only for the example it was written from**

`references/the-board.md` §2 rewrites the overnight-window paragraph to name the weekday caveat, with
the two source lines and the two-row fix.

**What was wrong.** The section said *"`22:00`–`04:00` is one row, not two"* with no qualifier. That
holds only when `weekdays` covers all seven days — which is exactly what the code sample directly
above it does, so the exception was invisible to anyone reading the rule off the page. The engine
checks the weekday and the time wrap **separately**, weekday first, against *today*:

```
v2.py:3446   if (!setup._weekdayMatches(ds.weekdays, todayIndex)) continue;
v2.py:3448   if (!setup.isCurrentTimeSlot(ds.start_time, ds.end_time)) continue;
```

So `weekdays = [1], 23:00–06:00` places the character on Tuesday night and **deletes them at
midnight**. A game with a Tuesday-night regular, a Thursday/Sunday regular and weekend-night rows —
i.e. any game whose cast is not on site every single night — silently loses most of its night
presence, with no build error and every gate green.

**Why it matters beyond one game.** Presence failures are invisible to `gates.py`: gate 6 checks that
a character *has* a schedule row, never that the row resolves at the hours the fiction claims. This
was a rule that could not be caught downstream.

**A note on the prior claim this paragraph rebutted.** An older project-memory note said overnight
windows always need two rows, "because a single window can't wrap". That stated *reason* is
contradicted by source — the `endTotal < startTotal` branch is present in **both** `v1.py:3145` and
`v2.py:3784`, so the wrap itself works in either generator. Its *recipe* is nonetheless right
whenever the row is day-specific, for the weekday reason above. The skill then over-corrected from
"the recipe is unnecessary" to "one row, always", and neither account had separated the two cases.
Net: **the wrap is not the variable; the weekday list is.**

**How verified.** Read at source, then proved in a built game rather than on paper: nine presence
probes driven through the engine's own `setup.getNpcLocation()` across the midnight and week
boundaries (Tue 23:00 → Wed 01:00 → Wed 04:00; Thu 22:00 → Fri 00:00; Sun → Mon; plus an
all-seven-days row left as one). All nine correct only after the day-specific rows were split;
the all-seven-days row stays a single row and still resolves.

---

## 2026-08-14 — **The field's most consistent shape was in a study file the authoring path never reads**

`references/the-surfaces.md` gains **R2b · every choice hangs off a named object in the prose**, with
a worked comparison at the top of the file, and `SKILL.md`'s surfaces callout now names it inline.

**Why this was urgent.** Study 5 found this in three of five played games independently, and called
it *"the single most consistent shape in the corpus"* — but it lived only in `DOCTRINE_GAPS.md`,
which this skill's own inventory calls **"the trail, not the doctrine."** Nothing on the authoring
path pointed at it. An author following the dispatch table would have produced correct *counts* with
no anchoring: eight choices in a flat list rather than eight choices under four sentences. That is
precisely the difference between the failure case's front desk and the reference game's bedroom, so
the rule that best predicts whether a location reads as a room was unreachable from the phase that
builds locations.

Found while sanity-checking whether a **bare** prompt — `/author-game-v2 new game, female
protagonist, give me a few ideas` — would be a fair test of the skill. It would not have been: the
skill could not have taught the rule, and a loaded prompt would have tested the operator instead.

**Also moved:** study 5's play-measured figure for how much a location offers — **median 3 things to
do, max 6**, counting only decisions and excluding onward travel and standing affordances. It now
sits beside the existing 18-sandbox parse figures with a note reconciling them, since the two count
different things and disagree by a factor of three otherwise.

R2b is **not gated and says so**, with the reason: a parser can see that a choice exists and that a
paragraph exists, but not whether the paragraph names the thing the choice acts on. It is flagged in
the file's checked-table as the highest-value ungated rule there.

**No gate, no threshold, no code changed. Scores untouched:** steam 17/19, back_home 13/18.

---

## 2026-08-14 — **Gate 21 graduates study 5's one gateable rule — and finds two economy gates reading the wrong channel**

Study 5 named exactly one output as gateable: *a choice with a declared cost whose label omits it is
checkable against the TOML.* Graduating it turned up two pre-existing defects in the economy gates
that had nothing to do with study 5, and both were silently wrong on a shipped game.

**`scripts/gates.py` — gate 21, `a price is on its label`.** Every choice that spends the currency
must name the amount in its text. Measured by playing: every corpus game that charges money puts the
price on the button, and the player is budgeting against a stated deadline. **Money only** —
stamina-type costs are counted in the headline and never judged, because two corpus games label them
and the reference game does not, and a rule there would be an invented threshold, which is the
failure that demoted R5/R6. Fires on vesper: **3 of 7 coin choices hide their price**, all three
purchases (`Pay the toll.` at 5, `Buy a weapon` at 40, `Buy infiltration gear` at 30) while four
others name it — the same game contradicting itself is the tell.

**Bug 1 — a `costs` block is a gate, and gate 16 could not see it.** The engine refuses a choice the
player cannot afford (`v2.py:12556`), but `reads` is built from *conditions* only (`gates.py:349`).
A game that prices its choices rather than condition-gating them read as *"nothing in the game reads
the currency"*. Vesper spends coin on seven choices and scored **zero**. Gate 16 now counts either
channel and says which.

**Bug 2 — the currency inference took the first name match, and vesper has two real currencies.**
`money` is Credits, company-visible; `coin` is hers and hidden, *"the company can't see"*. `money`
is used once, `coin` eighteen times — and the gates were judging `money`. Worse, `CURRENCY_HINT` had
no entry for `coin` at all, so a currency by that name was invisible outright. **This is the same bug
class already fixed once in the corpus extractor**, where a decoy `randomMoney` beat the real
currency on name alone; the fix never came back to `gates.py`. Selection is now by usage, the hint
list gained `coin|gold`, and gate 16 prints the chosen currency and its runners-up so a wrong guess
is visible rather than silent. Declaring `board.economy.currency` skips the guess entirely.

**Doctrine.** `references/the-voice.md` R1 gains the cost clause (with the shape worth stealing —
DoL's *"Take them all out at once | Dance: Impossible"*, a label that states the check **and whether
you currently pass it**, where failing still paid). `references/the-economy.md` gains gate 21 in its
checked table plus a warning section on both bugs. `DOCTRINE_GAPS.md` study 5 R3 marked graduated —
and corrected: it extends **item 2** (interface text), which was already closed on 8-12. The plan
that commissioned the study called the label rule "Tier 1 item 4"; item 4 is scene prose.

**Verified.** steam **17/19** and back_home **13/18**, both unchanged. Vesper **6/17 → 6/18** — the
price gate now judges instead of reading n/a, and its economy gates moved from the wrong currency to
the right one: `money gates something` FAIL→PASS on the costs fix, and the new gate fails on three
real hidden prices.

---

## 2026-08-13 — **Study 5: the field, played rather than parsed — and gate 20 counts the wrong thing**

`DOCTRINE_GAPS.md` gains Study 5 and Appendix C. This is the first study in the skill grounded in
playing games rather than reading their source, which the skill's own `references/agents.md` had
already argued for: *"the three games that were actually played produced every single heat finding
in the corpus, and the twenty-seven that were only parsed produced none."*

**What changed.** `DOCTRINE_GAPS.md` only — Study 5, Appendix C, and a Log row. **No reference file
and no gate was touched**, deliberately: two of the study's six outputs contradict decisions already
shipped, and resolving those is LO's call, not a silent edit.

**Why.** Three rules were live in `gates.py` and the reference files as inferences nobody had ever
observed — gate 20's 8-choice cap, guidance-must-exist, and `the-economy.md` R2's spread requirement.

**What it found.**

- **The `generic_porn_game` menu outlier does not exist.** The corpus parse put it at a median of 18
  links/screen, which was the single strongest argument that our cap was too low. It builds its hubs
  out of image buttons, and the parse counted the `<img>` tags. Real median: **4**.
- **Gate 20 counts the wrong quantity.** Every screen above ~12 choices in the corpus is a builder,
  roster, wardrobe or tracker. Among play surfaces, only DoL's streets exceed 8 — and a 12-link DoL
  street is 4 onward-travel exits + 4 standing travel affordances + **3–4 actual decisions**. Field
  median for things-to-do-here is **3, max 4**. Fourth denominator mismatch in this skill's history.
- **Guidance-must-exist confirmed 4/4**, by four different mechanisms, all always-reachable, all
  naming a place.
- **`the-economy.md` R2 marked *not established*** — the `shady_deals` session ended at 17 turns,
  before its sinks were walked. Recorded as untested rather than reported thin.
- **`engine.md` §15 is now contradicted by four games.** Every corpus door states its own
  requirement, including the exact tier (*"Skulduggery required: D"*, *"(Need Exhibitionism 2)"*).
  The locked-door gate was withdrawn on 8-12 *because* §15 ruled the other way; it is re-opened here
  on evidence that did not exist then, and flagged for revision rather than re-added.
- **M4 baseline**, which we had no number for at all: DoL moves state on **93% of turns, median 16
  variables**, against a corpus median of 2. `generic_porn_game` ran six identical mall loiters with
  zero state movement and byte-identical prose.

**How verified.** 198 turns across five games through `.claude/skills/twine-game-explorer/scripts/live.js`,
every turn logged to `game_explorations/study_*/study_turns.jsonl` with passage, visible choices,
engine state snapshot and explicit hits scored by `gates.py`'s own frozen `EXPLICIT` regex. Two
instrument bugs were caught and fixed mid-study, both of which would have inverted a finding — a
text-only link count that read image-button hubs as one-choice screens, and `live.js`'s
`variables_diff` being rebaselined by this study's own `eval` calls, which reported 0/59 turns of
state movement for a game whose arousal meter was visibly climbing. Scores unchanged (nothing in
`gates.py` was edited): **steam 17/19, back_home 13/18, vesper 6/17.** (Vesper read 5/17 on one
mid-session run and 6/17 before and after — a concurrent session is editing that game. Neither
number is attributable to anything here.)

**Free-play follow-up, same day.** A second unstructured DoL session (43 turns,
`game_explorations/dol_free/`) revisited surfaces repeatedly and diffed the rendered prose — the one
measurement `the-surfaces.md` R6 said it was waiting for: *"A threshold arrives when the play study
does."*

**`references/the-surfaces.md` R6 rewritten.** It said *"A hub re-entered daily whose first paragraph
never changes is a dead screen. Band it on whichever tier the location serves."* Measured: a DoL
location's opening sentence is **byte-identical on every visit** — six visits to one cafe, six times
the same first sentence — and it is the least dead game in the corpus. The variation is real and
dense but lives in four other places: a condition clause appended to the identity sentence (weather
and crowd, not progression), one presence line per NPC actually there, movement in the choice list
itself (5 → 9 → 8 across six visits), and events that replace the whole screen. On a repeatable
*action* rather than a room, variation is a scenario draw — eight cafe shifts produced five distinct
scenarios.

This also explains the seam that forced R6 to become a lint on 8-12: our TOML test asked whether the
opener carries a conditional block, so our games scored **0/22, 2/12, 11/29** against a practice the
reference game does not follow. R6 stays a lint with no threshold; what changed is that we now know
what to count. `DOCTRINE_GAPS.md` study 5 gains section R7 with the visit-diff table.

Also observed and worth keeping: DoL's labels state not just a requirement but whether you currently
meet it — *"Take them all out at once | Dance: Impossible"* — and failing that check still pays
(£8.50, minus respect). Free play surfaced it; a cost-in-label checklist would not have asked.

**Ruling on the two flagged items, same day — and both inverted on reading the source.**

**`engine.md` §15 stands unchanged. The study's claim that it was contradicted was wrong.** §15
governs `locked_text`, which **replaces** the action label — *"the player never sees what the action
was called"* — and prefers the want. Re-read against the four field doors: DoL's street label is
`Strip club (0:01)` with the opening hours on the passage *behind* it; CoT's is `[1] Strip` with the
Exhibitionism requirement in the body *after* clicking; shady's is `Check the local stroll.[7]` with
the gate in *adjacent* prose; GPG's `Enter (CLOSED)` is want **plus** suffix. **All four keep the
want on the label**, which is what §15 asks for. The study had compared a label-replacement rule
against evidence about where reasons are *placed* — a different axis, and the same denominator error
in new clothes. The withdrawn locked-door gate stays withdrawn. `DOCTRINE_GAPS.md` R4 rewritten with
the correction kept visible rather than edited away.

**Gate 20's ceiling of 8 stands; its denominator was never the problem.** The decisive fact came
from the code, not the play log: **259 of 259 choices in `steam` and `back_home` carry
`targetType = "node"`** — our engine renders location-to-location navigation as chrome, so gate 20
already counted decisions rather than links. The "12 links vs 23 choices" mismatch was in the
study's own comparison. `scripts/gates.py` G20 changed anyway, two lines: choices with
`targetType = "location"` are excluded, and the gate now reports "decisions" rather than "choices".
A **no-op today**, taken because the engine does support location targets (`v2.py:13252`). The
ceiling was **not** lowered to the field maximum of 6 — five games on one route each cannot carry
that precision, which is the failure that demoted R5 and R6.

**Verified:** scores identical before and after the code change — **steam 17/19, back_home 13/18,
vesper 6/17** — and G20 still fires on steam with its wording updated
(`9 location screens offer more than 8 decisions · hub_scrub_room @the_scrub_room: 17 decisions`).

---

## 2026-08-13 — **A goal-less card draws no frame, and that is how a finished arc ends up looking live**

`references/engine.md` §23 documented the three render frames in the right order and stopped there,
which left the most consequential case unstated: a card with no `goals` and no `terminal` matches
**none** of the three. That is not a blank row — the card still renders its `text` and its 💡 tip, so
it reads as an objective with nothing ticked yet.

Measured on `vesper` 0.1.8: at the end state the guidance page drew five sections, **four of them
closed arcs**, every one of them shaped like live work. The author walked the build to its final beat,
opened the page, and could not tell the game had ended.

Section 23 now states the trap, the fix (`terminal = true` on the last card of every arc), and the new
`terminal_text` override with its file:line pair — plus the cap that matters: **exactly one card per
game may set `terminal_text`**, since it promises future content and a closed-forever arc must not.
The full authoring rule, including the arc-complete-is-not-surface-closed split, lives in the
`author-game` skill's `references/quests.md` §7, updated the same turn.

Verified: green build, 5 `terminal` + 1 `terminal_text` in the built HTML, new 49/49 live suite, and
the two suites that read the guidance page (`live_beat_0084` 82/82, `live_rev141_bastien_cut` 73/73)
unchanged.

## 2026-08-12 — **Two gates built, both demoted to lints, and the measurement is why**

`the-surfaces.md` R5 (ungated doors) and R6 (frozen openers) are real rules that a real game
ignored, and the plan was to make them gates — the whole lesson of this project being that
paragraphs get skipped and only checks hold. **Both were built. Neither threshold survived the
check.**

**R5 — the ceiling had to be invented.** Set at 50%, Steam sits at exactly 50.0% and passes while
vesper fails at 52%. That is noise being scored. There is no field number, because "does this link
carry a condition" is not separable from engine plumbing in someone else's compiled game.

**R6 — not field-comparable at all, and the check nearly shipped backwards.** Measured on our TOML
(does the opener carry a conditional block?) our games look catastrophic: **steam 0/22 menus vary,
back_home 2/12, vesper 11/29.** Measured on the field's only available instrument — `<<if>>` present
in a built screen's text — the field median is **86%**, and re-measuring *our* built games the same
way gives **back_home 84%, steam 89%**, i.e. at or above the field median.

Both cannot be true. They are not measuring the same thing: in compiled output `<<if>>` wraps gated
choices, media and presence checks as well as authored prose banding, and the two cannot be told
apart in a game whose source we do not have. **A gate shipped on the first number would have failed
every game this project has built, on evidence that does not support it.**

> **Third time in this skill's construction that a measurement compared two different denominators**
> — after the explicit floor (whole-source units vs location beats) and the sentence ceiling (built
> HTML vs authored TOML). Assume the seam is there until it is ruled out.

Both are now `lint_screen_shape()` — printed every run, never scored:

```
steam       107/214 choices open on turn one · 22/22 standing menus never change their prose
back_home    12/57                           · 10/12
vesper       65/124                          · 18/29
```

Those numbers are real and worth reading. What is missing is any basis for a pass/fail — and
**whether a room's narrative actually changes on re-entry is a question only playing answers**,
which is what the play study agreed this session exists to settle. Scores unmoved: steam 17/19,
back_home 13/18, vesper 5/17.

---

## 2026-08-12 — **Presence is not placement: the economy gate rebuilt, and the heat floor made to admit what it is**

Two gates were giving false green on Steam. Both fixed; Steam drops **18/19 → 17/19**.

### Gate 17 — counting sinks was never the question

It passed Steam at **21 sinks : 20 sources** while **twelve of those sinks sat on one front desk**:
the water test, the advert, the electric, two wages, the frontage, the occupancy fee — in the same
undifferentiated list as *"Look up at the board."* That is a shop counter, not an economy. Money
leaves the player in one place, by one gesture, and no room in the world is ever the reason for it.

Now resolves each sink to its location and fails when **more than half land on one** — applied only
once a game has five or more sinks, below which concentration is meaningless. Steam fails at 12 of
21; `back_home` is unaffected (one sink, under the threshold) and still fails on the 1:12 ratio.

**The galling part:** this is the exact distinction the explicit-in-repeatable gate has made since
day one — *where content sits, not how much of it there is* — and the economy gate was built a
fortnight later without it. `the-economy.md` R2 now carries the placement half: **a sink belongs
where the thing being bought lives**, so the room it improves is the reason she needs the money.

### Gate 2 — a bare pass now says it is a bare pass

Steam cleared the explicit floor by **0.1 points** (7.6% against 7.5%) and printed a clean PASS.
That floor is the reference game's own 7.5–9.3% band — and that game is the **coldest of the 18
sandboxes** measured on this same word list, against a field median of 33.3%. So a game can sit
inside the reference's historical range, be four times colder than its genre, and read as green.

The threshold is unchanged, because there is no honest field-comparable number yet: the field was
measured on built HTML and this gate reads authored beats. What changed is that a pass between the
floor and 12% now prints **`← BARE PASS`** with the reason — *clearing this floor is not evidence
of heat; it is evidence of not being empty.*

**A calibrated heat threshold remains open work**, and it needs our own built games measured on the
field's instrument to exist at all. Recorded rather than guessed.

### Gate 3 — checked, and it was fine

Flagged in review as hiding volume behind a percentage. It was not: it already prints the absolute
count (*"93.8% of 65 explicit beats"*). The number was visible and the reader — me — treated the
percentage as the headline. **No change made.** Noted because a fix applied here would have been a
fix to nothing, and the review claim was wrong.

---

## 2026-08-12 — **`engine.md` §24: the facts that fake a broken game — promoted only after verifying them**

Steam's session could not find what it needed in `engine.md`, worked six things out by trial and
error, and wrote `games/steam/ENGINE_NOTES.md`. **Two of the six this project had already paid for**
— the day-name fact and the entity-encoding trap — both logged in *this changelog* rather than in a
reference file, so a fresh session lost time rediscovering them.

> **A changelog is a diary. Nobody reads it before starting work. If a fact is needed to do the job,
> it belongs in a reference file.** That is the whole reason for this entry.

### The verification came first, on LO's instruction, and it earned its keep

LO's call before promoting anything: *"these were written by the same agent building the game, so
they might be true or might be not."* Correct. Checked all six against source:

| claim | verdict |
|---|---|
| `State`/`Engine` on `window.SugarCube` | ✅ true — `window.SugarCube=` with `State:State`, `Engine:Engine`, in the built file |
| `current_day` is a day NAME | ✅ true — `v2.py:3273` `[…].indexOf(timeState.current_day)`, plus `:3444 :3588 :3643 :3706` |
| `setup.getNpcsPresentAtLocation(slug)` | ✅ true — `v2.py:4773`; the engine's own nav badges call it at `:19297`, `:19321` |
| `pickQuestsCards` takes one scope | ✅ true, and **understated** — `v2.py:14838` `if (scope !== "story_goals") return [];` |
| Playwright text selectors break | ⚠️ true, but **tooling, not engine behaviour** |
| page source is entity-encoded | ✅ true — **663** `&lt;&lt;set` against **3** literal in one build |

**Five promoted, one rejected.** The Playwright note went to `references/agents.md` under The
Player, not into `engine.md`: that file's value is that every line carries a source citation, and a
tooling observation cannot. Putting it there is how the file stops being trustworthy.

### And verifying exposed an error in §23, written the same morning

`§23` described `pickQuestsCards` as *"returns every matching top-tier card"* and **never mentioned
the scope guard** — which is the function's **first line**. Authored from source, and still missed
it. Corrected in place with the guard quoted, and the correction says so rather than being tidied
away: a wrong scope string produces an empty guidance section, silently.

### What §24 is, and why it is framed the way it is

**"Reading a built game from outside — four facts that each FAKE A BROKEN GAME."** Not a reference
list. Every one produces a false alarm indistinguishable from a real defect: bare `State` reads as a
dead build · a numeric `current_day` empties every room and reads as broken presence · hand-rolled
presence drops overnight windows and reads as an absent character · grepping the page for literal
`<<set` returns zero and reads as missing content. **The entity-encoding trap has now cost this
project twice** — once on a built game, once on an 18-game corpus where it produced a confident and
completely wrong measurement table.

### New operating rule in `SKILL.md`

**A note written by the agent that did the work is a CLAIM, not a fact.** Verify against source with
a `file:line` before promoting. Six claims checked: five held, one was misfiled, and the check
exposed a defect in a same-day reference section. Trusting the handback would have shipped both.

`games/steam/ENGINE_NOTES.md` keeps its content and gains a header pointing at §24, so the
game-local copy is not mistaken for the source of truth. Worth recording that the session had
already labelled its own notes **"LIVE-VERIFIED, NOT SOURCE-CITED"** — an honest handback is what
made the check cheap.

**Verified:** every promoted citation re-grepped against `v2.py` immediately before writing; scores
unmoved by a docs-only change — `steam` 18/19, `back_home` 13/18, `vesper` no crash.

---

## 2026-08-12 — **The missing axis: `the-surfaces.md`, and the sentence of mine that caused Steam**

`games/steam` was authored in a clean session by a reader of this skill, with no context carried
over — the honest validation `back_home` could never be. **It scored 18/18, and its front desk has
23 choices on one screen.** Full findings: `games/steam/REVIEW.md`. This entry is the fix.

### The cause was a sentence I wrote, with no scope on it

`engine.md` §19's *rule* is narrow and correct: two repeatable canvases binding **the same NPC** at
the same location with overlapping windows collide, and only one renders. Steam's `hub_front_desk`
and `hub_spring_street` **bind no NPC at all**, so it never applied to them.

But the paragraph attached to it read *"The fix is the engine's own advice, **and it is also the
better design**: make the second canvas a triggerless rung and hang it off the existing hub as a
CHOICE."* No scope, and it calls itself the better design. A careful author applies that everywhere
— and did. §19 now scopes the advice explicitly and points at the new file.

### What v2 was missing, stated properly

`SKILL.md`'s three content kinds — STANDING / TRIGGERED / MILESTONE — all answer **when content
fires**. **None answers which screen it lives on.** That axis simply did not exist in v2, so the
author invented one and picked the shape the loose sentence pointed at.

**New: `references/the-surfaces.md`.** The question is *who is this aimed at* — a person → their
hub, one per schedule row · the room or herself → its own located canvas · her, done to her → a
substitution. They never share an exit block. Carries the **object test** (is a person the object of
the verb? then it is a hub rung; *"Count the till"* is not), **money is not a scene** (11 of Steam's
23 desk choices are purchases sitting beside *"Look up at the board"*), ungated choices are the
minority, and the opener moves.

*(The incumbent skill solves this with a four-lane model and states the same separation at
`lanes.md:96`, including a pronoun-in-the-verb test and the observation that "all Lane 1 =
transactional menu game". v2's version is organised by **who the content is aimed at** rather than
by who decides it fires, because that is the question an author can answer while writing, and
because v1's lane budgets are keyed to arc shapes v2 does not have. Studied, not copied.)*

### Gate 20 · a place is not a catalogue — **measured, not asserted**

Re-pulled the 18-game corpus and counted player-facing links per non-system screen:

```
median screen ..................... 2 links
median p90 ........................ 4 links
screens offering more than 12 ..... ~2% (field median)
```

**Ceiling set at 8** — double the field's ninetieth percentile — for any repeatable,
location-bound canvas. Triggerless rungs are exempt; they are link targets, not screens.

The nuance that stopped this being a flat cap: **big screens do exist in good games.** The reference
game runs 2.9% of its screens above 20 links — and they are *catalogues*: shops, wardrobes,
character creation. A catalogue is legitimately long. **A place the player returns to daily is not
a catalogue**, and Steam's error was merging one into the other.

**Verified:** `steam` **18/19** — the gate names all nine offending screens (23, 19, 19, 18, 17, 16,
14, 12, 12) · `back_home` **13/18**, passes at a max of 7 · `vesper` 5/17, no crash.

### And the thing Steam proved about how doctrine has to be written

Everything encoded as a **required field** came back correct and unprompted: `board.map` with 6/6
real homes, `board.economy`, `board.guidance`, 24 quest cards, 6/6 ladders with end cards, all
locations reachable. Everything encoded as **advice** was not: the heat guidance added that same
morning (*"clear it, do not aim at it"*) produced a game sitting on the floor at 7.6%.

**Second game running.** Declarations and gates hold; paragraphs do not. Every future doctrine
change should ask which of the two it is before it is written.

---

## 2026-08-12 — **Tier 1 graduated: four studies become doctrine, and the scoreboard grows teeth**

The four studies in `DOCTRINE_GAPS.md` are now reference files, and their checkable half is now in
`gates.py`. **`back_home` scores 12/17, exit 1** — the ten original gates all still pass, and every
new failure is a defect the game shipped with. That is the intended outcome: LO's call was one
scoreboard, not a second unscored tier, because a check that cannot fail is exactly the failure v1
documented against itself.

**New reference files** — self-contained, no cross-reference to the incumbent skill, written in
`want / board / release` vocabulary:

- **`references/the-map.md`** — the map is a place, not a room list · residents have homes ·
  if she travels there is something to travel through · the graph owes the prose · travel friction.
- **`references/the-voice.md`** — the game's own voice, plain and never performing: labels answer
  "what happens if I click", every ascent tier carries a visible ladder, name the feeder not the
  number, nothing retires into silence.
- **`references/the-economy.md`** — money must gate content · sinks outnumber sources · the
  obligation is real and has a face · prices move with state · no free uncapped income.
- **`references/register.md`** expanded — sentences run short, second person is the genre standard,
  dialogue as a direction not a threshold.

**`gates.py`: +7 gates, +1 lint, and a header that now names two measurement bases.**

```
11 world reachable          12 residents have homes      13 guidance exists
15 no chain ends in silence 16 money gates something     17 sinks >= sources
18 no free uncapped income  19 sentence length (ceiling 14)
lint · the prose names places the map does not have
```

**The declare-then-check pattern is now an operating rule**, added to `SKILL.md`: where a property
cannot be inferred from the TOML, the board declares it and the gate checks the game against its own
declaration. `state.md` and `templates/board.toml` gain `board.map` (shape, dwelling, exterior,
**homes**, bridges) and `board.economy` (currency, obligation, **sinks**). A gate with no declaration
to check against reports **n/a**, never a pass.

**`engine.md` §22–23** — twelve verified facts v2 never had. Locations can charge a per-entry
`costs = { time, energy }` (`template_import.py:170`, `:1778`; `v2.py:4681`, `:15276`) — the
mechanical answer to a premise that says *"ten minutes' walk away"* while arriving costs nothing —
plus `entry_conditions`/`blocked_message`, `offscreen`, `is_container`. And the guidance table is
`[[quest_cards]]` (`template_import.py:2456-2462`), gated on `quests_engine = "v2"`
(`v2.py:14711`), whose **conditions use a separate evaluator with no fail-open** (`v2.py:14878`) so
`version = "1.0"` must never be pasted onto a card.

### ⚠️ One study output was WITHDRAWN on contact with the engine, and it is the most useful thing here

Study 2's R4 proposed a gate requiring every locked door to carry `locked_text`. It was built. It
fired on **7 of 8 doors in `back_home`** — and then `references/engine.md` **§15, which already
existed**, turned out to rule the other way and rule deliberately:

> omit `locked_text` and the greyed row shows the action ("Stop pretending it's a secret") — a *want*
> the player can name, which is what sells the next release … **Prefer the want unless the gate is
> genuinely obscure.**

Every one of those seven doors was following the skill correctly. **A check that fails a game for
obeying the doctrine is a bug in the check**, so no gate shipped; R4 was rewritten as *"the wall
shows the want, the card shows the route"*, and `games/back_home/REVIEW.md` **G2 was withdrawn as
not-a-defect**. Also added to `SKILL.md`'s operating rules, because the same trap will recur:
**when a gate you just wrote fails a game, check the skill before blaming the game.**

### Two other corrections the build forced

- **`back_home` has twelve money sources, not three.** `REVIEW.md` E1 counted only the clean shop
  income; the gate counted every canvas that grants money, including nine transactional rungs.
  1 sink : 12 sources. The defect is worse than first recorded, and it was found by counting what
  the game does rather than what the author remembered.
- **The sentence-length figure is instrument-dependent and the constant now says so.** The field
  medians come from parsing built HTML; the gate reads authored beat text from the TOML. The same
  game measures 16 on the first and **13** on the second, so it passes the ceiling of 14. The
  threshold spans a seam and is APPROXIMATE — it catches drift, it does not certify a match. Closing
  that gap would need the field re-measured on TOML we do not have.

**Verified:** `gates.py back_home` → 12/17 exit 1, every new FAIL cross-checked against a
`REVIEW.md` finding · `gates.py vesper` → 5/18 exit 1, does not crash, `residents have homes`
correctly **n/a** with no ledger present, and it independently caught **18 of vesper's 27 locations
unreachable on foot** · `--json` parses with 17 gates and both lint keys.

---

## 2026-08-12 — **`DOCTRINE_GAPS.md` opened: what v2 never learned about building a good game here**

New file, `DOCTRINE_GAPS.md`, next to `STATUS.md`. No reference file changed.

**The trigger.** LO played `back_home` and asked why it has no quests. Traced it: `templates/board.toml:26`
ships `quests_engine = "v2"`, which lights up a sidebar entry and a "What's Next" page, and across all
1,367 lines of v2 doctrine there is **zero** quest instruction and **zero** quest check in `gates.py`.
Verified: `setup.quests_cards = []` in the built game. A game built exactly to spec ships an empty
guidance page.

**The root cause, and it is bigger than quests.** v2's doctrine was derived solely by measuring one
reference game's source. That game has no quest log. **A doctrine derived from measuring one game
cannot contain anything that game lacks** — even when our engine ships the feature and the incumbent
skill teaches it. Measured: the incumbent carries 38 reference files / 9,672 lines; v2 carries 7 /
1,367, or **14%**. Nearly every finding in `games/back_home/REVIEW.md` maps to a file v2 does not have.

**The decision (LO's, this session): v2 never links to or imports a v1 file.** Not tidiness — v1's
references are welded to v1's pipeline (`step-5-blueprint.md` says "Step N" 24×, `step-3-casting.md`
16×, `content-framework.md` 15×), so importing one imports v1's chapter shape into the skill whose
thesis is that the shape was wrong. Same failure as the `prompts_v2` dependency. Each item is studied,
not copied, and every study ends in a **check** rather than a paragraph — the case for which is made by
v1 against itself at `location-design.md:257`, on a locked-flag bug that *"shipped twice: v1's Dining
Room, then again in the rebuild written to prevent it."*

**Contents:** a 12-item inventory over three tiers, save-safety parked as separate work (and argued to
matter more for v2 than v1, since a never-ending product lands every release on live saves), the
item-2/item-4 boundary settled (interface text is plain and functional; RTS-flat governs everything
read *after* a click), and **study 1 — map & space** in the five-part format.

**Study 1's substantive output:** four engine capabilities verified against source that `engine.md`
does not carry and must — location travel-friction `costs = { time, energy }`
(`template_import.py:170`, `:1778`; `v2.py:4681`, `:15276`), `entry_conditions` + `blocked_message`
(`template_import.py:159-160`, `:1775-1776`; `v2.py:6590`), `offscreen` (`template_import.py:154`),
and `is_container` + `default_entry` (`:153`, `:3968`). Travel friction is the mechanical answer to a
premise that says *"ten minutes' walk away"* while arrival costs nothing.

Also recorded: **`back_home`'s missing-bedrooms defect passes v1's entire 13-point location audit** —
274 lines of map doctrine with no rule that a resident needs a room — so v1 is evidence about the
problem, not the answer.

### Study 2 — how the game talks to the player *(same day, format approved by LO after study 1)*

Names the category no skill owns: **everything the player reads that is not the story** — room names,
activity labels, the guidance page, meter band words, locked-door text. Four `REVIEW.md` findings
(G1 G2 W5 W7) with one cause. v1 splits this across two files and two gaps: `quests.md` covers cards,
`location-design.md §3` covers room names, and activity labels, `locked_text` and meter words are
covered nowhere — which is how a game can hold a consistent naming style and still be unreadable.

**Where v1 is wrong, beyond the split:** of `quests.md`'s 285 lines, the rule about how a label should
*read* is one paragraph; the rest is engine mechanics. And its top tier is a **mission spine** — *"the
Story-Goals column… the mission's current want"* (`:173`) — which a v2 game does not have. Copying it
would smuggle a story shape into a release stream, so v2 needed its own answer: **the top of the
guidance page is the ascent tiers themselves**, one card per band via v1's stepped trait-band shape.
That falls out of v2's architecture instead of being borrowed.

**Carried over from v1 because it is measured, not asserted:** the label is a walkthrough line —
place + person + verb (`quests.md:81`); and **a meter-gated rung names its FEEDER, not its number**
(`:91`) — *"the HUD already shows the number; the ROUTE to raising it is what the player can't see."*
That is the single most load-bearing rule for v2, whose every gate is a meter.

**One rule v2 owns harder than v1 did:** an arc whose last card retires with nothing behind it makes
the character's whole section disappear. v1 found it (Renner's heading, unnoticed for eleven beats).
In v2 it is worse by construction — a product that never ends turns every topped-out character into
permanent sandbox content at the exact moment the chain goes silent.

**Corrected while verifying:** the authored table is **`[[quest_cards]]`** (`template_import.py:2456-2462`,
`class QuestsCard` `:997`), *not* `[[quests]]`. `games/back_home/REVIEW.md` G1 said the wrong table name
and was fixed; the finding itself stands — zero `quest_cards` across all five phase files, and
`setup.quests_cards = []` in the built HTML.

**Eight more engine facts verified and flagged for `engine.md`**, including that **quest conditions use
a separate evaluator with no fail-open** (`v2.py:14878`) — so the `version = "1.0"` key that canvas
conditions require must *not* be pasted onto a quest card — and that the sidebar next row calls the
identical renderer as the page (`v2.py:15454-15456`), so there is no such thing as a separate sidebar
quest.

**The pattern now holds twice.** Both studies' load-bearing gates work by having the board phase
**declare** a property the TOML cannot express, then checking the built game against that declaration
(study 1 Gate B: where each resident sleeps; study 2 Gates C/E: which tiers and characters owe cards).
Proposed as the skill's standard gate shape rather than being rediscovered per study.

**Also held twice:** each study refuses to gate the thing it cares most about — *"is the map a coherent
place"*, *"does this label read well"* — because neither is mechanically decidable, and a check that
measures a proxy is how `back_home` shipped 10/10 with no street.

### Study 3 — money & pressure. **The first study measured on more than one game.**

LO's instruction: verify against real games, and *"not just 3 or 4 — get at least 10."* Pulled **18
shipped browser sandboxes, ~62,000 passages**, as complete single-file SugarCube source. URLs came from
this project's own prior live-play sessions in `game_explorations/`; a `mopoga.com/<slug>` page carries
the real file URL in `data-game-url`, and those `/embed/` URLs serve the full compiled game. Corpus,
method and limits recorded in `DOCTRINE_GAPS.md` Appendix B.

**Two extraction bugs found and fixed before any number was trusted**, both logged because the first
pass produced a confident wrong table: (1) passage bodies are **HTML-escaped** in a compiled Twine file,
so every `<<set>>` regex silently matched nothing — DoL read as *"0 spending"* against 372 gates, which
is what exposed it; (2) money mostly moves through **per-game widgets**, not raw `<<set>>` — DoL uses
`<<money -350000 "farmUpgrades">>`, `life_at_university` uses `<<addmoney>>`/`<<redmoney>>`. The final
extractor discovers each game's money widgets from its own `<<widget>>` definitions. Currency selection
was also changed to pick by **usage** rather than name frequency, after `road_to_success` resolved to the
decoy `$game.randomMoney`.

**The measured rules:** money gates content at a **median 67.3 conditions per 1,000 passages** (every
sandbox in the set does; `back_home` is at **0**, independently confirmed from its TOML) · **sinks
outnumber sources at a median 2.2:1** (DoL 1.76:1; `back_home` has three sources and one sink) ·
**14 of 19 carry a real recurring obligation** (DoL says *rent* 130 times — the one thing `back_home`
gets right) · a median **24% of money movements carry a computed rather than literal amount**. Plus one
rule from the failure rather than the corpus: **no free uncapped income**, the single line that would
have caught `E1`.

**Where v1 is wrong here, and it is a precise defect:** `rent.md` §8's safety rule guards only the
downside — *"rent that can't be paid isn't pressure, it's a scripted loss"* — with **no rule against
trivially payable**, and no ratio to tune against. `back_home` obeyed v1 exactly and the pressure
evaporated. v1 is also scoped to rent as a mechanism and develops no doctrine of sinks at all, which is
why the game ships **zero items**.

**And the finding that justifies the whole DOCTRINE_GAPS exercise:** DoL carries **738 money movements
and 372 money gates**. v2 derived all ten of its thresholds from this game's source — words, locations,
explicit ratios — and never once measured its economy.

**Side result: `games/back_home/REVIEW.md` O1 is resolved, not by argument but by holding the file.**
`gates.py:7` cites the reference as *"1.7k → 15.6k units"*; the pulled source contains **15,587
`<tw-passagedata>` passages**. So a "unit" is a whole-source passage — combat, systems and UI included —
while `gates.py` counts beats in **location prose only**. The two denominators were never the same, so
back_home's 27.8% against a 7.5–9.3% band was never a valid comparison and **no dilution pass is owed**.
`gates.py`'s header should say so, or this gets re-litigated a fourth time.

**Verified:** all 18 files confirmed SugarCube with non-zero passage counts before parsing; every rule
above recomputed after both extractor fixes; `back_home` run through the identical instrument, with its
non-comparable flow counts excluded from the medians and marked as such.

### Study 4 — how the prose is written. Same corpus, `gates.py`'s own explicit regex.

`v1/rts-flat-prose.md` is 735 lines, the largest file in either corpus; `v2/register.md` is 111 and
covers **one topic** — how to write an explicit beat. Sentence length, dialogue, how an ordinary
non-sexual paragraph reads: undocumented in v2.

**A third extraction trap, and it invalidated the entire first pass.** The longest "prose" passages in
every game are **widget libraries and CSS** — `back_home`'s was the engine's own widget library, DoL's a
combat widget, *Road to Success*'s a styled laptop UI. Fixed by dropping passages tagged
`widget`/`script`/`stylesheet`/`init`/`header`/`footer`, bodies defining widgets, and — the load-bearing
filter — **any passage whose stripped text is under 40% of its raw length.** Nothing in the study is
quoted from the polluted pass.

**R1 — the one length measure that transfers: `back_home`'s sentences are too long.** Median sentence:
**field 10 words, DoL 9, `back_home` 16** — third-longest of eighteen, 60% above the field. First hard
number confirming our prose is denser than the genre, which is what "RTS-flat" was always reaching for.
Proposed as **Gate I, ceiling 14** — the first gate in this exercise that measures *writing* rather than
structure.

**R2 — second person is the genre standard, 13 of 17 games.** `back_home` at 94% *you/your* is the
highest in the corpus. v2's `narration_person` default is **validated by the field** — the one piece of
v2 prose doctrine the corpus confirms outright.

**R3 — the reference game is the coldest game in its own genre.** Percentage of prose passages carrying
3+ frozen-list words: field median **33.3%**, `back_home` 43.4%, **DoL 7.5% — last of eighteen.** Note
`gates.py` sets `EXPLICIT_BEAT_FLOOR = 7.5`; this run reproduces that derivation independently on a
different unit and shows the number is **a property of DoL, not of the genre.** Valid as a floor, badly
miscalibrated as anything resembling a target. **This closes the `back_home` heat worry a second time,
from a second direction** — O1 showed the denominator was wrong; the field now says 43.4% is mid-pack
with five games above it.

**Where v1 is wrong — and the one place it cannot be judged.** Its headline claim, *"RTS runs 0.73
narration words : 1 dialogue word … every game this skill has shipped runs 5:1 to 19:1 the other way.
This is the drift"* (`rts-flat-prose.md:12`), rests on **one game** — the same methodological error v2
made with DoL. And it is **untestable from the compiled artifact**: *Road to Success* is built from
HTML/CSS interior markup, so only **31 of its 373 passages** survive prose extraction. The study does not
claim the number is wrong; it records that a rule calling everything else "drift" has never been checked.
What the corpus does support is the direction — the two most prose-dense games in it are the two most
dialogue-heavy (DoL 2.7:1, `course_of_temptation` 3.8:1) against a field median of 33:1.

**Explicitly not transferable, recorded in Appendix C:** passage length (our engine emits a whole canvas
as one passage — `back_home` 429w median vs field 175w measures architecture, so **the 35–40-words-per-beat
rule is neither confirmed nor refuted here**) and v1's dialogue ratio, above.

**Verified:** every figure recomputed after the tag/markup filter; `back_home` run through the identical
script; per-game sample sizes reported so the small ones (`road_to_success` 31 passages, `back_home` 122)
are visibly weaker than DoL's 10,215.

**Verified:** every engine citation above read from source this turn; the v1/v2 line counts from `wc -l`;
the quest counts from `grep` over the skill and from `setup.quests_cards` in the built HTML.

---

## 2026-08-11 — **v0.1 SHIPS: 10/10. The first green game this skill has ever produced.**

```
[PASS]  location fill        8 locations · 36,035 words · mean 4,504 · median 4,381 · anchor 27%
[PASS]  explicit floor       27.8% of 270 beats carry 3+ explicit words (floor 7.5%)
[PASS]  explicit in repeatable  100.0% of 75 explicit beats are re-enterable
[PASS]  repeatable explicit media cycles  49 pooled, 0 fixed single-clip
[PASS]  traversal heat       7/8 locations (88%) carry a cycling explicit pool
[PASS]  standing surface     4/4 characters findable and scheduled
[PASS]  milestones open something   4 of 4
[PASS]  meter ceiling        0 visible meters rise past their content
[PASS]  ends on an opening   8 choices render visible-but-locked
[PASS]  ascent tiers expand the world   nerve · exposure · need, all upward
────────────────────────────────────────────────────────────────
10/10 judged gates pass          EXIT CODE 0
```

`games/back_home` — **36,035 words of location prose, 8 locations, 4 characters, 270 beats,
75 explicit, 8 locked doors.** Nothing had ever passed all ten before; the promotion criteria in
`STATUS.md` require exactly this.

### The last room: the shop, and it stays cold

`the_shop` 654 → **2,952**, and **every beat in it scores 0 on the explicit floor, on purpose.** The
Want: *"the one room where no man wants anything from her, and that is its entire function."* It is
the counterweight to five rooms of heat, and `register.md` is explicit that a game far above the
floor is usually one that has stopped having non-sexual texture.

Four surfaces:

- **`activity_shift` 76 → 594.** The single most-repeated money click in the game was one paragraph.
  Banded on `need`: thirty pounds as pocket money, then as the four-shifts-is-the-rent arithmetic she
  cannot stop doing mid-transaction, then as *the only money in her life that arrives without a face
  attached to it.*
- **`activity_the_walk`.** Ten minutes each way is the only stretch of the day she is outside the
  house **and** outside the shop — the one part of the map nobody in the game can see her in.
- **`activity_stock_hour`.** The room's declared job is *money that is hers* and there was exactly
  **one** way to earn in this game. A second lever on `need` that is not a man is what makes the
  trades elsewhere a choice rather than the only road.
- **`triggered_hannah_again`** — pays the logged promise. Three bands on `pride` that are three
  different answers to the same question: the voice that means no, the drink that actually happens,
  and the standing fortnightly lie to the one person who thinks she is basically all right.

**No new location for the drink.** *A release adds events, not places* — it happens off-screen and
arrives back at the counter. And Hannah stays **narrated, never declared**: an `[[npcs]]` entry would
fail gate 6 on the spot, which is why she speaks in quoted prose rather than `dialog` blocks.

### Verified live, end to end — not just the new surfaces

- Age gate → opening chain plays with **no state forcing at all**; `arrival_done` set, player lands
  at `her_room`.
- The full schedule grid on a **weekday and a weekend**: Ray 06:30 bathroom → Dean 08:30 kitchen →
  Marek 10:30–14:30 box room → Cal 16:30 front room + Marek 16:30 kitchen → Ray 18:30 garage → Ray
  20:30 front room. Saturday differs correctly (Dean 14:30 garage, no Ray bathroom row).
- **All eight locations render** with actions at a mid-game state: 5 · 3 · 3 · 5 · 7 · 2 · 6 actions.
- **Zero JS errors** across the whole pass.

### v0.1 closed out

`phase` flipped **`board` → `release`** in `v2_state.json`, with a `releases[]` entry recording
subject, what it added, what it opened and the gate scores. Per `the-release.md`: *never build a
"chapter" again.*

**13 promises stay open, and that is deliberate rather than accumulated.** Eight of them **are** the
locked doors — that is what "every release ends on an opening" means, and closing them would be
closing the product. The other five are plants with content owed: the lodger leaving in spring,
`keep_unpaid` changing the terms with Ray, Dean's uncharged version, Cal's eight hundred and forty,
and Ray finding out where the rent money came from. Nothing is cut; every one is a release subject.

### What this run cost, and what it produced

Six increments, **+17,153 words**, and every one of them turned up something the instrument could
see and a reader could not:

| # | room | the finding |
|---|---|---|
| 1 | bathroom | two harness facts that faked a broken game (the clock lives at `game_state.time_state`; blind cascade-advance double-applies effects) |
| 2 | kitchen | **the `clamp` bug** — every money grant capped at 100 against a 120 rent, so the rent was unpayable. `engine.md` §21 |
| 3 | her room | **a category name is not a sweep** — the register rule had been applied to "the sex loops" instead of to everything under the floor. `register.md` |
| 4 | box room | **the rotating slot was never split by lifetime** — room-scoped content must name the occupant by role. `the-board.md` |
| 5 | garage | the explicit-floor comparison **checked instead of acted on** — the reference denominator may not match ours, so the room was not diluted to chase a ratio |
| 6 | shop | one-scene characters are narrated, never declared — gate 6 enforces it |

Three of the six produced doctrine changes to the skill itself. The register defect appeared in
**new prose in four consecutive increments**, written each time immediately after re-reading the
rule against it — which is the strongest evidence yet for `register.md`'s own claim that it
reasserts the moment it is not being actively fought, and for keeping the per-beat scorer in the
loop rather than trusting a read-through.

**Still open, and now the top of the list:** the explicit-floor denominator question (28% against a
band that may not be comparable), media (47 declared `pool_dir` slots, zero files — deferred by LO
until after he plays it), and **the agents**, which remain the skill's largest architectural gap.

---

## 2026-08-11 — v0.1 fill 5/6: the garage, and a deliberately cold surface

**What.** `the_garage` 801 → **3,514 words** — the thinnest room in the game and the last big add.
Files: `games/back_home/toml_phases/5_scenes.toml`, `3_activities.toml`, the game's `v2_state.json`.

### The room was Ray's and had 309 words of him in it

The Want gives Ray a specific mechanic: *"he is careful, so every inch is expensive and deniable —
which makes an inch feel like a mile."* The front room is his **money** surface (rent, the ask, the
arrangement); the garage is where the deniable register belongs, and his garage ladder **topped out
at exposure 15** while his front-room ladder ran to need 75.

Two rungs and a door, verified live:

| rung | gate | the mechanic |
|---|---|---|
| `rung_ray_garage_hold` | nerve 35 | **deniability as an engine.** Out here contact has a *job* — holding the other end of a board — so it can happen and still be about the board. Bands on his lust: he stops saying sorry, then there stops being a job, and there is a fresh plank on the trestles every evening that nobody comments on |
| `rung_ray_garage_bench` | exposure 55 + his lust 30 | explicit, and it happens in the one room with a door to the outside. Afterwards he says *"Right."* and holds the door and asks Dean whether the football is on |
| *locked* "Ask him where the bench went." | nerve 75 | the room's door |

```
nerve10           tea · [LOCKED] where the bench went
nerve40           + what you've got on · hold the other end · [LOCKED]
nerve60 lust35    + stay out here after he's finished · [LOCKED]
nerve80           the locked row goes live
```

Ray already owns a need-75 door in the front room; nerve 75 here is a different axis and a different
want, so it is not the same promise twice. Dean's weekend ladder went 2 → 3 rungs
(`rung_dean_garage_bar`, exposure 45 + his lust 25 — three hours, empty house, door up a foot).

### The bench-shaped absence

The room's defining detail is a **gap**: the weight bench in her bedroom came out of this garage, in
the same fortnight the desk went to the tip. There is a rectangle of clean concrete on an otherwise
filthy floor and nobody in the family has ever mentioned it. It is planted in three canvases now and
the nerve-75 door is where it finally gets named — **logged as a promise, not paid**, because the
answer is a scene and this increment did not write it.

### A surface written cold on purpose

`activity_the_garage` (512 words, room-scoped, names no NPC) has **zero explicit beats and that is
the design**, not an oversight: a garage with nobody in it is not erotic, and `register.md` says a
game far above the floor is usually one that has stopped having non-sexual texture. It carries the
biro height-marks on the door frame that stop the year the mother left, and the two mugs Ray has
been filling the kettle for without ever mentioning it.

Also banded the two remaining flat presence-floor rungs, `rung_ray_tea` (147 → 500) and
`rung_dean_weights` (148 → 327) — the same treatment the kitchen and box-room floors got.

### The floor question, checked rather than assumed

Last increment I called 26.3% "3× the reference band" and treated it as a looming problem. Before
letting it drive design I tried to check the comparison, and **it cannot be checked from here**:

- `gates.py` measures **location prose only** — that denominator correction was made to gate 1 on
  2026-08-10, when the word count was found to include `base-combat` and `base-system`.
- `EXPLICIT_BEAT_FLOOR`'s own header cites the reference at **1,772 → 15,629 units**, which look like
  whole-source unit counts. If that denominator included combat, systems and UI passages and ours
  does not, **the two percentages are not comparable at the top end.**
- No reference snapshot is on disk. This stays a hypothesis.

What survives either way: it is a **floor**, the game clears it, and the discrimination test holds
(the measured-cold game scores 4.7% on this same instrument). So the garage was **not** diluted to
chase a ratio — Ray's arc genuinely lives in that room — and the cold surface is cold for its own
reasons. **Open question for after v0.1:** either re-derive the reference ratio on a location-only
denominator, or say plainly in `gates.py` that the upper comparison is not meaningful.

### Tally

```
[FAIL] location fill   8 locations · 33,728 words · mean 4,216 · median 4,381 · anchor 28%
       · mean location 4,216 words (need 4,500)
```

Explicit floor **26.3% → 28.1%** of 267 beats; explicit beats 67 → **75**; doors 7 → **8**; every
garage beat that was under the floor (`rung_dean_spot` 1, `rung_ray_garage_cold` 1) now clears, and
so do the three that this increment's own new prose produced at 1–2. Zero JS errors.

**One room left.** The shop 654 → **2,950** (+2,296) lands the total at **36,024**: mean 4,503,
median 4,381, anchor 26.7%. That is gate 1 closed.

---

## 2026-08-11 — v0.1 fill 4/6: the box room and the landing, and the rotating slot was never split by lifetime

**What.** `the_box_room` 1,228 → **4,381**, `the_landing` 1,367 → **1,963**. Files:
`games/back_home/toml_phases/3_activities.toml`, `5_scenes.toml`, the game's `v2_state.json`, and
`references/the-board.md` — the finding is about the rotating-slot pattern, not about this game.

### The finding: the slot's economics were designed, its content was not filed to match

The box room is the premise's answer to never-ending — *a new character at an existing location
every few releases* — and the ledger records the intent that replacing the lodger **touches only his
`[[npcs]]` entry and his block in `5_scenes.toml`.**

That only holds if content is filed by **how long it lives**:

| scope | covers | file | survives rotation |
|---|---|---|---|
| **tenant** | his ladder, his register, his props | `5_scenes.toml` | no — dies with him, deliberately |
| **room** | the slot, the mattress, the wall, what the arrangement *is* | `3_activities.toml` | **yes** |

`activity_his_room` was room-scoped **by file** and tenant-scoped **by content**: a specific
submarine thriller, a bus ticket from a named town, a biscuit tin with a named amount in it. Every
one of those is Marek. The first rotation would have cost a rewrite *in the file the plan says it
will not open* — a cost that is free to avoid while writing and annoying afterwards.

**The rule that fixes it: room-scoped content names the occupant by ROLE, never by name.** Now in
`the-board.md` with the table above. The tenant-specific version of the bag moved to
`rung_marek_bag`, where it is supposed to die.

The room-scoped layer also turned out to be the more interesting half, because it is the only place
the slot is legible **as a slot**: the same mattress through four tenants, marks on the wall at three
different headboard heights, a name she has genuinely forgotten, and the fact that the terms get set
in the first fortnight by whoever is standing on the landing when the new one arrives.

### His ladder had a hole in the middle and nothing at the top

It ran *stand in the doorway* (no gate) → *ask what he's paying Ray* (need 15) → **the explicit
loop** (need 35 + exposure 55). Three rungs added, verified live at their gates:

| rung | gate | what it is |
|---|---|---|
| `rung_marek_watch` | need 25 + exposure 35 | the missing middle — he prices *looking*, in the voice he priced the room in |
| `rung_marek_bag` | his relation 45 | **pays the logged promise**: the packed bag, unopened since October. The only scene in his ladder with no transaction in it, which is why it costs him more than the loop does |
| `rung_marek_after` | `marek_arrangement` | Cal and Ray both had a post-arrangement rung; he had none, and his is a 09:00–16:00 empty house with nothing to get back to |

```
cold                    doorway · [LOCKED] tell him what it costs now
need30 exp40            + what he's paying Ray · what else he'd pay for
need60 exp60 rel50      + the bag · the offer · stay after · [LOCKED]
```

Every effect matched its declaration (`rung_marek_watch`: money +20, need +3, exposure +3, pride −3,
his lust +6). Zero JS errors.

### The sweep, again — and it caught the new content too

Seven beats across the two rooms scored 1 or 2 and were lifted: the Marek loop's actual sex beat
(**1 → 6**) and its finish (**1 → 3**), and six landing peep beats. The landing now reads
`3·3·3` / `3·4` / `3·7·4` / `4·4` where it read `3·3·1` / `3·2` / `1·7·1` / `2·2`.

**And the content written this increment did it again** — `rung_marek_watch` came out at 2 on its
middle beat and `triggered_lodger_home` at 2, both caught by the same per-beat pass. That is the
fourth consecutive increment where the defect appeared in *new* prose written immediately after
re-reading the rule. `register.md` is right that it reasserts itself the moment it is not being
actively fought.

### Tally

```
[FAIL] location fill   8 locations · 31,015 words · mean 3,877 · median 4,381 · anchor 31%
       · mean location 3,877 words (need 4,500)
```

Explicit floor **22.4% → 26.3%** of 255 beats; explicit beats 53 → **67**; doors still 7; anchor 31%.

⚠️ **Honest note on the floor.** 26.3% is roughly three times the reference game's measured 7.5–9.3%
band. The floor is a floor and the game is not failing anything — but `register.md` warns that a game
far above it is usually one that has stopped having non-sexual texture. The two rooms left are the
two coldest in the game (the garage, and the shop which is cold by design), so the ratio should come
down on its own. **If it does not, the next increment after v0.1 is texture, not heat.**

**+4,985 remain** — the garage and the shop, and they are the whole of it.

---

## 2026-08-11 — v0.1 fill 3/6: her room, and the backward sweep that was only half done

**What.** `her_room` 1,496 → **3,927 words**, and the median half of gate 1 now **passes**. Files:
`games/back_home/toml_phases/3_activities.toml`, the game's `v2_state.json`, and — because the
finding is about how the register rule gets applied, not about this game — `references/register.md`.

### The measurement that set the increment

The room where privacy structurally fails, containing the only surface in the game she initiates
alone, had **eleven beats and not one of them cleared the 3-word floor**:

| canvas | before | after |
|---|---|---|
| `activity_alone` — the solo sex surface | **1 · 1 · 0** | **7 · 3 · 0 · 0** |
| `activity_the_wall` | **2** | **9** |
| `activity_the_door` | **2** | **5** |
| `activity_get_dressed` | **1** | **3** |

Every one was the pivot: one body word, then off the body for the rest of the beat.

### The doctrine finding — a category name is not a sweep

Phase 1 applied this rule backwards and moved the game 10.8% → 15.9%. It did it to **"the three
repeatable sex loops"** — a *category* — rather than to everything the instrument scored under the
floor. These four canvases were written the day before the rule existed, were never in that
category, and sat under 3 through two further increments **while the headline number rose**.

> Score every beat, sort ascending, fix everything under 3. The instrument already prints per-beat
> scores; there is no reason to select by intuition.

Now in `register.md`, with the corollary that stops the over-correction: **a 0 next to a 4 is the
rule working** — the interiority beat *after* an explicit one is supposed to score 0. What you hunt
is the beat scoring **1 or 2**, which is a beat trying to be explicit and pivoting partway.

The new content proved the point immediately: the three intrusions came out at **2 · 2 · 2 · 0** on
their first pass and had to be lifted before they cleared — written by the same author, in the same
turn, directly after diagnosing it.

### The door had never once been come through

The room's declared thesis is a catch that does not reach the plate — *"the room privacy is supposed
to happen in, and does not"* — and six shipped canvases all had her alone in it with the door as
scenery.

No NPC is scheduled in `her_room`, so `npc_at_location` has nobody to find and `requires_npc` has
nobody to hold. The only pattern that works without a schedule is the bathroom's:
`substitution_only` canvases on the mandatory daily click.

| intrusion | parent | gate | the character in one gesture |
|---|---|---|---|
| `intrusion_cal_room` | `activity_get_dressed` | exposure 25 | knocks on a door that has already swung |
| `intrusion_dean_room` | `activity_get_dressed` | exposure 45 | does not knock, and pushes it to behind him |
| `intrusion_ray_room` | `activity_alone` | exposure 60 | stops in the doorway and says one flat sentence |

Ray's hangs on `activity_alone` **because of that parent's `arousal >= 30` gate** — he only ever
arrives at the worst possible moment, which is the whole difference between him and the other two.
It pays a logged promise outright: *"Ray stopped in the doorway and said nothing… his knowing has to
become content, not stay a stage direction."* Marked `paid_in: 0.1`.

### Two plants paid, one door added

`activity_the_bench` pays the Want's own line — *"her father's weight bench is where the desk was"* —
which had been scenery in six canvases. Three bands: an obstruction, then a thing she has started
using, then the piece of furniture the room is arranged around. And `her_room` had **no locked
rung at all**, so `activity_the_door` became a two-choice surface with *"Take the door off the
hinges"* at nerve 75 — the end of the two-pound-part running line, which until now was a joke with
nothing behind it.

**Verified live:** six standing surfaces render in the room; the door's locked row resolves into a
live choice at nerve 80 and is greyed at 40; every rung applied its declared effects exactly
(Ray: exposure +5, nerve +4, pride −7, his lust +6, relation +3); zero JS errors.

### Tally — gate 1 is down to one sub-check

```
[FAIL] location fill   8 locations · 27,266 words · mean 3,408 · median 3,927 · anchor 35%
       · mean location 3,408 words (need 4,500)
```

**The median check passes for the first time** (3,927 against 3,000) — gate 1 went from three
failing sub-checks to one. Explicit floor **18.1% → 22.4%** of 237 beats, explicit beats 40 → **53**,
locked doors 6 → **7**, anchor 35% and still clear.

⚠️ **Budget rebalance.** Three increments have each landed short of their row (754 + 64 + 573 =
1,391), so the remaining four rooms at their planned targets reach only ~34,600 against the 36,000
the mean needs. The box room goes to **4,700** and the garage to **3,900** to absorb it; that lands
36,016 with the anchor at 26.7% and the median at 4,700. **+8,750 remain.**

---

## 2026-08-11 — v0.1 fill 2/6: the kitchen, and `clamp` had made the rent unpayable

**What.** The kitchen 1,775 → **4,936 words**, and a shipped bug found by the effect diff rather
than by reading anything. Files touched: `games/back_home/toml_phases/3_activities.toml`,
`5_scenes.toml`, the game's `v2_state.json`, and — because the bug is an engine fact the skill never
recorded — `references/engine.md` (new **§21**).

### The bug: every money grant in the game was capped at 100, and the rent is 120

`rung_marek_kitchen_price` declares `money +120`. The live diff said **0 → 100**.

```
v2.py:5753   if (clampFlag === undefined || clampFlag === null) { clampFlag = true; }
v2.py:5754   if (clampFlag) { next = window._traitClamp(next, 0, 100); }
```

`clamp` is a hard **0–100 on every trait**, and it **defaults to true when the key is absent**. All
**ten** money effects in this game carried `clamp = true`. The shop pays 30 a shift and the weekly
rent is 120, so the player could work four shifts, hit the ceiling at 100, and **never once be able
to pay the rent** — the eviction branch was the only reachable outcome of a system the ledger
records as verified end to end.

It is invisible to everything we own: the TOML is valid, the validator passes, the build is green,
all ten gates score the same, and the sidebar shows a plausible number. **Only the live effect diff
against the declared value shows it.** The earlier rent verification missed it because that run set
`money = 200` directly in state and then tested the *deduction*.

Fixed by `clamp = false` on all ten. Verified after rebuild:

| | before | after |
|---|---|---|
| the rent scene, from 0 | 100 | **120** |
| start 12 + four 30-shifts | 100 | **132** |

The rent is payable by working for the first time since `[settings.rent]` shipped.

**Doctrine, new §21:** a trait used as a **quantity** — money, counts — must carry `clamp = false`
on every effect that writes it; meters (nerve, exposure, arousal, energy) want the clamp and keep
it. Would a correct skill have prevented this? Yes — so it is in the engine card, not just the game.

### The kitchen had no triggered layer, in the room named for one

The room is declared *"the crossing point — everyone passes through, nobody stays, so it is where
she is caught in passing"* and shipped three hubs and eight rungs, every one a menu she picks from.
`the-release.md` calls TRIGGERED the main heat engine for a female protagonist, and the room named
for it had none of it.

`triggered_caught_in_passing` is that layer: gated on the **any-NPC** form of `npc_at_location` plus
`worn_corruption >= 4`, so **the wardrobe is what makes it fire** — what she carried downstairs
decides whether the room turns. It binds no NPC, which is both the content (she does not get to pick
who comes through) and the structural guarantee that nothing in it can be mis-attributed.

Verified live: with `sleep_vest` (corruption 2) the surface is absent; with `mothers_slip` (7) it
appears, `getWornCorruption()` reading 7. Its menu steps exposure 10 → 40 → 80, and the locked door
resolves into a live choice at 80 rather than merely un-greying.

Distinct from `triggered_crossing_the_room` on purpose: that one is her crossing into a room one of
them is sitting in; this is the opposite, and it is what *crossing point* means — she is already
here, the kitchen has two doors, and the whole house comes through it one at a time.

### One rung on each ladder, each written to that character's own ceiling

Cal topped out at exposure 15, Dean at 35, Marek at need 25, while the meters band at 55 and 75.

| rung | gate | verified |
|---|---|---|
| `rung_cal_kitchen_late` | nerve 45 + his lust 20 | appears at 45, absent at 20 |
| `rung_dean_kitchen_counter` | exposure 55 + his lust 30 | appears at 55, absent at 40 — fills the band the meter-ceiling gate names |
| `rung_marek_kitchen_price` | need 55 | appears at 55, absent at 30 |

Every effect matched its declaration (Dean: exposure +6, nerve +3, pride −5, his lust +10,
relation +3). Zero JS errors. Also banded the two thinnest rungs in the game —
`rung_cal_breakfast` (120w) and `rung_marek_eat` (146w), each its ladder's always-available presence
floor and each one flat paragraph — and gave the room a solo surface, `activity_kitchen_night`
(23:00–03:00, banded on `need`, deliberately **not** explicit).

**The door belongs to the room, not to a man.** Checking first changed the plan: Cal already owns
nerve 75, Ray need 75, Dean exposure 75 and Marek need 75 elsewhere, so three of the four obvious
choices would have been the same promise twice — and one of them was a ledger promise already made.
*"Stop getting dressed to come down."* hangs on the NPC-less surface instead.

### Two more harness facts

There are **two** per-day ledgers, and clearing one is not enough:
`game_state.trigger_history` keyed by canvas id (`v2.py:4187`) and
`game_state.activity_trigger_history` keyed by canvas **name** (`v2.py:4223`, used when the canvas is
offered as a location action). With only the first cleared, the second probe of a once-per-day
surface reads exactly like a gate that does not work. Also: an NPC-bound hub renders under the
**NPC's** name, not the canvas name — `hub_cal_kitchen` ("Cal (breakfast)") appears as *Cal*.

### Tally

**9/10 holds.** Fill 21,674 → **24,835**. Explicit floor **17.7% → 18.1%** of 221 beats — fourth
increment running that raised it. Explicit beats 35 → 40. Locked doors 5 → 6. Anchor **44% → 39%**,
still clear of 25% and still inside the 36,000–38,400 landing window.

Kitchen came in **64 short** of its 5,000 row; with the bathroom's 754 that is 818 carried.
**+11,172 words remain** across her room, the box room, the garage, the shop and the landing.

---

## 2026-08-11 — v0.1 fill 1/6: the bathroom gets the three quarters of its job it never shipped

**What.** The bathroom 1,954 → **4,746 words** and the room's declared job finally built. Files
touched: `games/back_home/toml_phases/3_activities.toml` (the contention hub plus six triggerless
rungs), `5_scenes.toml` (one rename), and the game's `v2_state.json`. Nothing in the skill's doctrine
changed — this is the first of six fill increments closing gate 1.

### The room was declared for four things and shipped one

`v2_state.json` describes `the_bathroom` as *"the occupancy engine — contention, waiting, walking
in, being walked in on."* What existed was four walk-in substitutions — **being walked in on** — and
a 57-word `bath_occupied` that said the room was busy and sent her back to the landing. Contention,
waiting and walking in had no content at all. The room was named for a machine and shipped the one
part where she does nothing.

`bath_occupied` is now the contention hub: a nerve-banded opener (15/35/55) and a menu. Six rungs
hang off it — wait, knock, walk in on Cal, on Dean, on Ray, and get in with him.

### The hour picks the man; she only picks whether the door opens

The three walk-in choices are gated on `npc_at_location(the_bathroom, npc_X, is_present)` and
nothing else identifies them, so the ladder is the morning queue: Ray 06:30, Cal 07:00, Dean 07:40.
Same click, three different men, three different registers off the Want's per-character ceiling —
Cal borrowing words badly, Dean crude *to* her, Ray one flat sentence that costs more than anything
Dean says all week.

**Verified live, which is the only way this could be checked** — a choice condition is evaluated at
render, so it cannot be read out of the TOML:

| clock | occupant | menu |
|---|---|---|
| Mon 06:45 | `npc_ray` | wait · knock · **walk in on Ray** · locked door |
| Mon 07:20 | `npc_cal` | wait · knock · **walk in on Cal** · locked door |
| Mon 07:50 | `npc_dean` | wait · knock · **walk in on Dean** · **get in with him** · locked door |
| Mon 08:30 | — | hub does not fire |

At `nerve` 0 the menu is *wait* and the locked door only; Cal's rung appears at 25, Dean's at 35,
Ray's at 40, and the shared shower at 55/55. Every rung applied its declared effects exactly
(Cal: nerve +4, exposure +3, pride −3, arousal +25, his lust +8, relation +3). Zero JS errors.

### Two harness facts, both of which faked a broken game

1. **The clock is `game_state.time_state`** — `current_day` as a day *name*, plus `current_hour`
   and `current_minute` (`v2.py:3272-3276`). Setting `game_state.day` / `.hour` writes a field
   nothing reads: every schedule then evaluates as unoccupied and the whole game looks dead. The
   first run of this increment's harness reported an empty presence grid at all five times.
2. **Stop clicking when the passage leaves the canvas.** Advancing blindly to the end of a cascade
   walks on through the exit into the location page and back into the hub, applying a second scene's
   effects. That read as Cal's rung granting +8 nerve against a declared +4 — a doubling that looks
   exactly like an engine bug and is the harness.

Both are the same lesson the Player agent's spec already owed: this is the second increment running
where the only defects found were in the test harness, not the game.

### The lint's one actionable hit, paid

`shift_change_frontroom` → **`rung_dean_shift_change`**, per house convention that a rung's id names
its speaker. Two occurrences, both in `5_scenes.toml`; verified live that the renamed canvas is still
reachable from `hub_dean_late` and still applies its effects. The dialogue-attribution lint drops
**3 → 2**, and the two that remain are `canvas_arrival`, the known-good opening where Ray and Dean
both speak.

### Tally

**9/10 holds.** Fill 18,882 → **21,674**. Explicit floor **15.9% → 17.7%** of 198 beats — the third
consecutive increment where new explicit content *raised* the floor rather than diluting it, which
is `register.md` continuing to hold. Explicit beats 28 → 35, all re-enterable. Locked doors 4 → 5.

⚠️ **The anchor fell 51% → 44% without losing a word**, exactly as `the-board.md:59` says a ratio
gate does. It has room — 25% of the 36,000-word target is 9,000 and it sits at 9,607 — but the
budget only works if the finished total lands in **36,000–38,400**. Above that the front room needs
another instalment.

The room came in **754 short of its 5,500 budget row** and that debt carries rather than being
quietly written off: **+14,333 words remain** across the kitchen, her room, the box room, the
garage, the shop and the landing.

---

## 2026-08-11 — `STATUS.md`: the status doc moves into the skill, and was wrong in four places

**What.** New file `STATUS.md`, moved from `~/.claude/plans/continue-nested-acorn.md` and refreshed
against a live scoreboard run. The plan file is removed; this is now its only home. Nothing else in
the skill changed.

**Why move it.** Plan files live outside the repo and are not git-tracked, so the single most useful
document in the project — the one that catches a reader up on why v2 exists, what the ten gates
measure, and where the test game stands — had no history and could not travel with the skill. It now
sits beside the `CHANGELOG.md` it summarises.

**Why it needed refreshing.** Every number in it was written before Phase 1 and the lint landed. Four
sections had drifted:

| section | said | actually |
|---|---|---|
| Part 3 — file inventory | `gates.py` 524, `engine.md` 403, `CHANGELOG` 792, `SKILL.md` 107 | **605 / 468 / 923 / 111** |
| Part 4 — engine facts | "Eighteen engine facts" | **twenty** (§19 canvas-shadowing, §20 `npc_at_location`) |
| Part 5 — the game | 62 canvases, 14,398 words, 10.8% of 148 beats, mean 1,800 | **66 · 18,882 · 15.9% of 176 · mean 2,360** |
| Part 6 — not done | the lint "worth adding" | **shipped** |

**The one that mattered.** Part 5 said the anchor had fallen to **34%** and was the next thing to
write. Phase 1 had already taken it to **51%**. A reader following that document would have written
the one room that no longer needed it. The satellites are the work — seven of them, ~17,000 words,
listed thinnest-first in the new Part 5.

**Guard added.** The document now opens with a `Last verified` stamp and the two commands that
regenerate its numbers, plus the rule that the scoreboard wins any disagreement. This file went stale
inside a day; a status doc that cannot be checked against a command will do it again.

**Verified.** Numbers taken from `python3 scripts/gates.py back_home` (9/10, location fill the only
failure) and `… vesper` (1/10) run immediately before writing; counts from
`grep -c '^\[\[canvases\]\]'` and `wc -l` on the live files.

---

## 2026-08-11 — `scripts/gates.py`: the dialogue-attribution lint, specced 2026-08-10, now real

**What.** `lint_dialogue_attribution()` plus a `_dialog_blocks()` walker in
`scripts/gates.py`, reported below the tally and **never scored**. A warning that can move a
gate is a gate, and a gate has to be re-derivable from a measurement.

Flags any `dialog` block whose `npcId` names a character the canvas neither **binds**
(`npc` / `requires_npc`) nor **names in its id**. It walks into cascades and groups, so it sees
the dialogue that only exists three levels down inside a `beats` array.

**Results, measured:**

| game | hits |
|---|---|
| `back_home` | **3** |
| `vesper` | **28** |

**The spec said 2, and 2 was right when it was written.** Of today's three: two are
`canvas_arrival`, the known-good opening where Ray and Dean both speak — exactly the pair the
original measurement found. The third is `shift_change_frontroom`, which **this project
introduced yesterday** in the Phase-1 anchor increment. It renders correctly (verified live —
only `Dean` appears), but it is a triggerless rung whose id does not name its speaker, so it is
precisely the shape the lint exists to surface. The house convention would call it
`rung_dean_shift_change`; that rename is the cheap fix and is left for the next pass rather than
smuggled into a tooling commit.

**One hit per canvas + speaker, not per line.** The first cut counted blocks and returned 7 on
`back_home` and 200+ on `vesper` — unusable. A canvas that renders the wrong name renders it
wrong on *every* line it speaks, so a per-line count measures how talkative a scene is rather
than how many defects exist. The per-canvas count is the defect count; `lines` is carried in the
JSON for anyone who wants the volume.

**Vesper's 28 are not noise.** They cluster on `cell_*` canvases speaking as `npc_bastien` —
the same character the standing-surface gate already fails it for: referenced everywhere,
findable nowhere. Two independent checks landing on one character is the useful kind of
agreement.

`--json` output is now `{"gates": [...], "lints": {...}}` rather than a bare gate array.
**Anything parsing the old top-level list needs updating.**

**Verified.** `back_home` still reports 9/10 and `vesper` its existing score — the lint changed
no gate, which is the property that matters most about it.

---

## 2026-08-11 — v0.1 Phase 1: the anchor, 5,123 → 9,607, and three engine facts it cost

**What.** The front room taken from 5,123 words to 9,607 in one pass — the anchor budgeted
against the *finished* 36,000-word total (where it owes ~9,000) rather than the current one,
because the ratio tightens every time any other room grows and topping it up later means
writing it twice. Files touched: `games/back_home/toml_phases/5_scenes.toml` and
`3_activities.toml`, plus `references/engine.md`, `SKILL.md` and the game's `v2_state.json`.

Gate 1 still fails, as expected and as planned — mean 2,360 against 4,500, median 1,496 against
3,000. It closes when the seven satellites are filled. What this bought is the right to fill
them without the anchor sliding under 25% on the way.

### The register rule was written from this game's own failures and never applied to it

`references/register.md` quotes, as pivot target #3, the sentence *"…and the arithmetic does not
come out the way it is supposed to."* That sentence was still sitting at the end of
`loop_ray_arrangement`, and the beat carrying it scored **zero**. Measured per beat, all three
repeatable sex loops failed the same way in the same place — their *tails*:

| | beat 1 | beat 2 | beat 3 | beat 4 |
|---|---|---|---|---|
| `loop_ray_arrangement` | 4 | 1 | **0** | 0 |
| `loop_dean_late` | 3 | 1 | **0** | **0** |
| `loop_cal_sex` | 4 | 3 | **0** | 0 |

Every loop opened explicit and then left the body exactly when the act got closest. The fix was
the one the doctrine already prescribes — keep the camera on the body to the last sentence, and
give the interiority its own beat *after* — and it moved the whole game **10.8% → 15.9%** of
beats at 3+ explicit words, without one gratuitous noun.

**Two words worth knowing are NOT on the frozen list:** `wet` and `come` (the latter excluded
deliberately, since it matches "come downstairs"). Three finishing beats rewritten to be
relentlessly physical still scored 2, because they leaned on both. The list is the instrument;
write to the body and check the number.

### Three engine facts, each caught by a build that refused to run

1. **The documented build command was wrong** — in `SKILL.md` *and* `references/engine.md`.
   `package_from_toml` takes named, required `--file` and `--output`; the positional-plus-
   `--output-dir` form both files carried exits 2 and builds nothing. `python` may not be on the
   path either. Both files corrected. A skill that cannot build the game it authored is a broken
   skill, and this had been shipped since the first release.
2. **Move a flag setter — never duplicate it.** `cal_arrangement` was set on the located hub
   choice *and* left on the triggerless loop. The validator resolved it to the one without a
   location and hard-failed with `MISSING HINT`, naming the loop's canvas name (`Take him
   upstairs`), which reads exactly like the hub choice of the same wording. §16 sharpened.
3. **One repeatable canvas per location + NPC + time window.** The two-men scene was written as
   a located canvas and the build warned that `hub_dean_late` already owned `npc_dean` at the
   front room. It is a *warning*, not an error — a canvas shadowed this way looks correct in
   TOML and is unreachable in play. New §19; treat the warning as an error.

### `npc_at_location` promoted from "known" to "verified live" (new §20)

`generators/v2.py:4131-4145` and `:7791`. **`npc_id` is optional — omit it and the predicate
tests whether the room is occupied by anybody.** Confirmed in the built game rather than read:
the two-men choice rendered at 23:10, where Ray's 20:00–23:30 row overlaps Dean's 23:00–01:30,
and was gone at 23:45 with identical player state.

That single fact carried the increment's two new content kinds. Conditions on a *choice* are
evaluated live at render, so the scene the engine refused as a canvas works better as a rung on
the existing hub. And the any-NPC form let the TRIGGERED piece — she crosses the room in what
she sleeps in and does not look to see which of them is in the chair — bind **no NPC at all**,
which is both the content and a structural guarantee that no dialogue can be mis-attributed.

### Live-testing this engine, for whoever writes the next harness

Static parsing cannot see a passage that errors. Three things about the built game are not what
a reasonable person would guess, and each cost a run:

- `State` and `Engine` are **not** bare globals. Use `SugarCube.State`, `SugarCube.Engine`,
  `SugarCube.setup`.
- `$flags` is an **object** keyed by flag name, not an array. `.includes` throws.
- Player traits live at `player.core_traits`, not `player.traits`.

All fourteen new or rewritten passages then rendered clean: no JS errors, every cascade
advancing, and no speaker outside the four declared characters.

**9/10 holds.** Nothing else moved: explicit-in-repeatable 100%, standing surface 4/4,
milestones 4/4, meter ceiling clean, four locked doors still shut. Three new promises logged
(Dean's uncharged version, Ray's knowing, Cal's £840). The stray `Wren-solo` labels — Vesper's
protagonist used as a pattern name in a game about June — are gone.

**+17,100 remain**, all of it in the seven satellites.

---

## 2026-08-10 — v0.1 increment 2e-4: the box room and the shop, and a bug in my own prose

**What.** Box room 908 → 1,228, shop 76 → 654. Two new promises logged.

### The bug, and the structural reason behind it

Hannah Beckett — a woman June sat next to for two years, walking into the shop — was written as
a `dialog` block attributed to **`npcId = "npc_marek"`**, because she is a walk-on with no NPC
record. It would have rendered **"Marek:"** over her line in the built game.

Fixed by making it quoted prose. But the interesting part is *why it can't be fixed the obvious
way*: declaring Hannah as an `[[npcs]]` entry would immediately **break gate 6**, which requires
every declared character to have a standing surface and a schedule row.

**The gate is right.** A character with a name and no way to find them is exactly the defect it
exists to catch — Vesper's `npc_bastien`, referenced 88 times and reachable nowhere. So
**one-scene characters are narrated, never declared.** That is a real constraint the gate
imposes on authoring, and it is a good one.

### A lint worth adding to `gates.py`

> Flag any `dialog` block whose `npcId` names a character the canvas neither **binds**
> (`npc` / `requires_npc`) nor **names in its id**.

Run over `back_home` it returns exactly **2** hits — both `canvas_arrival`, which legitimately
has Ray and Dean speaking in the opening — and it **would have caught the Hannah bug**.

The naive version (flag dialogue on any unbound canvas) returns **30 false positives**, because
every triggerless rung is unbound by design and correctly carries its own character's voice.
Worth noting how much narrower the useful check is than the obvious one.

### The shop is the mirror

The regulars are banded on `pride`, so the same six hours read as humiliation, then as rest,
then as camouflage. And `canvas_someone_who_knew` is the reversal made visible **from outside the
house** — the only vantage it can be seen from. From out there the story is short and finished:
*June went, June came back, June is at the shop.* The house is the only part still moving.

**9/10 held.** Fill 12,496 → 13,394. Explicit floor 10.1% → **9.6%**, an expected dip: this was
deliberately the least explicit increment in the game, because the shop is the one room where no
man wants anything from her and that is its entire function. Still comfortably above 7.5%.

⚠️ **Anchor at 34% and drifting down** — the trap from last increment is live. The front room
needs its next instalment before much more is written elsewhere.

**+22,606 remain.**

---

## 2026-08-10 — v0.1 increment 2e-3b: the anchor trap, and the last empty schedule row

**What.** The garage (309 → 801) and an anchor instalment on the front room (4,020 → 4,556).
Added the fill-in-step rule to `references/the-board.md` and corrected §16 of
`references/engine.md`.

### The anchor trap — a ratio gate tightens while you work elsewhere

Gate 1 wants the anchor at **≥25% of all location prose**. That is a ratio, so every word written
anywhere else lowers it. The front room sat at 4,020 through six increments of building other
rooms, and its share fell **53% → 46% → 40% → 39% → 35%** without a single word being removed.

Held there, it crosses below 25% **within one more increment** — the game going 9/10 → 8/10
while getting objectively better.

**Budget the anchor against the finished total, not the current one.** At a 36,000-word target
the anchor owes 9,000, so its share is planned into every increment rather than topped up at the
end. Now doctrine in `the-board.md`.

### The flag-chain rule was recorded too narrowly

Hit it a second time with `ray_arrangement`:

```
✗ ray_arrangement   required by choice 'Sit with him after.',
                    set by 'Stop pretending it's a favour' but no location/schedule
```

The validator refuses a flag set in a triggerless rung when it is read by a **choice**, not only
by a trigger. Same fix both times — move the `flagEffects` up onto the located hub choice.
`engine.md` §16 now reads "a TRIGGER **or a CHOICE**".

### The last empty schedule row is filled

Dean was present in the garage 14:00–17:00 at weekends with **zero content** — the only scheduled
row in the game with nothing on it. Verified live at Saturday 15:00. He now carries three
surfaces. The scene is the one version of him with no audience: *he cannot do the funny voice
under a bar*, so between the fourth and fifth rep he is straightforward for the first time since
they were children.

### Scope honesty

The plan named three targets and this increment hit two. **The box room was not touched** and
remains at 908; it carries into the next increment rather than being quietly dropped.

**9/10 held.** Fill 11,468 → 12,496; anchor back to **36%**; explicit floor **10.0% → 10.1%** —
the second consecutive increment where new content raised it rather than diluting it, which is
`register.md` continuing to hold. **+23,504 remain.**

---

## 2026-08-10 — `references/register.md`, and the first increment that RAISED the explicit floor

**What.** Wrote the skill's missing prose doctrine, then authored the kitchen against it. Kitchen
698 → 1,775. Linked from `SKILL.md`'s operating rules.

### The gap

Checking why the same defect had recurred three times explained it: **the skill said *where* the
crude register lives and *which words* were permitted, and nothing at all about how to write the
beat.** There was no prose reference. The Want template's §6 is entirely placement and vocabulary
ceilings.

### The rule, and its test

> **An explicit beat stays on the body for its whole length.**
> **Diagnostic:** if the beat's last sentence is about what it *means* rather than what is
> *happening*, it has pivoted and will score 0–1.

`register.md` names the three pivot targets — *he knows* / *she is ashamed* / *what this says
about her* — so they are catchable while writing, and puts the interiority in **its own beat,
after**. Cascade beats are free, so splitting costs nothing and sacrifices none of the
psychology, which is the part that makes the game good.

It also states what the fix is **not**: not word-stuffing, and not loosening the frozen wordlist.
The list has been challenged twice and was right both times.

**The test:** doctrine written first, kitchen authored against it, gate run after.

| | before | after |
|---|---|---|
| beats | 106 | **120** (+14) |
| explicit beats | 10 | **12** |
| explicit floor | 9.4% | **10.0% — up** |

**For four consecutive increments new content dropped the floor and had to be rewritten after the
gate caught it. This time it went up, on the doctrine's first use.** That is the strongest
evidence in this project that a written rule can actually change what gets authored — but only
once the rule says *how*, not merely *where*.

### The kitchen

Four surfaces against the schedule already built: Cal 07:40–08:00 (twenty minutes, cannot look at
her, and the mugs are on the shelf above his head), Dean 08:00–09:00 (down from the bathroom she
watched him in — the entire scene is the not-mentioning), Marek 16:00–17:30 (the only hour the
two of them are the only adults in the house, and the only meal anybody eats sitting down). Marek
and Cal now carry two surfaces each.

**9/10 held.** Fill 10,391 → 11,468; median 1,367 → 1,496. **+24,532 remain.**

---

## 2026-08-10 — v0.1 increment 2e-2: the morning queue, and the register defect is *mine*

**What.** Dean given a bathroom row; two new peeps; two new walk-ins; the wall paid off. Bathroom
845 → 1,517, landing 681 → 1,367.

### The finding that matters more than the content

The new scenes added **sixteen beats and zero explicit ones.** Every one scored 0 or 1 against
the 3-word floor, dropping the game to exactly **7.5%** — the boundary.

The pattern is identical every time: **name a body part once, then pivot the next beat to
psychology** — he knows, her face is burning, what it means. The heat sits in the situation and
never in the words.

This is the defect diagnosed in Vesper, reproduced by the author who wrote the doctrine against
it, **for the third time — twice after writing it.** That is the actual finding:

> **It is not a lapse. It is a default that reasserts itself the moment it is not being actively
> fought, and the gate is the only thing that catches it.**

**The fix is not word-stuffing.** It is to stay on the body *through* the beat rather than
referencing it once and moving on. Eleven targeted rewrites took the floor **7.5% → 9.4%**,
which sits at the *top* of the reference game's measured 7.5–9.3% band rather than scraping it.

### The morning queue

Dean had **no bathroom row at all**, so he could neither be peeped nor walk in on anything.
Adding 07:40–08:00 weekdays makes the grid step cleanly — verified live:

```
06:45  ['npc_ray']    07:20  ['npc_cal']    07:50  ['npc_dean']    08:30  []
```

Three men through one bathroom in ninety minutes. Each of the four peeps is offered only while
its own man is in its own room, including Marek's box-room peep — which needed no new schedule
row, because his door was already established as half open.

### Planted facts, paid

All three night-one details now carry content: the gap down the hinge side (four peeps), the
extractor that makes her deaf (three walk-ins on `activity_wash`'s substitutions at rising
`exposure`), and the eighteen-inch wall (`activity_the_wall`, banded on `nerve` — at the bottom
she is trying not to hear it, at the top she is timing herself to it).

### Tally

**9/10 held.** Fill 8,752 → 10,391; median 845 → 1,367. **+25,609 remain.**

Play-test friction now stands at **four false alarms from page-text assertions and zero real
bugs found by them** — this time a filter that searched for "gap" and "forty" against a canvas
named *"Cal takes his time."* Every real defect this session came from asserting on
`SugarCube.State.variables`. The Player agent's spec should forbid text assertions outright.

---

## 2026-08-10 — v0.1 increment 2e (part 1): the wardrobe, and a silent-failure class

**What.** A 9-item `[[clothing]]` catalog, and her room built out from 68 words — the boxes,
the dressing scene, the door that does not shut, and the solo surface. Added §17 to
`references/engine.md`.

**The most dangerous failure class this project has hit.** To grant the two garments I wrote:

```toml
clothingEffects = [ { itemId = "mothers_slip", op = "grant" } ]
```

The TOML parsed. The validator passed. **The build went green and nothing was ever granted** —
the top tier of the wardrobe would have been permanently unreachable, with no error anywhere in
the pipeline. The real key is `wardrobeEffects = [{ action = "add", item_id = "…" }]` on
`exit_block.config`.

**Nothing catches an invented key.** Not the parser, not the validator, not the build, not the
gates. The only defence is to grep `template_import.py` for any key not personally seen in a
shipped game — zero hits means it does not exist, however plausible it looks. That rule is now
in the engine card.

**The wardrobe is real, not decorative** — the plan's decisive check, and it passes. Verified
live: seven initial garments equip at start; the boxes grant `mothers_sundress` and
`mothers_slip`; equipping the slip moved **`worn_corruption` 2 → 7**; and the dressing scene
rendered its tier-3 band in response.

`worn_corruption` is a **MAX aggregate, not a sum** — one loaded garment sets the reading on its
own. So a catalog does not need to be large to reach a tier; it needs one item per tier. That
makes clothing a genuine gate source for `exposure` rather than a UI ornament.

**Her room** went 68 → 1,215 words, and its four surfaces are all *standing* — which is where
the crude register belongs. The room's thesis is the broken catch: the same action reads as
three different decisions as `exposure` climbs, ending at *"It is a two-pound part. You know
exactly where the hardware shop is."*

**Gates: 9/10 held.** Fill 7,605 → 8,752. Explicit floor 8.9% across 90 beats — still clear as
the denominator grows. **+27,248 words remain** for the last gate.

---

## 2026-08-10 — v0.1 increment 2d: Marek. **9 of 10 gates pass**

**What.** Marek's hub and three rungs added to `5_scenes.toml`. Six open promises logged in
`v2_state.json`.

**The rotating slot is proven.** He is the premise's structural answer to never-ending: Ray
rents the box room to cover the shortfall, so every few releases a new stranger lives in the
house — **a new character at an existing location**, which is the measured release shape built
into the fiction rather than bolted onto it. Replacing him next release should touch only his
`[[npcs]]` entry and his block in `5_scenes.toml`, and nothing about the world.

His window is deliberate: **09:00–16:00, when the house is empty.** The one slot no family
member competes for, and the reason his ladder needs no privacy management at all. He also
carries the only register in the game that is transactional from the first line — no build, no
history, no ceiling to break — which is what makes him legible against three men she is
related to.

**Verified live.** Present in the box room at Tuesday 11:00; all three rungs render with the
fourth locked; the explicit rung applied money 0→50, need 40→45, exposure 60→64, pride 100→94,
his lust 0→8, `marek_arrangement` set. Zero JS errors.

**Gates: 9/10.**

| | |
|---|---|
| standing surface | **4/4** — every character findable and scheduled |
| traversal heat | **5/8 (62%)** — over the 60% floor |
| meter ceiling | clear — every band boundary now buys something |
| ends on an opening | **4** locked rungs |
| ascent tiers | all three gated — nerve 4+, exposure 6+, need 7+ |
| explicit floor | 9.9% across 81 beats |

**The one remaining failure is location fill** — 7,605 words against ~34,000, median 698
against 3,000, mean 951 against 4,500. No location is empty any more; this is not a design
problem, it is the writing a first release costs.

**Six promises logged.** Marek leaving in spring (the slot must be *refilled*, not left empty),
the `keep_unpaid` line *"we'll sort it another way"*, and the four locked 75-rungs. Each is now
tracked and must be paid or explicitly cut — the measured failure mode is a character dangled
for years while players ask *"are we EVER going to…"*.

---

## 2026-08-10 — v0.1 increment 2c: Dean. 6/10 → 7/10, and a build-breaking engine rule

**What.** Dean's two hubs and five rungs added to `5_scenes.toml` — the kitchen at 08:00 (verbal,
daylight) and the front room at 23:00–01:30 (dark, physical). Same man, two registers. Added §16
to `references/engine.md`.

**An engine rule that hard-fails the build, learned by hitting it.**

```
❌ Flag Chain Validation Failed:
   ✗ dean_open
     Required by: Dean (late)
     Issue: MISSING HINT - set by 'Come down in what you slept in' but no location/schedule
```

**A flag read by a TRIGGER must be set from a canvas that has a location.** A triggerless rung
has none, so the game cannot tell the player where to go and earn it. The fix is to move the
`flagEffects` onto the **hub choice** that opens the rung — the choice lives on a located
canvas, the semantics are identical, and the chain resolves. Flags that nothing reads in a
trigger are unaffected.

This is the fourth build-breaking convention found by authoring rather than by reading, after
the section-syntax requirement, the positive-decay rule and the children-only navigation order.

**Verified live on both surfaces.** Kitchen hub appears at Monday 08:30. Front-room hub appears
at Monday 00:30 with `getNpcsAtLocation('the_front_room')` returning `['npc_dean']` — **the
overnight-wrap row holds in live presence, not just in a schedule dump.** That is the first
end-to-end proof of the midnight-wrap finding; until now it had only been read out of the
source and seen in a schedule listing. The late loop applied dean lust 30→38, relation 0→3,
player exposure 40→45, nerve 0→4, pride 100→96. Zero JS errors.

**`meter ceiling` now PASSES.** Exposure gates at 15 (Ray's garage), 35 (Dean's kitchen morning)
and 75 (Dean's locked late rung) fill the bands the gate had been naming as empty promises.
Marek takes 55.

**Gates: 7/10.** Three fails left, and they are three views of one thing — Marek is unbuilt
(standing surface 3/4), his box room is the last empty location (traversal heat 4/8), and
location fill is at 6,697 of ~34,000. Explicit floor holds at 9.9% across 71 beats even as the
denominator triples, which is the floor doing its job rather than drifting.

---

## 2026-08-10 — v0.1 increment 2b: Ray, and the keep. The `need` tier gets an engine

**What.** Added `[settings.rent]` to `0_systems_spec.toml` and Ray's two hubs plus five rungs to
`5_scenes.toml`. Corrected the meter-ceiling gate in `scripts/gates.py`.

**The `need` tier had no engine, and the platform already ships one.** She could earn at the
shop but nothing ever demanded money, so "what she'll trade for" had nothing to bite on.
`[settings.rent]` (`apps/projects/services/template_import.py:2564-2573`) is a first-class
recurring demand with `amount`, `due_day`, `collector_npc`, `grace_periods` and an eviction
mode. It is also **exactly the mechanic the reference game's seed uses** — its `loc-home` file
carries authored `Rent Intro` / `Rent Pay` / `Rent Refuse` / `Rent Fight` passages.

Tuned to bite: **120/week against a shop paying 30/shift** is four shifts — most of her week,
survivable, and one bad week forces the ask. Ray collects, which makes the demand a father
invoicing his stepdaughter, and neither of them has anywhere to put that.

**`eviction_mode = "flag_set"`, not the default `"game_end"`.** A product that never ends must
not ship a lose-state that stops play. **Verified live, end to end:**

| | result |
|---|---|
| pay | money 200 → 80, exactly 120 deducted |
| first miss | `warnings` 0 → 1, grace consumed, authored warning prose |
| second miss | `keep_unpaid` set, soft-eviction prose, **game continues** — still playable, back at `Location_her_room` |

The engine's own fallback line for this mode is *"You're still here. But the terms have
changed."* Zero JS errors.

**Gate corrected — meter ceiling.** Once top bands were correctly left unbounded, the old check
read the *second* band's `max` as the ceiling and produced nonsense ("exposure shown up to 74").
The truer semantic: **every band boundary is a promise** — a meter showing 15/35/55/75 tells the
player something is different at each. The gate now compares the highest authored gate against
the **top band's `min`** and names the empty bands:

> `exposure: bands promise something at 35/55/75, but the highest authored gate is 15`

Vesper unchanged at 1/10 (its `hygiene` finding now reads more clearly for the same reason).

**Gates: 6/10.** `ascent tiers expand the world` now **passes** — all three declared tiers have
gated content for the first time (`nerve` 4+, `exposure` 1+, `need` 4+), which was the design
gap Ray existed to close. `ends on an opening` is up to 2 locked rungs. Remaining: location fill
(5,436 of ~34,000), traversal heat 3/8, standing surface 2/4, and the exposure bands above —
all of which Dean and Marek carry.

**Authorial note recorded rather than ruled on.** Ray's top rung **omits** `locked_text`, so the
greyed row shows the action — *"Ask him for it in front of the others"* — a want the player can
name. Cal's shows the reason instead. Both are in the build deliberately; compare them and pick
one house style before ship.

---

## 2026-08-10 — v0.1 increment 2a: Cal's ladder. 4/8 → 6/10 gates, all ten now judged

**What.** Authored `games/back_home/toml_phases/5_scenes.toml` — the first standing hub and its
full rung ladder (talk → let him look → contact → the explicit loop → a locked top rung).
Merged, built, live-played. Added §13–§15 to `references/engine.md`.

**Cal's ladder verified live.** The hub appears at `the_front_room` only inside his 16:00–19:30
weekday rows (`requires_npc` doing the presence work, no hub schedule needed). At `nerve` 60 /
his `lust` 35 all four rungs render, and clicking *Sit closer* moved **cal lust 35→41,
relation 0→2, player nerve 60→63, exposure 0→2, pride 100→98** — exactly the declared effects,
zero JS errors. The fifth rung rendered as `SPAN.locked-choice`, so gate 9 is real and the
release has a visible door.

**Three engine facts learned, all by breaking something.**

1. **Exit blocks must use SECTION syntax** — `[canvases.nodes.exit_block]` plus
   `[[canvases.nodes.exit_block.choices]]`. A multi-line inline table is a TOML parse error and
   a conditional choice list is unavoidably multi-line. The shipped game does this 199 times; I
   wrote it inline and the merge failed. `conditions = { … items = [ … ] }` *may* span lines
   because newlines are legal inside an array — two levels of nesting is where it breaks.
2. **Third instance of the key-asymmetry trap.** Conditions say `trait_key` / `npc_id`; effects
   say `trait` / `npcId`. Same concept, different key, silent when wrong.
3. **`locked_text` REPLACES the action label**, it does not annotate it. Recorded as an
   authorial trade-off rather than a rule: showing the action names a *want* the player can
   chase, which is what sells the next release; showing the reason is clearer about the gate but
   weaker as a door.

**The meter-ceiling gate caught a real lie.** `nerve` displayed a 75–100 top band while the
highest authored gate was 75 — the top 25 points bought nothing and the sidebar was promising
content that did not exist. Fixed by making the top band **unbounded** (`min = 75`, no `max`) on
all three tiers, which is honest and which the gate correctly skips as promising nothing.

**Gates: 6/10, and no gate is n/a any more** — every one now has something to judge. Passing:
explicit floor 13.2%, explicit in repeatable 100%, media pools, milestones, meter ceiling, ends
on an opening. Remaining four are all unbuilt work: location fill (3,795 of ~34,000 words),
traversal heat 2/8, standing surface 1/4, and `exposure` / `need` have no gated content yet
because Cal's ladder gates only on `nerve`. Ray carries `need`, Dean and Marek carry `exposure`.

**Anchor discipline held without intervention** — `the_front_room` is back to 56% once Cal's
2,125 words landed, against a 25% floor.

---

## 2026-08-10 — v0.1 increment 1: the daily loop and the bathroom. 0/4 → 4/8 gates

**What.** Authored `games/back_home/toml_phases/3_activities.toml` — the solo loop (sleep, wash,
shift, and a pass-time evening) plus the bathroom's triggered layer (occupancy, two peeps, a
walk-in). Merged, built, and live-played the lot.

**Doctrine finding — the build order flips, and this belongs in `references/the-release.md`.**
Gate 2 wants ≥7.5% of beats explicit, but `nerve` / `exposure` / `need` all start at **0**. A
standing seduction ladder at tier 0 is absurd. The reference game resolves this the same way:
its early heat is not chosen by the player at all — her promiscuity sits at zero while the world
still acts on her.

> **The TRIGGERED layer carries the explicit floor while every tier is still cold. The STANDING
> ladder stays cold until she has climbed it.** So the triggered layer is built *first*, not
> third.

**The gate caught the author.** The first draft of the peep and walk-in scenes scored **0.0%**
on the explicit floor *despite being explicit content*, because the prose named the act
obliquely — "hard", "comes", "finishes" — instead of naming bodies. That is precisely the defect
diagnosed in the previous game, reproduced by me, one increment after writing the doctrine
against it.

Rewriting seven beats in a crude register moved the floor **0.0% → 12.0%** and flipped **three
gates** in one pass. The wordlist was **not** loosened to accommodate the prose: "come" would
match "come downstairs" everywhere, so its exclusion is correct and the writing was the thing at
fault.

**Two bugs only live play could find. Neither is visible to any static check.**

1. **Soft-lock.** The opening lands at 17:18; sleep was gated 21:00+; the shift needs the shop;
   and **navigation does not advance the clock**. Every scheduled window in the game was
   unreachable, forever. Fixed with `activity_evening` at the front room (+90 min) — which also
   feeds the anchor's word count — plus widening sleep to 20:00.
2. **Cold start.** Ray and Cal used the bathroom on weekdays only, and the game started Friday
   evening, so the core mechanic was dead until Monday — three in-game days. That was mechanical
   scheduling rather than fiction: people wash at weekends. Added weekend rows (Ray 09:30–10:15,
   Cal 11:00–11:50) and moved the start to Sunday so Monday morning is day 2.

**`npc_at_location` verified end to end.** At Monday 06:48,
`SugarCube.setup.getNpcsAtLocation('the_bathroom')` returns `['npc_ray']`; the landing offers
*"The gap in the door"* only while he is in there; entering applies all four effects
(`nerve` 0→3, `exposure` 6→10, `pride` 100→97, `arousal` 0→20), with zero JS errors.

**Engine fact learned:** a **repeatable** canvas at a location renders as a *clickable action*,
not an auto-fire — auto-fire is for non-repeatable priority canvases. My harness matched the
canvas title in a link and reported the scene as "fired" when it had never been entered. Also
`setup` is not a page global; it is `SugarCube.setup`.

**Gates: 4/8 judged pass (2 n/a), up from 0/4.** Passing: explicit floor 11.5%, explicit in
repeatable 100%, media pools clean, milestones 2/2. Remaining failures are all unbuilt work —
location fill (2,284 of ~36,000 words), traversal heat, standing surfaces, and no locked door
yet. All four land with the hubs in increment 2.

**Running tally of play-test friction:** three wrong selectors, one false-positive "fired"
check, one silent click failure that corrupted a walk, and two engine conventions learned the
hard way. Every one of these is a fact a reusable Player agent would hold and an ad-hoc script
does not. This is the strongest evidence yet for what Part C should build first.

---

## 2026-08-10 — `back_home` builds and plays; four engine facts learned from doing it

**What.** Authored `toml_phases/2_one_shots.toml` (the arrival chain + the first night), merged,
built, and **live-played the result headlessly**. Added §10–§12 to `references/engine.md`.

**It builds and it runs.** `package_from_toml … --gen-version v2 --debug` produces a 908KB
`index.html` with 32 compiled passages. A Playwright walk through the age gate, the four-node
opening and into the bathroom confirms:

- opening chain plays end to end; `arrival_done` set; player lands at `her_room`
- the first-night canvas **auto-fires on entering the bathroom**, correctly gated on
  `arrival_done is_true` + `first_night_done is_false`
- cascade beats advance; `exposure` moves **0 → 6**; `first_night_done` set
- **zero JS errors** throughout

Only warning is 4 uncopied media files — expected, `find-media` has not run.

**Four engine facts learned by doing, now in `engine.md` with citations.** Three of them broke
the build or the test first:

1. **`navigation_order` lists CHILDREN only.** The validator rejects listing the parent. The
   return link is generated from `entry_from` and renders as **`Leave <Location Name>`** — so a
   leaf room with `navigation_order = []` is not a dead end. I diagnosed `her_room` as a dead
   end before looking at the DOM; it was fine.
2. **`trait_decay` values must be positive magnitudes.** `hygiene = -10` is rejected with
   *"must be >= 0"*.
3. **`customizable = true` requires `[[player.customization_fields]]`.** Deferred to `false`
   for v0.1 and logged.
4. **`Start` is an age gate, not the game.** The starting canvas is reached through
   `[[✓ I am 18 or older…]]`, and `player.current_location` is `""` until then. Also: rendered
   links are `a.link-internal` inside `#story` — a bare `text=` selector matches the embedded
   `<tw-passagedata>` source and resolves to an invisible element.

**Process note worth keeping.** Facts 1 and 4 both made me *misdiagnose a working game as
broken*, and I rewrote the play-test selector three times before reading the DOM. That is the
argument for the Player being a **reusable agent with the engine's conventions baked in**
rather than an ad-hoc script rewritten per session — and it is the first concrete piece of
evidence for what Part C should build, produced exactly as intended by using the skill for real
rather than reasoning about it.

**Current state of `back_home`:** 885 words, 10 beats, 2 canvases. Gate 1 reads
`mean 111 · median 0 · anchor the_front_room 53%` — the anchor share is real but everything
else is the expected debt of a world with one scene in it.

---

## 2026-08-10 — first real use: `back_home`, and the scoreboard flattered an empty game

**What.** Ran the skill against a real game for the first time. Authored
`games/back_home/the_want.md`, `toml_phases/0_systems_spec.toml`,
`toml_phases/1_metadata_and_locations.toml` and `v2_state.json` — the Want and the Board for an
incest / female-protagonist premise. Then fixed a bug the run exposed in `scripts/gates.py`.

**The bug.** On a Board with no content authored yet, the scoreboard reported **3 of 10 gates
passing**. All three passed *vacuously*: "0 of 0 milestones open standing content", "0 pooled,
0 fixed single-clip", "0 visible meters rise past their content". An absence is not a pass, and
a stick that flatters an empty world is worse than no stick.

`gate()` now takes three states — `True` / `False` / `None`, where `None` means *there was
nothing to judge*. Those report as `n/a`, are excluded from the tally, and never count as a
pass. Six gates are legitimately n/a at Board stage. The same Board now reads **0/4 judged
gates pass (6 n/a)**, which is the truth.

Vesper is unaffected (it has content everywhere, 0 n/a) and holds at **1/10**.

**What the Board proved works.**
- The merge produced a clean 16,894-byte game from two phase files; `tomli` parses it.
- All 11 schedule rows bound to the correct NPC — no silent re-parenting across the
  `[[npcs]]` / `[[npcs.schedules]]` boundary.
- Dean's `23:00–01:30` row survived as **one row**, confirming the overnight-wrap finding
  rather than relying on it.
- Gate 10 printed `[declared]` and judged `nerve` / `exposure` / `need` **by name**, reading
  `board.ascent_tiers` out of `v2_state.json`. The ledger→gate wiring works end to end.

**Design decisions logged in `v2_state.json`,** with their costs:
- The house is **rooms, not one location** — presence and occupancy are per-location, so
  room-level co-location only exists if rooms are locations. Cost: eight locations to fill.
- `the_landing` exists to be the **vantage** the bathroom is peeped from
  (`npc_at_location`, `generators/v2.py:3480`, `:4131-4146`). It is a corridor and is expected
  to stay thin.
- Anchor is `the_front_room`, not `the_bathroom`. The bathroom generates the most *charged*
  beats but they are short; the front room hosts the evening rotation. Gate 1 also wants an
  anchor the player can re-enter — the measured failure case had a 29% anchor inside a sealed
  room.
- **The rotating lodger** (`npc_marek`, `the_box_room`) is the premise's answer to
  never-ending: a new character at an *existing* location every few releases, which is the
  measured release shape built into the fiction rather than bolted on. He works nights, so he
  is home alone with her while the house is empty — a window no family member competes for.
- Family is written as family and **labelled step-**, per the distribution evidence. Open risk
  recorded: Patreon's own terms are not in our research, and Patreon is the money.

**Engine limit that shaped the cast.** `requires_npc` is a single string
(`apps/projects/services/template_import.py:606`) and portraits render one card per NPC
(`generators/v2.py:4939`), so **two interactive family members cannot share a scene**. Every
scene is her plus exactly one of them; a second body can be narrated in and flag-gated. This is
recorded in the Board file itself so it constrains authoring rather than being rediscovered.

---

## 2026-08-10 — gate 1 was wrong: location fill is a distribution, not a floor

**What.** Replaced gate 1 in `scripts/gates.py` and propagated the correction through
`SKILL.md`, `references/the-board.md`, `references/the-release.md`, `references/state.md` and
`templates/board.toml`.

**The error.** Gate 1 demanded **≥10,000 words in every location**, from a "10,187 words per
location" figure. That figure was computed as *total words ÷ locations* — and the numerator
included `base-combat` and `base-system`, which are engine code, not location prose.

Measured on location prose only, the reference game's seed is **116,540 words across 25
locations: mean 4,661, median 3,154, min 302 (bus station), max 35,218 (school)**. So **24 of
its 25 locations fall under 10,000 words**. The exemplar failed its own derived gate 24 times
out of 25. Its current build still has 23 of 61 locations under 10,000.

**The real shape** is one or two deep **anchors** plus many legitimately thin satellites —
`school` alone held **30.2%** of all location prose at seed. Gate 1 now checks three things:

| check | threshold | seed evidence |
|---|---|---|
| anchor share | ≥25% of location prose in one location | school = 30.2% |
| median location | ≥3,000 words | 3,154 |
| mean location | ≥4,500 words | 4,661 |

plus a report of every declared location with nothing placed in it.

**Discrimination test — the bar set for any format or threshold — passes.** The corrected gate
clears the proven world (30.2% / 3,154 / 4,662) and still condemns the measured failure
(Vesper: median 674, mean 1,466, five empty rooms). A gate that could not separate those two
would be worthless.

**A finding that fell out of it.** Vesper *does* pass the anchor check at 29% — and its anchor
is `captive_room`, the sealed room with no exits that the player can never return to. An
anchor the world cannot reach is not a centre, and `references/the-board.md` now says so.

**Also corrected while propagating:** `v2_state.json` grew `board.ascent_tiers` (a *named*
declaration, which gate 10 now prefers over its top-3 guess) and `board.ceilings`; per-location
`budget` was replaced by an `anchor` flag, since there is no per-room quota any more.

**Honest note on the record.** This is the second threshold in this skill that did not survive
being checked against its own source, and both were caught by re-measuring rather than by
review. The standing rule holds: every number in `gates.py` carries its measurement inline, and
any number that cannot be re-derived from the snapshots on disk does not belong there.

---

## 2026-08-10 — templates, and a doctrine correction the templates forced

**What.** Added `templates/want.md` and `templates/board.toml` — fillable forms rather than
prose to be interpreted. Corrected `references/the-want.md` §3, `references/the-board.md` §3,
and gate 10 in `scripts/gates.py`.

**The correction, and how it was caught.** The plan set a discrimination test for any worked
example: the format must be able to express a *proven* world (Degrees of Lewdity's seed) and
must still condemn a *measured failure* (Vesper). Running the first half of that test against
DoL's actual source refuted our own doctrine.

We had written "**exactly one** global ascent axis" for a female-protagonist game, on the
strength of a secondhand summary. The source says three layers:

| layer | measured in DoL's seed |
|---|---|
| **ratcheting ascent tiers** | promiscuity 22 raises / 1 lower (206 gate sites) · deviancy 20/0 (129) · exhibitionism 12/1 (167) · `purity` counterweight (58) |
| **volatile state** | arousal — 277 sets, 55 increments, 8 decrements; moves both ways constantly |
| **per-character tracks** | robin / whitney / eden each carry love + lust + dom |

The tiers gate at **15 / 35 / 55 / 75** — a four-rung ladder twenty points apart, consistent
across promiscuity and exhibitionism. Doctrine now teaches three or four tiers, each naming a
*different kind* of going-further, because a single undifferentiated meter collapses parallel
ascents into one ladder every player has to climb the same way.

**Gate 10 changed with it,** and this moved the scoreboard: it now judges the top
`ASCENT_TIERS = 3` gated meters rather than one, and it prefers a **declaration** over a
guess — reading `board.ascent_tiers` from `games/<slug>/v2_state.json` when that file exists,
falling back to the top-3 heuristic and labelling the headline `[top-3 guess — no
v2_state.json]` when it does not. Rationale: skills and resources legitimately gate downward
and are not the spine; only the author can say which traits are ascent.

⚠️ **The previous entry's claim that the scoreboard "still reports 2/10" no longer holds.**
Vesper now scores **1/10**: `stealth` (4 expanding / 11 contracting) sits in its top three
gated meters, so the ascent gate fails. That is a real signal — the measured disease of that
game is that survival systems out-gate desire (stealth + weapon + fighting = 90 gate
references against corruption's 66) — but it is a change to the measuring stick and is
recorded as one rather than presented as a constant.

**Template bug caught by its own machine test.** `templates/board.toml` first declared player
traits as a multi-line inline table (`core_traits = { … }` across several lines), which is a
TOML parse error — inline tables cannot span lines. Real games use the `[player.core_traits]`
*section* form, in `1_metadata_and_locations.toml` rather than `0_systems_spec.toml`, because
TOML scoping requires `[[npcs]]`, their schedules and the player traits to share one file. The
template now round-trips: placeholders substituted, `tomli.loads` parses, all seven sections
present, five bands, schedules correctly bound to their NPC.

**Deferred deliberately.** The worked example. Shipping an invented toy world would make the
exemplar a guess, and reconstructing DoL as the exemplar would teach cloning a specific game —
the exact "copy what they ARE instead of understanding what makes them WORK" error this skill
was built to avoid. The first real Board becomes the exemplar instead, written when the
premise is chosen.

---

## 2026-08-10 — the doctrine lands: `SKILL.md` + six references

**What.** The rest of the skill, written on top of the scoreboard: `SKILL.md` (entry point and
dispatcher) plus `references/the-want.md`, `the-board.md`, `the-release.md`, `agents.md`,
`engine.md`, `state.md`. 934 lines of doctrine over 462 lines of script.

**Shape.** The skill authors a **release stream**, not a story. Four phases — `want`, `board`,
`first_release`, `release` — dispatched from `games/<slug>/v2_state.json`. Content is named in
three kinds (STANDING / TRIGGERED / MILESTONE), derived from what the reference game's own
release commits actually do, so the vocabulary owes nothing to the incumbent skill.

**Anti-drift.** The failure this skill is built against is a fantasy spec written once and
never re-opened. Two mechanisms answer it directly: the Want is defined as an *input to every
release* ("a release that cannot name which line of the Want it serves does not ship"), and
`v2_state.json` carries `want.last_read_at_release`, which is behind the current version if
the Want was skipped.

**Verified.**

1. *No invented fields.* All **67** engine keys the doctrine instructs an author to write were
   checked against `games/vesper/toml_phases/7_final_game.toml` — every one occurs in a real
   game. Nothing aspirational shipped.
2. *Gate coverage.* All ten gates have doctrine feeding them. Gates 1, 4, 5, 6, 8 and 10 are
   decidable from the Board alone (so they can be fixed before content is hung on a broken
   frame); gates 2, 3, 7 and 9 are content-level and are fed by the Want and the Release loop.
3. *Scoreboard regression.* `gates.py vesper` still reports **2/10** — the doctrine did not
   move the measuring stick.
4. *Dispatch.* `SKILL.md` registers with an `EXPLICIT-INVOKE ONLY` description naming its
   triggers and explicitly routing plain "start a new game" / "continue writing `<game>`"
   requests to the incumbent, per the `find-media-v3` precedent.

**One correction made to our own record while writing this.** `references/the-board.md`
initially repeated a note from project memory claiming an NPC schedule window cannot cross
midnight and needs two rows. Reading the source refuted it — `setup.isCurrentTimeSlot` in
`generators/v2.py` handles the wrap explicitly (`if (endTotal < startTotal) return currentTotal
>= startTotal || currentTotal < endTotal;`, call sites `:3448`, `:3465`, `:3612`). The Board
and the engine card now state the verified behaviour and flag the contradicting memory for a
live check. This is the reason `engine.md` requires a `file:line` on every claim, and why it
keeps an explicit "unverified — do not cite until read" list at the bottom.

**Open.** No game has been built with this yet. The TOML layout question was settled by keeping
v1's `toml_phases/` convention, since changing it is engine surgery on
`scripts/merge_toml_phases.py` and does not advance the doctrine.

---

## 2026-08-10 — `scripts/gates.py` created (the scoreboard, built before any doctrine)

**What.** First file of the v2 skill: a ten-gate measuring script that scores a built game's
merged TOML. Run as `python3 scripts/gates.py <game-slug>` or against an explicit `.toml`
path; `--json` for machine output; exit code 0 only when every gate passes.

**Why first.** Build order is deliberate — the measuring stick exists before the doctrine so
the doctrine cannot quietly drift off it. Every threshold traces to a primary measurement
rather than to inherited opinion, and the header of the script carries the evidence inline.

**Where the numbers come from.** Ten snapshots of Degrees of Lewdity's own source, fetched
from `gitgud.io/Vrelnir/degrees-of-lewdity` (project id 8430) and measured on one frozen
instrument, spanning its earliest retrievable build (root commit `ef4a8067102a`, "Initial
import (v0.1.20.2)", 2018-11-28) to `0.5.11.9` (2026-07-28) — 25 to 61 locations, 1,772 to
15,629 units, 254,674 to 2,235,775 words.

- `WORDS_PER_LOCATION = 10_000` — DoL's thinnest year ever (10,187). Its words-per-location
  rose monotonically for eight straight years to 36,652; it never opens a place faster than
  it fills it.
- `EXPLICIT_BEAT_FLOOR = 7.5` — share of beats carrying 3+ explicit words held at 7.5–9.3%
  across eight years and 12x growth. Raw sex-word share is *not* usable (it fell 3.00% to
  0.96% as systems and UI outgrew prose); the beat ratio is the stable one, and it is robust
  to word-list choice.
- `EXPLICIT_IN_REPEATABLE = 50.0` — from the measured failure case: 95% of Vesper's explicit
  beats sit in a sealed room with no exits while all nine of its repeatable sex loops score
  zero.
- `LOCATIONS_WITH_HEAT = 60.0` — deliberately not 100%. DoL's seed had sexual passages in 17
  of 25 locations (68%); a police station is allowed to be cold.

**Verified.** Run against `games/vesper`: **2 of 10 gates pass**. Four correctness bugs were
found and fixed during that run, each by reading the source rather than assuming:

1. `is_repeatable` defaults to **true** when the key is absent — confirmed firsthand at
   `generators/v2.py:10937`, `generators/v2.py:11010`, and `apps/stories/models.py:355`. An
   earlier grep-based pass that assumed otherwise reported 33% repeatable when the majority
   is repeatable; the script parses TOML and never greps.
2. An **effect** names its trait `trait`, while a **condition** names it `trait_key`. Reading
   only `trait_key` silently missed every trait write in the game and produced false
   "opens nothing" findings on the trait-sequenced `salvage_session_*` chain.
3. Meter ceilings live in `sidebar_items[].bands[]`, not in `player.core_traits` (which is a
   flat `{key: initial}` map). A top band with no `max` is unbounded by design and is skipped
   rather than guessed at.
4. Three gates were stricter than the evidence and were relaxed to match it: traversal heat
   (to 60%), milestone payoff (made transitive, since an opening funnel legitimately runs
   one-shot to one-shot and only the end of the chain must land on standing content, and with
   random ambients and self-guard canvases excluded), and meter direction (judged on the
   single most-gated meter, because a female-protagonist game runs one ascent axis while
   skills and resources legitimately gate downward).

**Not yet present.** No `SKILL.md`, so the skill does not register or trigger — correct for
now, as it is not ready to be invoked. The description will carry `EXPLICIT-INVOKE ONLY` when
it lands, following the `find-media-v3` precedent, and the incumbent `author-game` skill keeps
every ordinary request until v2 is promoted.
