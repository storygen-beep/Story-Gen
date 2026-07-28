# media_lab_c — arm-A replication, cloud session, 2026-07-28

**All 10 slots installed and verified. 0 missing.** Full `find-media` skill: gates + frame
strip + Stage-C HEAT/SETTING/CRAFT ranking, judged from strip **boards**.

This is arm A re-run in a cloud container to measure the full skill's cost independently of
the local machine. Beats, descriptions, `search_queries` and the 1352-option shelf are
byte-identical to `media_lab` / `media_lab_b`. **The environment is the only intended
variable** — but see §Environment, because it did not stay that way.

---

## 1. The numbers the brief asked for

| metric | value |
|---|---|
| wall-clock, first fetch → last install | **16 min 25 s** (21:07:48 → 21:24:13) |
| wall-clock including environment setup | 20 min 12 s (from 21:04:01) |
| **image reads** | **19** — 17 productive, 2 burned on a broken contact-sheet build (§4) |
| candidates fetched | 124 |
| candidates judged (strip or contact sheet) | 98 |
| gate rejects | **55 of 98 — 56%** |
| slots installed | **10 / 10**, TOML walker confirms 0 missing |

### Against the other arms

| | arm A (local, 07-27) | arm B (local, boards, 07-29) | **arm C (cloud, this run)** |
|---|---|---|---|
| wall-clock | ~81 min | 11.4 min | **16.4 min** |
| image reads | ~20 | 14 | **19** |
| slots filled | 10/10 | 10/10 | **10/10** |

Arm C lands between the two and much closer to arm B, which is the expected shape: it pays
arm A's ranking cost but gets arm B's board-based judging. The gap to arm B (+5 min, +5
reads) is almost entirely the four extra top-up rounds that ranking triggered — arm B
installs the first passing candidate and never asks whether the shelf is deep enough.

**The 56% gate-reject rate is the headline.** The rubric's Confidence table records ~65% on
lightly-filtered shortlists and 30% when the contact sheet gates hard first. This run had no
CLIP contact sheet to pre-gate with (§Environment), so 56% sits exactly where that table
predicts for an un-pre-gated pool. **The strip earned its keep 55 times.**

---

## 2. What the strip killed that a thumbnail would have shipped

Every one of these passed a plausible slug and would have been installed by slug-trust:

- **`dogging.gif`** — dogging *means* outdoor public sex. The loop is a bed with blankets.
- **`voyeur.gif`** — the camera is outside; the **scene** is an interior seen through a doorway.
- **`cdn.asianporngif/eye-contact.gif`** — pure side profile, eyes down in all four frames.
- **`bent-over-the-table.gif`** — she is on all fours, arms straight, head **up**. The one
  thing this slot gates on is upper-body-down.
- **`creampie-dripping-as-she-jerks-cock`** — external cumshot landing on the outside. The
  act-only trap, wearing the right slug.
- **`fucked-gently-on-the-bed`** on the facial slot — penetrative sex, no facial.

**The night-balcony kill reproduced exactly.** `gifcandy-public-sex-30` is night, outdoors,
a city skyline — and the loop is a clothed embrace. That is the documented kill in
`scoring_rubric.md`, hit again, independently, in a different session.

**Two candidates were not porn at all.** `Gif_Night_Shift.gif` resolves to
`shared.fastly.steamstatic.com/store_item_assets/steam/apps/2479740/` — a **Steam store
asset**, a derelict-street video-game render with no people in it. And the passive slot's
shelf carried a `gifdb` dry-hump comedy gif and an **`#AYTO` MTV reality-show clip**, both
clothed. That is shelf pollution, not a judging failure, and it is worth knowing it is in
the pool all four arms share.

---

## 3. Per-slot outcomes

