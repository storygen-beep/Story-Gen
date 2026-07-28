# find-media — CHANGELOG

The ledger for this skill. Record **every** change to any file in this skill
(`SKILL.md`, `references/*`, `scripts/*`, etc.) — including small fixes and wording.
Newest first. One bullet per change; group bullets under the date they were made.
Per entry: **what** changed (name the file) — **why** (the motivation / root cause) — and
how it was verified if relevant (grep / build / live-play).

Convention lives in `story_gen_django/CLAUDE.md` → "Skill ledger".

<!-- entries recorded going forward; example shape:
## YYYY-MM-DD
- reworded dispatch note (`SKILL.md`) — clarified phase resume — n/a
-->

## 2026-07-29 (later) — CLIP DELETED; the shortlister is named as Claude's vision

- **`scripts/clip_shortlist.py` — DELETED** (232 lines). **Why:** it never ran. Verified zero
  CLIP outputs anywhere in `games/media_lab/` or `games/media_lab_b/` across three full
  ten-slot runs. Its own docstring labelled its numbers **"Demo evidence"** — 88% top-3 on SFW,
  **25–31% on explicit acts**, and explicit acts are this skill's primary content. It was also
  the skill's **only** non-stdlib dependency (torch + transformers + Pillow on a pinned
  Framework interpreter outside the venv, plus a ~600MB model cache).
- **`scripts/requirements.txt` — DELETED.** It existed solely to install those three packages.
  **The skill now has no Python dependencies at all** — every script is stdlib-only under plain
  `python3`, and the single external dependency is `ffmpeg`/`ffprobe`. Side benefit that now
  matters: the skill runs unchanged in a cloud session, where torch and the model cache are
  absent (relevant to `media_lab_c` / `media_lab_d`).
- **`references/clip_preranking.md` → `references/sheets_and_boards.md`** — rewritten, not just
  renamed. Dropped: what CLIP is for, caption policy, torch prerequisites, the pinned-interpreter
  section, the `clip_shortlist.py` invocation. Kept and updated: the `video_frames.py` section
  (rep frames, strips, `--sheet`, `--board`), evidence-under-the-game, "the sheet is evidence
  not a decision", the fallback contract (now ffmpeg-only), and "auto-accept stays OFF".
  The two-column `video_frames.py` vs `clip_shortlist.py` input table collapsed to the one rule
  that survives: **a still IS its own rep frame; `--mode strip` refuses stills because there is
  no loop to make a claim about.**
- **The replacement doctrine**, now stated in `SKILL.md` §5 Stage A and in the new reference:
  **the shortlister is Claude's vision reading one assembled image.** ffmpeg only cuts, resizes,
  labels and glues — it judges nothing. Therefore (a) **tile order carries no claim** — the
  sheet/board is in `fetch_candidates.py` order, a stable index for naming a tile, not a
  ranking; and (b) because no algorithm can be re-run to check a call, **the written
  `gate_reason` in `scores.jsonl` IS the verification mechanism** and the board is the exhibit.
  Supporting evidence for (b): re-judging the same ten slots from boards reproduced **10/10** of
  the previous run's picks.
- **`SKILL.md`** — eight sites: Stage A rewritten; §Mode column header `Options stocked =
  --top-k` → `Options stocked` (`--top-k` was a `clip_shortlist.py` flag); §Batching pointer
  repointed and given the 52-vs-14 read measurement; `candidate-evaluator` subagent boundary
  now says tiles are in fetch order, not pre-ranked; disclosure-table row replaced; scripts
  inventory pruned; the Interpreter paragraph now asserts stdlib-only with ffmpeg as the sole
  external dependency; the exit-3 paragraph drops the torch clause.
- **`references/media_sources.md` (×2), `references/scoring_rubric.md` (×1)** — pointers
  repointed at `sheets_and_boards.md`.
- **Deliberately NOT touched:** older CHANGELOG entries mentioning CLIP. A changelog is the
  record of what was believed and when; rewriting it destroys the trail that makes drift
  visible.
- **Verified:** `grep -rniE "clip|torch|transformers|FIND_MEDIA_PY|montage|top-k"` over both
  skills returns hits in `CHANGELOG.md` only; no dangling `clip_preranking.md` reference; every
  reference named in the disclosure table exists on disk; `video_frames.py --sheet` and
  `--board` both still exit 0 and write their images against a real candidate dir; all six
  remaining scripts respond to `--help` under plain `python3`.

