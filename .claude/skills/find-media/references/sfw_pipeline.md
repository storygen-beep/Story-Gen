# SFW Pipeline

For media items where tier is `base`, `t2`, `t3`, or `location`. Rated as SFW by content_rating inferred from tier. Output format is `.jpg` (unless the action is motion-worthy — see SKILL.md §Format classification).

## Batch shape

Same batch-as-pipeline-slice rule as NSFW (see SKILL.md §Batching). Group missing items in 5s and run each group through RETRIEVE → EVALUATE → CRITIQUE → PACKAGE before starting the next group. Don't bulk-retrieve all 50 items upfront.

SFW has no URL-expiration concern (Unsplash/Pexels links are durable), but the batch rule still applies because:
- Incremental progress: each batch's 5 files are packaged before you start the next
- Token budget: CLIP ranks the candidates and you view one montage per item (not 15 thumbnails) — the budget is montage reads, scoped per batch
- Failure isolation: if one item triggers 3 critique cycles, only the 5 items in that batch wait on it

## Source priority — inline WebSearch, no per-source subagents

Run WebSearch **inline on the main thread**. Do NOT spawn one `sfw-searcher` subagent
per source — that old fan-out (4 subagents per item) multiplied token cost with no
benefit now that CLIP does the ranking. You only need a modest pool of ~8–15 candidate
URLs for CLIP to rank; breadth no longer needs parallel agents.

| Priority | Source | How to search | Notes |
|----------|--------|---------------|-------|
| 1 | Unsplash | `site:unsplash.com <query>` via WebSearch | High-quality, Creative Commons, durable URLs, best for locations |
| 2 | Pexels | `site:pexels.com <query>` via WebSearch | Similar to Unsplash, different catalog |
| 3 | DuckDuckGo images | WebSearch with query | Broad, good for lifestyle scenes |
| 4 | Pixabay | `site:pixabay.com <query>` via WebSearch | CRITIQUE-only fallback when 1–3 return nothing usable |

Issue 2–3 inline queries (`<query>`, `site:unsplash.com <query>`, `site:pexels.com <query>`)
and collect candidate image URLs. Use the **validated top search query** as the text —
that same query becomes CLIP's caption (see `references/clip_preranking.md` §Caption policy;
the query beats narrative prose 60% vs 32%).

## Query enhancement by content type

### Activity scenes (2 people)

Always include people-count signal. PornHub is opposite — SFW searches default to solo lifestyle shots unless told otherwise.

- Add `couple` or `two people` to the query
- Add `at home` or `domestic` for home-based scenes
- Example: `casual lunch kitchen` → `couple having casual lunch at home kitchen two people`

### Location scenes (no people)

Stock sites tend to return either close-ups of single objects or lifestyle shots with people. You want the room itself.

- Add `interior wide angle` or `room view`
- Add `empty` or `no people` explicitly
- Example: `home garage interior` → `home garage interior wide angle empty no people`

### Object / mood shots (0 people)

- Add `close up` or `detail shot`
- Example: `morning coffee` → `two coffee mugs morning light close up kitchen counter`

## Hard rejection filters (instant score = 0)

Apply before any scoring. Drop these before they reach the visual evaluator.

**People Count Filter (CRITICAL)**
- Activity canvases (canvas_id starts with `activity_`): MUST show exactly 1 or 2 people
- REJECT 3+ people, families, groups, children, crowds
- Images with 0 people acceptable ONLY for object/food close-ups or locations

**Setting Filter**
- Must match the described setting (kitchen, porch, couch, etc.)
- "home kitchen" = HOME, not a restaurant
- Location queries need ROOM shots, not close-ups of objects

**Style Filter**
- REJECT overly staged/kitschy, corporate/commercial, obvious AI-generation artifacts
- PREFER natural candid-looking lifestyle photography

## SFW scoring

| Criterion | Weight | What to check |
|-----------|--------|---------------|
| Relevance | 40% | Matches description and setting |
| Mood | 30% | Intimate, warm, domestic feel |
| Composition | 30% | Well-framed, good resolution, usable as game scene |

**Minimum score: 70** to auto-accept. Below 70 → critique cycle.

## Download candidates BEFORE evaluation (CLIP needs files on disk)

Unlike the old flow (which only curled the winner at PACKAGE), CLIP scores local
files — so download every candidate URL into the item's evidence dir first:

```bash
mkdir -p games/<game>/.find-media/evidence/<item>/candidates
# for each candidate URL, zero-padded index cNN:
curl -sL --max-time 15 -o games/<game>/.find-media/evidence/<item>/candidates/cNN.jpg "<url>"
# append {id, url, source, query_used, local_path} to evidence/<item>/candidates.jsonl
# skip any file < 1KB (same size floor as the quality gate)
```

These are small stock JPGs on durable URLs — downloading ~8–15 per item is the cheap
precondition for the token win. Then run `clip_shortlist.py --candidates-dir …` (see
`references/clip_preranking.md`); SFW uses `--top-k 5` (top-3 hit 88%).

## Package the winner

After you pick the winning tile from the montage, package it via the dev API exactly
as before (`POST /api/v1/dev/media-capture` — see SKILL.md §6 PACKAGE). SFW sources
don't need Tor. The `tier_format_check.py` + size gates still run post-download.

## SFW-specific rules

1. **SFW only** — if a candidate shows nudity or explicit content, REJECT. SFW sources occasionally leak borderline content through tag mismatches.
2. **No watermarks** — avoid visible stock-agency overlays. These are placeholder assets for the game, not redistribution.
3. **Realistic style** — photographic over illustrations/3D renders. The game is grounded in realism.
4. **Respect copyright** — prefer Unsplash/Pexels/Pixabay/Creative Commons. Never pull from a portfolio site or artist's gallery.
5. **Don't hallucinate URLs** — only use URLs returned by actual WebSearch results.
6. **Rate limit** — 1–2 seconds between searches on the same source to avoid block.
7. **People count is sacred** — this is a two-person story. 3+ people = always wrong, no exceptions.
8. **Room shots for locations** — wide angle showing the space, not a single object.