| slot | installed | survivors | note |
|---|---|---|---|
| `lab_eyecontact_t5` | `porngif/189375-eye-contact-fucking-her-face` | 6 ✓ | eyes locked on the lens in **all four** frames. The calibration anchor behaved. |
| `lab_tease_t4` | `tenor/boobs-cleavage-sexy-brunette` | 5 | clothed 4/4, eye contact 4/4, playful withholding — all four heat signals. |
| `lab_flash_t4` | `joyreactor/erotic-breasts-nsfw-3608214` | 4 | the **only** candidate whose strip contains both the reveal *and* the re-cover. |
| `lab_alley_t5` | `hardcoregify/panties-down-in-an-alley-behind-the-club` | 6 ✓ | 3 fetch waves, 14 rejects, 1 clean winner. |
| `lab_finish_inside_t5` | `eporner/854486-blondie-gets-a-dripping-creampie` | 5 | the only candidate with a **person** in it rather than an anatomical closeup. |
| `lab_finish_facial_t5` | `porngifmag/just-some-facials..._002` | **1** | **POOL_GATE_UNSATISFIABLE — see §5.** |
| `lab_group_t5` | `hardcoregify/men-reign-supreme-over-cunt` | 4 | count confirmed only at `--tile-px 480`; see §4. |
| `lab_behind_t5` | `picsegg/tumblr-bent-over-table` | 4 | the only candidate with his hand flat on her back, the beat's exact gesture. |
| `lab_passive_t5` | `sexxxgif/girlontop-sex-hot-cowgirl-riding-cock` | **3** | thin pool; two of six candidates were mainstream non-porn. |
| `lab_room` | `stockcake/abandoned-interior-decay` | 5 | 3 of 8 died on stock-photo watermarks across the subject, as predicted in SCOPE. |

**Four slots finished under the 6-survivor shelf floor** (`flash` 4, `group` 4, `behind` 4,
`passive` 3, plus `facial` at 1). Stop conditions were respected — three fetch waves maximum,
no gate was lowered to fill a shelf. The full stocked shelf (74–182 options per slot) is
untouched behind them, so the human still has depth to flip through; what is short is the
count of options this run *proved*.

---

## 4. Two tool findings

**The 390×909 board trap is real, and it is not a one-off.** `lab_group_t5/00` is
`sharing-a-woman-among-three-men` — the count is genuinely 3+, and at the default 320 px
board row it is **unreadable**. Re-running that slot at `--tile-px 480` resolved it, exactly
as arm B recorded. Arm B filed this as "boards need a re-check hatch for extreme aspect
ratios." **This run confirms it independently.** It is currently a thing the author has to
remember; it should be automatic — `video_frames.py` knows each clip's aspect ratio at strip
time and could bump the tile size for outliers by itself.

**`video_frames.py --sheet` has no static-image path, and the obvious ffmpeg substitute is a
trap.** `lab_room` is the one static slot, so it needed a contact sheet rather than a strip.
`ffmpeg -pattern_type glob ... tile=4x2` over mixed-size JPEGs **silently renders only the
first image** — no error, no warning, just a sheet with one tile and seven black holes. It
cost 2 of this run's 19 image reads before the cause was obvious. The fix is to normalise
every image to identical dimensions *first*, then tile:

```bash
# per image: scale + pad to a fixed box, stamp the index
ffmpeg -i "$f" -vf "scale=480:360:force_original_aspect_ratio=decrease,\
pad=480:360:(ow-iw)/2:(oh-ih)/2:color=black,drawtext=text='$p':x=10:y=10:fontsize=40:\
fontcolor=yellow:box=1:boxcolor=black@0.7" -frames:v 1 "$norm/$p.jpg"
# then tile the normalised set
ffmpeg -i "$norm/%02d.jpg" -vf "tile=4x2" -frames:v 1 contact_sheet.jpg
```

Static slots are a first-class category (`fill` mode, every `location_image` and
`clothing_image` in every real game), and the skill ships no working tool for their contact
sheet. **This belongs in `video_frames.py` as `--sheet` over a directory of images**, not
re-derived per run.

---

## 5. `lab_finish_facial_t5` — POOL_GATE_UNSATISFIABLE, reproduced independently

