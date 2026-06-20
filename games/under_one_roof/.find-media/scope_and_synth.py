"""Scope + query-synthesis for all 34 social_post_image items.

- Classify tier per caption (SFW base/t2/t3 vs NSFW t4/t5/t6)
- Write per-item scope briefs under .find-media/scope/
- Synthesize 2-3 search queries and write them back into game_review.json
"""
import json
import os
import re
from pathlib import Path

ROOT = Path("/Users/a0000/Desktop/Desktop_Archive_Backup/story_gen/story_gen_web_app/story_gen_django")
FM = ROOT / "games/under_one_roof/.find-media"
SCOPE_DIR = FM / "scope"
SCOPE_DIR.mkdir(parents=True, exist_ok=True)

review = json.loads((FM / "game_review.json").read_text())

# Tier + query synthesis per item, hand-classified from captions
PLAN = {
    # SFW tier (items 1-9) — routed to sfw-searcher
    "social/jess_gym_1.jpg":       ("t2", "sfw", [
        "fit woman gym mirror selfie leg day",
        "athletic woman squat rack gym selfie morning",
        "woman leg day workout gym selfie"]),
    "social/mia_beach_1.jpg":      ("t2", "sfw", [
        "woman beach golden hour sunset selfie",
        "girl sunset beach silhouette selfie",
        "woman beach sunset instagram selfie"]),
    "social/vanessa_mirror.jpg":   ("t2", "sfw", [
        "woman full length mirror selfie outfit casual",
        "outfit of the day mirror selfie woman",
        "casual chic mirror selfie woman brunch outfit"]),
    "social/kaylee_pool.jpg":      ("t2", "sfw", [
        "woman pool bikini summer selfie",
        "poolside bikini woman selfie sunny",
        "summer pool deck bikini woman selfie"]),
    "social/brooklyn_club.jpg":    ("t3", "sfw", [
        "woman nightclub bathroom mirror selfie",
        "woman club dressed up mirror selfie night",
        "nightlife woman bar mirror selfie makeup"]),
    "social/ember_tattoo.jpg":     ("t2", "sfw", [
        "woman fresh arm tattoo close up",
        "alternative woman new tattoo reveal",
        "woman showing fresh ink arm"]),
    "social/tiffany_bedroom.jpg":  ("t2", "sfw", [
        "woman cozy bedroom sunday selfie oversized shirt",
        "messy bun bedroom morning selfie woman",
        "cozy bedroom woman bed selfie lazy"]),
    "social/peachy_gym.jpg":       ("t3", "sfw", [
        "woman gym leggings booty mirror selfie",
        "fit woman athletic leggings squat progress",
        "gym progress selfie woman back view leggings"]),
    "social/jess_gym_2.jpg":       ("t3", "sfw", [
        "woman sweaty gym sports bra mirror selfie",
        "post workout gym selfie woman sports bra",
        "fit woman gym mirror sports bra tight"]),

    # t4 — suggestive NSFW (items 10-18)
    "social/natasha_lingerie.jpg": ("t4", "nsfw", [
        "amateur+lingerie+mirror+selfie",
        "bedroom+lingerie+tease",
        "amateur+lingerie+pose+mirror"]),
    "social/lexi_towel.jpg":       ("t4", "nsfw", [
        "amateur+towel+bathroom+selfie",
        "amateur+towel+drop+mirror",
        "bathroom+mirror+towel+reveal"]),
    "social/daisy_sheer.jpg":      ("t4", "nsfw", [
        "amateur+sheer+top+nipples",
        "seethrough+shirt+bedroom+selfie",
        "amateur+seethrough+top+bra+less"]),
    "social/mia_bikini.jpg":       ("t4", "nsfw", [
        "amateur+micro+bikini+beach",
        "tiny+bikini+selfie+beach",
        "amateur+bikini+beach+pose"]),
    "social/raven_underwear.jpg":  ("t4", "nsfw", [
        "amateur+panties+mirror+selfie+bedroom",
        "amateur+thong+mirror+late+night",
        "bedroom+underwear+selfie+amateur"]),
    "social/samantha_bed.jpg":     ("t4", "nsfw", [
        "amateur+lingerie+bed+pose",
        "amateur+bedroom+lingerie+tease",
        "amateur+bed+panties+selfie"]),
    "social/nikki_seethrough.jpg": ("t4", "nsfw", [
        "amateur+seethrough+dress+no+underwear",
        "transparent+outfit+reveal+amateur",
        "amateur+sheer+dress+mirror"]),
    "social/ember_bra.jpg":        ("t4", "nsfw", [
        "amateur+tattooed+girl+bra+selfie",
        "alternative+woman+bra+tattoo+mirror",
        "amateur+bra+tattoos+chest+mirror"]),
    "social/amelia_tease.jpg":     ("t4", "nsfw", [
        "amateur+lingerie+tease+bedroom",
        "amateur+seductive+pose+bedroom",
        "amateur+sultry+tease+lingerie"]),

    # t5 — explicit nude stills (items 19-28)
    "social/cherry_barely.jpg":    ("t5", "nsfw", [
        "amateur+undressing+bedroom+solo",
        "amateur+lingerie+off+selfie",
        "amateur+topless+bedroom+barely+clothed"]),
    "social/lexi_bedroom.jpg":     ("t5", "nsfw", [
        "amateur+solo+female+bedroom",
        "solo+female+touch+bed+amateur",
        "amateur+alone+bedroom+intimate+selfie"]),
    "social/jess_locker.jpg":      ("t5", "nsfw", [
        "amateur+locker+room+nude+selfie",
        "amateur+post+shower+locker+room",
        "amateur+gym+locker+room+fit+nude"]),
    "social/natasha_nude.jpg":     ("t5", "nsfw", [
        "amateur+nude+peek+mirror+selfie",
        "amateur+nude+tease+bedroom",
        "amateur+nude+partial+reveal+mirror"]),
    "social/samantha_spread.jpg":  ("t5", "nsfw", [
        "amateur+nude+bed+legs+spread",
        "amateur+naked+bed+pose+spread",
        "amateur+nude+bedroom+waiting"]),
    "social/raven_nude.jpg":       ("t5", "nsfw", [
        "amateur+artistic+nude+tattoo",
        "alternative+nude+tattooed+woman",
        "amateur+tattooed+nude+artistic"]),
    "social/tiffany_topless.jpg":  ("t5", "nsfw", [
        "amateur+topless+bedroom+selfie",
        "amateur+topless+bed+selfie",
        "amateur+bedroom+nude+lazy+sunday"]),
    "social/cherry_explicit.jpg":  ("t5", "nsfw", [
        "amateur+fully+nude+bedroom+mirror",
        "amateur+naked+stripped+mirror",
        "amateur+nude+full+body+mirror"]),
    "social/amelia_full.jpg":      ("t5", "nsfw", [
        "amateur+full+nude+bedroom+selfie",
        "amateur+nude+full+body+pose",
        "amateur+naked+bedroom+mirror+selfie"]),
    "social/peachy_nude.jpg":      ("t5", "nsfw", [
        "amateur+nude+booty+gym+body",
        "amateur+naked+workout+body+back",
        "amateur+nude+ass+fitness+selfie"]),

    # t6 — hardcore / explicit acts (items 29-34)
    "social/lexi_explicit.jpg":    ("t6", "nsfw", [
        "amateur+explicit+spread+bedroom+solo",
        "amateur+pussy+spread+bed+selfie",
        "amateur+explicit+nude+pose+bed"]),
    "social/daisy_nude.jpg":       ("t5", "nsfw", [
        "amateur+full+nude+young+woman+mirror",
        "amateur+naked+body+selfie+petite",
        "amateur+nude+full+body+slender"]),
    "social/nikki_reveal.jpg":     ("t5", "nsfw", [
        "amateur+nude+full+reveal+selfie",
        "amateur+full+nude+mirror+pose",
        "amateur+nude+reveal+bedroom+mirror"]),
    "social/samantha_hardcore.jpg":("t6", "nsfw", [
        "amateur+couple+sex+bedroom",
        "amateur+missionary+bedroom+couple",
        "amateur+bed+sex+pov+couple"]),
    "social/ember_explicit.jpg":   ("t6", "nsfw", [
        "amateur+toy+solo+bedroom+tattooed",
        "amateur+dildo+solo+selfie+alternative",
        "amateur+solo+toy+bedroom+female"]),
    "social/cherry_video.jpg":     ("t5", "nsfw", [
        "amateur+nude+promo+pose+selfie",
        "amateur+explicit+full+body+promo",
        "amateur+naked+full+body+tease"]),
}

