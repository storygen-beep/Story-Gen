# Stages 03 — Image Finder Prompt (port)

**Status:** LLM-consumed pipeline prompt. Post-TOML media stage.
**Replaces:** `prompts/image_finder_prompt.md` (33KB / 748 lines, 2026-03-21). Technical pipeline preserved verbatim; legacy game references replaced with prompts_v2 doctrine cites + RTS-shape examples.
**Input:** TOML file from Stage 2 (`stages/02_toml_generation_prompt.md`) OR explicit JSON query file.
**Output:** image + video files written to `games/{game}/output/videos/` per canvas image block.

This is a media fetcher, not an authoring prompt. It scrapes images (SFW: search engines) + video clips (NSFW: PornHub GIFs via Tor + Playwright) and writes them to disk for the build pipeline to package.

---

## §0 — How this fits into the prompts_v2 pipeline

Per `doctrine/05_rts_flat_prose.md` §2 Rule 8 — **image-first composition.** The visual asset (image / video) carries the scene; prose is the ≤ 30-word caption. Without media, scenes look incomplete; the placeholder visibility IS the missing-image signal (Rule 8 explicit). This stage closes that loop.

Per `schema/02_toml_schema.md` §7.2 — every canvas authors `[image]` / `[video]` block types with:
```toml
{ type = "image", props = { file = "scenes/<slug>.jpg", description = "<for image search>", search_queries = ["query 1", "query 2"] } }
```

The `description` + `search_queries` fields drive this stage's media fetch. Stage 2 (`stages/02_toml_generation_prompt.md`) emits the `search_queries` per canvas per the design book's per-canvas image notes; this stage takes that input and downloads the actual files.

---

## §1 — Invocation modes

### Mode A — JSON query file

Given a JSON file with explicit queries:

```json
{
  "game": "<game_slug>",
  "output_dir": "games/<game_slug>/output",
  "content_rating": "sfw",
  "queries": [
    {
      "file": "videos/activities/scene_name.jpg",
      "description": "Human-readable description of what the media should depict",
      "search_queries": ["search term 1", "search term 2"],
      "type": "image",
      "canvas": "canvas_id",
      "tier": "base"
    }
  ]
}
```

### Mode B — Direct game name

Given just `"Find missing media for <game_slug>"`. Auto-discover missing media via the game-review API.

**Prerequisites:** Django dev server running on `localhost:8000`. Game must have a final-stage TOML at `games/<game_slug>/toml_phases/<N>_final_game.toml`.

**Step 1:** Call API:
```bash
curl -s http://localhost:8000/api/v1/dev/game-review/load?game=<game_slug>
```

**Step 2:** Extract `missing_media` array from the JSON response. Each entry maps to the query format above.

**Step 3:** Infer tier + content_rating from filename:
```
{name}_t{N}.{ext}  → tier = "t{N}"
{name}_base.{ext}  → tier = "base"
{name}.{ext}        → tier = "base"
```

Content rating from tier:
```
base, t2, t3       → SFW
t4, t5, t6, t7, t8 → NSFW
```

---

## §2 — Tier system

| Tier | Rating | Media Type | Description |
|---|---|---|---|
| base, t2, t3 | SFW | image (.jpg) | Domestic, flirtatious, clothed |
| t4 | Borderline | image (.jpg) OR `.gif`/`.webm` | Kissing, suggestive, partial nudity |
| t5, t6 | NSFW | video (`.webm` / `.mp4` / `.gif`) | Explicit sex scenes |
| t7, t8 | NSFW | video | Graphic / specific acts |

### Format enforcement (HARD RULES)

| Tier | REQUIRED Format | Min File Size | Fallback to JPG? |
|---|---|---|---|
| base, t2, t3 | `.jpg` static image | > 1KB | N/A |
| t4 | `.jpg` OR animated clip | > 1KB | Acceptable |
| t5, t6 | `.webm` / `.mp4` / `.gif` animated | > 50KB | **NEVER** |
| t7, t8 | `.webm` / `.mp4` / `.gif` animated | > 50KB | **NEVER** |

