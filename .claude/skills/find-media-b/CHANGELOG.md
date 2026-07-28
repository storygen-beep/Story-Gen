# find-media-b — CHANGELOG

The ledger for this skill. Record **every** change to any file in it — including small fixes
and wording. Newest first. Per entry: **what** changed (name the file) — **why** — and how it
was verified. Convention lives in `story_gen_django/CLAUDE.md` → "Skill ledger".

⚠️ This skill is an **experiment arm**, not production. Its whole value is that it differs
from `find-media` in exactly ONE documented way (question 2 removed). **Any change that adds
a second difference invalidates the A/B** — if you edit this file, say explicitly whether the
diff against `find-media` is still one axis.

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
