# Media — images, video, clips (the image-first layer)

These games are **image-first**: the visual asset carries the scene and the prose is the ~35–40-word beat
hung off it (`references/rts-flat-prose.md` Rule 8). A scene with no media plan is a scene that ships blank —
a missing content image renders **nothing** to the player, silently. So media is not decoration you add at the
end; it's part of authoring the beat.

This file owns the media system: the real block shapes, the one engine law that trips everyone, what missing
files actually do, and — the part the skill was missing longest — **how to write the `search_queries` that turn
a scene into a findable asset.** Read it when you author any beat that carries a visual (Step 7) and when you
name a scene's intended media in the blueprint (Step 5). The actual fetching of art is a separate job — hand
off to the `find-media` skill (`.claude/skills/find-media/`); this file is about *authoring* the references it
consumes.

Every engine claim here is grounded in `apps/game_generation/twee_comprehensive/generators/v2.py` and
`apps/projects/services/template_import.py`. Where the old `prompts/` corpus taught a media fact wrong, it's
called out — the corpus is recovered for its craft, not trusted for its engine claims.

## Contents
1. The three block types (engine truth)
2. The resolution law — the on-disk file decides, not your filename
3. What a missing file actually does
4. Writing `search_queries` — the craft
5. Image vs video — the tier contract (authoring, not engine)
6. Placing media — the text-media-text rhythm + the 6 dimensions
7. Folder + naming convention (+ variant chains & cycling media pools)
7b. Media insurance — the corpus is the content plan, so protect it
8. Where media lives in the pipeline
9. Exemplar + anti-example
10. Cheat sheet

---

## 1. The three block types (engine truth)

Media is authored as a content block inside a canvas node's `blocks = [...]`, alongside `paragraph` and
`dialog`. Three media types are real: **`image`**, **`video`**, **`clip`**. (An unknown `type` is **not**
silently dropped — the importer **hard-fails the build** with a did-you-mean hint; `img`/`picture` → `image`.
`template_import.py:2786-2831` (`_CONTENT_BLOCK_TYPE_SUGGESTIONS` img/picture→image + did-you-mean hint). So a typo is caught at build, not in the shipped HTML.)

**`image`** — a still (renders `<img>`). `v2.py:14110` (`block_type == "image"` handler).
```toml
{ type = "image", props = {
    file = "scenes/penthouse_morning.jpg",   # path under the media folder (extension is advisory — see §2)
    description = "The penthouse by daylight, a woman at the glass with a tablet.",  # narrative; shown in debug + carried to the find list
    search_queries = ["penthouse window city morning", "woman apartment glass tablet"]  # see §4
} }
```
Optional props the engine also reads: `url` (a verbatim external URL instead of `file`), `alt`, `caption`
(wraps the image in `<figure><figcaption>`), and **`pool_dir`** — a *pool*:
```toml
{ type = "video", props = { pool_dir = "sex/brothel_oral_t5", pool = 4,
    description = "...", search_queries = ["...", "..."] } }
```
**A pool is a FOLDER.** Everything inside `videos/sex/brothel_oral_t5/` plays, and the block **CYCLES**
through it: visit 1 shows clip 1, visit 2 clip 2, wrapping back round. Files inside can be named
anything — the name only fixes the order (natural sort, so `clip_2` precedes `clip_10`).
`v2.py:11878` (`_render_media_pool`), `:11871` (`_resolve_pool_dir`), video branch `:14290`.

**`pool = 4` is a TARGET, not a manifest.** The folder is the truth. They are allowed to disagree —
3 clips in a 4-target pool plays a 3-cycle and the audit reports **"3 of 4"**. That split is the point:
the count is never hardcoded, so you curate by adding/removing files in the review UI instead of
editing TOML, *and* a half-filled pool still can't pass as finished. Omit `pool` and it defaults to 4.

