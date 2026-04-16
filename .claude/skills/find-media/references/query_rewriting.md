# Query Rewriting

This file documents the deterministic rewrite rules that `scripts/validate_queries.py` encodes. The script runs BEFORE any search. Read this file when you need to understand why a query was rewritten, or when extending the rule set.

## Why rewrite queries

Search engines — PornHub especially — are keyword-biased and context-blind. A query like "passionate manual stimulation kitchen" returns mostly solo content and trending garbage. The narrative might describe "his hand between her thighs on the kitchen counter" which is `men fingering girl kitchen counter`. The rewrite gap is what produces bad matches.

The validator handles the deterministic rewrites (regex-level). Narrative-context rewrites (which direction is the hand going? what's the setting?) need the LLM with the narrative in context.

## Banned words (always strip)

These add noise to keyword search without improving relevance. PornHub ignores them. SFW sources often interpret them as style tags that mismatch the scene.

Emotional fillers:
- `passionate`, `tender`, `urgent`, `loving`, `intimate`, `sensual`, `seductive`, `emotional`, `forbidden`

Story fillers:
- `morning`, `evening`, `first time`, `secret`, `lazy` (unless the setting genuinely is morning — then OK)

Vague quality words:
- `beautiful`, `gorgeous`, `perfect`, `hot`, `amazing`

Rewrite: strip these words, keep the nouns and actions.

## Gender-direction required (anti-solo/lesbian trap)

Actions that can be performed solo or same-sex MUST include gender indicators. PornHub's category pages for these terms are dominated by solo/lesbian content.

| Ambiguous | Required rewrite |
|-----------|------------------|
| `fingering` | `men fingering girl <setting>` |
| `cunnilingus` / `eating out` | `guy eating out girl <setting>` |
| `touching` / `rubbing` | `man <action> woman <setting>` or `couple <action>` |
| `masturbation` | Never use for M/F — it's inherently solo |

Actions that DON'T need gender direction (already imply M/F):
- `blowjob`, `handjob` — implies M/F by convention
- `sex`, `fuck`, `missionary`, `doggy`, `riding` — implies couple

For quality filtering on these, add `couple` or `amateur` as a suffix.

## Direction disambiguation (who's doing what to whom)

The TOML may contain direction-ambiguous terms. The narrative paragraphs before/after the media block tell you which direction. The validator flags these for the LLM to resolve with narrative context:

| Ambiguous term | Clue in narrative | Rewrite |
|----------------|-------------------|---------|
| `oral` | "your mouth wraps around" | `blowjob` |
| `oral` | "his mouth finds you" | `cunnilingus` |
| `manual stimulation` / `manual` | "his hand between your" | `fingering` |
| `manual stimulation` / `manual` | "your hand wraps around him" | `handjob` |
| `hand job` (two words) | any | `handjob` (one word — PornHub tokenizes on spaces) |

The validator can't do this rewrite — it needs narrative context. It flags the query with `needs_direction_from_narrative` and the LLM fills it in during PLAN.

## Setting-first formula

PornHub weights the first keyword heavily. Setting is the hardest constraint to match (any blowjob looks similar; a kitchen must actually look like a kitchen). So:

- `kitchen+blowjob` — GOOD
- `blowjob+kitchen` — WORSE (weights blowjob over kitchen)
- `blowjob+amateur+kitchen` — WORST (setting relegated to tail)

Rewrite: move the setting to position 1 unless gender direction needs to come first (see rule above).

For gender-ambiguous actions, the pattern becomes: `<gender1> <action> <gender2> <setting>` — the gender direction takes precedence over setting-first because solo-trap results are worse than setting-mismatch results.

## Tier-appropriate vocabulary

Queries MUST match the tier. A t2 (SFW) query with sexual terms will pull NSFW results from safe-search-optional sources. A t5 (NSFW) query with sanitized terms will pull SFW noise.

| Tier | Allowed vocabulary | Example good | Example bad |
|------|-------------------|--------------|-------------|
| base, t2, t3 | domestic, lifestyle, emotion-light | `couple morning coffee kitchen` | `sexual tension dinner` (t3 with sexual term) |
| t4 | suggestive, partial undress, kissing | `couple kissing bedroom` | `kitchen blowjob` (too explicit) |
| t5, t6 | explicit acts, positions, settings | `kitchen counter sex couple` | `romantic love bedroom` (too vanilla) |
| t7, t8 | graphic, specific acts | `doggy counter amateur` | any vague emotional term |

The validator checks query-tier alignment. A t2 query with `sex`/`fuck`/`blowjob` → flagged. A t5 query with only `romantic`/`intimate` → flagged.

## Action vocabulary (canonical forms)

Use these exact terms. Variants produce worse results:

- `fingering` — his hand on/in her (NOT `manual stimulation`, `manual`, `hand job`)
- `handjob` — her hand on him (one word — NOT `hand job`)
- `blowjob` — her mouth on him
- `cunnilingus` — his mouth on her (or `eating out`)
- `sex` / `fuck` — penetration (always add position: `missionary`, `doggy`, `riding`, `standing`, `bent over`)

## Synthesizing queries when `search_queries` is empty

Phone posts frequently arrive from the API with `search_queries = []`. Locations, clothing items, and dating profile photos can too. The skill synthesizes 2–3 queries from the entry's `description` + `type` + `category` before validation runs.

This is LLM judgment, not templates. Descriptions carry enough cue to write grounded queries; hardcoded templates would drift as new TOML shapes appear. Show the model these worked examples and let it write queries for new items.

### Worked examples per type

**1. `social_post_image`** — description is `"@poster_name: caption"`:

- desc `"@jessicafit_: 5am grind. no days off. #legday"`
  - Parse: hashtag `#legday` → leg workout; `@jessicafit_` → fit persona; `5am grind` → morning
  - Queries: `"fit woman gym leg workout selfie"`, `"woman morning gym mirror selfie athletic"`, `"legday workout selfie fitness"`
  - Tier: SFW (social posts are lifestyle-tier unless the caption explicitly escalates)

- desc `"@mia.xo: golden hour hits different"`
  - Parse: `golden hour` → sunset; `.xo` → playful; no activity hashtag
  - Queries: `"woman golden hour sunset selfie"`, `"beach sunset girl selfie lifestyle"`, `"sunset silhouette selfie attractive woman"`
  - Tier: SFW

**2. `location_image`** — description is `"Navigation image for {name}"`:

- desc `"Navigation image for The Harmon Property"`
  - Parse: location name, navigation → wide establishing shot, no people
  - Queries: `"rural property house workshop wide angle"`, `"American farmhouse property exterior establishing"`, `"country property gravel driveway wide shot empty"`
  - Tier: **always SFW** (all location images are SFW regardless of game state)

- desc `"Navigation image for Jake's Bedroom"`
  - Parse: interior room, no people, masculine
  - Queries: `"young man bedroom interior wide angle"`, `"college student bedroom messy artistic"`, `"young adult bedroom with sketches posters"`
  - Tier: **always SFW**

**3. `clothing_image`** — description is `"{name} ({slot})"`:

- desc `"Hoodie (top)"`
  - Parse: item = hoodie, slot = top → flat-lay product photography, no person
  - Queries: `"gray hoodie flat lay product photo white background"`, `"women hoodie casual product shot"`, `"simple hoodie top clothing product photo"`
  - Tier: **always SFW** (wardrobe UI)

- desc `"Athletic Leggings (bottom)"`
  - Parse: item = leggings, athletic style, bottom slot
  - Queries: `"black athletic leggings product photo flat lay"`, `"women workout leggings product shot"`, `"athletic leggings bottom clothing catalog"`
  - Tier: **always SFW**

**4. `dating_profile_photo`** — description is `"Dating profile photo for {npc}"` + look up NPC in the API response's `npcs` array for age/traits:

- desc `"Dating profile photo for Jake"`, NPC lookup: Jake, 22, athletic, artist
  - Parse: young male, athletic build, creative
  - Queries: `"dating app profile selfie 20s man athletic"`, `"artist man mirror selfie casual dating"`, `"young man outdoor casual selfie dating profile"`
  - Tier: SFW

**5. `image` / `video` (canvas)** — already carries queries from `props.search_queries`:

No synthesis needed. The TOML author wrote the queries directly on the canvas block. If these ever arrive empty (unusual), read the 2–3 narrative paragraphs before/after the block in the TOML and synthesize from those cues — same rules as the canonical §Setting-first formula.

### Synthesis hard constraints

- `location_image` and `clothing_image` are **always SFW**, no exceptions — they render in UI chrome, not in scenes
- Synthesized queries must still pass `validate_queries.py` checks (banned-word strip, tier alignment, format family) — feed synthesis output back through the validator, same pipeline as author-written queries
- If synthesis yields a query that would trigger a tier mismatch (e.g., accidentally sexual language on a `clothing_image` entry), the validator flags it and the LLM rewrites

### The synthesis step in the pipeline

1. Fetch API → get `missing_media` array
2. For each entry with `search_queries = []`, synthesize 2–3 queries using these examples as guidance
3. Write synthesized queries back into the entry's `search_queries` field
4. Save the augmented list to `games/<game>/.find-media/game_review.json`
5. Run `validate_queries.py --from-api-json <path>` — validator runs unchanged rules

The validator doesn't distinguish between author-written and synthesized queries. All queries face the same banned-word/tier/format checks.

## The validation report

Output format when the validator flags queries:

```
=== Query Validation Report ===
Checked {N} items.

⚠️ FLAGGED ({N} items need narrative-context rewrite):

| # | file | tier | current query | issue | proposed |
|---|------|------|---------------|-------|----------|
| 1 | breakfast_ethan_t6 | t6 | "manual stimulation kitchen" | needs_direction_from_narrative + solo_trap | (resolve with narrative; probable: "men fingering girl kitchen counter") |
| 2 | scene_taste2 | t5 | "blowjob couch night" | banned_word:night, needs_direction_check | "couch blowjob amateur" if she→him; else fix |

✅ AUTO-REWRITTEN ({N} items):

| # | file | original | rewritten | rules applied |
|---|------|----------|-----------|---------------|
| 3 | breakfast_base | "passionate morning coffee" | "couple morning coffee kitchen" | stripped:passionate, added:couple+kitchen |

✅ OK ({N} items — no changes needed)
```

The LLM reads this report, resolves the FLAGGED items using narrative context (reads the TOML), and produces the final ranked query list for RETRIEVE.
