# Scoring Rubric

How to score harvested candidates. Read this during EVALUATE phase. Scoring happens AFTER hard-rejection filters drop disqualified candidates.

## Format note — image vs animated is ACTION-driven, not tier-driven

Before scoring, confirm the candidate's format matches the scene's content class:

- **Static (`.jpg`)** for domestic, conversational, location, light-flirt scenes where motion doesn't add anything
- **Animated (`.webm` / `.gif` / `.mp4`)** for kiss / tease / undress / flash / bathing / solo-nudity / any explicit scene

A kiss scene rendered as a still photo loses the chemistry. A dinner scene as a looped GIF is overkill. If the TOML's file extension disagrees with the scene's action class, `scripts/validate_queries.py` catches it during PLAN — but remember this rule during EVALUATE too, so you don't score a static candidate highly on a scene that actually needs motion.

See SKILL.md §Format classification for the full matrix.

## Two rubrics by content rating

### SFW rubric (tier base, t2, t3)

| Criterion | Weight | What to check |
|-----------|--------|---------------|
| Relevance | 40% | Matches description and setting exactly |
| Mood | 30% | Intimate, warm, domestic feel appropriate to the narrative beat |
| Composition | 30% | Well-framed, good resolution (>800px), usable as a full-scene game asset |

**Accept threshold: 70.** Below 70 → critique cycle.

### NSFW rubric (tier t4+)

| Criterion | Weight | What to check |
|-----------|--------|---------------|
| Setting | 30 | Visible environment matches narrative (kitchen/couch/pool/bed/outdoor/etc) |
| Action | 40 | Sexual act matches narrative (oral/doggy/missionary/counter sex/etc) |
| Appearance | 20 | Default: white female, petite or thick body type. Hair flexible. Male appearance doesn't matter — POV or anonymous is fine. |
| Quality | 10 | Resolution, framing, lighting. Watermarks acceptable — these are placeholders. |

**Accept threshold: 60.** Below 60 → critique cycle.

## Hard rejection filters (score = 0, skip before scoring)

Apply these before anything else. A candidate that triggers ANY filter gets 0 and is not scored.

### SFW hard rejects

- **3+ people** on activity canvases — this is a two-person story
- **Children or families** — never appropriate
- **Crowds** — domestic activities are private
- **Restaurant or commercial venue** when query is home-based — `home kitchen` means HOME, not a restaurant kitchen
- **Obvious AI-generation artifacts** — wonky hands, smeared faces, impossible geometry
- **Heavy watermarks/logos covering subject** — usable only if the watermark is in a corner

### NSFW hard rejects

- **3+ people** (threesomes, groups) — two-person story
- **Solo** (no couple interaction) — every activity scene is M/F
- **Same-sex couple** when game requires M/F — check NPC gender from TOML
- **BDSM gear** (ropes, paddles, gags, restraints, crops, blindfolds, harnesses) — domestic scenes don't involve kink unless explicitly in narrative
- **Interracial** when game character doesn't match — check NPC description in TOML character section
- **Visibly 40+** (mature/MILF tagged content) when game character is young (20s–30s)
- **Cosplay/costumes/uniforms** when scene is casual/domestic — a schoolgirl outfit in a "morning coffee" scene is wrong
- **BBW/SSBBW** body types when NPC is described as petite or average
- **Extreme/fetish content** — rough/gagging/choking/facial when narrative is tender

## Scoring procedure

For each candidate that survives hard rejection:

1. **View the CLIP montage** with the Read tool — one image, top-K tiles labeled A, B, C…. CLIP pre-ranked the tiles but does NOT score them; you do. On NSFW, CLIP ranked only setting/people (25–31% on acts), so **re-judge the act on every tile**. Map a chosen tile letter back to its candidate id via the `clip_shortlist.py` JSON `ranked[].montage_label`. (If CLIP was unavailable — exit 3 — fall back to viewing each thumbnail directly, as before.)
2. **Score each criterion** 0 to its weight maximum. Don't inflate — if setting is "kitchen" and the thumbnail shows a generic bed, setting scores 0 to 5 out of 30, not 15.
3. **Sum the criteria** for the overall score.
4. **Record to `scores.jsonl`** — even losing scores are kept, for telemetry and resume.

## The `scores.jsonl` format

One JSON object per line. Written to `games/<game>/.find-media/evidence/<item_id>/scores.jsonl`:

```json
{"candidate_id": "gif/10941841", "thumbnail_path": "/tmp/nsfw_previews/breakfast_ethan_t5/4_10941841.jpg", "title": "Hot counter fuck", "setting": 28, "action": 38, "appearance": 16, "quality": 7, "total": 89, "decision": "winner", "rejected_reason": null}
{"candidate_id": "gif/53980631", "thumbnail_path": "...", "title": "Cum inside mouth", "setting": 0, "action": 0, "appearance": 0, "quality": 0, "total": 0, "decision": "hard_reject", "rejected_reason": "wrong_setting:bed"}
```

The `decision` field: `winner`, `runner_up`, `below_threshold`, `hard_reject`.

## Picking the winner

After scoring all candidates:

1. Filter to candidates above threshold (60 NSFW / 70 SFW)
2. Of those, pick the **highest total score**
3. Tiebreak: higher `setting` score wins (settings are rarer than actions)
4. Second tiebreak: higher `action` score wins

If zero candidates above threshold → trigger CRITIQUE cycle. Do NOT accept a below-threshold candidate silently.

## Calibration notes

**What a "good" NSFW score looks like**:
- Setting 25–30: thumbnail clearly shows the described environment, not ambiguous
- Action 30–40: the sexual act is the described act, in the described position if specified
- Appearance 15–20: female matches default (white, petite/thick, flexible hair); male is POV or unobtrusive
- Quality 7–10: not blurry, not a tiny preview frame, watermark is corner-only

**What a "passing but not great" score looks like (60–70)**:
- Setting partial — right type (kitchen-ish) but wrong specifics (restaurant instead of home)
- Action close but imperfect — described missionary but thumbnail shows cowgirl at counter instead
- Use this to PASS, but only if no higher-scored candidate exists

**What "below threshold" looks like (<60)**:
- Setting wrong — described kitchen, thumbnail shows bedroom with no kitchen element
- Action wrong — described blowjob, thumbnail shows kissing
- Trigger critique cycle, not a silent downgrade

## Why scores live on disk

Persistence in `scores.jsonl` isn't bookkeeping overhead. It unlocks:

- **Resume** — if a Tor circuit drops mid-evaluation, the LLM reads scores.jsonl on restart and skips already-scored candidates
- **Telemetry** — `run_manifest.json` aggregates score distributions across items, revealing whether queries were systematically weak or whether sources were thin
- **Audit** — a human reviewing a questionable final pick can read the rejected candidates and their reasons
- **Cross-game learning** — after 10 games, aggregated scores per source tell you whether GIPHY or Unsplash has higher hit rate for your typical scenes
