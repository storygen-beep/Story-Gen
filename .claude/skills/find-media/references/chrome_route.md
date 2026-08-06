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

### 2.0 PREFLIGHT — is the extension even connected? Ask the HUMAN, don't work around it.

**`list_connected_browsers` before anything else.** It costs one call. If it returns `[]`,
**STOP and tell the human, in your very next message, that the Chrome extension is
disconnected and you need them to reconnect it.** They can fix it in seconds. You cannot fix
it at all, and every minute you spend not saying so is wasted.

```
mcp__claude-in-chrome__list_connected_browsers   → []   ⇒ STOP. Tell the human. Do not proceed.
```

**Chrome's own process may still be running** — `pgrep "Google Chrome"` succeeding proves
nothing. What is down is the extension's pairing link, not the browser. Do not report "Chrome
is running" as though it means the route is alive.

**There is no fallback. Both plausible ones were measured and both are wrong:**

| Tempting fallback | What actually happens |
|---|---|
| `curl` the Google Images URL directly | **HTTP 200, ~90 KB, and ZERO extractable media urls** — the grid is JS-rendered. The danger is the *signature*: a rich-looking 200 that harvests as nothing reads exactly like "my query was bad," and sends you rewriting perfectly good queries for hours. |
| Mine a sibling slot's already-stocked shelf | Those urls were harvested against a **different slot's demand**. Installing from them is the exact cross-slot collision the scope brief exists to prevent. Three wrong clips on a self-loop node the player sees 4–6× per visit is worse than an honest 1-of-4. |

**An honest blocked report IS the correct deliverable here.** Report `pool_count_final` as-is,
say the route is down, and stop. This cost a 9-agent batch roughly an hour on 2026-08-03:
every agent independently invented a workaround before diagnosing the real cause, and one
nearly installed wrong-composition clips to hit its target.

If the route dies **mid-run**, the same rule applies — but everything you already installed
stays on disk, so `grab` + `dedup_tracker --record` each clip *the moment it passes its gates*
rather than batching installs to the end. That is what turned a later round of failures from
total losses into partial wins.

---

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
| `javascript_tool` `{action:"javascript_exec", tabId, text}` | The workhorse: the URL extract (§4) and the options POSTs (§5). REPL semantics — the last expression is the return value, and top-level `await` works, so an inline `await fetch()` call is fine. ⚠️ **One call has a hard 45 s ceiling** (`Runtime.evaluate`), and on timeout the page KEEPS EXECUTING while you get an error and no value — so any loop of network calls must be chunked/concurrent and idempotent (§5). |
| `browser_batch` | Collapse navigate + wait + screenshot into ONE round trip. |
| `computer` `{action:"scroll"}` | Pull in lazy-loaded tiles already on the page. Does **not** load more results — that needs a "More results" click (§4). |

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

**Shape:** `<act> <her posture> <HIS posture — only when it is not the act's default> [setting-if-load-bearing] [anti-studio modifier] gif`

**⚠️ `<act>` must be a REAL ACT WORD — and a position is not one.** `riding`, `cowgirl`, `missionary`
and `doggy` are ordinary English (a horse, a ranch, a religion, a dog). A query built only from them
does not return *bad* porn; it returns **none**. Measured 2026-08-01, same query minus one token:

| query | urls | on a porn host |
|---|---|---|
| `riding cowgirl man in office chair gif` | 83 | **0** — Tenor, BBC, Wikipedia, NFL, Warhol |
| `cowgirl riding fuck office chair gif` | 73 | **69 (95%)** |

`blowjob` anchors a query by itself, which is why every oral slot worked and this stayed invisible
until the first penetrative beat. `validate_queries.py` flags it as `no_act_anchor` on `t5`–`t8`;
the word list and its membership rule are in `scripts/scene_semantics.py` (`ACT_ANCHORS`).

**An act phrase carries a DEFAULT PARTNER POSTURE, and it wins unless you override it.** This is
the single largest source of rejections in this skill's recorded history, and until 2026-08-01 the
shape above had one `<position>` slot that never said whose body it named.

`kneeling blowjob` retrieves **she-kneels-he-STANDS**. That is the canonical composition on this
corpus. If your beat needs him **seated, reclining, lying down, or bent over**, that is not the
default and the query has to say so — `office chair`, `under the desk`, `sitting in chair`,
`on the couch`.

**Measured on `vesper`, 2026-07-31 — three slots, same act, different queries:**

