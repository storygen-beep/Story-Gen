---
name: find-media
description: Find and download missing media (images and video clips) for a story game. Reads the game's TOML, detects per-item content rating from tier (base/t2/t3 = SFW, t4+ = NSFW), validates and rewrites search queries, retrieves candidates in parallel (WebSearch for SFW, Playwright+Tor+PornHub for NSFW), scores candidates with a visual rubric, runs a critique loop on failures, and downloads via the game's dev API. Use this skill whenever the user says "find media for <game>", "download missing media", "populate media", "/find-media", or when a game TOML has media blocks with search_queries and the corresponding files don't exist on disk. Also use when an existing run needs to resume — the skill persists evidence and state to disk so crashed or interrupted runs recover cleanly.
---

# find-media

Find missing media for one game, run-to-run recoverable, with deterministic query rewriting and a critique loop for failures.

## When this triggers

Trigger conditions (any one):
- User says "find media for <game>", "/find-media <game>", "populate media", "missing media"
- A TOML file at `games/<game>/toml_phases/6_final_game.toml` or `apps/game_generation/games_toml_files/<game>.toml` contains `search_queries` fields with no matching file on disk
- User asks to resume a prior find-media run (state lives in `games/<game>/.find-media/`)

Do NOT trigger on: general questions about game design, TOML schema questions, questions about the tier system that aren't about downloading. Answer those directly.

## Decision tree — before any work

1. Is there a resolvable TOML for this game? If not, ask for the path and stop.
2. Is the Django dev server running on `localhost:8000`? If not, remind the user to run `python manage.py runserver` and stop.
3. Fetch the authoritative missing-media list from the game-review API:
   ```bash
   mkdir -p games/<game>/.find-media
   curl -s "http://localhost:8000/api/v1/dev/game-review/load?game=<game>" > games/<game>/.find-media/game_review.json
   ```
   Extract `missing_media` — if empty, report and stop. The API enumerates all 5 categories (canvas blocks, locations, clothing, phone posts, dating profiles) and checks three disk roots (`output/`, game root, `videos/`) to confirm absence. The list is authoritative; don't re-scan. See `references/game_review_api.md` for the contract. **Fallback** if Django is unreachable: use `scripts/validate_queries.py --toml games/<game>/toml_phases/6_final_game.toml` (walker mode; misses locations, clothing, and phone posts without queries — the 58-item blind spot the API fixes).
4. Classify each missing item by `type` (from the API). If any have tier t5+ (canvas NSFW) — derived from the canvas items' filename `_tN` suffix — also verify Tor + Playwright + ffmpeg prerequisites (see `references/nsfw_pipeline.md` §Prerequisites). Non-canvas types (`location_image`, `clothing_image`, `social_post_image`, `dating_profile_photo`) are always SFW.
5. **Tier audit + retag (before SCOPE).** Routing rides on the author's `_tN` suffix, which can be missing or wrong. Run `validate_queries.py` and read its `tag_proposals`: take the confident `auto_retag`s, **ASK the user** on every `ask` (borderline / down-grade), then `apply_retags.py` writes the corrected `_tN` into `toml_phases/*.toml` → re-merge + re-package + re-fetch the missing list. The corrected suffix then drives all routing. Full buckets, matrix, and commands in `references/content_rating.md`. Skip if the audit returns no proposals.

## Paths — source vs compiled

Two folders look similar and get confused. Keep them separate:

- **`games/<game>/videos/`** — the SOURCE of truth for media. The API (`/api/v1/dev/media-capture`) writes here. Scan here when checking which items are missing. The `scene_id` you pass to the API is relative to this folder — e.g., `scenes/kiss`, not `videos/scenes/kiss` (the API strips the `videos/` prefix) and NEVER `output/videos/scenes/kiss` (the API does NOT strip `output/`, and the file would land nested wrongly at `games/<game>/videos/output/videos/scenes/kiss.ext`).
- **`games/<game>/output/`** — the COMPILED HTML game produced by `package_from_toml`. Contains `index.html` plus a copy of `videos/`. Regenerated on every package run. Never write media here directly; it will be overwritten.

When a direct curl download is required (rare — only the NSFW age-gate-expired fallback in `references/nsfw_pipeline.md`), the target is always `games/<game>/videos/<subfolder>/<file>`, never `games/<game>/output/...`.

## Mode selection

Pick the lightest mode that fits the batch:

| Mode | When | Phase budget |
|------|------|--------------|
| **quick** | All items are SFW base/t2/t3 tier, under 10 items | SCOPE → PLAN → RETRIEVE → EVALUATE → PACKAGE (no critique loop unless everything fails) |
| **standard** | Mixed SFW + t4 borderline, or SFW-only over 10 items | All 5 phases including one critique cycle on failures |
| **deep** | Any t5+ NSFW items present | All 5 phases, up to 3 critique cycles per failed item |

The mode decision is per-batch. Split the batch by content rating and run SFW-first in parallel while NSFW-deep runs sequentially.

**Batch cap: 5 items per pipeline slice.** `scripts/nsfw_harvest.js` enforces this at runtime for NSFW harvest. The same cap applies to SFW (per-subagent dispatch).

## Batching — the batch is a pipeline slice, not just a RETRIEVE slice

When the total work is bigger than the cap (say 50 missing items), do NOT run RETRIEVE 10 times in a row for all 50 before starting EVALUATE. Do NOT harvest everything first, then evaluate everything, then package everything. That's the wrong shape.

**Correct shape**: each batch of 5 runs end-to-end through phases 3–6 before the next batch starts.

```
Phases 1-2 (SCOPE + PLAN)
  run UPFRONT for all 50 items
  ↓ they're cheap, network-free, TOML-only, no expiration concerns

Batched loop (phases 3-6)
  for each group of 5:
    RETRIEVE (5)  →  EVALUATE (5)  →  CRITIQUE+REFINE (any that fail)  →  PACKAGE (5)
  then next group of 5.
```

### Why the batch-as-pipeline-slice

- **Harvest-to-eval gap stays tight.** If you harvest 50 NSFW items and then evaluate 50, you're looking at thumbnails 30+ minutes after they were harvested. If CRITIQUE decides an item needs a re-harvest with a new query, you're also re-harvesting under a stale Tor circuit with possibly-dead cookies. Batch-of-5 keeps that gap to minutes.
- **Progress is durable.** After each batch completes, 5 items are fully downloaded, verified, deduped, and written to `run_manifest.json`. If the session crashes or the user interrupts, you have 5/10/15 complete — not 50 half-processed items with no final files on disk.
- **Critique loops stay local.** When CRITIQUE triggers a delta-query and re-harvest, it's for items WITHIN the current batch, running against a still-warm Tor circuit. Across batches, the critique loop counter resets.
- **Token budget stays sane.** CLIP ranks each item's ≤15 candidates and you view ONE montage of the top-K — so a batch of 5 is ~5 montage reads, not the ~75 individual thumbnail reads the old flow required. The 5-item cap stays for the reasons above (Tor circuits, durable progress, critique locality), but the token driver is now montage reads. See `references/clip_preranking.md`.
- **Tor circuits match the work unit.** One circuit should ideally complete one batch. Across batches, you can request a fresh circuit (`kill -HUP $(pgrep tor)`) between groups if needed — clean rotation.

### Explicit rule

If N items remain to process:
- `ceil(N / 5)` total batches
- Each batch: RETRIEVE → EVALUATE → CRITIQUE (up to 3 cycles) → PACKAGE
- Between batches: update `run_manifest.json`, then start the next group
- Never start a new RETRIEVE while the previous batch's PACKAGE is incomplete

## Format classification — image vs animated

Tier gates what can be shown (base/t2/t3 SFW → t5+ NSFW). **Format gates how it's shown — and it's driven by action, not by tier.**

The rule: **motion-worthy scenes use animated (.webm / .gif / .mp4). Static scenes use images (.jpg).**

| Content class | Examples | Format |
|---|---|---|
| Domestic / conversational | dinner, chores, talking, studying, working | `.jpg` |
| Location / object | kitchen, bedroom, garage, coffee mug | `.jpg` |
| Light flirt | hand-holding, greeting, sitting close, warm smile | `.jpg` |
| Kiss / tease | making out, teasing, biting lip, seductive gaze | **animated** |
| Solo body | undressing, flashing, bathing, showering, nude posing | **animated** |
| Intimate / explicit | any NSFW act (t5+) | **animated** |

A t4 kiss scene is `.webm`, not `.jpg`. A t5 tease is `.webm`. A t3 dinner is `.jpg`. A t4 "romantic candlelit dinner" can stay `.jpg` if no physical intimacy is shown.

`scripts/validate_queries.py` runs this check during PLAN phase. Keyword detection on description + search_queries. If a scene's description says "kiss" but the filename is `.jpg`, the validator flags it under FORMAT MISMATCH and surfaces the issue before RETRIEVE starts.

