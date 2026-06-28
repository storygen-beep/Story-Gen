# Content rating — SFW vs NSFW routing (tier audit + retag)

How the skill decides which pipeline an item goes to, and how it fixes a missing or
wrong tag at the source instead of routing around it.

## The principle

SFW vs NSFW comes from the `_tN` suffix in the filename (`infer_tier`,
`validate_queries.py`). That's a manual flag the author can forget or set wrong:

- **No tag** silently defaults to `base` = SFW. A passionate kiss with no suffix gets
  pulled as a tame stock photo.
- **Wrong tag** misroutes: a sex scene tagged `_t2` → stock (gets nothing); a dinner
  tagged `_t6` → PornHub (absurd).

So: **content leads the routing; the tag grades the heat.** The *description* is more
reliable than one keystroke for the binary "does this need an adult source?"; the tag is
the better signal for *how explicit* within NSFW (t4 vs t6), which words can't grade.
When they disagree, **fix the tag at the source** — don't route off a tag known to be
wrong. The routing question is **"is there nudity or a sex act?"** — not "is it intense?".

## The three rating buckets (NOT the format keywords)

These are purpose-built and deliberately separate from `ANIMATED_KEYWORDS` (the
still-vs-clip FORMAT axis, which lumps "kiss"/"bath" with "fuck"):

- **HARD-NSFW** (stock can't serve → confident): sex acts (`SEXUAL_TERMS_FOR_SFW_CHECK`)
  + explicit nudity (nude, naked, topless, undress, strip, flash) + anal/deepthroat.
- **BORDERLINE** (clothed→explicit; only the author knows the heat): kiss, makeout,
  tease, seduce, grind, caress, grope, fondle, straddle, "in bed", lingerie, and
  solo-body bathe/bath/shower/washing.
- **SFW** (vanilla): the domestic `STATIC_KEYWORDS` + flirt, hug, holding hands, cuddle,
  smile, date, greet, talk.

`classify_content_rating(description, search_queries)` → `hard_nsfw | borderline | sfw |
unknown` (hard wins, then borderline, then sfw).

## The audit → retag matrix

`infer_tier_tagged` reports `was_tagged` (true only on a real `_tN`/`_base` suffix —
distinguishing a forgotten tag from an intentional `_base`). Then `propose_tag`:

| was_tagged | tag | content | action |
|---|---|---|---|
| no | — | hard_nsfw | **auto-retag `_t5`**, announce |
| no | — | borderline | **ASK** the heat (t3 peck / t4 makeout / t5+ explicit); suggest t4 |
| no | — | sfw / unknown | leave (untagged = base = SFW, already correct) |
| yes | SFW (base/t2/t3) | hard_nsfw | **auto-retag `_t5`**, announce |
| yes | SFW | borderline | **ASK** (current tag may be fine); suggest t4 |
| yes | SFW | sfw / unknown | leave |
| yes | NSFW (t4+) | sfw (vanilla, no act/nudity) | **ASK** before demoting; suggest base |
| yes | NSFW | hard_nsfw / borderline / unknown | leave (tag stands) |

**Asymmetry by design:** up-grades on explicit content are confident **auto** (routing a
sex scene to stock is just broken); **down-grades and all borderline calls are ASKED** —
the author owns the heat grade, and the ask writes a *permanent* correct tag, not a
one-shot route. Non-canvas types (location/clothing/social/profile) are always SFW and
never audited.

## How to run it (ordering matters)

```bash
# 1. audit — proposals come out of the normal validate run
"$VALIDATE_PY" .../validate_queries.py --from-api-json games/<game>/.find-media/game_review.json --json
#    read tag_proposals[]: action ∈ {auto_retag, ask, leave}

# 2. take the auto_retags as-is; ASK the user the tier for every `ask`; build accepted.json
#    [{"file":"activities/couch_kiss.jpg","tier":"t4"}, ...]

# 3. write the corrected suffixes into the SOURCE phases (dry-run first)
"$VALIDATE_PY" .../apply_retags.py --phases-dir games/<game>/toml_phases --accepted accepted.json --dry-run
"$VALIDATE_PY" .../apply_retags.py --phases-dir games/<game>/toml_phases --accepted accepted.json

# 4. re-merge + re-package so the rename lands, then RE-FETCH the missing-media list
python scripts/merge_toml_phases.py ...   &&   python manage.py package_from_toml ...
#    re-run the game-review load — now the missing list reflects the corrected names
```

After that, routing/format/SCOPE all derive from the corrected `_tN` through the
**unchanged** `infer_tier`→pipeline path — no runtime override. `apply_retags.py` never
touches `*_final_game.toml` (the merge regenerates it; per CLAUDE.md). It exits 1 if any
accepted path matched nothing in the phases — check the path.

Edge: retag is cleanest for genuinely *missing* items (no file to orphan). If a file
already exists under the old name, also rename the on-disk asset to the new name.

## What stays the same

The **format** axis (`classify_content_family`, still-vs-animated) and
`tier_format_check.py` are untouched — once the suffix is correct, they just work. A
kiss is both *borderline-rating* (→ ASK the tier) and *animated-format* (→ `.webm`); the
two axes are decided independently.
