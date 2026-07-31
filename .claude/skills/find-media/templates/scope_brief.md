# Scope Brief — `{{item_id}}`

Fill this template during SCOPE — the first phase of SCOPE → PLAN → SEARCH → STOCK → JUDGE →
INSTALL. Write to `games/{{game}}/.find-media/scope/{{item_id}}.md`.

Sources: the API response cached at `games/{{game}}/.find-media/game_review.json` (see
`references/game_review_api.md`) for the item list, plus the game's merged TOML for canvas
narrative — `games/{{game}}/toml_phases/*_final_game.toml` (`7_final_game.toml` in current
games, `6_final_game.toml` in older ones like `under_one_roof` and `two_weeks`).

**This brief is the only thing the search and the frame-strip check get to read.** Whatever
you leave out here you re-derive badly two hours later, in front of 40 thumbnails, from
memory. §Demand is the part that carries: it feeds the heat axis in
`references/scoring_rubric.md` and it becomes the literal checklist you hold against the
frame strip.

## Identity

- **item_id**: `{{item_id}}` (derived from `file` field, filesystem-safe)
- **file_path**: `{{file}}` (verbatim — this is the key for the options store, the review
  store, and dedupe; every API call uses it unchanged)
- **type**: `{{type}}` — one of `image`, `video`, `location_image`, `clothing_image`,
  `social_post_image`, `dating_profile_photo`, `portrait_image`
- **category**: `{{category}}` — one of `Activities`, `Story`, `Locations`, `Clothing`,
  `Social Media`, `Portraits`, `Other`
- **canvas_id**: `{{canvas_id}}`
- **order**: `{{order}}`
- **tier**: `{{tier}}` (canvas items: infer from the filename `_tN` suffix; location /
  clothing / social_post / dating_profile: always `base`)
- **content_rating**: `{{sfw|nsfw}}` (non-canvas types: always `sfw`)
- **required_format**: from `scripts/tier_format_check.py` rules — but note the download API
  decides the saved extension from the SOURCE URL, not from the TOML, so this is what you
  *want*, not what you will necessarily get. Verify after install.
- **discovered_by**: `{{game_review|toml_walker}}` — record which list found this item, so a
  future coverage gap in the API shows up as a walker-only item instead of hiding. (The
  portrait classes were exactly such a gap until 2026-07-27; the API enumerates them now.)
  Walker regex: `(?:file|image|video|nav_image)\s*=\s*"([^"]+)"`.
- **scene_id for capture**: `{{scene_id}}` — the directory part of `file_path`, relative to
  `videos/`. `scenes/kiss`, never `videos/scenes/kiss`, never `output/videos/scenes/kiss`
  (the API strips `videos/` but not `output/`, and the file lands nested wrongly).

## Narrative context — branches by type

Fill ONE of the following subsections based on `{{type}}`.

### If `type` is `image` or `video` (canvas block)

Find the canvas block by matching `file = "{{file}}"` inside the canvas with id
`{{canvas_id}}` in the merged TOML. Extract the 2–3 narrative paragraphs / dialog blocks
that appear BEFORE and AFTER this block in the same node.

**Before:**
> {{before_paragraph_1}}
>
> {{before_paragraph_2}}

**After:**
> {{after_paragraph_1}}
>
> {{after_paragraph_2}}

### If `type` is `social_post_image`

Description shape: `"@poster_name: caption"`.

- **Poster**: `{{poster_name}}` (the `@handle` from description)
- **Caption**: `{{caption}}` (everything after the first `:`)
- **Hashtags** (extracted from caption): `{{hashtags}}`
- **Content cues** (nouns/verbs from the caption that ground the scene): `{{cues}}`

### If `type` is `location_image`

Description shape: `"Navigation image for {location_name}"`.

- **Location name**: `{{location_name}}`
- **Location TOML metadata** (find the `[[locations]]` entry whose `image` field matches):
  indoor/outdoor, type, tone

### If `type` is `clothing_image`

Description shape: `"{item_name} ({slot})"`.

- **Item name**: `{{item_name}}`
- **Slot**: `{{slot}}` (one of top/bottom/dress/shoes/etc)
- **Style inference** (from name): casual / formal / athletic / underwear / etc

### If `type` is `dating_profile_photo`

Description shape: `"Dating profile photo for {npc_name or id}"`.

- **NPC**: `{{npc_name_or_id}}`
- **NPC lookup** — find the NPC in `game_review.json` → `npcs` by id or name. Extract:
  - **age**: `{{npc_age}}`
  - **traits**: `{{npc_traits}}` (physical build, profession, hobbies)

