---
name: find-media-v3
description: EXPLICIT-INVOKE ONLY — the experimental v3 of media finding, run when the user asks for "/find-media-v3", "find media v3", "media v3", or "use v3 on <game>". Hunts the query, proves the query landed (host histogram + one grid look), then stocks EVERYTHING the results pages offered onto the slot's shelf — no fetching, no contact sheet, no triage, no pruning, and installs NOTHING: the human judges every candidate himself in the media-review UI and his pick is the install. Do NOT use for a plain "find media for <game>" / "populate media" / "missing media" request; those belong to the incumbent find-media skill until the user promotes this one.
---

# find-media v3 — prove the query, dump the shelf, install nothing

**v2 narrowed 70 candidates to 1 install. v3 hands the human all 70.**

That is the whole change. Everything upstream of the results page — the word hunt, the act
anchors, the query shape, the Chrome route — is v2's, unchanged, because it is the part that
was measurably working. Everything *after* the harvest is deleted: ranking, scoring, frame
strips, boards, `scores.jsonl`, fetching, contact sheets, triage, pruning, and the install.
The only quality control is per-QUERY — did the search land? — never per-candidate.

## Why (read this once — it prevents re-adding what was cut)

Measured on `vesper`, 2026-08-04: 32 queries across 18 pool slots took over an hour, ~7–8
minutes a slot. The dominant cost was visual judging — fetch top 8, build a sheet, strip the
top 6, read a board, rank, write scores for winners and losers.

Almost none of that output survived to a decision:

- **The ranking never reaches the human.** `find.html` shows the shelf in stocking order.
  Ranks are computed, written, and never rendered. They decided only which clip became a
  placeholder.
- **The human re-judges everything anyway.** The review UI plays real loops — `.gif` in an
  `<img>`, `.webm` in a `<video>`. A 4-frame strip is a worse approximation of exactly the
  thing the human does natively, one step later.
- **He picks from the shelf, not from the install.** His words: *"most of the times… I do
  choose from the other urls."*

So the machine's job is **"is this the right QUERY"** — a per-search question the host
histogram answers for free. The human's job is **everything per-candidate** — he was already
re-judging every clip in the review UI, watching real loops, which beats any frame-level check.