**HARD RULE:** if tier is t5+ and the only available asset is a static JPG thumbnail, report **FAIL** — do NOT save the thumbnail. A 10KB static screenshot is useless as a video placeholder. Real PornHub GIF clips are 100KB–4MB animated `.webm` files lasting 2–10 seconds.

---

## §3 — Query validation (CRITICAL before searching)

Before downloading anything, validate EVERY search_query against the actual narrative in the TOML. Bad queries waste time downloading wrong content.

### Validation procedure

1. Open the TOML at `games/<game_slug>/toml_phases/<N>_final_game.toml`
2. For each missing media item, find its block by matching `file = "<filename>"`
3. Read the 2–3 paragraph/dialog blocks BEFORE and AFTER the media block — this is the narrative context
4. Check each search_query against the §3.1 checklist
5. Output a validation report (§3.4) before proceeding

### §3.1 — Validation checklist

| Check | What to look for | Example problem → fix |
|---|---|---|
| **Wrong action** | Query says one act but narrative describes another | Narrative: "your hand wraps around him" = handjob. Query: "blowjob" → fix to "handjob" |
| **Wrong direction** | "manual"/"hand job" but narrative says HIS hand on HER | Narrative: "his hand finds you" = fingering. Query: "manual stimulation" → fix to "fingering" |
| **Banned words** | Query contains words PornHub ignores (§5.2) | "passionate fuck wall urgent" → "sex wall hallway standing" |
| **Tier mismatch** | t2/t3 (SFW) query uses sexual terms | t3 query: "sexual tension dinner" → "couple dinner eye contact" |
| **Vague terms** | "manual stimulation", "oral" (direction?), "foreplay" | "oral kitchen" → "blowjob kitchen kneeling" or "cunnilingus kitchen" |
| **Missing setting** | Narrative names a location but query omits it | Narrative: "kitchen counter" / Query: "fingering morning" → "kitchen counter fingering morning" |

### §3.2 — Action vocabulary (use these exact terms)

- `fingering` = his hand on/in her (NOT "manual stimulation", "manual", or "hand job")
- `handjob` = her hand on him (one word, NOT "hand job")
- `blowjob` = her mouth on him
- `cunnilingus` = his mouth on her (or "eating out")
- `sex` / `fuck` = penetration (add position: missionary, doggy, riding, standing)

### §3.3 — Per-NPC vocab ceiling alignment (prompts_v2 specific)

Per `doctrine/08_kink_vocab_ceilings.md` — each NPC has a declared vocab ceiling. Cross-check search queries against the NPC's ceiling row:

- **Frank — FULL DADDY:** search queries can include "daddy" / "older man" / "salt and pepper" / "paternal" registers
- **Jake — FULL INCEST CALLOUTS:** queries can include "stepbrother" / "sister" / "incest" / "taboo" framing
- **Diana — FULL CUCKOLD:** queries for brought-in branch include "cuckold" / "wife watches" framings
- **Marge / Cookie (Phase 3+ deferred):** NO sexual queries in slice — ceiling row blank means out-of-scope

If a search query escalates beyond the NPC's ceiling, it shouldn't fire. Cross-check tier × NPC at validation time.

### §3.4 — Validation report

Output before proceeding to download:

```
=== Query Validation Report ===
Checked {N} items against TOML narrative.

⚠️ FLAGGED ({N} items need query fixes):

| # | File | Tier | Current Query | Issue | Fixed Query |
|---|------|------|--------------|-------|-------------|
| 1 | scene_frank_walks_in_shower_t6 | t6 | "manual stimulation kitchen" | Vague + solo trap. Narrative: "his hand makes you forget" = fingering. "fingering" alone returns solo/lesbian | "men fingering girl kitchen counter" |
| 2 | scene_franks_bedroom_climax_t5 | t5 | "blowjob couch night" | Wrong action. Narrative: "your hand wraps around him" = handjob | "couch handjob couple night" |

✅ OK ({N} items — queries match narrative)
```