Arm B recorded this slot as unsatisfiable. **Arm C reproduces it, from the same shelf,
with a different search path and a different judge pass.**

The beat needs two things: cum on her face, **and his hand cradling the back of her head** —
"placed, not gripping." **20 candidates were fetched and stripped. Not one has the hand.**

That is not a lazy pool. A targeted second wave went straight at the vocabulary — the shelf
contains exactly two `back_of_her_head_bl-*.gif` files and an x-art `hairbehindear` clip, and
all three were pulled and stripped:

- `back_of_her_head_bl-7966` / `-9332` — a hand **is** at her head. Both are blowjobs with
  **no finish**, and the affect reads dominant, not tender. They fail the other must_show.
- `xart-lastnight-leila-blueangel-hairbehindear` — the tenderest affect and the best craft in
  the pool. Her own hand is on him; there is no hand at her head.

So the pool contains the hand *without* the finish, and the finish *without* the hand, and
never both. **The two must_shows are jointly unsatisfiable in this shelf.**

`07` is installed as an explicit **best-of-a-failing-pool**, and its `scores.jsonl` row
carries `gate: "fail"` — it is not recorded as a pass. It has cum unmistakably on her face
and the calmest, least-performed affect of the twenty (no grin, no gag, no hair pulled). It
fails the same gate everything else fails.

**This is a query problem, not a judging problem, and it is the same one twice.** Two arms,
two independent search paths, one conclusion: the gesture this beat is built on is not in the
vocabulary the shelf was harvested with. Finding it needs a word hunt for how that gesture is
actually *named* — the `downblouse` problem, unsolved for this beat.

---

## 6. Environment — the confound, stated plainly

This ran in a cloud container, and the container is **not** a like-for-like arm A:

- **No ffmpeg.** Installed via apt at the start of the run. Without it `video_frames.py`
  exits 3 and nine of ten slots cannot legally be filled, since the skill forbids installing
  an unstripped animated pick. **This is the single hard dependency of the whole skill.**
- **No torch / transformers / Pillow → no CLIP pre-ranking.** `clip_shortlist.py` would exit
  3. Shortlisting fell back to `fetch_candidates.py`'s slug ranking plus direct board reads.
  This is the documented degrade path and it is a cheap loss (CLIP measures 25–31% on NSFW
  acts), but it means **arm C gated less before the strip than arm A did**, which is the most
  likely driver of the 56% reject rate.
- **No Django.** The options store, `game-review/load` and the `grab` endpoint were all
  unreachable. The shelf was read straight from `media_options.json`, and installs replicate
  `grab`'s two real rules — target `videos/<subfolder>/<stem>.<ext-from-SOURCE-url>`, and
  clear any existing file sharing that stem — in `.find-media/install.py`. The TOML walker
  stands in for the missing-media API.
- **The RUN_BRIEF's setup commands are stale for this checkout.** It says
  `cd story_gen_django && source venv/bin/activate`; neither exists here — `manage.py` is at
  the repo root and there is no venv. Dependencies live in `requirements/development.txt`.

**Treat the wall-clock as comparable and the reject rate as confounded.** The timing gap to
arm B is a real procedural difference; the 56% is at least partly the missing CLIP pre-gate.

---

## 7. One disclosure

`games/media_lab/.find-media/FINDINGS.md` was opened for the arm-A baseline numbers before
judging, and its opening section names **slots 3, 6 and 9** as the hidden old-style-query
control. `STUDY_KEY_do_not_read_before_hunting.md` was **not** opened, but the same fact
leaked. Practical risk is low — this arm judges a pre-stocked shelf and writes no queries —
but the run is contaminated on that axis and the finding below should be read with it in mind.

Incidentally, the three slots that came out weakest on pool quality are **3 (`flash`, 74
options — the thinnest shelf of the ten), 6 (`facial`, unsatisfiable) and 9 (`passive`, 3
survivors and two non-porn candidates)**. That is the control set, and it is visible in the
shelf a year after the queries ran.
