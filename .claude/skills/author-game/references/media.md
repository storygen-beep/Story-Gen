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
7. Folder + naming convention (+ variant chains & random pools)
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

**`image`** — a still (renders `<img>`). `v2.py:13455-13659` (`block_type == "image"` handler).
```toml
{ type = "image", props = {
    file = "scenes/penthouse_morning.jpg",   # path under the media folder (extension is advisory — see §2)
    description = "The penthouse by daylight, a woman at the glass with a tablet.",  # narrative; shown in debug + carried to the find list
    search_queries = ["penthouse window city morning", "woman apartment glass tablet"]  # see §4
} }
```
Optional props the engine also reads: `url` (a verbatim external URL instead of `file`), `alt`, `caption`
(wraps the image in `<figure><figcaption>`), and **`files`** — a *pool*:
```toml
{ type = "image", props = { files = ["sex/loop_a.jpg", "sex/loop_b.jpg", "sex/loop_c.jpg"],
    description = "...", search_queries = ["...", "..."] } }
```
`files` (a string array) **wins over `file`** and emits `either(...)` so a different image shows on each visit —
replay variety for a repeatable scene. `v2.py:13702-13790` (`files` pool wins over `file` → `either()`).

> ⚠️ **The pool is IMAGE-ONLY, and it drops video SILENTLY.** Every entry is extension-checked and
> non-images are skipped with no warning (`v2.py:13728`), so a `files` pool of `.mp4`/`.webm` resolves on
> disk, gets emptied, and renders **nothing** — no error, and nothing in the importer validates media props
> at all. `.gif` and `.webp` DO work (they count as images). **For rotating CLIPS use a `block_pool` of
> `video` blocks** (§7) — its children recurse through the normal dispatch, so the real video handler runs.
> Full trap: `references/toml-gotchas.md`.

**`video`** — a looping clip from a file (renders `<video autoplay muted loop>`). `v2.py:13908+` (`block_type == "video"` handler; `<video autoplay muted loop>` at `:14005`). Same props as
image minus `files`/`alt`/`caption`:
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

---

## 4. Writing `search_queries` — the craft

`search_queries` are **search-engine queries for an adult-content site**, not scene descriptions. The
`description` field carries the narrative; the queries carry **platform-searchable vocabulary only.** The
find-media skill runs them to fetch the asset, so vague or literary queries return nothing usable. The engine
just stores the array verbatim (it never validates it), so this is pure craft — and it's the half Vesper, Last
Call, and Late Shifts all skipped.

**The rules (recovered from `prompts/toml_generation_prompt_v4.txt:905-1001`, engine-verified neutral):**

- **Two queries per block: a primary + one fallback.** **3-5 words each.** **Setting word goes FIRST** (the
  setting is the hardest thing to match, so anchor on it).
- **Queries are physical, not emotional.** The search index ignores story/feeling words — they add noise, not
  signal.
- **Vocabulary mapping — use these exact terms:**
  | Narrative | Query term |
  |---|---|
  | his hand on/in her | `fingering` (never "manual" / "manual stimulation") |
  | his mouth on her | `cunnilingus` or `eating out` |
  | her hand on him | `handjob` (one word) |
  | her mouth on him | `blowjob` or `kneeling oral` |
  | penetration | `sex` / `fuck` (+ position) |
  | positions | `missionary` (face-to-face), `doggy` (behind), `riding` / `girl on top` (not "cowgirl"), `standing` |
  | settings (index these — put FIRST) | kitchen, counter, couch, pool, table, shower, bed, bathroom, doorway, hallway, patio, outdoor, car, office, floor, desk |
- **⚠️ Gender-direction rule.** For acts that have heavy solo/lesbian results (fingering, cunnilingus,
  touching, rubbing), **always include `men`/`guy` + `girl`** or you get the wrong content.
  `kitchen fingering` → solo girls; `men fingering girl kitchen` → the M/F couple you meant.
- **⚠️ Banned words (noise — never put them in a query):** passionate, desperate, urgent, emotional, intimate,
  lingering, forbidden, tender, intense, domestic, tension, longing, devoted, savoring, seductive, sensual,
  secret, lazy, beautiful, gorgeous, perfect, hot. Also "manual", "manual stimulation", "sexual tension".
- **Tier-appropriate (see §5):** base/t2/t3 (SFW) = couple/action/setting, **no sex terms**; t4 = kissing /
  making out / hands on body; t5+ = the explicit vocabulary above.

**Good:** `["men fingering girl kitchen counter", "kitchen couple morning"]` · `["doorway blowjob kneeling",
"hallway oral standing"]` · `["couple wine patio night", "two people balcony evening"]`
**Bad:** `"manual stimulation kitchen morning light"` (unsearchable) · `"passionate fuck against wall urgent"`
(noise words) · `"oral kitchen morning"` (ambiguous — say blowjob or cunnilingus).

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

## 7. Folder + naming convention (+ variant chains & random pools)

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
- **Random pools — two kinds, and only one plays video.** The `files = [...]` array on an image block (§1)
  shows a different **still** each visit (images only — see the §1 warning). To rotate **clips**, use a
  **`block_pool`**: the engine emits `<<set _bp to random(0,N)>>` + an if/elseif chain and renders one child
  set per visit, and because children recurse through the normal block dispatch, a `video` child hits the
  real video handler (`v2.py:13664-13684`). **A branch renders exactly ONE block** (`[pool_item]`), and
  `video` carries no caption — so a pool rotates the *clip* while the beat's prose stays put. Two pools in
  one node do NOT stay in sync (both write `_bp`, rolled independently), so don't try to pair a clip pool
  with a text pool; if clip and prose must vary together, use N separate canvases instead. Constraints: a
  nested `block_pool` is silently stripped by the importer, depth caps at 4, and mixed child types log a
  warning. *(`block_pool` itself ships in three games with text children; a pool of **video** children is
  code-verified but not yet ship-proven.)* This is the mechanism behind the Lane-2 glimpse pool
  (`references/lanes.md`).

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

- Three real blocks: `image` `{file|files|url, alt, caption, description, search_queries}` · `video`
  `{file|url, description, search_queries}` · `clip` `{clipId}` (DB asset, owner-scoped, no file/queries).
  Unknown type = build-fatal.
- **The on-disk file decides `<img>` vs `<video>`** — your extension/`type` is advisory. Match all three.
- **Missing file = renders nothing** in a normal build (silent). Build `--debug` to see `[IMAGE MISSING]`
  placeholders + the Missing-Media page.
- **Every media block gets a `description` + 2 `search_queries`.** Queries: 3-5 words, **setting first**,
  physical vocabulary only, the gender-direction rule for solo-prone acts, no banned/emotional words.
- Locations use **`image_search_queries`**; content blocks use **`search_queries`**. Different key.
- SFW beats = `.jpg`; explicit beats = `.webm`. Quality contract, not an engine gate.
- Text before (specific) → media (mood, broad match) → text after (reaction). Don't describe what the media
  shows. Place at the action moment / mood peak.
- Step 5 names the media; Step 7 authors the block; **`find-media`** fetches it.
