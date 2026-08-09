---
name: find-media
description: Find missing media (images and animated clips) for a story game AND stock a shelf of alternates for the human to pick from. Enumerates missing files from the game's TOML plus the game-review API, detects per-item content rating from the `_tN` tier suffix, hunts the vocabulary the beat is actually named by, searches by driving the user's own Chrome (Google Images — the only retrieval route), extracts original CDN urls with one regex, stocks 6+ candidate options per slot in the media-finder options store, frame-strip verifies animated finalists, and installs one best-guess pick via the game's dev API so the game always renders — or, for a POOL slot (`pool_dir` — a folder the engine cycles one clip per visit), one gate-surviving pick per target. Use whenever the user says "find media for <game>", "download missing media", "populate media", "missing media", "/find-media", or when a game TOML has media blocks whose files don't exist on disk. Also use to resume an interrupted run, to refetch a slot whose installed pick the user rejected (a refetch stocks the fresh candidates, then prunes the stale ones), or to audit the media a game already has.
---

# find-media

**You are a scout stocking a shelf, not a judge handing down a verdict.**

The old version of this skill searched, scored, installed, and threw everything else away.
It was wrong in a specific, measurable way: the user's winning clip was POV, wrong room,
black-and-white and 264px wide, and the old rubric would have binned it at zero before he
ever saw it. The spec-perfect clip it installed instead was correct and dead.

So the job changed. You are not here to prove a clip is hot with a number. You are here to
**stop discarding hot clips before the human sees them.**

## The deliverable contract

Every worked slot ends with **both**:

1. **A working file installed** — the game never renders a hole. This is your best guess,
   frame-strip verified if it's animated, and you say out loud in your report that it is a
   guess.
2. **≥6 options stocked** in the media-finder options store — the human flips through them
   in the review UI and picks.

Six is a floor, not a target. A slot with 3 options is a rubber stamp with extra steps.
NSFW slots stock 12 because the frame strip kills roughly half (measured: 3 of 5 and 4 of
6, two independent rounds). Per-mode counts live in one place — §Mode.

### A POOL slot wants N files, not one

A media block can declare a **pool** — `pool_dir = "sex/brothel_oral_t5"` + `pool = 4`
instead of `file`. The pool is a **folder**: everything inside it plays, and the engine
**cycles** it — visit 1 shows clip 1, visit 2 clip 2, wrapping. Repeatable NSFW beats use
this so the player isn't looking at the same clip forever.

**The slot is the FOLDER, not the files.** One row on the missing list, one shelf, one
review verdict, all keyed by `pool_dir` — the same string the picker opens with. It arrives
as a single item carrying `pool_dir`, `pool_target` and `pool_count`. The filenames inside
are invented at install time and mean nothing; never key anything on them, or an unselect
re-keys the shelf and orphans the verdict.

`pool = 4` is a **target**, not a manifest. The folder is the truth, so a pool that ends at
3 renders a 3-cycle and audits as "3 of 4" — a real state, not a failure.

One `description` and one `search_queries` set cover the whole folder, so a pool costs
**one search and one judging pass**. You are not doing N times the work — you are keeping
work you already did: today the top-ranked survivor installs and ranks 2–4 go on the shelf
and are never used. A pool spends them.

**Install every survivor that PASSES the gate, up to `pool_target` — never "the top N
regardless."** Rank 4 of 6 may be the one that scraped past on a technicality; three good
clips beat four where one is visibly wrong, and the player sees that fourth one every fourth
visit forever. So a 4-target pool legitimately finishes at 4, 3, or 1. Report which.

