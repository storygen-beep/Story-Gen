# media_lab_d — arm-B replication result (cloud session, 2026-07-28)

Ran `find-media-b` — gates + frame strip only, no HEAT/SETTING/CRAFT, no bands, no
dead-clip veto, no ranking. Read each strip board top to bottom, installed the topmost row
that passed, marked everything below it `not_examined`.

## Headline numbers

| metric | value |
|---|---|
| wall-clock, first fetch → last install | **17m09s** (21:08:39 → 21:25:48) |
| **image reads** | **32** (17 boards/sheets + 15 single-clip re-checks) |
| candidates fetched | 104 |
| candidates examined | 54 |
| gate rejects | 44 |
| slots installed | **10 / 10** — `game-review/load` reports 0 missing |
| package | 0 failed, 31,547,372 bytes copied |

Comparison points, from `RUN_BRIEF.md`:

| run | wall-clock | image reads | installed |
|---|---|---|---|
| `media_lab` (arm A, local, 2026-07-27) | ~81 min | ~20 | 10/10 |
| `media_lab_b` (arm B, local, boards, 2026-07-29) | 11.4 min | 14 | 10/10 |
| **`media_lab_d` (arm B, cloud, this run)** | **17m09s** | **32** | **10/10** |

## Where the 32 reads went

17 were boards or contact sheets — one per wave per slot, which is the intended cost.
The other **15 were single-clip re-checks** at 5–6 frames, taken after the board because a
4-frame board tile could not settle a gate. They cluster exactly where the gate is about
something small in the frame:

- **gaze** (`lab_eyecontact_t5`) — 2 re-checks. Whether eye contact *holds* is invisible at
  board resolution; the board tile for candidate 00 read as held contact and the 6-frame
  re-strip showed it breaking twice.
- **affect** (`lab_finish_facial_t5`) — 2 re-checks hunting a hand at her head.
- **setting** (`lab_alley_t5`) — 2 re-checks, dark clips where "is there a wall" needed size.
- **position/partner** (`lab_passive_t5`) — 3 re-checks, including one 2-frame strip purely
  for pixels.

The board is right for coarse gates (interior vs alley, one man vs three, clothed vs not) and
under-resolved for fine ones (a gaze, a hand, who is lying down). That is the honest reason
this run cost 32 reads against arm B's 14, not a procedural slip — the 4-frame board was read
first in every single case.

## Two results worth keeping

**1. `lab_finish_facial_t5` is `pool_all_dead`.** 24 candidates across 3 fetch waves, every one
rejected on the same item: *his hand gentle at her head*. In every clip in this shelf the man's
hand is on his own cock — the standard framing for the act. 10 of the 24 additionally tripped
the "bright grinning performer" avoid. Installed the least-bad by the arm's own ordering (the
topmost candidate failing exactly one gate and tripping no avoid) and flagged it in
`scores.jsonl` and the manifest. The slot has a working file and it is **not** a correct pick.

**2. Two installs are correct and visibly rough** — precisely what removing question 2 predicts:

- `lab_group_t5` is a **3-panel stacked collage**. Every panel shows one woman with three men
  in frame simultaneously, so the count gate passes cleanly. A ranker would have called the
  collage format out; this arm has no axis for it.
- `lab_room.jpg` carries a **large diagonal Alamy watermark**. Interior, no people, heavy
  visible wear — all three must_show items pass. A watermark is a craft property, and craft is
  exactly what this arm deleted.

Both are gate-correct installs that an aesthetic pass would likely have replaced. They are the
arm's cost, recorded rather than fixed.

## Slot-by-slot

| slot | examined | rejects | first pass at |
|---|---|---|---|
| `lab_eyecontact_t5` | 6 | 5 | row 05 |
| `lab_tease_t4` | 5 | 4 | row 04 |
| `lab_flash_t4` | 2 | 1 | row 01 |
| `lab_alley_t5` | 10 | 9 | row 09 (wave 2 — wave 1 was a clean sweep) |
| `lab_finish_inside_t5` | 1 | 0 | row 00 |
| `lab_finish_facial_t5` | 24 | 23 | **none** — least-bad installed |
| `lab_group_t5` | 1 | 0 | row 00 |
| `lab_behind_t5` | 2 | 1 | row 01 |
| `lab_passive_t5` | 2 | 1 | row 01 |
| `lab_room` | 1 | 0 | row 00 (contact sheet — static, no strip) |

Three slots passed on the very first candidate. Two slots (`lab_alley_t5`, `lab_finish_facial_t5`)
burned a whole wave or more before anything passed, and both are slots where the gate is a
*property of the world* rather than of the act — night-and-a-wall, and a specific gesture.

## Method notes

- **SEARCH was not run**, per `RUN_BRIEF.md` — a cloud session has no Chrome to drive. All
  judging came off the pre-stocked 1352-candidate shelf shared with `media_lab` and
  `media_lab_b`, so the shelf is a constant across arms.
- Fetch order is `fetch_candidates.py` slug rank, which is deterministic and identical to what
  the other arms walked.
- Arm A's `scores.jsonl` and installed picks were not read at any point during this run.
- CLIP pre-ranking was unavailable (no torch/PIL in this container) and was **not needed** —
  arm B reads strip boards, and `fetch_candidates.py` already supplies the deterministic order.
- ffmpeg had to be installed (`apt-get update` first — the image ships a stale package index
  that 404s), and Django needed `django djangorestframework djangorestframework-simplejwt
  drf-spectacular python-decouple django-cors-headers psycopg2-binary django-filter pgvector
  pillow openai tomli`. `RUN_BRIEF.md` says to `cd story_gen_django` — that directory does not
  exist in this checkout; `manage.py` is at the repo root.
- The dev server needs `DB_ENGINE=django.db.backends.sqlite3`. Under the default postgres
  engine, `runserver`'s migration check hits an infinite recursion in
  `apps/stories/migrations/0001_initial.py:13` — `_array_or_json` calls itself on the
  postgresql branch instead of returning an `ArrayField`. Pre-existing, unrelated to this run,
  and left untouched.

## Evidence

`games/media_lab_d/.find-media/`
- `run_manifest.json` — totals, per-slot status, installed URLs
- `evidence/<slot>/scores.jsonl` — every candidate with its gate verdict and reason
- `evidence/<slot>/board*.jpg` — the strip boards actually read
- `evidence/<slot>/recheck_*.jpg` — the 15 single-clip re-checks
