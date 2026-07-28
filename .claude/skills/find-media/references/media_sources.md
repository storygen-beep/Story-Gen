# Media Sources

Where the pictures live and what each shelf is worth. There is one pipeline — Chrome, one
page, one regex — pointed at different sources. The only thing that changes between a
kitchen photo and a t6 clip is which shelf you point it at and how hard you check the
bytes.

- **How to run the hunt** → `references/chrome_route.md`
- **How to judge what comes back** → `references/scoring_rubric.md` (heat, setting, craft — after the binary correctness gate)
- **What to type** → `references/query_rewriting.md` (the dialect is source-specific)
- **Contact sheets instead of raw thumbnails** → `references/sheets_and_boards.md`

## The invariant

The tooling only harvests. **The human picks.** Your job is to stock a shelf of ≥6 live
options per slot and install one best guess so the game never renders a hole. No source is
reputable enough to skip the strip on an animated finalist, and no source is bad enough to
auto-exclude before a human has looked — the failure mode this skill is being rewritten to
kill is discarding hot clips before the eye that decides ever sees them.

## NSFW shelf — measured

One Google query in the user's Chrome put 54 URLs into one slot's option store across nine
hosts. Counts below are from `games/vesper/.find-media/media_options.json` (slot
`sex/renner_cheerup_alley_t5.webm`, an outdoor-blowjob beat) — so they measure that one
query's shape, not a universal ranking. What generalizes is the *spread*: the old route
reached PornHub and nothing else. That was the ceiling, and it is gone — which matters more
than it sounds, because the 4 PornHub URLs in those 54 are the only 4 that could not be
turned into bytes at all. The other 50 yielded 40 files.

### The fetchable corpus

Measured **200 on clearnet** — no Tor, no signing, no expiry. This is the one host list the
skill uses; there is no second one. Hits are from the single query above, so a `—` means
"surfaced on other queries, fetch verified, catalog not yet profiled" — not "worse".

Hosts below are the EXACT strings observed, some of them subdomains. Elsewhere in the
skill the same hosts appear as registrable domains (`flashingjungle.com`, `xgroovy.com`).
**Match on the registrable domain**, or a host filter written off one list misses the other.

| Host | Hits | URL shape | Serves | Worth |
|---|---|---|---|---|
| `imagex1.sx.cdn.live` (sex.com) | 16 | `/images/pinporn/<yyyy>/<mm>/<dd>/<numeric>.gif` | `.gif` | Biggest single supplier. Broad aggregator, shallow tags, **numeric ids — no vocabulary to mine** |
| `blovjob.com` | 14 | `/content/<yyyy>/<mm>/<slug>.gif` | `.gif` | Single-act site (blowjob). Deep on its act, useless off it — query it by act, not by scene |
| `public.flashingjungle.com` | 9 | `/exhibitionism/…/<hash>.gif` | `.gif` | Public / exhibitionism / flashing band. **Flash, not tease** — see Bands below |
| `i.xgroovy.com` | 6 | `/contents/videos_screenshots/<n>/<n>/preview_gif.mp4` | `.mp4` | Tube-site **hover previews derived from a full video**, not authored loops. Strip these before trusting them — whether the preview is one continuous cut or sampled frames from across the video is UNMEASURED |
| `cdn.hardcoregify.com` | 2 | `/<id>/<slug>.gif` | `.gif` | Descriptive slugs — term mine |
| `cdn.nsfwgify.com` | 1 | `/<id>/<slug>.gif` | `.gif` | Descriptive slugs — term mine |
| `static-ca-cdn.eporner.com` | 1 | `/gallery/<h>/<h>/<id>/<slug>.gif` | `.gif` | Tube-site gallery gifs, descriptive slugs |
| `porngif.co` | — | `/wp-content/uploads/<yyyy>/<mm>/<id>-<slug>.gif` | `.gif` | Fetch verified (200). Deep, very descriptive slugs — strong term mine |
| `cdn.xgifer.com` | — | `/<id>/<slug>.gif` | `.gif` | Fetch verified (200). Descriptive slugs |