## Demand — what this slot has to deliver

The three fields the rubric cannot reconstruct later. Write them from the beat prose, not
from the filename.

Note what is **not** here: a list of things the clip must contain. The gates are owned by
`references/scoring_rubric.md` (§Gate 1 CAST, §Gate 3 BEAT) and their inputs are the closed list in
§Gate inputs below. This section carries only the three judgement calls the rubric genuinely cannot
make on its own.

### setting_is_load_bearing: `{{true|false}}`

> Why: {{one line}}

The test: **does the setting carry danger, secrecy, or squalor?** If it does, it is part of
the meaning and both the query and the score spend on it — a dark alley beat died twice on
bright clips because the darkness *was* the danger. If it does not, the setting is
disposable: the query must not spend words on it (words spent on setting are words stolen
from act and heat), and the setting axis in `references/scoring_rubric.md` is **skipped and
recorded as `null`** — one answer only, never "scored low". Measured precedent: on one
blowjob beat the user said the setting "doesn't matter much here" and picked on the eyes.

### intended_heat: `{{one or two clauses}}`

What makes this beat land — the thing that, if missing, makes a spec-perfect clip dead.
Name the carrier, not the act. Known carriers, in the order they have actually won:

| Carrier | Reads on screen as |
|---|---|
| Eye contact | She holds the camera for the whole loop, not one frame |
| Being used | Passive body, someone else setting the pace |
| Power | Who is standing, who is kneeling, who is holding the head |
| Squalor / grime | The room is wrong for this and it is happening anyway |
| Exposure / risk | Public, half-dressed, someone could walk in |

The user's winning pick over the assistant's was chosen explicitly because "the eyes made
it win" — it beat a spec-correct alternative that was correct and dead. That is what this
field exists to protect.

### pov_case: `{{defect|fine|either}}`

> Why: {{one line}}

**POV is two cases, not one rule** — so decide it here, in advance, rather than at judging time
when forty thumbnails are in front of you and the argument goes whichever way you're leaning.

- **`defect`** — the scene's meaning needs the partner's body seen. A slack, limp, passed-out,
  watching or restrained man **cannot also be the camera**: if he is the camera, the thing the
  beat depicts is off-screen. Counting a crew you can't see fails the same way.
- **`fine`** — the clip's power is her face and her eyes aimed at the viewer. POV puts the camera
  where the player is, so eye contact into the lens is eye contact with the player. This is the
  strongest heat signal we have confirmed, and the one clip the user picked over a spec-perfect
  alternative was POV.

Full treatment in `references/scoring_rubric.md` §Gate 3. When POV is not a Gate-3 failure it
must not be penalised on any axis.

### strip checklist (derived)

Do **not** invent a checklist here. It is `references/scoring_rubric.md` §Gate 3 — act, position,
count, affect, extra people, finish — filled in from **§Gate inputs** (the next section down), plus
your `pov_case` call. Copy those in as a numbered list so the check is concrete when you're holding
it against an image. Fill §Gate inputs first, then come back and copy.

> **Why the checklist is a fixed list and not a free-form one.** It used to be free-form
> (`must_show` / `avoid`), pulled "straight from the beat prose" — and beat prose says things like
> *"in a dim red-lit room"*. Rooms went into the checklist, which the rubric explicitly forbids
> (`scoring_rubric.md` — *"`wrong_setting` is not a valid `gate_reason`"*). Observed on `vesper`:
> one slot's list required *"kneeling on a **hard floor** — concrete / bare / tile, not carpet"*,
> another required *"a dim indoor office / records setting"*. Neither room existed in the corpus, so
> both slots burned 6 query rounds hunting one.
> **What it did NOT do, so don't overstate it:** those gates mostly never fired — the recorded kills
> are bodies, and every slot still filled. The damage was an unsatisfiable demand and wasted rounds,
> not good clips binned. A closed list has nowhere for a room to hide in the first place.

**Every animated finalist (`.webm` / `.mp4` / `.gif`) is strip-verified; a static finalist (a
location or clothing `.jpg`, which cannot be stripped) is judged from the contact sheet.** The
strip is route-independent and it kills roughly half of what looked good: 3 of 5 in one round this
session, 4 of 6 in the next. Kills included a "perfect cluttered back room" thumbnail whose loop
was standing kissing with no blowjob at all, and a "dark outdoor" thumbnail whose loop was a bright
daytime laundromat. Eye contact in particular must HOLD ACROSS THE WHOLE STRIP — two candidates
died on wandering eyes their thumbnails hid.

