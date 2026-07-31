# Vesper — media pools across every repeatable sex beat

**Status:** planned, not started. Wave 0 (`sex/mercer_serve_knees_t5`) is DONE and shipped at
book_revision 104.
**Scope:** **20 slots** — 18 pose clips (6 loops × 3 poses) + 2 ambient. 1 done, **19 to run**.
*(An earlier draft said "19 total / 18 to run" — an arithmetic slip; the wave table always summed
to 20. Stage 1 converted 19, which is the correct remainder.)*
**Author's law for this run:** *no slot may reuse another slot's search.* §3 is that rule, its
mechanism, and the three places the current TOML already violates it.

---

## 1. What "the mercer_serve_knees treatment" was

The reference run, rev 103–104. Every wave below repeats it exactly:

1. **Convert** the block from `file = "sex/x_t5.webm"` to `pool_dir = "sex/x_t5"` + `pool = 4`.
2. **Seed before searching** — `git mv` the shipping clip into the new folder as clip 1, so the
   beat never renders a hole and the review API reports "1 of 4" instead of a miss.
3. **Re-key the ledgers** — `check_shelves --repair` (the conversion drops the extension, which
   orphans the verdict).
4. **Merge + build green** *before* a single byte is downloaded — proves the pool renders.
5. **Run find-media** on the slot: SCOPE brief → query plan → Chrome search → stock 12 → frame-strip
   the top 6 → install every gate-survivor up to 4.
6. **Rebuild both artifacts** (free + paid), verify the cycle live in the browser.
7. **Ledger** — `authoring_state.json` entry, book_revision bump.

What it produced: a 4-clip folder cycling `1→2→3→4→1` on `$game_state.media_cycle`, a 140-deep
shelf LO could re-curate from, and — after his re-pick — four clips none of which were mine.
That last part is the point of the shelf.

---

## 2. Why these slots — the structural finding

Vesper has **six structurally identical sex loops**. Verified against `7_final_game.toml`:

```
intro ──(ONE forced choice)──▶ ORAL pose ──┬─▶ self-loop: loop_npc_pleasure += random(8,14)
                                           ├─▶ switch pose (vaginal / anal / desk / glass)
                                           └─▶ elect finisher   (needs pleasure ≥ 50)
```

Two measured facts carry the whole plan:

- **Every pose node re-targets itself**, adding `random(8,14)` against a threshold of 50 — so one
  clip renders **4–6 times inside a single visit**, then again every later visit.
- **Every loop's intro node has exactly one choice, into the oral pose.** You cannot enter a sex
  loop in vesper without watching the oral clip. That makes the six oral clips the
  highest-view-count media in the game, by a wide margin and by construction.

The three gates in `.claude/skills/author-game/references/media.md` §7:

| Gate | Verdict for these slots |
|---|---|
| **1 — NSFW *and* repeatable** | ✅ all `sex/` t5, on repeatable hubs, 4–6 views *per visit* |
| **2 — interchangeable** | ✅ descriptions are loose generic acts, which is what fills a pool |
| **3 — rotate not escalate** | ✅ **strongest pass in the game.** A pose node has no internal state axis — escalation happens by *switching nodes* (`sex_stage` 0/1/2) and by the finisher election. Nothing changes between click 1 and click 5 but the counter. That is what a self-loop *means*. |

---

## 3. ⚠️ THE LAW — every slot gets a FRESH search

> **Every slot's clips must come from a live Chrome Google search run for *that slot*.
> Never recycle a harvest** — not `media_lab`'s, not an earlier run's, not another slot's
> candidate pile, not an existing shelf.

LO's rule, stated 2026-07-31. It is about **where the results come from**, not about
hand-crafting unique wording. A shelf that already holds candidates is *not* a reason to skip
the search; it is extra depth sitting next to a fresh harvest.

### Why it is not optional here