**Important**: the API ignores your TOML extension and saves files using the SOURCE URL's extension (see `references/api_behavior.md`). So the format mismatch warning is really a hint to **pick the right KIND of source** during RETRIEVE — an animated URL for kiss scenes, a static image URL for dinner scenes. If you do that, the saved file will be the right type regardless of what the TOML said, and the renderer's extension-agnostic lookup handles the mismatch.

TOML cleanup (fixing `.jpg` → `.webm` for kiss scenes) is still worth doing for human clarity, but it's not a download blocker.

## The five phases

**Phase ordering across items**:
- Phases 1–2 (SCOPE, PLAN) run UPFRONT for all missing items — they read the TOML, produce briefs, and rewrite queries. No network, no batching needed.
- Phases 3–6 (RETRIEVE, EVALUATE, CRITIQUE, PACKAGE) run in pipeline slices of 5 items. See §Batching above.

### 1. SCOPE (per item)

Iterate `missing_media` entries from `games/<game>/.find-media/game_review.json`. For each entry, produce a scope brief using `templates/scope_brief.md`. The brief contains:
- `item_id`, `file_path`, `type` (one of 6 API values), `category`, `canvas_id`, `order`
- `tier` (canvas: infer from filename `_tN` suffix; non-canvas: always `base`)
- `content_rating` (non-canvas types are always SFW; canvas inherits from tier)
- `required_format` from `scripts/tier_format_check.py` (tier-driven for canvas, `.jpg` for non-canvas static types)
- Narrative context — **branches by type** (see `templates/scope_brief.md`):
  - Canvas `image`/`video`: read 2–3 TOML paragraphs before/after the block (from `games/<game>/toml_phases/6_final_game.toml`)
  - `social_post_image`: use `description` directly (shape: `"@poster: caption"`), parse hashtags/nouns as cues
  - `location_image`: use `description` directly (shape: `"Navigation image for {name}"`)
  - `clothing_image`: use `description` directly (shape: `"{name} ({slot})"`)
  - `dating_profile_photo`: use `description` + look up NPC in API response's `npcs` array for age/traits
- `rejection_criteria` (derived from type + tier — see `references/scoring_rubric.md` and `templates/scope_brief.md`)

Write the brief to `games/<game>/.find-media/scope/<item_id>.md`. If the scope phase crashes, it resumes from here. The API already confirmed file absence — don't re-scan disk.

### 2. PLAN

**Step A — synthesize queries for items with empty `search_queries`.** Phone posts, and occasionally other categories, arrive from the API with no queries declared. For each such item, write 2–3 queries from `description` + `type` + `category` using the worked examples in `references/query_rewriting.md` §Synthesizing queries. Hard constraints: `location_image` and `clothing_image` are always SFW regardless of player state. Write synthesized queries back into the item entry in `game_review.json`.

**Step B — validate.** Run:
```bash
python .claude/skills/find-media/scripts/validate_queries.py --from-api-json games/<game>/.find-media/game_review.json
```

The validator applies deterministic rewrites (banned words, gender direction, setting-first, vague terms), tier alignment checks, and format family checks — same rules as before, now applied to both author-written and LLM-synthesized queries uniformly. Full rule set in `references/query_rewriting.md`. Rank the rewritten queries: top query uses setting-first formula, backups broaden progressively.

Never run a query the validator flagged as unfixable — surface it to the user instead.

**Offline fallback**: if the server isn't running, `--toml games/<game>/toml_phases/6_final_game.toml` still works for canvas items. Won't catch the non-canvas categories (locations, clothing, phone posts, profile photos) — those require the API.

### 3. RETRIEVE

Route by content_rating:
- **SFW** → inline WebSearch (2–3 queries, **no per-source subagents**) → download candidates to `evidence/<item_id>/candidates/`. Details in `references/sfw_pipeline.md`.
- **NSFW** → batch 3–5 items into `scripts/nsfw_harvest.js` (Playwright + Tor + PornHub GIF search, single-page harvest extracts thumbnails + video URLs in one load). Details in `references/nsfw_pipeline.md`.

All candidates persist to `games/<game>/.find-media/evidence/<item_id>/candidates.jsonl` as they arrive (SFW: downloaded JPGs; NSFW: harvested thumbs + clips). This makes Tor circuit drops and mid-batch crashes recoverable. CLIP then pre-ranks them before EVALUATE — see §EVALUATE and `references/clip_preranking.md`.

### 4. EVALUATE