## 2026-07-29 — strip BOARDS restored to `video_frames.py` (regression fix from the 07-28 promotion)

- **`scripts/video_frames.py`** — added `strip_board()` plus `--board` / `--board-rows`, and a
  `boards` field on `FrameResult`. Batch strip mode now stacks every candidate's strip into one
  labelled image, one row per candidate, six rows per board (1280×1920), spilling to
  `<stem>_2.jpg`. Guarded: `--board` without `--videos-dir --mode strip` exits 2.
  **Why — this is a REGRESSION I introduced.** Per-slot strip boards existed as an ad-hoc
  `strips.sh` and produced the 1280×1920 images that carried the 2026-07-27 media_lab run. The
  2026-07-28 promotion of that script into the skill kept `--sheet` for **rep mode only** and
  silently dropped strip boarding. Nothing failed loudly; the next run simply read strips one
  at a time — **52 image reads where ~15 would have done**, roughly 3× the cost of JUDGE.
  Worse, the lost time was first attributed to the experiment under test (`find-media-b`
  "not being faster") rather than to the missing feature — a wrong conclusion that stood until
  the user pushed back on it.
  **Implementation notes:** rows are padded to `cols*tile_px` before `vstack` because strips
  differ in width when a clip yields 3 frames instead of 4, and unequal widths make ffmpeg drop
  inputs; `vstack` is used rather than `tile=` for the reason already recorded in
  `contact_sheet()` (measured 07-28: `tile=` emitted one input of eight).
  **Verified 2026-07-29:** ran it over the 16 `lab_eyecontact_t5` candidates → 3 boards
  (1280×1920, 1280×1920, 1280×1280), both guard paths exit 2, and **reading board 1 reproduced
  all six run-1 per-candidate verdicts** — including the eye-contact breaks at 00/frame-2 and
  02/frame-1 — at ~260px per frame after the reader's downscale.
- **`SKILL.md`** §5 Stage B and the scripts inventory — batch JUDGE now reads a board; the
  single-clip form is explicitly demoted to "re-checking one candidate after the board".
- **`references/chrome_route.md`** §7 Stage B — same, with the regression history in a warning
  box so the feature is not dropped a second time.

## 2026-07-28 — the fetch harness becomes skill infrastructure + two-wave fetching

The media_lab run took 81 min, but batch 2 ran at **5.6 min/slot against batch 1's 10.6** —
the difference was that the tooling existed by then. That tooling lived in
`games/media_lab/.find-media/`, so every future game would re-pay ~20 min building it and
re-discover the same failures. The skill shipped **no fetcher at all** (only a "manual curl"
line). This entry fixes that, and records the fixes that did NOT survive measurement.

- **NEW `scripts/fetch_candidates.py`** — the skill's only fetcher; hand-rolling one is now
  explicitly wrong. Ports `hunt.py`'s slug `rank()` and own-origin-Referer `fetch()` (the
  403 lesson is now *code*, not prose), adds: two-wave `--top` / `--more` (skips what is on
  disk, contiguous numbering, never re-fetches a URL), `--max-tries` (default 4×`--top`, so a
  broken network cannot walk a 140-deep shelf — it walked 128 in testing before this), chunked
  reads, staging files so a partial download never lands as a candidate, and `--json`.
  **Verified live** against the media_lab shelf: wave 1 8/11, wave 2 6/9, 20 entries / 20
  unique URLs / contiguous `00`–`19` / no leftover staging; exit 1 on nothing-fetched, 2 on a
  bad slot.
- **`scripts/video_frames.py`** — `--sheet` builds the numbered contact sheet in one command
  (was a hand-written ffmpeg line in the docs), and batch **rep** mode now accepts stills
  (`STILL_EXTS`, `still_rep()`): a mixed pool is normal and dropping its images read as an
  empty harvest. Batch **strip** still refuses stills — no loop, no claim. `--sheet` is
  guarded to rep+batch (exit 2 otherwise); `FrameResult.sheet` added for `--json`.
  Regression-checked: single `--video` rep/strip and batch strip unchanged.
- **`references/chrome_route.md` §6** rewritten around the script, with the **two-wave
  pattern** as the default (measured: 144 files fetched to strip 60 — the surplus only padded
  a sheet; easy slots save ~40%, hard slots run wave 2 and pay what they always paid). §7
  Stage A now calls `--sheet`. Manual curl demoted to a single-file fallback (`--max-time`
  30 → 60, since 36.8s downloads are real). SKILL.md: script list + a two-wave line in JUDGE.