Six of these slots are *kneeling blowjob*. Recycling one harvest across them — or letting the
obvious query stand in for six searches — gives six pools that look like siblings even when the
files differ. Asset-level dedup (`dedup_tracker.py`) does not catch this: it stops the *same
file* landing twice, not six pools drawn from one bucket.

### The current TOML already breaks it — measured

| Collision | Slots | Severity |
|---|---|---|
| `brothel anal from behind red room` **and** `escort anal bent over bed dim` | `brothel_anal_t5` + `marsh_anal_t5` | **2 of 2 queries byte-identical** — worst in the game |
| `office desk sex from behind` | `mercer_serve_desk_t5` + `renner_loop_doggy_t5` | exact |
| `office blowjob kneeling chair` / `office blowjob kneeling desk` | renner + calloway oral | one word apart |
| `brothel blowjob red room pov` / `brothel blowjob kneeling red room pov` | brothel + marsh oral | one word apart |

Token frequency across the 24 authored queries: `room` 14, `dim` 14, `man` 11, `office` 10,
`kneeling` 8, `blowjob` 8, `desk` 8, `behind` 8. **The authored queries are not slot-specific
enough to be run as written.** Rewriting them is a phase of this plan, not a nicety.

### The rule, and the guidance under it

**THE RULE — hard.** One fresh Chrome search per slot. No slot is ever stocked from bytes or URLs
harvested for a different slot, a different game, or a different run. A slot that already has a
shelf still gets its own search.

**The guidance — quality, not law.** Each slot has an **anchor term** (§5) chosen so its grid
lands somewhere its siblings' don't. This is advice in the slot's brief, not a lock — nothing
blocks on it, and a slot whose anchor turns out to be a dead term goes to the word hunt
(`chrome_route.md` §1) rather than borrowing a sibling's.

**Measured, 2026-07-31** — two live searches, same browser, same moment:

| tab | query | urls | what came back |
|---|---|---|---|
| A | `office chair blowjob gif` | 76 | `office-duties`, `sucking-dick-under-desk`, `secretary_under_des`, `clothed_office_blow` |
| B | `storeroom blowjob gif` | 82 | `blowjob-at-the-store`, `you-got-a-store-room-right`, `storage-room`, `a-clerk-who-knows-to-work` |

Zero overlap, no rate-limiting, no CAPTCHA (`detected unusual traffic` false on both). Fresh
searches with distinct anchors do the job, and they do it **in parallel** — see §11.

### 3.1 The enforcement artifact — `query_ledger.jsonl`

New file, created by this plan: `games/vesper/.find-media/query_ledger.jsonl`. One line per query
ever run against this game:

```json
{"slot":"sex/mercer_serve_knees_t5","query":"kneeling blowjob hand in hair gif amateur","date":"2026-07-31","round":1,"source":"google","urls_yielded":54,"status":"burned"}
```

**Procedure, every slot:** append each query as it is run, with its yield. The ledger is a
**record**, not a gate — nothing blocks on it. It exists so the end-of-wave cross-check (§11) can
answer *"did two slots end up drawing the same thing?"* from data instead of memory, and so a
resumed run knows what was already tried.

Seed it with the six already-burned mercer queries — three from the scope brief, two authored, one
PornHub-dialect from the June run:

```
kneeling blowjob hand in hair gif amateur
office blowjob on knees gif
standing over her kneeling blowjob gif real
office floor blowjob hair pull
penthouse kneeling blowjob girl
blowjob+kneeling                              (pornhub dialect, June)
```

**Burned tokens that no later slot may anchor on:** `hand in hair`, `hair pull`, `penthouse`,
`office floor`, `standing over her`.

### 3.2 Result-level isolation — and the hole the law does NOT cover

Distinct queries can still converge on one file. Two cheap checks:

- `python3 .claude/skills/find-media/scripts/dedup_tracker.py --check <id_or_url> --game vesper`
  before every install.
- **No URL may be stocked on two vesper slots.** Check `media_options.json` at stock time; the
  store dedupes per-slot, not across them.

