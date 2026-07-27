# CLIP pre-ranking + the contact sheet

A local CLIP model orders harvested candidates so you look at **one contact sheet**
instead of ~15 thumbnails one at a time. That ordering is also how a slot's stocked
options — 6 / 12 / 18 depending on mode, per SKILL.md §Mode — get eyes on them without
burning the budget: a real run viewed ~5–8 thumbnails per item (≈0.5–1M tokens per game
just *looking*), and the new shape stocks *more* candidates per slot, not fewer. One image
Read per item is the only way that scales.

Read this when running `clip_shortlist.py` / `video_frames.py`, building a contact
sheet, or deciding what caption to feed CLIP.

## What CLIP is for here — and what it is NOT

CLIP is a **pre-filter that decides what gets LOOKED AT. It never replaces a gate and
never makes the final pick.** Its competence differs sharply by content rating
(measured on this repo's own media):

| Job | CLIP result | Role |
|---|---|---|
| SFW: pick the right image | top-1 **60%** / top-3 **88%** (25-way) | **Strong shortlister** — sheet the top few, confirm by eye |
| NSFW: judge the act | **25–31%** | **Cannot.** Coarse cull only |
| NSFW: cull garbage 15→6 | top-5 held 3–4 good, sank threesomes/wrong-setting | **Coarse cull** — the act is still judged by eye |

That 25–31% row is the whole argument for the skill's shape. **A machine cannot pick
these clips**, so the skill does not try: it culls the obvious garbage, stocks the
survivors as options, and lets the human eye decide. Use CLIP on NSFW **only** to drop
what is trivially wrong (wrong setting, solo, 3+ people, same-sex), never to choose
between two plausible clips — that is exactly the band where it is a coin flip.

## Caption policy (load-bearing)

- **Feed CLIP the validated SEARCH QUERY, never the narrative prose.** Measured: query
  caption scored 60% top-1 vs 32% for the scene's flavor text. CLIP was trained on
  literal web captions ("a woman eating a sandwich in a kitchen"), not second-person
  game prose. Use the top-ranked query from PLAN / `validate_queries.py`.
- **For the NSFW cull, caption on SETTING + PEOPLE, not the act.** CLIP is worst at
  acts (25–31%); an act-heavy caption ranks on its weakness and can sink a correctly-set
  clip. Caption `"a man and woman having sex on a kitchen counter"` (environment +
  people) — judge missionary-vs-cowgirl yourself on the sheet.

## Input contract — the candidate pool is MIXED

The Chrome route returns `.gif` as often as `.mp4`/`.webm`, plus ordinary stills. The
two scripts split on that boundary and the split is not cosmetic:

| Input | `video_frames.py` | `clip_shortlist.py` |
|---|---|---|
| `.gif` | **handled** — in `VIDEO_EXTS` (`video_frames.py:45`) | **rejected** — not in `IMAGE_EXTS` (`clip_shortlist.py:53`) |
| `.webm` `.mp4` `.mov` `.mkv` | handled | rejected |
| `.jpg` `.jpeg` `.png` `.webp` | n/a | ranked |

So: **anything animated gets a representative frame extracted FIRST, then ranks.**
Point `clip_shortlist.py` at a directory of raw gifs and it finds zero images and exits
1 ("no candidate images found") — which reads like an empty harvest when the harvest was
fine. Always run `--mode rep` over the candidates dir and rank the `frames/` dir.

Name candidate files `<i>_<id>.<ext>` (e.g. `03_10941841.gif`). `candidate_id()`
(`clip_shortlist.py:77`) strips the leading `<i>_`, so the source id survives the frame
extraction and the ranked JSON maps straight back to the option-store URL.

## Prerequisites (one-time)

CLIP needs `torch`, `transformers`, `Pillow`, which exist only on the **global Framework
python**, not the django venv. The model (~600MB) downloads once.

```bash
# install deps on the torch-bearing interpreter (NOT the venv)
/Library/Frameworks/Python.framework/Versions/3.10/bin/python3 -m pip install \
    -r .claude/skills/find-media/scripts/requirements.txt
# first clip_shortlist.py run fetches openai/clip-vit-base-patch32 into ~/.cache/huggingface
# (needs network ONCE; afterwards the pinned offline mode keeps it offline + fast)
```

`clip_shortlist.py` sets `HF_HUB_OFFLINE=1` / `TRANSFORMERS_OFFLINE=1` **before**
importing transformers (`clip_shortlist.py:48`). That is deliberate: a cache miss then
raises immediately and maps to exit 3, instead of silently pulling ~600MB in the middle
of a run.

`video_frames.py` needs only `ffmpeg`/`ffprobe` (no torch) — already at `/opt/homebrew/bin`.

## `clip_shortlist.py` is the ONLY script that needs the pinned interpreter

Bare `python3` may resolve to the torch-less venv; CLIP then falls back silently and is
never used at all. So pin it — for this one script:

```bash
"${FIND_MEDIA_PY:-/Library/Frameworks/Python.framework/Versions/3.10/bin/python3}" \
  .claude/skills/find-media/scripts/clip_shortlist.py --help
```

Override with `export FIND_MEDIA_PY=/path/to/torch-python` if the Framework python moves.

**Every other script in this skill is stdlib-only and runs under plain `python3`** —
`video_frames.py` (which only shells out to ffmpeg), `validate_queries.py`,
`tier_format_check.py`, `dedup_tracker.py`, `apply_retags.py`, plus the `scene_semantics.py`
module they import. Pinning them is harmless but pointless; writing `$FIND_MEDIA_PY` in
front of `video_frames.py` just makes the command look like it needs torch, which it does
not. There is no `$VALIDATE_PY` — nothing in this skill defines or reads such a variable.

## Evidence lives under the game, never `/tmp`

All frames, sheets and strips go to `games/<game>/.find-media/evidence/<item>/`.
`/tmp` gets wiped mid-session — that happened twice in one session and took the
candidate pool with it both times. The layout:

```
games/<game>/.find-media/evidence/<item>/
├── candidates/        # raw downloads: .gif .mp4 .webm .jpg …
├── frames/            # rep stills `<stem>.jpg` (feed CLIP) + batch strips `<stem>_strip.jpg`
├── contact_sheet.jpg  # the labeled sheet you Read
└── strip_<id>.jpg     # frame strip from a single-clip `--video` + `--out` run
```

(The flag that writes the sheet is still `--montage-out`. An older run dir may hold the
same artifact under its old names, `montage_shortlist.jpg` / `montage_cull.jpg`.)

## `video_frames.py` — rep frames and strips

ffmpeg only. An animated clip has no meaningful poster frame, so one must be chosen:
`--mode rep` samples N frames across the middle of the loop and keeps the **median by
file size**, which skips black frames and seams (they are tiny and sort to the bottom).

```bash
# rep: one representative still per candidate → feeds CLIP
python3 .claude/skills/find-media/scripts/video_frames.py \
  --videos-dir games/<game>/.find-media/evidence/<item>/candidates \
  --mode rep --frames 3 \
  --out-dir games/<game>/.find-media/evidence/<item>/frames --json

# strip: act-verification strip for a finalist → you Read it to confirm the act HOLDS
python3 .claude/skills/find-media/scripts/video_frames.py \
  --video games/<game>/.find-media/evidence/<item>/candidates/03_10941841.gif \
  --mode strip --frames 4 \
  --out games/<game>/.find-media/evidence/<item>/strip_10941841.jpg

# batch strip: one strip per animated option, so a whole shelf costs one shell call
python3 .claude/skills/find-media/scripts/video_frames.py \
  --videos-dir games/<game>/.find-media/evidence/<item>/candidates \
  --mode strip --frames 4 \
  --out-dir games/<game>/.find-media/evidence/<item>/frames --json
```

- `--videos-dir` batch mode supports **both modes**, and the out-names differ so one
  out-dir can hold both (`video_frames.py:289`): `--mode rep` writes `<stem>.jpg`
  (`03_10941841.gif` → `03_10941841.jpg`, id intact), `--mode strip` writes
  `<stem>_strip.jpg`. Batch strip is the cheap way to strip a whole shelf — one call
  instead of one round-trip per option.
- **A multi-frame strip supersedes any single verify frame.** A poster frame is one
  instant of a loop and the loop is what ships. In two rounds this session the strip
  killed 3 of 5 and 4 of 6 shortlisted candidates — including a thumbnail that read as a
  perfect cluttered back room whose loop was standing kissing with no blowjob at all, and
  a "dark outdoor" thumbnail whose loop was a bright daytime laundromat.
- Run the strip on **every ANIMATED finalist** (`.webm` / `.mp4` / `.gif`), not just the
  doubtful ones — top 6 by rank, per SKILL.md §Mode. A static `.jpg` finalist (location,
  clothing, profile photo) has no frames to strip and is judged from the contact sheet
  instead; that is the whole exception, and it is not a licence to skip an animated one.
  Traits that carry heat are duration traits: eye contact has to hold across the whole
  strip, and two candidates died on wandering eyes a lucky thumbnail hid. Bump
  `--frames 6` when the pick rests on affect or gaze rather than on the act.
- A frame under 500 bytes counts as failure and reports `no_frame:<name>`
  (`MIN_FRAME_BYTES`, `video_frames.py:46`). That threshold is about *extracted frames*
  only — it is not the fetch-sanity floor (1024 B, and discard HTML bytes) and not the
  pre-install gate (`tier_format_check.py`: images ≥ 1024 B, animated ≥ 51200 B).
- A whole batch of `no_frame:` means the **fetch** was refused or empty, not that the clips
  are bad: check the bytes on disk for an HTML error page saved under a media name. It will
  not be a phncdn refusal, because phncdn urls are never queued — PornHub is discovery-only
  (`egl.phncdn.com/gif/<id>.gif` returns 470 on clearnet and over Tor, and the real media
  url is signed, time-limited and IP-locked). Read those results for vocabulary, never for
  a file.

## `clip_shortlist.py` — build the contact sheet

Ranks a candidate set against a caption → ranked JSON on stdout + a labeled top-K sheet.

```bash
"${FIND_MEDIA_PY:-/Library/Frameworks/Python.framework/Versions/3.10/bin/python3}" \
  .claude/skills/find-media/scripts/clip_shortlist.py \
  --candidates-dir games/<game>/.find-media/evidence/<item>/frames \
  --caption "<top validated query>" --top-k 12 --grid-cols 4 --item-id <item> \
  --montage-out games/<game>/.find-media/evidence/<item>/contact_sheet.jpg --json
```

(That is `wide`, the NSFW-canvas default. `--top-k` is the mode's option count and nothing
else: `fill` 6 → `--grid-cols 3`, `wide` 12 → `--grid-cols 4`, `deep` 18 → `--grid-cols 6`.
The counts live in SKILL.md §Mode; the column widths are only layout.)

- Inputs: `--candidates-dir <dir>` (ranks every `.jpg/.jpeg/.png/.webp`) **or**
  `--manifest <candidates.jsonl>` (records with `path`/`thumbnail_path`/`frame_path`
  + optional `id`/`title`).
- `--top-k` sets the tile count. **Set it to the mode's option count** (SKILL.md §Mode —
  6 / 12 / 18), so the sheet shows the whole shelf and nothing sits on it unseen. By JUDGE
  the options are already stocked, so this number is purely how many you *look at*; sizing
  it under the shelf is the only way to ship an option no eye ever landed on.
