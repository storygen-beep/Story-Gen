# Contact sheets and strip boards — how JUDGE actually looks

Read this when building the image JUDGE reads: the **contact sheet** (one representative
frame per candidate, tiled) or the **strip board** (one whole 4-frame loop per candidate,
stacked). Both come out of `video_frames.py`, both are ffmpeg-only.

## Who does the looking

**You do. There is no model in this loop.**

ffmpeg's entire job is to **cut, resize, label and glue**. It extracts frames, pads them to a
common size, burns the candidate index on, and stacks them into one JPEG. It does not detect,
classify, score or rank anything.

Every judgement — *"three or more men visible simultaneously"*, *"her eyes up at the viewer in
every frame"*, *"his hand flat on her back"* — is made by **reading the assembled image**. No
person-detector, no gaze tracker, no aesthetic model.

Three consequences that matter:

- **Tile order carries no claim.** The sheet and the board are in `fetch_candidates.py` order
  (slug keyword rank). That is a stable index so a verdict can name "row 08" and map straight
  back to `08.gif` and to `manifest.json` — it is **not** a quality ordering, and tile 1 has no
  standing over tile 6.
- **The written reason IS the verification mechanism.** Nothing can be re-run to check a call,
  so every rejection gets a named `gate_reason` in `scores.jsonl` — `eye_contact:eyes_down_frame2`,
  `posture:man_seated_not_standing`. The board is the exhibit; the reason is the argument. A
  gate call with no reason recorded is unauditable and therefore worthless.
- **Repeatability is a property of the checklist, not the tool.** Measured 2026-07-29: the same
  ten slots re-judged from boards reproduced **10/10 of the previous run's picks**. That is the
  evidence the gates are stable — it comes from the `must_show`/`avoid` lists being concrete,
  not from anything ffmpeg did.

> **History.** This skill used to ship `clip_shortlist.py`, a local CLIP model meant to pre-rank
> the tiles. It was deleted 2026-07-29: it had never run in any recorded run, its own header
> called its numbers "Demo evidence", and it scored **25–31% on explicit acts** — the primary
> content here. It was also the skill's only non-stdlib dependency. Do not reintroduce a
> pre-ranking model without measuring it on this repo's own slots first.

## Why one image and not fifteen thumbnails

A slot stocks 6 / 12 / 18 options depending on mode (SKILL.md §Mode). Viewing those one at a
time cost a real run ~5–8 thumbnail reads *per item* — on the order of 0.5–1M tokens per game
spent purely looking.

Measured again 2026-07-28/29, on the identical candidate files: reading strips **one at a time
took 52 image reads; reading boards took 14**, for identical verdicts. One assembled image per
batch is the only thing that scales, and forgetting it triples JUDGE for nothing.

## Input contract — the candidate pool is MIXED

The Chrome route returns `.gif` as often as `.mp4`/`.webm`, plus ordinary stills. One rule
covers it:

| Input | `--mode rep` | `--mode strip` |
|---|---|---|
| `.gif` `.webm` `.mp4` `.mov` `.mkv` | a representative frame is extracted | 4 frames across the loop |
| `.jpg` `.jpeg` `.png` `.webp` | **the still IS its own rep frame** | **refused** — no loop to make a claim about |

A still cannot be stripped, and that is not an oversight: a strip is a claim about a *loop*.
Static finalists (location, clothing, profile photo) are judged from the contact sheet, and that
is the whole exception.

Name candidate files `<i>_<id>.<ext>` or plain `<i>.<ext>`. The burned-in label is the stem up
to the first `_`, so the index survives frame extraction and maps back to the option-store URL.

## `video_frames.py` — the only tool here

ffmpeg only, stdlib Python. An animated clip has no meaningful poster frame, so one must be
chosen: `--mode rep` samples N frames across the middle of the loop and keeps the **median by
file size**, which skips black frames and seams (they are tiny and sort to the bottom).

```bash
# CONTACT SHEET — one rep frame per candidate, tiled and numbered. Read this ONE image.
python3 .claude/skills/find-media/scripts/video_frames.py \
  --videos-dir games/<game>/.find-media/evidence/<item>/candidates \
  --mode rep --out-dir games/<game>/.find-media/evidence/<item>/frames \
  --sheet games/<game>/.find-media/evidence/<item>/contact_sheet.jpg --sheet-cols 4

# STRIP BOARD — one whole 4-frame loop per candidate, stacked. Read this ONE image.
python3 .claude/skills/find-media/scripts/video_frames.py \
  --videos-dir games/<game>/.find-media/evidence/<item>/candidates \
  --mode strip --frames 4 \
  --out-dir games/<game>/.find-media/evidence/<item>/strips \
  --board games/<game>/.find-media/evidence/<item>/board.jpg

# SINGLE CANDIDATE — only to re-check one you already judged from the board.
python3 .claude/skills/find-media/scripts/video_frames.py \
  --video games/<game>/.find-media/evidence/<item>/candidates/03.gif \
  --mode strip --frames 4 \
  --out games/<game>/.find-media/evidence/<item>/strip_03.jpg
```