> ### ⚠️ MEASURED 2026-07-31 — the fresh-search law does not prevent duplicate FOOTAGE
>
> Wave 1 obeyed §3 exactly: `renner_loop_oral_t5` searched `office chair` / `under the desk`,
> `calloway_loop_oral_t5` searched `file room` / `after hours` / `secretary working late`.
> Different words, different grids, different hosts. **Both installed the same source video.**
>
> Confirmed visually and numerically: identical glass-top desk and blue cabinets, identical white
> top and burgundy skirt, identical red heels kicked off at the same spot on the floor, identical
> man/watch/chair angle/camera position. Alignment-searched grayscale diff **16.75 mean-abs**
> (unrelated clips run 40–70). The two differ only as *rips*: 590 KB clean vs 1 MB with a
> `gif-porn.net` stamp.
>
> **Nothing in the pipeline could catch it.** Different URLs → URL dedup passes. Different bytes,
> sizes and watermarks → file dedup passes. Each harvest agent sees only its own pile → neither
> could know. Left in, it would have shipped the same woman in the same clothes in the same room
> as **two different NPCs** — an NPC-identity collapse, worse than a repetitive pool.
>
> **The law prevents shared harvests. It does not prevent the same footage arriving by two roads.**
> Only a cross-folder visual comparison finds it. That is a REQUIRED Stage-3 step, and every
> harvest brief must tell the agent to eyeball its candidate against its named collision partner
> before installing.

### 3.3 ⚠️ THE ROOM TRAP — `setting_is_load_bearing: YES` is a corpus bet

Wave 1's clean result: **three of three slots that gated on a ROOM failed. The one that gated on
the BODY succeeded.**

| slot | demand | outcome |
|---|---|---|
| brothel | red-lit paid room | 0 red-lit clips in 4 rounds → bright living room, white-tiled room, POV couch |
| colm | concrete storeroom, crates | 0 in 3 rounds → hallway, **gloryhole**, white bathroom |
| calloway | dim after-hours records room | 0 in 3 rounds → bright open-plan offices, `BANGBROS` watermarks |
| **marsh** | **her hands on him, her eyes up** | **4 coherent clips — the only shippable pool of the four** |

`media.md` §7 Gate 2 warns that a too-specific *gesture* cannot fill a pool (`lab_finish_facial`,
`pool_all_dead` at 24 candidates). **A room the corpus does not shoot is unfillable for exactly the
same reason, and nothing warns about it.** Worse, the doctrine's danger/secrecy/squalor test
actively *causes* the failure: it says "this setting is meaningful", the author writes it into
`must_show`, and the search then hunts a room that does not exist on these hosts.

**The corpus shoots:** offices, bedrooms, bathrooms, kitchens, cars, outdoors, bars, gloryholes,
and POV-anywhere. **It does not shoot:** red-lit brothel rooms, industrial storerooms, dim
after-hours archives.

**Rule going forward — gate on the BODY, score the ROOM.** `must_show` holds bodies, hands, gaze,
posture and who is standing or seated. A setting belongs on the SETTING axis where it can *lose
points*, never in `must_show` where it *rejects*. Add one question to the SCOPE brief before
`setting_is_load_bearing` is ever answered YES: **"does this corpus actually shoot this room?"**
If the answer is no, the setting is not load-bearing no matter what the beat means.

Corollary: when two slots share an act and a room by construction (the five oral slots here), the
durable separator is **camera distance and wardrobe**, not the room. Wave 2 splits the two office
slots that way — calloway takes tight face-level crops and the corporate `cover_analyst` styling,
renner takes the wide tripod side-shot and `cover_dockhand` casual. Both separators are diegetic:
the game really does dress her differently in those two places.

---

## 4. The waves

Cost basis, measured not quoted: `games/vesper/videos` is **388 MB / 116 files = 3.3 MB per clip**
(range 740 K – 5.6 M). Source `videos/` is gitignored (`.gitignore:78`); **both** output trees are
tracked (220 files / 347 MB each), so **every clip lands in git twice**. A 4-clip pool adds 3 clips
≈ **10 MB source / 20 MB committed**.