### Second wave — added 2026-07-27, all measured 200 on clearnet

Surfaced by the 10-slot study (27 queries). Fetch-verified, not yet catalog-profiled:
`cdn.sexxxgif.com` (very high volume, descriptive slugs — appeared on nearly every query),
`myteenwebcam.com`, `cumception.com`, `porngifs.ca`, `porngifs4u.com`, `pornogifs.net`,
`cdn.fapville.com`, `femdom-pov.me` (**tease band**), `cdn.asianporngif.com`,
`freakydeakygifs.com`, `gifcandy.net`, `img1.thatpervert.com`, `xxxpicss.com`,
`cdn.pictocum.com`, `bestadultgifs.com`. Tease-band extras: `media.tenor.com`,
`upskirt.pantiesless.com`, `pornogifs.net` — note tenor also carries a large SFW/meme
catalog, so it arrives as pollution on any query with story words in it.

**⚠️ `static-ca-cdn.eporner.com` failed every fetch attempted in that run** (URLError),
despite being in the corpus above. Re-measure before relying on it.

### PornHub is discovery-only — never a download

`egl.phncdn.com/gif/<id>.gif` is **not a fetch endpoint.** Measured: **470 on clearnet and
470 over Tor**, every id tried. It is not a header problem — the backend already sends a
full browser UA *and* `Referer: https://www.pornhub.com/` for phncdn hosts
(`_REFERER_BY_HOST` / `_fetch_headers`, `api/v1/media_finder.py:139-166`) and still gets
nothing back.

The real PornHub media URL, read off a gif page, is
`el2.phncdn.com/pics/gifs/<nnn>/<nnn>/<nnn>/<id>a.webm?validfrom=…&validto=…&ipa=1&hash=…`
— **signed, time-limited, IP-locked.** Our extraction strips query strings (the browser JS
tool blocks URLs carrying query data), so the signature is destroyed by construction. And
`pornhub.com` itself is unreachable on clearnet from this machine (curl exit: 000).

⇒ **A PornHub-hosted Google result is worth reading for its title and its tags — that is
free vocabulary — and must not be queued for download.** Read it, mine it, skip it as a
candidate.

**Surfaced, not yet characterised**: `porngipfy.com` (1 hit in the query above — a
WordPress gif blog with descriptive slugs; whether it serves us bytes is unmeasured).
Harvest it, check the bytes, assume nothing either way.

That closes the arithmetic on that page: 7 fetchable hosts + phncdn + porngipfy = the nine.
`porngif.co` and `cdn.xgifer.com` did not appear on it; they are in the corpus because
their bytes were measured elsewhere.

Three things this table teaches beyond the counts:

1. **Slugs are a term mine; numeric ids are not.** `getting-our-cock-sucked-by-a-beauty-outdoors-in-a-discreet-backalley.gif`
   and `panties-down-in-an-alley-behind-the-club.gif` are where `back alley` came from
   this session, unprompted. Read the URLs you harvest — the descriptive-slug hosts
   (nsfwgify, blovjob, hardcoregify, eporner) hand you the next query for free.
   sex.com's numeric ids hand you nothing, and neither does a phncdn URL — but the
   PornHub *page* behind it does, in its title and tags. That is the whole of what
   discovery-only buys you.

   **⚠️ A slug is worth a lot as VOCABULARY and exactly ZERO as a correctness claim.**
   It is uploader-written and routinely describes a different clip. Measured 2026-07-27:
   - `back-alley-slut.gif` → the loop is a woman pulling her top down on a **lit street**.
     No alley, no sex.
   - `three-men-fuck-one-woman_<hash>.gif` → only **two** men are ever in frame together,
     which fails the exact count gate its name promises.

   Both would have shipped if the name had been trusted. Rank candidates by slug if you
   like — that is what it is for — but **the frame strip is what decides**, and a slug that
   states the gate condition is not evidence the gate passes.