1. {{check}}
2. {{check}}

## Gate inputs — and the query's raw material

This section does two jobs: it is what the queries are built from, **and** it is what
`references/scoring_rubric.md` §Gate 3 checks a candidate against. Same facts, both uses.

**The list is closed on purpose.** Every field below is a fact about *bodies* — who is there, what
they are doing, who is standing or kneeling, where the hands and eyes are. There is no free-form
slot, because the free-form version is what let rooms become gates. `setting` appears here as a
**query input only** and is marked as such: it can lose points on the SETTING axis, it can never
reject a candidate.

Fill by type:

- **canvas (image/video)**: act, position, people count (1|2|3+), direction if ambiguous,
  affect, setting *only if load-bearing — and for the QUERY only, never a gate*
- **social_post_image**: poster persona (e.g. `fit woman`, `travel influencer`), scene
  subject (activity implied by hashtags/caption), setting if implied, selfie-style required
- **location_image**: wide-angle vs interior, empty (no people), time of day if implied
- **clothing_image**: flat-lay product photo (no person), style tag, colour (from name if
  declared)
- **dating_profile_photo**: selfie or candid, age range, gender, key trait hint

## Queries — one slot per source

Not a single ranked ladder. The dialects are **opposite**, so a query written for one source
is wrong on the other and ranking them against each other is meaningless.

### Google (Chrome) — primary route

- **google_query**: `{{query}}`
- **variant_2**: `{{query}}`
- **variant_3**: `{{query}}`

**Shape:** `<act> <her posture> <HIS posture — only when it is not the act's default> [setting-if-load-bearing] [anti-studio modifier] gif`

Rules that produced these — this list must stay in sync with `references/chrome_route.md` §3 and
`references/query_rewriting.md` Part 2:

- Verbose is fine. Natural language is fine. Loose grammar is fine — `on kneel blowjob`
  worked.
- **Append `gif` or `webm`. NOT optional — the highest-leverage token in the query.** Measured
  3×, same query ± that one token: **7→59, 1→54, 0→91** fetchable urls.
- **Name HIS posture when it is not the act's default.** `kneeling blowjob` retrieves
  she-kneels-he-**STANDS**; if the beat needs him seated or reclining, say `office chair`,
  `under the desk`, `sitting in chair`. Measured: the slot that named it got **13 of 43**
  seated-slugged results; the sibling slot that named only wardrobe and framing got **0 of 10**,
  and `him_standing` was its dominant rejection across three runs. A wrong partner posture is a
  legitimate gate failure, so this buys you an empty shelf, not a bad pick.
- **Strip story and character words.** Measured: `back alley blowjob gif drunk guy night`
  returned Reddit movie stills, Facebook, and TikTok — "drunk guy" reclassified the whole
  query as mainstream. Character words don't dilute here, they *change the intent class*.
- Add an anti-studio modifier when the beat is grimy: `amateur`, `real`, `voyeur`,
  `hidden cam`. This is the fix for the most-repeated defect in this game's history —
  bright studio porn arriving for a beat that wanted dirt.
- Only name the setting if `setting_is_load_bearing` is true — **and cap it at ~2 setting
  tokens.** Stacking place + time + light (`alley` + `at night` + `streetlight`) reclassifies the
  query as stock photography and returns Shutterstock. Name the place once and stop.
- **Log every query to `games/<game>/.find-media/query_ledger.jsonl`** — the only machine-written
  record of what was searched. Prose summaries of a run have already been caught contradicting it.
  ⚠️ **`urls_yielded` is NOT a quality signal:** 31 queries on `vesper` returned 40–92 urls with no
  relationship to whether the query worked. Record the number; never tune on it.

### PornHub tag — vocabulary only, never a download

- **bare_word**: `{{rare_word}}` → **pool size**: `{{n}}` results
- **pornhub_query**: `{{query}}` (≤3 tokens)
- **tags harvested**: `{{tags}}`

**A PornHub-hosted result is read for its title and its tags and then dropped.** It is never
queued as a candidate: `egl.phncdn.com/gif/<id>.gif` returns 470 on clearnet *and* over Tor,
and the real media URL is signed, time-limited and IP-locked — a signature our extraction
destroys by construction, because it strips query strings. Full measurement in
`references/media_sources.md` §"PornHub is discovery-only". So fill this section to learn the
word, then go spend the word on Google.