**Two "obvious" optimisations were MEASURED AND REJECTED — both are now warnings, because
the instinct to re-add them is strong:**
- **Slow-host deprioritisation is dead.** Hosts measured at 30–44s were **1–2s** an hour
  later. A blacklist built that afternoon would permanently avoid good sources. There is
  deliberately no slow-host list in this skill.
- **Parallelism is a hedge, not a speed feature.** These CDNs throttle: at 8 workers per-file
  went **7.8s → 34.1s** for ~1.5× total, and five benchmarks in one afternoon gave 0.8× /
  1.5× / 2.6×. `--workers` defaults to 3 and the docstring forbids raising it on one good
  measurement.
- **A flat download deadline is wrong.** 20s looked sane and threw away good clips:
  `101534-sultry-bj-on-knees.gif` is 6.6 MB, takes 36.8s at 0.18 MB/s, worst chunk gap 4.9s —
  slow, never stalled. Wave 2 went **1/9 → 6/9** once gating moved to stall-detection
  (`--timeout`, the socket gate) with `--deadline` demoted to a 120s runaway backstop.
- **ffmpeg's `tile=` filter is not trustworthy here.** Given eight verified 320×320 tiles it
  emitted a sheet containing **one**, reproduced in pure shell. `contact_sheet()` uses
  explicit `hstack`/`vstack`.

All of it is condensed into a "**Network timing is weather**" box in §6: if you measure
something here and want to act on it, measure it again hours later first.

Also: `games/media_lab/.find-media/{hunt.py,sheet.sh,strips.sh}` deleted (git history keeps
them) and `FINDINGS.md` §8 records the promotion.

## 2026-07-27 (later still) — `scene_semantics.py` classifier: vocabulary hole + two weak-evidence bugs

Reported symptom was one slot: `blowbang ring of men standing around one woman` classified
**static + vanilla**, so the validator recommended a `.jpg` for a gangbang clip and asked to
down-grade it to `_base`. The symptom was one slot; the cause was three.

- **Root cause — the multi-partner family was entirely absent from the vocabulary.**
  `blowbang`, `gangbang`, `bukkake`, `threesome`, `foursome`, `orgy`, `double penetration`,
  `spitroast` were unknown to BOTH `ANIMATED_KEYWORDS` and `RATING_HARD_NSFW`. With no strong
  signal anywhere in the blob, a single incidental word decided both axes. Also added
  `cumshot`, and added `anal`/`deepthroat`/`rimjob`/`titjob`/`squirt`/`pegging`/`doggystyle`
  to the ANIMATED set — those were rated NSFW but never marked as motion, so a `.jpg` version
  of any of them passed the format check unflagged. Tease band (`downblouse`, `upskirt`,
  `nipslip`) added as animated + borderline.
  **Bare `facial` is deliberately animated-only, NOT rated** — it is a spa treatment in a
  domestic beat, and the rating set drives an AUTO retag. Verified: a spa-facial beat now
  reads `unknown` → `leave`, while `facial cumshot` auto-retags correctly.
- **Bug 2 — a lone posture word could decide both axes.** New `WEAK_STATIC_KEYWORDS`
  (`standing`, `sitting`, `watching`): they classify static only when corroborated by a real
  static keyword, and they are **out of `RATING_SFW` entirely**. Alone they now yield
  `ambiguous` / `unknown`, which means "accept the author's extension, leave the tag".
  This is the fail-safe: an act word we have not thought of can no longer be overruled by
  the word "standing".
- **Bug 3 — found while regression-testing, same class, worse.** `LOCATION_KEYWORDS`
  (`kitchen`, `bedroom`, `office`, …) were in `RATING_SFW`, so a room name was treated as
  evidence a scene is vanilla. Live example: `sex/calloway_finish_facial_t5.webm` — "a man
  finishing on a kneeling woman's face in a dim office" — rated **SFW on the single word
  `office`**, and the validator asked to down-grade it to `_base`. Its sibling
  `renner_finish_facial_t5` escaped only by accident, because its query happened to contain
  `cumshot`. `STATIC_KEYWORDS` is now `ACTIVITY_STATIC_KEYWORDS | LOCATION_KEYWORDS` and
  `RATING_SFW` is built from the ACTIVITY set only — locations still drive FORMAT (an empty
  kitchen is a still) and no longer touch RATING.