- **Boards hold 6 rows** (`--board-rows`), 4 frames each at 320px = 1280×1920. Beyond six
  candidates it spills to `board_2.jpg`, `board_3.jpg`. That geometry is still ~260px per frame
  after the reader's downscale — enough to call eye contact.
- **Guards:** `--sheet` requires `--videos-dir --mode rep`; `--board` requires
  `--videos-dir --mode strip`. Either mismatch exits 2.
- **Out-names differ so one out-dir can hold both:** `--mode rep` writes `<stem>.jpg`,
  `--mode strip` writes `<stem>_strip.jpg`.
- **A multi-frame strip supersedes any single frame.** A poster frame is one instant; the loop
  is what ships. The strip killed **3 of 5** shortlisted candidates in one round and **4 of 6**
  in the next — including a thumbnail that read as a perfect cluttered back room whose loop was
  standing kissing with no blowjob in it, and a "dark outdoor" thumbnail whose loop was a bright
  daytime laundromat.
- Run the strip on **every ANIMATED finalist**, not just the doubtful ones. Traits that carry
  heat are duration traits: eye contact has to hold across the whole strip, and two candidates
  died on wandering eyes a lucky thumbnail hid. Bump `--frames 6` when the pick rests on affect
  or gaze rather than on the act.
- **Extreme aspect ratios need a re-check.** A 390×909 source squeezed into a 320px board row
  was unreadable — the men in a group shot could not be counted. Re-strip that one candidate at
  `--tile-px 480` and read it alone. Found 2026-07-29 on `media_lab_b/lab_group_t5`.
- A frame under 500 bytes counts as failure and reports `no_frame:<name>` (`MIN_FRAME_BYTES`).
  That threshold is about *extracted frames* only — not the fetch-sanity floor (1024 B, discard
  HTML bytes) and not the pre-install gate (`tier_format_check.py`: images ≥ 1024 B, animated
  ≥ 51200 B).
- A whole batch of `no_frame:` means the **fetch** was refused or empty, not that the clips are
  bad: check the bytes on disk for an HTML error page saved under a media name. It will not be a
  phncdn refusal, because phncdn urls are never queued — PornHub is discovery-only
  (`egl.phncdn.com/gif/<id>.gif` returns 470 on clearnet and over Tor, and the real media url is
  signed, time-limited and IP-locked). Read those results for vocabulary, never for a file.

## Evidence lives under the game, never `/tmp`

All frames, sheets, boards and strips go to `games/<game>/.find-media/evidence/<item>/`.
`/tmp` gets wiped mid-session — that happened twice in one session and took the candidate pool
with it both times. The layout:

```
games/<game>/.find-media/evidence/<item>/
├── candidates/        # raw downloads: .gif .mp4 .webm .jpg …
├── frames/            # rep stills `<stem>.jpg`
├── strips/            # per-candidate strips `<stem>_strip.jpg`
├── contact_sheet.jpg  # the labelled sheet you Read
├── board.jpg          # the labelled strip board you Read (board_2.jpg, … on spill)
└── strip_<id>.jpg     # single-clip re-check
```

## The sheet is evidence, not a decision

Sheets, boards and strips are durable artifacts under `evidence/<item>/`. They survive a crash,
are viewable on resume, and let a human audit what the shelf was picked from — which is the
point now that the human is the decider. A sheet with the mode's full option count live on it is
the deliverable's receipt.

**JUDGE does not stock.** Everything on the sheet went into the option store back in STOCK,
which is exactly why the runner-ups are still alive to be looked at.

## Fallback contract (never crash a run)

`video_frames.py` exits **3** when ffmpeg/ffprobe is absent. On exit 3, print the notice and
**degrade to looking at the harvest poster / thumbnails directly** — the run continues, it just
costs more. Treat this as the general convention for every optional tool here: **exit 3 means
degrade, not abort.** Nothing optional is allowed to fail a run.

## Auto-accept stays OFF — permanently

No candidate may be installed without a human-visible artifact behind it, and none may be
accepted by a number. There is **no accept threshold** anywhere in this skill: no score a
candidate clears on its own, no minimum, no below-the-bar bucket. The deliverable is a stocked
shelf for a human to flip through, which a silent auto-pick defeats by definition. Every slot
gets an installed best guess **and** its options, and every option was looked at.
