# Query Rewriting

Two things live in this file and they are NOT the same thing:

- **Part 1 — route-neutral semantics.** Rules about MEANING: which direction the act
  goes, whether the pool is secretly solo, which word names the act. These are true
  no matter what you type them into, because they are about what you are asking for.
- **Part 2 — per-source dialect.** Rules about ENGINES: how many tokens survive, what
  reclassifies your intent, which modifiers steer. These are source-specific, and Google's
  rules and PornHub's contradict each other, hard.

Keep them separate. Collapse them — state PornHub tokenizer behaviour as universal search
law — and the rules come out wrong or actively harmful on Google: a query PornHub returns
0 results for works fine on Google, and a query PornHub merely wastes tokens on can
reclassify your whole Google search as mainstream.

**Enforcement legend.** `[ENFORCED]` = implemented in `scripts/validate_queries.py`, runs
before SEARCH, deterministic. `[ADVISORY]` = your judgment, nothing checks it. Never
promote advisory prose into "the validator does X": `morning`, `evening`, `hot` and
`night` are stripped by nothing in this skill, and a rule set that claims otherwise has
drifted off the code and stopped being trustworthy.

---

# Part 1 — Route-neutral semantics

## What the script actually strips `[ENFORCED — and it depends on --target]`

Stripping is the one **target-dependent** half of the validator, so read this section with
Part 2 open. `validate_query()` picks the list from `--target`: the default `google` — the
route we actually search — runs `strip_story_words()`; `--target pornhub` runs
`strip_banned()`. Nothing else is removed, in either mode.

| Target | Function | Members |
|---|---|---|
| `google` (default) | `strip_story_words()` | `drunk` `wasted` `tipsy` `hungover` `angry` `nervous` `scared` `crying` `sad` `shy` `embarrassed` `reluctant` `unwilling` `hesitant` `exhausted` `tired` + phrases `passed out`, `first time` |
| `pornhub` | `strip_banned()` | `passionate` `tender` `urgent` `loving` `intimate` `sensual` `seductive` `emotional` `forbidden` `beautiful` `gorgeous` `perfect` `amazing` + phrases `first time`, `secret`, `lazy` |

The two lists strip for opposite reasons and share exactly one member (`first time`).
Google's list is character-STATE words, which flip its intent classifier — Part 2 has the
measurement. PornHub's is flowery adjectives that match no tag. Running the wrong list is
not fatal; it just throws away tokens that were doing no harm and keeps the ones that were.

Both are matched **word-bounded** — single tokens whole and punctuation-insensitive,
phrases wrapped in `\b…\b` (`_strip_words()` in `validate_queries.py`). An earlier version
did a raw substring replace, which ate the middle of `secretary` and shipped `ary hand on
man crotch`; that is fixed in the code (the code comment sits right on top of the fix). A
query that comes back with a word chewed through the middle is a bug report, not expected
behaviour.

**NOT stripped by either list:** `morning`, `evening`, `night`, `hot`. Do not add them.
`morning`/`evening`/`night` are real visual facts (light level, which the setting axis cares
about). `hot` is load-bearing vocabulary on the heat axis — stripping it would fight the
rubric (`references/scoring_rubric.md`).

## Direction disambiguation `[ENFORCED as a flag — you resolve it]`

Direction-ambiguous terms cannot be regexed into the right act; the narrative paragraphs
before and after the media block are the only evidence for which way the act is going.
The validator detects them and stops, setting `needs_direction_from_narrative`.

| Ambiguous term | Clue in narrative | Rewrite |
|----------------|-------------------|---------|
| `oral` | "your mouth wraps around" | `blowjob` |
| `oral` | "his mouth finds you" | `cunnilingus` |
| `manual stimulation` / `manual` | "his hand between your" | `fingering` |
| `manual stimulation` / `manual` | "your hand wraps around him" | `handjob` |
| `hand job` (two words) | any | `handjob` — auto-rewritten, one word `[ENFORCED]` |

`oral`, `manual`, `manual stimulation` flag; `hand job` → `handjob` is the one member of
`AUTO_REWRITES` that resolves without you. Resolve the flags during PLAN, from the TOML.

## The solo / same-sex trap `[ENFORCED]`

Actions a person can perform alone, or with a same-sex partner, return exactly that pool
unless you name the direction. `check_gender_direction()` substitutes in place:

| Trigger | Becomes | Note |
|---|---|---|
| `fingering` | `men fingering girl` | substituted where it sits in the query |
| `cunnilingus` | `guy eating out girl` | |
| `eating out` | `guy eating out girl` | |
| `masturbation` | — | returns `None`, query marked `unusable_query` — it is inherently solo, there is no M/F rewrite |

Actions that already imply M/F and need no direction: `blowjob`, `handjob` (convention),
`sex`, `fuck`, `missionary`, `doggy`, `riding` (imply a couple).

**Caveat, stated honestly:** this trap was measured on PornHub's category pages, whose
`fingering`/`cunnilingus` pools are solo- and lesbian-dominated. It has NOT been
re-measured on Google image results, where the index is a different shape. Treat the
rewrite as cheap insurance rather than proven necessity, and if a Google run for a
directed query comes back thin, try the bare term once and look — that is a one-query
experiment, not a rule change.

## Canonical action vocabulary `[ADVISORY]`

Use these exact forms; variants split the pool across synonyms.

- `fingering` — his hand on/in her (NOT `manual stimulation`, `manual`)
- `handjob` — her hand on him (one word, NOT `hand job`)
- `blowjob` — her mouth on him
- `cunnilingus` / `eating out` — his mouth on her
- `sex` / `fuck` — penetration; always pair with a position (`missionary`, `doggy`,
  `riding`, `standing`, `bent over`) because position is a documented rejection class.

### ⚠️ And the reciprocal: a POSITION without an ACT is not a query `[ENFORCED]`

The rule above is stated one way — pair the act with a position. The failure that actually
happened is the inverse: **the position was there and the act was missing.**

`riding`, `cowgirl`, `missionary` and `doggy` are ordinary English — a horse, a ranch, a religion,
a dog. They carry no sexual meaning to a general search engine, so a query anchored only on one of
them does not return bad porn; **it returns no porn at all.**

**Measured 2026-08-01, same query minus one token:**

| query | urls | on a porn host |
|---|---|---|
| `riding cowgirl man in office chair gif` | 83 | **0** — Tenor, BBC, Wikipedia, Billboard, NFL, Warhol |
| `cowgirl riding fuck office chair gif` | 73 | **69 (95%)** |

**Why this hid for so long:** `blowjob` is an act word and anchors a query by itself, so every oral
slot worked and nothing exposed the gap. It only appears on a penetrative beat.

`scripts/validate_queries.py` now flags an NSFW query (`t5`–`t8`) carrying no member of
`ACT_ANCHORS` as `no_act_anchor:position_or_setting_words_only`. `t4` is exempt — a tease beat must
never be forced to carry a penetrative word.

**Membership rule for `ACT_ANCHORS`** (`scripts/scene_semantics.py`): a word qualifies only if it has
no common non-sexual reading. `cum` and `cumshot` are in. `facial` (a spa treatment), `swallow` (a
bird), `load` (freight) and `finish` (a verb) are **out**, which is why `escort facial mouth red
room` still flags — correctly.

⚠️ Note the deliberate split between two sets that look interchangeable and are not.
`SEXUAL_TERMS_FOR_SFW_CHECK` **keeps** `cowgirl`/`missionary`/`doggy`, because it answers *"is a
sexual word leaking into an SFW query?"* — and for that job they belong. `ACT_ANCHORS` excludes them
because it answers *"will this query reach porn at all?"* Conflating the two is what let the broken
query through: `cowgirl` made `has_sexual` true and the validator passed a query that returned zero
usable results.

### Every act phrase has a DEFAULT PARTNER POSTURE — name his only when you need to override it

Position is not one token. It is **two bodies**, and the act phrase silently fixes the second one.
Ask for the act plus her posture and you get the corpus's canonical composition for that pair; if
your beat needs a different partner posture, the query has to say so or the default wins.

| act phrase | what it retrieves by default | say this to override |
|---|---|---|
| `kneeling blowjob` | she kneels, **he STANDS** | `office chair`, `under the desk`, `sitting in chair`, `seated`, `on the couch` |
| `blowjob` (bare) | unconstrained — expect both, in unknown proportion | name the posture you want |
| `sex` / `fuck` | nothing — genuinely ambiguous | always pair with a position; this act was already right |

**Measured** (`vesper`, 2026-07-31): a slot whose queries named his posture returned **13 of 43**
seated-slugged results; a sibling slot needing the same posture, whose queries named only wardrobe
and framing, returned **0 of 10** — and `him_standing` was its dominant rejection across three
separate runs (11 of 15, then 12 of 26 and 15 of 19). Full table in `chrome_route.md` §3.