CLIP pre-ranks the candidates so you view ONE montage instead of every thumbnail.
CLIP is a pre-filter — it never replaces a gate and never makes the final pick. Full
doctrine + exact script invocations in `references/clip_preranking.md`.

1. **Dedup** — `scripts/dedup_tracker.py --check <gif_id_or_url> --game <game>`; drop already-used candidates before ranking.
2. **Pre-rank with CLIP** (exit 3 → CLIP/ffmpeg unavailable → fall back to viewing thumbnails directly, exactly as the old flow did — never crash the run):
   - **SFW** → `clip_shortlist.py --candidates-dir evidence/<item>/candidates --caption "<top validated query>" --top-k 5 --montage-out evidence/<item>/montage_shortlist.jpg`. CLIP is a strong SFW shortlister (top-3 = 88%).
   - **NSFW** → first `video_frames.py --mode rep` (a still per clip), then `clip_shortlist.py --caption "<setting + people, NOT the act>" --top-k 6 --montage-out evidence/<item>/montage_cull.jpg`. CLIP only **culls** 15→6 here (25–31% on acts).
3. **View the ONE montage.** Apply hard-rejection filters from `references/scoring_rubric.md` (3+ people, solo, wrong setting, etc.) across the tiles; on NSFW **judge the act yourself** — CLIP did not.
4. **Score** each surviving tile with the rubric (SFW 40/30/30, NSFW 30/40/20/10); write to `games/<game>/.find-media/evidence/<item_id>/scores.jsonl`. Map the chosen tile letter back to its candidate id via the `clip_shortlist.py` JSON `ranked[].montage_label`.
5. **Pick** the highest above threshold (60 NSFW / 70 SFW). For an NSFW video pick, build a `video_frames.py --mode strip` and confirm the act holds across the loop before PACKAGE.

Do NOT auto-pick the top-titled result, and do NOT treat CLIP's #1 as the winner — CLIP ranks, you decide. PornHub/GIPHY titles are user-generated noise. The visual score is the decision.

### 5. CRITIQUE + REFINE (only on failure)

Trigger when no candidate scores above threshold after the first RETRIEVE pass. Dispatch the `fail-triage` subagent with these diagnostic questions:
1. **Query wrong?** Re-read narrative, check against `references/query_rewriting.md` rules, generate delta-queries.
2. **Source wrong?** Try an alternate (SFW: switch GIPHY→Pexels; NSFW: try `setting+action` reversed or body-type variant).
3. **Tier wrong?** If narrative actually warrants a lower tier, flag the TOML for review instead of downloading wrong content.

Loop back to RETRIEVE with the delta-queries. Cap at **3 critique cycles per item**. If still failing, write the best-below-threshold candidate to the failure report and surface it to the user — do NOT silently skip.

### 6. PACKAGE

For each winning candidate:
1. POST to `http://localhost:8000/api/v1/dev/media-capture` with `{url, scene_id, game}`. The API auto-detects the file extension from the source URL (or its Content-Type) and strips any TOML-declared extension — see `references/api_behavior.md` for the full detection chain.
2. Run `scripts/tier_format_check.py --file <actual_downloaded_path> --tier <tier>` on the file the API actually wrote. Magic-byte check catches mismatches (e.g., `.mp4` URL that served a JPEG). Blocks PACKAGE on any violation.
3. Update `games/<game>/.find-media/used_assets.jsonl` via `scripts/dedup_tracker.py --record`.
4. Append to `games/<game>/.find-media/run_manifest.json` (schema in `templates/run_manifest.schema.json`).

**Why check format AFTER download, not before**: the API decides the saved extension from the source, not from your request. A `.jpg` TOML pointer with a `.webm` source URL → the API saves `.webm`. The generator's extension-agnostic lookup still finds it. So FORMAT MISMATCH warnings during PLAN are advisory — the post-download check is what matters.

**Iteration is safe**: when `game` is provided, the API deletes any existing file with the same stem before writing (regardless of extension). Re-downloading with a better source silently replaces the previous file. No orphan `_1` suffix files, no manual cleanup.

## Subagent dispatch

Spawn subagents with focused briefs per Anthropic's multi-agent guidance — objective, output format, tool guidance, task boundaries. Vague briefs cause duplicate work. **SFW retrieval no longer uses a per-source subagent** — run WebSearch inline on the main thread (see §RETRIEVE). The table below is the current set.

