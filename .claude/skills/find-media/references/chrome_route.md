# Chrome route — the only retrieval route

This is how media is found. There is no second route.

You drive the user's own Chrome — already logged in, SafeSearch already off, cookies
already warm. You never handle a login, never clear an age gate, never touch an account
setting. The old skill routed everything through Playwright + Tor + PornHub GIF search.
That route is gone.

**Why:** one Google query in the user's Chrome surfaced nine hosts the old route could never
touch. The fetchable corpus now stands at nine hosts gathered across queries — nsfwgify,
xgroovy, blovjob, porngif.co, hardcoregify, xgifer, sex.com, flashingjungle, eporner —
of which seven came off that single page (the other two results were phncdn, unfetchable,
and one uncharacterised host). (Exact host strings, and what each one serves, in
`media_sources.md` — use that one list, don't keep a second copy in your head.) The Tor
route only ever reached PornHub, and PornHub is not a fetch target at all. That single
source was the real ceiling, and no amount of query tuning was going to raise it.

**Snapshot-driven browser automation costs roughly 30× the tokens per action**, because it
ships an accessibility snapshot on every call. That is the whole argument for §4: you
extract Google's results with one JS regex instead of clicking through tiles.

> ### PornHub is DISCOVERY-ONLY — never queue a phncdn URL for download
> `egl.phncdn.com/gif/<id>.gif` returns **470 on clearnet AND over Tor**, every id tried. It
> is not a fetch endpoint. The real media URL, read off a gif page, has the shape
> `el2.phncdn.com/pics/gifs/<nnn>/<nnn>/<nnn>/<id>a.webm?validfrom=<ts>&validto=<ts>&ipa=1&hash=<sig>` —
> **signed, time-limited, IP-locked** — and our extraction strips query strings by
> construction (§4, and it must), which destroys the signature. `pornhub.com` itself is
> unreachable on clearnet from this machine (curl reports `000`).
>
> So: a PornHub-hosted Google result is worth **reading** — its title and tags are free
> vocabulary for §1. Read the word, log it, and **skip the URL as a candidate.**

**What you deliver per slot:** one installed best-guess pick, plus **≥6 stocked options**
in the options store for the human to flip through in the review UI (NSFW slots stock 12,
because the strip in §7 kills roughly half). You are a scout stocking a shelf, not a judge
handing down a verdict. Your job is not to prove a clip is hot with a number — it is to stop
discarding hot clips before the human sees them.

---

## 1. Word hunt — BEFORE you search

This step did not exist in the old skill. That absence is why the skill never found
`downblouse`.

The user needed a "leans forward, cleavage on show" tease beat. He found `downblouse` on
Reddit in about a minute. The skill had spent a run failing at it, because it had no step
that asked *what is this thing actually called* — it only had a step that rewrote the
sentence it was already holding.

**The trigger:** you can describe the beat in a sentence but you cannot NAME it in one
word. Stop. Hunt the word. A search built out of your own paraphrase inherits your own
blind spot.

### Where terms come from, ranked by measured yield

| Source | What it gives | How much to trust |
|---|---|---|
| **Google's own result labels + URLs** | The richest mine. Taught `dogging` (public/outdoor sex) and `back alley` this session, unprompted, while looking at an adjacent query. | Highest. Read the labels, not just the pictures — the text under the tiles is a free vocabulary feed. |
| **Community / subreddit names** | Vocabulary clusters. `downblouse` came from a Reddit community name. | Verify alive first. `r/OutdoorBlowjobs` is real but nearly dead — 2.2k weekly visitors, 4 posts/week. A named community is not a populated one. |
| **An LLM (Grok) asked about the scene** | Modifiers, and the names of communities. | Partial — see below. |
| General web search (`WebSearch`) | Nothing. Sanitized: encyclopedia entries and SEO spam. | Skip. Tried this session, wasted the call. |
| Reddit's anonymous JSON API | Nothing. Blocked. | Skip. Tried this session. |

### Using Grok correctly

Ask it about the scene, then take exactly two things: **(a) modifiers** and **(b) community
names**. **Ignore its headline "best search terms" list** — it paraphrases your own sentence
back at you as 4–5 token phrases, which return 0 results on PornHub's search and read as
mainstream on Google. Its value is lateral vocabulary, not query construction.

### Verify the word before you trust it

On **PornHub's own search**, count the bare word's pool before building anything on it:
`stockroom` alone returns 5 gifs; `stockroom blowjob` returns 37 — and those 37 are generic
blowjob, because the rare word was silently dropped from the compound. A compound query that
"works" can be lying to you about which of its words did the work. Bare word first, always.

### The lexicon is the output of this step

Every confirmed term goes to `games/<game>/.find-media/lexicon.md`, one line each:

```
downblouse | woman leaning forward, view down the top | reddit community name | PH bare-word pool: check before use
dogging    | public/outdoor sex, often with watchers   | google result label (unprompted) | reached 9 hosts on google
back alley | outdoor, urban, grimy, night              | google result label | pairs with `amateur`
```

Terms that prove out across more than one game get copied up to `games/.find-media/lexicon.md`.
This is the one part of a run that compounds — every future run starts with a bigger vocabulary
than this one did.

---

## 2. Browser tooling

**`tabs_context_mcp` first, always.** Call it once per session with `{createIfEmpty: true}`
before any other browser tool — every other tool needs a `tabId` and this is the only thing
that hands you one. Work in a **new** tab (`tabs_create_mcp`), not one the user is reading.

```
mcp__claude-in-chrome__tabs_context_mcp  { createIfEmpty: true }   → tab ids
```

| Tool | Used for |
|---|---|
| `navigate` | Go to the query URL. `tabId` optional standalone, **required inside `browser_batch`**. |
| `computer` `{action:"screenshot"}` | The contact sheet. Google's results grid already IS a contact sheet — one screenshot shows 20–40 tiles. |
| `javascript_tool` `{action:"javascript_exec", tabId, text}` | The workhorse: the URL extract (§4) and the options POSTs (§5). REPL semantics — the last expression is the return value, and top-level `await` works, so an inline `await fetch()` call is fine. |
| `browser_batch` | Collapse navigate + wait + screenshot into ONE round trip. |
| `computer` `{action:"scroll"}` | Force Google's lazy-loaded tiles in before extracting. |

**Do not call `read_page` or `get_page_text` on a results page.** Accessibility snapshots are
the entire reason the old Playwright MCP path cost ~30× the tokens per action. One regex over
`innerHTML` returns the same URLs — more of them, actually — in one call.

**Batch the predictable prefix.** Navigate, settle, screenshot is three round trips as three
calls and one as a batch:

```json
{"actions": [
  {"name":"navigate","input":{"url":"https://www.google.com/search?q=back+alley+blowjob+gif+amateur&tbm=isch","tabId":123}},
  {"name":"computer","input":{"action":"wait","duration":2,"tabId":123}},
  {"name":"computer","input":{"action":"screenshot","tabId":123}}
]}
```

Actions run sequentially and stop on the first error; batches cannot nest.

**Before you stock anything, confirm the Django dev server is up on `localhost:8000`** —
the in-page `fetch` in §5 is what makes the whole run durable, and it fails silently against
a dead server.

---

## 3. SEARCH — query construction for Google

Google is not PornHub search, and the two dialects are **opposites**. Do not carry the PornHub
rules across (those live in `query_rewriting.md` and apply only to a site's own search box).

| Rule | Why |
|---|---|
| **Verbose is fine. Loose grammar is fine.** | `on kneel blowjob` worked. Google normalizes; it doesn't drop rare words the way a site search does. |
| **ZERO story or character words.** | Intent classification, not keyword dilution. One story word flips the entire result page out of porn. |
| **Add an anti-studio modifier when the beat is grimy:** `amateur`, `real`, `voyeur`, `hidden cam`. | The single most-repeated defect in this game's history is bright studio lighting on a beat that wanted squalor. This is the first systematic fix for it. |
| **Append `gif` or `webm`. NOT optional — this is the highest-leverage token in the query.** | Measured 3×, same query ± one token: **7→59, 1→54, 0→91** fetchable urls. All six pages carried ~200 tiles either way: without the token Google serves **stills**, and the §4 extractor only matches `gif\|mp4\|webm`, so a full-looking grid harvests as ~nothing. A single-digit extract off a rich grid means this token is missing — check it before rewriting anything else. Full table: `query_rewriting.md` §Google dialect. |
| **Spend words on setting ONLY when setting carries meaning** (danger / secrecy / squalor) — **and cap it at ~2 setting tokens.** | For one beat the user said the setting "doesn't matter much here"; for a dark alley he rejected bright clips twice, because the darkness carried the danger. But `back alley sex at night streetlight gif real` returned **Shutterstock and Getty stock footage of empty streets** — stacking place+time+light words reclassifies the query as stock photography. Name the place once and stop. |
| **Run 2–3 sibling queries per slot, never one.** | Different phrasings land on different host clusters. One query surfaced nine hosts; a second reaches a partly different set. This is how you get to ≥6 stocked options. |

**The measured failure:** `back alley blowjob gif drunk guy night` returned Reddit movie
stills, Facebook, and TikTok. `drunk guy` reclassified the whole query as mainstream. The
query was not too long — it had a character in it. `back alley blowjob gif amateur`, the same
length, worked.

**Shape:** `<act> <position> [setting-if-load-bearing] [anti-studio modifier] gif`

**The URL:** build it as `https://www.google.com/search?q=<url-encoded terms>&tbm=isch`, then
**confirm from the screenshot that you are on the image grid**, not the web tab. If you see a
list of blue links instead of tiles, click the Images tab before extracting — the extract in
§4 returns almost nothing from the web tab and you'd wrongly conclude the query was dead.

---

## 4. Extraction — one regex, one call

Google's result-page HTML carries the **original CDN URLs**. The thumbnails you see rendered
are Google's own re-encodes, but the source URLs are sitting in the markup. That is why one
regex beats clicking every tile: no snapshots, no per-tile navigation, and you get the real
file instead of a 200px Google thumbnail.

```js
[...new Set(
  (document.documentElement.innerHTML.match(/https?:\/\/[^"'\\\s]+?\.(?:gif|mp4|webm)/gi) || [])
    .map(u => u.split('?')[0])
)]
```

Measured: **54 direct URLs from one call** on a single query.

**Strip the query strings — `u.split('?')[0]` is not optional.** The browser JS tool blocks
results carrying query-string data. Un-stripped, you get a refusal, not a truncated list, and
the failure reads exactly like "the page had nothing on it." This is also, structurally, why
PornHub can't be fetched from here: its media URL keeps its signature in the query string, so
the extract that makes every other host work is the same extract that kills that one.

**Group by host** so you can see what you actually reached, and cull page furniture:

```js
const urls = [...new Set((document.documentElement.innerHTML
  .match(/https?:\/\/[^"'\\\s]+?\.(?:gif|mp4|webm)/gi) || []).map(u => u.split('?')[0]))];
const by = {}; urls.forEach(u => { const h = new URL(u).host; (by[h] ||= []).push(u); });
Object.entries(by).map(([h, v]) => `${v.length}  ${h}`).sort().reverse()
```

- Keep the original CDN hosts — that's the candidate pool (nsfwgify, xgroovy, blovjob,
  porngif.co, hardcoregify, xgifer, sex.com, flashingjungle, eporner). All nine answer 200
  on clearnet: no Tor, no signing, no expiry. Exact host strings — some are subdomains,
  e.g. `public.flashingjungle.com`, `i.xgroovy.com` — in `references/media_sources.md`;
  match on the registrable domain, not the full host, or a filter misses half of them.
- **Cut every `*.phncdn.com` URL before you stock anything.** They are not fetchable (see
  the box at the top of this file), so stocking one puts a guaranteed-broken option on the
  human's shelf:

  ```js
  const pool = urls.filter(u => !/phncdn\.com$/i.test(new URL(u).host));
  ```

- `gstatic` / `googleusercontent` entries are Google's re-encoded thumbnails. Fine as a
  preview, **never as the installed file** — they're small and they expire.
- Anything from an analytics or Chrome-UI host is furniture. Drop it.
- **Require a real path**, e.g. `new URL(u).pathname.length > 4`. The regex happily matches
  the bare string `www.gif` inside page text, yielding a url with an empty path that stocks
  as a permanently-dead option.
- A host outside the nine is **surfaced, not yet characterised**. Stock it and fetch it —
  the fetch sanity check in §6 tells you what it actually served. Don't assume behaviour
  for it in either direction, and don't skip it on suspicion.

**Scroll, then re-extract.** Google lazy-loads tiles. Scroll to the bottom, wait, run the
extract again, and compare counts — if the set didn't grow, the page was already fully loaded
and you've hit the pool's edge. That self-check costs one call and tells you whether to run a
sibling query.

---

## 5. STOCK — the step that keeps runner-ups alive

Under the old route you evaluated ~15 candidates, installed 1, and the other 14 died on
`/tmp`. Everything the human might have preferred was destroyed before he ever saw it. This
step is the fix, and it is the reason the whole skill changed shape.

**Stock ONCE, immediately after extraction, BEFORE you judge anything.** Stocking is free —
it's URLs, not bytes — and it is the only thing that makes runner-ups survive the judging
that follows. Nothing in §7 stocks; by the time you get there the shelf is already built.

POST every relevant candidate straight from the results page. Verified this session:
**54 of 54 accepted**, CORS fine, no proxy needed — the store takes whatever you hand it,
which is exactly why the phncdn filter in §4 has to run *before* this loop, not inside it.

```js
const GAME = 'vesper';
const FILE = 'scenes/alley_bj_t5.webm';          // the slot's TOML-declared path, verbatim
const urls = [ /* the host-filtered pool from §4 */ ];
const t0 = new Date().toISOString();             // keep this — the refetch prune needs it

const isVid = u => /\.(mp4|webm)$/i.test(u);
let ok = 0;
for (const u of urls) {
  const r = await fetch('http://localhost:8000/api/v1/dev/media-finder/options/add', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      game: GAME, file: FILE, url: u,
      type: isVid(u) ? 'video' : 'gif',
      media_kind: isVid(u) ? 'video' : 'img'
    })
  });
  if ((await r.json()).ok) ok++;
}
`${ok}/${urls.length}`
```

Rules, each with the reason it exists:

- **`file` is the slot's TOML-declared path, character for character.** It is the key the
  review UI reads. A typo stocks an orphan slot the human will never open.
- **`game` is a BODY field on every media-finder POST** (`options/add`, `options/clear`,
  `options/remove`, `grab`). It is a **query param** on `options/list`, which is a GET, and
  on all media-review endpoints. Sending it the wrong way returns
  `400 Invalid or missing game` — so read the method, don't reach for a rule of thumb.
- **`media_kind` is exactly `img` or `video`** — never `"image"`. It drives the preview
  widget: `.gif` → `img` (it animates inside an `<img>`); `.mp4` / `.webm` → `video`. The
  backend lowercases it and defaults to `img`, so a wrong value fails quietly and the option
  renders blank in the UI, which reads to the human as a dead candidate.
- **Dedup is by exact URL.** A repeat returns `{ok: true, duplicate: true}` and doesn't grow
  the list, so re-running a query is harmless.
- **≥6 options per slot is the floor** (12 on NSFW slots, where the strip kills about half).
  Counts are owned by SKILL.md §Modes; this restates them, it does not set them.
  A slot with 3 options is a slot the human can't actually choose in — it's a rubber stamp
  with extra steps. Short of the floor? Run another sibling query (§3) before you move on.
- **A refetch REBUILDS the shelf — but it STOCKS FIRST and PRUNES AFTER.** Take
  `t0 = new Date().toISOString()` before stocking, stock the new candidates, and only then:

  ```js
  await (await fetch('http://localhost:8000/api/v1/dev/media-finder/options/clear', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ game: GAME, file: FILE, before: t0 })
  })).json()
  ```

  `before` keeps every entry added at or after `t0` — your fresh shelf — and drops the
  stale ones. Entries with `origin: "previous"` (the slot's undo history: picks that were
  installed before) survive regardless.

  **Never clear on the way in.** A search that then comes back thin leaves the slot with
  nothing *and* the old candidates gone; wiping first once silently ate three harvests. And
  do not walk `options/list` → `options/remove` per URL as a substitute — that deletes the
  undo history along with the noise. Appending without any prune is the opposite failure:
  the human flips past clips he already rejected and stops trusting the shelf.

Ledger on disk: `games/<game>/.find-media/media_options.json`
(shape: `{game, updated_at, options: {<file>: [{url, type, media_kind, added_at}]}}`).

---

## 6. Fetching files — and INSTALL

### Installing the pick

Prefer the API — it derives the target path from the slot's declared `file`, so it cannot put
the file in the wrong place:

```bash
curl -sS -X POST http://localhost:8000/api/v1/dev/media-finder/grab \
  -H 'Content-Type: application/json' \
  -d '{"game":"vesper","file":"scenes/alley_bj_t5.webm","url":"https://<host>/<path>.webm","source":""}'
```

It re-derives the extension from the **source URL** (the TOML-declared extension is stripped
and ignored) and writes to `games/<game>/videos/<subfolder>/<stem>.<ext>`. It downloads to a
temp file first and only then swaps: the incumbent is demoted to an option
(`origin: "previous"`, which is why the refetch prune spares it), every same-stem file is
removed so the generator never sees an orphan it can't match, and the new file moves into
place. A dead URL therefore fails without emptying the slot.

### Path discipline

- **`games/<game>/videos/`** is the source of truth. Everything lands here.
- **`games/<game>/output/`** is the compiled copy, rewritten by packaging. A file written
  there survives until the next `package_from_toml` and then silently vanishes.
- The `file` / `scene_id` you pass is **relative to `videos/`** — `scenes/kiss`, not
  `videos/scenes/kiss` (that prefix is stripped for you), and **never**
  `output/videos/scenes/kiss` — `output/` is NOT stripped, and the file lands nested wrongly
  at `games/<game>/videos/output/videos/scenes/kiss.ext`.

### Getting the bytes down — `fetch_candidates.py`

The store holds URLs; JUDGE needs bytes. **Use the shipped script — do not hand-roll a
fetch loop.** Everything below was learned by hand-rolling one and getting it wrong; the
script has those lessons compiled in, so a fresh run starts where the last one finished
instead of rediscovering 403s and stall behaviour.

```bash
# WAVE 1 — the 8 best by slug rank
python3 .claude/skills/find-media/scripts/fetch_candidates.py \
  --game <game> --file 'scenes/alley_bj_t5.webm' \
  --want alley,night,outdoor,wall --avoid daylight,studio --top 8
```

It reads the slot's stocked URLs straight from `media_options.json`, ranks by slug, fetches
concurrently, applies fetch sanity, writes `NN.<ext>` plus `manifest.json`, and reports every
drop with a reason. Exit 0 ok / 1 nothing landed / 2 usage.

**Fetch in TWO WAVES — this is the default, not an optimisation.** The media_lab run
downloaded **144 files and frame-stripped 60**: the surplus existed only to pad a contact
sheet. So:

1. `--top 8` → sheet → apply the Gate-1/Gate-3 checks → strip the survivors.
2. Only if gate-survivors land **under the 6-option shelf floor**, top up with `--more`
   (skips what is already on disk, keeps numbering contiguous, never re-fetches a URL).
3. Still short after that? The problem is the *query*, not the shelf — run a sibling query (§3).

Easy slots stop at wave 1 and save ~40% of the bytes. Hard slots pay exactly what they always
paid — the alley slot finished with 3 survivors from 14 and would simply run wave 2. **Nothing
about the strip changes**: every animated finalist and every install is still stripped. This
trims fetching, never judging.

`--workers` defaults to **3** and should stay there — see the weather box below.
`--max-tries` (default 4×`--top`) stops the script walking a 140-deep shelf when the network
is broken; if it trips, the report says so.

> ### ⚠️ Network timing is WEATHER — never build rules from one day's numbers
> Every instinct here is wrong, and each was measured wrong on 2026-07-27/28:
> - **"These hosts are slow, deprioritise them."** The hosts measured at 30–44s were **1–2s**
>   an hour later. A blacklist built that afternoon would have permanently avoided good
>   sources for no reason. There is no slow-host list in this skill, deliberately.
> - **"Download in parallel, it'll be much faster."** These CDNs throttle concurrency: at 8
>   workers per-file time went **7.8s → 34.1s** for only ~1.5× total. Five benchmarks in one
>   afternoon disagreed (0.8× / 1.5× / 2.6×). Concurrency is a hedge against one stalled
>   straggler, **not** a speed feature.
> - **"Cap total download time to kill slow files."** A flat 20s cap threw away good clips:
>   `101534-sultry-bj-on-knees.gif` is 6.6 MB and takes **36.8s at 0.18 MB/s with a worst
>   chunk gap of 4.9s** — never stalled, just big. Kill **stalls** (`--timeout`, the socket
>   gate), not slowness; `--deadline` is a runaway backstop at 120s.
>
> If you measure something here and want to act on it, measure it again hours later first.

**Manual `curl`, single-file fallback** (the script is the route; this is for one-offs):

```bash
curl -sS -L --max-time 60 \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36' \
  -o /tmp/fm/<slot>/03.webm 'https://<host>/<path>.webm'
```

> ### ⚠️ NEVER send `Referer: https://www.google.com/` — it is hotlink protection bait
> You just came from a Google results page, so attaching a Google referer feels like the
> honest thing to do. It is the one header that breaks the fetch. Measured 2026-07-27:
>
> | Host | no referer | `google.com` referer | own-origin referer |
> |---|---|---|---|
> | `cdn.sexxxgif.com` | 200 | **403** | 200 |
> | `cdn.nsfwgify.com` | 200 | **403** | 200 |
> | `porngif.co` | 200 | **403** | 200 |
> | `cdn.xgifer.com` | 200 | **403** | 200 |
> | `cdn.hardcoregify.com` | 200 | **403** | 200 |
> | `blovjob.com` | 200 | 200 | 200 |
>
> Five of six catalogued hosts serve a 403 to an off-site referer. In the run that found
> this, **13 of 29 fetches died on it**, and the failure reads exactly like "those hosts are
> down" — it is per-host and total, so you will blame the catalog instead of your headers.
>
> **The backend is already correct and needs no change**: `_fetch_headers`
> (`api/v1/media_finder.py:158-159`) falls back to the URL's own origin, which measured 200
> everywhere. Only a hand-rolled fetcher is exposed. Send no `Referer`, or send the URL's own
> origin — never the search engine's.

**Do not spend a fetch on `*.phncdn.com`.** It is discovery-only — see the box at the top.
The header lore around phncdn (410 Gone without a User-Agent, 0-byte files at exit 0) is real
for any phncdn request you attempt, but the correct guidance is simply not to attempt one.

### Two size checks. They are different checks — do not merge them

**1. Fetch sanity, immediately after download.** Discard any response under **1024 bytes**, or
whose *bytes* are HTML. An error page is not media, and it sails past anything that only looks
at the filename — always check the bytes, never the URL:

```bash
for f in /tmp/fm/<slot>/*; do
  printf '%9s  %-12s  %s\n' "$(stat -f%z "$f")" "$(file -b --mime-type "$f")" "$f"
done
```

Anything reporting `text/html`, or under 1024 bytes, is a failed fetch. Delete it and
`options/remove` its URL — a dead URL on the shelf wastes a human click.

**2. The pre-install gate**, `scripts/tier_format_check.py`, which is a separate and stricter
bar: images ≥ **1024 B**, animated ≥ **51200 B**, plus magic-byte and per-tier extension
checks. A 20 KB "webm" passes fetch sanity and fails the gate, correctly.

Scratch goes in `/tmp/fm/<slot>/`. Anything worth keeping (contact sheets, strips) goes in
`games/<game>/.find-media/evidence/<slot>/`.

---

## 7. JUDGE — contact sheet, then the MANDATORY strip

Two stages. The second is route-independent — it applies to every clip from every host — and
it is scoped to **animated** finalists, which is all it can be: a location or clothing `.jpg`
has no frames to strip.

- **Every animated finalist (`.webm` / `.mp4` / `.gif`) is strip-verified before install.**
- **Static finalists are judged from the contact sheet.** That is the whole check for them.

JUDGE ranks and installs. JUDGE does not stock — §5 already did, and the store dedupes by
URL, so there is nothing left to add here.

### Stage A — contact sheet (cheap, narrows the field)

The Google results grid is already a contact sheet: one `computer {action:"screenshot"}` shows
20–40 tiles. Use it to decide which URLs are worth fetching at all.

For clips already on disk, build a local sheet — one representative still each, tiled into one
**numbered** image you Read once. One command, no hand-written ffmpeg:

```bash
# median-of-3 by file size, so black frames and seams (which are tiny) sort out
# video_frames.py is stdlib + ffmpeg only — plain python3, no pinned interpreter
python3 .claude/skills/find-media/scripts/video_frames.py \
  --videos-dir /tmp/fm/<slot> --mode rep --frames 3 \
  --out-dir /tmp/fm/<slot>/rep --sheet /tmp/fm/<slot>/sheet.jpg
```

The number burned into each tile is the candidate index, so `07` on the sheet is `07.gif`
on disk and entry `07` in `manifest.json` — that is what lets a judgement be acted on. Read
the **sheet**, not the tiles.

`--sheet` is rep-mode only. Batch rep also accepts **stills** (`.jpg/.png/.webp`), because a
mixed pool is normal — a location slot fetches images while a scene slot fetches clips — and
silently dropping the images reads as "the harvest found nothing". Batch **strip** still takes
clips only: a still has no loop to make a claim about.

Do NOT hand-roll the tiling with ffmpeg's `tile=` filter. Measured 2026-07-28: given eight
correct 320×320 tiles it emitted a sheet containing only **one** of them, reproduced in pure
shell. `video_frames.py` uses explicit `hstack`/`vstack` instead, which was verified correct.

`video_frames.py` exits **3** when ffmpeg isn't on PATH — then fall back to reading the
thumbnails individually. Exit 3 always means *degrade gracefully*, never crash the run.

### Stage B — frame strip, MANDATORY, on every animated finalist

Strip the **top 6 by contact-sheet rank** — that reliably covers the installed pick and its
nearest alternates. No animated option gets installed, and none gets recommended to the human
as your pick, until you have read its strip. Everything below the top 6 stays stocked and
unverified, which is correct: unproven on the shelf beats binned.

```bash
python3 .claude/skills/find-media/scripts/video_frames.py \
  --video /tmp/fm/<slot>/03.webm --mode strip --frames 4 \
  --out games/<game>/.find-media/evidence/<slot>/strip_03.jpg
```

**Thumbnails lie, constantly.** Measured this session: the strip killed **3 of 5** shortlisted
candidates in one round and **4 of 6** in another. The actual kills:

- a thumbnail that read as a perfect cluttered back room — the loop was standing **kissing**,
  with no blowjob anywhere in it
- a "dark outdoor" thumbnail whose loop was a **bright daytime laundromat**
- a thumbnail that read bent-over-from-behind — the clip was a **blowjob**
- two candidates that lost eye contact partway through, which their thumbnails hid

A single frame is a claim about one instant. The strip is a claim about the loop, and the loop
is what ships.

**Eye contact must HOLD ACROSS THE WHOLE STRIP.** It is a heat carrier, not a decoration —
the user's winning pick beat a spec-perfect alternative explicitly because "the eyes made it
win," she holds the camera the entire loop. A thumbnail with eye contact and a strip without
it is a fail, not a maybe.

Then stop. **Never auto-pick silently and never present one candidate.** Install your best
guess so the game always works, leave everything else stocked, and let the eye decide.

---

## 8. Worked example — the back-room beat

**Beat:** back room off a bar, she's on her knees, he's getting sucked off. The point is
squalor and the risk of being walked in on — so here the setting IS load-bearing and gets
words spent on it.

**1 — Word hunt.** Grok gave a headline term list that was just my own sentence rephrased;
discarded. Its modifiers were useful. While screenshotting an adjacent query, Google's own
result labels handed over `dogging` and `back alley` unprompted — neither was in my vocabulary
five minutes earlier. Both logged to the lexicon.

**2 — First query, and it failed:**

```
back alley blowjob gif drunk guy night
```

Returned Reddit movie stills, Facebook, TikTok. Zero usable results. The diagnosis is not
"too many words" — it's `drunk guy`. One character word reclassified the whole query as
mainstream.

**3 — Second query, same length, worked:**

```
back alley blowjob gif amateur
```

One `javascript_tool` regex call over `innerHTML` returned **54 direct CDN URLs**. Fifty of
them sat on fetchable aggregators — sex.com, blovjob, flashingjungle, xgroovy,
hardcoregify, nsfwgify and eporner on this page; porngif.co and xgifer joined the corpus
from other queries. Not one of them was reachable from the old PornHub-only route. The other **4 were phncdn**, and today they would be
filtered out at §4.

**4 — Stocked all 54** to `options/add` with an in-page `fetch` loop. 54/54 accepted — the
store never argued, which is precisely why the phncdn cut has to be mine and not its. The
shelf was full before I'd judged anything, which is the point: nothing that follows can
destroy a candidate the human hasn't seen.

**5 — Shortlist, and the phncdn URLs died.** Screenshotted the grid, picked candidates that
read dim + kneeling, fetched them. **Exactly the 4 phncdn URLs failed and nothing else did**;
the other 50 yielded 40 files. That is the measurement behind the discovery-only rule at the
top of this file — not "the batch mostly worked", but a clean split along one host. Every
shortlisted candidate from here on came off the aggregators, over clearnet, with no Tor
anywhere in the run.

**6 — Round 1 strips: 3 of 5 died.**
- the cluttered-back-room thumbnail → loop was standing kissing, no blowjob at all
- the "dark outdoor" thumbnail → bright daytime laundromat
- the bent-over-from-behind thumbnail → the clip was a blowjob (right act, wrong position for
  this beat, which wants kneeling)

Two survivors. Below the ≥6 floor, so:

**7 — Sibling query.** `on kneel blowjob` + `amateur` — grammatically broken, and Google did
not care. Six more fetched; **4 of 6 died on the strip**: two on eye contact that wandered
partway through the loop (their thumbnails hid it), two on standard rejection classes from
`scoring_rubric.md`.

**8 — Delivered:** four strip-verified candidates plus the rest of the 54 stocked, one
installed via `grab` as the best guess so the game builds.

**9 — What the human did:** picked a different one than mine — a **blovjob.com** clip. Chose
it explicitly because "the eyes made it win": she holds eye contact with the camera the whole
loop. It beat my pick, which was spec-perfect on act, position, and setting, and completely
dead.

That is the entire argument for this route, twice over. My scoring was correct and it was
wrong, and the only thing that saved the run was that the better clip was still on the shelf.
And the clip that won came off an aggregator — a host the old Tor route could not see, in a
run where the only unfetchable URLs were the ones that route was built around.

---

## Failure table

| Symptom | Cause | Fix |
|---|---|---|
| Extract returns `[]` or is refused | URLs still carry query strings | `.map(u => u.split('?')[0])` — the JS tool blocks query-string data |
| Extract returns only `gstatic` / `googleusercontent` | You're on the web tab, not Images | Confirm the tile grid in a screenshot; click Images, re-extract |
| Results are Reddit / TikTok / Facebook | A story or character word flipped the intent classification | Strip every story word; keep act + position + modifier |
| Bright studio when the beat wants grimy | No anti-studio modifier | Add `amateur` / `real` / `voyeur` / `hidden cam` |
| Extract count doesn't grow after scrolling | Pool exhausted, not a bug | Run a sibling query — different phrasing, different hosts |
| A candidate 470s / 410s / lands 0 bytes at exit 0 | It's a `*.phncdn.com` URL | Don't fetch phncdn at all — discovery-only. Cut it at §4 |
| File is under 1024 B, or `file` says `text/html` | Error page, not media | Delete it AND `options/remove` its URL |
| `tier_format_check.py` fails a file that downloaded fine | Pre-install gate is stricter than fetch sanity | Animated needs ≥ 51200 B — refetch a real clip, don't lower the gate |
| `options/add` → `400 Invalid or missing game` | Sent `game` the wrong way for that endpoint | **Body** on every media-finder POST; **query param** on `options/list` (GET) and on all media-review endpoints |
| Refetch left the slot empty | Cleared on the way in | Stock first, then `options/clear {before: t0}` — never the reverse |
| File lands at `videos/output/videos/…` | Passed `output/videos/…` as `file` | The API strips `videos/` but NOT `output/` |
| Option renders blank in the review UI | Wrong `media_kind` | `.gif` → `img`, `.mp4`/`.webm` → `video`. Only those two values; never `image` |
| Slot has fewer than 6 options | One query wasn't enough | Sibling query (§3). Never ship a 3-option slot |
| `video_frames.py` exits 3 | ffmpeg not on PATH | Read thumbnails individually — exit 3 means degrade, never crash |
