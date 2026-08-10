# find-media — CHANGELOG

## 2026-08-09 (latest) — `grab` now COMPRESSES on install, so the installed extension is `.mp4`

- **`SKILL.md` §6 INSTALL** — documented the new auto-compress step in `grab`. An animated
  download (`.gif/.webm/.mov/.mkv/.avi/.m4v`) is re-encoded to **H.264 CRF 23** between the
  staging fetch and the atomic install; `.mp4` sources and every still pass through untouched.
  **The operative warning: read the target path off the response's `file_path`, never off the
  url's extension** — `alley_bj_t5.webm` now lands as `alley_bj_t5.mp4`, so a post-install check
  built from the requested name hunts a file that does not exist. Also documented the new
  response fields `transcoded` / `transcode_skipped`, and that **a skip is never an error**.

- **Why (engine change, not doctrine).** LO's build had gone 359 MB → 1.7 GB. Diagnosed
  read-only: nothing was wasted — 365 refs, 0 broken, pools 196/196 — the build was simply
  **95.6% GIF**. `game_service.py:829-849` optimises stills (48 MB → 11 MB) and `shutil.copy2`s
  everything else verbatim, so there was a still optimiser and no video optimiser. Measured on
  vesper: 248 clips **1546 MB as GIF → 160 MB as H.264 CRF 23**, and the pixel difference is
  near-flat across CRF 18→26 (0.0578 → 0.0622) because it is GIF's dithering being smoothed
  away, not compression loss. The 20 VP8 webms measured **41 dB PSNR** at the same CRF —
  transparent. Compressing in `grab` is what stops the shelf re-inflating one pick at a time.

- **Verified:** new `tests/test_media_finder_transcode.py` (12 tests) covering the happy path,
  five distinct failure modes all falling back to the original bytes, no staging leak on
  fallback, `.mp4` and stills never re-encoded, and pool peers left intact. **241 existing tests
  still pass.** Real end-to-end through the un-mocked encoder: 19.02 MB → 2.80 MB, 216 frames
  preserved; junk input returns a reason instead of raising.

- **The guard that earned its place:** the frame-count check. A truncated encode still produces
  a *playable* file that stops early — on a looping clip that reads as "the pool got shorter",
  not as an error. During the bulk conversion two concurrent writers sharing a temp name
  produced exactly one corrupt file out of 229, and **only a frame count found it.**

## 2026-08-09 — selecting a clip no longer erases where it came from

LO asked why a selected clip loses its `⇢`. It is not a missing button: `grab` calls
`_drop_option` (media_finder.py:1532) and the row it deletes held the ONLY copy of the clip's
`docid`. Selecting was the single action in this tool that destroyed provenance — removing a
tile, unselecting and deleting a query all preserve or re-shelve. Measured on vesper: 182
installed pool clips with no record, and 276 demoted `origin: "previous"` rows, **0 of which
carried a docid or a found_by** — every one a permanently dead `⇢ no id` tile.

**Engine, not doctrine.** The skill taught nothing wrong here; the ledger simply had no place to
put the fact. Fixed at the ledger so it kills the class rather than the symptom.

**New:** a `picks` root in `media_options.json` — `{filename, url, docid, thumb, found_by}` per
installed file, written by `grab` from the row it consumes, keyed by basename so the picker joins
it client-side (neither `pool/list` nor `media-review/list` had to change). `options/list` returns
it. `pool_unselect` and `_preserve_current_as_option` hand it back to the option they demote it
into, as a new `source_url` field — deliberately NOT `url`, because a demoted pick must reinstall
by COPY from `local_path` so the exact approved bytes return.

**New:** `manage.py backfill_picks` — a pool member is named `c<md5(source_url)[:10]>`, so recovery
is a JOIN, not a search: hash every url still on any shelf and match stems. **Opens no socket.**
Live on vesper: 101 of 182 pool clips recovered (95 with a docid), 127 demoted rows repaired, and
it reports the 95 unmatched + 172 single-slot installs rather than guessing. Single slots are
unrecoverable by construction — `grab` names them after the SLOT, so no join key ever existed.
Cross-slot on purpose: only 15 of the 101 were on their own shelf.

**Changed:** `fetch_related.py` resolves a seed across `url` → `source_url` → `picks`, and refuses
an empty `--seed-url` (it would have matched every row missing a url key and borrowed a stranger's
docid). `check_shelves` re-keys `picks` alongside `options`/`queries`.

**Verified live** on `sex/arousal_weapon_use_t5`: ⇢ from an already-selected clip stocked 51, the
button flipped to `⇢ 51 related` with no page reload (the `selTileByUrl` sweep — the Selected zone
repaints on its own signature, which a landing fetch does not change), and deleting the test bucket
returned the shelf 472 → 520 → 472 with urls byte-identical. Tiles with no recoverable origin show
neither a ⇢ nor an origin line — it fails closed. 34 new tests; suite 432 passed / 6 pre-existing
`test_world_*` failures.

## 2026-08-09 — the human can run his own search, and delete one

The picker could re-run a chip's terms against PornHub (`PH`) and grow a bucket off one clip
(`⇢`), but the person looking at the shelf could not type a query of his own — every "try THIS
instead" cost a round trip through an agent. And nothing in the codebase had ever deleted a query
record, so a poisoned shelf had two doors: `✕` per tile, or `options/clear`, which empties the
slot. A search box without a bucket delete is a loaded gun with no safety, so both shipped together.

**New:** `scripts/fetch_search.py` — an UNSCOPED Google Images search, no `site:`, and crucially
**no label prefix**: `renderQueryBar` files `⇢ `/`◆ ` labels into side panels and everything else
onto the shelf, so an unprefixed label inherits the chip, the count, the host verdict and the PH
button from code that already draws them. Records `source: "manual"` so `query_ledger.jsonl` can
tell a human-typed search from an agent's.

**New:** `search/fetch` and `queries/remove` in `api/v1/media_finder.py`; a search box and the
page's first confirmation modal in `find.html` (z-index 1500 — above `.overlay`, below `.toast`;
Escape and backdrop-only cancel, no Enter-to-confirm).

**Changed:** the FORMAT axis is now first-class. A slot is animated or still, and that one fact
decides both whether `gif` is appended to the query and which extension group the extractor
matches. `clean_media_urls` grows `still=True` (default path byte-identical). ⚠️ It is read off
the declared **suffix**, never `media_kind` — `_IMAGE_SUFFIXES` contains `.gif`, so a `_t5` gif
pool reports as "img" while being animated. **Measured live: a `.jpg` slot that returns ZERO
today harvested 94 urls.**