If there are flagged items, use the FIXED queries (not the original TOML queries) for all subsequent searching. Do NOT search with a query you've identified as wrong.

---

## §4 — SFW Pipeline

### §4.1 — Sources

- DuckDuckGo image search (primary)
- Unsplash, Pexels, Pixabay (direct URL search)

### §4.2 — Search strategy

Use WebSearch. Try each `search_queries` entry in order, with enhancements:

**For activity scenes (2 people — Lane 1 hub / Lane 4 capstone):**
- Always add "couple" or "two people" to the query
- Add "at home" or "domestic" for home-based scenes
- Example: `"casual lunch kitchen"` → `"couple having casual lunch at home kitchen two people"`

**For location scenes (no people — `[[locations]]` entries):**
- Add "interior wide angle" or "room view"
- Add "empty" or "no people" to avoid lifestyle shots
- Example: `"home garage interior"` → `"home garage interior wide angle room view empty"`

**For object/mood shots (0 people — sidebar item icons / location detail):**
- Add "close up" or "detail shot"
- Example: `"morning coffee"` → `"two coffee mugs morning light close up kitchen counter"`

### §4.3 — SFW hard rejection filters

If ANY of these fail, the image scores 0 and is skipped:

**People count filter (CRITICAL):**
- Activity scenes (canvas slug starts with `activity_` OR `scene_`): MUST show exactly 1 or 2 people
- REJECT 3+ people, families, groups, children, crowds
- Images with 0 people acceptable ONLY for object/food close-ups

**Setting filter:**
- Must match the described setting (kitchen, porch, couch, etc.)
- "home kitchen" = HOME, not a restaurant
- Location queries need ROOM shots, not close-ups of objects

**Style filter:**
- REJECT overly staged/kitschy, corporate/commercial, AI-generated
- PREFER natural, candid-looking lifestyle photography

### §4.4 — SFW scoring

- **Relevance** (0–100): matches description and setting?
- **Mood** (0–100): intimate, warm, domestic feel?
- **Composition** (0–100): well-framed, good resolution, usable as game scene?
- **Overall:** average of three scores. Minimum **70** to auto-accept.

### §4.5 — SFW download

- Download with curl or wget to `{output_dir}/{file}`
- Create parent directories with `mkdir -p`
- Verify file exists and is > 1KB

### §4.6 — SFW rules

1. SFW only — skip any NSFW results
2. No watermarks — avoid visible watermarks or stock overlays
3. Realistic style — photographic over illustrations
4. Respect copyright — prefer Unsplash, Pexels, Pixabay, Creative Commons
5. Don't hallucinate URLs — only use URLs found via actual search
6. Rate limiting — 1–2 seconds between searches
7. People count is sacred — 2-person game, 3+ people = ALWAYS wrong
8. Room shots for locations — wide angle showing the space

---

## §5 — NSFW Pipeline

### §5.1 — ⚠️ TWO-PHASE PROCESS (DO NOT SKIP)

The NSFW pipeline has TWO mandatory phases that CANNOT be combined into one automated script:

1. **Search Phase (script):** run Playwright + Tor + PornHub GIF search to harvest thumbnails + video URLs for 10+ candidates per item
2. **Evaluation Phase (visual):** YOU view each thumbnail with the Read tool, score it against §5.4 criteria, pick the highest above 60%

**DO NOT** write a script that auto-selects the first candidate.
**DO NOT** batch-process all items in one script run without evaluating between items.

The script ONLY harvests candidates. YOU evaluate by viewing thumbnails.