> **Works on `image` and `video` blocks alike, and it is the right shape for rotating clips.** One
> `description` and one `search_queries` set covering the whole folder — which is the whole point:
> find-media searches **once** and keeps the gate-survivors it already paid to judge. A `block_pool` of
> N `video` blocks means N descriptions and N searches for a single beat: the *wrong* tool (§7).

**Cycle, not random.** `random()` over four clips repeats back-to-back 25% of the time — exactly the
staleness a pool exists to remove. The counter persists in `$game_state.media_cycle`, keyed on the
**folder** (`v2.py:11895`), which is why curating never resets a player's position mid-playthrough.

**Decide *whether* to pool before you decide what goes in it — §7.** Short version: NSFW media on a
repeatable canvas, whose clips are honestly interchangeable under one `description`. If the beat should
*escalate* rather than rotate, you want a `group` variant chain, not a pool.

**Optional `id` — tag a slot whose path you expect to move.** A media block's stocked options and
its approve/disapprove verdict are both filed under a string. By default that string is the
declared path, so **moving the path loses both** — a tier retag rewrites it, and converting to a
pool drops the extension. Measured: 148 stocked options stranded on the first pool conversion.
An authored `id` becomes the key instead, and it doesn't move:

```toml
{ type = "video", id = "renner_oral", props = { pool_dir = "sex/renner_oral_t5", pool = 4, … } }
```

- **Opt-in, and untagged is fine** — that is what ~560 existing blocks do. Tag the ones you expect
  to edit: anything you plan to pool, anything whose tier is still settling, hero assets.
- **Must be a real name**, not `b3`-shaped — the importer's own positional fallback ids look like
  that and are refused, because they shift when you insert a block above.
- Already stocked a shelf before tagging it? `python manage.py check_shelves --repair` moves it.
  `check_shelves` with no flags is the audit that tells you a shelf went missing at all.

> **Legacy: `files = ["a.webm", "b.webm"]`** — an explicit list, still supported and still cycling
> (`the_long_summer_test` ships 30 of them). Precedence is `pool_dir` > `files` > `file`, declared once
> in `apps/common/media_blocks.py`. Prefer `pool_dir` for anything new: an explicit list hardcodes a
> count you have to guess before seeing a single clip, and every entry it can't fill stays on the
> missing list forever.

> ⚠️ **An `image` pool still refuses clips — but it now says so.** Every entry is extension-checked and a
> `.mp4`/`.webm` in an *image* pool is dropped with a `logger.warning` (it used to vanish in total silence,
> unrendered and unrecorded). `.gif` and `.webp` count as images and work fine. **A `video` pool has no
> format filter at all** — it takes clips and stills alike and picks the right tag per entry, because the
> resolver is extension-agnostic and a pool asking for `.webm` can legitimately land on a `.gif`.
> Nothing in the importer validates media props, so a `file`/`files` typo still sails through.

**`video`** — a looping clip from a file (renders `<video autoplay muted loop>`). `v2.py:14285`
(`block_type == "video"` handler). Same props as image minus `alt`/`caption` — it **does** take
`files` (the cycling pool above, `v2.py:14290`), and that is the shape to reach for on any beat
the player replays:
```toml
{ type = "video", props = {
    file = "sex/renner_anal.webm",
    description = "She has him bent over the desk, taking the one thing he hasn't given yet.",
    search_queries = ["office desk sex from behind", "man fucking woman desk office"]
} }
```

**`clip`** — a pre-defined library asset by ID. **This is different from `file` media** and the corpus gets it
wrong. A clip carries **`clipId` only** — no `file`, no `search_queries`:
```toml
{ type = "clip", props = { clipId = "a1b2c3d4-…" } }
```
The id resolves to a database asset (`AssetClip.file_url`), **scoped to the project owner**, and renders a
hosted `<video>`. There is no disk file and no find-media handoff; if the id isn't accessible it's skipped
silently (not added to the missing list). `v2.py:13772-13817` (`block_type == "clip"`; `clips_by_id` → `AssetClip.file_url`). Use `clip` only when you're handed a clip UUID
from a library — **preserve the UUID exactly**. For art you intend to *find*, use `image`/`video`, not `clip`.