PornHub's search silently drops rare words from compound queries and returns literally 0
results for 4+ tokens. Measured: `stockroom` alone = 5 gifs; `stockroom blowjob` = 37, and
those 37 are generic blowjob — the rare word was dropped and the count went UP. **Always
count the bare word's pool before trusting a compound query**, and record the number above,
because a 5-result pool means the word is thin and the tag route is not worth a second query.

### Term discovery

Skip only if the beat is plain vanilla. This step is why `downblouse` was never found: the
skill had no term-discovery step at all.

- **candidate terms**: `{{terms}}`
- **where from**: `{{source}}`

Where terms actually come from, ranked by what worked:

1. **Google's own result labels and URLs** — the richest mine. They taught `dogging` and
   `back alley` this session, unprompted. Read the labels, not just the pictures.
2. **Grok / an LLM, for modifiers and community names only.** Its headline "best search
   terms" are near-useless — it paraphrases your sentence into 4–5 token phrases, which
   return 0 on PornHub. Verify any community it names before trusting it: `r/OutdoorBlowjobs`
   is real but nearly dead (2.2k weekly visitors, 4 posts/week).
3. **Not WebSearch.** Sanitised, returns encyclopedia and spam. Reddit's anonymous JSON API
   is blocked. Both were tried this session; both failed.

## Rejection criteria (auto-populated from type + tier)

These are the hard gates that run before scoring. `avoid` above is per-beat; this is
per-type and always applies.

### SFW types (location_image, clothing_image, social_post_image default, dating_profile_photo)

- Reject 3+ people on activity canvases (canvas items only)
- Reject commercial/restaurant when the narrative says home (canvas only)
- **location_image**: reject lifestyle shots with people dominating the frame — the point is
  the space
- **clothing_image**: reject fashion editorial with a model — the point is the item
- **social_post_image**: reject group shots, and anything that doesn't match the caption's
  persona
- **dating_profile_photo**: reject professional studio portraits — dating profiles are
  candid selfies and casual shots

### NSFW types (canvas image/video at t4+)

Full gate list in `references/scoring_rubric.md` §Gate 1 — CAST and §Gate 3 — the BEAT. **Those two
sections are the complete set** — this brief contributes the *inputs* to Gate 3 (§Gate inputs) and
the `pov_case` call, never additional gates of its own. Every gate is binary: a failure ends the
candidate and is recorded with a named reason. None of them is worth points.

A gate that is not on that list does not exist. In particular the room, the lighting and the
furniture are **scored on the SETTING axis, never gated** — `wrong_setting` is not a legal
`gate_reason` (`scoring_rubric.md:332`).

## Mode — how deep to stock the shelf

Mode is an **option count**, not a retry budget. Every slot ships one installed best-guess
pick plus a stocked shelf in the options store for the human to flip through; the mode only
sets how tall the shelf is.

| Mode | Options to stock | When |
|---|---|---|
| `fill` | 6 | SFW static slots — location, clothing, social post, dating profile. Low variance, cheap to eyeball, 6 is plenty. |
| `wide` | 12 | Any NSFW canvas slot. The strip kills ~half, so a 6-deep shelf can arrive as 2 survivors. Stock 12 to land 6. |
| `deep` | 18 | Capstones, hero assets reused across canvases, and any refetch after the human disapproved the installed pick — the first shelf already proved wrong. |

Selected mode for this item: `{{mode}}`
Option target: `{{n}}`

Mode sets shelf depth only. How many of that shelf get strip-verified is **one number for
every mode** — the top 6 by contact-sheet rank (`references/scoring_rubric.md` §Gate 2). The
rest stay stocked and unproven, which is honest and useful; they are alternates, not installs.

**A refetch rebuilds the shelf — stock first, prune after.** Never clear on the way in;
wiping first once silently ate three harvests. The order is:

1. `t0 = now()` in ISO-8601, recorded before you stock anything.
2. Stock the new candidates with `options/add`, exactly as on a first run.
3. `POST /api/v1/dev/media-finder/options/clear {game, file, before: t0}` — `before` drops
   only entries added before that instant, so the fresh set survives, and entries carrying
   `origin: "previous"` (the slot's undo history) survive regardless.

Do not walk `options/list` and `options/remove` each stale URL: that deletes the undo history
too, and it destroys the pool before its replacement exists.

## Resume marker

Write these as the last lines of the brief file:

```
PHASE: scope_complete
NEXT_PHASE: plan
OPTIONS_STOCKED: 0
INSTALLED: no
```

On resume, the skill reads this to decide whether to redo SCOPE or skip ahead.
`OPTIONS_STOCKED` is the real progress signal — an item with an installed pick but 0 stocked
options is not done, because the human has nothing to choose from.