| Wave | Slots | What | +source | +committed |
|---|---|---|---|---|
| **0** | 1 | `mercer_serve_knees_t5` | — | ✅ **done, rev 104** |
| **1** | 5 | forced-entry oral — every visit, guaranteed | ~50 MB | **~100 MB** |
| **2** | 2 | the Anchor ambient (one shelf already 54 deep) | ~20 MB | **~40 MB** |
| **3** | 6 | the middle poses (vaginal / ride / desk) | ~60 MB | **~120 MB** |
| **4** | 6 | the anal poses | ~60 MB | **~120 MB** |
| | **20** | 1 done + 19 to run | **~190 MB** | **~380 MB** |

Full completion grows the committed video weight by ~55%, on a **public** repo with a 1.4 GB
`.git`. **Each wave is a separate LO gate.** Ship wave 1, look at the real bill, then decide.

### Wave 1 — forced entry (5 slots)

| slot | loop | current size |
|---|---|---|
| `sex/renner_loop_oral_t5.webm` | `loop_renner_office_sex` | 776 K |
| `sex/calloway_loop_oral_t5.webm` | `loop_calloway_sex` | 1.9 M |
| `sex/colm_loop_oral_t5.webm` | `loop_colm_backroom` | 2.2 M |
| `sex/brothel_oral_t5.webm` | `underworld_brothel_loop` | 3.5 M |
| `sex/marsh_oral_t5.webm` | `hunt_marsh_sunday` | 1.1 M |

Exactly one pipeline slice (`SKILL.md` §Batching: 5 items).

### Wave 2 — the Anchor ambient (2 slots)

`amb_renner_cheerup` — a genuine Lane-2 random ambient: `chance 0.2`, `max_triggers_per_day 1`,
19:00–23:00 at the Anchor, gated `renner_office_open` + npc corruption ≥ 10 + `cover_dockhand`
equipped. `media.md` §7's own archetype: *"an ambient crossed fifty times earns four clips."*