v3 briefly kept a residual judging step (fetch the top ~24, read one contact sheet, bin the
frame-level-wrong, prune the rest). The first live run (`media_lab_g`, 2026-08-04) killed it,
by LO's call: it looked at 24 of ~140 and deleted the unseen ~110 — certifying a sample while
destroying the majority, which is the exact candidate-destruction v2's STOCK step exists to
prevent (the back-room beat's winner was a runner-up the machine had scored lower). It was
also most of the per-slot cost. **If you cannot verify all of them, verify none of them and
let the reviewer see everything.**

**The corollary that must not be lost:** because nothing is installed, an unreviewed slot is
an *empty* slot. The game renders a hole until the human picks. That is deliberate — LO chose
it over placeholders — and it makes the review pass a hard dependency of shipping, not a
nicety. Say so in every report.

## Status — this skill is UNDER TEST

`find-media` (v2) remains the default and answers every generic request. v3 runs only when
the user names it. Nothing here edits v2, and both write the same ledgers, so a game can be
worked by either.

**On promotion** (LO's call, after he has tested it): swap the two `description` fields so
v3 takes the generic triggers, move `scripts/` and `references/` into this directory, and
freeze v2 as the rollback — the same pattern the generator uses for v2/v1.

## The deliverable contract

Every worked slot ends with **both**:

1. **A query-verified FULL shelf** in the options store — everything the **proven** queries'
   results pages offered, after the extract-time filters only (phncdn cut, empty-path cut,
   furniture-host cut, correct `media_kind`). Expect 150–350 options on a healthy slot with
   3 sibling queries (measured across `media_lab_f`/`_h`, 20 slots).
   Verification is per-QUERY — the host histogram, read **before** the shelf is written
   (§4) — never per-candidate.
   Dead links and wrong-kind clips WILL be on the shelf (~10–30% each, measured on
   `media_lab_g`); the human flicks past them in the review UI, which costs seconds and
   destroys nothing. **What must NOT be on the shelf is the output of a query the histogram
   condemned** — that is not dump-all, it is a gate that fired too late, and §4 fixes it.
2. **Every candidate LABELLED with the search that found it**, and every search recorded —
   including one that yielded nothing. The picker groups the shelf into one bucket per search
   (newest first) and puts your histogram verdict on the chip, so "these results are wrong"
   finally lands on a specific query instead of the whole pile. An option stocked without a
   `query` is unattributable **forever**; see §4.
   **And every candidate carries its `docid`** when §4's join paired one (chrome_route.md §4
   — the metadata-triple regex, part of the same extraction pass). That id is what makes the
   picker's ⇢ "fetch related" a one-navigation lookup; an option stocked without it needs a
   whole grid re-search later, which usually fails on aged shelves. Contract since 2026-08-05.
3. **Nothing installed.** The slot stays empty and the review page shows
   `N options — pick` (the `ready_to_pick` state, `api/v1/media_review.py`).

You may never: install a file, rank the shelf, score a candidate, fetch-and-judge candidates,
frame-strip anything, build a contact sheet, or PRUNE a stocked option for any reason other
than the hard-dead byte sweep the human explicitly asked for (§Janitor). **Deleting a
candidate the human has not seen is the failure this skill exists to prevent** — which is why
the refetch prune is gone too (§4): buckets made it unnecessary, so it was only ever loss.

**Floor 6 is a QUERY-HEALTH signal, not a shelf target.** A slot that stocks under ~6 after
2–3 sibling queries has a broken query — fix the query (§Iteration), never pad the shelf.

---

# The phase flow

Steps 1–4 are **v2's, unchanged**. Read them from v2's files; do not re-derive them.

## 0. Decision tree — before any work

Identical to v2 `SKILL.md` §"Decision tree": resolve `games/<game>/toml_phases/*_final_game.toml`
(glob the number), confirm the Django dev server is up on `localhost:8000` (the in-page
`fetch` that stocks options fails *silently* against a dead server), fetch the missing list:

```bash
curl -s "http://localhost:8000/api/v1/dev/game-review/load?game=<game>" \
  > games/<game>/.find-media/game_review.json
```

(no trailing slash on `load` — it 404s), run v2's TOML-walk cross-check, and do the tier
audit/retag before scoping. **Pools:** a `pool_dir` slot is ONE row, ONE shelf, keyed by
`pool_dir` — v2 `SKILL.md` §"A POOL slot wants N files" still governs, minus the install half.

## 1. SCOPE (lite) — only what the query and the gates read

Fill `templates/scope_brief.md` (v2's), but only these fields carry now:

| Field | Used by |
|---|---|
| act, position, people count, direction | the query shape — nothing downstream judges candidates anymore |
| `setting_is_load_bearing` | whether the query spends 2 tokens on the room |
| `pov_case` | the query only: when the beat needs the partner's body seen, keep `pov` out of the terms |
| `intended_heat` | the query's flavour words |

Everything v2's brief carried for *scoring* is dead weight here — there is no HEAT/SETTING/CRAFT
axis to feed. Do not write one.

## 2. PLAN — hunt the word, then write the queries

**Unchanged from v2.** `references/chrome_route.md` §1 (word hunt: Google's own result labels
are the richest mine) and `references/query_rewriting.md`.

Validate before running anything:

```bash
python3 .claude/skills/find-media/scripts/validate_queries.py \
  --from-api-json games/<game>/.find-media/game_review.json
```

The two rules that decide whether a query lands at all, both measured:

- **One unmistakable act word or the query leaves porn entirely.** `riding cowgirl man in
  office chair gif` → 83 urls, **0** on a porn host. `cowgirl riding fuck office chair gif` →
  73 urls, **69** on porn hosts. Positions are ordinary English; `ACT_ANCHORS` in
  `scripts/scene_semantics.py` is the list that isn't.
- **Name HIS posture when it isn't the act's default.** `kneeling blowjob` retrieves
  she-kneels-he-STANDS. A beat that needs him seated must say `office chair` / `under the
  desk`. The largest single source of rejections in this skill's history.

Plus: zero story or character words, `gif` appended (measured 7→59, 1→54, 0→91 fetchable
urls), an anti-studio modifier (`amateur`, `real`, `voyeur`) when the beat is grimy, and at
most ~2 setting tokens.

## 3. SEARCH — drive the user's own Chrome

**v2's `references/chrome_route.md` §§2–4 govern — EXCEPT its §2.0 preflight, which v3
replaces. The rest stands: Google Images cannot be curled, so the browser is mandatory.**

### PREFLIGHT — probe with `tabs_context_mcp`, never gate on `list_connected_browsers`

⚠️ **`list_connected_browsers` returns `[]` while the browser is fully reachable.** Measured
2026-08-05 on `media_lab_f`: three per-slot agents obeyed v2's "on `[]` STOP" rule and killed
their slots; a fourth ignored the empty list, called `tabs_context_mcp` anyway, got a live tab
group and harvested 192 urls. **An empty list is not evidence of a dead browser.**

The probe order, in this order:

1. `tabs_context_mcp {createIfEmpty: true}`. A tab group back = **you are connected, proceed.**
   This is the only liveness signal that has proven reliable.
2. Only if *that* errors: `select_browser` with the known deviceId, then retry step 1 once.
3. Only if **both** fail: stop and report the exact errors. Every documented workaround
   (curling Google directly, mining a sibling slot's shelf) was measured and is wrong.

Then `tabs_create_mcp` for your own tab and work only that `tabId`.

⚠️ **`"Could not verify this site's safety category. Blocking as a precaution — try again in
a moment."` is TRANSIENT — retry once, do not treat it as a stop.** It is the extension's own
safety lookup timing out, it can fire mid-batch and discard the batch's earlier results, and it
reads exactly like a hard block. Two agents hit it and cleared it with an identical retry; it is
the likeliest cause of the run that was misdiagnosed as a dropped pairing.

**A genuine refusal is different and is final.** `"Cannot access this page. Claude cannot
assist with the content on this page."` is a real block. Log it as a gap in the ledger and move
on — **never reword a query to get past it.** Rephrasing around a safety refusal is
circumventing it, which this skill does not do at any scale.

Then: build `https://www.google.com/search?q=<terms>&tbm=isch`, confirm from the screenshot
you are on the image grid, extract with the one regex (`.split('?')[0]` is not optional),
group by host, cut `*.phncdn.com` (not fetchable — discovery only), scroll and re-extract to
find the page's edge.

**Read the host histogram — it is the query's diagnosis, and it is free.** Tenor/Wikipedia/BBC
means no act anchor. Reddit stills/TikTok means a story word leaked in. Getty/Shutterstock
means the setting words reclassified it as stock photography. Each wrong crowd names the exact
token to change, which is what makes iteration cheap.

**Run 2–3 sibling queries per slot, never one.** Different phrasings land on different host
clusters. v3 spends part of its saved time here: when a slot is comfortably over the floor
after two queries, **run a third distinct query anyway** — shelf variety comes from query
variety, and this is the step that produces it.

**Still-image slots (`type: image`, usually the SFW ones) need a WIDENED extract.** The §4
regex matches `gif|mp4|webm` only, so an image slot harvests as ZERO from a completely full
grid — measured on `media_lab_g` slot 10: 0 urls with the animated regex, 93 with
`(?:jpg|jpeg|png|webp)`. Widen the extension group for that slot only, keep every other
filter, and stock with `type: "image", media_kind: "img"`. Expect the stock-photo crowd
rather than the porn aggregators: iStock/Alamy/Dreamstime/Shutterstock watermark their
previews; Pexels/StockCake/Freerange are the clean end. The watermarks land on the shelf
with everything else — the human sees them on the tiles and picks around them.

## 4. STOCK — everything a PROVEN query offered. Two passes, gate first.

`references/chrome_route.md` §5, with one change v3 makes and v2 does not need.

### The gate fires BEFORE the shelf is written — two passes, not one

⚠️ **Extract and stock must NOT be the same script.** They were until 2026-08-05, which put
the per-query gate *behind* the write: a wrong-crowd query's candidates were already on the
shelf by the time the histogram diagnosed them, and §Contract forbids pruning them off. Three
independent agents flagged it on the same run. Measured cost on `media_lab_f`: **127 of the
tease slot's 336 options (38%) are golf swings, Vogue stills and a pony-booru gif**; ~90
skincare gifs on facial; ~56 magazine gifs on passive.

So, per query:

1. **Pass 1 — extract + histogram, write NOTHING.** Return the url list and the host counts.
2. **Read the histogram.** Wrong crowd → fix one token, re-run pass 1. Do not stock.
3. **Pass 2 — stock the list you already hold**, only once the query is proven.

One extra round trip per query. It reintroduces no per-candidate judgment whatsoever — the
gate is still per-QUERY, it simply now runs in time to matter.

⚠️ **Join the hostname labels with `" DOT "` in what the script RETURNS — and nowhere else.**
Bare dotted CDN hostnames trip a secret-scanner in the tool output filter and come back as
`[BLOCKED: JWT token]` — measured on three runs, once redacting 6 of 8 rows. **The histogram
is v3's only quality gate; a redacted histogram is a blind gate**, and it fails silently,
which is worse than failing loud. But a **POST body never passes through that filter**, so the
`hosts` array you send to `queries/add` keeps real hostnames. Transform once and reuse the
transformed array and the store is poisoned beyond repair — a host legitimately containing
`" DOT "` is indistinguishable from a mangled one. The endpoint answers 400 on a transformed
host; read that as "I transformed too early", never as "the endpoint is broken".

### The histogram is now a DELIVERABLE, not a scratch value

It used to be computed, read once, and thrown away — the single most informative artifact of a
run, and the human never saw it. Send it to `queries/add` and it becomes the label on that
search's chip in the picker: `dogging fuck alley wall voyeur gif · 75 · 100% porn hosts` next
to `tender intimate facial gif · 91 · 33% porn hosts`. That is your gate verdict reaching the
person who has to act on it, and it costs one POST you are already positioned to make.

Non-negotiables (each has a recorded failure behind it):

- `file` = the slot's TOML-declared path, character for character; also send the item's own
  `slot_key` verbatim — the shelf is keyed on it, and a tagged slot's shelf survives its path
  moving.
- **`query` on every `options/add`.** It is what puts a candidate in a labelled bucket instead
  of an undifferentiated pile. There is **no retroactive attribution** — the ledger records
  only a date, and dedup makes timestamps non-invertible — so an option stocked without it is
  filed under "older searches" permanently. ~19,300 already are; do not add to them.
- **One `queries/add` per query, including a query that yielded ZERO.** A search that came back
  empty is the record that stops you re-running a dead query three rounds later, and nothing
  else in the system would remember it. It also writes the `query_ledger.jsonl` line, so you
  never hand-write one again.
- `game` in the **body** on every `media-finder` POST; in the **query string** on
  `options/list` (a GET) and on media-review endpoints.
- `media_kind` is exactly `img` or `video` — never `"image"`. `.gif` → `img`; `.webm`/`.mp4`
  → `video`. A wrong value renders the tile blank, which reads to the human as a dead option.
- **A refetch is just another query. Stock it under its own label and do NOTHING else.** The
  old rule here was "stock first, prune after" (`options/clear {before: t0}`) — that existed
  only because a shelf was one undifferentiated pile, so a refetch had to *destroy* the old
  pile to be legible. With labelled buckets the newest chip already IS the fresh shelf that
  prune used to manufacture, and pruning now only deletes candidates the human has never seen
  — the exact failure §Contract exists to prevent. **v3 never calls `options/clear`.** (v2
  still does; it installs, and its refetch has different work to do.)

---

## 5. CLOSE — report, never install

No install step. Per slot:

1. Confirm the shelf: `GET options/list?game=<game>&file=<slot_key>` → it returns
   `{options, queries}`. **Check both.** `queries` is the picker's chip strip; a slot with
   200 options and one chip means you stocked most of them without a `query` and they are
   unattributable forever.
2. Append to `games/<game>/.find-media/run_manifest.json`:
   `{"slot", "generator": "v3", "status": "shelf_ready", "options": N, "queries": M}`.
3. Report: **N options across M labelled searches, nothing installed, waiting on the human's
   pick.** Name any query whose histogram you judged a wrong crowd — it is on his shelf under
   its own chip, so he can dismiss the whole bucket at a glance instead of flicking past it.

**Pools are identical.** One shelf keyed on `pool_dir`; the human's picks in `find.html` fill
the folder one clip at a time (`grab` with `pool_dir` set — his UI already does this). v3 never
calls `grab`.

## Janitor — OPTIONAL dead-link sweep. Script-only, judgment-free, on request

Not yet built; run it only when LO asks for it by name. A dumped shelf carries ~10–30% dead
links (measured on `media_lab_g`'s fetch waves). The janitor is a script pass — no model
turns, no contact sheet, no gates — that walks `media_options.json`, HEAD/GETs every URL,
and removes ONLY hard-dead entries: non-200, HTML bytes, under 1024 B. It never touches
`origin:"previous"` rows and never bins on content, composition, or format-vs-tier — that
would be triage growing back through the back door. This is now the ONLY shelf-prune the
contract permits, and it is the natural customer for the rolling pool
(§Execution model).

---

## Iteration and stop conditions

- **Under ~6 stocked, or a grid serving the wrong crowd → run a sibling query**, now, while
  the tab and vocabulary are warm.
- **3 sibling-query rounds per slot. 10 query variations total.** Then stop and surface it.
  - Before blaming the term, **check the SHAPE** — the recorded failure is almost never an
    exotic beat with no name; it is a query that named the act and *her* posture and let the
    corpus pick *his*.
  - ⚠️ **When one token has to go, suspect the POSTURE word before the ANATOMY word.**
    Posture is shared vocabulary with sports, fitness and fashion writing; anatomy is not.
    Measured 2026-08-05: `downblouse leaning forward cleavage` died on Tenor/Pinterest. The
    obvious suspect was `cleavage` — the SFW-ish word. Dropping it made things *worse*
    (golf, Vogue, Hearst, a physics blog). The poison was **`leaning forward`**, a fitness
    posture term; `downblouse tease amateur` landed clean. The innocent-looking word was the
    guilty one, and one wasted round trip proved it.
  - **Poisoned by measurement, do not use:** `lazy sex`, `passive man`, `doing nothing`
    (all pull sex-advice and magazine editorial *even with a real act anchor*); `cowgirl`
    alone (zero porn hosts — needs `fuck` present); `facial` beside vanilla affect words
    (reads as skincare — use `cumshot`); `desk` with `prone bone` (ergonomics — use `table`);
    `leaning forward` (sports/fashion).
  - **A `hotwifecaps.com`-dominated histogram is a soft warning**, not a pass: that host
    serves caption images rather than act footage, so the query has drifted toward
    text-overlay content.
  - A setting-driven slot stops at **2** rounds: if the room is absent from the entire grid,
    it is not retrievable, and in v3 that costs nothing at all.
- **Skip a slot marked `[FAIL]` twice** in `run_manifest.json`.

**Never end a slot silently.** When a shelf comes up short, name which queries failed and on
what crowd (the host histogram says), and how many options actually made it. A thin shelf is
a query problem the human can fix in ten seconds if you tell him.

## Execution model — ONE AGENT PER SLOT, rolling cap 20

**This section said the opposite until 2026-08-05.** It claimed "the find run is SERIAL" and
"the browser cannot fan out: one Chrome, one extension pairing, one driver," and it forbade
delegating browser work to a subagent. **Both claims were written without ever being tested,
and both are false.** They were asserted twice before LO's third challenge forced a test that
took one tool call to run. Whatever else this section says, keep that: *the rule that cost the
most here was the one nobody had checked.*

What is actually true:

- **One Chrome — but a Chrome holds many TABS**, every MCP call names a `tabId`, and nothing
  serializes them. Measured: 3 tabs harvesting 3 slots at once, 0 failures.
- **Subagents work.** Measured on `media_lab_f`: 10 slots, one agent each, all handshakes
  clean, ~3 min per agent, all concurrent. Against the same 10 beats run serially on
  `media_lab_g` (104 min), the whole harvest collapsed to roughly one agent's runtime.

### The model

**Fan out ONE AGENT PER SLOT, with a rolling cap of 20 — a concurrency CAP, never batches.**
Queue every slot, keep ≤20 agents in flight, backfill the moment one finishes. No barriers:
never "launch 5, wait for all 5, launch 5 more" — a barrier wastes every fast finisher's idle
time on the slowest straggler. Workflow's `pipeline()`/queue implements exactly this.

**Each agent owns its slot end to end**: read the beat → author its own queries → probe
(§3 PREFLIGHT) → its own tab → gate → stock → close its tab → return a structured report.

**This is the point of the design, not a speed trick.** Query authoring *and query repair*
move into the slot. Measured on `media_lab_f`: four agents caught a wrong crowd in their own
histogram and fixed it unaided. A single driver holding 100 slots must author ~300 queries and
read ~300 histograms in one context — the real ceiling was never the browser, it was the
driver's attention.

### Rules for the fan-out

- **Hand each agent the deviceId.** It cannot ask the user anything — an agent that blocks on
  a "which browser?" prompt is a dead run, not a slow one. Forbid `AskUserQuestion` explicitly.
- **Each agent creates and closes its OWN tab**, and touches no sibling's tab.
- **Every agent returns a structured report** — per-query text, url count, host histogram,
  verdict, and anything it could not do. An agent that died or came back short is named **by
  name** in the close, never absorbed into a total.
- **A zero shelf mid-flight means NOT FINISHED, not failed.** Do not relaunch a slot whose
  agent is still running; that mistake double-ran a slot on `media_lab_f`.
- **Never `run_in_background` a browser call from the main driver** — that rule survives, and
  it is about *the driver*, not about subagents: a silent failure must surface attributed to
  the query that caused it. Delegating to an agent that reports back does not break it.
- The shelf store serializes writes (`media_options.json.lock`, ~3 ms/op), so concurrent
  per-slot API calls are safe.
- Google tolerated 3 and then 10 concurrent search streams with **no captcha**. If one ever
  appears: **hard stop, never solve it**, report and wait for the human.

### Byte-work (§Janitor, audit mode)

Same rolling cap of 20. Any agent fetching bytes uses `--workers 2` — N agents share the same
few throttling CDNs. v2's weather box measured the throttle (7.8s → 34.1s per file at 8
workers), and this file taught `--workers 6` for one day, which cost a full wave of masked
`ERR URLError`s. If ≥⅓ of an agent's wave dies `URLError`, it reruns once with `--workers 1`
before blaming the hosts.

## Evidence and persistence

```
games/<game>/.find-media/
├── game_review.json            # cached missing list
├── lexicon.md                  # terms confirmed (compounds across runs — the one thing that does)
├── query_ledger.jsonl          # EVERY query — now written FOR you by queries/add, not by hand.
│                               # {slot, query, date, round, source, urls_yielded, status}
├── scope/<item_id>.md          # lite briefs
├── media_options.json          # the shelf AND its query table, both written by the options API
├── media_reviews.json          # the human's verdicts
└── run_manifest.json           # generator: "v3"
```

**Not written by v3:** `scores.jsonl`, `strips/`, `board*.jpg`, `evidence/<item>/candidates/`,
`contact_sheet.jpg`. The first three are v2's JUDGE; the last two are v3's own deleted triage
(2026-08-05). Creating any of them means a judging step is growing back — stop.

**Evidence never lives in `/tmp`** — it got wiped twice in one session and took the candidate
pool with it both times.

⚠️ **`urls_yielded` is NOT a quality signal.** Measured across 31 vesper queries: 40–92 urls
with no relationship to usefulness. Log it because it is free; never tune on it.

## Shared machinery — this skill owns no code

Every script lives in **v2's directory** and is called from there. No copies: a duplicated
script is one that stops getting the other's fixes.

`.claude/skills/find-media/scripts/` — `validate_queries.py`, `scene_semantics.py`,
`apply_retags.py`, `fetch_candidates.py`, `video_frames.py`, `tier_format_check.py`,
`dedup_tracker.py`. All stdlib-only under plain `python3`; the only external dependency is
`ffmpeg`/`ffprobe` on PATH. **Exit 3 = degrade gracefully**, exit 1 = real gate failure, exit
2 = usage error.

References, all under `.claude/skills/find-media/references/`:

| Read | For | Applies to v3? |
|---|---|---|
| `chrome_route.md` | §1 word hunt, §2 tooling, §3 query construction, §4 extraction, §5 stock, failure table | **Yes — §§1–5, EXCEPT §2.0's preflight (v3 §3 replaces it: `list_connected_browsers` false-negatives) and §5's one-pass stock (v3 §4 gates first). §6 fetching only for §Janitor/audit byte-work; §7 JUDGE not at all** |
| `query_rewriting.md` | writing/validating queries, synthesizing empty `search_queries` | Yes |
| `media_sources.md` | host catalog, the direct-fetch contract, size floors | Yes |
| `content_rating.md` | SFW vs NSFW, the `_tN` audit + retag flow | Yes |
| `game_review_api.md` | the `missing_media` entry schema | Yes |
| `api_behavior.md` | why the API saved a different extension than the TOML declared | Yes |
| `audit_mode.md` | auditing media a game already has | Yes |
| `scoring_rubric.md` | HEAT/SETTING/CRAFT, ranking, the dead-clip veto | **No — deleted in v3; nothing replaces it. The human judges** |
| `sheets_and_boards.md` | strips, boards, the ranking contract | **No — v3 builds no sheets at all (triage deleted 2026-08-05)** |
