---
name: find-media-b
description: EXPERIMENT ARM ONLY — not the production media skill. A deliberately crippled find-media that verifies CORRECTNESS and nothing else: gates plus the frame strip, then installs the first candidate that passes. No heat scoring, no ranking, no aesthetic judgement of any kind. Exists solely to A/B whether find-media's ranking step (question 2) earns its keep, by filling games/media_lab_b/ for comparison against games/media_lab/. Use ONLY when the user explicitly says "find-media-b" or names the Q2 A/B experiment. For any real game, use `find-media`.
---

# find-media-b — find-media with question 2 removed

**⚠️ This is an experiment arm. Never use it to fill a real game.** It is find-media with its
taste deliberately amputated, so that the value of that taste can be measured.

## Why this exists

find-media asks two questions of every candidate:

1. **Is this the correct scene?** Binary gates — act, position, people count, affect, cast,
   POV-when-the-partner-must-be-visible — verified against a 4-frame strip. This half is
   measured strong: it caught a clip slugged `back-alley-slut` that was a woman flashing on a
   lit street, and one slugged `three-men-fuck-one-woman` that only ever showed two.
2. **Of the correct ones, which is most alive?** HEAT / SETTING / CRAFT scoring, the bands,
   the dead-clip veto.

**Question 2 is the unproven half.** Exactly one of its heat signals is confirmed — eye
contact held across the whole loop — and it is confirmed largely because the user taught it:
in the one head-to-head, the spec-perfect ranked pick lost to the user's grainy, wrong-room,
black-and-white, 264px clip. Everything else in the rubric is inferred from a rejection
history and has never been tested.

So this arm removes question 2 entirely and installs the first *correct* clip. If the user
prefers arm A's picks, ranking earns its keep. If he can't tell the two apart, it doesn't.

## How to run it

**Read `.claude/skills/find-media/SKILL.md` and follow it exactly** — SCOPE → PLAN → SEARCH →
STOCK → JUDGE → INSTALL, the same scope briefs, the same `fetch_candidates.py` two-wave
fetching, the same `video_frames.py --mode rep --sheet` contact sheet and `--mode strip`
verification, the same install via `media-finder/grab`, the same quality gates
(`tier_format_check.py`, dedup, fetch sanity).

Both arms deliberately share every piece of tooling. If the tooling differs, the experiment
measures the tooling instead of the judging, and the whole thing is wasted.

**Exactly two things change:**

### Override 1 — Stage C is deleted

find-media's JUDGE has three stages: A contact sheet, B frame strip, C rank into a shelf.
**Stage C does not exist here.** Do not score HEAT, SETTING or CRAFT. Do not assign bands
(ALIVE / WORKING / DEAD). Do not apply the dead-clip veto. Do not rank the survivors. Do not
form an opinion about which clip is better and do not write one down.

Stages A and B stay exactly as they are — the contact sheet still narrows the field, and
**every animated finalist is still frame-stripped.** The strip is how *correctness* is
verified, so it belongs to question 1, not question 2. Removing it would test a different
question, and one we have already answered.

### Override 2 — install the FIRST candidate that passes

Walk the fetched candidates in `fetch_candidates.py` order (slug rank — deterministic, and
identical to what arm A used). Strip each in turn. **The moment one passes Gate 1 and Gate 3,
install it and stop judging that slot.** No looking ahead to see whether something better is
coming; that impulse *is* question 2.

If nothing in wave 1 passes, top up with `fetch_candidates.py --more` and continue down the
list. If nothing at all passes, install the least-bad and say so plainly — same as arm A.

The shelf still gets stocked (it already is: `media_lab_b`'s options store was copied from
arm A so both arms see the identical candidates), but it is **unranked** here. Order carries
no claim.

## Evidence format

`games/<game>/.find-media/evidence/<item>/scores.jsonl`, one object per candidate examined,
with these fields **only**:

```json
{"candidate_id":"blovjob/kneeling-blowjob","url":"https://…","verified":"strip","gate":"pass","decision":"installed","note":"first candidate to pass; stopped here"}
{"candidate_id":"sexxxgif/on-the-table","url":"https://…","verified":"strip","gate":"fail","gate_reason":"position:torso_upright","decision":"gate_reject"}
```

`decision` ∈ `installed` | `gate_reject` | `not_examined`. **No `heat`, `setting`, `craft`,
`total` or `heat_band` fields** — there is nothing to put in them, and their absence is what
keeps the two arms' evidence honestly comparable on question 1.

Candidates after the installed one are recorded as `not_examined` — that is the point, and it
is also the arm's cost: it never sees what it skipped.

## Integrity rules for whoever runs this

- **Do not read arm A's `scores.jsonl` or its installed picks during the run.** Knowing what
  arm A chose can only contaminate the gate calls.
- **Record a gate reason for every rejection.** The install is mechanical, so gate pass/fail
  is the only place bias could enter — the reasons make it auditable.
- **A tie is a real result.** If the first survivor here happens to be the same clip arm A
  installed, that slot says "ranking changed nothing here". Record it; do not re-roll it.
- Arm A must be left untouched: `game-review/load?game=media_lab` must still report
  0 missing / 10 found when this run finishes.