Everything else is unchanged: still ≥6 stocked (on the pool's own shelf), still frame-strip
every animated install, still a best guess and not a verdict.

> **Legacy:** `files = ["a.webm", "b.webm"]` — an explicit list, still supported. There each
> declared path IS its own slot with its own shelf. `the_long_summer_test` ships 30 of these.
> Anything new should use `pool_dir`.

You may never: auto-pick silently, present a single candidate, install an **animated** file
you have not frame-stripped, or drop a candidate for any reason other than a named gate
failure. A static `.jpg` — a location, a garment — cannot be stripped; those finalists are
judged from the contact sheet, and that is the whole exception.

**A refetch REBUILDS the shelf, it never appends — but it STOCKS FIRST and PRUNES AFTER.**
Take `t0 = now()` as ISO-8601, stock the new candidates, *then*
`POST options/clear {game, file, before: t0}`. Never clear on the way in: a clear-first
refetch whose search then comes back thin leaves the slot with nothing and the old pool
gone. That exact ordering once silently ate three harvests. **Never destroy a candidate
pool before its replacement exists.** Pruning afterwards still gets you the thing appending
would cost — the human never flips past a clip he already rejected, so he keeps trusting
the shelf, which is the only decider you have.

## When this triggers

Any one of:
- User says "find media for \<game>", "/find-media \<game>", "populate media", "missing media"
- A game TOML declares media whose files don't exist on disk
- User asks to resume a prior run (state lives in `games/<game>/.find-media/`)
- User rejected an installed pick and wants the slot refetched
- User wants an existing game's media audited → `references/audit_mode.md`

Do NOT trigger on: game-design questions, TOML schema questions, or tier-system questions
that aren't about downloading. Answer those directly.

## Decision tree — before any work

1. **Resolve the TOML.** `games/<game>/toml_phases/*_final_game.toml` — `7_final_game.toml`
   in current games, `6_` in older ones (`under_one_roof`, `two_weeks`). Glob it, don't
   hardcode the number. If nothing resolves, ask for the path and stop.
2. **Is the Django dev server up on `localhost:8000`?** If not, tell the user to run
   `python manage.py runserver` and stop. Everything downstream — the missing list, the
   options store, the install — is an HTTP call to it. The in-page `fetch` that stocks
   options fails *silently* against a dead server, so check first rather than discover it
   after a harvest.
3. **Fetch the missing list:**
   ```bash
   mkdir -p games/<game>/.find-media
   curl -s "http://localhost:8000/api/v1/dev/game-review/load?game=<game>" \
     > games/<game>/.find-media/game_review.json
   ```
   **No trailing slash on `load`** — a trailing slash 404s. Extract `missing_media`. It
   enumerates 6 categories (canvas blocks, location images, clothing, phone posts, dating
   profile photos, portraits) and confirms absence on disk. Contract in
   `references/game_review_api.md`.
4. **Cross-check with the TOML walker** (next section). The API is authoritative, but a
   cheap independent walk catches anything a future TOML shape introduces before it ships
   missing.
5. **Classify by type.** Non-canvas types (`location_image`, `clothing_image`,
   `social_post_image`, `dating_profile_photo`, `portrait_image`) are always SFW — they are
   UI chrome, not scenes. Canvas `image`/`video` inherit their rating from the filename
   `_tN` suffix.
6. **Tier audit + retag, before SCOPE.** Routing rides on the author's `_tN` suffix, which
   can be missing or wrong. Run `validate_queries.py`, read `tag_proposals`: take the
   confident `auto_retag`s, **ASK the user** on every `ask`, then `apply_retags.py` writes
   the corrected suffix into `toml_phases/*.toml` → re-merge → re-package → re-fetch the
   missing list. Full matrix and commands in `references/content_rating.md`. Skip if there
   are no proposals.

## The TOML walk — an independent cross-check

**Portraits are enumerated now.** NPC `portrait=`, `[player_portrait]` states and outfits,
and `customization_fields` image options all arrive from the API as `portrait_image`
(`api/v1/game_review.py`, `_add_portrait`). Verified live on vesper: 224 refs including 21
portraits, 0 missing.

That was NOT true until 2026-07-27, and the history is the reason this section still exists.
Those assets were invisible to the API for its whole life — they surfaced only as packaging
"File not found" errors, long after you thought you were done, which is how a new NPC's face
kept shipping absent. Repo-wide there are **81 `portrait =` declarations** across merged
TOMLs.

So: trust the API, and still run the walk below as a cheap second opinion. It costs one
command and it is what would have caught the portrait class years earlier.

Walk the merged TOML with the full regex and diff against disk **extension-agnostically** —
the TOML may say `.jpg` while the disk holds `.webm`, and that is normal, not a miss:

```bash
GAME=vesper
python3 - "$GAME" <<'PY'
import re, sys, pathlib
game = sys.argv[1]
root = pathlib.Path("games") / game
toml = sorted(root.glob("toml_phases/*_final_game.toml"))[-1]
src = toml.read_text()
# Singular keys: file = "…", image = "…", video = "…", nav_image = "…"
refs = set(re.findall(r'(?:file|image|video|nav_image)\s*=\s*"([^"]+)"', src))
# POOLS: files = ["a.webm", "b.webm", …] — N separate slots, one per entry.
# The singular regex CANNOT see these (`file` then hits `s`, not `=`), so a game
# whose repeatable beats all use pools audits as "0 missing" while shipping blank.
for arr in re.findall(r'files\s*=\s*\[([^\]]*)\]', src):
    refs.update(re.findall(r'"([^"]+)"', arr))
# FOLDER pools: pool_dir = "sex/oral_t5" — the slot is the folder, and it is
# unfilled only when the folder holds nothing. Reported separately below.
pools = re.findall(r'pool_dir\s*=\s*"([^"]+)"', src)
have = {p.relative_to(root / "videos").with_suffix("").as_posix()
        for p in (root / "videos").rglob("*") if p.is_file()}
missing = sorted(r for r in refs if pathlib.PurePosixPath(r).with_suffix("").as_posix() not in have)
empty_pools = sorted(d for d in set(pools)
                     if not any(h.startswith(d.rstrip("/") + "/") for h in have))
print(f"{toml.name}: {len(refs)} refs, {len(missing)} missing; "
      f"{len(set(pools))} pools, {len(empty_pools)} empty")
print("\n".join(missing + [d + "/  (empty pool)" for d in empty_pools]))
PY
```

**Use that exact key set.** A bare `image=` regex finds 38 of 202 refs on `vesper` —
it misses `file=`, `video=` and `nav_image=`, which is most of the game.

**And keep the `files` pass.** A pool declares N paths under `files = [...]` and no singular
`file`, so the first regex returns **nothing** for it — measured, not assumed. That blind spot
is why ~30 image pools in `the_long_summer_test` sat unfilled for months while every audit
said "0 missing". The API-side enumerators had the same bug and were fixed the same day
(`apps/common/media_blocks.py::block_media_paths`, used by `api/v1/game_review.py` and
`manage.py check_media`) — this walk is your independent check on them, so it must see pools too.

Anything this pass finds gets a scope brief and goes through the same phases as an
API-listed item. Record `discovered_by: toml_walker` in the brief so a later audit can tell
a coverage gap from a genuine miss.

## Paths — source vs compiled

Two folders look similar and get confused. Keep them separate:

- **`games/<game>/videos/`** — the SOURCE of truth. Every download lands here. Scan here to
  check what's missing.
- **`games/<game>/output/`** — the COMPILED game produced by `package_from_toml`: `index.html`
  plus a copy of `videos/`. Regenerated on every package run. **Never write media here** —
  it survives until the next package and then silently vanishes.

**The `scene_id` / `file` you pass the API is relative to `videos/`.** Say `scenes/kiss`,
not `videos/scenes/kiss` (the API strips the `videos/` prefix), and **never**
`output/videos/scenes/kiss` — the API does NOT strip `output/`, and the file lands nested
wrongly at `games/<game>/videos/output/videos/scenes/kiss.ext`, where nothing will ever
find it.

When a manual `curl` is required, the target is always
`games/<game>/videos/<subfolder>/<file>`.

## Format classification — image vs animated

Tier gates what can be *shown*. **Format gates how it's shown — and it's driven by ACTION,
not by tier.**

The rule: **motion-worthy scenes use animated (`.webm` / `.gif` / `.mp4`). Static scenes use
images (`.jpg`).**

| Content class | Examples | Format |
|---|---|---|
| Domestic / conversational | dinner, chores, talking, studying, working | `.jpg` |
| Location / object | kitchen, bedroom, garage, coffee mug | `.jpg` |
| Light flirt | hand-holding, greeting, sitting close, warm smile | `.jpg` |
| Kiss / tease | making out, teasing, biting lip, seductive gaze | **animated** |
| Solo body | undressing, flashing, bathing, showering, nude posing | **animated** |
| Intimate / explicit | any NSFW act (t5+) | **animated** |

A t4 kiss is `.webm`, not `.jpg`. A t5 tease is `.webm`. A t3 dinner is `.jpg`. A t4
"romantic candlelit dinner" stays `.jpg` if no physical intimacy is shown.

`scripts/validate_queries.py` runs this check during PLAN (keyword detection over
description + queries) and flags mismatches under FORMAT MISMATCH.

**But the download API ignores your TOML extension and saves using the SOURCE URL's
extension** (`references/api_behavior.md`). So a FORMAT MISMATCH warning is really a hint
about **which KIND of source to pick** — an animated URL for the kiss, a still for the
dinner. Do that and the saved file is right regardless of what the TOML said; the renderer
picks `<video>` vs `<img>` from what is actually on disk. Fixing the TOML extension is
worth doing for human clarity, but it is not a download blocker.

---

# The phase flow

Phases 1–2 run **upfront for every item** — they're cheap, network-free, TOML-only.
Phases 3–6 run in **pipeline slices of 5 items** (see §Batching).

## 1. SCOPE — write the brief

For each missing item, fill `templates/scope_brief.md` → `games/<game>/.find-media/scope/<item_id>.md`.

The brief is **the only thing the search and the frame-strip check get to read.** Whatever
you leave out, you re-derive badly two hours later in front of 40 thumbnails, from memory.

The part that carries is **§Demand**:

| Field | Why it exists |
|---|---|
| `setting_is_load_bearing` | Decides whether the query spends words on the room AND whether the setting axis is scored at all. Test: does the setting carry **danger, secrecy, or squalor**? A dark-alley beat rejected bright clips twice; a different beat, the user said the setting "doesn't matter much here". |
| `intended_heat` | Names the *carrier* — eye contact, being used, power, squalor, exposure. This is what makes a spec-perfect clip dead when it's missing. |
| `pov_case` | Decided **now**, not at judging time. POV is a defect when the meaning needs the partner's body seen (a slack, watching, restrained man cannot be the camera). POV is fine, often stronger, when the power is her face and eyes aimed at the viewer. |
| §Gate inputs | The closed list Gate 3 checks against — act, position, count, direction, affect. Bodies only. `setting` sits here too but feeds the **query** alone. |

**The brief does not carry its own gate list.** Gates live in one place —
`references/scoring_rubric.md` §Gate 1 (CAST) and §Gate 3 (BEAT) — and the brief supplies their
inputs. The brief used to carry free-form `must_show` / `avoid` lists that became the strip
checklist, and because they were filled "straight from the beat prose" they filled with rooms —
one slot's list required *"a hard floor — concrete / bare / tile, not carpet"*, another *"a dim
indoor office / records setting"*. The rubric forbids rejecting on a room, so those entries were
either ignored (making the demand theatre) or obeyed (breaking the rubric). Both are bad, and on
`vesper` both happened. A closed input list has nowhere for a room to hide, which is why it is
closed.

The API already confirmed the file is absent — don't re-scan disk.

## 2. PLAN — hunt the word, then write the queries

**Step A — the word hunt.** This step did not exist in the old skill, and its absence is
exactly why the skill never found `downblouse` for a lean-forward-cleavage beat that the
user named in about a minute on Reddit.

Trigger: **you can describe the beat in a sentence but you cannot NAME it in one word.**
Stop and hunt. A query built from your own paraphrase inherits your own blind spot.
Ranked yield, procedure, and the lexicon format are in `references/chrome_route.md` §1 —
short version: Google's own result labels are the richest mine, an LLM is good only for
modifiers and community names, and `WebSearch` and Reddit's JSON API are both dead ends.

**Step B — synthesize queries for items that have none.** Phone posts and occasionally
other categories arrive with `search_queries = []`. Write 2–3 from `description` + `type` +
`category` using the worked examples in `references/query_rewriting.md` §Synthesizing.
`location_image` and `clothing_image` are **always SFW**, no exceptions — they render in UI
chrome and an adult result there is a bug in the wardrobe screen.

**Step C — validate:**
```bash
python3 .claude/skills/find-media/scripts/validate_queries.py \
  --from-api-json games/<game>/.find-media/game_review.json
```
Deterministic rewrites (banned feeling-words, direction disambiguation, solo/same-sex trap),
tier alignment, format family. Never run a query it flags as unfixable — surface it instead.
Offline fallback: `--toml games/<game>/toml_phases/7_final_game.toml` (canvas items only;
misses the non-canvas categories the API covers).

**Step D — write per-source query slots.** The dialects are **opposites** and ranking them
against each other is meaningless. Google takes verbose natural language but story and
character words poison the intent (`back alley blowjob gif drunk guy night` returned Reddit
movie stills, Facebook and TikTok; the same query minus `drunk guy` worked). PornHub's own
search box takes 2–3 tags and returns literally 0 at 4+ — that dialect still matters because
its tag vocabulary is what you mine, and since 2026-08-06 PornHub is **also fetchable** — you retrieve
a file from it (§3). Full split in `references/query_rewriting.md` Part 2.

## 3. SEARCH — drive the user's own Chrome

**Chrome is the only retrieval route.** You drive a browser that is already logged in with
SafeSearch already off; you never handle a login or an age gate.

One Google query surfaced nine hosts the previous route could never touch. The fetchable
corpus below. That route only ever reached PornHub, whose media sits behind a signed url our
extraction strips (see the next paragraph). That single source was the real ceiling, and no
amount of query tuning was going to raise it.

Two facts that make this cheap:
- Google's result-page HTML carries the **original CDN urls**. One JS regex over
  `document.documentElement.innerHTML` returned **54 direct URLs in a single call**.
- The results grid **is already a contact sheet** — one screenshot shows 20–40 tiles.

**PornHub is DISCOVERY-ONLY. Never queue a phncdn url for download.** A PornHub-hosted
Google result is worth reading for its title and tags — that is where the vocabulary lives —
and worth nothing as a candidate. Measured: `egl.phncdn.com/gif/<id>.gif` returns **470 on
clearnet and over Tor alike**, every id tried; it is not a fetch endpoint. The real media url,
read off a gif page, lives on `el2.phncdn.com/pics/gifs/` and is **signed, time-limited and
IP-locked** (`validfrom` / `validto` / `ipa` / `hash` query params) — and our extraction
strips query strings by construction, which destroys that signature. `pornhub.com` itself is
unreachable on clearnet from this machine. Of the 54 urls in that one harvest, **exactly the
4 phncdn ones failed**; the other 50 yielded 40 files. Skip `*.phncdn.com` as a candidate.

**The fetchable corpus** — measured 200 on plain clearnet GET, no Tor, no signing, no expiry:
`blovjob.com`, `cdn.nsfwgify.com`, `xgroovy.com`, `porngif.co`, `cdn.hardcoregify.com`,
`cdn.xgifer.com`, `imagex1.sx.cdn.live` (sex.com), `flashingjungle.com`,
`static-ca-cdn.eporner.com`. That is the one host list; a host Google surfaces that isn't on
it is *surfaced, not yet characterised* — try it, record what it did, don't assume.

Do NOT call `read_page` / `get_page_text` on a results page; accessibility snapshots are the
whole reason the old browser-automation path cost ~30× the tokens per action. Exact tool
calls, the regex, the mandatory `.split('?')[0]`, and the extract → click "More results" →
re-extract self-check (scrolling alone never crosses Google's ~200-tile boundary)
are in `references/chrome_route.md` §§2–4. Which hosts serve what is in
`references/media_sources.md`.

Run **2–3 sibling queries per slot**, never one — different phrasings land on partly
different host clusters, and that's how you reach 6+ options.

## 4. STOCK — the step that keeps runner-ups alive

**Stocking happens exactly ONCE, here, and it happens BEFORE you judge.** POST every relevant
candidate straight from the results page to the options store — it costs nothing, it is urls
only, and it is the single thing that keeps runner-ups alive. Verified: 54 of 54 accepted,
CORS fine, in-page `fetch`. Nothing downstream stocks anything: JUDGE ranks, INSTALL installs.

```
POST /api/v1/dev/media-finder/options/add    {game, file, slot_key, url, type, media_kind, query, docid?}
POST /api/v1/dev/media-finder/queries/add    {game, file, slot_key, query, source, urls, stocked, hosts, seed_url?}
POST /api/v1/dev/media-finder/related/fetch  {game, file, slot_key, url}   (runs scripts/fetch_related.py)
GET  /api/v1/dev/media-finder/options/list   ?game=&file=   → {"options":[…], "queries":[…]}
POST /api/v1/dev/media-finder/options/remove {game, file, url}
POST /api/v1/dev/media-finder/options/clear  {game, file, before}      (api/v1/media_finder.py:331)
POST /api/v1/dev/media-finder/grab           {game, file, url, source}
```

⚠️ **`options/list` returns stored records verbatim, and the stored names are NOT the names you
POST.** The `query` you send on `options/add` comes back as **`found_by`, a list** (a url two
sibling queries both returned carries both labels); query records are keyed **`q`**. Neither
carries a `query` key, and no legacy one exists — an unlabelled option simply has no
`found_by`. Checking an option for `query` reports 100% unattributed on a perfect shelf. Full
shape in `references/chrome_route.md` §5.

`docid` = Google's index id for the image, paired by §4's join in `chrome_route.md` —
send it on every stock; it is what makes "fetch related" (§5b there) one navigation.
`seed_url` (+ `source: "related"`) marks a related-fetch's closing record — the pair
the picker's ⇢ button derives its state from.

Ledger: `games/<game>/.find-media/media_options.json`.

**`picks` — an installed clip is still traceable (2026-08-09).** Installing DROPS the option
row, so the `docid` used to die with it and a selected clip could never seed a `⇢` again. The
`picks` root now keeps what each install consumed — `{filename, url, docid, thumb, found_by}`,
keyed by the installed file's basename — and `fetch_related.py` resolves a seed across three
places in order: an option's `url`, an option's `source_url` (a DEMOTED pick, whose `url` is a
local `/games/…` serve path), then `picks`. **So never refuse a related fetch on the grounds
that the clip is already installed or was previously installed** — try it; only a genuinely
absent id is exit 4. `manage.py backfill_picks` recovers older installs by md5-joining the pool
filename against urls still on a shelf; it opens no socket and guesses nothing.

- **⚠️ The shelf key is `slot_key`, which is NOT always the path.** Every item from
  `game-review/load` carries one. It equals `file` for an untagged slot (nearly all of
  them), but a block that authored an `id` keys its shelf and its verdict on that
  instead — so the ledgers survive the path moving (a tier retag, a pool conversion).
  **Send both**: `file` says where the bytes go, `slot_key` says which shelf you are
  touching. Pass `slot_key` on `options/*`, on `grab`, and on a review POST. Omit it and
  it falls back to `file`, which is correct only for untagged slots. Use the item's own
  `slot_key` verbatim; never reconstruct it.
- **`file` is the slot's TOML-declared path, character for character** — it decides where a
  `grab` writes. A typo puts media somewhere nothing will ever find.
- **`game` rides in the BODY on every media-finder POST**, and in the **QUERY STRING** on
  `options/list` (it's a GET) and on every media-review endpoint. It is *not* a clean
  "finder = body, review = query" split — `options/list` is the exception that breaks that
  mnemonic. Put it in the wrong place and you get `400 Invalid or missing game`.
- **`media_kind` is exactly `img` or `video` — never `"image"`.** `.gif` → `img` (it previews
  inside an `<img>`), `.webm` / `.mp4` → `video`. The backend lowercases the value and
  defaults to `img`, so a bad value renders blank, which reads to the human as a dead candidate.
- Dedup is by exact URL, so re-running a query is harmless.
- **Refetch: stock first, prune after.** `t0 = now()` → stock → `options/clear {game, file,
  before: t0}`. `before` keeps everything this run just stocked; `origin: "previous"` entries
  (the slot's undo history) survive regardless. Do **not** walk `options/list` and fire
  `options/remove` url by url — that deletes the undo history along with the stale options.

This is the phase the whole redesign exists for. Under the old shape you evaluated ~15
candidates, installed 1, and the other 14 died on `/tmp` — everything the human might have
preferred was destroyed before he saw it.

## 5. JUDGE — contact sheet, then the mandatory strip

**First, get bytes down — in TWO WAVES.** `fetch_candidates.py --top 8` (see
`references/chrome_route.md` §6), sheet it, gate it, strip the survivors; only top up with
`--more` if gate-survivors land under the 6-option shelf floor. The media_lab run fetched
**144 files to strip 60** — the surplus only padded a sheet. This trims *fetching*, never
judging: every animated finalist and every install is still stripped.

**Stage A — contact sheet.** Build it with `video_frames.py --videos-dir … --mode rep
--sheet …`: one representative frame per candidate, tiled and numbered, so you Read **one
image** instead of 15 thumbnails.

**You are the shortlister. There is no model in this loop.** ffmpeg cuts, resizes, labels and
glues; it judges nothing. Every call — the act, the count, the gaze, the affect — is made by
reading the assembled image. So **tile order carries no claim**: the sheet is in
`fetch_candidates.py` order, which is a stable index for naming a tile, not a ranking. Because
nothing can be re-run to check a call, the written `gate_reason` in `scores.jsonl` is the
verification mechanism and the sheet is the exhibit.

Everything is already on the shelf by the time you get here, so the tile count is purely how
many you *look at*: **show the mode's full option count** (§Mode — 6 / 12 / 18), or you ship
an option no eye ever landed on.

Note the input split: the Chrome route returns `.gif` as often as `.mp4`, plus ordinary stills.
Animated files get a rep frame extracted; **a still IS its own rep frame** and needs no
extraction. Full contract in `references/sheets_and_boards.md`.

**Stage B — the frame strip. Every ANIMATED finalist, route-independent, no exceptions.**
`.webm` / `.mp4` / `.gif` get stripped; a static `.jpg` finalist has no frames to strip and
is judged from the contact sheet instead. Strip the **top 6 by rank** (§Mode).

**Strip the batch, then read ONE board.** `--board` stacks every candidate's strip into a
single labelled image — one row per candidate, six rows per board. Reading strips one at a
time costs ~3× the image reads for identical verdicts (measured 2026-07-28/29), and it is the
default people fall into whenever the flag is forgotten:

```bash
python3 .claude/skills/find-media/scripts/video_frames.py \
  --videos-dir <candidates-dir> --mode strip --frames 4 \
  --out-dir games/<game>/.find-media/evidence/<item>/strips \
  --board games/<game>/.find-media/evidence/<item>/board.jpg
```

Single-clip form — for re-checking one candidate after the board, not for a batch:

```bash
python3 .claude/skills/find-media/scripts/video_frames.py \
  --video <candidate> --mode strip --frames 4 \
  --out games/<game>/.find-media/evidence/<item>/strip_<id>.jpg
```

`video_frames.py` is stdlib-only but shells out to ffmpeg; no ffmpeg on PATH and it exits **3
— degrade, don't crash**: fall back to the harvest poster and say so in the report.

**Thumbnails lie, constantly.** Measured this session: the strip killed **3 of 5** in one
round and **4 of 6** in the next. Real kills: a thumbnail that read as a perfect cluttered
back room whose loop was standing *kissing* with no blowjob in it at all; a "dark outdoor"
thumbnail whose loop was a bright daytime laundromat; a thumbnail that read
bent-over-from-behind whose clip was a blowjob. A single frame is a claim about one instant.
The strip is a claim about the loop, and the loop is what ships.

**Eye contact must HOLD ACROSS THE WHOLE STRIP.** Two candidates died on wandering eyes
their thumbnails hid. One lucky frame is DEAD, not WORKING.

**Stage C — rank into a shelf.** The one law: **correctness is a binary GATE, quality is
scored.** Act, position, people count, affect, cast, and POV-when-the-scene-requires-the-
partner-visible are **gates** — pass or out. Being correct earns no points, ever, because
points are exactly how a correct-dead clip out-totals a flawed-alive one.

**A gate fails on ABSENT or CONTRADICTED — never on "can't see it."** A Gate-3 check the framing
simply doesn't cover is **UNVERIFIED, not failed**. A tight crop is a camera choice, not a defect,
and rejecting on it throws away correct clips for how the shot was composed. The **one exception is
gaze and affect**, which **fail** when their carrier is cropped out: the face is their only carrier,
so a face that is never in frame means the beat's content is **absent**, not merely unproven.
Measured both ways in one run — a tight-crop candidate **passed** on unverifiable posture because
its eyes held the lens in all four frames, while a covert downblouse **failed** because "aware of
the camera" can never be shown by a clip whose face never appears. Without this, "does it pass?" is
not deterministic: two readings of the same strip disagree, and the `gate_reason` stops being
auditable.

**The same three-way test applies to the room, and it is the case that has cost the most.** A room
either *confirms* the beat, is *neutral* toward it, or *contradicts* it — and only the third is
worth anything, as **points off the SETTING axis, never a rejection**:

| | example against a "dim back room" beat | what it costs |
|---|---|---|
| confirms | a real dim storeroom | full SETTING score. Rare — do not wait for it |
| **neutral** | a bare wall, a plain floor, a cropped background | **nothing. This is a normal, correct clip** |
| contradicts | a sunlit living room with a floral rug | SETTING 0–5. Still not a gate |

The failure mode this kills: the beat prose says *"in a dim red-lit room"*, that phrase gets treated
as a required element, and the search then spends round after round hunting a room these hosts do
not shoot. Observed on `vesper`: three slots demanded a red-lit brothel room, a concrete storeroom
and a dim records room; across 6–7 rounds each, none was retrieved, and calloway's own run note
reads *"none of the three installs is genuinely dim."*

**Be precise about the mechanism, because it is easy to overstate** (an earlier version of this
paragraph did): those slots still filled. The rooms in the demand were largely *inert* — authors
wrote them down and then correctly declined to reject on them, so the recorded kills are bodies
(`him_standing` 11 of 15 on calloway). The cost was wasted search rounds and a demand nobody could
satisfy, not good clips thrown away. That is reason enough to keep rooms out of the gate list, and
it is a smaller claim than "the room gate binned everything."

Remember what the picture is for — the beat's prose already told the player where they are, so the
clip has to *not argue with it*, not prove it independently.

What's left is scored on **three axes and only three: HEAT 60 / SETTING 25 / CRAFT 15.**
When the setting is not load-bearing — no danger, no secrecy, no squalor — **SETTING is
skipped and recorded as `null`.** Not scored low, not scored zero: skipped. The ranking is
then HEAT and CRAFT alone. `setting_is_load_bearing` is a per-slot call made back in the
SCOPE brief, so every candidate in a slot is scored the same way and the ranking stays
comparable.

**There is no accept threshold.** No bar, no auto-accept score, no "below_bar" — candidates
are ranked and stocked, and the human decides. The re-search trigger is **shelf depth:
fewer than 6 survivors → search more.** Never lower a gate to fill the shelf.

`wrong_setting` is **not** a valid rejection reason. If you write it, you have reintroduced
the bug the rubric was rewritten to kill. Full gates, bands, the dead-clip veto, and
`scores.jsonl` in `references/scoring_rubric.md`.

## 6. INSTALL — best guess in, everything else on the shelf

```bash
curl -sS -X POST http://localhost:8000/api/v1/dev/media-finder/grab \
  -H 'Content-Type: application/json' \
  -d '{"game":"<game>","file":"scenes/alley_bj_t5.webm","url":"<source-url>","source":""}'
```

`grab` derives the target path from the slot's declared `file`, so it cannot put the file in
the wrong place. `POST /api/v1/dev/media-capture` with `{url, scene_id, game}` is the
equivalent for a raw path.

**Iteration is safe and idempotent.** When `game` is provided, the API deletes any existing
file with the same stem before writing, regardless of extension. Re-downloading with a
better source silently replaces the previous file — no orphan `_1` suffixes, no manual
cleanup. That is what makes a refetch cheap.

Then, in order:
1. **Fetch sanity** on the file the API actually wrote: anything under **1024 bytes**, or
   whose bytes are HTML, is an error page, not media. Check the bytes, never the url.
2. Run the pre-install quality gates (below) on that same file.
3. `dedup_tracker.py --record`.
4. Append to `games/<game>/.find-media/run_manifest.json`
   (schema: `templates/run_manifest.schema.json`).
5. Report the install as **a best guess, not a verdict.**

Nothing gets stocked here. The pick and every runner-up went onto the shelf back in STOCK,
and the store dedupes by URL — there is no second stocking pass, and an INSTALL that thinks
it needs one has skipped STOCK.

**Pool slots: pass `pool_dir` and call `grab` once per survivor.** With `pool_dir` set, `grab`
**adds** to the folder instead of replacing the slot — it invents a unique filename from the
source url and skips the same-stem delete that a single-slot install does:

```bash
for u in "<survivor-1-url>" "<survivor-2-url>" "<survivor-3-url>"; do
  curl -sS -X POST http://localhost:8000/api/v1/dev/media-finder/grab \
    -H 'Content-Type: application/json' \
    -d "{\"game\":\"<game>\",\"file\":\"sex/brothel_oral_t5\",\"pool_dir\":\"sex/brothel_oral_t5\",\"url\":\"$u\",\"source\":\"\"}"
done
```

⚠️ **Omit `pool_dir` and the install path deletes every same-stem file in the target folder** —
installing clip 2 would wipe clip 1, silently. Guarded by
`tests/test_media_finder_pools.py::test_two_pool_installs_coexist`.

Re-grabbing the same url replaces that clip rather than duplicating it (the filename is derived
from the source), so a refetch stays idempotent.

**Stop when the survivors stop, not when the target does** (§The deliverable contract). Every
installed clip runs the same per-file gates: fetch sanity, `tier_format_check.py`, frame strip
if animated, `dedup_tracker.py --record`. A pool is exactly where an unstripped clip would ride
in behind a good one.

Two more routes exist for the human's curation pass, which you do not normally call:
`GET pool/list?game=&dir=` (what's currently in the folder) and
`POST pool/unselect {game, dir, filename}` (move one clip out; it returns to the shelf as an
`origin: "previous"` option).

---

## Quality gates — run AFTER download, before you call the slot done

**There are two size checks and they are not the same check.** *Fetch sanity* fires the
instant a byte stream lands: under **1024 bytes**, or HTML bytes, means an error page — throw
it away. *The pre-install gate* fires once the file is in place: `tier_format_check.py`,
images ≥ **1024 B**, animated ≥ **51200 B**. There is no 5KB rule anywhere in this skill.

| Gate | Tool | Threshold |
|---|---|---|
| Format matches tier | `python3 scripts/tier_format_check.py --file <path> --tier <tier>` | t5+ MUST be `.webm`/`.mp4`/`.gif`, never JPG. Valid tiers: `base`, `location`, `t0`–`t8` |
| Not already used in this game | `python3 scripts/dedup_tracker.py --check <id_or_url> --game <game>` | add `--global` to check the cross-game set too |
| Real bytes | `tier_format_check.py` (magic bytes) | images ≥ 1024 B, animated ≥ 51200 B; anything reporting `text/html` is an error page |
| Strip-verified | `video_frames.py --mode strip` | every ANIMATED finalist; static `.jpg` finalists are judged from the contact sheet instead |

`tier_format_check.py` checks magic bytes, not just the extension — the only check that
survives a third-party CDN, since any of a dozen hosts can serve a JPEG behind a `.gif` URL
or an HTML error page behind either.

**Why after download, not before:** the API decides the saved extension from the source, not
from your request. A `.jpg` TOML pointer with a `.webm` source URL saves `.webm`, and the
renderer's extension-agnostic lookup still finds it. PLAN-phase FORMAT MISMATCH warnings are
advisory; the post-download check is what matters.

**A failed gate drops the candidate back to JUDGE, not back to SEARCH.** The candidate was
already evaluated visually — the problem is the file, not the query. Take the next ranked
option off the shelf.

---

## Batching — the batch is a pipeline slice, not a search slice

When the total work is bigger than the slice (say 50 missing items), do NOT search all 50,
then judge all 50, then install all 50.

```
Phases 1–2 (SCOPE + PLAN)   →  upfront for all 50; cheap, network-free, TOML-only

Batched loop (phases 3–6)
  for each group of 5:
    SEARCH (5) → STOCK (5) → JUDGE (5) → re-query any slot under 6 options → INSTALL (5)
  then the next group of 5.
```

**Slice size: 5 items.** Nothing enforces it; it is a judgment default. The reasons:

- **Progress is durable.** After each batch, 5 slots have a working file installed, a stocked
  shelf, and a `run_manifest.json` entry. A crash leaves you at 5/10/15 complete, not 50
  half-processed items with nothing on disk.
- **The harvest-to-judge gap stays tight.** Search 50 slots first and you're looking at
  contact sheets long after the pages that produced them, with no cheap way to go back and
  run a sibling query for the slot in front of you. A batch of 5 keeps the browser one step
  away from the judgment.
- **Re-query loops stay local.** A slot that comes up short of 6 options gets its sibling
  query run *now*, inside the current batch, while the tab and the vocabulary are warm.
- **Token budget.** One contact sheet per item ≈ 5 image Reads per batch, versus the ~75
  individual thumbnail Reads the old flow required — that was 0.5–1M tokens per game spent
  purely looking. Measured again 2026-07-29 on identical files: **52 image reads one strip at
  a time vs 14 from boards**, same verdicts. See `references/sheets_and_boards.md`.

Never start a new SEARCH while the previous batch's INSTALL is incomplete.

## Mode — how tall to stock the shelf

Mode is an **option count**, not a retry budget. These are the only option counts in this
skill; every other section defers here rather than restating a number.

| Mode | Options stocked | Stripped | When |
|---|---|---|---|
| `fill` | 6 | none — static `.jpg`, judged from the contact sheet | SFW static slots: location, clothing, social post, dating profile. Low variance, cheap to eyeball. |
| `wide` | 12 | top 6 by rank | Any NSFW canvas slot. The strip kills ~half, so a 6-deep shelf can arrive as 2 survivors. Stock 12 to land 6. |
| `deep` | 18 | top 6 by rank | Capstones, hero assets reused across canvases, and any refetch after the human disapproved the installed pick — that shelf already proved wrong. |

## Subagent dispatch

**Do NOT spawn one subagent per source.** The old fan-out (4 per item) multiplied token cost
with no benefit — every agent paid to look at its own pile and none could compare across
piles. One page, one regex, one sheet, one look. The nine-host spread came from **one**
search, not nine.

Run the Chrome route on the main thread: it drives one shared browser session, and the
screenshot you take is the thing you immediately need to look at.

| Subagent | Objective | Output | Boundaries |
|---|---|---|---|
| `query-rewriter` | Read narrative + raw queries, produce per-source query slots | JSON `[{source, query, reason}]` | Doesn't search, doesn't invent facts |
| `candidate-evaluator` | Read the contact sheet, apply gates, rank survivors | `{ranked[], installed_id, gate_rejects[]}` | Tiles are in fetch order, **not** ranked; **judge the act yourself** |
| `shelf-triage` | Diagnose a slot that came up short of 6 options | `{diagnosis, sibling_queries, alt_terms}` | Only after the first search pass returns thin |

Give each a focused brief — objective, output format, tool guidance, task boundaries. Vague
briefs cause duplicate work.

## Evidence and persistence

```
games/<game>/.find-media/
├── game_review.json                     # cached missing list
├── lexicon.md                           # terms confirmed this run (compounds across runs)
├── query_ledger.jsonl                   # EVERY query run, one line each — see below
├── scope/<item_id>.md                   # SCOPE briefs, with resume markers
├── evidence/<item_id>/
│   ├── candidates/                      # raw downloads
│   ├── frames/                          # one rep still per animated candidate
│   ├── contact_sheet.jpg                # the sheet you Read
│   ├── strip_<id>.jpg                   # per-finalist frame strip
│   └── scores.jsonl                     # gates + axes + decision, winners AND losers
├── media_options.json                   # the shelf (written by the options API)
├── media_reviews.json                   # the human's verdicts (written by media-review)
├── used_assets.jsonl                    # dedup tracker state
└── run_manifest.json                    # final summary
```

**Evidence never lives in `/tmp`.** It got wiped twice in one session and took the candidate
pool with it both times. Scratch bytes may transit `/tmp/fm/<slot>/`; anything worth keeping
lands under the game.

To resume: re-invoke the skill on the same game. Read each brief's resume marker —
`OPTIONS_STOCKED` is the real progress signal. An item with an installed pick and 0 stocked
options is **not done**, because the human has nothing to choose from.

Terms that prove out across more than one game get copied up to `games/.find-media/lexicon.md`.
That is the one part of a run that compounds: every future run starts with a bigger
vocabulary than this one did.

**`query_ledger.jsonl` — written FOR you, by `queries/add`.** One JSON line per query:
`{"slot", "query", "date", "round", "source", "urls_yielded", "status"}`. Do not hand-write it any
more: the endpoint that records a search appends this line as a side effect, which is the first time
this file has actually been what it always claimed to be — a machine-written record. That matters
more than it sounds: a prose run summary claiming "4 rounds" has already been caught contradicting a
ledger showing 7. When the two disagree, **the ledger is right.**

It is also the DURABLE copy. The same facts live in `media_options.json`'s `queries` root, which is
rewritten whole on every write and which `_read_options` reads back as EMPTY if a write ever tears —
so one bad write could take the entire query history with it. This file is only ever appended to.

⚠️ **`urls_yielded` is NOT a quality signal.** Measured across 31 vesper queries: 40–92 urls, with no
relationship to whether the query found anything usable. Record the number because it is free; never
tune a query on it, and never report it as evidence a query worked.

The ledger is also what makes the lexicon honest — it is the raw log the lexicon's verdicts are
derived from, so a lexicon entry that no ledger line supports is a guess.

**Keep `scores.jsonl` even for losers.** `scores.jsonl` is your *prediction*;
`media_reviews.json` (approved / disapproved, written by the review UI) is the human's
*ground truth*. When he disapproves your install and grabs stocked option #4, that pair is a
labeled heat error — the only dataset that will ever validate or kill the provisional rows in
the rubric's Confidence table. Note also that POSTing a review status without re-sending
`note` **wipes the note**, and that reviews are per-ASSET after dedupe: one decision covers
every canvas reusing that file.

## Stop conditions

Hard limits — never exceed:
- **3 sibling-query rounds per slot.** If three differently-phrased Google queries can't put
  6 gate-survivors on the shelf, the problem is the term, not the query — go back to the word
  hunt or tell the user the beat may not have a name in this vocabulary.
  - **⚠️ Before blaming the term, check the SHAPE** (`references/chrome_route.md` §3). The
    recorded failure is almost never an exotic beat with no name; it is a query that named the
    act and *her* posture and let the corpus pick *his*. A slot can burn all three rounds on
    perfectly good terms and still return nothing usable because every result has the partner
    standing. That is a shape defect, and re-hunting the term will not find it.
  - **A setting-driven slot stops at 2, not 3** (`references/scoring_rubric.md` §SETTING). If two
    rounds come back with the room absent from *every* candidate, the room is not retrievable —
    score it `null` and rank on heat rather than spending the third round. The cap is tighter here
    because a missing room is cheap to work around (it costs SETTING points, never a rejection),
    while a missing act or posture is not.
- **10 total query variations per item**, across all rounds.
- **Skip items marked `[FAIL]` twice in `run_manifest.json`** — don't infinite-loop on cursed
  slots.

**Never end a slot silently.** When you hit a stop condition or the shelf comes up short,
surface the best of what you rejected — name the candidates, their gate reasons, and how many
options actually made it onto the shelf. If the entire surviving pool reads DEAD, install the
best of it, mark `pool_all_dead`, and say so plainly; a dead shelf is a query problem the user
can fix in ten seconds if you tell him, and an hour of debugging if you don't.

## Execution rule — always foreground

**Never use `run_in_background=true` in this skill.**

- **Search → judge is interactive.** You take a screenshot and immediately need to look at
  it. A backgrounded browser call hands you nothing to read.
- **Failures surface late in the background.** A silently-empty extract, a dead server, a
  0-byte fetch — all of them return "success" and you find out three steps later.
- **The re-query decision needs stdout.** Deciding whether a slot needs a sibling query means
  reading candidate counts and error text from the call you just made.
- **The calls are fast.** A `grab` is seconds. There is nothing to hide latency behind.

If a batch feels too slow for the foreground, the fix is **smaller batches**, not background
execution.

---

## Progressive disclosure — load on demand

The router above is enough to start. Load these when you reach the work they describe:

| Read this | When |
|---|---|
| `references/chrome_route.md` | Running the actual search: word hunt, browser tools, the extraction regex, stocking, fetching, judging. **The procedural spine — read it before your first query.** |
| `references/media_sources.md` | Choosing which shelf to point at: NSFW host catalog, tease/flash/explicit bands, the SFW stock shelf, the direct-fetch contract (headers, failure signatures, size floors) |
| `references/query_rewriting.md` | Writing or validating a query, synthesizing queries for empty `search_queries`, or reconciling the Google vs PornHub dialects |
| `references/scoring_rubric.md` | Judging candidates: the gates, HEAT/SETTING/CRAFT, the dead-clip veto, `scores.jsonl` |
| `references/sheets_and_boards.md` | Building the image JUDGE reads: `video_frames.py`, the contact sheet (`--sheet`), the strip board (`--board`), the mixed still/animated contract, evidence layout. **You are the shortlister — no model ranks the tiles.** |
| `references/content_rating.md` | Deciding SFW vs NSFW, or fixing a missing/wrong `_tN` tag (the audit + retag flow) |
| `references/api_behavior.md` | Confused about why the API saved a different extension than the TOML declared |
| `references/game_review_api.md` | Need the full `missing_media` entry schema or the API's category vocabulary |
| `references/audit_mode.md` | Auditing media a game **already has**, rather than filling holes |
| `templates/scope_brief.md` | Writing a SCOPE brief (the §Demand fields are the load-bearing part) |
| `templates/run_manifest.schema.json` | Writing the run manifest |

Scripts, all under `scripts/`: `validate_queries.py` (queries + format + tag proposals),
`scene_semantics.py` (tier / family / rating classification — imported, no CLI),
`apply_retags.py` (write corrected `_tN` into the phase TOMLs), **`fetch_candidates.py`
(stocked URLs → bytes on disk, in waves — the only fetcher; never hand-roll one)**,
`video_frames.py` (rep frames + strips + `--sheet` for the rep contact sheet and **`--board`
for the strip board — batch JUDGE reads a board, never one strip at a time**),
`tier_format_check.py` (pre-install gate), `dedup_tracker.py` (used-asset ledger).

**Interpreter.** Every script is **stdlib-only** and runs under plain `python3` — no pip
install, no virtualenv requirement, no pinned interpreter. The skill's **only** external
dependency is `ffmpeg`/`ffprobe` on PATH, which `video_frames.py` shells out to. Keep it that
way: a script that needs a package is a script that silently stops running.

**Exit code 3 means DEGRADE GRACEFULLY, never crash.** A script exits 3 when an *optional*
dependency is missing — in practice that is `video_frames.py` without ffmpeg on PATH. Fall
back (Read the thumbnails directly; use the harvest poster), keep going, and name the
degradation in your report. Exit 1 is a real gate failure; exit 2 is a usage error.