2. **The serving host is not the result host.** sex.com's 16 gifs all arrive from
   `imagex1.sx.cdn.live`, which contains neither "sex" nor "com" as a registrable domain.
   Any allowlist keyed to the site names you saw on the results page throws away your
   largest supplier. Filter on file extension, never on a host allowlist. The one host
   rule in this skill is a denial, not an admission: phncdn, which serves us nothing.
3. **Single-act sites beat aggregators inside their act and are dead outside it.**
   blovjob returned 14 on a blowjob beat. It will return nothing on a doggy beat. When a
   slot's act is one clean noun, expect one host to dominate; when the act is unusual,
   expect the aggregators to carry it.

## Bands — which shelf carries which content

The single most repeated defect is a shelf-band mismatch: you searched the explicit band
for a beat that was withheld, so every option is too hot and the human rejects all six.

| Band | What the beat means | Where it lives |
|---|---|---|
| **Tease / withheld** | Clothed. Something is *almost* visible. Nothing is shown. `downblouse`, `upskirt`, cleavage-lean, bra-through-shirt | Candid / voyeur / tease-tagged sources. **Not** the hardcore gif aggregators — they hold almost no clothed content, so a tease query there returns the explicit neighbours instead and you never notice the band slipped |
| **Flash / reveal** | The clothes come off or aside. It IS shown, briefly | flashingjungle and the public/exhibitionism sources |
| **Explicit act** | The act is the content | The gif aggregators above; single-act sites when the act is one noun |
| **Public / outdoor** | The place carries the danger | flashingjungle, plus the `dogging` / `back alley` vocabulary |
| **SFW** | Locations, objects, domestic, non-sexual activity | Stock shelf below |

**A STRIP IS NOT A TEASE.** This is an explicit rejection the user made. A tease is
lighter and withheld; a flash shows completely. They are different bands on different
shelves, and swapping them is not a near-miss — it destroys the beat, because a beat
written as withheld stops meaning anything once the thing is shown.

The tease band is also where term discovery pays most: the vocabulary is narrow, weird,
and community-coined (`downblouse` had to be found on Reddit — the skill had no way to
guess it). Budget a discovery pass for tease beats specifically. See
`references/query_rewriting.md`.

**The band model now has direct evidence, not just a rationale.** On the 2026-07-27 study,
`downblouse cleavage lean forward tease clothed gif` returned a host cluster that **no
explicit-act query in the run touched**: `femdom-pov.me` ×12, `media.tenor.com` ×12,
`upskirt.pantiesless.com`, `cdn.fapville.com`, `pornogifs.net`, giphy. Meanwhile the
hardcore aggregators that dominated every other slot (blovjob, hardcoregify, imagex1) were
nearly absent. The tease shelf is a genuinely different shelf, and **only the community term
reaches it** — a paraphrase like "woman leaning forward cleavage" lands you back on the
explicit shelf with the band silently wrong.

**Lexicon correction — `dogging` is mis-mapped.** It is catalogued here and in older notes
as the public/outdoor term, and it does return public/outdoor — but weighted heavily to
**beach and daylight**. It is *not* a night or alley term, and using it for a dark-alley beat
pulls the setting in exactly the wrong direction. For night/urban/grimy, `back alley` +
`amateur` is the pairing that works (and see the ≤2-setting-token ceiling in
`query_rewriting.md` before adding `at night` and `streetlight` on top of it).

## SFW shelf

Same Chrome route, different sources. These need no headers, have durable URLs, and are
licensed for placeholder use.

| Source | Reach it by | Good for |
|---|---|---|
| Unsplash | `site:unsplash.com <query>` | Locations, interiors, wide room shots. Best hit rate for empty-space queries |
| Pexels | `site:pexels.com <query>` | Same shape, different catalog — run both, they miss differently |
| Pixabay | `site:pixabay.com <query>` | Fallback when the first two return nothing usable |
| Broad image search | plain query | Lifestyle / activity scenes where stock reads too staged |

