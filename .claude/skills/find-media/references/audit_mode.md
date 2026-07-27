# Audit mode — checking the media a game ALREADY has

The main flow fills holes. Audit mode does the opposite job: it walks media that is
**already installed and already rendering**, and asks one question per file — *does this
clip show what its beat says it shows?*

It never replaces anything. It produces a prioritised list a human acts on.

## Why it exists

Found by hand in `vesper`: `sex/renner_cheerup_alley_t5.webm` is installed, renders fine,
and shows two people **standing**. Its beat says *"on her knees on dirty concrete behind a
bar."* Nothing in the pipeline was ever going to catch that, because nothing re-checks a
clip against its own beat after INSTALL.

Two measurements make the case that this is a class, not an incident:

- **Approval is not verification.** All 196 entries in
  `games/vesper/.find-media/media_reviews.json` read `approved`, zero `disapproved`. The
  median gap between consecutive approvals is **8.3 seconds** — a flip-and-click pace. The
  alley clip and its sibling were approved 3 seconds apart. `status: "approved"` therefore
  tells you a human *saw a thumbnail*, not that the loop matches the beat. **Audit mode does
  not trust prior approval, and it does not skip approved files.**
- **The blast radius is the whole game.** The walker finds **202 media refs** in
  `vesper`'s `7_final_game.toml`, all 202 present on disk, **112 of them animated**
  (measured this pass). If one clip drifted, the prior is not "one".

## The one law

**NEVER auto-replace. NEVER refetch on your own initiative.** The audit's output is a
claim about a mismatch; the verdict belongs to the human. You surface it, he disapproves
it, and only then does the slot go back through the normal SCOPE → PLAN → SEARCH → STOCK →
JUDGE → INSTALL flow as a refetch.

The reason is not politeness. An audit judgement is made against *your* reading of the
beat, and the beat is prose — the alley clip's drift is unambiguous, but "her affect reads
bored" is not. Auto-replacing on a soft call destroys a file the human may have chosen on
purpose, and destroys it silently.

---

## 1. ENUMERATE — every ref, extension-agnostic

Use the full key set. **A bare `image=` regex finds 38 of 202 refs on `vesper`** (measured
this pass) — it misses `file=`, `video=` and `nav_image=`, which is most of the game.

Compare extensions **agnostically**: the TOML may declare `.jpg` while the disk holds
`.webm`, and that is normal, not a finding — the download API saves using the source URL's
extension and the renderer looks up extension-agnostically (`references/api_behavior.md`).

```bash
GAME=vesper
python3 - "$GAME" <<'PY'
import json, pathlib, re, sys
game = sys.argv[1]
root = pathlib.Path("games") / game
toml = sorted(root.glob("toml_phases/*_final_game.toml"))[-1]
refs = sorted(set(re.findall(r'(?:file|image|video|nav_image)\s*=\s*"([^"]+)"', toml.read_text())))

# stem -> real file on disk, so a .jpg ref resolves to the .webm that actually shipped
disk = {}
for p in (root / "videos").rglob("*"):
    if p.is_file():
        disk[p.relative_to(root / "videos").with_suffix("").as_posix()] = p

rows = []
for ref in refs:
    stem = pathlib.PurePosixPath(ref).with_suffix("").as_posix()
    p = disk.get(stem)
    rows.append({"ref": ref, "path": str(p) if p else None,
                 "present": p is not None,
                 "animated": bool(p) and p.suffix.lower() in {".webm", ".mp4", ".gif"}})

out = root / ".find-media" / "audit"
out.mkdir(parents=True, exist_ok=True)
(out / "inventory.json").write_text(json.dumps(rows, indent=2))
present = [r for r in rows if r["present"]]
print(f"{toml.name}: {len(rows)} refs, {len(present)} present, "
      f"{sum(r['animated'] for r in present)} animated -> {out / 'inventory.json'}")
PY
```

Then reconcile against the two other sources of truth:

- **The game-review API's missing list** — `references/game_review_api.md`. Anything it
  reports missing is a *hole*, not an audit target; hand it to the normal flow. Anything the
  walker finds that the API does not is a coverage gap in the API, and is worth reporting on
  its own.