**Process items in small groups (3–5 at a time):**
1. Run harvest script for 3–5 items → thumbnails saved to `/tmp/nsfw_previews/{name}/`
2. VIEW all thumbnails for those items → score and pick winners
3. Download winning videos
4. Move to next group

### §5.2 — Prerequisites

**Tor (required for network access to adult sites):**
```bash
brew install tor   # one-time
tor &              # start daemon
# Verify
curl --socks5-hostname 127.0.0.1:9050 https://check.torproject.org/ 2>/dev/null | grep -o "Congratulations"
```

If Tor stuck:
```bash
kill -HUP $(pgrep tor)              # new circuit
kill $(pgrep tor) && sleep 2 && tor &   # full restart
```

**Playwright + Chromium:**
```bash
cd /tmp && npm install playwright
cd /tmp && npx playwright install chromium
```

**ffmpeg (for video verification):**
```bash
brew install ffmpeg
```

### §5.3 — Harvest script (single-page extraction)

Save as `/tmp/nsfw_harvest.js`:

```javascript
// nsfw_harvest.js — FAST HARVEST. Extracts thumbnails + video URLs from search page only.
// Edit the QUERIES array per batch (max 3-5 items per run).

const { chromium } = require('playwright');
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const PREVIEW_DIR = '/tmp/nsfw_previews';

// ============ EDIT THIS FOR EACH BATCH ============
const QUERIES = [
  { name: 'example_scene', search: 'kitchen+counter+sex', desc: 'Sex on kitchen counter' },
];
// ==================================================

async function harvestFromSearchPage(page, search) {
  await page.goto(
    `https://www.pornhub.com/gifs/search?search=${search}`,
    { waitUntil: 'domcontentloaded', timeout: 45000 }
  );

  // Dismiss age gate if present
  try {
    const btn = await page.$('button:has-text("I am 18 or older")');
    if (btn) { await btn.click(); await page.waitForTimeout(3000); }
  } catch (e) {}

  await page.waitForTimeout(8000);

  // Extract ALL data from search results in one shot
  return await page.evaluate(() => {
    const data = [];
    const seen = new Set();
    const gifLinks = document.querySelectorAll('a[href*="/gif/"]');

    for (const a of gifLinks) {
      const m = a.href.match(/\/gif\/(\d+)/);
      if (!m || seen.has(m[1])) continue;
      seen.add(m[1]);

      const gifId = m[1];
      const title = (a.textContent || '').trim().substring(0, 80);
      const parent = a.closest('li, div');
      const video = parent ? parent.querySelector('video') : null;

      let thumbnail = null;
      let videoUrl = null;
      if (video) {
        thumbnail = video.getAttribute('data-poster') || video.poster || null;
        videoUrl = video.getAttribute('data-webm') || video.getAttribute('data-mp4') || null;
        if (thumbnail && thumbnail.startsWith('data:')) thumbnail = null;
      }

      if (thumbnail || videoUrl) {
        data.push({ gifId, title, thumbnail, videoUrl });
      }
      if (data.length >= 15) break;
    }
    return data;
  });
}

