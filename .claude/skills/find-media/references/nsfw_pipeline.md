# NSFW Pipeline

For media items where tier is `t4`, `t5`, `t6`, `t7`, or `t8`. Routing is Playwright + Tor + PornHub GIF search because adult sites block raw curl and standard WebSearch doesn't reach them.

This pipeline has TWO mandatory phases that cannot be combined into one automated script:

1. **Harvest phase (script)** — `scripts/nsfw_harvest.js` extracts 10–15 candidates per query, downloads thumbnails AND videos in one pass
2. **Evaluation phase (CLIP cull + visual judging)** — `video_frames.py` makes a representative still per clip, `clip_shortlist.py` culls 15→6 on **setting/people** (CLIP can't judge acts — 25–31%), you view the ONE cull montage and **judge the act yourself**, then verify the pick with a frame strip. See `references/clip_preranking.md`.

The script ONLY harvests. CLIP only culls. The visual act-judging is what picks the winner — skipping it is the #1 cause of bad matches.

**Hard cap: max 5 items per harvest batch.** The script enforces this at runtime and exits if `QUERIES.length > 5`.

**The 5-item batch is the unit of PIPELINE work, not just the unit of HARVEST work.** See SKILL.md §Batching for the full rule. Concretely:

- DON'T run the harvest 10 times back-to-back for 50 items, then start evaluating batch 1
- DO run one harvest (≤5 items) → evaluate those 5 → critique/refine failures → package the 5 → then start the next harvest

Reasons specific to NSFW:
- Harvest-to-evaluate gap stays under a few minutes → Tor circuit is still warm, anti-bot cookies are still valid
- If CRITIQUE needs a fresh harvest for a failing item, it runs against the same Tor circuit that just worked
- Each completed batch means 5 more files on disk + updated `run_manifest.json` — durable progress
- Token cost of viewing 5 thumbnails × ≤15 candidates per batch stays manageable

## Prerequisites

Verify these before processing any NSFW batch. If any fail, report to the user and stop.

**Tor daemon on port 9050**
```bash
# One-time install
brew install tor

# Start
tor &

# Verify (should print "Congratulations")
curl --socks5-hostname 127.0.0.1:9050 https://check.torproject.org/ 2>/dev/null | grep -o "Congratulations"

# New circuit (new exit node) — use when rate-limited
kill -HUP $(pgrep tor)

# Full restart if stuck
kill $(pgrep tor) && sleep 2 && tor &
```

**Playwright + Chromium**
```bash
# One-time
cd /tmp && npm install playwright
cd /tmp && npx playwright install chromium

# Verify
node -e "const {chromium} = require('playwright'); console.log('OK')"
```

**ffmpeg** — for verification frame extraction
```bash
brew install ffmpeg
```

## Why this pipeline

Adult sites block raw curl with JS anti-bot challenges. The only working approach:

- **Playwright** — real headless browser that executes JavaScript and passes anti-bot checks
- **Tor SOCKS5** — network proxy that reaches adult sites (your ISP/curl can't)
- **PornHub GIF search** — returns short clips (5–30s), not full videos. Always search `/gifs/search`, never `/videos/search`.
- **Thumbnail preview is mandatory** — PornHub search returns trending garbage at positions 0–3. Relevant setting-matched results are typically at positions 4–10+. Visual preview is non-negotiable.

**Performance note**: PornHub search result pages have `<video>` elements with `data-poster`, `data-webm`, and `data-mp4` attributes on each result. The harvest script extracts all candidate data from a **single page load** — no need to visit individual GIF detail pages. This drops Playwright page loads from 10+ per query to 1.

**Tor cold-start**: The first page load in a fresh Playwright browser through Tor is slowest (new circuit, no cookies, age gate). First item: 30–60s. Subsequent items: 10–20s. The script uses `waitUntil: 'domcontentloaded'` (not `networkidle`) to avoid cold-start timeouts — we only need DOM data, not ads/tracking.

## Step-by-step workflow

### Step 1 — Build and validate the query

Start with the first entry in `search_queries`. Run it through `scripts/validate_queries.py` first (this happens in PLAN phase, before RETRIEVE). The validator rewrites vague/banned terms deterministically.

Common rewrites the validator applies:
- `manual stimulation` / `manual` → `fingering` (when narrative shows he touches her)
- `hand job` → `handjob` (one word) — when narrative shows she touches him
- `oral` (ambiguous) → `blowjob` (her→him) or `cunnilingus` (him→her)
- `fingering` alone → `men fingering girl <setting>` — prevents solo/lesbian results
- `cunnilingus` alone → `guy eating out girl <setting>` — prevents lesbian results

If the validator flagged an unfixable query, surface it to the user. Don't run broken queries.

### Step 2 — Harvest candidates

Run `scripts/nsfw_harvest.js`. Edit the `QUERIES` array in the script header for the batch (**max 5 items — the script refuses to run with more**):

```javascript
const QUERIES = [
  { name: 'breakfast_ethan_t5', search: 'kitchen+counter+sex', desc: 'Sex on kitchen counter' },
  // ...
];
```

Execute: `node /Users/a0000/.../.claude/skills/find-media/scripts/nsfw_harvest.js`

**Foreground only.** Never run the harvest script with `run_in_background=true` — you need the stdout (candidate counts, Tor errors, per-item download status) to decide whether to proceed with evaluation or retry with a new Tor circuit. See SKILL.md §Execution rule.

The script writes to `/tmp/nsfw_previews/<name>/`:
- `{i}_{gifId}.jpg` — thumbnail
- `{i}_{gifId}.webm` — video (downloaded in-line because URLs expire in ~4 hours)
- `{i}_{gifId}.json` — metadata (id, title, videoUrl, thumbnail)

### Step 3 — CLIP coarse-cull → view ONE montage → judge the act (DO NOT SKIP the judging)

CLIP cannot judge NSFW acts (25–31% — see `references/clip_preranking.md`). It culls
garbage; **you** judge the act on the survivors.

1. **Rep frames** — a GIF loop has no meaningful poster, so make a representative still per clip:
   ```bash
   "${FIND_MEDIA_PY:-/Library/Frameworks/Python.framework/Versions/3.10/bin/python3}" \
     .claude/skills/find-media/scripts/video_frames.py \
     --videos-dir /tmp/nsfw_previews/<name> --mode rep --frames 3 \
     --out-dir /tmp/nsfw_previews/<name>/frames
   ```
   (exit 3 → ffmpeg missing → fall back to the harvested `.jpg` posters.)
2. **Dedup** — `dedup_tracker.py --check <gifId>` each; drop already-used before ranking.
3. **Coarse cull** — rank the rep frames with CLIP, caption on **SETTING + people, NOT the act**, keep top-6 (extra tile for margin, since CLIP's act-blindness can sink a good clip to rank 6):
   ```bash
   "${FIND_MEDIA_PY:-…python3}" .claude/skills/find-media/scripts/clip_shortlist.py \
     --candidates-dir /tmp/nsfw_previews/<name>/frames \
     --caption "<setting + people — e.g. 'a man and woman having sex on a kitchen counter'>" \
     --top-k 6 --item-id <item_id> \
     --montage-out games/<game>/.find-media/evidence/<item_id>/montage_cull.jpg --json
   ```
   (exit 3 → CLIP unavailable → fall back to viewing every `.jpg` directly, as before.)
4. **View the ONE montage** (`montage_cull.jpg`). Apply the hard-rejection filters from
   `references/scoring_rubric.md` (3+ people, solo, same-sex, BDSM, mature/MILF when the
   character is young, etc.) and **judge the act yourself** on each tile — the step CLIP
   can't do. Score Setting (30) + Action (40) + Appearance (20) + Quality (10); record
   every score to `evidence/<item_id>/scores.jsonl`. Pick the highest above 60; if all
   below 60, trigger CRITIQUE. Map the chosen tile letter back to its `gifId` via the
   `clip_shortlist.py` JSON `ranked[].montage_label`.

**Never pick based on title alone.** PornHub titles are user-generated noise.
**CLIP ranks, it does not score — you do.** The montage order is a hint, not the decision.

### Step 4 — Use the already-downloaded media

Videos were downloaded during harvest to avoid URL expiration (PornHub video URLs are signed with `validfrom`/`validto` params and expire in ~4 hours).

- For `type: image` (t4): the `.jpg` thumbnail IS the final file. Copy to the output path.
- For `type: video` (t5+): use the `.webm` from the harvest directory.
- If the video file is missing or < 50KB (download failed during harvest): re-run harvest for just that item, OR visit the GIF detail page directly and extract a fresh video URL:

```bash
# Write directly to the media root — same location the API would save to.
# See SKILL.md §Paths for the rule. Never target games/<game>/output/.
curl --socks5-hostname 127.0.0.1:9050 \
  -o "games/<game>/videos/<subfolder>/<file_stem>.webm" \
  "<VIDEO_URL>" \
  --max-time 30 \
  -H "Referer: https://www.pornhub.com/"
```

### Step 5 — Verify the download

- File size: images > 1KB, videos > 50KB
- For t5+ files: `file <path>` must show WebM/MP4/GIF, NOT "JPEG image data". If it's a JPEG at t5+, DELETE and report FAIL — a 10KB thumbnail is useless as a video placeholder.
- `scripts/tier_format_check.py --file <path> --tier <tier>` enforces this as a hard gate before PACKAGE.
- For videos, build a multi-frame act-verification **strip** (one frame can mislead — the act may not be at 00:00:02):

```bash
"${FIND_MEDIA_PY:-/Library/Frameworks/Python.framework/Versions/3.10/bin/python3}" \
  .claude/skills/find-media/scripts/video_frames.py --video <file> --mode strip --frames 4 \
  --out games/<game>/.find-media/evidence/<item_id>/verify_strip.jpg
```

View the strip to confirm the act holds across the loop and matches the description.
This supersedes the old single-frame `ffmpeg -ss 00:00:02 -vframes 1` check.

### Step 6 — If no match, CRITIQUE cycle

Max 10 total query variations per item, max 3 critique cycles. Variation strategies:

1. Original query verbatim
2. SETTING + ACTION: `kitchen blowjob`, `couch doggy`
3. ACTION + SETTING reversed: `blowjob kitchen`, `doggy couch`
4. Add body position: `bent over counter`, `riding on couch`
5. Add POV: `pov kitchen sex`, `pov blowjob`
6. Simplify to just action: `missionary`, `cowgirl`, `doggy style`
7. Add amateur: `amateur kitchen sex`, `homemade couch missionary`
8. Add body type: `petite kitchen fuck`, `thick doggy`
9. Describe the visual: `girl on counter legs spread`, `girl kneeling kitchen`
10. Last resort — drop setting: `counter sex`, `kitchen fuck`

## Error table

| Error | Cause | Fix |
|-------|-------|-----|
| Connection refused on 9050 | Tor not running | `tor &` and wait 15 seconds |
| Playwright timeout | Tor circuit slow | New circuit: `kill -HUP $(pgrep tor)` |
| Empty search results | Query too specific | Broaden query, try next variation |
| og:image returns null | Page structure changed | Open `references/playwright_diagnostic.md` — use Playwright MCP to find new selectors |
| Video source not found | JS lazy-load or anti-bot | Wait for video element + 3s, check data-webm/data-mp4 attrs. For t5+: never fall back to thumbnail — FAIL instead |
| Download is 0 bytes | CDN rejected request | Add referer: `curl -H "Referer: https://www.pornhub.com/" ...` |
| Download is HTML not media | Redirect to captcha | New Tor circuit: `kill $(pgrep tor) && sleep 2 && tor &` |