> ⚠️ **Corpus lie #1:** old `prompts_v2/schema/02` says clip uses `props.file`. False. Clip is `props.clipId`.

---

## 2. The resolution law — the on-disk file decides, not your filename

This is the one engine fact that trips everyone, so internalize it: **the engine ignores the extension you
write.** When it resolves `file`, it strips the extension and matches on the base path (folder + stem), then
looks at the **actual file on disk** to decide everything: `<img>` vs `<video>`, and the `images/` vs `videos/`
copy folder. `_find_media_file`, `v2.py:11301-11342`.

So `file = "scenes/intro.mp4"` happily resolves to `scenes/intro.webm` on disk — and a file you *labelled*
`type = "video"` but that resolves to a `.jpg` renders as an `<img>`. The `type=` you write and the extension
you write are **advisory**; the bytes on disk win.

> ⚠️ **Corpus lie #2:** the corpus implies your declared extension/`type` is authoritative. It isn't.
> **The two_weeks footgun:** that game tagged 92 sex scenes `type = "video"` but shipped `.jpg` files — every
> one rendered as a static image, no video ever played, and the `type=video` signal bought nothing. Match your
> `type`, your filename extension, and the asset you actually intend (see §5) so the three never disagree.

---

## 3. What a missing file actually does

A `file`/`url` that can't be resolved does **not** error and does **not** show a broken image. The block is
added to the build's **missing-media list** and then:

- **normal build → renders nothing.** The block silently vanishes. This is why a game with no real art looks
  like it has no media at all even when the references are correct. `v2.py:13606` (image `# else: skip
  silently`; the video path is the sibling near `:13723` (video `# else: skip silently`)).
- **`--debug` build → an `[IMAGE MISSING] <path>` placeholder** (dashed box) with the `description` and, if you
  gave `search_queries`, clickable search links (`v2.py:13571` gate, text `:13578`; video `[VIDEO MISSING]`
  `:13695`). **This text is baked into the HTML at BUILD time** — it does not re-check, so a `--debug` build
  ships the `[IMAGE MISSING]` text even if you add the media later without rebuilding. `--debug` is a QA
  affordance ONLY (see "QA vs publish build" below).

The **Missing-Media page** (a generated shopping list of every needed asset, each with its description +
queries) is **always built**, but its nav button only shows in `--debug`. So in a player build the gaps are
invisible; build with `--debug` to see the placeholders and the page.

Two other media surfaces degrade differently — know them so you don't confuse symptoms:
- **NPC/player portraits** (the `dialog`-block face) fall back to an inline **silhouette SVG** via `onerror`, so
  a missing portrait shows a grey shape, not nothing.
- **Location images** fall back to a **building SVG** and flip the nav to a visual grid.

The lesson: **coverage matters, and it's invisible in a normal build.** Give every media block a `description`
and `search_queries` so the missing-media page is a usable list, and check coverage with a `--debug` build.

### QA build vs publish build
- **QA (while authoring):** `--dev` (stat/canvas dev controls) + `--debug` (the `[IMAGE MISSING]` placeholders +
  the Missing-Media nav button). Always pass **`--video-folder <media-dir>`** or every clip 404s — the src
  resolves to an unpopulated copy path in ANY build (folder-independent; `--debug` does NOT switch folders —
  that older belief is wrong).
- **PUBLISH (for players):** DROP `--dev` AND `--debug` (keep `--video-folder`). *(A build that goes to
  players also runs the whole-game checklist first — `references/ship-gate.md`. This section owns the
  command; that file owns everything else a release has to clear.)* `--debug` freezes the
  `[IMAGE MISSING]`/`[VIDEO MISSING]` text into the file; `--dev` leaks dev controls. Minimal publish build:
  `python manage.py package_from_toml --file <toml> --output <dir> --video-folder <media-dir>` (no `--owner-id`
  — the no-DB build is the default).
