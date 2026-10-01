# The roster — one skill, many agents

The split is not by task. It is by **what has to be remembered**.

> Test: can you write this job's complete input on one page?
> **Yes** → an agent. **No** → the Owner keeps it.

**Agents look. The Owner decides.** The two exceptions below are deliberate and narrow.

---

## The Owner — the main loop

Holds the world. Owns the Want, the Board, the wiring, the gates, and **every write to disk**.

Anything where *why* matters more than *what* stays here: which arc feeds which economy, what
a release must leave behind, what a milestone opens. These cannot be paged into a fresh
context, which is exactly why they cannot be delegated.

---

## Pitchers — 3, parallel, deliberately uncorrelated

> ✅ **BUILT 2026-08-29.** The agent is `.claude/agents/v2-pitcher.md`, callable as
> `subagent_type: "v2-pitcher"`. Run three in **one message** so they go in parallel and
> cannot see each other.

**Job:** three takes on the next release subject.

Run them with **no shared context**. This is the one place where not sharing is the feature —
common context yields three shades of one idea, and the point is genuinely different options.

⚠️ **That design has a cost, and the cost is what took the build.** A Pitcher with no context
does not know what the game already contains: it will name a location that exists, a character
who does not (outside the one new person a thread pitch may add), or a mechanic the engine cannot run. So the context it is denied is the
*conversation*, never the *facts* — and the facts are generated rather than remembered:

```bash
python3 scripts/pitch_pack.py <slug>
```

Places, people, the meters and flags a pitch can key to, the money, the Want verbatim, what
already shipped, and which promises are still open — read off the game's own
`7_final_game.toml` and `v2_state.json`. **Everything a Pitcher may name is in the pack**, plus,
in a thread pitch, one new person who belongs to that thread (`--thread <id>`).

It reuses `gates.build()` and re-parses nothing, for the reason the Player's harness exists:
in this subject alone, a condition names its trait `trait_key` while an effect names it
`trait`, a condition names its owner `subject`/`npc_id` while an effect uses
`targetType`/`npcId`, and a triggerless canvas inherits its location from whatever links to
it. **The pack's own first run got one of these wrong** — it matched the declared ladder to
the built one by substring and starred a rung on one character's `want` that belonged to
another's, because `want` is a substring of every cast label. It printed a fact that was not
true of the game, which is the one thing a fact pack may never do.

**And it scores nothing.** Every figure is a count or the author's own declared number; where
the two disagree it prints both and says nothing about which is right. *"This location is too
thin"* is an opinion, `gates.py <slug>` is where opinions with evidence live, and four checks
here have already been withdrawn for failing something correct.