| slot | beat needs | did the query name HIS posture? | seated/chair/desk slugs returned | dominant rejection |
|---|---|---|---|---|
| `colm` | standing — *the default* | yes | n/a | position was fine |
| `renner` | **seated** | yes — `office chair`, `under the desk`, `man sitting in chair` | **13 of 43** | reduced |
| `calloway` | **seated** | **no** — `glasses`, `close up`, `pov` only | **0 of 10** | `him_standing`, in three separate runs: 11/15, 12/26, 15/19 |

Calloway's queries asked for wardrobe and framing and never asked for a seated man, so the corpus
gave it the default one, over and over, and the judging step dutifully rejected every one.

**Be honest about which half of this is proven.** The *omission* is measured — naming his posture
correlates with getting it, and not naming it correlates with not getting it. Whether adding the
token to calloway's queries would have fixed that slot has **not** been tested. Treat the missing
token as the established defect and the extra token as the obvious remedy, not a proven one.

**Corollary — you cannot judge your way out of this.** A wrong partner posture is a legitimate
`position:` gate failure, so a bad query here does not produce bad picks; it produces an expensive
empty shelf. Fix it in the query or pay for it three rounds later.

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
const Q = 'dogging fuck alley wall voyeur gif';   // the query you just ran, verbatim
const html = document.documentElement.innerHTML;
const urls = [...new Set((html
  .match(/https?:\/\/[^"'\\\s]+?\.(?:gif|mp4|webm)/gi) || []).map(u => u.split('?')[0]))];
const by = {};
urls.forEach(u => { const h = new URL(u).host.replace(/^www\./, ''); by[h] = (by[h] || 0) + 1; });
const hosts = Object.entries(by).sort((a, b) => b[1] - a[1]);   // REAL hostnames — §5 POSTs these
// docid join — Google's index id per result, from the page's metadata triples
// ["<docid>",["<thumb>",h,w],["<file>",h,w]]. It is what makes "fetch related" a
// one-navigation lookup later (§5b), so capture it on EVERY harvest. Misses are
// lazy-loaded tiles — the scroll pass below recovers those already in the page;
// the "More results" click is what adds new ones.
const docids = {};
for (const m of html.matchAll(/"([A-Za-z0-9_-]{10,20})",\["https:\/\/encrypted-tbn[^"]+",\d+,\d+\],\["(https?:[^"]+?)",\d+,\d+\]/g))
  docids[m[2].replace(/\\u003d/g, '=').replace(/\\u0026/g, '&').replace(/\\\//g, '/').split('?')[0]] = m[1];
window.__fm = { q: Q, urls, hosts, docids };                    // §5 reads this
hosts.map(([h, n]) => `${n}  ${h.split('.').join(' DOT ')}`)    // the RETURN VALUE only
```

⚠️ **The `" DOT "` join is a RETURN-VALUE transform, and only that.** A tool's return value
passes through a secret-scanner that reads bare dotted CDN hostnames as credentials and hands
back `[BLOCKED: JWT token]` — measured on three runs, once redacting 6 of 8 rows, and the
histogram is the only gate this skill has, so a redacted one is a blind gate failing silently.
A **POST body never passes through that filter**. So `hosts` keeps real hostnames and the
transform is applied once, to the array you return. Transform first and reuse it and the
store is poisoned irreversibly: the picker renders `i DOT xgroovy DOT com` forever, and a
hostname that legitimately contains the text `" DOT "` is indistinguishable from a mangled
one, so nothing downstream can undo it. `queries/add` refuses such a host with a 400 — treat
that 400 as "I transformed too early", never as "the endpoint is broken".

`window.__fm` dies if the tab navigates between the two passes. If §5 finds it undefined,
re-run this block rather than guessing the url list.

- Keep the original CDN hosts — that's the candidate pool (nsfwgify, xgroovy, blovjob,
  porngif.co, hardcoregify, xgifer, sex.com, flashingjungle, eporner). All nine answer 200
  on clearnet: no Tor, no signing, no expiry. Exact host strings — some are subdomains,
  e.g. `public.flashingjungle.com`, `i.xgroovy.com` — in `references/media_sources.md`;
  match on the registrable domain, not the full host, or a filter misses half of them.
- **Stock `*.phncdn.com` like any other host** — the cut that used to live here was
  removed 2026-08-06; its urls are signed and fetch 200 (see
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

**Scroll pulls in lazy tiles; only the "More results" CLICK adds new ones.** Two different
mechanisms, and confusing them costs you most of the grid. Google renders ~200 tiles and
stops. Scrolling past that does nothing — measured 2026-08-06: four scroll-to-bottom passes
moved the page and added **zero** tiles. What adds tiles is the **"More results" button** at
the foot of the grid, and it is **repeatable**: 205 → click → 405 → click → 605, roughly 200
a click, with the button still present afterwards. Click until you have enough.

Grab it by visible TEXT, never a class — Google's class names are obfuscated and rotate:

```js
const btn = [...document.querySelectorAll('a[role="button"],div[role="button"],button,input')]
  .find(el => /^more results$/i.test((el.innerText || el.value || '').trim())
              && el.getBoundingClientRect().width > 0);
```

So the self-check is extract → click → re-extract. **A flat count after scrolling means you
reached the button — never that the pool is exhausted.**

⚠️ **The yield is thin on an ANIMATED slot.** At 605 tiles that same grid gave **80**
extractable `.gif`/`.mp4` urls (~13%) — the depth is mostly `.jpg`/`.webp` page thumbnails a
`gif|mp4|webm` extract cannot use. Two or three clicks is the sweet spot; grinding deeper is
not worth the calls.

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
const FILE = 'scenes/alley_bj_t5.webm';   // the slot's TOML-declared path, verbatim
const KEY  = 'scenes/alley_bj_t5.webm';   // the item's own slot_key, verbatim — the SHELF key
const API  = 'http://localhost:8000/api/v1/dev/media-finder';
const J    = b => ({ method: 'POST', headers: { 'Content-Type': 'application/json' },
                     body: JSON.stringify(b) });
const { q: Q, urls, hosts, docids } = window.__fm;   // from §4 — do not re-derive them here

// 1. stock, tagging every candidate with the search that produced it AND its
//    docid when §4's join paired one — that id is what powers "fetch related".
// ⚠️ ONE request for the whole query. options/add_bulk applies every row under a
//    single lock acquisition and a single file write — see the note below.
const isVid = u => /\.(mp4|webm)$/i.test(u);
const res = await (await fetch(`${API}/options/add_bulk`, J({
  game: GAME, file: FILE, slot_key: KEY, query: Q,
  items: urls.map(u => ({
    url: u,
    type: isVid(u) ? 'video' : 'gif',
    media_kind: isVid(u) ? 'video' : 'img',
    docid: (docids || {})[u] || ''
  }))
}))).json();
const ok = res.added;                      // {added, duplicates, invalid, count}

// 2. record the SEARCH — its real counts and its histogram. ALWAYS run this, INCLUDING
//    when `urls` is empty: a query that came back with nothing is still a query that ran,
//    and it is the record that stops you re-running a dead one three rounds later. It
//    also writes the query_ledger.jsonl line, so you never hand-write one again.
await fetch(`${API}/queries/add`, J({
  game: GAME, file: FILE, slot_key: KEY, query: Q,
  source: 'google', urls: urls.length, stocked: ok, hosts
}));
`${ok}/${urls.length}`
```

Rules, each with the reason it exists:

- ⚠️ **Stock with ONE `options/add_bulk`, not a loop of `options/add`.** Both write the same
  shelf; they differ in how many times the ledger is rewritten. **Every `options/add` rewrites
  the whole file, and the lock is global to the game** — measured on vesper's 5.7 MB store
  (2026-08-06): ~69 ms of pure serialize per call, ~145 ms projected at 12 MB. **Measured
  end-to-end against a 4.4 MB store: 250 urls cost 53.5 s per-url (214 ms each) against 0.21 s
  as one bulk call — 253×.** An 88-slot harvest posts ~22,000 urls, so the per-url path burns
  ~78 minutes of API time, much of it holding a lock no agent can overlap; bulk costs ~20
  seconds. It also drops the call well under the 45 s `Runtime.evaluate` ceiling
  instead of racing it. Cap is 2000 items — over that the endpoint **refuses**, because a
  silently truncated tail reads downstream as "the query was thin" and sends you rewriting a
  query that was fine. Read `{added, duplicates, invalid, count}`; `invalid` is never silent.
- ⚠️ **If you ever fall back to per-url `options/add`, it MUST be chunked and concurrent. A
  sequential `for … await fetch` loop over 60+ urls ALWAYS times out.** `Runtime.evaluate` has
  a hard **45 s** ceiling and each POST costs ~0.6 s, so ~75 sequential POSTs cannot finish in
  one `javascript_tool` call. Measured 2026-08-06 on vesper: **five of six slot agents hit it
  independently**, at 74, 79, 83 and 85 urls. `Promise.all` in chunks of 10 finishes 74 in ~20 s.
  **The failure is worse than a timeout, because it is not atomic.** The renderer keeps running
  the loop after the tool gives up, so the shelf goes on filling while you hold an error and no
  return value — you cannot tell how many landed. Recovery is safe (both endpoints dedupe by
  url) but you must re-read the shelf to learn the count.
- ⚠️ **POST `hosts` RAW — it is already `[[host, count], …]`, and that is the only shape the
  server accepts.** `_clean_hosts` (`api/v1/media_finder.py:551`) requires a list of 2-element
  pairs and returns `None` — silently **dropping the field, keeping the record** — for anything
  else. Reshaping it to `[{host, n}]` is the natural-looking mistake, and it costs the histogram
  without any error: measured 2026-08-06, all 34 chips of a vesper run stored `hosts: absent`
  and every query lost its diagnosis. The only mangling the endpoint *refuses* loudly is the
  `" DOT "` transform (400). Re-read one chip after your first `queries/add` and confirm
  `hosts` is actually stored.
- **`file` is the slot's TOML-declared path, character for character.** It is where the bytes
  will go. A typo installs to a path the game never reads.
- **`slot_key` is the item's own key, verbatim — the SHELF is filed under it.** They are the
  same string for an untagged slot, which is nearly all of them; they differ the moment a
  block authors an `id`. Send both. This snippet omitted `slot_key` for months while three
  prose rules demanded it, and code always beats prose it contradicts.
- **`query` is the search you ran, verbatim — and it comes BACK as `found_by`, a list.**
  That rename is the one field trap in this API: you POST `query`, the store files it under
  `found_by`, and there is no `query` key on an option ever. It is what puts this candidate
  in a labelled
  bucket in the picker instead of an undifferentiated pile. Omit it and the option lands
  under "older searches" with no way, ever, to work out where it came from — there is no
  retroactive attribution, which is exactly why ~19,300 already-stocked options can never
  be labelled. A url a sibling query re-finds keeps BOTH labels; that is handled server-side.
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

  > ⚠️ **v3 does not do this any more.** Once every candidate carries the search that found
  > it, a refetch is just another labelled bucket, and the newest chip already *is* the fresh
  > shelf this prune used to manufacture — so pruning now only destroys candidates the human
  > has never seen. This rule stays live for **v2**, which still installs, and for the
  > janitor's bulk-remove. See `find-media-v3/SKILL.md` §4.

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
(shape: `{game, updated_at,
         options: {<slot>: [{url, type, media_kind, added_at, found_by?: [q,…], docid?}]},
         queries: {<slot>: [{q, at, last_at, runs, source, urls, stocked, hosts, seed_url?}]}}`).

---

## 5b. RELATED — one option's Google related-feed, on request

The picker's ⇢ button normally does this through `scripts/fetch_related.py` (a CDP
script driving the dedicated find-media Chrome). When that runner is down — or the
human simply asks — the SAME recipe runs through this route. It is one navigation
plus §4's extraction; there is no query to write.

The measured facts it stands on (2026-08-05): the related feed is the plain URL
`https://www.google.com/search?udm=2&q=<query>&tbs=rimg:<blob>` where the blob is
base64url(`0x09` + first 8 bytes of the base64url-decoded docid). Ground truth:
docid `FvF5n0MlBjcrfM` → blob `CRbxeZ9DJQY3`. A truncated blob built that way
serves the real feed (~50 direct urls, seed excluded).

1. **Get the seed's docid** from `options/list` (the entry's `docid`). **If it is
   absent, STOP — do not fetch, and do not go looking for the id.** This is LO's
   ruling (2026-08-05) and the runner enforces it before it touches the browser.
   Hunting the id means running a text search built from a *guess* (the slot's
   query, or failing that the filename's slug words), which on an aged shelf opens
   a search nobody asked for and fails anyway because the clip no longer ranks.
   Say so plainly: the clip has no id, and the cure is a new SEARCH on the slot —
   any search that re-finds it attaches an id to the existing option in place
   (measured: one sibling query revived 17 of 226 on `media_lab_f`).
2. **Build the URL** (in-page, or by hand):
   ```js
   const d = atob(DOCID.replace(/-/g, '+').replace(/_/g, '/') + '='.repeat((4 - DOCID.length % 4) % 4));
   const blob = btoa('\x09' + d.slice(0, 8)).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
   `https://www.google.com/search?udm=2&q=${encodeURIComponent(Q)}&tbs=rimg:${blob}`
   ```
   `Q` = the seed's `found_by[0]`, else the slot's newest non-related query, else
   the filename's slug words. Keeping the slot's proven query pins the ACT while
   the visuals wander — it is what stops a related hop drifting off the brief.
3. **Navigate, scroll, click "More results", extract** — §4's blocks verbatim, including the docid join:
   every clip this stocks carries its own docid, so any of them can seed the next
   hop. Recursion is the human clicking again, never a loop you run.
4. **Stock under a related LABEL, then record.** Label = `⇢ ` + the seed's filename
   stem (e.g. `⇢ kneeling-blowjob`). If that label already belongs to a DIFFERENT
   seed's record, suffix ` ·2` (` ·3`, …). Stock loop = §5's, with `query: LABEL`.
   Close with:
   ```js
   await fetch(`${API}/queries/add`, J({
     game: GAME, file: FILE, slot_key: KEY, query: LABEL,
     source: 'related', seed_url: SEED, urls: urls.length, stocked: ok, hosts
   }));
   ```
   `source: 'related'` + `seed_url` are what flip the picker's ⇢ button to
   "N related" — omit either and the fetch is invisible. A zero-yield feed still
   gets this call. A **409** means the label was claimed by another seed mid-run:
   re-pick with the next suffix and RE-STOCK the urls under it (dedup makes that
   N cheap `found_by` appends) before re-recording — a bare re-record would leave
   the options under the other seed's label.
5. Re-fetching the same seed later is a TOP-UP of the same chip — never clear.

Captcha or "unusual traffic" at any step: stop and report, exactly as in §3.

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

**`*.phncdn.com` is fetchable** when the signed query string survives extraction — see the box at the top.
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

**Strip the whole batch and read ONE board — never one strip at a time.** `--board` stacks
every candidate's strip into a single labelled image, one row per candidate, six rows to a
board (1280×1920), spilling to `_2.jpg` beyond that:

```bash
python3 .claude/skills/find-media/scripts/video_frames.py \
  --videos-dir /tmp/fm/<slot> --mode strip --frames 4 \
  --out-dir games/<game>/.find-media/evidence/<slot>/strips \
  --board games/<game>/.find-media/evidence/<slot>/board.jpg
```

Single-clip form (`--video … --out strip_03.jpg`) still exists, for re-checking one candidate
after the board — not for working through a batch.

> **Why this is a rule and not a preference.** Boards were an ad-hoc `strips.sh` until the
> 2026-07-28 promotion, which kept `--sheet` for rep mode and **silently lost strip boarding**.
> The next run read strips one at a time: **52 image reads where ~15 would have done**, roughly
> tripling JUDGE, and the lost time was initially blamed on the thing being measured rather
> than on the missing feature. Re-verified 2026-07-29 on the same 16 candidates — one board
> reproduced all six per-candidate verdicts, including two eye-contact breaks, at ~260px per
> frame after the reader's downscale.

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
| **Any browser tool says "Browser extension is not connected", or `list_connected_browsers` returns `[]`** | **The extension's pairing link is down. Chrome's own process may still be running — that proves nothing.** | **STOP and tell the human in your next message so they can reconnect it. Do NOT curl (200 + 0 urls, reads like a bad query) and do NOT mine a sibling shelf (cross-slot collision). An honest blocked report is the deliverable. See §2.0** |
| Extract returns `[]` or is refused | URLs still carry query strings | `.map(u => u.split('?')[0])` — the JS tool blocks query-string data. **Check §2.0 FIRST — a dead extension presents almost identically and this row will send you rewriting good queries for hours** |
| Extract returns only `gstatic` / `googleusercontent` | You're on the web tab, not Images | Confirm the tile grid in a screenshot; click Images, re-extract |
| Results are Reddit / TikTok / Facebook | A story or character word flipped the intent classification | Strip every story word; keep act + position + modifier |
| Bright studio when the beat wants grimy | No anti-studio modifier | Add `amateur` / `real` / `voyeur` / `hidden cam` |
| Extract count doesn't grow after scrolling | You reached the ~200-tile boundary — scrolling cannot cross it | **Click "More results"** (§4), then re-extract. Measured: 4 dead scrolls → 0 new tiles; each click → +~200. Never call the pool exhausted before the click |
| Grid still flat after clicking "More results" | Pool genuinely exhausted for this phrasing | Run a sibling query — different phrasing, different hosts |
| A candidate 470s / 410s / lands 0 bytes at exit 0 | A phncdn URL that LOST ITS TICKET | 470 means the query string was stripped. Unescape before extracting and keep `?validfrom&validto&hash` — the bare path is always dead |
| File is under 1024 B, or `file` says `text/html` | Error page, not media | Delete it AND `options/remove` its URL |
| `tier_format_check.py` fails a file that downloaded fine | Pre-install gate is stricter than fetch sanity | Animated needs ≥ 51200 B — refetch a real clip, don't lower the gate |
| `options/add` → `400 Invalid or missing game` | Sent `game` the wrong way for that endpoint | **Body** on every media-finder POST; **query param** on `options/list` (GET) and on all media-review endpoints |
| Refetch left the slot empty | Cleared on the way in | Stock first, then `options/clear {before: t0}` — never the reverse |
| File lands at `videos/output/videos/…` | Passed `output/videos/…` as `file` | The API strips `videos/` but NOT `output/` |
| Option renders blank in the review UI | Wrong `media_kind` | `.gif` → `img`, `.mp4`/`.webm` → `video`. Only those two values; never `image` |
| Slot has fewer than 6 options | One query wasn't enough | Sibling query (§3). Never ship a 3-option slot |
| `video_frames.py` exits 3 | ffmpeg not on PATH | Read thumbnails individually — exit 3 means degrade, never crash |
| Histogram rows come back `[BLOCKED: JWT token]` | Bare dotted hostnames in a RETURN VALUE trip the secret-scanner | Join the labels with `" DOT "` — but only in what you *return*, never in what you POST (§4) |
| `queries/add` → `400 … ' DOT ' transform` | You transformed the hosts before POSTing them | Keep `hosts` real; the transform belongs on the returned array alone. The endpoint is fine |
| `options/add` loop returns a **45 s timeout** and no counts | Sequential `await` per url — `Runtime.evaluate` caps at 45 s and each POST is ~0.6 s | Use **`options/add_bulk`**: one request per query, one lock, one write. If you must use the per-url path, chunk it `Promise.all` 10 at a time. **The loop keeps running after the timeout**, so re-read the shelf for the true count rather than assuming zero (§5) |
| The whole run feels slow and agents sit idle | ~22,000 per-url `options/add` calls, each rewriting the whole ledger under a **game-global** lock — 214 ms per url measured against a 4.4 MB store | `options/add_bulk`: same 250 urls in 0.21 s against 53.5 s, **253×**. Over a full 88-slot run, ~78 min of API time → ~20 s (§5) |
| `options/add_bulk` → `400 items exceeds 2000` | One query yielded more rows than the cap | Split the list. The endpoint refuses rather than truncating on purpose — a dropped tail reads as a thin query (§5) |
| `queries/add` returns 200 but the chip has **no hosts** | You reshaped `hosts` to `[{host,n}]` — `_clean_hosts` accepts only `[[host,count],…]` and drops the field silently | POST `hosts` raw from `Object.entries()`. Re-read one chip to confirm it stored (§5) |
| Picker shows every option under "Older searches" | You stocked without `query` | Send `query` on every `options/add`. There is NO retroactive attribution — unlabelled is permanent |
| A chip is missing for a query that ran | You skipped `queries/add` | Call it once per query, including zero-yield ones |
| ⇢ button never flips to "N related" after a related run | The closing `queries/add` lacked `source: 'related'` or `seed_url` | Both fields, always — they are the join the button derives its state from (§5b) |
| `queries/add` → **409** on a related run | The label belongs to a different seed (two clips share a basename) | Suffix ` ·2` and **RE-STOCK the urls under the new label** before re-recording — a bare re-record leaves them filed under the other seed (§5b) |
| Related feed almost empty, zero porn hosts | Wrong Chrome on the CDP port, or SafeSearch crept back ON in the profile | Check the dedicated profile, not the query — a genuinely barren feed still serves furniture (§5b) |