- **Portraits.** NPC `portrait=`, `[player_portrait]` states and outfits, and
  `customization_fields` image options arrive from the API as `portrait_image` and are in
  scope for an audit like anything else. They were invisible to the API until 2026-07-27 —
  worth knowing, because a game authored before then may hold portraits nobody has ever
  looked at. Audit them with fresh eyes rather than assuming a previous pass covered them.

## 2. PAIR — every file with its beat

A file without its beat is unauditable. For each present ref, pull:

- the block's own `description` (what the author asked for), and
- the **surrounding narrative** — the sibling `paragraph` blocks in the same node or group.

Same pairing `templates/scope_brief.md` does. The description is the spec; the narrative is
what the spec *meant*. In the worked example below, the description says "on her knees" and
the narrative says "on her knees on the filthy concrete, or bent over a crate" — the
narrative is what tells you kneeling is load-bearing and not incidental phrasing.

Also carry the ref's **tier suffix** (`_tN`) forward. Valid tiers are `base`, `location`,
and `t0`–`t8`.

## 3. CLAIMS — extract what is checkable in a frame

Reduce the beat to a short list of claims that a frame can settle. Anything that cannot be
settled by looking is not a claim; drop it rather than guessing.

| Claim | Example from a beat | Checkable? |
|---|---|---|
| **Act** | oral / vaginal / anal / kissing / undressing | Yes — the primary gate |
| **Position** | on her knees / bent over / seated / standing | Yes |
| **People count** | two, and only two | Yes |
| **Who is visible** | the partner's body must be seen (POV would break it) | Yes |
| **Cast** | who is in frame at all — a third body is a fail | Yes |
| **Affect** | wrecked, devoted, bored, frightened | Partly — only when it is legible on a face |
| **Finish shown** | is a visible finish actually *required*, or merely allowed? | Yes, but ask the question — most beats do not require it |

**Affect and finish are the two that get over-claimed.** A beat that says a man is "wrecked"
is describing his interior state, not mandating a facial expression; only raise it when the
media actively contradicts it. And a beat that mentions coming is usually describing the
scene's end, not demanding the clip contain a visible finish — treat "finish required" as
false unless the beat is explicitly about the finish.

## 4. VERIFY — strip the animated, read the static

**Animated files (`.webm` / `.mp4` / `.gif`) get a frame strip.** `.gif` is included —
`video_frames.py` treats it as a video (`VIDEO_EXTS`, `video_frames.py:45`).

```bash
python3 .claude/skills/find-media/scripts/video_frames.py \
  --videos-dir games/<game>/videos/sex \
  --mode strip --frames 4 \
  --out-dir games/<game>/.find-media/audit/strips
```

Batch mode writes `<stem>_strip.jpg` per clip, which is one shell round-trip per folder
instead of one per file. Raise `--frames` to 8 on any clip you are about to call a
mismatch — a 4-frame strip is a claim about 4 instants, and a finding deserves the denser
sample before you write it down.

**Static files (`.jpg` / `.png`) get a single Read.** A still cannot be stripped, so the
contact-sheet judgement is the judgement. This is the same split the main flow uses: every
animated finalist is strip-verified; static finalists are judged from the sheet.

`video_frames.py` exits **3** when ffmpeg/ffprobe is not on PATH. That is the
degrade-gracefully code — report the animated files as `unverified` and carry on with the
static ones. **Never crash the audit on it**, and never silently mark an unstripped clip
as passing.

While the file is open, two mechanical checks are nearly free:

```bash
python3 .claude/skills/find-media/scripts/tier_format_check.py \
  --file games/<game>/videos/sex/<name>.webm --tier t5 --json

python3 .claude/skills/find-media/scripts/dedup_tracker.py \
  --check games/<game>/videos/sex/<name>.webm --game <game> --global
```

Images must be ≥ **1024 B**, animated ≥ **51200 B** (`tier_format_check.py:48`, `:49`), and
it checks magic bytes, so an HTML error page saved under a `.webm` name is caught here.

The dedup check earns its place in an audit specifically: the same clip installed against
two different beats is invisible slot-by-slot and obvious across the inventory. It cannot
be a HIGH on its own — reuse is sometimes deliberate — but it is worth a **MED** row so the
human can decide.