Each returns: the subject, which line of the Want it serves, which existing places and people
it touches (and a thread pitch's new person: name, age, thread), what it opens, and roughly what it
costs.

LO picks one. The Owner develops it.

### ⚠️ Three Pitchers with the same facts pitch the same thing

Removing the *conversation* removes conversational correlation. It does nothing about
**informational** correlation, and three agents given identical facts and an identical prompt
converge.

**Each Pitcher is given a different assignment** (LO, 2026-10-01): two get the two most-owed
relationships, from the pack's RELATIONSHIPS (`pitch_pack.py <slug> --person <npc>`); the third gets
a declared thread of her life (`--thread <id>`, `the-want.md` §6) and may add one new person who
belongs to it. Zero new places. The moment kind is a hint, and each names the kind its step serves.
All three keep the game's fantasy. A pitch is the next step on that relationship or in that thread —
what it pays, her moment, what it opens (`the-release.md`, "The next step").

> This is the capability the incumbent system most visibly lacks. It is a correctness
> pipeline — engine tables, traps, gates — which is a different muscle from "here are three
> ideas worth building."

---

## The Attack Panel — before the build, never after

> The agent is `.claude/agents/v2-attack.md` (`subagent_type: "v2-attack"`). Give each instance
> **one lens** and run them in one message; hand an instance somebody else's finding and its job
> flips to refuting it. It has **no instrument of its own**, so its first instruction is to run
> `gates.py` and `pitch_pack.py` and **report nothing they already report.**

**Job:** try to break the *design*, while changing it is still cheap.

Lenses, each drawn from a run that caught something real:

`soft-lock` · `grind` · `gate-parity` · `numbers` · `timing` · `prose-vs-mechanic` · `canon` ·
`flag chains` · `clamp/bounds` · `render buckets` · `excitement`

**`excitement` reads a pitch, not a design** (loop step 3b, before LO reads the three). It checks
that each of the eight lines is filled, specific and about her; that his three halves are there
(his want before, his "no" branch, he remembers); that *Before* names something the pack shows as
shipped and *Leads to* names a findable next step; that the two voice lines really differ; and
whether the pitch is **too close to a moment-library entry** — the same situation with the same kind
of person — naming the entry. **It scores nothing**: it returns the pitch with a one-line note beside
each line, and LO judges. Its only rejections are two instant fails, each quoting the line: a big
turn forced on her with no warning or way round, and sex used only as a punishment
(`the-surfaces.md` R5b.3). A final "no"
the button does not label is a defect: flagged, not failed.

**Every finding gets an adversarial verify.** *(LO decided.)* A raw finding is a hypothesis, and
the verify pass is what makes the survivors usable.

Give each verifier a **distinct lens** rather than running N identical skeptics. Diversity
catches failure modes that redundancy cannot.

---

## The Reader — the scenes, read as scenes

The agent is `.claude/agents/v2-reader.md`. Every release, after the build and before `--ship`, it reads
each **touched** canvas (`the-release.md` 6b) with a named person, and every explicit beat, against the
nine tests in `register.md` "What a scene contains". It returns a table — scene · test · PASS/FAIL/N/A ·
the line judged · why — and the same verdicts as JSON, which the session saves in
`release_page.reader`. **It fixes nothing and scores nothing; its verdicts gate** *(LO decided, D12;
`--ship` row *the reader passed*)*, with LO's waivers beside them. On test 1 it names the earlier canvases it checked
for his wanting (A13). The excitement lens is not here — it reads
pitches, on `v2-attack`.

---

## The Prose Maker — narrow on purpose

> ✅ **BUILT 2026-08-29.** The agent is `.claude/agents/v2-prose.md`, callable as
> `subagent_type: "v2-prose"`. The instrument is `gates.py --beat <path>`.
>
> ⚠️ **It was blocked on that instrument for as long as this section has existed, and the
> section never noticed.** The spec below promises "one measurable target" — and nothing in
> this skill could measure a loose paragraph. `Beat.explicit` (`gates.py:409`) is a property
> on a `Beat` assembled out of parsed TOML blocks, so it needs a built game; `--words` reports
> vocabulary and nothing else. **The agent's own spec named a target that did not exist**, and
> an agent that cannot be told whether it succeeded is not an agent, it is a wish.
>
> `--beat` closes it, and **every threshold in it is one `gates.py` already used** — the 3+
> explicit words that make a beat count as explicit at all, `SENTENCE_CEILING`, `DASH_CEILING`,
> the `RUNGS` list. Nothing new was invented, deliberately: an instrument built for one agent,
> measuring on its own private scale, would let the Prose Maker optimise for something the
> build never checks.
>
> **The pivot is reported as a SHAPE and never as a verdict.** The rule is a reading test —
> *is the last sentence about what it MEANS or what is HAPPENING* — and no regex decides what a
> sentence is about. What is observable is where the body words fall, so `--beat` prints the
> distribution across sentences and quotes the last sentence back. Whether a beat
> pivoted is a reader's call, and automating that call is how a check starts failing correct
> work.

**Job:** one beat, from a spec it cannot argue with, hitting one measurable target.

This agent exists for **attention**, not knowledge. *(LO decided.)* A rule can be right there
and still be broken, because when one agent is simultaneously holding flags, placement, media, tiers and save-safety,
prose is what slips.

Its spec: the beat, the character, the tier, the explicit ceiling from the Want, and the
target. Its output: the prose. It does not choose placement, gates, or media.

---

## The Player — measures heat, does not judge it

> ✅ **BUILT 2026-08-29.** The harness is `scripts/playtest.py`; the agent is
> `.claude/agents/v2-player.md`, callable as `subagent_type: "v2-player"`. A live play finds what
> no source gate can — for one, an effect op the runtime does not implement (`applyTraitEffect`
> handles only `add` and `set`, `v2.py:6213`).
>
> ⚠️ **Why it is shared code.** The engine's signatures are easy to get wrong by hand:
> `applyTraitEffect(targetType, npcId, trait, op, val, clampFlag, cap)` takes seven positional
> arguments, not one options object (`v2.py:6213`, `:20817`), and `pickQuestsCards` returns `[]`
> for any scope but `"story_goals"` (`v2.py:16227-16228`). Every signature the harness wraps is one
> nobody has to re-derive.

**Job:** play the build and report numbers.

- clicks and words to the first explicit beat
- whether high-traffic locations are erotic on entry
- whether repeatable loops clear the explicit floor
- where it soft-locks, where it drags

**It measures. LO judges.** This distinction is load-bearing: in a thirty-game study, the
three games that were actually *played* produced every single heat finding in the corpus, and
the twenty-seven that were only parsed produced none. A green build has never once detected
appeal.

### How it must assert — non-negotiable

**Assert on `SugarCube.State.variables`. Never on rendered page text.**

The
rendered label is not the string that was authored — icons, spacing, cost suffixes and state
decoration are added at render — so a selector matching author-side text fails on a working build
and the Player reports a defect that does not exist.

The same applies to finding things to click: locate by passage and canvas id, not by visible label.

**Before it can assert at all it needs `engine.md` §24** — four facts about reading a built game,
each of which otherwise produces a false alarm indistinguishable from a real defect.

⚠️ **The ban is on LABELS, and the line matters** — stated absolutely above, and one shipped script
sits the other side of it. `playtest_standing.py` asserts on **body prose** to decide which ladder
rung rendered, and it proved six rebuilt ladders live. The distinction
the record actually supports: a *label* is decorated at render — icons, spacing, cost suffixes — so
matching author-side text against it fails on a working build; a *beat's prose* is not. So: prose may
answer **which variant rendered**; only state may answer **whether the mechanic fired**. The harness
enforces exactly that split — it ships `sv()` and `body()` and deliberately no `assert_text`.

**Every red is a hypothesis until its cause is found in `v2.py` or the game's TOML, quoted as
`file:line`.** This is the Player's version of the Attack Panel's verify pass, and it is not
optional.

---

## The Listener — what players said after a release

> ✅ **BUILT 2026-09-27.** The agent is `.claude/agents/v2-listener.md`, callable as
> `subagent_type: "v2-listener"`. Its instrument is `scripts/listen_mopoga.py`.

**Job:** loop step 8, about two weeks after a build is public. It reads the new comments since the
release date — mopoga through the script, F95 read-only in LO's Chrome, gamcore by hand or recorded
as "not read" — and returns a `listen[]` draft for `v2_state.json`: what players praised, asked
for, complained about and got stuck on, each with a quote and a count. If anything would change
the Want's promise, it returns that as one question for LO.

**It reads and nothing else.** It never posts, likes, replies or downloads, never clicks anything
that changes state, and never judges or proposes ideas: players choose the order and supply small
ideas; they do not set the premise (Great Games Study, round 4b).

---

## What is NOT an agent

**Media finding.** That belongs to the `find-media` skills. This skill declares slots —
`pool_dir`, `pool`, the tier suffix, the search vocabulary — and stops there.

**Anything that writes game TOML.** One attempt, one deleted build.

---

## Calling them

Use the Agent tool with a schema when you want structured output; run independent work in a
single message so it goes in parallel. Keep each prompt to one page — if it will not fit, the
job belongs to the Owner.

Load only the references an agent actually needs. The library is addressable on purpose: a
Prose Maker needs the Want's register section and nothing else; the Attack Panel needs the
Board and the gates.