- **`--codes <path>`** — the cheat-code file, **required** for any game that authors `[ui.cheat_page]`.
  There is **ONE build** now: the same file ships to the portals, to itch and to a supporter, and which
  cheat rows are live is decided at RUNTIME by the codes the player entered. `--build free|paid`, the
  `[builds]` block and `games/<slug>/output-paid/` were removed on 2026-08-23 — a leftover `[builds]` block
  is a hard validate() error, so a game carrying the old shape tells you instead of silently losing a badge.
  Codes live in **`games/<slug>/guide/codes.toml`**, untracked because `games/*/guide/` is gitignored and
  this repo is public. Only salted hashes reach the build. The same file feeds `manage.py build_guide`, so
  the guide can never document a code the build will not accept. `--no-codes` builds the page with nothing
  that opens it; omitting both is a build error.
  **Why this shape:** the retired model shipped the cheats in a separate downloadable build, which a phone
  cannot practically open — a paying supporter playing on mopoga or gamcore had no route to what they bought.
  8 of the 26 top mopoga games carry a live code box inside the free web build; only 3 ship a separate paid
  file. See `.claude/skills/author-game/CHANGELOG.md` (2026-08-23) for the measurement.
- **Two queries per block: a primary + one fallback.** Length is not the constraint — *content* is. A
  descriptive query is fine; a story-flavoured one is not.
- **Lead with the ACT and the POSITION, and say who does what to whom.** That is what the searcher must match
  and what the reviewer will check. `woman kneeling man standing blowjob` beats `back room encounter`.
- **⚠️ Name the setting ONLY when the setting carries meaning** — danger, secrecy, squalor, being somewhere
  you shouldn't be. Otherwise leave it out entirely and spend the words on the act.
  Measured: for a dim-storeroom beat, six setting-led queries returned 72 candidates and only 2 usable ones;
  one act-led query returned 28 and 5 usable. But for a dark-alley beat the darkness *was* the point, and
  bright clips were rejected twice — there, the setting word earns its place. Ask which kind of beat it is.
- **⚠️ NEVER put story or character words in a query** — names, "drunk", "nervous", "her boss", plot state.
  These do not merely add noise; on a general image index they flip the whole result set to mainstream
  content. Measured: adding `drunk guy` to a working query returned film stills, news and social-media posts
  and zero usable candidates. The narrative lives in `description`; the query is physical only.
- **Mood adjectives are still wasted words** (see the list below) but for the milder reason: they just don't
  index. The story-word rule above is the one that actually breaks a search.
- **Vocabulary mapping — use these exact terms:**
  | Narrative | Query term |
  |---|---|
  | his hand on/in her | `fingering` (never "manual" / "manual stimulation") |
  | his mouth on her | `cunnilingus` or `eating out` |
  | her hand on him | `handjob` (one word) |
  | her mouth on him | `blowjob` or `kneeling oral` |
  | penetration | `sex` / `fuck` (+ position) |
  | positions | `missionary` (face-to-face), `doggy` (behind), `riding` / `girl on top` (not "cowgirl"), `standing` |
  | settings (index — but see the ⚠️ above: only when load-bearing, and **at most two**) | kitchen, counter, couch, pool, table, shower, bed, bathroom, doorway, hallway, patio, outdoor, car, office, floor, desk |
- **⚠️ Gender-direction rule.** For acts that have heavy solo/lesbian results (fingering, cunnilingus,
  touching, rubbing), **always include `men`/`guy` + `girl`** or you get the wrong content.
  `kitchen fingering` → solo girls; `men fingering girl kitchen` → the M/F couple you meant.