**Verified across 287 real items in two shipped games, old vs new:**
vesper format-OK **151→157/172**, "need your call" **4→0** (all four were false positives,
including two facial slots the old code wanted to make SFW); the_inheritance gained exactly
one format flag, `scenes/gray_pegging.jpg`, which is a **true** positive the old vocabulary
could not see. Domestic regressions hold (dinner/reading/empty-room still static+sfw).
media_lab now Format OK **10/10** with no retag prompts. `validate_queries.py` re-exports
still resolve; the other three scripts unaffected.

**Note for a later pass, not acted on:** vesper's confident auto-retags went 50→66, i.e. 16
more untagged-but-explicit files are now detected (`sex/salvage_session_*_fuck.webm`,
`sex/cell_turns_used_and_pissed_on.webm` …). That is real tagging debt in the game, not a
classifier problem. `apply_retags.py` was deliberately NOT run — that is an authoring call.

## 2026-07-27 (later) — doctrine corrected by the media_lab 10-slot study

The v2 rewrite below shipped with a query-craft rationale that turned out to be **partly
wrong about its own mechanism**. `games/media_lab/` ran it as a controlled experiment (10
slots, 27 queries, 3 slots carrying deliberately old-doctrine queries as a hidden control;
write-up in `games/media_lab/.find-media/FINDINGS.md`). These edits are what it forced.

- **`references/query_rewriting.md`** — §Google dialect: promoted the format token to the
  first and most emphatic rule, with the 3× measurement (`7→59`, `1→54`, `0→91` fetchable
  urls, same query ± the word `gif`). Added the ≤2-setting-token ceiling and the
  load-bearing-setting-slot-is-hardest corollary. Added a new subsection to the doctrine note,
  "What the 2026-07-27 control actually proved", stating plainly that the 21× old-vs-new gap
  is real but is **NOT** evidence for act-led word order — it decomposes into the missing
  format token and story-word intent-flipping, which are independent, and `gif` fixes only
  the first. **Why:** the old text let a reader credit word order for a gap caused by two
  other things, which would have survived the next rewrite as folklore. Two dialect-table
  rows updated to match. **Verified:** every number cited is a counter I recorded live.
- **`references/chrome_route.md`** — §3 same two query rules restated at the router level
  (they are the first thing a run reads). §4: require `pathname.length > 4`, because the
  extraction regex matches the bare string `www.gif` in page text and stocks a dead option.
  §6: new warning box — **never send `Referer: https://www.google.com/`**, with the per-host
  403/200 table. **Why:** attaching a Google referer is the natural thing to do right after
  scraping a Google results page, and it 403s five of six catalogued hosts; it cost 13 of 29
  fetches in this run and presents as "those hosts are down". Notes explicitly that
  `_fetch_headers` (`media_finder.py:158-159`) is already correct, so **no engine change was
  made** — the exposure is hand-rolled fetchers only.
- **`references/media_sources.md`** — added the referer rule to the direct-fetch contract
  table. **Downgraded slugs**: still a term mine, now explicitly worth **zero** as a
  correctness claim, with the two counter-examples (`back-alley-slut` is a street flash;
  `three-men-fuck-one-woman` shows two). Added the second-wave host list (15 new hosts, all
  measured 200) and flagged that `static-ca-cdn.eporner.com` failed every fetch this run
  despite being in the corpus. Added direct evidence for the band model (`downblouse` reaches
  a host cluster no explicit-act query touched) and **corrected `dogging`** — it returns
  beach/daylight, it is not a night/alley term, and the old mapping pushed dark-alley beats
  the wrong way.
- **`references/scoring_rubric.md`** — Confidence table: the "thumbnails lie ~2 of 3" row now
  reports both measurements (65% early, **30% across 54 strip finalists here**) and explains
  the denominator difference rather than pretending one supersedes the other — gate hard on
  the contact sheet and the strip kills less, without ever becoming optional. Replaced "a
  fresh 10-query study will refill this table" with the study's actual status: it refilled the
  **query-craft** rows and **not** the heat rows, because heat calibration needs the human's
  verdicts. Records the deliberate probe planted on the tease slot, where the install and
  rank-2 option disagree between two rules in that file.

