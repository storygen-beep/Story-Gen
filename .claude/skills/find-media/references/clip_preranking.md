# CLIP pre-ranking + montage

A local CLIP model ranks harvested candidates so the LLM views **one montage**
instead of ~15 thumbnails one by one. This is the largest token saving in the
skill: a real run viewed ~5–8 thumbnails per item (≈0.5–1M tokens per game just
*looking*); a montage collapses that to ~1 image Read per item.

Read this when running `clip_shortlist.py` / `video_frames.py`, building a montage,
or deciding what caption to feed CLIP.

## What CLIP is for here — and what it is NOT

CLIP is a **pre-filter that decides what the LLM looks at. It never replaces a
quality gate and never makes the final pick.** Its competence differs sharply by
content rating (measured on this repo's own media):

| Job | CLIP result | Role |
|---|---|---|
| SFW: pick the right image | top-1 **60%** / top-3 **88%** (25-way) | **Strong shortlister** — montage top-3, LLM confirms |
| NSFW: judge the act | **25–31%** | **Cannot.** Coarse cull only |
| NSFW: cull garbage 15→5 | top-5 held 3–4 good, sank threesomes/wrong-setting | **Coarse cull** — LLM still judges the act |

So: trust CLIP's shortlist on SFW; on NSFW use it **only** to drop obvious garbage
(wrong setting, solo, 3+ people, same-sex), then the LLM judges the act on the
survivors. Never let CLIP pick the act-specific NSFW winner.

## Caption policy (load-bearing)

- **Feed CLIP the validated SEARCH QUERY, never the narrative prose.** Demo: query
  caption scored 60% top-1 vs 32% for the scene's flavor text. CLIP was trained on
  literal web captions ("a woman eating a sandwich in a kitchen"), not second-person
  game prose. Use the top-ranked query from PLAN/`validate_queries.py`.
- **For the NSFW cull, caption on SETTING + PEOPLE, not the act.** CLIP is worst at
  acts (25–31%); an act-heavy caption ranks on its weakness and can sink a correctly-
  set clip. Caption `"a man and woman having sex on a kitchen counter"` (environment
  + people) — let the LLM judge missionary-vs-cowgirl on the montage.

## Prerequisites (one-time)

CLIP needs `torch`, `transformers`, `Pillow`, which exist only on the **global
Framework python**, not the django venv. The model (~600MB) downloads once.

```bash
# install deps on the torch-bearing interpreter (NOT the venv)
/Library/Frameworks/Python.framework/Versions/3.10/bin/python3 -m pip install \
    -r .claude/skills/find-media/scripts/requirements.txt
# first clip_shortlist.py run fetches openai/clip-vit-base-patch32 into ~/.cache/huggingface
# (needs network ONCE; afterwards HF_HUB_OFFLINE=1 keeps it offline + fast)
```

`video_frames.py` needs only `ffmpeg`/`ffprobe` (no torch) — already at `/opt/homebrew/bin`.

## Invoke via the explicit interpreter — never bare `python3`

Bare `python3` may resolve to the torch-less venv (then every run silently falls
back and CLIP is never used). Always pin the interpreter:

```bash
"${FIND_MEDIA_PY:-/Library/Frameworks/Python.framework/Versions/3.10/bin/python3}" \
  .claude/skills/find-media/scripts/clip_shortlist.py ...
```

Override with `export FIND_MEDIA_PY=/path/to/torch-python` if the Framework python moves.

## `clip_shortlist.py`

Ranks a candidate set against a caption → ranked JSON on stdout + a labeled top-K
montage JPG in the item's evidence dir.

```bash
"${FIND_MEDIA_PY:-/Library/Frameworks/Python.framework/Versions/3.10/bin/python3}" \
  .claude/skills/find-media/scripts/clip_shortlist.py \
  --candidates-dir games/<game>/.find-media/evidence/<item>/candidates \
  --caption "<top validated query>" --top-k 5 --item-id <item> \
  --montage-out games/<game>/.find-media/evidence/<item>/montage_shortlist.jpg --json
```

- Inputs: `--candidates-dir <dir>` (ranks every `.jpg/.jpeg/.png/.webp`) **or**
  `--manifest <candidates.jsonl>` (records with `path`/`thumbnail_path`/`frame_path`
  + optional `id`/`title`). Harvest/rep-frame files named `<i>_<gifId>.jpg` yield
  `id = gifId` (so the pick feeds `dedup_tracker.py` directly).
- `--top-k`: tiles in the montage. **SFW: 5** (top-3 was 88%). **NSFW cull: 6** —
  CLIP's act-blindness can push a good clip to rank 6; the extra tile is near-free.
- Output JSON lists **all** candidates ranked: `[{rank,id,path,score,montage_label}]`.
  `montage_label` is the tile letter (A,B,C…) for the top-K, else `null`.
- **The LLM does ONE Read on the montage**, then picks by tile letter; map the letter
  back to the candidate id via `ranked[].montage_label`. CLIP scores are advisory —
  the LLM still applies hard-rejects and the rubric and makes the call.

## `video_frames.py` (NSFW video)

ffmpeg-only. A GIF clip has no meaningful poster frame, so:

```bash
# rep: one representative still per clip (median-of-N — skips black/seam frames) → feeds CLIP
"$FIND_MEDIA_PY" .../video_frames.py --videos-dir /tmp/nsfw_previews/<name> \
  --mode rep --frames 3 --out-dir /tmp/nsfw_previews/<name>/frames --json
# strip: act-verification strip for the CHOSEN clip → LLM Reads it to confirm the act
"$FIND_MEDIA_PY" .../video_frames.py --video <pick.webm> --mode strip --frames 4 \
  --out games/<game>/.find-media/evidence/<item>/verify_strip.jpg
```

`--mode strip` supersedes the old single `ffmpeg -ss 00:00:02 -vframes 1` verify frame
in `nsfw_pipeline.md` — multi-frame catches an act the poster hides.

## Montage as evidence

Montages are durable artifacts at `evidence/<item>/montage_shortlist.jpg` (SFW) /
`montage_cull.jpg` (NSFW) / `verify_strip.jpg`. They survive a crash, are viewable on
resume, and let a human audit why a pick was made.

## Fallback contract (never crash a run)

Both scripts exit **3** when their deps/model are unavailable (`clip_shortlist.py`:
torch/transformers/PIL missing or model not cached; `video_frames.py`: ffmpeg/ffprobe
absent). On exit 3 the caller prints the notice and **degrades to today's behavior** —
the LLM Reads each thumbnail directly (and uses the harvest poster `.jpg` if frames
can't be extracted). "CLIP off" == the original skill, just more tokens. The feature is
a strict, reversible enhancement.

## Future: auto-accept (NOT enabled)

A tempting next step is to ship a CLIP top-1 with **no** LLM look when its score clears
a confident cutoff — removing easy SFW items from the LLM entirely. This is **not
enabled**: the per-pool SFW calibration was never run, and 60% top-1 means ~2 in 5
auto-accepts would be wrong without a tuned threshold. Design it later as a
`--auto-accept-threshold` flag calibrated on real per-query pools; until then every
item gets an LLM look at its montage.
