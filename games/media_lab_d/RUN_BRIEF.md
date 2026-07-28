# media_lab_d — RUN BRIEF (skill: `find-media-b`)

**Run the CRIPPLED arm.** Gates + frame strip and **nothing else**. No HEAT/SETTING/CRAFT, no
bands, no dead-clip veto, no ranking. Read the strip board top-to-bottom and **install the
topmost row that passes**, then stop judging that slot. Rows below it are `not_examined`.

This is the **arm-B replication**, re-run in a cloud session to measure the crippled arm's cost
independently of the local machine.

**Read `.claude/skills/find-media-b/SKILL.md` first** — it delegates to `find-media` with
exactly two documented overrides — minus SEARCH (see below).

## Before you touch anything — start the API

Every step below talks to the Django dev server. Nothing works without it.

```bash
cd story_gen_django
source venv/bin/activate                  # create it + pip install -r requirements.txt if absent
python manage.py runserver 8000 --noreload &
curl -s "http://localhost:8000/api/v1/dev/game-review/load?game=media_lab_d" | head -c 200
```

That last call must return JSON with **10 missing_media entries**. If it 404s, check the
trailing slash (there must be none on `load`).

## ⚠️ Do NOT run the SEARCH phase

`find-media`'s only retrieval route is Google Images driven through the user's own Chrome
(`claude-in-chrome` MCP). **A cloud session has no Chrome to drive**, and `WebSearch` is a
documented dead end for this. So SEARCH is out of scope here.

It doesn't need to run: `.find-media/media_options.json` is **pre-stocked with the identical
1352-candidate shelf** that `media_lab` and `media_lab_b` were judged from. That is deliberate —
all four games judge the same pool, so the only variable is the skill.

Start at **JUDGE**. Fetch bytes from the stocked shelf with the skill's own fetcher:

```bash
python3 .claude/skills/find-media/scripts/fetch_candidates.py \
  --game media_lab_d --file scenes/lab_eyecontact_t5.webm \
  --want "<slug keywords from the beat>" --avoid "<slug keywords to penalise>" \
  --top 8 --out-dir games/media_lab_d/.find-media/evidence/lab_eyecontact_t5/candidates
```

## Report these numbers when you finish

The point of this run is **performance**, so record them as you go — they cannot be
reconstructed afterwards:

| metric | how to get it |
|---|---|
| wall-clock, first fetch → last install | `date '+%H:%M:%S'` at both ends |
| **image reads** (contact sheets + boards + any single strips) | count them; this is the real cost driver |
| candidates examined / gate rejects | from `scores.jsonl` |
| slots installed | `game-review/load` must end at **0 missing** |

## Rules

- **Never run `scripts/merge_toml_phases.py` here.** Its `OUTPUT_FILENAME` is
  `7_final_game.toml`, so it would overwrite this hand-written file with an empty one.
- **Never edit the slots, descriptions or `search_queries`.** They are byte-identical across
  all four media_lab games and are the experiment's constants.
- The study key (which three slots carry deliberately old-style queries) is in
  `games/media_lab/STUDY_KEY_do_not_read_before_hunting.md` — do not read it before judging.
- Package when done:
  `python manage.py package_from_toml --file games/media_lab_d/toml_phases/7_final_game.toml --output games/media_lab_d/output --video-folder games/media_lab_d/videos`

## Compare against

- `games/media_lab/` — arm A, local, 2026-07-27 (~81 min, ~20 image reads)
- `games/media_lab_b/` — arm B, local, run 2 with boards, 2026-07-29 (11.4 min end-to-end, 14 image reads, 10/10 installed)
- Full write-up: `games/media_lab_b/AB_RESULT.md`