Two things this does **not** claim. It has not been tested whether adding the token would have
rescued that slot — the omission is what is measured, not the remedy. And the ratio is a slug count,
not a frame check: a slug saying `chair` is a term-mine hint, never a correctness claim
(`scripts/fetch_candidates.py` `rank()`), so the strip still decides.

**The old worked example here pointed the wrong way.** It read *"standing when the beat says
kneeling gets thrown back"* — which assumes **her** posture is the variable. Every failure actually
recorded in this repo is the opposite: her posture was right and **his** was wrong.

## Tier-appropriate vocabulary `[PARTLY ENFORCED]`

Vocabulary must match the tier or you search the wrong half of the internet: a t2 query
carrying sexual terms pulls porn into a UI slot; a t5 query written in vanilla-romance
words pulls stock couples into a sex beat.

| Tier | Allowed vocabulary | Good | Bad |
|------|-------------------|--------------|-------------|
| base, t2, t3 | domestic, lifestyle, emotion-light | `couple morning coffee kitchen` | `sexual tension dinner` |
| t4 | suggestive, partial undress, kissing | `couple kissing bedroom` | `kitchen blowjob` (too explicit) |
| t5, t6 | explicit acts, positions, settings | `kitchen counter sex couple` | `romantic love bedroom` (too vanilla) |
| t7, t8 | graphic, specific acts | `doggy counter amateur` | any vague emotional term |

What `check_tier_alignment()` actually enforces, and only this:

- tier ∈ {`base`,`t2`,`t3`,`location`} + any `SEXUAL_TERMS_FOR_SFW_CHECK` hit →
  `tier_mismatch:sfw_query_has_sexual_term`.
- tier ∈ {`t5`…`t8`} + a `VANILLA_TERMS_FOR_NSFW_CHECK` hit (`romantic` `sweet` `tender`
  `loving` `gentle` `intimate` `passionate` `sensual`) → one of two issues, split by
  whether the query carries an act word (`SEXUAL_TERMS_FOR_SFW_CHECK` ∪ `ACT_ANCHORS` —
  both lists, because `cumshot`/`bj`/`anal` live only in the second):
  - no act word → `tier_mismatch:nsfw_query_too_vanilla`.
  - act word present → `vanilla_dilution:mood_words_pull_stock_results`. Added 2026-08-05
    after `media_lab_f`: the old check was suppressed by any act presence, so `passionate
    real couple cumshot gif` validated clean and shelved a 17%-on-act romance pile (45
    Dreamstime stills; the act-first control ran 50%). A mood word is never saved by the
    act word beside it — Google weights every token and the mood words have the bigger
    SFW cluster.

Three blind spots to hold in your head, because the report will not mention them:

1. **t4 is checked by neither rule** — it is in `BORDERLINE_TIERS`, which appears in
   neither branch. The whole clothed→explicit span passes tier check silently.
2. **t0 and t1 are checked by neither rule either.** `infer_tier_tagged` returns them
   happily, but `scene_semantics.SFW_TIERS` is `{base, t2, t3, location}` — t0/t1 sit in no
   tier set, so a t0 slot carrying `blowjob` passes silently. (`tier_format_check.py` does
   know t0/t1 at the pre-install gate; the query validator does not.)
3. **On `--target pornhub`, the vanilla checks can only ever fire on `romantic`, `sweet`
   or `gentle`** — `strip_banned()` runs first inside `validate_query()` and
   `tender`/`loving`/`intimate`/`passionate`/`sensual` are banned words, so they are gone
   before `check_tier_alignment()` sees the string. On the default Google target nothing
   strips them, so all eight vanilla terms stay live.

Tier itself comes from the FILENAME (`infer_tier_tagged`: `_t0`…`_t8`, or `_base`,
else base-and-untagged). A wrong or missing suffix is a content-rating problem, not a
query problem — see `references/content_rating.md`.

## Synthesizing queries when `search_queries` is empty

Phone posts frequently arrive from the API with `search_queries = []`. Locations,
clothing items, and dating profile photos can too. Synthesize 2–3 queries from the
entry's `description` + `type` + `category` before validation runs.

This is judgment, not templates. Descriptions carry enough cue to write grounded queries;
hardcoded templates would drift as new TOML shapes appear. Work from these examples.

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