- Output JSON lists **all** candidates ranked: `[{rank,id,path,score,montage_label}]`.
  `montage_label` is the tile letter (A,B,C…) for the top-K, else `null`. Map a tile
  letter back to its candidate id — and thence to its source URL — through that field.
- **Do ONE Read on the sheet**, judge the tiles by eye against the rubric, strip-verify the
  animated survivors, then install the best guess. **JUDGE does not stock** — everything on
  this sheet went into the option store back in STOCK, which is exactly why the runner-ups
  are still alive to be looked at. CLIP scores are advisory ordering only; rank 1 has no
  standing over rank 6, and there is no score at which a candidate accepts itself.

## The sheet is evidence, not a decision

Contact sheets and strips are durable artifacts under `evidence/<item>/`. They survive a
crash, are viewable on resume, and let a human audit what the shelf was picked from —
which is the point now that the human is the decider. A sheet with the mode's full option
count live on it is the deliverable's receipt.

## Fallback contract (never crash a run)

Both scripts exit **3** when their deps/model are unavailable (`clip_shortlist.py`:
torch/transformers/PIL missing or model not cached; `video_frames.py`: ffmpeg/ffprobe
absent). On exit 3, print the notice and **degrade to looking at thumbnails directly** —
the run continues, it just costs more tokens. "CLIP off" is the same skill, slower. Treat
this as the general convention for every optional tool here: **exit 3 means degrade, not
abort.** Nothing optional is allowed to fail a run.

## Auto-accept stays OFF — permanently

A CLIP top-1 shipped with no human look would remove easy SFW items from review
entirely. It is **not** enabled and should not be built. Two reasons, and the second one
is now structural: the per-pool SFW calibration was never run, so 60% top-1 means ~2 in 5
auto-accepts would be wrong; and the deliverable is a stocked shelf for a human to flip
through, which a silent auto-pick defeats by definition. Every slot gets an installed
best guess **and** its options, and every option was looked at.

There is likewise no accept threshold to fall back on: no score a candidate can clear on
its own, no minimum, no below-the-bar bucket. Candidates get ranked and stocked; the human
decides.