### This step is a GATE, never a score

Audit checks **correctness only**. Act, position, people count, who is visible, cast, affect
and finish are **pass or fail** — they earn no points and they lose none.

Do not score an installed clip on HEAT / SETTING / CRAFT and do not compute a total. Those
three axes exist to rank *candidates against each other* when stocking a shelf. There is no
accept threshold anywhere in this skill, and inventing one here would let a correct-but-dull
clip get flagged for replacement because it "scored low" — which is the exact bug the
scoring rewrite exists to kill.

**Setting is only a claim when it is load-bearing** — when the setting carries danger,
secrecy, or squalor. Otherwise it is skipped and recorded as `null`. A bright kitchen behind
a beat that never cared about the room is **not a finding**.

## 5. REPORT — prioritised, and owned by the human

Write one row per audited file to `games/<game>/.find-media/audit/findings.jsonl`:

```json
{"ref": "sex/renner_cheerup_alley_t5.webm", "tier": "t5", "verdict": "MISMATCH",
 "severity": "HIGH", "gates_failed": ["act", "position"],
 "beat_claim": "on her knees on dirty concrete behind a bar, oral, in the dark",
 "media_shows": "both figures standing against a wall, underwear at the thighs, warm daylight",
 "evidence": "games/vesper/.find-media/audit/strips/renner_cheerup_alley_t5_strip.jpg",
 "frames_sampled": 8, "audited_at": "2026-07-27T12:00:00+00:00"}
```

Severity, and what each one means for the human:

| Severity | Meaning | Action he takes |
|---|---|---|
| **HIGH** | A correctness gate fails — the media contradicts the beat | Disapprove and refetch |
| **MED** | Gates hold, but a named `must_show` element is absent, or a mechanical gate fails (tier/format/size/dedup) | His call; often a re-crop or a re-grab |
| **LOW** | Drift no gate covers (beat says "seated", man is standing), or a craft defect like a burned-in watermark | Usually note-and-move-on |

Sort HIGH first. Report the count of each, and **name the evidence path** on every row — a
finding the human cannot see for himself is an assertion.

### Feeding the review page

The review UI reads `games/<game>/.find-media/media_reviews.json` via
`GET /api/v1/dev/media-review/list?game=<slug>` (`media_review.py:224`). `game` is a **query
param** on both media-review endpoints.

**Trap, verified at `media_review.py:257-265`:** `post_review` reads `status` and `note` off
the body, then upserts **both** on every call via a single `entry.update`. `status` defaults
to `None`, and `None` is an explicitly legal value. So a POST that sends a `note` **without**
re-sending the existing `status` silently clears the human's verdict, and a POST that sends
`status` without `note` wipes the note.

Because of that, the default is: **write findings to `findings.jsonl` and report them in
chat.** Only POST to media-review when the human asks you to, and when you do, read the
current entry first and re-send its `status` verbatim alongside your note.

When he disapproves a slot, it re-enters the normal flow as a refetch. A refetch **stocks
first and prunes after** — take `t0 = now()` in ISO-8601, stock the new candidates, then
`POST options/clear {game, file, before: t0}`, which drops only what predates `t0` and
always keeps `origin: "previous"` entries (`media_finder.py:331`). Never clear on the way
in; a pool destroyed before its replacement exists is a harvest lost.

## 6. BATCHING + RESUME

Audits run over whole games — 202 refs on `vesper` — so they will be interrupted.

- **Slice it.** Process ~10 files per slice, appending to `findings.jsonl` after each
  slice, not at the end. Strips are cheap; the Reads are the cost.
- **Persist under the game.** Everything lands in `games/<game>/.find-media/audit/`:
  `inventory.json`, `strips/`, `findings.jsonl`. Never `/tmp` — evidence there has been
  wiped mid-run before, taking the pool with it.
- **Resume by skipping what is already judged.** On rerun, load the `ref` values already in
  `findings.jsonl` and skip them:

```bash
python3 - vesper <<'PY'
import json, pathlib, sys
root = pathlib.Path("games") / sys.argv[1] / ".find-media" / "audit"
inv = json.loads((root / "inventory.json").read_text())
done = set()
f = root / "findings.jsonl"
if f.exists():
    done = {json.loads(line)["ref"] for line in f.read_text().splitlines() if line.strip()}
todo = [r for r in inv if r["present"] and r["ref"] not in done]
print(f"{len(done)} judged, {len(todo)} remaining")
print("\n".join(r["ref"] for r in todo[:10]))
PY
```