**4. `dating_profile_photo`** — description is `"Dating profile photo for {npc}"` + look up the NPC in the API response's `npcs` array for age/traits:

- desc `"Dating profile photo for Jake"`, NPC lookup: Jake, 22, athletic, artist
  - Parse: young male, athletic build, creative
  - Queries: `"dating app profile selfie 20s man athletic"`, `"artist man mirror selfie casual dating"`, `"young man outdoor casual selfie dating profile"`
  - Tier: SFW

**5. `image` / `video` (canvas)** — already carries queries from `props.search_queries`:

No synthesis needed; the TOML author wrote them on the block. If they do arrive empty
(unusual), read the 2–3 narrative paragraphs before and after the block and synthesize
from those cues — name the act, the position, the count of bodies, and the setting only
if the setting carries meaning.

### Synthesis hard constraints

- `location_image` and `clothing_image` are **always SFW**, no exceptions — they render
  in UI chrome, not in scenes, and an adult result there is a bug in the wardrobe screen.
- Synthesized queries face the same checks as author-written ones — feed them back
  through `validate_queries.py`; the validator does not know or care which is which.
- If synthesis yields language that trips tier alignment (accidentally sexual phrasing on
  a `clothing_image`), the validator flags it and you rewrite.

### Where synthesis sits — inside PLAN, before SEARCH

1. Fetch the API → `missing_media` array
2. For each entry with `search_queries = []`, synthesize 2–3 queries from these examples
3. Write them back into the entry's `search_queries` field
4. Save the augmented list to `games/<game>/.find-media/game_review.json`
5. Run it through the validator — stdlib only, so plain `python3`:

```bash
python3 .claude/skills/find-media/scripts/validate_queries.py \
  --from-api-json games/<game>/.find-media/game_review.json
```

---

# Part 2 — Per-source dialect

Google is the search route, and the only one (driven through your own Chrome — see
`references/chrome_route.md`).

**PornHub is DISCOVERY-ONLY — never a fetch target.** A PornHub-hosted Google result is
worth reading for its TITLE and TAGS, because that is where the canonical act vocabulary
lives, but it must not be queued for download. Measured: `egl.phncdn.com/gif/<id>.gif`
returns **470 on clearnet and over Tor**, every id tried — it is not a fetch endpoint at
all. The real media url, read off a gif page, is
`el2.phncdn.com/pics/gifs/<nnn>/<nnn>/<nnn>/<id>a.webm?validfrom=<ts>&validto=<ts>&ipa=1&hash=<sig>` —
signed, time-limited and IP-locked — and our extraction strips query strings, so the
signature is destroyed by construction. `pornhub.com` itself is unreachable on clearnet from
this machine. Skip phncdn urls as candidates: harvest the words, not the file.

So the tokenizer rules below are for **reading PornHub-sourced vocabulary**, and for the
validator's `--target pornhub` strip list. They are not instructions for a box you type
into. They are kept because they are measured, and because they explain why an
authoring-layer "fix" would be wrong — see the doctrine note at the end.

| | **Google** (the search route) | **PornHub tags** (vocabulary you read) |
|---|---|---|
| Length | 6–10 tokens is fine | tags come 2–3 wide; **4+ tokens returned literally 0 results** |
| Grammar | loose grammar works — `on kneel blowjob` returned usable results | grammar is noise; tags only |
| Rare words | fine, and they steer the result set | **silently dropped from compounds** |
| Story / character words | **poison** — reclassify the query as mainstream | dropped, so merely wasted |
| Format token (`gif`) | **mandatory** — without it Google serves stills and the extract harvests ~0 from a full page (7→59, 1→54, 0→91) | irrelevant; the tag taxonomy has no format axis |
| Setting words | only when the setting carries meaning, and **≤2 tokens** — more reclassifies the query as stock photography | costs a token from a 3-token budget |
| Anti-studio modifiers | `amateur` `real` `voyeur` `hidden cam` steer off bright studio | the same words are legitimate tags |
| Failure mode | wrong *neighbourhood* — Reddit, TikTok, Facebook, movie stills | 0 results, or 37 generic ones |

## Google dialect

**Append `gif` (or `webm`). This is the single highest-leverage token in the whole file —
put it in every query.** Measured three times on 2026-07-27, same query, one token added:

| Query | Fetchable urls |
|---|---|
| `bedroom flashing tits playful quick reveal` | 7 |
| `bedroom flashing tits playful quick reveal **gif**` | **59** |
| `bedroom tender facial cumshot gentle` | 1 |
| `bedroom tender facial cumshot gentle **gif**` | **54** |
| `bedroom woman riding passive man slow` | 0 |
| `bedroom woman riding passive man slow **gif**` | **91** |

**The failure is invisible from the screenshot.** All six pages carried ~200 image tiles.
The token-less queries were never starved of results — they were served **stills**, from
photo-gallery sites, and the §4 extractor only matches `gif|mp4|webm`. So a page that looks
rich harvests as approximately nothing, and it reads exactly like "the query was bad".
If an extract comes back in single digits off a full-looking grid, check for this token
before you rewrite anything else.

**Verbose is fine. Natural language is fine.** The descriptive multi-word queries game
authors write work here as written. Do not compress them into tags.

**Story and character words destroy porn intent.** Measured this session:
`back alley blowjob gif drunk guy night` returned Reddit movie stills, Facebook and
TikTok. Removing `drunk guy` is what put it back in the porn neighbourhood. The mechanism
is intent classification, not keyword dilution — Google reads "drunk guy" as narrative
language, decides you want a story about a drunk guy, and serves mainstream social. So:
strip who the person IS (drunk, stepbrother, boss, stranger, nervous) and keep what the
body DOES. This is the opposite reason from PornHub's rule, and it bites harder.

**Anti-studio modifiers are the fix for the most-repeated defect.** `amateur`, `real`,
`voyeur`, `hidden cam` push results away from bright, lit, three-camera studio porn. The
single most repeated rejection in this game's history is "bright studio when the beat
wants grimy". Add one of these whenever the beat is squalid, stolen, or hidden.

**Setting words only when the setting carries meaning — and at most about two of them.**
For one beat the user said the setting "doesn't matter much here"; for a dark-alley beat he
rejected bright clips twice, because the darkness carried the danger. Spend a token on
setting when it carries danger, secrecy or squalor — otherwise let act + position + heat
lead.

But there is a **ceiling**, and it was missed until 2026-07-27:
`back alley sex at night streetlight gif real` returned **Shutterstock and Getty licensable
stock footage of empty streets at night**, plus Medium, Wattpad, The Atlantic and Decider.
Pool collapsed to 33, mostly unusable. Piling up place-and-time words (`alley` + `at night`
+ `streetlight`) reclassifies the query as **stock photography** — the same intent flip that
story words cause, arriving from the words this rule tells you to spend. Name the place once,
add the light/time only if the place alone is ambiguous, and stop.

Corollary worth planning around: the load-bearing-setting slot is reliably **the hardest one
in any batch**. On the 10-slot study it was the only slot to need a sibling round and it
still finished with 3 survivors from 14 fetched, while non-setting slots cleared 6 easily.
Budget the extra round up front instead of treating it as a surprise.