| Subagent | Objective | Output format | Tool guidance | Boundaries |
|----------|-----------|---------------|---------------|------------|
| `query-rewriter` | Read narrative context + raw queries, produce ranked rewrites | JSON list `[{query, rank, reason}]` | Read, validate_queries.py | Don't search, don't invent facts |
| `nsfw-harvester` | Run harvest script for 3–5 items | Paths to `/tmp/nsfw_previews/<item>/` | Bash (node nsfw_harvest.js) | Never edits scoring — that's EVALUATE |
| `candidate-evaluator` | View the CLIP montage, score, pick winner | `{winner_id, score, rubric_breakdown}` | Read (the montage JPG), dedup_tracker.py | CLIP pre-ranked the tiles; reject hard-fails and **judge the act yourself** |
| `fail-triage` | Diagnose why no candidate passed | `{diagnosis, delta_queries, retry_source}` | Read (TOML), sequential-thinking if available | Only spawned after first RETRIEVE fails |

## Evidence and persistence

Every phase writes to `games/<game>/.find-media/`:

```
.find-media/
├── scope/<item_id>.md                   # SCOPE output
├── evidence/<item_id>/
│   ├── candidates.jsonl                 # all harvested candidates
│   ├── scores.jsonl                     # scored candidates
│   └── decisions.jsonl                  # picks + rejections + reasons
├── used_assets.jsonl                    # dedup tracker state
└── run_manifest.json                    # final summary
```

To resume a crashed run: re-invoke the skill on the same game. It reads `scope/` and `evidence/` and skips items that already have decisions.

## Stop conditions

Hard limits — never exceed:
- **3 critique cycles per item** (counted in `decisions.jsonl`)
- **10 total query variations per item** across all cycles
- **Skip items marked `[FAIL]` twice in the run_manifest** — don't infinite-loop on cursed items

When hitting a stop condition, always surface the best-below-threshold candidate with its score. Silent failures waste human debugging time.

## Execution rule — always foreground, never background

**Run all commands in the foreground.** Do NOT use `run_in_background=true` on any Bash call within this skill.

Reasons:
- **Harvest → evaluate is interactive.** `scripts/nsfw_harvest.js` writes thumbnails to `/tmp/nsfw_previews/`; you immediately View them with the Read tool to score. Backgrounding the harvest means you can't evaluate until you poll for completion — wasted round-trips.
- **Tor failures surface late.** A backgrounded harvest that hits a dead Tor circuit silently returns empty results. Foreground execution shows the error output in the same step.
- **PornHub video URLs expire in ~4 hours.** If a harvest runs in the background and you move on to other work, the video URLs in `/tmp/nsfw_previews/*/*.json` may be dead by the time you return to evaluate.
- **The critique loop needs stdout.** CRITIQUE phase reads harvest output (candidate counts, error messages) to decide delta-queries. Background tasks hide that.
- **API downloads are fast.** `curl` to `/api/v1/dev/media-capture` is typically under 5 seconds per item. No benefit to backgrounding.

The only command that could legitimately background is `tor &` itself (the daemon) — and that's a one-time setup step the user runs, not something find-media orchestrates.

If a harvest batch is too slow for foreground execution, the fix is **smaller batches** (already capped at 5), not background execution.

## Quality gates

Before PACKAGE, three gates must pass:
1. `tier_format_check.py` — format matches tier (t5+ MUST be .webm/.mp4/.gif, never JPG)
2. `dedup_tracker.py` — GIF ID not used in this game (and not in global used set if `--strict-dedup`)
3. File size check — images > 1KB, videos > 50KB

Failing any gate drops the candidate back to EVALUATE with an explanation, not to RETRIEVE. The candidate was evaluated visually — the problem is the file, not the query.

## Progressive disclosure

Load additional context on demand:
- Running SFW batch → read `references/sfw_pipeline.md`
- Running NSFW batch → read `references/nsfw_pipeline.md`
- Pre-ranking candidates with CLIP, building a montage, or extracting video frames → read `references/clip_preranking.md`
- Deciding SFW vs NSFW, or handling a missing/wrong tier tag (the audit + retag) → read `references/content_rating.md`
- Writing or validating a query, or synthesizing queries for empty `search_queries` → read `references/query_rewriting.md`
- Scoring candidates → read `references/scoring_rubric.md`
- Something broke and you need to debug a site → read `references/playwright_diagnostic.md`
- Confused about why the API saved a different extension than the TOML asked for → read `references/api_behavior.md`
- Confused about what fields the game-review API returns, or need the full `missing_media` entry schema → read `references/game_review_api.md`

Don't load all nine upfront. The router above is enough to start.