- `sex/renner_cheerup_alley_t5.webm` — has 54 stocked candidates from an earlier run. **Per §3 it
  still gets its own fresh search.** The 54 stay on the shelf as extra depth for LO's curation pass;
  they are not the source of the picks. *(Earlier draft of this plan called this slot "free, no new
  search needed" — that was wrong and is exactly what the rule forbids.)*
- `sex/renner_cheerup_oral_t5.webm` — no shelf; a normal run.

Both are branches of a `[group]` gated on spine flags (`renner_anal_once` / `renner_oral_once`).
Gate 3 holds: the *group* carries the escalation, so within one branch nothing varies and rotating
is correct.

### Wave 3 — middle poses (6 slots)

`mercer_serve_desk_t5` · `renner_loop_vaginal_t5` · `calloway_loop_vaginal_t5` ·
`colm_loop_vaginal_t5` · `brothel_client` · `marsh_ride_t5`

### Wave 4 — anal poses (6 slots)

`mercer_serve_glass_t5` · `renner_loop_doggy_t5` · `calloway_loop_anal_t5` · `colm_loop_anal_t5` ·
`brothel_anal_t5` · `marsh_anal_t5`

Waves 3 and 4 are 6 slots each → slice 5 + 1, or 3 + 3. Never start a new SEARCH while the previous
slice's INSTALL is incomplete.

### 4.1 Two housekeeping items inside the waves

- **`sex/brothel_client.webm` carries no tier suffix** while both its siblings are `_t5`. A pool
  conversion already re-keys the shelf and verdict, so **retag it to `brothel_vaginal_t5` in the
  same edit** — it costs nothing extra now and costs a second orphan-repair later. It has no shelf
  to strand.
- **`renner_loop_oral_t5`'s description must be rewritten before its search, not after.**
  *"his hand **gentle** in her hair"* is the exact gesture-specificity signature that returned
  `pool_all_dead` at 24 candidates on `lab_finish_facial_t5` (*"his hand gentle at her head"*).
  Every clip in a pool must satisfy the *same* description; loosen it to the hand *being there*.

---

## 5. Per-slot anchors and query axes

The differentiators are real and they come from the descriptions already in the TOML. **Anchor
terms are exclusive — one column, no repeats.**

| slot | he is | surface / room | light | **ANCHOR** | secondary axis |
|---|---|---|---|---|---|
| `mercer_serve_knees` ✅ | **standing**, clothed | penthouse floor | day, city | ~~hand in hair~~ **burned** | inattention |
| `renner_loop_oral` | **seated**, office chair | between chair and desk | office | **`office chair` / `under the desk`** | he's undone, not in control |
| `calloway_loop_oral` | **seated** | dim office / file room | **dim, after-hours** | **`file room` / `archive` / `after hours`** | plain, no named gesture |
| `colm_loop_oral` | **standing** | **concrete**, storeroom | dim | **`storeroom` / `stockroom` / `concrete floor`** | shelving, bar back room |
| `brothel_oral` | anonymous client | bed room | **red light** | **`red light` / `brothel`** + hand **fisted** | flat, transactional; his face NOT needed |
| `marsh_oral` | small neat client | bed room | red light | **`handjob and blowjob` / `two hands`** | **she watches his face — POV is ALLOWED here** |

### The two hard pairs — resolved in advance

**`brothel_oral` vs `marsh_oral`** — same act, same red-lit room. Split by *what her hands and eyes
do*: brothel is **his fist in her hair, her eyes down, flat**; marsh is **her two hands working him
while she watches his face**. That also inverts the POV rule between them — POV is a defect for
brothel (anonymity needs his body seen as a separate thing) and **fine, often stronger, for marsh**
(the power is her face aimed at the viewer). Decide it in the SCOPE brief, not at judging time.

**`brothel_anal` vs `marsh_anal`** (wave 4) — the worst collision in the game: identical act,
identical room, and today identical queries. Split by **body type**, the only differentiator the
descriptions offer: marsh is a *"small neat client"*, brothel is generic. If body-type terms come
back thin, this pair goes to the word hunt (`chrome_route.md` §1) rather than borrowing. **Flag it
now: this is the likeliest slot in the plan to end `pool_all_dead`.**

---

## 6. Per-slot procedure

Preconditions: Django up on :8000, tree clean, on `main`. Run from `story_gen_django/` with
`source venv/bin/activate`. Absolute `cd` prefixes — working-directory drift bit the last run twice.

### Phase A — convert and prove (no network)

```bash
# 1. Edit the block:  file = "sex/x_t5.webm"  ->  pool_dir = "sex/x_t5", pool = 4
#    Carry description + search_queries over; rewrite them per §3 and §5.
#    Keep the WHY as a comment — every pool block in this game explains itself.

# 2. Seed. The pool must never be empty.
mkdir -p games/vesper/videos/sex/x_t5
git mv games/vesper/videos/sex/x_t5.webm games/vesper/videos/sex/x_t5/incumbent.webm

# 3. Merge FIRST — check_shelves reads 7_final_game.toml, so repair after merge, never before.
python scripts/merge_toml_phases.py games/vesper --validate
python manage.py check_shelves --game vesper --repair

# 4. Prove the pool renders before spending a byte.
python manage.py package_from_toml --file games/vesper/toml_phases/7_final_game.toml \
  --output games/vesper/output --video-folder games/vesper/videos
```

### Phase B — find-media (`.claude/skills/find-media/SKILL.md`)

- **SCOPE brief** → `.find-media/scope/<slot>.md`. Fill `setting_is_load_bearing` honestly (the
  test is danger / secrecy / squalor — *not* "is there a room"), `intended_heat`, frame-checkable
  `must_show` / `avoid`, and **the POV call, decided now**.
- **PLAN** → §3 ledger check, then §5 anchor, then `validate_queries.py`.
- **SEARCH** → Chrome, 2–3 sibling queries. Never `read_page` on a results page.
- **STOCK** → mode `wide` = **12 options**, POSTed before judging. Stocking happens once.
- **JUDGE** → contact sheet, then the **mandatory frame strip** on every animated finalist. Gates
  are binary; quality is HEAT 60 / SETTING 25 / CRAFT 15, and SETTING is `null` — skipped, not
  zeroed — when the room isn't load-bearing.
- **INSTALL** → one `grab` per survivor, up to 4:

```bash
for u in "$U1" "$U2" "$U3"; do
  curl -sS -X POST http://localhost:8000/api/v1/dev/media-finder/grab \
    -H 'Content-Type: application/json' \
    -d "{\"game\":\"vesper\",\"file\":\"sex/x_t5\",\"pool_dir\":\"sex/x_t5\",\"url\":\"$u\",\"source\":\"\"}"
done
```

> ⚠️ **Omit `pool_dir` and the install deletes every same-stem file in the folder** — clip 2 wipes
> clip 1, silently. This is the one way the run can destroy the seeded incumbent.

- **Stop conditions:** 3 sibling-query rounds per slot, 10 query variations total. Three failed
  rounds means the *term* is wrong — go back to the word hunt. **Never end a slot silently**: name
  the rejects and their gate reasons.

### Phase C — rebuild, verify, ledger

```bash
python scripts/merge_toml_phases.py games/vesper --validate
python manage.py package_from_toml --file games/vesper/toml_phases/7_final_game.toml \
  --output games/vesper/output      --video-folder games/vesper/videos
python manage.py package_from_toml --file games/vesper/toml_phases/7_final_game.toml \
  --build paid --output games/vesper/output-paid --video-folder games/vesper/videos
python manage.py check_media --file games/vesper/toml_phases/7_final_game.toml \
  --media games/vesper/videos
```

⚠️ `check_media` takes `--file` + `--media`, **not** `--game` (an earlier draft of this plan had
that wrong and the command just errors out).

Vesper ships **two** builds. Rebuilding only `output/` diverges a released game. No `--dev`, and
**no `--debug`** — a debug build bakes `[VIDEO MISSING]` into the HTML permanently.

---

## 7. Verification, per wave

1. Merge + **both** packages green (*Validation passed / All flag chains valid / Package ready*).
2. **The cycle is in the HTML** — grep `output/index.html` for `media_cycle` and confirm the modulus
   equals the file count in the folder. Output is HTML-escaped, so grep the escaped form (`&quot;`).
3. `check_media --file … --media …` → 0 missing; packager ref/file counts match in **both** trees.
   Cross-check with the review API (`game-review/load?game=vesper`), which reports pool rows as
   "N of 4" — that is the view that would catch a pool the packager silently shipped half-empty.
4. **Prune behaved** — the packager drops the old flat `x_t5.webm` from both output trees once
   nothing references it. Confirm gone, folder present. Curation churn should net near zero.
5. **Live, in a browser** — this is the only check that proves the feature; a green build does not.
   Serve the build (`python3 -m http.server`; Chrome refuses `file://`), `Engine.play` the pose
   node, click the self-loop choice repeatedly, confirm `src` advances `1→2→3→4→1`.
6. **Review UI** — `media.html?id=vesper` (the param is `id`, **not** `game`) reads "N of 4" with a
   tile grid; `find.html` opens on the pool with SELECTED above the shelf.
7. `check_shelves --game vesper` → exactly the **2 pre-existing** orphans (`scenes/_e2e_test`,
   `sex/renner_anal_t5.webm`), no third. The command **exits 1** while they remain — expected, not a
   regression. Do not report it green.
8. `pytest apps/game_generation/tests/ tests/ -q` — no new failures (6 pre-existing `create_user()`
   world failures expected).
9. **Ledger** — `authoring_state.json` entry per wave: slots converted, pool composition, shelf
   depths, queries burned. Bump `book_revision`.

---

## 8. Traps — all of these have bitten, or are guarded by a test

| Trap | Consequence | Guard |
|---|---|---|
| `grab` without `pool_dir` | silently wipes the folder to one file | `tests/test_media_finder_pools.py::test_two_pool_installs_coexist` |
| `check_shelves --repair` before merge | reads a stale `7_final_game.toml`, repairs nothing | merge first, always |
| Rebuilding only `output/` | released game diverges free vs paid | both `package_from_toml` runs |
| `--debug` build | `[VIDEO MISSING]` baked into shipped HTML | never pass it |
| Pool left empty during conversion | the beat renders a hole | seed the incumbent first |
| Converting `file` → `pool_dir` | drops the extension, orphaning shelf + verdict (148 options stranded, measured) | `check_shelves --repair` |
| `.webm`-declared pool lands on `.gif` | none — legitimate | per-entry tag selection picks `<video>`/`<img>` from the real on-disk extension |
| Old saves entering a new pool | none | generator emits an inline `<<if ndef $game_state.media_cycle>>` guard at the render site; `backfillStateDefaults` does *not* cover `$game_state` sub-maps |
| `merge_toml_phases.py` on `media_lab*` | destroys a hand-written `7_final_game.toml` | never run it there |
| `media.html?game=vesper` | "No game id" | the param is `id` |
| Working-directory drift between Bash calls | `source venv/bin/activate` fails | absolute `cd` prefix every call |
| `git add -A` | stages `issue.md` and LO's untracked `.claude/skills/author-game-workspace/` | stage by explicit path only |

---

## 9. The honest caveat

`media.md` §7: *"A pool rotates the picture while the beat's prose stays put — so on a heavily
repeated beat the words become the stale thing."*

These are self-loop nodes. On the 5 clicks it takes to grind `loop_npc_pleasure` to 50, the **same
paragraph** renders 5 times. Pooling the clip fixes half the staleness and makes the other half more
visible. `block_pool` is the matching tool for the prose (it picks whole *blocks*, `random(0,N)`),
and it is **out of scope here** — but if the beats read worse after wave 1, that is why, and it is a
prose problem, not a pool problem.

---

## 10. Explicitly out of scope

- **The 15 finisher clips** (`mercer` / `renner` / `calloway` / `colm` / `brothel` finishers). Gate 3
  passes — the `group` is elected by player *choice* (`sex_finisher_type` 0/1/2), not by escalating
  state, so rotating within a branch is legitimate. But view count is 1× per loop run against the
  pose node's 4–6×, split three ways. Revisit after wave 4, with the real byte bill in hand.
- **The rung clips** — `rung_calloway_oral_t5`, `rung_renner_grope_t4`, `rung_calloway_contact_t4`.
  Real but low-traffic.
- **`cell_sleep`'s four clips.** A `group` banded on `core_strain` (<24 / 24–48 / 48–72 / ≥72) —
  textbook Gate-3 **escalation**. Pooling it would trade the captivity's deterioration arc for a
  slideshow. *Separate defect worth fixing on its own:* its four `description`s are raw search
  queries (`man fucking sleeping woman from behind in dark bedroom pov`), which will misdirect any
  future find-media pass.
- **All 6 `locations/` images.** The engine *cannot* pool them — a `[[locations]] image` resolves
  through a separate single-path route (`v2.py:485`) — and rotating wayfinding art is worse than
  useless.
- **The 99 one-shot media blocks** on non-repeatable canvases, including
  `sex/mercer_first_oral_t5.webm` despite its 143-deep shelf. Gate 1 kills it: three files found,
  shipped and paid for so one can be seen once.
- **The two arousal-weapon clips** (`yard_crawl`, `underworld_gate_check`) — repeatable, but a
  resource-gated escape hatch seen a handful of times.
- **Version bump and portal deploy.** Media-only changes; saves are compatible either way. Both are
  separate LO calls.
- **Skill/doctrine edits** — unless a wave surfaces a real gap, in which case the relevant
  `CHANGELOG.md` gets its dated bullet in the same turn.

---

## 11. Run shape — what is serial, what runs in parallel

LO's call, 2026-07-31. The per-slot pipeline in §6 stays the same; only *who runs it and when*
changes.

```
STAGE 1  serial, one pass, all 18 slots
         convert every block file -> pool_dir + seed the incumbent + merge + ONE build
         to prove every pool renders.  17 of 19 slots live in 5_scenes.toml, so this
         cannot be split.  No network, no downloads — cheap.

STAGE 2  PARALLEL, one agent per slot, each in its own Chrome tab
         SCOPE -> fresh Google search (§3) -> stock -> fetch -> judge -> install
         ⚠️ BLOCKED until the shelf-write lock lands (below).

STAGE 3  serial, once, at the very end
         merge -> both builds (free + paid) -> §7 verification -> cross-slot check
         -> ledger.  A whole-game job, not a per-slot job.
```

### The one blocker — the shelf write race

`_add_option` (`api/v1/media_finder.py:265`) is read-modify-write with **no lock**, and
`_write_options` (`:207`) uses a **fixed** tmp filename. Measured over the real HTTP path,
40 concurrent adds to one shelf:

```
HTTP:   25 x 200      15 x 500
shelf:  16 landed     24 LOST      <- nine "200 OK" responses silently dropped their candidate
```

`_read_options` swallows parse errors and returns `{}` (`:201`), so a torn shelf reads as an
**empty** one with no error anywhere. Django's `runserver` is threaded by default
(`--nothreading` is opt-*out*), so this is the production path.

**Existing shelves are intact** — every run to date stocked serially. This only bites under
Stage 2. Fix: `fcntl.flock` around the read-modify-write plus a PID-unique tmp name (~10 lines),
with a test that reruns the 40-concurrent case and asserts 40 land.

### Measured, and not measured

- **Measured, two SUBAGENTS, 2026-07-31:** each created its own tab, ran its own Google Images
  search, and extracted cleanly. **No content bleed** — every call executed on the tabId it was
  given. 165s of agent work finished in 98s of wall clock, so they genuinely ran in parallel.
  Agent startup is ~25–35s before the first real call.
- **⚠️ Real concurrency artifact, seen once:** agent B's first `javascript_tool` call failed with
  *"Couldn't determine which page this action targets. Re-read tabs_context_mcp and try again."* —
  on a tab it had just created and successfully navigated, with an explicit `tabId` passed. The
  other agent's concurrent navigation appears to clobber the extension's active-page resolution.
  **Recoverable:** one bare `tabs_context_mcp` re-read fixed it, no other change. Every brief must
  tell the agent to expect this and retry that way.
- **Not measured:** 5–8 concurrent. Google's tolerance and how often the targeting artifact fires
  at higher fan-out are both unknown. Wave 1 finds out; the fallback is a smaller fan-out.
- **⚠️ Chrome content guard — the exact cause, isolated:** the extension refuses a JS return value
  containing **query-string-like data**. `[BLOCKED: Cookie/query string data]` was traced to one
  field: `url: location.href`, because a Google search URL is `?q=…&udm=2`. Drop that field and the
  identical snippet returns 74–86 urls. Return only derived values — counts, hostnames, booleans,
  filename stems. **Never `location.href`, never raw HTML.** Not in `chrome_route.md` yet.
- **Brief-writing lesson:** the blocked snippet was blocked because it was **never run before it
  shipped in the brief** — a field was added at authoring time. Both agents followed instructions
  faithfully and both failed identically. **Run any snippet yourself before putting it in a brief.**
- **Token cost:** ~42–43K tokens per agent for trivial read-only recon. Real judging runs cost
  more. Parallelism buys wall-clock, not tokens.

### What still needs one pair of eyes

Cross-slot calibration. Five isolated agents cannot notice *"these two pools drew the same kind
of clip"* — each sees only its own pile. That is a **Stage 3 audit** against the query ledger and
`used_assets.jsonl`, not a reason to serialise Stage 2.