**Read the labels, not just the pictures.** Google's own result labels and URLs are the
richest term mine available — this session they taught `dogging` (public/outdoor sex) and
`back alley` unprompted. When a label uses a word you did not know, that word is your
next query. (General web search is useless for this — sanitized, returns encyclopedia and
spam. Reddit's anonymous JSON API is blocked. Both were tried.)

## PornHub dialect (how to read its vocabulary — not a route)

These were measured against PornHub's own search box while the site was reachable. They
survive here as facts about **its tag taxonomy**, which is what you are borrowing when you
read a PornHub title off a Google result.

**Its vocabulary is 2–3 canonical tags wide.** 4+ token queries returned literally 0
results — a hard cliff, not a degradation. So when you mine a PornHub title for terms,
what you are looking for is the 1–2 canonical tags inside it (`dogging`, `back alley`),
not the whole title as a phrase.

**Rare words get silently dropped from compounds — a bigger number means a worse pool.**
Measured: `stockroom` alone returned 5 gifs; `stockroom blowjob` returned 37, and those 37
were generic blowjob, because the rare word was dropped and only `blowjob` survived. The
transferable lesson: a compound containing an unusual word is no evidence that a pool for
that unusual word exists. On Google the equivalent check is free — read the result labels
and see whether the rare word actually appears in them.

---

## Doctrine note — the authoring skill was never the bug

It is tempting, after seeing a descriptive `search_queries` entry return garbage, to
"fix" it upstream by making the authoring skill emit two-word tags. Don't. Those
descriptive queries only ever failed against **PornHub's search tokenizer**, which is not a
route here at all. On Google the same verbose, natural-language queries work.
The defect lived in one engine's tokenizer, and it has been routed around. Mandating
tag-shaped queries in the authoring layer would throw away the narrative specificity that
makes a query steerable, to satisfy a search box we stopped typing into.

Also retired with it: the old **setting-first formula** (`kitchen+blowjob` over
`blowjob+kitchen`). Its entire justification was "PornHub weights the first keyword
heavily". The validator never enforced it, and no measurement supports word order
mattering on Google. Do not reorder queries for its own sake; decide whether the setting
word belongs in the query at all, which is the question that actually changes results.

### What the 2026-07-27 control actually proved — read this before crediting word order

A ten-slot rig (`games/media_lab/`) ran three slots with deliberately OLD-doctrine queries
against seven new-style ones. **OLD: 18 fetchable urls across 6 queries (7, 9, 1, 0, 0, 1).
NEW: ~63 per query across 14.** A ~21× gap, so the doctrine change is earned.

**But the gap is not evidence for act-led word order, and must not be cited as such.**
Disambiguation queries decomposed it into two independent causes, neither of which is order:

1. **The missing format token** — the table at the top of the Google dialect section. Worth
   roughly an order of magnitude on its own.
2. **Story / mood words flipping the intent class** — `loving facial girlfriend soft`
   returned TikTok, Instagram, Shutterstock, Temu and Amazon, with **zero** pornographic
   results on the page. `bedroom woman riding passive man slow` returned Cosmopolitan,
   Bustle, Men's Health and cartoon position diagrams.

**These are independent, and the format token fixes only the first.** The `+gif` rerun of the
riding query returned 91 urls, and half the contact sheet was Tenor reaction memes, a bull
rider, a bicycle and TV clips — 7 of 14 fetched candidates were mainstream gifs. `gif` made
the poison *fetchable*; it did not remove the poison. Diagnose which failure you have before
reaching for a fix: a full grid harvesting near-zero is (1); a full harvest of off-band
content is (2).

Full write-up and per-query counts: `games/media_lab/.find-media/FINDINGS.md`.

---

## The validation report

`validate_queries.py` prints these sections, in this order, and exits **1** if any of
FLAGGED / TIER MISMATCH / FORMAT MISMATCH / TIER RETAG is non-empty (0 otherwise):

```
=== Query Validation Report ===
Checked 47 queries across 19 items (target: google).

⚠️  FLAGGED (2 queries need narrative-context rewrite):

  [NEEDS NARRATIVE] scenes/breakfast_ethan_t6.webm (t6)
    Original: 'oral kitchen counter'
    Issues:   needs_direction_from_narrative:oral

  [UNUSABLE] scenes/solo_t5.webm (t5)
    Original: 'masturbation bedroom'
    Issues:   unusable_query, unusable:masturbation_is_solo_only

⚠️  TIER MISMATCH (1 queries):

  [t3] locations/kitchen_t3.jpg
    Query:    'kitchen blowjob morning'
    Issues:   tier_mismatch:sfw_query_has_sexual_term

✅ AUTO-REWRITTEN (1 queries):

  scenes/couch_t5.webm (t5)
    Original:  'hand job on the couch'
    Rewritten: 'handjob on the couch'
    Rules:     rewrote:hand job→handjob

⚠️  FORMAT MISMATCH (1 items — motion vs static):

  scenes/riding_t6.jpg
    Current:     .jpg
    Detected:    animated (riding, thrusting)
    Recommended: .webm
    description/queries suggest motion (riding, thrusting) but file is .jpg — use .webm or .gif

⚠️  TIER RETAG (1 confident auto, 1 need your call):

  [AUTO → _t5] scenes/hallway.webm
    untagged but description is explicit (blowjob) → NSFW
  [ASK  → suggest _t4] scenes/porch.jpg
    untagged borderline (kissing) — confirm heat: t3 peck / t4 makeout / t5+ explicit

✅ OK: 39 queries pass without changes.
   Format OK: 18/19 items.
```

`--json` emits `{target, exit_code, queries, format_checks, tag_proposals}` instead of the
human report — the same exit code rides in the payload, so a caller reading stdout does not
have to shell out for `$?`. Use it when you are feeding the retag flow in
`references/content_rating.md`.

Read the report, resolve every FLAGGED item from the TOML narrative, and carry the
rewritten queries into SEARCH. FORMAT MISMATCH and TIER RETAG are separate axes handled
elsewhere; they ride along in the same run because they need the same parse.