**Not changed, on purpose:** the HEAT weights and bands. Nothing in this study measured them,
and tuning them here would be exactly the "do not tune the weights to make a past pick come
out right" failure the file warns about.

## 2026-07-27 — v2: rebuilt as an options-stocking scout on the Chrome route

**Why the whole rewrite.** Players reported the videos were bad. A live A/B against LO
(same beat, independent hunts, traces compared) located the cause in the skill's *shape*,
not in any single rule: it was an autonomous picker (search → score → install → done).
Everything else followed. It locked onto one source because one site is what you can
automate. Its rubric scored setting/act/appearance/quality and had **no axis for whether a
clip was alive** — `scoring_rubric.md` even encoded a wrong room as a hard reject worth 0,
which would have binned LO's winning clip (POV, wrong room, B&W, 264px) before he saw it,
while my spec-perfect alternative scored well and was dead. Evidence + traces:
`games/vesper/.find-media/route_study/`.

- **New shape: stock a shelf, don't pick.** Install one best-guess so the game always
  renders, and stock ≥6 alternates per slot in the media-finder options store for the
  human to choose from. Verified live: 54/54 candidates POSTed to `options/add` straight
  from a Google results page, CORS fine.
- **Deleted the Tor/Playwright route entirely** — `scripts/nsfw_harvest.js`,
  `references/nsfw_pipeline.md`, `references/sfw_pipeline.md`,
  `references/playwright_diagnostic.md`. **Why:** one Google query in the user's own Chrome
  reached 9+ sites the old route never touched and produced a better clip; the Tor
  toolchain also broke twice in a single session (npm module wiped from `/tmp`, then a
  stale cached browser build).
- **New `references/chrome_route.md`** — the measured procedure, including the term-hunt
  step the skill never had. That gap is why `downblouse` was never found: there was no
  instruction to go learn what a beat is *called*. Google's own result labels are the
  richest term mine (they taught `dogging` unprompted); an LLM is useful for modifiers and
  community names but paraphrases uselessly when a thing has no canonical name.
- **New `references/media_sources.md`** (merges the two dead pipeline files) and
  **`references/audit_mode.md`** (sweeps already-shipped clips against their beats).
- **`references/scoring_rubric.md` rewritten — the centerpiece.** HEAT is now the dominant
  axis; correctness (act, position, count, affect, cast) is a **binary gate that can never
  earn points**, because points are how a correct-but-dead clip out-totals a flawed-but-
  alive one. SETTING is conditional and is *skipped* (recorded null) when not load-bearing.
  The accept threshold is gone — ranking + human choice replaces it. Honest confidence note
  kept: eye-contact-holding-across-the-strip is the one *proven* rule; the rest derives
  from a documented rejection history and gets refilled by a fresh study.
- **`references/query_rewriting.md` split** into route-neutral semantics and a per-source
  dialect section. **The correction that matters:** the old "strip banned words, 2 canonical
  tags" law was PornHub-tokenizer behaviour sold as universal. Verbose queries work fine on
  Google; the thing that breaks a Google search is *story/character* words (adding
  `drunk guy` returned film stills and news). So the authors' descriptive `search_queries`
  were never the bug — searching PornHub directly was. **This killed a fix I was one step
  from making to the author-game skill**, which would have mandated two-word tags at
  exactly the wrong layer.
- **Scripts.** `dedup_tracker.py`: normalizes `phncdn.com/gif/<id>` → `ph_gif:<id>` — without
  it, new-route ids would not collide with the 126 existing `ph_gif:` records and we would
  have shipped repeats from the first run (verified: 6 url forms collapse to one identity).
  Also tolerates 22 legacy hand-written rows that lacked `normalized_id` and were therefore
  invisible to the dedup check. `video_frames.py`: batch strip mode, and a short-clip
  sampling fix (an out-of-range seek returns the LAST frame, so a 2s clip's strip faked a
  held pose — it silently corrupted the one signal the rubric calls proven).
  `tier_format_check.py`: magic-byte check extended to t4, `.gif` allowed at SFW tiers, and
  `t0`/`t1` accepted (they previously failed the mandatory pre-install gate as
  "unknown_tier", a rejection describing nothing wrong with the file).
  `validate_queries.py`: route-neutral half split out into `scene_semantics.py`.