(async () => {
  fs.mkdirSync(PREVIEW_DIR, { recursive: true });

  const browser = await chromium.launch({
    headless: true,
    proxy: { server: 'socks5://127.0.0.1:9050' }
  });
  const page = await browser.newPage();

  for (const q of QUERIES) {
    console.log(`\n=== ${q.name}: "${q.desc}" ===`);
    const subdir = path.join(PREVIEW_DIR, q.name);
    if (fs.existsSync(subdir)) fs.rmSync(subdir, { recursive: true });
    fs.mkdirSync(subdir, { recursive: true });

    const results = await harvestFromSearchPage(page, q.search);
    console.log(`Found ${results.length} candidates with thumbnails+video URLs`);

    for (let i = 0; i < results.length; i++) {
      const r = results[i];
      if (!r.thumbnail) continue;

      const thumbPath = path.join(subdir, `${i}_${r.gifId}.jpg`);
      try {
        execSync(
          `curl -s --socks5-hostname 127.0.0.1:9050 -o "${thumbPath}" "${r.thumbnail}" --max-time 10`,
          { timeout: 15000 }
        );
        const size = fs.statSync(thumbPath).size;
        if (size < 500) { fs.unlinkSync(thumbPath); continue; }
      } catch (e) { continue; }

      fs.writeFileSync(
        path.join(subdir, `${i}_${r.gifId}.json`),
        JSON.stringify({ id: r.gifId, title: r.title, videoUrl: r.videoUrl || '', thumbnail: r.thumbnail })
      );

      // Download video immediately (URLs expire in ~4 hours)
      if (r.videoUrl) {
        const videoPath = path.join(subdir, `${i}_${r.gifId}.webm`);
        try {
          execSync(
            `curl -s --socks5-hostname 127.0.0.1:9050 -o "${videoPath}" "${r.videoUrl}" --max-time 30`,
            { timeout: 35000 }
          );
          const vSize = fs.statSync(videoPath).size;
          console.log(`  [${i}] ${r.gifId} "${r.title}" — ✓ ${(vSize/1024).toFixed(0)}KB`);
        } catch (e) {
          console.log(`  [${i}] ${r.gifId} "${r.title}" — ✗ video download failed`);
        }
      } else {
        console.log(`  [${i}] ${r.gifId} "${r.title}" — ✗ no video URL`);
      }
    }

    await page.waitForTimeout(1500);
  }

  await browser.close();
  console.log(`\n=== HARVEST COMPLETE ===`);
  console.log('NEXT STEP: View EVERY thumbnail with the Read tool.');
  console.log('Score each against §5.4 criteria. Pick the highest above 60%.');
  console.log('DO NOT auto-pick. DO NOT skip evaluation.');
})().catch(e => console.error('FATAL:', e.message));
```

Run with `node /tmp/nsfw_harvest.js`.

### §5.4 — NSFW evaluation criteria

**Hard rejection filters (instant score = 0):**
- 3+ people visible (groups, threesomes) → REJECT (unless tier-specific threesome scene)
- Solo only (no couple interaction) → REJECT
- Same-sex couple when scene requires M/F → REJECT (and vice versa for lesbian scenes if applicable)
- BDSM/bondage (ropes, paddles, gags, restraints) when scene doesn't call for it → REJECT
- Interracial when game character description doesn't match → REJECT
- Mature/MILF (visibly 40+) when game character is young → REJECT
- Cosplay/costumes/uniforms when scene is casual/domestic → REJECT

**Scoring (0–100):**

| Criterion | Weight | Check |
|---|---|---|
| Setting match | 30% | Visible environment matches description (kitchen/couch/pool/etc) |
| Action match | 40% | Sexual activity matches (oral/doggy/missionary/counter sex/etc) |
| Appearance match | 20% | Default: matches game character description. POV / anonymous male preferred. |
| Quality | 10% | Resolution, framing, lighting. Watermarks acceptable (placeholders). |

**Minimum score: 60** to accept. If nothing scores above 60 after 10 query variations, report FAIL with the best candidate details.

### §5.5 — Step-by-step NSFW workflow

For each NSFW query:

**Step 1: Build search query**
- Start with first entry in `search_queries`
- Enhance per §5.2 tips below

**Step 1b: Rewrite bad queries**
- Replace "manual stimulation"/"manual" → **"fingering"** (when narrative = HE touches HER)
- Replace "hand job" → **"handjob"** (one word) when narrative = SHE touches HIM
- Replace "oral" (ambiguous) → **"blowjob"** (her→him) or **"cunnilingus"** (him→her)
- Replace "fingering" alone → **"men fingering girl [setting]"** (prevents solo/lesbian results)
- Replace "cunnilingus" alone → **"guy eating out girl [setting]"**
- Remove banned words: passionate, intimate, tender, urgent, forbidden, emotional, seductive
- Apply setting-first formula: `[setting] + [specific act]`

**Step 2: Run harvest script** with the query → thumbnails + video URLs saved to `/tmp/nsfw_previews/{name}/`

**Step 3: Evaluate every thumbnail (MANDATORY)**
- View EACH downloaded thumbnail using the Read tool (you are multimodal)
- For each thumbnail, check hard rejection filters first
- Score survivors per §5.4
- Pick highest scoring above 60%
- If all below 60%, try next query variation (§5.6)
- DO NOT pick based on title alone — PornHub titles are user-generated garbage
- DO NOT write an auto-select script

**Step 4: Use the already-downloaded media**
- Videos downloaded during harvest (URLs expire ~4 hours)
- For `type: "image"` (tier t4 and below): the og:image thumbnail IS the final file. Save as `.jpg`.
- For `type: "video"` (tier t5+): the winning candidate's `.webm` should exist in harvest dir > 50KB

**Step 5: Verify download**
- Check file size: images > 1KB, videos > 50KB
- For t5+: verify NOT a static JPEG — `file <path>` must show WebM/MP4/GIF
- For video files, extract verification frame:
  ```bash
  ffmpeg -y -i {file} -ss 00:00:02 -vframes 1 -q:v 2 /tmp/verify.jpg
  ```
- View `/tmp/verify.jpg` to confirm content matches description

**Step 6: If no match, try next query variation** (§5.6). Up to **10 total variations** before FAIL.

### §5.6 — PornHub search query strategies

**CRITICAL: Setting-first queries**

PornHub search weights first keyword. Setting is the hard constraint:
- ALWAYS put setting word FIRST: `kitchen+blowjob` not `blowjob+kitchen`
- First 3 results are usually trending garbage; good matches at positions 4–10+. Need 10+ candidates.

**CRITICAL: Gender-direction queries for ambiguous actions**

PornHub's "fingering" category is dominated by solo girls + lesbian content. For any action that can be performed solo or same-sex, INCLUDE gender indicators:
- `men+fingering+girl+kitchen` NOT `kitchen+fingering`
- `guy+eating+out+girl+couch` NOT `couch+cunnilingus`

Actions that NEED gender direction:
- `fingering` → add `men` or `guy` + `girl`
- `cunnilingus` / `eating out` → add `guy` + `girl`
- `touching` / `rubbing` → add `man` + `woman` or `couple`
- `masturbation` → NEVER use this for M/F (it's inherently solo)

Actions that DON'T need it (inherently M/F):
- `blowjob`, `handjob` — implies M/F
- `sex`, `fuck`, `missionary`, `doggy`, `riding`, `bent over` — implies couple
- Add `couple` or `amateur` for quality filtering

**Words that WORK on PornHub:**
- Settings: `kitchen`, `couch`, `bathroom`, `pool`, `counter`, `table`, `shower`, `bed`
- Actions: `fuck`, `sex`, `blowjob`, `oral`, `riding`, `doggy`, `missionary`, `handjob`, `bent over`
- Body types: `petite`, `thick`, `curvy`, `slim`, `busty`
- Qualifiers: `amateur`, `homemade`, `pov`, `couple`

**Words that ADD NOISE (avoid):**
- Emotional: `passionate`, `tender`, `urgent`, `loving`, `intimate`, `sensual`
- Story: `morning`, `evening`, `first time`, `secret`, `lazy`
- Vague: `beautiful`, `gorgeous`, `perfect`, `hot`

**Query variation strategies (up to 10):**
1. Original query verbatim
2. SETTING + ACTION: `"kitchen blowjob"`
3. ACTION + SETTING reversed: `"blowjob kitchen"`
4. Add body position: `"bent over counter"`, `"riding on couch"`
5. Add POV: `"pov kitchen sex"`, `"pov blowjob"`
6. Simplify to action: `"missionary"`, `"cowgirl"`
7. Add amateur: `"amateur kitchen sex"`
8. Add body type: `"petite kitchen fuck"`
9. Describe the visual: `"girl on counter legs spread"`, `"girl kneeling kitchen"`
10. Broaden as last resort: drop setting, search just `"counter sex"`

### §5.7 — Error handling

| Error | Cause | Fix |
|---|---|---|
| Connection refused on 9050 | Tor not running | `tor &` and wait 15s |
| Playwright timeout | Tor circuit slow | `kill -HUP $(pgrep tor)` for new circuit |
| Empty search results | Query too specific | Broaden, try next variation |
| og:image returns null | Page structure changed | Try `<img>` tags instead |
| Video source not found | JS lazy-load | Wait + check `data-webm`/`data-mp4` attrs |
| Download 0 bytes | CDN rejected | Add referer: `curl -H "Referer: https://www.pornhub.com/" ...` |
| Download is HTML | Captcha redirect | New Tor circuit |

---

## §6 — Reporting format

For each query, report:

```
[OK]   {file} — downloaded from {source} (score: {score})
[SKIP] {file} — already exists
[FAIL] {file} — no suitable match after {N} query variations
[ERR]  {file} — download failed: {error}
```

Final summary:

```
=== Media Finder Summary ===
Total:      {n}
Downloaded: {n}
Skipped:    {n}  (already existed)
Failed:     {n}  (no match / download error)