# Write scope briefs + patch in synthesized queries
now_plan = []
for entry in review["missing_media"]:
    fpath = entry["file"]
    tier, rating, queries = PLAN[fpath]
    entry["search_queries"] = queries
    entry["_tier"] = tier
    entry["_content_rating"] = rating

    stem = Path(fpath).stem  # e.g. jess_gym_1
    poster_match = re.match(r"@([^:]+):\s*(.*)", entry["description"])
    poster = poster_match.group(1) if poster_match else "?"
    caption = poster_match.group(2) if poster_match else entry["description"]
    hashtags = re.findall(r"#\w+", caption)

    brief = f"""# Scope Brief — {stem}

- item_id: {stem}
- file_path: {fpath}
- type: social_post_image
- category: Social Media
- canvas_id: phone
- order: {entry["order"]}
- tier: {tier}
- content_rating: {rating}
- required_format: .jpg (static phone post)

## Narrative
- Poster: @{poster}
- Caption: {caption}
- Hashtags: {hashtags or "(none)"}

## Rejection
- Reject group shots (3+ people)
- Reject professional studio portraits — must look like a candid phone selfie
- {"Reject 2+ people (this is a solo selfie)" if rating == "nsfw" and "hardcore" not in fpath else "Allow solo or couple per caption"}
- Reject content that contradicts the caption persona

## Queries (synthesized)
1. {queries[0]}
2. {queries[1]}
3. {queries[2]}

## Mode
- {"quick" if rating == "sfw" else ("standard" if tier == "t4" else "deep")}

PHASE: scope_complete
NEXT_PHASE: plan
SCORED: no
PACKAGED: no
"""
    (SCOPE_DIR / f"{stem}.md").write_text(brief)
    now_plan.append((stem, tier, rating))

# Save updated review with synthesized queries
(FM / "game_review.json").write_text(json.dumps(review, indent=2))

# Summary
from collections import Counter
tc = Counter((t, r) for _, t, r in now_plan)
print(f"Wrote {len(now_plan)} scope briefs to {SCOPE_DIR}")
for (tier, rating), count in sorted(tc.items()):
    print(f"  {tier} {rating}: {count}")