SFW rules, all of them earned by a past bad asset:

1. **Never invent a URL.** Only use URLs that an actual search returned. A plausible-looking
   Unsplash path that you constructed will 404 or, worse, 200 with something else.
2. **People count is sacred.** A two-person story never shows 3+ people on an activity
   asset. No exceptions, no "but the composition is nice".
3. **Room shots for locations** — wide angle showing the space, not a close-up of one
   object. A player uses a location image to orient; a macro of a doorknob orients nobody.
4. **Photographic, not rendered.** Illustrations and 3D renders break the frame against
   the NSFW assets sitting next to them in the same game.
5. **No heavy watermarks.** Corner marks are fine — these are placeholders — but a
   diagonal agency bar across the subject is not usable.
6. **Prefer permissive licensing.** Stock sites, not an artist's portfolio or gallery.
7. **SFW sources leak.** Tag mismatches occasionally return nudity on an innocent query.
   Look before you install; an unexpected explicit asset in a `base`-tier slot is a bug.

## Query enhancement by content type (SFW)

Stock search defaults to solo lifestyle shots. The porn sources are the opposite — say
nothing and you get a couple. So the people-count signal has to be explicit on SFW and
usually not on NSFW.

| Content type | Add | Example |
|---|---|---|
| Activity, 2 people | `couple`, `two people`, `at home` / `domestic` | `casual lunch kitchen` → `couple having casual lunch at home kitchen two people` |
| Location, 0 people | `interior wide angle` / `room view`, `empty` / `no people` | `home garage interior` → `home garage interior wide angle empty no people` |
| Object / mood, 0 people | `close up` / `detail shot` | `morning coffee` → `two coffee mugs morning light close up kitchen counter` |

The NSFW dialect is a different animal: story words kill Google's porn intent, and the
canonical tag is short where your beat description is long. It lives in
`references/query_rewriting.md`.

## Ordering — do not trust the top of any list

The datum that started this rule, measured on a porn site's own search: positions 0–3 were
trending garbage and the setting-matched results sat at 4–10+. Generalize it carefully,
because Google is not a porn site's search box:

- What is measured on Google: **one page yielded 54 direct CDN URLs across nine hosts, 50
  of them fetchable.** The page is deep and host-diverse. Take the whole page.
- What is NOT measured on Google: whether its ordering is any good for heat. Google ranks
  on SEO and site authority, neither of which knows what a beat needs. So the first row is
  a *sample* of the shelf, not the top of it.
- Therefore: never stop at row one, and never assume the inverse either (that late results
  are secretly better). Harvest the page, contact-sheet it, let the eye order it.

## The direct-fetch contract

Applies to every route that turns a URL into bytes on disk — the `grab` endpoint, the
capture endpoint, and manual `curl`.

**Headers**

| Rule | Why |
|---|---|
| Always send a browser `User-Agent` | Picky CDNs answer a bare request with 410/470 — a 0-byte file that looks like a successful download. `download_direct` already sends one on every request including the HEAD (`api/v1/dev.py:213-217`), so `grab` is covered; **your manual `curl` is not** |
| **Never send `Referer: https://www.google.com/`. Send none, or the URL's own origin.** | Off-site referer = hotlink protection. Measured 403 on `cdn.sexxxgif.com`, `cdn.nsfwgify.com`, `porngif.co`, `cdn.xgifer.com`, `cdn.hardcoregify.com`; 200 on all five with no referer and with their own origin. **13 of 29 fetches died on this in one run**, and it presents as "those hosts are down". `_fetch_headers` (`api/v1/media_finder.py:158-159`) already falls back to the URL's own origin, so `grab` is safe — a hand-rolled fetcher is not. Full table in `chrome_route.md` §6 |
| Don't hand-fetch phncdn at all | The backend already attaches the UA *and* the pornhub `Referer` and it still returns 470. There is no header that fixes it — see "PornHub is discovery-only" above |
| `source` is a free label except `"redgifs"` | Only `redgifs` triggers the Bearer-token fetch (`api/v1/media_finder.py:475-478` on grab, `:591-594` on proxy). No source needs Tor — `_TOR_SOURCES` is empty (`media_finder.py:551`) |

