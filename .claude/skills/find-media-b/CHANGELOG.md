# find-media-b — CHANGELOG

The ledger for this skill. Record **every** change to any file in it — including small fixes
and wording. Newest first. Per entry: **what** changed (name the file) — **why** — and how it
was verified. Convention lives in `story_gen_django/CLAUDE.md` → "Skill ledger".

⚠️ This skill is an **experiment arm**, not production. Its whole value is that it differs
from `find-media` in exactly ONE documented way (question 2 removed). **Any change that adds
a second difference invalidates the A/B** — if you edit this file, say explicitly whether the
diff against `find-media` is still one axis.

## 2026-07-29 — judging procedure fixed; run 1 invalidated as a SPEED measurement

**Diff against `find-media` is still exactly one axis** (question 2 removed). Both changes
below are procedure and gate definition, not new differences — the board is a shared-tool
feature available to both arms, and the `must_show` rule is question 1 and binds both.

- **`SKILL.md`** — Override 2 now mandates reading a **strip BOARD top-to-bottom** and taking
  the topmost passing row, and explicitly forbids working through a batch one strip at a time.
  **Why:** run 1 read strips singly to guard against a real bias risk (I knew arm A's picks, and
  seeing a better row 5 could tempt me to invent a fault in row 1). The guard was unnecessary —
  row order is fixed *before* looking, so a later row cannot change whether an earlier one
  passed — and it cost **52 image reads instead of ~15**. That inflated arm B's judging time and
  led me to report "removing question 2 doesn't make it faster", which the data did not support.
  **Run 1's picks stand; run 1's TIMING does not.** The note now says what to do with the
  temptation instead: log it in `scores.jsonl`, since noticing it is the arm's actual job.
- **`SKILL.md`** — added the `must_show` rule as its own section: *fails when the strip shows it
  ABSENT or CONTRADICTED; framing that merely doesn't cover it is UNVERIFIED, not failed —
  except gaze/affect items, which fail when their carrier is cropped.* Promoted out of the
  changelog because without it "the first that passes" is not deterministic. Flagged as
  belonging in `find-media` proper.
- **Depends on** `find-media`'s 2026-07-29 `video_frames.py --board` entry — the capability had
  been silently lost in the 07-28 promotion, which is the root cause of the whole detour.

**Verified:** board built over the 16 `lab_eyecontact_t5` candidates reproduced all six run-1
verdicts from one image. Run 1's ten picks snapshotted to
`games/media_lab_b/.find-media/run1_picks.json` so run 2 can be diffed against them — identical
picks would prove the procedure change is speed-only.

## 2026-07-28 — first run executed (no skill files changed)

- **No file in this skill was edited.** The diff against `find-media` is still exactly one axis.
  Logged here because the ledger should record that the arm was *exercised*, not just written.
- Ran it on `games/media_lab_b/` end to end: 10/10 installed, all 10 green on
  `tier_format_check.py`, 31 strip kills, 1342 options left unranked on the shelf, and
  `game-review/load?game=media_lab` still 0 missing / 10 found (arm A untouched).
  **0 of 10 slots tied** — every arm-B pick is a different file from arm A's.
  Result write-up: `games/media_lab_b/AB_RESULT.md`.
- **One ambiguity in the spec surfaced and was resolved during the run** — worth folding into
  `find-media` proper if it survives review, because it is a *question-1* rule and therefore
  applies to both arms: what to do when a `must_show` item is outside the frame rather than
  visibly absent. Rule applied uniformly across all ten slots: *a `must_show` fails when the
  strip shows it ABSENT or CONTRADICTED; framing that merely doesn't cover it is UNVERIFIED,
  not failed — except for gaze/affect items, which fail when their carrier is cropped, since
  affect has one carrier and a cropped face means the content is absent.* Without this,
  "install the first that passes" is not actually deterministic.
  **Verified:** stated in `AB_RESULT.md` with the two slots that forced it
  (`lab_eyecontact_t5/08` passed on unverifiable posture, `lab_tease_t4/00` failed on an
  unshowable affect gate) so the calls can be audited against arm A.
- **Known miss recorded, not papered over:** `lab_finish_facial_t5` is
  `POOL_GATE_UNSATISFIABLE` — 16 of 16 stripped, none shows his hand at the back of her head.
  Least-bad installed and flagged. The gate is identical in both arms, so this slot carries no
  information about ranking and should be discounted when judging the A/B.

## 2026-07-28 — created

- **`SKILL.md`** — new. A thin *delegating* skill: it instructs the runner to read and follow
  `.claude/skills/find-media/SKILL.md` verbatim, then applies exactly two overrides —
  (1) JUDGE Stage C deleted (no HEAT/SETTING/CRAFT, no bands, no dead-clip veto, no ranking),
  (2) install the FIRST candidate that passes Gate 1 + Gate 3 on its strip, in
  `fetch_candidates.py` order, and stop judging that slot.
  **Why delegating rather than a fork:** a 10-file copy would drift from find-media, and the
  moment it drifts the experiment stops measuring the judging rule and starts measuring the
  divergence. One file keeps the experimental diff to a paragraph anyone can audit.
  **Why the frame strip stays:** the strip verifies *correctness*, so it is question 1. Cutting
  it would test a question already answered (thumbnails lie — measured 3/5 and 4/6 killed).
  Also specifies a reduced `scores.jsonl` (no heat/setting/craft/total fields) so neither arm
  can be compared on numbers only one of them produces, plus integrity rules: don't read arm
  A's evidence mid-run, log a gate reason for every rejection, treat a tie as a real result.
- **`CHANGELOG.md`** — this file.

**Verified:** paired with `games/media_lab_b/`, whose TOML diffs against `games/media_lab/`
by only the `[project] id`/`title` and a header comment — the ten slots, descriptions and
`search_queries` are byte-identical — and whose options store is a copy of arm A's
(1352 candidates, one junk `https://www.gif` regex artifact dropped), so the candidate shelf
is identical and the judging rule is the only variable.