### ⚠️ A factual error I introduced and then corrected the same day
I told the rewrite agents that `egl.phncdn.com/gif/<id>.gif` "fetches PornHub gifs direct —
no Tor, no signed URL, no expiry." **That is false**, and it propagated into several files
before I caught it. Measured: that URL returns **470 on clearnet AND over Tor**, for every
id tried. The real PornHub media URL is signed, time-limited and IP-locked
(`?validfrom=…&validto=…&ipa=1&hash=…`) — the old skill's signed-URL doctrine was right and
I overturned it on bad evidence. Worse, our extraction **strips query strings** (the browser
JS tool blocks URLs carrying them), which destroys that signature by construction. And
`pornhub.com` is unreachable on clearnet from this machine at all.

**Root cause of the error:** in the worked example, 40 of 54 candidates downloaded and I
called it a success without checking *which* 14 failed. Exactly the 4 phncdn ones were among
them. I generalised from "the batch mostly worked."

**Standing rule:** PornHub-hosted results are **discovery-only** — read them for their
titles and tags (vocabulary), never queue them for download. The fetchable corpus is the
aggregators, all measured 200 on clearnet with no signing and no expiry: blovjob,
nsfwgify, xgroovy, porngif.co, hardcoregify, xgifer, sex.com, flashingjungle, eporner. The
worked example's winning clip came from blovjob and never needed Tor.

### Engine changes shipped alongside (outside this skill, listed here because the skill depends on them)
- `api/v1/media_finder.py` — **`grab` was destroy-then-download**: it unlinked every
  same-stem file *before* attempting the fetch, so a dead URL left the slot empty and the
  old clip gone forever. Now: fetch to a temp file, and only on success park the incumbent
  in `.find-media/previous/`, register it as an option (`origin: "previous"`), and swap.
  Verified live — a deliberately dead URL left the file byte-identical; a real swap
  preserved the original at the same md5 and offered it back; reinstalling it restored the
  exact original bytes. Also: `grab` now clears the slot's review verdict and prunes the
  consumed option, and sends a full browser UA + host-appropriate Referer (the shipped UA
  was truncated and had no Referer, which picky CDNs reject).
- New `options/clear` with a `before` timestamp, so a refetch **stocks first and prunes
  after** — never clearing the shelf on the way in. This preserves a hard-won rule the
  rewrite had inverted; wiping a candidate pool before its replacement exists once
  silently ate three harvests.
- `api/v1/game_review.py` — enumerates **portraits** (NPC `portrait=`, `[player_portrait]`
  states and outfits, `image_select` options). They were invisible to the entire find/
  review loop for its whole life and surfaced only as packaging "File not found" lines,
  which is why a new NPC's face kept shipping absent. Verified: vesper 203 → 224 refs, all
  21 portraits enumerated. `api/v1/media_review.py` gives them their own lane.
- `apps/game_generation/services/game_service.py` — the output-copy skip test compared
  *sizes*, but images are downscaled to max width 800 on copy, so the destination is always
  smaller and the skip matched every time. A **replaced source image could therefore never
  reach the built game** — the long-standing "I swapped the art but the game shows the old
  one" bug. Now compares modification time.

## 2026-07-13 — nsfw_harvest video download timeout (30s→60s + curl --retry)

- `scripts/nsfw_harvest.js` — bumped the inline video-download curl from `--max-time 30`
  (execSync timeout 35s) to `--max-time 60` (timeout 65s) and added `--retry 2`. Root cause:
  a degraded Tor exit takes >30s to pull a 3–4MB webm, so `curl` hit its deadline, the file
  came back <50KB and got unlinked, and a batch that had already FOUND 15 valid candidates
  saved zero of them (observed live: `Found 15 candidates` immediately followed by
  `✗ video download failed`). The 60s ceiling + 2 retries lets slow-but-alive circuits finish
  the transfer. Verified: `node -c` parses clean.

## 2026-07-13 — nsfw_harvest batch resilience (goto retry + harvest-before-wipe)

- `scripts/nsfw_harvest.js` — two fixes to stop one flaky Tor navigation from destroying a
  whole batch. (1) `harvestFromSearchPage` now retries `page.goto` up to 3× (timeout raised
  45s→90s), rotating the Tor circuit (`kill -HUP tor`) between attempts, and only throws if
  all three fail. (2) The main loop wraps each item's harvest in try/catch and `continue`s on
  failure, and — critically — moved the `rmSync(subdir)` wipe to run only AFTER a successful
  harvest. Root cause: a degraded circuit made the FIRST query's `goto` time out; the throw was
  uncaught in the per-item loop, so the whole batch died — and because each subdir was wiped
  BEFORE harvesting, a failed item destroyed any candidate pool already sitting there (this
  silently ate three separate Vesper batches this session). Verified: `node -c` parses clean;
  re-run of a 5-item batch survives a first-query timeout and proceeds to the rest.

