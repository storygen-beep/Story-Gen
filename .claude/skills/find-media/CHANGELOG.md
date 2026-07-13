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
