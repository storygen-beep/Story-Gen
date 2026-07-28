# media_lab_c — RUN BRIEF (skill: `find-media`)

**Run the FULL skill.** Gates + frame strip **+ Stage C ranking** (HEAT 60 / SETTING 25 /
CRAFT 15, the bands, the dead-clip veto). Rank the survivors and install the top-ranked pick.

This is the **arm-A replication**, re-run in a cloud session to measure the full skill's cost
independently of the local machine.

**Read `.claude/skills/find-media/SKILL.md` and follow it**, minus SEARCH (see below).

**Use strip BOARDS, not one strip at a time** — `video_frames.py --videos-dir … --mode strip
--board …`. This was silently missing from the skill until 2026-07-29 and its absence tripled
JUDGE cost on a previous run. One board = six candidates, four frames each.

## Before you touch anything — start the API

Every step below talks to the Django dev server. Nothing works without it.

```bash
cd story_gen_django
source venv/bin/activate                  # create it + pip install -r requirements.txt if absent
python manage.py runserver 8000 --noreload &
curl -s "http://localhost:8000/api/v1/dev/game-review/load?game=media_lab_c" | head -c 200
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
  --game media_lab_c --file scenes/lab_eyecontact_t5.webm \
  --want "<slug keywords from the beat>" --avoid "<slug keywords to penalise>" \
  --top 8 --out-dir games/media_lab_c/.find-media/evidence/lab_eyecontact_t5/candidates
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
  `python manage.py package_from_toml --file games/media_lab_c/toml_phases/7_final_game.toml --output games/media_lab_c/output --video-folder games/media_lab_c/videos`

## Compare against

- `games/media_lab/` — arm A, local, 2026-07-27 (~81 min, ~20 image reads)
- `games/media_lab_b/` — arm B, local, run 2 with boards, 2026-07-29 (11.4 min end-to-end, 14 image reads, 10/10 installed)
- Full write-up: `games/media_lab_b/AB_RESULT.md`