## 2026-06-24 — nsfw_harvest video download fix (browser User-Agent)

> **SUPERSEDED 2026-07-27 — do not read this entry as current capability.** It is the only
> text left in this skill that says a phncdn URL fetches. That was true of the *signed*
> `el2.phncdn.com` URLs this deleted script pulled off a gif page over Tor, in the same
> circuit that minted them. It is NOT true of the unsigned `egl.phncdn.com/gif/<id>.gif`
> form: that returns 470 on clearnet and over Tor alike. PornHub is now discovery-only —
> see `references/media_sources.md`. Kept for the root cause, which still holds: a media
> CDN that gets no browser User-Agent answers 410 and you get a 0-byte file that looks like
> a success.

- `scripts/nsfw_harvest.js` — added `BROWSER_UA` + `REFERER` consts and sent both as `-H`
  headers on the thumbnail AND video Tor curls; added a <50KB guard that unlinks the file and
  logs `✗` instead of the misleading `✓ 0KB`. Root cause: PornHub's video CDN
  (`el2.phncdn.com`) returns `410 Gone` to requests with no browser User-Agent, so every
  harvested `.webm` saved as 0 bytes — a systematic break of the inline harvest-time video
  download for every NSFW run (the thumbnail CDN tolerated the missing UA, which masked it).
  Verified live during the media_testbed run: `-H Referer` alone → 410 (136B HTML);
  `-H User-Agent` + `-H Referer` → full 2–4MB WebM. Post-fix, a 1-item re-harvest writes real
  `.webm` files (>1MB) and `file` reports `WebM`. The `.json` metadata is still written before
  the video download, so an unlinked dud keeps its `videoUrl` for the Step-4 re-pull path.

## 2026-06-24 — content-led SFW/NSFW routing (tier audit + retag)

Problem: SFW/NSFW routing rode entirely on the author's `_tN` filename suffix. No tag →
silent default to base = SFW (under_one_roof's untagged kisses would've pulled as tame
stock); wrong tag → misroute (sex tagged t2 → stock; dinner tagged t6 → PornHub). LO's
call: don't route around a bad tag — **fix it at the source** so the suffix is correct.
Principle: content leads the routing, the tag grades the heat; confident up-grades auto,
borderline + down-grades asked.

- `scripts/validate_queries.py` — added three PURPOSE-BUILT rating buckets
  (`RATING_HARD_NSFW` = `SEXUAL_TERMS_FOR_SFW_CHECK` + explicit nudity; `RATING_BORDERLINE`
  = kiss/tease/bathe/shower/…; `RATING_SFW`) kept deliberately separate from the format
  `ANIMATED_KEYWORDS`; `infer_tier_tagged()` (reports `was_tagged` to tell a forgotten tag
  from an intentional `_base`); `classify_content_rating()`; `propose_tag()` + `TagProposal`
  dataclass implementing the audit→retag matrix; `main()` emits per-item `tag_proposals` in
  `--json` and a "⚠️ TIER RETAG" report section. Generalizes the existing
  `check_tier_alignment` warning into an actionable proposal. Verified: 6 crafted cases
  (dinner→leave, untagged kiss→ask t4, base+blowjob→auto t5, t6+dinner→ask down-grade,
  untagged+naked→auto t5, location→leave) + real `--toml 3_activities.toml` flags 1 auto
  (drawing_jake_sex+undressing→t5) and 12 asks (every untagged kiss AND solo shower).
- NEW `scripts/apply_retags.py` — mechanical, stdlib-only TOML suffix rewriter; takes
  accepted `[{file,tier}]`, rewrites quoted `file=` paths in the SOURCE `toml_phases/*.toml`
  (strips any existing `_tN`/`_base` first), `--dry-run` diff, exit 1 on a path that matches
  nothing. **Skips any `*_final_game.toml`** (the merge regenerates it — CLAUDE.md). Verified
  on a copy of under_one_roof: dry-run + apply rewrote only `3_activities.toml`, copy still
  parses, original game untouched.