Re-audit a file only when its beat text changed. Add `--force` behaviour by hand (delete the
row) rather than re-judging the whole game.

---

## Worked example — the alley clip

**The ref.** `sex/renner_cheerup_alley_t5.webm`, declared in
`games/vesper/toml_phases/7_final_game.toml:4700`, in canvas node `base`, inside a group
gated on `renner_anal_once`.

**The beat.** Description: *"A woman on her knees on dirty concrete behind a bar giving a
slumped man oral in the dark, a crate beside them."* The sibling paragraph confirms it is
not incidental phrasing: *"gets him out of the bar and into the dark behind it … on her
knees on the filthy concrete, or bent over a crate."*

**The claims.**

| Claim | Value | Load-bearing? |
|---|---|---|
| Act | oral | Yes — gate |
| Position | on her knees (or bent over a crate) | Yes — gate |
| People count | 2 | Yes — gate |
| Who is visible | the slumped man must be seen; his collapse is the heat | Yes — gate |
| Setting | dark, behind a bar, dirty concrete | **Yes** — squalor and secrecy both carry |
| Finish shown | not required | — |

**The verification.** The clip runs 10.0s. A 4-frame strip flagged it; an 8-frame strip
confirmed across the whole loop:

```bash
python3 .claude/skills/find-media/scripts/video_frames.py \
  --video games/vesper/videos/sex/renner_cheerup_alley_t5.webm \
  --mode strip --frames 8 --tile-px 240 \
  --out games/vesper/.find-media/audit/strips/renner_cheerup_alley_t5_strip8.jpg
```

**What all 8 frames show:** two figures **standing** against a concrete wall outdoors. The
woman is upright, facing the wall, underwear pulled down around her thighs; the man stands
behind her in jeans. Warm **daylight** cast, green standing water and litter on the ground,
a handbag beside them. No kneeling in any frame. No oral in any frame. A watermark is burned
across the middle of the image.

**The finding.**

| Field | Value |
|---|---|
| Verdict | `MISMATCH` |
| Severity | **HIGH** |
| Gates failed | `act` (standing sex, not oral), `position` (upright, never kneeling) |
| Also | setting drifts dark → daylight, and setting **is** load-bearing here, so it counts |
| Craft note | burned-in watermark (LOW on its own; noted, not the reason) |
| Prior review status | `approved` — which is exactly why the audit does not trust that field |

Two gates fail, so it is HIGH regardless of anything else. Note what did **not** happen: no
total was computed, no threshold was compared against, and the watermark did not need to
"add points" to reach a verdict. Act failed; that ends it.

**Contrast — its sibling passes.** `sex/renner_cheerup_oral_t5.webm` (beat: *"a woman
kneeling beside a cigarette machine in a dim bar giving a seated man fast oral, his hand in
her hair"*) strips to a dim bar interior — counter, stools, bottles — with a blonde woman
leaning in giving oral to a man in a jacket, his hand at her head. Act ✓, count ✓, cast ✓,
setting ✓, who-is-visible ✓. The man reads **standing** rather than seated, and there is a
burned-in `RUSSIANINSTITUTE.COM` watermark.

That is a **LOW**, not a finding that demands replacement. No gate failed. Standing-vs-seated
is drift the beat does not hang on, and the watermark is a craft defect the human may well
accept. Writing this up as HIGH because it is imperfect is how an audit becomes noise the
human stops reading.

---

## A clean audit is a real result

If you strip 40 clips and every one matches its beat, **the answer is "40 audited, 0
mismatches"** — reported plainly, with the count and the evidence directory, and nothing
else.

Do not pad it. Do not go hunting for LOWs to justify the run, do not downgrade the gate to
manufacture a HIGH, and do not append a list of clips that are "fine but could be better" —
that list is a scoring pass wearing an audit's clothes, and it hands the human a pile of
work that no defect asked for.

An audit that finds nothing has established that the game's media matches its beats. That is
the outcome you wanted.