**Failure signatures**

| What you see | What it means | Do |
|---|---|---|
| `URL returned HTML instead of media` | The host redirected to an age gate or captcha. `download_direct` aborts on a `text/html` Content-Type (`dev.py:224-225`) — this is the API protecting you, not a bug | Drop the URL; it was a page link, not a media link |
| `HEAD request failed` | `grab` HEADs before it GETs (`dev.py:221`). A host that 405s or 410s a HEAD kills the grab even when a plain GET would have worked | Fall back to `curl` straight into `games/<game>/videos/<subfolder>/` |
| 0-byte or tiny file | CDN rejected the request (missing UA/Referer) or served an error body with 200 OK | Re-fetch with headers; if it repeats, drop the URL |

**Bytes, not URLs**

- **Never trust a URL's extension.** The API decides the saved extension from the source
  URL path → HEAD `Content-Type` → `.jpg` as last resort, and strips whatever the TOML
  declared (`references/api_behavior.md`). A URL ending `.gif` can be anything.
- **Two size checks, and they are not the same check.**
  - *Fetch sanity*, run the moment a download lands: discard anything under **1024 bytes**,
    or whose bytes are HTML. An error page is not media. Check the bytes, never the URL.
  - *Pre-install gate*, `scripts/tier_format_check.py`: images ≥ **1024 B**, animated ≥
    **51200 B** (50 KB). Valid tiers there are `base`, `location`, `t0`–`t8`. The transport
    ceiling is 500 MB and the timeout 60 s (`dev.py:34-35`).
- **`file <path>` the result.** The extension is a claim; `file` is the evidence.
- **t5+ is a hard format rule.** A t5+ file must be WebM / MP4 / GIF. `file` reporting
  "JPEG image data" at t5+ is a **FAIL** — delete it and report. A 10 KB thumbnail is
  useless as a video placeholder, and it will render as a frozen `<img>` in a slot the
  writer wrote for motion. `tier_format_check.py` gates this before you install.
- **Strip query strings** off harvested URLs before returning or posting them. This is also
  why signed CDNs are unreachable to us — the signature lives in the query string, so
  stripping it is not a lossy convenience, it is a hard exclusion. Judge a signed host by
  that, not by hope.
- **Write to `games/<game>/videos/`**, never `games/<game>/output/` — output is the
  compiled copy and packaging rewrites it.

**Every animated finalist is frame-stripped — no exceptions, no reputable sources.** One
frame lies: the act may not be at 00:00:02, and thumbnails killed 3 of 5 and 4 of 6
shortlisted candidates in two separate rounds this session — including a "perfect cluttered
back room" whose loop was standing kissing with no blowjob in it at all. Static finalists
(a location or clothing `.jpg`) have nothing to strip; they are judged from the contact
sheet. The procedure lives in `references/chrome_route.md`; what to look for lives in
`references/scoring_rubric.md`. The store holds URLs, but the strip needs a local file —
bytes must be on disk before an animated candidate gets judged.

## Cost discipline

Two measured lessons from this skill's own history, both about the same thing:

- **Viewing raw thumbnails was the dominant token sink** — roughly 0.5–1M tokens per game
  spent purely *looking*. This is why candidates get assembled into a contact sheet and
  read as one image (`references/sheets_and_boards.md`), not opened one by one.
- **Do NOT spawn one subagent per source.** The old fan-out (4 subagents per item)
  multiplied token cost with no benefit — every agent paid to look at its own pile and
  none of them could compare across piles. One page, one regex, one sheet, one look.

The host spread above is not nine searches. It is one.
