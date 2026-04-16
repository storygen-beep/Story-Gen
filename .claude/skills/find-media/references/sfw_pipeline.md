# SFW Pipeline

For media items where tier is `base`, `t2`, `t3`, or `location`. Rated as SFW by content_rating inferred from tier. Output format is `.jpg` (unless the action is motion-worthy — see SKILL.md §Format classification).

## Batch shape

Same batch-as-pipeline-slice rule as NSFW (see SKILL.md §Batching). Group missing items in 5s and run each group through RETRIEVE → EVALUATE → CRITIQUE → PACKAGE before starting the next group. Don't bulk-retrieve all 50 items upfront.

SFW has no URL-expiration concern (Unsplash/Pexels links are durable), but the batch rule still applies because:
- Incremental progress: each batch's 5 files are packaged before you start the next
- Subagent token budget: parallel `sfw-searcher` dispatches scale per batch, not per total
- Failure isolation: if one item triggers 3 critique cycles, only the 5 items in that batch wait on it

## Source priority

Dispatch parallel `sfw-searcher` subagents — one per source — so results arrive concurrently rather than serial.

| Priority | Source | How to search | Notes |
|----------|--------|---------------|-------|
| 1 | DuckDuckGo images | WebSearch with query | Broad, good for lifestyle scenes |
| 2 | Unsplash | `site:unsplash.com <query>` via WebSearch | High-quality, Creative Commons, prefer for locations |
| 3 | Pexels | `site:pexels.com <query>` via WebSearch | Similar to Unsplash, different catalog |
| 4 | Pixabay | `site:pixabay.com <query>` via WebSearch | Fallback when 1–3 return nothing usable |

All four sources are attempted in parallel for the top-ranked query. Drop to sequential only if the first query failed everywhere — then try query #2 on Unsplash+Pexels first (highest signal for domestic scenes).

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

## Download

- `curl -L -o <output_dir>/<file>` — SFW sources don't need Tor
- Create parent directories with `mkdir -p`
- Verify file exists and is > 1KB before PACKAGE

## SFW-specific rules

1. **SFW only** — if a candidate shows nudity or explicit content, REJECT. SFW sources occasionally leak borderline content through tag mismatches.
2. **No watermarks** — avoid visible stock-agency overlays. These are placeholder assets for the game, not redistribution.
3. **Realistic style** — photographic over illustrations/3D renders. The game is grounded in realism.
4. **Respect copyright** — prefer Unsplash/Pexels/Pixabay/Creative Commons. Never pull from a portfolio site or artist's gallery.
5. **Don't hallucinate URLs** — only use URLs returned by actual WebSearch results.
6. **Rate limit** — 1–2 seconds between searches on the same source to avoid block.
7. **People count is sacred** — this is a two-person story. 3+ people = always wrong, no exceptions.
8. **Room shots for locations** — wide angle showing the space, not a single object.