Failed items:
  - {file} — suggested retry query: "{query}"
```

---

## §7 — Critical rules

1. **NEVER blind-pick** — ALWAYS preview thumbnails. First PornHub result is trending garbage.
2. **Couple only** — No groups, no solo. Two-person stories.
3. **Up to 10 query variations** before reporting FAIL.
4. **Use `--socks5-hostname`** (not `--socks5`) to route DNS through Tor.
5. **Don't hallucinate URLs** — only use URLs extracted from actual page navigation.
6. **Watermarks acceptable** for NSFW clips — these are placeholder assets.
7. **Rate limit** — 1–2 seconds between PornHub navigations.
8. **Verify every download** — images > 1KB, videos > 50KB. Use ffmpeg frame extraction for video.
9. **Default girl appearance** — matches game character description per `[player]` block.
10. **Always search GIFs** on PornHub — short clips (5–30s webm). Never search full videos.
11. **People count is sacred** — 2-person story. 3+ people = ALWAYS wrong.
12. **Settings matter** — Kitchen must look like a kitchen. Pool must show water.
13. **t5+ MUST be video/gif** — Static JPGs not acceptable for t5+.
14. **No duplicate GIF IDs** — Each game item uses a unique PornHub GIF. Track used IDs; skip previously-used.
15. **Per-NPC ceiling alignment** — cross-check tier × NPC vocab ceiling per `doctrine/08_kink_vocab_ceilings.md` before searching.

---

## §8 — Cross-references

### Sibling stages files

- `stages/01_game_book_prompt.md` — Stage 1 (design book authoring)
- `stages/02_toml_generation_prompt.md` — Stage 2 (TOML emission; provides `description` + `search_queries` per canvas)
- `stages/04_game_listing_prompt.md` — game listing blurb

### Doctrine cited

- `doctrine/05_rts_flat_prose.md` §2 Rule 8 — image-first composition (this stage closes the loop)
- `doctrine/08_kink_vocab_ceilings.md` — per-NPC vocab ceilings (cross-check at validation time)

### Schema cited

- `schema/02_toml_schema.md` §7.2 — image block schema (`{ type = "image", props = { file, description, search_queries } }`)

### Source

- `prompts/image_finder_prompt.md` — legacy port source (technical pipeline preserved verbatim with prompts_v2 framing adjustments)

---

**End of file.** Run media fetch per the §1 invocation modes. Validate queries per §3 before searching. Don't skip the two-phase NSFW process.