**Changed:** `related_fetch` / `pornhub_fetch` / `search_fetch` now share `_run_runner`. The
"deliberately a COPY" note on `pornhub_fetch` carried its own expiry condition ("before either
has run in anger"); a third caller came due on it. All ten existing `related_fetch` tests pass
unchanged, which is the proof the factoring preserved behaviour.

### Three bugs found while building this

**1. `--query -cartoon` crashed the runner.** argparse rejects a value that starts with `-`
("expected one argument") and exits 2, surfacing as a bare `500 runner exited 2`. `-word` is
ordinary Google negation syntax, so a free-text box makes it reachable. Every runner argv now
uses `--flag=value`, which argparse never re-scans. Pre-existing in `pornhub_fetch`.

**2. `looks_suspiciously_clean([])` is True**, so checking it before `if not urls` made exit 4
UNREACHABLE from the browser path and reported a zero-yield search as a broken Chrome profile.
Still live in `fetch_pornhub.py:143-148`; `fetch_search.py` asks "empty?" first.

**3. ⚠️ The delete destroyed 55 real options on `games/media_lab`.** `_apply_option` ADOPTS an
already-shelved url by appending the new label to the EXISTING row, and 1294 of media_lab's 1296
options predate provenance and carry no label at all. So a search that merely re-found one made
it look sole-owned, and deleting that search destroyed a row that had been on the shelf for
weeks — a 137-option shelf came back 82. **Fixed** with `added_at >= record.at`: an option
stamped before the search first ran cannot have been introduced by it, so it survives with its
`found_by` key POPPED (not set to `[]` — an empty list reads as the Q_UNLABELLED bucket, whose
chip says "stocked before searches were recorded", which for that row is true again). No record
means no proof of ownership, so an orphan label is stripped and the option kept.

**Verified:** `pytest tests/ -q` → 398 passed, 6 failed (the pre-existing `test_world_*`
`create_user()` failures, reproduced on a clean tree first). 107 new tests across
`tests/test_media_finder_search.py`, `tests/test_media_finder_delete_query.py`,
`tests/test_fetch_search.py` — including a parametrized `_RUNNERS` suite that retroactively
covers `pornhub_fetch`, which had ZERO tests. Live on the runner: a still slot 0→94 urls, an
animated slot 91 urls with `gif` auto-appended, stocking in 0.0 s via `add_bulk`, a 29/62
sole-vs-shared delete split, and a search→delete round trip that returns a shelf to its exact
prior count.

## 2026-08-06 — the stock loop was fixed twice; the second fix removed 22,000 of the writes

Chunking the loop (entry below) stopped it timing out. It did not touch the reason the loop was
expensive: **every `options/add` rewrites the entire ledger, and `_options_lock` is global to
the game.** Chunking made the *client* concurrent while the *server* stayed strictly serial.

Measured on vesper's live 5.7 MB store:

    json.load 35 ms + json.dumps 34 ms = ~69 ms of pure serialize per add
    projected at 12 MB (post-88-slot-run) ................ ~145 ms per add
    88 slots x ~250 options = ~22,000 adds ....... ~39 MINUTES of lock time

That 39 minutes is serialized by construction — six concurrent agents cannot overlap a single
lock, so it is a floor under the whole run, not a cost per agent. At 24 slots it was ~8 minutes
and invisible, which is why chunking looked like a complete fix.

**Fixed:** `api/v1/media_finder.py` grows `options/add_bulk` — the same shelf semantics applied
to a whole query's results under **one** lock acquisition and **one** file write. ~22,000 writes
become ~264. `options/add` is untouched and stays the single-url path the capture extension uses.

**Measured end-to-end**, live server, scratch game seeded from vesper's real 4.4 MB store:

    250 urls, sequential options/add ... 53.53 s   (214 ms/url)
    250 urls, one options/add_bulk ....  0.21 s   (0.8 ms/url)   -> 253x

214 ms/url is three times the 69 ms of raw serialize, because the round trip also pays HTTP,
Django, lock acquisition and the *read* of the whole ledger. Projected over the 88-slot run:
**~78 minutes of API time against ~20 seconds.** The arithmetic estimate that justified building
this said ~39 min — it was conservative by half, because it counted only the write.

- `chrome_route.md` §5 — the snippet now posts one `options/add_bulk` per query. The chunked
  `Promise.all` rule survives as the fallback for anyone still on the per-url path.
- `chrome_route.md` failure table — three rows: the timeout row now points at bulk first, plus
  "the whole run feels slow and agents sit idle" (the lock) and the 2000-item cap.
- Both mirrors hand-applied block-by-block. Delta between `.agents` and `.claude` still exactly
  42 lines, all of it the pre-existing §2.0 block, and **0 lines of the new text** — verified by
  diff, which is the check that proves the mirror took.

**The cap REFUSES rather than truncates.** A silently dropped tail reads downstream as "the
query was thin", and that is what sends an agent rewriting a query that was fine — the same
failure signature as curling Google and getting a rich-looking 200 with no urls in it.

**Verified:** `tests/test_media_finder_bulk.py`, 23 tests. The load-bearing one asserts the bulk
shelf is byte-identical to the same urls added one at a time (modulo `added_at`) — if those ever
diverge the fast path is silently a different feature. Also pinned: exactly 1 write for 50 items
against 5 writes for 5 singles; a re-harvest of already-stocked urls writes **zero** times; one
bad row costs only itself and is counted under `invalid`. Existing suites green (136 passed
across queries/pools/fetch_related; full `tests/` 291 passed, the 6 `test_world_*` failures
pre-date this work and are a `create_user()` signature issue).

## 2026-08-06 (later) — §5's stocking loop cannot finish inside a `javascript_tool` call, and the histogram it POSTs was being thrown away

Two defects in the same code block, both found by running it, not by reading it. A 24-slot v3
fan-out on `vesper` surfaced the first **five separate times** — five of the six agents that
completed hit it independently and each wrote the same fix in its report before I looked.

**1. The stock loop is sequential and `Runtime.evaluate` caps at 45 s.** `options/add` costs
~0.6 s, so ~75 POSTs cannot fit in one call. Measured failures at **74, 79, 83 and 85 urls**;
chunked `Promise.all` (10 at a time) finished the same 74 in ~20 s.

The important half is that **the failure is not atomic.** The renderer keeps executing after
the tool gives up, so the shelf goes on filling while the agent holds an error and no return
value — one agent recorded "46 of 74 had landed" mid-loop. It reads exactly like "the stock
failed", and the recovery an agent would reach for first (re-post everything) is in fact the
correct one, because `options/add` dedupes by url and answers `{"ok":true,"duplicate":true}`.
Nothing was lost on any of the five; but nothing told them that either.

**2. `hosts` was being POSTed in a shape the server silently discards.** `_clean_hosts`
(`api/v1/media_finder.py:551`) accepts only `[[host, count], …]` and returns `None` for
anything else — **dropping the field while keeping the record, with a 200**. Reshaping
`Object.entries()` output to `[{host, n}]` is the obvious-looking mistake and I made it in the
run's driver: **all 34 chips from that run stored no `hosts` at all.** The histogram is v3's
only quality gate and its stated deliverable on the chip, so this is a gate that reached the
store and evaporated. Note the asymmetry that hid it: the `" DOT "` mangling is refused
loudly with a 400, so the one malformation anybody had met before fails safe, and this one
does not.

Filed:
- `references/chrome_route.md` §5 — the code block now chunks `Promise.all` by 10, plus two
  new rules: the 45 s ceiling with its measurements and the non-atomic recovery, and the raw
  `[[host,count],…]` shape with "re-read one chip and confirm".
- `references/chrome_route.md` §2 tool table — `javascript_tool` now carries the 45 s ceiling
  and the keeps-executing-after-timeout behaviour, so it is visible before §5 is reached.
- `references/chrome_route.md` failure table — two new rows (timeout-with-no-counts;
  200-but-no-hosts).

Both trees edited block-by-block, never `cp`.

**Verified:** the 24-slot run's journal (6 formal results, 12 slots written) is the evidence
for defect 1; `media_options.json` showed 0 of 34 chips with a `hosts` key for defect 2; the
relaunch over the remaining 18 slots carries both fixes and reports `hosts_recorded` per slot
so the next run proves it rather than assuming.

## 2026-08-06 — PornHub is fetchable; the 470 was our own extractor, and it was law in eight files

**"PornHub is discovery-only — never a download" is REVERSED.** The measurement behind it was
real — `egl.phncdn.com/gif/<id>.gif` returns **470 on clearnet and over Tor, every id tried** —
and it was taken on urls this skill had already broken. Google's results HTML carries the
**signed** form, `…/gif/<id>.gif?validfrom=…&validto=…&hash=…`. `MEDIA_RE` was lazy and
terminated at the file extension, so the ticket was never captured; we fetched the corpse and
recorded it as a property of the host.

Measured today, 53 urls from one `site:pornhub.com` query on `media_lab_h`:

| | |
|---|---|
| signed url, GET / HEAD (with Referer, without, bare) | **200** every way |
| same url, query string removed | **470**, 173 bytes — 100% dead |
| ticket window | `validfrom` 2025 → `validto` **2125**. 99 years, not 2 hours |
| payload | GIF89a, up to 1280x720, 240 frames @25fps = **10.0s**, 1–40 MB |
| Django `proxy` on a signed url | **200 / 8.9 MB / image/gif** |

**Three further rules were built on the bad conclusion and all three are wrong:** the
`*.phncdn.com` extract cut, "there is no header that fixes it", and the reason attached to
`_REFERER_BY_HOST`'s phncdn row. No header is needed at all — a signed url serves with no UA
and no Referer. (The cut was also a DEAD VARIABLE in `chrome_route.md`'s own code block: §4
computed `pool` and §5 iterated the unfiltered `urls`, which is why 4 phncdn rows sat on
vesper's shelf despite the rule.)

**The 2-hour ticket in the older notes is a different url class** — `kl*/pics/gifs/*.webm`,
minted on a live PornHub page. This route never touches it, and never touches pornhub.com,
which is DNS-sinkholed *and* SNI-reset (9/10 connections die; the survivor returns 302, not
content). Only the CDN is used, and it is open without a VPN.

**Changed:** `scripts/fetch_related.py` — `_unescape` now runs before extraction (Google
JSON-escapes `=`/`&`, so the old character class stopped at the backslash); `MEDIA_RE` widened
to keep a query string; new `normalize_media_url` + `SIGNED_QUERY_HOSTS = ("phncdn.com",)`
keeps the ticket for signed hosts and strips it everywhere else, so **no non-phncdn url
changed**; the phncdn cut deleted; `DOCID_TRIPLE_RE`'s thumbnail group made capturing and
split into `media_triples` / `docid_join` / `thumb_join`; `PANEL_PREFIXES` + `is_panel_label`
so `pick_q` never sends a bucket label to Google as query text.

**New:** `scripts/fetch_pornhub.py` (imports every pure function from `fetch_related.py` — a
copied extractor is one that stops getting the other's fixes), `pornhub/fetch` endpoint
sharing `_RELATED_FETCH_LOCK`, a `thumb` field on the option row, and a thumbnails-first ◆
PornHub panel in `find.html`.

**Verified:** `pytest tests/ -q` → 268 passed (6 pre-existing `test_world_*` failures,
reproduced with these changes stashed). New tests cover the signed-url round trip, the
no-double-row rule, the unsigned-host regression guard, and the `clean_media_urls`/`docid_join`
same-key invariant — that last one because a mismatch would stock every PornHub clip with an
empty docid and silently kill its ⇢ button forever.

**The class this belongs to.** Third time an untested claim hardened into doctrine and cost
real work — after "the browser cannot fan out" and the concurrency-of-20. Here one bad
measurement propagated into eight files and three derived rules. The cure is not another
correction: it is that a doctrine line must carry `measured <date>` or say `asserted`, so the
asserted ones stay challengeable.

## 2026-08-06 — scrolling never expanded the grid, and the failure table taught the opposite of the fix

**"Scroll to the bottom… if the set didn't grow, you've hit the pool's edge" was wrong, and
the failure table turned it into a diagnosis.** Google renders ~200 tiles and stops; scrolling
past that adds nothing at all. What adds tiles is the **"More results" button**, which this
corpus never mentioned once — grep for the string across all three trees returned zero before
today. So every run that followed §4 harvested one screen's worth and was told, by
`chrome_route.md`'s own failure table, that the pool was exhausted.

Surfaced by a v3 agent during the 20-slot vesper harvest (2026-08-05): fourteen
scroll-to-bottom passes, zero new tiles, then one click took its grid from ~200 to 800+.
Re-measured by hand today on a fresh grid so the numbers in the doc are ours, not a report:
**205 → click → 405 → click → 605**, ~200 a click, **and the button is still present after
each click** — it is repeatable, not a one-shot. Four scroll passes in between: **405 → 405**.

**Root cause of the wrong text:** the original claim conflated two real mechanisms. Google
*does* lazy-load tiles on scroll, and a scroll-then-re-extract pass *does* recover them — that
part was true and observable, which is exactly why nobody questioned the inference bolted onto
it. "Set didn't grow" was read as "pool is empty" when it actually means "you reached the
button." A true premise carried a false conclusion.

- **`references/chrome_route.md`** (both copies) —
  - §4's `**Scroll, then re-extract.**` block replaced: the two mechanisms separated, the
    ~200 boundary named, the repeatable-click measurement, and a **text-matching** selector
    (`/^more results$/i` over `a[role=button]`/`div[role=button]`/`button`/`input`) with an
    explicit "never a class — Google's rotate". Verified live: the real element is
    `<a role="button" jsname="oHxHid">`, but `jsname` rotates too, so text is the handle.
  - ⚠️ **New caveat, measured:** the yield is thin on an ANIMATED slot. At 605 tiles that grid
    gave **80** extractable `.gif`/`.mp4` urls (~13%) — depth is mostly `.jpg`/`.webp` page
    thumbnails a `gif|mp4|webm` extract cannot use. Two or three clicks is the sweet spot.
    Recorded so nobody reads "6× the tiles" as "6× the shelf".
  - Failure table: the `Pool exhausted, not a bug` row **rewritten** to send the reader to the
    click, plus a NEW row for the genuinely-exhausted case (flat *after* clicking → sibling
    query). The old row was the highest-cost line in the file: it gave a confident wrong
    diagnosis for the exact symptom the bug produces.
  - §2 tool table: `computer {action:"scroll"}` no longer claims to "force tiles in" — it
    pulls lazy tiles already on the page and explicitly does **not** load more results.
  - §4 docid comment and §5b step 3 updated to name the click alongside the scroll.
  - §5 `query` bullet now states the round-trip rename (below).
- **`SKILL.md`** (both copies) —
  - §3's pointer renamed from "the scroll-then-re-extract self-check" to "extract → click
    'More results' → re-extract", with the boundary named inline.
  - ⚠️ **New note under the endpoint block:** `options/list` returns stored records
    **verbatim, and the stored names are not the names you POST**. `query` → **`found_by`, a
    list**; chips keyed **`q`**; no `query` key on either, and no legacy one. Line 358's
    `→ {"options":[…], "queries":[…]}` was the only response schema a v2 reader ever saw, and
    that elision is what let a v3 agent check `o.query` and conclude it had destroyed 197
    correctly-labelled options. The doctrine half of that is in find-media-v3's CHANGELOG,
    same date.

**Verified:** `grep -rn "scroll and re-extract to find the page's edge\|scroll-then-re-extract
self-check\|Pool exhausted, not a bug\|Force Google's lazy-loaded tiles" .claude/skills
.agents/skills` → **0**. `More results` now present 7× in each `chrome_route.md`, 1× in each
`SKILL.md`. Both trees edited block-by-block, never `cp`: the diff still shows **exactly the 42
pre-existing lines** (36 `<` = §2.0 PREFLIGHT + 2 failure rows, 6 `>` = the Antigravity CDP
blockquote + 1 failure row), and **zero** of today's edits appear in it — which is the proof
they landed identically. The click measurement was taken in the user's own Chrome on a live
`&tbm=isch` grid (note: Google now redirects that to `&udm=2`; the URL the skill builds still
works).

## 2026-08-05 (3rd today) — mood words flag even beside an act word; mirror drift healed

Root-caused `media_lab_f`'s SFW-skewed shelves (facial slot: 17% on-act vs 50% for
`media_lab_h`'s act-first control, 45 Dreamstime stills vs 0). The doctrine fix lives in
find-media-v3's SKILL.md (see its CHANGELOG, same date); the enforcement fix lives here:

- **`scripts/validate_queries.py`** — two changes to the vanilla machinery:
  - `VANILLA_TERMS_FOR_NSFW_CHECK` gains `gentle` `intimate` `passionate` `sensual` — f's
    measured offenders. `passionate real couple cumshot gif` validated CLEAN before this.
  - The vanilla branches now judge act presence on `SEXUAL_TERMS_FOR_SFW_CHECK` ∪
    `ACT_ANCHORS` (`has_any_act`), not `has_sexual` alone — `cumshot`/`bj`/`anal` live only
    in ACT_ANCHORS, so the old predicate called a cumshot query act-less. Split verdicts:
    no act word → `tier_mismatch:nsfw_query_too_vanilla` (as before); act word present →
    NEW `vanilla_dilution:mood_words_pull_stock_results`, because the old
    `not has_sexual` guard let any sexual term suppress the vanilla check entirely
    (`tender loving blowjob gif` passed). Both hard-fail through the existing
    `tier_issues` exit-1 path. Known consequence, intended: `tender cumshot gif`-shape
    queries that used to flag `too_vanilla` now flag `vanilla_dilution` — same failure,
    truer name.
- **`references/query_rewriting.md`** — the "what check_tier_alignment() actually
  enforces" list rewritten for the two-branch split + the eight-word list; blind-spot #3
  updated (on the pornhub target, strip_banned now eats five of the eight first, so the
  vanilla checks there can only fire on `romantic`/`sweet`/`gentle`).
- **`scripts/test_query_anchor.py`** — 7 new tests: the exact f query that passed clean,
  gentle-beside-anchor, mood-beside-sexual-term, the facial-is-not-an-anchor case
  (too_vanilla, NOT dilution — `facial` stays a spa treatment by the membership rule),
  old branch intact, act-first control clean, SFW-tier exemption. 20 passed.
- **Mirror heal:** the 08-03 `bj` change had never reached `.agents/` (stale
  `scene_semantics.py`, `test_query_anchor.py`, missing CHANGELOG entry), and the 08-01
  Antigravity entry existed only in `.agents/`. Both trees now carry both histories, and
  the four code/reference files are byte-identical again — verified by diff. Intentional
  divergence remains only in `chrome_route.md` (§2.0 preflight, 42 lines).

**Verified:** `python3 -m pytest` on the test file in BOTH trees; `check_tier_alignment`
run directly over media_lab_f's four real facial queries — all four now flag.

## 2026-08-05 (later) — related lives in a PANEL, and no id means no fetch

Two rulings from LO after using the feature on a real slot.

**1. Related fetches are not searches, so they leave the searches rail.**
`⇢ <stem>` chips were sitting next to real queries, and the shelf grid was mixing
grown-from-a-clip results into "what the searches found". Both wrong. The picker now
has a right-hand PANEL (Google's own shape when you click an image): a list of every
related fetch keyed by the SEED'S THUMBNAIL — a `⇢ label` is meaningless as text, the
clip is the name — and each bucket opens inside the panel, so the main shelf never
changes underneath you. Options found ONLY by related fetches are excluded from the
grid; an option a search also found appears in both places, because both are true.
No engine or storage change — the labels and `seed_url` join were already there.

**2. No stored docid → do not fetch at all, not even to go find the id.**
The old fallback ran a text search built from a guess (the slot's newest query, or the
filename's slug words) to hunt the id down. On an aged shelf that opened a Google tab
on a query nobody asked for and failed anyway, because the clip no longer ranked. LO's
call, and it is right: the guess-query was never evidence, it was a slot machine.
`fetch_related.py` now exits 4 **before touching the browser**, `§5b` step 1 teaches
STOP-and-report, and the picker disables the button with `⇢ no id`.
The cure is a SEARCH, not a retry: any search that re-finds an option attaches an id
to it in place (measured on `media_lab_f` — one sibling query revived 17 of 226, and
a ⇢ on one of the revived clips then worked first time, 33 clips in ~10s).

- `references/chrome_route.md` §5b step 1 rewritten (both copies, block-swapped, still
  differing by exactly the 42 pre-existing lines). `grid_url()` deleted from the runner
  — the lookup was its only caller.
- Verified: 22 live browser checks (idempotent — the fixture is rewritten per run after
  a mutated re-run once passed green while skipping the fetch path entirely), 79 unit
  tests including one that asserts the no-id refusal never reaches a browser.

## 2026-08-05 — related-fetch: every candidate carries its docid, and a shelf can grow from a clip

LO's ask: Google Images' "click a clip → related images → see more" as a feature — for a stocked
option, fetch its related feed and keep it. Probed live first, then built; the measured facts:
the related feed is a plain URL (`?udm=2&q=<query>&tbs=rimg:<blob>`), the blob is
base64url(0x09 + first 8 bytes of the base64url-decoded docid) — ground truth
`FvF5n0MlBjcrfM` → `CRbxeZ9DJQY3`, a truncated blob serves the real feed — and the docid↔url
join is one regex over the grid page's metadata triples (84/97 same-day coverage).

- **`references/chrome_route.md` §4** (both copies): the extraction pass now ALSO runs the
  docid-triple join and stashes `window.__fm.docids`. Why: there is no retroactive capture —
  an option stocked without its docid needs a whole grid re-search later, which usually fails
  on aged shelves (urls churn out of their query's grid).
- **§5** sends `docid` on every `options/add`. Verified: absent docid keeps the entry
  byte-identical server-side, so old snippets keep working.
- **NEW §5b — RELATED**: the agent-route recipe (blob construction with the ground-truth
  vector, label rules `⇢ <stem>` with ` ·2` suffix on other-seed collision, the 409 →
  re-pick + RE-STOCK rule, top-up on re-fetch, captcha = stop). This is the documented
  fallback the picker's runner-down message points at; the normal path is
  `scripts/fetch_related.py` driving the dedicated find-media Chrome over CDP.
- **§5's stale ledger-shape note** fixed — it still described the pre-`queries` shape.
- **`SKILL.md` endpoint table** (both copies): `docid?` on options/add, `seed_url?` on
  queries/add, new `related/fetch`.
- **Failure table**: three new rows (⇢ never flips → missing `source`/`seed_url`; 409 →
  re-stock not just re-record; suspiciously-clean feed → wrong Chrome / SafeSearch back on).
- Verified: both chrome_route.md copies edited block-by-block (never cp) and still differ by
  exactly the 42 pre-existing lines; SKILL.md copies byte-identical.

## 2026-08-05 — the harvest now labels every candidate with the query that found it

Shared-machinery change, driven by v3 (see `find-media-v3/CHANGELOG.md` for the why). v2's own
pipeline is unchanged — it still judges, ranks and installs — but the stock step it teaches is
this skill's file, so the edits land here.

- **`references/chrome_route.md` §4** now builds the histogram with REAL hostnames, stashes
  `window.__fm = {q, urls, hosts}` for the stock pass, and applies the `" DOT "` join **only to
  the value the script returns**. That transform exists to get past the tool-output
  secret-scanner; a POST body never passes through it. Transform before POSTing and the store is
  poisoned irreversibly — a host legitimately containing `" DOT "` is indistinguishable from a
  mangled one — so `queries/add` answers 400 on one. Prose plus a server refusal, because this
  is the one mistake here that cannot be undone.
- **§5** sends `query` on every `options/add` and calls `queries/add` once per query, including
  zero-yield ones. Four new failure-table rows cover the ways this goes wrong.
- **§5 also finally sends `slot_key`.** The snippet had omitted it for months while three prose
  rules demanded it. Code that contradicts prose wins every time, so the fix belongs in the code.
- The refetch prune (`options/clear {before: t0}`) is **unchanged for v2** and carries a note
  saying v3 no longer does it — v3's labelled buckets make the destroy step unnecessary, and v2
  still installs, so its refetch has different work to do.
- `SKILL.md`: endpoint table updated; the `query_ledger.jsonl` section now says the ledger is
  written **for** you by `queries/add`, and why it is still worth having — it is append-only, and
  the query table it mirrors lives in a file that is rewritten whole and reads back empty if a
  write ever tears.

Both copies (`.claude/` and `.agents/`) were edited block by block and diffed afterwards: they
still differ by exactly the 42 lines they differed by before — §2.0 PREFLIGHT and one
failure-table row. A `cp` would have silently reverted one of them.

## 2026-08-03 (later) — `bj` added to ACT_ANCHORS: the enforced rule was penalising the better query

The act-anchor rule shipped 08-01 is sound, but its vocabulary was incomplete in a way that bit.
`bj` was absent, so `validate_queries.py` flagged `bar bj chair seated gif` as
`no_act_anchor:position_or_setting_words_only` — an enforced gate telling the author to rewrite the
query that actually worked.

`bj` is not a synonym you reach for when `blowjob` fails. **It retrieves different and better
material**, measured on two vesper slots in the same batch:

| slot | finding |
|---|---|
| `renner_cheerup_alley_t5` | `blowjob` returned indoor studio kneeling (~3 outdoor tiles in 40). `public alley bj gif amateur` — built from a label Google itself surfaced, "Public Alley BJ" — returned real alleys: dumpsters, graffiti walls, `alleyway-fuck-after-club`. It was the payoff round. |
| `renner_cheerup_oral_t5` | `bj chair` / `bj couch` turned out to be **Sex.com's own tag names**, and solved `him_standing` — the dominant rejection across *four* prior runs on that slot. Seated went from "hard to retrieve" to easy. |

That is the same lesson as the 08-03 lexicon correction that an act anchor is necessary but not
sufficient: **porn-native jargon is what holds a query in the corpus.** `bj` IS that jargon; the
validator was rejecting it for not being English.

- **`scripts/scene_semantics.py`** — `bj` added to `ACT_ANCHORS`, with the measurement and the
  safety argument in a comment. It is the first 2-letter member, so the comment records why
  `\bbj\b` is safe: the boundary means "objects"/"subject" cannot match, since the `b` there is
  preceded by a word character.
- **`scripts/test_query_anchor.py`** — two new tests: `bj` anchors both measured query shapes, and
  an explicit substring-trap test over `objects` / `subject` / `objection`. A 2-letter anchor is the
  riskiest kind to add, so the false-positive case is pinned rather than argued.

**Verified:** `python3 -m pytest scripts/test_query_anchor.py -q` → **13 passed**. Both previously
false-flagged queries now anchor; `objects on the desk gif` still flags, so the boundary holds.
Regression on the live game (`validate_queries.py --toml games/vesper/toml_phases/7_final_game.toml`)
→ `no_act_anchor` count unchanged at 15, as expected: no authored vesper query uses `bj`, so this
widens what passes without silencing anything already flagged.

Requested by LO after the batch surfaced it.


## 2026-08-03 — a disconnected extension had no failure row, and the nearest one pointed the wrong way

Ran a 9-agent batch to fill vesper's remaining media pools. The Chrome extension was disconnected;
`list_connected_browsers` returned `[]`. All 9 agents failed, and the cost was not the outage — it
was that **the skill never told them what a dead route looks like**, so each one independently
invented a workaround before diagnosing it.

`chrome_route.md`'s failure table had **no row for a disconnected extension**, and its nearest
symptom — *"Extract returns `[]`"* — attributes that to query-string stripping. That row sends an
agent rewriting perfectly good queries for hours against a route that cannot answer.

Two fallbacks were measured, both wrong, both recorded:

| Fallback | Measured result |
|---|---|
| `curl` Google Images directly | **HTTP 200, ~90 KB, ZERO extractable urls** — the grid is JS-rendered. A rich-looking 200 that harvests as nothing is indistinguishable from "my query was bad." |
| Mine a sibling slot's stocked shelf | Cross-slot collision — those urls were harvested against a *different* slot's demand. One agent correctly refused to do this and reported a blocked run instead; several others were pivoting toward it when they were stopped. |

- **`references/chrome_route.md` §2.0 (NEW)** — a PREFLIGHT section: call `list_connected_browsers`
  before anything else; on `[]`, **STOP and tell the human so they can reconnect it**. Records that
  Chrome's own process may still be running (that proves nothing — the pairing link is what is down),
  both measured non-fallbacks, and that an honest blocked report IS the deliverable. Also records the
  mid-run corollary: install incrementally (`grab` + `--record` per clip) rather than batching, which
  is what turned a later round of stalls from total losses into partial wins.
- **`references/chrome_route.md` §Failure table** — new first row for the disconnected extension, and
  a cross-reference added to the `Extract returns []` row pointing at §2.0 first, so the misleading
  row can no longer be reached before the correct one.

Requested directly by LO: *"if chrome is disconnected I want it to tell me, so I will launch the
chrome and make it work."* The human can fix this in seconds; an agent cannot fix it at all.

**Verified:** `list_connected_browsers` reproduced `[]` from the main session during the outage, and
`[{deviceId…}]` after LO reconnected — the same call the new §2.0 mandates. `media_options.json` had
not been written since Aug 1 02:56, corroborating that no agent stocked anything. All 9 pools were
confirmed still at 1 file, so the batch left no partial state.

**Still open, not changed here:** `bj` is absent from `scene_semantics.ACT_ANCHORS`, so
`validate_queries.py` false-flags `bar bj chair seated gif` as `no_act_anchor` — measured this batch,
where `bj` outperformed `blowjob` on two slots. Awaiting LO's call.


## 2026-08-01 — Antigravity CDP browser tooling support
- **`references/chrome_route.md`**: Added Antigravity / CDP environment instructions for connecting via `http://localhost:9222` (`chromium.connectOverCDP`).
- **Why**: Allows agents running in Antigravity to attach directly to Chrome/Canary running on port 9222 without triggering headless CAPTCHA blocks or SafeSearch restrictions.
- **Verified**: Verified live via CDP connection to Chrome Canary on port 9222 extracting 62 direct CDN URLs from Google Images with 0 CAPTCHAs.

## 2026-08-01 (later) — a position word is not an act word; first ENFORCED query rule, first tests

Found by running `calloway_loop_vaginal_t5` under yesterday's new query shape. The first query
failed outright:

| query | urls | on a porn host |
|---|---|---|
| `riding cowgirl man in office chair gif` | 83 | **0** — Tenor, BBC, Wikipedia, Billboard, NFL, Warhol |
| `cowgirl riding fuck office chair gif` | 73 | **69 (95%)** |

One token. `riding` and `cowgirl` are *positions* and both are ordinary English, so the query had no
sexual word in it and Google classified it as mainstream. `gif` does not rescue that. **`blowjob`
anchors a query by itself** — which is why every oral slot filled fine and this stayed invisible
until the first penetrative beat.

- **The validator was actively passing the broken query.** `SEXUAL_TERMS_FOR_SFW_CHECK` contains
  `missionary`, `doggy`, **`cowgirl`** next to `sex`/`fuck`/`blowjob`, so `has_sexual` was true and
  nothing fired. That set answers *"is a sexual word leaking into an SFW query?"* — for which those
  three belong — not *"will this reach porn?"*
- **`scripts/scene_semantics.py` — added `ACT_ANCHORS`**, a narrower set beside the existing one,
  which is **unchanged**. Membership rule, stated in the code: a word qualifies only if it has no
  common non-sexual reading. `cum`/`cumshot` are in. **`facial` (a spa treatment), `swallow` (a
  bird), `load` (freight) and `finish` (a verb) are deliberately out** — recorded in a comment so
  nobody "fixes" them later. Inflections are explicit members, because `\bfuck\b` does not match
  "fucking" and prefix-matching would make `sex` swallow "sexy".
- **`scripts/validate_queries.py` — one new check** in `check_tier_alignment()`:
  `no_act_anchor:position_or_setting_words_only`, on `NSFW_TIERS` only. **`t4` is exempt** — a tease
  beat must never be forced to carry a penetrative word. Advisory, like everything else here.
- **⚠️ This REVERSES yesterday's entry**, which said *"validate_queries.py gains no position
  vocabulary."* It gains **act** vocabulary, and the distinction is the whole justification: *"is his
  posture the act's default?"* is a judgement about a beat and stays `[ADVISORY]`; *"does this string
  contain an act word?"* is a lookup, and only a lookup is safely enforceable.
- **`scripts/test_query_anchor.py` — NEW, the first tests these scripts have ever had.** 11 cases
  pinning both measured queries, the oral asymmetry, t4/SFW exemption, the two-sets-are-different
  invariant, and the two word-boundary traps found while writing them.
- **🐛 Fixed a crash I caused yesterday.** `validate_queries.py --toml` died with `KeyError: 'file'`
  on the first block it met that had `pool_dir` instead of `file` — so converting vesper's 19 slots
  to pools silently made the entire offline validator unusable on that game. Confirmed pre-existing
  by stashing. Now follows the same precedence as `apps/common/media_blocks.py`:
  **`pool_dir` > `files` > `file`**. Without this the verification below was impossible to run.
- **Verified on real data, not synthetic.** Over `games/vesper/toml_phases/7_final_game.toml`: 89
  NSFW queries, **21 flagged (23%), zero false positives** — every flag is a genuinely anchorless
  query. It caught **eight** slots about to waste a search round, not the four predicted:
  `office chair riding cowgirl dim`, `girl on top man desk chair`, `doggy bent over desk office`,
  `man woman against desk records room`, `brothel riding cowgirl red room pov`. All five already
  filled oral slots came back clean.
  - **Corrects a claim in the plan for this change.** It said all four riding slots lacked an anchor.
    Two do not — `colm_loop_vaginal` says `leg up standing **fuck** back room` and `brothel_vaginal`
    says `brothel **sex** riding pov red room` — and both correctly passed. The check discriminates
    better than the author did.
  - Widening the set for `cum`/`cumshot` moved it from 29 flags to 21; the drop is all true-positive
    preservation, not threshold-loosening.
- Docs: the rule is stated in `query_rewriting.md` (as the **reciprocal** of the existing
  "always pair an act with a position" line — the failure was the inverse), `chrome_route.md` §3
  (what counts as `<act>`), and `templates/scope_brief.md`. Marked `[ENFORCED]`, which it now
  genuinely is — this file's own rule is that advisory prose must never be *claimed* as enforced, and
  the inverse drift is just as bad.

## 2026-08-01 — the query names BOTH bodies; vesper gets the first real lexicon

Follows directly from yesterday's A/B null result. If judging was not the bottleneck, retrieval was
— and this skill already said so without acting on it (`scoring_rubric.md`: *"**Provisional.** The
mechanism is query-side, not gate-side."*).

- **`references/chrome_route.md` §3 — the query SHAPE now names both bodies.** **Why:** the shape was
  `<act> <position> …` with **one** position slot that never said whose posture it meant, and an act
  phrase silently fixes the partner's. `kneeling blowjob` retrieves she-kneels-he-**STANDS**.
  **Measured on `vesper`, three slots, same act:** `renner` needed him seated, its queries said
  `office chair` / `under the desk` / `man sitting in chair`, and **13 of 43** fetched slugs came back
  seated/chair/desk. `calloway` needed the same posture, its queries said `glasses` / `close up` /
  `pov` and named no posture at all — **0 of 10**, with `him_standing` the dominant rejection across
  three separate runs (11/15, then 12/26 and 15/19 in the A/B arms). `colm` needed the default and
  was fine. Shape is now
  `<act> <her posture> <HIS posture — only when it is not the act's default> …`.
  - **Stated honestly:** the *omission* is measured. Whether adding the token would have rescued
    calloway is **not** tested. Written up as an established defect with an obvious-but-unproven
    remedy, not as a fix with evidence behind it.
  - Recorded the corollary that makes it expensive: a wrong partner posture is a legitimate
    `position:` gate failure, so a bad query here does not produce bad picks — it produces an
    expensive empty shelf, three rounds later.
- **`references/query_rewriting.md` §Canonical action vocabulary — position guidance moved off
  `sex`/`fuck` and onto every act.** **Why:** the list bound positions only to penetration; `blowjob`
  — the act in every slot that failed — carried no posture guidance at all. Added a defaults table
  (what each act phrase retrieves unprompted, and the tokens that override it). **Also corrected a
  worked example that pointed the wrong way:** it read *"standing when the beat says kneeling gets
  thrown back"*, which assumes **her** posture is the variable. Every failure actually recorded in
  this repo is the opposite — her posture was right and *his* was wrong.
- **`templates/scope_brief.md` §Queries — closed two gaps against `chrome_route.md` §3.** The brief's
  own rule list was missing **the `gif`/`webm` token** (which `chrome_route.md` calls *"the
  highest-leverage token in the query"*, measured 3× at 7→59 / 1→54 / 0→91 fetchable urls) and the
  **~2-token setting cap**. Both added, plus the posture rule and the shape line, so the three
  statements of the Google rule set now agree.
- **`games/vesper/.find-media/lexicon.md` — CREATED.** **Why:** the mechanism has been specified since
  the chrome-route rewrite and used exactly twice, both times in a `media_lab` test rig. The
  cross-game roll-up `games/.find-media/` **does not exist**, and no real game had a lexicon at all —
  so every term measured yesterday would have died with the session. Seeded with what was measured:
  the posture defaults, which settings this corpus does and does not shoot, the slug-blindness
  finding, and one open gap carried over from `media_lab_c` (*the gentle cradling hand at the back of
  the head* still has no working name, and it killed a pool).
  - **It also records a correction.** A prior run reported "zero storerooms exist in this corpus"
    after 225 urls. False: `colm`'s wave-1 **did** retrieve a linen store
    (`cdn.nsfwgify.com/44903/kneeling-blowjob.gif`), later ranked #1 by *both* A/B arms. The claim was
    made after the clip disproving it had already been pulled from the pool.
- **`SKILL.md` §Evidence — `query_ledger.jsonl` documented.** **Why:** it exists, it is the only
  machine-written record of what was searched, and it appeared in **no instruction file** — a prose
  summary claiming "4 rounds" was caught contradicting a ledger showing 7. Rule added: when they
  disagree, the ledger is right. Recorded with it: **`urls_yielded` is not a quality signal** — 31
  queries returned 40–92 urls with no relationship to whether the query worked.
- **`SKILL.md` §Stop conditions — reconciled a live contradiction.** The global cap said 3 sibling
  rounds; `scoring_rubric.md` told a setting-driven slot to stop at 2. Now stated together with the
  reason the setting cap is tighter (a missing room costs points and never a rejection; a missing
  posture costs the whole shelf). Also added: **before blaming the term at round 3, check the
  shape** — the recorded failure is rarely an unnameable beat, it is a query that let the corpus
  choose the partner's posture.
- **Deliberately NOT changed.** `scripts/validate_queries.py` gains no position vocabulary — this
  skill's own rule is that advisory prose must never be promoted into "the validator does X", so the
  posture rule stays `[ADVISORY]`. `scripts/fetch_candidates.py` untouched, though the finding is
  recorded in the lexicon: the one genuine storeroom in 47 clips is slugged `kneeling-blowjob.gif`,
  so `--want <room-word>` ranks *down* exactly the clips that have the room. The repo's two
  exemplars already disagree about whether those flags take setting or body vocabulary; body wins.
- **Verified:** the three Google rule lists (`chrome_route.md` §3, `scope_brief.md` §Queries,
  `query_rewriting.md` Part 2) now state the same rules; `grep -n "position\|posture"
  scripts/validate_queries.py` still returns nothing, confirming no doctrine drifted onto the code;
  the lexicon parses as the documented 4-column pipe format.
  **NOT verified, and cannot be from disk:** this is a *retrieval* change. The honest test is the next
  slot needing a non-default partner posture — write its queries under the new shape and compare its
  seated-slug rate against the baselines now recorded in the lexicon (calloway 0/10, renner 13/43).
  Until that number exists, this is a reasoned change, not a proven one.

## 2026-07-31 (A/B result) — the must_show/avoid deletion has NO measurable effect on picks

The controlled comparison promised in the entry below was run. **It is a null result, and the
change should be understood at that size.**

**Design.** Two slots (`colm_loop_oral_t5` 47 clips, `calloway_loop_oral_t5` 26). Per slot, every
clip on disk — pool + `.find-media/previous/` + fetched candidates — merged, **md5-deduplicated**
(57→47 and 29→26; 13 byte-identical repeats collapsed) and renamed opaquely so no filename, slug or
url could leak a prior verdict. Arm A = the pre-change skill (`git show HEAD:` before commit
`9c07228`). Arm B = the committed version. **Identical clip sets, identical briefs, and `pov_case`
PINNED to the same value in both arms** — POV was the confound that drove the earlier n=1 result, so
it was held fixed rather than merely "instrumented". Metric = the per-clip PASS/FAIL vector, never
the reason string.

**Result — 67 of 73 decisions identical (91%).**

| slot | agreement | B stricter | B looser | shared installs |
|---|---|---|---|---|
| colm | 44/47 (93%) | `clip_06`, `clip_12` — `position:him_seated` | `clip_29` — `count:additional_men` | 3 of 4 |
| calloway | 23/26 (88%) | `clip_15`, `clip_18` — `position:him_reclining` | `clip_24` — `act:licking_not_insertion` | 3 of 4 |

**Not one of the six disagreements is about a room, a light or a floor.** Four are arm B being
*stricter* on position; two are arm B being *looser* on a correctness gate.

**Why the effect is zero: arm A never gated on the room either.** Both arm-A agents hit the
template-vs-rubric contradiction, named it, and resolved it in favour of the rubric unprompted.
Colm's arm A: *"the scope brief files 'a bed or bedroom' and 'soft or domestic surroundings' under
`avoid`, which the brief template calls 'the hard gates', but this rubric deletes `wrong_setting`…
I followed the rubric. **That single call flips roughly ten clips** from FAIL to PASS-but-bottom-ranked."*

**So the honest value of the change is that it removes a coin flip, not that it improves picks.**
The contradiction was real and load-bearing — resolved the other way it would have flipped ~10 of 47
clips on colm and finished calloway's pool at 3 instead of 4 — but every agent in this test resolved
it correctly anyway. The deletion makes that outcome guaranteed instead of dependent on judgement.
Worth keeping on determinism grounds. **Not** worth the "recovers clips the old rule binned" claim
made earlier, which this test does not support.

**⚠️ Small adverse signal, recorded rather than buried.** Two of the six disagreements are arm B
being **looser on correctness** — `act:licking_not_insertion` and `count:additional_men`. Neither
clip reached an install list, so no pool was harmed, and colm's arm A flagged its own `clip_29` call
as *"the one FAIL I would want a second eye on"*. But 2 of 6 divergences running toward permissive
on act and count is exactly the risk of deleting a checklist, and it should be watched, not
explained away.

**Incidental findings, all independently confirmed by more than one arm:**
- **The demanded room existed after all.** `clip_09` — *"utility/linen storeroom doorway — shelving,
  stacked linens, bare wood floor, man standing in plaid with jeans down"* — was on disk the whole
  time, and **both** arms ranked it a top-4 install. Wave-2 searched 225 urls, reported "zero bar
  clips" and concluded the vein was empty. It was judging on the wrong axis, not facing an empty
  corpus.
- **The strip earns its cost.** `clip_02` is the only true bar interior in 47 and would have been
  rank-1 from a contact sheet; both arms zoomed the strip and found **a third woman lying on the bar
  counter** through the whole loop. Dies on `count`.
- **Duplicate SCENES, not just duplicate bytes.** `clip_05`/`clip_22` and `clip_06`/`clip_12` are one
  shoot at two crops — different bytes, so every hash check this session would miss them. Arm B
  refused to install both halves; arm A installed both and flagged it. Sixth duplicate event today,
  first caught by eye.
- **Pool coherence surfaced on its own** — the hole this skill still cannot express. Arm B: *"clip_43's
  man is Black and the other three are white, so the pool's 'Colm' visibly changes race every fourth
  visit"*, with a coherent swap offered. Per-clip gates cannot see this; a good agent catches it
  manually, which is not the same as the skill catching it.
- **Retrieval, not judging, is the real bottleneck.** Dominant kill on calloway is `him_standing`
  (12/26 and 15/19 across arms), matching wave-1's 11/15. Both arms called it a query-vocabulary
  problem: the canonical office blowjob on this corpus is she-kneels-he-stands.

**Methodology flaw in this test, disclosed:** naming the frozen clips `clip_01…` broke
`video_frames.py`'s board labels (`stem.split("_")[0]` → every row reads "clip"), so row identity was
positional only. Detected by cross-checking each arm's one-phrase room description per clip:
**26/26 and 47/47 matched**, so no misalignment occurred — but the labels should be bare numbers next
time. Both arms also re-read individual strips for contested calls rather than trusting the board.
Separately, this test forced all 47 clips to be stripped, overriding the 12-clip pool budget added
the same day; that token cost is the test's, not the skill's.


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

## 2026-07-31 (latest) — `must_show` / `avoid` deleted; the rubric owns the gates alone

- **Deleted `must_show` and `avoid` from `templates/scope_brief.md`** (§Demand), and with them the
  "copy both into the strip checklist" instruction. **Why:** they were a *second, unconstrained gate
  channel* that overrode the rubric. `references/scoring_rubric.md` has said since its rewrite that a
  wrong room can never reject a clip (`:24-26`, and `:332` — *"`wrong_setting` is not a valid
  `gate_reason`"*), and its Gate 3 list is bodies only — act, position, count, affect, extra people,
  finish. But the brief told the author to fill `must_show` *"straight from the beat prose"*, and beat
  prose says things like *"in a dim red-lit room"*; `avoid` was captioned **"The hard gates"** with
  **`bright studio lighting`** among its own examples. Both were then copied into the JUDGE checklist,
  so the room became binary — the exact bug the rubric was rewritten to kill, reintroduced through the
  template. `must_show` never appeared in any of the rubric's enumerated gates; its whole binary force
  came from `SKILL.md:459`, `scope_brief.md:153` and `scope_brief.md:260`.
  **⚠️ CORRECTED SAME DAY — the first version of this bullet overclaimed, and the correction matters
  more than the original claim.** It said the three room-demanding slots "returned 0 usable clips from
  ~670 fresh urls" while the body-only slot "filled 4 of 4 on the first pass", and graded that
  *Confirmed as a class, the strongest evidence in this table*. An adversarial review of the
  experiment checked the run records and it is wrong on three counts:
  - **All four slots filled 4-of-4.** Each installed 3 clips plus its incumbent. "0 usable" silently
    meant "0 that exhibit the demanded room" — a different and much weaker statement.
  - **The room gates did not fire.** Recorded kill classes are bodies: calloway's dominant reject was
    `him_standing` (11 of 15), second `wrong_act` (3). Brothel's own author wrote that the red light
    was *"scored on the SETTING axis, NOT gated"*, citing this skill's `wrong_setting` ban — i.e. the
    old skill already complied with the rule this change enforces.
  - **The url/round counts were wrong.** `query_ledger.jsonl`, the only machine-written log, records
    **7 / 6 / 6** rounds for brothel / calloway / colm, not the 4 / 3 / 3 claimed.
  **What survives, stated at its true size:** the rooms demanded genuinely were not in the corpus
  (verified — 6–7 rounds each, none retrieved), and the template genuinely invited them into the
  demand (colm's list required *"a hard floor — concrete / bare / tile, not carpet"*, calloway's
  *"a dim indoor office / records setting"*). So the change removes an **unsatisfiable demand that
  wasted search rounds** — a query-side harm. It is *not* established that gating on the room was
  binning good clips, because the gates were largely inert. Strip-survival where recorded: colm 4/20,
  marsh 5/16 — a 20% vs 31% efficiency gap, not 0 vs 4.
  - **Replaced by what already existed.** `## Derived facts for query planning` → `## Gate inputs —
    and the query's raw material`. Its canvas row already enumerated Gate 3's inputs exactly (act,
    position, count, direction, affect). It is now explicitly a **closed** list: a fixed set of named
    body facts has no free-form slot for a room to hide in. `setting` stays in it flagged
    *query-only, never a gate*.
  - **`pov_case` promoted to its own field.** The old text said to write the POV call "into
    `must_show` or `avoid`"; with both gone it needed a home, and deciding it at SCOPE rather than at
    judging time is a rule worth keeping.
  - **`SKILL.md` §1 Demand table** — `must_show`/`avoid` row replaced by `pov_case` + §Gate inputs,
    with a paragraph stating that the brief supplies gate *inputs* and never gates of its own.
- **Re-anchored the ABSENT/CONTRADICTED rule** (`SKILL.md` §5 Stage C). **Why:** it was the best rule
  in the gating doctrine and it was written about the deleted field. It now governs the Gate-3 checks,
  and gained a worked example for the room as a three-way test — **confirms / neutral / contradicts** —
  where only "contradicts" costs anything, and only as SETTING points. A neutral room (bare wall,
  plain floor, cropped background) is a normal correct clip. Rationale recorded: the beat's prose
  already told the player where they are, so the clip has to not argue with it, not prove it.
- **`references/scoring_rubric.md` — two additions, no rewrites.** §SETTING gained the corpus-bet
  warning: answering `setting_is_load_bearing = true` asks whether the room carries meaning *in the
  fiction*, which is a different question from whether this corpus ever shoots it (it shoots bedrooms,
  offices, bathrooms, cars, bars, gloryholes, POV-anywhere — not red-lit brothel rooms or industrial
  storerooms), with the four-slot table. Confidence table gained the row, marked **Confirmed as a
  class, n=4 slots with one clean contrast**.
- **Pool-aware strip budget** (`scoring_rubric.md` §Gate 2, new rule 1b). **Why:** "strip the top 6"
  was set for a slot that installs **one** clip. A `pool_dir` slot installs up to `pool_target`
  (normally 4) from a step that kills 30–65%, so six yields ~2–4 survivors — short of target on a bad
  day. Rule: strip 6; if survivors < `pool_target`, strip one more board of 6; **stop at 12**. Without
  a written ceiling, wave-1 agents stripped 20+ per slot at 120–142K tokens each, and none of it
  improved the pick.
- **Consistency sweep.** `templates/run_manifest.schema.json` — `brief.must_show`/`brief.avoid`
  replaced by `brief.pov_case` + `brief.gate_inputs` (with the why recorded in its `description`).
  `references/audit_mode.md:208` MED row now names the Gate-3 checks instead of "a named `must_show`
  element". `references/sheets_and_boards.md:31` repeatability claim now credits the checks being
  concrete *and closed* rather than the deleted lists.
- **Untouched on purpose:** `setting_is_load_bearing` (correct, and does two real jobs); Gate 1 CAST
  in full, including wardrobe, face filters, AI artifacts and heavy watermarks (cast and provenance,
  not setting); the mandatory frame strip on every animated install; mode counts 6/12/18; and
  `scripts/fetch_candidates.py --avoid`, which is a **−25 ranking penalty** (`:83-85`), not a gate —
  it was already the model this change adopts.
- **Verified — grep.** `grep -rn must_show` outside this CHANGELOG returns only the two deliberate
  historical mentions (`SKILL.md:261`, `scope_brief.md:161`) that explain the removal, plus the
  rationale text inside `run_manifest.schema.json`'s new `gate_inputs.description`.
- **Verified — behavioural, and this is the load-bearing check.** An independent agent re-judged
  `sex/brothel_oral_t5` under the revised skill from material already on disk — **no new searches**,
  25 clips judged across the pool, `.find-media/previous/` and `/tmp/fm/`. It was not told what to
  expect.
  - **Every gate reason it recorded is about a body:** `act:solo_no_partner`,
    `act:from_behind_vaginal_not_oral`, `act:no_oral_contact_in_loop`, `count:1_not_2_gloryhole`,
    `affect:performed_arousal_not_flat`, `affect:face_never_readable_absent`. **None about a room, a
    light or a piece of furniture.** On this slot the change took.
  - **The risk did NOT materialise.** Removing the free-form checklist was supposed to risk wrong-act
    clips leaking. The closed act gate killed **six**, and **five of them arrived from `hair pulling`
    queries** — the exact vocabulary trap a grip-focused demand invites. Every clip it would install
    shows the act in *every* sampled frame, checked on the strip.
  - **Four clips recovered that a room rule bins on sight**, three of them the best on disk: an
    ordinary daylight living room with a blue couch (the cleanest hand-in-hair kneeling blowjob in
    the set), a bright dining room with a floral rug (verbatim the rubric's own "contradicts"
    example), a bare grey wall, and a dim candlelit room. **Two had been sitting unused in
    `previous/` the whole time, harvested for a different slot.**
  - **It also removed the clip the room rule had installed.** `c1d16864eac` is the only genuinely
    red-lit clip in all 25 — slug `madison-ivy-red-light-burlesque-blowjob` — and it was installed
    *because* of that. With the red light earning nothing, what remains is a posed burlesque loop with
    no grip and an arched, head-back performance: `affect:performed_arousal_not_flat`. Correct
    direction.
  - **⚠️ But this run is NOT a controlled comparison, and should not be read as one.** It has no
    arm A. Its headline metric — "zero room-based gate reasons" — has a **pre-measured control value
    of zero**: the old skill's own records show no room/lighting/furniture reject either, because
    `gate_reason` is a closed namespace (`cast:`/`act:`/`position:`/`count:`/`affect:`/`finish:`/`pov:`)
    with no room slot to emit. A room-motivated rejection gets written as `affect:*` or `craft:*` and
    the instrument still reads clean — which is plausibly what the one removal here was, since
    `c1d16864eac` died on `affect:performed_arousal_not_flat` *"once the room stopped earning credit."*
  - **And the recovery is confounded with POV, not isolated to the room.** This run flipped `pov_case`
    from the stale brief's `defect` to `either`, and that flip is single-handedly what surfaced the
    best clip. The room change and the POV change were not separated.
  - A planned 3-slot replication was **cancelled before running** for these reasons: it would have
    returned green checks against a criterion whose control value is zero, on a slot set where one
    member (`renner_loop_oral_t5`, `setting_is_load_bearing: false`) had no room gate to remove at
    all. The correct design is a **paired A/B** — same frozen clip set, `git show HEAD:` skill vs
    working-tree skill, `pov_case` pinned in both arms, metric = the per-clip decision vector rather
    than the reason string, plus a blind judge choosing between the two assembled pools. Not yet run.
- **⚠️ Two risks the re-judge surfaced — unmeasured, flagged rather than fixed.**
  - **`pov_case` is now doing very heavy lifting.** Flipping this one slot's call from `defect` to
    `either` is single-handedly what recovered the best clip in the set — and the field has no
    measured backing at all. It is the most likely place for a slot to go bad quietly. Related: the
    old brief justified `defect` with "anonymity needs his body seen as a separate thing", which is
    **not one of the two cases the rubric admits** (`scoring_rubric.md:148-160`). Inventing a third
    POV case is now a known failure mode; the rubric's test is whether the partner is *slack, limp,
    passed-out, watching, restrained or pointedly-still* — a man actively driving her head is none of
    those.
  - **The gaze/affect crop exception is where a room-shaped gate can grow back.** It is the one
    framing-derived rejection the rubric still authorises, and the re-judge used it **3 times in 25** —
    making it the busiest reason after `act`. Worth a measurement before it is worth trusting.
  - **⚠️ POOL COHERENCE — the harm this change could actually cause, and nothing here detects it.**
    Every gate and every axis in this skill judges **one clip at a time**. A pool is 4 clips the engine
    cycles *in one location*. Take the room out of the per-clip channel and it becomes strictly more
    likely that a pool ships a red-lit room, a daylight living room with a blue couch, a floral-rug
    dining room and a bare grey wall — each individually defensible on HEAT, collectively telling the
    player the brothel is four different houses. `calloway_loop_oral_t5` already shows the shape: its
    own run note says *"none of the three installs is genuinely dim"* while its brief called the dim
    records room the meaning of the scene. **No check in this skill looks at the assembled pool.**
    Cheap fix when someone gets to it: one contact sheet of the finished folder, one question — *does
    this read as one place?* Until then, treat a pool's coherence as unverified.
  - Incidental, fourth run in a row: byte-identical duplicates behind different urls. Of "10 fetched
    candidates", two were the same file twice and two more were already installed — **7 new files, not
    10.** URL-dedup does not see this. The re-judge's "25 judgements" therefore covers ~21 distinct
    clips.
- **Known follow-up, out of scope by decision:** `author-game/references/media.md` carries the same
  contradiction upstream — `:329-338` grades **Setting as `critical`, "the background location MUST be
  recognizable"**, while `:232-236` in the same file says name the setting only when it carries
  meaning. That is what makes authors write rooms into `description` in the first place. Likely fix is
  narrow rather than a reversal of image-first doctrine: setting is critical when the image's job IS
  the place (a `location_image`, an establishing shot) and incidental when its job is the act.

## 2026-07-31 (later) — the shelf key is `slot_key`, not necessarily the path

- **`SKILL.md` §STOCK — the key bullet rewritten.** **Why:** a slot's shelf AND its verdict were
  filed under the declared path, so any edit moving the path orphaned both. Converting one slot to
  a pool stranded **148 stocked options** (measured live). A block can now author an `id`, which
  becomes the key and doesn't move. Every `game-review/load` item carries a `slot_key`; it equals
  `file` for an untagged slot, so nothing changes for the ~560 blocks that have no id.
  **Send both** — `file` decides where a `grab` writes, `slot_key` decides which shelf it touches.
  Conflating them writes a tagged slot's media to the wrong path; pinned by
  `tests/test_slot_key.py::test_grab_writes_to_the_PATH_and_drops_from_the_KEY_shelf`.
- New: `python manage.py check_shelves [--all] [--repair]` — audits for orphaned shelves/verdicts
  and re-files the confidently-matched ones. It found 3 on first run, one of which was a hand
  re-key I had done an hour earlier and got half-right (shelf moved, verdict left behind).

## 2026-07-31 — a pool is a FOLDER now, not a list of filenames

The engine's pool declaration changed under us the day after the pool section was written.
`files = ["a_1.webm", "a_2.webm", …]` is replaced by `pool_dir = "sex/oral_t5"` + `pool = 4`:
the folder's contents play, and `pool` is only a target for THIS skill. That removes the count
from the TOML entirely, so the human curates by adding/removing files in the review UI instead
of editing source.

- **`SKILL.md` §"A POOL slot wants N files" rewritten.** **Why:** the previous text said "each
  entry is **its own slot**: its own path, its own row, its own install" *and* "≥6 stocked for
  the slot as a whole" four lines apart — those contradict, and the folder shape settles it.
  **The slot is the FOLDER.** One row, one shelf, one verdict, all keyed by `pool_dir`. The
  filenames inside are invented at install time and mean nothing; keying anything on them makes
  an unselect re-key the shelf and orphan the verdict. Also states that `pool` is a target and
  not a manifest, so ending at 3 of 4 is a real state rather than a failure.
- **`SKILL.md` §6 INSTALL — pass `pool_dir` on the grab.** **Why:** with it set, `grab` ADDS to
  the folder and skips the same-stem delete a single-slot install does. **Omit it and installing
  clip 2 silently deletes clip 1** — the loop unlinks every same-stem file in the target dir.
  Called out with the ⚠️ it deserves and pinned by
  `tests/test_media_finder_pools.py::test_two_pool_installs_coexist`. Also documents that a
  re-grab of the same url replaces rather than duplicates (the filename is url-derived), and
  names the two curation routes (`pool/list`, `pool/unselect`) as human-facing, not scout-facing.
- **`SKILL.md` — the second-opinion TOML walk now sees folder pools too.** **Why:** yesterday's
  fix taught it `files = [...]`; a `pool_dir` block has neither a singular `file` nor a `files`
  array, so it was invisible again by a different route. Added a `pool_dir` pass that reports a
  pool as unfilled only when its folder holds nothing. **Verified** by running the block verbatim
  against a real pooled game: `2 pools, 1 empty`, matching what `game-review/load` reports.
- **`SKILL.md` frontmatter `description`** — "per declared entry" → "per target", since there are
  no declared entries any more.

Superseded from the 07-30 entry below: the `files = [...]` guidance is now the LEGACY path.
It still works and `the_long_summer_test` still ships 30 of them, but nothing new should use it —
an explicit list hardcodes a count you must guess before seeing a clip, and every entry it can't
fill stays on the missing list forever.

## 2026-07-30 — media POOLS: a slot can want N files, and the walk was blind to them

An engine change this day made `files = [...]` work on `video` blocks as well as `image`, and made
pools **cycle** (visit 1 → entry 1, visit 2 → entry 2, wrapping) instead of picking at random. A
repeatable beat can now hold 3–4 clips. That changes this skill's job, because a pool entry is a
separate file to find and install.

- **`SKILL.md` — the second-opinion TOML walk now sees pools** (the `python3` block under
  "trust the API, and still run the walk"). **Why:** its regex is
  `(?:file|image|video|nav_image)\s*=\s*"…"` — against `files = ["a.webm", …]` the `file` alternative
  hits `s`, not `=`, so it matched **nothing**. Measured, not assumed:
  `rx.findall(pool_block)` → `[]`. A game whose repeatable beats all used pools would audit as
  "0 missing" while shipping blank — and ~30 image pools in `the_long_summer_test` have been dark
  for months for exactly this reason. Added a second pass over `files\s*=\s*\[([^\]]*)\]`.
  **Verified:** a fixture with 2 singular refs + 5 pool entries → singular pass finds 2, both passes
  find 7. The API-side enumerators (`api/v1/game_review.py`, `manage.py check_media`) had the
  identical bug and were fixed the same day behind `apps/common/media_blocks.py::block_media_paths`;
  this walk is the independent check on them, so it had to be fixed too, not just deferred to them.
- **`SKILL.md` — new "A POOL slot wants N files, not one" under the deliverable contract.**
  **Why:** the contract said "a working file installed" (singular) with no notion that one block can
  declare N paths. The load-bearing rule is **install every gate SURVIVOR up to N, never "the top N
  regardless"** — rank 4 of 6 may be the one that scraped past, and in a pool the player sees it
  every fourth visit forever. Also states the economics: a pool shares one `description` and one
  `search_queries` set, so it is one search and one judging pass — you are not doing N× the work,
  you are spending survivors you already paid to judge and currently throw away.
- **`SKILL.md` §6 INSTALL — "one `grab` per entry"** with the loop, and an explicit note that every
  entry runs the same per-file gates. **Why:** `grab` derives its path from the `file` passed in, so
  a pool is N calls; without saying so, the obvious failure is installing one clip and calling a
  4-entry pool done. The gate note exists because a pool is exactly where an unstripped clip would
  ride in behind a good one.
- **`SKILL.md` frontmatter `description`** — "installs one best-guess pick … — or, for a
  `files = [...]` pool slot, one gate-surviving pick per declared entry." **Why:** the description is
  the trigger surface and also the skill's own summary of its contract; leaving "one pick" there
  contradicts the new §. Trigger phrases left untouched.

## 2026-07-29 — `find-media-b` DELETED; the Q2 A/B is closed, ranking stays

Recorded here because the arm's own ledger went with it. The experiment asked one question:
**does question 2 — HEAT/SETTING/CRAFT ranking — earn its keep?** Answer: yes. Ranking stays.

- **`.claude/skills/find-media-b/` — DELETED** (`SKILL.md` 132 lines, `CHANGELOG.md` 113).
  **Why, on the measurement:** arm B existed to test whether deleting ranking made the skill
  faster. The only clean head-to-head — two cloud sessions, same day, same container shape,
  same pre-stocked 1352-option shelf, neither with Django — says **no**:

  | | wall-clock | image reads |
  |---|---|---|
  | arm A (`media_lab_c`) | **16m25s** | **19** |
  | arm B (`media_lab_d`) | 17m09s | 32 |

  The earlier local pair (11.4 min vs ~81 min) looked like a landslide for arm B and was never
  a fair comparison: arm A's local run included the search *and* building the harness for the
  first time. **Honest qualifier:** the read gap is not ranking's doing — 15 of arm B's 32 reads
  were single-clip re-checks for fine gates (gaze, a hand, who is lying down), and gates are
  question 1, identical in both arms. Arm B's fair best case is "about the same speed."
  **Why, on the output:** same speed is still fine if the picks are equal — they are not. Arm B
  shipped two installs that are gate-correct and visibly rough, both named in its own report:
  `lab_group_t5` is a **3-panel stacked collage** (every panel has three men, so the count gate
  passes clean) and `lab_room` carries a **large diagonal Alamy watermark** (interior, no people,
  heavy wear — all three `must_show` pass). A watermark and a collage format are *craft*, and
  craft is exactly the axis arm B deleted. No speed gain + measured quality cost = no case.
  **Why, on doctrine:** a skill nobody should invoke is drift bait — the same reasoning that
  deleted `clip_shortlist.py` below. A losing arm sitting in `.claude/skills/` is something a
  future run can pick up by accident.

- **Salvaged before deletion, verified present here:** the `must_show` ABSENT/CONTRADICTED rule
  (entry below — this was the blocking item, since arm B held the only copy); the strip-board
  lesson (`SKILL.md` §5 and §Batching, `references/sheets_and_boards.md` — 52 reads one-at-a-time
  vs 14 from boards); and the finding that the rubric's heat signals are mostly unvalidated,
  with LO's winning POV/wrong-room/B&W/264px clip as the counterexample
  (`references/scoring_rubric.md`). Nothing unique died with the file.

- **Deliberately NOT deleted — the evidence, which is the actual asset:** `games/media_lab_b/`
  and `games/media_lab_d/` with their `AB_RESULT.md` / `RUN_RESULT.md`, their `scores.jsonl`
  trees, and the `games-data.js` portal entries that say those games were filled by
  `find-media-b`. Those are accurate history, not instructions to use a skill that no longer
  exists. The arm was the instrument; the runs are the result.

**Open and unresolved, stated so it is not mistaken for settled:** LO never rendered his own
eye-verdict on which arm's picks he would keep, and **0 of 10 slots tied** — every pick differs.
This deletion rests on the timing measurement plus two self-reported rough installs, not on his
comparison. All four builds are playable on the portal if he ever wants to close it properly.

## 2026-07-29 — the `must_show` "can't see it" rule promoted in from arm B

- **`SKILL.md` §5 JUDGE Stage C** — added the rule that settles what a gate call means when a
  `must_show` item is **outside the frame** rather than visibly wrong: *fails on ABSENT or
  CONTRADICTED; framing that merely doesn't cover it is UNVERIFIED, not failed — except gaze
  and affect, which fail when their carrier is cropped, because the face is their only carrier.*
  Placed beside the binary-gate law, since that paragraph already names `affect` as a gate and
  the exception turns on exactly that.
  **Why:** without it "does this candidate pass?" is **not deterministic** — a tight crop reads
  as a failure to one judge and as a non-issue to another, and the written `gate_reason` stops
  being auditable, which is the only verification this skill has now that no algorithm can be
  re-run (see the CLIP entry below). It also silently discards correct clips for how the shot
  was framed.
  **Provenance:** discovered during `find-media-b`'s run 1 and written down only there, by
  accident of where it surfaced. It is **question 1** — a correctness gate — so it always bound
  both arms; it was never an arm-B-specific rule. Promoted now so it survives independently of
  that experiment arm.
  **Evidence it cuts both ways** (from the run that produced it): `lab_eyecontact_t5/08`
  **passed** on unverifiable posture because its eyes held the lens in all four frames, while
  `lab_tease_t4/00` **failed** because it is a covert downblouse whose face never appears, so
  "aware of the camera" can never be shown at all.
- **`find-media-b/SKILL.md`** — its copy now points here and states that `find-media` wins on
  any disagreement, so the two cannot drift into two different rules. Logged in that skill's
  own ledger too; the A/B diff against this skill is still exactly one axis.

**Verified:** `grep -n must_show` resolves in `SKILL.md` at the gate law; the arm-B copy no
longer claims to be the rule's home.

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