- NEW `references/content_rating.md` — principle, the three buckets (vs the format set),
  the audit→retag matrix, the auto-vs-ask asymmetry, and the run order
  (audit → accept/ask → apply_retags → re-merge+package → re-fetch missing list).
- `SKILL.md` — decision tree gains step 5 "Tier audit + retag (before SCOPE)";
  progressive-disclosure router adds `content_rating.md` (eight→nine).
- The format axis (`classify_content_family`) and `tier_format_check.py` untouched — once
  the suffix is correct they just work.

Default shipped: confident up-grades auto, borderline + down-grades ASK (flip to
propose-only by withholding the auto_retags from `apply_retags`'s accepted list). Deferred:
inferring fine t5/t6/t7 grades from text (only the human grades heat). Pending: end-to-end
dogfood through a real re-merge+package+re-fetch.

## 2026-06-24 — CLIP pre-rank + montage EVALUATE rewire

Root cause (audit `wf_752276bd-939` over a real 133-item run): the LLM viewing
~560 candidate thumbnails per game (~0.5–1M tokens just looking) was the dominant
token sink and the cause of daily-limit blowups; "more parallel subagents" made it
worse (fan-out reloads context). Everything else is already a 0-token script.
De-risked with 4 live demos before editing (SFW retrieval, NSFW act-judging,
multi-frame video, live PornHub cull). Plan: `~/.claude/plans/write-the-change-plan-eager-wilkes.md`.

- NEW `scripts/video_frames.py` — ffmpeg-only rep-frame (median-of-N samples, skips
  black/seam) + act-verification strip; GIF loops have no meaningful poster and one
  frame misleads — verified rep/strip/batch on shipped under_one_roof clips (strip =
  1280×320, 4 tiles) and exit-3 when ffmpeg is off PATH.
- NEW `scripts/clip_shortlist.py` + `scripts/requirements.txt` — local CLIP
  (openai/clip-vit-base-patch32) ranks candidates vs a caption and writes ONE labeled
  top-K montage so the LLM Reads one image, not ~15 thumbnails. `HF_HUB_OFFLINE`
  pinned; exit 3 → graceful fallback to direct thumbnail viewing. requirements.txt
  pins torch/transformers/Pillow (NOT auto-installed; other scripts stay stdlib-only)
  — verified: ranks 15 real harvested thumbs on MPS (scores match the cull demo),
  montage renders labeled tiles, exit-3 under the torch-less django venv python,
  exit-1 on empty dir.
- NEW `references/clip_preranking.md` — CLIP doctrine: pre-rank/cull, NEVER the final
  pick, with demo numbers (SFW top-1 60% / top-3 88%; NSFW act-judging 25–31%; cull
  15→5 keeps 3–4 good); caption policy (query not prose, 60 vs 32%; NSFW cull caption
  = setting+people, not the act); prereqs (`FIND_MEDIA_PY`, install cmd, cached model,
  HF offline); both scripts' usage; fallback contract; auto-accept documented-but-OFF.
- `SKILL.md` — RETRIEVE SFW → inline WebSearch + download-to-evidence (no per-source
  subagent); EVALUATE → CLIP pre-rank + ONE montage per rating (SFW top-5 / NSFW cull
  top-6, setting+people caption) with exit-3 fallback; §Batching arithmetic reworded
  (~5 montage reads/batch; 5-item cap stays); subagent table drops `sfw-searcher` and
  `candidate-evaluator` now Reads the montage; progressive-disclosure router adds
  `clip_preranking.md` (seven→eight).
- `references/sfw_pipeline.md` — removed parallel `sfw-searcher` fan-out → inline
  WebSearch (Unsplash/Pexels first, Pixabay CRITIQUE-only); download candidates to
  `evidence/<item>/candidates/` BEFORE eval (CLIP needs files); batch-token bullet now
  montage-based.
- `references/nsfw_pipeline.md` — Step 3 rewritten (rep frames → CLIP cull 15→6 on
  setting+people → view ONE montage → judge the act yourself); Step 5 verify frame →
  `video_frames.py --mode strip`, superseding the single `ffmpeg -ss 00:00:02 -vframes 1`.
- `references/scoring_rubric.md` — scoring step 1 "View the thumbnail" → "View the CLIP
  montage; CLIP ranks but doesn't score — you do; on NSFW re-judge the act per tile."

Deferred: auto-accept (needs per-pool SFW calibration, not run). Pending: end-to-end
dogfood on a live game with the dev server + Tor up.