- **⚠️ Wasted words (they don't index — leave them out):** passionate, desperate, urgent, emotional, intimate,
  lingering, forbidden, tender, intense, domestic, tension, longing, devoted, savoring, seductive, sensual,
  secret, lazy, beautiful, gorgeous, perfect, hot. Also "manual", "manual stimulation", "sexual tension".
- **Push away from studio porn when the beat is grimy.** `amateur`, `real`, `voyeur`, `hidden cam` are the
  words that do it. Bright-studio-when-the-beat-wants-dim is the single most common rejection we get, and
  these are the only reliable lever against it.
- **Tier-appropriate (see §5):** base/t2/t3 (SFW) = couple/action/setting, **no sex terms**; t4 = kissing /
  making out / hands on body; t5+ = the explicit vocabulary above.

**Good:** `["men fingering girl kitchen counter", "kitchen couple morning"]` · `["woman kneeling man standing
blowjob amateur", "kneeling blowjob eye contact"]` · `["couple wine patio night", "two people balcony evening"]`
**Bad:** `"manual stimulation kitchen morning light"` (unsearchable) · `"passionate fuck against wall urgent"`
(wasted words) · `"oral kitchen morning"` (ambiguous — say blowjob or cunnilingus) · `"back alley blowjob
drunk guy night"` (**"drunk guy" flips the whole search to mainstream results** — measured).

### The `description` is a checklist, not a caption

find-media derives its accept/reject gates from your `description`, and the reviewer checks the clip against
it. So write it **physically checkable**: who is where, in what position, who is visible, what act. "On her
knees on dirty concrete behind a bar, a slumped man above her" gives a gate. "A grim little transaction in the
dark" gives nothing, and whatever gets installed cannot be judged wrong.

A real cost of getting this wrong: a shipped clip in `vesper` showed the woman **standing** while its beat
said "on her knees" — it passed unnoticed for months because nothing was checkable enough to fail.

**Say what makes the beat land, too.** If the charge is her holding eye contact, or that she's being used and
not enjoying it, or that he's visibly wrecked — put it in the description. That is the one thing a searcher
cannot infer from an act name, and it is what separates a clip that is *correct* from a clip that *works*.

> ⚠️ **The key-name trap:** a **content block** uses bare `search_queries`. A **`[[locations]]`** entry uses a
> *different* key, **`image_search_queries`**, for its `image`. Same craft, different key — don't cross them.

---

## 5. Image vs video — the tier contract (authoring, not engine)

What format a beat wants tracks its heat:

| Tier | Heat | Format | Why |
|---|---|---|---|
| base / t2 / t3 | SFW — domestic, flirtatious, clothed | `.jpg` still | a setting/mood shot is enough |
| t4 | borderline — kissing, suggestive | `.jpg` or a short clip | either reads |
| t5+ | explicit sex | `.webm` looping video | a still can't carry the act |

Treat this as an **authoring/quality contract for the find-media pass, not an engine rule.** The engine doesn't
enforce it — resolution is extension-agnostic (§2), so a `.jpg` under a `type=video` block still renders as an
`<img>`. The point is human: **don't ship a 10KB static thumbnail as a sex scene.** A t5+ beat that can only
find a still should be reported as a gap, not filled with a JPG.

> ⚠️ **Corpus lie #3:** the corpus says "t5+ must be `.webm` or it won't render." The *engine* renders whatever
> the on-disk file is. The webm rule is a quality bar for the asset you fetch, not an engine gate.

**Density — count media *blocks* per canvas, not inline markers:** a talk/setting beat = 1 establishing image;
flirt = 1; kiss = 1 clip; oral = 1-2 clips; full sex = 2-3 clips marking the energy shifts. Escalation buys a
*new media slot*, not denser prose.

---

## 6. Placing media — the text-media-text rhythm + the 6 dimensions

**Text does the specific work; media does the mood work.** Build the beat as a sandwich
(`prompts/media_writing_guide.md:657-705`):

1. **Text before** — the specific approach. Character detail, internal thought, sensory grounding. Hyper-
   specific; no media needs to match this.
2. **Media** — the moment. It delivers the *feeling*; it matches broadly, not exactly.
3. **Text after** — the reaction, the aftermath, what it meant. Character voice.

**Rule: don't describe what the media shows.** Text before = approach, media = moment, text after = reaction.
Place the media block at the **action moment** (the pose, the act) or the **mood peak**, not over a line of
dialogue. (This is the same beat shape as a cascade: the establishing image opens the node, the act media lands
on the reveal.)

When you (or find-media) judge whether a found asset fits, the **6 dimensions, in priority order**, are:

| # | Dimension | Priority | Match requirement |
|---|---|---|---|
| 1 | Action | critical | what's physically happening MUST match |
| 2 | Setting | critical | the background location MUST be recognizable |
| 3 | People | important | count + gender MUST match; age/body should |
| 4 | Clothing | important | clothing level MUST match the tier |
| 5 | Energy | flexible | NPC personality should show; wrong energy beats wrong setting |
| 6 | Framing | flexible | nice-to-have; don't reject a good clip over the angle |

> ⚠️ **Corpus lie #4:** the corpus's worked scenes use an inline `[image: ...]` text marker. That is *brief-
> writing shorthand only* — the engine has no such syntax. Author the real TOML block (§1). The same shorthand
> in `rts-flat-prose.md` Rule 8 means the same thing: write the block, not the bracket.

---

## 7. Folder + naming convention (+ variant chains & cycling media pools)

The engine is path-agnostic (it joins your `file` under the media root and sorts by resolved type), so the
folders are a **house convention**, but keep it consistent so the find-media pass and the missing-media page
stay legible:

- `scenes/` — arc beats, capstones, sex · `activities/` — solo/repeatable · `locations/` — room art (the
  `[[locations]]` `image`) · `story/` — endings · `players/` — player/customizer art.
- **Filename encodes the tier:** `<slug>_<tier>.<ext>` — e.g. `breakfast_ethan_t5.webm`, `kitchen_base.jpg`.
  No suffix = base. The find-media pass reads the tier from the suffix to pick SFW-vs-NSFW search behavior.

Two engine features worth using:
- **Variant chains** — inside a `group`/`block_pool` (the conditional-content containers), give each branch its
  *own* media block (a different `.webm` per path) so the picture re-renders as state changes.
- **Media pools — `pool_dir` + `pool`, and they CYCLE.** A folder of clips shown one per visit. The
  shape is in §1; this is **when to reach for one**. Answer the gates in order — the first two decide
  whether a pool is even the right thing, and no amount of clips fixes a wrong answer to either.

  **Gate 1 — is it NSFW, on a repeatable canvas?** Both, not either.
    - *NSFW* (`_t4`/`_t5`): this is what the player replays *for*, so this is where staleness costs you.
      A location or establishing shot is **wayfinding** — the player reads it to know where they are —
      so rotating it is worse than useless. The engine agrees: a `[[locations]] image` resolves through
      a separate single-path route (`v2.py:485`) and **cannot** pool at all.
    - *Repeatable*: judge by expected **view count**, not by the flag. An ambient crossed fifty times
      earns four clips; a beat hit three times does not — that is three files found, shipped and paid
      for so one can be seen once. A Lane-4 capstone plays exactly once; a pool there is pure waste.
    - Evidence this is the real line: **27 of the 30** pools shipping in `the_long_summer_test` are
      under `sex/`.

  **Gate 2 — are the clips INTERCHANGEABLE?** This decides whether the pool is *fillable*. Every clip
  must satisfy the *same* `description`, so a loose one (a generic act) pools well and a tight one (a
  specific named gesture) cannot. Measured: `lab_finish_facial_t5` — *"his hand gentle at her head"* —
  came back **`pool_all_dead`, 24 candidates, every one rejected**. A 4-clip pool there wouldn't have
  been 4× the variety, it'd have been 4× impossible. If you can't write one description honestly true
  of all of them, you don't want a pool.

  **Gate 3 — should it ROTATE or ESCALATE?** A pool asserts the clips are interchangeable: nothing
  changed between visit 1 and visit 4 except a counter. If the 4th viewing should differ because
  **state** differs — corruption climbed, a flag flipped, a stage advanced — that is a `group` variant
  chain (above), not a pool. Reaching for a pool on a beat that should escalate quietly swaps character
  development for a slideshow, and it *looks* like it worked, which is what makes it the worse mistake.

  Then, and only then:
  - **How many — set `pool = 4` and stop thinking about it.** It is a target for find-media, not a
    manifest; the folder is what actually plays. 4 is the default because that is what the pipeline
    yields (measured strip survival **3-of-5 / 4-of-6**). You are not committing to it: 3 clips play a
    3-cycle and the audit says "3 of 4". Stills survive the strip at a much higher rate than clips, so
    an image pool can comfortably run larger — `the_long_summer_test`'s image pools hold 5–11.
  - **Cost — free to FIND, real to SHIP.** One `description` + one `search_queries` set covers the whole
    folder, so it is one search and one judging pass. The bytes are not free: `vesper` averages
    **2.9 MB per clip** (380 MB / 113), so **a 4-clip pool costs ~8.7 MB more than a single clip**.
    Multiply by however many you pool — and pool the beats the player actually lives in, not by reflex.
  - A pool rotates the **picture** while the beat's prose stays put — so on a heavily-repeated beat the
    words become the stale thing. If clip and prose must vary together, use N separate canvases
    (`lanes.md` — `vesper` ships eight at `captive_room`).
- **`block_pool` is a different tool, and it stays RANDOM.** It picks whole *blocks*, so its job is
  varying **prose** (the Lane-2 ambient text pool): `<<set _bp to random(0,N)>>` + an if/elseif chain,
  children recursing through the normal dispatch. **Do not reach for it to rotate clips** — N video
  children means N descriptions and N searches for one beat, which is 4× the find-media cost of a `files`
  pool for the same result. Constraints: a nested `block_pool` is silently stripped by the importer, depth
  caps at 4, mixed child types log a warning, and two pools in one node do not stay in sync (both roll `_bp`).

---

## 7b. Media insurance — the corpus is the content plan, so protect it

For a real-porn game the performer corpus **is** the content plan, and it is the least stable thing you
own. The field has three cautionary cases from the 2026-07 top-30 study: one top-20 game was legally forced
to replace all its real-porn media with dev-made AI art and its audience revolted overnight (every
top-liked comment was the revolt); another rebuilt its story and **recast its performer-NPCs**, and players
who had bonded with specific faces left ("I want my mom back"); a third had to **rewrite quests** because
the actresses had retired. None of those was a design failure. Four cheap habits:

- **The repo is NOT a backup.** Media is git-ignored by extension (a couple of portal-live games re-include
  their `output/videos/`, but that's the exception), so a tracked `games/<slug>/` proves almost nothing
  about the assets. Keep the media folder mirrored outside the build tree; a lost harvest is weeks of
  find-media work, not an afternoon.
- **The provenance record must survive — and it's ignored too.** The find-media pass writes a run manifest
  under the game (`.find-media/`) recording, per asset, the winning source + URL, the queries that found
  it, the tier and its scores. That's the only record of *where an asset came from* — and the repo ignores
  that directory as transient working evidence, so it needs the same off-tree mirror the media does.
- **Frame identity slots so a performer is replaceable.** For the **scene** slots that make an NPC *that
  person* — their signature beats, the shots a player reads as "her" — prefer framing you could crop or
  swap without the character dying (the field's fem-protagonist exemplar crops faces deliberately so
  players project onto the PC instead of onto a performer). **The portrait slots are exempt** — both the
  player sidebar portrait (`references/player-portrait.md`: subject centred, face upper-third) and the NPC
  portrait card (an 80px `object-fit: cover` circle) exist to be a recognisable face; that IS the identity
  anchor. The rule is about the scene corpus, not the two portrait surfaces.
- **Never name a performer in prose.** The game outlives any performer's availability; a name in the text
  turns a swapped asset into a continuity error you have to rewrite around.

---

## 8. Where media lives in the pipeline

- **Step 5 (blueprint):** when you place a scene, **name its intended media** — what the establishing shot is
  and (for a hot beat) what the act clip is. One line per scene; it makes coverage a design decision, not an
  afterthought.
- **Step 7 (authoring):** author the real block (§1) into the node, with `description` + 2 `search_queries`
  (§4), in the text-media-text rhythm (§6). Check it with a `--debug` build (§3).
- **Fetching the art:** hand the built game to the **`find-media` skill** — it reads the missing-media list
  (each entry's `description` + `search_queries`), runs the queries, and downloads assets into the media
  folder. This file authors the references; find-media fills them. Don't duplicate the fetch pipeline here.

---

## 9. Exemplar + anti-example

**Copy this** — `archive/the_inheritance_v1/toml_phases/3_activities.toml:97-104` (the v1 build, archived
2026-07-14 while the game is re-authored), the establishing-image →
paragraph → act-video rhythm in one node, each media block carrying a description + 2 queries:
```toml
blocks = [
  { type = "image", props = { file = "activities/porn_tv.jpg",
      description = "A dark bedroom lit only by the glow of an old TV, a young woman alone on the bed late at night.",
      search_queries = ["dark bedroom tv glow woman", "woman bed watching tv night"] } },
  { type = "paragraph", content = "The old set still pulls the channels nobody admits to. Sound low, lamp off." },
  { type = "video", props = { file = "scenes/act_porn_tv.webm",
      description = "She watches the late channel in the dark, heat building with nothing to spend it on.",
      search_queries = ["bedroom woman watching tv night", "girl aroused bed dark glow"] } },
]
```
`the_inheritance` ships 49 `type=video` `.webm` for its act layer, each with a description + 2 queries — the
shape to match.

**Don't copy two_weeks:** 92 sex beats tagged `type=video` shipped as `.jpg` (§2) — they render as stills and
the missing-media list is muddied. Tag matches asset matches intent, or don't tag it.

---

## 10. Cheat sheet

- Three real blocks: `image` `{file|files|pool_dir+pool|url, alt, caption, description, search_queries}` ·
  `video` `{file|files|pool_dir+pool|url, description, search_queries}` · `clip` `{clipId}` (DB asset,
  owner-scoped, no file/queries). Unknown type = build-fatal.
- **`pool_dir = "<folder>"` + `pool = 4` = a pool that CYCLES** (1→2→3→1), on either block type. The
  folder's contents play; `pool` is only find-media's target, so "3 of 4" is a healthy state, not a hole.
  Use it when the beat is **NSFW *and* on a repeatable canvas**, and only if the clips are
  interchangeable under one description — if they aren't, or if the beat should *escalate*, use a
  `group` variant chain instead. One search either way; ~2.9 MB per extra clip to ship.
  `files = [...]` is the legacy explicit form. `block_pool` varies *prose* and stays random.
- **The on-disk file decides `<img>` vs `<video>`** — your extension/`type` is advisory. Match all three.
- **Missing file = renders nothing** in a normal build (silent). Build `--debug` to see `[IMAGE MISSING]`
  placeholders + the Missing-Media page.
- **Every media block gets a `description` + 2 `search_queries`.** Queries: **act and position lead**;
  physical vocabulary only; name the setting only when it carries danger/secrecy/squalor and then with
  **at most two** setting words; the gender-direction rule for solo-prone acts; no banned/emotional words.
  (The "3-5 words, setting first" formula is **retired** — see the ⚠️ box in §4. Descriptive
  natural-language queries are correct here; `find-media` handles the search-engine dialect.)
- Locations use **`image_search_queries`**; content blocks use **`search_queries`**. Different key.
- SFW beats = `.jpg`; explicit beats = `.webm`. Quality contract, not an engine gate.
- Text before (specific) → media (mood, broad match) → text after (reaction). Don't describe what the media
  shows. Place at the action moment / mood peak.
- Step 5 names the media; Step 7 authors the block; **`find-media`** fetches it.
